# C92 icon hunt — expanded pack and historical controls

2026-09-13, derived at repo `ccd4ff58762558ba79eef6065121d22ec138bea2`;
Relaunched app **3215050**, Steam build **24995074**, source baseline
**1.1.0.403908**. Machine evidence: [icon_evidence.json](icon_evidence.json).
Reproducer: [icon_hunt.py](icon_hunt.py). No game launched or game/archive files changed.

## Result and refutations

**MEASURED:** No dedicated `UndergroundExploitation` research image was located in
the expanded installed-pack census. All research DDS assets were decoded and viewed,
including DLC art; the law glyph was viewed too. **INFERRED:** The existing law glyph
can communicate the subject, but substituting it for a research illustration is an
art/design decision. **The hunt does not establish that dedicated art was never drawn.**
That earlier assertion exceeds what any shipped-pack negative can show.

**MEASURED refutation:** The disputed orphan set is not uniformly unknown art from
the Relaunched rebuild. Two previously missed names have direct 1.0.7 preset owners,
five already occur in the ORIGINAL game's UI pack, and two are pixel-identical copies
of the funding image. These conclusions depend respectively on actual icon references,
a separately controlled original-game pack read, and decoded pixel hashes; they do not
depend on interpreting an icon's filename as its intended technology.

**SOURCE refutation:** The three law files represent **UI states, not technology/law
tiers**. `Lua/XDef/LawEntry.generated.lua:83-104` on 1.1.0 maps `_1` to locked,
`_2` to visible/preparing/no state, and `_3` to active/prepared. The law's hex background
is another asset. **MEASURED visual:** All three exploitation files show the same cave
opening/stalactites and magnifying-glass glyph, in dark gray, muted gold and bright gold.
They are each 186×216; file and decoded-pixel hashes differ. This is a visual silhouette
comparison, not a claim that every alpha pixel is identical.

## Instrument, scope and reproduction

**MEASURED:** `tools/flpk_extract.py` passes both its shallow positive-control and
nested-directory demand fixtures. The census uses that parser on every `.fpk` beneath
the manifest-resolved Relaunched installation, and additionally decodes/hashes one
named payload from **each** pack. These controls and directory hashes are retained in
the evidence JSON, including all map and texture packs. The three art-pack controls
also include successfully decoded DDS images.

| Sample | Result |
|---|---|
| MEASURED installed FLPK census | 183 packs, 58,037 directory entries; all parsed |
| MEASURED `Packs/UI.fpk` | 5,001 entries; 371 research DDS |
| MEASURED `DLC/norman.fpk` | 1,844 entries; 24 research DDS; includes the source-referenced `advanced_underground_farming` control |
| MEASURED `DLC/thomas.fpk` | 49 entries; no research directory assets; both UI images decoded: `interplanetary_codex`, `law_office` |
| MEASURED current art inspection | All 395 research DDS, 15 selected law DDS and 2 Thomas UI DDS extracted to scratch; all research illustrations viewed on contact sheets |
| MEASURED base Tech icon control | All 312 distinct `Data/Tech.lua` research-image references resolve after runtime `.png` to packed `.dds` normalization |
| MEASURED current source reference scan | All 4,715 Lua files under installed `ModTools/Src`, including Data, DLC and Lua UI |
| MEASURED archived source reference scan | All 4,446 Lua files under `SMR-SrcArchive/1.0.7.396349/Src` |
| MEASURED historical control only | ORIGINAL app 464920/build 8705308 `Packs/UI.hpk`: BPUL, 2,534 entries, 224 research images; `advanced_drone_drive` extracted and decoded successfully |

Reproduce from the repository root; this command was run 2026-09-13. Its only payload
writes are to the named scratch folder; the proof output is text metadata.

```powershell
python docs/agent/reports/c92-placement/icon_hunt.py --game 'A:\SteamLibrary\steamapps\common\Project Spark' --scratch 'C:\Dev\C92-placement-scratch\icons' --output 'C:\Dev\C92-placement-scratch\icons\summary.json' --archive 'C:\Dev\SMR-SrcArchive\1.0.7.396349\Src' --original-hpk 'A:\SteamLibrary\steamapps\common\Surviving Mars\Packs\UI.hpk' --proof docs/agent/reports/c92-placement/icon_evidence.json
```

**MEASURED:** The current source scan finds no direct image-path references to the
22 unused named research pictures. Its positive controls resolve `advanced_drone_drive`
at current Tech lines 384 and 10638, and archived TechPreset line 697. The separately
excluded `researched` checkmark does resolve in `Lua/GameRules.lua`. **Bound:** This
search is for literal research-image paths, not a proof against every dynamically
constructed path or external mod.

## The disputed nineteen, after actually opening the images

