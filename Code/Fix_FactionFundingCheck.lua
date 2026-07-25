-- F10: Faction income conditions permanently fail (Blue Sun / Brazil / Russia).
--
-- Defect: Funding:GetLastSolsFundingByType (Lua\Funding.lua:104-117) iterates
--     pairs(UIColony.funds.funding_gain_last_hours and ...[hour])
-- but the per-hour table exists only for hours in which positive funding was
-- gained (ChangeFunding, Funding.lua:52-65). For any hour without income — most
-- hours — the expression is nil and pairs(nil) raises, aborting the condition.
-- Faction content calls this directly (Data\FactionDef\BlueSun.lua:34,54,
-- Brazil.lua:42, Russia.lua:84), so goals/opportunities gated on recent export or
-- tourism income can never evaluate true.
--
-- Patch approach: replacement of the one method with nil-guarded iteration (copy
-- of Funding.lua:104-117, shipped Src 2026-07; the source-to-type remap is a file
-- local, recreated identically). Changes marked -- FIX.

SMRFixPack.Register("FactionFundingCheck", {
	title = "Faction goals based on recent export/tourism income can now trigger",
	apply = function()
		if not (rawget(_G, "Funding") and type(Funding.GetLastSolsFundingByType) == "function") then
			return "Funding.GetLastSolsFundingByType not found (game update changed it?)"
		end

		local funding_source_to_exports_type = {
			["Exports"] = { Export = true },
			["Tourist Profits"] = { Tourist = true, Celebrity = true },
			["Exports + Tourist Profits"] = { Tourist = true, Celebrity = true, Export = true },
		}

		function Funding:GetLastSolsFundingByType(sols, exports_type)
			local total = 0
			local remap = funding_source_to_exports_type[exports_type]
			if not remap or not next(remap) then return end -- FIX: nil-guard unknown type
			local per_hour = UIColony.funds.funding_gain_last_hours or empty_table -- FIX: nil-guard
			local abs_hour = UIColony.day * const.HoursPerDay + UIColony.hour
			for hour = abs_hour - sols * const.HoursPerDay + 1, abs_hour do
				for source, funding in pairs(per_hour[hour] or empty_table) do -- FIX: hours without income have no table
					if remap[source] then
						total = total + funding
					end
				end
			end
			return total
		end
	end,
})
