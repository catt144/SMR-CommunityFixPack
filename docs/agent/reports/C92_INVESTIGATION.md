# C92 investigation - hidden Underground Exploitation requirement

2026-09-13. Investigation only; no fix module, achievement award, research
mutation or shipped Lua change. Defect truth: [C92](../bugs/C92.md).

**MEASURED:** The supplied Sol 490 save fails the vanilla achievement predicate
solely on `UndergroundExploitation`, a hidden, unresearched ordinary Tech in
`Underground_1`. Both repeatables have completed once and retain `researched`.
Excluding repeatables still fails; excluding that one hidden preset passes.

## Provenance and limits

- **Owner authority:** The owner personally loaded the reporter's original,
  verified all non-repeatable technologies complete in the tree, and verified
  a clean original save with no mods on the current patch. This is accepted,
  not re-derived. A hidden requirement reconciles that check with the failure.
- **MEASURED:** Original: `C:\Users\stkot\Downloads\Autosave Sol 490.savegame.sav`;
  SHA256 `68d340ad0f1a2b13047034e21a7fc84199c66f069858f190be1e9f38d0ff9bb7`.
  Only a byte copy named `C92READ.savegame.sav` was loaded.
- **MEASURED:** Retail `1.1.0.403908`, DLCs norman + thomas, day 490, Japan,
  3 tech points, no game rules. These reads ran with the normal rig's Test Kit,
  Fix Pack and Opt-In Pack loaded. They establish live state and the predicate
  barrier, not an unmodded in-game award attempt on the reporter's account.
- **MEASURED:** Owner account `GetAchievementFlags("ResearchedAllTechs")=true`.
  This is account state, not save state or evidence the reporter was awarded it.
  The diagnostic never called the achievement handler or `AchievementUnlock`.
- **SOURCE + desk control:** `python tools/desk_c92_achievement.py` executes
  shipped preset data, iterator, completion/state methods, `Player:UIResearch`
  and the achievement listener. The unlock sink only records requests.
  It prints HEAD, version, body locations and hashes. Synthetic completion
  flags are declared; no claim it recreates the reporter's colony.
  [Retained desk output](../../archive/c92_desk_20260913.txt): all named demands
  held, including the incomplete-ordinary and never-completed-repeatable controls.

## Retained game transcripts

| leg | result | transcript |
|---|---|---|
| MEASURED r1, prep `1053bf3` | save loaded; census stopped at a diagnostic formatting error | [r1](../../archive/c92_read_r1_Mars.exe-20260913-03.49.24.log) |
| MEASURED r2, prep `2a7e596` | census completed; hidden Tech was the sole failed counted requirement | [r2](../../archive/c92_read_r2_Mars.exe-20260913-03.50.53.log) |
| MEASURED r3, prep `4586e9d` | confirmed failed normal reveal/research route; compared proposed filters read-only | [r3](../../archive/c92_read_r3_Mars.exe-20260913-03.53.17.log) |

**MEASURED r1 diagnostic error**, at process Lua age 45.353 s, caught by pcall:

```text
[mod] [C92READ] CENSUS ok=false result=CommonLua/Core/localization.lua:501: invalid value (table) at index 1 in table for 'concat'
```

Cause pinned: `ModsLoaded` contains mod tables; the diagnostic tried to
`table.concat` them. r2/r3 log each `mod.id` and complete. This error invalidates
r1's unfinished census, not r2/r3's successful independent loads.

**MEASURED unexplained boot diagnostics**, recurring before the save census,
around Lua age 19-20 s in each transcript (wording below from r3):

```text
[Braze] SessionStart error The server name or address could not be resolved
[Braze] Failed sending launcher ev The server name or address could not be resolved
[Braze] Failed to init
```

No attribution of these lines to C92 or dismissal as harmless. The archived logs
retain both repetitions and their timestamps. The existing Opt-In NoHomeless
self-check warning is also retained with its subsequent `applied` line; it was
not changed in this investigation.

## Solution options for the fix agent

| option | evidence and tradeoff |
|---|---|
| INFERRED recommendation: exempt only this unreachable hidden preset in the achievement's predicate | r3's read-only comparison passes. Preserve all other requirements, including each repeatable's first completion, and the existing tracked-group list. Scope the exemption to the shipped orphan shape; decline when a vendor change supplies a normal route. |
| INFERRED alternative: make Underground Exploitation a normal accessible tech | Repairs reachability instead of the achievement filter, but exposes the authored 20% underground-production benefit and changes gameplay. It needs a real placement/prerequisite design; simply setting a researched flag is not a repair. |
| SOURCE rejected: exempt repeatables | r3 still fails on the hidden ordinary Tech. It also drops their existing first-completion requirement. |
| SOURCE risk: ignore every currently hidden tech, or set this preset Obsolete | Hidden ordinary techs can be legitimate future requirements. Obsolete changes the shared preset iterator and all its consumers, rather than the achievement alone. Avoid these broad changes. |

