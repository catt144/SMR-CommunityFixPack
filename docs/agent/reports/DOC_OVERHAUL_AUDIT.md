# Documentation overhaul audit

**Verdict: REFUTED — the loose ends are not tied.** The largest omission was
independent checks of the instruments that now authorize inheritance, hide owner
work, and certify packaging. Reducing reading before those checks are reliable
makes an incorrect answer cheaper to inherit.

Report only, 2026-09-13. No generator, policy, existing decision status, archive,
or shipped Lua was repaired. The task's explicit close-out exceptions cover
its retirement, its README row, and a new owner-decision item with the necessary
generated-register refresh. Recommendations needing a ruling are checklist 170.

## Anchor and scope

Starting command set: git status -sb; git log --oneline -1; git worktree list;
python tools/doccheck.py. Starting HEAD:
a94aa9fe325d0d0e9b6520229d9b4110d38f8dec, main tracking origin/main, clean,
one worktree. The overhaul window was inspected with git log --oneline
1a487c0..HEAD; interleaved defect implementation was excluded.

During the audit, 9f9e07c5c2965e46372c8d59aed7e4ea4955dab3 changed only
perma/HANDOFF_ORCHESTRATOR.md. Its full committed body was read again.
All checklist/source line numbers below refer to that HEAD, before this audit
adds its own checklist item. Mutation tests used an isolated git archive of
a94aa9f, not the shared checkout. The report was the live todo list throughout.

Baseline emitted lines, copied from python tools/doccheck.py:

    STATE + STUBS: STATE.md 11961 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
    WAITING: fresh — 122 checklist items, 43 marked, 4 waiting on the owner, 29 need a marker
    SKILLS: 2 skill(s), mirrored to .agents/skills/
        smr-bug-library           3685 B  ⚠ over the 3072 B target
        smr-orientation           3312 B  ⚠ over the 3072 B target
    TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
    PUSH SET: 43457 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
    doccheck: GREEN

These warnings predate this report. No STATE-size warning fired. Ordinary
migration-row warnings also remain; this audit does not change those entries.
Cross-vendor ListAgents was not callable in this harness. Git status and
sha/diff checks, not author identity, fenced writes.

R-G provenance: the current thread's JSONL turn_context records model
gpt-6-astra, effort max. The file was located with rg --files
C:/Users/stkot/.codex/sessions -g "*01a09b7b-5e19-7541-8c21-401711ebd7c1*.jsonl";
only turn_context payload.model/effort fields were reported, not an assumed
model name or another session's transcript.

## Completed audit todo

| Task item | Completion / verdict | Finding |
|---|---|---|
| 1 markers | [x] CONFIRMED lossy; seed's “older wins” mechanism refined | 2 |
| 2 obligation | [x] CONFIRMED stranded; vocabulary and defer flag unused | 2 |
| 3 reproduction | [x] CONFIRMED deterministic; REFUTED byte/correctness interpretation | 2 |
| 4 archive boundary | [x] CONFIRMED working and discoverable | 9 |
| 5 co-runs split | [x] CONFIRMED preserved tiers; REFUTED complete citation cleanup | 8 |
| 6 fingerprints | [x] CONFIRMED consumers; REFUTED safe general inheritance | 3 |
| 7 rails in force | [x] CONFIRMED adopted; REFUTED demonstrated integration into firing routes | 5 |
| 8 STATE | [x] REFUTED wholly kernel-shaped and content-only measurement | 6 |
| 9 decisions | [x] REFUTED agreement; both directions checked, limits below | 2 |
| 10 retirement | [x] REFUTED unreachable payloads | 5 |
| 11 package | [x] CONFIRMED next-pack exclusions/mirrors; REFUTED absent artifact and unexplained gap | 1, 7 |
| 12 archive script | [x] REFUTED safe implementation of D4; apply never run | 4 |
| 13 push budget | [x] REFUTED total as universal startup cost | 6 |
| §5 omitted scope | [x] CONFIRMED missing instrument falsifiers and reading-route audit | 1, 3, 6 |

Findings below are ranked by the cost of leaving them in place. Each verdict
names the proposition being judged; “CONFIRMED” never certifies the overhaul
as a whole.

## 1. CONFIRMED: instrument correctness was missing from the overhaul's scope

The register, fingerprints, archive cutter, and archive reader need controls
that can disagree with them. Re-rendering with the same implementation checks
consistency, not the truth of what gets rendered. The live packaging discrepancy
is a particularly concrete example: two tools agreeing was one parser agreeing
with itself.

The supposedly unavailable delivered artifact is present at:

    A:/SteamLibrary/steamapps/workshop/content/3215050/3787202810/ModContent.fpk

