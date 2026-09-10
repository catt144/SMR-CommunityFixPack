# vanillahunt 03b — food/resource/UI preset reader report

Date: 2026-09-10  
Reader: `/root/03b_food_presets` (read-only subagent)  
Source pin: `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src` → `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`; installed manifest was re-read at buildid `24995074` before this read.  
Scope: `PRESETS.tagged.tsv` rows with `link == 03` and class in the 15-class assignment. No repository, TSV, source-tree, or game-file write; no game launch or runtime probe.

## Receipt and result boundary

- Queue count: **560**, matching the expected 560.
- Unique PRIDs: **560**. Duplicate PRIDs: **0**. Missing keys from the filtered queue: **0**.
- Class counts: Achievement 1; AmbientLife 5; Animal 26; BugReportTag 1; BuildingTemplate 22; BuildMenuSubcategory 7; CargoResource 3; CropPreset 153; ParticleSystemPreset 4; Resource 7; ResourcePreset 181; Trigger 1; TutorialStep 1; Vegetation 13; XDef 135.
- Complete: **all 560 exact rows**. Not reached: **none of the assigned rows**. Hunk-only: **none**; added bodies were read in full and matched to their old absence/old behavior route. Native rendering remains unmeasured, as called out below.
- The four FR-1(c) ParticleSystemPreset rows `P09388,P09389,P09392,P09397` were read first.
- This is a reader report, not a defect verdict. No surviving FIX_POLICY §4 hard tell was established in this queue. One bounded UI PERF smell and several conditional DLC handoffs are recorded for parent re-derivation.

## Malformed/generated-row drift

1. **ResourcePreset identity failure — all 181 rows.** `Data/ResourcePreset.lua` serializes identity as the pair form `'Id', "…"`; `presetdiff.py` assigned synthetic ordinal ids such as `Data/ResourcePreset.lua#29`. Insertions then shifted positional paths. Only 14 real preset bodies changed; the queue's 109 `REINDEX-SWAP` ResourcePreset rows are positional artifacts, not 109 independent semantic swaps. The real bodies and the unchanged reader were traced below.
2. **BuildingTemplate identity failure — 20 of 22 rows.** Old editor files use `'Id', "Diner"` while new files use `id = "Diner"`. The tool emitted ten false removed+added pairs. They are ten matched presets, not ten removals plus ten additions. The two genuine additions are `UniversalFarmPlantStorageDepot` and `UniversalMeatStorageDepot`.
3. **Id-less XDef positional artifacts — six rows.** `P27624,P27635` (GameShortcuts) and `P36405,P36406,P36439,P36441` (ipBuilding) are `REINDEX-SWAP` effects from inserted/reordered nodes. Their full old/new templates and generated twins were read; the apparent old/new node pairing is not a semantic assignment.
4. Prompt path quick correction: `SEAM_PRESETS_PLAN.md` is under `docs/agent/reports/vanillahunt/`, not beside the prompt. It was read at the actual path.
5. Incidental fence drift: a name-only `rg` found Norman copies of `UniversalFarmPlantStorageDepot` and `UniversalMeatStorageDepot`, plus DLC name hits for the five added AmbientLife programs. No DLC function body was opened and those hits were not counted as coverage.

## FR-1(c): ParticleSystemPreset — 4 rows

Keys: `P09388,P09389,P09392,P09397`.

- File/preset/function/class and locations: `Data/ParticleSystemPreset/HydroponicFarm_Shower.lua`, full old body lines 3–306 and new body lines 3–304; `P09392` old/new element `[5]` lines 118/116, `P09388` element `[14]` lines 211/209, `P09389` element `[18]` lines 235/233. `SmallFarm_Shower` is a full added body at new `Data/ParticleSystemPreset/SmallFarm_Shower.lua:3–296`; no old file/body. Class is ParticleSystemPreset.
- Actual change: Hydro shower `fade_in_alpha` values 160→100, 10→15, and 200→50. A separate 294-line SmallFarm shower definition was added.
- Definition ↔ reader/twin: old/new `Data/FXPreset/ActionFXParticles.lua:582/557` selects `HydroponicFarm_Shower`; new line 574 selects `SmallFarm_Shower`. Old/new `Lua/Buildings/Farm.lua:762/997` calls `PlayFX("FarmWater","start",sprinkler)` (and end at 765/1000). `ParticleBehaviorFadeInOut` property metadata is in `CommonLua/Classes/Particles/ParticleVisual.lua:146–163` in both trees. There is no Lua-rendered generated twin; the terminal renderer/asset resolution is native.
- Reach/player action: **R2** for the Hydro route after constructing and operating a farm with the matching actor/FX; the SmallFarm route is **U/R2 conditional** because the base ActionFX definition exists but no non-DLC SmallFarm actor was established.
- Falsifier: run the same working farm/actor in both builds and compare the water effect alpha envelope and whether SmallFarm resolves/spawns its named particle asset. Source cannot falsify native render timing or asset lookup.
- Seam/non-owner: the Hydro definition, ActionFX record, and farm call are base and can affect non-owners. SmallFarm has no proved non-owner caller; a name in base ActionFX is not itself a DLC dependency or a non-owner reach proof.
- Hard tell / SMELL / PERF: **none**. Fixed-size particle definitions add no Lua periodic loop. FR-1 asset/render behavior remains unmeasured and is not closed by this read.

