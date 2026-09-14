# SMRTK 03A - fan-out build report

2026-09-13, Codex coordinator. **Build complete for Claude 03B review. No page,
native save/load round trip, disaster effect or native stamp is claimed in play.**
Installed source build: 24995074. The 02 final PASS/outbox is the upstream
authority; 08 remains the first full page sitting. TestKit commit ids and exact
command output are emitted below, including every doccheck warning.

## Disagreements first

No payload failed the coordinator's required parse/safety/H-10/doccheck gate,
so no gate re-fire was needed. Passing those gates proves syntax, lexical
exclusions, registration and desktop consistency. It does not prove native
behavior or a leaf's entire transitive route. Payload reports remain claims.
The following claims were corrected during the build:

- **Late native editor discovery:** constructor Text does not initialize
  XTextEditor lines. Post-release setters now initialize World/Kit/Stamper;
  Agent already did so. Three stricter integration counterfeits go RED.
  Details and source routes are claim11 below.

- **Construction dry-run:** EF-099/briefs supplied a nonexistent building
  `test` parameter. `ConstructionSite.lua:2193-2250` still places; trailing
  booleans affect passability/flattening. `BuildableGrid.lua:310-312` is terrain
  classification, not complete fit. `Cheats.lua:55-104` completes unrelated
  current-map construction. Coordinator opened those sources and amended
  EF-099: plan uses nonmutating queries; stamp completes its own new references.
- **Grid/topology:** native loops include both endpoints (`0..steps`), and a
  truthy line result does not certify every cell. Passage ownership, ordered
  nodes and endpoint domes are absent from the original bag-of-hexes schema.
  P5 handles flat cables/pipes, preserves passage inventory and skips replay.
- **Mod loading/helpers:** non-Code paths execute before Code paths regardless
  of mixed metadata order (`Mod.lua:492-514`). Layout files queue data early.
  P5's initial blacklist-only getmetatable claim, which I adopted and relayed,
  was too broad: the environment explicitly installs safe_getmetatable and
  safe_rawget at :1578-1622. Both relays were corrected; normalization uses raw
  fields and fresh tables, without preserving metatable behavior.
- **Selected semantics:** CheatDelete has class overrides: tracks demolish,
  rubble clears. P2 uses honest Delete wording. Add maintenance is the actual
  CheatAddMaintenancePnts; rover dust uses CheatAddDustRC. Busy mechanized
  depot operations refuse because animation callbacks defer their mutation.
- **Agent:** literal `do =` is invalid Lua; use `["do"]`. Frozen Fire emits
  FIRE, so polling triggers enter guarded Run for a TRIGGER result. Screenshot
  native nil/false means accepted; it is not a witnessed file or pixel result.
  The first game-time screenshot draft failed its meaningful falsifier and
  was corrected to guarded real-time effects with stale-arm cancellation.
- **Saves/Kit:** display-name-only SaveGame creates unique files, so slots use
  explicit native savename. LoadMetadataCallback calls DoneGame; the guard
  uses Savegame.Load with the read-only LoadMetadata helper instead. Registry
  counters mean callback attempts, and provenance's last record can be a
  lifecycle/auxiliary record. False method results are preserved explicitly.
- **Shared panel:** my earlier scrolling claim lacked VScroll configuration.
  Native XScroll.lua:564,686,714 requires a resolving scrollbar. The final
  frame has an IdNode and sibling XSleekScroll, and all seven tabs fit its
  logical width. Saves status is sanitized/capped at 48 characters in the
  shared strip; the full refusal remains on Saves and in its result.
- **Upstream drift:** the 02 sitting report's old no-game header/todo conflicts
  with its final PASS and outbox. The final authority controls; no sitting was
  repeated. Three synthetic clean plans gate P5's second unit, not three
  native stamps. This changed default is explicit and awaits 03B judgment.

## Numbered, falsifiable coordinator claims

1. **Spike preceded every launch.** `git show --stat 8d1a6aa` reproduces the
   committed shared routes and all five populated inboxes. Infopanel injection
   uses DialogOpen; map targeting uses one exclusive armed TerminalTarget;
   dock menus use native XPopupMenu. Stateful pages use the owner's approved
   fixed side-panel rung. Rejected routes and source lines are in
   [SMRTK_UI_HOOKS.md](SMRTK_UI_HOOKS.md).
2. **Core/panel extensions are separate committed units.** Reproduce with
   `python docs/agent/reports/SMRTK_FANOUT_SMOKE.py`. Chrome records still reach
   file/ring but skip ConsolePrint; CLEAR leaves the cleared screen empty.
   All three restore messages produce only an actual create/show record.
   SaveGameStart disarms, click ownership is exclusive and UI clicks bypass
   it. The post-record contract is independently exercised by claim9.
   The complete 03A diff is copied below.
3. **P1 World is built and independently desk-verified.** Reproduce with
   `python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest --list`. All seven
   assigned units exist, with 55 registered World actions. Quiet's seven
   initiation gates capture/restore originals, preserve running stacks and
   refuse logger nesting. Counterfeit quiet cleanup and stale clicks go RED.
   Disasters report leaf dispatch, quiet reports held starts. Modern rocket
   travel completion reaches ordinary arrival policy/orbit, with bounded
   observation and explicit legacy/unready/paused/foreign-destination refusal.
   Run-until observes trigger callback attempts, including failed attempts.
   **Stopped:** native effects, quiet provocation, speed and rocket witnesses
   await 08. Full unit claims/routes: [P1 report](SMRTK_P1_REPORT.md).
4. **P2 Selected and dock are built and independently desk-verified.**
   Reproduce with `python docs/agent/reports/SMRTK_P2_SMOKE.py`. There are 21
   selected leaf actions plus four dynamic companion ids; objects show
   supported subsets. Message injection is idempotent and ordered, selection
   races refuse, named-host fallback builds Selected. Dock always shows taint,
   unavailable eligibility, arms and errors; its menus include only complete
   argument contracts and execute inside real-time threads. **Stopped:**
   native focus, IdNode registration, icon placement and size await 03B/08.
   Full claims/routes: [P2 report](SMRTK_P2_REPORT.md).
5. **P3 Agent and idle template are built and independently desk-verified.**
   Reproduce with `python docs/agent/reports/SMRTK_P3_SMOKE.py`. Six slots plus
   BindScratch preserve the legacy binding route; new contexts include
   sel/pin/cursor/mark/log. Pins clear on load/map, notes use one NOTE, native
   screenshot+mark uses one MARK with capture_id/path. Triggers poll in game
   time and enter Run inside guarded real-time effect threads; scalar watches
   preserve nil/false and never retarget. Queued effects/clicks and yielded
   screenshots cancel stale arms on lifecycle transitions. The entire
   80_AgentSlots file is commented and neither binds nor arms on load.
   **Stopped:** native timing, focus and screenshot files await 08.
   Full claims/template: [P3 report](SMRTK_P3_REPORT.md).
6. **P4 Saves/Kit and the authorized accessor are independently verified.**
   Reproduce with `python docs/agent/reports/SMRTK_P4_SMOKE.py`. Fixed A/B/C
   native names, process-session guard, explicit override, metadata errors,
   yielding-operation locks and provenance are modeled. Probes default-refuse
   until an explicit sitting/build/registry-bound desktop attestation; the mod
   cannot inspect desktop source or verify the attestor. Logger installation
   ownership is captured, manual arms are not adopted, quiet layering refuses.
   Dump preserves false, snapshots are detached/scoped/bounded, watch_field
   registers a disarmed P3 trigger, console uses only the settled console arm.
   Fingerprint reads live loaded ModDef/public registry, not ListFixes output.
   Exactly seven additive lines expose a copied LoggerState from 90.
   **Stopped:** native save/load/console and scoped reads await 08.
   Full claims/preflight contract: [P4 report](SMRTK_P4_REPORT.md).
7. **P5 base and optional state are independently verified in two units.**
   Reproduce with `python docs/agent/reports/SMRTK_P5_DESK.py`. Nineteen contract
   falsifiers pass, including three zero-mutation synthetic plans. Capture
   closes enclosing-dome dependencies and refuses caps/name collisions
   atomically; normalization/export use fresh bounded v1 data. Replay orders
   domes/interiors, uses owned-site completion, checks every line cell, refuses
   pause and bounds initialization waits. Cancellation/errors stop later
   mutation; partial objects remain and counts disclose that boundary.
   State visits retained last-stamp references only; upgrade logs distinguish
   unlock requests from actual reads. Fill/spawn/funding are separate late
   World dispatches. **Stopped:** passage topology, special controllers,
   suspended grids, nondefault skins and native geometry/behavior are not
   supported or witnessed. [P5 report](SMRTK_P5_REPORT.md) and
   [format contract](SMRTK_LAYOUT_FORMAT.md) list exact scope/exclusions.
8. **Required per-file gates were run by the coordinator before each commit.**
   Reproduce with `python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered`.
   The exact parsecheck runtime, no-sync and bare-print checks each pass;
   every toolkit file is actually in ModDef.code (H-10); doccheck is GREEN.
   Presence is 26 source lines and is copied once in the baseline evidence.
   Every per-file command/output, function inventory and warning is copied
   below. The directory CLI sweep also passes. No payload report supplies
   the coordinator's gate evidence.
9. **The complete toolkit co-loads in the actual metadata order in a desk
   model and every cross-id resolves.** Reproduce with
   `python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest`. P2 Dump -> dump_selected;
   Pins -> pin_A/B/C; P4 watch -> P3 TriggerField/watch_selected_field;
   P5 follow-ups -> fill_storages/spawn_colonists/funding. **No final page or
   cross-id is stubbed.** Both MARK routes invoke fingerprint after primary
   evidence, refused MARK does not, and recursion/error controls remain
   bounded/visible. Actual 90 Meteors and quiet refuse nesting in both orders;
   manual logger state is preserved. All seven advanced builders share one
   body with resolving scrollbar; tabs are bounded and save refusal appears
   in the strip. The model reuses P3's service setup, not its assertions;
   actual 70-77/80/90 implementations are loaded together. Other legacy TestKit
   files are parsed in order, not executed as probes by this check.
10. **Scope and commit hygiene are explicit.** The emitted commit map below
    lists sequential file+metadata pathspec commits in TestKit. Root owns
    metadata; no per-file metadata commit introduces another uncommitted
    payload file. Core was extended before launches and after all file releases,
    never during parallel payload ownership. No pack Code/items/metadata or
    mod version changed. Foreign CHECKLIST_ARCHIVE edits remain outside this
    commit. Reproduce scope with `git -C ../SMR-BugFixPack-TestKit diff
    5d8d3b3 HEAD --stat` and inspect the pack close-out commit's pathspecs.

11. **Native editor initialization was corrected after all payload releases.**
    Reproduce with `python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest`.
    P5 late review and coordinator source reads established XTextEditor.Init
    clears its buffer (:171-175), GetText reads lines (:221-228), and
    XControl XEditableText.SetText (:624-634) initializes it. Root added
    explicit setters in World/Kit/Stamper; P3 already used the correct helper.
    The stricter fake ignores constructor Text. Removing each correction
    independently gives its specific editor-default RED. The earlier19 P5
    tests did not model editors. Ordinary XText labels use XTranslateText
    initialization and require no correction. No shared core change was needed.

## Commit-and-verify units

- [x] Upstream spike/inboxes before launch; pre-launch core and panel.
- [x] P1 World; P2 section/dock; P3 Agent and slot template, one file per commit.
- [x] P4 Saves, Kit and authorized read-only 90 accessor, one file per commit.
- [x] P5 base, loader README and explicit state follow-up, sequential boundaries.
- [x] Post-release core hook and shared panel, one file per commit.
- [x] Ordered parse, complete co-load, all cross-ids and meaningful desk checks.
- [x] Post-release World, Kit, Stamper native editor corrections, one-file gates/commits.
- [x] Last-wave P1/P4 inboxes preserved in pack commit before their consumption.
- [ ] Successor/audit inboxes, consumed briefs/03A, row strike, doccheck/push.

## DEPARTURES - defaults changed, invariants retained

- The owner's revised surface adds a third spike technique. Dock/section use
  rung 1; stateful pages use the approved fixed side panel. The lettered SMR
  XButton avoids the index-sensitive HUDButtonFrame. A visible dock read
  survives closed menus/panel; the old floating surface is demoted/starts
  closed. A dedicated Stamper page and a small Sitting safety body are added.
- Expanded P2 was re-seated Astra/xhigh from Sol/high; P3 Astra/xhigh and P5
  Astra/max retain their assigned seats; P1/P4 Sol/high. Five payloads ran
  in waves within three child slots. Primary coordinator uses the inherited
  Codex seat; no tool emitted an exact primary model identifier. Claude 03B
  and Fable 99 retain the independent vendor check.
- A shared armed listener replaces temporary vanilla method wrapping.
  Native menus use explicit complete-argument opt-ins. Central metadata
  ownership removes shared writes; sequential commits list only that file.
