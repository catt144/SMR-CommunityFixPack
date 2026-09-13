# CK170 and fingerprint provenance — 2026-09-13

## Phase 1 — owner rulings implemented

Anchor: `5b807be`, clean checkout, doccheck GREEN. Executed model: GPT-6
(session developer identity; no more specific executed model identifier exposed).
Owner authority: the fired `CK170_AND_FINGERPRINTS.md` brief records the rulings;
this pass did not re-adjudicate them. Checklist 170 now says `ruled owner:no`.

### Measurements, separated by change

MEASURED with `python tools/doccheck.py | Select-String
'MARKER|duplicate|PUSH SET|STATE \+ STUBS|^doccheck'`, at the anchor and then
after each working-tree change, in the order below:

| stage | marker integrity | push set | STATE |
|---|---|---|---|
| before | 46 on disk, 45 parsed; WARN | 42199 B | 10388 B |
| (a) marker repair only | 46 on disk, 46 parsed; WARN | 42199 B | 10388 B |
| (b) LF accounting only | 46 on disk, 46 parsed; WARN | 42199 B | 10388 B |
| (c) reading routes | 46 on disk, 46 parsed; WARN | 42517 B | 10388 B |

All runs ended `doccheck: GREEN`. The matching ck144 duplicate is deliberately
WARN; the recorded ruling does not authorize renumbering. Current warning:

```
  warn duplicate ck:144 at lines 2269, 2343 (agree)
PUSH SET: 42517 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
```

(a) `tools/doccheck.py` rejects unknown vocabulary, malformed ck comments and
disagreeing duplicate status/owner pairs. The main gate consumes its Boolean
result. ck169's current marker uses legal `open owner:yes`; its historical marker
uses `ck:-`. Its current heading now agrees with its existing FAQ-discharge body.
The old heading is a subsection: **changing its marker alone does not exclude a
historical ask**, because the register selects decision-level headings. Verify:
`rg -n '^\| 169 |^\| 170 ' docs/WAITING_ON_YOU.md`.
The register now selects `owner:yes` independently of decision status: a settled
decision can still owe an action. A synthetic ruled/closed + owner:yes fixture
exposed the former status filter; live rows are unchanged by removing that filter.

(b) STATE total and per-line budgets, the push set and skill budgets count LF
content bytes. Byte-identity gates remain raw-byte comparisons. Caps and measured
document content are unchanged. The predicted line-ending saving did **not**
reproduce for the push set: those files already use LF. The skill-budget readings
did change: `smr-bug-library` 3685 → 3622 B and `smr-orientation` 3312 → 3248 B,
emitted by `python tools/doccheck.py` (filter `smr-bug-library|smr-orientation`),
with identical skill content and unchanged caps. `.gitattributes` keeps
the STATE pin but no longer describes raw-byte accounting as current behavior.

(c) DISPATCH and WORKFLOW now route index searches by task ID/keyword instead of
full scans. DISPATCH cites R-A/R-B/R-E/R-F/R-G at work/close-out and points brief
authors to R-C. WORKFLOW's required brief elements now include R-C and contain
the unchanged R-D body, moved out of the working verification section. Verify:
`rg -n 'R-[A-G]\b' docs/agent/prompts/perma/DISPATCH.md docs/agent/WORKFLOW.md`.
No additional skill text: both skills already route fingerprints, and duplicating
the labels there adds no reach beyond the dispatch/authoring routes.

### Falsifiers

`python tools/ck170_selftest.py` exercises deliberately broken **disk copies**:
unknown/hyphenated status, malformed identifier, unterminated comment, status
disagreement and owner disagreement all FAIL. Matching duplicates WARN. LF and
CRLF readings agree; real total/per-line overruns FAIL under both endings. A
reverted raw-byte measuring instrument FAILS the equivalence fixture. Restored
copies rerun the cases and print SHA256; the live file is asserted unchanged.
Skill caps also FAIL real overruns under both endings; their mirror gate still
rejects raw-byte drift. Owner-action fixtures cover every legal status and falsify
a reverted status filter. These added checks leave the live measurements unchanged.

