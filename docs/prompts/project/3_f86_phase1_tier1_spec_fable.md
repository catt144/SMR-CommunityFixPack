# Chain 3 — F86 Phase 1: the final Tier-1 spec, the enumeration re-run, and the build prompt

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** Game-free. This is the Phase-1 half of the archived
`docs/archive/F86_NEXT_SESSION_PROMPT.md` (split 2026-08-01), **amended by
the bug-list audit's packed-source findings** — the amendments are marked ⭐
below and are new obligations, not suggestions.

**Staleness check: `git log --oneline -10` + `git pull`.** Inputs you MUST
have from prompt 2's outbox (below): the GT-creation-ordering verdict and the
autosave-hook fact. If the inbox is empty, prompt 2 has not run — stop.

## Read first

1. `docs/reports/F86_EXECUTION_PLAN.md` Phase 1 (the authority for this session).
2. `docs/reports/SAVE_SAFETY_REDESIGN.md` §6 (the authorised build you are speccing)
   + §5 (the sweep results).
3. `docs/agent/FIX_POLICY.md` §3a as amended; `ENGINE_FACTS.md` incl. prompt 2's
   new entries.
4. ⭐ `docs/reports/BUG_LIST_AUDIT.md` §9 + the BUGS.md C34 entry — the
   packed-source findings this spec must absorb.

## Jobs (todo list first; one item per commit-and-verify unit)

1. **Amend `SAVE_SAFETY_REDESIGN.md` §6.2 into the FINAL Tier-1 spec:**
   - `Fix_MeteorFrequency`: layer-3 `GetDisasterWarningTime` wrapper keyed on
     `CurrentThread() == rawget(_G,"Meteors")`, deferring when the global is
     falsy; **one-shot latched heal** (GameVar version latch — restarts the
     persisted thread once per save lineage per version; simultaneously fixes
     F88, guards the §2.5 upgrade path, clears old bodies from existing
     saves); watchdog split onto `Msg("MeteorDone")`/`NewDay` restarting
     **vanilla's** body.
   - `Fix_RainsDeadlock`: wrapper or synchronous-heal shape **per prompt 2's
     verdict**; migration pass swapping persisted loops onto vanilla's
     `RainsDisasterLoop`, keyed on a version-stamped marker, handling the
     id-less entries the current pass skips.
   - ⭐ **The C34 rider (audit adoption decision):** the rains migration/heal
     ALSO clears the stale-ACTIVE class — `g_RainDisaster` set with a dead
     `main_thread` — healed through vanilla's own `FinishRainProcedure`
     (`TerraformingDisasters.lua:247-274`), plus the minor structure repairs
     recorded on C34 (missing `RainsDisasterThreads` table, dead
     `soil_thread`s, invalid `g_RainDisaster` values). Same file family, same
     A/B — it rides, it does not get its own module.
   - ⭐ **Design input, not obligation:** fredware's collision handling
     re-rolls immediately instead of waiting out a timeout (BUG_LIST_AUDIT §9
     A3). Consider it when choosing the rains shape; the Phase-0 verdict
     still rules.
   - ⭐ **Pre-cleared option (owner blanket, README):** a §3a-compliant
     MID-SESSION reconcile for the F81a flag class (OnMsg-based — e.g.
     NewDay — never a replaced waiting body): our current sweep is
     PostLoadGame-only, so a flag stranded mid-session waits for the next
     load. Include it if this session judges it sound; skip with one line of
     reasoning if not. Either answer is fine — the clearance removes the
     ask, not the judgment.
   - ⚠ Do NOT copy fredware's `WaitCurrentDisaster`/loop-body replacements —
     they are §3a violations (mod code on persisted waiting stacks); the
     audit records them as HIS exposure, not a pattern.
   - **Orphan-gate rule** (FIX_POLICY §3a): every mod-owned thread body opens
     each wake with `if not SMRFixPack then return end` and resets vanilla
     state BEFORE its first mod-name touch; reorder `SMRFixPack.StormWedgeHeal`
     accordingly. State each module's compliance explicitly in the spec.
2. **Re-run the exposure enumeration with all five assignment shapes**
   (class-method / table-slot / global assignment / preset-field /
   own-thread) over `Code/` — note it now contains the 2026-08-01 F49(a)
   strip, so re-derive, don't inherit. Record the durable list + dispositions
   on the BUGS F86 entry. Expected 13; a 14th that is NOT layer-2 compliant →
   file it and STOP (owner re-scope call).