## Animal — 26 rows

Keys: `P00827–P00852` (all integers in the range).

- File/presets/class and lines: `Data/Animal.lua`; Chicken id old/new 17/22, Cow 36/46, Goat 58/73, Goose 77/97, Ostrich 97/122, Pig 117/147, RabbitPasture 138/173, Turkey 158/198. Full eight old/new bodies were read. Class: Animal; no per-preset generated twin.
- Actual change by body: the scalar `food` output is replaced by `OutputResources[1]={resource="Food",amount=…}`. Amounts are Chicken 200→100, Cow 30000→12500, Goat 4500→2250, Goose 2250→1150, Ostrich 10000→5000, Pig 10000→5000, Rabbit 600→200, Turkey 4000→2000. Rabbit also changes air and water consumption 600→400.
- Reader: old `Lua/Units/Animals.lua` consumes scalar `food`; new `Pasture:GetBreedOutputResources` at 714–725 supplies the list to production, UI, and `Msg("FoodProduced",…)` paths at 729–757, 811, 943–1047, and 1197–1210. The entire changed Animal bodies and relevant Pasture functions were read.
- Reach/player action: **R2**, build/operate the corresponding ranch/pasture and complete a breeding/harvest cycle.
- Falsifier: for each animal, hold performance and cycle time constant and compare UI forecast, request/storage resource, actual produced amount, and `FoodProduced` argument to the preset list.
- Seam/non-owner: data and Pasture consumer are base. No named Norman class is required for the generic migration, though actual constructibility of every species/building can vary by content. This overlaps existing C56 support and must not be filed as a duplicate.
- Hard tell / SMELL / PERF: no new hard tell. The output loop is bounded by the current one-entry lists. The large balance changes are not a defect tell by themselves.

## CropPreset — 153 rows

Keys: every PRID `P02426–P02578`.

- File/presets/class and old/new id lines: `Data/CropPreset.lua`, class CropPreset. Algae 149/432; Corn 249/103; Cover Crops 337/209; Cure 285/126; Fruit Trees 303/149; Giant Corn 216/83; Giant Leaf Crops 74/372; Giant Potatoes 266/169; Giant Rice 30/271; Giant Wheat 199/42; Giant Wheat Grass 134/313; Kelp 167/455; Leaf Crops 88/391; Microgreens 102/353; Mystery9_GanymedeRice 16/250; Potatoes 320/189; Quinoa 183/21; Rice 44/292; SeedCrops 373/476; SeedCropsHydro 391/498; Soybeans 354/229; Vegetables 118/412; Wheat 232/63; Wheat Grass 60/334. Every complete old/new body was read.
- Actual change: all 24 bodies migrate `FoodOutput`/`ResourceType` to one-entry `OutputResources`. Descriptions gain explicit resource icons. Conventional crops change `FarmClass` from `FarmConventional` to `Farm`; outputs, sort keys, and several durations/soil effects are rebalanced. Removed conventional 2.5-sol fields fall to the new CropPreset class defaults `InitialGrowthTime=2880000` and `GrowthTime=2880000` (`Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:727–790`), rather than becoming nil. Notable values: Corn 70000→84000; Cover Crops 12000 Food→48000 Seeds and SoilEffect 40→20; Fruit Trees 88000→106000 and 4→3.2 sols; Giant Corn 110000→132000; Giant Potatoes 80000→96000; Potatoes 55000→66000; SeedCrops 80000→96000 Seeds; Rice 15000→8000; SeedCropsHydro 12000→7000 Seeds; Wheat 17000→20000 and 1→0.8 sol; Quinoa 22000→26000 and 1→0.8 sol.
- Reader/twin: new `Lua/Crop.lua:GetCropOutputResources` at 149–188 merges preset output and augmentation lists, capped by `ResourceProducer.max_resources_produced`. Direct UI callers are `Lua/Buildings/Farm.lua:17,28`; farm production/storage/UI callers include lines 256, 497, and 739 onward. Old `Lua/Buildings/Farm.lua:293–307,425,823,857–861` reads `ResourceType`/`FoodOutput`. CropPreset's generated **class definition**, not a data twin, was read in both trees.
- Reach/player action: **R2**, select each crop in the applicable farm and complete its growth/harvest; sort/description changes are immediately visible in the crop selector.
- Falsifier: for each listed crop, compare selector order/text, duration, forecast, selected producer slots, storage request type, actual harvest, and emitted production message. Multi-output augmentation needs a separate bounded test; existing C59 already owns that question.
- Seam/non-owner: base CropPresets and base Farm/Hydroponic readers execute for non-owners. DLC-defined extra crops are outside this row set and were not opened. `FungalFarm` and `FungalFarmBase` were not conflated.
- Hard tell / SMELL / PERF: none new. One-entry preset lists and a producer cap bound the list work. No periodic cadence was added by these data bodies.

## Resource — 7 rows

Keys: `P11032,P11033,P11035,P11036,P11037,P11038,P11039`.

