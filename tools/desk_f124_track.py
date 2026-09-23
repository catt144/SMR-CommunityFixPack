#!/usr/bin/env python3
"""F124 track rebase: archived split/repair bodies, refunds, shells and branch decline.

Runs complete modules under Lua via deskbench. Native split, ProcessAllElements,
element Done, track destruction and graph expansion are extracted, never retyped.
The engine hex grid is a deterministic line fixture with optional disconnected
fragments. ProcessTrackElements geometry is an explicit stub: it records inputs
and stamps physical order, so these tests verify delegation/exclusion, NOT the
engine's geometry, terrain or render effects. IsValid/DoneObject model object
lifetime; no station connectors or real game threads are exercised.
Pre-rebase falsifiers come from pinned git 16ff1aa; guard-reverted scratch text
is derived from the working module and is never written over the source.
"""
from pathlib import Path
import hashlib
import os
import sys

import deskbench as db

ROOT = Path(db.REPO)
ARCHIVE = Path(os.environ.get("SMR_SRCARCHIVE", "B:/Dev/SMR/SMR-Shared/SMR-SrcArchive"))
BUILD = "1.1.1.405907"
db.TREES[BUILD] = str(ARCHIVE / BUILD / "Src")
db.TREES["1.1.0.403908"] = str(ARCHIVE / "1.1.0.403908" / "Src")
WIPE = ROOT / "Code/Fix_TrackSalvageWipe.lua"
REFUND = ROOT / "Code/Fix_TrackSalvageRefund.lua"

