-- F44: Salvaging one track hex can delete the entire track — and every train
-- assigned to it.
--
-- Defect: TrackGridElement:DemolishAndSplitTrack (Lua\Buildings\TrackElement.lua:
-- 448-578) expands the deletion zone outwards to the nearest element that is
-- BOTH pillared and straight (:479-486):
--     repeat first = first + 1 until not all_elements[first] or (all_elements[first].pillared and IsTrackElementStraight(all_elements[first]))
-- Curves are pillared but never straight (IsTrackElementStraight, :52-65, needs
-- both connection deltas in {0,2}), so on a curved run the search walks off the
-- end of the array. `first` becomes n+1, `last` becomes 0, and both remainder
-- checks (:503, :519) then conclude the track is unsalvageable and call
--     track_obj:OnDemolish()
-- which deletes the whole track and calls DestroyAssignedTrains (Track.lua:248-284,
-- :158-165). The same nuke fires on any track short enough that one side of the
-- click has fewer than two elements. Element salvage is instant with no
-- countdown (:259-261), so the first the player knows of it is an entire line and
-- its trains gone. Matches the long-standing Martian Express reports.
--
-- Patch approach: the defect is mid-function, so this is a full replacement of
-- the method — a copy of Lua\Buildings\TrackElement.lua:448-578 (shipped Src,
-- game 1.0.7.396349) with three changes, all marked -- FIX:
--   1. when no pillared+straight anchor exists, the deletion zone stops at the
--      clicked element's neighbour instead of running off the array. A curved
--      track then loses exactly the hex that was clicked.
--   2. the two "remainder too short" fallbacks trim the deletion zone
--      element-by-element instead of demolishing the whole track. Nothing that
--      was not in the deletion zone is touched, and no train is destroyed.
--   3. UpdateEndElements is guarded — with (2) a trim can now empty the track,
--      which auto-deletes it (TrackElement.lua:203-207).
-- Also folds in the tolerant sort comparator promised by F45, so a repair site
-- that predates that fix cannot abort a salvage before anything is deleted.
--
-- Deliberately unchanged: mass_delete (Ctrl+click) still demolishes the whole
-- track, which is what it is for.

