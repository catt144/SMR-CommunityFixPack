#!/usr/bin/env python3
"""C121 Universal Depot Seeds toggle against archived 1.1.1.405907 Lua: the stale cache, the unlock refresh and the load heal.

Run: python tools/desk_c121_depot_seeds.py

Nothing here ran in a game. A PASS shows that Code/Fix_UniversalDepotSeedsToggle.lua
discriminates on the shipped bodies in this fixture; it does not show a colony
produces the fixture, and it says nothing about whether drones deliver Seeds.

SHIPPED (extracted from the archived 1.1.1.405907 tree, loaded under the real file
name and line, never retyped):
  * CommonLua/Features/LockablePreset.lua from line 1 through GetLockablePresetOwners
    (the class defs, ResolveEmptyOwner, the reason machinery AddPresetLockStateReason /
    RemovePresetLockStateReason / lRecalcLockState / lSetPresetLockedState, which posts
    Msg("PresetLockStateChanged"), GetPresetLockStateAndText, ResetLockablePresetState)
    and RemovePresetLockedState;
  * Lua/MarsGameEffects.lua Effect_RemovePresetLockedState:OnApplyEffect, applied to
    the UtilityCrops effect block of Data/Tech.lua (Class/LockState/PresetId read from
    the shipped PlaceObj), so Seeds is unhidden by the same call chain as research;
  * Data/Resource.lua whole (every Resource preset: Seeds ships LockState "hidden");
  * the Resource class def and Resource:OnLockStateChanged (ClassDef-Resources.generated.lua);
  * CommonLua/Libs/Resources/Resources.lua from "Preprocessing of resource presets"
    through PreProcessResources (ResourceCmp, ResourceInGroupIds, the InitResPreProcess
    / PreProcessRemoveGroup handlers), and UpdateResourceGlobalVars;
  * Lua/Resources.lua lines 1 through GroupResourcesForIP (ResourcesInfopanelGroups via
    the PreProcessResource handler, GroupResourcesForSelector, GroupResourcesForIP);
  * Lua/Buildings/StorageDepot.lua: the UniversalStorageDepotBase class def, :Init,
    :RebuildInfopanel, :SetDepotEntity, :GameInit (the :461 cache line), and
    :SetStorableResources (:509-519); Lua/BuildingTemplate/UniversalStorageDepot.generated.lua whole;
  * Lua/Buildings/MultiResourceDepot.lua vanilla OnMsg.PresetLockStateChanged (:470-475),
    registered before the pack's handler as game code loads first;
  * Code/00_Core.lua whole (Register / Require / WhenActive NOT stubbed) and the module whole.

RETYPED OR STUBBED, and whether each can DECIDE an outcome (the F59 rule):
  * Engine tolerances beyond deskbench.ENGINE_SHIMS: next(nil) returns nil (the shipped
    lClearLockState, LockablePreset.lua:392, calls it on a fresh owner on every new game);
    table.copy, table.create_add_unique, table.common_keys, sorted_pairs.
  * Class system (C-side in the engine): DefineClass files the def into _G and g_Classes;
    build_classes() gives each def `class`, parent lookup through __parents, and property
    defaults from `properties`. IsKindOf walks __parents. It DECIDES the Resource filter
    and the Player owner check; it answers exactly the declared hierarchy.
  * Stub classes: PropertyObject, InitDone, Preset (group "Default", SortKey 0, the
    Preset.lua:67 default), PresetWithTags, Player (-> LockablePresetOwner), StorageDepot
    (no-op HasSpot/GetEntity/ChangeEntity/SetCount: visuals only), Tech (-> LockablePreset,
    PresetClass "Tech"; the real Tech class is not loaded), RocketBase (-> UniversalStorageDepotBase
    only; the real class has 13 parents, RocketBase.lua:2), and ModUniversalDepot, a
    HYPOTHETICAL mod subclass of UniversalStorageDepot (no shipped class derives from it).
  * PlaceObj files a preset into Presets[PresetClass][group] (file order) and its GlobalMap,
    as Preset:Register does. Group order is file order, not the engine's sort; the one
    order that matters (ResourcesInfopanelGroups: Basic, Advanced, Other) is one group.
  * A new game's lock init is ResetLockablePresetState per Resource preset, for UIPlayer.
  * Depot construction: Init -> SetStorableResources (as CreateResourceRequests :522 calls it)
    -> the one line of CreateResourceRequests GameInit reads (stockpiled_amount = {}, :528)
    -> GameInit. IsGameRuleActive is false (no rules): it DECIDES whether Seeds is appended
    (NoTerraforming); false is the ordinary game the report is about. HintDisable no-op.
  * AllMapsForEach(true, class..., fn) walks the fixture's objects that are IsKindOf the
    class (descendants included, as the engine's class filter does) and IsValid.
  * IsValid: `valid == true`. RebuildInfopanel (global, UI): counts calls per object.
    ModLog captures log lines. Msg/OnMsg: handlers in registration order.
  * GroupResourcesForIP is wrapped by a call counter (instrumentation only; it returns the
    real body's result unchanged) so a leg can show a handler ran or did not.
  * Effect_RemovePresetLockedState property defaults (Group false, Reason false) retyped
    from its DefineClass (MarsGameEffects.lua:751-763).
Not loaded: TechTree.lua:1268 and XPresetMap.lua:73 handlers (they touch no depot, per C121).
"""
import os
import pathlib
import re
import subprocess
import sys

