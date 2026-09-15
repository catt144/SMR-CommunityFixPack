# 06 - Root one-offs and live chain folders

Audit the six root prompts and the live `fixtoggles/`, `smrcf-modbrowser/` and
`smrcf-verify/` folders against the prompt-content contract. This is the half the
overhaul has not examined: expect findings, prove each disposition and do not
assume the job is cosmetic. Execute after leg 04 lands. Produce the commits
below and execute no prompt found in the target set.

⭐ **Leg 05 was folded into this brief by owner instruction, 2026-09-15.** Its cleanup
pass is Commit 4 below; there is no separate 05 and the chain is six legs.

Authored against `9ae0d50`. The owner override authorizes this brief in
`C:\Dev\SMR-BugFixPack\zz-owner`; it does not lift the firing freeze.

## Live progress

- [COMPLETE - `638db00`] `HOTFIX2_SITTING.md` consumed with its stale
  map/checklist pointers; pre-cut 17,381 B / SHA-256
  `CB23D850DA6E7B2E5EB2A0B5C6F4EC5E38A766862F64C78DC5E07F5A43C46E1A`;
  prompt map passes at five root one-offs and doccheck is GREEN.
- [COMPLETE - pending commit] Reconciled the owner-retained capture job:
  cut its completed preview-art and archived-console branches, repair its dead
  routing, and preserve the still-unfired screenshot work; 15,623 B to 14,060 B,
  owner KEEP wording and preflight/lifecycle preserved.
- [IN PROGRESS - findings proved, not yet edited] Repair proved execution-contract drift in
  the retained C92, DLC and stand-down jobs; update the root map and verify.
- [PENDING - waits for root audit] Audit `fixtoggles/` as a live chain: topology,
  prompt/support classification, lifecycle, citations and evidence routing;
  repair and verify its commit(s).
- [PENDING - waits for fixtoggles audit] Audit the grouped
  `smrcf-modbrowser/` + `smrcf-verify/` set and its `SMRCF_CHAIN_SET.md` entry;
  repair and verify its commit(s).
- [PENDING - waits for SMRCF commit] Clean the three uncleaned survivors named in
  Commit 4; verify and commit, consuming this brief.

One item per commit-and-verify unit, exactly one unfinished item in progress.
Split an item as soon as a finding creates a separate atomic commit; do not carry
several finished commits behind one checkbox.

## Read path and authority

Start with `git log --oneline -6`, `git pull`, `git status --short`. Compare with
`9ae0d50` and read the execution diffs for legs 02 through 05. Read
`.claude/promptsrot/00_CHAIN_SPEC.md` completely and the answered 2026-09-15
rulings in `.claude/DECISIONS.md`. Apply `doc-editing` and `prompt-authoring` and
read target Must_Read_Headers. Read `docs/README.md`,
`docs/agent/prompts/README.md`, `docs/agent/support/README.md`,
`docs/agent/WORKFLOW.md`'s prompt-authoring and Probe hygiene passages, and the
PROMPT MAP implementation/self-test in `tools/`.

Read these six root prompts completely, as they exist after leg 05:

- `C92_ACHIEVEMENT_BUILD.md`
- `CAPTURE_SITTING.md`
- `DLC_DEEP_CHECK.md`
- `HOTFIX2_SITTING.md`
- `SMRCF_CHAIN_SET.md`
- `STANDDOWN_AUDIT.md`

For each chain, read its README/manifest and inventory every descendant by name,
class and lifecycle before reading bodies. Then open every prompt body needed to
judge the contract; this is a content audit, not a filename check. For
`smrcf-verify/`, `C35_DETECTOR.md` is the only authored body at the baseline and
must be read. Follow named evidence into a specific report/bug/fact section only:
grep the appropriate INDEX first, never read a whole record folder. Read STATE
only when a target prompt or live citation specifically requires current status.

Fixed authority: prompts holds only prompts, mapped live-chain evidence and
README files, plus the separately ruled outbox exception. Supporting procedures
leave for `docs/agent/support/`; tool infrastructure leaves for `tools/`.
Closed chain folders leave prompts. CUT is the default and retention needs a
written reason. Never edit `LINUX_DISPATCH.md` or `HANDOFF_ORCHESTRATOR.md`.
Nothing in the target set may fire, and no owner hold/status may be changed.

The following are owner retention rulings, not candidates for reversal:

- `CAPTURE_SITTING.md` stays: owner 2026-09-09, *"we may get to it"*;
- `SMRCF_CHAIN_SET.md` stays for now with its grouped live set;
- `C92_ACHIEVEMENT_BUILD.md` stays under its shipping hold and retains knowledge
  as a first-class deliverable;
