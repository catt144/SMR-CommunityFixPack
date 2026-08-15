-- C39: the three Automation laws cut `max_workers` by LABEL while the
-- performance compensation that is supposed to cancel that cut keys on CLASS.
-- The sets do not coincide, so the buildings on the wrong side of the line lose
-- half their staff and receive nothing back — roughly half their throughput.
--
-- THE TWO HALVES THAT DISAGREE (Src 1.0.7.396349, re-derived 2026-08-15):
--   * effect, by label — `LawEffectModifyLabel{ Label = "<X>Buildings",
--     Prop = "max_workers", Percent = -50 }`, one per law:
--     Data\LawDef\LawDef-Technology.lua:70-76   (FactoryBuildings),
--     :149-158  (ResearchBuildings), :226-235  (ServiceBuildings).
--     All three carry a `PresetParamPercent automation_workforce_reduction`
--     of -50 (:135-140, :212-217, :279-284).
--   * compensation, by class — `Workplace:GetWorkshiftPerformance` re-derives a
--     `law_scale` from that same parameter, but only under
--     `IsKindOf("Factory")` / `IsKindOf("ResearchBuilding")` /
--     `IsKindOf("Service")` (Lua\Buildings\Workplace.lua:205-218).
--
-- INTENT — an explicit dev comment, on the compensating block itself
-- (Workplace.lua:209-210): *"this code assumes that there's a modification in
-- max_workers matching the value on automation_workforce_reduction, and tries
-- to reverse its effect so that the overall performance is maintained"*. The
-- code says out loud that it assumes the two sets coincide. For the buildings
-- below they do not. This one is a plain repair, not a judgment call.
--
-- MEASURED (2026-08-11 attended sitting, log cp15sitting_Mars.exe-20260811-
-- 15.09.30, game paused for the whole bracket): subject
-- `TVStudioWorkshopCCP1#1526` and control `Diner#1475` took the IDENTICAL
-- `max_workers{percent=50}` cut; only the control was paid back — control
-- performance 114 -> 268 -> 124 across enact/revert, subject 127 -> 131 -> 129
-- while its shifts went 12/12/12 -> 6/6/6 -> 12/12/12. Full record:
-- docs/agent/bugs/C39.md. Repair ruled by the owner 2026-08-12 (extend the
-- compensation; the delabel alternative was put to them and DECLINED).
--
-- ⭐ COVERAGE — the static label sweep this module is built against
-- (docs/agent/bugs/C39.md §2026-08-15). All three labels enumerated over every
-- shipped BuildingTemplate (Lua\BuildingTemplate\*.generated.lua plus the one
-- DLC template) and each member resolved through its class chain. **EIGHT**
-- template families carry an automation label, are `Workplace`s, and fail all
-- three gates — the four known Workshops and FOUR that were never on any list:
--   ServiceBuildings   ArtWorkshop, BioroboticsWorkshop, VRWorkshop,
--                      TVStudioWorkshopCCP1   (-> Workshop = {ElectricityConsumer, Workplace})
--   ServiceBuildings   SecurityStation, SecurityPostCCP1
--                      (-> SecurityStationBase = {ElectricityConsumer, Workplace})
--   FactoryBuildings   DroneFactory       (-> {Building, ElectricityConsumer, Workplace})
--   FactoryBuildings   BottomlessPitResearchCenter
--                      (-> {Building, ElectricityConsumer, Workplace, WaypointsObj})
-- `ResearchBuildings` has NO Workplace mismatch. What the missing uplift costs
-- each family, traced to the consumer: Workshop Comfort payment
-- (ArtWorkshop.lua:24), TV-show progress (TVStudioWorkshop.lua:100),
-- neutralised renegades (SecurityStation.lua:13), drone/android build time
-- (DroneFactory.lua:73-78), resources processed into RP
-- (BottomlessPitResearchCenter.lua:45).
-- Four label members are NOT Workplaces at all — Amphitheater, OpenAirGym,
-- TaiChiGarden (`Service`, no Workplace in the chain) and MagneticFieldGenerator
-- (`OutsideBuildingWithShifts`). `max_workers` is declared ONLY on Workplace
-- (Workplace.lua:5), so the law's modifier lands on a property they do not
-- have: no cut, nothing to compensate, and `GetWorkshiftPerformance` never runs
-- for them. They are excluded by construction, not by a list.
--
-- ⚖️ DESIGN, settled here against FIX_POLICY §1 (the entry recorded two
-- candidates; this is a third that dominates both):
--   (a) the entry's post-wrapper scaling the whole result by `law_scale` —
--       rejected: it also scales the overtime additive, which vanilla adds
--       AFTER the worker loop and never scales (the entry flags this as a
--       disclosure; it is avoidable instead).
--   (b) a §1.5 body copy widening the :205-207 gate — rejected: it destroys any
--       other mod's wrapper on a hot method, and if an official patch ever
--       fixes the gate the copy silently reinstates the broken one (the §1.4b
--       warning, in the exact shape it warns about).
--   (c) SHIPPED — a §1.4 chained post-wrapper that adds the EXACT compensation
--       DELTA. It reconstructs only vanilla's per-worker loop (Workplace.lua:
--       220-228), twice: once at the `law_scale` the building should have had
--       and once at the `law_scale = 100` it actually got, and returns
--       `orig(...) + (compensated - uncompensated)`. Because the uncompensated
--       term is arithmetically identical to the loop term already inside
--       `orig`'s result, the sum equals what vanilla would have produced had
--       the gate been right — exactly, including its rounding. Every additive
--       term (overtime, RemoteFarming, anything a future patch adds) rides
--       through on `orig`'s result untouched.
-- ⚠️ §1.5 RECONSTRUCTION DISCLOSURE: the loop below is copied from
-- Workplace.lua:220-228 at 1.0.7.396349 and must be re-checked against that
-- block on every game update. It is NOT a byte-copy of the whole method — the
-- method still runs, in full, on every call.
--
-- DISCRIMINATOR — the game's own bookkeeping, no template list at runtime. A
-- law's `LawEffectModifyLabel:OnStart` registers the modifier under the EFFECT
-- OBJECT as its id (ClassDef-Factions.generated.lua:2039-2059), and
-- `ContinuousEffectsPreset:CreateInstance` gives each activated law its own
-- effect instances (CommonLua\Classes\ContinuousEffect.lua:152-163), so the
-- authoritative id lives on `ActiveLaws[<law_id>].Effects` — not on the preset.
-- A building is "mismatched" iff it carries one of those modifiers on
-- `max_workers` and fails all three gates. A future patch that widens the gate,
-- or moves the law off labels, makes this stop matching: the module becomes a
-- no-op instead of fighting the fix.
--
-- §3a SAVE-SAFETY TIER: **Layer 2 by construction, nothing persisted.** The
-- wrapper is synchronous and contains no blocking call, so no frame of ours can
-- be captured below a `Sleep`/`WaitMsg` on a game-time thread; it allocates no
-- table, stores no function value on any object, and creates no modifier, no
-- GameVar and no thread. All state read is the game's own. The wrapper lives in
-- a class table, which savegames do not serialise. Removing the mod restores
-- vanilla behaviour on the next load with nothing to clean up.

