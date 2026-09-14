# SMRTK full sitting — predictions before 08

2026-09-14, Codex 07. **As built, not as tested.** Game build 24995074;
TestKit runtime `f093e3baa86c014ec822e96238081ab5ddd77a35` (README-only successor
`c886fb7`). Pack input `25acafe`; documentation unit `f78d7a8`.
03B's PASS WITH FIXES and 03C's Selected extension are upstream claims;
the P5 desk instrument was rerun against these trees. No launch in 07.

## Scoring and aborts

Each numbered prediction describes a **button class**, not every button.
All record signatures below have the prefix `[SMRTK] SMRTK_` and suffix
`t=<live GameTime> id=<monotonic record id>`. These angle-bracket fields,
object handles, session nonces, selected intensity and captured counts are
runtime values, not owner-pasted placeholders. Compare fields independent
of logger sort order. Count one primary result **per distinct dispatch**;
MARK, persistence, queued STAMP, provenance and post-action taint assertions
are separate evidence. Trigger firing logs TRIGGER, not generic FIRE.

Ordinary UI/action result: normal 5 s, abort 15 s. Small stamp: normal 10 s,
abort 30 s, with native GameInit's separate hard 3 s per-object bound. Native
save/load: normal 60 s, abort 180 s after loading-screen transition begins.
Short trigger/run-until: normal 10 s, abort 30 s. Probe suite: normal 120 s,
abort 360 s; a progress line is not a completed suite. Stop immediately on
new taint, engine error, wrong map, unexpected refusal or unexpected mutation.
The intentional negative controls below are exceptions only for their named
REFUSED result. Do not repeat a mutation to improve the verdict. Abort means
archive partial evidence and report the missing class, never silently pass it.

## Numbered class predictions

1. **Navigation/chrome:** MENU (`dock_menu`/`dock_submenu`), TAB (`dock_page`
   or `tab_<page>`), PANEL (`panel_toggle`/`dock_close_panel`) and COLLAPSE
   (`panel_collapse`) have `status=OK`. First screen: dock menu, each of Sitting,
   Selected, World, Agent, Saves, Kit, Stamper; fixed status/common row remains
   when collapsed. Long More labels/scrolling and infopanel attachment are
   screen measurements owed to 08, not inferred from registry presence.
2. **Evidence:** MARK `action=mark label=SMRTK08_BEGIN status=OK`; COPY
   `action=copy status=OK`; FLUSH `action=flush status=OK`; CLEAR `action=clear
   status=OK`. First screen: clipboard pasted into a desktop text viewer contains
   the mark and later toolkit records; F9 clears the overlay without erasing
   the file/ring. The COPY result itself is logged after clipboard assembly.
3. **Console:** CONSOLE_CONTROL `action=console_control discriminates=true
   negative=false positive=true status=OK`, with SHORTCUT `console=false`
   then `console=true`. CONSOLE `action=console_open status=OK` opens input.
   Mod Manager/GED closed and Platform.cheats unset are required controls.
   First screen: Enter reopens after the control. Passive auto-open is not proof.
4. **Status:** TAINT_READ `action=taint_read used=false status=OK`; ELIGIBILITY
   `action=eligibility reason=UNAVAILABLE:sandbox status=OK`. First screen:
   CLEAN and unavailable are separate. End read of CheatsUsed must be empty;
   any TAINT record or newly populated entry aborts. A debug editor can transiently
   block eligibility without taint; close it, never relabel unavailable as OK.
5. **Curated selected mutations:** ACTION `action=selected_fill method=CheatFill
   status=OK` with before/after/resource discriminator on a supported depot;
   `selected_empty` returns its own after amount. Single-resource uses one
   storable resource; universal uses the total, never StorageDepot.resource.
   `selected_clean_fix`, `selected_malfunction`, `selected_add_prefab`, supported
   spawn/maintenance/dust/upgrade rows use ACTION with method/valid_after.
   First screen: selected scratch object's state changes. Busy mechanized depot
   Fill/Empty REFUSED is conditional, not required fixture coverage.