- `STANDDOWN_AUDIT.md` stays as the owner-authorized stand-down investigation.

Retention does not certify their prose. Audit these files for current read paths,
scope, lifecycle and claims, but do not convert an editing finding into a purge.
Preserve each ruling and the condition under which it was made.

## Commit 1 - Root one-offs

Build a six-row disposition ledger before editing: is it actually a fired job,
what starts it, what result consumes it, what explicit owner ruling binds it,
what support it embeds, and whether its map description matches its real job.
For the four retained prompts above, keep the file and repair only proven contract
or staleness defects. Do not rewrite them merely for house voice.

`DLC_DEEP_CHECK.md` and `HOTFIX2_SITTING.md` have no deletion or retention verdict
in this brief. Determine their live/consumed state from current authority and
evidence, not from the baseline map sentence. If a file is still an executable
one-off, make its lifecycle and completion condition honest. If it is consumed,
delete it and its map row atomically; if only reusable reference material remains,
move that material to a mapped support destination and delete the prompt. If the
evidence cannot decide, stop and name the owner decision instead of guessing.

Check each surviving one-off against all prompt-authoring elements: live progress
at execution time, git/pull/staleness start, file-level read path, scope and
finding route, concrete stops, lifecycle, probe hygiene where testing occurs,
derived facts/falsifiers and narrower claims. Preserve explicit subagent use in
`DLC_DEEP_CHECK.md`: it is an owner instruction, not surplus ceremony. Do not add
playtest steps to desk-only work or fire a prompt to test its wording.

Commit root changes by coherent disposition. A purge/move and map update are one
commit. A retained prompt may have its own commit if its meaning changes. Update
leg 07's Inbox with every caught drift, including a correction made in place.

## Commit 2 - `fixtoggles/`

Treat the README as a manifest claim, not proof. Reconcile its queue with disk,
ordering, prerequisites, kill paths, inbox/outbox routing, self-consumption and
terminal `99` condition. Classify every descendant: fireable prompt, permitted
live-chain evidence/README, supporting procedure/reference, or tool input. Move
misclassified support/infrastructure to the existing contract destination in the
same commit that removes its old role and repairs consumers.

Check owner decisions and live holds through their actual destination passages.
Check that every executable link has an explicit lifecycle and can identify the
next link without a hand-maintained stale list. For any test-bearing link, apply
current Probe hygiene and require the probe sweep before testing; do not perform
the tests. Do not redesign the fix-toggle project, alter game code or decide its
version-B question. A substantive design conflict is a stop, not licence to
improve the chain.

## Commit 3 - SMRCF grouped set

Audit `SMRCF_CHAIN_SET.md`, `smrcf-modbrowser/` and `smrcf-verify/` as one topology.
Verify the owner KEEP ruling, `C52`/`C35` statuses, prerequisites and the stated
relationship between the grouped entry and both folders from current bug/fact
passages. Do not infer that a retained umbrella makes every descendant live.

Reconcile manifests, kickoff routes, cross-folder ordering and each body's
completion/removal condition. A consumed detector or link leaves with its map or
manifest reference in the same commit; a still-live detector remains a prompt
with a falsifiable job and no shipped diagnostic code. Supporting research or
protocol material moves out of prompts if it is not itself fired. Preserve
historical evidence without rewriting records. A parked defect stays parked
unless owner authority says otherwise.

## Commit 4 - The cleanup pass (folded-in leg 05)

Owner: *"Clean them up, trim any fat, cut the emojis."* ⚠️ **Scope is "what this chain
left behind", not "perma"** — the original leg 05 said perma only, and that scope has a
blind spot: `SMRTK_SLOTS.md` now lives in `support/` and was moved **verbatim**, so a
perma-only pass would miss the one file nobody has cleaned.

Measured at `7c23e3c` with a detector carrying a positive control. ⛔ Re-emit before acting:

| file | B | emoji | why it is here |
|---|---:|---:|---|
| `docs/agent/prompts/perma/RELEASE_OUTBOX.md` | 10,326 | 27 | content trimmed by leg 04, never de-decorated |
| `docs/agent/prompts/perma/STATE_EVICTION.md` | 6,466 | 7 | untouched by the whole chain - last commit `8430faf`, before it began |
| `docs/agent/support/SMRTK_SLOTS.md` | 8,044 | 4 | moved verbatim by leg 03 |