import deskbench as db
from luafn import read_lines, find_bodies

ARCH = pathlib.Path(os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
                    "1.1.1.405907", "Src")
MODULE_REL = "Code/Fix_UniversalDepotSeedsToggle.lua"
MODULE = pathlib.Path(db.REPO, MODULE_REL)
FIX_ID = "UniversalDepotSeedsToggle"


def _lines(rel):
    return read_lines(str(ARCH / rel))


def _one(lines, rel, pat):
    hits = find_bodies(lines, pat)
    assert len(hits) == 1, (rel, pat, len(hits))
    return hits[0]


def fn(rel, pat):
    lines = _lines(rel)
    s, e = _one(lines, rel, pat)
    return (rel, s + 1, "\n".join(lines[s:e + 1]))


def from_top_through(rel, pat):
    lines = _lines(rel)
    _, e = _one(lines, rel, pat)
    return (rel, 1, "\n".join(lines[:e + 1]))


def marker_through(rel, marker, pat):
    lines = _lines(rel)
    starts = [i for i, l in enumerate(lines) if l.strip() == marker]
    assert len(starts) == 1, (rel, marker, len(starts))
    _, e = _one(lines, rel, pat)
    return (rel, starts[0] + 1, "\n".join(lines[starts[0]:e + 1]))


def table_block(rel, pat):
    """A top-level `DefineClass.X = {` block, to the first column-0 `}`."""
    lines = _lines(rel)
    s, _ = _one(lines, rel, pat)
    for j in range(s + 1, len(lines)):
        if lines[j] == "}":
            return (rel, s + 1, "\n".join(lines[s:j + 1]))
    raise AssertionError((rel, pat, "no closing }"))


def whole(rel):
    return (rel, 1, "\n".join(_lines(rel)))


def seeds_effect():
    """The UtilityCrops Effect_RemovePresetLockedState block for Seeds (Data/Tech.lua)."""
    rel = "Data/Tech.lua"
    lines = _lines(rel)
    for i, l in enumerate(lines):
        if "PlaceObj('Effect_RemovePresetLockedState'" in l:
            j = i + 1
            while not lines[j].strip().startswith("})"):
                j += 1
            block = lines[i:j + 1]
            if any('PresetId = "Seeds"' in b for b in block) and any('Class = "Resource"' in b for b in block):
                block[-1] = block[-1].rstrip().rstrip(",")
                return (rel, i + 1, "SEEDS_EFFECT = " + "\n".join(block).lstrip())
    raise AssertionError("no Seeds Effect_RemovePresetLockedState in Data/Tech.lua")


