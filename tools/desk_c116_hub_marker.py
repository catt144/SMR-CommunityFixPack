#!/usr/bin/env python3
"""C116 synchronous departure controls against archived 1.1.1.405907 bodies.

Run: python tools/desk_c116_hub_marker.py

Predictions: a marked walker off the hub loses marker and starts outside time;
a real in-flight ramp and a visual position still on the hub retain shelter;
an indoor stale hub holder is removed through native holder bookkeeping;
without the module the same walk keeps the marker. The fixture supplies hexes,
visual positions and pf.Step, so real movement timing remains for hubset 07.
"""
import os
from pathlib import Path

import deskbench as db


BUILD = "1.1.1.405907"
db.TREES[BUILD] = os.path.join(
    os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
    BUILD, "Src")
HELPER = Path(db.REPO) / "Code/Hubset_OnHubNow.lua"
MODULE = Path(db.REPO) / "Code/Fix_HubMarkerDeparture.lua"

PRELUDE = r'''
Unit = {passage_hub=false}
Colonist = setmetatable({}, {__index=Unit})
Holder = {}
PassageHubBase = {hub_domes=false}
const = {pfFinished=0}
pf = {}
function pf.Step(unit)
  if unit.next_hex then unit.hex=unit.next_hex end
  if unit.next_visual then unit.visual_hex=unit.next_visual end
  return unit.step_status or const.pfFinished
end
pfStep = pf.Step -- the file-local alias immediately before native Unit:Step
pfFinished = const.pfFinished
function IsValid(o) return type(o)=="table" and o.valid==true end
function IsKindOf(o, kind)
  return type(o)=="table" and (o.kind==kind or o.parents and o.parents[kind]) or false
end
function IsBeingDestructed() return false end
function ResolveMap(o) return o and o.map end
function WorldToHex(x, y) if type(x)=="table" then return x.hex, 0 end return x, 0 end
function HexGridGetObject(grid, q, r, class)
  assert(class=="PassageHub" and r==0)
  return grid[q]
end
function GetObjectHexGrid(unit) return unit.map.object_hex_grid end
function IsValidPos(unit) return unit:IsValidPos() end
function GetTopmostParent(unit) return unit end
function GetDomeAtPoint(grid, unit) return unit.pos_dome end
function IsObjInDome(holder) return holder.parent_dome end
function HideIfHeldDetached() end
function Camera3pFollow() error("unexpected camera follow") end
CameraFollowObjWaiting = false
function table.find(t, x)
  for i, v in ipairs(t) do if v==x then return i end end
end
function table.remove_entry(t, x)
  for i=#t,1,-1 do if t[i]==x then table.remove(t,i) end end
end
function Unit:IsValidPos() return self.pos_valid~=false end
function Unit:GetMap() return self.map end
function Unit:GetVisualPosXYZ() return self.visual_hex, 0, 0 end
function Unit:SetOutside(outside) self:SetOutsideEffects(outside) end
function Colonist:SetOutsideEffects(outside)
  self.outside_start = outside and 1234 or false
  self.outside_updates = self.outside_updates + 1
end
function make_case()
  local map={object_hex_grid={}}
  local hub=setmetatable({kind="PassageHub",parents={PassageHubBase=true,Holder=true},
    valid=true,map=map,hex=0,units={},connected_passages={},draining_passages={}},
    {__index=Holder})
  function hub:GetMap() return self.map end
  map.object_hex_grid[0]=hub
  local c=setmetatable({kind="Colonist",parents={Colonist=true,Unit=true},
    valid=true,map=map,hex=0,visual_hex=0,holder=false,passage_hub=hub,
    traversing_passage=false,outside_start=false,outside_updates=0},
    {__index=Colonist})
  return c,hub,map
end
SMRFixPack={OnHubNow=false}
function SMRFixPack.Require(_, specs)
  for _, s in ipairs(specs) do
    if s.class and s.method and type(_G[s.class][s.method])~="function" then return s.class.."."..s.method end
    if s.class and not s.method and type(_G[s.class])~="table" then return s.class end
    if s.global and type(_G[s.global])~="function" then return s.global end
    if s.path and type(SMRFixPack.OnHubNow)~="function" then return "OnHubNow" end
    if s.test and not s.test() then return s.reason end
  end
end
function SMRFixPack.Register(id, def)
  assert(id=="HubMarkerDeparture")
  local err=def.apply()
  if EXPECT_DECLINE then assert(err, "shape change must decline"); DECLINED=err
  else assert(not err, tostring(err)) end
end
'''