Commands that settled it:

    rg --files --hidden --no-ignore A:/SteamLibrary/steamapps -g "*ModContent*"
    python -X utf8 tools/pack_list.py A:/SteamLibrary/steamapps/workshop/content/3215050/3787202810/ModContent.fpk --names

Measured: 371,327 bytes; md5 bef42a2d5405e06444b7e6efdf28cf38;
mtime 2026-09-13 00:25:57 local. The upload-temp copy under
%LOCALAPPDATA%/Temp/Surviving Mars Relaunched/ModUpload/Pack has the same
size and md5. No download was required. The earlier absence claim cannot be
explained from this audit's evidence; its alleged search was not reproduced.

pack_list prints 56 names. A directory-record trace establishes that its
underlying flpk_extract.parse_table visits the SAME physical records twice:

| Record offset | Correct path | Invented second path |
|---|---|---|
| 2221 | .agents/skills/smr-orientation/SKILL.md | smr-orientation/SKILL.md |
| 2245 | .agents/skills/smr-bug-library/SKILL.md | smr-bug-library/SKILL.md |

The root directory arena is [32, 2269). The .agents table is [2137, 2159);
its skills table is [2159, 2221), followed by the leaf tables above.
parse_table's local skip list claims only immediate child-table spans.
After recursion, the root resumes inside a grandchild table and interprets
those descendants again under the wrong prefix.

A traversal that claims all descendant table spans yields 54 files. Their
names exactly equal the tracked-tree prediction at 1237454, with no missing
or additional name. Appendix B supplies the independent offset trace and a
synthetic falsifier: one nested leaf produces both a/b/x and x, while the
shallow control produces only a/x. Thus the extra “two entries” are a reader
defect. The two genuine .agents files were already in the old prediction,
as the audit prompt correctly cautioned.

Recommendation: give each instrument an adversarial fixture before using its
output to skip evidence. Fix nested table ownership in flpk_extract, then
recheck downstream listing/alias claims. An identical parser imported by
pack_list is useful reuse, not an independent control. Do not change packaging
to compensate for fictitious paths.

## 2. CONFIRMED: the owner register can erase obligations while GREEN

Settling commands: Appendix A; rg -n 'MARKER_STATUSES|MARKER_RE|CK_DEFER_RE|prose_defer'
tools/doccheck.py; git log --oneline -S 'ck:169 status:open' --
docs/PLAYTEST_CHECKLIST.md; the same command with status:part-ruled.

The raw-comment filter `<!-- ck:` finds 44 comments; MARKER_RE matches and
checklist_items consumes 43, across 122 headings. Line 33's part-ruled marker
does not match; line 71's open marker inside the historical details block does.
The register displays the obsolete upload ask at line 70. There is no
deduplication or “last wins” rule: both headings are parsed, and filtering
selects the obsolete one. Duplicate parsed IDs are 169, 157, 144, 99, and 98.
Some are historical headings; 99 is also a link number misread as a decision
identity. The parser likewise reads the “12 KiB” heading as item 12 rather
than item 126. Marker identity is parsed but not used as the displayed ID.

All following isolated mutations completed the REAL
python tools/doccheck.py --regen-waiting with exit 0, WAITING: fresh,
and doccheck: GREEN:

| Input/control | Result |
|---|---|
| Original sources, regenerate, restore | Same register bytes at both endpoints |
| Change historical 169 to closed / owner:no | Its decision row disappears |
| part-ruled beneath a RULED fixture heading | Marker ignored; item inferred closed |
| status:banana / owner:yes | Counted as marked; displayed nowhere |
| owner:maybe | Marker ignored; item inferred closed |
| Marker ck:391 under heading 390 | Displays decision 390 |
| Marker beyond the four-line window | Ignored without a diagnostic |
| ruled / owner:yes | Valid words, owner action displayed nowhere |
| Rename the decisions section | Zero items, zero waiting, still GREEN |
| Add a fenced example containing a level-two heading | Whole remaining section lost, still GREEN |

The last case occurs because section-end detection runs before fence handling.
Neither malformed markers nor missing sections must reach “needs a marker”;
the fallback can silently close them or consume no items at all.
MARKER_STATUSES has only its declaration. CK_DEFER_RE recognizes PART-RULED,
but its derived prose_defer flag also has no consumer. The orchestrator's
explanation of inconsistent vocabularies is supported; “the fallback honours
it” is too strong.

Lifecycle documentation search, with no truncated output:

    rg -n --glob "*.md" --glob "!DOC_OVERHAUL_AUDIT.md" "updating its marker" docs .claude/skills .agents/skills CLAUDE.md AGENTS.md