LP = "CommonLua/Features/LockablePreset.lua"
SD = "Lua/Buildings/StorageDepot.lua"
CLASS_CHUNKS = [
    from_top_through(LP, r"^function GetLockablePresetOwners\("),
    fn(LP, r"^function RemovePresetLockedState\("),
    table_block("CommonLua/Libs/Resources/ClassDefs/ClassDef-Resources.generated.lua", r"^DefineClass\.Resource = "),
    fn("CommonLua/Libs/Resources/ClassDefs/ClassDef-Resources.generated.lua", r"^function Resource:OnLockStateChanged\("),
    marker_through("CommonLua/Libs/Resources/Resources.lua", "----- Preprocessing of resource presets",
                   r"^function PreProcessResources\("),
    fn("CommonLua/Libs/Resources/Resources.lua", r"^function UpdateResourceGlobalVars\("),
    from_top_through("Lua/Resources.lua", r"^function GroupResourcesForIP\("),
    table_block(SD, r"^DefineClass\.UniversalStorageDepotBase = "),
    fn(SD, r"^function UniversalStorageDepotBase:Init\("),
    fn(SD, r"^function UniversalStorageDepotBase:RebuildInfopanel\("),
    fn(SD, r"^function UniversalStorageDepotBase:SetDepotEntity\("),
    fn(SD, r"^function UniversalStorageDepotBase:GameInit\("),
    fn(SD, r"^function UniversalStorageDepotBase:SetStorableResources\("),
    whole("Lua/BuildingTemplate/UniversalStorageDepot.generated.lua"),
    fn("Lua/Buildings/MultiResourceDepot.lua", r"^function OnMsg\.PresetLockStateChanged\("),
    fn("Lua/MarsGameEffects.lua", r"^function Effect_RemovePresetLockedState:OnApplyEffect\("),
]
DATA_CHUNKS = [whole("Data/Resource.lua"), seeds_effect()]

