#!/usr/bin/env python3
"""C105 investigation: does the Water Reclamation automation upgrade remove the spire's water saving?

Executes the SHIPPED bodies on the path from `Building:ApplyUpgrade` to the dome's water numbers:
the game's own modifier system (Lua/Modifiers.lua -- NOT CommonLua/Classes/Modifiers.lua, which
the game redefines), Workplace performance and max_workers handling, the whole
Lua/Buildings/WaterReclamation.lua, and LabelContainer:SetLabelModifier with its two update
helpers.

Retyped or stubbed, and why each is safe for THIS question:
  * the class system: RecursiveCallMethods "call" for OnModifiableValueChanged and OnSetWorking
    (Lua/Modifiers.lua:1, Lua/Buildings/Building.lua:3) runs every ancestor's OWN implementation,
    parents first (Lua/Modifiers.lua:18). Of the spire's ancestors only Workplace, Modifiable
    (empty) and RequiresMaintenance (reacts to disable_maintenance only, RequiresMaintenance.lua:56)
    define the callback; Workplace + the spire are the ones chained here.
  * OnSetWorking chain = the spire's RecalcModifiers only: Building:OnSetWorking is lights, sound
    and a Msg (Building.lua:1395-1412), HasConsumption:OnSetWorking a notification
    (HasConsumption.lua:660-671).
  * a colonist: GetFired -> SetWorkplace(false) -> old_workplace:RemoveWorker(self)
    (Colonist.lua:1875-1882, :1705-1720), GetWorkPerformance returns the fixture value.
  * working-state and UI plumbing that decides nothing numeric here (SetWorkplaceWorking,
    StopWorkCycle, UpdateAttachedSigns, CheckWorkForUnemployed, RebuildInfopanel,
    UpdateQualityRestNightShiftBan with no Right to Rest law, ObjModified).
  * DirectlyModifiedConstValue -> nil: it only overrides sponsor consts (PreGameMission.lua:461-470).
  * GetPropScale -> 1: automation, auto_performance and max_workers declare no scale
    (Workplace.lua:9, :14, :15).
"""
import hashlib
import subprocess
import sys

import deskbench as db

BODIES = (
    ("Lua/Modifiers.lua", r"^function Modifiable:UpdateModifier\("),
    ("Lua/Modifiers.lua", r"^function Modifiable:ModifyValue\("),
    ("Lua/Modifiers.lua", r"^function Modifiable:SetBase\("),
    ("Lua/Modifiers.lua", r"^function ObjectModifier:Init\("),
    ("Lua/Modifiers.lua", r"^function ObjectModifier:Add\("),
    ("Lua/Modifiers.lua", r"^function ObjectModifier:Remove\("),
    ("Lua/Modifiers.lua", r"^function ObjectModifier:Change\("),
    ("Lua/Modifiers.lua", r"^function ObjectModifier:IsApplied\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:GetWorkersPerformance\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:GetWorkshiftPerformance\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:UpdatePerformance\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:OnModifiableValueChanged\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:SetWorkshift\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:CloseAllWorkplacesWithoutClosingShift\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:RemoveWorker\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:FireWorker\("),
    ("Lua/Buildings/Workplace.lua", r"^function Workplace:IsOvertime\("),
    ("Lua/Buildings/ShiftsBuilding.lua", r"^function ShiftsBuilding:SetWorkshift\("),
    ("Lua/Buildings/Building.lua", r"^function Building:ApplyUpgrade\("),
    ("Lua/Buildings/UpgradableBuilding.lua", r"^function UpgradableBuilding:CreateUpgradeUpkeepObject\("),
)

