#!/usr/bin/env python3
"""Is the shipped code each module patches still the code it was pinned to?

Written 2026-09-08 (hotfix2 link 01, report PACK_1_1_0_REVERIFICATION §4 item 2)
for the bucket that had never been used. The 1.1.0 re-verification found 35
modules to retire, and **32 of them were modules whose defect the developers had
fixed themselves while our self-check passed anyway**. Every instrument the
project owned was blind to it: `Require` sees EXISTENCE, `sigcheck.py` sees
ARITY, a name sweep sees NAMES. A function that still exists, still takes the
same arguments, and no longer has the bug is invisible to all three -- and our
correction then lands on top of vanilla's, which is how F-1 stopped every Saint
in the game from blessing anyone.

⛔ THE GAP THIS TOOL EXISTS TO CLOSE, stated as the two questions nobody could
ask cheaply:
    1. is the body we pinned still the body that ships?      (class b)
    2. is the defective expression we correct still shipped?  (class d)

    python tools/bodycheck.py                  # check the pack against the live source
    python tools/bodycheck.py --src <path>     # point at another ModTools/Src
    python tools/bodycheck.py --code <path>    # check another Code/ tree (fixtures)
    python tools/bodycheck.py --all            # also print OK rows
    python tools/bodycheck.py --module NAME    # one module
    python tools/bodycheck.py --pin <file> <selector>   # emit a ready SRC: line
    python tools/bodycheck.py --selftest       # the falsifier -- run it before trusting a GREEN

WHAT IT REPORTS
  BODY-CHANGED   the SRC: hash no longer matches the shipped body (class b:
                 F114, F116, F-6, F-7, F-9 -- every one invisible until a human
                 read the body)
  DEFECT-GONE    the DEFECT: expression no longer appears in scope (class d:
                 "vanilla fixed it", 32 modules in the 1.1.0 audit)
  TARGET-ABSENT  the selector resolves to nothing -- the function is gone
                 (class e; `Require` also covers this one, at runtime)
  TARGET-MULTI   the selector resolves to several declarations: the pin is
                 ambiguous and therefore not a pin
  MALFORMED      a manifest line that does not parse. Worse than no manifest,
                 because it looks like coverage
  NO-MANIFEST    the module declares neither line. A COUNT, not a failure,
                 until the whole pack is stamped
  NO-DEFECT      a SRC: with no DEFECT: -- the body is pinned but the module
                 cannot state what it corrects. A count, and the named
                 exception list (FIX_POLICY §2b)
  SRC-NONE       `-- SRC: none <reason>` -- deliberately unhashable (a data
                 patch, an additive handler). A count
  OK             hash matches and every defect expression is still shipped

THE MANIFEST GRAMMAR (FIX_POLICY §2b holds the authoring rule; this is the
machine half). Both lines are ordinary Lua comments and live in the module's
header block:

    -- SRC: <path> <selector> sha256=<64 hex>
    -- SRC: none <free-text reason>
    -- DEFECT: <python regex>
    -- DEFECT@<path>: <python regex>

  <path>      slash-separated, relative to ModTools/Src. `\\` is accepted and
              normalised, because every existing header writes it that way.
  <selector>  no spaces. One of
                Class:Method / Class.Method   the separator is a hint, not a
                                              constraint -- both forms of
                                              declaration are matched, as is
                                              `Class.Method = function(`
                Name                          a global or `local function`
                L<first>-<last>               a literal 1-based line span, for
                                              data tables and generated files
                                              with no function to name
  <regex>     Python `re`, searched with re.search over the SCOPE below. One
              line only (it lives in a Lua comment): a multi-line expression
              uses `\\n` or `[\\s\\S]`. Shipped Lua indents with TABS -- write
              `\\s+` between tokens, never a literal space.
  scope       `-- DEFECT:` searches the body of the SRC: line ABOVE it, which
              is what makes DEFECT-GONE precise rather than a tree grep that
              could match anywhere. `-- DEFECT@<path>:` searches that whole
              file, and is the DataPatch form: a data patch has no function to
              hash, so it declares `SRC: none` and points its DEFECT at the
              shipped data expression (e.g. `modify_trait\\s*=\\s*"Religious"`
              in Data/TraitPreset.lua).
  repetition  a module may carry several SRC: lines; each DEFECT: binds to the
              nearest SRC: above it.

HOW A BODY IS DELIMITED, AND WHAT IS HASHED. The delimiter is
`luafn.py:find_bodies` -- imported, never re-implemented, so what this hashes is
exactly what `python tools/luafn.py <file> <fn>` prints. From the declaration
line to the first bare `end` at the same indentation. Before hashing, line
endings are normalised to \\n and TRAILING whitespace is stripped from each
line (the shipped tree is CRLF and 51 lines of Train.lua alone carry trailing
spaces; a whitespace-only diff is not a body change). Leading indentation is
kept -- it is structure. Comments are kept -- a changed comment in a shipped
body is a signal, not noise. sha256 of the utf-8 of that.

⚠️ WHAT IT CANNOT DECIDE, AND MUST NOT BE READ AS DECIDING. A GREEN here is not
a clearance. It sees classes (b), (d) and (e). It does NOT see class (c) --
semantics moving under a wrapper while the body it wraps is untouched (F111,
F112, F-1, F-2, F-3, F-5) -- and nothing this project owns sees that. It cannot
see a defect whose expression the module never stated: a NO-DEFECT module is
unwatched, which is the whole point of counting them. And a DEFECT-GONE is a
REMOVE *candidate*, never a verdict -- read the replacement before retiring
anything (a rename reads as "gone" and nearly retired a live fix, R-15).
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luafn import find_bodies, read_lines          # THE delimiter -- see above

DEFAULT_SRC = r"A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(HERE, "Code")

RE_SRC = re.compile(r"^\s*--\s*SRC:\s*(.+?)\s*$")
RE_DEFECT = re.compile(r"^\s*--\s*DEFECT(?:@(\S+?))?:\s*(.+?)\s*$")
RE_SHA = re.compile(r"^sha256=([0-9a-f]{64})$")
RE_SPAN = re.compile(r"^L(\d+)-(\d+)$")

FAIL_KINDS = ("BODY-CHANGED", "DEFECT-GONE", "TARGET-ABSENT", "TARGET-MULTI", "MALFORMED")
COUNT_KINDS = ("NO-MANIFEST", "NO-DEFECT", "SRC-NONE", "OK")
ORDER = {k: i for i, k in enumerate(FAIL_KINDS + COUNT_KINDS)}


# --------------------------------------------------------------------------- #
# resolving a selector to a body
# --------------------------------------------------------------------------- #

def selector_pattern(selector):
    """-> a regex for find_bodies, or None if the selector is a line span."""
    if RE_SPAN.match(selector):
        return None
    if ":" in selector or "." in selector:
        cls, meth = re.split(r"[:.]", selector, maxsplit=1)
        c, m = re.escape(cls), re.escape(meth)
        # `function C:M(` / `function C.M(` / `C.M = function(` / `C:M = function(`
        return r"^\s*function\s+%s\s*[:.]\s*%s\s*\(|^\s*%s\s*[:.]\s*%s\s*=\s*function\s*\(" % (c, m, c, m)
    n = re.escape(selector)
    return r"^\s*(?:local\s+)?function\s+%s\s*\(|^\s*%s\s*=\s*function\s*\(" % (n, n)


def resolve(src, path, selector):
    """-> (body_text, "file:first-last", None) or (None, None, why_not)."""
    full = os.path.join(src, path.replace("\\", os.sep).replace("/", os.sep))
    if not os.path.isfile(full):
        return None, None, "no such file in the source tree: %s" % path
    lines = read_lines(full)
    span = RE_SPAN.match(selector)
    if span:
        a, b = int(span.group(1)), int(span.group(2))
        if a < 1 or b > len(lines) or a > b:
            return None, None, "line span %s is outside %s (%d lines)" % (selector, path, len(lines))
        spans = [(a - 1, b - 1)]
    else:
        spans = find_bodies(lines, selector_pattern(selector))
    if not spans:
        return None, None, "no declaration of %s in %s" % (selector, path)
    if len(spans) > 1:
        where = ", ".join("%s:%d" % (path, i + 1) for i, _ in spans)
        return None, None, "%d declarations of %s (%s) -- the pin is ambiguous" % (
            len(spans), selector, where)
    i, j = spans[0]
    text = "\n".join(l.rstrip() for l in lines[i:j + 1])
    return text, "%s:%d-%d" % (path, i + 1, j + 1), None


def body_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_text(src, path):
    full = os.path.join(src, path.replace("\\", os.sep).replace("/", os.sep))
    if not os.path.isfile(full):
        return None
    return "\n".join(l.rstrip() for l in read_lines(full))


# --------------------------------------------------------------------------- #
# reading the manifest out of a module
# --------------------------------------------------------------------------- #

def parse_module(path):
    """-> list of manifest items, in file order.

    An item is a dict: kind 'src' {path, selector, sha, line} | 'src-none'
    {reason, line} | 'defect' {scope_path or None, regex, line}.
    A 'bad' item carries {why, line} for a line that does not parse.
    """
    items = []
    for n, line in enumerate(read_lines(path), 1):
        m = RE_SRC.match(line)
        if m:
            payload = m.group(1)
            head = payload.split(None, 1)
            if head and head[0].lower() == "none":
                items.append({"kind": "src-none", "line": n,
                              "reason": (head[1] if len(head) > 1 else "").strip(" -\u2014")})
                continue
            parts = payload.split()
            if len(parts) != 3:
                items.append({"kind": "bad", "line": n,
                              "why": "SRC: wants exactly `<path> <selector> sha256=<64 hex>`, got %d token(s)"
                                     % len(parts)})
                continue
            sha = RE_SHA.match(parts[2])
            if not sha:
                items.append({"kind": "bad", "line": n,
                              "why": "SRC: third token is not sha256=<64 lowercase hex>: %r" % parts[2]})
                continue
            items.append({"kind": "src", "line": n, "path": parts[0].replace("\\", "/"),
                          "selector": parts[1], "sha": sha.group(1)})
            continue
        m = RE_DEFECT.match(line)
        if m:
            scope, rx = m.group(1), m.group(2)
            try:
                re.compile(rx)
            except re.error as e:
                items.append({"kind": "bad", "line": n,
                              "why": "DEFECT: is not a valid Python regex (%s)" % e})
                continue
            items.append({"kind": "defect", "line": n,
                          "scope_path": scope.replace("\\", "/") if scope else None, "regex": rx})
    return items


def check_module(src, fname, path):
    """-> list of rows (kind, module, line, target, detail)."""
    items = parse_module(path)
    mod = fname[:-4] if fname.endswith(".lua") else fname
    if not items:
        return [("NO-MANIFEST", mod, 0, "", "declares neither SRC: nor DEFECT:")]

    rows = []
    # cache per SRC item: (target_label, body_text or None)
    current = None          # the SRC item each following DEFECT binds to
    for it in items:
        if it["kind"] == "bad":
            rows.append(("MALFORMED", mod, it["line"], "", it["why"]))
            current = None
            continue
        if it["kind"] == "src-none":
            current = it
            rows.append(("SRC-NONE", mod, it["line"], "none",
                         it["reason"] or "no reason given (the grammar wants one)"))
            continue
        if it["kind"] == "src":
            current = it
            text, where, why = resolve(src, it["path"], it["selector"])
            it["_body"] = text
            if text is None:
                rows.append(("TARGET-MULTI" if "ambiguous" in why else "TARGET-ABSENT",
                             mod, it["line"], "%s %s" % (it["path"], it["selector"]), why))
                continue
            got = body_hash(text)
            if got != it["sha"]:
                rows.append(("BODY-CHANGED", mod, it["line"],
                             "%s %s" % (it["path"], it["selector"]),
                             "pinned %s..., shipped %s... (%s) -- read the body before trusting this module"
                             % (it["sha"][:12], got[:12], where)))
            else:
                rows.append(("OK", mod, it["line"], "%s %s" % (it["path"], it["selector"]),
                             "body matches the pin (%s)" % where))
            continue
        # a defect line
        if current is None:
            rows.append(("MALFORMED", mod, it["line"], "",
                         "DEFECT: with no SRC: above it and no @<path> scope"))
            continue
        if it["scope_path"]:
            hay = file_text(src, it["scope_path"])
            scope = it["scope_path"]
            if hay is None:
                rows.append(("TARGET-ABSENT", mod, it["line"], scope,
                             "DEFECT@ names a file that is not in the source tree"))
                continue
        elif current["kind"] == "src-none":
            rows.append(("MALFORMED", mod, it["line"], "",
                         "a body-scoped DEFECT: under `SRC: none` has nothing to search -- "
                         "use DEFECT@<path>:"))
            continue
        else:
            hay = current.get("_body")
            scope = "%s %s" % (current["path"], current["selector"])
            if hay is None:
                continue        # the SRC row already reported ABSENT/MULTI
        if re.search(it["regex"], hay):
            rows.append(("OK", mod, it["line"], scope, "defect expression still shipped"))
        else:
            rows.append(("DEFECT-GONE", mod, it["line"], scope,
                         "/%s/ no longer matches -- vanilla may have fixed it (REMOVE candidate, "
                         "not a verdict: read the replacement)" % it["regex"]))

    # a module with a real SRC pin but no DEFECT line anywhere: name it
    if any(i["kind"] in ("src", "src-none") for i in items) and \
       not any(i["kind"] == "defect" for i in items):
        rows.append(("NO-DEFECT", mod, 0, "",
                     "pinned but cannot state the expression it corrects (FIX_POLICY §2b exception)"))
    return rows


# --------------------------------------------------------------------------- #

def run(src, code, only=None):
    rows = []
    for fname in sorted(os.listdir(code)):
        if not fname.endswith(".lua"):
            continue
        if only and only not in fname:
            continue
        rows.extend(check_module(src, fname, os.path.join(code, fname)))
    return rows


def report(rows, show_all):
    counts = {}
    for kind, _m, _l, _t, _d in rows:
        counts[kind] = counts.get(kind, 0) + 1
    rows = sorted(rows, key=lambda r: (ORDER.get(r[0], 99), r[1], r[2]))
    for kind, mod, line, target, detail in rows:
        if kind in ("OK", "NO-MANIFEST") and not show_all:
            continue
        at = "%s.lua:%d" % (mod, line) if line else "%s.lua" % mod
        print("%-13s %s" % (kind, at))
        if target:
            print("              target  %s" % target)
        print("              %s" % detail)
    print("=" * 78)
    stamped = len(set(r[1] for r in rows if r[0] != "NO-MANIFEST"))
    print("%d manifest row(s) over %d stamped module(s); %d module(s) carry no manifest."
          % (len([r for r in rows if r[0] != "NO-MANIFEST"]), stamped,
             counts.get("NO-MANIFEST", 0)))
    print("  " + ", ".join("%d %s" % (counts[k], k) for k in
                           sorted(counts, key=lambda k: ORDER.get(k, 99))))
    print("A GREEN here is NOT a clearance: it sees a changed body, a vanished defect")
    print("and a vanished target. It does NOT see semantics moving under a wrapper")
    print("(class c), and it sees nothing at all for a NO-DEFECT or NO-MANIFEST module.")
    return 1 if any(r[0] in FAIL_KINDS for r in rows) else 0


# --------------------------------------------------------------------------- #
# --pin: emit a manifest line rather than hand-typing a hash
# --------------------------------------------------------------------------- #

def pin(src, path, selector):
    text, where, why = resolve(src, path, selector)
    if text is None:
        print("cannot pin: %s" % why)
        return 2
    print("-- SRC: %s %s sha256=%s" % (path.replace("\\", "/"), selector, body_hash(text)))
    print("--   (%s, %d line(s) hashed; read them before you trust the pin)"
          % (where, text.count("\n") + 1))
    return 0


# --------------------------------------------------------------------------- #
# --selftest: the falsifier. A tool that returns GREEN on everything is
# indistinguishable from a broken one -- that is how F114 shipped past three
# instruments -- so this asserts each verdict against a KNOWN case before
# anybody trusts a run.
# --------------------------------------------------------------------------- #

# Every game-side case below is a real event in the 1.0.7 -> 1.1.0 update, not a
# contrivance. ⚠️ ONE HONEST LIMIT, stated rather than papered over: the 1.0.7
# tree is GONE from disk (EF-075), so no true 1.0.7-vs-1.1.0 body pair exists to
# hash. BODY-CHANGED is therefore exercised on (i) a real body edit in our own
# tree -- F116's in-body repair at add94b3, a genuine "the body under the pin
# moved" event -- and (ii) a hash negative control. The MECHANISM is proven; a
# game-side 1.0.7 pair is not available to prove it on.

FIXTURES = {
    # 1. DEFECT-GONE, real, game-side: one of the 32. 1.1.0 deleted the Food and
    #    maintenance branches outright (SavegameFixups.InsufficientResourcesGridOnly
    #    says so in words) and MinDaysFoodSupplyBeforeNotification is gone from
    #    the whole tree -- while the function it lived in is still there and
    #    still has our arity. Invisible to Require and to sigcheck.
    "Fix_SelftestDefectGone.lua": [
        "-- SRC: Lua/ResourceTracking.lua ResourceTracking:GatheredResourcesOnHourlyUpdate sha256=%(rt_sha)s",
        "-- DEFECT: MinDaysFoodSupplyBeforeNotification",
    ],
    # 2. TARGET-ABSENT, real, game-side: Colonist:UpdateSatisfaction is declared
    #    nowhere in the 1.1.0 tree (sigcheck reports the same site ABSENT).
    "Fix_SelftestTargetAbsent.lua": [
        "-- SRC: Lua/Units/Colonist.lua Colonist:UpdateSatisfaction sha256=%(zero)s",
    ],
    # 3. OK control, real: the live body pinned to its own hash, with a defect
    #    expression that IS still shipped (F46 is not fixed in 1.1.0 -- the
    #    unload is still computed from the station cap alone, with no
    #    IsResourceEnabled check anywhere). Without this row a tool that
    #    returned RED on everything would also "pass".
    "Fix_SelftestOk.lua": [
        "-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=%(train_sha)s",
        "-- DEFECT: Min\\(carried,\\s*station_cap\\)",
    ],
    # 3b. THE REFACTOR TRAP, kept as a fixture because writing this file walked
    #     straight into it. F46's 1.0.7 phrasing was
    #     `station.demand[res]:GetTargetAmount()`; 1.1.0 hoisted it to
    #     `local demand = station.demand and station.demand[res]` /
    #     `demand:GetTargetAmount()` (Train.lua:794-795) -- a REFACTOR, and the
    #     defect is untouched. A DEFECT: pinned to the phrasing therefore reports
    #     DEFECT-GONE for a bug that is still shipped: a FALSE "vanilla fixed
    #     it", the exact direction that retires a live fix (R-15's shape).
    #     ⇒ FIX_POLICY §2b: state the DEFECT, never the phrasing. This row locks
    #     the lesson in so a later session meets it as a PASS, not as a surprise.
    "Fix_SelftestRefactorTrap.lua": [
        "-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=%(train_sha)s",
        "-- DEFECT: station\\.demand\\[res\\]:GetTargetAmount\\(\\)",
    ],
    # 4. BODY-CHANGED, hash negative control: the same live target with one hex
    #    digit of the pin flipped. Proves the comparison is against the tree and
    #    not against itself.
    "Fix_SelftestBodyChanged.lua": [
        "-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=%(train_bad)s",
    ],
    # 5. MALFORMED: a manifest that looks like coverage and is not.
    "Fix_SelftestMalformed.lua": [
        "-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=nope",
    ],
    # 6. NO-MANIFEST: an unstamped module is a count, never a failure.
    "Fix_SelftestNoManifest.lua": [
        "-- an ordinary module header with no manifest at all",
    ],
    # 7. SRC-NONE + DEFECT@<path>: the DataPatch shape -- no function to hash,
    #    the defect stated against the shipped DATA. Real: 1.1.0 still ships
    #    modify_trait = "Religious" on the Saint preset (F-1's premise).
    "Fix_SelftestDataPatch.lua": [
        "-- SRC: none -- a preset patch has no function body to hash",
        '-- DEFECT@Data/TraitPreset.lua: modify_trait\\s*=\\s*"Religious"',
    ],
}

# The SET of kinds each fixture must produce -- a SRC line and a DEFECT line
# each report a row, so a stamped fixture whose hash matches and whose defect is
# gone legitimately yields {OK, DEFECT-GONE}.
EXPECT = {
    "Fix_SelftestDefectGone": {"OK", "DEFECT-GONE"},
    "Fix_SelftestTargetAbsent": {"TARGET-ABSENT", "NO-DEFECT"},
    "Fix_SelftestOk": {"OK"},
    "Fix_SelftestRefactorTrap": {"OK", "DEFECT-GONE"},
    "Fix_SelftestBodyChanged": {"BODY-CHANGED", "NO-DEFECT"},
    "Fix_SelftestMalformed": {"MALFORMED"},
    "Fix_SelftestNoManifest": {"NO-MANIFEST"},
    "Fix_SelftestDataPatch": {"SRC-NONE", "OK"},
}


def selftest(src):
    ok = True
    train, _w, why = resolve(src, "Lua/Units/Train.lua", "Train:UnloadAll")
    rt, _w, why2 = resolve(src, "Lua/ResourceTracking.lua",
                           "ResourceTracking:GatheredResourcesOnHourlyUpdate")
    if train is None or rt is None:
        print("SELFTEST CANNOT RUN: %s" % (why or why2))
        return 2
    train_sha = body_hash(train)
    subs = {"train_sha": train_sha, "rt_sha": body_hash(rt), "zero": "0" * 64,
            "train_bad": ("f" if train_sha[0] != "f" else "0") + train_sha[1:]}

    tmp = tempfile.mkdtemp(prefix="bodycheck_selftest_")
    for name, lines in FIXTURES.items():
        with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
            fh.write("\n".join(l % subs for l in lines) + "\n")

    rows = run(src, tmp)
    got = {}
    for kind, mod, _l, _t, _d in rows:
        got.setdefault(mod, set()).add(kind)
    for mod in sorted(EXPECT):
        want = EXPECT[mod]
        have = got.get(mod, set())
        good = have == want
        ok = ok and good
        print("  %-6s %-28s expected %-28s got %s"
              % ("PASS" if good else "FAIL", mod,
                 ",".join(sorted(want)), ",".join(sorted(have)) or "(nothing)"))

    # 8. BODY-CHANGED on a REAL body edit, from our own history: F116's in-body
    #    repair (add94b3) changed E:DemolishAndSplitTrack. Pin the pre-repair
    #    body, check the post-repair tree, and the tool must say the body moved.
    print("  ---- real body edit (F116 in-body repair, add94b3) ----")
    try:
        old = subprocess.check_output(["git", "show", "add94b3^:Code/Fix_TrackSalvageWipe.lua"],
                                      cwd=HERE, stderr=subprocess.STDOUT)
    except Exception as e:                                  # noqa: BLE001
        print("  SKIP   git show failed (%s) -- the real-body-edit leg did not run" % e)
        return 0 if ok else 1
    old_dir = tempfile.mkdtemp(prefix="bodycheck_f116_")
    os.makedirs(os.path.join(old_dir, "Code"))
    old_path = os.path.join(old_dir, "Code", "Fix_TrackSalvageWipe.lua")
    with open(old_path, "wb") as fh:
        fh.write(old)
    sel = "E:DemolishAndSplitTrack"
    old_body, _w, _y = resolve(os.path.join(old_dir, "Code"), "Fix_TrackSalvageWipe.lua", sel)
    new_body, _w, _y = resolve(CODE, "Fix_TrackSalvageWipe.lua", sel)
    if old_body is None or new_body is None:
        print("  FAIL   could not delimit %s on both sides" % sel)
        return 1
    mod_dir = tempfile.mkdtemp(prefix="bodycheck_f116mod_")
    with open(os.path.join(mod_dir, "Fix_F116Pin.lua"), "w", encoding="utf-8") as fh:
        fh.write("-- SRC: Fix_TrackSalvageWipe.lua %s sha256=%s\n" % (sel, body_hash(old_body)))
    kinds = set(k for k, _m, _l, _t, _d in run(CODE, mod_dir))
    good = "BODY-CHANGED" in kinds
    ok = ok and good
    print("  %-6s pre-repair pin vs the repaired body: expected BODY-CHANGED, got %s"
          % ("PASS" if good else "FAIL", ",".join(sorted(kinds))))
    # and the converse, so the leg is not just "always red"
    with open(os.path.join(mod_dir, "Fix_F116Pin.lua"), "w", encoding="utf-8") as fh:
        fh.write("-- SRC: Fix_TrackSalvageWipe.lua %s sha256=%s\n" % (sel, body_hash(new_body)))
    kinds = set(k for k, _m, _l, _t, _d in run(CODE, mod_dir))
    good = "BODY-CHANGED" not in kinds
    ok = ok and good
    print("  %-6s the repaired body pinned to itself: expected no BODY-CHANGED, got %s"
          % ("PASS" if good else "FAIL", ",".join(sorted(kinds))))

    print("=" * 78)
    print("SELFTEST: %s" % ("PASS -- every verdict fired on a known case" if ok else "*** FAIL ***"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--code", default=CODE)
    ap.add_argument("--all", action="store_true", help="also print OK and NO-MANIFEST rows")
    ap.add_argument("--module", help="limit to modules whose filename contains this")
    ap.add_argument("--pin", nargs=2, metavar=("PATH", "SELECTOR"),
                    help="print a ready-to-paste SRC: line for one target")
    ap.add_argument("--selftest", action="store_true", help="run the falsifier")
    a = ap.parse_args()

    if not os.path.isdir(a.src):
        print("source tree not found: %s" % a.src)
        return 2
    if a.pin:
        return pin(a.src, a.pin[0], a.pin[1])
    if a.selftest:
        return selftest(a.src)
    if not os.path.isdir(a.code):
        print("Code tree not found: %s" % a.code)
        return 2
    return report(run(a.src, a.code, a.module), a.all)


if __name__ == "__main__":
    sys.exit(main())
