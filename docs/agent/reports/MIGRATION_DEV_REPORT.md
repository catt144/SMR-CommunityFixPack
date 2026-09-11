# Colonist migration on 1.1.0.403908 — developer report

2026-09-11. **Source audit complete; game testing remains outstanding.** We
paused on a harmful interaction in our own F59 module, reported it, then resumed
at the owner's instruction. This is a developer review draft; it has not been sent.

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

| Shipped module | Verdict on 1.1.0 | Disposition / limit |
|---|---|---|
| `Fix_ShuttleTransportCache` (F51) | PARTIAL | Stale answer repaired; old permanent-block symptom no longer follows. |
| `Fix_VacuumWalks` (F52) | PARTIAL | Available passage selected; no-passage oxygen risk remains. |
| `Fix_ArrivalDeaths` (F53/C83/F117) | PARTIAL | C83 witnessed; terrain, distance and station branches have separate limits. |
| `Fix_ShuttleHubOffAvailable` (F54) | STILL NEEDED | Disabled-hub availability disagrees with dispatch. |
| `Fix_StaleReservations` (F58) | PARTIAL | Ordinary waits now expire; residual abandoned journey not reproduced. |
| `Fix_FreedHousingNotice` (F59) | HARMFUL | Original notification gap persists, but expedition timing requires repair. |
| `Fix_DomeFreeSpaceMismatch` (F60) | PARTIAL | Recommend retirement: no longer changes migration/birth gate; changes other estimates. |
| `Fix_ShelterReflex` (F73) | PARTIAL | Conditional shelter intervention only; organic benefit unverified. |

These are module verdicts, not eight confirmed player defects. No module is
declared wholly REDUNDANT merely because a gate moved. Recommended first work:
repair F59, retire F60's obsolete intervention, and capture F80 before mitigating
any recurrence. Those are proposals, not built changes.

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

**Confidence: DESK-CONTROLLED — `tools/desk_f59_expedition.py`, 12/12 demands held.**
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
other housing operations have similar multi-step lifecycles. No repair was built.

### 1a. The original vacancy gap still exists: repair, not retirement (F59)

**Symptom — INFERRED:** a suitable homeless neighbour can remain homeless after
an ordinary departure frees a bed, until another housing update runs.

**Where — SOURCE:** `Residence:RemoveResident` (`Residence.lua:119-126`) updates
occupation and invalidates the free-space cache, without notifying the homeless.
`Building:UpdateOccupation` (`Building.lua:3276-3318`) updates visuals/occupation;
`Community:ResetFreeSpace` (`Community.lua:361-364`) clears the tally and bumps
`g_ResidenceVersion`. Neither assigns the neighbour a home. `SetResidence`
(`Colonist.lua:2898-2917`) updates the departing colonist's state. Periodic housing
reevaluation remains in `Idle` (`:2338-2358`); the heavy-update interval reaches
12 game hours at 3,600 colonists (`Lua/City.lua:118`). Other events may shorten
that delay: this is not permanent homelessness or a guaranteed 12-hour wait.

**What our fix does / confidence:** F59's ordinary vacancy notification invokes
the existing homeless reassignment helper. **DESK-CONTROLLED**, same 12-demand
harness: vanilla ordinary departure leaves the bed free and the neighbour
homeless; a later explicit housing update fills it; F59 fills it immediately.

**Reproduce — INFERRED, CHEAP only with an existing housing fixture:**

1. Start with full suitable housing and one eligible, command-changeable homeless
   adult in that dome. Save before an ordinary resident moves to another home.
2. Compare F59 absent/present from the same state. Observe the newly empty bed
   and neighbour's residence immediately after departure, before their periodic
   housing update. The fixed leg should assign it during notification.
3. Let the ordinary housing update run in the absent leg: assignment should
   then succeed. An ineligible neighbour, another free bed, or a periodic update
   coinciding with departure makes the timing comparison inconclusive.

