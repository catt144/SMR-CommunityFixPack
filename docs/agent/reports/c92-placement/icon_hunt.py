"""Read-only installed-pack census and selected DDS contact sheets for C92.

Run from the repository root. Copyrighted payloads go only to --scratch.
Uses the repository FLPK table parser; no game process is started.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import mmap
from pathlib import Path
import re
import struct
import subprocess
import csv
from collections import defaultdict

from PIL import Image, ImageDraw
import zstandard


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unpack(buf, entry):
    name, flags, off, size = entry
    raw = buf[off:off + size]
    if flags == 0x10:
        return raw
    assert flags == 0x30 and raw[:4] == b"ZSTD", (name, flags)
    want, _, hdrlen = struct.unpack_from("<III", raw, 4)
    n = (hdrlen - 16) // 4
    starts = [hdrlen] + (list(struct.unpack_from(f"<{n}I", raw, 16)) if n else [])
    parts = []
    decoder = zstandard.ZstdDecompressor()
    for start, end in zip(starts, starts[1:] + [len(raw)]):
        chunk = raw[start:end]
        parts.append(decoder.stream_reader(io.BytesIO(chunk)).read()
                     if chunk[:4] == b"\x28\xb5\x2f\xfd" else chunk)
    result = b"".join(parts)[:want]
    assert len(result) == want, (name, len(result), want)
    return result


def original_comparison(path, scratch, current):
    """BPUL reader follows the local hpk crate's Header/DirEntry/walk layout.

    This historical ORIGINAL-game control is never evidence about current packing.
    """
    import lz4.block
    with path.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as buf:
        header = struct.unpack_from("<4s8I", buf)
        assert header[0] == b"BPUL"
        per, off, size = header[2], header[7], header[8]
        fragments = [struct.unpack_from("<II", buf, i) for i in range(off, off + size, 8)]
        entries = []

        def walk(index, prefix=""):
            pos, length = fragments[index * per]
            end = pos + length
            while pos < end:
                fid, flags, n = struct.unpack_from("<IIH", buf, pos)
                name = buf[pos + 10:pos + 10 + n].decode()
                pos += 10 + n
                if flags & 1:
                    walk(fid - 1, prefix + name + "/")
                else:
                    entries.append((prefix + name, fragments[(fid - 1) * per:fid * per]))

        walk(0)
        names = {"advanced_drone_drive", "eureka", "metal_foams", "polymer_autosynthesis",
                 "smart_alloys", "standardized_integration"}
        rows = []
        for name, parts in entries:
            if Path(name).stem not in names:
                continue
            raw = b"".join(buf[start:start + count] for start, count in parts)
            assert raw[:4] == b"LZ4 " and struct.unpack_from("<I", raw, 12)[0] == 16
            data = lz4.block.decompress(raw[16:], uncompressed_size=struct.unpack_from("<I", raw, 4)[0])
            im = Image.open(io.BytesIO(data)).convert("RGBA")
            dest = scratch / "original_control" / Path(name).name
            dest.parent.mkdir(exist_ok=True)
            dest.write_bytes(data)
            im.save(dest.with_suffix(".png"))
            rows.append(dict(path=name, dds_sha256=sha(data), pixel_sha256=sha(im.tobytes()),
                             width=im.width, height=im.height,
                             same_pixels_as_relaunched=sha(im.tobytes()) == current[name]["pixel_sha256"]))
        assert any("advanced_drone_drive" in r["path"] for r in rows)
        manifest_path = path.parents[3] / "appmanifest_464920.acf"
        manifest = manifest_path.read_text(encoding="utf-8")
        return dict(path=str(path), bytes=len(buf), table_sha256=sha(buf[off:off + size]),
                    appid="464920", buildid=re.search(r'"buildid"\s+"(.*?)"', manifest)[1],
                    entries=len(entries), research_entries=sum("/Research/" in n for n, _ in entries),
                    comparisons=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--original-hpk", type=Path)
    parser.add_argument("--proof", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[4]
    spec = importlib.util.spec_from_file_location("flpk", repo / "tools/flpk_extract.py")
    flpk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flpk)
    assert flpk._selftest()
    args.scratch.mkdir(parents=True, exist_ok=True)
    tech = (args.game / "ModTools/Src/Data/Tech.lua").read_text(encoding="utf-8")
    refs = sorted(set(x.removesuffix(".png") for x in re.findall(r'Icon = "UI/(.*?)"', tech)))
    out = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
           "game": str(args.game), "tech_sha256": sha(tech.encode()),
           "distinct_tech_icon_references": len(refs), "packs": [], "selected": []}
    manifest_path = args.game.parents[1] / "appmanifest_3215050.acf"
    manifest = manifest_path.read_text(encoding="utf-8")
    out["manifest"] = {"path": str(manifest_path), "sha256": sha(manifest.encode()),
                       "appid": re.search(r'"appid"\s+"(.*?)"', manifest)[1],
                       "buildid": re.search(r'"buildid"\s+"(.*?)"', manifest)[1]}
    inventory = []
    images = []
    for path in sorted(args.game.rglob("*.fpk")):
        with path.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as buf:
            label = path.relative_to(args.game).as_posix()
            info = {"pack": label, "bytes": len(buf), "magic": buf[:4].hex()}
            out["packs"].append(info)
            if buf[:4] != b"FLPK":
                info["unread"] = "Not FLPK"
                continue
            doff = struct.unpack_from("<I", buf, 12)[0]
            dsize = struct.unpack_from("<I", buf, 20)[0]
            entries = []
            flpk.parse_table(buf, doff, dsize, doff, "", entries)
            info.update(entries=len(entries), table_sha256=sha(buf[doff:doff + dsize]),
                        root_categories=sorted(set(e[0].split("/")[0] if "/" in e[0] else "<root>" for e in entries)),
                        example_entries=[e[0] for e in entries[:5]])
            if entries:
                sample = unpack(buf, entries[0])
                info["payload_control"] = dict(path=entries[0][0], bytes=len(sample),
                                               sha256=sha(sample), prefix_hex=sample[:12].hex())
            for index, entry in enumerate(entries):
                name, flags, offset, size = entry
                inventory.append(dict(pack=label, index=index, path=name, flags=flags,
                                      offset=offset, stored_size=size))
            research = [e for e in entries if "/research/" in "/" + e[0].lower()]
            info["research_assets"] = len(research)
            info["name_leads"] = [e[0] for e in entries if re.search(
                r"underground|exploitat|extractor|deep.mining|advanced.drone|law", e[0], re.I)]
            if label == "Packs/UI.fpk":
                names = set(e[0] for e in entries)
                info["missing_tech_references"] = [r for r in refs if r + ".dds" not in names]
                info["unreferenced_research"] = [e[0] for e in research
                    if e[0].removesuffix(".dds") not in refs]
            chosen = [e for e in entries if e[0].lower().endswith(".dds") and
                      (e in research or label == "DLC/thomas.fpk" and e[0].startswith("UI/") or
                       re.search(r"laws/(underground_exploitation|drone_hub_efficiency|shuttle_fuel_efficiency|sensor_towers|diet)_", e[0], re.I))]
            for entry in chosen:
                data = unpack(buf, entry)
                name = entry[0]
                dest = args.scratch / label.replace("/", "_") / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                im = Image.open(io.BytesIO(data)).convert("RGBA")
                row = dict(pack=label, path=name, bytes=len(data), sha256=sha(data),
                           pixel_sha256=sha(im.tobytes()), width=im.width, height=im.height)
                out["selected"].append(row)
                images.append((label, name, im.copy()))
                im.save(dest.with_suffix(".png"))
    (args.scratch / "inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    for i in range(0, len(images), 48):
        group = images[i:i + 48]
        sheet = Image.new("RGB", (1440, 6 * 220), "#18202b")
        draw = ImageDraw.Draw(sheet)
        for j, (pack, name, im) in enumerate(group):
            x, y = (j % 8) * 180, (j // 8) * 220
            im.thumbnail((166, 166))
            sheet.paste(im, (x + (180 - im.width) // 2, y), im)
            stem = Path(name).stem
            if len(stem) > 26:
                split = stem.rfind("_", 0, 26)
                stem = stem[:split] + "\n" + stem[split + 1:] if split > 0 else stem
            draw.text((x + 3, y + 167), stem, fill="white")
            if "Laws/" in name:
                draw.text((x + 3, y + 207), "LAW", fill="#ffdc72")
        sheet.save(args.scratch / f"sheet_{i // 48 + 1:02}.jpg", quality=92)
    unreferenced = next(p["unreferenced_research"] for p in out["packs"] if p["pack"] == "Packs/UI.fpk")
    candidates = [p for p in unreferenced if not Path(p).stem.startswith("rm_")]
    out["all_source_references"] = {}
    roots = {"installed": args.game / "ModTools/Src"}
    if args.archive:
        roots["archive_1.0.7"] = args.archive
    for label, root in roots.items():
        matches = defaultdict(list)
        files = list(root.rglob("*.lua"))
        controls = []
        for path in files:
            content = path.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(content.splitlines(), 1):
                for name in re.findall(r'(?:UI/)?(Icons/Research/[^"\s\x27]+)', line, re.I):
                    key = str(Path(name).with_suffix(".dds")).replace("\\", "/")
                    if key in candidates:
                        matches[key].append(dict(file=path.relative_to(root).as_posix(), line=line_no,
                                                  text=line.strip()))
                    if "advanced_drone_drive" in key.lower():
                        controls.append(dict(file=path.relative_to(root).as_posix(), line=line_no))
        out["all_source_references"][label] = dict(root=str(root), lua_files=len(files),
            presence_control=controls, matches={name: matches[name] for name in candidates})
    groups = defaultdict(list)
    for row in out["selected"]:
        groups[row["pixel_sha256"]].append(row["path"])
    out["identical_pixel_groups"] = {h: names for h, names in groups.items() if len(names) > 1}
    if args.original_hpk:
        out["original_game_control"] = original_comparison(args.original_hpk, args.scratch,
            {row["path"]: row for row in out["selected"]})
    if args.archive:
        oldtech = (args.archive / "Data/TechPreset.lua").read_text(encoding="utf-8")
        out["legacy_icon_owners"] = {}
        for block in re.split(r"\n(?=PlaceObj\('TechPreset')", oldtech):
            icon = re.search(r'\n\ticon = "UI/(.*?)"', block)
            ident = re.search(r'\n\tid = "(.*?)"', block)
            if icon and ident:
                name = icon[1].removesuffix(".png") + ".dds"
                if name in candidates:
                    out["legacy_icon_owners"][name] = ident[1]
    focus_names = set(candidates) | {"Icons/Research/terraforming_subsidies.dds",
        "Icons/Research/advanced_drone_drive.dds", "Icons/Research/underground_deep_mining.dds",
        "Icons/Research/underground_water_extractor.dds", "Icons/Research/extra_scanning_speed.dds"}
    focus = [(p, n, im) for p, n, im in images if n in focus_names or "underground_exploitation" in n]
    sheet = Image.new("RGB", (1260, ((len(focus) + 6) // 7) * 230), "#18202b")
    draw = ImageDraw.Draw(sheet)
    for j, (pack, name, im) in enumerate(focus):
        x, y = j % 7 * 180, j // 7 * 230
        im = im.copy()
        im.thumbnail((166, 166))
        sheet.paste(im, (x + (180 - im.width) // 2, y), im)
        stem = Path(name).stem
        split = stem.rfind("_", 0, 24)
        if len(stem) > 24 and split > 0:
            stem = stem[:split] + "\n" + stem[split + 1:]
        draw.text((x + 3, y + 170), stem, fill="white")
        draw.text((x + 3, y + 212), "LAW" if "Laws/" in name else
                  "UNREFERENCED BY TECH" if name in candidates else "CONTROL", fill="#ffdc72")
    sheet.save(args.scratch / "focused_orphans_laws.jpg", quality=95)
    category_rows = []
    for block in re.split(r"\n(?=PlaceObj\('Tech')", tech):
        group = re.search(r'\n\tgroup = "([^"]+)"', block)
        if not group or not re.match(r"(?:Industry_|Hi.?tech_)", group[1], re.I):
            continue
        ident = re.search(r'\n\tid = "([^"]+)"', block)
        icon = re.search(r'\n\tIcon = "([^"]+)"', block)
        description = re.search(r'\n\tDescription = T\((.*?)\),\n', block, re.S)
        category_rows.append(dict(id=ident[1], group=group[1],
            icon=icon[1] if icon else "", obsolete=bool(re.search(r'\n\tObsolete = true', block)),
            description=description[1] if description else ""))
    category_rows.sort(key=lambda r: (r["group"], r["id"]))
    out["industry_hitech_census"] = dict(presets=len(category_rows),
        with_explicit_icons=sum(bool(r["icon"]) for r in category_rows),
        obsolete=sum(r["obsolete"] for r in category_rows))
    category_path = args.proof.parent / "industry_hitech_icons.tsv" if args.proof else args.scratch / "industry_hitech_icons.tsv"
    with category_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "group", "icon", "obsolete", "description"], delimiter="\t", quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(category_rows)
    lookup = {name: im for _, name, im in images}
    category_images = [(r["id"], r["group"] + (" OBSOLETE" if r["obsolete"] else ""),
                        lookup[r["icon"].removeprefix("UI/").removesuffix(".png") + ".dds"])
                       for r in category_rows if r["icon"]]
    for name in ("metal_foams", "polymer_autosynthesis", "smart_alloys", "grand_engineering",
                 "proximity_power_resonance", "advanced_elevator_hydraulics"):
        category_images.append((name, "UNREFERENCED ART", lookup[f"Icons/Research/{name}.dds"]))
    for start in range(0, len(category_images), 35):
        chunk = category_images[start:start + 35]
        sheet = Image.new("RGB", (1400, 1150), "#18202b")
        draw = ImageDraw.Draw(sheet)
        for j, (name, group, im) in enumerate(chunk):
            x, y = j % 7 * 200, j // 7 * 230
            im = im.copy()
            im.thumbnail((175, 166))
            sheet.paste(im, (x + (200 - im.width) // 2, y), im)
            label = name if len(name) <= 29 else name[:29] + "\n" + name[29:]
            draw.text((x + 3, y + 169), label, fill="white")
            draw.text((x + 3, y + 211), group, fill="#ffdc72")
        sheet.save(args.scratch / f"industry_hitech_{start // 35 + 1:02}.jpg", quality=95)
    args.output.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    if args.proof:
        proof = {k: v for k, v in out.items() if k not in ("packs", "selected")}
        proof["census"] = dict(packs=len(out["packs"]), entries=len(inventory),
            extracted_current_dds=len(out["selected"]),
            research_dds=sum("/Research/" in r["path"] for r in out["selected"]))
        proof["pack_controls"] = [{k: p[k] for k in ("pack", "entries", "table_sha256", "payload_control")}
                                   for p in out["packs"]]
        proof["art_packs"] = [p for p in out["packs"] if p["pack"] in
                              ("Packs/UI.fpk", "DLC/norman.fpk", "DLC/thomas.fpk")]
        proof["selected_art_digests"] = [r for r in out["selected"] if r["path"] in focus_names or
                                        "underground_exploitation" in r["path"]]
        args.proof.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"head": out["head"], "packs": len(out["packs"]),
                      "entries": len(inventory), "selected": len(images),
                      "summary": str(args.output)}, indent=2))
    for p in out["packs"]:
        if p["pack"] in ("Packs/UI.fpk", "DLC/norman.fpk", "DLC/thomas.fpk"):
            print(p["pack"], "entries=", p.get("entries"), "research=", p.get("research_assets"),
                  "missing_refs=", p.get("missing_tech_references", "n/a"))


if __name__ == "__main__":
    main()
