# Colonist migration on game 1.1.1 — a standalone audit (2026-09-24)

Asked for by the owner after the 09-24 field reports, while their questions to the reporters
were still open: read the migration system as a whole piece, not only the diffs; say how the
pack meets it; say what 1.1.0 and 1.1.1 changed; say whether anything was missed.

## Must_Read_Header

Reader: the owner deciding what to file, what to fix in the pack and what to ask of play; then
any seat that picks one of those up. Nothing here ran the game. Every behavioural statement is
a reading of source. Game citations are SOURCE on the archived `1.1.1.405907` tree at
`B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src\Lua` unless a build is named; pack lines
are the tree at `ec3f4b9` (`Code/` unchanged since `45578d4`). Three reading seats worked disjoint
scopes; their full notes are the three companion files named in §7. A claim marked **cleared**
was re-read on the cited lines by the coordinating seat; **seat** means only the seat read it.
`HYPOTHESIS` means the code path is real but the trigger or the engine side is unmeasured.
No entry, fact or checklist item was changed by this audit; §4 lists what it recommends filing.

## Independent cross-check correction — 2026-09-24

The [cross-check](MIGRATION_CROSSCHECK_2026-09-24.md) corrects this audit's conclusions;
the original seat notes remain historical. C109's local-access bound is not just twenty
hexes, and a valid hub marker can suppress outside effects. C110/C113's mechanisms do
not establish unintended routing policy. C111 explains the display, not the reporter's
complete journey. C112's forced choice survives fullness and direct shuttle booking can
preserve its reservation. P1 restamps after a restarted StartMigration; the remaining
exposure is long uninterrupted travel. P6 contradicts categorical pack innocence.
The PT-13/phase-2b records do not supply an intact-passage, pack-off movement control.
Recommendations below are qualified by that report; no candidate status changed.

## 0 · Outcome in one screen

| question | answer | rests on |
|---|---|---|
| Did v15 miss a migration site? | **No.** Both F52 sites are repaired and the wrappers compose with every 1.1.1 caller; the retail on-leg of 09-23 watched both. | §3.1; bodycheck clean on the archived tree; `PLAYTEST_PLAN_1.1.1_2026-09-23.md` phase 2b |
| Can the pack produce the Steam symptoms? | Not excluded categorically. Native display explains (a); passage routing and failed-booking P6 can change exposure/movement. No reporter trajectory establishes causation. | §5; independent cross-check |
| What did the audit find? | Native candidates N1–N7 and pack items P1–P5. The cross-check qualifies their mechanisms, intent, reach and priorities; the original aggregate defect count was too strong. | §4; independent cross-check |
| What changed under us? | 1.1.0 moved destination choice to a route graph but kept single-hop execution. 1.1.1 executes leg by leg and re-plans at every stop. The cache F51 repairs left the main path in 1.1.1. | §2 |
| What is still unmeasured? | The engine pathfinder's passage-versus-open-ground choice, the N1 loop in play, the two owed phase 2b controls, and every decline path through the real `Require`. | §6 |

## 1 · The system as one piece (1.1.1)

### 1.1 Who starts a migration

| entry | when | cite |
|---|---|---|
| `TryToEmigrate(current_dome)` from Idle's heavy update | once per `colonist_heavy_update_time` per colonist | `Units/Colonist.lua:2538-2548` |
| `TryToEmigrate` from Idle while a user-forced dome is set | every Idle pass until the lock expires | `:2550-2551`; lock `CheckForcedDome :3134-3141` |
| `TryToEmigrate(nil, "stranded")` from the Stranded loop | hourly | `Units/ColonistTransport.lua:917, :943` |
| `TryToMigrateHome(home)` from Stranded | hourly, throttled by `stranded_migration_gt` | `:848-867, :896` |
| a rescue ride home from the `SetCommand` wrapper when home is unreachable | on any `SetCommand("Idle")` whose destination fails `HasLocalAccess` | `:461-483` (cleared: `HasLocalAccess :270-300`) |
| arrivals and expedition returns | rocket and transporter code; not the graph | `RocketBase.lua:1969-2117`, `CargoTransporterNew.lua:953-1121` |