**Repair idea — DESK-CONTROLLED CANDIDATE, UNBUILT:** capture whether the home being
left equals `self.expedition_residence` before calling the original `SetResidence`,
and suppress this notification for that exact home. An in-memory transformation
of the module passes expedition preservation with F58 loaded, ordinary vacancy
notification, and an unrelated-expedition-pointer control. It is not in `Code/`.
Before implementation, review failed boarding, cancellation and return: an
abandoned expedition intent could defer an ordinary notification, and suppressing
the whole helper also delays notification about other free beds in that home.
The periodic update is a fallback, not proof of immediate recovery.

**Alternative — INFERRED:** notify after the expedition reservation is complete,
but only after reviewing all `OnDisappear` callers and cleanup paths. An arbitrary
timer delay would assume engine ordering we have not established. Cancellation
(`Residence.lua:385-399`) still has no F59 notification hook; neither candidate
claims to solve every reservation-to-vacancy transition.

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

Module verdict **PARTIAL**. The following defects share `Fix_ArrivalDeaths`,
but they do not share one reproduction or one level of confidence.

### 4a. Impassable placement and overlong arrival walks (F53)

**Symptom — INFERRED:** arrivals may be placed at an impassable spot or assigned
an overlong outside walk. We have not reproduced either on 1.1.0 in this audit.

**Where — SOURCE:** `Lua/Units/Colonist.lua:1612-1628` places arrivals at the
rocket spot without a passable-point search, then commands a walk to their chosen
dome. `_GameUtils.lua:403-407` now excludes absent/negative foot routes from the
ordinary safety fallback (an improvement over 1.0.7), but a nonnegative foot
distance can exceed the normal walking limit. `ChooseDome` (`:486-500`)
retains the fallback when no candidate wins with suitable space.

**What our fix does — SOURCE:** `Fix_ArrivalDeaths` snaps an impassable arrival
position to a nearby passable point through `OnArrival`, and reconsiders the
arrival destination before `Idle` invokes `Arrive`. It preserves a paired
elevator route. F53 withholds the unsafe fallback during re-selection.

**Confidence: SOURCE-READ ONLY** for the F53 mechanisms in this review. C83's
witness below does not cover them.

**Reproduce — INFERRED, EXPENSIVE distance diagnostic:**

1. Land beyond normal walking range of all domes, with a finite outside foot
   route to one safety dome and no station or elevator alternative.
2. Compare assigned destination/command with and without the module. A missing
   foot route yields no ordinary safety fallback and does not test this branch.
3. Use a nearby welcoming dome as the control. This does not exercise F117:
   the far fixture's re-pick list is empty. No deterministic terrain recipe for
   impassable placement was validated; an ordinary passable pad is only a control.

**What we are unsure about:** frequency and outcome in a real colony; withholding
a far fallback does not itself deliver an arrival to shelter. A nearby passable
snap does not prove a route to the destination. Station-only destinations can be
re-selected without this wrapper proving the subsequent train journey.

### 4b. Overflow arrivals assigned to an unsafe dome (C83)

**Symptom:** arrivals enter an off, quarantined, unsupplied dome and raise
Suffocation despite another welcoming dome being reachable.

**Where — SOURCE:** the safety fallback (`_GameUtils.lua:403-407`) lacks the
welcoming predicate used for ordinary candidates (`:408`); `ChooseDome`
(`:486-500`) retains it when candidates lack suitable space.

**What our fix does — SOURCE:** the ArrivalDeaths pre-Idle wrapper reselects a
welcoming fallback even when that dome is full. It accepts homelessness in the
working dome in place of the unsafe arrival destination.

**Confidence: CONFIRMED IN PLAY**, owner attended 2026-09-10: ordinary safe-arrival
control, forced overflow reroute and one-sol follow-through, archived in
`docs/archive/c83_attended_Mars.exe-20260910-17.36.10.log`. Also **DESK-CONTROLLED**,
`tools/desk_c83_arrivals.py`, 12/12 this audit. No additional game run here.

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

**What we are unsure about:** other arrival layouts. With no welcoming candidate,
C83 leaves vanilla's assignment; an UNKNOWN argument probe also stands down.
Later must-have-filter migration into an unsupplied but accepting dome is
intentional C84 (`Community.lua:436-445`), not this arrival fallback.

### 4c. Our re-selection passed the wrong argument after 1.1.0 (F117)