- Per-file parse uses parsecheck.runtime because the CLI accepts directories,
  with a whole-tree CLI sweep also run. Checked-in gate/smoke/merge artifacts
  make the evidence reproducible; they do not execute native game probes.
- Display policy, actual-restore logging, save-start disarm, post-record
  evidence hook, resolving vertical scrollbar, seven bounded tabs and capped
  save-status strip extend the inherited core/panel between ownership waves.
- Honest Delete wording and busy-depot refusal replace false vanish/deferred
  success promises. Quiet delays scheduler entry instead of stopping running
  disasters; ARM/DISARM/FIRE retain one primary record each. Quiet/logger
  mutual exclusion prevents stale captured-wrapper restoration. Rocket waits
  finish to ordinary arrival policy and refuse unsupported legacy cases.
- Scratch has its own BindScratch; legacy options remain supported. Trigger
  Run preserves the TRIGGER verb; real-time effects preserve native screenshot
  threading. Repeating levels use rising edges; scalar watches refuse aliases.
  Screenshot capture_id/path is separate from the ring mark. `["do"]` is Lua.
- SaveGame uses deterministic savename; metadata guard uses the read helper
  instead of the destructive full-load callback. Probe hygiene is an explicit
  desktop attestation that expires per sitting/build/order. Public registry
  reads replace printing-only ListFixes. Provenance is attempt/record history;
  snapshots are scoped, detached and bounded. The tiny 90 accessor is additive.
- P5 replaces nonexistent building dry-run flags with explicit fit queries;
  three synthetic plans gate the second unit. Completion is serial/owned;
  steps=0 represents an isolated grid node. Passage inventory is preserved
  without replay. Bounds/exclusions, default entity checks, early data queue,
  running-game prerequisite, reserved template log key and explicit World
  follow-ups are stated in the format. No automatic state/funding/spawn occurs.
- EF-099 amendments file verified source corrections and retain status;
  generated fact index is regenerated, not hand-edited. No status is promoted
  from a source reading or desk PASS.

Every departure was checked against no sync/taint wrappers, one primary
tagged result through SMRTK.Log, zero idle vanilla function patches, armed
cleanup, shared click ownership, TestKit-only scope and owner-owned sittings.
Native no-taint of new routes still requires the independent review/sitting.

## OWNER-ROUTED - recommendations for 03B's single ck175 append

1. Accept the hybrid surface/lettered icon, honest Delete caveat and 48-character
   Saves strip read provisionally; use 08 to assess native dock placement,
   section/body size, input focus and scrolling. Keep eligibility unavailable
   alongside taint as already ruled; no clean read proves eligibility.
2. Retain quiet's scheduler delays and modern selected-rocket travel completion
   with ordinary operator landing policy. Provoke each quiet entry while a
   prior disaster is active; test rapid re-arm and save/load. Keep unsupported
   legacy/foreign flights visible, and manual logger arms operator-owned.
3. Recommend run-until pause on any target trigger attempt for operator review.
   If success-only is required, settle a successful-fire signal before 07;
   T.fires alone cannot provide it. Scalar-only fixed-target watches and
   game-time polling remain documented limits. Error triggers count
   notifications, not unique exceptions. A screenshot native acceptance needs
   an opened capture file in 08.
4. Retain default-refusing probes and compile exact desktop sweep/head/output/
   explicitly needed probe evidence into sitting-owned slots. Use a disposable
   current-branch fixture for save/load, and STOP on denied metadata, wedged
   native load or missing console. 03B owns the suggested legacy 00 bootstrap
   retirement. No wider console enable or runtime manual file parsing.
5. Accept scoped/bounded snapshots; verify on two loaded maps. Defer whole-colony
   aggregation until needed, with explicit per-map totals and source basis.
6. Accept bounded Stamper v1 with flat grids and named special-object skips;
   passage replay remains held for a versioned ownership/order/endpoint
   contract. Judge the synthetic-plan second-unit gate explicitly. 08 must
   witness native fit, GameInit, dome membership, connected grids and upgrade
   state. Keep partial objects/counts on abort; no rollback or complete colony
   duplication promise. Document capture caps and name collision refusal.

These merge every payload OWNER-ROUTED recommendation. 03B adds its own
agree/disagree recommendation and makes ONE owner-checklist append; 03A makes
no scattered owner request or checklist edit.

## DRIFT - retain for 99

- Late native editor correction and the three stricter counterfeits are in
  claim11. The first refreshed P1 smoke lacked a fake SetText method and
  failed; its fake now implements the setter and discards constructor Text.
  A preconsume doccheck capture printed non-ASCII under cp1252 and failed
  after saving full GREEN output; the saved output was read under UTF-8.
  Final child evidence capture explicitly uses PYTHONIOENCODING=utf-8.


All corrected claim/source contradictions are listed first above. Other
procedural corrections, none counted as successful negative evidence:

- Wrong prediction/source paths, nonexistent Disasters/singular filenames,
  oversized/truncated source reads, positional parsecheck CLI misuse and
  PowerShell quote/glob errors were rerun with actual paths/supported calls.
- Root's initial EF-099 append left its load-bearing lines field stale:
  doccheck RED. It was emitted from split_facts and regenerated to GREEN.
  The main draft briefly contained a guessed P2 short SHA; actual rev-parse
  corrected it before any commit. No guessed identifier survives as evidence.
- Root first tried committing an untracked Agent path before explicit git add;
  git refused with no commit. It was added by path and committed after the
  already-passing gate. Metadata's template line was withheld until its own
  file commit boundary. Foreign dirty paths were preserved throughout.
- Close-out staging initially included the six already-staged deletions;
  git add refused the absent paths. The existing deletions were retained,
  and the remaining owned paths were explicitly staged separately.
- P2 corrected an invented image asset, always-false menu enabled expression
  and overly permissive deleted-member fake. P1 corrected rapid quiet re-arm
  waiter behavior, Rain entry logic and counterfeit assertion expectations.
- P3 corrected game-time screenshot effects and template insertion quoting.
  P4 corrected pack id, active disaster flags, false-value fallback, provenance
  wording and a hygiene command literal that would have flagged itself.
- P5 corrected parent/interior recheck and enclosing FIRE after a capture
  refusal; the second unit falsifies both. Paused GameInit cannot progress.
- Root's first combined UI check lacked PropObjHasMember in the fake engine
  services. The dispatcher refused the Selected builder. The fake service was
  added and diagnostic assertions made page/refusal text explicit; the final
  actual co-load/UI checks pass. No native UI conclusion follows from it.
- Legacy skeleton smoke was updated for XSleekScroll and the hidden page frame;
  its remaining page stubs describe loading only core/panel, not final stubs.
- ALIASCHECK reports nine UNKNOWN references to order/probes/last despite
  00_TestCore's namespace initializer declaring them (opened lines 19-21).
  These report-only warnings are copied, not suppressed. Earlier transient
  LoggerState UNKNOWN disappeared once 90's accessor landed.
- Pack HEAD advanced through unrelated peer commits (C94, STATE and archive
  planning). Counts/fingerprints come from emitted commands. No peer dirty
  archive-planning edit is attributed to or restored by this task.

## SUGGESTIONS - merged, including deferred/disagreed choices

- **Adopted:** truthful leaf capabilities, complete menu contracts, actual
  mutation thread dispatch, copied scalar reads and conservative refusal.
  Keep native result witnesses distinct from toolkit OK records in 08.
- **Retained for 03B/08:** review native XPopup focus/close and actual IdNode
  registration, screenshot yield during save, focused notes with dynamic
  triggers, native scrollbar/tabs/scale, and two-map snapshot scope. Desk
  service models can mask engine-specific ownership/layout differences.
- **Deferred:** intensity submenus, a structured snapshot field watch,
  capability catalog, explicit whole-colony snapshot aggregation and better
  icon styling. Current controls expose complete intensity choices, scalar
  watches refuse aliases, and snapshots label their scope. I disagree with
  broadening these automatically before evidence; keep the suggestions.
- **Deferred, recommend when evidence demands:** successful-fire sequence for
  success-only run-until; exact event subscriptions where the target emits
  them. Polling cannot see changes that reverse between samples or while paused.
- **Retained:** 03B judges retirement of 00's console bootstrap. An alias
  checker enhancement can recognize namespace initializer fields separately;
  do not invent accessors for public tables or hide its warnings here.
- **Deferred v2:** ordered passage identities/endpoints/entrance tests and
  versioned skins/variants. Keep isolated/branched flat-grid fixtures after
  successful attended tests. Consider a native controller read adapter only
  if conservative fit refusal is costly; never use mutating test booleans or
  an idle live cursor controller.

## Outbox - final controls for 07; independent reads for 99

07 runs only after Claude 03B's verdict. Its canonical sitting slot template
is 80_AgentSlots.lua, copied verbatim in P3's report, kept entirely commented
until sitting preparation. Calls invoke real Lua functions through Run/Arm/
Fire in the actual mutation thread. No detached mutation or automatic arm.

| page/surface | final control list |
|---|---|
| dock/Sitting | SMR icon + always-visible taint/eligibility/arms/errors; native menus; MARK, Copy since mark, Flush, Clear, Pause/Resume, Stop disaster, Read taint, Read eligibility; open every advanced page, close advanced panel |
| fixed common row/Sitting body | same six evidence/world controls plus collapse; Read taint/Read eligibility body; Ctrl-Shift-F11 opens/closes, all chrome file/ring only |
| Selected section/fallback | Fill, Empty, Delete, Destroy (blow up), Clean & Fix, Malfunction, Add Prefab, Add Dust, Add Maintenance, Spawn Worker/Visitor/Child/Colonist/Drone/Shuttle, Upgrade 1-6; Dump, Pin A/B/C; supported subsets and class/busy caveats |
| Agent | Slot 1-6, Scratch, Pin A/B/C, note Enter/Add note, Screenshot + Mark, target sol trigger, selected scalar-field trigger, first error since mark, next rocket landed, live registered trigger arm/disarm rows |
| World | storms normal/electrostatic/great, devils minor/major, cold wave, Marsquake, rains with intensity choice; meteors single/multispawn/storm arm+click; underground cave-in/quake; quiet/stop; normal/fast/ultra/pause; run-until sol/trigger + cancel; fix/malfunction/fill; constructions/grids/selected rocket travel; research visible Main/unlock; domes open/close/unpin; applicants 50/100; funding +/-500M; tech points 1/10/100; adult/child/Martian-born adult/child each 1/10/100; trait category/id Add/Remove |
| Saves | Save/Load/explicit Override load A/B/C, process session, loaded provenance and complete status; strip has sanitized first 48 characters |
| Kit | default-disabled RunAll/run-one and probe dropdown/coloured verdicts, explicit preflight evidence; six existing logger toggles; print tee, console, cls; last 12 ring records/error count; fingerprint, Dump, snapshot/diff, field watch configure then separate arm/disarm |
| Stamper | name field, Capture selected/rectangle/map, Next saved, Copy layout, Cancel target/work, Plan at click, Stamp at click, Apply captured upgrades, Fill storages all maps, Add 10 colonists, Funding +500M |

Exact World registry and complete integration registry are emitted in the
smoke output below. Generic speed/spawn/funding, raw stamp/data operations and
probe_preflight are registry helpers, not invented argumentless menu buttons.
Slots/pins/triggers and watches resolve at invocation. No final stub remains.

07 must compile the explicit desktop probe attestation; preserve unavailable
eligibility, attempt/provenance semantics, scalar/paused polling limits,
native accepted screenshot witness, quiet/logger refusal, bounded rocket
policy and Stamper exclusions/caps/partial abort. Use P5's measured-count
capture/plan/stamp recipe; price first-screen witnesses and 3x abort limits
before 08. CopySince is the final clipboard operation or use its panel button.

99 must rederive lexical and transitive no-sync/no-cheat routes for every
actual action against source/archived 08 log, tag/primary-count coverage,
native taint invariants, idle function identities and lifecycle restoration,
counterfeit REDs, load order/H-10 and cross-vendor disagreements. Audit the
corrected source/fake/metadata/provenance drift, synthetic-plan gate departure,
all scope exclusions and 03B's single owner append. No agent report, eligibility
read or desktop model substitutes for native evidence. Briefs live in the
close-out commit's parent/grave; 99 retains the folder until its terminal gate.

## Emitted commit map, file inventory and scope

