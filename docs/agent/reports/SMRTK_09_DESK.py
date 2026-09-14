"""09 regression fixtures. Engine doubles; no rendering, taint or play verdict."""
from pathlib import Path
import runpy
import subprocess
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / 'SMR-BugFixPack-TestKit'
print('HEAD pack=' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
      + ' kit=' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=KIT,text=True).strip())
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
OnMsg={}; logs={}; SMRTK={actions={},armed={},fires={},triggers={},after_record={}}
function SMRTK.Action(d) SMRTK.actions[d.id]=d end
function SMRTK.Page() end
function rawget_global(n) return _G[n] end
function CurrentThread() return true end
function IsValid(o) return type(o)=='table' and not o.deleted end
function IsKindOf(o,c) return IsValid(o) and (o.class==c or o[c]) end
function IsValidThread(t) return t and t.valid end
function IsThreadInside(t,n) return t.inside==n end
function GameTime() return 1000 end
function Wakeup(t) t.woken=true end
function RGBA(...) return 0 end
const={DefaultTimeFactor=1000,MaxSaneTimeFactor=128000,
 GameSpeeds={normal=1,medium=3,fast=5,fastest=20}}
CurrentMap={}; UICity={labels={Colonist={}}}; UIColony={day=10}
Cities={UICity}; MainCity={GetMap=function() return CurrentMap end}
function CheatSpawnNColonists(n,a,b) pending_spawn={n=n,age=a,backstory=b} end
function CheatCompleteAllConstructions() end
function CheatCompleteAllWiresAndPipes() end
function GetTimeFactor() return factor or 1000 end
function SetGameSpeed(n) factor=n*1000 end
function GetGameSpeed() return 'normal' end
function AllMapsForEach(_,c,fn) for _,o in ipairs(buildings or {}) do fn(o) end end
''')
lua.execute((KIT/'Code/72_SMRTK_World.lua').read_text(encoding='utf-8-sig'))
lua.execute('''
local A=SMRTK.actions
for _,kind in ipairs({'colonists','children','martian_colonists','martian_children'}) do
 for _,n in ipairs({1,10,100}) do
  local f=A['spawn_'..kind..'_'..n].run({})
  assert(type(f)=='table' and f.outcome=='spawn_dispatched' and f.after_same_tick==0)
  assert(pending_spawn.n==n)
 end
end
assert(A.spawn_colonists.run({},1.5)==false)
buildings={{mal=true,accumulated_maintenance_points=5,
 IsMalfunctioned=function(o) return o.mal end,
 CheatCleanAndFix=function(o) o.mal=false; o.accumulated_maintenance_points=0 end}}
assert(A.fix_all.run({}).changed==1)
assert(A.fix_all.run({}).changed==0)
for _,id in ipairs({'speed_normal','speed_medium','speed_fast','speed_fastest','speed_ultra'}) do
 local f=A[id].run({}); assert(f.factor==f.requested*1000)
end
local flight={valid=true,inside='SleepFlight'}
local rocket={class='UniversalRocketBase',command='CmdFlyToLocation',command_thread=flight,
 arrival_time=6000,arrival_loc={spot_type='our_colony'},
 AddFlightTime=function(o,n) o.arrival_time=o.arrival_time+n end}
local pod={class='UniversalSupplyPod',command='CmdFlyToLocation',command_thread=flight,
 arrival_time=6000,arrival_loc={spot_type='our_colony'}}
UICity.labels.UniversalRocketBase={rocket,pod}; Cities[2]=UICity
SelectedObj=nil
local f=A.rocket_arrive.run({}); assert(f.changed==1 and f.visited==2 and flight.woken)
assert(rocket.arrival_time==1000 and f.outcome=='inbound_transit_skip_requested')
rocket.arrival_time=6000; rocket.arrival_loc.spot_type='earth'
assert(A.rocket_arrive.run({}).changed==0)
rocket.arrival_loc.spot_type='our_colony'; rocket.is_paused=true
assert(A.rocket_arrive.run({}).changed==0)
meteor_args=nil
function MeteorsDisaster(...) meteor_args=table.pack(...) end
Presets={MapSettings={Meteor={low={id='low'}}}}
for _,k in ipairs({'single','scattered_single'}) do
 local state={setting='low'}
 local f=A['meteor_'..k].run({phase='fire',state=state},{owner=state,pos='CURSOR'})
 assert(type(f)=='table' and meteor_args[3]=='CURSOR')
 assert(meteor_args[4]==(k=='single') and meteor_args[2]=='single')
