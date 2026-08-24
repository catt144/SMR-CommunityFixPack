#!/usr/bin/env python3
"""Harvest every `{ class = C, method = M }` target the pack declares.

Why this is a tool and not a hand-typed list: the pack declares these across
~60 modules and the count drifts with every fix. `EF-066` said "~60"; the real
figure the first run of this script produced was 105 entries / 100 distinct
(class, method) pairs. A hand-typed list is a silent under-sweep, and an
under-sweep is the expensive error — a wrap wrongly believed reachable stays
broken forever.

WHAT A TARGET IS, EXACTLY. `SMRFixPack.Require` (Code/00_Core.lua:117-166) takes
a spec list; a `{ class, method }` entry is a SHAPE SELF-CHECK ("this function
still exists on this class"). ⚠️ That is NOT the same as "the module wraps it":
some modules require a function they only READ. The sweep in
TestKit/Code/64_Probes_Wave14.lua is deliberately built on the Require targets
anyway, because the runtime test it applies is self-limiting — a target the pack
never wrote to still resolves identically on every descendant, so it reports
clean. Sweeping the superset costs nothing and cannot miss a wrap.

⛔ NOT harvested: `{ global = ... }` (SetGlobal replacements — no class
dispatch involved), `{ class = ... }` with no method (existence checks),
`{ path = ... }`, `{ test = ... }`. `changed_class = ...` is a DataChanged
re-run key, not a target, and the class-name regex excludes it by word boundary.

Usage:
    python tools/harvest_wrap_targets.py            # counts only
    python tools/harvest_wrap_targets.py --list     # module / Class.method
    python tools/harvest_wrap_targets.py --lua      # the Lua table body
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(HERE, "Code")


def strip_comments(text):
    """Remove Lua comments without touching string literals.

    Needed because Code/00_Core.lua documents the spec shapes in a comment
    block — `-- { class = "Building", method = "X" }` — and a naive grep
    harvests the documentation as a target.
    """
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("--", i):
            m = re.match(r"--\[(=*)\[", text[i:])
            if m:                                   # long comment
                close = "]" + m.group(1) + "]"
                j = text.find(close, i)
                i = n if j < 0 else j + len(close)
            else:                                   # line comment
                j = text.find("\n", i)
                i = n if j < 0 else j
                out.append("\n")
            continue
        if text[i] == '"':                          # keep string literals whole
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    j += 1
                    break
                j += 1
            out.append(text[i:j])
            i = j
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def require_blocks(src):
    """Yield the argument text of each SMRFixPack.Require( ... ) call."""
    for m in re.finditer(r"SMRFixPack\.Require\s*\(", src):
        i = m.end()
        depth, j = 1, m.end()
        while j < len(src) and depth:
            c = src[j]
            if c in "({[":
                depth += 1
            elif c in ")}]":
                depth -= 1
            j += 1
        yield src[i:j - 1]


def entries(block):
    """Yield each `{ ... }` spec entry inside the block's spec table.

    Depth-aware, so multi-line entries (Fix_DestroyedTunnels, Fix_BombardmentSpread)
    are harvested whole rather than truncated at the newline.
    """
    k = block.find("{")
    if k < 0:
        return
    depth, start = 0, None
    for j in range(k, len(block)):
        c = block[j]
        if c == "{":
            depth += 1
            if depth == 2:
                start = j
        elif c == "}":
            if depth == 2 and start is not None:
                yield block[start:j + 1]
                start = None
            depth -= 1


def harvest():
    """-> list of (module, class, method), in file then declaration order."""
    found = []
    for name in sorted(os.listdir(CODE)):
        if not name.endswith(".lua"):
            continue
        with open(os.path.join(CODE, name), encoding="utf-8") as fh:
            src = strip_comments(fh.read())
        for block in require_blocks(src):
            for entry in entries(block):
                # (?<![\w.]) keeps `changed_class` and `object_class` out.
                cm = re.search(r'(?<![\w.])class\s*=\s*"([^"]+)"', entry)
                mm = re.search(r'(?<![\w.])method\s*=\s*"([^"]+)"', entry)
                if cm and mm:
                    row = (name[:-4], cm.group(1), mm.group(1))
                    if row not in found:
                        found.append(row)
    return found


def main():
    rows = harvest()
    pairs = sorted(set((c, m) for _, c, m in rows))
    classes = sorted(set(c for c, _ in pairs))
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--lua":
        for mod, c, m in rows:
            print('\t{ %-32s %-38s %-40s },'
                  % ('"%s",' % mod, '"%s",' % c, '"%s"' % m))
        return
    if mode == "--list":
        for mod, c, m in rows:
            print("  %-34s %s.%s" % (mod, c, m))
    print("TARGETS: %d entries, %d distinct (class, method) pairs, %d classes"
          % (len(rows), len(pairs), len(classes)))


if __name__ == "__main__":
    main()
