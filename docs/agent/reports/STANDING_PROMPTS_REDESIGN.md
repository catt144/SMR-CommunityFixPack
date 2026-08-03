# Standing-prompts redesign — decision record (Fable, owner-triggered, 2026-08-03)

Executed from `REDESIGN_STANDING_PROMPTS_FABLE.md` (self-deleted with this
commit) against `DOCS_RESTRUCTURE_REPORT.md`'s §6 inventory and O1–O7.
Immutable once committed, like every report. Authority order unchanged; this
report is not authority over `agent/bugs/` or `agent/facts/`.

## 1 · O1–O7 verdicts, each with its reasoning

- **O1 (read-path element 8 for all briefs) — ADOPTED, in WORKFLOW.**
  Every stale item in the report's §6 inventory was a folder-granularity
  reading instruction; a brief that names its files at file granularity plus
  the index is one whose staleness the next session can check against git.
  Landed as WORKFLOW required-element **8**; both rewritten prompts' read
  paths now comply with it.
- **O2 (`row_status:` relocation) — DEFERRED.** The field is load-bearing for
  conservation and lives in `agent/bugs/` front matter — fenced out of this
  brief — and moving it means a schema + doccheck + INDEX-regeneration change.
  If ever taken it is a scripted job to a SPEC (O6's shape), not an edit.
  Cost of deferral: front-matter skimmability on heavy entries, nothing else.
- **O3 (mandatory read points at folders, not indexes) — ADOPTED.** One-word
  class fix: STATE.md's pointer line now names `agent/bugs/INDEX.md` /
  `agent/facts/INDEX.md`; WORKFLOW's reading path and both prompts route
  through the two indexes explicitly.
- **O4 (status/heading-tag edit order is folklore) — ADOPTED, one sentence.**
  WORKFLOW mechanical rule 6 now states the order: front-matter `status:`
  first (the index regenerates from it), then the heading tag, same edit —
  a red doccheck means you stopped halfway.
- **O5 (link/path resolver in doccheck) — DECLINED.** The omission was
  deliberate and the false-positive cost (archive's intentionally-stale
  paths, `<ID>` placeholders, prose) is real and unmeasured; `tools/` is
  outside this brief's fence anyway. The two throwaway sweeps in the report
  are the recipe: any future restructure-class chain should run one as a
  chain step (this session did — §4 below), not grow a standing checker.
- **O6 (topical EF ids) — DECLINED; the window it depended on is already
  shut.** O6's own condition was "cheap only until something cites `EF-###`"
  — `agent/STATE.md` cites `agent/facts/EF-014` today, and this redesign adds
  mandatory per-id opens (EF-019/022/023) to the drone prompt. The INDEX.md
  summary column already provides topical lookup at 7,293 B, which is most of
  what topical filenames would buy. If the owner wants it regardless: scripted
  rename job to SPEC, never an edit.
- **O7 (60-line cap with no eviction rule) — ADOPTED.** Canonical rule is
  WORKFLOW mechanical rule **8**: evict resolved/superseded material to
  `SESSION_LOG.md` in the same commit; never evict open gates, holds, owner
  decisions or the counts block. Both prompts' close-out steps now cite it.

Stop-and-ask check: none of the adoptions touches the CHAIN mechanics
(self-consumption, inbox/outbox, model placement). O1 extends the
brief-authoring element list the chain rules reference — the brief itself
pre-authorized exactly that ("a WORKFLOW change, adopt it there if taken").

## 2 · `GENERAL_USE_PROMPT.md` — what changed and why

Rewritten in full; the standing session rules (probe gate job 0,
account-state, §4a, PT-52 freeze, game-dir/Mars.exe rules, F76 block, console
and harness facts) are **unchanged in substance**. The changes:

1. **The "`docs/agent/facts/` — whole file" instruction is dead** (report §3
   Q3, its highest-value item). Read-first item 2 is now: scan
   `facts/INDEX.md`'s 43 rows, open only the facts the sitting touches — with
   the explicit warning that reading all 43 files re-spends what the
   restructure saved.
2. **Read-first is element-8 compliant**: STATE.md → facts/INDEX.md →
   checklist+HELP → bugs/INDEX.md→entries → FIX_POLICY §§ → REACHABILITY_AUDIT
   "Challenge review". The bugs read now says what the INDEX row answers
   (status/priority/evidence-label) vs what needs the entry (narrative).
3. **Close-out carries O7's eviction rule** and points at WORKFLOW rule 8.
4. **Chain routing retired**: "route to `docs/agent/prompts/project/`" pointed
   at a directory that does not exist in git. Job 3 and the close-out now say:
   FILE it — entry, plus checklist rider with TAKEABLE-WHEN when
   situation-gated. No project chain is active to route to.
5. **Status flips cite the O4 edit order** (front matter first, then tag).
6. DOCS LAYOUT block rewritten around the two INDEX entry points; staleness
   anchor updated to this redesign.

## 3 · `DRONE_PROJECT_PROMPT.md` — scaffolding only; drone content untouched

D06 design decisions, freezes, the three options, gates Q1–Q4, §§2–4 and
§§6–8 substance: **not touched**. The scaffolding changes:

1. **The stale `DOCS LAYOUT (reorganised 2026-08-01)` block** — all three
   false claims the report named (STATUS at root, bugs at root,
   MOD_DESCRIPTION as daily truth) replaced with the as-built 2026-08-03 tree
   and the two INDEX entry points.
2. **Reading order is element-8 compliant**, and the vague "every fact"
   instruction became mandatory named opens: `EF-022.md` (the
   closure-persistence fact the old text alluded to without an id),
   `EF-023.md`, `EF-019.md`.
3. **The `prompts/project/README.md` reference: RETIRED, not rewritten**
   (report §7.1). The chain README was consumed with the chain and exists
   only in git history; no README is written — resurrecting a consumed chain
   artifact to hold one clearance record would recreate the drift class this
   redesign exists to end. The ADDENDUM's carve-out item is updated to past
   tense — pre-cleared AND landed — because the chain that was "going to"
   move the wrapper call completed on 2026-08-03; its instruction (don't
   re-do, rebase on the module as it stands) is unchanged.
4. Three `agent/bugs/  F86`-shape half-citations fixed to `F86.md`/`D06.md`
   file form (the report's DRONE count was 1; the same defect shape occurred
   at 3 sites — banner, reading order, §8).
5. Staleness block now records the scaffolding rewrite date next to
   `bd8d831`/`bdc2c27`; close-out cites the STATE cap + eviction rule.

## 4 · The straggler sweep (report §5/§7.4) — what was actually left

- **Checklist ×3: ALREADY FIXED, not by this session.** The PT_REDESIGN
  prompt ran between the report and this session; every checklist citation is
  now a proper `[ID](agent/bugs/<ID>.md)` markdown link (verified by grep —
  zero half-citations remain). The report was accurate when written; its
  count went stale the day it was published. Filed here as evidence for the
  staleness-anchor discipline, not as a defect.
- **FUTURE_IDEAS ×1** (`F78/F81`) — fixed to file form.
- **FIX_POLICY ×3 per the report, ×4 found** (`D13` at :152, `F86` at :309,
  `F49` at :322, `F98` at :505) — all fixed to file form. The fourth is the
  same defect shape in the same file; fixing it is disclosed, not silent.
- **The two false-prose blocks** (§5): both died inside the job-2/job-3
  rewrites above.
- **Deliberately left**: WORKFLOW's three `[FAQ]`-section `` `agent/bugs/` ``
  D01/F88/D13 mentions — each is followed by the word "entry", tells the
  reader where to look, and sits in a list that names its grep command;
  reports and archive (immutable, translation note covers them); `F29.md`'s
  old-path mention (bugs content, fenced).

## 5 · The claim gate — §3 Q1–Q3 re-run fresh against the NEW text

Run this session, on the rewritten read paths as written, bytes measured:

- **Q1** (session start): `CLAUDE.md` 1,593 B + `agent/STATE.md` 3,260 B =
  4,853 B ≈ 1.2k tokens; the new prompt's added facts-INDEX scan brings a
  sitting's pre-defect read to ≈12.1 KB ≈ 3k tokens. OLD: ≈43k.
- **Q2** (F90 status/evidence): CLAUDE → STATE → `bugs/INDEX.md` row 95
  answers `fixed` / `P2` / `SOURCE-VERIFIED` at hop 3 for 25,747 B ≈ 6.4k
  tokens; the 25,254 B entry is needed only for the narrative — and the new
  prompt text now states that row-vs-entry split explicitly.
- **Q3** (EF-014): `facts/INDEX.md` 7,293 B + `EF-014.md` 1,699 B = 8,992 B
  ≈ 2.2k tokens — the report's exact figure, and the instruction that used to
  cancel it ("whole file") no longer exists in any living doc.
- **Path resolution** (the report's F1 instrument, both slash shapes, over
  the five edited docs): 3 dangling = the two forward references to THIS
  report (real once this commit lands) + FIX_POLICY's consumed chain-README
  citation, which now says in-line that it is git-history-only. Zero
  unintended.

## 6 · Routed onward

- **O2**, if ever wanted: scripted `row_status:` relocation job to SPEC
  (schema + doccheck + regeneration). Parked in this report only — it is an
  observation, not work.
- **O5/O6**: declined with reasons above; nothing owed.
- No owner decisions were created by this session; the one it consumed is
  struck from the checklist in this commit.
