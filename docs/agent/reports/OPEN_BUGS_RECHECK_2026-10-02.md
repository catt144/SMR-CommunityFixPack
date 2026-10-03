# Open-bug recheck — 2026-10-02

## Must_Read_Header

Investigation record for the owner's per-entry build decision. No fix is authorized
by this report. Dated entry sections hold the exact commands, output and limits;
earlier entry material remains historical evidence. The sitting section names
discriminating evidence, not scheduled or owed owner time.

## Outcome and scope

The confirmed mechanisms are C57 (disabled delicacies consumed), C63 (expired
zero-seat faction disaster continues), C64 (completed opportunity expiry skipped)
and C106 (arrival fallback chooses an unsuitable habitat). C106 remains under
the owner's hold. C55, C91 and C104 have replaced vanilla bodies that remove their
filed mechanisms; C101's absolute-rejection premise conflicts with explicit player
help. Own-code retirements concern the blamed modules or repaired expressions,
not a claim that every related gameplay issue is cured.

Source baseline: `B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src`,
**game 1.1.1.406343 / build 25579348** throughout this report's current game-source
citations. Installed build verified by `python tools/doccheck.py --emit-fingerprint`
at firing HEAD `445a4d59`. Checkout reads identify their HEAD in the entry receipt;
prior observations explicitly retain their older build/date.

The firing filter is the committed `445a4d59:docs/agent/bugs/INDEX.md`, statuses
`filed`, `cand`, `blocked`, `built`, `open`, excluding C121. C122 is the named
addition required by the sibling train report; no other entry was added to scope.
The prompt's explicit owner exclusions use `out-of-scope` alongside its defect
verdicts. Counts below are produced by `python tools/open_bugs_recheck.py --selftest`:

```text
confirmed 4 C106 C57 C63 C64
not-a-defect 1 C101
ours-retired 8 F111 F112 F113 F114 F116 F117 F118 F98
out-of-scope 6 C47 C48 C92 D06 D07 D14
possible-unconfirmed 42 C100 C103 C105 C108 C109 C110 C112 C113 C118 C122 C40 C41 C45 C53 C56 C58 C59 C60 C61 C62 C65 C66 C67 C68 C69 C70 C71 C72 C73 C75 C76 C78 C79 C81 C82 C87 C94 C97 C98 C99 F103 F99
vanilla-fixed 3 C104 C55 C91
FIRING MEMBERS PLUS TRAIN 64 REPORT ROWS 64 ENTRY SECTIONS 64
DECIDING READS 42 POSSIBLE ROWS 42
PASS: report, entry sections, statuses and deciding reads reconcile by id
```

The checker compares named firing members plus C122, table rows, dated entry
sections, closure statuses and the possible-unconfirmed deciding-read list. It
also rejects missing-row, changed-verdict and missing-deciding-read variants.
It verifies the record's structure; the source/log reads and controls recorded in
the entries clear the evidence. Each delegated result received an independent
recording-seat check before insertion.

## Verdicts

Each command cell links to the dated entry receipt containing the **exact rerunnable
command and its key output**. Named desk commands are shown directly. All were run
on 2026-10-02 by the recording seat. SOURCE, CHECKOUT and AUTHORITY rows are reads
with assertions, not gameplay confirmations. Priorities are the existing filed
priorities, not a new ranking.

