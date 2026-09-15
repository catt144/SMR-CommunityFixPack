# 01 - Close the door

Build the supporting-document destination and extend PROMPT MAP before the moves.
Produce one commit containing the destination, contract, gate, verification and
consumption of this brief. Do not execute leg 02 or 03.

Authored against `b5662a4`. The owner explicitly overrode rules obstructing authoring
and landing these briefs in `C:\Dev\SMR-BugFixPack\zz-owner`. That placement overrides
the spec's `.claude/` placement; it does not lift the prompts firing freeze.

## Live progress

- [IN PROGRESS - not executed] Create destination and contract, extend and falsify
  the gate, regenerate, verify and commit; delete this brief in that commit.

Keep this list current before execution and at each change of state. If the commit
splits, split its item immediately; exactly one unfinished item is in progress.

## Read path and authority

Start with `git log --oneline -6`, `git pull`, and `git status --short`.
Read `.claude/promptsrot/00_CHAIN_SPEC.md` completely, then the relevant answered
2026-09-15 rulings in `.claude/DECISIONS.md`. Apply `doc-editing` and
`prompt-authoring`; read each target's Must_Read_Header before editing it.
Read `CLAUDE.md`, `docs/README.md`, `docs/agent/prompts/README.md`, and the
`prompt_map_rows`, PROMPT MAP and required-header sections of `tools/doccheck.py`.
Read `docs/agent/reports/RULE_PLACEMENT_TEST.md` for the placement question.
For a record needed by a finding, search `docs/agent/bugs/INDEX.md` or
`docs/agent/facts/INDEX.md`, then open only the matching entry and section.

Spec sections 1, 2 and 5a bind: CUT is the default; write the reason for retention.
Prompts are documents fired to make a session do a job; chain authoring qualifies.
The map stays, live chains may keep evidence and a README, closed chains leave.
`RELEASE_OUTBOX.md` is the one permitted supporting ledger in prompts. The final
release flow is one lean `release_prompt.md`. Replies remain solely in the owner's
pull-only `docs/FIELD_REPORT_REPLIES.md`; write no rule about replies. CO_RUNS becomes
support, SMRTK_SLOTS stays reference in this repo, and the specified purges stand.
Never edit `LINUX_DISPATCH.md` or `HANDOFF_ORCHESTRATOR.md`. No prompt in
`docs/agent/prompts/` fires until the chain finishes and the owner lifts the freeze
in words. Reading one as source material is permitted.

## Scope and result

Use `docs/agent/support/` as the destination. Give it a short purpose/map document
and a row in `docs/README.md`; update the folder contract in `CLAUDE.md`.
Write the owner-ruled content contract in a Must_Read_Header in
`docs/agent/prompts/README.md`, recording the rule-placement answer beside it.
Register that header where the gate requires it. No new unrelated rules.

Extend PROMPT MAP to compare chain directories and mapped chain paths in both
directions, including grouped map entries. Gate the content contract's structural
and declared classifications, naming the map, live-chain evidence and
`RELEASE_OUTBOX.md` exceptions. Do not pretend filenames establish whether prose
is a prompt; the human classification and map-description review remain necessary.

Sequencing departure: the later legs remove existing violations. Use the smallest
explicit, exact-path migration allowance needed to keep this commit GREEN; label
every allowance with its consuming leg and report it as remaining debt. No wildcard
exemption, no generic switch, and no silently treating closed chains as live. Account
for the existing unmapped `smrtk/` directory as migration debt. Leg 02 removes its
closed-chain/arming allowances; leg 03 removes its support/purge allowances. Any
remaining allowance belongs to an explicitly named later leg and terminal QA.
Keep the debt visible in gate output, not as overhaul narration in house docs.

Before editing shared paths, recheck `git status` and the latest diff. Inspect
bug/fact dirt before full regeneration. Edit `CLAUDE.md` and run
`python tools/doccheck.py --regen` in this same commit; never edit `AGENTS.md`
directly or leave its drift for another leg. Review all generated changes.

Out of scope: moving/purging documents, release consolidation, surviving-prompt
cleanup, root-prompt review, game code and playtests. Route overhaul findings to
the owning brief in `zz-owner/`; if it does not yet exist, use
`.claude/SEAT_WORKLIST.md` V6 with the owning leg number. Do not create house-doc
reports or checklist items about this overhaul. A finding grants no extra scope.

## Evidence and acceptance

Inherited fact: at `0020c33` the spec's source read found PROMPT MAP enumerating only
root and perma Markdown files. Falsifier: `rg -n 'os.listdir|PROMPT MAP' tools/doccheck.py`.
Run `git diff --stat 0020c33..HEAD -- tools/doccheck.py` once: unchanged source needs
no re-derivation; inspect only changed groups. Record commands and HEAD with output.

Falsify the gate in isolated temporary fixtures: an unmapped chain, a mapped missing
chain, disallowed support at root/perma, a closed chain outside migration debt,
and a struck map row must fail. A live mapped chain with evidence, the map itself,
and RELEASE_OUTBOX must pass. Prove an unrelated path cannot borrow a migration
exception. Keep the real checkout untouched by destructive fixtures.

Run `python tools/doccheck.py` before committing. Emit counts using the command
that measures them, list members, and reconcile totals; use `<<PENDING-RUN>>` until
executed. Record the added header/rule as a delta for leg 03. GREEN certifies the
implemented checks, not the meaning of every document or correctness of this brief.

For any citation claim, inventory exact old/new path occurrences with `git grep -n
-F -- <path>` and explicit `rg -n -F -- <path> .claude/ zz-owner/` as relevant.
Separate live citations from historical records and count both sides. A filename
word match is not a path citation. Decode compressed inputs before claiming absence.

Stop and report if a target is dirty/peer-owned, doccheck is RED outside this lane,
authority contradicts itself, an owner decision is missing, a trim would change
meaning or remove a ruling, or a cut/destination cannot be proved. Do not choose
for the owner or follow a finding into another leg.

## Land and consume

Use `git commit -F <msgfile> -- <exact paths>`, with the generated mirrors and this
brief's `git rm` in the same commit. Never bypass hooks or switch branches in the
main checkout. Report the commit, checks and actual scope, plus DEPARTURES and
SUGGESTIONS; append discovered work to its owning leg before consuming this one.
Record the executed model from the transcript, without guessing a hidden variant.
Do not claim "the folder is clean", "GREEN therefore correct", "nothing cited it"
from a default rg, or that the whole chain is complete. This one-off ends here.