Only HANDOFF_ORCHESTRATOR:119 supplies the obligation at 9f9e07c. The register
banner does tell readers to change sources and regenerate, so the obligation
is not literally absent from every live surface; what is missing is the
writer's mandatory status-change rule at the normal authoring entry points.
Recommendation: home it in WORKFLOW's owner-decision mirroring rule, validate
syntax, placement, IDs and vocabulary, and give every source item an explicit
included/excluded/error disposition. Decide partial-status semantics before
changing existing markers. owner:yes needs explicit treatment independently
of whether the decision itself is ruled.

### Reproducibility and the orchestrator's confound

Baseline and restoration were byte-identical, but check_waiting compares text
after universal-newline decoding. Replacing the register's CRLFs with LFs still
reports fresh; regeneration changes those bytes back. Therefore “byte for
byte” is not the check's contract.

Marker provenance is confirmed: beb940e added open; 1237454 added part-ruled
and retained the older marker. The audit's fixed a94aa9f snapshot is later
than bf2d75f and unaffected by a peer regenerating during the tests.

The specific relay claim “1b7d695 left the register genuinely stale” was
REFUTED for committed trees: replaying the checklist, STATE and register blobs
at 1b7d695^, 1b7d695, and bf2d75f through check_waiting reports fresh at each.
git show --format= --name-only 1b7d695 lists only C92.md and bugs/INDEX.md;
neither is a register input. bf2d75f did change the register alongside its
STATE edits. This does not exclude transient uncommitted staleness; it does
exclude attributing this audit's result to self-healing or the C92 commit.

### STATE versus checklist, both directions

The historical replay also compared the ASTs of all register parsing,
classification, rendering and checking functions at those commits with
a94aa9f: they are identical. The fresh results are not an artifact of applying
a later parser to an earlier tree.

Settling command/filter: classify_items(checklist_items()), then inspect each
STATE-owed item and every unmarked heading; search item bodies for current
rulings, open subparts and numbered decisions, rather than treating header
keywords as adjudications. state_owed_numbers emits [47, 53, 133, 144, 151, 152].

| ID | Comparison and recommendation |
|---|---|
| 47 | STATE asks for wordings; header and marker say ruled/no owner, and body :6249 says both wording choices were ruled and applied. Separate site review/commit follow-through is mentioned at :6272 and current 169. Preserve that distinction; do not re-ask the wording choices. |
| 53 | Body :5757 and :5789 retains hardening row 3 for the owner. Its inclusion is supported, but “six rows go, one survives” needs to remain attached to the actual residual. |
| 133 | STATE and header still ask for (2)/(4). Body :2825/:2827 records both ruled under ck166 and landed; removal of the stranded pilot remains a separate recommendation. The header-only conflict flag misses this. |
| 144 | Decision (b) is closed; body :2224 explicitly moves (a)'s boot obligation to STATE. Its absence from Decisions is correct because the boot is reproduced in Owed playtest legs. Duplicated headings do not by themselves prove a lost boot. |
| 151 | (b)/(c) are stated open in body :1509 and represented by the parent ID. Messaging (b) remains pull-only; no new nudge is warranted. A parent row cannot express the differing action/deferral conditions. |
| 152 | STATE still lists (c); header, marker and body :1325 explicitly close it as design. The requested decisions are settled in the checklist. |
| 169 (reverse) | Present as an owed register row but discharged in STATE. The current body itself retains an obsolete FAQ ask beneath its completion receipt. Treat as a source contradiction, not an upload task. |

Reverse-scan qualifications: 148 is explicitly deferred and still named in
STATE's Now section; it is absent from the literal open enumeration but not
lost. 131's bench question survives in a LANDED heading, which the generator
silently closes; git log identifies dffa062 as the later “promote” ruling.
125's apparent open header is answered in its body; 111/112/113 similarly
retain older headings over recorded rulings. 157 is off the owed list under
the pull-only ruling, despite two “needs marker” rows. 83 explicitly says not
owed; 88 is overtaken by deferred 148; 87's remaining design work belongs to
the opt-in lane. The old 98 rig heading contradicts the other ruled 98 record
and current no-branch-install state; this is not evidence to revive that task.

No additional present fix-pack owner decision was proved omitted from STATE
by this reverse pass. This is not certification of all historical bodies:
Save Rescue's conditional 17/28 work and other-repo obligations were not
re-adjudicated. Their missing/ambiguous register representation remains a
coverage limit. Existing owner statuses were not changed.

## 3. REFUTED: a matching fingerprint generally licenses inheritance

