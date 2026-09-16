# STATE admission audit

The admission test does not govern the section that accumulates receipts and
role-specific reference. The owner's diagnosis stands. This report implements
only the corrections explicitly authorized by `zz-owner/08_STATE.md`; the
admission, routing and generator changes below remain proposals.

Audit baseline: `f72dc20478c97c54951172abf2de01828a939ec9`. The working tree was
clean. `git show --stat f72dc20` confirms the prerequisite terminal brief was
consumed. The prompt firing freeze remains an owner gate; this owner-supplied
brief runs outside that folder. `python tools/doccheck.py` passed at baseline.
Executed model: GPT-6 (the session's model identity; no more specific variant
is exposed in the transcript).

## Measurement and method

All STATE line numbers below refer to the baseline, not the edited file.
Measurements use UTF-8 bytes with CRLF normalized to LF, as doccheck does.
Heading slices include their heading and trailing blank lines. The title is
accounted for separately, so every byte has exactly one member.

| Slice | Baseline lines | LF bytes |
|---|---|---:|
| Title | 1–2 | 87 |
| Must_Read_Header and navigation | 3–13 | 747 |
| Now | 14–95 | 8,913 |
| Hazard pointers | 96–102 | 586 |
| Governing pointers | 103–116 | 888 |
| Open owner decisions | 117–129 | 1,185 |
| Build state | 130–138 | 368 |
| Total | 1–138 | 12,774 |

`Now` is **69.8%** of the file. The brief's 8,766, 882 and 1,171 are
Unicode-character lengths for Now, Governing and Open, respectively, rather
than byte lengths. Its 139 lines includes the empty slot after the terminal
newline; there are 138 physical lines. There are six `##` headings (including
Must_Read_Header) and no `###` headings. These are measurement corrections,
not changes to the owner's diagnosis.

Reproduce the baseline slices from the repo root with this Python code
(`python -`, supplied through a PowerShell single-quoted here-string):

```python
import re, subprocess
ref = 'f72dc20478c97c54951172abf2de01828a939ec9'
b = subprocess.check_output(['git', 'show', ref + ':docs/agent/STATE.md'])
b = b.replace(b'\r\n', b'\n')
lines = b.splitlines(keepends=True)
starts = [i for i, line in enumerate(lines) if re.match(rb'^#{1,3} ', line)]
assert not any(line.startswith(b'### ') for line in lines)
parts = []
for k, i in enumerate(starts):
    end = starts[k+1] if k+1 < len(starts) else len(lines)
    section = b''.join(lines[i:end])
    parts.append(len(section))
    print(i+1, end, len(section), len(section.decode('utf-8')))
assert sum(parts) == len(b) == 12774
assert parts == [87, 747, 8913, 586, 888, 1185, 368]
assert len(lines) == 138 and len(b.split(b'\n')) == 139
print(ref, 'Now percent', round(parts[2] * 100 / len(b), 1))
```

## Disposition of the header and Now

Every physical line through the end of Now is covered below, without overlaps.
“Keep pending routing” means retained in this patch because its obligations or
authority need a destination check or an owner decision. It does not certify
that the material earns a place in STATE. Proposed homes are not verified
destinations unless explicitly stated otherwise.