PRELUDE = db.ENGINE_SHIMS + r'''
OnMsg = {}; TrackBase = {}; TrackGridElement = {}; Colonist = {MigrateStep=function() end}
ConstructionGroupLeader = {Complete=function() end}
ConstructionSite = {MarkSpentResources=function() end}
empty_table = {}; SMRFixPack_Disabled = {}; LOG={}; OBJECTS={}; PROCESSED={}; DROPS={}
function ret_false() return false end
function IsValid(o) return type(o)=="table" and o.live == true end
function IsBeingDestructed(o) return o and o.dying == true end
function table.icopy(t) local r={} for i,v in ipairs(t) do r[i]=v end return r end
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
function table.remove_value(t,v) local i=table.find(t,v) if i then table.remove(t,i) end end
table.remove_entry=table.remove_value
function table.insert_unique(t,v) if not table.find(t,v) then table.insert(t,v) end end
function ripairs(t) local i=#(t or {})+1 return function() i=i-1 if i>0 then return i,t[i] end end end
function IsTrackElementStraight(el) return el.straight end
function Msg(...) end
function RemoveObjectFromNotification(...) end
function RebuildTrainRoutes() ROUTES=(ROUTES or 0)+1 end
function ResolveMap(o) return MAP end
MAP={object_hex_grid={}}
function MAP:SuspendPassEdits() self.suspended=(self.suspended or 0)+1 end
function MAP:ResumePassEdits() self.suspended=self.suspended-1 end
function MAP:MapForEach(_,class,cb,arg) for _,o in ipairs(OBJECTS) do if o.class==class then cb(o,arg) end end end
function AllMapsForEach(_,class,cb) for _,o in ipairs(OBJECTS) do if o.class==class then cb(o) end end end
function HexGetTrackGridElement(grid,q,r)
  local found
  for _,o in ipairs(OBJECTS) do
    if o.class=="TrackGridElement" and IsValid(o) and not o.dying and o.q==q and o.r==r then
      if o.is_construction_site then return o end
      found=o
    end
  end
  return found
end
HexNeighbours={{xy=function() return -1,0 end},{xy=function() return 1,0 end}}
function ProcessTrackElements(map,elements)
  PROCESSED[#PROCESSED+1]=table.icopy(elements)
  for _,el in ipairs(elements) do el.node_idx=el.q end
end
function DoneObject(o)
  if not IsValid(o) or o.dying then return end
  o.dying=true
  if o.Done then o:Done() end
  o.live=false; o.dying=false
end
function CreateGameTimeThread() error("fixture unexpectedly created a station thread") end
local BASE={}
function BASE:GetMap() return MAP end
function BASE:GetPos() return self.q or 0 end
function BASE:GetVisualPos() return self:GetPos() end
function BASE:GetAngle() return 0 end
function BASE:IsValidPos() return true end
function BASE:SetPos(p) self.pos=p end
setmetatable(TrackBase,{__index=BASE}); setmetatable(TrackGridElement,{__index=BASE})
function PlaceObjectIn(class,map)
  local o=setmetatable({class=class,live=true,assigned_vehicles={},city={labels={Train={}}}}, {__index=TrackBase})
  o:Init(); OBJECTS[#OBJECTS+1]=o; return o
end
function TrackBase:GetStartStation() return false end
function TrackBase:GetEndStation() return false end
function TrackBase:DisconnectStations() end
function TrackBase:DisconnectFromGrids() self.supply_tunnel_set=false; self.disconnected=true end
Building={}
function Building:CalcRefundAmount(n) return n/2 end
function Building:AddRefundResource(t,r,n) t[#t+1]={resource=r,amount=n} end
TrackBase.CalcRefundAmount=Building.CalcRefundAmount
TrackBase.AddRefundResource=Building.AddRefundResource
function TrackBase:ReturnResources() for _,x in ipairs(self:GetRefundResources()) do DROPS[#DROPS+1]=x end end
function PlaceResourceStockpile_Delayed(pos,map,r,n,angle,flag) DROPS[#DROPS+1]={resource=r,amount=n} end
GroupResourceIds={ConstructionResources={"Metals"}}
UIColony={construction_cost={GetConstructionCost=function() return 200 end}}
SMRFixPack={fixes={}}
function SMRFixPack.Log(...) end
function SMRFixPack.Require(id,specs)
 for _,s in ipairs(specs) do
  if s.test or s.probe then local ok,v=pcall(s.test or s.probe) if not ok or v~=true then return s.reason or "decline" end
  elseif s.class then if type(_G[s.class])~="table" or type(_G[s.class][s.method])~="function" then return "missing "..s.class.."."..s.method end
  elseif s.global and type(_G[s.global])~="function" then return "missing "..s.global end
 end
end
function SMRFixPack.Register(id,def)
 local err=SMRFixPack_Disabled[id] and "disabled" or def.apply()
 SMRFixPack.fixes[id]={status=err and "inactive" or "active",detail=err}
end
function SMRFixPack.WhenActive(id,fn) return function(...)
 if SMRFixPack.fixes[id].status=="active" and not SMRFixPack_Disabled[id] then return fn(...) end
end end
function fixture(n,curved,repair_index,plain_index,gap)
 local t=PlaceObjectIn("TrackBase",MAP); local es={}
 for i=1,n do
  local e=setmetatable({class="TrackGridElement",live=true,q=i+(gap and i>=gap and 10 or 0),r=0,node_idx=i,
    pillared=true,straight=not curved,track_obj=t,connections={},is_construction_site=i==plain_index}, {__index=TrackGridElement})
  es[i]=e; OBJECTS[#OBJECTS+1]=e
  table.insert(e.is_construction_site and t.elements_under_construction or t.elements,e)
 end
 local cs
 if repair_index then
  local e=es[repair_index]
  cs=setmetatable({class="TrackGridElement",live=true,q=e.q,r=0,node_idx=false,pillared=true,straight=not curved,
    track_obj=t,connections={},is_construction_site=true,broken=e,construction_group={}}, {__index=TrackGridElement})
  e.broken=cs; t.elements_under_construction[#t.elements_under_construction+1]=cs
  t.repair_cgs[1]=cs.construction_group; OBJECTS[#OBJECTS+1]=cs
 end
 return t,es,cs
end
function amount() local n=0 for _,v in ipairs(DROPS) do n=n+v.amount end return n end
function check_arrays()
 for _,t in ipairs(OBJECTS) do if t.class=="TrackBase" and IsValid(t) then
  for _,e in ipairs(t.elements) do assert(IsValid(e) and e.track_obj==t and not e.is_construction_site,"completed array") end
  for _,e in ipairs(t.elements_under_construction) do assert(IsValid(e) and e.track_obj==t and e.is_construction_site,"construction array") end
 end end
end
'''


def native(rt, rel, selector, build=BUILD):
    text, first, _ = db.body(rel, selector, tree=build)
    db.load_at(rt, text, "=" + build + "/" + rel, first)


def runtime(module=None, branch=True, refund=True, build=BUILD):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    track = "Lua/Buildings/Track.lua"
    element = "Lua/Buildings/TrackElement.lua"
    for name in ("Init", "Done", "UpdatePos", "DestroyAssignedTrains", "CanDelete", "UpdateEndElements", "OnDemolish", "GetRefundResources", "ProcessAllElements"):
        native(rt, track, r"^function TrackBase:" + name + r"\(", build)
    text, first, _ = db.span(track, [r"^local function check_track_elements_on_track_delete\(", r"^function TrackBase:DestroyTrackElements\("], tree=build)
    db.load_at(rt, text, "=" + build + "/" + track, first)
    for name in ("Done", "Demolish", "DemolishAndSplitTrack"):
        native(rt, element, r"^function TrackGridElement:" + name + r"\(", build)
    text, first, _ = db.span(element, [r"^local alien_search_visited,", r"^function ExpandTrackFromElement\("], tree=build)
    db.load_at(rt, text, "=" + build + "/" + element, first)
    if not branch:
        rt.execute("Colonist.MigrateStep=nil")
    if module is not None:
        db.load_at(rt, module, "=" + str(WIPE))
    if refund:
        db.load_at(rt, REFUND.read_text(encoding="utf-8"), "=" + str(REFUND))
    return rt


