"""Read-only source fingerprint, full-suite reconciliation and canary-evidence census.

Run from the repo root after load_first_audit.py and the recorded desk suite/main
commands. Text output is the receipt; source reads always use archived 1.1.1.405907.
No archive file, game state or mod setting is changed.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = Path.cwd()
archive = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907")
results = root / "scratch/load_first_audit_results"
manifest = {}
for line in (archive / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    digest, rel = line.split(None, 1)
    manifest[rel.strip().replace("\\", "/")] = digest
sources = {
    "CommonLua/Modding/Mod.lua": [(973, 993), (1487, 1515), (1628, 1645), (1715, 1724), (1966, 2001), (2099, 2113)],
    "CommonLua/UI/ModManager.lua": [(35, 41), (123, 166), (1532, 1569), (1864, 1909)],
    "CommonLua/Classes/GedModEditor.lua": [(676, 681), (713, 751), (825, 843), (884, 893)],
    "CommonLua/Libs/Paradox/ParadoxMods.lua": [(165, 175)],
    "CommonLua/Platforms/steam/SteamWorkshop.lua": [(1, 25)],
    "CommonLua/AccountStorage.lua": [(166, 187)],
    "CommonLua/Core/types.lua": [(143, 148), (1028, 1037)],
}
for rel, spans in sources.items():
    data = (archive / "Src" / rel).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == manifest[rel], rel
    print("FINGERPRINT", json.dumps({"build": "1.1.1.405907", "file": rel, "sha256": digest, "manifest": "MATCH"}))
    lines = data.decode("utf-8").splitlines()
    for a, z in spans:
        print("SOURCE", rel, a, min(z, len(lines)))
        for n in range(a, min(z, len(lines)) + 1):
            print(str(n) + ":" + lines[n - 1])
print("FINGERPRINT_TOTAL", len(sources), "MATCH", len(sources))

suite = (results / "desk_suite.txt").read_text(encoding="utf-8")
members = re.findall(r"^  (desk_\S+\.py)\s+(HELD|REFUTED \(exit \d+\))$", suite, re.M)
assert int(re.search(r"DESK BENCH: (\d+) harness", suite)[1]) == len(members)
failed = [name for name, status in members if status != "HELD"]
main = (results / "main_failed_harnesses.txt").read_text(encoding="utf-8") + (results / "main_additional_failed_harnesses.txt").read_text(encoding="utf-8")
for name in failed:
    rel = "tools/" + name
    original = subprocess.check_output(["git", "show", "8e2325a:" + rel])
    assert (root / rel).read_bytes().replace(b"\r\n", b"\n") == original.replace(b"\r\n", b"\n"), name
    part = next(p for p in re.split(r"(?m)^COMMAND python tools/(?=\S+ on main )", main) if p.startswith(name))
    assert "\nEXIT 1\n" in part
    print("BASELINE_FAILURE", name, "same harness bytes; main rerun exit 1")
print("SUITE_MEMBERS", json.dumps(members))
print("SUITE_TOTAL", json.dumps({"members": len(members), "held": len(members)-len(failed), "refuted": failed}))

# Search decoded text, with known predictor/retail lines as the presence control.
folder = root / "docs/archive/load_order_first_2026-09-25"
keywords = ["GedModEditor", "DbgPackMod", "CANARY", "pack_predict", "upload_preflight", "Loaded mod items for:"]
census = {k: [] for k in keywords}
for path in sorted(folder.iterdir()):
    if path.suffix not in (".txt", ".log"):
        continue
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for key in keywords:
            if key in line:
                census[key].append({"file": path.name, "line": n, "text": line})
assert census["pack_predict"] and census["upload_preflight"] and census["Loaded mod items for:"]
for key, hits in census.items():
    print("CANARY_EVIDENCE_MEMBERS", json.dumps({"keyword": key, "hits": hits}))
print("CANARY_EVIDENCE_TOTAL", json.dumps({k: len(v) for k, v in census.items()}))
print("COST_ESTIMATE_PENDING_RUN", {"required_legs": [3, 4, 3, 2, 3], "total_minutes": sum([3, 4, 3, 2, 3]), "with_optional_pn_minutes": sum([3, 4, 3, 2, 3, 4])})
