# DESKBENCH_C90 — instrument repair and measured callback reach

Date: 2026-09-12. Executor: root Codex; bounded read-only census and fixture review by
`/root/c90_census`, independently re-read by root before recording. Baseline: `690a1ee`.
Task: `docs/agent/prompts/DESKBENCH_C90.md` (the supplied DESKBENCH/_C90.md path did not exist).
This is the complete handback, preserved as written for a fresh audit.

## Outcome and landing boundary

**MEASURED:** the migration instrument is repaired: all **16/16** pre-existing demands still hold.
F60 reads its actual pre-retirement body from `9bc4360^:Code/Fix_DomeFreeSpaceMismatch.lua`.
Its two harmful outcomes remain demonstrable, despite the module's retirement from the live pack.
The three F51 demands and every other demand are unchanged; the diff adds a named revision and passes
it to the existing module loader. Before repair, the full bench had exactly the known migration REFUTED row.
After leg 1, all 19 original harnesses held. Leg 2 started only after that green run.

**MEASURED:** C90 control **18/18**; eight external scratch variants **all FAILED as required**,
collectively falsifying every added demand. Final deskbench: **20/20 harnesses HELD**, **254/254**
numbered demands across 17 harnesses. Three harnesses emit unnumbered checks, so 254 is not a count of
every assertion executed. Those three are desk_caller_seam.py, desk_progress_seam.py and desk_seam_food.py.

