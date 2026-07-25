-- F36: Universities keep training geologists for extractors that need nobody.
--
-- Defect: City:GetNeededSpecialist (Lua\City.lua:561-593) walks every Workplace
-- and adds `max_workers` of its `specialist` to the colony's demand, gated only on
--     spec ~= "none" and ValidateBuilding(building) and building.ui_working
--     and building.max_workers > 0
-- Nothing in that test asks whether the workplace still WANTS workers.
--
-- The Extractor AI breakthrough (Data\TechPreset.lua:1050-1075) puts
-- `automation = 1` and `auto_performance = 50` on the MetalsExtractor and
-- PreciousMetalsExtractor labels. A workplace with `automation > 0` returns
-- `auto_performance` from Workplace:GetWorkshiftPerformance outright
-- (Workplace.lua:197-199) and reports HasWorkforce/HasAnyWorkers/
-- HasNearByWorkers true regardless of staffing (:137, :153, :856) — staffing it
-- changes literally nothing. Yet a Metals Extractor with specialist "geologist"
-- and max_workers 4 still contributes 12 geologists (4 per shift) to colony
-- demand, forever.
--
-- Everything downstream reads that number: MartianUniversityBase:CanTrain's
-- "train as needed" policy (MartianUniversity.lua:77), the auto specialization
-- pick on graduation (:27 -> Colony:GetMostNeededSpecialist, Colony.lua:630) and
-- the infopanel's needed-specialization list (:109). So auto universities keep
-- graduating geologists for jobs nobody has to do, which is the reported
-- "universities train geologists after Extractor AI".
--
-- Note the BUGS.md sketch proposed keying on the global g_ExtractorAIResearched.
-- That flag turns out to do only one thing in the whole codebase — silence a
-- construction warning (BaseExtractor.lua:60-68, MicroGExtractor.lua:103-111) —
-- while the actual "works without colonists" effect is the `automation` property.
-- Keying on `automation` is both the precise gameplay meaning and correct for any
-- other automated workplace (and for mods that automate one).
--
-- Patch approach: full replacement of City:GetNeededSpecialist — a copy of
-- Lua\City.lua:561-593 (shipped Src, 2026-07) with one clause added to the
-- existing gate, marked -- FIX. Replacement because the decision is inside the
-- accumulation loop: a pre-wrapper cannot reach it and a post-wrapper would have
-- to reconstruct and unpick the Max(0, …) clamp on line 587.

SMRFixPack.Register("UniversityOvertraining", {
	title = "Universities stop training specialists for workplaces that run themselves",
	apply = function()
		local C = rawget(_G, "City")
		if type(C) ~= "table" or type(C.GetNeededSpecialist) ~= "function" then
			return "City.GetNeededSpecialist not found (game update changed it?)"
		end
		-- `automation` is declared on Workplace (Workplace.lua:8); if the property
		-- is gone the gate below would silently exclude nothing. Property defaults
		-- are not copied onto the class until the classes are built, well after mod
		-- code loads, so look in the classdef's own `properties` list instead of
		-- reading Workplace.automation (which is still nil at this point).
		local W = rawget(_G, "Workplace")
		if type(W) ~= "table" or type(W.properties) ~= "table"
			or not table.find(W.properties, "id", "automation") then
			return "Workplace 'automation' property not found (game update changed it?)"
		end
		if type(rawget(_G, "ValidateBuilding")) ~= "function" then
			return "ValidateBuilding not found (game update changed it?)"
		end
		if type(rawget(_G, "ColonistSpecializationList")) ~= "table" then
			return "ColonistSpecializationList not found (game update changed it?)"
		end

		function C:GetNeededSpecialist()
			if self.needed_specialist_last_time == GameTime() then
				return self.needed_specialist_cache
			end

			local needed_specialist = {}
			for _, building in ipairs(self.labels.Workplace) do
				local spec = building.specialist
				-- FIX (F36): `and (building.automation or 0) <= 0` — an automated
				-- workplace performs at auto_performance whether or not anybody
				-- works there (Workplace.lua:197-199), so its posts are not jobs
				-- the colony needs specialists for.
				if spec ~= "none" and ValidateBuilding(building) and building.ui_working and building.max_workers > 0
					and (building.automation or 0) <= 0 then
					local count = 0
					if building.active_shift>0 then
						count = building.max_workers - (building.closed_workplaces[building.active_shift] or 0)
					else
						local max = building.max_workers
						for i = 1, building.max_shifts do
							count = count + Max(0, max - (building.closed_workplaces[i] or 0))
						end
					end
					needed_specialist[spec] = (needed_specialist[spec] or 0) + count
				end
			end
			for _, spec in ipairs(ColonistSpecializationList) do
				local specs_count = 0
				for _, colonist in ipairs(self.labels[spec]) do
					specs_count = specs_count + (colonist:CanWork() and 1 or 0)
				end
				needed_specialist[spec] =  Max(0, (needed_specialist[spec] or 0) - specs_count)
			end
			self.needed_specialist_last_time = GameTime()
			self.needed_specialist_cache = needed_specialist

			return needed_specialist
		end
	end,
})
