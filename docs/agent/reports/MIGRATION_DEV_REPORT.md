# Colonist migration on 1.1.0.403908 — partial developer report

2026-09-11. **Audit stopped on a harmful interaction in our own F59 module.**
Sections below distinguish completed findings from work still outstanding. This
is a review draft, not a clearance of the migration cluster or a sent message.

We investigate player reports against the shipped Lua, compare game revisions,
and use controlled Lua checks and, where available, attended game tests. Our
public list uses broad player-facing descriptions; those descriptions are not
the evidence. We will narrow or withdraw claims that your implementation
disproves, as the 1.1.0 source review did for F37's farm-oxygen claim. This review
found another case where our wording overstated current evidence, and a case
where our own fix interferes with your new reservation lifecycle.

`SOURCE` marks a directly read mechanism; `INFERRED` marks its proposed player
effect or an unrun recipe. All game citations below refer to **1.1.0.403908**
unless explicitly marked 1.0.7. Desk controls use Lua 5.5 / lupa 2.8, not the game
engine. No game was launched for this audit. Historical July tests are 1.0.7
evidence only. The 1.1.0 TestKit suite is still owed; no predicted kit result is
counted here. D03/D07/D12 are in a separate optional mod, outside this review.

## 1. Our vacancy notification can take an expedition crew member's home (F59)

**Symptom — INFERRED:** with our fix active, a homeless neighbour can take an
expedition crew member's bed during boarding, before the game reserves it for
their return. We have not reproduced this on 1.1.0 in play.

**Where — SOURCE:** `Lua/Units/Colonist.lua:5027-5040` saves
`expedition_residence` and calls `SetDome(false)` during `EnterTransporter`.
`SetDome` removes the colonist from the dome and calls `SetResidence(false)`
(`:410-435`), which removes the resident (`:2898-2917`). Our
`Code/Fix_FreedHousingNotice.lua:66-79` post-wrapper immediately calls
`CheckHomeForHomeless`; the shipped `Lua/Buildings/Residence.lua:160-168` then
runs each homeless colonist's `UpdateResidence` synchronously. Suitable homeless
neighbours can acquire the newly freed bed through `Colonist.lua:2919-2926`,
`Dome.lua:3554-3557`, and `Residence.lua:437-467`.

**SOURCE:** the expedition reservation is only taken later, in
`Colonist:OnDisappear` (`Colonist.lua:5003-5007`). If the bed is already occupied,
`CanReserveResidence` returns false (`Residence.lua:283-288`, `:232-234`), so
`expedition_residence` is cleared. The engine route into that callback is
`Unit:EnterTransporter` → `Disappear` → `OnDisappear`
(`Lua/Units/Unit.lua:1292-1305`, `:1222-1225`). The first competing notification
normally occurs at `EnterTransporter`'s `SetDome`, not its later redundant
`OnDisappear:SetResidence(false)` cleanup.

**What our fix does — SOURCE:** `Fix_FreedHousingNotice` was intended to wake
homeless colonists after a completed move frees housing. A completed
`SetResidence` is not necessarily the end of the higher-level housing operation:
expedition boarding continues and needs that same slot. This is an unintended
interaction in our mod, not a request for you to reproduce a vanilla defect.
The current `Fix_StaleReservations` expedition-age exemption cannot protect a
reservation that was never created.

**Confidence: DESK-CONTROLLED — `tools/desk_f59_expedition.py`, 6/6 demands held.**
The harness extracts the real `EnterTransporter`, `SetDome`, `SetResidence`,
`OnDisappear`, selection and reservation bodies, and loads our whole modules.
With F59 absent, the crew member retains the bed reservation. With F59 applied,
the homeless neighbour takes it and the expedition hold becomes false. With no
homeless neighbour, the hold survives even with F59. Adding current F58 and
running its daily sweep does not restore the lost hold. UI/labels/comfort and
the Unit transport boundary are stubbed; the result establishes the synchronous
interference, not a real colony reproduction or the returning crew's fate.

**Reproduce — INFERRED, EXPENSIVE; never run on 1.1.0:**