- File/preset/class/lines: Food in `Data/Resource.lua`, id old/new lines 106/138, full body read; class Resource.
- Actual change: removes `--Will be removed in Norman`; replaces description with explicit production/import/perishability copy; moves Food from `OtherResources` to `BasicResources`; adds medium icon; adds `Export` tag alongside `Edible`; replaces text/UI icons with import artwork.
- Reader: resource preset preprocessing expands group membership into `LeafResourceIds`/`GroupResourceIds` in the base resources library; base storage, overview, resupply, export, and infobar consumers use those tables and `Resources.Food`. The related spoilage implementation was already fully traced in SEAM_REPORT/C58; this row does not independently prove runtime decay results.
- Reach/player action: **R1** for a normal colony's overview/infobar/group selection and resupply/export presentation; decay consequences are R2 over a Sol.
- Falsifier: on a non-owner colony, inspect Basic Resources grouping and Food icons/export availability, then compare the description's stated decay percentage with measured storage decay under controlled exclusions.
- Seam/non-owner: fully base-shipped and reachable without Norman. Removing the old comment does not make Norman a runtime requirement.
- Hard tell / SMELL / PERF: none; the description mirrors the new intended decay feature but is not a proof of native/runtime outcome.

## Vegetation — 13 rows

Keys: `P23922,P23923,P23924,P23928,P23929,P23931,P23935,P23938,P23939,P23941,P23946,P23947,P23949`.

- File/presets/class/lines: `Data/Vegetation.lua`, full bodies read. Herbs old/new id 238/258; Potato 271/296; Rapeseed 305/334; Spinach 336/370; Wheat 369/407. Class Vegetation.
- Actual change: legacy `output_resource`/`output_amount` fields become `OutputResources` lists and descriptions are rewritten. Full-body companion changes: Herbs 125 Food and placement 100→50; Potato 7000→500 Food and placement 600→100; Rapeseed remains 500 Seeds; Spinach 4000→250 Food and placement 200→50; Wheat 12000→750 Food and placement 400→150. Other non-food vegetation bodies in the same file also migrate to list outputs but are outside the exact row queue.
- Reader: new `Lua/Vegetation.lua:GetVegetationOutputResources` at 1794–1804, callers at 1048, 1408, 1904, 2073; `Lua/Buildings/TerraformingBuilding.lua` consumes the list at 403, 422, 614, 625, 722, 738, 976, 1023, 1061. Old readers use scalar output fields.
- Reach/player action: **R2**, unlock/plant/harvest the vegetation via Open Farm/terraforming UI.
- Falsifier: compare controlled plots for placement cost, displayed resource/icon, yield, and drone-delivered amount; verify Wheat's “most Food” claim against all eligible vegetation crops under equal modifiers.
- Seam/non-owner: readers and preset file are base, but constructibility depends on the Green Planet/terraforming feature route; no Norman dependency was inferred.
- Hard tell / SMELL / PERF: no hard tell. Fixed one-entry lists; no added periodic loop.

## CargoResource — 3 rows

Keys: `P01956,P01957,P01958`.

- File/preset/class/lines: Food in `Data/Cargo.lua`, id old/new lines 226/214, full body read; class CargoResource.
- Actual change: SortKey 3003000→4003600, price 4,000,000→10,000,000, and verifier added: `return GameState.gameplay`.
- Reader: old/new `Lua/ResupplyItems.lua:19,123–129` reads price, verifier, and SortKey; a parallel Building cargo path applies the verifier at `Lua/Buildings/Building.lua:109–110`.
- Reach/player action: **R1**. Food is hidden/locked from first-rocket payload before `GameState.gameplay`, then eligible in an in-game resupply screen at the higher price.
- Falsifier: compare first payload and post-landing resupply lists, ordering and displayed charge, with sufficient funding.
- Seam/non-owner: base cargo record and consumers, no DLC requirement.
- Hard tell / SMELL / PERF: none; gating and repricing are coherent policy changes absent contrary intent evidence.

## BuildMenuSubcategory — 7 rows

Keys: `P01311,P01312,P01313,P01314,P01315,P01322,P01330`.

- File/presets/class/lines: `Data/BuildMenuSubcategory.lua`; Farms old/new id line 291/259 plus full added FastFood, FoodDepots, FoodPlants, FoodStorages (new 541–550), Restaurants, and SpecialtyFarms bodies. Class BuildMenuSubcategory.
- Actual change: Farms build_pos 10→13; six food subcategories are added with parent categories, icons, names and sort positions.
- Reader: `Lua/X/BuildMenu.lua:UIItemMenu` at 1398 onward collects subcategories only when at least one child passes `UIGetBuildingPrerequisites` (662–790); sorting reads build positions. No generated twin exists for these data presets.
- Reach/player action: **R1/R2** on opening relevant construction categories; empty subcategories are suppressed.
- Falsifier: open each parent category on owner and non-owner installs and enumerate only nonempty child subcategories and order.
- Seam/non-owner: the registries and reader are base. DLC-only children do not become reachable merely because a base subcategory name exists. The two apparent base food storage helpers are `Obsolete=true`; `ForEachPreset` excludes obsolete presets (`CommonLua/Preset.lua:1763–1774`), falsifying the apparent non-owner build-menu leak.
- Hard tell / SMELL / PERF: none.

