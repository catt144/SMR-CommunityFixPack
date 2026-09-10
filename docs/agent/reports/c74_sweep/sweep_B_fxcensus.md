# Sweep B — ActionFX census (1.1.0.403908 vs 1.0.7.396349), desk only

Trees: `C:\Dev\SMR-SrcArchive\<ver>\Src` (both have `Src`). Citations are `tree path:line`; bare paths mean 1.1.0.
Scripts (re-runnable, scratchpad): `fx_census.py` (lupa loader + indexes) -> `fx_analyze.py` -> `fx_report_data.py` -> `fx_routes.py [tree]`.
JSON outputs: `census_<tree>.json`, `literals_<tree>.json`, `analysis_<tree>.json`, `routes_<tree>.json`, `treediff.json`.

## 0. Method + controls

- Loader: every `Data/FXPreset/*.lua` + `DLC/*/Presets/FXPreset/*.lua` is executed in lupa. A `PlaceObj` stub records class, props and `debug.getinfo(2).currentline`. Nested `ActionFXEndRule` objects are kept under their parent's `EndRules` field and not counted as FX. AnimMetadata and BuildingTemplate presets are loaded the same way.
- **CONTROL (task 1) PASS, both trees.** The census has all 8 ActionFXSound + 3 ActionFXParticles `hit-moment*` entries on `Target=UniversalExtractorHammer`:
  - 1.1.0: ActionFXSound.lua:17156/17166/17187/17197/17208/17218/17229/17239 and ActionFXParticles.lua:860/897/916.
  - 1.0.7: ActionFXSound.lua:19034..19117 and ActionFXParticles.lua:882/921/941.
  - There is also a 4th hammer particle with Moment=`start` (1.1.0 ActionFXParticles.lua:1931).
- Literal index: every string literal in all non-FX `.lua` under Lua/, CommonLua/, DLC/ and Data/ (comments stripped), with file:line. There are 66,894 distinct literals in 1.1.0.
- Class index: brace-matched `DefineClass.X = {…}` / `DefineClass("X", …)`, 4,047 classes in 1.1.0. Templates: 323. Entities (`EntityData["X"]`): 3,342.
- Orphan method control: known names (`PreciousMetalsExtractor`, `MOXIE`, `MirrorSphere`, `Metatron`) resolve to class, and `UniversalExtractorHammer` to entity. A fabricated `ZzNoSuchClass` returns orphan.
- Coverage control: in both trees, 0 non-generic (Action, Moment) rows are left unrouted when the moment is not co-located with its Action in code.

## 1. Totals

| class | 1.1.0 | 1.0.7 |
|---|---|---|
| ActionFXSound | 1825 | 2013 |
| ActionFXParticles | 751 (746 base + 5 norman) | 762 |
| ActionFXObject | 76 (74 + 2 norman) | 74 |
| ActionFXLight | 18 (17 + 1 norman) | 17 |
| ActionFXRemove | 7 | 7 |
| ActionFXColorization | 2 | 2 |
| ActionFXUIParticles | 1 | 1 |
| **total** | **2680** | **2876** |

(`ActionFXEndRule`: 1122 nested objects in each tree, not FX.)

Files: 1.1.0 `Data/FXPreset/ActionFX{Sound,Particles,Object,Light,Remove,Colorization,UIParticles}.lua` + `DLC/norman/Presets/FXPreset/ActionFX{Particles,Object,Light}.lua`; 1.0.7 only the Data set (no DLC FX files). `DLC/thomas` has no FX.

AnimMetadata presets (both trees; the norman group exists only in 1.1.0):
- `Data/AnimMetadata.lua`: AdvancedStirlingGenerator (closing, idle, idleOpened, opening — `Hit`), CaveIn_Buildings / CaveIn_UndergroundDome / CaveIn_UndergroundMicroDome (falling — `Hit`).
- `DLC/norman/Presets/AnimMetadata.lua:166` BakeryHands/workIdle (`bread_raw_*`, `bread_baked_*`).
- The brief's list of 5 groups is confirmed; 1.0.7 has 4 (no BakeryHands).

## 2. How moments reach FX (the rules this census relies on)

