# C92 placement, assets and scope

Investigation, 2026-09-13. Starting HEAD `ccd4ff5`;
installed app 3215050, Steam build 24995074, game 1.1.0.403908.
Report only; no game launch or fix implementation.

## Live progress

- [x] Resolve brief, read state and bindings, refresh shared checkout.
- [x] Packed-data, full icon survey, placement and production/residue checks.
- [x] Owner's additional Industry/Hi-Tech icon/effect comparison.
- [x] Reconcile evidence and answer Q1–Q5, including refutations and blind spots.
- [x] Update C92 and add the marked owner decision to the checklist.
- [x] Consume the brief and complete doccheck/evidence review.
- [x] Prepare the reviewed report/evidence for commit and push; delivery receipt
  is recorded in the session's final response and Git history.

## Findings that change the previous answer

**MEASURED:** the earlier **44% water-bonus claim is wrong**. The declarative
water modifier and hardcoded stockpile multiplier serve separate production
paths. Offline execution of the shipped bodies produces 5000 → 6000 for each,
with no second water multiplication. Reapplying the same keyed effect does
not stack it. [Production controls](c92-placement/SCOPE_RESIDUE.md).

**SOURCE:** the old five-member conversion census was incomplete and
misclassified one member. Renamed underground laws became
`UndergroundDeepMining` and `UndergroundWaterExtraction`; a named migration
function explicitly lists their old laws. **MartianDiet already existed in
1.0.7 with the same research icon**, so it was not a new conversion/art control.
[Authoring evidence](c92-placement/PLACEMENT_EVIDENCE.md).

**MEASURED:** no dedicated research illustration was identified. The unused
images include old-game artwork, renamed old technologies and identical
funding pictures under different filenames. **“Never drawn” is withdrawn**;
an installed-asset search cannot establish that. The owner's Industry/Hi-Tech
lead found plausible substitute art but no recovered assignment to C92.
[Icon evidence](c92-placement/ICON_HUNT.md).

**SOURCE + MEASURED:** restoration leaves vanilla state after removal, but
“unremovable” was too strong. Clearing the completion flag and removing the
original keyed water modifier stops both bonuses in desk controls. That is
not a tested save migration/refund contract. Obsolete-only retirement and
actual preset deletion also have different consequences.

**OWNER AUTHORITY + MEASURED:** the owner identifies only one Underground
tree, which appears complete; their supplied screenshot shows the complete
Underground I ring. The preset's explicit `Underground_1` assignment establishes
a family, **not an empty seat or a requirement to extend that ring**. Exact
intended placement remains unrecovered.

## Q1 — should the pack fix it?

**INFERRED recommendation: build the narrow achievement repair next, if the
owner selects it; retain technology restoration as an explicit design choice.**
The reporter's achievement barrier is established by the earlier retail
census. Exempting that one verified unreachable requirement repairs the harm
without choosing when a new permanent production benefit becomes available.
The recommendation does not rely on a doubled bonus or an impossibility of
cleanup. C92 remains **`cand`**; no fix or award was attempted here.

**SOURCE + INFERRED:** the non-obsolete ordinary preset, authored content,
rewired consumer and completed siblings strongly suggest unfinished
integration. They do not exclude a deliberate hold by its designer. The
achievement defect does not depend on deciding that intent. Restoration is
plausibly a bug fix, but choosing a prerequisite/seat sets progression and
replaces the old law's upkeep with permanent tech-point access. The available
evidence does not settle that choice.

The selected implementation must meet the existing ship line and
`FIX_POLICY` behavior-based guard/save-safety rules. This report discharges
no live test and creates no new per-change overhaul gate. The inaccessible
technology is useful developer-report material; no external message or
player reply was drafted or sent. Owner decision: checklist **171**.

## Q2 — assets, including the owner's broader category lead

