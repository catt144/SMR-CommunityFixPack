#!/usr/bin/env python3
"""Migration audit controls, 2026-09-11. No engine or colony execution.

Extract live shipped bodies and load whole pack modules. Require is deliberately
stubbed: these tests measure runtime branches, NOT install/branch-guard safety.
Geometry, engine validity, transport availability and task creation are fixtures;
they cannot establish that a real colony reaches the supplied state.
"""
from pathlib import Path
import deskbench as db


def runtime():
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS)
    rt.execute('''
        Colonist = {}; Residence = {}; Dome = {}; Community = {}
        OnMsg = {}; modules = {}
        SMRFixPack = {
          Register = function(id, spec) modules[id] = spec end,
          Require = function() end,
          SetGlobal = function(id, fn) _G[id] = fn end,
          WhenActive = function(id, fn) return fn end,
          Log = function() end,
        }
        IsValid = function(o) return type(o) == "table" and not o.invalid end
        ValidateBuilding = function(o) return IsValid(o) and o end
        IsKindOf = function(o, cls) return o.kind == cls end
        g_Consts = {ColonistMaxDomeWalkDist=400, ColonistMinDistToIgnorePassage=1000}
        const = {ColonistMaxPassagePassthroughDomes=5}
        UIColony = {labels={Elevator={}, Station={}}}
    ''')
    return rt


def shipped(rt, rel, pattern):
    text, start, _ = db.body(rel, pattern)
    db.load_at(rt, text, '=' + rel, start)


def module(rt, name):
    path = Path(db.REPO) / 'Code' / ('Fix_' + name + '.lua')
    db.load_at(rt, db.read(path), '=' + str(path))
    rt.execute('assert(modules["' + name + '"].apply() == nil)')


