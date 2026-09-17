# Checklist purge ledger — 2026-09-16

Owner instruction: `zz-owner/CHECKLIST_PURGE_PROMPT.md` (authored at `4f610d3`). One line per
marker of `docs/PLAYTEST_CHECKLIST.md` as it stood at `4f610d3`, with its disposition. Bodies were
archived in `4568912`; the file was deleted and doccheck made GREEN in the following commit; the
owner's live list is `zz-owner/playtest_checklist.md` (local, gitignored).

## Counts, reconciled

Markers counted with doccheck's own regex `<!--\s*ck:(\d+|-)\s+status:([a-z]+)\s+owner:(yes|no)\s*-->`
over the file at `4f610d3` (scratchpad `gen_addendum.py`; the same 154 as
`grep -o -E "<!-- ck:[^>]*" docs/PLAYTEST_CHECKLIST.md | wc -l`).

| disposition | count |
|---|---|
| already homed | 138 |
| homed now | 15 |
| homed with 169 | 1 |
| **total markers** | **154** |
| purged (item bodies) | 0 |
| purged for time | 0 |
| kept for the owner (a subset of the rows above, not additive) | 17 |

Already homed = 93 new-wording stubs (exact `## ck.. -- archived` heading line found) + 35 old-wording
stubs (a 40-character heading core found; the old archiver dropped the date) + 10 pointer stubs (their
archive section heading found) = 138. Every stub was found; none was re-copied.

154 markers = 153 `### ` items + 1 marker nested inside item 169's `<details>` block (line 1136).
That reconciles doccheck's WAITING line (153 items, 9 waiting) against the marker grep (154, 10 open
owner:yes): the nested marker was open/owner:yes but never an item.

**Call made without asking — why nothing was purged.** Every body still live in the file was appended
verbatim to the append-only archive instead of being adjudicated item by item: a ruled body is an owner
decision the kernel rule requires to stay recorded, the archive is pull-only so the bytes cost no
session anything, and the time available did not allow a defensible per-item cut. The peer analysis in
`.claude/checklist_overhaul/useful_candidates.md` (local) rates most of the tail as spent or redundant;
the tail went in as one block regardless. Non-item content purged: the file's preamble (lines 1-28:
its own Must_Read_Header rules, the 08-03 redesign note and the 08-11 "BOTH TICKS DONE" pointer),
all of which was either checklist-local or already in the archive; git history keeps the text.

## Per-marker ledger

