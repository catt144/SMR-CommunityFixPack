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

### From hubset 01, 2026-09-24 — build and drift inbox

- Branch/worktree: `hubset` at `795aefa`, `B:\Dev\SMR\SMR-BugFixPack-hubset`. Main evidence
  landed through `6227f2f`. The four built members and subagent reports are in
  [the fan-out plan](../../reports/hubset/agents/PLAN_2026-09-24.md); P3 has its own
  [dated build record](../../reports/hubset/P3_BUILD_2026-09-24.md).
- P3 adds only two `SRC:` pins to `Fix_VacuumWalks`; archived 1.1.1.405907 bodycheck returned
  6 OK for the module. This verifies shape, not wrapper composition.
- C42's `Fix_PassageStaleHolder` mitigates teardown kicks by filtering invalid or mismatched
  passage-element members before the native Holder method. The raw `unit.holder = nil` in
  `TraverseTunnel` still creates stale entries. The desk held 11/11, including fix-absent harm;
  C42 stays `filed` pending play and an audit of whether the narrower mitigation suffices.
  Inspect its interaction with C116 and C117 when they touch traversal.
- F127's repaired `Fix_ArrivalDeaths` C83 branch cancels the rejected booking before reserving
  in a new destination. The archived desk held 12/12; the existing C83 desk held 12/12.
  F127 is `fixed` pending attended play. **Drift instance:** the first build only called
  `new_dome:ReserveResidence`, which left an orphan in a full Naturalist Habitat because its
  method cancels only when a slot is free. The final desk includes full-habitat and old-shape
  mutant controls. Audit the final code and those controls, not the initial passing matrix.
- C111 wraps only the synchronous UI getter. Proposed exact own-home wording for owner
  approval: `Returning to Dome: <h SelectEmigrationDome InfopanelSelect><em><EmigrationDomeDisplayName></em></h>`.
  Real relocations retain shipped T ID 4333 and the destination link. Checklist ck216 owns
  approval; `cand` remains until that word and attended play. Desk 8 pass and fix-removed
  own-home control fails; retail rendering and real save/reload are untested. Flag the wording
  as unapproved if ck216 is still open at audit time.
- Branch and main doccheck were GREEN after these builds. Link 07 still owes all in-game
  verification; no desk result is a play verdict. No load-order change or release surface was
  made. The ignored `local/` evidence folders had to be created empty in the new worktree for
  its inherited `local/README.md` gate; main's evidence stayed in main's `local/`.
