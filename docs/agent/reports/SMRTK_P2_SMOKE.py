"""P2 desk falsifiers using the real dispatcher/panel/payload, never rendering proof."""
from pathlib import Path
import hashlib
import re
import subprocess
import sys

from lupa import LuaRuntime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
source = (KIT / "Code/73_SMRTK_Infopanel.lua").read_text(encoding="utf-8-sig")
sys.path.insert(0, str(ROOT))
from tools.parsecheck import runtime

check, version = runtime()
assert check is not None, version
parse_error = check(source, "@73_SMRTK_Infopanel.lua")
assert parse_error is None, parse_error
print("PACK HEAD:", subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip())
print("TESTKIT HEAD:", subprocess.check_output(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"], text=True).strip())
print("P2 SHA256:", hashlib.sha256((KIT / "Code/73_SMRTK_Infopanel.lua").read_bytes()).hexdigest())
print(f"P2 PARSE: PASS [{version}]")
for gate, pattern in (("RULE 6", r"NetSyncEvent|LogCheatUsed"), ("RULE 7", r"^\s*print\("),
                      ("FORBIDDEN STATE", r"config\.BuildingInfopanelCheats\s*=|Platform\.cheats\s*=|AccountStorage|AreCheatsEnabled\(")):
    hits = [n for n, line in enumerate(source.splitlines(), 1) if re.search(pattern, line)]
    print(f"{gate}: {len(hits)} lines {hits}")
    assert not hits
presence = Path("A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src/Data/CheatDef.lua")
print("RULE 6 PRESENCE:", sum(bool(re.search(r"NetSyncEvent|LogCheatUsed", line))
      for line in presence.read_text(encoding="utf-8-sig").splitlines()), "lines")
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
hooks, records, displayed, queued = {}, {}, {}, {}
OnMsg = setmetatable({}, {__newindex=function(_,id,fn)
  hooks[id]=hooks[id] or {}; table.insert(hooks[id],fn)
end})
function emit(id,...) for _,fn in ipairs(hooks[id] or {}) do fn(...) end end
function RGBA(...) return table.concat({...},",") end
function GameTime() return 42 end
function ModLog(s) records[#records+1]=string.format(s) end
function FlushLogFile() end
function ConsolePrint(s) displayed[#displayed+1]=s end
taint=false
function AreCheatsUsed() return taint end
function IsValid(o) return type(o)=="table" and o.handle and not o.deleted end
function IsValidThread(t) return t == "busy" end
function PropObjHasMember(o,k) return o[k] ~= nil end
function ResolvePropObj(o) return o end
function ObjModified(o) modified=o end
function Untranslated(s) return s end
function CreateRealTimeThread(fn) queued[#queued+1]=fn end
CreateGameTimeThread=CreateRealTimeThread
function run_queued() local q=queued; queued={}; for _,fn in ipairs(q) do fn() end end
function Sleep() end
function WaitLoadingScreenClose() end
function SaveLocalStorage() end
function CopyToClipboard(s) clipboard=s end
function cls() end
LocalStorage={SMRTKPanel={surface="hybrid-v1",open=false,tab="Kit",x=8,y=80,collapsed=false}}
local bm={}
function bm:x() return self[1] end
function bm:y() return self[2] end
function bm:sizex() return 1920 end
function bm:sizey() return 1080 end
function bm:min() return self end
function box(...) return setmetatable({...},{__index=bm}) end
point=box
function MulDivRound(a,b,c) return math.floor(a*b/c+.5) end
local parents={HUDClass="XDialog",InfopanelDlg="XDialog",XDialog="XActionsHost",XActionsHost="XWindow",
  InfopanelSection="XWindow",XPopupMenu="XActionsView",XActionsView="XWindow",XButton="XWindow",
  XText="XWindow",XSleekScroll="XWindow",XScrollArea="XWindow"}
function IsKindOf(o,k)
  if type(o)~="table" then return false end
  if o.kinds and o.kinds[k] then return true end
  local c=o.class
  while c do if c==k then return true end; c=parents[c] end
  return false
end
local W={}
function W:ResolveId(id)
  if rawget(self,id) then return rawget(self,id) end
  local p=self.parent
  while p and not p.IdNode do p=p.parent end
  return p and rawget(p,id)
end
function W:Open()
  self.window_state="open"
  for _,c in ipairs(self) do c:Open() end
end
function W:delete()
  self.window_state="destroying"
  if self.parent then
    for i,c in ipairs(self.parent) do if c==self then table.remove(self.parent,i); break end end
    local p=self.parent
    while p and not p.IdNode do p=p.parent end
    if p and self.Id then p[self.Id]=nil end
  end
end
W.Close=W.delete
function W:SetVisible(v) self.visible=v end
function W:GetVisible() return self.visible end
function W:SetText(v) self.Text=v end
function W:SetBackground(v) self.Background=v end
function W:SetMargins(v) self.Margins=v end
function W:SetMinHeight(v) self.MinHeight=v end
function W:SetMaxHeight(v) self.MaxHeight=v end
function W:CreateThread(id,fn) self.threads[id]=fn end
function W:ClearActions() self.actions={} end
function W:ActionById(id) for _,a in ipairs(self.actions) do if a.ActionId==id then return a end end end
function W:ClosePopupMenus() self:delete() end
function W:PopupAction(id,host,source) self.submenu={id=id,host=host,source=source} end
local function cls(name)
  local c={}
  function c:new(props,parent,context)
    local w=props or {}; w.class=name; w.parent=parent; w.context=context
    w.window_state="new"; w.visible=w.Visible~=false; w.threads={}; w.actions={}
    w.box=box(20,20,80,80); w.scale=point(1000,1000); w.desktop=terminal and terminal.desktop
    if name=="XDialog" or name=="HUDClass" or name=="InfopanelDlg" then w.IdNode=true end
    setmetatable(w,{__index=W})
    if parent then
      table.insert(parent,w)
      local node=parent
      while node and not node.IdNode do node=node.parent end
      if node and w.Id then node[w.Id]=w end
    end
    if name=="InfopanelSection" then XWindow:new({Id="idContent"},w,context) end
    return w
  end
  return c
end
for _,n in ipairs({"XWindow","XDialog","XActionsHost","XButton","XText","XScrollArea","XSleekScroll",
  "XPopupMenu","InfopanelSection","HUDClass","InfopanelDlg"}) do _G[n]=cls(n) end
terminal={desktop=XWindow:new({IdNode=true})}
interface=XWindow:new({IdNode=true},terminal.desktop)
function GetInGameInterface() return interface end
function GetHUD() return hud end
function GetParentOfKind(win,kind)
  while win do if IsKindOf(win,kind) then return win end; win=win.parent end
end
XAction={new=function(self,props,host) table.insert(host.actions,props); return props end}
XShortcutsTarget={}
''')
for name in ("70_SMRTK_Core.lua", "71_SMRTK_Panel.lua", "73_SMRTK_Infopanel.lua"):
    lua.execute((KIT / "Code" / name).read_text(encoding="utf-8-sig"))
lua.execute(r'''
local T=SMRTK
local function find_button(win,text)
  for _,child in ipairs(win) do
    if child.class=="XButton" and child[1] and child[1].Text==text then return child end
    local found=find_button(child,text); if found then return found end
  end
end
function depot(resources)
  return {class="StorageMetals",handle=1054,kinds={UniversalStorageDepotBase=true},
    resource=resources,storable_resources=resources,stored=13,
    GetStoredAmount=function(self,r) return self.stored end,
    CheatFill=function(self) self.stored=180 end, CheatEmpty=function(self) self.stored=0 end,
    CheatDelete=function(self) self.deleted=true end}
end
local obj=depot({"Metals"}); SelectedObj=obj
local count=#records
local ok,result=T.Run("selected_fill",obj)
assert(ok and result.before==13 and result.after==180 and result.resources==1 and result.resource=="Metals")
assert(result.object=="StorageMetals(1054)" and #records==count+1 and not taint)
obj=depot({"Metals","Food"}); SelectedObj=obj
ok,result=T.Run("selected_fill",obj)
assert(ok and result.resources==2 and result.before==26 and result.after==360 and result.resource=="multiple")
local previous=obj; SelectedObj=depot({"Food"})
ok,result=T.Run("selected_fill",previous)
assert(not ok and result.status=="REFUSED" and SelectedObj.stored==13)
SelectedObj={class="MechanizedDepot",handle=9,is_storing="busy",CheatFill=function() error("deferred leaf entered") end}
ok,result=T.Run("selected_fill")
assert(not ok and result.status=="REFUSED" and result.reason:find("animation",1,true))
SelectedObj=nil; ok,result=T.Run("selected_fill"); assert(not ok and result.status=="REFUSED")
SelectedObj={class="Odd",handle=1}; ok,result=T.Run("selected_fill"); assert(not ok and result.status=="REFUSED")
assert(#T.SelectedActions(SelectedObj)==0)
obj=depot({"Metals"}); SelectedObj=obj
local rows=T.SelectedActions(obj); assert(rows[#rows].label=="Pin C (not built)")
count=#records; ok,result=T.Run("pin_C"); assert(not ok and result.status=="NOT_BUILT" and #records==count+1)
local pin_called=false
T.Action{id="pin_C",needs="selected",run=function() pin_called=true end}
assert(T.SelectedActions(obj)[#rows].label=="Pin C")
local host=InfopanelDlg:new({IdNode=true},interface,obj)
local content=XWindow:new({Id="idContent"},host,obj)
local vanilla=XWindow:new({Id="idSectionCheats"},content,obj)
local tail=XWindow:new({},content,obj)
local before_display=#displayed
emit("DialogOpen",host)
local section=host.idSMRTKSection
assert(section and section.class=="InfopanelSection" and section.window_state=="open")
assert(content[1]==vanilla and content[2]==section and content[3]==tail)
assert(#displayed==before_display)
count=#records; emit("DialogOpen",host); assert(#records==count)
local pin=find_button(section,"Pin C"); assert(pin); pin:OnPress(); run_queued(); assert(pin_called)
local fill=find_button(section,"Fill"); assert(fill)
fill:OnPress(); SelectedObj=depot({"Food"}); run_queued()
assert(SelectedObj.stored==13 and records[#records]:find("status=REFUSED",1,true))
SelectedObj=obj
local unsupported=InfopanelDlg:new({IdNode=true},interface,obj)
ok,result=T.Run("section_attach",unsupported)
assert(ok and result.fallback=="Selected" and not result.attached and T.pages.Selected)
-- Late registration is visible; unannotated parameter consumers never get menu items.
T.Action{id="world_args",page="World",run=function(ctx,a) assert(a~=nil) end}
T.Action{id="world_complete",page="World",menu=true,run=function() return {done=true} end}
T.Action{id="world_explicit",page="World",menu={phase="run",args={27}},run=function(ctx,n) assert(n==27) end}
T.Action{id="world_toggle",page="World",menu="arm",run=function() end,arm=function() end,disarm=function() end}
local ids={}
for _,group in ipairs(T.DockMenuItems()) do for _,item in ipairs(group.items) do ids[item.id]=item end end
assert(not ids.world_args and ids.world_complete and ids.world_explicit.args[1]==27 and ids.world_toggle.phase=="arm")
hud=HUDClass:new({IdNode=true},interface)
local bottom=XWindow:new({Id="idBottom"},hud)
local left=XWindow:new({Id="idLeft",LayoutMethod=""},bottom)
local map=XWindow:new({},left)
emit("DialogOpen",hud)
assert(T.dock and T.dock.parent==bottom and left[1]==map and left.LayoutMethod=="")
assert(T.dock.status.Text:find("CLEAN",1,true) and T.dock.status.Text:find("eligibility: unavailable",1,true))
assert(T.dock.status.Text:find("Armed: 0",1,true))
count=#records; emit("DialogOpen",hud); assert(#records==count)
assert(T.Run("dock_menu")); assert(T.dock_menu.class=="XPopupMenu")
local explicit=T.dock:ActionById("SMRTKDockAction_world_explicit")
count=#records; explicit.OnAction(); run_queued(); assert(#records==count+1)
local toggle=T.dock:ActionById("SMRTKDockAction_world_toggle")
count=#records; toggle.OnAction(); run_queued(); assert(T.armed.world_toggle and #records==count+1)
assert(T.dock.status.Text:find("Armed: 1",1,true))
toggle.OnAction(); run_queued(); assert(not T.armed.world_toggle)
T.Action{id="late_world",page="World",menu=true,run=function() end}
T.Run("dock_menu"); T.Run("dock_menu"); assert(T.dock:ActionById("SMRTKDockAction_late_world"))
assert(not T.dock:ActionById("SMRTKDockAction_world_args"))
T.Run("dock_page","Selected"); assert(T.PanelState().tab=="Selected" and T.panel:GetVisible())
assert(T.dock:ActionById("SMRTKDockClosePanel").ActionState()==nil)
T.Run("dock_close_panel"); assert(not T.panel:GetVisible())
assert(T.dock:ActionById("SMRTKDockClosePanel").ActionState()=="disabled")
-- Positive taint/error controls: the read must turn red, including closed panels.
T.Action{id="synthetic_taint",run=function() taint=true end}
count=#records; T.Run("synthetic_taint")
assert(#records==count+2 and records[#records]:find("SMRTK_TAINT action=synthetic_taint",1,true))
assert(T.dock.status.Text:find("TAINTED",1,true))
AreCheatsUsed=nil; T.RefreshDock(); assert(T.dock.status.Text:find("UNKNOWN",1,true))
T.OnLuaError("desk error","witness"); T.RefreshDock(); assert(T.dock.status.Text:find("errors since mark: 1",1,true))
local dock=T.dock; emit("ChangeMap"); assert(not T.dock and dock.window_state=="destroying" and not T.dock_menu)
assert(not T.armed.world_toggle)
''')
print("P2 DESK: PASS — selected guards, single/multi depots, busy refusal, dynamic companions, injection/order/idempotence, queued selection race, fallback, argument-safe menus, late actions, one primary per click, arms, side page, CLEAN/TAINTED/UNKNOWN/errors, lifecycle")
leaf_count = lua.eval("function() local n=0; for _,d in pairs(SMRTK.actions) do if d.page=='Selected' then n=n+1 end end; return n end")()
catalog_count = lua.eval("function() local o=setmetatable({class='AllMethodsDesk',handle=1,deleted=false},{__index=function() return function() end end}); return #SMRTK.SelectedActions(o) end")()
assert catalog_count >= leaf_count, "catalog mock must remain a valid selected object"
print(f"P2 CATALOG: {leaf_count} selected leaf actions + {catalog_count - leaf_count} companion registry ids; actual objects show supported subsets")
print("P2 LIMIT: fake X controls and game services; no rendering, save mutation, or in-game no-taint claim")
