#!/usr/bin/env python3
"""Scan Surviving Mars logs for what the fix pack did, and for anything that threw.

Written 2026-09-08 for the first systematic 1.1.0 scan (brief
`docs/agent/prompts/TRAINS_AND_LOGSCAN_SITTING.md` §3). The point is that this
gets run again on EVERY game update, and a tool beats a habit.

    python tools/logscan.py                     # live log dir + docs/archive/logs
    python tools/logscan.py --build 6a91a190    # one game build only
    python tools/logscan.py --errors            # only logs that carry a throw
    python tools/logscan.py --retire            # the RETIRE-candidate list, log
                                                #   evidence merged with
                                                #   bodycheck.py's DEFECT-GONE
    python tools/logscan.py --selftest          # the falsifier
    python tools/logscan.py <path> [<path>...]  # specific files

⭐ A LATER LINE CAN OVERTURN A VERDICT (augment A-3, 2026-09-09). "Last verdict
wins" was wrong, and it was wrong in the direction that reassures: a DataPatch
module can log `inactive` on one pass and be restored to active by `ctx.heal()`
on a later one, and the heal prints site prose with no verdict keyword in it.
In the canonical 1.1.0 boot log `SaintBlessing` latches at :166 and heals at
:186, so the headline "17 inactive" was really 16 -- and the one module that
was actively breaking the Saint blessing (F-1) was hiding inside the number
that was supposed to reassure us.

⛔ HOW THE HEAL IS RECOGNISED, AND WHY NOT BY KEYWORD. The 1.1.0 re-verification
suggested matching `corrected` / `made effective` / `re-based` / `added ...
missing`. That list is wrong twice over against the pack as it actually stands:
  * it MISSES two of the three live `ctx.heal()` sites -- Sinkhole's heal prints
    "the St. Elmo's Fire sinkhole is now indestructible" and SaintBlessing's
    1.1.0 branch prints "the shipped code resolves the trait label itself ...",
    neither of which carries an edit verb. The 1.1.0 branch is the one that
    fires on the shipped game, so a keyword rule would report a healthy module
    dead on the branch we ship against.
  * and it CATCHES lines that are not heals. `re-based` and `restored` are
    SaintBlessing's SAVE re-base lines, which do not run through `ctx.heal()`
    at all; F92 records a measured near-miss from exactly that confusion.
So the shapes are DERIVED FROM THE PACK SOURCE instead: `pack_signals()` reads
Code/*.lua, finds each `ctx.heal()`, and takes the format string of the `log(`
call that follows it. Check the thing, not its label. When a heal site's prose
changes, the derivation follows it; when the source cannot be read, the tool
says UNRESOLVED rather than guessing.

⭐ A BENIGN LATCH IS A RETIRE SIGNAL, NOT A HEALTHY ONE (augment A-2). A
`DataPatch` pass that finds the shipped data "already correct" used to read as
fine. It is vanilla having fixed the defect -- R-13 sat in that branch while
being a module the pack no longer needed, and 32 modules survived an audit on
that reading. Benign latches are listed under their own heading, and `--retire`
merges them with `bodycheck.py`'s DEFECT-GONE rows so the two instruments
produce ONE list. ⚠️ Benign-ness is read from the pack source's third argument
to `ctx.latch`, never from the latch prose: `Fix_SaintBlessing:289` latches
NON-benign on purpose ("we do not recognise the body, so we did nothing"), and
a retire list that swallowed a fail-closed latch would retire a live fix.
⚠️ A RETIRE CANDIDATE IS NOT A VERDICT. Trace the replacement before retiring
anything -- a rename reads as "gone" and nearly retired a live fix (R-15).

WHAT IT WILL NOT DO
  * It never decides a line is uninteresting. Unrecognised error-shaped lines
    are printed VERBATIM with their line number, because "not caused by our
    leg" is an attribution verdict, not a dismissal, and every pushback this
    project has had on that has found a real defect.
  * It reports counts; it does not reconcile them against a stored baseline.
    A baseline lives in a fact file (EF-078) that a human reads. Automating
    that comparison would let a stale constant silently overrule a live
    reading, which is the exact failure mode the 1.1.0 launch punished.

BUILD HASHES SEEN SO FAR (the filename's last field, and a free build filter):
    6a22b86d = game 1.0.7.396349      6a91a190 = game 1.1.0.403908
    6a22b8b3 = MarsDebug.exe builds
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict

# The console on this rig is cp1252 and these tools print em-dashes, arrows and
# warning marks. Without this, `--help` alone raises UnicodeEncodeError -- which
# it already did for sigcheck.py, bodycheck.py and upload_preflight.py before
# 2026-09-09. `errors="replace"` so a redirected or piped run still cannot die
# on a character: a census tool that crashes instead of reporting is worse than
# one that prints a question mark.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # not a reconfigurable stream
        pass


# --- where logs live ---------------------------------------------------------

LIVE_DIR = os.path.join(
    os.environ.get("APPDATA", ""), "Surviving Mars Relaunched", "logs"
)
ARCHIVE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "archive", "logs",
)

LOG_NAME = re.compile(r"^(?P<exe>Mars(?:Debug)?\.exe)-(?P<date>\d{8})-(?P<time>[\d.]+)-(?P<build>[0-9a-f]+)\.log$")

# --- what we pull out --------------------------------------------------------

VERSION = re.compile(r"^\s*Build version:\s*(?P<v>\S+)")
LUAREV = re.compile(r"^\s*Lua revision:\s*(?P<v>\S+)")
MODDEF = re.compile(r"\[mod\]\s+Loaded mod def\s+(?P<rest>.+)$")
DLC = re.compile(r"\bDLC\b.*?\b(norman|thomas)\b", re.I)

# our own tagged lines
TAGGED = re.compile(r"\[(?P<tag>Community[A-Za-z]*Pack)\]\s*(?P<body>.*)$")
MOD_STATUS = re.compile(r"^(?P<id>[A-Za-z0-9_]+):\s*(?P<verdict>applied|inactive|disabled|FAILED to apply|SELF-CHECK OVERRIDDEN)\b(?P<tail>.*)$")
# any other `<Id>: <prose>` line the pack prints -- progress, a heal, a
# diagnostic. Carries no verdict word, which is exactly the problem A-3 fixes.
MOD_DETAIL = re.compile(r"^(?P<id>[A-Za-z0-9_]+):\s*(?P<tail>.+)$")
# the marker 00_Core.lua's ctx.latch prints for a benign latch (A-2). Present
# only in logs from 2026-09-09 onward; older logs fall back to the
# source-derived prose below, which is why both routes exist.
RETIRE_MARK = re.compile(r"already correct, RETIRE candidate")

# --- what the LOG cannot tell us, read from the pack source instead ----------

CODE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Code")

RE_HEAL = re.compile(r"^\s*ctx\.heal\(\)")
RE_LOG = re.compile(r'^\s*log\(\s*"((?:[^"\\]|\\.)*)"')
RE_LATCH = re.compile(r"ctx\.latch\(")
RE_STRLIT = re.compile(r'"((?:[^"\\]|\\.)*)"')


def fmt_to_regex(fmt):
    """A Lua `string.format` template -> a regex matching what it prints.

    `%s: ` is stripped: every one of these templates leads with the fix id,
    which the caller has already split off. `%d` and `%s` become wildcards;
    everything else is literal. Anchored at the start so a template cannot
    match in the middle of an unrelated sentence.
    """
    fmt = fmt.replace("\\n", " ").replace('\\"', '"')
    if fmt.startswith("%s: "):
        fmt = fmt[4:]
    out = re.escape(fmt)
    out = re.sub(r"%%", "\x00", out)
    out = re.sub(r"%d", r"[-\\d]+", out)
    out = re.sub(r"%s", r".+?", out)
    out = out.replace("\x00", "%")
    return re.compile("^" + out)


def _call_args(text, start):
    """Split the argument list of a Lua call whose '(' is at `start`.

    Returns (args, end). Depth-aware and string-aware, because a latch detail
    routinely contains a comma and a parenthesis.
    """
    i, depth, args, cur, quote = start + 1, 1, [], "", None
    while i < len(text) and depth > 0:
        ch = text[i]
        if quote:
            if ch == "\\":
                cur += text[i:i + 2]
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            args.append(cur.strip())
            cur = ""
            i += 1
            continue
        cur += ch
        i += 1
    if cur.strip():
        args.append(cur.strip())
    return args, i


def pack_signals(code_dir=None):
    """Derive the two line shapes a log alone cannot classify.

    heals   -- the `log(` template printed immediately after each `ctx.heal()`.
               A module that prints one of these AFTER an `inactive` ended the
               boot ACTIVE, because that is precisely what ctx.heal() does
               (00_Core.lua: restore an "inactive" mislabel to active).
    benign  -- the text a `ctx.latch(detail, log_suffix, benign)` prints when
               its THIRD argument is present. Read from the argument, never
               from the prose: a fail-closed latch and a retire-signal latch
               are both English sentences about data.

    Returns {"heals": [(module, regex, template)], "benign": [...],
             "source": <dir or None>}. An unreadable Code/ yields empty lists
             and the report says so -- it never falls back to guessing.
    """
    code_dir = code_dir or CODE_DIR
    sig = {"heals": [], "benign": [], "source": None}
    if not os.path.isdir(code_dir):
        return sig
    sig["source"] = code_dir
    for fn in sorted(os.listdir(code_dir)):
        if not fn.endswith(".lua"):
            continue
        path = os.path.join(code_dir, fn)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        lines = text.splitlines()
        mod = fn[:-4]

        # heals: the first log(" after each ctx.heal()
        for i, line in enumerate(lines):
            if not RE_HEAL.match(line):
                continue
            for nxt in lines[i + 1:i + 4]:
                m = RE_LOG.match(nxt)
                if m:
                    sig["heals"].append((mod, fmt_to_regex(m.group(1)), m.group(1)))
                    break

        # benign latches: ctx.latch(detail, log_suffix, benign)
        for m in RE_LATCH.finditer(text):
            args, _end = _call_args(text, m.end() - 1)
            if len(args) < 3 or args[2] in ("nil", "false"):
                continue
            # what it PRINTS is `log_suffix or detail`
            printed = args[1] if args[1] not in ("nil", "") else args[0]
            lit = RE_STRLIT.search(printed)
            if lit:
                sig["benign"].append((mod, fmt_to_regex(lit.group(1)), lit.group(1)))
    return sig

# throws. Deliberately broad -- a false positive costs one printed line, a
# false negative costs a shipped defect.
ERROR_PATTERNS = [
    ("LUA ERROR", re.compile(r"\[LUA ERROR\]", re.I)),
    ("assert", re.compile(r"\bassert(ion)?\s+fail", re.I)),
    ("nil index", re.compile(r"attempt to (index|call|compare|perform|concatenate)", re.I)),
    ("traceback", re.compile(r"\b(stack )?traceback\b", re.I)),
    ("blame", re.compile(r"\bfix pack\b.*\b(may be|blame|responsible)", re.I)),
    ("lua error kw", re.compile(r"^\s*(Error|ERROR)\b.*\.lua")),
]


def discover(paths, build=None):
    """Return an ordered list of (path, meta) for every log we should read."""
    files = []
    if paths:
        for p in paths:
            files.append(os.path.abspath(p))
    else:
        for d in (LIVE_DIR, ARCHIVE_DIR):
            if not os.path.isdir(d):
                continue
            for n in sorted(os.listdir(d)):
                if n.endswith(".log"):
                    files.append(os.path.join(d, n))

    out = OrderedDict()
    for f in files:
        base = os.path.basename(f)
        # archive copies carry a descriptive prefix (first110_, playtest110_)
        m = LOG_NAME.match(base)
        if not m:
            stripped = re.sub(r"^[A-Za-z0-9]+_", "", base)
            m = LOG_NAME.match(stripped)
        meta = m.groupdict() if m else {"exe": "?", "date": "?", "time": "?", "build": "?"}
        if build and meta.get("build") != build:
            continue
        # de-dupe archive copies of a live file by (date, time, build)
        key = (meta["date"], meta["time"], meta["build"], os.path.getsize(f))
        if key in out:
            out[key][1].append(f)
        else:
            out[key] = (meta, [f])
    return list(out.values())


def scan(path):
    """Read one log; return a dict of everything worth reporting."""
    r = {
        "version": None, "luarev": None, "moddefs": [], "dlc": set(),
        "packs": OrderedDict(), "errors": [], "forced": [], "report": [],
        "lines": 0,
    }
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for n, raw in enumerate(fh, 1):
            r["lines"] = n
            line = raw.rstrip("\n")

            m = VERSION.search(line)
            if m and not r["version"]:
                r["version"] = m.group("v")
            m = LUAREV.search(line)
            if m and not r["luarev"]:
                r["luarev"] = m.group("v")
            m = MODDEF.search(line)
            if m:
                r["moddefs"].append((n, m.group("rest").strip()))
            for d in DLC.findall(line):
                r["dlc"].add(d.lower())

            m = TAGGED.search(line)
            if m:
                tag, body = m.group("tag"), m.group("body").strip()
                bucket = r["packs"].setdefault(tag, {"verdicts": Counter(),
                                                     "detail": OrderedDict(),
                                                     "events": OrderedDict()})
                s = MOD_STATUS.match(body)
                if s:
                    verdict = s.group("verdict")
                    bucket["verdicts"][verdict] += 1
                    # FIRST-PASS view, kept as it was: last verdict wins. The
                    # heal-aware resolution below overturns it where a later
                    # line says so, and BOTH are printed -- a silently
                    # corrected number is destroyed evidence.
                    bucket["detail"][s.group("id")] = (verdict, s.group("tail").strip(), n)
                    bucket["events"].setdefault(s.group("id"), []).append(
                        ("verdict", verdict, s.group("tail").strip(), n))
                    if verdict == "SELF-CHECK OVERRIDDEN":
                        r["forced"].append((n, body))
                elif MOD_DETAIL.match(body) and not body.startswith("update report:") \
                        and not body.startswith("ForceApply:"):
                    d = MOD_DETAIL.match(body)
                    bucket["events"].setdefault(d.group("id"), []).append(
                        ("detail", None, d.group("tail").strip(), n))
                elif body.startswith("update report:") or body.startswith("ForceApply:") \
                        or "OVERRIDE LEG ARMED" in body or body.startswith("update dialog suppressed"):
                    r["report"].append((n, tag, body))

            for label, pat in ERROR_PATTERNS:
                if pat.search(line):
                    r["errors"].append((n, label, line.strip()))
                    break
    return r


def resolve(bucket, sig):
    """Final per-module state, with the evidence that produced it.

    -> OrderedDict id -> {"first": <last-verdict-wins verdict>, "final": ...,
                          "tail": ..., "line": ..., "healed": (n, text) | None,
                          "unresolved": (n, text) | None, "retire": bool}

    Three rules, in order, and each of them is a claim about `00_Core.lua`'s
    contract rather than about English:
      1. last verdict wins  -- unchanged, and reported as `first`.
      2. a HEAL overturns an `inactive`. Only `inactive`: `ctx.heal()` refuses
         to touch "disabled" (the user veto) or "error" (the A1 guard), so
         neither is ever promoted here either.
      3. a post-`inactive` line that matches NO known heal is UNRESOLVED, and
         is printed. It is not silently kept inactive and it is certainly not
         promoted -- "not caused by our leg" is an attribution verdict, not a
         dismissal, and the same applies to "probably not a heal".
    """
    out = OrderedDict()
    for mid, events in bucket["events"].items():
        verdicts = [e for e in events if e[0] == "verdict"]
        if not verdicts:
            continue
        _k, verdict, tail, ln = verdicts[-1]
        rec = {"first": verdict, "final": verdict, "tail": tail, "line": ln,
               "healed": None, "unresolved": None, "retire": False}
        if verdict == "inactive":
            for kind, _v, text, n in events:
                if kind != "detail" or n < ln:
                    continue
                if any(rx.match(text) for _m, rx, _t in sig["heals"]):
                    rec["final"] = "applied"
                    rec["healed"] = (n, text)
                    break
                rec["unresolved"] = (n, text)
        if rec["final"] == "inactive":
            rec["retire"] = bool(RETIRE_MARK.search(tail)) or any(
                rx.match(tail.strip("() ")) for _m, rx, _t in sig["benign"])
        out[mid] = rec
    return out


def defect_gone(src=None, code=None):
    """bodycheck.py's DEFECT-GONE rows -- the OTHER half of the retire bucket.

    Consumed, not re-implemented: bodycheck owns that check (hotfix2 link 01).
    A DEFECT-GONE and a benign latch are the same finding reached from two
    directions -- "the shipped code no longer has the fault we correct" and
    "the shipped data is already what we would write" -- so they belong on one
    list. Returns (rows, note); an unavailable bodycheck yields a note, never
    a silent empty list.
    """
    tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bodycheck.py")
    if not os.path.isfile(tool):
        return [], "bodycheck.py not found -- DEFECT-GONE half of the list is MISSING"
    cmd = [sys.executable, tool]
    if src:
        cmd += ["--src", src]
    if code:
        cmd += ["--code", code]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
    except Exception as e:                                   # noqa: BLE001
        return [], "bodycheck.py could not be run (%s) -- DEFECT-GONE half MISSING" % e
    # rows are `DEFECT-GONE   <module>.lua:<line>` followed by indented detail
    # lines, the LAST of which states why. bodycheck exits 1 on any red row, so
    # the return code is not an error signal here -- the rows are.
    rows, inside = [], False
    for line in (p.stdout or "").splitlines():
        m = re.match(r"^DEFECT-GONE\s+(\S+)", line)
        if m:
            rows.append([m.group(1), ""])
            inside = True
        elif line.startswith("      ") and line.strip():
            # an indented detail line belongs to the row above it -- and ONLY
            # to that row, or a later OK row's detail would overwrite the
            # reason of the DEFECT-GONE before it.
            if inside:
                rows[-1][1] = line.strip()
        else:
            inside = False
    return [tuple(r) for r in rows], None


def human_mtime(p):
    import datetime
    return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")


def report(meta, paths, r, errors_only=False, sig=None):
    if errors_only and not r["errors"]:
        return False
    sig = sig if sig is not None else {"heals": [], "benign": [], "source": None}
    primary = paths[0]
    print("=" * 78)
    print("%s   build %s   %s lines   %s" % (
        os.path.basename(primary), meta["build"], r["lines"], human_mtime(primary)))
    if len(paths) > 1:
        for extra in paths[1:]:
            print("    (also archived as %s)" % os.path.basename(extra))
    bits = []
    if r["version"]:
        bits.append("game " + r["version"])
    if r["luarev"]:
        bits.append("LuaRevision " + r["luarev"])
    if r["dlc"]:
        bits.append("DLC " + ",".join(sorted(r["dlc"])))
    if bits:
        print("    " + " · ".join(bits))

    for n, d in r["moddefs"]:
        print("    mod  %s" % d)

    for tag, bucket in r["packs"].items():
        # BOTH counts are printed, always. `first` is the old last-verdict-wins
        # reading; `final` is heal-aware. Where they differ the delta is stated
        # rather than quietly corrected -- a silently-corrected number is
        # destroyed evidence, and this project has published the old one.
        first = Counter(x[0] for x in bucket["detail"].values())
        res = resolve(bucket, sig)
        final = Counter(x["final"] for x in res.values())
        print("    [%s] %d modules seen -- %s" % (
            tag, len(bucket["detail"]),
            ", ".join("%s %d" % (k, final[k]) for k in sorted(final)) or "no per-module lines"))
        if first != final:
            healed = [(m, v) for m, v in res.items() if v["healed"]]
            print("        ^ heal-aware. FIRST-PASS (last verdict wins) read %s"
                  % ", ".join("%s %d" % (k, first[k]) for k in sorted(first)))
            for mid, v in healed:
                print("        HEALED %-30s %s ended ACTIVE: :%d %s"
                      % (mid, "inactive at :%d," % v["line"], v["healed"][0],
                         v["healed"][1]))
        # name every non-applied module: SKIPs by name, never a total
        off = [(m, v) for m, v in res.items() if v["final"] != "applied"]
        for mid, v in sorted(off, key=lambda x: x[1]["line"]):
            mark = "  <== RETIRE candidate" if v["retire"] else ""
            print("        %-6s %-32s %s  (:%d)%s"
                  % (v["final"][:6], mid, v["tail"], v["line"], mark))
            if v["unresolved"]:
                # loud on purpose: an unclassified line after an `inactive` may
                # be a heal this tool does not know about, and quietly keeping
                # the module inactive would be the same silent discount the
                # last-verdict-wins rule was making.
                print("            ??? UNRESOLVED post-inactive line, verdict NOT settled:"
                      "  :%d %s" % v["unresolved"])
        retire = [m for m, v in res.items() if v["retire"]]
        if retire:
            print("        RETIRE candidates (benign latch = vanilla already does it): %s"
                  % ", ".join(retire))
            print("        ⚠️ a candidate, never a verdict -- trace the replacement (R-15)")
        if not sig["source"]:
            print("        ⚠️ Code/ not readable: heal and benign-latch shapes could not be")
            print("           derived, so this census is LAST-VERDICT-WINS and may overcount")
            print("           `inactive` exactly as the pre-A-3 tool did.")

    for n, tag, body in r["report"]:
        print("    >>> :%d [%s] %s" % (n, tag, body))

    if r["errors"]:
        print("    !!! %d ERROR-SHAPED LINE(S) -- VERBATIM, none discounted:" % len(r["errors"]))
        for n, label, line in r["errors"]:
            print("        :%-6d [%s] %s" % (n, label, line))
    else:
        print("    no error-shaped lines")
    return True


def retire_report(found, sig, src=None):
    """ONE list of retire candidates, from both instruments (A-2).

    Two different questions with the same answer:
      * logscan  -- a benign latch: the shipped DATA is already what we would
                    write, so the pass has nothing to do.
      * bodycheck -- DEFECT-GONE: the defective EXPRESSION we correct is no
                    longer in the shipped body.
    They were reported in different places by different tools, which is part of
    how 32 already-fixed modules survived an audit. Merged here.
    """
    print("=" * 78)
    print("RETIRE CANDIDATES -- modules the shipped game may no longer need")
    print("=" * 78)

    latched = OrderedDict()
    for meta, paths in found:
        r = scan(paths[0])
        for _tag, bucket in r["packs"].items():
            for mid, v in resolve(bucket, sig).items():
                if v["retire"]:
                    latched.setdefault(mid, []).append(
                        "%s:%d" % (os.path.basename(paths[0]), v["line"]))

    print("\nbenign latch, seen in a log (%d):" % len(latched))
    if not latched:
        print("    none in the %d log(s) read" % len(found))
    for mid, where in latched.items():
        print("    %-32s %s" % (mid, ", ".join(where[:3])))

    rows, note = defect_gone(src)
    print("\nDEFECT-GONE, from bodycheck.py (%d):" % len(rows))
    if note:
        print("    ⚠️ %s" % note)
    for mod, detail in rows:
        print("    %-32s %s" % (mod, detail))

    print("\n" + "=" * 78)
    print("%d candidate(s) total." % (len(latched) + len(rows)))
    print("⚠️ A CANDIDATE IS NOT A VERDICT. \"vanilla fixed it\" is a claim: trace")
    print("the replacement body before retiring anything. A rename reads as")
    print("\"gone\" and nearly retired a live fix (R-15), and a DEFECT: pinned to")
    print("phrasing rather than to the fault reports GONE for a shipped bug.")
    return 0


# --- the falsifier -----------------------------------------------------------

SELFTEST_MODULE = '''\
	local run = SMRFixPack.DataPatch(FIX_ID, {
		pass = function(ctx)
			if changed then
				ctx.heal()
				log("%s: corrected %d dome-colonists trait modifier label(s) of %d",
					FIX_ID, changed, found)
			elseif resolved then
				ctx.heal()
				log("%s: the shipped code resolves the trait label itself \\u2014 data left untouched",
					FIX_ID)
			elseif found == 0 then
				ctx.latch("no dome-colonists trait presets found (game update changed it?)",
					"no dome-colonists trait presets")
			else
				ctx.latch("every dome-colonists trait preset already names a real label",
					nil, "benign")
			end
		end,
	})
	log("%s: re-based %d dome blessing(s) onto the label colonists are filed under", FIX_ID, n)
'''

SELFTEST_LOG = '''\
Build version: 1.1.0.403908
[mod] [CommunityFixPack] Alpha: applied
[mod] [CommunityFixPack] Bravo: inactive (no dome-colonists trait presets)
[mod] [CommunityFixPack] Charlie: inactive (every dome-colonists trait preset already names a real label)
[mod] [CommunityFixPack] Delta: inactive (something we do not recognise \\u2014 fail closed)
[mod] [CommunityFixPack] Echo: inactive (the shipped Sinkhole is already indestructible \\u2014 already correct, RETIRE candidate)
[mod] [CommunityFixPack] Foxtrot: disabled (vetoed)
[mod] [CommunityFixPack] Golf: inactive (no dome-colonists trait presets)
[mod] [CommunityFixPack] Bravo: corrected 1 dome-colonists trait modifier label(s) of 2
[mod] [CommunityFixPack] Golf: the shipped code resolves the trait label itself \\u2014 data left untouched
[mod] [CommunityFixPack] Delta: some later line that is not a heal at all
[mod] [CommunityFixPack] Foxtrot: the shipped code resolves the trait label itself \\u2014 data left untouched
[mod] [CommunityFixPack] Alpha: re-based 3 dome blessing(s) onto the label colonists are filed under
'''


def selftest():
    """Thirteen legs. A census tool that cannot go red is indistinguishable from one
    that agrees with you, and this project has now shipped two checkers that
    silently accused clean files."""
    import shutil
    import tempfile
    fails = []

    def check(label, cond, detail=""):
        print("  %-4s %s%s" % ("ok" if cond else "FAIL", label,
                               ("   " + detail) if detail and not cond else ""))
        if not cond:
            fails.append(label)

    tmp = tempfile.mkdtemp(prefix="logscan_selftest_")
    try:
        code = os.path.join(tmp, "Code")
        os.makedirs(code)
        with open(os.path.join(code, "Fix_Selftest.lua"), "w", encoding="utf-8") as fh:
            fh.write(SELFTEST_MODULE.replace("\\u2014", "—"))
        logp = os.path.join(tmp, "Mars.exe-20260909-00.00.00-6a91a190.log")
        with open(logp, "w", encoding="utf-8") as fh:
            fh.write(SELFTEST_LOG.replace("\\u2014", "—"))

        print("source derivation (pack_signals)")
        sig = pack_signals(code)
        # 1. BOTH heal sites are found, including the one with no edit verb.
        #    The keyword rule the report proposed finds only the first.
        check("both ctx.heal() sites derived, verb or no verb",
              len(sig["heals"]) == 2, repr([t for _m, _r, t in sig["heals"]]))
        # 2. ...and ONLY the benign latch is a retire signal. The fail-closed
        #    latch two lines above it must not be swallowed.
        check("only the ctx.latch(..., benign) site is a retire shape",
              [t for _m, _r, t in sig["benign"]]
              == ["every dome-colonists trait preset already names a real label"],
              repr(sig["benign"]))
        # 3. THE TRAP LEG. `re-based` is a SAVE re-base, not a ctx.heal(). F92
        #    records a measured near-miss from counting it as one.
        check("a `re-based` line NOT behind ctx.heal() is not a heal shape",
              not any(rx.match("re-based 3 dome blessing(s) onto the label "
                               "colonists are filed under")
                      for _m, rx, _t in sig["heals"]),
              repr([t for _m, _r, t in sig["heals"]]))

        print("resolution against a log")
        r = scan(logp)
        bucket = r["packs"]["CommunityFixPack"]
        res = resolve(bucket, sig)
        first = Counter(x[0] for x in bucket["detail"].values())
        final = Counter(x["final"] for x in res.values())
        # 4. the headline number actually moves -- the whole point of A-3
        check("heal overturns an earlier inactive",
              res["Bravo"]["final"] == "applied" and res["Bravo"]["healed"],
              repr(res.get("Bravo")))
        # 5. THE LEG THAT KILLS THE KEYWORD RULE, and it is the branch we ship
        #    against. Golf's heal carries NO edit verb -- it is SaintBlessing's
        #    1.1.0 branch, the one that fires on the shipped game. A
        #    `corrected|made effective|re-based|added` matcher reports this
        #    healthy module dead.
        check("a heal with NO edit verb still overturns an inactive",
              res["Golf"]["final"] == "applied" and res["Golf"]["healed"],
              repr(res.get("Golf")))
        # 6. ...and the first-pass reading is still available beside it
        check("first-pass count preserved for the delta",
              first["inactive"] == 5 and final["inactive"] == 3,
              "first=%r final=%r" % (dict(first), dict(final)))
        # 6. NEGATIVE CONTROL: an unrecognised post-inactive line must NOT heal
        check("an unrecognised post-inactive line does not heal",
              res["Delta"]["final"] == "inactive", repr(res.get("Delta")))
        # 7. ...and it is reported rather than silently discounted
        check("...it is flagged UNRESOLVED instead",
              res["Delta"]["unresolved"] is not None, repr(res.get("Delta")))
        # 8. `ctx.heal()` never touches "disabled" (the user veto), so neither
        #    does this: a heal line after a `disabled` must change nothing.
        check("a heal line after `disabled` promotes nothing",
              res["Foxtrot"]["final"] == "disabled", repr(res.get("Foxtrot")))
        # 9. retire list: source-derived prose (old logs) AND the new marker
        check("retire = benign prose + the RETIRE marker, and nothing else",
              sorted(m for m, v in res.items() if v["retire"]) == ["Charlie", "Echo"],
              repr({m: v["retire"] for m, v in res.items()}))
        # 10. THE CONVERSE. With no source to derive from, the tool must fall
        #     back to last-verdict-wins and NOT invent a heal. The two retire
        #     routes separate cleanly here: the LOG MARKER still stands on its
        #     own (Echo), the source-derived prose does not (Charlie).
        blind = resolve(bucket, {"heals": [], "benign": [], "source": None})
        check("no Code/ => no inferred heals; only the log marker survives",
              blind["Bravo"]["final"] == "inactive"
              and sorted(m for m, v in blind.items() if v["retire"]) == ["Echo"],
              repr({m: (v["final"], v["retire"]) for m, v in blind.items()}))

        print("the DEFECT-GONE half of --retire")
        # 12/13. END TO END through the REAL bodycheck.py, because "0 rows" from
        #    an unexercised parser and "0 rows" from a clean tree look identical,
        #    and this whole augment exists because a reassuring number was never
        #    checked. A fixture whose DEFECT: cannot match must come back as a
        #    parsed row; the same fixture with a matching DEFECT: must not.
        bcsrc = os.path.join(tmp, "Src", "Lua")
        os.makedirs(bcsrc)
        with open(os.path.join(bcsrc, "Fixture.lua"), "w", encoding="utf-8") as fh:
            fh.write("function Vanilla:Fixed(a)\n\treturn a + 1\nend\n")
        bccode = os.path.join(tmp, "BcCode")
        os.makedirs(bccode)
        hdr = ("-- SRC: Lua/Fixture.lua Vanilla:Fixed sha256=%s\n-- DEFECT: %s\n"
               % ("0" * 64, "%s"))
        with open(os.path.join(bccode, "Fix_Gone.lua"), "w", encoding="utf-8") as fh:
            fh.write(hdr % r"return\s+a\s*-\s*1")     # not in the shipped body
        rows, note = defect_gone(os.path.join(tmp, "Src"), bccode)
        check("a real DEFECT-GONE row is parsed, module and reason",
              note is None and len(rows) == 1 and rows[0][0].startswith("Fix_Gone")
              and "no longer matches" in rows[0][1], "%r / %r" % (rows, note))
        with open(os.path.join(bccode, "Fix_Gone.lua"), "w", encoding="utf-8") as fh:
            fh.write(hdr % r"return\s+a\s*\+\s*1")    # IS in the shipped body
        rows2, _n = defect_gone(os.path.join(tmp, "Src"), bccode)
        check("...and a defect that IS still shipped yields no row", rows2 == [],
              repr(rows2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("=" * 78)
    if fails:
        print("SELFTEST FAILED: %s" % ", ".join(fails))
        return 1
    print("selftest: 13 leg(s) pass. This falsifies the INFERENCE only -- it says")
    print("nothing about whether a module that logged `applied` actually works.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="specific log files (default: live dir + archive)")
    ap.add_argument("--build", help="only logs whose filename carries this build hash")
    ap.add_argument("--errors", action="store_true", help="only logs that carry a throw")
    ap.add_argument("--retire", action="store_true",
                    help="the RETIRE-candidate list: benign latches merged with "
                         "bodycheck.py's DEFECT-GONE rows")
    ap.add_argument("--src", help="ModTools/Src for the bodycheck half of --retire")
    ap.add_argument("--selftest", action="store_true",
                    help="falsify the heal-aware and benign-latch inference")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    sig = pack_signals()
    if not sig["source"]:
        print("⚠️ Code/ not found -- heal-aware resolution is DISABLED for this run.")

    found = discover(a.paths, a.build)
    if not found:
        print("no logs found (live dir: %s)" % LIVE_DIR)
        return 1

    if a.retire:
        return retire_report(found, sig, a.src)

    shown = 0
    total_errors = 0
    for meta, paths in found:
        r = scan(paths[0])
        total_errors += len(r["errors"])
        if report(meta, paths, r, a.errors, sig):
            shown += 1

    print("=" * 78)
    print("%d log(s) matched, %d shown, %d error-shaped line(s) total." % (
        len(found), shown, total_errors))
    if total_errors:
        print("Report every one of them with its age. 'Not caused by our leg' is an")
        print("attribution verdict, not a dismissal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