BODIES = (
    ("Lua/Units/Unit.lua", r"^function Unit:Step\("),
    ("Lua/Units/Unit.lua", r"^function Unit:SetHolderOnMap\("),
    ("Lua/Units/Unit.lua", r"^function Unit:SetHolder\("),
    ("Lua/Units/Unit.lua", r"^function Unit:UpdateOutside\("),
    ("Lua/Units/Colonist.lua", r"^function Colonist:StopMoving\("),
    ("Lua/Units/Colonist.lua", r"^function Colonist:SetHolderOnMap\("),
    ("Lua/Buildings/Holder.lua", r"^function Holder:OnExitHolder\("),
    ("Lua/Buildings/Holder.lua", r"^function Holder:OnEnterHolder\("),
    ("Lua/Buildings/Dome.lua", r"^function IsUnitInDome\("),
)


def runtime(fixed, decline=False):
    rt = db.lua_runtime()
    db.load_at(rt, PRELUDE, "=c116_fixture")
    for rel, pattern in BODIES:
        body, first, _ = db.body(rel, pattern, BUILD)
        db.load_at(rt, body, "=" + rel, first)
    db.load_at(rt, db.read(str(HELPER)), "=Code/Hubset_OnHubNow.lua")
    if fixed:
        if decline:
            rt.execute("Unit.passage_hub=nil; EXPECT_DECLINE=true; native_step=Unit.Step")
        db.load_at(rt, db.read(str(MODULE)), "=Code/Fix_HubMarkerDeparture.lua")
    return rt


def case(name, fixed, arrange, check):
    rt = runtime(fixed)
    rt.execute("c,h,map=make_case()")
    rt.execute(arrange)
    rt.execute("c:Step()")
    assert rt.eval(check), name
    print(f"PASS {name}")


def main():
    case("walk-off clears marker and starts timer", True,
         "c.next_hex=5; c.next_visual=5",
         "not c.passage_hub and c.outside_start==1234")
    case("module-removed walk remains marked", False,
         "c.next_hex=5; c.next_visual=5",
         "c.passage_hub==h and c.outside_start==false")
    case("real traversal ramp keeps shelter", True,
         "p={valid=true,traversing_colonists={c}}; h.connected_passages[p]=true; "
         "c.traversing_passage=p; c.next_hex=5; c.next_visual=5",
         "c.passage_hub==h and c.outside_start==false")
    case("visual still on hub keeps shelter", True,
         "c.next_hex=5; c.next_visual=0",
         "c.passage_hub==h and c.outside_start==false")
    case("next step after visual departure clears", True,
         "c.next_hex=5; c.next_visual=0; c:Step(); c.next_visual=5",
         "not c.passage_hub and c.outside_start==1234")
    case("stale holder removed and outside starts", True,
         "c.holder=h; h.units={c}; c.next_hex=5; c.next_visual=5",
         "not c.passage_hub and not c.holder and #h.units==0 and c.outside_start==1234")
    case("indoor stale holder removed without exposure", True,
         "c.holder=h; h.units={c}; c.pos_dome={}; c.next_hex=5; c.next_visual=5",
         "not c.passage_hub and not c.holder and #h.units==0 and c.outside_start==false")
    case("standing on hub keeps marker", True, "", "c.passage_hub==h and c.outside_start==false")
    rt = runtime(True)
    rt.execute("c,h,map=make_case(); c.hex=5; c.visual_hex=5; c:StopMoving()")
    assert rt.eval("not c.passage_hub and c.outside_start==1234")
    print("PASS interrupted walk StopMoving fallback")
    rt = runtime(True)
    rt.execute("c,h,map=make_case(); c.hex=5; c.visual_hex=5; "
               "vehicle={kind='Holder',valid=true,map=map,units={},OnEnterHolder=Holder.OnEnterHolder}; "
               "function vehicle:GetMap() return self.map end; c:SetHolderOnMap(vehicle,map)")
    assert rt.eval("not c.passage_hub and c.holder==vehicle and c.outside_start==false")
    print("PASS holder transition after departure")
    rt = runtime(True, decline=True)
    assert rt.eval("DECLINED and Unit.Step==native_step")
    print("PASS changed marker shape declines without wrapper")


if __name__ == "__main__":
    main()
