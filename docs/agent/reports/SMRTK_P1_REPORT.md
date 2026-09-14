# SMRTK 03A P1 — World build claims

2026-09-13, Codex, owner seat Sol/high. Source build 24995074.
`python tools/doccheck.py --emit-fingerprint` emitted the 1.1.0 group HOLDS
and `doccheck: GREEN`; the relevant initiation/travel leaves were then opened.
Desk evidence below was emitted at pack `e245d80`, TestKit `965fb08`.
This payload edits only `Code/72_SMRTK_World.lua` and this report/falsifier;
it does not commit, remove prompts, or edit metadata/core/panel.

## Disagreements and limits first

Disaster leaves create their own native game-time threads. A toolkit result
with `outcome=leaf_dispatched` witnesses a leaf invocation, **not a disaster
starting or finishing**. `stop_requested` likewise requests the native stop.
Quiet's `SMRTK_FIRE outcome=scheduled_start_held` witnesses a scheduler entry
being delayed before its original; it is **not** a disaster effect.
No World behavior or achievement eligibility is claimed in play.

The rocket action finishes a selected modern rocket's travel wait to our
colony, then observes the command leaving `CmdFlyToLocation`. It preserves
normal arrival policy and does not choose a landing site. A legacy
`RocketBase:FlyToMars` object refuses visibly. Its global instant-travel
message also releases Earth-bound flights; that route is not a bounded
selected-rocket action.

## Numbered falsifiable claims

All claims 1–8 are falsifiable with one command:
`python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest --list`.
The doubles exercise the actual World file and frozen core dispatch; they
cannot establish native behavior or rendering.

1. **Disasters built:** `dust_storm`, `dust_storm_electrostatic`,
   `dust_storm_great` call `CheatDustStorm(type,setting)`;
   `dust_devil`/`dust_devil_major` call `CheatDustDevil(major,setting,pos)`;
   `cold_wave`, `marsquake`, `rains` call their explicit globals.
   `underground_cave_in` validates environment/cursor;
   `underground_marsquake` validates environment. The intensity controls
   use `PresetsCombo("MapSettings", group)()` and validate the chosen id.
   Parameterless menu contracts choose the first valid shipped preset,
   reported as `setting=`; page controls permit an explicit intensity.
   Meteors use only AcquireClick/ReleaseClick, fire in guarded real-time
   threads, consume one map click, and cancel on second arm/right click
   or core lifecycle disarm. Two queued clicks cannot fire twice; an old
   click cannot mutate after disarm/re-arm. **Stopped:** native effect
   verification is reserved for 08.
2. **Quiet built:** off by default, seven temporary initiation wrappers.
   `StartDustStorm` gates `scheduler_owned=true`; `StartColdWave`,
   `GenerateDustDevilIn`, `MeteorsDisaster`, `TriggerMarsquake`, and
   `FindEpicentre` identify the exact periodic thread with
   `GetPeriodicRepeatThread`; `RainProcedure` gates non-cheat new entries.
   Source: DustStorm.lua:353,514–532; ColdWave.lua:101,166–189;
   DustDevils.lua:128,235–274; Meteors.lua:308–352;
   Marsquake.lua:42–55,271,336–350; TerraformingDisasters.lua:188,352–381;
   CommonLua/Core/lib.lua:1668–1676. Already running bodies retain their
   original stack, dust-devil minions bypass the periodic gate, manual
   leaves pass, and quiet never calls the stop leaf. Pending starts remain
   held across a rapid quiet disarm/re-arm. Disarm restores every captured
   global it still owns; foreign replacements are preserved. Core save,
   load, map-change and DoneGame routes remove these wrappers. Arming
   dynamically reads `SMRTest.LoggerState()` and refuses any enabled
   logger or armed `logger_` action. Missing accessor refuses safely.
   **Stopped:** actual scheduler provocation/active-disaster preservation
   must be witnessed in 08; logger/quiet co-load is coordinator merge work.
3. **Speed built:** normal, fast, numeric ultra (128 ×), pause/resume;
   generic `speed` refuses out-of-range requests. Source
   CommonLua/Core/const.lua:127–129, Features/GameSpeed.lua:49–80,
   Lua/Config/config.lua:116–125. Numeric ultra is accepted by the source
   route; the toolkit never changes limits or forces native time factor.
   `SMRTK_SPEED clamped_by=<reason>` reports native clamps.
   `run_until` arms ultra, polls future sol or a dynamically resolved armed
   Agent trigger, then fires pause/cue inside a guarded real-time thread.
   Trigger form observes `T.fires` **attempts**, including failed attempts,
   because that is the frozen core counter contract. Loss/replacement of
   the target arm cancels the run-until watcher. **Stopped:** native ultra
   and clamps remain source-derived until 08.
