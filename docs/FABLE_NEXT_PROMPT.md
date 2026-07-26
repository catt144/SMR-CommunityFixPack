# Fable continuation prompt — playtest reports / playtest QA (written 2026-07-26)

Paste everything below into a fresh Claude Code session (Fable). This is the ONE
live prompt: the old OPUS_BUILD / FABLE_QA / FABLE_PLAYTEST prompts are retired
(git history has them). The build state is: 67 registered modules, 66/67 active,
four clean A/B pairs on 2026-07-26, everything pushed. The session before this
one closed F18's open half (savegame sweep), landed the F44/F45 seed-crash
repair, the F66 reclaim trigger, the F47 composition repairs, the F02 stall
watchdog, and recorded the D01 export-half design decision. What remains is
playtest-driven.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is most likely **processing the user's playtest reports** (or answering
playtest questions; queued build work is listed at the end).

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — "Follow-up session — Fable, 2026-07-26" AND the whole
   engine-facts list.
2. `docs\PLAYTEST_CHECKLIST.md` — the un-run tests, their save fixtures, and the
   "Reporting protocol" section at the end. Completed tests + their result
   evidence live in `docs\PLAYTEST_ARCHIVE.md` (completed sections move there,
   protocol step 8).
3. `docs\BUGS.md` — the tracker you will be updating.
4. `docs\FIX_POLICY.md` — binding rules for any code you write.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit` — confirm the user is not mid-playtest before
any edit the game could load (mod code loads at LAUNCH only; doc edits are
always safe; A/B legs need the game to be free).

## Processing playtest reports

- The playtest is the ONLY thing that flips a fix from `fixed` (probe-verified)
  to `tested` (ships in the release text). Partial reports are fine — process
  what was reported, leave the rest untouched. Record results in the checklist
  (preserve the user's own words; add dated evidence notes), flip BUGS statuses,
  and keep STATUS's session record current.
- FAILs: diagnose from the logs in `%AppData%\Surviving Mars Relaunched\logs`
  before touching code (the F02 hunt in STATUS is the worked example). Mechanical
  repairs land with a re-verified A/B pair; redesigns go to the user.
- **Three checklist items are decision gates that trigger real work:**
  * **PT-36** → F10's final `wontfix` (delete the commented metadata line).
  * **PT-37** → F48: PASS = build the corrected fixup behind a one-shot flag;
    FAIL = `wontfix`.
  * **PT-38** → D02: confirms the 2-real-minute cadence, then build
    `Opt_AcknowledgedWarnings` (+probe) in a build leg.

## Playtest state as of 2026-07-26 (see checklist for the user's own notes)

- **Done:** PT-02 PASS, PT-04 PASS, **PT-03 PASS in full** (F44 halves + the F45
  retry — load sweep reported both counts, broken element salvaged cleanly),
  **PT-45 PASS** (refund = stamped sections × 100, scales with length; partial
  stockpiles observed), **PT-46 PASS** (F49(b) resolved as no-defect — the
  engine stores a train on a removed element correctly). Status flips landed:
  **F03/F44/F45/F50/F47 are `tested`** (commits 4310fb2/73406ff; index rows
  synced 2026-07-26 late). PT-01 cadence + towers verified on real play
  (+49h/+40h post-load, >42h impossible under the broken code); the ~42h
  tower-extended STORM warning banner verified live (bc4e828); necropsy
  answered: the wedged thread was **ALIVE-stuck** (scheduler/persist side).
  Only a longer silence-watch remains — the watchdog self-reports
  (`WATCHDOG — Meteors thread silent … last phase 'X', thread ALIVE|DEAD`) and
  THAT log line is the root-cause evidence if it ever fires.
- **PT-41 PASS (recorded 2026-07-26 late): F66 is `tested`.** Shared hex stayed
  stable ("could not determine which building owned it", no connector churn in
  the 11.48.31 log); demolishing one building left the connector "its own node
  but stayed connected to the remaining building with no weird visuals" — the
  reclaim repair; plain-tile control clean.
- **Everything else is un-run:** PT-05..PT-19 (fixture saves B/C/D/E per the
  checklist's fixture table), PT-23..35 (wave-3), PT-36/37/38 (gates, attended),
  PT-39/40/42/43/44 (wave-4), PT-47 (wave-5), PT-46's untested tail (F49(d)
  train cap follows length, F49(a) instant-track palette), PT-20/21/22
  (uninstall / soak / log hygiene). The F18 savegame sweep announces itself on load of an affected save
  (`corrected the already-researched tech's stored discount from 10% to 20%`) —
  worth capturing when it happens.

## Queued build work (each unblocks on its trigger)

- **F02 root cause:** if the watchdog line ever appears, pull last-phase +
  alive/dead from the log and design the real repair (an alive-stuck Sleep
  points at how save/persist re-schedules persisted game-time thread wake-ups;
  the MeteorStorm thread — NOT restarted by our fix — wedged identically).
- **D01 export half** (user decision recorded 2026-07-26: match the ORIGINAL
  game; the legacy loader `RocketBase.lua:1729-1736` is the spec — standing
  PreciousMetals demand to `max_export_storage`, any-drone flags, per-rocket
  `allow_export` toggle). Three research items on the D01 entry, incl. whether
  the original auto-offloaded RC transports (decides if F56 rides along). Own
  probe + playtest item; same `ClassicRockets` flag; extend MOD_DESCRIPTION's
  side-by-side when it ships.
- **F48 / D02** per their gates above.
- MarsDebug attended `[install]` pass for the wave-4/5 fixes (SetupOnly mode;
  procedure + modal-dialog warning in STATUS's wave-3 QA section).
- Release checklist (STATUS): statuses to `tested` as reports come in, fpk
  target verification, MOD_DESCRIPTION final pass (only `tested` fixes ship in
  the list).

## Harness facts (hard-won — do not re-derive)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; watch for Mars.exe to appear (up to 4 min) then exit.
  **Never kill on a short timeout** — no-kill watcher (25 min guard); harness
  watchdog 15 min.
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list;
  restore with `git checkout -- metadata.lua`. **NEVER `git commit -a` while
  that edit is in the working tree.**
- Expected healthy numbers (2026-07-26): baseline **1 PASS / 58 FAIL / 11 SKIP /
  0 ERROR**; full pack **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR**, 66/67 active
  (ClassicRockets opt-in inactive). The 11 SKIPs: 9 `[install]` probes,
  ClassicRockets, TechDescriptionBuilding (F25 rides its playtest item).
  Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors + a few
  GameInit `attempt to call a nil value` lines in BOTH legs; a `[mod] Error in
  mod … Test Kit` line at quit is a shutdown artifact.
- Parse sweep: python + luaparser,
  `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` on both ends; prefer the editor's file tools.
  Git commit messages via single-quoted here-strings; no embedded double quotes
  (PS 5.1 native-arg quoting eats them).

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING class;
presets only after DataLoaded (GlobalMaps exist EMPTY before it;
DataChanged(false) re-fires right after); GameVars only inside patched
functions; post-wrappers on command methods never run; `IsValid()` is falsy for
ALL pure-Lua objects; never modify the game directory; only the playtest flips
statuses to `tested`; mechanical repairs land with a re-verified A/B, redesigns
go to the user. Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt, commit, push, summarize.