### 1.2 Journey state on the colonist

All plain fields, so all saved. `emigration_dome` (:106), `emigration_elevator` (:107),
`transport_task` and its `dest_dome`, `shuttle`, `state`, `migration_dest` (`LRTransport.lua:27`),
`migration_step_fails` (:108), `migration_start_gt` (:109), `stranded_migration_gt` (:110),
`reserved_residence` (:91), `reserved_workplace` (:88), `user_forced_dome` (:116),
`failed_domes` and `dome_enter_fails` (:146-147), `was_abandoned` (:175). The route graph is a
per-call local and is never cached. The pack's wrappers add no field (cleared, §3.1).

Two fields are easy to confuse and the field reports turn on the difference: `self.dome` is the
dome the colonist is *registered* to; `IsUnitInDome(self)` is the dome the colonist *stands in*.

### 1.3 The planner

`BuildReachableGraph` (:3609-3662) is a breadth-first search over Communities, Stations and
Elevators with a write-once predecessor map (`AddReachableNode :3478-3486`). Arrival modes are
`start`, `walk`, `train`, `elevator`, `shuttle`. `GetNextLegToward` (:3667-3706) walks the
predecessor chain back from the destination and returns the first hop as a leg:
`{walk, dome, final}`, `{train, src_station, dst_station}`, `{elevator}` or `{shuttle, landing}`.

Three planner facts decide most of what follows (all **cleared**):

- **Walk reach is a pathfinder path length under the cap.** `AddNodesInWalkDist` (:3488-3532)
  admits a dome when `CheckWalkableDistanceCached` says so; that is `g_DomeToDomeDist`, else
  `CheckWalkableDistance` (`Buildings/Dome.lua:209-231`), a straight-line pre-reject then
  `PathLenCached` with the colonist's pathfinder class, capped at `ColonistMaxDomeWalkDist`.
  Passages are pathfinder tunnels, so that length may run through a passage; whether a walk
  then uses the tunnel or open ground is the engine's choice, not Lua's.
- **Passage reach is one hop.** `Dome:GetClusterDomes` returns `connected_domes`, the dome's
  *direct* passage neighbours (`Buildings/Dome.lua:534, :745-747`); the transitive network lives
  in `dome_network` (:535), which the graph never reads. The cluster is expanded only from a
  node that did not arrive by `walk` (`Units/Colonist.lua:3591`). A dome two passages away
  enters the graph only if its path length is under the cap, or by train, elevator or shuttle.
- **Shuttle reach is every landing pad in a city whose transport is "available"** (:3623-3659),
  and availability is `IsLRTransportAvailable` (`Buildings/ShuttleHub.lua:410-419`), which in
  vanilla counts a switched-off hub (F54; the pack corrects this, §3.2).

### 1.4 Execution

`MigrateStep` (:2155-2221) runs up to `max_migration_legs_per_step` (8, :2118) legs per
invocation and rebuilds the graph for each (:2166). Shuttle to an intermediate pad: book, stamp
`migration_dest`, return to Idle and wait for a shuttle to commit (`StartShuttleLeg :2016-2029`,
`BookShuttleRide :1986-2012`); a delivered leg re-issues `MigrateStep` from `Transport`
(:4009-4012). Shuttle to the destination or a final walk: the old `TryToEmigrateToDome`
(:1894-1982). Train: `StartTransport("MigrateStep")`, re-issued on arrival (`ColonistTransport.lua:678-703`).
Elevator: inline. Intermediate walk (:2195-2213): a passage path only when the distance is
missing, negative or above the vacuum-or-air threshold (:2198-2202), then one `EnterBuilding` per
passage element **with the result ignored** (:2204-2209), then `EnterBuilding(leg.dome)`.

`TransportByFoot` (:3835-3880) is the settling step and the whole of the old single-hop walk:
it sets `emigration_dome`, then **registers the colonist in the destination before moving**
(`SetDome(dest)` :3840, which drops the old residence and workplace, :437-438), walks the
passage elements with results ignored (:3842-3849), and enters the dome, teleporting only after
100 failed entries (`ColonistTransport.lua:518-527`).

