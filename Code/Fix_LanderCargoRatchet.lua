-- F68: An automatic rocket/lander loads cargo and then unloads its own cargo
-- again, an hour later, over and over.
--
-- Defect: UniversalRocketBase:CreateAutoCargoRequest (Lua\UniversalRocket.lua:
-- 1727-1766) is re-run every hour while landed (HourlyUpdate, :1357-1370) and
-- recomputes the whole request from scratch:
--     local amount_on_target_loc = GetTotalCargoAvailable(target_city, "Resource", res)
--     to_transfer = amount_on_target_loc - threshold        -- export direction
-- but resources already loaded into the rocket are no longer "available" in the
-- city. So every hour the request shrinks by exactly what the drones just loaded.
-- Once `requested` drops below what is aboard, GetCargoResourcesStatus
-- (CargoTransporterNew.lua:1124-1141) reports "unloading" and the drones carry
-- the cargo straight back out. In the worst phase the request collapses to {}
-- with a full hold, everything is unloaded, and the rocket departs empty (F67).
-- This is the "loads exotics, dumps them back, leaves with junk" report.
--
-- Only the export direction ratchets: when the rocket is NOT on the automode
-- target location it compares against stock at the REMOTE location, which
-- loading here does not change.
--
-- Patch approach: the defect is mid-function and unhookable, so this is a full
-- replacement of the method — a copy of Lua\UniversalRocket.lua:1727-1766
-- (shipped Src, 2026-07) with two changes, both marked -- FIX and both confined
-- to the export direction:
--   1. count the rocket's own load as still being "here" before comparing to the
--      threshold, so the requested amount stays put instead of ratcheting down;
--   2. belt and braces, never let the final request for an exported resource sit
--      below what is already aboard (the capacity split can still starve a
--      resource that came earlier in the loop).

SMRFixPack.Register("LanderCargoRatchet", {
	title = "Automatic rockets stop unloading the cargo they just loaded",
	apply = function()
		local R = rawget(_G, "UniversalRocketBase")
		if type(R) ~= "table" or type(R.CreateAutoCargoRequest) ~= "function" then
			return "UniversalRocketBase.CreateAutoCargoRequest not found (game update changed it?)"
		end
		-- NB: mod code loads before the classes are built (autorun.lua:423 vs
		-- OnMsg.Autorun in classes.lua:980), so these tables are still the CLASS
		-- DEFS — only members the class declares itself are visible. The cargo
		-- plumbing lives on the CargoTransporterNew parent.
		for _, name in ipairs{ "ResolveAutoModeTarget", "IsOnAutoModeTargetLocation", "IsSpecialAutomode" } do
			if type(R[name]) ~= "function" then
				return "UniversalRocketBase." .. name .. " not found (game update changed it?)"
			end
		end
		local CT = rawget(_G, "CargoTransporterNew")
		if type(CT) ~= "table" or type(CT.GetCargoWeightCapacity) ~= "function"
				or type(CT.SetCargoRequest) ~= "function" then
			return "CargoTransporterNew cargo-request methods not found (game update changed them?)"
		end
		for _, name in ipairs{ "GetCargoType", "GetTotalCargoAvailable", "GetResupplyItem", "GetResupplyItemWeight" } do
			if type(rawget(_G, name)) ~= "function" then
				return name .. " not found (game update changed it?)"
			end
		end

		function R:CreateAutoCargoRequest()
			if self:IsSpecialAutomode() or not self:IsAutoModeEnabled() or not self.arrival_loc or not self.departure_loc then return end

			local automode_target_loc = self:ResolveAutoModeTarget()
			local is_on_automode_target_loc = self:IsOnAutoModeTargetLocation()
			local current_loc = self.departure_loc

			local request = {}
			local cargo_capacity = self:GetCargoWeightCapacity()
			for res, threshold in sorted_pairs(is_on_automode_target_loc and self.export_above or self.import_below) do
				local res_type = GetCargoType(res)
				assert(res_type == "Resource")
				local target_map = automode_target_loc and automode_target_loc.map
				target_map = not IsKindOf(target_map, "MapDescriptor") and target_map or (target_map and target_map.map)
				local target_city = target_map and target_map.City
				local amount_on_target_loc = target_city and GetTotalCargoAvailable(target_city, "Resource", res) or 0
				if is_on_automode_target_loc then
					-- FIX (F68): what we already loaded here is still "here" as far as
					-- this decision goes; without this the request ratchets down by
					-- exactly the amount loaded each hour and flips to "unloading".
					local aboard = table.get(self, "cargo", res, "amount") or 0
					amount_on_target_loc = amount_on_target_loc + aboard / const.ResourceScale
				end
				local to_transfer
				if is_on_automode_target_loc then
					to_transfer = amount_on_target_loc - threshold
				else
					to_transfer = threshold - amount_on_target_loc
				end
				if to_transfer > 0 then
					local meta = GetResupplyItem(res)
					local pack_weight = meta and GetResupplyItemWeight(meta) or 0
					if pack_weight ~= 0 then
						local transfer_packs = Min(to_transfer / meta.pack, cargo_capacity / pack_weight)
						request[res] = { type = res_type, class = res, amount = transfer_packs * meta.pack * const.ResourceScale }
						cargo_capacity = cargo_capacity - transfer_packs * pack_weight
					end
				end
			end

			-- FIX (F68): never ask for less of an exported resource than is already
			-- in the hold — that is what turns a loaded rocket into an unloading one.
			if is_on_automode_target_loc then
				for res in sorted_pairs(self.export_above or empty_table) do
					local aboard = table.get(self, "cargo", res, "amount") or 0
					if aboard > 0 then
						local entry = request[res]
						if not entry then
							request[res] = { type = GetCargoType(res), class = res, amount = aboard }
						elseif entry.amount < aboard then
							entry.amount = aboard
						end
					end
				end
			end

			self:SetCargoRequest(request)

			if self:GetArrivalLocType() == "earth" and (UIColony.funds:GetFunding() + self:GetEarthExportResPossibleReward()) <= g_Consts.FundingImportThreshold then
				self:CreateStopAutomodeNotification("no flights")
				self:CancelFlight()
			end
		end
	end,
})
