-- F27: modifiers that change a battery's or tank's charge/discharge RATE are
-- accepted, displayed, and then never reach the grid element that uses them.
--
-- Defect: all three storage classes react to the rate properties changing and
-- then copy everything EXCEPT the rates.
--     ElectricityStorage:OnModifiableValueChanged   (Lua\ElectricityStorage.lua:47-63)
--     WaterStorage:OnModifiableValueChanged          (Lua\LifeSupportStorage.lua:25-42)
--     AirStorage:OnModifiableValueChanged            (Lua\LifeSupportStorage.lua:131-148)
-- Each fires for `max_*_charge`, `max_*_discharge`, `*_conversion_efficiency`
-- and `*_capacity`, and each then writes back only
--     element.charge_efficiency = self.<conversion_efficiency>
--     element.storage_capacity  = self.<capacity>
-- before calling `element:UpdateStorage()`. The rates live on the element as
-- `max_charge` / `max_discharge` (`SupplyGrid.lua:34-35`), are set once at
-- creation (`NewSupplyGridStorage`, `:64-76`), and are what the grid actually
-- reads every tick:
--     local charge    = bld.working and Min(self.max_charge, self.storage_capacity - current_storage) or 0
--     local discharge = bld.working and self:CanDischarge() and Min(self.max_discharge, current_storage) or 0
-- (`SupplyGrid.lua:167-168`). So a modifier on a rate changes the building's
-- property and the UI, and changes nothing about how fast the thing charges.
--
-- Latent in the base game — no shipped tech or law modifies these four
-- properties — but they are declared modifiable, which makes them part of the
-- documented modding surface. Fixed for that reason (and because a game or DLC
-- update that adds such a modifier would ship broken).
--
-- Patch approach: post-wrappers (FIX_POLICY §1.4) on the three
-- `OnModifiableValueChanged` methods. The shipped body runs first and does all
-- its own work; the wrapper then copies the two missing fields and re-runs
-- `UpdateStorage()` so the grid picks the new rates up in the same pass the
-- shipped code intended. Chaining rather than replacing keeps any other mod's
-- handler intact, and the wrapper does nothing at all unless the property that
-- changed is one of the two rates.

SMRFixPack.Register("StorageRateModifiers", {
	title = "Charge and discharge rate modifiers on batteries and tanks take effect",
	apply = function()
		-- class, element field, charge property, discharge property
		local TARGETS = {
			{ "ElectricityStorage", "electricity", "max_electricity_charge", "max_electricity_discharge" },
			{ "WaterStorage",       "water",       "max_water_charge",       "max_water_discharge" },
			{ "AirStorage",         "air",         "max_air_charge",         "max_air_discharge" },
		}

		local patched = 0
		for _, target in ipairs(TARGETS) do
			local class_name, element_field, charge_prop, discharge_prop = table.unpack(target)
			local class = rawget(_G, class_name)
			-- OnModifiableValueChanged must be declared on this very class — mod
			-- code loads before the classes are flattened, so an inherited one
			-- would read as nil here and is not ours to wrap anyway.
			if type(class) == "table" and type(rawget(class, "OnModifiableValueChanged")) == "function" then
				local orig = class.OnModifiableValueChanged
				class.OnModifiableValueChanged = function(self, prop, ...)
					local res = orig(self, prop, ...)
					-- FIX (F27): the shipped body copies capacity and efficiency to
					-- the grid element but never the rates it also listens for.
					if prop == charge_prop or prop == discharge_prop then
						local element = self[element_field]
						if type(element) == "table" then
							element.max_charge = self[charge_prop]
							element.max_discharge = self[discharge_prop]
							if type(element.UpdateStorage) == "function" then
								element:UpdateStorage()
							end
						end
					end
					return res
				end
				patched = patched + 1
			end
		end

		if patched == 0 then
			return "no storage class declares OnModifiableValueChanged (game update changed it?)"
		end
		SMRFixPack.StorageRateModifiers = { patched = patched }
	end,
})