**Symptom — INFERRED:** our old arrival wrapper could throw during re-selection
when it passed traits where the rewritten selector expects a colonist. This is
our compatibility defect, not a new vanilla migration bug.

**Where — SOURCE:** `ChooseDome` (`_GameUtils.lua:486-500`) passes the colonist to
community scoring and suitability; `Community:GetScoreFor`
(`Community.lua:442-445`) reads `colonist.traits`. A traits table is the wrong shape.

**What our fix does — SOURCE:** current ArrivalDeaths probes the argument contract
and passes the appropriate shape, standing down if it cannot determine the shape.
**Confidence: DESK-CONTROLLED**, `tools/desk_f117_argshape.py`, 11/11 this audit.
No new F117-specific attended test is claimed from C83's witness.

**Reproduce — INFERRED, EXPENSIVE; unrun recipe from F117's Control section:**

1. Use a passenger pad with no dome within walking distance and no paired elevator
   destination. Put a walkable passenger station within the pad's station-search
   radius (`_GameUtils.lua:450-451`), linked to a welcoming dome cluster.
2. Include free filtered housing or a dome trait filter so scoring/suitability
   actually consumes the colonist shape. Land passengers and verify that the
   station supplies a nonempty re-pick list (`:450-478`).
3. Observe the argument-shape result and errors on that re-selection, comparing
   a nearby ordinary welcoming-dome landing where the wrapper stands down. The
   desk harness supplies the old wrong-argument failure leg; do not install the
   obsolete v5 pack as a whole on 1.1.0 for comparison.
4. A far pad without a station yields an empty list, and a paired elevator
   bypasses re-selection: both are vacuous. A non-nil cached argument shape alone
   does not prove this branch fired if C83 already populated the session cache.

**What we are unsure about:** organic branch reach, the train-only journey after
selection, and engine navigation. Correct argument shape does not guarantee a
safe final arrival.

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

## 7. Housing tally no longer controls migration, but still changes warnings (F60)

**Symptom — INFERRED:** with our override active, housing estimates can count
unpowered, player-enabled residences that the migration/arrival space gate rejects.

**Where — SOURCE:** `GatherFreeLivingSpaces` checks the selected operating member
on both home and parent dome (`_GameUtils.lua:541-544`) and returns filter buckets
(`:548-557`). Migration and births use `HasFreeLivingSpaceFor` / direct `working`
checks (`Community.lua:212`, `:323`, `:366-384`, `:402-418`). Assignment still uses
`ui_working` (`Residence.lua:452`). These are distinct policies; changing the
tally does not reconcile them.

**What our fix does — SOURCE:** `Fix_DomeFreeSpaceMismatch` passes
`player_enabled` from `Dome:RefreshFreeLivingSpaces` (`Dome.lua:3353-3355`). It
changes UI totals and `GetAvailableResidencesFor` (`RocketUtilities.lua:89-124`).
`PrepareApplicantsForTravel` uses that estimate at `:137`, then offers a housing
warning / smaller passenger selection when space is short (`:150-169`).
**INFERRED:** the override can suppress this warning without opening the space
gate. The launch dialog itself was not executed at the desk.

**Confidence: DESK-CONTROLLED — `tools/desk_migration_cluster.py`.** Real tally,
space gate, assignment and applicant-estimate bodies run with a single Everyone
applicant group and a three-bed home. Vanilla estimates zero; F60 estimates all
three applicants housed; the space gate rejects in both. Powered housing is the
agreement control. Geometry, population and dialog execution are not simulated.

**Reproduce — INFERRED, CHEAP if a suitable dome already exists:**

1. Use a functioning dome whose only suitable free housing is player-enabled but
   unpowered. Confirm other domes cannot satisfy the selected applicants.
2. Compare estimates and the housing warning while preparing passengers with F60
   absent/present; stop before launch. Record residence working/player switches,
   available bed counts, filters and passenger count.
3. Restore power and repeat: tally and space gate should agree. Alternative
   housing, incompatible filters or a different launch warning obscures this test.