| Baseline lines | Classification | Disposition and reason |
|---|---|---|
| 1–7 | Pull notice and local header | Keep: defines when to read and where binding duties live. Blank lines delimit the block. |
| 8 | Procedure pointer and owner format ruling | Keep: existing owner-governed cleanup route. Changing the procedure is a proposal. |
| 9–10 | History and grave navigation | Keep: the current eviction procedure expressly retains the grave pointer. Its historical detail can be reviewed with that procedure. |
| 11–12 | Duplicate global navigation | Cut: CLAUDE's folder contract, map and final authoring paragraph already supply these destinations. No unique duty is removed. |
| 13–14 | Separator and Now heading | Keep: section structure. |
| 15–16 | Release status plus release contents | Keep pending routing: owner-reported release state, not revalidated portal data. Proposed home: release records/outbox; retain a status pointer if admitted. |
| 17–22 | Artifact receipt, reader-fix history, gate and portal uncertainty | Keep pending routing: mixes settled evidence with an unread portal value. Proposed homes: release record and the cited packaging audit; check the outstanding uncertainty before cutting. |
| 23 | Release-only procedure | Keep pending routing: proposed home is UPLOAD_WORKFLOW's pack procedure; this patch does not refactor release instructions. |
| 24–25 | Baseline and archived-source reference | Keep pending routing: proposed fact homes are EF-075/EF-083. Historical version conditions must survive. |
| 26–27 | Evidence priority and playtest branch constraints | Keep and flag: rule wording and triage-only override; not authority for this sweep to retire. Proposed homes: evidence policy and EF-078/079/080. |
| 28–30 | Entry statuses and pending tests | Keep and flag: held work and vacuous-control caveat. Proposed homes: F116/F117/F118 and their playtest riders. |
| 31–33 | ck144 completion receipt | Keep and flag: explicit obligation closure; cannot silently change what is owed. Proposed home: checklist ck144/184 and its closeout report. |
| 34–38 | Probe-maintenance reference and evidence limits | Keep pending routing: active instrument work, not merely retirement markers. Proposed home: toolkit maintenance record; preserve names and the no-prior-comparison caveat. |
| 39–42 | Owner-declined C89 leg and unavailable C85/C88 legs | Keep and flag: owner ruling, reopening condition and not-owed conditions. Proposed homes: the entries' attended checks and checklist. |
| 43–45 | C90/C91/C92 entry summaries | Keep pending routing: source/test distinctions and pending work; proposed homes are those entries and reports. |
| 46–47 | ck172 build permission and shipping hold | Keep and flag: owner authority; any future pointer must preserve the hold and ck171's separate question. |
| 48–51 | C93 field dependency and D14 audit work | Keep and flag: pull-only owner condition mixed with a desk-work pointer. Proposed homes: C93, D14 and STANDDOWN_AUDIT. |
| 52–58 | C95/C96 build hold, classification, C94 status and facts | Keep and flag: owner permission, pack classification and control retirement. Proposed homes: ck185, entries and EF-103/104; do not cut the C94 status in a vocabulary sweep. |
| 59–63 | C97 source audit and unaccepted facts | Keep pending routing: entry-specific evidence and unfinished acceptance work. Proposed home: C97's fact-candidate section; no new engine audit. |
| 64–65 | Saint probe limitation and play receipt | Keep and flag: ck130 detector condition mixed with evidence. Proposed home: toolkit probe record and the relevant entry/checklist item. |
| 66–67 | Release history and pending F107 field leg | Keep pending routing: contains a live untested condition; a blanket history cut would lose it. Proposed homes: release history and F107. |
| 68–72 | Site receipt and owner publication/wording conditions | Keep and flag: publication authority and decision 47 are mixed into the receipt. Proposed homes: site/release record and checklist 47. No live external deployment claim is made by this audit. |
| 73–74 | FR-1 route and wrong field status | Correct the field statement from the owner's ruling; keep the route. Use qualitative wording, avoiding an unverified new field-report total. |
| 75–83 | Toolkit closure, technical reference, age gate and owner limits | Keep and flag: role-specific content with explicit owner conditions. Proposed homes: toolkit report, WORKFLOW probe hygiene, ck184 and FUTURE_IDEAS. No blanket CLOSED cut. |
| 84–85 | Next-work pointers and shipping hold | Keep and flag: current sequence claim plus binding shipping hold. The prompt freeze is not lifted by these pointers. |
| 86 | Sitting continuation and pilot tombstone | Keep “playtest sitting.”; cut the pilot-removal clause under the explicit authorization. No replacement pointer or retirement note. |
| 87 | Owner debt consumed by generator | Keep: current generator dependency; ck151 must survive the proposed migration. |
| 88–89 | Fixture receipt and sitting constraint | Keep pending routing: fixture suitability, taint evidence and a live handoff claim require their task home; not just a completion marker. |
| 90 | Desk-work pointer and owner-deferred chain | Keep and flag: ck148 deferral cannot be changed by this sweep. |
| 91–92 | Watch list | Keep pending routing: role-specific organic tests and falsifiers; proposed homes are the named entries/facts and checklist riders. |
| 93 | Parked/retired statuses and remaining watches | Keep and flag: F60 is an additional tombstone candidate, but it states a ruling-backed status. F60's retirement section was read and preserves the decision plus separate loose ends; do not erase or settle those in this sweep. F109 and the other watches also await routing. |
| 94 | DestroyedRebuild closure with reopening conditions | Keep and flag: deleting CLOSED text would also delete the specific evidence that reopens it. Proposed home: its entry/checklist record. |
| 95 | Separator | Keep: section boundary. |