6. **Removal/destruction:** ACTION `action=selected_delete method=CheatDelete
   status=OK valid_after=false`; ACTION `action=selected_destroy method=CheatDestroy
   status=OK` reports its actual valid_after. First screen: one sacrificial
   building disappears, another follows vanilla destruction/rubble behavior.
   Do not predict Destroy invalidates every class immediately.
7. **More Cheat:** SELECTED `action=selected_more method=CheatKill category=Cheat
   status=OK` on a sacrificial colonist and corresponding CheatDespawn on a
   sacrificial drone. First screen: death/despawn and taint stays CLEAN. Dispatcher
   return does not prove any leaf's deferred work completed. Source-name capacity
   is 106/106, never a simultaneous-button census.
8. **More AsyncCheat/refusal:** SELECTED `action=selected_more method=AsyncCheatInspect
   category=AsyncCheat status=OK` if supported; first screen: inspect/editor or
   explicit retail limitation. Stale expected object gives SELECTED
   `action=selected_more status=REFUSED reason="selection changed; choose the action again"`
   and touches neither old nor new object. An unsupported inspector is UNAVAILABLE,
   not PASS or an invented successful retail-debug claim.
9. **World direct/amount/list actions:** DISASTER `action=cold_wave status=OK
   outcome=leaf_dispatched`; DISASTER_STOP `action=stop_disaster outcome=stop_requested
   status=OK`. ACTION for funding_plus, tech_points_1, applicants_50,
   spawn_colonists_1, trait_add/trait_remove, fix_all, complete_constructions and
   complete_grids has the callback's amount/count/outcome fields. First screen:
   chosen amount/trait/state and disaster notification, followed by stopping it.
   Test one of each direct, numeric preset, picker, spawn, repair and completion
   subclass; unvisited disasters/traits/research are not individually covered.
10. **World cursor/quiet:** ARM `action=meteor_single status=OK`; FIRE
    `action=meteor_single outcome=leaf_dispatched status=OK` with chosen position,
    then DISARM. First screen: one target at an empty scratch area. Quiet ARM/
    DISARM `action=quiet status=OK` owns/restores its captured wrappers. Quiet
    with DustDevils logger conflict refuses; never nest them from the console.
11. **Speed/run-until:** SPEED `action=speed_normal status=OK`, and pause/resume
    reflects the visible clock. ARM `action=run_until status=OK target=smrtk08_break`;
    FIRE `action=run_until paused=true status=OK`, then DISARM when the custom
    trigger fires. First screen: clock advances then stops; restore normal.
12. **Agent slots/pins/note:** ACTION `action=slot_1 status=OK` or the sitting's
    named once slot; PIN `action=pin_A status=OK`; NOTE `action=note status=OK`.
    ARM/FIRE/DISARM `action=slot_4 status=OK` for a read-only map click, correct
    fire count, right-click cancellation. First screen: plain labels, pin refs,
    note and fire counter. Every prepared leg supplies MARK/DUMP/MARK evidence.
13. **Triggers/watch:** ARM `action=smrtk08_break status=OK`; TRIGGER
    `action=smrtk08_break status=OK trigger=smrtk08_break`, then DISARM once.
    WATCH `action=watch_field armed=false status=OK`; explicit ARM/DISARM
    `action=watch_selected_field` controls polling. First screen: trigger row
    changes and run-until pauses. Field watch observes a scalar change when
    the fixture supplies one; missed intermediate values are outside its promise.
14. **Screenshot:** MARK `action=screenshot_mark status=OK` records the native
    screenshot result/path. First screen: open that exact image after capture
    and confirm it depicts the marked scene. API acceptance alone is not evidence
    that an image exists. Inspect screenshot fields before scoring.
15. **Saves/provenance:** SAVE `action=save_A slot=A status=OK`; LOAD
    `action=load_A slot=A status=OK` in the same session, and PROVENANCE
    `present=true` with saved session/attempt/last-record fields. Intentional
    foreign guard: LOAD `action=load_A status=REFUSED reason="foreign session: ..."`
    with colony unchanged, then LOAD_OVERRIDE `action=load_override_A slot=A
    override=true status=OK`. First screen: loaded colony, full status and
    provenance; every arm gone, pins cleared. 08 uses a temporary toolkit nonce
    mismatch and restores it, avoiding a second boot or save-header mutation.
