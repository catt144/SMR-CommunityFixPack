#!/usr/bin/env python3
"""C120 deport-law rocket against archived 1.1.1.405907 Lua: the stall, K2 and E.

Run: python tools/desk_c120_deport_rocket.py

Shipped bodies are extracted from the archived 1.1.1.405907 tree, never retyped:
CmdLoad, the launch gate (IsCargoReady, GetLaunchIssue, AreEarthDepartColonistsReady,
GetPendingDepartureCount, WaitsForManualLaunch, WaitTakeOffHold), the draft
(GenerateDepartures, FindStopoverDomeForRocket, PurgeStopoverDepartures,
UpdateDepartureThread, StopDepartureThread, ReturnDehydratedColonists), and the
colonist side (LeavingMars, FindExit, CleanupLeavingColonist, GetDehydratedData,
CanChangeCommand, IsTransported, ClearTransportRequest). Code/Fix_DeportRocketLaunch.lua
is loaded whole.

Modelled, not shipped (named so a reader can judge each):
  * a game-time scheduler (coroutines ordered by wake time, then creation) and a
    CommandObject model: SetCommand runs the old command's pending destructors in
    the new thread before the new command, and marks thread_running_destructors
    while it does (CommandObject.lua:346-386 is C-backed thread plumbing).
  * Colonist:SetCommand is CommandObject.SetCommand. GenerateDepartures calls it
    only for walk/train reach; fixture walkers are in walking distance, where the
    shipped override reduces to CommandObject.SetCommand (ColonistTransport.lua:406-420).
    Trains are not modelled.
  * one shuttle serving stopover tasks FIFO: commit (task.shuttle set) -> fly 15000
    -> "transporting" -> ride 45000 -> drop-off Idle in the stopover dome.
  * GotoBuildingSpot sleeps 15000 and reaches the pad only from the pad dome.
  * SetDome(false) records the call and clears residence/workplace, as the shipped
    body does through SetWorkplace/SetResidence (Colonist.lua:432-433); DoneObject
    records whether it ran on the colonist's own command thread and removes it from
    UIColony.labels.Colonist. Neither is the shipped body.
  * cargo is "loading" with the auto-depart window open until CARGO_READY_AT, then
    "ready" with it closed; fuel, maintenance and dust are clear.
  * 00_Core.lua's veto gate (index_key, read_flag, WhenActive) is extracted from
    Code/00_Core.lua, not stubbed; Register is stubbed to mark the fix active.
Nothing here ran in a game. A PASS shows the module discriminates on the shipped
bodies in this fixture; it does not show that a colony produces the fixture.
"""
import os
import pathlib
import subprocess
import sys

import deskbench as db
from luafn import read_lines, find_bodies

ARCH = pathlib.Path(os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
                    "1.1.1.405907", "Src")
MODULE = pathlib.Path(db.REPO, "Code", "Fix_DeportRocketLaunch.lua")

UR = "Lua/UniversalRocket.lua"
COL = "Lua/Units/Colonist.lua"
BODIES = [
    (UR, r"^function UniversalRocketBase:CmdLoad\("),
    (UR, r"^function UniversalRocketBase:GetPendingDepartureCount\("),
    (UR, r"^function UniversalRocketBase:AreEarthDepartColonistsReady\("),
    (UR, r"^function UniversalRocketBase:IsCargoReady\("),
    (UR, r"^function UniversalRocketBase:CargoSleep\("),
    (UR, r"^const\.RocketTakeOffHoldTime\s*="),
    (UR, r"^function UniversalRocketBase:WaitTakeOffHold\("),
    (UR, r"^function UniversalRocketBase:GetLaunchIssue\("),
    (UR, r"^function UniversalRocketBase:GetDepartureLocType\("),
    (UR, r"^function UniversalRocketBase:GetArrivalLocType\("),
    (UR, r"^function UniversalRocketBase:IsRocketLanded\("),
    (UR, r"^function UniversalRocketBase:IsSpecialAutomode\("),
    (UR, r"^function UniversalRocketBase:WaitsForManualLaunch\("),
    (UR, r"^function UniversalRocketBase:IsColonistValidForDeparture\("),
    (UR, r"^function UniversalRocketBase:UpdateDepartureThread\("),
    (UR, r"^function UniversalRocketBase:StopDepartureThread\("),
    (UR, r"^function UniversalRocketBase:ReturnDehydratedColonists\("),
    (UR, r"^function UniversalRocketBase:ClearDepartures\("),
    (UR, r"^function UniversalRocketBase:IsBoardingAllowed\("),
    (COL, r"^function Colonist:FindExit\("),
    (COL, r"^function Colonist:GetDehydratedData\("),
    (COL, r"^function CleanupLeavingColonist\("),
    (COL, r"^function Colonist:LeavingMars\("),
    (COL, r"^function Colonist:CanChangeCommand\("),
    (COL, r"^function Colonist:IsTransported\("),
    (COL, r"^function Colonist:ClearTransportRequest\("),
]
# a file-local helper and the two methods after it, loaded as one span
SPAN = (UR, [r"^local function FindStopoverDomeForRocket\(",
             r"^function UniversalRocketBase:PurgeStopoverDepartures\("])