- `PlayFX(action, moment, actor, target)` (CommonLua/Classes/ActionFX.lua:144) → `GetPlayFXList` (ActionFX.lua:4095-4168).
  - Matching walks the action, moment, actor and target inherit lists and always ends at `"any"`. An actor/target of nil/false skips straight to `"any"` (ActionFX.lua:4109-4145).
  - `Target="ignore"` is stored under `"any"` (AddInRules ActionFX.lua:229).
  - So **an entry with no Actor (`Actor="any"`) matches every PlayFX with that Action+Moment, whatever the actor, including nil.**
- `Lua/_fixup.lua:1556-1568` wraps PlayFX to accept a table form `{actionFXClass=…, actionFXMoment=…}` (1.0.7 `_fixup.lua:1450`).
- Animation moments exist only in Lua presets:
  - `CObject:GetAnimMoments` → `GetEntityAnimMoments` → `Presets.AnimMetadata[GetAnimEntity(entity, anim)][anim].Moments` (CommonLua/Classes/AnimMoment.lua:5-16, 35-37).
  - `TimeToMoment`, `TypeOfMoment`, `GetAnimMoment` and `GetAnimMomentsCount` all go through it (AnimMoment.lua:127-331). No other definitions exist outside the editor (grep control: only `AnimationMomentsEditor.lua:378/593`, which are editor classes).
  - **No preset means no moments for any Lua-side tracker.**
- Anim-moment → FX routes in the code:
  1. `CObject:OnAnimMoment` → `PlayFX("Anim:"..anim, momentType, self)` (AnimMoment.lua:152-154, FXAnimToAction ActionFX.lua:1464-1469). It is reached from `WaitMomentTrackedAnim` and from AnimMomentHook objects with `anim_moments_hook_all` (`WaitTrackMoments`, AnimMomentHook.lua:74-112, 126-129).
  2. `TrackAllMoments(obj, fx_action, actor, target)` (Lua/Buildings/Building.lua:3364) uses `GetAllAnimMoments` (Building.lua:3346-3362), i.e. presets. It passes the state **name**, so it has no index bug, but it is dead without a preset.
  3. `BaseBuilding:TrackMultipleHitMoments` (Lua/Buildings/BaseBuilding.lua:1037-1079) calls `GetAnimMomentsCount(obj:GetAnim(1) /*index*/, "Hit")` (:1045-1046). It is dead on the index-vs-name bug (C74) and also on missing presets. Its default moment list is `hit-moment1..2` (:1026).
  4. Metatron's private copy (Lua/Mysteries/Metatron.lua:50-80) has the same index-vs-name bug (`self:GetAnim(1)` at :52) and emits `"Start"..i` / `"End"..i`.
- Lifecycle/generic moments `start` and `end` are fired by the FX system and its callers everywhere. Examples:
  - `PlayWorkingStateFXes` (BaseBuilding.lua:870)
  - `PlayDestructionFX` (ActionFX.lua:54)
  - `Unit:StartFX`/`StopFX` (Lua/Units/Unit.lua:79-96)
  - the anim-hook start/end (AnimMomentHook.lua:82/109/146/152)
  
  `any` is the wildcard. These 340 (Action, generic-moment) rows are class (i) and were not traced per Action; that was out of scope.

## 3. Distinct moments and classification (1.1.0: 95 distinct; 1.0.7: 95)

1.1.0 non-generic (Action, Moment) pairs: 121.
- **35 are "co-located"**: a literal PlayFX site for that Action has the moment string within 25 lines. That is class (ii) CODE-FIRED, cited in `analysis_1.1.0.json` (`colo` field). Examples: `AlienDiggerLanding/pre-hit-ground-2` Lua/Mysteries/Diggers.lua:124; `RegolithExtractorDigging/dig-reverse` RegolithExtractor.lua:494; `StirlingGenerator/open_start` StirlingGenerator.lua:57.
- **86 were hand-routed** (fx_routes.py table, each rule cited):

| route | meaning | 1.1.0 entries | 1.0.7 |
|---|---|---|---|
| CODE (dynamic string) | fired by code that builds the moment | 47 | 47 |
| PRESET | needs `Presets.AnimMetadata[entity]` (class iii) | 45 | 44 |
| TRACKER | TrackMultipleHitMoments (dead, C74) | 14 | 14 |
| NOPATH | no code emits this moment for this Action, even with presets | 24 | 24 |
| DISABLED | `Disabled=true` | 174 (all moments) | 180 |

CODE-FIRED dynamic moments (class ii):

