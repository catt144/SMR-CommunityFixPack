# Fable continuation prompt (rewritten 2026-07-27, after the build leg)

Paste everything below into a fresh Claude Code session (Fable). This is the ONE
live prompt. Build state: **68 registered modules, 64/68 active by default
(4 opt-in: ClassicRockets, AcknowledgedWarnings, ResidencyControl,
MultipleSuns), 16 fixes carry playtest status, latest clean legs 2026-07-27
(logs 20.38.21 / 20.39.59 / 20.41.49: baseline 1/56/14/0, fixed 57/0/14/0,
opt-in 60/0/11/0 at 67/68), everything pushed.** The 2026-07-27 build leg
deleted the F61 fix, folded F39 into D04, and shipped the three opt-in modules
D02/D03/D04 with probes (PASS in the opt-in leg) and playtest items
(**PT-48/49/50, checklist Group 8**). The build queue is EMPTY — no module work
is pending except what a playtest FAIL creates.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack". This
session has NO queued build work; it is one of these, in priority order:

1. **If the user opens with playtest results** — process them per the reporting
   protocol (`PLAYTEST_CHECKLIST.md`, bottom; completed sections move to
   `PLAYTEST_ARCHIVE.md`; statuses flip in BOTH BUGS.md places: index row +
   heading tag). The new Group 8 items (PT-48/49/50) cover the opt-in modules —
   a PASS there flips the D-entry to `tested`-equivalent wording on its heading
   and index row.
2. **If the user is present and wants the F76 sitting** — the attended,
   game-free repair leg for the vanilla P1 depot-picker bug (below). Do NOT
   start this unattended or on a play session.
3. **Otherwise** — smaller queued tail: nothing is currently staged. Offer the
   user the open decision gates (PT-37) and the un-run playtest board.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "Build leg" section AND the whole engine-facts list
   ("Key technical facts").
2. `docs\BUGS.md` — F76 (if doing the sitting) or whatever entries the playtest
   report touches.
3. `docs\FIX_POLICY.md` — binding rules for any code you write.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code or launching A/B legs** (`tasklist`).

## F76 — THE ATTENDED SITTING (user present, throwaway session, freezes cost nothing)

Vanilla P1 with a hard-lock vector — full forensics on the F76 entry. Facts
already established: the dialog's own `self.scale` is applied AFTER `Init` (an
Init-time anchor conversion is a NO-OP — the fix belongs in or around
`ResourceItems:UpdateLayout`, `ResourceItems.lua:45-71`); the anchor captures
the true mouse (`terminal:GetMousePos()` was (1731,665) on the 4K desktop);
teardown can leave a destroyed window in the modal/anim chain → every
MouseEvent errors (`XWindow.lua:1154`) → UI hard-lock, Alt-F4. User env:
fullscreen 3840×2160, UI Scale ~80-85%. Tier-2 fallback design if the anchor
resists: bypass the picker (single-resource depot load → direct
`TransferResources`; multi-type unload → unload every accepted type). Verified
player workaround meanwhile:
`rc:SetCommand("TransferResources", depot, "load", "<Res>", 30000, true)`.
Survey the `ItemMenuBase` siblings that anchor the same way while in there.
MOD_DESCRIPTION already carries the F76 false-report draft note (~line 90) —
resolve it when the fix ships (it becomes the fix bullet) or when release text
is finalized (it becomes the "known vanilla issue" explainer).

## Playtest board (open; process reports whenever they arrive)

- **NEW — Group 8 (the three opt-in modules, one sitting, all flags on):**
  PT-48 AcknowledgedWarnings, PT-49 ResidencyControl (**first added infopanel
  row in the pack — needs critical eyes on the UI**), PT-50 MultipleSuns
  (night-production signature vs the banked PT-26 single-sun baseline:
  −21% atmospheric → small 3.6 vs 4, large 9 vs 10).
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- Un-run: PT-09..11, PT-15..19 (fixtures B/D/E), PT-23, PT-25, PT-27..33,
  PT-35 (PT-27's Biorobots grant is `ThePositronicBrain` — command table
  corrected: `CheatResearchAll()` SKIPS undiscovered breakthroughs; grant
  directly via `UIColony:SetTechResearched("<Id>")`), PT-40/42/43/44, PT-47,
  PT-46 tail (F49(d) cap, F49(a) palette), PT-20/21/22 (cross-cutting).
- Passive: PT-01 meteor silence-watch (the watchdog self-reports — that log
  line is F02's root-cause evidence); F18 savegame-sweep line on affected
  saves.
- Speed techs are sanctioned for test setup (recorded in the command table):
  `AdvancedDroneDrive` (breakthrough, drones +40%), `LowGDrive` (+20% drones +
  rovers), `MartianAerodynamics` (shuttles +33%). Hive Mind is NOT a drone
  tech in Relaunched (repurposed to Arcology).

## Harness facts (hard-won — do not re-derive)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; watch for Mars.exe to appear (up to 4 min) then exit.
  **Never kill on a short timeout** — no-kill watcher (25 min guard); harness
  watchdog 15 min.
- Arm the TestKit autorun by adding `"Code/96_AutoRunFlag.lua"` to the TestKit
  metadata `code` list; remove the line to disarm (it is commented out at rest).
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list.
  **Restore from a saved copy, NOT `git checkout`, while uncommitted metadata
  changes exist. NEVER `git commit -a` while that edit is in the working tree.**
- Opt-in leg mechanism (proven this leg): temporary `Code/97_OptInLeg.lua` in
  the FIX PACK listed right after 00_Core, setting
  `SMRFixPack_Optional = { AcknowledgedWarnings = true, ResidencyControl = true,
  MultipleSuns = true }` (TestKit load order vs the fix pack is not guaranteed,
  so the flag file must live in the fix pack itself). Delete it after the leg.
- **Expected numbers (current):** baseline 1 PASS / 56 FAIL / 14 SKIP / 0 ERROR;
  fixed 57/0/14/0 (64/68 active); opt-in (three modules) 60/0/11/0 (67/68).
  Baseline's 1 PASS = FactionFundingCheck canary; default-leg 14 SKIP =
  10 [install] + 4 opt-in.
- Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors + a
  few GameInit nil-call lines in BOTH legs; a `[mod] Error in mod … Test Kit`
  line at quit is a shutdown artifact.
- Retail console gotchas (checklist command table): infopanel cheat buttons
  need `Platform.cheats = true` AND ride the game-time sync queue (dead while
  paused); direct `SelectedObj:Cheat*()` bypasses both. `SMRTest.Cls` wipes
  the overlay. Log buffer only flushes at exit — `FlushLogFile()` forces it.
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
