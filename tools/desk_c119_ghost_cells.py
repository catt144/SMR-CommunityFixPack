#!/usr/bin/env python3
"""C119 load cleanup: execute Fix_GhostPowerCells.lua on synthetic loaded maps.

Run: python tools/desk_c119_ghost_cells.py

The module is loaded whole under lupa. This checks stale electricity cells,
tunnel and live-object preservation, off-module behavior, shape protection,
gridless retries across object classes, construction sites, and retry isolation.
The map grid, object index, map iterator, and connect operation are synthetic:
their engine implementations are C functions unavailable to the desk bench.
This does not prove game load ordering, C grid mutation, or save serialization.
"""

from pathlib import Path

import deskbench as db


MODULE = Path(db.REPO) / "Code" / "Fix_GhostPowerCells.lua"

FIXTURE = r'''
OnMsg = {}
LoadedMaps = {}
LOGS, ATTEMPTS = {}, {}
OWNER_LOOKUPS = 0
SupplyGridObject = {}
BaseSupplyGridTunnelConnectorObj = {ApplyRemoveSupplyTunnelMask=function() end}
ElectricityGridObject = {SetupElectricityElement=function() end}
TheExcavatorBase = {GetSupplyGridConnectionShapePoints=function() end}
OpenFarmBase = {GetSupplyGridConnectionShapePoints=function() end}
ElectricityGrid = {supply_resource="electricity"}
function IsValid(o) return type(o)=="table" and o.valid==true end
function IsBeingDestructed(o) return o.dying==true end
function IsKindOf(o, class) return o.kinds and o.kinds[class]==true or false end
function WorldToHex(o) return o.q, o.r end
function HexAngleToDirection() return 0 end
function HexRotate(q, r, direction) assert(direction==0); return q, r end
function band(a,b) return a & b end
function RealTime() return 100 end
function log(fmt, ...) LOGS[#LOGS+1]=string.format(fmt, ...) end
function HexGridGet(grid, q, r) return grid[r*grid.width+q] or 0 end
function HexGridSet(grid, q, r, value) grid[r*grid.width+q]=value end
function HexGridGetObject(grid,q,r,unused1,unused2,predicate)
  assert(unused1==nil and unused2==nil and type(predicate)=="function")
  for _,o in ipairs(grid.objects) do
    if o.q==q and o.r==r and predicate(o) then
      if grid==MAP_A.object_hex_grid and q==2 and r==0 then
        OWNER_LOOKUPS=OWNER_LOOKUPS+1
      end
      return o
    end
  end
end

local function grid(width) return {width=width} end
local function map(width, height)
  local m={hex_width=width, hex_height=height, objects={},
    supply_connection_grid={electricity=grid(width), water=grid(width)}}
  m.object_hex_grid={width=width,height=height,objects=m.objects}
  function m.object_hex_grid:size() return self.width,self.height end
  function m:MapForEach(scope,class,callback)
    assert(scope=="map")
    for _,o in ipairs(self.objects) do
      if o.kinds[class] then callback(o) end
    end
  end
  return m
end
local function add(m, name, q, r, class, grid_state, extras)
  local o={name=name,q=q,r=r,valid=true,kinds={[class]=true,SupplyGridObject=true},
    electricity={grid=grid_state}, parent_dome=false}
  if extras then for k,v in pairs(extras) do o[k]=v end end
  m.objects[#m.objects+1]=o
  return o
end
local function shape(q,r)
  return {{x=function() return q end,y=function() return r end}}
end

MAP_A=map(12,2)
MAP_B=map(4,1)
LoadedMaps={MAP_A,MAP_B}
local a=MAP_A.supply_connection_grid
HexGridSet(a.electricity,0,0,512)   -- no object: stale
HexGridSet(a.electricity,1,0,32768) -- tunnel endpoint: no object
HexGridSet(a.electricity,2,0,256)   -- live power owner
HexGridSet(a.electricity,3,0,128)   -- non-power object: stale
HexGridSet(a.electricity,4,0,64)    -- Excavator off-footprint cell
HexGridSet(a.electricity,6,0,64)    -- Open Farm off-footprint cell
HexGridSet(a.water,0,0,77)          -- water must be untouched
POWER=add(MAP_A,"power",2,0,"ElectricityGridObject",true)
NONPOWER=add(MAP_A,"nonpower",3,0,"Building",false)
NONPOWER.electricity=nil
EXCAVATOR=add(MAP_A,"excavator",5,0,"TheExcavatorBase",true,
  {GetSupplyGridConnectionShapePoints=function() return shape(-1,0) end})
FARM=add(MAP_A,"farm",7,0,"OpenFarmBase",true,
  {GetSupplyGridConnectionShapePoints=function() return shape(-1,0) end})
FAIL=add(MAP_A,"failed",8,0,"Cable",false,{fail=true})
CABLE=add(MAP_A,"cable",9,0,"Cable",false)
GENERATOR=add(MAP_A,"generator",10,0,"ElectricityGridObject",false)
SITE=add(MAP_A,"site",11,0,"ConstructionSite",false)
HexGridSet(MAP_B.supply_connection_grid.electricity,0,0,3)
DOME=add(MAP_B,"dome",1,0,"Dome",false)
PARENT={valid=true}
PASSAGE=add(MAP_B,"passage",2,0,"PassageBase",false,
  {domes_connected={{valid=true},{valid=true}},elements_under_construction={},
   shape_points={electricity={}},shape_connections={electricity={}},
   supply_tunnel_set=true,water={grid=true},parent_dome=PARENT})

function SupplyGridObject.SupplyGridConnectElement(self, element, grid_class, skin, force)
  assert(grid_class==ElectricityGrid and element==self.electricity)
  ATTEMPTS[#ATTEMPTS+1]={name=self.name,force=force,parent_dome=self.parent_dome}
  -- The synthetic C seam rejects a known adjacent stale cell. This forces the
  -- cleanup pass to finish before a retry can succeed.
  assert(HexGridGet(MAP_A.supply_connection_grid.electricity,0,0)==0, "stale neighbour")
  assert(HexGridGet(MAP_B.supply_connection_grid.electricity,0,0)==0, "second map stale")
  if self.fail then error("deliberate retry failure") end
  element.grid={connected=true}
end

SMRFixPack={Log=log}
function SMRFixPack.Require(_,specs)
  for _,spec in ipairs(specs) do
    if spec.class then
      assert(type(_G[spec.class])=="table",spec.class)
      if spec.method then assert(type(_G[spec.class][spec.method])=="function",spec.class.."."..spec.method) end
    elseif spec.global then assert(type(_G[spec.global])=="function",spec.global) end
    if spec.test then assert(spec.test(),spec.reason) end
  end
end
function SMRFixPack.Register(id,def)
  assert(id=="GhostPowerCells")
  local err=def.apply()
  assert(not err,tostring(err))
end
function SMRFixPack.WhenActive(id,fn)
  assert(id=="GhostPowerCells")
  return function(...) if ACTIVE then return fn(...) end end
end

function snapshot_keys()
  local result={}
  for _,m in ipairs(LoadedMaps) do
    for _,o in ipairs(m.objects) do
      local keys={}
      for k in pairs(o) do keys[k]=true end
      result[o]=keys
    end
  end
  return result
end
function same_keys(before)
  for o,keys in pairs(before) do
    for k in pairs(o) do if not keys[k] then return false,o.name.." gained "..k end end
    for k in pairs(keys) do if o[k]==nil then return false,o.name.." lost "..k end end
  end
  return true
end
function attempt_count(name)
  local n=0
  for _,a in ipairs(ATTEMPTS) do if a.name==name then n=n+1 end end
  return n
end
'''


