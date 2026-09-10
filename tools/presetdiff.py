#!/usr/bin/env python3
"""What did the game change inside its PRESET DATA between two ModTools/Src trees?

Written 2026-09-10 for `prompts/vanillahunt/01_INVENTORY.md` unit B2, beside
`treediff.py` and under the same discipline.

⛔ THE GAP THIS TOOL EXISTS TO CLOSE. Of the 2,444 files the game changed
between 1.0.7.396349 and 1.1.0.403908, **1,630 are generated preset data** --
`PlaceObj('Class', { key = value, … })` blocks exported by the in-game editors.
A function-level differ reads all of it as noise, so the chain's first draft
would have written off two thirds of the diff as unreadable. It is not
unreadable; it is a different shape. This reads it at FIELD level: one row per
KEY whose value moved.

    python tools/presetdiff.py --selftest      # the falsifier -- run it first
    python tools/presetdiff.py --out <dir>     # write PRESETS.tsv
    python tools/presetdiff.py --sample T-ID   # print rows of one churn class

PRESET IDENTITY IS `class::id::group`, NOT THE FILE -- because that is how the
GAME identifies a preset, and a file is only where the editor happened to write
it. ⚠️ MEASURED, so the justification is not a story: on these two trees 17
generated files exist only in 1.0.7 and 59 only in 1.1.0, but **0 matched
presets changed file**. So file-keying would NOT in fact have produced the
thousands of false rows an earlier draft of this header asserted; the identity
choice is right on principle and the file churn is smaller than claimed. The
file each side was found in is carried as a COLUMN, and a preset whose file
moved is flagged `FILE-MOVED`.

⭐ AND THE REGISTRY THIS SURFACED: 1.0.7 has 264 `TechPreset` presets; 1.1.0 has
274 `TechPreset` **and** 441 `Tech`, with 258 of 1.0.7's TechPreset ids present
under BOTH classes in 1.1.0. The tech registry exists twice in the new build.
⛔ What that MEANS is a reader's question (chain link 04), not this tool's.

⭐ CHURN CLASSES ARE RULES THE TOOL APPLIES, and every one of them is a CLAIM
about a row being uninteresting -- which is exactly the kind of claim this
project has been burned by. So each is stated as a rule, each is applied
mechanically, and `--sample` prints rows of any class so a human can falsify it.
⛔ A single row where the rule hid a REAL value change voids that class.

  T-ID     both sides are `T(<id>, "<text>")`, the ids differ, the TEXT is
           byte-identical. A localisation id was reissued; nothing a player can
           see moved. ⚠️ If the text ALSO changed the row is `none`, never T-ID.
  FORMAT   the raw texts differ but the parsed VALUES are equal -- number
           spelling (`10000` / `1e4` / `10000.0`), quote style, trailing commas.
  SAVE-ID  the key is an editor bookkeeping field (`save_in`, `PresetIdCounter`,
           `__index`), which records where the editor wrote the preset and not
           what it contains.
  COMMENT  the only difference lies inside a `--[[ … ]]` comment (the editors
           embed the localisation context there).
  REINDEX  one side is `<absent>` and that exact value is still present in the
           other tree under the same index-free key -- an array element moved
           position. ⭐ PROVEN on a read pair: `XDef:ipTrack`'s
           `T(529, "Today…")` leaves `children[6]` and arrives at `children[5]`,
           two rows, one value.
  REINDEX-SWAP
           ⚠️ THE WEAK ONE, AND IT IS SEPARATE FOR THAT REASON. Both sides hold
           a real value and each is accounted for elsewhere. Consistent with a
           reordering -- and equally consistent with a genuine change at that
           position, which the tool CANNOT distinguish. Where a list's order is
           semantic (`Parameters`, `likes`, `Effects`) this class must be READ,
           not skipped. It exists because reading 20 `REINDEX` rows showed the
           two halves do not deserve the same confidence.
  REORDER  ⛔ NOT A ROW, BY CONSTRUCTION. Rows are keyed by key PATH, so a
           preset whose keys were re-emitted in another order with equal values
           produces no row at all. The presets that moved this way are COUNTED
           in the banner, because "zero rows" and "we never looked" must not
           look the same.
  none     the readable pile. Everything the rules could not explain away.

⚠️ WHAT IT CANNOT DECIDE, AND MUST NOT BE READ AS DECIDING. Whether a `none`
row MATTERS -- that is a reader's job (04's registry agents). Whether a preset
is CONSUMED: a preset read only by C-side engine code has no Lua reader to find,
and this tool cannot tell a live field from a dead one. Whether the churn rules
are right on rows nobody sampled -- the banner reports the sample size per
class, and an unsampled class is an unfalsified claim.
"""

import argparse
import collections
import datetime
import hashlib
import io
import os
import random
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luafn import read_lines
from treediff import (DEFAULT_OLD, DEFAULT_NEW, GENERATED, tree_digest,
                      tree_files, write_tsv)

