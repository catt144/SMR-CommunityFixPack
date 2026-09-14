"""P5 contract falsifiers with fake native services; no engine/colony stamp claim."""
from pathlib import Path
import subprocess
import sys
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
hooks, logs, threads, world_objects, mutations, events = {}, {}, {}, {}, 0, {}
OnMsg = setmetatable({}, {__newindex=function(_,n,f) hooks[n]=hooks[n] or {}; table.insert(hooks[n],f) end})
function emit(n,...) for _,f in ipairs(hooks[n] or {}) do f(...) end end
function ModLog(s) logs[#logs+1]=string.format(s) end
function ConsolePrint(s) end
function FlushLogFile() end
function GameTime() return 400 end
function AreCheatsUsed() return false end
function CopyToClipboard(s) clipboard=s end
function SaveLocalStorage() return true end
function CreateRealTimeThread(f) threads[#threads+1]=f; return f end
function drain() local t=threads; threads={}; for _,f in ipairs(t) do f() end end
function Sleep(ms) if on_sleep then on_sleep() end end
function IsPaused() return paused or false end
LocalStorage={}
GameInitThreads={}
point_meta={__index={x=function(s)return s[1]end,y=function(s)return s[2]end,xy=function(s)return s[1],s[2]end}}
function point(x,y) return setmetatable({x,y},point_meta) end
function WorldToHex(p) return p:x(),p:y() end
function HexToWorld(q,r) return q,r end
function HexAngleToDirection(a) return a/3600 end
function HexRotate(p,d) local q,r=p:xy(); for i=1,d do q,r=-r,q+r end; return q,r end
HexNeighbours={point(1,0),point(0,1),point(-1,1),point(-1,0),point(0,-1),point(1,-1)}
function IsValid(o) return type(o)=='table' and o.valid==true end
function IsKindOf(o,k) return type(o)=='table' and (o.class==k or o.kinds and o.kinds[k]) or false end
local methods={}
function methods:HasMember(k) return self[k]~=nil end
function methods:GetEntity() return self.entity end
function methods:GetBuildShape() return self.shape end
function methods:GetBuildableAreaShape() return self.shape end
function methods:GetMap() return self.map or CurrentMap end
function methods:GetPos() return self.pos end
function methods:GetAngle() return self.angle or 0 end
function methods:GetUpgradeID(i) return (self.upgrade_ids or {})[i] or '' end
function methods:HasUpgrade(id) return (self.upgrades_built or {})[id] end
function make_proto(n,ks,shape)
  return setmetatable({class=n,kinds=ks or {Building=true},entity=n,shape=shape or {point(0,0)},template_name=n}, {__index=methods})
end
BuildingTemplates={
  Habitat=make_proto('Habitat'),
  DomeBasic=make_proto('DomeBasic',{Building=true,Dome=true},{point(-1,0),point(0,0),point(1,0)}),
  Landing=make_proto('Landing',{Building=true,LandingPadBase=true}),
}
local next_handle=100
function object(t,q,r,classes)
  next_handle=next_handle+1
  local p=BuildingTemplates[t] or make_proto(t,classes)
  local o=setmetatable({valid=true,class=t,template_name=t,kinds=classes or p.kinds,entity=p.entity,shape=p.shape,pos=point(q,r),handle=next_handle,map=CurrentMap}, {__index=methods})
  world_objects[#world_objects+1]=o
  return o
end
function covers(o,q,r)
  if not IsValid(o) then return false end
  for _,p in ipairs(o.shape) do local x,y=HexRotate(p,HexAngleToDirection(o.angle or 0)); if o.pos:x()+x==q and o.pos:y()+y==r then return true end end
  return false
end
CurrentMap={name='desk',City={},object_hex_grid={},buildable={},changing=false}
CurrentMap.City.colony={day=3}
function CurrentMap.City:GetMap() return CurrentMap end
function CurrentMap:IsPointInBounds(p) return p:x()>=0 and p:y()>=0 and p:x()<1000 and p:y()<1000 end
function CurrentMap.buildable:GetZ(q,r) return heights and heights[q..','..r] or 0 end
function IsBuildableZoneQR(q,r) return not (unbuildable and unbuildable[q..','..r]) end
function CurrentMap:MapForEach(area,cls,fn) local snap={table.unpack(world_objects)}; for _,o in ipairs(snap) do if IsValid(o) and IsKindOf(o,cls) then fn(o) end end end
function CurrentMap.object_hex_grid:GetObject(q,r,cls) for _,o in ipairs(world_objects) do if o.map==CurrentMap and covers(o,q,r) and IsKindOf(o,cls) then return o end end end
function GetDomeAtPoint(grid,p) return grid:GetObject(p:x(),p:y(),'Dome') end
function HexGridShapeGetObjectList(grid,pos,a,shape,c,ignore,filter)
  local out={}; for _,o in ipairs(world_objects) do
    if IsValid(o) and o.map==CurrentMap and (not filter or filter(o)) then
      for _,p in ipairs(shape) do local x,y=HexRotate(p,HexAngleToDirection(a)); if covers(o,pos:x()+x,pos:y()+y) then out[#out+1]=o; break end end
    end
  end; return out
end
function HexGetUnits(...) return loose and {loose} or {} end
function DoneObject(o) o.valid=false; events[#events+1]='done:'..o.class end
local original_city=CurrentMap.City
function reset_world()
  world_objects={}; mutations=0; events={}; native_calls={}; loose=nil; unbuildable=nil; heights=nil; on_sleep=nil; paused=false; fail_cell=nil; native_error=nil; GameInitThreads={}
  CurrentMap.City=original_city
  if SMRTK then SMRTK.Stamper.busy=nil; SMRTK.DisarmAll('desk reset') end
end
function PlaceConstructionSite(city,t,pos,a,params)
  assert(not prohibit_mutation, 'PLAN CALLED A MUTATING BUILDING PLACER')
  mutations=mutations+1; events[#events+1]='place:'..t
  local site=object(t,pos:x(),pos:y(),{ConstructionSite=true,Building=true})
  site.class='ConstructionSite'; site.angle=a
  function site:Complete(mode)
    assert(mode=='quick_build'); mutations=mutations+1; events[#events+1]='complete:'..t
    self.valid=false
    local built=object(t,pos:x(),pos:y()); built.angle=a
    if t=='DomeBasic' and wait_for_dome then
      GameInitThreads[built]=true
      on_sleep=function() GameInitThreads[built]=nil; on_sleep=nil end
    end
    return built
  end
  if native_error then emit('OnLuaError','synthetic placement failure','P5 desk') end
  return site
end
SupplyGridElementHexStatus={clear=1,blocked=2}
native_calls={}
local function line(k,city,q,r,dir,steps,test,requires,input_group,input_data)
  assert(input_group==nil,'test/placement inherited an unrelated group')
  native_calls[#native_calls+1]={k=k,q=q,r=r,dir=dir,steps=steps,test=test}
  local data={}; local dq,dr=HexNeighbours[dir+1]:xy()
  local grp
  if not test then
    assert(not prohibit_mutation,'PLAN CALLED A MUTATING GRID PLACER')
    mutations=mutations+1
    local leader=object('ConstructionGroupLeader',q,r,{ConstructionSite=true,ConstructionGroupLeader=true})
    leader.shape={}; grp={leader}; leader.construction_group=grp
    function leader:Complete(mode)
      assert(mode=='quick_build_skip_done'); events[#events+1]='group_complete:'..k
      for i=2,#grp do local s=grp[i]; local b=object(s.class,s.pos:x(),s.pos:y(),{[s.class]=true}); s.construction_group=false end
    end
  end
  for i=0,steps do
    local x,y=q+i*dq,r+i*dr
    local cls=k=='cable' and 'ElectricityGridElement' or 'LifeSupportGridElement'
    local o=CurrentMap.object_hex_grid:GetObject(x,y,cls)
    data[i]={q=x,r=y,status=fail_cell==i and 2 or 1,rocks={},stockpiles={}}
    if not test then
      if not o then o=object(cls,x,y,{[cls]=true,ConstructionSite=true}); o.construction_group=grp; grp[#grp+1]=o end
      data[i][k]=o
    end
  end
  if grp and #grp==1 then grp[1].valid=false end
  return true,{data=data,construction_group=grp}
end
function PlaceCableLine(...) return line('cable',...) end
function PlacePipeLine(...) return line('pipe',...) end
function PlacePassageLine() error('PASSAGE PLACER MUST NEVER RUN IN V1') end
function base(name) return {v=1,name=name or 'test',anchor={q=1,r=1},buildings={},grid={},meta={map='desk',sol=3,captured=400}} end
function building(t,dq,dr,dome) return {t=t or 'Habitat',dq=dq or 0,dr=dr or 0,a=0,dome=dome} end
terminal={targets={}}
function terminal.AddTarget(o) terminal.targets[o]=true end
function terminal.RemoveTarget(o) terminal.targets[o]=nil end
TerminalTarget={new=function(self,t)return t end}
''')
lua.execute((KIT / "Code/70_SMRTK_Core.lua").read_text(encoding="utf-8-sig"))
lua.execute("function SMRTK.Page(...) end")
lua.execute((KIT / "Code/77_SMRTK_Stamper.lua").read_text(encoding="utf-8-sig"))
cases = []

def case(name, code):
    lua.execute(code)
    cases.append(name)
    print("PASS " + name)

print("$ python docs/agent/reports/SMRTK_P5_DESK.py")
print("HEAD pack=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
      + " testkit=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=KIT, text=True).strip())
case("strict schema and fresh raw normalization", r'''
local L=SMRTK.Stamper; local b=base(); b.buildings={building()}
local n=assert(L.Normalize(b)); b.buildings[1].dq=20; assert(n.buildings[1].dq==0)
b.v=99; assert(not L.Normalize(b)); b.v=1
b.grid={[2]={k='pipe',dq=0,dr=0}}; assert(not L.Normalize(b)); b.grid={}
b.buildings[1].dq=0/0; assert(not L.Normalize(b)); b.buildings[1].dq=0
b.buildings[1].dome=2; assert(not L.Normalize(b)); b.buildings[1].dome=nil
b.buildings[1].upgrades={2,1}; assert(not L.Normalize(b)); b.buildings[1].upgrades=nil
b.grid={{k='pipe',dq=0,dr=0},{k='pipe',dq=0,dr=0}}; assert(not L.Normalize(b)); b.grid={}
local called=false
setmetatable(b,{__index=function() called=true end,__pairs=function()called=true;error('meta ran')end})
local clean=assert(L.Normalize(b)); assert(not called and getmetatable(clean)==nil)
b.extra=function()end; assert(not L.Normalize(b)); b.extra=nil
b.buildings[1].upgrades=b; assert(not L.Normalize(b))
''')
case("deterministic literal export and round trip", r'''
local L=SMRTK.Stamper; local b=base(); b.buildings={building()}
local code=assert(L.Export(b)); local round=assert(load(code))(); assert(L.Export(round)==code)
assert(not L.Normalize(setmetatable({}, {__index=b})))
''')
case("clean plan 1 ordinary building with zero mutation", r'''
reset_world(); prohibit_mutation=true
local b=base(); b.buildings={building()}; local p=assert(SMRTK.Stamper.Plan(b,20,20))
assert(p.ready==1 and p.skipped==0 and mutations==0)
''')
case("clean plan 2 dome and interior with zero mutation", r'''
reset_world(); prohibit_mutation=true
local b=base(); b.buildings={building('DomeBasic'),building('Habitat',1,0,1)}
local p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==2 and p.skipped==0 and mutations==0)
''')
case("clean plan 3 flat grids: steps 1 has two captured nodes; isolated steps 0", r'''
reset_world(); prohibit_mutation=true
local b=base(); b.grid={{k='cable',dq=0,dr=0},{k='cable',dq=1,dr=0},{k='pipe',dq=4,dr=0}}
local p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==3 and p.skipped==0 and mutations==0)
assert(#native_calls==2 and native_calls[1].test and native_calls[1].steps==1 and native_calls[2].steps==0)
''')
case("terrain truth cannot pass occupancy, loose objects, height or bad parent", r'''
reset_world(); prohibit_mutation=true
local b=base(); b.buildings={building()}; object('Habitat',20,20)
local p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==0 and p.buildings[1].reason:find('occupied'))
reset_world(); loose={class='Worker'}; p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==0)
reset_world(); b.buildings={building('DomeBasic'),building('Habitat',3,0,1)}
p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==1 and p.skipped==1)
b.buildings[1].t='Habitat'; assert(not SMRTK.Stamper.Plan(b,20,20))
b.buildings={building('DomeBasic')}; heights={['21,20']=3}
p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==0)
''')
case("truthy line result with blocked second cell is rejected", r'''
reset_world(); prohibit_mutation=true; fail_cell=1
local b=base(); b.grid={{k='cable',dq=0,dr=0},{k='cable',dq=1,dr=0}}
local p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.ready==0 and p.skipped==2 and mutations==0)
''')
case("passages and suspended grids do not call a mutating or passage placer", r'''
reset_world(); prohibit_mutation=true
local b=base(); b.grid={{k='passage',dq=0,dr=0},{k='pipe',dq=2,dr=0,unsupported='suspended span'}}
local p=assert(SMRTK.Stamper.Plan(b,20,20)); assert(p.skipped==2 and #native_calls==0 and mutations==0)
''')
case("selected dome capture closes references and refuses name overwrite", r'''
reset_world(); prohibit_mutation=false; LocalStorage.smrtk_layouts={}
local dome=object('DomeBasic',20,20); object('Habitat',21,20); object('Habitat',60,60); SelectedObj=dome
local ok,f=SMRTK.Run('layout_capture_selected','dome_fixture'); assert(ok,f.reason)
assert(f.buildings==2); local saved=LocalStorage.smrtk_layouts.dome_fixture
assert(saved.buildings[2].dome==1 and saved.anchor.q==20)
local old=clipboard; assert(not SMRTK.Run('layout_capture_selected','dome_fixture')); assert(clipboard==old)
drain()
''')
case("oversized whole-map capture is atomic", r'''
reset_world(); LocalStorage.smrtk_layouts={}; for i=1,513 do object('Habitat',i,5) end
local previous=clipboard; local ok,f=SMRTK.Run('layout_capture_map','too_big')
assert(not ok and f.reason:find('exceeds') and LocalStorage.smrtk_layouts.too_big==nil and clipboard==previous)
''')
case("rectangle uses two clicks, armed service and lifecycle teardown", r'''
reset_world(); LocalStorage.smrtk_layouts={}; object('Habitat',20,20); object('Habitat',30,30)
assert(SMRTK.Arm('layout_target','rectangle','rect')); assert(SMRTK.click_capture)
assert(SMRTK.Fire('layout_target',point(19,19))); assert(not LocalStorage.smrtk_layouts.rect)
assert(SMRTK.Fire('layout_target',point(21,21))); assert(LocalStorage.smrtk_layouts.rect and #LocalStorage.smrtk_layouts.rect.buildings==1)
assert(not SMRTK.armed.layout_target and not SMRTK.click_capture)
assert(SMRTK.Arm('layout_target','rectangle','cancelled')); emit('SaveGameStart')
assert(not SMRTK.armed.layout_target and not SMRTK.click_capture and not LocalStorage.smrtk_layouts.cancelled)
drain()
''')
case("queued stamp dispatch owns only new sites and waits for its dome", r'''
reset_world(); prohibit_mutation=false; LocalStorage.smrtk_layouts={}; wait_for_dome=true
local b=base('stamp'); b.buildings={building('DomeBasic'),building('Habitat',1,0,1)}
LocalStorage.smrtk_layouts.stamp=b
local unrelated=object('OtherSite',80,80,{ConstructionSite=true,Building=true}); unrelated.shape={point(0,0)}
function unrelated:Complete() error('UNRELATED SITE COMPLETED') end
assert(SMRTK.Arm('layout_target','stamp','stamp')); assert(SMRTK.Fire('layout_target',point(20,20))); drain()
assert(IsValid(unrelated)); assert(SMRTK.Stamper.last.complete)
assert(#events==4 and events[1]=='place:DomeBasic' and events[2]=='complete:DomeBasic' and events[3]=='place:Habitat')
assert(not SMRTK.armed.layout_target and not SMRTK.click_capture and not SMRTK.Stamper.busy)
wait_for_dome=nil
''')
case("grid completion builds all owned groups before first removal", r'''
reset_world(); prohibit_mutation=false; LocalStorage.smrtk_layouts={}
local b=base('grid_stamp'); b.grid={{k='cable',dq=0,dr=0},{k='cable',dq=1,dr=0},{k='pipe',dq=4,dr=0}}
LocalStorage.smrtk_layouts.grid_stamp=b
assert(SMRTK.Arm('layout_target','stamp','grid_stamp')); assert(SMRTK.Fire('layout_target',point(20,20))); drain()
assert(SMRTK.Stamper.last.complete)
assert(events[1]=='group_complete:cable' and events[2]=='group_complete:pipe' and events[3]:find('done:'))
assert(CurrentMap.object_hex_grid:GetObject(20,20,'ElectricityGridElement'))
''')
case("paused stamp and cancelled queued work place nothing", r'''
reset_world(); LocalStorage.smrtk_layouts={}; local b=base('cancel'); b.buildings={building()}; LocalStorage.smrtk_layouts.cancel=b
assert(SMRTK.Arm('layout_target','stamp','cancel')); assert(SMRTK.Fire('layout_target',point(20,20))); paused=true; drain(); assert(mutations==0)
paused=false; assert(SMRTK.Arm('layout_target','stamp','cancel')); assert(SMRTK.Fire('layout_target',point(20,20))); emit('CurrentMapChange'); drain(); assert(mutations==0)
''')
case("engine-reported non-unwinding error stops later mutations", r'''
reset_world(); LocalStorage.smrtk_layouts={}; local b=base('error'); b.buildings={building(),building('Habitat',5,0)}; LocalStorage.smrtk_layouts.error=b; native_error=true
assert(SMRTK.Arm('layout_target','stamp','error')); assert(SMRTK.Fire('layout_target',point(20,20))); drain()
assert(mutations==1 and SMRTK.Stamper.last and not SMRTK.Stamper.last.complete)
assert(not SMRTK.armed.layout_target and not SMRTK.Stamper.busy)
''')
case("rectangle failure propagates and invalid names never acquire clicks", r'''
reset_world(); LocalStorage.smrtk_layouts={}
assert(not SMRTK.Arm('layout_target','rectangle','../bad')); assert(not SMRTK.click_capture)
assert(SMRTK.Arm('layout_target','rectangle','empty'))
assert(SMRTK.Fire('layout_target',point(10,10)))
local ok,f=SMRTK.Fire('layout_target',point(11,11))
assert(not ok and f.status=='REFUSED' and not SMRTK.click_capture and not SMRTK.armed.layout_target)
''')
case("upgrade state stays on retained buildings and declares colony unlocks", r'''
reset_world(); upgrade_calls=0
UIColony=CurrentMap.City.colony; UIColony.unlocked={}
function UIColony:IsUpgradeUnlocked(id) return self.unlocked[id] or false end
local o=object('Habitat',20,20); o.upgrade_ids={'Habitat_1'}
function o:ApplyUpgrade(tier,force)
  assert(tier==1 and force==true); upgrade_calls=upgrade_calls+1
  self.upgrades_built={Habitat_1=true}; UIColony.unlocked.Habitat_1=true
end
local b=base('state'); b.buildings={building()}; b.buildings[1].upgrades={1}
SMRTK.Stamper.last={map=CurrentMap,epoch=SMRTK.Stamper.epoch,complete=true,layout=b,objects={o}}
assert(SMRTK.Run('layout_upgrades_start')); drain(); assert(upgrade_calls==1)
assert(SMRTK.Run('layout_upgrades_start')); drain(); assert(upgrade_calls==1)
local found=false; for _,line in ipairs(logs) do if line:find('SMRTK_STAMP_STATE ') and line:find('colony_unlock_requests=1') then found=true end end; assert(found)
''')
case("save cancels queued state and invalidates previous stamp references", r'''
assert(SMRTK.Run('layout_upgrades_start')); emit('SaveGameStart'); drain()
assert(upgrade_calls==1 and not SMRTK.Stamper.last and not SMRTK.Run('layout_upgrades_start'))
''')
case("World follow-ups resolve late, pass explicit amounts and retain refusals", r'''
reset_world(); SMRTK.Stamper.last={map=CurrentMap,epoch=SMRTK.Stamper.epoch,complete=true,layout=base('follow'),objects={}}
assert(not SMRTK.Run('layout_funding'))
SMRTK.Action{id='funding',run=function(ctx,amount) assert(amount==500000000); return {amount=amount} end}
SMRTK.Action{id='spawn_colonists',run=function(ctx,amount) assert(amount==10); return false,'no suitable dome' end}
SMRTK.Action{id='fill_storages',run=function(ctx,...) assert(select('#',...)==0); return {count=4} end}
assert(SMRTK.Run('layout_funding')); assert(SMRTK.Run('layout_fill_storages'))
local ok,f=SMRTK.Run('layout_spawn_colonists'); assert(not ok and f.reason=='no suitable dome')
''')
print(f"P5 DESK: {len(cases)} contract falsifiers PASS; 3 clean synthetic plans; no native/game stamps run")
