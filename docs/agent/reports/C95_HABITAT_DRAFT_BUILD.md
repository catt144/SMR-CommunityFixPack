# C95 habitat expedition draft — build record, 2026-09-16

**Built, desk-verified and tested-attended on the live 1.1.0 receiver.** Owner authority is
[checklist 185](../../PLAYTEST_CHECKLIST.md), which lifts C95's build/test hold
and retains C96's hold. Repair: main-pack judgment call, excluding habitat
residents from automatic expedition drafting. Release remains a separate task.
The owner supplied the prepared save used by the attended rerun.

Baseline `00259ea6d12b6fabfa6773a6de727b33fb21d4cd`; desk run at
`7c29ecf0d09591a7b10ae9b107477f373fe6b116` plus this change. That intervening
commit changed STATE, the handoff and session archive, not this task's inputs
(`git diff 00259ea..7c29ecf -- <read-path files>` was empty).
Executed model disclosed by this transcript: **GPT-6 / Codex**; no more specific
model identifier is exposed. No delegated agents were used.

Re-point session: code `4ec3e32`, desk suite `b055210`, executed model
**GPT-5 / Codex**; no delegated agents were used.

## Implementation and cost

**SOURCE:** [Fix_HabitatExpeditionDraft.lua](../../../Code/Fix_HabitatExpeditionDraft.lua)
registers `HabitatExpeditionDraft`, with all captured/installed method pairs in
its `Require` block, and is present in both load manifests. It chains both shipped
gathers: legacy `CargoTransporter` guarded to `RocketExpeditionBase`, and
`CargoTransporterNew` guarded to `UniversalRocketBase` in Expedition type. Either
receiver can install if the other is absent. Foreign receivers delegate before field
inspection, and `FilterColonistsByTrait` is swapped only during an expedition gather.
The named predicate is `IsKindOf(unit.residence, "MicroGHabitatBase")`.
Every bucket is filtered before vanilla trait selection, preserving priority,
specialisation, soft-trait relaxation, and filling from subsequent buckets.

**SOURCE:** cost is a fresh eligible array and one protected predicate pass per
visited bucket, plus a protected gather call and a return-tuple table. No timing
benchmark was run. Labels and colonists are never mutated. No migration, saved
fields, new classes, GameVars or threads are introduced: FIX_POLICY layer 3.
Missing residence is a normal false type test, not an unevaluable predicate.
An actual predicate exception leaves that bucket unchanged and silent.

**SOURCE:** the global is captured at each call and restored before returning on
success or failure. Assignment is plain, routed through `ModEnvMeta.__newindex`
(`CommonLua/Modding/Mod.lua:1570-1576`); `rawset` in the mod sandbox would miss the
global read by vanilla. On picker failure, restoration precedes a retry of the
original read-only picker with its original filter. This preserves vanilla's
failure path without using retail `error()` as a rethrow: that function reports
and continues. The retry is safe only while the gather is read-only. A third-party
wrapper adding mutations or yields invalidates that assumption; such wrappers
were not audited.

## Scope and atomicity

**MEASURED:** `python tools/desk_c95_habitat_draft.py`, HEAD `7c29ecf`, installed
Steam build **24995074**, scans decoded `ModTools/Src/**/*.lua`, prints each member
beside its total, and asserts the caller counts. Its filters are literal
`FilterColonistsByTrait(` excluding function declarations, and
`CargoTransporter.Load(` / `self:Load(`. Results:

| Search | Members and reconciliation |
|---|---|
| Filter calls | **4** = CargoTransporter:278 + CargoTransporterNew:272 + LanderRocket:1171 + LanderRocket:1182 |
| Load candidates | **3** = RocketExpedition:536 + LanderRocket:306 + unrelated MapDescriptor:56; therefore **2** CargoTransporter callers |
| Direct inheritors | **3** = RocketBase + RocketExpeditionBase + LanderRocketBase |
| Transitive named DefineClass inheritors | **25**, complete membership printed by the same command; closure starts at CargoTransporter and includes every parsed parent edge, excluding the root itself |

**SOURCE:** RocketExpedition's override explicitly calls the legacy base table field
(`RocketExpedition.lua:497`). Lander overrides the gather with its own passenger
list. Universal rockets inherit `CargoTransporterNew` and enter expedition behavior
by `RocketType`; the New guard excludes elevators and other transport modes.
These are counts of decoded shipped Lua declarations, not runtime mod classes.

**SOURCE:** no yield occurs along either shipped gather path: both gathers,
GetConnectedCitiesForColonists, GetConnectedCities, GetCityLabelWithConnected,
is_colonist_reachable, ValidateBuilding, IsDead, CanChangeCommand/IsTransported,
the trait filter and its local callbacks, and the array helpers were read.
The harness rejects `Sleep`, `WaitMsg`, `WaitWakeup` and thread-creation calls in
its extracted bodies. `table.get`, `IsValid`, `IsKindOf` and primitive array
operations are synchronous engine primitives. `table.copy` can invoke a custom
`__copy`; the shipped colonist label array is the ordinary-array path, not a
foreign metatable contract. No yielding callback is supplied here.
**INFERRED:** on this shipped path the swap cannot be observed by another game
thread or a save. This depends on those callees staying synchronous; a body pin
alone does not prove a future callee or foreign wrapper retains that property.

## Desk evidence and falsifiers

**MEASURED:** `python tools/desk_c95_habitat_draft.py` passes under lupa Lua 5.4,
using extracted shipped gather/filter bodies and ancestry parsed from shipped
class declarations. It models distinct mod and shipped environments. Shims for
native primitives, labels and synthetic objects are named in the script.