## BuildingTemplate — 22 rows

Keys: false-pair old rows `P01396,P01417,P01424,P01425,P01439,P01484,P01524,P01578,P01579,P01599`; corresponding new rows `P01653,P01674,P01681,P01682,P01696,P01741,P01781,P01836,P01837,P01857`; genuine additions `P01889,P01893`.

- Files/presets/class: full old/new `Data/BuildingTemplate/<id>.lua` and `Lua/BuildingTemplate/<id>.generated.lua` bodies were read for Diner, Farm, FungalFarm, FungalFarm_Asteroid, HydroponicFarm, MechanizedDepotFood, OpenFarm, ShopsFood, ShopsFood_Small, StorageFood. The generated definitions prove the ten parser pairs are the same runtime class ids. Class BuildingTemplate.
- Actual matched-body changes: Diner/Grocer/Small Grocer migrate scalar Food consumption to `FoodBuilding` storage/meal fields and new food-service categories; costs/capacity/visit/work fields change. Farm/Hydroponic/Fungal/OpenFarm storage, cost, environment, work and category fields are rebalanced; Farm gains three 600k producer slots and `crop_spot`; FungalFarm is explicitly disabled on Asteroid+Surface, while the distinct FungalFarm_Asteroid is disabled on Surface+Underground. Food depots receive new category/icon/desired-amount metadata. These are changes, not removals/additions.
- Genuine additions: new full Data bodies `UniversalFarmPlantStorageDepot.lua:3–37` and `UniversalMeatStorageDepot.lua:3–37`, with generated twins `Lua/BuildingTemplate/...generated.lua:3–38`. Each is `Obsolete=true` in Data and therefore omitted by the runtime `ForEachPreset` table build; generated class metadata alone does not make it a build-menu entry.
- Reader/twin: `Lua/Buildings/Building.lua:2674–2686` constructs `BuildingTemplates`/`BuildingTemplatesPresets` from non-obsolete presets and generated `g_Classes`. `Lua/X/BuildMenu.lua:662–790,1398–1460` consumes the result. Food-specific runtime consumers are `Lua/Buildings/Farm.lua` and `Lua/Buildings/FoodServiceBuilding.lua`.
- Reach/player action: **R1/R2** for the ten active base templates via construction/operation. Genuine obsolete helpers are **R4** in base/non-owner runtime and exist for compatibility/DLC override, not normal menu reach.
- Falsifier: enumerate `BuildingTemplates` after ClassesBuilt on owner and non-owner states, confirm obsolete helper absence, then compare cost/category/environment/storage/meal behavior for each active class.
- Seam/non-owner: the ten active definitions are base and non-owner relevant. FungalFarm is not FungalFarmBase from DLC; LowGFungi's underground route is already documented upstream. No DLC interior was used to clear the active templates.
- Hard tell / SMELL / PERF: none newly established. The obsolete-filter check falsified the strongest apparent non-owner leak.

## ResourcePreset — 181 malformed rows, 14 real bodies

Keys: all ResourcePreset PRIDs in the exact appendix. Synthetic ordinal-to-real-body mapping and actual changes:

- `#1` AsteroidBType_ExoticMinerals_Average, id old/new 4/4: Subs1 volume 300–800→100–200; adds Subs2 count 1, volume 200–600.
- `#3` AsteroidCType_Metals_Average, 33/35: Subs1 volume 300–800→200–400; adds Subs2 count 1, volume 400–800.
- `#6` AsteroidDType_ExoticMinerals_High, 74/78: Subs1 count 3–5→3 and volume 200–800→200–400; adds Subs2 count 1, volume 400–800.
- `#9` AsteroidMType_Metals_High, 111/117: Subs1 count 4→3 and volume 200–800→300–500.
- `#10` AsteroidMType_RareMetals_Average, 125/131: Subs1 volume 300–600→200–400; adds Subs2 count 1, volume 300–600.
- `#13` AsteroidMystery_Metals_High, 163/171: Subs1 volume 30000–100000→1000–3000; adds Subs2 count 1, volume 2000–6000, and grade weights 0/0/0/0/100.
- `#14` AsteroidMystery_RareMetals_High, 179/194: Subs1 volume 20000–50000→800–2000; adds Subs2 count 1, volume 1500–3000, and grade weights 0/0/0/0/100.
- `#16` AsteroidPType_ExoticMinerals_High, 202/224: Subs1 volume 300–800→300–600; adds Subs2 count 1, volume 500–1000.
- `#19` AsteroidSType_ExoticMinerals_Average, 234/258: Subs1 volume 100–500→100–200; adds Subs2 count 1, volume 200–400.
- `#29` Metals_High, 484/510: adds PrefabSizeDistrib 35–65; SmallClustersCount 12–16→5–10.
- `#30` Metals_Low, 509/536: adds PrefabSizeDistrib 70–95; SmallClustersCount 10–14→12–17; BigClustersCount 2–3→2–4.
- `#32` Metals_VeryHigh, 561/589: adds PrefabSizeDistrib 10–40; BigClusterDeposits 8–12→6–10; SmallClustersCount 12–18→1–5; BigClustersCount 3–6→4–6.
- `#33` Metals_VeryLow, 586/615: adds PrefabSizeDistrib 90–100; SmallClusterDeposits 1–3→1–2; BigClusterDeposits 5–10→6–10; SmallClustersCount 10–14→38–48; removes BigClustersCount (class default `range00`).
- `#41` Polymers_VeryLow, 689/718: adds PrefabSizeDistrib 100–100; removes SmallClusterDeposits; BigClusterDeposits 4–8→1–2; SmallClustersCount 1–3 removed; adds BigClustersCount 0–9 and ClusterSpacing 2.

