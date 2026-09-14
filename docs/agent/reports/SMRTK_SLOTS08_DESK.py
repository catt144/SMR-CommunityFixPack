"""smrtk 08 slot falsifiers: execute Code/80_AgentSlots.lua against shimmed
native services. Shim style follows SMRTK_P5_DESK.py. No engine/colony claim -
this proves the slot LOGIC, never the game's behaviour."""
from pathlib import Path
import sys
from lupa import LuaRuntime

import os
KIT = Path(os.environ.get("SMRTK_DESK_KIT", r"C:\Dev\SMR-BugFixPack-TestKit"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
lua = LuaRuntime(unpack_returned_tuples=True)

lua.execute(r'''
hooks, logs, threads, events = {}, {}, {}, {}
game_time = 1000
OnMsg = setmetatable({}, {__newindex=function(_,n,f) hooks[n]=hooks[n] or {}; table.insert(hooks[n],f) end})
function emit(n,...) for _,f in ipairs(hooks[n] or {}) do f(...) end end
function ModLog(s) logs[#logs+1]=string.format(s) end
function ConsolePrint(s) end
function FlushLogFile() end
function GameTime() return game_time end
function AreCheatsUsed() return cheats_used or false end
function CopyToClipboard(s) clipboard=s end
function SaveLocalStorage() return true end
function CreateRealTimeThread(f) threads[#threads+1]=f; return f end
function CreateGameTimeThread(f) game_threads[#game_threads+1]=f; return f end
game_threads = {}
function drain() local t=threads; threads={}; for _,f in ipairs(t) do f() end end
sleep_budget = 40
function Sleep(ms)
  game_time = game_time + (ms or 0)
  sleep_budget = sleep_budget - 1
  if sleep_budget <= 0 then error("desk: sleep budget exhausted") end
  if on_sleep then on_sleep() end
end
-- A game-time thread body is an endless poll loop in real life; on the desk we
-- turn it a bounded number of times and treat budget exhaustion as "still polling".
function turn_game_threads(n)
  sleep_budget = n or 40
  local t = game_threads; game_threads = {}
  for _, f in ipairs(t) do pcall(f) end
end
function IsValidThread(t) return t ~= nil and t ~= false end
function DeleteThread(t) end
function CurrentThread() return "desk" end
function IsRealTimeThread() return true end
function IsThreadInside() return true end
function PlayFX() fx_played = (fx_played or 0) + 1 end
function SetGameSpeed(n) game_speed = n end
function GetGameSpeed() return game_speed == 0 and "pause" or game_speed end
function GetTimeFactor() return (game_speed or 1) * 100 end
function AsyncRand(n) return 7 end
function GetPreciseTicks() return 12345 end
function ObjModified(o) end
function IsValid(o) return type(o)=='table' and o.valid==true end
function IsKindOf(o,k) return type(o)=='table' and (o.class==k or (o.kinds and o.kinds[k])) or false end
function PropObjHasMember(o,n) return type(o)=='table' and o[n]~=nil end
function WorldToHex(p) return 1,2 end
LocalStorage={}
LuaRevision = 403908
game_speed = 1
empty_table = setmetatable({}, {__newindex=function() error('empty_table written') end})
const = { GameSpeeds={fast=3}, MaxSaneTimeFactor=1000, DefaultTimeFactor=100 }
config = { SaveGameExt=".sav" }
terminal={targets={}}
function terminal.AddTarget(o) terminal.targets[o]=true end
function terminal.RemoveTarget(o) terminal.targets[o]=nil end
TerminalTarget={new=function(self,t) return t end}
function GetTerrainCursor() return "pt(100,200)" end
function SelectionMouseObj() return clicked_obj end
function GetInGameInterfaceModeDlg() return nil end
function GetInGameInterface() return nil end
-- Kit/TestKit registry the preflight reads for its order key.
SMRTest = { order = {"p1","p2"}, probes = {p1=true,p2=true}, Log = {},
  LoggerState=function() return false end }
CurrentMap = { map_id = "desk_map" }
UIColony = { day = 490 }
UICity = { labels = { Building = {}, Colonist = {}, Drone = {},
  ConstructionSite = {}, UniversalRocketBase = {} } }
SelectedObj = nil
function object(class, kinds, fields)
  local o = { valid=true, class=class, handle=(next_handle or 0)+1, kinds=kinds or {} }
  next_handle = o.handle
  for k,v in pairs(fields or {}) do o[k]=v end
  return o
end
''')

def load(name):
    lua.execute((KIT / "Code" / name).read_text(encoding="utf-8-sig"))

load("70_SMRTK_Core.lua")
lua.execute("function SMRTK.Page(...) end function SMRTK.Button(...) return {} end")
load("74_SMRTK_Agent.lua")
load("75_SMRTK_Saves.lua")
load("76_SMRTK_Kit.lua")

# Stubs for the two registered actions slot 5 and slot 6 orchestrate. These are
# NOT 72/73 - their own payload desks cover those. A stub for something that can
# REFUSE is itself a behaviour change, so each is exercised both ways below.
lua.execute(r'''
run_until_refuses = false
SMRTK.Action { id="run_until", verb="SPEED", run=function(ctx,event)
  if ctx.phase ~= "fire" then return false, "arm run-until first" end
  SetGameSpeed(0); return { paused = true, target = ctx.state.target }
end, arm=function(ctx,target)
  if run_until_refuses then return false, "desk: run-until refused" end
  if not SMRTK.triggers[target] or not SMRTK.armed[target] then return false, "choose an armed Agent trigger id" end
  ctx.state.target = target
  return { target = target, requested = 10, before = 1, factor = 1000 }
end, disarm=function(ctx) end }

fill_refuses = false
SMRTK.Action { id="selected_fill", verb="ACTION", needs="selected", run=function(ctx, expected)
  local obj = ctx.selected
  if expected and obj ~= expected then return false, "selection changed; choose the action again" end
  if fill_refuses then return false, "selected object does not support CheatFill" end
  obj.stored = 5000
  return { object="d", method="CheatFill", before=0, after=5000, resources=4,
    resource="multiple", valid_after=true }
end }
''')

load("80_AgentSlots.lua")

FAILS = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("  -- " + str(detail)) if detail else ""))
    if not cond:
        FAILS.append(name)