| Action / Moment | Site |
|---|---|
| ElectrostaticStorm / hit-moment1..4 | Lua/DustStorm.lua:267 |
| Dig / hit-moment1..3 | Lua/Mysteries/MirrorSphere.lua:872-873 |
| StirlingGenerator / hit-moment | Lua/Buildings/StirlingGenerator.lua:72 |
| MysteryDream / hit-moment | Lua/Units/Colonist.lua:4960+4965 via Unit.lua:89-92 |
| CrystalCompose / attach1..12 | Lua/Mysteries/Crystals.lua:288 |
| PlantsGrowing / idle2..4 | Lua/Buildings/Farm.lua:411 + Lua/Crop.lua:19-20 |
| EmergencyRecharge / hooking | RechargeStation.lua:179 / RCRover.lua:170 then Lua/Units/Drone.lua:1578 |
| BlackCubeDemolishBuilding / hit | Data/Scenario/Mystery 1.lua:414-415 → Lua/Sequences/SA_Gameplay.lua:2024 |

**Task-2(iii) grep receipts.** Command: `grep -rlF '"<m>"' Lua CommonLua DLC --include=*.lua`, with FXPreset/AnimMetadata hits listed separately.
- Zero code hits, data definitions only, for: `LiftStart LiftEnd SprayStart SprayEnd RotateStart Hit1 Out1 Out12 End1 End7 hit-moment4 hit-moment5 hit-moment7 dig-reveerse bread_raw_start bread_baked_start`.
- The same command finds the controls: `pre-hit-ground-2` Diggers.lua:124, `hooking` Drone.lua:1578, `dig-reverse` RegolithExtractor.lua:494/737, `hit-moment` BaseBuilding.lua:1026 + StirlingGenerator.lua:72, `attach` Crystals.lua:287-288.
- `Hit`/`HitN`/`OutN`/`EndN` have no literal because TrackAllMoments/Metatron take the moment **types from the preset** at run time. So these are anim-only by construction, not by absence of a grep hit.

## 4. Candidates — FX that need an animation moment, grouped by entity (1.1.0; ranked by FX count)

"Preset?" is checked against the 5 AnimMetadata groups. Any GetAnimEntity redirect would have to land on one of those 5 groups, and none is plausible for these entities.

| # | entity whose anim must carry the moment | FX (1.1.0) | route | player misses | sites (1.1.0) |
|---|---|---|---|---|---|
| 1 | **ExcavatorShovel** (TheExcavator arm, TheExcavator.lua:47) | **24 particles** (`Hit1..12`, `Out1..12`) | TrackAllMoments TheExcavator.lua:120 | dig/dump dust bursts on The Excavator (wonder) | ActionFXParticles.lua:115-530 |
| 2 | **UniversalExtractorHammer** (PreciousMetalsExtractor, entity UniversalExtractor) | 9 live-keyed (6 sound + 3 particle) + 2 hit-moment4 sounds (NOPATH) | TRACKER BaseBuilding.lua:929/947 | hammer peaks/smoke sounds + steam (C74, measured dead) | Sound 17156-17239, Particles 860/897/916 |
| 3 | **Monolith** (Metatron, Metatron.lua:23) | 7 particles `End1..7` (PRESET + index bug) + 7 sounds `hit-moment1..7` (NOPATH) | Metatron.lua:52-80 | rotation particles and "Mystery Metatron Rotate" sound | Particles 5486-5601, Sound 7442-7514 |
| 4 | **MoxiePump** / any MOXIE attach | 5 (3 sounds Target=MoxiePump, 2 particles Target=any) | TRACKER (MOXIE.lua:5, default list 1..2) | MOXIE LoopPeaks/LoopSteam sounds + steam puffs (measured dead) | Sound 17136/17146/17177, Particles 842/879 |
| 5 | **Shuttle** (ShuttleHub.lua:461) | 4 (ShuttleHubExit Hit: 2 particles + 1 sound; ShuttleHubEnter Hit: 1 sound) | TrackAllMoments ShuttleHub.lua:1632/1649 | touchdown/lift-off hit sound + particles at hub | Particles 8404/8421, Sound 13519/13480 |
| 6 | **WaterExtractorPump** (WaterExtractor.lua:113) | 3 sounds (`working`/Hit; Actors WaterExtractor ×2, MicroGAutoWaterExtractor ×1) | TrackAllMoments WaterExtractor.lua:115 | pump stroke peaks | Sound 20276/20286/20296 |
| 7 | **RoverTerraformer** (RCTerraformer.lua:6) | 3 (Load/Hit1 particle+sound, Construct/Hit1 particle) | TrackAllMoments RCTransport.lua:133-134 (`track_anim_moments={"workIdle"}` RCTerraformer.lua:35) | load/construct impact puff + sound | Particles 7119/6948, Sound 7031 |
| 8 | **RoverRussiaDriller** (RCDriller.lua:6) | 2 (Drill/Hit particle + sound) | TrackAllMoments RCDriller.lua:105 | drill hit burst + sound | Particles 6999, Sound 5568 |

