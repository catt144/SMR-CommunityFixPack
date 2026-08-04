# Project State — the one mandatory read

Current only, rewritten in place; history is append-only and newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine
behaviour `agent/facts/INDEX.md` · doc map `docs/README.md` · authoring
`agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · efforts over ~2 sessions
`agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ **The 18-prompt project chain is COMPLETE (2026-08-03)**; the playtest
campaign is the main line. **Read `agent/reports/CHAIN_QA_REPORT.md` first** —
verdict, doctrine re-verification (it HOLDS), F97/D12/F76 adjudications,
standing items, and §9's ordered top (PT-62 remainder · load-heal round-trip
sweep · doctrine C-sitting).

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 100 F + 12 D + 41 C
```

Re-emit after any module or entry change; a red run refuses to hand one out.
Pinned **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).

⚖️ **F76 CLOSED-REFUTED, P1 released** (evicted to SESSION_LOG). Live residue:
**`C41` (cand)**, instrument `F76MISS`; MOD_DESCRIPTION's F76 note is VOID.

✅ **F11 rider RUN AND SETTLED 2026-08-03** — abduction keeps `train.units`
synced on BOTH maps (`table.find` → `nil`, `#units` 6, `holder == rocket` true):
**no demonstrated producer**, `TransferToMap` hypothesis refuted by measurement.
Entry's old citation was the wrong class/file; corrected. ⭐ Owner: keep `P1`?

⚠️ **F99 filed (`cand`)** — 14 × `TrackElement.lua:805` `start_el` nil in ~1h,
**every hit under `CheatCompleteAllConstructions()`**; vanilla, no-cheat
reachability UNPROVEN. ⭐ Owner: severity. (Both new items → checklist.)

⭐ **FIRST COMPLETE PROBE COVERAGE 2026-08-03** — MarsDebug `[install]` pass
(EXECUTED-ONCE, `PLAYTEST_HELP`): **87 PASS / 0 FAIL / 0 SKIP**. ⛔ **Never quote
as retail health** — `TechDescriptionBuilding` PASSes there, SKIPs on retail (F98
from the second side). **Retail coverage is 78/87.**

## Gates and holds

- **PT-62 remainder** (P12/P13/P14 + the split loop counter through a landing)
  → D12; P4/P6 PASSED 2026-08-03, ⭐ owner calls it a win needing more testing,
  ⛔ NOT a release gate (opt-in). Detail evicted to SESSION_LOG.
- ⭐ **F02 · F78 · F81 fired ORGANICALLY 2026-08-03** in the owner's campaign
  (storm wedge healed, 14 stray meteors cleared) — evidence upgraded, entries.
- **PT-37** → F48 · **F42** `blocked`, wontfix recommended, owner call needed.
- **D08 extender overhaul** — 5 layers speced in
  `agent/reports/DRONE_OVERHAUL_OPTIONS.md`, unbuilt; D06's dials wait on B2.
- **Owner decisions (9 open)** → `docs/PLAYTEST_CHECKLIST.md` "Decisions
  waiting on you", never only in agent docs.
- **Release** — `docs/archive/MOD_DESCRIPTION.md` is FROZEN, rebuilt from
  `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
