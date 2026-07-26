-- F11: A train parks at a platform and never leaves again, blocking the line.
--
-- Defect: Colonist:ExitVehicle (Lua\Units\ColonistTransport.lua:540-570) has a
-- guard for a passenger that is no longer aboard (the dev comment blames a
-- CargoTransporter abducting them). The guard tries to drop the passenger from the
-- train's list with
--     table.remove(vehicle.units, self)
-- but table.remove takes an integer POSITION, not a value — the intended API is
-- table.remove_entry, which the codebase uses everywhere else. The call raises,
-- which aborts ExitVehicle before DiscardTransportTicket runs, so the colonist is
-- still listed as a passenger. Train:UnloadTrain (Units\Train.lua:443-453) then
-- spins waiting for a passenger who can never disembark and the train occupies the
-- platform for good.
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\Units\ColonistTransport.lua:540-570 (shipped Src, game 1.0.7.396349) with the one call
-- corrected. The file-local stat_scale is recreated (ColonistTransport.lua:1).
-- Change marked -- FIX.

SMRFixPack.Register("TrainPlatformWedge", {
	title = "A stale passenger no longer wedges a train at the platform forever",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.ExitVehicle) ~= "function" then
			return "Colonist.ExitVehicle not found (game update changed it?)"
		end
		if type(table.remove_entry) ~= "function" then
			return "table.remove_entry not found (game update changed it?)"
		end
		local stat_scale = const.Scale and const.Scale.Stat
		if not stat_scale then
			return "const.Scale.Stat not found (game update changed it?)"
		end

		function C:ExitVehicle(vehicle)
			if not self.holder or self.holder ~= vehicle or not IsSameMap(self, vehicle) then
				--abducted by CargoTransporter?
				TrainsLogging.warn(self, "not in train", self.command)
				table.remove_entry(vehicle.units, self) -- FIX (F11): was table.remove(list, value), which raises
				self:DiscardTransportTicket()
				return
			end
			local station = self.transport_ticket.dst_station
			local ticket = self.transport_ticket
			self:DiscardTransportTicket()
			local travel_time = GameTime() - ticket.start_wait
			self:PushDestructor(function(self)
				self:SetHolder(station)
				self:ExitBuilding(station)
				if not UIColony:IsTechResearched("LuxuriousTrains") then
					self:ChangeComfort(0 - MulDivRound(stat_scale, travel_time, const.HourDuration), "travel time")
				end
				if vehicle.track and vehicle.track.seen_forest then
					self:ChangeSanity(TechDef.GreenView.param1, "seen forest")
				end
				if IsValid(ticket.destination) then
					return CommandObject.SetCommand(self, ticket.reason, ticket.destination, ticket.param)
				else
					return self:SetCommand("Idle", true)
				end
			end)
			RebuildInfopanel(vehicle.track)
			vehicle:AddSpentTime(travel_time)
			vehicle.track:AddSpentTime(travel_time)
			self:PopAndCallDestructor()
		end
	end,
})
