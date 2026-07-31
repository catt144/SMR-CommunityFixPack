-- F46: Trains dump cargo at stations where the player switched that resource off.
--
-- Defect: Train:UnloadAll (Lua\Units\Train.lua:783-803) empties the train into
-- whatever the current station has room for:
--     local station_cap = station.demand[res]:GetTargetAmount()
--     local unload_amnt = Min(carried, station_cap)
-- with no station:IsResourceEnabled(res) check. Switching a resource off at a
-- station only removes its demand request from task_requests
-- (UniversalStorageDepotBase:SetAcceptResource, StorageDepot.lua:641-668) — the
-- demand request object itself lives on and still reports a target amount, so
-- the unload sails through.
--
-- The cargo planner then sees stock the station is not supposed to hold and
-- treats it as "forbidden excess" that must be hauled back out
-- (Train:TransferCargo, Train.lua:868, :905-939), which is the resource
-- ping-pong players see: a train drops Waste Rock at a station with Waste Rock
-- disabled, and the next train picks it up again.
--
-- Note the loading side is already correct — both load paths check
-- dest:IsResourceEnabled (:905-912, :930-939), so a train only ever takes on
-- cargo bound for a station that accepts it. Cargo with nowhere to go therefore
-- means something changed mid-trip (the switch was flipped, a station was
-- demolished, the train was re-assigned).
--
-- Patch approach: full replacement of Train:UnloadAll — a copy of
-- Lua\Units\Train.lua:783-803 (shipped Src, game 1.0.7.396349) with one guard added,
-- marked -- FIX. Replacement rather than a wrapper because the decision is
-- mid-loop: a pre-wrapper cannot see it and a post-wrapper runs after the
-- resources have already moved.
--
-- The guard deliberately keeps two escape hatches so a fix for ping-pong can
-- never stall a train holding undeliverable cargo:
--   * if NO station on this train's route accepts the resource, the dump is
--     allowed — the cargo has nowhere else to go and holding it would occupy
--     the hold for the rest of the game;
--   * a train on its way to be stored (is_stopping) always dumps, because it is
--     about to be refabbed and anything still aboard is destroyed with it
--     (Train.lua:85-86, :457-458 -> DestroySilent -> DoDemolish).

SMRFixPack.Register("TrainCargoDumping", {
	title = "Trains stop dumping cargo at stations where that resource is switched off",
	apply = function()
		local err = SMRFixPack.Require("TrainCargoDumping", {
			{ class = "Train", method = "UnloadAll" },
			-- IsResourceEnabled is declared on UniversalStorageDepotBase, not on
			-- Station: mod code loads before the classes are flattened, so looking
			-- for it on Station would find nil and deactivate this fix for nothing.
			{ class = "UniversalStorageDepotBase", method = "IsResourceEnabled" },
			{ global = "RequestUnassignUnit" },
		})
		if err then return err end
		local T = Train

		-- Does any OTHER station this train can reach on its current route still
		-- accept `res`? Reads the route table directly (city.train_track_routes,
		-- TrainTransport.lua:368) rather than calling ForEachStationAlongTrack,
		-- which keeps shared iteration state in a file-local table.
		local function route_accepts_elsewhere(train, station, res)
			local city = station.city
			local routes = city and city.train_track_routes
			local route = routes and train.track and routes[train.track]
			if not route then return false end
			for _, st in ipairs(route) do
				-- task_requests is what IsResourceEnabled reads (StorageDepot.lua:583-587);
				-- checking it here keeps the query safe on anything in the route
				-- table that is not a live universal depot.
				if st ~= station and type(st) == "table" and st.task_requests
					and st.demand and st.demand[res] and st.IsResourceEnabled
					and st:IsResourceEnabled(res) then
					return true
				end
			end
			return false
		end

		function T:UnloadAll()
			local station = self.current_station

			-- cancel all our "inbound" assignments, we'll recreate them
			for dest, cargo_list in pairs(self.assigned_resources) do
				for res, amount in pairs(cargo_list) do
					RequestUnassignUnit(dest.demand[res], self, amount, false)
				end
			end
			self.assigned_resources = {}

			for _, res in ipairs(station.storable_resources) do
				local carried = self:GetStoredAmount(res)
				local station_cap = station.demand[res]:GetTargetAmount()
				local unload_amnt = Min(carried, station_cap)
				-- FIX (F46): respect the station's per-resource switch. Skip the
				-- unload only while somewhere else on the route would take it,
				-- and never while this train is on its way to be stored.
				if unload_amnt > 0 and not self.is_stopping
					and station.IsResourceEnabled and not station:IsResourceEnabled(res)
					and route_accepts_elsewhere(self, station, res) then
					unload_amnt = 0
				end
				if unload_amnt > 0 then
					station:AddResource(unload_amnt, res)
					self:AddResource(-unload_amnt, res)
				end
			end
		end
	end,
})