**MEASURED:** the inventory covers all **183** installed FLPK packs and
**58,037** directory entries, with a decoded presence control for every pack.
All **395** research DDS images were decoded and viewed: **371** in base UI
and **24** in Norman. All **312** distinct base Tech icon references resolve.
Thomas has no research-directory art; its two UI images were decoded as controls.

**MEASURED:** the law variants share a cave/magnifier silhouette, in different
colors. **SOURCE:** `_1/_2/_3` encode locked, visible/preparing and
active/prepared UI states, not tiers. This is existing subject-related art;
using it on the research board would be a design substitution.

**MEASURED + SOURCE:** the extra pass selected actual **Industry I–V and
Hi-Tech I–V** groups, pairing **55** presets with their assigned art and effects.
It did not depend on an `underground` filename match.

| Candidate | What the evidence establishes |
|---|---|
| **SOURCE + MEASURED:** `closed_loop_extraction.png`, obsolete Industry V `ClosedLoopExtraction` | Strongest retired extraction-themed image: rock and cycle arrows. Its documented upgrade removes extractor maintenance; it is not an unclaimed C92 asset. **INFERRED:** best existing retired-art substitute to discuss if restoration is selected. |
| **SOURCE + MEASURED:** `continuous_operation_protocols.png`, Industry V | Production diagram already assigned to a separate +15% bonus after uninterrupted operation. **INFERRED:** useful production-theme comparator, no C92 attribution. |
| **SOURCE + MEASURED:** `ExtractorAmplification`, `FueledExtractors`, `DeepWaterExtraction` art | Relevant rigs/machinery already assigned to live Industry technologies. Reuse would be deliberate. |
| **SOURCE:** `EnhancedTopographicalExploitation` and Hi-Tech mineral art | Despite suggestive names, their effects concern wind elevation or solar upgrades. No renamed C92 implementation was recovered. |
| **MEASURED:** unused `metal_foams`, `polymer_autosynthesis`, `smart_alloys` | Industrial imagery exists, but these names/art motifs already occur in the separately controlled ORIGINAL-game pack. Their origin cannot be attributed to this rebuild. |

Other corrected orphan claims: **SOURCE** `capture_asteroids` and
`vehicle_optimization` resolve to archived 1.0.7 technologies under different
IDs. **MEASURED** `crawling_hyperdome` and `near_orbit_observatory` are
pixel-identical to `terraforming_subsidies`; filenames do not prove bespoke
illustrations. Original-game comparisons are explicitly historical and do
not substitute for the current Relaunched census.

**INFERRED:** the narrow achievement repair needs no icon. For a full
restoration, the law glyph or the retired Closed Loop Extraction picture are
reviewable substitutes; neither is proven intended artwork. A new commission
is not established as necessary. See the local
[unused-art/law contact sheet](C:/Dev/C92-placement-scratch/icons/focused_orphans_laws.jpg),
[Industry/Hi-Tech sheet 1](C:/Dev/C92-placement-scratch/icons/industry_hitech_01.jpg)
and [sheet 2](C:/Dev/C92-placement-scratch/icons/industry_hitech_02.jpg).
The full [icon report](c92-placement/ICON_HUNT.md) records provenance and bounds.

## Q3 — authored data and actual production scope

**MEASURED:** [pack_truth.py](c92-placement/pack_truth.py) decodes every Lua
payload in `Data.fpk`, `Lua.fpk`, Norman and Thomas. The target-containing
files, Tech/TechGroup definitions and production-control dependencies match
ModTools source byte for byte. The shipped Data blob supplies no alternate
position/connection; the decoded DLCs contain no named C92 reference.
[Commands, positive controls and hashes](c92-placement/PACK_TRUTH.json).

**SOURCE, 1.1.0.403908:** `Data/Tech.lua:10635` assigns `Underground_1`, parks
the node at `(14576,4352)`, and supplies no preset Comment, TODO, SortKey,
Condition or RequireTech. The parameter comment is only `Production Buff`.
No base Tech has a direct SortKey, so that absence is not exceptional.

