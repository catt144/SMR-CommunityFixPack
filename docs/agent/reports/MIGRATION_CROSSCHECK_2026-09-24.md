# Migration cross-check — 2026-09-24

## Must_Read_Header

Reader: the owner deciding which migration candidates merit work, and a future implementer.
This is an independent OpenAI/Codex source review of the Claude-authored migration audit.
Baseline: `c8a4aef`. Game citations below are relative to the archived
`B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src/` tree unless another
build is explicitly named. SOURCE means a read of that archive; INFERRED means a
reasoned consequence or likelihood judgement. Confirmed never means observed in play.
No game was launched, no module changed, and candidate statuses remain `cand`.

## Decision

Prioritise the pack's missing pins (P3) and arrival reservation mismatch (P2).
Keep a bounded C109 diagnostic, not a build: it is the serious candidate, but its
player route and recovery proposal are not established. Correct P1 before designing
a long-journey control. Drop C110, C111, C112 and C113 from the proposed build queue
for now: C110/C113 lack settled intent, C111 is cosmetic, and C112's actual harm
requires an uncommon race. These are recommendations, not entry status changes.

| Finding | Verdict | Practical consequence |
|---|---|---|
| C109 / N1 | **corrected** | Conditional source loop; access is not limited to twenty hexes, and hub dumps do not alone prove oxygen exposure. |
| C110 / N2 | **unproven** as a defect | One-hop admission confirmed; wider migration is not established developer intent. |
| C111 / N3 | **confirmed** mechanism | Destination registration explains the matching UI names; it does not diagnose the reporter's entire journey. |
| C112 / N6 | **corrected** | Foot/multi-leg starts can replace the reservation; direct shuttle differs, and the forced choice is not immediately cleared when full. |
| C113 / N7 | **unproven** as a defect | The negative-distance branch attempts a shuttle; intent and frequency remain unresolved. |
| P1 | **corrected** | Restarting a journey restamps. Long uninterrupted travel can still age out. |
| P2 | **confirmed** | Arrival reroute leaves a reservation in the rejected dome. |
| P3 | **confirmed** | Wrapped planner/distance bodies lack manifest pins. |
| P4 | **confirmed**, conditional | A deferred vacancy check can house a migrant temporarily at origin; vanilla shares the path. |
| P5 | **confirmed**, narrow scope | F51's cache repair is off the normal migration graph; retirement still needs a fallback reach decision. |

The field symptoms do not establish pack causation or innocence. Matching Dome/status
names have a vanilla explanation; outdoor deaths need trajectory and outside-state
evidence; unused passages have several native and pack-sensitive branches. The audit's
blanket exclusion of pack effects is stronger than its evidence. No new reporter log
was supplied during this task; no messages or save requests were sent.

## C109 — corrected: a conditional loop, not a demonstrated fatal player route

SOURCE (`1.1.1.405907`): `Lua/Units/ColonistTransport.lua:389-390` overwrites
the second argument of **every** Idle command with `"checked"`.
`Idle_TransportDestination` at :193-195 consequently returns home; :408-420 still
checks access. `SetCommand("Idle", true)` at :760 does not bypass rescue.
`CommonLua/Classes/CommandObject.lua:341-384` starts the replacement command and
deletes the old thread, with an explicit failure branch if deletion fails. This
supports the ordinary command-transfer reading; it is not a fresh engine measurement.

The loop chain holds for an outside colonist with an entry failure, a home,
`HasLocalAccess(home) == true`, and `IsInWalkingDist(self, home) == false`:
`Lua/Units/Colonist.lua:2501-2503` selects Abandoned; :1451-1477 clears transport,
keeps home and tries entry; `ColonistTransport.lua:750-760` sleeps and idles before
`Unit.EnterBuilding` can run. The counter increment is in `Colonist.lua:1416-1423`,
called after an actual entry attempt (`Lua/Units/Unit.lua:348-376`), so this guard
does not advance the teleport threshold (`ColonistTransport.lua:518-527`).

Corrections to the entry and audit:

- **Twenty hexes is sufficient, not necessary.** `HasLocalAccess` also calls
  `HasAccessViaCommunity` (:262-291); `IsDestinationInCommunityRange` (:249-258)
  accepts a nearby community's passage neighbours. `IsUnitInDomeRange` (:19-27)
  uses the community's outside-work range. The fallback at :300 is not the whole
  predicate. A farther-away colonist can still bypass rescue through these branches.
