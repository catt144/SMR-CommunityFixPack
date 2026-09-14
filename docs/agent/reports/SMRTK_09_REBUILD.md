# SMRTK 09 — architecture build and source trace

2026-09-14. **BUILD + DESK COMPLETE; PLAY NOT RUN.** Pack input `8a2dca2`; TestKit
`d9f8fb1` (capture identity and mutation evidence), `9057fb6` (task controls and More filter).
Installed source: 1.1.0.403908, Steam build 24995074. No game launch. Requirement (A)
was witnessed by 08 on the previous surface; it has **no current-surface verdict**.

## Disagreements and recommendation

**Stamper: retain only as experimental until the three native examples in 08b. Do not
expand it.** The owner's removal licence is authority, recorded in ck183. Source and
synthetic fixtures do not establish that the feature is hopeless, but its recovery is
fragile: placement and GameInit are deferred, interior placement depends on a completed
parent, grids depend on native group completion, and an interrupted partial placement
has no rollback. A disposable save is its recovery boundary. The UI now says this.

Recommend removal if 08b shows systemic placement/connection failures on supported flat
fixtures, source-object mutation, or repeatable partial failures that cannot be diagnosed
from the log and safely recovered by reload. An isolated repairable defect is different
evidence. If the owner prefers to retire it before that test, this build supplies no claim
against that choice: drop the class-18 blocks and still run the changed-surface acceptance.
Do not spend further owner time on expanding a feature that has not placed one native object.

**Defect 7 is PARTIAL.** Actual shipped `ConsoleLog` is font size 13; vanilla Cheats is
18. The prompt's request to shrink the former while remaining larger than the latter
cannot be fulfilled literally. Toolkit controls use proportional size 20, compact height
26 and automatic-width wrapping instead of 146/296-wide rows. Density is source-built;
font size did not shrink. Visual acceptance and any revised typography ruling belong to
08b/ck183. No desk fixture can certify readable density or screen fit.

## Numbered claims by strand

1. **A — task grouping.** Eight pages: Sitting, Run, Selected, Agent, World, Saves, Kit,
   Stamper. Run holds run-until, all four triggers and the shared field editor/watch;
   Selected holds selection dump, capture, pins, field watch and colonist traits. Agent
   holds slots and notes. The shared hot bar holds status, MARK, Flush + copy, Clear screen,
   Screenshot + Mark, Stop disaster, pause and five speed constants, and Cancel target.
   Fixed controls precede each page's scrolling readout. Falsifier: load real modules and
   construct each page with `python docs/agent/reports/SMRTK_09_DESK.py`.
2. **A — attachment and input ownership.** One text SMR XButton toggles the panel, with
   clean/unknown/tainted colour. It attaches idempotently to HUDMiddle/idMiddleList (HList);
   fallback is a sibling of idBottom. No popout remains. The armed owner ID, label and
   right-click-map escape appear in the hot bar and an independent closed-panel HUD notice.
   Disabled captions/backgrounds propagate. Clear screen/readout affects presentation;
   the ring and file remain evidence. Falsifier: the same script checks both parent routes,
   toggle, banner, clearing, disabled captions and teardown. Real layout is still owed.
3. **B — truthful mutation.** All twelve spawn variants report `spawn_dispatched`, before
   and same-tick counts, with deferred GameInit/census verification; they no longer refuse
   after dispatch. Invalid inputs still refuse before mutation. Repair/malfunction share
   actual before/after malfunction and maintenance fields; unchanged calls do not count
   as changed. Core logs a failed callback with `ctx.mutated` as ERROR/mutated, rather than
   REFUSED. Stamper marks the mutation boundary before native placement/upgrade calls;
   a partial failure is incomplete and blocks follow-ups. No rollback was invented.
4. **B — identity and native dispatch.** Every Stamper template lookup uses template_name
   or class, including validation, skipping, sorting, export and upgrades. Exact meteor
   passes fourth argument true; scattered single/storm remains separate and native storm
   movement is retained. Cursor meteor refuses non-main surfaces because native disaster
   code uses MainCity. The click capture releases exclusive input before queued game-time
   mutation. Five speed labels match 1/3/5/20/128. Logged target TRIGGER ends run-until
   immediately even when that trigger has paused its game-time polling thread.
5. **B — arrivals.** World-wide `rocket_arrive` iterates deduplicated city labels, including
   detached inbound rockets. It requires UniversalRocketBase, our_colony, a live transit
   sleep thread and future arrival time; pods, paused flights and other destinations are
   excluded. It skips remaining transit and wakes the native flight; orbit/landing waits
   remain native. No selected in-flight object or picker is required. Falsifier: the desk
   fixture includes detached labels, duplicate references, pods, directions and pause.