SMRFixPack.Register("TrackSalvageWipe", {
	title = "Salvaging one track piece no longer deletes the whole track and its trains",
	apply = function()
		local E = rawget(_G, "TrackGridElement")
		if type(E) ~= "table" or type(E.DemolishAndSplitTrack) ~= "function" then
			return "TrackGridElement.DemolishAndSplitTrack not found (game update changed it?)"
		end
		for _, name in ipairs{ "IsTrackElementStraight", "ResolveMap", "ExpandTrackFromElement",
				"ProcessTrackElements", "RebuildTrainRoutes", "PlaceObjectIn" } do
			if type(rawget(_G, name)) ~= "function" then
				return name .. " not found (game update changed it?)"
			end
		end

		function E:DemolishAndSplitTrack(mass_delete, skip_track_process)
			local track_obj = self.track_obj
			-- FIX (F44, playtest PT-03 2026-07-25): an element orphaned by an
			-- earlier corrupted split has track_obj == false, and the shipped
			-- body then raises on every click — the debris becomes immune to
			-- salvage. Treat it as the loose piece it is: delete just it.
			if not track_obj then
				DoneObject(self)
				return
			end
			-- Repair construction sites (with a broken real element) delegate to demolishing the real element
			if self.is_construction_site and IsValid(self.broken) and table.find(track_obj.elements, self.broken) then
				return self.broken:Demolish(mass_delete)
			end

			-- Build a combined list of all elements sorted by node_idx to reflect their physical order along
			-- the track. Both .elements (completed) and .elements_under_construction may be mixed along it.
			local all_elements = {}
			for _, el in ipairs(track_obj.elements) do
				all_elements[#all_elements + 1] = el
			end
			for _, el in ipairs(track_obj.elements_under_construction) do
				all_elements[#all_elements + 1] = el
			end
			-- FIX (F44/F45 rework, playtest PT-03 2026-07-25): the earlier
			-- comparator sorted a never-stamped node_idx as -1 and CARRIED ON —
			-- but the zone math below assumes sorted order == physical order, so
			-- proceeding with a scrambled list deletes a physically scattered
			-- zone and strands fragments no seed can reach (the corrupted-track
			-- report from the playtest). Stamp what can be stamped, and if any
			-- element still has no numeric node_idx, decline the partial salvage
			-- entirely — the shipped code's abort point, minus its raise. Nothing
			-- is deleted on the decline path.
			for _, el in ipairs(all_elements) do
				if type(el.node_idx) ~= "number" and el.is_construction_site
						and IsValid(el.broken) and type(el.broken.node_idx) == "number" then
					el.node_idx = el.broken.node_idx
				end
			end
			for _, el in ipairs(all_elements) do
				if type(el.node_idx) ~= "number" then
					return
				end
			end
			table.sort(all_elements, function(a, b) return a.node_idx < b.node_idx end)

			local idx = table.find(all_elements, self)
			if mass_delete or not idx then
				track_obj:OnDemolish()
				return
			end

			-- We're about to delete some elements from this track, which will tamper with its connection shape.
			-- If the track is tunneling power, it needs to be disconnected before it loses any elements.
			if track_obj.supply_tunnel_set then
				track_obj:DisconnectFromGrids()
			end

			-- find next and previous pillared elements where the resulting tracks would start/end
			local n = #all_elements
			local first, last = idx, idx
			repeat
				first = first + 1
			until not all_elements[first] or (all_elements[first].pillared and IsTrackElementStraight(all_elements[first]))
			repeat
				last = last - 1
			until not all_elements[last] or (all_elements[last].pillared and IsTrackElementStraight(all_elements[last]))
			-- FIX (F44): a curved run has no pillared+straight element at all, and the
			-- shipped search then reports the deletion zone as the whole track.
			-- Fall back to the clicked element's own neighbours.
			if not all_elements[first] then first = Min(first, idx + 1) end
			if not all_elements[last] then last = Max(last, idx - 1) end

			local map = ResolveMap(self)
			local s1, s2 = track_obj:GetStartStation(), track_obj:GetEndStation()
			Msg("StationsDisconnected", s1, s2, track_obj)

			-- Remove an element from its source array on track_obj.
			-- Regular construction sites (no broken) live in elements_under_construction;
			-- completed elements and repair construction sites (with broken) live in elements.
			local function remove_from_track_arrays(el)
				if el.is_construction_site and not IsValid(el.broken) then
					table.remove_value(track_obj.elements_under_construction, el)
				else
					table.remove_value(track_obj.elements, el)
				end
			end

			if last <= 1 then
				-- shorten the track from the start: keep all_elements[first..n]
				-- FIX (F44): removed `if n - first < 2 then track_obj:OnDemolish() return end`.
				-- A short remainder is no reason to delete the rest of the line and
				-- every train assigned to it; trim the deletion zone and stop.
				map:SuspendPassEdits("TrackElement:Demolish")
				for i = 1, first - 1 do
					local el = all_elements[i]
					remove_from_track_arrays(el)
					DoneObject(el)
				end
				map:ResumePassEdits("TrackElement:Demolish")
				if IsValid(track_obj) then -- FIX (F44): the trim can now empty (and auto-delete) the track
					track_obj:UpdateEndElements()
				end
			elseif first >= n then
				-- shorten the track from the end: keep all_elements[1..last]
				-- FIX (F44): removed `if last < 2 then track_obj:OnDemolish() return end` (same reason).
				map:SuspendPassEdits("TrackElement:Demolish")
				for i = last + 1, n do
					local el = all_elements[i]
					remove_from_track_arrays(el)
					DoneObject(el)
				end
				map:ResumePassEdits("TrackElement:Demolish")
				if IsValid(track_obj) then -- FIX (F44)
					track_obj:UpdateEndElements()
				end
			else
				-- split the track: left side (1..last) stays on track_obj, right side (first..n) goes to new_track
				map:SuspendPassEdits("TrackElement:Demolish")
				-- delete elements in the demolished zone (last+1..first-1, which includes self at idx)
				for i, el in ipairs(all_elements) do
					el.track_obj = false -- we'll use ExpandTrackFromElement to restore this
					if i >= last + 1 and i <= first - 1 then
						DoneObject(el)
					end
				end
				map:ResumePassEdits("TrackElement:Demolish")
				assert(not IsValid(self)) -- we should be deleted here
				table.clear(track_obj.elements)
				table.clear(track_obj.elements_under_construction)

				-- seed the tracks with the last elements on either side
				-- FIX (F44/F45 interplay, playtest 2026-07-26): deleting a repair
				-- site in the zone ALSO destroys its broken twin element
				-- (TrackGridElement:Done, TrackElement.lua:200-201), and the twin —
				-- sharing the site's node_idx — can sit just OUTSIDE the zone at
				-- the seed index. The shipped blind seeds then crash
				-- ExpandTrackFromElement on the dead element (TrackElement.lua:
				-- 718-719, `map` is nil). Seed each side with its first still-valid
				-- survivor instead, and tolerate a side with none.
				local new_track = PlaceObjectIn("TrackBase", map)
				local el1, el2
				for i = last, 1, -1 do
					if IsValid(all_elements[i]) then el1 = all_elements[i] break end
				end
				for i = first, n do
					if IsValid(all_elements[i]) then el2 = all_elements[i] break end
				end
				if el1 then
					el1.track_obj = track_obj
					table.insert(el1.is_construction_site and track_obj.elements_under_construction or track_obj.elements, el1)
					ExpandTrackFromElement(track_obj, el1)
				end
				if el2 then
					el2.track_obj = new_track
					table.insert(el2.is_construction_site and new_track.elements_under_construction or new_track.elements, el2)
					ExpandTrackFromElement(new_track, el2)
				else
					DoneObject(new_track) -- just created, still empty, no trains assigned
					new_track = false
				end

				-- FIX (F44, playtest PT-03 2026-07-25): every survivor must have
				-- been reclaimed by one of the two expansions; anything still
				-- carrying track_obj == false is debris no track can reach —
				-- delete it now instead of leaving immune, half-rendered pieces.
				for _, el in ipairs(all_elements) do
					if IsValid(el) and not el.track_obj then
						DoneObject(el)
					end
				end
				-- FIX (F44, same playtest): guard the tail — an expansion that
				-- came up empty auto-deletes its track (TrackElement.lua:203-205),
				-- and the shipped calls then raised on the dead object
				-- (Track.lua:556 in the playtest log).
				if IsValid(track_obj) then
					track_obj:UpdateEndElements()
					track_obj:UpdatePos()
				end
				if IsValid(new_track) then
					new_track:UpdateEndElements()
					new_track:UpdatePos()
				end
				if not skip_track_process then
					if IsValid(new_track) and #new_track.elements_under_construction == 0 then
						ProcessTrackElements(map, new_track.elements)
					end
					if IsValid(track_obj) and #track_obj.elements_under_construction == 0 then
						ProcessTrackElements(map, track_obj.elements)
					end
					if IsValid(new_track) and #new_track.elements == 0 then
						ProcessTrackElements(map, new_track.elements_under_construction)
					end
					if IsValid(track_obj) and #track_obj.elements == 0 then
						ProcessTrackElements(map, track_obj.elements_under_construction)
					end
				end
			end
			if s1 and s2 then
				RebuildTrainRoutes()
			end
		end
	end,
})

-- Debris repair (playtest PT-03 2026-07-25): a save written after a corrupted
-- split can contain elements with track_obj == false that sit in no track's
-- arrays — invisible to every track system and, before this session's click
-- guard, immune to salvage. Sweep them out once per load; a healthy save has
-- none (every live element belongs to a track).
function OnMsg.LoadGame()
	local fix = SMRFixPack.fixes.TrackSalvageWipe
	if not (fix and fix.status == "active") then return end
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end
	local removed = 0
	AllMapsForEach(true, "TrackGridElement", function(el)
		if IsValid(el) and not el.track_obj and not IsBeingDestructed(el) then
			DoneObject(el)
			removed = removed + 1
		end
	end)
	-- A salvage aborted mid-split (the pre-2026-07-26 seed crash) can also leave
	-- a DESTROYED element sitting inside a track's arrays; purge those entries so
	-- end-element updates and daily walks stop tripping over them.
	local purged = 0
	AllMapsForEach(true, "TrackBase", function(track)
		for _, t in ipairs({ track.elements, track.elements_under_construction }) do
			if type(t) == "table" then
				for i = #t, 1, -1 do
					if not IsValid(t[i]) then
						table.remove(t, i)
						purged = purged + 1
					end
				end
			end
		end
	end)
	if removed > 0 or purged > 0 then
		local msg = string.format("[CommunityFixPack] TrackSalvageWipe: removed %d orphaned track element(s) and %d dead track-list entr(y/ies) left behind by a corrupted salvage", removed, purged)
		if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
	end
end
