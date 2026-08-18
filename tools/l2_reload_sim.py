#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""L2 (lifecycle & idempotency) — two-Lua-load simulator for the DataPatch scaffold.

WHY THIS EXISTS
    `ReloadLua` re-executes every mod file in the SAME process (lib.lua:353-382 ->
    autorun.lua `ModsLoadCode()`), while the tables our preset patches write to
    are NOT rebuilt (`Presets = rawget(_G,"Presets") or {}`, Preset.lua:1339-1340;
    `LoadData` is not re-run by autorun). A player reaches that path by closing the
    Mod Manager after any change (ModManager.lua:162 -> Mod.lua:2145).

    Two archived sessions caught it in the wild — `spowner_Mars.exe-20260812-18.30.09`
    and `rs_ownertick_Mars.exe-20260813-11.16.44`, both 148 `applied` lines = 2x74.
    Diffing their two load blocks shows the pack's ENTIRE second-load delta is four
    modules flipping to `inactive` with a reason that is false.

WHAT IT DOES
    Runs the REAL shipped source of Code/00_Core.lua and the four affected modules
    under a Lua 5.4 runtime (lupa), twice in one process, with the engine's own
    persistence rules reproduced:
      * `SMRFixPack` and the preset fixtures PERSIST between loads;
      * the OnMsg store is DISCARDED between loads (`message_to_staticfuncs` is a
        plain file-local, cthreads.lua:6);
      * class tables are rebuilt (classes.lua:37-38).

    The fixtures are sized so that load 1 reproduces the four archived log lines
    VERBATIM. That reproduction is the harness's own control: a simulator that
    cannot reproduce the measurement is not evidence about it.

USAGE
    python tools/l2_reload_sim.py            # report both loads
    python tools/l2_reload_sim.py --expect-clean-second-load   # exit 1 if load 2
                                             # latches any module inactive
