# Rules headers — migration report

Final execution report, 2026-09-15. Executed by **Codex (GPT-5)**. The mechanical migration is
complete; semantic questions that require the owner are isolated in **Asks**. The companion
[`RULES_HEADERS_INVENTORY.json`](RULES_HEADERS_INVENTORY.json) is the full candidate-occurrence
attachment. Its 852 rows are a locator produced by the earlier heuristic, not the final rule count.

## Done

### Boundary and adjudicated count

The one-time pass read the exact corpus named by the brief: `CLAUDE.md`, `docs/README.md`,
`docs/agent/STATE.md`, `docs/PLAYTEST_CHECKLIST.md` through its preamble only,
`docs/agent/WORKFLOW.md`, `docs/agent/FIX_POLICY.md`, `docs/PLAYTEST_HELP.md`,
`docs/UPLOAD_WORKFLOW.md`, and these fourteen standing prompts:
`CO_RUNS`, `COMBINED_SITTING`, `DISPATCH`, `DRONE_PROJECT_PROMPT`, `GENERAL_USE_PROMPT`,
`HANDOFF_ORCHESTRATOR`, `LINUX_DISPATCH`, `POST_UPLOAD_CLOSE`, `PUBLIC_SURFACE_SWEEP`,
`RELEASE`, `RELEASE_OUTBOX`, `SITE_AUDIT`, `SMRTK_SLOTS`, and `STATE_EVICTION`.
`tools/doccheck.py` was read for the enforcement model. The archive, one-off prompts, chain
folders, generated indexes, facts/bugs entries, and the checklist below its preamble were outside
the semantic census exactly as the brief specified.

The pass separated durable, independently violable duties from facts, status, past rulings,
examples, and ordinary ordered procedure. Obvious duties were filed and carry an A3 verdict.
Imperatives whose status as a durable rule was not obvious were not silently promoted or retired;
they are covered by Ask 1 and remain locatable in the attachment.

| canonical home | global | doc-local | task-local | redundant | dead | total |
|---|---:|---:|---:|---:|---:|---:|
| `CLAUDE.md` | 21 | 0 | 0 | 0 | 0 | 21 |
| `docs/PLAYTEST_CHECKLIST.md` | 0 | 3 | 0 | 0 | 0 | 3 |
| `docs/PLAYTEST_HELP.md` | 0 | 1 | 0 | 0 | 0 | 1 |
| `docs/UPLOAD_WORKFLOW.md` | 0 | 2 | 0 | 0 | 0 | 2 |
| `docs/agent/FIX_POLICY.md` | 0 | 1 | 0 | 0 | 0 | 1 |
| `docs/agent/STATE.md` | 0 | 0 | 0 | 0 | 0 | 0 |
| `perma/COMBINED_SITTING.md` | 0 | 1 | 0 | 0 | 0 | 1 |
| `perma/HANDOFF_ORCHESTRATOR.md` | 0 | 1 | 0 | 0 | 0 | 1 |
| `perma/RELEASE_OUTBOX.md` | 0 | 4 | 0 | 0 | 0 | 4 |
| **total** | **21** | **13** | **0** | **0** | **0** | **34** |

These columns count canonical duties, not prose occurrences. The 34 members reconcile as
21 + 13. The literal list is:

- `CLAUDE.md`: read STATE; read a document's header before editing it; invoke the doc-editing
  skill; do not edit the archive; edit generated sources and regenerate; run doccheck before doc
  commits; record owner decisions in the checklist; honor owner authority; verify identified
  command output once; treat authored material as claims; inherit facts after one check; command-
  read volatile external values; read volatile repository status from STATE/WAITING; use
  fingerprints for durable facts; prove negatives by grep/decode/presence count; make verification
  falsifiable; run before writing measurements; record and reconcile counts; record the executed
  model; attribute shared work by commit/diff; and recheck/stage shared paths safely.
- `PLAYTEST_CHECKLIST.md`: keep work items here and help elsewhere; archive completed/settled
  bodies while retaining their markers and pointers; move dated session records to SESSION_LOG.
- `PLAYTEST_HELP.md`: keep reference material here and tests in the checklist.
- `UPLOAD_WORKFLOW.md`: keep only the owner-facing upload procedure here; keep backup page copies
  byte-matching their authoritative descriptions.