### 1.5 Failure paths

| path | releases | leaves behind | cite |
|---|---|---|---|
| `FailMigrationStep` | nothing; sleeps and idles | `emigration_dome`, both reservations, any booked task. Idle does not resume the journey. | :2129-2137 |
| `AbortMigration` (5th failure) | `emigration_dome`, fail count, both reservations | the transport task with `migration_dest = false` | :2140-2151 |
| a failed train leg | the ticket | `emigration_dome` and both reservations; no failure counted | `ColonistTransport.lua:575-599` (seat) |
| `TransportByFootDtor` | `emigration_dome`, elevator | `self.dome == dest` even when interrupted outside | :3823-3833 |
| `Abandoned` | task and reservations | on enter failure `SetDome(false)` | :1434-1494 |
| `Stranded` | its effect and notification | hourly loop: home access, `TryToMigrateHome`, rescue ride, emigrate away, foot fallback | `ColonistTransport.lua:871-945` |

Reservations are made only at the final destination, at journey start, and held across every
leg (:2099-2109; `WaitTransport :3948`). No leg reserves at an intermediate dome.

### 1.6 What the player sees

`Getui_command` (:4672-4716) shows "Moving to a new Dome: X" for `Transport`, `TransportByFoot`
and `MigrateStep`; X is `emigration_dome`, else `transport_task.dest_dome` (:4462-4465). The
guard `and self.emigration_dome` at :4676 is dead: its `else` returns the same text (:4713-4714).
Because `TransportByFoot` registers the destination before walking, the infopanel's Dome line
and the "moving to" line name the **same dome for every foot migration** (cleared).

## 2 · What changed under us

### 2.1 1.0.7 → 1.1.0

Destination choice moved from a per-candidate transport lookup to the route graph
(`BuildReachableGraph`, 1.1.0 `:3400-3423`), scored by the extracted
`GetBestReachableCommunities`. Execution stayed single-hop: one cached mode from
`FindTransportationModeToCommunity` (1.1.0 `:3524-3525`). A dome the graph reached only by a
chain could therefore be chosen and not travelled to (seat, INFERRED). The passage network
representation changed: `connected_domes` became direct neighbours plus `dome_network` for the
closure; `Dome:GetConnectedDomes` and the city-level networks were removed. The one-hop planner
narrowing (§1.3) dates from here. `Stranded`, task expiry after one sol, the teleport rescue and
workplace reservations were all added in 1.1.0.

### 2.2 1.1.0 → 1.1.1: the multi-leg rewrite

Sixteen declarations added, sixteen bodies changed, one signature changed; 157 in scope
identical (seat inventory of 194 declarations, totals reconciled). `FindEmigrationDome` now
returns `(dome, leg)`; `StartMigration`, `MigrateStep`, `FailMigrationStep`, `AbortMigration`,
`StartShuttleLeg`, `BookShuttleRide`, `GetNextLegToward`, `GetNextMigrationLeg`,
`TryToMigrateHome` and `IsInSafeAtmosphere` are new. `Stranded` now tries a multi-leg route home
before a rescue ride and shelters only in unsafe air.

| situation | 1.0.7 | 1.1.0 | 1.1.1 |
|---|---|---|---|
| destination in walk reach or directly passage-linked | walk, optionally through passages | same execution, graph selection | final walk leg → the same walk branch, with the distance from `IsInWalkingDistDome` |
| transfers, or walk → train → walk to a non-adjacent dome | not a candidate | chosen by the graph, not executable | executed leg by leg |
| elevator or station out of walk range but on a pad | not representable | not representable | shuttle leg to the pad, journey continues |
| user-forced dome | single-mode lookup, no shuttles | same | graph routing including shuttles; single-mode lookup only if the graph cannot route |
| a journey that keeps failing | no journey state | same | five failures then `AbortMigration` |
| reservations | at the walk start or booking | plus workplace | at journey start, held across every leg |

