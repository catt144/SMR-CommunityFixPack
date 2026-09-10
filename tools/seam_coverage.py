"""Reproduce/check link 03's close-out receipt and disjoint continuation queues.

The full-read labels are the parent/reader attestations recorded in SEAM_REPORT.md,
not something this script measures. Original tagged inputs are never changed.
This is a dated snapshot; later links keep their own read receipts.
"""
import argparse
import csv
import io
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs/agent/reports/vanillahunt"
OUTPUT = REPORTS / "SEAM_COVERAGE.tsv"

GROUPS = {
    "food": "Lua/Buildings/FoodServiceBuilding.lua Lua/Meal.lua Lua/Buildings/RecipeProductionBuilding.lua".split(),
    "farms": "Lua/Buildings/Farm.lua Lua/Buildings/FungalFarm.lua Lua/Crop.lua Lua/Units/Animals.lua".split(),
    "resources": "Lua/Resources.lua Lua/ResourceOverview.lua Lua/ResourceTracking.lua Lua/HasConsumption.lua Lua/Spoilage.lua Lua/Buildings/ResourceStockpile.lua Lua/Buildings/ResourceProduction.lua Lua/Buildings/StockpileController.lua Lua/Buildings/StorageDepot.lua Lua/Buildings/MultiResourceDepot.lua Lua/Buildings/MultiResourceCubeVisuals.lua Lua/Buildings/MixedPoolStockpile.lua".split(),
    "colonists": ["Lua/Units/Colonist.lua"],
    "parent": "Lua/Buildings/Dome.lua Lua/Buildings/Building.lua Lua/Colony.lua Lua/UpgradeUnlocks.lua Lua/Buildings/Community.lua".split(),
}
PROGRESS = set("Lua/TechTree.lua Lua/Tech.lua Lua/Research.lua Lua/Sequences/SA_Gameplay.lua Lua/MarsGameEffects.lua Lua/_GameUtils.lua Lua/PreGameMission.lua Lua/RandomMap/RandomMapGenerator.lua Lua/RandomMap/RandomMapGeneratorEdit.lua Lua/GameRules.lua Lua/ResupplyItems.lua Lua/Traits.lua Lua/MissionProfileDlg.lua".split())
NOROWS = """CommonLua/Libs/Research/ClassDefs/ClassDef-Conditions.generated.lua
CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua
CommonLua/Libs/Research/Data/ClassDef-Conditions.lua
CommonLua/Libs/Research/Data/ClassDef-Effects.lua
CommonLua/Libs/Research/Data/ClassDef-PresetDefs.lua
Lua/AmbientLife/VisitFastFoodRestaurant.lua
Lua/AmbientLife/VisitFoodStand.lua
Lua/AmbientLife/VisitGourmetRestaurant.lua
Lua/AmbientLife/WorkFarmInsect.lua
Lua/AmbientLife/WorkFarmSmall.lua
Lua/AmbientLife/WorkFoodStand.lua
Lua/Buildings/Diner.lua
Lua/Buildings/RocketTrade.lua
Lua/Config/config.lua
Lua/Refabable.lua
Lua/UI/CreditsData.lua
Lua/_EntityData.generated.lua
Lua/__const.lua""".splitlines()
CALLS_READ = {"C00579", "C00731", "C00732", "C00733", "C00734", "C00735"}
CALLS_LINE_ONLY = {"C00595", "C00596", "C00597", "C03968"}
GENERATED_PREFIXES = ("Data/", "Lua/BuildingTemplate/", "Lua/XDef/", "Lua/ClassDefs/")
FIELDS = "surface key file subject span107 span110 original_link owner read_status reader evidence fr".split()


def read(name):
    with (REPORTS / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader((line for line in f if not line.startswith("#")), delimiter="\t"))


