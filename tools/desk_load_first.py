#!/usr/bin/env python3
"""LoadFirst (load-order option B) desk controls on archived 1.1.1.405907 Lua.

    python tools/desk_load_first.py                 # every demand must hold
    python tools/desk_load_first.py --no-promotion  # the pack WITHOUT Code/01_LoadFirst.lua:
                                                    # every case must FAIL, or that case is vacuous

WHAT IS SHIPPED AND LOADED VERBATIM (luafn's delimiter, archived
B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src): the ModEnvBlacklist
literal, the mod-environment metatable and LuaModEnv, ModDef:SetupEnv with the
file-local persistent-data writer and reader, TurnModOn/TurnModOff/AllModsOff,
GetModsEnabledByUser, the dependency queue (GetModAllDependencies through
GetLoadingQueue) and Colonist:StartShuttleLeg (VacuumWalks' behaviour probe).
The pack's own files are loaded whole, UNDER THE REAL SANDBOX (the shipped
metatable over the shipped blacklist), so a name a module reads that the
sandbox hides fails here the way it fails in the game.

RETYPED, AND NAMED AS SUCH: table.find / remove_entry / insert_unique / icopy /
keys follow CommonLua/Core/types.lua:143,1028 and the exported docs
(LuaExportedDocs/Global/table.lua:9-22,194-224); remove_entry removes the FIRST
match, insert_unique appends only an absent value, which is what the duplicate
case below turns on. STUBBED: SaveAccountStorage (a recorder: the desk records
the save REQUEST, never a disk write), CreateRealTimeThread (a recorder; the
notice thread is run on demand), the pregame menu, WaitQuestion/WaitMessage,
ModsRestartApp, Platform, and the class/engine tables VacuumWalks and
HubLocalAccess require. Passage Network's two `function Dome(` definitions are
extracted from the archived 1.38 source (docs/archive/, lines 45-51).

This is desk evidence: it shows what the module WRITES into the saved list and
what it REQUESTS, on the shipped helpers. Whether account.dat lands on disk,
survives a restart or a platform sync is the retail sitting's question.
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import deskbench as db  # noqa: E402
from luafn import find_bodies, read_lines  # noqa: E402

SRC = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src")
MOD_LUA = "CommonLua/Modding/Mod.lua"
UI_LUA = "CommonLua/UI/ModManager.lua"
PN = REPO / "docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua"
PACK = "SMR_CommunityFixPack"
PN_ID = "iooW34Y"
CANARY = "SMRFP-LOADORDER-CANARY-2026-09-25-b7e1"
PROMOTION = True   # set False by --no-promotion: the pack loads without Code/01_LoadFirst.lua

PACK_FILES = ["Code/00_Core.lua", "Code/01_LoadFirst.lua"]
PN_FILES = ["Code/Hubset_OnHubNow.lua", "Code/Fix_VacuumWalks.lua", "Code/Fix_HubLocalAccess.lua"]


def shipped_body(lines, pattern):
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (pattern, hits)
    first, last = hits[0]
    return "\n" * first + "\n".join(lines[first:last + 1]), first + 1, last + 1


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── shipped slices, read once ────────────────────────────────────────────────
mod_lines = read_lines(str(SRC / MOD_LUA))
ui_lines = read_lines(str(SRC / UI_LUA))

BLACKLIST_START = next(i for i, l in enumerate(mod_lines) if l == "ModEnvBlacklist = {")
BLACKLIST_END = next(i for i, l in enumerate(mod_lines[BLACKLIST_START + 1:], BLACKLIST_START + 1) if l == "}")
BLACKLIST = "\n" * BLACKLIST_START + "\n".join(mod_lines[BLACKLIST_START:BLACKLIST_END + 1])
ENV_START = next(i for i, l in enumerate(mod_lines) if l == "if FirstLoad then" and i > 1450)
ENV_END = find_bodies(mod_lines, r"^function LuaModEnv\(env\)")[0][1]
ENV_BLOCK = "\n" * ENV_START + "\n".join(mod_lines[ENV_START:ENV_END + 1])
STORAGE, STORAGE_A, STORAGE_B = shipped_body(mod_lines, r"^local function WriteModPersistentData\(mod, data\)")
READER, _, _ = shipped_body(mod_lines, r"^local function ReadModPersistentData\(mod\)")
SETUP, SETUP_A, SETUP_B = shipped_body(mod_lines, r"^function ModDef:SetupEnv\(\)")
ENABLED, ENABLED_A, ENABLED_B = shipped_body(mod_lines, r"^function GetModsEnabledByUser\(\)")
HELPERS = [shipped_body(ui_lines, rf"^function {n}\(id\)") for n in ("TurnModOn", "TurnModOff")]
ALL_OFF, _, _ = shipped_body(ui_lines, r"^function AllModsOff\(\)")
QUEUE_START = find_bodies(mod_lines, r"^local function GetModAllDependencies\(mod\)")[0][0]
QUEUE_END = find_bodies(mod_lines, r"^local function GetLoadingQueue\(list(?:, silent)?\)")[0][1]
QUEUE = "\n" * QUEUE_START + "\n".join(mod_lines[QUEUE_START:QUEUE_END + 1])
colonist_lines = read_lines(str(SRC / "Lua/Units/Colonist.lua"))
START_SHUTTLE, SS_A, SS_B = shipped_body(colonist_lines, r"^function Colonist:StartShuttleLeg\(")
pn_lines = read_lines(str(PN))
PN_HITS = find_bodies(pn_lines, r"^function Dome\(")
assert len(PN_HITS) == 2, PN_HITS
PN_CLOBBER = "\n".join("\n".join(pn_lines[a:b + 1]) for a, b in PN_HITS)

# Retyped table helpers (see the docstring) plus the engine tolerances deskbench names.
TABLE_RETYPED = r'''
function table.find(array, field, value)
	if not array then return end
	if value == nil then
		value = field
		for i = 1, #array do if value == array[i] then return i end end
	else
		for i = 1, #array do
			if type(array[i]) ~= "boolean" and value == array[i][field] then return i end
		end
	end
end
function table.remove_entry(array, field, value)   -- types.lua:143: the FIRST match only
	local i = table.find(array, field, value)
	if i then return i, table.remove(array, i) end
end
function table.insert_unique(t, x)                 -- types.lua:1028
	if not table.find(t, x) then t[#t + 1] = x return true end
end
function table.icopy(t, deep)
	local copy = {}
	for i = 1, #t do local v = t[i]; if deep and type(v) == "table" then v = table.icopy(v, deep) end; copy[i] = v end
	return copy
end
function table.keys(t, sorted)
	local res = {}
	if t and next(t) then for k in pairs(t) do res[#res + 1] = k end end
	if sorted then table.sort(res) end
	return res
end
function table.copy(t) local out = {} for k, v in pairs(t) do out[k] = v end return out end
'''

BOOT = r'''
FirstLoad = true; Loading = true; PersistableGlobals = {}; ModMsgBlacklist = {}
const = { MaxModDataSize = 32768,
	Colonist = { ColonistMaxDomeWalkDist = 20, ColonistMinDistToIgnorePassage = 120 } }
function IsPStr() return false end
LocalStorage = {}
SAVE = { calls = 0, last_delay = nil }
function SaveAccountStorage(delay) SAVE.calls = SAVE.calls + 1; SAVE.last_delay = delay end
MESSAGES = {}
OnMsg = setmetatable({}, { __newindex = function(_, name, fn)
	local l = MESSAGES[name] or {}; MESSAGES[name] = l; l[#l + 1] = fn end })
function Msg(name, ...) for _, fn in ipairs(MESSAGES[name] or {}) do fn(...) end end
function ModMessage() end
function IsUserCreatedContentAllowed() return true end
function GetModBlacklistedReason() return nil end
function CreateModPersistentStorageTable() return {} end
function WriteModPersistentStorageTable() end
LOG = {}
function ModLog(s) LOG[#LOG + 1] = s end
THREADS = {}
function CreateRealTimeThread(fn, ...) THREADS[#THREADS + 1] = fn end
CLOCK = 0
function RealTime() return CLOCK end
function Sleep(ms) CLOCK = CLOCK + (ms or 0) end
function Untranslated(s) return s end
Platform = { pc = true, debug = false }
MENU_OPEN = true
function GetPreGameMainMenu() return MENU_OPEN and { menu = true } or nil end
UI = { questions = {}, messages = {}, restarts = {}, answer = "cancel" }
function WaitQuestion(parent, title, text, ok, cancel)
	UI.questions[#UI.questions + 1] = { title = title, text = text, ok = ok, cancel = cancel }
	return UI.answer
end
function WaitMessage(parent, title, text) UI.messages[#UI.messages + 1] = { title = title, text = text } end
function ModsRestartApp(debug) UI.restarts[#UI.restarts + 1] = debug; return UI.restart_err end
-- class/engine tables VacuumWalks and HubLocalAccess require (fixtures; the guards read shapes only)
Dome = { __parents = {}, ReserveWorkplace = function() end, dome_network = false }
ORIGINAL_DOME = Dome
PassageHubBase = { hub_domes = false }
Colonist = { MigrateStep = function() end, GetNextMigrationLeg = function() end,
	TryToEmigrateToDome = function() end, CancelWorkReservation = function() end,
	HasLocalAccess = function() return false end }
HasShuttleLandingSlots = function() end
GetAtmosphereBreathable = function() end
AreDomesConnectedWithPassage = function() end
IsInWalkingDistDome = function() end
IsUnitInDome = function() end
CurrentThread = function() end
IsValid = function(x) return x ~= nil end
IsKindOf = function() return false end
ResolveMap = function() return nil end
IsBeingDestructed = function() return false end
function DefineMods(ids)
	Mods = {}
	for _, id in ipairs(ids) do
		Mods[id] = { id = id, version = 1, dependencies = {}, code = {}, entities = {}, options = {},
			GetModLabel = function(self) return self.id end, IsTooOld = function() return false end }
	end
end
'''


class Case:
    """One runtime per case: a fresh sandbox, a fresh AccountStorage."""

    def __init__(self, seed, mods, *, options=None, config_load_all=False,
                 account_load_all=False, veto=False, persistent=None, deps=None,
                 loaded=None, promotion=None, before_pack=None, extra_files=()):
        self.lua = db.lua_runtime()
        L = self.lua
        L.execute(db.ENGINE_SHIMS + TABLE_RETYPED + BOOT)
        L.execute("DefineMods(%s)" % lua_list(mods))
        L.execute("AccountStorage = { LoadMods = %s, ModPersistentData = {}, ModOptions = {} }" % lua_list(seed))
        if account_load_all:
            L.execute("AccountStorage.LoadAllMods = true")
        L.execute("config = { LoadAllMods = %s }" % ("true" if config_load_all else "false"))
        if persistent is not None:
            L.globals().PRESEED = persistent
            L.execute("AccountStorage.ModPersistentData[%r] = PRESEED" % PACK)
        for mod_id, dep_list in (deps or {}).items():
            L.execute("Mods[%r].dependencies = { %s }" % (mod_id, ", ".join(
                "{ id = %r, required = true, ModFits = function() return true end }" % d for d in dep_list)))
        opts = {"LoadFirst": True} if options is None else options
        L.execute("Mods[%r].options = { %s }" % (PACK, ", ".join(
            "%s = %s" % (k, "true" if v else "false") for k, v in opts.items())))
        L.execute("ModsLoaded = {}; for _, id in ipairs(%s) do if Mods[id] then ModsLoaded[#ModsLoaded+1] = Mods[id] end end"
                  % lua_list(loaded or seed))
        if veto:
            L.execute("SMRFixPack_Disabled = { LoadFirst = true }")
        # shipped slices
        L.execute(BLACKLIST)
        L.execute(ENV_BLOCK)
        L.execute("ModDef = {}\nlocal max_data_length = const.MaxModDataSize\n" + STORAGE + "\n" + READER + "\n" + SETUP)
        for text, _, _ in HELPERS:
            L.execute(text)
        L.execute(ALL_OFF)
        L.execute(ENABLED)
        L.execute(QUEUE + "\nGetLoadingQueueShipped = GetLoadingQueue")
        L.execute(START_SHUTTLE)
        L.execute("mod_env = LuaModEnv(); Mods[%r].env = mod_env; ModDef.SetupEnv(Mods[%r])" % (PACK, PACK))
        if before_pack:
            L.execute(before_pack)
        files = list(PACK_FILES)
        if promotion is None:
            promotion = PROMOTION
        if not promotion:
            files.remove("Code/01_LoadFirst.lua")
        files += list(extra_files)
        for rel in files:
            self.load_pack_file(rel)

    def load_pack_file(self, rel):
        text = (REPO / rel).read_text(encoding="utf-8")
        self.lua.globals().SRC_TEXT = text
        self.lua.globals().SRC_NAME = "=" + rel
        self.lua.execute('local fn = assert(load(SRC_TEXT, SRC_NAME, "t", mod_env)); fn()')

    def ev(self, expr):
        return self.lua.eval(expr)

    def ex(self, code):
        self.lua.execute(code)

    def saved(self):
        return lua_join(self.ev("GetModsEnabledByUser()"))

    def queue(self):
        return lua_join(self.ev("GetLoadingQueueShipped(GetModsEnabledByUser(), true)"))

    def loaded(self):
        return lua_join(self.ev("(function() local t = {} for i, m in ipairs(ModsLoaded) do t[i] = m.id end return t end)()"))

    def status(self, fix_id):
        return self.ev("(function() local f = SMRFixPack.fixes[%r]; return f and f.status or 'absent' end)()" % fix_id)

    def detail(self, fix_id):
        return self.ev("(function() local f = SMRFixPack.fixes[%r]; return f and f.detail or '' end)()" % fix_id)

    def saves(self):
        return int(self.ev("SAVE.calls"))

    def run_threads(self):
        # each recorded real-time thread body, once, on the desk clock
        self.ex("for _, fn in ipairs(THREADS) do fn() end; THREADS = {}")

    def questions(self):
        return int(self.ev("#UI.questions"))

    def messages(self):
        return int(self.ev("#UI.messages"))

    def restarts(self):
        return int(self.ev("#UI.restarts"))

    def slot(self):
        v = self.ev("AccountStorage.ModPersistentData[%r]" % PACK)
        return None if v is None else str(v)


def lua_list(items):
    return "{ " + ", ".join("%r" % s for s in items) + " }"


def lua_join(t):
    if t is None:
        return "<nil>"
    return ",".join(str(t[i]) for i in range(1, len(t) + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-promotion", action="store_true",
                    help="load the pack without Code/01_LoadFirst.lua; every case must then FAIL")
    args = ap.parse_args()
    promo = not args.no_promotion
    global PROMOTION
    PROMOTION = promo

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    bench = db.Bench("LoadFirst desk controls — %s (HEAD %s, game 1.1.1.405907, %s)"
                     % ("WITHOUT the promotion (control run)" if args.no_promotion else "with the promotion", head, db.lua_version()))
    for rel in PACK_FILES + PN_FILES:
        print("INPUT", rel, sha((REPO / rel).read_text(encoding="utf-8")))
    print("SHIPPED %s ModEnvBlacklist %d-%d %s" % (MOD_LUA, BLACKLIST_START + 1, BLACKLIST_END + 1, sha(BLACKLIST.strip("\n"))))
    print("SHIPPED %s env block %d-%d %s" % (MOD_LUA, ENV_START + 1, ENV_END + 1, sha(ENV_BLOCK.strip("\n"))))
    print("SHIPPED %s WriteModPersistentData %d-%d, SetupEnv %d-%d, GetModsEnabledByUser %d-%d"
          % (MOD_LUA, STORAGE_A, STORAGE_B, SETUP_A, SETUP_B, ENABLED_A, ENABLED_B))
    print("SHIPPED %s queue %d-%d %s" % (MOD_LUA, QUEUE_START + 1, QUEUE_END + 1, sha(QUEUE.strip("\n") + "\n")))
    print("SHIPPED %s TurnModOn %d-%d TurnModOff %d-%d" % (UI_LUA, HELPERS[0][1], HELPERS[0][2], HELPERS[1][1], HELPERS[1][2]))
    print("SHIPPED Lua/Units/Colonist.lua StartShuttleLeg %d-%d" % (SS_A, SS_B))
    print("PN_DEFINITIONS", ",".join("%d-%d" % (a + 1, b + 1) for a, b in PN_HITS), "members=%d" % len(PN_HITS))
    print()
    mods = ["A", "B", "C", PACK]

    # 1. Promotion: middle, then last; the running session untouched; one save request
    c = Case(["B", PACK, "C"], mods)
    bench.check("1a middle: saved B,PACK,C becomes PACK,B,C", c.saved() == "%s,B,C" % PACK, c.saved())
    bench.check("1a next queue is PACK,B,C", c.queue() == "%s,B,C" % PACK, c.queue())
    bench.check("1a running ModsLoaded stays B,PACK,C", c.loaded() == "B,%s,C" % PACK, c.loaded())
    bench.check("1a exactly one save request, delay 1000", c.saves() == 1 and c.ev("SAVE.last_delay") == 1000,
                "calls=%d delay=%s" % (c.saves(), c.ev("SAVE.last_delay")))
    bench.check("1a LoadFirst active, detail names the move", c.status("LoadFirst") == "active"
                and "moved to the front" in c.detail("LoadFirst"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.run_threads()
    bench.check("1a notice: one question, Restart now / Later, no restart on Later",
                c.questions() == 1 and c.restarts() == 0 and c.ev("UI.questions[1].ok") == "Restart now"
                and c.ev("UI.questions[1].cancel") == "Later", "questions=%d restarts=%d" % (c.questions(), c.restarts()))
    if promo:
        c.load_pack_file("Code/01_LoadFirst.lua")   # a Lua reload re-runs the file
    c.run_threads()
    bench.check("1a Lua reload: no second write, no second notice", c.saves() == 1 and c.questions() == 1,
                "saves=%d questions=%d" % (c.saves(), c.questions()))
    c = Case(["A", "B", PACK], mods)
    c.ex("UI.answer = 'ok'")
    bench.check("1b last: saved A,B,PACK becomes PACK,A,B", c.saved() == "%s,A,B" % PACK, c.saved())
    c.run_threads()
    bench.check("1b Restart now calls the game's restart routine once", c.restarts() == 1, c.restarts())

    # 2. Already first: nothing written, no request, no notice
    c = Case([PACK, "A", "B"], mods)
    bench.check("2 already first: saved list unchanged", c.saved() == "%s,A,B" % PACK, c.saved())
    bench.check("2 already first: no save request", c.saves() == 0, c.saves())
    bench.check("2 already first: LoadFirst active, detail says first of 3", c.status("LoadFirst") == "active"
                and c.detail("LoadFirst").startswith("first of 3"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.run_threads()
    bench.check("2 already first: no notice", c.questions() == 0 and c.messages() == 0,
                "questions=%d messages=%d" % (c.questions(), c.messages()))
    bench.check("2 already first: persistent slot untouched", c.slot() is None, c.slot())

    # 3. LoadAllMods, both flags: no write, the player is told (status + log)
    for label, kw in (("3a config.LoadAllMods", {"config_load_all": True}),
                      ("3b AccountStorage.LoadAllMods", {"account_load_all": True})):
        c = Case(["B", PACK, "C"], mods, **kw)
        bench.check(label + ": raw saved list untouched", lua_join(c.ev("AccountStorage.LoadMods")) == "B,%s,C" % PACK,
                    lua_join(c.ev("AccountStorage.LoadMods")))
        bench.check(label + ": no save request", c.saves() == 0, c.saves())
        bench.check(label + ": LoadFirst inactive naming LoadAllMods", c.status("LoadFirst") == "inactive"
                    and "LoadAllMods" in c.detail("LoadFirst"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
        bench.check(label + ": a log line says not applied", c.ev(
            "(function() for _, l in ipairs(LOG) do if l:find('LoadFirst: not applied', 1, true) then return true end end return false end)()"),
            c.ev("table.concat(LOG, ' | ')"))

    # 4. Opt-out: Mod Option off leaves the order alone; on again promotes; the veto too
    c = Case(["B", PACK, "C"], mods, options={"LoadFirst": False})
    bench.check("4a option off: saved list untouched", c.saved() == "B,%s,C" % PACK, c.saved())
    bench.check("4a option off: no save request", c.saves() == 0, c.saves())
    bench.check("4a option off: LoadFirst inactive 'turned off in Mod Options'",
                c.status("LoadFirst") == "inactive" and c.detail("LoadFirst") == "turned off in Mod Options",
                "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.ex("rawset(Mods[%r].options, 'LoadFirst', true); Msg('ApplyModOptions', %r)" % (PACK, PACK))
    bench.check("4b toggled on: promotes at once", c.saved() == "%s,B,C" % PACK, c.saved())
    bench.check("4b toggled on: one save request, LoadFirst active", c.saves() == 1 and c.status("LoadFirst") == "active",
                "saves=%d status=%s" % (c.saves(), c.status("LoadFirst")))
    c.run_threads()
    bench.check("4b toggled on: the notice shows", c.questions() == 1, c.questions())
    c.ex("rawset(Mods[%r].options, 'LoadFirst', false); Msg('ApplyModOptions', %r)" % (PACK, PACK))
    bench.check("4c toggled off again: inactive, order left as it is, no new request",
                c.status("LoadFirst") == "inactive" and c.saved() == "%s,B,C" % PACK and c.saves() == 1,
                "status=%s saved=%s saves=%d" % (c.status("LoadFirst"), c.saved(), c.saves()))
    c = Case(["B", PACK, "C"], mods, veto=True)
    bench.check("4d veto SMRFixPack_Disabled.LoadFirst: disabled, untouched, no request",
                c.status("LoadFirst") == "disabled" and c.saved() == "B,%s,C" % PACK and c.saves() == 0,
                "status=%s saved=%s saves=%d" % (c.status("LoadFirst"), c.saved(), c.saves()))

    # 5. The pack's own persistent slot: foreign lines preserved, our line counts promotions
    c = Case(["B", PACK, "C"], mods, persistent="somebody-else v3 alpha\nbeta")
    slot = c.slot() or ""
    lines = slot.split("\n")
    bench.check("5a slot: our line first, promotions=1 from=2 of=3", lines[0].startswith("SMRFixPack.LoadFirst v1 promotions=1 ")
                and "from=2 of=3" in lines[0], repr(lines[0]))
    bench.check("5a slot: both foreign lines preserved verbatim", lines[1:] == ["somebody-else v3 alpha", "beta"], repr(lines[1:]))
    # the player disables and re-enables the pack (it goes last); a new process promotes again
    c.ex("TurnModOff(%r); TurnModOn(%r); if SMRFixPack.LoadFirst then SMRFixPack.LoadFirst.promoted = nil end" % (PACK, PACK))
    c.ex("if SMRFixPack.LoadFirst then assert(SMRFixPack.LoadFirst.Promote('desk') == nil) end")
    slot = c.slot() or ""
    lines = slot.split("\n")
    bench.check("5b second promotion: promotions=2, foreign lines still intact, saved list PACK first",
                lines[0].startswith("SMRFixPack.LoadFirst v1 promotions=2 ") and lines[1:] == ["somebody-else v3 alpha", "beta"]
                and c.saved() == "%s,B,C" % PACK and c.saves() == 2,
                "%r saved=%s saves=%d" % (lines, c.saved(), c.saves()))
    c = Case([PACK, "B"], mods, persistent="somebody-else v3 alpha")
    bench.check("5c already first: a foreign slot is not rewritten, LoadFirst active 'first of'",
                c.slot() == "somebody-else v3 alpha" and c.saves() == 0 and c.status("LoadFirst") == "active"
                and c.detail("LoadFirst").startswith("first of"), "%r saves=%d %s" % (c.slot(), c.saves(), c.status("LoadFirst")))

    # 6. Dependencies: a prerequisite of ours stays ahead in the queue; a dependant of ours is unmoved
    c = Case(["B", PACK, "A"], mods, deps={PACK: ["A"]})
    bench.check("6a own prerequisite A: saved PACK,B,A; queue hoists A first, PACK before B",
                c.saved() == "%s,B,A" % PACK and c.queue() == "A,%s,B" % PACK, "saved=%s queue=%s" % (c.saved(), c.queue()))
    c = Case(["Z", PACK, "B"], mods + ["Z"], deps={"Z": [PACK]})
    bench.check("6b Z requires the pack: saved PACK,Z,B; queue PACK,Z,B (Z unmoved relative to B)",
                c.saved() == "%s,Z,B" % PACK and c.queue() == "%s,Z,B" % PACK, "saved=%s queue=%s" % (c.saved(), c.queue()))

    # Audit item 2: list shapes — absent, duplicate and stale ids
    c = Case(["A", "B"], mods)
    bench.check("shape: pack absent from the list: untouched, no request, inactive 'not in the saved mod list'",
                c.saved() == "A,B" and c.saves() == 0 and c.status("LoadFirst") == "inactive"
                and "not in the saved mod list" in c.detail("LoadFirst"),
                "saved=%s saves=%d %s/%s" % (c.saved(), c.saves(), c.status("LoadFirst"), c.detail("LoadFirst")))
    c = Case(["B", PACK, "B", "GHOST"], mods)
    bench.check("shape: duplicate B collapses to its first position, stale GHOST kept in place",
                c.saved() == "%s,B,GHOST" % PACK, c.saved())
    bench.check("shape: duplicate/stale list requests exactly one save", c.saves() == 1, c.saves())
    c = Case(["A", "B", PACK, "C", "D"], mods + ["D"])
    bench.check("shape: five mods, pack third: others keep A,B,C,D order",
                c.saved() == "%s,A,B,C,D" % PACK, c.saved())

    # 7. Passage Network: this launch loads PN before the pack (guards decline); the promoted
    #    order is the next queue, and loading in THAT order both guards pass.
    c = Case([PN_ID, PACK], [PN_ID, PACK], loaded=[PN_ID, PACK], before_pack=PN_CLOBBER, extra_files=PN_FILES)
    bench.check("7a PN before pack: VacuumWalks declines (inactive)", c.status("VacuumWalks") == "inactive",
                "%s / %s" % (c.status("VacuumWalks"), c.detail("VacuumWalks")))
    bench.check("7a PN before pack: HubLocalAccess does not apply", c.status("HubLocalAccess") != "active",
                "%s / %s" % (c.status("HubLocalAccess"), c.detail("HubLocalAccess")))
    next_queue = c.queue()
    bench.check("7a saved PN,PACK becomes PACK,PN; next queue PACK,PN", next_queue == "%s,%s" % (PACK, PN_ID),
                "saved=%s queue=%s" % (c.saved(), next_queue))
    # the next launch: load in the queue the promotion produced
    order = next_queue.split(",")
    c2 = Case(order, [PN_ID, PACK], loaded=order,
              before_pack=PN_CLOBBER if order[0] == PN_ID else None, extra_files=PN_FILES)
    if order[0] == PACK:
        c2.ex(PN_CLOBBER)   # PN loads after us and swaps the global; our guards already ran
    bench.check("7b next launch in that order: VacuumWalks active", c2.status("VacuumWalks") == "active",
                "%s / %s" % (c2.status("VacuumWalks"), c2.detail("VacuumWalks")))
    bench.check("7b next launch in that order: HubLocalAccess active", c2.status("HubLocalAccess") == "active",
                "%s / %s" % (c2.status("HubLocalAccess"), c2.detail("HubLocalAccess")))
    bench.check("7b next launch: LoadFirst already first, no write", c2.status("LoadFirst") == "active" and c2.saves() == 0,
                "status=%s saves=%d" % (c2.status("LoadFirst"), c2.saves()))

    # Canary: metadata.lua still loads under the metadata env (PlaceObj + box only), returns
    # the ModDef with the same declared properties as the committed pre-canary file
    L = db.lua_runtime()
    L.globals().META = (REPO / "metadata.lua").read_text(encoding="utf-8")
    base = subprocess.run(["git", "show", "4e4c97b:metadata.lua"], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout   # cp1252 default raises on the file's emoji
    L.globals().META_BASE = base
    L.execute(r'''
	function props_of(src)
		local env = { PlaceObj = function(class, props) return { class = class, props = props } end, box = function(...) return {...} end }
		local fn = assert(load(src, "=metadata.lua", "t", env))
		local def = fn()
		assert(type(def) == "table" and def.class == "ModDef", "no ModDef returned")
		local keys = {}
		for i = 1, #def.props, 2 do keys[#keys + 1] = def.props[i] end
		return def, table.concat(keys, ","), rawget(env, "SMRFixPack_LoadOrderCanary")
	end
	DEF, KEYS, LEAK = props_of(META)
	DEF0, KEYS0 = props_of(META_BASE)
	''')
    keys, keys0 = L.eval("KEYS"), L.eval("KEYS0")
    bench.check("canary: metadata.lua loads under the metadata env and returns a ModDef",
                L.eval("DEF.class") == "ModDef")
    bench.check("canary: declared property set = pre-canary set + default_options",
                set(keys.split(",")) == set(keys0.split(",")) | {"default_options"},
                sorted(set(keys.split(",")) ^ set(keys0.split(","))))
    bench.check("canary: the literal is in the tree file and leaks no global", CANARY in L.globals().META and L.eval("LEAK") is None)
    bench.check("canary: the code list still starts 00_Core, 01_LoadFirst", L.eval(
        "(function() for i = 1, #DEF.props, 2 do if DEF.props[i] == 'code' then return DEF.props[i+1][1] .. ',' .. DEF.props[i+1][2] end end end)()")
        == "Code/00_Core.lua,Code/01_LoadFirst.lua")

    code = bench.finish()
    if args.no_promotion:
        # per CASE (the label's leading token: 1a, 2, 3b, shape, 7a ...): a case is vacuous
        # only if NONE of its demands fails without the promotion. The canary demands are
        # independent of the module by design and are reported apart.
        failed = sum(1 for ok, _ in bench.results if not ok)
        cases = {}
        for ok, label in bench.results:
            key = label.split(":")[0].split(" ")[0] if not label.startswith("shape") else "shape"
            cases.setdefault(key, []).append(ok)
        vacuous = [k for k, oks in cases.items() if all(oks) and k != "canary"]
        print()
        print("CONTROL: %d of %d demands FAILED with Code/01_LoadFirst.lua removed; %d case(s), %d with no failing demand%s"
              % (failed, len(bench.results), len(cases) - 1, len(vacuous),
                 (": " + ", ".join(vacuous)) if vacuous else " (none vacuous)"))
        print("CONTROL: the demands that still held are the no-write halves; each case's status demand fails, which is the control")
        return 1
    return code


if __name__ == "__main__":
    sys.exit(main())