Commands: python tools/doccheck.py --emit-fingerprint; inspect
emit_fingerprints at tools/doccheck.py:684; Appendix A's missing-pin control;
read EF-076's header/body and the live skill consumers.

The emitter groups 92 facts, all pinned, with 90 pins explicitly inferred.
Installed build 24995074 yields 17 game facts labelled HOLDS (16 inferred),
55 old-game facts MOVED, and 20 repository facts collapsed to commit-age
counts. No source-path dependency diff is performed for the repository group.

A real counterexample to “HOLDS means no re-read”: EF-076 is in the HOLDS
group although it describes the then-current mod target set, and its own
summary says its prediction was superseded by a contradictory runtime
measurement. Its game build alone cannot validate a changing mod inventory
or revive a withdrawn prediction. EF-015's later updated date likewise does
not establish that its older mod-code observation was re-measured.

Additional controls: removing EF-015's derived_at field leaves ordinary
doccheck GREEN; substituting installed_build = '2499507' still matches the
24995074 group because the implementation uses substring membership.
Even valid exact build equality establishes build identity, not the truth,
scope, or source dependencies of every sentence in that group.

The “no live consumer” suspicion is REFUTED: both skills explicitly tell a
working session to emit fingerprints and inherit behind HOLDS. That makes
the overstatement consequential.

Recommendation: give a fact its actual dependency set and evidence scope;
separate build identity, inferred dating, source-change status, and validated
claims. Until then, make the output a routing aid, not permission to skip
the evidence. Repository age alone is not a staleness test.

## 4. REFUTED: archive_settled implements D4 safely

Commands: python -X utf8 .claude/tools/archive_settled.py (DRY RUN ONLY);
compare its is_archive_old membership with the ARCHIVE-OLD section of
.claude/CHECKLIST_MOVE_MANIFEST.md; inspect the apply tail :478-508.
The script's sha256 was
b21f85847a7023d1a8d487fc80022d09cf86bc0bf3e0fe10e97637d4067405b9.

The manifest has 17 members; the script has 18. Exact header-set subtraction
finds just the Steam-ID/history item at checklist :8509, which the original
manifest classed LIVE. Its body :8511 actually records the owner's LEAVE IT
ruling, but that does not silently add it to D4's approved membership.
This is classifier drift, not a new item. More decisively, ARCHIVE-OLD is
report-only in the script and can never enter move_items. --apply therefore
cannot execute D4 as ruled.

The current dry run emits 42 candidates, 15 movable bodies, 41,568 bytes
removed; 730,376 = 688,808 + 41,568 balances. Among MOVE are 163 and 166.
The original protection depended on their numbers staying in STATE/perma;
the kernel eviction removes those incidental pins. A count from the earlier
dry run is not a durable approval of today's move set.

Other apply-path gaps, established by inspection rather than executing it:

- Git-clean is checked after bytes were captured. A peer commit can leave
  git clean while making those bytes obsolete; no HEAD/content comparison
  protects against overwriting that commit.
- Archive and checklist replacements are individually atomic, not a
  transaction. Failure between them leaves a partial move.
- The header-count “invariant” only prints the before count. It does not
  compare a constructed after count.
- The tally proves conservation of removed byte lengths, not correct
  selection, rule retention, or usable archive navigation.
- It leaves a header/marker without adding an archive-body link, and does
  not regenerate the line-addressed owner register or run a final doccheck.
- One EOL delimiter is selected for the whole file, unlike doccheck's
  universal-newline parser; mixed EOLs are not guarded.
- The ordinary PowerShell invocation failed during dry-run reporting with
  UnicodeEncodeError; -X utf8 allowed the dry run to finish.

Recommendation: do not use --apply. Bind any future implementation to reviewed
members, retain body locations explicitly, and validate the complete
two-file result plus register before replacing anything. Execute the existing
D4 membership only; any expansion needs its own owner decision.

## 5. CONFIRMED: adopted rules and retirement notices do not reach every firing path

Settling searches (exclude this audit from self-created hits):

    rg -n --glob "*.md" --glob "!DOC_OVERHAUL_AUDIT.md" "\bR-[A-G]\b" docs .claude/skills .agents/skills CLAUDE.md AGENTS.md
    rg -n --hidden --glob "*.md" --glob "!DOC_OVERHAUL_AUDIT.md" --glob "!docs/archive/**" "REPORTS_CUT_LIST|IMPLEMENT_PROMPT|SELFCHECK_PILOT|MOVE_CANDIDATES_57" docs .claude

