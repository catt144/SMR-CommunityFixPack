#!/usr/bin/env python3
"""F125/F52 composable migration controls on archived 1.1.1.405907 Lua.

The source roots below are explicit. Do not route this harness through
deskbench.TREES["1.1.0"]: that legacy name points at the live ModTools tree and
silently changed meaning when 1.1.1 landed.

WHAT IS SHIPPED AND LOADED VERBATIM (with luafn's delimiter and real line
offsets): Colonist:TryToEmigrateToDome, BookShuttleRide, StartShuttleLeg,
GetNextMigrationLeg, the local limits plus CanBoardTrainLeg/FailMigrationStep/
AbortMigration/MigrateStep span, IsInWalkingDistDome, ValidateBuilding,
GetAtmosphereBreathable, IsLRTransportAvailable, and the passage path builder.
The production Fix_VacuumWalks module is loaded whole. The regression leg loads
the pre-F125 module from git revision 16ff1aae, never a retyped imitation.

RETYPE/STUB BOUNDARY: engine exports (IsValid, IsSameMap, CurrentThread), the
route graph result, object construction, commands/building entry, reservations
and transport-task creation are controlled fixtures. The route graph is an
explicit input: BuildReachableGraph/GetNextLegToward return the queued leg.
Passage enumeration and both faulty threshold decisions remain shipped code.
Reservation/command stubs record order and arguments; they do not decide which
branch runs. This is desk evidence, not geometry, scheduler or in-play reach.
"""
import subprocess
from pathlib import Path

import deskbench as db
from luafn import find_bodies, read_lines


ARCHIVE_ROOT = Path(r"B:/Dev/SMR/SMR-Shared/SMR-SrcArchive")
SRC_110 = ARCHIVE_ROOT / "1.1.0.403908" / "Src"
SRC_111 = ARCHIVE_ROOT / "1.1.1.405907" / "Src"
MODULE_REL = "Code/Fix_VacuumWalks.lua"
MODULE_PATH = Path(db.REPO) / MODULE_REL
PRE_FIX_REV = "16ff1aae4c55a3c466496e49089824a6dafe7437"
KIT_WAVE2 = Path(db.TESTKIT) / "Code" / "20_Probes_Wave2.lua"


def body(src, rel, pattern):
    lines = read_lines(str(src / rel))
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (src, rel, pattern, hits)
    start, end = hits[0]
    return "\n".join(lines[start:end + 1]), start + 1


def span(src, rel, first_pattern, last_pattern):
    lines = read_lines(str(src / rel))
    first = find_bodies(lines, first_pattern)
    last = find_bodies(lines, last_pattern)
    assert len(first) == len(last) == 1, (rel, first, last)
    start, end = first[0][0], last[0][1]
    return "\n".join(lines[start:end + 1]), start + 1


def load_body(rt, rel, pattern):
    text, line = body(SRC_111, rel, pattern)
    db.load_at(rt, text, "=" + rel, line)


def module_source(prefixed=False):
    if not prefixed:
        return db.read(str(MODULE_PATH)), str(MODULE_PATH)
    out = subprocess.run(
        ["git", "show", "%s:%s" % (PRE_FIX_REV, MODULE_REL)],
        cwd=db.REPO, check=True, capture_output=True,
    ).stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    return out, "%s:%s" % (PRE_FIX_REV, MODULE_REL)


def vacuum_probe_block():
    lines = read_lines(str(KIT_WAVE2))
    starts = [i for i, line in enumerate(lines)
              if 'SMRTest.Register("VacuumWalks"' in line]
    assert len(starts) == 1, (KIT_WAVE2, starts)
    start = starts[0]
    ends = [i for i in range(start + 1, len(lines)) if lines[i] == "})"]
    assert ends, KIT_WAVE2
    return "\n".join(lines[start:ends[0] + 1]), start + 1


