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
		-- F115 (2026-09-08, CONFIRMED LIVE on 1.1.0, owner repro): the body below
		-- is a 1.0.7 copy of the global LandscapeForEachUnit, and game 1.1.0 changed
		-- that global's SIGNATURE -- `(mark, callback, ...)` became
		-- `(map, mark, callback, ...)` (Landscaping.lua:509) -- so every argument
		-- arrives one slot late, and it moved the landscape store from a GameVar to
		-- `MapVar("Landscapes", {})` (:21), read as `map.Landscapes[mark]`. Our body
		-- indexes the bare global and raises "attempt to index a nil value (global
		-- 'Landscapes')" on every landscaping site, aborting ConstructionSite:
		-- Initialize mid-body. Owner ruled GATE, not repair (decision 109): a repair
		-- would pin us to 1.1.0's signature and re-break on the next change.
		--
		-- THE DISCRIMINATOR, and why it is this one. The name still exists, so
		-- `{ global = "LandscapeForEachUnit" }` cannot see this, and arity is
		-- unreadable (`debug.getinfo` is absent in the mod sandbox). What IS
		-- readable is the exact expression that throws:
		--   * GameVar(name, ...) rawsets the global to `false` when it registers
		--     (lib.lua:1069-1071), so on 1.0.7 `Landscapes` was a real global key;
		--   * MapVar(name, ...) registers into MapVars/MapVarValues and NEVER
		--     touches _G (lib.lua:984-1000), so on 1.1.0 the global is nil.
		-- Both run at the top level of Lua/Landscape/Landscaping.lua:21, and
		-- autorun.lua:432-434 runs `dofolder("Lua")` -> `DlcsLoadCode()` ->
		-- `ModsLoadCode()`, so the whole game tree has registered before any line of
		-- ours loads. The registry is therefore populated when this runs -- that is
		-- the load-order check this gate depends on, and it is static, not assumed.
		-- ⛔ 1.0.7 SIDE UNVERIFIABLE: the 1.0.7 tree is gone from disk (EF-075), so
		-- "Landscapes was a GameVar" rests on this module's own header and F115, not
		-- on a re-read. If that is wrong the module also declines on 1.0.7 -- SAFE
		-- (vanilla's working-but-F34(d)-buggy body is restored) and inert, since the
		-- 1.0.7 branch has no players. The 1.1.0 side is read from the shipped tree.
		local function landscapes_is_per_map()
			-- MapVarValues is the engine's own "already registered" test (lib.lua:991).
			local mvv = rawget(_G, "MapVarValues")
			return type(mvv) == "table" and mvv["Landscapes"] ~= nil
		end

		local err = SMRFixPack.Require("LandscapeUnitFilter", {
			{ global = "LandscapeForEachUnit" },
			{ global = "Landscape_ForEachObject" },
			-- THE GATE. A `{ global }` check on purpose rather than a `test`: it is
			-- the literal expression the shipped body raises on, and Require marks
			-- `update_suspect` natively for shape specs while deliberately exempting
			-- `test` ones (00_Core.lua:157-163), so this route needs no hand-written
			-- mark and cannot be lost if that hand-written mark is ever wrong.
			{ global = "Landscapes", kind = "any",
			  reason = "the global Landscapes table is gone (game update changed it?)" },
			-- Belt to the above's braces: if some other mod defines a global named
			-- `Landscapes`, the check above passes on 1.1.0 and we would install the
			-- very P1 this gate exists to stop. Registration is the fact that cannot
			-- be faked by a stray global.
			{ test = function() return not landscapes_is_per_map() end,
			  reason = "the landscape data is per-map now (game update changed it?)" },
		})
		if err then
			-- This is patch ROT (a pinned body over a rewritten function), not an
			-- "already handled?" verdict, so it must be named in the update report.
			-- Require covers the `{ global }` route; the `test` route it exempts, so
			-- mark that one here. `run_apply` clears `update_suspect` only on the
			-- ACTIVE branch (00_Core.lua:411), so a write before returning survives.
			if landscapes_is_per_map() then
				local entry = SMRFixPack.fixes["LandscapeUnitFilter"]
				if entry then entry.update_suspect = true end
			end
			return err
		end
		-- On the 1.0.7 shape Landscapes is a GameVar holding `false` until a game
		-- starts, so its VALUE is still read inside the function, never here.

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
