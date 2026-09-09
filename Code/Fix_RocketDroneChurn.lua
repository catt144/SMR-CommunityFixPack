-- F50: A landed automatic rocket sends every drone that is on its way to it back
-- to Idle, once an hour, forever.
--
-- Defect: CargoTransporterNew:UpdateCargoResourceRequests
-- (Lua\CargoTransporterNew.lua:1238-1271 on game 1.0.7.396349; :1430-1463 on
-- 1.1.0.403908 — the bracket is unchanged) brackets its whole body with
--     if self.working then self:DisconnectFromCommandCenters() end
--     ... update request amounts ...
--     if self.working then self:ConnectToCommandCenters() end
-- Disconnecting makes every command center run DroneControl:OnRemoveBuilding
-- (DroneControl.lua:720-729 on 1.0.7; :784-793 on 1.1.0), which does
-- `drone:SetCommand("Idle")` for every drone whose goto_target resolves to the
-- rocket. For a landed automatic rocket this runs EVERY GAME HOUR: HourlyUpdate
-- (UniversalRocket.lua:1357-1370 on 1.0.7; :1557-1568 on 1.1.0) ->
-- CreateAutoCargoRequest -> SetCargoRequest -> UpdateCargoResourceRequests. Any
-- drone trip longer than one game hour can therefore never complete, no matter
-- what priority the player sets — and rockets start with zero drones of their own
-- and are excluded from shuttle transport, so distant rockets simply never get
-- loaded. This is the "drones ignore rocket cargo" report.
--
-- The disconnect is only meaningful when a NEW request object is created
-- (AddCargoDemandRequest, :1202-1207 on 1.0.7); the rest of the body just calls
-- SetAmount on requests that already exist, which command centers re-read in
-- place.
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\CargoTransporterNew.lua:1430-1463 (shipped Src, game 1.1.0.403908) that
-- decides up front whether any request is actually missing and only then does the
-- disconnect/reconnect dance. A transporter that somehow has no command centers
-- still gets its one-time connect. Changes marked -- FIX.
--
-- RE-COPIED 2026-09-08 on game 1.1.0.403908 (hotfix2 link 04, re-verification row
-- F-7, VANILLA_FIX_QA §0.5 + Reader A). Two-sided diff, the archived 1.0.7 tree
-- (C:\Dev\SMR-SrcArchive\1.0.7.396349\Src) against the live 1.1.0 tree: the
-- previous copy's non-FIX lines matched 1.0.7 exactly, and 1.1.0 changed ONE line
-- of this body —
--     local additional_amount = is_refuel_resource and not self.refuel_disabled and self:GetFuelResourceRequest()
-- `refuel_disabled` is the new "Accept fuel" infopanel toggle (UniversalRocket.lua:70
-- declares it, :3319 ToggleRefuel flips it, :774 clears it when a parked rocket
-- gets a trip). Our copy lacked the clause, so with the pack on, a rocket the
-- player had told to stop refuelling kept requesting fuel every hour. Carried now.
-- Deliberately NOT carried: nothing — the body is otherwise identical on both
-- branches. (The rocket-side override that now calls ForceInterruptIncomingDrones
-- before delegating here, UniversalRocket.lua:1937-1943, is outside this body and
-- untouched.)
--
-- ⛔ BRANCH GUARD (FIX_POLICY §2a, checklist 118): this body is written for 1.1.0
-- and the module must DECLINE on 1.0.7. There is no version field to read
-- (EF-077), so the Require below tests the SHAPE the new clause reads — the
-- `refuel_disabled` property and the ToggleRefuel method that sets it, both
-- declared on UniversalRocketBase on 1.1.0 and absent from 1.0.7 (0 hits for
-- either name in the archived UniversalRocket.lua). On 1.0.7 the check fails, the
-- module stands down, and that player keeps the frozen v5 pack's copy.
-- ⚠️ Why a shape `test` and not a stub `probe`: the target loops over
-- TransportableResourceIds, which PreProcessResources fills from the resource
-- presets on DataChanged (CommonLua\Libs\Resources\Resources.lua:404-449,
-- :492-500) and which is still EMPTY at ClassesBuilt on a cold boot, when this
-- apply runs. A probe would capture nothing there — UNKNOWN, which is a decline —
-- and switch the module off on every cold start. A decline on 1.0.7 is the CORRECT
-- outcome, not patch rot, so the check is a `test` (no update_suspect) whose reason
-- string names the branch.
--
-- ⛔ NOT tested. Nothing here has run in a game; the refuel toggle has never been
-- exercised on 1.1.0 with the pack on. A boot log line `RocketDroneChurn: applied`
-- proves the module loaded and the shape check passed, nothing more.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:UpdateCargoResourceRequests sha256=ff30071f4a4e5a1e96765f18ebd793aeba6bbfc2a404b5ea24ceace4481ad80c
--   (Lua/CargoTransporterNew.lua:1430-1463 at pin time)
-- DEFECT: if\s+self\.working\s+then\s+self:DisconnectFromCommandCenters\(\)
--   the UNCONDITIONAL disconnect that idles every inbound drone on a routine
--   amount refresh; a vanilla fix that makes it conditional on a request actually
--   being created (our own `needs_reconnect and self.working`) stops the match

SMRFixPack.Register("RocketDroneChurn", {
	title = "Landed rockets stop sending their delivery drones back to Idle every hour",
	apply = function()
		local err = SMRFixPack.Require("RocketDroneChurn", {
			{ class = "CargoTransporterNew", method = "UpdateCargoResourceRequests" },
			{ class = "CargoTransporterNew", method = "AddCargoDemandRequest",
			  reason = "CargoTransporterNew cargo request helpers not found (game update changed them?)" },
			{ class = "CargoTransporterNew", method = "AddCargoSupplyRequest",
			  reason = "CargoTransporterNew cargo request helpers not found (game update changed them?)" },
			-- FIX (F-7, 2026-09-08) — the branch guard (FIX_POLICY §2a). The body
			-- below reads self.refuel_disabled; this checks that the shipped rocket
			-- DECLARES that property and the toggle that sets it. Both are 1.1.0
			-- shapes (UniversalRocket.lua:70, :3319); neither exists on 1.0.7.
			{ test = function()
				local R = rawget(_G, "UniversalRocketBase")
				return type(R) == "table" and type(R.ToggleRefuel) == "function"
					and type(R.properties) == "table"
					and table.find(R.properties, "id", "refuel_disabled") ~= nil
			  end,
			  reason = "the shipped rocket has no refuel toggle (refuel_disabled / ToggleRefuel) — this copy of UpdateCargoResourceRequests is written for game 1.1.0 and stands down on an older body" },
		})
		if err then return err end
		local CT = CargoTransporterNew

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
				-- 1.1.0: `not self.refuel_disabled` honours the "Accept fuel" toggle (re-copied 2026-09-08)
				local additional_amount = is_refuel_resource and not self.refuel_disabled and self:GetFuelResourceRequest()
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
