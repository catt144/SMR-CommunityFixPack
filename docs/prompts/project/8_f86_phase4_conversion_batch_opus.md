# Chain 8 — F86 Phase 4: the conversion batch + every approved audit fix, one leg

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gates: prompt 5's
Tier-2 leg verified (D10/D12 unhold recorded) and prompt 7's outbox below
states which fixes were approved. Authority for the conversions:
`docs/reports/SAVE_SAFETY_REDESIGN.md` §5.4 (the six A-class chained-wrapper
conversions).

## Jobs (todo list first; ONE ITEM PER MODULE — the Phase-4 lesson about
coarse lists is on WORKFLOW element 1; never bundle the batch behind one
checkbox)

1. **The six §5.4-A wrapper conversions**, one module per todo item, each
   parse-swept and committed separately. These are safety-shape conversions
   (full replacement → chained wrapper); behavior must be byte-equivalent —
   say so in each commit.
2. **Every fix prompt 7 approved**, built exactly to the spec written on its
   BUGS entry, one item each, incl. (if approved) the **F44 shell amendment**
   (C33) — that one touches `Fix_TrackSalvageWipe`, a `tested` module, so
   its A/B expectations must be stated BEFORE the leg.
3. **Probes** for every new fix (TestKit; explicit `return "PASS", …` — the
   fall-off-the-end trap is documented); probe-count changes land in STATUS.
4. **ONE leg for the whole batch** (stale-probe gate first; write the
   predicted numbers down before launching; counts WILL move if prompt 7
   approved new modules — predict them).
5. STATUS.md: new counts, batch results, and the chain's remaining tail.

## Scope fence

**In:** the six conversions, the approved fixes, their probes, the leg.
**Out:** anything prompt 7 did not approve; the four design-pass modules
§5.4 marks B-class (they stay as-is unless a later owner decision); D10/D12
(prompts 9/10); layer 1 (⛔).

## Stop conditions

- A conversion is NOT byte-equivalent in behavior when you diff carefully →
  it is a B-class in disguise; skip it, record why, route to prompt 12.
- The leg fails prediction → stop, report; the chain waits.
- Context pressure → self-split (`8b_…_opus.md`) — with this many modules,
  splitting EARLY beats splitting late.

## What may not be claimed

"Converted" requires the before/after diff summary in the commit message.
No new fix may be called `fixed` without its probe existing and the leg
passing. Counts are claims — recount, don't increment.

## On completion

Outbox → `9_d10_workshops_build_opus.md` (state + new counts). Delete this
file, commit, push.

## Notes from upstream

(prompt 7 appends approved-fix specs here)
