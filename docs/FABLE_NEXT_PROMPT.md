# Continuation prompt (model-agnostic) — PLAYTEST STANDBY (rewritten 2026-07-30, mid-playtest)

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks the model per task and everything here works identically on
either.** This is the ONE live prompt. **Start with `git log --oneline -5` +
`git pull`** in case another session ran since this prompt was written — this
file goes stale the moment another session commits. (The filename keeps its
historical FABLE_ prefix so existing references stay valid — nothing in it is
model-specific.)

## Where the project stands (2026-07-30, mid-playtest — a live sitting is in progress)

**Build state: 75 registered modules — 69 active by default, 6 opt-in via
Options → Mod Options (D05, `tested`), plus the D09 stat-dials module
(`Opt_DroneStatDials`, BUILT 2026-07-29 late: Drone speed 1x/2x/3x/5x and
Drone carry +0/+1/+2 dropdowns, active-at-base = vanilla, PT-56 owed).
Everything committed and pushed.**
**The post-D09 A/B set RAN IN FULL — nothing is owed to the harness and the
code gate is CLEAR.** Current numbers (**77 probes**): baseline
**1 / 61 / 15 / 0** · default config, six toggles OFF **62 / 0 / 15 / 0 at
69/75** · all six toggles ON + dials **67 / 0 / 10 / 0 at 75/75**. Logs clean
in every leg; the four engine error signatures appear in both halves of the
pair. (Pre-D09 reference, 76 probes: 1/60/15/0 · 61/0/15/0 at 68/74 ·
66/0/10/0 at 74/74.) The audit-remediation Code/ changes are probe-run, not
just parse-swept. **The set earned its keep:** all three wave-6 probes had been
silently reporting SKIP (they ran every assertion then fell off the end of
`run()` with no verdict; `SMRTest.Run` turns nil into SKIP), so wave 6's
automated coverage was imaginary until the repair (TestKit `d701595`) — the
fixes themselves were correct throughout.

**Account state: the six Mod Options toggles were OFF as of 2026-07-30, but a
live PT-55 sitting has been flipping them** — **read the state, never assume
it.** `SMRFixPack.ListFixes()` or `SMRFixPack.fixes.<Id>.status`. The two D09
dials default to base and are not part of the six.

**A whole-mod audit ran 2026-07-29 and its Phase 1-3 remediation is DONE
(same day, one-off fix session).** Findings + the plan (all Phase 1-3 boxes
ticked) live in `docs/AUDIT_FINDINGS.md`; Phase 4 (core helpers, merges,
deactivation surface) stays deferred pending a user go-decision. Playtest
consequences NOW:

1. **The opt-module first-enable defect is FIXED (audit 1.3) and CONFIRMED IN
   PLAY (PT-55, 2026-07-30):** a first mid-session enable of ClassicRockets /
   ResidencyControl / MultipleSuns works without a relaunch — hooks install at
   file scope. Do NOT treat a dead first-enable as legacy behavior any more; it
   would be a regression. The two known-and-explained exceptions are the D04
   panel-binding timing and the D01 parked-rocket demand refresh — both in the
   PT-55 section above.
2. The audit-era warning about running the fix prompt concurrently is
   obsolete — that one-off executed and deleted itself 2026-07-29.

## ⚠️ PT-55 — WHAT IS STILL OWED TO CLOSE IT (tell the user this explicitly)

**PT-55 is PARTIALLY run (2026-07-30) and is NOT closed.** The audit's A2
question is already answered **YES** — all three reworked hooks install and run
on a first mid-session enable, no relaunch. Recorded on the checklist and the
D01/D03/D04 entries. What was proven: **D03 clean**; **D04 passes** with an
expected self-healing limitation (a panel built BEFORE the flip cannot be
retro-bound — the wrap is on `SolarPanelBase:GameInit` — and a reload snaps it
to sun #2); **D01's hook is live** (a rocket that LANDS after the flip fills
immediately).

**Three things remain. State them to the user when they ask what is left:**