Every named R-A through R-G hit is in WORKFLOW's rails section. The live
DLC_DEEP_CHECK route loads CHAIN_METHOD, whose opening sends authors to
WORKFLOW elements 1–7. fixtoggles names elements 1–8. Element 9 and the
rails follow elsewhere. The skills reach R-A's fingerprint behavior but do
not wire the full rail set into those authors/legs.

Thus adoption is established; systematic application is not. Do not claim
nobody could read WORKFLOW whole. That possibility is not a declared route.
Also reconcile CHAIN_METHOD's mandatory re-derivation framing with R-A/R-C
inheritance, and R-D's author-only depth instructions with a worker reading
the whole policy. The owner adopted these rails; resolving their operating
scope belongs with the owner.

Retirement audit:

| Artifact | Live route / verdict |
|---|---|
| REPORTS_CUT_LIST / old report-move batch | No affirmative firing route found in tracked live docs outside this audit. But BLUEPRINT's sequencing, BATCH_A_BRIEF and FRESH_SESSION_PROMPT still direct it in ignored local material. REPORT_MOVES_VERDICT:95/110 and HANDOFF_PROMPT retire it. This is conflicting local topology, not complete retirement. |
| IMPLEMENT_PROMPT | Its own opening still says “Fire with”; PLAN_TODO:160 still says Fire in an older section. No internal spent/do-not-fire banner. |
| SELFCHECK_PILOT | STATE and prompt README say unreachable; the payload still instructs a real boot and prototype, and SELFCHECK_PROMISE_COMBINED:98 still routes there. Removal remains a recommendation awaiting the owner. |
| HANDOFF_ORCHESTRATOR | At 9f9e07c it still has sole-home marker instructions and other residue despite a fired removal condition. Its removal cannot safely be treated as routine consumption yet. |

Recommendation: put retirement at the executable entry, remove affirmative
firing routes, and route authors to the adopted rails explicitly. Do not
reactivate the report-move batch or delete the pilot during this audit.

## 6. REFUTED: the push total is universal startup cost or content-only measurement

Commands: python tools/doccheck.py; Appendix C; read the opening and Read first
sections of GENERAL_USE_PROMPT and DISPATCH; apply STATE_EVICTION's admission
test to each H-line.

The current total is 43,457 bytes against 40,960. All measured push files
currently have zero CR bytes. This rules out CRLF as the reason for THIS
overage, not the intermittent defect.

The instrument sums GENERAL_USE (sittings only), DISPATCH (non-sittings,
switch to the dedicated task when one exists), and Claude-local MEMORY.
They are not all automatically loaded into every Codex or Claude task.
Conversely it omits the skills when invoked, the 7,179-byte owner register,
and the 95,497 bytes of indices both standing prompts instruct sessions to
scan. Those index scans alone exceed the nominal push budget. The local
Codex entry + mandatory STATE + orientation skill total is 17,779 bytes;
this is a file-route measurement, not a claim about all system/tool context.
Do not double-charge both vendors' identical skill copies to one session.

The checklist is 730,376 bytes, with 682,235 in the decision section before
“Do first” at line 9054. Merely making a register “fresh” has not made this
reading route effective, particularly while its links and statuses are weak.

Two independent budget/procedure failures:

- A scratch STATE with 200 ASCII content bytes plus LF passes; the same
  content plus CRLF fails its per-line cap (201 measured line bytes).
  .gitattributes cannot govern arbitrary writer output.
- STATE_EVICTION:48 contains U+0001 where the sed replacement should extract
  the decision ID. Running its actual expression outputs four U+0001 lines,
  not 169/151/133/53. A same-size substitution of one owed ID for another
  is invisible to that advertised set check. The report-count comparison
  cannot rescue it.

Hazards, individually, against “action + rail + detail pointer”:

| Hazard | Admission result |
|---|---|
| H-01 | Pass: unattended tag movement, prohibition, ck57. |
| H-02 | Rail/exception belong; save-engine explanation is derivation and can move behind ck71/75. |
| H-03 | Pass: portal call prohibition with source and safe route. |
| H-04 | Action/rail present; no specific detail pointer. |
| H-05 | Pass: unattended sweep-verdict consumption and named fence. |
| H-06 | Pass: pre-copy autosaves, EF-056. |
| H-07 | Pass: opt-in restoration prohibition, parked-reference report. |
| H-08 | Rail and same-ID exception belong; current opt-in-state story/derivation can move behind EF-055/ck43. |
| H-09 | Pass: parallel packed folder prohibition, source pointer. |
| H-10 | Rail belongs; SaveDef/upload explanation is derivation behind ck46. |