CASES = {
    "curved split and physical refund": r'''
local t,e=fixture(7,true); e[4].construction_cost_at_completion={Metals=200}
local train={live=true,track=t,DestroySilent=function(self) self.live=false end}; t.city.labels.Train={train}
e[4]:Demolish(false)
assert(not IsValid(e[4]) and IsValid(e[1]) and IsValid(e[7]))
assert(IsValid(train) and not t.demolishing and amount()==100); check_arrays()
''',
    "short start trim preserves survivor": r'''
local t,e=fixture(3,false); e[1]:Demolish(false)
assert(not IsValid(e[1]) and IsValid(e[2]) and IsValid(e[3]) and not t.demolishing); check_arrays()
''',
    "short end trim preserves survivor": r'''
local t,e=fixture(3,false); e[3]:Demolish(false)
assert(not IsValid(e[3]) and IsValid(e[1]) and IsValid(e[2]) and not t.demolishing); check_arrays()
''',
    "repair split ownership and repair_cgs": r'''
local t,e,cs=fixture(7,false,6,5); e[4].construction_cost_at_completion={Metals=200}
e[4]:Demolish(false)
assert(IsValid(cs) and cs.node_idx==false and cs.track_obj==e[6].track_obj)
assert(table.find(cs.track_obj.elements_under_construction,cs))
assert(table.find(cs.track_obj.repair_cgs,cs.construction_group))
assert(#t.repair_cgs==0 and amount()==100)
for _,list in ipairs(PROCESSED) do assert(not table.find(list,cs),"repair site reached geometry") end
assert(#PROCESSED==3,"preprocess plus both survivors"); check_arrays()
''',
    "repair click delegates once and forwards skip": r'''
local t,e,cs=fixture(7,false,4); e[4].construction_cost_at_completion={Metals=200}
cs:Demolish(false,true)
assert(not IsValid(cs) and not IsValid(e[4]) and amount()==100)
assert(#PROCESSED==0); check_arrays()
''',
    "disconnected survivor is rehomed": r'''
local t,e,cs=fixture(8,false,8,nil,8); e[4]:Demolish(false)
assert(IsValid(e[8]) and e[8].track_obj~=e[7].track_obj)
assert(cs.track_obj==e[8].track_obj and table.find(cs.track_obj.repair_cgs,cs.construction_group)); check_arrays()
''',
    "plain site trim refunds completed stamps": r'''
local t,e=fixture(5,false,nil,2); e[1].construction_cost_at_completion={Metals=200}
e[2]:Demolish(false)
assert(not IsValid(e[1]) and not IsValid(e[2]) and IsValid(e[3]) and amount()==100); check_arrays()
''',
    "whole salvage refund and shell cleanup": r'''
local t,e,cs=fixture(7,false,5); e[1].construction_cost_at_completion={Metals=200}; e[7].construction_cost_at_completion={Metals=400}
local train={live=true,track=t,DestroySilent=function(self) self.live=false end}; t.city.labels.Train={train}
e[3]:Demolish(true)
assert(not IsValid(train) and not IsValid(t) and not IsValid(cs) and amount()==300)
for _,el in ipairs(e) do assert(not IsValid(el)) end
''',
    "empty trim refunds before auto-deleted track disappears": r'''
local t,e=fixture(1,false); e[1].construction_cost_at_completion={Metals=200}; e[1]:Demolish(false)
assert(not IsValid(t) and not t.demolishing and amount()==100)
''',
    "unindexable physical element declines": r'''
local t,e=fixture(7,false); e[4].node_idx=false; e[3]:Demolish(false,true)
for _,el in ipairs(e) do assert(IsValid(el)) end
''',
    "pre-sort processing repairs colliding physical indices": r'''
local t,e=fixture(7,false)
for _,el in ipairs(e) do el.node_idx=1 end
e[4]:Demolish(false)
assert(not IsValid(e[4]) and IsValid(e[3]) and IsValid(e[5]) and e[5].node_idx==5); check_arrays()
''',
    "surviving stamps are not refunded": r'''
local t,e,cs=fixture(7,false,6); e[6].construction_cost_at_completion={Metals=600}
e[4]:Demolish(false); assert(IsValid(e[6]) and IsValid(cs) and amount()==0); check_arrays()
''',
    "shared repair group rebuilt once on each side": r'''
local t,e,left=fixture(9,false,2)
local right=setmetatable({class="TrackGridElement",live=true,q=8,r=0,node_idx=false,pillared=true,straight=true,
 track_obj=t,connections={},is_construction_site=true,broken=e[8],construction_group=left.construction_group}, {__index=TrackGridElement})
e[8].broken=right; t.elements_under_construction[#t.elements_under_construction+1]=right; OBJECTS[#OBJECTS+1]=right
e[5]:Demolish(false)
assert(left.track_obj~=right.track_obj and #left.track_obj.repair_cgs==1 and #right.track_obj.repair_cgs==1)
assert(left.track_obj.repair_cgs[1]==right.track_obj.repair_cgs[1]); check_arrays()
''',
    "supply grid disconnected before trim": r'''
local t,e=fixture(7,false); t.supply_tunnel_set=true; e[1]:Demolish(false)
assert(t.disconnected and not t.supply_tunnel_set); check_arrays()
''',
    "load heals legacy shell and orphan but preserves healthy track": r'''
local t,e=fixture(3,false); local shell=PlaceObjectIn("TrackBase",MAP)
shell.elements=false; shell.elements_under_construction=false; shell.assigned_vehicles=false; shell.demolishing=true
local ot,oe=fixture(1,false); oe[1].track_obj=false; ot.elements={}
OnMsg.LoadGame()
assert(not IsValid(shell) and not IsValid(oe[1]) and IsValid(t) and IsValid(e[1]))
''',
    "load veto is inert": r'''
local t,e=fixture(1,false); e[1].track_obj=false; t.elements={}
SMRFixPack_Disabled.TrackSalvageWipe=true; OnMsg.LoadGame(); assert(IsValid(e[1]))
''',
}


