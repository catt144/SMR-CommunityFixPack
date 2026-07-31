-- F34(d): the units-underneath sweep on a landscaping site ignores its own
-- filter, so boarding colonists are yanked out of the vehicle they are entering
-- and the same unit can be handled more than once.
--
-- Defect: LandscapeForEachUnit (Lua\Landscape\Landscaping.lua:455-469) builds a
-- filter and then hands the raw callback to the engine anyway:
--     local passed = {}
--     local function filter_embark(o, ...)
--         if IsValid(o) and not passed[o] and o.command ~= "Embark" then
--             passed[o] = true
--             callback(o, ...)
--         end
--     end
--     Landscape_ForEachObject(landscape, landscape.grid, foreach_params_unit, callback, ...)
--                                                                            ^^^^^^^^
-- `filter_embark` is never used. The function directly above it,
-- LandscapeForEachStockpile (:436-451), is written identically and DOES pass its
-- filter (`filter_parent`) — the slip is a copy-paste, not a decision.
--
-- Two things are lost:
--   * the Embark exclusion. That the exclusion is intended is settled by the
--     ordinary construction site, which applies exactly the same rule to exactly
--     the same question: ConstructionSite:GetUnitsUnderneath passes
--     `exit_impassable_filter`, i.e. `obj.command ~= "Embark"`
--     (Lua\Buildings\ConstructionSite.lua:1713-1720);
--   * the `passed` de-duplication — the engine sweep can visit an object more
--     than once, which is why every sibling here keeps that table.
--
-- The consumer is LandscapeConstructionSite:GetUnitsUnderneath
-- (LandscapeConstructionSite.lua:21-27), whose list is scattered by
-- ConstructionSite:ScatterUnitsUnderneath (:1722-1740) with
-- `u:SetCommand("ExitImpassable")`. So placing a landscaping job over a rocket,
-- train or shuttle boarding point interrupts the colonists in the middle of
-- boarding it, and does so repeatedly for any unit the sweep reports twice.
--
-- Patch approach: full replacement of the global LandscapeForEachUnit — a copy of
-- Lua\Landscape\Landscaping.lua:455-469 (shipped Src, game 1.0.7.396349) with the argument
-- corrected, marked -- FIX. The file-local `foreach_params_unit` (:452-454) is
-- reproduced verbatim, a file-local being unreachable from here. Replacement
-- rather than a wrapper because the wrong argument is the whole defect.
--
-- The other three items filed under F34 are NOT patched — see the BUGS.md entry:
-- (a) and (b) are nil-indexes no shipped caller can reach, and (c) would need a
-- behavior change (skipping hexes another mark already owns), not a guard.

SMRFixPack.Register("LandscapeUnitFilter", {
	title = "Landscaping over a boarding point no longer drags boarding colonists out",
	apply = function()
		local err = SMRFixPack.Require("LandscapeUnitFilter", {
			{ global = "LandscapeForEachUnit" },
			{ global = "Landscape_ForEachObject" },
		})
		if err then return err end
		-- Landscapes is a GameVar (Landscaping.lua:21) and does not exist yet, so
		-- it is read inside the function, never here.

		-- Reproduced from the file-local at Landscaping.lua:452-454.
		local foreach_params_unit = {
			accept = { "Unit", },
		}

		function LandscapeForEachUnit(mark, callback, ...)
			local landscape = Landscapes[mark]
			if not landscape then
				return
			end

			local passed = {}
			local function filter_embark(o, ...)
				if IsValid(o) and not passed[o] and o.command ~= "Embark" then
					passed[o] = true
					callback(o, ...)
				end
			end
			-- FIX (F34d): was `callback` — the filter above was built and then
			-- never used, so boarding units were reported and duplicates were not
			-- collapsed.
			Landscape_ForEachObject(landscape, landscape.grid, foreach_params_unit, filter_embark, ...)
		end
	end,
})
