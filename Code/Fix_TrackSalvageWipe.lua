-- F44/F91/F116/F124: partial salvage keeps survivors; whole salvage leaves no shell.
--
-- Full replacement of archived game 1.1.1.405907:
-- Lua/Buildings/TrackElement.lua:467-637. Only marked F44/F91 deltas differ.
-- Native repair exclusion, correct-array removal, repair rehome/repair_cgs and
-- ProcessAllElements are retained. F116 indexing, skip forwarding and orphan
-- rehome/processing now come from this native body.
--
-- A wrapper cannot alter the mid-body anchor search or stop OnDemolish destroying
-- trains after the short-remainder decision. Mutating pillars/arrays beforehand
-- would also alter geometry and repair bookkeeping.
--
-- The split and ProcessAllElements enter engine map/grid/geometry operations,
-- so a full behavior probe is unsafe on fake objects. Colonist.MigrateStep is
-- a named branch shape absent from archived 1.1.0.403908, present in 1.1.1.405907.
-- It does not validate repair semantics or future same-shape body changes.
-- Missing/unknown shape declines; source review remains required after updates.
--
-- Save safety: synchronous replacement and LoadGame sweep, with no yields or new
-- persisted fields/functions/threads. Element Done creates vanilla connector
-- threads without capturing this caller. Removal leaves ordinary repaired state,
-- no mod continuation. The owner-ruled legacy orphan sweep remains below.
--
-- MANIFEST (FIX_POLICY section 2b).
-- SRC: Lua/Buildings/TrackElement.lua TrackGridElement:DemolishAndSplitTrack sha256=2f08d0c520e67f7bb6b615f2047ca044ee06ab87fa28edd16890b14089494983
-- DEFECT: until not all_elements\[first\] or \(all_elements\[first\]\.pillared and IsTrackElementStraight

SMRFixPack.Register("TrackSalvageWipe", {
	title = "Salvaging one track piece no longer deletes the whole track and its trains",
	apply = function()
		local err = SMRFixPack.Require("TrackSalvageWipe", {
			{ class = "TrackGridElement", method = "DemolishAndSplitTrack" },
			{ class = "TrackBase", method = "ProcessAllElements" },
			{ global = "IsTrackElementStraight" },
			{ global = "ResolveMap" },
			{ global = "ExpandTrackFromElement" },
			{ global = "RebuildTrainRoutes" },
			{ global = "PlaceObjectIn" },
			{ test = function()
				local C = rawget(_G, "Colonist")
				return type(C) == "table" and type(C.MigrateStep) == "function"
			end, reason = "1.1.1 track-repair branch shape not found" },
		})
		if err then return err end
		local E = TrackGridElement

		function E:DemolishAndSplitTrack(mass_delete, skip_track_process)
			local track_obj = self.track_obj
			-- FIX (F44): salvage stranded legacy debris.
			if not track_obj then DoneObject(self) return end
			-- Repair construction sites (with a broken real element) delegate to demolishing the real element
			if self.is_construction_site and IsValid(self.broken) and table.find(track_obj.elements, self.broken) then
				return self.broken:Demolish(mass_delete, skip_track_process)
			end
			if not skip_track_process then
				-- make sure elements' node_idx is actually valid, since we're assuming it represents the distance from the start for the given element
				track_obj:ProcessAllElements()
			end

			-- Build a combined list of all elements sorted by node_idx to reflect their physical order along
			-- the track. Both .elements (completed) and .elements_under_construction may be mixed along it.
			local all_elements = {}
			for _, el in ipairs(track_obj.elements) do
				all_elements[#all_elements + 1] = el
			end
			for _, el in ipairs(track_obj.elements_under_construction) do
				if not IsValid(el.broken) then
					all_elements[#all_elements + 1] = el
				end
			end
			-- FIX (F44/F45): decline if disconnected physical elements resist reindexing.
			for _, el in ipairs(all_elements) do
				if type(el.node_idx) ~= "number" then return end
			end
			table.sort(all_elements, function(a, b) return a.node_idx < b.node_idx end)

			local idx = table.find(all_elements, self)
			if mass_delete or not idx then
				track_obj:OnDemolish()
				-- FIX (F91): finish the deletion OnDemolish only prepares.
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
			-- FIX (F44): curves without anchors stop at the clicked neighbours.
			if not all_elements[first] then first = Min(first, idx + 1) end
			if not all_elements[last] then last = Max(last, idx - 1) end

			local map = ResolveMap(self)
			local s1, s2 = track_obj:GetStartStation(), track_obj:GetEndStation()
			Msg("StationsDisconnected", s1, s2, track_obj)

			-- Remove an element from its source array on track_obj: construction sites live in
			-- elements_under_construction, completed elements in elements.
			local function remove_from_track_arrays(el)
				if el.is_construction_site then
					table.remove_value(track_obj.elements_under_construction, el)
				else
					table.remove_value(track_obj.elements, el)
				end
			end

			if last <= 1 then
				-- shorten the track from the start: keep all_elements[first..n]
				-- FIX (F44): a short remainder does not justify whole-track demolition.
				map:SuspendPassEdits("TrackElement:Demolish")
				for i = 1, first - 1 do
					local el = all_elements[i]
					remove_from_track_arrays(el)
					DoneObject(el)
				end
				map:ResumePassEdits("TrackElement:Demolish")
				if IsValid(track_obj) then -- FIX (F44): an empty trim can auto-delete its track.
					track_obj:UpdateEndElements()
				end
			elseif first >= n then
				-- shorten the track from the end: keep all_elements[1..last]
				-- FIX (F44): a short remainder does not justify whole-track demolition.
				map:SuspendPassEdits("TrackElement:Demolish")
				for i = last + 1, n do
					local el = all_elements[i]
					remove_from_track_arrays(el)
					DoneObject(el)
				end
				map:ResumePassEdits("TrackElement:Demolish")
				if IsValid(track_obj) then -- FIX (F44): an empty trim can auto-delete its track.
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
				-- FIX (F44): retain valid-survivor seeding when a twin deletion invalidates a seed.
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

				local tracks = { track_obj }
				if new_track then tracks[#tracks + 1] = new_track end

				-- safeguard: if ExpandTrackFromElement didn't reach an element for some reason, create a new track for it and expand from it until all elements are assigned
				while true do
					local orphan
					for _, el in ipairs(all_elements) do
						if IsValid(el) and not el.track_obj then
							orphan = el
							break
						end
					end
					if not orphan then break end
					local extra = PlaceObjectIn("TrackBase", map)
					orphan.track_obj = extra
					table.insert(orphan.is_construction_site and extra.elements_under_construction or extra.elements, orphan)
					ExpandTrackFromElement(extra, orphan)
					tracks[#tracks + 1] = extra
				end

				-- repair sites are not in all_elements, so follow each surviving broken element to its new track
				for _, track in ipairs(tracks) do
					table.clear(track.repair_cgs)
				end
				for _, el in ipairs(all_elements) do
					local cs = IsValid(el) and IsValid(el.broken) and el.broken
					if cs then
						if cs.track_obj ~= el.track_obj and IsValid(cs.track_obj) then
							table.remove_value(cs.track_obj.elements_under_construction, cs)
						end
						cs.track_obj = el.track_obj
						table.insert_unique(el.track_obj.elements_under_construction, cs)
						if cs.construction_group then
							table.insert_unique(el.track_obj.repair_cgs, cs.construction_group)
						end
					end
				end

				for i, track in ripairs(tracks) do
					if IsValid(track) and (#track.elements == 0) and (#track.elements_under_construction == 0) then
						DoneObject(track)
					end
					if not IsValid(track) or IsBeingDestructed(track) then
						table.remove(tracks, i)
					end
				end
				for _, track in ipairs(tracks) do
					track:UpdateEndElements()
					track:UpdatePos()
				end
				if not skip_track_process then
					for _, track in ipairs(tracks) do
						track:ProcessAllElements()
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
