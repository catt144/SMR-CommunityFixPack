# One-off: can the fix pack load first? A cross-vendor exploration (2026-09-24)

Single use, for a Codex seat. Authored at `2eadd83`. Start with `git log --oneline -8`, `git pull`
and `git status --short`. Peers commit concurrently, so commit only by pathspec.

## The question

Is there any way, at any level, for the Relaunched Fix Pack to make sure its code loads before
other mods' code? That covers the game's Lua, the engine, account storage, mod metadata, Steam,
Paradox Mods, the player's setup and anything else you find. If there is, the owner expects it
to solve nearly every load-order issue. Test that premise as well: say where loading first would
help, where it would not, and whether some other approach solves the same problems better.

The last time anyone looked was the 1.0.7 era, and it has never been checked by a second vendor.
Treat everything below as claims to confirm or overturn, not as settled facts.

**You have no limits on scope.** Read anything in the repo, the three archived game trees, the
live install, the Workshop mods on disk and anything public. Take any angle, and follow leads as
far as they go. The ideas at the end are starting points, not a checklist.

## What we currently hold

- **EF-054** ([facts/EF-054.md](../facts/EF-054.md), derived on 1.0.7): code runs in the
  player's enable order. `AccountStorage.LoadMods` is copied in order, `GetLoadingQueue` walks
  it depth-first with each mod's dependencies first, and `ModsLoadCode` runs `LoadCode` down
  that list. Under `LoadAllMods` the order is alphabetical by mod id instead. Its conclusion is
  that no mod can declare, request or detect its position ahead of its own load.
- **FIX_POLICY.md §8**: we prefer to load first as deference, not precedence. First is
  innermost, so we patch the vanilla code we verified and later mods wrap us. It says never to
  build on this, and there is deliberately no load-order advice for players, because the Mod
  Manager's list is a cosmetic sort. The same section records the first observed orders
  (2026-08-23/24): the pack loaded first on a player's rig and on the owner's.
- **EF-025** ([facts/EF-025.md](../facts/EF-025.md), 1.0.7): enabling a mod at the main menu
  loads code by a different path from a cold boot. `ClassesBuilt` fires on both paths and
  `DataLoaded` does not. Class globals are bare classdefs while mod code runs.
- **Read on 1.1.1.405907 today** (archived tree, `CommonLua/Modding/Mod.lua` unless noted):
  `GetLoadingQueue` :1907-1994, `GetModsEnabledByUser` :1995-2001, `GetModsToLoad` :2003,
  `ModsReloadItems` :2099, `ModsLoadCode` :2285, and `ModEnvMeta.__newindex` :1570-1576, which
  `rawset`s a mod's global writes into the real `_G`. `TurnModOn` is
  `CommonLua/UI/ModManager.lua:35-37` and appends to `LoadMods`. The 1.0.7 line numbers in
  EF-054 have moved; whether the logic did is yours to check.

## The case that prompted this (a hypothesis, not yet confirmed in-game)

Players on pack v19 report a startup dialog on every launch, saying the vacuum-walk fix switched
itself off. The current lead:

- Passage Network 1.38 ([archived copy](../../archive/PassageNetwork_1.38_Code_PassageNetwork.lua))
  has two stray `function Dome()` definitions at file scope, which replace the `Dome` class
  global with a function. The class rebuild after all mod code restores it.
- The pack's VacuumWalks checks at load time that `Dome` is a table
  (`Code/Fix_VacuumWalks.lua`, `has_110_helpers`). If Passage Network's code ran first, the fix
  declines and flags itself as broken by a game update, so the dialog names it.
- The owner's run on the reporter's save loaded the pack first, and the fix applied:
  `docs/archive/logs/reporter_TheGodUncle_modson_*.log`, lines 95 and 136.
- An owner sitting with the order reversed is planned to confirm or refute it.

Use it as a worked example if it helps. The question is the general one.

## Places to start (not a checklist)

- The archived game trees: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\` (1.0.7.396349, 1.1.0.403908,
  1.1.1.405907). The live install is `A:\SteamLibrary\steamapps\common\Project Spark`.
- Mod metadata fields and dependency handling (required and optional), including other mods
  declaring ours; anything mod code can write that changes the next launch's order; the
  alphabetical `LoadAllMods` branch; Steam required items; Paradox Mods.
- Hooks that run before or between mods' code; what mod options, items or entities load ahead of
  code.
- Late binding instead of early position: resolving targets at `ClassesBuilt` or later, and
  detecting and recovering from clobbered globals.
- What other Surviving Mars mods do: the Workshop mods under
  `B:\Dev\SMR\SMR-Shared\workshop_fpk_archive\`, ChoGGi's libraries, and public prior art.
- What changed in the loader between 1.0.7, 1.1.0 and 1.1.1.
- Whether "first" is the right goal at all, given the owner's deference reasoning in FIX_POLICY §8.

## What to hand back

Write a report at `docs/agent/reports/LOAD_ORDER_CROSSCHECK_2026-09-24.md`, or with the date
you run it. Mark each claim SOURCE-VERIFIED (with build and file:line), MEASURED (with the
command or log) or HYPOTHESIS (with the measurement that would decide it). Re-verdict each claim
above as confirmed, corrected or unproven. List every lever you found, working or not, with its
cost to players and its risks. End with your recommendation. The owner decides what, if
anything, gets built, and the Claude seat checks the report before any entry changes.

In the same commit, `git rm` this file and delete its row in `docs/agent/prompts/README.md`.
