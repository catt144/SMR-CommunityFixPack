-- D01 — OPTIONAL module, OFF BY DEFAULT. Not a bug fix.
--
-- Enable it by setting, before this mod loads (console on the main menu, or a
-- tiny mod that loads first):
--     SMRFixPack_Optional = { ClassicRockets = true }
-- `SMRFixPack.ListFixes()` reports it as inactive with the reason until you do.
--
-- Why it exists: the remaster deliberately changed rocket logistics, and the
-- BUGS.md D01 entry records the verdict that this is a redesign and NOT a defect
-- — the legacy always-on behaviour survives only in the dead legacy class
-- (RocketBase:CreateExportRequests, Lua\Buildings\RocketBase.lua:1729-1736, whose
-- `allow_export` / `export_requests` / `max_export_storage` fields are nilled on
-- migration, RocketCompatibility.lua:58,95-99). Players who preferred the old
-- behaviour get it here, opt-in, so the pack itself stays a pure bug-fix mod
-- (FIX_POLICY §4). The file is named Opt_* rather than Fix_* for exactly that
-- reason.
--
-- WHAT THIS SHIPS: automatic refuelling of a landed rocket.
--
-- UniversalRocketBase:GetFuelResourceRequest (Lua\UniversalRocket.lua:1639-1650)
-- returns 0 whenever there is no `arrival_loc`, and manual landing clears
-- `arrival_loc` (CmdLand, :414). So a rocket sitting on its pad with no
-- destination picked asks for no fuel at all, and only starts being refuelled
-- once you have chosen where it is going — which is the "my rocket never has
-- fuel when I need it" complaint. That request feeds the drone demand directly:
-- CargoTransporterNew:UpdateCargoResourceRequests takes
-- `additional_amount = is_refuel_resource and self:GetFuelResourceRequest()`
-- straight into the demand (CargoTransporterNew.lua:1249-1265), so raising it is
-- the whole mechanism.
--
-- With this module on, a player-controlled rocket parked at the colony with no
-- destination keeps its launch ration requested, and drones top it up while it
-- waits. Neither notification branch in UpdateCargoResourceRequests fires in that
-- state (both require `arrival_loc`, :1308-1314), so there is no "refuelled" spam
-- and no entry in g_LandedRocketsInNeedOfFuel.
--
-- Chained wrapper, and only when the shipped answer is 0 — every case the game
-- already answers, including F69's asteroid-lander reserve, falls through
-- untouched.
--
-- WHAT THIS DOES NOT SHIP: the standing Rare Metals export request. That half of
-- the D01 sketch is a gameplay system, not a hook: the modern cargo request is
-- driven by SetCargoRequest / the payload dialog / Automated Mode's
-- `export_above` thresholds, and injecting a permanent demand into it touches the
-- same machinery as F50, F68, F70 and F71. It is deliberately left for a design
-- decision plus an in-game test rather than improvised here — see the D01 entry
-- in docs/BUGS.md.

SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

SMRFixPack.Register("ClassicRockets", {
	title = "OPTIONAL: rockets refuel while parked, without a destination selected",
	apply = function()
		if not SMRFixPack_Optional.ClassicRockets then
			return "opt-in module, off by default — set SMRFixPack_Optional = { ClassicRockets = true } before this mod loads"
		end

		local R = rawget(_G, "UniversalRocketBase")
		if type(R) ~= "table" or type(R.GetFuelResourceRequest) ~= "function" then
			return "UniversalRocketBase.GetFuelResourceRequest not found (game update changed it?)"
		end
		-- Both declared on UniversalRocketBase itself (:826 and :2140), so this
		-- lookup is valid even though mod code loads before the classes are
		-- flattened and only self-declared members are visible.
		for _, name in ipairs{ "GetDepartureLocType", "IsPlayerControlled" } do
			if type(R[name]) ~= "function" then
				return "UniversalRocketBase." .. name .. " not found (game update changed it?)"
			end
		end
		local CT = rawget(_G, "CargoTransporterNew")
		if type(CT) ~= "table" or type(CT.UpdateCargoResourceRequests) ~= "function" then
			return "CargoTransporterNew.UpdateCargoResourceRequests not found (game update changed it?)"
		end

		local orig = R.GetFuelResourceRequest
		function R:GetFuelResourceRequest(...)
			local amount, reserve = orig(self, ...)
			-- D01: parked at the colony with nowhere to go. The shipped answer is 0
			-- only because no destination is selected; keep the launch ration
			-- requested so drones fuel it while it waits.
			if (amount or 0) <= 0 and not self.arrival_loc
					and self:IsPlayerControlled()
					and self:GetDepartureLocType() == "our_colony" then
				return Max(0, self.FuelResourceAmount or 0), reserve
			end
			return amount, reserve
		end
	end,
})
