"""Read-only identity checks and decoded, named Workshop sample for this report.

Writes decoded copies only to scratch/load_order_identity_decoded. The absence
claim is limited to the literal word dependencies in these metadata.lua files;
each file must also contain a title and internal id. This is not a Workshop census.
"""
import contextlib
import hashlib
import io
import re
import subprocess
import sys
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO / "tools"))
from flpk_extract import extract

ARCHIVE = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive")
LIVE = Path("A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src")
FILES = ["CommonLua/PropertyObject.lua", "CommonLua/Core/classes.lua", "CommonLua/Core/autorun.lua",
         "CommonLua/Core/lib.lua", "CommonLua/Dlc.lua", "CommonLua/UI/ModManager.lua"]
SAMPLES = {
    "archive": (Path("B:/Dev/SMR/SMR-Shared/workshop_fpk_archive"),
                ["3675370940", "3676027320", "3717125029", "3730839706", "3745475097", "3775120166"]),
    "installed": (Path("A:/SteamLibrary/steamapps/workshop/content/3215050"),
                  ["3607071753", "3787202810", "3799500849"]),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


print("HEAD", subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip())
manifest_path = Path("A:/SteamLibrary/steamapps/appmanifest_3215050.acf")
manifest = manifest_path.read_text(encoding="utf-8")
build_id = re.search(r'"buildid"\s+"(\d+)"', manifest).group(1)
assert build_id == "25390750", build_id
print("STEAM_BUILD", manifest_path, build_id)
for build in ["1.0.7.396349", "1.1.0.403908", "1.1.1.405907"]:
    manifest = {}
    for line in (ARCHIVE / build / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        value, path = line.split("  ", 1)
        manifest[path.replace("\\", "/")] = value.lower()
    modpath = "CommonLua/Classes/Mod.lua" if build.startswith("1.0.7") else "CommonLua/Modding/Mod.lua"
    for relative in [modpath] + FILES:
        data = (ARCHIVE / build / "Src" / relative).read_bytes()
        actual = digest(data)
        assert actual == manifest[relative], (build, relative, actual, manifest[relative])
        live_equal = ""
        if build == "1.1.1.405907":
            assert actual == digest((LIVE / relative).read_bytes()), ("LIVE_MOVED", relative)
            live_equal = " live=equal"
        print("SOURCE", build, relative, actual, "manifest=equal" + live_equal)

for group, (root, identifiers) in SAMPLES.items():
    seen = []
    positive = 0
    dependency_files = []
    for identifier in identifiers:
        package = root / identifier / "ModContent.fpk"
        target = REPO / "scratch/load_order_identity_decoded" / group / identifier
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            extract(str(package), str(target))
        assert "WARN" not in captured.getvalue() and "SKIP" not in captured.getvalue(), captured.getvalue()
        metadata = (target / "metadata.lua").read_text(encoding="utf-8-sig")
        fields = {}
        for field in ["title", "id"]:
            matches = re.findall(r"['\"]" + field + r"['\"]\s*,\s*['\"]([^'\"]+)['\"]", metadata)
            assert len(matches) == 1, (package, field, matches)
            fields[field] = matches[0]
        positive += 1
        if re.search(r"\bdependencies\b", metadata):
            dependency_files.append(identifier)
        print("PACKAGE", group, identifier, fields, "fpk_sha256=" + digest(package.read_bytes()),
              "metadata_sha256=" + digest((target / "metadata.lua").read_bytes()))
        seen.append(identifier)
    assert seen == identifiers and positive == len(identifiers)
    assert not dependency_files, (group, dependency_files)
    print("SAMPLE", group, "metadata=" + str(len(seen)), "title_id_controls=" + str(positive),
          "dependencies_files=" + str(len(dependency_files)), "members=" + ",".join(seen))

pn_live = (REPO / "scratch/load_order_identity_decoded/installed/3607071753/Code/PassageNetwork.lua").read_text(encoding="utf-8-sig")
pn_archive = (REPO / "docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua").read_text(encoding="utf-8-sig")
assert pn_live == pn_archive, "PassageNetwork normalized source differs from archived 1.38"
print("PASS PassageNetwork installed/archive source equal after newline normalization")
