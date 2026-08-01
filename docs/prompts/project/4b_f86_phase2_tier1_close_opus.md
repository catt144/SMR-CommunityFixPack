# Chain 4b — F86 Tier-1 close-out: leg 5, the records, the consumption

**One-off; delete this file in your final commit. Read `README.md` in this
folder first. This is the README-rule-3 CONTINUATION of chain prompt 4
(context split, 2026-08-01): the build is DONE, legs 1–4 are PASSED on log
evidence (ledger below), and every decision is closed. This session runs
leg 5, writes the records, and consumes the chain files.**

**Staleness check: `git log --oneline -10` + `git pull`.** This prompt matches
the repo at the commit that added it. Gate: `docs/prompts/F86_TIER1_BUILD_PROMPT.md`
must still exist (this session consumes it). TestKit repo (local-only,
`C:\Dev\SMR-BugFixPack-TestKit`) sits at `26073bf` or later.

**Todo list REQUIRED before starting** (one item per commit-and-verify unit;
mark complete the moment each completes; exactly one in progress). Check
`Mars.exe` is not running before touching loadable code — though NO code
changes are expected this session; this is legs + records.

## State inherited (do not re-derive; every item is committed)

- **Build:** pack commits `d899a54` (Fix_MeteorFrequency rewrite),
  `d94ac94` (Fix_RainsDeadlock rewrite + C34 rider), `e5b4284`
  (DisasterPredictionLeak NewDay rider), `a213492` (StormWedgeHeal reorder),
  `b728d9c` (STATUS built-not-verified block), `70e6d0c` (leg-3 id-less
  clause amended, owner-cleared), `94cfa46` (F89 filed), `212c841`
  (ENGINE_FACTS: Msg/OnMsg env-specials). TestKit `09a4f47..26073bf`
  (probe realignment at 78, ENV_SPECIALS guard, digger-noise fix).
- **Spec:** `SAVE_SAFETY_REDESIGN.md` §6.2a (final). **Build prompt:**
  `F86_TIER1_BUILD_PROMPT.md` (leg definitions; its leg-3 id-less clause
  carries the amended reading note).
- **PROBE SWEEP: clean** — zero hits both repos, re-verified at the F89
  filing commit. Sweep again before recording leg 5 (mechanical:
  `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`).

## Evidence ledger — legs 1–4 PASSED (2026-08-01 sitting, owner at keyboard)

Save lineage `save_game_id HdmSxGs6kyd0uz6-` (test-2, map
BlankBigCanyonCMix_09). Logs: `Mars.exe-20260801-16.42.31` (step 0 first
load) and `Mars.exe-20260801-17.11.08` (main sitting). Quote these when
flipping statuses; do NOT re-run the legs.

**Step 0 (PASS):** first load — `MeteorFrequency: one-shot heal — persisted
Meteors thread was alive; restarting onto vanilla's body (latch false ->
1.0.1)` once; `RainsDeadlock: 'normal' rain loop migrated onto vanilla's
body (settings 'Normal_VeryLow', version 1.0.1)`; `toxic` correctly silent
(vanilla empty fill-in, amended reading, commit `70e6d0c`); zero Lua errors.
Reloads: NO second heal, NO re-migration (stamps honored round-trip).
`*r SMRTest.RunAll()` = **63 PASS / 0 FAIL / 15 SKIP / 0 ERROR**;
ListFixes `68/74 active` clean.

