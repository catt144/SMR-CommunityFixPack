#!/usr/bin/env python3
"""What did the game change, function by function, between two ModTools/Src trees?

Written 2026-09-10 for `prompts/vanillahunt/01_INVENTORY.md` unit B. The game
went 1.0.7.396349 -> 1.1.0.403908 and **2444 files changed**. A textual diff of
2444 files is not readable by anyone; this emits one ROW per top-level function
that was added, removed, body-changed or signature-changed, so the hunt reads
changes instead of files.

    python tools/treediff.py --selftest        # the falsifier -- run it first
    python tools/treediff.py --out <dir>       # write INVENTORY.tsv + friends
    python tools/treediff.py --old <Src> --new <Src>

⛔ THE DELIMITER IS NOT OURS. `luafn.py:find_bodies` is this project's single
canonical body delimiter -- `bodycheck.py` imports it so that every `SRC:` hash
in `Code/` is the hash of exactly what `luafn.py` prints. This tool imports it
too and NEVER re-implements it. Two extractors would disagree, and the day they
disagreed we would trust the wrong one.

WHAT IS A ROW, AND WHAT IS NOT
  added / removed        the key exists in one tree only
  body                   the body under the declaration changed
  sig                    the parameter list changed
  body+sig               both

  ⚠️ TWO HASHES, AND THE REASON THERE ARE TWO. A body span INCLUDES its own
  declaration line, so hashing the span alone would make every signature change
  report as `body+sig` and would make a RENAME never hash-match its partner --
  both of which this tool's own falsifier caught on its first run. So:
    `hash`   the WHOLE span, byte-for-byte what `bodycheck.py` hashes, so a row
             can be cross-checked against a `SRC:` pin in `Code/` directly;
    `ihash`  the span with the declaration line DROPPED -- what "the body
             changed" actually means, and what `RENAME?` matches on.
  ⭐ `sig` with no `body` is therefore the F115 shape exactly: a parameter
  arrived, every line under it is byte-identical, and every argument inside is
  now one slot late.

  ⛔ A WHITESPACE-ONLY DIFF IS NOT A ROW. Normalisation before hashing is
  EXACTLY `bodycheck.py`'s: `\\r\\n` -> `\\n` (done by `luafn.read_lines`), then
  TRAILING whitespace stripped per line. Leading indentation is KEPT -- it is
  structure.
  ⭐ **A CHANGED COMMENT IS A ROW.** Comments are kept in the hash, exactly as
  `bodycheck.py` keeps them: a changed comment in a shipped body is a signal
  about what the developers thought they were doing, not noise.

THE KEY, AND WHY THE SEPARATOR IS NORMALISED. Rows are keyed
`file:function`. `Class:Method` and `Class.Method` collapse to ONE key
(`Class.Method`) because the game rewrites between the two forms, and a
rewrite that only moved `self` from implicit to explicit is a SIGNATURE change
worth reading -- not an unrelated add plus an unrelated remove. The separator
that was actually written is carried in the `sig` columns as a leading `:` or
`.`, and a flip is flagged `SEP-CHANGED`.

v1.1 (2026-09-10, the chain's authoring session, AFTER link 01 closed): the
"4,883 indented declarations covered by neither instrument" hole was MEASURED
first -- 2,033 of the 4,142 in changed hand files sit INSIDE an enumerated
function and were already covered by its hash; 2,109 sat outside every span:
table-field methods in `DefineClass{}`/metatables, the `Run = function(seq_state)`
steps of `Lua/Scenario/*.generated.lua` (player-facing mystery code), and
file-level nested locals. Those "orphans" are now enumerated too (`_orphans`),
keyed `name@<anchor>`, flagged INDENTED, matched by hash inside their group so
an inserted sibling cannot cascade (`_diff_orphans`), and a self-closing
orphan hashes its own line only (flag ONE-LINE -- deliberate, stated in the
banner; the indent-0 pass keeps the delimiter's over-span, checklist 135).
Falsified in `--selftest` (`Lua/T.lua`). The `hash` column of an orphan row is
NOT comparable to a `SRC:` pin, because no pin ever targeted one.

WHAT THE REGEX RECOGNISES -- the completeness contract, stated so it can be
checked rather than assumed. Five declaration forms, **at indentation 0 only**:

    function Class:Method(...)      function Class.Method(...)   function A.B.C:D(...)
    function Global(...)            local function name(...)
    local name = function(...)      Name.Field = function(...)

⛔ WHAT IT DOES NOT RECOGNISE. Every banner MEASURES this rather than asserting
it, so the hole is a number a reader can act on (8,473 on the two trees as
shipped: 4,883 in `hand` files, 3,590 in `generated`):
  * INDENTED declarations -- `X = function(self)` table fields inside
    `DefineClass` / `PlaceObj` blocks. Sampled at authoring: overwhelmingly
    `Data/`, `Lua/XDef/`, `Lua/Scenario/*.generated.lua` and `CommonLua/Ged/`,
    i.e. preset data, which `presetdiff.py` reads at FIELD level instead. The
    remainder are hand-written table-field methods and they are NOT covered by
    either instrument -- the largest single known hole in this inventory.
  * anonymous `function(` literals passed as arguments (~12,200 lines).
A function this tool never emitted is not a function that did not change.
⛔ Rule 7 of the chain README: no instrument here is a clearance.

⚠️ THE ONE-LINE-FUNCTION TRAP, MEASURED NOT ASSUMED. `find_bodies` scans
FORWARD from a declaration for a bare `end` at the same indentation and does
not check whether the declaration line already closed the function. So
`function f() return 1 end` spans past its own `end` to the NEXT one, and its
"body" swallows whatever follows. Every such declaration is flagged
`SPAN-SUSPECT` and counted in the banner; that count IS the inventory's stated
imprecision. ⛔ This tool does NOT fix `luafn.py`: a delimiter change re-hashes
every `SRC:` pin in `Code/`, which is a hotfix-3 decision for the owner, filed
to the checklist -- not a side effect of an inventory run.

BUCKETS ARE A COLUMN, NEVER A FILTER
  generated   `Data/`, `Lua/BuildingTemplate/`, `Lua/XDef/`, `Lua/ClassDefs/`
  dlc         `DLC/` -- ⛔ EXCLUDED from the diff entirely (chain blind spot 5:
              the 1.0.7 archive's DLC subtree is a Steam branch artefact)
  hand        everything else
⛔ No bucket is assigned by "is this tooling" -- that is a judgement about
ROUTE and it belongs to a reader, not to a path prefix.

⚠️ WHAT IT CANNOT DECIDE. That a `body` row MEANS anything -- most of 2444
changed files is churn, and deciding which rows matter is link 02's job, not an
instrument's. That `RENAME?` is a rename: it is a body-similarity HINT with the
partner named, and a hint is not a verdict. That the two trees are the two
builds: that is the manifests' job, and their digests are in the banner.
"""

import argparse
import datetime
import hashlib
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luafn import find_bodies, read_lines          # THE delimiter -- see above
from sigcheck import params                        # THE parameter reader

VERSION = "treediff.py v1.1 (2026-09-10, indented orphans covered)"

ARCHIVE = r"C:\Dev\SMR-SrcArchive"
DEFAULT_OLD = os.path.join(ARCHIVE, "1.0.7.396349", "Src")
DEFAULT_NEW = os.path.join(ARCHIVE, "1.1.0.403908", "Src")

GENERATED = ("Data/", "Lua/BuildingTemplate/", "Lua/XDef/", "Lua/ClassDefs/")

