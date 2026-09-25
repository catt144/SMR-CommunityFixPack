#!/usr/bin/env python3
"""C114 access fallback against archived 1.1.1.405907 Lua.

Run: python tools/desk_c114_hub_access.py

The native HasLocalAccess body and its two file-local helpers are extracted
verbatim. The native dome and workforce range predicates and service admission
predicate are extracted too. Geometry, maps, object identity, and registration
are explicit desk seams. This checks decisions, not a game's path choice or a
colonist's successful entry after access is granted.
"""
import hashlib
import os
from pathlib import Path

import deskbench as db


BUILD = "1.1.1.405907"
db.TREES[BUILD] = os.path.join(
    os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
    BUILD, "Src",
)
HELPER = Path(db.REPO) / "Code" / "Hubset_OnHubNow.lua"
MODULE = Path(db.REPO) / "Code" / "Fix_HubLocalAccess.lua"


PRELUDE = r'''
Colonist = {}
CommandObject = {}
Workforce = {}
Dome = {dome_network = false}
PassageHubBase = {hub_domes = false}
ServiceBase = {}
ServiceFailure = {None = 0, NotFound = 1, CanServiceFailed = 2, Closed = 3, Full = 4}
empty_table = {}
g_Consts = {DefaultOutsideWorkplacesRadius = 20}

function IsValid(o) return type(o) == "table" and o.valid == true end
function IsValidPos(o) return IsValid(o) and o.valid_pos ~= false end
function IsKindOf(o, kind)
  return type(o) == "table" and (o.kind == kind or type(o.parents) == "table" and o.parents[kind] == true)
end
function IsBeingDestructed(o) return o.destroyed == true end
function IsLRTransportAvailable() return true end
function CreateColonistTransportTask(c, source, home)
  c.rescue_bookings = c.rescue_bookings + 1
  local task = {dest_dome = home, shuttle = false}
  c.transport_task = task
  return task
end
function CommandObject.SetCommand(c, command)
  c.command = command
  return command
end
function ResolveMap(o) return type(o) == "table" and o.map or nil end
function IsSameMap(a, b) return ResolveMap(a) == ResolveMap(b) end
function GetObjectHexGrid(o) return o.map.object_hex_grid end
function GetTopmostParent(o) return o end
function WorldToHex(o) return o.q, o.r end
function HexAxialDistance(a, b)
  local dq, dr = a.q - b.q, a.r - b.r
  return (math.abs(dq) + math.abs(dr) + math.abs(dq + dr)) / 2
end
local function key(q, r) return tostring(q) .. ":" .. tostring(r) end
function HexGridGetObject(grid, q, r, kind)
  if kind == "PassageHub" then return grid.hubs[key(q, r)] end
end
function GetDomeAtHex(grid, q, r) return grid.domes[key(q, r)] end
function GetDomeAtPoint(grid, o) return GetDomeAtHex(grid, o.q, o.r) end
function IsObjInDome(o) return IsValid(o) and o.parent_dome or false end
function FindNearestObject(communities, unit)
  local best, best_dist
  for _, c in ipairs(communities) do
    local dist = HexAxialDistance(c, unit)
    if not best_dist or dist < best_dist then best, best_dist = c, dist end
  end
  return best
end
table.find = function(t, value)
  for i, v in ipairs(t) do if v == value then return i end end
end
function Dome:GetMap() return self.map end
function Dome:GetOutsideWorkplacesDist() return 20 end
function Dome:GetClusterDomes() return self.cluster or {} end
setmetatable(Dome, {__index = Workforce})
function Colonist:IsValidPos() return self.valid_pos ~= false end
function Colonist:GetMapSlot() return self.map.slot end
function Colonist:IsServiceMarkedUnreachable() return false end
function Colonist:HasMember(name) return name == "Idle_TransportDestination" end
function Colonist:Idle_TransportDestination() return self.dome end
function Colonist:GetTransportRoute() return nil, nil end
setmetatable(Colonist, {__index = {}})

function make_case()
  local map = {slot = 1, object_hex_grid = {hubs = {}, domes = {}}}
  local function dome(q)
    return setmetatable({kind = "Dome", valid = true, q = q, r = 0, map = map,
      dome_network = {}, cluster = {}, parents = {Building = true}}, {__index = Dome})
  end
  local source, target, small, unrelated = dome(-30), dome(30), dome(10), dome(50)
  source.dome_network[target] = true
  source.dome_network[source] = true
  local hub = {kind = "PassageHubBase", parents = {PassageHubBase = true},
    valid = true, q = 0, r = 0, map = map, hub_domes = {source},
    connected_passages = {}, draining_passages = {}}
  hub.hub_domes[source] = 1
  function hub:GetMap() return self.map end
  map.object_hex_grid.hubs["0:0"] = hub
  map.object_hex_grid.domes["-30:0"] = source
  map.object_hex_grid.domes["30:0"] = target
  map.object_hex_grid.domes["10:0"] = small
  map.object_hex_grid.domes["50:0"] = unrelated
  local c = setmetatable({kind = "Colonist", valid = true, q = 0, r = 0,
    map = map, city = {labels = {Community = {source}}}, dome = source,
    holder = false, passage_hub = false, traversing_passage = false,
    traits = {}, rescue_bookings = 0, command = "Roam"}, {__index = Colonist})
  local p = {kind = "PassageBase", valid = true, domes_connected = {hub, source},
    traversing_colonists = {c}, map = map}
  hub.connected_passages[p] = true
  return {map = map, source = source, target = target, small = small,
    unrelated = unrelated, hub = hub, colonist = c, passage = p}
end
function make_building(map, dome, q)
  return {kind = "Building", parents = {Building = true}, valid = true,
    map = map, parent_dome = dome, q = q, r = 0}
end
function make_service(map, dome)
  local service = make_building(map, dome, dome.q)
  service.HasFreeVisitSlots = function() return false end
  service.CanService = function() return true end
  return setmetatable(service, {__index = ServiceBase})
end

SMRFixPack = {}
function SMRFixPack.Require(_, checks)
  for _, c in ipairs(checks) do
    local ok
    if c.class and c.method then
      ok = type(_G[c.class]) == "table" and type(_G[c.class][c.method]) == "function"
    elseif c.class then
      ok = type(_G[c.class]) == "table"
    elseif c.global then
      ok = type(_G[c.global]) == (c.kind or "function")
    elseif c.path then
      local obj = _G
      for _, part in ipairs(c.path) do obj = type(obj) == "table" and obj[part] end
      ok = type(obj) == (c.kind or "function")
    elseif c.test then
      ok = c.test() and true or false
    end
    if not ok then return c.reason or "required game shape absent" end
  end
end
function SMRFixPack.Register(id, def)
  assert(id == "HubLocalAccess")
  SMRFixPack.result = def.apply()
end
'''


