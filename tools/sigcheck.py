#!/usr/bin/env python3
"""Compare every function this pack replaces against the SHIPPED signature.

Written 2026-09-08, immediately after F115: `Fix_LandscapeUnitFilter` replaced
`LandscapeForEachUnit(mark, callback, ...)` while game 1.1.0 had changed it to
`LandscapeForEachUnit(map, mark, callback, ...)`. Every argument arrived one
slot late and the module threw on the first landscaping site -- while reporting
`applied`, because its self-check only asked whether the NAME existed.

⛔ THE GAP THIS TOOL EXISTS TO CLOSE. The 1.1.0 sweep behind F113 checked 106
global call-names and 174 method names. Names. A NAME SWEEP CANNOT SEE AN ARITY
CHANGE -- the name is still there, which is exactly why the module applied. This
is the same failure shape EF-078 recorded when path specs were verified by their
last segment's NAME instead of as a path, and that one made the desk audit wrong
by 5. Check the THING, not its label.

    python tools/sigcheck.py                    # compare against the live source
    python tools/sigcheck.py --src <path>       # point at another ModTools/Src
    python tools/sigcheck.py --all              # include matches, not just problems

WHAT IT REPORTS
  MISMATCH   our parameter list differs from the shipped one -- read every one
  ABSENT     we define a name the shipped tree no longer declares anywhere
  MULTI      several shipped declarations share the name; shown for a human
  OK         parameter lists agree

⚠️ WHAT IT CANNOT DECIDE, AND MUST NOT BE READ AS DECIDING. A matching arity is
NOT proof a replacement is still correct: a same-named, same-arity function
whose BODY changed is invisible here, exactly as it is to the runtime
self-checks. This narrows the search; it does not clear anything. And a
MISMATCH on a wrapper that forwards with `...` may still be harmless -- read
the site.
"""

import argparse
import os
import re
import sys

DEFAULT_SRC = r"A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(HERE, "Code")

# `function Class:Method(a, b)` / `function Class.Method(a)` / `function Name(a)`
DEF_METHOD = re.compile(r"^\s*function\s+([A-Za-z_][\w.]*)\s*([:.])\s*([A-Za-z_]\w*)\s*\(([^)]*)\)")
DEF_GLOBAL = re.compile(r"^\s*function\s+([A-Za-z_]\w*)\s*\(([^)]*)\)")
# `local C = Colonist` / `local C = rawget(_G, "Colonist")`
ALIAS = re.compile(r"^\s*local\s+([A-Za-z_]\w*)\s*=\s*(?:rawget\s*\(\s*_G\s*,\s*[\"']([\w]+)[\"']\s*\)|([A-Z][\w]*))\s*$")

# names that are ours, not the game's
OURS = ("SMRFixPack", "OnMsg", "SMRTest", "ctx")


def params(s):
    out = [p.strip() for p in s.split(",")]
    return [p for p in out if p]


def scan_source(src):
    """name -> list of (paramlist, file, line). Indexed by bare method/global name."""
    table = {}
    for root, _dirs, files in os.walk(src):
        for fn in files:
            if not fn.endswith(".lua"):
                continue
            path = os.path.join(root, fn)
            try:
                fh = open(path, "r", encoding="utf-8", errors="replace")
            except OSError:
                continue
            with fh:
                for n, line in enumerate(fh, 1):
                    m = DEF_METHOD.match(line)
                    if m:
                        cls, _sep, meth, ps = m.groups()
                        rel = os.path.relpath(path, src)
                        table.setdefault(meth, []).append((cls, params(ps), rel, n))
                        continue
                    m = DEF_GLOBAL.match(line)
                    if m:
                        name, ps = m.groups()
                        rel = os.path.relpath(path, src)
                        table.setdefault(name, []).append((None, params(ps), rel, n))
    return table