Positive control for the preset route: **BakeryHands** (DLC) has a preset (`DLC/norman/Presets/AnimMetadata.lua:166`). Its 2 ActionFXObject entries (`Anim:workIdle`, bread_*_start; `DLC/norman/Presets/FXPreset/ActionFXObject.lua:3/17`) are reached via `anim_moments_hook_all` (`DLC/norman/Code/Bakery.lua:1-4`). They are **not** a candidate; this is the only anim-moment FX route that has data behind it.

Tracker attribution, per the coordinator's lead:
- **All 16 `Working`/`hit-moment*` entries belong to two of the five tracker classes** (11 PreciousMetalsExtractor → PreciousMetalsExtractorBase, 5 MOXIE → MOXIEBase; class chain from the template index).
- **None are keyed to ElectrolyzerBase** (template Electrolyzer), **MicroGExtractorBase** (MicroGExtractor, …Metals, …RareMetals, …ExoticMinerals) or **PreciousMineralsExtractorBase**. That last class has **no template** in 1.1.0 (0 templates inherit it).
- Those three trackers run with no FX consumer. Fixing the tracker would change nothing audible for them.
- No `Working`/`hit-moment*` entry has `Actor=any`.

NOPATH, unreachable even with presets. These are dead data, not anim candidates; list them separately:
- `HydroponicFarm` Lift/Spray/Rotate, **10 sounds** (ActionFXSound.lua:6785-6890). There is no PlayFX("HydroponicFarm",…) anywhere, `FarmHydroponic:StartAnimThread` is empty (Farm.lua:1033; 1.0.7 Farm.lua:796), and `HydroponicFarmElevator` is a bare entity class (Farm.lua:1036). This looks like a removed elevator animation driver. It is the largest dead sound group after the Excavator.
- `MetatronRotation` hit-moment1..7, 7 sounds. The code emits `Start<i>`/`End<i>`, not `hit-moment<i>`.
- `ConstructingDrones` Hit1..4 on DroneHub, 4 particles (only start/end at DroneFactory.lua:52/63, Station.lua:527/537).
- `Working` hit-moment4, 2 hammer sounds (tracker lists stop at 3).
- `RegolithExtractorDigging` `dig-reveerse` typo, 1 sound (ActionFXSound.lua:10141).

## 5. The 13 no-Actor hit-moment* entries — resolved (both trees)

All 13 have `Actor="any"`, `Target="ignore"`. That is 12 ElectrostaticStorm + 1 MysteryDream (9 particles + 4 sounds).

| entries (1.1.0) | who fires them | verdict |
|---|---|---|
| ElectrostaticStorm hit-moment1..4: particles ActionFXParticles.lua:3066/3078/3090/3102/3113/3125/3136/3148, sounds ActionFXSound.lua:5716/5727/5738/5749 | `ElectrostaticDustStormStrike` → `PlayFX({actionFXClass="ElectrostaticStorm", actionFXMoment="hit-moment"..(1+Random(4)), action_pos=…})` Lua/DustStorm.lua:265-270. Unpacked by `_fixup.lua:1556`. Nil actor falls to "any" (ActionFX.lua:4109-4145). 1.0.7: DustStorm.lua:241-244 + `_fixup.lua:1450`. | **CODE-FIRED, fine** |
| MysteryDream hit-moment: particle ActionFXParticles.lua:5143 | `Colonist:MysteryDream` → `StartFX("MysteryDream")` (Colonist.lua:4960) then `PlayFXMoment("hit-moment")` (:4965) → `PlayFX(self.fx, moment, self.fx_actor=colonist)` (Unit.lua:79-92). Colonist actor falls through inherit to "any". | **CODE-FIRED, fine** |

