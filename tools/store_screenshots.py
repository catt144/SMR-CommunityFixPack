#!/usr/bin/env python3
"""Build the store-gallery screenshots from the owner's marked-up originals.

The uploaders read `metadata.lua`'s screenshot1..5 (GedModEditor.lua:687-702,
ParadoxMods.lua:97-110) and reject any file over Steam's 1 MB
(SteamWorkshop.lua:85, :101) or Paradox's 2 MB (ParadoxMods.lua:87, :101). The
owner's PNGs are ~2 MB, so this re-encodes them as JPEG under a 1,000,000-byte
margin into `store_screenshots/`, which `ignore_files` keeps OUT of the pack
(`python tools/pack_predict.py .` shows them under IGNORED).

Re-run after editing an original: python tools/store_screenshots.py
"""
import os
import sys

from PIL import Image

SRC = r"C:\Dev\SMR-ScreenCaptures\c74_skins"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "store_screenshots")
LIMIT = 1_000_000  # Steam's cap is 1 MiB; keep a margin

# gallery order = screenshot1..3 in metadata.lua
MAP = [
    ("Metal Extractor 2.png", "1_rare_metals_drill_skin.jpg"),
    # the original circled the stacked-squares button; the corrected copy circles Change Skin
    ("Metal Extractor 1 - corrected.png", "2_rare_metals_hammer_skin.jpg"),
    ("Water Extractor.png", "3_moxie_skins.jpg"),  # the owner's file shows the MOXIE
]


def main():
    os.makedirs(OUT, exist_ok=True)
    ok = True
    for src_name, out_name in MAP:
        im = Image.open(os.path.join(SRC, src_name)).convert("RGB")
        dst = os.path.join(OUT, out_name)
        for q in range(92, 49, -4):
            im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
            size = os.path.getsize(dst)
            if size <= LIMIT:
                break
        ok &= size <= LIMIT
        print(f"{out_name:<34} {im.size[0]}x{im.size[1]}  q={q}  {size:>9,} B  {'OK' if size <= LIMIT else 'TOO BIG'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