local AUTOMATION_LAWS = {
	"Policy_Automation_FactoryAutomation",
	"Policy_Automation_ResearchAutomation",
	"Policy_Automation_ServiceAutomation",
}

-- Which active Automation law's max_workers cut is THIS building carrying?
-- nil when none — and nil when more than one does, because a building on two
-- automation labels at once is a shape the 2026-08-12 ruling does not cover and
-- this module will not guess at (no shipped template carries two).
--
-- `active` is the ActiveLaws table, passed IN rather than read from _G — the
-- F97 donor pattern, so the TestKit can drive the discriminator with a fixture
-- instead of stubbing a GameVar (and can run it at the main menu, where
-- ActiveLaws does not exist yet).
local function find_automation_law(self, active)
	local mods = self.modifications
	local mod_list = mods and mods.max_workers
	if not mod_list then return end
	if type(active) ~= "table" then return end
	local found
	for _, law_id in ipairs(AUTOMATION_LAWS) do
		local law = active[law_id]
		local effects = law and law.Effects
		if type(effects) == "table" then
			local matched = false
			for _, effect in ipairs(effects) do
				if not matched and effect.Prop == "max_workers" then
					for _, modifier in ipairs(mod_list) do
						if modifier.id == effect then
							matched = true
							break
						end
					end
				end
			end
			if matched then
				if found then return end   -- two laws: decline, do not guess
				found = law
			end
		end
	end
	return found
end

-- Vanilla's per-worker loop, Workplace.lua:220-228, at an arbitrary law_scale.
-- Copied verbatim so the integer division and the remainder-on-the-first-worker
-- rounding match the shipped arithmetic exactly. The additive terms that follow
-- it in the shipped body are deliberately NOT reproduced.
local function shift_loop_performance(workers, law_scale, max_workers)
	local part_per_worker = law_scale / max_workers
	local part_rem_add = law_scale % max_workers
	local performance = 0
	for _, worker in ipairs(workers) do
		performance = performance + MulDivRound(Max(worker.performance, 25), part_per_worker + part_rem_add, 100)
		part_rem_add = 0
	end
	return performance