**SOURCE:** `SavegameFixups.TransformLawsToTechs_v2`
(`Lua/Factions/Laws.lua:1136`) explicitly names the old underground mining
and water laws. Their successors occupy `(9766,3200)` and `(9322,3200)` in
Underground I and preserve the old `NoUndergroundAndAsteroids` restriction.
**INFERRED:** retaining that restriction is a reasonable restoration choice;
adding a Condition alone does not repair the achievement's counted requirement.

**SOURCE + MEASURED:** the general extractor wording is consistent with two
output systems. Water uses the supply grid and its `water_production` modifier;
stockpiled-resource components use `SingleResourceProducer`. Do not narrow
the text to water or delete either half because of the withdrawn duplicate
theory. The old/new scope is not byte-equivalent: the new hardcoded branch
adds an Extractors-label check, and the new declarative effect covers water.
Byproduct/deposit/prediction interactions were not exhaustively measured.

**SOURCE:** explicit `UnlockTech` clears the circular lock barrier, but
provides no intended map location. Ordinary availability uses `RequireTech`;
multiple connections mean **OR**, not AND. Connecting both siblings would
allow access after either one, so it is a progression choice.

## Q4 — where is the hole?

**No exact intended slot was recovered.** The complete visible Underground
ring and the preset's Underground family assignment are compatible. An added
satellite is a possible design, not a repair compelled by an empty seat.

| Area | Evidence and ranked interpretation |
|---|---|
| **SOURCE + INFERRED:** Underground I satellite row | Strongest family-based candidate. Empty `(9618,3200)` neighbours `UndergroundDeepMining`; `(9470,3200)` neighbours `UndergroundWaterExtraction`. Neither is reserved for C92. |
| **MEASURED + INFERRED:** bridge `(9914,3200)` | Empty beside `UndergroundDeepMining`, `FactoryAI`, `ThermalCyclingDampeners`. Strong geometric bridge; no authored reservation. |
| **MEASURED + INFERRED:** Industry V holes | `(10062,2944)` and `(9988,2816)` are empty. The wider art/effect pass strengthens production-theme relevance, but finds no C92 edge or identity. |
| **MEASURED + INFERRED:** Hi-Tech I hole | `(7768,2816)` is empty beside `AtomicAccumulator` and `MineralApplications_MineralTreatments`. No missing-tech identity or icon assignment established. |

**INFERRED connection ranking, only if restoration is selected:**
`UndergroundDeepMining` first for the broader extractor theme;
`UndergroundWaterExtraction` second for the water half and sibling history.
Neither is a recovered developer-authored connection.

**MEASURED:** historical theme/range mapping does not identify a unique new
cluster. Old Physics range 7–9 splits across Hi-Tech, Sustainability and
Industry; old underground-related techs from widely separated ranges all
land in Underground I. Those ranges describe sequence bands, not coordinates.
[Mapping, slot census and source citations](c92-placement/PLACEMENT_EVIDENCE.md).

