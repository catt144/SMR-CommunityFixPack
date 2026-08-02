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

### From chain prompt 4b (Tier-1 close-out, 2026-08-01) — Tier 1 is DONE and VERIFIED

**What landed, with commits.** Build: `d899a54` (Fix_MeteorFrequency rewrite),
`d94ac94` (Fix_RainsDeadlock rewrite + C34 rider), `e5b4284`
(DisasterPredictionLeak NewDay rider), `a213492` (StormWedgeHeal reorder),
`b728d9c`, `70e6d0c` (leg-3 id-less clause amended, owner-cleared), `94cfa46`
(F89 filed), `212c841` (ENGINE_FACTS Msg/OnMsg), `a9d68e3`, `8e00868` (split),
**`c6180ad` (this close-out: legs recorded, four entries flipped)**. TestKit
`09a4f47..49b40da`, local-only.

**All five legs RAN** (owner at the keyboard; save lineage `save_game_id
HdmSxGs6kyd0uz6-`, test-2, map BlankBigCanyonCMix_09). Logs:
`Mars.exe-20260801-16.42.31` (first load), `-17.11.08` (main sitting),
`-19.14.11` (uninstall/leg 5). **F02, F78, F81, F88 → `tested`** (index rows
and heading tags both); C34's rider verified; PT-54's retirement made good in
`PLAYTEST_CHECKLIST.md` §3. Full leg readings live in the entries and in
STATUS — do not re-derive them, cite them.

**⚠️ THE ONE THING TIER 2 MUST PICK UP — F86 Site 2 is live and measured
again.** Leg 5's uninstall log carries **80** orphan
`[LUA ERROR] Opt_DroneOverhaul.lua:96: attempt to index a nil value (global
'SMRFixPack')`, call chain `(96) ← (190) ← sprocall ← CommandObject.lua(246)`
— byte-for-byte the shape `BUGS.md` already records for Site 2 (at 98/session).
The route is the persisted `Drone:Idle` wrapper reaching the save through drone
command state.
- **NEW measurement, not previously recorded:** the errors are confined to the
  **first load** of the uninstalled save (all 80 inside ~2 s at Lua
  `0:00:26`), and there are **ZERO after a save+reload** — the leak
  **self-clears in one load**, because the erroring commands abort and get
  re-issued onto vanilla bodies. Worth folding into the Site 2 record.
- Harm remains log noise only (line 188 calls `orig_idle(self)` first, so
  vanilla's `Idle` completes before line 190 throws; drones behaved normally).
- The owner **explicitly ruled this out of prompt 4b's purview** (2026-08-01):
  it belongs to this chain, notes only. It did **not** gate the Tier-1 flips.

**MOD_DESCRIPTION's no-precedent sentence is YOURS to unlock, not prompt 4b's.**
The `[DRAFT NOTE — CONDITIONAL]` marker is still in place and the sentence is
**unchanged and unsoftened** — it ships whole or not at all. Its gate was
CORRECTED this session: it used to read "until F86 Tier 1 has landed AND
verified", which is now *true* while the claim is still unbackable, so a
session reading only the old note would have published it wrongly. The gate now
names **Tier 2** and carries a do-not-delete-on-the-old-reading warning.
**When Site 2 closes and an uninstall leg reads clean across the whole pack,
delete the note and keep the sentence verbatim.**

**⭐ THE ETHOS AND THE RELEASE GATE WERE RESTATED BY THE OWNER 2026-08-01 —
read `FIX_POLICY.md` §3a before scoping anything here.** Two changes bind this
prompt:

1. **Three-tier ethos** (supersedes any "leave no trace" framing still lying
   around the docs): (1) leave no trace; (2) failing that, leave **inert**
   trace, named and disclosed; (3) failing that, leave harmful trace **only**
   paired with its remedy — the D13 cleaner, a **hard launch dependency**.
2. **The release gate is PER-SITE, not blanket.** Every exposed site needs a
   recorded disposition: repaired in-pack where a layer 3/2 route exists,
   handed to the cleaner where one provably does not. A site without a
   disposition blocks release; a site with one does not, either way.

⛔ **DO NOT READ THAT AS PERMISSION TO DESCOPE.** The owner was explicit:
*"We will build everything now, regardless of whether the cleaner exists now
because we won't launch till it does. It doesn't make sense to build a cleaner
until we know everything it needs to clean and how."* So: **build every
reachable repair in this tier, now.** A cleaner hand-off is a valid disposition
only *after* the in-pack attempt has been made and the route proven absent —
never as a prediction, never as a reason to skip work. D13's target list is the
**output** of what you build here, which is exactly why it cannot be specced
first. **Record a disposition for every site you touch, including the ones you
repair.**

**Constraints and facts Tier 2 should respect:**
1. **All legs ran on the test-2 lineage** (`HdmSxGs6kyd0uz6-`). Anything you
   compare against that state must account for the lineage, and the re-cut
   uninstall article is saved as `T1-UNINSTALL` / `t10uninstall-r`.
2. **D10/D12 unhold is THIS prompt's record to make** (chain README row 5).
3. **F89 (`94cfa46`) is filed and open** — vanilla's drain loop wedges the
   *Meteors* thread on ordinary strikes; covered by the F02 watchdog, no direct
   fix routable. Two recorded caveats: event-spawned meteors **re-arm** the
   watchdog's liveness clock (any meteor posts `MeteorDone`), stretching
   detection latency in event-heavy periods (accepted by design); and leg 5
   added an **uninstrumented** vanilla sighting — do not upgrade it to a
   measurement.
4. **TestKit facts a probe author must know** (all committed): `Msg`, `OnMsg`,
   `rawget`, `getmetatable`, `os`, `_G` are **per-env specials** — the
   ENV_SPECIALS guard refuses them in `SetGlobal`/`WithGlobals`, and
   `ENGINE_FACTS.md` has the mechanism (`212c841`: they can be neither stubbed
   nor read back once their env wrapper is deleted). `FromFixPack` defers a
   retail SKIP that **replaces** a probe's verdict — gate such checks on
   `SMRTest.GetDebug()`. A bare console `RunAll` has no thread context;
   `*r SMRTest.RunAll()` is the full-coverage form.
5. **The observability loggers are per-session toggles** (`SMRTest.Log.<name>(true)`,
   `90_Loggers.lua`) and a game restart clears them. Leg 5 lost its meteor
   instrumentation exactly this way — turn the logger on *after* every restart,
   or the silence in your log will mean nothing. `SMRTest.Loggers()` lists state.
6. **`IsValidThread` returns NO value on load** (already in BUGS at the F86
   Site 1 block) — `tostring(IsValidThread(x))` throws `bad argument #1`. Read
   thread liveness via `SMRTest.FixtureCarry()` instead, which reports it
   properly.
7. **FixtureCarry cannot see label modifiers** — it says so itself
   (`NOT INSPECTABLE … absence here is NOT evidence of absence`). Any Tier-2
   residual claim about modifiers needs a different instrument.
8. **The natural storm's 74h UI countdown was read with the pack ON.** If a
   Tier-2 sitting sees storm warnings near ~90h, that is the wrapper key
   leaking and F02's entry says where to look.
9. **Probe sweep was clean** (zero `TEMPORARY` hits, both repos) at `c6180ad`.
   Re-run the gate before any test of your own.