4. **Building sweeps built:** `fix_all` and `malfunction_all` use
   `AllMapsForEach(true,"Building",callback)`; maintenance-ineligible
   buildings are skipped and counts are logged. Malfunction counts actual
   membership changes. Source map.lua:1125–1129,
   Building.lua:1944–1947, RequiresMaintenance.lua:374 onward.
   **Stopped:** native object mutation is untested in play.
5. **Waits built:** current-map constructions and wires/pipes call their
   explicit leaves (Cheats.lua:55–103). `rocket_arrive` requires a selected
   `UniversalRocketBase`, our-colony destination, running unpaused command
   inside `SleepFlight`, and positive remaining travel time. It applies
   `AddFlightTime(-remaining)` and wakes only that command thread, then
   observes its command for up to 2 real-time seconds. Failure/timeout
   refuses; `config.RocketInstantTravel` is untouched. Source
   UniversalRocket.lua:271–302,1085–1150; RocketBase.lua:233–283;
   RocketUtilities.lua:546–552. Desk `travel_wait_finished` is a **mock
   arrival-policy observation**, never a witnessed game arrival.
6. **Re-exposures built:** exact P5 contracts `fill_storages()`;
   `spawn_colonists(integer count[,Child[,martianborn]])`;
   `funding(native integer amount)`. Spawn checks observed colonist-label
   growth and refuses mismatches. Zero-argument 1/10/100 variants include
   adults, children, Martian-born adults/children; applicants 50/100;
   funding ±500000000; tech points 1/10/100; research visible Main techs;
   unlock buildings; open/close domes; unpin all. Variants share local leaf
   helpers and each produces one primary dispatch record. Source
   Cheats.lua:106–119,151–205; ApplicantsPool.lua:192;
   CheatDef.lua:3–145,808–865; TechTree.lua:721,1200;
   Dome.lua:4034–4050; PinnableObject.lua:79–87;
   StorageDepot.lua:710 onward. Fill preserves the preset's depot sweep,
   using each object's actual CheatFill implementation. **Stopped:**
   counters/amounts and achievement taint still require native 08 readings.
7. **Traits built:** shipped category/trait selection on World;
   `trait_add`/`trait_remove` require a selected colonist and valid id,
   refuse duplicate/missing/locked traits, call AddTrait/RemoveTrait and
   verify membership changed. Source Colonist.lua:473–530 onward.
   **Stopped:** per-object mirror is P2/judge scope.
8. **UI/dispatch built:** World page construction has no world mutations.
   Its buttons capture arguments before queuing, then call Run/Arm/Disarm
   within real-time threads. Generic mutation actions refuse bare UI or
   console dispatch without a yielding thread. Native menu invokes complete
   zero-argument run/arm contracts; raw parameter actions have no menu.
   Registered callback functions are never invoked as a substitute for
   Run/Fire. The core supplies one logger and post-dispatch taint assertions.

## Exact desk gate output

Command `python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest`:

```text
PARSE Code/72_SMRTK_World.lua: 0 errors [Lua 5.5]
NO SYNC Code/72_SMRTK_World.lua: 0 lines
NO BARE PRINT Code/72_SMRTK_World.lua: 0 lines
BEHAVIOR: PASS — idle identity, all 7 quiet gates/manual bypass/active preservation, logger refusal, lifecycle restoration, stale meteor clicks, speed clamps, run-until cancellation, sweeps, spawn/funding contracts, traits, rocket wait, UI thread dispatch
PLAY: NOT RUN — doubles prove control flow only
HEAD pack=e245d80 TestKit=965fb08
FALSIFIER quiet: RED as required
FALSIFIER stale-click: RED as required
```

`python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet`
emitted `PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]`.
The explicit `rg -n 'NetSyncEvent|LogCheatUsed'` and
`rg -n '^\s*print\('` on `72_SMRTK_World.lua` each emitted no lines
(rg exit 1 is its no-match result). `python tools/doccheck.py` emitted
`doccheck: GREEN`; its warnings are quoted below. `tasklist /FI
"IMAGENAME eq Mars.exe"` emitted `INFO: No tasks are running which match
the specified criteria.` before the first Code write.