6. **B — outbound cost, NOT BUILT.** Earth completion consumes fuel, emits RocketReachedEarth,
   tourist rewards and cargo funding (`Data/FlightPolicyDef.lua:349+`). Asteroid completion
   changes map/rocket state (199+); project completion invokes project effects and may
   consume the rocket (616+). Anomaly/rival paths also need their own route and fixtures.
   Widening means tracing five additional destinations and native completion cases, then
   native tests for each; it is not a predicate edit. Relabelled inbound scope is explicit.
7. **C — trace and filter.** Concurrent payload completed all 84 More names, all declaring
   overrides: 18 keep, 7 cut, 59 needs-rollover; 97 explicit More bodies out of 150 explicit
   Cheat/Async bodies. No source-name delta or current Cheat/Async suffix collision.
   Coordinator re-ran its executable census and applied the policy at both walk and
   dispatch. Unknown future names fail closed. Empty Deposit.CheatRefill and
   SupplyPodBase.CheatRefuel are omitted only by exact function identity; overrides remain.
   Full body citations, caveats and executable inventory: [SMRTK_09_MORE_TRACE.md](SMRTK_09_MORE_TRACE.md).
   The payload's reference to "class-11 More" is a class-number error: predictions 7/8
   cover More; prediction 11 covers speeds/run-until. Exposure does not prove behavior.

## Every defect's disposition

| 08 defect | strand | disposition in this build; native acceptance remains 08b |
|---|---|---|
| 1 | A | Dock moved out of idBottom; HList primary, Box sibling fallback. Screen geometry unproved. |
| 2 | A | Old hidden-window space claim becomes moot with the new parent/toggle. |
| 3 | A | One SMR button opens/closes the whole panel; popout removed. |
| 4 | A | HUDMiddle/idMiddleList built; sibling fallback desk-tested. |
| 5 | A | Delete unit/rubble caveat retained in its rollover. |
| 6 | A | Clear above growing readouts; presentation clears preserve ring/file and new verdicts can return. |
| 7 | A | PARTIAL: compact auto-width rows built; font-premise disagreement above, visual decision pending. |
| 8 | A | Disabled background and caption colour implemented; native rendering pending. |
| 9 | A | Kit is Probes & logs; Run all probes/Run selected probe explicitly labelled. |
| 10 | A | One shared field editor/watch workflow on Run/Selected; arm disabled until configured. |
| 11 | B | Print tee arm/disarm surfaced on Kit; paired ownership unchanged. |
| 12 | B | Exact fourth-argument meteor plus separately labelled scattered modes. |
| 13 | A | Controls fixed above scroll readouts on every page. |
| 14 | record | Superseded by 15; no separate speed-caption patch. |
| 15 | B | Explicit 1x,3x,5x,20x,128x; pause/resume separate. |
| 16 | C | All 84 traced; seven global cuts and two exact receiver omissions; 59 caveats implemented. |
| 17 | record | Inspect worked in 08; blanket prediction of retail failure withdrawn. Other helpers remain unproved. |
| 18 | B | Complete buildings + wires/pipes vs Complete wires/pipes only. |
| 19 | B | Common actual-state changed basis with unchanged count; repeat repair fixture yields zero changed. |
| 20 | A | Armed owner label/ID, right-click-map escape and Cancel target visible, including panel closed. |
| 21 | B | All template reads audited and fallback built; class-only dome/interior capture desk-tested. |
| 22 | B | All twelve spawn variants truthfully report dispatch/deferred census; premutation refusal retained. |
| 23 | B | Skip remaining transit (inbound); outbound costed above and HELD, not built. |
| 24 | record | Attendee pod/rocket drift corrected by UniversalRocketBase guard; agent-owned 80 unchanged. |
| 25 | B | Finish all in-transit arrivals, world-wide; selection dependency dissolved. |

## More dispositions — complete names

The lists below are the executable trace partition, rather than a runtime button census.
Retained source-union exposure after seven global cuts is 77 More / 10 async, with 59
named rollovers. Conditional exact-receiver omissions can reduce a selected object's list.
See the trace table for each declaring body, reason, dependencies and limitation.

