#!/usr/bin/env python3
"""Desk bench -- run shipped game Lua under a real interpreter, at the desk, without a game.

Promoted 2026-09-09 on the owner's ruling (checklist 131) from four session
scratchpads: the two F117 falsifiers hotfix2 link 99a wrote and the two link 99b
wrote. Until then each re-implemented the same twenty lines and the transcript
pasted into a bug entry was all that survived a session. This module is the
shared half; the harnesses beside it (`tools/desk_*.py`) carry the demands.

    python tools/deskbench.py                 # run every desk_*.py, summarise
    python tools/desk_f117_argshape.py        # or any one harness on its own
    SMR_TESTKIT=<path> SMR_SRC_ARCHIVE=<path>  # override the two local-only trees

What every harness here does, and why it is trusted exactly as far as it is:

  * SHIPPED BODIES ARE EXTRACTED, NEVER RETYPED. `body()` uses
    tools/luafn.find_bodies -- the ONE delimiter bodycheck.py hashes with -- on
    the live 1.1.0 tree (luafn.SRC) and the archived 1.0.7 tree (SRC_ARCHIVE).
    `load_at()` loads a body under its REAL file name and line offset, so an
    error raised inside it reads `Lua/Units/Colonist.lua:2914: attempt to call
    a nil value (method 'X')` -- byte-comparable to a game log line. That is the
    cheapest proof a harness walks the same path the game did, and the 99b
    harnesses use it to reproduce two sitting ERROR lines exactly.
  * OUR CODE IS EXTRACTED TOO. Module files are loaded whole through a stub
    SMRFixPack.Register; kit probe files through a mini SMRTest that mirrors
    00_TestCore's contracts; the F117 probe by its marker span. A harness names
    the few lines it retypes.
  * ENGINE TOLERANCES ARE SHIMMED, AND NAMED. Haemimont's ipairs/pairs iterate
    nothing on false/nil (_GameUtils.lua:415 relies on it), Min/Max skip a nil
    argument (:434), table.get is a nil-safe nested index. Stock Lua raises on
    all three, so ENGINE_SHIMS supplies them. A shim is a convention the shipped
    code depends on, not a claim about the game.
  * ⛔ BUT A STUB FOR A BODY THAT CAN *REFUSE* IS A BEHAVIOUR CHANGE, NOT A
    TOLERANCE -- the rule above does NOT extend to it, and the distinction cost a
    false finding that cleared a full audit (F59 "A3", filed and retracted
    2026-09-11; EF-092). desk_f59_interact.py stubbed GetResidenceComfort to
    `function() return 50,0 end`, which reads as inert because comfort SCORES were
    not what the test measured. The real body (Residence.lua:416-434) gates on
    ValidateBuilding (Workplace.lua:1316-1327), which tests `destroyed` -- so the
    constant stub DELETED a validity guard and three legs then "measured" a harm
    that cannot happen, repeatably, in a fixture that could not have produced the
    right answer. Shim what the shipped code needs to RUN; never what it uses to
    DECIDE. Before asserting a harm, list every stubbed function the result passes
    through and ask of each: can the real body return nil, validate, or reject?
    Cheap tell -- the claim turns on an object being in an unusual STATE
    (destroyed / demolishing / dying / disabled), which is exactly what validity
    helpers test. When you find one, keep BOTH legs (stub shows the difference,
    shipped body refutes it) so the artefact cannot be re-derived; desk_f59_*.py's
    `real_comfort=True` is the worked example. And note that a peer re-running
    your harness is NOT an independent check of your fixture: consistency across
    legs proves nothing when every leg shares one stub.

⚠️ WHAT THIS IS NOT. The desk Lua is lupa's, not the engine's; nothing here ran
in a game; a harness that holds shows that a probe or a recipe DISCRIMINATES on
the shipped bodies, never that a colony produces the trigger. Every harness
carries negative legs (a module registered but not applied, an over-broad
wrapper, a body that indexes neither table) precisely so that it can fail -- a
harness that cannot fail is not a falsifier, and a PASS from one enters the
record as coverage it never was.
"""
import glob
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from luafn import read_lines, find_bodies, SRC as SRC_LIVE  # noqa: E402

TESTKIT = os.environ.get("SMR_TESTKIT", r"C:\Dev\SMR-BugFixPack-TestKit")
SRC_ARCHIVE = os.environ.get("SMR_SRC_ARCHIVE", r"C:\Dev\SMR-SrcArchive\1.0.7.396349\Src")
TREES = {"1.1.0": SRC_LIVE, "1.0.7": SRC_ARCHIVE}

# probe messages carry em dashes; a cp1252 console would print them as '?'
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def lua_runtime(unpack_returned_tuples=True):
    from lupa import LuaRuntime
    return LuaRuntime(unpack_returned_tuples=unpack_returned_tuples)


def lua_version():
    import lupa
    return "%s | lupa %s" % (lua_runtime().eval("_VERSION"), lupa.__version__)


def body(rel, pattern, tree="1.1.0"):
    """-> (text, first_line, last_line) of the ONE shipped body matching `pattern`.

    1-based line numbers, so `load_at(rt, text, '=' + rel, first_line)` puts the
    body back at its real place in the file."""
    lines = read_lines(os.path.join(TREES[tree], rel))
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, "%s %s /%s/ -> %d hits" % (tree, rel, pattern, len(hits))
    s, e = hits[0]
    return "\n".join(lines[s:e + 1]), s + 1, e + 1