"""

import os
import sys

try:
    import lupa
except ImportError:  # pragma: no cover
    sys.exit("l2_reload_sim: needs `lupa` (pip install lupa)")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(ROOT, "Code")

MODULES = [
    "00_Core.lua",
    "Fix_LastTransmissionStorage.lua",
    "Fix_IndependenceTerraforming.lua",
    "Fix_SaintBlessing.lua",
    "Fix_AstrogeologistExtractors.lua",
]

WATCHED = [
    "LastTransmissionStorage",
    "IndependenceTerraforming",
    "SaintBlessing",
    "AstrogeologistExtractors",
]

# The five load-1 lines the two archived sessions both carry, byte for byte
# (the SaintBlessing pair is the empty-preset window followed by the real pass).
ARCHIVED_LOAD1 = [
    "SaintBlessing: inactive (no dome-colonists trait presets)",
    "LastTransmissionStorage: 6 storage condition(s) made effective, 1 retargeted",
    "IndependenceTerraforming: Independence_TerraformingProjects now discounts special projects by 20% as its param1 says",
    "SaintBlessing: corrected 1 dome-colonists trait modifier label(s) of 2",
    "AstrogeologistExtractors: added 2 missing extractor entr(y/ies) to the astrogeologist profile (10 already present)",
]

# The four load-2 lines they both carry — the defect.
ARCHIVED_LOAD2 = [
    "LastTransmissionStorage: inactive (the shipped presets are already correct)",
    "IndependenceTerraforming: inactive (the shipped tech already matches its own param1)",
    "SaintBlessing: inactive (every dome-colonists trait preset already names a real label)",
    "AstrogeologistExtractors: inactive (the shipped profile already pays every buildable extractor)",
]

# ---------------------------------------------------------------------------
# The engine stubs. Everything here is either (a) reproduced from Src, or
# (b) a fixture standing in for shipped data — never a stand-in for our code.
# ---------------------------------------------------------------------------

BOOT = r"""
-- ---- captured log -------------------------------------------------------
SMRSIM = SMRSIM or { log = {}, threads = 0 }
-- ModLog stores the message and its ModPrint output path formats the single
-- argument AGAIN (Mod.lua:109-132, lib.lua:164-174) — which is why
-- SMRFixPack.Log escapes '%'. Reproduce the second pass so the captured text
-- is what lands in the game's log file.
function ModLog(msg) SMRSIM.log[#SMRSIM.log + 1] = string.format(msg) end

-- ---- Msg / OnMsg --------------------------------------------------------
-- cthreads.lua:6 — `local message_to_staticfuncs = {}` is a plain file-local,
-- NOT under FirstLoad, so registrations do NOT survive a Lua reload. The
-- simulator therefore recreates this store at the head of every load.
function SMRSIM_ResetMessages()
    SMRSIM_msgs = {}
    OnMsg = setmetatable({}, { __newindex = function(_, name, fn)
        local t = SMRSIM_msgs[name]
        if not t then t = {}; SMRSIM_msgs[name] = t end
        t[#t + 1] = fn
    end })
end
function Msg(name, ...)
    for _, fn in ipairs(SMRSIM_msgs[name] or {}) do
        local ok, err = pcall(fn, ...)
        if not ok then SMRSIM.log[#SMRSIM.log + 1] = "SIMERROR " .. tostring(err) end
    end
end

-- ---- misc engine surface our four modules touch at load time -------------
function CreateRealTimeThread(fn) SMRSIM.threads = SMRSIM.threads + 1 end
function RealTime() return 0 end
function Sleep(ms) end
function Untranslated(s) return s end
function T(id, s) return s end
function GetPreGameMainMenu() return nil end
function WaitMessage() end
function IsValid() return false end
function AllMapsForEach() end
function GameTime() return 0 end
function GetModifiablePropScale() return 1 end
function GetGridGlobalStorage() return 0 end
function GetCommanderProfile() return nil end
function PlaceObj(cls, t) t = t or {}; t.class = cls; return t end
empty_table = {}
CurrentModOptions = false
Mods = false
DataLoaded = false
SMRFixPack_Disabled = SMRFixPack_Disabled or {}
SMRFixPack_Optional = SMRFixPack_Optional or {}

-- ---- classes: REBUILT every Lua load (classes.lua:37-38 clears the class
-- globals, OnMsg.Autorun rebuilds them). Redefining them here each load is
-- exactly that behaviour.
function SMRSIM_RebuildClasses()
    TraitPreset = { AddDomeColonistsModifier = function() end }
    LabelContainer = { SetLabelModifier = function() end }
    Effect_ModifyLabel = { OnApplyEffect = function() end }
    FactionDef = {}
    TechPreset = {}
end

-- ---- shipped DATA: survives a Lua reload (Preset.lua:1339-1340, and LoadData
-- is not re-run by autorun). Built ONCE, deliberately.
--
-- The preset GlobalMaps exist EMPTY before DataLoaded (the F75 lesson quoted in
-- 00_Core.lua) — SMRSIM_EmptyPresets reproduces that window, which is what makes
-- load 1 emit SaintBlessing's "no dome-colonists trait presets" line before its
-- "corrected 1 of 2" line, exactly as both archived sessions do.
function SMRSIM_EmptyPresets()
    FactionDefs, TechDef, TraitPresets, CommanderProfiles = {}, {}, {}, {}
    GetTraitLabel = function(id) return "Trait" .. tostring(id) end
end
function SMRSIM_BuildPresets()
    -- Last Transmission: six storage `likes` carrying the test in the wrong
    -- field, one of which also names the wrong grid (-> "6 ... 1 retargeted").
    local likes = {}
    local ids = { "TLEPowerStorage2Sols", "TLENoPowerStorage", "TLEWaterStorage2Sols",
                  "TLENoWaterStorage", "TLEOxygenStorage2Sols", "TLENoOxygenStorage" }
    for i, id in ipairs(ids) do
        local prereq = { { class = "ScriptOther" } }
        if i == 1 then
            prereq = { { class = "ScriptCheckGridGlobalStorage",
                         GridType = "Oxygen", Condition = ">", Value = 1440000 } }
        end
        likes[i] = { Id = id, Prerequisite = prereq, Condition = false }
    end
    FactionDefs = { LastTransmission = { likes = likes } }

    -- Independence_TerraformingProjects: one Consts effect at the shipped -10.
    TechDef = { Independence_TerraformingProjects = {
        { class = "Effect_ModifyLabel", Label = "Consts",
          Prop = "SpecialProjectResourcesModifier", Amount = -10 },
    } }

    -- Two dome-colonists traits; one names a trait id whose LABEL differs.
    GetTraitLabel = function(id)
        if id == "Religious" then return "Religious" end
        return "Trait" .. tostring(id)
    end
    TraitPresets = {
        Saint      = { modify_target = "dome colonists", modify_trait = "Composed" },
        Preacher   = { modify_target = "dome colonists", modify_trait = "Religious" },
        Composed   = {},
        Religious  = {},
    }

    -- The astrogeologist profile: ten Effect_ModifyLabel entries, neither of the
    -- two the shipped enumeration misses. (SMRSIM_AlreadyCorrect below rewrites
    -- these four fixtures into the state a future game patch would ship.)
    local profile = {}
    for i = 1, 10 do
        profile[i] = { class = "Effect_ModifyLabel", Label = "Extractor" .. i,
                       Prop = "production_per_day1", Percent = 10 }
    end
    CommanderProfiles = { astrogeologist = profile }
end

-- NEGATIVE CONTROL. The state a future game patch would ship: every defect this
-- pack repairs is already repaired in the DATA, so nothing our passes do can be
-- the reason. The four modules must still latch `inactive` with their benign
-- "already correct" verdict — if the ever_changed memo suppressed that, the fix
-- would have traded a false `inactive` for a false `active`.
function SMRSIM_AlreadyCorrect()
    SMRSIM_BuildPresets()
    for _, like in ipairs(FactionDefs.LastTransmission.likes) do
        like.Condition = like.Prerequisite
        like.Prerequisite = false
        for _, node in ipairs(like.Condition) do
            if node.class == "ScriptCheckGridGlobalStorage" then node.GridType = "Power" end
        end
    end
    TechDef.Independence_TerraformingProjects[1].Amount = -20
    TraitPresets.Saint.modify_trait = "TraitComposed"
    local profile = CommanderProfiles.astrogeologist
    profile[#profile + 1] = { class = "Effect_ModifyLabel",
        Label = "AutomaticMetalsExtractor", Prop = "production_per_day1", Percent = 10 }
    profile[#profile + 1] = { class = "Effect_ModifyLabel",
        Label = "MicroGAutoWaterExtractor", Prop = "water_production", Percent = 10 }
end
"""


def run(already_correct=False):
    lua = lupa.LuaRuntime(unpack_returned_tuples=True)
    lua.execute(BOOT)
    lua.execute("SMRSIM_EmptyPresets()")
    builder = "SMRSIM_AlreadyCorrect()" if already_correct else "SMRSIM_BuildPresets()"

    loads = []
    for n in (1, 2):
        lua.execute("SMRSIM_ResetMessages()")
        lua.execute("SMRSIM_RebuildClasses()")
        lua.execute("SMRSIM.log = {}")
        for m in MODULES:
            with open(os.path.join(CODE, m), encoding="utf-8") as f:
                src = f.read()
            try:
                lua.execute(src)
            except lupa.LuaError as e:
                sys.exit("l2_reload_sim: %s failed to load on pass %d:\n%s" % (m, n, e))
        if n == 1:
            # COLD BOOT. autorun.lua fires Msg("Autorun") -> ClassesBuild ->
            # Msg("ClassesBuilt") right after ModsLoadCode, while the preset
            # GlobalMaps are still empty; LoadData runs later in StartupSequence
            # and posts DataLoaded, then Dlc.lua:715 posts DataChanged.
            lua.execute('Msg("ClassesBuilt")')
            lua.execute(builder + '; DataLoaded = true')
            lua.execute('Msg("DataLoaded")')
            lua.execute('Msg("DataChanged", nil)')
        else:
            # RELOAD (Mod Manager closed after a change -> ModsReloadItems ->
            # ReloadLua). LoadData is NOT re-run, so neither DataLoaded nor the
            # DataChanged it triggers is posted; ClassesBuilt and ModsReloaded are.
            lua.execute('Msg("ClassesBuilt")')
            lua.execute('Msg("ModsReloaded", false)')
        log = list(lua.eval("SMRSIM.log").values())
        status = {}
        for fid in WATCHED:
            e = lua.eval('SMRFixPack.fixes["%s"]' % fid)
            status[fid] = (e["status"], e["detail"])
        loads.append((log, status))
    return loads


def negative_control():
    """A future game patch already fixed the data: the benign verdict must survive."""
    loads = run(already_correct=True)
    out = []
    for n, (_log, status) in enumerate(loads, 1):
        for fid in WATCHED:
            out.append((n, fid) + status[fid])
    print("=" * 72)
    print("NEGATIVE CONTROL — shipped data already correct (no pass edits anything)")
    print("=" * 72)
    for n, fid, st, det in out:
        print("  load %d | %-28s %-9s %s" % (n, fid, st, det or ""))
    wrong = [(n, fid) for n, fid, st, _ in out if st != "inactive"]
    print("  => modules NOT reporting inactive: %d %s" % (len(wrong), wrong or ""))
    return 1 if wrong else 0


def main():
    strict = "--expect-clean-second-load" in sys.argv
    if "--negative-control" in sys.argv:
        return negative_control()
    loads = run()
    bad = 0

    for n, (log, status) in enumerate(loads, 1):
        print("=" * 72)
        print("LUA LOAD %d  (mod code re-executed in the same process)" % n)
        print("=" * 72)
        for line in log:
            if line.startswith("[CommunityFixPack] "):
                line = line[len("[CommunityFixPack] "):]
            if any(line.startswith(f + ":") for f in WATCHED):
                print("   log |", line)
        for fid in WATCHED:
            st, det = status[fid]
            print("  stat | %-28s %-9s %s" % (fid, st, det or ""))
        print()

    # --- control: does the harness reproduce the archived load-1 measurement?
    l1 = [l[len("[CommunityFixPack] "):] if l.startswith("[CommunityFixPack] ") else l
          for l in loads[0][0]]
    missing = [x for x in ARCHIVED_LOAD1 if x not in l1]
    print("CONTROL — load 1 vs the two archived sessions' load-1 lines:",
          "REPRODUCED (%d/%d)" % (len(ARCHIVED_LOAD1), len(ARCHIVED_LOAD1))
          if not missing else "MISMATCH")
    for x in missing:
        print("   missing:", x)
        bad = 1

    l2 = [l[len("[CommunityFixPack] "):] if l.startswith("[CommunityFixPack] ") else l
          for l in loads[1][0]]
    hit = [x for x in ARCHIVED_LOAD2 if x in l2]
    print("DEFECT   — load 2 reproduces %d/4 of the archived false-inactive lines" % len(hit))
    for x in hit:
        print("   ", x)

    latched = [f for f in WATCHED if loads[1][1][f][0] != "active"]
    print("VERDICT  — modules not `active` after the second load: %d %s"
          % (len(latched), latched or ""))

    if strict and latched:
        print("\nFAIL: --expect-clean-second-load was passed and %d module(s) latched."
              % len(latched))
        return 1
    if strict:
        print("\nPASS: every watched module is still `active` after the second load.")
    return bad


if __name__ == "__main__":
    sys.exit(main())
