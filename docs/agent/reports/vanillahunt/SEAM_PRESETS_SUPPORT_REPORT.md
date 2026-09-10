# 03b support/story preset read-only report

Date: 2026-09-10. Sources: `O = C:/Dev/SMR-SrcArchive/1.0.7.396349/Src`, `N = C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`. The live appmanifest was re-read as build `24995074`. This is a source-read handoff, not a defect verdict or a runtime test. No game was launched, no archive/game/repository file was written, and no tagged TSV was changed. The only DLC interior opened was the directly called `N/DLC/norman/Code/FarmInsect.lua:57-59` function.

## Receipt and drift

Filter: `link == 03` and class in the 21-class assignment. Result: **510 rows**, **510 unique `prid` values**, zero missing expected keys, zero duplicate `prid` values. (`key` is a field path and is intentionally non-unique.) Class totals:

| class | rows | class | rows |
|---|---:|---|---:|
| PresetDef | 251 | StoryBit | 127 |
| SA_Exec | 23 | OnScreenHint | 20 |
| Label | 13 | SA_WaitMessage | 11 |
| SoundPreset | 10 | ClassDef | 9 |
| NotificationPreset | 8 | PopupNotificationPreset | 8 |
| EncyclopediaArticle | 7 | SA_GrantTechBoost | 4 |
| MsgDef | 2 | SA_WaitChoice | 2 |
| AppendClassDef | 10 | DumbAIDef | 1 |
| ScriptConditionList | 1 | StatsImpactRest | 1 |
| StatusEffectPreset | 1 | TraitPreset | 1 |

All 510 rows were reached as source definitions. The full present owning preset/class bodies on both sides (or the sole present side for an add/remove), their generated twins in both directions where one exists, and the actual Lua reader/consumer were inspected. “Read” is not “tested.” Dynamic/native callers, assets, rendering, localization at runtime, and game execution remain unmeasured.

**Malformed/hunk-only identity drift (29 rows):** `presetdiff` keys id-less presets by class + file + ordinal. These rows do not describe a valid same-object old/new pair because same-class insertions/removals shifted ordinals. Both ordinal bodies and generated scenario hunks were inspected, but these rows remain hunk-only and are not semantic changes: Label (file count 76→79): `P05907 P05908 P05911 P05912 P05915 P05916 P05917 P05923 P05924 P05952 P05959 P05973 P05980`; SA_Exec, Mystery 7 (85→93): `P11840 P11853 P11861 P11871 P11984 P12007 P12013 P12024 P12025 P12032 P12042`; Mystery 8 (31→32): `P12063`; Mystery 9 (46→48): `P12094 P12097 P12144`; SA_WaitMessage UndergroundAnomalies_Rare (25→24): `P12475`. This is caught instrument drift, not a gameplay conclusion.

No other queue row was not reached. No queue row was omitted. `Data/StoryBit` has no separate generated twin; nested effect classes do, and those effect implementations were checked. Added definitions have `O:absent`; removed definitions have `N:absent` rather than an invented counterpart.

## Surviving leads (no verdict)

### L1 — The Incident no-explosion construction suspension

`P18963`, `Data/StoryBit/TheIncident_3_Aftermath_NoExplosion.lua`, `StoryBit:TheIncident_3_Aftermath_NoExplosion`, `Effects[1].Tech`: old absent → new `TheIncident`. The new branch discovers the tech at `N:15-19`, and activation disables only already-existing `FusionReactor` objects at `N:4-12`. The visible text says construction of new reactors is suspended (`N:46`). The full preset retains two unusually direct author comments: “no effect to disable construction of Fusion Reactors; No tech implemented” (`N:57`) and “should make sure that Fusion Reactor constructions are on hold in general and resumed in this case” (`N:62`). The tech half was added; no construction-site or build-menu effect is present. Its Explosion sibling contains `SetConstructionSiteState` plus `LockUnlockBuildingFromBuildMenu` (`N/Data/StoryBit/TheIncident_1_Aftermath_Explosion.lua:11-23`, also present in O). This is a **PASSING-style hard tell** surfaced while reading the changed row, not a claim that P18963 caused the pre-existing omission.

Reach: R2 after the no-explosion Incident follow-up is selected/activated. Player action: enter the event branch, then try placing or continuing a Fusion Reactor before researching The Incident. Falsifier: an independently reached common path already locks both construction sites and the build menu for this branch, or an observed run proves new construction impossible. Seam/non-owner: all named definitions/effects are base; the same mismatch is available without DLC. SMELL: sibling contradiction and explicit unfinished author comments. PERF: none in the opened bodies.

### L2 — FactionOpportunity nil-guard asymmetry

`P08551/P08552`, `Data/NotificationPreset.lua`, `NotificationPreset:FactionOpportunity`: DismissFunc adds `canceled_faction_task_time = GameTime()`; PressFunc changes from generic object navigation to a guarded `g_Legislature` task/UI route with fallback. Old full preset is `O:1212-1227`; new is `N:1916-1944`. New PressFunc first evaluates `g_Legislature and ...`, while new DismissFunc immediately dereferences `g_Legislature` twice. Old DismissFunc was already unguarded, so this is a **PASSING/asymmetry hard tell**, not a clean diff-caused assertion.

Reach: R2 while FactionOpportunity is displayed and dismissed as legislature state is absent/torn down. Falsifier: notification lifecycle proves it is synchronously removed before `g_Legislature` can become false in every path, or a controlled run dismisses it safely after teardown. Seam/non-owner: the politics system and preset are in base; no DLC class is required. SMELL: adjacent guard contradiction. PERF: none.

### L3 — Long Winter no-tech branch changes discovery to full grant

`P16594`, `Data/StoryBit/LongWinter_BigExtension_NoTech.lua`, `StoryBit:LongWinter_BigExtension_NoTech`, `Effects[1].Tech`: the nested effect changes from `DiscoverTech{Tech="SubsurfaceHeating"}` to `RewardTech{Research="SubsurfaceHeating"}` (the flattened row records the vanished `Tech` key; the whole-node class/key change is visible only in the full body). `DiscoverTech:__exec` calls discovery, while `RewardTech:__exec` calls researched/grant state. This is a real behavior delta, but no hard unintended-intent tell was found.

Reach: R2 through Long Winter's no-tech extension branch. Player action: reach that branch with Subsurface Heating unknown. Falsifier: design intent or runtime observation confirms the branch is meant to grant completed research, not merely reveal it. Seam/non-owner: base story/effect/tech only. SMELL/PERF: none.

### FR-2 — Boost2_DigDeep

The FR-tagged row was read first. `P13830`, `Data/StoryBit/Boost2_DigDeep.lua`, `StoryBit:Boost2_DigDeep`, `[2].Effects[4].Tech`: absent → `DeepScanning`. The same reply also changes outcome wording (`P13827`) and now runs two deposit spawns, `RewardTechBoost{Research="DeepScanning", Amount=50}`, then `DiscoverTech{Tech="DeepScanning"}`. `StoryBitState:ProcessOutcomeEffects` preserves array order (`O/Lua/_StoryBits.lua:723`, `N:749`). In N, `RewardTechBoost:__exec` (`Lua/ClassDefs/ClassDef-Effects.generated.lua:2467`) routes explicit Research to `Research:BoostTech` (`Lua/Research.lua:255`), followed by `DiscoverTech:__exec` (`...Effects.generated.lua:646`). The live `Tech:DeepScanning` is `N/Data/Tech.lua:3934-3961`; `Data/TechPreset.lua:847-852` is a legacy stub, not a second live effect definition. The source route is coherent but does not close FR-2.

Reach: R2, pre-founder Boost2 first reply. Player action: select it and inspect Deep Scanning discovery plus its per-tech 50% boost. Falsifier: observed absence/wrong ordering, or an engine loader override that reorders effect arrays. Seam/non-owner: wholly base. Hard tell: none. SMELL/PERF: none.

## Route dossiers used by the exact ledger

Every ledger row below inherits all fields in its route code: actual reader/consumer, reach/action, falsifier, seam/non-owner result, hard tell, and FIX_POLICY §4 SMELL/PERF result. `loc` is the exact owning definition's ID line (or id-less `PlaceObj` ordinal line) in O and N; the complete owning bodies, not just those lines, were read.