PRELUDE = db.ENGINE_SHIMS + r'''
Colonist = {}
Dome = {}
OnMsg = {}
MODULES = {}
guim = 1
SMRTest = {probes={}}
function SMRTest.Register(id, spec) SMRTest.probes[id] = spec end
function SMRTest.FixMissing(id)
  local f = SMRFixPack and SMRFixPack.fixes[id]
  if not f or f.status ~= "active" then return "FAIL", "fix is not active" end
end
function SMRTest.WithGlobals(vars, fn)
  local old = {}
  for k, v in pairs(vars) do old[k] = rawget(_G, k); _G[k] = v end
  local result = table.pack(pcall(fn))
  for k in pairs(vars) do _G[k] = old[k] end
  if not result[1] then error(result[2]) end
  return table.unpack(result, 2, result.n)
end
SMRFixPack = {fixes={}}
function SMRFixPack.Register(id, spec)
  MODULES[id] = spec
  SMRFixPack.fixes[id] = {status="pending"}
end
function SMRFixPack.SetGlobal(name, value, reason)
  if FAIL_SETGLOBAL then return reason end
  _G[name] = value
  if rawget(_G, name) ~= value then return reason end
end
function SMRFixPack.Require(id, specs)
  for _, s in ipairs(specs) do
    local ok, name
    if s.test then
      ok = s.test() and true or false; name = "test"
    elseif s.probe then
      local ran, answer = pcall(s.probe)
      ok = ran and answer == true; name = "probe"
    elseif s.global then
      local v = rawget(_G, s.global)
      ok = s.kind == "any" and v ~= nil or type(v) == (s.kind or "function")
      name = s.global
    elseif s.class then
      local c = rawget(_G, s.class)
      ok = type(c) == "table" and (not s.method or type(c[s.method]) == "function")
      name = s.class
    elseif s.path then
      local v = _G
      for _, part in ipairs(s.path) do v = type(v) == "table" and v[part] or nil end
      ok = s.kind == "any" and v ~= nil or type(v) == (s.kind or "function")
      name = table.concat(s.path, ".")
    end
    if not ok then return s.reason or ((name or "requirement") .. " declined") end
  end
end

const = {
  Colonist = {ColonistMaxDomeWalkDist=400, ColonistMinDistToIgnorePassage=1000},
  ColonistMaxPassagePassthroughDomes=1,
}
g_Consts = {ColonistMaxDomeWalkDist=400, ColonistMinDistToIgnorePassage=1000}
THREAD = {}
function CurrentThread() return THREAD end
MainMap = {City=false}
BreathableAtmosphere = false
function IsValid(o) return type(o) == "table" and not o.invalid end
function IsSameMap(a, b) return a.map ~= nil and a.map == b.map end
function ResolveMap(o) return type(o) == "table" and o.map or nil end
function GetOpenAirBuildings() return false end
function CheckWalkableDistance(_, a, b)
  local row = g_DomeToDomeDist[a]
  local d = row and row[b]
  return d and d[1] or false, d and d[2] or -1
end
function HasShuttleLandingSlots(o) return type(o) == "table" and o.landing end
function IsTransportAvailableBetween(a, b) return a ~= nil and b ~= nil end
function CreateColonistTransportTask(unit, src, dest)
  unit.transport_task = {src_dome=src, dest_dome=dest, shuttle=false}
  return unit.transport_task
end
function FindNearestObject() return nil end
function IsCloser2D() return false end
function CanTrainTravelBetween() return true end
function Sleep() EVENTS[#EVENTS+1] = "sleep" end

EVENTS = {}
CURRENT_LEGS = {}
g_DomeToDomeDist = {}
function BuildReachableGraph() return {} end
function GetNextLegToward() return table.remove(CURRENT_LEGS, 1) end
function IsUnitInDome(unit) return unit.current_dome end

function Colonist:CanWork() return self.can_work and true or false end
function Colonist:GetMap() return self.map end
function Colonist:GetNavigationPos() return self.current_dome end
function Colonist:ClearTransportRequest()
  EVENTS[#EVENTS+1] = "clear"
  self.transport_task = false
end
function Colonist:DiscardTransportTicket() EVENTS[#EVENTS+1] = "ticket" end
function Colonist:CancelResidenceReservation() EVENTS[#EVENTS+1] = "cancel_residence" end
function Colonist:CancelWorkReservation() EVENTS[#EVENTS+1] = "cancel_work" end
function Colonist:SetCommand(cmd, dest, path)
  EVENTS[#EVENTS+1] = "command:" .. tostring(cmd)
  self.command, self.command_dest, self.command_path = cmd, dest, path
  return cmd
end
function Colonist:StartTransport(reason, dest, param, src, dst)
  EVENTS[#EVENTS+1] = "train:" .. tostring(reason)
  self.started_transport = {reason, dest, param, src, dst}
  return reason
end
function Colonist:EnterBuilding(bld)
  EVENTS[#EVENTS+1] = "enter:" .. tostring(bld.name)
  self.current_dome = bld
  return true
end
function Colonist:UseElevator(elevator)
  self.map_slot = elevator.other and elevator.other.map_slot
end
function Colonist:GetMapSlot() return self.map_slot end

function Dome:ReserveResidence(unit)
  EVENTS[#EVENTS+1] = "reserve_residence"
  unit.reserved_residence = self
end
function Dome:ReserveWorkplace(unit)
  EVENTS[#EVENTS+1] = "reserve_work"
  unit.reserved_workplace = self
end

function new_dome(name, landing)
  local d = setmetatable({name=name, map=MainMap, landing=landing ~= false,
    city=MainMap.City, connected_domes={}, dome_network={}}, {__index=Dome})
  return d
end
function new_colonist(dome)
  local c = setmetatable({map=MainMap, city=MainMap.City, current_dome=dome,
    command="MigrateStep", command_thread=THREAD, traits={}, status_effects={},
    stat_health=100}, {__index=Colonist})
  return c
end
function set_dist(a, b, dist)
  g_DomeToDomeDist[a] = g_DomeToDomeDist[a] or {}
  g_DomeToDomeDist[b] = g_DomeToDomeDist[b] or {}
  g_DomeToDomeDist[a][b] = {true, dist}
  g_DomeToDomeDist[b][a] = {true, dist}
end
function connect_path(nodes)
  for _, a in ipairs(nodes) do
    a.connected_domes = {a}
    a.dome_network = {}
    for _, b in ipairs(nodes) do a.dome_network[b] = true end
  end
  for i = 1, #nodes - 1 do
    local a, b = nodes[i], nodes[i+1]
    a.connected_domes[#a.connected_domes+1] = b
    a.connected_domes[b] = true
    b.connected_domes[#b.connected_domes+1] = a
    b.connected_domes[a] = true
  end
end
function reset_world()
  EVENTS = {}; CURRENT_LEGS = {}; g_DomeToDomeDist = {}
  BreathableAtmosphere = false
  MainMap.City = {labels={ShuttleHub={}}}
end
'''