### 2.3 Tracked sites, byte for byte

| entry | 1.1.0 → 1.1.1 | consequence |
|---|---|---|
| F51 cache key | function identical | **off the main path**: the only migration caller is the `leg == false` fallback (:2063), whose flag is false for every forced dome; three rocket callers pass `false` (cleared: four callers) |
| F52 threshold | `:1911` identical; **a second copy** at `MigrateStep :2199` | the copy has no passthrough cap and no shuttle alternative; both sites are the ones v15 repairs |
| F54 hub predicate | identical | now also feeds the graph's shuttle fill (:3639) and `BookShuttleRide` (:1991) |
| F58 reservations | identical | holds now span whole journeys |
| F59 `RemoveResident` | identical | unchanged exposure |
| F53 / C83 / C102 arrival choice | identical | arrivals do not use the graph |
| C42 passage holder | identical (`Passage.lua:1234`) | a second traversing caller, `MigrateStep :2204-2209` |

## 3 · Where the pack meets it

### 3.1 `Fix_VacuumWalks` (F52, F125) — composes; two bodies unpinned

Three wrappers: an input-only wrapper on `TryToEmigrateToDome` that raises a short vacuum
walk's distance across the lookup threshold when the domes share a passage network; a post-wrapper
on `GetNextMigrationLeg` that arms a one-call, thread-keyed marker for a non-final walk leg; and
a global swap of `IsInWalkingDistDome` that consumes the marker and reports `-1`, which
`MigrateStep :2198-2202` reads as "ask for the passage path". Checked against 1.1.1 (seat, then
cleared on :2166-2202): the distance call at :2198 is the first statement after the leg is
fetched, its argument order matches the marker, a second `GetNextMigrationLeg` in the same step
clears the marker first, and every yield comes after consumption. `AreDomesConnectedWithPassage`
reads the transitive `dome_network` (`Passage.lua:1267-1274`), so the direct wrapper acts on any
passage-linked pair; the native body then applies its own passthrough cap and shuttle choice.

Two facts to carry: the wrapped `GetNextMigrationLeg` and `IsInWalkingDistDome` bodies carry
**no manifest pin**, so a body change there is invisible to bodycheck (P3); and the module marks
**every** decline other than the 1.0.7 shape as `update_suspect` (`Fix_VacuumWalks.lua:143-149`),
where `00_Core.lua:241-249` deliberately exempts `test` and `probe` verdicts. That is the ck118
design recorded in F52, and the dialog text already names "another mod" as a cause; the
consequence is only that a mod-caused decline is reported the same way as patch rot (§5.4).

### 3.2 The other modules

| module | target on 1.1.1 | still live on the migration path? | verdict |
|---|---|---|---|
| `Fix_ShuttleHubOffAvailable` (F54) | global `IsLRTransportAvailable`, ten call sites incl. the graph's shuttle fill | yes | safe: it can only remove shuttle legs and add walks, and those walks take a passage when one exists (:1922-1924) |
| `Fix_ShuttleTransportCache` (F51) | full replacement of `FindTransportationModeToCommunity` | **nearly dead**: fallback only | P5, retire or re-scope |
| `Fix_StaleReservations` (F58) | `Residence:ReserveResidence` stamp plus a daily sweep | yes | P1 corrected: a restarted StartMigration clears and restamps; uninterrupted long travel and same-slot retargets can still age out |
| `Fix_FreedHousingNotice` (F59) | `SetResidence` post-wrapper | yes | P4, low: can house a homeless migrant in its origin dome mid-walk, as vanilla's own triggers can |
| `Fix_ArrivalDeaths` (F53/C83/C102) | `Idle` pre-wrapper on `arriving`, `OnArrival`, `GetExpeditionReturnDome` | yes; arrivals are not on the graph | P2: the reroute rewrites `emigration_dome` (`Fix_ArrivalDeaths.lua:485-486`, cleared) and leaves the arrival-time reservation in the rejected dome |
| `Fix_ShelterReflex` (F73b) | `Idle` pre-wrapper | yes | design interplay: an outdoor mid-journey idle (after `FailMigrationStep` or a shuttle drop) is sent to Rest at the **old** home; the destination reservation stays held |
| `Fix_HabitatExpeditionReturn` (C95) | `GetExpeditionReturnDome`, `SetCommand` on its own returnees | yes | no migration effect found |
| `90_SaveSanitizer` | none | — | no touch |