```text
pre-launch core 265fde79e8b35fd7886bdccc1c77c9dd88aba22e
pre-launch panel 05c7e45552006d2dcc28a4a49c446f288d74d356
P2 section/dock e0458841cebae5dd7eb7301f023c6fec48d87b21
P3 Agent 6e3512997d6fc85c599fa2c236eb6e2ffa0799e8
P3 template eec059709fb5e455cf40c6eef21d94b95708625d
P5 base 5d5ea0e5a462c271336d79ffe81741a8cd099a7a
P1 World c467dfedcc3031f301b2af3c61f42483c6f9aced
P4 Saves 51500d1ad00ac078d9e37b1047ddb65dca9e31d5
P4 Kit 96c9f1ad6c8edd7d0213ce8cdde537200ccecf7f
P4 accessor 2ce880489a4bad1b0d5574a7ae1480e3fcefbbe3
P5 state 790deaa40c9dd4ab4a3fe6a58e8d3881b5806ad5
Root post-record 11b359cee66def72c39f33e63181f6b67c84ce2d
Root final panel 45770f8b4ad4799a63912448213b06572b46a08d
Root World editor d183729d1abe0309a8dd3fc424cff91c54a42f49
Root Kit editor c372f4a9e25abc04564fbe085bc756b2c06ef0d1
Root Stamper editor cee5bab230f2fac876aa0e6d86bb97f6b56ad020
```

| file | final lines | principal functions |
|---|---:|---|
| Code/70_SMRTK_Core.lua | 425 | Log, Action, Run/Arm/Disarm/Fire, AcquireClick/ReleaseClick, ConsoleArm |
| Code/71_SMRTK_Panel.lua | 241 | Page, Button, OpenPanel, BuildPage, RefreshPanel |
| Code/72_SMRTK_World.lua | 453 | register, scheduled, speed, spawn_colonists, funding |
| Code/73_SMRTK_Infopanel.lua | 375 | SelectedActions, DockMenuItems, RefreshDock, DialogOpen |
| Code/74_SMRTK_Agent.lua | 432 | Bind, BindScratch, Trigger, TriggerField, screenshot |
| Code/75_SMRTK_Saves.lua | 140 | operation, readmeta, provenance, GatherGameMetadata |
| Code/76_SMRTK_Kit.lua | 335 | ProbePreflight, EnsureKitLoggers, fingerprint, snapshot, differences |
| Code/77_SMRTK_Stamper.lua | 717 | Normalize/Export/Resolve/Names/Plan, capture, execute_stamp, last_stamp |
| Code/80_AgentSlots.lua | 78 | fully commented template; no executable functions |
| Code/90_Loggers.lua | 359 | seven-line LoggerState addition; existing toggle bodies retained |

Every function inventory is emitted in per-file gate evidence.

```text
$ git -C ../SMR-BugFixPack-TestKit diff 5d8d3b3 HEAD --stat
 Code/70_SMRTK_Core.lua      |  63 +++-
 Code/71_SMRTK_Panel.lua     |  44 ++-
 Code/72_SMRTK_World.lua     | 453 ++++++++++++++++++++++++++++
 Code/73_SMRTK_Infopanel.lua | 375 +++++++++++++++++++++++
 Code/74_SMRTK_Agent.lua     | 432 ++++++++++++++++++++++++++
 Code/75_SMRTK_Saves.lua     | 140 +++++++++
 Code/76_SMRTK_Kit.lua       | 335 +++++++++++++++++++++
 Code/77_SMRTK_Stamper.lua   | 717 ++++++++++++++++++++++++++++++++++++++++++++
 Code/80_AgentSlots.lua      |  78 +++++
 Code/90_Loggers.lua         |   7 +
 Layouts/README.md           |   1 +
 metadata.lua                |   7 +
 12 files changed, 2637 insertions(+), 15 deletions(-)
```

## Complete 03A core/panel/accessor diff

```diff
diff --git a/Code/70_SMRTK_Core.lua b/Code/70_SMRTK_Core.lua
index d58be49..825b0c9 100644
--- a/Code/70_SMRTK_Core.lua
+++ b/Code/70_SMRTK_Core.lua
@@ -1,4 +1,4 @@
--- SMR Tool Kit: local TestKit only. Runtime premises await the 02 sitting.
+-- SMR Tool Kit: local TestKit only. 02 passed; page effects await sitting 08.
 -- Actions return a fields table, or false + a refusal reason. Payloads call
 -- Run/Arm/Disarm/Fire; they never call a registered callback themselves.
 SMRTK = rawget(_G, "SMRTK") or {}
@@ -16,6 +16,11 @@ T.mark_errors = T.mark_errors or 0
 T.tap = T.tap or { console = 0, print = 0 }
 T.capacity = 300
 local emitting, handling_error, tee_depth = false, false, 0
+local recording = {}
+T.after_record = T.after_record or {}
+T.chrome_verbs = { TAB = true, MOVE = true, PANEL = true, COLLAPSE = true,
+	CLEAR = true, SHORTCUT = true, PANEL_RESTORE = true, DOCK = true,
+	MENU = true, SECTION = true }
 local unpack_values = table.unpack or unpack
 local function pack(...) return { n = select("#", ...), ... } end
 
@@ -47,7 +52,7 @@ end
 -- One formatter, one file sink. ModLog passes its argument through a second
 -- printf formatter (Mod.lua:109-132); escape literal percent signs for it.
 -- ConsolePrint is display only. Direct ring insertion is NOT native tap proof.
-function T.Log(verb, kv)
+function T.Log(verb, kv, screen)
 	T.sequence = T.sequence + 1
 	local words = { "[SMRTK] SMRTK_" .. tostring(verb):gsub("[^%w_]", "_") }
 	local keys = {}
@@ -68,7 +73,7 @@ function T.Log(verb, kv)
 		if not ok then T.log_error = tostring(err) end
 	end
 	local console = rawget(_G, "ConsolePrint")
-	if console then pcall(console, line) end
+	if console and screen ~= false and not T.chrome_verbs[verb] then pcall(console, line) end
 	local flush = rawget(_G, "FlushLogFile")
 	if flush then pcall(flush) end
 	emitting = previous
@@ -191,8 +196,19 @@ local function dispatch(id, phase, reason, ...)
 		elseif phase == "disarm" and fields.status == "OK" then T.armed[id] = nil end
 		if phase == "run" or phase == "fire" then T.fires[id] = (T.fires[id] or 0) + 1 end
 	end
-	T.Log(verb, fields)
+	T.Log(verb, fields, def and def.screen)
 	check_taint(id, before)
+	-- Read-only coordination after the primary evidence and its assertion.
+	-- A callback may dispatch distinct evidence actions; bound same-verb recursion.
+	local after = T.after_record[verb]
+	if fields.status == "OK" and (phase == "run" or phase == "fire")
+		and type(after) == "function" and not recording[verb] then
+		recording[verb] = true
+		local ok, err = pcall(after, fields)
+		recording[verb] = nil
+		if not ok then T.OnLuaError("after_record " .. verb .. ": " .. tostring(err)) end
+	end
+	if T.RefreshDock then T.RefreshDock() end
 	return fields.status == "OK", fields
 end
 
@@ -291,7 +307,7 @@ function T.PrintTee(on)
 	return T.Disarm("print_tee", "manual")
 end
 
-local defaults = { open = true, tab = "Sitting", collapsed = false, x = 40, y = 160 }
+local defaults = { open = false, tab = "Sitting", collapsed = false, x = 40, y = 160, surface = "" }
 function T.PanelState()
 	if T.panel_state then return T.panel_state end
 	local storage = rawget(_G, "LocalStorage")
@@ -303,6 +319,7 @@ function T.PanelState()
 		if type(saved) == "table" and type(saved[key]) == "boolean" and type(default) == "boolean" then state[key] = saved[key] end
 	end
 	T.panel_state = state
+	if state.surface ~= "hybrid-v1" then state.open, state.surface = false, "hybrid-v1" end
 	return state
 end
 function T.SavePanelState(changes)
@@ -342,6 +359,7 @@ function OnMsg.PreLoadGame()
 	T.ConsoleArm("PreLoadGame")
 end
 function OnMsg.SavegameSaved() T.DisarmAll("SavegameSaved") end
+function OnMsg.SaveGameStart() T.DisarmAll("SaveGameStart") end
 function OnMsg.LoadGame() T.DisarmAll("LoadGame") end
 function OnMsg.ChangeMap()
 	T.DisarmAll("ChangeMap")
@@ -370,3 +388,38 @@ T.Action { id = "console_control", verb = "CONSOLE_CONTROL", run = function()
 end }
 function T.ConsoleControl() return T.Run("console_control") end
 T.Log("CORE", { loaded = true, tee = false })
+
+-- Shared exclusive listener: no vanilla method is replaced while armed/idle.
+function T.AcquireClick(id, callback)
+	if not T.armed[id] then return false, "click owner must be armed" end
+	if T.click_capture then return false, "map click owned by " .. T.click_capture.id end
+	if type(callback) ~= "function" then return false, "click callback required" end
+	if not terminal or not terminal.AddTarget or not TerminalTarget then return false, "terminal unavailable" end
+	local target = TerminalTarget:new { terminal_target_priority = 10001 }
+	T.click_capture = { id = id, target = target }
+	target.OnMouseButtonDown = function(self, pt, button)
+		if button ~= "L" and button ~= "R" then return end
+		local desktop = terminal.desktop
+		local hit = desktop and desktop.modal_window and desktop.modal_window:GetMouseTarget(pt)
+		local mode = GetInGameInterfaceModeDlg and GetInGameInterfaceModeDlg()
+		local interface = GetInGameInterface and GetInGameInterface()
+		if hit and hit ~= desktop and hit ~= mode and hit ~= interface then return end
+		if not T.armed[id] then T.ReleaseClick(id); return end
+		if button == "R" then T.Disarm(id, "right click"); return "break" end
+		local pos = GetTerrainCursor and GetTerrainCursor()
+		if not pos then return end
+		local obj = SelectionMouseObj and SelectionMouseObj()
+		local ok, err = pcall(callback, pos, obj)
+		if not ok then T.OnLuaError(err, "map click " .. id); T.Disarm(id, "click error") end
+		return "break"
+	end
+	local ok, err = pcall(terminal.AddTarget, target)
+	if not ok then T.click_capture = nil; return false, tostring(err) end
+	return true
+end
+function T.ReleaseClick(id)
+	local capture = T.click_capture
+	if not capture or capture.id ~= id then return end
+	terminal.RemoveTarget(capture.target)
+	T.click_capture = nil
+end
diff --git a/Code/71_SMRTK_Panel.lua b/Code/71_SMRTK_Panel.lua
index 0d17e13..52201f1 100644
--- a/Code/71_SMRTK_Panel.lua
+++ b/Code/71_SMRTK_Panel.lua
@@ -1,9 +1,10 @@
--- Floating skeleton only. Page payloads arrive after the attended kill gate.
+-- Fixed advanced side panel. The dock and selected section are separate hosts.
 local T = SMRTK
 T.pages = T.pages or {}
 T.page_order = T.page_order or {}
 T.hotkey = "Ctrl-Shift-F11"
-local width, expanded, collapsed = 780, 340, 100
+local width, expanded, collapsed = 780, 540, 100
+T.surface = "hybrid-v1"
 local bg = RGBA(25, 32, 40, 245)
 local button_bg = RGBA(55, 68, 82, 255)
 
@@ -52,14 +53,19 @@ function T.BuildPage()
 	if not panel or panel.window_state == "destroying" then return end
 	local state = T.PanelState()
 	if not T.pages[state.tab] then state.tab = "Sitting" end
-	if panel.page_host then panel.page_host:delete() end
-	panel.page_host = XWindow:new({ Id = "idSMRTKPage", Dock = "bottom", MinHeight = 186, MaxHeight = 186,
-		FoldWhenHidden = true, LayoutMethod = "VList", LayoutVSpacing = 6, Padding = box(8, 6, 8, 6) }, panel)
+	if panel.page_frame then panel.page_frame:delete()
+	elseif panel.page_host then panel.page_host:delete() end
+	panel.page_frame = XWindow:new({ Id = "idSMRTKPageFrame", IdNode = true, Dock = "bottom",
+		MinHeight = 386, MaxHeight = 386, FoldWhenHidden = true }, panel)
+	XSleekScroll:new({ Id = "idSMRTKPageScroll", Dock = "right", Target = "idSMRTKPage",
+		AutoHide = true, MinWidth = 12, MaxWidth = 12 }, panel.page_frame)
+	panel.page_host = XScrollArea:new({ Id = "idSMRTKPage", Dock = "box", VScroll = "idSMRTKPageScroll",
+		LayoutMethod = "VList", LayoutVSpacing = 6, Padding = box(8, 6, 8, 6) }, panel.page_frame)
 	local page = T.pages[state.tab]
 	if page.build then page.build(panel.page_host)
 	else text(panel.page_host, page.label .. " â€” page content follows the skeleton sitting.") end
-	panel.page_host:SetVisible(not state.collapsed)
-	if panel.window_state == "open" then panel.page_host:Open() end
+	panel.page_frame:SetVisible(not state.collapsed)
+	if panel.window_state == "open" then panel.page_frame:Open() end
 	T.RefreshPanel()
 end
 
@@ -73,10 +79,15 @@ function T.RefreshPanel()
 	local strip = string.format("SMR Tool Kit | %s | eligibility: %s\nArmed: %d | quiet: %s | errors since mark: %d | %s",
 		taint_label, eligibility, T.ArmedCount(), T.armed.quiet and "ON" or "off",
 		T.error_count - T.mark_errors, state.tab)
+	if T.saves and T.saves.status then
+		local status = tostring(T.saves.status):gsub("[%c]", " ")
+		if #status > 48 then status = status:sub(1, 45) .. "..." end
+		strip = strip .. " | Saves: " .. status
+	end
 	if T.log_error then strip = strip .. " | LOG ERROR" end
 	panel.status:SetText(strip)
 	panel.tabs:SetVisible(not state.collapsed)
-	if panel.page_host then panel.page_host:SetVisible(not state.collapsed) end
+	if panel.page_frame then panel.page_frame:SetVisible(not state.collapsed) end
 	panel:SetMinHeight(state.collapsed and collapsed or expanded)
 	panel:SetMaxHeight(state.collapsed and collapsed or expanded)
 	for id, button in pairs(panel.tab_buttons) do
@@ -109,10 +120,12 @@ function T.OpenPanel()
 	local x, y = clamp_position(state.x, state.y, panel)
 	-- Logical margins let the engine keep position/size correct at UI scales.
 	panel:SetMargins(box(x, y, 0, 0))
+	panel:SetMargins(box(8, 80, 0, 130))
 	local strip = XWindow:new({ MinHeight = 50, MaxHeight = 50, HandleMouse = true }, panel)
 	panel.status = text(strip, "SMR Tool Kit", { Dock = "box" })
 	-- Only this instance's strip handles dragging; no vanilla method is patched.
 	strip.OnMouseButtonDown = function(self, pt, button)
+		if T.surface == "hybrid-v1" then return "break" end
 		if button ~= "L" then return "break" end
 		self.drag_start, self.panel_start = pt, panel.box:min()
 		self.desktop:SetMouseCapture(self)
@@ -148,8 +161,10 @@ function T.OpenPanel()
 	T.Button(row, "[_]", "panel_collapse", { MinWidth = 50 })
 	panel.tabs = XWindow:new({ LayoutMethod = "HList", LayoutHSpacing = 4, MinHeight = 30, MaxHeight = 30, FoldWhenHidden = true }, panel)
 	panel.tab_buttons = {}
+	local tab_width = math.floor((width - 16 - 4 * (#T.page_order - 1)) / #T.page_order)
 	for _, id in ipairs(T.page_order) do
-		panel.tab_buttons[id] = T.Button(panel.tabs, T.pages[id].label, "tab_" .. id, { MinWidth = 128 })
+		panel.tab_buttons[id] = T.Button(panel.tabs, T.pages[id].label, "tab_" .. id,
+			{ MinWidth = tab_width, MaxWidth = tab_width })
 	end
 	T.BuildPage()
 	panel:Open()
@@ -186,6 +201,13 @@ end }
 function T.TogglePanel() return T.Run("panel_toggle") end
 
 for _, id in ipairs({ "Sitting", "Agent", "World", "Saves", "Kit" }) do T.Page(id, id) end
+T.Page("Sitting", "Sitting", function(parent)
+	text(parent, "Read the safety state before changing the fixture.")
+	local row = XWindow:new({ LayoutMethod = "HList", LayoutHSpacing = 4, MinHeight = 30 }, parent)
+	T.Button(row, "Read taint", "taint_read", { MinWidth = 144 })
+	T.Button(row, "Read eligibility", "eligibility", { MinWidth = 144 })
+	text(parent, "MARK, Copy, Flush, Clear, Pause and Stop stay in the top row.")
+end)
 
 -- Shortcuts is emitted AFTER vanilla shortcut creation (XShortcuts.lua:63).
 -- It is correct for registering our action, too late for arming DE_Console.
@@ -199,8 +221,10 @@ local function restore_panel()
 	CreateRealTimeThread(function()
 		WaitLoadingScreenClose()
 		if T.PanelState().open and GetInGameInterface() then
+			local previous = T.panel
+			local visible = previous and previous.window_state ~= "destroying" and previous:GetVisible()
 			local panel = T.OpenPanel()
-			if panel then T.Log("PANEL_RESTORE", { open = true, tab = T.PanelState().tab }) end
+			if panel and not visible then T.Log("PANEL_RESTORE", { open = true, tab = T.PanelState().tab }) end
 		end
 	end)
 end
diff --git a/Code/90_Loggers.lua b/Code/90_Loggers.lua
index 2dfd86a..bd38751 100644
--- a/Code/90_Loggers.lua
+++ b/Code/90_Loggers.lua
@@ -9,6 +9,13 @@
 
 SMRTest.Log = SMRTest.Log or {}
 local installed = {}   -- name -> uninstall function
+-- Read-only toolkit coordination; callers cannot mutate installation state.
+function SMRTest.LoggerState(name)
+	if name ~= nil then return not not installed[name] end
+	local copy = {}
+	for key in pairs(installed) do copy[key] = true end
+	return copy
+end
 local out = SMRTest.Print
 
 -- Declare a toggle. install() must return an uninstall function, or a string
```

