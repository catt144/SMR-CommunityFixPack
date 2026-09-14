# SMRTK 03A / P3 — Agent page and sitting slot contract

2026-09-13, Codex P3 payload (owner seat Astra/xhigh). Builder claims only;
03B remains the independent Claude judge. No game was launched.
Upstream spike `8d1a6aa`; frozen TestKit core `265fde7`, panel `05c7e45`.
Final desk run emitted pack `e245d8028e9d648f02453b5b4230b52155439bd9`,
TestKit `05c7e45552006d2dcc28a4a49c446f288d74d356`.

## Disagreements first

- The payload's literal `do = { ... }` is invalid Lua: `do` is a keyword.
  The implemented and documented spelling is `["do"] = { ... }`.
- Frozen `Fire` always emits `SMRTK_FIRE`, irrespective of `def.verb`.
  Registered triggers therefore use guarded `Run(id)` from their effect
  thread to emit the required single `SMRTK_TRIGGER` result. Coordinator
  accepted this departure; the original dispatch functions are unchanged.
- `WriteScreenshot` returns an error value, with nil/false meaning success,
  rather than true meaning success. It is called from a real-time thread.
  A native success is logged as `capture="native accepted"`; it is not a
  claim that an agent opened a file or witnessed pixels.

## Numbered claims

1. **Slot contract built.** `74_SMRTK_Agent.lua` extends `Bind` locally;
   slots retain `slot_1` through `slot_6`, and `BindScratch` supplies
   `slot_scratch`. Once functions execute on Run; armed functions execute on
   Arm, then their `on_click` on Fire. With no `on_click`, the function also
   handles explicit Fire. New contexts retain all core fields and add
   `sel`, `pin`, `cursor`, `mark`, `log`. Binding an armed action refuses.
   Old `opts.arm/disarm` calls delegate to the original Bind and keep their
   original context. `80_AgentSlots.lua` is entirely commented, with example
   bindings for every numbered slot and scratch; loading it does nothing.
   **Falsifier:** the standalone command below checks original dispatcher
   identity, context values, scratch, legacy caller and refused rebind.

2. **Agent UI built inside the supplied page host.** Seven slot buttons show
   labels, callback-attempt counts and armed text/colour. Pin buttons show
   `Class(handle)` and register the cross-page ids `pin_A`, `pin_B`, `pin_C`.
   Note Enter emits one NOTE result and clears only after success; other
   editor shortcuts delegate to native `XTextEditor.OnShortcut`. Screenshot
   + Mark emits one MARK result, including `mark`, `capture_id`, `path`,
   `capture`, and any fallback reason. Trigger rows refresh from the live
   registry without rebuilding or defocusing the note editor. There is no
   added dialog, fullscreen window or shared surface.
   **Falsifier:** actual Agent builder creates all slot controls and handles
   Enter, failed/empty notes, native shortcut delegation, late trigger
   registration, and delayed screenshot-button dispatch under fake X classes.
   This does not prove rendering, scrolling, focus or screen fit in play.

3. **Click targeting uses only the spike service.** Arm first reserves core
   state; `AcquireClick(id, callback(pos,obj))` then acquires the exclusive
   listener. Acquisition failure never runs slot setup or steals the prior
   consumer. Fire occurs inside a real-time thread, after checking that its
   captured arm is still current. Pending clicks coalesce; stale clicks after
   save/disarm cannot mutate a later arm. Disarm always calls ReleaseClick
   before user cleanup. Failed clicks disarm; `once_click=true` disarms after
   the first successful click. Right click is the core's disarm route.
   **Falsifier:** contention, actual delayed mutation, exactly one FIRE,
   stale click across re-arm, partial-arm cleanup and failed-click cleanup.

4. **Triggers and shared field watch built.** `Trigger` registers disarmed,
   `T.triggers[id]` exposes the definition, and core `T.armed/T.fires` are
   authoritative. Cadence defaults to 1000 game milliseconds. A game-time
   thread polls the read-only predicate; a guarded real-time thread enters
   Run to execute effects, preserving native screenshot threading and
   post-mutation checks. Predicates fail visibly and disarm; effects cannot
   complete a stale arm's pause/mark after save/load. Non-once level
   conditions fire on rising edges. Field and rocket conditions represent
   events and can fire on adjacent polls.
   Built-ins are target sol (`UIColony.day`), first error since the mark
   captured at arm, selected scalar field change, and next rocket landing
   (including the asteroid landing message).
   **Falsifier:** false/true controls, repeat edges, one-shot cleanup,
   registry ownership, thrown predicates, nil/false/zero watch values,
   adjacent changes, table refusal, deleted target, error baseline, rocket
   event, screenshot trigger, queued cancellation and mid-capture lifecycle.