def loglines():
    return list(lua.globals().logs.values())

def last(verb):
    for line in reversed(loglines()):
        if " SMRTK_" + verb + " " in line:
            return line
    return ""

def run(code):
    lua.execute(code)

print("\n== A. every slot bound, nothing armed at load ==")
errs = [l for l in loglines() if "SMRTK_SLOT_ERROR" in l]
check("no SLOT_ERROR at load", not errs, errs)
bound = lua.eval('(function() local n=0 for _,id in pairs(SMRTK.slots) do if SMRTK.actions[id] then n=n+1 end end return n end)()')
check("slots 1-6 bound", bound == 6, bound)
check("scratch bound", lua.eval('SMRTK.actions.slot_scratch ~= nil'))
check("smrtk08_break registered", lua.eval('SMRTK.triggers.smrtk08_break ~= nil'))
check("nothing armed at mod load", lua.eval("SMRTK.ArmedCount()") == 0)
check("SLOTS banner logged", "SMRTK_SLOTS" in "".join(loglines()))

print("\n== B. slot 2 accepts the embedded desktop evidence ==")
run('ok2, f2 = SMRTK.Run("slot_2")')
print("      " + last("PROBE_PREFLIGHT"))
check("slot_2 status OK", lua.eval("ok2") is True, lua.eval("f2.reason"))
check("PROBE_PREFLIGHT clean=true", "clean=true" in last("PROBE_PREFLIGHT"))
check("attestation stored", lua.eval("SMRTK.kit.preflight ~= nil"))
# ProbeHygiene returns two values; unpack_returned_tuples hands back a tuple.
hyg = lua.eval("SMRTK.ProbeHygiene()")
ok, why = (hyg[0], hyg[1]) if isinstance(hyg, tuple) else (hyg, "")
check("hygiene now clean", ok is True, why)
check("  hygiene quotes the desk HEADs", "3ae67dea" in str(why) and "c886fb70" in str(why), why)

print("\n== C. the gate really is a gate (negative legs) ==")
run('SMRTK.kit.preflight = nil; ok_gate, f_gate = SMRTK.Run("run_all")')
check("run_all REFUSED with no attestation",
      lua.eval('f_gate.status') == "REFUSED", lua.eval("f_gate.reason"))
check("  reason names the sweep",
      "desktop probe sweep not provisioned" in str(lua.eval("f_gate.reason")))
run('SMRTK.Run("slot_2"); emit("PreLoadGame")')
check("load expires the attestation", lua.eval("SMRTK.kit.preflight == nil"))
run('saved_session = SMRTK.session; SMRTK.session = "foreign"; ok_s, f_s = SMRTK.Run("slot_2"); SMRTK.session = saved_session')
check("slot_2 still OK after re-press (live session read, not baked)",
      lua.eval("ok_s") is True, lua.eval("f_s.reason"))
run('SMRTK.kit.preflight=nil; saved_game=LuaRevision; LuaRevision=999999; ok_g, f_g = SMRTK.Run("slot_2"); LuaRevision=saved_game')
check("slot_2 tracks a changed build too", lua.eval("ok_g") is True, lua.eval("f_g.reason"))
run('SMRTK.kit.preflight=nil; saved_map=CurrentMap; CurrentMap=nil; ok_m, f_m = SMRTK.Run("slot_2"); CurrentMap=saved_map')
check("slot_2 REFUSES with no colony loaded", lua.eval('f_m.status') == "REFUSED", lua.eval("f_m.reason"))