| marker | line | status | owner | disposition | destination | kept for the owner |
|---|---|---|---|---|---|---|
| ck:191 | 32 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:190 | 37 | ruled | no | already homed | archive; verified by archive section heading 'C93 diagnosis scope' | one line under standing rulings |
| ck:188 | 44 | open | yes | homed now | archive `## ck188 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: attribution question + live look or drop |
| ck:189 | 141 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:188 | 146 | open | yes | homed now | archive `## ck188 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: C100 defect-or-design + the cheap watch |
| ck:187 | 174 | ruled | no | already homed | archive; verified by exact archive heading line | one line under standing rulings |
| ck:- | 179 | closed | no | already homed | archive; verified by archive section heading 'Citations do not hold evidence' |  |
| ck:- | 184 | closed | no | already homed | archive; verified by archive section heading 'Checklist archival answers' |  |
| ck:- | 189 | closed | no | already homed | archive; verified by archive section heading 'Release closes empty the outbox' |  |
| ck:- | 194 | closed | no | already homed | archive; verified by archive section heading 'LF tree and RED mixed line endings' |  |
| ck:- | 199 | closed | no | already homed | archive; verified by archive section heading 'Do not build a fix for a version players cannot play' |  |
| ck:- | 204 | closed | no | already homed | archive; verified by archive section heading 'Affected-save recovery requirement' |  |
| ck:- | 209 | closed | no | already homed | archive; verified by archive section heading 'Wildfire investigation override' |  |
| ck:- | 214 | closed | no | already homed | archive; verified by archive section heading 'STATE admission door installation' |  |
| ck:- | 219 | closed | no | already homed | archive; verified by archive section heading 'STATE cleanup scope override' |  |
| ck:186 | 224 | open | yes | homed now | archive `## ck186 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: skill caps |
| ck:185 | 241 | ruled | yes | already homed | archive; verified by exact archive heading line |  |
| ck:184 | 247 | ruled | yes | already homed | archive; verified by exact archive heading line | one line under standing rulings |
| ck:182 | 253 | ruled | yes | homed now | archive `## ck182 -- archived 2026-09-16 (was checklist status:ruled)`, commit 4568912 | two lines under approved agent work not run |
| ck:181 | 420 | open | yes | homed now | archive `## ck181 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: attended monolith audit gate (178 restore rides on it) |
| ck:180 | 445 | open | yes | homed now | archive `## ck180 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 |  |
| ck:179 | 470 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:178 | 476 | ruled | yes | already homed | archive; verified by exact archive heading line | one line under 181 and under standing rulings |
| ck:177 | 481 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:176 | 486 | open | no | homed now | archive `## ck176 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 |  |
| ck:175 | 599 | ruled | yes | already homed | archive; verified by exact archive heading line |  |
| ck:183 | 604 | ruled | yes | homed now | archive `## ck183 -- archived 2026-09-16 (was checklist status:ruled)`, commit 4568912 | section: slot engine, defect 20, Stamper; two Run lines |
| ck:174 | 1015 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:172 | 1020 | ruled | yes | homed now | archive `## ck172 -- archived 2026-09-16 (was checklist status:ruled)`, commit 4568912 | section: C92 shipping held + account.dat route |
| ck:173 | 1044 | open | yes | homed now | archive `## ck173 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: FIX_POLICY §2a call |
| ck:171 | 1066 | open | yes | homed now | archive `## ck171 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | folded into the 172 section (overtaken by option B) |
| ck:170 | 1093 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:169 | 1098 | open | yes | homed now | archive `## ck169 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: site deploy is the owner's act |
| ck:- | 1136 | open | yes | homed with 169 | archive `## ck169 -- archived 2026-09-16` (marker sits inside 169's details block) |  |
| ck:168 | 1175 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:167 | 1180 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:166 | 1185 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:165 | 1190 | ruled | no | already homed | archive; verified by exact archive heading line | one line under standing rulings |
| ck:164 | 1195 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:163 | 1200 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:162 | 1205 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:161 | 1210 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:160 | 1215 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:158 | 1220 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:159 | 1225 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:157 | 1230 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:157 | 1235 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:156 | 1240 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:155 | 1245 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:154 | 1250 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:153 | 1255 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:152 | 1260 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:151 | 1265 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:150 | 1270 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:149 | 1275 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:148 | 1280 | deferred | no | homed now | archive `## ck148 -- archived 2026-09-16 (was checklist status:deferred)`, commit 4568912 | section: fix toggles deferred, how to start |
| ck:146 | 1318 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:147 | 1323 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:145 | 1328 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1333 | closed | no | already homed | archive; verified by 40-char heading core 'v7 IS LIVE on both stores (your word). N' |  |
| ck:144 | 1338 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:143 | 1343 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:144 | 1348 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:142 | 1353 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:141 | 1358 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:140 | 1363 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:139 | 1368 | closed | no | already homed | archive; verified by 40-char heading core '139 BUILT + TESTED-ATTENDED: all seven s' |  |
| ck:138 | 1373 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:137 | 1378 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:136 | 1383 | open | yes | homed now | archive `## ck136 -- archived 2026-09-16 (was checklist status:open)`, commit 4568912 | section: FR-3 profiling decision; FR-1 nothing owed |
| ck:135 | 1503 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:134 | 1508 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1513 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1518 | closed | no | already homed | archive; verified by 40-char heading core '`100_DOCSWEEP` IS DONE: the words now ma' |  |
| ck:133 | 1523 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1528 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1533 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:131 | 1538 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1543 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1548 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1553 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:126 | 1558 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1563 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1568 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1573 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1578 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1583 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:125 | 1588 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:124 | 1593 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:98 | 1598 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:118 | 1603 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1608 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1613 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:111 | 1618 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1623 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1628 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:87 | 1633 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1638 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:82 | 1643 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1648 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:79 | 1653 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:78 | 1658 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1663 | ruled | no | already homed | archive; verified by 40-char heading core 'RULED AND APPLIED. The hazard is reworde' |  |
| ck:- | 1668 | closed | no | already homed | archive; verified by 40-char heading core 'F105 IS FIXED ON YOUR WORD, AND BUILDING' |  |
| ck:- | 1673 | closed | no | already homed | archive; verified by 40-char heading core 'F105 IS REPRODUCED ON OUR OWN RIG, AND T' |  |
| ck:76 | 1678 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:73 | 1683 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1688 | closed | no | already homed | archive; verified by 40-char heading core 'IT IS PUBLISHED, ON BOTH PORTALS. The id' |  |
| ck:- | 1693 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1698 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1703 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1708 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1713 | closed | no | already homed | archive; verified by 40-char heading core 'C50 IS BUILT, AND IT TOUCHES THREE SCREE' |  |
| ck:- | 1718 | closed | no | already homed | archive; verified by 40-char heading core 'THE PLAN CHANGED ON YOUR RULING: C50+C51' |  |
| ck:- | 1723 | ruled | no | already homed | archive; verified by 40-char heading core 'YOU RULED THE POST-RELEASE TESTING MODEL' |  |
| ck:56 | 1728 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1733 | closed | no | already homed | archive; verified by 40-char heading core 'your two rulings are carried out. Nothin' |  |
| ck:53 | 1738 | closed | no | homed now | archive `## ck53 -- archived 2026-09-16 (was checklist status:closed)`, commit 4568912 |  |
| ck:52 | 1900 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:50 | 1905 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1910 | closed | no | already homed | archive; verified by 40-char heading core 'the SAME defect class, in the third mod.' |  |
| ck:- | 1915 | closed | no | already homed | archive; verified by 40-char heading core "the launch test's own first question cou" |  |
| ck:47 | 1920 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1925 | closed | no | already homed | archive; verified by 40-char heading core 'run B now has an ATTENDED moment in it. ' |  |
| ck:- | 1930 | closed | no | already homed | archive; verified by 40-char heading core 'THE UPLOAD IS PAUSED ON YOUR OWN WORD. T' |  |
| ck:43 | 1935 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1940 | ruled | no | already homed | archive; verified by 40-char heading core 'STATE.md WAS EVICTED ON YOUR DIRECTION, ' |  |
| ck:41 | 1945 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:40 | 1950 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:39 | 1955 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1960 | closed | no | already homed | archive; verified by 40-char heading core 'SWEEP CHAIN, LINK 1 REPORTED. Nothing bl' |  |
| ck:- | 1965 | closed | no | already homed | archive; verified by 40-char heading core 'THE RENAME IS DONE, EVERYWHERE A PERSON ' |  |
| ck:- | 1970 | closed | no | already homed | archive; verified by 40-char heading core 'SOLO LAUNCH: ✅ the parking work is DONE;' |  |
| ck:- | 1975 | closed | no | already homed | archive; verified by 40-char heading core '"ONE MOD FIX ALL": I checked the other c' |  |
| ck:- | 1980 | closed | no | already homed | archive; verified by 40-char heading core 'WE MEASURED YOUR OPEN FARM CASE ON YOUR ' |  |
| ck:- | 1985 | closed | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 1990 | closed | no | already homed | archive; verified by 40-char heading core 'pricing your "quick playtest?" question ' |  |
| ck:- | 1995 | closed | no | already homed | archive; verified by 40-char heading core 'the C39 repair you ruled turns out to to' |  |
| ck:- | 2000 | closed | no | already homed | archive; verified by 40-char heading core '④ IS CUT: your launch afternoon reads ON' |  |
| ck:- | 2005 | closed | no | already homed | archive; verified by 40-char heading core 'the release descriptions are being writt' |  |
| ck:- | 2010 | closed | no | already homed | archive; verified by 40-char heading core 'the SITE is built (unpublished): one sma' |  |
| ck:- | 2015 | closed | no | already homed | archive; verified by 40-char heading core 'D13 CHAIN CLOSED; the ONE combined sitti' |  |
| ck:- | 2020 | closed | no | already homed | archive; verified by 40-char heading core 'THE SHIP LINE (three rulings, decided in' |  |
| ck:- | 2025 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 2030 | closed | no | already homed | archive; verified by 40-char heading core 'public documentation: platform decided, ' |  |
| ck:- | 2035 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 2040 | closed | no | already homed | archive; verified by 40-char heading core 'your Steam ID is scrubbed from the live ' |  |
| ck:- | 2045 | closed | no | already homed | archive; verified by 40-char heading core 'I DELETED ONE OF YOUR AUTOSAVES. Telling' |  |
| ck:- | 2050 | closed | no | already homed | archive; verified by 40-char heading core 'asteroid Exotic-Minerals freeze (decided' |  |
| ck:- | 2055 | closed | no | already homed | archive; verified by 40-char heading core 'raised by you mid-sitting during `corun-' |  |
| ck:- | 2060 | closed | no | already homed | archive; verified by 40-char heading core 'from the `corun-pt15` SITTING (two calls' |  |
| ck:- | 2065 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 2070 | ruled | no | already homed | archive; verified by exact archive heading line |  |
| ck:- | 2075 | closed | no | already homed | archive; verified by 40-char heading core 'from `corun-batch-2` prep (nothing needs' |  |