**SOURCE:** the designer describes numbered clusters as positional aids and
explicitly leaves space for expansion. An empty ring slot alone therefore
cannot establish a separate missing technology.
[July 14 research diary](https://steamcommunity.com/games/3215050/announcements/detail/699895897307217965).
**MEASURED:** its four original screenshots supply no named C92 node and do
not cover every present hole. The owner's later screenshot supplies the full
visible board; its hash and observation are retained in the placement report.

**INFERRED disposition:** neither the Hi-Tech hole nor the orphan set is a
new defect without missing behavior or a direct authoring link. A historical
named node, reserved edge, editor revision or developer instruction would
supersede the present placement conclusion.

## Q5 — decline and residue

**INFERRED builder contract for the recommended achievement repair:**

1. Keep vanilla's listener; add a synchronous recheck after normal post-load
   fixups and on eligible research events, including repeat completions.
   The first-time-only trigger cannot recover this completed visible tree.
2. Defer until registries/player state are ready. Initialized absent/obsolete
   target means decline without dereferencing it. Missing groups and empty
   registries cannot count as all-complete; use current objects at every event.
3. Match only the known counted, ordinary, hidden, disconnected orphan.
   Decline on changed identity/group/counting status, new final graph edges,
   visibility, retirement/deletion or effective live reveal/research access.
   Inspect symmetric/incoming connections. Insufficient-points `CanResearch`
   nil is a known affordability result; establish the hidden barrier separately.
4. Use vanilla's tracked groups and filter. The callback receives
   `(tech, groupTable)`. Require vanilla's census to fail, the single-target
   exemption to pass, and that target actually to be visited/counted. Another
   incomplete ordinary, repeatable-first-use or hidden tech must still block.
   Do not credit an uncommitted preview queue.
5. Request the result through normal `AchievementUnlock`, retaining provider,
   platform, tutorial, cheat and game-rule restrictions. Do not directly
   change account flags, tech locks or research state. Unknown behavior declines.

The [complete contract and acceptance matrix](c92-placement/SCOPE_RESIDUE.md)
are **builder demands, not a newly implemented/passed guard suite**. A future
scripted grant that leaves all inspected observations identical cannot be
detected universally; ordinary source review after vendor updates remains
necessary. Four field checks do not guarantee automatic retirement.

**SOURCE + MEASURED:** finishing the tech persists lock state, completion,
the colony water label modifier and building modifiers. Removing the mod
does not undo them. Clearing only completion leaves the water modifier;
removing the original stored effect key through the normal label API restores
current water output and stops future label application in desk controls.
Provenance, compensation and saved-state cleanup remain unimplemented.

**MEASURED distinct hypothetical vendor cases:** obsolete-but-retained
preset keeps the bonus; physically deleted preset plus retained flag and
unchanged consumer causes a conditional Lua nil-index error. A coordinated
vendor migration could adopt or remove state instead. This is not a prediction
of a shipped patch or retail crash. The per-site inventory in the scope report
also covers preset changes, purchase history and already-used resources;
no site is preassigned to an unbuilt cleaner. The ordinary account achievement
is the expected lasting result for either route.

## Not opened / limits

- No game launch, actual award, restored-tech purchase, production play leg,
  save cleanup or disable/reload experiment in this task.
- No studio art source, editor history, deleted assets or historical depot
  download. All installed pack names were examined; arbitrary nonresearch
  textures and atlas contents were not visually exhausted.
- No proof that unused industrial art belongs to C92, or that a complete
  Underground ring requires another seat.
- No exhaustive census of every semantically renamed law conversion. Named
  counterexamples suffice to refute the prior complete-set claim.
- No full byproduct/depletion/prediction audit or migrated old colony.
- The earlier localization evidence was not re-extracted; no recommendation
  depends on inferred commissioning spend or translation-vendor contracts.
- No public report/reply, release module, public promise or status promotion.

## Evidence and validation

Retained instruments: [pack comparison](c92-placement/PACK_TRUTH.json),
[icon census](c92-placement/icon_evidence.json),
[source mapping](c92-placement/placement_inventory.json) and
[production controls](c92-placement/scope_controls.py), with commands and
build/HEAD identity. The primary independently reran the production controls:
**14 passed**. The scope investigation also ran the existing achievement
harness: **15/15 passed**. Neither is retail verification.

**MEASURED validation:** doccheck is GREEN, including the clean TEMPORARY sweep.
The primary reproduced the placement inventory, all icon proof metadata
(identical to the retained evidence), and the existing 15/15 achievement
controls. Local report links resolve and the diff passes whitespace review.
The complete [doccheck transcript](c92-placement/DOCCHECK.txt) preserves its
existing warnings verbatim, including frozen-row discrepancies, the two
over-target skills and the PUSH SET warning; those are outside this report's
scope. No generated index or shipped-code change was needed.
