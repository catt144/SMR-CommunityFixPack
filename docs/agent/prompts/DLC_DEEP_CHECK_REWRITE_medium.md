# Rewrite DLC_DEEP_CHECK to the current brief style

Owner instruction 2026-09-17: `docs/agent/prompts/DLC_DEEP_CHECK.md` (292 lines, 17.7 KB, about 50
⛔/⭐/⚠️ marks at authoring) is over-railed and predates this month's rules. Rewrite it. Its job does
not change and it is not fired by this session.

## Start

`git log --oneline -5; git pull; git status -sb`. Authored at `acb3227`; an empty
`git diff --stat acb3227..HEAD -- docs/agent/prompts/DLC_DEEP_CHECK.md docs/agent/support/CHAIN_METHOD.md
.claude/skills/prompt-authoring/SKILL.md docs/agent/prompts/README.md` means these facts hold.
Invoke `doc-editing` before editing. Keep a live work list.

## The job it must still do

Author a chain under `docs/agent/prompts/dlccheck/` that deep-checks the DLC's own new code and the
base-game changes made to accommodate it, and consume itself without firing a link. Keep, in the
rewrite: the deep-not-census bound (the owner rejected an exhaustive per-row census); sizing the
chain and stating its budget from a re-emitted inventory, never the 2026-09-08 figures; the thesis
that DLC content is under-tested and nobody checked what it does to an existing player's game; the
overlap with the vanilla hunt, whose terminal link must have run first and whose base-game seam
result this inherits rather than redoes; what a source read cannot settle and the play leg that can;
the finding contract; the bindings; and the rule that a fan-out which cannot be falsified is not
evidence.

## Apply the current rules

- `prompt-authoring`: authority first, end state, judgement handed over, live work list, staleness
  sha, facts only where they would be re-derived, two-line scope, at most three stops, do-not-claim,
  lifecycle, skills named not restated.
- Investigation links get the evidence, the question and the hard rules, then free rein: no read
  path, no step order, no prescribed hypothesis, no fence on what to open or run. Rails belong only
  on the job-shaped links (inventory, records, the terminal audit).
- No model or vendor names anywhere, in the brief or in the link names it prescribes. Link filenames
  carry `_low`, `_medium`, `_high`, or `_fanout_level_<x>` for the reading fan-out.
- Chain mechanics come from `docs/agent/support/CHAIN_METHOD.md`: cite it, do not restate it. Cut
  what it already covers (folder committed before firing, manifest, self-consumption, subagent model
  choice, tool-neutral fan-out briefs, committed agent reports, terminal QA independence).
- Owner asks go to `docs/PLAYTEST_CHECKLIST.md` in its item format, never only into the brief.
- Voice: imperative, condition → action → the one reason; no emphasis marks, no dates, no quotes, no
  restated rationale. Ids instead of re-explanations.

## Also

- Re-check every path and citation the brief carries; several docs moved this month. A dead citation
  is repointed or cut, not carried.
- Keep the brief's own `prompts/README.md` row true to the rewritten purpose; update it if it drifts.
- The rewritten file keeps the name `DLC_DEEP_CHECK.md` and its root one-off lifecycle.

## Scope

In: that brief, its README row, and citations inside it. Out: authoring or firing the dlccheck chain,
the vanilla hunt, game code, any other prompt. Findings elsewhere go in the report.

## Stop

A file you must write is dirty with a peer's change; doccheck is RED outside this job and was before
you started; or the rewrite would drop an owner ruling you cannot re-home.

## Done

`python tools/doccheck.py` GREEN, committed with a pathspec and pushed, this file `git rm`'d with its
row in the same commit. Report: lines and bytes before and after, what was cut, what moved to the
chain method or the checklist, dead citations found, and calls made without asking.

Do not claim the dlccheck chain is authored or that the DLC has been checked. This job rewrites a
brief.