PRELUDE = r'''
-- next(nil) returns nil, like the engine's ipairs/pairs tolerance: the shipped
-- lClearLockState (LockablePreset.lua:392) calls next(group_entries) on an owner
-- with no entry yet, on every new game
local _next = next
function next(t, k) if t == nil then return nil end return _next(t, k) end
FirstLoad = true
LOGS = {}
ModLog = function(s) LOGS[#LOGS+1] = s end
CreateRealTimeThread = function(f) return {fn=f} end
T = function(id, text) if type(id) == "table" then return id end if text == nil then return id end return text end
TLookupTag = function(s) return s end
set = function(...) return {...} end
range = function(a, b) return {a, b} end
point = function(x, y, z) return {x, y, z} end
const = {ResourceScale = 1000, rfStorageDepot = 1, rfSpecialSupplyPairing = 2}
function table.copy(t, deep)
  if type(t) ~= "table" then return t end
  local r = {} for k, v in pairs(t) do r[k] = (deep and type(v) == "table") and table.copy(v, deep) or v end return r
end
function table.create_add_unique(t, v) t = t or {} for _, x in ipairs(t) do if x == v then return t end end t[#t+1] = v return t end
function table.common_keys(a, b) for k in pairs(a or {}) do if b[k] ~= nil then return true end end return false end
function sorted_pairs(t)
  if type(t) ~= "table" then return function() end end
  local keys = {} for k in pairs(t) do keys[#keys+1] = k end
  table.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
  local i = 0
  return function() i = i + 1 local k = keys[i] if k ~= nil then return k, t[k] end end
end

-- messages ------------------------------------------------------------------
local handlers = {}
OnMsg = setmetatable({}, {__newindex = function(_, ev, f)
  handlers[ev] = handlers[ev] or {} table.insert(handlers[ev], f) end})
MSGS = {}
function Msg(ev, ...)
  if ev == "PresetLockStateChanged" then
    local p = ...
    MSGS[#MSGS+1] = (p and (p.PresetClass or p.class) or "?") .. ":" .. tostring(p and p.id)
  end
  for _, f in ipairs(handlers[ev] or {}) do f(...) end
end

-- class system (C-side in the engine) ----------------------------------------
g_Classes = {}
CLASS_ORDER = {}
DefineClass = setmetatable({}, {__newindex = function(_, name, def)
  rawset(_G, name, def) g_Classes[name] = def CLASS_ORDER[#CLASS_ORDER+1] = name end})
function UndefineClass() end
local function kind(cname, name)
  if cname == name then return true end
  local d = g_Classes[cname]
  if not d then return false end
  for _, p in ipairs(rawget(d, "__parents") or {}) do if kind(p, name) then return true end end
  return false
end
function IsKindOf(o, name) return type(o) == "table" and type(o.class) == "string" and kind(o.class, name) end
function build_classes()
  for _, name in ipairs(CLASS_ORDER) do
    local def = g_Classes[name]
    rawset(def, "class", name)
    setmetatable(def, {__index = function(_, k)
      for _, p in ipairs(rawget(def, "__parents") or {}) do
        local pd = g_Classes[p]
        if pd then local v = pd[k] if v ~= nil then return v end end
      end
    end})
  end
  for _, name in ipairs(CLASS_ORDER) do
    local def = g_Classes[name]
    for _, prop in ipairs(rawget(def, "properties") or {}) do
      if prop.id and prop.default ~= nil and rawget(def, prop.id) == nil then rawset(def, prop.id, prop.default) end
    end
  end
end
function new(cls, t) return setmetatable(t or {}, {__index = g_Classes[cls]}) end

DefineClass.PropertyObject = {}
DefineClass.InitDone = {}
DefineClass.Preset = {__parents = {"PropertyObject"}, group = "Default", SortKey = 0, id = ""}
DefineClass.PresetWithTags = {__parents = {"Preset"}}
DefineClass.Player = {__parents = {"LockablePresetOwner"}}
DefineClass.StorageDepot = {}
function StorageDepot:HasSpot() return false end
function StorageDepot:GetEntity() return "" end
function StorageDepot:ChangeEntity() end
function StorageDepot:SetCount() end
DefineClass.Tech = {__parents = {"LockablePreset"}, PresetClass = "Tech"}
DefineClass.RocketBase = {__parents = {"UniversalStorageDepotBase"}}
DefineClass.ModUniversalDepot = {__parents = {"UniversalStorageDepot"}}
Effect_RemovePresetLockedState = {Group = false, Reason = false, LockState = "enabled"}

-- presets ---------------------------------------------------------------------
Presets = {}
function PlaceObj(cls, t)
  if cls == "Effect_RemovePresetLockedState" then return setmetatable(t, {__index = Effect_RemovePresetLockedState}) end
  local def = g_Classes[cls]
  local o = new(cls, t)
  local pc = def.PresetClass or cls
  local groups = Presets[pc] or {} Presets[pc] = groups
  local g = groups[o.group]
  if not g then g = {} groups[#groups+1] = g groups[o.group] = g end
  g[#g+1] = o g[o.id] = o
  if def.GlobalMap then _G[def.GlobalMap] = _G[def.GlobalMap] or {} _G[def.GlobalMap][o.id] = o end
  return o
end
function InitResListClasses() end

-- engine surface the depot bodies touch ------------------------------------------
function IsGameRuleActive() return false end
function HintDisable() end
function GetEntitySpotPos() return point(0, 0, 0) end
function IsValid(o) return type(o) == "table" and o.valid == true end
OBJECTS = {}
function AllMapsForEach(_, ...)
  local args = {...}
  local f = table.remove(args)
  for _, o in ipairs(OBJECTS) do
    if IsValid(o) then
      for _, c in ipairs(args) do if IsKindOf(o, c) then f(o) break end end
    end
  end
end
REBUILDS = {}
function RebuildInfopanel(o) REBUILDS[o] = (REBUILDS[o] or 0) + 1 end
'''

