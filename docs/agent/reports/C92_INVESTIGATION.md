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

## Why no 1.0.7 → 1.1.0 layout diff is possible

**SOURCE:** 1.0.7 has **no hex tech tree**. Its techs are `PlaceObj('TechPreset', …)` in
`Data/TechPreset.lua` with **no `MapPos` anywhere**; the `PlaceObj('Tech', …)` class, the
`MapPos` hex grid and the group rings are all **new in 1.1.0**. The whole tree was rebuilt
for *Services & Science*, which is also the change that converted laws into techs.

⇒ ⛔ **Do not attempt a cross-version layout diff to locate the intended slot** — there is
no prior layout to diff against. It also reframes the defect: this is debris from a
full tech-tree rebuild, which is consistent with 19 further orphaned art assets.

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
