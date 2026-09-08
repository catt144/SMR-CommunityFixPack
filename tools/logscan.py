#!/usr/bin/env python3
"""Scan Surviving Mars logs for what the fix pack did, and for anything that threw.

Written 2026-09-08 for the first systematic 1.1.0 scan (brief
`docs/agent/prompts/TRAINS_AND_LOGSCAN_SITTING.md` §3). The point is that this
gets run again on EVERY game update, and a tool beats a habit.

    python tools/logscan.py                     # live log dir + docs/archive/logs
    python tools/logscan.py --build 6a91a190    # one game build only
    python tools/logscan.py --errors            # only logs that carry a throw
    python tools/logscan.py <path> [<path>...]  # specific files

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
import sys
from collections import Counter, OrderedDict

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
                bucket = r["packs"].setdefault(tag, {"verdicts": Counter(), "detail": OrderedDict()})
                s = MOD_STATUS.match(body)
                if s:
                    verdict = s.group("verdict")
                    bucket["verdicts"][verdict] += 1
                    # last verdict wins: a module can fail a pass then succeed
                    bucket["detail"][s.group("id")] = (verdict, s.group("tail").strip(), n)
                    if verdict == "SELF-CHECK OVERRIDDEN":
                        r["forced"].append((n, body))
                elif body.startswith("update report:") or body.startswith("ForceApply:") \
                        or "OVERRIDE LEG ARMED" in body or body.startswith("update dialog suppressed"):
                    r["report"].append((n, tag, body))

            for label, pat in ERROR_PATTERNS:
                if pat.search(line):
                    r["errors"].append((n, label, line.strip()))
                    break
    return r


def human_mtime(p):
    import datetime
    return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")


def report(meta, paths, r, errors_only=False):
    if errors_only and not r["errors"]:
        return False
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
        v = bucket["verdicts"]
        # recount from the LAST verdict per module, which is the truth
        final = Counter(x[0] for x in bucket["detail"].values())
        print("    [%s] %d modules seen -- %s" % (
            tag, len(bucket["detail"]),
            ", ".join("%s %d" % (k, final[k]) for k in sorted(final)) or "no per-module lines"))
        # name every non-applied module: SKIPs by name, never a total
        off = [(i, d) for i, d in bucket["detail"].items() if d[0] != "applied"]
        for mid, (verdict, tail, ln) in sorted(off, key=lambda x: x[1][2]):
            print("        %-6s %-32s %s  (:%d)" % (verdict[:6], mid, tail, ln))

    for n, tag, body in r["report"]:
        print("    >>> :%d [%s] %s" % (n, tag, body))

    if r["errors"]:
        print("    !!! %d ERROR-SHAPED LINE(S) -- VERBATIM, none discounted:" % len(r["errors"]))
        for n, label, line in r["errors"]:
            print("        :%-6d [%s] %s" % (n, label, line))
    else:
        print("    no error-shaped lines")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="specific log files (default: live dir + archive)")
    ap.add_argument("--build", help="only logs whose filename carries this build hash")
    ap.add_argument("--errors", action="store_true", help="only logs that carry a throw")
    a = ap.parse_args()

    found = discover(a.paths, a.build)
    if not found:
        print("no logs found (live dir: %s)" % LIVE_DIR)
        return 1

    shown = 0
    total_errors = 0
    for meta, paths in found:
        r = scan(paths[0])
        total_errors += len(r["errors"])
        if report(meta, paths, r, a.errors):
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
