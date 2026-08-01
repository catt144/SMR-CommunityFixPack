# Chain 4 — F86 Phase 2: build Tier 1 and prove it with its own legs

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gate: this session
runs ONLY if `docs/prompts/F86_TIER1_BUILD_PROMPT.md` exists (prompt 3 writes
it). If it does not, stop — the chain is out of order.

## The job

**Execute `F86_TIER1_BUILD_PROMPT.md` exactly.** That brief (written with
full spec context by prompt 3) is the authority for this session — scope,
build order, leg definitions, todo granularity. This chain file only pins the
chain-level obligations around it:

1. **Stale-probe gate before any leg** (zero hits expected now — `97` and
   `99` are gone; declare anything you arm yourself).
2. The build touches `Fix_MeteorFrequency` and `Fix_RainsDeadlock` (both
   full rewrites, incl. the C34 rider) — **check `Mars.exe` is not running
   before touching loadable code**, and parse-sweep every edited Lua file
   before each commit.
3. **The legs are the verification** (one tier, per owner decision 7):
   the A/B pair, the F88 load-3×-inside-a-rolled-interval regression
   mini-leg, and the PT-20-method uninstall leg (expect: zero orphan errors,
   vanilla threads present, `ListFixes` clean). **These legs are also PT-54's
   retirement made good** — record their results on the F78/F81/F02/F88 BUGS
   entries and flip statuses per the protocol (index row + heading tag,
   BOTH).
4. TestKit probes: update/replace the probes covering the rewritten modules
   so no probe asserts deleted behavior (the F28/F49 lesson); probe-count
   changes land in STATUS in the same commit.
5. STATUS.md: rewrite the F86 block to the post-Tier-1 truth (what shipped,
   what the legs read, what Tier 2 still owes).

## Scope fence

**In:** exactly what the build prompt authorises. **Out:** Tier 2 (prompt 5),
layer 1 (⛔), D10/D12 (still held until Tier-2 verifies per the owner's
gate), drones, the cleaner. Anything discovered → file + route.

## Stop conditions

- Any leg reads numbers the build prompt did not predict → stop at the
  failing leg, report with log lines; no further chain work until resolved.
- The uninstall leg shows ANY mod-named residue the spec said would be gone →
  that is a spec falsification, not a tuning issue: stop, report, owner call.
- Context pressure → self-split per README rule 3 (`4b_…_fable.md`).

## What may not be claimed

"Repaired" only with the uninstall leg's own log quoted. The F88 fix may not
be claimed without the load-3× mini-leg's meteor arriving on the persisted
deadline. No status flips without both BUGS locations updated.

## On completion

Delete `F86_TIER1_BUILD_PROMPT.md` (consumed) in the same commit as this
file. Outbox → `5_f86_phase3_tier2_build_opus.md`: what landed, leg numbers,
anything the Tier-2 builds must respect. Commit, push.

## Notes from upstream

**From prompt 1 (2026-08-01) — two things become true when your legs pass, and
both are already written and waiting.**

1. **`MOD_DESCRIPTION.md` holds a `[FAQ]`-tagged sentence that is deliberately
   NOT yet publishable** — the claim that no mod in either game's community has
   held itself to this uninstall standard (`PRIOR_ART_SURVEY.md` §6). It sits
   under a `[DRAFT NOTE — CONDITIONAL]` marker because our own
   `Fix_MeteorFrequency` is currently one of the modules leaving a running
   thread behind, which makes the claim false while it is true. **If your
   uninstall leg passes on its own log, delete the DRAFT NOTE and keep the
   sentence; if it does not, leave the marker exactly where it is.** Do not
   soften the sentence to make it survive a weaker result.
2. **PT-54 was retired into your legs** (prompt 1's record;
   `PLAYTEST_CHECKLIST.md` §3 carries the trigger-by-trigger absorption table,
   full text in `PLAYTEST_ARCHIVE.md`). Triggers C, D and E are yours. Triggers
   A and B are **not** absorbed by the Tier-1 shape and were routed to prompt 3
   to be written into `F86_TIER1_BUILD_PROMPT.md` as legs against
   `Fix_DisasterPredictionLeak` — if the build prompt you receive does not
   carry them, that is prompt 3 dropping a routed item, not a scope reduction
   you may accept silently.

(prompt 3 appends the build-prompt pointer + non-relitigable decisions here)
