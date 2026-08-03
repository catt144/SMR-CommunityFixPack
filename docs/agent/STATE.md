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

✅ **Docs restructure + standing-prompts redesign COMPLETE 2026-08-03** —
`agent/reports/DOCS_RESTRUCTURE_REPORT.md`, `STANDING_PROMPTS_REDESIGN.md`.

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

✅ **D12 — PT-62 P4/P6 PASS 2026-08-03** (attended): the retirement dome ran
homeless **23 → 10 → 0** and `overpop true → false`; 0 leaked subjects. ⭐ Owner:
a win needing more testing, and ⛔ **NOT a release gate** — it is opt-in, so no
release step waits on it. Status stays `speced`. Owed: P12/P13/P14, the split
loop counter through a landing. ⚠️ The old loop check **could not fail** (it
counted the cohort delivery a flagged dome must receive) — split form now binds.

## Gates and holds

- **PT-62 remainder** (P12, P13, P14, landing check) → D12 — ⛔ NOT a release gate.
- ⭐ **F02 · F78 · F81 fired ORGANICALLY 2026-08-03** in the owner's campaign
  (storm wedge healed, 14 stray meteors cleared) — evidence upgraded, entries.
- **PT-37** → F48 · **F42** `blocked`, wontfix recommended, owner call needed.
- **D08 extender overhaul** — 5 layers speced in
  `agent/reports/DRONE_OVERHAUL_OPTIONS.md`, unbuilt; D06's dials wait on B2.
- **Owner decisions (6 open)** → `docs/PLAYTEST_CHECKLIST.md` "Decisions
  waiting on you", never only in agent docs.
- **Release** — `docs/archive/MOD_DESCRIPTION.md` is FROZEN, rebuilt from
  `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
