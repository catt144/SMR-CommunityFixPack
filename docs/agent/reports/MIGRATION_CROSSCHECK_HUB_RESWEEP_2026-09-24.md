# Migration cross-check: measured hub resweep — 2026-09-24

## Must_Read_Header

Reader: the owner and coordinating seat deciding what to build and file after the
TheGodUncle sitting. This supplements, and revises the recommendations in,
[the cross-check based on c8a4aef](MIGRATION_CROSSCHECK_2026-09-24.md).
Inputs were read in the requested order: [field findings](HUB_FIELD_FINDINGS_2026-09-24.md),
[hub source audit](MIGRATION_AUDIT_2026-09-24_D_hubs.md), then the complete
[Passage Network 1.38 code](../../archive/PassageNetwork_1.38_Code_PassageNetwork.lua).
Starting HEAD was `536db7d`; the concurrent handoff advanced it to `2eadd83` during
review. SOURCE-VERIFIED means independently checked archived Lua, not a game result.
MEASURED refers to the owner's recorded sitting; HYPOTHESIS identifies a remaining
causal or engine claim. Every game citation below uses build **1.1.1.405907**, relative
to `B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src/`, unless explicitly stated.
This is report-only: no implementation, entry/status change, or new game sitting.
Proposed controls are not results or newly assigned owner obligations.

## Decision

**Put S1's missing passage-origin access first, followed by S2's obsolete rescue
pickup.** The ordinary route and serious harm are now evidenced. C109 remains a
separate conditional failure and is not the explanation for this save. C111's own-home
rescue wording is measured and recurrent: withdraw its unconditional drop recommendation,
but keep its cosmetic repair behind movement safety. Preserve the last-exit demolition
safeguard; the evidence does not establish an undismantlable passage.

The proposed S1 wrapper is correct **as a narrowly guarded connectivity fallback**,
not as an unconditional `holder/marker -> dome_network -> true` test. Its physical
origin check and the actual route taken after granting access remain build controls.
The centre-based workplace metric is source fact; that does not make changing the
global workplace radius the right repair.

## What the measurements establish, and corrections to their summary

Log aliases in this report:

- **OFF**: [reporter_TheGodUncle_modsoff_Mars.exe-20260924-12.55.27-6aad2d75.log](../../archive/logs/reporter_TheGodUncle_modsoff_Mars.exe-20260924-12.55.27-6aad2d75.log).
- **ON**: [reporter_TheGodUncle_modson_Mars.exe-20260924-13.07.16-6aad2d75.log](../../archive/logs/reporter_TheGodUncle_modson_Mars.exe-20260924-13.07.16-6aad2d75.log).

MEASURED: own-home Transport tasks occur in both samples. ON:640-643 and :660-663
track the same named colonists: access fails at positions beyond the centre range;
some later reach work/services; colonist `2000011174` goes from hub holder/marker,
access true and a new task, to no holder/marker, access false, pickup-ready and a
running outside timer. The owner witnessed a death on this route. That observation
is accepted; the two SMRWATCH snapshots alone do not timestamp booking, identify
the pickup anchor, or record the door-versus-tunnel trajectory. The field report's
last section correctly leaves that anchor measurement open. Its earlier description
of the entire intervening trajectory is stronger than these logged snapshots.

MEASURED: ON:697 reports hub 2692's listed and holder-matching populations both as
71, with invalid and holder-mismatched populations both zero. This checks the
**holder relation**, not physical footprint membership. ON:713 and :722 enumerate
the changing member sets; the common handles are `2000012765` (Transport→VisitService),
`2000018440` (VisitService→Rest), `2000021723` (VisitService→Roam), and `2000023003`
(Transport→VisitService). Those reads support throughput, not a permanently stuck
population. ON:730 later reports 35 of 45 held units beyond collision radius 2309;
the earlier holder count and this later count are different snapshots, not a mismatch.
Neither collision-radius distance nor `holder == hub` determines the walkable footprint.

Corrections found by checking the raw inputs:

- **Census:** OFF:718-735 and :747-764 each reconcile to 858, all Brussels. ON:606-623
  instead reconciles to **868**: Brussels 853, Prague 2, Bern 1, Strasbourg 0,
  Amsterdam 2, Tallinn 1, Paris 0, berlin 3, London 2, Paracelsus #1 1, Planck #1 3.
  These named rows explain the difference; “858, all Brussels, both runs” is false.
  The snapshots do not identify which births, deaths or migrations changed the census.
