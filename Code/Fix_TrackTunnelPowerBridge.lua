-- F65: a station attached directly to a train tunnel (or to another station)
-- never bridges the power grid, although the Train Tunnel's own description
-- promises it does.
--
-- Defect: `OnMsg.StationsConnected` (Lua\Buildings\Track.lua:668-680) skips the
-- grid work for short tracks:
--     if #track.elements > 2 then
--         -- 2-element tracks don't need to tunnel connections,
--         -- as the connected buildings are already adjacent and can connect without the track
--         track:ConnectToGrids()
--     else
--         track.stations_connected = true
--     end
-- A 2-element track is exactly the two buildings' own connector elements
-- (`TrackBase:GetSupplyTunnelElement`, Track.lua:567-574, returns elements[1]
-- and elements[#elements] — the two ends), and a connector element sits on a hex
-- OUTSIDE its building: `OrientConnectorElements` records the connection back
-- towards the building at `conq - dq, conr - dr` (TrainTransport.lua:91-100). So
-- when the shortcut fires, the two buildings are two hexes apart with the
-- connector hexes between them — not adjacent, and track elements carry no
-- power of their own (`TrackBase.ApplyToGrids = empty_func`, Track.lua:663;
-- "Since we're not an ElectricityGridObject", :98). The comment's premise can
-- therefore be false, and when it is, `AddSupplyTunnel` + `MergeGrids`
-- (Track.lua:97-124) never run and the two grids stay apart.
--
-- The Train Tunnel is where players notice it, because its description sells the
-- feature outright — "The tunnel entrance and exit can connect tracks AND POWER
-- GRIDS at different locations and different elevations"
-- (Data\BuildingTemplate\TrackTunnel.lua:17) — and the tunnel's own
-- entrance-to-exit merge (`TrackTunnelBase:OnTrackPowerReconnected`,
-- TrackTunnel.lua:12-17) is useless if the station never reaches the entrance.
--
-- Patch approach: an additional `OnMsg.StationsConnected` handler (FIX_POLICY
-- §1.2 — OnMsg is additive, the shipped handler keeps running untouched). Ours
-- runs after it and repairs only the case the shortcut got wrong.
--
-- *Implemented on runtime evidence rather than on the tracked sketch.* The
-- sketch said "if a 2-element track touches a TrackTunnelBase, call
-- ConnectToGrids()". Whether the two buildings really end up adjacent depends on
-- entity spot geometry, which is binary data and cannot be read from Lua — so
-- instead of assuming the premise is wrong, this asks the game: it bridges only
-- when the two stations demonstrably sit on DIFFERENT live electricity grids
-- after the shipped handler has run. If the shortcut's premise holds, both
-- stations are already on one grid and this fix does nothing at all.
--
-- *Scope note:* that check makes the tunnel restriction unnecessary, so it is
-- not applied — the same shortcut fails the same way for two stations a short
-- track apart, and the runtime test cannot be fooled by which classes are
-- involved. The Train Tunnel is only the case with a written promise attached.
--
-- After a successful bridge the handler clears `stations_connected`, so the
-- track's bookkeeping ends up identical to a >2-element track's (supply tunnel
-- set, stations_connected false) and the shipped teardown paths — Track.lua:506,
-- :511, :682-684 and Station.lua:1224-1234 — see the state they expect.
--
-- *Teardown (QA audit 2026-07-25):* one deletion path does NOT run the grid
-- teardown — the special case for a 2-element both-stationed track in
-- `TrackConnectedObjBase:Done` (TrainTransport.lua:24-27) DoneObjects the track
-- directly, and `TrackBase:Done` (Track.lua:69-76) never calls
-- `DisconnectFromGrids` (only `OnDemolish`, Track.lua:273-276, does). Shipped
-- code never creates a BRIDGED 2-element track, so that path never needed it;
-- this fix is what creates them, and without a repair, demolishing either
-- endpoint building leaked the tunnel mask + adjacency (persisted, survives
-- uninstall) and skipped the grid-split walk. So this fix also pre-wraps
-- `TrackBase:Done`: any deletion of a `supply_tunnel_set` track runs the
-- shipped `DisconnectFromGrids` first. That inverse is built for exactly this
-- moment — it tolerates a dead endpoint ("we don't require two working
-- stations", Track.lua:139-149) and `RemoveSupplyTunnel` clears the flag, so
-- the demolish path (which already disconnected) makes the wrap a no-op.
--
-- Known scope limit (recorded, accepted): the different-grids test runs once,
-- at StationsConnected time. If the two stations happened to share a grid via
-- cables right then, the fix declines, and nothing re-checks when those cables
-- are later removed — until the next load's sweep. The every-load sweep is the
-- deliberate mitigation.
--
-- Existing saves: a `PostLoadGame` pass re-checks every track once, because
-- StationsConnected does not fire again on load. It is PostLoadGame and not
-- LoadGame deliberately — `Msg("LoadGame")` fires BEFORE `FixupSavegame`
-- (Savegame.lua:810-813) and the shipped `SavegameFixups.ConvertTrackPowerLinks`
-- (Station.lua:1395-1420) tears down and rebuilds exactly these links; a
-- LoadGame-time pass would race it. Same lesson as F35.

SMRFixPack.Register("TrackTunnelPowerBridge", {
	title = "A station attached to a train tunnel bridges the power grid again",
	apply = function()
		local GRID_METHODS = "TrackBase.ConnectToGrids/GetStartStation/GetEndStation not found (game update changed it?)"
		local DONE_METHODS = "TrackBase.Done/DisconnectFromGrids not found (game update changed it?)"
		local err = SMRFixPack.Require("TrackTunnelPowerBridge", {
			{ class = "TrackBase", method = "ConnectToGrids", reason = GRID_METHODS },
			{ class = "TrackBase", method = "GetStartStation", reason = GRID_METHODS },
			{ class = "TrackBase", method = "GetEndStation", reason = GRID_METHODS },
			{ class = "TrackBase", method = "Done", reason = DONE_METHODS },
			{ class = "TrackBase", method = "DisconnectFromGrids", reason = DONE_METHODS },
			{ global = "IsBeingDestructed" },
		})
		if err then return err end
		local T = TrackBase

		-- Returns "bridged" when it created the missing supply tunnel, or nil plus
		-- a short reason. Never raises: every read is guarded, because this runs
		-- from a message handler and from a savegame pass.
		local function bridge_if_needed(track)
			if type(track) ~= "table" then return nil, "not a track" end
			if track.supply_tunnel_set then return nil, "already bridged" end
			local elements = track.elements
			if type(elements) ~= "table" then return nil, "no elements" end
			-- Only the case the shipped handler declined; longer tracks it bridges
			-- itself and we must not touch them.
			if #elements == 0 or #elements > 2 then return nil, "not a short track" end

			local s1, s2 = track:GetStartStation(), track:GetEndStation()
			for _, s in ipairs({ s1 or false, s2 or false }) do
				if not IsValid(s) or IsBeingDestructed(s) or s.destroyed then
					return nil, "station missing or being destroyed"
				end
			end
			-- ConnectToGrids indexes s.electricity.grid unguarded; a station
			-- without a grid element would raise there, so stop short of it.
			local e1, e2 = s1.electricity, s2.electricity
			if not e1 or not e2 then return nil, "a station has no electricity element" end
			-- THE test: only bridge when the shortcut's own premise ("already
			-- adjacent, they connect without the track") is demonstrably false.
			if not (e1.grid and e2.grid and e1.grid ~= e2.grid) then
				return nil, "stations already share a grid"
			end

			track:ConnectToGrids()
			if track.supply_tunnel_set then
				-- match the state a >2-element track ends up in
				track.stations_connected = false
				return "bridged"
			end
			return nil, "ConnectToGrids declined"
		end

		SMRFixPack.TrackPowerBridge = { BridgeIfNeeded = bridge_if_needed }

		-- FIX (QA 2026-07-25): tear the tunnel down on ANY deletion of a bridged
		-- track — see the "Teardown" note in the header. DisconnectFromGrids
		-- guards on supply_tunnel_set (cleared by RemoveSupplyTunnel), so paths
		-- that already disconnected (OnDemolish) no-op here.
		local orig_done = T.Done
		function T:Done(done_map, ...)
			if not done_map and self.supply_tunnel_set then
				pcall(self.DisconnectFromGrids, self)
			end
			return orig_done(self, done_map, ...)
		end

		OnMsg.StationsConnected = function(s1, s2, track)
			pcall(bridge_if_needed, track)
		end

		-- Sweep for tracks already saved in the unbridged state — once per load,
		-- and idempotent (an already-bridged track returns early above).
		OnMsg.PostLoadGame = function()
			local cities = rawget(_G, "Cities")
			if type(cities) ~= "table" then return end
			local repaired = 0
			for _, city in ipairs(cities) do
				local tracks = city and city.labels and city.labels.TrackBase
				for _, track in ipairs(tracks or empty_table) do
					local ok, res = pcall(bridge_if_needed, track)
					if ok and res == "bridged" then repaired = repaired + 1 end
				end
			end
			SMRFixPack.TrackPowerBridge.repaired = repaired
		end
	end,
})
