# Chain prompt 3 — freeze the spec, build the artifact, correct every count

**Read `README.md` first — binding chain rules apply.** Staleness check (all
three repos), todo list. ⛔ **GATE CHECK BEFORE ANY WORK (README rule 7):**
prompt 2's verdict must be BUILD (its Notes below), and BOTH owner answers
(Q-A player story, Q-B channel/mod-shape confirmation) must be recorded on
`docs/PLAYTEST_CHECKLIST.md`. **Either missing → STOP: report which, commit
nothing but the report note, leave this file in place. The chain resumes here
when the owner answers.** Game closed throughout; nothing here launches.

## Job 1 — freeze the spec

From the QA-corrected `90_DERIVATION.md` + the owner's Q-A answer: write the
artifact spec INTO the derivation doc (one doc carries derivation → lists →
disposition → spec, so prompt 5 audits one chain of custody). The spec states:
detection (the curated list as embedded data — repo, name, kind, KEEP/REMOVE,
why), the clean pass order, the one-shot thread-restart set with per-thread
interval cost, what the player sees (report text), the version-skew statement
(which pack versions' residue it handles — say how a too-old or too-new save
is answered), the self-removal story, and the constitution-6d compliance
argument (why nothing of the artifact can persist).

## Job 2 — scaffold and build

* Scaffold the artifact repo per the QA-reviewed proposal (working name from
  prompt 1; LOCAL git, no remote unasked — README rule; junction installed
  but the mod NOT enabled — enabling is owner-only, and the verify prompt
  works junction-side per EF-055 regardless). Scaffolding depth per the
  proposal: the split's `SMR-OptInPack` scaffold is precedent, but this
  artifact is a single-purpose tool — carry PROVENANCE (what came from
  where), a README that answers the no-retraining questions AT ITS SIZE, and
  doccheck only if the proposal argued for it; do not cargo-cult the full
  pack apparatus where the proposal said it is not needed.
* Build the cleaner to the frozen spec. FIX_POLICY binds where it applies
  (fail-safe, never loud; self-checks return reasons, never error). Every
  Lua file parse-swept before commit.
* TestKit: teach the kit to see the artifact the way it learned the opt-in
  pack (a missing artifact is SKIP, never FAIL — it is legitimately absent
  from every config but the rescue ones), and write its probes: the clean
  pass on synthetic residue (KEEP survives, REMOVE goes, one-shot bound
  holds), the artifact-absent no-op, the version-skew answers. If you
  re-baseline the suite here, take the queued `FactionFundingCheck`
  PASS→SKIP repair (TestKit `62f03da`, comment on the probe) in the same
  measured commit and re-stamp the baseline everywhere it is quoted;
  otherwise leave it queued and say so.

## Job 3 — correct every count-stating doc (the derivation is authoritative)

Re-sweep BOTH repos' current docs for every count/denominator the derivation
supersedes ("≥13", "at least 13", "12 exposed", "five of the twelve", every
per-module denominator in the F86 reports). The D13 entry's location table is
the 2026-08-01 starting point with pre-restructure paths — translate and
re-sweep; your sweep's method line goes in the commit. Archive-tier files
(`docs/archive/`) are history and are NOT edited. Every corrected site cites
`agent/reports/D13_EXPOSED_SET.md` — which you create in this job by
promoting the QA-corrected derivation doc (the in-folder draft stays until
prompt 5 deletes the folder). Update the D13 entry itself: front-matter +
heading tag to `speced`/`built` per the truth at your close (edit order:
front matter first, then tag — doccheck red means you stopped halfway).

## Close

doccheck GREEN in every repo that has it; parse sweep GREEN; PROBE SWEEP line
in every result-bearing commit. Append your outbox to `04_OPUS_VERIFY.md`
`## Notes from upstream`: what shipped where (repos, shas), the spec's
verification-relevant promises (exact KEEP/REMOVE names the matrix must read,
the thread set, the version-skew answers), the fixture requirements you
foresee (which saves carry which residue classes — the split matrix's
FixtureCarry dumps say PT35FIXTURE carries fields + `MeteorLatch`; say what a
PRE-REWRITE-lineage witness needs and whether one exists in the save folder
BY NAME, or must be manufactured by a probe writing synthetic residue), and
every uncertainty. Delete this file in the same commit.

## ⛔ What you may not claim

- Not "the artifact works" — nothing launched; every claim here is
  static/probe-design tier and says so.
- Not "residue-zero" — that is prompt 4's measured claim; yours is the
  compliance ARGUMENT (no thread, no GameVar, no field, no closure — cited).
- Not "all docs corrected" without the sweep method stated and the archive
  exclusion honored.
- Not "suite baseline unchanged" if you touched any probe — recount or say
  which change is pending measurement.

## Notes from upstream (prompt 2 appends here)
