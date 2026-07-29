# Project Status — read this first in a new session

Updated: **2026-07-28 LATE (post-D07-build): D07 `Opt_CohortHousing` BUILT
(user-authorized unattended leg) with a FRESH A/B pair — 73 probes, baseline
1/57/15/0 · all-six-toggles 63/0/10/0 (71/71) — plus PT-23 → F46 and PT-09 →
F14 flips (twelve flips total on the day). See the "D07 build leg" section
directly below.** Prior wrap: **2026-07-28 session wrap — the PT-52 live sitting (D03 tested,
F71 tested, PT-52 telemetry healthy, F68 over-draw caught) + the same-day
game-free F68 repair leg with a FRESH A/B pair (baseline 1/57/14/0 ·
all-five-toggles 62/0/10/0, 70/70 — no pre-flight queued for the next
session). See the two 2026-07-28 leg sections below and the header
additions.** Prior wrap follows: 2026-07-27 night (**D05 SHIPPED AND TESTED same
night — optional modules enable in-game via Options → Mod Options, live both
directions, restart-persistent (PT-51 archived); PT-50 PASS in full → D04
tested; PT-49 core passing + row reposition verified; ListFixes crash found
by play and repaired; F76 surface widened to the dozer path; the drone
task-assignment investigate item is fully stocked and has its own kickoff
prompt.** 72 probes; last legs clean: baseline 1/57/14/0 · fixed 58/0/14/0
(64/68) · opt-in 61/0/11/0 (67/68); **an A/B re-verify is QUEUED as the next
session's pre-flight** (two mechanical repairs landed after the last pair —
expected numbers unchanged). See "Mod Options build leg" below; the earlier
same-day build leg and the playtest-marathon record follow). **2026-07-28:
the drone task-assignment static investigation leg is DONE (section below),
and the user-greenlit D06 overhaul core + F77 fix are BUILT the same day —
see the build-leg section directly below. PT-52 (attended, multi-iteration)
is the next sitting's centerpiece.** **2026-07-28 PT-52 sitting (live):
PT-49 COMPLETED in full → D03 `tested` (archived) — arrivals + tourists
proven against an adversarial pad-beside-the-closed-dome setup, an
unexpected child resident forensically cleared as in-dome birth, MicroG row
verified on an asteroid habitat and KEPT there by user decision (two real
auto-move-in paths exist: inter-habitat resettlement and stranded
re-homing).** **Same sitting, lander leg: PT-17 ratchet PASS (request pinned
at the hold across 4 automated cycles, no unload flip) and PT-32 PASS in
full → F71 `tested` (archived) — live two-resource priority inversion,
valuables first, nothing dropped. Capacity-edge leg: no wedge, BUT a NEW
FINDING on the F68 fix — request over-draws below the GET-WHEN-ABOVE
threshold under active mining (asteroid drained to 84 vs threshold 144);
root cause + repair sketch on the F68 entry (the fix double-implements the
anti-churn floor; delete the aboard-into-ground half). **BOTH queued repairs
LANDED the same evening (F68 over-draw + TestKit logger — see the repair-leg
section) with a fresh A/B pair; the build queue is EMPTY again.** PT-17
stays un-archived pending an attended capacity-edge re-run — **DONE 2026-07-28
next sitting: re-run PASS (ground settled AT the threshold, request tracked
instead of ratcheting) → F68 `tested`, PT-17 archived; PT-19 PASS same
sitting → F73 `tested`, archived (residence held through both gap shapes);
PT-33 PASS same sitting → F72 `tested`, archived (all three cases incl.
both not-over-broad negatives); PT-40 PASS same sitting → F65 `tested`,
archived (merge both geometries, clean salvage split, long-track control,
reload, log clean); PT-31 PASS same sitting → F70 `tested`, archived
(round trip held, prefill negative intact); PT-16 PASS same sitting →
F67 + F69 `tested`, archived — **the ASTEROID SECTION is COMPLETE.** PT-43
PASS in full same sitting → F19 + F20 + F21 `tested`, archived — **TEN
status flips in one sitting (F68, F73, F72, F65, F70, F67, F69, F19, F20,
F21), plus two NEW vanilla findings from the PT-43 setup (F79 trains-never-
serve-services, confirmed; F80 trains-skip-waiting-passengers,
investigating).**
Also proven this
sitting: the class-flattening runtime corollary (Key technical facts).**

## D07 build leg + two more flips — Fable, 2026-07-28 late (mixed live/game-free)

Same calendar day as the ten-flip sitting; a short live leg (user at keyboard)
followed by a user-authorized unattended build leg while they were away.

- **PT-23 PASS → F46 `tested` (archived), eleventh flip.** Both halves on the
  live 5-station network: forbidden Metals drained to 0/60 and STAYED; the
  all-five-stations-forbidden + drones-off leg proved trains dump rather than
  strand (zero loaded roamers). Isolated no-drone stations keeping stock =
  expected statics, recorded as an observation on the entry.
- **PT-09 PASS → F14 `tested` (archived), twelfth flip.** Red low-stat cell
  verified per-CELL both directions (red at Comfort 0, white on recovery).
  Two researched facts recorded: the peril statuses share a 12-36h
  per-colonist GRACE window before Health damage (StatusEffects.lua:93-98,
  then avg ~2x base rate, stacking); the fifth overview column is
  SATISFACTION (tourist-rating stat, ChangeSatisfaction zeroes gains past
  the tourist sol window) — its red 0 on every mature dome is CORRECT
  vanilla-intended rendering the F14 bug had been hiding.
- **D07 `Opt_CohortHousing` BUILT (user gave config + go the same evening:
  in-dome-first + cross-dome, Seniors+Children one toggle, then "start
  working on it" for the unattended window).** Colonist/housing-level rule,
  zero persisted state, all hooks per-call-gated: UpdateResidence post-wrap
  (in-dome move), FindEmigrationDome post-wrap (nearest-reachable cohort
  slot, tie rule bypassed; quarantine/D03/forced-dome/overpopulation
  respected), ColonistBecameYouth nudge. Mod Options toggle #6. Full notes
  on the D07 entry; PT-53 written into the checklist (5 triggers).
- **A/B pair FRESH (2026-07-28 late, 73 probes):** baseline **1/57/15/0** ·
  all-SIX-toggles **63/0/10/0 (71/71 applied)**, zero errors, both legs on
  predicted numbers. NO pre-flight owed. Two probe-side lessons from the
  leg (module itself never wrong): (a) **WithGlobals stubs cannot reach a
  game file that localizes the global at load time** — Colonist.lua:5 does
  `local IsValid = IsValid`, so stand-in probes must assert on the MODULE's
  action (absence/presence of its move), not on vanilla bookkeeping around
  plain-table stand-ins; (b) a fake colonist driven through the shipped
  FindEmigrationDome tail needs a PickEmigrationCommunity stub.
- Housekeeping: D07 config decision recorded on the entry when given
  (commit 6ca11a1); prompt un-run list updated (PT-09/PT-23 gone, PT-53
  added); Satisfaction/grace observations archived with their PTs.

## TEN-FLIP playtest sitting — Fable, 2026-07-28 evening (live, the project's most productive sitting)

One long attended session; full per-test evidence in `PLAYTEST_ARCHIVE.md`,
forensic trails on the entries. Zero pack code changed (no A/B owed).

- **Ten `tested` flips:** F68 (PT-17 capacity-edge re-run — ground settled AT
  the threshold), F73 (PT-19, both life-support gap shapes), F72 (PT-33, all
  three cases), F65 (PT-40 full procedure), F70 (PT-31 round trip), F67+F69
  (PT-16 — full-sol asteroid hold logged; manual-landing fuel ration kept and
  flown home), F19+F20+F21 (PT-43 in full). **The ASTEROID SECTION is
  COMPLETE.**
- **Validated live:** the map-switch console-death repair (workaround
  retired), the repaired AutoCargo logger (first live capture drove the F68
  re-run), the repaired CargoReady logger (leaf-class + change-only, repaired
  mid-session in a game-free break, first verdicts drove the F67 read).
- **F78:** hypothesis 1 (descriptor-validate infinite loop) REFUTED live
  (`table.validate` removes plain tables — `kept: 0`); on VeryLow the strike
  routine is statically seconds-bounded, so the 183h stall contradicts static
  analysis → on-demand repro plan banked on the entry (bracket taps +
  `CheatMeteors("single")` at empty ground).
- **NEW F79 (confirmed):** colonists never use trains for services —
  `Dome:GetService` is passage-only while the train-aware reachability serves
  only Workplace/Training/Residence. Fix = feature-completion, D-item, USER
  DECISION pending. **NEW F80 (investigating):** trains stopped 4+ times and
  skipped ~19 valid waiting passengers (full config-exonerating forensics on
  the entry; direction-blind-spot suspicion; mitigated by adding trains 2→5).
- **NEW D07 speced (user-commissioned, revised same day):
  `Opt_CohortHousing`** — colonist/housing-level rule, NO dome designation:
  cohort members in normal housing move to free Retirement Home/Nursery
  slots anywhere (in-dome reassignment first, cross-dome emigration
  second), completely untouched when no cohort slot exists; employed
  seniors exempt; graduation drains naturally; zero persisted state. Build
  awaits user go.
- **PT-52 sitting 2: healthy.** Readings `vetoed 1→9 / veto_expired 0→1 /
  moonlighted 0`, `unclaimed=0` on all seven hubs throughout (new hub 4230
  integrated); counters correctly survived a save reload and correctly reset
  on the mid-session relaunch. **Trigger B still un-run.** Log hygiene: the
  full session log swept — ZERO Lua/mod errors.
- New engine facts recorded on entries: `CheckAutoDepart` consults only the
  CURRENT side's rule set (empty side-set = designed collect-trip);
  `RoughTouchDown` storybit can strand a lander on a bare asteroid
  (`maintenance_request:SetAmount(0)` is the verified recovery);
  `Colonist:ChangeComfort(amount, reason)` is the clean stat-injection path;
  trains carry workers/trainees/migrants only (F79); the trip planner books
  tickets with no regard for actual train service.

## F68 over-draw repair leg — Fable, 2026-07-28 (game-free, post-playtest): same-day mechanical repair + fresh A/B pair

The PT-52 sitting's lander leg (PT-17 capacity edge) caught the pack's own
F68 fix over-exporting below the player's GET-WHEN-ABOVE threshold; the
repair landed the same evening once the user closed the game.

- **Root cause, live-proven before touching code:** the TAP2 console-tap
  arithmetic matched `ground + 2×aboard − threshold` EXACTLY at every
  recompute (52/72/98 at aboard 12/32/58; final ground 184−100=84) —
  **`GetTotalCargoAvailable` already counts a landed rocket's own hold**, so
  the v1 fix's aboard-into-ground addition double-counted every unit aboard
  and the request ratcheted monotonically to the hold cap. New engine fact,
  recorded here.
- **Repair (`Code/Fix_LanderCargoRatchet.lua`):** the addition
  (old :145-151) DELETED; the explicit request-floor block (never ask below
  aboard) now carries the whole F68 anti-churn fix. Header comment documents
  the discovery + repair. Parse clean.
- **TestKit AutoCargo logger repaired in the same leg** (local commit): two
  live-proven flaws — wraps the leaf class `UniversalLanderRocket` now (the
  flattening corollary made the old base-class runtime wrap structurally
  blind to real landers), and reads `self.cargo[res].requested` post-call
  (the return value it used to print is always nil).
- **A/B pair, fresh (also clears the queued pre-flight):** baseline
  1/57/14/0 · all-five-toggles 62/0/10/0 (**70/70 applied**, user's Mod
  Options toggles all on, zero pack errors, noise = the known synthetic-map
  set). The LanderCargoRatchet probe passes through the floor path
  (`request 300000 >= 300000 aboard`) — the probe needed no change, by
  design of the repair.
- **Validation debt: CLEARED 2026-07-28 (next sitting).** The attended
  capacity-edge re-run PASSed on the live colony: Concrete above 0 + Rare
  Metals above 140 with extractors replenishing mid-load; request tracked
  `aboard + surplus` (PreciousMetals 90000→92000, creeping only by the mined
  amount) instead of ratcheting; ground after departure 146 with miners
  running = settled AT the threshold. The repaired TestKit AutoCargo logger
  did the capture — its first live validation. **F68 → `tested`; PT-17
  archived.**

## D06 build leg — Fable, 2026-07-28: drone dispatch overhaul core v1 + F77 fix (user-greenlit, PT-52 pending)

Built same-day on the investigation verdict and the user's design review
(their proximity-cascade idea became option H in the study; the shipped claim
gate is its veto variant — reversible and orphan-proof, chosen for v1).

- **`Code/Opt_DroneOverhaul.lua`** (opt-in, off by default, Mod Options
  toggle "Drone dispatch overhaul (experimental)"; hooks installed at
  classdef time, gated per call on IsActive; NO persisted state):
  1. closest-fleet-first claim gate — chained wrapper on
     `TaskRequestHub:FindTask` (sole caller = drone auto-Idle, so player
     orders untouched): repair/clean work offered to a non-closest covering
     hub is withheld while the closest hub has idle drones; per-request
     strike cap (4 polls / 30s decay) makes starvation impossible;
  2. repair moonlighting — chained POST-wrapper on `Drone:Idle` (the body
     falls through exactly when workless — verified engine fact): workless
     drones take unclaimed repair/clean work of SATURATED neighbor hubs
     within 30 hexes and their own restrict area, vanilla-style SetCommand;
  3. `SMRFixPack.DroneReport()` telemetry (always on, read-only): per-hub
     state + module counters vetoed/veto_expired/moonlighted.
- **`Code/Fix_ExtenderFlapChurn.lua`** (F77, default-on fix): extender
  working-flaps now debounce+coalesce the whole-hub rebuild (2s, per root
  hub, chains resolved) instead of tearing it down twice per blip.
- Wire-up: items.lua toggle + metadata `default_options.DroneOverhaul` +
  code list. Parse sweep: all 4 touched files pass (python luaparser).
- Scope guards worth knowing when judging PT-52: rockets/rovers/construction/
  hauling all exempted by design; the claim gate cannot veto player orders
  structurally (FindTask is not on that path); toggling off restores vanilla
  instantly (registration layer untouched).
- Docs (full pass, same day): D06 entry + index row (BUGS), F77 flipped to
  `fixed` (row + tag), options doc carries the build note. **PT-52 is a full
  checklist procedure now** (PLAYTEST_CHECKLIST, optional-modules group):
  CAN/CANNOT-do lists, Trigger A passive watch, Trigger B controlled off/on
  A/B demo, Trigger C regression watch, result lines, knob log line.
  MOD_DESCRIPTION got the player-facing F77 bullet (Buildings & economy) and
  the "Drone dispatch overhaul — experimental" module block.
  FABLE_NEXT_PROMPT rewritten post-build (PT-52 centerpiece + assistant
  briefing notes, 65/70 module counts, D06 read-list pointers);
  DRONE_INVESTIGATION_PROMPT retired/deleted. `DroneReport` upgraded to
  print ON-SCREEN (ConsolePrint) AND to the log — the ListFixes lesson,
  applied before it bit.
- The user expects multiple iterations across sittings; knob changes get
  recorded on the D06 entry (mechanical, assistant may land same-day);
  design-level changes (H-v2, registration-H, balancer C) stay user
  decisions per the options doc.
- Testing debt, stated: no TestKit probes for the module yet (attended
  playtest is the v1 validation instrument; probes come with the iteration
  that stabilizes the design).

## Drone task-assignment investigation leg — Fable, 2026-07-28 (game-free, docs-only): verdict in

The `DRONE_INVESTIGATION_PROMPT.md` kickoff, executed as specced (no game, no
loadable-code edits, Src read-only). Full verdict + trace + instrumentation
plan live on the BUGS "Not yet swept" DroneControl bullet; **F77** filed
(index row + entry). Headlines:

- **Architecture verdict: working-as-coded, but with NO cross-hub locality
  anywhere.** Assignment is PULL and own-hub-only — `Drone:Idle`
  (`Drone.lua:564-641`) polls `command_center:FindTask(self)` (`:621`), the
  single FindTask call site in Src; the match itself is the C-side
  `Request_FindTask` over the hub's own queues (ordering/distance policy
  engine-internal — recorded as unverifiable from Lua). A building in overlap
  registers with EVERY covering hub and its (shared, C-side) request objects
  sit in every such hub's queues; the claim is first-poller-wins at command
  start and **held through the whole approach** (`Drone:Work`,
  `Drone.lua:898-924`); maintenance repair requests are **max_units = 1**
  (`RequiresMaintenance.lua:82`), so one far drone locks out a fleet parked
  next to the job. No handoff, stealing, or rebalancing exists anywhere.
