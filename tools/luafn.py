#!/usr/bin/env python3
"""Print a top-level Lua function body from the shipped ModTools/Src tree (added 2026-09-08 for the 1.1.0 re-verification).

    python luafn.py <file-relative-to-Src> <regex-on-the-function-line> [more regexes]

Prints from the matching `function` / `local function` line down to the
first line that is a bare `end` at the same indentation, with line numbers.

⚠️ `find_bodies` below is THE body delimiter for this project — `bodycheck.py`
imports it so the `SRC:` manifest hashes exactly what this prints, and there is
never a second extractor to disagree with. Change it here or nowhere.
"""
import os, re, sys

SRC = r"A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src"


def read_lines(path):
    """The one reader: bytes -> utf-8 (replace) -> universal newlines -> list.

    Deliberately decodes with `errors="replace"` rather than failing: the
    result is deterministic, which is all a hash needs.
    """
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def find_bodies(lines, pattern):
    """-> list of (start, end) 0-based inclusive line indices for `pattern`.

    A hit whose line declares a `function` runs to the first line that is a
    bare `end` at the SAME indentation (`end)` excluded — that closes a call,
    not a block). A hit that is not a function declaration is a single line.
    """
    rx = re.compile(pattern)
    out = []
    for i, l in enumerate(lines):
        if not rx.search(l):
            continue
        indent = len(l) - len(l.lstrip("\t "))
        j = i
        if re.search(r"\bfunction\b", l):
            for j in range(i + 1, len(lines)):
                m = lines[j]
                mi = len(m) - len(m.lstrip("\t "))
                if mi == indent and m.strip().startswith("end") and not m.strip().startswith("end)"):
                    break
        out.append((i, j))
    return out


def main():
    rel = sys.argv[1]
    path = os.path.join(SRC, rel)
    lines = read_lines(path)
    for pat in sys.argv[2:]:
        spans = find_bodies(lines, pat)
        if not spans:
            print("### %s: NO MATCH for %r" % (rel, pat))
            continue
        for i, j in spans:
            print("### %s:%d-%d" % (rel, i + 1, j + 1))
            for k in range(i, j + 1):
                print("%5d\t%s" % (k + 1, lines[k]))
            print()

if __name__ == "__main__":
    main()