**SOURCE patch seam:** The vanilla filter and group list are file locals in
`Lua/Achievements.lua`; a mod cannot assign that local filter by name. A focused
additional achievement listener can evaluate the existing groups with the narrow
exemption and call the engine's normal `AchievementUnlock`, preserving the vanilla
listener and other sponsor achievements. Do not globally redefine
`IsTechResearched` or `Research:IsTechGroupResearched` to manufacture completion.
The declaring class for the latter is `Research`, not `Colony`.

**SOURCE recovery trap:** The vanilla listener returns on `not first_time`
(`Achievements.lua:21-23`). In this save both repeatables have already completed
once. Merely correcting a filter while retaining that event gate leaves the
reporter without a remaining ordinary first completion. A fix must specify its
recovery trigger: a repeat research event may re-evaluate the corrected predicate,
and/or a properly ordered post-load check may award already eligible colonies.
The engine's own account/platform/tutorial/rule restrictions still apply.

**INFERRED acceptance demands:** On a copy, confirm that the corrected predicate
accepts this completed save; still refuses a never-completed repeatable and a
missing ordinary tech; and re-evaluates an already-completed colony without
forcing a tech flag. Check behavioral decline on the frozen 1.0.7 branch and on
a hypothetical vendor repair that connects/reveals this preset. A live award
outcome needs an eligible account; the owner's already-unlocked account cannot
witness a first award for this achievement.

Terraforming's omission from the vanilla list is separate scope. Adding it
would strengthen the requirement and does not repair this blocker. No scope
decision or player reply is requested by this investigation.

## Close-out

**MEASURED:** Each process quit normally before log capture and disarm. The kit
returned to its original metadata bytes; the arming helper's removal of the
existing disarmed ForceInactive comment was explicitly reversed after verifying
that it was the only delta. The temporary Code payload and staged save are gone.

**MEASURED:** Before any load, all autosaves were backed up to
`C:\Dev\SMR-C92-Evidence-20260913`. SHA256 comparisons after the final run show
`Autosave Sol 490.savegame.sav`, `Autosave Sol 56.savegame.sav` and
`Autosave Sol 6.savegame.sav` unchanged. The Downloads original and its pre-existing
import in Saved Games remain byte-identical. No save was written by the diagnostic.

---

# Addendum 2026-09-13 — accident vs deliberate, the finishing route, asset inventory

Second pass, `smr-bugfixpack-f4`, answering the owner's question: **why is the tech
hidden — accident, or did the devs bench it because it was not ready?** Desk only;
no game launched, no save touched, no shipped Lua changed. This addendum does not
revisit the r1/r2/r3 live census above; it takes that as established.