## Dead citations left in place (121 files)

Counted after the deletion with
`grep -rl PLAYTEST_CHECKLIST --include=*.md --include=*.py . | grep -v ^./docs/archive`. Only the
files doccheck or a skill needs were repointed (CLAUDE.md, AGENTS.md, docs/README.md, two skills and
their mirrors, tools/doccheck.py, tools/counts_selftest.py). The rest cite a path that no longer
exists; the bodies they cite are in `PLAYTEST_ARCHIVE.md` under `## ck<n>`. The two perma prompts
under the owner's no-edit ruling (`HANDOFF_ORCHESTRATOR.md`, `LINUX_DISPATCH.md`) are untouched.

- `.claude/BASELINE.md`
- `.claude/BATCH_A_BRIEF.md`
- `.claude/CHECKLIST_MOVE_MANIFEST.md`
- `.claude/CONTEXT_ECONOMICS_REVIEW.md`
- `.claude/DECISIONS.md`
- `.claude/FRESH_SESSION_PROMPT.md`
- `.claude/HANDOFF_ORCHESTRATOR.md`
- `.claude/HANDOFF_ORCHESTRATOR_control.md`
- `.claude/HANDOFF_ORCHESTRATOR_non_skill.md`
- `.claude/IMPLEMENT_PROMPT.md`
- `.claude/MERGE_CONTRACT.md`
- `.claude/OPTIN_INVENTORY.md`
- `.claude/PLAN_TODO.md`
- `.claude/REPORT_MOVES_VERDICT.md`
- `.claude/SEAT_WORKLIST.md`
- `.claude/SWEEP_RESULTS.md`
- `.claude/baseline.py`
- `.claude/briefs/POST08_A_WORKFLOW_RETIREMENTS.md`
- `.claude/briefs/POST08_C_SAVE_SELECTION_RULE.md`
- `.claude/checklist_marked_preview.md`
- `.claude/checklist_overhaul/CHECKLIST_MARKER_TABLE.md`
- `.claude/checklist_overhaul/markers_A.md`
- `.claude/checklist_overhaul/markers_B.md`
- `.claude/checklist_overhaul/procedure_triage.md`
- `.claude/checklist_overhaul/useful_candidates.md`
- `.claude/claude_HANDOFF_ORCHESTRATOR.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/A_handoff_control.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/B_handoff_noskill.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/C_handoff_skill.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/D_handoff_codexskill.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/SKILL_codex_draft1.md`
- `.claude/evidence/skill_ab_2026-09-14/artifacts/SKILL_codex_draft2_ARM_D.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/ck182_append_C_only.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/ck184_B_noskill.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/ck184_C_skill.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/ck184_D_codexskill.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/downstream_cost_orphaned_finding.md`
- `.claude/evidence/skill_ab_2026-09-14/extracts/lost_finding_c.md`
- `.claude/evidence/skill_codex_design/candidate_draft1.md`
- `.claude/evidence/skill_codex_v2/handoff_before.md`
- `.claude/evidence/skill_codex_v2/skill_v1.md`
- `.claude/evidence/skill_codex_v2/skill_v2.md`
- `.claude/lookback_ffd04af_post/PLAYTEST_CHECKLIST.md`
- `.claude/lookback_ffd04af_post/STATE.md`
- `.claude/lookback_ffd04af_post/WAITING_ON_YOU.md`
- `.claude/tools/archive_settled.py`
- `.claude/tools/checklist_archive_falsify.py`
- `.claude/tools/checklist_archive_live.py`
- `.claude/tools/mkmarkers.py`
- `.claude/tools/relevance.py`
- `.git/vanillahunt03/closeout_docs.py`
- `docs/README.md`
- `docs/agent/STATE.md`
- `docs/agent/WORKFLOW.md`
- `docs/agent/bugs/C46.md`
- `docs/agent/bugs/C95.md`
- `docs/agent/bugs/D10.md`
- `docs/agent/bugs/D12.md`
- `docs/agent/bugs/F04.md`
- `docs/agent/bugs/F100.md`
- `docs/agent/bugs/F110.md`
- `docs/agent/bugs/F116.md`
- `docs/agent/bugs/F117.md`
- `docs/agent/bugs/F34.md`
- `docs/agent/bugs/F35.md`
- `docs/agent/bugs/F48.md`
- `docs/agent/bugs/F50.md`
- `docs/agent/bugs/F52.md`
- `docs/agent/bugs/F70.md`
- `docs/agent/bugs/F74.md`
- `docs/agent/bugs/F78.md`
- `docs/agent/bugs/F80.md`
- `docs/agent/bugs/F82.md`
- `docs/agent/bugs/F85.md`
- `docs/agent/bugs/F86.md`
- `docs/agent/bugs/F97.md`
- `docs/agent/bugs/F99.md`
- `docs/agent/facts/EF-051.md`
- `docs/agent/prompts/C92_ACHIEVEMENT_BUILD.md`
- `docs/agent/prompts/CAPTURE_SITTING.md`
- `docs/agent/prompts/STANDDOWN_AUDIT.md`
- `docs/agent/prompts/fixtoggles/README.md`
- `docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md`
- `docs/agent/prompts/perma/LINUX_DISPATCH.md`
- `docs/agent/prompts/perma/STATE_EVICTION.md`
- `docs/agent/prompts/smrcf-verify/C35_DETECTOR.md`
- `docs/agent/reports/ARCHIVE_RECHECK.md`
- `docs/agent/reports/BETA_READINESS_REVIEW.md`
- `docs/agent/reports/C90_GUARDS_BUILD.md`
- `docs/agent/reports/C95_HABITAT_DRAFT_BUILD.md`
- `docs/agent/reports/CHECKLIST_ARCHIVE.md`
- `docs/agent/reports/D13_EXPOSED_SET.md`
- `docs/agent/reports/DOCS_FOR_THE_OWNER.md`
- `docs/agent/reports/DOCS_RESTRUCTURE_REPORT.md`
- `docs/agent/reports/DOC_OVERHAUL_AUDIT.md`
- `docs/agent/reports/DOC_RESTRUCTURE_SPEC.md`
- `docs/agent/reports/DOC_RULES_ARCHITECTURE.md`
- `docs/agent/reports/DOC_STRUCTURE_REVIEW.md`
- `docs/agent/reports/F105_BRIEF_RECONSTRUCTION.md`
- `docs/agent/reports/FR1_CACHE_ROUTE_2026-09-11.md`
- `docs/agent/reports/HAZARD_KERNEL_PASS.md`
- `docs/agent/reports/HOTFIX_1_AUDIT.md`
- `docs/agent/reports/L8_ADVERSARIAL_MAP.md`
- `docs/agent/reports/PACK_1_1_0_REVERIFICATION.md`
- `docs/agent/reports/PUBLIC_DOCS_DESIGN.md`
- `docs/agent/reports/REACHABILITY_AUDIT.md`
- `docs/agent/reports/REPAIR_PASS.md`
- `docs/agent/reports/RULES_HEADERS.md`
- `docs/agent/reports/SAVE_SAFETY_REDESIGN.md`
- `docs/agent/reports/SELFCHECK_PROMISE_AUDIT.md`
- `docs/agent/reports/SELFCHECK_PROMISE_COMBINED.md`
- `docs/agent/reports/SMRCF_COVERAGE_SWEEP.md`
- `docs/agent/reports/SMRTK_FANOUT_REPORT.md`
- `docs/agent/reports/STATE_DOOR_APPLICATION.md`
- `docs/agent/reports/STILL_NEEDED_SWEEP.md`
- `docs/agent/reports/WILDFIRE_CURE_RESEARCH.md`
- `docs/agent/reports/monoliths/C1_WORKFLOW.md`
- `docs/agent/reports/still-needed/90_SaveSanitizer.md`
- `docs/agent/reports/vanillahunt/SEAM_REPORT.md`
- `tools/doccheck.py`
- `zz-owner/CHECKLIST_PURGE_PROMPT.md`

