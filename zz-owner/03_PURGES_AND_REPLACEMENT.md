# 03 - Purges, and one replacement

Purge the ruled-dead prompts, replace GENERAL_USE_PROMPT with a minimal idle
orientation, and move CO_RUNS/SMRTK_SLOTS into support. Execute after leg 02 lands.
Produce the commits below and execute no later leg.

Authored against `b5662a4`. The owner overrides obstructing authoring/placement
rules for these briefs in `C:\Dev\SMR-BugFixPack\zz-owner`; the prompts firing
freeze and substantive owner rulings remain in force.

## Live progress

- [IN PROGRESS - not executed] Purge COMBINED_SITTING, DRONE_PROJECT_PROMPT and
  DISPATCH; reconcile required headers, map and live consumers; verify and commit.
- [PENDING - waits for purge commit] Purge and replace GENERAL_USE_PROMPT in one
  commit; carry the cheap triage method into the source bug-library skill,
  regenerate its mirror, verify and commit.
- [PENDING - waits for replacement commit] Move SMRTK_SLOTS verbatim and move/trim
  CO_RUNS into support; reconcile live pointers, verify and commit; consume this brief.

Update at each commit and split items if a commit splits. Exactly one unfinished
item is in progress and its text states actual state, not just a phase name.

## Read path and authority

Start with `git log --oneline -6`, `git pull`, `git status --short`. Read
`.claude/promptsrot/00_CHAIN_SPEC.md` completely and the relevant answered
2026-09-15 rulings in `.claude/DECISIONS.md`. Apply `doc-editing`, `prompt-authoring`
and `smr-bug-library` when editing the triage method. Read target Must_Read_Headers.
Read `docs/README.md`, `docs/agent/prompts/README.md`, the support map created by
leg 01, and required-header/PROMPT MAP sections of `tools/doccheck.py`.
Read these named source files under `docs/agent/prompts/perma/`:
`COMBINED_SITTING.md`, `DRONE_PROJECT_PROMPT.md`, `DISPATCH.md`, `CO_RUNS.md` and
`SMRTK_SLOTS.md`. For `GENERAL_USE_PROMPT.md`, inspect only the Default mode method
needed below; the owner explicitly rejected auditing/rerouting its old body.
Read `.claude/skills/smr-bug-library/SKILL.md`, the editable source, before changing
it; `.agents/skills/smr-bug-library/SKILL.md` is a generated mirror.
Search `docs/agent/bugs/INDEX.md` or `docs/agent/facts/INDEX.md` for any additional
record, then open the matching section only. STATE is read only if a live path
search identifies a citation needing repair.

Fixed: prompts holds prompts, its map stays, live chains may hold evidence and
their README, closed chains leave. RELEASE_OUTBOX is the one ledger exception;
one lean release_prompt is later work. Replies have only the owner's pull-only
`docs/FIELD_REPORT_REPLIES.md`; write no rule about them. Purges and support moves
below are owner decisions. CUT is the default; retention needs a written reason
using the placement question in `docs/agent/reports/RULE_PLACEMENT_TEST.md`.
Never edit `LINUX_DISPATCH.md` or `HANDOFF_ORCHESTRATOR.md`, even to fix their
citations. No prompt in `docs/agent/prompts/` fires until the chain finishes and
the owner lifts the freeze in words. Do not test the replacement by firing it.

## Commit 1 - Purges

Delete `COMBINED_SITTING.md`, `DRONE_PROJECT_PROMPT.md`, `DISPATCH.md` and their map
rows. Remove COMBINED_SITTING from doccheck's required-header list in this same
commit, along with applicable migration allowances. Repair live entry points,
including the edited `CLAUDE.md` source if it still points to DISPATCH; regenerate
AGENTS in that commit. Do not recreate DISPATCH's task router elsewhere.

The spec inherited a corpus of 8 blocks/31 rules at `0020c33`; deleting
COMBINED_SITTING removes one block and one rule (historically 7/30 afterward).
These are inherited measurements, not today's acceptance totals: leg 01 adds a
contract header. Run the current corpus command below, enumerate actual members,
and reconcile the removal against that baseline and any intervening additions.
Do not force the corpus to 30 by deleting an unrelated rule.

## Commit 2 - Purge and replace, atomically

