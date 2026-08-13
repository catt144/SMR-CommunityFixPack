# Chain prompt 2 — fresh-context adversarial QA of the derivation (the gate)

**Read `README.md` first — binding chain rules apply. You are a GATE: prompt 3
may not run unless your verdict is BUILD.** Staleness check (all three repos),
todo list. Precedent floor: the split-optins QA (SESSION_LOG 2026-08-12 —
every MUST-FIX it raised was real) and the split-optins terminal audit's
method (re-derive the ROUTE, not the citations).

**Your posture: the derivation is WRONG until you fail to break it.** The
project's own history says this stance pays: the enumeration was 12, then 13,
corrected both ways in one day, by a grep later proven blind — and the
"empty `_ENV`" persistence belief survived two audits before dying. Every
number in `90_DERIVATION.md` is a claim by a session that wanted to finish.

## Job 1 — re-derive, independently, before reading the draft's reasoning

Take the draft's TABLE (membership + lists) but not its arguments. Then:

* Run your own five-shape + capture-route sweep over BOTH trees — your own
  instrument invocations, your own hand-reads. Diff your membership against
  the draft's. Every difference is a finding; zero differences is a claim
  about your sweep's independence, so vary the method (different grep axes,
  different candidate ordering, read the AMBIGUOUS set whole).
* Sample-verify per-row provenance: for every row tagged MEASURED, find the
  measurement; for SOURCE, open the cited lines; INFERRED rows are attack
  surface — try to convert or kill each one.
* ⛔ Attack the three historical blindness classes BY NAME: slot assignments,
  global assignments, preset fields — the exact shapes the old grep missed.
  Then attack route (b) (captured locals/upvalues of engine frames), which no
  grep sees at all: pick the modules with `Sleep`-bearing bodies and trace
  what their frames actually hold.

## Job 2 — attack the KEEP/REMOVE lists (the save-breaking surface)

* For every REMOVE: what reads this name on a HEALTHY save? What does the
  reading code do when it is gone? (The F35 trap generalises: a repair the
  cleaner deletes re-breaks the save silently.)
* For every KEEP: does keeping it strand anything on a save whose pack never
  returns? Is it inert by §3a's definition (named, bounded, incapable)?
* For every thread-restart: is the one-shot bound real in the draft's design,
  and is the interval-reset cost stated per thread?

## Job 3 — rule on the rest

* The disposition draft: every site dispositioned; every 6f candidate
  actually routed (a "cleaner-target" that hides a reachable in-pack repair
  is the failure shape §3a names).
* The two owner questions as packaged: options honest, costs real, the
  recommendation supported by the derivation data (not inherited from the
  entry's hint). The channel-dissolving argument verified or refuted.
* The artifact sketch vs constitution 6d: anything in it that could persist
  (a thread, a GameVar, a named field, a notification closure) fails here,
  not in prompt 4.
* The doc-correction plan: is the location re-sweep actually complete
  (post-restructure paths), or does it inherit the entry's 2026-08-01 table?

## Verdict and close

Verdict: **BUILD** / **BUILD with MUST-FIXes** (enumerated, each with its
exact edit) / **BACK TO DERIVE** (with the break that forced it). Correct the
draft in place (strike-and-supersede, visibly — never silently). Append your
outbox to `03_OPUS_BUILD.md` `## Notes from upstream`: the verdict, every
MUST-FIX, your membership diff and how it settled, and what you did NOT get
to (named residue for prompt 5). Commit (doccheck GREEN), delete this file in
the same commit.

## ⛔ What you may not claim

- Not "complete" without your own independent sweep having found ZERO
  membership differences OR every difference settled by source reading.
- Not "the lists are safe" without Job 2 run per-name, both directions.
- A verdict of BUILD with unconverted INFERRED rows on load-bearing sites is
  a contradiction — convert them, kill them, or hold the gate.

## Notes from upstream (prompt 1 appends here)