5. **Lifecycle stays in the core.** Every armed slot/trigger is in `T.armed`;
   the existing SaveGameStart, SavegameSaved, PreLoadGame, LoadGame,
   ChangeMap, CurrentMapChange and DoneGame dispatches therefore disarm it.
   Trigger cleanup deletes a separate polling thread but never deletes the
   thread currently delivering DISARM, which would suppress its result.
   Load/map change clears session pins. Nothing is serialized or auto-rearmed.
   **Falsifier:** every listed lifecycle message cancels polling and click
   capture; no delayed mutation or trigger appears after the lifecycle event.
   Frozen taint alarms and non-unwinding engine-error detection still fire.

## Source routes opened

Installed source build 24995074: `python tools/doccheck.py --emit-fingerprint`
emitted the 1.1.0 group HOLDS and doccheck GREEN. These paths are relative to
`A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src`.

| route | opened evidence |
|---|---|
| exclusive click listener | `CommonLua/Core/terminal.lua:11-30,210-225`, `CommonLua/X/XDesktop.lua:320`, `Lua/UI/SelectionModeDialog.lua:43-51`; agrees with the spike |
| editor focus and Enter override | `CommonLua/X/XTextEditor.lua:513` native shortcut handler, `:838` focus setup, `:1508-1525` mouse down calls SetFocus; required X classes are outside the mod blacklist |
| screenshot | `CommonLua/gamelib.lua:330-342` collision-avoiding GenerateScreenshotFilename, `:494-511` WriteScreenshot and error-valued caller; `CommonLua/Classes/XDef/CommonShortcuts.generated.lua:37,50` real-time calls using AppData |
| pause and sound effects | `CommonLua/Features/GameSpeed.lua:49-91` SetGameSpeed, `Lua/MarsStoryBits.lua:89` PlayFX notification sound |
| sol | `Lua/Colony.lua:203-208` NewDay updates UIColony.day |
| landed rocket | `Lua/UniversalRocket.lua:429`, `Lua/Buildings/RocketBase.lua:370`, `Lua/Buildings/LanderRocket.lua:1065` emitted messages |

Additional negative blacklist search for CurrentThread, IsValidThread,
DeleteThread, GenerateScreenshotFilename, WriteScreenshot, XTextEditor and
CreateGameTimeThread returned no matching blacklist assignments. No
metatable introspection, string compilation, account or cheat-enable writes
were introduced. The screenshot destination directory was prepared with
`New-Item -ItemType Directory -Path C:/Dev/SMR-ScreenCaptures -Force`, which
emitted `C:\Dev\SMR-ScreenCaptures`; no screenshot was taken.

## Gates — emitted output

Before Code edits, separate command:

```text
$ tasklist /FI "IMAGENAME eq Mars.exe"
INFO: No tasks are running which match the specified criteria.
```

```text
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
HEAD pack=e245d8028e9d648f02453b5b4230b52155439bd9
HEAD testkit=05c7e45552006d2dcc28a4a49c446f288d74d356
```

Rule-6 and rule-7 direct `rg -n` searches on the two owned Lua files also
returned no matches. `python tools/parsecheck.py --dir
C:/Dev/SMR-BugFixPack-TestKit/Code --quiet` emitted:

```text
PARSE: 30 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]
```

Subsequent doccheck saw a peer's newly created file and emitted:

```text
PARSE: 31 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
doccheck: GREEN
```

The frozen core, panel and metadata had no working-tree diff at that gate.
Metadata is intentionally coordinator-owned; requested exact code-list lines,
after their numerical predecessors and before `90_Loggers.lua`:

```lua
"Code/74_SMRTK_Agent.lua",
"Code/80_AgentSlots.lua",
```

## Stopped / OWNER-ROUTED