Delete the old GENERAL_USE_PROMPT body and create a fresh file at the same path
in this commit. Do not evolve it section by section. Target these two lines:

> Use the project and rules already supplied by CLAUDE.md or AGENTS.md; nothing is expected yet.
> Wait for my instructions without checking current work, surveying, planning, proposing, or starting a default task.

The owner pastes it, walks away and returns later with a task. The session must
be oriented and idle during that gap. No status read, git/doccheck survey, plan,
proposal or task-shaped default. Do not restate the loaded project rules.
Update its map description to match this actual purpose.

Carry only the cheap ours-or-vanilla keyword search method into the source
smr-bug-library skill, as required by spec section 5b. Do not preserve the
"never open Code top-to-bottom" wish. Keep it one method line; identify the search
scope and avoid treating an empty literal keyword search as proof against aliases
or indirect effects. Regenerate the skill mirror in the same commit. If the
owner explicitly prefers losing this method, honor that and report the departure.

## Commit 3 - Support

Move SMRTK_SLOTS to `docs/agent/support/SMRTK_SLOTS.md` verbatim; it stays in this
repo, never the TestKit repo. Move CO_RUNS to `docs/agent/support/CO_RUNS.md` and
give it the authorized alignment pass/content trim to what it needs to function.
Move and remove the source in the same commit. Inspect actual destination passages
beside source diffs; update support map and live consumers and remove prompt rows
and their gate migration allowances.

CO_RUNS carries verbatim owner rulings (including D5/adoption) and material rescued
from the now-deleted PLAYTEST_HELP at `c91310f`. Open that commit's CO_RUNS diff:
`git show c91310f -- docs/agent/prompts/perma/CO_RUNS.md`. Inventory its obligations
and check their actual destination passages after the trim. Wordiness is trimmable;
owner rulings and their conditions are not. Keep only justified operational prose.

## Evidence, scope and stops

For inherited claims use `git diff --stat <baseline>..HEAD -- <source paths>`:
unchanged groups need no re-derivation; recheck changed groups once. The corpus
falsifier is `python tools/doccheck.py` (RULES HEADERS output), paired with the
required-header members and their Rule lines. The rescue falsifier is the
`git show c91310f` command above; measure the diff if reporting its byte count.
Every count must carry command/filter/HEAD and reconciled members. Before a
measurement runs, write `<<PENDING-RUN>>`, not an inherited figure as current fact.

Inventory exact old/new path citations before/after with `git grep -n -F --
<path>` and explicit `rg -n -F -- <path> .claude/ zz-owner/` for local material.
Inspect relative forms as needed. Count both removed/source and retained/destination
sides; a word hit is not a path citation. Decode compressed inputs before absence
claims. Sweep live docs only: reports, bugs, facts, archive and dated records keep
old paths. Record exempt handoff citations for its next handoff session; no leg
repairs them. Check replacement disposition by reading its text and map, and check
SMRTK_SLOTS preservation by before/after hashes. These checks do not prove a future
session's behavior.

Out of scope: release consolidation, RELEASE_OUTBOX trimming, SITE_AUDIT, remaining
perma cleanup, root/live-chain review, game code and playtests. Append findings to
the owning brief in `zz-owner/`; if absent, use `.claude/SEAT_WORKLIST.md` V6 with
the owning leg number. Keep overhaul measurements/rulings internal rather than
adding house-doc reports/checklist items. Finding a problem grants no repair scope.

Stop and report if a target is dirty or peer-owned, doccheck is RED outside this
lane, authority conflicts, a decision is missing, a trim changes meaning or loses
an owner ruling, a cut cannot be proved, or a destination passage is unopened.
Do not carry out an owner decision on your own judgment.

Before every write, recheck status and shared-path diff. Before regeneration,
inspect peer bug/fact dirt and review generated changes afterward. Run
`python tools/doccheck.py` before every commit; use exact paths with
`git commit -F <msgfile> -- <paths>`. Never bypass hooks or change branch in the
main checkout. Append findings to the proper leg and `git rm` this brief in its
final result commit.

Report actual cuts, moves, preserved obligations, commits, evidence, DEPARTURES
and SUGGESTIONS; record the executed model from the transcript without guessing.
Do not claim "the folder is clean", "GREEN therefore correct", or "nothing cited
it" from default rg. Do not claim the whole chain is complete. This one-off ends
after these commits.