- `FIX_POLICY.md`: retain section 5.
- `COMBINED_SITTING.md`: strike each scheduled moment as it is taken.
- `HANDOFF_ORCHESTRATOR.md`: only the owner may retire, archive, gut, or delete the file.
- `RELEASE_OUTBOX.md`: append player-facing pending entries; exclude never-shipped internal fixes;
  clear pending only through RELEASE after upload; delete only through release or stated withdrawal.

`STATE.md` intentionally has a header with zero canonical lines. Its header is a status/pointer
declaration, not a rule. `prompts/README.md:5` remains the single owner-approved folder-level
survivor for the perma lifecycle: “never `git rm`; update in place.” It is not a doc-local duty of
the map itself, so putting it in the map's own edit header would make it invisible to the perma
prompt edits it governs.

### Canonical style and header sizes

The style decision was recorded before migration in `bdf6862`. One physical line has the form
`Rule: <present-tense imperative ending in a period> [A3: pass]`. It begins at column 1 between
literal RULES markers under `## Must_Read_Header`. A line contains one independently violable duty;
paths and commands use code spans. It contains no emoji, bold emphasis, history, rationale,
examples, severity language, or shout-case synonyms. This converges duplicate wording and gives
the checker a cheap syntax plus an explicit adjudication token.

The cap unit is UTF-8 bytes after CRLF/CR normalization to LF, from the header heading through the
closing marker inclusive. Warning is over 1,024 B; RED is over 2,048 B.

| required header | bytes | duties |
|---|---:|---:|
| `CLAUDE.md` | 1,968 | 21 |
| `docs/PLAYTEST_CHECKLIST.md` | 385 | 3 |
| `docs/PLAYTEST_HELP.md` | 181 | 1 |
| `docs/UPLOAD_WORKFLOW.md` | 265 | 2 |
| `docs/agent/FIX_POLICY.md` | 144 | 1 |
| `docs/agent/STATE.md` | 178 | 0 |
| `perma/COMBINED_SITTING.md` | 112 | 1 |
| `perma/HANDOFF_ORCHESTRATOR.md` | 158 | 1 |
| `perma/RELEASE_OUTBOX.md` | 512 | 4 |

The seven owner-named documents all received headers. `COMBINED_SITTING.md` is the sole census
addition: “strike each scheduled moment as it is taken” is a unique constraint on editing that
recipe, so the uniform criterion required a local header. `CLAUDE.md` is the kernel rather than an
additional local document. Only `CLAUDE.md` crosses WARN; no header crosses the hard cap.

### Moves, rewrites, and deletion-survivor ledger

The following ten WORKFLOW globals were restyled in `CLAUDE.md`; the current survivor is named on
the right. These are wording-preserving restyles rather than byte-identical moves, so both forms
are quoted instead of claiming literal preservation.

| deleted WORKFLOW wording | canonical survivor |
|---|---|
| “VOLATILE-external … Read it with a command, every time” | “Read volatile external values with a command every time.” |
| “VOLATILE in-repo … STATE.md, docs/WAITING_ON_YOU.md” | “Read volatile in-repository status from `STATE.md` and `docs/WAITING_ON_YOU.md`.” |
| “DURABLE structural … fingerprint … re-derive only what MOVED” | “Verify durable structural facts by fingerprint and rederive only groups that moved.” |
| “Never read a file to prove a negative … decode first … presence side counted” | “Prove absence with a grep after decoding compressed inputs and count the presence side.” |
| “Every check must be scoped so it CAN fail” | “Scope every verification command so contrary evidence could make it fail.” |
| “Run, then write … `<<PENDING-RUN>>`” | “Run a measurement before writing it and mark unrun measurements `<<PENDING-RUN>>`.” |
| “Every count carries the command and the filter … reconcile … members” | “Record every count with its command and filter and reconcile each total against its members.” |
| “Record the executed model at close-out” | “Record the executed model from the transcript at close-out.” |
| “git log --author cannot attribute work … sha + diff” | “Attribute shared-tree work by commit and diff rather than author identity.” |
| “Re-check git status … stage your own hunks … without a pathspec” | “Recheck shared paths immediately before writing and stage only owned hunks without a pathspec.” |

