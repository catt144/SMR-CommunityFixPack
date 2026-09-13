# smrtk 05 — the Saves page and the Kit page

Link 05 of `smrtk`. README rules 1–20 are yours. After 02 PASS; independent of 03/03b/04/06. Two files; self-split
into 05b at the file boundary if the first fills your budget (rule 4).

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
3. **Log tail pane** — the ring buffer, errors highlighted, "errors since mark: N"; **Force-open console**
   (`ShowConsole(true)`); **cls**.
4. **Fingerprint** — one button and automatically on every MARK: game build (`LuaRevision`), pack `version` from the
   loaded `ModDef`, the live `fix pack present: N/N` read (`SMRFixPack.ListFixes()` — read how the pack exposes it in
   its `00_Core.lua`, do not re-derive counts), active mod ids, save name, sol. `SMRTK_FINGERPRINT` one line.
5. **Object dump** (`SMRTK_DUMP`) — class, handle, template, pos/hex, dome, workers/shifts, storage, modifiers,
   malfunction/destroyed/demolishing flags, `IsValid`; registered as the id 03b's Dump button calls.
6. **World snapshot** (`SMRTK_SNAPSHOT`) — sol, funding, colonists by status, buildings by class, resources,
   active disasters, current speed; and **diff** between two snapshot ids (`SMRTK_DIFF`).
7. **Watch a field** — a trigger (04's engine) on `SelectedObj.<field>` change; armed toggle, logs each change.

## Scope fence

IN: the two files + `metadata.lua` lines. OUT: the panel frame, World actions, slots, the stamper.

## Stop conditions

`LoadGame` from a mod thread wedges the loading screen on the desk · metadata cannot be read back without file I/O ·
`SMRTest` internals you need are local (then add a tiny accessor to `00_TestCore.lua` and say so).

## What may NOT be claimed

That a save/load round trip works (08). That the fingerprint's `N/N` is right (it is a read, quote it as one).

## Close-out

Rules 15–16. Commit per unit. Outbox to 07 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (02 appends here)