def load_body(rt, rel, pattern):
    source, first, last = db.body(rel, pattern, tree=BUILD)
    db.load_at(rt, source, "=" + rel, first)
    return first, last


def runtime(patched, broken_shape=None):
    rt = db.lua_runtime()
    db.load_at(rt, PRELUDE, "=c114_fixture")
    native, begin, end = db.body("Lua/Units/ColonistTransport.lua",
                                 r"^function Colonist:HasLocalAccess\(", tree=BUILD)
    assert (begin, end) == (270, 300)
    assert hashlib.sha256(native.encode()).hexdigest() == (
        "3249abc15338e94695a7afe6336c9f065f9d93dd6a9cc84574b16aad0edd3e24"
    )
    load_body(rt, "Lua/Buildings/Workforce.lua", r"^function Workforce:IsBuildingInWorkRange\(")
    load_body(rt, "Lua/Buildings/Dome.lua", r"^function Dome:IsBuildingInWorkRange\(")
    load_body(rt, "Lua/Buildings/Dome.lua", r"^function IsBuildingInDomeRange\(")
    load_body(rt, "Lua/Buildings/Dome.lua", r"^function IsUnitInDome\(")
    load_body(rt, "Lua/Units/ColonistTransport.lua", r"^function IsUnitInDomeRange\(")
    source, first, last = db.span("Lua/Units/ColonistTransport.lua", (
        r"^local function IsDestinationInCommunityRange\(",
        r"^local function HasAccessViaCommunity\(",
        r"^function Colonist:HasLocalAccess\(",
    ), tree=BUILD)
    db.load_at(rt, source, "=Lua/Units/ColonistTransport.lua", first)
    rt.execute("NATIVE_ACCESS = Colonist.HasLocalAccess")
    load_body(rt, "Lua/Units/ColonistTransport.lua", r"^function Colonist:SetCommand\(")
    load_body(rt, "Lua/ServiceBase.lua", r"^function ServiceBase:CanBeUsedBy\(")
    if broken_shape:
        assert broken_shape in ("hub", "network")
        rt.execute("PassageHubBase.hub_domes = true" if broken_shape == "hub"
                   else "Dome.dome_network = true")
    if patched:
        db.load_at(rt, db.read(str(HELPER)), "=Code/Hubset_OnHubNow.lua")
        db.load_at(rt, db.read(str(MODULE)), "=Code/Fix_HubLocalAccess.lua")
    return rt


