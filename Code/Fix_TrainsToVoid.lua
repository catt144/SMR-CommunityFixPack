-- F64: Demolishing a station permanently deletes trains ("trains go to void").
--
-- Defect: trains are a colony-counted resource (city.available_prefabs["Train"]).
-- The count is refunded only by Train:OnDemolish (Lua\Units\Train.lua:205-209),
-- which only runs via Demolishable:DoDemolish. But when a Station is demolished,
-- the OnMsg.BuildingDemolished handler (Lua\Buildings\Station.lua:163-171) does a
-- bare DoneObject() on every train whose current_station is that station — no
-- refund, no notification — and it runs synchronously BEFORE Station:Done's proper
-- storing loop (Station.lua:145-149), which then finds nothing. Because
-- current_station stays set to the DEPARTURE station for a whole trip
-- (Train.lua:164-166), trains mid-transit elsewhere are vaporized too. Once the
-- counter hits 0, "Send out Train" is disabled at every station forever
-- (Station.lua:653-660), even after rebuilding all rail.
--
-- Patch approach: pre-hook the demolition path (chained wrapper). We store the
-- affected trains via their legitimate DestroySilent path (prefab refund + the
-- "A Train was stored" notification) BEFORE Building:OnDemolish broadcasts
-- BuildingDemolished — so the vanilla deleting handler finds no matching trains
-- and becomes a harmless no-op. The vanilla handler itself stays untouched
-- (OnMsg handlers are additive and can't be safely removed).
--
-- The hook goes on Building.OnDemolish (Building.lua:873-883), gated to Stations:
-- Station does not declare OnDemolish of its own, and mod code runs before the
-- classes are built (autorun.lua:423 vs OnMsg.Autorun in classes.lua:980), so at
-- this point Station is still a classdef and nothing is inherited into it yet.
-- Demolishable:OnDemolish (Demolishable.lua:157) is empty and OnDemolish is not
-- an auto-resolved method, so Building's is the only implementation in the chain.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Buildings/Station.lua OnMsg.BuildingDemolished sha256=77d6a439755dd83af1e7ab928766edba1c3155cd7af56d88445f60f1f8c270ad
--   (Lua/Buildings/Station.lua:289-299 at pin time)
-- DEFECT: if train\.current_station == bld then\s+DoneObject\(train\)
--   a bare DoneObject: no prefab refund, no notification, and current_station
--   still names the DEPARTURE station for a whole trip

SMRFixPack.Register("TrainsToVoid", {
	title = "Demolishing a station stores its trains instead of permanently deleting them",
	apply = function()
		local err = SMRFixPack.Require("TrainsToVoid", {
			{ class = "Building", method = "OnDemolish" },
			{ class = "Station",
			  reason = "Station class not found (game update changed it?)" },
			{ class = "Train", method = "DestroySilent" },
		})
		if err then return err end

		local orig = Building.OnDemolish
		function Building:OnDemolish(...)
			if IsKindOf(self, "Station") then
				local trains = self.city and self.city.labels and self.city.labels.Train
				for i = #(trains or empty_table), 1, -1 do
					local train = trains[i]
					if IsValid(train) and train.current_station == self then
						train:DestroySilent("station", self) -- refunds the prefab + shows "stored" notification
					end
				end
			end
			return orig(self, ...)
		end
	end,
})
