# C92 investigation - hidden Underground Exploitation requirement

2026-09-13. Investigation only; no fix module, achievement award, research
mutation or shipped Lua change. Defect truth: [C92](../bugs/C92.md).

**Correction, placement follow-up 2026-09-13:** the initial census and live
achievement barrier below stand. The later claims of a 44% water bonus, an
exhaustive five-conversion cohort, a never-drawn icon, and unremovable save
residue have been corrected. Current reasoning and evidence are in
[C92_PLACEMENT.md](C92_PLACEMENT.md); historical wording is retained in git.


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

## Intent: unfinished conversion is the leading inference

**SOURCE:** the shipped non-obsolete Tech remains hidden and disconnected,
while its consumer tests research completion and its authored text/effect
promise an underground production bonus. The law and policy are obsolete.
These are contradictory shipping states; the live achievement barrier is
measured independently of why the author left them that way.

**SOURCE correction:** the original sibling census wrongly treated ID/loc-ID
matching as exhaustive. Underground mining and water permits were converted
under different IDs into `UndergroundDeepMining` and
`UndergroundWaterExtraction`. `SavegameFixups.TransformLawsToTechs_v2`
(`1.1.0 Lua/Factions/Laws.lua:1136`) explicitly names the former laws in its
conversion list. Conversely, `MartianDiet` was already a 1.0.7 breakthrough;
its same-ID match did not establish a new law-to-tech conversion.

**INFERRED:** unfinished conversion remains the best explanation of the
contradiction and completed neighbouring work. An absence of `Obsolete` is not
proof of a designer's mental intent and cannot exclude a deliberate hold.
The earlier categorical accident verdict and its purportedly exhaustive
control set are withdrawn. [Placement evidence](c92-placement/PLACEMENT_EVIDENCE.md)
records the corrected named cohort and limits.

## The unavailable bonus

**SOURCE:** 1.0.7 had an active-law production route; 1.1.0 removes the law and
requires research of this normally unreachable replacement. New colonies
therefore cannot obtain the authored bonus through the normal route.

**SOURCE limitation:** law-removal fixups describe what happens if an old
colony is successfully migrated. This investigation did not observe an
upgraded old colony losing its law, and the normal 1.0.7-to-1.1.0 save-load
barrier remains in force (`EF-079`). The former claim that players had carried
it across and silently lost it was not a measured field finding.

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

## Correction: the water and stockpile consumers are separate

**SOURCE + MEASURED:** the earlier +44% claim is refuted. Water is produced by
`WaterExtractorBase:ProduceSupply` and the grid's `water_production` callback
(`1.1.0 Lua/Buildings/WaterExtractor.lua:73,125`); the +20% declarative modifier
acts there. Stockpiled resources use
`SingleResourceProducer:CalcProductionAmount` (`BuildingComponents.lua:1356`),
where the hardcoded +20% consumer acts. A label shared by the buildings does
not join those output paths.

**MEASURED:** offline shipped-body controls yield 5000 → 6000 for each output;
the water path does not become 7200. Reapplying the same keyed effect does not
stack a second modifier. Do not change production code to repair the alleged
double application. [Scope/residue evidence](c92-placement/SCOPE_RESIDUE.md)
names fixtures, controls and the unmeasured retail boundary.

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

## Icon search: bounded absence, corrected origin claims

**MEASURED:** base Tech icon paths resolve through the FLPK reader's positive
controls. No dedicated `underground_exploitation` research icon was identified.
The law art exists as the same cave/magnifier glyph in three UI-state colors.
The follow-up expands the search to every installed pack directory and views
all research DDS; [ICON_HUNT.md](c92-placement/ICON_HUNT.md) records the set.

**WITHDRAWN:** the original assertions that the research icon had never been
drawn, that the vendor must commission one, and that all named orphans were
art commissioned for this rebuild. A pack inventory cannot prove those
claims. Two orphan filenames contain pixel-identical funding art, and two
additional names resolve to old technologies missed by ID matching. The
historical original-game pack supplies further provenance controls.

**INFERRED:** an unused image can be considered as a substitute, but visual
suitability does not establish its intended association with this technology.
The target's current Advanced Drone Drive art remains a borrowed asset; its
presence alone does not prove how the preset was authored.

## Corrected sibling cohort

**SOURCE:** Tech presets use research-directory icon paths; this is a shipping
convention, not proof that each file contains newly commissioned artwork.
The old same-ID census omitted renamed underground and asteroid conversions
and included the pre-existing `MartianDiet` breakthrough as a new conversion.
Its “five total, no renamed cases outside the set” conclusion is withdrawn.

**SOURCE:** the two renamed underground successors share the target's explicit
`Underground_1` group, retain the underground game-rule Condition and occupy
its satellite row. This is stronger family evidence than generic production
flavour or ring geometry. It supplies no exact target coordinate or prescribed
connection. The full named comparisons and migration function are in
[PLACEMENT_EVIDENCE.md](c92-placement/PLACEMENT_EVIDENCE.md).

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

## Orphan-icon lineage: follow-up supersedes the ID-only match

**MEASURED:** searches of actual icon references recover `capture_asteroids`
and `vehicle_optimization` from archived 1.0.7 `TechPreset.lua`, despite their
different Tech IDs. Original-game art is a distinct historical comparison,
not the current Relaunched inventory. [ICON_HUNT.md](c92-placement/ICON_HUNT.md)
records those controls, duplicate pixels and unresolved origins.

**INFERRED limit:** an orphan filename is not evidence of a new missing
technology, a commissioned illustration, or an intended tree position.

## Residue: automatic cleanup is absent, removal is possible

**SOURCE:** a narrow achievement recheck need not change tech lock state,
research completion or production modifiers. Its intended lasting result is
the ordinary platform/account achievement. It must still use normal engine
restrictions and decline if the orphan is now reachable, changed, obsolete
or absent. The former four field checks are an incomplete implementation
contract: they also need nil-safe prerequisites, data-readiness handling and
current player-state checks. [C92_PLACEMENT.md](C92_PLACEMENT.md) specifies the
builder contract and recovery for an already-completed colony.

**SOURCE + MEASURED:** completing the tech persists vanilla research/lock
state and the water label modifier. Removal of the mod does not automatically
undo those changes. However, clearing the research flag and removing the
original keyed label modifier stops both bonuses in the offline controls.
The former “unremovable/permanent by construction” conclusion is withdrawn;
this is an unimplemented, unverified cleanup/migration obligation, not an
impossibility proof. A tech-point refund and provenance for prior state still
need a deliberate contract.

**MEASURED distinct vendor cases:** an obsolete retained preset still lets
the unchanged stockpile consumer pay the bonus. A physically deleted preset
with a retained researched flag instead raises a nil-index error at
`1.1.0 BuildingComponents.lua:1362`. Neither case predicts what an actual
future vendor patch will do; coordinated consumer/fixup changes may resolve
it. Declining to make new edits cannot undo old save state by itself.

**INFERRED recommendation:** keep the narrow achievement exemption as the
proposed mod-side repair pending owner scope decision. Restoration is feasible
but requires placement and residue choices. The recommendation no longer
rests on a 44% bonus or a claimed impossibility of cleanup.

## Not opened in the first pass (historical scope)

The placement follow-up opens several routes below; its own Not opened list
is the current boundary. These bullets describe the earlier pass only.

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
