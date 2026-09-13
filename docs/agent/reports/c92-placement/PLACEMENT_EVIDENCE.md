# C92 placement and authoring evidence

2026-09-13; report-only subtask. Main report: [C92_PLACEMENT](../C92_PLACEMENT.md).
No game launch, game/archive modification, or mod implementation occurred here.

## Findings that change the prior account

**SOURCE:** The earlier five-member conversion cohort is incomplete, and one member
is misclassified. The two closest controls were missed:
`Policy_UndergroundMiningPermits` became `UndergroundDeepMining`, and
`Policy_UndergroundWaterPermits` became `UndergroundWaterExtraction`. Both finished
successors are assigned to `Underground_1`, and both preserve the old prerequisite
excluding the no-underground game rule. These supply positive evidence for the
*family* of the hidden tech. Neither supplies its intended coordinate or connection.

**SOURCE:** `MartianDiet` already existed as a Breakthrough in 1.0.7, using
`martian_diet.png`, the same localization IDs, and the same 25% food-consumption
effect as its 1.1 successor (`Data/TechPreset.lua:546–561`, 1.0.7;
`Data/Tech.lua:1329–1352`, 1.1). The separate old law reduced consumption by 50%.
Retiring that law did not create this technology or its icon. The previous statement
that every finished member received a newly created bespoke icon therefore fails
this control. The tech remains a valid control for normal hidden Breakthrough flags,
but not for art newly produced during this conversion.

**OWNER AUTHORITY:** There is only one Underground tree and it appears fully laid
out. **MEASURED:** The supplied screenshot shows a complete Underground I ring.
**SOURCE:** The target's explicit `group = "Underground_1"` establishes an authored
family assignment; it does not establish a vacancy, require adding a satellite, or
override the owner's observation. No exact intended slot was recovered.

## Reproduction and boundaries

**MEASURED:** Run:

```powershell
python docs/agent/reports/c92-placement/placement_inventory.py
```

Recorded at HEAD `ccd4ff58762558ba79eef6065121d22ec138bea2`, installed Steam app
`3215050`, installdir `Project Spark`, build `24995074`. The command resolves these
three manifest fields and emits source hashes. Current archived
`C:/Dev/SMR-SrcArchive/1.1.0.403908/Src` files `Data/Tech.lua`, `Data/TechGroup.lua`,
`Data/XPresetMapLabel.lua`, and `DLC/norman/Presets/Tech.lua` were byte-identical to
the corresponding installed ModTools files. The Tech source SHA256 is
`7033a4b9330ab73eebf302347d063364c883ba229665884af52049bf5276efc9`.
Historical comparisons use `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src`.

**MEASURED:** The parser splits generated, unindented `PlaceObj` declarations and
reads direct assignment lines, retaining original line numbers. Assertions check
declaration accounting, duplicate IDs, known old/new presets, a known connection,
and archive/current hash agreement. No Lua is executed. This is a source census,
not an in-game visibility or research test. Records bearing conditions can still
be hidden by those conditions at runtime.

Evidence outputs:

- [Inventory/provenance](placement_inventory.json).
- [Every base preset's direct authoring fields](placement_new_authoring.tsv).
- [Exact-ID historical mapping](placement_old_to_new.tsv) and its
  [theme/range/group aggregation](placement_mapping_summary.tsv).
- [Compared law/tech controls](placement_conversion_controls.tsv).
- [Candidate-slot occupancy and adjacent live preset IDs](placement_slots.tsv).

**MEASURED:** The script emitted 264 old TechPreset declarations, 441 new base Tech
declarations, 25 norman Tech declarations, and 258 exact-ID historical matches.
Nine compared law/tech pairs include eight new tech IDs and the retained
`MartianDiet`. These are comparison controls, not a claimed exhaustive migration
count. Missing IDs are not automatically removed content: the exact-ID map exposes
`FarmAutomation ` with a trailing space as one obvious normalization hazard.

## Direct placement hints and their limits

All source citations in this section are 1.1.0.403908 unless otherwise marked.

| Observation | Evidence and consequence |
|---|---|
| **SOURCE:** Explicit family | `Data/Tech.lua:10635–10660`: `UndergroundExploitation` names `Underground_1`. This is the strongest direct placement datum. |
| **SOURCE:** No intended slot annotation | The same complete block has no preset-level `Comment`, `TODO`, `SortKey`, `Condition`, or `RequireTech`. The parameter has only `Comment = "Production Buff"`. |
| **SOURCE:** Current off-board position | The block saves `MapPos = point(14576, 4352)`, `LockState = "hidden"`, and `Unknown = true`. The coordinate does not encode a visible destination. |
| **MEASURED:** Sort keys cannot recover destination | None of the 441 base Tech blocks has a direct `SortKey`, although the class supports it (`CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua:24`). A missing target sort key is therefore not exceptional. |
| **SOURCE:** Neighbour annotations do not name C92 | `UndergroundDeepMining` and `UndergroundWaterExtraction` have `TODO = Review`; `UndergroundDomes` has `TODO = Test`. No Underground I member has a preset `Comment` identifying a missing neighbour. The Hi-Tech I and Industry V members' annotations likewise name no missing target. |
| **SOURCE:** No dropped link elsewhere | Whole-source search for `UndergroundExploitation` found the preset, retired LawDef/PolicyDef, save fixup, and stockpiled-production consumer. No other Tech connection or DLC source refers to it. The main agent separately sampled decoded shipped packs. |

**SOURCE:** Old `Policy_UndergroundExploitation` at
`Data/LawDef/LawDef-Economy.lua:1090–1099` (1.0.7) had the explicit prerequisite
`not IsGameRuleActive("NoUndergroundAndAsteroids")`. Its new tech has no corresponding
`Condition`. The default Tech condition returns true (`Lua/TechTree.lua:264–265`).

**INFERRED:** If the owner ever elects to restore reachability, preserving that old
restriction is well supported by the two Underground I conversion controls below.
It is still a repair design decision. Missing direct conditions are not unique:
the finished `Space_Farming` conversion also lacks the old no-underground/asteroids
condition, and is linked only through `DeepAsteroid_Extraction`, which has it.
Thus the target's missing condition alone cannot prove an accidental omission.

## Stronger conversion controls

**SOURCE:** `Lua/Factions/Laws.lua:1136–1149` explicitly names
`SavegameFixups.TransformLawsToTechs_v2`. Its list includes the underground mining
and water laws, asteroid mining, sensor extra scanning, shuttle efficiency, and
drone-hub efficiency. Removing an active listed law refunds a Tech Point. This is
direct authoring evidence of conversion, not an inference from similar titles.

| Compared former law | Successor and evidence |
|---|---|
| **SOURCE:** `Policy_UndergroundMiningPermits` | `UndergroundDeepMining`, `Underground_1`, `(9766,3200)`, `Data/Tech.lua:10570–10594`. Old consumer `Lua/Buildings/SubsurfaceDeposit.lua:26,33` (1.0.7) checked the law; new `:26,34` checks this tech for underground mines. |
| **SOURCE:** `Policy_UndergroundWaterPermits` | `UndergroundWaterExtraction`, `Underground_1`, `(9322,3200)`, `Data/Tech.lua:10708–10732`. Old law advertised continued depleted-water extraction (`LawDef-Economy.lua:1175` onward, 1.0.7); old water-specific consumer `SubsurfaceDeposit.lua:438` checked it. New `:27,35` checks the tech. The historical mining law also covered WaterExtractorBase, so this is a semantic split as well as a rename. |
| **SOURCE:** `Policy_AsteroidDeepMining` | `DeepAsteroid_Extraction`, `Space_3`, `(8508,5376)`, `Data/Tech.lua:8687–8711`; same old-to-new consumer substitution at `SubsurfaceDeposit.lua:25,32–33`. |
| **SOURCE:** `Policy_SpaceFarming` | `Space_Farming`, `Space_3`, `(8360,5376)`, `Data/Tech.lua:8785–8801`. The old `Lua/BuildingTemplate/FungalFarm_Asteroid.generated.lua:12–18` required the law; the new tech's effect unlocks that building. |
| **SOURCE:** Drone hub, shuttle fuel, sensor scanning | Finished connected techs in `Logistics_2`, `Logistics_3`, and `Space_1`; complete fields and source lines are in the conversion TSV. |
| **SOURCE:** `Policy_MartianDiet` | Retired law alongside a retained old Breakthrough, not a fresh tech conversion; old/new source blocks above provide the counterexample. |

**INFERRED:** The closest family controls are the underground pair, not the
Logistics/Space examples from the previous pass. Their y=3200 locations make that
row a reasonable place to discuss with the developer. The conversions' shared old
Economy grouping does not recover an exact new coordinate or a numerical tier.

## What a connection would mean

**SOURCE:** `Lua/TechTree.lua:443–473` walks `RequireTech`, accepts the first visible
connection whose other tech is researched, and breaks. Multiple neighbours mean
OR, not AND. With no connections, it falls back to whether the tech is already
unlocked, producing the known circular requirement. `MapPos` has no part in this
check. Editor metadata declares symmetric connections at `:278–279`.

**INFERRED, design candidates only:** `UndergroundDeepMining` is the strongest
single connection candidate because it is the closest converted mining-law
sibling and covers the broader extractor-production theme. `UndergroundWaterExtraction`
is a second candidate supported by the water effect and the other sibling's
history. Linking both would allow research after either and would need deliberate
review for progression. Neither candidate is a recovered developer-authored edge.
The parent scope investigation owns whether water and stockpiled production
actually overlap; this report does not assume a doubled bonus.

## What the holes and historical mapping establish

**OWNER AUTHORITY:** Only one Underground tree is present and it appears fully laid
out. **MEASURED:** Viewed the owner's original image
`C:/Users/stkot/OneDrive/Pictures/Screenshots/2026-09/Mars_hQgXBGTKNZ.jpg` unchanged;
SHA256 `126f530ce0d262f25871c2346d44ac715c1d7d38ec1834292b94343bddee2713`.
The image shows the complete Underground I ring and the incomplete Hi-Tech I and
Industry V shapes. It does not show a named empty slot for Underground Exploitation.

**SOURCE/MEASURED:** Underground I's authored ring is complete; the group's other
visible members are satellites. `placement_slots.tsv` samples the owner's candidate
coordinates against non-hidden, non-obsolete base presets. The actual empty slots
and immediate hex neighbours are:

| Slot | Current measurement; destination interpretation |
|---|---|
| **MEASURED:** Hi-Tech I `(7768,2816)` | Empty; adjacent `AtomicAccumulator` and `MineralApplications_MineralTreatments`. **INFERRED:** Weak fit for C92, because the target's explicit group says Underground I; not evidence of a separate missing technology. |
| **MEASURED:** Industry V `(10062,2944)` / `(9988,2816)` | Both empty; adjacent to `ThermalCyclingDampeners` / `ContinuousOperationProtocols`, respectively. **INFERRED:** Production theme fits, but neither slot has an authored link to C92. |
| **MEASURED:** Bridge `(9914,3200)` | Empty; adjacent to `FactoryAI`, `ThermalCyclingDampeners`, and `UndergroundDeepMining`. **INFERRED:** Strongest geometric bridge candidate, still no authored reservation. |
| **MEASURED:** Sibling-row `(9470,3200)` / `(9618,3200)` | Empty; adjacent to `UndergroundWaterExtraction` / `UndergroundDeepMining`, respectively. **INFERRED:** Strongest family-based candidates if a new seat were chosen; neither is forced by the complete Underground ring. |

**MEASURED:** The old-to-new map has 258 exact-ID matches. Old `Physics`,
`range(7,9)` alone splits three ways: `AtomicAccumulator` → Hi-Tech I,
`DustRepulsion` → Sustainability I, `FactoryAmplification` → Industry I. The old
Underground-themed members also spanned wide old bands: `LowGFungi` was Biotech
1–5, `RemoteFarming` Biotech 6, and `UndergroundPsychStudies` ReconAndExpansion
16–19. They all landed in Underground I. A deterministic old theme+tier → new
cluster rule therefore cannot be recovered from these fields. The full map is
retained so another reader can test a different convention.

**SOURCE:** The old `position` range controlled a randomized sequence placement
(`Lua/Research.lua:100`, 1.0.7), not map coordinates. **MEASURED:** Old TechPreset
blocks have no `MapPos`. New coordinates are stored directly; `Tech:SnapPos`
(`Lua/TechTree.lua:427–432`, 1.1) snaps an editor coordinate to the hex grid.
**INFERRED:** Neither supplies an inverse placement rule for a former law.

**SOURCE, public author statement:** The developer describes the cluster numbers
as positional aids, with farther numbers tending outward, and explicitly planned
room for future additions. That narrows what an empty ring can prove: blank space
is compatible with intended layout. It does not prove that these specific holes
were reserved for anything. [Haemimont Diaries #4: Lab Leaks](https://steamcommunity.com/games/3215050/announcements/detail/699895897307217965).

**MEASURED:** Fetched the same diary through Steam's `ISteamNews/GetNewsForApp/v2`
API (`appid=3215050&count=100&maxlength=0`), which dates the post to
2026-07-14 14:11:20 UTC. Viewed its four body images at original resolution.
The overview shows Underground I and the sibling row, but crops the Hi-Tech I and
Industry V empty seats above the image. Its bridge slot is visibly blank; the other
images cover upper Hi-Tech sectors, the southern board, and Breakthroughs. None
shows a historical named C92 node. This is bounded visual evidence, not proof that
no other prerelease screenshot exists. The overview original is
[the diary image](https://clan.fastly.steamstatic.com/images/45747899/21f1d3a65418a40f0b6f7728e1ab05b5fae3d305.png).

**INFERRED recommendation for Q4:** Report the explicit Underground I assignment,
the complete visible ring, and the two converted underground siblings. Do not
select a required coordinate from the holes. The developer still needs to supply
the intended seat and connections if restoration is pursued. A historical named
node, reserved-link record, editor revision, or developer confirmation would
falsify the current conclusion that an exact intended placement is unrecovered.

## Owner-directed follow-up: upper Industry and Hi-Tech associations

The owner explicitly asked to look beyond Underground names, especially the upper
Industry and Hi-Tech icons. **SOURCE:** Read the complete preset blocks in
`Industry_4`, `Industry_5`, and `Hi_tech_3` through `Hi_tech_5`, then traced the
most relevant effects. This pass used the same 1.1 source fingerprint above; the
icon subtask separately viewed the art. No source association identifies any of
these images as Underground Exploitation's missing icon.

| Candidate or misleading match | Source ownership and effect |
|---|---|
| **SOURCE:** `ClosedLoopExtraction` → `UI/Icons/Research/closed_loop_extraction.png` | Industry V, obsolete, `(10210,2944)` outside the ring, `Data/Tech.lua:4539–4570`. The effects unlock the extractor `*_ClosedLoopExtraction` upgrades. `Lua/BuildingTemplate/MetalsExtractor.generated.lua:58–65` identifies that upgrade as disabling maintenance. This is actual retired extractor art, making it a useful visual candidate to inspect, but its recorded purpose is a different benefit and it retains a separate owning preset. |
| **SOURCE:** `ContinuousOperationProtocols` → `UI/Icons/Research/continuous_operation_protocols.png` | Industry V, `Data/Tech.lua:4572–4599`, gives 15% production after three uninterrupted Sols. `Lua/Buildings/ContinuousOps.lua:12–36,84–100` independently modifies stockpiled producer output and grid water, under its own modifier ID and timer. This supplies the closest current Industry production-buff comparator; it is already an assigned, connected tech with its own implementation, not an unclaimed C92 icon or renamed copy. |
| **SOURCE:** `ThermalCyclingDampeners` → `UI/Icons/Research/thermal_cycling_dampeners.png` | Industry V, `Data/Tech.lua:4656–4679`, removes extractor cold-wave power penalties (`Extractors.penalty_pct`), not a production bonus. |
| **SOURCE:** `FueledExtractors` / `DeepWaterExtraction` | Industry IV owns `UI/Icons/Research/fueled_extractors.png` and `UI/Icons/Research/deep_water_extraction.png` (`Data/Tech.lua:4339–4416`). They unlock fuel-powered extractor upgrades and deep-water exploitation respectively; both remain separately connected techs. Their mining/water imagery is already explained by those assignments. |
| **SOURCE:** `EnhancedTopographicalExploitation` → `UI/Icons/Research/enhanced_topographical_exploitation.png` | Hi-Tech IV, `Data/Tech.lua:3122–3153`; the similar word “Exploitation” denotes a 50% increase to wind-turbine elevation bonuses (`WindTurbines.bonus_per_kilometer_elevation`). Its effect supplies no underground-production link. |
| **SOURCE:** `MineralApplications` / `MineralApplications_AdvancedMineralComposites` | Hi-Tech V owns `UI/Icons/Research/Mineral_Applications.png` and `UI/Icons/Research/advanced_mineral_composites.png`, respectively (`Data/Tech.lua:3288–3348`). Both unlock Improved Photovoltaics for solar buildings; the latter is obsolete. The mineral wording describes solar upgrades, not underground extraction. |
| **SOURCE:** `WindStoreEnergy` / `SolarStoreEnergy` | Retired Hi-Tech IV/V presets own `UI/Icons/Research/oboard_power_buffering.png` and `UI/Icons/Research/hybrid_solar_capacitors.png` (`Data/Tech.lua:3248–3258,3414–3424`). Their effects unlock turbine/solar battery upgrades. These are further concrete unused-in-the-live-tree images with explicit unrelated histories. |
| **SOURCE:** `MineralApplications_MineralTreatments` | The Hi-Tech I hole's neighbour owns `UI/Icons/Research/mineral_treatments.png`, but its effects unlock Infirmary and Medical Post health/sanity upgrades (`Data/Tech.lua:2784–2814`). Its mineral name is not evidence of an extractor link. |

**INFERRED:** The source supports the owner's thematic instinct: Industry V
already groups extraction-production, extraction-maintenance, and cold-wave
efficiency. That improves its usefulness as an art comparison set. It does not
identify C92 with either vacant ring seat. The strongest retired-art lead here is
`closed_loop_extraction.png`; its known maintenance-upgrade ownership prevents
calling it recovered dedicated C92 art. The already assigned production comparator
is `continuous_operation_protocols.png`. Exact pixel judgments remain in the icon
report; this section establishes what their associated code actually does.

## Not opened / not established

- No internal vendor editor history, design document, or version between the two
  archived source trees was available. No claim that such evidence does not exist.
- No in-game research, visibility, Chaos Theory, or game-rule leg was run.
- The eight new-ID comparison rows are not an exhaustive census of all law
  retirement/replacement policies. Remaining obsolete laws were enumerated, but
  their replacement semantics were not traced.
- No claim that `Hi-Tech_1` has a separate missing technology, or that an orphan
  icon must correspond to any open seat. Neither is established enough to file.
- This subtask did not decode packed assets or independently test bonus/save
  semantics; the main and other parallel reports own those evidence routes.
- The public screenshot search is limited to the located diary images, and their
  content does not establish absence from other historical images or videos.
