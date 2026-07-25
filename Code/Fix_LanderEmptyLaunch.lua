-- F67: An automatic rocket/asteroid lander launches with nothing aboard and
-- ping-pongs between Mars and the asteroid.
--
-- Defect: UniversalRocketBase:IsCargoReady (Lua\UniversalRocket.lua:455-472) ends
-- with
--     return cargo_status == "ready"
-- and GetCargoResourcesStatus (CargoTransporterNew.lua:1124-1141) reports "ready"
-- when every cargo entry's amount equals its requested amount — which is trivially
-- true when the automatic request came out EMPTY (nothing currently above an
-- export threshold / below an import threshold; CreateAutoCargoRequest,
-- UniversalRocket.lua:1727-1766). "Wait for cargo" (CheckAutoDepart, :1768-1783)
-- only produces the "waiting_cargo" launch issue, which GetLaunchIssue
-- (:883-885) returns WITHOUT the blocker flag, so IsCargoReady's early
-- `launch_issue and blocker` guard doesn't stop it either. The rocket therefore
-- takes off empty the moment it is refuelled, burns ~70 fuel, lands, finds
-- nothing to do, and repeats. On asteroids the only brake is a 1-hour sleep
-- (:227-229); on Mars there is none.
--
-- Patch approach: chained wrapper. We only ever turn a "ready" verdict into
-- "not ready", and only while the rocket is (a) player controlled, (b) in normal
-- automatic mode, (c) still inside its "wait for cargo" window — i.e. exactly
-- when CheckAutoDepart() is true — and (d) carrying and requesting literally
-- nothing but fuel. Once g_Consts.AutoDepartTimerSols (1 sol, :1401) elapses,
-- CheckAutoDepart returns false and the vanilla forced departure happens as
-- designed, so the rocket can never wedge. Every hour spent waiting is another
-- CreateAutoCargoRequest tick that can find cargo to load.

SMRFixPack.Register("LanderEmptyLaunch", {
	title = "Automatic rockets and asteroid landers wait for cargo instead of launching empty",
	apply = function()
		local R = rawget(_G, "UniversalRocketBase")
		if type(R) ~= "table" or type(R.IsCargoReady) ~= "function" then
			return "UniversalRocketBase.IsCargoReady not found (game update changed it?)"
		end
		-- NB: mod code loads before the classes are built (autorun.lua:423 vs
		-- OnMsg.Autorun in classes.lua:980), so these tables are still the CLASS
		-- DEFS — only members declared by the class itself are visible here.
		-- IsAutoModeEnabled comes from the AutoMode mixin, so check it there.
		for _, name in ipairs{ "CheckAutoDepart", "IsSpecialAutomode", "IsPlayerControlled" } do
			if type(R[name]) ~= "function" then
				return "UniversalRocketBase." .. name .. " not found (game update changed it?)"
			end
		end
		local AutoMode = rawget(_G, "AutoMode")
		if type(AutoMode) ~= "table" or type(AutoMode.IsAutoModeEnabled) ~= "function" then
			return "AutoMode.IsAutoModeEnabled not found (game update changed it?)"
		end

		-- Would this rocket take off carrying nothing at all? Fuel does not count:
		-- it is the trip's cost, not its purpose.
		local function is_empty_flight(rocket)
			local fuel = rocket:HasMember("FuelResource") and rocket.FuelResource or false
			for id, entry in pairs(rocket.cargo or empty_table) do
				if id ~= fuel and ((entry.requested or 0) > 0 or (entry.amount or 0) > 0) then
					return false
				end
			end
			if #(rocket.departures or empty_table) > 0 then return false end
			if #(rocket.boarded or empty_table) > 0 then return false end
			return true
		end

		local orig = R.IsCargoReady
		function R:IsCargoReady(instant, ...)
			local ready = orig(self, instant, ...)
			if not ready or instant then
				return ready
			end
			-- FIX (F67): don't call an empty automatic flight "ready" while the
			-- rocket is still supposed to be waiting for cargo.
			if self:IsAutoModeEnabled() and not self:IsSpecialAutomode()
					and self:IsPlayerControlled() and self:CheckAutoDepart()
					and is_empty_flight(self) then
				return false
			end
			return ready
		end
	end,
})
