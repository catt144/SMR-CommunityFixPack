#!/usr/bin/env python
"""doccheck.py — the structure checker (DOC_RESTRUCTURE_SPEC.md §5).

v1 (prompt 1, 2026-08-03): BUGS.md row<->tag status-word agreement, a counts
recount printed as a STATE-ready block, and a TEMPORARY sweep over both repos.
v2 (prompt 2, 2026-08-03): docs/BUGS.md is now 116 entry files under
docs/agent/bugs/ plus a GENERATED INDEX.md, so the row<->tag check moves onto
front matter, INDEX freshness is checked by regenerating and diffing, and
`--verify-split` re-runs the migration's byte-accounting against the pre-split
blob in git.

    python tools/doccheck.py                 # check; exit 1 on any red
    python tools/doccheck.py --emit-counts   # + the pasteable counts block
    python tools/doccheck.py --verify-split [REV]   # REV defaults to HEAD~1

Every parsing rule below that carries a "trap" note was learned the hard way by
the 2026-08-03 QA session that hand-ran these checks. Do not "simplify" them.
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTKIT = os.environ.get("SMR_TESTKIT", r"C:\Dev\SMR-BugFixPack-TestKit")

BUGS = os.path.join(REPO, "docs", "BUGS.md")          # a stub since 2026-08-03
BUGS_DIR = os.path.join(REPO, "docs", "agent", "bugs")
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


def mentions(text, word):
    """Does `word` occur in `text` on a left word boundary?"""
    return re.search(r"(?<![A-Za-z])" + re.escape(word), text, re.IGNORECASE) is not None


def splitter():
    """The migration module, imported lazily so it can import this one."""
    import split_bugs
    return split_bugs


def all_rows(model):
    """-> every index row the split preserved: 116 entry-owning rows, the rows
    adopted into grouped front matter, and the orphan rows in _notes.md."""
    rows = []
    for entry in model["entries"]:
        rows.append(entry)
        rows.extend(entry.get("members", []))
    rows.extend(model["by_id"][i] for i in model["orphans"])
    return rows


def check_entries(model, out):
    """Front-matter validation + the row<->tag check on its new surface.

    v1 compared a hand-written index row against the heading tag. The row is
    gone as a hand-written artifact — it is now `row_status:`, copied verbatim
    and never re-typed — so the same drift is checked between the DERIVED
    `status:` and the tag the entry body still carries. The tag stays
    authoritative; a `row_status` that opens with prose instead of a status word
    is a warn, exactly as before, and is never silently discounted.
    """
    sb = splitter()
    red, warns = [], []
    seqs, rows = {}, {}
    tagged = 0

    for entry in model["entries"]:
        name = entry["file"]
        for field in sb.FRONT_FIELDS:
            if field not in entry:
                red.append("%s: front matter is missing %r" % (name, field))
        if red and red[-1].startswith(name):
            continue
        if entry["status"] not in STATUS_WORDS:
            red.append("%s: status %r is not in the vocabulary"
                       % (name, entry["status"]))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(entry["updated"])):
            red.append("%s: updated %r is not a date" % (name, entry["updated"]))
        if not isinstance(entry["copies"], list):
            red.append("%s: copies must be a list" % name)
        if entry["kind"] == "grouped":
            if name != "%s-%s" % (entry["contains"][0], entry["contains"][-1]):
                red.append("%s: file name does not state the range it holds" % name)
            member_ids = [m["id"] for m in entry["members"]]
            if sorted(entry["contains"]) != sorted([entry["id"]] + member_ids):
                red.append("%s: contains: disagrees with members: + id" % name)
        elif name != entry["id"]:
            red.append("%s: file name does not match id %r" % (name, entry["id"]))

        # the body must still open with the heading the split preserved
        body = entry["body"]
        head = HEAD_RE.match(body[0]) if body else None
        if not head or head.group(1) != entry["id"]:
            red.append("%s: body does not open with its `### %s` heading"
                       % (name, entry["id"]))
        else:
            tag = TAG_RE.search(body[0])
            if tag:
                tagged += 1
                word = status_word(tag.group(1))
                if word is None:
                    red.append("%s: heading tag has no vocabulary status word: %r"
                               % (name, tag.group(1)[:60]))
                elif word != entry["status"]:
                    red.append("%s: front matter says %r, heading tag says %r"
                               % (name, entry["status"], word))
                elif entry["status_source"] != "tag":
                    red.append("%s: status_source is %r but the heading is tagged"
                               % (name, entry["status_source"]))
            elif entry["status_source"] == "tag":
                red.append("%s: status_source says 'tag' but the heading has none"
                           % name)

        seqs.setdefault(entry["seq"], []).append(name)

    sources = {}
    for row in all_rows(model):
        rows.setdefault(row["row"], []).append(row["id"])
        sources[row["status_source"]] = sources.get(row["status_source"], 0) + 1
        word = status_word(row["row_status"])
        if word is not None and word != row["status"]:
            # NOT red, and the difference from v1 is deliberate. v1 compared two
            # LIVE hand-written surfaces, so drift between them was a defect.
            # `row_status` is now a frozen copy of the row the migration
            # deleted: a status that has since advanced (fixed -> tested) MUST
            # be free to leave it behind. Reported so it is never invisible.
            warns.append("%s: the frozen index-row cell says %r, entry says %r "
                         "(from %r)"
                         % (row["id"], word, row["status"], row["status_source"]))

    dup_seq = {k: v for k, v in seqs.items() if len(v) > 1}
    if dup_seq:
        red.append("duplicate seq: %r" % dup_seq)
    if sorted(seqs) != list(range(1, len(model["entries"]) + 1)):
        red.append("seq is not 1..%d contiguous" % len(model["entries"]))
    dup_row = {k: v for k, v in rows.items() if len(v) > 1}
    if dup_row:
        red.append("duplicate index row numbers: %r" % dup_row)
    if sorted(rows) != list(range(1, len(rows) + 1)):
        red.append("index row numbers are not 1..%d contiguous" % len(rows))

    out.append("ENTRIES: %d files (%d grouped), %d preserved index rows, "
               "%d heading tags compared"
               % (len(model["entries"]),
                  len([e for e in model["entries"] if e["kind"] == "grouped"]),
                  len(rows), tagged))
    out.append("  status derived from: %s"
               % ", ".join("%s x%d" % (k, v) for k, v in sorted(sources.items())))
    for line in red:
        out.append("  RED  " + line)
    for line in warns:
        out.append("  warn " + line)
    return not red


def check_index(model, out):
    """INDEX.md is generated: regenerate it and require an empty diff."""
    sb = splitter()
    path = os.path.join(BUGS_DIR, "INDEX.md")
    if not os.path.exists(path):
        out.append("INDEX: RED  %s is missing" % path)
        return False
    with open(path, encoding="utf-8") as fh:
        have = fh.read().replace("\r\n", "\n").split("\n")
    if have and have[-1] == "":
        have.pop()
    want = sb.render_index(model)
    if have == want:
        out.append("INDEX: fresh — regenerating from front matter reproduces "
                   "%s.md byte for byte (%d rows)"
                   % (os.path.basename(path)[:-3], len(sb.index_rows(model))))
        return True
    out.append("INDEX: RED  regenerated INDEX.md differs from the file "
               "(%d lines on disk, %d regenerated)" % (len(have), len(want)))
    for n, (a, b) in enumerate(zip(have, want), 1):
        if a != b:
            out.append("  RED  first difference at line %d:" % n)
            out.append("    on disk:     %r" % a[:100])
            out.append("    regenerated: %r" % b[:100])
            break
    return False


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


def recount(model, out):
    """The counts block. Reported, never asserted — adding a module is legal."""
    counts = {}
    rows = [r["id"] for r in all_rows(model)]
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
    out.append("        index rows: %d F + %d D + %d C = %d (in %d entry files)"
               % (counts["rows_F"], counts["rows_D"], counts["rows_C"],
                  counts["rows_F"] + counts["rows_D"] + counts["rows_C"],
                  len(model["entries"])))
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
    ap.add_argument("--verify-split", nargs="?", const="HEAD~1", metavar="REV",
                    help="re-run the BUGS split accounting against REV's "
                         "docs/BUGS.md and the files on disk (default HEAD~1)")
    args = ap.parse_args()

    # The docs are full of non-cp1252 markup; a Windows console (or a git hook
    # running under one) must not die on printing a finding.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    out = []
    sb = splitter()
    try:
        model = sb.load_from_dir()
        ok = check_entries(model, out)
        ok = check_index(model, out) and ok
    except sb.SplitError as exc:
        print("doccheck: RED — %s" % exc)
        return 1
    counts = recount(model, out)
    ok = temporary_sweep(out) and ok

    if args.verify_split:
        try:
            out.append("VERIFY-SPLIT against %s:%s" % (args.verify_split, "docs/BUGS.md"))
            sb.verify_split(args.verify_split, out)
        except sb.SplitError as exc:
            out.append("  RED  %s" % exc)
            ok = False

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
