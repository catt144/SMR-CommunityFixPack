-- F21: time spent waiting on a train platform is charged again as time spent
-- riding the train — as a Comfort penalty on the passenger and as "spent time"
-- on both the train and the track.
-- F86 Tier-2 REWRITE (2026-08-01, spec `docs/reports/SAVE_SAFETY_REDESIGN.md`
-- §6.2 Tier 2): layer 3 — the restamp moves onto a synchronous input and
-- vanilla's blocking `Colonist:BoardVehicle` is left alone.
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
-- Fix shape (layer 3, FIX_POLICY §3a — replaces the `BoardVehicle` body copy
-- shipped until 2026-08-01). `BoardVehicle` blocks for the entire journey in its
-- `while self.holder == vehicle` / `PlayPrg` loop (:525-527), so a copy of it is
-- F86 exposure route (a) and a REPLACE-class one. The restamp does not need that
-- body: it needs the MOMENT, and vanilla marks the moment itself by calling
-- `TransportStatistics:AddSpentTime` on the station at :511 — the line that pays
-- the station for the wait, immediately before the ride begins.
--
-- The wrapped input is **VERIFIED SYNCHRONOUS**: `TransportStatistics:AddSpentTime`
-- (`Lua\TransportStatistics.lua:31-37`) is `#`, `table.remove`, `table.insert` and
-- arithmetic — no yield, no blocking callee; `tools/blocking_analysis.py` reports
-- it `clear`. Its call sites are enumerated and there are exactly three in the
-- whole shipped source, all in `ColonistTransport.lua`: `:511` on the STATION
-- (this one), `:568` on the Train and `:569` on the TrainTrack. So
-- `IsKindOf(self, "Station")` is a precise key for the boarding moment and cannot
-- reach the other two.
--
-- Which colonist is boarding is answered exactly, not guessed: `BoardVehicle` is
-- a COMMAND (`Train.lua:967` — `colonist:SetCommand("BoardVehicle", self)`), so it
-- runs on that colonist's own command thread, and the colonist is still in the
-- station's `waiting_for_train` list at :511 (it is removed later, in the
-- destructor at :517). One scan of that list for `command_thread == CurrentThread()`
-- identifies them; at most one object in the game can own a given command thread.
--
-- Deliberately unchanged: the station still receives the full wait (our work
-- happens before `orig`, but `value` was computed by the caller at :511 before the
-- call, so it cannot be affected either way), so no statistic loses anything; only
-- the boundary between "waiting" and "travelling" moves to where the colonist
-- actually boards.
--
-- Disclosed narrowing vs. the pre-2026-08-01 shipped fix: that copy restamped
-- unconditionally, this one restamps only when vanilla actually credits a Station
-- — i.e. when `self.holder` is a Station at :510. Every shipped path reaches
-- boarding that way (`GoToStation` does `EnterBuilding(starting_station)` and only
-- then joins `waiting_for_train`, :447-455), so the difference is unreachable in
-- vanilla; if some future path did board a colonist with no station holder, the
-- old F21 arithmetic would simply persist for them. Fail-safe, FIX_POLICY §2.
--
-- §3a COMPLIANCE, stated: no mod-owned thread; no replaced body; the module's
-- only code is a wrapper on the verified-synchronous `AddSpentTime`, which cannot
-- be on the stack while a thread is blocked (route (a) closed), is held only by
-- the `TransportStatistics` classdef and the classes flattened from it (safe by
-- construction, route (b)), and stores no function value (route (c)).
-- SAVE FOOTPRINT (FIX_POLICY §3): none.

SMRFixPack.Register("TrainWaitTime", {
	title = "Waiting on a train platform no longer counts as time spent riding",
	apply = function()
		local err = SMRFixPack.Require("TrainWaitTime", {
			{ class = "TransportStatistics", method = "AddSpentTime" },
			{ class = "Station",
			  reason = "Station class not found (game update changed it?)" },
			-- the two shipped sites this repair reasons about: the boarding moment
			-- it keys on, and the triple-spend consumer it corrects
			{ class = "Colonist", method = "BoardVehicle" },
			{ class = "Colonist", method = "ExitVehicle" },
			-- the identification machinery: the station's waiting list and the
			-- command-thread field. Both are class defaults (Station.lua:84,
			-- CommandObject.lua:91), so `false` is the expected value here.
			{ path = { "Station", "waiting_for_train" }, kind = "any",
			  reason = "Station.waiting_for_train not found (game update changed it?)" },
			{ path = { "CommandObject", "command_thread" }, kind = "any",
			  reason = "CommandObject.command_thread not found (game update changed it?)" },
			{ global = "CurrentThread" },
			{ global = "IsKindOf" },
		})
		if err then return err end
		local TS = TransportStatistics
		local orig_add = TS.AddSpentTime

		function TS:AddSpentTime(value, ...)
			-- FIX (F21): this is the ONLY AddSpentTime call made on a Station
			-- (ColonistTransport.lua:511) and it is vanilla's own "the wait is now
			-- paid for" line. Restart the ticket clock here so the train, the track
			-- and the "travel time" Comfort penalty measure the ride only.
			if IsKindOf(self, "Station") then
				local waiting = self.waiting_for_train
				local thread = CurrentThread()
				if waiting and thread then
					for i = 1, #waiting do
						local c = waiting[i]
						if c and c.command_thread == thread and c.transport_ticket then
							c.transport_ticket.start_wait = GameTime()
							break
						end
					end
				end
			end
			return orig_add(self, value, ...)
		end
	end,
})
