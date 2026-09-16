# C97 re-check — an Opus pass over a mostly-Sonnet audit

**Run 2026-09-15 at the owner's request**, read-only, against live
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (1.1.0.403908) and the archived
1.0.7.396349 tree. ⛔ **NONE OF THIS IS APPLIED TO [C97](../bugs/C97.md) YET** — the entry still
carries every error below. Applying it is the next action; see the handoff.

⚠️ **Same-vendor check.** Claude re-checking Claude. The tier bump did real work (ten disagreements
on a filed entry) but it is weaker evidence than a cross-vendor pass would be. Recorded so nobody
reads a survived claim as independently corroborated.

## Disagreements — apply these to C97

**D1 — the scope proof is the wrong proof; the conclusion survives, the argument does not.**
C97 argues no normal-play reach because `g_Tutorial` is a plain global, never a GameVar. But
Findings 1, 2 and 4 are step-graph stalls driven by the tutorial state machine, and
**`g_TutorialStates` IS a GameVar** (`CommonLua/Libs/Tutorial/Tutorials.lua:32`, with
`g_TutorialQueue` `:31` and `g_TutorialVars` `:33`); `GameVar` sets `PersistableGlobals[name]`
(`CommonLua/Core/lib.lua:1061-1076`). Those three are written to savegames. What actually holds the
line is never stated in the entry: **saving is blocked outright while the tutorial game state is
set** — `OnMsg.CanSaveGameQuery` sets `query.tutorial` and `CanSaveGame` then returns nil
(`CommonLua/Savegame.lua:75-78`, `:92-98`); `CanAutosave` separately excludes `GameState.Tutorial`
(`:1474`). Depends on: `CanSaveGameQuery` being additive-only (all three handlers enumerated —
`Savegame.lua:75`, `CommonLua/Classes/Player.lua:64`, `Lua/Savegame.lua:54`) and
`Platform.developer` false in retail (`Savegame.lua:76` exempts developer builds).

**D2 — Finding 4's code fence is attributed to the wrong function, with an inverted condition.**
The fence C97 prints under `CheckWorkshiftsPreciousMetalsExtractor` is verbatim
`CheckWorkshiftsDiner` (`Lua/TutorialsNew.lua:2078-2082`). The real one (`:2072-2076`) uses a
different label and carries a **`not`** on `closed_shifts[2]` that the fence drops:
`MainCity.labels.PreciousMetalsExtractor` … `return extractor.closed_shifts and not
extractor.closed_shifts[2] and extractor.closed_shifts[3]`. The call sites are also paired
backwards: `Data/TutorialStep.lua:3290` is `CheckWorkshiftsDiner()`, `:3315` is
`CheckWorkshiftsPreciousMetalsExtractor()`. The unguarded-deref mechanism holds for both.
⛔ Anyone writing a fix or control off that fence gets the truth condition backwards.

**D3 — Finding 5's drone row is overstated three ways.** (1) "the consumer side survived untouched"
is false for this row: 1.0.7 had **three** consumers — `Lua/Units/Drone.lua:1783`, `:1813` and
`Lua/MultiSelection.lua:493` — and 1.1.0 has two; the MultiSelection one *was* cleaned up.
(2) In 1.0.7 the flag was true only inside one window of one tutorial (`Tutorial2.lua:189` set,
`:227` clear); everywhere else `g_Tutorial.Id ~= "Tutorial2"` already forced it false and already
showed "This feature has been disabled during the tutorials". What the rewrite lost is one
temporary enable window, not a working feature. (3) **No 1.1.0 step depends on it** — `reassign`
returns zero hits across `Data/TutorialStep.lua` and `Lua/TutorialsNew.lua`. Dead contract, not a
stall.

**D4 — Finding 3 lists a read with the wrong polarity.** `Data/XDef/RocketManualPayload.lua:249-252`
is `if g_Tutorial and (g_Tutorial.ManualRocketPayloadOnly and not g_Tutorial.SwitchToAutomode) then
return "disabled"` — a stuck-true `SwitchToAutomode` **enables** "SWITCH TO AUTOMATED MODE". Only
`:96`/`:197` (CANCEL/Escape) and `:228` (SWITCH TO PASSENGERS) are broken by it. The finding's
substance stands; the list of affected reads does not.

