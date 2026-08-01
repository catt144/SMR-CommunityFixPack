# Chain 0 — the owed A/B code-gate leg + stale-probe teardown

**One-off; delete this file in your final commit (chain rule 1). Read
`README.md` in this folder first — its mechanics bind this session.**
Model-neutral body; routing is in the filename.

**Staleness check: `git log --oneline -10` + `git pull`.** Written after the
F49(a) strip (`0dc1039`) and the chain-creation commit. If unrecognised
commits landed since, read them before acting.

## Why this exists

The F49(a) guard was stripped from `Code/Fix_TrainMinors.lua` on 2026-08-01
(adjudicated R4 non-fix; BUGS.md F49 entry carries the full record) and the
TestKit probe lost its palette half in the same change (TestKit commit
`43d823d`, local-only repo). **Per the removal precedent (F24/F28/F49(c)),
an unattended A/B code-gate leg is owed and nothing else may claim "nothing
owed on the harness side" until it runs.** Separately, TestKit probe
`99_OrphanEnvProbe.lua` is stale-but-armed and contaminates logs and saves.

## Jobs, in order (todo list per WORKFLOW element 1 before starting)

1. **Stale-probe sweep (HARD GATE):**
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — put the
   result in the todo list. **Expected: exactly two hits** —
   `97_SaveHookProbe.lua` (KEEP: it is chain prompt 2's armed instrument;
   declare it) and `99_OrphanEnvProbe.lua` (STALE: its answer is recorded in
   the adjudication §8.1, but it re-arms on every LoadGame and fires a loud
   `[LUA ERROR]` ~1 sol later). Any OTHER hit: stop and repair first.
2. **Delete `99_OrphanEnvProbe.lua`** + its TestKit metadata/items lines;
   commit (TestKit is local-only, no push). This was Phase 0.0's first half —
   note in the outbox that prompt 2 should now expect exactly ONE hit (`97`).
3. **Run the owed code-gate leg** (recipe: `PLAYTEST_HELP.md`; facts:
   `FABLE_NEXT_PROMPT.md` harness section): check `Mars.exe` not running
   (`tasklist`) BEFORE touching loadable code; arm `96_AutoRunFlag.lua`;
   launch `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`;
   never kill on a short timeout (25-min guard). Read the account config from
   the leg's own `fix pack present:` line — never assume it.
4. **Judge the leg against the predictions recorded on the F49 entry:**
   counts unchanged (74 registered / 68 default-active); all-ON 68/0/10/0 or
   default 63/0/15/0 per what the account actually is; the TrainMinors probe
   PASSes with its new cap-only text (ONE expected fingerprint difference);
   zero `[CommunityFixPack]` error/disabled/FAILED lines; known noise only.
5. **Record:** result + `PROBE SWEEP:` line in the commit; update the F49
   entry ("A/B code-gate leg RAN <result>") and STATUS's owed-leg line.
   PASS → nothing owed on the harness side again. FAIL → diagnose before
   anything else in the chain runs; if the cause is not obvious, STOP and
   report — do not improvise repairs on a gate leg.

## Scope fence

- **In:** the sweep, the `99` deletion, the one leg, the records.
- **Out:** any `Code/` change in the fix pack; any other probe; any playtest;
  the checklist (prompt 1 owns it). Found something interesting → file it
  (BUGS.md) and route it (README rule 2).

## Stop conditions

- The sweep shows unexpected hits → repair or stop; no leg until clean.
- The leg FAILs for a non-obvious reason → report with the log excerpt; the
  chain waits.
- `Mars.exe` is running or the owner is mid-something → wait; never launch
  over a live session.

## What may not be claimed

"CLEAR" only with the leg's own numbers quoted from the log read THIS session.
No prediction may be reported as a result.

## On completion

Append your outbox (leg result + the `97`-only expectation + anything
discovered) to `2_f86_phase0_measurements_opus.md` → `## Notes from
upstream` — prompt 1 is doc-only and does not need harness notes, but copy
anything checklist-relevant to prompt 1 too. Then delete this file, commit,
push.

## Notes from upstream

(none — chain head)
