# smrtk 02 — the skeleton in the real game (attended) — ⛔ KILL GATE

Link 02 of `smrtk`. Any model, the owner at the keyboard. README rules 1–20 are yours; rule 13 shaped the script
below (01 writes it). Score every step against `reports/SMRTK_SKELETON_PREDICTIONS.md`, prediction by prediction.

## The four premises this sitting decides

| # | premise | PASS reads as | FAIL means |
|---|---|---|---|
| P1 | a leaf action leaves `CheatsUsed` empty | `SMRTK_TAINT_READ used=false` AFTER a Fill on a selected depot, and the status strip says CLEAN; the Mod Manager is CLOSED throughout | the chain's requirement (A) is false at the source level — KILL, reduced 99 |
| P2 | `ConsoleEnabled` gives the console with mod tools closed | after a fresh load with the Mod Manager never opened, **Enter** opens the console | the load-time hook is wrong or the arm is too late — 01 re-fires with 02's log; not a kill unless a second try fails |
| P3 | the tap sees console lines | Copy-since-mark pastes the `[SMRTK]` lines AND at least one vanilla `print` line from the same window | the tee fallback carries it (02 records which); a kill only if neither path carries lines |
| P4 | the panel survives a save/load | after Save then Load, the panel is open on the same tab | persistence route wrong — 01 re-fires; not a kill |

The stale-probe gate binds: `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` → 0 before any reading,
and the line goes in the todo list.

## Pre-declared control (so PASS cannot be vacuous)

Before P1, the agent reads the same thing the vanilla way in a **scratch save that is then discarded**: open the Mod
Manager, press the vanilla infopanel `Fill`, read `CheatsUsed` — it must show one entry. That is the RED the
toolkit's GREEN is compared against. ⛔ That scratch save is never loaded again for a reading (`EF-051`: a stray save
is the falsifier's own hazard) — the owner names it `SMRTK_SCRATCH_TAINTED` and the agent records its deletion.

## Verdict

PASS / PASS WITH CORRECTIONS (strike-and-supersede the predictions doc, section by section) / KILL. Written to
`reports/SMRTK_SKELETON_SITTING.md` with the archived log path, and in plain language to ck175. A KILL is the gate
working: 99 runs its reduced form.

## What may NOT be claimed

Anything the log does not show. "Works on gamepad" (not tested here). That any page beyond the skeleton exists.

## Close-out

Outbox to 03, 03b, 04, 05, 06 (one paragraph each: what P1–P4 read, which tap path carries lines, the hotkey
that stuck) and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (01 writes the script here: fenced copy-paste lines, one per line, where each runs, the LOG witness per step, the
  fixture, the scratch-save control above as step 0.)
