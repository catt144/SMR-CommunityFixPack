-- F12: The "Insufficient Resources" warning can never fire for Food or for
-- maintenance resources.
--
-- Defect: ResourceTracking:GatheredResourcesOnHourlyUpdate
-- (Lua\ResourceTracking.lua:211-316) computes the remaining supply window as
--     local num_hours = v > 0 and transportable_resources[k]*const.HoursPerDay / v*const.HoursPerDay or 0
-- The missing parentheses make that `((supply * 24) / v) * 24`, and this engine's
-- `/` truncates — so the result is either 0 or at least 24. The guard right below
-- needs `num_hours > 0 and num_hours < const.MinDaysMaintenanceSupplyBeforeNotification`
-- (3), which those two ranges can never satisfy. The Food branch (:227-234) repeats
-- the same expression against MinDaysFoodSupplyBeforeNotification. Both warnings are
-- therefore dead: the colony runs out of Food, Machine Parts or Electronics with no
-- notice at all. The grid branches further down (:246-303) use a different, correct
-- formula, which is what makes the Power/Water/Air warnings work.
--
-- The intended value is hours of supply: the notification renders `hours` and sets
-- `expiration = num_hours * const.HourDuration`, and the constants are "MinDays…",
-- i.e. days that need converting to hours before the comparison.
--
-- Patch approach: chained post-wrapper rather than a 100-line replacement. The
-- shipped add branch is unreachable, so on every tick the shipped code takes the
-- else branch and REMOVES any Food/maintenance entry; we then re-add exactly the
-- ones that are genuinely low, computed with MulDivRound(supply, HoursPerDay,
-- consumed_per_day) against MinDays* * HoursPerDay. The grid half of the function,
-- its notification cleanup and any other mod's hooks are untouched.

SMRFixPack.Register("LowStorageWarning", {
	title = 'The "Insufficient Resources" warning works again for Food and maintenance resources',
	apply = function()
		local RT = rawget(_G, "ResourceTracking")
		if type(RT) ~= "table" or type(RT.GatheredResourcesOnHourlyUpdate) ~= "function" then
			return "ResourceTracking.GatheredResourcesOnHourlyUpdate not found (game update changed it?)"
		end
		for _, name in ipairs{ "GatherTransportableResources", "GetCityResourceOverview",
				"AddObjectToNotification", "MulDivRound" } do
			if type(rawget(_G, name)) ~= "function" then
				return name .. " not found (game update changed it?)"
			end
		end
		if const.MinDaysMaintenanceSupplyBeforeNotification == nil
				or const.MinDaysFoodSupplyBeforeNotification == nil then
			return "supply-warning constants not found (game update changed them?)"
		end

		local orig = RT.GatheredResourcesOnHourlyUpdate
		function RT:GatheredResourcesOnHourlyUpdate(map, ...)
			local result = orig(self, map, ...)

			-- FIX (F12): the shipped arithmetic above can only ever produce 0 or >= 24,
			-- so its warning branch is dead and it has just cleared these entries.
			-- Recompute the supply window properly and raise the ones that are due.
			local hours_per_day = const.HoursPerDay

			local transportable_resources = {}
			GatherTransportableResources(transportable_resources, self)
			local maintenance_limit = const.MinDaysMaintenanceSupplyBeforeNotification * hours_per_day
			for k, v in pairs(self.maintenance_resources_consumed_yesterday or empty_table) do
				local supply = transportable_resources[k] or 0
				if v > 0 and supply > 0 then
					local num_hours = MulDivRound(supply, hours_per_day, v)
					if num_hours > 0 and num_hours < maintenance_limit then
						AddObjectToNotification(k, { resource = k, hours = num_hours, expiration = num_hours * const.HourDuration }, "InsufficientResources", map)
					end
				end
			end

			-- food
			local resource_overview = GetCityResourceOverview(self)
			local food_consumed = resource_overview:GetConsumedByConsumptionYesterday("Food")
			local food_total = resource_overview:GetAvailable("Food")
			if food_total > 0 and food_consumed > 0 then
				local num_hours = MulDivRound(food_total, hours_per_day, food_consumed)
				if num_hours > 0 and num_hours < const.MinDaysFoodSupplyBeforeNotification * hours_per_day then
					AddObjectToNotification("Food", { resource = "Food", hours = num_hours, expiration = num_hours * const.HourDuration }, "InsufficientResources", map)
				end
			end

			return result
		end
	end,
})
