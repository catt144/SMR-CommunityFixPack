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
