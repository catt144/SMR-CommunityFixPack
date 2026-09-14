"""Coordinator integration falsifier. Native UI/timing still belongs to sitting 08."""
from pathlib import Path
import ast
import subprocess
import sys
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print("$ " + subprocess.list2cmdline(["python", "docs/agent/reports/SMRTK_FANOUT_MERGE.py"] + sys.argv[1:]))
print("HEAD pack=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
      + " testkit=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=KIT, text=True).strip())
# Reuse only the deterministic engine-service setup, not a payload's assertions.
tree = ast.parse((ROOT / "docs/agent/reports/SMRTK_P3_SMOKE.py").read_text(encoding="utf-8"))
setup = next(n.value.args[0].value for n in tree.body if isinstance(n, ast.Expr)
             and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
             and isinstance(n.value.func.value, ast.Name) and n.value.func.value.id == "lua"
             and n.value.func.attr == "execute")
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(setup)
lua.execute(r'''
function IsRealTimeThread() return active_thread and active_thread.kind=='real' end
function GetPreciseTicks() return 123456 end
function AsyncRand(n) return 5 end
empty_table={}; const={HourDuration=1000,Scale={Resources=1000},DefaultTimeFactor=1000,MaxSaneTimeFactor=100000,GameSpeeds={fast=3}}
function GetPeriodicRepeatThread() return nil end
config={SaveGameExt='.savegame.sav'}
SMRTest={Print=function(...) end,SetGlobal=function(name,value) _G[name]=value end,
  order={},probes={},last={}}
SMRFixPack={order={'a','b'},fixes={a={status='active'},b={status='inactive'}}}
XSleekScroll=XWindow; XPopupMenu=XWindow; InfopanelSection=XWindow; XCombo=XWindow
function XWindow:SetVisible(v) self.visible=v end
function XWindow:GetVisible() return self.visible~=false end
function XWindow:SetMinHeight(v) self.MinHeight=v end
function XWindow:SetMaxHeight(v) self.MaxHeight=v end
function XWindow:SetMargins(v) self.Margins=v end
function XWindow:SetEnabled(v) self.enabled=v end
function XWindow:SetTextColor(v) self.TextColor=v end
function XWindow:SetItems(v) self.Items=v end
function XWindow:SetValue(v) self.Value=v end
function XWindow:GetValue() return self.Value or self.DefaultValue end
function XWindow:ResolveId(id)
  if id=='node' then local p=self; while p and not p.IdNode do p=p.parent end; return p or self end
  if self.Id==id then return self end
  for _,child in ipairs(self) do local v=child:ResolveId(id); if v then return v end end
end
function XWindow:InvalidateMeasure() end
function XWindow:InvalidateLayout() end
local old_new=XWindow.new
function XWindow:new(props,parent)
 local w=old_new(self,props,parent)
 if parent then w.desktop=parent.desktop; w.scale=parent.scale; w.box=parent.box end
 if self==XTextEditor then w.Text=''; w.editor=true end
 return w
end
function MulDivRound(a,b,c) return math.floor(a*b/c+0.5) end
function IsKindOf(o,c) return o and (o.class==c or (o.kinds and o.kinds[c])) or false end
function PropObjHasMember(o,k) return o and o[k]~=nil end
function ResolvePropObj(o) return o end
function GetGameSpeed() return game_speed or 1 end
function sorted_pairs(t)
 local ks={}; for k in pairs(t) do ks[#ks+1]=k end; table.sort(ks)
 local i=0; return function() i=i+1; local k=ks[i]; if k then return k,t[k] end end
end
function MeteorsDisaster(...) meteor_calls=(meteor_calls or 0)+1 end
vanilla_meteors=MeteorsDisaster
function StartDustStorm(...) end
function StartColdWave(...) end
function GenerateDustDevilIn(...) end
function TriggerMarsquake(...) end
function FindEpicentre(...) end
function RainProcedure(...) end
function PresetsCombo() return function() return {} end end
Presets={MapSettings={}}; TraitPresets={}; TraitsCombo={}
CurrentMap=1; UICity={labels={}}; ActiveMaps={[1]={}}
world=XWindow:new({}); world.desktop={box={sizex=function() return 1920 end,sizey=function() return 1080 end}}
world.box=world.desktop.box; world.scale=point(1000,1000)
function GetInGameInterface() return world end
function GetInGameInterfaceModeDlg() return world end
function PlaceObj(class,fields) local t={} for i=1,#fields,2 do t[fields[i]]=fields[i+1] end return t end
''')
mod = lua.execute((KIT / "metadata.lua").read_text(encoding="utf-8-sig"))
code = [mod["code"][i] for i in range(1, len(mod["code"]) + 1)]
ordered = [p for p in code if not p.startswith("Code/") and p != "__const.lua"] + [p for p in code if p.startswith("Code/")]
names = {"Code/70_SMRTK_Core.lua", "Code/71_SMRTK_Panel.lua", "Code/72_SMRTK_World.lua",
         "Code/73_SMRTK_Infopanel.lua", "Code/74_SMRTK_Agent.lua", "Code/75_SMRTK_Saves.lua",
         "Code/76_SMRTK_Kit.lua", "Code/77_SMRTK_Stamper.lua", "Code/80_AgentSlots.lua", "Code/90_Loggers.lua"}
assert names <= set(code), "missing toolkit metadata entries"
for name in ordered:
    if name in names or name.startswith("Layouts/"):
        src = (KIT / name).read_text(encoding="utf-8-sig")
        if "--editor-mutant" in sys.argv:
            mutant = sys.argv[sys.argv.index("--editor-mutant") + 1]
            target, text = {"World": ("Code/72_SMRTK_World.lua", "\tedit:SetText(tostring(value))"),
                            "Kit": ("Code/76_SMRTK_Kit.lua", "\teditor:SetText(K.field)"),
                            "Stamper": ("Code/77_SMRTK_Stamper.lua", "\teditor:SetText(L.name)")}[mutant]
            if name == target:
                assert src.count(text) == 1
                src = src.replace(text, "")
        lua.execute(src)
        print("LOAD " + name)
lua.execute("emit('DataLoaded')")

def case(name, src):
    lua.execute(src)
    print("PASS " + name)

case("co-load is idle, selected companions and World follow-ups resolve", r'''
T=SMRTK
assert(T.ArmedCount()==0 and #terminal.targets==0 and MeteorsDisaster==vanilla_meteors)
assert(next(SMRTest.LoggerState())==nil)
for _,id in ipairs({'dump_selected','pin_A','pin_B','pin_C','watch_field',
 'fill_storages','spawn_colonists','funding','pause','stop_disaster','quiet'}) do
 assert(T.actions[id], 'missing cross-payload action '..id)
end
for _,id in ipairs({'Sitting','Selected','Agent','World','Saves','Kit','Stamper'}) do
 assert(T.pages[id] and T.pages[id].build,'stubbed page '..id)
end
assert(type(T.TriggerField)=='function' and T.Stamper)
''')
case("actual90 logger and quiet refuse nesting and restore captured functions", r'''
real(function()
 assert(T.actions.logger_Meteors)
 assert(T.Arm('logger_Meteors'))
 local wrapped=MeteorsDisaster; assert(wrapped~=vanilla_meteors)
 assert(not T.Arm('quiet') and not T.armed.quiet and MeteorsDisaster==wrapped)
 assert(T.Disarm('logger_Meteors') and MeteorsDisaster==vanilla_meteors)
 assert(T.Arm('quiet'))
 wrapped=MeteorsDisaster; assert(wrapped~=vanilla_meteors)
 assert(not T.Arm('logger_Meteors') and not T.armed.logger_Meteors and MeteorsDisaster==wrapped)
 emit('SaveGameStart')
 assert(T.ArmedCount()==0 and MeteorsDisaster==vanilla_meteors and next(SMRTest.LoggerState())==nil)
 SMRTest.Log.Meteors(true); wrapped=MeteorsDisaster
 assert(not T.Arm('quiet') and not T.Arm('logger_Meteors') and MeteorsDisaster==wrapped)
 SMRTest.Log.Meteors(false); assert(MeteorsDisaster==vanilla_meteors)
end)
''')
case("P4 field-watch command creates P3 trigger without implicit arming or retarget", r'''
real(function()
 assert(T.Run('watch_field','command'))
 assert(T.triggers.watch_selected_field and not T.armed.watch_selected_field)
 assert(T.Arm('watch_selected_field'))
end)
step('game')
local watched=SelectedObj; SelectedObj={class='Other',handle=8,command='Changed'}
watched.command='Work'; tick()
assert(T.fires.watch_selected_field==1 and count('TRIGGER','watch_selected_field')==1)
emit('PreLoadGame'); assert(T.ArmedCount()==0)
SelectedObj=watched
''')
case("MARK hook follows primary evidence and covers ordinary and screenshot marks", r'''
local base=#file_log
assert(T.Run('mark','merge mark'))
assert(count('MARK','mark',base+1)==1 and count('FINGERPRINT','fingerprint',base+1)==1)
assert(file_log[base+1]:find('SMRTK_MARK ',1,true) and file_log[base+2]:find('SMRTK_FINGERPRINT ',1,true))
assert(T.kit.fingerprint.fix_pack_present=='1/2' and T.kit.fingerprint.read=='live registry')
base=#file_log
real(function() assert(T.Run('screenshot_mark')) end)
assert(count('MARK','screenshot_mark',base+1)==1 and count('FINGERPRINT','fingerprint',base+1)==1)
T.Action{id='refused_mark',verb='MARK',run=function() return false,'control' end}
base=#file_log; assert(not T.Run('refused_mark'))
assert(count('MARK','refused_mark',base+1)==1 and count('FINGERPRINT','fingerprint',base+1)==0)
local saved=T.after_record.MARK
T.after_record.MARK=function() T.Run('mark','recursive control') end
base=#file_log; assert(T.Run('mark','outer control'))
assert(count('MARK','mark',base+1)==2,'hook recursion not bounded')
T.after_record.MARK=function() error('hook control') end
base=#file_log; assert(T.Run('mark','hook error control'))
assert(count('MARK','mark',base+1)==1 and count('ERROR',nil,base+1)==1)
T.after_record.MARK=saved
''')
case("all advanced pages build in one body with sibling scrollbar and bounded tabs", r'''
local panel=assert(T.OpenPanel())
local tab_width=0
for _,button in pairs(panel.tab_buttons) do tab_width=tab_width+button.MinWidth end
assert(tab_width+4*(#T.page_order-1)<=panel.MinWidth-16)
for _,id in ipairs(T.page_order) do
 local ok,fields=T.Run('tab_'..id); assert(ok,id..': '..tostring(fields.reason))
 assert(panel.page_host and panel.page_frame and panel.page_frame.IdNode)
 assert(panel.page_host.parent==panel.page_frame and panel.page_host.VScroll=='idSMRTKPageScroll')
 assert(panel.page_host:ResolveId('node'):ResolveId(panel.page_host.VScroll))
end
local function edits(w,out)
 if w.editor then out[#out+1]=w end
 for _,child in ipairs(w) do edits(child,out) end
 return out
end
assert(T.Run('tab_World'))
local fields=edits(panel.page_host,{})
assert(#fields>0); for _,e in ipairs(fields) do assert(e:GetText()~='','World editor lost default') end
assert(T.Run('tab_Kit')); fields=edits(panel.page_host,{})
assert(#fields==1 and fields[1]:GetText()==T.kit.field,'Kit field default lost')
assert(T.Run('tab_Stamper')); fields=edits(panel.page_host,{})
assert(#fields==1 and fields[1]:GetText()==T.Stamper.name,'Stamper name default lost')
T.agent_sol='11'; T.agent_field='command'
assert(T.Run('tab_Agent')); fields=edits(panel.page_host,{})
assert(#fields>=3); local initialized=0
for _,e in ipairs(fields) do if e:GetText()~='' then initialized=initialized+1 end end
assert(initialized>=2,'Agent sol/field defaults lost')
T.saves.status='foreign session: control'
T.RefreshPanel(); assert(panel.status.Text:find('foreign session:',1,true))
''')
actions = lua.globals().SMRTK["actions"]
for page in ("Selected", "Agent", "World", "Saves", "Kit", "Stamper"):
    values = sorted((str(d["label"] or action) + " [" + str(action) + "]")
                    for action, d in actions.items() if d["page"] == page)
    print("REGISTRY " + page + ": " + "; ".join(values))
print("MERGE DESK: PASS (mock services; no native render, save round trip or stamp claim)")
if "--selftest" in sys.argv:
    for name, message in (("World", "World editor lost default"), ("Kit", "Kit field default lost"),
                          ("Stamper", "Stamper name default lost")):
        result = subprocess.run([sys.executable, __file__, "--editor-mutant", name],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result.returncode != 0 and message in result.stderr, result.stdout + result.stderr
        print("FALSIFIER editor " + name + ": RED as required")