end
''')
print('PASS: 12 deferred spawn variants, pre-mutation refusal, repair idempotence, five speeds, world rocket dedup/class/direction/pause, exact/scattered meteor arguments')

# ⛔ STAMPER CUT 2026-09-14 (owner ruling; TestKit d80fb5e). The P5 capture and
# partial-stamp legs that stood here tested `77_SMRTK_Stamper.lua`, which no longer
# exists — they loaded SMRTK_P5_DESK.py and crashed this whole instrument on import.
# Excised so the remaining legs run. What they asserted is preserved in
# SMRTK_09_REBUILD.md; the design is parked in docs/FUTURE_IDEAS.md entry 5.
# Grave: git show 81d97eb~1:docs/agent/reports/SMRTK_09_DESK.py

# Re-use only P2's window constructor doubles, not its obsolete menu assertions.
import re
init=(ROOT/'docs/agent/reports/SMRTK_P2_SMOKE.py').read_text(encoding='utf-8-sig')
ui=LuaRuntime(unpack_returned_tuples=True)
ui.execute(re.search(r"lua.execute\(r'''(.*?)'''\)",init,re.S).group(1))
ui.execute('''
TextStyles={}; function PlaceObj(c,p) return p end
function RGB(...) return 0 end
function Untranslated(s) return s end
local W=getmetatable(XWindow:new({})).__index
function W:SetEnabled(v) self.enabled=v; for _,c in ipairs(self) do c:SetEnabled(v) end end
function W:SetFoldWhenHidden(v) self.FoldWhenHidden=v end
function W:SetRolloverText(v) self.RolloverText=v end
function W:SetTextColor(v) self.TextColor=v end
function W:GetText() return self.Text or '' end
function W:GetValue() return self.value or self.DefaultValue end
function W:SetValue(v) self.value=v end
function W:SetItems(v) self.Items=v end
XCombo=XWindow; XTextEditor=XWindow
LuaRevision=24995074
function RealTime() return 12345 end
function GetPreciseTicks() return 12345 end
function AsyncRand() return 12345 end
CurrentMap={}; UICity={labels={}}; UIColony={day=10}
const={DefaultTimeFactor=1000,MaxSaneTimeFactor=128000,
 GameSpeeds={normal=1,medium=3,fast=5,fastest=20}}
Presets={MapSettings={}}; TraitPresets={}
function PresetsCombo() return function() return {} end end
SMRTest={order={'probe1'},last={},probes={},Log={}}
function CurrentThread() return true end
function CreateGameTimeThread(fn) return {fn=fn,valid=true} end
function GetGameSpeed() return 'normal' end
function GetTimeFactor() return 1000 end
function SetGameSpeed() end
function PlayFX() end
function IsRealTimeThread() return true end
''')
for name in ('70_SMRTK_Core.lua','71_SMRTK_Panel.lua','72_SMRTK_World.lua',
             '73_SMRTK_Infopanel.lua','74_SMRTK_Agent.lua','75_SMRTK_Saves.lua',
             '76_SMRTK_Kit.lua'):
    ui.execute((KIT/'Code'/name).read_text(encoding='utf-8-sig'))
ui.execute('''
local T=SMRTK
local function tick(w,id)
 local f=assert(w.threads[id]); local co=coroutine.create(f)
 local saved=Sleep; Sleep=function() coroutine.yield() end
 local ok,err=coroutine.resume(co); Sleep=saved; assert(ok,err)
end
local function find(w,text)
 for _,c in ipairs(w) do
  if c.caption and c.caption.Text==text then return c end
  local f=find(c,text); if f then return f end
 end
