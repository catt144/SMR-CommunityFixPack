# Project State — the one mandatory read

Current only, rewritten in place; history newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine facts
`agent/facts/INDEX.md` · doc map `docs/README.md` · authoring `agent/WORKFLOW.md`
· code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ 18-prompt chain COMPLETE 2026-08-03; playtest campaign is the main line.
⭐⭐ corun-rig + `unattended-1` CLOSED 2026-08-04 (SAVE primitive PROVEN, tiers
ADOPTED) · **`corun-batch-1` CLOSED 2026-08-05**, every verdict SUSTAINED —
PT-37 case A PASS, case B UNSAMPLED, D07 4-of-5, E's precedence ROUTED.
⭐⭐ **`corun-batch-2` SITTING RAN 2026-08-10 — ALL 7 LEGS, 9 predictions HELD, 0
FALSIFIED, 0 `[LUA ERROR]`** (logs `archive/cb2sitting_…15.30.16.log` +
`cb2uninstall_…17.20.20.log`; ≈75 attended min vs 33–36, overrun all rig-side):
⭐ **popup KEYSTONE ANSWERED** (a storybit popup survives save/load AND still
applies its outcome); ⭐ **F21 restamp WITNESSED** organically (+33,884 ms), NOT
`tested`; **F85 CONFIRMED on its own site, ROUTE REFUTED** ⇒ owner; **F99's last
2×2 cell FILLED**, 0 throws, rate datum only; **PT-47 PASS** on every sampled
check; **`PT35FIXTURE.savegame.sav` BUILT** (unblocks PT-35's turbine half);
**PT-53 E CLEAN, but only after a FULL RESTART** ⇒ D13. ⛔ 14-entry ledger, 0 of
them the game's fault. ⇒ **NEXT: prompt 3 of `agent/prompts/corun-batch-2/` —
the terminal audit; it empties the folder and closes the chain.**

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 101 F + 12 D + 44 C
```

Re-emit after any module/entry change (red refuses); pinned **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).

⚖️ **F76 CLOSED-REFUTED**, residue **`C41`**. ✅ **F11** route (a) SETTLED, ⛔ NOT
`tested`. ⚠️ **F99 (`cand`)** cheat-only — 0-in-4 organic + 0-in-3 cheat-driven,
**2×2 now FULL**; rate bounds NOT refutation. ⚠️ **C42 (`cand`)** 3 empty
denominators. ⭐ **PROBE COVERAGE** — `[install]` 87/0; ⛔ **retail 78/87.**

## Gates and holds

- **PT-62 remainder** (P12/P13/P14 + split loop through a landing) → D12; P4/P6
  PASSED, ⛔ NOT a release gate. ⚠️ D12's preflight names the wrong class.
- ⭐ **F02 · F78 · F81 ORGANIC 2026-08-03 and ALL THREE again 2026-08-05** (entries).
- **F42** `blocked`, wontfix recommended. **D08 extender overhaul** speced in
  `agent/reports/DRONE_OVERHAUL_OPTIONS.md`, unbuilt; D06's dials wait on B2.
- ⛔⛔ **Close-out save-dir gate hole — FAILED TWICE.** Batch-1's audit AND
  batch-2's prep each recorded deleting the same four staged copies; all four
  were still on disk 2026-08-10. 15 deleted (~780 MB), `PT35FIXTURE` kept.
  ⭐ **Untested: does Steam Cloud restore saves deleted while Steam runs?**
- ⛔ **A Mod-Manager disable needs a FULL RESTART** to unload (D13, measured
  2026-08-10) — main-menu-only leaves code live with its permanent already gone.
- **Owner decisions (19 open** — F101 DECIDED `wontfix`; ⭐ 4 NEW from the sitting:
  F85's third cell · the 4th OFF state + PT-20 · the save-dir gate · the
  uncommitted tree incl. an unrecorded D07 answer) → checklist. Relabel OWED.
- **Release** — `docs/archive/MOD_DESCRIPTION.md` is FROZEN, rebuilt from
  `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
