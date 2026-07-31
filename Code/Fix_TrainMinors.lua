-- F49: the train minors bundle. Five items were tracked; each was screened
-- against the shipped source and two are fixed here. What the other three turned
-- out to be is recorded on the BUGS.md entry and summarised at the bottom of
-- this header — none of them is a no-op fix waiting to be written.
--
---- (a) instantly-built track is painted with the PIPES palette --------------
-- `Tracks.lua:385` captures `local cm1, cm2, cm3, cm4 = GetPipesPalette()` and
-- `:412` applies it to every element the instant placement path creates
-- (`place_track`, used when the track does not require construction — map
-- setup, cheats, the instant-build rule). Every other track path uses
-- `GetTracksPalette()`: the completed-construction path (`TrackElement.lua:791`),
-- the construction cursor (`GridConstruction.lua:220`), and — decisively — the
-- colony colour-scheme refresh, which repaints *every* `TrackGridElement` on
-- every map with it (`ColonyColorScheme.lua:120-121`). The two palettes differ:
-- pipes is `(pipes_metal, pipes_base, pipes_metal, pipes_base)`, tracks is
-- `train_track_base` four times (`ColonyColorScheme.lua:69-77`). So instant
-- track comes out pipe-coloured until the player happens to change colour
-- scheme, at which point it silently corrects itself — which is what makes the
-- scheme refresh the authority on what the colour should have been.
--
-- Patch approach: a post-wrapper on `TrackGridElement:GameInit`
-- (TrackElement.lua:218-224) applying exactly what the scheme refresh applies.
-- The palette assignment at Tracks.lua:412 happens during construction of the
-- object, before GameInit, so the wrapper lands after it. Construction sites
-- (`TrackConstructionSite`, which inherits TrackGridElement) are skipped — the
-- shipped GameInit branches on the same flag, and their visuals belong to the
-- construction cursor. Elements built the normal way are repainted with the
-- colour they already had, so this is a no-op for them.
--
---- (d) `max_vehicles` is computed once and never again ---------------------
-- `TrackBase:GameInit` (Track.lua:62-67) sets
--     local elements = #self.elements + (#self.repair_cgs > 0 and 0 or #self.elements_under_construction)
--     self.max_vehicles = (elements == 0) and 0 or (elements < 30) and 1 or 2 * Max(1, DivRound(elements,50))
-- and that is the ONLY assignment to `max_vehicles` in the whole codebase
-- (elsewhere it is only read, via `StationsLink:GetMaxVehicles` ->
-- `CanAddVehicle`, StationsLink.lua:28-32; the class default is 2, :8). A
-- track's element count changes throughout its life: salvaging a piece shortens
-- it or splits it in two (`TrackElement.lua:503-541`). (Corrected by the QA
-- audit 2026-07-25: GameInit is deferred to a game-time thread,
-- _object.lua:187-192, so the split-off track's cap IS computed correctly once
-- its elements are in; the residual defect is the SURVIVING track, which never
-- re-runs GameInit and keeps the cap of a length it no longer has.) Known
-- accepted gap: the AutoConnectTracks merge path (TrackElement.lua:381-409) and
-- instant-build track_obj reuse recompute nothing in-session; the PostLoadGame
-- sweep corrects them on the next load, and no path ever sets a WRONG value.
--
-- Patch approach: recompute with the shipped formula whenever the element set
-- changes, at the two points that mark exactly that:
--   * `TrackBase:UpdateEndElements` (Track.lua:554-562) — called at the end of
--     all three partial-salvage branches (TrackElement.lua:516, :530, :556-557),
--     always after the arrays have been repopulated;
--   * `ExpandTrackFromElement` (TrackElement.lua:714) — the merge/expand path,
--     called when a split re-seeds a track and when a construction site
--     completes (:795).
-- Plus a `PostLoadGame` sweep so tracks already saved with a stale cap are
-- corrected once. It is PostLoadGame rather than LoadGame for the usual reason
-- (Savegame.lua:810-813 — `FixupSavegame` runs after `Msg("LoadGame")`, and
-- `SavegameFixups.RemoveTrackDoubleTurns`, TrackElement.lua:839-843, re-processes
-- track elements).
--
---- (c) REMOVED 2026-07-30 — it was "fixing" designed behavior --------------
-- The guard that used to live here made a station-owned connector element
-- propagate to nothing in demolish mode. It is gone, closed `wontfix` by user
-- decision on live evidence (full record on the F49 BUGS.md entry).
--
-- What the tester established at the keyboard, which no amount of source
-- reading would have shown: the salvage cursor transitions from
-- `Salvage Train Station` to `Salvage Track` seamlessly, to the millimetre,
-- with no third state in between — and a player has NO exposed control that
-- distinguishes a station's connector from the station itself. The
-- propagation to `self.station` is therefore not a defect at all; it is what
-- makes that boundary continuous, and it is why the station's own track
-- cannot be salvaged out from under it.
--
-- Station connector elements are real and station-owned (`station = self`,
-- TrainTransport.lua:132-139, at the station's `Trackconnector` spots), so
-- the guard was not inert by accident — had it engaged it would have carved a
-- DEAD BAND into that boundary where nothing is targetable. A repair that can
-- only make the UI worse is not a repair.
--
---- screened, NOT fixed here (full write-ups on the BUGS.md entry) ----------
-- (b) `DemolishAndSplitTrack` never touches `assigned_vehicles`: mechanism
--     confirmed, consequence not establishable from source alone — playtest
--     item PT-46.
-- (e) `GridConstructionController:CanContinueTrack` (GridConstruction.lua:478-491)
--     is dead code and `ConstructionStatus.TrackRequiresTwoStations` is only
--     read by it. Wiring it up would mean inventing both the call site and the
--     condition that inserts the status — a redesign, not a fix.

SMRFixPack.Register("TrainMinors", {
	title = "Instant-track paint, train cap follows length",
	apply = function()
		local TE = rawget(_G, "TrackGridElement")
		if type(TE) ~= "table" or type(TE.GameInit) ~= "function" then
			return "TrackGridElement.GameInit not found (game update changed it?)"
		end
		local TB = rawget(_G, "TrackBase")
		if type(TB) ~= "table" or type(TB.GameInit) ~= "function"
			or type(TB.UpdateEndElements) ~= "function" then
			return "TrackBase.GameInit/UpdateEndElements not found (game update changed it?)"
		end
		if type(rawget(_G, "GetTracksPalette")) ~= "function"
			or type(rawget(_G, "SetObjectPaletteRecursive")) ~= "function" then
			return "GetTracksPalette/SetObjectPaletteRecursive not found (game update changed it?)"
		end
		local expand = rawget(_G, "ExpandTrackFromElement")
		if type(expand) ~= "function" then
			return "ExpandTrackFromElement not found (game update changed it?)"
		end
		-- (the SelectionPropagate / GetInGameInterfaceMode self-check went with
		-- the (c) guard, 2026-07-30 — nothing here touches either any more)

		---- (a) ---------------------------------------------------------------
		local orig_el_gameinit = TE.GameInit
		function TE:GameInit(...)
			local res = orig_el_gameinit(self, ...)
			if not self.is_construction_site then
				-- exactly what ColonyColorScheme.lua:120-121 applies to every
				-- TrackGridElement when the player changes colour scheme
				local cm1, cm2, cm3, cm4 = GetTracksPalette()
				SetObjectPaletteRecursive(self, cm1, cm2, cm3, cm4)
			end
			return res
		end

		---- (d) ---------------------------------------------------------------
		-- The shipped formula, Track.lua:64-65, verbatim. Returns the value it
		-- set, or nil when the track is in no state to be measured.
		local function recompute_max_vehicles(track)
			if type(track) ~= "table" then return end
			local els, under = track.elements, track.elements_under_construction
			if type(els) ~= "table" or type(under) ~= "table" then return end
			local repair_cgs = track.repair_cgs
			local elements = #els + ((type(repair_cgs) == "table" and #repair_cgs > 0) and 0 or #under)
			local value = (elements == 0) and 0 or (elements < 30) and 1 or 2 * Max(1, DivRound(elements, 50))
			track.max_vehicles = value
			return value
		end

		SMRFixPack.TrainMinors = { RecomputeMaxVehicles = recompute_max_vehicles }

		local orig_update_end = TB.UpdateEndElements
		function TB:UpdateEndElements(...)
			local res = orig_update_end(self, ...)
			pcall(recompute_max_vehicles, self)
			return res
		end

		-- (c) removed 2026-07-30 — see the header block.

		-- ExpandTrackFromElement(track, element) — a global, so replace it in the
		-- real _G by plain assignment (ModEnvMeta.__newindex, Mod.lua:1557-1563).
		local orig_expand = expand
		local wrapped_expand = function(track, element, ...)
			local res = orig_expand(track, element, ...)
			pcall(recompute_max_vehicles, track)
			return res
		end
		local err = SMRFixPack.SetGlobal("ExpandTrackFromElement", wrapped_expand,
			"could not install the ExpandTrackFromElement wrapper")
		if err then return err end

		-- Existing saves: one pass over every track, idempotent.
		OnMsg.PostLoadGame = function()
			local cities = rawget(_G, "Cities")
			if type(cities) ~= "table" then return end
			local corrected = 0
			for _, city in ipairs(cities) do
				local tracks = city and city.labels and city.labels.TrackBase
				for _, track in ipairs(tracks or empty_table) do
					local before = track and track.max_vehicles
					local ok, after = pcall(recompute_max_vehicles, track)
					if ok and after and after ~= before then corrected = corrected + 1 end
				end
			end
			SMRFixPack.TrainMinors.corrected = corrected
		end
	end,
})
