#!/usr/bin/env python3
"""C115: archived Transport, task cleanup and dome position check on a desk fixture.

Predictions before run: the repaired obsolete own-home task cleans without a
pickup walk; remote, committed and multi-leg tasks enter native Transport; with
the module absent the obsolete task walks to its old pickup. Shipped Lua bodies
decide delegation and cleanup. The dome geometry and movement are fixture inputs,
so this cannot prove a real save's anchor or trajectory.
"""
from pathlib import Path
import os

import deskbench as db


BUILD = "1.1.1.405907"
db.TREES[BUILD] = os.path.join(
    os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
    BUILD, "Src")
MODULE = Path(db.REPO) / "Code/Fix_ObsoleteHomeRescue.lua"

PRELUDE = r'''
Colonist = {}
ColonistTransportTask = {source_dome=false, migration_dest=false,
  shuttle=false, departure_rocket=false}
working_anims = {"idle"}
const = {ColonistMaxWaitShuttlePickupTimeMs=1000}
function IsKindOf(obj, kind) return obj and obj.kind == kind end
function IsValid(obj) return obj and obj.valid ~= false end
function IsValidPos(obj) return obj and obj.pos_valid ~= false end
function GetObjectHexGrid(obj) return "grid" end
function GetTopmostParent(obj) return obj end
function GetDomeAtPoint(grid, obj) assert(grid == "grid"); return obj.pos_dome end
function IsObjInDome(obj) error("holder lookup must not decide the bypass") end
function IsLRTransportAvailable(city) return true end
function IsInWalkingDist(unit, dome) return true end
function GameTime() return 0 end
function DoneObject(obj) obj.done=true end
function Wakeup(thread) end
function Colonist:IsTransported() return false end
function Colonist:IsWaitingTransport() return false end
function Colonist:GetMap() return self.map end
function Colonist:ExitHolder() self.exits=self.exits+1; return true end
function Colonist:Goto(pos)
  self.walks=self.walks+1
  if self.cancel_on_walk then self.transport_task:Cleanup() end
  return true
end
function Colonist:CancelResidenceReservation() end
function Colonist:CancelWorkReservation() end
function Colonist:PushDestructor(fn) self.destructor=fn end
function Colonist:PopAndCallDestructor()
  local fn=self.destructor; self.destructor=nil; if fn then fn(self) end
end
function Colonist:PlayState(anim) error("wait loop unexpectedly entered") end
function SMRFixPack_Register(id, def) local reason=def.apply(); assert(not reason, tostring(reason)) end
SMRFixPack = {Register=SMRFixPack_Register}
function SMRFixPack.Require(id, specs)
  for _,spec in ipairs(specs) do
    if spec.class and spec.method then
      if type(_G[spec.class][spec.method]) ~= "function" then return spec.class.."."..spec.method end
    elseif spec.global and type(_G[spec.global]) ~= "function" then return spec.global
    elseif spec.test and not spec.test() then return spec.reason end
  end
end
function make_case(kind)
  local home={kind="Community"}
  local manager={removed=0}
  function manager:RemoveColonistTransportRequest(task) self.removed=self.removed+1 end
  local c=setmetatable({kind="Colonist",dome=home,pos_dome=home,
    transport_task=false,holder=false,city={},pfclass=0,walks=0,exits=0,
    map={GetPassablePointNearby=function(_,pos,pfclass) return pos end}}, {__index=Colonist})
  local task=setmetatable({colonist=c,dest_dome=home,source_dome=false,
    migration_dest=false,departure_rocket=false,shuttle=false,state="new",
    source_landing_site={"old pickup",false},lr_manager=manager},
    {__index=ColonistTransportTask})
  c.transport_task=task
  if kind == "remote" then c.pos_dome=false end
  if kind == "committed" then task.shuttle={} end
  if kind == "multi_leg" then task.migration_dest={} end
  if kind == "relocation" then task.dest_dome={kind="Community"} end
  if kind == "expedition" then task.departure_rocket={} end
  if kind == "holder" then c.holder={} end
  if kind == "bad_state" then task.state="transporting" end
  if kind == "cancellation" then c.pos_dome=false; c.cancel_on_walk=true end
  return c,task,manager,task.dest_dome
end
'''


def load_body(rt, rel, pattern):
    body, first, _ = db.body(rel, pattern, BUILD)
    db.load_at(rt, body, "=" + rel, first)


def run_case(kind, fixed, expected_walks):
    rt = db.lua_runtime()
    db.load_at(rt, PRELUDE, "=c115_fixture")
    load_body(rt, "Lua/Buildings/Dome.lua", r"^function IsUnitInDome\(")
    load_body(rt, "Lua/LRTransport.lua", r"^function ColonistTransportTask:Cleanup\(")
    load_body(rt, "Lua/Units/Colonist.lua", r"^function Colonist:WaitTransport\(")
    load_body(rt, "Lua/Units/Colonist.lua", r"^function Colonist:Transport\(")
    if fixed:
        db.load_at(rt, db.read(str(MODULE)), "=Code/Fix_ObsoleteHomeRescue.lua")
    c, task, manager, dest = rt.globals().make_case(kind)
    c.Transport(c, dest)
    assert c.walks == expected_walks, (kind, fixed, c.walks, expected_walks)
    assert c.exits == expected_walks, (kind, fixed, c.exits, expected_walks)
    assert manager.removed == 1 and task.done and c.transport_task is False, (
        kind, fixed, manager.removed, task.done, c.transport_task)
    print("PASS", kind, "fixed" if fixed else "module absent", "walks", c.walks)


def main():
    assert MODULE.is_file(), MODULE
    print("C115 predictions: obsolete=0 walks; native controls=1; absent=1")
    run_case("obsolete", True, 0)
    for kind in ("remote", "committed", "multi_leg", "relocation",
                 "expedition", "holder", "bad_state", "cancellation"):
        run_case(kind, True, 1)
    run_case("obsolete", False, 1)
    try:
        run_case("obsolete", False, 0)
    except AssertionError:
        print("PASS fixed demand fails with module absent")
    else:
        raise AssertionError("the fix-absent control did not falsify the fixed demand")


if __name__ == "__main__":
    main()