Bodycheck against the archived 1.1.1 tree is clean for every module above; the two
BODY-CHANGED rows (`Colonist:UpdateWorkplace`, `CargoTransporterNew:GatherAvailableColonists`)
are outside migration (seat, `python tools/bodycheck.py --src … --all --module <M>`).

### 3.3 Natural-habitat residents keeping their homes (C95) — not affected

Asked by the owner mid-audit. `Fix_HabitatExpeditionReturn` acts on the expedition-return path
(`ReturnFromExpedition` → `GetExpeditionReturnDome` → `TransportByFoot`, settled at :5463), which
is not on the route graph and which 1.1.1 did not touch: every body it pins is byte-identical
from 1.1.0 except `UpdateWorkplace`, whose change is a `ValidateWorkplace` helper swap and a
type guard (cleared by diff this session; adjudicated KEEP on 09-23,
`GAMEPATCH_1.1.1_AUDIT_2026-09-23.md`; the pin still carries the 1.1.0 hash, a standing hygiene
item). Of this audit's findings, none reaches a held habitat home: N6 does not apply because a
habitat reserves itself (`MicroGHabitatBase:ReserveResidence`, `Buildings/MicroGHabitat.lua:85-88`)
rather than picking a first free residence; P1's sweep exempts expedition holds
(`Fix_StaleReservations.lua:54-65`); and the `TransportByFoot` body C95 was built on is unchanged.
One habitat-adjacent hypothesis is recorded as N11 below; it concerns a habitat used as an
intermediate hop in someone else's journey, not a returnee's home.

## 4 · Findings

Each row: the defect, the trigger, the control that would falsify it, and what the owner
decides. Native rows are candidates for `bugs/`; none is filed by this audit.

### 4.1 Native, not in the library