Coverage check: parse the first cell of the rows in this section, expand each
range, and assert that their concatenation is exactly `list(range(1, 96))`.
This checks coverage, not the judgment assigned to a line.

## Full-file closure sweep and other sections

Command at baseline:
`rg -n -i 'discharged|removed|retired|closed|nothing owed|not owed|supersed|no longer|out \(|history|parked' docs/agent/STATE.md`.
The file is plain UTF-8; no compressed input requires decoding.

Both explicit pilot matches were found, at baseline 86 and 123. At 123 only
the removal clause goes: `(2) and (4) still open` remains. The standalone F60
retirement at 93 is flagged above. Other closure vocabulary occurs inside
release histories, maintenance work, control status, owner rulings and
reopening conditions; their retention reasons are in the table. At 128 the
ck169 receipt also carries the owner's publication authority, so it stays
flagged rather than being automatically removed.

Outside the audited header/Now block, Hazard pointers (96–102) and Governing
pointers (103–116) stay: this task does not grant a new hazard/rule retirement
decision. Open owner decisions (117–129) stay except the authorized pilot
clause, because the generator still consumes the enumeration and the other
lines contain status/authority. Build state (130–138) stays: doccheck verifies
the generated block; the following baseline qualifier is not being changed.

## The admission gap and the generator dependency

Read at baseline: STATE_EVICTION's “The boundary” and “Hazards admission test,”
and `tools/doccheck.py` functions `check_state_and_stubs`,
`state_owed_numbers`, `state_owed_lines`, `classify_items`, `render_waiting`.
Now is governed by current position/next action and no supersession chains.
Harm, universality and gate tests are introduced only for Hazard pointers.
`check_state_and_stubs` checks size, line size and stubs, not whether a Now
line earns admission. This establishes the gap without rerunning the owner's
diagnosis. The temporary cap and its restore condition are untouched.

For the proposed case-insensitive closure pattern
`DISCHARGED|REMOVED|RETIRED|CLOSED|nothing owed|not owed`, the baseline Now slice
matches **13 physical lines**: 31, 33, 34, 35, 41, 56, 70, 75, 78, 81, 86, 93,
94. Filter: baseline lines 14–95, one count per matching line. This is not a
count of tombstones. “closed enumeration” at 78 is a false positive. The
pattern also misses “NOTHING from the toolkit chain is owed” at 83. A gate
needs tested semantics, not an automatic deletion rule.

The generator dry-run at baseline imported `tools/doccheck.py`, classified
the checklist, then replaced `state_owed_numbers` in memory with a function
returning an empty set and classified fresh input again. No files changed.
The same filtering as `render_waiting` was used: `status in MARKER_STATUSES`
and `owner` true, sorted by checklist number.

| Set | Count | Members |
|---|---:|---|
| Parsed STATE owner IDs | 5 | 47, 53, 133, 151, 152 |
| Current rendered decision rows | 16 | 53, 133, 151, 169, 171, 172, 173, 175, 178, 180, 181, 182, 183, 184, 185, 186 |
| Marker-supplied rows / rows surviving without STATE | 13 | 169, 171, 172, 173, 175, 178, 180, 181, 182, 183, 184, 185, 186 |
| Lost on immediate removal of STATE input | 3 | 53, 133, 151 |