| id | verdict | priority | evidence class and finding | falsifying command |
|---|---|---|---|---|
| [F98](../bugs/F98.md) | ours-retired | P3 | CHECKOUT; blamed TechDescriptionBuilding module absent | [Recorded assertion / output](../bugs/F98.md#recheck-2026-10-02--ours-retired) |
| [F99](../bugs/F99.md) | possible-unconfirmed | ? | SOURCE; endpoint dereference remains; organic throw unobserved, passive WATCH | [Recorded assertion / output](../bugs/F99.md#recheck-2026-10-02--possible-unconfirmed) |
| [F103](../bugs/F103.md) | possible-unconfirmed | ? | SOURCE + CHECKOUT; repeater retained, old consumer replaced; harm unmeasured | [Recorded assertion / output](../bugs/F103.md#recheck-2026-10-02--possible-unconfirmed) |
| [F111](../bugs/F111.md) | ours-retired | P2 | CHECKOUT; blamed ExtractorStaffedPerformance module absent | [Recorded assertion / output](../bugs/F111.md#recheck-2026-10-02--ours-retired) |
| [F112](../bugs/F112.md) | ours-retired | P2 | CHECKOUT; blamed AutomationLawCompensation module absent | [Recorded assertion / output](../bugs/F112.md#recheck-2026-10-02--ours-retired) |
| [F113](../bugs/F113.md) | ours-retired | P1 | CHECKOUT; blamed LanderCargoRatchet module absent | [Recorded assertion / output](../bugs/F113.md#recheck-2026-10-02--ours-retired) |
| [F114](../bugs/F114.md) | ours-retired | P1 | CHECKOUT; blamed TrainCargoDumping module absent | [Recorded assertion / output](../bugs/F114.md#recheck-2026-10-02--ours-retired) |
| [F116](../bugs/F116.md) | ours-retired | P2 | CHECKOUT; skip forwarding, revalidation, rehoming and final processing repaired | [Recorded assertion / output](../bugs/F116.md#recheck-2026-10-02--ours-retired) |
| [F117](../bugs/F117.md) | ours-retired | P1 | CHECKOUT; repaired argument selection and unknown-behavior decline | [Recorded assertion / output](../bugs/F117.md#recheck-2026-10-02--ours-retired) |
| [F118](../bugs/F118.md) | ours-retired | P3 | CHECKOUT; blamed LayoutTechLock module absent | [Recorded assertion / output](../bugs/F118.md#recheck-2026-10-02--ours-retired) |
| [D06](../bugs/D06.md) | out-of-scope | dsgn | AUTHORITY; design signpost, Opt-In ownership | [Recorded assertion / output](../bugs/D06.md#recheck-2026-10-02--out-of-scope) |
| [D07](../bugs/D07.md) | out-of-scope | dsgn | AUTHORITY; design signpost, Opt-In ownership | [Recorded assertion / output](../bugs/D07.md#recheck-2026-10-02--out-of-scope) |
| [D14](../bugs/D14.md) | out-of-scope | P2 | AUTHORITY; design audit owned by STANDDOWN_AUDIT | [Recorded assertion / output](../bugs/D14.md#recheck-2026-10-02--out-of-scope) |
| [C40](../bugs/C40.md) | possible-unconfirmed | ? | SOURCE; conditional bed capacity absent from law text; visible effect unmeasured | [Recorded assertion / output](../bugs/C40.md#recheck-2026-10-02--possible-unconfirmed) |
| [C41](../bugs/C41.md) | possible-unconfirmed | ? | SOURCE; picker anchor/clamp survives; missing selector cause unresolved | [Recorded assertion / output](../bugs/C41.md#recheck-2026-10-02--possible-unconfirmed) |
| [C45](../bugs/C45.md) | possible-unconfirmed | ? | SOURCE + OLD LOG; invalid-position diagnostic persists; producer unknown | [Recorded assertion / output](../bugs/C45.md#recheck-2026-10-02--possible-unconfirmed) |
| [C47](../bugs/C47.md) | out-of-scope | ? | AUTHORITY; owner retirement 2026-08-16 | [Recorded assertion / output](../bugs/C47.md#recheck-2026-10-02--out-of-scope) |
| [C48](../bugs/C48.md) | out-of-scope | ? | AUTHORITY; owner family handoff to Opt-In 2026-08-16 | [Recorded assertion / output](../bugs/C48.md#recheck-2026-10-02--out-of-scope) |
| [C53](../bugs/C53.md) | possible-unconfirmed | ? | SOURCE + OLD REPORT; menu-close lifecycle compatible; cause unresolved | [Recorded assertion / output](../bugs/C53.md#recheck-2026-10-02--possible-unconfirmed) |
| [C55](../bugs/C55.md) | vanilla-fixed | P3 | REPLACEMENT READ; repair-site duplicates excluded from ordered track elements | [Recorded assertion / output](../bugs/C55.md#recheck-2026-10-02--vanilla-fixed) |
| [C56](../bugs/C56.md) | possible-unconfirmed | P3 | SOURCE; rounding differs; old harness substitutes accepting guards | [Recorded assertion / output](../bugs/C56.md#recheck-2026-10-02--possible-unconfirmed) |
| [C57](../bugs/C57.md) | confirmed | P3 | DESK CONTROL; disabled ingredient still consumed; toggle-gate mutant rejects defect | [`python tools/desk_c57_disabled_ingredients.py`](../bugs/C57.md#recheck-2026-10-02--confirmed) |
| [C58](../bugs/C58.md) | possible-unconfirmed | P2 | SOURCE; spoilage includes meal reservations; native response unmeasured | [Recorded assertion / output](../bugs/C58.md#recheck-2026-10-02--possible-unconfirmed) |
| [C59](../bugs/C59.md) | possible-unconfirmed | P3 | SOURCE; nonadvancing helper; no literal caller found, native reach unresolved | [Recorded assertion / output](../bugs/C59.md#recheck-2026-10-02--possible-unconfirmed) |
| [C60](../bugs/C60.md) | possible-unconfirmed | P3 | SOURCE; discarded ranch list; cost unmeasured | [Recorded assertion / output](../bugs/C60.md#recheck-2026-10-02--possible-unconfirmed) |
| [C61](../bugs/C61.md) | possible-unconfirmed | P3 | SOURCE; popup promise survives removed direct applicant-removal call | [Recorded assertion / output](../bugs/C61.md#recheck-2026-10-02--possible-unconfirmed) |
| [C62](../bugs/C62.md) | possible-unconfirmed | P3 | SOURCE; unused explosion table; cost unmeasured | [Recorded assertion / output](../bugs/C62.md#recheck-2026-10-02--possible-unconfirmed) |
| [C63](../bugs/C63.md) | confirmed | P2 | DESK CONTROL; expired zero-seat disaster kept and dispatched; one-seat control stops it | [`python tools/desk_c63_zero_seats.py`](../bugs/C63.md#recheck-2026-10-02--confirmed) |
| [C64](../bugs/C64.md) | confirmed | P2 | DESK CONTROL; expired completed task retained; cleanup mutant removes it | [`python tools/desk_c64_expiry.py`](../bugs/C64.md#recheck-2026-10-02--confirmed) |
| [C65](../bugs/C65.md) | possible-unconfirmed | P3 | SOURCE; intro helper has no literal caller; native/dynamic reach unresolved | [Recorded assertion / output](../bugs/C65.md#recheck-2026-10-02--possible-unconfirmed) |
| [C66](../bugs/C66.md) | possible-unconfirmed | P2 | SOURCE; selected-group ground unload forwards all; rendered event unobserved | [Recorded assertion / output](../bugs/C66.md#recheck-2026-10-02--possible-unconfirmed) |
| [C67](../bugs/C67.md) | possible-unconfirmed | P2 | SOURCE; old reservation can debit current shift; crossover unobserved | [Recorded assertion / output](../bugs/C67.md#recheck-2026-10-02--possible-unconfirmed) |
| [C68](../bugs/C68.md) | possible-unconfirmed | P2 | SOURCE; fulfillment outside service guard; genuine failed entry unobserved | [Recorded assertion / output](../bugs/C68.md#recheck-2026-10-02--possible-unconfirmed) |
| [C69](../bugs/C69.md) | possible-unconfirmed | P2 | SOURCE; instant research changes story timing; attack-phase impact unobserved | [Recorded assertion / output](../bugs/C69.md#recheck-2026-10-02--possible-unconfirmed) |
| [C70](../bugs/C70.md) | possible-unconfirmed | P3 | SOURCE; experiment can rebind to old tank; gameplay branch unobserved | [Recorded assertion / output](../bugs/C70.md#recheck-2026-10-02--possible-unconfirmed) |
| [C71](../bugs/C71.md) | possible-unconfirmed | P3 | SOURCE; unlucky rover text has no matching effect; outcome unobserved | [Recorded assertion / output](../bugs/C71.md#recheck-2026-10-02--possible-unconfirmed) |
| [C72](../bugs/C72.md) | possible-unconfirmed | P3 | SOURCE; tutorial polling cadence survives; cost unmeasured | [Recorded assertion / output](../bugs/C72.md#recheck-2026-10-02--possible-unconfirmed) |
| [C73](../bugs/C73.md) | possible-unconfirmed | P3 | SOURCE; overwritten cached overview read; cost unmeasured | [Recorded assertion / output](../bugs/C73.md#recheck-2026-10-02--possible-unconfirmed) |
| [C75](../bugs/C75.md) | possible-unconfirmed | P2 | SOURCE; no-explosion branch lacks construction lock; play control absent | [Recorded assertion / output](../bugs/C75.md#recheck-2026-10-02--possible-unconfirmed) |
| [C76](../bugs/C76.md) | possible-unconfirmed | P2 | SOURCE; retained RP story costs meet tech-point migration; intent unresolved | [Recorded assertion / output](../bugs/C76.md#recheck-2026-10-02--possible-unconfirmed) |
| [C78](../bugs/C78.md) | possible-unconfirmed | P2 | SOURCE; old effect-key predicate survives; eligible save unlocated | [Recorded assertion / output](../bugs/C78.md#recheck-2026-10-02--possible-unconfirmed) |
| [C79](../bugs/C79.md) | possible-unconfirmed | P2 | SOURCE; exact scenario cost becomes percent boost; intent unresolved | [Recorded assertion / output](../bugs/C79.md#recheck-2026-10-02--possible-unconfirmed) |
| [C81](../bugs/C81.md) | possible-unconfirmed | P3 | SOURCE; periodic grid visibility scan survives; scaling cost unmeasured | [Recorded assertion / output](../bugs/C81.md#recheck-2026-10-02--possible-unconfirmed) |
| [C82](../bugs/C82.md) | possible-unconfirmed | P2 | SOURCE; reply-1 reactor restart missing; play control absent | [Recorded assertion / output](../bugs/C82.md#recheck-2026-10-02--possible-unconfirmed) |
| [C87](../bugs/C87.md) | possible-unconfirmed | P2 | REPLACEMENT READ; lake-height test survives safer lookup; native inputs unmeasured | [Recorded assertion / output](../bugs/C87.md#recheck-2026-10-02--possible-unconfirmed) |
| [C91](../bugs/C91.md) | vanilla-fixed | P3 | REPLACEMENT READ; repeal OnStop removes law modifiers through real lifecycle | [Recorded assertion / output](../bugs/C91.md#recheck-2026-10-02--vanilla-fixed) |
| [C92](../bugs/C92.md) | out-of-scope | P2 | AUTHORITY; separate live build prompt and shipping hold, decision 171 | [Recorded assertion / output](../bugs/C92.md#recheck-2026-10-02--out-of-scope) |
| [C94](../bugs/C94.md) | possible-unconfirmed | P2 | SOURCE; disaster comparison refuted; recurring farm damage unattributed | [Recorded assertion / output](../bugs/C94.md#recheck-2026-10-02--possible-unconfirmed) |
| [C97](../bugs/C97.md) | possible-unconfirmed | P3 | SOURCE; prior corrections applied; missed unload event remains uncontrolled | [Recorded assertion / output](../bugs/C97.md#recheck-2026-10-02--possible-unconfirmed) |
| [C98](../bugs/C98.md) | possible-unconfirmed | P3 | SOURCE; invalid-navigation loss route lacks native-state witness | [Recorded assertion / output](../bugs/C98.md#recheck-2026-10-02--possible-unconfirmed) |
| [C99](../bugs/C99.md) | possible-unconfirmed | P2 | SOURCE; legitimate last-exit guard survives; permanent stall unobserved | [Recorded assertion / output](../bugs/C99.md#recheck-2026-10-02--possible-unconfirmed) |
| [C100](../bugs/C100.md) | possible-unconfirmed | P3 | SOURCE; habitat scoring survives; migration intent unresolved | [Recorded assertion / output](../bugs/C100.md#recheck-2026-10-02--possible-unconfirmed) |
| [C101](../bugs/C101.md) | not-a-defect | P3 | INTENT + SHIPPED FILTER; must-include explicitly overrides undesired traits | [Recorded assertion / output](../bugs/C101.md#recheck-2026-10-02--not-a-defect) |
| [C103](../bugs/C103.md) | possible-unconfirmed | P3 | SOURCE; current entity shape checked; native closed/open shapes unmeasured | [Recorded assertion / output](../bugs/C103.md#recheck-2026-10-02--possible-unconfirmed) |
| [C104](../bugs/C104.md) | vanilla-fixed | P2 | REPLACEMENT READ; incompatible and hidden/unavailable policy exemptions added | [Recorded assertion / output](../bugs/C104.md#recheck-2026-10-02--vanilla-fixed) |
| [C105](../bugs/C105.md) | possible-unconfirmed | P3 | SOURCE; upgrade chain reread; no zero-saving expression found | [Recorded assertion / output](../bugs/C105.md#recheck-2026-10-02--possible-unconfirmed) |
| [C106](../bugs/C106.md) | confirmed | P3 | PRIOR ATTENDED + CURRENT SOURCE; unsuitable homeless habitat arrivals; OWNER HOLD | [Recorded assertion / output](../bugs/C106.md#recheck-2026-10-02--confirmed) |
| [C108](../bugs/C108.md) | possible-unconfirmed | P2 | SOURCE; home Health payment and service-only cure; owner closure preserved | [Recorded assertion / output](../bugs/C108.md#recheck-2026-10-02--possible-unconfirmed) |
| [C109](../bugs/C109.md) | possible-unconfirmed | P1 | SOURCE; access-failure conjunction unresolved; closed P-item preserved | [Recorded assertion / output](../bugs/C109.md#recheck-2026-10-02--possible-unconfirmed) |
| [C110](../bugs/C110.md) | possible-unconfirmed | P2 | SOURCE; direct passage expansion limited; intent and alternate routes unresolved | [Recorded assertion / output](../bugs/C110.md#recheck-2026-10-02--possible-unconfirmed) |
| [C112](../bugs/C112.md) | possible-unconfirmed | P3 | SOURCE; specific home hold can become generic; occupancy loss unobserved | [Recorded assertion / output](../bugs/C112.md#recheck-2026-10-02--possible-unconfirmed) |
| [C113](../bugs/C113.md) | possible-unconfirmed | P3 | SOURCE; cached-negative route can attempt shuttle; intent unresolved | [Recorded assertion / output](../bugs/C113.md#recheck-2026-10-02--possible-unconfirmed) |
| [C118](../bugs/C118.md) | possible-unconfirmed | P3 | SOURCE; task success includes free-space threshold; intent unresolved | [Recorded assertion / output](../bugs/C118.md#recheck-2026-10-02--possible-unconfirmed) |
| [C122](../bugs/C122.md) | possible-unconfirmed | P3 | SOURCE + ONE ARCHIVED LOG; booked unload mismatch; earlier witness missing | [`python tools/desk_c122_train_spoilage.py`](../bugs/C122.md#recheck-2026-10-02--possible-unconfirmed) |

## Fix candidates, ranked

Ranking is by harm in the stated phase, not by source oddity or ease of editing.
None is a build instruction. The held C106 is retained in the ranking so its
observed harm and the owner's boundary remain visible together.

1. **C63 — expired disaster continues after its faction loses its seats (P2).**
   Phase: a young staffed colony with politics unlocked, without stock/factory
   slack, at 1x speed. Continued disaster callbacks can prolong that disaster's
   consequences; actual additional gameplay harm was not measured by this desk
   control. Intent tell: finite `max_duration` and the existing stop branch are
   bypassed solely by the zero-seat guard. **R2**, conditional ordinary politics;
   current callbacks and Colony inheritance were enumerated, but the fixture
   does not simulate an election. The shipped recalc/update bodies retain and
   dispatch the expired zero-seat disaster; the one-seat control stops/removes it.
   Shape: a synchronous chained recalc wrapper stops already-active zero-seat
   disasters, preserving stop messages and vanilla creation/warning behavior;
   verify the complete stop-side effects before building. Current source:
   `Lua/Factions/Factions.lua:987-1067`, `Lua/Factions/FactionDef.lua:644,679`.

2. **C106 — unsuitable habitat arrival fallback (P3; OWNER HOLD).**
   Phase: early habitat-only live communities whose admission filters reject the
   arrivals. Prior attended colonists remained alive but homeless in/beside an
   unsuitable habitat; this is better than the dead-dome fallback, yet violates
   habitat residency. Intent tell: vanilla habitat safety opt-out and the
   homeless-habitat save fix-up. **R2**, previously attended ordinary passenger
   landing with travel time shortened; no module-off control or current-build
   sitting was run. The archived 2026-09-17 observation on game 1.1.0.403908 was
   reread against current `Code/Fix_ArrivalDeaths.lua:380-386,463-486` and archived
   current `Lua/_GameUtils.lua:486-501`, `Lua/Buildings/MicroGHabitat.lua:14,173-182`.
   Shape, not a recommendation: respect habitat safety eligibility in C83's
   fallback while preserving the intentional alive-but-homeless Dome behavior
   and C102's separate Dome filter. Owner, 2026-09-17: *"I am unsure if we are gonna
   mess with this, its such a niche situation and really blurring the lines."*
   **Do not build from this entry.**

3. **C57 — disabled delicacy is consumed from residual stock (P3).**
   Phase: a colony using registered DLC delicacies, where scarce ingredients have
   been disabled and are still stored before haulage drains them. Unwanted stock
   consumption undermines the player's rationing; no colony-scale loss was
   measured. Intent tells: the toggle's help and the availability check honor
   the setting while the consuming gate ignores it. **R2**, registered ingredient,
   residual stock and non-Vegan meal; callers and subclasses were enumerated.
   The real storage/gate/consumption bodies advertise disabled Meat as unavailable
   but consume it. A toggle-gate mutant removes that discrepancy; enabled, Vegan
   and registry-absent controls distinguish the conditions. Shape: a chained
   **post-wrapper** on `GetIngredientConsumeGate` masks disabled ingredients after
   the original vegan gate, retaining the complete consuming body. Current source:
   `Lua/Buildings/FoodServiceBuilding.lua:525-554,629-653` and
   `Lua/Buildings/RecipeProductionBuilding.lua:35-47`.

4. **C64 — completed opportunity's approval effect outlives expiry (P2).**
   Phase: a colony after completing a faction opportunity, with no other active
   task. This grants a persistent benefit rather than causing an immediate
   survival loss. Intent tell: authored lifetime and unconditional completed-
   promise cleanup contradict the completed-task cleanup's unrelated active-task
   guard. **R2**, normal completion followed by expiry; current hourly/event
   dispatch and Colony inheritance were enumerated. The shipped body retains the
   expired task; unnesting the real cleanup removes it, while an unexpired task
   remains. Shape: a synchronous chained post-wrapper sweeps expired completed
   tasks through the real `RemoveEffect`, preserving vanilla returns. Current
   source: `Lua/Factions/Legislature.lua:1334-1335,1445-1462,1478-1481,1497-1536`.

## What a sitting would decide

Each possible-unconfirmed entry has one deciding read below. Some require an
intent ruling, a caller, a supported save or an organic recurrence before any
sitting has a useful recipe. These conditions preserve existing WATCH closures
and owner refusals; they create no obligation or time estimate.

- **F99**: Passive watch only: an organic track completion or repair produces the current TrackElement.lua:922 endpoint throw, with logged action context proving no CheatCompleteAllConstructions.
- **F103**: If the owner reopens this WATCH item: save/load during the active mystery with the repeater sleeping, then log CrystalFlyAway posts per game hour. More than one supports duplicate lineages; one refutes the claimed mechanism. No sitting is scheduled.
- **C40**: With Crowded Living enacted and extra beds occupied, stop Ministry of Culture; capture the same residence capacity/Homeless count and rendered law/building descriptions before and after.
- **C41**: On an affected depot click, capture selector object, nonempty item count, mouse anchor, desktop box and screen appearance on the same event.
- **C45**: Passive recurrence during ordinary rocket departure outside forced bombardment, capturing the named colonist's holder, arriving, map and position at the diagnostic.
- **C53**: If subscribed-copy/dev-junction state recurs, capture UI dialog/mode, window_state, screen and reload stage at disappearance. A deliberate repeat remains optional/owner-only, not owed.
- **C56**: An attended low-performance Chicken harvest with accepted storage output compared to its pre-harvest forecast, before drones haul it away.
- **C58**: One raw-pile reservation held across decay: physical stock, request actual/target and the colonist's meal assignment before decay, after decay and after fulfillment, with unreserved-pile control.
- **C59**: A concrete shipped caller that reaches the gap-slot helper, or a native/dynamic call observation identifying this method; there is no valid gameplay sitting recipe from the current search.
- **C60**: An attended open-ranch-panel profile attributing callback frequency, allocations and meaningful frame-time cost to this discarded list.
- **C61**: Use an isolated fresh-colony non-natural-death fixture that triggers the popup; record applicant identities/pool mutations and rendered promise, separating expiry, generation and passenger launches.
- **C62**: At a naturally reached Hostage Situation detonation with a destructible neighbor, profile the allocation/time attributable to buildings_hit; determine whether removal has a player-visible cost benefit.
- **C65**: Fresh eligible sponsor-faction politics colony reaches first Council availability: count calls and observe intro. Manually display in the same state as positive display control.
- **C66**: RC Transport carrying resources in at least two displayed groups: render and choose one group's All ground-unload event; compare every resource before/after. One group or no rendered group-All item is vacuous.
- **C67**: Observe an old reservation surviving shift rollover, a new reservation counted, then interruption of the old VisitService command while the new reservation remains; read meals_this_shift before/after return.
- **C68**: A genuine same-map EnterBuilding=false on a still-valid reserved Food service, reached by play without command transport rerouting, with fulfillment/eating and skipped Service recorded.
- **C69**: In a naturally reached AI mystery, observe whether the promised intensified-attack phase produces sustained additional attacks between En Garde and Root of It popup dismissal under instant-tech-point research.
- **C70**: In St. Elmo with an old tank preserved, destroy the designated new experiment tank before fill completion and read whether the old tank is renamed/used without another ConstructionComplete event.
- **C71**: Naturally scan the first Dredger encounter, choose inspection and reach the unlucky message; read the identified scanner rover's command/status on the same line before message dismissal.
- **C72**: An attributed Basics-tutorial profile of these two threads versus equivalent slower/event-driven callbacks at the same tutorial state.
- **C73**: An attributed Food-infobar profile comparing identical refresh counts with only the overwritten cached-data read omitted, establishing meaningful cost.
- **C75**: In a naturally reached Incident emergency-shutdown no-explosion branch before researching The Incident, read the Fusion Reactor build entry and a preplaced site's construction status; compare explosion branch.
- **C76**: Owner intent decision on whether retained story crisis costs are meant to become RP initiatives or intentionally collapse to ordinary tech-point unlocks; current UI RP-price recipe cannot decide.
- **C78**: A supported platform/save-generation specimen with the old %10 effect key still serialized before this migration; inspect whether that same key survives afterward.
- **C79**: Owner migration-intent decision: whether retained exact scenario costs were deliberately replaced by a uniform 20% tech-point refund; a current research-requirement display cannot recover the old contract.
- **C81**: An attributed large-colony profile of RefreshMostVisibleGrid/CountVisibleBuildings with grid/element population held fixed and only periodic visibility refresh omitted in the comparison.
- **C82**: Naturally reach Incident, choose reply 1, research The Incident and read each existing reactor's exceptional_circumstances/working state after follow-up, comparing reply 2 on reload.
- **C87**: Only if a second field report reopens it: lake cursor entity, prefab min_z, cursor_z, ground height and resulting status on the same flat-ground sample. This is the deciding observation, not a renewed owner sitting ask.
- **C94**: An attributed outdoor-farm repeated-malfunction observation recording actual building class, responsible disaster identity and local hazard settings, so recurrence can be separated from normal vanilla disaster damage or third-party changes.
- **C97**: One Basics run: allow the rocket to finish unloading before pressing Continue into Step031, then read whether the rocket objective ticks. This decides the strongest finding; it does not settle every bundled tutorial/flag hypothesis.
- **C98**: Existing log-only DroneDrop instrument during ordinary loaded-drone drops: actual navigation validity, holder, actual pile/deposit outcome and carried amount on the same event; invalid pos is the loss-route witness.
- **C99**: If naturally reproduced: read the exact true predicate clause on a hub's final exit together with holder/traversal/marker turnover, paired native MapHasAny visibility and repair-module state; finite rescues are not permanence.
- **C100**: Owner intent ruling on whether a naturally resident jobless habitat colonist, whose listed jobs offer no free slot, should be allowed to emigrate for a dome job; C95's repair remains separately ruled.
- **C103**: On the same known tree hex, compare passage shape-test ok/reason and entity/OpenAirBuildings before and after legitimate Open Domes; standing pre-law passage pieces avoid an obstruction confound.
- **C105**: Read upgraded spire performance/automation/max_workers and dome SupplyGridBuildings.WaterReclamationSpireWaterConsumptionReduction before/after actual automation upgrade with no second spire and upgrade on.
- **C108**: If a new field report reopens it: an eligible infected colonist at cure stage under full medical coverage, pack disabled, read actual home Health payment and absence/presence of a medical visit/cure over sols. This is an evidence condition, not an owner sitting request.
- **C109**: Only if the full native predicate conjunction appears in ordinary play, read command/dome/dome_enter_fails/IsInWalkingDist/HasLocalAccess/outside_start and whether repeated loop persists without rescue. Fatal outcome remains a separate conditional observation.
- **C110**: Owner/developer intent ruling for limiting passage-only graph expansion, supported by an ordinary serial chain whose endpoint fails the independent cached walk scan and is absent from graph with no alternate transport.
- **C112**: At an ordinary manual cross-dome home assignment, read reserved_residence immediately after departure and on arrival while a competitor can claim the selected bed; show a different generic hold plus lost assigned occupancy.
- **C113**: Owner/developer intent ruling plus an ordinary cached-negative passage-connected pair reading attempted transport with a working hub; distinguish attempted shuttle from successful booking and cache-refresh window.
- **C118**: Owner decides whether retaining at least 10 free hexes is intended Prosperity for Mars task flavor or a misplaced offer-space filter; do not infer what threshold protects.
- **C122**: Witness cargo, destination bookings and station stock across the same food loss and unload with Opt-In Modules disabled after a full restart; recover the earlier archived unload witness as well. The prior sitting had Opt-In loaded.

## Rulings and evidence limits

- C47/C48 remain retired for this pack; the D entries remain design records.
  C92 belongs to its separate live build prompt and retains decision 171's
  shipping hold. This investigation does not resolve those authorities.
- C109–C117's P-items remain closed under the owner, 2026-09-26: *"marking thats
  as closed unless we get reports of actual impact"*. Rechecking entries has
  not recreated those diagnostic or sitting obligations.
- C108 keeps its built status and the skipped cure check/no-longer-tracked ruling;
  only a new field report can reopen it. C87's declined sitting is not owed.
  F99 remains passive WATCH; cheat-triggered throws do not reopen its organic
  gameplay question. C106's hold appears in the ranking itself.
- C122 is sourced to the sibling report at Opt-In commit
  `e120c83ee2bdea089fbcfd3c82b43572079873ae`. Current Train unload arithmetic was
  reread, and one archived log supports cargo loss. The earlier unload-witness
  log was not located. Name searches for spoilage callers do not prove complete
  indirect-writer coverage or native attribution. The Opt-In-disabled full-
  restart control is still absent. Its booking reconciliation is **shape, not a
  recommendation**; replacing `UnloadAll` remains the owner's FIX_POLICY §1.5
  decision, with F114's previous body-copy cost preserved in the entry.
- C105's replacement chain did not expose a zero-saving expression; the field
  report remains unresolved rather than being confirmed by its old harness.
  C59/C65 literal caller searches do not establish native/dynamic unreachability.
  C60/C62/C72/C73/C81 have no attributed performance measurement. C97's old
  corrections remain in force; deciding its strongest event race would not
  confirm every bundled tutorial hypothesis.
- No current game session, save change, TestKit probe, fix build or release was
  performed. Source-only closure of a filed expression is not an attended cure.
  The separate hotfix patch sweep remains skipped by the owner's ruling recorded
  in `76a90558`; this scoped recheck does not change that ruling.

## Completion and work attribution

All groups in the live work list completed. Entry receipts landed in
`f4d5e363` (food, story, stale pack, owner exclusions, C122 and controls),
`839f2f34` (tracks/general), `0bccccd7` (movement/colony) and `0dd4871f`
(remaining candidates). The first concurrent wave was committed together to keep
its shared generated index/catalog consistent. This report's commit also corrects
C57's recorded wrapper shape to run after the original gate, adds the structural
reconciliation tool, and consumes the executed prompt and its map row.

Validation on 2026-10-02: `python tools/doccheck.py` **GREEN** after staging the
prompt deletion; `python tools/open_bugs_recheck.py --selftest` **PASS**, including
the named falsifiers. A baseline comparison against `445a4d59` verified existing
`row_status`, identity/numbering, priorities and copy fields unchanged, and retained
statuses for every nonclosing verdict. Comparing the investigation commits' entry
paths against the report found no missing or extra member and no Code/TestKit edit.

## Findings outside the work list

No additional defect was established outside the requested set. C122 is the
explicitly requested addition. C106 is the already-filed own-code finding under
an existing owner hold, not a newly discovered throw or save-corruption defect.