Recommendation: keep the existing caps while pricing actual reading routes
per harness/task, replacing mandatory full-index scans with targeted lookup.
If the owner approves normalized byte measurement, use one LF-normalization
helper consistently for total/per-line measurements and test threshold
boundaries. This is a bounded tooling change; it requires no cap increase
or mass re-eviction. Repair the eviction set extractor and test a replacement
ID, not merely an empty set.

The local evidence supports avoidable reading and faulty certification.
It does NOT establish that read cost is this repo's binding constraint:
no local throughput comparison was made against the still-unrun attended
boot, rework caused by false controls, or authoring churn. Sister-repo
multipliers were not re-measured or treated as local evidence. A small sample
of real task routes, owner minutes, and correctness/rework outcomes would
test that premise more usefully than another corpus-size cut.

## 7. CONFIRMED: skill exclusion/mirroring works; an unrelated root file still ships

Commands: python tools/pack_predict.py . --json; extract metadata.lua's
ignore_files array and compare it with pack_predict.IGNORE; byte-compare
each .claude/skills/*/SKILL.md to its .agents counterpart.

Current model: 52 files; 47 Code files and root .rgignore, LICENSE,
items.lua, metadata.lua, preview.png. All 14 ignore patterns agree with
metadata. Both skill pairs are byte-identical; both .agents paths are
excluded by the current next-pack model. This is not a claim that the
already-delivered v10 artifact retroactively changed.

.rgignore is the unasked root payload addition. The exclusion list is
duplicated in code and metadata without a parity gate, although it agrees
today. The historic mismatch was the parser defect in finding 1, not a
second demonstrated predictor defect.

Recommendation: exclude .rgignore if there is no player use, add ignore-list
parity checking, and validate the next actual archive with the corrected
reader. No new upload or repack is needed to establish this audit finding.

## 8. CONFIRMED: the split preserved tiers; citation cleanup was incomplete

Commands: compare the span from **Sign-off tiers:** to ## Release steps in
git show d56293a^:docs/agent/WORKFLOW.md and the current file, normalizing EOL;
rg -n --glob "*.md" "CO_RUNS.md|WORKFLOW.*Co-runs" docs, plus adjacent-line
inspection of WORKFLOW/CO_RUNS citations.

The sign-off body is identical, including the owner's 2026-08-04 adoption
and standing-policy wording. C44:108 cites the log-review rule that did not
move; it was never a control for the relocated protocol.

Stale protocol citations include checklist:8880, EF-051:43,
F11:187/:250, DOC_STRUCTURE_REVIEW:107, and CHAIN_METHOD:122/:124/:126/:128.
The last is a reusable authoring playbook, so it matters more than a dated
record. PLAYTEST_HELP:615, the checklist convention at :9014, and
COMBINED_SITTING:29 correctly point at CO_RUNS. No citation checked directs a
tier rule to CO_RUNS; CO_RUNS explicitly leaves the tiers in WORKFLOW.

Recommendation: update reusable authoring/procedure citations first. The
remaining WORKFLOW move pointer preserves reachability, so this is an extra
hop and misleading citation rather than a lost rule. Do not rewrite archived
records or use this as a reason to re-audit their verdicts.

## 9. CONFIRMED: the archive boundary is discoverable

An existing archive-only line was chosen and searched without a path:

    written and are NOT maintained — the current state lives in [the old STATUS path]

For an exact replay, obtain the line containing “written and are NOT maintained”
from docs/archive/SESSION_LOG.md and pass that complete line as the literal
pattern to rg -l -F with NO path, then with docs/archive/, then git grep -l -F.
The audit's default search returned exit 1 and no files; both deliberate
searches returned only docs/archive/SESSION_LOG.md.

A complete filename census using rg --files docs, selecting Markdown and
excluding DOC_OVERHAUL_AUDIT.md, found 163 documents mentioning docs/archive/;
161 lacked .rgignore or a default-rg explanation (the explainers were the map
and handoff). That count is not evidence of a discovery failure. CLAUDE.md,
its generated AGENTS copy, and the orientation skill teach the boundary and
escape forms before the normal session search. The owner rider is satisfied.

Recommendation: retain those entry-point explanations. Repeating them in
every dated report or entry is NOT WORTH AUDITING/implementing; it increases
the cost this overhaul meant to reduce.

One adjacent contract drift remains: rg -n 'six|WAITING_ON_YOU|Folder contract'
CLAUDE.md docs/README.md finds CLAUDE:8 still restricting the root to its old
human-file list while README:20 admits the new register. Synchronize that
entry-file contract with the adopted map in the follow-up; the generated
AGENTS mirror currently reproduces the omission faithfully.

## Not opened / limits

- No retail launch, portal call, publication, code fix, archive apply, owner
  status flip, or change to the source archives was attempted.
- The nested-parser defect may affect earlier FLPK alias/count claims such as
  EF-085. Those pack-wide results were not re-derived here. Their evidence
  dependencies warrant a separate tool-correction/revalidation task; this
  report does not retract byte-parity claims it has not tested.
- No full economic transcript census or causal time-cost study was made.
  The universal push claim is refuted by the live reading instructions;
  a numeric local depth multiplier is not established.
- Historical conditional asks in other repos, especially Save Rescue 17/28,
  were not re-adjudicated. “Not proved owed now” does not mean “closed.”
- Source completeness of every individual engine fact and the old row_status
  migration were not re-audited. The fingerprint contract itself was tested.
- Forbidden economics/cut-list/sweep files were searched only for relevant
  strings or membership; excluded whole-file reports and sweep verdicts
  were not used to certify game behavior.
- Ignored planning files are local claims. The ARCHIVE-OLD manifest sha256 was
  08f5f3e1e8ad70b0c86a13ac4f23b39ba6a126125b6275d3beacc20144cb5cc8.
  It is not a committed authority or a substitute for the owner's ruling.

## Reproduction appendix

Run the Python blocks from the repository root in a UTF-8 Python session.
They write only under a fresh system temporary directory. They do not run
archive_settled --apply. Ordinary command/filter citations above are the
cheaper first route for non-mutation findings.

### A. Register and fingerprint controls

    import io, zipfile, tempfile, pathlib, subprocess, sys, re
    rev = "a94aa9fe325d0d0e9b6520229d9b4110d38f8dec"
    root = pathlib.Path(tempfile.mkdtemp(prefix="smr-audit-replay-"))
    blob = subprocess.check_output(["git", "archive", "--format=zip", rev])
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        archive.extractall(root)
    sys.path.insert(0, str(root / "tools"))
    import doccheck as d
    cp, wp = pathlib.Path(d.CHECKLIST), pathlib.Path(d.WAITING_MD)
    source, register = cp.read_bytes(), wp.read_bytes()
    items = d.classify_items(d.checklist_items())
    comments = [l for l in source.decode().splitlines() if "<!-- ck:" in l]
    print("raw/matched/consumed/items", len(comments),
          sum(bool(d.MARKER_RE.search(l)) for l in comments),
          sum(i["source"] == "marker" for i in items), len(items))
    def run(label, data):
        cp.write_bytes(data)
        p = subprocess.run(
            [sys.executable, "-X", "utf8", str(root/"tools/doccheck.py"),
             "--regen-waiting"], cwd=root, capture_output=True)
        lines = p.stdout.decode("utf-8").splitlines()
        print(label, p.returncode,
              [l for l in lines if l.startswith(("WAITING:", "doccheck:"))])
        return wp.read_bytes()
    try:
        print("baseline bytes equal", run("baseline", source) == register)
        data = source.replace(b"ck:169 status:open owner:yes",
                              b"ck:169 status:closed owner:no")
        print("169 absent", b"| 169 |" not in run("closed", data))
        markers = {
            "hyphen": "<!-- ck:390 status:part-ruled owner:yes -->",
            "unknown": "<!-- ck:390 status:banana owner:yes -->",
            "bad-owner": "<!-- ck:390 status:open owner:maybe -->",
            "wrong-id": "<!-- ck:391 status:open owner:yes -->",
            "late": "\n\n\n\n<!-- ck:390 status:open owner:yes -->",
            "ruled-action": "<!-- ck:390 status:ruled owner:yes -->",
        }
        key = b"## Decisions waiting on you"
        for label, marker in markers.items():
            item = "\n### AUDIT_CASE 390 RULED 2026-09-13\n"+marker+"\n\n"
            run(label, source.replace(key, key+item.encode(), 1))
        run("missing-section", source.replace(key, b"## Decisions archive", 1))
        fence = (chr(96)*3).encode()
        run("fenced-section", source.replace(
            key, key+b"\n"+fence+b"\n## EXAMPLE\n"+fence+b"\n", 1))
    finally:
        print("restored bytes equal", run("restored", source) == register)
    lf = register.replace(b"\r\n", b"\n")
    wp.write_bytes(lf)
    out = []
    print("LF still fresh", d.check_waiting(out), out)
    d.regen_waiting([])
    print("regen changed LF bytes", wp.read_bytes() != lf)
    wp.write_bytes(register)
    fact = root/"docs/agent/facts/EF-015.md"
    raw = fact.read_bytes()
    try:
        fact.write_bytes(re.sub(rb"^derived_at:.*\r?\n", b"", raw, flags=re.M))
        p = subprocess.run([sys.executable, str(root/"tools/doccheck.py")],
                           cwd=root, capture_output=True)
        print("missing pin", p.returncode,
              p.stdout.decode("utf-8").splitlines()[-1])
    finally:
        fact.write_bytes(raw)
    d.installed_build = lambda: "2499507"
    out = []
    d.emit_fingerprints(out)
    print("prefix control", [l for l in out if "24995074" in l])

### B. Independent archive-record falsifier

    import pathlib, sys, struct, collections
    sys.path.insert(0, str(pathlib.Path("tools").resolve()))
    import flpk_extract as fx
    def record(name, flag, offset, size):
        name = name.encode()
        return (struct.pack("<III", offset, flag<<16 | len(name)<<24, size)
                + name + struct.pack("<I", 0))
    unit = len(record("a", 1, 0, 0))
    leaf = record("x", 16, 999, 1)
    nested = record("a", 1, unit, unit) + record("b", 1, unit*2, len(leaf)) + leaf
    shallow = record("a", 1, unit, len(leaf)) + leaf
    for label, buf in [("nested: expect a/b/x only", nested),
                       ("shallow: expect a/x only", shallow)]:
        out = []
        fx.parse_table(buf, 0, len(buf), 0, "", out)
        print(label, [f[0] for f in out])
    path = pathlib.Path(
        "A:/SteamLibrary/steamapps/workshop/content/3215050/3787202810/ModContent.fpk")
    buf = path.read_bytes()
    base, size = struct.unpack_from("<I", buf, 12)[0], struct.unpack_from("<I", buf, 20)[0]
    visits = collections.defaultdict(list)
    def trace(start, size, prefix):
        at, end, skip = start, start+size, []
        while at+12 <= end:
            if any(a <= at < b for a,b in skip):
                at += 1
                continue
            off, packed, n = struct.unpack_from("<III", buf, at)
            flag, length = (packed>>16)&255, packed>>24
            if packed & 65535 or not length:
                break
            name = buf[at+12:at+12+length].decode("utf-8")
            visits[at].append((prefix+name, flag))
            if flag == 1:
                skip.append((base+off, base+off+n))
                trace(base+off, n, prefix+name+"/")
            at += 16+length
    trace(base, size, "")
    files = {at:names for at,names in visits.items() if names[0][1] != 1}
    print("emitted / unique physical file records",
          sum(len(v) for v in files.values()), len(files))
    print("duplicate file records", {k:v for k,v in files.items() if len(v)>1})

### C. Byte measurements and the eviction command

    import pathlib, sys, re, subprocess
    sys.path.insert(0, str(pathlib.Path("tools").resolve()))
    import doccheck as d
    for label, resolve in d.PUSH_SET:
        path = pathlib.Path(resolve())
        if path.exists():
            raw = path.read_bytes()
            print(label, "raw", len(raw), "CR", raw.count(b"\r"),
                  "normalized", len(raw.replace(b"\r\n", b"\n")))
    for name in ["docs/WAITING_ON_YOU.md", "docs/PLAYTEST_CHECKLIST.md",
                 "docs/agent/bugs/INDEX.md", "docs/agent/facts/INDEX.md",
                 ".agents/skills/smr-orientation/SKILL.md",
                 ".agents/skills/smr-bug-library/SKILL.md"]:
        print(name, pathlib.Path(name).stat().st_size)
    text = pathlib.Path("docs/agent/prompts/perma/STATE_EVICTION.md").read_text(
        encoding="utf-8")
    line = next(l for l in text.splitlines() if "sed -n" in l)
    expression = re.search("sed -n '([^']+)'", line).group(1)
    p = subprocess.run(["C:/Program Files/Git/usr/bin/sed.exe", "-n",
                        expression, "docs/WAITING_ON_YOU.md"], capture_output=True)
    print("actual expression", repr(expression), "output", repr(p.stdout),
          "exit", p.returncode)

## Close-out

The report's reproduction appendices A, B and C were executed from their
stored text; each exited 0 and reproduced the stated controls. After the
checklist-only addition, python tools/doccheck.py --regen-waiting reported
WAITING: fresh — 123 checklist items, 44 marked, 5 waiting on the owner,
29 need a marker, and doccheck: GREEN. Existing erroneous rows remain
untouched; freshness is not used here as evidence that they are correct.

All requested audit areas have a result or an explicit limit above. Owner
choices are mirrored in checklist 170 with a marker. The one-off prompt is
retired in its README row and deleted in the report's commit; git is its grave.
Required validation and diff-stat are recorded in the close-out commit/tool
output. No load-bearing finding is left solely in the conversation.
