#!/usr/bin/env python3
"""C83 arrival reroute control over shipped GetDomes/ChooseDome bodies.

The 1.1.0 ``Lua/_GameUtils.lua:382-501`` span is extracted under its real
file name and offset.  ``Code/Fix_ArrivalDeaths.lua`` is loaded whole through
the same Register/Require seam the game uses.  Only engine objects and the
already-separately-falsified F117 argument discriminator are stubbed.

This controls the desk demands recorded in ``agent/bugs/C83.md``, plus the D03
composition and destination/elevator pairing.  It proves branch behaviour on
the shipped function bodies; it does not prove that a retail colony produces
the layouts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

REL = "Lua/_GameUtils.lua"
MODULE = os.path.join(db.REPO, "Code", "Fix_ArrivalDeaths.lua")

PRELUDE = db.ENGINE_SHIMS + r'''
MainCity = nil
local INVALID = {}
function InvalidPos() return INVALID end
function ValidateBuilding(b) return b end
g_Consts = { DefaultOutsideWorkplacesRadius = 10, CommunityEvalNone = 0 }
const = { trfPassengerTransport = 1, Scale = { Stat = 100 } }

WALK = {}
function IsInWalkingDist(a, b)
	local r = (WALK[a] and WALK[a][b]) or (WALK[b] and WALK[b][a])
	if not r then return false, -1 end
	return r[1], r[2]
end
function CanReachByTrain(a, b) return false end
function IsSameMap(a, b) return a.map == b.map end
function IsValid(o) return type(o) == "table" and o.valid ~= false end
g_CObjectFuncs = { GetMapSlot = function(self) return self.slot end }

-- The F117 discriminator itself is controlled separately by desk_f117_*.
-- This faithful shape stub lets this harness drive (or deliberately decline)
-- C83 without re-testing that whole concern here.
Community = {}
ARG_MODE = "colonist"
function Community.GetScoreFor(self, arg)
	if ARG_MODE == "unknown" then return 0 end
	local attrs = ARG_MODE == "colonist" and arg.traits or arg
	local score = 0
	for trait in pairs(self.traits_filter) do
		if attrs and attrs[trait] then score = score + 1 end
	end
	return score
end
function Community:HasLifeSupport() return true end
function Community:CanAcceptNewColonists() return true end

Colonist = {}
function Colonist:Idle(...)
	self.orig_idle_calls = (self.orig_idle_calls or 0) + 1
	return "orig"
end
function Colonist:OnArrival(...) return "arrival" end
function Colonist:Arrive(...) return "arrive" end

SMRFixPack = { logs = {} }
APPLY_MODULE = true
function SMRFixPack.Register(id, def)
	SMRFixPack.registered = id
	if APPLY_MODULE then
		local err = def.apply()
		assert(not err, err)
	end
end
function SMRFixPack.Require(id, specs)
	for _, spec in ipairs(specs) do
		if spec.probe then
			local ok, answer = pcall(spec.probe)
			if not ok or answer ~= true then
				return spec.reason
			end
		end
	end
end
function SMRFixPack.Log(fmt, ...)
	local line = string.format(fmt, ...)
	SMRFixPack.logs[#SMRFixPack.logs + 1] = line
end
'''

SCENARIO_LIB = r'''
function dome(name, o)
	o = o or {}
	local d = {
		name = name, map = o.map or "mars", slot = o.slot or 1,
		can_be_safety_dome = o.safety ~= false,
		accept_colonists = o.accept ~= false,
		ui_working = o.working ~= false,
		life = o.life ~= false,
		space = o.space ~= false,
		score = o.score or 10,
		closed = o.closed or false,
		labels = {},
	}
	d.labels.Dome = { d }
	function d:HasLifeSupport() return self.life end
	function d:CanAcceptNewColonists()
		return self.ui_working and self.accept_colonists and not self.closed
	end
	function d:CanVisit() return true end
	function d:GetScoreFor(c) return self.score end
	function d:HasFreeLivingSpaceFor(c) return self.space end
	function d:GetClusterDomes() return { self } end
	function d:GetMapSlot() return self.slot end
	return d
end

function station(name, o)
	local s = { name = name, remote = o.remote or {}, labels = { Dome = o.domes or {} } }
	function s:CanAcceptColonists() return true end
	function s:ForEachReachableStation(flags, cb, ...)
		for _, remote in ipairs(self.remote) do cb(remote, "train", ...) end
	end
	function s:CanColonistsFromDifferentDomesWorkServiceTrainHere() return true end
	return s
end

function city(o)
	local map = { stations = o.stations or {} }
	function map:MapForEach(pos, kind, radius, cls, fn)
		for _, s in ipairs(self.stations) do fn(s) end
	end
	local c = {
		labels = {
			Community = o.communities or {},
			Elevator = o.elevators or {},
			Dome = o.communities or {},
		}
	}
	function c:GetMap() return map end
	return c
end

function elevator(name, o)
	local e = { name = name, map = "mars" }
	e.other = { city = o.other_city, slot = o.other_slot or 2 }
	function e.other:GetPos() return "otherpos" end
	function e.other:GetMapSlot() return self.slot end
	return e
end

ROCKET = { name = "Rocket", map = "mars", valid = true }
function ROCKET:IsValidPos() return true end
function ROCKET:GetPos() return "pad" end

function run(assigned, c, traits, assigned_elevator)
	local unit = setmetatable({
		name = "Arrival", arriving = ROCKET,
		emigration_dome = assigned,
		emigration_elevator = assigned_elevator or false,
		city = c, traits = traits or {},
	}, { __index = Colonist })
	local result = unit:Idle("control")
	return {
		result = result,
		dome = unit.emigration_dome,
		elevator = unit.emigration_elevator,
		orig_calls = unit.orig_idle_calls or 0,
		cached = SMRFixPack.ArrivalDeaths and SMRFixPack.ArrivalDeaths.CachedArgShape(),
		logs = #SMRFixPack.logs,
		last_log = SMRFixPack.logs[#SMRFixPack.logs],
	}
end
'''


def make_runtime(apply=True, arg_mode="colonist"):
    span_text, lo, hi = db.span(
        REL,
        (
            r"^local function is_welcoming_community\(",
            r"^function GetDomesReachableByColonists\(",
            r"^function ChooseDome\(",
        ),
    )
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    rt.globals().APPLY_MODULE = apply
    rt.globals().ARG_MODE = arg_mode
    db.load_at(rt, span_text, "=" + REL, lo)
    db.load_at(rt, db.read(MODULE), "=Code/Fix_ArrivalDeaths.lua", 1)
    rt.execute(SCENARIO_LIB)
    return rt, lo, hi


def named(result, key):
    obj = result[key]
    return obj["name"] if obj else "false"


def main():
    bench = db.Bench("C83 arrivals -- welcoming fallback and composition control")
    expect = bench.check

    # Premise control: this same layout must NOT repair itself when the module
    # registers but is deliberately not applied.
    rt, lo, hi = make_runtime(apply=False)
    print(f"extracted {REL}:{lo}-{hi} ({hi - lo + 1} lines)")
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		LIVE = dome("Live")
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[LIVE] = { pad = { true, 300 } }
		CITY = city{ communities = { DEAD, LIVE } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("control: without apply, the dead assignment survives (the harness cannot pass by vanilla alone)", named(r, "dome") == "Dead")

    print("\n== A/B: reachable dead assignment, welcoming target with and without housing ==")
    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		LIVE = dome("Live")
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[LIVE] = { pad = { true, 300 } }
		CITY = city{ communities = { DEAD, LIVE } }
		A1 = run(DEAD, CITY)
		A2 = run(DEAD, CITY)
	''')
    a1, a2 = rt.globals().A1, rt.globals().A2
    expect("A: dead reachable dome -> welcoming dome with space", named(a1, "dome") == "Live")
    expect(
        "log: first C83 reroute names the colonist and both domes once per session",
        a1["logs"] == 1
        and a2["logs"] == 1
        and a1["last_log"] == "ArrivalDeaths: C83 rerouted Arrival from Dead to Live",
    )

    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		FULL = dome("FullLive", { space = false })
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[FULL] = { pad = { true, 300 } }
		CITY = city{ communities = { DEAD, FULL } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("B: full welcoming dome is still the fallback (arrival becomes homeless there)", named(r, "dome") == "FullLive")

    print("\n== stand-down controls ==")
    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		WALK[DEAD] = { pad = { true, 100 } }
		CITY = city{ communities = { DEAD } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("C: no welcoming dome -> preserve vanilla's assignment", named(r, "dome") == "Dead" and r["logs"] == 0)

    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		LIVE = dome("Live")
		WALK[LIVE] = { pad = { true, 100 } }
		CITY = city{ communities = { LIVE } }
		RESULT = run(LIVE, CITY)
	''')
    r = rt.globals().RESULT
    expect("D: welcoming assigned dome is untouched and never asks the F117 probe", named(r, "dome") == "Live" and r["cached"] is None)

    rt, _, _ = make_runtime(arg_mode="unknown")
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		LIVE = dome("Live")
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[LIVE] = { pad = { true, 300 } }
		CITY = city{ communities = { DEAD, LIVE } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("F: unknown ChooseDome argument shape -> stand down", named(r, "dome") == "Dead" and r["cached"] is False)

    print("\n== F53 regression and station-order falsifier ==")
    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		FAR = dome("Far")
		LIVE = dome("Live")
		WALK[FAR] = { pad = { false, 5000 } }
		WALK[LIVE] = { pad = { true, 300 } }
		CITY = city{ communities = { FAR, LIVE } }
		RESULT = run(FAR, CITY)
	''')
    r = rt.globals().RESULT
    expect("E: F53 not-reachable branch still re-picks with no safety fallback", named(r, "dome") == "Live")

    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		WALKABLE = dome("WalkableFarther", { space = false })
		STATION_ONLY = dome("StationNearer", { space = false })
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[WALKABLE] = { pad = { true, 500 } }
		WALK[STATION_ONLY] = { pad = { false, 200 } }
		REMOTE = station("Remote", { domes = { STATION_ONLY } })
		PAD_STATION = station("PadStation", { remote = { REMOTE } })
		WALK[PAD_STATION] = { pad = { true, 50 } }
		CITY = city{ communities = { DEAD, WALKABLE, STATION_ONLY }, stations = { PAD_STATION } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("G: station-sweep dome appended after sort wins by minimum dome_dist, not list order", named(r, "dome") == "StationNearer")

    print("\n== D03 composition and elevator pairing ==")
    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		CLOSED = dome("Closed", { closed = true, space = false })
		OPEN = dome("Open", { space = false })
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[CLOSED] = { pad = { true, 200 } }
		WALK[OPEN] = { pad = { true, 400 } }
		CITY = city{ communities = { DEAD, CLOSED, OPEN } }
		NONTOURIST = run(DEAD, CITY)
	''')
    r = rt.globals().NONTOURIST
    expect("D03: non-tourist fallback cannot bypass a closed dome's CanAcceptNewColonists veto", named(r, "dome") == "Open")

    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		CLOSED = dome("Closed", { closed = true, space = false })
		OPEN = dome("Open", { space = false })
		WALK[DEAD] = { pad = { true, 100 } }
		WALK[CLOSED] = { pad = { true, 200 } }
		WALK[OPEN] = { pad = { true, 400 } }
		CITY = city{ communities = { DEAD, CLOSED, OPEN } }
		TOURIST = run(DEAD, CITY, { Tourist = true })
	''')
    r = rt.globals().TOURIST
    expect("D03: tourists retain the opt-in module's documented closed-dome exemption", named(r, "dome") == "Closed")

    rt, _, _ = make_runtime()
    rt.execute('''
		WALK = {}
		DEAD = dome("Dead", { working = false, life = false, accept = false })
		UNDER = dome("Under", { map = "under", slot = 2, space = false })
		UNDER_CITY = city{ communities = { UNDER } }
		WALK[UNDER] = { otherpos = { true, 100 } }
		LIFT = elevator("Lift", { other_city = UNDER_CITY, other_slot = 2 })
		WALK[LIFT] = { pad = { true, 50 } }
		WALK[DEAD] = { pad = { true, 100 } }
		CITY = city{ communities = { DEAD }, elevators = { LIFT } }
		RESULT = run(DEAD, CITY)
	''')
    r = rt.globals().RESULT
    expect("pairing: a rerouted elevator dome keeps its matching emigration_elevator", named(r, "dome") == "Under" and named(r, "elevator") == "Lift")

    return bench.finish("ALL C83 DEMANDS HELD -- negative control discriminates; all seven prompt cases, D03 composition, one-shot logging and elevator pairing pass.")


if __name__ == "__main__":
    sys.exit(main())
