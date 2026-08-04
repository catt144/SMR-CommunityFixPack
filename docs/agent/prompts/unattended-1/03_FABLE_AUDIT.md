# Chain prompt 3 — adversarial audit, the unforeseen-issues report, integration

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 2 touched · the archived logs it cites · the
`CORUN_RIG_SPEC` audit precedent if useful
(`git show 93088ba:docs/agent/prompts/corun-rig/CORUN_RIG_SPEC.md`).

**Every "done", "PASS", "SKIP" and "measured" upstream is a claim.** This is
the owner's audit floor for unattended work (their rule, 2026-08-04): the
whole reason this prompt exists on a separate tier is that nobody watched
the run.

## Jobs

**Job 1 — audit the run record, verdict-by-verdict, against the archived
logs.** Does each cited line say what the entry now says? Are
forced/organic labels present and honest — leg C's repair especially: the
log must show the repair happened WITHOUT the completion cheat. Are `SKIP`
reasons true against the cycle-0 confirm reads? Did any number get rounded
or any zero get dressed as a refutation (condition-sampled rule)? Were the
`[NEVER RUN]` → `[RAN]` flips justified by readable log evidence? Commit
discipline: probes deleted in their recording commits, sweeps present,
staged/throwaway saves gone, every cited log actually archived
(`git show` it — a claimed archive that a plain `git add` silently dropped
is the known failure). ⛔ A missing archived log is an automatic finding,
not a shrug. Corrections visible, never silent; a correction that changes a
verdict re-routes that item to the owner.

**Job 2 — audit the SAVE-primitive claim chain.** If prompt 2 promoted it
to PROVEN, verify the proof cycle's log shows save → list → load-back on
the throwaway name, and that the WORKFLOW envelope update (Job 4) states
exactly what ran, no more. If the proof failed, verify legs A/D were routed
as gaps and not quietly improvised.

**Job 3 — the unforeseen-issues report (the run's second product, and the
owner's actual question).** From prompt 2's ledger AND your own audit
residue: everything that surprised, deviated, retried, or would have needed
a hand — each with its log line, whether it recurs, and what it means for
the CO-RUN program specifically (that is the decision this feeds: the owner
runs co-runs next; what should their briefs guard against?). "None observed
over N cycles" is a legitimate report if the audit sustains it. Route
anything that changes a co-run assumption into `WORKFLOW.md` "Co-runs" or
the HELP rig section — surgically, no sprawl.

**Job 4 — integrate.** Entries carry their verdicts (already, per prompt 2
— verify rather than re-write); checklist: strike/annotate the lines this
run settled (PT-35, the F99 residue rider, leg E's rows; the F99
discriminator RESULT lands on the owner's existing F99 decision line as
input, never as the decision); `WORKFLOW.md` capability envelope: add what
this run PROVED (the save primitive, if it passed) and nothing it did not;
`STATE.md`: chain CLOSED line (cap 60, evict in-commit); `SESSION_LOG.md`:
the chain's record, newest-first — verdicts, actuals-vs-predictions,
economics of the batch (machine time, owner time ≈ 0 + kickoff word, token
actuals unrecorded unless you have them), the unforeseen-issues summary;
`CHAIN_METHOD.md`: one lesson entry ONLY if this chain taught something the
corun-rig close did not (the first Opus-executes/Fable-audits instance —
did the audit floor catch anything? Say honestly either way).

**Job 5 — close the chain.** Delete every remaining file in this folder in
the closing commit (parked sources included — they survive in git; cite the
pre-deletion sha in the SESSION_LOG record). doccheck green, push. Then
report to the owner: what ran, what each leg found, what the batch cost
(against the ~90 s/cycle + zero-owner expectation), what the audit caught,
the unforeseen-issues verdict for the co-run program, and what is owed or
routed. ⛔ **The report ENDS with the next-chain kickoff** (chain rule 14):
read `STATE.md`'s NEXT pointer and give the owner the exact line to start —
which model, which prompt file — or say plainly that nothing is queued and
name what the front of the co-run queue looks like instead. If a
`02b_OPUS_CORUN.md` was inserted upstream, its results were claims like any
other (Job 1 covers them) and its owner-minutes go into the batch cost.

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route the item to the owner, keep closing the chain.
- Prompt 2 stopped mid-run (owner interrupt, stop condition): audit what
  ran, inventory what did not into routed items with their staged state
  cleaned up, and still empty the folder — an honestly-closed partial chain
  beats a lingering one.

## ⛔ What you may not claim

- Not `tested` for anything in this chain.
- Not "the rig is ready for co-runs" as a blanket — say which assumptions
  this run exercised and which it could not (it had no eyes/hands moments,
  which is precisely what co-runs add).
- Not owner-time savings — one batch is a data point; report cost against
  the expectation, per WORKFLOW.
- Not F99 severity, reachability beyond what leg C actually sampled, or any
  tier/sign-off change (still routed, still the owner's).

## Notes from upstream

*(Prompt 2 appends per-leg verdicts, the actuals table, the
unforeseen-issues ledger, routed gaps, and anything owed.)*
