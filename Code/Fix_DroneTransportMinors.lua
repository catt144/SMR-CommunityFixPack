-- F57: the drone/transport minors bundle. Three items were tracked; each was
-- screened against the shipped source. Two are fixed here; the third is
-- deliberately left alone because fixing it would undo F61.
--
---- (b) a passability change corrupts every drone's unreachables table -------
-- `OnMsg.OnPassabilityChanged` (Lua\Units\Drone.lua:851-864) drops the entries
-- belonging to the changed map by building a fresh table and swapping it in:
--     local unreachable = {}
--     for key, value in pairs(drone.unreachable_buildings) do ... end
--     drone.unreachable_buildings = unreachable
-- Two things are lost in that swap.
--
-- 1. **The weak-keys metatable.** Every other place this table is created uses
--    `setmetatable({version = g_DroneUnreachablesVersion}, weak_keys_meta)` —
--    `Drone:ApproachWrapper` (:826) and `Drone:ResetUnreachablesTable` (:875).
--    The replacement is a plain `{}`, so from the first passability change
--    onwards each drone holds a STRONG reference to every building it could not
--    reach. Salvaged and destroyed buildings are then kept alive by the drone
--    that once failed to reach them, and they keep coming back out of `pairs`
--    in `CleanUnreachables` (:890) and the recharger scan (:1281).
-- 2. **The count.** `unreachable_buildings_count` is never recomputed, so it
--    keeps the pre-change value while the table it describes has shrunk. That
--    number is not decoration: `Drone:ApproachWrapper` compares it against
--    `const.MaxUnreachablesInTable` and starts evicting the oldest entry when it
--    looks full (:827-838), and `DroneControl` only restarts its idle clock
--    while `self.unreachable_buildings_count <= 0` (:630). `CleanUnreachables`
--    then decrements the same stale number (:893) and can drive it negative.
--
-- This is NOT the nil-iteration kind of claim (the F10 lesson): the table can be
-- `false` here and this engine tolerates `pairs(false)` — no crash is asserted,
-- and none is fixed. What is fixed is the state left behind.
--
-- Patch approach: an additional `OnMsg.OnPassabilityChanged` handler
-- (FIX_POLICY §1.2 — OnMsg is additive; the shipped handler keeps running
-- untouched and ours runs after it, because mod code registers later). It
-- re-applies `weak_keys_meta` to whatever table each drone now has and
-- recomputes the count with `table.count`, which is exactly how
-- `ApproachWrapper` recomputes it after it changes the table (:841). Nothing
-- else is touched: the map filtering, the `version` key and the shipped expiry
-- all stay as they are.
--
---- (a) a non-"Fuel" rocket leaves a stale request restrictor ----------------
-- `DroneControl:UpdateRocketsInternal` (Lua\Buildings\DroneControl.lua:613-639)
-- clears exactly one key before rebuilding:
--     local r_t = self.restrictor_tables[rfRestrictorRocket]
--     r_t.Fuel = nil
-- The legacy `RocketBase` branch then writes `r_t["Fuel"]`, matching the clear.
-- The Relaunched `UniversalRocketBase` branch instead writes
-- `r_t[r.FuelResource]` (:634) — a per-class property. Whenever that is
-- anything other than the literal "Fuel", the entry it wrote is never cleared
-- again, and a request belonging to a rocket that has since left, launched or
-- been destroyed keeps restricting drone work forever.
--
-- **Latent as the game ships.** `FuelResource` is a building-template property
-- with no assignment anywhere in `ModTools\Src` (only `FuelResourceAmount` is
-- set per template), and the legacy branch hardcoding "Fuel" says what the
-- normal value is — so on shipped data the two keys coincide and nothing goes
-- wrong. It is fixed for the same reason F27 and F28 are: a mod or a future
-- rocket with its own fuel resource inherits a leak that is invisible until it
-- bites. Patch: full replacement of the 27-line method, byte-identical except
-- that it also clears the key it wrote last time, remembered on the
-- DroneControl in an absent-tolerant `SMRFixPack_` field (FIX_POLICY §3).
--
---- (c) screened, deliberately NOT fixed -------------------------------------
-- `recursive_enum_dome_workplaces` (Lua\Buildings\Dome.lua:670-680) computes
--     local can_work_here = work_or_train or (cdome == colonist.dome)
--     can_work_here = can_work_here or cdome:CanColonistsFromDifferentDomesWorkServiceTrainHere()
-- so for reason "work" or "training" the quarantine test short-circuits away,
-- although the function it skips is named for exactly those cases and is
-- commented `--quarantine` where the service path calls it (Dome.lua:2907).
-- The test is `self.accept_colonists and not self.supply_interrupted and
-- self.ui_working` (Dome.lua:2880-2882) — and `accept_colonists` is the property
-- **F61 exists to stop gating outbound work, shopping and training on**. Adding
-- the check here would re-impose, one level up, the block F61 removes; the two
-- fixes would fight over the same flag. The tracked mitigation also holds: the
-- enumeration only produces candidates, and `Workplace:IsSuitable` re-checks
-- before anyone is actually assigned, so nothing reaches the player. Recorded on
-- the BUGS entry; not fixed.

