#!/usr/bin/env python
"""doccheck.py — the structure checker (DOC_RESTRUCTURE_SPEC.md §5).

v1 (prompt 1, 2026-08-03): BUGS.md row<->tag status-word agreement, a counts
recount printed as a STATE-ready block, and a TEMPORARY sweep over both repos.
Green on the CURRENT structure is the migration baseline; v2/v3 grow this file
as the restructure chain proceeds.

    python tools/doccheck.py                 # check; exit 1 on any red
    python tools/doccheck.py --emit-counts   # + the pasteable counts block

Every parsing rule below that carries a "trap" note was learned the hard way by
the 2026-08-03 QA session that hand-ran these checks. Do not "simplify" them.
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTKIT = os.environ.get("SMR_TESTKIT", r"C:\Dev\SMR-BugFixPack-TestKit")

BUGS = os.path.join(REPO, "docs", "BUGS.md")
CODE = os.path.join(REPO, "Code")

# Index rows. Trap (a): this pattern also matches a rate table inside the F97
# entry (`| F97 | **50%** (gate fails) | ...`) — dedupe by ID, keep the FIRST.
ROW_RE = re.compile(r"^\|\s*([FDC]\d+)\s*\|")

# Entry headings. Trap: `^### ` alone is NOT an entry delimiter — entries carry
# their own `###` sub-headings (e.g. F97's "### THE UNINSTALL LOG..."), so the
# ID must be matched explicitly.
HEAD_RE = re.compile(r"^### ([FDC]\d+)\b")

# Heading tag. Trap: titles contain backticks (e.g. `table.remove`), so the tag
# is the LAST `[...]` group on the line, never the first backtick group.
TAG_RE = re.compile(r"`\[(.*)\]`\s*$")

# Status vocabulary, longest-first so `fixed*` is never read as `fixed`.
STATUS_WORDS = sorted(
    [
        "tested", "fixed*", "fixed", "wontfix", "blocked", "todo", "open",
        "investigating", "closed", "built", "directed", "parked", "opt-in",
        "candidate", "folded", "filed", "speced", "cand", "dsgn",
    ],
    key=len,
    reverse=True,
)

# Emphasis/attention markup that can precede the status word in either place:
# bold stars, strikethrough, backticks and a growing zoo of emoji (⭐ ⛔ ✅ ⚠️
# ⏸️ ⚖️ ...). Strip every leading non-letter rather than enumerate them.
MARKUP_RE = re.compile(r"^[^A-Za-z]+")


def read(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read().splitlines()


def status_word(cell):
    """First vocabulary status word of a row cell or heading tag, or None."""
    text = MARKUP_RE.sub("", cell or "").lower()
    for word in STATUS_WORDS:
        if text.startswith(word):
            return word
    return None


def parse_bugs():
    """-> (rows {id: status_cell}, tags {id: tag_text}) from docs/BUGS.md."""
    rows, tags = {}, {}
    for line in read(BUGS):
        m = ROW_RE.match(line)
        if m and m.group(1) not in rows:  # first occurrence wins (trap a)
            cells = line.rstrip().split("|")
            if cells and cells[-1].strip() == "":
                cells = cells[:-1]
            # cells[0] is the empty pre-pipe field; 1=ID 2=title 3=sev 4=conf
            rows[m.group(1)] = "|".join(cells[5:]).strip() if len(cells) > 5 else ""
        h = HEAD_RE.match(line)
        if h:
            t = TAG_RE.search(line)
            if t:
                tags[h.group(1)] = t.group(1)
    return rows, tags


def mentions(text, word):
    """Does `word` occur in `text` on a left word boundary?"""
    return re.search(r"(?<![A-Za-z])" + re.escape(word), text, re.IGNORECASE) is not None


def check_status_agreement(rows, tags, out):
    """Index row must not contradict the heading tag's status word.

    The TAG is authoritative — spec §2 derives front-matter `status:` from its
    first status word, and the index row is deleted by the migration. So:

      * the tag MUST lead with a vocabulary word (else the derivation has
        nothing to read) — red;
      * if the row also leads with one, the two must be equal — red on drift;
      * a row that leads with a narrative announcement instead ("⭐ MECHANISM
        FOUND...") only has to *carry* the tag's word somewhere — reported as
        WARN so it is visible, never silently discounted.
    """
    mismatches, untagged, warns = [], [], []
    compared = 0
    for bug_id, tag in sorted(tags.items()):
        if bug_id not in rows:
            continue
        row, tag_word = rows[bug_id], status_word(tag)
        if tag_word is None:
            untagged.append((bug_id, tag[:60]))
            continue
        compared += 1
        row_word = status_word(row)
        if row_word is not None:
            if row_word != tag_word:
                mismatches.append((bug_id, row_word, tag_word))
        elif mentions(row, tag_word):
            warns.append((bug_id, tag_word, row[:60]))
        else:
            mismatches.append((bug_id, "(absent)", tag_word))

    out.append("STATUS AGREEMENT: %d IDs compared (index row vs heading tag)"
               % compared)
    for bug_id, row_word, tag_word in mismatches:
        out.append("  RED  %s: index row says '%s', heading tag says '%s'"
                   % (bug_id, row_word, tag_word))
    for bug_id, tag in untagged:
        out.append("  RED  %s: heading tag has no vocabulary status word: %r"
                   % (bug_id, tag))
    for bug_id, tag_word, row in warns:
        out.append("  warn %s: row leads with prose, not a status word; "
                   "agrees on '%s' further in — %r" % (bug_id, tag_word, row))
    return not (mismatches or untagged)


def lua_files(directory):
    if not os.path.isdir(directory):
        return None
    return sorted(f for f in os.listdir(directory) if f.endswith(".lua"))


def files_containing(directory, names, needle):
    hits = []
    for name in names:
        with open(os.path.join(directory, name), encoding="utf-8-sig",
                  errors="replace") as fh:
            if needle in fh.read():
                hits.append(name)
    return hits


def occurrences(directory, names, needle):
    total = 0
    for name in names:
        with open(os.path.join(directory, name), encoding="utf-8-sig",
                  errors="replace") as fh:
            total += fh.read().count(needle)
    return total


def recount(rows, out):
    """The counts block. Reported, never asserted — adding a module is legal."""
    counts = {}
    names = lua_files(CODE) or []
    counts["files"] = len(names)
    registered = files_containing(CODE, names, "SMRFixPack.Register(")
    # 00_Core.lua defines Register; it is not itself a registered module.
    counts["modules"] = len([n for n in registered if n != "00_Core.lua"])
    counts["optional"] = len(files_containing(CODE, names, "optional = true"))
    # Opt_DroneStatDials is the 8th optional but reports active at base, so
    # default-active is modules - 7, not modules - len(optional).
    counts["default_active"] = counts["modules"] - 7

    tk_code = os.path.join(TESTKIT, "Code")
    tk_names = lua_files(tk_code)
    if tk_names is None:
        counts["probes"] = None
        out.append("NOTE: TestKit not found at %s — probe count skipped "
                   "(set SMR_TESTKIT to override)" % TESTKIT)
    else:
        # minus 1: the SMRTest.Register definition in 00_TestCore.lua.
        counts["probes"] = occurrences(tk_code, tk_names, "SMRTest.Register(") - 1

    for kind in "FDC":
        counts["rows_" + kind] = len([i for i in rows if i.startswith(kind)])

    out.append("COUNTS: %d Code/*.lua files, %d registered modules "
               "(%d default-active, %d files carry optional = true), %s probes"
               % (counts["files"], counts["modules"], counts["default_active"],
                  counts["optional"],
                  "?" if counts["probes"] is None else counts["probes"]))
    out.append("        index rows: %d F + %d D + %d C = %d"
               % (counts["rows_F"], counts["rows_D"], counts["rows_C"],
                  counts["rows_F"] + counts["rows_D"] + counts["rows_C"]))
    return counts


def temporary_sweep(out):
    """No TEMPORARY markers may survive in shipped or TestKit Lua."""
    hits = []
    for directory in (CODE, os.path.join(TESTKIT, "Code")):
        names = lua_files(directory)
        if names is None:
            continue
        for name in names:
            path = os.path.join(directory, name)
            with open(path, encoding="utf-8-sig", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    if "TEMPORARY" in line:
                        hits.append("%s:%d: %s" % (path, n, line.strip()))
    out.append("TEMPORARY SWEEP: %d hit(s) in Code/ + TestKit Code/" % len(hits))
    for hit in hits:
        out.append("  RED  " + hit)
    return not hits


def counts_block(counts):
    """A STATE-ready block; commit bodies may paste it verbatim."""
    lines = [
        "BUILD STATE (emitted by tools/doccheck.py)",
        "- modules: %d registered (%d default-active, %d optional-gated files)"
        % (counts["modules"], counts["default_active"], counts["optional"]),
        "- Code/*.lua files: %d" % counts["files"],
        "- TestKit probes: %s"
        % ("not counted (TestKit absent)" if counts["probes"] is None
           else counts["probes"]),
        "- BUGS index rows: %d F + %d D + %d C"
        % (counts["rows_F"], counts["rows_D"], counts["rows_C"]),
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="SMR-BugFixPack doc structure check")
    ap.add_argument("--emit-counts", action="store_true",
                    help="also print the STATE-ready counts block")
    args = ap.parse_args()

    # The docs are full of non-cp1252 markup; a Windows console (or a git hook
    # running under one) must not die on printing a finding.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    out = []
    rows, tags = parse_bugs()
    ok = check_status_agreement(rows, tags, out)
    counts = recount(rows, out)
    ok = temporary_sweep(out) and ok

    print("\n".join(out))
    print("doccheck: %s" % ("GREEN" if ok else "RED"))
    if args.emit_counts:
        print()
        # Never hand a pasteable block to a red run: the whole point of the
        # block is that a commit body can quote it as verified state, and the
        # numbers above a failure are not verified state.
        print(counts_block(counts) if ok
              else "BUILD STATE withheld — doccheck is RED; fix it, then re-run.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