Reader/class: complete `Data/ResourcePreset.lua` bodies were read. `Lua/RandomMap/ResourcePreset.lua` is unchanged in both trees and defines defaults, including missing range fields as `range00`. `Lua/RandomMap/RandomMapResourceInfo.lua:38–154` reads the selected preset: surface distributions/counts at 70–109, terrain at 111–133, then `Subs1`/`Subs2` count, volume and weights at 135–154; `const.DepositDeepestLayer` is 2. There is no per-preset generated twin (`StoreAsTable=false`); the Data objects are the registry consumed by this reader.

- Reach/player action: **R1** for selecting/creating a new Mars map with Metals_High/Low/VeryHigh/VeryLow or Polymers_VeryLow; **R2 conditional** for asteroid preset generation.
- Falsifier: deterministic same-seed map generation with each explicit ResourcePreset, then count cluster sizes, surface deposits, volumes, layers and grades. Random/native placement behavior remains unmeasured.
- Seam/non-owner: Mars resource presets/readers are base and non-owner relevant. Asteroid presets are base-shipped but their playable route depends on B&B content; no Norman body was opened or required.
- Hard tell / SMELL / PERF: no hard tell. Metals_VeryLow's 38–48 small clusters is a large intentional-looking redistribution, not proof of harm. Work is generation-time and bounded by preset counts; no periodic gameplay loop.

## AmbientLife — 5 rows

Keys: `P00821,P00822,P00823,P00825,P00826`.

- Files/presets/class: full added Data bodies in `Data/AmbientLife/{VisitFastFoodRestaurant,VisitFoodStand,VisitGourmetRestaurant,WorkFarmSmall,WorkFoodStand}.lua` and full generated runtime twins in `Lua/AmbientLife/<same>.lua`; class AmbientLife. None exists in old tree.
- Actual change: five new visit/work animation programs. `WorkFarmSmall` selects Workcrop/Worktablet and creates/attaches a temporary Tablet on the tablet branch; visit programs select matching slots and fall back to holder behavior.
- Reader: old/new generic `Lua/Units/Colonist.lua:GetVisitPrg` at 2167/2774–2779 resolves `PrgAmbientLife["Work"..(prg_class or class)]` or Visit; `Lua/Buildings/Service.lua:277` calls `unit:PlayPrg(GetVisitPrg(self),…)`.
- Reach/player action: **U/R2 conditional**. All five names correspond to content not proved constructible in the non-owner base route. The generic base reader is present, but a registry name alone does not prove a caller.
- Falsifier: on an owning install, visit/work each named building, verify spot selection/fallback and cleanup on restart; separately prove whether any base non-owner building's class/prg_class resolves one of these names.
- Seam/non-owner: absent a matching base class/prg_class, no non-owner execution was established. DLC interior is deferred: TAKEABLE WHEN dlccheck reads the named building class and its `prg_class` assignment.
- Hard tell / SMELL / PERF: no hard tell. Conditional smell only: generated WorkFarmSmall creates Tablet on `Maps[1]`; test only if dlccheck proves FarmSmall can operate on another map. Programs are per-visit, bounded, and clean temporary objects with a destructor.

## Achievement, BugReportTag, Trigger, TutorialStep — 4 rows

### Achievement `P00010`

- PoliticalAnimal in `Data/Achievement.lua`, id old/new 854/846; class Achievement. Actual change is only `TODO=set("Review")` removed.
- Runtime achievement conditions/messages are otherwise unchanged; TODO is editor metadata and has no runtime reader effect. Reach **R4**. Falsifier: inspect serialized preset/runtime property table for TODO use; none was found. Base/non-owner neutral. Hard tell/PERF: none.

### BugReportTag `P01305`

- Added Food body at `Data/BugReportTag.lua:16–22`; class BugReportTag. It enrolls a developer bug-report classification only.
- Reach **R4** in player gameplay (developer/report UI only). Falsifier: open the developer bug-report tag selector. Base-shipped but no gameplay effect. Hard tell/PERF: none.

### Trigger `P23817`