- **Control configuration:** OFF:742 and ON:380 are live SMRTK fingerprints. Both
  include the pack, TestKit, Opt-In Pack, RailShaftDev and TrainHubDev; ON additionally
  includes Passage Network (`iooW34Y`, definition ON:61). “Pack only” is shorthand
  that is too strong. This is a Passage Network off/on comparison, not a completely
  unmodified-game control. VacuumWalks is applied in OFF:97 and ON:95.
- **Service wrapper:** the field report's “redundant” verdict is wrong. Although
  `Lua/Stats.lua:536-546` dispatches across `dome_network`, its called
  `PlaceServiceInConnectedDomes` reads **`home.connected_domes`** at :375-386.
  The mod's temporary substitution (:54-94 of the archived mod) therefore widens
  service-capacity distribution. Restoring the tables does not undo those allocations.
- **Oxygen:** a valid marker suppresses `Unit:UpdateOutside` (:468-470) and the
  normal stop/exit checks. It does not make every oxygen-start path impossible:
  `Lua/Buildings/Dome_Entrance.lua:71` sets outside unconditionally. A later
  marker-aware stop can clear that timer again. “A marked colonist never starts
  the timer” overstates the source, although the watched exposed colonist had
  already lost its marker.
- **Version continuity:** the access predicate, its centre-distance helper,
  SetCommand rescue dispatcher, task-position capture and passage traversal bodies
  compare identical to archived **1.1.0.403908**. Transport's pickup/wait core is
  unchanged, but its full body is not: 1.1.1 adds multi-leg destination handling
  and continuation. The new dome-off worker interrupt is another changed exposure
  source. “Every line unchanged” is sound for the identified defect expressions,
  not for all surrounding control flow.

The owner reports no entry failures. Independently, every emitted SMRCOL row in
both logs has `fails 0`; neither sample contains Abandoned. This clears the sampled
C109 precondition in the negative, not every possible future colonist state.
SMRNET's emitted edges all reconcile their stored and real-link counts, and their
per-dome neighbour summaries reconcile with the emitted edges. Together with the
owner's missing-link check, this refutes the proposed connection-table residue in
these runs. It does not measure historical corruption in every possible save.

## Re-verdict of the original cross-check

The pack files cited by the original report have no diff from `c8a4aef` through
the reviewed HEAD. Archived source fingerprints were checked rather than treating
new field observations as evidence that unrelated reservation code changed.

