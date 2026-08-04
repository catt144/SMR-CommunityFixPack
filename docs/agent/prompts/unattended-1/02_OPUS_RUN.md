# Chain prompt 2 — the run: prove, execute, record

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended once launched — **confirm with the owner in chat that the machine
is free before the first launch; that word is the only attendance in this
prompt.** Start with `git log --oneline -10` + `git pull`. Todo list up
front: one item per cycle plus one per recording commit — the owner reads
the list to see where the run is without a transcript.

**Read path**: this folder's README + the cycle plan in "Notes from
upstream" below · `docs/PLAYTEST_HELP.md` "The co-run rig" (the mechanics —
staging, arming at the run per rule 5, launch command, timing discipline) ·
the parked probe sources beside this file · the entries each leg records to
(`F99.md`, `C42.md`, `F35.md`, `F03.md`, the heal entries prompt 1 names).

## Jobs

**Job 1 — probe-hygiene sweep, then stage.** Sweep first (hard gate).
Stage the copy game-closed per the HELP procedure; the campaign save is
never written.

**Job 2 — cycle 0: the proof cycle.** Fixture confirms (all label reads) +
the SAVE-primitive proof exactly as prompt 1 wrote it. ⛔ Nothing that
leans on an unproven read or primitive runs before its proof passes. A
failed confirm turns its legs into `SKIP <reason>` lines and routed gaps —
continue with the rest.

**Job 3 — the leg cycles, per the plan.** For every cycle: arm at the run
(file + metadata line via a script FILE — C11), parse sweep, launch, read
the log after flush, disarm in the commit that records the answers, staged
saves and throwaway saves deleted, `PROBE SWEEP:` line, `git add -f` every
cited log. Every recorded number carries the run-conditions header.
Per-line watchdog discipline: if a cycle hangs, the probe's own watchdog
quits; **if the process must be killed from outside, that is an
unforeseen-issue finding — record how it presented before killing.**

**Job 4 — record as you go, not at the end.** Each leg's verdict goes on
its entry (or checklist rider line) in the commit that archives its log:
what was forced, what stayed organic, the falsifier, `SKIP` reasons
verbatim. Leg E flips the two `[NEVER RUN]` table rows to
`[RAN 2026-MM-DD, log <name>]` — only if the log actually shows the storm
start/stop and the electro devil (the fx class or an equivalent readable
mark; if nothing readable confirms the electro variant, say so and leave
the row marker honest).

**Job 5 — the unforeseen-issues ledger.** This run is the co-run program's
test bed. Keep a running list IN THE OUTBOX of every deviation, however
small: unexpected log lines (report verbatim with age — never discount),
timing surprises against predictions, retries, tool quirks, anything that
would have needed a hand. An uneventful run reports "none observed over N
cycles", which is itself the measurement.

**Job 6 — close out.** Append to `03_FABLE_AUDIT.md` "Notes from upstream":
per-leg verdicts with log names, the actuals-vs-predictions table, the
unforeseen-issues ledger, every routed gap, and anything owed. Update the
README manifest row; commit (doccheck green, push); delete this file in the
same commit.

## Stop conditions

- README chain-wide stops bind (modal/picker/hang → record, quit, route).
- A leg needs eyes or hands after all → chain rule 14: route it with the
  offer to author `02b_OPUS_CORUN.md` before the audit (measure-moments
  list, prep per rule 5, cost stated). Owner yes → build it, add its
  manifest row, append its handoff needs to the audit's inbox. No answer
  by your close-out → checklist rider, chain continues.
- The owner interrupts or needs the machine → finish the current cycle's
  disarm + recording commit, then stop cleanly; the chain resumes later
  from the todo list.
- Any leg's world-mutation leaks into a later read on the same cycle →
  void that read, note it, re-run the read on a fresh cycle.

## ⛔ What you may not claim

- Not `tested` for anything — unattended ceiling is MECHANISM /
  probe-verified (WORKFLOW triage mode 1).
- Not a refutation from any zero — state the CONDITION sampled and the
  count (leg C especially: zero `:805` under organic repair is a rate bound
  on the sampled configuration, not proof of unreachability).
- Not F99 severity — the discriminator's RESULT routes to the owner's
  existing decision line either way.
- Not rig capabilities beyond what this run exercised.

## Notes from upstream

*(Prompt 1 appends the cycle plan, predictions, parked-source list and open
risks here.)*
