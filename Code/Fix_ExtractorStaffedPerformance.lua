-- F108: Extractor AI caps STAFFED Metals / Rare Metals Extractors at 50, which
-- makes Russia's own "3 Extractors at 160 Performance" sponsor goal unreachable.
--
-- Defect: the Extractor AI breakthrough (Data\TechPreset.lua:1050-1075) puts
-- `automation = 1` and `auto_performance = 50` on the MetalsExtractor and
-- PreciousMetalsExtractor labels. Workplace:GetWorkshiftPerformance returns
-- `auto_performance` OUTRIGHT whenever `automation > 0` (Workplace.lua:197-199),
-- on an early branch ABOVE the worker loop at :219 — so a fully STAFFED extractor
-- is pinned at 50 and its workers, overtime and every performance boost are
-- discarded. The tech's own text scopes the 50 to unmanned use: "Metals
-- Extractors and Rare Metals Extractors can work WITHOUT Colonists at 50
-- Performance" (TechPreset.lua ExtractorAI description). The code applies it with
-- Colonists too. Downstream, the Roscosmos (Russia) sponsor goal
-- `ExtractorPerformance` (Data\SponsorGoals.lua:467-492; goal_4_param 3 / 160 on
-- Roscosmos, Data\MissionSponsorPreset.lua) counts MetalsExtractor /
-- PreciousMetalsExtractor with `extractor.performance >= 160`, so once Extractor
-- AI is researched the goal is PERMANENTLY unreachable — a breakthrough cannot be
-- un-researched. Matches a Steam Workshop field report, 2026-08-28.
--
-- Owner ruling (2026-08-28): FLOOR, not ceiling. A STAFFED automated metals
-- extractor earns the greater of its worker performance and `auto_performance`;
-- 50 stays a guaranteed floor for UNMANNED operation instead of a hard ceiling.
-- To exceed 50 the player still pays the full geologist cost, exactly as a player
-- without the breakthrough does — so this removes the trap without buffing the
-- tech into a free lunch. Scoped to MetalExtractorWorkplace (MetalsExtractor.lua:
-- 21), the common Workplace ancestor of the two staffable extractors; the
-- always-unmanned AutomaticMetalsExtractor is NOT under it and is left alone.
--
-- SHAPE — a §1.4 chained POST-wrapper, deliberately NOT a body copy.
-- Workplace:GetWorkshiftPerformance is ALREADY wrapped by
-- Fix_AutomationLawCompensation (C39); a full-body replacement (the F36 style)
-- would blow that wrapper away depending on load order (the §1.4b warning). The
-- two are orthogonal and compose in EITHER load order: C39 returns a 0 delta for
-- `automation > 0` (its :175 guard), this module acts ONLY on `automation > 0`
-- extractors, and both call `orig`.
--
-- §1.5 RECONSTRUCTION DISCLOSURE: staffed_performance() below reproduces vanilla's
-- per-worker loop (Workplace.lua:219-228) plus the overtime additive (:230-233).
-- It runs at `law_scale = 100` because these extractors are Mine / ExtractorWorkplace,
-- never Factory / ResearchBuilding / Service, so vanilla's law lookup
-- (Workplace.lua:204-206) returns nil and its law_scale is always 100 for them.
-- No RemoteFarming term — extractors are not farms. Re-check this loop against
-- that block on every game update. `orig` still runs in full on every call; only
-- the automated-and-staffed extractor branch ever adds anything.
--
-- §3a SAVE-SAFETY TIER: Layer 2, nothing persisted. The wrapper is synchronous
-- with no blocking call, allocates nothing it keeps, stores no function value on
-- any object, and creates no GameVar, modifier or thread. It lives in a class
-- table, which savegames do not serialise. Removing the mod restores vanilla on
-- the next load with nothing to clean up.

-- Vanilla's staffed-shift performance for an extractor: the per-worker loop at
-- law_scale 100 (Workplace.lua:219-228), plus the overtime additive (:230-233).
local function staffed_performance(self, shift)
	if self.active_shift > 0 then shift = self.active_shift end
	local workers = self.workers and self.workers[shift]
	if not workers or #workers == 0 then return 0 end
	local max_workers = self.max_workers
	if type(max_workers) ~= "number" or max_workers <= 0 then return 0 end

	local part_per_worker = 100 / max_workers
	local part_rem_add = 100 % max_workers
	local performance = 0
	for _, worker in ipairs(workers) do
		performance = performance + MulDivRound(Max(worker.performance, 25), part_per_worker + part_rem_add, 100)
		part_rem_add = 0
	end
	if self.overtime and self.overtime[shift] then
		performance = performance + g_Consts.OvertimedShiftPerformance
	end
	return performance
end

SMRFixPack.Register("ExtractorStaffedPerformance", {
	title = "Extractor AI no longer caps STAFFED Metals / Rare Metals Extractors at 50 — staffing them raises performance again, so Russia's 160-Performance sponsor goal is reachable",
	-- exposed for the TestKit (the F97 donor pattern): pure, fixture-drivable
	staffed_performance = staffed_performance,
	apply = function()
		local err = SMRFixPack.Require("ExtractorStaffedPerformance", {
			-- the DECLARING class (FIX_POLICY §2): Workplace.lua:184
			{ class = "Workplace", method = "GetWorkshiftPerformance" },
			{ global = "Max" },
			{ global = "MulDivRound" },
			-- the extractor scope and the two properties the branch reads. Classes
			-- exist at load; property DEFAULTS are not copied onto the class until
			-- flattening, so look in the classdef's own `properties` list (the
			-- Fix_UniversityOvertraining donor), never read Workplace.automation.
			{ test = function()
					return rawget(_G, "MetalExtractorWorkplace") ~= nil
				end,
			  reason = "MetalExtractorWorkplace class not found (game update changed the extractor hierarchy?)" },
			{ test = function()
					local W = rawget(_G, "Workplace")
					return type(W) == "table" and type(W.properties) == "table"
						and table.find(W.properties, "id", "automation")
						and table.find(W.properties, "id", "auto_performance") and true or false
				end,
			  reason = "Workplace 'automation'/'auto_performance' properties not found (game update changed them?)" },
		})
		if err then return err end

		local orig = Workplace.GetWorkshiftPerformance

		function Workplace:GetWorkshiftPerformance(shift)
			local performance = orig(self, shift)
			if type(performance) ~= "number" then return performance end
			-- FIX (F108): a STAFFED automated metals extractor earns its workers'
			-- performance; `orig` (vanilla, or C39's wrapper) has already returned
			-- the flat `auto_performance` for it. 50 stays the floor. Inert for
			-- every non-extractor and every unstaffed extractor — staffed_performance
			-- returns 0 with no workers, so `orig`'s answer stands.
			if (self.automation or 0) > 0 and self:IsKindOf("MetalExtractorWorkplace") then
				local staffed = staffed_performance(self, shift)
				if staffed > performance then return staffed end
			end
			return performance
		end

		if Workplace.GetWorkshiftPerformance == orig then
			return "could not install the Workplace.GetWorkshiftPerformance wrapper"
		end
	end,
})
