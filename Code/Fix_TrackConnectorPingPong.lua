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
-- Lua\TrainTransport.lua:114-154 (shipped Src, 2026-07) with one condition
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
-- The shipped `assert` line is dropped from the copy: it cannot unwind, its
-- condition is now enforced by the guard above it, and leaving it in would print
-- on every legitimate destroy of a dead owner's element.

SMRFixPack.Register("TrackConnectorPingPong", {
	title = "A station and a tunnel one hex apart stop stealing each other's track connector",
	apply = function()
		local B = rawget(_G, "TrackConnectedObjBase")
		if type(B) ~= "table" or type(B.CreateConnectorElements) ~= "function" then
			return "TrackConnectedObjBase.CreateConnectorElements not found (game update changed it?)"
		end
		for _, name in ipairs({ "HexGetTrackGridElement", "TrackGridElement", "PlaceObjectIn",
			"ResolveMap", "WorldToHex", "HexToWorld", "HexGetDirection", "IsBeingDestructed" }) do
			if rawget(_G, name) == nil then
				return name .. " not found (game update changed it?)"
			end
		end

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
	end,
})