16. **Kit probe gate:** before attestation RUNALL `action=run_all status=REFUSED
    reason="desktop probe sweep not provisioned for this sitting"`. After a real
    desktop sweep PROBE_PREFLIGHT `action=probe_preflight clean=true status=OK`;
    PROBE `action=run_probe status=OK` carries a named verdict, and RUNALL
    `action=run_all status=OK` carries completed counts. Probe FAIL/ERROR by name
    is evidence to triage, not a toolkit gate failure by itself; no suite totals
    predicted from a VOID baseline. First screen: disabled before preflight,
    verdict colours afterwards. Load/map change expires the attestation.
17. **Kit observation toggles/views:** ARM/DISARM `action=logger_DustDevils` and
    `action=print_tee` restore ownership; FINGERPRINT, DUMP, SNAPSHOT and DIFF
    for their named actions have `status=OK`. Two snapshots before diff;
    funding between them supplies a known delta. First screen: ring tail/error
    counter, selected dump and snapshot delta; no idle vanilla wrappers persist.
18. **Capture/layout target/plan/stamp/state:** CAPTURE `action=layout_capture_selected`
    or `layout_capture_rectangle/map status=OK` gives buildings/grid/skipped;
    LAYOUT_PERSIST separately confirms persistence; LAYOUT_COPY/SELECT/NAME have
    their named OK results. LAYOUT_TARGET → ARM/FIRE/DISARM `layout_target`
    starts capture/plan/stamp; first rectangle click does not finish capture.
    STAMP_PLAN `action=layout_plan mode=plan placed=0 ready=R skipped=S status=OK`
    freezes the numeric forecast before mutation. STAMP `action=layout_stamp
    placed=R skipped=S left_sites=0 status=OK` is the successful native prediction
    at the same unchanged target; **buildings/grid totals must also match**.
    PENDING_DOME forecasts demand actual completed parent/member inspection.
    A paused stamp must REFUSE without placement; occupied plan skips with zero
    mutation. STAMP_STATE_QUEUE precedes STAMP_STATE for Apply captured upgrades;
    compare built upgrade state on retained objects and colony unlock disclosure.
    STAMP_FOLLOWUP resolves separate World actions; do not infer follow-up mutation
    from queue acknowledgement. LAYOUT_CANCEL/right-click/save removes targets.

## Stamp forecast — executable desk counts, native counts still owed

This reruns the **existing** P5 harness and emits its three zero-mutation
fixtures through the actual registry. It writes no code and launches no game.
The synthetic templates/hexes are not an owner colony placement recipe.

```python
import runpy
ns = runpy.run_path('docs/agent/reports/SMRTK_P5_DESK.py')
lua = ns['lua']
lua.execute('''
local fixtures = {
  {name='desk_ordinary', buildings={building()}, grid={}},
  {name='desk_dome', buildings={building('DomeBasic'),building('Habitat',1,0,1)}, grid={}},
  {name='desk_grids', buildings={}, grid={{k='cable',dq=0,dr=0},{k='cable',dq=1,dr=0},{k='pipe',dq=4,dr=0}}}
}
forecast_lines = {}
for _, f in ipairs(fixtures) do
  reset_world(); prohibit_mutation=true
  local b=base(f.name); b.buildings=f.buildings; b.grid=f.grid
  LocalStorage.smrtk_layouts[f.name]=b
  local ok, result=SMRTK.Run('layout_plan',f.name,20,20)
  assert(ok and result.placed==0 and result.skipped==0 and mutations==0)
  forecast_lines[#forecast_lines+1]=logs[#logs]
end
''')
for line in lua.globals().forecast_lines.values():
    print(line)
```

Expected desk results: ordinary plan placed **0**, ready **1**, skipped **0**;
dome/interior placed **0**, ready **2**, skipped **0**; two adjacent cables plus
one isolated pipe placed **0**, ready **3**, skipped **0**. Native successful
replay predictions for these shapes would be placed **1/2/3**, skipped **0**,
left_sites **0** respectively; that is a prediction, not a native measurement.