1. Prepare a disposable 1.1.0 colony with a working dome whose suitable housing
   is full, at least one housed adult available for an expedition, and an idle
   homeless adult eligible for that same residence. Record the crew member's
   actual home and the competing homeless colonist. Save before boarding.
2. With F59 active, send the housed adult on an expedition. Observe boarding,
   then inspect the neighbour's residence, the crew member's
   `expedition_residence` / `reserved_residence`, and the home's `reserved` list.
   Losing the hold at boarding is the measure; waiting five sols is unnecessary.
3. Reload the same fixture with only F59 disabled for a fresh process, preserving
   the same expedition and housing state. The control must retain the crew's
   reservation while the neighbour stays homeless. Also repeat with no eligible
   homeless neighbour: the hold should survive in either configuration.
4. If the crew member did not have that home at the start of `EnterTransporter`,
   the neighbour was not eligible/command-changeable, or unrelated housing opened,
   the comparison is not this trigger. If both legs lose the hold, capture the
   earlier loss; this does not demonstrate the F59-specific interference.

**What we are unsure about:** how often ordinary boarding reaches the supplied
state; earlier transport can already change a crew member's residence; whether
other unreviewed housing operations have similar multi-step lifecycles. No
repair was built. Our audit brief requires owner disposition before continuing
past a potentially harmful shipped module.

## 2. Shuttle transport cache: stale answer remains, original symptom claim narrows (F51)

**Symptom — INFERRED:** a transport-mode query can keep the answer calculated
before shuttle availability changed. We no longer claim that this alone makes
homeless colonists permanently skip a reachable dome on 1.1.0.

**Where — SOURCE:** `Lua/Units/Colonist.lua:3170-3204` caches on community and
position, while the computation uses `shuttles_available` (`:3111-3119`,
`:3206-3218`). Train/passage/rocket invalidation exists at `:3122-3153`, but
does not key the result on shuttle availability. However, `FindEmigrationDome`
now selects from `BuildReachableGraph` (`:3400-3423`, `:3497-3526`), whose shuttle
expansion consults current availability directly. It queries the mode cache only
after choosing a destination. `TryToEmigrateToDome` can create a shuttle request
even if that mode is false (`:1959-1979`).

**What our fix does — SOURCE:** `Fix_ShuttleTransportCache` adds a normalized
shuttle-availability flag to each cache entry and recomputes when it differs.
The module repairs the cache contract, but current player impact needs a narrower
reproduction than the historical F51 description.

**Confidence: DESK-CONTROLLED — `tools/desk_migration_cluster.py`.** Vanilla
retains false after availability becomes true; the patch recomputes in both
directions. A separate extracted `TryToEmigrateToDome` leg creates a task even
with false mode when the fixture allows transport. Task creation and geography
are stubs, so this refutes the unconditional permanent-block inference, not
every possible migration failure.

**Reproduce:** we have not reproduced a F51-specific player symptom on 1.1.0.
**INFERRED, CHEAP diagnostic only, if an existing colony has two distant domes
and a hub:** query the same dome pair before and after hub availability changes;
compare the cached mode with a fresh `GetTransportationModeToCommunity` result.
Use an unchanged-availability query as control, and ensure no train/passage/rocket
event cleared the cache. This can demonstrate stale data; it is not evidence of
homelessness. No reliable current player-level reproduction is claimed.

**What we are unsure about:** which remaining reachable caller can turn this
stale answer into harm. Other callers query rocket destinations with shuttles
disabled (`UniversalRocket.lua:2223`, `:2245`; `SupplyRocket.lua:68`); that is not
proof of a live false→true migration failure. Verdict **PARTIAL**: verified
cache repair, unresolved necessity for the old symptom.

## 3. Short outside walks can omit an available passage (F52)

**Symptom — INFERRED:** a migrating colonist can walk outside in vacuum despite
an available passage. Suffocation on 1.1.0 has not been reproduced here.

**Where — SOURCE:** `Lua/Units/Colonist.lua:1898-1927` only asks for a passage
when distance exceeds a threshold. In vacuum that threshold is the maximum dome
walk distance (`:1903`), so short positive-distance outside routes skip the
lookup. The new negative-distance handling already requests a passage for a
pair walkable only through passages (`:1904-1907`).

