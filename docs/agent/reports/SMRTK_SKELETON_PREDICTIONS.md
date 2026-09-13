# SMRTK 01 — skeleton predictions and build record

Written before code, 2026-09-13, Codex (GPT-6). No game leg has run.
Pack starting HEAD `d4ece6c`; TestKit starting HEAD `dbc68f8`; installed game
build `24995074` (fingerprint command: `python tools/doccheck.py --emit-fingerprint`).
All game behavior below is a **prediction**, never a PASS.

## Disagreements first / job 0

1. **Eligibility is blocked.** `CommonLua/Modding/Mod.lua:1403` lists
   `CanUnlockAchievement = true`; `UnableToUnlockAchievementReasons` is also a
   blacklisted message. `GetAchievementFlags` reads unlocked/secret flags, not
   eligibility (`CommonLua/Classes/Achievement.lua:39-41`). The skeleton must
   return `UNAVAILABLE:sandbox`, never infer `OK` from a clean taint read.
   The invariant remains; 02 cannot claim full achievement eligibility from
   this instrument. No progress/unlock calls are a substitute for a read.
2. **The existing console is a confounder.** `00_TestCore.lua:513-637` already
   enables, rebuilds and auto-opens the console. 02 must distinguish an
   ordinary load check from an isolated shortcut-creation check; closing its
   auto-opened console and pressing Enter alone does not identify our hook.
3. **The default hotkey collides beyond the two requested files.**
   `Ctrl-Shift-K` is absent from GameShortcuts/CommonShortcuts but belongs to
   Toggle Collisions in `DevToolsShortcuts.generated.lua:1972`.
   `Ctrl-Shift-F11` has no match across the shipped source or existing TestKit.
4. **01 has no Fill button.** Keep the pages empty. 02 registers a console-only
   `skeleton_fill` action against the core, then calls the selected depot's
   `CheatFill` leaf through `SMRTK.Run`. This avoids consuming P2 early.
