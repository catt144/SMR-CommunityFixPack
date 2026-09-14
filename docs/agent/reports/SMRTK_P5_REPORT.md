# SMRTK P5 — layout stamper payload report

2026-09-13, Codex P5. **Numbered source/desk claims, no native stamp or game-play
claim.** No payload commit, removal, portal call, pack runtime edit, or version
edit. Coordinator owned metadata and both TestKit commit boundaries.

## Disagreements first / DRIFT

1. **EF-099 and the brief overstate the construction dry run.**
   `ConstructionSite.lua:2193–2250` has no `test` argument; passing a trailing
   true changes passability/flattening while still placing. The implemented
   building plan never invokes it. `BuildableGrid.lua:310–312` only classifies
   terrain; occupancy and rotated footprints need separate native queries.
   `Cheats.lua:55–104` completes **all** current-map construction, so the stamper
   completes only references returned by its own placers. These contradictions
   were sent upstream before implementation, and the coordinator is correcting
   EF-099 separately.
2. **A grid step is an edge, not one captured hex.** Cable
   `ElectricityGrid.lua:661–1154` and pipe
   `LifeSupportGrid.lua:940–1650` iterate `0..steps`; v1 uses `steps=1` only
   for two captured adjacent nodes, and `steps=0` for an isolated node. Their
   first result means “can build anything,” so every returned zero-based cell
   must also be clear. No input group is passed to a dry run: the leaf's
   `or input_constr_grp` path can clean a group even with `test=true`.
3. **Passage replay cannot be reconstructed from the specified bag of hexes.**
   `Passage.lua:1917–2275` needs scratch/entrance tables, ordered nodes,
   shared `input_data.passage_obj` and endpoint domes. V1 preserves inventory
   rows and logs explicit skips. It never calls the passage placer.
4. **Metadata order is not execution order across folders.**
   `Mod.lua:492–514` loads every non-`Code/` path before every `Code/` path,
   and discards returned tables. Layout files queue literal data under
   `SMRTK.layout_files[name]`; 77 validates after its API exists. A bare
   `return` or early `SMRTK.RegisterLayout` is insufficient.
5. **Two corrections to my own initial draft were retained.** I initially
   repeated a broad “getmetatable is blocked” claim; opening
   `Mod.lua:1578–1622` showed the environment's safe replacements at 1617/1619.
   The final normalizer uses `next/rawget`, copies only raw scalar schema
   fields into fresh tables, and does not inspect or preserve input metatables.
   Also a real-time waiter does not make GameInit run while paused:
   `CommonLua/Classes/_object.lua:187–195` schedules game-time threads.
   Stamping now requires a running game and bounds each init wait at three
   seconds; planning works paused.
6. **Logger and instrument corrections.** Core `T.Log` reserves `t` for
   game time, so the prompt's `STAMP_SKIP t=<template>` is emitted as
   `template=<template>`. A direct PowerShell `python -c` parse attempt lost
   embedded quotes and failed with Python SyntaxError; no code ran. The normal
   parsecheck rerun below succeeded. Initial broad source-output requests were
   truncated or included absent paths; narrowed successful reads supplied the
   cited routes. Those failed/partial searches were never negative gates.
   The first base had a parent-footprint recheck that could reject its own
   planned interiors, and returned an enclosing click FIRE success after an
   explicit capture refusal. Both were corrected; dedicated desk falsifiers
   now cover parent/interior and propagated rectangle refusal.
   **Late UI DRIFT after release of 77:** the page initially relied on
   `Text=L.name` inside `XTextEditor:new`. `PropertyObject.lua:1746–1751`
   only sets the metatable and runs Init; `XTextEditor.lua:171–175` resets
   `lines` to one empty string, and `GetText:221–228` reads those lines.
   `XControl.lua:624–634` supplies the required `SetText` route. Unlike
   ordinary `XText`, this class does not inherit `XTranslateText:Init` at
   `XControl.lua:534–536`. The coordinator applied the post-release correction,
   `editor:SetText(L.name)` immediately after construction, and owns the stricter
   merge fake that discards constructor Text. The 19 desk cases below did
   **not** model editor initialization and do not establish a rendering pass.