- **SB** — StoryBit data consumed by `StoryBitState` activation/reply/outcome processing (`O/Lua/_StoryBits.lua:723`, `N:749`) and nested effect `Execute/__exec` classes (generated twin `Lua/ClassDefs/ClassDef-Effects.generated.lua`). R2: trigger the named story and choose the affected reply. Falsifier: authored route is unreachable/obsolete or run shows different text/effect. Base seam/non-owner present. Hard tell none; SMELL/PERF none. Obsolete FoodFight, DustSickness, WindsOfChange families are source-reached but runtime-not-reached (R4) in current data.
- **FR2/L1/L3** — use the dedicated dossiers above.
- **PD-A** — Animal schema moves scalar food to `OutputResources`; generated twin `Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:3+`; actual readers `N/Lua/Units/Animals.lua:714-1047`. R2 via pasture breeding/harvest; falsifier output differs from authored list. Base Animal remains for non-owners. No new tell; SMELL/PERF none. (Overlaps parent C56 evidence but does not duplicate its verdict.)
- **PD-C** — CropPreset migration to `OutputResources` plus growth/farm metadata; generated twin `...PresetDefs.generated.lua:727-787`; readers `N/Lua/Crop.lua:25-149` and `N/Lua/Buildings/Farm.lua:17-739`. R2 via planting/growth/harvest; falsifier generated/live crop or harvest disagrees. Base works without DLC. No new tell; SMELL/PERF none (overlaps C59 evidence, no duplicate verdict).
- **PD-T** — TechPreset old runtime-rich class becomes legacy compatibility shell while live techs are `Data/Tech.lua` `Tech` objects consumed through `Techs`; `Data/TechPreset.lua` retains inert compatibility IDs. R2 via tech UI/effects; falsifier a traced runtime reader uses legacy fields as authoritative. Base/non-owner registry exists. No tell; SMELL/PERF none.
- **PD-V** — Vegetation OutputResources schema; reader `N/Lua/Vegetation.lua:1794+` and TerraformingBuilding paths. R2 through vegetation production; falsifier emitted resources differ. Base definitions work; DLC-owned actor rows remain inert without their class. No tell; SMELL/PERF none.
- **PD-O** — Cargo/CargoResource/CargoUnit/CargoBuildingPrefab, CommanderProfile, FlightPolicy, MissionSponsor, PlanetaryAnomalyDescription, POI, LawDef/PolicyDef and other PresetDef editor/schema churn. Generated twins were checked; LawDef/PolicyDef behavior moved from old generated `Lua/ClassDefs/ClassDef-Factions.generated.lua` to `N/Lua/Factions/LawDef.lua`, not deleted. R1/R2 through the named registry/UI; falsifier generated/live object lacks the recorded property. Base shells are present; DLC-only values inert for non-owner. No hard tell; SMELL/PERF none.
- **AX** — AppendClassDef Resource fields feed `N/Lua/Resources.lua:30-54` (`OnMsg.PreProcessResource`) and `N/Lua/Buildings/MultiResourceCubeVisuals.lua:199-203`; generated twin `Lua/ClassDefs/ClassDef-Resources.generated.lua:39-41`. R1/R2 at resource preprocessing/storage UI. Falsifier registry omits/misgroups base resource. Base safe; optional DLC resources absent. No tell; SMELL/PERF none.
- **CD** — ClassDef rows are property reorder/move: MapDataProperties reindex; LawEffect classes moved to `N/Lua/Factions/LawDef.lua:362-673` from old generated definitions. R2 when effects execute. Falsifier class absent after class build. Base present. No tell; SMELL/PERF none.
- **SX** — Stable-ordinal SA_Exec code leaf replaces `TechDef[id].display_name` with `Techs[id].DisplayName`; matching `Lua/Scenario/*.generated.lua` twins execute via scenario `SARun`. R2 through named mystery sequence. Falsifier sequence does not reach that node/new registry is missing. Base seam. No tell; SMELL/PERF none.
- **MAL** — malformed ordinal alignment listed above. Actual change is “no valid row-pair; inspect semantic file hunk instead.” Reach/action/falsifier/seam verdict are not attributable to the row. Non-owner base file exists. Hard tell is instrument identity drift only; no gameplay tell. SMELL/PERF not attributable.
- **SG** — SA_GrantTechBoost fields migrate to Hi-Tech/Underground naming; `O/Lua/Sequences/SA_Gameplay.lua:817`, `N:822` and generated scenario twins. Empty Research uses `BoostTechField`; explicit Research uses `BoostTech`. R2 by scanning the anomaly/sequence. Falsifier resulting field boost differs. Base. No tell; SMELL/PERF none.
- **SW/SC** — SA_WaitMessage/SA_WaitChoice presentation text, generated scenario twins and sequence wait UI. R2 by reaching the node/choice. Falsifier shown text differs. Base. No tell; SMELL/PERF none.
- **H** — OnScreenHint definitions consumed by base hints/UI. `HintComfortFood` becomes obsolete and its save fixup removes it; `HintCrops` is added in base and has a DLC override. R1/R2 on matching hint trigger/building construction. Falsifier hint not selected/rendered. Non-owner gets base definition; DLC owner may override wording. No tell; SMELL/PERF none.
- **SO** — SoundPreset definitions are referenced by base `Data/FXPreset/ActionFXSound.lua`; OpenFarm range changes 2000→1500 and several IDs are added. R2 when matching FX actor/action fires; native playback/assets unmeasured. Falsifier resolved FX uses another preset/range. Base presets exist; DLC actor can be absent. No tell; SMELL/PERF none.
- **N** — NotificationPreset data consumed by HUD notification machinery. CropsFailed text markup, StarvingColonists addition, TerraformingSeeds markup, PoliticsOpenSession obsolescence/removal path. R1/R2 on matching notification trigger. Falsifier notification route uses another ID. Base definitions; no DLC required. No tell; SMELL/PERF none.
- **NI** — added `CropsFailed_Insects`; only direct caller found is the permitted `N/DLC/norman/Code/FarmInsect.lua:57-59`, returning that ID. R2 for DLC owner with insect crop failure; non-owner R4/inert because no base caller/class. Falsifier another base caller exists or owner route uses different ID. No tell; SMELL/PERF none.
- **NF** — use L2 dossier.
- **P** — PopupNotificationPreset UI text/add/remove. Starving first-status popup is removed alongside data-driven starving/missed-meal notification; tutorials replaced; NewFeatures has a base generic preset and DLC override. R1/R2 on popup trigger. Falsifier active preset/translation differs. Non-owner sees base, owner may override. No tell; SMELL/PERF none.
- **E** — EncyclopediaArticle presentation text consumed by Encyclopedia UI. R1 on opening article. Falsifier resolved translation/article differs. Base. No tell; SMELL/PERF none.
- **MSG** — MsgDef signature metadata. FoodProduced grows from `(building, amount)` to `(building, amount, resource)`; all three N emitters pass resource (`Buildings/FungalFarm.lua:14`, `Buildings/Farm.lua:497`, `Units/Animals.lua:757`). FoodServiceMealServed is added and emitted at `N/Lua/Buildings/FoodServiceBuilding.lua:805`. R1/R2 via production/service. Falsifier stale literal emitter or receiver contract mismatch. Base emission; DLC receivers optional. No tell; SMELL/PERF none.
- **AI** — default DumbAI research rule delegates selection to `DumbAIPlayer:RandResearchTechId` (`N/Lua/RivalColonies.lua:181+`), logs `Techs[id].DisplayName`, inserts researched ID, decrements TechPoints. Invocation is framework/dynamic (U); player action indirect through rival-colony simulation. Falsifier a controlled AI tick shows wrong point/tech accounting. Base; no DLC dependency. No tell; SMELL/PERF none.
- **BT** — old FungalFarm_Asteroid ScriptConditionList checking `ActiveLaws.Policy_SpaceFarming` is removed; new building template uses `disabled_in_environment = set("Surface","Underground")`, making it asteroid-only through BuildingTemplate availability. R2 with asteroid building menu/policy. Falsifier building is available in wrong environment or policy is still required by a live reader. Base template is present, but its old parent `FungalFarmBase` was DLC-shaped; no DLC interior was opened. No hard tell; SMELL/PERF none.
- **SR** — added StatsImpactRest:Food is registered in `ConditionalStatImpacts` (`N/Lua/Stats.lua:142-185`) and applied by `Colonist:GetRestStatTarget` (`N/Lua/Units/Colonist.lua:2519-2545`): +10000 Comfort after recent Diner meal. R2 on rest after Diner meal. Falsifier target lacks increment. Base Diner path exists; DLC may override same ID. No tell; PERF path already caches target (`Colonist.lua:2610+`), no new measured regression.
- **ST** — added data `StatusEffect_Starving`; old hard-coded starving class moves to generic data-driven `N/Lua/StatusEffectPreset.lua` consumption. R1/R2 on missed meals. Falsifier status/notification lifecycle differs. Base. No tell; SMELL/PERF none.
- **TR** — Martianborn `apply_func` is removed because `N/Data/Tech.lua:1396-1401` now applies an `Effect_ModifyLabel` to label Martianborn; save fixup explicitly removes stamped modifiers and reapplies the tech (`N/Lua/_fixup.lua:2682-2689`). R2 on researching tech/load old save. Falsifier new colonist misses modifier or old saves double-apply. Base. No tell; SMELL/PERF none.

## Exact 510-row ledger

