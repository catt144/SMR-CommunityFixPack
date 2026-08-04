# Project State — the one mandatory read

Current only, rewritten in place; history is append-only and newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine
behaviour `agent/facts/INDEX.md` · doc map `docs/README.md` · authoring
`agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · efforts over ~2 sessions
`agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ **The 18-prompt project chain is COMPLETE (2026-08-03)**; the playtest
campaign is the main line. **Read `agent/reports/CHAIN_QA_REPORT.md` first**
(verdict · doctrine HOLDS · §9 ordered top). ⭐⭐ **corun-rig chain CLOSED
2026-08-04** — rig PROVEN over 4 launches (**~30 s fixed + payload**, owner
~8 min vs ~25–30 promised), 3 of 4 payload items settled; **sign-off tiers
ROUTED (checklist)**; rule-5 recheck DONE, STANDS. Record: SESSION_LOG.

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

⚖️ **F76 CLOSED-REFUTED, P1 released**. Residue **`C41` (cand)**: ⭐ M5 lead
**MEASURED 2026-08-04** — an out-of-range mouse displaces the picker; ⛔ it
appeared 52/52, OG symptom unreproduced. MOD_DESCRIPTION's F76 note is VOID.

✅ **F11** — ⭐ cross-map route **SETTLED 2026-08-04: route (a)**. Pre-wrapper
WATCHED: **2 of 3** pass, ⛔ NOT `tested`. ⭐ Owner: close on 2/3? `P1`?

⚠️ **F99 (`cand`)** — **7** × `TrackElement.lua:805`, cheat-only; no-cheat
UNPROVEN, nothing built. Drain = `ExpandTrackFromElement:729` absorb-walk + the
dead `:800` guard; ⭐ the hex tie-break is **MEASURED 2026-08-04** (it returns
the hidden element). Blocked on §4 reachability; severity = owner (checklist).

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
- **Owner decisions (11 open, incl. the sign-off tiers)** →
  `docs/PLAYTEST_CHECKLIST.md` "Decisions waiting on you", never only in agent docs.
- **Release** — `docs/archive/MOD_DESCRIPTION.md` is FROZEN, rebuilt from
  `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