**D5 — Finding 2's masking bug is mis-mechanised and understated.** `MainCity.labels.X_Construction`
is nil **before the first construction site ever exists**, not merely empty after the last leaves —
`City:Init` pre-creates only `"Dome"` (`Lua/City.lua:56`). And the tick loop evaluates every
incomplete task of an active step every tick (`Tutorials.lua:212-228`), so task 2 self-ticks the
instant the step opens whenever nothing is selected, before the player does anything.

**D6 — refuted-hypothesis #1 is recorded against a line that was never a hazard.**
`TutorialsNew.lua:1112` is guarded on the next line (`:1113`). The unguarded deref is `:1117-1118`
(`local cargo_parts = rocket.cargo.MachineParts; cargo_parts.amount = …`). The refutation reasoning
does cover `:1117` — `UpdateCargoResourceRequests` backfills every `TransportableResourceIds` entry
(`Lua/CargoTransporterNew.lua:1430`, `:1439`, `:1451-1453`), called from `CmdUnload`
(`Lua/UniversalRocket.lua:580`) — so the outcome stands, but the citation aims a REFUTED verdict at
a non-hazard. Related: the backfill is in `UpdateCargoResourceRequests`, not `CmdUnload` itself.

**D7 — Finding 1's "sibling objective" contrast is a wrong citation.** `Data/TutorialStep.lua:216-229`
is inside the **next** step (`Step033_GatherMetal`, opens `:209`) and is `OnStart` `ScriptCode`
boilerplate, not an objective. The actual sibling with a `check_script` is `:168-195` (script
`:182-194`).

**D8 — "NOT OURS" rests on a string match, not an exposure audit.** The two named modules are the
only ones containing "tutorial". At least three more sit on Finding 1's rocket path and were neither
named nor cleared: `Fix_RocketDroneChurn` wraps `CargoTransporterNew:UpdateCargoResourceRequests`
(`Code/Fix_RocketDroneChurn.lua:82`), `Fix_TradeRocketFuelRefresh` wraps the
`UniversalRocketBase` override (`Code/Fix_TradeRocketFuelRefresh.lua:89`), `Fix_LanderEmptyLaunch`
wraps `UniversalRocketBase:IsCargoReady` (`Code/Fix_LanderEmptyLaunch.lua:45`, called at
`UniversalRocket.lua:500`/`:509`, whose sibling `:507` is itself `g_Tutorial`-gated).
⭐ **No defect was found in any of the three** — the disagreement is with the completeness claim,
which is load-bearing for a NOT-OURS verdict.

**D9 — "The run must be abandoned" omits a one-click recovery.**
`Lua/UI/PreGameMenus.lua:325-330`: `if g_Tutorial and g_Tutorial.UseTutorialId then
CreateRealTimeThread(StartTutorial, g_Tutorial.Id)`, and `UseTutorialId` is set for every tutorial
started via `StartTutorial` (`Lua/Tutorial.lua:97`). **Restart Map re-enters the same tutorial from
step 1.** Progress is lost so the finding is real, but the player is not left hunting for a save —
which also softens C97's "Who is actually affected" section.

**D10 (nit) — the ~107 KB figure double-counts.** `Tutorial1-5.lua` total **80,986 bytes (~79 KB)**;
adding 1.0.7's `Lua/Tutorial.lua` (26,019) reaches 107,005, but C97 credits that file separately.

## Extra findings — route into C97

**X1 — the best evidence for Finding 1 is in the tree and the entry missed it.**
`Data/TutorialStep.lua:2160-2185`: Asteroids `Step07_LandRocket` puts the `LandRocketTask` and the
`RocketUnloaded` reaction task **in the same step**, so the listener is registered before the player
can designate a landing site — no lost edge. Basics splits exactly those two across
`Step02_LandRocket` and `Step031_GameSpeed` with a manual Continue between. Same author, same
pattern, solved correctly once and split incorrectly once. Stronger than the (wrongly cited, D7)
contrast the entry offers.

**X2 — a second, un-enumerated member of the un-contained `expression` class.**
`ScriptableTutorialTask:Evaluate` calls `self.world_arrow_find_target()` raw at
`Lua/TutorialsNew.lua:1631`; it is declared `editor = "expression"` (`:1600`) — a plain Lua
function, no `ScriptProgram`, no `procall` — and `Evaluate` is called bare from the tick loop
(`Tutorials.lua:218`). Five of the 15 such expressions deref unguarded: `Data/TutorialStep.lua:1558`
(`AllRockets[1]`), `:3285` (`Spacebar_Small[1]`), `:3310` (`PreciousMetalsExtractor[1]`), `:3494`
(`g_TutorialVars.Trains.deposit`), `:3745` (`…Trains.dome_station`). ⛔ **Reach not established for
any** — Latent grade, same as the entry's `HexAxialDistance` item.
⭐ **Control separating this class from Finding 4:** one throw here freezes the *entire* step UI at
once (one tick thread serves all tasks); Finding 4 stalls exactly one objective while the rest keeps
ticking. "The whole tutorial froze" vs "one tick never appeared" distinguishes them.