POST = r'''
UIPlayer = new("Player")
UIPlayer:Init()
local real_group = GroupResourcesForIP
GROUP_CALLS = 0
GroupResourcesForIP = function(...) GROUP_CALLS = GROUP_CALLS + 1 return real_group(...) end

HANDLE = 0
function new_depot(cls, force)
  HANDLE = HANDLE + 1
  local o = new(cls, {handle = HANDLE, valid = true})
  o:Init()
  o:SetStorableResources(force)
  o.stockpiled_amount = o.stockpiled_amount or {}
  o:GameInit()
  OBJECTS[#OBJECTS+1] = o
  return o
end
function new_game()
  for _, group in ipairs(Presets.Resource) do
    for _, p in ipairs(group) do ResetLockablePresetState(p, UIPlayer) end
  end
end
function unlock_seeds() SEEDS_EFFECT:OnApplyEffect(nil, nil) end
function unhide_blackcube() RemovePresetLockedState("Resource", nil, "BlackCube", "hidden", false) end
TECH = new("Tech", {id = "DeskTech", group = "Default", LockState = "hidden"})
function flip_tech()
  ResetLockablePresetState(TECH, UIPlayer)
  RemovePresetLockStateReason(TECH, "hidden", false, UIPlayer)
end
function state(id) return GetPresetLockStateAndText(Resources[id]) end
function stores(o, id) for _, r in ipairs(o.storable_resources) do if r == id then return true end end return false end
function has(o, id)
  for _, g in ipairs(o.grouped_resources_for_ip or {}) do
    for _, x in ipairs(g.items or {}) do if x == id then return true end end
  end
  return false
end
function ids(o)
  local t = {}
  for _, g in ipairs(o.grouped_resources_for_ip or {}) do for _, x in ipairs(g.items or {}) do t[#t+1] = tostring(x) end end
  table.sort(t) return table.concat(t, ",")
end
function fixlogs(from)
  local n = 0
  for i = (from or 0) + 1, #LOGS do if LOGS[i]:find("UniversalDepotSeedsToggle", 1, true) then n = n + 1 end end
  return n
end
function haslog(pat, from)
  for i = (from or 0) + 1, #LOGS do if LOGS[i]:find(pat) then return true end end
  return false
end
function status() local f = SMRFixPack and SMRFixPack.fixes[FIX_ID] return f and f.status end
FIX_ID = "UniversalDepotSeedsToggle"
'''


def runtime(module_src, veto_at_load=False):
    rt = db.lua_runtime()
    db.load_at(rt, db.ENGINE_SHIMS, "=deskbench_shims")
    db.load_at(rt, PRELUDE, "=C121_prelude")
    for rel, first, text in CLASS_CHUNKS:
        db.load_at(rt, text, "=" + rel, first)
    rt.execute("build_classes()")
    for rel, first, text in DATA_CHUNKS:
        db.load_at(rt, text, "=" + rel, first)
    rt.execute("PreProcessResources()")
    db.load_at(rt, POST, "=C121_post")
    if veto_at_load:
        rt.execute("SMRFixPack_Disabled = {UniversalDepotSeedsToggle = true}")
    if module_src is not None:
        db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "00_Core.lua")), "=Code/00_Core.lua")
        db.load_at(rt, module_src, "=" + MODULE_REL)
    rt.execute("new_game()")
    return rt


# ---- legs: each returns (ok, detail) so a mutant can re-run the same demand ----

def leg_control(src, veto_at_load):
    rt = runtime(src, veto_at_load)
    ev = rt.eval
    rt.execute("PRE = new_depot('UniversalStorageDepot'); B0 = state('Seeds'); H0 = has(PRE, 'Seeds'); "
               "unlock_seeds(); B1 = state('Seeds'); POST_D = new_depot('UniversalStorageDepot')")
    ok = ev("B0 == 'hidden' and stores(PRE, 'Seeds') and not H0 and B1 == 'enabled' and not has(PRE, 'Seeds') "
            "and has(POST_D, 'Seeds') and REBUILDS[PRE] == nil")
    detail = "state %s -> %s; pre groups=[%s]; post groups=[%s]; status=%s" % (
        ev("B0"), ev("B1"), ev("ids(PRE)"), ev("ids(POST_D)"), ev("status()"))
    return rt, ok, detail