| id | defect | trigger | falsifier | status | recommend |
|---|---|---|---|---|---|
| **N1** | A colonist with `self.dome` set and one failed entry loops Idle → Abandoned → a walk-cap guard that sleeps and idles **without moving or counting a failure**, standing outside until it suffocates; the teleport rescue needs 100 counted failures. `Colonist.lua:2501-2503, :1452, :1477`; `ColonistTransport.lua:753-760`; `:518-527`. | HasLocalAccess(home) passes while capped walking fails; the twenty-hex fallback is not the whole predicate, and a hub dump alone does not establish oxygen exposure | a colonist in that state moves, or the log shows `dome_enter_fails` rising | **cleared** path; trigger frequency HYPOTHESIS | conditional diagnostic: fatal ordinary-play route and recovery unproven |
| **N2** | Passage reach in the planner is one hop, from non-walk nodes only; a dome two passages away and beyond the cap by path is shuttle-only or unreachable. `:3591-3596`; `Dome.lua:534, :745-747`. Dates from 1.1.0. | A–P–B passages, A→B path over the cap | B appears in the graph as `walk` | **cleared** | file, P2: it changes where colonists can go; the legacy walk test (`Dome.lua:315-316`) still honours the whole network, so the developers' intent is unclear |
| **N3** | `TransportByFoot` registers destination before the walk (:3840), so both display names agree. The `Getui_command` guard is outcome-redundant (:4676, :4713-4714); rescue text uses home only without a higher-precedence emigration_dome (:4463). | foot migration; qualifying rescue | the Dome line mid-walk shows the origin | **cleared mechanism, qualified by cross-check** | cosmetic explanation; not a diagnosis of the reporter's complete journey |
| **N4** | `FailMigrationStep` and a failed train leg leave `emigration_dome` and both reservations in place and Idle never resumes the journey; a stale `emigration_dome` then outranks a later rescue ride's destination in the status text. :2129-2137; `ColonistTransport.lua:575-599`. | one failed leg | the reservation is cancelled before the next heavy-update re-plan | seat | **Owner ruling 2026-09-24: no fix.** The next re-plan releases the reservations anyway; file as a note only |
| **N5** | `AbortMigration` keeps the booked shuttle task with `migration_dest = false`; a shuttle can later fly the colonist to the intermediate pad and register it there without a reservation, or leave it at a station or elevator. :2143-2146, :3968, :3946-3947. | abort while a leg's ride is booked but uncommitted | the task is cleared after an abort | seat | **Owner ruling 2026-09-24: intended, no fix.** The developers' comment keeps the ride deliberately, and stations and elevators are legitimate leg targets in 1.1.1, so a wrapper would interfere with real journeys; the game's own rescue and Stranded paths recover from a stray landing. Tier I note only |
| **N6** | Foot/multi-leg start clears the selected reservation and may take a different generic home (:1925, :2097-2100; `Dome.lua:3482-3493`). The forced choice remains; direct shuttle can preserve the hold. | cross-dome assignment plus competing occupancy | the selected hold survives departure | **corrected by cross-check** | uncommon race; no build recommended pending occurrence |
| **N7** | A negative cached distance is treated as infinitely far, so a passage-linked final leg with an available hub attempts a shuttle (:1912-1924, :1972). Booking can fail; ordinary frequency is unknown. | passage-connected pair with runtime -1, hubs on | the branch selects passage walking | **cleared mechanism; intent unproven** | design question; no routing change recommended |
| N8 | The intermediate walk in `MigrateStep` applies no `ColonistMaxPassagePassthroughDomes` cap and offers no shuttle alternative (:2195-2212); a short leg can become a long passage detour. | ≤ cap leg, long passage chain | — | cleared reading | note only; safe in vacuum, slow |
| N9 | Passage-hop `EnterBuilding` results are ignored in both traversing callers (:2204-2209, :3842-3849); a failed hop continues from wherever the colonist stopped. | a passage removed or blocked mid-walk | a hop failure stops the walk | seat; engine side HYPOTHESIS | file with N1 if play shows it; it is the mechanism by which more passage routing raises exposure |
| N10 | `pairs(self.failed_domes)` in Abandoned runs on `false` or `nil` (:1458; class default :147; reset :3229). | Abandoned with no dome, no safety dome, no recorded failures | no error at :1458 in any log | HYPOTHESIS (engine `pairs` on false) | check one log before filing |
| N11 | Inside a natural habitat `IsUnitInDome` is falsy, because it returns the holder building's `parent_dome` (`Buildings/Dome.lua:158-165`, cleared), so an intermediate walk leg into a habitat never registers as arrival: the same leg can repeat until the eight-leg bound, then `FailMigrationStep`. :2162-2166, :3504-3508. | a route that passes through a habitat with an onward station | the next iteration plans past the habitat | HYPOTHESIS; whether a habitat can be an intermediate node was not established | check the graph on a habitat-and-station layout before filing |

### 4.2 Pack-side