The task-specific “a fix invalidates its own tests” and owner-observability rail remain in
WORKFLOW. They did not become global merely because neighboring clauses moved.

The seven perma files below lost the owner-approved duplicate lifecycle restatements. Every one has
the same survivor, `docs/agent/prompts/README.md:5`, quoted above.

| deleted copy | former wording (condensed only where one occurrence spanned lines) | survivor |
|---|---|---|
| `RELEASE.md` | “reusable, not self-consuming”; “REUSABLE — do NOT git rm this file” | prompt map line 5 |
| `POST_UPLOAD_CLOSE.md` | “REUSABLE SUB-PROMPT … do NOT git rm this file” | prompt map line 5 |
| `DRONE_PROJECT_PROMPT.md` | “RE-RUNNABLE … does NOT delete itself … Update it in place” | prompt map line 5 |
| `LINUX_DISPATCH.md` | “standing”; “never git rm this file”; “Update §1 in place” | prompt map line 5 |
| `SMRTK_SLOTS.md` | “updated in place, never consumed with git rm” | prompt map line 5 |
| `STATE_EVICTION.md` | “reusable; do not delete after a run” | prompt map line 5 |
| `COMBINED_SITTING.md` | two copies of “does NOT delete itself” | prompt map line 5 |

Other source-local consolidations also name their survivors:

- Checklist preamble constraints → its three current header lines.
- Playtest Help content split → its current header line.
- Upload scope and page-copy parity → its two current header lines.
- FIX_POLICY section-5 retention → its current header line.
- Handoff owner-only retirement block and reminder → its current header line; the body now records
  authority and the empty-list ask trigger without granting retirement.
- Release Outbox append/exclude/clear/delete clauses → its four current header lines.
- Combined Sitting's duplicate lifecycle statements → prompt-map line 5; its separate strike duty
  → the Combined header.
- STATE's archive, generated-file, verification, measurement, and shared-tree directives → the
  corresponding `CLAUDE.md` lines; tracker/deployment/player-surface specializations → pointers to
  `PUBLIC_SURFACE_SWEEP`, `SITE_AUDIT`, and FIX_POLICY; upload backup duty → UPLOAD's header.

The migration did not delete the uncertain semantic duplicates in Ask 2 or any dead candidate in
Ask 3.

### Commits, byte budget, and verification

The independently reverting source units are:

`bdf6862` style record · `51fdbaf` checklist · `a3d316f` help · `2ec044f` upload ·
`1cf9ada` FIX_POLICY · `dcb401a` handoff · `ad3dd5a` outbox · `c52e185` CLAUDE plus regenerated
AGENTS mirror · `5a6e02a` WORKFLOW globals · `8e350d6` STATE · `74e2584` RELEASE · `8936a51`
POST_UPLOAD_CLOSE · `5f8a653` drone · `06296f3` Linux · `021387f` SMRTK slots · `8430faf`
STATE_EVICTION · `be3a171` Combined Sitting · `3817472` checker.

Doccheck was GREEN after every committed source unit. Literal `git grep -F` controls were run for
moved clauses; reworded clauses are explicitly paired above and are not claimed byte-identical.
At baseline `57ca926`, STATE was 12,930 B with SHA-256
`df45ad35533d57c197969eae61de929b39fb4c7294714a5507356884ebd98bbe`; it is now 11,437 B,
a 1,493 B reduction. CLAUDE grew from 2,506 B to 3,713 B, a 1,207 B increase. The two-file net is
**−286 B**. The complete push set moved from 42,602 B to 42,316 B against the 40,960 B budget:
still over, but not further over.

`tools/doccheck.py` now gates the nine required blocks, marker count/order, normalized byte cap,
STATE's zero-duty condition, canonical style, permitted surfaces, and duplicate canonical text.
It issues the separately scoped repo-wide placement WARN. The check was falsified by removing
PLAYTEST_HELP's closing marker: it reported `RULES HEADERS: RED` and `doccheck: RED`. Restoration
returned blob hash `c76b3a45c8d0b0924f439ada1bbf2c03fb605517` exactly and doccheck returned GREEN.

