# Chain 10 — D12: the no-homeless dome policy build

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gate: the D10/D12
unhold recorded (prompt 5); prompt 9 (D10) landed and its leg read clean —
**never build D12 in the same session as D10** (both touch colonist
assignment; standing rule: separate landings, own A/Bs). Authority: **the
BUGS.md D12 entry is the spec** — speced 2026-07-30, user-approved.

## Jobs (todo list first)

1. **Build per the D12 entry**: own module; `Opt_ResidencyControl` as donor
   PATTERN only (not shared code); breaks vanilla's emigration tie for
   homeless colonists so specialist domes stop stranding them (also unwinds
   the D07 overpopulated deadlock without touching D07).
2. **Hard constraints from the entry (binding):** the new flag must NOT
   route through `CanAcceptNewColonists` (D03's gate) or it blocks the
   cohort delivery it exists to protect; **never expel to the surface**.
3. **Probe + the module's own A/B leg** (stale-probe gate; predictions
   first).
4. Its playtest item added to the checklist for the campaign (mirror what
   the entry specifies); STATUS/BUGS records.

## Scope fence

**In:** D12 per its entry, its probe, its leg, its checklist row.
**Out:** D10 (done or not — either way not here); D07 (untouched by design);
any residency behavior beyond the entry.

## Stop conditions

- The build cannot satisfy a hard constraint without redesign → STOP; the
  constraints are owner-set; spec the conflict on the entry and ask.
- Leg fails prediction → stop, report.

## What may not be claimed

`fixed` only after the leg; `tested` belongs to the playtest campaign. The
D07-unwind claim may not be asserted as verified — it is the entry's design
rationale until a playtest observes it.

## On completion

Outbox → `11_f76_depot_picker_repair_opus.md`. Delete this file, commit, push.

## Notes from upstream

(prompt 9 appends state here)