end

-- The exact amount `orig`'s answer is short by, or 0 when this call is none of
-- our business. Every early return here mirrors one of vanilla's own.
local function compensation_delta(self, shift, active)
	-- cheapest and most selective test first: almost no building in a colony
	-- carries a max_workers modifier at all
	local law = find_automation_law(self, active)
	if not law then return 0 end

	-- vanilla returns before the loop in all three of these cases
	-- (Workplace.lua:185-202) — there is no loop term to correct
	if self:IsShroudedInRubble() then return 0 end
	if (self.automation or 0) > 0 then return 0 end
	local max_workers = self.max_workers
	if type(max_workers) ~= "number" or max_workers <= 0 then return 0 end

	-- already paid by the shipped gate (Workplace.lua:205-207)
	if self:IsKindOf("Factory") or self:IsKindOf("ResearchBuilding") or self:IsKindOf("Service") then
		return 0
	end

	-- vanilla's shift resolution (Workplace.lua:188-195)
	if self.active_shift > 0 then shift = self.active_shift end
	local workers = self.workers and self.workers[shift]
	if not workers or #workers == 0 then return 0 end

	-- vanilla's law_scale (Workplace.lua:209-218)
	local reduction = law:GetParameterValue("automation_workforce_reduction")
	if type(reduction) ~= "number" then return 0 end
	local pre_auto_workers = self.base_max_workers
	if type(pre_auto_workers) ~= "number" then return 0 end
	local post_auto_workers = MulDivRound(pre_auto_workers, 100 + reduction, 100)
	if post_auto_workers <= 0 then return 0 end
	local law_scale = MulDivRound(pre_auto_workers, 100, post_auto_workers)
	if law_scale == 100 then return 0 end

	return shift_loop_performance(workers, law_scale, max_workers)
		- shift_loop_performance(workers, 100, max_workers)
end

SMRFixPack.Register("AutomationLawCompensation", {
	title = "Automation laws pay back the buildings they take workers from — Workshops, Security Stations, the Drone Assembler and the Bottomless Pit no longer lose half their output",
	-- exposed for the TestKit (the F97 donor pattern): the discriminator and
	-- the arithmetic, both pure and both drivable with a fixture
	find_automation_law = find_automation_law,
	compensation_delta = compensation_delta,
	apply = function()
		local err = SMRFixPack.Require("AutomationLawCompensation", {
			-- the DECLARING class (FIX_POLICY §2): Workplace.lua:184
			{ class = "Workplace", method = "GetWorkshiftPerformance" },
			-- declared on Shroudable (Shroudable.lua:15), which Building lists
			-- among its parents (Building.lua:150-155) — checking it on
			-- Workplace would read nil before flattening (the F64 lesson)
			{ class = "Shroudable", method = "IsShroudedInRubble" },
			{ global = "MulDivRound" },
			{ global = "Max" },
			-- `base_max_workers` is created by Modifiable:InitBaseProperties for
			-- every modifiable property; if `max_workers` stopped being
			-- modifiable there would be no cut to compensate. Property defaults
			-- are not on the class until flattening, so read the classdef's own
			-- property list (the Fix_UniversityOvertraining donor).
			{ test = function()
					local W = rawget(_G, "Workplace")
					if type(W) ~= "table" or type(W.properties) ~= "table" then return false end
					local meta = table.find_value(W.properties, "id", "max_workers")
					return meta and meta.modifiable and true or false
				end,
			  reason = "Workplace 'max_workers' is no longer a modifiable property (game update changed it?)" },
		})
		if err then return err end

		local orig = Workplace.GetWorkshiftPerformance

		function Workplace:GetWorkshiftPerformance(shift)
			local performance = orig(self, shift)
			-- FIX (C39): pay the label-carrying, out-of-class Workplaces the
			-- uplift the shipped gate cannot reach them with. Inert — and
			-- exactly `orig`'s own answer — for every other building.
			if type(performance) ~= "number" then return performance end
			local delta = compensation_delta(self, shift, rawget(_G, "ActiveLaws"))
			if delta == 0 then return performance end
			return performance + delta
		end

		if Workplace.GetWorkshiftPerformance == orig then
			return "could not install the Workplace.GetWorkshiftPerformance wrapper"
		end
	end,
})