**Keep (18):** `CheatAddSolOnMars`, `CheatAge1Year`, `CheatBreak`, `CheatDespawn`, `CheatDrainBattery`, `CheatEmptyFood`, `CheatFeed`, `CheatFillConsumptionRes`, `CheatFillElectronics`, `CheatFillRecipeInputs`, `CheatKill`, `CheatMakeEarthsick`, `CheatMakeRenegade`, `CheatRechargeBattery`, `CheatRemove`, `CheatRemoveDustRC`, `CheatStarve`, `CheatUnfreeze`.

**Cut (7):** `AsyncCheatDebugger`, `AsyncCheatScreenshot`, `CheatBreakTrack`, `CheatMeteorHit`, `CheatPrintRequests`, `CheatSpawnLinkedUndergroundPassage`, `CheatTransformUnderground`.

**Needs rollover (59):** `AsyncCheatClassHierarchy`, `AsyncCheatClipPlane`, `AsyncCheatCollision`, `AsyncCheatGizmo`, `AsyncCheatInspect`, `AsyncCheatMarker`, `AsyncCheatPassTypeRange`, `AsyncCheatProperties`, `AsyncCheatShowGrid`, `AsyncCheatSpots`, `CheatAddProgressPoints`, `CheatAddTouristTrait`, `CheatAllowExploration`, `CheatAllowSalvage`, `CheatBreakElement`, `CheatClearAsteroids`, `CheatClearCooldowns`, `CheatCompleteTraining`, `CheatDeliverResources`, `CheatEmptyStorage`, `CheatExpand`, `CheatFillFood`, `CheatGenerateDepartures`, `CheatGenerateOffer`, `CheatLaunch`, `CheatLightningStrike`, `CheatLowConsumption`, `CheatMakeSphereTarget`, `CheatNoConsumption`, `CheatQuickRefab`, `CheatRefill`, `CheatRefuel`, `CheatRepair`, `CheatResetShowProgress`, `CheatScan`, `CheatShoot`, `CheatShowGridBBox`, `CheatSpawnAndroid`, `CheatSpawnCat`, `CheatSpawnDeer`, `CheatSpawnDog`, `CheatSpawnDustDevil`, `CheatSpawnGoat`, `CheatSpawnLlama`, `CheatSpawnPenguin`, `CheatSpawnPony`, `CheatSpawnRabbit`, `CheatSpawnTrain`, `CheatStartLiftoff`, `CheatStressedOut`, `CheatToggleWaterGrid`, `CheatTransformAsteroid`, `CheatTransformSurface`, `CheatTriggerAsteroidLocked`, `CheatTriggerAsteroidMystery`, `CheatTriggerAsteroidUnlocked`, `CheatTriggerDiscovery`, `CheatTriggerEvent`, `CheatUnlockAsteroids`.

## Verification and practical limits

`python docs/agent/reports/SMRTK_09_DESK.py` at pack `8a2dca2` / TestKit `9057fb6`
passed real-module page construction, twelve spawn variants, repair idempotence, rocket
scope, exact/scattered arguments, source-union policy, receiver identity, sibling depot
before/after counts and partial-mutation evidence. Existing P5's 19 failure fixtures and
three synthetic plans remain PASS. Class-only placed dome/interior capture also passed.
The Python file is the reproducible report support instrument, not shipped infrastructure.

Gates emitted by that command: **nine files; sync/taint calls 0; bare prints 0; logger 1;
tag sink 1; positive source presence 26 lines**. C's fenced recheck separately emitted
13 actual preset calls, partition 18/7/59 and no current suffix collisions. Parsecheck:
34 TestKit Lua files, zero errors (Lua 5.5). Doccheck: GREEN, clean TestKit tree.

Idle write audit: persistent UI adds listeners and toolkit-owned classes/TextStyle, not
replacement vanilla functions. Print tee remains an explicit `_G.print` install paired
with restore; quiet wrappers remain paired arms. ConsoleEnabled remains the existing
explicit arm route. No new SMRTest.Register was added. The synthetic lifecycle checks
cover cleanup but cannot certify native idle ownership, taint or eligibility after this
build. 08b owns those readings; 02's unchanged console kill gate is not rerun here.

Native fit, font/density, all long rows, deferred colonist counts, meteor impact location,
rocket landing behavior, actual dome membership, connected grids, upgrades, after-taint
and final zero arms are **NOT RUN**. No More body is play-proven by source existence.

## DEPARTURES

- Typography resolves contradictory raw sizes with proportional 20/compact geometry;
  defect 7 remains partial rather than silently claiming a smaller font. Owner decision
  routed below. Native XButton text provides SMR identification without a new bitmap asset.
