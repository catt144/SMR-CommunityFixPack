# Project State — the one mandatory read

Current only, rewritten in place; history is append-only and newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine
behaviour `agent/facts/INDEX.md` · doc map `docs/README.md` · authoring
`agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · efforts over ~2 sessions
`agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ **The 18-prompt project chain is COMPLETE (2026-08-03)** — chain prompt 12
(Fable) verified it end to end and emptied the folder. **Read
`agent/reports/CHAIN_QA_REPORT.md` first**: verdict, findings, the doctrine
re-verification (it HOLDS), the F97/D12/F76 adjudications, the standing-item
table, and the campaign's ordered top. **The owner is free for the playtest
campaign** (`docs/PLAYTEST_CHECKLIST.md`; at the keyboard first: PT-62's
remainder, the load-heal round-trip sweep, the doctrine C-sitting — §9).

✅ **Docs-restructure chain COMPLETE (2026-08-03)**, spec executed, doccheck v3
armed as pre-commit hook — end state in `agent/reports/DOCS_RESTRUCTURE_REPORT.md`.
✅ **Standing prompts REDESIGNED 2026-08-03** — O1–O7 decided, O1/O3/O4/O7
adopted (WORKFLOW element 8, mech. rules 6/8), both prompts route via the
INDEXes: `agent/reports/STANDING_PROMPTS_REDESIGN.md`.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 98 F + 12 D + 41 C
```

Re-emit after any module or entry change; a red run refuses to hand one out.
Pinned build **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).

⚖️ **F76 — CLOSED, REFUTED** (QA job 10, owner-routed). Re-verified rather than
inherited: box and mouse are one coordinate space, the forensic box was correct
placement, the load failure did not reproduce, the picker is vanilla. **P1
released.** The unrefuted residue is **not** closed with it — the "icon does not
appear" witness and the out-of-range-mouse lead are **`C41` (cand)**, instrument
`F76MISS`; MOD_DESCRIPTION's F76 note is VOID.

✅ **D12 `Opt_NoHomeless` — THE BUILD STANDS** (job 9). Five live-review decisions
upheld, the veto's D07-independence verified from code; **PT-62's remainder is
the only gate left**, and D12 claims nothing beyond `speced`.

## Gates and holds

- **PT-62 remainder** (P4/P6 stable colony, P12 uninstall, P13 veto) → D12.
- **PT-37** → F48 · **F42** `blocked`, wontfix recommended, owner call needed.
- **D08 extender overhaul** — 5 layers speced in
  `agent/reports/DRONE_OVERHAUL_OPTIONS.md`, unbuilt; D06's dials wait on B2.
- ✅ **Checklist REDESIGNED 2026-08-03** (owner-approved at the checkpoint):
  by-system groups, Bug/Requirements/Setup format; snapshot+old protocol archived.
- **Owner decisions (6 open)** → `docs/PLAYTEST_CHECKLIST.md` "Decisions
  waiting on you", never only in agent docs.
- **Release** — `docs/archive/MOD_DESCRIPTION.md` is FROZEN, rebuilt from
  `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