**What we are unsure about / disposition:** **PARTIAL; retirement recommended**
for this obsolete migration intervention. This is not a claim that vanilla now
uses one consistent housing policy everywhere. The remaining assignment-versus-
admission difference is a policy question for the developers; widening our
override would be a new decision. No code was removed. The consumer read also
covered dome/UI totals (`Dome.lua:2600`, `:3877`, `:3908`), `CheckLivingSpace`
(`:4281-4306`), `ColonyControlCenter.lua:1320-1330`, and general available-residence
helpers (`_GameUtils.lua:348-367`). `Dome:HasFreeLivingSpace` is deprecated, with no
live caller found. The `CargoRequestNew.lua:358` use is asteroid-only and must not
be offered as proof of a normal rocket warning; the relevant path is above.

## 8. Oxygen-timer shelter intervention has narrow eligibility (F73)

**Symptom — INFERRED:** an idle colonist outside may need to return to shelter
before their oxygen timer expires. We have not reproduced this on 1.1.0.

**Where — SOURCE:** `Idle` (`Colonist.lua:2212-2389`) has no oxygen-timer branch;
`Rest` tries to enter the residence (`:2578-2581`). Outside timing is at
`:3015-3026`, suffocation after the full budget at `:4575-4578`. However, `Roam`
already enters a stand-alone habitat when `self.dome == self.residence`
(`:1493-1512`). Absence of a timer branch does not prove vanilla leaves an
eligible colonist outside until death.

**What our fix does — SOURCE:** current `Fix_ShelterReflex` retains only half (b):
at half the outside timer, request `Rest` if a valid working home exists, without
a transport task, dying state, breathable atmosphere or recent retry. It has no
asteroid-class restriction. Removed half (a) remains removed; a colonist with no
residence cannot benefit from half (b). `MicroGHabitat.lua:162-175` preserves a
suitable existing habitat even when full, and suitability uses community scoring.
Life-support scoring intentionally yields to must-have filters (C84,
`Community.lua:436-445`); that is not evidence to restore our old override.

**Confidence: DESK-CONTROLLED — `tools/desk_shelter_reflex.py`, 10/10.** The whole
module wraps a finite Idle spy; a sentinel models command replacement ending the
caller. Absent/present and each eligibility exclusion discriminate. This checks
the wrapper, not shipped Idle scheduling, navigation or actual survival. The kit
probe is install-kind and SKIPs on retail; July PT-19 mainly exercised removed (a).

**Reproduce — INFERRED, EXPENSIVE:** no reliable organic trigger recipe exists.
For a provisioned diagnostic, identify an idle colonist actually outside in vacuum,
with a working reachable home, no task and at least half the oxygen budget spent.
Compare module absent/present from the same state and observe `Rest` followed by
entry, with an early-timer control. Do not count a forced timer/state as an organic
reproduction. If vanilla Roam enters the home first, the intended trigger was not
exercised. Creating a homeless colonist without a home tests neither branch.

**What we are unsure about:** organic frequency, whether Rest reaches shelter,
and benefit after 1.1.0's habitat-selection changes. Verdict **PARTIAL**; no broader
suffocation guarantee or fresh in-play confirmation.

## 9. Quarantine: our original F61 proposal remains withdrawn

**Observed behavior / confidence:** the 2026-07-27 quarantine witness is historical
1.0.7 evidence. Current migration's quarantine early-return remains
(`Colonist.lua:3510-3512`), **SOURCE-READ ONLY**. We withdrew the proposal to weaken
quarantine and do not propose restoring `Fix_HomeDomeMigrationGate`.

**Where — SOURCE:** 1.1.0 rewrote `Dome:GetService` (`Dome.lua:3501-3519`) and
`ChooseTraining` (`:3537-3545`): their old explicit home/destination quarantine
checks are gone. Resident helpers use passage-policy switches and adjacency
(`:824-830`), not `accept_colonists`. The ordinary service eligibility chain
(`ServiceBase.lua:214-231`, `:255-274`; `Service.lua:240-257`) checks service
availability and visitor filters, not either dome's quarantine. The old predicate
still exists at `Dome.lua:3445-3447`; its presence does not prove these callers use it.

**What our fix does:** none; F61 was retired. **DESK-CONTROLLED selection only**,
`tools/desk_migration_observations.py`: an otherwise eligible service fixture is
selected with both dome quarantine flags off; disabling passage services prevents
selection. This is an observation about the rewritten selector, not a reproduced
quarantine escape or a conclusion about developer intent.

