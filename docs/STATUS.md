# Project Status — read this first in a new session

Updated: 2026-07-25 (build-out session 2). This is the handoff snapshot; BUGS.md is
the canonical defect tracker, FIX_POLICY.md the patching rules, WORKFLOW.md the
dev/test/release process, RESEARCH.md the lead catalog (incl. ChatGPT dossier
cross-check), MOD_DESCRIPTION.md the player-facing mod-page draft (update its fix
list in the same commit that implements a fix; only `tested` fixes ship in the
final text), TESTING.md the force-the-bug test plan, CHEATS_INVENTORY.md the
shipped cheat/debug surface the tests drive.

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

Companion **Test Kit** mod (never shipped): `C:\Dev\SMR-BugFixPack-TestKit` (git).
`SMRTest.RunAll()` runs one probe per fix and prints PASS/FAIL/SKIP; run it with
the fix pack disabled (expect FAILs) and enabled (expect PASSes). It also enables
the Lua console at load and carries observability loggers and state reports.

## Discovery: COMPLETE

- 73 tracked findings (~85 distinct defects) verified against the CURRENT
  (post-1.0.7) shipped source, each with file:line evidence + fix sketch in BUGS.md.
- 1 design-change verdict (D01 rocket auto-refuel/rare-metals — plan opt-in module).
- 2 candidates needing runtime checks (C01 BreakthroughOrder, C02 asteroid cave-ins).
- 3 critical UNTRACED leads (RESEARCH.md): 90%-breathable-atmosphere freeze,
  Last War mystery import lock at 54%, game-stops-saving. Plus smaller new leads
  from the ChatGPT dossier cross-check (top of RESEARCH.md).

## Implementation: 30 fixes DONE (none in-game tested yet)

Wave 1 (earlier session): F01 cave-ins/NoDisasters, F02 meteor frequency,
F03* upgrade-modifier leak, F04 night shift, F05 milestone crash, F07+F15* wisp
power/rewards, F08 tourist applicants, F10 faction funding, F64 trains-to-void.

Wave 2 (this session, in queue order): F67 lander empty launch, F68 lander cargo
ratchet, F69 lander return fuel, F73 shelter reflex, F45 broken-track salvage,
F44 track salvage wipe, F30 lake entombment, F37 ghost farm oxygen, F50 rocket
drone churn, F51 shuttle transport cache, F52* vacuum walks, F53 arrival deaths,
F55* drone unreachable-forever, F58* stale reservations, F61 home-dome migration
gate, F06 crystal mystery hang, F09 tourist satisfaction, F11 train platform
wedge, F12 low-storage warning, F13 Command Center numbers, F14 Domes Overview
highlight.
(* = partial; the remaining half is recorded on the BUGS.md entry.)

Six fixes carry a one-shot `OnMsg.LoadGame` / `OnMsg.NewDay` repair pass for state
already baked into savegames: F02 (thread restart), F45 (stamp repair sites),
F37 (remove phantom farm oxygen), F58 (release stale reservations), F06 (restart
the crystal repeater), plus F55's expiry which self-heals. The consolidated
`Code/90_SaveSanitizer.lua` module is still a later phase — the remaining sweeps
it was to collect are F03 (leaked modifiers), F35 (turbine buff) and F48
(connectors).

## QA session snapshot (Fable, 2026-07-25) — partial, session cut short

- BUGS.md index was stale (16 wave-2 rows said `todo` despite tagged headings) —
  synced in commit 0ef4e7c. README/MOD_DESCRIPTION verified complete. Follow-up:
  wave-1 detail headings (F04/05/07/08/10/15/64) lack the `[fixed]` tag.
- Nothing was marked `blocked` in the build session. F55's "open-air entrance half
  not actionable" verdict was re-verified and is CORRECT (CalcOpenAirSkin only
  empties skin[2] configurable attaches; Dome_Entrance is entity-spot auto-attach
  data, Dome.lua:404 — not patchable from Lua). F55 drone half diffs clean.
