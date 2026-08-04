# Chain prompt 3 — co-run #1: the first payload, and the first evidence cards

**Read `README.md` in this folder first — binding chain rules apply.** Start
with `git log --oneline -10` + `git pull`, then `CORUN_RIG_SPEC.md` (as
corrected by prompt 2 — the corrections are part of the spec) and prompt 2's
outbox below. If prompt 2's outbox is missing, STOP — the kill-gate may have
fired; check the manifest.

**ATTENDED (~15–20 min of owner time), batched per the WORKFLOW batch rule:**
one launch drains everything below. Prep everything unattended first; the
todo list tells the owner when to sit down.

## The payload (from the checklist's tagged candidates)

1. **F11 pre-wrapper watch** (Tier A — WITNESS): staged passenger line, owner
   watches one unload — train leaves, stats move, `ListFixes` shows
   `TrainPlatformWedge [active]`. This is the rider "F11: verify the
   pre-wrapper conversion"; a PASS earns the conversion `tested` **per the
   rider's own terms** (it was written for exactly this).
2. **F99 hex tie-break read** (ride-along, no eyes): on a hex holding a hidden
   broken element and its repair site, what does `HexGetTrackGridElement`
   return? One console/scripted read; settles `F99.md`'s last C-side link.
3. **C41 amplification loop** (Tier A — WITNESS): drive the depot spawn/open
   cycle repeatedly while the owner watches for the picker failing to appear
   (`F76MISS` is the instrument). Intermittent-trigger amplification is THE
   class-2 use case — record hit rate per N cycles, even if the answer is
   0/N.
4. **F11 Done-timing trace** — ONLY if prompt 2's outbox says it was not
   settled in the skeleton.

For each: produce an **evidence card** per the spec's Tier B template — even
for the Tier A items, because prompt 4 audits whether the cards would have
sufficed without the owner's eyes. The cards are the experiment inside the
experiment.

## Jobs

**Job 1 — todo list up front**, one item per payload item plus prep/close
units, "OWNER SITS DOWN HERE" marked.

**Job 2 — prep unattended:** probe sweep (record the line); staged save copy;
scenario scripts as `TEMPORARY` TestKit files; parse sweep; measure-moments
list with the owner's verdict words pre-written ("train left / train stuck",
"picker appeared / missing", …).

**Job 3 — the run**, batched: fixed cost first (launch, load, warm-up per
spec), then payload items in the order above — owner-needed items
back-to-back so their attended window is contiguous, ride-alongs after they
leave. Record actual wall-clock and actual owner-minutes.

**Job 4 — record, one commit per verdict class:** rider outcomes to their
entries and checklist rows (strike/annotate per convention); the tie-break
verdict to `F99.md`; every recorded number cites its log line; forced/organic
labels on everything; TEMPORARY probes deleted in the recording commits;
`PROBE SWEEP:` lines throughout; archive the log if cited.

**Job 5 — close:** outbox to prompt 4 — verdicts, evidence cards (or where
they live), actual costs vs. spec, owner-minutes used vs. promised, and your
honest note on which payload items the cards alone would have settled; delete
this file in the same commit; doccheck green; push.

## Scope fence

**In:** the four payload items, their evidence cards, cost accounting.
**Out:** any fix (route findings); the F99 no-cheat discriminator (needs
drone-repair wall-clock the spec has not budgeted — route it as a rider for
the NEXT co-run with the measured fixed-cost numbers attached, so the owner
can price it); new candidates discovered mid-run (rider them, rule 3).

## Stop conditions

- The C41 loop perturbs the game state it measures (spawn side-effects piling
  up) → stop the loop, record N so far, note the perturbation — an honest
  0/N-with-caveat beats a contaminated 0/2N.
- Owner has to leave mid-window → finish the current item, run the remaining
  ride-alongs, leave the rest as riders. Their time budget is the contract.

## ⛔ What you may not claim

- Not `tested` for anything except F11's watch rider on ITS OWN terms (Tier A
  witness PASS) — nothing else in this run has a rider granting that word.
- Not "C41 refuted" from 0/N — absence of the intermittent under N forced
  cycles is a rate bound, not a refutation; say the number.
- Not that the evidence cards suffice for sign-off — that is prompt 4's
  question and then the owner's.

## Notes from upstream

*(Prompt 2 appends here: skeleton verdict, actual costs, spec corrections,
whether the Done-timing trace already ran, and anything about the launch/load
path prompt 3 must do differently.)*
