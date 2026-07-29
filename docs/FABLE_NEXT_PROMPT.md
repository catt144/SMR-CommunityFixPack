# Fable continuation prompt — PLAYTEST STANDBY (updated 2026-07-28 night, post-TEN-FLIP sitting)

**NEWEST FIRST (2026-07-28 evening sitting — read the "TEN-FLIP playtest
sitting" STATUS section before anything):** ten `tested` flips in one
sitting (F68, F73, F72, F65, F70, F67, F69, F19, F20, F21) — **the
ASTEROID SECTION and PT-43 are COMPLETE and archived**; the map-switch
console repair + BOTH leaf-class loggers validated live; F78 hypothesis 1
REFUTED live (on-demand repro plan on the entry: bracket taps +
`CheatMeteors("single")` at empty ground); **NEW F79 confirmed** (trains
never carry service seekers — fix would be feature-completion),
**NEW F80 investigating** (trains skip valid waiting passengers), **NEW D07
speced** (`Opt_CohortHousing` — cohort members in normal housing move to
free Retirement Home/Nursery slots anywhere, in-dome first, untouched when
none exist; no dome UI). **DECISION UPDATE 2026-07-28 late: D07 config
CONFIRMED by the user (in-dome-first + cross-dome, Seniors+Children one
toggle — the spec as written) but build HELD — do not build until an
explicit go. Still pending: whether F79 gets a D-item fix.** Zero pack
code changed —
no pre-flight owed. PT-52 sitting 2 healthy; **Trigger B STILL un-run.**

Paste everything below into a fresh Claude Code session (Fable). This is the
ONE live prompt. **Start with `git log --oneline -5` + `git pull`** in case
another session ran since this prompt was written.

Build state: **70 registered modules, 65/70 active by default (5 opt-in via
Options → Mod Options — D05, `tested`), 72 probes, everything pushed.
A/B pair is FRESH (2026-07-28 late, post-F68-repair): baseline 1/57/14/0 ·
all-five-toggles 62/0/10/0 (70/70 applied) — NO pre-flight queued.**
NEW since the last rewrite (2026-07-28 PT-52 sitting + same-evening repair
leg, all committed):
- **PT-49 COMPLETE → D03 `tested` (archived).** Adversarial arrivals proof,
  tourists exemption, quarantine independence, MicroG row (KEPT on asteroid
  habitats by user decision), uninstall shape, and a child-in-closed-dome
  sighting forensically cleared as in-dome birth.
- **PT-32 COMPLETE → F71 `tested` (archived).** Live two-resource priority
  inversion via console taps: valuables allocated first, bulk the remainder,
  nothing dropped, below-threshold resources correctly excluded.
- **PT-17: ratchet half PASS; capacity-edge leg caught a REAL pack defect —
  and its repair LANDED the same evening (A/B re-verified).** The v1 F68 fix
  double-counted aboard cargo (`GetTotalCargoAvailable` already counts a
  landed rocket's hold — new engine fact) and over-exported 60 units below
  the player's GET-WHEN-ABOVE threshold. Repaired by deleting the
  aboard-into-ground addition; the explicit floor carries the fix. **The
  attended capacity-edge re-run PASSed 2026-07-28 (next sitting): request
  tracked aboard + surplus, ground settled AT the threshold (146 with miners
  running vs threshold 140) → F68 `tested`, PT-17 ARCHIVED.** Full trail on
  the F68 entry.
- **PT-52 first sitting: HEALTHY.** D06 live-enable bridge verified; two
  DroneReport readings (`vetoed 4→10, veto_expired 0→1, moonlighted 0`,
  `unclaimed=0` on all six hubs all sitting). The watch continues every
  sitting; F77 flap check (Trigger B) still un-run.
- **TestKit AutoCargo logger repaired** (leaf-class wrap + reads
  `cargo[res].requested`; the old one was structurally blind to landers).
- **NEW F78 (P1, investigating): the live save has had ZERO disasters in 194
  sols and no weather at all** — the PT-01 meteor watchdog caught the
  mechanism live (Meteors thread hangs INSIDE shipped `MeteorsDisaster`,
  restarted repeatedly); sibling disaster threads may be wedging invisibly.
  Board item below; evidence + plan on the F78 entry.
- **Map-switch console-death repair VALIDATED 2026-07-28 (next sitting):**
  the console now survives Mars↔asteroid switches (TestKit
  `OnMsg.CurrentMapChangeDone` re-assert). Details in the console facts
  below.
- New hard-won facts recorded: the **class-flattening runtime corollary**
  (runtime instrumentation must target the LEAF class; STATUS Key facts),
  the **console-death-on-map-switch bug + recovery**, and the
  first-landing-is-manual lander behavior (reserved sites auto-land after).
Prior state stands: D05 tested (PT-51), D04 tested (PT-50), F76 dozer
surface filed. **The build queue is EMPTY again — the map-switch
console-death repair is BUILT (TestKit, validation pending: see console
facts below; first thing next sitting, switch to the asteroid and press
Enter).** New work comes only from playtest FAILs, live findings, the F76
attended sitting, or D06 iteration decisions (user decision, knobs first).

**NO PRE-FLIGHT NEEDED** — the A/B pair above is fresher than every code
change. **Session-start sequence (in order, ~2 min):**
1. Game relaunched fresh (the F68 repair + both TestKit repairs only exist
   on disk until then).
2. ~~Console-repair validation~~ **DONE 2026-07-28: VALIDATED** (console
   survives map switches; workaround retired).
3. Re-arm `SMRTest.Log.AutoCargo(true)` AND `SMRTest.Log.CargoReady(true)`
   (runtime-only; both leaf-class now — no console taps needed).
4. Fresh `SMRFixPack.DroneReport` baseline (D06 counters reset every launch).
**THE ASTEROID SECTION IS COMPLETE (2026-07-28 next sitting): PT-17, PT-19,
PT-33, PT-40, PT-31 AND PT-16 all PASSed and archived** — F68, F73, F72,
F65, F70, F67 and F69 all `tested` (seven flips in one sitting). The
remaining P1 there is the **F78 disaster-silence investigation** (board
below; hypothesis 1 refuted live, on-demand repro plan ready).

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is **LIVE PLAYTEST STANDBY**: the user is (or is about to be) at the
keyboard in the retail game with both mods loaded, and you assist in real time.
Your jobs, in the order they usually come up:

1. **Set tests up** — for whichever PT item the user picks, walk them through
   setup using the checklist's own steps and the verified command table
   (`PLAYTEST_CHECKLIST.md`); hand them exact console lines to paste. The
   opt-in modules are enabled in **Options → Mod Options → Community Fix
   Pack** (main menu or pause menu; toggles apply live both directions —
   PT-51 verified the whole surface; the user's toggles are ON and persist).
2. **Process results as they arrive** — reporting protocol at the bottom of
   `PLAYTEST_CHECKLIST.md`: PASS → status flips in BOTH BUGS.md places (index
   row + heading tag; for D-entries flip the "built" wording to tested), the
   completed section moves to `PLAYTEST_ARCHIVE.md`; FAIL → diagnose live if
   possible (console wrappers, timestamped logging — the F12 pattern), file
   the finding on the BUGS entry with the full forensic trail.
3. **Diagnose surprises** — anything odd the user reports mid-play gets the
   live-instrumentation treatment. New defects get a new F-number, entry, and
   severity call. Mechanical repairs may land same day WITH a re-verified A/B
   (F12 + ListFixes precedents); redesigns go to the user.
4. **Commit as you go** — every processed result or finding is a commit
   (identity below), pushed. Docs never lag play.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the **"TEN-FLIP playtest sitting"** section (newest)
   + the "F68 over-draw repair leg" and "D06 build leg" sections AND the
   whole engine-facts list ("Key technical facts").
2. `docs\PLAYTEST_CHECKLIST.md` — ground rules, the verified command table,
   **the PT-52 procedure** (what the D06 module CAN and CANNOT do — judge it
   only on the CAN list) with its two progress notes, the reporting
   protocol. (PT-17 is complete and archived 2026-07-28.)
3. `docs\BUGS.md` — the entries the sitting touches (D06 + F77 for the
   PT-52 watch;
   D02 for PT-48; **F76 before ANY depot-picker
   interaction**; F48 before PT-37). For any drone anomaly, the DroneControl
   bullet in "Not yet swept" carries the full assignment-machinery trace and
   the R1-R7 paste-ready console forensics.
4. `docs\FIX_POLICY.md` — binding rules for any code you write.
5. Only if D06 needs design iteration (not just knob tuning):
   `docs\DRONE_OVERHAUL_OPTIONS.md` — the shipped core is the veto variant of
   option H + option A; the upgrade paths (H-v2, B, C) are speced there.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code** (`tasklist`) — edits to loaded Lua mid-session do
nothing until relaunch, and a baseline-metadata accident during play would be
silent.

## The board (user picks; suggested order)

- **PT-52 — D06 Drone dispatch overhaul + F77, CONTINUING watch (sitting 1
  was healthy).** Full procedure is the PT-52 section of
  `PLAYTEST_CHECKLIST.md` (two progress notes recorded); briefing notes
  below the board. The user's toggle is ON and account-persistent — verify
  `DroneOverhaul [active]` at session start, take a fresh
  `SMRFixPack.DroneReport` baseline (counters are NOT persisted — they
  restart at 0 every game launch), keep half an eye on drones all session.
  **Trigger B (controlled off/on CheatMalfunction A/B demo + the F77
  extender-flap check) is still un-run** — the natural next PT-52 step.
- **PT-48** AcknowledgedWarnings (D02) — break two buildings so they won't
  self-heal, dismiss the warning: acked buildings stay quiet; a THIRD breakage
  warns promptly and lists only itself; repair + re-break re-warns; stamp
  survives reload; other warning types behave vanilla.
- **Asteroid closeout: COMPLETE.** PT-16 PASS 2026-07-28 → F67 + F69
  `tested` (full-sol asteroid hold logged by the repaired CargoReady
  logger; manual-landing fuel ration kept and flown home; CheckAutoDepart
  side-rule engine fact + RoughTouchDown stranding hazard recorded on the
  entries). **Earlier same sitting: PT-17
  capacity-edge re-run PASS → F68 `tested` (ground settled AT the threshold;
  repaired AutoCargo logger validated live); PT-19 PASS → F73 `tested`
  (residence held through both gap shapes — habitat off AND supply cut;
  vanilla status-reads-residence observation on the entry); PT-33 PASS →
  F72 `tested` (all three cases; refusal presents as an empty picker via
  the documented vanilla gate quirk — entry observation (a)); PT-31 PASS →
  F70 `tested` (round trip held, prefill negative intact).**
- **F78 — P1 INVESTIGATION, next step is the LIVE REPRO (5 min):**
  hypothesis 1 (descriptor-validate loop) REFUTED live 2026-07-28
  (`kept: 0`); on VeryLow the strike routine is statically seconds-bounded,
  so the 183h alive-but-stuck stall contradicts static analysis. Next
  session: arm the bracket taps from the F78 entry (MeteorsDisaster
  ENTER/EXIT + SpawnMeteor), aim at empty ground, `CheatMeteors("single")`
  — ENTER-without-EXIT reproduces the wedge on demand and the last print
  brackets the stall line.
- **DECISIONS:** D07 `Opt_CohortHousing` config CONFIRMED 2026-07-28 late
  (in-dome-first + cross-dome, Seniors+Children one toggle) but build
  HELD — no code until an explicit user go. Still owed: whether F79
  (trains never serve service trips — confirmed vanilla gap) gets a
  feature-completion D-item.
- **PT-40 DONE 2026-07-28 → F65 `tested` (archived):** full procedure PASS —
  merge in both geometries (snug + couple-tracks), clean salvage split,
  long-track control unchanged, reload persistence, log clean.
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- Un-run: PT-09..11, PT-15, PT-18 (fixtures B/D/E), PT-25, PT-27..30, PT-35 (PT-27's Biorobots
  grant is `ThePositronicBrain`; `CheatResearchAll()` SKIPS undiscovered
  breakthroughs — grant directly via `UIColony:SetTechResearched("<Id>")`),
  PT-42/44, PT-47,
  PT-46 tail (F49(d) cap, F49(a) palette), PT-20/21/22 (cross-cutting, last).
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
  DroneReport right after load. Sitting-1 reference: healthy at
  `vetoed=10 / veto_expired=1 / moonlighted=0` over a full evening.
- **`SMRFixPack.DroneReport` prints ON-SCREEN (ConsolePrint) AND to the log
  (ModLog)** — unlike ListFixes, no FlushLogFile dance needed live; the log
  copy is the evidence trail.
- **Counter interpretation** (the module's ground truth): `vetoed` climbing +
  `veto_expired` staying low = near fleets are taking the yielded work
  (healthy). `veto_expired` ≈ `vetoed` = strike window too short or near
  fleets can't respond → knob-tune or investigate. `moonlighted` > 0 near
  saturated hubs. All three flat at 0 with the toggle on = the module never
  intervenes — either the colony has no overlap contention this session
  (fine) or something is wrong (check ListFixes status + log).
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
  the lock-up. The F76 REPAIR is a separate attended, game-free sitting: fix
  belongs in/around `ResourceItems:UpdateLayout` (`ResourceItems.lua:45-71`)
  — Init-time anchor conversion is a proven NO-OP (scale applied post-Init);
  tier-2 fallback = bypass the picker; survey the `ItemMenuBase` siblings
  while in there. If the user asks for this sitting, that spec + the F76
  entry are the whole brief.
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
- **Mars↔asteroid map switches KILL the console** (isolated 2026-07-28 late:
  switch to the asteroid → console won't open on ANY binding, and stays dead
  after switching back; the earlier "echo died after map hops" was the same
  bug's milder face). Root: the Enter/Alt-Shift-C/Ctrl-Alt-C shortcuts only
  EXIST while the `ShowConsole` gate holds (uiConsole.lua:429-431 +
  CommonShortcuts.generated.lua:174-186); the TestKit enables the gate and
  rebuilds shortcuts once at load (00_TestCore.lua:288-306), and the asteroid
  switch tears that state down — with every binding gone, the re-enable
  command cannot be typed (chicken-and-egg). **Workaround: quicksave +
  reload ON the map you need** — the reload re-runs the TestKit colony-up
  hook and restores the console there; it dies again on the next switch, so
  batch console work per visit. **TestKit repair BUILT same evening
  (00_TestCore `OnMsg.CurrentMapChangeDone` — the switch machinery's own
  completion signal, map.lua:372/:404 — re-asserts gate + shortcuts after a
  1s settle; no auto-open on switches; the pre-existing
  InGameInterfaceCreated re-assert demonstrably did NOT cover this).
  VALIDATED 2026-07-28 next sitting: console opened normally after repeated
  Mars↔asteroid switches across a full live session — the workaround is
  retired.** If only the ECHO is gone
  but typing works, the lighter recovery is `ShowConsoleLog(true)` blind
  (uiConsoleLog.lua:88).
- **Runtime console wrappers must target the LEAF class** (STATUS engine
  facts, flattening corollary 2026-07-28): wrapping a base class at runtime
  does nothing for already-built subclasses — e.g. lander taps go on
  `UniversalLanderRocket`, not `UniversalRocketBase`.
- Bare console expressions echo on-screen only (NOT logged); `print(...)`
  goes to the log — use `print` when output must be retrievable.
- Infopanel cheat buttons need `Platform.cheats = true` AND ride the
  game-time sync queue (dead while paused; fire on unpause). Direct
  `SelectedObj:Cheat*()` bypasses both.
- Console opens via Enter / Alt-Shift-C / Ctrl-Alt-C (TestKit auto-opens it
  in-colony; there is NO main-menu console — Mod Options replaced that need).
- Speed techs sanctioned for setup: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`. Hive Mind is NOT a drone tech in Relaunched.
- Cheat use is logged per save and blocks that save's achievements — fixture
  saves only.

## Harness facts (for any A/B pair / same-day repair — none queued; last pair 2026-07-28 late)

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
  Delete it after the leg. NOTE: the user's own Mod Options toggles are
  account-persistent and will ALSO be on during legs — for a true default-
  config leg numbers, either ask the user to toggle them off first or accept
  the four opt-ins active (then expect 62/0/10/0-style shifts and document).
  Simplest: run legs with the toggles as-is and compare against the matching
  expectation.
- **Expected numbers (current, 72 probes — none for D06/F77 yet, opt-in
  toggles OFF):** baseline 1 PASS / 57 FAIL / 14 SKIP / 0 ERROR; fixed
  58/0/14/0 (**65/70 active** — ExtenderFlapChurn joins the default-on set,
  DroneOverhaul reads `inactive (opt-in...)`); opt-in (three modules)
  61/0/11/0 (68/70); all five toggles on = 62/0/10/0 (70/70). Baseline's 1
  PASS = FactionFundingCheck canary; the OptionsMenu probe (D05) asserts in
  every leg and FAILs baseline by design. Pre-D06 records said /68 — the
  denominator moved, the probe numbers did not.
- Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors +
  a few GameInit nil-call lines in BOTH legs; a `[mod] Error in mod … Test
  Kit` line at quit is a shutdown artifact. The MultipleSuns
  "not found → lifted" line pair during load is the known benign transient.
- Parse sweep: python + luaparser, `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` both ends; prefer the editor's file tools. Git
  commit messages via single-quoted here-strings; **no embedded double
  quotes** (a quote in the message breaks the here-string — proven again
  2026-07-27).

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING
class; presets only after DataLoaded (GlobalMaps exist EMPTY before it;
DataChanged(false) re-fires right after; DataLoaded can fire MORE THAN ONCE —
a template can miss the first pass); GameVars only inside patched functions;
post-wrappers on command methods never run; `IsValid()` is falsy for ALL
pure-Lua objects; never modify the game directory; only the playtest flips
statuses to `tested`; mechanical repairs land with a re-verified A/B,
redesigns go to the user; **no live UI-internals prototyping on the user's
play sessions** (F76 lesson). Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt, commit, push, summarize.
