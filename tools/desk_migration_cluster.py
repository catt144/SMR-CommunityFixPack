#!/usr/bin/env python3
"""Migration audit controls, 2026-09-11. No engine or colony execution.

Extract live shipped bodies and load whole pack modules. Require is deliberately
stubbed: these tests measure runtime branches, NOT install/branch-guard safety.
Geometry, engine validity, transport availability and task creation are fixtures;
they cannot establish that a real colony reaches the supplied state.
"""
import subprocess
from pathlib import Path
import deskbench as db

# The last commit that carried the PRE-REPAIR Fix_FreedHousingNotice wrapper
# (the synchronous CheckHomeForHomeless call inside Colonist:SetResidence).
# F59's harm legs run against this shape, because the repair removed it from
# Code/ and a falsifier that cannot express the harm is not a falsifier.
F59_HARMFUL_REV = 'bb50f5d'

# F60 was retired in 9bc4360. Keep its harm controls on the actual last
# pre-retirement body; the live pack deliberately no longer contains this file.
F60_HARMFUL_REV = '9bc4360^'


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


def module_text(name, rev=None):
    """-> (source, chunkname) for a pack module: from Code/, or from git at `rev`.

    `rev` reads a SUPERSEDED shape out of git by sha rather than re-typing it,
    which keeps deskbench's "our code is extracted, never retyped" property for
    a body that no longer exists on disk.
    """
    rel = 'Code/Fix_%s.lua' % name
    if rev is None:
        path = Path(db.REPO) / rel
        return db.read(path), str(path)
    spec = '%s:%s' % (rev, rel)
    out = subprocess.run(['git', 'show', spec], cwd=db.REPO, check=True,
                         capture_output=True, text=True, encoding='utf-8')
    return out.stdout, spec


def load_module(rt, name, text, chunkname):
    """Load module source and apply it, raising if apply() declined.

    ⛔ `error`, not `assert`: two harnesses here shim `assert` to
    record-and-continue (EF-008), which would swallow a failed apply() and read
    as coverage it never was.
    """
    db.load_at(rt, text, '=' + chunkname)
    rt.execute('do local e = modules["%s"].apply()'
               ' if e ~= nil then error("apply() declined: " .. tostring(e)) end end' % name)


def module(rt, name, rev=None):
    text, chunkname = module_text(name, rev)
    load_module(rt, name, text, chunkname)


def defer_shim(rt, synchronous=False):
    """Model game-time thread scheduling for a one-shot deferred body.

    EF-029 (MEASURED 2026-08-01, owner at the keyboard): `CreateGameTimeThread`
    DEFERS -- the body does NOT run before the creating statement continues. The
    engine's Lua is cooperative, so a thread also cannot resume in the middle of
    a synchronous call stack. Together those mean a created thread's body runs
    only once the creating stack has unwound, which is what the queue below
    models: `CreateGameTimeThread` records the call, and `RunDeferred()` is what
    a harness calls AFTER the shipped operation returns, standing in for the next
    scheduler opportunity.

    ⚠️ A CONVENTION modelling EF-029, not a measurement of the engine scheduler.
    It models ORDERING only -- never latency, never pause behaviour, and it does
    not establish that a real colony reaches the supplied state.

    `synchronous=True` DEFEATS the deferral (the body runs inside the creating
    statement, i.e. back to the pre-repair timing). That is the falsifier for the
    repair itself: under it the repaired module must express the harm again.
    """
    rt.execute('SYNCHRONOUS = ' + ('true' if synchronous else 'false'))
    rt.execute('''
      _deferred = {}
      Sleep = function() end
      IsValidThread = function() return false end
      if SYNCHRONOUS then
        CreateGameTimeThread = function(f, ...) f(...) return {} end
      else
        CreateGameTimeThread = function(f, ...)
          _deferred[#_deferred+1] = {f, {...}}
          return {}
        end
      end
      -- `error`, not `assert`: assert is shimmed to record-and-continue here.
      function RunDeferred()
        local ran = 0
        while #_deferred > 0 do
          ran = ran + 1
          if ran > 50 then error("deferred queue did not drain") end
          local job = table.remove(_deferred, 1)
          job[1](table.unpack(job[2]))
        end
        return ran
      end
    ''')


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
        ('Lua/Buildings/Community.lua', r'^function Community:GetFreeLivingSpace\('),
        ('Lua/Buildings/RocketUtilities.lua', r'^function GetAvailableResidencesFor\('),
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
      dome.GetFreeLivingSpace=Community.GetFreeLivingSpace
      dome.RefreshFreeLivingSpaces=Dome.RefreshFreeLivingSpaces
      applicants={{{traits={}}},{{traits={}}},{{traits={}}}}
      housing_city={labels={Community={dome}}}
      ApplicantResidenceFilter=function() return "Everyone" end
      sorted_pairs=pairs -- only one applicant group in this fixture
      Dome.RefreshFreeLivingSpaces(dome)
    ''')
    bench.check('F60 vanilla tally/gate exclude unpowered home, assignment accepts it',
                rt.eval('dome.free_spaces.inclusive == 0 and not Community.HasFreeLivingSpaceFor(dome,colonist) and ChooseResidence(colonist,{home}) == home'))
    bench.check('F60 vanilla applicant housing estimate excludes the unpowered home',
                rt.eval('GetAvailableResidencesFor(applicants,3,housing_city) == 0'))
    module(rt, 'DomeFreeSpaceMismatch', rev=F60_HARMFUL_REV)
    rt.execute('Dome.RefreshFreeLivingSpaces(dome)')
    bench.check('F60 patched tally counts 3 but migration gate still rejects',
                rt.eval('dome.free_spaces.inclusive == 3 and not Community.HasFreeLivingSpaceFor(dome,colonist)'))
    bench.check('F60 patch reports all 3 applicants housed while arrival space gate rejects home',
                rt.eval('GetAvailableResidencesFor(applicants,3,housing_city) == 3 and not Community.HasFreeLivingSpaceFor(dome,colonist)'))
    rt.execute('home.working=true; g_ResidenceVersion=2; Dome.RefreshFreeLivingSpaces(dome)')
    bench.check('F60 powered-home control agrees on tally and gate',
                rt.eval('dome.free_spaces.inclusive == 3 and Community.HasFreeLivingSpaceFor(dome,colonist)'))
    return bench.finish()


if __name__ == '__main__':
    raise SystemExit(main())
