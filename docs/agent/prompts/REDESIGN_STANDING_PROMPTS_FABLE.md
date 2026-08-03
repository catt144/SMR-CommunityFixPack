# One-off — Standing-prompts redesign (FABLE; owner-triggered)

**Why Fable:** this is the compounding point — a standing prompt is a spec for
every future session that pastes it, so an error here multiplies (CHAIN_METHOD
§2.10). Authored 2026-08-03 by the chain-12 session; the owner fires it by
pasting this file into a Fable session.

Staleness first: `git log --oneline -10` + `git pull`. WORKFLOW elements 1–7
bind. The pre-commit hook is armed; doccheck must stay green.

## Read, in order (your whole picture — the read path, declared)

1. `docs/agent/reports/DOCS_RESTRUCTURE_REPORT.md` — WHOLE FILE. It was
   written for you; §6 is your inventory, O1–O7 are your open questions.
2. `CLAUDE.md` + `docs/agent/STATE.md` (what every future session auto-sees).
3. The two subjects: `docs/agent/prompts/FABLE_NEXT_PROMPT.md`,
   `docs/agent/prompts/DRONE_PROJECT_PROMPT.md`.
4. `docs/agent/WORKFLOW.md` — elements 1–7 and the adopted-rules block.
5. `docs/agent/reports/CHAIN_METHOD.md` §2–4 (the method your output must fit).

## Jobs

1. **Decide O1–O7, each explicitly** (report §6) — adopt / decline / defer,
   one recorded line of reasoning each. Two have teeth beyond the prompts:
   O1 (a read-path element 8 for ALL briefs — a WORKFLOW change, adopt it
   there if taken) and O6 (EF topical ids — the window closes at the first
   citation; if adopted, the rename is a scripted job to SPEC, not to do here).
2. **Rewrite `FABLE_NEXT_PROMPT.md`** against the new tree. Musts from the
   report: kill the "`docs/agent/facts/` — whole file" instruction (§3 Q3 —
   the most expensive stale sentence in the repo); route readers through the
   two INDEX.md files; give the STATE.md close-out step an eviction rule
   (O7 — the cap is enforced, the eviction is folklore); keep the prompt's
   standing session rules (probe gate, account-state, §4a, PT-52 freeze)
   intact in substance.
3. **Rewrite `DRONE_PROJECT_PROMPT.md`'s doc-facing scaffolding**: the stale
   `DOCS LAYOUT` block, the read path, the `prompts/project/README.md`
   references (decide: retire the references or write that README — report
   §7.1). ⛔ **Scope fence: the drone-track CONTENT is untouchable** — D06
   design decisions, freezes, research state are the drone chain's, not yours.
4. **Sweep the report's deliberately-unfixed content stragglers** (§5): the
   ~8 `agent/bugs/ F97`-style half-citations (checklist ×3, FUTURE_IDEAS,
   FIX_POLICY ×3, DRONE ×1) and the two false-prose blocks it names.
5. **Write `docs/agent/reports/STANDING_PROMPTS_REDESIGN.md`** — the decision
   record (O1–O7 verdicts + reasoning), what changed in each prompt and why,
   and anything routed onward. Reports are immutable once written; this is
   yours, write it complete.

## Fence / stops / claims

Out of scope: `agent/bugs/`, `agent/facts/` content; the checklist beyond job
4's citations; `archive/`; other reports; CHAIN_METHOD. Stop and ask: any O
whose adoption would change the CHAIN mechanics themselves (that is owner
territory). May not claim: a rewrite is "aligned with the new tree" without
having run the report's §3 Q1–Q3 read-paths yourself, fresh, as written in
your new text. **Checkpoint: show the owner a summary of both rewrites before
the final commit** — standing prompts are the owner's firing interface.

## Close-out

Strike the checklist's "Decisions waiting on you" line for this task; update
STATE.md's pointer; delete this file; commit (`-F` convention, doccheck
output rides the hook); push.