H = 30000

FIXTURE = r'''
-- engine: time, threads, commands --------------------------------------------
NOW, THREADS, SEQ, CURRENT = 0, {}, 0, nil
function GameTime() return NOW end
function CurrentThread() return CURRENT end
function CreateGameTimeThread(fn, ...)
  local args = table.pack(...)
  SEQ = SEQ + 1
  local t = {alive=true, wake=NOW, seq=SEQ}
  t.co = coroutine.create(function() return fn(table.unpack(args, 1, args.n)) end)
  THREADS[#THREADS+1] = t
  return t
end
function Sleep(ms) coroutine.yield(ms or 0) end
function IsValidThread(t) return type(t) == "table" and t.alive == true end
function DeleteThread(t) if type(t) == "table" then t.alive = false end end
function run_until(limit)
  while true do
    local best
    for _, t in ipairs(THREADS) do
      if t.alive and (not best or t.wake < best.wake or (t.wake == best.wake and t.seq < best.seq)) then best = t end
    end
    if not best or best.wake > limit then NOW = limit return end
    NOW = best.wake
    CURRENT = best
    local ok, ms = coroutine.resume(best.co)
    CURRENT = nil
    if not ok then error(ms) end
    if coroutine.status(best.co) == "dead" then best.alive = false
    else best.wake = NOW + (ms or 0); SEQ = SEQ + 1; best.seq = SEQ end
  end
end

CommandObject = {}
function CommandObject.SetCommand(self, command, ...)
  local args = table.pack(...)
  self.command = command or nil
  local old = self.command_thread
  local dtors = self.dtors or {}
  self.dtors = {}
  local t
  t = CreateGameTimeThread(function()
    if #dtors > 0 then
      self.thread_running_destructors = t
      for i = #dtors, 1, -1 do dtors[i](self) end
      self.thread_running_destructors = false
    end
    if not command then return end
    self[command](self, table.unpack(args, 1, args.n))
    if self.command_thread == t and self.valid then
      self.command = "Idle"
      self:Idle()
    end
  end)
  self.command_thread = t
  if old then DeleteThread(old) end
  return true
end
local function push(self, f) self.dtors = self.dtors or {}; self.dtors[#self.dtors+1] = f end
local function pop(self) local d = self.dtors; local f = d[#d]; d[#d] = nil; return f end

-- engine tolerances and globals the bodies read --------------------------------
function table.find(t, a, b)
  if type(t) ~= "table" then return end
  for i, v in ipairs(t) do
    if b == nil then if v == a then return i end
    elseif type(v) == "table" and v[a] == b then return i end
  end
end
function table.icount(t, f) local n = 0 for i, v in ipairs(t) do if f(i, v) then n = n + 1 end end return n end
insert, remove_entry, find = table.insert, table.remove_entry, table.find
function IsValid(o) return type(o) == "table" and o.valid == true end
function IsKindOf() return false end
function IsSameMap(a, b) return (a.slot or 1) == (b.slot or 1) end
function ValidateBuilding(b) return IsValid(b) and b or nil end
function HasDustStorm() return false end
function IsValidPos() return true end
function Msg() end
function RebuildInfopanel() end
function RemoveObjectFromNotification() end
function CallFlightPolicyFunc() end
SELREMOVED = 0
function SelectionRemove(o) if SelectedObj == o then SelectedObj = nil; SELREMOVED = SELREMOVED + 1 end end
const = {HourDuration=30000, DayDuration=720000, MinuteDuration=500, ColonistTransportTaskExpirationTime=720000}
g_Consts = {SupplyMissionsEnabled=1}
g_RocketTypes = {Player="Player", TradePad="TradePad", Rival="Rival", Trade="Trade", Expedition="Expedition"}
ActiveLaws = {Policy_Seniors_Banish=true}
MAP = {GetPassablePointNearby=function() return {SetInvalidZ=function(p) return p end} end}

-- rocket class ---------------------------------------------------------------
UniversalRocketBase = {departure_tick=1000*30, departure_stopover_deadline=720000}
local R = UniversalRocketBase
R.PushDestructor, R.PopDestructor = push, function(s) pop(s) end
function R:PopAndCallDestructor() pop(self)(self) end
function R:CreateGameTimeThread(fn, ...) return CreateGameTimeThread(fn, ...) end
function R:SetCommand(...) return CommandObject.SetCommand(self, ...) end
function R:GetMapSlot() return 1 end
R.waypoint_chains = {rocket_entrance={{}}}
function R:LeadIn() end
function R:GetMap() return MAP end
function R:IsValidPos() return true end
function R:GetPos() return {SetInvalidZ=function(p) return p end} end
function R:IsAutoModeEnabled() return self.auto_mode_on end
function R:IsPlayerControlled() return true end
function R:HasEnoughFuelToLaunch() return true end
function R:MaintenanceDone() return true end
CARGO_READY_AT = 61000
function R:CheckAutoDepart() return GameTime() < CARGO_READY_AT end
function R:GetCargoResourcesStatus() return GameTime() < CARGO_READY_AT and "loading" or "ready" end
for _, n in ipairs{"UpdatePinVisibility","OpenDoor","ForceUnloadRemainingCargo","CreateAutoCargoRequest",
    "SetCargoRequest","SeedDefaultExportResources","UpdateEarthExportRequests","LoadNonResourceCargo",
    "UpdateReadyNoDestinationNotification"} do R[n] = function() end end
LAUNCHED, AT_LAUNCH = nil, nil
function R:CmdTakeOff()
  self:StopDepartureThread()
  LAUNCHED = GameTime()
  AT_LAUNCH = {departures={}, rides={}}
  for _, c in ipairs(self.departures) do AT_LAUNCH.departures[#AT_LAUNCH.departures+1] = c end
  for _, task in ipairs(TASKS) do
    if task.shuttle and task.state ~= "done" then AT_LAUNCH.rides[#AT_LAUNCH.rides+1] = task end
  end
  while true do Sleep(1e9) end
end
function R:CmdWaitOrder() while true do Sleep(1e9) end end
function R:Idle() while true do Sleep(1e9) end end

-- colonist class ---------------------------------------------------------------
Colonist = {pfclass=0}
local C = Colonist
C.PushDestructor, C.PopDestructor = push, function(s) pop(s) end
function C:PopAndCallDestructor() pop(self)(self) end
function C:SetCommand(...) return CommandObject.SetCommand(self, ...) end
function C:GetMapSlot() return self.slot or 1 end
function C:GetMap() return MAP end
function C:GetPos() return {} end
function C:SetPos() end
function C:GetParent() return self.parent end
function C:IsTouristReadyToGoHome() return false end
function C:ClearDetrimentalStatusEffects() end
function C:DiscardTransportTicket() self.transport_ticket = false end
function C:CancelResidenceReservation() end
function C:CancelWorkReservation() end
function C:SetOutside() end
function C:UpdateOutside() end
ORDER, SETDOME_FALSE, GOTO, DONE, RESPAWNS = {}, {}, {}, {}, 0
function C:SetDome(d)
  if not d and self.dome then
    SETDOME_FALSE[self.name] = true
    ORDER[#ORDER+1] = self.name .. ":setdome"
    self.residence, self.workplace = false, false
  end
  self.dome = d or false
end
function C:GotoBuildingSpot()
  GOTO[self.name] = (GOTO[self.name] or 0) + 1
  Sleep(15000)
  return self.dome_before_leaving == PAD_DOME
end
function C:Idle() while true do Sleep(1e9) end end
function C:Abandoned() while true do Sleep(1e9) end end
function C:RideShuttle() while true do Sleep(1e9) end end
function C:Work()
  self:PushDestructor(function(self)
    ORDER[#ORDER+1] = self.name .. ":exit-start"
    Sleep(5000)
    ORDER[#ORDER+1] = self.name .. ":exit-done"
  end)
  while true do Sleep(1e9) end
end
function C.new(cls, data, map)
  RESPAWNS = RESPAWNS + 1
  local o = setmetatable({name="respawn"..RESPAWNS, valid=true, traits=data.traits or {}}, {__index=Colonist})
  return o
end
function DoneObject(o)
  DONE[o.name] = {own = CURRENT ~= nil and CURRENT == o.command_thread, at = NOW}
  o.valid = false
  remove_entry(UIColony.labels.Colonist, o)
  if CURRENT ~= o.command_thread then CommandObject.SetCommand(o, false) end
end

-- domes, draft helpers, shuttle -------------------------------------------------
PAD_DOME = {name="pad", valid=true, mode="walk", slot=1}
FAR_DOME = {name="far", valid=true, slot=1}
OTHER_DOME = {name="other", valid=true, slot=2}
for _, d in ipairs{PAD_DOME, FAR_DOME, OTHER_DOME} do
  d.CanVisit = function() return true end
  d.CanAcceptNewColonists = function() return true end
  d.HasFreeLivingSpaceFor = function() return true end
  d.ReserveResidence = function() end
end
CITY = {labels={Dome={PAD_DOME, FAR_DOME, OTHER_DOME}}}
UIColony = {labels={Colonist={}}}
function FindTransportationModeToCommunity(rocket, target)
  if target.CanVisit then return target.mode end   -- a dome
  if target.dome == PAD_DOME then return "walk" end
end
function IsUnitInDome(c) return c.dome end
function IsTransportAvailableBetween(a, b) return (a.slot or 1) == (b.slot or 1) end
TASKS = {}
function CreateColonistTransportTask(c, src, dst)
  local task = {colonist=c, src=src, dst=dst, state="new", shuttle=false}
  task.Cleanup = function(t) t.cancelled = true end
  c.transport_task = task
  TASKS[#TASKS+1] = task
  return task
end
SHUTTLE = {valid=true, transport_task=false}
SHUTTLE_IDLE = 0
function SHUTTLE.SetCommand() SHUTTLE_IDLE = SHUTTLE_IDLE + 1 end
RIDES = 0
function shuttle_loop()
  while true do
    local task
    for _, t in ipairs(TASKS) do
      if not task and t.state == "almost_ready_for_pickup" and not t.shuttle and not t.cancelled
          and IsValid(t.colonist) and t.colonist.transport_task == t then task = t end
    end
    if not task then Sleep(1000) else
      task.shuttle = SHUTTLE; SHUTTLE.transport_task = task
      Sleep(15000)
      local c = task.colonist
      if task.cancelled or not IsValid(c) or c.transport_task ~= task then
        task.state = "done"; SHUTTLE.transport_task = false
      else
        task.state = "transporting"; c.parent = SHUTTLE
        CommandObject.SetCommand(c, "RideShuttle")
        Sleep(45000)
        c.parent = nil; task.state = "done"; SHUTTLE.transport_task = false
        c.transport_task = false; c.dome = task.dst
        RIDES = RIDES + 1
        CommandObject.SetCommand(c, "Idle")
      end
    end
  end
end

-- population ---------------------------------------------------------------------
function colonist(name, dome, senior, extra)
  local c = setmetatable({name=name, valid=true, dome=dome, city=CITY, slot=dome and dome.slot or 1,
    traits={Senior=senior or nil}, status_effects={}, residence=false, workplace=false,
    dtors={}}, {__index=Colonist})
  if extra then for k, v in pairs(extra) do c[k] = v end end
  -- GotoBuildingSpot's reach is decided by where the walk started
  c.dome_before_leaving = dome
  local labels = UIColony.labels.Colonist
  labels[#labels+1] = c
  CommandObject.SetCommand(c, (extra and extra.cmd) or "Idle")
  return c
end
local orig_setdome = C.SetDome
function C:SetDome(d)
  if not d and self.dome then self.dome_before_leaving = self.dome end
  return orig_setdome(self, d)
end

function rocket(extra)
  local r = setmetatable({name="R", handle=1, valid=true, RocketType="Player",
    departure_loc={spot_type="our_colony"}, arrival_loc={spot_type="earth"},
    auto_mode_on=true, automode_start_time=0, departures={}, boarding={}, boarded={},
    stopover_departures=false, dtors={}, city=CITY}, {__index=UniversalRocketBase})
  if extra then for k, v in pairs(extra) do r[k] = v end end
  return r
end

GENERATE = {}
function count_generate_after(t)
  local n = 0 for _, x in ipairs(GENERATE) do if x > t then n = n + 1 end end return n
end
function watch_generate()
  local g = R.GenerateDepartures
  R.GenerateDepartures = function(self, ...) GENERATE[#GENERATE+1] = NOW; return g(self, ...) end
end
function boarded_has(r, name)
  for _, d in ipairs(r.boarded) do if d.name == name then return true end end
  return false
end
function in_list(t, c) for _, x in ipairs(t) do if x == c then return true end end return false end

SMRFixPack = {LOGS={}}
function SMRFixPack.Log(fmt, ...) SMRFixPack.LOGS[#SMRFixPack.LOGS+1] = string.format(fmt, ...) end
function SMRFixPack.Require(id, spec)
  for _, s in ipairs(spec) do
    if s.class and s.method then
      if type(_G[s.class]) ~= "table" or type(_G[s.class][s.method]) ~= "function" then return "missing "..s.class.."."..s.method end
    elseif s.global and type(_G[s.global]) ~= "function" then return "missing "..s.global end
  end
end
SMRFixPack.fixes = {}
SMRFixPack_Disabled = {}
function SMRFixPack.Register(id, def)
  REG_ID = id; REG_ERR = def.apply()
  SMRFixPack.fixes[id] = {status = REG_ERR and "inactive" or "active"}
end
'''

