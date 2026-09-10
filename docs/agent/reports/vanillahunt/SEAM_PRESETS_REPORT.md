# 03b — preset/generated seam close-out

Date: 2026-09-10.
Builds: old `1.0.7.396349`; new `1.1.0.403908`; installed Steam build `24995074`.
Method: read-only source audit. No game was launched and no source archive, game file, module, or frozen receipt was changed.

## Exact receipt

03b read **1,984/1,984 assigned items**: all **1,618 PRESETS** rows, all **360 INVENTORY** rows assigned to 03b, and all **6 CALLERS** items. There were zero missing, duplicate, extra, or `NOROWS` items and no child queue. Per-key ledgers and methods are preserved in:

- `SEAM_PRESETS_FOOD_REPORT.md` — 560 food/resource/UI preset rows;
- `SEAM_PRESETS_PROGRESSION_REPORT.md` — 548 progression/politics preset rows;
- `SEAM_PRESETS_SUPPORT_REPORT.md` — 510 support/story preset rows;
- `SEAM_PRESETS_GENERATED_DATA_REPORT.md` — 184 generated Data rows;
- `SEAM_PRESETS_GENERATED_CLASSDEFS_REPORT.md` — 92 generated ClassDefs rows;
- `SEAM_PRESETS_GENERATED_XDEF_REPORT.md` — 82 XDef and 2 BuildingTemplate rows, plus all 6 callers.

Instrument qualifications were retained rather than silently normalized: 181 ResourcePreset rows use synthetic ordinal identities over 14 real bodies; 20/22 BuildingTemplate remove/add pairs are false splits from `Id` spelling; 6 XDef rows are positional artifacts; progression has 22 nested-list `REINDEX-SWAP` rows; support has 29 hunk-only ordinal mismatches (13 Label, 15 SA_Exec, 1 SA_WaitMessage); generated Data has 179 `MULTI` anonymous ordinals reconciled by enclosing preset; ClassDefs R07357/R07525 are over-span unchanged anonymous leaves. The generated XDef receipt has no malformed rows.

## Parent verdicts

- **C75**, P2 cand/source-read: The Incident's no-explosion branch says and comments that new Fusion Reactor construction is suspended, but only disables existing reactors. Its explosion sibling also locks the building menu; the shared researched-tech follow-up unlocks it. Runtime remains unobserved.
- **C76**, P2 cand/source-read, DIFF-CAUSED: new `DiscoverTech.__exec` sends authored `Cost` to `SetResearchPointInitiativeCost`, whose `IsInitiative` guard rejects ordinary researchable Techs. Twenty-six positive authored nodes in 15 base StoryBit files target 13 regular Techs. Runtime remains unobserved.
- FactionOpportunity's guarded `PressFunc` versus unguarded `DismissFunc` was rejected: creation requires `g_Legislature`, and every located cleanup removes the notification while that global exists.
- LongWinter's `DiscoverTech` to `RewardTech` full-grant change was retained as a real delta but not filed because no hard unintended tell survived.
- Generated Data's four hard tells are old-only defects repaired by 1.1: rival milestone ownership, funding-notice amount, Childcare's boundary comparison, and Skip Founder Stage's law-key lookup.
- PERF-only, unmeasured: XTechTree's per-query full-tech scan/translation, three repeated Now Serving menu computations, and Renegade daily connected-dome suppression lookups. None was promoted.
- SameOldSlop's `> 500` consumer correctly unlocks after the described 500-Sol threshold; LowGFungi is correctly underground; DeepScanning's Tech/effect/Exploration route is connected; no concrete authored C62 ScriptStatements instance was found; R11004 universal-storage Seeds remains for 04.

## Controls and field reports

The parent re-derived `.NET Random(2026091003)` sample `P02567 P25371 P05044 P07434 P09902 P09779 R11538 R11606`: **8/8 change descriptions and 8/8 routes**. Eligible F114-F117 positive seeds: zero, score N/A.

Exact 03b FR tags were four FR-1(c) rows (`P09388`, `P09389`, `P09392`, `P09397`) and two FR-2 rows (`P02707`, `P13830`); FR-1(b) and FR-3 had zero assigned rows. Native particle rendering remains unmeasured with no established crash mechanism. DeepScanning remains connected. PERF leads are unprofiled and cannot explain a report predating 1.1. **FR-1, FR-2, and FR-3 remain open; no field report was closed.**

## Handoff and limits

04 owns the broader research-cost migration in R09089/R09475 and must avoid duplicating C76's narrower `DiscoverTech` route. It also retains C62's authored ScriptStatements-instance search and R11004's universal-storage Seeds route.

For dlccheck only, TAKEABLE WHEN a concrete owning class/preset is read: five added AmbientLife programs and their actual building `prg_class`; WorkFarmSmall's `Maps[1]` tablet assumption if another-map reach is established; InsectFarming/FarmInsect task availability and completion; Sugar/Spices registration against guarded flight lists; and whether official DLC Techs exclusively use the new `Techs` structure. The Norman Now Serving surface is profiling-only. Base routes are not DLC clearance.

Known search drift is disclosed: two parent absolute-root `rg -g '!DLC/**'` probes emitted broad DLC name-line hits because the exclusion did not bind; no DLC body entered coverage. The food reader performed incidental Norman name searches. The support reader opened exactly the directly called `N/DLC/norman/Code/FarmInsect.lua:57-59`. A separate 03c Norman search is not 03b coverage. The ResearchTechsCombo correction is explicit: old callers already passed the sentinel but the old callee ignored it; the new varargs callee consumes it.

The immutable inputs `INVENTORY.tagged.tsv`, `PRESETS.tagged.tsv`, `CALLERS.tagged.tsv`, and `SEAM_COVERAGE.tsv` were not edited. Terminal audit 99 waits only for 04 and any child 04 declares.

## Gate result and standing warnings

The clean close-out sweep found zero `TEMPORARY` hits. `doccheck.py` was GREEN,
`treediff.py --selftest` passed, and `presetdiff.py --selftest` passed. Doccheck
emitted the existing frozen-index warnings below, retained verbatim:

```text
warn F85: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
warn C12: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C13: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C14: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C15: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C16: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C17: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C37: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C35: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C34: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C38: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
warn C39: the frozen index-row cell says 'filed', entry says 'tested-unattended' (from 'tag')
warn F100: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
warn C43: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
warn C49: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
warn C50: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
warn C51: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
warn C52: the frozen index-row cell says 'filed', entry says 'parked' (from 'tag')
```