print("\n== D. slot 5: breakpoint + run-until ==")
run('SMRTK.kit.preflight=nil; game_time = 10000; ok5, f5 = SMRTK.Run("slot_5")')
print("      " + last("ARM"))
check("slot_5 OK", lua.eval("ok5") is True, lua.eval("f5.reason"))
check("breakpoint armed", lua.eval("SMRTK.armed.smrtk08_break ~= nil"))
check("run_until armed", lua.eval("SMRTK.armed.run_until ~= nil"))
check("target is now+5000", lua.eval('SMRTK.armed.smrtk08_break.state.target') == 15000)
run('ok5b, f5b = SMRTK.Run("slot_5")')
check("re-press REFUSED while armed", lua.eval('f5b.status') == "REFUSED", lua.eval("f5b.reason"))
# advance game time and turn the trigger's poll by hand
run('''
game_time = 16000
turn_game_threads(6)
drain(); drain()
''')
print("      " + last("TRIGGER"))
check("TRIGGER fired", "action=smrtk08_break" in last("TRIGGER") and "status=OK" in last("TRIGGER"))
check("trigger did NOT pause (run_until owns the pause)",
      "pause=true" not in last("TRIGGER"), last("TRIGGER"))
check("trigger marked + sounded", "mark=" in last("TRIGGER") and "sound=true" in last("TRIGGER"))
check("breakpoint auto-disarmed", lua.eval("SMRTK.armed.smrtk08_break == nil"))

print("\n== D2. slot 5 leaves nothing armed when run-until refuses ==")
run('''
SMRTK.DisarmAll("desk reset"); run_until_refuses = true
game_time = 20000
ok5c, f5c = SMRTK.Run("slot_5")
''')
check("slot_5 REFUSED", lua.eval('f5c.status') == "REFUSED", lua.eval("f5c.reason"))
check("  reason names run-until", "run-until arm refused" in str(lua.eval("f5c.reason")))
check("breakpoint NOT left armed", lua.eval("SMRTK.armed.smrtk08_break == nil"))
check("nothing armed at all", lua.eval("SMRTK.ArmedCount()") == 0)
run('run_until_refuses = false')

print("\n== E. slot 4: armed click reader, once ==")
run('''
clicked_obj = object("Drone", {Drone=true})
ok4, f4 = SMRTK.Arm("slot_4")
''')
check("slot_4 armed", lua.eval("ok4") is True, lua.eval("f4.reason"))
check("click target acquired", lua.eval('SMRTK.click_capture ~= nil and SMRTK.click_capture.id == "slot_4"'))
run('''
capture = SMRTK.click_capture.target
capture:OnMouseButtonDown("pt", "L")
drain(); drain()
''')
print("      " + last("FIRE"))
check("one FIRE recorded", "clicks=1" in last("FIRE"), last("FIRE"))
check("click read the object", 'object="Drone(' in last("FIRE") or "object=Drone(" in last("FIRE"), last("FIRE"))
check("auto-disarmed after one click (once_click)", lua.eval("SMRTK.armed.slot_4 == nil"))
check("click target released", lua.eval("SMRTK.click_capture == nil"))
check("DISARM carries the click count", "clicks=1" in last("DISARM"), last("DISARM"))
run('''
SMRTK.Arm("slot_4")
SMRTK.click_capture.target:OnMouseButtonDown("pt", "R")
drain()
''')
check("right-click cancels without firing", lua.eval("SMRTK.armed.slot_4 == nil"))
check("  and logs the cancel reason", 'reason="right click"' in last("DISARM") or "right click" in last("DISARM"), last("DISARM"))

print("\n== F. slot 6: checked bracket around a representative mutation ==")
run('''
SMRTK.DisarmAll("desk reset")
depot = object("UniversalStorageDepot", {UniversalStorageDepotBase=true},
  { working=true, malfunction=false, GetPos=function() return "pt" end })
SelectedObj = depot
ok6, f6 = SMRTK.Run("slot_6")
''')
print("      " + last("DUMP"))
check("slot_6 OK", lua.eval("ok6") is True, lua.eval("f6.reason"))
d = last("DUMP")
check("DUMP brackets before/after", "amount_before=0" in d and "amount_after=5000" in d, d)
check("DUMP carries scalar state both sides", "state_before=" in d and "state_after=" in d, d)
marks = [l for l in loglines() if "SMRTK08_S6_" in l]
check("MARK before and after", len(marks) >= 2, marks)
run('SelectedObj = nil; ok6b, f6b = SMRTK.Run("slot_6")')
check("no selection REFUSED", lua.eval('f6b.status') == "REFUSED", lua.eval("f6b.reason"))
run('''
SelectedObj = object("Habitat", {Building=true})
fill_refuses = true
ok6c, f6c = SMRTK.Run("slot_6")
fill_refuses = false
''')
check("unsupported object REFUSED, not invented", lua.eval('f6c.status') == "REFUSED", lua.eval("f6c.reason"))
check("  refusal names the method", "CheatFill" in str(lua.eval("f6c.reason")))
check("  refusal still emits its DUMP", 'phase=refused' in last("DUMP"), last("DUMP"))