**What our fix does — SOURCE:** `Fix_VacuumWalks` carries the rewritten 1.1.0
body with the vacuum threshold changed to zero. Work reservations, shuttle-owned
task protection, train-ticket discard, task retargeting and landing-slot checks
remain. Verdict **PARTIAL**: the passage case is repaired, but a no-passage walk
is still allowed; the module provides no oxygen-budget cap.

**Confidence: DESK-CONTROLLED — `tools/desk_migration_cluster.py`.** A controlled
300-distance vacuum leg omits the passage in vanilla and forwards it with the
patch. No-passage and breathable controls preserve outside walking. Fixture
distances use normalized units; the game uses its own distance scale.

**Reproduce — INFERRED, CHEAP only with an existing two-dome fixture:**

1. In vacuum, use two domes with an outside walk shorter than the dome walk cap,
   connected by a usable passage. Pick an adult with a valid destination and no
   shuttle-owned task. Confirm the outside route has positive distance (not -1).
2. From the same saved state, compare migration with F52 absent and present.
   Observe the route, not just arrival or survival: the fixed leg should use the
   passage where the vanilla leg takes the outside route.
3. On a disposable copy, remove the passage and repeat. Both legs may walk
   outside. A no-outside-route pair, a different transport mode, or a colonist
   never actually migrating makes this test vacuous. Building a new fixture is
   EXPENSIVE; it is not automatically a rider on any loaded save.

**What we are unsure about:** organic route timing, entrance queues, oxygen
loss and the frequency of actual deaths on 1.1.0. July PT-13 does not verify the
new body in play.

## 4. Arrivals: placement, distance fallback, and unsafe destination are separate (F53/C83/F117)

**Symptom — SOURCE/INFERRED:** C83's arrivals entering an off, quarantined,
unsupplied dome and raising Suffocation were observed by the owner on 2026-09-10.
F53's impassable placement and overlong journey remain source-derived on 1.1.0.

**Where — SOURCE:** `Lua/Units/Colonist.lua:1612-1628` places arrivals at the
rocket spot without a passable-point search, then commands a walk to their chosen
dome. `_GameUtils.lua:403-407` now excludes absent/negative foot routes from the
ordinary safety fallback (an improvement over 1.0.7), but a nonnegative foot
distance can exceed the normal walking limit, and the fallback still lacks the
welcoming check applied to ordinary candidates (`:408`). `ChooseDome`
(`:486-500`) retains that fallback when no candidate wins with suitable space.

**What our fix does — SOURCE:** `Fix_ArrivalDeaths` snaps an impassable arrival
position to a nearby passable point through `OnArrival`, and reconsiders the
arrival destination before `Idle` invokes `Arrive`. It preserves a paired
elevator route. F53 withholds the unsafe fallback during re-selection; C83 uses
a welcoming fallback even if that dome is full. F117 is our compatibility repair
for `ChooseDome` now taking a colonist rather than a traits table, not a new
vanilla migration defect. Verdict **PARTIAL**, with separate evidence per part.

**Confidence:** C83 **CONFIRMED IN PLAY**, owner attended 2026-09-10; ordinary
safe-arrival control, forced overflow reroute and one-sol follow-through, archived
in `docs/archive/c83_attended_Mars.exe-20260910-17.36.10.log`. F117
**DESK-CONTROLLED**, `tools/desk_f117_argshape.py` (11/11 this audit), and C83's
wrapper controls `tools/desk_c83_arrivals.py` (12/12). F53 placement is
**SOURCE-READ ONLY** for this review; do not extend C83's witness to it.

**Reproduce — INFERRED, CHEAP if the saved C83 1.1.0 fixture is available:**

1. Use a nearer walkable dome switched off, quarantined and unsupplied, and a
   farther welcoming dome. Ensure the welcoming dome has insufficient suitable
   housing for the arriving passengers; remove alternative station/elevator
   destinations from this comparison. Save before landing.