Each filename below is under `Icons/Research/` in current `UI.fpk`. Visual descriptions
are observations; thematic relevance to C92 remains inference.

| File stem | Observed illustration and provenance |
|---|---|
| `advanced_asteroid_economy` | MEASURED blue asteroid/economy display; no direct icon reference in either source snapshot |
| `advanced_elevator_hydraulics` | MEASURED elevator machinery schematic; no direct icon reference in either snapshot |
| `advanced_landing_techniques` | SOURCE 1.0.7 `AdvancedLandingTechniques`, TechPreset line 3509; MEASURED rocket schematic |
| `capture_asteroids` | SOURCE 1.0.7 **`CaptureAsteroid`**, TechPreset line 85; MEASURED targeting display marked CAPTURED; earlier normalized-ID matching missed this owner |
| `crawling_hyperdome` | MEASURED funding/cash graphic, pixel-identical to `near_orbit_observatory` and live `terraforming_subsidies` |
| `educating_mars` | MEASURED group of colonists; no direct icon reference in either snapshot |
| `eureka` | MEASURED small lightbulb badge; already present in the ORIGINAL UI pack |
| `grand_engineering` | MEASURED blue dome/terrain schematic; no direct icon reference in either snapshot |
| `metal_foams` | MEASURED porous metallic sphere; already present in the ORIGINAL UI pack |
| `micro-g_vehicles` | MEASURED vehicle on rocky gray terrain; no direct icon reference in either snapshot |
| `near_orbit_observatory` | MEASURED funding/cash graphic; exact duplicate identified above, not a distinct observatory illustration |
| `polymer_autosynthesis` | MEASURED industrial robot arm; already present in the ORIGINAL UI pack |
| `proximity_power_resonance` | MEASURED grouped red/cream machinery/cells; no direct icon reference in either snapshot; nothing in its pixels establishes Hi-Tech I placement |
| `smart_alloys` | MEASURED metallic block with blue/black surrounding material; already present in the ORIGINAL UI pack |
| `standardized_integration` | MEASURED speaker/podium with Mars behind; already present in the ORIGINAL UI pack |
| `terraforming_mars` | MEASURED globe of Mars; no direct icon reference in either snapshot |
| `underground_trains` | SOURCE 1.0.7 `UndergroundTrains`, TechPreset line 3572; MEASURED train in a cavern |
| `vacuum_rail_systems` | MEASURED blue tubular schematic; no direct icon reference in either snapshot |
| `vehicle_optimization` | SOURCE 1.0.7 **`VehicleWeightOptimizations`**, TechPreset line 230; MEASURED vehicle schematic with weight display; earlier normalized-ID matching missed this owner |

**MEASURED:** The three money images share decoded RGBA SHA-256
`1eb9b61c2555768963b9c2cedadb41f825aeb2f29167ab16548dff70735b7516`.
A second equality group is `Mineral_Applications` / `advanced_mineral_composites`.
Therefore distinct asset filenames do not imply distinct illustrations.

**MEASURED:** The five original-game images and the `advanced_drone_drive` control
decode successfully. Original and Relaunched pixel hashes are **not equal**. Side by
side inspection shows matching compositions with changed framing/scale; exact file
reuse is not claimed. Their original-game presence establishes older names/art motifs,
not an exact export date or designer intention. The original BPUL directory parser
follows the locally available `hpk/src/hpk/mod.rs` Header/DirEntry layout and
`hpk/src/hpk/walk.rs` traversal; the small reproducer includes the controlled read.

**INFERRED:** None of these unused pictures supplies positive evidence identifying
it as Underground Exploitation art. Elevator/engineering/materials pictures could be
repurposed by a designer, as could the law glyph. Resemblance alone cannot settle the
tech's intended image, tier, coordinates or prerequisites.

## Owner follow-up: Industry and Hi-Tech category pass

**MEASURED:** A second pass selected presets by their **actual group**, covering all
Industry I–V and Hi-Tech I–V, rather than by words such as underground in a filename.
It emitted **55 presets, 54 explicit image assignments and 7 obsolete presets**.
The spelling difference `Hi-Tech_1` versus `Hi_tech_2` through `_5` is included.
[industry_hitech_icons.tsv](industry_hitech_icons.tsv) retains the preset ID, group,
assigned icon, obsolete flag and full shipped description. Both focused sheets were
viewed, with six unreferenced materials/engineering/power candidates beside the owners.