# the steady-state colony: a walker, three stopover riders, an out-of-reach senior
# (selected), a worker who turns Senior at the takeoff hold, a pad-dome colonist
# who turns Senior before the 2h draft, a senior on another map, a bystander,
# and one new far-dome Senior every 1.5 h
SCENARIO = r'''
R1 = rocket()
W1 = colonist("W1", PAD_DOME, true)
F1 = colonist("F1", FAR_DOME, true)
F2 = colonist("F2", FAR_DOME, true)
F3 = colonist("F3", FAR_DOME, true)
U1 = colonist("U1", false, true, {cmd="Abandoned"})
W2 = colonist("W2", PAD_DOME, false)
WORKER = colonist("WORKER", FAR_DOME, false, {cmd="Work", residence={}, workplace={}})
OTHER = colonist("OTHER", OTHER_DOME, true)
NON = colonist("NON", PAD_DOME, false)
SelectedObj = U1
CreateGameTimeThread(shuttle_loop)
INFLOW = 0
CreateGameTimeThread(function()
  while true do Sleep(45000); INFLOW = INFLOW + 1; colonist("I"..INFLOW, FAR_DOME, true) end
end)
CreateGameTimeThread(function() Sleep(45000); W2.traits.Senior = true end)
HOLD_SEEN = nil
CreateGameTimeThread(function()
  while true do
    if R1.takeoff_hold_end and not HOLD_SEEN then HOLD_SEEN = NOW; WORKER.traits.Senior = true end
    Sleep(1000)
  end
end)
MIN_PENDING, SAMPLES = nil, 0
CreateGameTimeThread(function()
  Sleep(CARGO_READY_AT + 1000)
  while not LAUNCHED do
    local p = R1:GetPendingDepartureCount()
    MIN_PENDING = MIN_PENDING and math.min(MIN_PENDING, p) or p
    SAMPLES = SAMPLES + 1
    Sleep(1000)
  end
end)
R1:SetCommand("CmdLoad")
'''


