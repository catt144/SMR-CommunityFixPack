"""World behavior falsifier with cooperative engine doubles; never play proof."""
from pathlib import Path
import argparse
import re
import subprocess
import sys
from lupa import LuaRuntime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
args = argparse.ArgumentParser()
args.add_argument("--mutant", choices=("quiet", "stale-click"))
args.add_argument("--selftest", action="store_true")
args.add_argument("--list", action="store_true")
options = args.parse_args()

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
source = (KIT / "Code/72_SMRTK_World.lua").read_text(encoding="utf-8-sig")
if options.mutant == "quiet":
    source = source.replace("and predicate(...) then", "and false then")
elif options.mutant == "stale-click":
    source = source.replace("if not active or active.state ~= state or state.cancelled then return end", "if false then return end")
    source = source.replace("event.owner ~= ctx.state or ctx.state.cancelled", "false")
lua = LuaRuntime(unpack_returned_tuples=True)
loader = lua.eval("function(s) local f,e=load(s); return f~=nil,e end")
ok, error = loader(source)
assert ok, error
print("PARSE Code/72_SMRTK_World.lua: 0 errors [" + lua.eval("_VERSION") + "]")
for name, pattern in (("NO SYNC", r"NetSyncEvent|LogCheatUsed"), ("NO BARE PRINT", r"^\s*print\(")):
    count = sum(bool(re.search(pattern, line)) for line in source.splitlines())
    print(f"{name} Code/72_SMRTK_World.lua: {count} lines")
    assert count == 0

