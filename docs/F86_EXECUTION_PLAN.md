# F86 execution plan — from adjudicated design to shipped repair

**Written 2026-07-31 at the owner's direction, after: the adjudication
(`F86_ADJUDICATION.md`, rounds 1+2), the prior-art survey
(`PRIOR_ART_SURVEY.md`), and the owner's decisions of the same evening
(recorded in §7 below). This is the plan of record for retiring F86; the
redesign doc keeps the analysis, this file keeps the sequence. Each phase
names its session type, its inputs, and its exit gate.**

**The analysis phase is OVER.** Every load-bearing claim has been verified
twice (independent adjudication + measured round 2); the community context is
settled. Nothing below is a reading task except where explicitly marked.

---

## Phase 0 — the measurement session (GAME session, owner at the keyboard, ~30 min)

The one thing gating Tier-1 design choices. Prompt: `F86_NEXT_SESSION_PROMPT.md`.

1. **GT-creation-ordering probe.** Two console lines: create a GT thread whose
   body `ModLog`s, `ModLog` immediately after the create call, `FlushLogFile()`,
   read the order. Decides:
   - the **rains wrapper** shape — if new GT threads run at creation, the
     wrapper's collision-post fires before the vanilla loop reaches `WaitMsg`
     and the design does nothing → use the synchronous-heal shape instead
     (prior art: ChoGGi's `Fix Eternal Dust Storm`);
   - the **F02 wrapper** first-iteration edge — if run-at-creation, the
     `CurrentThread()` key misses once per restart → the wrapper's
     defer-when-global-falsy guard is load-bearing, and one short cycle per
     restart is accepted (or eliminated by assigning the global before create
     in our own restart paths).
2. **Autosave-hook leg.** The probe is already armed
   (`SMR-BugFixPack-TestKit/Code/97_SaveHookProbe.lua`). Play ~1 sol past an
   autosave, quit, read the log for `SaveGameStart`/`SaveGameDone` with
   `autosave=true`.
3. **Teardown:** delete `97_SaveHookProbe.lua` and `99_OrphanEnvProbe.lua`
   (+ their TestKit metadata lines) once both results are recorded in
   ENGINE_FACTS.

**Exit gate:** both facts in ENGINE_FACTS with log citations; probes deleted.

## Phase 1 — spec and paperwork (game-free, same or next session)

1. **Finalise the Tier-1 spec** (amend `SAVE_SAFETY_REDESIGN.md` §6.2):
   - `Fix_MeteorFrequency`: layer-3 `GetDisasterWarningTime` wrapper keyed on
     `CurrentThread() == rawget(_G,"Meteors")`, deferring when the global is
     falsy; **one-shot latched heal** (GameVar version latch — restart the
     persisted thread once per save lineage under the new version, cost one
     re-roll; this simultaneously fixes F88, guards the §2.5 upgrade path, and
     clears old bodies out of existing saves); watchdog split onto
     `Msg("MeteorDone")`/`NewDay` restarting **vanilla's** body.
   - `Fix_RainsDeadlock`: wrapper or synchronous-heal shape per the Phase-0
     probe; **migration pass** swapping persisted loops onto vanilla's
     `RainsDisasterLoop`, keyed on a **version-stamped marker** (the shipped
     boolean now means "old fixed body"), handling **id-less entries** the
     current pass skips.
   - **Orphan-gate rule** (adopted — FIX_POLICY §3a): every mod-owned thread
     body opens each wake with `if not SMRFixPack then return end` and resets
     any vanilla state it set **before** its first mod-name touch. Reorder
     `SMRFixPack.StormWedgeHeal` accordingly (the `g_MeteorStormStop` reset
     precedes the branch logging).
2. **Re-run the exposure enumeration with all five assignment shapes**
   (class-method, table-slot, global assignment, preset-field, own-thread) and
   record the durable list + dispositions in the F86 entry. Expected: confirms
   13 (CaveIns compliant).
3. Close the last route-(c) residual: read the faction-likes evaluation path
   for `Fix_LastTransmissionStorage`'s `Condition.eval` (adjudication §4.4).
4. Produce the **Tier-1 build prompt** (per WORKFLOW's brief requirements) as
   this phase's final act.

**Exit gate:** spec committed; enumeration recorded; build prompt exists.

## Phase 2 — Tier 1 build + leg (build session, then GAME session)

Build `Fix_MeteorFrequency` rewrite + `Fix_RainsDeadlock` rewrite exactly per
spec. One A/B leg for the tier (owner decision 7), including: a load-heavy
mini-leg for F88 (load 3× inside a rolled interval; meteors must still arrive
on the persisted deadline — the defect's own reproduction becomes its
regression test), and a PT-20-method uninstall leg against the rewritten
modules (expect: zero orphan errors, vanilla threads present, `ListFixes`
clean).

## Phase 3 — Tier 2 (build, then leg)

`Fix_DroneUnreachableForever` (consumer patch on `CleanUnreachables`),
`Fix_TrainWaitTime` (`AddSpentTime` wrapper), `Fix_ArrivalDeaths` half (b) —
plus the **half (a) design pass** (raw `SetPos`, still routeless),
`Opt_DroneOverhaul` layer-2 move (carve-out granted). One leg for the tier.

## Phase 4 — the conversion batch, then the held builds

The six §5.4-A wrapper conversions as one batch, single leg. Then D10/D12
unhold (the owner's gate was "repairs land and verify").

## Phase 5 — prelaunch save-exit work (⭐ owner directive 2026-07-31, supersedes the §7/FUTURE_IDEAS parking)

**The pack must ship with its exit paved.** Two deliverables, both ready
BEFORE launch, published as needed after:

1. **The pack's own exit hygiene** (mostly falls out of Tiers 1+2): the
   latched heal + rains migration mean a player who **updates, loads, saves,
   then uninstalls** leaves with a save whose threads are all vanilla. Write
   this as a player-facing **uninstall procedure** in `MOD_DESCRIPTION.md`
   ("to remove the pack cleanly: update to the latest version, load your
   colony, save, then uninstall" + backup-first advice). `[FAQ]`
2. **The standalone save-rescue mod** ("SMR FixPack Save Cleaner") for saves
   that already lost the pack — the F86 scenario. Primitives already named in
   FUTURE_IDEAS entry 5: sweep `GlobalGameTimeThreads` /
   `RestartGlobalGameTimeThread` (rebuilds vanilla bodies when the pack is
   absent), refresh `RainsDisasterThreads` entries, clear `SMRFixPack_*`
   GameVars and instance fields (the fixture measured the field inventory:
   919× `reserved_at` + 8 others). Build and test it prelaunch; publish it on
   PDX Mods so it exists the day anyone needs it. **It works on console**
   (it's just a mod — Paradox Mods reaches Xbox/PS5), which makes it the ONLY
   console-viable remedy and therefore not optional.

**Honest limits (state them wherever the cleaner is described):** a cleaner
cannot remove **inert captured frames** from old saves (invisible, inert,
harmless — layer-2 residue); it cannot resurrect **irreversible history**
(the ~15% class in STATUS's save-rescue section); and it must run at least
once inside the save to act (some mod must execute — physics, not policy).

**Release gates added (WORKFLOW):** uninstall procedure published; cleaner
built + tested; residual disclosure in MOD_DESCRIPTION; the five-shape
exposure enumeration re-run after every game update alongside the fpk diff.

## §6 — What is deliberately NOT in this plan

- **Layer 1** — stays behind the adjudication §8.5 gates. Nothing measured or
  surveyed moved toward opening them.
- **Further adversarial review** — two rounds + a survey; a third pass would
  re-read verified ground.
- **The ChoGGi conventions we examined and declined** (survey §7): upvalue
  orig-capture in persisted bodies, single-switch gating, silence-the-persist-
  errors hygiene.

## §7 — Decision log (owner, 2026-07-31 evening)

| # | decision |
|---|---|
| 1 | **F88 filed** — the per-load meteor restart gets its own F-number; fix rides the F02 rewrite (the latched heal) |
| 2 | **One-shot latched heal ADOPTED** for `Fix_MeteorFrequency` (and the pattern for rains migration) |
| 3 | **Orphan-gate rule ADOPTED** into FIX_POLICY §3a; loud-death demoted from failure mechanism to backstop |
| 4 | **BombardmentSpread: KEEP**, corrected residual (≈nil) accepted — closes adjudication D3 |
| 5 | **Prelaunch save-exit directive**: uninstall procedure + standalone cleaner ready before launch (this section) — supersedes the "parked, post-launch-only" status of FUTURE_IDEAS entry 5 and REDESIGN §7 |
| 6 | Prior-art survey run and closed; Tier-3 control leg not required (source-verified per module) |