## Built and verified

7. **Format and capture built.** TestKit
   `Code/77_SMRTK_Stamper.lua`, `Layouts/README.md`, and pack
   `SMRTK_LAYOUT_FORMAT.md` define normalized v1 data, bounds, exclusions,
   file-queue loading and deterministic clipboard export. Capture is selected
   building/dome, two-click world rectangle, or current map; missing enclosing
   domes are dependency-closed before indexing. Limits are in code and format:
   512 buildings, 2048 grid nodes, 12 names, 1 MiB text, bounded coordinates.
   Over-cap capture refuses atomically. Existing names refuse rather than
   overwrite. LocalStorage persistence runs on a real-time thread and logs its
   separate actual writer result.
8. **Plan and bounded stamp built.** `Stamper.Normalize/Export/Resolve/Names/Plan`
   are reusable data APIs; mutation enters registry dispatch.
   `layout_plan` returns zero placements with per-row forecasts.
   Ordinary buildings use native full-shape gridded/ungridded obstruction
   queries plus terrain, level and parent checks. Domes complete before
   interiors. Ordinary new sites complete serially; native grid groups all
   complete with `quick_build_skip_done` before any owned member is removed.
   Existing sites never join that set. Save/load/map changes and engine error
   events stop subsequent mutations. Actual stamping is queued on one armed
   shared click, immediately releases that listener, and logs its final result
   inside the worker's registered action. Aborted work keeps ordinary game
   objects and reports partial counts, rather than promising a rollback.
9. **Optional state built as a second unit.** The coordinator committed the
   base as `5d5ea0e5a462c271336d79ffe81741a8cd099a7a`, and the loader README
   as `965fb0869caca2b84d0782bb5da3d909cbfcb30f`, before returning 77
   ownership for this unit. `layout_apply_upgrades` only walks the retained
   last-stamp building references; it checks each actual result.
   `ApplyUpgrade(tier,true)` was opened at `Building.lua:1131–1239` with
   `HasUpgrade:1349–1351`, `UpgradableBuilding.lua:155–157`, and
   `UpgradeUnlocks.lua:23–33`. The page discloses colony unlocks and enabled
   upgrade state; logs distinguish unlock requests from the post-call read.
   Separate buttons resolve `fill_storages()`, `spawn_colonists(10)`,
   `funding(500000000)` through P1's registry at invocation. Their direct P1
   routes were read before use; no World callback is called directly.
10. **Desk gates passed.** The harness tests the real core and payload against
    fake native services. Mutation bombs prove that the three clean plans do
    not place; adverse terrain/occupancy/blocked-cell cases make their matching
    predictions fail. It exercises cancellation, unrelated-site protection,
    grid completion order, refused captures, last-stamp upgrade ownership and
    dynamically registered World actions. It cannot execute the engine or
    establish real construction behavior. The fake point/grid model does not
    certify native geometry; the source's zero-based data and two-result
    contracts are explicit assumptions under test.

```text
$ python docs/agent/reports/SMRTK_P5_DESK.py
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=c467dfedcc3031f301b2af3c61f42483c6f9aced
PASS strict schema and fresh raw normalization
PASS deterministic literal export and round trip
PASS clean plan 1 ordinary building with zero mutation
PASS clean plan 2 dome and interior with zero mutation
PASS clean plan 3 flat grids: steps 1 has two captured nodes; isolated steps 0
PASS terrain truth cannot pass occupancy, loose objects, height or bad parent
PASS truthy line result with blocked second cell is rejected
PASS passages and suspended grids do not call a mutating or passage placer
PASS selected dome capture closes references and refuses name overwrite
PASS oversized whole-map capture is atomic
PASS rectangle uses two clicks, armed service and lifecycle teardown
PASS queued stamp dispatch owns only new sites and waits for its dome
PASS grid completion builds all owned groups before first removal
PASS paused stamp and cancelled queued work place nothing
PASS engine-reported non-unwinding error stops later mutations
PASS rectangle failure propagates and invalid names never acquire clicks
PASS upgrade state stays on retained buildings and declares colony unlocks
PASS save cancels queued state and invalidates previous stamp references
PASS World follow-ups resolve late, pass explicit amounts and retain refusals
P5 DESK: 19 contract falsifiers PASS; 3 clean synthetic plans; no native/game stamps run
```

