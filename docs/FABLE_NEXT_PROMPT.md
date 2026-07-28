# Fable continuation prompt — THE BUILD LEG (rewritten 2026-07-27 late)

Paste everything below into a fresh Claude Code session (Fable). This is the ONE
live prompt. Build state: **67 registered modules, 66/67 active (ClassicRockets
opt-in), 16 fixes carry playtest status, latest clean A/B pair 2026-07-27
(logs 11.45.34 / 11.47.09: baseline 1/58/11/0, fixed 59/0/11/0), everything
pushed.** The 2026-07-27 sitting closed PT-06/14/24/26/39 (F08, F36, F74 →
`tested`; F61 → `wontfix`, superseded; F39 → latent, absorbed into D04), filed
three new opt-in designs (D03, D04, joining D02), and found the new vanilla P1
**F76** (depot resource picker off-cursor, unclickable, can HARD-LOCK the UI).

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is **the queued BUILD LEG** (user-approved 2026-07-27). If the user
instead opens with playtest results, process those first per the reporting
protocol (`PLAYTEST_CHECKLIST.md`, bottom; completed sections move to
`PLAYTEST_ARCHIVE.md`; statuses flip in BOTH BUGS.md places: index row +
heading tag).

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "Playtest marathon" section AND the whole
   engine-facts list ("Key technical facts").
2. `docs\BUGS.md` — the D02, D03, D04, F61, F39 and F76 entries (the full
   specs for this leg live there).
3. `docs\FIX_POLICY.md` — binding rules for any code you write.
4. `docs\PLAYTEST_CHECKLIST.md` — you will ADD playtest items for the new
   modules.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code or launching A/B legs** (`tasklist`); the game was
confirmed closed at wrap.

## The build queue (in order; all specs already written)

1. **F61 retirement mechanics (decision DONE):** delete
   `Code/Fix_HomeDomeMigrationGate.lua` + its `metadata.lua` code line; DELETE
   the TestKit `HomeDomeMigrationGate` probe (it tests removed behavior — not
   an F10-style canary). Doc side is already recorded.
2. **D02 `Opt_AcknowledgedWarnings`** — per-object acknowledgment of
   `NotWorkingBuildings`; spec + corrected cadence facts (120,000 GAME-ms =
   4 game h; suppression per notification id) on the D02 entry. Opt-in via
   `SMRFixPack_Optional` (ClassicRockets precedent), own probe, own PT item.
3. **D03 `Opt_ResidencyControl`** — new per-dome "closed to new residents"
   policy. Spec on the D03 entry incl. the move-in-path survey list (resettle
   via `Community:CanAcceptNewColonists`; arrivals need their own patch point —
   `is_welcoming_community` is file-local in `_GameUtils.lua:342-344`; manual
   relocation deliberately stays allowed; tourists/births untouched). UI row by
   post-wrapping `sectionDome:Init` (+ `sectionMicroGHabitat:Init`) — the
   section classes build rows imperatively, verified. Persisted absent-tolerant
   flag on the Dome object. Probe + PT item.
4. **D04 `Opt_MultipleSuns`** — lift `BuildingTemplates.ArtificialSun.build_once`
   (preset-patch timing: templates exist only after DataLoaded; the build menu
   re-reads `CanBuildOnlyOnce()` live — verified in-session) AND absorb
   `Fix_SecondArtificialSun.lua` unchanged; DELETE the standalone fix file.
   Rework its probe to the ClassicRockets SKIP-unless-opted pattern. PT item
   (single-sun night baseline for comparison is in the PT-26 archive section:
   −21% atmospheric, small 3.6 vs 4, large 9 vs 10). Update F39's heading/row
   to point at the shipped module.
5. **Parse sweep** (python luaparser, `utf-8-sig`) over both mods, then the
   **A/B pair** — plus ONE opt-in leg with all three new modules enabled so
   their probes PASS (ClassicRockets opt-in precedent). **Expected numbers
   CHANGE this leg — derive and RECORD the new baseline/fixed/SKIP counts**
   (F61 probe deleted; F39 probe moves to opt-in SKIP; three new opt probes
   SKIP by default). Old healthy numbers for reference: baseline 1/58/11/0,
   fixed 59/0/11/0, 66/67 active.
6. **Same-commit doc duties:** MOD_DESCRIPTION module sections for D02/D03/D04
   (resolve the F39/D04 draft note at ~line 65 and the sweep-list phrase near
   ~line 290; feature framing, not bug-fix framing), BUGS statuses/headings for
   the shipped modules, new PT items in the checklist, STATUS session record.

## F76 — SEPARATE ATTENDED SITTING (do NOT fold into the unattended leg)

Vanilla P1 with a hard-lock vector — full forensics on the F76 entry. The
repair facts already established: the dialog's own `self.scale` is applied
AFTER `Init` (an Init-time anchor conversion is a NO-OP — the fix belongs in or
around `ResourceItems:UpdateLayout`, `ResourceItems.lua:45-71`); the anchor
captures the true mouse (`terminal:GetMousePos()` was (1731,665) on the 4K
desktop); teardown can leave a destroyed window in the modal/anim chain →
every MouseEvent errors (`XWindow.lua:1154`) → UI hard-lock, Alt-F4. User env:
fullscreen 3840×2160, UI Scale ~80-85%. Tier-2 fallback design if the anchor
resists: bypass the picker (single-resource depot load → direct
`TransferResources`; multi-type unload → unload every accepted type).
Verified player workaround meanwhile:
`rc:SetCommand("TransferResources", depot, "load", "<Res>", 30000, true)`.
**Prototype only in a throwaway session (a freeze must cost nothing), with the
user present.** MOD_DESCRIPTION false-report explainer draft note is in place —
the user flagged this as a false-report magnet for the pack.

## Playtest board (open; process reports whenever they arrive)

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
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list;
  restore with `git checkout -- metadata.lua`. **NEVER `git commit -a` while
  that edit is in the working tree.**
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
