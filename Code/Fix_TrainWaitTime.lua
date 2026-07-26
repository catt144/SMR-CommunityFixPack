-- F21: time spent waiting on a train platform is charged again as time spent
-- riding the train — as a Comfort penalty on the passenger and as "spent time"
-- on both the train and the track.
--
-- Defect: `ticket.start_wait` is stamped when the colonist reaches the platform
-- (`Lua\Units\ColonistTransport.lua:491-497`) and is never restamped when they
-- actually board. `Colonist:BoardVehicle` (:503-528) closes the waiting period
-- correctly for the station:
--     if self.holder then
--         self.holder:AddSpentTime(GameTime() - self.transport_ticket.start_wait)
--     end
-- but leaves `start_wait` pointing at the platform arrival, so
-- `Colonist:ExitVehicle` (:540-571) computes
--     local travel_time = GameTime() - ticket.start_wait
-- over wait + ride, and spends that figure three times:
--   * `self:ChangeComfort(0 - MulDivRound(stat_scale, travel_time, const.HourDuration), "travel time")`
--     (:555-557) — the passenger pays Comfort for standing on the platform, and
--     since the penalty is skipped entirely once LuxuriousTrains is researched,
--     the waiting charge quietly rides along with the travel charge;
--   * `vehicle:AddSpentTime(travel_time)` and `vehicle.track:AddSpentTime(travel_time)`
--     (:568-569) — the same wait the STATION already recorded at :511 is added
--     to the train and the track statistics as well (TransportStatistics.lua),
--     so the colony's transport numbers double-count every platform wait.
--
-- Patch approach: full replacement of `Colonist:BoardVehicle` — a copy of
-- ColonistTransport.lua:503-528 (shipped Src, 2026-07) with one line added,
-- marked -- FIX. Replacement rather than a wrapper because the restamp has to
-- happen mid-function: it must come AFTER the station is credited with the wait
-- at :511 and BEFORE the `while self.holder == vehicle` loop at :525, which
-- blocks for the whole journey — so a pre-wrapper would erase the wait before
-- the station is paid, and a post-wrapper would not run until the ride is over.
--
-- Deliberately unchanged: the station still receives the full wait, so no
-- statistic loses anything; only the boundary between "waiting" and "travelling"
-- moves to where the colonist actually boards.

SMRFixPack.Register("TrainWaitTime", {
	title = "Waiting on a train platform no longer counts as time spent riding",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.BoardVehicle) ~= "function" then
			return "Colonist.BoardVehicle not found (game update changed it?)"
		end
		local S = rawget(_G, "Station")
		if type(S) ~= "table" then
			return "Station class not found (game update changed it?)"
		end
		if type(rawget(_G, "RebuildInfopanel")) ~= "function"
			or type(rawget(_G, "PrgAmbientLife")) ~= "table" then
			return "RebuildInfopanel/PrgAmbientLife not found (game update changed it?)"
		end

		function C:BoardVehicle(vehicle)
			if not self.transport_ticket then
				if IsKindOf(self.holder, "Station") then
					self.holder:RemoveColonist(self)
				end
				return
			end
			if self.holder then
				self.holder:AddSpentTime(GameTime() - self.transport_ticket.start_wait)
			end
			-- FIX (F21): the wait is now paid for — restart the clock so the train,
			-- the track and the "travel time" Comfort penalty measure the ride only.
			self.transport_ticket.start_wait = GameTime()
			self:PushDestructor(function(self)
				self:SetHolder(vehicle)
				vehicle:IncreasePassengersCount()
				vehicle.track:IncreasePassengersCount()
				table.remove_entry(self.transport_ticket.src_station.waiting_for_train, self)
				self.transport_ticket.vehicle = vehicle
				self.transport_ticket.stage = "Traveling"
				RebuildInfopanel(vehicle.track)
			end)
			self:PopAndCallDestructor()
			RebuildInfopanel(self.transport_ticket.src_station)
			self:SetState("idle")
			while self.holder == vehicle do
				self:PlayPrg(PrgAmbientLife.VisitDefault, const.HourDuration, vehicle)
			end
		end
	end,
})