**Reproduce — INFERRED, CHEAP with connected populated domes:**

1. Put the only eligible non-food service in the neighbouring dome. Keep passage
   services enabled, both domes supplied and the service working with free capacity.
2. Compare normal service selection/visits with the home dome quarantined, then
   with the destination quarantined. Record assignments and actual passage travel
   separately; use an unquarantined run as the control.
3. Disable passage services as an exclusion control. Do not use food fallback,
   unavailable services or preexisting visits as proof of new selection.

**What we are unsure about:** actual travel enforcement and intended 1.1.0 policy.
Ask the developers whether the selector change is deliberate; no new bug status
or reinstatement is justified from this observation alone.

## 10. Service reach is adjacency, including Passage Hub neighbours (F62)

**Behavior — SOURCE:** an ordinary A–B–C chain can be walkable end-to-end while
C's services remain invisible from A. `GetClusterDomes` returns `connected_domes`
(`Dome.lua:745-747`), not the transitive `dome_network` built at `:688-706`.
`GetService` consumes resident service domes (`:828-830`, `:3501-3519`).
`PassageBase:ConnectDomePair` adds pairwise adjacency (`Passage.lua:1572-1589`).
But **Passage Hubs connect each attached dome to every other attached dome**
(`:1592-1600`): two hub spokes are neighbours for services. “Exactly one physical
passage hop” is therefore no longer a correct blanket description.

**What our fix does:** none, intentionally declined. **Confidence: DESK-CONTROLLED**,
`tools/desk_migration_observations.py`: real adjacency/network construction and
selector, controlled eligible service. Ordinary chain omits C; a shared hub offers
C. This corrects wording, not the owner's design decision. No original-game source
was available to rederive the historical provenance claim.

**Reproduce — INFERRED, EXPENSIVE unless both layouts already exist:**

1. Compare an ordinary three-dome chain with all services for a chosen non-food
   interest in the far end dome, passage services enabled, and a suitable resident
   in the other end dome. Record the candidate set and actual visits separately.
2. Put the equivalent service in the adjacent middle dome as the positive control.
3. Compare domes attached to one Passage Hub. The far spoke must be in adjacency;
   substituting a middle dome for the Passage Hub tests a different topology.

**What we are unsure about:** no new in-play comparison; policy intent beyond the
implemented scope. Offer as a design observation, not a pack bug to fix.

## 11. Training availability is still not an emigration incentive (F63)

**Behavior — SOURCE:** the rewritten migration scorer uses workplace availability,
not training slots (`Colonist.lua:3425-3495`; `Workforce.lua:83-128`). Dome workplace
availability iterates resident work domes (`Dome.lua:3521-3535`). Training remains
separate, selected through `ChooseTraining` (`:3537-3545`) using
`labels.TrainingBuilding`. No automatic training-seat attraction is established.

**What our fix does:** none; adding such a scoring term remains a feature.
**Confidence: SOURCE-READ ONLY.** The permitted-versus-offered discrepancy remains:
`ShiftsBuilding:CanWorkTrainHereDomeCheck` permits a transport route outside the
cluster (`ShiftsBuilding.lua:302-320`); automatic dome training selection searches
resident work domes. Manual training interaction also checks reachability
(`TrainingBuilding.lua:147-164`). The old claim that training is F61-quarantine-gated
must not be carried forward unchanged after the selector rewrite.

**Reproduce — INFERRED, EXPENSIVE diagnostic:**

1. Provision an eligible unspecialized adult and an operating university reachable
   only by train, with an open training slot and valid transport connection.
2. Compare automatic training offers with manual assignment eligibility. Record
   both checks rather than treating an empty university as a reproduction.
3. Put equivalent training in the home/adjacent dome as a selection control.
   A specialized or otherwise ineligible adult makes the comparison vacuous.

**What we are unsure about:** current player frequency and intended training policy.
“Nobody moves there” is not a controlled scoring test: housing and filters can
cause migration independently. No original-game provenance was newly verified.

## 12. Train service trips remain a declined feature (F79)

