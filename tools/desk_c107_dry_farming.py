#!/usr/bin/env python3
"""C107 Dry Farming reaches the four Feeding the Future plant farms: the module
through the REAL core, over the shipped DryFarming preset, the shipped farm
templates and the shipped BuildingTemplates builder, in the engine's load order.

Desk evidence, never an engine or reachability claim. Nothing here ran in a game.

⛔ REVISED 2026-09-18 AFTER THE FIRST IN-GAME BOOT REFUTED THE FIRST VERSION OF
THIS HARNESS. The build it verified (e95a7d5) went `error` on the owner's boot
(Mars.exe-20260918-17.51.56-6a91a190.log): "none of the four Feeding the Future
plant farms is loaded" at DataLoaded, then "Fix_DryFarmingFarms.lua:113: table
index is nil" on each DataChanged. The first harness had passed it because it
modelled the data wrongly in two ways, both now replaced by shipped code:
  1. It filled `BuildingTemplates` with the raw presets. The game fills it only in
     SetupBuildingTemplateTables (Lua/Buildings/Building.lua:2674-2692), on
     ClassesBuilt and on DataChanged. It is now loaded from there, and its
     handlers are registered before the pack's, as game code loads before mods.
  2. Its values were the presets, which carry `id`. The shipped values are
     proxies, `setmetatable({ template_name = id }, g_Classes[id])` (:2680), whose
     `id` is nil. The classes now come from the shipped generated class files.
  3. It ran every pass with the templates already in place. The legs now follow
     the cold-boot order: ClassesBuilt (no presets yet) -> LoadData (presets
     register into the GlobalMap BuildingTemplates_Raw) -> Msg DataLoaded ->
     DataChanged(false), which Dlc.lua posts after DataLoaded (CommonLua/Dlc.lua:
     715-717 -> :686-690 -> :683). The enable path is a separate leg.
The e95a7d5 module is kept as a regression run: it must FAIL here.

WHAT IS SHIPPED (extracted, loaded under its real file name and line):
  * the DryFarming `Tech` preset block of Data/Tech.lua; the BuildingTemplate
    presets and generated classes of the base plant farms, the Fungal Farm, the
    four norman plant farms and the Insect Farm;
  * SetupBuildingTemplateTables and its ClassesBuilt / DataChanged handlers
    (Lua/Buildings/Building.lua:2674-2692);
  * Effect_ModifyLabel:GetLabelModifierId / :OnApplyEffect (Lua/MarsGameEffects.lua),
    HasModifiablePropScale / GetModifiablePropScale (CommonLua/Classes/Modifiers.lua),
    LabelContainer:SetLabelModifier with its two file locals (Lua/LabelContainer.lua),
    GameEffectsContainer:EffectsApply (CommonLua/Classes/GameEffect.lua),
    the BuildingCustomLabelProps line (Lua/Buildings/Building.lua);
  * Code/00_Core.lua whole (Register / Require / DataPatch / WhenActive are NOT
    stubbed), the module whole, and the Test Kit probe file whole through a mini
    SMRTest.

WHAT IS RETYPED OR STUBBED, and whether it can decide an outcome (the F59 rule):
  * PlaceObj / ForEachPreset: a preset registers into PRESETS and its GlobalMap
    the way Preset:Register does (CommonLua/Preset.lua:562-581): Tech into Techs,
    BuildingTemplate into BuildingTemplates_Raw. Nothing else is filed.
  * DefineClass / class building: a generated class gets `class` = its name,
    `__index` = itself, and inherits from a stub of its object class carrying
    default_label = "Building" (Building.lua:277 via the chain). That is the one
    inherited field the module reads; the rest are the generated class's own.
  * IsKindOf: a fixed kind table (Effect_ModifyLabel is a Tech_Effect/GameEffect;
    Tech is a GameEffectsContainer). It DECIDES the heal's presence test, so the
    copy leg keeps the class metatable exactly as a deserialised key keeps its class.
  * Effect_ModifyLabel / Modifier class tables: the property defaults from the
    shipped DefineClass (MarsGameEffects.lua:234-246, Modifiers.lua:228-235).
  * A farm object in a label is a table whose UpdateModifier sums `percent`; the
    legs only read the net percent.
  * IsTechResearched: a flag per leg.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE_REL = "Code/Fix_DryFarmingFarms.lua"
MODULE = os.path.join(db.REPO, MODULE_REL)
PROBE = os.path.join(db.TESTKIT, "Code", "67_Probes_Wave16.lua")
FIRST_BUILD = "e95a7d5"   # the module that went `error` on the first in-game boot
TARGETS = ["FarmSmall", "FarmSmallUnderground", "FarmUnderground", "AutomatedFarm"]
BASE = ["Farm", "HydroponicFarm", "OpenFarm", "FungalFarm"]
NORMAN = TARGETS + ["FarmInsect"]


def preset_rel(name):
    return ("DLC/norman/Presets/BuildingTemplate/%s.lua" % name if name in NORMAN
            else "Data/BuildingTemplate/%s.lua" % name)


def class_rel(name):
    return ("DLC/norman/Code/BuildingTemplate/%s.generated.lua" % name if name in NORMAN
            else "Lua/BuildingTemplate/%s.generated.lua" % name)


PRELUDE = db.ENGINE_SHIMS + r'''
LOGS = {}
ModLog = function(s) LOGS[#LOGS+1] = s end
CreateRealTimeThread = function(fn) return {fn=fn} end
T = function(id, text) if type(id) == "table" then return id end return text end
IsPoint = function() return false end
point = function(x, y) return {x, y} end
range = function(a, b) return {a, b} end
set = function(...) return {...} end
abs = math.abs
percentWithSign = function(x) return x end
function string.ends_with(s, suffix) return suffix == "" or s:sub(-#suffix) == suffix end
-- procall reports and continues in the engine; here an error is recorded so a leg
-- cannot pass over a swallowed throw
PROCALL_ERRORS = {}
procall = function(f, ...)
  local ok, err = pcall(f, ...)
  if not ok then PROCALL_ERRORS[#PROCALL_ERRORS+1] = tostring(err) end
  return ok
end
print_format = function(...) return "" end
DataLoaded = false
local handlers = {}
OnMsg = setmetatable({}, {__newindex = function(_, event, fn)
  handlers[event] = handlers[event] or {}
  table.insert(handlers[event], fn)
end})
function Msg(event, ...)
  for _, fn in ipairs(handlers[event] or {}) do fn(...) end
end

KINDS = {
  Effect_ModifyLabel = {Effect_ModifyLabel=true, Tech_Effect=true, ModEffect=true, GameEffect=true},
  Tech = {Tech=true, GameEffectsContainer=true, Preset=true},
}
function IsKindOf(o, name)
  if type(o) ~= "table" then return false end
  local k = KINDS[o.class]
  return (o.class == name) or (k ~= nil and k[name] == true)
end

GameEffectsContainer = {}
Tech = setmetatable({class="Tech"}, {__index = GameEffectsContainer})
function GameEffectsContainer:GetEffectIdentifier() return "GameEffect" end
Effect_ModifyLabel = {class="Effect_ModifyLabel", Label="", Prop="", Amount=0, Percent=0,
  Stackable=false, Reason=""}
Modifier = {id=false, prop=false, amount=0, percent=0, display_text=false}
function Modifier:new(t) return setmetatable(t, {__index = Modifier}) end
LabelContainer = {}
g_TechTimesResearched = {}
ModifiablePropScale = {water_consumption = 1000}
CLASSES = {Effect_ModifyLabel = Effect_ModifyLabel, Tech = Tech}

-- classes: generated class files define into CLASSDEFS; build_classes() makes them
CLASSDEFS = {}
DefineClass = setmetatable({}, {__newindex = function(_, name, def) CLASSDEFS[name] = def end})
UndefineClass = function() end
g_Classes = {}
function build_classes()
  for name, def in pairs(CLASSDEFS) do
    def.class = name
    def.__index = def
    local parent = def.__parents and def.__parents[1]
    local base = g_Classes[parent]
    if not base then
      base = {class = parent, default_label = "Building"}
      base.__index = base
      g_Classes[parent] = base
    end
    setmetatable(def, base)
    g_Classes[name] = def
  end
end

-- presets: the effect of Preset:Register (CommonLua/Preset.lua:562-581)
PRESETS = {}
Techs = {}
BuildingTemplates_Raw = {}
function PlaceObj(cls, t)
  t = t or {}
  if type(t[1]) ~= "string" then t.class = cls end
  local C = CLASSES[cls]
  if C then setmetatable(t, {__index = C}) end
  if cls == "Tech" then Techs[t.id] = t
  elseif cls == "BuildingTemplate" then
    BuildingTemplates_Raw[t.id] = t
    PRESETS.BuildingTemplate = PRESETS.BuildingTemplate or {}
    table.insert(PRESETS.BuildingTemplate, t)
  end
  return t
end
function ForEachPreset(cls, fn)
  for _, p in ipairs(PRESETS[cls] or {}) do fn(p) end
end
RESEARCHED = false
function IsTechResearched(id) return id == "DryFarming" and RESEARCHED end

-- A colony: a LabelContainer with one farm object per template label.
function new_colony(labels)
  local c = setmetatable({labels = {}, label_modifiers = {}}, {__index = LabelContainer})
  for _, label in ipairs(labels) do
    local obj = {label = label, pct = 0}
    function obj:UpdateModifier(action, mod, amount, percent) self.pct = self.pct + percent end
    c.labels[label] = {obj}
  end
  return c
end
function net(colony, label) return colony.labels[label][1].pct end
-- A save boundary: every stored key becomes a copy that keeps its class.
function save_boundary(colony)
  for label, mods in pairs(colony.label_modifiers) do
    local copied = {}
    for key, mod in pairs(mods) do
      local c = {}
      for k, v in pairs(key) do c[k] = v end
      setmetatable(c, getmetatable(key))
      copied[c] = mod
    end
    colony.label_modifiers[label] = copied
  end
end
function water_count(label)
  local n = 0
  for _, e in ipairs(Techs.DryFarming or {}) do
    if IsKindOf(e, "Effect_ModifyLabel") and e.Prop == "water_consumption" and e.Label == label then n = n + 1 end
  end
  return n
end
function logs_with(s)
  local n = 0
  for _, l in ipairs(LOGS) do if l:find(s, 1, true) then n = n + 1 end end
  return n
end

-- mini SMRTest: the contracts 00_TestCore gives a probe file
SMRTest = {probes = {}}
function SMRTest.Register(id, def) SMRTest.probes[id] = def end
function SMRTest.FixMissing(id)
  if not rawget(_G, "SMRFixPack") then return "FAIL", "fix pack not loaded" end
  local f = SMRFixPack.fixes[id]
  if not f then return "FAIL", "not registered" end
  if f.status ~= "active" then return "FAIL", "fix is " .. f.status end
end
'''


def tech_block(rt):
    rel = "Data/Tech.lua"
    text = db.read(os.path.join(db.TREES["1.1.0"], rel))
    blocks = [m for m in re.finditer(r"^PlaceObj\('Tech', \{\n.*?^\}\)", text, re.M | re.S)
              if '\tid = "DryFarming",' in m.group()]
    assert len(blocks) == 1, len(blocks)
    m = blocks[0]
    db.load_at(rt, m.group(), "=" + rel, text[:m.start()].count("\n") + 1)


def shipped(rt, rel, pattern):
    text, start, _ = db.body(rel, pattern)
    db.load_at(rt, text, "=" + rel, start)


def load_file(rt, rel):
    db.load_at(rt, db.read(os.path.join(db.TREES["1.1.0"], rel)), "=" + rel)


def module_source(replace=None, rev=None):
    src = db.git_show(db.REPO, rev, MODULE_REL) if rev else db.read(MODULE)
    for old, new in (replace or []):
        assert src.count(old) == 1, "variant anchor not found exactly once: %r" % old
        src = src.replace(old, new)
    return src


def runtime(dlc=True, variant=None, rev=None, pre=None, before=None, late=False,
            enable_path=False, veto=False):
    """pre: Lua run before the module registers. before: Lua run after LoadData and
    before Msg DataLoaded. late: the norman presets register only after DataLoaded
    (a template absent at the first pass). enable_path: the pack is ticked at the
    menu of a running game: data already loaded, then ClassesBuilt."""
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    shipped(rt, "Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:GetLabelModifierId\(")
    shipped(rt, "Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:OnApplyEffect\(")
    shipped(rt, "CommonLua/Classes/Modifiers.lua", r"^function HasModifiablePropScale\(")
    shipped(rt, "CommonLua/Classes/Modifiers.lua", r"^function GetModifiablePropScale\(")
    text, start, _ = db.span("Lua/LabelContainer.lua",
                             [r"^local function UpdateModWithoutCheck\(",
                              r"^function LabelContainer:SetLabelModifier\("])
    db.load_at(rt, text, "=Lua/LabelContainer.lua", start)
    shipped(rt, "CommonLua/Classes/GameEffect.lua", r"^function GameEffectsContainer:EffectsApply\(")
    rel = "Lua/Buildings/Building.lua"
    lines = db.read(os.path.join(db.TREES["1.1.0"], rel)).split("\n")
    at = [i for i, l in enumerate(lines) if l.startswith("BuildingCustomLabelProps = {")]
    assert len(at) == 1
    db.load_at(rt, lines[at[0]], "=" + rel, at[0] + 1)
    # the game's own BuildingTemplates builder and its two handlers, registered
    # before the pack's because game code loads before mods
    text, start, _ = db.span(rel, [r"^function SetupBuildingTemplateTables\(",
                                   r"^function OnMsg\.DataChanged\(classes\)"])
    db.load_at(rt, text, "=" + rel, start)
    # generated classes: code, loaded before any preset (a DLC's only if owned)
    for name in BASE + (NORMAN if dlc else []):
        load_file(rt, class_rel(name))
    rt.execute("build_classes()")

    def load_data(with_dlc_presets):
        tech_block(rt)
        for name in BASE:
            load_file(rt, preset_rel(name))
        if with_dlc_presets:
            for name in NORMAN:
                load_file(rt, preset_rel(name))

    if enable_path:
        load_data(dlc)
        if before:
            rt.execute(before)
        rt.execute("DataLoaded = true")
    if veto:
        rt.execute("SMRFixPack_Disabled = {DryFarmingFarms = true}")
    if pre:
        rt.execute(pre)
    db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "00_Core.lua")), "=Code/00_Core.lua")
    db.load_at(rt, module_source(variant, rev), "=" + MODULE_REL)
    if enable_path:
        rt.execute('Msg("ClassesBuilt"); Msg("ModsReloaded")')
        return rt
    rt.execute('Msg("ClassesBuilt")')           # cold boot: no preset loaded yet
    load_data(dlc and not late)
    if before:
        rt.execute(before)
    rt.execute('Msg("DataLoaded"); DataLoaded = true')   # Dlc.lua:661 then :663
    if dlc and late:
        for name in NORMAN:
            load_file(rt, preset_rel(name))
        # a trigger that does NOT re-arm the pass (DataPatch resets `patched` only
        # on DataChanged): what is appended here is what an early final verdict costs
        rt.execute('Msg("ModsReloaded"); SNAP = {}; for _, l in ipairs({"FarmSmall", '
                   '"FarmSmallUnderground", "FarmUnderground", "AutomatedFarm"}) do '
                   'SNAP[l] = water_count(l) end')
    rt.execute('Msg("DataChanged", false)')     # Dlc.lua:715-717, posted after DataLoaded
    return rt


def status(rt):
    return rt.eval("SMRFixPack.fixes.DryFarmingFarms.status")


def counts(rt):
    return {l: rt.eval('water_count("%s")' % l) for l in TARGETS}


def ev(rt, expr):
    return rt.eval(expr)


def logs(rt):
    return [l for l in rt.globals().LOGS.values() if "DryFarmingFarms" in l]


ALL_LABELS = "{'Farm','HydroponicFarm','OpenFarm','FungalFarm','FarmInsect','FarmSmall','FarmSmallUnderground','FarmUnderground','AutomatedFarm'}"
HEALED_SAVE = """RESEARCHED = true; COL = new_colony(%s); UIColony = COL
    for _, e in ipairs(Techs.DryFarming) do
      if e.Label == 'Farm' or e.Label == 'HydroponicFarm' or e.Label == 'OpenFarm' then
        e:OnApplyEffect(COL, Techs.DryFarming) end end
    save_boundary(COL); Msg('LoadGame')""" % ALL_LABELS


def run_probe(rt):
    db.load_at(rt, db.read(PROBE), "=67_Probes_Wave16.lua")
    return tuple(rt.eval("{SMRTest.probes.DryFarmingFarms.run()}").values())


def legs(bench, variant=None, rev=None, tag=""):
    """Every demand. Returns nothing; a variant or old-build run is expected to fail some."""
    p = tag
    kw = dict(variant=variant, rev=rev)
    # (a) the cold-boot order the owner's boot took
    rt = runtime(**kw)
    c = counts(rt)
    bench.check(p + "(a) cold boot: one water entry per DLC plant farm, module active",
                all(v == 1 for v in c.values()) and status(rt) == "active",
                "%s %s %s" % (c, status(rt), logs(rt)))
    bench.check(p + "(a2) entries copy the shipped -50 and stay in scope",
                ev(rt, """(function() for _, e in ipairs(Techs.DryFarming) do
                    if e.Label == 'FarmSmall' then return e.Percent end end end)()""") == -50
                and all(ev(rt, 'water_count("%s")' % l) == 0
                        for l in ("FungalFarm", "FungalFarm_Asteroid", "FarmInsect", "AllFarms")))
    bench.check(p + "(a3) no 'DLC absent' line on a boot where the DLC is loaded",
                ev(rt, 'logs_with("nothing to add")') == 0, logs(rt))
    # (a4) the enable path: data already loaded, then ClassesBuilt
    rt = runtime(enable_path=True, **kw)
    c = counts(rt)
    bench.check(p + "(a4) enable path: one entry per DLC plant farm, module active",
                all(v == 1 for v in c.values()) and status(rt) == "active",
                "%s %s %s" % (c, status(rt), logs(rt)))
    # (a5) a template absent at the first pass arrives later: paid on the next
    # trigger, even one that does not re-arm the pass
    rt = runtime(late=True, **kw)
    snap = {l: ev(rt, 'SNAP["%s"]' % l) for l in TARGETS}
    bench.check(p + "(a5) DLC presets absent at DataLoaded, present by ModsReloaded: paid then, active",
                all(v == 1 for v in snap.values()) and all(v == 1 for v in counts(rt).values())
                and status(rt) == "active", "%s %s %s" % (snap, status(rt), logs(rt)))
    # (b) a NEW research walks the preset: vanilla's own EffectsApply pays all seven
    rt = runtime(**kw)
    rt.execute("COL = new_colony(%s); UIColony = COL; Techs.DryFarming:EffectsApply(COL)" % ALL_LABELS)
    nets = {l: ev(rt, 'net(COL, "%s")' % l) for l in TARGETS + ["Farm", "FungalFarm", "FarmInsect"]}
    bench.check(p + "(b) new research: DLC farms and Farm at -50, Fungal and Insect at 0",
                all(nets[l] == -50 for l in TARGETS + ["Farm"]) and nets["FungalFarm"] == 0
                and nets["FarmInsect"] == 0 and ev(rt, "#PROCALL_ERRORS") == 0,
                "%s %s" % (nets, list(ev(rt, "PROCALL_ERRORS").values())))
    # (c) a save that researched before the fix: only vanilla's three are stored
    rt = runtime(**kw)
    rt.execute(HEALED_SAVE)
    first = {l: ev(rt, 'net(COL, "%s")' % l) for l in TARGETS}
    bench.check(p + "(c) load heal: each DLC farm gets -50 once",
                all(v == -50 for v in first.values()) and ev(rt, 'logs_with("applied 4 Dry Farming")') == 1, first)
    rt.execute("save_boundary(COL); Msg('LoadGame'); save_boundary(COL); Msg('LoadGame')")
    again = {l: ev(rt, 'net(COL, "%s")' % l) for l in TARGETS}
    bench.check(p + "(c2) two more save/load round trips: still -50, no second heal line",
                all(v == -50 for v in again.values()) and ev(rt, 'logs_with("Dry Farming water reduction")') == 1,
                again)
    bench.check(p + "(c3) Farm, HydroponicFarm, OpenFarm untouched at -50 by the heal",
                all(ev(rt, 'net(COL, "%s")' % l) == -50 for l in ("Farm", "HydroponicFarm", "OpenFarm")))
    # (d) not researched: the heal does nothing
    rt = runtime(**kw)
    rt.execute("COL = new_colony(%s); UIColony = COL; Msg('LoadGame')" % ALL_LABELS)
    bench.check(p + "(d) unresearched save: no modifier written",
                all(ev(rt, 'net(COL, "%s")' % l) == 0 for l in TARGETS)
                and ev(rt, "next(COL.label_modifiers) == nil"))
    # (e) a further re-fire and a Lua reload adopt, never duplicate
    rt = runtime(**kw)
    rt.execute("Msg('DataChanged', false)")
    c1, s1 = counts(rt), status(rt)
    db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "00_Core.lua")), "=Code/00_Core.lua")
    db.load_at(rt, module_source(variant, rev), "=" + MODULE_REL)
    rt.execute("Msg('ClassesBuilt')")
    c2, s2 = counts(rt), status(rt)
    bench.check(p + "(e) re-fire and Lua reload: still one entry each, still active",
                all(v == 1 for v in list(c1.values()) + list(c2.values())) and s1 == s2 == "active",
                "%s %s %s %s" % (c1, s1, c2, s2))
    # (f) Feeding the Future absent: nothing appended, active, idle, one log line
    rt = runtime(dlc=False, **kw)
    rt.execute("RESEARCHED = true; COL = new_colony({'Farm'}); UIColony = COL; Msg('LoadGame')")
    bench.check(p + "(f) DLC absent: no entry, active and idle, logged once, nothing in the save",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "active"
                and ev(rt, 'logs_with("nothing to add")') == 1 and ev(rt, "next(COL.label_modifiers) == nil"),
                logs(rt))
    # (g) a template already in a paid label is left alone (no -100% stack)
    rt = runtime(before="g_Classes.FarmSmall.label5 = 'Farm'", **kw)
    c = counts(rt)
    bench.check(p + "(g) FarmSmall already in label Farm: no entry for it, the other three added",
                c["FarmSmall"] == 0 and all(c[l] == 1 for l in TARGETS[1:]) and status(rt) == "active", c)
    # (h) vanilla fixes it by AllFarms: nothing appended, benign latch
    rt = runtime(before="""table.insert(Techs.DryFarming,
        PlaceObj('Effect_ModifyLabel', {Label='AllFarms', Percent=-50, Prop='water_consumption'}))""", **kw)
    bench.check(p + "(h) a shipped AllFarms entry: nothing appended, benign RETIRE latch",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, 'logs_with("RETIRE candidate")') >= 1, logs(rt))
    # (i) vanilla ships the four entries itself: adopted, benign latch, no duplicate
    rt = runtime(before="""for _, l in ipairs({'FarmSmall','FarmSmallUnderground','FarmUnderground','AutomatedFarm'}) do
        table.insert(Techs.DryFarming, PlaceObj('Effect_ModifyLabel', {Label=l, Percent=-50, Prop='water_consumption'})) end""", **kw)
    bench.check(p + "(i) shipped DLC entries: adopted, not doubled, benign latch",
                all(v == 1 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, 'logs_with("RETIRE candidate")') >= 1, logs(rt))
    # (j) shape moved: siblings disagree on Percent -> latch, nothing appended
    rt = runtime(before="""for _, e in ipairs(Techs.DryFarming) do
        if e.Label == 'OpenFarm' then e.Percent = -40 end end""", **kw)
    bench.check(p + "(j) shipped entries disagree on Percent: latched, nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, "SMRFixPack.fixes.DryFarmingFarms.update_suspect") is True)
    # (k) probe declines when the modifier is not keyed by the effect object
    rt = runtime(pre="""function Effect_ModifyLabel:GetLabelModifierId(parent)
        return 'x.' .. self.Label .. '.' .. self.Prop end""", **kw)
    bench.check(p + "(k) OnApplyEffect keyed by a string id: probe declines, nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive")
    # (l) the 1.0.7 shape: DryFarming is not in Techs
    rt = runtime(before="Techs.DryFarming = nil", **kw)
    bench.check(p + "(l) Techs.DryFarming absent (1.0.7 shape): latched inactive",
                status(rt) == "inactive" and ev(rt, 'logs_with("Techs.DryFarming not found")') >= 1)
    # (m) apply's self-check declines: the pass must not write
    rt = runtime(pre="IsTechResearched = nil", **kw)
    bench.check(p + "(m) self-check declined: inactive and nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive")
    # (n) the veto
    rt = runtime(veto=True, **kw)
    bench.check(p + "(n) veto: disabled and nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "disabled")
    # (q) a malformed water entry with no Label cannot throw the pass. A PlaceObj'd
    # effect always has Label "" by class default, so the leg inserts a bare table
    # (what another mod could put there); the guard is defensive.
    rt = runtime(before="""table.insert(Techs.DryFarming,
        {class='Effect_ModifyLabel', Percent=-50, Prop='water_consumption'})""", **kw)
    bench.check(p + "(q) a water entry with no Label: no throw, four entries, active",
                all(v == 1 for v in counts(rt).values()) and status(rt) == "active",
                "%s %s" % (status(rt), logs(rt)))
    # (o) the Test Kit probe: PASS on a healed save, FAIL with the module absent
    rt = runtime(**kw)
    rt.execute(HEALED_SAVE + "; save_boundary(COL)")
    res = run_probe(rt)
    bench.check(p + "(o) kit probe PASS with the module applied", res[0] == "PASS", res)
    rt.execute("SMRFixPack.fixes.DryFarmingFarms = nil")
    res = run_probe(rt)
    bench.check(p + "(o2) kit probe FAIL with the module not registered", res[0] == "FAIL", res)


# Each variant reverts one guard in a scratch copy of the module; the named legs
# must FAIL. Anchors must hit exactly once.
VARIANTS = [
    ("identity presence test (the F95 regression)",
     [("if IsKindOf(key, \"Effect_ModifyLabel\") and key.Label == label\n"
       "\t\t\t\t\t\t\tand key.Prop == effect.Prop and key.Percent == effect.Percent\n"
       "\t\t\t\t\t\t\tand (key.Amount or 0) == 0 then",
       "if key == effect then")],
     ["(c2)", "(o)"]),
    ("no adopt",
     [("\t\t\t\tif water[label] then", "\t\t\t\tif false then")],
     ["(e)", "(i)"]),
    ("no data_loaded gate",
     [("\t\tif not ctx.data_loaded then return end\n", "")],
     ["(f)"]),
    ("absence latched final (the first boot's fault 1)",
     [("\t\tif complete then ctx.patched = true end", "\t\tctx.patched = true")],
     ["(a5)"]),
    ("existence and labels from BuildingTemplates (the first boot's source)",
     [("\t\tlocal presets = rawget(_G, \"BuildingTemplates_Raw\")",
       "\t\tlocal presets = rawget(_G, \"BuildingTemplates\")")],
     ["(a3)", "(a5)"]),
    ("no already-reached guard",
     [("\t\t\t\t\tif via then", "\t\t\t\t\tif false then")],
     ["(g)", "(h)"]),
    ("no self_check_passed gate",
     [("\t\tif not self_check_passed then return end\n", "")],
     ["(m)"]),
    ("no shape check",
     [("\t\t\t\t\tor (percent and e.Percent ~= percent) then", "\t\t\t\t\tor false then")],
     ["(j)"]),
    ("no behaviour probe",
     [("{ probe = function() return files_as_expected(farm_entry, tech) end },",
       "{ probe = function() return true end },")],
     ["(k)"]),
    ("no Label type guard",
     [("\t\t\t\t\tand type(effect.Label) == \"string\" then", "\t\t\t\t\tthen")],
     ["(q)"]),
]


def failed_legs(b):
    return sorted({lbl.split(")")[0].split("(")[-1] for ok, lbl in b.results if not ok})


def run_quiet(title, **kw):
    b = db.Bench(title)
    try:
        legs(b, tag="[x] ", **kw)
    except Exception as e:  # an old build or variant that errors out is also caught
        print("  run raised:", e)
    return ["(%s)" % f for f in failed_legs(b)], b


def main():
    bench = db.Bench("C107 Fix_DryFarmingFarms over the shipped DryFarming preset, farm "
                     "templates and BuildingTemplates builder")
    legs(bench)
    held = bench.finish("ALL DEMANDS HELD -- desk evidence; nothing ran in a game.")

    print()
    print("REGRESSION: the %s build (the one that went `error` in game) must FAIL (a), (a3), (a4)"
          % FIRST_BUILD)
    failed, _ = run_quiet("regression: module at " + FIRST_BUILD, rev=FIRST_BUILD)
    reg_ok = all(m in failed for m in ("(a)", "(a3)", "(a4)"))
    print("  -> %s: FAIL %s" % ("REPRODUCED" if reg_ok else "NOT REPRODUCED", failed))

    print()
    print("FALSIFICATION: one guard reverted per scratch variant; the named legs must FAIL")
    ok_all = True
    for name, repl, must_fail in VARIANTS:
        failed, _ = run_quiet("variant: " + name, variant=repl)
        caught = all(m in failed for m in must_fail)
        ok_all &= caught
        print("  -> %s [%s]: expected FAIL %s, got FAIL %s"
              % ("CAUGHT" if caught else "MISSED", name, must_fail, failed))
    print()
    print("REGRESSION:", "reproduced" if reg_ok else "NOT REPRODUCED")
    print("FALSIFICATION:", "every variant caught" if ok_all else "A VARIANT WAS MISSED")
    return held or (0 if (ok_all and reg_ok) else 1)


if __name__ == "__main__":
    raise SystemExit(main())
