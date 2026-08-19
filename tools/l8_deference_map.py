#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""L8 (adversarial / hostile modder) — the DEFERENCE census.

WHY THIS EXISTS
    `00_Core.lua:4-6` states the pack's first design goal in its own words:

        "Mod-compatible: fixes prefer wrapping/chaining originals over
         replacement, so other mods that hook the same functions keep working."

    That is a claim about all 75 modules and nothing has ever tested it. It is
    the load-bearing claim for this whole lens, because it decides what happens
    when a foreign mod patches what we patch:

      * a CHAINING patch that captured the live value adopts a foreign mod that
        loaded BEFORE us and calls through to it — their fix survives ours;
      * a FULL REPLACEMENT installed over that same foreign patch DISCARDS it
        silently — no call-through, no log line, no way for anyone to notice.

    `EF-054` records the owner's design intent (load first, be innermost, let a
    later mod's replacement win cleanly). ⛔ That intent is only achievable for
    sites that chain. It says nothing about sites that replace, and inter-mod
    order is the player's enable order, which nobody can set (`ModManager.lua:36`).

WHAT IT MEASURES, AND THE ONE DIRECTION THAT IS SOUND
    For every patch install site the pack owns, does the module anywhere
    reference the PREVIOUS value of that same symbol?

      ⇒ NO reference anywhere in the file  =>  the patch CANNOT chain. Airtight:
        a call-through needs the prior value to be textually reachable, and a
        module cannot call what it never names.
      ⇒ A reference exists  =>  it MIGHT chain. NOT airtight — the tool reports
        these as `reads-prior` and every one is read at its lines by hand.

    ⛔ The tool therefore emits a LOWER BOUND on replacements, never an upper
    bound on chaining. That asymmetry is deliberate and is the only reason the
    numbers below can be trusted without reading all 76 files twice.

    Alias resolution is done first, per link 1's rule: modules capture targets as
    file-locals (`local C = rawget(_G, "Colonist")`) and then write
    `function C:Idle`, which a plain grep cannot join across files.

USAGE
    python tools/l8_deference_map.py
    python tools/l8_deference_map.py --selftest    # the control, run it first
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(ROOT, "Code")

# --- alias forms this pack actually uses -----------------------------------
RE_ALIAS = [
    re.compile(r'^\s*local\s+(\w+)\s*=\s*rawget\s*\(\s*_G\s*,\s*"([\w.]+)"\s*\)'),
    re.compile(r'^\s*local\s+(\w+)\s*=\s*_G\.(\w+)\s*$'),
    re.compile(r'^\s*local\s+(\w+)\s*=\s*g_Classes\.(\w+)'),
    re.compile(r'^\s*local\s+(\w+)\s*=\s*rawget\s*\(\s*g_Classes\s*,\s*"(\w+)"\s*\)'),
    # ⚠️ the fifth form, and the first pass of this tool did not have it: several
    # modules alias by a BARE global read inside apply (`local C = Community`,
    # Fix_DomeOverviewHighlight.lua:25). Without it the census printed unresolved
    # holders (`C.UICommandCenterStatUpdate`) that cannot be joined across files —
    # link 1's exact failure, reproduced here before being fixed.
    # An ALL_CAPS right-hand side is a file constant (FIX_ID), never a class.
    re.compile(r'^\s*local\s+(\w+)\s*=\s*([A-Z][a-z]\w*)\s*$'),
]
RE_FIXID = re.compile(r'^\s*local\s+(\w*FIX_ID\w*)\s*=\s*"([^"]+)"')

# --- install shapes --------------------------------------------------------
RE_FN_GLOBAL = re.compile(r'^\s*function\s+([A-Z]\w*)\s*\(')            # function Name(
RE_FN_METHOD = re.compile(r'^\s*function\s+(\w+)\s*[:.]\s*(\w+)\s*\(')  # function C:M( / C.M(
RE_ASSIGN_METHOD = re.compile(r'^\s*(\w+)\s*\.\s*(\w+)\s*=\s*(.+)$')    # C.M = expr
RE_SETGLOBAL = re.compile(r'SMRFixPack\.SetGlobal\s*\(\s*"(\w+)"')
RE_STRIP_COMMENT = re.compile(r'^\s*--')

