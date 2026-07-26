-- F50: A landed automatic rocket sends every drone that is on its way to it back
-- to Idle, once an hour, forever.
--
-- Defect: CargoTransporterNew:UpdateCargoResourceRequests
-- (Lua\CargoTransporterNew.lua:1238-1271) brackets its whole body with
--     if self.working then self:DisconnectFromCommandCenters() end
--     ... update request amounts ...
--     if self.working then self:ConnectToCommandCenters() end
-- Disconnecting makes every command center run DroneControl:OnRemoveBuilding
-- (DroneControl.lua:720-729), which does `drone:SetCommand("Idle")` for every
-- drone whose goto_target resolves to the rocket. For a landed automatic rocket
-- this runs EVERY GAME HOUR: HourlyUpdate (UniversalRocket.lua:1357-1370) ->
-- CreateAutoCargoRequest -> SetCargoRequest -> UpdateCargoResourceRequests. Any
-- drone trip longer than one game hour can therefore never complete, no matter
-- what priority the player sets — and rockets start with zero drones of their own
-- and are excluded from shuttle transport, so distant rockets simply never get
-- loaded. This is the "drones ignore rocket cargo" report.
--
-- The disconnect is only meaningful when a NEW request object is created
-- (AddCargoDemandRequest, :1202-1207); the rest of the body just calls SetAmount
-- on requests that already exist, which command centers re-read in place.
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\CargoTransporterNew.lua:1238-1271 (shipped Src, game 1.0.7.396349) that decides up
-- front whether any request is actually missing and only then does the
-- disconnect/reconnect dance. A transporter that somehow has no command centers
-- still gets its one-time connect. Changes marked -- FIX.

SMRFixPack.Register("RocketDroneChurn", {
	title = "Landed rockets stop sending their delivery drones back to Idle every hour",
	apply = function()
		local CT = rawget(_G, "CargoTransporterNew")
		if type(CT) ~= "table" or type(CT.UpdateCargoResourceRequests) ~= "function" then
			return "CargoTransporterNew.UpdateCargoResourceRequests not found (game update changed it?)"
		end
		if type(CT.AddCargoDemandRequest) ~= "function" or type(CT.AddCargoSupplyRequest) ~= "function" then
			return "CargoTransporterNew cargo request helpers not found (game update changed them?)"
		end

		function CT:UpdateCargoResourceRequests()
			-- FIX (F50): only a request that has to be CREATED needs the command
			-- centers cycled; updating the amount of an existing one does not.
			local needs_reconnect = false
			for _, res_id in ipairs(TransportableResourceIds) do
				if not self.demand[res_id] then
					needs_reconnect = true
					break
				end
			end
			if needs_reconnect and self.working then -- FIX: was unconditional
				self:DisconnectFromCommandCenters()
			end
			-- resource and storable_resources are used in resource transportation, so they need to be set to whatever the transporter can carry
			-- copy to prevent someone from modifying the original table and messing up the resource transportation
			self.storable_resources = table.copy(TransportableResourceIds)
			-- make sure resource references the same table as storable_resources like in other storage classes
			self.resource = self.storable_resources
			for _, res_id in ipairs(TransportableResourceIds) do
				local is_refuel_resource = self:HasMember("FuelResource") and self.FuelResource == res_id
				local additional_demand_flags = is_refuel_resource and const.rfRestrictorRocket or 0
				local additional_amount = is_refuel_resource and self:GetFuelResourceRequest()
				local additional_requested_amount = Max(0, additional_amount or 0)

				if not self.demand[res_id] then
					local unit_count = g_Consts.CargoRequestDroneAmount
					self:AddCargoDemandRequest(res_id, 0, additional_demand_flags + self.demand_r_flags, unit_count)
					self:AddCargoSupplyRequest(res_id, 0, self.supply_r_flags, unit_count)
				end
				local res_in_cargo = table.get(self, "cargo", res_id)
				if not res_in_cargo then
					self.cargo[res_id] = { class = res_id, amount = 0, requested = 0 }
				end
				local requested = (res_in_cargo and res_in_cargo.requested or 0) + additional_requested_amount
				local amount = res_in_cargo and res_in_cargo.amount or 0
				local amount_diff = requested - amount
				self.supply[res_id]:SetAmount(Max(0, -amount_diff))
				self.demand[res_id]:SetAmount(Max(0, amount_diff))
			end
			-- FIX: reconnect after creating requests, and cover the case of a working
			-- transporter that has never been connected to anything.
			if self.working and (needs_reconnect or #(self.command_centers or empty_table) == 0) then
				self:ConnectToCommandCenters()
			end
		end
	end,
})
