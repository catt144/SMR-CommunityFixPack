# 07 - Terminal adversarial QA

Audit the prompts overhaul backward from its surviving tree, repair proved
in-scope defects, and consume the last overhaul brief. This must run in fresh
context by a vendor that did not execute any leg it judges. It hunts
over-retention before ordinary mistakes.

Authored against `9ae0d50`. Do not run until legs 02 through 06 are committed and
consumed and this is the last overhaul brief file in `zz-owner/`. The firing
freeze remains in force throughout; only the owner can lift it in words.

## Inbox

Earlier legs append here before consuming themselves. Every correction, departure,
unresolved citation, retained-passage reason and caught drift belongs here even
if it was fixed in place. At authoring time the inbox is empty.

## Live progress

- [IN PROGRESS - not executed] Prove the execution boundary: fresh context,
  cross-vendor eligibility, complete leg commit manifest, no unconsumed earlier
  brief, clean target paths and a frozen before-inventory.
- [PENDING] Audit survivors for over-retention first, backward from prompts and
  support to the reasons written for keeping each passage; repair or stop.
- [PENDING] Audit cuts, moves, owner rulings, live citations, generated sources,
  maps and corpus reconciliation; repair or stop.
- [PENDING] Run terminal gates, prove the brief-file emptying condition, commit
  final repairs if any, then consume this brief in the final commit.

Maintain one item per commit-and-verify unit with exactly one unfinished item in
progress. Add repair items the moment findings split. An audit-only check does
not need an empty commit; put its stable evidence in the progress text and final
report.

## Entry gate and read path

Start with `git log --oneline -12`, `git pull`, `git status --short`. Record the
vendor/model that executed every leg from commit/transcript evidence available to
the owner. If this session's vendor executed any judged leg, stop before reading
its reasoning and ask for a different vendor. Fresh context means no inherited
working analysis from an executing leg; the briefs, commits and tree are the
evidence.

Verify legs 01 through 06 by commit and diff, beginning with leg 01 commit
`9ae0d50`; never attribute work by the shared git author. Read
`.claude/promptsrot/00_CHAIN_SPEC.md` completely, the answered 2026-09-15 rulings
in `.claude/DECISIONS.md`, every surviving brief in this Inbox, and the final
diffs/commit messages of all six legs. Apply `doc-editing` and `prompt-authoring`.
Read target Must_Read_Headers.

Read `docs/README.md`, `docs/agent/prompts/README.md`,
`docs/agent/support/README.md`, `CLAUDE.md`, the required-header/PROMPT MAP gates
and their self-tests in `tools/`. Inventory every file under `prompts/` and
`support/` before selecting bodies. Read every surviving prompt completely for
purpose, scope and lifecycle; read each support document needed to verify its
consumer pointer. Use bug/fact INDEX lookups and named entry sections rather than
whole-folder reads. Read STATE only for pointers changed by the overhaul or when
status is itself under audit.

Fixed: prompts contains only mapped prompts, mapped live-chain evidence/README,
and the owner-exempt outbox ledger. The map stays. Closed chains leave. There is
one lean `release_prompt.md`. Replies have one pull-only source with owner
transport and no newly created rule. The ruled purges/moves stand. CUT is the
default. `LINUX_DISPATCH.md` and `HANDOFF_ORCHESTRATOR.md` were never edited, even
to repair their deliberately loud dead citations. No QA finding lifts the firing
freeze.

## Pass 1 - Over-retention first

Begin with the exact question from the spec:

> What did this chain KEEP that should have gone, and what reason was written for keeping it?

Work backward from every surviving prompt, support document, map row and new
pointer. For each retained section—not merely each file—record its job, consumer,
retention reason and the mechanism that prevents failure without reader memory.
Challenge vague reasons such as useful, safer, historical, context, orientation,
owner-facing or might need later. A file having been moved to support is not
evidence that all its prose belongs there.

Apply the placement table strictly: structure is deleted; a guard earns at most
a pointer; a violated wish is not a rule; a one-job obligation belongs in that
job; an existing fact is not duplicated. Confirm owner-retained prompts retain
their authority and condition, but distinguish file retention from passage
retention. Check especially the new release support, outbox history/staging,
trimmed CO_RUNS, root prompt bodies and live-chain manifests.

If over-retention is proved and its removal needs no owner decision, add a repair
unit and remove it with all dependent pointers. If meaning or authority is
uncertain, stop and name the exact decision; do not retain by default. Append
each finding and disposition to this Inbox before changing it so silently fixed
drift is not lost during the audit.

## Pass 2 - Ordinary correctness, backward

Audit the end state against the commits, not the execution summaries:

- every purge has no surviving live entry point or tombstone;
- every verbatim move has matching before/after file manifests, lengths and
  SHA-256 hashes except explicitly declared edits;
- every trim has a source-passage disposition and an inspected destination that
  preserves live obligations and owner conditions;
- every generated output was changed through its source and regenerates cleanly;
- every prompt-map description matches the actual job and lifecycle;
- every support document has a real prompt consumer and is not independently
  fireable;
- every one-off/chain has a consumption condition and every closed chain left;
- every owner ruling remains verbatim where the ruling required verbatim text;
- reports, bugs, facts, archive and dated records were not rewritten to hide old
  paths;
- the release prompt spans the upload pause/resume, contains no standing reply
  step, and the site read route remains usable without becoming a prompt;
- exempt handoff/Linux files are byte-identical to their pre-overhaul versions.

Search each removed old path and meaningful relative form with
`git grep -n -F -- <path>` plus explicit `rg -n -F -- <path> .claude/ zz-owner/`.
Count both the removed/source and retained/destination sides, classify
live/historical/exempt hits, and make the live unresolved set explicit. Default
`rg` cannot prove absence because the archive is hidden. Decode compressed
inputs before an absence claim.

Reconcile the rules corpus from its members. Run the emitting gate; list required
blocks and their canonical `Rule:` lines; explain every net change from the
pre-overhaul baseline through the final tree. Do the same for prompt-map classes
and disk members. A current count is emitted, never inherited or hand-typed.

## Repair commits and final commit

Do not write an audit report into house docs. For each proved, in-scope defect,
make the smallest coherent repair commit after adding it to the live progress
list. Re-run the focused falsifier and `python tools/doccheck.py` before that
commit. A move/cut and its map/citation updates are atomic. Use
`git commit -F <msgfile> -- <exact paths>`, never `-a`, never bypass hooks and
never switch the main checkout's branch.

Anything requiring an owner decision, game-code change, playtest, firing a
prompt or editing an exempt file is a stop. Do not convert terminal QA into a new
overhaul phase. Suggestions that are not defects go in the final SUGGESTIONS
section and nowhere in the tree.

The final commit has one purpose: consume this brief after all acceptance checks
pass. Immediately before it:

1. `git status --short` shows no foreign target work;
2. `git ls-files zz-owner` names only this brief, and
   `Get-ChildItem -Force zz-owner -File` names only this brief;
3. the prompt/support inventory reconciles with the two maps;
4. focused old-path searches have no unresolved live hit except the declared
   exempt handoff citations;
5. the corpus and all generated mirrors reproduce;
6. `python tools/doccheck.py` is GREEN.

Then `git rm zz-owner/07_TERMINAL_QA.md` and commit that deletion with any final
Inbox removal. Afterward, both file-list commands above must emit no overhaul
brief file. Ignored empty memory directories are not chain briefs and are not a
licence to delete owner data. The empty brief queue is the chain's done-condition;
the owner still has to lift the firing freeze separately.

## Derived facts and falsifiers

| fact | measured | falsifier |
|---|---|---|
| leg 01 landed at `9ae0d50`; legs 02-06 are later work this audit must identify by commit/diff | authoring log at `9ae0d50` | `git log --oneline --reverse 9ae0d50^..HEAD` plus each candidate `git show --stat` |
| the pre-overhaul contract measured 9 required rule blocks and 32 canonical rules after leg 01 | `python tools/doccheck.py --emit-counts` at `9ae0d50` | rerun the current gate and enumerate every member; do not force the old total |
| the map at `9ae0d50` measured 14 perma, 6 root one-offs and 4 chain rows, with migration debt for legs 02/03 | PROMPT MAP output at `9ae0d50` | current PROMPT MAP output plus disk enumeration |

An empty `git diff --stat <derived-sha>..HEAD -- <paths>` clears only that
specified fact group. Any moved group is re-derived once against the final tree.
Every reported count includes command, filter, HEAD and reconciled members.

## Stops and permitted claims

Stop and report if the vendor-independence gate fails, an earlier brief remains,
authority conflicts, a decision is missing, a target is dirty/peer-owned, RED is
outside the repair lane, a cut or move cannot be proved, a destination passage
was not opened, an owner ruling changed meaning, or repair would require firing
a prompt. A stop leaves this brief in place.

Final report: commits audited and repair commits; exact over-retention findings
first; cuts/moves and surviving historical/exempt citations; corpus/map evidence;
DEPARTURES; SUGGESTIONS; and executed model/vendor from transcript evidence.
The narrow success statement is: legs 01-07 landed, terminal checks passed, and
no overhaul brief file remains in `zz-owner/`. Do not claim prompts were fired,
the owner lifted the freeze, a release/playtest passed, or GREEN proves semantic
correctness.