3. **Close adjudication §4.4**: read the faction-likes evaluation path for
   `Fix_LastTransmissionStorage`'s `Condition.eval`; record either way.
4. **Write `docs/prompts/project/4_f86_phase2_tier1_build_fable.md`'s
   payload: `F86_TIER1_BUILD_PROMPT.md`** (in `docs/prompts/`), compliant
   with WORKFLOW's brief elements, carrying: the final spec, the orphan-gate
   rule, the StormWedgeHeal reorder, the F88 regression leg (load 3× inside
   a rolled interval — the defect's own repro becomes its regression test),
   and the PT-20-method uninstall leg. Note in it that PT-54 was retired into
   these legs (prompt 1's record).

## Scope fence

**In:** the spec amendment, the enumeration, §4.4, the build prompt.
**Out:** ANY `Code/` change (the pack is untouchable this session); layer 1
(⛔ not to be built — do not re-propose); the cleaner (D13, gated); drones.

## Stop conditions

- Enumeration finds a non-compliant 14th → file, stop, owner call.
- The Phase-0 verdict is missing or ambiguous → the rains spec takes the
  synchronous heal (the shape needing no ordering guarantee) and says so.

## What may not be claimed

The spec may not claim save-cleanliness for existing saves without naming the
clearing mechanism (latched heal / migration), and may not claim it for
layer-2 residue at all (inert, accepted, disclosed). Nothing is RE-VERIFIED
on inherited facts.

## On completion

Outbox → `4_f86_phase2_tier1_build_fable.md`: point at the build prompt,
list any spec decisions the build session must not re-litigate. Delete this
file, commit, push.

## Notes from upstream

**From prompt 1 (2026-08-01) — PT-54 is retired, and two of its five triggers
are NOT absorbed by the legs you are about to specify. They are yours to place.**

PT-54 was retired unrun (record: `PLAYTEST_CHECKLIST.md` §3, full text kept in
`PLAYTEST_ARCHIVE.md`, notes on BUGS F78/F81). Triggers **C**, **D** and **E**
ride the Tier-1 legs you are writing (A/B pair · F88 load-3× regression ·
uninstall) — job 4 already tells you to say so in the build prompt.

**Triggers A and B do not, and dropping them would be the retirement claiming
more than it can.** They test `Fix_DisasterPredictionLeak`, which is in no tier
— Tier 1 neither rewrites nor deletes it — so no Tier-1 leg touches it by
construction, and its wave-6 probe asserts the mechanism synthetically only.
Add both to `F86_TIER1_BUILD_PROMPT.md` as legs (they are cheap: the build
session is already loading disaster saves):

- **A — the load-time reconciliation heals a stranded flag.** Hand-plant
  `g_DisastersPredicted["DisasterMeteorStorm"] = true` with nothing on screen,
  quicksave, reload → expect `DisasterPredictionLeak: cleared stranded
  prediction flag` and a clean flag dump.
- **B — a genuine warning is NEVER cleared.** Quicksave mid-countdown on any
  live disaster warning, reload → the notification must still be counting AND
  its flag must still read `true`. A cleared flag under a visible countdown is
  a FAIL of the sweep's liveness test.
- Flag dump: `*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`

**This is also the reason the routing is to you and not to the checklist:** your
job 1 carries the pre-cleared option to add a **mid-session** reconcile to this
exact flag class. If you take it, A and B change shape (a stranded flag must
heal without a reload) and the legs must say so; if you skip it, they stand as
written above. Either way they are specified where the decision is made.

### From prompt 2 (2026-08-01) — Phase 0 is MEASURED, and both answers are the permissive ones

**One sitting, owner at the keyboard, one log:
`Mars.exe-20260801-14.59.57-6a22b86d.log`** (a loaded colony, unpaused, fix pack
+ Test Kit enabled). ENGINE_FACTS entry names, both new bullets in
`docs/agent/ENGINE_FACTS.md`:
**"`CreateGameTimeThread` DEFERS — the body does NOT run before the creating
statement continues"** and **"THE PRE-SAVE HOOK COVERS AUTOSAVES —
`SaveGameStart`/`SaveGameDone` fire on the autosave path with `autosave=true`"**.
`F86_ADJUDICATION.md` §4.1 and §4.2 are flipped to CLOSED; the execution plan's
Phase 0 gate is marked MET; the F86 BUGS entry carries the answer inline.

**1. §0.1 GT-creation ordering → DEFERRED. Your spec takes the WRAPPER shape.**

- Log lines, form 1 (creator = console context), `Lua 0:01:43:086`:
  `SMRPROBE-GTORDER: statement after create ran` **then**
  `SMRPROBE-GTORDER: thread body ran`.
- **I did not stop there, and you should know why the second form exists.** Form
  1 creates the GT thread from the console; every call site you are speccing
  creates one *from inside another GT thread*
  (`TerraformingDisasters.lua:310-316`). Treating form 1 as the answer for form 2
  would have been an inference, which is the exact move that has put a wrong
  fact in ENGINE_FACTS before. Form 2 reproduces vanilla's shape — outer GT
  thread creates inner GT thread, inner posts a `Msg`, outer `WaitMsg`s with a
  5000 ms timeout — and its verdict is order-independent (receipt vs timeout,
  not log line order). Result at `Lua 0:04:29:476`: `outer past create, about to
  WaitMsg` → `inner ran, posting` → **`outer GOT the message`**.
- **Consequences you can spec on:**
  - `Fix_RainsDeadlock` takes the **authorised wrapper shape as written** — wrap
    `RainsDisasterActivation`, post `RainDisasterEnd` on the collision
    early-return, vanilla's loop stays. **The synchronous-heal branch is NOT
    needed** and the ChoGGi-style fallback is off the table for this reason
    (adjudication §4.1's first bullet). The `Sleep(1)`-first micro-thread variant
    is likewise unnecessary — do not spend the 1 ms own-thread window on it.
  - `Fix_MeteorFrequency`'s **F02 defer-when-`rawget(_G,"Meteors")`-falsy guard
    is not load-bearing**: under deferral, `RestartGlobalGameTimeThread`
    (`_fixup.lua:21`) always assigns the global before the persisted body can
    make its first `GetDisasterWarningTime` call, so the `CurrentThread()` key
    cannot miss on iteration 1. **Keep the guard anyway as defence in depth** —
    that was the standing instruction and the measurement does not retire it —
    but do **not** write a spec that spends anything to buy the "one short cycle
    per restart" it was hedging; that cycle does not occur.
  - Scope limit, so you do not over-read it: this measures the **create call**,
    not scheduler latency. In both forms the body ran inside the same
    log-timestamp group — "deferred" here means next scheduler opportunity, not
    "much later". Nothing in your spec should assume a long window.

**2. §0.2 autosave hook → FIRES, cleanly.** `SaveGameStart FIRED — … 
SavingGame=true` then `SaveGameDone FIRED — name=Autosave Sol 285.savegame.sav
autosave=true err=false` (`Lua 0:02:29:324`/`0:02:30:011`), and a second
identical pair at `0:02:37:203`/`0:02:37:846`. Positive control
`LoadGame FIRED (positive control)` present in the same log, so the probe was
demonstrably alive.
**State the trigger honestly if you cite this:** both autosaves were
**console-forced** with `CreateRealTimeThread(Autosave)`; no naturally-timed
autosave was observed. That is the engine's own invocation — the periodic
autosave thread does literally `CreateRealTimeThread(Autosave)`
(`Savegame.lua:1550-1555`) and `Autosave` → `SaveAutosaveGame` (`:1450-1453`,
which is what sets `params.autosave = true`) → `DoSaveGame` — so nothing
downstream of the trigger differs, and `CanAutosave()` gates only *whether* the
periodic thread fires. **Note what this does and does not unlock:** layer 1
stays barred (§8.5's four-part gate; this measurement satisfies only gate #2's
autosave half, and §4.1 satisfies its other half). Do not spec a
tear-down-on-save scheme — and if you are tempted, the ⚠️ on the existing
ENGINE_FACTS entry still stands: autosaves fire ~once a sol, so a handler that
*restarts* a long-interval loop resets its timer forever.

**3. Housekeeping done, so you inherit a clean board.** `97_SaveHookProbe.lua`
and its `metadata.lua` line are deleted (TestKit commit, local-only). **The
stale-probe sweep now returns ZERO hits in both repos** — you are game-free so
you run no leg, but the build prompt you write must tell prompt 4 to expect
`PROBE SWEEP: clean`, not the one declared hit the last three sessions saw. The uncommitted
`99_FixtureCarry.lua` repair prompt 0 routed to me is committed (the
`IsValidThread(...) or false` fix; the TestKit tree is clean).

**4. Nothing was found out of scope, and nothing is owed back to me.** No defect
turned up, so the amended FIX_POLICY §4 bar was not exercised. The optional F35
live-label rider was not taken — the sitting was a loaded save on
`BlankBigCanyonCMix_09` at Sol 285 and I would have had to extend it, which
prompt 1 explicitly forbade.