# a target name that is really a local table of ours, not a game class
# ⛔ `OnMsg` is here for a reason the first pass of this tool got wrong: `function
# OnMsg.PostLoadGame()` is an ADDITIVE message registration (cthreads.lua:6 —
# `__newindex` appends), not a patch of anything. Counting it scored 6 message
# handlers as "full replacements" and inflated the headline number.
NOT_A_CLASS = {"SMRFixPack", "OnMsg", "ctx", "opts", "self", "def", "entry", "t", "copy"}


def strip_comments(lines):
    """Blank out full-line comments only. Inline `--` inside strings is why this
    does NOT try to strip trailing comments: over-stripping is how link 6's
    extractors were wrong three times in one sitting."""
    return ["" if RE_STRIP_COMMENT.match(l) else l for l in lines]


def scan_file(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read().splitlines()
    lines = strip_comments(raw)
    body = "\n".join(lines)

    aliases = {}
    for l in lines:
        for rx in RE_ALIAS:
            m = rx.match(l)
            if m:
                aliases[m.group(1)] = m.group(2)

    sites = []

    # 1 . global function replacement by bare `function Name(`
    for i, l in enumerate(lines, 1):
        m = RE_FN_GLOBAL.match(l)
        if m and m.group(1) not in aliases:
            sites.append(("global", m.group(1), m.group(1), i, "function Name()"))

    # 2 . global replacement through the pack's own helper
    for i, l in enumerate(lines, 1):
        m = RE_SETGLOBAL.search(l)
        if m:
            sites.append(("global", m.group(1), m.group(1), i, "SetGlobal()"))

    # 3 . class method by `function C:M(` / `function C.M(`
    for i, l in enumerate(lines, 1):
        m = RE_FN_METHOD.match(l)
        if m:
            holder, meth = m.group(1), m.group(2)
            if holder in NOT_A_CLASS:
                continue
            cls = aliases.get(holder, holder)
            sites.append(("method", "%s.%s" % (cls, meth), meth, i, "function C:M()"))

    # 4 . class method by assignment `C.M = expr`
    for i, l in enumerate(lines, 1):
        m = RE_ASSIGN_METHOD.match(l)
        if m:
            holder, meth, rhs = m.group(1), m.group(2), m.group(3)
            if holder in NOT_A_CLASS or holder not in aliases:
                continue
            if rhs.strip().startswith("=") or "==" in l.split("=")[0]:
                continue
            cls = aliases.get(holder, holder)
            sites.append(("method", "%s.%s" % (cls, meth), meth, i, "C.M = expr"))

    # --- does the file anywhere reference the PRIOR value of that symbol? ----
    # ⛔ The install sites themselves must not count as references to the prior
    # value: `function C:Idle()` matches a naive `C[.:]Idle(` call pattern and
    # would score every replacement as chaining — i.e. it would invert the whole
    # census. The selftest case `local C = rawget(_G,"Colonist") function C:Idle() end`
    # exists to catch exactly that, and it did.
    search_body = "\n".join(
        re.sub(r'^(\s*)function\s+\w+\s*[.:]\s*\w+\s*\(', r'\1--INSTALL-SITE(', l)
        for l in lines)

    out = []
    seen = set()
    for kind, target, short, line, shape in sites:
        key = (kind, target)
        if key in seen:
            continue
        seen.add(key)
        if kind == "global":
            prior = [
                r'rawget\s*\(\s*_G\s*,\s*"%s"\s*\)' % re.escape(short),
                r'_G\.%s\b(?!\s*=)' % re.escape(short),
            ]
        else:
            cls, meth = target.rsplit(".", 1)
            holders = [h for h, c in aliases.items() if c == cls] + [cls]
            prior = []
            for h in holders:
                prior.append(r'=\s*[^\n]*\b%s\s*[.:]\s*%s\b' % (re.escape(h), re.escape(meth)))
                prior.append(r'rawget\s*\(\s*%s\s*,\s*"%s"\s*\)' % (re.escape(h), re.escape(meth)))
                prior.append(r'\b%s\s*[.:]\s*%s\s*\(' % (re.escape(h), re.escape(meth)))
        hit = any(re.search(p, search_body) for p in prior)
        out.append((kind, target, line, shape, "reads-prior" if hit else "REPLACES"))
    return out


SELFTEST = [
    # (source, expected (kind, target, verdict) set)
    ('function Foo(a) return a end',
     {("global", "Foo", "REPLACES")}),
    ('local o = rawget(_G, "Foo")\nfunction Foo(a) return o(a) end',
     {("global", "Foo", "reads-prior")}),
    ('local C = rawget(_G, "Colonist")\nfunction C:Idle() end',
     {("method", "Colonist.Idle", "REPLACES")}),
    ('local C = rawget(_G, "Colonist")\nlocal p = C.Idle\nfunction C:Idle() return p(self) end',
     {("method", "Colonist.Idle", "reads-prior")}),
    ('local C = rawget(_G, "Drone")\nC.Fly = function(self) end',
     {("method", "Drone.Fly", "REPLACES")}),
    ('SMRFixPack.SetGlobal("Bar", function() end)',
     {("global", "Bar", "REPLACES")}),
    ('local w = rawget(_G, "Bar")\nSMRFixPack.SetGlobal("Bar", function() return w() end)',
     {("global", "Bar", "reads-prior")}),
    # a comment naming the prior value must NOT count as a capture
    ('-- we deliberately do not call rawget(_G, "Baz")\nfunction Baz() end',
     {("global", "Baz", "REPLACES")}),
    # an OnMsg registration is ADDITIVE and is not a patch site at all
    ('function OnMsg.PostLoadGame() end', set()),
    # the fifth alias form: a bare global read, indented inside apply
    ('\t\tlocal C = Community\n\t\tfunction C:Refresh() end',
     {("method", "Community.Refresh", "REPLACES")}),
    # an ALL_CAPS right-hand side is a constant, never a class alias
    ('local FIX_ID = "Thing"\nlocal X = FIX_ID\nfunction Foo() end',
     {("global", "Foo", "REPLACES")}),
]


def selftest():
    import tempfile
    ok = 0
    for src, expect in SELFTEST:
        fd, p = tempfile.mkstemp(suffix=".lua")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(src)
        got = {(k, t, v) for k, t, _l, _s, v in scan_file(p)}
        os.unlink(p)
        if got == expect:
            ok += 1
        else:
            print("  FAIL  %-60s" % src.replace("\n", " | "))
            print("        expected %s" % sorted(expect))
            print("        got      %s" % sorted(got))
    print("selftest: %d/%d cases pass" % (ok, len(SELFTEST)))
    return 0 if ok == len(SELFTEST) else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()

    files = sorted(f for f in os.listdir(CODE) if f.endswith(".lua"))
    rows = []
    for f in files:
        for r in scan_file(os.path.join(CODE, f)):
            rows.append((f,) + r)

    print("=" * 92)
    print("L8 DEFERENCE CENSUS — does each patch site reference the PRIOR value of its target?")
    print("  %d Code/*.lua scanned. REPLACES is AIRTIGHT (cannot chain what it never names)." % len(files))
    print("  reads-prior is a CANDIDATE only and is read by hand — see the artifact.")
    print("=" * 92)

    for kind in ("global", "method"):
        sub = [r for r in rows if r[1] == kind]
        rep = [r for r in sub if r[5] == "REPLACES"]
        print()
        print("--- %s patch sites: %d total, %d REPLACES, %d reads-prior"
              % (kind, len(sub), len(rep), len(sub) - len(rep)))
        for f, _k, target, line, shape, verdict in sorted(sub, key=lambda r: (r[5], r[0])):
            flag = "REPLACES  " if verdict == "REPLACES" else "reads-prior"
            print("  %s %-34s %-30s %s:%d  (%s)" % (flag, target, "", f, line, shape))

    print()
    print("=" * 92)
    print("TOTALS  %d patch sites  |  %d REPLACES  |  %d reads-prior"
          % (len(rows), sum(1 for r in rows if r[5] == "REPLACES"),
             sum(1 for r in rows if r[5] == "reads-prior")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