# --------------------------------------------------------------------------- #
# declaration forms. Order matters: `local function` before `function`, method
# before global, and every one anchored at column 0 (the top-level contract).
# The parameter list is `[^)]*` because Lua has no default arguments, so a
# parameter list cannot itself contain `)` -- the same rule sigcheck.py uses.
# --------------------------------------------------------------------------- #
DECLS = (
    ("localfn", re.compile(r"^local\s+function\s+([A-Za-z_][\w.]*(?:[.:][A-Za-z_]\w*)?)\s*\(([^)]*)\)")),
    ("method",  re.compile(r"^function\s+([A-Za-z_][\w.]*[.:][A-Za-z_]\w*)\s*\(([^)]*)\)")),
    ("global",  re.compile(r"^function\s+([A-Za-z_]\w*)\s*\(([^)]*)\)")),
    ("localas", re.compile(r"^local\s+([A-Za-z_]\w*)\s*=\s*function\s*\(([^)]*)\)")),
    ("assign",  re.compile(r"^([A-Za-z_][\w.]*(?:[.:][A-Za-z_]\w*)?)\s*=\s*function\s*\(([^)]*)\)")),
)
INDENTED = re.compile(r"^[ \t]+(?:local\s+)?(?:function\s+[A-Za-z_]|[A-Za-z_][\w.:]*\s*=\s*function\s*\()")
# a declaration line that already closes its own function: `... end` as the last
# token, comment stripped. This is the one-line-function trap's detector.
SELF_CLOSING = re.compile(r"\bend\b[\s,;)\]}]*$")


def strip_comment(line):
    """Good enough to find a trailing `end`: drop a `--` that is not in a string."""
    out, i, quote = [], 0, None
    while i < len(line):
        c = line[i]
        if quote:
            if c == "\\":
                out.append(line[i:i + 2]); i += 2; continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "-" and line[i:i + 2] == "--":
            break
        out.append(c)
        i += 1
    return "".join(out)


def body_hash(lines, start, end):
    """EXACTLY bodycheck.py's normalisation: LF (read_lines did it) + rstrip."""
    return hashlib.sha256(
        "\n".join(l.rstrip() for l in lines[start:end + 1]).encode("utf-8")
    ).hexdigest()


def canon(name):
    """`Class:Method` and `Class.Method` are ONE key -- see the header."""
    return name.replace(":", ".")


def declarations(lines, indented=False):
    """-> list of dicts, one per recognised indent-0 declaration, in file order.

    Each carries the span from `find_bodies` (never our own delimiter), the
    normalised body hash, the parameter list, and the flags this row earned.

    v1.1: with `indented=True` the list ALSO carries every INDENTED declaration
    that lies OUTSIDE every span enumerated so far (an "orphan": a table-field
    method `X = function(self)` inside `DefineClass{}` or a metatable, a
    sequence step `Run = function(seq_state)` in `Lua/Scenario/*.generated.lua`,
    a `local function` under a file-level `if`). An indented declaration INSIDE
    an enumerated span is NOT listed: the outer body's hash already covers it.
    Orphans carry `orphan=True`, `oneline=True` when the declaration line
    closes itself, and a key of the form `name@<anchor>` (see `_anchor`).
    """
    raw = []
    for i, line in enumerate(lines):
        if not line or line[0] in " \t":
            continue
        for form, rx in DECLS:
            m = rx.match(line)
            if m:
                raw.append((i, line, form, m.group(1), m.group(2)))
                break

    # find_bodies is called ONCE per distinct declaration line text and returns
    # every span for it; the k-th occurrence takes the k-th span. That is what
    # makes the MULTI ordinal keying exact rather than approximate.
    spans, seen = {}, {}
    out = []
    for i, line, form, name, sig in raw:
        if line not in spans:
            spans[line] = find_bodies(lines, "^" + re.escape(line) + "$")
        k = seen.get(line, 0)
        seen[line] = k + 1
        got = spans[line]
        if k >= len(got):                       # cannot happen; say so if it does
            start, end = i, i
        else:
            start, end = got[k]
        out.append(dict(
            line=i + 1, form=form, raw_name=name, key=canon(name),
            sep=":" if ":" in name else ".",
            sig=",".join(params(sig)),
            span=(start, end), hash=body_hash(lines, start, end),
            ihash=body_hash(lines, start + 1, end),
            body=[l.strip() for l in lines[start + 1:end + 1] if l.strip()],
            self_closing=bool(SELF_CLOSING.search(strip_comment(line))),
            orphan=False, oneline=False,
        ))
    if indented:
        out.extend(_orphans(lines, [d["span"] for d in out]))
    # ordinal-key the duplicates, and flag them
    counts = {}
    for d in out:
        counts[d["key"]] = counts.get(d["key"], 0) + 1
    nth = {}
    for d in out:
        if counts[d["key"]] > 1:
            n = nth.get(d["key"], 0) + 1
            nth[d["key"]] = n
            d["key"] = "%s#%d" % (d["key"], n)
            d["multi"] = True
        else:
            d["multi"] = False
    return out


def _anchor(lines, i):
    """The nearest preceding indent-0 non-blank line, hashed to 6 hex chars.

    An orphan's NAME repeats (`Run` appears dozens of times in one scenario
    file), so the key needs a locality: the top-level construct it sits in.
    Two orphans with the same name under the same anchor still collide and get
    the MULTI ordinal; `_diff_orphans` then matches them by HASH first so an
    inserted sibling does not cascade into a column of false `body` rows.
    """
    j = i - 1
    while j >= 0:
        l = lines[j]
        if l and l[0] not in " \t" and l.strip():
            return hashlib.sha256(l.rstrip().encode("utf-8")).hexdigest()[:6]
        j -= 1
    return "top"


def _orphans(lines, spans):
    """Indented declarations outside every span in `spans` (which grows as
    orphans are found, so a declaration nested inside an orphan is skipped)."""
    spans = list(spans)
    cache, seen, out = {}, {}, []
    for i, line in enumerate(lines):
        if not INDENTED.match(line):
            continue
        if any(s <= i <= e for s, e in spans):
            continue
        stripped = line.lstrip(" \t")
        hit = None
        for form, rx in DECLS:
            m = rx.match(stripped)
            if m:
                hit = (form, m.group(1), m.group(2))
                break
        if hit is None:
            continue
        form, name, sig = hit
        oneline = bool(SELF_CLOSING.search(strip_comment(line)))
        if oneline:
            # ⚠️ DELIBERATE, AND ONLY HERE: a self-closing declaration is its own
            # span. `find_bodies` would run it to the next same-indent `end`,
            # which inside a table constructor is the NEXT field's `end,` —
            # every neighbour's edit would then re-hash this row. The indent-0
            # pass keeps the delimiter's behaviour untouched (checklist 135 is
            # the owner's); this pass never had a pin to protect.
            start, end = i, i
        else:
            if line not in cache:
                cache[line] = find_bodies(lines, "^" + re.escape(line) + "$")
            k = seen.get(line, 0)
            seen[line] = k + 1
            got = cache[line]
            start, end = got[k] if k < len(got) else (i, i)
        spans.append((start, end))
        out.append(dict(
            line=i + 1, form=form, raw_name=name,
            key="%s@%s" % (canon(name), _anchor(lines, i)),
            sep=":" if ":" in name else ".",
            sig=",".join(params(sig)),
            span=(start, end), hash=body_hash(lines, start, end),
            ihash=body_hash(lines, start + 1, end) if end > start else "",
            body=[l.strip() for l in lines[start + 1:end + 1] if l.strip()],
            self_closing=oneline, orphan=True, oneline=oneline,
        ))
    return out


def bare_name(key):
    """`Class.Method#2` -> `Method`; `Run@1a2b3c#3` -> `Run`."""
    return key.split("@")[0].split("#")[0].split(".")[-1]


def count_indented(lines):
    return sum(1 for l in lines if INDENTED.match(l))


