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
-- Patch approach: pre-hook Station:OnDemolish (chained wrapper). We store the
-- affected trains via their legitimate DestroySilent path (prefab refund + the
-- "A Train was stored" notification) BEFORE Building:OnDemolish broadcasts
-- BuildingDemolished — so the vanilla deleting handler finds no matching trains
-- and becomes a harmless no-op. The vanilla handler itself stays untouched
-- (OnMsg handlers are additive and can't be safely removed).

SMRFixPack.Register("TrainsToVoid", {
	title = "Demolishing a station stores its trains instead of permanently deleting them",
	apply = function()
		local Station = rawget(_G, "Station")
		if not Station or type(Station.OnDemolish) ~= "function" then
			return "Station.OnDemolish not found (game update changed it?)"
		end
		if not (rawget(_G, "Train") and type(Train.DestroySilent) == "function") then
			return "Train.DestroySilent not found (game update changed it?)"
		end

		local orig = Station.OnDemolish
		function Station:OnDemolish(...)
			local trains = self.city and self.city.labels and self.city.labels.Train
			for i = #(trains or empty_table), 1, -1 do
				local train = trains[i]
				if IsValid(train) and train.current_station == self then
					train:DestroySilent("station", self) -- refunds the prefab + shows "stored" notification
				end
			end
			return orig(self, ...)
		end
	end,
})