def build():
    receipt = []
    groups = {file: group for group, files in GROUPS.items() for file in files}
    for row in read("INVENTORY.tagged.tsv"):
        if row["link"] != "03":
            continue
        file = row["file"]
        group = groups.get(file) if row["bucket"] == "hand" else None
        if group:
            owner, status = "03", "full-present-spans"
            reader = {"food": "food_seam", "farms": "farm_seam", "resources": "resource_seam", "colonists": "food_seam", "parent": "parent"}[group]
            evidence = "SEAM_REPORT.md#" + group
        else:
            owner = "03b" if row["bucket"] != "hand" else "03c" if file.startswith("Lua/Factions/") or file in PROGRESS else "03d"
            status, reader, evidence = "pending", "", "SEAM_REPORT.md#remaining"
        receipt.append(dict(zip(FIELDS, ["INVENTORY", row["rid"], file, row["function"], row["span107"], row["span110"], "03", owner, status, reader, evidence, row["fr"]])))
    for row in read("PRESETS.tagged.tsv"):
        if row["link"] == "03":
            receipt.append(dict(zip(FIELDS, ["PRESETS", row["prid"], row["file"], "|".join(row[k] for k in ("class", "id", "key")), "", "", "03", "03b", "pending", "", "SEAM_REPORT.md#remaining", row["fr"]])))
    for row in read("CALLERS.tagged.tsv"):
        if row["caller_link"] != "03":
            continue
        file, key = row["call_file"], row["cid"]
        owner = "03" if key in CALLS_READ else "03b" if file.startswith(GENERATED_PREFIXES) else "03c" if file.startswith("Lua/Factions/") else "03d"
        status = "caller-and-contract-read" if key in CALLS_READ else "line-checked-body-pending" if key in CALLS_LINE_ONLY else "pending"
        receipt.append(dict(zip(FIELDS, ["CALLERS", key, file, row["callee_file"] + ":" + row["callee_function"], row["call_line107"], row["call_line110"], "03", owner, status, "parent/chasers" if status != "pending" else "", "SEAM_REPORT.md#callers", ""])))
    available = {r["path"] for r in read("NOROWS.tsv")}
    assert set(NOROWS) <= available, "NOROWS snapshot no longer matches source ledger"
    for file in NOROWS:
        receipt.append(dict(zip(FIELDS, ["NOROWS", file, file, "whole-file-text-diff", "", "", "03", "03d", "pending", "", "SEAM_REPORT.md#remaining", ""])))
    counts = Counter((r["surface"], r["owner"]) for r in receipt)
    assert counts == {("INVENTORY", "03"): 396, ("INVENTORY", "03b"): 360, ("INVENTORY", "03c"): 284, ("INVENTORY", "03d"): 249, ("PRESETS", "03b"): 1618, ("CALLERS", "03"): 6, ("CALLERS", "03b"): 6, ("CALLERS", "03c"): 2, ("CALLERS", "03d"): 16, ("NOROWS", "03d"): 18}, counts
    assert len(receipt) == len({(r["surface"], r["key"]) for r in receipt}) == 2955
    out = io.StringIO(newline="")
    out.write("# Link 03 close-out snapshot 2026-09-10; read attestations, not automated clearance.\n")
    # Keep the always-present evidence pointer last; an empty FR field should
    # remain a real empty TSV field without looking like trailing whitespace.
    writer = csv.DictWriter(out, fieldnames=FIELDS[:-2] + ["fr", "evidence"], delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(receipt)
    return out.getvalue(), counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the dated receipt; default verifies it")
    args = parser.parse_args()
    content, counts = build()
    if args.write:
        OUTPUT.write_text(content, encoding="utf-8", newline="")
    elif not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
        raise SystemExit("FAIL: SEAM_COVERAGE.tsv differs from the dated receipt")
    print("PASS: 2955 unique items, exact input coverage and disjoint continuation ownership")
    for (surface, owner), count in sorted(counts.items()):
        print(f"  {owner} {surface}: {count}")


if __name__ == "__main__":
    main()
