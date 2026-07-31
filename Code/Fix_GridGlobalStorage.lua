-- F22: `GetGridGlobalStorage` adds up two maps' "hours of autonomy" and counts a
-- map with no demand as ~41 sols, so conditions built on it stop meaning anything
-- once a second map is loaded.
--
-- Defect (`Lua\ResourceOverview.lua:880-899`):
--     function GetGridGlobalStorageInSols(city, grid_type)
--         ...
--         if required == 0 then
--             return 1000 * const.HourDuration      -- "unlimited" sentinel
--         end
--         return ro[stored_fn](ro) / required * const.HourDuration
--     end
--     function GetGridGlobalStorage(grid_type)
--         ... return GetGridGlobalStorageInSols(MainCity, X)
--                  + GetGridGlobalStorageInSols(UndergroundMap and UndergroundMap.City, X)
-- Two things go wrong once the Underground map exists:
--   * the sentinel is 1000 hours of game time (const.HourDuration is per HOUR,
--     so 1000 * it, not 1000 sols) — about 41 sols. An underground city with no
--     demand yet contributes that to the sum, which is 20x the "> 2 sols"
--     threshold on its own. Every `> 2 sols` test is then permanently true and
--     every `== 0` test permanently false, no matter what the surface does.
--   * even without the sentinel, adding two ratios is not a ratio: 1 sol of
--     reserve on the surface plus 1 sol underground reads as 2 sols of reserve,
--     which is true of neither map nor of the colony.
--
-- The tests are the six Last Transmission storage conditions
-- (`Data\FactionDef\LastTransmission.lua:103-184`) and, in general, any
-- `ScriptCheckGridGlobalStorage` a storybit or mod places
-- (`ClassDef-Conditions.generated.lua:2040`).
--
-- Patch approach: replace the global `GetGridGlobalStorage` with one that
-- aggregates the INPUTS instead of the answers — sum stored and sum required
-- across the same two cities the shipped function names, then take one ratio.
-- Assigning a global from mod code reaches the real `_G` through
-- `ModEnvMeta.__newindex` (Mod.lua:1557-1563), and the shipped callers are
-- generated closures that resolve the name at call time, so they pick this up.
--
-- Three deliberate properties:
--   * `stored == 0` now returns 0. That is what makes `== 0` ("No Power stored")
--     reachable again, and it is literally true: nothing stored is nothing
--     stored, demand or no demand.
--   * the "unlimited" sentinel is kept for the case it was written for — real
--     storage with no demand at all — so a colony that has banked power and
--     switched everything off still counts as having reserves.
--   * `GetGridGlobalStorageInSols` is NOT touched. Its per-city semantics are
--     self-consistent and it is a public global other code may call; only the
--     colony-wide combination was wrong.
--
-- Arithmetic is copied exactly, including that `/` truncates in this engine, so
-- the threshold a condition must clear is unchanged for a single-map colony.
--
-- Scope note: the aggregate covers the surface and the Underground, the two maps
-- the shipped function looks at. Asteroid maps are not added — that would change
-- how hard the shipped conditions are to satisfy, which is a balance decision,
-- not a defect repair (FIX_POLICY §4).

SMRFixPack.Register("GridGlobalStorage", {
	title = "Colony-wide power/water/oxygen reserve is measured as one ratio again",
	apply = function()
		if type(rawget(_G, "GetGridGlobalStorage")) ~= "function" then
			return "GetGridGlobalStorage not found (game update changed it?)"
		end
		if type(rawget(_G, "GetCityResourceOverview")) ~= "function" then
			return "GetCityResourceOverview not found (game update changed it?)"
		end

		-- Same table the shipped GetGridGlobalStorageInSols uses
		-- (ResourceOverview.lua:874-878), restated because it is a file-local there.
		local getters = {
			Power  = { "GetTotalStoredPower", "GetTotalRequiredPower" },
			Water  = { "GetTotalStoredWater", "GetTotalRequiredWater" },
			Oxygen = { "GetTotalStoredAir",   "GetTotalRequiredAir" },
		}

		local replacement = function(grid_type)
			local fns = getters[grid_type]
			-- shipped falls off the end (returns nil) for an unknown type
			if not fns then return end
			local stored_fn, required_fn = fns[1], fns[2]

			local stored, required = 0, 0
			local function add(city)
				if not city then return end
				local ro = GetCityResourceOverview(city)
				if type(ro) ~= "table" or type(ro[stored_fn]) ~= "function"
					or type(ro[required_fn]) ~= "function" then
					return
				end
				stored = stored + (ro[stored_fn](ro) or 0)
				required = required + (ro[required_fn](ro) or 0)
			end
			add(MainCity)
			local underground = rawget(_G, "UndergroundMap")
			add(underground and underground.City)

			-- FIX (F22): nothing banked is nothing banked — this is the value the
			-- shipped `== 0` conditions were written against.
			if stored <= 0 then return 0 end
			-- FIX (F22): the sentinel now applies to the COLONY having no demand,
			-- not to either map having none.
			if required <= 0 then return 1000 * const.HourDuration end
			-- FIX (F22): one ratio over the summed inputs, not a sum of ratios.
			return stored / required * const.HourDuration
		end

		local err = SMRFixPack.SetGlobal("GetGridGlobalStorage", replacement,
			"could not replace the global GetGridGlobalStorage")
		if err then return err end
		SMRFixPack.GetGridGlobalStorage = replacement   -- exposed for the probe
	end,
})