- Report-support Python added to make real-module synthetic evidence reproducible.
- Failed post-placement callbacks now carry ERROR/mutated and incomplete-stamp guards;
  this extends the spawn truthfulness repair to the same invariant at Stamper boundaries.
- Run-until listens to toolkit TRIGGER records to avoid deadlocking on a trigger that
  pauses game-time polling. No vanilla function wrapper was introduced.
- More uses a reviewed-name policy around the dynamic walk; future unreviewed names
  refuse. This enforces the trace's no-sync boundary when installed source changes.

## SUGGESTIONS

- Freeze Stamper scope. Score recovery and usefulness alongside native placement in 08b;
  remove it on the systemic-failure criteria above. If only connected-grid replay fails,
  the owner may prefer a smaller building-only tool; do not expand or silently downgrade.
- Outbound flight skip needs distinct completion cases, not a broad destination guard.
  Current inbound action should be compared with ultra speed on a real waiting flight.
- Preserve the 59 source-qualified More caveats. Neither a retained name nor a nominal
  dispatch should be advertised as completed mutation.

## DRIFT for 99

- Synthetic UI double initially lacked AsyncRand/SetTextColor; fixed the fixture, not
  the game. A compact default initially overrode the explicit 52-pixel dock size; code
  review found and fixed it before commit. Gates re-ran on final bytes.
- Actual shipped font sizes refute the prompt's shrink premise; no visual PASS inherited.
- Dynamic walk's inherited suffix dedup is structurally weak, but current source census
  contains zero Cheat/Async collisions. No current capacity defect or stop condition found.
- C's table and complete partition are the trace evidence; its class-number typo is
  corrected above. Inspector retail/achievement blanket predictions are not evidence.
- Aliascheck's order/probes/last UNKNOWN findings are false positives against the nested
  initialization in `00_TestCore.lua:18-22`. They are reported verbatim below, not repaired
  by changing working globals or weakening the gate.

## OWNER-ROUTED and out-of-scope filings

- **OWNER-ROUTED → orchestrator/ck183:** defect-7 font/density decision at first native
  contact; Stamper experimental retention/removal recommendation and criteria above.
  The owner's removal licence is already in ck183; no new permission requested here.
- **OWNER-ROUTED → orchestrator/STATE:** replace the spent 09/old-surface pointers with
  this report and 08b. STATE write scope was not added: no new probe registration/count.
- **FILED SOURCE CONCERNS → 99 triage:** linked underground passage omits required city;
  BreakTrack uses unsafe fixed indices; SpawnTrain consumes queued state. These are named
  body findings in the C report, not verified vanilla defects; no pack/game body changed.
- **SOURCE CORRECTION → 99/fact maintainer:** GED app opening alone is not the declared
  achievement blocker. ModEditor/GedModManager/editor map/testModGame are named by the
  source checks; GedInspector/GedObjectEditor/GedMarkerViewer require actual runtime
  eligibility readings. Retain 08's Inspect witness, avoid generalizing it to all helpers.

08b's inbox names every changed class/verdict, including old block-1 PASS. 99 gets this
outbox. Prompt 09 is consumed in the documentation commit; pack pushes, TestKit stays local.

## Doccheck warnings — verbatim close-out summary

```text
  warn F59: the frozen index-row cell says 'fixed*', entry says 'tested-attended' (from 'tag')
  warn F85: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C12: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C13: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C14: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C15: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C16: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C17: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C37: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C35: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C34: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C38: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C39: the frozen index-row cell says 'filed', entry says 'tested-unattended' (from 'tag')
  warn F100: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C43: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C49: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C50: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C51: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C52: the frozen index-row cell says 'filed', entry says 'parked' (from 'tag')
STATE + STUBS: STATE.md 12689 bytes (warn 15360 TEMPORARY, hard 18432, line 200); 3 stubs present and pointing
  ⏳ STATE warn is TEMPORARILY raised +25% (12288 → 15360) by owner ruling 2026-09-14, checklist 178, for the duration of the doc overhaul. Restore: set STATE_WARN_TEMPORARY = False in this file. ⛔ Owner's word only — no agent retires this on its own judgement.
MARKER INTEGRITY: 94 on disk, 94 parsed; WARN
  warn duplicate ck:144 at lines 3205, 3279 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
PUSH SET: 41433 B in 5 file(s) ≈ 19k tokens (budget 40960 B)  ⚠ OVER
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
```

The warnings above are retained verbatim. No warning was promoted to a new play result.