## Found, not acted on

- PT-20 redo (08-14): a Mod-Manager disable takes effect only after a full process restart, but
  `docs/agent/WORKFLOW.md` ("98 vs 98"), `FIX_POLICY.md` and `facts/EF-002.md` still teach the older
  measurement. The correction now lives only in the archived tail and D13.
- 182's ruling to retire WORKFLOW's "Save-exit gates" release blocker was never carried out.
- 182 also noted that no standing prompt makes an agent scan existing saves for a fixture before asking
  the owner to build one.
- C89 leg B2's seat recipe (`C89-SEATS`) is not in `docs/agent/bugs/C89.md`; it survives only in the
  archived body of 158.
- Duplicate marker numbers 144, 157 and 188 (each used twice) are preserved as-is in the archive headings.
- `tools/doccheck.py` keeps the retired register code (marker_integrity, checklist_items,
  render_waiting, check_waiting) only for three selftests; a later cut can remove both together.
- Two near-miss facts from the peer analysis: `CheatStartMystery` writing `FinishedMysteries` into
  `account.dat` (unverified source claim), and SMRTK log records appearing twice except chrome verbs.
- `.claude/checklist_overhaul/` (local, untracked) holds the marker tables and the peer's triage notes
  this ledger leaned on; they are not in git.

