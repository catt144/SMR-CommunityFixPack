# Chain 2 — F86 Phase 0: the two engine measurements (OWNER AT THE KEYBOARD)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** This is the Phase-0 half of the archived
`docs/archive/F86_NEXT_SESSION_PROMPT.md` (split into chain prompts 2+3 on
2026-08-01); content is carried faithfully — where this file and that one
disagree, THIS file is current.

**Staleness check: `git log --oneline -10` + `git pull`.** F86 is the single
release blocker; the analysis is finished and twice-verified; your job is
`docs/reports/F86_EXECUTION_PLAN.md` **Phase 0 only** (prompt 3 owns Phase 1).

## Read first (nothing else required)

1. `docs/reports/F86_EXECUTION_PLAN.md` — Phase 0.
2. `docs/reports/F86_ADJUDICATION.md` §4.1, §8.4-8.6 — why each measurement
   gates a design.
3. `docs/agent/ENGINE_FACTS.md` (2026-07-31 entries) + `FIX_POLICY.md` §3a.

## Standing rules

Todo list per WORKFLOW element 1. Console lines for the owner: **one command
per line**. Never modify the game directory. `ModLog` (never `print`) for
anything that must reach the log; `FlushLogFile()` before reading
mid-session; `IsValidThread(x) or false` when displaying thread validity.
Docs never lag findings — each probe result lands in ENGINE_FACTS in the same
commit as its log evidence.

## 0.0 ⛔ Stale-probe gate FIRST (HARD RULE)

`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` → todo list.
**Expected for THIS session: exactly ONE hit — `97_SaveHookProbe.lua`**
(declared: it IS the 0.2 instrument). Chain prompt 0 already deleted
`99_OrphanEnvProbe.lua`; if it is still present, prompt 0 did not complete —
STOP and check the chain state. Any other hit: repair before testing. Every
result commit carries the `PROBE SWEEP:` line.

## 0.1 GT-creation ordering — does `CreateGameTimeThread` run the body before the creating statement continues?

Hand the owner this as ONE console line, in a loaded colony, game UNPAUSED
(a paused game may defer GT scheduling and mask the answer — if the result
looks deferred, re-run unpaused before recording):

```
CreateGameTimeThread(function() ModLog("SMRPROBE-GTORDER: thread body ran") end) ModLog("SMRPROBE-GTORDER: statement after create ran")
FlushLogFile()
```

- body line FIRST → **run-at-creation**: the rains wrapper's naive shape is
  DEAD (its Msg posts before the vanilla loop can WaitMsg) — the Tier-1 spec
  takes the synchronous-heal branch; the F02 wrapper's defer-when-global-falsy
  guard is load-bearing.
- statement line FIRST → **deferred**: both authorised shapes work as
  written; the F02 guard stays anyway (defence in depth).
- Record verdict + log filename in ENGINE_FACTS. **A test that cannot
  discriminate is worse than none** — interleaving doubt → say so and re-run;
  do not guess.

## 0.2 The autosave hook (probe already armed)

`97_SaveHookProbe.lua` is live. The owner plays ~1 sol past an autosave (or
forces one), quits to desktop; read the newest log for
`SaveGameStart`/`SaveGameDone` with `autosave=true`. Record in ENGINE_FACTS
(upgrade or correct the "same path, source-only" entry).

## 0.3 Teardown

Delete `97_SaveHookProbe.lua` + its TestKit metadata/items lines in the same
commit as the recorded results.

## Scope fence

**In:** the two measurements, ENGINE_FACTS updates, `97` teardown.
**Out:** ANY fix-pack `Code/` change; Phase 1 (prompt 3 owns it); anything
drone. Interesting out-of-scope finding → file it, route it.

## Stop conditions

- 0.1 refuses to discriminate after two attempts → record "unresolved" in
  ENGINE_FACTS, note to prompt 3 that the rains repair MUST take the
  synchronous-heal shape (needs no ordering guarantee), and say so plainly.
- Owner unavailable → this session cannot run; stop, nothing else is
  runnable here.

## What may not be claimed

Nothing is MEASURED without a log filename + line read this session. Nothing
is RE-VERIFIED whose chain includes an inherited recorded fact not re-derived
(ENGINE_FACTS has been wrong twice before).

## On completion

Outbox → `3_f86_phase1_tier1_spec_fable.md`: both verdicts (or the
"unresolved → synchronous heal" instruction), the ENGINE_FACTS entry names,
the log filenames. Delete this file, commit, push.

## Notes from upstream

### From prompt 0 (2026-08-01) — harness gate discharged, probe `99` gone

**Your §0.0 expectation is now correct as written: the sweep returns exactly
ONE hit, `97_SaveHookProbe.lua`.** Verified after the deletion, both repos.
`99_OrphanEnvProbe.lua` and its `metadata.lua` line are deleted (TestKit commit
`57247ee`, local-only). Nothing in the fix pack's `Code/` carries the marker.