- Added full `FoodServiceMealServed` body at `Data/Trigger.lua:331–345`; class Trigger. It registers on the same-named message, validates the optional Colonist, and exposes building/colonist params.
- Producer/reader: new `Lua/Buildings/FoodServiceBuilding.lua:805` emits `Msg("FoodServiceMealServed",self,colonist)` after a served meal. `CommonLua/Libs/TriggersAndEvents/Triggers.lua:68–113,128–133` evaluates the condition and registers the message reaction; event selection is through `EventsByTrigger`.
- Reach **R2** for trigger activation after a valid colonist eats; downstream player effect is **U** unless an event bound to this trigger is separately identified. Falsifier: instrument message/trigger activation with valid vs nil/invalid colonist, then enumerate bound events. Base/non-owner meal service route exists. Hard tell/PERF: none; one dispatch per served meal.

### TutorialStep `P23881`

- Added full Step08_Food body at new `Data/TutorialStep.lua:3088–3145`; no old `Data/TutorialStep.lua` body/file for this id. Class TutorialStep.
- Actual change: tutorial popup; disables tutorial resupply toggle; sequential placement tasks for HydroponicFarm, ShopsFood_Small, StorageFood within ten units of the first Dome; final wait checks the three colony labels.
- Reader: `CommonLua/Libs/Tutorial/Tutorials.lua:88,121,178` and `Lua/TutorialsNew.lua:652` select TutorialSteps; `ConstructBuildingTask` is defined/evaluated at `Lua/TutorialsNew.lua:1174–1368`.
- Reach **R1/R2 tutorial-only**. Falsifier: play the Colonists tutorial step, violate each distance rule, then construct the three requested buildings and confirm sequential completion. All named buildings are base; no DLC requirement. Hard tell/PERF: none.

## XDef — 135 rows

All 42 affected full Data/XDef files and both present generated twins were read. Three XDefs are genuine additions and therefore have only new Data/generated bodies: RolloverCropItem, sectionFoodProducerStoredResources, sectionFoodService. Runtime uses the generated `Lua/XDef/*.generated.lua` classes; Data bodies are editor source. `CommonLua/X/XTemplate.lua:10–111,520–564,1503–1537` resolves templates, while generated section classes are directly instantiated from `Lua/XDef/ipBuilding.generated.lua:48,62,75`. No extra semantic delta was found between a Data body and its generated twin.

Grouped row ledger and actual change:

