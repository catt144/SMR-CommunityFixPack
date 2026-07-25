-- F33: a drone sent to a small landscaping site raises an error and drops its
-- command.
--
-- Defect: LandscapeConstructionSiteBase:GetClosestDests
-- (Lua\Landscape\LandscapeConstructionSiteBase.lua:178-192) sorts the site's
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
-- The only caller is DroneApproach (:194-205), which runs inside the drone's own
-- command thread, so the error kills that thread: the drone stops mid-approach
-- and the little landscaping job never gets worked.
--
-- Patch approach: full replacement of GetClosestDests — a copy of
-- Lua\Landscape\LandscapeConstructionSiteBase.lua:178-192 (shipped Src, 2026-07)
-- with the loop bound clamped, marked -- FIX. Replacement rather than a wrapper
-- because the fault is inside the loop: a pre-wrapper cannot prevent it and a
-- post-wrapper never runs.
--
-- The shipped `assert(self.drone_dests_cache)` is dropped: assert does not unwind
-- in mod code, so it only prints, and with the clamp in place a missing cache now
-- yields an empty list instead of an error. `drone:Goto` already handles being
-- given nothing to go to.

SMRFixPack.Register("SmallLandscapeSites", {
	title = "Drones no longer error out when sent to a small landscaping site",
	apply = function()
		local L = rawget(_G, "LandscapeConstructionSiteBase")
		if type(L) ~= "table" or type(L.GetClosestDests) ~= "function" then
			return "LandscapeConstructionSiteBase.GetClosestDests not found (game update changed it?)"
		end
		if type(rawget(_G, "table")) ~= "table" or type(table.imap) ~= "function" then
			return "table.imap not found (game update changed it?)"
		end

		function L:GetClosestDests(drone, top_count)
			top_count = top_count or 5

			local dests = table.imap(self.drone_dests_cache, function(dest)
				return {dest = dest, dist2 = dest:Dist2(drone)}
			end)
			table.sort(dests, function(a, b) return a.dist2 < b.dist2 end)

			local top_dests = {}
			-- FIX (F33): was `for i = 1, top_count`. A site whose periphery is
			-- smaller than top_count has fewer destinations than that, and
			-- dests[i].dest then indexes a nil.
			for i = 1, Min(top_count, #dests) do
				top_dests[i] = dests[i].dest
			end

			return top_dests
		end
	end,
})