## OWNER-ROUTED / recommendations for 03B consolidation

- 08 should provoke each quiet initiation while a prior disaster is active,
  then disarm/re-arm and save/load once; require route-held FIRE and a map
  witness. Recommend retaining scheduler delay rather than stop/re-arm.
- Recommend the modern selected-rocket travel completion with ordinary
  operator landing-site selection. Keep legacy/refugee/foreign-aid route
  refusals visible; do not introduce a global travel toggle/message.
- Recommend pausing on any target trigger attempt for operator review.
  `T.fires` is not a successful-fire counter. If the owner wants success-only
  run-until, 03B should settle a P3 success signal before 07 documents it.

## For 07 — final buttons and metadata request

`python docs/agent/reports/SMRTK_P1_SMOKE.py --list` emits the exact
55-action World registry with native-menu contracts.
The page buttons are: three dust storms; two dust devils; cold wave;
Marsquake; rains (each intensity combo + Trigger); three meteor arm buttons
(shared intensity combo); Underground cave-in/quake; quiet; stop disaster;
normal/fast/ultra; pause/resume; run-until sol/trigger + cancel;
fix all/malfunction all/fill storages; complete constructions/grids/selected
rocket flight; research all/unlock buildings; open/close domes/unpin;
applicants 50/100; funding ±500M; tech points 1/10/100;
adults/children/Martian-born adults/Martian-born children each 1/10/100;
trait category + id combos with Add/Remove.

Parameterized registry-only helpers are `speed`, `spawn_colonists`, and
`funding`; sitting code calls them inside its yielding slot thread. No extra
input-required menu entry was added. Requested TestKit metadata line:
`"Code/72_SMRTK_World.lua",` immediately after the panel line and before P2.
Coordinator owns that change.

## DRIFT

- Initial source searches named the payload's nonexistent Disasters directory
  and singular DustDevil filename; errors were read and explicit files opened.
- The first quiet draft allowed RainProcedure re-entry whenever any rain was
  active; corrected to hold every new non-cheat entry. Existing bodies do not
  re-enter this function to continue.
- An old quiet waiter initially exited its old state after rapid re-arm;
  corrected to respect the new arm and added that negative test.
- The first UI double did not insert Button children; its assertion failed,
  then the double was repaired. No behavior PASS was taken from that run.
- Mutant harness initially expected generic assertion text despite custom
  assertion messages; corrected to require each specific counterfeit failure.
- Full-tree gates observed parallel P4 changes and report-only alias warnings;
  this payload neither restores nor edits those files.

## DEPARTURES

- Quiet uses armed-only initiation wrappers and scheduler delays instead of
  a nonexistent common WaitDisaster wrapper. ARM/DISARM log on/off; FIRE logs
  held starts. No duplicate QUIET primary record. Checked against one logger,
  zero idle patches, restoration, and active-disaster preservation.
- Rocket control completes travel to orbit and refuses legacy/unready flights;
  it does not select a terrain landing site. The one-shot wake preserves normal
  arrival policy and avoids a persistent or colony-wide debug toggle.
- Raw input actions are registry helpers; complete presets expose menu=true
  or menu="arm". World page adds explicit yielding-thread button callbacks
  instead of changing the frozen Button/core.
- Research all preserves the preset's visible Main-tech scope, expressed in
  its button label; it does not secretly research hidden/unreachable techs.

## SUGGESTIONS

Use a P3 successful-fire sequence if run-until should ignore failed trigger
attempts; the core counter alone cannot supply that meaning. 08 should compare
leaf dispatch records with native disaster-start messages rather than count
OK records as visible world success. A future menu refinement can expose
explicit intensity submenus instead of the parameterless first-valid-preset
contract; the existing World combos already expose the full choice.

## Doccheck warnings — verbatim desk output

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
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
TESTKIT TREE: 4 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN  M Code/90_Loggers.lua
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
```

## Coordinator post-release editor correction

Native XTextEditor.Init clears lines; constructor Text does not initialize
the editor. Coordinator explicitly calls SetText after construction in this
payload, independently gated/committed by file. Source: XTextEditor171-175,
221-228 and XControl624-634. The stricter combined merge model discards
constructor Text and the specific missing-setter counterfeit goesRED. The
original payload smoke did not establish this native initialization behavior.