| id | defect | trigger | falsifier | status | recommend |
|---|---|---|---|---|---|
| **P1** | `Fix_StaleReservations` can expire a long uninterrupted journey. Restarted StartMigration clears then re-reserves (:2097-2100, :2239), so it DOES restamp; same-slot retargets and continuous legs need separate treatment. `Fix_StaleReservations.lua:104-114, :155-162`; `Dome.lua:3483-3485`. | a long journey, e.g. a stranded wait | a continuous live journey retains its slot beyond timeout | **corrected by cross-check** | control live journey versus abandoned hold; neither blanket restamping nor emigration_dome alone is sufficient |
| **P2** | `Fix_ArrivalDeaths`' C83 reroute rewrites `emigration_dome` but leaves `reserved_residence` in the rejected dome until the colonist settles or the sweep runs. `Fix_ArrivalDeaths.lua:485-486`; `RocketBase.lua:2072-2074`. | an arrival whose chosen dome was reservable but unwelcoming | `reserved_residence.parent_dome` equals the new dome after the wrapper | **cleared** mechanism; harm HYPOTHESIS | fix: cancel or move the reservation with the reroute |
| **P3** | `Fix_VacuumWalks` wraps `GetNextMigrationLeg` and `IsInWalkingDistDome` without manifest pins. | the next game patch | — | **cleared** | add `SRC:` pins for both bodies (FIX_POLICY 2b) |
| P4 | `Fix_FreedHousingNotice` can house a homeless, unreserved migrant in its origin dome while it walks away in `MigrateStep`; the bed is dropped on arrival. `Fix_FreedHousingNotice.lua:284-288`; `Residence.lua:161-169`; `:3123-3130`. | a vacancy in the origin dome during the walk | the migrant stays homeless after the deferred check | seat | low; vanilla's own triggers do the same |
| **P5** | `Fix_ShuttleTransportCache`'s repaired dimension is unreachable on the 1.1.1 main path (§2.3). | any 1.1.1 migration | a 1.1.1 call with a varying truthy `shuttles_available` | **cleared** (four callers) | owner decides: retire, or re-scope F51 to the fallback |
| P6 | After the direct raise, a pair with eight or more intermediate passage domes, hubs "available" and a failing `BookShuttleRide` ends with no command, no reservation and no counted failure; vanilla would have walked outside. `Fix_VacuumWalks.lua:179-180` → :1922-1924, :1972-1981. | that geometry plus `IsTransportAvailableBetween` false | a desk leg ending in `TransportByFoot` | seat; reach HYPOTHESIS | add the desk leg; the geometry is rare |
| P7 | `Fix_ShelterReflex` sends an outdoor mid-journey colonist to Rest at its old home; the journey resumes only at the next heavy update. | `FailMigrationStep` or a shuttle drop outdoors | — | seat | owner ruling on which regime the reflex protects |

## 5 · The field reports, read against this audit

Timestamps and the pack-version reasoning are in the session's earlier assessment; this section
adds only what the audit changed.

### 5.1 (a) "moving to a new dome, which is the dome they live in"

Native, by construction, and now explained rather than only excluded: **N3**. On every foot
migration the colonist is registered in the destination before it walks, so the Dome line and the
"moving to" line agree for the whole walk; a rescue ride home and a stranded return name the
home dome as new. The pack lengthens the window by choosing passage detours over short outside
walks, and destination choice still runs native graph/scoring. The leg picker IS wrapped by F125;
its wrapper marks a subsequent distance query. Removing shuttle availability can change the
candidate set and therefore the chosen destination.

### 5.2 (b) "walk outside, stuck near passages and production buildings, suffocate"

The most complete native mechanism is **N1**, which needs conflicting access/walk predicates after an entry failure. It is not proof that
every such colonist remains motionless or suffocates; see the cross-check for interrupts and hub shelter state. **N9** is how a passage route
turns into an outside walk when a hop fails. The engine chooses the eventual path; the pack changes routing inputs and does
route more colonists into passage traversal, so it raises exposure to N1 and N9 without causing
either. `Fix_ShelterReflex` can add an outdoor leg toward the old home (P7). If the vacuum-walk
fix is inactive on that rig, the symptom is plain vanilla F52.

### 5.3 (c) "other colonists don't use passages between domes"

The cross-check rejects a categorical exclusion of pack influence (see P6). In ordinary eligible short-leg cases, `Fix_VacuumWalks` only moves inputs *into* the
passage lookup and `Fix_ShuttleHubOffAvailable` only forces walks. Native explanations, in
order of reach: **N2** (a dome two passages away becomes a shuttle leg or is unreachable),
**N7** (a passage-only pair books a shuttle when any hub is available), a breathable map
(vanilla walks outside under the passage threshold by design), eight or more intermediate domes
(a shuttle by design), or the fix declined on that rig.

### 5.4 The "switched itself off" dialog on other rigs

