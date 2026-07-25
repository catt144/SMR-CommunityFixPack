-- F69: An asteroid lander unloads its own return fuel and strands itself.
--
-- Defect: the asteroid flight policy deliberately loads a double fuel ration and
-- reserves half of it for the trip home — OnGetFuelResourceRequest returns
-- `2 * FuelResourceAmount, FuelResourceAmount` (Data\FlightPolicyDef.lua:208-211),
-- and ConsumeFuel burns only the difference (UniversalRocket.lua:1664-1673). But
-- CmdLand finishes with
--     self:SetFlightData(self.arrival_loc, self:IsAutoModeEnabled() and self.departure_loc)
-- (UniversalRocket.lua:414) — in MANUAL mode the second argument is false, so
-- arrival_loc is cleared. GetFuelResourceRequest (:1639-1642) then short-circuits
-- to 0 for want of a destination, CmdUnload zeroes every cargo request (:486-494),
-- and GetCargoResourcesStatus (CargoTransporterNew.lua:1124-1141) sees fuel in the
-- hold that nobody asked for -> "unloading". The reserved return fuel is carried
-- down the ramp and dumped on the ground. On an asteroid with no drones and no
-- fuel production that is permanent: "no fuel, no drones, can't send another
-- lander". Automatic mode is unaffected (it keeps a destination).
--
-- Patch approach: chained wrapper on GetFuelResourceRequest. A lander sitting on
-- an asteroid with no destination selected still needs one ration to get home, so
-- report that instead of 0. We return it as BOTH the request and the
-- return-trip reserve, so any ConsumeFuel in this state burns nothing
-- (Max(0, amount - return_trip_fuel) == 0) — the fix can only preserve fuel,
-- never spend it. Every other case falls through to the shipped function.

SMRFixPack.Register("LanderReturnFuel", {
	title = "Asteroid landers keep their return fuel instead of unloading it on the asteroid",
	apply = function()
		local R = rawget(_G, "UniversalRocketBase")
		if type(R) ~= "table" or type(R.GetFuelResourceRequest) ~= "function" then
			return "UniversalRocketBase.GetFuelResourceRequest not found (game update changed it?)"
		end
		if type(R.GetDepartureLocType) ~= "function" then
			return "UniversalRocketBase.GetDepartureLocType not found (game update changed it?)"
		end
		local types = rawget(_G, "g_RocketTypes")
		if type(types) ~= "table" or types.LanderRocket == nil then
			return "g_RocketTypes.LanderRocket not found (game update changed it?)"
		end
		local LanderRocket = types.LanderRocket

		local orig = R.GetFuelResourceRequest
		function R:GetFuelResourceRequest()
			-- FIX (F69): a lander parked on an asteroid without a destination still
			-- has to fly home; keep its ration requested so it is not treated as
			-- excess cargo and hauled out.
			if not self.arrival_loc and self.RocketType == LanderRocket
					and self:GetDepartureLocType() == "asteroid" then
				local reserve = Max(0, self.FuelResourceAmount or 0)
				return reserve, reserve
			end
			return orig(self)
		end
	end,
})
