# Project State — the one mandatory read

Current only, rewritten in place; history newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine facts
`agent/facts/INDEX.md` · doc map `docs/README.md` · authoring `agent/WORKFLOW.md`
· code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ 18-prompt chain COMPLETE 2026-08-03; playtest campaign is the main line.
⭐⭐ corun-rig + `unattended-1` CLOSED 08-04 · **`corun-batch-1` CLOSED 08-05** ·
**`corun-batch-2` CLOSED 08-10, EVERY leg verdict SUSTAINED** (keystone ANSWERED,
F21 WITNESSED, F85 route REFUTED ⇒ owner, F99 2×2 FULL, PT-47 ARCHIVED,
**`PT35FIXTURE` BUILT**, D13's 4th OFF state).
✅✅ **`unattended-2` prompt 1 DONE 2026-08-11 — ALL FOUR ITEMS BUILT AND
VERIFIED** (`3c1ccc8` + TestKit `d8e1fbf`; log `u2run3_*`, 81/81 active AS READ,
3 loads, 2 R4 round trips, **0 `[LUA ERROR]`**). **F48 → `fixed`: 7 tracks
repaired, every one to the clean-chain `2×(n−1)`, incl. PT-37's own 280-element
559→558; held across BOTH round trips; zero on the clean save.** **C43 →
`fixed`**: 77/0/10/0 vs baseline 78/0/9/0 — one declared flip, zero TestKit
errors, gap answered (**no other caller**). **F100 → `fixed`**: new boot line
verbatim. **PT-35 leg A case A COMPLETE** — 0 of 14 at every comparison, both
halves sampled at last. ⚠️ First launch VOID (pack disabled; owner re-enabled).
⭐ NEW `EF-050` (savename verbatim) · **`EF-051` STEAM CLOUD RESTORES DELETED
SAVES — predicted, then confirmed twice; clears both "failed" close-outs** ·
WORKFLOW batch-2 rule 7 amended (the gate must STOP, at every run).
⇒ **NEXT: `02_FABLE_AUDIT.md` (terminal audit, folder must end empty). Owner has
ONE tick left — untick Steam Cloud saves (checklist top). Then the PT-20 REDO
co-run (+ the Ctrl-F9 check that settles F85; chain unauthored).**

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 101 F + 12 D + 45 C
```

Re-emit after any module/entry change (red refuses); pinned **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).
⚖️ **F76 CLOSED-REFUTED** → `C41`. ✅ **F11** settled, P2, NOT `tested`. ⚠️
**F99/C42 (`cand`)** — rate bounds only. ⛔ **retail probes 78/87.**

## Gates and holds

- **PT-62 remainder** (P12/P13/P14 + split loop through a landing) → D12; P4/P6
  PASSED, ⛔ NOT a release gate. ⚠️ D12's preflight names the wrong class.
- ⭐ **F02 · F78 · F81 ORGANIC 2026-08-03 and ALL THREE again 2026-08-05** (entries).
- **F42** `blocked`, wontfix recommended. **D08 extender overhaul** speced,
  unbuilt (`agent/reports/DRONE_OVERHAUL_OPTIONS.md`); D06's dials wait on B2.
- ✅ **Save-dir "failures" EXPLAINED: Steam Cloud restores them at launch
  (`EF-051`)** — record "deleted, listing verified", never "gone", until untick.
- ⛔ **Mod-Manager disable needs a FULL RESTART** (D13); PT-20 re-check =
  decision 6. ⚠️ **A leg that disables the pack HANDS THE RE-ENABLE BACK — it is
  unscriptable, and leg T left the pack off from 08-10 to 08-11.**
- **Owner decisions: 2 open**: **F85** (evidence-gated — Ctrl-F9 check rides the
  PT-20 redo) · **relabel WORDING** (owner text, launch prep). ⭐⭐ **Src
  FOUND**: `Project Spark` dir (EF-014).
- **Release** — `archive/MOD_DESCRIPTION.md` FROZEN, rebuilt from `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
