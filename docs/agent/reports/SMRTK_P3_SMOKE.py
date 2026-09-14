"""Deterministic P3 behavior falsifier; mock engine services, never play proof."""
from pathlib import Path
import re
import subprocess
import sys
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
sys.path.insert(0, str(ROOT))
from tools.parsecheck import runtime  # noqa: E402

parse, version = runtime()
assert parse is not None, version
for name in ("74_SMRTK_Agent.lua", "80_AgentSlots.lua"):
    source = (KIT / "Code" / name).read_text(encoding="utf-8-sig")
    error = parse(source, "@Code/" + name)
    assert error is None, error
    print(f"PARSE Code/{name}: 0 errors [{version}]")
    for gate, pattern in (("NO SYNC", r"NetSyncEvent|LogCheatUsed"), ("NO BARE PRINT", r"^\s*print\(")):
        hits = sum(bool(re.search(pattern, line)) for line in source.splitlines())
        print(f"{gate} Code/{name}: {hits} lines")
        assert hits == 0
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
hooks, file_log, threads = {}, {}, {}
OnMsg = setmetatable({}, {__newindex=function(_, name, fn)
  hooks[name]=hooks[name] or {}; table.insert(hooks[name], fn)
end})
function emit(name, ...) for _,fn in ipairs(hooks[name] or {}) do fn(...) end end
clock, taint, flushes, active_thread = 42, false, 0, false
function GameTime() return clock end
function AreCheatsUsed() return taint end
function FlushLogFile() flushes=flushes+1 end
function ModLog(line) file_log[#file_log+1]=string.format(line) end
function ConsolePrint(line) emit('ConsoleLine',line,true) end
function IsValid(o) return type(o)=='table' and not o.deleted end
function CurrentThread() return active_thread end
local function create_thread(kind, fn, ...)
  local args=table.pack(...)
  local thread={kind=kind, co=coroutine.create(function() fn(table.unpack(args,1,args.n)) end)}
  threads[#threads+1]=thread
  return thread
end
function CreateRealTimeThread(fn,...) return create_thread('real',fn,...) end
function CreateGameTimeThread(fn,...) return create_thread('game',fn,...) end
function IsValidThread(t) return t and not t.cancelled and coroutine.status(t.co)~='dead' end
function DeleteThread(t) t.cancelled=true end
function Sleep(ms) return coroutine.yield(ms or 0) end
function step(kind)
  local todo={}; for _,t in ipairs(threads) do todo[#todo+1]=t end
  for _,t in ipairs(todo) do
    if t.kind==kind and IsValidThread(t) then
      active_thread=t
      local ok,why=coroutine.resume(t.co)
      active_thread=false
      assert(ok,why)
    end
  end
end
function tick() clock=clock+1000; step('game'); step('real') end
function SetGameSpeed(speed) game_speed=speed end
function PlayFX(...) sounds=(sounds or 0)+1 end
function CopyToClipboard(value) clipboard=value end
function SaveLocalStorage() end
function cls() end
LocalStorage={}
UIColony={day=10}
SelectedObj={class='Depot',handle=7,command='Idle',counter=0,flags={one=true}}
cursor={class='Cursor',handle=1}
function GetTerrainCursor() return cursor end
function SelectionMouseObj() return SelectedObj end
function RGBA(r,g,b,a) return r..','..g..','..b..','..a end
function RGB(r,g,b) return RGBA(r,g,b,255) end
function box(...) return {...} end
function point(x,y) return {x=function() return x end,y=function() return y end} end
local window={}
function window:new(props,parent)
  props=props or {}; props.window_state='new'; props.parent=parent
  setmetatable(props,{__index=self}); if parent then parent[#parent+1]=props end
  return props
end
function window:SetText(text) self.Text=text end
function window:GetText() return self.Text or '' end
function window:SetBackground(color) self.Background=color end
function window:Open() self.window_state='open'; for _,child in ipairs(self) do child:Open() end end
function window:delete()
  self.window_state='destroying'
  if self.parent then for i,v in ipairs(self.parent) do if v==self then table.remove(self.parent,i); break end end end
end
function window:CreateThread(name,fn) self[name]=fn end
XWindow=window; XText=window; XButton=window; XTextEditor=setmetatable({},{__index=window})
function XTextEditor.OnShortcut(self,key) self.last_key=key; return 'native' end
XScrollArea=window; XDialog=window
TerminalTarget=setmetatable({},{__index=window})
world={}
terminal={targets={},desktop={modal_window={GetMouseTarget=function() return world end}}}
function terminal.AddTarget(target) terminal.targets[#terminal.targets+1]=target end
function terminal.RemoveTarget(target) for i,v in ipairs(terminal.targets) do if v==target then table.remove(terminal.targets,i); break end end end
function GetInGameInterfaceModeDlg() return world end
function GetInGameInterface() return world end
function click(button) assert(#terminal.targets==1); return terminal.targets[1]:OnMouseButtonDown({},button or 'L') end
function GenerateScreenshotFilename(prefix,folder)
  generated=(generated or 0)+1
  return folder..prefix..string.format('%04d',generated)..'.png'
end
function WriteScreenshot(path,ui)
  assert(CurrentThread() and CurrentThread().kind=='real','screenshot requires real-time thread')
  captures=captures or {}; captures[#captures+1]=path
  if fail_capture or (fail_preferred and path:sub(1,2)=='C:') then return 'native write denied' end
  if yield_capture then Sleep(1) end
  return nil
end
function count(verb,action,from)
  local n=0
  for i=(from or 1),#file_log do
    local line=file_log[i]
    if line:find('SMRTK_'..verb..' ',1,true) and (not action or line:find('action='..action..' ',1,true)) then n=n+1 end
  end
  return n
end
function real(fn) CreateRealTimeThread(fn); step('real') end
function check(ok,message) assert(ok,message) end
''')
for name in ("70_SMRTK_Core.lua", "71_SMRTK_Panel.lua", "74_SMRTK_Agent.lua", "80_AgentSlots.lua"):
    lua.execute((KIT / "Code" / name).read_text(encoding="utf-8-sig"))


def case(name, code):
    lua.execute(code)
    print("PASS " + name)


case("template idle and original dispatch identity", r'''
T=SMRTK
assert(T.ArmedCount()==0 and next(T.slots)==nil and #terminal.targets==0)
original_run,original_arm,original_disarm,original_fire=T.Run,T.Arm,T.Disarm,T.Fire
assert(next(T.triggers) and T.pages.Agent.build)
''')
case("slots context, scratch, legacy binding, refused armed rebind", r'''
assert(T.Run('pin_A')); assert(T.pins.A==SelectedObj)
assert(T.Bind(1,'once',function(ctx)
  assert(ctx.sel==SelectedObj and ctx.pin.A==SelectedObj and ctx.cursor==cursor)
  assert(ctx.mark==T.Mark and ctx.log==T.Log); return {object=ctx.sel}
end,{mode='once'}))
local start=#file_log+1
assert(T.Run('slot_1')); assert(count('ACTION','slot_1',start)==1)
assert(T.BindScratch('scratch',function() return {ready=true} end,{mode='once'})); assert(T.Run('slot_scratch'))
assert(not T.Bind(7,'bad',function() end))
assert(T.Bind(6,'legacy',function(ctx) return {phase=ctx.phase} end,{arm=function() end,disarm=function() end}))
assert(T.Arm('slot_6')); assert(not T.Bind(6,'overwrite',function() end)); assert(T.Disarm('slot_6'))
assert(T.Run==original_run and T.Arm==original_arm and T.Disarm==original_disarm and T.Fire==original_fire)
''')
case("exclusive click, delayed actual dispatch, stale click cancellation", r'''
mutations,cleanups=0,0
local opts={mode='armed',on_click=function(ctx,pos,obj)
  assert(CurrentThread().kind=='real'); assert(pos==cursor and obj==SelectedObj and ctx.cursor==pos)
  mutations=mutations+1; return {mutation=mutations}
end,on_disarm=function() cleanups=cleanups+1 end}
assert(T.Bind(2,'click',function(ctx) ctx.state.ready=true end,opts))
assert(T.Bind(3,'rival',function() error('must not run') end,opts))
assert(T.Arm('slot_2')); assert(#terminal.targets==1)
assert(not T.Arm('slot_3')); assert(not T.armed.slot_3 and T.armed.slot_2)
local start=#file_log+1
click(); assert(mutations==0 and count('FIRE','slot_2',start)==0)
step('real'); assert(mutations==1 and count('FIRE','slot_2',start)==1)
click(); emit('SaveGameStart'); assert(T.ArmedCount()==0 and #terminal.targets==0)
assert(T.Arm('slot_2')); step('real'); assert(mutations==1)
click('R'); assert(T.ArmedCount()==0 and #terminal.targets==0 and cleanups==2)
''')
case("partial arm cleanup and click error fail closed", r'''
local restored=0
assert(T.Bind(3,'partial',function() error('setup failed') end,{mode='armed',
on_click=function() end,on_disarm=function() restored=restored+1 end}))
assert(not T.Arm('slot_3')); assert(restored==1 and not T.armed.slot_3 and #terminal.targets==0)
assert(T.Bind(3,'bad click',function() end,{mode='armed',on_click=function() error('mutation failed') end}))
assert(T.Arm('slot_3')); click(); step('real'); assert(not T.armed.slot_3 and #terminal.targets==0)
''')
case("every lifecycle disarms triggers and slots, deleting poll threads", r'''
for _,message in ipairs({'SaveGameStart','SavegameSaved','PreLoadGame','LoadGame','ChangeMap','CurrentMapChange','DoneGame'}) do
  assert(T.Arm('slot_2')); assert(T.Arm('trigger_sol',30))
  step('game'); emit(message)
  assert(T.ArmedCount()==0 and #terminal.targets==0,message)
  local first=#file_log+1; UIColony.day=50; tick()
  assert(count('TRIGGER',nil,first)==0,'late trigger after '..message)
end
assert(next(T.pins)==nil)
''')
case("once trigger, repeat edges, action ownership, predicate failure", r'''
level=false
assert(T.Trigger{id='edge',when=function() return level end,once=false,['do']={}})
assert(not T.Trigger{id='note',when=function() end})
assert(T.Arm('edge')); step('game'); tick(); local first=#file_log+1
level=true; tick(); tick(); assert(count('TRIGGER','edge',first)==1)
level=false; tick(); level=true; tick(); assert(count('TRIGGER','edge',first)==2)
assert(not T.Run('edge')); assert(T.Disarm('edge'))
assert(T.Trigger{id='one',when=function() return true end,['do']={}})
assert(T.Arm('one')); step('game'); tick(); assert(T.fires.one==1 and not T.armed.one)
assert(T.Trigger{id='bad',when=function() error('predicate failure') end,['do']={}})
assert(T.Arm('bad')); step('game'); first=#file_log+1; tick(); tick()
assert(count('TRIGGER','bad',first)==1 and not T.armed.bad)
''')
case("scalar watch nil, false, adjacent changes, table refusal, invalid object", r'''
watched={class='Rocket',handle=9,value=nil}
assert(T.TriggerField('watch',watched,'value',{once=false,['do']={}}))
assert(T.Arm('watch')); step('game'); tick(); local first=#file_log+1
watched.value=false; tick(); watched.value=0; tick(); watched.value=nil; tick()
assert(count('TRIGGER','watch',first)==3)
watched.deleted=true; tick(); assert(not T.armed.watch)
assert(T.TriggerField('table_watch',SelectedObj,'flags',{['do']={}}))
assert(not T.Arm('table_watch') and not T.armed.table_watch)
''')
case("mark-relative error and post-arm rocket builtins", r'''
T.Mark('baseline'); assert(T.Arm('trigger_error')); step('game'); tick()
assert(T.armed.trigger_error); T.OnLuaError('injected','desk'); tick()
assert(not T.armed.trigger_error and T.fires.trigger_error==1 and game_speed==0)
assert(T.Arm('trigger_rocket')); step('game'); tick(); assert(T.armed.trigger_rocket)
emit('RocketLanded',SelectedObj); tick(); assert(not T.armed.trigger_rocket and T.fires.trigger_rocket==1)
''')
case("screenshot native return, fallback, failure and single MARK result", r'''
local first=#file_log+1
real(function() local ok,res=T.Run('screenshot_mark'); assert(ok and res.path:sub(1,2)=='C:' and res.capture_id and res.mark==T.mark_index) end)
assert(count('MARK','screenshot_mark',first)==1 and count('MARK','mark',first)==0)
fail_preferred=true
real(function() local ok,res=T.Run('screenshot_mark'); assert(ok and res.path:sub(1,8)=='AppData/' and res.fallback) end)
fail_capture=true
real(function() local ok,res=T.Run('screenshot_mark'); assert(not ok and res.reason:find('screenshot failed',1,true)) end)
fail_preferred,fail_capture=false,false
''')
case("trigger screenshot executes in real-time thread, then one trigger result", r'''
assert(T.Trigger{id='photo',when=function() return true end,['do']={screenshot=true,pause=true}})
assert(T.Arm('photo')); step('game'); local first=#file_log+1; tick()
assert(not T.armed.photo and count('TRIGGER','photo',first)==1)
local found=false
for i=first,#file_log do if file_log[i]:find('SMRTK_TRIGGER action=photo',1,true) then
  assert(file_log[i]:find('status=OK',1,true),file_log[i]); found=true
end end
assert(found)
''')
case("queued trigger cancellation and screenshot completion after lifecycle disarm", r'''
assert(T.Trigger{id='queued',when=function() return true end,['do']={pause=true}})
assert(T.Arm('queued')); step('game'); step('game')
local first=#file_log+1; emit('SaveGameStart'); step('real')
assert(count('TRIGGER','queued',first)==0 and not T.armed.queued)
yield_capture=true; game_speed=1
assert(T.Trigger{id='delayed',when=function() return true end,['do']={screenshot=true,pause=true}})
assert(T.Arm('delayed')); step('game'); step('game'); step('real')
local mark=T.mark_index; first=#file_log+1
emit('PreLoadGame'); step('real')
assert(T.mark_index==mark and game_speed==1 and not T.armed.delayed)
assert(count('TRIGGER','delayed',first)==1 and count('MARK','screenshot_mark',first)==1)
for i=first,#file_log do if file_log[i]:find('action=delayed ',1,true) and file_log[i]:find('SMRTK_TRIGGER ',1,true) then
  assert(file_log[i]:find('status=REFUSED',1,true))
end end
yield_capture=false
''')
case("Agent UI note Enter, native shortcut forwarding, seven slots and live registry", r'''
local host=XWindow:new({}); T.pages.Agent.build(host); host:Open()
local notes,slot_buttons,photo_button={},0,false
local function walk(win)
  if win.Hint=='Note; Enter records it' then notes[#notes+1]=win end
  if win.caption then
    local text=win.caption:GetText()
    if text:match('^Slot ') or text:match('^Scratch:') then slot_buttons=slot_buttons+1 end
    if text=='Screenshot + Mark' then photo_button=win end
  end
  for _,child in ipairs(win) do walk(child) end
end
walk(host); assert(slot_buttons==7 and #notes==1 and photo_button)
local note=notes[1]; note:SetText('owner note 100%')
local first=#file_log+1
assert(note:OnShortcut('Enter')=='break' and note:GetText()=='')
assert(count('NOTE','note',first)==1)
note:SetText('   '); note:OnShortcut('Enter'); assert(note:GetText()=='   ')
assert(note:OnShortcut('Left')=='native')
assert(T.Trigger{id='late_registry',label='Late registry',when=function() return false end,['do']={}})
local refresh=coroutine.create(host.SMRTKAgentRefresh); assert(coroutine.resume(refresh))
local late=false
local function find(win) if win.caption and win.caption:GetText():find('Late registry',1,true) then late=true end
  for _,child in ipairs(win) do find(child) end
end
find(host); assert(late)
first=#file_log+1; photo_button:OnPress(); assert(count('MARK','screenshot_mark',first)==0)
step('real'); assert(count('MARK','screenshot_mark',first)==1)
''')
case("post-action taint and non-unwinding error remain visible", r'''
assert(T.Bind(5,'taint control',function() taint=true end,{mode='once'}))
local first=#file_log+1; assert(T.Run('slot_5')); assert(count('TAINT',nil,first)==1); taint=false
assert(T.Bind(5,'non-unwinding control',function() T.OnLuaError('control','desk'); return {looks_ok=true} end,{mode='once'}))
local ok,res=T.Run('slot_5'); assert(not ok and res.status=='ERROR')
assert(T.ArmedCount()==0 and #terminal.targets==0 and flushes==#file_log)
''')
print("P3 DESK: PASS (mock services; no rendering, timing, disk-write or game claim)")
print("HEAD pack=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
print("HEAD testkit=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=KIT, text=True).strip())