- **Extender transparency CONFIRMED** (the user's hypothesis): both connect
  directions register the far HUB itself on the building
  (`DroneHubExtender.lua:156-160` building-side recursion;
  `DroneControl.lua:315-325` hub-side recursion) — extender-mediated coverage
  is indistinguishable from native in every match structure. Extenders do NOT
  extend drone movement: `const.DroneRestrictRadius` (100 hexes-worth) is
  anchored on the HUB position (`Drone.lua:227-230`, `_GameConst.lua:71`);
  post-SignalBoosters a 2-extender chain can register buildings a hub's
  drones can never legally reach (suspected F55-feeder, engine-side check —
  flagged for live).
- **NEW F77 (defect, provable):** every extender working transition (power
  blip, malfunction, repair, toggle — both edges) triggers a FULL
  disconnect+reconnect of the entire uplink hub's requester set
  (`DroneHubExtender.lua:171-178` → `DroneControl.lua:441-450`), Idle-kicking
  every drone en route to any connected building (`:720-729`) and burning
  O(B×D) + queue-rebuild work per flap. Reproduces both observed halves on
  its own. Fix sketch: debounce wrapper (user decision).
- **The live starvation stays two-hypothesis** until one attended sitting:
  (a) registration gap (starving buildings outside hub 2608's circle, inside
  the far hub's extender-stretched coverage — pure design) vs (b) claim
  lockout (in both queues, far fleet wins the claim race every chunk). The
  banked `target:0` read is consistent with both. **R1-R7 console reads** (on
  the bullet; sandbox-verified, incl. a `RequestAssignUnit` claim tap — no
  file-local alias in Drone.lua, so a console global wrapper is seen) settle
  it; R7 is the hub-A/hub-B/extender repro with `CheatMalfunction`.
- **Performance answer (the user's second observation):** per-idle-drone
  FindTask polls scan the hub's full queue set every ~3s and overlap
  multiplies queue content (k-hub overlap ≈ k× colony-wide scan work); the 1s
  empty-queue throttle can't engage while any drone holds unreachable-cache
  entries (`Drone.lua:630`); reconnect storms (radius change, F77 flaps, and
  `OnMsg.DepositsSpawned` reconnecting EVERY hub at once,
  `DroneHub.lua:188-199`) are O(B×D)-grade each. Range × drones × requests,
  exactly as reported.
- **Nothing was built** (per spec). Build decisions for the user: F77
  debounce (plain repair), and the locality levers — cross-hub idle-pull
  pre-wrap on `Drone:Idle` for (a) vs near-idle claim veto on
  `Drone:Work`/`PickUp` for (b) — which are assignment-POLICY changes
  (D-item territory). All sketches + risk statements on the bullet/F77 entry.
- **Follow-up same leg (user-commissioned): `docs/DRONE_OVERHAUL_OPTIONS.md`**
  — the D06-candidate feasibility study for an optional overhaul toggle.
  Options A-G with verified patch points; key new engine findings:
  `Drone:Idle` falls through (returns) exactly when no work was found, so a
  chained POST-wrapper is a legal dispatch hook (the F73 pre-wrap-only rule
  is for command bodies that always SetCommand); `Drone:Work`/
  `ApproachWrapper` never consult `command_center` (cross-hub execution is
  clean); `Drone:SetCommandCenterUser` (`Drone.lua:2687-2694`) is the
  vanilla migration path. Recommended order: telemetry → repair
  moonlighting → migration balancer; claim-veto/handoff gated on the R1/R3
  live answer. USER DECISION before any build.

## Mod Options build leg (D05) — Fable, 2026-07-27 late: in-game enable surface for the optional modules

Triggered live: the user sat down for Group 8 and had **no main-menu console**
— and the briefed console route was falsified outright (the Opt_ gates run at
mod code load during startup, BEFORE the main menu; that is why the A/B
harness always needed the `97_OptInLeg.lua` flag FILE). Release context made
it a blocker: Steam Workshop + Paradox Mods, and **Paradox delivers PS/Xbox,
which have no console at all**. User picked "build now" over "temp file for
tonight". Full spec + Src evidence on the **D05** BUGS entry; summary:

- **items.lua (new):** four `ModItemOptionToggle`s (names == registry ids) put
  the pack on **Options → Mod Options** (main menu and pause menu, gamepad
  capable). **metadata.lua** gains the matching `default_options` table (what
  `HasOptions()` reads — without it the page ignores the pack).
- **00_Core:** `SMRFixPack.OptionEnabled(id)` (pre-load `SMRFixPack_Optional`
  OR the saved toggle — the values load before mod code, `CurrentModOptions`),
  `SMRFixPack.IsActive(id)`, defs retained, and an `OnMsg.ApplyModOptions`
  reconciler: ON = re-arm installed hooks or apply now (+`on_activate`); OFF =
  registry status flip (+`on_deactivate`). **Every optional module's wrappers
  consult IsActive per call**, so toggles are live in both directions with no
  unhooking. D04 flips the `build_once` template flag in its callbacks
  (restore guarded so a third-party limit mod is never stomped).
- **D04 cosmetic repair (pre-existing, exposed by the leg):** the transient
  pre-DataLoaded "ArtificialSun not found" detail no longer sticks on
  `ListFixes`; miss only recorded post-DataLoaded, cleared when the template
  appears. Engine fact: **DataLoaded fires more than once during startup; a
  template can miss the first pass.**
- **TestKit:** new probe `OptionsMenu` (60_Probes_Opt.lua) asserts the wiring
  in EVERY leg — metadata defaults, the four toggle items, the 00_Core bridge
  — and FAILs discriminatingly in baseline (registry absent). **72 probes.**
- **Legs (2026-07-27, logs Mars.exe-20260727-…):** parse sweep 82 files/0
  failures; baseline 21.20.32 = 1/**57**/14/0; fixed 21.21.51 = **58/0/14/0**
  (64/68); opt-in 21.34.28 = **61/0/11/0** (67/68) — all module probes +
  OptionsMenu PASS; gates log the new "enable it in Options → Mod Options"
  reason.
- **Docs same-commit:** D05 entry + index row, **PT-51** (Mod Options page
  eyes-on — now the FIRST step of the Group 8 sitting, since it is the enable
  mechanism), Group 8 preamble rewritten, MOD_DESCRIPTION optional-modules
  enable text now points at Mod Options (console-only instructions removed
  from player-facing text).
- **PT-51 first sitting, same night: `ListFixes()` crash found live and
  repaired** — latent since the 2026-07-25 F75/F18 status repairs
  (`entry.detail = nil` writers vs a concat in ListFixes; full trail on the
  D05 entry). Both writers now use `""`, ListFixes nil-tolerant. Takes effect
  on the user's next relaunch; **A/B pair re-verify queued for the next
  game-free window** (cosmetic to the probes — nothing reads ListFixes).
- **PT-51 COMPLETE, same night → D05 `tested` (archived):** all four toggles
  + tooltips good; live both ways proven twice (ClassicRockets on
  mid-session, MultipleSuns off/on vs the build menu); full shutdown +
  relaunch kept every toggle and the startup log shows all four modules
  self-activating from saved values; ListFixes printed 2×68 clean lines
  post-repair; log swept clean twice. **The PT-49 row reposition is also
  verified** ("UI good for dome" — the policy row now sits with the toggle
  group).
- **PT-49 first sitting, same night: core behavior PASSing** (closed
  high-comfort dome: zero move-ins, commute/services normal — screenshots).
  Cosmetic finding repaired same day: the policy row now inserts directly
  after the shipped accept-colonists toggle instead of below the stat bars
  (array reposition; trail on the D03 entry). Position re-check + the
  remaining PT-49 steps (arrivals, manual relocation, tourists, quarantine
  independence, MicroG row, uninstall) continue after the next relaunch.
- **PT-50 PASS in full, same night (the Group 8 sitting, running on the new
  Mod Options toggles) → D04 `tested`, F39's absorbed fix play-verified:**
  sun #2 built through the normal menu multiple sectors from #1; night
  production beside a sun matched the banked PT-26 signature exactly (3.6/9 @
  −21%; other sector 10 @ 0% — no atmospheric penalty there); sunless panels
  closed to 0 at night (not over-broad); save/reload clean; limit off/on
  verified LIVE via the toggle (doubles as PT-51 live-toggle evidence).
  Section archived. PT-51 partials recorded (page + live both ways verified;
  persistence-across-restart + log check remain). **Also observed live: an RC
  Terraformer (dozer) + waste-rock heap showed the F76 detached-hex picker
  rendering — Load-on-WasteRock is vanilla dozer behavior (RCTerraformer.lua:33,
  :224-237; pack ruled out, F74 wrappers refuse-only), and the picker surface
  DOES extend to the dozer path (user confirmed: hex appeared on CLICK) — F76
  addendum filed: any vehicle whose click-load reaches a storage-depot-class
  object is affected; loose rubble piles safe; the same TransferResources
  command workaround applies.**

## Build leg — Fable, 2026-07-27 late: F61 deletion + D02/D03/D04 built, A/B renumbered

The queued game-free build leg, executed as speced (all specs were on the BUGS
entries). Game never touched a save; three unattended `-smrautorun` legs only.

- **F61 retirement mechanics DONE:** `Code/Fix_HomeDomeMigrationGate.lua` + its
  metadata line deleted (git history restores them); the TestKit
  `HomeDomeMigrationGate` probe deleted with it (it tested the removed behavior —
  not an F10-style canary).
- **D02 `Opt_AcknowledgedWarnings` BUILT** (opt-in, off by default): dismissal of
  `NotWorkingBuildings` stamps every listed building
  (`SMRFixPack_ack_notworking`, absent-tolerant) and SKIPS the shipped
  4-game-hour whole-id window; stamped buildings' re-adds are dropped until
  recovery clears the stamp. Three chained wrappers on the notification helper
  GLOBALS (`SuppressNotification` — sole caller runs only under `dismissed`, so
  it IS the dismissal hook; `AddObjectToNotification`;
  `RemoveObjectFromNotification` — none is file-local in Notifications.lua, F22
  precedent). Only that one id is touched.
- **D03 `Opt_ResidencyControl` BUILT** (opt-in): new per-dome/habitat "closed to
  new residents" policy (`SMRFixPack_closed_to_new_residents` on the Dome,
  absent-tolerant). Gates: post-wrap `Community:CanAcceptNewColonists`
  (voluntary resettlement — only Src caller is FindEmigrationDome's filter) +
  post-wrap the global **`ChooseDome`** for arrivals. Build-time survey
  refinement: `GetDomesReachableByColonists` was rejected as the arrival patch
  point — it also feeds construction range display and worker checks, which must
  keep seeing closed domes; `ChooseDome` is the single choose-a-new-home funnel
  (rockets ×3, landers ×3, factory androids, stranded re-homing). `safety_dome`
  passes through unfiltered (no suffocation), `traits.Tourist` exempt (hotels).
  UI: post-wraps on `sectionDome:Init`/`sectionMicroGHabitat:Init` append the
  row; the toggle rides shipped `Community:TogglePolicy`/`SetPolicyState`
  (FX, Ctrl+click broadcast, rogue-dome UI lock for free). Closed state styled
  yellow/limit so it cannot be read as the red quarantine row.
- **D04 `Opt_MultipleSuns` BUILT** (opt-in): lifts
  `BuildingTemplates.ArtificialSun.build_once` from OnMsg.DataLoaded/DataChanged
  (handlers gate on registry status = opt-in + veto covered, F75 lesson; menu
  re-reads `CanBuildOnlyOnce()` live) AND absorbs the F39 wrapper + LoadGame
  sweep unchanged. `Fix_SecondArtificialSun.lua` DELETED; its probe reworked to
  the ClassicRockets SKIP-unless-opted pattern.
- **TestKit:** new `Code/60_Probes_Opt.lua` carries the three module probes
  (each SKIPs with the opt-in reason unless active); the two retired probes
  removed in place with dated tombstone comments.
- **Parse sweep:** 81 Lua files across both mods, 0 failures.
- **A/B pair + opt-in leg (2026-07-27, all clean, NEW EXPECTED NUMBERS —
  71 probes total now):**

| Leg | Log (Mars.exe-20260727-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack emptied) | 20.38.21 | 1 PASS, **56 FAIL**, 14 SKIP, 0 ERROR |
| Fixed (default config) | 20.39.59 | **57 PASS, 0 FAIL, 14 SKIP, 0 ERROR** — 64/68 active (4 opt-in inactive) |
| Opt-in (three new modules on via temp flag file) | 20.41.49 | **60 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — 67/68 active; all three new probes PASS incl. the live template lift |

  Renumbering from the old 1/58/11 · 59/0/11 (70 probes): −1 armed probe (F61
  deleted), F39's probe moved to opt-in SKIP, +2 new opt-in SKIPs (D02, D03).
  The 14 default-leg SKIPs = 10 [install] + 4 opt-in modules. Baseline's 1 PASS
  is still the FactionFundingCheck canary. Log noise unchanged (synthetic-map
  Flight.lua blocks in both legs; the quit-time TestKit mod-error artifact).
  Opt-in mechanism for the leg: temporary `Code/97_OptInLeg.lua` in the FIX
  PACK's code list right after 00_Core (set `SMRFixPack_Optional` before the
  Opt_ files load) — deleted after the leg; TestKit autorun flag line reverted.
- **Registered modules now 68** (67 − 2 deleted + 3 new); 64 active by default.
- **Docs same-commit:** BUGS index rows + heading tags (F39, F61, D02, D03,
  D04), MOD_DESCRIPTION Optional-modules section rewritten with the three new
  module blurbs (feature framing; F39 bug-fix bullet removed, sweep-list phrase
  dropped, D02 draft note resolved), PLAYTEST_CHECKLIST gains **Group 8:
  PT-48 (D02), PT-49 (D03 — first added infopanel row, needs eyes-on),
  PT-50 (D04, reworked PT-26 vs the banked single-sun baseline)**.
- **F76 was deliberately NOT touched** — attended sitting only (hard-lock
  vector; see the F76 entry and the prompt).

## Playtest marathon — Fable, 2026-07-26/27: 12 PTs resolved, F10 retired, D02 unblocked

One long interactive run with the user at the keyboard and this session driving
console instrumentation. Full per-test evidence is in `docs/PLAYTEST_ARCHIVE.md`
(new file — completed checklist sections move there, reporting-protocol step 8);
one-line summary here:

- **Flipped `tested`:** F03 (PT-02), F05 (PT-05), F12 (PT-07), F13 (PT-08),
  F44+F45 (PT-03), F47 (PT-45), F50 (PT-04), F51 (PT-12), F54 (PT-34),
  F66 (PT-41); **F52 `tested*`** (PT-13). F49(b) resolved no-defect (PT-46).
- **F12 second defect — the session's big catch (PT-07 first run):** the fixed
  updater's maintenance loop and food branch share the `"Food"` object key on
  the SAME notification; the maintenance else-path deleted the food branch's
  entry hourly → notification destroyed/recreated with FX + voice every game
  hour (voice plays only on whole-notification creation; VoicePerObject false).
  Latent in vanilla (broken math meant nothing could ever be added). Diagnosed
  by live console wrappers after five falsified hypotheses (dismissal cycle,
  threshold flap, object validation, stale second body, cross-city removal —
  full trail on the F12 entry). Repair: maintenance loop skips `"Food"`.
  **A/B clean 2026-07-27:** baseline 11.45.34 = 1/58/11/0; fixed 11.47.09 =
  59/0/11/0, 66/67 active. Re-run PASSed all behaviors incl. silent organic
  clears on both branches.
- **F10 CLOSED `wontfix` + DELETED (PT-36):** the three funding calls returned
  0 cleanly over a maximally nil organic history, and later read a real
  $544.5M tourist payout correctly — premise dead both ways.
  `Fix_FactionFundingCheck.lua` and its commented metadata line removed
  (git history restores both); the TestKit probe stays as a canary (it is the
  baseline's expected "1 PASS" — documented A/B numbers unchanged).
- **D02 gate DONE with a premise CORRECTION (PT-38):** the dismiss window is
  **120,000 GAME-ms = 4 game hours**, not 2 real minutes (`GameTime` defaults
  true; three live timestamped dismissal→return pairs = 120,000 +
  time-to-next-attempt, every in-window re-add attempt observed BLOCKED;
  suppression is per notification id). At ultra the re-nag is every few REAL
  seconds — D02's case is STRONGER. `Opt_AcknowledgedWarnings` build unblocked.
- **PT-06 (F08) DONE 2026-07-27 (later) → F08 `tested`:** 5★ 10-tourist
  departure paid at Earth ARRIVAL "+23 applicants, $544.5M" (2.3/head =
  top-tier); the tanked half (a 25-tourist group into a stripped dome —
  homeless, services off, Earthsick early leavers) paid "+7 applicants,
  $94.5M" = **0.28 applicants/$3.78M per head — an 8× per-head split**.
  Mechanics confirmed from Src during the run: departure rewards walk every
  boarded Tourist with no sols/reason filter (early leavers count); any stat
  < 30 caps the rating at the 2★ tier (`HolidayStatCapRating`); 7-from-25 is
  in band for the corrected mostly-1★ roll (~10 expected) and ~3σ below the
  shipped inverted roll (~15 expected) — corroborating evidence, not noise.
  Two cosmetic vanilla quirks
  recorded in the archive entry (overstay-cycle button no-ops silently on an
  empty sol-10+ bucket and only cycles the current map; sols-based tooltip
  labels early-leavers "Enjoying their holiday").
- **PT-26 (2026-07-27, later): F39's premise UNREACHABLE in the unmodded game →
  D04 filed (user decision).** The Artificial Sun is a `build_once` wonder
  enforced colony-wide incl. construction sites (`BuildMenu.lua:711-719`
  counting `UIColony.labels`; the tester's build menu refused sun #2 with sun
  #1 standing) — two suns can never coexist, so the F39 fix is latent hardening
  vanilla can never exercise. Resolution: **D04 `Opt_MultipleSuns`** — opt-in
  module that lifts the limit (`BuildingTemplates.ArtificialSun.build_once =
  false`, read live by the menu — verified in-session) AND absorbs the F39
  binding fix, so the pack provides the condition its fix needs and spares
  players a third-party limit mod that would hit the vanilla `[1]` bug.
  Single-sun baseline banked (night production at −21% atmospheric beside the
  lit sun). Standalone fix file deletion + module build queued for the
  game-free leg. Spec on the D04 entry.
- **F76 NEW FINDING (2026-07-27, found live during PT-39 setup): the RC
  Transport depot resource picker renders far from the cursor and cannot be
  clicked** (vanilla, P1). "Load from depot" looks completely broken — icon +
  noise, nothing loads — while ground piles work (no picker on that path). Live
  instrumentation proved the `ResourceItems` dialog opens and STAYS ALIVE
  (`box=(886,13)-(1054,442)`, 1 item) but draws as a giant detached hex near
  the top of the screen, and clicks on it fall through to the map (selection
  churn then closes it via its own `OnMsg.SelectionChange`). Suspected
  `terminal:GetMousePos()` vs scaled-UI coordinate mismatch (~1.88 display
  scale maps the box back onto the true cursor position); 1080p error is small
  enough that it passed QA. Pack ruled out (all wrappers pass-through). Also
  affects the multi-resource unload and route pickers. Command-level workaround
  verified. **Wave-6 build candidate** (`Fix_ResourcePickerAnchor`); PT-39's
  depot control half is blocked on it (trade-rocket half unaffected).
  **User's release warning, recorded: this WILL draw false bug reports against
  the pack** — MOD_DESCRIPTION carries a draft-note for a "known vanilla
  issue" explainer (D02 precedent). Full forensics on the F76 entry.
  **Escalations (same day, later):** the multi-resource UNLOAD surface confirmed
  by play; environment pinned (fullscreen 3840×2160, UI Scale ~80-85%); and the
  broken picker can **HARD-LOCK the UI** (every MouseEvent erroring on a
  destroyed window in the modal/anim chain, `XWindow.lua:1154` — Alt-F4
  required, session lost). Live prototyping also established the dialog's own
  scale is applied AFTER Init (Init-time anchor conversion is a no-op — the
  repair belongs in/around UpdateLayout). **Process decision: no further live
  UI-internals prototyping on play sessions; F76 repair is an attended
  game-free leg task.**
- **PT-39 (2026-07-27, later): F74 → `tested`.** A landed TRADE rocket was
  fully refused by the RC Transport cursor ("treats it like normal terrain")
  AND by the route path — the route endpoint fell back to a ground position
  and the cargo was dumped at the pad, rocket untouched (the route handler
  only stores targets the guarded interaction check approves). Controls
  clean: ground-pile pickup + depot loading via route mode both work (the
  route path skips F76's broken picker for single-resource depots,
  `RCTransport.lua:466-476`). Cosmetic aside recorded: rovers clip through
  the landed event rocket's model.
- **Engine/tooling facts learned (also in the prompt + command table):**
  infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused); tourists are 5% of applicants and the
  passenger filter EXCLUDES the Tourist trait by default (`initial_filter`);
  tourist stay is 5-10 sols; tourism rewards fire at Earth arrival; funding
  history is a 12-sol ring (`Funding.lua:86`); `CityStart` fires at
  map-generation time — use `InGameInterfaceCreated` for UI-ready work (TestKit
  console repair 2026-07-26); TestKit gained `SMRTest.Cls`.
- **Docs restructure:** completed playtests + evidence now live in
  `docs/PLAYTEST_ARCHIVE.md`; the checklist carries only un-run work
  (reporting protocol step 8 keeps it that way).
- **PT-14 (2026-07-27, after the session wrap): F61's premise FALSIFIED →
  CLOSED `wontfix` (user decision same day), community ask re-filed as D03.**
  The accept-colonists toggle is a **quarantine**: its OFF state is titled
  "Quarantined" and the rollover promises "Colonists are not allowed to enter
  or leave" (reused original-game T-ids — carried-forward wording);
  `Colonist:FindEmigrationDome` enforces it with the literal comment
  "quarantine, no one enters or leaves" (`Colonist.lua:2632-2634`). The lockdown
  the tester observed is designed behavior, and the shipped fix half-SUBVERTED
  it — worse, a use-case survey found scripted content that depends on the seal
  (Wildfire's dome-local infection spread `Traits.lua:1155-1173`; the RogueDome
  story bit FORCE-quarantines a renegade dome via `SetBuildingRogueState` →
  `Dome:SetUIInteractionState`; arrival routing's `is_welcoming_community`).
  **Resolution: `Fix_HomeDomeMigrationGate.lua` deletion STAGED (F10 precedent;
  needs a game-free leg, A/B numbers shift by one probe), and the real community
  ask — block move-ins WITHOUT locking commute/services — is filed as D03
  `Opt_ResidencyControl`:** a new per-dome "closed to new residents" policy row
  appended by post-wrapping `sectionDome:Init` (the infopanel section is a plain
  Lua class building rows imperatively — verified), gating
  `Community:CanAcceptNewColonists` + the arrival path, quarantine untouched.
  Full spec on the D03 entry; build queued for a game-free leg alongside D02.
- **PT-24 (2026-07-27, later): F36 → `tested`, both halves.** Geologist demand
  went **11 → 0 at the ExtractorAI grant with every other row identical**
  (before/after screenshots — the user reloaded a pre-tech save for the
  baseline, which also disproves over-exclusion since the pack was active both
  sides); multiple `CheatCompleteTraining` rounds across two universities
  graduated **38 engineers + 2 medics, zero geologists** (tallies from the
  universities' `trained_specialists`, captured in log
  Mars.exe-20260727-15.19.26). Setup gotcha found live and corrected in the
  checklist command table: **`CheatResearchAll()` skips undiscovered
  breakthroughs** (`Cheats.lua:84` discoverable-or-discovered gate) — grant
  directly via `UIColony:SetTechResearched("<Id>")`; PT-27's Biorobots route
  corrected to `ThePositronicBrain` in the same pass.
**ONE live prompt (updated 2026-07-28 — post-D06 build):**
- `docs/FABLE_NEXT_PROMPT.md` — playtest-standby assistance: the user plays,
  the session drives console instrumentation and processes results live.
  Rewritten 2026-07-28: PT-52 (D06 overhaul watch-and-judge) is the board
  centerpiece with assistant-side briefing notes; carries the queued A/B
  re-verify as pre-flight (module counts moved to 65/70 — probe numbers
  unchanged), the F76 avoidance rules, and the attended-sitting spec.
- Retired prompt files (each done and deleted/superseded):
  ~~OPUS_BUILD_PROMPT~~, ~~FABLE_QA_PROMPT~~ (2026-07-25),
  ~~FABLE_PLAYTEST_PROMPT~~ (merged into the one live prompt),
  ~~DRONE_INVESTIGATION_PROMPT~~ (2026-07-28 — its verdict, F77, and the
  D06 build all landed; the R1-R7 forensics it produced live on the BUGS
  DroneControl bullet, and PT-52 carries the live half).
BUGS.md is
the canonical defect tracker, FIX_POLICY.md the patching rules, WORKFLOW.md the
dev/test/release process, RESEARCH.md the lead catalog (incl. ChatGPT dossier
cross-check), MOD_DESCRIPTION.md the player-facing mod-page draft (update its fix
list in the same commit that implements a fix; only `tested` fixes ship in the
final text), TESTING.md the force-the-bug test plan, CHEATS_INVENTORY.md the
shipped cheat/debug surface the tests drive.

## Follow-up session — Fable, 2026-07-26: F02 hunt + watchdog, F66 reclaim, F47 composition, version tags — A/B CLEAN

**Task 1 — F02 regression hunt (PT-01 FAIL, no reloads).** Every static explanation
was FALSIFIED against the playtest log (Mars.exe-20260725-19.04.10) — full record on
the F02 entry. Established: one uninterrupted session (single `Load Game:` marker,
day counters monotonic to 36, wave-3 roster); no `[LUA ERROR]` anywhere near the
stall; the tower wait-math is bounded (warning = Min(6h+12h·3, 75h) = 42h, two sleeps
total ≤ spawn+1s ≤ 60h on Meteor_VeryHigh); the descriptor-nil day-loop needs
Atmosphere > the **80%** MeteorStormStop threshold (TerraformingDisasters.lua:69,
TerraformingParam.lua:80-84) — impossible at sol 12; nothing in Src or either mod
deletes/restarts the thread mid-game; the PT-03 track debris postdates the silence.
Bonus finding: the first MeteorStorm (birth_hour = 250h + 0..25h) was due in the SAME
window and never visibly fired — BOTH disaster threads went quiet at t≈8.2-8.3M, so
the mechanism sits outside both loop bodies (scheduler/persist side) and needs a live
capture. **Root cause NOT pinned; the rework captures it next time:** heartbeat
phases in the thread body (zero closure upvalues — the persisted thread keeps the
engine-proven persistence shape), loud top-of-body exits, a daily OnMsg.NewDay
watchdog (`SMRFixPack.MeteorsWatchdogCheck`, threshold spawn+random+75h+1 sol, gives
up loudly after 3 restarts, respects the fix's status — F75 lesson) that logs
**thread ALIVE-but-stuck vs DEAD + last phase** before restarting, and a LoadGame
necropsy of the persisted thread — loading the user's sol-36 save answers
dead-vs-stuck directly. Probe reworked install→behavior (drives the watchdog with a
synthetic stale heartbeat; discriminates in the retail sandbox instead of SKIPping).

**Task 2 — F66 rebuild trigger (user decision: repair).** Landed in
Fix_TrackConnectorPingPong.lua: post-wrap of `TrackConnectedObjBase:Done` (declaring
class; destructor, not command-killed) records the dying building's connector hexes
before the shipped body runs, then `SMRFixPack.TrackConnectorReclaim` queries each
hex with `map:MapForEach(pos, "hex", 3, "TrackConnectedObjBase", …)` (spots reach
≤ ~2 hexes; no global rebuild) and schedules the engine's own deferred idiom with
in-thread revalidation (TrackElement.lua:194-198) for every other live,
non-destructing candidate; guarded CreateConnectorElements makes re-runs idempotent;
done_map early-returns. Probe extended: exactly one rebuild scheduled (live
neighbour), dying self + destructing excluded, hexes deduplicated.

**Task 3 — F47 composition under-refunds (both audit MEDIUMs).** Landed in
Fix_TrackSalvageRefund.lua: the stand-down test is now the `demolishing` stamp
`TrackBase:OnDemolish` writes (Track.lua:250 — survives object death), so a
trim-to-empty (dies via CanDelete→DoneObject, no OnDemolish) refunds instead of
being misread as "already handled"; map/drop-pos captured pre-orig. The
construction-site early-return is narrowed to the repair-site delegation only —
plain sites fall through and their zone's stamped completed elements are accounted
(no double-refund: sites never carry stamps). Details on the F47 entry.

**Release item:** all full-replacement headers now name the game version the copy
came from — **game 1.0.7.396349** (was "shipped Src, 2026-07" / "post-1.0.7").

**A/B pairs (both clean; probe-count change is by design: the F02 probe moved from
install-SKIP to a discriminating behavior probe, so 12 SKIP → 11, 57 FAIL → 58):**

| Leg | Log (Mars.exe-20260726-…) | Result |
|-----|---------------------------|--------|
| Baseline #1 (pack emptied) | 00.06.11 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #1 (F02+F66 in) | 00.08.03 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — watchdog exercised end-to-end in-log |
| Baseline #2 (after F47 + version tags) | 00.11.46 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #2 (everything in) | 00.13.02 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active (ClassicRockets opt-in) |
| Baseline #3 (after the seed-crash repair) | 00.48.22 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #3 (seed repair + sweep extension in) | 00.50.08 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active |
| Baseline #4 (after the F18 savegame sweep) | 11.33.34 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #4 (F18 sweep in) | 11.34.58 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — F18 probe verifies the sweep both ways |

Parse sweep: every .lua in both mods parses (python luaparser).

**Live playtest, same night (user on the sol-36 save, results processed live):**
- **F02 necropsy answered: the wedged Meteors thread was ALIVE** — "persisted
  Meteors thread on load was alive" — a live thread whose wake-up never came
  (scheduler/persist side), not a dead one. Post-load natural gaps **+49h and
  +40h**, both in band; >42h is impossible under the broken code with 3 towers, so
  the cadence+towers check is satisfied on real play. Watchdog reported `healthy`.
  Also confirmed: single meteors get NO tower-scaled warning banner in the shipped
  game (the singles thread posts no notification; only the ~30 s Predict marker,
  and only with objects in the blast area) — the PT-01 checklist expectation was
  corrected accordingly (towers' lead shows in the STORM countdown).
- **PT-03 F44 halves PASS:** the load sweep removed the 40 orphaned elements from
  the first attempt; repeated build → salvage → rebuild cycles on straight AND
  curved tracks clean; train survives; **partial-salvage Metals refund observed
  live** (F47's half B).
- **New defect found during the F45 attempt, repaired same night (seed crash):**
  destroying a repair site in the deletion zone ALSO destroys its broken twin
  (TrackGridElement:Done, TrackElement.lua:200-201); the twin shares the site's
  node_idx and can sit just outside the zone at the seed index, and the shipped
  blind seeds (`all_elements[last]`/`[first]`) then crash ExpandTrackFromElement
  on a dead element (TrackElement.lua:718-719, `map` nil — mod-flagged MouseEvent
  error; unreachable in vanilla because broken tracks were unsalvageable before
  F45). Repair in Fix_TrackSalvageWipe.lua: seeds walk outward to the first
  still-VALID survivor, a side with no survivor is tolerated (empty new_track
  destroyed), and the LoadGame sweep now ALSO purges destroyed entries left
  inside track arrays by the aborted split (log line reports both counts —
  expect it on the user's save). **F45's salvage step remains the open PT-03
  item** (retry procedure written into the checklist).

**Open for the user after this session (updated 2026-07-26 late):** PT-01 longer
silence-watch only (cadence, tower warning lead AND necropsy all verified live;
the watchdog self-reports if the wedge recurs); rest of the merged-pack
checklist; PT-36/37/38 gates; MarsDebug attended [install] pass for wave-4/5.
**DONE since this record was written (commits 4310fb2..bc4e828, same day):**
PT-03 F45 retry PASS → F03/F44/F45/F50 `tested`; PT-45 PASS → F47 `tested`;
PT-46 PASS → F49(b) resolved no-defect; PT-01 tower-extended ~42h storm warning
banner verified live. Those commits flipped the BUGS.md detail headings but not
the index rows; the rows were synced in the follow-up doc-sync commit.
**PT-41 PASS (recorded 2026-07-26 later) → F66 `tested`:** shared hex stable, no
connector churn in the 11.48.31 log; demolishing one building left the survivor
connected ("became its own node but stayed connected … no weird visuals" — the
reclaim repair); plain-tile control clean.
**PT-07 first run FAILED the steadiness half (2026-07-27) → F12 second defect
found + repaired, A/B PENDING:** the Food warning fired correctly but the
notification was destroyed/recreated hourly (flash + voice replay). Live console
instrumentation attributed it to the surface city's own tick: the maintenance
loop and the food branch share the `"Food"` object key, and the maintenance
else-path deleted the food branch's entry each hour (voice plays only on
whole-notification creation — VoicePerObject false). Repair: maintenance loop
skips `"Food"` (the food branch owns the key). Full forensic record on the F12
entry. **A/B pair re-verified clean same day (2026-07-27):** baseline
Mars.exe-20260727-11.45.34 = 1 PASS / 58 FAIL / 11 SKIP / 0 ERROR; fixed
-11.47.09 = **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR**, 66/67 active,
LowStorageWarning applied, zero errors from our files. Repair landed. **Open:
the user re-runs PT-07 on the repaired build (warning fires AND sits steady +
the Machine Parts half).** → **DONE 2026-07-27: PT-07 PASS in full, F12 `tested`**
(fires once / steady a sol / silent organic clear, both branches; see the
checklist archive).
**PT-38 DONE (2026-07-27) — D02's premise measured and CORRECTED; build
unblocked.** The dismissal window is **120,000 GAME-ms = 4 game hours**, NOT 2
real minutes: `GetTime()` = `GameTime()` because `GameTime` defaults true and
the NotWorkingBuildings preset doesn't override it (`NotificationPreset.lua:65-66,
:126-128`). Live timestamp wrappers measured three dismissal→return pairs at
148,805 / 161,755 / 132,056 game-ms — each 120,000 + time-to-next-attempt, every
in-window attempt observed BLOCKED. At ultra the re-nag is every few REAL
seconds — D02's case is stronger than premised. Suppression is per notification
id (fuel warnings independent — user-observed). **D02 (`Opt_AcknowledgedWarnings`
+ probe) is now buildable in the next build leg with the corrected spec.** Two
engine facts from the sitting: infopanel cheat buttons need `Platform.cheats =
true` (ObjCheat gate, `Network.lua:218-219`) AND their presses ride the
game-time sync queue — dead-looking while paused, firing on unpause.
**TestKit console repair (2026-07-26 later, user report: console dead on every
NEW save, fine on loads):** root cause — `Msg("CityStart")` fires from
`OnMsg.NewMap` DURING map generation (`Lua/_init.lua:18-26`), so the kit's fixed
2 s sleep auto-opened the console into a desktop the loading flow then replaced.
Repair in TestKit 00_TestCore.lua: also hook **`InGameInterfaceCreated`** (end
of `InGameInterface:Open`, `Lua/UI/InGameInterface.lua:388` — fires on BOTH new
games and loads, guarantees the UI exists), the open thread now waits on
`WaitLoadingScreenClose()` (`CommonLua/UI/LoadingScreen.lua:374`) instead of
guessing, and auto-open arms once per session entry so mid-session interface
reopens re-assert enable+shortcut without popping the console again. **Engine
fact: CityStart is a map-generation-time message, NOT a UI-ready message — use
InGameInterfaceCreated for anything that needs the in-game UI.**

**F18 open half CLOSED (2026-07-26, user-driven):** the user asked whether
resetting the tech was the easy fix; the investigation it prompted found better —
the stored modifier is keyed by the effect object and the shipped applier passes
the tech preset as parent (`GameEffect.lua:36-40`), so a LoadGame sweep re-runs
`effect:OnApplyEffect(UIColony, tech)` argument-identically to research and
replaces the stale -10 with -20 in place. No reset, no re-research, no first-load
flag (state-detected, idempotent). Probe extended to drive the sweep both ways.
F18 status is now plain `fixed`.

**User decision 2026-07-26 (D01 export half): match the ORIGINAL game, not a new
design.** Spec = the legacy loader (RocketBase.lua:1729-1736: standing
PreciousMetals demand to max_export_storage, any-drone flags, per-rocket
allow_export toggle). Build queued for a build leg with three research items
(toggle mapping onto UniversalRocket, modern sell-on-arrival path, whether the
original auto-offloaded RC transports — decides if F56's behavior rides along);
own probe + playtest item; same ClassicRockets flag. Details on the D01 entry.

## QA session (waves 4+5) — Fable, 2026-07-25 evening: merge + audits + A/B CLEAN

**Task 0 — merge:** `wave4` merged to main in BOTH repos with zero conflicts (fix pack
2f09133, TestKit 17f7b3c), worktrees removed, branches deleted, fix pack pushed. The
commented-out F10 metadata line survived. 21 new modules → 68 metadata entries,
67 registered modules.

**Task 1 — parse sweep + A/B pair:** all 80 Lua files in both mods parse. Logs in
`%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack code list emptied) | 22.46.34 | 1 PASS, **57 FAIL**, 12 SKIP, 0 ERROR — every armed probe FAILs |
| Full pack | 22.48.50 | **58 PASS, 0 FAIL**, 12 SKIP — exposed the F75/F18 status-relabel defects (fixed, cdff2ce) |
| Verification (status repairs in) | 22.52.57 | **66/67 active** (ClassicRockets opt-in inactive), **58 PASS, 0 FAIL, 12 SKIP, 0 ERROR** |

The 12 SKIPs: 10 `[install]` probes (retail sandbox — MarsDebug pass covers them),
ClassicRockets (opt-in, verified separately in the wave-3 opt-in leg), and
TechDescriptionBuilding (below). Non-Flight `[LUA ERROR]`s present in BOTH legs are
synthetic-map GameInit noise in shipped files (BuildingWayPoints/TaskRequest/GridObject);
nothing names an SMR file. A `[mod] Error in mod … Test Kit` line at quit time is a
shutdown artifact (fires at the harness's own `quit()`, exit code 0, results complete).

**The two wedged legs (21.01.55 and 22.29.10) were a TestKit probe defect, not the
game:** the TrainWaitTime probe faked the sleeping `PlayPrg` as a no-op, so the shipped
`while self.holder == vehicle do self:PlayPrg() end` ride loop span without yielding and
starved EVERY Lua thread — including the harness watchdog (why it never fired) and the
log writer (why the logs looked empty; the buffer only flushes at exit). Repairs
(TestKit bafbd61 + 80de593): the fake now ends the ride; the harness flushes the log
per line so a killed run keeps its evidence; `ShowStartGamePopup` is neutered when the
autorun is armed (the "Welcome to Mars, Commander!" popup was on screen but was NOT the
wedge); watchdog raised to 15 min. **Engine-fact lesson: a probe must never fake a
blocking primitive as a no-op inside a driven loop.**

**Task 2 — probe discrimination:** 19/20 wave-4/5 probes FAILed baseline → PASSed
fixed: RocketInteractGuard, TrackConnectorPingPong, TrackTunnelPowerBridge,
GridGlobalStorage, LastTransmissionStorage, TrainWaitTime, GraphConsumedCaption,
MoraleComfortTooltip, ReplaceTechCount, StorageRateModifiers, SequenceLatents,
FounderTraitNotification, IndependenceTerraforming, TrackSalvageRefund, LayoutTechLock,
TrainMinors, DroneTransportMinors, AnomalyCaveInMap, BombardmentSpread. **Not
discriminating: TechDescriptionBuilding** — SKIPs both legs ("the tech has no
description T": the probe finds `TechDef.UndergroundLargeDome.description` is not a
table at probe time). F25 is therefore NOT probe-verified; its playtest item is the
evidence path (or a console read of the description). F24 has no probe by design
(PT-44). FactionFundingCheck PASSes both legs as always (F10 retired, PT-36 gate).

**Task 3 — audit fan-out (14 read-only subagents, every verdict verified before
action):** CLEAN: F20, F21, F22, F24, F74 (premises held; only LOWs). Findings that
led to repairs, all landed and covered by the final A/B:
- **F57a HIGH (live game-breaker):** `rfRestrictorRocket` is a FILE-LOCAL
  (DroneControl.lua:12); the replacement read it as a global and raised on every
  rocket-restrictor update → drones would stop servicing rockets. Repaired 493f054.
- **F28 MEDIUM:** the dropped `assert(tech_def.group == status.field)` was load-bearing
  through its ARGUMENT (raises on unknown tech_id_new BEFORE mutation); the copy mutated
  first. Guard restored b66995f.
- **F26 HIGH (dead fix):** preflight checked BombardMissile for methods declared on
  BaseMeteor (invisible pre-flattening — the F64 lesson AGAIN) and required the
  SessionRandom GameVar at apply time; the fix could never activate. Repaired 11ecd22.
- **F75 HIGH + F18 sibling:** preset-patch fixes relabeled themselves
  "inactive: already correct" when the engine's post-DataLoaded `DataChanged(false)`
  reran them over their own corrections; F75 also bypassed the SMRFixPack_Disabled veto
  in its OnMsg path and misread the EMPTY pre-DataLoaded GlobalMap as a vanished
  target. Repaired 11ecd22 + cdff2ce. **Engine fact: `Msg("DataChanged", false)` fires
  right after every DataLoaded (Dlc.lua:715-717, :680-685); FactionDefs/TechDef
  GlobalMap tables exist EMPTY before DataLoaded.**
- **F43 HIGH (latent):** `IsValid()` on pure-Lua InitDone controllers is always falsy
  (C-side check; cf. RealTimeCommandObject's own override) — the teardown was dead code
  and would have leaked the cursor object when a tech-gated layout entry ever goes
  live. Guard dropped 11ecd22. **Engine fact: IsValid() rejects pure-Lua objects, not
  just probe stand-ins.**
- **F31 MEDIUMs:** the divergence paragraph's marsquake claim was FALSE (every engine
  TriggerCaveIn call is already Underground-gated, Marsquake.lua:285/:294/:323-325) —
  corrected in place; and the 8th call site crashes inside `FindCaveInLocation`
  (CaveInRubble.lua:27) before the wrapper — a second decline-wrapper now covers it
  (11ecd22, 8/8 sites).
- **F49:** (d)'s rationale was backwards (GameInit is DEFERRED, _object.lua:187-192 —
  the surviving track is the real defect, which the fix covers) and coverage gaps via
  AutoConnectTracks/instant-build reuse are recorded as accepted (sweep corrects on
  load); (c) implemented per the user's decision (below); (b)(e) screenings verified
  sound. F20/F74 wrappers got vararg pass-throughs (§1.4).
- **F65 HIGH:** the 2-element special deletion path (TrackConnectedObjBase:Done,
  TrainTransport.lua:24-27) DoneObjects the track with NO DisconnectFromGrids — and
  only F65 ever creates a bridged 2-element track, so demolishing an endpoint leaked
  tunnel mask/adjacency into the save. Repaired 8e0b177: TrackBase:Done is pre-wrapped
  to run the shipped DisconnectFromGrids (tolerates a dead endpoint by design;
  RemoveSupplyTunnel clears the flag so demolish-path double-calls no-op). The
  MEDIUM (different-grids test is one-shot; cable-topology declines re-check only on
  next load's sweep) is documented as accepted in the fix header.
- **F47 MEDIUMs (recorded, NOT yet repaired — both under-refunds, no over-refund/save
  hazard):** F44's trim-to-empty exit skips the refund (composition gap), and the
  construction-site early-return is broader than repair sites. On the list for a
  future leg.
- **F66 MEDIUM (recorded, awaiting user decision):** after the blocking neighbour is
  demolished, the guarded building never reclaims the connector hex (no rebuild
  trigger reaches it) until any track demolish fires the global rebuild or it is
  re-placed. Options given to the user: accept+document vs a demolition-path rebuild
  trigger.
- Recurring minors: full-replacement headers date the copy instead of naming the game
  version (FIX_POLICY §1.5) — release-checklist item; assorted citation drift fixed.

**User decisions recorded this session:** F42 CLOSED `wontfix`; F49(c) = "the click
does nothing", implemented.

**Playtest findings processed live (first sitting, wave-3 pack):** PT-02 PASS, PT-04
PASS (status flips belong to the playtest-report session). **PT-03 F44 curve FAIL →
diagnosed and REWORKED (a38cbf2):** the split branch could delete a physically
scattered zone whenever sorted order diverged from physical order (exactly the
non-numeric node_idx state the old comparator sorted as -1 and carried on with),
stranding orphaned elements (track_obj == false) that raise on every later click —
the user's "broke itself, became immune" with screenshots. Now: orphan clicks delete
the debris, the salvage declines BEFORE deleting anything when order can't be trusted,
the split tail is IsValid-guarded, and a LoadGame sweep removes orphans already baked
into saves (the user's playtest save will log `TrackSalvageWipe: removed N orphaned
track element(s)`). **PT-03 needs a re-run.** PT-01 (meteors stopped after sol ~12.5,
FAIL) is NOT yet diagnosed — first question is whether the user reloaded during the
quiet stretch (every load re-rolls the 65-90h Low-threat interval; frequent reloads
legitimately push strikes out). If they didn't reload, F02 has a real regression to
find.

**Commits this session (fix pack):** 2f09133 merge, b66995f F28, 493f054 F57a,
09af088 playtest notes, 11ecd22 audit repairs, 8e0b177 F49c+F65, 75c54f6 doc
corrections + F42 (NOTE: accidentally committed the baseline's emptied metadata via
`commit -a`; restored in 1321795 — never use `-a` while an A/B leg's metadata edit is
in the working tree), a38cbf2 F44 rework, cdff2ce F75/F18 status. TestKit: 80de593
harness hardening, bafbd61 probe wedge fix + 15-min watchdog.

**Open after this session (both user answers now in, 2026-07-25 late):**
- **PT-01: NO reloads** → F02 is genuinely regressed (meteors stopped for 560+ game
  hours on a max-threat map after Sensor Towers went up) — REOPENED `fixed*`,
  investigation speced in docs/FABLE_NEXT_PROMPT.md Task 1.
- **F66: user chose the rebuild-trigger repair** over accept-and-document — spec on
  the F66 entry + docs/FABLE_NEXT_PROMPT.md Task 2.
- PT-03 re-run (user, next sitting); F47 composition under-refunds; MarsDebug
  [install] pass for wave-4/5 (attended, SetupOnly); game-version tags on
  full-replacement headers (release checklist).

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

Companion **Test Kit** mod (never shipped): `C:\Dev\SMR-BugFixPack-TestKit` (git).
`SMRTest.RunAll()` runs one probe per fix and prints PASS/FAIL/SKIP; run it with
the fix pack disabled (expect FAILs) and enabled (expect PASSes). It also enables
the Lua console at load and carries observability loggers and state reports.

## Discovery: COMPLETE

- 73 tracked findings (~85 distinct defects) verified against the CURRENT
  (post-1.0.7) shipped source, each with file:line evidence + fix sketch in BUGS.md.
- 1 design-change verdict (D01 rocket auto-refuel/rare-metals — plan opt-in module).
- 2 candidates needing runtime checks (C01 BreakthroughOrder, C02 asteroid cave-ins).
- 3 critical UNTRACED leads (RESEARCH.md): 90%-breathable-atmosphere freeze,
  Last War mystery import lock at 54%, game-stops-saving. Plus smaller new leads
  from the ChatGPT dossier cross-check (top of RESEARCH.md).

## Implementation: 47 tracked defects DONE across 46 registered modules (ALL probe-verified in-game 2026-07-25 — wave-3 A/B pair clean, see the QA session section; F10 retirement STAGED 2026-07-26, premise falsified, final wontfix gated on PT-36)

Wave 1 (earlier session): F01 cave-ins/NoDisasters, F02 meteor frequency,
F03* upgrade-modifier leak, F04 night shift, F05 milestone crash, F07+F15* wisp
power/rewards, F08 tourist applicants, F10 faction funding, F64 trains-to-void.

Wave 2 (earlier session, in queue order): F67 lander empty launch, F68 lander cargo
ratchet, F69 lander return fuel, F73 shelter reflex, F45 broken-track salvage,
F44 track salvage wipe, F30 lake entombment, F37 ghost farm oxygen, F50 rocket
drone churn, F51 shuttle transport cache, F52* vacuum walks, F53 arrival deaths,
F55* drone unreachable-forever, F58* stale reservations, F61 home-dome migration
gate, F06 crystal mystery hang, F09 tourist satisfaction, F11 train platform
wedge, F12 low-storage warning, F13 Command Center numbers, F14 Domes Overview
highlight.
(* = partial; the remaining half is recorded on the BUGS.md entry.)

Wave 3, first leg (session 3, in queue order): F46 train cargo dumping, F36 university
overtraining, F38 destroyed tunnels, F39 second artificial sun, F40 Dust Sickness on
Biorobots, F17 Dust Sickness randomization, F41 Gene Forging, F16 Mirror Sphere site,
F70 Edit Payload template refill.

Wave 3, second leg (session 4, in queue order): **F71** auto-export capacity priority
(folded into `Fix_LanderCargoRatchet.lua` — F68 already replaced that function),
**F72** asteroid-lander availability gate, **F54** switched-off shuttle hubs,
**F59*** freed housing notifies the homeless, **F60** dome free-space member mismatch,
**F33** small landscaping site drone crash, **F34*** landscape units-underneath filter,
**F35 + F03 sweep** in the new `Code/90_SaveSanitizer.lua`, and **D01** as the opt-in
`Code/Opt_ClassicRockets.lua` (fuel half only).
(* = partial; the remaining half is recorded on the BUGS.md entry.)

**The whole wave-3 queue is now done.** Nothing from the session-3 handoff list is left
except the four entries deliberately parked as `blocked` (see below).

**Wave-3 fixes are now probe-verified in-game (2026-07-25 QA session):** the RunAll A/B
pair ran clean — every armed probe flipped FAIL→PASS, 46 fixes + sanitizer `applied`,
ClassicRockets `inactive` by default and `applied`+PASS in the opt-in leg. Full results
in the "QA session (wave 3)" section below.

Three first-leg fixes add their own `OnMsg.LoadGame` repair pass: F38 (close destroyed
tunnels left open in pathfinding), F39 (reconnect solar panels to a sun in range), F40
(clear Dust Sickness from already-infected Biorobots).

`Code/90_SaveSanitizer.lua` now exists and carries the remaining consolidated sweeps:
**F35** (restore the Frictionless Composites label modifiers the shipped migration fixup
dropped) and **F03** (remove upgrade modifiers orphaned by salvaged buildings). Both are
idempotent, both run on **`OnMsg.PostLoadGame`** (NOT LoadGame — the QA audit found that
`Msg("LoadGame")` fires BEFORE `FixupSavegame`, `Savegame.lua:810-813`, so a LoadGame-time
F35 pass raced the shipped turbine fixup and could bake +200% onto Shrouded turbines on a
never-patched save's first load; see the F35 entry), and both are exposed on
`SMRFixPack.Sanitizer` so QA can re-run them from the console (`RepairTurbineBuff` /
`RepairLeakedUpgradeModifiers`, each returns a repair count). **F48 is NOT in it** — see
its BUGS.md entry.

Other fixes carrying their own one-shot `OnMsg.LoadGame` / `OnMsg.NewDay` pass for state
already baked into savegames: F02 (thread restart), F45 (stamp repair sites), F37 (remove
phantom farm oxygen), F58 (release stale reservations), F06 (restart the crystal repeater),
plus F55's expiry which self-heals.

**Savegame footprint** (FIX_POLICY §3 — all absent-tolerant): `colonist.SMRFixPack_reserved_at`
(F58), `transporter.SMRFixPack_payload_set` (F70), an entry keyed `smr_shuttles` on a
transport-cache entry (F51, a hash key that does not affect `table.unpack`), and — only
where the sanitizer repaired one — a label modifier under `SMRFixPack_F35_<label>` (F35).
README's old "stores nothing in your savegames" claim has been corrected accordingly.

## Optional modules (new in session 4)

Off by default. **Players enable them in Options → Mod Options (D05,
2026-07-27 late — live toggles, both directions);** the pre-load
`SMRFixPack_Optional = { <Id> = true }` table remains as the override surface
for other mods and the test harness. `SMRFixPack.ListFixes()` reports them as
`inactive` with the opt-in reason until enabled. Files use an `Opt_` prefix
instead of `Fix_` to mark them as not-bug-fixes.

- **ClassicRockets** (D01, `Code/Opt_ClassicRockets.lua`) — a player-controlled rocket
  parked at the colony keeps its launch ration requested even with no destination selected,
  so drones refuel it while it waits. Only the fuel half of D01; the standing Rare Metals
  export half is deliberately unwritten (see the D01 entry).
- **AcknowledgedWarnings** (D02, `Code/Opt_AcknowledgedWarnings.lua`, added 2026-07-27) —
  dismissing "Building Not Working" acknowledges the listed buildings until they recover;
  new breakages always warn immediately. See the build-leg section above / D02 entry.
- **ResidencyControl** (D03, `Code/Opt_ResidencyControl.lua`, added 2026-07-27) —
  per-dome/habitat "closed to new residents" policy row; quarantine untouched. See the
  build-leg section above / D03 entry.
- **MultipleSuns** (D04, `Code/Opt_MultipleSuns.lua`, added 2026-07-27) — lifts the
  Artificial Sun build-once limit and carries the absorbed F39 panel-binding fix. See the
  build-leg section above / D04 entry.
  **This module is also where F56 would land** if the closed-`wontfix` auto-offload
  decision is ever reopened (user decision 2026-07-26): auto-offload and the export half
  are the same "rockets should load and unload themselves like they used to" request over
  the same machinery, so they ship together behind this one flag or not at all. Do not
  create an `Opt_AutoRocketOffload`.

## QA session (wave 3) — Fable, 2026-07-25 evening: A/B pair CLEAN, audits done

All four RunAll legs unattended via `-smrautorun` (Steam `-applaunch 3215050`); a
Python `luaparser` pre-pass first proved all 57 mod Lua files parse (no file-level
load failures possible). Logs in `%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|--------------------------|--------|
| Baseline (pack code list emptied) | 16.19.54 | 1 PASS, **38 FAIL**, 11 SKIP, 0 ERROR — every armed probe FAILs, all discriminate |
| Full pack | 16.22.38 | **39 PASS, 0 FAIL**, 11 SKIP — 46/47 active + ClassicRockets `inactive` (expected); found the ModLog `%` defect (below) |
| Opt-in (`SMRFixPack_Optional.ClassicRockets`) | 16.28.35 | **40 PASS, 0 FAIL**, 10 SKIP — ClassicRockets `applied`, its probe asserts; F69 chain intact |
| Final verification (default config, repairs in) | 16.31.30 | **39 PASS, 0 FAIL**, 11 SKIP, zero errors from our code |

(The ~49 `[LUA ERROR] Flight.lua objects_to_mark` blocks per leg are engine noise on
the synthetic map — present in the baseline too, not ours.)

**Defects found and repaired this session (all verified by the later legs):**
1. **HIGH — SaveSanitizer fixup race** (subagent audit, verified first-hand): pass moved
   `OnMsg.LoadGame` → `OnMsg.PostLoadGame`; see the F35 BUGS entry. Not probe-coverable
   (needs a real never-patched save — PT-35 case C).
2. **ModLog re-formats its message**: `ModPrint` is a printf-style `CreatePrint`
   (Mod.lua:109-113 + lib.lua:164-174), so a literal `%` in an already-formatted message
   raises `[LUA ERROR] string.format` — three per fixed leg (sanitizer "+100%" lines,
   TurbineBuff PASS line). All four log helpers now escape `%` for the second pass
   (fix pack 00_Core + 90_SaveSanitizer; TestKit 00_TestCore + 95_AutoRun, whose
   "ModLog is %-safe" comment was WRONG — corrected). **Engine-facts correction.**
3. **F35 amount now scaled** via `GetModifiablePropScale` (dormant hardening, matches
   Tech.lua:298-301).

**Spot-audits of the six highest-risk wave-3 divergences (subagent fan-out, each
verified against Src):** F59 CLEAN (ordering + assert-race claims true; recursion
bounded — homeless have `residence == false`), F71/F68 CLEAN (body diff exact; pcall
degrades to shipped alphabetical order; reorder provably cannot drop or starve a
resource), F72 CLEAN (strict pass-through; scan is an exact subset of
GetRocketsForExpedition incl. supply-pod exclusion), F54 CLEAN (full reason-state
enumeration found a FIFTH string `ExceptionalCircumstancesMalafunction` (sic) —
provably never admitted, malfunction forces GetWorkNotPossibleReason truthy), F34(d)
CLEAN (params table matches shipped; engine never mutates it; per-call dedup),
SaveSanitizer = the HIGH defect above, now repaired. Recurring minor: header/BUGS
line-number drift (off-by-ones, catalogued in the session transcript — cosmetic).

**Probe-discrimination sweep (Task 2):** ground truth from the pair — every armed
probe FAILed baseline and PASSed fixed except **F10 `FactionFundingCheck`**, which is
**fundamentally non-discriminating**: the baseline drove the shipped body over 240 nil
hours and it returned 0 — **this engine tolerates `pairs(nil)`** (new engine fact,
consistent with the `next(nil)` tolerance). F10's defect premise is falsified; entry
updated, probe PASS message now says "not evidence". Decision for the user below.
The rewritten F51 probe now discriminates (FAIL→PASS observed). 10 `[install]` probes
still SKIP on retail — the MarsDebug.exe pair remains the missing coverage.

**MarsDebug [install] pass (2026-07-26, attended) — FULL COVERAGE, 49 PASS / 0 FAIL /
0 ERROR** (1 SKIP = ClassicRockets opt-in, verified separately in the opt-in leg). Logs:
MarsDebug.exe-20260725-17.40.38 (baseline, installs SKIP — see below) and -17.46.04
(fixed, attended). All 10 `[install]` probes PASS with real verdicts, and **F73's Idle
pre-wrapper half is verified** ("Idle carries the shelter branch") — the last unverified
wiring in the pack. Install-probe baselines are FAIL-by-construction (they test function
provenance), so the attended fixed leg alone completes the coverage.
Three facts corrected/learned doing it:
- **The mod sandbox applies on ALL builds including MarsDebug.exe** — the wave-2
  assumption that an asserts build un-sandboxes mod code is WRONG. An asserts build
  unsandboxes the CONSOLE (g_ConsoleFENV reads real `_G`, console.lua:36-44), and
  `ConsoleExec` is on the ModEnvBlacklist (Mod.lua:1285), so the introspection bridge
  cannot be automated — it is typed: `SMRTest.EnableIntrospection(debug)` then
  `SMRTest.RunAll()`.
- The TestKit autorun now has a flag-gated **SetupOnly mode** (95_AutoRun +
  96_AutoRunFlag comment) that builds the colony and hands the session to the human —
  the attended-leg harness.
- **The debug build pops MODAL dialogs for asserts** — the first is the known vanilla
  `Flight.lua:465 objects_to_mark` noise; click **Ignore All** or the run blocks (and
  the 8-min watchdog can then expire; harmless, relaunch).

**D01/ClassicRockets (Task 4):** default-off / opt-on / no-spam claims all verified;
the no-spam citation in the Opt file pointed at the wrong file (the `arrival_loc`
gates live in the UniversalRocketBase override, UniversalRocket.lua:1687-1692) —
corrected; a third benign `Msg("RocketRefueled")` path via DroneUnloadResource is
now documented in the file. MOD_DESCRIPTION wording tightened so the module text
cannot be read as promising the unwritten Rare Metals half.

## QA session snapshot (Fable, 2026-07-25) — kept for the audit record

**NOTE — everything actionable below is RESOLVED:** the F53 and F12 reworks
LANDED (commits aa980e7 / 40d5a73) and survived the final A/B pair; the autorun
harness IS committed (TestKit); the RunAll pair HAS run clean — see the FINAL
A/B section above. Still open from this section: F68 capacity-cap in-game check,
F44 curve-ended track visual check, wave-1 heading tags.

- BUGS.md index was stale (16 wave-2 rows said `todo` despite tagged headings) —
  synced in commit 0ef4e7c. README/MOD_DESCRIPTION verified complete. Follow-up:
  wave-1 detail headings (F04/05/07/08/10/15/64) lack the `[fixed]` tag.
- Nothing was marked `blocked` in the build session. F55's "open-air entrance half
  not actionable" verdict was re-verified and is CORRECT (CalcOpenAirSkin only
  empties skin[2] configurable attaches; Dome_Entrance is entity-spot auto-attach
  data, Dome.lua:404 — not patchable from Lua). F55 drone half diffs clean.
- Spot-audit of 6 fixes (F61, F12, F44, F53, F68, F73) — full reports in the
  session transcript; summary:
  * **F53 CRITICAL — rework before release.** The `not IsInWalkingDist` gate in
    Fix_ArrivalDeaths.lua is always true for cross-map elevator destinations
    (IsInWalkingDistDome returns false when maps differ, Dome.lua:248-251), so
    every legitimate elevator arrival triggers the re-choose; the re-choose
    discards ChooseDome's elevator return and never clears stale
    self.emigration_elevator → TransportByFoot rides the stale elevator, fails
    the map-slot check (Colonist.lua:2731) → SetCommand("Abandoned"). Repair:
    skip the gate when ValidateBuilding(self.emigration_elevator) routes to
    dome; on re-choice take BOTH returns and assign emigration_elevator.
  * **F12 MODERATE — rework.** Post-wrapper leaves shipped dead branch removing
    the notification hourly, wrapper re-adds → destroy/recreate churn + FX replay
    every game hour while active; dismiss/suppression semantics differ. Docs
    prescribe full replacement — do that instead.
  * **F68 MODERATE — verify in-game.** The requested-floor (belt-and-braces
    block) doesn't debit hold capacity: with multiple exports, an alphabetically
    earlier resource's request can exceed remaining capacity → status stuck
    "loading", automode rocket sits on pad (departure gate needs "ready").
    Consider capping the floor against remaining capacity.
  * **F61 CLEAN**, **F44 CLEAN** (in-game check: curve-ended remainder track
    visuals; F45-comparator fold-in disclosed), **F73 CLEAN** (note:
    IsSuitable is AutoResolveMethods "and"-combined with Residence.IsSuitable —
    correct today, document it; partial-application isn't reported in the log).
  * Recurring minor: header/BUGS line-number drift (off-by-ones); apply()
    self-checks don't pre-check every runtime symbol.
- AccountStorage research (for the RunAll pair): enabled mods live in
  AccountStorage.LoadMods (plain array of metadata.lua `id` strings), persisted
  in `%AppData%\Surviving Mars Relaunched\<SteamID64>\account.dat` — an
  in-memory HPK (magic BPUL) containing `account.lua`, AES-encrypted+HMAC with
  key SHA256(GetAppId()..config.ProjectKey), compressed. BUT the loader is
  best-effort: a plaintext `return {...}` account.lua inside the container still
  loads (lib.lua:2187-2216). Edit only with the game closed; ids for missing/
  too-old mods are auto-stripped at menu (Mod.lua:2033-2059). Escape hatch:
  `AccountStorage.LoadAllMods = true` loads every discovered mod, bypassing the
  list. Unpacked mods in Mods\ need metadata.lua with `id` + `lua_revision` ≥
  350453. No Paradox cloud sync of account.dat (CloudSavesAllowed() = false).
- RunAll before/after pair NOT run: the Relaunched profile has never been created
  (%AppData%\Surviving Mars Relaunched\ has only Mods; no saves/logs/AccountStorage;
  no Steam userdata for appid 3215050) and mods can't be enabled until first launch.
  TestKit is now junctioned next to the fix pack. An opt-in autorun harness
  (TestKit Code\95_AutoRun.lua: flag-file gated, auto new game via
  NewGame/InitNewGameMissionParams/LoadLastNewGameSettings + fill g_CurrentMapParams
  + GenerateCurrentRandomMap, then RunAll with [SMRAUTO] markers, watchdog, quit())
  was being built when the session ended — it is NOT committed; check the TestKit
  repo before relying on it. Retail exe ignores -save/-map (goldmaster-gated,
  autorun.lua:126-144); Mars.exe launches directly, no external Paradox launcher.

## Parked by decision, not by effort — one entry left open (F48)

Each has a full write-up on its BUGS.md entry. None was parked for effort; each was parked
because the remedy is not a defect repair, or because the shipped code no longer matches
the tracker. **Only F48 is still open** — the other four are closed.

| ID | Why it is parked | What would unblock it |
|----|------------------|------------------------|
| **F56** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds as F62/F63.** Screened in the wave-4 build leg: the cited code is designed scope (`GetAutoGatherDeposits` is a declared accessor; the `Automation_Unload` rocket exclusion goes through the Relaunched `IsRocketClass` shim, i.e. maintained intent; auto mode promises only "gather resources"). **No standalone opt-in** — if revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten export half, never in an `Opt_AutoRocketOffload` of its own. | — done. Rides on whatever design decision D01's export half gets, or stays closed. |
| **F32** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** The shipped data already carries the fix (`NotWorkingBuildings` is now `Suppressable`); the other two presets are one-shot adds. The residual by-design annoyance (2-real-minute window, per-category suppression, no per-building ack) is spun out as **D02** — a planned `Opt_AcknowledgedWarnings` module, gated on **PT-38**; MOD_DESCRIPTION carries a player-facing "looks like a bug, isn't" explainer. | — done. D02 build belongs to a wave-4+ leg after PT-38. |
| **F42** | **NEW, wave-5 screening.** `blocked` — wontfix candidate. The tracked observation is entirely correct and does not add up to a defect: the guard it names exists to stop units being entombed, a dust devil has no footprint to be entombed in, the omission sits in declared overridable class members, no shipped text promises the block, and the game's one weather-gated placement rule (`RocketLandingDustStorm`) is implemented and working. Full write-up on the entry. | **A user decision.** Recommend `wontfix` on the F56/F62/F63 grounds. |
| **F48** | Mechanism confirmed, but the corrected call runs `OrderTrackElements`, which clears and rebuilds `el.connections` and rewrites `node_idx` on **every element of every track**, with a non-unwinding `assert` as its only failure handling. Too invasive to ship untested for a P3. | **PT-37** (added 2026-07-26) — exact console steps for the healthy-network + meteor-damaged-track test, on the user's in-person list. PASS → sanitizer behind a one-shot flag; FAIL → `wontfix`. |
| **F62** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** Verified identical to the original game (same one-hop algorithm, same two transitive-predicate callers): carried-forward dev vision in both games, breaks nothing. No opt-in module planned. | — done. |
| **F63** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds** — no training term ever existed in either game's emigration score. | — done. |

Recorded on those entries but deliberately untouched (real inconsistencies, no action):
walkability says A↔C is walkable while services say C is invisible from A;
`CanWorkTrainHereDomeCheck` permits training at a train-reachable school that
`ChooseTraining` never offers; the `PlanetaryAsteroidVisitPossible` legacy branch's
`and`/`or` precedence slip; `IsDifferentAsteroidLocation` comparing a map to a
MapDescriptor. All are permissive failures — none blocks a player.

## Wave 4 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**14 new fix modules, 13 new probes, 6 new playtest items (PT-39..PT-44).** Everything
lives on the `wave4` branch in `C:\Dev\SMR-BugFixPack-wave4` and
`C:\Dev\SMR-BugFixPack-TestKit-wave4`; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the wave-4 QA leg
(`docs/FABLE_QA_PROMPT.md`), which also performs the merge.

Implemented, in queue order:

| ID | Module | Note |
|----|--------|------|
| **F74** *(new)* | `Fix_RocketInteractGuard` | found by screening F56; the shipped guard at `RCTransport.lua:341` names only the pre-Relaunched trade/refugee classes |
| **F66** | `Fix_TrackConnectorPingPong` | enforces the invariant the shipped assert only states |
| **F65** | `Fix_TrackTunnelPowerBridge` | bridges only when the two stations demonstrably sit on different grids; PostLoadGame sweep |
| **F22** | `Fix_GridGlobalStorage` | one ratio over summed inputs instead of a sum of ratios plus a sentinel |
| **F75** *(new)* | `Fix_LastTransmissionStorage` | found by implementing F22; six conditions were on `Prerequisite`, which `Eval` never reads, and the Oxygen one measured Power |
| **F19** | `Fix_GraphConsumedCaption` | caption counts maintenance, like the bar |
| **F20** | `Fix_MoraleComfortTooltip` | hides the one row `UpdateMorale` no longer grants |
| **F21** | `Fix_TrainWaitTime` | full replacement — `BoardVehicle` blocks for the whole ride |
| **F23** | `Fix_FounderTraitNotification` | additive handler beside the dead one |
| **F24** | `Fix_DomePipeMoveInside` | `dome` → `self`; no probe, PT-44 covers it |
| **F27** | `Fix_StorageRateModifiers` | three post-wrappers |
| **F28** | `Fix_ReplaceTechCount` | entry title corrected: no crash is claimed, only that the line is wrong either way |
| **F29** | `Fix_SequenceLatents` | `fixed*` — items 1 and 3; item 2 is a Mod Editor code generator, deliberately left |
| **F18** | `Fix_IndependenceTerraforming` | `fixed*` — preset half; already-researched saves keep 10% |

**Screened and CLOSED `wontfix` (user decision 2026-07-26): F56.** Screening before
implementing found designed scope, not a defect — `GetAutoGatherDeposits` is a declared
accessor, the `Automation_Unload` rocket exclusion goes through the Relaunched
`IsRocketClass` shim (i.e. a developer consciously re-stated it for the new class tree),
and auto mode promises only "gather resources". Closed on the same grounds as F62/F63:
deliberately maintained design, breaks nothing. **No standalone opt-in is planned** — if it
is ever revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten Rare Metals
export half, not in a module of its own (same request, same machinery, and shipping them
apart would let a player enable emptying without refilling). Full write-up on both entries.

**Still `todo` after wave 4 — eight entries, the P2/P3 tail:** F25, F26, F31, F42, F43,
F47, F49, F57. ~~Suggested order for a wave-5 build leg~~ **All eight were taken in wave 5
— seven implemented, F42 screened to `blocked`. Nothing is `todo` any more.** The `fixed*`
partials whose open half is recorded on the entry are now: F15, F18, F29, F34, F49, F52,
F55, F57, F58, F59.

**Every wave-4 fix is unverified in-game.** The four full replacements (F66
`CreateConnectorElements`, F21 `BoardVehicle`, F24 `MoveInside`, F28 `ReplaceTech`) and the
one global-function replacement (F22 `GetGridGlobalStorage`) are the highest-risk items for
the QA audit; F20's per-call instance `GetProperty` override and F65's PostLoadGame sweep
are the two most unusual techniques in the pack and deserve a look.

## Wave 5 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**7 new fix modules, 7 new probes, 3 new playtest items (PT-45..PT-47).** Everything lives
on the `wave4` branch beside wave 4's; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the QA leg, which covers waves 4 and 5
together. **The BUGS.md `todo` queue is now empty.**

| ID | Module | Note |
|----|--------|------|
| **F47** | `Fix_TrackSalvageRefund` | sums every construction group's stamp instead of reading one; + partial-salvage refund |
| **F43** | `Fix_LayoutTechLock` | latent — no shipped layout has a tech-gated entry |
| **F49** | `Fix_TrainMinors` | `fixed*` — items (a) palette and (d) train cap; (b)(c)(e) screened, see the entry |
| **F57** | `Fix_DroneTransportMinors` | `fixed*` — (a) latent restrictor leak and (b) the unreachables table; (c) would undo F61 |
| **F31** | `Fix_AnomalyCaveInMap` | guards the argument, not the environment — the sketch's test would have killed marsquake cave-ins |
| **F25** | `Fix_TechDescriptionBuilding` | preset patch reusing the original translation id, so localised builds are untouched |
| **F26** | `Fix_BombardmentSpread` | the pack's **sixth and largest full replacement** (100 lines) |

**Screened items — both user decisions made 2026-07-25 (wave-4/5 QA session):**
- **F42** (buildings placeable on active dust devils) → **CLOSED `wontfix`** on the
  F56/F62/F63 grounds: the guard it names exists to stop units being *entombed*, a dust
  devil has no footprint and cannot be trapped, the omission is in declared overridable
  class members, and no shipped text promises the block.
- **F49(c)** (a salvage click on a station's connector hex reaches the station) →
  **user chose "the click does nothing"; IMPLEMENTED** in `Fix_TrainMinors.lua` as a
  demolish-mode pre-guard on `TrackGridElement:SelectionPropagate`.

**Every wave-5 fix is unverified in-game.** Highest-risk items for the QA audit, in order:
**F26** (100-line copy of `WaitBombard` — mechanically diffed against the shipped body,
identical apart from the function header, the dropped non-unwinding `assert`, and the one
`-- FIX:` line, but it replaces a whole disaster path); **F47's** partial-salvage wrapper on
`TrackGridElement:Demolish` (places resource stockpiles from a before/after snapshot);
**F49's** replacement of the global `ExpandTrackFromElement`; and **F43's** teardown of
live construction controllers inside a post-wrapper on `Activate`.

**New engine facts learned this leg (do not re-derive):**
- **Track is billed per construction GROUP, not per hex.** Groups hold at most
  `const.ConstructiongGridElementsGroupSize` = 5 elements (`_GameConst.lua:480`), and
  `Tracks.lua:463` leaves the leader's `construction_cost_multiplier` at 100 — one
  element's cost per group. Passages do it the other way (`Passage.lua:1969`).
- **`ConstructionGroupLeader:Complete` stamps the group's whole spend onto exactly ONE
  finished element** — the last it completed — after suppressing every member's own
  `MarkSpentResources` (`ConstructionSite.lua:2469`, `:2479-2489`). So
  `construction_cost_at_completion` is one stamp per group, spread along a track. This is
  what F47 turns on.
- **A T can be corrected without breaking translations** by rebuilding it with the SAME
  translation id: localised builds resolve the id and never see the literal, English builds
  fall back to it. Minting a fresh T would push English text into every language (F25).
- **`UndergroundMap` is a GameVar defaulting to `false`** (`RandomMapGenerator_Picard.lua:263`)
  and stays false under the "No Underground and Asteroids" rule — eight scenario call sites
  hand it straight to `TriggerCaveIn`, which indexes it unguarded (F31).
- **Verify every full replacement mechanically.** F26's 100-line copy was diffed against
  `ModTools\Src` with a throwaway Python script that strips comments and whitespace; it
  caught nothing this time, but it is the only way to be sure a copy that large is faithful.

## Key technical facts (hard-won, do not re-derive)

- **Mod code loads BEFORE the classes are built.** `autorun.lua:423` calls
  `ModsLoadCode()`; classes are assembled later in `OnMsg.Autorun`
  (`CommonLua\Core\classes.lua:980`). So at apply() time a class global is still
  its **classdef**, exposing only members the class declares ITSELF — an inherited
  method reads as nil. Two consequences:
  * `function Building:X() ... end` in a fix DOES propagate to every subclass
    (the classdef is what gets flattened later) — this is why class-method
    replacement works at all;
  * an apply() self-check must look for the method on its **declaring** class.
    Checking `Station.OnDemolish` (declared on Building), or
    `UniversalRocketBase.IsAutoModeEnabled` (declared on the AutoMode mixin),
    finds nil and silently deactivates the fix. F64 shipped broken this way and
  * **the flattening cuts BOTH ways at runtime (proven live 2026-07-28):** once
    classes are built, each class carries its own baked copy of every method —
    so a RUNTIME patch on a base class (console wrapper, TestKit logger toggle)
    is INVISIBLE to already-built derived classes. Live proof:
    `rawget(UniversalLanderRocket, "CreateAutoCargoRequest")` resolves to
    `Fix_LanderCargoRatchet.lua(124)` (the pack's pre-build replacement, baked
    in — the live lander RUNS the fix), while the TestKit `AutoCargo` logger's
    runtime wrap of `UniversalRocketBase` never fired across a full load cycle.
    Rule: pre-build (mod-load) patches on the declaring class propagate;
    runtime instrumentation must target the LEAF class the instances actually
    use (e.g. `UniversalLanderRocket`, not `UniversalRocketBase`). TestKit's
    AutoCargo logger needs the leaf-class repair (game-free item, queued).
    was corrected this session.
- `g_Consts` is a **GameVar** (`Lua\Modifiers.lua:427`) and does not exist while
  mods load — read it inside the patched function, never in apply(). `const` IS
  populated at that point.
- Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` (verified from working
  code paths) but NOT boolean relational compares — don't report/fix nil-iteration
  as crashes. `/` truncates (integer division); that is what makes F12's
  `a*24/v*24` unsatisfiable.
- **Mods run in a sandbox (LuaModEnv) on ALL platforms**, including unpacked dev
  mods (Mod.lua:1730/:1750; blacklist at :1267-1428). Key facts: `debug`, `io`,
  `package`, `lfs`, all `Async*` file ops, load/dofile/require are BLACKLISTED;
  `os` is `{time}` only; `setmetatable` is available (:1408 commented out);
  `rawget` is a safe wrapper that reaches real `_G` for non-blacklisted names —
  the pack's `rawget(_G, "X")` pattern works; `_G` maps to the env, but NEW
  globals created at load are rawset into the REAL `_G` (:1557-1563), so
  `SMRFixPack`/`SMRTest` are cross-mod and console visible; `Msg`/`OnMsg` are
  filtered only for persist/debug messages. The fix pack Code/ uses no
  blacklisted API (verified) — sandbox- and console-clean.
- **`error()` and `assert()` do NOT unwind mod code — they report and execution
  continues** with the next statement (LuaExports.lua:567 "asserts pop instead of
  being printed out"). Never use them for control flow; `pcall` still catches
  genuine runtime errors. Cost us four bogus FAILs and ten ERRORs in the first
  A/B pair (see the diagnosis section).
- **`rawset(_G, k, v)` from mod code writes only into the mod's own env table**
  (`_G` IS that table, Mod.lua:1603; `rawset` is the real rawset, only `rawget`
  is replaced at :1606). To write a global the game can see, assign it —
  `_G[k] = v` goes through `ModEnvMeta.__newindex` (:1557-1563) into the real
  `_G`. `rawget(_G, "X")` for READS is fine (safe_rawget falls through, :1577).
- **CORRECTION of an earlier "fact": `debug.getinfo` is NOT available in mod
  code** (debug is blacklisted). The Test Kit's install probes
  (00_TestCore.lua:37) break under the sandbox; repair in progress — bridge
  real `debug` via a console-exec path or SKIP install probes with a
  `SMRTest.debug = debug` console instruction. `GetStaticMsgNames()` (F06 probe)
  is a real global and still fine.
- Patch points that work: `PeriodicRepeatInfo[name]` slots (THREAD/SLEEP/FUNC/COND
  = 1..4, CommonLua\Core\lib.lua:1538+), `GlobalGameTimeThreadFuncs[name]` +
  `RestartGlobalGameTimeThread(name)` on LoadGame (Lua\Config\_fixup.lua),
  class-method replacement, chained wrappers, `OnMsg.*` additive handlers,
  preset/data patches at ClassesPostprocess.
- A post-wrapper on a **command** method (anything ending in `SetCommand`) never
  runs — `DoSetCommand` kills the calling thread. `Colonist:Idle` must be
  pre-wrapped (F73).
- Mod registry: every fix goes through `SMRFixPack.Register(id, {title, apply})`
  (Code/00_Core.lua); apply self-checks the target and returns a reason string to
  deactivate gracefully; `SMRFixPack_Disabled` = user veto; `SMRFixPack.ListFixes()`
  console status.
- All line numbers reference `ModTools\Src`; the game executes `Packs\Lua.fpk`
  (slightly newer date) — runtime self-checks in apply() are the guard.
  `GatherTransportableResources` (`ResourceTracking.lua:216`) is *called* but
  defined nowhere in Src — an engine export or an fpk-only function. F12's fix
  checks for it at apply time.
- Sample mod format in `<game>\ModTools\Samples\Mods`; docs in `ModTools\Docs\index.md.html`.
- **Replacing an EXISTING global from mod code works**: `ModEnvMeta.__newindex`
  (`Mod.lua:1557-1563`) rawsets any non-blacklisted key into the real `_G`, and the
  "attempt to create a new global" assert only fires for names that do not already
  exist there. Generated closures (script conditions, sequence code) resolve the name
  at call time, so they pick the replacement up. Read the name back with
  `rawget(_G, ...)` in apply() to confirm the write landed — F22 does.
- **`OnMsg` is additive, confirmed structurally**: four shipped files each define
  `OnMsg.StationsConnected` (`Station.lua:1213`, `Track.lua:668`,
  `TrainTransport.lua:357`, `UnderconstructionSign.lua:87`) and all four must run.
- **TOOLING: never round-trip a doc through PowerShell 5.1 `Get-Content -Raw` +
  `WriteAllText`.** `Get-Content` without `-Encoding` decodes UTF-8 files as cp1252, so
  every `—`, `↔`, `≤` comes back double-encoded and the whole file shows as changed.
  It happened to `BUGS.md` in the wave-4 session and was reversed with
  `Encoding.GetEncoding(1252).GetBytes(UTF8.GetString(bytes))`; nothing was committed
  corrupted. Use the editor's own file tools for docs, or pass `-Encoding UTF8` on
  BOTH ends.

## FINAL A/B RunAll pair (repaired TestKit) — CLEAN SWEEP (2026-07-25)

Re-run after the TestKit repairs (WithGlobals now writes real globals; sentinel
SKIPs; probe fixes). Logs: Mars.exe-20260725-14.17.33 (baseline) / -14.20.37
(fixed). **19/19 discriminating probes flipped FAIL→PASS; zero FAILs remain;
all 30 fixes `applied`.** Probe-verified fixes: F03, F04, F07, F08, F09, F11,
F13, F14, F15, F50, F51*, F52, F55, F58, F61, F67, F68, F69, F73, F06.
Not discriminated on a virgin colony: F10 (funding table non-nil → PASS both),
F51 probe PASSed both runs (cache re-evaluated even unfixed in this synthetic
scenario — probe may need a stricter setup). 10 [install] probes SKIP on retail
(sandbox); run the pair once under MarsDebug.exe for that coverage. F73's Idle
wrapper half also needs the debug-exe run (PASS was the IsSuitable half).
`tested` status remains reserved for scenario/manual verification per
TESTING.md — probe-verified ≠ full in-game scenario pass, but the wiring and
regression harness are now proven.

## Superseded: first pair (buggy TestKit) — kept for the record

Unattended harness works end-to-end (TestKit 95_AutoRun, `-smrautorun` via Steam
relaunch; Steam DRM blocks direct Mars.exe launch — bootstrap exits in 28ms).
Baseline = fix pack metadata `code` emptied; B = full pack. **All 30 fixes
report `applied`** (no inactive/error self-checks). Results:
- **FAIL→PASS (10):** UpgradeModifierLeak, TouristApplicants, LanderEmptyLaunch,
  LanderReturnFuel, RocketDroneChurn, StaleReservations, CrystalMysteryHang,
  TouristSatisfaction, TrainPlatformWedge, CommandCenterNumbers.
- **Applied but probe still FAILs (4) — diagnose fix-vs-probe:** WispPower (nil
  power units both runs), LanderCargoRatchet (request still drops to 0 with
  cargo aboard), HomeDomeMigrationGate (same fail text both runs),
  DomeOverviewHighlight (baseline "renders as 0", B "renders as table:0x…" —
  behavior changed, probe may mis-parse a T() value).
- **Probe/tooling casualties:** 10 [install] probes ERROR both runs — the
  no-introspection sentinel itself crashes (00_TestCore.lua:76 indexes nil
  'lib'); ShelterReflex ERROR in B (same crash via its wrapper check);
  VacuumWalks SKIP in B ("unexpected route value: unset").
- **Non-discriminating on a virgin colony:** FactionFundingCheck PASS both
  (funding table not nil on fresh game); NightShiftWork/WispResearch/
  ShuttleTransportCache/DroneUnreachableForever SKIP both (need colonists/
  mystery/shuttle state).
- Full logs: %AppData%\Surviving Mars Relaunched\logs\Mars.exe-20260725-13.56.49
  (baseline) and -13.58.35 (fixed).
- For [install] coverage: run the pair under MarsDebug.exe (console/asserts
  build un-sandboxes introspection; auto-bridge then fires).

### Diagnosis of the four "applied but still FAIL" probes — ALL FOUR FIXES ARE SOUND

Every one of the four was a Test Kit defect; **no fix pack code changed**. Two
engine facts (both now recorded in the Test Kit sources) explain all of them plus
the tooling casualties:

1. **`error()` does not unwind mod code.** It REPORTS (the `[LUA ERROR]` block
   with stack + locals) and execution continues with the next statement — the
   same treatment `assert` gets ("asserts pop instead of being printed out",
   LuaExports.lua:567). So `SourceOf`'s sentinel printed a stack and then ran the
   line it was guarding (00_TestCore.lua:76 → ERROR, not SKIP), and
   `WithGlobals`' `if not ok then error(res, 0) end` swallowed every error raised
   inside a probe's driven code — the probe carried on with a nil result and
   reported FAIL. Never use `error()` for control flow in mod code.
2. **`rawset(_G, k, v)` from mod code writes nothing the game can see.** In the
   sandbox `_G` IS the mod's own env table (Mod.lua:1603) and `rawset` is the
   real rawset (only `rawget` is replaced, :1606), so the Test Kit's fake globals
   were shadows in the Test Kit's env — invisible to shipped code (real `_G`) and
   to the fix pack (its own env). Plain assignment `_G[k] = v` goes through
   `ModEnvMeta.__newindex` (:1557-1563), which rawsets the REAL `_G`; that is the
   write a probe needs. **Every `WithGlobals` probe in the pair was therefore
   driving the real globals**, which is why the numbers looked absurd.

Per item, with the evidence that settled it:
- **WispPower (F07) — probe.** The fake `MainCity.labels.LightTrap` was invisible,
  so `SetLightTrapMode` iterated the live (empty) label and never called
  `el_prod_modifier:Change` → `granted` stayed nil in BOTH runs. The `* 1000` fix
  (Fix_WispRewards.lua:49) matches the sibling call sites exactly.
- **LanderCargoRatchet (F68) — probe.** The fixed method ran; the fake
  `GetTotalCargoAvailable` was invisible, so the real one crashed on the
  synthetic city (`[LUA ERROR] Lua/ResourceOverview.lua:30: attempt to call a nil
  value (method 'GetMap')`, raised from WithGlobals) and the swallowed error left
  `captured` nil → "request dropped to 0". The requested-floor block is intact
  and would have engaged (`is_on_automode_target_loc` true, `export_above.Metals`
  set, 300k aboard). The separate audit finding stands and is NOT this:
  the floor still does not debit hold capacity — verify in-game with multiple
  exports.
- **HomeDomeMigrationGate (F61) — probe.** Proof the fix worked: the fake global
  `ChooseWorkplace` was invisible, so the *real* one ran on the synthetic
  colonist and crashed (`Lua/Buildings/Workplace.lua:1095: attempt to index a nil
  value (local 'traits')`) — which it can only have been handed after
  `GetCommutableWorkplaces` produced the connected list, i.e. after the
  `accept_colonists` gate was gone. No fifth ungated call path is involved.
- **DomeOverviewHighlight (F14) — probe.** The fix is right and the shipped UI
  wants exactly what it now passes: a T value is a TABLE in this engine
  (`Untranslated(s)` → `T{s, untranslated = true}`, localization.lua:343) and the
  shipped sibling paths hand the same kind of table to the same `SetText`
  (ColonyControlCenter.lua:502-507). The probe `tostring()`ed it and saw
  `table: 0x…`; it now reads the literal out of the T.
- **VacuumWalks (F52) — probe** (same root cause; the fixed run's "unset" meant
  `SetCommand` was never reached because the real `GetDomesPassagePath` answered).

Test Kit repairs (repo `C:\Dev\SMR-BugFixPack-TestKit`): deferred-verdict
mechanism replacing the raise (657b668), WithGlobals write-through (413d87c),
F73 partial PASS (57139f5), F14 T reader (3f1abb4), F52 message (77fdb72),
AutoRun `wait_for` timeout (d2636b7), Meteors logger global swap (42d9f43).
**The A/B pair must be re-run** — with the fakes finally visible, several probes
that "passed" or SKIPped were not testing what they claimed.

## Waiting on the user

1. DONE 2026-07-25/26 — retail A/B pairs clean AND the MarsDebug [install] pass is
   complete (49 PASS / 0 FAIL, F73 fully verified — see the QA session section).
   **Automated + attended probe coverage is now 100%**; nothing further is owed to
   the harness. All that remains is the human playtest.
2. DONE 2026-07-26 — author set to **catt144** in both mods' metadata.lua.
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.
4. An in-game observation for F55: do drones still enter a dome after the roof is
   opened? The Lua half of that report turned out not to be actionable (see the
   F55 entry) — only play can tell us whether the entity data is at fault.
5. Manual playtest per `docs/PLAYTEST_CHECKLIST.md` (35 tests — PT-23..PT-35 are the
   wave-3 group 6; no third-party mods;
   covers what scripts can't: feel, visuals, UI, long-running behavior). Results
   reported back flip each covered fix's BUGS.md status to `tested` — see that
   file's "Reporting protocol" section for the exact follow-up workflow.
6. **All decisions made (2026-07-26).** F32 closed `wontfix` → D02 filed (planned
   `Opt_AcknowledgedWarnings`, gated on PT-38); F62/F63 closed `wontfix` (carried-forward
   design in both games, user decision); F10 retirement STAGED (46 modules / 45 active,
   final `wontfix` gated on PT-36; rollback is one metadata line); F48 rides on PT-37;
   TestKit stays local-only. Nothing is blocked on a decision anymore — only on play.
8. ~~TestKit remote~~ **DECIDED 2026-07-26: local-only, by design.** The kit was never
   meant to ship publicly, so no remote is created. Note the consequence: the repo's
   51 commits exist in exactly one place — if a local backup is ever wanted,
   `git -C C:\Dev\SMR-BugFixPack-TestKit bundle create <somewhere-else>\testkit.bundle --all`
   is the one-liner (a bundle is a single file that `git clone` accepts).
7. A donated save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture for the F35 sanitizer pass (PT-35 case C). Everything
   else about that pass is probe-covered.
10. **OPEN (2026-07-29): the F81 decision** — the rains disaster loop deadlocks
   permanently on an untimed `WaitMsg` the first time a rain roll collides with
   any active or predicted disaster (fully traced, static; explains the
   never-any-toxic-rain half of the F78 report). Fix = replace the global
   `RainsDisasterLoop` with a bounded wait + a one-shot LoadGame pass that
   recreates already-wedged activation threads. P1 for anyone terraforming.
   Build it, or leave it documented? (`CheatRainsDisaster` is a live workaround
   that also un-wedges the loop.)
9. **OPEN (2026-07-28): the F79 decision** — trains never carry service seekers
   (confirmed vanilla gap, entry has the fix sketch). Feature-completion D-item or
   leave as documented vanilla behavior? This is the only decision currently owed.
   (D07 was decided AND built 2026-07-28 — see the build-leg section.)

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need active repair; those passes now ship — eight in
their own fix files plus F03 and F35 in `Code/90_SaveSanitizer.lua`. Only F48
remains queued, and it is blocked on an in-game test (see the blocked table). ~15% is irreversible history (dead colonists,
lost expeditions; F64 voided trains have no recorded count — heuristic
compensation option at best, and document the vanilla train re-purchase at
stations, Station.lua:573-611). Save rescue is the headline differentiator vs
official patches ("new games only") — lead with it.

## Distribution facts (researched 2026-07-25, source-verified)

- BOTH Steam Workshop AND Paradox Mods are supported; the in-game Mod Editor has
  upload buttons for each (ModEditor.lua:78/:115). Steam Workshop reaches PC
  only; **Paradox Mods is the only channel that reaches Xbox/PS5** — platform
  fan-out is automatic on the backend, no platform fields, no modder-side
  signing (PS5 signatures are created client-side at install, Mod.lua:49-95).
  Console loads packed Lua code mods fine; no engine restriction found.
- PDX upload hard-requires: title, short_description (≤200 chars), description,
  preview image, lua_revision; last_changes on every update; ≤10 tags
  (ParadoxMods.lua:13-54, Mod.lua:410). GitHub repo link goes in metadata
  `external_links` — "github" is a supported LinkType shown on the PDX portal
  (Mod.lua:180-201). Default ignore_files already excludes *.git/*.
- Public repo: github.com/catt144/SMR-CommunityFixPack (main). Commit identity
  is the GitHub noreply address — never commit with a real email again.
- **CORRECTED 2026-07-26 (user unlocked one in play):** achievements are NOT
  disabled by mods on PC/Steam. `DoModsBlockAchievements()` returns
  `Platform.playstation or Platform.xbox or Platform.windows_store`
  (Achievement.lua:61-63) — the ModManager.lua:78 string is warning TEXT shown
  only behind that gate. Mods block achievements on console/MS Store ONLY.
  Separately, cheat use is logged per save (`LogCheatUsed` → persisted
  `CheatsUsed`, Network.lua:241-255) and adds "cheats used" to the
  unlock-refusal reasons on retail — so cheated fixture saves self-block their
  achievements. Mod description: say achievements keep working on PC, are
  disabled on consoles.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
Four `[DRAFT NOTE]` markers remain in `MOD_DESCRIPTION.md` (lines ~6, ~90 F76 explainer, ~390 ClassicRockets export half, ~448 final) and are
deleted before the text ships. The export-half one is load-bearing: do NOT promise the
ClassicRockets module's unwritten Rare Metals export half.