| Original finding | Resweep verdict | What changed / resulting recommendation |
|---|---|---|
| C109 / N1 conditional entry-failure loop | **CONFIRMED**, conditional; field attribution **unproven** | The original correction holds. No observed entry failure; access false selects rescue before the proposed Idle/Abandoned loop. Withdraw C109 as the leading diagnostic for this report. Retain its separate ordinary-geometry sitting only if that predicate conjunction is actually found. Its bypass still has no proven eventual recovery. |
| C110 / N2 one-hop admission, intent unresolved | **CONFIRMED** mechanism; defect **UNPROVEN** | Passage Network actually widens the cluster, including migration consumers. Clean vanilla hub pairing remains enough for a single hub's spokes; transitive serial migration intent is still not established. Symptom (c), unused passages, was not isolated. No global-cluster repair. |
| C111 / N3 matching names; drop as cosmetic | **CORRECTED recommendation**, mechanism **CONFIRMED** | The repeated own-home rescue is now a measured player route, not merely a possible selection during ordinary migration. It explains the wording, not a decision to emigrate to the same home. Keep an optional rescue-specific/neutral text repair after safety; do not copy a movement command for UI. |
| C112 / N6 specific-home reservation loss | **CONFIRMED corrected finding**; observed harm **UNPROVEN** | Foot/multi-leg reservation replacement and direct-shuttle distinction remain. These rescue tasks do not demonstrate the manual-home/competing-bed race. No build promotion. |
| C113 / N7 negative-distance shuttle preference | **CONFIRMED** branch; defect **UNPROVEN** | Home rescues use HasLocalAccess and CreateColonistTransportTask; they are not evidence of cached `-1` final-leg migration. Keep the intent/cache/failed-booking controls. |
| P1 live reservation aging | **CONFIRMED corrected finding** | Restart restamps; an uninterrupted journey may age out. No reservation-duration measurement here. No blanket emigration exemption. |
| P2 arrival reroute leaves old hold | **CONFIRMED** source finding | New readings neither test nor repair the full-destination/Homeless-label branch. Still a useful separate targeted repair. |
| P3 missing planner/distance pins | **CONFIRMED** | Metadata gap remains; cheap independent work, not a remedy for this rescue chain. |
| P4 deferred origin housing | **CONFIRMED**, conditional | No measured contention. Keep the low-priority/drop-separate-repair recommendation. |
| P5 F51 cache repair off normal migration graph | **CONFIRMED**, limited | No new non-forced fallback observation or 1.0.7 evidence; retirement remains unproven. |
| F52 explicit passage lookup vs actual engine route | **CONFIRMED evidence gap** | The rescue observations are not an intact-passage pack-off/on migration control. Tunnel eligibility still does not settle engine route choice. Existing phase-2b controls remain open. |
| P6 short-distance raise + hop cap + failed shuttle booking | **CONFIRMED conditional source interaction**; ordinary geometry **UNPROVEN** | These own-home rescues do not exercise that branch. Retain the qualification against universal pack innocence, without attributing this field failure to P6. |
| Temporary stale distance cache after connection | **CONFIRMED possibility**, actual instance **UNPROVEN** | Connection tables being clean does not measure the separate distance cache. Daily-refresh distinction remains. |
| Worker-kick and shuttle executor supplied no independent defect | **CORRECTED scope** | The new hub audit connects an ordinary interrupt to the pre-existing access/pickup defects. A worker kick need not itself be defective to expose S1/S2. A working shuttle still is not a guaranteed timely rescue. |
| N4/N5 owner no-fix rulings | **CONFIRMED unchanged disposition** | No new evidence overturns their conditions; no status change. |
| Desk/body checks and their limits | **CONFIRMED historical results only** | No code changed, so no claim that re-running them would validate hub physics. Their stubbed movement and incomplete multi-leg installation coverage remain limits. |
| Broad “outdoor deaths still unexplained” priority | **CORRECTED** | The owner has now observed the serious rescue chain. S1/S2 outrank the original C109 diagnostic. Broad immunity for every mod/pack path remains unproven; the specific Passage Network residue explanation is refuted. |

## S1 — access from an actual passage origin

**SOURCE-VERIFIED; false access and rescue are MEASURED.**
`Lua/Units/ColonistTransport.lua:270-300` first preserves same-map and in-dome
access, then tests an explicit reference dome or the nearest community and home.
`HasAccessViaCommunity` (:262-268) requires the holder or colonist to be in the
community's centre-based work range before testing destination reach. The final
fallback also measures holder/colonist to destination, at :293-299. The range
helper at :19-28 recognises dome hexes, then measures to the centre. It never
recognises an actual passage/hub origin as its own connected access point.
`Lua/Buildings/Workforce.lua:131-136` and `Buildings/Dome.lua:2349-2363` confirm
the range semantics. For this Geoscape geometry, being beside a connected shell
does not guarantee any community passes the centre test.

**Player route:** use a native hub between a large home dome and work/service
domes, then encounter a normal command interruption while crossing or on the hub.
Work reassignment/dome shutdown is a concrete player trigger (`Colonist.lua:1755-1758`;
`Buildings/Dome.lua:1905-1935`). No failed entry, altered radius, modded network,
or forced console position is needed for the false-access mechanism. A nearer
small community can make the same test pass, so not every hub or interruption fails.

The proposed wrapper's justified shape is a synchronous §1.4 **result-widening
chain** on `Colonist:HasLocalAccess`, with no new persisted state or blocking frame
(FIX_POLICY §3a layer 3). Call the original with both arguments and preserve its
successful result; add a true result only after establishing all of the following:

1. The unit and destination are valid and on the same map. The destination is a
   Dome, or a building with a valid Dome `parent_dome`; a random outdoor target,
   habitat, station or elevator must not be relabelled as a dome by proximity.
2. This is the **current-position** query. The explicit `dome` argument at
   `ColonistTransport.lua:447` asks about access *from home*. Preserve that
   hypothetical-origin contract instead of letting the current hub override it.
3. Physical occupancy of a live hub or passage is established, including its
   actual walkable ramps/height. Neither `passage_hub` alone nor `holder == hub`
   alone proves this. An active traversal can use its live passage/element
   relationship, but stale traversal fields must also fail closed.
