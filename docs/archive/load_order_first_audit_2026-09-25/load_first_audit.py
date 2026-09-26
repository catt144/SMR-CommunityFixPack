"""Fresh-seat audit of load-first 8e2325a; no game launch or installed-tree edits.

Run from the repository: python <this-file> <scratch-export-of-8e2325a> <output-dir>
The tree is checked byte-for-byte against git, except newline normalization.
The builder harness is run intact, with its whole-module omission switch, and
with only the promotion loops removed in a scratch file (restored and hashed).
Extra cases reuse its extracted 1.1.1.405907 helpers and real pack core/sandbox.
Thread scheduling, UI and disk remain desk stubs. The extra cases deliberately
drain startup threads BEFORE an ordinary later Options click.
"""
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

REV = "8e2325aa219efc253e2c957eb776ca77ca06a2d2"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = Path.cwd().resolve()
tree = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
assert tree.is_relative_to(root / "scratch"), tree
out.mkdir(parents=True, exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=root)


def emit(label, value):
    print(label, json.dumps(value, ensure_ascii=False, sort_keys=True))


emit("IDENTITY", {"code": REV, "records": git("rev-parse", "HEAD").decode().strip(),
                  "source": "archived 1.1.1.405907", "tree": str(tree)})
for rel in ["Code/01_LoadFirst.lua", "Code/00_Core.lua", "tools/desk_load_first.py",
            "Code/Fix_VacuumWalks.lua", "Code/Fix_HubLocalAccess.lua", "Code/Hubset_OnHubNow.lua",
            "metadata.lua", "items.lua"]:
    data = (tree / rel).read_bytes()
    assert data.replace(b"\r\n", b"\n") == git("show", REV + ":" + rel).replace(b"\r\n", b"\n"), rel
    emit("INPUT", {"file": rel, "sha256": sha(data)})


def run(label, argv):
    p = subprocess.run([sys.executable, *argv], cwd=tree, capture_output=True)
    (out / (label + ".txt")).write_bytes(p.stdout + p.stderr)
    text = p.stdout.decode("utf-8", errors="replace")
    results = [line.strip() for line in text.splitlines() if line.strip().startswith(("PASS ", "FAIL "))]
    emit("RUN", {"name": label, "command": [sys.executable, *argv], "exit": p.returncode,
                 "result_lines": len(results), "pass": sum(line.startswith("PASS ") for line in results),
                 "fail": sum(line.startswith("FAIL ") for line in results), "tail": text.splitlines()[-5:]})
    return p.returncode


assert run("builder", ["tools/desk_load_first.py"]) == 0
assert run("builder_omission", ["tools/desk_load_first.py", "--no-promotion"]) == 1
module = tree / "Code/01_LoadFirst.lua"
original = module.read_bytes()
loops = b"\t\tfor _, id in ipairs(list) do TurnModOff(id) end\n\t\tfor _, id in ipairs(wanted) do TurnModOn(id) end"
assert original.count(loops) == 1
try:
    module.write_bytes(original.replace(loops, b"\t\t-- AUDIT MUTANT: list rebuilding removed; registration retained"))
    assert run("promotion_loops_removed", ["tools/desk_load_first.py"]) == 1
    # The unmodified builder aborts at an inline assertion in case 5b. Keep
    # the call, remove only that assertion to reach all remaining demands.
    harness = tree / "tools/desk_load_first.py"
    original_harness = harness.read_bytes()
    assertion = b"assert(SMRFixPack.LoadFirst.Promote('desk') == nil)"
    assert original_harness.count(assertion) == 1
    try:
        harness.write_bytes(original_harness.replace(assertion, b"SMRFixPack.LoadFirst.Promote('desk')"))
        assert run("promotion_loops_removed_complete", ["tools/desk_load_first.py"]) == 1
    finally:
        harness.write_bytes(original_harness)
    assert harness.read_bytes() == original_harness
    emit("HARNESS_RESTORE", {"before_sha256": sha(original_harness), "after_sha256": sha(harness.read_bytes())})
finally:
    module.write_bytes(original)