2. Compare arrival with the module absent and present. Observe each destination
   and Suffocation, then check one sol later. The fixed overflow should enter the
   working dome homeless rather than the nearer unsafe dome.
3. Give the welcoming dome space for every arrival as a negative control: the
   bad fallback should not be used. A log with no reroute is not a pass unless
   the trigger actually selected the bad fallback in the comparison leg.

**INFERRED, EXPENSIVE F53 distance recipe:** land beyond normal walking range of
all domes but with a finite outside foot route to one safety dome and no station
or elevator alternative. Compare assigned destination/command with and without
the module; a near welcoming dome is the control. A missing foot route yields
no ordinary safety fallback on 1.1.0 and is not this case. This does not exercise
F117 because the re-pick candidate list is empty. No deterministic terrain
recipe for F53's impassable drop has been validated; a passable ordinary pad is
only a control, not a reproduction.

**What we are unsure about:** station-only destinations can be re-selected by
the helper without this wrapper proving the subsequent train journey. F117's
station recipe is still unrun (`bugs/F117.md`, Control); a non-nil cached argument
shape alone cannot identify which branch fired once C83 has exercised it. C83
leaves vanilla's assignment when there is no welcoming candidate; an UNKNOWN
argument probe also stands down. A nearby passable snap does not prove a route
to the destination. Later must-have-filter migration into an unsupplied but
accepting dome is intentional C84, not C83's unguarded arrival fallback.

## 5. Player-disabled hubs still satisfy transport availability (F54)

**Symptom — INFERRED:** route selection can believe colonist shuttles are
available even when the player has switched every capable hub off.

**Where — SOURCE:** `Lua/Buildings/ShuttleHub.lua:410-419` accepts a hub with a
permission reason and no physical failure; `BaseBuilding.lua:657-663` returns
`TurnedOff` for the player's switch. Dispatch sites are gated on `working`
(`ShuttleHub.lua:583-588`, `:1836-1840`). The graph's shuttle expansion reads the
availability predicate (`Colonist.lua:3408-3413`).

**What our fix does — SOURCE:** `Fix_ShuttleHubOffAvailable` delegates to vanilla
then filters its positive verdict through a scan requiring the player switch on
for a nonworking hub. Working hubs and self-lifting exceptional suspensions
remain eligible. Verdict **STILL NEEDED** for this predicate discrepancy.

**Confidence: DESK-CONTROLLED — `tools/desk_migration_cluster.py`.** Off, working,
and self-lifting suspension controls distinguish the predicates. No fresh
1.1.0 in-play result is claimed.

**Reproduce — INFERRED, CHEAP if a suitable hub exists:**

1. In a disposable colony, identify every hub with shuttles capable of people
   transport. Keep them supplied and otherwise functional; switch all off and
   let working-state changes settle.
2. Compare `IsLRTransportAvailable(city)` with and without F54. Record all hub
   states and observe whether new shuttle departures occur, distinguishing
   existing airborne tasks from new dispatch.
3. Switch one functional people-capable hub back on: availability should return
   in both legs. Another enabled hub, zero shuttles, cargo-only mode or missing
   fuel/power makes the off-state comparison nondiscriminating.

**What we are unsure about:** the extent of downstream waiting after 1.1.0's
task expiry changes. This is not a claim that all off-hub waits last forever.

## 6. Reservations without a completed journey (F58)

**Symptom — INFERRED:** a residual housing reservation can consume a bed after a
journey fails. Ordinary uncommitted shuttle waits are no longer evidence for an
unbounded reservation on 1.1.0.

**Where — SOURCE:** `Residence.lua:232-234` subtracts reserved slots.
`LRTransport.lua:43-59` expires old uncommitted tasks, and
`LRManager.lua:50-62` releases a matching colonist request through
`Colonist:ClearTransportRequest` (`Colonist.lua:2036-2038`). Committed shuttles
are exempt from that expiry and command `Transport` is skipped by the manager.
`TransportByFootDtor` (`Colonist.lua:3529-3539`) itself does not cancel a home
reservation. These are local gaps, not proof that nothing later cleans them:
ordinary `Idle` / `UpdateResidence` can reassign housing (`:2338-2358`,
`:2919-2926`), and other transport cleanup sites exist.