1. **Step 2 — toggle OFF, for all three modules.** Un-run. Flip each module
   back off mid-session and confirm the behavior reverts immediately to vanilla
   answers. Nothing about the OFF direction has been exercised this sitting.
2. **Step 3 — `SMRFixPack.ListFixes()` agreement + a log sweep.** Un-run.
   ListFixes must agree with the toggle at each step, and the session log must
   be clean per PT-22 rules.
3. **The D01 decision (user's call, blocks closure).** PT-55 step 1's literal
   wording — *"a parked, destination-less player rocket starts requesting
   launch fuel"* — **FAILED**: an already-parked rocket did not begin refuelling
   after the flip and **did not heal on a save/reload either**. Cause confirmed
   in source: the wrap is on `GetFuelResourceRequest`, only consulted when
   `CargoTransporterNew:UpdateCargoResourceRequests` runs, and nothing
   re-triggers that for a parked rocket (landing is what does — the tester's own
   "on-land interaction" guess). **Either** accept it as a documented limitation
   (PT-55 then closes on items 1-2 alone) **or** build the `on_activate` demand
   refresh on parked destination-less player rockets, then re-verify D01's
   step 1. Full write-up on the D01 entry.

**Playtest state:** **PT-11 PASS → F01 `tested`** and **PT-29 PASS → F41
`tested`** (both 2026-07-29, archived). PT-53 (D07 CohortHousing) is 3-of-5
PASS — triggers A and E left, though **A may be effectively covered**: on
2026-07-30 the user ran the exact employed/unemployed A/B (Forever Young ON →
employed seniors did NOT move; reload without it → unemployed seniors re-homed
over 1-2 sols). The employed half is only valid if the module read `active`
at the time — **confirm that before crediting it**. PT-52 (D06 + F77) has three
healthy passive sittings; Trigger B is un-run and the **B2 stress A/B re-run on
the v2 harness is the natural centrepiece of the next live sitting**. PT-54
gates the wave-6 disaster fixes. PT-56 gates D09 (and its PASS un-gates the
D10 build).

**A live sitting is in progress on a SAVE-B-derived no-disasters save** with
Forever Young researched, a dedicated nursery-only child dome, and homelessness
/ unemployment deliberately saturated. That save is the fixture for D12's
origin evidence — do not assume a healthy colony.

**Open decisions on the user (nothing blocks on you):** F79 D-item or not
(trains never serve service trips — confirmed vanilla gap); audit Phase 4
go/no-go (core-helper extraction + module merges — deferred, see
AUDIT_FINDINGS); D06 iteration beyond knobs (design changes are user calls;
the stat dials are BUILT — D09, 2026-07-29 late, range widened to 1x/2x/3x/5x
by user call after the live no-clamp probe; PT-56 owed).
D08 (extender overhaul) is speced in `DRONE_OVERHAUL_OPTIONS.md`, nothing built.
**D10 (workshops: text repairs + capacity dial) is DECIDED and speced
(2026-07-30, BUGS.md entry) — build it after PT-56 PASSes; not a decision.**
Deferred decision recorded there: seniors-in-workshops (D07 interaction).
**D12 (no-homeless dome policy) is DECIDED and speced (2026-07-30, BUGS.md
entry) — build owed, not a decision.** Origin: found in play — a nursery-only
child dome deadlocked itself. Vanilla's emigration tie rule
(`Colonist.lua:2675-2681`) never moves homeless colonists when every candidate
ties, so graduates evicted from nurseries strand in place; that pushes the dome
over `IsOverpopulated`, and D07's own `consider()` skips overpopulated
communities — so no new children arrive. D12 drains the homeless and the loop
unwinds without touching D07. **Its own module**, `Opt_ResidencyControl` as
donor pattern ONLY — the hard constraint is that the new flag must NOT route
through `CanAcceptNewColonists` (D03's gate), or it blocks the cohort delivery
it exists to protect. Never expel to the surface: best-effort via the shipped
emigration machinery, and if no destination qualifies the colonist stays.
**Sequencing:** D10 and D12 both touch colonist assignment — land them
separately with their own A/B, never entangled.
Release-time owner tasks from the audit (plan 2.5): preview image (PDX ≤2 MB
/ Steam ≤1 MB), screenshots, Paradox portal console-publishing rules.

**Session-start sequence (~2 min):**
1. `git log --oneline -5` + `git pull` (see above).
2. Verify the pack loaded clean: on-screen status loop (below) — all 69
   default fixes `active` (incl. DroneStatDials, active-at-base), plus
   whichever opt-in toggles the user runs (account-persistent — currently
   ALL SIX ON, see the account-state note above).
3. Fresh `SMRFixPack.DroneReport` baseline if D06 is on (counters reset
   every launch; the PT-52 passive watch continues every sitting).
4. Optional (only if a lander/cargo read is planned): re-arm
   `SMRTest.Log.AutoCargo(true)` + `SMRTest.Log.CargoReady(true)`
   (runtime-only, reset every launch).

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is **LIVE PLAYTEST STANDBY**: the user is (or is about to be) at the
keyboard in the retail game with both mods loaded, and you assist in real time.
Your jobs, in the order they usually come up:

1. **Set tests up** — for whichever PT item the user picks, walk them through
   setup using the checklist's own steps and the verified command table
   (`PLAYTEST_CHECKLIST.md`); hand them exact console lines to paste. The
   opt-in modules are enabled in **Options → Mod Options → Community Fix
   Pack** (main menu or pause menu; PT-51 verified the surface — but see the
   first-enable caveat above for the three affected modules).
2. **Process results as they arrive** — reporting protocol at the bottom of
   `PLAYTEST_CHECKLIST.md`: PASS → status flips in BOTH BUGS.md places (index
   row + heading tag; for D-entries flip the "built" wording to tested), the
   completed section moves to `PLAYTEST_ARCHIVE.md` (partially-passed tests
   stay in the checklist with their passed triggers recorded); FAIL →
   diagnose live if possible (console wrappers, timestamped logging — the
   F12 pattern), file the finding on the BUGS entry with the full forensic
   trail.
3. **Diagnose surprises** — anything odd the user reports mid-play gets the
   live-instrumentation treatment. New defects get a new F-number, entry, and
   severity call. Mechanical repairs may land same day WITH a re-verified A/B
   (F12 + ListFixes precedents); redesigns go to the user.
4. **Commit as you go** — every processed result or finding is a commit
   (identity below), pushed. Docs never lag play.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\ENGINE_FACTS.md` — the whole file (the engine behaviors that will
   otherwise mislead you; moved out of STATUS.md 2026-07-29). Then
   `docs\STATUS.md` — now a compact current-state doc: header (counts, open
   decisions, next gates) + reference sections. Session legs all live in
   `docs\archive\SESSION_LOG.md` (newest first) — read the newest ones (the
   2026-07-29 audit-remediation and disaster/QA legs) down through the D06
   build leg.
2. `docs\PLAYTEST_CHECKLIST.md` — **restructured 2026-07-29**: toolbox/
   reference first (ground rules, verified command table, stress harness),
   then §1 standing watches (log hygiene, meteor watchdog, PT-52 passive),
   §2 owed halves (PT-53 A/E, PT-52 Trigger B + B2 re-run, PT-46 tail),
   §3 wave-6 PT-54, §4 fixture sittings, §5 cross-cutting (PT-20/21).
   The PT-52 section still carries the CAN/CANNOT lists — judge the module
   only on the CAN list.
3. `docs\BUGS.md` — the entries the sitting touches (D06 + F77 for the PT-52
   watch; D07 for PT-53; F78/F81 for PT-54; **F76 before ANY depot-picker
   interaction**; F48 before PT-37). For any drone anomaly, the DroneControl
   bullet in "Not yet swept" carries the full assignment-machinery trace and
   the R1-R7 paste-ready console forensics.
4. `docs\FIX_POLICY.md` — binding rules for any code you write.
5. Only when relevant: `docs\AUDIT_FINDINGS.md` (audit findings + the plan —
   Phases 1-3 implemented 2026-07-29, Phase 4 awaiting the user's
   go-decision); `docs\DRONE_OVERHAUL_OPTIONS.md` (only if D06 needs design
   iteration, not just knob tuning — the shipped core is the veto variant of
   option H + option A; upgrade paths H-v2/B/C and the DECISION section are
   there).

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code** (`tasklist`) — edits to loaded Lua mid-session do
nothing until relaunch, and a baseline-metadata accident during play would be
silent.

## The board (user picks; suggested order)

- **~~Post-D09 A/B RunAll set~~ DONE IN FULL 2026-07-30** — 77 probes (new
  DroneStatDials probe drives the real Apply path via `Mods[pack].options`):
  baseline **1/61/15/0** · default config **62/0/15/0 at 69/75** ·
  all-six-toggles + dials **67/0/10/0 at 75/75**, logs clean in every leg.
  OptionsMenu now asserts the two dial wirings too (TestKit `ed01ef7`).
  Nothing owed to the harness; the next A/B is owed only when new code lands.
- **~~AUDIT_FIX_PROMPT~~ DONE 2026-07-29** — AUDIT_FINDINGS Phases 1-3 all
  landed (veto bypasses, opt-module first-enable repair, error-status
  checkbox, F78/F81 decoupling, upload blockers + ignore_files + ModItemCode,
  MOD_DESCRIPTION/README corrections, ENGINE_FACTS + STATUS/SESSION_LOG
  restructure). What it left for humans: **PT-55** (opt-module live-toggle
  re-verify, checklist §2 — **PARTIALLY RUN 2026-07-30, see the PT-55 section
  near the top for the exact three items still owed**) and the **Phase 4
  go-decision** (user).
- **PT-55 — FINISH IT (cheapest open item).** Toggle-OFF direction for all
  three modules, ListFixes agreement + log sweep, and the D01 decision. Full
  list in the dedicated section above. Nothing else on the board is closer to
  done.
- **PT-52 STRESS A/B — re-run with the v2 harness (the v1 run's metric was
  invalid).** Protocol is Trigger B2 in the checklist (§2): quicksave →
  `Targets` dry run (check the `pure_only=true` cohort size too) → D06 OFF →
  `Break{scope="overlap", n=25, seed=1}` → reload → D06 ON → same call →
  `Compare()` → repeat seeds 2-3. Read the **GATE-DECIDED first claims** line
  (closest-hub % over FindTask-decided claims only) and the lifecycle deltas
  (haul queue vs exec vs claim wait vs travel — this is what gates the
  Track B structural choice). Do NOT read total clearance time as a D06
  score. Reload-based protocols do NOT re-poison a save (tested, F81).
- **PT-54 — wave-6 disaster fixes live gate** (checklist §3): stranded-flag
  reconcile, live-warning-never-cleared, wedge self-heal, reschedule-after-
  heal, rains survive collisions. The live 194-sol save is the fixture.
- **PT-53 — D07 CohortHousing, TWO cheap triggers left** (checklist §2):
  **(A)** unemployed Senior re-homes in-dome, EMPLOYED Senior does NOT move
  (two-minute infopanel read); **(E)** manual assignment wins, toggle-off =
  instantly vanilla, save-ON/reload-OFF loads clean. Then it flips `tested`.
- **PT-52 Trigger B — controlled off/on CheatMalfunction A/B demo + F77
  extender-flap check** (checklist §2) — still un-run; cheap once hub A/B +
  extender geometry exists.
- **F82** — split-grid notification lingers ~a sol; machinery located,
  updater cadence still to trace (own entry). **F80** — trains skip valid
  waiting passengers; investigating, forensic tap on the entry.
- **F76 REPAIR — separate attended, game-free sitting** (vanilla P1,
  unfixed): fix belongs in/around `ResourceItems:UpdateLayout`
  (`ResourceItems.lua:45-71`); Init-time anchor conversion is a proven NO-OP;
  tier-2 fallback = bypass the picker. The F76 entry + section below are the
  whole brief.
- **PT-48** AcknowledgedWarnings (D02, checklist §4) — break two buildings so
  they won't self-heal, dismiss: acked stay quiet; a THIRD breakage warns
  promptly; repair + re-break re-warns; stamp survives reload.
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- **Playtest-method rule (earned 2026-07-29, applies to every PT):** two tests
  in a row proved unrunnable as written (PT-29's trigger needed a colonist that
  could not exist yet; PT-11 compressed a scheduler const without re-arming the
  repeat, so it would have false-PASSed regardless of the fix). **Treat an
  un-run PT's procedure as unverified until it has been executed once**, and
  for any "nothing should happen" test insist on a positive control and an
  objective counter. Details in the checklist's ground rules.
- Un-run fixture PTs (checklist §4-5): PT-10, PT-15, PT-18 (fixtures
  A/D/E), PT-25, PT-27/28/30 (**PT-29 and PT-11 PASSED 2026-07-29 → F41 and F01
  `tested`, both archived**; PT-27's Biorobots grant is
  `ThePositronicBrain`; `CheatResearchAll()` SKIPS undiscovered
  breakthroughs — grant directly via `UIColony:SetTechResearched("<Id>")`),
  PT-35, PT-42, PT-44, PT-46 tail (F49(d) cap, F49(a) palette), PT-47,
  PT-20/21/22 (cross-cutting, last — PT-20's save should post-date wave 6 so
  the cycle covers the new persisted state).
- **PT-56 — D09 stat dials** (checklist §2, ~5 min): baseline reads → 2x/+1
  → Apply → stacked reads → base → Apply → baseline again → stale-save
  reconcile. PASS flips D09 to tested **and un-gates the D10 build** (the
  workshops module reuses the same label-modifier dial machinery).
- **D10 — workshops module BUILD (assistant, game-free, after PT-56 PASS):**
  speced + user-approved 2026-07-30, full spec on the BUGS.md D10 entry —
  T1 text repairs (workshop descriptions + Unemployed rollover gain the
  Relaunched faction-approval fact; ≥10% dome unemployment costs -900..-3000
  approval per faction clause) + T2 capacity dial (base/+50%/+100%, colony
  label modifiers on the three template labels, max_workers AND
  consumption_amount PAIRED — the pairing keeps per-worker cost vanilla).
  Adds PT-57 (~7 min) at build time. Seniors-in-workshops deliberately
  deferred (D07 interaction — own decision).
- **DECISIONS owed (user):** F79 D-item or not; audit Phase 4 go/no-go; D08;
  seniors-in-workshops (D10 deferral); **D11 shuttle same-pair passenger
  batching — feasibility is on the BUGS entry but it is NOT approved: ask
  fresh before any build (user's explicit instruction 2026-07-30); multi-hop
  passenger routing is REJECTED, do not re-propose.**
- Passive: PT-01 meteor silence-watch (the watchdog self-reports); F18
  savegame-sweep line on affected saves.

## PT-52 briefing notes (D06 + F77 — read WITH the checklist's PT-52 section)

The checklist section is the procedure; these are the assistant-side facts:
- **Setup check (each sitting):** the toggle persists, but confirm
  `DroneOverhaul [active]` AND `ExtenderFlapChurn [active]` via the
  on-screen loop or `SMRFixPack.fixes.DroneOverhaul.status` (bare
  expression). F77 rides along default-on — vetoable via
  `SMRFixPack_Disabled["ExtenderFlapChurn"] = true` pre-load if a confound
  is suspected. **Counters are NOT persisted** (zero-persisted-state design)
  — they restart at 0 each game launch, so take the sitting's baseline
  DroneReport right after load. Reference: three sittings healthy, peak
  `vetoed=10 / veto_expired=1 / moonlighted=0`, nine hubs integrated,
  `unclaimed=0` throughout including right after a marsquake mass-damage
  event.
- **`SMRFixPack.DroneReport` prints ON-SCREEN (ConsolePrint) AND to the log
  (ModLog)** — unlike ListFixes, no FlushLogFile dance needed live; the log
  copy is the evidence trail.
- **Counter interpretation** (the module's ground truth): `vetoed` climbing +
  `veto_expired` staying low = near fleets are taking the yielded work
  (healthy). `veto_expired` ≈ `vetoed` = strike window too short or near
  fleets can't respond → knob-tune or investigate. `moonlighted` > 0 near
  saturated hubs (it only fires for a neighbour hub with ZERO idle drones —
  0 is CORRECT when every hub has idle drones). All three flat at 0 with the
  toggle on = the module never intervenes — either no overlap contention this
  session (fine) or something is wrong (check status + log).
- **Starvation is the one theoretical risk the design accepts a window for**
  (max ~4 far-fleet polls ≈ 10-15s before the veto expires). If a wrench
  icon ever visibly outlives vanilla expectations: DroneReport + the R1/R2
  reads on the building IMMEDIATELY, then toggle off and watch whether
  vanilla clears it. That capture is a same-day knob/logic decision.
- **Iteration knobs** (top of `Code/Opt_DroneOverhaul.lua`, relaunch to take
  effect): STRIKES_MAX/STRIKE_TTL (veto patience), MOONLIGHT_MAX_HEXES (help
  radius), HUB_MISS_TTL/COVER_CACHE_TTL (scan cadence). Record every change
  + observed effect on the D06 entry. Knob changes are mechanical (assistant
  may land them same-day, committed); DESIGN changes (H-v2 demand filter,
  registration-H, balancer C) are user decisions per the options doc.
- **Scope guards to lean on when diagnosing:** the claim gate cannot touch
  player orders (FindTask is only called by auto-Idle); rockets, rovers,
  construction, and all hauling are exempt by class/type; toggling off is
  instant-and-complete vanilla. If a hauling or construction anomaly shows
  up, it is NOT this module — investigate it as its own finding.
- R1-R7 forensics (DroneControl bullet) double as the module debug kit; R7
  (hub A + hub B + extender + `CheatMalfunction`) is the cleanest off/on
  demonstration of the claim gate.

## F76 — READ THIS BEFORE THE USER TOUCHES AN RC TRANSPORT **OR DOZER** (vanilla P1, unfixed)

The resource picker (`ResourceItems`) renders far from the cursor and cannot
be clicked on the user's 4K/80%-scale setup — and interacting with it can
**HARD-LOCK the UI (Alt-F4, session lost)**. Full forensics on the F76 entry.
**Surface (widened 2026-07-27 late): ANY vehicle whose click-load reaches a
storage-depot-class object** — RC Transport depot LOAD, multi-type UNLOAD,
route resource choice, and the RC Terraformer ("RC Dozer") clicking a
waste-rock storage heap (confirmed by play, on-click). During play sessions:
- **Avoid the picker paths entirely.** Loose ground/rubble piles are safe (no
  picker — direct pickup, this includes the dozer's auto-gathering), and
  route-mode depot loading works for single-resource depots
  (`RCTransport.lua:466-476`).
- **Verified command workaround** (works for transports AND the dozer):
  `rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`
  (select the vehicle, `rc = SelectedObj`; depot via `~` inspector or
  selection).
- **NO live UI-internals prototyping in a play session** — hard rule since
  the lock-up. The F76 REPAIR is a separate attended, game-free sitting (see
  the board).
- It WILL draw false reports against the pack — the MOD_DESCRIPTION explainer
  note covers it.

## Live-session console facts (hard-won — do not re-derive)

- **`SMRFixPack.ListFixes()` prints to the LOG, not the console overlay**
  (ModLog path; the function returns nothing, so the console shows nothing —
  that is correct behavior, not a failure. The nil-detail CRASH it used to
  have is repaired). Read it via `FlushLogFile()` + the newest log, or use
  the on-screen variant:
  `*r for _, id in ipairs(SMRFixPack.order) do local f = SMRFixPack.fixes[id] ConsolePrint(id .. " [" .. f.status .. "]") end`
- The log buffer only flushes at exit — `FlushLogFile()` forces it
  mid-session (always do this before reading the log).
- **Mars↔asteroid map switches used to KILL the console** — TestKit repair
  BUILT and VALIDATED 2026-07-28 (`OnMsg.CurrentMapChangeDone` re-asserts
  gate + shortcuts; console opened normally across repeated switches; the
  quicksave+reload workaround is retired). If only the ECHO is gone but
  typing works, the lighter recovery is `ShowConsoleLog(true)` blind
  (uiConsoleLog.lua:88).
- **Runtime console wrappers must target the LEAF class** (engine-facts
  flattening corollary): wrapping a base class at runtime does nothing for
  already-built subclasses — e.g. lander taps go on `UniversalLanderRocket`,
  not `UniversalRocketBase`. (The same fact is why the opt-module
  first-enable defect existed — fixed by audit 1.3's file-scope installs;
  human re-verify is PT-55.)
- **CORRECTED 2026-07-29 — the earlier claim here was backwards.** Bare console
  expressions echo on-screen only (NOT logged), **and so does `print(...)`**:
  `print = CreatePrint{""}` (`lib.lua:202`) and `CreatePrint` defaults its
  output to **`ConsolePrint`** (`lib.lua:149`), which the engine documents as
  on-screen only. `print` therefore does NOT reach the log — the old advice to
  "use `print` when output must be retrievable" would have silently lost it.
  **`ModLog(...)` is the only path proven to reach the log file on disk**
  (ModLog → ModPrint → DebugPrint, `Mod.lua:109-132`), which is why the pack's
  own logging goes through it. Read the log with `FlushLogFile()` first.
- **`not understood` = the console could not COMPILE the line** (`console.lua:24`
  — no rule in `ConsoleRules` produced a loadable chunk). Overwhelmingly the
  cause is a `--` comment inside a `*r` / `*g` snippet: those rules splice your
  code into `CreateRealTimeThread(function() %s end) return` **on one line**
  (`uiConsole.lua:360-361`), so the comment eats the closing `end) return`.
  **Never write a console snippet with a trailing comment or a `--> value`
  annotation** — hand the user paste-safe lines, one command per line, because
  the console input is a SINGLE line and a pasted block silently concatenates
  (proven 2026-07-29: `--> nil` + the next line arrived as `--> nilUIColony:…`).
- For a simple read prefer a **bare expression** over `*r ConsolePrint(...)`:
  rule `{ "(.*)", "ConsolePrint(print_format(%s))" }` (`uiConsole.lua:363`)
  wraps anything that compiles as an expression, so `GetRareTraitChance()`
  prints itself. Reserve `*r`/`*g` for multi-statement snippets.
- Infopanel cheat buttons need `Platform.cheats = true` AND ride the
  game-time sync queue (dead while paused; fire on unpause). Direct
  `SelectedObj:Cheat*()` bypasses both.
- Console opens via Enter / Alt-Shift-C / Ctrl-Alt-C (TestKit auto-opens it
  in-colony; there is NO main-menu console — Mod Options replaced that need).
- Speed techs sanctioned for setup: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`. Hive Mind is NOT a drone tech in Relaunched.
- Cheat use is logged per save and blocks that save's achievements — fixture
  saves only.

## Harness facts (for the queued pre-flight pair / any same-day repair)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; Mars.exe may take minutes to appear. **Never kill on a
  short timeout** (25 min no-kill guard; harness watchdog 15 min).
- Arm the TestKit autorun by adding `"Code/96_AutoRunFlag.lua"` to the TestKit
  metadata `code` list; remove it to disarm (commented out at rest).
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list —
  **keep the `default_options` block** (it is part of the mod def now).
  **Restore from a saved copy, NOT `git checkout`, while uncommitted metadata
  changes exist. NEVER `git commit -a` while that edit is in the working
  tree.**
- Opt-in leg mechanism (proven): temporary `Code/97_OptInLeg.lua` in the FIX
  PACK listed right after 00_Core, setting the `SMRFixPack_Optional` table
  (the OptionEnabled bridge ORs it with the saved Mod Options toggles).
  Delete it after the leg. **The bridge is one-way: it can only force a module
  ON, never off** (OptionEnabled ORs the table with the saved toggles), and the
  user's own Mod Options toggles are account-persistent and apply during legs.
  So ALWAYS read the leg's own `fix pack present: N/74 fixes active` line to
  learn which config you actually measured — and a true default-config leg
  (68/74) requires the user to turn the six toggles off by hand first. Proven
  2026-07-29: the "default" leg came up 74/74 because all six were on.
- **TestKit `Code/91_Stress.lua` (v2, lifecycle tracing)** — the drone stress
  harness. It registers NO probes; v2 installs permanent classdef-time wraps
  on `RequiresMaintenance` `StartDemandPhase`/`StartWorkPhase`/`Repair`, but
  they gate on an active stress run and pass straight through otherwise.
- **Expected numbers — FRESH (post-D09 set completed 2026-07-30, 77 probes,
  all three legs run):** baseline (`code` list emptied) **1 / 61 / 15 / 0**;
  default config, six toggles OFF **62 / 0 / 15 / 0 at 69/75**; all six
  toggles ON + dials **67 / 0 / 10 / 0 at 75/75**. The D09 dial probe PASSes
  in BOTH fixed legs (DroneStatDials registers active-at-base, independent of
  the toggles). The 10 SKIPs are 9 `[install]`
  retail-sandbox probes + TechDescriptionBuilding; a default leg's extra 5 are
  the opt-module probes reporting `inactive (opt-in)` — **five, not six,
  because D06 has no probe of its own** (the stress harness covers it).
  Baseline's 1 PASS = FactionFundingCheck canary; the OptionsMenu probe (D05)
  asserts all six toggle wirings PLUS the two D09 dial wirings and FAILs
  baseline by design. The D09 dial probe writes `Mods[pack].options` (NOT its
  own env's CurrentModOptions — per-mod-env, see ENGINE_FACTS) and restores
  the leg's values through the same path. The rains probe does NOT skip on
  the synthetic map — the harness builds a colony, so `HasGame()` is true.
- **Probe-authoring trap (cost wave 6 its coverage, 2026-07-29):** a probe
  whose `run` falls off the end returns nil, and `SMRTest.Run` turns nil into
  **SKIP with an empty message** (`00_TestCore.lua:243`) — it looks like a
  deliberate skip, not a missing verdict. Baseline legs never catch it (the
  `FixMissing` guard returns FAIL before the tail runs), so only a FIXED leg
  can. Every probe needs an explicit `return "PASS", …`; grep
  `Register(` vs `return "PASS"` counts per wave file to audit this.
- **TestKit stand-in probe corollary (D07 leg):** WithGlobals stubs CANNOT
  reach a game file that localizes the global at load time
  (`local IsValid = IsValid`, Colonist.lua:5) — a probe driving shipped code
  with plain-table stand-ins must assert on the MODULE's own action, never on
  vanilla bookkeeping around the stand-ins; a fake colonist through the
  shipped FindEmigrationDome tail needs a PickEmigrationCommunity stub.
- Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors +
  a few GameInit nil-call lines in BOTH legs; a `[mod] Error in mod … Test
  Kit` line at quit is a shutdown artifact. The MultipleSuns
  "not found → lifted" line pair during load is the known benign transient.
- Parse sweep: python + luaparser, `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` both ends; prefer the editor's file tools. Git
  commit messages via single-quoted here-strings or `git commit -F <file>`;
  **no embedded double quotes** (proven again 2026-07-27).

## Hard rules

`docs/ENGINE_FACTS.md` governs (the facts moved there from STATUS 2026-07-29):
sandbox on all platforms; `error()`/`assert()` report-and-continue;
self-checks read the DECLARING class; presets only after DataLoaded
(GlobalMaps exist EMPTY before it; DataChanged(false) re-fires right after;
DataLoaded can fire MORE THAN ONCE — a template can miss the first pass);
GameVars only inside patched functions; post-wrappers on command methods
never run; `IsValid()` is falsy for ALL pure-Lua objects; **the shipped build
IS Src** (full fpk extraction, 2250/2256 byte-identical, build 1.0.7.396349 —
keep apply-time self-checks anyway, they guard future patches); never modify
the game directory; only the playtest flips statuses to `tested`; mechanical
repairs land with a re-verified A/B, redesigns go to the user; **no live
UI-internals prototyping on the user's play sessions** (F76 lesson). Commit
with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (rewrite stale blocks —
no banner stacking), commit, push, summarize.