- **A hub dump is not by itself a death route.** The vendor acknowledges the dump
  in `Lua/Passage.lua:1147-1150`, but `Unit:UpdateOutside` (:468-470) treats a valid
  `passage_hub` as sheltered. `Colonist:SetOutsideEffects(false)` (:3223-3231)
  clears the outside timer and failure history. The proposed route needs readings
  of holder, hub marker, outside timer and failed entry after the interruption.
- **A pocket inside the dome is not proof of a colonist trapped outside.**
  `Unit.lua:352-368` describes an unreachable *destination* near the dome centre
  and then retries entrance points. Both Gotos must fail, with the colonist still
  outside, before that route supplies C109's precondition.

Other exits read: Idle handles committed shuttle transport, mystery commands,
sanity breakdown and panic before Abandoned (`Colonist.lua:2449-2503`). A clean
loop case excludes those interrupts. `HourlyUpdate` (:4860-4916) applies outside
damage effects; it supplies no movement rescue in that branch. The stranded
fixup (:5765-5771) restarts only an already-Stranded colonist. Abandoned clears a
transport request at :1451, so a shuttle cannot be assumed to rescue every cycle.
The pack's `Fix_ShelterReflex.lua:118-131` can interrupt Idle with Rest when a
working residence exists and half the oxygen budget is spent; entry then runs
outside the Abandoned-only guard. It is a conditional escape, not a guarantee.

INFERRED player route: while colonists use an exterior workplace or passage,
alter or demolish nearby access, or interrupt passage travel during a dome
reconfiguration; entry must actually fail and leave a position satisfying the
two conflicting reach predicates. Normal work and migration alone do not prove
that geometry. **Likely uncommon; frequency unknown.** Keep one targeted
diagnostic because the possible cost is a founder/specialist death in a small
vacuum colony. Do not build a repair from a console-created pocket alone; drop
the build proposal if ordinary actions cannot supply the predicate conflict.

Preferred conditional repair: a **guarded method bypass**, not a §1.4 chain
(because the failing branch does not call the original), tail-delegating all
other calls. Require Abandoned, a same-map Dome, and the failing walk predicate;
return false to expose vanilla's fallback. Preserve cross-map elevator handling
by delegating such calls. No synchronous data or table change has been shown to
repair the guard alone. Under §3a this is layer 2: the bypass returns immediately,
and the delegated branch has no post-work after a possible yield. A full §1.5
copy of EnterBuilding touches elevator selection and blocking entry unnecessarily.
Wrapping Abandoned pre-call cannot reach its local entry result; clearing home
pre-emptively repeats wider dome-choice effects, and a post-wrapper never runs
when the old command is replaced. Neither is preferable.

**The bypass is not yet a proven rescue.** Abandoned's fallback
(`Colonist.lua:1481-1493`) drops home, cancels housing/work reservations, wanders,
and waits; `Unit:GoToRandomPos` (:705-739) still depends on a reachable random
point. A later Abandoned can choose the same failed dome, so command alternation
alone is no success criterion. Do not broaden the bypass to TransportByFoot:
Stranded intentionally uses it for longer walks (:919-940).

Proposed measurement, not run: use the phase-2b layout only after confirming an
existing fixture with the owner. First obtain the state by ordinary passage or
workplace actions, log colonist identity/position, command, home, holder,
passage_hub, outside_start, entry count, access and walk results on the same
sample. Pair the failing case with reachable access and distant no-local-access
controls. Compare vanilla and proposed bypass for eventual safe entry or a
successful alternative route, not just exit from Abandoned. Include repeated
same-dome selection, cross-map travel, and Stranded's extended walk; record
reservation release and the oxygen budget. Engine geometry and rescue outcome
stop here pending that sitting.

## C110 — one-hop admission is real; widening it is not yet a bug fix

SOURCE (`1.1.1.405907`): `Lua/Buildings/Dome.lua:534-535,688-706,745-747`
separates direct `connected_domes` from the transitive `dome_network`.
`Lua/Units/Colonist.lua:3590-3596` expands a cluster only from a non-walk node;
the same gate is in archived `1.1.0.403908`, `Colonist.lua:3374-3380`.
The cached walk scan (:3488-3504) can still admit the far dome independently.
`Dome.lua:218-230` rejects excessive straight-line distance *before* pathfinding,
then caps the returned path length. Thus not every serial passage chain fails.