**What our fix does — SOURCE:** `Fix_StaleReservations` timestamps reservations
and sweeps `MainCity.labels.Residence` daily for invalid, desynchronized, dying,
or sufficiently old holders. Current code exempts expedition reservations from
age expiry. Verdict **PARTIAL**: the generic cleanup still exists, but residual
organic reach and benefit have not been demonstrated on 1.1.0. F59's newly found
loss happens before this protection can operate.

**Confidence: SOURCE-READ ONLY** for residual vanilla defects; the F58/F59
composition limit is **DESK-CONTROLLED** by `tools/desk_f59_expedition.py`.

**Reproduce:** no reliable in-game recipe for the residual stuck journey has
been established. **INFERRED, EXPENSIVE preservation control:** launch a crew
whose homes remain reserved after boarding, keep them away beyond the age
threshold and a daily sweep, then confirm the reservations survive and returning
crew can reclaim them. No-homeless-neighbour boarding distinguishes this from
F59. A short trip, an already-lost hold or a run without a daily sweep is
vacuous. This checks preservation, not the alleged residual stale journey.

**What we are unsure about:** whether a real non-expedition reservation outlives
all the normal cleanup paths; the daily sweep is MainCity-only; age alone does
not demonstrate a journey is abandoned. We do not claim an additional harmful
case without a discriminating state and evidence.

## 7. Housing tally and migration gate disagree (F60) — review not completed

**SOURCE:** the extracted `GatherFreeLivingSpaces` now checks the chosen
operating member on both home and parent dome (`_GameUtils.lua:541-544`) and
returns filter buckets (`:548-557`). Our `Fix_DomeFreeSpaceMismatch` still passes
`player_enabled` from `Dome:RefreshFreeLivingSpaces` (`Dome.lua:3353-3355`). The
migration gates independently inspect `working` (`Community.lua:366-384`,
`:402-418`); `ChooseResidence` still uses `ui_working` (`Residence.lua:452`).

**DESK-CONTROLLED:** `tools/desk_migration_cluster.py` shows a three-bed unpowered
but enabled home counts as zero in vanilla and three with the module, while the
migration gate rejects it in both. Power-on is a passing comparison control.
This corroborates the existing removal-candidate finding in F60; it does not
decide which housing policy is preferable. Remaining consumer/reproduction
review and per-module bodycheck are deferred at the F59 stop. **No final module
verdict is issued.** No new F60 repair or removal is proposed as completed work.

## 8. Shelter and declined entries — not cleared by this partial report

- **SOURCE, F73:** the current `Fix_ShelterReflex` retains only the oxygen-timer
  pre-wrapper; it requires a valid working residence and no transport task.
  `Colonist:Idle` (`Colonist.lua:2212-2389`) has no corresponding timer branch;
  `Rest` tries to enter the residence (`:2578-2581`). A homeless colonist with no
  residence cannot be rescued by this wrapper. Final verdict, reproduction and
  bodycheck are deferred; July PT-19 primarily exercised the removed half (a).
- **SOURCE, F61:** quarantine's explicit no-enter/no-leave branch remains in
  `FindEmigrationDome` (`Colonist.lua:3510-3512`). Our original interpretation
  was withdrawn; no reinstatement is proposed.
- **SOURCE, C84:** no-life-support scoring is intentionally overridable by a
  must-have filter (`Community.lua:436-445`). It is separate from C83.
- **INFERRED from existing records, not reverified here:** F62/F63 are design
  observations, F79 is our own declined feature decision. Their current service,
  training and workplace paths still need the planned review; do not present
  them as newly verified 1.1.0 defects.
- **Historical evidence only, F80:** the entry records a 2026-07-28 colonist
  waiting 17+ game hours with a valid Waiting ticket while at least four trains
  stopped and left, around 19 queued passengers, and zero recorded full-train
  Comfort penalties. That is **45 days old**, on 1.0.7, not a 1.1.0 reproduction.
  The later stride/enumeration theory still lacks a demonstrated trigger. No
  verbatim runtime log line was recovered or invented in this review. A fresh
  recurrence should be captured before adding trains; the full current-body
  analysis and developer-ready F80 handoff remain outstanding.