4. A still-connected endpoint dome's network contains the destination dome, and
   the origin still has a usable connection into that network. A hub itself has
   `hub_domes`, not `dome_network` (`Lua/PassageHub.lua:9-15`); derive the network
   through a valid attached dome (`Passage.lua:1593-1601`, `Dome.lua:688-706`).
   A valid marker to an isolated hub, disconnected element, or dismantled branch
   is not connectivity. Membership is topology, not proof of the engine's next route.

This is a recommendation for the **first bounded repair**, not clearance to ship
a marker-only approximation while the footprint is unknown. A home-only variant
is narrower but leaves Work/VisitService interruptions taking indirect recovery
paths. Full destination-dome reach is justified for physically connected travel;
it must not silently import Passage Network's assignment policy into vanilla.

### Effects beyond migration

The literal callers are the transport dispatcher at `ColonistTransport.lua:416`,
its home-relative fallback at :447, its rescue check at :461, and Stranded at :888.
Definitions and these callers were found in a decoded-tree search. The dispatcher
uses it for commands with transport destinations unless they supply their own
reach predicate (:406-417). Work, VisitService, Idle, Rest and Roam are consequently
in scope (:193-247), as are applicable arrival/elevator commands.

| Surface | What a guarded S1 fallback changes, and what remains separate |
|---|---|
| Work | An already assigned worker on a passage can continue to an in-dome workplace rather than request transport/rescue. It does not expand workforce assignment radius or jobs. `SetWorkplace` has its own range/cluster calculation (`Colonist.lua:1769-1786`), which remains unchanged. Outdoor worksites with no Dome parent retain native access checks. |
| Services | An already selected in-dome service can become locally reachable from the passage. That can avoid train fallback, the unreachable-service cooldown, and a home detour (:436-452). It does not change capacity allocation, interests, or cross-dome service toggles. |
| Stations | A true local result bypasses the later general train search for that destination. Existing cached work-route handling runs earlier (:392-404). Station labels, `Station:IsBuildingConnected` (`Buildings/Station.lua:352-374`), GetStartingPoint and the transport graph are not repaired or widened by this wrapper. A station with no valid Dome parent gets no new grant. |
| Migration/rescue | It prevents some unnecessary rescue bookings and lets Stranded try GoToDome. It neither widens the migration chooser nor guarantees that the resulting engine movement uses a passage. It also does not cancel an already booked obsolete pickup. |

**S1 falsifier/sitting — large-dome interrupted crossing, not run here:** compare
the same natural interruption with and without the proposed fallback, Passage
Network off first. Capture origin footprint/height, holder, marker, active traversal,
destination, optional reference dome, live endpoint/network, original access result,
command and subsequent tunnel events. Success is safe entry without a rescue loop,
not merely `access == true`. Controls: a small dome, a connected destination already
accepted by vanilla, unrelated destination, same network but physically off-hub stale
marker/holder, removed last connection, cross-map destination, outdoor workplace,
service denied by native policy, and a valid station commute. A grant from a stale
origin, suppression of a needed train, entry failure, or an unsafe surface path
falsifies the proposed implementation. Hub footprint and engine route choice stop
unproven pending this sitting; no radius-based substitute is cleared by this review.

## S2 — an obsolete pickup can send a rescued colonist back outside

**SOURCE-VERIFIED mechanism; harmful pattern MEASURED; exact anchor/trajectory
HYPOTHESIS.** `ColonistTransport.lua:461-474` books an own-home rescue before
transferring command. `Lua/LRTransport.lua:86-124` validates destination/map/pads,
then for a false source captures `colo:GetPos()` at :106-111, creates and registers
the task. The passage walk runs inside its destructor (`Lua/Passage.lua:1205-1246`);
`CommonLua/Classes/CommandObject.lua:363-368,441-459` allows that walk to finish
before command replacement completes. Thus booking position can precede actual
Transport start. Transport obtains a passable pickup, exits its holder, walks
there and marks readiness (`Colonist.lua:3973-3986`); it does not first ask whether
the rescue is obsolete because home has already been reached. The wait is capped
at a sol (:4000-4006; `Lua/_GameConst.lua:143`), not the outside oxygen budget.

**Player route:** the same ordinary hub/passage interruption as S1. Rescue may be
booked at an intermediate position, traversal finishes safely, then the colonist
walks back toward the old pickup. The watched colonist with access true and a task
already present is precisely why a new HasLocalAccess predicate alone cannot clean
up all existing tasks. No claim that GetPassablePointNearby always chooses ground,
or that a Goto always chooses a dome door, follows from Lua.

