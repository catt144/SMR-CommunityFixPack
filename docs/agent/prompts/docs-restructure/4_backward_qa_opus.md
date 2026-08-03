# 4 — Backward QA + the end-state handoff report (fresh context; trust nothing forward)

Runs from `docs/agent/prompts/docs-restructure/` (prompt 3 moved the folder).
Staleness check; read the spec + all Notes from upstream. This prompt CLOSES
the chain: the folder must end empty.

## Part A — verify, sampling against git history, not the chain's claims

1. **Conservation**: pick 5 random `agent/bugs/` entries + 5 `agent/facts/`
   entries; diff their bodies against extracts from
   `git show <pre-chain-commit>:docs/BUGS.md` and `:docs/agent/ENGINE_FACTS.md`
   — bodies must be byte-identical (front matter and heading handling per the
   split specs are the only permitted deltas).
2. **Counts**: `doccheck --emit-counts` must equal prompt 1's recorded
   baseline (98 F + 12 D + 41 C rows; 82 Code files; 81 modules; 87 probes) —
   this chain moved text, so ANY count change is a defect, not an update.
3. **Structure**: doccheck v3 green (paste output); root allowlist holds both
   directions; stubs at `docs/BUGS.md`, `docs/STATUS.md`,
   `docs/agent/ENGINE_FACTS.md` resolve; the pre-commit hook fires on a test
   commit; CLAUDE.md is accurate (REMOVE its "layout live after the chain"
   line now).
4. **Spot-usability**: as a fresh session, answer "what is F90's status and
   evidence?" using ONLY CLAUDE.md → STATE.md → bugs/INDEX.md → F90.md.
   Record the hop count and anything that felt missing.

## Part B — ⭐ THE END-STATE HANDOFF REPORT (owner-requested; this is a
## first-class deliverable, not a QA formality)

Write `docs/agent/reports/DOCS_RESTRUCTURE_REPORT.md`. **Its purpose: the
owner will feed it to a fresh top-tier (Fable) session that will REDESIGN the
project's standing prompts and authoring conventions against the new
structure. That session was deliberately NOT given this job here — prompt
redesign is compounding-risk design work, the top-tier slot — so this report
is its entire picture of reality. Write it for that reader.** Contents:

1. **The as-built tree**, complete: every directory and file the chain
   created/moved/stubbed, with one line each on role and format (front-matter
   fields, generated files, banners). Include a real `tree`-style listing.
2. **Deviations from the spec** — every place execution differed from
   `DOC_RESTRUCTURE_SPEC.md` and why (there will be some; a report that
   claims none is suspect).
3. **The read-path economics**: for three representative agent questions
   (a bug's status; an engine fact; "what do I read at session start"), the
   actual hop sequence and rough token cost under the new layout vs the old.
4. **What doccheck enforces as of v3**, exactly, and what it deliberately
   does not.
5. **Friction log**: everything that was awkward, ambiguous, or surprising
   during migration — parser edge cases hit, references that had no good
   home, judgment calls made under rule pressure. This is the raw material
   for the redesign.
6. **The standing-prompts inventory for the redesigner**: current state of
   `agent/prompts/FABLE_NEXT_PROMPT.md` and `DRONE_PROJECT_PROMPT.md` (which
   paths were mechanically fixed by prompt 3, which content now reads stale
   against the new structure), plus WORKFLOW elements 1–7 and the spec §7
   adopted-rules block — with this prompt's own observations on what the
   redesign should reconsider, marked as OBSERVATIONS, not decisions.
7. **Open items** routed onward (anything discovered but out of scope).

## Close-out

Verdict (CLEAR or findings — a findings report is a fully successful
outcome), update STATE.md's pointers, add one line to the checklist's
"Decisions waiting on you": *"feed DOCS_RESTRUCTURE_REPORT.md to a Fable
session to redesign the standing prompts"*. Strike the last README rows,
delete README + this file (folder EMPTY), commit with doccheck output in the
body, push.

Stop: any conservation diff → headline finding, finish the sweep, do NOT
patch content. May not claim CLEAR with any unexplained byte, and may not
skip Part B regardless of Part A's outcome.

## Notes from upstream

(none yet)
