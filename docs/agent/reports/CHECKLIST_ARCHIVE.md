# Checklist archive execution — completed 2026-09-14

Executed model: Codex (GPT-6), preparation and live execution. Consumed task:
`prompts/CHECKLIST_ARCHIVE.md`, checklist 176 (brief preserved in Git at `4624ec2`).
Both approved groups moved, verified, committed and pushed separately on 2026-09-14.
**D4's original 16 items / 43,223 B did NOT move and remain in the checklist.**
This completes the selected task, not the entire archival backlog.

## Progress

- [x] Group 1 marks: `d80fe75`, doccheck GREEN.
- [x] Group 2 marks: `8988d90`, doccheck GREEN; explicit session approval for
  `closed owner:no` on the date-only items. This means retirement under the date
  heuristic, not evidence that every historical request or test was completed.
- [x] Copy falsification: both proposed moves preserve headers and surviving
  bytes; archive bodies are copied exactly, with only the declared wrappers added.
- [x] SHA guard: both target files checked against loaded SHA256; committed peer
  changes in the load-to-write interval cause refusal before either file is written.
- [x] Stub pointer: archive path plus ck label and instruction to search this
  heading; added bytes included in the balance. Already archived stubs are skipped.
- [x] Tool, evidence and owner-gate handover prepared; committed together after GREEN doccheck.
- [x] Owner gate: explicit all-clear granted 2026-09-14 for both groups.
- [x] Group 1: `1090f70`, register regenerated, doccheck GREEN, committed and pushed.
- [x] Group 2: `cfd97bc`, register regenerated, doccheck GREEN, committed and pushed
  after group 1. Independently revertible.
- [x] Consume prompt and its map row together; record all-clear in ck176 and finish
  this report. The same commit regenerates the register and passes doccheck.

## Selection and authority

MEASURED at `376c216239f3c2235fcddc45ea756bdbfb83d1bc`, using
`.claude/tools/checklist_archive_plan.py` and the original tool's own
`rule_a_matches`, `cited_by_number`, `is_procedure_bearing` (tuple unpacked):

| Group | Selection | Items | Original body bytes |
|---|---|---:|---:|
| 1 | Completion word or checkmark in heading | 11 | 44,288 |
| 2 | Date before 2026-09-08, no completion word | 24 | 115,333 |
| Total | Exact reproduction of the brief | 35 | 159,621 |

The exact headings, original offsets and body-byte counts are preserved in
`.claude/checklist_archive_selection.json`. Line numbers describe the pre-mark
snapshot; use headings for selection after edits. The task helper captures the
initial unmarked set, so it reports no such candidates once marking is complete.

Owner session approval for group 2, after the distinction was explained:
"If that gives you a more broad route to rtetire items I approve it, the more closed the better".
Owner authority on 2026-09-14: **both live moves approved**. The owner was shown,
and accepted, that marking put 16 of the 18 previously report-only ARCHIVE-OLD
items into the selected group 2 move set. That retirement is authorised through
group 2; the archival script itself remains unchanged from preparation and
ARCHIVE-OLD remains report-only by design. No additional headings were selected.

Checklist 176 records the discharged all-clear with `owner:no`. Its broader
backlog stays `open`: the original D4 bodies still remain; no new owner ask was
created by this close-out. The Sonnet archive-addendum recheck described in the
brief is a subsequent task, not part of this execution and not claimed here.

## Falsification and actual moves

Preparation command, executed before the live moves:
`python -X utf8 .claude/tools/checklist_archive_falsify.py` from the repository
root. It copied tracked repository bytes and the companion TestKit into a new
scratch directory, initializes an independent scratch Git repository, runs the
actual whole-repo doccheck, then executes the actual `--apply` there. It never
applies to the live tree, never checks out a branch, and never restores via Git.

The preparation evidence remains in `.claude/checklist_archive_falsification.json`.
Its size predictions were superseded when 03B added 4,467 B at `4624ec2`.
The table below uses each actual live run's own emitted tally, checked against
the owner's revised expected sizes before and after applying. MEASURED:

| Move | Checklist before | Checklist after | Body bytes moved | Pointer bytes added | Archive delta |
|---|---:|---:|---:|---:|---:|
| Group 1 | 761,372 | 718,296 | 44,288 | 1,212 | 46,310 |
| Group 2 | 718,296 | 605,603 | 115,333 | 2,640 | 119,536 |

Both moves keep 160 headings. Archive deltas include 2,022 / 4,203 bytes of
entry wrappers respectively; all other added archive bytes are original bodies.
The archive grew from 365,038 to 530,884 B. The checklist was 605,603 B immediately
after move 2; the consume commit's ck176 receipt then brought it to 606,050 B.
That later wording change is separate from both measured move tallies.

Actual commands (each preceded by a clean status and a matching dry-run tally):
`python -X utf8 .claude/tools/archive_settled.py --headers-file .claude/checklist_archive_group1.json --apply`
then, after committing and pushing group 1,
`python -X utf8 .claude/tools/archive_settled.py --headers-file .claude/checklist_archive_group2.json --apply`.
The JSON files contain only the reviewed exact headings. The unrestricted
default plan was never applied. Neither live run needed a SHA-guard retry.

Live evidence: `.claude/checklist_archive_live_group1.json` and
`.claude/checklist_archive_live_group2.json`, committed with their respective
moves. The verifier is `.claude/tools/checklist_archive_live.py`; its captured
snapshots and full command outputs are located by those evidence files.
**For each move:** 160 headings before and after; balance True; surviving bytes
identical; archive bodies identical with only declared wrappers added;
`MARKER INTEGRITY: 86 on disk, 86 parsed; WARN`; doccheck GREEN. The WARN is the
pre-existing agreeing duplicate ck144, not a parse gap. No marker failed parsing.

MEASURED: dirty checklist refusal; dirty archive refusal; whole-repo RED doccheck
refusal; an unrelated dirty README permitted with GREEN doccheck; SHA refusal
after a real peer commit to each target; already archived selection refusal.
Every refusal preserves target bytes, including the peer's committed edit in the
race cases. Surviving bytes are independently reconstructed from original spans;
the archive check consumes every original body and each declared header wrapper
and requires no remaining bytes. The header count is compared before and after.
Each scratch move is followed by register regeneration, GREEN doccheck and commit.

The first test-reader run omitted the archive format's blank separator after
each entry header, causing its comparison to fail. Inspection located the extra
separator in the declared wrapper; the test reader was corrected and the complete
suite rerun. No archive-body repair or disabled check was used to make it pass.

MEASURED after both live moves, before the consume note:
`python -X utf8 .claude/tools/archive_settled.py` still reports **16 movable
items / 43,223 B**. These are the original D4 backlog, preserved as surviving
bytes in both move verifications. The remaining unmarked ARCHIVE-OLD bucket is
2 items / 14,250 B; it remains report-only.

## Reversal and remaining limits

34 of the 35 selected items are unnumbered: rule (d) cannot protect them at all.
All 24 items in group 2 rely on the owner's age heuristic. This is a selected
retirement set, not proof that those records contain no unfinished obligations.
The repeated `ck-` label is not unique; each pointer also tells the reader to
search the preserved heading. Group 2 marking and movement remain separately
revertible from group 1.

The default tool plan includes already-marked backlog outside these groups.
The execution used `--headers-file` with each group's exact JSON headings;
it refuses missing, duplicate, excluded or already-archived selections. Do not
apply the unrestricted default plan as part of this task.

The cleanliness rail checks only `docs/PLAYTEST_CHECKLIST.md` and
`docs/archive/PLAYTEST_ARCHIVE.md`; doccheck still checks the whole repository.
SHA guards detect changes since loading, including clean peer commits. The two
file replacements remain individually atomic, not a transaction or file lock:
a process failure between writes can leave an archive-only partial move. Preserve
and inspect both files before recovery; do not blindly retry. Register generation
is a separate step immediately after each successful live move.

The original script and approved selection were ignored local files. The exact
tool, helper, falsifier, selection and evidence used here are explicitly tracked
in the preparation commit so this execution can be reviewed and reproduced.
No broad ignore-rule change was made. During live verification `git diff --check`
flagged a new blank line at archive EOF after group 1: this was a copied body
terminator and was retained to preserve the required original bytes. No trimming
or archive-history edits were made.
