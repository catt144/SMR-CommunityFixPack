# Project Status — read this first in a new session

Updated: 2026-07-25. This is the handoff snapshot; BUGS.md is the canonical
defect tracker, FIX_POLICY.md the patching rules, WORKFLOW.md the dev/test/release
process, RESEARCH.md the lead catalog (incl. ChatGPT dossier cross-check),
MOD_DESCRIPTION.md the player-facing mod-page draft (update its fix list in the
same commit that implements a fix; only `tested` fixes ship in the final text),
TESTING.md the force-the-bug test plan (script probes + cheat scenarios + the
SMRTest companion-mod spec — build the test kit early in the build-out leg;
its RunAll() before/after pair is the acceptance gate for `tested` status).

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

## Discovery: COMPLETE

- 73 tracked findings (~85 distinct defects) verified against the CURRENT
  (post-1.0.7) shipped source, each with file:line evidence + fix sketch in BUGS.md.
- 1 design-change verdict (D01 rocket auto-refuel/rare-metals — plan opt-in module).
- 2 candidates needing runtime checks (C01 BreakthroughOrder, C02 asteroid cave-ins).
- 3 critical UNTRACED leads (RESEARCH.md): 90%-breathable-atmosphere freeze,
  Last War mystery import lock at 54%, game-stops-saving. Plus smaller new leads
  from the ChatGPT dossier cross-check (top of RESEARCH.md).

## Implementation: 10 of ~30 planned fixes DONE (none in-game tested yet)

Implemented (see metadata.lua code list, one file per fix, all committed):
F01 cave-ins/NoDisasters, F02 meteor frequency, F03* upgrade-modifier leak,
F04 night shift, F05 milestone crash, F07+F15* wisp power/rewards, F08 tourist
applicants, F10 faction funding, F64 trains-to-void.
(* = runtime leak stopped / partial; save-cleanup sweep still TODO.)

Next up (P1 queue, in order): F67-F69 asteroid lander trio (makes asteroids
playable — fix sketches in BUGS.md are detailed), F73 shelter reflex, F45 damaged
track salvage, F44 whole-track deletion, F30 lake entombment, F37 ghost farm O2,
F50 rocket drone churn, F51 shuttle cache, F52 vacuum walks, F53 arrival deaths,
F55 open-dome drone access, F58 residence reservations, F61 shopping passage gate,
F06 crystal hang, F09 tourist satisfaction, F11 train wedge, F12 low-storage warning.
Then: `Code/90_SaveSanitizer.lua` module collecting the one-shot LoadGame sweeps
(F03, F35, F37, F45, F48 + ChoGGi-pattern cleanups) — adopted from dossier strategy.

## Key technical facts (hard-won, do not re-derive)

- Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` (verified from working
  code paths) but NOT boolean relational compares — don't report/fix nil-iteration
  as crashes.
- Patch points that work: `PeriodicRepeatInfo[name]` slots (THREAD/SLEEP/FUNC/COND
  = 1..4, CommonLua\Core\lib.lua:1538+), `GlobalGameTimeThreadFuncs[name]` +
  `RestartGlobalGameTimeThread(name)` on LoadGame (Lua\Config\_fixup.lua),
  class-method replacement, chained wrappers, `OnMsg.*` additive handlers,
  preset/data patches at ClassesPostprocess.
- Mod registry: every fix goes through `SMRFixPack.Register(id, {title, apply})`
  (Code/00_Core.lua); apply self-checks the target and returns a reason string to
  deactivate gracefully; `SMRFixPack_Disabled` = user veto; `SMRFixPack.ListFixes()`
  console status.
- All line numbers reference `ModTools\Src`; the game executes `Packs\Lua.fpk`
  (slightly newer date) — runtime self-checks in apply() are the guard.
- Sample mod format in `<game>\ModTools\Samples\Mods`; docs in `ModTools\Docs\index.md.html`.

## Waiting on the user

1. Launch the game once, enable "Community Fix Pack" in the Mod Manager, confirm
   `SMRFixPack.ListFixes()` shows fixes active → validates packaging + F01-F64 wave.
2. Author name/handle for metadata.lua (placeholder TBD_SET_BEFORE_RELEASE).
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need the planned sanitizer module (baked state:
F03 leaked modifiers, F37 ghost O2, F58 stale reservations, F35 turbine buff,
F48 connectors; also detect-and-force-finish hung mysteries). ~15% is
irreversible history (dead colonists, lost expeditions; F64 voided trains have
no recorded count — heuristic compensation option at best, and document the
vanilla train re-purchase at stations, Station.lua:573-611). Save rescue is the
headline differentiator vs official patches ("new games only") — lead with it.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion);
credit ChoGGi (Fix Bugs) + LukeH (Martian Express) as prior art; keep per-fix
disable instructions in the description.