The totals reconcile: 13 marker rows + 3 STATE-dependent rows = 16 current
rows. Markers override STATE for 47 and 152. The STATE parser does not capture
185 from its uppercase gist, but its marker does. ck186 likewise reaches the
register through its `status:open owner:yes` marker despite STATE omitting it.
Thus markers are the right direction, but ck186 alone does not demonstrate a
safe migration. `state_owed_lines()` supplies a separate playtest-leg channel;
it currently returns no lines but also needs a destination in the redesign.

Reproduce that dry-run against the unchanged generator/checklist:

```python
import sys
sys.path.insert(0, 'tools')
import doccheck as d
waiting = lambda items: sorted(i['num'] for i in items
    if i['status'] in d.MARKER_STATUSES and i['owner'])
items = d.classify_items(d.checklist_items())
current = waiting(items)
marked = waiting([i for i in items if i['source'] == 'marker'])
print('STATE IDs', sorted(d.state_owed_numbers()))
d.state_owed_numbers = lambda: set()
without_state = waiting(d.classify_items(d.checklist_items()))
lost = sorted(set(current) - set(without_state))
assert without_state == marked
assert lost == [53, 133, 151]
assert len(current) == len(marked) + len(lost) == 16
assert 186 in marked
assert d.state_owed_lines() == []
print('current', current, 'markers', marked, 'lost', lost)
```

## Decision point — proposals, not adopted

| Proposal | Evidence and benefit | Cost / acceptance condition |
|---|---|---|
| Extend admission tests to Now | Reuses the owner's existing tests at the actual growth point. | Small procedure edit, then a content-routing pass. Preserve legitimate status/next-action pointers and owner conditions. The prompts folder remains outside this patch and under its firing freeze. |
| Provide a tracked pull-only intake for unhomed findings | Gives an author somewhere visible to file a finding without defaulting to STATE. | Proposed location: `docs/agent/reports/FINDING_INTAKE.md`; each entry supplies a proposed destination, evidence and routing action. Use an existing suitable record if chosen; define who drains it and remove routed entries so it cannot become another status log. This report is evidence, not that queue. |
| Gate closure vocabulary in Now | Would expose the pilot marker, receipts and F60 status. | Moderate tooling work: delimit Now, test positive/negative cases, handle “closed enumeration” and phrasing variants. Report candidates without automatically deleting owner conditions. Gate severity and exceptions need a decision. |
| Generate WAITING from checklist markers and reduce STATE decisions to a pointer | Removes the second hand-maintained owner-debt source; ck186 demonstrates marker precedence. | Migrate and verify ck53/133/151 first, account for ambiguous unmarked items and playtest legs, then change generator/tests and compare exact before/after member sets. An immediate switch silently loses obligations. |

Recommendation: approve the admission extension and a tracked routing home;
approve the generator direction with the migration conditions above. A literal
closure gate is useful only after its false positives and omissions are
specified. These choices are independently answerable, presented together.
No proposal is adopted, no owner decision is manufactured, and no cap change
is proposed here.

## Execution record

Audit complete; STATE is unchanged at this report's initial commit.
Authorized correction and final verification: pending.

Departures: measure encoded bytes rather than the brief's character totals;
do not call the marker-only switch immediately safe; preserve ruling-backed
closure candidates under the brief's stop-and-report condition. The checklist
body is explicitly out of scope, so unresolved proposals live in this report
and the owner response, not a new checklist edit. Any resulting owner ruling
must be recorded in the checklist by its implementing task.

Suggestions: stage the generator migration before removing STATE's owner
enumeration; make the vocabulary gate a candidate detector whose severity is
chosen explicitly. Do not interpret doccheck GREEN as content admission.