def extract():
    chunks = []
    for rel, pat in BODIES:
        lines = read_lines(str(ARCH / rel))
        hits = find_bodies(lines, pat)
        assert len(hits) == 1, (rel, pat, len(hits))
        s, e = hits[0]
        chunks.append((rel, s + 1, "\n".join(lines[s:e + 1])))
    rel, pats = SPAN
    lines = read_lines(str(ARCH / rel))
    rng = []
    for pat in pats:
        hits = find_bodies(lines, pat)
        assert len(hits) == 1, (rel, pat, len(hits))
        rng.append(hits[0])
    lo, hi = min(s for s, _ in rng), max(e for _, e in rng)
    chunks.append((rel, lo + 1, "\n".join(lines[lo:hi + 1])))
    return chunks


CHUNKS = extract()


def core_gate():
    """00_Core.lua's own veto gate, extracted (index_key, read_flag, WhenActive)."""
    lines = read_lines(str(pathlib.Path(db.REPO, "Code", "00_Core.lua")))
    parts = []
    for pat in (r"^local function index_key\(", r"^local function read_flag\(",
                r"^function SMRFixPack\.WhenActive\("):
        hits = find_bodies(lines, pat)
        assert len(hits) == 1, (pat, len(hits))
        a, b = hits[0]
        parts.append(chr(10).join(lines[a:b + 1]))
    return chr(10).join(parts)