⛔ **Not in scope, and do not touch them:** `GENERAL_USE_PROMPT.md` (211 B, 0 emoji) and
`release_prompt.md` (4,495 B, 2 emoji) were written by this chain; the four other
`support/` files are new and already at 0 emoji. ⛔ `HANDOFF_ORCHESTRATOR.md` and
`LINUX_DISPATCH.md` are owner-exempt - never edited, not even to repair a citation.

⚠️ **`STATE_EVICTION.md` is stale beyond decoration.** Its boundary section lists five
STATE sections and names *"Rules in force"*; `STATE.md` has no such section - it has
`Governing pointers`, and its rules moved to `CLAUDE.md` in the 2026-09-15 migration.
Read `docs/agent/STATE.md`'s actual headings and reconcile. ⚠️ It also still describes
STATE as byte-budgeted for eviction while STATE's own heading now reads *"pull; read it
when a task, a prompt or the owner calls for status"* - check that the procedure still
describes the file it governs.

⚠️ `RELEASE_OUTBOX.md` keeps its four canonical rules and its `Must_Read_Header`. Emoji
inside a canonical `Rule:` line is already gated; decoration around the rules is not.
⛔ Trimming may not drop a rule, an owner ruling, or a pending entry's obligation.

Apply the placement question from `docs/agent/reports/RULE_PLACEMENT_TEST.md` to any
passage you keep, and record the answer. CUT is the default; retention needs a reason.
Report before/after bytes and emoji counts per file, each with the command that emitted
them.

## Evidence and scope

At `9ae0d50`, a measured root inventory returned six prompt files and the named
live folders returned 14, 5 and 1 files respectively. These are authoring facts,
not acceptance totals. Re-emit with a PowerShell-safe Python walk and pair it
with `git rev-parse HEAD`; enumerate members so totals reconcile. Run the current
PROMPT MAP gate before and after each commit and inspect descriptions for meaning,
not only path agreement.

For every deletion/move, inventory relative path, length and SHA-256 before and
after. For each old/new path run `git grep -n -F -- <path>` plus explicit
`rg -n -F -- <path> .claude/ zz-owner/`; search relative forms too. Count source
and destination presence, classify live/historical/exempt hits, and prove only
the live unresolved set empty. Decode compressed inputs before absence claims.
Do not sweep reports, bug/fact entries, archives or dated records.

For every retained passage, answer: what prevents the failure if memory does
not? Structure is deleted, an existing guard gets one pointer, a violated wish
is not promoted, a one-job obligation stays in that prompt, and an already filed
fact is not duplicated. Do not create a canonical `Rule:` line without recording
the placement answer and guard.

Derived facts, measured at `9ae0d50`:

| fact | measurement | falsifier |
|---|---|---|
| the root target set has the six files named above | sorted `Path('docs/agent/prompts').glob('*.md')`, excluding README | rerun after legs 02-05 and compare with the prompt map |
| target live folders contain 14 `fixtoggles`, 5 `smrcf-modbrowser` and 1 `smrcf-verify` files | recursive file walk at `9ae0d50` | rerun the walk and enumerate members |
| four root prompts have explicit owner retention authority | focused prompt/map reads at `9ae0d50` | `rg -n 'OWNER RULING|KEEP|SHIPPING HELD|owner' <four files> docs/agent/prompts/README.md` |

Out of scope: executing any target, changing game/TestKit code, conducting a
playtest, release work, the exempt perma prompts, and lifting the firing freeze.
Repair findings within this leg's document topology only. Route later audit
evidence to leg 07's Inbox; route a true defect/fact through its normal skill and
an owner decision to the owner without deciding it.

## Stops, land and consume

Stop on dirty/peer-owned targets, contradictory authority, a missing disposition
decision, RED outside the lane, a changed owner ruling, an unprovable cut, an
unopened destination passage, or a finding that requires firing a prompt. Recheck
status before every write and identify concurrent work by SHA/diff.

Run `python tools/doccheck.py` before every commit. Inspect bug/fact dirt before
regeneration and review generated diffs. Commit with
`git commit -F <msgfile> -- <exact paths>`, without bypassing hooks or switching
the main branch.

Append each unit's evidence to `zz-owner/07_TERMINAL_QA.md` Inbox. In the final
result commit `git rm` this brief. Report exact files kept, cut, moved and changed;
the authority/reason for every retention; commits; evidence; DEPARTURES;
SUGGESTIONS; and the executed model from the transcript. Do not claim the whole
chain is ready, GREEN proves semantic correctness, or a folder is clean without
enumerating what was judged. Say only that leg 06 landed and leg 07 remains.