def scan_pack():
    """Our replacement sites: (file, line, cls_or_None, name, params)."""
    sites = []
    for fn in sorted(os.listdir(CODE)):
        if not fn.endswith(".lua"):
            continue
        path = os.path.join(CODE, fn)
        aliases = {}
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
        for line in lines:
            m = ALIAS.match(line)
            if m:
                aliases[m.group(1)] = m.group(2) or m.group(3)
        for n, line in enumerate(lines, 1):
            m = DEF_METHOD.match(line)
            if m:
                cls, _sep, meth, ps = m.groups()
                if cls.split(".")[0] in OURS:
                    continue
                sites.append((fn, n, aliases.get(cls, cls), meth, params(ps)))
                continue
            m = DEF_GLOBAL.match(line)
            if m:
                name, ps = m.groups()
                if name in OURS or name.startswith("OnMsg"):
                    continue
                sites.append((fn, n, None, name, params(ps)))
    return sites


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--all", action="store_true", help="also print OK rows")
    a = ap.parse_args()

    if not os.path.isdir(a.src):
        print("source tree not found: %s" % a.src)
        return 2

    shipped = scan_source(a.src)
    sites = scan_pack()

    counts = {"MISMATCH": 0, "ABSENT": 0, "MULTI": 0, "OK": 0}
    rows = []
    for fn, ln, cls, name, ours in sites:
        cands = shipped.get(name, [])
        if not cands:
            counts["ABSENT"] += 1
            rows.append(("ABSENT", fn, ln, cls, name, ours, None, ""))
            continue
        # prefer a declaration on the same class
        same = [c for c in cands if cls and c[0] == cls]
        pool = same or cands
        # A trailing `...` on OUR side is the pack's deliberate forwarding
        # convention (FIX_POLICY wrapping) and is NOT a mismatch. What matters
        # is whether the FIXED leading parameters still line up POSITIONALLY:
        # F115 was `(mark, callback, ...)` against a shipped
        # `(map, mark, callback, ...)` -- same trailing vararg, every argument
        # one slot late. Compare names by position, not lengths.
        def fixed(ps):
            return [p for p in ps if p != "..."]
        ours_f = fixed(ours)
        ok = None
        for c in pool:
            theirs_f = fixed(c[1])
            n = min(len(ours_f), len(theirs_f))
            shifted = any(ours_f[i] != theirs_f[i] for i in range(n))
            # we drop a fixed parameter the game still passes, and we have no
            # vararg to catch it => arguments are silently lost
            short = len(ours_f) < len(theirs_f) and "..." not in ours
            if not shifted and not short:
                ok = c
                break
        if ok:
            counts["OK"] += 1
            if a.all:
                rows.append(("OK", fn, ln, cls, name, ours, ok[1],
                             "%s:%d" % (ok[2], ok[3])))
            continue
        best = pool[0]
        kind = "MISMATCH" if len(pool) == 1 or same else "MULTI"
        counts[kind] += 1
        alts = "; ".join("%s(%s) @%s:%d" % (c[0] or "<global>", ", ".join(c[1]), c[2], c[3])
                         for c in pool[:4])
        rows.append((kind, fn, ln, cls, name, ours, best[1], alts))

    order = {"MISMATCH": 0, "ABSENT": 1, "MULTI": 2, "OK": 3}
    rows.sort(key=lambda r: (order[r[0]], r[1], r[2]))

    for kind, fn, ln, cls, name, ours, theirs, note in rows:
        target = ("%s:%s" % (cls, name)) if cls else name
        print("%-9s %s:%d" % (kind, fn, ln))
        print("            ours    %s(%s)" % (target, ", ".join(ours)))
        if theirs is not None:
            print("            shipped %s(%s)" % (name, ", ".join(theirs)))
        if note:
            print("            %s" % note)

    print("=" * 78)
    print("%d replacement site(s): %d MISMATCH, %d ABSENT, %d MULTI, %d OK" % (
        len(sites), counts["MISMATCH"], counts["ABSENT"], counts["MULTI"], counts["OK"]))
    print("An OK is NOT a clearance: a same-name, same-arity function whose BODY")
    print("changed is invisible here, exactly as it is to the runtime self-checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