def leg_on(src):
    """Demands 2, 3, 4, 4b on one colony."""
    rt = runtime(src)
    rt.execute("""
      PRE = new_depot('UniversalStorageDepot')
      ROCKET = new_depot('RocketBase', true)
      MODSUB = new_depot('ModUniversalDepot', true)
      ROCKET_REF, MODSUB_REF = ROCKET.grouped_resources_for_ip, MODSUB.grouped_resources_for_ip
      L0 = #LOGS
      unlock_seeds()
      POST_D = new_depot('UniversalStorageDepot')
      PRE_REF, POST_REF = PRE.grouped_resources_for_ip, POST_D.grouped_resources_for_ip
      L1 = #LOGS
      GROUP_CALLS = 0
      unhide_blackcube()
      BC = state('BlackCube')
      CALLS3 = GROUP_CALLS
    """)
    return rt


def d2(rt):
    ev = rt.eval
    ok = ev("status() == 'active' and has(PRE, 'Seeds') and REBUILDS[PRE] == 1 and ids(PRE) == ids(POST_D) "
            "and haslog('Seeds changed lock state; updated the resource toggles on 1 Universal Depot', L0)")
    return ok, "pre=[%s] rebuilds=%s post=[%s]" % (ev("ids(PRE)"), ev("REBUILDS[PRE]"), ev("ids(POST_D)"))


def d3(rt):
    ev = rt.eval
    ok = ev("BC == 'enabled' and CALLS3 > 0 and rawequal(PRE.grouped_resources_for_ip, PRE_REF) "
            "and rawequal(POST_D.grouped_resources_for_ip, POST_REF) and REBUILDS[POST_D] == nil "
            "and REBUILDS[PRE] == 1 and fixlogs(L1) == 0")
    return ok, "BlackCube %s; grouping calls in handler=%s; post rebuilds=%s; pre rebuilds=%s" % (
        ev("BC"), ev("CALLS3"), ev("REBUILDS[POST_D]"), ev("REBUILDS[PRE]"))


def d4(rt):
    ev = rt.eval
    ok = ev("stores(ROCKET, 'Seeds') and not has(ROCKET, 'Seeds') and rawequal(ROCKET.grouped_resources_for_ip, ROCKET_REF) "
            "and REBUILDS[ROCKET] == nil")
    return ok, "rocket stores Seeds=%s, groups=[%s], rebuilds=%s" % (
        ev("stores(ROCKET, 'Seeds')"), ev("ids(ROCKET)"), ev("REBUILDS[ROCKET]"))


def d4b(rt):
    ev = rt.eval
    ok = ev("stores(MODSUB, 'Seeds') and not has(MODSUB, 'Seeds') and rawequal(MODSUB.grouped_resources_for_ip, MODSUB_REF) "
            "and REBUILDS[MODSUB] == nil")
    return ok, "mod subclass groups=[%s], rebuilds=%s" % (ev("ids(MODSUB)"), ev("REBUILDS[MODSUB]"))


def stale_colony(src):
    """A depot built while Seeds is hidden, Seeds unlocked while the fix was vetoed,
    veto cleared: a stale cache under an active fix (the shape a save carries)."""
    rt = runtime(src)
    rt.execute("""
      STALE = new_depot('UniversalStorageDepot')
      SMRFixPack_Disabled[FIX_ID] = true
      unlock_seeds()
      SMRFixPack_Disabled[FIX_ID] = nil
      STALE_REF = STALE.grouped_resources_for_ip
      S_SEEDS = state('Seeds')
    """)
    return rt


def d5(src):
    rt = stale_colony(src)
    rt.execute("M0 = #MSGS; GROUP_CALLS = 0; L0 = #LOGS; flip_tech(); CALLS5 = GROUP_CALLS")
    ev = rt.eval
    tech_msgs = [m for m in list(rt.eval("MSGS").values())[int(ev("M0")):] if m.startswith("Tech:")]
    ok = ev("S_SEEDS == 'enabled' and CALLS5 == 0 and rawequal(STALE.grouped_resources_for_ip, STALE_REF) "
            "and not has(STALE, 'Seeds') and REBUILDS[STALE] == nil and fixlogs(L0) == 0") and len(tech_msgs) == 2
    return ok, "Tech messages=%s; grouping calls=%s; stale depot groups=[%s]" % (
        tech_msgs, ev("CALLS5"), ev("ids(STALE)"))


