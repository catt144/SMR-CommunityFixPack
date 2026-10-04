"""Read-only evidence collector for the 2026-10-04 upload audit.

Run from any directory: python <this file>. No uploads, game launches, saves,
tree changes, or DNS changes. The live log/package inputs can age out.
"""
import collections
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[4]
OPT = ROOT.parent / "SMR-OptInPack"
LAUNCH = ROOT.parent / "SMR-OptInPack-launch"
LOGS = Path(os.environ["APPDATA"]) / "Surviving Mars Relaunched/logs"
PACK = Path(os.environ["TEMP"]) / "Surviving Mars Relaunched/ModUpload/Pack/ModContent.fpk"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(label, value):
    print(label + " " + json.dumps(value, ensure_ascii=False, sort_keys=True))


def run(args, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, capture_output=True, check=True)
    return result.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n").strip()


emit("COMMAND", "python docs/agent/reports/optin_upload_audit_20261004/collect_evidence.py")
for repo in (ROOT, OPT):
    emit("REPO", {"path": str(repo), "head": run(["git", "rev-parse", "HEAD"], repo)})

for name in (
    "MarsDebug.exe-20261004-00.19.10-6aba6e9d.log",
    "MarsDebug.exe-20261004-00.32.43-6aba6e9d.log",
):
    path = LOGS / name
    data = path.read_text(encoding="utf-8", errors="replace")
    lines = data.splitlines()
    groups = {}
    for term in ("was not uploaded", "blkPageCompress.cpp(35)", "[PDXDBG]", "Reloading done"):
        members = [{"line": i, "text": line} for i, line in enumerate(lines, 1) if term in line]
        second = len(re.findall(re.escape(term), data))
        assert len(members) == second
        groups[term] = {"members": members, "line_count": len(members), "occurrence_control": second}
    assert groups["was not uploaded"]["line_count"] > 0
    assert groups["Reloading done"]["line_count"] > 0
    emit("LOG", {"path": str(path), "sha256": sha(path), "groups": groups,
                 "build": [line for line in lines if line.startswith(("Build version:", "Lua revision:", "Platform:"))],
                 "braze": [{"line": i, "text": line} for i, line in enumerate(lines, 1) if "[Braze]" in line]})

for repo, tree in ((ROOT, ROOT), (OPT, OPT), (OPT, LAUNCH)):
    predictor = repo / "tools/pack_predict.py"
    spec = importlib.util.spec_from_file_location("audit_predict_" + tree.name, predictor)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    packed, ignored, links = module.predict(str(tree))
    buckets = collections.Counter(name.split("/")[0] if "/" in name else "(root)" for name, _ in packed)
    assert sum(buckets.values()) == len(packed)
    emit("PREDICTION", {"tree": str(tree), "tool_sha256": sha(predictor),
                        "filter": module.IGNORE, "count": len(packed), "bucket_control": sum(buckets.values()),
                        "buckets": buckets, "members": [name for name, _ in packed], "links": links})

emit("PACK", {"path": str(PACK), "sha256": sha(PACK), "bytes": PACK.stat().st_size})
emit("PACK_COMMAND", [sys.executable, "tools/pack_list.py", str(PACK), "--tree", str(LAUNCH), "--names"])
print(run([sys.executable, "tools/pack_list.py", str(PACK), "--tree", str(LAUNCH), "--names"], OPT))

src = ROOT.parent / "SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src"
live = Path("A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src")
for rel in (
    "CommonLua/Classes/GedModEditor.lua",
    "CommonLua/Libs/Paradox/ParadoxMods.lua",
    "CommonLua/Modding/Mod.lua",
    "CommonLua/console.lua",
):
    emit("SOURCE", {"build": "1.1.1.406343", "path": rel, "archive_sha256": sha(src / rel),
                    "live_sha256": sha(live / rel), "archive_equals_live": (src / rel).read_bytes() == (live / rel).read_bytes()})