def span(rel, patterns, tree="1.1.0"):
    """-> (text, first_line, last_line) covering several bodies AND the lines
    between them -- for functions that close over file locals declared between
    them (e.g. _GameUtils.lua's is_welcoming_community / no_foot_route_dist)."""
    lines = read_lines(os.path.join(TREES[tree], rel))
    ranges = []
    for pat in patterns:
        hits = find_bodies(lines, pat)
        assert len(hits) == 1, "%s %s /%s/ -> %d hits" % (tree, rel, pat, len(hits))
        ranges.append(hits[0])
    lo = min(s for s, _ in ranges)
    hi = max(e for _, e in ranges)
    return "\n".join(lines[lo:hi + 1]), lo + 1, hi + 1


def read(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace").replace("\r\n", "\n")


def git_show(repo, rev, rel):
    """A file at a pinned commit -- how a harness keeps an OLD probe text as a
    regression leg after the working copy has moved on."""
    out = subprocess.check_output(["git", "-C", repo, "show", "%s:%s" % (rev, rel)])
    return out.decode("utf-8", "replace").replace("\r\n", "\n")


def load_at(rt, text, chunkname, first_line=1):
    """Load `text` so its line numbers match the file it came from."""
    src = "\n" * (first_line - 1) + text
    rt.eval("function(src, name) return assert(load(src, name)) end")(src, chunkname)()


def marker_span(path, begin, end):
    """Our own code between two marker comments, verbatim (the F117 probe)."""
    lines = read_lines(path)
    starts = [i for i, l in enumerate(lines) if begin in l]
    ends = [i for i, l in enumerate(lines) if end in l]
    assert len(starts) == 1 and len(ends) == 1, "%s/%s markers not found exactly once" % (begin, end)
    return "\n".join(lines[starts[0] + 1:ends[0]])


# The engine conventions the shipped bodies lean on and stock Lua does not have.
# Each line names the shipped line that would raise without it.
ENGINE_SHIMS = r'''
-- ipairs/pairs iterate nothing on false/nil (_GameUtils.lua:415 `ipairs(not no_elevators and ...)`)
local _ipairs, _pairs = ipairs, pairs
function ipairs(t) if type(t) ~= "table" then return _ipairs({}) end return _ipairs(t) end
function pairs(t) if type(t) ~= "table" then return _pairs({}) end return _pairs(t) end
-- Min/Max skip a nil argument (_GameUtils.lua:434 on the first elevator merge)
function Min(a, b) if a == nil then return b end if b == nil then return a end return a < b and a or b end
function Max(a, b) if a == nil then return b end if b == nil then return a end return a > b and a or b end
-- table.get: nil-safe nested index (C export; only a stub in LuaExportedDocs/Global/table.lua:106)
table.get = function(t, ...)
	for i = 1, select("#", ...) do
		if type(t) ~= "table" then return nil end
		t = t[(select(i, ...))]
	end
	return t
end
table.remove_entry = function(t, v) for i = #t, 1, -1 do if t[i] == v then table.remove(t, i) end end end
table.insert_unique = function(t, v) for _, x in ipairs(t) do if x == v then return end end t[#t + 1] = v end
table.clear = function(t) for k in pairs(t) do t[k] = nil end end
table.sortby = function(t, map) table.sort(t, function(a, b) return (map[a] or 0) < (map[b] or 0) end) end
empty_table = setmetatable({}, { __newindex = function() error("empty_table write") end })
max_int = 9223372036854775807
'''


class Bench:
    """Collects demands; `finish()` prints the tally and returns the exit code."""

    def __init__(self, title):
        self.title = title
        self.results = []
        print("=" * 78)
        print(title)
        print("=" * 78)
        print("lua:", lua_version())
        print()

    def check(self, label, ok, detail=""):
        self.results.append((bool(ok), label))
        print(("  PASS  " if ok else "  FAIL  ") + label + (("  -- " + str(detail)) if detail else ""))
        return ok

    def finish(self, held_msg="ALL DEMANDS HELD"):
        bad = [l for ok, l in self.results if not ok]
        print()
        print("=" * 78)
        print("%d of %d demands held" % (len(self.results) - len(bad), len(self.results)))
        if bad:
            print("REFUTED -- %d demand(s) failed:" % len(bad))
            for l in bad:
                print("   -", l)
            return 1
        print(held_msg)
        return 0


def main():
    harnesses = sorted(glob.glob(os.path.join(TOOLS, "desk_*.py")))
    if not harnesses:
        print("no tools/desk_*.py harness found")
        return 1
    summary = []
    for path in harnesses:
        name = os.path.basename(path)
        print("\n" + "#" * 78 + "\n# " + name + "\n" + "#" * 78, flush=True)
        rc = subprocess.call([sys.executable, path])
        summary.append((name, rc))
    print("\n" + "=" * 78)
    print("DESK BENCH: %d harness(es)" % len(summary))
    for name, rc in summary:
        print("  %-32s %s" % (name, "HELD" if rc == 0 else "REFUTED (exit %d)" % rc))
    return 0 if all(rc == 0 for _, rc in summary) else 1


if __name__ == "__main__":
    sys.exit(main())
