# hubset 99: adversarial audit, then the merge on the owner's go

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first. Fire only
when this file and the README are the only files left in `docs/agent/prompts/hubset/`. Run in fresh
context, on a different model or vendor from the one that built the links (owner routing: the builds
on Codex, this audit on Fable).

## Authority and outcome

Your job is to disbelieve the chain. Trust no link's summary, including its outbox and the entries'
build sections; check each against primary evidence (the branch diff, the archived `1.1.1.405907`
source, the desk harnesses re-run, the archived sitting logs). End state: a report at
`docs/agent/reports/HUBSET_AUDIT_<date>.md` with one verdict for the set: **SHIP**, **SHIP WITH
CHANGES** (each change named, small, and not needing another sitting) or **NO SHIP** (with what
would make it shippable). Then the close-out below. Open a live todo list before the first write.

## What to audit

- **Every member against its entry.** For C114, C115, C116, C117, C42, C111, F127 and P3: does the
  module fix the defect the entry states, by the shape and guards the entry and the resweep require,
  and nothing wider? Re-run each desk harness on the branch, and confirm its controls fail with the
  fix removed.
- **FIX_POLICY.** Technique ranking (§1), `Require` checks, MANIFEST pins and stand-down (§2), save and
  blocking-frame disposition (§3a), localisation (§6). Run `tools/bodycheck.py` on the branch.
- **Interactions.** C42, C116 and C117 all touch passage traversal, and C114, C115 and C116 all touch
  the rescue chain. Look for two members wrapping the same target in a noncommuting order, or one
  assuming state another changes.
- **The sitting.** Sample 07's verdicts against its archived logs. Every `tested-attended` needs the
  owner's observation in the log.
- **Drift.** Every instance in your inbox: was it routed or silently fixed?
- **The rulings.** Nothing from the set reached `main`'s `Code/`, `metadata.lua` or `items.lua` before
  this link. No load-order change is in the branch. C111's wording carries the owner's approval, or is
  flagged as still unapproved.
- **Owed work.** Anything a link said it would do and did not.

## Close-out

- **NO SHIP:** commit the report, route the verdict and its remedies to the owner, and leave the branch
  and worktree in place. Archive this README and remove the chain folder only when the owner closes the
  effort.
- **SHIP or SHIP WITH CHANGES:** give the owner the verdict and wait for their go in words. On the go:
  merge `hubset` into `main` (`git merge --no-ff hubset`, resolving `metadata.lua` and `items.lua`
  against anything `main` gained); run doccheck GREEN; append one filled `### Pending` entry per
  player-facing member to `docs/agent/prompts/perma/RELEASE_OUTBOX.md`, per its rules (P3 has no player
  surface); set each entry's status from its evidence; remove the worktree
  (`git worktree remove ../SMR-BugFixPack-hubset`) and delete the branch after the merge commit lands.
  The upload itself is the owner's, through `release_prompt.md`.
- Then the README's terminal lifecycle: archive it, remove the `hubset/` map row, `git rm` this file,
  and leave no live chain folder. End the report with the next chain's kickoff line, or say none is
  queued. The load-order decision the owner deferred until after the fixes is the natural next item;
  name it.

## Notes from upstream
