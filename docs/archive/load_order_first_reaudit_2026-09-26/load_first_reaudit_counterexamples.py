"""Source-backed counterexamples to repaired report section 12's sitting plan.

Run from repo root after load_first_reaudit.py. Uses exact 8ea5449 Lua under the
builder's real-core/sandbox fixture. Queue decisions are extracted from archived
1.1.1.405907; coroutine yielding models an outstanding asynchronous callback.
No game, network, account, installed mod, or existing archive is written.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = Path.cwd()
tree = root / "scratch/load_first_reaudit_8ea5449"
sys.path.insert(0, str(tree / "tools"))
spec = importlib.util.spec_from_file_location("branch", tree / "tools/desk_load_first.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
module = (tree / b.MODULE).read_text(encoding="utf-8")
assert hashlib.sha256(module.encode()).hexdigest() == "c7fdea6a3c878fb49d9e8f5bdf25b369c7eabb3600d4b106b530ec0a06838e79"
results = []


def demand(name, holds, **observed):
    row = {"name": name, "holds": bool(holds), "observed": observed}
    results.append(row)
    print("DEMAND", json.dumps(row, sort_keys=True))


# The original state named by the plan: option ON and pack later. Model the
# fresh readback boot after its restore slot, when option is still OFF.
p = b.PACK
start = ["Kit", "TrainHub", p, "OptIn", "RailShaft"]
c = b.Case(module, start, start, options={"LoadFirst": False})
c.run_threads()
demand("restoration control: OFF fresh readback retains captured order",
       c.raw() == ",".join(start) and c.saves() == 0, order=c.raw(), saves=c.saves())
c.toggle(True)  # exact final option click in section 12 E, no boot/reload
demand("section 12 E: restoring ON retains captured order until exit",
       c.raw() == ",".join(start), expected=",".join(start), actual=c.raw(),
       saves=c.saves(), pending=c.ev("SMRFixPack.LoadFirst.pending_notice"))
c.run_threads()
demand("restoration control: ON invokes repaired notice", c.questions() == 1,
       questions=c.questions(), actual=c.raw())

# Real queue removal and execution order, with one yielding task. The test is
# about queue state while an async callback is in flight, not PDX API results.
src = b.SRC / "CommonLua/Libs/Paradox/PdxSDK.lua"
lines = b.read_lines(str(src))
lua = b.db.lua_runtime()
lua.execute("PdxTaskQueue = {}; function CanYield() return true end; function sprocall(fn, ...) return fn(...) end")
for method in ["__Pop", "__WaitPop", "WaitDoTask"]:
    body, lo, hi = b.shipped_body(lines, r"^function PdxTaskQueue:" + method + r"\(")
    print("SOURCE_BODY", json.dumps({"build": "1.1.1.405907", "file": str(src), "method": method,
                                     "first": lo, "last": hi, "sha256": b.sha(body)}))
    lua.execute(body)
lua.execute("""
QUEUE = setmetatable({{function()
    STARTED = true
    coroutine.yield('async operation pending')
    DONE = true
end}}, {__index=PdxTaskQueue})
WORKER = coroutine.create(function() QUEUE:WaitDoTask() end)
assert(coroutine.resume(WORKER))
""")
demand("section 12 D: zero queue length proves callback completion",
       lua.eval("#QUEUE ~= 0 or DONE == true"), queued=lua.eval("#QUEUE"),
       started=lua.eval("STARTED"), done=lua.eval("DONE"), worker=lua.eval("coroutine.status(WORKER)"))
lua.execute("assert(coroutine.resume(WORKER))")
demand("queue control: resume permits real completion", lua.eval("DONE == true"),
       queued=lua.eval("#QUEUE"), done=lua.eval("DONE"), worker=lua.eval("coroutine.status(WORKER)"))

# Fingerprints and narrow source excerpts used by the verdict.
manifest = {}
for line in (b.SRC.parent / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    digest, rel = line.split(None, 1)
    manifest[rel.strip().replace("\\", "/")] = digest
files = {
    "CommonLua/Libs/Paradox/PdxSDK.lua": [(894, 923)],
    "CommonLua/UI/ModManager.lua": [(35, 41), (123, 166), (1864, 1885), (1902, 1929)],
    "CommonLua/Modding/Mod.lua": [(973, 993), (1153, 1170), (1487, 1503), (1995, 2001), (2104, 2112)],
    "CommonLua/Classes/GedModEditor.lua": [(713, 739), (742, 765)],
}
for rel, spans in files.items():
    data = (b.SRC / rel).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert manifest[rel] == digest
    print("FINGERPRINT", json.dumps({"build": "1.1.1.405907", "file": rel, "sha256": digest, "manifest": "MATCH"}))
    lines = data.decode("utf-8").splitlines()
    for a, z in spans:
        print("SOURCE", rel, a, z)
        for n in range(a, z + 1):
            print(str(n) + ":" + lines[n - 1])
print("FINGERPRINT_TOTAL", len(files), "MATCH", len(files))
print("DEMAND_TOTAL", json.dumps({"members": len(results), "held": sum(r["holds"] for r in results),
                                 "failed_names": [r["name"] for r in results if not r["holds"]]}))
assert [r["holds"] for r in results] == [True, False, True, False, True]