def d6(src):
    rt = stale_colony(src)
    rt.execute("""
      L0 = #LOGS
      Msg('PostLoadGame')
      H1, R1 = has(STALE, 'Seeds'), REBUILDS[STALE]
      REF1 = STALE.grouped_resources_for_ip
      L1 = #LOGS
      Msg('PostLoadGame')
    """)
    ev = rt.eval
    ok = ev("S_SEEDS == 'enabled' and H1 and R1 == 1 "
            "and haslog('load pass updated the resource toggles on 1 Universal Depot', L0) "
            "and rawequal(STALE.grouped_resources_for_ip, REF1) and REBUILDS[STALE] == 1 "
            "and haslog('load pass updated the resource toggles on 0 Universal Depot', L1) "
            "and not haslog('on 1 Universal', L1)")
    return ok, "first pass healed=%s rebuilds=%s; logs=%s" % (
        ev("H1"), ev("REBUILDS[STALE]"), [l for l in rt.eval("LOGS").values() if "load pass" in l])


def d7(src):
    rt = runtime(src)
    rt.execute("""
      PRE = new_depot('UniversalStorageDepot')
      REF = PRE.grouped_resources_for_ip
      SMRFixPack_Disabled[FIX_ID] = true
      L0 = #LOGS
      unlock_seeds()
      Msg('PostLoadGame')
    """)
    ev = rt.eval
    ok = ev("status() == 'active' and state('Seeds') == 'enabled' and not has(PRE, 'Seeds') "
            "and rawequal(PRE.grouped_resources_for_ip, REF) and REBUILDS[PRE] == nil and fixlogs(L0) == 0")
    return ok, "status=%s seeds=%s groups=[%s] fix log lines=%s" % (
        ev("status()"), ev("state('Seeds')"), ev("ids(PRE)"), ev("fixlogs(L0)"))


def d8(src):
    rt = runtime(src)
    rt.execute("""
      BAD = new_depot('UniversalStorageDepot')
      BAD.storable_resources = {'Metals', 1, 'zzz'}
      BAD_REF = BAD.grouped_resources_for_ip
      GOOD = new_depot('UniversalStorageDepot')
      L0 = #LOGS
      MSG_OK, MSG_ERR = pcall(unlock_seeds)
    """)
    ev = rt.eval
    # the throw is ResourceCmp's `a < b` on two ids with no preset (CommonLua Resources.lua:357)
    pat = ("refresh raised on UniversalStorageDepot#%d: CommonLua/Libs/Resources/Resources%%.lua:357: "
           "attempt to compare") % ev("BAD.handle")
    ok = ev("MSG_OK and has(GOOD, 'Seeds') and REBUILDS[GOOD] == 1 and rawequal(BAD.grouped_resources_for_ip, BAD_REF) "
            "and REBUILDS[BAD] == nil and haslog('updated the resource toggles on 1 Universal Depot', L0)") \
        and bool(ev("haslog(%r, L0)" % pat))
    logs = list(rt.eval("LOGS").values())[int(ev("L0")):]
    return ok, "msg ok=%s err=%s; good healed=%s; logs=%s" % (ev("MSG_OK"), ev("MSG_ERR"), ev("has(GOOD,'Seeds')"), logs)


def mutate(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new, 1)