lua.execute(r'''
hooks, logs, threads, leaves, wrapped_calls = {}, {}, {}, {}, {}
OnMsg=setmetatable({}, {__newindex=function(_,name,fn) hooks[name]=hooks[name] or {}; table.insert(hooks[name],fn) end})
function emit(name,...) for _,fn in ipairs(hooks[name] or {}) do fn(...) end end
clock,taint,active_thread=10000,false,false
function GameTime() return clock end
function AreCheatsUsed() return taint end
function ModLog(s) logs[#logs+1]=string.format(s) end
function ConsolePrint(s) emit('ConsoleLine',s,true) end
function FlushLogFile() end
function IsValid(o) return type(o)=='table' and not o.deleted end
function IsKindOf(o,k) return IsValid(o) and (o.class==k or o[k]==true) end
function CurrentThread() return active_thread end
function create(kind,fn,...)
 local args=table.pack(...); local t={kind=kind}
 t.co=coroutine.create(function() fn(table.unpack(args,1,args.n)) end)
 threads[#threads+1]=t; return t
end
function CreateRealTimeThread(fn,...) return create('real',fn,...) end
function CreateGameTimeThread(fn,...) return create('game',fn,...) end
function IsValidThread(t) return t and not t.cancelled and coroutine.status(t.co)~='dead' end
function DeleteThread(t) t.cancelled=true end
function Sleep(ms) return coroutine.yield(ms) end
function resume(t)
 if not IsValidThread(t) then return end
 active_thread=t; local ok,why=coroutine.resume(t.co); active_thread=false; assert(ok,why)
end
function step(kind)
 local copy={}; for _,t in ipairs(threads) do copy[#copy+1]=t end
 for _,t in ipairs(copy) do if t.kind==kind then resume(t) end end
end
function run(id,...)
 local args=table.pack(...); local result
 local t=create('real',function() result=table.pack(SMRTK.Run(id,table.unpack(args,1,args.n))) end)
 resume(t); return result and table.unpack(result,1,result.n),t
end
function threaded_arm(id,...)
 local args=table.pack(...); local result
 local t=create('real',function() result=table.pack(SMRTK.Arm(id,table.unpack(args,1,args.n))) end)
 resume(t); return table.unpack(result,1,result.n)
end
function PlayFX(...) cues=(cues or 0)+1 end
function GetTerrainCursor() return 'CURSOR_POINT' end
function SelectionMouseObj() end
function GetInGameInterfaceModeDlg() end
function GetInGameInterface() end
TerminalTarget={new=function(self,p) return p end}
terminal={AddTarget=function(t) terminal.target=t end,RemoveTarget=function(t) assert(terminal.target==t); terminal.target=nil end}
const={DefaultTimeFactor=1000,MaxSaneTimeFactor=128000,GameSpeeds={fast=5}}
time_factor,last_speed=1000,1
function SetGameSpeed(n)
 if n==0 then paused=true else paused=false; LastGameSpeed=n end
 time_factor=(type(GameSpeedLimit)=='number' and math.min(n,GameSpeedLimit) or n)*1000
end
function GetTimeFactor() return time_factor end
function GetGameSpeed() return paused and 'pause' or 'normal' end
UIColony={day=10,funds={funding=1000000000}}
function UIColony.funds:ChangeFunding(n) self.funding=self.funding+n end
UICity={labels={Colonist={},Dome={}}}
MainMap={name='Main'}; CurrentMap=MainMap
function GetEnvironment(map) return map.environment or 'Surface' end
SMRTest={LoggerState=function() local copy={}; for k,v in pairs(enabled_loggers or {}) do copy[k]=v end; return copy end}
Presets={MapSettings={}}
for _,g in ipairs({'DustStorm','DustDevils','ColdWave','Marsquake','Meteor','RainsDisaster'}) do Presets.MapSettings[g]={low={id='low'},high={id='high'}} end
function PresetsCombo(kind,g) return function() return {'','low','high'} end end
function leaf(name,...)
 assert(active_thread,'mutation outside thread')
 leaves[#leaves+1]={name=name,args=table.pack(...)}
end
function CheatDustStorm(...) leaf('duststorm',...) end
function CheatDustDevil(...) leaf('dustdevil',...) end
function CheatColdWave(...) leaf('coldwave',...) end
function CheatTriggerMarsquake(...) leaf('marsquake',...) end
function CheatRainsDisaster(...) leaf('rains',...) end
function CheatMeteors(...) leaf('meteor',...) end
function CheatTriggerUndergroundCaveIn(...) leaf('cavein',...) end
function CheatTriggerUndergroundMarsquake(...) leaf('ugquake',...) end
function CheatStopDisaster() stops=(stops or 0)+1 end
function CheatCompleteAllConstructions() leaf('construction') end
function CheatCompleteAllWiresAndPipes() leaf('grids') end
function CheatUnlockAllBuildings() leaf('unlock') end
function CheatAddFunding(n) assert(active_thread); UIColony.funds:ChangeFunding(n) end
function CheatSpawnNColonists(n,age,backstory)
 assert(active_thread); last_spawn={n,age,backstory}
 if spawn_failure then return end
 for i=1,n do table.insert(UICity.labels.Colonist,{}) end
end
function CheatGenerateApplicants(n) leaf('applicants',n) end
UIPlayer={TechPoints=0,GainTechPoint=function(self) self.TechPoints=self.TechPoints+1 end,UIResearch=function(self,id,force) leaf('research',id,force); return id~='known' end}
function ForEachPreset(kind,fn) for _,t in ipairs({{id='new',group='Main'},{id='known',group='Main'},{id='hidden',group='Main',LockState='hidden'},{id='other',group='Other'}}) do fn(t) end end
function TechGroupToSection(g) return g end
function ReopenXBuildMenu() end
function OpenAllDomes() leaf('open_domes') end
function CloseAllDomes() leaf('close_domes') end
function UnpinAll(force) leaf('unpin',force) end
function AllMapsForEach(_,kind,other,callback)
 if type(other)=='function' then callback=other end
 for _,o in ipairs(kind=='Building' and buildings or storages) do callback(o) end
end
buildings={{class='Building',mal=false,CheatCleanAndFix=function(self) self.mal=false end,
 DoesRequireMaintenance=function() return true end,IsMalfunctioned=function(self) return self.mal end,SetMalfunction=function(self) self.mal=true end},
 {class='Building',DoesRequireMaintenance=function() return false end}}
storages={{CheatFill=function(self) self.amount=100 end},{CheatFill=function(self) self.amount=200 end}}
TraitPresets={Genius={group='Positive'},Locked={group='Positive'},Flaw={group='Negative'}}
function IsTraitAvailable(id) return id~='Locked' end
SelectedObj={class='Colonist',handle=1,traits={},AddTrait=function(self,id) self.traits[id]=true end,RemoveTrait=function(self,id) self.traits[id]=nil end}
repeat_threads={}
function GetPeriodicRepeatThread(name,map) return repeat_threads[(map and map.name or 'global')..':'..name] end
originals={}
for _,name in ipairs({'StartDustStorm','StartColdWave','GenerateDustDevilIn','MeteorsDisaster','TriggerMarsquake','FindEpicentre','RainProcedure'}) do
 _G[name]=function(...)
  wrapped_calls[name]=(wrapped_calls[name] or 0)+1
  if pause_active_body then Sleep(1) end
  completed_calls=completed_calls or {}; completed_calls[name]=(completed_calls[name] or 0)+1
  return 'ORIGINAL_'..name
 end; originals[name]=_G[name]
end
g_RainDisaster=false
function IsThreadInside(t,name) return t and t.inside==name end
function Wakeup(t) t.woken=true end
config={RocketInstantTravel=false}
function cls() end
function CopyToClipboard() end
function SaveLocalStorage() end
LocalStorage={}
SMRTK={}
''')
lua.execute((KIT / "Code/70_SMRTK_Core.lua").read_text(encoding="utf-8-sig"))
# The frozen panel's API can be replaced by inert UI construction doubles;
# actual callbacks and core dispatch remain under test.
lua.execute(r'''
function SMRTK.Page(id,label,fn) SMRTK.page_builder=fn end
function SMRTK.Button(parent,label,id) return ui({OnPress=function() SMRTK.Run(id) end},parent) end
function ui(props,parent)
 local o=props or {}; if parent then parent[#parent+1]=o end
 function o:GetText() return self.Text end
 function o:SetText(v) self.Text=v end
 function o:GetValue() return self.value or self.DefaultValue end
 function o:SetValue(v) self.value=v end
 function o:SetItems(v) self.Items=v end
 return o
end
XText={new=function(self,p,parent) return ui(p,parent) end}
XWindow=XText; XCombo=XText
XTextEditor={new=function(self,p,parent) p.Text=''; return ui(p,parent) end}
''')
lua.execute(source)
lua.execute(r'''
T=SMRTK
assert(T.ArmedCount()==0)
for name,fn in pairs(originals) do assert(_G[name]==fn,'idle patch '..name) end
local before=#leaves
local ok,fields=T.Run('dust_storm','high')
assert(not ok and fields.reason=='invoke inside a yielding thread' and #leaves==before)
assert(run('dust_storm','high')); assert(leaves[#leaves].args[1]=='normal' and leaves[#leaves].args[2]=='high')
assert(run('dust_devil_major','high','TARGET')); assert(leaves[#leaves].args[1]=='major' and leaves[#leaves].args[3]=='TARGET')
assert(not run('cold_wave','BAD')); assert(not run('underground_cave_in','TARGET'))
CurrentMap.environment='Underground'; assert(run('underground_cave_in','TARGET')); CurrentMap.environment=nil
assert(T.Arm('meteor_single','high'))
local captured=terminal.target
captured:OnMouseButtonDown({},'L')
assert(#leaves==before+3,'click ran outside queued thread')
assert(T.Disarm('meteor_single','save'))
assert(T.Arm('meteor_single','low'))
step('real'); assert(#leaves==before+3,'stale old click mutated new arm')
terminal.target:OnMouseButtonDown({},'L'); terminal.target:OnMouseButtonDown({},'L'); step('real')
assert(leaves[#leaves].name=='meteor' and leaves[#leaves].args[2]=='low' and leaves[#leaves].args[3]=='CURSOR_POINT')
assert(not T.armed.meteor_single and not terminal.target)
enabled_loggers={Meteors=true}; assert(not T.Arm('quiet')); enabled_loggers={}
T.armed.logger_dummy={state={}}; assert(not T.Arm('quiet')); T.armed.logger_dummy=nil
active_bodies={}; pause_active_body=true
for name,fn in pairs(originals) do
 local t=create('game',fn)
 resume(t); active_bodies[#active_bodies+1]={t,name,completed_calls and completed_calls[name] or 0}
end
pause_active_body=false
assert(T.Arm('quiet'))
for name,fn in pairs(originals) do assert(_G[name]~=fn) end
for _,item in ipairs(active_bodies) do resume(item[1]); assert(completed_calls[item[2]]==item[3]+1,'quiet interrupted active body '..item[2]) end
-- Manual starts and active rain pass while quiet is armed.
assert(StartDustStorm('normal',{},MainMap,false)=='ORIGINAL_StartDustStorm')
assert(StartColdWave({})=='ORIGINAL_StartColdWave')
assert(GenerateDustDevilIn('P',MainMap,{})=='ORIGINAL_GenerateDustDevilIn')
assert(MeteorsDisaster({},'storm','P')=='ORIGINAL_MeteorsDisaster')
assert(TriggerMarsquake('Building',10,1)=='ORIGINAL_TriggerMarsquake')
assert(FindEpicentre(MainMap)=='ORIGINAL_FindEpicentre')
assert(RainProcedure({},'from cheat')=='ORIGINAL_RainProcedure')
-- Every scheduler waits before original; already running bodies stay intact.
local cases={
 {'StartDustStorm','DustStorm',MainMap,{'normal',{},MainMap,true}},
 {'StartColdWave','ColdWave',MainMap,{{}}},
 {'GenerateDustDevilIn','DustDevils',MainMap,{'P',MainMap,{}}},
 {'MeteorsDisaster','Meteors',MainMap,{{},'single'}},
 {'TriggerMarsquake','MagneticFieldMarsquake',false,{'MagneticFieldGenerator',10,1}},
 {'FindEpicentre','UndergroundMarsquake',MainMap,{MainMap}},
 {'RainProcedure','Rain',MainMap,{{},false}},
}
held={}
for _,c in ipairs(cases) do
 local n=wrapped_calls[c[1]] or 0
 local t=create('game',function() _G[c[1]](table.unpack(c[4])) end)
 repeat_threads[(c[3] and c[3].name or 'global')..':'..c[2]]=t
 resume(t); assert((wrapped_calls[c[1]] or 0)==n,'quiet failed '..c[1]); held[#held+1]={t,c[1],n}
end
assert((stops or 0)==0,'quiet stopped an active disaster')
emit('SaveGameStart')
assert(not T.armed.quiet)
for name,fn in pairs(originals) do assert(_G[name]==fn,'restore failed '..name) end
assert(T.Arm('quiet'))
for _,item in ipairs(held) do resume(item[1]); assert((wrapped_calls[item[2]] or 0)==item[3],'stale quiet waiter bypassed fresh arm') end
assert(T.Disarm('quiet','release waiters'))
for _,item in ipairs(held) do resume(item[1]); assert(wrapped_calls[item[2]]==item[3]+1) end
assert(run('speed_ultra')); assert(GetTimeFactor()==128000)
GameSpeedLimit=2; GameSpeedLimitReasons={'Disaster'}
local ok,fields=T.Run('speed_ultra'); assert(ok and fields.clamped_by=='Disaster' and GetTimeFactor()==2000)
assert(not T.Run('speed',129)); GameSpeedLimit=false
assert(threaded_arm('run_until',11)); step('game'); assert(T.armed.run_until)
UIColony.day=11; step('game'); assert(T.armed.run_until); step('real')
assert(not T.armed.run_until and GetGameSpeed()=='pause' and cues==1)
assert(threaded_arm('run_until',12)); UIColony.day=12; step('game'); T.Disarm('run_until','save'); step('real'); assert(cues==1)
T.triggers={other={}}; T.armed.other={state={}}; T.fires.other=3
assert(threaded_arm('run_until','other')); T.fires.other=4; step('game'); step('real'); assert(cues==2 and not T.armed.run_until); T.armed.other=nil
assert(run('malfunction_all')); assert(buildings[1].mal)
assert(run('fix_all')); assert(not buildings[1].mal)
assert(run('complete_constructions')); assert(run('complete_grids'))
assert(run('fill_storages')); assert(storages[1].amount==100 and storages[2].amount==200)
assert(run('spawn_colonists',10)); assert(#UICity.labels.Colonist==10)
assert(not run('spawn_colonists',1.5)); spawn_failure=true; assert(not run('spawn_colonists',1)); spawn_failure=false
local seq=T.sequence; assert(run('spawn_martian_children_100')); assert(T.sequence==seq+1 and last_spawn[2]=='Child' and last_spawn[3]=='martianborn')
assert(run('funding',-100000)); assert(UIColony.funds.funding==999900000)
assert(not run('funding','500M')); seq=T.sequence; assert(run('funding_plus')); assert(T.sequence==seq+1)
assert(run('tech_points_10')); assert(UIPlayer.TechPoints==10)
assert(run('research_all')); assert(run('unlock_buildings')); assert(run('open_domes')); assert(run('close_domes')); assert(run('unpin_all'))
assert(run('trait_add','Genius')); assert(SelectedObj.traits.Genius)
assert(not run('trait_add','Genius')); assert(not run('trait_add','Locked'))
assert(run('trait_remove','Genius')); assert(not SelectedObj.traits.Genius)
-- Modern rocket flight remains on its policy command until its own waiter completes.
local flight=create('game',function() Sleep(1000); rocket.command='CmdWaitInOrbit' end); flight.inside='SleepFlight'
rocket={class='UniversalRocketBase',handle=8,command='CmdFlyToLocation',command_thread=flight,arrival_time=clock+5000,
 arrival_loc={spot_type='our_colony'},AddFlightTime=function(self,n) self.arrival_time=self.arrival_time+n; self.bonus_sleep_time=n end}
SelectedObj=rocket; resume(flight)
local result; local action=create('real',function() result=table.pack(T.Run('rocket_arrive')) end)
resume(action); assert(flight.woken and rocket.command=='CmdFlyToLocation' and not config.RocketInstantTravel)
resume(flight); resume(action); assert(result[1] and result[2].outcome=='travel_wait_finished')
rocket.command='CmdFlyToLocation'; rocket.is_paused=true; assert(not run('rocket_arrive')); rocket.is_paused=nil
-- UI wiring creates no mutations; presses queue core dispatch in a yielding thread.
parent={}; before=#leaves; T.page_builder(parent); assert(#leaves==before)
local first=parent[2][3]; assert(first and first.OnPress); first.OnPress(); assert(#leaves==before); step('real'); assert(#leaves==before+1)
for _,id in ipairs({'SavegameSaved','SaveGameStart','PreLoadGame','LoadGame','ChangeMap','CurrentMapChange','DoneGame'}) do
 assert(T.Arm('quiet')); emit(id); assert(not T.armed.quiet)
 for name,fn in pairs(originals) do assert(_G[name]==fn,id..' leaked '..name) end
end
assert(T.Taint()==false)
''')
print("BEHAVIOR: PASS — idle identity, all 7 quiet gates/manual bypass/active preservation, logger refusal, lifecycle restoration, stale meteor clicks, speed clamps, run-until cancellation, sweeps, spawn/funding contracts, traits, rocket wait, UI thread dispatch")
print("PLAY: NOT RUN — doubles prove control flow only")
print("HEAD pack=" + subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
      + " TestKit=" + subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=KIT, text=True).strip())
if options.list:
    lines = lua.eval("function() local ids={}; for id,d in pairs(SMRTK.actions) do if d.page=='World' then ids[#ids+1]=id end end; table.sort(ids); local out={'WORLD REGISTRY: '..#ids..' actions'}; for _,id in ipairs(ids) do local d=SMRTK.actions[id]; out[#out+1]=id..' | '..d.label..' | menu='..tostring(d.menu or false) end; return table.concat(out,'\\n') end")()
    print(lines)
if options.selftest:
    for mutant in ("quiet", "stale-click"):
        result = subprocess.run([sys.executable, str(Path(__file__)), "--mutant", mutant], capture_output=True, text=True)
        expected = "quiet failed" if mutant == "quiet" else "stale old click mutated new arm"
        assert result.returncode != 0 and expected in result.stderr, mutant + " escaped falsifier"
        print("FALSIFIER " + mutant + ": RED as required")
