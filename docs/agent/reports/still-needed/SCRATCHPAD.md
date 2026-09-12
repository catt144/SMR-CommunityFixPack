# Coordinator scratchpad — resume here after compaction

User invoked `docs/agent/prompts/STILL_NEEDED_SWEEP.md` on 2026-09-12. All work
must be completed autonomously; long task and compactions explicitly anticipated.
User authorised game launches and TestKit firings and clarified only this team
is in the tree. Prompt explicitly requires one-module fan-out. No retirements,
code builds, public edits, uploads, or deployment in this sweep; verdicts to owner.
v9 (F59 repair/F60 retirement) stays separate. State is stale about metadata:
HEAD `2983fac` actually carries version 10/pdx_version 8; do not hand-set versions.

Persistent files:
- `../STILL_NEEDED_SWEEP_PROGRESS.md`: live checkboxes for every module and stage.
- `CENSUS.json`: 46-module queue, source/build/site pins, input and boot hashes,
  final runtime statuses with archived-log line numbers. Entries intentionally
  absent; front-matter `copies` is not a reliable module-to-entry map.
- `REVIEW_INSTRUCTIONS.md`: review contract shared by all agents.
- `BODYCHECK.txt`: captured complete check, 117 manifest rows, 112 OK, four SRC-NONE,
  one NO-DEFECT, two NO-MANIFEST (00_Core and sanitizer). Ten falsifiers passed.
- Per-module `.md` + `.json`: preserve agent-authored Markdown verbatim in commits.

Primary inputs: archived game `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`, Steam build
24995074 unchanged; EF-085 proves pack/source parity. Legacy tree 1.0.7.396349.
Site `C:/Dev/SMR-CommunityMods` HEAD `a061665` (49 rows), read-only this session.
Fresh boot `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log`,
SHA256 `fb36ba55fec6986c100d21ea736980c1e8e8ccbe29e59321d2d31b50a1490a56`.
All 46 logged; final 45 applied, Saint inactive; F102 applied; Saint save re-base
armed. Retail, both packs/TestKit enabled. No colony, suite, or screen witness.
First unarchived boot closed during data load; SECOND archived boot settled and
gracefully closed via CloseMainWindow/WM_QUIT. No forced termination.
Stale-probe gate CLEAN zero TEMPORARY hits before launching. No TestKit mutations.
First unsettled boot contains invalid SIE_ExporterValidity object message; settled
archived logs have opt-in transient NoHomeless/MultipleSuns diagnostics. RUNTIME
preserves the distinction; don't transfer diagnostic lines between launch logs.

Agent pool: module_a finished F102, now F51; module_b finished F54, now F58;
module_c finished Saint, now F52. Reuse idle agents
via followup_task for ONE module per task, until every census module has a JSON
and verbatim MD. No agent git/code/entry changes. Root can do useful whole-list
surface audit while agents review. Parent owns coverage checks, disputed-primary
review, synthesis, checklist 156, pending *after-v9* routing, docs validation/commits.
Do not infer completion from agent status: validate every module JSON and report.

Bindings read: STATE, CLAUDE/AGENTS, docs map, WORKFLOW authoring/probe/commit rules,
facts INDEX (92), FIX_POLICY incl owner who-benefits/branch guards, DISPATCH,
hotfix2 manifest/audit, migration report/audit, PUBLIC_SURFACE_SWEEP, RELEASE_OUTBOX.
Need whole-list surface audit: ~22 metadata bullets vs 49 fix-list rows, latent
claim THREE, judgment-call count THREE, LakeEntombment disabled-id example.
Existing migration F51/F58 narrowed, F52/F53/F73 partial, F59 repaired, F60 removed;
F54 was a gap, despite a previous table claiming STILL NEEDED. Don't redo hotfix2
36 retirements/10 recopies or known EF-078 inactive class; do consumer traces.

Git initial clean; a handoff edit appeared during orientation, owner now says
only our team present. Still exclude it from explicit-path commits. No regen
without checking entry status for drafts; archive log is gitignored, add -f.
Project standing authorisation includes commit/push (no publish); use explicit
paths and message file, agent name in commit body. doccheck green required.
Before final commit refresh hashes/HEAD/staleness; if inputs move re-review affected
rows. Update prompt lifecycle/map when completed; scratchpad/report stay in agent
reports. No archival records edited except adding new session/log records.