SETUP = r'''
-- EF-005 engine tolerance: #nil is 0
debug.setmetatable(nil, { __len = function() return 0 end })
-- file locals ModifyValue closes over, verbatim from Lua/Modifiers.lua:88-89
max_int64 = 2^63 - 1
min_int64 = -(2^63)
function MulDivRound(a, b, c) local v = a * b / c; return v >= 0 and math.floor(v + 0.5) or -math.floor(-v + 0.5) end
function Clamp(v, lo, hi) if v < lo then return lo elseif v > hi then return hi end return v end
function IsValid(o) return o ~= nil and o ~= false end
function IsKindOfClasses() return false end
function RebuildInfopanel() end
function ObjModified() end
function UpdateQualityRestNightShiftBan() end
function DirectlyModifiedConstValue() return nil end
function GetPropScale() return 1 end
function Msg() end
function print() end
function assert(v, msg) if not v then error(msg or "assertion failed", 2) end return v end
GameInitThreads = {}
g_WorkforceVersion = 0
ActiveLaws = {}
g_Consts = { NoWorkersPerformance = 100, OvertimedShiftPerformance = 30 }
const = { Building = { UpgradeModifierSlots = 3, MaxUpgrades = 6 } }
g_ConsumptionType = { Production = "production" }
UpgradeModifierModifiers = {}
UIColony = { day = 1, IsUpgradeUnlocked = function() return true end }
empty_table = {}

Modifiable, ObjectModifier, Workplace, ShiftsBuilding, Building, UpgradableBuilding = {}, {}, {}, {}, {}, {}
ObjectModifier.amount, ObjectModifier.percent, ObjectModifier.is_applied = 0, 0, false
ObjectModifier.__index = ObjectModifier
function ObjectModifier:new(t) setmetatable(t, ObjectModifier); t:Init(); return t end
Modifier = { new = function(self, t) t.amount = t.amount or 0; t.percent = t.percent or 0; return t end }
function DefineClass() end
OWN_OMVC, OWN_OSW = {}, {}
'''

AFTER_LOAD = r'''
ObjectModifier.TurnOn = ObjectModifier.Add        -- Lua/Modifiers.lua:318
ObjectModifier.TurnOff = ObjectModifier.Remove    -- :319
WRS = WaterReclamationSpire
-- RecursiveCallMethods "call": parents' own implementations first, then the class's own
local wp_own = Workplace.OnModifiableValueChanged
local wrs_own = WRS.OnModifiableValueChanged
local wrs_osw = WRS.OnSetWorking
Workplace.OnModifiableValueChanged = function(self, ...) wp_own(self, ...) end
function spire_omvc(self, ...) wp_own(self, ...) wrs_own(self, ...) end
function spire_osw(self, working) wrs_osw(self, working) end

LabelContainer = {}
local function UpdateModWithoutCheck(obj, ...) return obj:UpdateModifier(...) end
local function UpdateModWithCheck(obj, action, mod, ...)
	if obj[mod.prop] ~= nil then return obj:UpdateModifier(action, mod, ...) end
end
'''

