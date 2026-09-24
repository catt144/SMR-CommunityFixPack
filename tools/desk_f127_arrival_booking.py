#!/usr/bin/env python3
"""F127: archived 1.1.1 arrival booking, full-dome Homeless label, and fix-removed control.

Run with --premise before the repair to confirm the reported orphan booking.
The C83 module runs whole; reservation and label decisions use shipped Lua bodies.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402
import desk_c83_arrivals as c83  # noqa: E402

ARCHIVE = os.path.join(os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"), "1.1.1.405907", "Src")
db.TREES["1.1.0"] = ARCHIVE

BOOKING = r'''
table.find = function(t, v) for i, x in ipairs(t) do if x == v then return i end end end
Residence = {}
Dome = {}
MicroGHabitatBase = {}
function Colonist:CanChangeCommand() return true end
function Colonist:CheckForcedResidence() return false end
function Colonist:SetResidence(home) self.residence = home end
function Colonist:IsDying() return false end
function Colonist:Affect(effect, value) self.homeless_effect = value end
function make_home(parent)
	local home = setmetatable({parent_dome = parent, reserved = {}, ui_working = true}, {__index = Residence})
	function home:IsSuitable(unit) return true end
	function home:GetFreeSpace() return 1 - #self.reserved end
	return home
end
function booked_arrival(with_reroute, full, habitat)
	WALK = {}
	local dead = dome("Dead", {working = not with_reroute, life = not with_reroute, accept = not with_reroute})
	local live = dome(habitat and "Habitat" or "Live", {space = not full, safety = not habitat})
	WALK[dead] = {pad = {true, 100}}
	WALK[live] = {pad = {true, 300}}
	local c = city{communities = {dead, live}}
	function c:AddToLabel(label, unit) self.homeless = true end
	function c:RemoveFromLabel(label, unit) self.homeless = false end
	function dead:ResetFreeSpace() end
	function live:ResetFreeSpace() end
	function dead:AddToLabel(label, unit) self.homeless = true end
	function dead:RemoveFromLabel(label, unit) self.homeless = false end
	dead.ReserveResidence = Dome.ReserveResidence
	if habitat then
		live.reserved = {}
		live.ReserveResidence = MicroGHabitatBase.ReserveResidence
		live.CanReserveResidence = Residence.CanReserveResidence
		live.ChooseResidence = MicroGHabitatBase.ChooseResidence
		function live:IsSuitable(unit) return true end
		function live:GetFreeSpace() return self.space and 1 - #self.reserved or 0 end
		function live:RefreshFreeLivingSpaces() end
	else
		live.ReserveResidence = Dome.ReserveResidence
		function live:ChooseResidence(unit) return false end
	end
	function live:AddToLabel(label, unit) self.homeless = true end
	function live:RemoveFromLabel(label, unit) self.homeless = false end
	local home = make_home(dead)
	dead.labels.Residence = {home}
	live.labels.Residence = habitat and {} or (full and {} or {make_home(live)})
	local unit = setmetatable({name = "Arrival", arriving = ROCKET, emigration_dome = dead,
		emigration_elevator = false, city = c, traits = {}, residence = false,
		reserved_residence = false}, {__index = Colonist})
	dead:ReserveResidence(unit)
	local originally_booked = unit.reserved_residence == home and home.reserved[unit] == true
	unit:Idle("control")
	local travel_booking = unit.reserved_residence and (unit.reserved_residence.parent_dome or unit.reserved_residence).name or "none"
	unit.dome = unit.emigration_dome
	unit:UpdateResidence()
	unit:UpdateHomelessLabels()
	return {originally_booked = originally_booked,
		destination = unit.emigration_dome.name,
		travel_booking = travel_booking,
		reserved_dome = unit.reserved_residence and (unit.reserved_residence.parent_dome or unit.reserved_residence).name or "none",
		old_booked = home.reserved[unit] == true,
		homeless = c.homeless == true,
		residence = unit.residence ~= false}
end
'''


def runtime(module_text):
    rt = db.lua_runtime()
    rt.execute(c83.PRELUDE)
    span, lo, hi = db.span(c83.REL, (
        r"^local function is_welcoming_community\(",
        r"^function GetDomesReachableByColonists\(",
        r"^function ChooseDome\(",
    ))
    db.load_at(rt, span, "=" + c83.REL, lo)
    db.load_at(rt, module_text, "=Code/Fix_ArrivalDeaths.lua", 1)
    rt.execute(c83.SCENARIO_LIB)
    rt.execute(BOOKING)
    bodies = (
        ("Lua/Units/Colonist.lua", r"^function Colonist:CancelResidenceReservation\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:UpdateResidence\("),
        ("Lua/Units/Colonist.lua", r"^function Colonist:UpdateHomelessLabels\("),
        ("Lua/Buildings/Residence.lua", r"^function Residence:CanReserveResidence\("),
        ("Lua/Buildings/Residence.lua", r"^function Residence:ReserveResidence\("),
        ("Lua/Buildings/Residence.lua", r"^function Residence:CancelResidenceReservation\("),
        ("Lua/Buildings/Dome.lua", r"^function Dome:ReserveResidence\("),
        ("Lua/Buildings/MicroGHabitat.lua", r"^function MicroGHabitatBase:ReserveResidence\("),
        ("Lua/Buildings/MicroGHabitat.lua", r"^function MicroGHabitatBase:ChooseResidence\("),
    )
    for rel, pattern in bodies:
        body, first, last = db.body(rel, pattern)
        db.load_at(rt, body, "=" + rel, first)
        print(f"extracted {rel}:{first}-{last}")
    return rt


def run_case(module_text, reroute=True, full=True, habitat=False):
    rt = runtime(module_text)
    return rt.eval("booked_arrival")(reroute, full, habitat)


def main():
    original = db.read(c83.MODULE)
    premise = "--premise" in sys.argv
    bench = db.Bench("F127 arrival booking on archived 1.1.1.405907")
    check = bench.check
    result = run_case(original)
    if premise:
        check("originally reserved a bed in rejected dome", result["originally_booked"])
        check("C83 reroutes into full welcoming dome", result["destination"] == "Live")
        check("orphan booking remains in rejected dome", result["reserved_dome"] == "Dead" and result["old_booked"])
        check("full-dome arrival is missing from Homeless label", not result["residence"] and not result["homeless"])
        return bench.finish("F127 full-destination harm reproduced on shipped decisions")

    check("originally reserved a bed in rejected dome", result["originally_booked"])
    check("C83 reroutes into full welcoming dome", result["destination"] == "Live")
    check("full-dome reroute releases rejected bed", result["reserved_dome"] == "none" and not result["old_booked"])
    check("full-dome arrival reaches Homeless label", not result["residence"] and result["homeless"])

    room = run_case(original, full=False)
    check("reroute with free housing transfers the booking", room["destination"] == "Live" and room["travel_booking"] == "Live" and not room["old_booked"])

    habitat = run_case(original, habitat=True)
    check("full habitat releases rejected bed", habitat["destination"] == "Habitat" and habitat["reserved_dome"] == "none" and not habitat["old_booked"])
    check("full habitat arrival reaches Homeless label", not habitat["residence"] and habitat["homeless"])

    habitat_room = run_case(original, full=False, habitat=True)
    check("habitat with room takes the transferred booking", habitat_room["destination"] == "Habitat" and habitat_room["travel_booking"] == "Habitat" and not habitat_room["old_booked"])

    marker = ("\t\t\t\t\t\t-- FIX (F127): release the rejected booking before reserving elsewhere.\n"
              "\t\t\t\t\t\tif reachable and new_dome and new_dome ~= dome then\n"
              "\t\t\t\t\t\t\tlocal booked = self.reserved_residence\n"
              "\t\t\t\t\t\t\tif IsValid(booked) and (booked.parent_dome or booked) == dome then\n"
              "\t\t\t\t\t\t\t\tself:CancelResidenceReservation()\n"
              "\t\t\t\t\t\t\t\tif type(new_dome.ReserveResidence) == \"function\" then\n"
              "\t\t\t\t\t\t\t\t\tnew_dome:ReserveResidence(self)\n"
              "\t\t\t\t\t\t\t\tend\n"
              "\t\t\t\t\t\t\tend\n"
              "\t\t\t\t\t\tend\n")
    assert original.count(marker) == 1, "F127 fix block missing or duplicated"
    removed = original.replace(marker, "")
    control = run_case(removed)
    check("fix-removed control retains orphan and hides Homeless", control["destination"] == "Live" and control["reserved_dome"] == "Dead" and control["old_booked"] and not control["homeless"])

    habitat_control = run_case(removed, habitat=True)
    check("fix-removed full habitat retains orphan and hides Homeless", habitat_control["destination"] == "Habitat" and habitat_control["reserved_dome"] == "Dead" and habitat_control["old_booked"] and not habitat_control["homeless"])

    cancel_line = "\t\t\t\t\t\t\t\tself:CancelResidenceReservation()\n"
    old_shape = original.replace(cancel_line, "", 1)
    assert old_shape != original, "old-shape control did not remove cancellation"
    old_habitat = run_case(old_shape, habitat=True)
    check("old reserve-only shape fails on full habitat", old_habitat["reserved_dome"] == "Dead" and old_habitat["old_booked"] and not old_habitat["homeless"])

    native = run_case(original, reroute=False)
    check("unrerouted booking remains native", native["destination"] == "Dead" and native["reserved_dome"] == "Dead" and native["old_booked"])
    return bench.finish("F127 fix and fix-removed control discriminate")


if __name__ == "__main__":
    sys.exit(main())
