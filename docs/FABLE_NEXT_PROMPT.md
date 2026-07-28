# Fable continuation prompt — PLAYTEST STANDBY (rewritten 2026-07-28, post-D06 build)

Paste everything below into a fresh Claude Code session (Fable). This is the
ONE live prompt (the drone investigation prompt is retired — its verdict and
build landed). **Start with `git log --oneline -5` + `git pull`** in case
another session ran since this prompt was written.

Build state: **70 registered modules, 65/70 active by default (5 opt-in via
Options → Mod Options — D05, `tested`), 72 probes, everything pushed.**
NEW since the last sitting (2026-07-28, all committed):
- **D06 `Opt_DroneOverhaul` core v1 BUILT** (user-greenlit): closest-fleet-
  first claim gate + repair moonlighting + `SMRFixPack.DroneReport()`
  telemetry. Opt-in toggle "Drone dispatch overhaul (experimental)".
  **PT-52 is this sitting's centerpiece** — full procedure in
  `PLAYTEST_CHECKLIST.md`, briefing notes on the board below.
- **F77 `Fix_ExtenderFlapChurn` BUILT** (default-on): extender working-flaps
  debounce+coalesce the whole-hub rebuild instead of Idle-kicking the fleet
  twice per blip.
- Full design context if anything needs iterating:
  `docs/DRONE_OVERHAUL_OPTIONS.md` (options A-H, what shipped and why, what
  the future iterations are — H-v2 demand filter, B full moonlighting,
  C migration balancer). The investigation trace + R1-R7 console forensics
  live on the BUGS.md DroneControl bullet ("Not yet swept" section).
Prior state stands: D05 tested (PT-51), D04 tested (PT-50), PT-49 core
passing, F76 dozer surface filed. **The build queue is EMPTY** — new work
comes only from playtest FAILs, live findings, the F76 attended sitting, or
D06 iteration decisions (user decision, knobs first).

**PRE-FLIGHT (game-free, ~5 min, do BEFORE the user starts playing):** the
QUEUED A/B pair re-verify is now MORE important — since the last verified
pair, two mechanical repairs (ListFixes nil-detail, D03 row reposition) AND
two new code files (D06 core, F77) landed. **Expected PROBE numbers
unchanged** (no new probes yet — stated testing debt): baseline 1/57/14/0,
fixed 58/0/14/0; module counts shift to **65/70 active** in the fixed leg
(ExtenderFlapChurn active, DroneOverhaul inactive-until-toggled; the OLD
expectations said 64/68). Watch the fixed-leg log specifically for
`ExtenderFlapChurn: applied` and `DroneOverhaul: inactive (opt-in module...)`
— an `error` status on either is a same-day repair item. Harness facts
below. If the user is already at the keyboard wanting to play, ask whether
to run it first or at session end.

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
1. `docs\STATUS.md` — the "D06 build leg" section (newest) AND the whole
   engine-facts list ("Key technical facts").
2. `docs\PLAYTEST_CHECKLIST.md` — ground rules, the verified command table,
   **the PT-52 procedure** (what the D06 module CAN and CANNOT do — judge it
   only on the CAN list), the reporting protocol.
3. `docs\BUGS.md` — the entries the sitting touches (**D06 + F77 for PT-52**;
   D02 for PT-48; D03 for PT-49's tail; F65 for PT-40; **F76 before ANY
   depot-picker interaction**; F48 before PT-37). For any drone anomaly, the
   DroneControl bullet in "Not yet swept" carries the full assignment-
   machinery trace and the R1-R7 paste-ready console forensics.
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

- **PT-52 — D06 Drone dispatch overhaul + F77, FIRST SITTING — the
  centerpiece.** Full procedure (CAN/CANNOT lists, Triggers A/B/C, result
  lines) is the PT-52 section of `PLAYTEST_CHECKLIST.md`; briefing notes
  below the board. It runs as a WATCH-AND-JUDGE layer across the WHOLE
  session while other PT items are played — enable the toggle at session
  start, run `SMRFixPack.DroneReport` as baseline, keep half an eye on
  drones all session. Not a 15-minute test; the user expects multiple
  iterations across sittings.
- **PT-48** AcknowledgedWarnings (D02) — break two buildings so they won't
  self-heal, dismiss the warning: acked buildings stay quiet; a THIRD breakage
  warns promptly and lists only itself; repair + re-break re-warns; stamp
  survives reload; other warning types behave vanilla.
- **PT-49 tail** (D03; core behavior + row position already verified —
  progress note in the section): arrivals routed away from the closed dome,
  MANUAL relocation into it still works, tourists still check into its
  hotels, quarantine toggles independently, the MicroG habitat row appears on
  asteroid habitats, uninstall shape (save with a closed dome → module off →
  reload → accepts again, no errors).
- **PT-40** train tunnel power (F65) — **use a NORMAL station for the
  short-track half**: the fix triggers only on 2-element tracks (station
  snugged directly to the tunnel entrance); a large station's footprint tends
  to force a longer track, which is the already-working case and proves
  nothing. Station size is otherwise irrelevant (the fix is class-agnostic —
  it bridges whenever the two ends read as different live grids).
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- Un-run: PT-09..11, PT-15..19 (fixtures B/D/E), PT-23, PT-25, PT-27..33,
  PT-35 (PT-27's Biorobots grant is `ThePositronicBrain`;
  `CheatResearchAll()` SKIPS undiscovered breakthroughs — grant directly via
  `UIColony:SetTechResearched("<Id>")`), PT-42/43/44, PT-47,
  PT-46 tail (F49(d) cap, F49(a) palette), PT-20/21/22 (cross-cutting, last).
- Passive: PT-01 meteor silence-watch (the watchdog self-reports); F18
  savegame-sweep line on affected saves.
## PT-52 briefing notes (D06 + F77 — read WITH the checklist's PT-52 section)

The checklist section is the procedure; these are the assistant-side facts:
- **Setup check:** after the toggle, `SMRFixPack.ListFixes` (log) or the
  on-screen loop must show `DroneOverhaul [active]` AND
  `ExtenderFlapChurn [active]` (F77 rides along as a default-on fix —
  vetoable via `SMRFixPack_Disabled["ExtenderFlapChurn"] = true` pre-load if
  a confound is suspected).
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
- **The on-screen console echo can silently die mid-session** (observed
  2026-07-28 after Mars↔asteroid map hops): commands still execute, prints
  still reach the log, only the display overlay (`dlgConsoleLog`) is gone.
  Recovery: type `ShowConsoleLog(true)` blind (uiConsoleLog.lua:88) — no
  restart needed.
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

## Harness facts (for the pre-flight A/B and any same-day repair)

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
