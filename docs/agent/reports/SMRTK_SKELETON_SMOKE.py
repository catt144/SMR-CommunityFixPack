"""Desk model, not engine proof. Run from the pack: python <this path>."""
from pathlib import Path
import sys
import re
from lupa import LuaRuntime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
lua = LuaRuntime(unpack_returned_tuples=True)
syntax = lua.eval("function(s,n) local f,e=load(s,n); return f~=nil,e end")
sitting = ROOT / "docs/agent/prompts/smrtk/02_SKELETON_SITTING_owner.md"
snippets = []
if sitting.exists():
    for block in re.findall(r"```lua\n(.*?)```", sitting.read_text(encoding="utf-8"), re.S):
        snippets.extend(line.removeprefix("*r ") for line in block.splitlines() if line.strip())
for index, snippet in enumerate(snippets, 1):
    ok, error = syntax(snippet, f"@sitting-line-{index}")
    assert ok, error
if sitting.exists():
    print(f"SITTING SYNTAX: {len(snippets)} one-line Lua commands parse (not executed)")
else:
    print("SITTING SYNTAX: not rerun; 02 has been consumed (use its git grave)")
lua.execute(r'''
hooks, file_log, threads = {}, {}, {}
OnMsg = setmetatable({}, {__newindex = function(_, name, fn)
  hooks[name] = hooks[name] or {}; table.insert(hooks[name], fn)
end})
function emit(name, ...) for _, fn in ipairs(hooks[name] or {}) do fn(...) end end
clock, flushes, native_console, taint = 42, 0, true, false
function GameTime() return clock end
function FlushLogFile() flushes = flushes + 1 end
function ModLog(s) file_log[#file_log + 1] = string.format(s) end
function ConsolePrint(s) if native_console then emit("ConsoleLine", s, true) end end
function print(...) ConsolePrint(table.concat({...}, "\t")); return "first", nil, "last" end
original_print = print
function AreCheatsUsed() return taint end
function IsValid(o) return type(o) == "table" and not o.deleted end
function CopyToClipboard(s) clipboard = s end
function cls() clears = (clears or 0) + 1 end
function CreateRealTimeThread(fn) threads[#threads + 1] = fn; return fn end
function Sleep() end
function SaveLocalStorage() saved = LocalStorage.SMRTKPanel; return true end
function run_threads() local todo = threads; threads = {}; for _, f in ipairs(todo) do f() end end
LocalStorage = {SMRTKPanel = {open=false, collapsed=false, tab="Kit", x=60, y=90}}
XShortcutsTarget = {actions = {}}
function XShortcutsTarget:ActionById(id) return self.actions[id] end
function ReloadShortcutsImmediate()
  XShortcutsTarget.actions = {}
  if ConsoleEnabled then XShortcutsTarget.actions.DE_Console = {} end
  emit("Shortcuts", XShortcutsTarget)
  emit("ShortcutsReloaded")
end
''')
core = (KIT / "Code/70_SMRTK_Core.lua").read_text(encoding="utf-8-sig")
lua.execute(core)
lua.execute(r'''
local before = #file_log
local line = SMRTK.Log("FORMAT", {value="100% ready\nnext", object={class="Depot", handle=7}})
assert(file_log[#file_log] == line and #file_log == before + 1)
assert(line:find('object=Depot(7)', 1, true) and line:find([[value="100% ready\nnext"]], 1, true))
assert(not line:find("\n", 1, true) and flushes == #file_log)
assert(SMRTK.Eligibility() == "UNAVAILABLE:sandbox")
assert(print == original_print and SMRTK.ArmedCount() == 0)

SMRTK.Mark("native")
emit("ConsoleLine", "VANILLA_100%", true)
assert(SMRTK.CopySince("native"))
assert(clipboard:find("VANILLA_100%", 1, true) and clipboard:find("source=console", 1, true))
assert(not SMRTK.CopySince("nonexistent"))
SMRTK.Mark("overflow")
for n=1,305 do emit("ConsoleLine", "line" .. n, true) end
assert(#SMRTK.ring == 300)
local ok, copy = SMRTK.CopySince("overflow")
assert(ok and copy.truncated and copy.lines == 300)

-- Native delivery absent: our own lines must not count as native proof.
native_console = false
SMRTK.Mark("fallback")
assert(SMRTK.PrintTee(true))
local a,b,c = print("TEE_100%")
assert(a == "first" and b == nil and c == "last")
assert(SMRTK.tap.print == 1 and SMRTK.fires.print_tee == 1)
assert(SMRTK.CopySince() and clipboard:find("source=print", 1, true))
emit("SavegameSaved")
assert(print == original_print and SMRTK.ArmedCount() == 0)
for _, message in ipairs({"PreLoadGame", "LoadGame", "ChangeMap", "CurrentMapChange", "DoneGame"}) do
  assert(SMRTK.PrintTee(true)); emit(message)
  assert(print == original_print and SMRTK.ArmedCount() == 0, message)
end
assert(not SMRTK.Fire("print_tee", "must not fire"))

SMRTK.Action {id="needs_object", needs="selected", run=function() taint=true end}
assert(not SMRTK.Run("needs_object") and not taint)
SMRTK.Action {id="synthetic_taint", run=function() taint=true end}
assert(SMRTK.Run("synthetic_taint"))
assert(file_log[#file_log]:find("SMRTK_TAINT action=synthetic_taint before=false used=true", 1, true))
taint = false -- ONLY this synthetic desk model resets its fake flag.
SMRTK.Action {id="throws", run=function() error("known desk failure") end}
local ok, result = SMRTK.Run("throws"); assert(not ok and result.status == "ERROR")
SMRTK.Action {id="engine_reports", run=function() emit("OnLuaError", "reported, no unwind", "stack witness") end}
local ok, result = SMRTK.Run("engine_reports"); assert(not ok and result.status == "ERROR")
SMRTK.Mark("errors")
emit("OnLuaError", "injected", "STACK\nNEXT")
emit("OnThreadError", "thread", "thread error")
assert(SMRTK.error_count - SMRTK.mark_errors == 2)
SMRTK.CopySince(); assert(clipboard:find([[STACK\nNEXT]], 1, true))

local restored = 0
SMRTK.Action {id="partial_arm", run=function() end,
  arm=function(ctx) ctx.state.partial=true; return false, "installation refused" end,
  disarm=function(ctx) if ctx.state.partial then restored=restored+1 end end}
assert(not SMRTK.Arm("partial_arm") and restored == 1 and not SMRTK.armed.partial_arm)
SMRTK.Action {id="throws_arm", run=function() end,
  arm=function(ctx) ctx.state.partial=true; error("arm failure") end,
  disarm=function(ctx) restored=restored+1 end}
assert(not SMRTK.Arm("throws_arm") and restored==2 and not SMRTK.armed.throws_arm)
SMRTK.Action {id="engine_arm", run=function() end,
  arm=function(ctx) emit("OnLuaError", "arm reports", "stack") end,
  disarm=function(ctx) restored=restored+1 end}
assert(not SMRTK.Arm("engine_arm") and restored==3 and not SMRTK.armed.engine_arm)
SMRTK.Action {id="bad_cleanup", run=function() end,
  arm=function(ctx) return false, "no" end,
  disarm=function(ctx) return false, "cannot restore" end}
assert(not SMRTK.Arm("bad_cleanup") and SMRTK.armed.bad_cleanup)
SMRTK.actions.bad_cleanup.disarm=function() end
assert(SMRTK.Disarm("bad_cleanup", "desk repair") and not SMRTK.armed.bad_cleanup)
assert(not SMRTK.Run("not_built"))
assert(SMRTK.Bind(1, "slot", function(ctx) return {selected=ctx.selected ~= nil} end))
assert(not SMRTK.Bind(7, "bad", function() end))
local before = #file_log
assert(SMRTK.Run("slot_1") and SMRTK.fires.slot_1 == 1 and #file_log == before+1)

assert(SMRTK.PanelState().open == false and SMRTK.PanelState().tab == "Kit")
assert(SMRTK.SavePanelState{open=true, x=123, collapsed=true})
run_threads(); assert(saved.open and saved.x == 123 and saved.collapsed)
local ok, result = SMRTK.ConsoleControl()
assert(ok and result.negative == false and result.positive == true and result.discriminates)
assert(ConsoleEnabled)
''')
print("CORE SMOKE: PASS — formatting/flush, native absent/present, overflow, clipboard, tee restore/returns, lifecycle cleanup, taint RED, failures, slots, persistence, console false/true")