| Lead | Evidence and consequence |
|---|---|
| SOURCE Industry V `ContinuousOperationProtocols` | Its own `continuous_operation_protocols` icon and description promise extractor production after uninterrupted operation. MEASURED the art shows material flowing through a production diagram. INFERRED thematically close to the production part of C92, but it is already assigned to a separate technology. |
| SOURCE Industry V `ClosedLoopExtraction` | Its own `closed_loop_extraction` icon remains assigned to an obsolete preset. MEASURED the art shows a blue rock with circular arrows. INFERRED this is the strongest retired extraction-themed image in the group; an obsolete owner is positive provenance, not proof of an unclaimed C92 asset. |
| SOURCE Industry V `FactoryAI` / `ThermalCyclingDampeners` | Descriptions address factory output / extractor cold-wave power spikes. MEASURED their pictures show a factory with a graph / a labeled machine housing. Their separate owners are recorded in the TSV. |
| SOURCE Industry IV `DeepWaterExtraction` / `FueledExtractors` | Assigned pictures depict extractor machinery, paired with deep-water access / fuel-fed production upgrades. INFERRED visually closer to extraction than the borrowed drone picture, but already occupied by those techs. |
| SOURCE Industry I `ExtractorAmplification` | Its rig-and-rising-graph image already denotes extractor output/power amplification. INFERRED a plausible generic illustration if an owner deliberately chooses reuse; no evidence makes it the intended underground picture. |
| SOURCE Hi-Tech IV `EnhancedTopographicalExploitation` | The attractive filename is already assigned to **wind-turbine elevation power bonuses**. MEASURED the picture is a terrain/elevation graphic. This rules out treating the word exploitation as an undiscovered C92 connection. |
| SOURCE Hi-Tech V `MineralApplications` / `MineralApplications_AdvancedMineralComposites` | The two paths with identical pixels are assigned to solar-panel upgrade presets; the latter is obsolete. Their mineral names do not establish extraction scope. |
| SOURCE Hi-Tech I `MineralApplications_MineralTreatments` | Its explicit description concerns infirmary/medical-post Health and Sanity, and its crystal/medical illustration has its own owner. It supplies no source link to the empty Hi-Tech I ring slot. |
| MEASURED unreferenced `metal_foams`, `smart_alloys`, `polymer_autosynthesis` | Materials sphere, metallic block and robotic manufacturing arm, also found in the original-game pack. INFERRED broad Industry themes fit; there is no underground-specific visual or source assignment. |
| MEASURED unreferenced `grand_engineering`, `advanced_elevator_hydraulics`, `proximity_power_resonance` | Dome/terrain schematic, elevator assembly and grouped machinery/cells. INFERRED these support broad engineering, logistics or power interpretations; none establishes an extractor bonus or a tree coordinate. |

**INFERRED result of the wider pass:** Industry contains several more suitable
extraction/production illustrations than the drone placeholder, including a retired
extraction picture. Those are **known assignments available for deliberate reuse**,
not discovered proof of C92's intended image. Unreferenced materials/power art remains
plausible only at the broad theme level. No new positive link to Underground
Exploitation or a particular Industry/Hi-Tech slot emerged from the category pass.

## Ordering, review files and bounds

**MEASURED:** The complete directory inventory retains pack path, traversal index,
payload offset, flags and stored length. The law sequence in UI traversal is `_1`,
then `_3`, then `_2`, interspersed with unrelated laws. **SOURCE:** The current FLPK
reader has no decoded per-asset creation timestamp. A spot read of the trailing u32
returns 129, 0 and 46 for the three exploitation records, not a usable date field.
**INFERRED:** No measured chronology or authoring placement follows from that order;
these values' semantics were not reverse-engineered.

Scratch review artifacts (copyrighted assets are not committed):

- `C:\Dev\C92-placement-scratch\icons\focused_orphans_laws.jpg`: unused names, law variants and live controls.
- `...\sheet_01.jpg` through `...\sheet_09.jpg`: complete current research-image contact sheets, plus selected law/Thomas controls.
- `...\original_comparison.jpg`: original/relaunched side-by-side comparison viewed in this investigation.
- `...\industry_hitech_01.jpg` and `...\industry_hitech_02.jpg`: all explicit Industry/Hi-Tech image owners, obsolete flags, and six unreferenced comparison candidates.
- `...\inventory.json`: complete current pack table inventory; `summary.json`: full hashes and source-reference census.

**Not opened / not established:** No arbitrary visual inspection of every terrain,
material, model texture or nonresearch UI bitmap; their packed names were enumerated
and relevant name matches inspected in the inventory. No proof against an image
hidden under an unrelated name outside the research directories or inside an atlas.
No original-game DLC HPK census. No archived Relaunched UI pack was available in the
source-archive trees (the file search found source/manifests, no image or pack assets).
No studio art source, commissioning history, deleted files, depot history or private
repository. No live game rendering or placement trial. These are limits on a universal
absence claim, not evidence that a dedicated icon exists.