def bucket(rel):
    if rel.startswith("DLC/"):
        return "dlc"
    return "generated" if rel.startswith(GENERATED) else "hand"


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tree_files(root):
    out = {}
    for dp, _d, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            out[os.path.relpath(p, root).replace("\\", "/")] = p
    return out


def tree_digest(root):
    """The MANIFEST.sha256 digest beside the tree, or '(no manifest)'."""
    man = os.path.join(os.path.dirname(root), "MANIFEST.sha256")
    if not os.path.isfile(man):
        return "(no manifest)"
    with open(man, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16] + "…"


# --------------------------------------------------------------------------- #
# the diff
# --------------------------------------------------------------------------- #
def diff(old_root, new_root, progress=False):
    old_files, new_files = tree_files(old_root), tree_files(new_root)
    rel_all = sorted(set(old_files) | set(new_files))

    stats = dict(changed=0, identical=0, added=0, removed=0, dlc_skipped=0,
                 fn_identical=0, fn_old=0, fn_new=0, indented_hand=0,
                 indented_generated=0, span_suspect=0, multi=0, span_eof=0,
                 orphan_hand=0, orphan_generated=0, orphan_oneline=0,
                 orphan_identical=0, orphan_rows=0)
    rows, spanlist, multilist = [], [], []
    file_class = {}

    for rel in rel_all:
        if rel.startswith("DLC/"):
            stats["dlc_skipped"] += 1
            continue
        if not rel.lower().endswith(".lua"):
            # non-.lua still counts for the manifest re-derivation
            o, n = rel in old_files, rel in new_files
            file_class[rel] = ("added" if not o else "removed" if not n else
                               ("identical" if sha_file(old_files[rel]) == sha_file(new_files[rel])
                                else "changed"))
            stats[file_class[rel]] += 1
            continue
        o, n = rel in old_files, rel in new_files
        if o and n:
            same = sha_file(old_files[rel]) == sha_file(new_files[rel])
            file_class[rel] = "identical" if same else "changed"
        else:
            file_class[rel] = "added" if n else "removed"
        stats[file_class[rel]] += 1

    lua = [r for r in rel_all
           if r.lower().endswith(".lua") and not r.startswith("DLC/")]
    for idx, rel in enumerate(lua):
        cls = file_class[rel]
        b = bucket(rel)
        old_lines = read_lines(old_files[rel]) if rel in old_files else None
        new_lines = read_lines(new_files[rel]) if rel in new_files else None

        if cls == "identical":
            # nothing in it changed; count its functions and move on. Parsing
            # both sides here would be ~1900 files of pure cost for zero rows.
            d = declarations(new_lines)
            stats["fn_identical"] += len(d)
            stats["fn_old"] += len(d)
            stats["fn_new"] += len(d)
            stats["indented_generated" if b == "generated" else "indented_hand"] \
                += count_indented(new_lines)
            continue

        od_all = declarations(old_lines, indented=True) if old_lines is not None else []
        nd_all = declarations(new_lines, indented=True) if new_lines is not None else []
        od = [d for d in od_all if not d["orphan"]]
        nd = [d for d in nd_all if not d["orphan"]]
        oo = [d for d in od_all if d["orphan"]]
        no = [d for d in nd_all if d["orphan"]]
        stats["fn_old"] += len(od)
        stats["fn_new"] += len(nd)
        # orphans are counted on the same side as `indented_*` (1.1.0, or 1.0.7
        # for a removed file) so the two numbers in the banner are comparable
        side_orph = no if new_lines is not None else oo
        stats["orphan_generated" if b == "generated" else "orphan_hand"] += len(side_orph)
        stats["orphan_oneline"] += sum(1 for d in side_orph if d["oneline"])
        # ⚠️ counted on the 1.1.0 side ONLY (the 1.0.7 side for a REMOVED file),
        # so the banner's "not covered" number is one tree's worth and can be
        # compared against a hand count. Summing both sides double-counts.
        stats["indented_generated" if b == "generated" else "indented_hand"] \
            += count_indented(new_lines if new_lines is not None else old_lines)
        for side, ds, lines in (("107", od, old_lines), ("110", nd, new_lines)):
            for d in ds:
                if d["self_closing"] and d["span"][1] > d["span"][0]:
                    stats["span_suspect"] += 1
                    spanlist.append("%s\t%s\t%s\t%d\t%d lines" % (
                        side, rel, d["key"], d["line"], d["span"][1] - d["span"][0] + 1))
                if lines is not None and d["span"][1] >= len(lines) - 1 \
                        and d["span"][0] < len(lines) - 1:
                    stats["span_eof"] += 1
                if d["multi"]:
                    stats["multi"] += 1
                    multilist.append("%s\t%s\t%s\t%d" % (side, rel, d["key"], d["line"]))

        omap = {d["key"]: d for d in od}
        nmap = {d["key"]: d for d in nd}
        for k in sorted(set(omap) | set(nmap)):
            a, z = omap.get(k), nmap.get(k)
            flags = []
            if a and z:
                if a["hash"] == z["hash"] and a["sig"] == z["sig"] \
                        and a["sep"] == z["sep"]:
                    stats["fn_identical"] += 1
                    continue
                body_ch = a["ihash"] != z["ihash"]
                sig_ch = a["sig"] != z["sig"]
                if a["sep"] != z["sep"]:
                    flags.append("SEP-CHANGED")
                    sig_ch = True
                if not body_ch and not sig_ch:
                    # the span moved but neither the parameters nor the lines
                    # under them did: only the declaration line's OWN text
                    # changed (`local` dropped, a trailing comment added, the
                    # form rewritten). Real, and a different question.
                    flags.append("DECL-ONLY")
                    body_ch = True
                kind = ("body+sig" if body_ch and sig_ch else
                        "sig" if sig_ch else "body")
            elif z:
                kind = "added"
                # ⭐ "a new function in a file that already existed" and "a
                # function in a brand-new file" are different questions — class
                # (f) vs a whole new system — so the row says which.
                if cls == "added":
                    flags.append("NEWFILE")
            else:
                kind = "removed"
                if cls == "removed":
                    flags.append("GONEFILE")
            for d in (a, z):
                if d is None:
                    continue
                if d["multi"]:
                    flags.append("MULTI")
                if d["self_closing"] and d["span"][1] > d["span"][0]:
                    flags.append("SPAN-SUSPECT")
            rows.append(dict(
                file=rel, key=k, kind=kind, bucket=b,
                line107=a["line"] if a else "", line110=z["line"] if z else "",
                sig107=(a["sep"] + a["sig"]) if a else "",
                sig110=(z["sep"] + z["sig"]) if z else "",
                flags=sorted(set(flags)),
                hash107=a["hash"] if a else "", hash110=z["hash"] if z else "",
                ihash107=a["ihash"] if a else "", ihash110=z["ihash"] if z else "",
                body107=a["body"] if a else [], body110=z["body"] if z else [],
            ))
        orows = _diff_orphans(oo, no, rel, b, cls, stats)
        stats["orphan_rows"] += len(orows)
        rows.extend(orows)
        if progress and idx % 300 == 0:
            print("    ... %d/%d files, %d rows" % (idx, len(lua), len(rows)),
                  file=sys.stderr)

    stats.setdefault("rename_trivial", 0)
    stats.setdefault("rename_ambiguous", 0)
    annotate_renames(rows, stats)
    return rows, stats, file_class