**Preferred repair direction:** revalidate an uncommitted, own-home rescue at the
start of Transport and suppress an obsolete pickup when the colonist is physically
safe at home. A guarded command bypass with native task cleanup and tail delegation
elsewhere avoids copying the animation/wait body (layer 2); it is not an always-call
§1.4 chain. Preserve committed-shuttle cleanup, real relocation, multi-leg tasks,
expedition destinations and actual remote rescues. A task-creation wrapper can
correct/reject an unsafe source synchronously, but a safe position at booking does
not resolve later obsolescence. Returning nil for every hub rescue can instead
strand units after disconnection. A global wait reduction only shortens exposure
and can abort legitimate busy-hub service; it is not the first repair.

**Stop/sitting — pickup anchor and obsolete rescue:** record task creation position,
`source_landing_site[1]`, selected passable pickup, traversal completion, physical
home entry, first Transport step, actual exit path, shuttle commitment and oxygen
timeline for the dying route. Include a remote unit that still needs rescue and a
committed shuttle already approaching. A pickup that remains necessary/safe, or an
ordinary ride that already clears hub holder before departure, falsifies the
corresponding stronger theory. The owner-witnessed death does not require inventing
the missing anchor measurement.

## S3–S12 — independent verdicts, routes and controls

| Suspect | Verdict and source | Ordinary player route, repair shape, and stopping measurement |
|---|---|---|
| **S3 stale hub marker** | **SOURCE-VERIFIED lifetime defect**, lasting harm conditional. Marker set at `Passage.lua:1228`, cleared at :1235 on dome-side traversal; `Unit.lua:468-470`, `Colonist.lua:2963-2966` and `BuildingWayPoints.lua:541-547` trust validity rather than position. ON:661,663 still show a marker after a watched unit reaches work. This is not proof those workplaces are physically off every hub. | Interrupt a crossing, then walk/work elsewhere without another dome-side passage exit. Scope marker cleanup to verified departure from the physical passage/hub; invoke native outside recomputation. A synchronous lifecycle hook is preferable to a permanent polling thread; a conservative load cleanup is separate. Never clear on every ExitHolder: the native comment protects a real dump onto the hub. **Stop:** footprint/height plus marker and timer readings on departure, dome entry, work, death and reload; clearing shelter on a real ramp falsifies the fix. |
| **S4 holder carried off hub** | **HYPOTHESIS**, not refuted by turnover, not established by radius. The proposed normal-shuttle retention chain is **refuted by source**: `Colonist.lua:3973-3978` requires ExitHolder before pickup; `Unit.lua:473-477` and `BuildingWayPoints.lua:541-546` clear it. Reading ShuttleHub's attach/drop code in isolation misses that prerequisite. | Ordinary Roam/work movement after a hub crossing remains the candidate. **No repair yet. Stop:** follow one held unit beyond the actual walkable footprint/height, then through ExitHolder, pickup and drop. If established, repair the missed departure with SetHolder and UpdateOutside, not bulk deletion of hub.units. Collision-radius pruning is unsafe. |
| **S5 disconnect destroys arrival metadata during traversal** | **SOURCE-VERIFIED conditional race.** A live sibling bypasses the last-exit wait (`Passage.lua:1134-1138`); disconnect at :1181 removes tunnel metadata (:1404,1742-1750,710); the remaining traverser reads `element.is_pf_tunnel` only at :1224 and can take the non-hub branch. **Corrected:** elements are not deleted immediately; :1182-1184 waits before `Demolishable.lua:132-140` calls DoneObject. Later stale-element kicks are a separate consequence to measure. | Salvage one busy spoke while another exit remains. Prefer preserving the arriving traverser's endpoint independently of mutable tunnel-registration state, or moving the traversal drain ahead of disconnect while preventing fresh admission. Do not restore a removed PF tunnel merely to preserve metadata. A simple OnDemolish wait-wrapper can admit fresh traffic forever and adds a blocking frame; it needs cancellation/save analysis. **Stop:** salvage during natural crossing; log pre/post-disconnect endpoint, final holder/marker/outside timer, element membership and later removal. |
| **S6 / C42 stale passage-element units** | **SOURCE-VERIFIED bookkeeping defect**, field harm unproven. LeadIn sets the element holder (`BuildingWayPoints.lua:489-497,531-535`); ordinary holder writes maintain membership (`Unit.lua:805-825`), but `Passage.lua:1231-1235` uses raw nil when no valid hub marker exists. `Holder.lua:6-25` later kicks listed units. Clean **hub** lists do not test **element** lists. | Complete direct dome-to-dome passage travel, then salvage it. Correct the raw exit assignment through SetHolder. A narrow synchronous holder-list filter before Done can mitigate stale kicks but does not fix creation; copying the blocking TraverseTunnel body solely for this is expensive. **Stop:** inspect terminal-element members against their current holders before removal and observe any displaced colonist after it. |
| **S7 / C99 last-exit salvage never finishes** | Last-exit predicate **SOURCE-VERIFIED**; permanent failure **HYPOTHESIS**. `Passage.lua:1131-1152` allows a remaining active sibling and otherwise protects traversers, hub holders, draining siblings and nearby markers; :1175-1177 waits. The audit's correction rejecting a mutual-sibling deadlock holds. The field sitting measured turnover and finite rescues, not a permanently blocked demolition. | Salvage all spokes while units still need the last exit. That ordinary wait is intentional. Repair proven stale marker/list state through S3/S6/S9 as applicable; do not delete the safety predicate or exclude live waiters merely for waiting a long time. **Stop:** sample the exact true clause and named units through rescue/death cleanup and cancellation/reload. Engine MapHasAny visibility of detached units needs a positive/negative paired measurement; source does not settle it. |
| **S8 ignored intermediate hop failure** | Ignored returns **SOURCE-VERIFIED** at `Colonist.lua:2204-2209,3844-3848`; harmful hub route **HYPOTHESIS**. MigrateStep checks the final entry (:2210-2211). A failed intermediate return alone does not prove a later failed dome entry or increment; see :1416-1423 and `Unit.lua:371-376`. No entry-failure example in this sitting. | Break/change a passage during a genuine multi-hop migration. If reproduced, stop/replan at the failed hop and release/retain reservations appropriately. A narrow command-specific entry seam needs caller proof; do not globally alter every EnterBuilding result. Full copies of both blocking callers are a last resort. **Stop:** record each hop result and position, final entry and failure-counter delta; reaching safety normally falsifies the claimed harm for that route. |
| **S9 traversal destructor throws and leaves a stale list** | **HYPOTHESIS.** List insertion/removal surrounds the walk (`Passage.lua:1205-1239`), whose destructor is called under sprocall (`CommandObject.lua:441-455`). A throw before cleanup could retain it, but neither a throw nor the proposed natural trigger was measured. Unit deletion alone does not prove a throw; command teardown also runs destructors. | Death/deletion during crossing is a candidate, not a demonstrated ordinary route. If justified, prune demonstrably invalid members synchronously before both waits; a valid stale member needs stronger evidence than timeout. **Stop:** controlled death/deletion records the error, object validity, command and list before/after; no error and clean removal falsify that trigger. No build from the possibility of an exception alone. |
| **S10 hub shelter disagrees with IsInSafeAtmosphere** | Predicate mismatch **SOURCE-VERIFIED**: on a non-breathable map `ColonistTransport.lua:836-842` accepts a life-supported Community, not a PassageHub; :909-914 may seek station shelter while Unit's marker logic suppresses outside effects. Independent harm **HYPOTHESIS**, partly downstream of S1. | Lose shuttle/train access while a hub colonist cannot pass native local access. Stranded may leave nominal shelter or apply its status unnecessarily. After S1/S3, consider a synchronous result-widening shelter predicate only for verified physical safe occupancy; never bless a stale marker globally. **Stop:** no-shuttle hub sitting follows the complete recovery ordering, actual station route and damage; ordinary safe return can make this branch vacuous. |
| **S11 dome demolished with sole passage to isolated hub** | **HYPOTHESIS**, with a plausible existing blocker. `Dome.lua:1791-1793` also requires empty Building/Colonist labels and Building.CanDemolish, not merely `connected_domes <= 1`. PassageGridElement inherits Building (`Passage.lua:448-450`); placement plus Building.GameInit/SetDome can add endpoints to the dome's Building label (`Buildings/Building.lua:496-504,701-724`). | Try salvaging an otherwise empty dome whose only passage ends at a hub with no other dome. **Stop before repair:** inspect endpoint parent_dome, label membership and every CanDemolish operand. If vanilla rejects it, drop this route. Only a real acceptance justifies a synchronous additional connected_passages guard; border membership remains unmeasured. |
| **S12 home shuttle drop outside local-access band** | **HYPOTHESIS; audit overstates FindDropPos.** `Buildings/ShuttleHub.lua:647-652` can return a passable/buildable initial point without a dome exclusion; later branches (:658-678) exclude dome hexes. A drop exactly twenty hexes away passes the <= comparison (`ColonistTransport.lua:27,299`). Neither a Geoscape radius nor the helper proves access failure. | A normal rescue to a large dome with a displaced/obstructed pad is plausible. **Stop:** measure requested pad, actual drop hex, holder, nearest/home community checks and immediate command. Need distance beyond the band **and** final access false, not merely an outside landing. A safe drop-point adjustment or post-drop recovery seam would be narrower than changing global work range, if a natural rebooking loop is observed. |