**SOURCE / unchanged boundary:** no Code/*.lua, items.lua, metadata.lua or TestKit file changed.
No game launched. No C90 fix landed. C90 remains cand; the owner decision remains in checklist 158.

## 2a — what happens before a missing target is used

The fixture removes one Require target before loading the whole module. Actual Register and Require
record the decline; actual ClassesBuilt callbacks then run. The whole real core supplies DataPatch,
ctx.heal, WhenActive, logging and UpdateSuspects. This replaces the k2 template's stubbed orchestration,
because those status transitions are precisely what must be measured.

| Removal | Ordered writes / first missing-target use | Verdict |
|---|---|---|
| Saint GetTraitLabel, both branches | No preset writes; pass's explicit function check returns at Fix_SaintBlessing.lua:221-227 before use. | **MEASURED:** inactive → inactive |
| Saint actual AddDomeColonistsModifier, both branches | No preset writes; attempted method call at :183 throws inside Require(probe). Both behavior probes decline; :289 latches inactive. | **MEASURED:** inactive → inactive; no outer runner error |
| Saint LabelContainer.SetLabelModifier, 1.0.7 | Missing setter never used in pass: probe supplies its own dome.SetLabelModifier at :172-175. First local-map write rebased_from[Saint] = "Religious" (:268), then sole preset write Saint.modify_trait = "TraitReligious" (:269), then ctx.ever_changed and ctx.heal. | **MEASURED:** inactive → active, detail/mark cleared, absent from UpdateSuspects |
| Saint same setter, 1.1.0 | No preset writes. Missing setter never used; local rebase_resolved = candidates (:280), then ctx.heal (:281). Real arm log follows assignment. | **MEASURED:** inactive → active, repair armed; detail/mark cleared, absent from UpdateSuspects |
| Sinkhole class, both global and g_Classes member removed | No class/template writes. Type check returns at Fix_SinkholeIndestructible.lua:86-95. | **MEASURED:** inactive → inactive |
| Sinkhole DestroyBuildingImmediate | Missing global never checked or called. Class.indestructible = true (:102), template.indestructible = true (:107), ctx.patched, ctx.ever_changed, ctx.heal (:109-114). | **MEASURED:** inactive → active, detail/mark cleared, absent from UpdateSuspects |

**SOURCE:** core ctx.heal deliberately accepts inactive and clears update_suspect
(`Code/00_Core.lua:345-356`). The pass runner checks readiness, patched and veto at :364-367, but
not the apply verdict before pcall at :373. Register's reason-string branch records inactive at :456-459.

**Refuted initial inferences:** Sinkhole does not recheck both Require targets, only its class.
Saint does not partially edit and then hit an outer runner exception under these removals. Most
significantly, the successful bypasses do not leave the registry inactive: they erase the decline.
The initial inactive log remains in history; ListFixes reports active and UpdateSuspects is empty.

**INFERRED route:** target loss was injected. A real game update exposing this condition has not
been established, so reach remains **U**, not R1/R2. The archived leg is today's module against
1.0.7.396349 vanilla, not a claim about the frozen v5 module. Live-tree citations name 1.1.0.403908.

## 2b — instrument and fixture audit

New `tools/desk_c90_datapatch.py` keeps the k2 experiment's target-removal shape but loads real core.
It extracts Saint, Empath and Religious preset blocks verbatim; the fixed_labels table and
GetTraitLabel; AddDomeColonistsModifier; GetPropScale; SetLabelModifier; Sinkhole's classdef and
DestroyBuildingImmediate. All carry real source file names and line offsets.

**SOURCE / independently checked offsets:**

| Body | 1.0.7.396349 | 1.1.0.403908 |
|---|---|---|
| AddDomeColonistsModifier | Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1774-1791 | Lua/TraitPreset.lua:77-95 |
| GetTraitLabel | Lua/Traits.lua:1300-1302 | Lua/Traits.lua:1325-1328 |
| GetPropScale | CommonLua/PropertyObject.lua:1680-1688 | CommonLua/PropertyObject.lua:1760-1768 |
| SetLabelModifier | Lua/LabelContainer.lua:59-78 | Lua/LabelContainer.lua:59-78 |

Independent reviewer ran 18/18, read the real bodies, and checked debug.getinfo offsets. Root then
read every census callback and its actual mutation gate. The module's own capture stub is the reason
the missing setter is bypassed; it is not a harness replacement for a refusal-capable game method.

Fixtures: additive OnMsg registration; explicit ClassesBuilt with DataLoaded true; preset construction
and inheritance; first-write-observing proxies; translation identity; numeric IsPoint convention
(rejects unsupported types); core menu thread queued without execution; common ENGINE_SHIMS.
The actual probe supplies scale=1; the real GetPropScale is retained. No validity, transport or
save-healing decision is replaced to manufacture this result.

One initial fixture failure mattered: GetPropScale needed IsPoint. The real body logged
`CommonLua/PropertyObject.lua:1764: attempt to call a nil value (global 'IsPoint')`.
It correctly made the intact Saint control FAIL. Added only the numeric-point convention, preserving
the shipped body, after verifying the probe supplies numeric 1. No failure was dismissed as success.

A second improvement came from scratch verification: an intact 1.1.0 Saint with zero writes could
pass if its callback never ran. The demand now also requires its real repair-arm log; suppressing the
runner makes this demand FAIL. No shipping fix or field observation is inferred from that log.

**Independent review limitation:** the observer proxy stays raw-empty after backing-store writes.
That preserves the fresh first pass tested here, but would manufacture an extra template assignment on
a later re-fire. Therefore the harness explicitly disclaims idempotency/reload coverage.

## 2c — all callback sites, not a total alone

**SOURCE:** searched every DataPatch/OnDataReady occurrence in Code/*.lua and checked aliases/computed
access. Comments and helper definitions excluded. Complete executable membership:

| API and call site | Apply decline? | Guard conclusion |
|---|---|---|
| DataPatch, Fix_DustSicknessBiorobots.lua:104 | No: apply :168-170 only calls patch. | **SOURCE:** core veto; own pass checks target/construction. No apply-decline path. |
| DataPatch, Fix_FactionDomeSizeGate.lua:220 | Require CountDome at :420-423. | **SOURCE:** self_check_passed checked :235, set :424 after Require. |
| DataPatch, Fix_SaintBlessing.lua:207 | Three targets at :402-407. | **SOURCE + MEASURED:** unguarded apply verdict, per-target distinctions above. |
| DataPatch, Fix_SinkholeIndestructible.lua:81 | Class/global at :142-149. | **SOURCE + MEASURED:** class recheck only; global removal bypasses decline. |
| OnDataReady, Fix_BuildingCodesPrefab.lua:247 | IsKindOf, IsValid, Modifiable.SetModifier/FindModifier at :325-330. | **SOURCE:** callback check_shape :195-244 runs without verdict/veto guard but writes only local/registry/log state and calls probes on stubs. Actual building mutation :158 is behind WhenActive and guard == true at :251-252. |
| OnDataReady, Fix_SilentHitMomentFX.lua:286 | Require :291-303, unknown behavior :319-320. | **SOURCE:** callback wrapped in WhenActive; status/veto protect preset construction :128/:135. |

**INFERRED conclusion from enumerated routes:** OnDataReady has no id, status, veto or own exception
trap (core :431-446), but neither current caller exposes C90's data-mutation bypass. Its API being less
protective is insufficient evidence to call present reach worse. BuildingCodesPrefab may still run its
check and log under a decline/veto; that is distinct from touching a live building or preset.

Counts freshly emitted by doccheck:
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 49 registered (49 default-active, 0 optional-gated files)
- Code/*.lua files: 50
- TestKit probes: 97
- BUGS index rows: 119 F + 12 D + 91 C
```

## 3 — external scratch falsification

`python tools/c90_scratch_verify.py` writes altered source into a temporary Code tree, redirects only
the source read, and runs the original harness. Each variant must return **exit 1** with the expected
named FAIL; exceptions before assertions do not count. No built-in harness control switch is used.

| Scratch source change | Required discriminator |
|---|---|
| Remove real DataPatch callback invocation | Actual writes / arm log / recovery demands fail, including intact 1.1.0 Saint |
| Remove core veto guards | Both Saint branch veto demands and Sinkhole veto demand fail |
| Make ctx.heal return immediately | Status restoration and update-suspect erasure demands fail |
| Remove Saint's first-pass GetTraitLabel existence guard | Missing-label demands fail on both branches |
| Make Saint's behavior probe accept without reading the target | Missing-method demands fail on both branches |
| Remove Sinkhole's class existence guard | Missing-class demand fails |
| Remove C89 self_check_passed guard | Existing k2 fails, plus k and m3 |
| Remove historical F60 player_enabled argument | Exactly the two F60 harm demands fail; other migration demands still pass |

These are different kinds of claims: some demands characterize a defect, others hold a stopping guard.
For a defect demand, suppressing the defect must fail the demand. Reversing only a nonexistent guard
would be meaningless. The verifier requires the union of failures to include every new C90 demand.

## 4 — recommendation, filed-only work and unchecked artifacts

**INFERRED recommendation:** keep the repair bounded to apply-success guards in Saint and Sinkhole.
The census supplies no reason to change OnDataReady. If the owner chooses shared-core handling, define
a successful-apply contract and its retry ordering, then recheck all four DataPatch callers. Either
implementation must specify resetting/retrying a previous success; blindly retaining a once-true flag
is not equivalent to the latest apply verdict. Decision is mirrored in checklist 158, still unruled.

Do not gate on entry.status == active: run_apply sets status after apply returns, while apply may
legitimately invoke a pass during a retry. Generic optional reconciliation supports this ordering;
none of the four present DataPatch modules is optional. No code fix was landed.

**Filed rather than fixed:** updated existing C90 only. No unrelated new candidate found, no C91 work.

**Unchecked artifacts, explicitly:**

- No launched game, real update removing a target, or field reproduction.
- No real cold boot, enable/reload sequence, engine class flattening, classdef-only target loss with a
  surviving flattened copy, or save-healing execution.
- No post-registration veto, failed retry after prior success, DataChanged/idempotency claim, or
  comprehensive DataPatch lifecycle correctness claim.
- OnDataReady census is source evidence; no new injected runtime matrix for its two callers.
- logscan.py detection remains unopened; logs alone do not read changed preset values.
- The inherited migration fixture's GetResidenceComfort constant remains untouched, as directed.
  No new destroyed/invalid-object conclusion is drawn from it. Only the F60 source revision changed.
- No release approval, upload, deployment or version-number change.

## Landing receipts

Implementation/report landing: **576581c00e95f090414353a6df537f7b99293527** — only the eleven explicit
task paths, including this report and the brief deletion. Its pre-commit doccheck was GREEN. The follow-up
receipt commit is identified by `git log -1 -- docs/agent/reports/DESKBENCH_C90.md`; a commit cannot
contain its own hash. Both exact SHAs are supplied in the final owner handback.

Validation: doccheck GREEN (including parse checks), explicit-path commit/push; no production-code diff.
The consumed brief is removed and its grave row added to the prompt map. STATE replaces the resolved
instrument warning with the measured outcome, preserving open decisions and release holds. Its prior
warning is preserved in the appended session entry.

Doccheck's current STATE warning, verbatim (GREEN with warning, no hard-cap failure):

```text
  warn STATE.md is 13905 bytes, warn threshold is 12288 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md
```

Concurrency exception: a sibling edit to C74.md appeared during final documentation work. One regen
was batched after status before its output was inspected, violating the brief's no-regen-over-foreign-
bug-edits instruction. I inspected the resulting generated diff immediately: INDEX changed **only C90**;
C74's sibling edit changes its updated date/body and contributes no generated row diff. No sibling
content is staged or committed by this task. No further regeneration runs over that edit.

## Execution transcripts

These are the direct C90 and scratch-verifier transcripts, preserved without summarizing away failures
or demanding that the reviewer trust an agent's count.

```text
==============================================================================
C90 actual core: decline, ordered writes, and healing of status
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  1.0.7 Saint intact: exact writes and status  -- active -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint failed self-check is erased from UpdateSuspects
  PASS  1.0.7 Saint veto stops the pass
  PASS  1.1.0 Saint intact: exact writes and status  -- active -> active; []
  PASS  1.1.0 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; []
  PASS  1.1.0 Saint failed self-check is erased from UpdateSuspects
  PASS  1.1.0 Saint arms the save re-base despite decline
  PASS  1.1.0 Saint veto stops the pass
  PASS  Sinkhole intact: exact ordered writes and status  -- active -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole class: exact ordered writes and status  -- inactive -> inactive; []
  PASS  Sinkhole DestroyBuildingImmediate: exact ordered writes and status  -- inactive -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole failed self-check is erased from UpdateSuspects
  PASS  Sinkhole veto stops the pass

==============================================================================
18 of 18 demands held
ALL DEMANDS HELD -- injected target loss, not a field reproduction.
```

```text
EXPECTED FAIL: runner suppressed (exit 1)
  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.0.7 Saint failed self-check is erased from UpdateSuspects
  1.0.7 Saint intact: exact writes and status
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint arms the save re-base despite decline
  1.1.0 Saint failed self-check is erased from UpdateSuspects
  1.1.0 Saint intact: exact writes and status
  Sinkhole DestroyBuildingImmediate: exact ordered writes and status
  Sinkhole failed self-check is erased from UpdateSuspects
  Sinkhole intact: exact ordered writes and status
EXPECTED FAIL: veto removed (exit 1)
  1.0.7 Saint veto stops the pass
  1.1.0 Saint veto stops the pass
  Sinkhole veto stops the pass
EXPECTED FAIL: heal removed (exit 1)
  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.0.7 Saint failed self-check is erased from UpdateSuspects
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint failed self-check is erased from UpdateSuspects
  Sinkhole DestroyBuildingImmediate: exact ordered writes and status
  Sinkhole failed self-check is erased from UpdateSuspects
EXPECTED FAIL: Saint label-existence guard removed (exit 1)
  1.0.7 Saint GetTraitLabel: exact writes and status
  1.1.0 Saint GetTraitLabel: exact writes and status
EXPECTED FAIL: Saint behaviour refusal removed (exit 1)
  1.0.7 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.1.0 Saint arms the save re-base despite decline
  1.1.0 Saint intact: exact writes and status
EXPECTED FAIL: Sinkhole class guard removed (exit 1)
  Sinkhole class: exact ordered writes and status
EXPECTED FAIL: C89 apply-success guard removed (exit 1)
  (k) NEGATIVE -- a module registered but never applied patches nothing
  (k2) NEGATIVE -- a module whose self-check DECLINED patches nothing, even though DataPatch's runner still fires its pass
  (m3) Report() with the fix NOT applied says shipped=not-wrapped and does NOT claim the gate is active -- the owner cannot bank a false PASS
EXPECTED FAIL: F60 harmful argument removed (exit 1)
  F60 patch reports all 3 applicants housed while arrival space gate rejects home
  F60 patched tally counts 3 but migration gate still rejects
All 8 scratch variants failed as required; 18/18 C90 demands falsified.
```