**The owed F49(a)-strip A/B code-gate leg RAN CLEAR** — 2026-08-01 14.15,
unattended, default config, log `Mars.exe-20260801-14.15.08-6a22b86d`.
`fix pack present: 68/74 fixes active` · `---- 63 PASS, 0 FAIL, 15 SKIP, 0
ERROR ----` over 78 verdict lines · zero `[CommunityFixPack]`
error/disabled/FAILED lines · exactly ONE real fingerprint change vs the
2026-07-31 18.44 default-config reference (TrainMinors' palette clause gone) plus
the two known RNG lines. Numbers and noise inventory on the F49 BUGS entry.
**Nothing is owed on the harness side.**

**Two things worth knowing before you run 0.2:**

1. **`97` is passive and quiet in an unattended leg.** Across the whole 14.15
   log it emitted one line — `probe loaded — waiting for LoadGame /
   SaveGameStart / SaveGameDone` — because the autorun harness starts a NEW
   game and never saves. So on your leg, an absent `SaveGameStart FIRED` line is
   only an answer if a save actually happened; the positive control
   (`LoadGame FIRED`) is what tells you the probe is alive at all. Do not read
   the unattended silence this leg produced as evidence about the save hook.
2. **The autorun harness never loads a save** (`95_AutoRun.lua` →
   `NewGame()` + `GenerateCurrentRandomMap()`). That is why deleting `99` could
   not disturb this leg. But note the shape for your own work: any save written
   while `99` was armed carries a persisted `SMRTestOrphanEnvProbe` game-time
   thread whose body no longer exists. If you load an old save and see a nil-body
   or missing-permanent line naming that thread, it is `99`'s residue, not a
   finding.

**Baseline-noise reference for your leg** (from 14.15, all known/documented): 60
`Flight.lua objects_to_mark`/`objects_to_unmark` lines, three GameInit nil-calls
(`CreateResourceRequests`, `ApplyToGrids`, `BuildWaypointChains`), 2
`ResManager LawOfficeDoor`, the `no debug.getinfo (mod sandbox)` notice, and one
`MeteorFrequency: WATCHDOG … probe-stall` line — that last one appears
identically in the 2026-07-31 leg, so it is pre-existing and not a signal.

**One TestKit housekeeping item, routed to you because you own the TestKit
next.** `Code/99_FixtureCarry.lua` sits **uncommitted** in the TestKit working
tree — a prior session's real repair wrapping two `IsValidThread(...)` reads in
`... or false` (the engine returns NO VALUE for an invalid thread, so bare
`tostring()` throws "value expected"; the same fact your own §preamble cites).
Prompt 0 left it alone as out of scope rather than adopt someone else's
unverified edit. It is inert for legs — the file only defines
`SMRTest.FixtureCarry()` — but the tree should not stay dirty. Commit it when you
next touch the TestKit, or discard it if you judge it wrong.

*(Nothing found here was checklist-relevant, so nothing was copied to prompt 1.)*

### From prompt 1 (2026-08-01) — the §4 decision is MADE, and two things about your keyboard session changed

**1. FIX_POLICY §4 is AMENDED AND IN FORCE** (applied verbatim from
`REACHABILITY_AUDIT.md` §4 under the owner's blanket pre-clearance; the F49(a)
contradiction died with the guard strip). It does not change what you measure,
but it changes what any finding you file is judged by: a defect claim now needs
a positive intent statement with a named hard tell, and a reachability tier,
before anything is written. **If Phase 0 turns up a defect, file it to that
standard** — prompt 3 inherits the amended bar when it specs.
*One consequence, for your awareness only, already routed to prompt 7:* F29 and
F57(a) are R3 fixes shipped as §1.5 replacements, the combination the new R3
bullet makes conditional on an owner decision. Not yours; do not act on it.

**2. Checklist facts you should know at the keyboard:**

- **PT-54 is RETIRED UNRUN** — nobody runs the wave-6 disaster tests against
  the current bodies again. If the owner asks why the disaster tests vanished
  from the checklist: the code under them is being replaced, and the intent
  moved onto the Tier-1 build's own legs (`PLAYTEST_CHECKLIST.md` §3 carries
  the trigger-by-trigger table).
- **Your §0.1 measurement is what decides the rains shape**, and prompt 3's
  spec now also carries two PT-54 legs I routed there against
  `Fix_DisasterPredictionLeak`. Nothing about that changes your job; it is why
  prompt 3's inbox is longer than you left it.
- **Four cheap needs-eyes riders were added** (F35 live-label, C32
  label-membership, F80 enumeration tap, F82 timing). **One is worth knowing
  while a colony is up in front of the owner: the F35 read must be taken with
  NO reload** — our sanitizer runs on every load and would silently repair the
  very thing the reading is looking for. If the session happens to sit in a
  colony that is about to research Frictionless Composites, that reading is 30
  seconds and it is otherwise hard to schedule. Entirely optional; do not
  extend the sitting for it, and do not let it displace the two measurements.
- **The `97` teardown you owe is unchanged.** The stale-probe sweep still
  returns exactly one hit, `97_SaveHookProbe.lua` — re-verified this session
  (game-free, no legs run).