- `CommandCenterBuildingOverviewRow` `P24028`: added HeavyWorkload overtime row update. `CommandCenterBuildingsOverview` `P24046`: Consumption heading capitalization. `CommandCenterCategories` `P24055`: Food value switches `<food>` to generic `<resource(GetAvailable)>`. Reach R1 in Command Center; base/non-owner. Falsifier: open rows with HeavyWorkload off/on and compare amount formatting. No tell/PERF.
- `CommandCenterDomeOverviewRow` `P25028` and `CommandCenterDomesOverview` `P25258`: old inline birth-policy control/Policies column removed as the dome controls were consolidated. `sectionDome` `P36944,P36945,P37015,P37021` removes the duplicated second definition and updates current-status layout in the surviving definition. `sectionMicroGHabitat` `P37072` mirrors status layout. Reach R1/R2 UI; birth control gated by ActiveLaws. Non-owner base. Falsifier: open Dome/CCC under all three birth states and quarantine states. No tell/PERF.
- `CommandCenterPowerGridsOverview` `P25322` and row `P25333,P25362,P25365,P25371,P25374`: headings/ids are reorganized to Name, Balance, Production, Consumption, Stored; the root update computes all five values, formats sign/red deficit, storage/capacity, and warning. Reach R1. Falsifier: grid with negative/zero/positive balance and small/large capacity. No tell/PERF.
- `GameCheatShortcuts` `P26581,P26587,P26593,P26598,P26599,P26601,P27394`: policy/tech developer cheats removed. Reach R4/dev only. `GameShortcuts` `P27624,P27635` are positional artifacts around inserted Build Menu shortcut, not Toggle/Reset semantic replacements. Falsifier: enumerate ActionIds/bindings in full templates. No player hard tell.
- `HUDMiddle` `P28057`: resupply rollover appends `<ResupplyButtonInfo()>`. `PayloadRollover` `P31550` changes title style. `PGMissionPayloadRemastered` `P31268,P31269,P31272` adds tutorial rollovers/uppercase destinations and includes placed prefabs in “available” counts. `ResupplyCategories` `P34366`: Cargo Rocket rollover title. Reach R1 in payload/resupply. Non-owner base. Falsifier: first payload vs in-game resupply and prefab count with placed+unplaced prefabs. No tell/PERF.
- `InfobarUI` `P28530,P28538,P28539,P28542,P28553,P28575`: adds Food cycling/rollover/text using `Resources.Food.visible`, plus ingredient submenu gated by `next(LeafResourceIds.MealIngredients)`. EF-005 covers engine `next(nil)` behavior; normal non-owner Food does not populate ingredient leaves, so submenu stays hidden. Reach R1. Falsifier: owner/non-owner infobar, visible false/true, empty/populated ingredient group. No tell/PERF.
- `ipBuilding` `P36345,P36354,P36405,P36406,P36439,P36441,P36559,P36560,P36561,P36570`: inserts food stored-resource/service sections and crop-selector visibility, plus WaterGrid/Consumption node reorder; removes obsolete decommission disabled text. Four middle rows are positional artifacts. Reach R1/R2 on infopanels. Falsifier: Farm/Pasture/FoodBuilding/water/life-support/construction contexts with and without crop selector. Non-owner base sections guard by class/condition. No hard tell.
- Law/policy UI: `LawDevelopCard` `P30042,P30043,P30078,P30114,P30132,P30133,P30145,P30171,P30172,P30183,P30188,P30204,P30217`; `LawEntry` `P30224,P30225,P30227,P30234,P30240,P30241,P30244`; `LawInDevelopmentCard` `P30245,P30250,P30251`; `LawVoteDropdownList` `P30252`; `LawVotingBar` `P30254`; `LawVotingCard` `P30453,P30454,P30459,P30460,P30461,P30462,P30463,P30464,P30465,P30466,P30467,P30468`; `PolicyEntry` `P32611`; `PolicyEntryActive` `P32613,P32614,P32615,P32616`; `PoliticsDlg` `P32941,P33047,P33055,P33240,P33241,P33250,P33572,P33637,P33808,P33809,P34019,P34141,P34273,P34325,P34328`. Actual change is the legislature redesign: queued preparation, preparing state/timers, affordability/upkeep/cooldown feedback, direct Begin/Enact/Revoke methods, voting/action layout, agenda relocation, and UI lifecycle cleanup. Reach R1/R2 after opening Politics and preparing/voting. Base code executes only when the feature state supplies `g_Legislature`; no named DLC function was needed for these template readers. Falsifier: single-law and multi-law policies through locked, visible, preparing, prepared, active, unaffordable, cooldown and target-selection states on mouse/gamepad. The “Missing description” expression is correctly `~= ""` in actual Data/generated Lua (the TSV tokenizer dropped `~`); the apparent inversion is falsified. No hard tell/PERF established.
- `customMagneticFieldGenerator` `P36072`, `sectionBottomlessPitResearchCenter` `P36876`, `sectionResearchProject` `P37189`: research text becomes Tech Points/current production detail. `customSpaceElevator` `P36117` and `customUniversalRocket` `P36178`: cargo/export copy. Reach R1 UI when those buildings exist; some building reach is content-conditional. Falsifier: compare displayed totals with underlying context values. No tell/PERF.
- `RolloverCropItem` `P34794`: full new Data lines 3–197 and generated lines 3–205; specialized crop rollover with title, description, traits, text and enabled/disabled hints. `sectionCrop` `P36893–P36906` switches to that rollover, generic production text, hides conventional soil row for hydroponics, and removes scalar stored-resource line. Reach R1/R2 in farm crop selection. Base/non-owner. Falsifier: mouse/gamepad and enabled/disabled crop cards on conventional/hydroponic farms, including multi-output text. No tell/PERF.
- `sectionConsumption` `P36889,P36890`: section now hides when `UpdateUISectionConsumption` returns false and renames an id to recipe input. `sectionPasture` `P37159` removes scalar Stored Food line in favor of the new shared resource section. `sectionResourceProducer` `P37226` adds a short-circuit `g_Classes.ReplicatorBase` condition. Reach R1/R2; non-owner Replicator absence is guarded. Falsifier: contexts with/without consumption text and Pasture outputs. No tell/PERF.
- `sectionFoodProducerStoredResources` `P37068`: full new Data 3–27/generated 3–40. For FarmBase/Pasture it loops `GetUIStoredResourcesList()` and displays per-resource stored amounts. Reach R1/R2 base. Falsifier: one-, two-, and empty-output lists. No tell; bounded by output slots.
- `sectionFoodService` `P37069`: full new Data 3–78/generated 3–110. Shows base Food storage/service capacity; ingredient and menu sections are gated by data and `IsDlcAvailable("norman")`. `FoodBuilding:Init` initializes `serveable_ingredients`; base non-owner gets the core Food section and no Norman menu course calls. Reach R1/R2.
  - Falsifier: owner/non-owner Diner/Grocer, empty/populated ingredient sets, three/less/no available courses, enable toggles and context refresh.
  - Hard tell: none. **PERF smell:** each of three course rows calls `building:GetNowServingMenu()` on every context update; that function scans available ingredients and the building's Meal preset list. It is UI-only and bounded, and the source comment explicitly requests recomputation, so this is a smell to measure rather than a performance finding.
- `sectionVegetationPlant` `P37315,P37317,P37325,P37326`: adds crop production id/style and replaces Food-only output with `<GetHarvestText>` for generic resources. Reach R1/R2 Green Planet route. Falsifier: each vegetation output and empty range. No tell/PERF.
- `sectionWaterGrid` `P37343`: shows maximum water production only when greater than current. Reach R1. Falsifier: current=max and current<max. No tell/PERF.
- `sectionWorkshifts` `P37371` and `sectionWorkshiftsRow` `P37454`: overtime control moves to a max-workers + HeavyWorkload condition rather than disabling the row at layout. Reach R1/R2 with policy off/on and workplace/non-workplace contexts. Non-owner base. Falsifier: contexts with max_workers 0 and >0; policy off/on. No tell/PERF.

## Exact PRID appendix

This appendix is the duplicate/missing audit set used above.

