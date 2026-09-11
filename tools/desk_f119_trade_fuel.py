#!/usr/bin/env python3
"""F119 trade-rocket fuel-request control over shipped Lua bodies.

The relevant 1.1.0 functions are extracted with ``tools.luafn`` and loaded at
their real file names and line offsets. The fix module is loaded whole through
the same Register/Require seam used in game. Only engine containers, requests,
and message/map iteration are stubbed.

This reproduces the stuck request/status mismatch and proves the wrapper and
load-time heal repair that desk model. It does not claim an in-game trade rocket
was produced or that a real save was healed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_TradeRocketFuelRefresh.lua")

PRELUDE = db.ENGINE_SHIMS + r'''
-- table.copy is the engine helper used by CargoTransporterNew.lua:1436.
table.copy = function(t)
	local copy = {}
	for k, v in pairs(t) do copy[k] = v end
	return copy
end
UniversalRocketBase = {}
CargoTransporterNew = {}
OnMsg = {}

TransportableResourceIds = { "Fuel" }
const = { rfRestrictorRocket = 8 }
g_Consts = { CargoRequestDroneAmount = 3 }
g_RocketTypes = {
	Player = "SupplyRocket", LanderRocket = "LanderRocket",
	Expedition = "ExpeditionRocket", SupplyPod = "SupplyPod",
	PassengerPod = "PassengerPod", Trade = "TradeRocket",
}
g_LandedRocketsInNeedOfFuel = {}

function CallFlightPolicyFunc() return nil end
function Msg() end

ROCKETS = {}
function AllMapsForEach(_, class, fn)
	for _, rocket in ipairs(ROCKETS) do
		if class == "UniversalTradeRocket" and rocket.class == class then
			fn(rocket)
		end
	end
end

SMRFixPack = { fixes = {}, logs = {} }
APPLY_MODULE = true
function SMRFixPack.Register(id, def)
	SMRFixPack.fixes[id] = { status = APPLY_MODULE and "active" or "inactive" }
	if APPLY_MODULE then
		local err = def.apply()
		if err then SMRFixPack.fixes[id].status = "inactive" end
		SMRFixPack.apply_error = err
	end
end
function SMRFixPack.Require(_, specs)
	for _, spec in ipairs(specs) do
		if spec.probe then
			local ok, answer = pcall(spec.probe)
			if not ok or answer ~= true then return spec.reason or "declined" end
		elseif spec.class and spec.method then
			local class = _G[spec.class]
			if type(class) ~= "table" or type(class[spec.method]) ~= "function" then
				return spec.class .. "." .. spec.method .. " absent"
			end
		end
	end
end
function SMRFixPack.WhenActive(id, fn)
	return function(...)
		local fix = SMRFixPack.fixes[id]
		if fix and fix.status == "active" then return fn(...) end
	end
end
function SMRFixPack.Log(fmt, ...)
	SMRFixPack.logs[#SMRFixPack.logs + 1] = string.format(fmt, ...)
end
'''

ROCKET_FACTORY = r'''
function request()
	local r = { amount = 0 }
	function r:SetAmount(amount) self.amount = amount end
	return r
end

function rocket(class, fuel_amount, amount)
	local r = setmetatable({
		class = class,
		RocketType = class == "UniversalTradeRocket" and g_RocketTypes.Trade or g_RocketTypes.Player,
		command = "CmdLoad",
		FuelResource = "Fuel",
		FuelResourceAmount = fuel_amount,
		arrival_loc = {},
		cargo = { Fuel = { class = "Fuel", requested = 0, amount = amount } },
		demand = { Fuel = request() },
		supply = { Fuel = request() },
		storable_resources = {},
		resource = {},
		working = false,
		refuel_disabled = false,
	}, { __index = UniversalRocketBase })
	function r:HasMember(name) return name == "FuelResource" end
	function r:IsAutoModeEnabled() return true end
	function r:ForceInterruptIncomingDrones() end
	function r:HasEnoughFuelToLaunch()
		return self.cargo.Fuel.amount >= self:GetFuelResourceRequest()
	end
	function r:UpdateReadyNoDestinationNotification() end
	function r:AddCargoDemandRequest() error("unexpected missing demand request") end
	function r:AddCargoSupplyRequest() error("unexpected missing supply request") end
	function r:UpdateCargoResourceRequests()
		self.update_calls = (self.update_calls or 0) + 1
		return UniversalRocketBase.UpdateCargoResourceRequests(self)
	end
	r:UpdateCargoResourceRequests() -- the landing-time sizing pass
	r.update_calls = 0
	return r
end

function change_fuel(r, amount)
	local old = r.FuelResourceAmount
	r.FuelResourceAmount = amount
	r:OnModifiableValueChanged("FuelResourceAmount", old, amount)
end
'''


def load_body(rt, rel, pattern):
    text, lo, hi = db.body(rel, pattern)
    db.load_at(rt, text, "=" + rel, lo)
    return lo, hi


def make_runtime(apply):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    spans = []
    spans.append(("Lua/CargoTransporterNew.lua",) + load_body(
        rt, "Lua/CargoTransporterNew.lua", r"^function CargoTransporterNew:GetCargoResourcesStatus"))
    spans.append(("Lua/CargoTransporterNew.lua",) + load_body(
        rt, "Lua/CargoTransporterNew.lua", r"^function CargoTransporterNew:UpdateCargoResourceRequests"))
    for pattern in (
        r"^function UniversalRocketBase:GetFuelResourceRequest",
        r"^function UniversalRocketBase:IsPlayerControlled",
        r"^function UniversalRocketBase:OnModifiableValueChanged",
        r"^function UniversalRocketBase:UpdateCargoResourceRequests",
    ):
        spans.append(("Lua/UniversalRocket.lua",) + load_body(
            rt, "Lua/UniversalRocket.lua", pattern))
    # The game class builder copies this mixin method onto UniversalRocketBase.
    # The desk loads declarations directly, so mirror that one inheritance edge.
    rt.execute("UniversalRocketBase.GetCargoResourcesStatus = CargoTransporterNew.GetCargoResourcesStatus")
    rt.globals().APPLY_MODULE = apply
    db.load_at(rt, db.read(MODULE), "=Code/Fix_TradeRocketFuelRefresh.lua", 1)
    rt.execute(ROCKET_FACTORY)
    return rt, spans


def main():
    bench = db.Bench("F119 trade fuel -- shipped request/status bodies and module")
    check = bench.check

    vanilla, spans = make_runtime(False)
    print("extracted:")
    for rel, lo, hi in spans:
        print(f"  {rel}:{lo}-{hi}")

    vanilla.execute('''
	DROP = rocket("UniversalTradeRocket", 50000, 50000)
	change_fuel(DROP, 30000)
	DROP_STATUS = DROP:GetCargoResourcesStatus()
	RISE = rocket("UniversalTradeRocket", 50000, 50000)
	change_fuel(RISE, 60000)
	RISE_STATUS = RISE:GetCargoResourcesStatus()
	''')
    v = vanilla.globals()
    drop = v.DROP
    rise = v.RISE
    check("vanilla DROP reproduces status 'unloading'",
          v.DROP_STATUS == "unloading")
    check("vanilla DROP leaves supply at 0",
          drop["supply"]["Fuel"]["amount"] == 0)
    check("vanilla RISE reproduces status 'loading'",
          v.RISE_STATUS == "loading")
    check("vanilla RISE leaves demand at 0",
          rise["demand"]["Fuel"]["amount"] == 0)

    fixed, _ = make_runtime(True)
    check("module behaviour guard accepts the shipped defective body",
          fixed.globals().SMRFixPack["apply_error"] is None)
    fixed.execute('''
	DROP = rocket("UniversalTradeRocket", 50000, 50000)
	change_fuel(DROP, 30000)
	DROP_SUPPLY = DROP.supply.Fuel.amount
	DROP.cargo.Fuel.amount = 30000 -- simulate the requested unload completing
	DROP_STATUS = DROP:GetCargoResourcesStatus()

	RISE = rocket("UniversalTradeRocket", 50000, 50000)
	change_fuel(RISE, 60000)

	HEAL = rocket("UniversalTradeRocket", 50000, 50000)
	HEAL.FuelResourceAmount = 30000 -- pre-stuck save: requests still size 50k
	HEAL.update_calls = 0
	HEALTHY = rocket("UniversalTradeRocket", 30000, 30000)
	HEALTHY.update_calls = 0
	ROCKETS = { HEAL, HEALTHY }
	OnMsg.LoadGame()

	PLAYER = rocket("UniversalRocket", 50000, 50000)
	change_fuel(PLAYER, 60000)
	''')
    f = fixed.globals()
    check("module DROP sets a 20000 supply request", f.DROP_SUPPLY == 20000)
    check("module DROP reaches 'ready' once that fuel is unloaded",
          f.DROP_STATUS == "ready")
    check("module RISE sets a 10000 demand request",
          f.RISE["demand"]["Fuel"]["amount"] == 10000)
    check("load heal refreshes one pre-stuck Trade rocket",
          f.HEAL["supply"]["Fuel"]["amount"] == 20000
          and f.HEAL["update_calls"] == 1)
    check("load heal is a no-op on a healthy Trade rocket",
          f.HEALTHY["update_calls"] == 0)
    check("player rocket behaviour is unchanged (one vanilla refresh)",
          f.PLAYER["demand"]["Fuel"]["amount"] == 10000
          and f.PLAYER["update_calls"] == 1)

    return bench.finish(
        "ALL DEMANDS HELD -- the shipped bodies reproduce the request mismatch; "
        "the module repairs the desk model and the heal is selective."
    )


if __name__ == "__main__":
    sys.exit(main())