**Behavior — SOURCE:** service selection uses the resident dome list above; it
does not enumerate stations. Workplace selection does include station routes
(`Dome.lua:762-798`, `:812-821`). **Confidence: SOURCE-READ ONLY** on 1.1.0;
the 2026-07-28 no-shopping-riders observation belongs to 1.0.7.

**What our fix does:** none. The owner declined this feature on 2026-07-31; it is
not parked or proposed again. **Reproduce:** no new test owed for the declined
feature. A diagnostic would need an otherwise eligible service reachable only by
train and a home-dome service control; a train carrying no passengers alone is not
evidence. **What we are unsure about:** future developer intent and train-service
performance; neither warrants adding a feature to this repair pack.

## 13. Waiting train passengers: historical symptom, current enumeration defect candidate (F80)

**Symptom — historical, UNVERIFIED ON 1.1.0:** on 2026-07-28, the owner observed
a valid Waiting ticket for 17+ game hours while at least four trains stopped and
left, approximately 19 passengers queued, and no recorded full-train Comfort
penalties. Adding trains helped. The report is **45 days old**, from 1.0.7; no
verbatim runtime log line was recovered here. Its root cause remains unexplained.

**Where — SOURCE:** `ForEachStationAlongTrack` (`TrainTransport.lua:371-455`)
still takes a raw difference between two first-occurrence indices (`:373-378`),
advances by that difference (`:453`), wraps to endpoints (`:397-409`), and returns
on a missing edge (`:422`). The 1.1.0 change adds `trfRunnableOnly` handling
(`:384`, `:425-427`); it does not normalize this stride. `EnumRouteTracks`
(`:251-300`) still constructs closed loops and permits repeated station entries.
`Train:TransferCargo` enumerates the train's departure track (`Train.lua:836-841`,
`:887`); Waiting-ticket destination matching precedes both boarding and the
capacity penalty (`:962-979`). An omitted destination reaches neither branch.

**Confidence: DESK-CONTROLLED enumeration only — `tools/desk_migration_observations.py`.**
With three stations and paired connector fixtures forming A–B–C–A, the real route
builder produces `[A,B,C]`, `loop=true`, with all three edges. At C departing toward
A, the raw stride is -2: the enumerator returns A, then revisits C and omits B.
Starting A→B visits B,C; C's opposite departure visits B,A; an open-line control
works both ways. Cargo-only truncation behaves as designed. No duplicate station
or missing edge is needed for this particular omission. This corrects the older
claim that every non-unit stride necessarily fails on a missing edge.

**What our fix does:** none. Do not implement “normalize to ±1” from this result:
at a loop seam the raw sign itself is misleading, and repeated stations require
the correct occurrence/edge, not only a magnitude fix. Connector pairing and
physical buildability were supplied by the harness; no game colony or full
boarding sequence was executed. This is not proof of the July incident's cause.

**Reproduce — INFERRED, EXPENSIVE, not yet run:**

1. On a disposable 1.1.0 map, provision a three-station closed loop with passenger
   transport allowed, stations working, no construction/broken edges and trains
   with capacity. Capture the actual route array and connector pairing; if the
   builder chooses a different anchor, identify the corresponding last→first seam.
2. At that seam departure, record the enumerated destination sequence for that
   exact track, the waiting colonist's ticket/destination/stage, and actual train
   departure track. Compare the opposite track and an ordinary adjacent-index
   departure. Merely seeing trains pass the platform is insufficient.
3. If the historical waiting/walking symptom recurs, capture both ticket state
   and per-track enumeration **before adding trains or altering the network**.
   Keep the diagnostic callback read-only and non-nesting: `stations_visited` is
   shared (`TrainTransport.lua:369`, `:391-394`).
4. Record `GetReachableStations()` at both endpoints as context, not a definitive
   falsifier: it unions enumerations from all connected tracks (`Station.lua:426-433`),
   so another track can hide the bad departure's omission. Both endpoints listing
   one another does **not** refute a per-train departure omission. Conversely, an
   exact failing departure that enumerates the ticket destination shifts the
   investigation downstream into boarding eligibility/capacity/command handling.

