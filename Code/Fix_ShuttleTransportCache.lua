-- F51: Colonists stay homeless (or stranded in the wrong dome) after you build a
-- Shuttle Hub — the answer "there is no way to get there" is cached forever.
--
-- Defect: FindTransportationModeToCommunity (Lua\Units\Colonist.lua:2504-2537)
-- memoises the result per (community, pos) in the g_TransportationModeToCommunityCache
-- GameVar — including the negative result. But the answer also depends on the
-- third argument, `shuttles_available`, which is NOT part of the key:
--     FindTransportationModeToCommunity_BeforeTrains (:2467-2476) returns "shuttle"
--     only when that flag is set.
-- Callers recompute the flag freshly every time (FindEmigrationDome, :2650, calls
-- IsLRTransportAvailable), but the cache hands back the stale verdict regardless.
-- It is only ever flushed on TrainRoutesRebuilt / DomesConnected / DomesDisconnected
-- (:2480-2488) and when an elevator or station changes validity — building,
-- fuelling or repairing a Shuttle Hub flushes nothing. FindEmigrationDome
-- (:2657-2698) therefore keeps skipping every dome it once judged unreachable,
-- which is the "homeless despite free housing" and "seniors never move to the
-- retirement dome" report.
--
-- Patch approach: full replacement of the one caching function — a copy of
-- Lua\Units\Colonist.lua:2504-2537 (shipped Src, game 1.0.7.396349) that records which
-- shuttle availability each cached answer was computed under and recomputes when
-- it differs. The flag is stored on a NON-array key of the existing entry, so the
-- entry still unpacks to exactly (mode, dist, elevator) — a save made with this
-- mod and then loaded without it reads the cache exactly as vanilla would.
-- The file-local is_identical helper is recreated verbatim. Changes marked -- FIX.

SMRFixPack.Register("ShuttleTransportCache", {
	title = "New Shuttle Hubs are noticed: colonists stop being stuck with a cached 'unreachable'",
	apply = function()
		if type(rawget(_G, "FindTransportationModeToCommunity")) ~= "function"
				or type(rawget(_G, "GetTransportationModeToCommunity")) ~= "function" then
			return "FindTransportationModeToCommunity not found (game update changed it?)"
		end
		if type(rawget(_G, "ValidateBuilding")) ~= "function" then
			return "ValidateBuilding not found (game update changed it?)"
		end

		local function is_identical(t1, t2)
			for k, v in pairs(t1) do
				if t2[k] ~= v then
					return false
				end
			end
			for k, v in pairs(t2) do
				if t1[k] ~= v then
					return false
				end
			end
			return true
		end

		function FindTransportationModeToCommunity(community, pos, shuttles_available, source_city)
			if IsKindOf(pos, "Unit") then
				local dome = IsUnitInDome(pos)
				if dome then
					pos = dome
				else
					return GetTransportationModeToCommunity(community, pos, shuttles_available, source_city)
				end
			end
			if not IsValid(community) or not IsValid(pos) then
				return GetTransportationModeToCommunity(community, pos, shuttles_available, source_city)
			end
			g_TransportationModeToCommunityCache = g_TransportationModeToCommunityCache or {}

			local validation = {}
			for _, elevator in ipairs(UIColony.labels.Elevator) do
				validation[elevator] = ValidateBuilding(elevator)
			end
			for _, station in ipairs(UIColony.labels.Station) do
				validation[station] = ValidateBuilding(station) and station:IsWorkPossible()
			end

			if g_TransportationModeToCommunityCache.elevator_validation and not is_identical(g_TransportationModeToCommunityCache.elevator_validation, validation) then
				g_TransportationModeToCommunityCache = {}
			end
			g_TransportationModeToCommunityCache.elevator_validation = validation

			local t = g_TransportationModeToCommunityCache[community] or {}
			g_TransportationModeToCommunityCache[community] = t
			local with_shuttles = not not shuttles_available -- FIX: callers pass nil, false or true
			local entry = t[pos]
			-- FIX (F51): the cached answer depends on shuttle availability, which was
			-- not part of the key — a hub built later was never noticed.
			if not entry or entry.smr_shuttles ~= with_shuttles then
				local mode, dist, elevator = GetTransportationModeToCommunity(community, pos, shuttles_available, source_city)
				entry = { mode, dist, elevator }
				entry.smr_shuttles = with_shuttles -- hash key: does not affect table.unpack
				t[pos] = entry
			end
			return table.unpack(entry)
		end
	end,
})