`python tools/repair_pass_selftest.py` also passes, including its reverted
instrument falsifiers; its marker expectations were updated to the adopted gate.
`git diff --check` passes. Pre-test probe sweep:
`rg -n 'TEMPORARY' Code ../SMR-BugFixPack-TestKit/Code` returned no matches.

### Not done / scope limits

- ck169 still carries `owner:yes` as instructed. Its body and STATE contain later
  discharge information; this pass does not invent permission to close that item.
- No other owner status, game code, hazard or release artifact changed.
- No push-set eviction; the warning remains. No separate peer adjudication run.
- Phase 2 provenance audit is recorded below and committed separately.

## Phase 2 — recovered provenance, and a refuted reclamation premise

MEASURED: `python tools/fact_provenance.py --summary`, body history at
`e9f589d` (same fact tree as the original inventory's `f020bf3`):

```
FACT PROVENANCE: 93 facts; 81 inferred; 54 old-build inferred; 0 nonblank old-build body lines committed on/after 2026-09-08
```

The brief's premise that many of the inferred old-build facts were actually
derived on 1.1.0 **does not reproduce**. Their complete nonblank bodies predate
the update in Git, independently of `updated:`. This establishes that these are
older observations; it does **not** independently establish their exact original
game build, so their inferred pins remain. Nor does old provenance prove that a
behavior changed. No old fact was promoted to HOLDS on unchanged-looking code.

An exploratory full-file comparison found changed bytes in the source files for
the short sandbox, message-dispatch and label examples too. That is not a claim
that all their behaviors changed: for example `Lua/LabelContainer.lua` changes an
unrelated filtering method. Full source/dependency re-derivation would be new
work, not correction of an invented derivation date. Historical citations remain
unchanged. No inferred old-build fact had a recovered later derivation to file.

### Before/after routing

MEASURED with `python tools/doccheck.py --emit-fingerprint | Select-String
'FINGERPRINTS|fact\(s\)|route by|^doccheck'` before Phase 2, after the first
receipt corrections, then after the source/control and mixed-scope corrections:

| stage | old-build MOVED (inferred) | matching-build HOLDS (inferred) | repo (inferred) | mixed / no fingerprint |
|---|---|---|---|---|
| before | 55 (54) | 18 (16) | 20 (20) | — |
| archived/explicit receipts | 56 (54) | 20 (12) | 17 (17) | — |
| final | 56 (54) | 18 (8) | 17 (17) | 2 (2 inferred) |

Installed build read by each run: `24995074`. Every run: `doccheck: GREEN`.
MOVED grew because EF-049 was a game observation incorrectly filed under a repo
sha. EF-078/EF-087 gained a measured game-build pin; EF-015/EF-019 lost a
misleading whole-fact HOLDS. The net HOLDS count hides those opposite corrections.

### What established each changed pin

These are **provenance corrections**, not fresh tests or upgrades to the claims'
evidence status. `derivation_basis:` is recorded in each fact, alongside its pin.
The runtime receipts name `1.1.0.403908`; the original EF-075 observation and
EF-085's explicit ACF reading supply its recorded Steam identity. A game pin
does not pin historical mod contents, an old-branch control, or external state.

| fact | change | recovered evidence / one re-check |
|---|---|---|
| EF-015 | HOLDS → mixed, still inferred | `git show cd9b0948 -- docs/agent/facts/EF-015.md`: only the console-print exception was added in September; the retained July MOD-print claim explicitly was **not re-measured**. |
| EF-019 | HOLDS → mixed, still inferred | `git show d2e5414e -- docs/agent/facts/EF-019.md`: the September unpersisted-function extension does not re-derive the July persistence/RT-vs-GT observation preserved by `ef5d3142`. |
| EF-049 | inferred repo → explicit old game | `git show 0b22bc49:docs/agent/facts/EF-049.md`: the contemporaneous observation expressly identifies **retail 1.0.7.396349** for both ListForTag readings. This recovers the recorded build, not the unknown cause. |
| EF-078 | inferred repo → game | `rg -n 'Build version:' docs/archive/logs/first110_Mars.exe-20260908-15.20.28-6a91a190.log`: line 56 identifies the actual launch recorded by `c81e6f69`. Historical module counts remain historical. |
| EF-080 | same game, inference removed | `git show c81e6f69:docs/agent/facts/EF-080.md`: source observation identifies revision 403908 and floor 402200; the same commit's EF-078 launch receipt supplies the runtime version. The comparison uses old-save revision 396349. |
| EF-081 | same game, inference removed | `rg -n 'Build version:' docs/archive/logs/forced110_Mars.exe-20260908-15.43.37-6a91a190.log docs/archive/logs/unforced110_Mars.exe-20260908-15.57.09-6a91a190.log`: both line 54. Observations `ed2b17df`/`f4dc62ab`; override and mod-state dependencies remain. |
| EF-083 | same game, inference removed | `git show 42b9a17c:docs/agent/facts/EF-083.md`: the original two-tree observation explicitly records the owner's build **24995074** and digest **a4577da2…**, alongside the separate old control **23584660 / 09d95e34…**. Both source dependencies are retained in the new basis. |
| EF-085 | same game, inference removed | `git show 7f7d87a3:docs/agent/facts/EF-085.md`: the original measurement explicitly names the ACF `buildid 24995074` read and archived 1.1.0.403908 source digest. The extraction is not rerun or newly certified here. |
| EF-087 | inferred repo → game | `rg -n 'Build version:' docs/archive/c74build_initial_Mars.exe-20260910-16.20.36.log docs/archive/c74build_final_Mars.exe-20260910-16.47.24.log`: lines 55/53 identify both runs behind `0cfc53ae`. Scheduling explanation remains inferred. |
| EF-091 | same game, inference removed | `rg -n 'Build version:' docs/archive/logs/f119sitting110_Mars.exe-20260911-14.02.05-6a91a190.log`: line 53, original observation `5056a001`. No promotion of C-side claim arithmetic. |
| EF-092 | same game, inference removed | `git show 0f910faa:docs/agent/facts/EF-092.md`: original observation explicitly names **game 1.1.0.403908**. Archived Residence.lua:416-417 and Workplace.lua:1316-1327 still carry its validity chain; EF-085 supplies the source/build mapping. No new attended leg. |

### Instrument and limits

`tools/fact_provenance.py` is read-only and makes **no build classifications**.
It parses body boundaries, maps every body line using `git blame --line-porcelain`,
and refuses mismatched body/blame text. JSON preserves every line, original path,
commit, author date and committer date; summaries use the committer date and retain
the full body SHA256 and latest origin. The first instrument cut used author dates;
that was corrected before close-out because authorship need not be commit time.
Dates and version mentions are leads, never automatic evidence of a build.

`python tools/fact_provenance.py --selftest` passes fixtures for CRLF, a misleading
updated date, negated/new versus old version text, different blame dates on
adjacent lines, distinct author/committer dates, malformed front matter and
incomplete blame output. The fixture
runs before inventory output. `--summary` selects inferred pins and counts every
nonblank old-build line on/after the update, without a deduplication step.
`--inventory` emits all rows for independent review.

The source-body integrity check against `e9f589d` confirms that changes are
confined to `derived_at:` and `derivation_basis:`; regeneration leaves the indices
unchanged. No new source/runtime conclusion was inserted into a fact body.

### Not done

- No reduction of the original MOVED set: the proposed later derivations were not
  found. The inferred legacy pins below remain conservative, not declarations
  that the exact old build has independently been recovered.
- No full contemporary re-derivation, new colony, runtime boot, pack-parity run,
  Linux investigation, screenshot recovery or external portal action.
- No blanket upgrade of inferred repo pins to a migration commit: the commit that
  copied a fact is not necessarily the checkout used to establish it.
- Mixed facts retain their observations in place. No prose rewrite or invented
  common baseline conceals their different evidence scopes.
- No automatic future check of `derivation_basis:` semantics; it is a readable
  receipt. The fingerprint is still a routing aid, and source dependencies matter.

### Commit receipts

Phase 1: `e9f589d` (amended locally from `f020bf3` to include the owner-action
fixture and skill-budget falsifiers). `git show --stat e9f589d`:
`9 files changed, 354 insertions(+), 95 deletions(-)`.
Phase 2: `14dcaa9`. `git show --stat 14dcaa9`:
`14 files changed, 366 insertions(+), 156 deletions(-)`.
The consumed prompt is deleted in this commit. This receipt was added afterward
in a report-only close-out commit; no implementation or fact body changed there.

Independent control: the final pre-update snapshot `f7bd2882`
(`git log -1 --before=2026-09-08T00:00:00Z --format=%H`) contains all 54
inferred old-build bodies exactly as they are now. This compares entire bodies
from `git show <snapshot>:docs/agent/facts/<ID>.md`, excluding front matter,
not dates or selected citations. No body differed.

### Every fact left inferred

The table below is emitted from the complete provenance inventory, with an
individual disposition for every retained inferred pin. Origin means the latest
nonblank body-line commit, **not** a claimed derivation build. For the old group,
the absence of post-update body lines was counted across every member and every
line. The table is a historical audit receipt, not a new generated index.

| fact | latest body origin | why still inferred |
|---|---|---|
| EF-001 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-002 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-003 | `628ea4db` (2026-09-08) | September GameVar clarification supplements older advice; no independent whole-fact exact-build receipt recovered. |
| EF-004 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-005 | `ef5d3142` (2026-08-03) | Engine Lua dialect observation has no explicit game-build receipt; guessed repo sha does not establish it. |
| EF-006 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-007 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-008 | `6c714fea` (2026-08-19) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-009 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-010 | `ef5d3142` (2026-08-03) | Sandbox/debug observation lacks an exact-build measurement receipt; migration origin is not derivation. |
| EF-011 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-012 | `ef5d3142` (2026-08-03) | Command-wrapper behavior lacks an exact engine-build receipt; guessed repo date is insufficient. |
| EF-013 | `ef5d3142` (2026-08-03) | Registry behavior depends on the mod checkout; the actual derivation checkout is not identified by the migration. |
| EF-015 | `cd9b0948` (2026-09-10) | Mixed July MOD-print observation and September console exception; the latter explicitly did not re-measure the former. |
| EF-016 | `ef5d3142` (2026-08-03) | External samples/documentation layout lacks a recorded installation snapshot; repo date cannot pin it. |
| EF-017 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-018 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-019 | `d2e5414e` (2026-09-12) | Mixed July thread-persistence observation and September extension; no common build/checkout receipt. |
| EF-020 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-021 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-022 | `ef5d3142` (2026-08-03) | Persisted-closure experiment requires its game, mod and save state; exact joint provenance not recovered. |
| EF-023 | `689a3960` (2026-08-13) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-024 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-025 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-026 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-027 | `ef5d3142` (2026-08-03) | Engine serialization documentation and experimental interpretation lack an exact dependency snapshot. |
| EF-028 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-029 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-030 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-031 | `ef5d3142` (2026-08-03) | Thread-predicate observation lacks an explicit engine-build receipt; repo timestamp is insufficient. |
| EF-032 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-033 | `ef5d3142` (2026-08-03) | PowerShell encoding/tooling observation has no game baseline; a migration commit cannot identify the tested environment. |
| EF-034 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-035 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-036 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-037 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-038 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-039 | `4cc20f1c` (2026-08-21) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-040 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-041 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-042 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-043 | `ef5d3142` (2026-08-03) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-044 | `c3738cb4` (2026-08-04) | Explicitly compares retail and MarsDebug/TestKit configurations; no single fix-pack sha pins both. |
| EF-045 | `9a9475a8` (2026-08-04) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-046 | `93088ba5` (2026-08-04) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-047 | `0b22bc49` (2026-08-10) | Process-exit log-flush observation lacks an independently recovered exact-build receipt. |
| EF-048 | `0b22bc49` (2026-08-10) | Engine predicate-return measurements lack an explicit full engine-build receipt. |
| EF-050 | `ea81faaf` (2026-08-13) | Save naming/filesystem experiment requires runtime and filesystem context not pinned by the guessed repo sha. |
| EF-051 | `7698f91a` (2026-08-15) | Save/Steam Cloud history depends on external account and filesystem state; no single repo fingerprint established. |
| EF-052 | `a0c75bc2` (2026-08-12) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-053 | `c3bccd48` (2026-08-12) | Spawn/menu-route experiment depends on runtime state and source; precise original joint snapshot not recovered. |
| EF-054 | `3ff6d8ce` (2026-08-24) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-055 | `5c570353` (2026-08-20) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-056 | `68675521` (2026-08-13) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-057 | `fd1102a8` (2026-08-16) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-058 | `11f1ff5e` (2026-08-19) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-059 | `b2d710f2` (2026-08-16) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-060 | `b2d710f2` (2026-08-16) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-061 | `38606e82` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-062 | `38606e82` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-063 | `2d2cae1b` (2026-08-16) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-064 | `2d2cae1b` (2026-08-16) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-065 | `3ff6d8ce` (2026-08-24) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-066 | `e4caf551` (2026-08-24) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-067 | `223b0714` (2026-08-21) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-068 | `094693d9` (2026-08-29) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-069 | `0a4b02a3` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-070 | `3e224a7c` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-071 | `3e224a7c` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-072 | `3e224a7c` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-073 | `3e224a7c` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-074 | `f7bd2882` (2026-09-01) | Complete nonblank body predates the update; no later derivation or explicit original build receipt recovered. Keep legacy inference. |
| EF-076 | `c81e6f69` (2026-09-08) | Superseded source-sweep prediction also depends on the historical module list/tool; generic 1.1.0 label is not a complete receipt. |
| EF-077 | `66c16eb5` (2026-09-13) | Source floor plus repo metadata/UI-route claims; generic 1.1.0 label does not independently pin all dependencies. |
| EF-079 | `66c16eb5` (2026-09-13) | Old-save/new-game comparison and owner screenshot observations; complete original screenshot/build provenance not recovered. |
| EF-082 | `628ea4db` (2026-09-08) | Names 1.1.0 source but expressly leaves its 1.0.7 half unrechecked; retain weaker pin rather than imply whole-scope recovery. |
| EF-084 | `4e994d64` (2026-09-09) | Two-branch source comparison plus historical retirement state; retain inferred pin without independently pinning all source/repo dependencies. |
| EF-086 | `8b65f4e0` (2026-09-10) | Cited original 11.47.24 hammer run receipt was not found in the archive filename search; later C74 logs are different runs. |
| EF-088 | `df5af12b` (2026-09-11) | Linux options/shader/driver record spans multiple artifacts and corrections; no complete dependency fingerprint recovered; no FR-1 investigation run. |
| EF-089 | `df5af12b` (2026-09-11) | Linux renderer/cache record includes source, executable and driver dependencies; game label alone does not establish them all. |
| EF-090 | `9031634f` (2026-09-11) | Linux shader-cache/parser/driver record has separate binary and corrected measurement artifacts; no whole-record pin established. |