No source stop condition fired. P3 stops at its assigned build fence: files,
desk falsifier, this report; no commits, removals, metadata edits or play
claims. Screenshot pixels, native timing/focus and visual overflow await 08.

**OWNER-ROUTED recommendations for 03B's single consolidation:** retain
scalar-only watches with an explicit refusal for tables, functions, threads
and userdata; add a structured snapshot watch only if a sitting needs one.
The core counts both Lua and thread error notifications, so the built-in
"First Lua error since mark" means first error notification since that mark,
not a count of unique exceptions. Game-time polls stop during pause and cannot
see changes which occur and reverse between polls. These are product limits
to document, not a new owner permission request. The screenshot file is the
08 witness, even after a native accepted result. Eligibility remains the
upstream unavailable read; no P3 claim expands it.

## for-07 — slot contract and button list

The exact reusable slot template is `C:/Dev/SMR-BugFixPack-TestKit/Code/80_AgentSlots.lua`.
Copy its contents verbatim into the standing slot guidance; do not turn its
commented examples into automatically running/arming defaults. Its executable
contract example, with the same helper semantics and callback-return rule:

```lua
SMRTK.Bind(1, "Read selected", function(ctx)
  if not IsValid(ctx.sel) then return false, "select an object" end
  return { object = ctx.sel }
end, { mode = "once" })

SMRTK.Bind(4, "Read map click", function(ctx)
  ctx.state.clicks = 0
  return { ready = true }
end, { mode = "armed",
  on_click = function(ctx, pos, obj)
    ctx.state.clicks = ctx.state.clicks + 1
    return { cursor = tostring(pos), object = IsValid(obj) and obj or "none",
      clicks = ctx.state.clicks }
  end,
  on_disarm = function(ctx) return { clicks = ctx.state.clicks or 0 } end,
  once_click = false,
})
```

`ctx` retains `action/phase/selected/state/reason`; `sel` is SelectedObj at
dispatch, `pin` is the shared A/B/C object-reference table, `cursor` is the
current terrain cursor or captured click position, `mark=SMRTK.Mark`,
`log=SMRTK.Log`. Validate references with IsValid. Callbacks return their
fields; `ctx.log` is auxiliary evidence only, never a duplicate result.
`ctx.mark` creates a distinct MARK action. Never detach mutation threads
inside callbacks: the outer assertion would then cover the wrong work.
Legacy opts.arm/disarm remains available, with the original core context.

```lua
SMRTK.Trigger { id = "slot_breakpoint", label = "Sol 20", cadence = 1000,
  when = function() return UIColony and UIColony.day >= 20 end,
  ["do"] = { mark = true, pause = true, screenshot = false, sound = true },
  once = true }
SMRTK.Arm("slot_breakpoint")

SMRTK.TriggerField("watch_example", SelectedObj, "command", {
  once = false, ["do"] = { mark = true, pause = true, sound = true } })
SMRTK.Arm("watch_example")
```

`when` must be read-only, non-yielding and without logging or side effects.
`TriggerField(id, object, field, opts)` returns a disarmed registered definition
or false/reason. Its target is fixed at arm, so subsequent selection changes
do not retarget a watch. The baseline accepts nil/string/number/boolean only;
fires log object/field/before/after with nil spelled explicitly. P4 may register
`watch_selected_field` while retaining its separate command id `watch_field`.
Registered definitions are `T.triggers[id]`; counts/state are `T.fires[id]` and
`T.armed[id]`. Resolve these at invocation, not initial file load.

| Agent control | registry / dispatch |
|---|---|
| Slot 1 through Slot 6 | slot_1 through slot_6; Run for once, Arm/Disarm for armed |
| Scratch | slot_scratch, registered with BindScratch |
| Pin A / Pin B / Pin C | pin_A / pin_B / pin_C, current selection |
| note field Enter / Add note | note, text argument, clear after successful NOTE |
| Screenshot + Mark | screenshot_mark; real-time Run; one MARK with capture_id/path |
| Target sol field + Sol >= target trigger | trigger_sol, Arm with target sol |
| Selected field + Selected field changed | trigger_field, Arm with object and field |
| First Lua error since mark | trigger_error, Arm captures current mark/error baseline |
| Next rocket landed | trigger_rocket, Arm captures event baseline |
| additional registered trigger rows | registry id; Arm/Disarm, live refresh |