panel = KIT / "Code/71_SMRTK_Panel.lua"
if not panel.exists():
    print("PANEL SMOKE: not built yet")
else:
    lua.execute(r'''
    function RGBA(...) return table.concat({...}, ",") end
    function MulDivRound(a,b,c) return math.floor(a*b/c+0.5) end
    local pmt = {__index={x=function(p) return p[1] end, y=function(p) return p[2] end}}
    function point(x,y) return setmetatable({x,y},pmt) end
    pmt.__add=function(a,b) return point(a:x()+b:x(),a:y()+b:y()) end
    pmt.__sub=function(a,b) return point(a:x()-b:x(),a:y()-b:y()) end
    local bmt = {__index={minx=function(b) return b[1] end, miny=function(b) return b[2] end,
      sizex=function(b) return b[3]-b[1] end, sizey=function(b) return b[4]-b[2] end,
      min=function(b) return point(b[1],b[2]) end}}
    function box(x,y,r,b) return setmetatable({x,y,r,b},bmt) end
    local window = {}
    function window:new(props,parent)
      local o = props or {}; setmetatable(o,{__index=self}); o.class=self.class
      o.window_state='new'; o.parent=parent; o.desktop=parent and parent.desktop
      o.scale=parent and parent.scale or point(1000,1000); o.box=box(0,0,0,0)
      o.visible=true
      if parent then parent[#parent+1]=o end
      return o
    end
    function window:SetText(s) self.Text=s end
    function window:SetVisible(v) self.visible=v end
    function window:GetVisible() return self.visible end
    function window:SetMinHeight(n) self.MinHeight=n end
    function window:SetMaxHeight(n) self.MaxHeight=n end
    function window:SetBackground(c) self.Background=c end
    function window:SetMargins(b)
      self.Margins=b
      self.box=box(b:minx(),b:miny(),b:minx()+(self.MinWidth or 0),b:miny()+(self.MinHeight or 0))
    end
    function window:Open() self.window_state='open'; for _,child in ipairs(self) do child:Open() end end
    function window:CreateThread(name,fn) self.status_thread=fn end
    function window:delete()
      self.window_state='destroying'
      for _,child in ipairs(self) do child:delete() end
      if self.parent then for i,v in ipairs(self.parent) do if v==self then table.remove(self.parent,i); break end end end
    end
    XWindow=setmetatable({class='XWindow'},{__index=window})
    XScrollArea=setmetatable({class='XScrollArea'},{__index=window})
    XDialog=setmetatable({class='XDialog'},{__index=window})
    XButton=setmetatable({class='XButton'},{__index=window})
    XText=setmetatable({class='XText'},{__index=window})
    XAction={new=function(self, props, host) host.actions[props.ActionId]=props end}
    desktop={box=box(0,0,1920,1080),scale=point(1000,1000)}; desktop.desktop=desktop
    function desktop:SetMouseCapture(w) self.capture=w end
    function desktop:GetMouseCapture() return self.capture end
    interface=XWindow:new({},desktop)
    function GetInGameInterface() return interface end
    function WaitLoadingScreenClose() end
    ''')
    lua.execute(panel.read_text(encoding="utf-8-sig"))
    lua.execute(r'''
    local p=SMRTK.OpenPanel()
    assert(p and p.class=='XDialog' and #SMRTK.page_order==5 and p.FocusOnOpen=='')
    assert(p.status.Text:find('eligibility: unavailable (sandbox)',1,true))
    assert(SMRTK.Run('tab_World') and SMRTK.PanelState().tab=='World')
    assert(SMRTK.Run('panel_collapse') and not SMRTK.PanelState().collapsed)
    assert(p.tabs.visible and p.page_host.visible and p.MinHeight==540)
    assert(SMRTK.Run('panel_collapse') and not p.tabs.visible and p.MinHeight==100)
    local ok,result=SMRTK.Run('pause'); assert(not ok and result.status=='NOT_BUILT')
    local strip=p[1]
    strip:OnMouseButtonDown(point(140,100),'L')
    strip:OnMouseButtonUp(point(180,130),'L')
    assert(SMRTK.PanelState().x==123 and SMRTK.PanelState().y==90)
    assert(desktop.capture==nil)
    assert(SMRTK.TogglePanel() and not p.visible and not SMRTK.PanelState().open)
    assert(SMRTK.TogglePanel() and p.visible and SMRTK.PanelState().open)
    assert(SMRTK.Run('tab_Kit'))
    ReloadShortcutsImmediate()
    assert(XShortcutsTarget.actions.SMRTK_Panel.ActionShortcut=='Ctrl-Shift-F11')
    emit('PreLoadGame'); assert(SMRTK.panel==nil)
    emit('PostLoadGame'); run_threads()
    assert(SMRTK.panel~=p and SMRTK.PanelState().tab=='Kit' and SMRTK.panel.visible)
    assert(SMRTK.ArmedCount()==0 and print==original_print)
    ''')
    print("PANEL SMOKE: PASS — registry, collapse, tabs, stubs, fixed side position, toggle, shortcut, reload reconstruction (mock X classes; no rendering claim)")