```text
$ python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]
P5 NO SYNC: 0 lines
P5 NO BARE PRINT: 0 lines
PRESENCE CheatDef.lua: 26 lines
32:		"Code/77_SMRTK_Stamper.lua",
$ python tools/doccheck.py
doccheck: GREEN
```

Own negative gates: `rg -n 'NetSyncEvent|LogCheatUsed'` and
`rg -n '^\s*print\('` on 77. Presence side: same first expression on the
installed `Data/CheatDef.lua`. The counts above are emitted, not inferred
from an empty/error output. Metadata line 32 was added by the coordinator;
P5 requested only `"Code/77_SMRTK_Stamper.lua",`. No sample layout code file
was invented or silently added to metadata.

## Stopped / OWNER-ROUTED

11. **OWNER-ROUTED through 03B to ck175:** passage replay is stopped at the
    missing topology contract, with source lines in claim 3. Suspended spans,
    switches, special/map-specific buildings, spires and custom placement
    controllers have named skips in v1; the exhaustive implemented exclusion
    list is in the format and `excluded` array. This is a useful bounded v1,
    not complete colony duplication. 03B should judge the scope and costs;
    P5 made no owner-checklist edit.
12. **Unmeasured, not stopped by a desk PASS:** native X layout/rendering,
    native obstruction results, GameInit behavior, dome membership after
    completion, actual cable/pipe connections, no-taint for these new leaves,
    and the stamped colony's behavior all await 08. Eligibility still reports
    `UNAVAILABLE:sandbox`. There was no Mars.exe launch or game action.
    `tasklist /FI "IMAGENAME eq Mars.exe"` emitted
    `INFO: No tasks are running which match the specified criteria.`
    before Code writes.

## For 07 / sitting 08

13. **Button inventory:** Capture selected (`layout_capture_selected`);
    Capture rectangle (`layout_arm_rectangle`); Capture map
    (`layout_capture_map`); Next saved (`layout_next`); Copy layout
    (`layout_copy`); Cancel target / work (`layout_cancel`);
    Plan at click (`layout_arm_plan`); Stamp at click
    (`layout_arm_stamp`); Apply captured upgrades
    (`layout_upgrades_start`); Fill storages (all maps)
    (`layout_fill_storages`); Add 10 colonists
    (`layout_spawn_colonists`); Funding +500M (`layout_funding`).
    The name editor changes `layout_name`. Cancel remains usable even if
    that editor holds an invalid name. All live on the separate Stamper page
    in the shared 386-high scrolling host; actual fit/scroll awaits 08.
    `layout_target` uses only AcquireClick/ReleaseClick and requires Arm.
    Internal registry actions are `layout_register`,
    `layout_capture_rectangle`, `layout_plan`, `layout_stamp`,
    `layout_apply_upgrades`; raw data registration is
    `SMRTK.RegisterLayout(table)`.
14. **Suggested attended recipe, predictions before action.** Use the clean
    disposable branch required by 08. Identify a default-skin dome with
    ordinary interiors (exclude spires/custom objects), and a separate flat
    cable/pipe patch for the rectangle leg. The attending agent records
    capture counts from the actual CAPTURE line/clipboard before predicting
    the matching STAMP totals; do not invent counts from a screenshot.

    First-screen witnesses: CAPTURE summary plus copied literal layout;
    ARM then first rectangle FIRE without any capture; second FIRE produces
    CAPTURE and DISARM; PLAN summary with `placed=0`, and no new object;
    STAMP summary followed by visible new buildings and connected flat grids;
    state summary plus the upgrade/funding/resource/colonist observation.

    Pasteable starter block after selecting that dome:

