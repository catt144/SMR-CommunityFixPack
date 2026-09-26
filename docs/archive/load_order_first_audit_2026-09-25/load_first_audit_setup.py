"""Export the audited tree without changing the installed checkout or junction."""
import io
import subprocess
import zipfile
from pathlib import Path

root = Path.cwd().resolve()
target = root / "scratch/load_first_audit_8e2325a"
assert not target.exists(), target
blob = subprocess.check_output(["git", "archive", "--format=zip", "8e2325a"], cwd=root)
with zipfile.ZipFile(io.BytesIO(blob)) as archive:
    archive.extractall(target)
print("ARCHIVE_SOURCE", subprocess.check_output(["git", "rev-parse", "8e2325a"], cwd=root, text=True).strip())
print("SCRATCH", target)
print("NOTE: git HEAD inside this export resolves to parent records main; code identity is ARCHIVE_SOURCE.")
