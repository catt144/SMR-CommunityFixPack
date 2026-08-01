# F86 Tier-1 build prompt — the two rewrites, the riders, and the legs that prove them

**One-off. Chain prompt `4_f86_phase2_tier1_build_fable.md` executes this and
deletes it (consumed) in its own final commit — this file does not delete
itself mid-job.** Written 2026-08-01 by chain prompt 3 with full spec context.

**THE SPEC IS `docs/reports/SAVE_SAFETY_REDESIGN.md` §6.2a. It is final.**
Every load-bearing input is measured or owner-decided; the decisions below are
**not re-litigable** in this session:

- GT creation **DEFERS** (measured twice, incl. GT-creates-GT with a live
  `WaitMsg` receipt) → the rains wrapper works as written. Do not build the
  synchronous heal, the ChoGGi-style body, or the `Sleep(1)` micro-thread.
- The F02 wrapper keys on `CurrentThread() == rawget(_G,"Meteors")`; the
  defer-when-falsy guard is kept as defence in depth (measured: not
  load-bearing). Descriptor keying is a barred balance change.
- The one-shot latched heal is the F88 fix (owner decision; GameVar version
  latch). Never restart the meteor thread on an ordinary load.
- The C34 rider rides the rains pass — no module of its own.
- The F81a **mid-session NewDay reconcile is TAKEN** (pre-cleared option,
  reasoning in §6.2a-C) — legs A/B below carry its changed shape.
- ⛔ Layer 1 is not to be built. ⚠ fredware's `WaitCurrentDisaster`/loop-body
  replacements are §3a violations — never a pattern to copy.

## Staleness check

`git log --oneline -10` + `git pull` first. This brief matches the repo at
commit `9e53753` (adjudication §4.4 closed). If `SAVE_SAFETY_REDESIGN.md`
§6.2a or the BUGS F86 enumeration block has moved since, re-read them before
building.

## Todo list — REQUIRED before starting, one item per commit-and-verify unit

Create it covering the whole job; mark items complete the moment they
complete; exactly one in progress; expand any item that turns out to contain
more units (the S6a-d lesson). The build units below are the starting
granularity — each is its own commit with BUGS.md updated in the same commit
and a parse sweep (python + `luaparser`, `utf-8-sig`) over every edited file
before committing. Check `Mars.exe` is not running before touching loadable
code.

## Build units (order matters — each compiles and self-checks before the next)

1. **`Fix_MeteorFrequency` rewrite** per §6.2a-A: the keyed
   `GetDisasterWarningTime` wrapper (`Max(orig(descr), descr.spawntime +
   descr.spawntime_random)` on the keyed path only); delete the `funcs.Meteors`
   body install and the heartbeat surface; `GameVar("SMRFixPack_MeteorLatch",
   false)` one-shot version-latched restart on PostLoadGame; watchdog liveness
   moved onto an additive `OnMsg.MeteorDone` timestamp + the NewDay check
   (unchanged threshold, 3-restart ladder, designed-silence guards), restarting
   **vanilla's** body. Header states layer 3, the ~10-game-minute residual, and
   the latch residual.
2. **`Fix_RainsDeadlock` rewrite** per §6.2a-B: the collision-mirroring
   wrapper on `RainsDisasterActivation` (pre-check → `Msg("RainDisasterEnd",
   MainMap, settings.type or "normal")` → return; else tail-call orig);
   delete `fixed_loop`, the `RainsDisasterLoop` replacement and
   `SMRFixPack.RainsFixedLoop`; the version-stamped migration pass
   (`SMRFixPack_loop_version`, id-less entries resolved by unique
   `settings.type` match, `main_thread` never touched); **the C34 rider in the
   same pass** (structure repairs → stale-ACTIVE heal via vanilla
   `FinishRainProcedure` → loop migration; manual fallback for invalid
   `g_RainDisaster` values). Update the C34 BUGS row/entry disposition in the
   same commit.
3. **`Fix_DisasterPredictionLeak` rider** per §6.2a-C: `OnMsg.NewDay` →
   `ReconcileDisasterPredictions()` (WhenActive-gated, pcall-wrapped).
4. **`SMRFixPack.StormWedgeHeal` reorder** per §6.2a-D: orphan gate at body
   start and after every `Sleep` (`if not SMRFixPack then g_MeteorStormStop =
   false return end`); vanilla-state resets before every mod-name touch;
   logging last.
5. **TestKit probe updates** so no probe asserts deleted behavior
   (`RainsFixedLoop`, the meteor heartbeat phases, the old bounded-timeout
   loop — all gone; the F28/F49 lesson). Probe-count changes → STATUS, same
   commit. Declare any probe you arm; tear it down in the recording commit.

