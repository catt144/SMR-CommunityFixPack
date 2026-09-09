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
--
-- AMENDED 2026-08-02 for F91 (whole-track salvage leaves an undeletable invisible
-- TrackBase shell). Two halves, both inside this file — no new module, no new
-- registry id, no new thread, so this adds ZERO save-safety exposure:
--   A. the mass_delete / not-idx branch now FINISHES the deletion vanilla's
--      OnDemolish only prepares (see the -- FIX (F91) block there);
--   B. the OnMsg.LoadGame sweep below gained a shell heal for saves that already
--      carry them — vanilla produces one per Ctrl+click salvage, unbounded and
--      permanent, so an existing save can hold any number.
-- AMENDED 2026-09-08 for F116 (game 1.1.0.403908). This body is a 1.0.7 copy and
-- 1.1.0 changed the shipped one; two of those changes are repaired here, marked
-- -- FIX (F116). Both are IN-BODY additions, not a re-copy: the ~13 interleaved
-- F44/F45/F91 sites (several of which REMOVE shipped early-returns) make a
-- re-copy a rewrite, and the actual gap turned out to be one call and one
-- argument.
--   1. the PRE-SORT node_idx revalidation 1.1.0 added (TrackElement.lua:473-476);
--   2. skip_track_process forwarded to self.broken:Demolish (:471).
-- ⛔ TWO KNOWN, DELIBERATE DIVERGENCES REMAIN — documented, not accidental, and
-- both are owner-facing questions in bugs/F116.md, NOT things a later reader
-- should quietly "fix":
--   A. ORPHAN POLICY. 1.1.0 (:580-595) REHOMES any element left with
--      track_obj == false into a fresh track; we DELETE it (the F44 block near
--      the tail). Ours is playtest-derived (PT-03) and was correct on 1.0.7,
--      where nothing rehomed the orphan and it really was immune debris. On
--      1.1.0 it means we can destroy a fragment vanilla would have saved. Left
--      as-is because (1) above removes the mechanism that MANUFACTURES orphans,
--      and changing destructive logic with no reproduction is worse than the
--      long tail it leaves.
--   B. POST-SPLIT PROCESSING. 1.1.0 processes each resulting track's COMBINED
--      element list (:609-613); our 1.0.7 tail processes one array only, and
--      only when the other is empty (:277-290 equivalent), so a track with both
--      completed AND under-construction elements gets no post-split processing.
-- ⛔ NEITHER the repair nor this note is TESTED. F116 is source-derived and has
-- never been reproduced in a log.
--
-- ⚠️ WHAT DOES NOT CHANGE, stated because this module is `tested` and an A/B
-- reader must not misread it: mass salvage still removes exactly the same track
-- and still destroys the same assigned trains. The only difference is that the
-- now-empty TrackBase object is deleted instead of being left as a shell — and
-- the shell was invisible (entity = "InvisibleObject", Track.lua:35) and carried
-- count_as_building = false (:52), so nothing player-visible moves EXCEPT the
-- colony's daily "trains on tracks" walk, which stops enumerating dead tracks
-- (ResourceTracking.lua:197-201).

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Buildings/TrackElement.lua TrackGridElement:DemolishAndSplitTrack sha256=7466b9403e6a3b27d12702a8825a61bfcdd2674c9bb6b0289c255cbc0b987c0e
--   (Lua/Buildings/TrackElement.lua:467-618 at pin time)
-- DEFECT: until not all_elements\[first\] or \(all_elements\[first\]\.pillared and IsTrackElementStraight
--   the outward search needs pillared AND straight; a curve is pillared and
--   never straight, so it walks off the array

SMRFixPack.Register("TrackSalvageWipe", {
	title = "Salvaging one track piece no longer deletes the whole track and its trains",
	apply = function()
		local err = SMRFixPack.Require("TrackSalvageWipe", {
			{ class = "TrackGridElement", method = "DemolishAndSplitTrack" },
			{ global = "IsTrackElementStraight" },
			{ global = "ResolveMap" },
			{ global = "ExpandTrackFromElement" },
			{ global = "ProcessTrackElements" },
			{ global = "RebuildTrainRoutes" },
			{ global = "PlaceObjectIn" },
		})
		if err then return err end
		local E = TrackGridElement

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
			-- FIX (F116): forward skip_track_process. Ours dropped it, so the
			-- delegated call re-entered with it nil and ran the element
			-- processing its one caller (Construction.lua:1692, station build)
			-- explicitly asked to skip — that caller does the processing itself
			-- afterwards (:1696-1704).
			if self.is_construction_site and IsValid(self.broken) and table.find(track_obj.elements, self.broken) then
				return self.broken:Demolish(mass_delete, skip_track_process)
			end

			-- FIX (F116, 2026-09-08): revalidate node_idx BEFORE the sort, which is
			-- what 1.1.0 does at TrackElement.lua:473-476 with the comment "make sure
			-- elements' node_idx is actually valid, since we're assuming it represents
			-- the distance from the start for the given element."
			-- This body is a 1.0.7 copy and had no counterpart: the four
			-- ProcessTrackElements calls at the tail are the POST-split step (1.1.0's
			-- own :609-613), they run after the sort and only in the split branch, so
			-- they never validated the sort's input.
			-- Why it matters: node_idx is NOT maintained as distance-from-start.
			-- It is stamped as a monotonic per-track counter at build time
			-- (Tracks.lua:370-371, :393-401) and, on a track merge, from TWO separate
			-- array positions (TrackElement.lua:415-425) — completed elements from
			-- #elements, under-construction ones from #elements_under_construction —
			-- which COLLIDE, and the merge only repairs them when nothing is under
			-- construction (:430-432). all_elements is exactly those two arrays
			-- concatenated, so after such a merge the sort below is ordered by a
			-- stale, colliding key while the zone math (first/last walk, and the
			-- last+1..first-1 deletion range) assumes array order == physical order.
			-- The result is a physically scattered deletion — the corrupted-track
			-- outcome PT-03 reported on 1.0.7, which vanilla 1.1.0 no longer has.
			-- Guarded, not assumed: if the method is absent (older tree) we fall
			-- through to the F44/F45 guard below exactly as before, rather than
			-- declining and costing players F44 and F91.
			if not skip_track_process and IsValid(track_obj)
					and type(track_obj.ProcessAllElements) == "function" then
				track_obj:ProcessAllElements()
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
			-- ⚠️ F116 NOTE (2026-09-08): the F116 revalidation above now handles the
			-- COMMON case (stale/colliding indices on a contiguous track), so this
			-- guard rarely fires on 1.1.0. It is NOT retirable: ProcessTrackElements
			-- bails without restamping when OrderTrackElements cannot walk the track
			-- (Tracks.lua:615-620, :818-819) — i.e. exactly when the track is
			-- physically disconnected — so this stays as the backstop for that case.
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
				-- FIX (F91): OnDemolish PREPARES a deletion that nothing performs.
				-- It sets CanDelete = ret_false (Track.lua:249) and empties
				-- elements / elements_under_construction / assigned_vehicles to
				-- `false` — and the element-side auto-delete it just disarmed
				-- (TrackElement.lua:203-205) is the only other route to DoneObject.
				-- What survives is an entity = "InvisibleObject" TrackBase sitting
				-- in the map, in city.labels.TrackBase and in every later save,
				-- with no route to deletion left in the game. Every OTHER path out
				-- of TrackBase:OnDemolish ends in DoneObject: TrackBase sets
				-- use_demolished_state = false (Track.lua:45) and
				-- Demolishable:Demolish deletes on exactly that branch
				-- (Demolishable.lua:132-141). We finish the deletion vanilla
				-- started — what mass salvage REMOVES is unchanged.
				-- The three arrays are restored first so Done can walk them
				-- (Track.lua:69-76); Done re-falsifies them itself. Belt and
				-- braces: whether `#false` raises here is unverified and nothing
				-- depends on the answer (the F10 lesson).
				-- Deliberately NOT Msg("Demolished", track_obj): vanilla's direct
				-- OnDemolish path never sends it, and firing it would reach
				-- listeners outside this defect's scope.
				if IsValid(track_obj) and not IsBeingDestructed(track_obj) then
					track_obj.elements = track_obj.elements or {}
					track_obj.elements_under_construction = track_obj.elements_under_construction or {}
					track_obj.assigned_vehicles = track_obj.assigned_vehicles or {}
					DoneObject(track_obj)
				end
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
OnMsg.LoadGame = SMRFixPack.WhenActive("TrackSalvageWipe", function()
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
	--
	-- FIX (F91), same walk: heal saves that already carry OnDemolish shells — the
	-- undeletable invisible TrackBase the half-done deletion above leaves behind.
	-- Vanilla produces them on every Ctrl+click whole-track salvage, so a save
	-- from before this fix (or from an unmodded game) can hold any number of them.
	-- The signature is EXACT, so a live track cannot match: all three arrays
	-- `== false` — only TrackBase:OnDemolish produces that (DestroyAssignedTrains
	-- Track.lua:165, DestroyTrackElements :190-191), while construction gives all
	-- three real tables (TrackBase:Init, Track.lua:56-60, and assigned_vehicles
	-- from the combined StationsLink:Init, StationsLink.lua:13) — AND
	-- `demolishing` truthy (set at Track.lua:250).
	-- Timing is safe: on the healthy Demolishable path there is no yield between
	-- OnDemolish (Demolishable.lua:133) and DoneObject (:139), so a save can never
	-- capture a legitimately mid-deletion track and the signature cannot
	-- false-positive on one.
	-- The purge loop below is unaffected either way — it tests type(t) == "table"
	-- and a shell's fields are `false`.
	local purged, shells = 0, 0
	AllMapsForEach(true, "TrackBase", function(track)
		if IsValid(track) and not IsBeingDestructed(track)
				and track.elements == false
				and track.elements_under_construction == false
				and track.assigned_vehicles == false
				and track.demolishing then
			track.elements = {}
			track.elements_under_construction = {}
			track.assigned_vehicles = {}
			DoneObject(track)
			shells = shells + 1
			return
		end
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
		SMRFixPack.Log("TrackSalvageWipe: removed %d orphaned track element(s) and %d dead track-list entr(y/ies) left behind by a corrupted salvage", removed, purged)
	end
	if shells > 0 then
		SMRFixPack.Log("TrackSalvageWipe: deleted %d invisible track shell(s) left behind by a whole-track salvage (F91)", shells)
	end
end)