def runtime(pre_fix=False, setglobal_fail=False):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)

    # Real current-build functions. The two spans retain their file-local helpers.
    for rel, pat in [
        ("Lua/Terraforming.lua", r"^function GetAtmosphereBreathable\("),
        ("Lua/Buildings/ShuttleHub.lua", r"^function IsLRTransportAvailable\("),
        ("Lua/Buildings/Dome.lua", r"^function IsInWalkingDistDome\("),
        ("Lua/Buildings/Workplace.lua", r"^function ValidateBuilding\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:TryToEmigrateToDome\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:BookShuttleRide\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:StartShuttleLeg\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:GetNextMigrationLeg\("),
    ]:
        load_body(rt, rel, pat)

    text, line = span(SRC_111, "Lua/Passage.lua",
                      r"^function AreDomesConnectedWithPassage\(",
                      r"^function GetDomesPassagePath\(")
    db.load_at(rt, text, "=Lua/Passage.lua", line)
    text, line = span(SRC_111, "Lua/Units/Colonist.lua",
                      r"^local max_migration_legs_per_step = ",
                      r"^function Colonist:MigrateStep\(")
    db.load_at(rt, text, "=Lua/Units/Colonist.lua", line)

    source, chunk = module_source(prefixed=pre_fix)
    db.load_at(rt, source, "=" + chunk)
    rt.execute("ORIGINAL_TRY=Colonist.TryToEmigrateToDome; ORIGINAL_WALK=IsInWalkingDistDome")
    if setglobal_fail:
        rt.execute("FAIL_SETGLOBAL=true")
    err = rt.eval('MODULES["VacuumWalks"].apply()')
    if setglobal_fail:
        rt.globals().APPLY_ERROR = err
        return rt
    if err is not None:
        raise AssertionError("module declined: %s" % err)
    rt.execute('SMRFixPack.fixes["VacuumWalks"].status="active"')
    return rt


