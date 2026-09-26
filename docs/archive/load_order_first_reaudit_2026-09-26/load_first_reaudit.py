"""Re-audit exact 8ea5449 in a disposable export; no game or account mutation.

Run from repository root. Exported harnesses inherit main's git HEAD; this script
records and byte-checks the actual branch code identity separately. Existing
archives are only read. All generated output goes under scratch/.
"""
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path.cwd().resolve()
REV = "8ea54494362a2d0cf2e8a49225870fcf5245774e"
TREE = ROOT / "scratch/load_first_reaudit_8ea5449"
OUT = ROOT / "scratch/load_first_reaudit_results"
REPAIRS = ROOT / "docs/archive/load_order_first_repairs_2026-09-25"
OUT.mkdir(exist_ok=True)
if not TREE.exists():
    blob = subprocess.check_output(["git", "archive", "--format=zip", REV])
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        z.extractall(TREE)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def emit(label, value):
    print(label, json.dumps(value, ensure_ascii=False, sort_keys=True))


def run(label, args, cwd=TREE):
    p = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True)
    text = (p.stdout + p.stderr).decode("utf-8", errors="replace").replace("\r\n", "\n")
    (OUT / (label + ".txt")).write_text(text, encoding="utf-8", newline="\n")
    emit("RUN", {"name": label, "command": ["python", *args], "cwd": str(cwd), "exit": p.returncode,
                 "tail": text.splitlines()[-3:]})
    return p.returncode, text


emit("IDENTITY", {"code": REV, "records": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()})
for rel in ["Code/01_LoadFirst.lua", "Code/00_Core.lua", "metadata.lua", "items.lua", "tools/desk_load_first.py",
            "Code/Fix_VacuumWalks.lua", "Code/Fix_HubLocalAccess.lua", "Code/Hubset_OnHubNow.lua",
            "tools/arming/payloads/98_LoadFirstPack.lua.txt"]:
    data = (TREE / rel).read_bytes()
    assert data == subprocess.check_output(["git", "show", REV + ":" + rel]), rel
    emit("INPUT", {"file": rel, "sha256": sha(data)})

rc, baseline = run("baseline_and_mutants", ["tools/desk_load_first.py"])
assert rc == 0
assert run("killers", ["tools/desk_load_first.py", "--list"])[0] == 0
sys.path.insert(0, str(TREE / "tools"))
spec = importlib.util.spec_from_file_location("repaired", TREE / "tools/desk_load_first.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
base_lines = [s for s in baseline.splitlines() if s.startswith(("  PASS ", "  FAIL "))]
held = sum(s.startswith("  PASS ") for s in base_lines)
assert "BASELINE %d of %d demands held" % (held, len(base_lines)) in baseline
mutant_rows = []
for name in b.MUTANTS:
    rc, txt = run("mutant_" + name, ["tools/desk_load_first.py", "--mutant", name])
    assert rc == 0  # verbose mode reports individual failures; exit is not a kill verdict.
    members = [s for s in txt.splitlines() if s.startswith(("  PASS ", "  FAIL "))]
    failures = [s for s in members if s.startswith("  FAIL ")]
    assert len(members) == len(base_lines) and failures, name
    summary = next(s for s in baseline.splitlines() if re.match(r"^  " + re.escape(name) + r"\s+fails ", s))
    assert re.search(r"fails\s+%d of\s+%d demands" % (len(failures), len(members)), summary), name
    mutant_rows.append({"name": name, "failed": len(failures), "total": len(members), "summary": summary.strip()})
emit("MUTANT_MEMBERS", mutant_rows)
emit("MUTANT_TOTAL", {"members": len(mutant_rows), "with_failures": sum(r["failed"] > 0 for r in mutant_rows),
                      "baseline_held": held, "baseline_demands": len(base_lines)})
assert run("parsecheck", ["tools/parsecheck.py"])[0] == 0
assert run("preflight", ["tools/upload_preflight.py", "."])[0] == 0
assert run("extractor_selftest", ["tools/flpk_extract.py", "--selftest"], ROOT)[0] == 0

packages = []
for mode in ["nosave", "aftersave"]:
    fpk = REPAIRS / ("canary_pack_" + mode + "_ModContent.fpk")
    decoded = OUT / ("decoded_" + mode)
    assert run("decode_" + mode, ["-c", "import sys; sys.path.insert(0, 'tools'); from flpk_extract import extract; extract(sys.argv[1], sys.argv[2])", str(fpk), str(decoded)], ROOT)[0] == 0
    meta = (decoded / "metadata.lua").read_bytes()
    reference = (REPAIRS / ("canary_pack_" + mode + "_metadata.lua.txt")).read_bytes()
    assert meta == reference, mode
    text = meta.decode("utf-8")
    marker_hits = [i for i, s in enumerate(text.splitlines(), 1) if b.CANARY in s]
    id_hits = [i for i, s in enumerate(text.splitlines(), 1) if re.match(r"\s*'id',\s*\"SMR_LoadFirstCanaryScratch\"", s)]
    comment_hits = [i for i, s in enumerate(text.splitlines(), 1) if s.lstrip().startswith("--")]
    assert len(id_hits) == 1 and len(marker_hits) == (1 if mode == "nosave" else 0)
    row = {"mode": mode, "package_sha256": sha(fpk.read_bytes()), "package_bytes": fpk.stat().st_size,
           "metadata_sha256": sha(meta), "metadata_bytes": len(meta), "canary_lines": marker_hits,
           "id_lines": id_hits, "comment_lines": comment_hits,
           "members": sorted(str(p.relative_to(decoded)) for p in decoded.rglob("*") if p.is_file())}
    packages.append(row)
    emit("PACKAGE", row)
emit("PACKAGE_TOTAL", {"members": len(packages), "canary_counts": [len(p["canary_lines"]) for p in packages],
                       "id_counts": [len(p["id_lines"]) for p in packages], "comment_counts": [len(p["comment_lines"]) for p in packages]})

logs = []
for log in sorted(REPAIRS.glob("L*.log")):
    text = log.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    needles = ["Lua revision:", "Loaded mod items for:", "LoadFirst", "LOADFIRST", "CANARY", "LUA ERROR",
               "SMR_LoadFirstCanaryScratch", "PackModForBugReporter", "SaveWholeMod", "[PdxSDK]"]
    hits = [{"line": i, "text": s} for i, s in enumerate(lines, 1) if any(n in s for n in needles)]
    row = {"file": log.name, "sha256": sha(log.read_bytes()), "hits": hits,
           "build_lines": sum("Lua revision: 405907" in s for s in lines),
           "loaded_lists": sum("Loaded mod items for:" in s for s in lines),
           "lua_errors": sum("[LUA ERROR]" in s for s in lines)}
    assert row["build_lines"] == 1 and row["loaded_lists"] >= 1
    emit("LOG", row)
    logs.append(row)
emit("LOG_TOTAL", {"members": len(logs), "build_lines": sum(r["build_lines"] for r in logs),
                   "loaded_lists": sum(r["loaded_lists"] for r in logs), "lua_errors": sum(r["lua_errors"] for r in logs)})