Format: `prid | class | file :: preset/function :: field | loc O/N | actual delta | route dossier`. Long values are compacted only in this index; the complete values and complete containing bodies were read.
- P13294 | StoryBit | Data/StoryBit/Boost10_Frogleap.lua :: Boost10_Frogleap :: Text | loc O:21 / N:21 | T(820124822035, "With the downpour of new scientific data from Mars, ... => T(820124822035, "With the downpour of new scientific data from Mars, ... | **SB**
- P13297 | StoryBit | Data/StoryBit/Boost10_Frogleap.lua :: Boost10_Frogleap :: [1].Text | loc O:21 / N:21 | T(144383271199, "Physics") → T(144383271199, "Hi-Tech") | **SB**
- P13315 | StoryBit | Data/StoryBit/Boost10_Frogleap.lua :: Boost10_Frogleap :: [6].Effects[1].Tech | loc O:21 / N:21 | ResilientArchitecture → HomeCollective | **SB**
- P13353 | StoryBit | Data/StoryBit/Boost11_OtherSideSun.lua :: Boost11_OtherSideSun :: [1].CustomOutcomeText | loc O:32 / N:32 | T(776958472119, "gain <rechargestations> Recharge Station Prefabs; re... → T(776958472119, "gain <rechargestations> Recharge Station Prefabs; un... | **SB**
- P13357 | StoryBit | Data/StoryBit/Boost11_OtherSideSun.lua :: Boost11_OtherSideSun :: [3].CustomOutcomeText | loc O:32 / N:32 | T(555966538256, "gain <tanks> Water Tower and <tanks> Oxygen Tank Pre... → T(555966538256, "gain <tanks> Water Tower and <tanks> Oxygen Tank Pre... | **SB**
- P13361 | StoryBit | Data/StoryBit/Boost11_OtherSideSun.lua :: Boost11_OtherSideSun :: [5].CustomOutcomeText | loc O:32 / N:32 | T(101146018367, "gain <statuesandgardens> Statue Prefabs; reveal Tech... → T(101146018367, "gain <statuesandgardens> Statue Prefabs; unlock rand... | **SB**
- P13384 | StoryBit | Data/StoryBit/Boost12_DarkSideSun.lua :: Boost12_DarkSideSun :: [1].CustomOutcomeText | loc O:28 / N:28 | T(329677357422, "reveal Techs in the Biotech tree; gain <research(sma... → T(329677357422, "unlock a random Tech in the Habitation field; gain <... | **SB**
- P13388 | StoryBit | Data/StoryBit/Boost12_DarkSideSun.lua :: Boost12_DarkSideSun :: [3].CustomOutcomeText | loc O:28 / N:28 | T(940087920995, "reveal Techs in the Physics tree; gain <research(sma... → T(940087920995, "unlock a random Tech in the Hi-Tech field; gain <res... | **SB**
- P13390 | StoryBit | Data/StoryBit/Boost12_DarkSideSun.lua :: Boost12_DarkSideSun :: [4].Effects[2].Field | loc O:28 / N:28 | Physics → Hi-Tech | **SB**
- P13442 | StoryBit | Data/StoryBit/Boost14_MandatoryUpgrades.lua :: Boost14_MandatoryUpgrades :: Text | loc O:50 / N:50 | T(754140094868, "The Extractor Amplification project has received a m... → T(754140094868, "The Extractor Amplification project has received a m... | **SB**
- P13610 | StoryBit | Data/StoryBit/Boost18_ResearchCooperation_Finale.lua :: Boost18_ResearchCooperation_Finale :: [3].Prerequisite.Law | loc O:30 / N:30 | Policy_Outsourcing → <absent> | **SB**
- P13611 | StoryBit | Data/StoryBit/Boost18_ResearchCooperation_Finale.lua :: Boost18_ResearchCooperation_Finale :: [3].Prerequisite.Policy | loc O:30 / N:30 | <absent> → AdditionalSponsorResearch | **SB**
- P13827 | StoryBit | Data/StoryBit/Boost2_DigDeep.lua :: Boost2_DigDeep :: [1].CustomOutcomeText | loc O:15 / N:15 | T(968824402245, "gain a discount on the Deep Scanning Tech") → T(968824402245, "Deep Scanning Tech boosts next Tech Point") | **FR2**
- P13830 | StoryBit | Data/StoryBit/Boost2_DigDeep.lua :: Boost2_DigDeep :: [2].Effects[4].Tech | loc O:15 / N:15 | <absent> → DeepScanning | **FR2**
- P13934 | StoryBit | Data/StoryBit/Boost5_LeapForward.lua :: Boost5_LeapForward :: [1].CustomOutcomeText | loc O:21 / N:21 | T(327107269772, "reveal the Tech unlocking the Mohole Mine Wonder") → T(327107269772, "Initiative unlocking the Mohole Mine Wonder - <TechS... | **SB**
- P13936 | StoryBit | Data/StoryBit/Boost5_LeapForward.lua :: Boost5_LeapForward :: [2].Effects[1].Tech | loc O:21 / N:21 | ProjectMohole → MoholeMine | **SB**
- P13941 | StoryBit | Data/StoryBit/Boost5_LeapForward.lua :: Boost5_LeapForward :: [3].CustomOutcomeText | loc O:21 / N:21 | T(407459351494, "reveal the Tech unlocking the Project Morpheus Wonder") → T(407459351494, "Initiative culminating in the Project Morpheus Wonde... | **SB**
- P13944 | StoryBit | Data/StoryBit/Boost5_LeapForward.lua :: Boost5_LeapForward :: [4].Effects[1].Tech | loc O:21 / N:21 | DreamReality → BehavioralShaping | **SB**
- P13949 | StoryBit | Data/StoryBit/Boost5_LeapForward.lua :: Boost5_LeapForward :: [5].CustomOutcomeText | loc O:21 / N:21 | T(826549039619, "reveal the Tech unlocking the Artificial Sun Wonder") → T(826549039619, "Unlock the Artificial Sun Wonder Tech - <TechShortDe... | **SB**
- P14059 | StoryBit | Data/StoryBit/Boost7_DiminishingReturns_Success.lua :: Boost7_DiminishingReturns_Success :: [3].CustomOutcomeText | loc O:36 / N:36 | T(993109934364, "the Martian Patents Tech costs <boost>% less") → T(993109934364, "the Martian Patents Tech boosts next Tech Point by 3... | **SB**
- P14104 | StoryBit | Data/StoryBit/Boost9_Eureka.lua :: Boost9_Eureka :: [12].Effects[1].Field | loc O:21 / N:21 | Physics → Hi-Tech | **SB**
- P14106 | StoryBit | Data/StoryBit/Boost9_Eureka.lua :: Boost9_Eureka :: [12].Effects[2].Field | loc O:21 / N:21 | <absent> → Hi-Tech | **SB**
- P14130 | StoryBit | Data/StoryBit/Boost9_Eureka.lua :: Boost9_Eureka :: [6].Effects[1].Field | loc O:21 / N:21 | Physics → Hi-Tech | **SB**
- P14613 | StoryBit | Data/StoryBit/DarkMatter.lua :: DarkMatter :: [2].Effects[1].Field | loc O:26 / N:26 | Physics → Hi-Tech | **SB**
- P14614 | StoryBit | Data/StoryBit/DarkMatter.lua :: DarkMatter :: [2].Text | loc O:26 / N:26 | T(770227749350, "The scientists are happy that they can keep using th... → T(770227749350, "The scientists are happy that they can keep using th... | **SB**
- P14756 | StoryBit | Data/StoryBit/DormantLife_FollowUp2.lua :: DormantLife_FollowUp2 :: [1].CustomOutcomeText | loc O:29 / N:29 | T(388743962939, "research boost by 5% in the Biotech Field") → T(388743962939, "Habitation techs boost next Tech Point by 5% ") | **SB**
- P14888 | StoryBit | Data/StoryBit/DustSickness_Cure.lua :: DustSickness_Cure :: [1].CustomOutcomeText | loc O:45 / N:46 | T(105294187788, "Colonists with Dust Sickness lose <abs(comfort_penal... → T(105294187788, "Colonists with Dust Sickness lose <abs(comfort_penal... | **SB**
- P14894 | StoryBit | Data/StoryBit/DustSickness_Cure.lua :: DustSickness_Cure :: [3].CustomOutcomeText | loc O:45 / N:46 | T(725813827810, "Tech cost reduced by <tech_reduction_pay>%") → T(725813827810, "Tech boosted by <tech_reduction_pay>") | **SB**
- P14900 | StoryBit | Data/StoryBit/DustSickness_Cure.lua :: DustSickness_Cure :: [5].CustomOutcomeText | loc O:45 / N:46 | T(340073631258, "Tech cost reduced by <tech_reduction_pay>%") → T(340073631258, "Tech boosted by <tech_reduction_pay>") | **SB**
- P15326 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: Obsolete | loc O:35 / N:36 | <absent> → true | **SB**
- P15327 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [2].Effects[1].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15328 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [2].Effects[2].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15329 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [2].Effects[3].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15330 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [2].Effects[4].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15331 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [4].Effects[2].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15332 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [4].Effects[3].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15333 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [4].Effects[4].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15334 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [4].Effects[5].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15335 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [6].Effects[4].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15336 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [6].Effects[5].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15337 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [6].Effects[6].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15338 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [8].Effects[5].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15339 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [8].Effects[6].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15340 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [8].Effects[7].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15341 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: [8].Effects[9].Prop | loc O:35 / N:36 | service_comfort → Comfort | **SB**
- P15342 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: qa_info.__class | loc O:35 / N:36 | 'PresetQAInfo' → <absent> | **SB**
- P15343 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: qa_info.data[1].action | loc O:35 / N:36 | Modified → <absent> | **SB**
- P15344 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: qa_info.data[1].time | loc O:35 / N:36 | 1744628415 → <absent> | **SB**
- P15345 | StoryBit | Data/StoryBit/FoodFight.lua :: FoodFight :: qa_info.data[1].user | loc O:35 / N:36 | Lina → <absent> | **SB**
- P15346 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: Obsolete | loc O:33 / N:34 | <absent> → true | **SB**
- P15347 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [10].Effects[1].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15348 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [10].Effects[2].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15349 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [10].Effects[3].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15350 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [4].Effects[1].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15351 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [4].Effects[2].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15352 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [4].Effects[3].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15353 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [6].Effects[1].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15354 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [6].Effects[2].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15355 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [6].Effects[3].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15356 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [8].Effects[1].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15357 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [8].Effects[2].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15358 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: [8].Effects[3].Prop | loc O:33 / N:34 | service_comfort → Comfort | **SB**
- P15359 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.__class | loc O:33 / N:34 | 'PresetQAInfo' → <absent> | **SB**
- P15360 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[1].action | loc O:33 / N:34 | Modified → <absent> | **SB**
- P15361 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[1].time | loc O:33 / N:34 | 1637248193 → <absent> | **SB**
- P15362 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[2].action | loc O:33 / N:34 | Modified → <absent> | **SB**
- P15363 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[2].time | loc O:33 / N:34 | 1739976507 → <absent> | **SB**
- P15364 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[2].user | loc O:33 / N:34 | Lina → <absent> | **SB**
- P15365 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[3].action | loc O:33 / N:34 | Modified → <absent> | **SB**
- P15366 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[3].time | loc O:33 / N:34 | 1731659874 → <absent> | **SB**
- P15367 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[3].user | loc O:33 / N:34 | Lina → <absent> | **SB**
- P15368 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[4].action | loc O:33 / N:34 | Modified → <absent> | **SB**
- P15369 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[4].time | loc O:33 / N:34 | 1744628442 → <absent> | **SB**
- P15370 | StoryBit | Data/StoryBit/FoodFight_FollowUp.lua :: FoodFight_FollowUp :: qa_info.data[4].user | loc O:33 / N:34 | Lina → <absent> | **SB**
- P15381 | StoryBit | Data/StoryBit/ForeignerInAForeignLand_FollowUp1.lua :: ForeignerInAForeignLand_FollowUp1 :: [5].Effects[1].Field | loc O:33 / N:33 | Physics → Hi-Tech | **SB**
- P15384 | StoryBit | Data/StoryBit/ForeignerInAForeignLand_FollowUp1.lua :: ForeignerInAForeignLand_FollowUp1 :: [8].Effects[1].Field | loc O:33 / N:33 | Physics → Hi-Tech | **SB**
- P16063 | StoryBit | Data/StoryBit/InvestmentOpportunity_GreatReturn.lua :: InvestmentOpportunity_GreatReturn :: Text | loc O:33 / N:33 | T(333547415315, "We stand to gain <return>% return on our initial inv... → T(333547415315, "We stand to gain <percent(return)> return on our ini... | **SB**
- P16594 | StoryBit | Data/StoryBit/LongWinter_BigExtension_NoTech.lua :: LongWinter_BigExtension_NoTech :: Effects[1].Tech | loc O:54 / N:53 | SubsurfaceHeating → <absent> | **L3**
- P16625 | StoryBit | Data/StoryBit/LongWinter_MoraleEvent.lua :: LongWinter_MoraleEvent :: [3].CustomOutcomeText | loc O:33 / N:33 | T(284727608577, "Colonists will consume <food_increase>% more Food an... → T(284727608577, "Colonists will consume <percent(food_increase)> more... | **SB**
- P17176 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.__class | loc O:14 / N:14 | 'PresetQAInfo' → <absent> | **SB**
- P17177 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[1].action | loc O:14 / N:14 | Modified → <absent> | **SB**
- P17178 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[1].time | loc O:14 / N:14 | 1731003414 → <absent> | **SB**
- P17179 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[1].user | loc O:14 / N:14 | Assen → <absent> | **SB**
- P17180 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[2].action | loc O:14 / N:14 | Modified → <absent> | **SB**
- P17181 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[2].time | loc O:14 / N:14 | 1745486550 → <absent> | **SB**
- P17182 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[2].user | loc O:14 / N:14 | Lina → <absent> | **SB**
- P17183 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[3].action | loc O:14 / N:14 | Modified → <absent> | **SB**
- P17184 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[3].time | loc O:14 / N:14 | 1775126469 → <absent> | **SB**
- P17185 | StoryBit | Data/StoryBit/MysteryRocket_FoodGoneBad.lua :: MysteryRocket_FoodGoneBad :: qa_info.data[3].user | loc O:14 / N:14 | Lina → <absent> | **SB**
- P17216 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.__class | loc O:11 / N:11 | 'PresetQAInfo' → <absent> | **SB**
- P17217 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[1].action | loc O:11 / N:11 | Modified → <absent> | **SB**
- P17218 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[1].time | loc O:11 / N:11 | 1551087296 → <absent> | **SB**
- P17219 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[1].user | loc O:11 / N:11 | Radomir → <absent> | **SB**
- P17220 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[2].action | loc O:11 / N:11 | Modified → <absent> | **SB**
- P17221 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[2].time | loc O:11 / N:11 | 1731003414 → <absent> | **SB**
- P17222 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[2].user | loc O:11 / N:11 | Assen → <absent> | **SB**
- P17223 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[3].action | loc O:11 / N:11 | Modified → <absent> | **SB**
- P17224 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[3].time | loc O:11 / N:11 | 1745486718 → <absent> | **SB**
- P17225 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[3].user | loc O:11 / N:11 | Lina → <absent> | **SB**
- P17226 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[4].action | loc O:11 / N:11 | Modified → <absent> | **SB**
- P17227 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[4].time | loc O:11 / N:11 | 1775125362 → <absent> | **SB**
- P17228 | StoryBit | Data/StoryBit/MysteryRocket_TaintedFood.lua :: MysteryRocket_TaintedFood :: qa_info.data[4].user | loc O:11 / N:11 | Lina → <absent> | **SB**
- P17239 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.__class | loc O:18 / N:18 | 'PresetQAInfo' → <absent> | **SB**
- P17240 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[1].action | loc O:18 / N:18 | Modified → <absent> | **SB**
- P17241 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[1].time | loc O:18 / N:18 | 1731003414 → <absent> | **SB**
- P17242 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[1].user | loc O:18 / N:18 | Assen → <absent> | **SB**
- P17243 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[2].action | loc O:18 / N:18 | Modified → <absent> | **SB**
- P17244 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[2].time | loc O:18 / N:18 | 1745486766 → <absent> | **SB**
- P17245 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[2].user | loc O:18 / N:18 | Lina → <absent> | **SB**
- P17246 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[3].action | loc O:18 / N:18 | Modified → <absent> | **SB**
- P17247 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[3].time | loc O:18 / N:18 | 1768831936 → <absent> | **SB**
- P17248 | StoryBit | Data/StoryBit/MysteryRocket_Wait_FoodGoneBad.lua :: MysteryRocket_Wait_FoodGoneBad :: qa_info.data[3].user | loc O:18 / N:18 | Lina → <absent> | **SB**
- P17294 | StoryBit | Data/StoryBit/NewHorizons.lua :: NewHorizons :: [6].CustomOutcomeText | loc O:39 / N:40 | T(261696901616, "unlock a new Tech - <em>Gene Forging</em>") → T(261696901616, "unlock a new Breakthrough - <em>Gene Selection</em>") | **SB**
- P17297 | StoryBit | Data/StoryBit/NewHorizons.lua :: NewHorizons :: [7].Effects[1].Tech | loc O:39 / N:40 | GeneForging → GeneSelection | **SB**
- P17408 | StoryBit | Data/StoryBit/OverworkedGenius_GrantTech.lua :: OverworkedGenius_GrantTech :: Text | loc O:35 / N:28 | T(574513689394, "Short of breath and visibly excited, <DisplayName> e... → T(574513689394, "Short of breath and visibly excited, <DisplayName> e... | **SB**
- P17513 | StoryBit | Data/StoryBit/PersonalSpace.lua :: PersonalSpace :: [7].CustomOutcomeText | loc O:53 / N:48 | T(373007909943, "<em>Home Collective</em> Tech research cost reduction") → T(373007909943, "<em>Home Collective</em> Tech boosts next Tech Point") | **SB**
- P17582 | StoryBit | Data/StoryBit/Prototype_MediumDome_Success.lua :: Prototype_MediumDome_Success :: Text | loc O:28 / N:28 | T(922577396950, "Not only that, but their work has lead to important ... → T(922577396950, "Not only that, but their work has lead to important ... | **SB**
- P17621 | StoryBit | Data/StoryBit/Prototype_Reactor_Success.lua :: Prototype_Reactor_Success :: Text | loc O:29 / N:29 | T(614163462789, "Not only that, but their work has lead to important ... → T(614163462789, "Not only that, but their work has lead to important ... | **SB**
- P17665 | StoryBit | Data/StoryBit/Prototype_Scrubber_Success.lua :: Prototype_Scrubber_Success :: Text | loc O:29 / N:29 | T(857899493605, "Not only that, but their work has lead to important ... → T(857899493605, "Not only that, but their work has lead to important ... | **SB**
- P18288 | StoryBit | Data/StoryBit/Shocky_FollowUp3.lua :: Shocky_FollowUp3 :: [1].CustomOutcomeText | loc O:59 / N:59 | T(721256685409, "many Colonists lose Morale; reveal a random Physics ... → T(721256685409, "many Colonists lose Morale; unlock a random Hi-Tech ... | **SB**
- P18293 | StoryBit | Data/StoryBit/Shocky_FollowUp3.lua :: Shocky_FollowUp3 :: [2].Effects[2].Field | loc O:59 / N:59 | Physics → Hi-Tech | **SB**
- P18940 | StoryBit | Data/StoryBit/TheIncident_1_Aftermath_Explosion.lua :: TheIncident_1_Aftermath_Explosion :: Effects[1].Tech | loc O:55 / N:64 | <absent> → TheIncident | **SB**
- P18963 | StoryBit | Data/StoryBit/TheIncident_3_Aftermath_NoExplosion.lua :: TheIncident_3_Aftermath_NoExplosion :: Effects[1].Tech | loc O:42 / N:51 | <absent> → TheIncident | **L1**
- P19754 | StoryBit | Data/StoryBit/WindsOfChange_1_Expedition.lua :: WindsOfChange_1_Expedition :: [4].Text | loc O:33 / N:35 | T(186554687367, "Using the research output of the colony would help t... → T(186554687367, "Using the research output of the colony would help t... | **SB**
- P19755 | StoryBit | Data/StoryBit/WindsOfChange_1_Expedition.lua :: WindsOfChange_1_Expedition :: [8].Text | loc O:33 / N:35 | T(728201607140, "Meanwhile, the rogue nanites outside continue their ... → T(728201607140, "Meanwhile, the rogue nanites outside continue their ... | **SB**
- P19824 | StoryBit | Data/StoryBit/WindsOfChange_WaitRogueNaniteAnalysisTech.lua :: WindsOfChange_WaitRogueNaniteAnalysisTech :: Text | loc O:26 / N:27 | T(252316382326, "<effect>Your colony is well-informed on the properti... → T(252316382326, "<effect>Your colony is well-informed on the properti... | **SB**
- P19906 | StoryBit | Data/StoryBit/WithAGrainOfSalt.lua :: WithAGrainOfSalt :: [5].CustomOutcomeText | loc O:68 / N:60 | T(154468048268, "unlock a Tech for <resource(terr_veg_big,'Vegetation... → T(154468048268, "Unlock the Low-G Shrimp GMO Tech which gives <resour... | **SB**
- P09763 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [10].id | loc O:9 / N:9 | grazing_spot → ambient_life_suffix | **PD-A**
- P09764 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [10].items | loc O:9 / N:9 | function ( self , prop_meta , validate_fn ) return PastureGrazingSpot... → function ( self , prop_meta , validate_fn ) return AnimalAmbientLifeS... | **PD-A**
- P09765 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [10].name | loc O:9 / N:9 | Grazing spot → Ambient life suffix | **PD-A**
- P09766 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].__class | loc O:9 / N:9 | 'PropertyDefChoice' → 'PropertyDefPresetIdList' | **PD-A**
- P09767 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].add_prop | loc O:9 / N:9 | <absent> → true | **PD-A**
- P09768 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].id | loc O:9 / N:9 | ambient_life_suffix → OutputResources | **PD-A**
- P09770 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].name | loc O:9 / N:9 | Ambient life suffix → Output resources | **PD-A**
- P09771 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].preset_class | loc O:9 / N:9 | <absent> → Resource | **PD-A**
- P09772 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].preset_filter | loc O:9 / N:9 | <absent> → function ( preset , obj , prop_meta ) return not preset.is_group end | **PD-A**
- P09773 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].prop_default | loc O:9 / N:9 | <absent> → 1000 | **PD-A**
- P09774 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].prop_key | loc O:9 / N:9 | <absent> → amount | **PD-A**
- P09775 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].prop_name | loc O:9 / N:9 | <absent> → Amount | **PD-A**
- P09776 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].prop_scale | loc O:9 / N:9 | <absent> → res | **PD-A**
- P09777 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [11].value_key | loc O:9 / N:9 | <absent> → resource | **PD-A**
- P09778 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [9].__class | loc O:9 / N:9 | 'PropertyDefNumber' → 'PropertyDefChoice' | **PD-A**
- P09779 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [9].help | loc O:9 / N:9 | per animal → <absent> | **PD-A**
- P09780 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [9].id | loc O:9 / N:9 | food → grazing_spot | **PD-A**
- P09782 | PresetDef | Data/ClassDef-PresetDefs.lua :: Animal :: [9].name | loc O:9 / N:9 | Food amount → Grazing spot | **PD-A**
- P09793 | PresetDef | Data/ClassDef-PresetDefs.lua :: Cargo :: DefModItem | loc O:229 / N:249 | <absent> → true | **PD-O**
- P09794 | PresetDef | Data/ClassDef-PresetDefs.lua :: Cargo :: DefModItemName | loc O:229 / N:249 | <absent> → Cargo - Other | **PD-O**
- P09795 | PresetDef | Data/ClassDef-PresetDefs.lua :: Cargo :: DefModItemSubmenu | loc O:229 / N:249 | <absent> → Resources | **PD-O**
- P09796 | PresetDef | Data/ClassDef-PresetDefs.lua :: Cargo :: DefNameInEditor | loc O:229 / N:249 | <absent> → Other | **PD-O**
- P09797 | PresetDef | Data/ClassDef-PresetDefs.lua :: Cargo :: DefPresetClass | loc O:229 / N:249 | <absent> → Cargo | **PD-O**
- P09798 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoBuildingPrefab :: DefEditorName | loc O:338 / N:361 | Cargo → false | **PD-O**
- P09800 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoBuildingPrefab :: DefModItemName | loc O:338 / N:361 | <absent> → Cargo - Prefab | **PD-O**
- P09803 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoBuildingPrefab :: DefPresetClass | loc O:338 / N:361 | Cargo → <absent> | **PD-O**
- P09810 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefEditorName | loc O:418 / N:451 | Cargo → false | **PD-O**
- P09811 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefModItem | loc O:418 / N:451 | <absent> → true | **PD-O**
- P09812 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefModItemName | loc O:418 / N:451 | <absent> → Cargo - Resource | **PD-O**
- P09813 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefModItemSubmenu | loc O:418 / N:451 | <absent> → Resources | **PD-O**
- P09814 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefNameInEditor | loc O:418 / N:451 | <absent> → Resource | **PD-O**
- P09815 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: DefPresetClass | loc O:418 / N:451 | Cargo → <absent> | **PD-O**
- P09816 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: [2].translate | loc O:418 / N:451 | <absent> → false | **PD-O**
- P09817 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: [5].code | loc O:418 / N:451 | function ( self ) return self GetDescription ( ) end → function ( self ) return TTranslate ( self GetDescription ( ) ) end | **PD-O**
- P09818 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoResource :: [7].code | loc O:418 / N:451 | function ( self ) local def = Resources [ self.resource ] return def ... → function ( self ) local def = Resources [ self.resource ] return def ... | **PD-O**
- P09819 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoUnit :: DefEditorName | loc O:507 / N:544 | Cargo → false | **PD-O**
- P09821 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoUnit :: DefModItemName | loc O:507 / N:544 | <absent> → Cargo - Unit | **PD-O**
- P09824 | PresetDef | Data/ClassDef-PresetDefs.lua :: CargoUnit :: DefPresetClass | loc O:507 / N:544 | Cargo → <absent> | **PD-O**
- P09902 | PresetDef | Data/ClassDef-PresetDefs.lua :: CommanderProfilePreset :: [8].name | loc O:1024 / N:1063 | Bonus free Tech Anomalies → Bonus event Anomalies | **PD-O**
- P09907 | PresetDef | Data/ClassDef-PresetDefs.lua :: CommanderProfilePreset :: [9].name | loc O:1024 / N:1063 | Bonus Rockets → Bonus free Tech Anomalies | **PD-O**
- P09908 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [10].__class | loc O:1210 / N:1255 | 'PropertyDefNumber' → 'PropertyDefText' | **PD-C**
- P09909 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [10].default | loc O:1210 / N:1255 | 2880000 → empty | **PD-C**
- P09910 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [10].id | loc O:1210 / N:1255 | GrowthTime → GrowthSequence | **PD-C**
- P09911 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [10].name | loc O:1210 / N:1255 | Growth Time → Growth Sequence | **PD-C**
- P09914 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [11].__class | loc O:1210 / N:1255 | 'PropertyDefText' → 'PropertyDefNumber' | **PD-C**
- P09915 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [11].default | loc O:1210 / N:1255 | empty → 1000 | **PD-C**
- P09916 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [11].id | loc O:1210 / N:1255 | GrowthSequence → WaterDemand | **PD-C**
- P09917 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [11].name | loc O:1210 / N:1255 | Growth Sequence → Water Demand | **PD-C**
- P09920 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [12].id | loc O:1210 / N:1255 | WaterDemand → OxygenProduction | **PD-C**
- P09921 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [12].name | loc O:1210 / N:1255 | Water Demand → Oxygen Production | **PD-C**
- P09922 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [13].default | loc O:1210 / N:1255 | 1000 → 0 | **PD-C**
- P09923 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [13].id | loc O:1210 / N:1255 | OxygenProduction → SoilDemand | **PD-C**
- P09924 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [13].name | loc O:1210 / N:1255 | Oxygen Production → Soil Demand | **PD-C**
- P09926 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [14].id | loc O:1210 / N:1255 | SoilDemand → SoilEffect | **PD-C**
- P09927 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [14].name | loc O:1210 / N:1255 | Soil Demand → Soil Effect | **PD-C**
- P09928 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [15].id | loc O:1210 / N:1255 | SoilEffect → SoilQualityMin | **PD-C**
- P09929 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [15].name | loc O:1210 / N:1255 | Soil Effect → Soil Quality Min | **PD-C**
- P09930 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [16].default | loc O:1210 / N:1255 | 0 → 100 | **PD-C**
- P09931 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [16].id | loc O:1210 / N:1255 | SoilQualityMin → SoilQualityMax | **PD-C**
- P09932 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [16].name | loc O:1210 / N:1255 | Soil Quality Min → Soil Quality Max | **PD-C**
- P09933 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [17].__class | loc O:1210 / N:1255 | 'PropertyDefNumber' → 'PropertyDefChoice' | **PD-C**
- P09934 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [17].default | loc O:1210 / N:1255 | 100 → empty | **PD-C**
- P09935 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [17].id | loc O:1210 / N:1255 | SoilQualityMax → FarmClass | **PD-C**
- P09937 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [17].name | loc O:1210 / N:1255 | Soil Quality Max → Farm Class | **PD-C**
- P09938 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [18].id | loc O:1210 / N:1255 | FarmClass → CropEntity | **PD-C**
- P09939 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [18].items | loc O:1210 / N:1255 | function ( self , prop_meta , validate_fn ) return ClassDescendantsCo... → function ( self , prop_meta , validate_fn ) return GetCropEntities ( ... | **PD-C**
- P09940 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [18].name | loc O:1210 / N:1255 | Farm Class → Entity | **PD-C**
- P09941 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [19].__class | loc O:1210 / N:1255 | 'PropertyDefChoice' → 'PropertyDefFunc' | **PD-C**
- P09943 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [19].id | loc O:1210 / N:1255 | CropEntity → OnProduce | **PD-C**
- P09945 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [19].name | loc O:1210 / N:1255 | Entity → Produce | **PD-C**
- P09947 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [20].__class | loc O:1210 / N:1255 | 'PropertyDefFunc' → 'PropertyDefChoice' | **PD-C**
- P09949 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [20].id | loc O:1210 / N:1255 | OnProduce → modify_target | **PD-C**
- P09951 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [20].name | loc O:1210 / N:1255 | Produce → Modifier target | **PD-C**
- P09953 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [21].id | loc O:1210 / N:1255 | modify_target → modify_property | **PD-C**
- P09954 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [21].items | loc O:1210 / N:1255 | function ( self , prop_meta , validate_fn ) return { "" , "dome" , "f... → function ( self , prop_meta , validate_fn ) return ModifiablePropsCom... | **PD-C**
- P09955 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [21].name | loc O:1210 / N:1255 | Modifier target → Modified property | **PD-C**
- P09956 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [22].__class | loc O:1210 / N:1255 | 'PropertyDefChoice' → 'PropertyDefNumber' | **PD-C**
- P09957 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [22].default | loc O:1210 / N:1255 | empty → 0 | **PD-C**
- P09958 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [22].id | loc O:1210 / N:1255 | modify_property → modify_amount | **PD-C**
- P09960 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [22].name | loc O:1210 / N:1255 | Modified property → Modification amount | **PD-C**
- P09961 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [23].id | loc O:1210 / N:1255 | modify_amount → modify_percent | **PD-C**
- P09962 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [23].name | loc O:1210 / N:1255 | Modification amount → Modification percent | **PD-C**
- P09963 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [24].__class | loc O:1210 / N:1255 | 'PropertyDefNumber' → 'ClassMethodDef' | **PD-C**
- P09967 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [24].name | loc O:1210 / N:1255 | Modification percent → SetLocked | **PD-C**
- P09973 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].__class | loc O:1210 / N:1255 | 'PropertyDefNumber' → 'PropertyDefPresetIdList' | **PD-C**
- P09974 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].add_prop | loc O:1210 / N:1255 | <absent> → true | **PD-C**
- P09977 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].id | loc O:1210 / N:1255 | FoodOutput → OutputResources | **PD-C**
- P09978 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].name | loc O:1210 / N:1255 | Food Output → Output resources | **PD-C**
- P09980 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].preset_filter | loc O:1210 / N:1255 | <absent> → function ( preset , obj , prop_meta ) return not preset.is_group and ... | **PD-C**
- P09981 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].prop_default | loc O:1210 / N:1255 | <absent> → 1000 | **PD-C**
- P09982 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].prop_key | loc O:1210 / N:1255 | <absent> → amount | **PD-C**
- P09983 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].prop_name | loc O:1210 / N:1255 | <absent> → Amount | **PD-C**
- P09984 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].prop_scale | loc O:1210 / N:1255 | <absent> → res | **PD-C**
- P09986 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [5].value_key | loc O:1210 / N:1255 | <absent> → resource | **PD-C**
- P09987 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [6].__class | loc O:1210 / N:1255 | 'PropertyDefPresetId' → 'PropertyDefBool' | **PD-C**
- P09988 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [6].default | loc O:1210 / N:1255 | Food → <absent> | **PD-C**
- P09990 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [6].id | loc O:1210 / N:1255 | ResourceType → Locked | **PD-C**
- P09993 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [7].__class | loc O:1210 / N:1255 | 'PropertyDefBool' → 'PropertyDefNumber' | **PD-C**
- P09996 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [7].id | loc O:1210 / N:1255 | Locked → InitialGrowthTime | **PD-C**
- P09997 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [7].name | loc O:1210 / N:1255 | Locked → Initial Growth Time | **PD-C**
- P09999 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [8].__class | loc O:1210 / N:1255 | 'PropertyDefNumber' → 'PropertyDefText' | **PD-C**
- P10000 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [8].default | loc O:1210 / N:1255 | 2880000 → empty | **PD-C**
- P10001 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [8].id | loc O:1210 / N:1255 | InitialGrowthTime → InitialGrowthSequence | **PD-C**
- P10002 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [8].name | loc O:1210 / N:1255 | Initial Growth Time → Initial Growth Sequence | **PD-C**
- P10005 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [9].__class | loc O:1210 / N:1255 | 'PropertyDefText' → 'PropertyDefNumber' | **PD-C**
- P10006 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [9].default | loc O:1210 / N:1255 | empty → 2880000 | **PD-C**
- P10007 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [9].id | loc O:1210 / N:1255 | InitialGrowthSequence → GrowthTime | **PD-C**
- P10008 | PresetDef | Data/ClassDef-PresetDefs.lua :: CropPreset :: [9].name | loc O:1210 / N:1255 | Initial Growth Sequence → Growth Time | **PD-C**
- P10055 | PresetDef | Data/ClassDef-Default.lua :: FlightPolicyDef :: DefModItemName | loc O:12 / N:13 | FlightPolicyModItem → Flight Policy | **PD-O**
- P10064 | PresetDef | Data/ClassDef-Factions.lua :: LawDef :: <preset> | loc O:2445 / N:absent | <removed> → empty | **PD-O**
- P10080 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [12].help | loc O:1632 / N:1742 | Applicants earned for each Breakthrough Tech researched → Planetary events reduce fee | **PD-O**
- P10088 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [13].name | loc O:1632 / N:1742 | Cargo Capacity → Breakthrough applicants | **PD-O**
- P10091 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [14].name | loc O:1632 / N:1742 | Starting Rockets → Cargo Capacity | **PD-O**
- P10128 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [22].name | loc O:1632 / N:1742 | Bonus free Tech Anomalies → Bonus event Anomalies | **PD-O**
- P10134 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [23].name | loc O:1632 / N:1742 | Additional research points per Sol → Bonus free Tech Anomalies | **PD-O**
- P10240 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [46].category | loc O:1632 / N:1742 | Cargo Weight/Cost Modification → General | **PD-O**
- P10246 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [47].category | loc O:1632 / N:1742 | Cargo Weight/Cost Modification → General | **PD-O**
- P10251 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [48].category | loc O:1632 / N:1742 | Cargo Weight/Cost Modification → General | **PD-O**
- P10269 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [50].category | loc O:1632 / N:1742 | Parameters → Cargo Weight/Cost Modification | **PD-O**
- P10275 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [51].category | loc O:1632 / N:1742 | Parameters → Cargo Weight/Cost Modification | **PD-O**
- P10281 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [52].category | loc O:1632 / N:1742 | Parameters → Cargo Weight/Cost Modification | **PD-O**
- P10406 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [70].code | loc O:1632 / N:1742 | function ( self , properties ) for i = 1 , const.MissionSponsorPriceM... → <absent> | **PD-O**
- P10435 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [74].code | loc O:1632 / N:1742 | function ( self ) if not self.faction and not s_AllowedMissionSponsor... → function ( self , properties ) for i = 1 , const.MissionSponsorPriceM... | **PD-O**
- P10461 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [7].name | loc O:1632 / N:1742 | Tech Funding (M) → Starting Funding (M) | **PD-O**
- P10462 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [8].help | loc O:1632 / N:1742 | Funding earned for each Breakthrough Tech researched → Funding earned for each Tech researched | **PD-O**
- P10464 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [8].name | loc O:1632 / N:1742 | Breakthrough Funding (M) → Tech Funding (M) | **PD-O**
- P10468 | PresetDef | Data/ClassDef-PresetDefs.lua :: MissionSponsorPreset :: [9].help | loc O:1632 / N:1742 | Pay a lump sum to the sponsor → Funding earned for each Breakthrough Tech researched | **PD-O**
- P10485 | PresetDef | Data/ClassDef-PresetDefs.lua :: POI :: [14].items | loc O:2223 / N:2361 | function ( self , prop_meta , validate_fn ) return PresetsCombo ( "Te... → function ( self , prop_meta , validate_fn ) return PresetsCombo ( "Te... | **PD-O**
- P10496 | PresetDef | Data/ClassDef-PresetDefs.lua :: PlanetaryAnomalyDescription :: [8].value | loc O:2369 / N:2515 | <absent> → A description text for planetary anomalies. An anomaly that has no cu... | **PD-O**
- P10498 | PresetDef | Data/ClassDef-Factions.lua :: PolicyDef :: <preset> | loc O:3385 / N:absent | <removed> → empty | **PD-O**
- P10574 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechFieldPreset :: [3].help | loc O:2744 / N:3101 | Required Research Points For Each Tech Slot → <absent> | **PD-T**
- P10596 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].FuncName | loc O:2837 / N:3120 | TechEditor_Reveal → <absent> | **PD-T**
- P10597 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].Icon | loc O:2837 / N:3120 | CommonAssets/UI/Ged/Plus.png → <absent> | **PD-T**
- P10598 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].Menubar | loc O:2837 / N:3120 | Debug → <absent> | **PD-T**
- P10599 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].Name | loc O:2837 / N:3120 | Reveal selected tech → <absent> | **PD-T**
- P10600 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].Rollover | loc O:2837 / N:3120 | Reveal selected tech → <absent> | **PD-T**
- P10601 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[1].__class | loc O:2837 / N:3120 | 'EditorCustomActionDef' → <absent> | **PD-T**
- P10602 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].FuncName | loc O:2837 / N:3120 | TechEditor_Research → <absent> | **PD-T**
- P10603 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].Icon | loc O:2837 / N:3120 | CommonAssets/UI/Ged/play.tga → <absent> | **PD-T**
- P10604 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].Menubar | loc O:2837 / N:3120 | Debug → <absent> | **PD-T**
- P10605 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].Name | loc O:2837 / N:3120 | Reveal and research selected tech → <absent> | **PD-T**
- P10606 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].Rollover | loc O:2837 / N:3120 | Reveal and research selected tech → <absent> | **PD-T**
- P10607 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorCustomActions[2].__class | loc O:2837 / N:3120 | 'EditorCustomActionDef' → <absent> | **PD-T**
- P10608 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorName | loc O:2837 / N:3120 | Techs → <absent> | **PD-T**
- P10609 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefEditorShortcut | loc O:2837 / N:3120 | Ctrl-Alt-T → <absent> | **PD-T**
- P10610 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefHasObsolete | loc O:2837 / N:3120 | <absent> → true | **PD-T**
- P10611 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefHasSortKey | loc O:2837 / N:3120 | true → <absent> | **PD-T**
- P10612 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: DefParentClassList[3] | loc O:2837 / N:3120 | GameEffectsContainer → <absent> | **PD-T**
- P10613 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [10].__class | loc O:2837 / N:3120 | 'PropertyDefFunc' → <absent> | **PD-T**
- P10614 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [10].category | loc O:2837 / N:3120 | Tech → <absent> | **PD-T**
- P10615 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [10].id | loc O:2837 / N:3120 | OnResearched → <absent> | **PD-T**
- P10616 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [10].params | loc O:2837 / N:3120 | self, research, first_time → <absent> | **PD-T**
- P10617 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [11].__class | loc O:2837 / N:3120 | 'PropertyDefText' → <absent> | **PD-T**
- P10619 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [11].id | loc O:2837 / N:3120 | param1comment → <absent> | **PD-T**
- P10620 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [11].name | loc O:2837 / N:3120 | Param 1 Comment → <absent> | **PD-T**
- P10621 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [11].translate | loc O:2837 / N:3120 | false → <absent> | **PD-T**
- P10627 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [13].__class | loc O:2837 / N:3120 | 'PropertyDefText' → <absent> | **PD-T**
- P10629 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [13].id | loc O:2837 / N:3120 | param2comment → <absent> | **PD-T**
- P10630 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [13].name | loc O:2837 / N:3120 | Param 2 Comment → <absent> | **PD-T**
- P10631 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [13].translate | loc O:2837 / N:3120 | false → <absent> | **PD-T**
- P10637 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [15].__class | loc O:2837 / N:3120 | 'PropertyDefText' → <absent> | **PD-T**
- P10639 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [15].id | loc O:2837 / N:3120 | param3comment → <absent> | **PD-T**
- P10640 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [15].name | loc O:2837 / N:3120 | Param 3 Comment → <absent> | **PD-T**
- P10641 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [15].translate | loc O:2837 / N:3120 | false → <absent> | **PD-T**
- P10647 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [17].__class | loc O:2837 / N:3120 | 'PropertyDefText' → <absent> | **PD-T**
- P10649 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [17].id | loc O:2837 / N:3120 | param4comment → <absent> | **PD-T**
- P10650 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [17].name | loc O:2837 / N:3120 | Param 4 Comment → <absent> | **PD-T**
- P10651 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [17].translate | loc O:2837 / N:3120 | false → <absent> | **PD-T**
- P10657 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [19].__class | loc O:2837 / N:3120 | 'PropertyDefText' → <absent> | **PD-T**
- P10659 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [19].id | loc O:2837 / N:3120 | param5comment → <absent> | **PD-T**
- P10660 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [19].name | loc O:2837 / N:3120 | Param 5 Comment → <absent> | **PD-T**
- P10661 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [19].translate | loc O:2837 / N:3120 | false → <absent> | **PD-T**
- P10662 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].__class | loc O:2837 / N:3120 | 'PropertyDefText' → 'PropertyDefNumber' | **PD-T**
- P10663 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].category | loc O:2837 / N:3120 | Tech → Params | **PD-T**
- P10664 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].default | loc O:2837 / N:3120 | T(3900, "<no name>") → 0 | **PD-T**
- P10665 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].help | loc O:2837 / N:3120 | Tech Game Name - translated string → <absent> | **PD-T**
- P10666 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].id | loc O:2837 / N:3120 | display_name → param1 | **PD-T**
- P10667 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [1].name | loc O:2837 / N:3120 | Display Name → Param 1 | **PD-T**
- P10674 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].category | loc O:2837 / N:3120 | City → <absent> | **PD-T**
- P10676 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].dont_save | loc O:2837 / N:3120 | true → <absent> | **PD-T**
- P10677 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].help | loc O:2837 / N:3120 | Research cost. Depends on the tech field costs table and the tech pos... → <absent> | **PD-T**
- P10678 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].id | loc O:2837 / N:3120 | cost → <absent> | **PD-T**
- P10679 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].name | loc O:2837 / N:3120 | Research Cost → <absent> | **PD-T**
- P10680 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [21].read_only | loc O:2837 / N:3120 | true → <absent> | **PD-T**
- P10683 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [22].help | loc O:2837 / N:3120 | This tech will get initialized with the selected mystery, non mystery... → <absent> | **PD-T**
- P10686 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [22].name | loc O:2837 / N:3120 | From Mystery → <absent> | **PD-T**
- P10687 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [23].__class | loc O:2837 / N:3120 | 'ClassMethodDef' → <absent> | **PD-T**
- P10688 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [23].code | loc O:2837 / N:3120 | function ( self ) local field = TechFields [ self.group ] return fiel... → <absent> | **PD-T**
- P10689 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [23].name | loc O:2837 / N:3120 | GetFieldDisplayName → <absent> | **PD-T**
- P10690 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [24].__class | loc O:2837 / N:3120 | 'ClassMethodDef' → <absent> | **PD-T**
- P10691 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [24].code | loc O:2837 / N:3120 | function ( self ) local field = TechFields [ self.group ] return fiel... → <absent> | **PD-T**
- P10692 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [24].name | loc O:2837 / N:3120 | GetFieldDescription → <absent> | **PD-T**
- P10693 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [25].__class | loc O:2837 / N:3120 | 'ClassMethodDef' → <absent> | **PD-T**
- P10694 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [25].code | loc O:2837 / N:3120 | function ( self ) if UIColony then local id , points , cost , researc... → <absent> | **PD-T**
- P10695 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [25].name | loc O:2837 / N:3120 | Getcost → <absent> | **PD-T**
- P10696 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [26].__class | loc O:2837 / N:3120 | 'ClassMethodDef' → <absent> | **PD-T**
- P10697 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [26].code | loc O:2837 / N:3120 | function ( self , queue_idx ) return UIColony ResearchQueueCost ( sel... → <absent> | **PD-T**
- P10698 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [26].name | loc O:2837 / N:3120 | ResearchQueueCost → <absent> | **PD-T**
- P10699 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [26].params | loc O:2837 / N:3120 | queue_idx → <absent> | **PD-T**
- P10700 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [27].__class | loc O:2837 / N:3120 | 'ClassMethodDef' → <absent> | **PD-T**
- P10701 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [27].code | loc O:2837 / N:3120 | function ( self ) for _ , effect in ipairs ( self ) do procall ( effe... → <absent> | **PD-T**
- P10702 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [27].name | loc O:2837 / N:3120 | OnDataLoaded → <absent> | **PD-T**
- P10703 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].__class | loc O:2837 / N:3120 | 'PropertyDefUIImage' → 'PropertyDefNumber' | **PD-T**
- P10704 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].category | loc O:2837 / N:3120 | Tech → Params | **PD-T**
- P10705 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].default | loc O:2837 / N:3120 | UI/Icons/Research/rm_available.png → 0 | **PD-T**
- P10706 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].help | loc O:2837 / N:3120 | Tech Game Icon → <absent> | **PD-T**
- P10707 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].id | loc O:2837 / N:3120 | icon → param2 | **PD-T**
- P10708 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [2].name | loc O:2837 / N:3120 | Icon → Param 2 | **PD-T**
- P10709 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].__class | loc O:2837 / N:3120 | 'PropertyDefText' → 'PropertyDefNumber' | **PD-T**
- P10710 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].category | loc O:2837 / N:3120 | Tech → Params | **PD-T**
- P10712 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].help | loc O:2837 / N:3120 | Tech Description - translated text → <absent> | **PD-T**
- P10713 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].id | loc O:2837 / N:3120 | description → param3 | **PD-T**
- P10714 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].lines | loc O:2837 / N:3120 | 3 → <absent> | **PD-T**
- P10715 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [3].name | loc O:2837 / N:3120 | Description → Param 3 | **PD-T**
- P10716 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].__class | loc O:2837 / N:3120 | 'PropertyDefText' → 'PropertyDefNumber' | **PD-T**
- P10717 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].category | loc O:2837 / N:3120 | Tech → Params | **PD-T**
- P10719 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].help | loc O:2837 / N:3120 | Short Tech Description - translated text → <absent> | **PD-T**
- P10720 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].id | loc O:2837 / N:3120 | short_description → param4 | **PD-T**
- P10721 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].lines | loc O:2837 / N:3120 | 3 → <absent> | **PD-T**
- P10722 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [4].name | loc O:2837 / N:3120 | Short Description → Param 4 | **PD-T**
- P10723 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].__class | loc O:2837 / N:3120 | 'PropertyDefRange' → 'PropertyDefNumber' | **PD-T**
- P10724 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].category | loc O:2837 / N:3120 | Tech → Params | **PD-T**
- P10725 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].default | loc O:2837 / N:3120 | range(1, 100) → 0 | **PD-T**
- P10726 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].help | loc O:2837 / N:3120 | Shuffle slot range → <absent> | **PD-T**
- P10727 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].id | loc O:2837 / N:3120 | position → param5 | **PD-T**
- P10728 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].max | loc O:2837 / N:3120 | 100 → <absent> | **PD-T**
- P10729 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].min | loc O:2837 / N:3120 | 1 → <absent> | **PD-T**
- P10730 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [5].name | loc O:2837 / N:3120 | Unlock Position → Param 5 | **PD-T**
- P10731 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [6].__class | loc O:2837 / N:3120 | 'PropertyDefBool' → 'PropertyDefCombo' | **PD-T**
- P10732 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [6].category | loc O:2837 / N:3120 | Tech → Mystery | **PD-T**
- P10733 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [6].help | loc O:2837 / N:3120 | Can be researched multiple times → <absent> | **PD-T**
- P10734 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [6].id | loc O:2837 / N:3120 | repeatable → mystery | **PD-T**
- P10736 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [6].name | loc O:2837 / N:3120 | Research Repeatable → <absent> | **PD-T**
- P10738 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [7].category | loc O:2837 / N:3120 | Tech → <absent> | **PD-T**
- P10739 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [7].default | loc O:2837 / N:3120 | 10 → <absent> | **PD-T**
- P10740 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [7].help | loc O:2837 / N:3120 | Base research cost increase for repeatable techs → <absent> | **PD-T**
- P10741 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [7].id | loc O:2837 / N:3120 | cost_increase → <absent> | **PD-T**
- P10742 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [7].name | loc O:2837 / N:3120 | Repeat Cost Increase (%) → <absent> | **PD-T**
- P10743 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].__class | loc O:2837 / N:3120 | 'PropertyDefExpression' → <absent> | **PD-T**
- P10744 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].category | loc O:2837 / N:3120 | Tech → <absent> | **PD-T**
- P10745 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].default | loc O:2837 / N:3120 | function ( self ) return true end → <absent> | **PD-T**
- P10746 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].help | loc O:2837 / N:3120 | returns whether the technology should be used in the tech tree → <absent> | **PD-T**
- P10747 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].id | loc O:2837 / N:3120 | condition → <absent> | **PD-T**
- P10748 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [8].name | loc O:2837 / N:3120 | Condition → <absent> | **PD-T**
- P10749 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [9].__class | loc O:2837 / N:3120 | 'PropertyDefFunc' → <absent> | **PD-T**
- P10750 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [9].category | loc O:2837 / N:3120 | Tech → <absent> | **PD-T**
- P10751 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [9].id | loc O:2837 / N:3120 | OnDiscovered → <absent> | **PD-T**
- P10752 | PresetDef | Data/ClassDef-PresetDefs.lua :: TechPreset :: [9].params | loc O:2837 / N:3120 | self, research → <absent> | **PD-T**
- P10759 | PresetDef | Data/ClassDef-PresetDefs.lua :: Vegetation :: [22].name | loc O:3407 / N:3311 | Output Resource → Output resources | **PD-V**
- P10768 | PresetDef | Data/ClassDef-PresetDefs.lua :: Vegetation :: [23].name | loc O:3407 / N:3311 | Output Amount → Placement Consumption | **PD-V**
- P10772 | PresetDef | Data/ClassDef-PresetDefs.lua :: Vegetation :: [24].name | loc O:3407 / N:3311 | Placement Consumption → Add Local Soil Quality On Grown | **PD-V**
- P05907 | Label | Data/Label.lua :: Data/Label.lua#28 :: [2] | loc O:133 / N:133 | FoodProducers → FactoryBuildingWorkplaces | **MAL**
- P05908 | Label | Data/Label.lua :: Data/Label.lua#28 :: [4] | loc O:133 / N:133 | T(876111165575, "Food producer") → T(792038414265, "Staffed Factories") | **MAL**
- P05911 | Label | Data/Label.lua :: Data/Label.lua#30 :: [2] | loc O:143 / N:143 | Homeless → FoodProducers | **MAL**
- P05912 | Label | Data/Label.lua :: Data/Label.lua#30 :: [4] | loc O:143 / N:143 | T(5435, "Homeless Colonists") → T(876111165575, "Food producer") | **MAL**
- P05915 | Label | Data/Label.lua :: Data/Label.lua#31 :: [2] | loc O:149 / N:148 | HostileAttackRovers → FoodService | **MAL**
- P05916 | Label | Data/Label.lua :: Data/Label.lua#32 :: [2] | loc O:153 / N:152 | InsideFarm → Frozen | **MAL**
- P05917 | Label | Data/Label.lua :: Data/Label.lua#32 :: [4] | loc O:153 / N:152 | T(734467311949, "Inside Farms") → T(5434, "Frozen Buildings") | **MAL**
- P05923 | Label | Data/Label.lua :: Data/Label.lua#35 :: [2] | loc O:167 / N:167 | LowQualityResidence → InsideFarm | **MAL**
- P05924 | Label | Data/Label.lua :: Data/Label.lua#35 :: [4] | loc O:167 / N:167 | T(413652480882, "Low quality residences") → T(734467311949, "Inside Farms") | **MAL**
- P05952 | Label | Data/Label.lua :: Data/Label.lua#48 :: [4] | loc O:225 / N:226 | T(5437, "Resource Exploiter") → <absent> | **MAL**
- P05959 | Label | Data/Label.lua :: Data/Label.lua#51 :: [4] | loc O:238 / N:239 | <absent> → T(5437, "Resource Exploiter") | **MAL**
- P05973 | Label | Data/Label.lua :: Data/Label.lua#56 :: [2] | loc O:262 / N:262 | ServiceBuildings → SecurityBuildings | **MAL**
- P05980 | Label | Data/Label.lua :: Data/Label.lua#59 :: [2] | loc O:277 / N:276 | SoilRemove → ServiceBuildings | **MAL**
- P11765 | SA_Exec | Data/Scenario/Mystery 1.lua :: Data/Scenario/Mystery 1.lua#17 :: [2] | loc O:1423 / N:1423 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11766 | SA_Exec | Data/Scenario/Mystery 10.lua :: Data/Scenario/Mystery 10.lua#22 :: [4] | loc O:532 / N:532 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11768 | SA_Exec | Data/Scenario/Mystery 11.lua :: Data/Scenario/Mystery 11.lua#30 :: [4] | loc O:917 / N:917 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11769 | SA_Exec | Data/Scenario/Mystery 12.lua :: Data/Scenario/Mystery 12.lua#30 :: [4] | loc O:621 / N:621 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11817 | SA_Exec | Data/Scenario/Mystery 3.lua :: Data/Scenario/Mystery 3.lua#6 :: [2] | loc O:339 / N:339 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11822 | SA_Exec | Data/Scenario/Mystery 4.lua :: Data/Scenario/Mystery 4.lua#9 :: [2] | loc O:810 / N:810 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11823 | SA_Exec | Data/Scenario/Mystery 5.lua :: Data/Scenario/Mystery 5.lua#13 :: [2] | loc O:693 / N:693 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11824 | SA_Exec | Data/Scenario/Mystery 6.lua :: Data/Scenario/Mystery 6.lua#38 :: [2] | loc O:1023 / N:1023 | _grantedTech = TechDef[tech_id].display_name → _grantedTech = Techs[tech_id].DisplayName | **SX**
- P11840 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#15 :: [2] | loc O:568 / N:441 | 'local rockets = table.copy(MainCity.labels.TradeRocket or empty_tabl... → _RocketCounter = 0 | **MAL**
- P11853 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#19 :: [2] | loc O:623 / N:584 | 'UnlockImport("Polymers", "ResupplyCutoff")' → 'local rockets = table.copy(MainCity.labels.TradeRocket or empty_tabl... | **MAL**
- P11861 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#22 :: [2] | loc O:635 / N:635 | 'UnlockImport("Food", "ResupplyCutoff")' → 'UnlockImport("Concrete", "ResupplyCutoff")' | **MAL**
- P11871 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#26 :: [2] | loc O:691 / N:651 | _WarTension = _WarTension + ChoiceA_Tension → 'UnlockImport("Food", "ResupplyCutoff")' | **MAL**
- P11984 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#65 :: [2] | loc O:1342 / N:1260 | 'local rockets = table.copy(MainCity.labels.TradeRocket or empty_tabl... → _WarTension = _WarTension - TensionReduction | **MAL**
- P12007 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#71 :: [2] | loc O:1369 / N:1322 | 'UnlockImport("Food", "ResupplyCutoff")' → for telemetry | **MAL**
- P12013 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#73 :: [2] | loc O:1382 / N:1374 | 'ModifyResupplyParams("price", -50)' → 'local rockets = table.copy(MainCity.labels.TradeRocket or empty_tabl... | **MAL**
- P12024 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#79 :: [2] | loc O:1425 / N:1401 | 'UnlockImport("MachineParts", "ResupplyCutoff")' → 'UnlockImport("Food", "ResupplyCutoff")' | **MAL**
- P12025 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#80 :: [2] | loc O:1429 / N:1405 | 'UnlockImport("Food", "ResupplyCutoff")' → 'ModifyResupplyParams("price", 50)' | **MAL**
- P12032 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#83 :: [2] | loc O:1491 / N:1441 | 'local rockets = table.copy(MainCity.labels.TradeRocket or empty_tabl... → 'UnlockImport("Metals", "ResupplyCutoff")' | **MAL**
- P12042 | SA_Exec | Data/Scenario/Mystery 7.lua :: Data/Scenario/Mystery 7.lua#85 :: [4] | loc O:1516 / N:1449 | _grantedTech = TechDef[tech_id].display_name → true | **MAL**
- P12063 | SA_Exec | Data/Scenario/Mystery 8.lua :: Data/Scenario/Mystery 8.lua#31 :: [4] | loc O:1133 / N:1107 | _grantedTech = TechDef[tech_id].display_name → tech_id = GrantWonderTech() | **MAL**
- P12094 | SA_Exec | Data/Scenario/Mystery 9.lua :: Data/Scenario/Mystery 9.lua#29 :: [2] | loc O:864 / N:854 | 'UnlockCrop("Mystery9_GanymedeRice")' → Reward = 10 | **MAL**
- P12097 | SA_Exec | Data/Scenario/Mystery 9.lua :: Data/Scenario/Mystery 9.lua#31 :: [2] | loc O:915 / N:912 | 'UIColony:ChangeTechRepeatable("SolExploration", false)' → 'UnlockCrop("Mystery9_GanymedeRice")' | **MAL**
- P12144 | SA_Exec | Data/Scenario/Mystery 9.lua :: Data/Scenario/Mystery 9.lua#42 :: [4] | loc O:1127 / N:1161 | _grantedTech = TechDef[tech_id].display_name → 'Msg("MysteryEnd", "failed")' | **MAL**
- P12237 | SA_GrantTechBoost | Data/Scenario/GenericAnomalies.lua :: Data/Scenario/GenericAnomalies.lua#3 :: [2] | loc O:100 / N:100 | Physics → Hi-Tech | **SG**
- P12240 | SA_GrantTechBoost | Data/Scenario/GenericAnomalies.lua :: Data/Scenario/GenericAnomalies.lua#6 :: [2] | loc O:166 / N:166 | Physics → Hi-Tech | **SG**
- P12245 | SA_GrantTechBoost | Data/Scenario/MarsAnomalies.lua :: Data/Scenario/MarsAnomalies.lua#3 :: [2] | loc O:307 / N:307 | Physics → Hi-Tech | **SG**
- P12251 | SA_GrantTechBoost | Data/Scenario/Mystery 9.lua :: Data/Scenario/Mystery 9.lua#2 :: [2] | loc O:822 / N:870 | Physics → Hi-Tech | **SG**
- P12328 | SA_WaitChoice | Data/Scenario/MarsAnomalies.lua :: Data/Scenario/MarsAnomalies.lua#3 :: [12] | loc O:290 / N:290 | T(5803, "Conduct on-site volatiles experiments. (Reduce cost of Physi... → T(5803, "Conduct on-site volatiles experiments. (Boosts all Hi-Tech t... | **SC**
- P12338 | SA_WaitChoice | Data/Scenario/UndergroundAnomalies.lua :: Data/Scenario/UndergroundAnomalies.lua#2 :: [10] | loc O:92 / N:99 | T(13460, "Research the asteroid and use the findings to develop new t... → T(13460, "Research the asteroid and use the findings to develop new t... | **SC**
- P12399 | SA_WaitMessage | Data/Scenario/BuriedWonder_Ancient_Artifact.lua :: Data/Scenario/BuriedWonder_Ancient_Artifact.lua#1 :: [4] | loc O:13 / N:13 | T(13131, "Our Explorer vehicle's systems blacked out. All attempts to... → T(13131, "Our Explorer vehicle's systems blacked out. All attempts to... | **SW**
- P12403 | SA_WaitMessage | Data/Scenario/BuriedWonder_Bottomless_Pit.lua :: Data/Scenario/BuriedWonder_Bottomless_Pit.lua#1 :: [4] | loc O:13 / N:13 | T(13162, "We discovered what appears to be an enormous pit. The engin... → T(13162, "We discovered what appears to be an enormous pit. The engin... | **SW**
- P12414 | SA_WaitMessage | Data/Scenario/GenericAnomalies.lua :: Data/Scenario/GenericAnomalies.lua#1 :: [6] | loc O:92 / N:92 | T(5790, "The contrast with the red Martian dust made them appear almo... → T(5790, "The contrast with the red Martian dust made them appear almo... | **SW**
- P12417 | SA_WaitMessage | Data/Scenario/GenericAnomalies.lua :: Data/Scenario/GenericAnomalies.lua#5 :: [6] | loc O:158 / N:158 | T(5814, "Mankind's ingenuity had found a myriad of applications for i... → T(5814, "Mankind's ingenuity had found a myriad of applications for i... | **SW**
- P12429 | SA_WaitMessage | Data/Scenario/Mystery 2.lua :: Data/Scenario/Mystery 2.lua#18 :: [6] | loc O:1427 / N:1421 | T(6005, "The problem is the lack of information - so far, we know ver... → T(6005, "The problem is the lack of information - so far, we know ver... | **SW**
- P12431 | SA_WaitMessage | Data/Scenario/Mystery 2.lua :: Data/Scenario/Mystery 2.lua#20 :: [6] | loc O:1466 / N:1460 | T(6012, 'This accidental discovery was made later rather than sooner,... → T(6012, 'This accidental discovery was made later rather than sooner,... | **SW**
- P12447 | SA_WaitMessage | Data/Scenario/Mystery 8.lua :: Data/Scenario/Mystery 8.lua#14 :: [6] | loc O:824 / N:828 | T(8337, "The survivors of the Wildfire gathered in remote places of t... → T(8337, "The survivors of the Wildfire gathered in remote places of t... | **SW**
- P12448 | SA_WaitMessage | Data/Scenario/Mystery 8.lua :: Data/Scenario/Mystery 8.lua#16 :: [6] | loc O:956 / N:964 | T(8346, "People all around the world celebrate, but the consequences ... → T(8346, "People all around the world celebrate, but the consequences ... | **SW**
- P12449 | SA_WaitMessage | Data/Scenario/Mystery 8.lua :: Data/Scenario/Mystery 8.lua#3 :: [6] | loc O:112 / N:116 | T(8291, "The challenge would be monumental as our researchers lack an... → T(8291, "The challenge would be monumental as our researchers lack an... | **SW**
- P12453 | SA_WaitMessage | Data/Scenario/Mystery 9.lua :: Data/Scenario/Mystery 9.lua#6 :: [6] | loc O:814 / N:862 | T(8408, "A shipyard built in deep space, the Station is expected to g... → T(8408, "A shipyard built in deep space, the Station is expected to g... | **SW**
- P12475 | SA_WaitMessage | Data/Scenario/UndergroundAnomalies_Rare.lua :: Data/Scenario/UndergroundAnomalies_Rare.lua#22 :: [2] | loc O:802 / N:799 | T(14163, "Received an Asteroid Lander") → T(217432324648, "Space Tech Boost") | **MAL**
- P00853 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].__class | loc O:5 / N:5 | 'ClassGlobalCodeDef' → 'PropertyDefBool' | **AX**
- P00854 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].category | loc O:5 / N:5 | <absent> → Grouping | **AX**
- P00856 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].help | loc O:5 / N:5 | <absent> → If true, this resource group is used to group its sub-resources under... | **AX**
- P00857 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].id | loc O:5 / N:5 | <absent> → is_infopanel_group | **AX**
- P00858 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].name | loc O:5 / N:5 | <absent> → Use as infopanel group | **AX**
- P00860 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [16].no_edit_expression | loc O:5 / N:5 | <absent> → function ( self , prop_meta ) return not self.is_group end | **AX**
- P00861 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [17].__class | loc O:5 / N:5 | 'ClassConstDef' → 'ClassGlobalCodeDef' | **AX**
- P00873 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [19].help | loc O:5 / N:5 | <absent> → Whether this resource is allocated visual space in storage depots | **AX**
- P00874 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [19].id | loc O:5 / N:5 | <absent> → visually_placed_in_storage | **AX**
- P00875 | AppendClassDef | Data/ClassDef-Resources.lua :: Resource :: [19].name | loc O:5 / N:5 | <absent> → Take visual space in storages | **AX**
- P02137 | ClassDef | Data/ClassDef-Factions.lua :: LawEffect :: <preset> | loc O:2785 / N:absent | <removed> → empty | **CD**
- P02138 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectAutoSatisfyNeed :: <preset> | loc O:2793 / N:absent | <removed> → empty | **CD**
- P02139 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectCode :: <preset> | loc O:2831 / N:absent | <removed> → empty | **CD**
- P02140 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectDisableBuildMenuEntry :: <preset> | loc O:2861 / N:absent | <removed> → empty | **CD**
- P02141 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectModifyLabel :: <preset> | loc O:2920 / N:absent | <removed> → empty | **CD**
- P02142 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectModifyLabelMinistry :: <preset> | loc O:3011 / N:absent | <removed> → empty | **CD**
- P02143 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectModifyLabelMinistryWorking :: <preset> | loc O:3124 / N:absent | <removed> → empty | **CD**
- P02144 | ClassDef | Data/ClassDef-Factions.lua :: LawEffectTurnOffBuildings :: <preset> | loc O:3223 / N:absent | <removed> → empty | **CD**
- P02182 | ClassDef | Data/ClassDef-Default.lua :: MapDataProperties :: [26].name | loc O:179 / N:180 | Resource Info → Playable Height Range | **CD**
- P02595 | DumbAIDef | Data/DumbAIDef.lua :: default :: production_rules[5].Run | loc O:5 / N:5 | function ( self , resources , ai_player ) local fields = { "Biotech" ... → function ( self , resources , ai_player ) local tech_id = ai_player R... | **AI**
- P02712 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: Anomaly :: text | loc O:462 / N:471 | T(8116, "<em>Anomalies</em> appear all over the map in scanned sector... → T(8116, "<em>Anomalies</em> appear all over the map in scanned sector... | **E**
- P02728 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: Food :: text | loc O:144 / N:153 | T(5384, "<em>Food</em> <image UI/Icons/res_food.png> is grown on <em>... → T(5384, "<em>Food</em> <image UI/Icons/res_food.png> can be grown on ... | **E**
- P02729 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: ForestationAndSeeds :: text | loc O:570 / N:588 | T(625960246815, "Sustaining plant life on Mars is one of the major po... → T(625960246815, "Sustaining plant life on Mars is one of the major po... | **E**
- P02735 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: LifeSupport :: text | loc O:453 / N:462 | T(5413, "Colonists need <em>Life Support resources</em> in order to s... → T(5413, "Colonists need <em>Life Support resources</em> in order to s... | **E**
- P02750 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: Research :: text | loc O:471 / N:480 | T(5414, "New <em>technologies</em> will unlock new <em> buildings, up... → T(5414, "New <em>technologies</em> unlock <em>buildings, upgrades, Co... | **E**
- P02755 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: Seeds :: text | loc O:198 / N:207 | T(267062506431, "<em>Seeds</em> <image UI/Icons/res_seeds.png> are us... → T(267062506431, "<em>Seeds</em> <image UI/Icons/res_seeds.png> are us... | **E**
- P02767 | EncyclopediaArticle | Data/EncyclopediaArticle.lua :: UndergroundExploration :: text | loc O:633 / N:651 | T(354954610059, "The <em>Martian Underground</em> is dark and devoid ... → T(354954610059, "The <em>Martian Underground</em> is dark and devoid ... | **E**
- P08493 | MsgDef | Data/MsgDef.lua :: FoodProduced :: Params | loc O:359 / N:395 | building, amount → building, amount, resource | **MSG**
- P08494 | MsgDef | Data/MsgDef.lua :: FoodServiceMealServed :: <preset> | loc O:absent / N:402 | empty → <added> | **MSG**
- P08532 | NotificationPreset | Data/NotificationPreset.lua :: CropsFailed :: Text | loc O:426 / N:699 | T(5677, "No edible Food has been harvested") → T(5677, "No edible <em>Food</em> has been harvested") | **N**
- P08533 | NotificationPreset | Data/NotificationPreset.lua :: CropsFailed_Insects :: <preset> | loc O:absent / N:714 | empty → <added> | **NI**
- P08551 | NotificationPreset | Data/NotificationPreset.lua :: FactionOpportunity :: DismissFunc | loc O:1226 / N:1943 | function ( self , win ) g_Legislature.active_faction_task = false end → function ( self , win ) g_Legislature.active_faction_task = false g_L... | **NF**
- P08552 | NotificationPreset | Data/NotificationPreset.lua :: FactionOpportunity :: PressFunc | loc O:1226 / N:1943 | function ( self , win ) local obj = NotificationGetItemObj ( self ) N... → function ( self , win ) local task = g_Legislature and g_Legislature.... | **NF**
- P08628 | NotificationPreset | Data/NotificationPreset.lua :: PoliticsOpenSession :: OnInit | loc O:1294 / N:2067 | function ( self ) self.Expiration = g_Legislature.progress_end_time G... → <absent> | **N**
- P08632 | NotificationPreset | Data/NotificationPreset.lua :: PoliticsOpenSession :: Title | loc O:1294 / N:2067 | T(958624437879, "Legislative Session Open") → <absent> | **N**
- P08674 | NotificationPreset | Data/NotificationPreset.lua :: StarvingColonists :: <preset> | loc O:absent / N:1403 | empty → <added> | **N**
- P08683 | NotificationPreset | Data/NotificationPreset.lua :: TerraformingSeeds :: Text | loc O:2154 / N:2972 | T(758560215245, "New Resource: Seeds") → T(758560215245, "New Resource: <em>Seeds</em>") | **N**
- P08718 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortFood :: Obsolete | loc O:1590 / N:6 | <absent> → true | **H**
- P08719 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortFood :: SortKey | loc O:1590 / N:6 | 14900 → <absent> | **H**
- P08720 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortFood :: encyclopedia_image | loc O:1590 / N:6 | UI/Encyclopedia/Food.png → <absent> | **H**
- P08721 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortFood :: text | loc O:1590 / N:6 | T(613719950531, "Colonists living on <em>Asteroids</em> don't require... → <absent> | **H**
- P08722 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortFood :: title | loc O:1590 / N:6 | T(631911690656, "Comfort Food") → <absent> | **H**
- P08724 | OnScreenHint | Data/OnScreenHint.lua :: HintComfortStatAndServices :: text | loc O:518 / N:577 | T(5577, "Colonists will visit buildings to increase their Comfort sta... → T(5577, "Colonists will visit buildings to increase their <em>Comfort... | **H**
- P08726 | OnScreenHint | Data/OnScreenHint.lua :: HintCrops :: <preset> | loc O:absent / N:752 | empty → <added> | **H**
- P08741 | OnScreenHint | Data/OnScreenHint.lua :: HintFirstElevator :: text | loc O:1528 / N:683 | T(629055319176, "The <em>surface of Mars</em> and the <em>Underground... → T(629055319176, "The <em>surface of Mars</em> and the <em>Underground... | **H**
- P08748 | OnScreenHint | Data/OnScreenHint.lua :: HintHealthcare :: text | loc O:536 / N:597 | T(5580, "Healthcare Buildings will increase the Health and Sanity of ... → T(5580, "Healthcare Buildings will increase the <em>Health</em> and <... | **H**
- P08751 | OnScreenHint | Data/OnScreenHint.lua :: HintLawUI :: text | loc O:6 / N:12 | T(352334453164, "You can boost and specialize your colony by enacting... → T(352334453164, "<em>Laws</em> are special policies enacted by the pl... | **H**
- P08759 | OnScreenHint | Data/OnScreenHint.lua :: HintNeeds :: text | loc O:467 / N:522 | T(5569, "<em>Colonists</em> have several basic stats. You can monitor... → T(5569, "<em>Colonists</em> have several basic stats. You can monitor... | **H**
- P08763 | OnScreenHint | Data/OnScreenHint.lua :: HintPassengerRockets :: text | loc O:459 / N:514 | T(5567, "When you are ready you can invite the first Colonists to Mar... → T(5567, "When you are ready you can invite the first Colonists to Mar... | **H**
- P08765 | OnScreenHint | Data/OnScreenHint.lua :: HintPoliticsUI :: text | loc O:14 / N:20 | T(434196473597, 'In the Politics screen, you can see the active facti... → T(434196473597, 'In the Politics screen, you can see the active <em>F... | **H**
- P08781 | OnScreenHint | Data/OnScreenHint.lua :: HintResupply :: gamepad_text | loc O:354 / N:406 | T(7564, "A Cargo Rocket can deliver additional supplies for the colon... → T(7564, "A Cargo Rocket can deliver additional supplies for the colon... | **H**
- P08782 | OnScreenHint | Data/OnScreenHint.lua :: HintResupply :: text | loc O:354 / N:406 | T(5553, "A Cargo Rocket can deliver additional supplies for the Colon... → T(5553, "A <em>Cargo Rocket</em> can deliver additional supplies for ... | **H**
- P08784 | OnScreenHint | Data/OnScreenHint.lua :: HintResupplyUI :: text | loc O:366 / N:418 | T(5555, "Select a Cargo Rocket and load the desired payload up to the... → T(5555, "Select a <em>Cargo Rocket</em> and load the desired payload ... | **H**
- P08802 | OnScreenHint | Data/OnScreenHint.lua :: HintSuggestHydroponicFarm :: in_encyclopedia | loc O:510 / N:568 | <absent> → false | **H**
- P08803 | OnScreenHint | Data/OnScreenHint.lua :: HintSuggestHydroponicFarm :: text | loc O:510 / N:568 | T(5575, "Local Food production will be crucial to the survival of you... → T(5575, "Local <em>Food</em> production will be crucial to the surviv... | **H**
- P08953 | OnScreenHint | Data/OnScreenHint.lua :: Tutorial_4_HydroponicFarmAndStore :: <preset> | loc O:1228 / N:absent | <removed> → empty | **H**
- P08968 | OnScreenHint | Data/OnScreenHint.lua :: Tutorial_5_NewDomeFarms :: <preset> | loc O:1413 / N:absent | <removed> → empty | **H**
- P09560 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-Colonist.lua :: FirstStatusEffect_Starving :: <preset> | loc O:77 / N:absent | <removed> → empty | **P**
- P09562 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-Colonist.lua :: FirstStatusEffect_Suffocating :: text | loc O:35 / N:35 | T(5717, "Our Domes are large enough to contain tons of breathable air... → T(5717, "Our Domes are large enough to contain tons of breathable air... | **P**
- P09591 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-System.lua :: NewFeatures :: text | loc O:5 / N:5 | <absent> → T(442241367333, "Surviving Mars: Relaunched has been recently updated... | **P**
- P09599 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-GreenMars.lua :: ResearchedMartianVegetation :: text | loc O:48 / N:51 | T(269336522838, "Congratulations, you have successfully made the firs... → T(269336522838, "Congratulations, you have successfully made the firs... | **P**
- P09602 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-GreenMars.lua :: TerraformingHint_Seeds :: text | loc O:75 / N:78 | T(320203725995, "Seeds are now available. Seeds are a new resource, w... → T(320203725995, "<em>Seeds</em> are now available. <em>Seeds</em> are... | **P**
- P09662 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-Tutorial.lua :: Tutorial4_PopUp6_Food :: <preset> | loc O:636 / N:absent | <removed> → empty | **P**
- P09726 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-NewTutorial.lua :: Tutorial_Colonists_Meals :: <preset> | loc O:absent / N:360 | empty → <added> | **P**
- P09735 | PopupNotificationPreset | Data/PopupNotifications/PopupNotificationPreset-NewTutorial.lua :: Tutorial_Domes_Food :: <preset> | loc O:absent / N:449 | empty → <added> | **P**
- P12531 | ScriptConditionList | Lua/BuildingTemplate/FungalFarm_Asteroid.generated.lua :: Lua/BuildingTemplate/FungalFarm_Asteroid.generated.lua#1 :: <preset> | loc O:10 / N:absent | <removed> → empty | **BT**
- P12541 | SoundPreset | Data/SoundPreset.lua :: Building AutomatedFarm Work :: <preset> | loc O:absent / N:1748 | empty → <added> | **SO**
- P12542 | SoundPreset | Data/SoundPreset.lua :: Building Bakery_Loop :: <preset> | loc O:absent / N:1763 | empty → <added> | **SO**
- P12543 | SoundPreset | Data/SoundPreset.lua :: Building SmallFarm Start :: <preset> | loc O:absent / N:5860 | empty → <added> | **SO**
- P12544 | SoundPreset | Data/SoundPreset.lua :: Building SmallFarm Stop :: <preset> | loc O:absent / N:5870 | empty → <added> | **SO**
- P12545 | SoundPreset | Data/SoundPreset.lua :: Building_FoodProcessing_01 :: <preset> | loc O:absent / N:6744 | empty → <added> | **SO**
- P12546 | SoundPreset | Data/SoundPreset.lua :: Building_FoodProcessing_02 :: <preset> | loc O:absent / N:6756 | empty → <added> | **SO**
- P12547 | SoundPreset | Data/SoundPreset.lua :: Building_Replicator_Working :: <preset> | loc O:absent / N:6768 | empty → <added> | **SO**
- P12548 | SoundPreset | Data/SoundPreset.lua :: InsectFarm_Loop :: <preset> | loc O:absent / N:6779 | empty → <added> | **SO**
- P12549 | SoundPreset | Data/SoundPreset.lua :: Object OpenFarm Loop :: loud_distance | loc O:11985 / N:12078 | 2000 → 1500 | **SO**
- P12550 | SoundPreset | Data/SoundPreset.lua :: Object OpenFarm Loop :: volume | loc O:11985 / N:12078 | 130 → <absent> | **SO**
- P12852 | StatsImpactRest | Data/StatsImpact.lua :: Food :: <preset> | loc O:absent / N:57 | empty → <added> | **SR**
- P12880 | StatusEffectPreset | Data/StatusEffectPreset.lua :: StatusEffect_Starving :: <preset> | loc O:absent / N:130 | empty → <added> | **ST**
- P23771 | TraitPreset | Data/TraitPreset.lua :: Martianborn :: apply_func | loc O:565 / N:578 | function ( colonist , trait , init ) if colonist.city.colony IsTechRe... → <absent> | **TR**

## Close receipt

- Exact ledger validation: 510 ledger rows; 510 unique `prid`; expected-minus-ledger = 0; ledger-minus-expected = 0; duplicate `prid` = 0.
- Reached: all 510 assigned definitions and the route dossiers above. Runtime-not-reached: obsolete StoryBit/hint/popup definitions identified in SB/H/P; DLC-owner execution for `CropsFailed_Insects`; native sound/rendering/localization; dynamic DumbAI rule invocation; actual game execution.
- Hunk-only/malformed: exactly 29 keys enumerated in “Receipt and drift”; these are not counted as semantic paired reads.
- Adds/removes: 31 ledger rows have one side absent, each consistent with the tagged add/remove or the LawDef/ClassDef move; no row has both sides absent.
- FR-2: source route read first and reported; not closed from source.
- DLC fence: one directly called function only, `FarmInsectBase:GetCropsFailedNotificationId` at `N/DLC/norman/Code/FarmInsect.lua:57-59`; no other DLC function body was opened.
- FIX_POLICY §4: owner/non-owner, SMELL and PERF questions were applied to every opened function/body. L1 and L2 are the surviving hard-tell reads; L3 is a behavior delta without a hard tell; other dossiers record none. No frame-time/native/runtime result is claimed.

End of read-only support report. No final defect verdict is made here.