print("\n== G. slot 3 + scratch: read-only ==")
run('''
SelectedObj = nil
SMRTK.pins.A = object("Dome", {Dome=true})
SMRTK.saves.loaded = { present=true, session="other-session", actions=12, last="mark" }
before_mut = SMRTK.sequence
ok3, f3 = SMRTK.Run("slot_3")
''')
print("      " + last("DUMP"))
check("slot_3 OK", lua.eval("ok3") is True, lua.eval("f3.reason"))
check("reports the foreign provenance", 'provenance_session=other-session' in last("DUMP"), last("DUMP"))
check("session_matches false", "session_matches=false" in last("DUMP"))
check("attestation reported expired", "attestation=expired" in last("DUMP"))
check("arms/pins reported", "armed_count=0" in last("DUMP") and "A=Dome(" in last("DUMP"))
run('''
UICity.labels.Building = { object("UniversalStorageDepot",{UniversalStorageDepotBase=true}),
  object("MechanizedDepot",{MechanizedDepot=true,UniversalStorageDepotBase=true}),
  object("DomeBasic",{Dome=true}), object("DroneHub",{DroneHub=true}) }
UICity.labels.Colonist = { 1, 2, 3 }
UICity.labels.Drone = { 1, 2 }
rocket = object("UniversalRocket", {UniversalRocketBase=true},
  { command="CmdFlyToLocation", is_paused=false, arrival_loc={spot_type="our_colony"},
    command_thread=true, arrival_time=99999 })
UICity.labels.UniversalRocketBase = { rocket }
oks, fs = SMRTK.Run("slot_scratch")
''')
print("      " + last("DUMP"))
s = last("DUMP")
check("scratch OK", lua.eval("oks") is True, lua.eval("fs.reason"))
check("counts universal vs mechanized depots separately",
      "depots_universal=1" in s and "depots_mechanized=1" in s, s)
check("counts domes and hubs", "domes=1" in s and "drone_hubs=1" in s, s)
check("rocket fitness uses the rocket_arrive predicate",
      "rockets=1" in s and "rockets_ready=1" in s, s)
run('''
rocket.arrival_loc = { spot_type = "somewhere_else" }
SMRTK.Run("slot_scratch")
''')
check("a rocket not bound for our colony is NOT ready",
      "rockets=1" in last("DUMP") and "rockets_ready=0" in last("DUMP"), last("DUMP"))
check("grids declared a screen check, not invented",
      "grids=" in last("DUMP") and "screen check" in last("DUMP"))

print("\n== H. taint + tagging invariants across everything run above ==")
lines = loglines()
untagged = [l for l in lines if not l.startswith("[SMRTK] SMRTK_")]
check("every line carries the tag", not untagged, untagged[:3])
check("no TAINT record", not [l for l in lines if "SMRTK_TAINT " in l])
check("no ERROR record", not [l for l in lines if "SMRTK_ERROR " in l], [l for l in lines if "SMRTK_ERROR " in l][:2])
check("error counter still zero", lua.eval("SMRTK.error_count") == 0)
check("nothing left armed", lua.eval("SMRTK.ArmedCount()") == 0, lua.eval("SMRTK.ArmedCount()"))
check("print not left wrapped", lua.eval("SMRTK.armed.print_tee == nil"))

print("\n== I. the sweep string in 80 matches 76's, and 80 is not its own hit ==")
kit_sweep = lua.eval('SMRTK.actions.probe_preflight ~= nil')
src80 = (KIT / "Code" / "80_AgentSlots.lua").read_text(encoding="utf-8")
src76 = (KIT / "Code" / "76_SMRTK_Kit.lua").read_text(encoding="utf-8")
token = "TEMP" + "ORARY"
check("80 does not contain the bare probe token", token not in src80)
check("76 does not contain it either (control)", token not in src76)
check("both assemble the same split", "'TEMP' .. 'ORARY'" in src80.replace('"', "'")
      and "'TEMP' .. 'ORARY'" in src76.replace('"', "'"))

print("\n" + ("DESK RESULT: PASS" if not FAILS else "DESK RESULT: %d FAIL(S): %s" % (len(FAILS), ", ".join(FAILS))))
sys.exit(1 if FAILS else 0)
