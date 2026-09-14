"""P4 desk falsifier: actual Lua with yielding fake native services, never play proof."""
from pathlib import Path
import re
import sys
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
sys.path.insert(0, str(ROOT))
from tools.parsecheck import runtime

parse, version = runtime()
for name in ("75_SMRTK_Saves.lua", "76_SMRTK_Kit.lua", "90_Loggers.lua"):
    source = (KIT / "Code" / name).read_text(encoding="utf-8-sig")
    assert parse(source, "@" + name) is None
    print(f"PARSE {name}: 0 errors [{version}]")
    if name.startswith(("75", "76")):
        for gate, pattern in (("NO SYNC", r"NetSyncEvent|LogCheatUsed"), ("NO BARE PRINT", r"^\s*print\("), ("PROBE TOKEN", "TEMPORARY")):
            hits = sum(bool(re.search(pattern, line)) for line in source.splitlines())
            print(f"{gate} {name}: {hits} lines")
            assert hits == 0

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
hooks, logs, threads, stored = {}, {}, {}, {}
OnMsg=setmetatable({}, {__newindex=function(_,name,fn)
  hooks[name]=hooks[name] or {}; table.insert(hooks[name],fn)
end})
function emit(name,...) for _,fn in ipairs(hooks[name] or {}) do fn(...) end end
clock, active_thread, taint, flushes = 20, false, false, 0
function GameTime() return clock end
function GetPreciseTicks() return 12345 end
function AsyncRand(max) return max-1 end
function AreCheatsUsed() return taint end
function FlushLogFile() flushes=flushes+1 end
function ModLog(s) logs[#logs+1]=string.format(s) end
function ConsolePrint(s) emit('ConsoleLine',s,true) end
function IsValid(o) return type(o)=='table' and not o.deleted end
function IsValidThread(t) return type(t)=='table' and t.co and not t.cancelled and coroutine.status(t.co)~='dead' end
function DeleteThread(t) t.cancelled=true end
function CurrentThread() return active_thread end
function IsRealTimeThread() return active_thread and active_thread.kind=='real' or false end
function thread(kind,fn,...)
  local a=table.pack(...); local t={kind=kind,co=coroutine.create(function() fn(table.unpack(a,1,a.n)) end)}
  threads[#threads+1]=t; return t
end
function CreateRealTimeThread(fn,...) return thread('real',fn,...) end
function CreateGameTimeThread(fn,...) return thread('game',fn,...) end
function Sleep(ms) return coroutine.yield(ms) end
function step(kind)
  local todo={}; for _,t in ipairs(threads) do todo[#todo+1]=t end
  for _,t in ipairs(todo) do if t.kind==kind and IsValidThread(t) then
    active_thread=t; local ok,why=coroutine.resume(t.co); active_thread=false; assert(ok,why)
  end end
end
function real(fn) CreateRealTimeThread(fn); step('real') end
function settle() for i=1,4 do step('real') end end
function tick() clock=clock+1000; step('game'); step('real') end
function count(verb,action,from)
  local n=0; for i=from or 1,#logs do
    if logs[i]:find('SMRTK_'..verb..' ',1,true) and (not action or logs[i]:find('action='..action..' ',1,true)) then n=n+1 end
  end; return n
end
function RGBA(...) return table.concat({...},',') end
function RGB(...) return RGBA(...) end
function box(...) return {...} end
function point(x,y) return {x=function() return x end,y=function() return y end} end
local W={}
function W:new(props,parent)
  props=props or {}; props.parent=parent; props.window_state='open'; setmetatable(props,{__index=self})
  if parent then parent[#parent+1]=props end; return props
end
function W:SetText(s) self.Text=s end
function W:GetText() return self.Text or '' end
function W:SetBackground(s) self.Background=s end
function W:SetTextColor(s) self.TextColor=s end
function W:SetEnabled(s) self.enabled=s end
function W:SetItems(s) self.Items=s end
function W:Open() self.window_state='open' end
function W:delete() self.window_state='destroying' end
function W:CreateThread(name,fn) self[name]=CreateRealTimeThread(fn) end
XWindow=W; XText=W; XButton=W; XTextEditor=W; XCombo=W; XScrollArea=W; XDialog=W
function cls() cleared=(cleared or 0)+1 end
function ShowConsole(on) console_requests=(console_requests or 0)+1; assert(ConsoleEnabled==true and on==true) end
function SaveLocalStorage() end
function SetGameSpeed(s) speed=s end
function GetGameSpeed() return speed or 1000 end
function PlayFX() end
function CopyToClipboard(s) clipboard=s end
function GetTerrainCursor() return {} end
function GenerateScreenshotFilename(prefix,folder) return folder..prefix..'0001.png' end
function WriteScreenshot() return nil end
function WorldToHex(pos) return pos.q,pos.r end
function GetColonyTotalResources(res) return total_resources[res] or 0 end
LocalStorage={}; config={SaveGameExt='.sav'}; SavingGame=false; SavegameRunningThread=false
LuaRevision=403908; CurrentMap={}; MainMap={g_DustDevils={}}; speed=1000
UIColony={day=10,funds={GetFunding=function() return funds end}}; funds=100
SelectedObj={class='UniversalDepot',handle=7,template_name='StorageMetals',command='Idle',counter=0,
  stockpiled_amount={Metals=2}, workers={{class='Colonist',handle=8}}, destroyed=false,
  GetPos=function() return {q=2,r=3} end}
UICity={labels={Colonist={SelectedObj},Building={SelectedObj}}}
total_resources={Metals=3}; TransportableResourceIds={'Metals'}
g_DustStorm=false; g_ColdWave=false; g_MeteorStorm=false; g_RainDisaster=false; g_MarsquakeActive=false
ModsLoaded={{id='SMR_CommunityFixPack',version=11},{id='Other',version=2}}
SMRFixPack={order={'a','b'},fixes={a={status='active'},b={status='blocked'}}}
probe_runs, all_runs=0,0
SMRTest={order={'DeskProbe'},probes={DeskProbe={}},last={},Print=function() end}
function SMRTest.SetGlobal(key,v) _G[key]=v end
function SMRTest.Run(id) probe_runs=probe_runs+1; SMRTest.last[id]={status='PASS',msg='desk'}; return 'PASS','desk' end
function SMRTest.RunAll() all_runs=all_runs+1; return {PASS=1,FAIL=0,ERROR=0,SKIP=0} end
Colonist={ShouldLeaveForWork=function() return 'original' end}
MeteorsDisaster=function() return 'meteor' end
Savegame={}
function Savegame.Load(name,cb)
  assert(IsRealTimeThread(),'metadata needs real time')
  metadata_reads=(metadata_reads or 0)+1
  Sleep(1)
  if fail_metadata then return 'corrupt' end
  current_meta=stored[name]; if not current_meta then return 'missing' end
  return cb('mounted')
end
function LoadMetadata(folder) assert(folder=='mounted'); return nil,current_meta end
function LoadMetadataCallback() destructive_callback=(destructive_callback or 0)+1; error('wrong callback') end
function SaveGame(title,params)
  assert(IsRealTimeThread() and not SavingGame and params.silent and params.savename)
  save_calls=(save_calls or 0)+1; SavingGame=true; emit('SaveGameStart',params)
  local m={}; emit('GatherGameMetadata',m); Sleep(1)
  SavingGame=false
  if fail_save then return 'native save error' end
  stored[params.savename]=m; emit('SavegameSaved',params.savename); return nil,params.savename,m
end
function LoadGame(name)
  assert(IsRealTimeThread() and not SavingGame)
  load_calls=(load_calls or 0)+1; Sleep(1)
  if fail_load then return 'native load error' end
  emit('PreLoadGame'); emit('DoneGame'); emit('GameMetadataLoaded',stored[name]); return nil
end
function findbutton(parent,title)
  for _,b in ipairs(parent) do
    for _,v in ipairs(b) do if v.Text==title and b.OnPress then return b end end
    local found=findbutton(b,title); if found then return found end
  end
end
''')
for name in ("70_SMRTK_Core.lua", "71_SMRTK_Panel.lua", "74_SMRTK_Agent.lua", "75_SMRTK_Saves.lua", "76_SMRTK_Kit.lua", "90_Loggers.lua"):
    lua.execute((KIT / "Code" / name).read_text(encoding="utf-8-sig"))


def case(name, code):
    lua.execute(code)
    print("PASS " + name)


case("idle has no logger/trigger arms or callback replacements", r'''
T=SMRTK; orig_meteor=MeteorsDisaster; orig_work=Colonist.ShouldLeaveForWork
assert(T.ArmedCount()==0 and not SMRTest.LoggerState('Meteors'))
assert(MeteorsDisaster==orig_meteor and Colonist.ShouldLeaveForWork==orig_work)
assert(T.actions.dump_selected and T.actions.watch_field)
''')
case("saves refuse UI/game-time callers and native busy before mutation", r'''
assert(not T.Run('save_A')); assert(not save_calls)
CreateGameTimeThread(function() assert(not T.Run('save_A')) end); step('game'); assert(not save_calls)
real(function() SavingGame=true; assert(not T.Run('save_A')); SavingGame=false end); assert(not save_calls)
SavegameRunningThread=CreateRealTimeThread(function() Sleep(100) end)
real(function() assert(not T.Run('save_A')) end); assert(not save_calls)
DeleteThread(SavegameRunningThread); SavegameRunningThread=false
''')
case("real-time yielding save has one result, fixed slot name and provenance", r'''
local from=#logs+1
real(function() assert(T.Run('save_A')) end)
assert(T.saves.busy and count('SAVE','save_A',from)==0)
settle(); assert(not T.saves.busy and count('SAVE','save_A',from)==1)
assert(stored['SMRTK_A.sav'].smrtk.session==T.session)
assert(type(stored['SMRTK_A.sav'].smrtk.last)=='table')
''')
case("foreign/missing provenance refuses before LoadGame; override logged once", r'''
stored['SMRTK_B.sav']={smrtk={session='foreign',actions=3,last={action='fixture'}}}
local from=#logs+1
real(function() assert(not T.Run('load_B')) end); settle(); assert(not load_calls)
assert(T.saves.status:find('foreign session',1,true))
real(function() assert(T.Run('load_override_B')) end); settle()
assert(load_calls==1 and count('LOAD_OVERRIDE','load_override_B',from)==1)
assert(count('PROVENANCE',nil,from)==1 and not destructive_callback)
stored['SMRTK_C.sav']={}
real(function() assert(not T.Run('load_C')) end); settle(); assert(load_calls==1)
''')
case("metadata errors block override; save/load errors release toolkit lock", r'''
fail_metadata=true
real(function() assert(not T.Run('load_override_B')) end); settle(); assert(load_calls==1 and not T.saves.busy)
fail_metadata=false; fail_save=true
real(function() assert(not T.Run('save_C')) end); settle(); assert(not T.saves.busy)
fail_save=false; fail_load=true
real(function() assert(not T.Run('load_override_B')) end); settle(); assert(not T.saves.busy)
fail_load=false
''')
case("metadata race with new save refuses load after mount", r'''
local calls=load_calls
real(function() assert(not T.Run('load_override_B')) end)
SavingGame=true; settle(); SavingGame=false
assert(load_calls==calls and not T.saves.busy)
''')
case("probes default-refuse and dishonest/incomplete stamp refuses", r'''
real(function() assert(not T.Run('run_all')); assert(not T.Run('run_probe','DeskProbe')) end)
assert(all_runs==0 and probe_runs==0)
e={session=T.session,sitting=T.kit.sitting,game=LuaRevision,pack_head=string.rep('a',40),testkit_head=string.rep('b',40),
  checked_at='desk UTC',brief='P4 desk',command='grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/',output='',exit=1,hits={},needed={}}
assert(not T.ProbePreflight({clean=true})); e.output='not empty'; assert(not T.ProbePreflight(e)); e.output=''
''')
case("provisioned desktop stamp enables both run routes and expires on registry/map", r'''
assert(T.ProbePreflight(e)); assert(T.ProbeHygiene())
real(function() assert(T.Run('run_all')); assert(T.Run('run_probe','DeskProbe')) end)
assert(all_runs==1 and probe_runs==1)
SMRTest.order[2]='New'; real(function() assert(not T.Run('run_all')) end); SMRTest.order[2]=nil
assert(all_runs==1); assert(T.ProbePreflight(e)); emit('CurrentMapChange'); assert(not T.ProbeHygiene())
''')
case("named sweep hits require exact stdout and explicit needed-probe declaration", r'''
e.sitting=T.kit.sitting; e.hits={'Code/needed.lua'}; e.output='Code/needed.lua\n'; e.exit=0
assert(not T.ProbePreflight(e)); e.needed={'Code/needed.lua'}; assert(T.ProbePreflight(e))
e.output='Code/stale.lua\n'; assert(not T.ProbePreflight(e))
''')
case("logger state copy cannot mutate native state and manual arms are refused", r'''
T.EnsureKitLoggers(); assert(T.actions.logger_Meteors)
assert(SMRTest.Log.Meteors(true)); local copy=SMRTest.LoggerState(); copy.Meteors=nil
assert(SMRTest.LoggerState('Meteors'))
local manual=MeteorsDisaster
real(function() assert(not T.Arm('logger_Meteors')) end)
assert(MeteorsDisaster==manual and SMRTest.LoggerState('Meteors'))
SMRTest.Log.Meteors(false); assert(MeteorsDisaster==orig_meteor)
''')
case("toolkit logger arms/restores on lifecycle and refuses quiet layering", r'''
T.armed.quiet={state={}}
real(function() assert(not T.Arm('logger_Meteors')) end); T.armed.quiet=nil
real(function() assert(T.Arm('logger_Meteors')) end)
assert(MeteorsDisaster~=orig_meteor and SMRTest.LoggerState('Meteors'))
emit('SavegameSaved'); assert(MeteorsDisaster==orig_meteor and not SMRTest.LoggerState('Meteors'))
''')
case("fingerprint reads public registry and live ModDef without ListFixes", r'''
SMRFixPack.ListFixes=function() error('printing accessor must never run') end
assert(T.Run('fingerprint')); assert(T.kit.fingerprint.fix_pack_present=='1/2')
assert(T.kit.fingerprint.pack_version==11 and T.kit.fingerprint.mods=='Other,SMR_CommunityFixPack')
SMRFixPack.fixes.b.status='active'; assert(T.Run('fingerprint')); assert(T.kit.fingerprint.fix_pack_present=='2/2')
-- Frozen core hook is merge work; test the installed callback contract directly.
local from=#logs+1; T.after_record.MARK({action='screenshot_mark'})
assert(count('FINGERPRINT','fingerprint',from)==1 and T.kit.fingerprint.mark_action=='screenshot_mark')
''')
case("dump preserves false flags and snapshot numeric diff observes detached data", r'''
assert(T.Run('dump_selected')); assert(T.kit.dump.destroyed=='false' and T.kit.dump.hex=='2,3')
assert(T.Run('snapshot')); local a=T.kit.next_snapshot
funds=135; total_resources.Metals=5; UIColony.day=11; g_DustStorm={active=true}
assert(T.Run('snapshot')); local b=T.kit.next_snapshot
assert(T.kit.snapshots[a].funding==100 and T.kit.snapshots[b].funding==135)
local ok,v=T.Run('snapshot_diff',a,b); assert(ok and v.changes:find('funding:35',1,true))
assert(v.changes:find('resources.Metals:2',1,true)); assert(not T.Run('snapshot_diff',999,b))
local funding_method=UIColony.funds.GetFunding
UIColony.funds.GetFunding=function() return false end
assert(T.Run('snapshot')); assert(T.kit.snapshots[T.kit.next_snapshot].funding==false)
UIColony.funds.GetFunding=funding_method
''')
case("watch registers disarmed P3 trigger; selection change never retargets; auto-cleanup", r'''
local watched=SelectedObj
real(function() assert(T.Run('watch_field','counter')); assert(T.Arm('watch_selected_field')) end)
assert(T.armed.watch_selected_field.state.object==watched)
SelectedObj={class='Other',handle=10,counter=100}; tick()
watched.counter=1; tick()
assert(T.fires.watch_selected_field==1 and T.armed.watch_selected_field)
assert(T.armed.watch_selected_field.state.object==watched)
emit('ChangeMap'); assert(not T.armed.watch_selected_field)
''')
case("force console uses existing arm only and refuses missing arm", r'''
real(function() assert(T.Run('console_open')) end); assert(console_requests==1)
ConsoleEnabled=false; real(function() assert(not T.Run('console_open')) end)
assert(console_requests==1); ConsoleEnabled=true
''')
case("page callbacks queue actual Run/Arm in real-time with one primary result", r'''
host=XWindow:new({}); T.pages.Saves.build(host)
local from=#logs+1; local b=findbutton(host,'Save A'); assert(b)
b:OnPress(); assert(count('SAVE','save_A',from)==0); settle()
assert(count('SAVE','save_A',from)==1)
host.window_state='destroying'
kit_host=XWindow:new({}); T.pages.Kit.build(kit_host); step('real')
assert(findbutton(kit_host,'RunAll').enabled==false)
local console=findbutton(kit_host,'Console'); from=#logs+1; console:OnPress()
assert(count('CONSOLE','console_open',from)==0); step('real')
assert(count('CONSOLE','console_open',from)==1); kit_host.window_state='destroying'
''')
case("synthetic taint is asserted after real save action completes", r'''
local from=#logs+1; taint=true
real(function() assert(T.Run('save_A')) end); settle(); taint=false
assert(count('TAINT','save_A',from)==1 and not T.saves.busy)
''')
print("P4 DESK: 17 falsifiers PASS; fake natives/UI, no save/load or rendering play claim")
