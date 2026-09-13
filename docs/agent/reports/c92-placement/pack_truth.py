"""Read-only C92 shipped-payload comparison; no game code executes."""
import hashlib
import io
import json
import mmap
import re
import struct
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))
from flpk_extract import parse_table, ZMAGIC
import zstandard


def payload(buf, row):
    name, flags, off, size = row
    region = buf[off:off + size]
    if flags == 0x10:
        return region
    assert flags == 0x30 and region[:4] == b"ZSTD", name
    want, _, hdrlen = struct.unpack_from("<III", region, 4)
    n = (hdrlen - 16) // 4
    starts = [hdrlen] + (list(struct.unpack_from(f"<{n}I", region, 16)) if n else [])
    parts = []
    for start, end in zip(starts, starts[1:] + [len(region)]):
        data = region[start:end]
        if data[:4] == ZMAGIC:
            data = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(data)).read()
        parts.append(data)
    data = b"".join(parts)[:want]
    assert len(data) == want, (name, len(data), want)
    return data


def main():
    manifest = Path(r"A:\SteamLibrary\steamapps\appmanifest_3215050.acf")
    info = manifest.read_text(encoding="utf-8")
    game = manifest.parent / "common" / re.search(r'"installdir"\s+"([^"]+)"', info)[1]
    out = {
        "command": "python docs/agent/reports/c92-placement/pack_truth.py",
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "app": 3215050,
        "steam_build": re.search(r'"buildid"\s+"([^"]+)"', info)[1],
        "game_version": "1.1.0.403908",
        "game": str(game),
        "packs": [],
    }
    for pack, source_prefix, controls in [
        ("Packs/Data.fpk", "Data", ["Tech.lua", "TechGroup.lua"]),
        ("Packs/Lua.fpk", "", ["Lua/TechTree.lua", "Lua/Achievements.lua",
          "Lua/Buildings/WaterExtractor.lua", "Lua/Modifiers.lua", "Lua/LabelContainer.lua",
          "Lua/MarsGameEffects.lua", "CommonLua/Libs/Research/Research.lua"]),
        ("DLC/norman.fpk", "DLC/norman", ["Presets/Tech.lua"]),
        ("DLC/thomas.fpk", "DLC/thomas", ["Presets/MissionSponsorPreset.lua"]),
    ]:
        p = {"path": pack, "controls": [], "matches": [], "comparison": []}
        with (game / pack).open("rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as buf:
            assert buf[:4] == b"FLPK"
            off, size = struct.unpack_from("<I", buf, 12)[0], struct.unpack_from("<I", buf, 20)[0]
            rows = []
            parse_table(buf, off, size, off, "", rows)
            p["entries"] = len(rows)
            p["lua_payloads_read"] = 0
            for row in rows:
                name = row[0]
                if not name.endswith(".lua"):
                    continue
                data = payload(buf, row)
                p["lua_payloads_read"] += 1
                matched = b"UndergroundExploitation" in data
                if name in controls:
                    assert b"PlaceObj" in data or b"function" in data, name
                    p["controls"].append({"name": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
                if matched:
                    hits = [{"line": n, "text": line.strip()} for n, line in enumerate(data.decode("utf-8-sig").splitlines(), 1) if "UndergroundExploitation" in line]
                    p["matches"].append({"name": name, "hits": hits})
                if matched or name in controls:
                    src = game / "ModTools/Src" / source_prefix / name
                    old = src.read_bytes() if src.is_file() else None
                    p["comparison"].append({"name": name, "source": str(src), "packed_sha256": hashlib.sha256(data).hexdigest(), "source_exists": old is not None, "byte_identical": data == old})
            assert sorted(x["name"] for x in p["controls"]) == sorted(controls), (pack, p["controls"])
        out["packs"].append(p)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