def event_string(rt):
    return rt.eval('table.concat(EVENTS, ",")')


def main():
    for src in (SRC_110, SRC_111):
        if not src.is_dir():
            raise SystemExit("missing pinned archive: %s" % src)

    bench = db.Bench("F125/F52: native 1.1.1 migration with composable vacuum inputs")

    # Falsifier: the exact pre-fix module loses the 1.1.1 task state and never
    # reaches the intermediate threshold.
    old = runtime(pre_fix=True)
    old.execute(r'''
      reset_world(); a=new_dome("A"); d=new_dome("D")
      u=new_colonist(a); u.command="Transport"; u.emigration_dome=a
      u.transport_task={shuttle=false,dest_dome=d,migration_dest=a}
      Colonist.TryToEmigrateToDome(u,a,d,"shuttle",300)
      OLD_MIGRATION_DEST = u.transport_task.migration_dest
      reset_world(); a=new_dome("A"); p=new_dome("P"); b=new_dome("B")
      connect_path({a,p,b}); set_dist(a,b,300)
      u=new_colonist(a); u.emigration_dome=b
      CURRENT_LEGS={{kind="walk",final=false,dome=b}}
      Colonist.MigrateStep(u,b)
      OLD_INTERMEDIATE_EVENTS=table.concat(EVENTS,",")
    ''')
    bench.check("pre-fix control loses migration_dest retarget",
                old.eval("OLD_MIGRATION_DEST ~= false"))
    bench.check("pre-fix control skips the intermediate passage",
                old.eval("not OLD_INTERMEDIATE_EVENTS:find('enter:P',1,true)"))

    failed = runtime(setglobal_fail=True)
    failed.execute(r'''
      reset_world(); a=new_dome("A"); b=new_dome("B"); set_dist(a,b,300)
      local _, d=IsInWalkingDistDome(b,a,MainMap.City); FAILED_DIST=d
    ''')
    bench.check("SetGlobal failure returns inactive reason",
                failed.eval("type(APPLY_ERROR) == 'string'"))
    bench.check("SetGlobal failure leaves both shipped targets untouched",
                failed.eval("Colonist.TryToEmigrateToDome == ORIGINAL_TRY and IsInWalkingDistDome == ORIGINAL_WALK and FAILED_DIST == 300"))

    rt = runtime()

    # Direct final leg, reservations and the intended no-passage fallback.
    rt.execute(r'''
      reset_world(); a=new_dome("A"); p=new_dome("P"); b=new_dome("B")
      connect_path({a,p,b}); set_dist(a,b,300)
      u=new_colonist(a); u.command="Idle"; u.can_work=true
      DIRECT_RETURN=Colonist.TryToEmigrateToDome(u,a,b,"walk",300)
      DIRECT_PATH=u.command_path; DIRECT_EVENTS=table.concat(EVENTS,",")

      reset_world(); a2=new_dome("A2"); b2=new_dome("B2"); set_dist(a2,b2,300)
      u2=new_colonist(a2); u2.command="Idle"
      Colonist.TryToEmigrateToDome(u2,a2,b2,"walk",300)
      FALLBACK_CMD=u2.command; FALLBACK_PATH=u2.command_path

      reset_world(); BreathableAtmosphere=true
      a3=new_dome("A3"); p3=new_dome("P3"); b3=new_dome("B3")
      connect_path({a3,p3,b3}); set_dist(a3,b3,300)
      u3=new_colonist(a3); u3.command="Idle"
      Colonist.TryToEmigrateToDome(u3,a3,b3,"walk",300)
      BREATHABLE_PATH=u3.command_path
    ''')
    bench.check("direct vacuum final leg receives the real passage path",
                rt.eval("DIRECT_PATH and #DIRECT_PATH == 3 and DIRECT_PATH[2].name == 'P'"))
    bench.check("direct leg preserves clear/ticket/residence/work/command order",
                rt.eval("DIRECT_EVENTS == 'clear,ticket,reserve_residence,reserve_work,command:TransportByFoot'"),
                rt.eval("DIRECT_EVENTS"))
    bench.check("repaired direct branch preserves shipped nil return",
                rt.eval("DIRECT_RETURN == nil"))
    bench.check("no-passage vacuum fallback remains TransportByFoot with nil path",
                rt.eval("FALLBACK_CMD == 'TransportByFoot' and FALLBACK_PATH == nil"))
    bench.check("breathable short walk remains outside with nil path",
                rt.eval("BREATHABLE_PATH == nil"))

    # The long-detour path stays in the native 1.1.1 BookShuttleRide block.
    rt.execute(r'''
      reset_world(); hub={shuttle_infos={1},working=true,transport_mode="all"}
      MainMap.City.labels.ShuttleHub={hub}
      a=new_dome("A"); p1=new_dome("P1"); p2=new_dome("P2"); b=new_dome("B")
      connect_path({a,p1,p2,b}); set_dist(a,b,300)
      u=new_colonist(a); u.command="Idle"
      Colonist.TryToEmigrateToDome(u,a,b,"walk",300)
      LONG_TASK=u.transport_task; LONG_COMMAND=u.command
    ''')
    bench.check("long passage detour keeps native shuttle booking and state",
                rt.eval("LONG_TASK and LONG_TASK.dest_dome.name == 'B' and LONG_TASK.state == 'almost_ready_for_pickup' and LONG_COMMAND == 'Idle'"))

    # Runtime constants are volatile. If their order no longer leaves a safe
    # +1 lookup-only value, the wrapper must hand the call through unchanged.
    rt.execute(r'''
      reset_world(); a=new_dome("A"); p=new_dome("P"); b=new_dome("B")
      connect_path({a,p,b}); set_dist(a,b,300); u=new_colonist(a); u.command="Idle"
      g_Consts.ColonistMaxDomeWalkDist=400; g_Consts.ColonistMinDistToIgnorePassage=400
      Colonist.TryToEmigrateToDome(u,a,b,"walk",300); EQUAL_PATH=u.command_path
      g_Consts.ColonistMinDistToIgnorePassage=401; u.command_path=nil; u.command="Idle"
      Colonist.TryToEmigrateToDome(u,a,b,"walk",300); CROSS_PATH=u.command_path
      g_Consts.ColonistMaxDomeWalkDist=400; g_Consts.ColonistMinDistToIgnorePassage=1000
    ''')
    bench.check("equal runtime thresholds decline to native input unchanged",
                rt.eval("EQUAL_PATH == nil"))
    bench.check("+1 crossing the runtime passage threshold also declines",
                rt.eval("CROSS_PATH == nil"))

    # The 1.1.1 task-retarget machine remains installed, unlike the pre-fix copy.
    rt.execute(r'''
      reset_world(); a=new_dome("A"); d=new_dome("D")
      u=new_colonist(a); u.command="Transport"; u.emigration_dome=a
      u.transport_task={shuttle=false,dest_dome=d,migration_dest=a}
      Colonist.TryToEmigrateToDome(u,a,d,"shuttle",300)
      RETARGET_TASK=u.transport_task; RETARGET_EMIGRATION=u.emigration_dome
    ''')
    bench.check("native task retarget clears migration_dest and follows journey",
                rt.eval("RETARGET_TASK.migration_dest == false and RETARGET_EMIGRATION.name == 'D'"))
    rt.execute(r'''
      reset_world(); a=new_dome("A"); d=new_dome("D"); other=new_dome("OTHER")
      u=new_colonist(a); u.command="Transport"; u.transport_task={shuttle=true,dest_dome=other,migration_dest=d}
      Colonist.TryToEmigrateToDome(u,a,d,"walk",300)
      ACTIVE_SHUTTLE=u.transport_task; ACTIVE_COMMAND=u.command
    ''')
    bench.check("active shuttle remains committed and is not retargeted",
                rt.eval("ACTIVE_SHUTTLE.shuttle and ACTIVE_SHUTTLE.dest_dome.name == 'OTHER' and ACTIVE_COMMAND == 'Transport'"))

    # Intermediate walk followed by a direct final walk in one native MigrateStep.
    rt.execute(r'''
      reset_world()
      a=new_dome("A"); ap=new_dome("AP"); mid=new_dome("MID")
      mb=new_dome("MB"); b=new_dome("B")
      connect_path({a,ap,mid}); set_dist(a,mid,300)
      -- Add the second network without destroying the first one's A->MID path.
      mb.connected_domes={mb,b}; mb.connected_domes[b]=true
      b.connected_domes={b,mb}; b.connected_domes[mb]=true
      mid.connected_domes[#mid.connected_domes+1]=mb
      mid.connected_domes[mb]=true
      mb.connected_domes[#mb.connected_domes+1]=mid
      mb.connected_domes[mid]=true
      for _,x in ipairs({mid,mb,b}) do for _,y in ipairs({mid,mb,b}) do x.dome_network[y]=true end end
      set_dist(mid,b,300)
      u=new_colonist(a); u.emigration_dome=b
      CURRENT_LEGS={{kind="walk",final=false,dome=mid},{kind="walk",final=true,dome=b}}
      Colonist.MigrateStep(u,b)
      MULTI_EVENTS=table.concat(EVENTS,","); MULTI_PATH=u.command_path
    ''')
    bench.check("intermediate vacuum leg traverses its passage before the community",
                rt.eval("MULTI_EVENTS:find('enter:AP,enter:MID',1,true) ~= nil"),
                rt.eval("MULTI_EVENTS"))
    bench.check("multi-leg continuation reaches native direct final passage",
                rt.eval("MULTI_PATH and MULTI_PATH[1].name == 'MID' and MULTI_PATH[#MULTI_PATH].name == 'B'"))

    # Breathable and no-passage intermediate controls.
    rt.execute(r'''
      reset_world(); BreathableAtmosphere=true
      a=new_dome("A"); p=new_dome("P"); mid=new_dome("MID"); b=new_dome("B")
      connect_path({a,p,mid}); set_dist(a,mid,300)
      u=new_colonist(a); u.emigration_dome=b
      CURRENT_LEGS={{kind="walk",final=false,dome=mid}}
      Colonist.MigrateStep(u,b); BREATHABLE_EVENTS=table.concat(EVENTS,",")

      reset_world(); a2=new_dome("A2"); mid2=new_dome("MID2"); b2=new_dome("B2")
      set_dist(a2,mid2,300); u2=new_colonist(a2); u2.emigration_dome=b2
      CURRENT_LEGS={{kind="walk",final=false,dome=mid2}}
      Colonist.MigrateStep(u2,b2); NO_PASS_EVENTS=table.concat(EVENTS,",")
    ''')
    bench.check("breathable intermediate control skips passage detour",
                rt.eval("not BREATHABLE_EVENTS:find('enter:P',1,true)"))
    bench.check("no-passage intermediate fallback still enters the next community",
                rt.eval("NO_PASS_EVENTS:find('enter:MID2',1,true) ~= nil"))

    # Shuttle/train continuation and cancellation remain native-owned.
    rt.execute(r'''
      reset_world(); a=new_dome("A"); landing=new_dome("LAND"); b=new_dome("B")
      u=new_colonist(a); u.emigration_dome=b
      CURRENT_LEGS={{kind="shuttle",landing=landing}}
      Colonist.MigrateStep(u,b); SHUTTLE_TASK=u.transport_task

      reset_world(); a2=new_dome("A2"); b2=new_dome("B2")
      s1={CanWork=function() return true end}; s2={CanWork=function() return true end}
      u2=new_colonist(a2); u2.emigration_dome=b2
      CURRENT_LEGS={{kind="train",src_station=s1,dst_station=s2}}
      Colonist.MigrateStep(u2,b2); TRAIN_CALL=u2.started_transport

      reset_world(); u3=new_colonist(false); u3.emigration_dome={invalid=true}
      u3.transport_task={migration_dest=true}; u3.reserved_residence=true; u3.reserved_workplace=true
      Colonist.MigrateStep(u3,u3.emigration_dome)
      CANCEL_EVENTS=table.concat(EVENTS,","); CANCEL_TASK=u3.transport_task
    ''')
    bench.check("intermediate shuttle keeps migration_dest for continuation",
                rt.eval("SHUTTLE_TASK and SHUTTLE_TASK.migration_dest and SHUTTLE_TASK.migration_dest.name == 'B'"))
    bench.check("train leg keeps native MigrateStep ticket continuation",
                rt.eval("TRAIN_CALL and TRAIN_CALL[1] == 'MigrateStep' and TRAIN_CALL[2].name == 'B2'"))
    bench.check("cancellation clears journey state and reservations",
                rt.eval("CANCEL_TASK.migration_dest == false and CANCEL_EVENTS:find('cancel_residence',1,true) and CANCEL_EVENTS:find('cancel_work',1,true)"))

    # Marker falsifiers: wrong next call and command cancellation consume it.
    rt.execute(r'''
      reset_world(); a=new_dome("A"); mid=new_dome("MID"); other=new_dome("OTHER")
      set_dist(a,mid,300); set_dist(a,other,300)
      u=new_colonist(a); CURRENT_LEGS={{kind="walk",final=false,dome=mid}}
      local leg=Colonist.GetNextMigrationLeg(u,mid)
      local _, wrong=IsInWalkingDistDome(other,a,u.city)
      local _, after=IsInWalkingDistDome(mid,a,u.city)
      LEAK_WRONG=wrong; LEAK_AFTER=after

      CURRENT_LEGS={{kind="walk",final=false,dome=mid}}
      leg=Colonist.GetNextMigrationLeg(u,mid); u.command="Idle"
      local _, cancelled=IsInWalkingDistDome(mid,a,u.city)
      LEAK_CANCELLED=cancelled
    ''')
    bench.check("unexpected next distance call consumes marker without changing either result",
                rt.eval("LEAK_WRONG == 300 and LEAK_AFTER == 300"))
    bench.check("command cancellation makes an armed marker inert",
                rt.eval("LEAK_CANCELLED == 300"))

    rt.execute(r'''
      local m2={City=MainMap.City}; local x={map=MainMap}; local y={map=m2}
      RETURN_COUNT=select("#", IsInWalkingDistDome(x,y,MainMap.City))
      RETURN_VALUE=IsInWalkingDistDome(x,y,MainMap.City)
    ''')
    bench.check("global wrapper preserves the native one-value different-map return",
                rt.eval("RETURN_COUNT == 1 and RETURN_VALUE == false"))

    probe, line = vacuum_probe_block()
    db.load_at(rt, "local FixMissing, WithGlobals = SMRTest.FixMissing, SMRTest.WithGlobals\n" + probe,
               "=" + str(KIT_WAVE2), line - 1)
    rt.execute(r'''
      const.ColonistMaxPassagePassthroughDomes=5
      local result=table.pack(pcall(SMRTest.probes.VacuumWalks.run))
      KIT_OK=result[1]; KIT_STATUS=result[2]; KIT_DETAIL=result[3]
    ''')
    bench.check("actual TestKit VacuumWalks behavior probe passes",
                rt.eval("KIT_OK and KIT_STATUS == 'PASS'"),
                rt.eval("tostring(KIT_STATUS) .. ': ' .. tostring(KIT_DETAIL)"))

    return bench.finish()


if __name__ == "__main__":
    raise SystemExit(main())
