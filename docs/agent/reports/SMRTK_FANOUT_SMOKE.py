"""03A desk falsifiers; mocks do not prove game rendering or construction."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
model = runpy.run_path(str(ROOT / "docs/agent/reports/SMRTK_SKELETON_SMOKE.py"))
lua = model["lua"]
lua.execute(r'''
screen_lines = {}
function ConsolePrint(s) screen_lines[#screen_lines+1]=s; emit("ConsoleLine",s,true) end
local files, screens = #file_log, #screen_lines
SMRTK.Run("clear")
assert(#file_log==files+1 and #screen_lines==screens)
SMRTK.Run("mark", "screen witness")
assert(#screen_lines==screens+1 and file_log[#file_log]:find("SMRTK_MARK",1,true))

TerminalTarget={new=function(self,props) return props end}
terminal={desktop=desktop,targets={}}
desktop.modal_window=desktop
world_mode={}
mouse_hit=world_mode
function desktop:GetMouseTarget(pt) return mouse_hit end
function GetInGameInterfaceModeDlg() return world_mode end
function GetTerrainCursor() return point(12,34) end
function SelectionMouseObj() return {class="Depot",handle=9} end
function terminal.AddTarget(target) terminal.targets[#terminal.targets+1]=target end
function terminal.RemoveTarget(target)
 for i,t in ipairs(terminal.targets) do if t==target then table.remove(terminal.targets,i); return end end
end
SMRTK.Action{id="click_smoke",run=function(ctx,pos,obj)
 assert(pos:x()==12 and obj.handle==9); return {target=obj}
end,arm=function(ctx)
 return SMRTK.AcquireClick(ctx.action,function(pos,obj) SMRTK.Fire(ctx.action,pos,obj) end)
end,disarm=function(ctx) SMRTK.ReleaseClick(ctx.action) end}
assert(not SMRTK.AcquireClick("click_smoke",function() end))
assert(SMRTK.Arm("click_smoke") and #terminal.targets==1)
assert(not SMRTK.AcquireClick("click_smoke",function() end) and #terminal.targets==1)
local target=terminal.targets[1]
mouse_hit={class="XTextEditor"}
target:OnMouseButtonDown(point(0,0),"L")
assert(SMRTK.fires.click_smoke==nil)
mouse_hit=world_mode
target:OnMouseButtonDown(point(0,0),"L")
assert(SMRTK.fires.click_smoke==1)
target:OnMouseButtonDown(point(0,0),"R")
assert(#terminal.targets==0 and not SMRTK.armed.click_smoke and not SMRTK.click_capture)
for _,event in ipairs({"SaveGameStart","PreLoadGame","CurrentMapChange","DoneGame"}) do
 assert(SMRTK.Arm("click_smoke")); emit(event)
 assert(#terminal.targets==0 and not SMRTK.click_capture and SMRTK.ArmedCount()==0)
end
SMRTK.SavePanelState{open=true}
emit("PostLoadGame"); emit("InGameInterfaceCreated"); emit("CurrentMapChangeDone")
local before=SMRTK.sequence
run_threads()
local restores=0
for _,line in ipairs(file_log) do
 local id=tonumber(line:match(" id=(%d+)$"))
 if id and id>before and line:find("SMRTK_PANEL_RESTORE",1,true) then restores=restores+1 end
end
assert(restores==1)
''')
print("FANOUT CORE: PASS — chrome sinks, evidence screen, exclusive clicks, UI exclusion, save/load/map cleanup, one actual restore")
