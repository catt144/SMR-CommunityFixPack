# Chain 5 — F86 Phase 3: the Tier-2 repairs, the half-(a) design pass, and the unhold

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gate: prompt 4's
outbox below must confirm Tier 1 landed and its legs read clean. Authority
for shapes: `docs/reports/SAVE_SAFETY_REDESIGN.md` §5/§6 + `FIX_POLICY.md` §3a.

## Jobs (todo list first; one item per commit-and-verify unit)

1. **`Fix_DroneUnreachableForever`** — layer 3: patch the *consumer*
   (`CleanUnreachables`), leave the blocking body alone.
2. **`Fix_TrainWaitTime`** — layer 3 via the verified-synchronous
   `AddSpentTime` wrapper.
3. **`Fix_ArrivalDeaths` half (b)** — via `ChooseDome` per the sweep's route.
4. **`Fix_ArrivalDeaths` half (a) — DESIGN PASS, not a build.** The raw
   `SetPos` has NO route yet (plan's own warning: a design pass, not a
   guess). Produce the design with §3a compliance stated. **Stop condition:
   if no clean route exists, spec the options + trade-offs on the BUGS F53
   entry and route the decision to the owner via prompt 12's inbox — do NOT
   force a shape.**
5. **`Opt_DroneOverhaul` layer-2 move — CARVE-OUT PRE-GRANTED** (owner
   blanket clearance, README; also recorded in DRONE_PROJECT_PROMPT's
   2026-08-01 addendum so the drone track expects it). It is save-safety
   surgery on the wrapper's call position, touching no drone design — do
   the move here. **The clearance does not cover drone-design judgment:**
   if the move turns out to require ANY behavioral choice beyond call
   position, stop and ask — that would be new scope.
6. **One leg for the tier** (stale-probe gate first; probes updated so none
   asserts replaced behavior; predictions written down BEFORE the leg runs).
7. **After the leg verifies: record the D10/D12 UNHOLD** in STATUS and on
   both D-entries — the owner's gate was "repairs land and verify"; this leg
   is that verification. Prompts 9/10 are now runnable.

## Scope fence

**In:** the three builds, the one design pass, the carve-out ask, the leg,
the unhold records. **Out:** layer 1 (⛔ four own-thread modules +
`BombardmentSpread` are the accepted residual — do not re-propose); the
§5.4-A conversions (prompt 8); anything drone beyond the single carve-out
surgery; D10/D12 themselves.

## Stop conditions

- Half-(a) has no clean route → item 4's stop applies (spec + ask, don't build).
- The leg fails prediction → stop, report, chain waits.
- Context pressure → self-split (`5b_…_opus.md`).

## What may not be claimed

No module may be called layer-compliant without naming its verified
synchronous input. The unhold may not be recorded before the leg's numbers
are quoted.

## On completion

Outbox → `6_audit_candidate_sweeps_opus.md` (state) AND, if the carve-out or
half-(a) left residuals, → prompt 12's inbox. Delete this file, commit, push.

## Notes from upstream

(prompt 4 appends Tier-1 results here)