def main():
    bench = db.Bench('Migration cluster: controlled branch evidence, not in-play reproduction')
    rt = runtime()
    # is_identical is file-local: load its extracted body with the cache function.
    src, start, _ = db.span('Lua/Units/Colonist.lua',
                           [r'^local function is_identical\(',
                            r'^function FindTransportationModeToCommunity\('])
    db.load_at(rt, src, '=Lua/Units/Colonist.lua', start)
    shipped(rt, 'Lua/Units/Colonist.lua', r'^function FindTransportationModeToCommunity_BeforeTrains\(')
    shipped(rt, 'Lua/Units/Colonist.lua', r'^function GetTransportationModeToCommunity\(')
    rt.execute('''
        IsInWalkingDistDome = function() return false, 800 end
        GetTransportThroughElevator = function() return false end
        CanReachByTrain = function() return false end
        dest = {}; origin = {}; city = {}
        a = FindTransportationModeToCommunity(dest, origin, false, city)
        b = FindTransportationModeToCommunity(dest, origin, true, city)
    ''')
    bench.check('F51 vanilla retains false after shuttles become available', rt.eval('a == false and b == false'))
    module(rt, 'ShuttleTransportCache')
    rt.execute('''
        c = FindTransportationModeToCommunity(dest, origin, true, city)
        d = FindTransportationModeToCommunity(dest, origin, false, city)
    ''')
    bench.check('F51 patch recomputes both false-to-true and true-to-false', rt.eval('c == "shuttle" and d == false'))
    shipped(rt, 'Lua/Units/Colonist.lua', r'^function Colonist:TryToEmigrateToDome\(')
    rt.execute('''
        HasShuttleLandingSlots = function() return true end
        IsTransportAvailableBetween = function() return true end
        CreateColonistTransportTask = function(c) c.transport_task={}; tasks=tasks+1; return true end
        IsLRTransportAvailable = function() return true end
        dest.ReserveResidence = function() end
        unit = {CanWork=function() return false end}
        tasks=0
        Colonist.TryToEmigrateToDome(unit, origin, dest, false, nil)
    ''')
    bench.check('F51 old permanent-block inference fails: false mode still creates shuttle task', rt.eval('tasks == 1'))

    rt.execute('''
        breathable=false; passage={1,2,3}; lookups=0
        GetAtmosphereBreathable=function() return breathable end
        GetDomesPassagePath=function() lookups=lookups+1; return passage end
        unit.GetMap=function() return {} end
        unit.ClearTransportRequest=function(self) self.transport_task=nil end
        unit.DiscardTransportTicket=function() end
        unit.SetCommand=function(self, cmd, dest, path) self.chosen_path=path end
        unit.transport_task=nil
        Colonist.TryToEmigrateToDome(unit, origin, dest, "walk", 300)
    ''')
    bench.check('F52 vanilla 300-unit vacuum leg omits passage', rt.eval('lookups == 0 and unit.chosen_path == nil'))
    module(rt, 'VacuumWalks')
    rt.execute('Colonist.TryToEmigrateToDome(unit, origin, dest, "walk", 300)')
    bench.check('F52 patch uses available passage', rt.eval('lookups == 1 and unit.chosen_path == passage'))
    rt.execute('passage=nil; Colonist.TryToEmigrateToDome(unit, origin, dest, "walk", 300)')
    bench.check('F52 no-passage control remains an outside walk', rt.eval('unit.chosen_path == nil'))
    rt.execute('breathable=true; lookups=0; Colonist.TryToEmigrateToDome(unit, origin, dest, "walk", 300)')
    bench.check('F52 breathable control unchanged', rt.eval('lookups == 0'))

    rt = runtime()
    shipped(rt, 'Lua/Buildings/ShuttleHub.lua', r'^function IsLRTransportAvailable\(')
    rt.execute('''
      hub={shuttle_infos={1}, working=false, ui_working=false, transport_mode="all",
        GetWorkNotPermittedReason=function() return "TurnedOff" end,
        GetWorkNotPossibleReason=function() return false end}
      city={labels={ShuttleHub={hub}}}
    ''')
    bench.check('F54 vanilla admits player-disabled hub', rt.eval('IsLRTransportAvailable(city)'))
    module(rt, 'ShuttleHubOffAvailable')
    bench.check('F54 wrapper rejects player-disabled hub', not rt.eval('IsLRTransportAvailable(city)'))
    rt.execute('hub.ui_working=true; hub.working=true')
    bench.check('F54 working-hub control admitted', rt.eval('IsLRTransportAvailable(city)'))
    rt.execute('hub.working=false; hub.GetWorkNotPermittedReason=function() return "ExceptionalCircumstancesDisabled" end')
    bench.check('F54 self-lifting suspension control admitted', rt.eval('IsLRTransportAvailable(city)'))

    rt = runtime()
    for rel, pat in [
        ('Lua/_GameUtils.lua', r'^function GatherFreeLivingSpaces\('),
        ('Lua/Buildings/Dome.lua', r'^function Dome:RefreshFreeLivingSpaces\('),
        ('Lua/Buildings/Community.lua', r'^function Community:HasAnyFreeLivingSpace\('),
        ('Lua/Buildings/Community.lua', r'^function Community:HasFreeLivingSpaceFor\('),
        ('Lua/Buildings/Residence.lua', r'^function ChooseResidence\('),
    ]:
        shipped(rt, rel, pat)
    rt.execute('''
      min_int=-999999; g_ResidenceVersion=1
      GetResidenceComfort=function() return 50,0 end
      dome={working=true,ui_working=true}
      home={parent_dome=dome,working=false,ui_working=true,
        GetFreeSpace=function() return 3 end, IsSuitable=function() return true end}
      dome.labels={Residence={home}}
      dome.HasAnyFreeLivingSpace=Community.HasAnyFreeLivingSpace
      colonist={dome=dome}
      Dome.RefreshFreeLivingSpaces(dome)
    ''')
    bench.check('F60 vanilla tally/gate exclude unpowered home, assignment accepts it',
                rt.eval('dome.free_spaces.inclusive == 0 and not Community.HasFreeLivingSpaceFor(dome,colonist) and ChooseResidence(colonist,{home}) == home'))
    module(rt, 'DomeFreeSpaceMismatch')
    rt.execute('Dome.RefreshFreeLivingSpaces(dome)')
    bench.check('F60 patched tally counts 3 but migration gate still rejects',
                rt.eval('dome.free_spaces.inclusive == 3 and not Community.HasFreeLivingSpaceFor(dome,colonist)'))
    rt.execute('home.working=true; g_ResidenceVersion=2; Dome.RefreshFreeLivingSpaces(dome)')
    bench.check('F60 powered-home control agrees on tally and gate',
                rt.eval('dome.free_spaces.inclusive == 3 and Community.HasFreeLivingSpaceFor(dome,colonist)'))
    return bench.finish()


if __name__ == '__main__':
    raise SystemExit(main())
