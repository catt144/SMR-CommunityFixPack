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

## Phase 0 — ✅ DONE 2026-08-01 (GAME session, owner at the keyboard)

**Exit gate MET.** Both facts measured in one sitting, log
`Mars.exe-20260801-14.59.57-6a22b86d.log`, recorded in ENGINE_FACTS, probe `97`
deleted in the recording commit:
1. **GT-creation ordering: DEFERRED** (two forms, incl. GT-creates-GT with a
   live `WaitMsg` receipt) → **the rains wrapper works as written; take the
   wrapper shape, not the synchronous heal.** F02's falsy-global guard is not
   load-bearing; keep it as defence in depth.
2. **Autosave hook: FIRES** — `SaveGameStart`/`SaveGameDone` with
   `autosave=true err=false`, twice, positive control present.

The one thing gating Tier-1 design choices. Prompt: **superseded 2026-08-01 —
Phases 0-4 now run as the numbered chain in `docs/prompts/project/` (prompts
2-5 and 8); the original `F86_NEXT_SESSION_PROMPT.md` is archived, split into
chain prompts 2+3 with the audit's C34 rider added to Phase 1.**

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

## Phase 5 — prelaunch save-exit work (⭐ owner directive 2026-07-31; home: **BUGS.md D13**)

**The pack must ship with its exit paved.** Two deliverables, both ready
BEFORE launch. The full record — primitives inventory, the two traps, the
second-artifact costs, the open player-story design question — lives on
**D13** (moved out of FUTURE_IDEAS 2026-08-01 so that file's "nothing here is
work" rule stays true). What this phase owns:

1. **The pack's own exit hygiene** (mostly falls out of Tiers 1+2): the
   latched heal + rains migration mean a player who **updates, loads, saves,
   then uninstalls** leaves with a save whose threads are all vanilla. Write
   this as a player-facing **uninstall procedure** in `MOD_DESCRIPTION.md`
   ("to remove the pack cleanly: update to the latest version, load your
   colony, save, then uninstall" + backup-first advice). `[FAQ]`
2. **The standalone save-rescue artifact** for saves that already lost the
   pack — the only console-viable remedy, therefore not optional.
   ⛔ **SPEC GATE (owner, 2026-08-01): scoped against what is LEFT after
   Tiers 1+2 land AND verify — never against today's leak set.** The F86
   build exists to stop creating residue; a cleaner specced now would be
   built to clean things that won't exist when it ships, and would grow to
   fit. Its target list is Tier 1/2's measured output (the uninstall leg's
   findings), so this phase CANNOT start before Phase 3 verifies — building
   in parallel means building it twice. Design question (run-after vs
   keep-installed vs pack-as-own-cleaner) is decided when the gate opens.

**Honest limits (state them wherever the cleaner is described):** a cleaner
cannot remove **inert captured frames** from old saves (invisible, inert,
harmless — layer-2 residue); it cannot resurrect **irreversible history**
(the ~15% class in STATUS's save-rescue section); and it must run at least
once inside the save to act (some mod must execute — physics, not policy).
Its own residue must be **zero** (purely synchronous, no threads, no
GameVars), and the release checklist must absorb the second artifact's full
cost: own metadata, preview, description, PDX portal pass, console cert,
version-skew statement (WORKFLOW).

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
| 5 | **Prelaunch save-exit directive**: uninstall procedure + standalone cleaner ready before launch — filed as **D13** (BUGS.md), spec gated on Tier 1/2 verification; supersedes REDESIGN §7's "no cleanup mod" (the FUTURE_IDEAS entry was MOVED to D13, not annotated in place) |
| 6 | Prior-art survey run and closed; Tier-3 control leg not required (source-verified per module) |