The structural check cannot determine whether prose is really a rule, whether the census found
every semantic duty, whether an agent read or understood a header, or whether an agent obeyed it.
It proves only the mechanical properties of adjudicated, marked rules. The not-yet-built
doc-editing skill remains the intended future mechanism for creating a header when a new local
duty appears in a headerless document.

## Asks

### 1. Where is the boundary between a durable rule and an ordered task instruction?

The attachment's heuristic found 852 imperative occurrences: 30 labeled doc-local, 780 task-local,
16 global, 20 redundant, and 6 dead. Those figures reconcile as 852, but they are deliberately not
inherited as a rule count. Most of the 780 are numbered procedure steps such as “run this command”
or “record this result.” Treating every step as a canonical rule would exceed the header cap and
erase the distinction between a task procedure and a durable constraint; treating all of them as
mere prose may be too narrow for the owner's definition. Should ordinary ordered steps remain
instructions, with only independently reusable constraints becoming canonical rules? This one
answer adjudicates all `classification: task-local` members and the unfiled doc-local candidates
in the attachment.

### 2. May the remaining semantic echoes be deduplicated to the named homes?

The old locator's R1–R14 groups quote both sides and proposed homes. Mechanical work already
settled R4 and R9, while R12–R14 are now explicit pointers rather than restatements. The remaining
question covers R1 (STATE bootstrap), R2 (doccheck-before-doc-commit), R3 (owner-decision mirror),
R5 (restore editor-stripped comments), R6 (release spans upload and close-out), R7 (STATE is status
and pointers), R8 (game/source trees read-only), R10 (no trailing console comments), and R11
(MarsDebug tally is not retail). Their exact source/survivor quotes are in `redundancy`; some echoes
carry task context, so they were preserved rather than being silently treated as identical scope.

### 3. May the six proven-dead instructions be retired?

They were flagged, not deleted. Rechecked together at HEAD `38174722f8d2818bd8a8865cc0196f00b932c239`:

- POST_UPLOAD_CLOSE's first-launch hold: `rg -n '④|NOTHING IS PUBLISHED' docs/agent/STATE.md`
  returned exit 1.
- Its opt-in report kickoff: `Test-Path C:/Dev/SMR-OptInPack/docs/agent/reports/PARKED_OPTIN_REFERENCES.md`
  returned `False`.
- Its self-consume step: the current command finds `perma/POST_UPLOAD_CLOSE.md:93` saying
  “`git rm` this file” and `prompts/README.md:5` saying perma prompts are never removed. The latter
  is the owner-approved lifecycle survivor; the former is the dead candidate.
- PUBLIC_SURFACE_SWEEP's one-off gate: `Test-Path docs/agent/prompts/SURFACE_AUDIT_FABLE.md`
  returned `False`.
- HANDOFF's checklist-archive prompt: `Test-Path docs/agent/prompts/CHECKLIST_ARCHIVE.md`
  returned `False`.
- COMBINED_SITTING's old release-state promotion: `rg -n '②|③' docs/agent/STATE.md` returned exit 1.

### 4. How should the surviving scope conflicts be resolved?

One answer per conflict class is enough; members and verbatim source excerpts are in attachment
flags X1–X7 and X9:

- X1: live MOD_DESCRIPTION editing versus the archive prohibition.
- X2: the entry-file folder list versus generated WAITING_ON_YOU.
- X3: explicit-path commits versus the shared-file no-pathspec exception.
- X4/X5: reply-as-shipping and Linux ASK playbooks versus the owner's pull-only reply policy.
- X6: legacy bare `tested` wording versus attended/unattended labels.
- X7: first-launch assumptions mixed into current release procedures.
- X9: the literal U+0001 in STATE_EVICTION's sed example.

X8 is no longer open: the owner routed globals to CLAUDE, and this migration implemented that
ruling. Checklist 177's marker-gate question was not touched.

### 5. What interpretation should close the trust-by-source class-2 wording?

The duty was restyled without choosing the open policy outcome: CLAUDE currently says both to
verify identified command output once and to inherit a fact after one check. The owner decision
register's row 8 remains the authority for whether that “one check” is always sufficient or has a
narrower scope. No wording in this migration claims to resolve it.