## Ranked follow-up shapes

This ranks proposed repairs, not entry statuses. Each game-dependent item stops at
its named sitting above; this report does not authorise substituting an engine guess.

| Priority | Action | Main control / rejected shortcut |
|---|---|---|
| 1 | S1 synchronous access fallback, after establishing a sound physical-origin discriminator | Natural interrupt must end safely; false marker/holder, cut network, outdoor work and train controls must retain native behavior. Do not increase global range or globally widen GetClusterDomes. |
| 2 | S2 obsolete-rescue revalidation at Transport start; safe source selection where needed | Old pickup after reaching home vs necessary remote rescue; committed shuttle and multi-leg controls. No blanket task cancellation or one-sol timeout tuning. |
| 3 | S5 preserve in-flight destination across disconnect | Busy spoke with sibling vs last exit; cancellation, new arrivals, save/reload and final holder/list consistency. Do not conflate tunnel removal with element destruction. |
| 4 | S3 marker lifetime repair, coordinated with S1 | Actual ramp remains sheltered; departed unit loses stale protection. A physical discriminator is shared evidence, not yet an implemented helper. |
| 5 | S6 native holder bookkeeping / C42 | Direct passage terminal elements, genuine occupants, demolition and save/reload. No hub-wide prune based on collision radius. |
| Separate, still justified | P3 pins and P2 arrival reservation mismatch | Original source-specific controls remain; neither explains nor cures this death chain. |
| After safety | C111 rescue wording | Own-home rescue should read as returning/rescue; real relocation still names its destination. Preserve destination selection/link, localisation and reload behavior. Prefer command-text/getter work over movement hooks. |
| Diagnostic only | S4, S7, S8, S9, S10, S11, S12; original C109/P1/P5/P6 gaps | Their individual physical, lifetime or ordinary-route falsifiers above. No generic hub cleanup or planner rewrite. |

