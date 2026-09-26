#!/usr/bin/env python3
"""LoadFirst (load-order option B) desk controls on archived 1.1.1.405907 Lua.

    python tools/desk_load_first.py                # baseline: every demand must hold, then every
                                                   # behavioural mutant must kill the groups it names
    python tools/desk_load_first.py --mutant NAME  # one mutant, verbose (names: see MUTANTS)
    python tools/desk_load_first.py --list         # the groups, their demands and their expected killers

WHAT IS SHIPPED AND LOADED VERBATIM (luafn's delimiter, archived
B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src): the ModEnvBlacklist
literal, the mod-environment metatable and LuaModEnv, ModDef:SetupEnv with the
file-local persistent-data writer and reader, TurnModOn/TurnModOff/AllModsOff,
GetModsEnabledByUser, the dependency queue (GetModAllDependencies through
GetLoadingQueue), Colonist:StartShuttleLeg (VacuumWalks' behaviour probe) and, for
the engine case, ModsReloadItems. The pack's own files are loaded whole, UNDER THE
REAL SANDBOX (the shipped metatable over the shipped blacklist), so a name a module
reads that the sandbox hides fails here the way it fails in the game.

CONTROLS (audit R4, 2026-09-25). A no-op promise ("already first writes nothing")
survives removing the module, so absence is not its falsifier. Each case group
names the MUTANTS that must make it fail: a copy of the module with one behaviour
broken (the rebuild removed, the already-first return removed, the option ignored,
the config flag ignored, the probe ignored, foreign slot bytes dropped, the notice
never scheduled, the veto bypassed, a fixed pre-cleared probe id). Every mutant is
applied by an exact single-occurrence text replacement and asserted to have taken;
a stale replacement is a harness defect and stops the run. All cases keep running
after a failure; nothing asserts inline.

RETYPED, AND NAMED AS SUCH: table.find / remove_entry / insert_unique / icopy /
keys / copy / map / iequal follow CommonLua/Core/types.lua:143,1028 and the
exported docs (LuaExportedDocs/Global/table.lua:9-22,194-224); remove_entry
removes the FIRST match, insert_unique appends only an absent value. STUBBED:
SaveAccountStorage (a recorder: the desk records the save REQUEST, never a disk
write), CreateRealTimeThread (a recorder; threads run when a case says so, which
is what lets a later Options click come AFTER the startup threads have finished),
the pregame menu, WaitQuestion/WaitMessage, ModsRestartApp, Platform, and the
class/engine tables VacuumWalks and HubLocalAccess require. Passage Network's two
`function Dome(` definitions are extracted from the archived 1.38 source.

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
MODULE = "Code/01_LoadFirst.lua"
PACK_FILES = ["Code/00_Core.lua", MODULE]
PDX_LUA = "CommonLua/Libs/Paradox/PdxSDK.lua"
WITNESS = "tools/arming/payloads/98_LoadFirstSync.lua.txt"   # the kit's sync completion witness (R5-D)
PN_FILES = ["Code/Hubset_OnHubNow.lua", "Code/Fix_VacuumWalks.lua", "Code/Fix_HubLocalAccess.lua"]
PRE_CANARY_META_REV = "4e4c97b"


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
RELOAD, RELOAD_A, RELOAD_B = shipped_body(mod_lines, r"^function ModsReloadItems\(")
pdx_lines = read_lines(str(SRC / PDX_LUA))
PDX_METHOD_NAMES = ("GetTask", "__Notify", "__Pop", "__WaitPop", "WaitDoTask", "Clear", "WorkerThread", "PushTask")
PDX_METHODS = [shipped_body(pdx_lines, r"^function PdxTaskQueue:" + n + r"\(") for n in PDX_METHOD_NAMES]
FETCH, FETCH_A, FETCH_B = shipped_body(ui_lines, r"^function AsyncPdxGetAllSubscribedMods\(\)")
colonist_lines = read_lines(str(SRC / "Lua/Units/Colonist.lua"))
START_SHUTTLE, SS_A, SS_B = shipped_body(colonist_lines, r"^function Colonist:StartShuttleLeg\(")
pn_lines = read_lines(str(PN))
PN_HITS = find_bodies(pn_lines, r"^function Dome\(")
assert len(PN_HITS) == 2, PN_HITS
PN_CLOBBER = "\n".join("\n".join(pn_lines[a:b + 1]) for a, b in PN_HITS)

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
function table.map(t, field) local r = {} for i, x in ipairs(t) do r[i] = x[field] end return r end
function table.iequal(a, b) if #a ~= #b then return false end for i = 1, #a do if a[i] ~= b[i] then return false end end return true end
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
function CreateRealTimeThread(fn, ...) THREADS[#THREADS + 1] = fn; return { thread = #THREADS } end
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

# The sync witness fixture (R5-D): the archived PdxTaskQueue methods run on a real
# coroutine worker, exactly as PdxSDK.lua:927-931 runs them on a real-time thread;
# WaitWakeup yields "wait", an outstanding AsyncPdx* call inside a callback yields
# "async" (the shape the re-audit's counterexample used). The game's two handlers
# (ModManager.lua:1902-1906 pushes the root; :1922-1927 clears on logout) and the
# root/child push shapes (:1877, :1882, :1906) are reproduced; SyncUpdatePdxMod is
# a stub whose behaviour each case chooses (return, yield, raise, error string, or
# re-enable the pack the way a version change's TurnModOff/TurnModOn does).
SYNC_FIXTURE = r'''
function CanYield() return true end
SPRO_ERRORS = {}
function sprocall(fn, ...)
	local r = table.pack(pcall(fn, ...))
	if not r[1] then SPRO_ERRORS[#SPRO_ERRORS + 1] = tostring(r[2]) end
	return table.unpack(r, 1, r.n)
end
table.iclear = function(t) for i = #t, 1, -1 do t[i] = nil end end
WORKER = false
function CurrentThread() return WORKER end
function WaitWakeup() coroutine.yield("wait") end
function Wakeup() end
function AsyncPending() coroutine.yield("async") end
SIM = { children = 2, behaviour = {}, root_fetch_fails = false, root_async = false }
function SyncUpdatePdxMod(modId, subscribed_mod, installed_mods)
	local b = SIM.behaviour[modId] or "ok"
	if b == "async" then AsyncPending() end
	if b == "raise" then error("assertion failed: RepositoryPath") end
	if b == "errstring" then return "failed to fetch subscribed mod info" end
	if b == "move-pack-last" then TurnModOff(PACKID); TurnModOn(PACKID) end
end
local function SyncPdxMods()
	if SIM.root_async then AsyncPending() end   -- AsyncPdxGetAllSubscribedMods, :1865
	if SIM.root_fetch_fails then return end
	for i = 1, SIM.children do
		g_PopsDownloadModsQueue:PushTask(false, SyncUpdatePdxMod, i, {}, {})
	end
end
OnMsg.PdxLogin = function() g_PopsDownloadModsQueue:PushTask(false, SyncPdxMods) end
OnMsg.PdxLogout = function() g_PopsDownloadModsQueue:Clear() end
g_PopsDownloadModsQueue = setmetatable({ push_message = "PopsDownloadModPush" }, { __index = PdxTaskQueue })
WORKER = coroutine.create(function() g_PopsDownloadModsQueue:WorkerThread() end)
function DRIVE()
	for step = 1, 1000 do
		local ok, why = coroutine.resume(WORKER)
		assert(ok, why)
		if why == "async" then return "async" end
		if why == "wait" and #g_PopsDownloadModsQueue == 0 then return "idle" end
	end
	error("runaway worker")
end
QUIT = { calls = 0 }
function quit() QUIT.calls = QUIT.calls + 1 end
SLOTS = {}
SMRTK = { BindScratch = function(label, fn, opts) SLOTS[label] = fn; return { id = "slot_scratch" } end }
'''

# ── behavioural mutants: (old text, new text) applied to the module source ───
MUTANTS = {
    "no-rebuild": [("\t\tfor _, id in ipairs(list) do TurnModOff(id) end\n\t\tfor _, id in ipairs(wanted) do TurnModOn(id) end",
                    "\t\t-- MUTANT no-rebuild: the list is not rebuilt; registration, probe and record stay")],
    "always-rebuild": [("\tif pos == 1 then\n\t\t-- nothing is written here",
                        "\tif false and pos == 1 then -- MUTANT always-rebuild\n\t\t-- nothing is written here")],
    "ignore-option": [("\t\tif not SMRFixPack.OptionEnabled(ID) then", "\t\tif false then -- MUTANT ignore-option")],
    "ignore-config": [("\tif config_load_all() then", "\tif false then -- MUTANT ignore-config")],
    "ignore-probe": [("\tif not live then", "\tif false then -- MUTANT ignore-probe")],
    "ignore-absent": [("\tif not pos then", "\tif false then -- MUTANT ignore-absent")],
    "clobber-slot": [('\tif rest ~= nil then line = line .. "\\n" .. rest end', "\t-- MUTANT clobber-slot: foreign bytes dropped")],
    "no-notice": [("\tstate.pending_notice = true\n\tschedule_notice()\n\treturn nil", "\treturn nil -- MUTANT no-notice")],
    "bypass-veto": [("\nloading = false\n", "\nloading = false\nstate.Promote('mutant bypass-veto')\n")],
    "fixed-probe": [('\tlocal probe = string.format("SMRFixPack.LoadFirst.probe.%d.%d",\n\t\ttype(os_time) == "function" and os_time() or 0, probe_serial)',
                     '\tlocal probe = "SMRFixPack.LoadFirst.probe" -- MUTANT fixed-probe\n\tpcall(TurnModOff, probe)')],
    # the config flag is also caught by the probe, so only both ignored at once can miss LoadAllMods
    "ignore-loadall": [("\tif config_load_all() then", "\tif false then -- MUTANT ignore-loadall"),
                       ("\tif not live then", "\tif false then -- MUTANT ignore-loadall")],
    # the toggle-off path is 00_Core's reconciler; a module that is not `optional` is invisible to it
    "not-optional": [("\toptional = true,", "\toptional = false, -- MUTANT not-optional")],
}

# witness mutants: the same rule, applied to the kit's sync witness payload. The
# first is the re-audit's counterexample made into code: queue empty means done.
WITNESS_MUTANTS = {
    "witness-queue-only": [("function LoadFirstSync.Verdict(a)\n",
                            'function LoadFirstSync.Verdict(a)\n    if queued() == 0 then return "COMPLETE" end -- MUTANT witness-queue-only\n')],
    "witness-no-finish": [("        rec.finished = now()", "        -- MUTANT witness-no-finish: a returned callback is never recorded")],
    "witness-ignore-clear": [("                rec.cancelled = now()", "                -- MUTANT witness-ignore-clear: a cleared task is not marked")],
    "witness-ignore-error": [("            rec.error = tostring(res[2])", "            -- MUTANT witness-ignore-error (raise)"),
                             ('        if type(res[2]) == "string" then rec.error = "returned: " .. res[2] end',
                              "        -- MUTANT witness-ignore-error (error string)")],
    "witness-empty-is-pass": [('    if #a.children == 0 then return "COMPLETE-EMPTY" end',
                               "    -- MUTANT witness-empty-is-pass: a root that scheduled nothing reads COMPLETE")],
}

# group -> the mutants that must make at least one of its demands fail
KILLERS = {
    "R5D1": {"witness-no-finish", "no-rebuild"}, "R5D2": {"witness-queue-only"},
    "R5D3": {"witness-queue-only", "witness-ignore-clear"}, "R5D4": {"witness-queue-only", "witness-ignore-error"},
    "R5D5": {"witness-queue-only", "witness-empty-is-pass"}, "R5D6": {"witness-no-finish"},
    "R5E1": {"bypass-veto"}, "R5E2": {"no-rebuild", "not-optional"}, "R5E3": {"no-rebuild"},
    "1a": {"no-rebuild", "no-notice"}, "1b": {"no-rebuild", "no-notice"},
    "2": {"always-rebuild"},
    "3a": {"ignore-loadall"}, "3b": {"ignore-probe"},
    "4a": {"ignore-option"}, "4b": {"no-rebuild", "no-notice", "not-optional"}, "4c": {"not-optional"}, "4d": {"bypass-veto"},
    "5a": {"no-rebuild", "clobber-slot"}, "5b": {"clobber-slot"}, "5c": {"always-rebuild"},
    "6a": {"no-rebuild"}, "6b": {"no-rebuild"},
    "7a": {"no-rebuild"}, "7b": {"no-rebuild"},
    "shape": {"no-rebuild", "ignore-absent"},
    "R1a": {"no-notice", "no-rebuild"}, "R1b": {"no-notice"}, "R1c": {"no-notice"}, "R1d": {"no-notice"},
    "R2a": {"clobber-slot"}, "R2b": {"clobber-slot"}, "R2c": {"clobber-slot"},
    "R3a": {"fixed-probe"}, "R3b": {"ignore-config"}, "R3c": {"always-rebuild"},
}
INDEPENDENT = {"canary", "engine", "pdxfetch"}


def mutate(text, name, table=MUTANTS):
    for old, new in table[name]:
        assert text.count(old) == 1, ("mutant text not found exactly once", name, old[:60])
        text = text.replace(old, new)
    return text


class Case:
    """One runtime per case: a fresh sandbox, a fresh AccountStorage."""

    def __init__(self, module_text, seed, mods, *, options=None, config_load_all=False,
                 account_load_all=False, veto=False, persistent=None, deps=None,
                 loaded=None, before_pack=None, extra_files=()):
        self.module_text = module_text
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
        for rel in PACK_FILES:
            self.load_pack_file(rel)
        for rel in extra_files:
            self.load_pack_file(rel)

    def load_pack_file(self, rel):
        text = self.module_text if rel == MODULE else (REPO / rel).read_text(encoding="utf-8")
        self.lua.globals().SRC_TEXT = text
        self.lua.globals().SRC_NAME = "=" + rel
        self.lua.execute('local fn = assert(load(SRC_TEXT, SRC_NAME, "t", mod_env)); fn()')

    def ev(self, expr):
        return self.lua.eval(expr)

    def ex(self, code):
        self.lua.execute(code)

    def saved(self):
        return lua_join(self.ev("GetModsEnabledByUser()"))

    def raw(self):
        return lua_join(self.ev("AccountStorage.LoadMods"))

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
        # every recorded real-time thread body, once, in order, on the desk clock
        self.ex("local t = THREADS; THREADS = {}; for _, fn in ipairs(t) do fn() end")

    def threads_pending(self):
        return int(self.ev("#THREADS"))

    def questions(self):
        return int(self.ev("#UI.questions"))

    def messages(self):
        return int(self.ev("#UI.messages"))

    def restarts(self):
        return int(self.ev("#UI.restarts"))

    def slot(self):
        v = self.ev("AccountStorage.ModPersistentData[%r]" % PACK)
        return None if v is None else str(v)

    def log_has(self, needle):
        return bool(self.ev("(function() for _, l in ipairs(LOG) do if l:find(%r, 1, true) then return true end end return false end)()" % needle))

    def toggle(self, on):
        self.ex("rawset(Mods[%r].options, 'LoadFirst', %s); Msg('ApplyModOptions', %r)" % (PACK, "true" if on else "false", PACK))

    def move_pack_last(self):
        self.ex("TurnModOff(%r); TurnModOn(%r)" % (PACK, PACK))

    # ── the sync witness (R5-D): archived queue class + fixture + the kit payload under the sandbox ──
    def load_witness(self, witness_text, mode="sitting", install=True):
        self.ex("PACKID = %r; PdxTaskQueue = {}" % PACK)
        for body, _, _ in PDX_METHODS:
            self.ex(body)
        self.ex(SYNC_FIXTURE)
        anchor = 'MODE = "sitting"'
        assert witness_text.count(anchor) == 1, "witness MODE literal not found exactly once"
        text = witness_text.replace(anchor, "MODE = %r" % mode)
        self.lua.globals().SRC_TEXT = text
        self.lua.globals().SRC_NAME = "=" + WITNESS
        self.lua.execute('local fn = assert(load(SRC_TEXT, SRC_NAME, "t", mod_env)); fn()')
        # the payload's first thread installs the wrappers as soon as the queue exists; the
        # unattended driver (its second thread) stays pending until a case runs the threads
        if install:
            self.install_witness()

    def install_witness(self):
        self.ex("local t = table.remove(THREADS, 1); t()")

    def login(self):
        self.ex("Msg('PdxLogin')")

    def logout(self):
        self.ex("Msg('PdxLogout')")

    def drive(self):
        return self.ev("DRIVE()")

    def verdict(self):
        return self.ev("mod_env.LoadFirstSync.Verdict(mod_env.LoadFirstSync.W.current)")

    def passes(self):
        return bool(self.ev("mod_env.LoadFirstSync.Pass(mod_env.LoadFirstSync.Verdict(mod_env.LoadFirstSync.W.current))"))

    def queued(self):
        return int(self.ev("#g_PopsDownloadModsQueue"))

    def log_count(self, needle):
        return int(self.ev("(function() local n = 0 for _, l in ipairs(LOG) do if l:find(%r, 1, true) then n = n + 1 end end return n end)()" % needle))


def lua_list(items):
    return "{ " + ", ".join("%r" % s for s in items) + " }"


def lua_join(t):
    if t is None:
        return "<nil>"
    return ",".join(str(t[i]) for i in range(1, len(t) + 1))


def group_of(label):
    return label.split(":")[0].split(" ")[0]


class Recorder:
    def __init__(self, verbose):
        self.verbose = verbose
        self.results = []

    def check(self, label, ok, detail=""):
        self.results.append((bool(ok), label))
        if self.verbose:
            print(("  PASS  " if ok else "  FAIL  ") + label + (("  -- " + str(detail)) if detail else ""))
        return ok

    def failed_groups(self):
        return {group_of(l) for ok, l in self.results if not ok}

    def groups(self):
        return {group_of(l) for _, l in self.results}


def run_cases(rec, module_text, witness_text):
    mods = ["A", "B", "C", PACK]
    check = rec.check
    C = lambda seed, m=mods, **kw: Case(module_text, seed, m, **kw)  # noqa: E731

    # 1. Promotion, middle and last; the running session untouched; one save request
    c = C(["B", PACK, "C"])
    check("1a middle: saved B,PACK,C becomes PACK,B,C", c.saved() == "%s,B,C" % PACK, c.saved())
    check("1a next queue is PACK,B,C", c.queue() == "%s,B,C" % PACK, c.queue())
    check("1a running ModsLoaded stays B,PACK,C", c.loaded() == "B,%s,C" % PACK, c.loaded())
    check("1a exactly one save request, delay 1000", c.saves() == 1 and c.ev("SAVE.last_delay") == 1000,
          "calls=%d delay=%s" % (c.saves(), c.ev("SAVE.last_delay")))
    check("1a LoadFirst active, detail names the move", c.status("LoadFirst") == "active"
          and "moved to the front" in c.detail("LoadFirst"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.run_threads()
    check("1a notice: one question, Restart now / Later, no restart on Later",
          c.questions() == 1 and c.restarts() == 0 and c.ev("UI.questions[1].ok") == "Restart now"
          and c.ev("UI.questions[1].cancel") == "Later", "questions=%d restarts=%d" % (c.questions(), c.restarts()))
    c.load_pack_file(MODULE)   # a Lua reload re-runs the file
    c.run_threads()
    check("1a Lua reload: no second write, no second notice", c.saves() == 1 and c.questions() == 1,
          "saves=%d questions=%d" % (c.saves(), c.questions()))
    c = C(["A", "B", PACK])
    c.ex("UI.answer = 'ok'")
    check("1b last: saved A,B,PACK becomes PACK,A,B", c.saved() == "%s,A,B" % PACK, c.saved())
    c.run_threads()
    check("1b Restart now calls the game's restart routine once", c.restarts() == 1 and c.questions() == 1,
          "restarts=%d questions=%d" % (c.restarts(), c.questions()))

    # 2. Already first: nothing written, no request, no notice
    c = C([PACK, "A", "B"])
    check("2 already first: raw saved list unchanged", c.raw() == "%s,A,B" % PACK, c.raw())
    check("2 already first: no save request", c.saves() == 0, c.saves())
    check("2 already first: LoadFirst active, detail names the loaded list", c.status("LoadFirst") == "active"
          and c.detail("LoadFirst").startswith("first in the list the game loads (3 mods)"),
          "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.run_threads()
    check("2 already first: no notice", c.questions() == 0 and c.messages() == 0,
          "questions=%d messages=%d" % (c.questions(), c.messages()))
    check("2 already first: persistent slot untouched", c.slot() is None, c.slot())

    # 3. LoadAllMods, both flags, pack not first: raw list byte-identical, no request, told
    c = C(["B", PACK, "C"], config_load_all=True)
    check("3a config.LoadAllMods: raw saved list untouched", c.raw() == "B,%s,C" % PACK, c.raw())
    check("3a config.LoadAllMods: no save request", c.saves() == 0, c.saves())
    check("3a config.LoadAllMods: LoadFirst inactive naming LoadAllMods", c.status("LoadFirst") == "inactive"
          and "LoadAllMods" in c.detail("LoadFirst"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    check("3a config.LoadAllMods: a log line says not applied", c.log_has("LoadFirst: not applied"), c.ev("table.concat(LOG, ' | ')"))
    c = C(["B", PACK, "C"], account_load_all=True)
    check("3b AccountStorage.LoadAllMods: raw saved list untouched", c.raw() == "B,%s,C" % PACK, c.raw())
    check("3b AccountStorage.LoadAllMods: no save request", c.saves() == 0, c.saves())
    check("3b AccountStorage.LoadAllMods: LoadFirst inactive naming LoadAllMods", c.status("LoadFirst") == "inactive"
          and "LoadAllMods" in c.detail("LoadFirst"), "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    check("3b AccountStorage.LoadAllMods: a log line says not applied", c.log_has("LoadFirst: not applied"), c.ev("table.concat(LOG, ' | ')"))

    # 4. Opt-out: Mod Option off leaves the order alone; on again promotes; the veto too
    c = C(["B", PACK, "C"], options={"LoadFirst": False})
    check("4a option off: raw saved list untouched", c.raw() == "B,%s,C" % PACK, c.raw())
    check("4a option off: no save request", c.saves() == 0, c.saves())
    check("4a option off: LoadFirst inactive 'turned off in Mod Options'",
          c.status("LoadFirst") == "inactive" and c.detail("LoadFirst") == "turned off in Mod Options",
          "%s / %s" % (c.status("LoadFirst"), c.detail("LoadFirst")))
    c.run_threads()
    c.toggle(True)
    check("4b toggled on later: promotes at once", c.saved() == "%s,B,C" % PACK, c.saved())
    check("4b toggled on later: one save request, LoadFirst active", c.saves() == 1 and c.status("LoadFirst") == "active",
          "saves=%d status=%s" % (c.saves(), c.status("LoadFirst")))
    c.run_threads()
    check("4b toggled on later: the notice shows", c.questions() == 1, c.questions())
    c.toggle(False)
    check("4c toggled off again: inactive, order left as it is, no new request",
          c.status("LoadFirst") == "inactive" and c.saved() == "%s,B,C" % PACK and c.saves() == 1,
          "status=%s saved=%s saves=%d" % (c.status("LoadFirst"), c.saved(), c.saves()))
    c.move_pack_last()
    c.run_threads()
    check("4c option off, pack moved last, nothing promotes: raw B,C,PACK, no request, no notice",
          c.raw() == "B,C,%s" % PACK and c.saves() == 1 and c.questions() == 1,
          "raw=%s saves=%d questions=%d" % (c.raw(), c.saves(), c.questions()))
    c = C(["B", PACK, "C"], veto=True)
    c.run_threads()
    check("4d veto SMRFixPack_Disabled.LoadFirst: disabled, untouched, no request, no notice",
          c.status("LoadFirst") == "disabled" and c.raw() == "B,%s,C" % PACK and c.saves() == 0 and c.questions() == 0,
          "status=%s raw=%s saves=%d questions=%d" % (c.status("LoadFirst"), c.raw(), c.saves(), c.questions()))

    # 5. The pack's own persistent slot: foreign lines preserved, our line counts promotions
    c = C(["B", PACK, "C"], persistent="somebody-else v3 alpha\nbeta")
    slot = c.slot() or ""
    lines = slot.split("\n")
    check("5a slot: our line first, promotions=1 from=2 of=3", lines[0].startswith("SMRFixPack.LoadFirst v1 promotions=1 ")
          and "from=2 of=3" in lines[0], repr(lines[0]))
    check("5a slot: both foreign lines preserved verbatim", lines[1:] == ["somebody-else v3 alpha", "beta"], repr(lines[1:]))
    c.move_pack_last()
    c.ex("if SMRFixPack.LoadFirst then SMRFixPack.LoadFirst.promoted = nil; SMRFixPack.LoadFirst.Promote('desk') end")
    slot = c.slot() or ""
    lines = slot.split("\n")
    check("5b second promotion: promotions=2, foreign lines still intact, saved list PACK first",
          lines[0].startswith("SMRFixPack.LoadFirst v1 promotions=2 ") and lines[1:] == ["somebody-else v3 alpha", "beta"]
          and c.saved() == "%s,B,C" % PACK and c.saves() == 2,
          "%r saved=%s saves=%d" % (lines, c.saved(), c.saves()))
    c = C([PACK, "B"], persistent="somebody-else v3 alpha")
    check("5c already first: a foreign slot is not rewritten, no request",
          c.slot() == "somebody-else v3 alpha" and c.saves() == 0, "%r saves=%d" % (c.slot(), c.saves()))

    # 6. Dependencies
    c = C(["B", PACK, "A"], deps={PACK: ["A"]})
    check("6a own prerequisite A: saved PACK,B,A; queue hoists A first, PACK before B",
          c.saved() == "%s,B,A" % PACK and c.queue() == "A,%s,B" % PACK, "saved=%s queue=%s" % (c.saved(), c.queue()))
    c = C(["Z", PACK, "B"], mods + ["Z"], deps={"Z": [PACK]})
    check("6b Z requires the pack: saved PACK,Z,B; queue PACK,Z,B (Z unmoved relative to B)",
          c.saved() == "%s,Z,B" % PACK and c.queue() == "%s,Z,B" % PACK, "saved=%s queue=%s" % (c.saved(), c.queue()))

    # Audit item 2: list shapes
    c = C(["A", "B"])
    check("shape: pack absent from the list: raw untouched, no request, inactive 'not in the saved mod list'",
          c.raw() == "A,B" and c.saves() == 0 and c.status("LoadFirst") == "inactive"
          and "not in the saved mod list" in c.detail("LoadFirst"),
          "raw=%s saves=%d %s/%s" % (c.raw(), c.saves(), c.status("LoadFirst"), c.detail("LoadFirst")))
    c = C(["B", PACK, "B", "GHOST"])
    check("shape: duplicate B collapses to its first position, stale GHOST kept in place, one request",
          c.saved() == "%s,B,GHOST" % PACK and c.saves() == 1, "%s saves=%d" % (c.saved(), c.saves()))
    c = C(["B", PACK, PACK, "C"])
    check("shape: duplicate PACK collapses: PACK,B,C", c.saved() == "%s,B,C" % PACK, c.saved())
    c = C(["A", "B", PACK, "C", "D"], mods + ["D"])
    check("shape: five mods, pack third: others keep A,B,C,D order", c.saved() == "%s,A,B,C,D" % PACK, c.saved())
    import itertools
    bad = []
    for seed in itertools.permutations(["A", "B", "C", PACK]):
        c = C(list(seed))
        others = [x for x in seed if x != PACK]
        expected = list(seed) if seed[0] == PACK else [PACK, *others]
        want_saves = 0 if seed[0] == PACK else 1
        if c.saved().split(",") != expected or c.saves() != want_saves:
            bad.append((seed, c.saved(), c.saves()))
    check("shape: all 24 permutations of A,B,C,PACK keep the others' order; a save only when moved", not bad, bad[:3])

    # 7. Passage Network
    c = C([PN_ID, PACK], [PN_ID, PACK], loaded=[PN_ID, PACK], before_pack=PN_CLOBBER, extra_files=PN_FILES)
    check("7a PN before pack: VacuumWalks declines (inactive)", c.status("VacuumWalks") == "inactive",
          "%s / %s" % (c.status("VacuumWalks"), c.detail("VacuumWalks")))
    check("7a PN before pack: HubLocalAccess does not apply", c.status("HubLocalAccess") != "active",
          "%s / %s" % (c.status("HubLocalAccess"), c.detail("HubLocalAccess")))
    next_queue = c.queue()
    check("7a saved PN,PACK becomes PACK,PN; next queue PACK,PN", next_queue == "%s,%s" % (PACK, PN_ID),
          "saved=%s queue=%s" % (c.saved(), next_queue))
    order = next_queue.split(",")
    c2 = C(order, [PN_ID, PACK], loaded=order, before_pack=PN_CLOBBER if order[0] == PN_ID else None, extra_files=PN_FILES)
    if order[0] == PACK:
        c2.ex(PN_CLOBBER)
    check("7b next launch in that order: VacuumWalks active", c2.status("VacuumWalks") == "active",
          "%s / %s" % (c2.status("VacuumWalks"), c2.detail("VacuumWalks")))
    check("7b next launch in that order: HubLocalAccess active", c2.status("HubLocalAccess") == "active",
          "%s / %s" % (c2.status("HubLocalAccess"), c2.detail("HubLocalAccess")))
    check("7b next launch: LoadFirst already first, no write", c2.status("LoadFirst") == "active" and c2.saves() == 0,
          "status=%s saves=%d" % (c2.status("LoadFirst"), c2.saves()))

    # R1. Notice lifecycle with realistic chronology: startup threads finish BEFORE the later click
    c = C(["B", PACK, "C"], options={"LoadFirst": False})
    c.run_threads()
    c.toggle(True)
    c.run_threads()
    check("R1a cold option off, later opt-in: promotes and a notice is shown",
          c.saved() == "%s,B,C" % PACK and c.saves() == 1 and c.questions() == 1,
          "saved=%s saves=%d questions=%d" % (c.saved(), c.saves(), c.questions()))
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.toggle(False)
    c.move_pack_last()
    c.toggle(True)
    c.run_threads()
    check("R1b already-first boot, off, moved last, on: promotes and a notice is shown",
          c.saved() == "%s,B,C" % PACK and c.saves() == 1 and c.questions() == 1,
          "saved=%s saves=%d questions=%d" % (c.saved(), c.saves(), c.questions()))
    c = C(["B", PACK, "C"])
    c.run_threads()
    c.toggle(False)
    c.move_pack_last()
    c.toggle(True)
    c.run_threads()
    check("R1c promotion boot, off, moved last, on: a second notice for the second promotion",
          c.saves() == 2 and c.questions() == 2, "saves=%d questions=%d" % (c.saves(), c.questions()))
    c = C(["B", PACK, "C"])
    c.load_pack_file(MODULE)   # reload while the first notice thread is still waiting
    c.run_threads()
    check("R1d reload while a notice is pending: one box, not two", c.questions() == 1 and c.saves() == 1,
          "questions=%d saves=%d" % (c.questions(), c.saves()))

    # R2. Persistent slot: foreign bytes exact, including blank lines, prefix collisions, a full slot
    for tag, foreign in (("R2a", "alpha\n\nbeta\n"), ("R2b", "SMRFixPack.LoadFirstExtra payload")):
        c = C(["B", PACK, "C"], persistent=foreign)
        slot = c.slot() or ""
        tail = slot.partition("\n")[2]
        check("%s slot %r: our line then the foreign bytes exactly" % (tag, foreign[:24]),
              slot.split("\n")[0].startswith("SMRFixPack.LoadFirst v1 promotions=1 ") and tail == foreign and c.saves() == 1,
              "after=%r saves=%d" % (slot, c.saves()))
    full = "z" * 32768
    c = C(["B", PACK, "C"], persistent=full)
    check("R2c full valid slot: nothing written, nothing dropped, promotion made, log says the save could not be requested",
          c.slot() == full and c.saved() == "%s,B,C" % PACK and c.saves() == 0
          and c.log_has("could not be requested through this pack's persistent slot"),
          "slot_len=%d saved=%s saves=%d" % (len(c.slot() or ""), c.saved(), c.saves()))

    # R3. LoadAllMods edges
    stale = "SMRFixPack.LoadFirst.probe"
    c = C(["B", stale, PACK, "C"], account_load_all=True)
    check("R3a account flag with a stale probe id in the raw list: raw list untouched, no request",
          c.raw() == "B,%s,%s,C" % (stale, PACK) and c.saves() == 0, "raw=%s saves=%d" % (c.raw(), c.saves()))
    c = C(["B", stale, PACK, "C"])
    check("R3a normal list with a stale probe id: promoted, the stale id kept in place",
          c.saved() == "%s,B,%s,C" % (PACK, stale), c.saved())
    c = C(["z", PACK], [PACK, "z"], config_load_all=True)
    check("R3b config.LoadAllMods with the pack sorted first: diagnosed, inactive, no request",
          c.status("LoadFirst") == "inactive" and "LoadAllMods" in c.detail("LoadFirst") and c.saves() == 0,
          "%s / %s saves=%d" % (c.status("LoadFirst"), c.detail("LoadFirst"), c.saves()))
    c = C(["z", PACK], [PACK, "z"], account_load_all=True)
    check("R3c account flag with the pack sorted first: the STATED LIMIT holds — no write, wording names the loaded list",
          c.status("LoadFirst") == "active" and c.detail("LoadFirst").startswith("first in the list the game loads")
          and c.saves() == 0 and c.raw() == "z,%s" % PACK,
          "%s / %s saves=%d raw=%s" % (c.status("LoadFirst"), c.detail("LoadFirst"), c.saves(), c.raw()))

    # Engine: an order-only change never reloads (the sitting's S2 shape), shipped ModsReloadItems
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.move_pack_last()
    c.ex("function IsRealTimeThread() return true end; GetModsToLoad = function() return GetLoadingQueueShipped(GetModsEnabledByUser(), true) end")
    c.ex(RELOAD)
    c.ex("ModsReloadItems()")
    check("engine: same-visit off/on is order-only: ModsReloadItems returns early, running list unchanged, no promotion",
          c.raw() == "B,C,%s" % PACK and c.loaded() == "%s,B,C" % PACK and c.saves() == 0 and c.questions() == 0,
          "raw=%s running=%s saves=%d" % (c.raw(), c.loaded(), c.saves()))

    # R5D. The Paradox sync completion witness (kit payload) on the archived PdxTaskQueue: an
    # attempt is PASS only when its root and every child returned without error or cancellation
    def sync_case(**sim):
        c = C([PACK, "B", "C"])
        c.run_threads()
        c.load_witness(witness_text)
        for k, v in sim.items():
            if k == "behaviour":
                for i, b in v.items():
                    c.ex("SIM.behaviour[%d] = %r" % (i, b))
            else:
                c.ex("SIM.%s = %s" % (k, ("true" if v else "false") if isinstance(v, bool) else v))
        return c

    c = sync_case(children=2)
    c.login()
    state = c.drive()
    check("R5D1 root and two children returned: worker idle, queue 0, verdict COMPLETE, pass",
          state == "idle" and c.queued() == 0 and c.verdict() == "COMPLETE" and c.passes(),
          "state=%s queued=%d verdict=%s" % (state, c.queued(), c.verdict()))
    check("R5D1 the log carries one PUSH, START and END per task (root + 2 children = 3 each)",
          c.log_count("PUSH serial=") == 3 and c.log_count("START serial=") == 3 and c.log_count("END serial=") == 3
          and c.log_count("kind=root") >= 3 and c.log_count("kind=child parent=1") == 2,
          "push=%d start=%d end=%d" % (c.log_count("PUSH serial="), c.log_count("START serial="), c.log_count("END serial=")))
    c = sync_case(children=1, behaviour={1: "move-pack-last"})
    c.login()
    c.drive()
    moved = c.raw()
    c2 = C(moved.split(","))
    check("R5D1 a sync child that re-enables the pack leaves it last; the next boot promotes it again",
          moved == "B,C,%s" % PACK and c2.saved() == "%s,B,C" % PACK and c2.saves() == 1,
          "after sync=%s next boot=%s saves=%d" % (moved, c2.saved(), c2.saves()))
    c = sync_case(children=1, behaviour={1: "async"})
    c.login()
    state = c.drive()
    check("R5D2 a child with an outstanding async call: queue reads 0, verdict IN-FLIGHT, not pass",
          state == "async" and c.queued() == 0 and c.verdict() == "IN-FLIGHT" and not c.passes(),
          "state=%s queued=%d verdict=%s" % (state, c.queued(), c.verdict()))
    state = c.drive()
    check("R5D2 control: the call returns, verdict COMPLETE, pass",
          state == "idle" and c.verdict() == "COMPLETE" and c.passes(), "state=%s verdict=%s" % (state, c.verdict()))
    c = sync_case(children=2, behaviour={1: "async"})
    c.login()
    c.drive()          # child 1 is in flight, child 2 queued
    c.logout()         # OnMsg.PdxLogout clears the queue: child 2 never starts
    state = c.drive()  # child 1 returns
    check("R5D3 logout cleared an unstarted child: worker idle, queue 0, verdict CANCELLED, not pass",
          state == "idle" and c.queued() == 0 and c.verdict() == "CANCELLED" and not c.passes()
          and c.log_has("CLEAR clears=1 cancelled_unstarted=1"),
          "state=%s queued=%d verdict=%s" % (state, c.queued(), c.verdict()))
    c = sync_case(children=2, behaviour={2: "raise"})
    c.login()
    state = c.drive()
    check("R5D4 a child raised: queue 0, verdict FAILED, not pass; the error reached the queue's own sprocall",
          state == "idle" and c.queued() == 0 and c.verdict() == "FAILED" and not c.passes() and c.ev("#SPRO_ERRORS") == 1,
          "state=%s verdict=%s sprocall_errors=%s" % (state, c.verdict(), c.ev("#SPRO_ERRORS")))
    c = sync_case(children=2, behaviour={1: "errstring"})
    c.login()
    c.drive()
    check("R5D4 a child returned an error string: verdict FAILED, not pass",
          c.verdict() == "FAILED" and not c.passes(), c.verdict())
    c = sync_case(root_fetch_fails=True)
    c.login()
    state = c.drive()
    check("R5D5 the root scheduled nothing (the :1866-1868 failure shape): verdict COMPLETE-EMPTY, not pass on its own",
          state == "idle" and c.queued() == 0 and c.verdict() == "COMPLETE-EMPTY" and not c.passes(),
          "state=%s verdict=%s" % (state, c.verdict()))
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.load_witness(witness_text, install=False)
    c.login()                  # the root is queued before the witness installs
    c.install_witness()
    state = c.drive()
    check("R5D5 a root already queued when the witness installs is wrapped in place: verdict COMPLETE, pass",
          c.log_has("INSTALL ok=true note=wrapped_queued=1") and state == "idle" and c.verdict() == "COMPLETE" and c.passes(),
          "state=%s verdict=%s" % (state, c.verdict()))
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.load_witness(witness_text, install=False)
    c.ex("SIM.root_async = true")
    c.login()
    c.drive()                  # the root started and is inside its async call, unwrapped
    c.install_witness()
    state = c.drive()          # its children are pushed through the wrapper, without a seen root
    check("R5D5 the witness arrived after the root started: verdict UNWITNESSED, queue 0, not pass",
          state == "idle" and c.queued() == 0 and c.verdict() == "UNWITNESSED" and not c.passes()
          and c.log_count("kind=other parent=none sync_update=true") == 2,
          "state=%s verdict=%s" % (state, c.verdict()))
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.load_witness(witness_text, mode="unattended")
    c.run_threads()
    check("R5D5 no login in this process: the driver logs NO-ATTEMPT pass=false and quits",
          c.log_has("VERDICT verdict=NO-ATTEMPT pass=false") and c.ev("QUIT.calls") == 1,
          "quit=%s" % c.ev("QUIT.calls"))
    c = C([PACK, "B", "C"])
    c.run_threads()
    c.load_witness(witness_text, mode="unattended")
    c.ex("SIM.children = 2")
    c.login()
    c.drive()
    c.run_threads()
    check("R5D6 unattended driver after a complete attempt: logs VERDICT verdict=COMPLETE pass=true, the saved order, and quits once",
          c.log_has("AT_MENU VERDICT verdict=COMPLETE pass=true") and c.log_has("AT_MENU ORDER saved=%s,B,C" % PACK)
          and c.ev("QUIT.calls") == 1, "quit=%s" % c.ev("QUIT.calls"))
    c = sync_case(children=2)
    check("R5D6 sitting mode binds the Sync read slot; pressing it reports the verdict",
          c.ev("SLOTS['Sync read'] ~= nil") and c.ev("SLOTS['Sync read']().verdict") == "NO-ATTEMPT"
          and c.log_has("SLOT VERDICT verdict=NO-ATTEMPT"), c.ev("table.concat(LOG, ' | ')")[-200:])

    # R5E. Restoration for the sitting's leg E: after the last option click, under the kit's veto,
    # read back on a build without the module. The rejected OFF/readback/ON recipe is kept as R5E2.
    captured = ["Kit", "TrainHub", PACK, "OptIn", "RailShaft"]
    post = [PACK, "Kit", "TrainHub", "OptIn", "RailShaft"]
    kit_restore = ("for _, id in ipairs(table.icopy(AccountStorage.LoadMods)) do TurnModOff(id) end; "
                   "for _, id in ipairs(%s) do TurnModOn(id) end; SaveAccountStorage(1000)" % lua_list(captured))
    c = C(post, post, veto=True)      # option ON; the set leg's veto is in place before the pack loads
    c.run_threads()
    c.ex(kit_restore)                 # the set slot rewrites the captured order, requests the kit's save
    c.load_pack_file(MODULE)          # a Lua reload in the same process re-runs the file
    c.run_threads()
    c.toggle(True)                    # an Apply click with the option already ON
    c.run_threads()
    check("R5E1 vetoed restore with the option ON: the captured order survives a reload and an Apply click; one save (the kit's), no notice, LoadFirst disabled",
          c.raw() == ",".join(captured) and c.saves() == 1 and c.questions() == 0 and c.status("LoadFirst") == "disabled",
          "raw=%s saves=%d questions=%d status=%s" % (c.raw(), c.saves(), c.questions(), c.status("LoadFirst")))
    c = C(captured, post, options={"LoadFirst": False})
    c.run_threads()
    check("R5E2 the rejected recipe: an OFF readback keeps the captured order",
          c.raw() == ",".join(captured) and c.saves() == 0, "raw=%s saves=%d" % (c.raw(), c.saves()))
    c.toggle(True)
    check("R5E2 the rejected recipe: the final ON click promotes at once, so restoration must come after it",
          c.raw() == ",".join(post) and c.saves() == 1 and c.ev("SMRFixPack.LoadFirst.pending_notice") is True,
          "raw=%s saves=%d" % (c.raw(), c.saves()))
    c = C(captured, post)
    check("R5E3 the next feature-enabled boot on the restored order, option ON, promotes by design",
          c.saved() == ",".join(post) and c.saves() == 1, "saved=%s saves=%d" % (c.saved(), c.saves()))

    # pdxfetch (independent, shipped code): AsyncPdxGetAllSubscribedMods tests the page length
    # BEFORE the error, so a failed first page that comes back empty returns no error and
    # SyncPdxMods prints nothing: an empty attempt cannot be told from a failed fetch by the
    # game's own log line, which is why COMPLETE-EMPTY is never PASS.
    L2 = db.lua_runtime()
    L2.execute(db.ENGINE_SHIMS + TABLE_RETYPED)
    L2.execute("table.iappend = function(t, s) for _, v in ipairs(s) do t[#t + 1] = v end end; Pdx = { DefaultPlaysetId = 0 }")
    L2.execute("function AsyncPdxGetSubscribedMods(p) return 'Timeout', {} end")
    L2.execute(FETCH)
    err, mods = L2.eval("AsyncPdxGetAllSubscribedMods()")
    check("pdxfetch: a failed first page with an empty table returns no error and an empty list (ModManager.lua:%d-%d)" % (FETCH_A, FETCH_B),
          err is False and len(mods) == 0, "err=%r n=%d" % (err, len(mods)))
    L2.execute("function AsyncPdxGetSubscribedMods(p) if p.Page == 1 then return false, { { ModID = 'm1' } } end return false, {} end")
    err, mods = L2.eval("AsyncPdxGetAllSubscribedMods()")
    check("pdxfetch control: one subscribed mod is returned without error", err is False and len(mods) == 1, "err=%r n=%d" % (err, len(mods)))

    # Canary: metadata.lua loads under the metadata env, same declared properties + default_options
    L = db.lua_runtime()
    L.globals().META = (REPO / "metadata.lua").read_text(encoding="utf-8")
    base = subprocess.run(["git", "show", PRE_CANARY_META_REV + ":metadata.lua"], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout
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
    check("canary: metadata.lua loads under the metadata env and returns a ModDef", L.eval("DEF.class") == "ModDef")
    check("canary: declared property set = pre-canary set + default_options",
          set(keys.split(",")) == set(keys0.split(",")) | {"default_options"}, sorted(set(keys.split(",")) ^ set(keys0.split(","))))
    check("canary: the literal is in the tree file and leaks no global", CANARY in L.globals().META and L.eval("LEAK") is None)
    check("canary: the code list still starts 00_Core, 01_LoadFirst", L.eval(
        "(function() for i = 1, #DEF.props, 2 do if DEF.props[i] == 'code' then return DEF.props[i+1][1] .. ',' .. DEF.props[i+1][2] end end end)()")
        == "Code/00_Core.lua,Code/01_LoadFirst.lua")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", help="run one mutant verbosely: " + ", ".join(MUTANTS))
    ap.add_argument("--list", action="store_true", help="print the groups and their expected killers")
    args = ap.parse_args()
    if args.list:
        for g, ks in sorted(KILLERS.items()):
            print("%-6s killed by %s" % (g, ", ".join(sorted(ks))))
        print("independent groups (no killer by design): " + ", ".join(sorted(INDEPENDENT)))
        print("module mutants: " + ", ".join(MUTANTS))
        print("witness mutants (applied to %s): " % WITNESS + ", ".join(WITNESS_MUTANTS))
        return 0

    module_text = (REPO / MODULE).read_text(encoding="utf-8")
    witness_text = (REPO / WITNESS).read_text(encoding="utf-8")
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    if args.mutant:
        print("MUTANT", args.mutant, "(verbose)")
        rec = Recorder(verbose=True)
        if args.mutant in WITNESS_MUTANTS:
            run_cases(rec, module_text, mutate(witness_text, args.mutant, WITNESS_MUTANTS))
        else:
            run_cases(rec, mutate(module_text, args.mutant), witness_text)
        print("failed groups:", ", ".join(sorted(rec.failed_groups())) or "none")
        return 0

    print("=" * 78)
    print("LoadFirst desk controls — baseline then behavioural mutants (HEAD %s, game 1.1.1.405907, %s)" % (head, db.lua_version()))
    print("=" * 78)
    for rel in PACK_FILES + PN_FILES + [WITNESS]:
        print("INPUT", rel, sha((REPO / rel).read_text(encoding="utf-8")))
    print("SHIPPED %s PdxTaskQueue %s" % (PDX_LUA, ", ".join("%s %d-%d" % (n, a, b) for n, (_, a, b) in zip(PDX_METHOD_NAMES, PDX_METHODS))))
    print("SHIPPED %s ModEnvBlacklist %d-%d %s" % (MOD_LUA, BLACKLIST_START + 1, BLACKLIST_END + 1, sha(BLACKLIST.strip("\n"))))
    print("SHIPPED %s env block %d-%d %s" % (MOD_LUA, ENV_START + 1, ENV_END + 1, sha(ENV_BLOCK.strip("\n"))))
    print("SHIPPED %s WriteModPersistentData %d-%d, SetupEnv %d-%d, GetModsEnabledByUser %d-%d, ModsReloadItems %d-%d"
          % (MOD_LUA, STORAGE_A, STORAGE_B, SETUP_A, SETUP_B, ENABLED_A, ENABLED_B, RELOAD_A, RELOAD_B))
    print("SHIPPED %s queue %d-%d %s" % (MOD_LUA, QUEUE_START + 1, QUEUE_END + 1, sha(QUEUE.strip("\n") + "\n")))
    print("SHIPPED %s TurnModOn %d-%d TurnModOff %d-%d" % (UI_LUA, HELPERS[0][1], HELPERS[0][2], HELPERS[1][1], HELPERS[1][2]))
    print("SHIPPED Lua/Units/Colonist.lua StartShuttleLeg %d-%d" % (SS_A, SS_B))
    print("PN_DEFINITIONS", ",".join("%d-%d" % (a + 1, b + 1) for a, b in PN_HITS), "members=%d" % len(PN_HITS))
    print()
    print("BASELINE")
    base = Recorder(verbose=True)
    run_cases(base, module_text, witness_text)
    held = sum(1 for ok, _ in base.results if ok)
    print("BASELINE %d of %d demands held" % (held, len(base.results)))
    groups = sorted(base.groups())
    print()
    print("MUTANTS (each row: the groups whose demands FAILED under that mutant; witness-* mutate the kit payload)")
    kills = {g: set() for g in groups}
    for name in list(MUTANTS) + list(WITNESS_MUTANTS):
        rec = Recorder(verbose=False)
        if name in WITNESS_MUTANTS:
            run_cases(rec, module_text, mutate(witness_text, name, WITNESS_MUTANTS))
        else:
            run_cases(rec, mutate(module_text, name), witness_text)
        failed = rec.failed_groups()
        for g in failed:
            kills.setdefault(g, set()).add(name)
        print("  %-15s fails %2d of %2d demands; groups: %s" % (name, sum(1 for ok, _ in rec.results if not ok),
              len(rec.results), ", ".join(sorted(failed)) or "none"))
    print()
    print("CONTROL VERDICT per group (expected killers must all kill; a group with no killer at all is vacuous)")
    problems = []
    for g in groups:
        if g in INDEPENDENT:
            print("  %-6s independent by design (%s)" % (g, "not a module behaviour"))
            continue
        expected = KILLERS.get(g, set())
        missing = expected - kills[g]
        line = "  %-6s killed by: %-45s expected: %s" % (g, ", ".join(sorted(kills[g])) or "NONE", ", ".join(sorted(expected)))
        if not kills[g]:
            problems.append("%s: VACUOUS, no mutant makes it fail" % g)
            line += "  <-- VACUOUS"
        elif missing:
            problems.append("%s: expected killer(s) did not kill: %s" % (g, ", ".join(sorted(missing))))
            line += "  <-- expected killer missing"
        if not expected:
            problems.append("%s: no killers declared" % g)
            line += "  <-- undeclared"
        print(line)
    print()
    print("RESULT baseline %d/%d held; %d group(s), %d independent; control problems: %d"
          % (held, len(base.results), len(groups), len([g for g in groups if g in INDEPENDENT]), len(problems)))
    for p in problems:
        print("   -", p)
    return 0 if held == len(base.results) and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
