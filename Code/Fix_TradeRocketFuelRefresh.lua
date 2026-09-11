-- F119: an Earth-sent trade rocket can wait forever after its fuel cost changes
-- while it is loading on Mars.
--
-- The Trade landing branch sets the cargo request once and enters CmdLoad
-- (Data/FlightPolicyDef.lua:561-568). GetCargoResourcesStatus compares the fuel
-- aboard with the LIVE GetFuelResourceRequest result
-- (Lua/CargoTransporterNew.lua:1288-1306), but the shipped modifier callback
-- refreshes requests only for player-controlled rockets. Trade rockets are not
-- player controlled (Lua/UniversalRocket.lua:1916-1920, :2631-2638). A fuel-cost
-- drop therefore leaves surplus fuel with no supply request; a rise leaves a
-- shortfall with no demand request. CmdLoad waits until the status is "ready"
-- (:500-502), so either mismatch can hold the rocket permanently.
--
-- Patch approach: chained post-wrapper on the declaring class. It calls the
-- shipped callback first, preserves its returns, then asks the game's own
-- UpdateCargoResourceRequests to re-size the requests. The object gate is the
-- exact shipped class used by both trade-rocket creation routes
-- (SA_Gameplay.lua:2851-2861; ClassDef-Effects.lua:215-226), so a foreign
-- subclass is untouched. CmdLoad is the narrow landed/loading state: the Trade
-- landing branch enters it after SetFlightData, and IsRocketLanded itself defines
-- CmdLoad as landed (:1574-1577), making separate arrival_loc and landed checks
-- redundant rather than safer.
--
-- Existing-save heal: once per LoadGame, inspect only exact
-- UniversalTradeRocket objects already in CmdLoad. A refresh occurs only when
-- the fuel entry's amount differs from requested cargo plus the LIVE trip fuel.
-- Healthy rockets are therefore no-ops. The shipped updater overwrites the
-- supply/demand target amounts with SetAmount (CargoTransporterNew.lua:1454-1458);
-- it never grants cargo and cannot double-grant anything.
--
-- FIX_POLICY §3a: layer 2 / synchronous-only. The wrapper performs no work after
-- a blocking call, owns no thread, and stores no function or new field on a
-- persisted object. The load heal is one synchronous scan. SAVE FOOTPRINT: none.
--
-- BRANCH GUARD (FIX_POLICY §2a): the behaviour probe calls the shipped modifier
-- callback on a closed stub and confirms the defect itself -- a non-player fuel
-- change does not refresh requests. The body is synchronous and side-effect-free:
-- it reads only the prop, calls the stub IsPlayerControlled, and (on the repaired
-- shape) may call the stub updater. Both outcomes touch only the two local stub
-- fields. The defect and wrapper seam are identical on 1.0.7, and this module
-- carries no branch-specific shipped body, so applying there is branch-neutral.
--
-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-11 against shipped game 1.1.0.403908.
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:OnModifiableValueChanged sha256=b2a420e92556f9bd1e625f468dfb7e87f9d57a9524e3dba79e7c67c1b29ef873
--   (Lua/UniversalRocket.lua:1916-1920 at pin time)
-- DEFECT: prop == "FuelResourceAmount" and self:IsPlayerControlled\(\) and self\.cargo
--   the player-only gate omits landed Trade rockets
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:UpdateCargoResourceRequests sha256=ff30071f4a4e5a1e96765f18ebd793aeba6bbfc2a404b5ea24ceace4481ad80c
--   (Lua/CargoTransporterNew.lua:1430-1463 at pin time)

local FIX_ID = "TradeRocketFuelRefresh"

local function is_shipped_trade_rocket_loading(rocket)
	return rocket.class == "UniversalTradeRocket"
		and rocket.command == "CmdLoad"
		and type(rocket.cargo) == "table"
end

local function fuel_request_is_stale(rocket)
	local entry = rocket.cargo[rocket.FuelResource]
	if type(entry) ~= "table" then return true end
	local requested = (entry.requested or 0) + rocket:GetFuelResourceRequest()
	return (entry.amount or 0) ~= requested
end

OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local each = rawget(_G, "AllMapsForEach")
	if type(each) ~= "function" then return end
	local refreshed = 0
	each(true, "UniversalTradeRocket", function(rocket)
		if is_shipped_trade_rocket_loading(rocket) and fuel_request_is_stale(rocket) then
			rocket:UpdateCargoResourceRequests()
			refreshed = refreshed + 1
		end
	end)
	if refreshed > 0 then
		SMRFixPack.Log("%s: refreshed %d landed trade rocket fuel request(s) after load", FIX_ID, refreshed)
	end
end)

SMRFixPack.Register(FIX_ID, {
	title = "Trade rockets update their fuel requests when the trip cost changes",
	apply = function()
		local R = UniversalRocketBase
		local orig = R and R.OnModifiableValueChanged
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "UniversalRocketBase", method = "OnModifiableValueChanged" },
			{ class = "UniversalRocketBase", method = "UpdateCargoResourceRequests" },
			{ class = "UniversalRocketBase", method = "GetFuelResourceRequest" },
			{ probe = function()
				local refreshes = 0
				local stub = {
					cargo = {},
					IsPlayerControlled = function() return false end,
					UpdateCargoResourceRequests = function()
						refreshes = refreshes + 1
					end,
				}
				orig(stub, "FuelResourceAmount", 50000, 30000)
				return refreshes == 0
			end,
			reason = "non-player fuel changes already refresh cargo requests (F119 repaired by the game?)" },
		})
		if err then return err end

		function R:OnModifiableValueChanged(...)
			local results = table.pack(orig(self, ...))
			local prop = select(1, ...)
			if prop == "FuelResourceAmount" and is_shipped_trade_rocket_loading(self) then
				self:UpdateCargoResourceRequests()
			end
			return table.unpack(results, 1, results.n)
		end
	end,
})
