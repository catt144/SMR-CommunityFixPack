"""Independent coordinator gates. Evidence is copied verbatim into 03A's report."""
from pathlib import Path
import argparse
import re
import subprocess
import sys
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT.parent / "SMR-BugFixPack-TestKit"
sys.path.insert(0, str(ROOT))
from tools.parsecheck import runtime  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("files", nargs="*")
ap.add_argument("--presence", action="store_true")
ap.add_argument("--ordered", action="store_true")
ap.add_argument("--evidence", type=Path,
                 default=ROOT / "scratch" / "smrtk_gate_evidence.md")
args = ap.parse_args()
output = []
failed = False

def say(line):
    output.append(line)
    print(line)

check, version = runtime()
if check is None:
    raise SystemExit(version)
metadata = (KIT / "metadata.lua").read_text(encoding="utf-8-sig")
assert check(metadata, "@metadata.lua") is None
reader = LuaRuntime(unpack_returned_tuples=True)
reader.execute("function PlaceObj(class, fields) local t={} for i=1,#fields,2 do t[fields[i]]=fields[i+1] end return t end")
mod = reader.execute(metadata)
code = [mod["code"][n] for n in range(1, len(mod["code"]) + 1)]
files = args.files or [p.relative_to(KIT).as_posix() for p in sorted((KIT / "Code").glob("*.lua"))
                      if re.match(r"(7\d_SMRTK|80_AgentSlots)", p.stem)] + ["Code/90_Loggers.lua"]
say("$ " + subprocess.list2cmdline(["python", "docs/agent/reports/SMRTK_FANOUT_GATES.py"] + sys.argv[1:]))
say("HEAD pack=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    + " testkit=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=KIT, text=True).strip())
ordered = ([p for p in code if not p.startswith("Code/") and p != "__const.lua"]
           + [p for p in code if p.startswith("Code/")])
if args.ordered:
    say("LOAD ORDER: ModDef.LoadCode non-Code pass, then Code pass; each preserves metadata order")
for filename in (ordered + [p for p in files if p not in code] if args.ordered else files):
    path = KIT / filename
    src = path.read_text(encoding="utf-8-sig")
    err = check(src, "@" + filename)
    say(f"PARSE {filename}: {'FAIL ' + str(err) if err else '0 errors'} [{version}]")
    failed |= bool(err)
    if filename not in files:
        continue
    say(f"BUILT {filename}: {len(src.splitlines())} lines")
    names = re.findall(r"\bfunction\s+([\w.:]+)\s*\(", src)
    say("FUNCTIONS " + filename + ": " + ", ".join(names))
    for label, pattern in [("NO SYNC", r"NetSyncEvent|LogCheatUsed"), ("NO BARE PRINT", r"^\s*print\(")]:
        matches = [(n, line) for n, line in enumerate(src.splitlines(), 1) if re.search(pattern, line)]
        say(f"{label} {filename}: {len(matches)} lines")
        for n, line in matches:
            say(f"  {n}: {line}")
        failed |= bool(matches)
    member = filename in code
    say(f"H-10 {filename}: {'listed' if member else 'MISSING'}")
    failed |= not member
if args.presence:
    source = Path("A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src/Data/CheatDef.lua")
    hits = [(n, line) for n, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1)
            if re.search(r"NetSyncEvent|LogCheatUsed", line)]
    say(f"PRESENCE Data/CheatDef.lua (build 24995074): {len(hits)} lines")
    for n, line in hits:
        say(f"  {n}: {line}")
    failed |= len(hits) < 13
say("$ python tools/doccheck.py")
result = subprocess.run([sys.executable, "tools/doccheck.py"], cwd=ROOT,
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
say(result.stdout.rstrip())
if result.stderr:
    say(result.stderr.rstrip())
failed |= result.returncode != 0
say("COORDINATOR GATES: " + ("FAIL" if failed else "PASS"))
if args.evidence:
    with args.evidence.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n```text\n" + "\n".join(output) + "\n```\n")
raise SystemExit(1 if failed else 0)
