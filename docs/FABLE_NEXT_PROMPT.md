# Fable continuation prompt — PLAYTEST STANDBY (rewritten 2026-07-27 late)

Paste everything below into a fresh Claude Code session (Fable). This is the ONE
live prompt. Build state: **68 registered modules, 64/68 active by default
(4 opt-in: ClassicRockets, AcknowledgedWarnings, ResidencyControl,
MultipleSuns), 16 fixes carry playtest status, latest clean legs 2026-07-27
(logs 20.38.21 / 20.39.59 / 20.41.49: baseline 1/56/14/0, fixed 57/0/14/0,
opt-in 60/0/11/0 at 67/68), everything pushed.** The 2026-07-27 build leg
deleted the F61 fix, folded F39 into D04, and shipped the three opt-in modules
D02/D03/D04 with probes and playtest items (**PT-48/49/50, checklist Group 8**).
**The build queue is EMPTY** — new work only comes from playtest FAILs, live
findings, or the F76 attended sitting.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is **LIVE PLAYTEST STANDBY**: the user is (or is about to be) at the
keyboard in the retail game with both mods loaded, and you assist in real time —
the 2026-07-26/27 marathon model. Your jobs, in the order they usually come up:

1. **Set tests up** — for whichever PT item the user picks, walk them through
   setup using the checklist's own steps and the verified command table
   (`PLAYTEST_CHECKLIST.md`); hand them exact console lines to paste. Group 8
   (the new opt-in modules) needs its flag set at the MAIN MENU console first:
   `SMRFixPack_Optional = { AcknowledgedWarnings = true, ResidencyControl = true, MultipleSuns = true }`
   then load/start; `SMRFixPack.ListFixes()` must show all three `applied`.
2. **Process results as they arrive** — reporting protocol at the bottom of
   `PLAYTEST_CHECKLIST.md`: PASS → status flips in BOTH BUGS.md places (index
   row + heading tag; for D-entries flip the "built" wording to tested), the
   completed section moves to `PLAYTEST_ARCHIVE.md`; FAIL → diagnose live if
   possible (console wrappers, timestamped logging — the F12 pattern), file the
   finding on the BUGS entry with the full forensic trail.
3. **Diagnose surprises** — anything odd the user reports mid-play gets the
   live-instrumentation treatment (F76 and the F12 second defect were both
   caught this way). New defects get a new F-number, entry, and severity call.
   Mechanical repairs may land same day WITH a re-verified A/B (F12 precedent);
   redesigns go to the user.
4. **Commit as you go** — every processed result or finding is a commit
   (identity below), pushed. Docs never lag play.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "Build leg" section AND the whole engine-facts list
   ("Key technical facts").
2. `docs\PLAYTEST_CHECKLIST.md` — ground rules, the verified command table, the
   open board, the reporting protocol. Group 8 = PT-48/49/50.
3. `docs\BUGS.md` — the entries the sitting touches (D02/D03/D04 for Group 8;
   F76 before ANY depot-picker interaction; F48 before PT-37).
4. `docs\FIX_POLICY.md` — binding rules for any code you write.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code** (`tasklist`) — edits to loaded Lua mid-session do
nothing until relaunch, and a baseline-metadata accident during play would be
silent.

## The board (user picks; suggested order)

- **Group 8 — the three new opt-in modules (one sitting, all flags on):**
  - **PT-48** AcknowledgedWarnings — dismiss sticks per-building, new breakage
    still warns, re-break re-warns, stamp survives reload.
  - **PT-49** ResidencyControl — **the pack's first added infopanel row: look
    at it critically** (position, icons, yellow-vs-red distinction from
    quarantine, rollover text). Then: arrivals + resettlement blocked, commute/
    services intact, manual relocation + tourists work, MicroG habitat row too.
  - **PT-50** MultipleSuns — menu allows sun #2, its panels produce at night
    (banked PT-26 baseline: −21% atmospheric → small 3.6 vs 4, large 9 vs 10),
    survives reload, limit returns with the module off.
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- Un-run: PT-09..11, PT-15..19 (fixtures B/D/E), PT-23, PT-25, PT-27..33,
  PT-35 (PT-27's Biorobots grant is `ThePositronicBrain`;
  `CheatResearchAll()` SKIPS undiscovered breakthroughs — grant directly via
  `UIColony:SetTechResearched("<Id>")`), PT-40/42/43/44, PT-47,
  PT-46 tail (F49(d) cap, F49(a) palette), PT-20/21/22 (cross-cutting, last).
