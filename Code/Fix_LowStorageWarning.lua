-- F12: The "Insufficient Resources" warning can never fire for Food or for
-- maintenance resources.
--
-- Defect: ResourceTracking:GatheredResourcesOnHourlyUpdate
-- (Lua\ResourceTracking.lua:211-316) computes the remaining supply window as
--     local num_hours = v > 0 and transportable_resources[k]*const.HoursPerDay / v*const.HoursPerDay or 0
-- The missing parentheses make that `((supply * 24) / v) * 24`, and this engine's
-- `/` truncates — so the result is either 0 or at least 24. The guard right below
-- needs `num_hours > 0 and num_hours < const.MinDaysMaintenanceSupplyBeforeNotification`
-- (3), which those two ranges can never satisfy. The Food branch (:229-230) repeats
-- the same expression against MinDaysFoodSupplyBeforeNotification. Both warnings are
-- therefore dead: the colony runs out of Food, Machine Parts or Electronics with no
-- notice at all. The grid branches further down (:247-310) use a different, correct
-- formula, which is what makes the Power/Water/Air warnings work.
--
-- The intended value is hours of supply: the notification renders `hours` and sets
-- `expiration = num_hours * const.HourDuration`, and the constants are "MinDays…"
-- (_GameConst.lua:10-11), i.e. days that need converting to hours before comparing.
--
-- Patch approach: full replacement. Wrapping it from outside cannot work: because the
-- add branch is unreachable, the shipped else branch REMOVES the Food/maintenance
-- entry every single hour, and re-adding it afterwards destroys and recreates the whole
-- notification whenever it is the only object left (RemoveObjectFromNotification →
-- RemoveNotification at Notifications.lua:284-287, AddObjectToNotification →
-- AddNotification at :233-235) — FX replay and reset dismiss/suppression state once per
-- game hour. Taking the add branch in the first place is the only correct repair.
--
-- So: a copy of Lua\ResourceTracking.lua:204-316 (shipped Src, game 1.0.7.396349), byte-identical
-- but for the four lines marked `-- FIX (F12):` — the two num_hours expressions and
-- their two comparisons. Two notes on the copy:
--   * the file-locals the shipped function closes over (GetGridObj and the reused
--     `to_remove` scratch table, :204-209) are unreachable from mod code, so they are
--     recreated verbatim as locals of apply();
--   * the shipped maintenance expression would nil-deref if a consumed resource had no
--     entry in transportable_resources; since the fix line already rewrites exactly that
--     expression it carries an `or 0`. Everything else, including the truncating
--     division in the grid branches, is left exactly as shipped.