## ⛔ Stale-probe gate — before ANY leg

Run the stale-probe sweep over both repos and record its output BEFORE
launching the game. **Expect `PROBE SWEEP: clean` — ZERO hits in both repos**
(97 and 99 are gone since 2026-08-01; the "one declared hit" earlier sessions
saw is stale). A hit means an undeclared probe: stop and remove it first.

## The legs (one GAME sitting for the tier, owner at the keyboard)

**Leg 1 — Tier-1 A/B pair** (PT-54 triggers C+D absorbed here): B-side on the
rewritten pack — meteor cadence on the designed 35–115 h schedule (vanilla
body + wrapper), storm warning timing UNCHANGED (~6 h + tower time — the
`CurrentThread()` key's proof), wedge heal exercised on the reordered path,
storms keep scheduling after a heal.

**Leg 2 — F88 regression mini-leg** (PT-54 trigger D's sharper form): roll an
interval, **load 3× inside it**, and the meteor must still arrive on the
persisted deadline — the defect's own repro is its regression test. May not be
claimed passed without the arrival observed on the pre-load deadline.

**Leg 3 — rains A/B** (PT-54 trigger E): under the rewrite, a forced collision
re-rolls immediately (wrapper Msg observed in log) and rain returns; the
migration pass moves persisted loops (the `test 2i` fixture's `toxic`
`id=nil` entry is the id-less case — it must migrate, not be skipped); the C34
stale-ACTIVE state (plant `g_RainDisaster` with a dead `main_thread`) heals
through `FinishRainProcedure`.

**Leg 4 — PT-54 triggers A and B, `Fix_DisasterPredictionLeak`** (routed here
by prompt 1's retirement record; **shape CHANGED by the taken mid-session
reconcile**):

- **A — a stranded flag heals BOTH ways.** Hand-plant
  `g_DisastersPredicted["DisasterMeteorStorm"] = true` with nothing on screen.
  (a) WITHOUT reloading, let the next NewDay tick arrive (or wait out the sol)
  → expect `DisasterPredictionLeak: cleared stranded prediction flag` and a
  clean flag dump, no reload involved. (b) Re-plant, quicksave, reload →
  the load-time sweep clears it too.
- **B — a genuine warning is NEVER cleared, by either sweep.** Quicksave
  mid-countdown on any live disaster warning, reload → the notification must
  still be counting AND its flag must still read `true`; additionally let a
  NewDay tick pass during a live countdown → flag stays `true`. A cleared flag
  under a visible countdown is a FAIL of the liveness test.
- Flag dump: `*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`

**Leg 5 — PT-20-method uninstall leg** against the rewritten modules: update →
load → save → uninstall → load. Expect: **zero orphan errors, vanilla threads
present (`Meteors`, `RainsDisasterThreads` activation threads all on vanilla
bodies), `ListFixes` clean before the uninstall, and no mod-named residue the
spec said would be gone.** Allowed residuals, by name: the
`SMRFixPack_MeteorLatch` GameVar (inert data), `SMRFixPack_loop_version`
fields inside `RainsDisasterThreads` entries (inert data), and inert layer-2
residue (incl. the route-(c) `LastTransmissionStorage` closure) — nothing
else.

PT-54 is retired INTO these legs (prompt 1's record, absorption table in
`PLAYTEST_CHECKLIST.md` §3). Status flips for F78/F81/F02/F88 ride the legs —
index row AND heading tag, both, per protocol.

## Scope fence

**In:** the four build units, the probe updates, the legs, the records.
**Out:** Tier 2 (chain prompt 5), layer 1 (⛔), the cleaner (D13, gated),
drones, the §5.4-A conversions (chain prompt 8). Found something → file it in
BUGS.md, route it per the chain README, do not fix it here.

## Stop conditions (reporting beats pushing through)

- A leg reads numbers this brief did not predict → stop at that leg, report
  with log lines.
- The uninstall leg shows mod-named residue outside the allowed list → spec
  falsification: stop, owner call.
- The migration pass meets a `RainsDisasterThreads` shape the spec did not
  anticipate → stop before writing to it; report the shape.
- Context pressure → self-split per the chain README rule 3.

## What may not be claimed

- "Repaired" — only with the uninstall leg's own log quoted.
- The F88 fix — only with leg 2's meteor arriving on the persisted deadline.
- Save-cleanliness for existing saves — only via the named mechanisms (latch,
  migration), never for layer-2/route-(c) residue (inert, accepted,
  disclosed).
- No status flips without both BUGS.md locations updated. Nothing RE-VERIFIED
  on inherited facts.