5. **A fixture must start clean.** An arbitrary 1.1.0 playtest save is
   insufficient (WORKFLOW's ordinary fixtures intentionally use cheats).
   Preserve a clean baseline and discard the tainted control; never clear
   `CheatsUsed` to manufacture a GREEN.

The build/judge ordering and payload cut hold. 02's measurement script and
the achievement-reading promises in unconsumed links are corrected; no page
build moves ahead of 02.

## Live todo — commit and verify units

- [x] Core, including the required formatting smoke and behavior falsifiers (`774b55a`).
- [x] Floating panel and shortcut registration (`b400683`).
- [x] TestKit metadata code list only (`5d8d3b3`).
- [x] Predictions, source corrections, ck175, successor/audit inboxes and consumed 01 (this documentation commit; pack push verified in the closing response).

## Echo contract

The LOG FILE is the reading; the first-screen witness only identifies the step.
Each logger record is `[SMRTK] SMRTK_<VERB> <sorted k=v fields> t=<game time> id=<sequence>`.
Fields containing spaces are quoted; embedded newlines are escaped. `t` and
`id` are measured values, not literals to paste. An action has one result
record; a taint or error alarm is an additional, explicitly named record.
Native console capture is measured separately from the toolkit's own ring
insertion: finding toolkit lines alone cannot PASS the native tap.

## Predictions for 02 (numbering is the sitting script's)

| Step | Expected LOG/read; first-screen witness | Normal / abort at 3× |
|---|---|---|
| 0a baseline | `SMRTK_TAINT_READ action=taint_read status=OK used=false`; CLEAN strip; `SMRTK_ELIGIBILITY action=eligibility reason=UNAVAILABLE:sandbox status=OK` | 5 s / 15 s |
| 0b control | After one vanilla Fill in a scratch branch, `SMRTK_TAINT_READ action=taint_read status=OK used=true` and `SMRTK_TAINT action=taint_read before=true used=true`; TAINTED strip | 5 s / 15 s |
| 1 fresh load | `SMRTK_CONSOLE_ARM enabled=true hook=PreLoadGame` before load completion; Enter reopens the console with Mod Manager never opened this boot; Ctrl-Shift-F11 toggles panel | 10 s after loading screen / 30 s |
| 2 isolated console control | With retail cheat/devtools gates false, `SMRTK_CONSOLE_CONTROL action=console_control discriminates=true negative=false positive=true status=OK`; Enter opens on positive leg. If another native gate is true, `negative=true discriminates=false` is explicitly non-discriminating; record `PLATFORM_READ`, never claim our hook was necessary | 5 s / 15 s |
| 3 leaf | `SMRTK_ACTION action=skeleton_fill after=<amount> before=<amount> object=<Class(handle)> status=OK`, with after > before; selected depot visibly fills; next `SMRTK_TAINT_READ ... used=false`, CLEAN strip | 5 s / 15 s |
| 4 native tap | `SMRTK_TAP_READ action=tap_read native_console=1 native_print=1 status=OK`; clipboard includes output witnesses with `source=console`, and toolkit records with `source=toolkit`. Reject input-command echoes; if native chunks are decorated, retain actual chunks and mark this exact prediction false before scoring the corrected read | 5 s / 15 s |
| 5 fallback | Arm print tee: `SMRTK_ARM action=print_tee status=OK`; one print yields `SMRTK_FIRE action=print_tee ... text=SMRTK_TEE_WITNESS_100%`; clipboard contains `source=print`; disarm restores captured function identity | 5 s / 15 s |
| 6 frame | Each tab changes within the same footprint; collapse retains strip/top controls; drag persists; Clear calls `cls`; Flush logs `SMRTK_FLUSH action=flush status=OK`; Pause and Stop log `status=NOT_BUILT` by registry id | 5 s each / 15 s each |
| 7 error witness | Explicit `SMRTK.OnLuaError` desk-style injection logs `SMRTK_ERROR kind=lua ... stack=SMRTK_STACK_WITNESS`; errors since mark increases, Copy retains stack. This proves the handler, not native delivery | 5 s / 15 s |
| 8 save/load | Armed tee logs `SMRTK_DISARM action=print_tee reason=SavegameSaved status=OK`; after save/load panel is open at persisted position, Kit tab, expanded, armed=0; `used=false` | 30 s per save/load / 90 s; report at 30 s, never wait silently |

Stop immediately on new taint on the clean branch, loss of the baseline,
an unexpected game error, or an action refusal. Do not retry a mutation on
the same fixture to obtain a preferred reading. A missing tap chooses the
declared fallback; missing both paths kills that premise. Timed-out UI work
returns to 01 with the archived log. The eligibility field remains unavailable
even on a fully successful skeleton sitting.

## DEPARTURES

- Eligibility is an explicit unavailable read when sandboxed; no fake OK and
  no alternate achievement mutation. Checked against no-taint and sandbox rails.
- Ctrl-Shift-F11 replaces Ctrl-Shift-K after the wider collision search.
- The console diagnostic is an **explicit, synchronous** negative/positive
  rebuild, to keep old TestKit auto-open behavior from passing our test.
- The sitting registers its own Fill action; payload pages remain empty.
- Native tap counters and `source` metadata distinguish automatic toolkit
  ring insertion from console delivery. A ring full of our own lines proves
  neither native delivery nor a working print tee.
- Scope extends to the reusable desk smoke, the omitted sandbox boundary in
  EF-096 and generated index, corrected unconsumed prompts, and STATE/the prompt map's next
  pointer. These route findings and keep the consumed 01 from remaining NEXT;
  they add no shipped code or page content.

## SUGGESTIONS

- 03B should decide when to retire the old TestKit console bootstrap, after
  02 supplies evidence. Do not silently patch it in 01.
- P3/P4 should prefer one registered action API for every mutation and treat
  unavailable readings as unavailable, including achievement eligibility.
- 08 should budget a genuinely clean colony separately from normal test saves.

## Desk evidence / actual API

1. `python docs/agent/reports/SMRTK_SKELETON_SMOKE.py` runs lupa on the actual
   files with fake game services. It checks logging through a second printf,
   one-line escaping, flush, a bounded ring, overflow disclosure, clipboard,
   native delivery present **and absent**, print return preservation and
   restoration after every lifecycle message, missing selection, synthetic
   taint RED, thrown and non-unwinding errors, partial-arm cleanup, slot
   dispatch, persistence, shortcut negative/positive, panel callbacks and
   reconstruction after load. Fake X classes do not prove rendering.
2. `python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet`
   emits `PARSE: 27 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]`.
   TestKit metadata was separately passed through `tools.parsecheck.runtime`;
   the only metadata diff is the two new code-list lines.
3. `rg -n 'NetSyncEvent|LogCheatUsed'` on both SMRTK files: **0 lines**;
   presence side on shipped `Data/CheatDef.lua`: **26 lines**. `80_AgentSlots.lua`
   does not exist yet. `rg -n '^\s*print\('` on both files: **0 lines**.
   These gates and doccheck GREEN ran before each TestKit commit.
4. `python tools/doccheck.py`: GREEN. Its complete final warning block is
   recorded below. No pack runtime file or version field changed. TestKit
   has no remote; the pack report is the only pushed artifact.
5. Source routes opened on build 24995074: `StorageDepot.lua:196-210` (single
   resource Fill); `XShortcuts.lua:7-25,37-79` (DataLoaded wait, spawn before
   Shortcuts); `Dlc.lua:641-664` (DataLoading precedes DataLoaded);
   `Savegame.lua:800-811` (PreLoadGame before unpersist/load); `map.lua:570-578`
   (PreNewMap before NewMap); `XDialog.lua:238-300` (construct/Open without
   a template); `XWindow.lua:562-612,623-664,858-905` (box/margin/layout);
   `XButton.lua` (label must be a child); `uiConsoleLog.lua:116-137`;
   `cthreads.lua:138-142` (thread, error signature); `GlobalStorageTables.lua:337-351`
   (yielding local-storage writer); `Mod.lua:109-132,1403,1560-1618` (logger,
   blacklist, globals). No required X class is blacklisted.

### API frozen for 03A, subject to 02's corrections

| API | Contract |
|---|---|
| `Action{ id, label, page, run, arm, disarm, needs, verb }` | Register at mod load. `run` required; `arm/disarm` paired. Returns definition or false/reason; refuses replacing an armed action. No UI automatically created |
| `Run(id, ...)` | Dispatch synchronously. Callback receives `(ctx, ...)`, with `ctx.action`, `phase`, `selected`, `state`, `reason`. Return fields table, nil for success, or false/reason for refusal. One primary log result, then taint assertion. Returns boolean + result fields |
| `Arm(id, ...)`, `Disarm(id, reason)`, `Fire(id, ...)` | Toggle state is `ctx.state`. `arm` installs, `disarm` restores; paired cleanup runs after partial arm failure. Fire uses `run` only while armed. Log ARM/DISARM/FIRE. Future delayed work must enter Run/Fire **inside** its thread so assertions cover the actual work |
| `Bind(n, label, fn, opts)` | Slots 1..6 map to `slot_1`..`slot_6`; opts carries `arm/disarm/needs`. Bindings are session code, never serialized |
| `Page(id, label, build)` | Register at mod load; optional `build(parent)` populates a fresh host when selected. Current pages Sitting/Agent/World/Saves/Kit. Build must not mutate game state |
| `Button(parent, label, action_id, props)` | XButton plus XText label; dispatches Run, refreshes strip. P3's arm UI should register a command action or implement a callback which calls Arm/Disarm, preserving the logger |
| `Mark(label)` / `CopySince(index_or_label)` | Mark returns the absolute ring index. Numeric Copy argument is an absolute index; nil or the **current** label uses the current mark. Unknown/older labels refuse. Evicted data reports `truncated=true`. Copy's own result is logged after the copied range |
| `TaintRead()` / `Eligibility()` | TaintRead logs through its action. Eligibility is a side-effect-free read returning `UNAVAILABLE:sandbox` here; `Run("eligibility")` logs it |
| `PrintTee(on)` | Toggle, default off; captures and restores the original global. Native tap remains a message listener. Each fire is logged; no idle function patch |
| `PanelState()` / `SavePanelState(fields)` | LocalStorage.SMRTKPanel only: open/tab/collapsed/x/y. Logical UI coordinates. Save requests coalesce onto a real-time thread; failures are logged |
| `T.ring`, `tap`, `fires`, `armed` | Ring rows `{n,t,mark,source,text}`; capacity 300. `source` distinguishes toolkit, console, print. Error counter counts notifications, not distinct exceptions (one engine failure may send both events). Fire counters count callback attempts, including failures |

P1's reserved ids are `pause`, `stop_disaster`, `quiet` (quiet strip reads its
armed state). The first two intentionally return NOT_BUILT until P1 registers
them. No Fill, World or Kit payload button was added.