def main():
    print("COMMAND: python tools/desk_c121_depot_seeds.py")
    print("HEAD:", subprocess.check_output(["git", "-C", db.REPO, "rev-parse", "HEAD"], text=True).strip())
    print("TREE:", ARCH)
    bench = db.Bench("C121 Universal Depot Seeds toggle: stale cache, unlock refresh, load heal")
    check = bench.check
    for rel, first, text in CLASS_CHUNKS + DATA_CHUNKS:
        print("  extracted %s:%d (%d lines)" % (rel, first, text.count("\n") + 1))
    src = db.read(str(MODULE))

    # ---- 1. control: the harness reproduces the defect ---------------------
    _, ok, det = leg_control(None, False)
    check("1a fix not loaded: pre-unlock depot stores Seeds but no group shows it, before and after the unlock; "
          "a depot built after the unlock shows it", ok, det)
    rt, ok, det = leg_control(src, True)
    check("1b fix vetoed at load: same stale cache, no rebuild, status disabled",
          ok and rt.eval("status() == 'disabled'"), det)

    # ---- 2-4 on one colony -----------------------------------------------
    on = leg_on(src)
    for label, f in (("2 fix on: the unlock message gives the pre-unlock depot a Seeds group entry, "
                      "equal to a fresh depot's, with one infopanel rebuild and one log line", d2),
                     ("3 idempotent: a later Resource lock change (BlackCube) runs the handler but writes and "
                      "rebuilds nothing on either depot", d3),
                     ("4 scope: a RocketBase (UniversalStorageDepotBase sibling) storing Seeds with a stale cache "
                      "is not touched", d4),
                     ("4b scope: a mod subclass of UniversalStorageDepot with a stale cache is not touched "
                      "(the exact-class test)", d4b)):
        ok, det = f(on)
        check(label, ok, det)

    ok, det = d5(src)
    check("5 a Tech lock change (hide then unhide) touches nothing: no grouping call, stale depot unchanged", ok, det)
    ok, det = d6(src)
    check("6 PostLoadGame heals a stale depot (log 'on 1'); a second PostLoadGame writes nothing, logs 'on 0'", ok, det)
    ok, det = d7(src)
    check("7 veto set after apply: neither the unlock handler nor PostLoadGame writes, rebuilds or logs", ok, det)
    ok, det = d8(src)
    check("8 a depot whose regroup raises is caught, logged by handle with the shipped error line, "
          "and the next depot still refreshes", ok, det)

    # ---- mutants: each must FAIL a demand above ---------------------------
    cls_test = "depot.class == DEPOT_CLASS"
    ma = mutate(src, cls_test, 'IsKindOf(depot, "UniversalStorageDepotBase")')
    ma_on = leg_on(ma)
    a4, _ = d4(ma_on)
    a4b, det = d4b(ma_on)
    check("mutant (a) class test widened to IsKindOf(UniversalStorageDepotBase) FAILS demand 4b", not a4b, det)
    print("        (a) demand 4 under this mutant: %s -- AllMapsForEach(true, \"UniversalStorageDepot\") never "
          "enumerates a sibling, so only a descendant exposes the widened test" % ("held" if a4 else "failed"))
    ma2 = mutate(mutate(src, cls_test, "IsKindOf(depot, DEPOT_CLASS)"),
                 'local DEPOT_CLASS = "UniversalStorageDepot"', 'local DEPOT_CLASS = "UniversalStorageDepotBase"')
    ok, det = d4(leg_on(ma2))
    check("mutant (a2) enumeration AND class test widened to UniversalStorageDepotBase FAILS demand 4", not ok, det)
    mb = mutate(src, "if grouping_key(fresh) == grouping_key(depot.grouped_resources_for_ip) then return false end", "")
    ok, det = d3(leg_on(mb))
    ok6, det6 = d6(mb)
    check("mutant (b) differs-check removed FAILS demand 3 (and 6)", not ok and not ok6, det + " | " + det6)
    mc = mutate(src, 'if not IsKindOf(preset, "Resource") then return end', "")
    ok, det = d5(mc)
    check("mutant (c) Resource filter removed FAILS demand 5", not ok, det)

    check("module declares no save hook, persisted variable or thread",
          all(t not in src for t in ("OnMsg.Save", "GameVar(", "MapVar(", "CreateGameTimeThread", "CreateRealTimeThread")))

    return bench.finish("ALL DEMANDS HELD -- desk-verified on archived 1.1.1.405907 Lua, not in game.")


if __name__ == "__main__":
    sys.exit(main())