Pins and screenshot_mark advertise complete menu commands; screenshot_mark
requires a real-time dispatch from the dock too. Console screenshot usage:
`*r SMRTK.Run("screenshot_mark")`. The screenshot basename and MARK record share
`capture_id`; `mark` remains the core's absolute ring index. The normal mark
effect produces its own MARK record and a trigger produces its own TRIGGER
record; this is not two primary results for one action.

08 predictions to incorporate: each arm gets ARM, each map callback one FIRE,
each trigger effect one TRIGGER, each lifecycle one DISARM per active id;
all with status=OK and subsequent taint check. A screenshot success additionally
has one MARK with native accepted/capture_id/path and a file the owner opens.
Do not infer timing or screenshot success from the desk model. Cadence = one
game second; use the chain's 3× abort convention for attended polling, with
wall-time budgeting adjusted to current simulation speed and paused state.

## DRIFT

- A shortened upstream report name was absent; the actual required file is
  `SMRTK_SKELETON_PREDICTIONS.md`, which was opened, including its actual API.
- The sitting report's pre-flight header still says no game leg; its final
  VERDICT/outbox supersedes that old header and agrees with owner authority.
- Two source searches initially used a nonexistent GameSpeed.lua location
  or shell-quoted pattern. Rerun searches located the actual files; neither
  failed query was counted as negative evidence.
- The first implementation put trigger screenshot effects on the polling
  thread. The falsifier rejected its game-time context; effects now enter
  Run in a real-time thread, with cancellation checks after yielding capture.
- The brief's `do` keyword syntax and frozen FIRE/TRIGGER distinction are
  recorded above rather than silently copied into the slot guide.
- Shared pack HEAD advanced during the payload, including C94/STATE work;
  EF-099, generated fact index, other prompts and peer payload files were
  already dirty and were preserved. No shared write was attributed by author.
- A peer relay initially described getmetatable as blocked. Coordinator and
  P5 corrected that claim after reading Mod.lua:1579-1582,1617-1619: mod
  environments receive safe_getmetatable/safe_rawget. P3 did not depend on
  the erroneous claim; scalar-only watches avoid alias comparison issues.
- A report-template insertion first used a non-ASCII anchor through a
  PowerShell pipe and made no insertion. The follow-up used an ASCII anchor
  and asserted that the complete source template appears verbatim.

## DEPARTURES

- Added BindScratch rather than extending numbered Bind to 7: preserves the
  six-slot API while making the requested scratch button usable.
- Kept backward-compatible legacy arm/disarm options alongside new mode
  bindings; mixed option families refuse rather than guessing semantics.
- Registered TRIGGER Run plus game-time polling and guarded real-time effects
  replaces Fire for trigger results; preserves one logger, one primary
  result and the actual-mutation taint/error checks without core changes.
- Screenshot+Mark is one MARK action. Engine GenerateScreenshotFilename
  allocates a collision-safe capture_id, separate from the ring index, and
  uses the preferred capture directory with AppData fallback. This avoids
  overwriting a previous session's same-numbered ring mark.
- Field watches explicitly support scalars only; silent alias comparisons
  would violate the observer's usefulness. They patch no methods.
- Repeating level predicates use edges; repeated field/landing events fire
  per observed event. This prevents a permanently true condition from
  producing one pause/sound/screenshot per poll.

## SUGGESTIONS

- 03B should check native game-time to real-time handoff, including a save
  during a yielded screenshot. The desk model proves guard ordering only.
- Use capture_id/path as screenshot evidence; keep the core ring mark an
  index so CopySince remains compatible. No runtime filesystem read is needed.
- A future event subscription can provide exact field transitions only when
  the target already emits them; polling intentionally does not promise that.
- The coordinator's planned scrollbar/tab-width repair should be measured
  with Agent's dynamic trigger rows and a focused note editor visible.

## for-07: verbatim sitting template

