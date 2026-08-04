# Chain prompt 2 — co-run #0: the walking skeleton, with a kill-gate

**Read `README.md` in this folder first — binding chain rules apply,
especially rules 8 (save copy + probe hygiene) and 10 (no assumed
capability).** Start with `git log --oneline -10` + `git pull`, then read
`CORUN_RIG_SPEC.md` in this folder — you execute its co-run #0 definition
VERBATIM. If the spec is missing or its co-run #0 section is incomplete, STOP:
prompt 1 has not run or did not finish; do not improvise a skeleton.

**ATTENDED (~10 min of owner time).** This is the first co-run ever run.
Everything is prepped before the owner sits down; the todo list is how they
know when. Schedule by asking in-session; if the owner is not available, prep
everything, commit, and leave the run itself as the only unchecked item.

## Jobs

**Job 1 — todo list up front**, one item per unit including "OWNER SITS DOWN
HERE" placed exactly where their time starts.

**Job 2 — prep, all unattended:** probe-hygiene sweep (record the line);
stage the save COPY per spec; write the scenario script(s) — the trivial
read + the F11 Done-timing ride-along — as TestKit files carrying the literal
`TEMPORARY` marker; parse sweep; pre-write the measure-moments list (what the
owner will see, what verdict words to say back).

**Job 3 — the run.** Execute the spec's step list. Record ACTUAL wall-clock
per step next to the spec's prediction. The owner launches (or you do, if the
spec binned agent-launch PROVEN) and stands by; you drive everything else and
read the log back after quit.

**Job 4 — the kill-gate, honestly applied.** Compare actuals to the spec's
abort criteria. Three outcomes, and you write down which one happened:

- **PASS** — every UNKNOWN answered, costs within bounds → hand to prompt 3.
- **PASS WITH CORRECTIONS** — it worked but the spec was wrong somewhere →
  correct `CORUN_RIG_SPEC.md` visibly (strike-and-supersede, never silent) and
  hand to prompt 3.
- ⛔ **KILL** — a foundation primitive failed or a step blew its 3× budget →
  the chain STOPS HERE. Append findings to prompt 4's `## Notes from
  upstream` (skipping 3), route the situation to the owner with options
  (respec / descope / abandon), and delete this file AND
  `03_OPUS_PAYLOAD_RUN.md` in the same commit, updating both manifest rows.
  **Prompt 4 still runs** — it audits what was learned and empties the folder.
  A killed chain that recorded why is a success of the gate, not a failure of
  the chain; say it that way.

**Job 5 — record.** The Done-timing verdict goes to `F11.md` (it settles the
"Route claim narrowed" question — SYNC = OnTransferToMapDone route confirmed,
DEFERRED = the `:1209` route confirmed; either way MEASURED, cite the log
line). Delete the TEMPORARY probes in the same commit that records their
answers (`PROBE SWEEP:` line in the commit). Archive the run's log if any
recorded number cites it.

**Job 6 — close:** outbox to prompt 3 (or 4, on KILL) — actual costs, spec
corrections, owner-minutes actually used vs. promised; delete this file in the
same commit; doccheck green; push.

## Scope fence

**In:** the skeleton steps, the ride-along trace, cost measurement, spec
corrections. **Out:** ANY payload rider (that is prompt 3 — do not "just
quickly" do the F11 watch even if the game is sitting there and it is
tempting; the skeleton's budget discipline is itself under test), any fix,
any new probe beyond the two scripted ones.

## Stop conditions

- Owner unavailable after prep → commit prep, report, leave the run owed.
- The game hangs and the abort protocol fails (agent blind, no timeout fires)
  → have the owner kill the process, record it as an UNKNOWN answered "no",
  and treat per the kill-gate.

## ⛔ What you may not claim

- Not that the rig "works" beyond what the skeleton exercised — the envelope
  stays the spec's, updated only by what actually ran.
- Not `tested` for anything — the ride-along verdict is MEASURED mechanism
  evidence, labeled forced/organic per rule 11.
- Not owner-minutes savings — prompt 4 owns the economics audit.

## Notes from upstream

*(Prompt 1 appends here: the co-run #0 definition pointer, the UNKNOWN list the
skeleton must answer, predicted costs, and anything the inventory found that
changes this prompt's jobs.)*