assert module.read_bytes() == original
emit("SCRATCH_RESTORE", {"before_sha256": sha(original), "after_sha256": sha(module.read_bytes())})
assert run("parsecheck", ["tools/parsecheck.py"]) == 0
assert run("preflight", ["tools/upload_preflight.py", "."]) == 0

sys.path.insert(0, str(tree / "tools"))
spec = importlib.util.spec_from_file_location("builder", tree / "tools/desk_load_first.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
P = b.PACK
mods = ["A", "B", "C", P]
findings = []


def check(name, ok, **actual):
    findings.append({"name": name, "held": bool(ok), "actual": actual})
    emit("AUDIT_DEMAND", findings[-1])


def toggle(c, on):
    c.ex("rawset(Mods[%r].options, 'LoadFirst', %s); Msg('ApplyModOptions', %r)" %
         (P, "true" if on else "false", P))


# C1: real chronology, versus builder's toggle-before-first-thread-run fixture.
c = b.Case(["B", P, "C"], mods, options={"LoadFirst": False})
c.run_threads()
toggle(c, True)
c.run_threads()
check("late opt-in schedules a restart notice", c.questions() == 1,
      saved=c.saved(), saves=c.saves(), questions=c.questions(),
      pending=c.ev("SMRFixPack.LoadFirst.pending_notice"), threads=c.ev("#THREADS"))

c = b.Case([P, "B", "C"], mods)
c.run_threads()
toggle(c, False)
c.ex("TurnModOff(%r); TurnModOn(%r)" % (P, P))
toggle(c, True)
c.run_threads()
check("already-first boot then opt-in schedules a notice", c.questions() == 1,
      saved=c.saved(), saves=c.saves(), questions=c.questions())

c = b.Case(["B", P, "C"], mods)
c.run_threads()
toggle(c, False)
c.ex("TurnModOff(%r); TurnModOn(%r)" % (P, P))
toggle(c, True)
c.run_threads()
check("later promotion in same process notifies again", c.questions() == 2,
      saved=c.saved(), saves=c.saves(), questions=c.questions(),
      notice_shown=c.ev("SMRFixPack.LoadFirst.notice_shown"))

# C2: foreign slot bytes, valid at the writer's limit, cannot be discarded.
for label, foreign in [("blank lines", "alpha\n\nbeta\n"),
                       ("prefix collision", "SMRFixPack.LoadFirstExtra payload"),
                       ("full valid slot", "z" * 32768)]:
    c = b.Case(["B", P, "C"], mods, persistent=foreign)
    actual = c.slot() or ""
    tail = actual.partition("\n")[2]
    check("persistent data preserved: " + label, actual == foreign or tail == foreign,
          before_bytes=len(foreign), after_bytes=len(actual),
          before_sha256=sha(foreign.encode()), after_sha256=sha(actual.encode()),
          saved=c.saved(), saves=c.saves(), log=c.ev("table.concat(LOG, ' | ')") if len(foreign) > 100 else actual)

# Normal relative order, including duplicate/stale shapes, independently expanded.
shapes = list(itertools.permutations(["A", "B", "C", P]))
shapes += [("A", "B"), ("B", P, "B", "GHOST"), ("B", P, P, "C")]
shape_rows = []
for seed in shapes:
    c = b.Case(list(seed), mods)
    others = list(dict.fromkeys(x for x in seed if x != P))
    expected = list(seed) if P not in seed or seed[0] == P else [P, *others]
    want_saves = int(P in seed and seed[0] != P)
    held = c.saved().split(",") == expected and c.saves() == want_saves
    shape_rows.append({"seed": seed, "actual": c.saved(), "expected": expected,
                       "saves": c.saves(), "held": held})
emit("SHAPE_MEMBERS", shape_rows)
check("relative-order shape census", all(r["held"] for r in shape_rows),
      members=len(shape_rows), held=sum(r["held"] for r in shape_rows))

# D1 probe is net-zero only when its reserved id was absent; test LoadAllMods first too.
probe = "SMRFixPack.LoadFirst.probe"
seed = ["B", probe, P, "C"]
c = b.Case(seed, mods, account_load_all=True)
raw = b.lua_join(c.ev("AccountStorage.LoadMods"))
check("LoadAllMods leaves stale/probe ids untouched", raw == ",".join(seed),
      expected=",".join(seed), raw=raw, saves=c.saves())
for label, kw in [("config", {"config_load_all": True}), ("account", {"account_load_all": True})]:
    c = b.Case(["z", P], [P, "z"], **kw)
    check("LoadAllMods with pack sorted first is diagnosed: " + label,
          c.status("LoadFirst") == "inactive" and "LoadAllMods" in c.detail("LoadFirst"),
          status=c.status("LoadFirst"), detail=c.detail("LoadFirst"), saves=c.saves())

# S2 exact loader short-circuit, extracted in full; no manual simulation of its decision.
reload_body, start, end = b.shipped_body(b.mod_lines, r"^function ModsReloadItems\(")
c = b.Case([P, "B", "C"], mods)
c.run_threads()
c.ex("TurnModOff(%r); TurnModOn(%r)" % (P, P))
c.ex("function IsRealTimeThread() return true end; GetModsToLoad = function() return GetLoadingQueueShipped(GetModsEnabledByUser(), true) end")
c.ex("function table.map(t, field) local r = {}; for i, x in ipairs(t) do r[i] = x[field] end; return r end; function table.iequal(a, b) if #a ~= #b then return false end; for i=1,#a do if a[i] ~= b[i] then return false end end; return true end")
c.ex(reload_body)
c.ex("ModsReloadItems()")
check("S2 same-dialog disable/re-enable promotes", c.saved().split(",")[0] == P,
      saved=c.saved(), running=c.loaded(), saves=c.saves(), questions=c.questions(),
      source="1.1.1.405907 Mod.lua:%d-%d" % (start, end))

emit("AUDIT_TOTAL", {"members": len(findings), "held": sum(r["held"] for r in findings),
                     "failed": sum(not r["held"] for r in findings),
                     "failed_names": [r["name"] for r in findings if not r["held"]]})
(out / "extra_cases.json").write_text(json.dumps(findings, indent=2) + "\n", encoding="utf-8", newline="\n")

# Reconcile printed harness totals against their named members, not report prose.
for label in ["builder", "builder_omission", "promotion_loops_removed_complete"]:
    transcript = (out / (label + ".txt")).read_text(encoding="utf-8")
    demands = [line.strip() for line in transcript.splitlines()
               if line.strip().startswith(("PASS ", "FAIL "))]
    passed = sum(x.startswith("PASS ") for x in demands)
    assert "%d of %d demands held" % (passed, len(demands)) in transcript
    groups = {}
    for line in demands:
        status, title = line.split(None, 1)
        key = "shape" if title.startswith("shape") else title.split(":")[0].split()[0]
        groups.setdefault(key, []).append((status, title))
    emit("CONTROL_RECONCILE", {"run": label, "total": len(demands), "pass": passed,
                               "fail": len(demands)-passed, "groups": len(groups),
                               "all_pass_groups": [k for k, v in groups.items() if all(s == "PASS" for s, _ in v)]})

# Re-read decoded archived logs; pair absence with build and loaded-list presence.
logrows = []
for log in sorted((root / "docs/archive/load_order_first_2026-09-25").glob("L*.log")):
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    needles = ["Lua revision:", "Loaded mod items for:", "LoadFirst:", "fix LoadFirst",
               "VacuumWalks:", "HubLocalAccess:", "[PdxSDK] Started up", "[LUA ERROR]"]
    hits = [{"line": i, "text": s} for i, s in enumerate(lines, 1) if any(n in s for n in needles)]
    row = {"file": log.name, "sha256": sha(log.read_bytes()), "hits": hits,
           "lua_errors": sum("[LUA ERROR]" in s for s in lines),
           "build_lines": sum("Lua revision: 405907" in s for s in lines),
           "loaded_lists": sum("Loaded mod items for:" in s for s in lines)}
    assert row["build_lines"] == 1 and row["loaded_lists"] == 1
    logrows.append(row)
    emit("LOG", row)
emit("LOG_TOTAL", {"members": len(logrows), "build_lines": sum(r["build_lines"] for r in logrows),
                   "loaded_lists": sum(r["loaded_lists"] for r in logrows),
                   "lua_errors": sum(r["lua_errors"] for r in logrows)})
