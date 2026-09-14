# smrtk payload P1 — the World page

Payload P1 of link 03A (`smrtk`). README rules 1–22 are yours, **21 especially: you write, you never commit.** Your
inbox carries 02's outbox (which console tap carries lines, the hotkey) and 03A's spike decisions. Independent of P2–P5.

## Job — `Code/72_SMRTK_World.lua`, every action through `SMRTK.Action`, every one logged and taint-asserted

1. **Disasters, cursor-targeted, leaf calls only** (`EF-098`): Dust Storm (normal / electrostatic / great, intensity
   from `PresetsCombo("MapSettings", "DustStorm")`), Dust Devil (minor / major), Cold Wave, Meteor (single / multi /
   storm) at `GetTerrainCursor()`, Marsquake, Rains, Underground cave-in at cursor, Underground marsquake. Read each
   `Cheat*` leaf's signature in `Lua/Cheats.lua` before calling it. **Stop disaster** → `CheatStopDisaster()`.
   Meteor buttons are **armed** actions: arm, click the map, it lands there; disarm on second click / save / load.
2. **Quiet mode** (toggle, rule 9): suppress scheduled disasters while armed. Find the scheduler (`Lua/Disasters/*` —
   the per-disaster `WaitDisaster`/spawn threads) and gate at the narrowest point that stops *new* disasters without
   killing a running one; log `SMRTK_QUIET on/off`. If no clean point exists, ship "stop + re-arm" and say so.
3. **Speed:** normal / fast / ultra (`SetGameSpeed(n)` above the UI max; read `const.MaxSaneTimeFactor`), pause /
   resume, and **run-until** (sol N, or a trigger id from P3's registry — stub the trigger form; P3 lands beside you):
   ultra + auto-pause + `PlayFX` cue. Surface `GameSpeedLimit` when it clamps (`CommonLua/Features/GameSpeed.lua:49-80`)
   as `SMRTK_SPEED clamped_by=<reason>` rather than silently no-op.
4. **Fix all / Malfunction all** — `AllMapsForEach` over `Building`: `CheatCleanAndFix` / `SetMalfunction`, counts logged.
5. **Finish what I'm waiting on:** `CheatCompleteAllConstructions()`, complete wires/pipes, and "land the in-flight
   rocket" (read `RocketBase`'s travel state and the instant-travel debug toggle `dbg_ToggleRocketInstantTravel`,
   `CheatDef.lua:424-431` — prefer a one-shot over leaving a toggle on).
6. **Re-exposures with no taint:** spawn colonists (1/10/100, incl. Martian-born), applicants, funding ±, tech points,
   research all / unlock all buildings, `FillAllStorages`, open/close all domes, unpin all — each by calling the
   preset's leaf as `EF-098` lists them; **never `def:run()`** for the 13.
7. **Add trait** — a submenu over `TraitPresets` (grouped by category) applied to the selected colonist via
   `Colonist:AddTrait(id)`; remove trait likewise. Lives on World for now; P2 may mirror it in the infopanel.

## Scope fence

IN: `72_SMRTK_World.lua` + its `metadata.lua` line. OUT: per-object actions (P2), slots/triggers (P3), saves/kit (P4).
A cheat you find that the list lacks: add it if it is a plain leaf call; otherwise note it in your report's for-07 section.

## Stop conditions

A disaster leaf needs a `NetSyncEvent` to fire at all · quiet mode needs a wrap the toggle cannot cleanly uninstall
· `SetGameSpeed` refuses values above the list on this build. Report; do not force.

## What may NOT be claimed

That a disaster button fires correctly in play (08 reads it). That quiet mode suppresses (08 provokes it).

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. `python tools/parsecheck.py` on your file; rule 6's and rule 7's greps on it, counts
quoted. Return a **numbered-claims report** to 03A: per unit (disasters · quiet · speed · fix/malfunction · waits ·
re-exposures · traits) — built (function names), verified how (the exact command + its output), stopped, OWNER-ROUTED
(with a recommendation), for-07 (the final button list), DRIFT. Every claim falsifiable by one command. Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox and the spike decisions here before launch)


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
