# Project State — the one mandatory read

Current only, rewritten in place; history is append-only and newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine
behaviour `agent/facts/INDEX.md` · doc map `docs/README.md` · authoring
`agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · efforts over ~2 sessions
`agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ **The 18-prompt project chain is COMPLETE (2026-08-03)**; the playtest
campaign is the main line. **Read `agent/reports/CHAIN_QA_REPORT.md` first**
(verdict · doctrine HOLDS · §9 ordered top). ⭐⭐ **corun-rig: CO-RUN #0
PASSED 2026-08-04 w/ corrections — the rig WORKS**: cycle **79.9 s**, owner
**1.5 min** of ~10; next = prompt 3. ⛔ 5 corrections bind: `CORUN_RIG_SPEC` §8.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 100 F + 12 D + 44 C
```

Re-emit after any module or entry change; a red run refuses to hand one out.
Pinned **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).

⚖️ **F76 CLOSED-REFUTED, P1 released** (evicted to SESSION_LOG). Live residue:
**`C41` (cand)**, instrument `F76MISS`; MOD_DESCRIPTION's F76 note is VOID.

✅ **F11** — rider: **no demonstrated producer**; ⚠️ the cross-map route is not
provable from Lua (entry). **Fix CONVERTED full-copy → pre-wrapper `3a6512f`**:
by construction only, ⛔ NOT `tested` — checklist rider. ⭐ Owner: keep `P1`?

⚠️ **F99 (`cand`)** — **7** × `TrackElement.lua:805`, cheat-only observed;
no-cheat UNPROVEN, nothing built. **Route SETTLED at chain close**: the list is
empty BEFORE the rebuild (the filed route is refuted); drain =
`ExpandTrackFromElement:729` absorb-walk + the dead `:800` guard. Fix shape
known (`F99.md`), blocked on §4 reachability; severity = owner call (checklist).

⭐ **FIRST COMPLETE PROBE COVERAGE 2026-08-03** — MarsDebug `[install]`: **87
PASS / 0 FAIL / 0 SKIP** (EXECUTED-ONCE, `PLAYTEST_HELP`). ⛔ Never quote as
retail health (F98 is two-sided); **retail coverage is 78/87.**

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
