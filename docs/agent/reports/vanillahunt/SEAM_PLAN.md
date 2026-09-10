# 03 seam reading plan — 2026-09-10

Parent: Codex `/root`; read-only chasers: `food_seam`, `farm_seam`, `resource_seam`.
The parent owns all writes, candidate verdicts, filing, and handoffs.

## Live todo (one commit-and-verify unit per item)

- [x] Record the measured split and source pins; chain gates GREEN, both instrument selftests PASS.
- [ ] IN PROGRESS: Read and adjudicate the 396-row core-food slice, execute suitable falsifiers,
  file surviving candidates, record explicit read coverage and continuation ownership; gates and commit.
- [ ] Write full continuation inboxes and 04/99 outboxes, update manifest and state,
  consume 03, run chain gates, commit and push.

## Pin and split

MEASURED: start HEAD `0f9f006`, clean worktree, `git pull` already up to date;
installed `A:/SteamLibrary/steamapps/appmanifest_3215050.acf` buildid `24995074`.
MEASURED: manifest file counts/digests match the chain: 1.0.7 4,448 /
`09d95e3448573dc378fa0bed5fc987fead3aafb70bf2ecf6a2cddef3f1ff9921`;
1.1.0 4,717 / `a4577da25cb3fe8586bb7388b9b557d3dfd343938e453382e65d066f1945b3b2`.
This check hashes manifests, not a fresh rehash of every source file.

MEASURED: link `03` has 1,289 INVENTORY rows (929 hand, 360 generated),
1,618 PRESETS rows (49 registries), 30 CALLERS rows; 18 NOROWS files are assigned
in TRIAGE §3. The prompt's approximately 400-row stop condition is exceeded.
The current slice is 396 hand rows, by whole files, including added/removed bodies.
All 360 generated INVENTORY rows and 1,618 PRESETS rows go to `03b_SEAM_PRESETS.md`;
the remaining 533 hand rows and 18 NOROWS text items receive a full Lua continuation.
Rows consulted as callers outside the current slice remain assigned to their owner;
incidental reads are recorded separately and do not imply full coverage.

| reader | rows | exact files (under archived Src) |
|---|---:|---|
| food_seam | 127 | Lua/Buildings/FoodServiceBuilding.lua; Lua/Meal.lua; Lua/Buildings/RecipeProductionBuilding.lua |
| farm_seam | 105 | Lua/Buildings/Farm.lua; Lua/Buildings/FungalFarm.lua; Lua/Crop.lua; Lua/Units/Animals.lua |
| resource_seam | 91 | Lua/Resources.lua; Lua/ResourceOverview.lua; Lua/ResourceTracking.lua; Lua/HasConsumption.lua; Lua/Spoilage.lua; Lua/Buildings/ResourceStockpile.lua; Lua/Buildings/ResourceProduction.lua; Lua/Buildings/StockpileController.lua; Lua/Buildings/StorageDepot.lua; Lua/Buildings/MultiResourceDepot.lua; Lua/Buildings/MultiResourceCubeVisuals.lua; Lua/Buildings/MixedPoolStockpile.lua |
| parent | 73 | Lua/Units/Colonist.lua; Lua/Buildings/Dome.lua; Lua/Buildings/Building.lua; Lua/Colony.lua; Lua/UpgradeUnlocks.lua; Lua/Buildings/Community.lua (no tagged ConstructionSite row exists) |

The chasers return row ids, both-tree locations, actual changes, reachability,
falsifiers, non-owner dependency evidence and hard tells. Shared evidence may be
named once and referenced by row; unresolved rows must be explicit. The parent
checks their claims against the primary trees. No game launch or module change.

## Limits inherited from the chain

Assets absent from Src, native engine behavior, timing/UI/progression and console
behavior cannot be settled here. EF-085 proves 1.1.0 packed bytes match Src, not
execution. The old DLC archive is incomplete and excluded. Preset C consumers,
anonymous functions and dynamically dispatched unchanged callers can escape the
instruments. No report closes FR-1/2/3 without the required runtime witness.
