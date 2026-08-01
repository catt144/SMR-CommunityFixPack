# Chain 2 — F86 Phase 0: the two engine measurements (OWNER AT THE KEYBOARD)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** This is the Phase-0 half of the archived
`docs/archive/F86_NEXT_SESSION_PROMPT.md` (split into chain prompts 2+3 on
2026-08-01); content is carried faithfully — where this file and that one
disagree, THIS file is current.

**Staleness check: `git log --oneline -10` + `git pull`.** F86 is the single
release blocker; the analysis is finished and twice-verified; your job is
`docs/reports/F86_EXECUTION_PLAN.md` **Phase 0 only** (prompt 3 owns Phase 1).

## Read first (nothing else required)

1. `docs/reports/F86_EXECUTION_PLAN.md` — Phase 0.
2. `docs/reports/F86_ADJUDICATION.md` §4.1, §8.4-8.6 — why each measurement
   gates a design.
3. `docs/agent/ENGINE_FACTS.md` (2026-07-31 entries) + `FIX_POLICY.md` §3a.

## Standing rules

Todo list per WORKFLOW element 1. Console lines for the owner: **one command
per line**. Never modify the game directory. `ModLog` (never `print`) for
anything that must reach the log; `FlushLogFile()` before reading
mid-session; `IsValidThread(x) or false` when displaying thread validity.
Docs never lag findings — each probe result lands in ENGINE_FACTS in the same
commit as its log evidence.

## 0.0 ⛔ Stale-probe gate FIRST (HARD RULE)

`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` → todo list.
**Expected for THIS session: exactly ONE hit — `97_SaveHookProbe.lua`**
(declared: it IS the 0.2 instrument). Chain prompt 0 already deleted
`99_OrphanEnvProbe.lua`; if it is still present, prompt 0 did not complete —
STOP and check the chain state. Any other hit: repair before testing. Every
result commit carries the `PROBE SWEEP:` line.

## 0.1 GT-creation ordering — does `CreateGameTimeThread` run the body before the creating statement continues?

Hand the owner this as ONE console line, in a loaded colony, game UNPAUSED
(a paused game may defer GT scheduling and mask the answer — if the result
looks deferred, re-run unpaused before recording):

```
CreateGameTimeThread(function() ModLog("SMRPROBE-GTORDER: thread body ran") end) ModLog("SMRPROBE-GTORDER: statement after create ran")
FlushLogFile()
```

- body line FIRST → **run-at-creation**: the rains wrapper's naive shape is
  DEAD (its Msg posts before the vanilla loop can WaitMsg) — the Tier-1 spec
  takes the synchronous-heal branch; the F02 wrapper's defer-when-global-falsy
  guard is load-bearing.
- statement line FIRST → **deferred**: both authorised shapes work as
  written; the F02 guard stays anyway (defence in depth).
- Record verdict + log filename in ENGINE_FACTS. **A test that cannot
  discriminate is worse than none** — interleaving doubt → say so and re-run;
  do not guess.

## 0.2 The autosave hook (probe already armed)

`97_SaveHookProbe.lua` is live. The owner plays ~1 sol past an autosave (or
forces one), quits to desktop; read the newest log for
`SaveGameStart`/`SaveGameDone` with `autosave=true`. Record in ENGINE_FACTS
(upgrade or correct the "same path, source-only" entry).

## 0.3 Teardown

Delete `97_SaveHookProbe.lua` + its TestKit metadata/items lines in the same
commit as the recorded results.

## Scope fence

**In:** the two measurements, ENGINE_FACTS updates, `97` teardown.
**Out:** ANY fix-pack `Code/` change; Phase 1 (prompt 3 owns it); anything
drone. Interesting out-of-scope finding → file it, route it.

## Stop conditions

- 0.1 refuses to discriminate after two attempts → record "unresolved" in
  ENGINE_FACTS, note to prompt 3 that the rains repair MUST take the
  synchronous-heal shape (needs no ordering guarantee), and say so plainly.
- Owner unavailable → this session cannot run; stop, nothing else is
  runnable here.

## What may not be claimed

Nothing is MEASURED without a log filename + line read this session. Nothing
is RE-VERIFIED whose chain includes an inherited recorded fact not re-derived
(ENGINE_FACTS has been wrong twice before).

## On completion

Outbox → `3_f86_phase1_tier1_spec_fable.md`: both verdicts (or the
"unresolved → synchronous heal" instruction), the ENGINE_FACTS entry names,
the log filenames. Delete this file, commit, push.

## Notes from upstream

(prompt 0 appends the leg result + the one-hit expectation here)
