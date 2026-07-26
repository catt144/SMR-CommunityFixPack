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
-- it or splits it in two (`TrackElement.lua:503-541`), and the halves are
-- re-seeded and re-expanded — the NEW track object created at :547 runs its
-- GameInit before `ExpandTrackFromElement` (:553-554) gives it any elements at
-- all. So a track can keep the vehicle cap of a length it no longer has, and a
-- freshly split-off track can be left holding the count it was born with.
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
---- (c) a salvage click on a station's connector hex reached the STATION ----
-- Mechanism: `TrackGridElement:SelectionPropagate` returns `self.station`
-- (TrackElement.lua:297-300), `SelectionMouseObj` runs every candidate through
-- it (SelectionModeDialog.lua:44-50), and both shipped demolish-mode guards
-- test only `TrackBase` (:54-56 discards, :84-88 substitutes the element) — a
-- Station is neither, so the salvage toggle landed on the whole station. The
-- two guards prescribe different remedies, so this was screened as a design
-- decision; **the user chose "the click does nothing" (2026-07-25)**. Patch:
-- a pre-guard on `SelectionPropagate` — in demolish mode a station-owned
-- element propagates to nothing. Every other mode keeps the shipped behavior
-- (clicking a connector selects its station), and the station itself is still
-- salvageable by clicking the station's own footprint.
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
	title = "Instant-track paint, train cap follows length, connector-hex salvage click neutralized",
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
		if type(TE.SelectionPropagate) ~= "function"
			or type(rawget(_G, "GetInGameInterfaceMode")) ~= "function" then
			return "SelectionPropagate/GetInGameInterfaceMode not found (game update changed it?)"
		end

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

		---- (c) ---------------------------------------------------------------
		-- In demolish mode a station-owned connector element propagates to
		-- nothing (user decision — see header). All other modes fall through
		-- to the shipped body untouched.
		local orig_prop = TE.SelectionPropagate
		function TE:SelectionPropagate(...)
			if self.station and GetInGameInterfaceMode() == "demolish" then
				return nil
			end
			return orig_prop(self, ...)
		end

		-- ExpandTrackFromElement(track, element) — a global, so replace it in the
		-- real _G by plain assignment (ModEnvMeta.__newindex, Mod.lua:1557-1563).
		local orig_expand = expand
		local wrapped_expand = function(track, element, ...)
			local res = orig_expand(track, element, ...)
			pcall(recompute_max_vehicles, track)
			return res
		end
		ExpandTrackFromElement = wrapped_expand
		if rawget(_G, "ExpandTrackFromElement") ~= wrapped_expand then
			return "could not install the ExpandTrackFromElement wrapper"
		end

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
