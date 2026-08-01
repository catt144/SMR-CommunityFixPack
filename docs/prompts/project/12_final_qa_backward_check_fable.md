# Chain 12 — FINAL QA: the backward check over everything (run LAST)

**One-off; deletes this file AND `README.md` in its final commit — the
folder must end EMPTY. Read `README.md` first; its exclusion list is part of
your evidence.** Gate: this folder contains only this file + README. If any
numbered prompt remains, the chain is not done — stop and say which.

**Staleness check: `git log --oneline -10` + `git pull`.**

## The job — check BACKWARDS, trust nothing forward

You verify that the chain (and the two big efforts it drained — the
2026-08-01 bug-list audit and the F86 adjudication-through-build arc) left
nothing missed, pending, or wrong. You are adversarial: every "done" is a
claim; sample the evidence, not the assertion (this project's recorded facts
have been wrong before — `recorded-facts-are-claims` is a standing lesson).

1. **Inbox audit.** Git history of this folder: every deleted prompt's final
   commit should show its outbox landing in a later prompt or a BUGS/STATUS
   record. Hunt for notes that were written and never consumed, and for
   stop-and-ask items routed here — **resolve or present every one**.
2. **Owed-work sweep.** Grep the living docs (`STATUS`, `BUGS`, checklist,
   `FIX_POLICY`, the two standing prompts) for `owed`, `pending`,
   `blocked`, `gated`, `⚠`, `TODO`, `ask the owner` — classify every hit:
   done (point at evidence) / deliberately standing (name the gate) /
   DROPPED (present to the owner). The deliberate-standing list must match
   README's exclusions plus decisions the owner explicitly deferred.
3. **Consistency pass.** BUGS index rows ↔ heading tags (every one);
   STATUS counts recounted from `Code/` and TestKit, not inherited; the
   checklist references no retired test; probe sweep reads ZERO hits;
   `docs/prompts/` holds exactly the two standing prompts + live one-offs.
4. **Verification sampling.** Pick ≥3 status flips the chain made
   (e.g. Tier-1 entries, an approved audit fix, a D-build) and walk each
   back to its leg numbers in the log/commit — not to the entry's own claim.
5. **The freed state, stated.** Write
   `docs/reports/CHAIN_QA_REPORT.md`: verdict up front (CLEAR or the finding
   list), the standing-item table (owner decisions deferred, D13 + release
   gates as the post-playtest queue, the drone track's own prompt, owner
   web-checks if still open), and **the playtest campaign's current top** —
   what the owner should run first at the keyboard now that they are free.
6. Update `STATUS.md` (chain complete, pointer to the QA report) and
   `FABLE_NEXT_PROMPT.md`'s staleness line.

## Scope fence

**In:** verification, the report, presenting unresolved items. **Out:**
fixing anything substantive you find — a QA session that repairs its own
findings un-verifies itself. Trivial doc corrections (a stale row) are fine
WITH the finding recorded; anything larger is presented, not patched.

## Stop conditions

- A sampled verification fails (a flip without its leg) → that is the
  headline finding; finish the sweep, report, do not quietly re-run legs.
- The folder is not empty → stop immediately (gate above).

## What may not be claimed

CLEAR requires: zero unconsumed notes, zero unclassified owed-hits, zero
index/heading mismatches, all samples verified. Anything less is a findings
report, and that is a fully successful outcome too — say the true thing.

## On completion

Commit the QA report; delete this file and `README.md`; push. The owner is
free for playtesting.

## Notes from upstream

(any prompt may have routed standing items here — resolve them all)