**Provenance.** All code and preset citations are SOURCE, read from the archived
`C:\Dev\SMR-SrcArchive\1.1.0.403908\Src`. Installed build re-confirmed as
`buildid 24995074` from `appmanifest_3215050.acf` (`EF-075`'s build). Localisation
is MEASURED from the live install's shipped packs.

⚠️ **Recorded trap, cost ~6 commands here.** `A:\SteamLibrary\steamapps\common\Surviving Mars`
is app **464920, the ORIGINAL game** — not ours. Relaunched (app 3215050) has
`"installdir" "Project Spark"`. The wrong tree has `.hpk` packs, no `ModTools\Src`,
and a 7-digit loc id space; ours has `.fpk` packs, `ModTools\Src`, and 12-digit ids.
Searches against the wrong tree returned clean, confident, meaningless negatives —
caught only because the presence controls failed too. ⛔ Resolve the game path from
the appmanifest `installdir`, never from the folder name.

## Verdict: ACCIDENT, and the shape of it

**SOURCE:** The devs' retirement idiom is `Obsolete = true`, and they used it **three
times in this very change**: on `LawDef Policy_UndergroundExploitation`
(`Data/LawDef/LawDef-Economy.lua:1428`), on `PolicyDef UndergroundExploitation`
(`Data/PolicyDef.lua:202`), and on `SelfSufficientLighting` — a tech in the **same
`Underground_1` group**. `UndergroundExploitation` carries none of it.

**SOURCE census, `Data/Tech.lua`, 441 Tech presets:** 10 obsolete techs across the
ordinary groups; **zero are hidden**. 218 hidden techs; **zero are obsolete**. The two
idioms never overlap. `Unknown` is documented as *"Shown with a question mark until
enabled by a script"* (`Lua/TechTree.lua:257`), so the flag pair asserts *this is
meant to be revealed*, not *this is withdrawn*.

**SOURCE:** They wired a live consumer to it. `SingleResourceProducer:CalcProductionAmount`
(`Lua/Buildings/BuildingComponents.lua:1358-1364`) is a line-for-line port of the 1.0.7
law check (`1.0.7 Src/Lua/Buildings/BuildingComponents.lua:1083-1087`) onto
`UIColony:IsTechResearched("UndergroundExploitation")`, and *tightened* on the way with
an `IsInLabel("Extractors")` test the law version lacked.

**SOURCE:** They migrated existing saves off the law with no replacement grant —
`SavegameFixups.ObsoleteUndergroundExploitationLaw()` (`Lua/Factions/Laws.lua:773-775`).

**SOURCE control, the sibling migrations:** the four other laws retired in that same
batch (`RedTapeReduction`, `Policy_NativeFood`, `Policy_MoralValues`,
`Policy_UndergroundMiningPermits`) have **no replacement Tech preset at all**. They were
genuinely cut. `UndergroundExploitation` alone got a full replacement tech plus rewired
code — a deliberate promotion, not a cut.

**SOURCE, 1.0.7 side:** the law was live there — real `Prerequisite` (disabled only
under `NoUndergroundAndAsteroids`), `upkeep_rp = 100`, and a designer note
`TODO = set( "Balance" )`. The law→tech promotion *is* that pending work.

⇒ **The flags are authoring leftovers, not a bench.** A refutation of this would need
either an `Obsolete` marking, a cut sibling that kept its consumer, or a named reveal
route. None exists. ⚠️ What this verdict depends on (rule 5a): it holds while no script
in the shipped tree unlocks the preset. The only references to the id anywhere in Src
are its own preset, the retired law/policy, the savegame fixup and the consumer.

## The second defect, larger than the achievement

**SOURCE:** The +20% underground-extractor bonus **shipped and worked in 1.0.7** via the
law. In 1.1.0 the law is obsolete and stripped from saves, and its replacement is
unreachable. So the bonus **cannot be obtained by anyone on 1.1.0**, and players who
carried the enacted law across the patch lost it silently with no route back. The
achievement is the symptom a player happened to notice; this is the underlying loss.

## Can the wiring be finished? Yes — one call

**SOURCE, traced end to end:** `UnlockTech(tech_id, queue, notify)`
(`CommonLua/Libs/Research/Research.lua:31-38`) calls `UnhideTech`, removing both
`"hidden"` lock reasons, then removes both `"locked"` reasons ⇒ state `enabled`
⇒ `Tech:IsVisibleOnMap` passes (it rejects only `"hidden"`, `Lua/TechTree.lua:434-436`)
⇒ `Player:CanResearch` accepts (`state == "enabled"`, `CanBeResearched` defaults true,
one tech point — `Lua/TechTree.lua:868-873`). The game's own override
(`Lua/TechTree.lua:1274-1282`) additionally fires `Msg("TechUnlocked", ...)`.

**SOURCE, why it cannot self-heal:** `UnhideUnlockedTechs` (`:182-192`) unhides only
what `CheckUnlockPrerequisites` passes; with no `RequireTech` that branch requires
`IsTechUnlocked`, which requires state `enabled`, which being hidden prevents
(`:443-459`). Circular. An explicit `UnlockTech` bypasses the loop.

**SOURCE:** `Research:TechCost` returns 0 (`Lua/Research.lua:339-341`) — Relaunched
prices research in tech points, so there is **no per-tech cost to author**.

## Asset inventory — what is and is not built

| component | state |
|---|---|
| DisplayName / Description / ShortDescription / flavor | built |
| localisation, all 8 shipped languages | **complete, 4/4 strings each** |
| `Effect_ModifyLabel` (declarative) | built; targets `UndergroundWaterExtractor`, a live label (`Lua/Buildings/WaterExtractor.lua:56-63,142`) |
| hardcoded consumer | built (above) |
| `Parameters` 20%, comment "Production Buff" | built |
| research cost | N/A — tech-point system |
| old law retired + saves migrated | done |
| **Icon** | **placeholder** — see below |
| **tree position** | **parked outside the main tree** — see below |
| **`RequireTech`** | **absent** |
| **reveal trigger** | **absent** |

**MEASURED, localisation.** `python tools/flpk_extract.py`'s `extract()` run against
`A:\SteamLibrary\steamapps\common\Project Spark\Local\*.fpk` yields
`CurrentLanguage/Game.csv` per language. The tech's four loc ids — `218141292199`
(DisplayName), `483192202247` (Description), `632638598166` (ShortDescription),
`118750111326` (flavor) — are **translated in all eight**: German, French, Brazilian,
Polish, Russian, Schinese, Spanish, Turkish. Presence control `516867455139`
(`UndergroundDeepMining` DisplayName) translated in every file. **SOURCE:** all four ids
are **absent from the 1.0.7 tree** and differ from the law's ids, so they are new strings
authored for 1.1.0 — including new flavour prose the law never had.

⇒ **INFERRED:** eight translation vendors were paid to localise flavour text for this
tech. That is shipping-content spend, not cut-content spend. This is the single
strongest signal that it was meant to go live.

## The icon, and how the mistake probably happened

**SOURCE:** `Icon = "UI/Icons/Research/advanced_drone_drive.png"` — the icon of the
`AdvancedDroneDrive` **breakthrough**. Of 312 distinct icons across the 441 presets,
only 9 are shared, and every other share is a legitimate tier family (`WildfireCure_1..10`,
`FasterTrains`/`EvenFasterTrains`, the generic `story_bit.png`, the `_1.._3` mystery
tiers). `AdvancedDroneDrive` + `UndergroundExploitation` is the **only unrelated pair in
the dataset**.

**SOURCE:** `UndergroundExploitation` sits at `MapPos = point(14576, 4352)`.
`AdvancedDroneDrive` sits at `point(14428, 3584)` — exactly **one hex column** away
(`hex_width = 148`, `hex_radius = 128`, `Lua/TechTree.lua:425-427`). Both are in the
Breakthroughs field's coordinate region (x ≈ 13096–15316); the entire main tech tree
lives at x ≈ 5918–10432.

⇒ **INFERRED, mechanism:** the preset looks like a **duplicate of the breakthrough node
beside it in the editor**, inheriting that node's `Icon`, `LockState = "hidden"` and
`Unknown = true` — all three correct defaults for a Breakthrough — then re-authored as an
Underground tech (new group, strings, parameter, effect) and never moved into the tree
or un-flagged. ⚠️ This is a story about intent and is labelled INFERRED. **It does not
carry the verdict**; the verdict rests on the five SOURCE controls above. Position alone
proves nothing either way: the obsolete `ModularIndustry` is parked in the same region
(`point(14724, 5376)`), so retired *and* unplaced nodes both end up there.

## Double application if it is simply unlocked

**SOURCE:** a `WaterExtractor` is `disabled_in_environment = set( "Asteroid" )` — so it
**can** be built underground — carries `label4 = "Extractors"`
(`Lua/BuildingTemplate/WaterExtractor.generated.lua`), and is added to
`UndergroundWaterExtractor` when underground. Both effects therefore fire on the same
building: the declarative +20% on `water_production` **and** the consumer's ×1.20.
Underground water extractors would compound to ≈+44% while underground metals, rare
metals, exotic minerals and concrete get the advertised +20%. ⛔ Nobody specified that
split — it is a third unfinished edge, and an argument against "just unlock it".

## Tree geometry — the layout motif, and a SEPARATE lead

**SOURCE, derived from every non-Breakthrough/Mystery/Storybit `MapPos`:** the dominant
layout motif is a **ring of six techs around an empty centre hex**. 17 groups have a
complete 6/6 ring; several others are chains or stars rather than rings. **An empty hex
at a group's centre is normal and is NOT evidence of a missing tech.**

Groups whose shape *is* a ring but is short of six:

| group | live nodes | ring occupancy | empty ring slot |
|---|---|---|---|
| **Hi-Tech_1** | 5 | **5/6** | **(7768, 2816)** |
| Space_3 | 6 | 5/6 | — (one node sits off-ring) |
| Hi_tech_3 | 4 | 4/6 | two short |
| Industry_5 | 4 | 4/6 | two short |
| Terraforming_1 | 4 | 4/6 | two short |

⭐ **Hi-Tech_1 is the only group in the game whose node count equals its ring occupancy
AND is exactly one short** — all five of its techs are in the ring, and one ring slot at
`(7768, 2816)` is empty. That is the cleanest "a node is missing here" signature in the
tree, and it was spotted by the owner from the tech-tree screen before any of this was
computed.

⚠️ **But it is probably NOT where `UndergroundExploitation` belongs**, for two reasons:
the preset declares `group = "Underground_1"`, and **`Underground_1`'s ring is complete
(6/6, centre `(9544, 3584)`)** with three satellites hanging off it
(`UndergroundWaterExtraction`, `UndergroundDeepMining`, `RemoteFarming`); and Hi-Tech_1's
members are power/manufacturing themed (`MicroManufacturing`, `AtomicAccumulator`,
`AccumulatorDurability`, `StirlingGenerator`, `MineralApplications_MineralTreatments`),
which an underground-extractor buff does not fit.

⇒ **Two separate leads, do not merge them.** (a) Where `UndergroundExploitation` belongs
— most likely a fourth satellite off the `Underground_1` ring near
`UndergroundWaterExtraction (9322, 3200)` / `UndergroundDeepMining (9766, 3200)`, which
are its thematic neighbours. (b) **Hi-Tech_1's empty ring slot may be a second, unrelated
missing tech** — a candidate defect in its own right, never previously looked at here.

### Theme, and the bridge slot (owner's read, 2026-09-13)

**Owner's observation, authority:** *"most of the hi-tech items seem to follow the flavor
of power and science, whereas industry is more production based."* **SOURCE, member
names bear this out.** Hi-Tech_1 = `MicroManufacturing`, `AtomicAccumulator`,
`AccumulatorDurability`, `StirlingGenerator`, `MineralApplications_MineralTreatments` —
power storage/generation and materials science. Industry_5 = `WasteRockLiquefaction`,
`ContinuousOperationProtocols`, `FactoryAI`, `ThermalCyclingDampeners` (+ obsolete
`ClosedLoopExtraction`) — production throughput. **An extractor-output buff is Industry
flavour, not Hi-Tech flavour.** This retires Hi-Tech_1 as a placement candidate for
*this* tech on theme grounds as well as on the `group = "Underground_1"` declaration —
and it leaves Hi-Tech_1's empty slot standing as lead (b), something else's hole.

**SOURCE, Industry_5's two empty ring slots:** `(10062, 2944)` and `(9988, 2816)`.

⭐ **SOURCE, the bridge slot.** `(9914, 3200)` is empty and adjacent to **three** live
techs across two groups: `Underground_1/UndergroundDeepMining (9766, 3200)`,
`Industry_5/FactoryAI (9840, 3072)` and `Industry_5/ThermalCyclingDampeners (9988, 3072)`.
It is the one empty hex that touches both the Underground satellite row and the Industry_5
cluster. ⚠️ It is **not** an Industry_5 ring slot — it sits below that ring — so this is a
shape observation, not a claim that the devs reserved it.

**SOURCE, the Underground satellite row at y = 3200** holds
`UndergroundWaterExtraction (9322)` and `UndergroundDeepMining (9766)` with the hexes at
`9470`, `9618` and `9914` empty between and after them.

⛔ None of the above is a placement verdict. It is the geometry a placement specialist
should start from, and it must be checked against `RequireTech` reachability (a node with
no incoming connection stays unreachable wherever it is drawn) before anyone proposes a
slot.

## The icon question, ANSWERED from the shipped art pack

**MEASURED.** `Packs\UI.fpk` (852 MB) is FLPK, the format `tools/flpk_extract.py` reads.
Parsing its directory table alone (header `dir_off` @0x0C, `dir_size` @0x14) enumerates
**5001 entries** without extracting payloads.

**Instrument soundness — the presence side, counted.** `Icons/Research/` holds **371**
assets. `Data/Tech.lua` references **312** distinct research icons, and **all 312 are
present in the pack — zero missing**. Three named controls resolved:
`advanced_drone_drive.dds`, `self_sufficient_lighting.dds`, `underground_deep_mining.dds`.
⇒ A negative from this enumeration is a real sample, not an `EF-088` non-result.

⛔ **MEASURED: there is NO research-tree icon for this tech.** No
`Icons/Research/underground_exploitation*` exists, under that or any near spelling.

✅ **MEASURED: the LAW art does exist — three variants.**
`IconsRemaster/Laws/underground_exploitation_1.dds`, `_2.dds`, `_3.dds`. The `PolicyDef`
references `_1`. So the art commissioned for this content is 1.0.7 law-panel art; a
research-tree icon was never made, which is exactly why the preset points at a
breakthrough's icon.

⇒ **The owner's hypothesis is half right, and the half that holds is bigger than the
tech.** There is no hidden icon for *this* tech — but the pack does carry unused research
art. **22 research icons are referenced by no tech at all**, and after removing the `rm_*`
research-map chrome and the `researched`/`obsolete_4` sprites, **19 of them name a
technology that does not exist anywhere in the shipped tree**:

```
advanced_asteroid_economy      advanced_elevator_hydraulics   advanced_landing_techniques
capture_asteroids              crawling_hyperdome             educating_mars
eureka                         grand_engineering              metal_foams
micro-g_vehicles               near_orbit_observatory         polymer_autosynthesis
proximity_power_resonance      smart_alloys                   standardized_integration
terraforming_mars              underground_trains             vacuum_rail_systems
vehicle_optimization
```

(The other three orphans — `decommission_protocol`, `low-g_fungi`, `mars_hype` — do match
live tech ids that simply reference different icon files.)

**MEASURED control:** those 19 names have **no loc strings** in the Relaunched export
`ModTools\Game.csv` (control: a shipped tech name resolves). So they are **art-only**
orphans — art commissioned, tech never authored or dropped before localisation. That is
the **opposite** shape to `UndergroundExploitation`, which has strings, translations in
eight languages, a parameter, an effect and a live consumer, and lacks only the icon and
the wiring. ⇒ The two are different kinds of debris from the same rebuild; do not merge
them.

⭐ `proximity_power_resonance` is power-flavoured and therefore a candidate for the
**Hi-Tech_1 empty ring slot** (lead b). Unverified — offered as a lead, not a finding.

## ⭐ The sibling cohort: the other law→tech conversions

*Owner's question, 2026-09-13: did any other laws become techs, and if so did they reuse
the law icon? Both halves answer decisively, and this is the strongest evidence in the
investigation — a batch of siblings where every other member was finished.*

**SOURCE, the icon convention is absolute.** Every one of the **356** `Icon` values in
`Data/Tech.lua` (312 distinct) points into `UI/Icons/Research/`. **Zero** Tech preset
uses an `IconsRemaster/Laws/` icon. ⇒ **No, the law icon is never reused as a tech icon**,
and a fix or dev report proposing the existing law art would be breaking a 356/356
convention.

**SOURCE, the conversions.** Matching 1.0.7 `PolicyDef` ids against 1.1.0 `Tech` ids finds
**five** law→tech conversions. Each got a **brand-new bespoke research icon under a new
name** — the law art was abandoned every time:

| converted id | 1.0.7 law icon | 1.1.0 tech icon | group | hidden | `RequireTech` |
|---|---|---|---|---|---|
| `DroneHubEfficiency` | `Laws/drone_hub_efficiency_1` | `Research/high_capacity_drone_networks` | Logistics_2 | no | **yes** |
| `ShuttleFuelEfficiency` | `Laws/shuttle_fuel_efficiency_1` | `Research/shuttle_fuel_conservation` | Logistics_3 | no | **yes** |
| `SensorTowers` | `Laws/sensor_towers_1` | `Research/extra_scanning_speed` | Space_1 | no | **yes** |
| `MartianDiet` | `Laws/diet_1` | `Research/martian_diet` | Breakthroughs | yes | no |
| **`UndergroundExploitation`** | `Laws/underground_exploitation_1` | **`Research/advanced_drone_drive`** ⛔ borrowed | Underground_1 | **yes** | **no** |

⭐ **Four of the five were finished; one was not — and it is ours.** Three landed in an
ordinary group with a connection and bespoke art. `MartianDiet` landed in **Breakthroughs**,
where `hidden` + no `RequireTech` is the *correct* configuration — so it is not a
counterexample but a **control**: it shows the devs set those flags deliberately and
correctly when the destination was right. `UndergroundExploitation` is the only conversion
that received neither a bespoke icon nor a connection.

**SOURCE, bounding the set (a total is not a set).** 1.1.0 carries **37** obsolete
`LawDef`/`PolicyDef` entries. Only 4 of them have a same-id Tech
(`DroneHubEfficiency`, `MartianDiet`, `ShuttleFuelEfficiency`, `UndergroundExploitation`);
`SensorTowers` is the fifth id-match but its `PolicyDef` is **not** marked obsolete. No
obsolete law shares a `DisplayName` loc id with any Tech, so there are **no renamed
conversions hiding** outside this cohort — the other ~32 retired laws were simply cut with
no tech replacement.

⇒ **This closes the accident question.** A deliberate bench would not produce one
unfinished member inside a batch of five where the other four are complete, nor leave it
pointing at a neighbouring breakthrough's art while its own conversion siblings each
received new art.

⇒ **Consequence for any repair, ours or the vendor's:** the expected finished state is a
**bespoke `UI/Icons/Research/*` icon that does not exist and has never been drawn**. The
vendor cannot finish this tech without commissioning art. That is a concrete, checkable
ask for the dev report.

## Position provenance, and what 1.0.7 can and cannot tell us

*This section follows two routes the owner proposed on 2026-09-13: trace how a tech that
IS on the web got its position, and mine 1.0.7's themes for hints. Both were run. One
correction to an earlier claim in this addendum falls out of them.*

**SOURCE, how a tech gets its position: by hand, and nothing records why.**
`Data/Tech.lua` is `-- GENERATED BY Tech Editor (Ctrl-Alt-T) DO NOT EDIT MANUALLY!`, and
`MapPos` is a plain `point2d` editor property (`CommonLua/X/XPresetMap.lua:9`). Every
engine reference to it (`Lua/TechTree.lua:104`, `:1703-1705`, `:2018`,
`XDef/XTechTree.generated.lua:734`) only ever **reads** it. `Tech:SnapPos` is an editor
helper that rounds a dragged point to the hex grid. ⇒ **There is no generator, no layout
rule and no derivation to invert.** A designer dragged each node. Tracing any node back
yields no "why" — the *semantic* structure of the tree is `RequireTech`, and `MapPos` is
only how it is drawn.

⚠️ **CORRECTION to "no cross-version layout diff is possible" above.** That is true of
*coordinates* — 1.0.7 has no `MapPos` on anything — but it was too strong. **1.0.7 does
carry positional and thematic data in a different currency**, and a mapping IS derivable:

- **SOURCE:** `Data/TechPreset.lua`, **264** presets, each with a `group` **theme**:
  `Biotech` 21 · `Engineering` 21 · `Physics` 21 · `Robotics` 21 · `Social` 21 ·
  `Terraforming` 21 · `ReconAndExpansion` 23 · `BuriedWonders` 6 · `Independence` 5, plus
  `Breakthroughs` 67 / `Storybits` 20 / `Mysteries` 17.
- **SOURCE:** **153** presets carry `position = range(a, b)` — **not a coordinate, a tier
  band** (which research column the tech may appear in), the old Surviving Mars model.
  `SortKey` is present on 233.

⇒ **A live evidence route, not yet taken:** map 1.0.7 `theme` + `tier band` onto the 1.1.0
group each surviving tech landed in. That yields the rebuild's actual placement convention
from data rather than taste, and lets a converted item be placed **by analogy with how
other converted content was placed**. ⚠️ It cannot locate `UndergroundExploitation`
directly — in 1.0.7 it was a law, not a `TechPreset`, so it has no theme or tier band to
carry forward. It constrains the answer; it does not hand it over.

## ⚠️ Correction: the orphan icons are mostly NOT dropped 1.0.7 techs

Tested rather than assumed, against `Data/TechPreset.lua`:

| orphan icon | 1.0.7 tech? | 1.1.0 tech? | 1.0.7 theme |
|---|---|---|---|
| `advanced_landing_techniques` | **yes** | no | `ReconAndExpansion` |
| `underground_trains` | **yes** | no | `ReconAndExpansion` |
| `decommission_protocol` | yes | yes | `Engineering` |
| `low-g_fungi` | yes | yes | `Biotech` |
| `mars_hype` | yes | yes | `Social` |
| the other **17** | no | no | — |

⇒ **Only 2 of 22 are genuinely techs dropped in the rebuild** (`AdvancedLandingTechniques`,
`UndergroundTrains` — both `ReconAndExpansion`, a theme 1.1.0 dissolved); 3 more still
exist under different icon files. **17 match no tech in either version.** So the earlier
framing of the orphan set as debris from this rebuild is **only partly right** and should
not be relied on. Their origin — original-game (app 464920) legacy art, or art for
content never authored in either version — is **NOT ESTABLISHED**.

⚠️ This weakens but does not remove the `proximity_power_resonance` → Hi-Tech_1 lead: that
icon matches no tech in 1.0.7 *or* 1.1.0, so nothing dates it to this rebuild.

## ⭐ Residue risk, and whether each route can fail cleanly

*Owner's question, 2026-09-13: if we FINISH the work rather than bypass it, what is left
behind when the devs eventually fix it — and can our fix fail cleanly when that patch
drops? Both halves answer from source. The two routes have **opposite** residue shapes,
and that asymmetry is an argument on its own.*

### Route A — BYPASS (the achievement exemption, standing recommendation)

**SOURCE: it writes nothing to the save.** A focused listener evaluates the corrected
predicate and calls the engine's `AchievementUnlock`. The residue is an achievement flag
on the **account/platform** — which is the intended outcome and the thing the reporter
asked for. Nothing of ours enters the savegame. Three-tier ethos: layer 1–2.

✅ **It CAN fail cleanly, and the decline is a behaviour test, never a version label**
(`FIX_POLICY` §2a). Any one of four shapes means stand down:

1. `next(Techs.UndergroundExploitation.RequireTech)` is non-empty — it got connected;
2. its `LockState` is no longer `"hidden"` — it got revealed;
3. the preset reports `Obsolete` — retired, so vanilla's own iterator skips it and the
   achievement passes unaided;
4. the preset is absent entirely.

In all four we do nothing and vanilla handles it.

⛔ **The decline is REQUIRED, not optional.** If the devs wire the tech properly and we
keep exempting it, we award the achievement to players who genuinely have **not**
researched a now-reachable technology — we would be shipping the inverse defect. Any
build of this fix must carry the test.

### Route B — FINISH THE WORK (unlock / place the tech)

**SOURCE: the unlock is persisted.** `LockablePresetOwner` declares `PresetLockStates` and
`ProcessedLockablePresets` as properties (`CommonLua/Features/LockablePreset.lua:5-16`),
held on the `Player` (`CommonLua/Classes/Player.lua:10`) and written by
`RemovePresetLockStateReason` (`:190-201`). `UnlockTech` therefore writes
`PresetLockStates.Tech.UndergroundExploitation` **into the savegame**.

**SOURCE: research completion is persisted too**, in `UIPlayer.tech_researched`, and is
**indistinguishable from a legitimately researched tech**.

⛔ **The decisive point: the +20% consumer is VANILLA code.**
`SingleResourceProducer:CalcProductionAmount` gates only on
`UIColony:IsTechResearched("UndergroundExploitation")`
(`Lua/Buildings/BuildingComponents.lua:1358-1364`). Once that flag is true, **the bonus
keeps applying with our pack uninstalled.** The mod is not required to sustain the effect
it caused.

⇒ ⛔ **Route B cannot fail cleanly, by construction.** A decline test can stop us acting
*again*; nothing undoes what is already written. Uninstalling the pack does not remove the
bonus. A vendor patch does not remove it. Reversing it would mean clearing a vanilla
researched flag — destructive, and it robs the player of the tech point they spent.
Under the three-tier ethos that is **layer 3, harmful trace**, which §3a accepts only
**paired with a remedy**, with a recorded per-site disposition. It compounds with the
double-application: the permanent, unremovable change is ≈+44% on underground water
extractors, not the advertised +20%.

### What happens when the devs actually fix it

| vendor action | Route A (bypass) | Route B (finished work) |
|---|---|---|
| **wires it** (adds `RequireTech`, unhides) | declines on test 1 or 2 — clean | player already holds it, obtained without the prerequisite; bonus stands |
| **retires it** (`Obsolete = true`) | declines on test 3 — becomes a no-op | ⛔ **residue turns silent and permanent** — see below |
| **ships a savegame fixup** | unaffected | the one mechanism that could clean it — see below |

✅ **Refuted — an obsolete retirement does NOT crash.** I expected
`Techs.UndergroundExploitation:GetParameterValue(...)` to nil-index once the preset went
obsolete. It does not: obsolete presets are *"kept for backwards compatibility"*
(`CommonLua/Preset.lua:85-88`) and only the **iterators** skip them (`:1773`, `:1808`,
`:1894`), so the id still resolves. No error.

⛔ **But that is exactly what makes retirement the worst case for Route B.** The tech
disappears from the tech tree (iterators skip it), while `tech_researched` stays true and
the vanilla consumer keeps paying the bonus — **a permanent balance change with no UI
trace and no route for the player to see or undo it.**

✅ **One reassurance for Route B.** Fixups are gated by the `AppliedSavegameFixups`
GameVar, and any fixup **added after a save was created** runs on that save
(`CommonLua/SavegameFixup.lua:10-40`). Our pack changes neither `lua_revision` nor that
var, so a vendor remedy would still reach a save we had touched. ⚠️ That depends entirely
on the vendor choosing to write one, which we cannot assume and must not plan around.

### Verdict

**The residue asymmetry is an independent argument for the bypass.** Route A puts nothing
in the save and stands down on four behaviour tests. Route B writes self-sustaining
vanilla state that neither uninstalling the pack nor patching the game removes, and whose
worst case is silent and permanent. ⇒ This reinforces the standing recommendation without
relying on any of the earlier reasoning.

## Not opened

- **Where the tech was *intended* to sit.** No positive evidence was found — only the
  geometry above, which is INFERENCE. The cross-version diff is ruled out (previous
  section). Untried evidence routes: the `Data.fpk` shipped preset blob (may differ from
  `ModTools\Src`), `.dds` mtimes or pack ordering inside `UI.fpk`, and the DLC packs
  `norman.fpk` / `thomas.fpk`.
- Whether the three law `.dds` variants differ in art or only in tier decoration — not
  extracted or viewed.
- Any DLC-supplied unlock route beyond the Src tree's `Data/` and `DLC/` folders.
- Whether the vanilla tree renders the parked node on-screen at all, or clips it.
- The 19 orphan icons were not traced to any cut feature, and no entry was filed for them.
- No fix was built, no module written, no public row drafted.