FIXTURE = r'''
local function modifiable(t)
	t.modifications = false
	t.UpdateModifier = Modifiable.UpdateModifier
	t.ModifyValue = Modifiable.ModifyValue
	t.SetBase = Modifiable.SetBase
	t.HasMember = function(self, k) return self[k] ~= nil end
	t.GetPropertyMetadata = function(self, prop) return (self.__meta or {})[prop] end
	t.OnModifiableValueChanged = t.OnModifiableValueChanged or function() end
	return t
end

function make_colonist(perf)
	return {
		work_performance = perf, workplace = false,
		GetWorkPerformance = function(self) return self.work_performance end,
		IsInWorkCommand = function() return false end,
		InterruptCommand = function() end,
		UpdateWorkplace = function() end,
		GetFired = function(self) if not self.workplace then return end; self:SetWorkplace(false) end,
		SetWorkplace = function(self, b)
			local old = self.workplace
			if old and not b then old:RemoveWorker(self) end
			self.workplace = b
		end,
	}
end

function build_world(worker_perf, n_workers, n_spires)
	dome = modifiable({ water_consumption = 10000, base_water_consumption = 10000,
		label_modifiers = {}, labels = { WaterReclamationSpires = {}, SupplyGridBuildings = {} } })
	dome.SetLabelModifier = LABEL_SET
	farm = modifiable({ water_consumption = 5000, base_water_consumption = 5000 })
	dome.labels.SupplyGridBuildings[1] = farm
	spires = {}
	for s = 1, n_spires do
		local sp = modifiable({
			class = "WaterReclamationSystem", handle = s, parent_dome = dome, parent_dome_modifier = false,
			max_workers = 2, base_max_workers = 2, automation = 0, base_automation = 0,
			auto_performance = 0, base_auto_performance = 0, performance = 100, base_performance = 100,
			max_shifts = 3, current_shift = 1, active_shift = 0, closed_shifts = {}, closed_workplaces = {},
			workers = { {}, {}, {} }, overtime = { false, false, false }, destroyed = false, working = true,
			upgrades_built = false, upgrade_on_off_state = false,
			upgrade1_id = "WaterReclamationSystem_JumboCave",
			upgrade1_mod_prop_id_1 = "automation", upgrade1_add_value_1 = 1, upgrade1_mul_value_1 = 0,
			upgrade1_mod_prop_id_2 = "auto_performance", upgrade1_add_value_2 = 100, upgrade1_mul_value_2 = 0,
			upgrade1_mod_prop_id_3 = "max_workers", upgrade1_add_value_3 = 0, upgrade1_mul_value_3 = -100,
			upgrade1_mod_target_1 = "self", upgrade1_mod_target_2 = "self", upgrade1_mod_target_3 = "self",
			upgrade1_consumption_resource_type = "no_consumption",
			__meta = { max_workers = { min = 0, max = 20 }, performance = { min = 0 } },
		})
		setmetatable(sp, { __index = function(t, k)
			local v = WRS[k]; if v ~= nil then return v end
			v = Workplace[k]; if v ~= nil then return v end
			v = ShiftsBuilding[k]; if v ~= nil then return v end
			v = Building[k]; if v ~= nil then return v end
			return UpgradableBuilding[k]
		end })
		sp.OnModifiableValueChanged = spire_omvc
		sp.OnSetWorking = spire_osw
		sp.GetUpgradeID = function(self, tier) return self["upgrade" .. tier .. "_id"] end
		sp.HasUpgrade = function(self, id) return self.upgrades_built and self.upgrades_built[id] end
		sp.GetProperty = function(self, p) return self[p] end
		sp.IsShroudedInRubble = function() return false end
		sp.SetWorkplaceWorking = function() end
		sp.StopWorkCycle = function() end
		sp.UpdateAttachedSigns = function() end
		sp.CheckWorkForUnemployed = function() end
		sp.OnChangeWorkshift = function() end
		sp.CanWork = function() return true end
		sp.UpdateWorking = function(self) self:SetWorking(true) end
		sp.SetWorking = function(self, w) self.working = w; self:OnSetWorking(w) end
		sp.CancelWorkReservation = function() end
		for i = 1, n_workers do
			local c = make_colonist(worker_perf); c.workplace = sp
			sp.workers[1][#sp.workers[1] + 1] = c
		end
		dome.labels.WaterReclamationSpires[s] = sp
		spires[s] = sp
	end
	for _, sp in ipairs(spires) do sp:UpdatePerformance() end
	for _, sp in ipairs(spires) do sp:RecalcModifiers() end
end

function reading(sp)
	local mod = dome.label_modifiers.SupplyGridBuildings and dome.label_modifiers.SupplyGridBuildings.WaterReclamationSpireWaterConsumptionReduction
	return string.format("perf=%s automation=%s auto_perf=%s max_workers=%s workers=%d label_percent=%s dome_water=%s farm_water=%s",
		tostring(sp.performance), tostring(sp.automation), tostring(sp.auto_performance), tostring(sp.max_workers),
		#sp.workers[1], tostring(mod and mod.percent), tostring(dome.water_consumption), tostring(farm.water_consumption))
end
'''