- Passive: PT-01 meteor silence-watch (the watchdog self-reports — that log
  line is F02's root-cause evidence); F18 savegame-sweep line on affected
  saves.

## F76 — READ THIS BEFORE THE USER TOUCHES AN RC TRANSPORT (vanilla P1, unfixed)

The RC Transport depot resource picker renders far from the cursor and cannot
be clicked on the user's 4K/80%-scale setup — and interacting with the broken
picker can **HARD-LOCK the UI (Alt-F4, session lost)**. Full forensics on the
F76 entry. During play sessions:
- **Avoid the picker paths entirely**: depot LOAD with a picker, multi-type
  UNLOAD, route resource choice. Ground piles are safe (no picker), and
  route-mode depot loading works for single-resource depots
  (`RCTransport.lua:466-476`).
- **Verified command workaround** when the user needs a depot load anyway:
  `rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`
  (select the transport, `rc = SelectedObj`; depot via `~` inspector or
  selection).
- **NO live UI-internals prototyping in a play session** — hard rule since the
  lock-up. The F76 REPAIR is a separate attended, game-free sitting (throwaway
  session, user present, a freeze costs nothing): fix belongs in/around
  `ResourceItems:UpdateLayout` (`ResourceItems.lua:45-71`) — Init-time anchor
  conversion is a proven NO-OP (scale applied post-Init); tier-2 fallback =
  bypass the picker (single-resource → direct TransferResources; multi-type
  unload → unload every accepted type); survey the `ItemMenuBase` siblings
  while in there. If the user asks for this sitting, that spec + the F76 entry
  are the whole brief.
- If it draws a false report against the pack mid-test, that is EXPECTED — the
  MOD_DESCRIPTION draft note (~line 90) already plans the explainer.

## Live-session console facts (hard-won — do not re-derive)

- Infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused; fire on unpause). Direct
  `SelectedObj:Cheat*()` bypasses both.
- `SMRTest.Cls` wipes the console overlay. Log buffer only flushes at exit —
  `FlushLogFile()` forces it mid-session (do this before reading the log).
- Console opens via Enter / Alt-Shift-C / Ctrl-Alt-C (TestKit auto-opens it).
- Speed techs sanctioned for setup: `AdvancedDroneDrive` (breakthrough, drones
  +40%), `LowGDrive` (+20% drones + rovers), `MartianAerodynamics` (shuttles
  +33%). Hive Mind is NOT a drone tech in Relaunched.
- Live wrappers for diagnosis: wrap in the console with the same chained
  pattern the pack uses; timestamp with `GameTime()`/`RealTime()` pairs (the
  PT-38 measurement pattern). Cheat use is logged per save and blocks that
  save's achievements — fixture saves only.

## Harness facts (for any same-day repair's re-verified A/B)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; Mars.exe may take minutes to appear. **Never kill on a
  short timeout** (25 min no-kill guard; harness watchdog 15 min).
- Arm the TestKit autorun by adding `"Code/96_AutoRunFlag.lua"` to the TestKit
  metadata `code` list; remove it to disarm (commented out at rest).
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list.
  **Restore from a saved copy, NOT `git checkout`, while uncommitted metadata
  changes exist. NEVER `git commit -a` while that edit is in the working tree.**
- Opt-in leg mechanism (proven): temporary `Code/97_OptInLeg.lua` in the FIX
  PACK listed right after 00_Core, setting the `SMRFixPack_Optional` table
  (TestKit-vs-fix-pack load order is not guaranteed — the flag file must live
  in the fix pack). Delete it after the leg.
- **Expected numbers (current, 71 probes):** baseline 1 PASS / 56 FAIL /
  14 SKIP / 0 ERROR; fixed 57/0/14/0 (64/68 active); opt-in (three modules)
  60/0/11/0 (67/68). Baseline's 1 PASS = FactionFundingCheck canary;
  default-leg 14 SKIP = 10 [install] + 4 opt-in.
- Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors + a
  few GameInit nil-call lines in BOTH legs; a `[mod] Error in mod … Test Kit`
  line at quit is a shutdown artifact.
- Parse sweep: python + luaparser, `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` both ends; prefer the editor's file tools. Git
  commit messages via single-quoted here-strings; no embedded double quotes.

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING class;
presets only after DataLoaded (GlobalMaps exist EMPTY before it;
DataChanged(false) re-fires right after); GameVars only inside patched
functions; post-wrappers on command methods never run; `IsValid()` is falsy for
ALL pure-Lua objects; never modify the game directory; only the playtest flips
statuses to `tested`; mechanical repairs land with a re-verified A/B, redesigns
go to the user; **no live UI-internals prototyping on the user's play
sessions** (F76 lesson — it hard-locked a session). Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt, commit, push, summarize.