### DRIFT caught before the sitting

- The eligibility blacklist and wider shortcut collision above contradicted
  the original plan; its unconsumed measurement promises are corrected.
- The first smoke assertion accidentally compared escaped output with a real
  newline; corrected the assertion to a Lua long string and reran it.
- Partial-arm cleanup now uses its own error-counter boundary; an earlier
  body would have retained a successfully restored toggle after an arm error.
- The first panel draft used Dock=ignore with measured heights. Source shows
  that route skips parent sizing; logical margins now let engine layout handle
  collapse and scaling. No game claim is inferred from the mock.
- A mistyped speculative commit id in the uncommitted live todo was removed
  immediately; only command-emitted commit ids above were retained.
- The first commit-message file carried PowerShell's UTF-8 BOM. The commit
  subject retains that harmless character; later messages use UTF-8 without BOM.
- Initial source searches hit PowerShell quoting/glob errors and were rerun
  successfully with explicit paths. No negative gate was taken from those errors.
- During work, peer commits `b9501dd`/`2037626` added model seating and regenerated
  WAITING. Their diffs were read and preserved. ListAgents exposed only this
  Codex thread; no external Claude-agent registry was available. TestKit has no
  remote, so no pull/push was attempted there.
- The fifth-ruling seating was added to the manifest while the old 03A/07
  headers still said Astra; those headers are aligned to the owner's manifest
  (Sol) in this close-out. No cross-vendor judge was reassigned.
- The first documentation staging command included the already `git rm`'d
  prompt; git add rejected that path. The deletion remained staged. The retry
  stages only existing paths and retains the deletion in the explicit commit.

### Doccheck warnings (verbatim final output)

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
STATE + STUBS: STATE.md 11442 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2498, 2572 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
PUSH SET: 44038 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
```

The earlier per-unit gates also reported these own pending files, all resolved
by the three TestKit commits before the final gate:

```text
  WARN ?? Code/70_SMRTK_Core.lua
  WARN ?? Code/71_SMRTK_Panel.lua
  WARN  M metadata.lua
```