S5's least invasive *complete* shape is not yet settled. Capturing endpoint state
outside a blocking traversal and reconciling it afterwards risks a persisted mod
frame or per-unit state; a copied traversal must also preserve error cleanup.
Changing disconnect sequencing must stop new admissions without disabling the
last real escape. That choice belongs in its build design, with §3a disposition;
this source verdict does not endorse an unanalysed blocking wrapper.

## Causation

**The evidenced access/rescue failure is vanilla, with Passage Network an exposure
modifier, not a necessary trigger.** Native hub traversal, centre-based access,
false-source pickup capture, rescue waiting and misleading own-home Transport text
supply the chain, and the rescue symptom persists with Passage Network absent.
Its archived code overrides cluster membership and service distribution, not those
mechanisms; the sampled connection tables refute the proposed persistent-link
residue. Its wider work/service reach plausibly creates more crossings, while its
wider cluster can make some native access checks pass more often. The source defects
identified in the hub audit likewise belong to vanilla, but the remaining hypotheses
are not thereby proven defects. Thus the owner's working causation answer holds for
the identified symptoms/mechanisms, with two limits: these logs are not a pack-off
control, and they do not establish that every hypothetical migration failure is
mod-independent. The earlier conditional P6 pack interaction and unisolated unused-
passage symptom remain separate, not counterevidence attributing these rescues to
Passage Network.

## Verification record and reproducibility