def _diff_orphans(oo, no, rel, b, cls, stats):
    """Rows for the INDENTED orphans of one file (v1.1).

    Grouped by base key (`name@anchor`, ordinals dropped). Inside a group the
    two sides are matched by HASH first — an unchanged sibling never becomes a
    row just because a neighbour was inserted above it — and the leftovers are
    paired in file order as body/sig rows, with the excess as added/removed.
    """
    def base(k):
        return k.split("#")[0]
    og, ng = {}, {}
    for d in oo:
        og.setdefault(base(d["key"]), []).append(d)
    for d in no:
        ng.setdefault(base(d["key"]), []).append(d)
    rows = []
    for g in sorted(set(og) | set(ng)):
        A, Z = list(og.get(g, [])), list(ng.get(g, []))
        # 1. cancel identical hashes (same declaration line + same body)
        zh = {}
        for z in Z:
            zh.setdefault(z["hash"], []).append(z)
        A2 = []
        for a in A:
            if zh.get(a["hash"]):
                zh[a["hash"]].pop(0)
                stats["fn_identical"] += 1
                stats["orphan_identical"] += 1
            else:
                A2.append(a)
        Z2 = [z for zs in zh.values() for z in zs]
        Z2.sort(key=lambda d: d["line"])
        # 2. leftovers pair in file order
        for k in range(max(len(A2), len(Z2))):
            a = A2[k] if k < len(A2) else None
            z = Z2[k] if k < len(Z2) else None
            flags = ["INDENTED"]
            if a and z:
                body_ch = a["ihash"] != z["ihash"] or (a["oneline"] != z["oneline"])
                sig_ch = a["sig"] != z["sig"]
                if a["sep"] != z["sep"]:
                    flags.append("SEP-CHANGED")
                    sig_ch = True
                if not body_ch and not sig_ch:
                    flags.append("DECL-ONLY")
                    body_ch = True
                kind = ("body+sig" if body_ch and sig_ch else
                        "sig" if sig_ch else "body")
            elif z:
                kind = "added"
                if cls == "added":
                    flags.append("NEWFILE")
            else:
                kind = "removed"
                if cls == "removed":
                    flags.append("GONEFILE")
            for d in (a, z):
                if d is None:
                    continue
                if d["oneline"]:
                    flags.append("ONE-LINE")
                if len(og.get(g, [])) > 1 or len(ng.get(g, [])) > 1:
                    flags.append("MULTI")
            key = (z or a)["key"]
            rows.append(dict(
                file=rel, key=key, kind=kind, bucket=b,
                line107=a["line"] if a else "", line110=z["line"] if z else "",
                sig107=(a["sep"] + a["sig"]) if a else "",
                sig110=(z["sep"] + z["sig"]) if z else "",
                flags=sorted(set(flags)),
                hash107=a["hash"] if a else "", hash110=z["hash"] if z else "",
                ihash107=a["ihash"] if a else "", ihash110=z["ihash"] if z else "",
                body107=a["body"] if a else [], body110=z["body"] if z else [],
            ))
    return rows


MIN_RENAME_BODY = 4      # distinct non-blank body lines
MAX_RENAME_PARTNERS = 3  # more than this is an idiom, not a rename


