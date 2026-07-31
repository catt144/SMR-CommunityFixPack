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
-- F71 (same function, folded in here rather than replacing it twice): the loop
-- below hands the weight budget out in the order `sorted_pairs` yields, i.e.
-- ALPHABETICALLY — Concrete, Electronics, Food, Fuel, MachineParts, Metals,
-- Polymers, PreciousMetals, PreciousMinerals, WasteRock. `cargo_capacity` is
-- decremented as it goes, so bulk that happens to sort early eats the 80,000kg
-- hold before the valuables are ever considered, and the 1-sol forced departure
-- (AutoDepartTimerSols, :1773-1775) ships whatever got in first. WasteRock is a
-- legal auto-export from an asteroid (FlightPolicyDef.lua:393), so a lander can
-- fill up on tailings and leave the exotic minerals on the ground.
--
-- The game already states the intended order, in every flight policy:
--     GetAutoModeAllowedResources -> { "PreciousMinerals", "Electronics",
--         "PreciousMetals", "MachineParts", "Polymers", "Food", "Fuel",
--         "Metals", "Concrete", "WasteRock" }
-- (FlightPolicyDef.lua:133-141, :232-240, :390-396 — value-descending, WasteRock
-- last, identical in all three policies). That is the same function
-- UniversalRocketBase:GetAllowedResources already calls for this rocket
-- (:649-658); it only throws the order away because it wants a set
-- (table.invert). So the fix is to walk the thresholds in the policy's own
-- order, and fall back to the shipped alphabetical order for anything the
-- policy does not list (including "return -- all", where it lists nothing).
--
-- Patch approach: the defect is mid-function and unhookable, so this is a full
-- replacement of the method — a copy of Lua\UniversalRocket.lua:1727-1766
-- (shipped Src, game 1.0.7.396349) with two changes, all marked -- FIX:
--   1. (F68) never let the final request for an exported resource sit below
--      what is already aboard — that is the flip that turns a loaded rocket
--      into an unloading one;
--   2. (F71) iterate the thresholds in flight-policy order instead of
--      alphabetically.
--
-- REPAIRED 2026-07-28 (PT-17 capacity-edge finding, F68 entry): v1 of this fix
-- ALSO added the aboard amount into `amount_on_target_loc` before the threshold
-- compare. Live TAP2 forensics proved `GetTotalCargoAvailable` already counts
-- the landed rocket's own hold (the observed request tracked
-- ground + 2×aboard − threshold EXACTLY, and the asteroid drained to
-- threshold − 60), so that addition double-counted every unit aboard and the
-- request ratcheted monotonically to the hold cap — over-exporting far below
-- the player's GET-WHEN-ABOVE threshold. Deleted: on the live path the shipped
-- `available − threshold` is already aboard + ground surplus (equilibrium lands
-- ground exactly at the threshold), and the change-1 floor below still
-- guarantees no unload flip on any path where the hold is not counted.
-- The shipped `assert(res_type == "Resource")` on :1738 is dropped: assert does
-- not unwind mod code (it prints and execution continues), so keeping it would
-- only add log noise on a resource the policy allows but we did not expect.
--
-- Change 3 applies to the import direction as well as the export one — it is the
-- same loop and the same shared budget, and importing Concrete ahead of
-- Electronics wastes the hold exactly the same way.

SMRFixPack.Register("LanderCargoRatchet", {
	title = "Automatic rockets stop unloading the cargo they just loaded, and fill up with the valuable resources first",
	apply = function()
		-- NB: Require's class/method checks run against the CLASS DEFS (mod code
		-- loads before the classes are built) — only members the class declares
		-- itself are visible. The cargo plumbing lives on the CargoTransporterNew
		-- parent, so it is checked there.
		local err = SMRFixPack.Require("LanderCargoRatchet", {
			{ class = "UniversalRocketBase", method = "CreateAutoCargoRequest" },
			{ class = "UniversalRocketBase", method = "ResolveAutoModeTarget" },
			{ class = "UniversalRocketBase", method = "IsOnAutoModeTargetLocation" },
			{ class = "UniversalRocketBase", method = "IsSpecialAutomode" },
			{ class = "CargoTransporterNew", method = "GetCargoWeightCapacity",
			  reason = "CargoTransporterNew cargo-request methods not found (game update changed them?)" },
			{ class = "CargoTransporterNew", method = "SetCargoRequest",
			  reason = "CargoTransporterNew cargo-request methods not found (game update changed them?)" },
			{ global = "GetCargoType" },
			{ global = "GetTotalCargoAvailable" },
			{ global = "GetResupplyItem" },
			{ global = "GetResupplyItemWeight" },
		})
		if err then return err end
		local R = UniversalRocketBase

		-- FIX (F71): the order the weight budget is handed out in. The flight
		-- policy for this rocket's destination lists the resources it allows,
		-- best first; anything it does not mention keeps the shipped
		-- alphabetical order behind them, so the SET of resources considered is
		-- unchanged and only the sequence moves. Called defensively — the policy
		-- function reads back from the rocket (GetDepartureLocType), so a rocket
		-- in an unexpected state must degrade to the shipped order, not error.
		local function priority_order(rocket, thresholds)
			local order = empty_table
			local get_policy = rawget(_G, "GetFlightPolicy")
			if type(get_policy) == "function" then
				local ok, policy = pcall(get_policy, rocket)
				local fn = ok and type(policy) == "table" and policy.GetAutoModeAllowedResources or nil
				if type(fn) == "function" then
					local listed
					ok, listed = pcall(fn, policy, rocket)
					if ok and type(listed) == "table" then order = listed end
				end
			end
			local out, seen = {}, {}
			for _, res in ipairs(order) do
				if thresholds[res] ~= nil and not seen[res] then
					seen[res] = true
					out[#out + 1] = res
				end
			end
			for res in sorted_pairs(thresholds) do
				if not seen[res] then
					seen[res] = true
					out[#out + 1] = res
				end
			end
			return out
		end

		function R:CreateAutoCargoRequest()
			if self:IsSpecialAutomode() or not self:IsAutoModeEnabled() or not self.arrival_loc or not self.departure_loc then return end

			local automode_target_loc = self:ResolveAutoModeTarget()
			local is_on_automode_target_loc = self:IsOnAutoModeTargetLocation()
			local current_loc = self.departure_loc

			local request = {}
			local cargo_capacity = self:GetCargoWeightCapacity()
			-- FIX (F71): was `sorted_pairs(...)` — alphabetical, so bulk that sorts
			-- early (Concrete, Metals) spent the hold before PreciousMinerals and
			-- PreciousMetals were ever reached. `or empty_table`: both threshold
			-- tables default to false (:178-179), which sorted_pairs tolerated.
			local thresholds = (is_on_automode_target_loc and self.export_above or self.import_below) or empty_table
			for _, res in ipairs(priority_order(self, thresholds)) do
				local threshold = thresholds[res]
				local res_type = GetCargoType(res)
				local target_map = automode_target_loc and automode_target_loc.map
				target_map = not IsKindOf(target_map, "MapDescriptor") and target_map or (target_map and target_map.map)
				local target_city = target_map and target_map.City
				local amount_on_target_loc = target_city and GetTotalCargoAvailable(target_city, "Resource", res) or 0
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
