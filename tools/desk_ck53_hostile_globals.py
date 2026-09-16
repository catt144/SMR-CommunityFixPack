#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Desk control for checklist 53's hardening rows 1 + 2 (built 2026-09-16).

Loads Code/00_Core.lua VERBATIM under lupa, once per seeded _G, with the file
inside its own pcall (pdofile, lib.lua:242-251), then registers two throwaway
fixes and exercises every veto/override read: Register, WhenActive, DataPatch's
runner and OptionEnabled. Each case states the outcome it requires.

Supersedes tools/l8_hostile_input.py for these rows: that harness loads modules
deleted since (DustDevilSpawnGate, MeteorFrequency) and measures throws only.

FALSIFY: `--src <path>` loads another copy of 00_Core. Run it against the
pre-fix body and the hostile cases must FAIL while the controls PASS:
    git show c0e3dcc:Code/00_Core.lua > <scratch>/core_old.lua
    python tools/desk_ck53_hostile_globals.py --src <scratch>/core_old.lua
Exit status: 0 when every case passes, 1 otherwise.
"""

import os
import sys

try:
    import lupa
except ImportError:  # pragma: no cover
    sys.exit("desk_ck53_hostile_globals: needs `lupa` (pip install lupa)")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(ROOT, "Code", "00_Core.lua")

BOOT = r"""
SIM = { log = {} }
function ModLog(msg) SIM.log[#SIM.log + 1] = msg end
SIM_msgs = {}
OnMsg = setmetatable({}, { __newindex = function(_, name, fn)
    local t = SIM_msgs[name] or {}
    SIM_msgs[name] = t
    t[#t + 1] = fn
end })
-- cthreads.lua:15-21: Msg calls handlers through procall, which swallows.
function Msg(name, ...)
    for _, fn in ipairs(SIM_msgs[name] or {}) do
        local ok, err = pcall(fn, ...)
        if not ok then SIM.log[#SIM.log + 1] = "SIMERROR " .. tostring(err) end
    end
end
function CreateRealTimeThread() end
function RealTime() return 0 end
function Sleep() end
function Untranslated(s) return s end
CurrentModOptions = false
Mods = false
DataLoaded = false
"""

# Runs after the core loaded. Every read is pcall'd so one throw is reported
# as that check's failure instead of ending the case.
PROBE = r"""
local R = {}
local function try(name, fn)
    local ok, v = pcall(fn)
    if ok then R[name] = v else R[name] = "THREW: " .. tostring(v) end
end
try("registry", function() return type(SMRFixPack) == "table" and type(SMRFixPack.fixes) == "table" and type(SMRFixPack.order) == "table" end)
try("regA", function() SMRFixPack.Register("A", { title = "A", apply = function() end }); return SMRFixPack.fixes.A.status end)
try("regB", function() SMRFixPack.Register("B", { title = "B", apply = function() end }); return SMRFixPack.fixes.B.status end)
try("whenA", function()
    local ran = false
    SMRFixPack.WhenActive("A", function() ran = true end)()
    return ran
end)
try("datapatchA", function()
    local ran = false
    local run = SMRFixPack.DataPatch("A", { pass = function() ran = true end })
    Msg("ClassesBuilt")
    return ran
end)
try("optA", function() return SMRFixPack.OptionEnabled("A") end)
try("list", function() SMRFixPack.ListFixes(); return true end)
return R
"""

CASES = [
    # label, seed, {check: required value}, log substring required (or None), control?
    ("CONTROL nothing set", "",
     {"registry": True, "regA": "active", "regB": "active", "whenA": True,
      "datapatchA": True, "optA": False, "list": True}, None, True),
    ("CONTROL documented veto {A=true}", 'SMRFixPack_Disabled = { A = true }',
     {"regA": "disabled", "regB": "active", "whenA": False, "datapatchA": False}, None, True),
    ("CONTROL documented optional {A=true}", 'SMRFixPack_Optional = { A = true }',
     {"regA": "active", "optA": True}, None, True),
    ("CONTROL metatable default vetoes A", 'SMRFixPack_Disabled = setmetatable({}, {__index = function(_, k) return k == "A" end})',
     {"regA": "disabled", "regB": "active", "whenA": False}, None, True),
    ("SMRFixPack_Disabled = true", 'SMRFixPack_Disabled = true',
     {"registry": True, "regA": "active", "regB": "active", "whenA": True, "datapatchA": True},
     "ignored SMRFixPack_Disabled (boolean)", False),
    ('SMRFixPack_Disabled = "yes"', 'SMRFixPack_Disabled = "yes"',
     {"regA": "active", "regB": "active"}, "ignored SMRFixPack_Disabled (string)", False),
    ("SMRFixPack_Disabled with throwing __index", 'SMRFixPack_Disabled = setmetatable({}, {__index = function() error("hostile") end})',
     {"regA": "active", "regB": "active", "whenA": True, "datapatchA": True},
     "SMRFixPack_Disabled could not be read", False),
    ("SMRFixPack_Optional = true", 'SMRFixPack_Optional = true',
     {"regA": "active", "optA": False}, "ignored SMRFixPack_Optional (boolean)", False),
    ("SMRFixPack_Optional with throwing __index", 'SMRFixPack_Optional = setmetatable({}, {__index = function() error("hostile") end})',
     {"regA": "active", "optA": False}, None, False),
    ("SMRFixPack = true", 'SMRFixPack = true',
     {"registry": True, "regA": "active", "regB": "active", "list": True},
     "ignored SMRFixPack (boolean)", False),
    ("SMRFixPack = {} (shim)", 'SMRFixPack = {}',
     {"registry": True, "regA": "active", "datapatchA": True, "list": True}, None, False),
    ('SMRFixPack = {fixes = "x"} (mistyped)', 'SMRFixPack = { fixes = "x", order = 5 }',
     {"registry": True, "regA": "active", "list": True}, None, False),
]


def lua_long(src):
    n = 0
    while ("]" + "=" * n + "]") in src:
        n += 1
    return "[" + "=" * n + "[\n" + src + "]" + "=" * n + "]"


def load_core(lua, src):
    lua.execute("SIM_chunk = " + lua_long(src))
    return lua.eval('(function() local fn, e = load(SIM_chunk, "00_Core.lua") '
                    'if not fn then return "COMPILE: " .. tostring(e) end '
                    'local ok, e2 = pcall(fn) return ok or tostring(e2) end)()')


def run_case(src, seed):
    lua = lupa.LuaRuntime(unpack_returned_tuples=True)
    lua.execute(BOOT)
    if seed:
        lua.execute(seed)
    loaded = load_core(lua, src)
    res = lua.execute(PROBE)
    got = {k: res[k] for k in res.keys()}
    log = [lua.eval("SIM.log")[i] for i in range(1, int(lua.eval("#SIM.log")) + 1)]
    return loaded, got, log


def reload_case(src):
    """Regression: a Lua reload in the same process keeps one registry, one order
    entry per id, and the data_edited memo (00_Core's documented lifetimes)."""
    lua = lupa.LuaRuntime(unpack_returned_tuples=True)
    lua.execute(BOOT)
    load_core(lua, src)
    lua.execute('SMRFixPack.Register("A", {title="A", apply=function() end}); SMRFixPack.data_edited.A = true; SIM_first = SMRFixPack')
    load_core(lua, src)
    lua.execute('SMRFixPack.Register("A", {title="A", apply=function() end})')
    return (lua.eval("SIM_first == SMRFixPack") and int(lua.eval("#SMRFixPack.order")) == 1
            and lua.eval("SMRFixPack.data_edited.A == true"))


def main():
    src_path = DEFAULT_SRC
    if "--src" in sys.argv:
        src_path = sys.argv[sys.argv.index("--src") + 1]
    with open(src_path, encoding="utf-8") as f:
        src = f.read()
    print("source: %s" % src_path)
    passed = failed = 0
    for label, seed, want, log_need, control in CASES:
        loaded, got, log = run_case(src, seed)
        bad = []
        if loaded is not True:
            bad.append("file load: %s" % loaded)
        for k, v in want.items():
            if got.get(k) != v:
                bad.append("%s = %r, want %r" % (k, got.get(k), v))
        if log_need and not any(log_need in line for line in log):
            bad.append("log lacks %r" % log_need)
        errs = [line for line in log if line.startswith("SIMERROR")]
        if errs:
            bad.append("handler error: %s" % errs[0])
        tag = "CONTROL" if control else "HOSTILE"
        if bad:
            failed += 1
            print("FAIL  [%s] %s" % (tag, label))
            for b in bad:
                print("        %s" % b)
        else:
            passed += 1
            print("PASS  [%s] %s" % (tag, label))
    if reload_case(src):
        passed += 1
        print("PASS  [CONTROL] Lua reload keeps registry, single order entry, data_edited memo")
    else:
        failed += 1
        print("FAIL  [CONTROL] Lua reload keeps registry, single order entry, data_edited memo")
    print("%d passed, %d failed, %d cases" % (passed, failed, passed + failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