def runtime(module_src):
    rt = db.lua_runtime()
    db.load_at(rt, db.ENGINE_SHIMS, "=deskbench_shims")
    db.load_at(rt, FIXTURE, "=C120_fixture")
    db.load_at(rt, core_gate(), "=Code/00_Core.lua(gate)")
    for rel, first, text in CHUNKS:
        db.load_at(rt, text, "=" + rel, first)
    rt.execute("watch_generate()")
    if module_src is not None:
        db.load_at(rt, module_src, "=Code/Fix_DeportRocketLaunch.lua")
        assert rt.eval("REG_ERR") is None, rt.eval("REG_ERR")
    return rt


def stall_leg(src):
    rt = runtime(src)
    db.load_at(rt, SCENARIO, "=C120_scenario")
    rt.execute("run_until(5 * 720000)")
    return rt


def launch_leg(src):
    rt = runtime(src)
    db.load_at(rt, SCENARIO, "=C120_scenario")
    rt.execute("run_until(5 * 720000)")
    if rt.eval("LAUNCHED"):
        rt.execute("run_until(LAUNCHED + 6 * 30000)")
    return rt


def e_leg(src, arrival_earth=False, clear_at=None):
    rt = runtime(src)
    rt.execute("""
      R1 = rocket({arrival_loc = %s,
                   boarded = {{name="held1", traits={Senior=true}}, {name="held2", traits={Senior=true}}}})
      W1 = colonist("W1", PAD_DOME, true)
      F1 = colonist("F1", FAR_DOME, true)
      CreateGameTimeThread(shuttle_loop)
      CommandObject.SetCommand(R1, "CmdWaitOrder")
      R1:UpdateDepartureThread()
      CLEAR_AT = %s
      if CLEAR_AT then CreateGameTimeThread(function() Sleep(CLEAR_AT); R1.arrival_loc = false end) end
      -- HourlyUpdate (UniversalRocket.lua:1563-1575) calls UpdateDepartureThread every hour while landed
      CreateGameTimeThread(function()
        Sleep(20000)
        while true do if R1:IsRocketLanded() then R1:UpdateDepartureThread() end Sleep(30000) end
      end)
    """ % ('{spot_type="earth"}' if arrival_earth else "false", clear_at if clear_at else "nil"))
    rt.execute("run_until(5 * 30000)")
    return rt