**What we are unsure about:** whether the supplied loop is buildable with the
current station assets, whether this omission causes persistent waiting in actual
train scheduling, repeated-station variants, and the July incident's topology.
The desk result makes a sharper developer question; it does not close F80.

## Appendix A — seven changed-function comparisons

| Function | SOURCE: archived 1.0.7 → live 1.1.0 | Effect on claims / new-defect assessment |
|---|---|---|
| `FindEmigrationDome` | `Colonist.lua:2581-2699` → `:3497-3527`: graph + scorer replace inline candidate enumeration; `force_leave` flows from `TryToEmigrate` (`:1989-2019`) into `GetBestReachableCommunities` (`:3425-3495`), suppressing home scoring at `:3434`. | SOURCE: none of the eight modules replaces this signature. INFERRED: no F115/F117-style missing-argument failure found; F51's permanent-skip premise no longer follows. C84 design preserved. |
| `TryToEmigrateToDome` | `Colonist.lua:1546-1590` → `:1886-1983`: work reservations, shuttle-owned-task guard, moved constants, negative-distance conversion, ticket discard, task retargeting, landing-slot-aware request creation. | SOURCE: F52 retains all these changes and changes only the vacuum threshold. INFERRED: no separate new defect established from this diff. |
| `UpdateResidence` | `Colonist.lua:2309-2317` → `:2919-2927`: `(home.parent_dome or home)` must equal own dome, including stand-alone habitats. | SOURCE: `ui_working` and `CanReserveResidence` checks remain. INFERRED: does not remove F60's policy disagreement; no new defect established. |
| `ChooseResidence` | `Residence.lua:399-423` → `:437-468`: comfort tiers precede score and free-space tie-breaks. | SOURCE: F59 invokes this new selection synchronously; ui-enabled housing still eligible. INFERRED: tier change alone establishes no defect. |
| `CanReserveResidence` | `Residence.lua:250-255` → `:283-288`: generalized `IsSuitable(unit)` replaces exclusive-trait-only check. | SOURCE: rejects unsuitable applicants before accepting an existing hold or a free bed. INFERRED: expected filter expansion, no independent defect established. |
| `CancelResidenceReservation` | `Residence.lua:353-365` → `:385-399`: cancellation also clears `expedition_residence`. | SOURCE: current F58 age exemption matters; F59 can prevent the reservation earlier. No homeless notification added. |
| `GatherFreeLivingSpaces` | `_GameUtils.lua:475-497` → `:535-558`: parent-dome operating gate; named filters replace exclusive-trait buckets. | SOURCE: F60 keeps bucket structure, but migration no longer consumes this tally. Applicant estimates still do; retirement recommended, not a blanket vanilla-policy clearance. |

Bodies were extracted with `tools/luafn.py` / `deskbench.body`, using the single
project delimiter, and compared with `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src`.
The live source root was `A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src`.
The inventory lists all seven changed functions; none is in the old seam coverage
ledger. The prior colony skim explicitly disclaimed function-level clearance.

## Appendix B — validation and owner handoff

**Recorded desk validation:** `MIGRATION_DESK_RESULTS.txt` records six suites:
migration 16/16, F59 12/12, shelter 10/10, topology observations 10/10,
F117 argument shape 11/11, C83 arrivals 12/12. All 21 pinned bodycheck rows across
the eight modules are OK, including F59: mechanical currency does not establish
semantic safety. The TEMPORARY sweep returned zero in both Code directories.
No engine load or owed TestKit run is covered by these checks.

The one-off audit brief is consumed. Progress is retained in
`MIGRATION_CHECK_PROGRESS.md`; checklist **151** carries repair/retirement,
developer-sharing and sitting choices. F59 implementation, F60 removal and the
proposed game tests require their own follow-through. The report recommends
sharing F52/F54 mechanisms and C83's scoped witness, the corrected uncertainty
for F51/F58/F73, and F80's per-track evidence as separate claims. F59's regression
and F60's obsolete override are our own maintenance findings. F61/F62/F63/F79
belong as policy observations, not a list of confirmed game defects.
No fix or release file was edited and no developer was messaged.

Doccheck result: GREEN. Required owner-facing warning (verbatim):

```text
warn STATE.md is 12469 bytes, warn threshold is 12288 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md
```