## Post-release native editor correction diff

```diff
diff --git a/Code/72_SMRTK_World.lua b/Code/72_SMRTK_World.lua
index 99da827..523ff81 100644
--- a/Code/72_SMRTK_World.lua
+++ b/Code/72_SMRTK_World.lua
@@ -395,8 +395,10 @@ local function button(parent, value, id, phase, args)
 	return b
 end
 local function editor(parent, value, width)
-	return XTextEditor:new({ Text = tostring(value), Translate = false, MinWidth = width or 160, MaxWidth = width or 160,
+	local edit = XTextEditor:new({ Translate = false, MinWidth = width or 160, MaxWidth = width or 160,
 		MinHeight = 30, MaxHeight = 30, Multiline = false, TextStyle = "ConsoleLog" }, parent)
+	edit:SetText(tostring(value))
+	return edit
 end
 T.Page("World", "World", function(parent)
 	label(parent, "Disasters dispatch their native leaves; inspect the map before retrying. Meteors: arm, click map; right click cancels.")
diff --git a/Code/76_SMRTK_Kit.lua b/Code/76_SMRTK_Kit.lua
index 27fa948..e4afd9f 100644
--- a/Code/76_SMRTK_Kit.lua
+++ b/Code/76_SMRTK_Kit.lua
@@ -288,7 +288,8 @@ T.Page("Kit", "Kit", function(parent)
 	local tools = XWindow:new({ LayoutMethod = "HWrap", LayoutHSpacing = 4, LayoutVSpacing = 4 }, parent)
 	for _, item in ipairs({ { "Console", "console_open" }, { "cls", "clear" }, { "Fingerprint", "fingerprint" },
 		{ "Dump", "dump_selected" }, { "Snapshot", "snapshot" }, { "Diff latest", "snapshot_diff" } }) do button(tools, item[1], item[2]) end
-	local editor = XTextEditor:new({ Text = K.field, Translate = false, MinHeight = 30, MaxHeight = 30 }, parent)
+	local editor = XTextEditor:new({ Translate = false, MinHeight = 30, MaxHeight = 30 }, parent)
+	editor:SetText(K.field)
 	local watch = button(parent, "Configure watch of selected field", "watch_field")
 	watch.OnPress = function()
 		local value = editor:GetText(); K.field = value
diff --git a/Code/77_SMRTK_Stamper.lua b/Code/77_SMRTK_Stamper.lua
index bca2902..f508f68 100644
--- a/Code/77_SMRTK_Stamper.lua
+++ b/Code/77_SMRTK_Stamper.lua
@@ -613,7 +613,8 @@ function OnMsg.DoneGame() reset() end
 T.Page("Stamper","Stamper",function(parent)
 	local function text(label) return XText:new({Text=label,Translate=false,TextStyle="ConsoleLog",HandleMouse=false},parent) end
 	text("Layouts: select a name, capture or choose saved, then plan before stamping.")
-	local editor=XTextEditor:new({Id="idLayoutName",Translate=false,Text=L.name,MinHeight=32,MaxHeight=32,Multiline=false,MaxLen=48},parent)
+	local editor=XTextEditor:new({Id="idLayoutName",Translate=false,MinHeight=32,MaxHeight=32,Multiline=false,MaxLen=48},parent)
+	editor:SetText(L.name)
 	local function row(buttons)
 		local host=XWindow:new({LayoutMethod="HList",LayoutHSpacing=4,MinHeight=30,MaxHeight=30},parent)
 		for _,b in ipairs(buttons) do
```

## Independent coordinator per-file and ordered gates - verbatim, WARN included

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/70_SMRTK_Core.lua Code/71_SMRTK_Panel.lua --presence --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=8d1a6aa3019acc0184efd37b28693f258647c35b testkit=05c7e45552006d2dcc28a4a49c446f288d74d356
PARSE Code/70_SMRTK_Core.lua: 0 errors [Lua 5.5]
NO SYNC Code/70_SMRTK_Core.lua: 0 lines
NO BARE PRINT Code/70_SMRTK_Core.lua: 0 lines
H-10 Code/70_SMRTK_Core.lua: listed
PARSE Code/71_SMRTK_Panel.lua: 0 errors [Lua 5.5]
NO SYNC Code/71_SMRTK_Panel.lua: 0 lines
NO BARE PRINT Code/71_SMRTK_Panel.lua: 0 lines
H-10 Code/71_SMRTK_Panel.lua: listed
PRESENCE Data/CheatDef.lua (build 24995074): 26 lines
  147: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  154: 			NetSyncEvent("Cheat", "CheatColdWave", chosen)
  161: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  168: 			NetSyncEvent("Cheat", "CheatDustDevil", false, chosen, GetCameraLookAtPassable())
  175: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  182: 			NetSyncEvent("Cheat", "CheatDustDevil", "major", chosen, GetCameraLookAtPassable())
  189: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  196: 			NetSyncEvent("Cheat", "CheatDustStorm", "normal", chosen)
  203: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  210: 			NetSyncEvent("Cheat", "CheatDustStorm", "electrostatic", chosen)
  217: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  224: 			NetSyncEvent("Cheat", "CheatDustStorm", "great", chosen)
  231: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  238: 			NetSyncEvent("Cheat", "CheatTriggerMarsquake", chosen)
  245: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  252: 			NetSyncEvent("Cheat", "CheatMeteors", "single", chosen, GetCameraLookAtPassable())
  259: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  266: 			NetSyncEvent("Cheat", "CheatMeteors", "multispawn", chosen, GetCameraLookAtPassable())
  273: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  280: 			NetSyncEvent("Cheat", "CheatMeteors", "storm", chosen, GetCameraLookAtPassable())
  287: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  294: 			NetSyncEvent("Cheat", "CheatRainsDisaster", chosen)
  704: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  711: 			NetSyncEvent("Cheat", "CheatFinishMystery", cls)
  718: 	Comment = "sync=false so the picker UI isn't opened on every client; the chosen action syncs via NetSyncEvent regardless.",
  725: 			NetSyncEvent("Cheat", "CheatStartMystery", cls)
$ python tools/doccheck.py
ENTRIES: 190 files (2 grouped), 225 preserved index rows, 187 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x187
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (225 rows)
FACTS: 101 files, 60 state an observation date, 3544 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 93 C = 225 (in 190 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 27 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.172 s)
REPAIR PASS SELFTEST: PASS (0.166 s)
STATE COUNTS SELFTEST: PASS (0.143 s)
PUSH SET: 43878 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       7947 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
    → every session pays this before it has decided anything; evict from the largest, not the easiest
