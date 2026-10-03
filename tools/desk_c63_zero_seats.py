#!/usr/bin/env python3
"""C63: expired disaster skips termination at zero seats on build 25579348.

Read-only control using extracted 1.1.1.406343 RecalcFactionsDisasters and
UpdateFactionsDisasters bodies. GameTime, faction_log/dbg/Msg are environment
shims; DailyUpdate counts dispatch only. ShouldStop raises if invoked: the
expired-duration control must short-circuit it, never replace its decision.
Fixtures set stored state, not election reachability or real daily harm.
One-seat falsifying fixture must reject the zero-seat-retention predicate.
No game, save, mod, document, or archive writes. Run from repo:
    python tools/desk_c63_zero_seats.py
"""
from pathlib import Path
import deskbench as d

ROOT = Path(__file__).resolve().parents[2] / "SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src"
d.TREES["current"] = str(ROOT)


def run(seats):
    rt = d.lua_runtime()
    rt.execute("""
        FactionsHolder = {}; const = {DayDuration = 720000}
        UIColony = {labels = {FactionObject = {}}}
        FactionDefs = {}; messages = {}; updates = 0
        function GameTime() return 3000000 end
        function faction_log(...) return '' end
        function dbg(...) end
        function Msg(name, ...) messages[#messages + 1] = name end
    """)
    rt.globals().seats = seats
    rt.execute("g_Legislature = {legislature_members = {A = seats}}")
    for selector in ("RecalcFactionsDisasters", "UpdateFactionsDisasters"):
        text, first, last = d.body("Lua/Factions/Factions.lua",
            "^function FactionsHolder:" + selector + "[(]", "current")
        d.load_at(rt, text, "=Lua/Factions/Factions.lua", first)
        print(f"body build=25579348 {selector} lines={first}-{last}")
    return rt.execute("""
        local disaster = {start_time = 0, max_duration = 2160000,
            ShouldStop = function() error('refusing dependency unexpectedly reached') end,
            DailyUpdate = function() updates = updates + 1 end}
        local holder = setmetatable({active_factions = {A=true},
            factions_tension = {A=900}, factions_tension_warnings = {A=true},
            factions_approval = {A={approval=-1000}}, factions_disaster={A=disaster}},
            {__index=FactionsHolder})
        holder:RecalcFactionsDisasters('stop only')
        holder:UpdateFactionsDisasters()
        return holder.factions_disaster.A ~= nil, updates, messages[1]
    """)


def main():
    zero, one = run(0), run(1)
    print("expired zero-seat stored,daily-dispatch,message:", zero)
    print("expired one-seat stored,daily-dispatch,message:", one)
    assert zero == (True, 1, None), zero
    assert one == (False, 0, "FactionDisasterStop"), one
    defect = lambda result: result[0] and result[1] == 1
    assert defect(zero) and not defect(one)
    print("PASS C63: defect predicate accepts shipped zero-seat and rejects one-seat falsifier")


if __name__ == "__main__":
    main()