## Appendix A — seven changed-function reads completed before the stop

| Function | SOURCE: archived 1.0.7 → live 1.1.0 | Effect on claims / new-defect assessment |
|---|---|---|
| `FindEmigrationDome` | `Colonist.lua:2581-2699` → `:3497-3527`: graph + scorer replace inline candidate enumeration; `force_leave` flows from `TryToEmigrate` (`:1989-2019`) into `GetBestReachableCommunities` (`:3425-3495`), suppressing home scoring at `:3434`. | SOURCE: none of the eight modules replaces this signature. INFERRED: no F115/F117-style missing-argument failure found; F51's permanent-skip premise no longer follows. C84 design preserved. |
| `TryToEmigrateToDome` | `Colonist.lua:1546-1590` → `:1886-1983`: work reservations, shuttle-owned-task guard, moved constants, negative-distance conversion, ticket discard, task retargeting, landing-slot-aware request creation. | SOURCE: F52 retains all these changes and changes only the vacuum threshold. INFERRED: no separate new defect established from this diff. |
| `UpdateResidence` | `Colonist.lua:2309-2317` → `:2919-2927`: `(home.parent_dome or home)` must equal own dome, including stand-alone habitats. | SOURCE: `ui_working` and `CanReserveResidence` checks remain. INFERRED: does not remove F60's policy disagreement; no new defect established. |
| `ChooseResidence` | `Residence.lua:399-423` → `:437-468`: comfort tiers precede score and free-space tie-breaks. | SOURCE: F59 invokes this new selection synchronously; ui-enabled housing still eligible. INFERRED: tier change alone establishes no defect. |
| `CanReserveResidence` | `Residence.lua:250-255` → `:283-288`: generalized `IsSuitable(unit)` replaces exclusive-trait-only check. | SOURCE: rejects unsuitable applicants before accepting an existing hold or a free bed. INFERRED: expected filter expansion, no independent defect established. |
| `CancelResidenceReservation` | `Residence.lua:353-365` → `:385-399`: cancellation also clears `expedition_residence`. | SOURCE: current F58 age exemption matters; F59 can prevent the reservation earlier. No homeless notification added. |
| `GatherFreeLivingSpaces` | `_GameUtils.lua:475-497` → `:535-558`: parent-dome operating gate; named filters replace exclusive-trait buckets. | SOURCE: F60 delegates to the new helper so keeps bucket structure, but migration no longer consumes this tally. INFERRED: final disposition still needs consumer review. |

Bodies were extracted with `tools/luafn.py` / `deskbench.body`, using the single
project delimiter, and compared with `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src`.
The live source root was `A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src`.
The inventory lists all seven changed functions; none is in the old seam coverage
ledger. The prior colony skim explicitly disclaimed function-level clearance.

## Appendix B — validation, stop and remaining work

**SOURCE:** this audit stopped under `MIGRATION_CLUSTER_CHECK.md` §5 after F59's
harmful interaction was established. Live progress is in
`MIGRATION_CHECK_PROGRESS.md`; owner decisions are checklist **151**. The brief
remains live because the full deliverable is incomplete.

**Recorded desk validation:** `MIGRATION_DESK_RESULTS.txt` contains the three
control suites above, the F59 regression control, and bodycheck for the six
modules reviewed through F59. Every recorded bodycheck was OK, including F59;
that demonstrates why a pin/signature check is not semantic clearance. These
checks do not validate an in-game load or the owed TestKit run. The pre-test
TEMPORARY sweep found no matches in either Code directory.

**Remaining:** complete F60 and F73 module reviews; rederive the declined four
and F80 against 1.1.0; finish all recipes and their controls; incorporate the
owner's F59 disposition; then review this report as a whole before sending.
No fix was edited, no release file was touched, and no developer was messaged.

Doccheck result: GREEN. Required owner-facing warning (verbatim):

```text
warn STATE.md is 12474 bytes, warn threshold is 12288 ? copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md
```