TESTKIT TREE: clean
ALIASCHECK: 27 file(s), 37 SMRTest member(s) derived, 0 finding(s)  (report-only)
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/73_SMRTK_Infopanel.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=05c7e45552006d2dcc28a4a49c446f288d74d356
PARSE Code/73_SMRTK_Infopanel.lua: 0 errors [Lua 5.5]
BUILT Code/73_SMRTK_Infopanel.lua: 375 lines
FUNCTIONS Code/73_SMRTK_Infopanel.lua: alive, label, member, method_for, object_name, depot_read, T.SelectedActions, selected_button, selected_body, named_child, T.DockMenuItems, close_menu, invoke_menu, build_menu_actions, action, T.RefreshDock, OnMsg.DialogOpen, restore_dock, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_dock, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.DoneGame
NO SYNC Code/73_SMRTK_Infopanel.lua: 0 lines
NO BARE PRINT Code/73_SMRTK_Infopanel.lua: 0 lines
H-10 Code/73_SMRTK_Infopanel.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 31 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.150 s)
REPAIR PASS SELFTEST: PASS (0.168 s)
STATE COUNTS SELFTEST: PASS (0.145 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 6 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M metadata.lua
  WARN ?? Code/73_SMRTK_Infopanel.lua
  WARN ?? Code/74_SMRTK_Agent.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
ALIASCHECK: 31 file(s), 37 SMRTest member(s) derived, 0 finding(s)  (report-only)
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/74_SMRTK_Agent.lua Code/80_AgentSlots.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=e0458841cebae5dd7eb7301f023c6fec48d87b21
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
BUILT Code/74_SMRTK_Agent.lua: 432 lines
FUNCTIONS Code/74_SMRTK_Agent.lua: object_name, slot_context, bind_slot, T.Bind, T.BindScratch, screenshot, stop_thread, effect_fields, T.Trigger, scalar, field_prepare, field_changed, T.TriggerField, OnMsg.RocketLanded, OnMsg.AsteroidRocketLanded, clear_pins, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, label, row, button, editor, invoke, submit_note, refresh
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
H-10 Code/74_SMRTK_Agent.lua: listed
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
BUILT Code/80_AgentSlots.lua: 78 lines
FUNCTIONS Code/80_AgentSlots.lua: 
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
H-10 Code/80_AgentSlots.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 31 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.152 s)
REPAIR PASS SELFTEST: PASS (0.160 s)
STATE COUNTS SELFTEST: PASS (0.146 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 5 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M metadata.lua
  WARN ?? Code/74_SMRTK_Agent.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
ALIASCHECK: 31 file(s), 37 SMRTest member(s) derived, 0 finding(s)  (report-only)
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/74_SMRTK_Agent.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=e0458841cebae5dd7eb7301f023c6fec48d87b21
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
BUILT Code/74_SMRTK_Agent.lua: 432 lines
FUNCTIONS Code/74_SMRTK_Agent.lua: object_name, slot_context, bind_slot, T.Bind, T.BindScratch, screenshot, stop_thread, effect_fields, T.Trigger, scalar, field_prepare, field_changed, T.TriggerField, OnMsg.RocketLanded, OnMsg.AsteroidRocketLanded, clear_pins, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, label, row, button, editor, invoke, submit_note, refresh
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
H-10 Code/74_SMRTK_Agent.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 33 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.146 s)
REPAIR PASS SELFTEST: PASS (0.176 s)
STATE COUNTS SELFTEST: PASS (0.163 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 7 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M metadata.lua
  WARN ?? Code/72_SMRTK_World.lua
  WARN ?? Code/74_SMRTK_Agent.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
ALIASCHECK: 33 file(s), 37 SMRTest member(s) derived, 0 finding(s)  (report-only)
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/80_AgentSlots.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=6e3512997d6fc85c599fa2c236eb6e2ffa0799e8
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
BUILT Code/80_AgentSlots.lua: 78 lines
FUNCTIONS Code/80_AgentSlots.lua: 
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
H-10 Code/80_AgentSlots.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 33 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.151 s)
REPAIR PASS SELFTEST: PASS (0.164 s)
STATE COUNTS SELFTEST: PASS (0.141 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 6 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M metadata.lua
  WARN ?? Code/72_SMRTK_World.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
ALIASCHECK: 33 file(s), 37 SMRTest member(s) derived, 1 finding(s)  (report-only)
  WARN UNKNOWN   72_SMRTK_World.lua         SMRTest.LoggerState is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/77_SMRTK_Stamper.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=eec059709fb5e455cf40c6eef21d94b95708625d
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 640 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 33 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.160 s)
REPAIR PASS SELFTEST: PASS (0.163 s)
STATE COUNTS SELFTEST: PASS (0.152 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 5 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M metadata.lua
  WARN ?? Code/72_SMRTK_World.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Layouts/
ALIASCHECK: 33 file(s), 37 SMRTest member(s) derived, 1 finding(s)  (report-only)
  WARN UNKNOWN   72_SMRTK_World.lua         SMRTest.LoggerState is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/72_SMRTK_World.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=965fb0869caca2b84d0782bb5da3d909cbfcb30f
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
BUILT Code/72_SMRTK_World.lua: 451 lines
FUNCTIONS Code/72_SMRTK_World.lua: threaded, world, integer, register, preset, first_setting, scheduled, speed, cancel_thread, spawn_colonists, funding, label, row, button, editor, refresh_traits
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
H-10 Code/72_SMRTK_World.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.147 s)
REPAIR PASS SELFTEST: PASS (0.177 s)
STATE COUNTS SELFTEST: PASS (0.156 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 6 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
  WARN  M Code/90_Loggers.lua
  WARN  M metadata.lua
  WARN ?? Code/72_SMRTK_World.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/76_SMRTK_Kit.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/75_SMRTK_Saves.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=c467dfedcc3031f301b2af3c61f42483c6f9aced
PARSE Code/75_SMRTK_Saves.lua: 0 errors [Lua 5.5]
BUILT Code/75_SMRTK_Saves.lua: 140 lines
FUNCTIONS Code/75_SMRTK_Saves.lua: realtime, slotname, available, provenance, OnMsg.GatherGameMetadata, OnMsg.GameMetadataLoaded, readmeta, operation, OnMsg.SaveGameStart, label, button
NO SYNC Code/75_SMRTK_Saves.lua: 0 lines
NO BARE PRINT Code/75_SMRTK_Saves.lua: 0 lines
H-10 Code/75_SMRTK_Saves.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.146 s)
REPAIR PASS SELFTEST: PASS (0.165 s)
STATE COUNTS SELFTEST: PASS (0.146 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 5 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
  WARN  M Code/90_Loggers.lua
  WARN  M metadata.lua
  WARN ?? Code/75_SMRTK_Saves.lua
  WARN ?? Code/76_SMRTK_Kit.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/76_SMRTK_Kit.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=51500d1ad00ac078d9e37b1047ddb65dca9e31d5
PARSE Code/76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
BUILT Code/76_SMRTK_Kit.lua: 334 lines
FUNCTIONS Code/76_SMRTK_Kit.lua: scalar, serial, method, realtime, orderkey, hygiene, T.ProbePreflight, invalidate, OnMsg.PreLoadGame, OnMsg.NewGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.EnsureKitLoggers, OnMsg.DataLoaded, OnMsg.InGameInterfaceCreated, OnMsg.DialogOpen, fingerprint, snapshot, differences, label, button
NO SYNC Code/76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT Code/76_SMRTK_Kit.lua: 0 lines
H-10 Code/76_SMRTK_Kit.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.149 s)
REPAIR PASS SELFTEST: PASS (0.158 s)
STATE COUNTS SELFTEST: PASS (0.141 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 4 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
  WARN  M Code/90_Loggers.lua
  WARN  M metadata.lua
  WARN ?? Code/76_SMRTK_Kit.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/90_Loggers.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=96c9f1ad6c8edd7d0213ce8cdde537200ccecf7f
PARSE Code/90_Loggers.lua: 0 errors [Lua 5.5]
BUILT Code/90_Loggers.lua: 359 lines
FUNCTIONS Code/90_Loggers.lua: SMRTest.LoggerState, toggle, SMRTest.Loggers, stamp, predicted, SMRTest.ReportReservations, SMRTest.ReportBrokenTrack, SMRTest.ReportTrains
NO SYNC Code/90_Loggers.lua: 0 lines
NO BARE PRINT Code/90_Loggers.lua: 0 lines
H-10 Code/90_Loggers.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.148 s)
REPAIR PASS SELFTEST: PASS (0.166 s)
STATE COUNTS SELFTEST: PASS (0.147 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 2 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
  WARN  M Code/90_Loggers.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/77_SMRTK_Stamper.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=2ce880489a4bad1b0d5574a7ae1480e3fcefbbe3
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 716 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row, last_stamp
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.152 s)
REPAIR PASS SELFTEST: PASS (0.167 s)
STATE COUNTS SELFTEST: PASS (0.145 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 1 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/70_SMRTK_Core.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=790deaa40c9dd4ab4a3fe6a58e8d3881b5806ad5
PARSE Code/70_SMRTK_Core.lua: 0 errors [Lua 5.5]
BUILT Code/70_SMRTK_Core.lua: 425 lines
FUNCTIONS Code/70_SMRTK_Core.lua: pack, now, value, append, T.Log, OnMsg.ConsoleLine, T.OnLuaError, OnMsg.OnLuaError, OnMsg.OnThreadError, T.Taint, T.Eligibility, check_taint, T.ArmedCount, T.Action, dispatch, T.Run, T.Arm, T.Disarm, T.Fire, T.DisarmAll, T.Bind, T.Mark, T.CopySince, T.TaintRead, tee, T.PrintTee, T.PanelState, T.SavePanelState, T.ConsoleArm, OnMsg.DataLoading, OnMsg.PreNewMap, OnMsg.PreLoadGame, OnMsg.SavegameSaved, OnMsg.SaveGameStart, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.ConsoleControl, T.AcquireClick, T.ReleaseClick
NO SYNC Code/70_SMRTK_Core.lua: 0 lines
NO BARE PRINT Code/70_SMRTK_Core.lua: 0 lines
H-10 Code/70_SMRTK_Core.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.146 s)
REPAIR PASS SELFTEST: PASS (0.170 s)
STATE COUNTS SELFTEST: PASS (0.143 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 2 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/70_SMRTK_Core.lua
  WARN  M Code/71_SMRTK_Panel.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/71_SMRTK_Panel.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=11b359cee66def72c39f33e63181f6b67c84ce2d
PARSE Code/71_SMRTK_Panel.lua: 0 errors [Lua 5.5]
BUILT Code/71_SMRTK_Panel.lua: 241 lines
FUNCTIONS Code/71_SMRTK_Panel.lua: text, T.Button, T.Page, T.BuildPage, T.RefreshPanel, clamp_position, T.OpenPanel, T.TogglePanel, OnMsg.Shortcuts, restore_panel, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_panel, OnMsg.ChangeMap, OnMsg.PreLoadGame, OnMsg.DoneGame
NO SYNC Code/71_SMRTK_Panel.lua: 0 lines
NO BARE PRINT Code/71_SMRTK_Panel.lua: 0 lines
H-10 Code/71_SMRTK_Panel.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.152 s)
REPAIR PASS SELFTEST: PASS (0.198 s)
STATE COUNTS SELFTEST: PASS (0.151 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 1 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/71_SMRTK_Panel.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=45770f8b4ad4799a63912448213b06572b46a08d
LOAD ORDER: ModDef.LoadCode non-Code pass, then Code pass; each preserves metadata order
PARSE Code/00_TestCore.lua: 0 errors [Lua 5.5]
PARSE Code/10_Probes_Wave1.lua: 0 errors [Lua 5.5]
PARSE Code/20_Probes_Wave2.lua: 0 errors [Lua 5.5]
PARSE Code/30_Probes_Wave3.lua: 0 errors [Lua 5.5]
PARSE Code/40_Probes_Wave4.lua: 0 errors [Lua 5.5]
PARSE Code/50_Probes_Wave5.lua: 0 errors [Lua 5.5]
PARSE Code/55_Probes_Wave6.lua: 0 errors [Lua 5.5]
PARSE Code/56_Probes_Wave7.lua: 0 errors [Lua 5.5]
PARSE Code/57_Probes_Wave8.lua: 0 errors [Lua 5.5]
PARSE Code/58_Probes_Wave9.lua: 0 errors [Lua 5.5]
PARSE Code/59_Probes_Wave10.lua: 0 errors [Lua 5.5]
PARSE Code/61_Probes_Wave11.lua: 0 errors [Lua 5.5]
PARSE Code/62_Probes_Wave12.lua: 0 errors [Lua 5.5]
PARSE Code/63_Probes_Wave13.lua: 0 errors [Lua 5.5]
PARSE Code/64_Probes_Wave14.lua: 0 errors [Lua 5.5]
PARSE Code/66_Probes_Wave15.lua: 0 errors [Lua 5.5]
PARSE Code/60_Probes_Opt.lua: 0 errors [Lua 5.5]
PARSE Code/65_Probes_Rescue.lua: 0 errors [Lua 5.5]
PARSE Code/70_SMRTK_Core.lua: 0 errors [Lua 5.5]
BUILT Code/70_SMRTK_Core.lua: 425 lines
FUNCTIONS Code/70_SMRTK_Core.lua: pack, now, value, append, T.Log, OnMsg.ConsoleLine, T.OnLuaError, OnMsg.OnLuaError, OnMsg.OnThreadError, T.Taint, T.Eligibility, check_taint, T.ArmedCount, T.Action, dispatch, T.Run, T.Arm, T.Disarm, T.Fire, T.DisarmAll, T.Bind, T.Mark, T.CopySince, T.TaintRead, tee, T.PrintTee, T.PanelState, T.SavePanelState, T.ConsoleArm, OnMsg.DataLoading, OnMsg.PreNewMap, OnMsg.PreLoadGame, OnMsg.SavegameSaved, OnMsg.SaveGameStart, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.ConsoleControl, T.AcquireClick, T.ReleaseClick
NO SYNC Code/70_SMRTK_Core.lua: 0 lines
NO BARE PRINT Code/70_SMRTK_Core.lua: 0 lines
H-10 Code/70_SMRTK_Core.lua: listed
PARSE Code/71_SMRTK_Panel.lua: 0 errors [Lua 5.5]
BUILT Code/71_SMRTK_Panel.lua: 241 lines
FUNCTIONS Code/71_SMRTK_Panel.lua: text, T.Button, T.Page, T.BuildPage, T.RefreshPanel, clamp_position, T.OpenPanel, T.TogglePanel, OnMsg.Shortcuts, restore_panel, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_panel, OnMsg.ChangeMap, OnMsg.PreLoadGame, OnMsg.DoneGame
NO SYNC Code/71_SMRTK_Panel.lua: 0 lines
NO BARE PRINT Code/71_SMRTK_Panel.lua: 0 lines
H-10 Code/71_SMRTK_Panel.lua: listed
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
BUILT Code/72_SMRTK_World.lua: 451 lines
FUNCTIONS Code/72_SMRTK_World.lua: threaded, world, integer, register, preset, first_setting, scheduled, speed, cancel_thread, spawn_colonists, funding, label, row, button, editor, refresh_traits
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
H-10 Code/72_SMRTK_World.lua: listed
PARSE Code/73_SMRTK_Infopanel.lua: 0 errors [Lua 5.5]
BUILT Code/73_SMRTK_Infopanel.lua: 375 lines
FUNCTIONS Code/73_SMRTK_Infopanel.lua: alive, label, member, method_for, object_name, depot_read, T.SelectedActions, selected_button, selected_body, named_child, T.DockMenuItems, close_menu, invoke_menu, build_menu_actions, action, T.RefreshDock, OnMsg.DialogOpen, restore_dock, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_dock, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.DoneGame
NO SYNC Code/73_SMRTK_Infopanel.lua: 0 lines
NO BARE PRINT Code/73_SMRTK_Infopanel.lua: 0 lines
H-10 Code/73_SMRTK_Infopanel.lua: listed
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
BUILT Code/74_SMRTK_Agent.lua: 432 lines
FUNCTIONS Code/74_SMRTK_Agent.lua: object_name, slot_context, bind_slot, T.Bind, T.BindScratch, screenshot, stop_thread, effect_fields, T.Trigger, scalar, field_prepare, field_changed, T.TriggerField, OnMsg.RocketLanded, OnMsg.AsteroidRocketLanded, clear_pins, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, label, row, button, editor, invoke, submit_note, refresh
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
H-10 Code/74_SMRTK_Agent.lua: listed
PARSE Code/75_SMRTK_Saves.lua: 0 errors [Lua 5.5]
BUILT Code/75_SMRTK_Saves.lua: 140 lines
FUNCTIONS Code/75_SMRTK_Saves.lua: realtime, slotname, available, provenance, OnMsg.GatherGameMetadata, OnMsg.GameMetadataLoaded, readmeta, operation, OnMsg.SaveGameStart, label, button
NO SYNC Code/75_SMRTK_Saves.lua: 0 lines
NO BARE PRINT Code/75_SMRTK_Saves.lua: 0 lines
H-10 Code/75_SMRTK_Saves.lua: listed
PARSE Code/76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
BUILT Code/76_SMRTK_Kit.lua: 334 lines
FUNCTIONS Code/76_SMRTK_Kit.lua: scalar, serial, method, realtime, orderkey, hygiene, T.ProbePreflight, invalidate, OnMsg.PreLoadGame, OnMsg.NewGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.EnsureKitLoggers, OnMsg.DataLoaded, OnMsg.InGameInterfaceCreated, OnMsg.DialogOpen, fingerprint, snapshot, differences, label, button
NO SYNC Code/76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT Code/76_SMRTK_Kit.lua: 0 lines
H-10 Code/76_SMRTK_Kit.lua: listed
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 716 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row, last_stamp
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
BUILT Code/80_AgentSlots.lua: 78 lines
FUNCTIONS Code/80_AgentSlots.lua: 
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
H-10 Code/80_AgentSlots.lua: listed
PARSE Code/90_Loggers.lua: 0 errors [Lua 5.5]
PARSE Code/91_Stress.lua: 0 errors [Lua 5.5]
PARSE Code/95_AutoRun.lua: 0 errors [Lua 5.5]
PARSE Code/99_FixtureCarry.lua: 0 errors [Lua 5.5]
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.154 s)
REPAIR PASS SELFTEST: PASS (0.160 s)
STATE COUNTS SELFTEST: PASS (0.142 s)
PUSH SET: 40158 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11946 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: clean
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/72_SMRTK_World.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=45770f8b4ad4799a63912448213b06572b46a08d
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
BUILT Code/72_SMRTK_World.lua: 453 lines
FUNCTIONS Code/72_SMRTK_World.lua: threaded, world, integer, register, preset, first_setting, scheduled, speed, cancel_thread, spawn_colonists, funding, label, row, button, editor, refresh_traits
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
H-10 Code/72_SMRTK_World.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.152 s)
REPAIR PASS SELFTEST: PASS (0.170 s)
STATE COUNTS SELFTEST: PASS (0.145 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 3 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/72_SMRTK_World.lua
  WARN  M Code/76_SMRTK_Kit.lua
  WARN  M Code/77_SMRTK_Stamper.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/76_SMRTK_Kit.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=d183729d1abe0309a8dd3fc424cff91c54a42f49
PARSE Code/76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
BUILT Code/76_SMRTK_Kit.lua: 335 lines
FUNCTIONS Code/76_SMRTK_Kit.lua: scalar, serial, method, realtime, orderkey, hygiene, T.ProbePreflight, invalidate, OnMsg.PreLoadGame, OnMsg.NewGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.EnsureKitLoggers, OnMsg.DataLoaded, OnMsg.InGameInterfaceCreated, OnMsg.DialogOpen, fingerprint, snapshot, differences, label, button
NO SYNC Code/76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT Code/76_SMRTK_Kit.lua: 0 lines
H-10 Code/76_SMRTK_Kit.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.151 s)
REPAIR PASS SELFTEST: PASS (0.202 s)
STATE COUNTS SELFTEST: PASS (0.150 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 2 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/76_SMRTK_Kit.lua
  WARN  M Code/77_SMRTK_Stamper.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py Code/77_SMRTK_Stamper.lua --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9 testkit=c372f4a9e25abc04564fbe085bc756b2c06ef0d1
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 717 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row, last_stamp
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.154 s)
REPAIR PASS SELFTEST: PASS (0.166 s)
STATE COUNTS SELFTEST: PASS (0.185 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: 1 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/77_SMRTK_Stamper.lua
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020
LOAD ORDER: ModDef.LoadCode non-Code pass, then Code pass; each preserves metadata order
PARSE Code/00_TestCore.lua: 0 errors [Lua 5.5]
PARSE Code/10_Probes_Wave1.lua: 0 errors [Lua 5.5]
PARSE Code/20_Probes_Wave2.lua: 0 errors [Lua 5.5]
PARSE Code/30_Probes_Wave3.lua: 0 errors [Lua 5.5]
PARSE Code/40_Probes_Wave4.lua: 0 errors [Lua 5.5]
PARSE Code/50_Probes_Wave5.lua: 0 errors [Lua 5.5]
PARSE Code/55_Probes_Wave6.lua: 0 errors [Lua 5.5]
PARSE Code/56_Probes_Wave7.lua: 0 errors [Lua 5.5]
PARSE Code/57_Probes_Wave8.lua: 0 errors [Lua 5.5]
PARSE Code/58_Probes_Wave9.lua: 0 errors [Lua 5.5]
PARSE Code/59_Probes_Wave10.lua: 0 errors [Lua 5.5]
PARSE Code/61_Probes_Wave11.lua: 0 errors [Lua 5.5]
PARSE Code/62_Probes_Wave12.lua: 0 errors [Lua 5.5]
PARSE Code/63_Probes_Wave13.lua: 0 errors [Lua 5.5]
PARSE Code/64_Probes_Wave14.lua: 0 errors [Lua 5.5]
PARSE Code/66_Probes_Wave15.lua: 0 errors [Lua 5.5]
PARSE Code/60_Probes_Opt.lua: 0 errors [Lua 5.5]
PARSE Code/65_Probes_Rescue.lua: 0 errors [Lua 5.5]
PARSE Code/70_SMRTK_Core.lua: 0 errors [Lua 5.5]
BUILT Code/70_SMRTK_Core.lua: 425 lines
FUNCTIONS Code/70_SMRTK_Core.lua: pack, now, value, append, T.Log, OnMsg.ConsoleLine, T.OnLuaError, OnMsg.OnLuaError, OnMsg.OnThreadError, T.Taint, T.Eligibility, check_taint, T.ArmedCount, T.Action, dispatch, T.Run, T.Arm, T.Disarm, T.Fire, T.DisarmAll, T.Bind, T.Mark, T.CopySince, T.TaintRead, tee, T.PrintTee, T.PanelState, T.SavePanelState, T.ConsoleArm, OnMsg.DataLoading, OnMsg.PreNewMap, OnMsg.PreLoadGame, OnMsg.SavegameSaved, OnMsg.SaveGameStart, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.ConsoleControl, T.AcquireClick, T.ReleaseClick
NO SYNC Code/70_SMRTK_Core.lua: 0 lines
NO BARE PRINT Code/70_SMRTK_Core.lua: 0 lines
H-10 Code/70_SMRTK_Core.lua: listed
PARSE Code/71_SMRTK_Panel.lua: 0 errors [Lua 5.5]
BUILT Code/71_SMRTK_Panel.lua: 241 lines
FUNCTIONS Code/71_SMRTK_Panel.lua: text, T.Button, T.Page, T.BuildPage, T.RefreshPanel, clamp_position, T.OpenPanel, T.TogglePanel, OnMsg.Shortcuts, restore_panel, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_panel, OnMsg.ChangeMap, OnMsg.PreLoadGame, OnMsg.DoneGame
NO SYNC Code/71_SMRTK_Panel.lua: 0 lines
NO BARE PRINT Code/71_SMRTK_Panel.lua: 0 lines
H-10 Code/71_SMRTK_Panel.lua: listed
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
BUILT Code/72_SMRTK_World.lua: 453 lines
FUNCTIONS Code/72_SMRTK_World.lua: threaded, world, integer, register, preset, first_setting, scheduled, speed, cancel_thread, spawn_colonists, funding, label, row, button, editor, refresh_traits
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
H-10 Code/72_SMRTK_World.lua: listed
PARSE Code/73_SMRTK_Infopanel.lua: 0 errors [Lua 5.5]
BUILT Code/73_SMRTK_Infopanel.lua: 375 lines
FUNCTIONS Code/73_SMRTK_Infopanel.lua: alive, label, member, method_for, object_name, depot_read, T.SelectedActions, selected_button, selected_body, named_child, T.DockMenuItems, close_menu, invoke_menu, build_menu_actions, action, T.RefreshDock, OnMsg.DialogOpen, restore_dock, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_dock, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.DoneGame
NO SYNC Code/73_SMRTK_Infopanel.lua: 0 lines
NO BARE PRINT Code/73_SMRTK_Infopanel.lua: 0 lines
H-10 Code/73_SMRTK_Infopanel.lua: listed
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
BUILT Code/74_SMRTK_Agent.lua: 432 lines
FUNCTIONS Code/74_SMRTK_Agent.lua: object_name, slot_context, bind_slot, T.Bind, T.BindScratch, screenshot, stop_thread, effect_fields, T.Trigger, scalar, field_prepare, field_changed, T.TriggerField, OnMsg.RocketLanded, OnMsg.AsteroidRocketLanded, clear_pins, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, label, row, button, editor, invoke, submit_note, refresh
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
H-10 Code/74_SMRTK_Agent.lua: listed
PARSE Code/75_SMRTK_Saves.lua: 0 errors [Lua 5.5]
BUILT Code/75_SMRTK_Saves.lua: 140 lines
FUNCTIONS Code/75_SMRTK_Saves.lua: realtime, slotname, available, provenance, OnMsg.GatherGameMetadata, OnMsg.GameMetadataLoaded, readmeta, operation, OnMsg.SaveGameStart, label, button
NO SYNC Code/75_SMRTK_Saves.lua: 0 lines
NO BARE PRINT Code/75_SMRTK_Saves.lua: 0 lines
H-10 Code/75_SMRTK_Saves.lua: listed
PARSE Code/76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
BUILT Code/76_SMRTK_Kit.lua: 335 lines
FUNCTIONS Code/76_SMRTK_Kit.lua: scalar, serial, method, realtime, orderkey, hygiene, T.ProbePreflight, invalidate, OnMsg.PreLoadGame, OnMsg.NewGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.EnsureKitLoggers, OnMsg.DataLoaded, OnMsg.InGameInterfaceCreated, OnMsg.DialogOpen, fingerprint, snapshot, differences, label, button
NO SYNC Code/76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT Code/76_SMRTK_Kit.lua: 0 lines
H-10 Code/76_SMRTK_Kit.lua: listed
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 717 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row, last_stamp
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
BUILT Code/80_AgentSlots.lua: 78 lines
FUNCTIONS Code/80_AgentSlots.lua: 
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
H-10 Code/80_AgentSlots.lua: listed
PARSE Code/90_Loggers.lua: 0 errors [Lua 5.5]
PARSE Code/91_Stress.lua: 0 errors [Lua 5.5]
PARSE Code/95_AutoRun.lua: 0 errors [Lua 5.5]
PARSE Code/99_FixtureCarry.lua: 0 errors [Lua 5.5]
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.162 s)
REPAIR PASS SELFTEST: PASS (0.164 s)
STATE COUNTS SELFTEST: PASS (0.142 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: clean
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

```text
$ python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered --evidence C:/Dev/smrtk_gate_evidence.md
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020
LOAD ORDER: ModDef.LoadCode non-Code pass, then Code pass; each preserves metadata order
PARSE Code/00_TestCore.lua: 0 errors [Lua 5.5]
PARSE Code/10_Probes_Wave1.lua: 0 errors [Lua 5.5]
PARSE Code/20_Probes_Wave2.lua: 0 errors [Lua 5.5]
PARSE Code/30_Probes_Wave3.lua: 0 errors [Lua 5.5]
PARSE Code/40_Probes_Wave4.lua: 0 errors [Lua 5.5]
PARSE Code/50_Probes_Wave5.lua: 0 errors [Lua 5.5]
PARSE Code/55_Probes_Wave6.lua: 0 errors [Lua 5.5]
PARSE Code/56_Probes_Wave7.lua: 0 errors [Lua 5.5]
PARSE Code/57_Probes_Wave8.lua: 0 errors [Lua 5.5]
PARSE Code/58_Probes_Wave9.lua: 0 errors [Lua 5.5]
PARSE Code/59_Probes_Wave10.lua: 0 errors [Lua 5.5]
PARSE Code/61_Probes_Wave11.lua: 0 errors [Lua 5.5]
PARSE Code/62_Probes_Wave12.lua: 0 errors [Lua 5.5]
PARSE Code/63_Probes_Wave13.lua: 0 errors [Lua 5.5]
PARSE Code/64_Probes_Wave14.lua: 0 errors [Lua 5.5]
PARSE Code/66_Probes_Wave15.lua: 0 errors [Lua 5.5]
PARSE Code/60_Probes_Opt.lua: 0 errors [Lua 5.5]
PARSE Code/65_Probes_Rescue.lua: 0 errors [Lua 5.5]
PARSE Code/70_SMRTK_Core.lua: 0 errors [Lua 5.5]
BUILT Code/70_SMRTK_Core.lua: 425 lines
FUNCTIONS Code/70_SMRTK_Core.lua: pack, now, value, append, T.Log, OnMsg.ConsoleLine, T.OnLuaError, OnMsg.OnLuaError, OnMsg.OnThreadError, T.Taint, T.Eligibility, check_taint, T.ArmedCount, T.Action, dispatch, T.Run, T.Arm, T.Disarm, T.Fire, T.DisarmAll, T.Bind, T.Mark, T.CopySince, T.TaintRead, tee, T.PrintTee, T.PanelState, T.SavePanelState, T.ConsoleArm, OnMsg.DataLoading, OnMsg.PreNewMap, OnMsg.PreLoadGame, OnMsg.SavegameSaved, OnMsg.SaveGameStart, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.ConsoleControl, T.AcquireClick, T.ReleaseClick
NO SYNC Code/70_SMRTK_Core.lua: 0 lines
NO BARE PRINT Code/70_SMRTK_Core.lua: 0 lines
H-10 Code/70_SMRTK_Core.lua: listed
PARSE Code/71_SMRTK_Panel.lua: 0 errors [Lua 5.5]
BUILT Code/71_SMRTK_Panel.lua: 241 lines
FUNCTIONS Code/71_SMRTK_Panel.lua: text, T.Button, T.Page, T.BuildPage, T.RefreshPanel, clamp_position, T.OpenPanel, T.TogglePanel, OnMsg.Shortcuts, restore_panel, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_panel, OnMsg.ChangeMap, OnMsg.PreLoadGame, OnMsg.DoneGame
NO SYNC Code/71_SMRTK_Panel.lua: 0 lines
NO BARE PRINT Code/71_SMRTK_Panel.lua: 0 lines
H-10 Code/71_SMRTK_Panel.lua: listed
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
BUILT Code/72_SMRTK_World.lua: 453 lines
FUNCTIONS Code/72_SMRTK_World.lua: threaded, world, integer, register, preset, first_setting, scheduled, speed, cancel_thread, spawn_colonists, funding, label, row, button, editor, refresh_traits
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
H-10 Code/72_SMRTK_World.lua: listed
PARSE Code/73_SMRTK_Infopanel.lua: 0 errors [Lua 5.5]
BUILT Code/73_SMRTK_Infopanel.lua: 375 lines
FUNCTIONS Code/73_SMRTK_Infopanel.lua: alive, label, member, method_for, object_name, depot_read, T.SelectedActions, selected_button, selected_body, named_child, T.DockMenuItems, close_menu, invoke_menu, build_menu_actions, action, T.RefreshDock, OnMsg.DialogOpen, restore_dock, OnMsg.InGameInterfaceCreated, OnMsg.PostLoadGame, OnMsg.CurrentMapChangeDone, drop_dock, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.DoneGame
NO SYNC Code/73_SMRTK_Infopanel.lua: 0 lines
NO BARE PRINT Code/73_SMRTK_Infopanel.lua: 0 lines
H-10 Code/73_SMRTK_Infopanel.lua: listed
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
BUILT Code/74_SMRTK_Agent.lua: 432 lines
FUNCTIONS Code/74_SMRTK_Agent.lua: object_name, slot_context, bind_slot, T.Bind, T.BindScratch, screenshot, stop_thread, effect_fields, T.Trigger, scalar, field_prepare, field_changed, T.TriggerField, OnMsg.RocketLanded, OnMsg.AsteroidRocketLanded, clear_pins, OnMsg.PreLoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, label, row, button, editor, invoke, submit_note, refresh
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
H-10 Code/74_SMRTK_Agent.lua: listed
PARSE Code/75_SMRTK_Saves.lua: 0 errors [Lua 5.5]
BUILT Code/75_SMRTK_Saves.lua: 140 lines
FUNCTIONS Code/75_SMRTK_Saves.lua: realtime, slotname, available, provenance, OnMsg.GatherGameMetadata, OnMsg.GameMetadataLoaded, readmeta, operation, OnMsg.SaveGameStart, label, button
NO SYNC Code/75_SMRTK_Saves.lua: 0 lines
NO BARE PRINT Code/75_SMRTK_Saves.lua: 0 lines
H-10 Code/75_SMRTK_Saves.lua: listed
PARSE Code/76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
BUILT Code/76_SMRTK_Kit.lua: 335 lines
FUNCTIONS Code/76_SMRTK_Kit.lua: scalar, serial, method, realtime, orderkey, hygiene, T.ProbePreflight, invalidate, OnMsg.PreLoadGame, OnMsg.NewGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, T.EnsureKitLoggers, OnMsg.DataLoaded, OnMsg.InGameInterfaceCreated, OnMsg.DialogOpen, fingerprint, snapshot, differences, label, button
NO SYNC Code/76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT Code/76_SMRTK_Kit.lua: 0 lines
H-10 Code/76_SMRTK_Kit.lua: listed
PARSE Code/77_SMRTK_Stamper.lua: 0 errors [Lua 5.5]
BUILT Code/77_SMRTK_Stamper.lua: 717 lines
FUNCTIONS Code/77_SMRTK_Stamper.lua: integer, name_ok, key, member, field, kind, api, keys_ok, array_count, L.Normalize, serialize, L.Export, saved, L.Names, L.Resolve, T.RegisterLayout, world, alive, available, special, skip_capture, capture, contains, add_building, template, shape_cells, bounds, inspect_building, line_test, L.Plan, log_plan, stamp_skip, settle, complete_building, execute_stamp, check, reset, OnMsg.SaveGameStart, OnMsg.SavegameSaved, OnMsg.PreLoadGame, OnMsg.LoadGame, OnMsg.ChangeMap, OnMsg.CurrentMapChange, OnMsg.DoneGame, text, row, last_stamp
NO SYNC Code/77_SMRTK_Stamper.lua: 0 lines
NO BARE PRINT Code/77_SMRTK_Stamper.lua: 0 lines
H-10 Code/77_SMRTK_Stamper.lua: listed
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
BUILT Code/80_AgentSlots.lua: 78 lines
FUNCTIONS Code/80_AgentSlots.lua: 
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
H-10 Code/80_AgentSlots.lua: listed
PARSE Code/90_Loggers.lua: 0 errors [Lua 5.5]
BUILT Code/90_Loggers.lua: 359 lines
FUNCTIONS Code/90_Loggers.lua: SMRTest.LoggerState, toggle, SMRTest.Loggers, stamp, predicted, SMRTest.ReportReservations, SMRTest.ReportBrokenTrack, SMRTest.ReportTrains
NO SYNC Code/90_Loggers.lua: 0 lines
NO BARE PRINT Code/90_Loggers.lua: 0 lines
H-10 Code/90_Loggers.lua: listed
PARSE Code/91_Stress.lua: 0 errors [Lua 5.5]
PARSE Code/95_AutoRun.lua: 0 errors [Lua 5.5]
PARSE Code/99_FixtureCarry.lua: 0 errors [Lua 5.5]
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.154 s)
REPAIR PASS SELFTEST: PASS (0.176 s)
STATE COUNTS SELFTEST: PASS (0.165 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: clean
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
COORDINATOR GATES: PASS
```

## Final independent desk commands - verbatim

```text
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020

$ python docs/agent/reports/SMRTK_FANOUT_SMOKE.py
SITTING SYNTAX: not rerun; 02 has been consumed (use its git grave)
CORE SMOKE: PASS — formatting/flush, native absent/present, overflow, clipboard, tee restore/returns, lifecycle cleanup, taint RED, failures, slots, persistence, console false/true
PANEL SMOKE: PASS — registry, collapse, tabs, stubs, fixed side position, toggle, shortcut, reload reconstruction (mock X classes; no rendering claim)
FANOUT CORE: PASS — chrome sinks, evidence screen, exclusive clicks, UI exclusion, save/load/map cleanup, one actual restore

$ python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest --list
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
BEHAVIOR: PASS — idle identity, all 7 quiet gates/manual bypass/active preservation, logger refusal, lifecycle restoration, stale meteor clicks, speed clamps, run-until cancellation, sweeps, spawn/funding contracts, traits, rocket wait, UI thread dispatch
PLAY: NOT RUN — doubles prove control flow only
HEAD pack=8a833bc TestKit=cee5bab
WORLD REGISTRY: 55 actions
applicants_100 | Applicants 100 | menu=true
applicants_50 | Applicants 50 | menu=true
close_domes | Close all domes | menu=true
cold_wave | Cold wave | menu=true
complete_constructions | Complete constructions | menu=true
complete_grids | Complete wires / pipes | menu=true
dust_devil | Dust devil | menu=false
dust_devil_major | Major dust devil | menu=false
dust_storm | Dust storm | menu=true
dust_storm_electrostatic | Electrostatic storm | menu=true
dust_storm_great | Great dust storm | menu=true
fill_storages | Fill all storages | menu=true
fix_all | Fix all buildings | menu=true
funding | Change funding (native amount) | menu=false
funding_minus | Funding -500M | menu=true
funding_plus | Funding +500M | menu=true
malfunction_all | Malfunction all buildings | menu=true
marsquake | Marsquake | menu=true
meteor_multispawn | Meteor multispawn | menu=arm
meteor_single | Meteor single | menu=arm
meteor_storm | Meteor storm | menu=arm
open_domes | Open all domes | menu=true
pause | Pause / Resume | menu=true
quiet | Quiet scheduled disasters | menu=arm
rains | Rains | menu=true
research_all | Research all visible Main techs | menu=true
rocket_arrive | Finish selected rocket flight | menu=true
run_until | Run until sol / trigger | menu=false
spawn_children_1 | Children 1 | menu=true
spawn_children_10 | Children 10 | menu=true
spawn_children_100 | Children 100 | menu=true
spawn_colonists | Spawn colonists | menu=false
spawn_colonists_1 | Colonists 1 | menu=true
spawn_colonists_10 | Colonists 10 | menu=true
spawn_colonists_100 | Colonists 100 | menu=true
spawn_martian_children_1 | Martian-born children 1 | menu=true
spawn_martian_children_10 | Martian-born children 10 | menu=true
spawn_martian_children_100 | Martian-born children 100 | menu=true
spawn_martian_colonists_1 | Martian-born colonists 1 | menu=true
spawn_martian_colonists_10 | Martian-born colonists 10 | menu=true
spawn_martian_colonists_100 | Martian-born colonists 100 | menu=true
speed | Set speed | menu=false
speed_fast | Fast speed | menu=true
speed_normal | Normal speed | menu=true
speed_ultra | Ultra speed | menu=true
stop_disaster | Stop disaster | menu=true
tech_points_1 | Tech points 1 | menu=true
tech_points_10 | Tech points 10 | menu=true
tech_points_100 | Tech points 100 | menu=true
trait_add | Add trait | menu=false
trait_remove | Remove trait | menu=false
underground_cave_in | Cave-in at cursor | menu=false
underground_marsquake | Underground marsquake | menu=true
unlock_buildings | Unlock all buildings | menu=true
unpin_all | Unpin all objects | menu=true
FALSIFIER quiet: RED as required
FALSIFIER stale-click: RED as required

$ python docs/agent/reports/SMRTK_P2_SMOKE.py
PACK HEAD: 8a833bc
TESTKIT HEAD: cee5bab
P2 SHA256: 3dbbce3a4c093de6b033f31f476707473228593aa2b3bae4b5f22762bedd83ea
P2 PARSE: PASS [Lua 5.5]
RULE 6: 0 lines []
RULE 7: 0 lines []
FORBIDDEN STATE: 0 lines []
RULE 6 PRESENCE: 26 lines
P2 DESK: PASS — selected guards, single/multi depots, busy refusal, dynamic companions, injection/order/idempotence, queued selection race, fallback, argument-safe menus, late actions, one primary per click, arms, side page, CLEAN/TAINTED/UNKNOWN/errors, lifecycle
P2 CATALOG: 21 selected leaf actions + 4 companion registry ids; actual objects show supported subsets
P2 LIMIT: fake X controls and game services; no rendering, save mutation, or in-game no-taint claim

$ python docs/agent/reports/SMRTK_P3_SMOKE.py
PARSE Code/74_SMRTK_Agent.lua: 0 errors [Lua 5.5]
NO SYNC Code/74_SMRTK_Agent.lua: 0 lines
NO BARE PRINT Code/74_SMRTK_Agent.lua: 0 lines
PARSE Code/80_AgentSlots.lua: 0 errors [Lua 5.5]
NO SYNC Code/80_AgentSlots.lua: 0 lines
NO BARE PRINT Code/80_AgentSlots.lua: 0 lines
PASS template idle and original dispatch identity
PASS slots context, scratch, legacy binding, refused armed rebind
PASS exclusive click, delayed actual dispatch, stale click cancellation
PASS partial arm cleanup and click error fail closed
PASS every lifecycle disarms triggers and slots, deleting poll threads
PASS once trigger, repeat edges, action ownership, predicate failure
PASS scalar watch nil, false, adjacent changes, table refusal, invalid object
PASS mark-relative error and post-arm rocket builtins
PASS screenshot native return, fallback, failure and single MARK result
PASS trigger screenshot executes in real-time thread, then one trigger result
PASS queued trigger cancellation and screenshot completion after lifecycle disarm
PASS Agent UI note Enter, native shortcut forwarding, seven slots and live registry
PASS post-action taint and non-unwinding error remain visible
P3 DESK: PASS (mock services; no rendering, timing, disk-write or game claim)
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0
HEAD testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020

$ python docs/agent/reports/SMRTK_P4_SMOKE.py
PARSE 75_SMRTK_Saves.lua: 0 errors [Lua 5.5]
NO SYNC 75_SMRTK_Saves.lua: 0 lines
NO BARE PRINT 75_SMRTK_Saves.lua: 0 lines
PROBE TOKEN 75_SMRTK_Saves.lua: 0 lines
PARSE 76_SMRTK_Kit.lua: 0 errors [Lua 5.5]
NO SYNC 76_SMRTK_Kit.lua: 0 lines
NO BARE PRINT 76_SMRTK_Kit.lua: 0 lines
PROBE TOKEN 76_SMRTK_Kit.lua: 0 lines
PARSE 90_Loggers.lua: 0 errors [Lua 5.5]
PASS idle has no logger/trigger arms or callback replacements
PASS saves refuse UI/game-time callers and native busy before mutation
PASS real-time yielding save has one result, fixed slot name and provenance
PASS foreign/missing provenance refuses before LoadGame; override logged once
PASS metadata errors block override; save/load errors release toolkit lock
PASS metadata race with new save refuses load after mount
PASS probes default-refuse and dishonest/incomplete stamp refuses
PASS provisioned desktop stamp enables both run routes and expires on registry/map
PASS named sweep hits require exact stdout and explicit needed-probe declaration
PASS logger state copy cannot mutate native state and manual arms are refused
PASS toolkit logger arms/restores on lifecycle and refuses quiet layering
PASS fingerprint reads public registry and live ModDef without ListFixes
PASS dump preserves false flags and snapshot numeric diff observes detached data
PASS watch registers disarmed P3 trigger; selection change never retargets; auto-cleanup
PASS force console uses existing arm only and refuses missing arm
PASS page callbacks queue actual Run/Arm in real-time with one primary result
PASS synthetic taint is asserted after real save action completes
P4 DESK: 17 falsifiers PASS; fake natives/UI, no save/load or rendering play claim

$ python docs/agent/reports/SMRTK_P5_DESK.py
$ python docs/agent/reports/SMRTK_P5_DESK.py
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020
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

$ python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest
$ python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest
HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020
LOAD Code/70_SMRTK_Core.lua
LOAD Code/71_SMRTK_Panel.lua
LOAD Code/72_SMRTK_World.lua
LOAD Code/73_SMRTK_Infopanel.lua
LOAD Code/74_SMRTK_Agent.lua
LOAD Code/75_SMRTK_Saves.lua
LOAD Code/76_SMRTK_Kit.lua
LOAD Code/77_SMRTK_Stamper.lua
LOAD Code/80_AgentSlots.lua
LOAD Code/90_Loggers.lua
PASS co-load is idle, selected companions and World follow-ups resolve
PASS actual90 logger and quiet refuse nesting and restore captured functions
PASS P4 field-watch command creates P3 trigger without implicit arming or retarget
PASS MARK hook follows primary evidence and covers ordinary and screenshot marks
PASS all advanced pages build in one body with sibling scrollbar and bounded tabs
REGISTRY Selected: Add Dust [selected_add_dust]; Add Maintenance [selected_add_maintenance]; Add Prefab [selected_add_prefab]; Clean & Fix [selected_clean_fix]; Delete [selected_delete]; Destroy (blow up) [selected_destroy]; Empty [selected_empty]; Fill [selected_fill]; Malfunction [selected_malfunction]; Spawn Child [selected_spawn_child]; Spawn Colonist [selected_spawn_colonist]; Spawn Drone [selected_spawn_drone]; Spawn Shuttle [selected_spawn_shuttle]; Spawn Visitor [selected_spawn_visitor]; Spawn Worker [selected_spawn_worker]; Upgrade 1 [selected_upgrade_1]; Upgrade 2 [selected_upgrade_2]; Upgrade 3 [selected_upgrade_3]; Upgrade 4 [selected_upgrade_4]; Upgrade 5 [selected_upgrade_5]; Upgrade 6 [selected_upgrade_6]
REGISTRY Agent: First Lua error since mark [trigger_error]; Next rocket landed [trigger_rocket]; Note [note]; Pin A [pin_A]; Pin B [pin_B]; Pin C [pin_C]; Screenshot + Mark [screenshot_mark]; Selected field changed [trigger_field]; Sol >= target [trigger_sol]; Watch command [watch_selected_field]
REGISTRY World: Add trait [trait_add]; Applicants 100 [applicants_100]; Applicants 50 [applicants_50]; Cave-in at cursor [underground_cave_in]; Change funding (native amount) [funding]; Children 1 [spawn_children_1]; Children 10 [spawn_children_10]; Children 100 [spawn_children_100]; Close all domes [close_domes]; Cold wave [cold_wave]; Colonists 1 [spawn_colonists_1]; Colonists 10 [spawn_colonists_10]; Colonists 100 [spawn_colonists_100]; Complete constructions [complete_constructions]; Complete wires / pipes [complete_grids]; Dust devil [dust_devil]; Dust storm [dust_storm]; Electrostatic storm [dust_storm_electrostatic]; Fast speed [speed_fast]; Fill all storages [fill_storages]; Finish selected rocket flight [rocket_arrive]; Fix all buildings [fix_all]; Funding +500M [funding_plus]; Funding -500M [funding_minus]; Great dust storm [dust_storm_great]; Major dust devil [dust_devil_major]; Malfunction all buildings [malfunction_all]; Marsquake [marsquake]; Martian-born children 1 [spawn_martian_children_1]; Martian-born children 10 [spawn_martian_children_10]; Martian-born children 100 [spawn_martian_children_100]; Martian-born colonists 1 [spawn_martian_colonists_1]; Martian-born colonists 10 [spawn_martian_colonists_10]; Martian-born colonists 100 [spawn_martian_colonists_100]; Meteor multispawn [meteor_multispawn]; Meteor single [meteor_single]; Meteor storm [meteor_storm]; Normal speed [speed_normal]; Open all domes [open_domes]; Pause / Resume [pause]; Quiet scheduled disasters [quiet]; Rains [rains]; Remove trait [trait_remove]; Research all visible Main techs [research_all]; Run until sol / trigger [run_until]; Set speed [speed]; Spawn colonists [spawn_colonists]; Stop disaster [stop_disaster]; Tech points 1 [tech_points_1]; Tech points 10 [tech_points_10]; Tech points 100 [tech_points_100]; Ultra speed [speed_ultra]; Underground marsquake [underground_marsquake]; Unlock all buildings [unlock_buildings]; Unpin all objects [unpin_all]
REGISTRY Saves: Load A [load_A]; Load B [load_B]; Load C [load_C]; Override load A [load_override_A]; Override load B [load_override_B]; Override load C [load_override_C]; Save A [save_A]; Save B [save_B]; Save C [save_C]
REGISTRY Kit: Diff latest snapshots [snapshot_diff]; Dump selected [dump_selected]; Fingerprint [fingerprint]; Logger AutoCargo [logger_AutoCargo]; Logger CargoReady [logger_CargoReady]; Logger DroneChurn [logger_DroneChurn]; Logger DustDevils [logger_DustDevils]; Logger Meteors [logger_Meteors]; Logger WorkShift [logger_WorkShift]; Open console [console_open]; Print tee [print_tee]; Run all probes [run_all]; Run selected probe [run_probe]; Watch selected field [watch_field]; World snapshot [snapshot]; probe_preflight [probe_preflight]
REGISTRY Stamper: Add 10 colonists [layout_spawn_colonists]; Apply captured upgrades [layout_upgrades_start]; Cancel layout target [layout_cancel]; Capture map [layout_capture_map]; Capture rectangle [layout_arm_rectangle]; Capture selected [layout_capture_selected]; Copy layout [layout_copy]; Fill storages (all maps) [layout_fill_storages]; Funding +500M [layout_funding]; Layout target [layout_target]; Next saved layout [layout_next]; Plan at click [layout_arm_plan]; Stamp at click [layout_arm_stamp]
MERGE DESK: PASS (mock services; no native render, save round trip or stamp claim)
FALSIFIER editor World: RED as required
FALSIFIER editor Kit: RED as required
FALSIFIER editor Stamper: RED as required

$ python tools/parsecheck.py --dir C:\Dev\SMR-BugFixPack-TestKit\Code --quiet
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]
```

## Consumed-prompt close-out doccheck - verbatim

HEAD pack=8a833bc48be93393291c49b419df99f5a79e8cf0 testkit=cee5bab230f2fac876aa0e6d86bb97f6b56ad020

```text
$ python tools/doccheck.py
ENTRIES: 191 files (2 grouped), 226 preserved index rows, 188 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x188
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
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (226 rows)
FACTS: 101 files, 60 state an observation date, 3579 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (101 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
PROMPT MAP: PASS — 13 perma + 7 one-off row(s) agree with disk in both directions; no tombstones
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 11979 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 128 checklist items, 50 marked, 7 waiting on the owner, 28 need a marker
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 13 D + 94 C = 226 (in 191 entry files)
STATE BUILD STATE: fresh — regeneration reproduces the region byte for byte
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 47 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 47 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 47 file(s) in Code/, items.lua and metadata.lua's code list agree by name
PACK IGNORE PARITY: PASS — 15 filters agree in order
FLPK SELFTEST: PASS (nested + shallow; the pack reader owns every descendant span)
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
CK170 SELFTEST: PASS (0.193 s)
REPAIR PASS SELFTEST: PASS (0.178 s)
STATE COUNTS SELFTEST: PASS (0.144 s)
PUSH SET: 40191 B in 5 file(s) ≈ 19k tokens (budget 40960 B)
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      11979 B
    prompts/perma/GENERAL_USE_PROMPT.md       4227 B
    prompts/perma/DISPATCH.md                10500 B
    MEMORY.md (Claude, outside the repo)     10979 B
TESTKIT TREE: clean
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
doccheck: GREEN
```
