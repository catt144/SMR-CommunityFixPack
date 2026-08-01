# Chain 6 — audit candidate verification sweeps (game-free reading)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** Game-free; no `Code/` changes; READ-ONLY on the game dir.
Evidence base: `docs/reports/BUG_LIST_AUDIT.md` §5/§9 + the BUGS.md C-entries
named below. Extracted mod sources, if needed, re-derive via
`tools/flpk_extract.py` over the archived FPKs in
`C:\Dev\workshop_fpk_archive\` (all six mods, copied 2026-08-01 before any
unsubscribe — including the REMOVED fredware mod, whose FPK is otherwise
unrecoverable). Workshop subscriptions are no longer required for any chain
work.

**Staleness check: `git log --oneline -10` + `git pull`.**

## Jobs (todo list first; one item per sweep; each ends in a BUGS entry update)

1. **C32 sweep (ShiftsBuilding label desync).** Find the de-labeling path in
   Src (map unload? relabel?); check whether `AddToLabel` re-registration is
   safe; **and answer the owner's standing challenge: did 1.0.7 already fix
   it?** (GromGor's workaround is 1.0.6-era — the one packed-source finding
   never verified against current Src.) If 1.0.7 fixed it AND the witness
   thread's reports predate 1.0.7 → **re-examine F04's witness reassignment**
   (BUGS F04 audit note) and correct the audit record either way.
2. **C04 sweep (cross-map supply-grid breaks).** Trace WHO calls
   `SupplyGridFragment:RandomBreakConnection` (`SupplyGrid.lua:669-683`)
   during a surface dust storm and HOW an underground connector enters
   `self.connectors`. Verdict: F-row (with tier + intent tell) or corrected
   record.
3. **F35 scope check.** Source-level: does the old-save fixup our F35 ships
   cover the LIVE Frictionless-Composites label miss the audit's witness
   thread describes (audit §2.2 flag)? If the live case is real and
   uncovered → file it (new F-row or F35 extension) — do not fix here. The
   keyboard rider from prompt 1 settles the live half if source can't.
4. **fredware #11 comparison pass.** His
   `bf_restore_asteroid_lander_cargo_safety` ("payload changes interrupting
   drones/passengers on the cargo ramp") vs our F67/F68/F70 family — gap,
   overlap, or covered? One paragraph on the audit report §9 + a C-row if
   it's a real gap.
5. **Owner homework reminder (no session work):** the two audit stop-and-ask
   items still open — a logged-in Paradox subforum browse (F01's claimed
   report, F64's "void" report, F74's rival-rocket report) and a Paradox
   Mods browser check (console channel; feeds D13). If the owner has done
   them, record the outcomes on the relevant entries; if not, route the
   reminder to prompt 12's inbox.

## Scope fence

**In:** the four sweeps + records. **Out:** any fix; any decision (prompt 7
owns decisions); C22-C24 (already Src-verified — nothing to sweep); anything
the sweeps surface gets filed + routed, not chased.

## Stop conditions

- A sweep contradicts a recorded audit verdict → update the record with the
  new evidence trail and say so prominently (recorded facts are claims).
- Context pressure → self-split (`6b_…_opus.md`).

## What may not be claimed

No verdict without file:line read this session. "Already fixed in 1.0.7" only
by reading current Src, never by patch-note text alone.

## On completion

Outbox → `7_audit_candidate_decisions_opus.md`: sweep verdicts that change
its decision packages (esp. C32/F04). Delete this file, commit, push.

## Notes from upstream

(prompt 5 appends state here)