end
hud=HUDClass:new({IdNode=true,LayoutMethod='Box'},interface)
local overlay=XWindow:new({IdNode=false,LayoutMethod='Box'},hud)
local bottom=XWindow:new({Id='idBottom'},overlay)
local middle=XWindow:new({Id='idMiddle'},overlay)
local list=XWindow:new({Id='idMiddleList',LayoutMethod='HList'},middle)
local vanilla=XWindow:new({},list)
assert(T.Run('dock_attach',hud))
-- Owner ruling 2026-09-14: the right-corner Box sibling is the PRIMARY route and
-- the chip is a wide status bar. The HList beside the game's dock is the fallback,
-- so the vanilla row must be left untouched here.
assert(T.dock.parent==bottom.parent and #list==1 and list[1]==vanilla and #bottom==0)
assert(T.dock.MinHeight==30 and T.dock.smrtk_wide and not T.actions.dock_menu)
local count=#records; local ok_again,f_again=T.Run('dock_attach',hud)
assert(ok_again and f_again.attached==false and #list==1)
local dock=T.dock
dock:OnPress(); run_queued(); assert(T.panel:GetVisible())
dock:OnPress(); run_queued(); assert(not T.panel:GetVisible())
assert(T.TogglePanel())
assert(T.actions.run_until.page=='Run' and T.actions.trigger_sol.page=='Run')
assert(T.actions.watch_field.page=='Selected' and T.actions.dump_selected.page=='Selected')
for _,id in ipairs(T.page_order) do
 assert(T.Run('tab_'..id))
 if id=='Agent' then tick(T.panel.page_host,'SMRTKAgentRefresh') end
 if id=='Run' then tick(T.panel.page_host,'SMRTKRunRefresh') end
 if id=='Kit' then tick(T.panel.page_host,'SMRTKKitReadout') end
end
assert(T.Run('tab_Kit'))
tick(T.panel.page_host,'SMRTKKitReadout')
local all=find(T.panel.page_controls,'Run all probes')
assert(all and all.enabled==false and all.DisabledBackground~=nil and all.caption.enabled==false)
local evidence=#T.ring
find(T.panel.page_controls,'Clear log readout'):OnPress()
assert(#T.ring==evidence+1 and T.readout_start>T.ring[#T.ring].n)
T.armed.slot_4={state={}}; T.actions.slot_4={label='Read map click'}
T.click_capture={id='slot_4',target={}}
T.RefreshDock(); T.RefreshPanel()
assert(T.click_notice.visible and T.click_notice.Text:find('slot_4',1,true)
 and T.click_notice.Text:find('right-click',1,true))
T.click_capture=nil; T.armed.slot_4=nil; T.RefreshDock()
assert(not T.click_notice.visible)
-- Missing Box route falls back to the native HList beside the game's dock, where
-- there is no room for the status bar, so the chip stays the compact 52 square.
emit('DoneGame')
overlay.LayoutMethod='VList'
local ok,f=T.Run('dock_attach',hud)
assert(ok and f.route=='HUDMiddle/idMiddleList' and T.dock.parent==list)
assert(T.dock.MinHeight==52 and not T.dock.smrtk_wide and #bottom==0)
overlay.LayoutMethod='Box'
emit('DoneGame')
assert(T.dock==nil and T.panel==nil and T.click_notice==nil and T.ArmedCount()==0)
-- Trigger record reacts even after the trigger itself has paused game time.
local active={state={target='trigger_sol'}}; T.armed.run_until=active
local fired,disarmed=false,false
local original_fire,original_disarm=T.Fire,T.Disarm
T.Fire=function(id,event) assert(id=='run_until' and event.owner==active.state); fired=true end
T.Disarm=function(id) assert(id=='run_until'); disarmed=true; T.armed[id]=nil end
T.after_record.TRIGGER({action='trigger_sol'})
assert(fired and disarmed)
T.Fire,T.Disarm=original_fire,original_disarm
''')
print('PASS: all seven page constructors, HUD HList and sibling fallback, dock toggle/idempotence, disabled captions, readout clear retains evidence, armed banner, teardown, paused-trigger coordination')

src=Path('A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src')
names=set()
for p in src.rglob('*.lua'):
    names.update(re.findall(r'^function\s+[\w.]+:((?:AsyncCheat|Cheat)\w*)\s*\(',p.read_text(encoding='utf-8-sig'),re.M))
names.update('CheatUpgrade'+str(i) for i in range(1,7))
ui.globals().source_names=ui.table_from(sorted(names))
ui.execute('''
local T=SMRTK
g_Classes={Deposit={CheatRefill=function() end},SupplyPodBase={CheatRefuel=function() end}}
local methods={}
local leaf_calls=0
for _,name in ipairs(source_names) do methods[name]=function() leaf_calls=leaf_calls+1 end end
local obj=setmetatable({class='SourceUnion',handle=900},{__index=methods})
SelectedObj=obj
local rows=T.SelectedActions(obj); local more,async,caveats=0,0,0
for _,r in ipairs(rows) do
 if r.id=='selected_more' then
  more=more+1; async=async+(r.async and 1 or 0)
  assert(r.rollover and r.rollover:find('SOURCE-derived',1,true))
  caveats=caveats+(r.disposition=='needs-rollover' and 1 or 0)
 end
end
assert(more==77 and async==10 and caveats==59)
for _,name in ipairs({'AsyncCheatDebugger','AsyncCheatScreenshot','CheatBreakTrack','CheatMeteorHit',
 'CheatPrintRequests','CheatSpawnLinkedUndergroundPassage','CheatTransformUnderground'}) do
 local before=leaf_calls; local ok,f=T.Run('selected_more',obj,name)
 assert(not ok and f.status=='REFUSED' and leaf_calls==before)
end
methods.CheatRefill=g_Classes.Deposit.CheatRefill
methods.CheatRefuel=g_Classes.SupplyPodBase.CheatRefuel
local ok=T.Run('selected_more',obj,'CheatRefill'); assert(not ok)
local ok=T.Run('selected_more',obj,'CheatRefuel'); assert(not ok)
obj.CheatRefill=function() leaf_calls=leaf_calls+1 end
obj.CheatRefuel=function() leaf_calls=leaf_calls+1 end
local before=leaf_calls
assert(T.Run('selected_more',obj,'CheatRefill'))
assert(T.Run('selected_more',obj,'CheatRefuel'))
assert(leaf_calls==before+2)
-- Expanded MultiResource runtime list is read through the common StorageDepot.
local depot={class='UniversalIngredientsDepot',handle=901,kinds={StorageDepot=true,MultiResourceDepotBase=true},
 storable_resources={'Grain','Leaf'},stored=5,
 GetStoredAmount=function(o,r) return o.stored end,CheatFill=function(o) o.stored=20 end}
SelectedObj=depot
local ok,f=T.Run('selected_fill',depot)
assert(ok and f.before==10 and f.after==40 and f.resources==2)
''')
print('PASS: filtered source-union inventory 77 More / 10 async / 59 named caveats, seven cuts cannot dispatch, receiver no-op omission preserves overrides, sibling depot amounts')

import hashlib
files=[*sorted((KIT/'Code').glob('7*_SMRTK*.lua')),KIT/'Code/80_AgentSlots.lua']
for title,pattern,want in [('NO SYNC',r'NetSyncEvent|LogCheatUsed',0),
                           ('NO BARE PRINT',r'^\s*print\(',0),
                           ('ONE LOGGER',r'^function T\.Log\(',1),
                           ('ONE TAG SINK',r'\[SMRTK\] SMRTK_',1)]:
    hits=[(p.name,i) for p in files for i,l in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1) if re.search(pattern,l)]
    print(title,len(hits),hits); assert len(hits)==want
presence=(src/'Data/CheatDef.lua').read_text(encoding='utf-8-sig').splitlines()
print('PRESENCE',sum(bool(re.search(r'NetSyncEvent|LogCheatUsed',l)) for l in presence),'lines')
print('SOURCE FILES',len(files))
for p in files: print(p.name,hashlib.sha256(p.read_bytes()).hexdigest())
print('PLAY: NOT RUN')
