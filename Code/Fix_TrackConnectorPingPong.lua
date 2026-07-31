-- F66: two train buildings whose track connector lands on the same hex steal it
-- from each other forever, so neither ever holds a usable connection.
--
-- Defect: `TrackConnectedObjBase:CreateConnectorElements`
-- (Lua\TrainTransport.lua:114-154) claims any hex its Trackconnector spot points
-- at, even when another live building already owns the element standing there:
--     local el = HexGetTrackGridElement(map.object_hex_grid, q, r)
--     if IsValid(el) and (force or el.station ~= self) then
--         assert(not IsValid(el.station) or IsBeingDestructed(el.station))
--         DoneObject(el)
--         el = nil
--     end
-- The assert states the invariant — "the element I am about to destroy has no
-- live owner" — and then the code destroys it regardless. In this engine
-- `assert` does not unwind (it reports and execution continues,
-- LuaExports.lua:567), so a violated invariant is a log line and nothing more.
--
-- That turns into a loop because destroying a connector element makes its owner
-- rebuild it: `TrackGridElement:Done` (Lua\Buildings\TrackElement.lua:193-199)
-- spawns a game-time thread that calls `station:CreateConnectorElements()` for
-- any still-live `self.station`. So with a station and a train tunnel (or two
-- stations) one hex apart, whose connector spots resolve to the same hex:
--   A claims the hex -> destroys B's element -> B's element Done() schedules B
--   -> B claims the hex -> destroys A's element -> A is scheduled -> ...
-- Whichever building is currently without an element fails `GetConnectedTrack` /
-- `GetDestStation` (Track.lua:320-355), so no route ever forms — the "tracks
-- won't connect to stations" report. The known player workaround is to leave a
-- gap of at least two hexes.
--
-- Patch approach: full replacement of CreateConnectorElements — a copy of
-- Lua\TrainTransport.lua:114-154 (shipped Src, game 1.0.7.396349) with one condition
-- widened, marked -- FIX. Replacement rather than a wrapper because the decision
-- is inside the per-spot loop: a pre-wrapper cannot see it and a post-wrapper
-- runs after the element has already been destroyed and replaced.
--
-- The change is exactly the invariant the shipped assert already states: a hex
-- whose element belongs to a DIFFERENT building that is alive and not being
-- destructed is left alone. Everything else behaves as before — in particular
-- the ordinary case of a plain track element sitting on the hex (`el.station` is
-- false, so `IsValid(el.station)` is false) is still cleared, and `force` still
-- rebuilds this building's own element.
--
-- Consequence when the guard engages: the second building simply gets no
-- connector on that hex, which reads to the player exactly like the ≥2-hex-gap
-- workaround — one connection instead of an endless fight over one hex. Making
-- a single hex genuinely serve two owners is a redesign of the connector model,
-- not a defect repair (FIX_POLICY §4).
--
-- The shipped `assert` line is dropped from the copy: it cannot unwind, and its
-- other-owner condition is now enforced by the guard above it. (CORRECTED by the
-- QA audit 2026-07-25: an earlier version claimed keeping it "would print on
-- every legitimate destroy of a dead owner's element" — false; the assert is
-- TRUE, i.e. silent, for a dead or destructing owner. The case where it would
-- print is a `force` rebuild of the building's own live element, e.g. the
-- savegame fixup's CreateConnectorElements(true), Station.lua:1352.)
--
-- Recovery gap + repair (user decision 2026-07-25: repair, not document): when
-- the guard declines, this building owns no element on the contested hex, and
-- after the OTHER building is later demolished nothing reschedules our rebuild —
-- every engine trigger notifies only the dying element's own station
-- (TrackElement.lua:193-199; Track.lua:179-183; TrainTransport.lua:24-26 needs
-- a 2-element both-stationed track; Msg("TrackDemolished") fires only from
-- player track demolition, TrainTransport.lua:156-159). Repair below: post-wrap
-- the declaring class's destructor, TrackConnectedObjBase:Done
-- (TrainTransport.lua:14 — an object destructor, not a command method, so a
-- post-wrapper does run). The wrap records the dying building's connector hexes
-- BEFORE the shipped body tears them down, lets the shipped body run, then
-- schedules a guarded CreateConnectorElements for every OTHER live, non-
-- destructing TrackConnectedObjBase near those hexes — the engine's own deferred
-- pattern, including the in-thread revalidation (TrackElement.lua:194-198).
-- Connector spots reach <= ~2 hexes from a building's centre, so a 3-hex query
-- around each contested hex covers every possible loser; re-running the guarded
-- CreateConnectorElements on an unaffected building is a no-op (its elements
-- exist and el.station == self), so overshooting the radius costs nothing and
-- there is no global rebuild. done_map teardown early-returns exactly like the
-- shipped body.

SMRFixPack.Register("TrackConnectorPingPong", {
	title = "A station and a tunnel one hex apart stop stealing each other's track connector",
	apply = function()
		local err = SMRFixPack.Require("TrackConnectorPingPong", {
			{ class = "TrackConnectedObjBase", method = "CreateConnectorElements" },
			{ class = "TrackConnectedObjBase", method = "Done" },
			{ global = "HexGetTrackGridElement", kind = "any" },
			{ global = "TrackGridElement", kind = "any" },
			{ global = "PlaceObjectIn", kind = "any" },
			{ global = "ResolveMap", kind = "any" },
			{ global = "WorldToHex", kind = "any" },
			{ global = "HexToWorld", kind = "any" },
			{ global = "HexGetDirection", kind = "any" },
			{ global = "IsBeingDestructed", kind = "any" },
			{ global = "CreateGameTimeThread", kind = "any" },
		})
		if err then return err end
		local B = TrackConnectedObjBase

		function B:CreateConnectorElements(force)
			-- check track direction spots for track elements and connect them to us
			local map = ResolveMap(self)
			local x, y, z = self:GetPosXYZ()
			for i = 0, 4 do
				local dirspot = self:GetSpotBeginIndex("Trackdirection" .. i)
				local conspot = self:GetSpotBeginIndex("Trackconnector" .. i)
				if conspot >= 0 and dirspot >= 0 then
					local conpos = self:GetSpotPos(conspot)
					local dirpos = self:GetSpotPos(dirspot)
					local q, r = WorldToHex(conpos)
					local el = HexGetTrackGridElement(map.object_hex_grid, q, r)
					-- FIX (F66): honour the invariant the shipped assert only stated.
					-- An element owned by another building that is alive and not being
					-- destructed is not ours to take; taking it makes that building
					-- rebuild and take it back (TrackElement.lua:193-199), forever.
					local owned_by_live_other = IsValid(el) and el.station ~= self
						and IsValid(el.station) and not IsBeingDestructed(el.station)
					if IsValid(el) and (force or el.station ~= self) and not owned_by_live_other then
						DoneObject(el)
						el = nil
					end
					if not IsValid(el) then
						local el = TrackGridElement:new({
							city = self.city,
							q = q,
							r = r,
							station = self,
							connections = {},
							track_obj = PlaceObjectIn("TrackBase", map),
							node_idx = 1,
						}, map)

						local x, y = HexToWorld(q, r)
						local dirq, dirr = WorldToHex(dirpos)
						local dir = HexGetDirection(q, r, dirq, dirr)
						el:SetPos(x, y, z)
						el:Face(dirpos)
						el:SetGameFlags(const.gofPermanent)
						el:ClearEnumFlags(const.efVisible)
						el:ApplyToGrids()
						el:AutoConnectTracks("start element")
					end
				end
			end
		end

		-- Recovery-gap repair (see header): when a track-connected building dies,
		-- give its neighbours a chance to reclaim the hexes it was holding.
		-- Exposed on SMRFixPack so the TestKit can drive it with synthetic objects.
		function SMRFixPack.TrackConnectorReclaim(map, hexes, dying)
			local seen = {}
			for _, h in ipairs(hexes) do
				local x, y = HexToWorld(h.q, h.r)
				map:MapForEach(point(x, y), "hex", 3, "TrackConnectedObjBase", function(o)
					if o ~= dying and not seen[o] and IsValid(o) and not IsBeingDestructed(o) then
						seen[o] = true
						-- the engine's own deferred-rebuild idiom, in-thread
						-- revalidation included (TrackElement.lua:194-198)
						CreateGameTimeThread(function(station)
							if IsValid(station) and not IsBeingDestructed(station) then
								station:CreateConnectorElements()
							end
						end, o)
					end
				end)
			end
		end

		local orig_done = B.Done
		function B:Done(done_map)
			if done_map then
				-- map teardown: no reclaim work, exactly like the shipped early-return
				return orig_done(self, done_map)
			end
			-- collect this building's connector hexes BEFORE the shipped body
			-- destroys the elements standing on them (same spot reads it does)
			local map = ResolveMap(self)
			local hexes = {}
			if map then
				for i = 0, 4 do
					local conspot = self:GetSpotBeginIndex("Trackconnector" .. i)
					if conspot >= 0 then
						local q, r = self:GetSpotPosHex(conspot)
						hexes[#hexes + 1] = { q = q, r = r }
					end
				end
			end
			orig_done(self, done_map)
			if map and #hexes > 0 then
				SMRFixPack.TrackConnectorReclaim(map, hexes, self)
			end
		end
	end,
})