def e_leg_veto(src):
    rt = runtime(src)
    rt.execute("SMRFixPack_Disabled.DeportRocketLaunch = true")
    rt.execute("""
      R1 = rocket({arrival_loc = false})
      W1 = colonist("W1", PAD_DOME, true)
      CommandObject.SetCommand(R1, "CmdWaitOrder")
      R1:UpdateDepartureThread()
      CreateGameTimeThread(function()
        Sleep(20000)
        while true do if R1:IsRocketLanded() then R1:UpdateDepartureThread() end Sleep(30000) end
      end)
    """)
    rt.execute("run_until(5 * 30000)")
    return rt


def mutate(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new, 1)


def main():
    print("COMMAND: python tools/desk_c120_deport_rocket.py")
    print("HEAD:", subprocess.check_output(["git", "-C", db.REPO, "rev-parse", "HEAD"], text=True).strip())
    print("TREE:", ARCH)
    bench = db.Bench("C120 deport-law rocket: stall, K2 boarding + launch, E no-destination draft")
    check = bench.check
    src = db.read(str(MODULE))
    for rel, first, text in CHUNKS:
        print("  extracted %s:%d (%d lines)" % (rel, first, text.count("\n") + 1))

    # ---- fix off: the stall -------------------------------------------------
    off = stall_leg(None)
    ev = off.eval
    check("fix off: rocket never launches in 5 sols", ev("LAUNCHED == nil and R1.command == 'CmdLoad'"))
    check("fix off: pending count stays above zero every second after cargo is ready",
          ev("SAMPLES == (5 * 720000 - (CARGO_READY_AT + 1000)) // 1000 + 1 and MIN_PENDING > 0"), "min=%s over %s samples" % (ev("MIN_PENDING"), ev("SAMPLES")))
    check("fix off liveness: draft ran hourly, shuttle kept delivering, walkers kept boarding",
          ev("#GENERATE >= 100 and RIDES >= 50 and #R1.boarded >= 50"),
          "drafts=%s rides=%s boarded=%s inflow=%s" % (ev("#GENERATE"), ev("RIDES"), ev("#R1.boarded"), ev("INFLOW")))

    # ---- fix on: K2 ------------------------------------------------------------
    on = launch_leg(src)
    ev = on.eval
    check("fix on: rocket launches within an hour of cargo being ready",
          ev("LAUNCHED ~= nil and LAUNCHED - CARGO_READY_AT < 30000"), "launched at %s" % ev("LAUNCHED"))
    check("fix on: the hold ran and a colonist turned eligible during it", ev("HOLD_SEEN ~= nil and HOLD_SEEN < LAUNCHED"))
    check("K2 boards out-of-reach, awaiting-pickup and dropped-off deportees through the shipped fallback without walking",
          ev("boarded_has(R1,'U1') and boarded_has(R1,'F3') and boarded_has(R1,'I1') and GOTO.U1 == nil and GOTO.F3 == nil and GOTO.I1 == nil"))
    check("K2 waits out an old command's destructors: the worker boards, after its exit ran",
          ev("boarded_has(R1,'WORKER') and GOTO.WORKER == nil"),
          "order=" + ",".join(str(x) for x in ev("ORDER").values() if "WORKER" in str(x)))
    check("every K2 boarding ran CleanupLeavingColonist on the colonist's own command thread",
          ev("DONE.U1 and DONE.U1.own and DONE.F3.own and DONE.WORKER.own and DONE.I1.own"))
    check("boarded colonists went through SetDome(false) and lost residence and workplace",
          ev("SETDOME_FALSE.U1 == nil and SETDOME_FALSE.F3 and SETDOME_FALSE.WORKER and WORKER.residence == false and WORKER.workplace == false"),
          "U1 had no dome, so SetDome(false) is a no-op for it, as in the shipped body")
    check("the worker's exit finished before the LeavingMars prelude",
          ev("(function() local s,d,p for i,x in ipairs(ORDER) do if x=='WORKER:exit-done' then d=i end if x=='WORKER:setdome' then p=i end end return d and p and d < p end)()"))
    check("no boarded colonist is respawned and the selected one is deselected",
          ev("RESPAWNS == 0 and SelectedObj == nil and SELREMOVED == 1"))
    check("a committed shuttle ride is never cancelled: the shuttle gets no Idle order",
          ev("SHUTTLE_IDLE == 0"))
    check("at launch a walker and a committed ride were still pending (the release is exercised)",
          ev("#AT_LAUNCH.departures >= 1 and #AT_LAUNCH.rides >= 1"),
          "walkers=%s rides=%s" % (ev("#AT_LAUNCH.departures"), ev("#AT_LAUNCH.rides")))
    check("released walker: leaving false, off the list, Idle, eligible for the next rocket",
          ev("(function() for _, c in ipairs(AT_LAUNCH.departures) do if c.leaving or in_list(R1.departures, c) or c.command ~= 'Idle' or not c:CanChangeCommand() or not R1:IsColonistValidForDeparture(c) or c.transport_task then return false end end return true end)()"))
    check("released ride: task handed back (departure_rocket false), rider Idle and eligible after drop-off",
          ev("(function() for _, t in ipairs(AT_LAUNCH.rides) do local c = t.colonist if t.departure_rocket ~= false or not IsValid(c) or c.command ~= 'Idle' or not c:CanChangeCommand() or c.transport_task then return false end end return true end)()"))
    check("no colonist is left leaving outside LeavingMars (the RemoveLeavingColonistsNotInRocket shape)",
          ev("(function() for _, c in ipairs(UIColony.labels.Colonist) do if c.leaving and c.command ~= 'LeavingMars' then return false end end return true end)()"))
    check("the colonist on another map and the non-deportee are untouched",
          ev("OTHER.valid and OTHER.command == 'Idle' and not SETDOME_FALSE.OTHER and NON.valid and NON.command == 'Idle' and NON.dome == PAD_DOME and not SETDOME_FALSE.NON"))
    check("module logged the boarding and the release", ev("#SMRFixPack.LOGS >= 2"), " | ".join(on.eval("SMRFixPack.LOGS").values()))

    # ---- negative leg: a rocket waiting for manual launch --------------------
    man = runtime(src)
    db.load_at(man, SCENARIO.replace("R1 = rocket()", "R1 = rocket({auto_mode_on=false, auto_takeoff=false})"), "=C120_scenario")
    man.execute("run_until(CARGO_READY_AT + 3 * 30000)")
    check("manual-launch rocket: K2 boards nobody and does not launch",
          man.eval("LAUNCHED == nil and #SMRFixPack.LOGS == 0 and GOTO.U1 == nil and U1.valid"))

    # ---- E ----------------------------------------------------------------------
    e_off = e_leg(None)
    check("E fix off: an idle rocket with no destination drafts and holds",
          e_off.eval("#GENERATE >= 4 and (boarded_has(R1,'W1') or W1.command == 'LeavingMars') and RESPAWNS == 0 and #R1.boarded >= 2"))
    e_on = e_leg(src)
    check("E fix on: no destination drafts nobody, stops the thread, hands back the held",
          e_on.eval("#GENERATE == 0 and not IsValidThread(R1.departure_thread) and #R1.boarded == 0 and RESPAWNS == 2 and W1.command == 'Idle' and W1.valid"))
    e_earth = e_leg(src, arrival_earth=True)
    check("E control: an Earth-bound idle rocket still drafts with the fix on",
          e_earth.eval("#GENERATE >= 4 and (boarded_has(R1,'W1') or W1.command == 'LeavingMars')"))
    e_save = e_leg(src, arrival_earth=True, clear_at=10000)
    check("E existing save: a live draft thread on a rocket that lost its destination stops at the next hourly update",
          e_save.eval("#GENERATE >= 1 and count_generate_after(20000) == 0 and not IsValidThread(R1.departure_thread)"))

    # ---- mutants: each must FAIL a demand above ------------------------------
    m1 = launch_leg(mutate(src, 'cycle == rocket.command_thread and rocket.command == "CmdLoad"', "false"))
    check("mutant no-mark FAILS the no-walk boarding demand",
          not m1.eval("boarded_has(R1,'U1') and GOTO.U1 == nil and boarded_has(R1,'F3') and GOTO.F3 == nil"))
    m2 = launch_leg(mutate(src, "local waiting = still_boarding(cycle)", "local waiting = false"))
    check("mutant no-wait FAILS the worker-boards demand",
          not m2.eval("boarded_has(R1,'WORKER')"))
    m3 = e_leg(mutate(src, "if not self.arrival_loc and self.RocketType", "if false and self.RocketType"))
    check("mutant no-E FAILS the no-destination demand",
          not m3.eval("#GENERATE == 0 and #R1.boarded == 0"))

    # ---- the sitting's A/B: veto set on load, cleared once the stall has formed --------
    ab = runtime(src)
    ab.execute("SMRFixPack_Disabled.DeportRocketLaunch = true")
    db.load_at(ab, SCENARIO, "=C120_scenario")
    ab.execute("run_until(2 * 720000)")
    check("A (vetoed): stall forms -- no launch in 2 sols, pending never zero, no fix log",
          ab.eval("LAUNCHED == nil and MIN_PENDING > 0 and #SMRFixPack.LOGS == 0"),
          "min=%s" % ab.eval("MIN_PENDING"))
    ab.execute("SMRFixPack_Disabled.DeportRocketLaunch = nil; CLEARED = NOW; run_until(CLEARED + 30000)")
    check("B (veto cleared mid-session): launches within an hour, fix logged",
          ab.eval("LAUNCHED ~= nil and LAUNCHED - CLEARED < 30000 and #SMRFixPack.LOGS >= 1"),
          "launched %s ms after clearing" % ab.eval("LAUNCHED and LAUNCHED - CLEARED"))
    m4 = runtime(mutate(src, "SMRFixPack.WhenActive(FIX_ID, function(self, instant, ...)",
                        "(function(_, f) return f end)(FIX_ID, function(self, instant, ...)"))
    m4.execute("SMRFixPack_Disabled.DeportRocketLaunch = true")
    db.load_at(m4, SCENARIO, "=C120_scenario")
    m4.execute("run_until(2 * 720000)")
    check("mutant ungated-K2 FAILS the vetoed-stall demand", m4.eval("LAUNCHED ~= nil"))
    ev_veto = e_leg_veto(src)
    check("E vetoed: an idle no-destination rocket drafts as vanilla does",
          ev_veto.eval("#GENERATE >= 4 and RESPAWNS == 0"))

    check("module declares no save hook, persisted variable or thread",
          all(t not in src for t in ("OnMsg.Save", "GameVar(", "MapVar(", "CreateGameTimeThread", "CreateRealTimeThread")))

    return bench.finish("ALL DEMANDS HELD -- desk-verified on archived 1.1.1.405907 Lua, not in game.")


if __name__ == "__main__":
    sys.exit(main())
