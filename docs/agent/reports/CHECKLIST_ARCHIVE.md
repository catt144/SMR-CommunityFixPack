# Checklist archive execution — 2026-09-13

Executed model: Codex (GPT-6). Task: `prompts/CHECKLIST_ARCHIVE.md`, checklist 176.
Live moves are HELD pending the separate owner all-clear. The prompt remains live.

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
- [ ] In progress: owner gate, BLOCKED waiting for the all-clear after this handover.
- [ ] Move group 1, regenerate owner register, doccheck, commit and push.
- [ ] Move group 2, regenerate owner register, doccheck, commit and push.
- [ ] Consume prompt and its map row in the same commit; finish report.

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
The existing exclusions still apply. ARCHIVE-OLD remains report-only. The live
move gate is separate and has not yet been answered after this evidence.

## Falsification and move prediction

Run: `python -X utf8 .claude/tools/checklist_archive_falsify.py` from the repository
root. It copies tracked repository bytes and the companion TestKit into a new
scratch directory, initializes an independent scratch Git repository, runs the
actual whole-repo doccheck, then executes the actual `--apply` there. It never
applies to the live tree, never checks out a branch, and never restores via Git.

The evidence JSON is `.claude/checklist_archive_falsification.json`; it records
the source HEAD, working-byte hashes, scratch location and separate move measurements.
The final rehearsal includes the checklist 176 handover note. MEASURED:

| Move | Checklist before | Checklist after | Body bytes moved | Pointer bytes added | Archive delta |
|---|---:|---:|---:|---:|---:|
| Group 1 | 756,905 | 713,829 | 44,288 | 1,212 | 46,310 |
| Group 2 | 713,829 | 601,136 | 115,333 | 2,640 | 119,536 |

Both moves keep 160 headings. Archive deltas include 2,022 / 4,203 bytes of
entry wrappers respectively; all other added archive bytes are original bodies.
The live checklist is still 756,905 bytes; the archive is still 365,038 bytes.

After owner approval only, run each group separately with
`--headers-file .claude/checklist_archive_group1.json` or
`--headers-file .claude/checklist_archive_group2.json`; commit and push the first
move before the second. These JSON files contain only the reviewed exact headings.

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

## Reversal and remaining limits

34 of the 35 selected items are unnumbered: rule (d) cannot protect them at all.
All 24 items in group 2 rely on the owner's age heuristic. This is a selected
retirement set, not proof that those records contain no unfinished obligations.
The repeated `ck-` label is not unique; each pointer also tells the reader to
search the preserved heading. Group 2 marking and movement remain separately
revertible from group 1.

The default tool plan includes already-marked backlog outside these groups.
Use `--headers-file` with each group's exact JSON headings for these two moves;
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
No broad ignore-rule change is needed.
