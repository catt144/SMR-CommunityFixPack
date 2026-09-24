"""Read-only load-order desk controls; no game, account or production writes.

Loads the pinned pack core and VacuumWalks module verbatim. The two offending
Passage Network definitions and current StartShuttleLeg, ProcessClassdefChildren,
and ResolveValues bodies are extracted with the repo's delimiter. Fixtures stub
unused function targets, constants and engine services. Message dispatch is
additive; no thread/dialog is run. Class restoration is simulated explicitly,
not represented as a full execution of the engine's class builder.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO / "tools"))
import deskbench as db
from luafn import find_bodies, read_lines

REV = "680c2799282dc6c60079691f1e201974a8a006e8"
SRC = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src")
PN = REPO / "docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua"


def from_git(path):
    return subprocess.check_output(["git", "show", REV + ":" + path], cwd=REPO).decode("utf-8")


def extract(path, pattern):
    lines = read_lines(str(path))
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (path, pattern, hits)
    start, end = hits[0]
    text = "\n".join(lines[start:end + 1])
    print("BODY", path.relative_to(SRC) if path.is_relative_to(SRC) else path.relative_to(REPO),
          str(start + 1) + "-" + str(end + 1), hashlib.sha256(text.encode()).hexdigest())
    return text


BOOT = r'''
MESSAGES = {}
OnMsg = setmetatable({}, {__newindex = function(_, name, fn)
  local list = MESSAGES[name] or {}; MESSAGES[name] = list
  list[#list+1] = fn
end})
function Msg(name, ...) for _,fn in ipairs(MESSAGES[name] or {}) do fn(...) end end
function CreateRealTimeThread() end
function ModLog() end
CurrentModOptions = false
DataLoaded = false
const = {Colonist={ColonistMaxDomeWalkDist=20, ColonistMinDistToIgnorePassage=120}}
Dome = {__parents={}, ReserveWorkplace=function() end}
ORIGINAL_DOME = Dome
Colonist = {
  MigrateStep=function() end, GetNextMigrationLeg=function() end,
  TryToEmigrateToDome=function() end, CancelWorkReservation=function() end,
}
HasShuttleLandingSlots = function() end
GetAtmosphereBreathable = function() end
AreDomesConnectedWithPassage = function() end
IsInWalkingDistDome = function() end
IsUnitInDome = function() end
CurrentThread = function() end
'''


def main():
    print("BASE", REV, "GAME", "1.1.1.405907", db.lua_version())
    core = from_git("Code/00_Core.lua")
    module = from_git("Code/Fix_VacuumWalks.lua")
    for name, text in [("Code/00_Core.lua", core), ("Code/Fix_VacuumWalks.lua", module)]:
        print("INPUT", name, hashlib.sha256(text.encode()).hexdigest())
    pn_hits = find_bodies(read_lines(str(PN)), r"^function Dome\(")
    assert len(pn_hits) == 2, pn_hits
    pn_lines = read_lines(str(PN))
    clobber = "\n".join("\n".join(pn_lines[a:b+1]) for a, b in pn_hits)
    print("PN_DEFINITIONS", ",".join(str(a+1)+"-"+str(b+1) for a,b in pn_hits),
          "members=" + str(len(pn_hits)), "declarations=" + str(clobber.count("function Dome(")))
    start_shuttle = extract(SRC / "Lua/Units/Colonist.lua", r"^function Colonist:StartShuttleLeg\(")
    process_defs = extract(SRC / "CommonLua/Core/classes.lua", r"^function ProcessClassdefChildren\(")
    resolve_values = extract(SRC / "CommonLua/Core/classes.lua", r"^local function ResolveValues\(")
    results = []

    def demand(name, observed, expected):
        assert observed == expected, (name, observed, expected)
        results.append(name)
        print("PASS", name, repr(observed))

    def runtime():
        rt = db.lua_runtime()
        rt.execute(db.ENGINE_SHIMS + BOOT)
        rt.execute(start_shuttle)
        rt.execute(core)
        return rt

    rt = runtime()
    rt.execute(module)
    demand("pack_first_active", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "active")
    rt.execute(clobber)
    demand("later_pn_global_is_function", rt.eval('type(Dome)'), "function")
    demand("later_pn_does_not_revoke_application", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "active")

    rt = runtime()
    rt.execute(clobber)
    rt.execute(module)
    demand("pn_first_inactive", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "inactive")
    demand("pn_first_update_suspect", rt.eval('SMRFixPack.fixes.VacuumWalks.update_suspect'), True)
    demand("pn_first_suspects_names_vacuum", rt.eval('table.concat(SMRFixPack.UpdateSuspects(), ",")'), "VacuumWalks")
    print("DECLINE_REASON", rt.eval('SMRFixPack.fixes.VacuumWalks.detail'))
    rt.execute('Dome=ORIGINAL_DOME; Msg("ClassesBuilt")')
    demand("restoring_global_and_message_do_not_retry", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "inactive")

    rt = runtime()
    rt.execute(clobber)
    rt.execute('Dome=ORIGINAL_DOME; Msg("ClassesBuilt")')
    rt.execute(module)
    demand("first_application_after_restoration_active", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "active")
    demand("first_application_after_restoration_no_suspects", rt.eval('table.concat(SMRFixPack.UpdateSuspects(), ",")'), "")

    rt = runtime()
    rt.execute("local classdefs={Dome=ORIGINAL_DOME}; " + process_defs)
    rt.execute(clobber)
    rt.execute('RECOVERED=false; ProcessClassdefChildren("Dome", function(def, name) if name=="Dome" then RECOVERED=def end end)')
    demand("canonical_definition_recovered_before_rebuild", rt.eval('RECOVERED==ORIGINAL_DOME and type(RECOVERED.ReserveWorkplace)=="function"'), True)
    demand("recovery_does_not_rewrite_global", rt.eval('type(Dome)'), "function")

    rt = runtime()
    rt.execute('SMRFixPack_Disabled.VacuumWalks=true')
    rt.execute(module)
    demand("veto_before_pack_disables", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "disabled")
    rt = runtime()
    rt.execute(module)
    rt.execute('SMRFixPack_Disabled.VacuumWalks=true')
    demand("veto_after_pack_does_not_undo_install", rt.eval('SMRFixPack.fixes.VacuumWalks.status'), "active")

    # Execute shipped simple-inheritance branch. Both control classes are fixtures;
    # this proves the late-patch hazard, not its incidence among today's classes.
    rt = db.lua_runtime()
    rt.execute('''
local classes={Parent={},Child={}}
local classdefs={Parent={__parents={},probe=function() return "old" end},Child={__parents={"Parent"}}}
local resolved={}
local ancestors_by_parents={}
local noninheritable={class=true,__parents=true,__ancestors=true,__index=true}
local noncopyable={}
local all_classes_meta={}
''' + resolve_values + '''
ResolveValues("Child", nil, classdefs.Child)
classes.Parent.probe=function() return "new" end
CLASS_RESULT=classes.Parent.probe() .. "," .. classes.Child.probe()
''')
    demand("postbuild_parent_patch_leaves_copied_child_old", rt.globals().CLASS_RESULT, "new,old")
    print("RESULT", str(len(results)) + "/" + str(len(results)), "PASS; members=" + ",".join(results))


if __name__ == "__main__":
    main()