- Spot-audit of 6 fixes (F61, F12, F44, F53, F68, F73) — full reports in the
  session transcript; summary:
  * **F53 CRITICAL — rework before release.** The `not IsInWalkingDist` gate in
    Fix_ArrivalDeaths.lua is always true for cross-map elevator destinations
    (IsInWalkingDistDome returns false when maps differ, Dome.lua:248-251), so
    every legitimate elevator arrival triggers the re-choose; the re-choose
    discards ChooseDome's elevator return and never clears stale
    self.emigration_elevator → TransportByFoot rides the stale elevator, fails
    the map-slot check (Colonist.lua:2731) → SetCommand("Abandoned"). Repair:
    skip the gate when ValidateBuilding(self.emigration_elevator) routes to
    dome; on re-choice take BOTH returns and assign emigration_elevator.
  * **F12 MODERATE — rework.** Post-wrapper leaves shipped dead branch removing
    the notification hourly, wrapper re-adds → destroy/recreate churn + FX replay
    every game hour while active; dismiss/suppression semantics differ. Docs
    prescribe full replacement — do that instead.
  * **F68 MODERATE — verify in-game.** The requested-floor (belt-and-braces
    block) doesn't debit hold capacity: with multiple exports, an alphabetically
    earlier resource's request can exceed remaining capacity → status stuck
    "loading", automode rocket sits on pad (departure gate needs "ready").
    Consider capping the floor against remaining capacity.
  * **F61 CLEAN**, **F44 CLEAN** (in-game check: curve-ended remainder track
    visuals; F45-comparator fold-in disclosed), **F73 CLEAN** (note:
    IsSuitable is AutoResolveMethods "and"-combined with Residence.IsSuitable —
    correct today, document it; partial-application isn't reported in the log).
  * Recurring minor: header/BUGS line-number drift (off-by-ones); apply()
    self-checks don't pre-check every runtime symbol.
- AccountStorage research (for the RunAll pair): enabled mods live in
  AccountStorage.LoadMods (plain array of metadata.lua `id` strings), persisted
  in `%AppData%\Surviving Mars Relaunched\<SteamID64>\account.dat` — an
  in-memory HPK (magic BPUL) containing `account.lua`, AES-encrypted+HMAC with
  key SHA256(GetAppId()..config.ProjectKey), compressed. BUT the loader is
  best-effort: a plaintext `return {...}` account.lua inside the container still
  loads (lib.lua:2187-2216). Edit only with the game closed; ids for missing/
  too-old mods are auto-stripped at menu (Mod.lua:2033-2059). Escape hatch:
  `AccountStorage.LoadAllMods = true` loads every discovered mod, bypassing the
  list. Unpacked mods in Mods\ need metadata.lua with `id` + `lua_revision` ≥
  350453. No Paradox cloud sync of account.dat (CloudSavesAllowed() = false).
- RunAll before/after pair NOT run: the Relaunched profile has never been created
  (%AppData%\Surviving Mars Relaunched\ has only Mods; no saves/logs/AccountStorage;
  no Steam userdata for appid 3215050) and mods can't be enabled until first launch.
  TestKit is now junctioned next to the fix pack. An opt-in autorun harness
  (TestKit Code\95_AutoRun.lua: flag-file gated, auto new game via
  NewGame/InitNewGameMissionParams/LoadLastNewGameSettings + fill g_CurrentMapParams
  + GenerateCurrentRandomMap, then RunAll with [SMRAUTO] markers, watchdog, quit())
  was being built when the session ended — it is NOT committed; check the TestKit
  repo before relying on it. Retail exe ignores -save/-map (goldmaster-gated,
  autorun.lua:126-144); Mars.exe launches directly, no external Paradox launcher.

## Next up

P2/P3 backlog in BUGS.md, roughly by value: F46 train cargo dumping, F36
university overtraining, F38 destroyed tunnels, F39 second artificial sun, F40
Dust Sickness on Biorobots, F41 Gene Forging, F17 Dust Sickness randomization,
F35 turbine buff sweep, F16 Mirror Sphere, F70/F71/F72 remaining lander issues,
F54 switched-off shuttle hubs, F59/F60/F62/F63 housing/service reach, F32
notification suppression, F33/F34 landscape nil guards. Then
`Code/90_SaveSanitizer.lua` and the D01 opt-in classic-rockets module.

## Key technical facts (hard-won, do not re-derive)

- **Mod code loads BEFORE the classes are built.** `autorun.lua:423` calls
  `ModsLoadCode()`; classes are assembled later in `OnMsg.Autorun`
  (`CommonLua\Core\classes.lua:980`). So at apply() time a class global is still
  its **classdef**, exposing only members the class declares ITSELF — an inherited
  method reads as nil. Two consequences:
  * `function Building:X() ... end` in a fix DOES propagate to every subclass
    (the classdef is what gets flattened later) — this is why class-method
    replacement works at all;
  * an apply() self-check must look for the method on its **declaring** class.
    Checking `Station.OnDemolish` (declared on Building), or
    `UniversalRocketBase.IsAutoModeEnabled` (declared on the AutoMode mixin),
    finds nil and silently deactivates the fix. F64 shipped broken this way and
    was corrected this session.
- `g_Consts` is a **GameVar** (`Lua\Modifiers.lua:427`) and does not exist while
  mods load — read it inside the patched function, never in apply(). `const` IS
  populated at that point.
- Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` (verified from working
  code paths) but NOT boolean relational compares — don't report/fix nil-iteration
  as crashes. `/` truncates (integer division); that is what makes F12's
  `a*24/v*24` unsatisfiable.
- **Mods run in a sandbox (LuaModEnv) on ALL platforms**, including unpacked dev
  mods (Mod.lua:1730/:1750; blacklist at :1267-1428). Key facts: `debug`, `io`,
  `package`, `lfs`, all `Async*` file ops, load/dofile/require are BLACKLISTED;
  `os` is `{time}` only; `setmetatable` is available (:1408 commented out);
  `rawget` is a safe wrapper that reaches real `_G` for non-blacklisted names —
  the pack's `rawget(_G, "X")` pattern works; `_G` maps to the env, but NEW
  globals created at load are rawset into the REAL `_G` (:1557-1563), so
  `SMRFixPack`/`SMRTest` are cross-mod and console visible; `Msg`/`OnMsg` are
  filtered only for persist/debug messages. The fix pack Code/ uses no
  blacklisted API (verified) — sandbox- and console-clean.
- **CORRECTION of an earlier "fact": `debug.getinfo` is NOT available in mod
  code** (debug is blacklisted). The Test Kit's install probes
  (00_TestCore.lua:37) break under the sandbox; repair in progress — bridge
  real `debug` via a console-exec path or SKIP install probes with a
  `SMRTest.debug = debug` console instruction. `GetStaticMsgNames()` (F06 probe)
  is a real global and still fine.
- Patch points that work: `PeriodicRepeatInfo[name]` slots (THREAD/SLEEP/FUNC/COND
  = 1..4, CommonLua\Core\lib.lua:1538+), `GlobalGameTimeThreadFuncs[name]` +
  `RestartGlobalGameTimeThread(name)` on LoadGame (Lua\Config\_fixup.lua),
  class-method replacement, chained wrappers, `OnMsg.*` additive handlers,
  preset/data patches at ClassesPostprocess.
- A post-wrapper on a **command** method (anything ending in `SetCommand`) never
  runs — `DoSetCommand` kills the calling thread. `Colonist:Idle` must be
  pre-wrapped (F73).
- Mod registry: every fix goes through `SMRFixPack.Register(id, {title, apply})`
  (Code/00_Core.lua); apply self-checks the target and returns a reason string to
  deactivate gracefully; `SMRFixPack_Disabled` = user veto; `SMRFixPack.ListFixes()`
  console status.
- All line numbers reference `ModTools\Src`; the game executes `Packs\Lua.fpk`
  (slightly newer date) — runtime self-checks in apply() are the guard.
  `GatherTransportableResources` (`ResourceTracking.lua:216`) is *called* but
  defined nowhere in Src — an engine export or an fpk-only function. F12's fix
  checks for it at apply time.
- Sample mod format in `<game>\ModTools\Samples\Mods`; docs in `ModTools\Docs\index.md.html`.

## Waiting on the user

1. Launch the game once with BOTH mods enabled, confirm `SMRFixPack.ListFixes()`
   shows 30 fixes active (any `inactive`/`error` line is a self-check that needs
   revisiting), then run `SMRTest.RunAll()` — this is the packaging + wiring
   validation for the whole pack.
2. Author name/handle for metadata.lua (placeholder TBD_SET_BEFORE_RELEASE), in
   both mods.
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.
4. An in-game observation for F55: do drones still enter a dome after the roof is
   opened? The Lua half of that report turned out not to be actionable (see the
   F55 entry) — only play can tell us whether the entity data is at fault.

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need active repair; six of those passes now ship
(see above), the rest are queued for the sanitizer module (F03 leaked modifiers,
F35 turbine buff, F48 connectors). ~15% is irreversible history (dead colonists,
lost expeditions; F64 voided trains have no recorded count — heuristic
compensation option at best, and document the vanilla train re-purchase at
stations, Station.lua:573-611). Save rescue is the headline differentiator vs
official patches ("new games only") — lead with it.

## Distribution facts (researched 2026-07-25, source-verified)

- BOTH Steam Workshop AND Paradox Mods are supported; the in-game Mod Editor has
  upload buttons for each (ModEditor.lua:78/:115). Steam Workshop reaches PC
  only; **Paradox Mods is the only channel that reaches Xbox/PS5** — platform
  fan-out is automatic on the backend, no platform fields, no modder-side
  signing (PS5 signatures are created client-side at install, Mod.lua:49-95).
  Console loads packed Lua code mods fine; no engine restriction found.
- PDX upload hard-requires: title, short_description (≤200 chars), description,
  preview image, lua_revision; last_changes on every update; ≤10 tags
  (ParadoxMods.lua:13-54, Mod.lua:410). GitHub repo link goes in metadata
  `external_links` — "github" is a supported LinkType shown on the PDX portal
  (Mod.lua:180-201). Default ignore_files already excludes *.git/*.
- Public repo: github.com/catt144/SMR-CommunityFixPack (main). Commit identity
  is the GitHub noreply address — never commit with a real email again.
- Achievements are disabled while any mod is active (ModManager.lua:78) —
  mention in the mod description.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