VERSION = "presetdiff.py v1 (2026-09-10)"

# nested scenario/storybit presets go deeper than CPython's default 1000 frames
sys.setrecursionlimit(20000)

SAVE_ID_KEYS = ("save_in", "PresetIdCounter", "__index", "SaveIn")


# --------------------------------------------------------------------------- #
# a tokenizer + recursive-descent reader for the Lua VALUE subset these
# generated files use. Not a Lua interpreter: strings, numbers, booleans, nil,
# tables, and calls (`T(…)`, `point(…)`, `set(…)`, nested `PlaceObj(…)`).
# --------------------------------------------------------------------------- #
TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<blockcomment>--\[(?P<beq>=*)\[.*?\](?P=beq)\])
  | (?P<comment>--[^\n]*)
  | (?P<longstring>\[(?P<leq>=*)\[.*?\](?P=leq)\])
  | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<number>-?(?:0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+))
  | (?P<name>[A-Za-z_][\w.]*)
  | (?P<punct>[{}(),=\[\]])
""", re.VERBOSE | re.DOTALL)


class Tok(object):
    __slots__ = ("kind", "text", "pos")

    def __init__(self, kind, text, pos):
        self.kind, self.text, self.pos = kind, text, pos


def lex(src):
    out, i, n = [], 0, len(src)
    while i < n:
        m = TOKEN.match(src, i)
        if not m:
            i += 1                              # unlexable byte: skip, do not die
            continue
        kind = m.lastgroup
        for k in ("ws", "blockcomment", "comment", "longstring", "string",
                  "number", "name", "punct"):
            if m.group(k) is not None:
                kind = k
                break
        if kind == "ws":
            pass
        elif kind in ("blockcomment", "comment"):
            out.append(Tok("comment", m.group(0), i))
        else:
            out.append(Tok(kind, m.group(0), i))
        i = m.end()
    return out


class Parser(object):
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self, skip_comments=True):
        j = self.i
        while skip_comments and j < len(self.t) and self.t[j].kind == "comment":
            j += 1
        return self.t[j] if j < len(self.t) else None

    def next(self, skip_comments=True):
        while skip_comments and self.i < len(self.t) \
                and self.t[self.i].kind == "comment":
            self.i += 1
        tok = self.t[self.i] if self.i < len(self.t) else None
        self.i += 1
        return tok

    def comments_ahead(self):
        out, j = [], self.i
        while j < len(self.t) and self.t[j].kind == "comment":
            out.append(self.t[j].text)
            j += 1
        return out

    def value(self):
        """-> (raw_text, python_value_or_marker). Never raises on odd input."""
        cs = self.comments_ahead()
        tok = self.next()
        if tok is None:
            return "", None
        if tok.kind in ("string", "longstring"):
            return tok.text, ("s", unquote(tok.text))
        if tok.kind == "number":
            return tok.text, ("n", num(tok.text))
        if tok.kind == "punct" and tok.text == "{":
            return self.table()
        if tok.kind == "name":
            if tok.text in ("true", "false"):
                return tok.text, ("b", tok.text == "true")
            if tok.text == "nil":
                return tok.text, ("z", None)
            if tok.text == "function":
                return self.function_value()
            nxt = self.peek()
            if nxt and nxt.kind == "punct" and nxt.text == "(":
                return self.call(tok.text, cs)
            return tok.text, ("i", tok.text)
        return tok.text, ("?", tok.text)

    # ⛔ EMBEDDED LUA IS ONE VALUE, NOT A HUNDRED ARRAY ITEMS.
    # `XDef` windows and `FlightPolicyDef` carry real code in preset fields
    # (`OnPress = function(self) … end`). Without this, `table()` failed to
    # parse each statement as `key = value`, fell through to its array branch,
    # and appended every stray token as an element -- so a one-line edit inside
    # one handler produced hundreds of rows whose "values" were `local`,
    # `then`, `end`, `dlg`. MEASURED before the fix: 42,072 such rows, every
    # one of them mis-explained by the REINDEX rule as positional churn. A
    # function body is now a single opaque leaf: a changed handler is ONE row
    # carrying its source, which is what a reader can act on.
    BLOCK_OPEN = ("function", "if", "do")        # `for`/`while` open via their `do`

    def function_value(self):
        parts, depth = ["function"], 1
        while self.i < len(self.t):
            tok = self.next(skip_comments=False)
            if tok is None:
                break
            if tok.kind == "comment":
                continue
            parts.append(tok.text)
            if tok.kind == "name":
                if tok.text in self.BLOCK_OPEN:
                    depth += 1
                elif tok.text == "end":
                    depth -= 1
                    if depth == 0:
                        break
        raw = " ".join(parts)
        return raw, ("f", re.sub(r"\s+", " ", raw))

    def call(self, name, cs):
        # ⚠️ NO MANUAL DEPTH COUNTING. The first version tracked bracket depth
        # here *and* let self.value() consume the nested structure, so the two
        # desynced, the loop never saw its own ')' and ran to the end of the
        # file -- which is how this arrived as a RecursionError on the real
        # trees rather than as a wrong answer. self.value() is already
        # recursive; arguments are just values separated by commas.
        self.next()                              # '('
        args = []
        while self.i < len(self.t):
            tok = self.peek()
            if tok is None:
                break
            if tok.kind == "punct" and tok.text == ")":
                self.next()
                break
            if tok.kind == "punct" and tok.text == ",":
                self.next()
                continue
            raw, val = self.value()
            args.append((raw, val))
        return "%s(%s)" % (name, ", ".join(r for r, _v in args)), \
               ("c", name, tuple(r for r, _v in args),
                tuple(v for _r, v in args), tuple(cs))

    def table(self):
        items, arr = {}, []
        raws = []
        while self.i < len(self.t):
            tok = self.peek()
            if tok is None:
                break
            if tok.kind == "punct" and tok.text == "}":
                self.next()
                break
            if tok.kind == "punct" and tok.text == ",":
                self.next()
                continue
            # `key = value`
            if tok.kind in ("name", "string") :
                save = self.i
                k = self.next()
                nxt = self.peek()
                if nxt and nxt.kind == "punct" and nxt.text == "=":
                    self.next()
                    raw, val = self.value()
                    key = k.text if k.kind == "name" else unquote(k.text)
                    items[key] = (raw, val)
                    raws.append("%s = %s" % (key, raw))
                    continue
                self.i = save
            if tok.kind == "punct" and tok.text == "[":
                self.next()
                kraw, _kv = self.value()
                nxt = self.peek()
                if nxt and nxt.kind == "punct" and nxt.text == "]":
                    self.next()
                nxt = self.peek()
                if nxt and nxt.kind == "punct" and nxt.text == "=":
                    self.next()
                    raw, val = self.value()
                    items["[%s]" % kraw] = (raw, val)
                    raws.append("[%s] = %s" % (kraw, raw))
                    continue
            raw, val = self.value()
            arr.append((raw, val))
            raws.append(raw)
        return "{" + ", ".join(raws) + "}", ("t", items, tuple(arr))


def unquote(s):
    if s.startswith("[") :
        return re.sub(r"^\[=*\[|\]=*\]$", "", s)
    return s[1:-1]


def num(s):
    try:
        return int(s, 0) if not any(c in s for c in ".eE") or s.lower().startswith("0x") \
            else float(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


# --------------------------------------------------------------------------- #
# flattening a parsed PlaceObj table into `key.sub[3].leaf -> (raw, value)`
# --------------------------------------------------------------------------- #
def as_pairs(items, arr):
    """⭐ THE `PlaceObj` SUB-ITEM PROPERTY FORM, which is NOT `key = value`.

    A top-level preset writes `{ id = "x", count = 3 }`. A NESTED one writes a
    flat array of alternating name/value pairs instead:

        PlaceObj('XDefWindowRoot', {'__class', "Infopanel", 'Description', T(…)}, {…})

    Read positionally, `'__class'` is element [1] and `"Infopanel"` is element
    [2] -- so every property NAME is reported as a value, and inserting one
    property shifts every element after it. MEASURED: that is what made
    `XDef:PoliticsDlg` alone produce 5,307 rows keyed `[1][2][7][2][2]…`.
    Recognised as pairs, the same data keys as `.Description` and survives an
    insertion untouched.

    ⛔ Applied ONLY to a `PlaceObj` property table (`pairs_ok`), never to an
    arbitrary array -- `{"a", "b"}` is a two-element list, not `a = "b"`.
    """
    if items or not arr or len(arr) % 2:
        return None
    names = []
    for i in range(0, len(arr), 2):
        raw, v = arr[i]
        if v is None or v[0] != "s":
            return None
        names.append(unquote(raw))
    if len(set(names)) != len(names):
        return None
    return [(names[i // 2], arr[i + 1]) for i in range(0, len(arr), 2)]


def flatten(val, prefix, out, raw="", pairs_ok=False):
    """`key.sub[3].leaf -> raw value text`.

    ⭐ A NESTED `PlaceObj` IS DESCENDED INTO, not stringified. Sub-item presets
    (a law's `Effects[1]`, a storybit's replies, a scenario step) are the
    interesting half of this data, and the first version compared each one as a
    single 500-character blob -- technically a diff, useless as a row. Their
    tables flatten to `Effects[1].Amount`, which is a row a reader can act on.
    Every OTHER call (`T(…)`, `point(…)`, `set(…)`) stays a leaf: it is a
    value, not a structure.
    """
    if val is None:
        out[prefix] = raw
        return
    tag = val[0]
    if tag == "t":
        _t, items, arr = val
        pairs = as_pairs(items, arr) if pairs_ok else None
        if pairs is not None:
            for name, (r, v) in pairs:
                flatten(v, ("%s.%s" % (prefix, name)) if prefix else name, out, r)
            return
        for k in sorted(items):
            r, v = items[k]
            flatten(v, ("%s.%s" % (prefix, k)) if prefix else k, out, r)
        for n, (r, v) in enumerate(arr, 1):
            flatten(v, "%s[%d]" % (prefix, n), out, r)
    elif tag == "c" and val[1] == "PlaceObj":
        # PlaceObj('Class', <properties>[, <children>]) — the FIRST table is the
        # property table (pair form); any later table is a children array and
        # stays positional, because a child list's order is real structure.
        out[prefix + ".__class"] = val[2][0] if val[2] else ""
        tables = [s for s in val[3] if s is not None and s[0] == "t"]
        for n, sub in enumerate(tables):
            flatten(sub, prefix if n == 0 else "%s.children" % prefix, out,
                    pairs_ok=(n == 0))
    else:
        out[prefix] = raw or (val[1] if tag == "i" else str(val))


def parse_file(path):
    """-> list of (class, ordered-key-list, {flat_key: raw_text}, id, group)

    ⚠️ The file is lexed ONCE and the token stream walked; the first version
    re-lexed a 400 KB window per `PlaceObj`, which on `Data/StoryBit`'s 514
    files is quadratic in the file size for no gain.

    ⛔ TOP-LEVEL PlaceObj ONLY. A `PlaceObj` NESTED inside another preset's
    table (sub-items: effects, conditions, scenario steps) is parsed as part of
    its PARENT's value and reached by key path (`Effects[2].Amount`), which is
    what makes it diffable at all -- a nested sub-item has no id of its own to
    key on.
    """
    toks = lex("\n".join(read_lines(path)))
    out, i, n = [], 0, len(toks)
    while i < n:
        t = toks[i]
        if t.kind == "name" and t.text == "PlaceObj" \
                and i + 4 < n and toks[i + 1].text == "(" \
                and toks[i + 2].kind == "string" and toks[i + 3].text == "," \
                and toks[i + 4].text == "{":
            cls = unquote(toks[i + 2].text)
            p = Parser(toks)
            p.i = i + 5                          # just past the '{'
            _raw, val = p.table()
            i = p.i
            if val is None or val[0] != "t":
                continue
            flat = {}
            flatten(val, "", flat)
            items = val[1]
            pid = items.get("id", ("", None))[0]
            grp = items.get("group", ("", None))[0]
            out.append((cls, list(items.keys()), flat,
                        unquote(pid) if pid[:1] in "\"'" else pid,
                        unquote(grp) if grp[:1] in "\"'" else grp))
            continue
        i += 1
    return out


def scan_tree(root):
    """-> {identity: (file, flat, keyorder)}, plus collision + file counts

    ⚠️ IDENTITY, AND THE FALLBACK THAT MATTERS. A preset with an `id` is keyed
    `(class, id, group)` so it survives its file being renamed. **Many presets
    have no id at all** -- `SA_Exec`, `SA_Block`, `MapSettings_*`, most scenario
    steps -- and the first version gave each of those a unique synthetic key,
    which made all 5,743 of them report as `added-preset` on one side and
    `removed-preset` on the other. Nothing had been added. An id-less preset is
    therefore keyed `(class, file, ordinal-within-file)`, which matches across
    the trees whenever its file did not move; when the file DID move it is
    honestly unmatchable, and that is counted rather than reported as an add.
    """
    presets, collisions, per_dir = {}, 0, collections.Counter()
    files = tree_files(root)
    for rel in sorted(files):
        if rel.startswith("DLC/") or not rel.endswith(".lua"):
            continue
        if not rel.startswith(GENERATED):
            continue
        per_dir[rel.split("/")[0] if not rel.startswith("Lua/")
                else "/".join(rel.split("/")[:2])] += 1
        nth = collections.Counter()
        for cls, order, flat, pid, grp in parse_file(files[rel]):
            if pid:
                key = (cls, pid, grp or "")
                if key in presets:
                    collisions += 1
                    key = (cls, pid, "%s~%d" % (grp or "", collisions))
            else:
                nth[cls] += 1
                key = (cls, "%s#%d" % (rel, nth[cls]), "<no-id>")
            presets[key] = (rel, flat, order)
    return presets, collisions, per_dir


# --------------------------------------------------------------------------- #
# the churn rules. ⛔ Each is a CLAIM that a row is uninteresting; `--sample`
# exists so a human can falsify one.
# --------------------------------------------------------------------------- #
T_CALL = re.compile(r"^T\(\s*(-?\d+)\s*,\s*(.*)\)$", re.DOTALL)
COMMENT_RX = re.compile(r"--\[(=*)\[.*?\]\1\]|--[^\n]*", re.DOTALL)


def strip_comments(s):
    return re.sub(r"\s+", " ", COMMENT_RX.sub("", s)).strip()


def norm_value(s):
    """Format-insensitive form: comments out, whitespace collapsed, quotes and
    number spelling canonicalised."""
    s = strip_comments(s)
    def _num(m):
        v = num(m.group(0))
        return repr(float(v)) if isinstance(v, (int, float)) else m.group(0)
    s = re.sub(r"'((?:\\.|[^'\\])*)'", lambda m: '"%s"' % m.group(1), s)
    s = re.sub(r"(?<![\w.])-?(?:\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+)(?![\w.])", _num, s)
    return s.rstrip(",").strip()


INDEX_RX = re.compile(r"\[\d+\]")


def index_free(key):
    return INDEX_RX.sub("[]", key)


def reindex_sets(aflat, zflat):
    """⭐ THE RE-INDEX RULE, and why it had to exist.

    The deeply nested `XDef` UI trees are arrays of arrays: `PoliticsDlg` is
    seven to fifteen levels of `[N][N][N]…`. Insert ONE child near the top and
    every descendant below it shifts index, so a purely positional edit reports
    as thousands of `<absent>` rows. Measured before this rule existed:
    **75,896 `none` rows, 60,186 of them `<absent>` on one side, and one preset
    (`XDef:PoliticsDlg`) contributing 5,307 of them.** That is not a readable
    pile; it is an instrument drowning its own signal.

    So: strip every `[digits]` from the key and compare the resulting
    multisets of `(index-free key, value)`. If they are EQUAL, the preset's
    CONTENT is identical and only positions moved -- every row in it is
    `REINDEX`. If they are not, a row is still `REINDEX` when its own value is
    accounted for elsewhere in the other side under the same index-free key.

    ⛔ WHAT THIS RULE CAN HIDE, stated because a churn class is a claim: a
    genuine REORDERING of a list whose ORDER IS SEMANTIC (a priority list, a
    sequence of scenario steps) is content-identical and will be classed
    `REINDEX`. If order matters for a registry, that registry's rows must be
    read with `--sample REINDEX`, not trusted.
    """
    a_ms = collections.Counter((index_free(k), v) for k, v in aflat.items())
    z_ms = collections.Counter((index_free(k), v) for k, v in zflat.items())
    return a_ms, z_ms, a_ms == z_ms


def churn_class(key, a, z):
    """The RULES, applied in this order. The order is part of the rule."""
    leaf = key.rsplit(".", 1)[-1].split("[")[0]
    if leaf in SAVE_ID_KEYS:
        return "SAVE-ID"
    ma, mz = T_CALL.match(a.strip()), T_CALL.match(z.strip())
    if ma and mz:
        ta, tz = strip_comments(ma.group(2)), strip_comments(mz.group(2))
        if ta == tz and ma.group(1) != mz.group(1):
            return "T-ID"
        # ⚠️ the text moved too -- that is player-visible, and NOT churn
        return "none"
    if strip_comments(a) == strip_comments(z):
        return "COMMENT"
    if norm_value(a) == norm_value(z):
        return "FORMAT"
    return "none"


def annotate_class_renames(rows, old, new):
    """⭐ `CLASS-RENAMED?<old>-><new>` — class (d) at the PRESET-CLASS level.

    FOUND BY THIS TOOL'S OWN SAMPLING, and it would otherwise have been the
    single largest lie in `PRESETS.tsv`: the tech registry's preset class was
    renamed `TechPreset` -> `Tech` (`Data/TechPreset.lua` -> `Data/Tech.lua`,
    441 `Tech` blocks in 1.1.0 where 1.0.7 had 264 `TechPreset`), and a
    `class::id` identity tears every migrated preset into one `removed-preset`
    and one `added-preset`. Neither is true; the preset MOVED CLASS.

    So: a removed preset and an added preset that share an `id` are flagged as
    each other's class-rename candidates. ⛔ A HINT, not a verdict — two
    registries can legitimately use the same id for different things, and the
    method rule still stands: the presence side is what this enumerates, and a
    reader confirms it.
    """
    rm = collections.defaultdict(list)
    for r in rows:
        if r[6] == "removed-preset":
            rm[r[2]].append(r)
    for r in rows:
        if r[6] != "added-preset":
            continue
        for p in rm.get(r[2], []):
            if p[1] == r[1]:
                continue
            r[7] = (r[7] + "," if r[7] else "") + "CLASS-RENAMED?%s->%s" % (p[1], r[1])
            p[7] = (p[7] + "," if p[7] else "") + "CLASS-RENAMED?%s->%s" % (p[1], r[1])


def diff(old_root, new_root):
    old, ocoll, odirs = scan_tree(old_root)
    new, ncoll, ndirs = scan_tree(new_root)
    rows = []
    reorder_only = 0
    reindex_only = 0
    file_moved = 0
    for key in sorted(set(old) | set(new)):
        a, z = old.get(key), new.get(key)
        cls, pid, grp = key
        if a and z:
            afile, aflat, aorder = a
            zfile, zflat, zorder = z
            moved = afile != zfile
            if moved:
                file_moved += 1
            a_ms, z_ms, content_same = reindex_sets(aflat, zflat)
            if content_same and aflat != zflat:
                reindex_only += 1
            changed = False
            for k in sorted(set(aflat) | set(zflat)):
                av, zv = aflat.get(k, "<absent>"), zflat.get(k, "<absent>")
                if av == zv:
                    continue
                changed = True
                ik = index_free(k)
                if content_same:
                    cc = "REINDEX"
                elif "<absent>" in (av, zv):
                    # the value is not gone if it is still in the other side
                    # under the same index-free key -- it moved position
                    other = zv if av == "<absent>" else av
                    src = a_ms if av == "<absent>" else z_ms
                    cc = "REINDEX" if src.get((ik, other), 0) else "none"
                elif z_ms.get((ik, av), 0) and a_ms.get((ik, zv), 0):
                    # ⚠️ THE WEAK HALF, SEPARATED AFTER READING 20 ROWS OF IT.
                    # Both sides hold a real value and each is accounted for
                    # elsewhere, so this is CONSISTENT with a list reordering --
                    # but it is equally consistent with a genuine swap at this
                    # position, and the tool cannot tell. Where list order is
                    # semantic (`Parameters`, `likes`, `Effects`) that
                    # difference matters. ⛔ NOT safe to skip: its own class.
                    cc = "REINDEX-SWAP"
                else:
                    cc = churn_class(k, av, zv)
                rows.append([zfile or afile, cls, pid, k, av, zv, cc,
                             "FILE-MOVED" if moved else ""])
            if not changed and aorder != zorder:
                reorder_only += 1
        elif z:
            rows.append([z[0], cls, pid, "<preset>", "", "<added>",
                         "added-preset", ""])
        else:
            rows.append([a[0], cls, pid, "<preset>", "<removed>", "",
                         "removed-preset", ""])
    annotate_class_renames(rows, old, new)
    return rows, dict(old=len(old), new=len(new), ocoll=ocoll, ncoll=ncoll,
                      odirs=odirs, ndirs=ndirs, reorder_only=reorder_only,
                      reindex_only=reindex_only, file_moved=file_moved)


# --------------------------------------------------------------------------- #
# --selftest
# --------------------------------------------------------------------------- #
OLD_FIX = """
PlaceObj('Widget', {
\tid = "alpha",
\tgroup = "G",
\tcount = 10,
\tlabel = T(111, --[[Widget alpha label]] "Hello"),
\tmoved_text = T(333, --[[old ctx]] "Before"),
\tdropme = "gone",
\tstyle = 'single',
\tsave_in = "base",
\tnested = { a = 1, b = { deep = "x" } },
\tlist = { "one", "two" },
\thandler = function(self) local x = 1 if x then print("old") end end,
\tstable_handler = function(self) return 7 end,
\tkids = {
\t\tPlaceObj('Sub', {'Name', "first", 'Colour', "red"}),
\t\tPlaceObj('Sub', {'Name', "second", 'Colour', "blue"}),
\t},
})