Emitted by the fenced instrument at pack `f78d7a8294a2e03a263a81c21507f21627c12105`
and TestKit `c886fb7049cf50a149938f9515eae78d039af33b`:

```text
[SMRTK] SMRTK_STAMP_PLAN action=layout_plan mode=plan name=desk_ordinary placed=0 ready=1 skipped=0 status=OK t=400 id=58
[SMRTK] SMRTK_STAMP_PLAN action=layout_plan mode=plan name=desk_dome placed=0 ready=2 skipped=0 status=OK t=400 id=61
[SMRTK] SMRTK_STAMP_PLAN action=layout_plan mode=plan name=desk_grids placed=0 ready=3 skipped=0 status=OK t=400 id=65
```

For the actual 08 fixture, select one ordinary depot for stamp 1, a dome with
at least one supported interior for stamp 2, and a flat connected cable/pipe
patch for stamp 3. Capture/plan counts are **not known before inspecting the
colony**. The attendee records each capture and the target's numeric R/S,
buildings/grid counts into the sitting report **before** clicking Stamp at the
same hex. Plan may skip excluded/blocked rows; either score those names or move
to a clean target and re-plan before any mutation. No target/capture change
may reuse a prior forecast. Inspect native fit, GameInit completion, dome
membership, cable/pipe connectivity and a captured built upgrade as distinct
witnesses. Missing fixture state is NOT RUN, never inferred from totals.

## DEPARTURES and SUGGESTIONS for 99

Verification summary (07, pack `f78d7a8`, TestKit `c886fb7`): doccheck GREEN;
03C's executable recheck emitted 106 source names, 22 curated/84 More and
12 async, P2/03C desk PASS; P5 desk PASS and the three counts above; 08's
17 individual console lines compiled with zero errors and no placeholders
or inline comments, without execution. Rule 6 = 0 across 9 toolkit files;
rule 7 = 0; installed source presence = 26 lines / 13 actual calls.

- 07 documents 03C's result, including conditional AddDustRC omission, rather
  than 03B's historical 22-name coverage. No runtime/slot/template edit in 07;
  08's attendee preloads 80 via the standing prompt before the owner starts.
- Foreign-session control changes/restores only SMRTK.session temporarily,
  intentionally refuses once, then exercises explicit Override in the same
  boot. It tests the real comparison, not process-nonce regeneration on restart.
- Native stamp totals are frozen from capture/plan before placement; exact
  source-only desk totals do not invent a census of the owner's colony.
- Final CopySince retains the numeric opening mark: 70's string lookup accepts
  only the current mark label. Later MARKs and screenshots replace it. If the
  bounded ring reports truncated=true, the whole-sitting audit uses the archived
  full boot log. Upstream P5's old-label CopySince recipe is historical drift.
- More labels are raw method suffixes and require retail editor/debug knowledge.
  Consider plain rollovers explaining effects/retail prerequisites after 08.
- Separate captured geometry, upgrade state and colony-wide follow-ups are hard
  to explain briefly. Keep their actual scopes visible on the buttons; consider
  an affected-object count before colony-wide follow-ups in a later build.
- The 00 bootstrap inversion remains owed to a code link (03B ruled it,
  neither applied it nor authorised 07's docs fence to change infrastructure).
  FIX_POLICY is untouched: toolkit documentation is not fix policy.

## Doccheck warnings - verbatim close-out summary

`python tools/doccheck.py`: GREEN at pack `f78d7a8`, TestKit `c886fb7`;
existing report-only warnings follow. No index/checklist/alias repair in 07.

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
STATE + STUBS: STATE.md 12191 bytes (warn 15360 TEMPORARY, hard 18432, line 200); 3 stubs present and pointing
  ⏳ STATE warn is TEMPORARILY raised +25% (12288 → 15360) by owner ruling 2026-09-14, checklist 178, for the duration of the doc overhaul. Restore: set STATE_WARN_TEMPORARY = False in this file. ⛔ Owner's word only — no agent retires this on its own judgement.
MARKER INTEGRITY: 88 on disk, 88 parsed; WARN
  warn duplicate ck:144 at lines 2733, 2807 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
```