```lua
-- Sitting-owned TEMPLATE. An agent replaces this file before the next sitting.
-- Nothing below binds or arms an action until its example is uncommented.
-- Use real Lua functions here, or the same Bind call once in the console.
-- Six numbered slots; BindScratch is the seventh, disposable slot.
--
-- ctx = core context (action, phase, selected, state, reason), plus:
--   sel    SelectedObj at this dispatch (validate with IsValid before use)
--   pin    SMRTK.pins: A/B/C object refs; validate each before use
--   cursor GetTerrainCursor(), or the captured map-click position on Fire
--   mark   SMRTK.Mark(label): a distinct MARK evidence action
--   log    SMRTK.Log(verb, fields): AUXILIARY evidence only, never the result
-- Return a fields table, nil for success, or false, "reason" for refusal.
-- The dispatcher owns the single primary result and post-action taint check.
-- state survives Arm -> Fire(s) -> Disarm; bindings/pins are not serialized.
-- UI invokes Run/Arm/Fire inside the thread that executes your function.
-- Do not spawn detached mutation threads inside callbacks; their work would
-- escape the dispatch's taint/error assertion. Use ctx.state for cleanup.
--
-- SMRTK.Bind(1, "Read selected", function(ctx)
--   if not IsValid(ctx.sel) then return false, "select an object" end
--   return { object = ctx.sel }
-- end, { mode = "once" })
--
-- SMRTK.Bind(2, "Read pin A", function(ctx)
--   if not IsValid(ctx.pin.A) then return false, "pin A first" end
--   return { object = ctx.pin.A }
-- end, { mode = "once" })
--
-- SMRTK.Bind(3, "Read cursor", function(ctx)
--   return { cursor = tostring(ctx.cursor) }
-- end, { mode = "once" })
--
-- SMRTK.Bind(4, "Read map click", function(ctx)
--   ctx.state.clicks = 0 -- fn runs on ARM; acquisition already succeeded
--   return { ready = true }
-- end, { mode = "armed",
--   on_click = function(ctx, pos, obj)
--     ctx.state.clicks = ctx.state.clicks + 1
--     return { cursor = tostring(pos), object = IsValid(obj) and obj or "none",
--       clicks = ctx.state.clicks }
--   end,
--   on_disarm = function(ctx) return { clicks = ctx.state.clicks or 0 } end,
--   once_click = false, -- true disarms after the first successful click
-- })
--
-- SMRTK.Bind(5, "Read mark", function(ctx)
--   return { mark = SMRTK.mark_index, errors = SMRTK.error_count - SMRTK.mark_errors }
-- end, { mode = "once" })
--
-- SMRTK.Bind(6, "Read sol", function(ctx)
--   if not UIColony then return false, "load a colony" end
--   return { sol = UIColony.day }
-- end, { mode = "once" })
--
-- SMRTK.BindScratch("Scratch read", function(ctx)
--   return { cursor = tostring(ctx.cursor) }
-- end, { mode = "once" })
--
-- API: Run("slot_1"), Arm("slot_4"), Fire("slot_4", pos, obj),
-- Disarm("slot_4", "manual"). Rebinding an armed slot refuses: disarm first.
-- Armed slots without on_click can be fired explicitly; fn runs on ARM and FIRE.
-- Click capture is exclusive across the toolkit. Right-click cancels it.
-- Save/load/map change disarms every slot/trigger; load/map change clears pins.
-- Legacy opts.arm/disarm calls keep the skeleton's original context/API.
--
-- Trigger example (registers disarmed; Arm explicitly before the sitting):
-- when is a read-only predicate. It must not mutate, log, yield or arm work.
-- SMRTK.Trigger { id = "slot_breakpoint", label = "Sol 20", cadence = 1000,
--   when = function() return UIColony and UIColony.day >= 20 end,
--   ["do"] = { mark = true, pause = true, screenshot = false, sound = true },
--   once = true }
-- SMRTK.Arm("slot_breakpoint")
-- The literal field name do MUST be ["do"] in Lua (do is a keyword).
-- Repeating conditions fire on false -> true; a scalar field watch fires on
-- each observed change. A 1 s game-time poll cannot see intermediate changes.
-- SMRTK.TriggerField("watch_example", SelectedObj, "command", {
--   once = false, ["do"] = { mark = true, pause = true, sound = true } })
-- SMRTK.Arm("watch_example")
```

## Doccheck warnings — verbatim from the final P3 gate

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
TESTKIT TREE: 5 uncommitted change(s) — report-only, never a block. Route or commit them; never `git restore` (the 2026-08-03 orphan lesson).
  WARN ?? Code/73_SMRTK_Infopanel.lua
  WARN ?? Code/74_SMRTK_Agent.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
```