On stock 1.1.1 with v15 every check in the module is pure Lua against code-defined values, so a
difference between rigs needs a mod, a mod-altered constant, another game build, or v14. The
two checks a third-party mod would plausibly trip: the threshold-gap test (a "walk further" mod
that raises `const.Colonist.ColonistMaxDomeWalkDist` to the passage threshold or above) and the
`StartShuttleLeg` probe (a transport mod wrapping that method). Each writes its own reason on the
`[CommunityFixPack] VacuumWalks:` log line, which is why the log settles this and a save does
not. On v14 the probe called the 1.1.1 body with a table stub and reached `IsSameMap` on Lua
tables (:1943); on the owner's rig that applied (archived ck208on log, line 94), and there is no
evidence it behaves differently elsewhere (seat HYPOTHESIS, not adopted).

## 6 · What is not measured, and what would measure it

- **N1 in play.** Strand a colonist in a pocket within twenty hexes of its dome on the phase 2b
  fixture and watch whether it ever moves. One sitting.
- **The two owed phase 2b controls**: cancel-mid-route and the deliberate no-passage fallback
  (`PLAYTEST_PLAN_1.1.1_2026-09-23.md`, "Not run").
- **The desk does not run the real planner.** `tools/desk_f125_vacuum.py` (25/25 held at
  `b06d6b8`) stubs `BuildReachableGraph` and `GetNextLegToward`, never composes the hub-off
  wrapper, never fails a `BookShuttleRide` or a passage hop, and never reaches a decline through
  the real `Require`. `tools/desk_migration_cluster.py` (16/16) loads the module with an empty
  `Colonist`, so it measures the **1.1.0** single-wrapper install, not the 1.1.1 one, though its
  header says 1.1.1. The TestKit probe (`20_Probes_Wave2.lua:569-634`) drives only the direct
  wrapper.
- **Engine side.** Whether a plain walk goes through a passage tunnel or over open ground;
  `pairs(false)`; `DeleteThread` on the current thread after `SetCommand("Abandoned")` without a
  `return` (:3866); persistence of the weak `failed_domes` metatable across a load. None is
  decidable from Lua.
- **Not read.** `GetScoreFor`, `HasFreeLivingSpaceFor`, the global `ChooseResidence` (which decides
  whether N4's reservation actually leaks), `CargoShuttle:TransportColonist` beyond how it ends a
  task, and the four 1.1.1 `Dome.lua` worker-kick additions.

## 7 · Method and the not-opened list

Three tier-2 reading seats with disjoint scopes, launched in parallel, read-only, no game run,
no git write, no gate: (A) the native 1.1.1 system as a standalone piece; (B) a declaration-level
diff across `1.0.7.396349`, `1.1.0.403908` and `1.1.1.405907`; (C) every pack touch point on the
1.1.1 tree, with bodycheck and both desk harnesses run. Their notes, verbatim, are
[`MIGRATION_AUDIT_2026-09-24_A_native.md`](MIGRATION_AUDIT_2026-09-24_A_native.md),
[`MIGRATION_AUDIT_2026-09-24_B_diff.md`](MIGRATION_AUDIT_2026-09-24_B_diff.md) and
[`MIGRATION_AUDIT_2026-09-24_C_pack.md`](MIGRATION_AUDIT_2026-09-24_C_pack.md); each ends with
its own commands-run and not-done lists, and B's inventory of 194 declarations with per-step
status is in its §1. The coordinating seat cleared each claim marked **cleared** above by
re-reading the cited lines on the archived tree (`sed -n` ranges over `Units/Colonist.lua`
1445-1486, 2497-2510, 3589-3597, 3835-3841, 4461-4466, 4672-4680, 4710-4716;
`Units/ColonistTransport.lua` 268-300, 516-527, 748-762; `Buildings/Dome.lua` 209-251, 296-330,
532-536, 744-748, 3482-3493; `Buildings/ShuttleHub.lua` 408-418; `Code/00_Core.lua` 236-252; the
four `FindTransportationModeToCommunity(` callers by grep). Seat C disclosed two brief
deviations: bodycheck output first written to `/tmp` and then deleted, and one difflib script run
from a heredoc (it contained no backslashes). Nothing in this audit changed an entry, a fact, the
checklist or code.