def annotate_renames(rows, stats=None):
    """`RENAME?<partner>` -- an added body that equals, or ~equals, a removed one.

    A HINT (chain class (d)), never a verdict: the project has already nearly
    retired a live fix by reading "the name is gone" as "the feature is gone".

    ⛔ TWO GUARDS, BOTH SET FROM A MEASUREMENT AND NOT FROM TASTE. The first
    version of this had neither and produced 1,328 "rename partners" inside one
    `LuaExportedDocs` file. Counting what it had actually matched: 57 pairs with
    a ONE-line body (`end` -- an empty function), 304 with two (`return true` /
    `end`, `return {}` / `end`), and single hashes with 32 partners apiece. Those
    are shared idioms, not renames, and a hint that fires 1,328 times is not a
    hint. So a partner must have
      * at least MIN_RENAME_BODY distinct non-blank body lines, and
      * at most MAX_RENAME_PARTNERS candidates on the other side.
    Both rejections are COUNTED in the banner rather than hidden, because "we
    looked and it was too generic to say" is a different answer from "no match".
    """
    added = [r for r in rows if r["kind"] == "added"]
    removed = [r for r in rows if r["kind"] == "removed"]
    trivial = ambiguous = 0
    # matched on ihash, NOT hash: a rename by definition changes the
    # declaration line, so the whole-span hashes of two halves of one rename
    # can never agree. (The falsifier caught this; the first version matched on
    # `hash` and reported zero renames on a planted one.)
    by_hash = {}
    for r in removed:
        by_hash.setdefault(r["ihash107"], []).append(r)
    for r in added:
        partners = by_hash.get(r["ihash110"], [])
        if not partners:
            continue
        if len(set(r["body110"])) < MIN_RENAME_BODY:
            trivial += 1
            continue
        if len(partners) > MAX_RENAME_PARTNERS:
            ambiguous += 1
            continue
        for p in partners:
            r["flags"].append("RENAME?%s:%s" % (p["file"], p["key"]))
            p["flags"].append("RENAME?%s:%s" % (r["file"], r["key"]))
    # fuzzy: >= 90% of the larger body's distinct non-blank lines in common.
    # Size-filtered so this stays O(n * small) rather than O(n^2) over the tree.
    by_size = {}
    for p in removed:
        by_size.setdefault(len(set(p["body107"])) // 4, []).append(p)
    for r in added:
        if any(f.startswith("RENAME?") for f in r["flags"]):
            continue
        s = set(r["body110"])
        if len(s) < MIN_RENAME_BODY:
            continue                            # too small to be evidence
        for bkt in (len(s) // 4 - 1, len(s) // 4, len(s) // 4 + 1):
            for p in by_size.get(bkt, []):
                t = set(p["body107"])
                if not t:
                    continue
                if len(s & t) / float(max(len(s), len(t))) >= 0.90:
                    r["flags"].append("RENAME?~%s:%s" % (p["file"], p["key"]))
                    p["flags"].append("RENAME?~%s:%s" % (r["file"], r["key"]))
                    break
    if stats is not None:
        stats["rename_trivial"] = trivial
        stats["rename_ambiguous"] = ambiguous


# --------------------------------------------------------------------------- #
# output
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# STORAGE.tsv -- class (c), "same concept, new home". `Landscapes` went GameVar
# -> MapVar and the walk consts went `const.` -> `g_Consts`; both were invisible
# to every instrument the project owned.
# --------------------------------------------------------------------------- #
STORAGE_FORMS = (
    ("GlobalVar", re.compile(r"^\s*GlobalVar\s*\(\s*[\"']([\w.]+)[\"']")),
    ("MapVar",    re.compile(r"^\s*MapVar\s*\(\s*[\"']([\w.]+)[\"']")),
    ("GameVar",   re.compile(r"^\s*GameVar\s*\(\s*[\"']([\w.]+)[\"']")),
    ("PersistableGlobals", re.compile(r"^\s*PersistableGlobals\.([\w.]+)\s*=")),
    ("const",     re.compile(r"^\s*const\.([\w.]+)\s*=")),
    ("g_Consts",  re.compile(r"^\s*g_Consts\.([\w.]+)\s*=")),
)
# the same calls with a non-literal name (`GameVar(modified_name, ...)`): a
# storage declaration this tool cannot name. COUNTED, never dropped -- an
# unnameable declaration is a hole, and a hole that is not counted is a lie.
STORAGE_DYNAMIC = re.compile(r"^\s*(GlobalVar|MapVar|GameVar)\s*\(\s*(?![\"'])")


def scan_storage(root):
    found, dynamic = {}, []
    for dp, _d, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith(".lua"):
                continue
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel.startswith("DLC/"):
                continue
            for n, line in enumerate(read_lines(p), 1):
                for kind, rx in STORAGE_FORMS:
                    m = rx.match(line)
                    if m:
                        found.setdefault((kind, m.group(1)), []).append((rel, n))
                        break
                else:
                    if STORAGE_DYNAMIC.match(line):
                        dynamic.append((rel, n, line.strip()))
    return found, dynamic


def storage_rows(old_root, new_root):
    old, dyn_o = scan_storage(old_root)
    new, dyn_n = scan_storage(new_root)
    # index by NAME so a kind change (GameVar -> MapVar) is one row, not two
    o_by_name, n_by_name = {}, {}
    for (kind, name), sites in old.items():
        o_by_name.setdefault(name, []).append((kind, sites))
    for (kind, name), sites in new.items():
        n_by_name.setdefault(name, []).append((kind, sites))
    rows = []
    for name in sorted(set(o_by_name) | set(n_by_name)):
        a, z = o_by_name.get(name), n_by_name.get(name)
        if a and z:
            ak = ",".join(sorted(k for k, _s in a))
            zk = ",".join(sorted(k for k, _s in z))
            af = ",".join(sorted(set(f for _k, s in a for f, _n in s)))
            zf = ",".join(sorted(set(f for _k, s in z for f, _n in s)))
            bits = []
            if ak != zk:
                bits.append("kind-changed")
            if af != zf:
                bits.append("moved-file")
            status = "+".join(bits) or "same"
            al = ",".join(str(n) for _k, s in a for _f, n in s)
            zl = ",".join(str(n) for _k, s in z for _f, n in s)
        elif z:
            zk = ",".join(sorted(k for k, _s in z))
            zf = ",".join(sorted(set(f for _k, s in z for f, _n in s)))
            zl = ",".join(str(n) for _k, s in z for _f, n in s)
            ak = af = al = ""
            status = "added"
        else:
            ak = ",".join(sorted(k for k, _s in a))
            af = ",".join(sorted(set(f for _k, s in a for f, _n in s)))
            al = ",".join(str(n) for _k, s in a for _f, n in s)
            zk = zf = zl = ""
            status = "removed"
        rows.append([name, ak, zk, af, al, zf, zl, status])
    return rows, dyn_o, dyn_n


# --------------------------------------------------------------------------- #
# FILES.tsv -- the added and removed files. ⛔ THE METHOD RULE: for a REMOVED
# file the presence side is ENUMERATED mechanically. "grep found 0 hits" can
# only prove a NAME is gone; a nonzero count here says "moved", not "gone", and
# the project has already nearly retired a live fix by confusing the two.
# --------------------------------------------------------------------------- #
def files_rows(old_root, new_root, file_class, old_files, new_files):
    # one pass over the whole 1.1.0 tree, so "is this name still anywhere?" is
    # answered from an index instead of 36 tree greps
    present = set()
    for rel, p in new_files.items():
        if rel.startswith("DLC/") or not rel.endswith(".lua"):
            continue
        for d in declarations(read_lines(p)):
            present.add(d["key"].split("#")[0])
            present.add(d["key"].split(".")[-1].split("#")[0])
    rows = []
    for rel in sorted(list(set(old_files) | set(new_files))):
        st = file_class.get(rel)
        if st not in ("added", "removed"):
            continue
        b = bucket(rel)
        if rel.endswith(".lua"):
            src = new_files[rel] if st == "added" else old_files[rel]
            names = [d["key"].split("#")[0] for d in declarations(read_lines(src))]
        else:
            names = []
        if st == "removed":
            still = [n for n in names
                     if n in present or n.split(".")[-1] in present]
            rows.append([rel, st, b, len(names), len(still),
                         "; ".join(sorted(set(still))[:8])])
        else:
            rows.append([rel, st, b, len(names), "", ""])
    return rows


# --------------------------------------------------------------------------- #
# CALLERS.tsv -- class (b'). ⭐ THE HIGHEST-YIELD ROW CLASS IN THIS CHAIN: a
# call line that is byte-identical across the two trees, against a callee whose
# SIGNATURE moved, is the F117 shape exactly -- the developers' own bug, where
# the callee's contract changed and a caller kept the old one.
# --------------------------------------------------------------------------- #
CALL_SKIP = re.compile(r"^\s*(?:local\s+)?function\b|^\s*[\w.:]+\s*=\s*function\s*\(")


def scan_calls(root, names):
    """name -> file -> ordered [(line, text)]. Text-level; see the banner."""
    rx = re.compile(r"[.:]?\b(%s)\s*\(" % "|".join(sorted(map(re.escape, names),
                                                          key=len, reverse=True)))
    out = {}
    for dp, _d, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith(".lua"):
                continue
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel.startswith("DLC/"):
                continue
            for n, line in enumerate(read_lines(p), 1):
                if CALL_SKIP.match(line):
                    continue                    # a declaration is not a call
                for m in rx.finditer(line):
                    out.setdefault(m.group(1), {}).setdefault(rel, []) \
                       .append((n, line.strip()))
                    break                       # one row per line per name-hit
    return out


def caller_rows(old_root, new_root, rows):
    targets = {}
    for r in rows:
        if r["kind"] in ("sig", "body+sig") and r["bucket"] == "hand":
            bare = bare_name(r["key"])
            targets.setdefault(bare, []).append(r)
    if not targets:
        return [], {}
    o = scan_calls(old_root, targets)
    n = scan_calls(new_root, targets)
    out, tally = [], dict(same=0, changed=0, new=0, gone=0)
    for bare in sorted(targets):
        owner = targets[bare][0]
        oc, nc = o.get(bare, {}), n.get(bare, {})
        for f in sorted(set(oc) | set(nc)):
            a, z = oc.get(f, []), nc.get(f, [])
            for k in range(max(len(a), len(z))):
                ao = a[k] if k < len(a) else None
                zo = z[k] if k < len(z) else None
                if ao and zo:
                    status = "same" if ao[1] == zo[1] else "changed"
                elif zo:
                    status = "new"
                else:
                    status = "gone"
                tally[status] += 1
                out.append([owner["file"], owner["key"], bare, f,
                            ao[0] if ao else "", zo[0] if zo else "", status,
                            (zo or ao)[1][:200]])
    return out, tally


def banner(old_root, new_root, stats, extra=()):
    cmd = "python " + " ".join([os.path.basename(sys.argv[0])] + sys.argv[1:])
    out = ["# %s | old=%s digest=%s | new=%s digest=%s | %s | %s"
           % (VERSION, old_root, tree_digest(old_root), new_root,
              tree_digest(new_root), cmd,
              datetime.date.today().isoformat())]
    out.append("# NORMALISATION: CRLF->LF, trailing whitespace stripped per line; "
               "leading indentation KEPT; ⭐ COMMENTS ARE KEPT AND COUNT — a "
               "whitespace-only diff is NOT a row, a changed comment IS a row.")
    out.append("# DELIMITER: luafn.find_bodies, imported not re-implemented. "
               "Keys collapse `Class:Method` and `Class.Method`; the separator "
               "actually written is the first character of the sig columns.")
    out.append("# COVERAGE (v1.1): indent-0 declarations, five forms "
               "(function C:M / function C.M / function G / local function f / "
               "[local] x = function), PLUS every INDENTED declaration of those "
               "forms that lies OUTSIDE every enumerated span — table-field "
               "methods, sequence `Run = function(seq_state)` steps, file-level "
               "nested locals — keyed `name@<anchor>` and flagged INDENTED "
               "(ONE-LINE when the declaration closes itself: that row hashes "
               "its own line only, deliberately, so a neighbour's edit cannot "
               "re-hash it; the indent-0 pass keeps the delimiter's over-span "
               "untouched, checklist 135). Indented declarations INSIDE an "
               "enumerated span are covered by the outer body's hash and not "
               "listed. Orphans on the 1.1.0 side: %d in `hand` files, %d in "
               "`generated` (%d one-line); %d identical across the trees, %d "
               "rows. Total indented declarations for comparison: %d (%d hand, "
               "%d generated). STILL NOT COVERED: every anonymous `function(` "
               "literal passed as an argument. ⛔ A function never emitted is "
               "not a function that did not change."
               % (stats["orphan_hand"], stats["orphan_generated"],
                  stats["orphan_oneline"], stats["orphan_identical"],
                  stats["orphan_rows"],
                  stats["indented_hand"] + stats["indented_generated"],
                  stats["indented_hand"], stats["indented_generated"]))
    out.append("# FILES: changed=%d identical=%d added=%d removed=%d "
               "(DLC/ excluded: %d paths). ⭐ MANIFEST RE-DERIVATION CONTROL vs "
               "chain README §0 (which counts DLC): 2437+7=2444 changed, "
               "1963+5=1968 identical, 166+139=305 added, 36+0=36 removed — "
               "MATCHES; the 139 DLC adds are 138 `DLC/norman` + 1 `DLC/thomas`."
               % (stats["changed"], stats["identical"], stats["added"],
                  stats["removed"], stats["dlc_skipped"]))
    out.append("# FPK PARITY (EF-085, measured 2026-09-10): every `Lua/`, "
               "`CommonLua/` and `Data/` file in the archived 1.1.0 Src ships "
               "BYTE-IDENTICAL in Packs\\Lua.fpk / Packs\\Data.fpk — 0 divergent. "
               "⇒ NO ROW CARRIES `FPK-DIVERGENT`, because there is nothing to "
               "flag. ⛔ That proves the bytes match, not that the game executes "
               "them (EF-078 stands).")
    out.append("# FUNCTIONS: 1.0.7=%d 1.1.0=%d | IDENTICAL (counted, not listed)=%d "
               "| SPAN-SUSPECT=%d declarations (the one-line-function trap, "
               "MEASURED — see the tool header; ⛔ NOT fixed here, a delimiter "
               "change re-hashes every SRC: pin in Code/) | MULTI=%d "
               "declarations | spans reaching EOF=%d"
               % (stats["fn_old"], stats["fn_new"], stats["fn_identical"],
                  stats["span_suspect"], stats["multi"], stats["span_eof"]))
    out.append("# RENAME? is a HINT, never a verdict, and it is GUARDED: a "
               "partner needs >=%d distinct non-blank body lines and <=%d "
               "candidates. Rejected as too trivial to be evidence: %d added "
               "rows (bodies like `end` or `return true`); rejected as "
               "ambiguous (one body, many partners): %d. Those are NOT `no "
               "match` — they are `too generic to say`."
               % (MIN_RENAME_BODY, MAX_RENAME_PARTNERS,
                  stats.get("rename_trivial", 0), stats.get("rename_ambiguous", 0)))
    for e in extra:
        out.append("# " + e)
    return out


def write_tsv(path, banner_lines, header, rows):
    import io
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        for b in banner_lines:
            fh.write(b + "\n")
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c).replace("\t", " ").replace("\n", " ")
                               for c in r) + "\n")
    print("  wrote %s (%d rows)" % (path, len(rows)))