**X3 — a Finding-4-shaped stall in Trains, which C97 lists as not opened.**
`Data/TutorialStep.lua:3750`/`:3755` deref `g_TutorialVars.Trains.dome_station.trains_in_construction`
two levels unguarded; `dome_station` comes from `FindObjectOfClassAroundMyDome("StationSmall")`
(`:3630`), which returns nil when `UIColony.labels.Dome[1]` is falsy or the search finds nothing
(`TutorialsNew.lua:592-597`). procall-contained, so a permanently stalled step. Reach low. Record,
do not file. **Control:** demolish the Train Station right after the step that builds it completes,
then see whether the next step advances.

**X4 — two negatives chased and killed; recorded so nobody re-derives them.**
(a) `SpawnUIArrow` does **not** permanently defeat its own `complete_task_after` monitor: `:92` sets
visible false and the `visibility_update` thread (`:104-113`) restores only transparency, but the
arrow's own update loop calls `SetVisible(true, true)` whenever it finds a visible target
(`Lua/TutorialUI.lua:78-83`). **Not a bug**, and it is Finding 2's exact shape, so it will catch the
next reader. (b) `OnMsg.DialogSetMode` is assigned twice in `TutorialsNew.lua` (`:391`, `:2259`) and
the first is **not** lost — `OnMsg` has a `__newindex` appending to a per-message handler list
(`CommonLua/Core/cthreads.lua:64-73`). **Not a bug.**

## What the re-check confirmed

Independently re-derived and holding: the four whole-word `g_Tutorial` writes
(`Lua/Tutorial.lua:34, :60, :75, :168`) and no others, with all 23 negated-grep candidate reads
opened; Claim D's containment boundary in both halves (`CommonLua/Scripting.lua:412-417`, `:419-424`;
bare `Evaluate` at `Tutorials.lua:218`); Finding 1's full mechanism including **no escape**
(`RocketUnloaded` fired from exactly two sites tree-wide, no replay — `ReapplyObjectReactions`
re-registers instances, it does not re-deliver, `CommonLua/Reactions.lua:424-460`); both named
modules' neutrality, with `Fix_ScanDowngrade`'s residual **narrowed** to the F3 call only (the F4
call at `TutorialStep.lua:983` has no `IsDepositObstructed` stub); and the 1.0.7→1.1.0 file diff.

⭐ **Claim E is now strictly stronger than when filed**: the computed-key escape hatch C97 could only
acknowledge is **closed** — exactly two computed-key writes to `g_Tutorial` exist tree-wide
(`TutorialsNew.lua:2576`, `:2677`), both
`[self.rocket_mode == "Manual" and "ManualRocketPayloadOnly" or "AutoRocketPayloadOnly"]`, neither
able to synthesise any of the five names.

⚠️ Also found: a second `EF-005` site the entry does not name — `#MainCity.labels.AllRockets` at
`TutorialsNew.lua:1106`. Tolerated.

## Not checked — stated, not implied

The Metals exhaustion item (map deposit inventory never sampled) · the Colonists/Trains/Asteroids
step graphs edge-by-edge for further Finding-1 shapes (spot-checked only; X1 is the counter-example
found) · the `Tutorial_Politics_*` orphan popups · `SpawnWorldArrow`'s nil-return reach ·
`HexAxialDistance` on a boolean (C export) · nothing was run in the game.

## Readiness verdict

**Not ready to base a code fix on.** Finding 1 is the only item worth a fix and its incidence is
unbounded with a one-click recovery (D9). Finding 5 should not be in fix scope until someone shows a
step that needs the flag — the drone row is dead code (D3). And the entry needs D1–D10 applied
first, because D1/D2/D4/D7 are the kind of errors that propagate into a fix or a control recipe.

**Cheapest next step, unchanged:** one ~10-minute Basics run — designate the landing site, let the
rocket fully land and unload, then press Continue, and watch whether the "Wait for the Rocket to
land" objective ever ticks. That converts C97 from source-derived to reproduced.