Synthetic fixture: Naturalist and Micro-G residents lead the idle/unemployed
bucket; ordinary candidates span idle/unemployed, busy/unemployed, idle/employed
and busy/employed. The colony has exactly the ordinary candidates required for
the fill request. The pre-fix picker takes both habitat residents; the repaired
picker returns the full ordinary crew in order. There is no real colony, fleet,
density, physical layout or departure in this measurement.

The extended run covers both receiver contrasts; the New passenger-request and
connected-label branches; New liveness filtering; player-chosen lander passengers;
elevator selection; foreign receiver delegation; absent residence; genuine predicate
error; hard specialisation and soft traits; transient-destructor exclusion;
restoration by function identity on success, shortage and injected picker error;
return tuples including trailing nil; common and one-receiver-only dependency paths;
and a desk-only removal control. Post-filter mutants for both receiver bodies return a
short crew on fixtures the repaired picker fills.

**MEASURED:** `python tools/bodycheck.py --module HabitatExpeditionDraft --all`
matches the pinned body and defect expression. `python tools/doccheck.py` passed
after adding the runtime module and manifests, including parse, registration,
wrap-target and probe-sweep checks. Final documentation checks run before commit.
**PROBE SWEEP:** clean (`rg -n TEMPORARY Code ../SMR-BugFixPack-TestKit/Code`,
no matches; doccheck independently reports the same).

## Corrections and attempts that failed

- **MEASURED:** the brief's five filter call sites included the definition.
  There are four calls; only the lander's two and elevator's one lie outside
  the expedition picker. The scoped-hook conclusion survives this correction.
- **SOURCE / MEASURED:** no residence is not an error. The harness separately
  injects a genuine predicate exception to exercise silent fallback.
- **MEASURED:** the default desk Lua 5.5 rejected shipped `table.copy` because
  it assigns to a loop variable. The harness explicitly uses Lua 5.4; the shipped
  body was not rewritten to make the test pass. An early retail-assert shim hid
  that compiler message; it now installs after body compilation.
- **SOURCE:** a leaf-class predicate misses Micro-G; policy flags also describe
  player-toggleable domes. **MEASURED:** the repaired desk case includes both
  habitat classes and an ordinary residence in a dome with connected work off.
- **MEASURED:** filtering the returned list fails the fill falsifier. Neither
  the label-swap fallback nor a copied picker body was needed or built.
- **SOURCE:** stale C95 wording still called the defect unreproduced and the
  build unauthorized, despite its reproduction and later owner ruling. Current
  title/status/evidence and acceptance wording were reconciled with that record.
- **MEASURED:** the first build targeted only the legacy receiver and was inert for
  `UniversalZeusRocket`. The re-point retains that hook and adds `CargoTransporterNew`;
  this corrects the earlier report's statement that the New gather was independent.
- **MEASURED:** the first extended `CrewDraft` logger collapsed a three-value return
  through Lua `and/or` and raised a formatting popup. TestKit `7b57b8a` assigns the
  tuple through an explicit branch; the accepted rerun is clean.

## Game acceptance — core passed attended

[Checklist 189](../../PLAYTEST_CHECKLIST.md) records the attended pass. On game
1.1.0.403908 build `6a91a190`, repo `733bed2`, TestKit `7b57b8a`, the New trace
showed all five Naturalist Habitat residents in the eligible pre-fix pool and none
in the returned 5/5 ordinary crew. The owner witnessed departure and habitat
occupancy **5 → 5**. The archived whole log has zero error-shaped lines:
[`c95_repoint_Mars.exe-20260916-12.45.56-6a91a190.log`](../../archive/logs/c95_repoint_Mars.exe-20260916-12.45.56-6a91a190.log).

**OWNER RULING:** lander/elevator player-choice coverage remains desk-verified and
will not be playtested absent a reported issue. **UNRUN / NOT CLAIMED:** Micro-G,
live pack removal/load, and deliberate-shortage UI behavior.

**MEASURED:** checklist membership comparison using `tools.doccheck.checklist_items()`
against the captured pre-edit headers at `7c29ecf` gives **145 → 146**:
all **145** prior headers remain and the sole addition is **189**. No item was
orphaned by the new subheading. The consumed prompt and its map row leave together;
its design and failed approaches survive here, the owner's rules remain on C95
and ck185, and the pending acceptance legs are on ck189.

## Public copy draft — for the release pass

**Judgment call — Habitat residents and expeditions.** The game can take habitat
residents on expeditions without asking and then fail to bring them home, costing
them their house. The automatic expedition draft now leaves Naturalist and
Micro-G habitat residents at home. You can still move them into a dome before
sending them, or hand-pick them for an asteroid lander.

**Reasoning:** the habitat's employment rules already separate its residents
from dome work. Applying that separation to automatic expedition recruitment
preserves the player's housing choice. This is a judgment call about intended
behavior, marked as such in the main pack.

**FAQ draft:** Does this rescue residents already away? No: this changes future
automatic drafts only. It does not change the return path or prevent deliberate
player transfers. Habitat residents leaving by ordinary migration is a separate
question and is not repaired here.

## Not opened

C96 implementation; C100 classification or migration repair; return-path widening;
provisioning a fixture; release version/store edits or publication; foreign-mod
yielding wrappers; unexplained historical draft selection; engine behavior of
`#nil` (EF-104's attended panel step remains the discriminator).