def main():
    module = WIPE.read_text(encoding="utf-8")
    original_hash = hashlib.sha256(WIPE.read_bytes()).hexdigest()
    old = db.git_show(db.REPO, "16ff1aa", "Code/Fix_TrackSalvageWipe.lua")
    results = []

    def run(name, rt, text, expected_failure=False):
        try:
            rt.execute(text)
            failed = False
        except Exception as exc:
            failed = True
            if not expected_failure:
                print("ERROR", name, str(exc))
        ok = failed if expected_failure else not failed
        results.append((name, ok))
        print(("PASS " if ok else "FAIL ") + name)

    for name, text in CASES.items():
        run(name, runtime(module), text)
    for name in ("repair split ownership and repair_cgs", "repair click delegates once and forwards skip", "disconnected survivor is rehomed"):
        run("native control: " + name, runtime(), CASES[name])
    for name in ("curved split and physical refund", "short start trim preserves survivor", "whole salvage refund and shell cleanup"):
        run("native defect falsifier: " + name, runtime(), CASES[name], True)
    for name in ("repair split ownership and repair_cgs", "disconnected survivor is rehomed"):
        run("git pre-rebase falsifier: " + name, runtime(old), CASES[name], True)
    decline = 'assert(SMRFixPack.fixes.TrackSalvageWipe.status=="inactive")'
    run("missing branch declines", runtime(module, branch=False), decline)
    run("archived 1.1.0 declines", runtime(module, branch=False, build="1.1.0.403908"), decline)
    rt = runtime(module)
    rt.execute("saved_track,saved_elements=fixture(7,false)")
    db.load_at(rt, module, "=" + str(WIPE))
    run("in-place module reload preserves live state and works", rt,
        'assert(IsValid(saved_elements[4])); saved_elements[4]:Demolish(false); '
        'assert(not IsValid(saved_elements[4]) and IsValid(saved_elements[3])); check_arrays()')
    needle = 'return type(C) == "table" and type(C.MigrateStep) == "function"'
    assert module.count(needle) == 1
    mutant = module.replace(needle, "return true")
    run("scratch branch-guard reversal is detected", runtime(mutant, branch=False), decline, True)
    assert hashlib.sha256(WIPE.read_bytes()).hexdigest() == original_hash
    passed = sum(ok for _, ok in results)
    print("source unchanged sha256=" + original_hash)
    print(f"TOTAL {len(results)} = PASS {passed} + FAIL {len(results)-passed}")
    if passed != len(results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
