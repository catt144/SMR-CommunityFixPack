-- F55 (drone half): once a drone fails to approach a building, it writes that
-- building off forever.
--
-- Defect: Drone:ApproachWrapper (Lua\Units\Drone.lua:818-848) records a failed
-- approach as
--     unreachable_buildings[building] = GameTime() + max_int
-- with the comment "mark it so it is basically unreachable forever". But the game
-- also ships an expiry mechanism for exactly this table: Drone:CleanUnreachables
-- (:879-895) drops entries once `GameTime() - ts >= const.UnreachablesCleanupDeltaT`
-- (5 sols, :867). A timestamp max_int in the future makes that difference hugely
-- negative, so the entry never expires. The only escape is a passability change
-- bumping g_DroneUnreachablesVersion — and after any such change the drone simply
-- re-fails and re-marks it forever. A dome that was briefly unreachable (opened
-- roof, a blocked entrance, a construction site in the way) is dropped by that
-- drone permanently, which is the "late-game drones stop maintaining buildings
-- and cluster outside" report.
--
-- Patch approach: full replacement of the small method — a copy of
-- Lua\Units\Drone.lua:818-848 (shipped Src, game 1.0.7.396349) storing the actual failure
-- time, so the shipped 5-sol expiry does what it was written to do. Nothing else
-- changes: the table, its cap, the eviction of the oldest entry and the
-- version-based reset are all untouched.
--
-- Scope note: BUGS.md F55 also describes open-air domes losing their Dome_Entrance
-- attaches (and with them the only drone routes inside). That half is NOT patched
-- here — Dome_Entrance is an auto-attach of the dome entity, recreated by
-- AutoAttachObjects in Building:RebuildAttaches (Building.lua:2409-2429), not one
-- of the configurable attaches that Dome:CalcOpenAirSkin empties
-- (OpenAirBuilding.lua:216-237). Whether the *_Open entity carries the entrance
-- spot is engine data that Lua cannot inspect, so there is nothing to repair from
-- here. See the F55 entry for the finding.

SMRFixPack.Register("DroneUnreachableForever", {
	title = "Drones re-try buildings they once failed to reach instead of writing them off forever",
	apply = function()
		local D = rawget(_G, "Drone")
		if type(D) ~= "table" or type(D.ApproachWrapper) ~= "function" then
			return "Drone.ApproachWrapper not found (game update changed it?)"
		end
		if type(D.CleanUnreachables) ~= "function" or const.UnreachablesCleanupDeltaT == nil then
			return "the unreachables expiry mechanism is gone (game update changed it?)"
		end

		function D:ApproachWrapper(building, resource)
			if not IsValid(building) or not building:IsValidPos() then
				return
			end

			local result = self:ExitHolder(building) and building:DroneApproach(self, resource)
			if not result then
				local unreachable_buildings = self.unreachable_buildings or setmetatable({version = g_DroneUnreachablesVersion}, weak_keys_meta)
				if self.unreachable_buildings_count >= const.MaxUnreachablesInTable then
					--kick oldest
					local min_time = max_int
					local min_id = false
					for id, ts in pairs(unreachable_buildings) do
						if not min_id or ts < min_time then
							min_id = id
							min_time = ts
						end
					end
					unreachable_buildings[min_id] = nil
				end

				-- FIX (F55): shipped value was GameTime() + max_int, which put the entry
				-- permanently beyond CleanUnreachables' 5-sol expiry test.
				unreachable_buildings[building] = GameTime()
				self.unreachable_buildings_count = table.count(unreachable_buildings)
				self.unreachable_buildings = unreachable_buildings
				if IsKindOf(building, "ConstructionSite") and self.command_center then
					self.command_center:UpdateConstructions()
				end
			end

			return IsValid(building) and result
		end
	end,
})