Note: the combo count is 8 distinct (Action, Actor, Target) among the 40 hit-moment* entries, not 9. The difference may come from the earlier census keying on something extra; re-derive before citing either number.

## 6. Orphaned FX names (task 5; not defects)

1.1.0 names with no class, template or entity, and no literal outside FX data (same method as the controls in §0):
- `Actor=BombardRocket` ×4 sounds (ActionFXSound.lua:357/580/5467/…). It appears nowhere else in the tree.
- `Actor=GiantLaser` ×2 and `PowerSwitch` ×3; these appear only in Data/SoundPreset.lua.
- `WaterTower` ×2 (only SoundPreset / a particle preset / a tutorial text).
- `RCExplorer` ×1, which is Disabled. The rover's actor class is `ExplorerRover` (ExplorerRover.lua:26).
- `Target=idCategory1..11`, 11 `UIButtonPressed` sounds (ActionFXSound.lua:16051-16161). Only an unnumbered `idCategory` Id exists (CommonLua/Data/XDef/BugReport.lua:223). This is likely a legacy UI; unresolved.

ActionFXRemove, 7 entries (design): ActionFXRemove.lua:3 (Working/start MOXIE→MoxieCP3Pump, FxId MoxieSmoke), :13, :22, :32, :42, :52, :62.

## 7. 1.0.7 → 1.1.0 differences

- The FX engine and anim-moment readers are functionally the same.
  - ActionFX.lua adds only debug-selection and map-gating changes (e.g. `IsCurrentMapOnly` at 1.1.0 ActionFX.lua:199-201) and `GetCustomFXInheritActionRules`.
  - The AnimMoment.lua `table.ifilter` lambda change matches each tree's own `table.ifilter` signature (1.0.7 CommonLua/Core/types.lua:345-346 passes `(i,obj)`; 1.1.0 types.lua:362-363 passes `(obj)`), so there is no break.
  - `TrackAllMoments`/`GetAllAnimMoments` are byte-identical. TrackMultipleHitMoments differs only in the thread closure's parameter list; the index bug is the same in both.
- AnimMetadata: identical, except 1.1.0 adds the BakeryHands (norman) group.
- FX multiset (key = class, Action, Moment, Actor, Target, asset, Disabled): 235 entries only in 1.0.7 and 39 only in 1.1.0.
  - 1.1.0 dropped 194 SelectObj sounds (165 actors), the `MeteorLarge2`/`MeteorSmall2` meteor set, 5 disabled `Research` particles (`done`, `50+` moments; that is why those two moments exist only in 1.0.7), and 1 `working`/Hit MicroGAutoWaterExtractor sound. 1.0.7 had 2 of those (ActionFXSound.lua:22030/22040); 1.1.0 has 1.
  - 1.1.0 **fixed actor typos**: `GHGFActory`→`GHGFactory`, `PolymerFactory`→`PolymerPlant` (Destroyed sounds). It retargeted Meteor/Spawn sounds from `Building` to `DestroyedBuilding`.
  - 1.1.0 added the norman DLC FX (Bakery, FarmInsect, AutomatedFarm, FoodProcessing, SmallFarm sprinkler), Replicator and WindTurbine_Diffuser Working FX, and Thrusters for Rocket/SupplyPod.
- Candidate set: identical in both trees except the WaterExtractorPump group (1.0.7: 4 sounds, 1.1.0: 3). All candidates are pre-existing 1.0.7 defects.

## 8. Unresolved / limits

- Everything here is desk-derived. Only the hammer and MOXIE have been measured live (C74).
- Candidates 1 and 5-8 all run through the same preset-only reader, so a single live check would confirm the class: The Excavator dust bursts, or a Water Extractor pump-stroke sound, with a debug `print` inside TrackAllMoments showing `#moment_names == 0`.
- `GetAnimEntity` is engine-side and could not be read. The claim "no preset ⇒ no moments" assumes it cannot map these entities onto one of the 5 preset groups.
- The co-location heuristic (moment literal within 25 lines of an Action literal) classified 35 rows as code-fired without per-row reading. I spot-checked Diggers, RegolithExtractor, Crystals, Stirling, OpenAirBuilding and SupplyGridSwitch; the rest are trusted on the heuristic.
- Class (i) generic rows (340) were not traced per Action for a live caller. A dead `start`/`end` FX (Action never fired) is outside this census.
- `idCategory1..11` is unresolved; it looks like a legacy UI orphan.