def scenario(rt, setting, target="target", home_relative=False):
    case = rt.eval("make_case()")
    c, h, p = case["colonist"], case["hub"], case["passage"]
    if setting == "flight":
        c["traversing_passage"] = p
        c["q"] = 5  # passage hex: native target distance is still over 20
    elif setting == "hub":
        c["holder"] = h
    elif setting == "marker_hub":
        c["passage_hub"] = h
    elif setting == "stale_holder":
        c["holder"] = h
        c["q"] = 5
    elif setting == "stale_marker":
        c["passage_hub"] = h
        c["q"] = 5
    elif setting == "disconnected":
        c["traversing_passage"] = p
        c["q"] = 5
        h["connected_passages"][p] = None
    elif setting == "draining":
        c["traversing_passage"] = p
        c["q"] = 5
        h["connected_passages"][p] = None
        h["draining_passages"][p] = True
    elif setting == "unlisted":
        c["traversing_passage"] = p
        c["q"] = 5
        p["traversing_colonists"] = rt.table()
    elif setting == "no_endpoint":
        c["holder"] = h
        h["hub_domes"][case["source"]] = 0
    elif setting == "ground":
        c["q"] = 5
    else:
        raise ValueError(setting)
    destination = case[target]
    if target == "outdoor":
        destination = rt.table_from({"kind": "Building", "valid": True,
                                     "q": 30, "r": 0, "map": case["map"]})
    return case, destination, bool(c.HasLocalAccess(c, destination, case["source"] if home_relative else None))


def main():
    bench = db.Bench("C114 hub local access -- archived 1.1.1.405907")
    native, fixed = runtime(False), runtime(True)
    bench.check("module registered and applied", fixed.eval("SMRFixPack.result == nil"))
    for shape in ("hub", "network"):
        declined = runtime(True, broken_shape=shape)
        bench.check("changed " + shape + " shape declines without wrapper",
                    declined.eval("type(SMRFixPack.result) == 'string' "
                                  "and Colonist.HasLocalAccess == NATIVE_ACCESS"))
    for rt, patched in ((native, False), (fixed, True)):
        name = "fix on" if patched else "module removed"
        _, _, result = scenario(rt, "flight")
        bench.check(name + ": large-dome in-flight access", result == patched)
        _, _, result = scenario(rt, "hub")
        bench.check(name + ": standing on hub", result == patched)
        _, _, result = scenario(rt, "marker_hub")
        bench.check(name + ": dumped on hub retains access", result == patched)
        _, _, result = scenario(rt, "hub", target="small")
        bench.check(name + ": small dome native true retained", result)
        case, _, _ = scenario(rt, "hub")
        colonist = case["colonist"]
        colonist.SetCommand(colonist, "Idle")
        bench.check(name + ": natural Idle rescue booking follows access",
                    colonist["rescue_bookings"] == (0 if patched else 1)
                    and colonist["command"] == ("Idle" if patched else "Transport"))
    _, _, result = scenario(fixed, "draining")
    bench.check("fix on: connected draining passage still grants access", result)
    for setting, target, home, label in (
        ("hub", "unrelated", False, "unrelated destination"),
        ("stale_holder", "target", False, "stale holder off hub"),
        ("stale_marker", "target", False, "stale marker off hub"),
        ("disconnected", "target", False, "cut passage"),
        ("unlisted", "target", False, "stale flight flag without list membership"),
        ("no_endpoint", "target", False, "removed last dome connection"),
        ("hub", "target", True, "home-relative query"),
        ("hub", "outdoor", False, "outdoor workplace"),
    ):
        _, _, result = scenario(fixed, setting, target, home)
        bench.check("fix on: " + label + " remains denied", not result)
    case, target, _ = scenario(fixed, "hub")
    target["map"] = fixed.eval("{slot=2, object_hex_grid={hubs={}, domes={}}}")
    bench.check("fix on: cross-map destination denied",
                not bool(case["colonist"].HasLocalAccess(case["colonist"], target)))
    case, _, _ = scenario(fixed, "hub")
    service = fixed.eval("make_service")(case["map"], case["target"])
    granted = bool(case["colonist"].HasLocalAccess(case["colonist"], service))
    bench.check("native service policy still refuses a full service after access grant",
                granted and service.CanBeUsedBy(service, case["colonist"])[0] is False)
    # The native SetCommand body performs the train search only after access is
    # false (ColonistTransport.lua:416-436); this exercises that gate, not PF.
    case, _, _ = scenario(fixed, "hub")
    station = fixed.eval("make_building")(case["map"], case["unrelated"], 50)
    train_access = bool(case["colonist"].HasLocalAccess(case["colonist"], station))
    bench.check("unrelated station destination leaves train-search gate open",
                not train_access)
    return bench.finish()


if __name__ == "__main__":
    raise SystemExit(main())
