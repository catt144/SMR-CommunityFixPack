# smrtk payload P4 — the Saves page and the Kit page

Payload P4 of link 03A (`smrtk`). README rules 1–22 are yours, **21 especially: you write, you never commit.**
Independent of P1–P3/P5. Two files; if Job A fills your budget, finish it, report the split point, and stop — 03A
re-fires Job B as its own payload (rule 4).

## Job A — `Code/75_SMRTK_Saves.lua`

1. **Slots A/B/C.** Save → `SaveGame("SMRTK_<slot>", { silent = true })` in a real-time thread (it opens a loading
   screen and waits on render mode — `CommonLua/Savegame.lua:1069-1090`); Load → `LoadGame(name)` likewise. ⛔ Never
   from a game-time thread; never while `SavingGame`.
2. **The session-id guard.** `OnMsg.GatherGameMetadata(metadata)` adds `smrtk = { session = <id>, actions = n,
   last = {...} }`; LOAD refuses a slot whose `session` is not this process's id and says so on the strip (an
   override button exists and logs `SMRTK_LOAD_OVERRIDE`). Read the metadata back the way the load dialog does
   (`Savegame.Load`'s `LoadMetadataCallback` path) — never parse the file yourself.
3. **Provenance readout:** the loaded save's `smrtk` block, if any, on the page and via `SMRTK_PROVENANCE` on load.

## Job B — `Code/76_SMRTK_Kit.lua`

1. **RunAll / run one probe** — `SMRTest.RunAll()` and a dropdown over `SMRTest.order`; verdicts coloured on the page
   from `SMRTest.last`; the probe-hygiene sweep line shown before the run button enables (WORKFLOW's hard gate).
2. **Logger toggles** — every `SMRTest.Log.<name>` as a lit/unlit button (they already uninstall cleanly).
3. ⛔ **Force-open console may ONLY call `ShowConsole(true)` on 01's `ConsoleEnabled` arm — it must NEVER set
   `Platform.cheats` (rule 10), nor any other route that flips `AreCheatsEnabled()` process-wide.** Raised from the
   02 sitting: that global paste is the owner's current workaround and retiring it is much of the point of the
   toolkit; a button that re-introduces it defeats the tool and makes the console gate non-discriminating. If
   `ShowConsole(true)` does not open the console on 01's arm, that is a STOP condition and a finding — never a
   licence to widen the enable.
   **Log tail pane** — the ring buffer, errors highlighted, "errors since mark: N"; **Force-open console**
   (`ShowConsole(true)`); **cls**.
4. **Fingerprint** — one button and automatically on every MARK: game build (`LuaRevision`), pack `version` from the
   loaded `ModDef`, the live `fix pack present: N/N` read (`SMRFixPack.ListFixes()` — read how the pack exposes it in
   its `00_Core.lua`, do not re-derive counts), active mod ids, save name, sol. `SMRTK_FINGERPRINT` one line.
5. **Object dump** (`SMRTK_DUMP`) — class, handle, template, pos/hex, dome, workers/shifts, storage, modifiers,
   malfunction/destroyed/demolishing flags, `IsValid`; registered as the id P2's Dump button calls.
6. **World snapshot** (`SMRTK_SNAPSHOT`) — sol, funding, colonists by status, buildings by class, resources,
   active disasters, current speed; and **diff** between two snapshot ids (`SMRTK_DIFF`).
7. **Watch a field** — a trigger (P3's engine, by registry id; stub if absent at load) on `SelectedObj.<field>` change;
   armed toggle, logs each change.

## Scope fence

IN: the two files + `metadata.lua` lines. OUT: the panel frame, World actions, slots, the stamper.

## Stop conditions

`LoadGame` from a mod thread wedges the loading screen on the desk · metadata cannot be read back without file I/O ·
`SMRTest` internals you need are local (then add a tiny accessor to `00_TestCore.lua` and say so).

## What may NOT be claimed

That a save/load round trip works (08). That the fingerprint's `N/N` is right (it is a read, quote it as one).

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. Parse-check both files; rule 6's and rule 7's greps, counts quoted. Return a
**numbered-claims report** to 03A: per unit — built · verified how (command + output) · stopped · OWNER-ROUTED ·
for-07 · DRIFT. If you added an accessor to `00_TestCore.lua`, it is its own numbered claim with the diff. Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox here before launch)


### 03A frozen upstream inbox, 2026-09-13

(one paragraph, for every payload's inbox)

P1-P4 all PASS on build 24995074; the core, the logger, the taint assert, the
`ConsoleEnabled` arm, the ring, the clipboard and LocalStorage persistence are
all confirmed in play, so build on them. The native console tap **and** the print
tee both carry real output, so either is a valid capture route. Five things to
carry: **(a)** per-object code must target `UniversalStorageDepotBase` and
`#storable_resources`, never `StorageDepot.resource` — 01's leaf refused on every
depot in the game; **(b)** `AsyncCheat*` infopanel entries bypass `ObjCheat` and
never taint even in vanilla (`ClassHierarchy`, `ClipPlane`, `Gizmo`, `Inspect`,
`Properties`, `Screenshot`), so they need no re-implementation; **(c)** `CLEAR`
logs onto the screen it just wiped, and the fix is a per-action opt-in honoured
by `dispatch`, never moving `T.Log` before the callback, which would empty
`before`/`after` on every action; **(d)** `PANEL_RESTORE` logs once per
registration and there are **three** (`InGameInterfaceCreated`, `PostLoadGame`,
`CurrentMapChangeDone`) though only one panel results — log on actual
create/make-visible; **(e)** `CopySince` is destroyed by the operator's next
copy, so it must be the last command of a block, and the panel **button** form is
immune. The owner's surface ruling and ranked fallback ladder are in ck175.

Shared routes and API are in `docs/agent/reports/SMRTK_UI_HOOKS.md` ??1?3 (read all).
Infopanel: DialogOpen ? toolkit InfopanelSection under idContent; no vanilla patch.
Map targeting: SMRTK.AcquireClick(id, callback(pos,obj)) / ReleaseClick(id); exclusive TerminalTarget listener, armed only.
Dock: DialogOpen on HUDClass ? appended controls; native XPopupMenu action menus, advanced pages in fixed left-side panel.
Always-visible safety text lives on dock. Chrome display policy is in core; use screen=false for pure chrome actions.
Registry ids: P3 pin_A/pin_B/pin_C; P4 dump_selected/watch_field. Resolve at invocation, not initial file load.
Core/panel are frozen while payloads run; do not edit them. Report requested metadata lines; coordinator owns metadata writes.
Each payload owns only its assigned files, never commits/removes files, and writes its numbered-claims report to docs/agent/reports/SMRTK_PN_REPORT.md (replace N with your number).