# --------------------------------------------------------------------------- #
# --selftest: the falsifier. ⛔ An instrument nobody has watched FAIL is not an
# instrument. Every verdict below fires on a planted case, and the two negative
# cases (whitespace-only, reorder-free) must NOT fire.
# --------------------------------------------------------------------------- #
OLD_FIX = {
"Lua/A.lua": [
    "function Body:Same(a, b)",
    "\tlocal x = a + b",
    "\treturn x",
    "end",
    "",
    "function LeadingParam(mark, callback, ...)",
    "\treturn callback(mark)",
    "end",
    "",
    "function GoesAway(x)",
    "\treturn x",
    "end",
    "",
    "-- a comment that will change",
    "function CommentOnly(x)",
    "\t-- the OLD note",
    "\treturn x",
    "end",
    "",
    "function OldName(v)",
    "\tlocal q = v * 2",
    "\tlocal r = q + 1",
    "\treturn r",
    "end",
    "",
    "function OneLiner() return 1 end",
    "function AfterTheOneLiner(z)",
    "\treturn z",
    "end",
    "",
    "function Dup(a)",
    "\treturn 1",
    "end",
    "function Dup(a)",
    "\treturn 2",
    "end",
    "",
],
"Lua/Ws.lua": [
    "function WhitespaceOnly(a)   ",
    "\treturn a\t",
    "end",
    "",
],
# v1.1 — the indented orphans (table-field methods and sequence steps)
"Lua/T.lua": [
    "DefineClass.Thing = {",
    "\tGetA = function(self) return self.a end,",
    "\tSetB = function(self, b)",
    "\t\tself.b = b",
    "\tend,",
    "\tNested = function(self)",
    "\t\tlocal function inner(x)",
    "\t\t\treturn x",
    "\t\tend",
    "\t\treturn inner(1)",
    "\tend,",
    "}",
    "function Outer(y)",
    "\tlocal function innerOuter(z)",
    "\t\treturn z + 1",
    "\tend",
    "\treturn innerOuter(y)",
    "end",
    "PlaceObj('Sequence', {",
    "\tRun = function(seq_state)",
    "\t\treturn 1",
    "\tend,",
    "\tRun = function(seq_state)",
    "\t\treturn 2",
    "\tend,",
    "})",
    "",
],
}
NEW_FIX = {
"Lua/A.lua": [
    "function Body:Same(a, b)",
    "\tlocal x = a - b            -- the planted BODY change",
    "\treturn x",
    "end",
    "",
    "function LeadingParam(map, mark, callback, ...)",
    "\treturn callback(mark)",
    "end",
    "",
    "-- a comment that will change",
    "function CommentOnly(x)",
    "\t-- the NEW note",
    "\treturn x",
    "end",
    "",
    "function NewName(v)",
    "\tlocal q = v * 2",
    "\tlocal r = q + 1",
    "\treturn r",
    "end",
    "",
    "function OneLiner() return 1 end",
    "function AfterTheOneLiner(z)",
    "\treturn z",
    "end",
    "",
    "function Dup(a)",
    "\treturn 1",
    "end",
    "function Dup(a)",
    "\treturn 2",
    "end",
    "",
    "function BrandNew(q)",
    "\treturn q",
    "end",
    "",
],
"Lua/Ws.lua": [
    "function WhitespaceOnly(a)",
    "\treturn a",
    "end",
    "",
],
"Lua/T.lua": [
    "DefineClass.Thing = {",
    "\tGetA = function(self) return self.a2 end,",
    "\tNewField = function(self) return 0 end,",
    "\tSetB = function(self, b)",
    "\t\tself.b = b",
    "\tend,",
    "\tNested = function(self)",
    "\t\tlocal function inner(x)",
    "\t\t\treturn x",
    "\t\tend",
    "\t\treturn inner(1)",
    "\tend,",
    "}",
    "function Outer(y)",
    "\tlocal function innerOuter(z)",
    "\t\treturn z + 2",
    "\tend",
    "\treturn innerOuter(y)",
    "end",
    "PlaceObj('Sequence', {",
    "\tRun = function(seq_state)",
    "\t\treturn 0",
    "\tend,",
    "\tRun = function(seq_state)",
    "\t\treturn 1",
    "\tend,",
    "\tRun = function(seq_state)",
    "\t\treturn 2",
    "\tend,",
    "})",
    "",
],
}


