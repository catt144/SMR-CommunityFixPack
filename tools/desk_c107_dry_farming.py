#!/usr/bin/env python3
"""C107 Dry Farming reaches the four Feeding the Future plant farms: the module
through the REAL core, over the shipped DryFarming preset and farm templates.

Desk evidence, never an engine or reachability claim. Nothing here ran in a game.

WHAT IS SHIPPED (extracted, loaded under its real file name and line):
  * the DryFarming `Tech` preset block of Data/Tech.lua, and the BuildingTemplate
    presets of the three base plant farms, both Fungal Farms, the four norman
    plant farms and the Insect Farm;
  * Effect_ModifyLabel:GetLabelModifierId / :OnApplyEffect (Lua/MarsGameEffects.lua),
    HasModifiablePropScale / GetModifiablePropScale (CommonLua/Classes/Modifiers.lua),
    LabelContainer:SetLabelModifier (Lua/LabelContainer.lua),
    GameEffectsContainer:EffectsApply (CommonLua/Classes/GameEffect.lua),
    the BuildingCustomLabelProps line (Lua/Buildings/Building.lua);
  * Code/00_Core.lua whole (Register / Require / DataPatch / WhenActive are NOT
    stubbed: status transitions are part of the question), the module whole, and
    the Test Kit probe file whole through a mini SMRTest.

WHAT IS RETYPED OR STUBBED, and whether it can decide an outcome (the F59 rule):
  * PlaceObj: stores the table, sets `class` and a class metatable, files Tech and
    BuildingTemplate presets in Techs / BuildingTemplates. Constructs nothing else.
  * IsKindOf: a fixed kind table (Effect_ModifyLabel is a Tech_Effect/GameEffect;
    Tech is a GameEffectsContainer), read off the shipped DefineClass lines. It
    DECIDES the heal's presence test and the probe's count, so the copy leg keeps
    the class metatable exactly as a deserialised key keeps its class.
  * Effect_ModifyLabel / Modifier class tables: the property defaults from the
    shipped DefineClass (MarsGameEffects.lua:234-246, Modifiers.lua:228-235).
    Modifier is InitDone with no Init, so `new` is a setmetatable.
  * A farm object in a label is a table whose UpdateModifier sums `percent`. The
    real Modifiable body is not modelled; the legs only read the net percent, and
    the real body cannot refuse an add for a prop the object carries.
  * IsTechResearched: a flag per leg. g_Classes: default_label = "Building" for
    the farm object classes (Building.lua:277 via the class chain).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_DryFarmingFarms.lua")
PROBE = os.path.join(db.TESTKIT, "Code", "67_Probes_Wave16.lua")
TARGETS = ["FarmSmall", "FarmSmallUnderground", "FarmUnderground", "AutomatedFarm"]
BASE_TEMPLATES = ["Data/BuildingTemplate/%s.lua" % n
                  for n in ("Farm", "HydroponicFarm", "OpenFarm", "FungalFarm", "FungalFarm_Asteroid")]
DLC_TEMPLATES = ["DLC/norman/Presets/BuildingTemplate/%s.lua" % n
                 for n in TARGETS + ["FarmInsect"]]

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
Techs = {}
BuildingTemplates = {}
g_Classes = {
  FarmConventional = {default_label="Building"}, FarmHydroponic = {default_label="Building"},
  OpenFarmBase = {default_label="Building"}, FungalFarmBase = {default_label="Building"},
  FarmSmallBase = {default_label="Building"}, AutomatedFarmBase = {default_label="Building"},
  FarmInsectBase = {default_label="Building"},
}
function PlaceObj(cls, t)
  t = t or {}
  if type(t[1]) ~= "string" then t.class = cls end
  local C = CLASSES[cls]
  if C then setmetatable(t, {__index = C}) end
  if cls == "Tech" then Techs[t.id] = t
  elseif cls == "BuildingTemplate" then BuildingTemplates[t.id] = t end
  return t
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


def module_source(replace=None):
    src = db.read(MODULE)
    for old, new in (replace or []):
        assert src.count(old) == 1, "variant anchor not found exactly once: %r" % old
        src = src.replace(old, new)
    return src


def runtime(dlc=True, variant=None, before=None, templates_late=False, veto=False):
    """before: Lua run after the data loads and before the module registers.
    templates_late: the DLC templates arrive only at DataLoaded (the cold-boot order)."""
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    shipped(rt, "Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:GetLabelModifierId\(")
    shipped(rt, "Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:OnApplyEffect\(")
    shipped(rt, "CommonLua/Classes/Modifiers.lua", r"^function HasModifiablePropScale\(")
    shipped(rt, "CommonLua/Classes/Modifiers.lua", r"^function GetModifiablePropScale\(")
    # SetLabelModifier closes over two file locals declared above it
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
    tech_block(rt)
    for r in BASE_TEMPLATES:
        load_file(rt, r)
    if dlc and not templates_late:
        for r in DLC_TEMPLATES:
            load_file(rt, r)
    if before:
        rt.execute(before)
    if veto:
        rt.execute("SMRFixPack_Disabled = {DryFarmingFarms = true}")
    db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "00_Core.lua")), "=Code/00_Core.lua")
    db.load_at(rt, module_source(variant), "=Code/Fix_DryFarmingFarms.lua")
    rt.execute('Msg("ClassesBuilt")')
    if dlc and templates_late:
        for r in DLC_TEMPLATES:
            load_file(rt, r)
    rt.execute('DataLoaded = true; Msg("DataLoaded")')
    return rt


def status(rt):
    return rt.eval("SMRFixPack.fixes.DryFarmingFarms.status")


def counts(rt):
    return {l: rt.eval('water_count("%s")' % l) for l in TARGETS}


def ev(rt, expr):
    return rt.eval(expr)


ALL_LABELS = "{'Farm','HydroponicFarm','OpenFarm','FungalFarm','FarmInsect','FarmSmall','FarmSmallUnderground','FarmUnderground','AutomatedFarm'}"


def run_probe(rt):
    db.load_at(rt, db.read(PROBE), "=67_Probes_Wave16.lua")
    return tuple(rt.eval("{SMRTest.probes.DryFarmingFarms.run()}").values())


def legs(bench, variant=None, tag=""):
    """Every demand. Returns nothing; a variant run is expected to fail some."""
    p = tag
    # (a) cold boot, DLC templates arriving at DataLoaded (the real order)
    rt = runtime(variant=variant, templates_late=True)
    c = counts(rt)
    bench.check(p + "(a) cold boot: one water entry per DLC plant farm, module active",
                all(v == 1 for v in c.values()) and status(rt) == "active", "%s %s" % (c, status(rt)))
    bench.check(p + "(a2) entries copy the shipped -50 and stay in scope",
                ev(rt, """(function() for _, e in ipairs(Techs.DryFarming) do
                    if e.Label == 'FarmSmall' then return e.Percent end end end)()""") == -50
                and all(ev(rt, 'water_count("%s")' % l) == 0
                        for l in ("FungalFarm", "FungalFarm_Asteroid", "FarmInsect", "AllFarms")))
    # (b) a NEW research walks the preset: vanilla's own EffectsApply pays all seven
    rt.execute("COL = new_colony(%s); UIColony = COL; Techs.DryFarming:EffectsApply(COL)" % ALL_LABELS)
    nets = {l: ev(rt, 'net(COL, "%s")' % l) for l in TARGETS + ["Farm", "FungalFarm", "FarmInsect"]}
    bench.check(p + "(b) new research: DLC farms and Farm at -50, Fungal and Insect at 0",
                all(nets[l] == -50 for l in TARGETS + ["Farm"]) and nets["FungalFarm"] == 0
                and nets["FarmInsect"] == 0 and ev(rt, "#PROCALL_ERRORS") == 0,
                "%s %s" % (nets, list(ev(rt, "PROCALL_ERRORS").values())))
    # (c) a save that researched before the fix: only vanilla's three are stored
    rt = runtime(variant=variant)
    rt.execute("""RESEARCHED = true; COL = new_colony(%s); UIColony = COL
        for _, e in ipairs(Techs.DryFarming) do
          if e.Label == 'Farm' or e.Label == 'HydroponicFarm' or e.Label == 'OpenFarm' then
            e:OnApplyEffect(COL, Techs.DryFarming) end end
        save_boundary(COL); Msg('LoadGame')""" % ALL_LABELS)
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
    rt = runtime(variant=variant)
    rt.execute("COL = new_colony(%s); UIColony = COL; Msg('LoadGame')" % ALL_LABELS)
    bench.check(p + "(d) unresearched save: no modifier written",
                all(ev(rt, 'net(COL, "%s")' % l) == 0 for l in TARGETS)
                and ev(rt, "next(COL.label_modifiers) == nil"))
    # (e) the DataChanged(false) re-fire and a Lua reload adopt, never duplicate
    rt = runtime(variant=variant)
    rt.execute("Msg('DataChanged', false)")
    c1, s1 = counts(rt), status(rt)
    db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "00_Core.lua")), "=Code/00_Core.lua")
    db.load_at(rt, module_source(variant), "=Code/Fix_DryFarmingFarms.lua")
    rt.execute("Msg('ClassesBuilt')")
    c2, s2 = counts(rt), status(rt)
    bench.check(p + "(e) re-fire and Lua reload: still one entry each, still active",
                all(v == 1 for v in list(c1.values()) + list(c2.values())) and s1 == s2 == "active",
                "%s %s %s %s" % (c1, s1, c2, s2))
    # (f) Feeding the Future absent: nothing appended, active, idle, no heal
    rt = runtime(dlc=False, variant=variant)
    rt.execute("RESEARCHED = true; COL = new_colony({'Farm'}); UIColony = COL; Msg('LoadGame')")
    bench.check(p + "(f) DLC absent: no entry, active and idle, nothing in the save",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "active"
                and ev(rt, 'logs_with("nothing to add")') == 1 and ev(rt, "next(COL.label_modifiers) == nil"))
    # (g) a template already in a paid label is left alone (no -100% stack)
    rt = runtime(variant=variant, before="BuildingTemplates.FarmSmall.label5 = 'Farm'")
    c = counts(rt)
    bench.check(p + "(g) FarmSmall already in label Farm: no entry for it, the other three added",
                c["FarmSmall"] == 0 and all(c[l] == 1 for l in TARGETS[1:]) and status(rt) == "active", c)
    # (h) vanilla fixes it by AllFarms: nothing appended, benign latch
    rt = runtime(variant=variant, before="""table.insert(Techs.DryFarming,
        PlaceObj('Effect_ModifyLabel', {Label='AllFarms', Percent=-50, Prop='water_consumption'}))""")
    bench.check(p + "(h) a shipped AllFarms entry: nothing appended, benign RETIRE latch",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, 'logs_with("RETIRE candidate")') == 1)
    # (i) vanilla ships the four entries itself: adopted, benign latch, no duplicate
    rt = runtime(variant=variant, before="""for _, l in ipairs({'FarmSmall','FarmSmallUnderground','FarmUnderground','AutomatedFarm'}) do
        table.insert(Techs.DryFarming, PlaceObj('Effect_ModifyLabel', {Label=l, Percent=-50, Prop='water_consumption'})) end""")
    bench.check(p + "(i) shipped DLC entries: adopted, not doubled, benign latch",
                all(v == 1 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, 'logs_with("RETIRE candidate")') == 1)
    # (j) shape moved: siblings disagree on Percent -> latch, nothing appended
    rt = runtime(variant=variant, before="""for _, e in ipairs(Techs.DryFarming) do
        if e.Label == 'OpenFarm' then e.Percent = -40 end end""")
    bench.check(p + "(j) shipped entries disagree on Percent: latched, nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive"
                and ev(rt, "SMRFixPack.fixes.DryFarmingFarms.update_suspect") is True)
    # (k) probe declines when the modifier is not keyed by the effect object
    rt = runtime(variant=variant, before="""function Effect_ModifyLabel:GetLabelModifierId(parent)
        return 'x.' .. self.Label .. '.' .. self.Prop end""")
    bench.check(p + "(k) OnApplyEffect keyed by a string id: probe declines, nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive")
    # (l) the 1.0.7 shape: DryFarming is not in Techs
    rt = runtime(variant=variant, before="Techs.DryFarming = nil")
    bench.check(p + "(l) Techs.DryFarming absent (1.0.7 shape): latched inactive",
                status(rt) == "inactive" and ev(rt, 'logs_with("Techs.DryFarming not found")') == 1)
    # (m) apply's self-check declines: the pass must not write
    rt = runtime(variant=variant, before="IsTechResearched = nil")
    bench.check(p + "(m) self-check declined: inactive and nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "inactive")
    # (n) the veto
    rt = runtime(variant=variant, veto=True)
    bench.check(p + "(n) veto: disabled and nothing appended",
                all(v == 0 for v in counts(rt).values()) and status(rt) == "disabled")
    # (o) the Test Kit probe: PASS on a healed save, FAIL with the module absent
    rt = runtime(variant=variant)
    rt.execute("""RESEARCHED = true; COL = new_colony(%s); UIColony = COL
        for _, e in ipairs(Techs.DryFarming) do if e.Label == 'Farm' or e.Label == 'HydroponicFarm'
          or e.Label == 'OpenFarm' then e:OnApplyEffect(COL, Techs.DryFarming) end end
        save_boundary(COL); Msg('LoadGame'); save_boundary(COL)""" % ALL_LABELS)
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
     ["(a)", "(a2)", "(b)"]),
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
]


def main():
    bench = db.Bench("C107 Fix_DryFarmingFarms over the shipped DryFarming preset and farm templates")
    legs(bench)
    held = bench.finish("ALL DEMANDS HELD -- desk evidence; nothing ran in a game.")

    print()
    print("FALSIFICATION: one guard reverted per scratch variant; the named legs must FAIL")
    ok_all = True
    for name, repl, must_fail in VARIANTS:
        vb = db.Bench("variant: " + name)
        try:
            legs(vb, variant=repl, tag="[v] ")
        except Exception as e:  # a variant that errors out is also a caught variant
            print("  variant raised:", e)
        failed = {lbl.split(")")[0].replace("[v] ", "") + ")" for ok, lbl in vb.results if not ok}
        caught = all(m in failed for m in must_fail)
        ok_all &= caught
        print("  -> %s: expected FAIL %s, got FAIL %s" % ("CAUGHT" if caught else "MISSED",
                                                           must_fail, sorted(failed)))
    print()
    print("FALSIFICATION:", "every variant caught" if ok_all else "A VARIANT WAS MISSED")
    return held or (0 if ok_all else 1)


if __name__ == "__main__":
    raise SystemExit(main())