PlaceObj('Widget', {
\tid = "reorder_me",
\tgroup = "G",
\tfirst = 1,
\tsecond = 2,
})

PlaceObj('Widget', {
\tid = "goodbye",
\tgroup = "G",
\tv = 1,
})
"""
NEW_FIX = """
PlaceObj('Widget', {
\tid = "alpha",
\tgroup = "G",
\tcount = 12,
\tlabel = T(222, --[[Widget alpha label]] "Hello"),
\tmoved_text = T(444, --[[new ctx]] "After"),
\taddme = "fresh",
\tstyle = "single",
\tsave_in = "dlc",
\tnested = { a = 1, b = { deep = "y" } },
\tlist = { "one", "two" },
\thandler = function(self) local x = 1 if x then print("NEW") end end,
\tstable_handler = function(self) return 7 end,
\tkids = {
\t\tPlaceObj('Sub', {'Name', "inserted", 'Colour', "green"}),
\t\tPlaceObj('Sub', {'Name', "first", 'Colour', "red"}),
\t\tPlaceObj('Sub', {'Name', "second", 'Colour', "blue"}),
\t},
})

PlaceObj('Widget', {
\tid = "reorder_me",
\tgroup = "G",
\tsecond = 2,
\tfirst = 1,
})

PlaceObj('Widget', {
\tid = "hello_new",
\tgroup = "G",
\tv = 1,
})
"""


def selftest(old_root, new_root, sample_n=20, seed=5):
    ok = True

    def check(label, cond, detail=""):
        nonlocal ok
        ok = ok and cond
        print("  %-6s %s%s" % ("PASS" if cond else "FAIL", label,
                               ("   -> " + detail) if detail and not cond else ""))

    print("=" * 78)
    print("PART 1 — planted fixtures")
    tmp = tempfile.mkdtemp(prefix="presetdiff_selftest_")
    for side, body in (("old", OLD_FIX), ("new", NEW_FIX)):
        d = os.path.join(tmp, side, "Data")
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "Widget.lua"), "w", encoding="utf-8",
                newline="\n").write(body)
    rows, st = diff(os.path.join(tmp, "old"), os.path.join(tmp, "new"))
    got = {(r[2], r[3]): r for r in rows}

    def cc(pid, key):
        r = got.get((pid, key))
        return r[6] if r else None

    check("changed NUMERIC value -> a row, churn `none`",
          cc("alpha", "count") == "none", repr(got.get(("alpha", "count"))))
    check("changed STRING deep in a nested table -> a row at `nested.b.deep`",
          cc("alpha", "nested.b.deep") == "none",
          repr(got.get(("alpha", "nested.b.deep"))))
    check("a key ADDED -> a row (old side `<absent>`)",
          cc("alpha", "addme") == "none"
          and got[("alpha", "addme")][4] == "<absent>",
          repr(got.get(("alpha", "addme"))))
    check("a key REMOVED -> a row (new side `<absent>`)",
          cc("alpha", "dropme") == "none"
          and got[("alpha", "dropme")][5] == "<absent>",
          repr(got.get(("alpha", "dropme"))))
    check("a preset ADDED -> `added-preset`",
          cc("hello_new", "<preset>") == "added-preset",
          repr(got.get(("hello_new", "<preset>"))))
    check("a preset REMOVED -> `removed-preset`",
          cc("goodbye", "<preset>") == "removed-preset",
          repr(got.get(("goodbye", "<preset>"))))
    check("⛔ a REORDER-ONLY preset produces NO ROW AT ALL",
          not any(r[2] == "reorder_me" for r in rows) and st["reorder_only"] == 1,
          "rows=%r reorder_only=%d"
          % ([r for r in rows if r[2] == "reorder_me"], st["reorder_only"]))
    check("⭐ T() id changed, TEXT IDENTICAL -> `T-ID`",
          cc("alpha", "label") == "T-ID", repr(got.get(("alpha", "label"))))
    check("⭐ T() id changed AND TEXT CHANGED -> `none`, never T-ID "
          "(a player can see this one)",
          cc("alpha", "moved_text") == "none",
          repr(got.get(("alpha", "moved_text"))))
    check("quote style only ('single' -> \"single\") -> `FORMAT`",
          cc("alpha", "style") == "FORMAT", repr(got.get(("alpha", "style"))))
    check("`save_in` -> `SAVE-ID`",
          cc("alpha", "save_in") == "SAVE-ID", repr(got.get(("alpha", "save_in"))))
    check("an UNCHANGED key produces no row",
          ("alpha", "nested.a") not in got and ("alpha", "list[1]") not in got,
          repr([k for k in got if k[0] == "alpha"]))
    # ---- the three parser defects the real trees found, pinned so a future
    #      change to this file cannot silently reintroduce them ----
    print("  ---- parser defects found on the real trees, now pinned ----")
    check("⛔ an embedded `function … end` is ONE value, not a shred of tokens: "
          "a changed handler is exactly ONE row carrying its source",
          cc("alpha", "handler") == "none"
          and "print" in got[("alpha", "handler")][4]
          and not any(k[1].startswith("handler[") for k in got),
          repr(got.get(("alpha", "handler"))))
    check("...and an UNCHANGED handler is no row at all",
          ("alpha", "stable_handler") not in got,
          repr(got.get(("alpha", "stable_handler"))))
    check("⭐ `PlaceObj` sub-item PAIR form keys by NAME (`kids[1].Colour`), "
          "not by position",
          any(k[1].endswith(".Colour") or k[1].endswith(".Name") for k in got),
          repr(sorted(k[1] for k in got if k[0] == "alpha")))
    check("⭐ inserting a child at the FRONT of a list re-indexes it, and the "
          "shifted rows are classed REINDEX, not `none`",
          any(k[0] == "alpha" and ".Name" in k[1] and got[k][6] == "REINDEX"
              for k in got),
          repr([(k[1], got[k][6]) for k in got if k[0] == "alpha" and "kids" in k[1]]))

    print()
    print("PART 2 — the REAL trees: falsify each churn RULE on its own rows.")
    print("         ⭐ %d random rows per class, printed for a human to read"
          % sample_n)
    if not (os.path.isdir(old_root) and os.path.isdir(new_root)):
        print("  SKIP   archives not on disk")
        print("=" * 78)
        print("SELFTEST: %s" % ("PASS" if ok else "*** FAIL ***"))
        return 0 if ok else 1
    rows, st = diff(old_root, new_root)
    by = collections.defaultdict(list)
    for r in rows:
        by[r[6]].append(r)
    random.seed(seed)
    for c in sorted(by):
        print("  ---- %s: %d rows ----" % (c, len(by[c])))
        for r in random.sample(by[c], min(sample_n, len(by[c])))[:5]:
            print("     %s | %s:%s | %s" % (r[0], r[1], r[2], r[3]))
            print("        107: %s" % r[4][:150])
            print("        110: %s" % r[5][:150])
    print("=" * 78)
    print("SELFTEST: %s" % ("PASS — every verdict fired on a known case"
                            if ok else "*** FAIL ***"))
    return 0 if ok else 1


def banner(old_root, new_root, st, rows, extra=()):
    cmd = "python " + " ".join([os.path.basename(sys.argv[0])] + sys.argv[1:])
    by = collections.Counter(r[6] for r in rows)
    out = ["# %s | old=%s digest=%s | new=%s digest=%s | %s | %s"
           % (VERSION, old_root, tree_digest(old_root), new_root,
              tree_digest(new_root), cmd, datetime.date.today().isoformat())]
    out.append("# SCOPE: the `generated` bucket only — %s. DLC/ excluded."
               % ", ".join(GENERATED))
    out.append("# PRESETS: 1.0.7=%d  1.1.0=%d. Identity is `class::id::group` "
               "(how the GAME names a preset), with id-less presets keyed "
               "`class::file#ordinal`. Matched presets whose FILE moved: %d. "
               "Ambiguous ids needing a disambiguator: 1.0.7=%d 1.1.0=%d."
               % (st["old"], st["new"], st["file_moved"], st["ocoll"], st["ncoll"]))
    out.append("# ⭐ ROUTED TO 02, NOT READ HERE: the tech registry exists TWICE "
               "in 1.1.0 — 264 `TechPreset` in 1.0.7 became 274 `TechPreset` "
               "PLUS 441 `Tech`, and 258 of the 1.0.7 ids appear under both "
               "classes in the new tree. Mechanical count only; what it means "
               "is a reader's question.")
    out.append("# ⛔ REORDER IS NOT A ROW, BY CONSTRUCTION: rows are keyed by key "
               "PATH, so re-emitting a preset's keys in another order with equal "
               "values yields nothing. %d presets are in exactly that state — "
               "COUNTED here so that `no rows` and `never looked` do not look "
               "alike." % st["reorder_only"])
    out.append("# ROWS BY CHURN CLASS: " +
               "  ".join("%s=%d" % kv for kv in sorted(by.items())) +
               "   ⭐ `none` is the READABLE PILE — the rows 04's registry "
               "agents actually read.")
    out.append("# ⭐ THE GENERATED-LUA TWINS, so 04 can confirm they carry nothing "
               "extra: 1.1.0 files parsed per registry — " +
               ", ".join("%s=%d" % kv for kv in sorted(st["ndirs"].items())) +
               " | 1.0.7 — " +
               ", ".join("%s=%d" % kv for kv in sorted(st["odirs"].items())))
    out.append("# ⚠️ CHURN CLASSES ARE CLAIMS. Each is a rule asserting a row is "
               "uninteresting; `python tools/presetdiff.py --sample <class>` "
               "prints rows so one can be falsified. A single row where a rule "
               "hid a real value change VOIDS that class.")
    for e in extra:
        out.append("# " + e)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--old", default=DEFAULT_OLD)
    ap.add_argument("--new", default=DEFAULT_NEW)
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sample", help="print random rows of one churn class")
    ap.add_argument("-n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=5)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.old, a.new, a.n, a.seed)
    rows, st = diff(a.old, a.new)
    if a.sample:
        pool = [r for r in rows if r[6] == a.sample]
        random.seed(a.seed)
        print("%s: %d rows; %d sampled" % (a.sample, len(pool),
                                           min(a.n, len(pool))))
        for r in random.sample(pool, min(a.n, len(pool))):
            print("\n%s | %s:%s | key=%s" % (r[0], r[1], r[2], r[3]))
            print("   107: %s" % r[4][:300])
            print("   110: %s" % r[5][:300])
        return 0
    print("preset rows: %d" % len(rows))
    for k, v in sorted(collections.Counter(r[6] for r in rows).items()):
        print("  %-16s %d" % (k, v))
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        write_tsv(os.path.join(a.out, "PRESETS.tsv"),
                  banner(a.old, a.new, st, rows),
                  ["file", "class", "id", "key", "value107", "value110",
                   "churn-class", "flags"], rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