SMRFixPack.Register("LowStorageWarning", {
	title = 'The "Insufficient Resources" warning works again for Food and maintenance resources',
	apply = function()
		local WARN_CONSTS = "supply-warning constants not found (game update changed them?)"
		local err = SMRFixPack.Require("LowStorageWarning", {
			{ class = "ResourceTracking", method = "GatheredResourcesOnHourlyUpdate" },
			-- GatherTransportableResources is called at :216 but declared engine-side only.
			{ global = "GatherTransportableResources" },
			{ global = "GetCityResourceOverview" },
			{ global = "FindNotification" },
			{ global = "AddObjectToNotification" },
			{ global = "RemoveObjectFromNotification" },
			{ global = "GetCommandCenterPowerGrids" },
			{ global = "GetCommandCenterLifeSupportGrids" },
			{ global = "MulDivRound" },
			{ global = "ripairs" },
			{ path = { "const", "MinDaysMaintenanceSupplyBeforeNotification" }, reason = WARN_CONSTS },
			{ path = { "const", "MinDaysFoodSupplyBeforeNotification" }, reason = WARN_CONSTS },
			{ path = { "const", "HoursPerDay" }, reason = WARN_CONSTS },
		})
		if err then return err end
		local RT = ResourceTracking

		local function GetGridObj(grid)
			local obj = grid.storages[1] or grid.producers[1] or grid.consumers[1] or grid.elements[1]
			return obj and obj.building
		end

		local to_remove = {}

		function RT:GatheredResourcesOnHourlyUpdate(map)
			local notification = FindNotification("InsufficientResources", map)
			local maintenance_resources = self.maintenance_resources_consumed_yesterday
			local transportable_resources = {}
			local resource_overview = GetCityResourceOverview(self)	
			GatherTransportableResources(transportable_resources, self)
			for k,v in pairs(maintenance_resources) do
				-- FIX (F12, second defect — found live in playtest PT-07, 2026-07-27):
				-- "Food" can appear in the maintenance-consumed table too, and BOTH this
				-- loop and the dedicated food branch below write the SAME "Food" object
				-- key on the SAME notification. This loop's hours are maintenance-based,
				-- so its guard fails for Food and its else-path deleted the entry the
				-- food branch had added — destroying the (single-object) notification
				-- and forcing a recreate one line later, replaying the FX and the
				-- "Warning! Insufficient resources" voice every game hour. The food
				-- branch owns the "Food" key; skip it here. Latent in the shipped body:
				-- with the broken math neither branch could ever add, so the collision
				-- had no visible effect.
				if k ~= "Food" then
				-- FIX (F12): the shipped `a*const.HoursPerDay / v*const.HoursPerDay` parses as
				-- `((a*24)/v)*24`, and `/` truncates here: the result is 0 or >= 24, so the
				-- `0 < num_hours < 3` guard below can never hold and the warning is dead.
				-- MulDivRound yields the real hours of supply; the added `or 0` also removes
				-- the nil deref the shipped expression risks when a consumed resource has no
				-- stock entry at all.
				local num_hours = v > 0 and MulDivRound(transportable_resources[k] or 0, const.HoursPerDay, v) or 0
				-- FIX (F12): the constant counts days, num_hours counts hours - scale to compare.
				if v > 0 and num_hours>0 and num_hours < const.MinDaysMaintenanceSupplyBeforeNotification * const.HoursPerDay  then
					AddObjectToNotification(k, { resource = k, hours = num_hours, expiration = num_hours*const.HourDuration }, "InsufficientResources", map)
				else
					RemoveObjectFromNotification(k, notification)
				end
				end
			end

			-- food
			local food_consumed = resource_overview:GetConsumedByConsumptionYesterday("Food")
			local food_total = resource_overview:GetAvailable("Food")
			-- FIX (F12): the same broken expression as the maintenance branch above.
			local num_hours = food_consumed>0 and MulDivRound(food_total, const.HoursPerDay, food_consumed) or 0
			-- FIX (F12): the constant counts days, num_hours counts hours - scale to compare.
			if food_total>0 and food_consumed>0 and num_hours>0 and num_hours < const.MinDaysFoodSupplyBeforeNotification * const.HoursPerDay  then
				AddObjectToNotification("Food", { resource = "Food", hours = num_hours, expiration = num_hours*const.HourDuration }, "InsufficientResources", map)
			else
				RemoveObjectFromNotification("Food", notification)
			end
			
			local objects = notification and notification.objects
			table.clear(to_remove, true)
			for _, obj in ripairs(objects) do
				local data = objects[obj]
				if type(data) == "table" and (data.resource=="Power" or data.resource=="Water" or data.resource=="Air") then
					to_remove[obj] = true
				end
			end
			local electricity_grids = GetCommandCenterPowerGrids(false, self)
			local lifesupport_grids = GetCommandCenterLifeSupportGrids(false, self)
			
			for i, egrid in ipairs(electricity_grids) do
				local el_consumption    = egrid.consumption
				local el_production     = egrid.production
				local el_stored         = 0
				local el_discharge      = 0
				for _, storage in ipairs(egrid.storages) do
					el_stored = el_stored + storage.current_storage
					el_discharge = el_discharge + storage.discharge
				end			

			   -- power
			   local needed_discharge = el_consumption - el_production
			   local required = Min(needed_discharge, el_discharge)
			   local num_hours = el_consumption ~= el_production and required > 0 and el_stored/required or 0
				if el_stored>0 and num_hours>0 and const.MinHoursPowerResourceSupplyBeforeNotification > num_hours then
					AddObjectToNotification(egrid, { obj = GetGridObj(egrid), resource = "Power", hours = num_hours, expiration = Max(num_hours, 1)*const.HourDuration }, "InsufficientResources", map)
					to_remove[egrid] = nil
				end
				if el_consumption <= el_production or num_hours<=0 then
					RemoveObjectFromNotification(egrid, notification)
				end	
			end
			
			for i, lgrid in ipairs(lifesupport_grids) do
				local lair, lwater = lgrid.air, lgrid.water
				local air_consumption   = lair.consumption
				local air_production    = lair.production
				local air_discharge, air_stored = 0, 0
				
				for _, storage in ipairs(lair.storages) do
					air_stored = air_stored + storage.current_storage
					air_discharge = air_discharge + storage.max_discharge
				end	

				local water_consumption = lwater.consumption
				local water_production  = lwater.production
				local water_stored, water_discharge = 0, 0
				for _, storage in ipairs(lwater.storages) do
					water_stored = water_stored + storage.current_storage
					water_discharge = water_discharge + storage.max_discharge
				end	
				--water
			   local water_needed_discharge = water_consumption - water_production
			   local required = Min(water_needed_discharge, water_discharge) 
			   local num_hours = water_consumption ~= water_production and required > 0 and water_stored/required or 0
				if water_stored>0 and num_hours>0 and const.MinHoursWaterResourceSupplyBeforeNotification > num_hours then
					AddObjectToNotification(lwater, { obj = GetGridObj(lwater), resource = "Water", hours = num_hours, expiration = Max(num_hours, 1)*const.HourDuration }, "InsufficientResources", map)
					to_remove[lwater] = nil
				end
				if water_consumption <= water_production or num_hours<=0 then
					RemoveObjectFromNotification(lwater, notification)
				end
			   -- air
				local air_needed_discharge = air_consumption - air_production
				local required = Min(air_needed_discharge, air_discharge)
				local num_hours = air_consumption ~= air_production and required > 0 and air_stored/required or 0
				if air_stored>0 and num_hours>0 and const.MinHoursAirResourceSupplyBeforeNotification > num_hours then
					AddObjectToNotification(lair, { obj = GetGridObj(lair), resource = "Air", hours = num_hours, expiration = Max(num_hours, 1)*const.HourDuration }, "InsufficientResources", map)
					to_remove[lair] = nil
				end
				if air_consumption <= air_production or num_hours<=0 then
					RemoveObjectFromNotification(lair, notification)
				end	
			end

			for obj in pairs(to_remove) do
				RemoveObjectFromNotification(obj, notification)
				to_remove[obj] = nil
			end
		end
	end,
})