The developer's [1.1.0 announcement](https://steamcommunity.com/games/3215050/announcements/detail/719041087473189790)
describes sharing service capacity among connected domes and introducing Passage Hubs.
The [1.1.1 announcement](https://steamcommunity.com/games/3215050/announcements/detail/689769594581155953)
describes migration improvements through train transfers at Large Stations and permits
passage endpoints on Capital City edges. Neither statement specifies transitive passage
migration. The individual pages failed browser retrieval; their version-titled contents
were read through the official [Steam news API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3215050&count=20&maxlength=0)
on 2026-09-24 (news gids `1842846814454975` and `1844751498218376` respectively).
The source's work/service toggles (`Dome.lua:832-847`) concern work and services, not
an unlimited migration contract. INFERRED: widening **all cluster consumers** is a
design change, suitable for tier I/no fix. Migration-only intent remains unresolved;
do not turn that uncertainty into an asserted tier-I disposition for the entire entry.

All literal `GetClusterDomes` consumers found by recursive `grep -rn -F` over the
decoded archive were checked by group (paths below under `Lua/`, build 1.1.1.405907):

| Consumers | What global widening also changes |
|---|---|
| `Buildings/Dome.lua:805,825,829,1916,4345`; `Buildings/Workplace.lua:851,931` | Workplace lists, assignment/reassignment, service access. |
| `Buildings/Dome.lua:897`; `Buildings/Station.lua:363`; `_GameUtils.lua:457`; `Units/ColonistTransport.lua:253` | Station reach, arrival reach and local-access rescue decisions. |
| `Buildings/Dome.lua:2086,2253,2262,2315,2330,2497`; `Buildings/SecurityStation.lua:22`; `Factions/Factions.lua:298` | Media-centre coverage, crime/security and faction totals. |
| `Buildings/Dome.lua:906,923,931`; `City.lua:228,254`; `X/ColonyControlCenter.lua:1278,1311` | Dome visual opening/selection and connected-dome display. |
| `Units/Colonist.lua:1775,3593` | Service-visit selection and migration graph. |

Definitions are in `Buildings/Community.lua:569`, `Buildings/Dome.lua:745` and
`Buildings/MicroGHabitat.lua:103`; these are the presence controls in the same search.
This is a literal-reader inventory, not proof against arbitrary computed dispatch.

INFERRED player route: build serial domes A–P–B, where P is a **dome**, and leave
housing/jobs in B attractive to residents of A. Endpoints must fail the cached walk
scan and lack another admitting route. A single hub with several spokes is not this
fixture: `Passage.lua:1593-1600` pairs every hub-attached dome with the others. A player
would see B unused or a shuttle serving it. **Uncommon**, requiring a spread-out serial
layout rather than merely several domes; weaker early-game priority than the entry
implies. Drop the build proposal unless a measured layout and design ruling justify it.

| Proposed lever | FIX_POLICY shape, reach and risk |
|---|---|
| `GetNextMigrationLeg` alone | §1.4 result-widening chain, synchronous layer 3. Cannot make the automatic chooser score an absent destination (`Colonist.lua:3791-3813`). Can cover forced targets, home rescue and per-leg replanning. A false-only fallback also misses an existing shuttle leg. |
| Chooser plus leg-picker wrappers | §1.4 chains, layer 3, the least invasive plausible **migration-only** change if intent is settled. Maintain graph array, mode and predecessor together; handle already-shuttle candidates deliberately. A final walk avoids intermediate replanning but still passes the native final-leg shuttle preference. |
| Caller-scoped `GetClusterDomes` | Synchronous scoped wrapper only with a demonstrated caller marker around every planner entry, restored on returns/errors, and no scope surviving a yield. An extra call changes graph expansion itself but may expose cluster-based station/access helpers in that scope. A call-stack-name guess is not a reliable discriminator. |
| Change `connected_domes` / global cluster result | §1.3 data surgery or §1.4 global method chain, but changes all consumer groups above and the counted adjacency map used on disconnect. Reject as a migration repair. |
| Reconstruct graph/planner | §1.5 reconstruction because helpers are file-local; largest maintenance and multi-mode-routing burden. No demonstrated need over the paired wrappers. |

Control, not run: extracted real graph/chooser/leg bodies with A–P–B, hubs off/on,
already-shuttle B, forced B, non-Dome communities, and a re-plan after each leg;
assert service/work/station reach stays unchanged. Then observe the ordinary serial
layout with current cache and actual passage traversal. Stops: engine path length and
developer intent remain unresolved; no routing change is recommended now.

## C111 and C112 — narrower harm than the audit implies

**C111 confirmed mechanism, recommend drop as cosmetic.** On archived 1.1.1.405907,
`Lua/Units/Colonist.lua:3835-3840` sets the destination before walking;
:4446-4464 reads it into both names. `Lua/XDef/ipColonist.generated.lua:106-109`
uses `DomeDisplayName` linked to `SelectDome`, which also selects `self.dome`
(:4428-4431). The :4676 guard is outcome-redundant, not unreachable: :4677 and
:4714 return the same command text. A rescue names home only if a stale
`emigration_dome` does not take precedence (:4463).

INFERRED player route: let a normal foot migration begin and select its colonist
before arrival; matching names are common then, while selecting during travel is
less frequent. No housing or movement failure follows from this display alone.
Preferred optional change would be §1.3 command-text table surgery to neutral wording,
preserving the destination link; cost is localisation under §6 and changed wording
for all affected commands. Alternative §1.4 weak-memory origin wrappers must cover
both getter **and** hyperlink, tail-delegate TransportByFoot (layer 2), and disclose
vanilla display after midwalk reload. Copying a movement command for a cosmetic issue
is disproportionate. Control: direct walk, multi-leg and rescue displays, clicks,
controller rendering, localisation and midwalk save/reload. None run here.

**C112 corrected, recommend drop pending an ordinary occurrence.**
`Lua/Buildings/Residence.lua:331-353` reserves the manually selected home and forces
its dome. Foot departure (`Colonist.lua:1925-1935`), multi-leg start (:2097-2100)
and train migration (`ColonistTransport.lua:805-808`) clear the hold through
`Colonist.lua:2238-2240`, then take the first reservable home in that dome
(`Dome.lua:3482-3493`). It may be the same home. Direct shuttle booking
(`Colonist.lua:1972-1973`) preserves an existing same-dome hold through the early return.
On arrival, :3123-3130 tries the still-live forced choice first. If full it chooses
another home; :3143-3156 does **not** clear the forced choice merely for fullness.

INFERRED player route: manually send X from A to the second available residence in
B, while the generic selector prefers B's first residence; another resident must
claim the selected home before X arrives. Scarce beds and manual founder placement
make this possible, but the conjunction is **unlikely** and no field instance is
supplied. The assignment can recover while the lock holds if space reopens.
If later justified, prefer a §1.4 synchronous chain on `Dome:ReserveResidence`:
call the original, then move its reservation to a valid, unexpired, reservable
forced residence in that dome, preserving original returns and ignoring foreign
units. This incurs transient generic reserve/cancel effects (`Residence.lua:291-305,
386-400`); a pre-wrapper that reserves the chosen home **then still calls orig**
avoids that generic allocation, but must guard the target's declaring class and
let orig's same-dome early return preserve it. Compare those effects before choosing.
The entry's early-return pre-wrapper is a guarded bypass, not a §1.4 chain.
No blocking replacement or new persisted field is warranted. Control: distinct
first/selected beds, a competing resident, full/invalid/expired selected home,
direct shuttle retention, and final residence after lock expiry.

## C113 — confirmed branch, unproven defect; no route-policy change

SOURCE (`1.1.1.405907`): `Lua/Buildings/Dome.lua:308-316` can return cached `-1`
while recognising passage connectivity. `Lua/Units/Colonist.lua:1912-1924` explicitly
treats that value as infinitely far, and with a passage and available hub proceeds
to a shuttle **attempt** (:1972). `BookShuttleRide` can decline on pad/transport
checks (:1986-2011). The intermediate walk (:2195-2210) has no shuttle alternative,
so its different handling is not decisive proof of contradictory design intent.

INFERRED ordinary route: build an initially unreachable pair and then join it by a
passage while a working hub exists. A cached negative result may survive until the
daily refresh described below. Cliffs, hub spokes and obstruction do not by themselves
prove a runtime `-1`, because passages are eligible pathfinder tunnels. **Likelihood
unknown, plausibly uncommon or transient; the entry's claim that it is common is
unsupported. Drop a fix for now.** No lost colonist follows merely from preferring a
working shuttle; failed booking deserves separate observation.

If a routing-intent ruling later justifies change, §1.4 input adjustment in the
existing VacuumWalks chain is narrower than a §1.5 copy: map `-1` to `walkcap + 1`
only for a verified passage route and within the native hop cap. Layer 3 input work
and layer 2 tail delegation minimise save exposure. Risk: forcing a slow or failing
passage route instead of a valid shuttle. Control: identical endpoints with hub
on/off, before/after passage construction and daily refresh, route count/cap,
failed booking and failed passage hop; record both cached and fresh path results.

## P1–P5 — pack findings

Pack line citations in this section are at `c8a4aef`; game citations use archived
1.1.1.405907. No listed code file changed during this review.

**P1 corrected.** `StartMigration` :2097 calls `ClearTransportRequest` :2239, then
reserves at :2100. A successful restarted journey reaches the Residence hook and
restamps (`Code/Fix_StaleReservations.lua:107-114`): the audit's proposed falsifier
is already answered by source. Same-dome retarget (:1954) can skip that hook, and
one continuous MigrateStep/committed wait has no per-leg restamp (:2161-2221).
The daily age branch (`Fix_StaleReservations.lua:155-164`) can cancel that live
destination. INFERRED: long interrupted infrastructure/service availability is
the plausible player route, probably rare relative to normal travel. Do not repair
this with unconditional Dome-call restamping or an `emigration_dome` exemption;
the first misses uninterrupted travel, the second can preserve abandoned state.

**P2 confirmed.** `Lua/Buildings/RocketBase.lua:2072-2074` reserves the original
dome; `Code/Fix_ArrivalDeaths.lua:481-486` changes destination without transferring
the hold. Settlement into a new residence cancels it (`Residence.lua:111`), but
if the welcoming destination is full, `UpdateResidence` (:3123-3130) may find no
home and :3095 suppresses adding the colonist to Homeless while the old valid hold
remains. INFERRED ordinary route: arrivals rerouted from an unsuitable dome into a
working full one, precisely the C83 fallback scenario. More actionable than the
speculative migration geometries; validate the full-destination branch before repair.

**P3 confirmed.** `Code/Fix_VacuumWalks.lua:189-192,226-227` captures
`GetNextMigrationLeg` and `IsInWalkingDistDome`; its SRC manifest pins the large
caller bodies instead. The missing bodies are `Colonist.lua:3709-3717` and
`Dome.lua:299-319`. Pins are review metadata, not a runtime repair or proof that
a wrapper still composes. The existing Require/probe checks establish their stated
shape only; `update_suspect` is the core's update-reporting flag, not proof of a
vendor defect (`Code/00_Core.lua:236-252`).

**P4 confirmed conditional path, drop separate repair.**
`Code/Fix_FreedHousingNotice.lua:284-288` schedules a vacancy check;
`Residence.lua:161-169` can reach `UpdateResidence`, whose command gate
(`Colonist.lua:2889-2891`) admits MigrateStep. An unreserved homeless traveller
still registered at origin can take its newly free bed, then release it when
TransportByFoot changes dome (:3840). INFERRED: transient housing contention,
low harm; vanilla's own vacancy triggers also reach the same selector. Excluding
all migrants would hide housing from stranded/failed travellers who need it. An
alternative guard inside F59's existing deferred handler would affect only its
added trigger, leaving native triggers unchanged; a §1.5 replacement of the
shared housing selector would change too much for this transient issue. Control
any future proposal with a staying homeless colonist, a departing unreserved
migrant and an aborted migrant that needs origin housing.

**P5 confirmed narrow reach, not proven safe retirement.** The shipped literal
callers of `FindTransportationModeToCommunity` are `Lua/Buildings/SupplyRocket.lua:68`,
`Lua/UniversalRocket.lua:2229,2251` (false shuttle flag), and `Colonist.lua:2063`
(graph fallback). Forced dome makes the latter flag false at :2062. Normal chooser
uses the graph (:3791-3821). F51 still replaces :3374-3408. Drop a broad rewrite;
decide retirement on 1.1.1 only after tracing the fallback's reachable non-forced
inputs. Do not infer retirement on the still-playable 1.0.7 branch from this census.

## What the audit missed or overclaimed

**F52's stronger observation premise is not in the records.** PT-13's actual result
(`docs/archive/PLAYTEST_ARCHIVE.md`, PT-13) records passage use, then surface walking
after the passage was destroyed. It is a no-passage fallback control, not an intact
passage with the pack off. The 2026-09-23 [phase 2b record](PLAYTEST_PLAN_1.1.1_2026-09-23.md)
observes both repaired sites with the pack on. Its direct and intermediate route
observations remain valid. The ck208off log's VacuumWalks “bug reproduces” line is
a TestKit verdict; it is not an observed engine trajectory.

SOURCE: `Dome.lua:225` passes `Colonist.pfclass` (:43) to `PathLenCached`;
`Lua/Config/_pfclasses.lua:48-50` gives Colonists mask 6, including passage mask 2
(`Passage.lua:1733-1739`). Engine pfclass uses the table's index minus one
(`Lua/_fixup.lua:1543`). `Pathfinding.lua:186-205` delegates the length to engine
`ConnectivityCheck`. Registration supports eligibility, not which route was chosen
or how tunnel weight maps to reported length. F52's missing **explicit** passage
lookup is source-confirmed; mandatory surface walking/death on that particular
intact-passage fixture is unproven.

Proposed same-geometry control, not run: on a vacuum pair within the short-walk band,
keep the same intact passage, obstacles and start/destination. Compare pack disabled
after restart with pack enabled; log the route request, actual `TraverseTunnel`
entry/exit, identity, positions and outside timer. Positive control: explicit passage
movement records tunnel events. A deliberate disconnected passage must instead
record surface movement. Include both direct and intermediate legs. Merely watching
a passage with the pack on cannot discriminate the premise. The existing phase-2b
cancel-mid-route and no-passage controls remain unperformed.

**P6 was listed but discounted in the headline.** After the direct wrapper raises a
short distance (`Fix_VacuumWalks.lua:179-180`), a passage route at/above the native
passthrough cap fails the foot choice (`Colonist.lua:1922-1924`). Failed shuttle
booking (:1972-1981) then returns without a walk command. Without that raise the
short-distance call never requests the passage and takes the foot branch. This is
a conditional pack-sensitive loss of movement, already present in the audit's seat
note, inconsistent with categorical innocence. INFERRED geometry is rare; a winding
large network near close endpoints must actually be constructible. First use a desk
failed-booking control, then ordinary geometry; no fallback rewrite is proposed on
source alone. It matters more than C111's cosmetic display.

**Cached-distance age is a missed measurement dimension.** `Dome.lua:255-286` stores
walk results; `Passage.lua:1557-1590` updates connections and tunnel registration
without an immediate `UpdateDistToDomes` call. However the daily update
(`Dome.lua:1225-1228`) recomputes pairs except the straight-line `too_far` case.
This is a possible temporary stale-cache window, not proof of a permanent cache bug.
Read both cache and fresh path result before/after construction and the daily tick
when investigating C110/C113.

The review also read the audit's omitted dome worker-kick path
(`Dome.lua:1904-1942`) and shuttle executor (`ShuttleHub.lua:742-940`). Switching a
dome off interrupts its blocked workplace occupants; a shuttle needs a real task,
available pads and command acceptance. Neither makes an arbitrary C109 colonist
automatically rescued. No newly proven independent defect is claimed from these
reads. N4 and N5's owner no-fix rulings remain intact; nothing here establishes that
those rulings rested on a wrong claim.

## Ranked changes and their proof

These are proposed follow-ups, not authorisation to build or new owner obligations.
No §1.1 preset or §1.3 runtime-data change was found that repairs the movement and
reservation faults without changing broader policy; copying a blocking body is not
justified by any current result.

| Order | Recommendation / shape | Risk, alternative, and discriminating control |
|---|---|---|
| 1 | P3: add review pins, no runtime technique needed | Cheap metadata correction. Mutating each pinned body in a disposable archive must produce BODY-CHANGED; existing unchanged bodies must stay OK. Pins do not replace semantic review. |
| 2 | P2: repair the existing §1.4 Idle pre-wrapper at its reroute, layer 2 tail delegation | Move the hold through the destination's native ReserveResidence, or cancel it if no destination/home can be reserved. Preserve native cancellation/label effects and avoid affecting expedition holds. A new broad ReserveResidence replacement is unnecessary. Controls: old hold released, new bed available/full, Homeless label, no-reroute and expedition returns. |
| 3 | C109: bounded diagnostic; only then same-map EnterBuilding bypass | Serious possible harm, unresolved ordinary reach. Alternatives and layer-2 save risk analysed above. Require eventual safety and no repeated same-dome loop. |
| 4 | P1: repair the existing §1.2 daily handler's live-journey age policy only after duration control | Check actual command/task, destination and continuing validity; a stale destination field alone is insufficient. Alternative restamp on every ReserveResidence call misses one continuous journey. Long live journey must retain a bed while genuinely abandoned, invalid and dying holds still release; expedition exemption remains. |
| 5 | P6/F52: close the failed-booking and actual-route gaps before more routing edits | The hypothetical fallback must not send a no-path colonist into vacuum or fight the native hop cap. Compare successful booking, failed booking, cap boundary and no-passage cases. |
| 6 | P5: investigate retirement/re-scope, no new broad replacement | A §1.4 argument-key/cache wrapper would be preferable if a live flag collision exists; otherwise retire only the applicable branch. Trace forced, rocket and non-forced fallback calls with both flag values. |
| Drop | C110, C111, C112, C113 and separate P4 repair | Their alternatives and controls are recorded above. Widening global cluster policy is a design change; the remaining harms are cosmetic, uncommon, or intent-unproven. |

## Verification and limits

Read-only seats handled C110, C111–C113 and pack effects; the coordinating seat
handled C109 and cleared their load-bearing graph, reservation, UI, PF-mask,
booking and historical-observation claims against the archive/records. A proposed
PF-mask exclusion was rejected after checking zero-based engine indexing; it is
not a finding. Line numbers were obtained with Git's `grep.exe -n`, including
`grep -n '^' <file>` line windows. All game source was read from named archives.

Reproducible command families run on this baseline:

- `git log --oneline -6`, `git pull`, `git status --short`: up to date, clean at start.
- `grep -rn -F 'GetClusterDomes' <archive>/Src`: literal reader inventory above.
- `grep -rn -F 'UpdateDistToDomes(' <archive>/Src/Lua`: positive callers in Dome,
  OpenAirBuilding and _fixup, none in Passage; daily update explicitly read.
- `grep -rn -F 'FindTransportationModeToCommunity(' <archive>/Src`: callers named
  in P5, with its definition as the presence control.
- `grep -n -E 'dome_enter_fails|Idle_TransportDestination|HasLocalAccess'` and
  numbered full-body reads: loop and exits described in C109.
- `python tools/bodycheck.py --selftest`; then `python tools/bodycheck.py --src
  B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src --all --module <M>` for
  VacuumWalks, ShuttleHubOffAvailable, ShuttleTransportCache, StaleReservations,
  FreedHousingNotice, ArrivalDeaths and ShelterReflex: selftest and scoped checks
  succeeded. This does not clear unpinned dependencies.
- `python tools/desk_f125_vacuum.py` and `python tools/desk_migration_cluster.py`:
  completed successfully. The former stubs graph and engine movement; the latter
  loads archived 1.1.1 bodies but its empty Colonist fixture selects the module's
  single-wrapper installation. Its success does not verify multi-leg installation.

No game, save inspection, source archive mutation, module edit, new probe, or status
promotion occurred. Engine tunnel choice, genuine pocket geometry, runtime frequency,
UI rendering and successful bypass recovery remain unmeasured. Proposal controls
above are not results. Original audit seat notes remain historical evidence.

Repository verification: bug index regenerated and reviewed; doccheck GREEN. Candidate statuses and N4/N5 owner-ruling rows checked unchanged; module paths unchanged. The initial pre-stage check could not read the removed prompt still listed in the index; staging the authorised deletion cleared that procedural failure.