- Achievement (1): `P00010`
- AmbientLife (5): `P00821,P00822,P00823,P00825,P00826`
- Animal (26): `P00827,P00828,P00829,P00830,P00831,P00832,P00833,P00834,P00835,P00836,P00837,P00838,P00839,P00840,P00841,P00842,P00843,P00844,P00845,P00846,P00847,P00848,P00849,P00850,P00851,P00852`
- BugReportTag (1): `P01305`
- BuildingTemplate (22): `P01396,P01417,P01424,P01425,P01439,P01484,P01524,P01578,P01579,P01599,P01653,P01674,P01681,P01682,P01696,P01741,P01781,P01836,P01837,P01857,P01889,P01893`
- BuildMenuSubcategory (7): `P01311,P01312,P01313,P01314,P01315,P01322,P01330`
- CargoResource (3): `P01956,P01957,P01958`
- CropPreset (153): every key `P02426–P02578`
- ParticleSystemPreset (4): `P09388,P09389,P09392,P09397`
- Resource (7): `P11032,P11033,P11035,P11036,P11037,P11038,P11039`
- ResourcePreset (181): `P11062,P11063,P11065,P11066,P11067,P11068,P11069,P11070,P11072,P11073,P11075,P11076,P11077,P11079,P11081,P11083,P11085,P11087,P11088,P11090,P11091,P11092,P11094,P11096,P11098,P11100,P11102,P11103,P11104,P11105,P11106,P11107,P11108,P11110,P11111,P11112,P11113,P11114,P11115,P11116,P11117,P11118,P11119,P11120,P11121,P11122,P11123,P11124,P11125,P11126,P11127,P11128,P11129,P11130,P11131,P11132,P11133,P11134,P11135,P11136,P11137,P11138,P11139,P11140,P11141,P11142,P11143,P11144,P11145,P11146,P11149,P11150,P11151,P11152,P11153,P11154,P11155,P11157,P11158,P11159,P11160,P11161,P11162,P11163,P11164,P11165,P11166,P11167,P11168,P11169,P11170,P11171,P11172,P11173,P11174,P11175,P11176,P11177,P11178,P11179,P11180,P11181,P11182,P11183,P11184,P11185,P11186,P11187,P11188,P11189,P11190,P11191,P11192,P11193,P11196,P11197,P11198,P11199,P11200,P11201,P11202,P11203,P11204,P11205,P11206,P11207,P11208,P11209,P11210,P11211,P11212,P11213,P11214,P11215,P11216,P11217,P11218,P11219,P11220,P11221,P11222,P11223,P11224,P11225,P11226,P11227,P11228,P11229,P11230,P11231,P11232,P11233,P11234,P11237,P11238,P11239,P11240,P11241,P11242,P11243,P11244,P11245,P11246,P11247,P11248,P11249,P11250,P11251,P11252,P11253,P11254,P11255,P11256,P11257,P11258,P11259,P11260,P11261,P11262,P11263,P11264`
- Trigger (1): `P23817`
- TutorialStep (1): `P23881`
- Vegetation (13): `P23922,P23923,P23924,P23928,P23929,P23931,P23935,P23938,P23939,P23941,P23946,P23947,P23949`
- XDef (135): `P24028,P24046,P24055,P25028,P25258,P25322,P25333,P25362,P25365,P25371,P25374,P26581,P26587,P26593,P26598,P26599,P26601,P27394,P27624,P27635,P28057,P28530,P28538,P28539,P28542,P28553,P28575,P30042,P30043,P30078,P30114,P30132,P30133,P30145,P30171,P30172,P30183,P30188,P30204,P30217,P30224,P30225,P30227,P30234,P30240,P30241,P30244,P30245,P30250,P30251,P30252,P30254,P30453,P30454,P30459,P30460,P30461,P30462,P30463,P30464,P30465,P30466,P30467,P30468,P31268,P31269,P31272,P31550,P32611,P32613,P32614,P32615,P32616,P32941,P33047,P33055,P33240,P33241,P33250,P33572,P33637,P33808,P33809,P34019,P34141,P34273,P34325,P34328,P34366,P34794,P36072,P36117,P36178,P36345,P36354,P36405,P36406,P36439,P36441,P36559,P36560,P36561,P36570,P36876,P36889,P36890,P36893,P36894,P36895,P36896,P36897,P36898,P36899,P36900,P36901,P36902,P36904,P36906,P36944,P36945,P37015,P37021,P37068,P37069,P37072,P37159,P37189,P37226,P37315,P37317,P37325,P37326,P37343,P37371,P37454`

## Final limits and handoffs

- No final defect verdict is issued. No eligible new hard-tell seed survived this source read.
- Runtime/native blind spots: particle rendering/asset resolution; random map placement distribution; actual UI frame cost; dynamic event bindings; platform/gamepad behavior.
- Conditional dlccheck handoffs only: prove the building-class/prg_class caller for the five added AmbientLife programs; test WorkFarmSmall's `Maps[1]` only if another-map reach is established. The Norman-gated Now Serving UI needs owner runtime measurement only if its repeated menu scan is suspected in profiling.
- Existing C56/C58/C59 and other SEAM_REPORT findings were not duplicated.