def _plant(root, files, crlf=()):
    for rel, lines in files.items():
        p = os.path.join(root, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        nl = "\r\n" if rel in crlf else "\n"
        with open(p, "wb") as fh:
            fh.write(nl.join(lines).encode("utf-8"))


def selftest(old_root, new_root, break_one=None):
    ok = True

    def check(label, cond, detail=""):
        nonlocal ok
        ok = ok and cond
        print("  %-6s %s%s" % ("PASS" if cond else "FAIL", label,
                               ("   -> " + detail) if detail and not cond else ""))

    print("=" * 78)
    print("PART 1 — planted fixtures (two tiny trees; the NEW side is CRLF, so a")
    print("         line-ending difference is under every single assertion below)")
    tmp = tempfile.mkdtemp(prefix="treediff_selftest_")
    o, n = os.path.join(tmp, "old"), os.path.join(tmp, "new")
    _plant(o, OLD_FIX)
    _plant(n, NEW_FIX, crlf=("Lua/A.lua", "Lua/Ws.lua"))
    rows, stats, _fc = diff(o, n)
    got = {(r["file"], r["key"]): r for r in rows}

    def row(f, k):
        return got.get((f, k))

    r = row("Lua/A.lua", "Body.Same")
    check("planted BODY change, name + arity identical -> kind=body",
          r is not None and r["kind"] == "body" and not r["flags"],
          repr(r and (r["kind"], r["flags"])))
    r = row("Lua/A.lua", "LeadingParam")
    check("planted LEADING parameter (the F115 shape) -> kind=sig",
          r is not None and r["kind"] == "sig"
          and r["sig107"] == ".mark,callback,..." and r["sig110"] == ".map,mark,callback,...",
          repr(r and (r["kind"], r["sig107"], r["sig110"])))
    r = row("Lua/A.lua", "GoesAway")
    check("planted REMOVAL -> kind=removed",
          r is not None and r["kind"] == "removed", repr(r and r["kind"]))
    r = row("Lua/A.lua", "BrandNew")
    check("planted ADDITION -> kind=added",
          r is not None and r["kind"] == "added", repr(r and r["kind"]))
    a, z = row("Lua/A.lua", "OldName"), row("Lua/A.lua", "NewName")
    check("planted RENAME, identical body -> RENAME? on BOTH partners, named",
          a is not None and z is not None
          and any(f == "RENAME?Lua/A.lua:NewName" for f in a["flags"])
          and any(f == "RENAME?Lua/A.lua:OldName" for f in z["flags"]),
          repr((a and a["flags"], z and z["flags"])))
    check("⛔ CRLF + trailing-space-only change is NOT A ROW",
          row("Lua/Ws.lua", "WhitespaceOnly") is None,
          repr(row("Lua/Ws.lua", "WhitespaceOnly")))
    r = row("Lua/A.lua", "CommentOnly")
    check("⭐ a changed COMMENT *is* a row (bodycheck keeps comments)",
          r is not None and r["kind"] == "body", repr(r and r["kind"]))
    # the one-line-function trap: pin whatever the delimiter does, so a future
    # change to luafn.py becomes visible here instead of silently re-hashing.
    ol = row("Lua/A.lua", "OneLiner")
    print("  ---- the one-line-function trap, pinned (NOT fixed here) ----")
    olds = declarations(read_lines(os.path.join(o, "Lua", "A.lua")))
    d = [x for x in olds if x["key"] == "OneLiner"][0]
    over = d["span"][1] - d["span"][0] + 1
    check("`function OneLiner() return 1 end` OVER-SPANS past its own end "
          "(pinned at %d lines, and the next function is inside it)" % over,
          over > 1 and d["self_closing"], "span=%r" % (d["span"],))
    check("...and the row it produces is flagged SPAN-SUSPECT (or it is "
          "identical on both sides and produces no row)",
          ol is None or "SPAN-SUSPECT" in ol["flags"], repr(ol and ol["flags"]))
    dup = [k for (f, k) in got if f == "Lua/A.lua" and k.startswith("Dup")]
    alld = [x for x in olds if x["key"].startswith("Dup")]
    check("duplicate declaration -> ordinal keys Dup#1/Dup#2 and MULTI",
          sorted(x["key"] for x in alld) == ["Dup#1", "Dup#2"]
          and all(x["multi"] for x in alld),
          repr([x["key"] for x in alld]))
    print("  ---- v1.1: indented orphans (table-field methods, sequence steps) ----")
    trows = {k: r for (f, k), r in got.items() if f == "Lua/T.lua"}
    by_bare = {}
    for k, r in trows.items():
        by_bare.setdefault(bare_name(k), []).append(r)
    r = by_bare.get("GetA", [None])[0]
    check("planted change in a ONE-LINE table-field method -> kind=body, "
          "flags INDENTED+ONE-LINE",
          r is not None and r["kind"] == "body"
          and "INDENTED" in r["flags"] and "ONE-LINE" in r["flags"],
          repr(r and (r["kind"], r["flags"])))
    r = by_bare.get("NewField", [None])[0]
    check("planted NEW table-field method -> kind=added, INDENTED",
          r is not None and r["kind"] == "added" and "INDENTED" in r["flags"],
          repr(r and (r["kind"], r["flags"])))
    check("⛔ the UNCHANGED sibling below the insertion (SetB) is NOT a row",
          "SetB" not in by_bare, repr(by_bare.get("SetB")))
    check("⛔ an indented declaration INSIDE an orphan (inner) is NOT a row",
          "inner" not in by_bare, repr(by_bare.get("inner")))
    r = by_bare.get("Outer", [None])[0]
    check("a change inside a NESTED local surfaces as the OUTER function's "
          "body row, and the nested local is not its own row",
          r is not None and r["kind"] == "body" and "innerOuter" not in by_bare,
          repr((r and r["kind"], by_bare.get("innerOuter"))))
    runs = by_bare.get("Run", [])
    check("an inserted sequence step among same-named `Run` steps -> exactly "
          "ONE added row (hash-matching cancels the shifted siblings)",
          len(runs) == 1 and runs[0]["kind"] == "added"
          and "MULTI" in runs[0]["flags"],
          repr([(x["kind"], x["flags"]) for x in runs]))
    shutil.rmtree(tmp, ignore_errors=True)

    print()
    print("PART 2 — the REAL trees: the four seeded positives of chain README §4.")
    print("         ⭐ These are the control. An inventory that cannot see them")
    print("            is not reporting on the other 2,437 files either.")
    if not (os.path.isdir(old_root) and os.path.isdir(new_root)):
        print("  SKIP   archives not on disk (%s / %s)" % (old_root, new_root))
        return 0 if ok else 1

    seeds = (
        ("Lua/Units/Train.lua", "Train.UnloadAll", "body", None, "F114"),
        ("Lua/Landscape/Landscaping.lua", "LandscapeForEachUnit", "sig",
         (".mark,callback,...", ".map,mark,callback,..."), "F115"),
        ("Lua/Buildings/TrackElement.lua", "TrackGridElement.DemolishAndSplitTrack",
         "body", None, "F116"),
        ("Lua/_GameUtils.lua", "ChooseDome", "sig", None, "F117"),
    )
    for rel, key, want, wantsig, tag in seeds:
        old_p = os.path.join(old_root, rel.replace("/", os.sep))
        new_p = os.path.join(new_root, rel.replace("/", os.sep))
        if not (os.path.isfile(old_p) and os.path.isfile(new_p)):
            check("%s %s:%s — both files present" % (tag, rel, key), False,
                  "missing on one side")
            continue
        od = {d["key"]: d for d in declarations(read_lines(old_p))}
        nd = {d["key"]: d for d in declarations(read_lines(new_p))}
        a, z = od.get(key), nd.get(key)
        if not (a and z):
            check("%s %s:%s — found in both trees" % (tag, rel, key), False,
                  "old=%s new=%s" % (bool(a), bool(z)))
            continue
        body_ch, sig_ch = a["hash"] != z["hash"], a["sig"] != z["sig"]
        kind = ("body+sig" if body_ch and sig_ch else "sig" if sig_ch else
                "body" if body_ch else "identical")
        good = (kind == want) or (want == "sig" and kind == "body+sig")
        check("%s  %s:%s  ->  %s   [1.0.7 %s:%d | 1.1.0 %s:%d]"
              % (tag, rel, key, kind, a["sep"] + a["sig"], a["line"],
                 z["sep"] + z["sig"], z["line"]),
              good, "expected %s" % want)
        if wantsig:
            check("      ...and its parameter list moved %s -> %s"
                  % wantsig,
                  (a["sep"] + a["sig"], z["sep"] + z["sig"]) == wantsig,
                  repr((a["sep"] + a["sig"], z["sep"] + z["sig"])))

    if break_one:
        print()
        print("  (--break-one active: one assertion was inverted on purpose)")
    print("=" * 78)
    print("SELFTEST: %s" % ("PASS — every verdict fired on a known case"
                            if ok else "*** FAIL ***"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--old", default=DEFAULT_OLD)
    ap.add_argument("--new", default=DEFAULT_NEW)
    ap.add_argument("--out", help="directory to write INVENTORY.tsv into")
    ap.add_argument("--selftest", action="store_true", help="run the falsifier")
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.old, a.new)
    print("diffing\n  old %s\n  new %s" % (a.old, a.new))
    rows, stats, file_class = diff(a.old, a.new, progress=True)
    kinds = {}
    for r in rows:
        kinds[(r["kind"], r["bucket"])] = kinds.get((r["kind"], r["bucket"]), 0) + 1
    print("rows: %d" % len(rows))
    for k in sorted(kinds):
        print("  %-10s %-10s %d" % (k[0], k[1], kinds[k]))
    if not a.out:
        return 0
    os.makedirs(a.out, exist_ok=True)
    write_tsv(os.path.join(a.out, "INVENTORY.tsv"),
              banner(a.old, a.new, stats),
              ["file", "function", "kind", "bucket", "line107", "line110",
               "sig107", "sig110", "flags"],
              [[r["file"], r["key"], r["kind"], r["bucket"], r["line107"],
                r["line110"], r["sig107"], r["sig110"], ",".join(r["flags"])]
               for r in sorted(rows, key=lambda r: (r["file"], r["key"]))])

    print("  storage...")
    srows, dyn_o, dyn_n = storage_rows(a.old, a.new)
    st = {}
    for r in srows:
        st[r[7]] = st.get(r[7], 0) + 1
    write_tsv(os.path.join(a.out, "STORAGE.tsv"),
              banner(a.old, a.new, stats, extra=[
                  "STORAGE: class (c), 'same concept, new home' — the shape that "
                  "moved `Landscapes` GameVar->MapVar and the walk consts "
                  "`const.`->`g_Consts`, and that NO instrument this project owns "
                  "sees. Forms scanned: " +
                  ", ".join(k for k, _ in STORAGE_FORMS) + ".",
                  "STATUS COUNTS: " + " ".join("%s=%d" % kv for kv in sorted(st.items())),
                  "⛔ PRESENCE SIDE, ENUMERATED: `GlobalVar(\"…\")` has %d "
                  "declarations in 1.0.7 and %d in 1.1.0 — the form exists in "
                  "`CommonLua/Core/lib.lua` but the game declares through "
                  "GameVar/MapVar. Zero is a MEASUREMENT here, not an omission."
                  % (sum(1 for r in srows if "GlobalVar" in r[1]),
                     sum(1 for r in srows if "GlobalVar" in r[2])),
                  "⚠️ NOT NAMEABLE BY THIS TOOL: %d dynamic declarations in 1.0.7 "
                  "and %d in 1.1.0 (`GameVar(modified_name, …)` — the name is a "
                  "variable). They are storage this row set does not cover."
                  % (len(dyn_o), len(dyn_n)),
                  "⚠️ NOT COVERED AT ALL: `ConstDef` preset definitions, which is "
                  "where most consts are actually DEFINED — `presetdiff.py` reads "
                  "those. `const.X =` here is the Lua-side assignment only.",
              ]),
              ["name", "kind107", "kind110", "file107", "line107", "file110",
               "line110", "status"], srows)

    print("  files...")
    old_files, new_files = tree_files(a.old), tree_files(a.new)
    frows = files_rows(a.old, a.new, file_class, old_files, new_files)
    rm = [r for r in frows if r[1] == "removed"]
    moved = [r for r in rm if r[4] and int(r[4]) > 0]
    write_tsv(os.path.join(a.out, "FILES.tsv"),
              banner(a.old, a.new, stats, extra=[
                  "FILES: the added and removed files (DLC/ excluded — the 305/36 "
                  "of chain README §0 include 139 DLC adds; here that is %d added "
                  "and %d removed)." % (stats["added"], stats["removed"]),
                  "⛔ THE METHOD RULE, MECHANISED. `names_still_in_110` is the "
                  "PRESENCE SIDE for every removed file: how many of the names it "
                  "declared are still declared SOMEWHERE in the 1.1.0 tree. A "
                  "NONZERO COUNT SAYS 'MOVED', NOT 'GONE'. %d of the %d removed "
                  "files have a nonzero count. ⛔ This is a HINT for a reader, not "
                  "a verdict: a surviving name can be an unrelated homonym, and a "
                  "zero count still only proves the NAME is gone, never the "
                  "FEATURE (search for the capability — the preset, the UI string, "
                  "the inheriting class)." % (len(moved), len(rm)),
              ]),
              ["path", "status", "bucket", "declared_names",
               "names_still_in_110", "sample_of_surviving_names"], frows)

    print("  callers...")
    crows, tally = caller_rows(a.old, a.new, rows)
    byfile = {}
    for r in crows:
        if r[6] == "same":
            byfile[r[3]] = byfile.get(r[3], 0) + 1
    top = sorted(byfile.items(), key=lambda kv: -kv[1])[:12]
    write_tsv(os.path.join(a.out, "CALLERS.tsv"),
              banner(a.old, a.new, stats, extra=[
                  "CALLERS: class (b′). Every call site, in BOTH trees, of every "
                  "`sig` or `body+sig` function in a `hand` file (%d callees)."
                  % len(set(r["key"] for r in rows
                            if r["kind"] in ("sig", "body+sig") and r["bucket"] == "hand")),
                  "⭐⭐ READ THIS FIRST: **a `same` call line against a CHANGED "
                  "SIGNATURE is the F117 shape, and it is the single "
                  "highest-yield row class in this chain.** The callee's contract "
                  "moved; this call site's text did not. F117 is exactly that, and "
                  "the developers wrote it themselves. status counts: " +
                  " ".join("%s=%d" % kv for kv in sorted(tally.items())),
                  "`same`-against-changed-signature by file, top 12: " +
                  " | ".join("%s=%d" % kv for kv in top),
                  "⛔ TEXT-LEVEL, AND THAT IS THE WHOLE BOUND. Matching is `Name(`, "
                  "`:Name(`, `.Name(` by text on the bare name, so it CANNOT see a "
                  "dynamic dispatch (`self[name]`, a preset's `func` field, `Msg` "
                  "handlers — chain blind spot 7), it cannot tell two classes' "
                  "same-named methods apart, and it counts a mention inside a "
                  "string or a comment. ⛔ IT DOES NOT BOUND REACH.",
                  "PAIRING RULE, stated because it is an assumption: within one "
                  "file, the k-th call site of a name in 1.0.7 is paired with the "
                  "k-th in 1.1.0. Equal text => `same`, different => `changed`, "
                  "unpaired => `new`/`gone`. If call sites were REORDERED inside a "
                  "file, that pairing mislabels — read the line, not the label.",
              ]),
              ["callee_file", "callee_function", "name", "call_file",
               "call_line107", "call_line110", "status", "call_text"], crows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