def runtime(source: str, active: bool):
    rt = db.lua_runtime()
    db.load_at(rt, f"ACTIVE={'true' if active else 'false'}\n" + FIXTURE, "=C119_fixture")
    db.load_at(rt, source, "=Code/Fix_GhostPowerCells.lua")
    return rt


def main():
    bench = db.Bench("C119 ghost power-cell cleanup")
    source = db.read(str(MODULE))
    check = bench.check

    fixed = runtime(source, True)
    fixed.execute("BEFORE=snapshot_keys(); OnMsg.PostLoadGame()")
    eval_fixed = fixed.eval
    check("stale power cells clear on both loaded maps",
          eval_fixed("HexGridGet(MAP_A.supply_connection_grid.electricity,0,0)==0 and "
                     "HexGridGet(MAP_A.supply_connection_grid.electricity,3,0)==0 and "
                     "HexGridGet(MAP_B.supply_connection_grid.electricity,0,0)==0"))
    check("tunnel-bit cell without an object remains",
          eval_fixed("HexGridGet(MAP_A.supply_connection_grid.electricity,1,0)==32768"))
    check("live electricity-object cell remains",
          eval_fixed("HexGridGet(MAP_A.supply_connection_grid.electricity,2,0)==256"))
    check("measured global object lookup visits the live power-owner cell",
          eval_fixed("OWNER_LOOKUPS>0 and MAP_A.object_hex_grid.GetObject==nil"))
    check("off-footprint Excavator and Open Farm cells remain",
          eval_fixed("HexGridGet(MAP_A.supply_connection_grid.electricity,4,0)==64 and "
                     "HexGridGet(MAP_A.supply_connection_grid.electricity,6,0)==64"))
    check("water connection cells remain untouched",
          eval_fixed("HexGridGet(MAP_A.supply_connection_grid.water,0,0)==77"))
    check("gridless cable, generator, dome and construction site reconnect",
          eval_fixed("CABLE.electricity.grid and GENERATOR.electricity.grid and "
                     "DOME.electricity.grid and SITE.electricity.grid and "
                     "attempt_count('cable')==1 and attempt_count('generator')==1 and "
                     "attempt_count('dome')==1 and attempt_count('site')==1"))
    check("built passage retry uses forced physical connection and restores dome",
          eval_fixed("PASSAGE.electricity.grid and PASSAGE.parent_dome==PARENT and "
                     "ATTEMPTS[#ATTEMPTS].name=='passage' and "
                     "ATTEMPTS[#ATTEMPTS].force=='force' and "
                     "ATTEMPTS[#ATTEMPTS].parent_dome==false"))
    check("failed retry leaves its grid empty and does not stop later retries",
          eval_fixed("FAIL.electricity.grid==false and attempt_count('failed')==1 and "
                     "CABLE.electricity.grid and SITE.electricity.grid"))
    check("one load log reports exact scan and retry counts",
          eval_fixed("#LOGS==1 and string.find(LOGS[1]," 
                     "'maps=2 cleared=3 tunnel_skipped=1 shape_protected=2 "
                     "reconnected=5 retry_failed=1 unbuilt_skipped=0 map_failed=0',1,true)~=nil"))
    check("repair adds no fields to world objects", eval_fixed("same_keys(BEFORE)"))
    check("module declares no save hook or persisted variable",
          all(token not in source for token in ("OnMsg.Save", "GameVar(", "MapVar(", "AddGameVar(")))

    off = runtime(source, False)
    off.execute("OnMsg.PostLoadGame()")
    check("disabled module leaves stale cells and gridless objects alone",
          off.eval("HexGridGet(MAP_A.supply_connection_grid.electricity,0,0)==512 and "
                   "HexGridGet(MAP_B.supply_connection_grid.electricity,0,0)==3 and "
                   "CABLE.electricity.grid==false and #ATTEMPTS==0 and #LOGS==0"))

    needle = "if band(cell, TUNNEL_MASK) ~= 0 then"
    check("mutant target occurs once", source.count(needle) == 1)
    if source.count(needle) == 1:
        mutant = runtime(source.replace(needle, "if false then", 1), True)
        mutant.execute("OnMsg.PostLoadGame()")
        check("no-tunnel-skip mutant FAILS the tunnel preservation demand",
              mutant.eval("HexGridGet(MAP_A.supply_connection_grid.electricity,1,0)==0"))

    return bench.finish("ALL DEMANDS HELD -- C119 load cleanup discriminates the tunnel-guard mutant.")


if __name__ == "__main__":
    raise SystemExit(main())