Started with `git log --oneline -8`, `git pull`, `git status --short`: clean at
`536db7d`, pull up to date. Rechecked after the concurrent `2eadd83` handoff;
`git diff --name-only c8a4aef -- Code` printed no changed code paths.
Used numbered UTF-8 reads from the archived source and scoped decoded-tree
`rg -n` searches for HasLocalAccess, its helpers, GetClusterDomes, holder changes,
passage endpoints, ReassignServices and its capacity helper. Two read-only review
seats covered lifecycle/demolition; their load-bearing claims were cleared against
the actual ExitHolder/OnExitUnit, FindDropPos, OnDemolish/RemovePFTunnel/traversal,
CanDemolish and intermediate-entry bodies.

Read files were SHA-256 checked against the build's `MANIFEST.sha256`: Colonist,
ColonistTransport, Unit, Passage, PassageHub, LRTransport, Stats, Dome,
BuildingWayPoints, Workforce, Station, ShuttleHub, Demolishable and CommandObject.
All matched. `tools.luafn.find_bodies` extracted the named access, task-creation,
SetCommand, traversal and Transport bodies in both archives. Direct normalized
body equality cleared the unchanged expressions; the Transport diff was read,
not interpreted as a whole-body match.

The following read-only Python reconciliation was run via a PowerShell here-string
to `python -` on 2026-09-24. It counts only plain SMR-tagged records, avoiding
duplicated SMRTK echo lines. Emitted SMRCOL rows are the sample population, not
the entire census; the field report provides its independent sample totals.

```python
from pathlib import Path
from collections import Counter
import re
for p in sorted(Path('docs/archive/logs').glob('reporter_TheGodUncle_*.log')):
    lines = p.read_text(encoding='utf-8-sig').splitlines()
    rows = [s for s in lines if s.startswith('SMRCOL ')]
    commands = Counter(re.search(r' cmd (\S+)', s)[1] for s in rows)
    assert len(rows) == sum(commands.values())
    assert all(' fails 0 ' in s for s in rows)
    rides = [s.split()[1] for s in rows if ' cmd Transport ' in s
             and 'home Brussels#1896' in s and 'task Brussels#1896' in s]
    assert len(rides) == commands['Transport']
    print(p.name, len(rows), commands, 'home rescue handles', rides)
    census = []
    for s in lines:
        if s.startswith('SMRPOP ') and ' residents ' in s:
            census.append((s[7:s.index(' residents ')],
                           int(re.search(r' residents (\d+)', s)[1])))
        elif s.startswith('SMRPOP total '):
            assert sum(n for _, n in census) == int(s.split()[-1])
            print('census', census, s)
            census = []
    edges = [s for s in lines if s.startswith('SMRNET ') and ' -> ' in s]
    summaries = [s for s in lines if s.startswith('SMRNET ') and ' neighbours ' in s]
    assert edges and summaries
    assert all(re.search(r'count (\d+) real \1 ok$', s) for s in edges)
    assert len(edges) == sum(int(re.search(r' neighbours (\d+)', s)[1])
                             for s in summaries)
    sets = [s.split() for s in lines if s.startswith('SMRHUBSET ')]
    if sets:
        a, b = [dict(v.split(':') for v in row[3:]) for row in sets]
        assert len(a) == int(sets[0][2]) and len(b) == int(sets[1][2])
        print('common', [(h, a[h], b[h]) for h in sorted(a.keys() & b.keys())])
```

Results: OFF sample 264 = Rest 84 + VisitService 31 + BoardVehicle 47 +
WaitForTransport 41 + Transport 10 + GoToDome 8 + WorkCycle 15 + Work 21 +
GoToStation 7. ON sample 163 = Roam 10 + Rest 23 + VisitService 58 + Transport 12 +
WorkCycle 14 + Idle 26 + Work 18 + GoToDome 2. Transport members all name Brussels
as both home and task destination; these totals agree with the field report's
run table. Census totals reconcile to the named rows above and each log's SMRPOP
total line. Each connection census has 30 directed edge records, reconciling to
the neighbour summaries; no emitted edge disagrees with its real-link count.
The hub sets reconcile their enumerated members to 66 and 70, with exactly the
four named common handles above; their timestamps differ by 502505 game-time units.
The SMRHUBU and SMRHUBOFF figures are aggregate instrument readings: the archived
log does not enumerate their individual distance/holder members, so this resweep
does not claim an independent per-unit remeasurement of those aggregates.

No game launched, save opened, probe added, source archive modified, entry filed,
or status changed. Missing engine readings remain explicitly stopped above.
`python tools/doccheck.py` returned GREEN, and the exact embedded reconciliation
script completed without an assertion failure. The commit is scoped to this report.
