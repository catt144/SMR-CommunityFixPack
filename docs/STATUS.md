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
- `debug.getinfo` is available — the Test Kit uses `.source` to tell whether a
  function now comes from the fix pack. `GetStaticMsgNames()` lists every message
  with a static handler, which is how the F06 probe proves a handler exists.
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

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