**Leg 1 (PASS):** cadence gaps **75h** (t=216351730→218608231, pristine) and
**83h** (t=227810769→230312200, post-recovery, inside the predicted window),
plus **72h** (→232476636) — all in the 65–90h roll. Wedge heal exercised
live on the REORDERED path (forced storm): `0:20:28.442 WEDGE confirmed …
alive but stuck); healing` → `scheduler thread restarted` →
`0:20:28.517 DisasterPredictionLeak: meteor storm ended — its notification
and prediction flag are cleared` (vanilla end path ran) → `0:20:29.230 …
released through the vanilla end path` (logging LAST — §6.2a-D order
visible). Storms keep scheduling: `IsValidThread(MeteorStorm)` = true.
Storm-warning timing (the CurrentThread key's proof, three forms): probe
keyed/unkeyed discrimination PASS; live read
`GetDisasterWarningTime(GetMeteorsDescr())` from a non-Meteors thread =
**2250000** (75h tower-cap, NOT the keyed 2700000); natural storm warning
UI countdown read **"Starts in 3 Sols 2 h" ≈ 74h** ✓.
**F89 discovered and FILED mid-leg** (`94cfa46`): drain-loop wedge on the
singles path (strike #2's call never returned; 192h silence, descriptor
valid, Atmosphere 59.37%); F02 watchdog detected at its 189h threshold
(`ALIVE but stuck`), restarted, cadence resumed — the insurance proved
itself. Strike #3 (t=225356557) attributed to the Singularity story bit
(event spawners enumerated from Src; only story-bit line sits between #2
and #3). Watchdog nuance recorded in F89: event strikes re-arm its
liveness clock.

**Leg 2 (PASS — F88's own repro):** strike #1 t=216351730 → quicksave →
**3 loads** (three `Load Game` blocks, ZERO pack lines — no heal, no
migration) → strike #2 t=218608231, **`+2256501 ms = 75 game hours`** on
the persisted deadline. The F88 claim is now evidenced.

**Leg 3 (PASS):** collision arrived NATURALLY —
`0:20:06 RainsDeadlock: rain activation collided with an active/predicted
disaster — posting RainDisasterEnd so the loop re-rolls`; rain returned
(recurring on-and-off rains observed = the migrated loop lapping
healthily). Migration: 'normal' stamped 1.0.1 (+ probe live drive incl.
id-less shape + legacy-boolean clear). C34 stale-ACTIVE: planted
`g_RainDisaster="toxic"` + dead main_thread → on reload
`0:23:39 … stale-ACTIVE rain 'toxic' (main_thread dead) — healing through
vanilla FinishRainProcedure (C34)`; `g_RainDisaster` read false after.

**Leg 4 (PASS, both halves, changed shape per §6.2a-C):**
A(a) planted flag cleared by the NewDay sweep with NO reload
(`cleared stranded prediction flag 'DisasterMeteorStorm'` at 0:02:24);
A(b) re-planted, no sol tick either side, cleared INSIDE the load block
(0:10:47). B (liveness): live storm countdown; quicksave/reload → NO clear
line, dump `DisasterMeteorStorm = true`; sol ticked during live countdown
(owner confirmed) → still `true`. Genuine warnings are never touched.

**Natural storm cycle (bonus headline — BOTH heal branches now live-proven):**
The scheduler's own storm arrived: warning UI countdown ≈74h (the key's
proof, third form), storm call printed `t=234154036`, ran its duration, and
WEDGED at end (storms are 2-for-2 wedging in this colony — F78's repro is
robust). The heal took the **force-clean branch** this time:
`1:56:48.368 WEDGE confirmed … healing` → `scheduler thread restarted` →
`1:57:01.692 forced storm state clean (8 stray meteor object(s) removed)` —
stop-flag and GameVar resets BEFORE any mod-name touch, Note last, and the
13s restart→Note spread is exactly the 10×4s pulse window. Together with the
forced storm's **release-branch** heal earlier, both §6.2a-D completion paths
have now run live on the reordered body. Regular cadence continued cleanly
around the storm (86.7h scheduler gap interleaved with the storm call).
Second natural rain collision also handled (`1:50:10`).

## The job, in order

1. **Leg 5 — the PT-20-method uninstall** (owner at keyboard). Procedure:
   - Pack ON: play ~2 min → `SMRFixPack.ListFixes()` clean → **save under a
     NEW name** (`T1-UNINSTALL`) — the re-cut article carrying the
     new-shape state. Quit to menu.
   - Mod Manager: disable **Community Fix Pack only** (TestKit stays ON).
     **Full game restart.** Load `T1-UNINSTALL`.
   - ~10 min ordinary play (build, salvage, a sol passes, save+reload once).
     Old bugs returning is expected; corruption/errors are not.
   - The hunt: `*r ConsolePrint("Meteors body: " ..
     tostring(GlobalGameTimeThreadFuncs and GlobalGameTimeThreadFuncs.Meteors))`
     (vanilla function); the two `IsValidThread` reads (Meteors,
     MeteorStorm — vanilla threads present); `SMRTest.FixtureCarry()`
     (residue by name); then **a full meteor cycle at ultra (65–90h game)**
     and read the whole log: zero orphan errors, zero lines naming
     `SMRFixPack`.
   - **Allowed residuals, by name, NOTHING else:** `SMRFixPack_MeteorLatch`
     (inert GameVar), `SMRFixPack_loop_version` fields inside
     `RainsDisasterThreads` entries (inert data), inert layer-2 residue
     (incl. the route-(c) `LastTransmissionStorage` closure — adjudication
     §4.4, recorded as compliant). Anything else mod-named = **spec
     falsification: STOP, report with log lines, owner call.**
   - Re-enable the pack afterwards.
2. **Records** (one commit, `PROBE SWEEP:` line required):
   - **BUGS flips, index row AND heading tag, BOTH, per protocol:**
     F02 → `tested` (Tier-1 legs 1+2+5, quote the log evidence from the
     ledger); F78 → `tested` (leg 1 wedge-heal + leg 4 absorbed PT-54);
     F81 → `tested` (legs 3+4); F88 → `fixed`→`tested`-equivalent per its
     entry's own bar (leg 2's 75h-across-3-loads IS the named condition —
     quote it). C34 disposition is already recorded (`70e6d0c`) — add the
     leg-3 heal observation. PT-54's retirement is made good — note it on
     the F78/F81 entries per the build prompt.
   - **STATUS.md:** rewrite the F86 block to post-Tier-1 truth: what
     shipped (keep the built list), what the legs read (from the ledger),
     F89's story, what Tier 2 still owes. Counts: 101 rows (89 F + 12 D)
     already recorded at `94cfa46`.
   - **`MOD_DESCRIPTION.md`:** leg 5 PASS on its own log → delete the
     `[DRAFT NOTE — CONDITIONAL]` marker and KEEP the `[FAQ]` no-precedent
     sentence (owner pre-authorized, prompt-1 note in chain file 4). Leg 5
     FAIL → leave the marker exactly where it is. Do not soften the
     sentence either way.
   - **`PLAYTEST_CHECKLIST.md`:** PT-54 absorption table (§3) — mark the
     five triggers' absorbing legs as RUN with this sitting's date/logs.
3. **Consumption:** append the outbox to
   `5_f86_phase3_tier2_build_opus.md` `## Notes from upstream` (what
   landed with commits, leg numbers + log names, F89 pointer, the
   Msg/OnMsg env-special fact, anything Tier-2 must respect — e.g. legs
   run on the test-2 lineage; D10/D12 unhold is prompt 5's record). Then
   **delete `F86_TIER1_BUILD_PROMPT.md` AND this file in that same
   commit.** README row 4 gets its ✅. Commit, push.

## Scope fence

**In:** leg 5, the records above, the consumption. **Out:** Tier 2
(prompt 5), layer 1 (⛔), D10/D12, drones, the cleaner (D13), any new code.
Discovered defects → file in BUGS.md, route per README rule 2.

## Stop conditions

- Leg 5 shows mod-named residue outside the allowed list → spec
  falsification: stop, report, owner call. No flips, no draft-note
  deletion, chain halts until resolved.
- Any leg-5 error naming pack code → same.
- Context pressure → self-split again per README rule 3 (`4c_…`).

## What may not be claimed

- "Repaired" — only with leg 5's own log quoted.
- No status flips without BOTH BUGS locations updated. Nothing RE-VERIFIED
  on inherited facts — the ledger above is this sitting's measurement, cite
  it as such (recorded 2026-08-01, logs named).
- The no-precedent sentence ships only on a leg-5 PASS.

## Notes from upstream (chain prompt 4 / build session, 2026-08-01)

1. **Model routing:** the build session (Fable) recommends this close-out
   for the standard model — every decision is closed; the work is guided
   execution + careful records. Heavy anomalies (should any appear in
   leg 5) go to stop-and-report, not to on-the-spot redesign.
2. **F89 masking nuance** is recorded in the F89 entry: event-spawned
   meteors re-arm the F02 watchdog's liveness clock (any meteor posts
   MeteorDone), stretching detection latency in event-heavy periods.
   Accepted-by-design; no action owed.
3. **TestKit facts a future probe author must know** (all committed):
   `Msg`/`OnMsg`/`rawget`/`getmetatable`/`os`/`_G` are per-env specials —
   ENV_SPECIALS guard refuses them in SetGlobal/WithGlobals (ENGINE_FACTS
   has the full mechanism); FromFixPack defers a retail SKIP that REPLACES
   a probe's verdict — gate such checks on `SMRTest.GetDebug()`; bare
   console RunAll has no thread context — `*r SMRTest.RunAll()` is the
   full-coverage form.
4. **The natural storm's UI countdown (74h) was read with the pack on** —
   if Tier-2 sittings see storm warnings near ~90h, that's the wrapper key
   leaking and F02's entry says where to look.
