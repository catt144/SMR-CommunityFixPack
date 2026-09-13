# smrtk 03 — the World page

Link 03 of `smrtk`. README rules 1–20 are yours. Runs only after 02 PASSed (read 02's outbox first — it says which
console tap carries lines and what the hotkey is). Independent of 03b/04/05/06.

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
   resume, and **run-until** (sol N, or a trigger id from 04's registry — stub the trigger form until 04 lands):
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
   `Colonist:AddTrait(id)`; remove trait likewise. Lives on World for now; 03b may mirror it in the infopanel.

## Scope fence

IN: `72_SMRTK_World.lua` + its `metadata.lua` line. OUT: per-object actions (03b), slots/triggers (04), saves/kit (05).
A cheat you find that the list lacks: add it if it is a plain leaf call; otherwise note it in 07's inbox.

## Stop conditions

A disaster leaf needs a `NetSyncEvent` to fire at all · quiet mode needs a wrap the toggle cannot cleanly uninstall
· `SetGameSpeed` refuses values above the list on this build. Report; do not force.

## What may NOT be claimed

That a disaster button fires correctly in play (08 reads it). That quiet mode suppresses (08 provokes it).

## Close-out

Rules 15–16. Commit per unit (disasters · quiet · speed · fix/malfunction · waits · re-exposures · traits).
Outbox to 07 (the final button list for the docs) and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (02 appends here)