def main():
    print("COMMAND python tools/desk_c105_water_reclamation.py")
    print("HEAD " + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=db.REPO, text=True).strip())
    bench = db.Bench("C105 Water Reclamation automation upgrade vs the spire's water saving; no fix")
    check = bench.check
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS + SETUP)
    for rel, pattern in BODIES:
        text, lo, hi = db.body(rel, pattern)
        db.load_at(rt, text, "=" + rel, lo)
        print(f"SOURCE 1.1.0 {rel}:{lo}-{hi} sha256={hashlib.sha256(text.encode()).hexdigest()[:16]}")
    wr = db.read(db.SRC_LIVE + "/Lua/Buildings/WaterReclamation.lua")
    rt.execute("WaterReclamationSpire = {}")
    db.load_at(rt, wr.replace("DefineClass.WaterReclamationSpire = ", "local _unused_classdef = "), "=Lua/Buildings/WaterReclamation.lua")
    print(f"SOURCE 1.1.0 Lua/Buildings/WaterReclamation.lua (whole) sha256={hashlib.sha256(wr.encode()).hexdigest()[:16]}")
    rt.execute(AFTER_LOAD)
    text, lo, hi = db.body("Lua/LabelContainer.lua", r"^function LabelContainer:SetLabelModifier\(")
    db.load_at(rt, "local function UpdateModWithoutCheck(obj, ...) return obj:UpdateModifier(...) end\n"
                   "local function UpdateModWithCheck(obj, action, mod, ...) if obj[mod.prop] ~= nil then return obj:UpdateModifier(action, mod, ...) end end\n"
               + text + "\nLABEL_SET = LabelContainer.SetLabelModifier", "=Lua/LabelContainer.lua", lo - 2)
    print(f"SOURCE 1.1.0 Lua/LabelContainer.lua:{lo}-{hi} (+ the two local helpers, :49-57, retyped verbatim)")
    rt.execute(FIXTURE)
    g = rt.globals()
    print()

    # A. staffed spire, skilled workers: the saving is live
    rt.execute("build_world(140, 2, 1); BEFORE = reading(spires[1])")
    print("  staffed:  " + g.BEFORE)
    check("staffed spire at 140 performance saves 70% of the dome's water (10000 -> 3000) and the farm's (5000 -> 1500)",
          rt.eval("spires[1].performance == 140 and dome.water_consumption == 3000 and farm.water_consumption == 1500"), g.BEFORE)

    # B. apply the automation upgrade through the shipped ApplyUpgrade
    rt.execute("spires[1]:ApplyUpgrade(1); AFTER = reading(spires[1])")
    print("  upgraded: " + g.AFTER)
    check("upgrade installs automation=1, auto_performance=100, max_workers=0 and dismisses both workers",
          rt.eval("spires[1].automation == 1 and spires[1].auto_performance == 100 and spires[1].max_workers == 0 and #spires[1].workers[1] == 0"),
          g.AFTER)
    check("upgraded spire's performance is 100 (the automation value)", rt.eval("spires[1].performance == 100"), g.AFTER)
    check("the saving is STILL APPLIED after the upgrade: 50% (dome 10000 -> 5000, farm 5000 -> 2500)",
          rt.eval("dome.water_consumption == 5000 and farm.water_consumption == 2500"), g.AFTER)

    # C. idempotence: the working-state refresh and later recalcs do not drift
    rt.execute("for i = 1, 5 do spires[1]:SetWorking(false); spires[1]:SetWorking(true); spires[1]:UpdatePerformance() end; AGAIN = reading(spires[1])")
    check("five more refresh cycles leave the same numbers (no drift, no loss)",
          rt.eval("dome.water_consumption == 5000 and farm.water_consumption == 2500 and spires[1].performance == 100"), g.AGAIN)

    # D. a second, still-staffed spire in the same dome: best performance wins
    rt.execute('''
        build_world(140, 2, 2)
        spires[1]:ApplyUpgrade(1)
        TWO = reading(spires[1])
    ''')
    check("two spires, one upgraded: the staffed one's 140 still sets the dome to 70%",
          rt.eval("dome.water_consumption == 3000 and farm.water_consumption == 1500"), g.TWO)

    # E. negative control: the instrument CAN show a lost saving -- remove the automation modifiers after install
    rt.execute('''
        build_world(140, 2, 1)
        spires[1]:ApplyUpgrade(1)
        for _, m in ipairs(spires[1].upgrade_modifiers["WaterReclamationSystem_JumboCave"]) do m:TurnOff() end
        spires[1]:UpdatePerformance()
        LOST = reading(spires[1])
    ''')
    print("  modifiers forced off: " + g.LOST)
    check("NEGATIVE CONTROL: with the upgrade's modifiers off and the workers gone, performance is 0 and the saving vanishes",
          rt.eval("spires[1].performance == 0 and dome.water_consumption == 10000 and farm.water_consumption == 5000"), g.LOST)

    return bench.finish("CONTROLS HOLD: on the shipped path the automation upgrade keeps a 50% saving; only modifiers switched off would zero it.")


if __name__ == "__main__":
    sys.exit(main())