```lua
SMRTK.Mark("P5_CAPTURE")
SMRTK.Run("layout_name","smrtk08_dome")
SMRTK.Run("layout_capture_selected")
SMRTK.Run("layout_arm_plan")
```

    Click an empty, level target. Require
    `SMRTK_STAMP_PLAN action=layout_plan mode=plan name=smrtk08_dome placed=0`
    with `skipped=0 status=OK`, `ready` matching the captured supported
    building count, and `PENDING_DOME` on each interior forecast.
    Resume the game before the next button; use the same target hex for
    `Stamp at click`. Require the primary
    `SMRTK_STAMP action=layout_stamp name=smrtk08_dome` with
    `left_sites=0 skipped=0 status=OK` and `placed/buildings` equal to the
    captured count. Inspect the new dome and interiors; counts alone cannot
    establish membership or functionality.

    Repeat capture/plan/stamp using the rectangle button and name
    `smrtk08_grids` around a flat connected cable/pipe patch, then inspect
    connection behavior. A deliberately included passage must yield
    `SMRTK_STAMP_SKIP ... template=passage` with the topology reason.
    A plan over the original occupied fixture must skip rather than mutate;
    a paused real stamp must REFUSE before any placement.
    Arm a rectangle then save/reload: expect DISARM and no retained target.
    If a built upgrade was captured, run its optional button only after
    inspecting the base stamp; check `STAMP_STATE` and the affected building.
    The World colonist button follows selected-dome/current-city rules; select
    the intended new dome before using it.

    After these operations, the evidence-copy block ends with CopySince:

```lua
SMRTK.TaintRead()
SMRTK.Run("eligibility")
SMRTK.CopySince("P5_CAPTURE")
```

    Prefer the panel Copy button if more console commands follow. Require
    `used=false`; eligibility remains unavailable. Native wrapper/taint
    searches against the archived boot are 99's responsibility.

    Timing: capture/plan/UI normal 5 s, abort at 15 s; a small stamp normal
    10 s, abort at 30 s. Each native GameInit wait has its own hard 3 s cap.
    Stop immediately on new taint, engine error, unexpected refusal, wrong
    map, or unexpected object mutation; do not repeat a mutation to obtain
    a preferred reading. Partial STAMP_STOP is an abort, not a PASS.

## DEPARTURES

15. Building planning substitutes explicit nonmutating queries for the nonexistent
    test argument. The second-unit gate is **three clean synthetic plans**, not
    three native stamps; the coordinator's base commit preserves unit ordering.
    03B must weigh that change, and 08 must supply the missing runtime evidence.
    Other explicit defaults changed: separate Stamper page; serial completion
    within ordered building phases; completion limited to new references;
    `steps=0` for an isolated grid node; passage inventory without replay;
    default-entity equality and conservative special-object exclusions;
    bounded schema/capture caps; early data queue for non-Code layouts;
    `template` log field instead of reserved `t`; explicit running-game
    prerequisite; name collision refusal; explicit World follow-up buttons.
    All preserve no-taint dispatch, one logger, idle zero patches, shared armed
    clicks, TestKit-only scope and owner-controlled game sittings.

## SUGGESTIONS

16. Add a v2 ordered route record for passages, with owning route identity,
    endpoint dome references and explicit entrance tests; do not infer topology
    from adjacent hexes. Retain one isolated-node and one branched cable/pipe
    fixture in the attended test library after they work in game.
    Capture variants/skins only with a versioned entity/skin contract; v1's
    equality refusal avoids manufacturing a different dome footprint.
    Consider a future native construction-controller read adapter if 08 shows
    conservative fit refusals are costly, but never call a mutating “test”
    boolean or attach a live cursor controller during idle.

## Doccheck warnings, verbatim

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
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
  WARN  M Code/77_SMRTK_Stamper.lua
  WARN  M Code/90_Loggers.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/76_SMRTK_Kit.lua
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

These are the emitted shared-tree warnings at the report's gate, including peer
files. P5 did not edit those peers or route their in-progress work as a P5 defect.
