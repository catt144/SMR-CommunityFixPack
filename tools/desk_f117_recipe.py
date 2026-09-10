#!/usr/bin/env python3
"""Which landing layouts make Fix_ArrivalDeaths half (b) call Community:GetScoreFor at all?

Written 2026-09-09 by hotfix2 link 99b Unit D (session scratchpad); promoted to
tools/ the same day on the owner's ruling (checklist 131). The scenarios and
demands are verbatim; this is the run bugs/F117.md §Control quotes.

The shipped 1.1.0 span _GameUtils.lua:382-501 (is_welcoming_community,
no_foot_route_dist, GetDomesReachableByColonists, ChooseDome -- the two file
locals the functions close over come along verbatim) is extracted with
tools/luafn.find_bodies and loaded under the real file name and line offset.
Everything the span calls into is a stub keyed on a walking-distance table.
The wrapper's reachability test (Code/Fix_ArrivalDeaths.lua:341-344) and its
re-pick (:352-355) are RETYPED here -- seven lines, cited. The stub dome's
GetScoreFor counts calls; the question per scenario is whether the count in
the wrapper's re-pick is zero (throw unreachable) or not (throw reachable).

Scenarios (each an expectation; the run fails if any does not hold):
  S0   one welcoming dome walkable, with space      -> assigned; wrapper stands down
  S1   the REFUTED recipe (foot route, beyond walking, no station)
       -> landing list empty, far dome assigned as safety, wrapper FIRES,
          re-pick list empty, GetScoreFor NEVER called (a clean arrival either way)
  S1b  same with no foot route at all               -> nothing assigned; wrapper cannot fire
  S2   the station route                            -> far dome listed WITHOUT an elevator,
          wrapper FIRES, re-pick list non-empty, GetScoreFor CALLED
  S2b  station route, far dome full                 -> assigned as safety; FIRES; CALLED
  S2c  station route, no foot route to the dome     -> safety from the sweep; FIRES; CALLED
  S3   elevator by the pad, dome on the far side    -> assigned WITH its elevator; stands down
  S4   a walkable dome that is FULL + a far dome    -> safety = the nearest = the walkable one;
          stands down (a full dome is not a route either)

⚠️ This models REACHABILITY on the shipped bodies, not a map: it shows which
layouts reach the scoring call, never that a colony produces one. IsInWalkingDist
is a table here (its CheckWalkableDistance branch, Dome.lua:209-231, was read,
not run).

Usage: python tools/desk_f117_recipe.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

REL = "Lua/_GameUtils.lua"

PRELUDE = db.ENGINE_SHIMS + r'''
MainCity = nil
local INVALID = {}
function InvalidPos() return INVALID end
function ValidateBuilding(b) return b end
g_Consts = { DefaultOutsideWorkplacesRadius = 10, CommunityEvalNone = 0 }
const = { trfPassengerTransport = 1 }

WALK = {}    -- WALK[a][b] = { is_walking, dist }; symmetric lookup; absent = no foot route (false, -1)
function IsInWalkingDist(a, b)
	local r = (WALK[a] and WALK[a][b]) or (WALK[b] and WALK[b][a])
	if not r then return false, -1 end
	return r[1], r[2]
end
function CanReachByTrain(a, b) return false end
function IsSameMap(a, b) return a.map == b.map end
'''

SCENARIO_LIB = r'''
CALLS = 0
function dome(name, o)
	o = o or {}
	local d = { name = name, map = o.map or "mars", slot = o.slot or 1,
		can_be_safety_dome = o.safety ~= false, accept_colonists = true, ui_working = true,
		space = o.space ~= false, labels = {} }
	d.labels.Dome = { d }
	function d:HasLifeSupport() return true end
	function d:CanVisit() return true end
	function d:GetScoreFor(c) CALLS = CALLS + 1; return 10 end
	function d:HasFreeLivingSpaceFor(c) return self.space end
	function d:GetClusterDomes() return { self } end
	function d:GetMapSlot() return self.slot end
	return d
end
function station(name, o)
	local s = { name = name, remote = o.remote or {}, labels = { Dome = o.domes or {} } }
	function s:CanAcceptColonists() return true end
	function s:ForEachReachableStation(flags, cb, ...) for _, r in ipairs(self.remote) do cb(r, "train", ...) end end
	function s:CanColonistsFromDifferentDomesWorkServiceTrainHere() return true end
	return s
end
function city(o)
	local m = { stations = o.stations or {} }
	function m:MapForEach(pos, kind, radius, cls, fn) for _, s in ipairs(self.stations) do fn(s) end end
	local c = { labels = { Community = o.communities or {}, Elevator = o.elevators or {}, Dome = o.communities or {} } }
	function c:GetMap() return m end
	return c
end
function elevator(name, o)
	local e = { name = name, map = "mars" }
	e.other = { city = o.other_city, slot = o.other_slot or 2 }
	function e.other:GetPos() return "otherpos" end
	function e.other:GetMapSlot() return self.slot end
	return e
end
ROCKET = { map = "mars" }
POS = "pad"
COLONIST = { traits = {} }

-- RocketBase.lua:2026 + :2064 -- vanilla's landing-time assignment
function land(c)
	local domes, safety, _, elevs = GetDomesReachableByColonists(c, POS)
	local d, e = ChooseDome(COLONIST, domes, safety, elevs)
	return d, e, #domes, safety
end
-- Code/Fix_ArrivalDeaths.lua:341-344, retyped
function wrapper_fires(dome, elev, c)
	if not dome then return false end   -- :339 `if dome and ...`
	local reachable = IsInWalkingDist(dome, POS, c)
		or (elev and IsSameMap(ROCKET, elev) and elev.other
			and elev.other:GetMapSlot() == dome:GetMapSlot())
	return not reachable
end
-- Code/Fix_ArrivalDeaths.lua:352-355, retyped: safety_dome withheld (false)
function repick(c)
	local domes, _, _, elevs = GetDomesReachableByColonists(c, POS)
	local before = CALLS
	local nd = ChooseDome(COLONIST, domes, false, elevs)
	return #domes, CALLS - before, nd
end
function run(c)
	local d, e, n, safety = land(c)
	local fires = wrapper_fires(d, e, c)
	local listn, calls, nd = 0, 0, nil
	if fires then listn, calls, nd = repick(c) end
	return { assigned = d and d.name or "nil", elevator = e and e.name or "nil", landing_list = n,
		safety = safety and safety.name or "nil", fires = fires, repick_list = listn, repick_calls = calls,
		repicked = nd and nd.name or "nil" }
end
'''


def scenario(rt, name, setup):
    rt.execute(setup)
    d = dict(rt.eval("run(CITY)").items())
    print(f"  {name}: assigned={d['assigned']} via={d['elevator']} landing_list={d['landing_list']} safety={d['safety']} "
          f"| wrapper fires={str(d['fires']).lower()} | re-pick list={d['repick_list']} GetScoreFor calls={d['repick_calls']} -> {d['repicked']}")
    return d


def main():
    bench = db.Bench("F117 recipe falsifier -- which landings reach GetScoreFor, on the shipped _GameUtils span")
    expect = bench.check

    span_text, lo, hi = db.span(REL, (r"^local function is_welcoming_community\(",
                                       r"^function GetDomesReachableByColonists\(",
                                       r"^function ChooseDome\("))
    assert "local no_foot_route_dist" in span_text
    print(f"extracted {REL}:{lo}-{hi} ({hi - lo + 1} lines)")

    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    db.load_at(rt, span_text, "=" + REL, lo)
    rt.execute(SCENARIO_LIB)

    print("\n== S0 control: one welcoming dome IN walking distance, with space ==")
    d = scenario(rt, "S0", '''
		WALK = {}; CALLS = 0
		local N = dome("Near")
		WALK[N] = { [POS] = { true, 300 } }
		CITY = city{ communities = { N } }''')
    expect("S0: assigned the walkable dome; wrapper stands down", d["assigned"] == "Near" and not d["fires"])

    print("\n== S1 the refuted recipe: every dome beyond walking distance (foot route exists), no station ==")
    d = scenario(rt, "S1", '''
		WALK = {}; CALLS = 0
		local F = dome("Far")
		WALK[F] = { [POS] = { false, 5000 } }
		CITY = city{ communities = { F } }''')
    expect("S1: landing list EMPTY, far dome assigned as safety_dome, wrapper FIRES, re-pick list empty, GetScoreFor NEVER called",
           d["landing_list"] == 0 and d["assigned"] == "Far" and d["fires"] and d["repick_list"] == 0 and d["repick_calls"] == 0,
           "a clean arrival whether or not F117 is present")

    print("\n== S1b the refuted recipe, no foot route at all (dist -1) ==")
    d = scenario(rt, "S1b", '''
		WALK = {}; CALLS = 0
		local F = dome("Far")
		CITY = city{ communities = { F } }''')
    expect("S1b: nothing assigned (safety needs dist >= 0), wrapper cannot fire", d["assigned"] == "nil" and not d["fires"])

    print("\n== S2 the station route: no dome walkable; a passenger station by the pad reaches a far welcoming dome ==")
    d = scenario(rt, "S2", '''
		WALK = {}; CALLS = 0
		local F = dome("Far")
		WALK[F] = { [POS] = { false, 5000 } }
		local R = station("RemoteStation", { domes = { F } })
		local S = station("PadStation", { remote = { R } })
		WALK[S] = { [POS] = { true, 200 } }
		CITY = city{ communities = { F }, stations = { S } }''')
    expect("S2: far dome on the landing list WITHOUT an elevator pairing, assigned, wrapper FIRES, re-pick list non-empty, GetScoreFor CALLED",
           d["landing_list"] == 1 and d["assigned"] == "Far" and d["elevator"] == "nil" and d["fires"] and d["repick_list"] >= 1 and d["repick_calls"] >= 1)

    print("\n== S2b the station route with the far dome FULL (assignment falls to safety_dome) ==")
    d = scenario(rt, "S2b", '''
		WALK = {}; CALLS = 0
		local F = dome("Far", { space = false })
		WALK[F] = { [POS] = { false, 5000 } }
		local R = station("RemoteStation", { domes = { F } })
		local S = station("PadStation", { remote = { R } })
		WALK[S] = { [POS] = { true, 200 } }
		CITY = city{ communities = { F }, stations = { S } }''')
    expect("S2b: still assigned (as safety), wrapper FIRES, GetScoreFor CALLED in the re-pick",
           d["assigned"] == "Far" and d["fires"] and d["repick_calls"] >= 1)

    print("\n== S2c the station route with NO foot route to the far dome (dist -1) ==")
    d = scenario(rt, "S2c", '''
		WALK = {}; CALLS = 0
		local F = dome("Far")
		local R = station("RemoteStation", { domes = { F } })
		local S = station("PadStation", { remote = { R } })
		WALK[S] = { [POS] = { true, 200 } }
		CITY = city{ communities = { F }, stations = { S } }''')
    expect("S2c: safety_dome comes from the station sweep (:470-472), wrapper FIRES, GetScoreFor CALLED",
           d["assigned"] == "Far" and d["fires"] and d["repick_calls"] >= 1)

    print("\n== S3 the elevator case the sitting guessed: elevator by the pad, dome on the other side ==")
    d = scenario(rt, "S3", '''
		WALK = {}; CALLS = 0
		local D = dome("Under", { map = "under", slot = 2 })
		local U = city{ communities = { D } }
		WALK[D] = { otherpos = { true, 100 } }
		local E = elevator("Lift", { other_city = U, other_slot = 2 })
		WALK[E] = { [POS] = { true, 100 } }
		CITY = city{ elevators = { E } }''')
    expect("S3: dome assigned WITH its elevator; the wrapper's elevator clause holds -> stands down (NOT a trigger)",
           d["assigned"] == "Under" and d["elevator"] == "Lift" and not d["fires"])

    print("\n== S4 a walkable dome that is FULL plus a far foot-reachable dome ==")
    d = scenario(rt, "S4", '''
		WALK = {}; CALLS = 0
		local N = dome("Near", { space = false })
		local F = dome("Far")
		WALK[N] = { [POS] = { true, 300 } }
		WALK[F] = { [POS] = { false, 5000 } }
		CITY = city{ communities = { N, F } }''')
    expect("S4: safety_dome is the NEAREST foot-reachable community = the walkable one, so the full dome is assigned and the wrapper stands down",
           d["assigned"] == "Near" and d["safety"] == "Near" and not d["fires"])

    return bench.finish("ALL DEMANDS HELD -- the refuted recipe never scores, the station route does,\n"
                        "the elevator route stands down by design, and a full walkable dome is not a route either.")


if __name__ == "__main__":
    sys.exit(main())