SMRFixPack.Register("DroneTransportMinors", {
	title = "A passability change no longer corrupts each drone's unreachable-buildings table",
	apply = function()
		local D = rawget(_G, "Drone")
		if type(D) ~= "table" or type(D.ApproachWrapper) ~= "function"
			or type(D.CleanUnreachables) ~= "function" then
			return "Drone.ApproachWrapper/CleanUnreachables not found (game update changed it?)"
		end
		local meta = rawget(_G, "weak_keys_meta")
		if type(meta) ~= "table" then
			return "weak_keys_meta not found (game update changed it?)"
		end
		if type(rawget(_G, "table")) ~= "table" or type(table.count) ~= "function" then
			return "table.count not found (game update changed it?)"
		end

		---- (b) ---------------------------------------------------------------
		-- Runs after the shipped handler has swapped in its plain table.
		local function repair_unreachables()
			local colony = rawget(_G, "UIColony")
			local labels = colony and colony.labels
			local repaired = 0
			for _, drone in ipairs((labels and labels.Drone) or empty_table) do
				local t = drone and drone.unreachable_buildings
				if type(t) == "table" then
					-- idempotent: re-applying the same metatable costs nothing
					setmetatable(t, meta)
					-- same recount ApproachWrapper does after it edits the table
					drone.unreachable_buildings_count = table.count(t)
					repaired = repaired + 1
				end
			end
			return repaired
		end

		SMRFixPack.DroneTransportMinors = { RepairUnreachables = repair_unreachables }

		OnMsg.OnPassabilityChanged = function()
			pcall(repair_unreachables)
		end

		---- (a) ---------------------------------------------------------------
		local DC = rawget(_G, "DroneControl")
		if type(DC) ~= "table" or type(DC.UpdateRocketsInternal) ~= "function" then
			-- (b) is installed and useful on its own; say so rather than
			-- deactivating the whole fix.
			SMRFixPack.DroneTransportMinors.rockets = "DroneControl.UpdateRocketsInternal not found"
			return
		end

		-- Source: Lua\Buildings\DroneControl.lua:613-639 (post-1.0.7 ModTools\Src).
		function DC:UpdateRocketsInternal()
			local r_t = self.restrictor_tables[rfRestrictorRocket]
			r_t.Fuel = nil
			-- FIX (F57a): the UniversalRocketBase branch below writes
			-- r_t[r.FuelResource]; only the literal "Fuel" was ever cleared, so
			-- any other fuel resource left its request behind forever.
			local previous = self.SMRFixPack_rocket_fuel_key
			if previous then
				r_t[previous] = nil
				self.SMRFixPack_rocket_fuel_key = nil
			end

			for i = 1, #self.serviced_rockets do
				local r = self.serviced_rockets[i]

				if IsKindOf(r, "RocketBase") then
					local rr = r.refuel_request
					if rr and rr:GetTargetAmount() > 0 then
						r_t["Fuel"] = rr
						break
					end
					local rr = r:GetExportRequest(r, "Fuel")
					if rr and rr:GetTargetAmount() > 0 then
						r_t["Fuel"] = rr
						break
					end
				elseif IsKindOf(r, "UniversalRocketBase") then
					local rr = table.get(r, "demand", r.FuelResource)
					if rr and rr:GetTargetAmount() > 0 then
						r_t[r.FuelResource] = rr
						if r.FuelResource ~= "Fuel" then                 -- FIX (F57a)
							self.SMRFixPack_rocket_fuel_key = r.FuelResource -- FIX (F57a)
						end                                              -- FIX (F57a)
						break
					end
				end
			end
		end
	end,
})
