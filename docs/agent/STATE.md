# Project State — the one mandatory read

Current only, rewritten in place; history newest-first in
`docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md` · engine facts
`agent/facts/INDEX.md` · doc map `docs/README.md` · authoring `agent/WORKFLOW.md`
· code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Where the project is

✅✅ 18-prompt chain COMPLETE 08-03; playtest campaign is the main line. Closed
co-runs, every audit sustaining every verdict: `unattended-1` 08-04 · `batch-1`
08-05 · `batch-2` 08-10 · `unattended-2` + `corun-pt15` 08-11 (F07 `tested`, C39
MISSING UPLIFT, EF-051/052; saves KEPT `CP15PT15` `CP15F15`) · **RULINGS 08-12**:
C46 `wontfix` · F85 = build the `dont_pause` flip · C39 = extend compensation +
sweep all 3 automation labels · load-heal CLOSED · F102 shipped w/ disclaimer.
⭐⭐ **`corun-pt60` SITTING RAN 08-12 (~95 min attended, promised 40–60): P1–P5
HIT · P6 zero errors in 1,082 lines · P7 owner verbatim · ⭐ P8 DECIDER TAKEN on
the pre-batch Sol-302 campaign — heal fired ONCE (10 re-based, 10-of-10 effect),
ZERO repeat after the round trip, both boot look-alikes once each pre-load** ·
P8's F95 half + P9 non-discriminating, recorded as such · F91 controlled zero (0
of 7) · **F48 repaired 3 of 7 tracks and the repair PERSISTED** · ⭐ **F34(d) route
re-derived on the owner's challenges: RC Commander is the ONE live route, rocket
route UNREACHABLE, 3 wrong claims in its paperwork** · EF-053 · WORKFLOW +1 · log
archived, staged saves deleted + listing verified. ⚠️ Its `81/81` predates
`5a1508b` (F102 landed 12 min after that launch).
⇒ **NEXT: prompt 3, the Fable AUDIT** — `agent/prompts/corun-pt60/03_FABLE_AUDIT.md`
(carries an owner AGENDA item: a costed route to ship-ready for the train queue).
Behind it: `unattended-3` (F85+C39+3-label) · PT-20 redo.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 82 registered (75 default-active, 8 optional-gated files)
- Code/*.lua files: 83
- TestKit probes: 87
- BUGS index rows: 102 F + 12 D + 46 C
```

Re-emit after any module/entry change (red refuses); pinned **1.0.7.396349** (fpk parity — `agent/facts/EF-014`).
⚖️ **F76 CLOSED-REFUTED** → `C41`. ✅ **F11** settled, P2, NOT `tested`. ⚠️
**F99/C42 (`cand`)** — rate only. ⛔ **retail MEASURED 08-12: `77 PASS, 0 FAIL, 10
SKIP, 0 ERROR`; 79 attempt a verdict (8 `[install]`), +`AnomalyCaveInMap` +`TechDescriptionBuilding`. SKIPs read BY NAME, never as a total.**

## Gates and holds

- **PT-62 remainder** (P12/P13/P14 + split loop through a landing) → D12; P4/P6
  PASSED, ⛔ NOT a release gate. ⚠️ D12's preflight names the wrong class.
- ⭐ **F02 · F78 · F81 ORGANIC 08-03, again 08-05; F78 +2 · F02 +1 08-11.** **F42**
  wontfix (owner 07-25). **D08 extender overhaul** speced, unbuilt; D06 → B2.
- ⚠️ **EF-051 ON HOLD 08-12 — owner re-ticked Steam Cloud ON** (temporary; they
  announce the untick); 18 strays DID return 08-12 12:29 — mechanism, NOT findings.
- ⛔ **Mod-Manager disable needs a FULL RESTART** (D13); the PT-20 redo is NEXT.
  ⚠️ **A leg that disables the pack HANDS THE RE-ENABLE BACK — unscriptable.**
- **Owner decisions: 2 open**: **relabel WORDING** (launch prep) · ⭐ **TRAINS —
  what standard puts them ship-ready** (checklist 12, owner-raised 08-12; nothing
  blocked on it). ⭐ **cheats-on-playtest-saves RULED 08-12 → WORKFLOW rule.**
- ⚠️ **The rig has CHEATS ENABLED (owner, 08-12)** — infopanels expose
  `Inspect`/`Properties`: every "on retail" claim must name that. Routed to audit.
- **Release** — `archive/MOD_DESCRIPTION.md` FROZEN, rebuilt from `agent/bugs/` at launch prep; four `[DRAFT NOTE]` markers die first.
