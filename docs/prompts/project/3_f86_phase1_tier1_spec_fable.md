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

(prompt 2 appends the two measurement verdicts here)
