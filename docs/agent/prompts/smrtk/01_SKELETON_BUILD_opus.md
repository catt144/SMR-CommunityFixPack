# smrtk 01 — the walking skeleton (build)

Link 01 of `smrtk`. README binding rules 1–22 are yours. Staleness: rule 1 in both repos. Pre-flight: the
five facts' fingerprint (rule 12) and `Mars.exe` closed (rule 16).

## Job 0 — re-validate the cut (30 minutes, not a re-design)

Read the README's queue, layout and rules against `EF-095`–`EF-099` and the TestKit as it is on disk. If a link is
mis-sized, mis-ordered or rests on a premise you cannot find in the source, **rewrite that unconsumed link and say
so in its inbox and in ck175** — never absorb the disagreement silently. If the cut holds, write one line in 02's
inbox: "cut re-validated, no change".

## Job — the smallest end-to-end proof, predictions first

1. **Predictions first.** `reports/SMRTK_SKELETON_PREDICTIONS.md`: for every step 02 will run, the exact
   `[SMRTK]` line or read you expect (e.g. `SMRTK_TAINT_READ used=false`), and a 3× abort threshold. 02 scores
   against this file.
2. **`Code/70_SMRTK_Core.lua`** — `SMRTK = rawget(_G, "SMRTK") or {}` at load; `SMRTK.Log(verb, kv)` (the ONE
   logger, rule 7, running `id`, flush per line — reuse `SMRTest.Print`'s `%` escaping lesson); `SMRTK.Action{ id,
   label, page, run, arm, disarm, needs = "selected"|nil }` registry; `SMRTK.Bind(n, label, fn, opts)` slots API
   (the UI is P3's; the API is yours so 03A's payloads can register against it); the ring buffer (`OnMsg.ConsoleLine`,
   `OnMsg.OnLuaError` with stack, `OnMsg.OnThreadError`; ~300 lines; each with `GameTime()` and a mark index);
   the **taint assert** wrapper every action runs through (rule 8); `SMRTK.Mark(label)`; `SMRTK.CopySince(n_or_mark)`
   → `CopyToClipboard`; `SMRTK.Eligibility()` → `CanUnlockAchievement` reason or "OK"; `ConsoleEnabled = true`
   **before shortcuts build** — find the message that precedes `OnMsg.Shortcuts` on a map load and hook that (rule
   10; `EF-097`); LocalStorage read/write of panel state; auto-disarm hooks on `SavegameSaved`, `LoadGame`,
   `ChangeMap`. ⚠️ `EF-096`: whether native `ConsolePrint` reaches `ConsoleLine` is unverified — build the `print`
   tee as a **toggle (off)** fallback per rule 9 and let 02 measure which path carries lines.
3. **`Code/71_SMRTK_Panel.lua`** — the floating `XDialog`: status strip (taint · eligibility · armed count · quiet ·
   errors since mark), top row (MARK · Copy since mark · Flush · Pause/Resume · Stop disaster — the last two may be
   stubs that call P1's registry id and say "not built" until 03A lands), tab bar with `SMRTK.Page(id, label)` registry
   and empty Sitting/Agent/World/Saves/Kit pages, `[_]` collapse, drag, persistence, the hotkey (rule 20 collision
   check — write the result to ck175 either way). Plain look is fine; it must be usable with a mouse.
4. **`metadata.lua`** `code` list: add both files (H-10). Nothing else in `metadata.lua`.
5. **Desk checks:** `python tools/parsecheck.py` on both files; a lupa smoke of `SMRTK.Log`'s formatting with a `%`
   in a value; rule 6 and rule 7 greps quoted with counts.
6. **Write 02's script** into `02_SKELETON_SITTING_owner.md`'s inbox per rule 13: fenced lines, where each runs,
   the echo contract (the LOG), the first-screen witness per step, and the fixture (any 1.1.0 colony; `EF-079`).

## Scope fence

IN: the two files, `metadata.lua`'s list, the predictions doc, 02's inbox, ck175 notes. OUT: every page's content
(03A's payloads), the infopanel section (P2), docs (07). A World/Kit button you are tempted to add is a note in 03A's
inbox, not code.

## Stop conditions

`ConsoleEnabled` cannot be set before the shortcut build on a load path you can find · an X class you need is
blacklisted · the panel cannot be created from a mod without the Mod Editor · `OnMsg.ConsoleLine` never fires on
the desk and you cannot tell why. Report; do not force.

## What may NOT be claimed

That anything is untainted, that the hotkey works, that the tap sees lines — 02 decides all four. A GREEN whose
falsifier you did not see RED.

## Close-out

Green gates (rule 15), `Mars.exe` closed (rule 16). Commit per unit (core · panel · metadata · predictions);
outbox to 02 and 99; strike your row; `git rm` this file; push the pack repo.

## Notes from upstream

- (authoring session, 2026-09-13) The owner confirmed F9 clears the console (`EF-097`); do not build a second
  clear — the panel button calls `cls()` and that is all.
