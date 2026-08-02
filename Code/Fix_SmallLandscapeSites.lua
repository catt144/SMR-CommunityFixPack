-- F33: a drone sent to a small landscaping site raises an error and drops its
-- command.
--
-- Defect: LandscapeConstructionSiteBase:GetClosestDests
-- (Lua\Landscape\LandscapeConstructionSiteBase.lua:178-193) sorts the site's
-- drone destinations by distance and then copies a fixed number of them out:
--     top_count = top_count or 5
--     ...
--     for i = 1, top_count do
--         top_dests[i] = dests[i].dest
--     end
-- with no check that there are that many. `drone_dests_cache` is built in
-- GameInit (:47-64) from the site's PERIPHERY hexes only — `if border then` — so
-- a small clear / paint / level blob has fewer than five entries, `dests[i]` is
-- nil, and indexing it raises.
--
-- The only caller is DroneApproach (:195-205), which runs inside the drone's own
-- command thread, so the error kills that thread: the drone stops mid-approach
-- and the little landscaping job never gets worked.
--
-- Patch approach: FIX_POLICY §1.4 chained PRE-wrapper — zero copied logic.
-- The shipped function already TAKES the bound as a parameter and its only
-- caller never passes it, so clamping `top_count` to the number of cached
-- destinations before delegating fixes the overrun without a body copy.
-- Layer: §3a layer 2 by construction — all of our work happens before
-- `return orig(...)`, so there is no mod frame left to run after the call.
--
-- CONVERTED 2026-08-02 from a §1.5 full replacement (SAVE_SAFETY_REDESIGN §5.4
-- group A). Before/after: the copied 15-line body is gone; behaviour is
-- unchanged. Equivalence, argument by argument —
--   * n >= 5 and no explicit top_count → clamp yields 5, vanilla's default: identical;
--   * n < top_count → the loop now runs 1..n, exactly the old copy's
--     `Min(top_count, #dests)` bound (`#dests` == `#drone_dests_cache`, because
--     table.imap builds one entry per ipairs element);
--   * n == 0 → bound 0, empty list returned, same as the copy.
-- One deliberate, documented delta: the shipped `assert(self.drone_dests_cache)`
-- is back (the copy dropped it). It is vanilla's own line, it does not unwind in
-- mod code (ENGINE_FACTS) and no fix claim rested on its absence — a nil cache
-- raises inside `table.imap` in the copy and in the wrapper alike, so nothing a
-- player can reach changed.

SMRFixPack.Register("SmallLandscapeSites", {
	title = "Drones no longer error out when sent to a small landscaping site",
	apply = function()
		local err = SMRFixPack.Require("SmallLandscapeSites", {
			{ class = "LandscapeConstructionSiteBase", method = "GetClosestDests" },
		})
		if err then return err end
		local L = LandscapeConstructionSiteBase
		local orig = L.GetClosestDests

		function L:GetClosestDests(drone, top_count)
			-- FIX (F33): clamp the bound to what the cache actually holds. The
			-- shipped body copies `top_count` entries out of the sorted list with
			-- no bounds check, and a small site's periphery is shorter than the
			-- default 5.
			local cache = self.drone_dests_cache
			local n = type(cache) == "table" and #cache or 0
			return orig(self, drone, Min(top_count or 5, n))
		end
	end,
})
