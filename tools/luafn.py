#!/usr/bin/env python3
"""Print a top-level Lua function body from the shipped ModTools/Src tree (added 2026-09-08 for the 1.1.0 re-verification).

    python luafn.py <file-relative-to-Src> <regex-on-the-function-line> [more regexes]

Prints from the matching `function` / `local function` line down to the
first line that is a bare `end` at the same indentation, with line numbers.
"""
import os, re, sys

SRC = r"A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src"

def main():
    rel = sys.argv[1]
    path = os.path.join(SRC, rel)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    for pat in sys.argv[2:]:
        rx = re.compile(pat)
        hits = [i for i, l in enumerate(lines) if rx.search(l)]
        if not hits:
            print("### %s: NO MATCH for %r" % (rel, pat))
            continue
        for i in hits:
            l = lines[i]
            indent = len(l) - len(l.lstrip("\t "))
            end_rx = re.compile(r"^[\t ]{%d}end\b" % indent)
            j = i
            if re.search(r"\bfunction\b", l):
                for j in range(i + 1, len(lines)):
                    m = lines[j]
                    mi = len(m) - len(m.lstrip("\t "))
                    if mi == indent and m.strip().startswith("end") and not m.strip().startswith("end)"):
                        break
            print("### %s:%d-%d" % (rel, i + 1, j + 1))
            for k in range(i, j + 1):
                print("%5d\t%s" % (k + 1, lines[k]))
            print()

if __name__ == "__main__":
    main()
