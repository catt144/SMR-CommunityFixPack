# Cheat & Debug Inventory (for the Test Kit)

Inventory pass over `<game>\ModTools\Src\Lua\Cheats.lua` and
`Lua\XDef\GameCheatShortcuts.generated.lua` (plus the helpers they call).
Everything here is *shipped game code* — the Test Kit calls it, it does not
reimplement it.

## Getting a console

`ShowConsole` bails unless `AreCheatsEnabled() or ConsoleEnabled or Platform.asserts`
(`CommonLua\UI\Dev\uiConsole.lua:429-431`), and the **Enter / Alt-Shift-C**
shortcut is only created while that same condition holds
(`CommonLua\Classes\XDef\CommonShortcuts.generated.lua:174-186`).

- `AreCheatsEnabled()` = `Platform.cheats or AreModdingToolsActive()`
  (`CommonLua\gamelib.lua:1035`), and `AreModdingToolsActive()` is true when the
  Mod Editor / Mod Manager is open or `Game.testModGame` (`Mod.lua:144-146`) —
  i.e. **testing a mod from the Mod Editor gives you the console for free**.
- In a plain session the Test Kit turns it on itself: `ConsoleSetEnabled(true)`
  followed by `ReloadShortcuts()` (`SMRTest.EnableConsole()`, runs at mod load).

## The cheats-enabled gate

`CheatsEnabled()` (`Lua\Cheats.lua:1-3`) returns **only** `Platform.cheats` — it is
*not* the same as `AreCheatsEnabled()`. The DevMenu entries all sit behind
`if not CheatsEnabled() then return end`, but **almost every underlying `Cheat*`
function does not self-check** and can be called straight from the console.

Self-gated (won't run in a retail build): `CheatStartMystery`, `CheatChangeMap`.
For those, either run from a Mod Editor test session or temporarily set
`Platform.cheats = true` from the console before calling (Test Kit does the
latter, and restores it).

## Useful for our test plan

### Build / economy setup
| Call | Effect |
|------|--------|
| `CheatCompleteAllConstructions()` | finishes every construction site (Alt-B). Our "cheat-build X" scenarios = place it, then this |
| `CheatCompleteAllWiresAndPipes()` | same, cables/pipes only |
| `CheatFillAllStorages()` | fills every depot/storage (`StorageDepot.lua:2020`) |
| `CheatAddFunding(n)` / `CheatRemoveAllFunding()` | funding; default step $500M. Needed for the D01/rocket $1000M export floor |
| `CheatUnlockAllBuildings()` / `CheatUnlockAllSponsorBuildings()` | ignore build-menu prerequisites (F43 test needs this **off**) |

### Research
| Call | Effect |
|------|--------|
| `CheatResearchAll()` / `CheatResearchCurrent()` | grant techs. F35 (Frictionless Composites), F36 (Extractor AI), F41 (Gene Forging) all start here |
| `CheatUnlockAllTech()` / `CheatUnlockAllBreakthroughs()` | discovery only, no points |
| `UIColony:SetTechResearched(tech_id)` | the single-tech primitive the above use |

### Colonists
| Call | Effect |
|------|--------|
| `CheatSpawnNColonists(n, age_trait, backstory)` | spawns into the selected Dome, else spreads over all domes, else bare map. Backbone of F04/F52/F53/F58/F73 setups |
| `CheatGenerateApplicants(n)` | applicant pool (F08 before/after count) |
| `CheatUpdateAllWorkplaces()` | forces `UpdateWorkplaces(UICity.labels.Colonist)` — re-runs assignment on demand instead of waiting a sol |
| `CheatClearForcedWorkplaces()` | drops `user_forced_workplace` |
| `CheatToggleAllShifts()` | open/close every shift (F04 night-shift setup) |
| DevMenu "Max All Stats (Temp)" | inline: sets comfort/health/sanity to `100*const.Scale.Stat` per colonist — the F08/F09 satisfaction lever |

### Disasters (F01, F02, F45)
| Call | Effect |
|------|--------|
| `CheatMeteors(type, setting, pos)` | `type` = `"single"`/`"multispawn"`/`"storm"`; runs `MeteorsDisaster` in a game-time thread at the camera look-at. **This is how we break a track for F45** |
| `CheatDustDevil(major, setting)` | dust devil at camera look-at (F42) |
| `CheatTriggerMarsquake` / `CheatTriggerUndergroundMarsquake` / `CheatTriggerUndergroundCaveIn` | `Lua\Marsquake.lua:223-304`. Note: these **bypass** the `UndergroundMarsquake` repeat, so they still fire with F01 applied — that is expected, F01 gates the scheduler only |
| `CheatStopDisaster()` | broadcasts `CheatStopDisaster` |
| `g_Consts.MarsquakeSpawnTime = 1`, `g_Consts.MarsquakeRandomTime = 1` | compress the repeat's schedule for the F01 scenario |

### Mysteries (F06, F07, F15)
- `CheatStartMystery(<class id>)`, `CheatFinishMystery(<class id>)` (`Mysteries.lua:90,142`).
- Class ids (from the DevMenu ActionIds): `AIUprisingMystery`, `UnitedEarthMystery`,
  `DreamMystery`, `MarsgateMystery`, `MetatronMystery`, **`CrystalsMystery`
  (Philosopher's Stone — F06)**, `MirrorSphereMystery` (F16), **`LightsMystery`
  (St. Elmo's Fire — F07/F15)**, `DiggersMystery`, `BlackCubeMystery`, `TheMarsBug`.
- Starting a mystery while one runs auto-finishes the old one.

### Map / underground / asteroids (F31, F67-F73, C02)
| Call | Effect |
|------|--------|
| `CheatMapExplore("scanned" / "deep scanned" / "scan queued")` | reveal deposits |
| `UIColony:UnlockUnderground()` | underground access; `CheatRevealDarkness()` also generates the map and switches slot |
| `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` | **asteroid discover+scan+unlock** (Alt-Shift-A) — the entry point for every lander test |
| `CheatSpawnPlanetaryAnomalies()` / `CheatBatchSpawnPlanetaryAnomalies()` | planetary anomalies (C01) |
| `CheatUnlockBreakthroughs()` | resolves every map breakthrough anomaly |

### Rockets (F50, F56, F67-F72)
- `dbg_ToggleRocketInstantTravel()` (`RocketUtilities.lua:451`) flips
  `config.RocketInstantTravel` — collapses flight time so a Mars↔asteroid round
  trip is seconds. Essential for the lander trio.

### Terraforming / domes (F52, F55, F61)
- `SetTerraformParamPct(param, pct)` / `GetTerraformParamPct(param)`;
  `CheatChangeTerraformingParamPct(param, delta)`.
- `CheatOpenAllDomes()` / `CheatCloseAllDomes()` — note these *also* max/lower all
  terraforming params and toggle `LawDefs.Policy_OpenDomes`; for a pure F55 test use
  `OpenAllDomes()` / `CloseAllDomes()` directly.
- Atmosphere breathability is what gates F52: drive it with
  `SetTerraformParamPct("Atmosphere", n)`.

### Misc
- `CheatToggleInfopanelCheats()` — per-building cheat buttons in the infopanel
  (`config.BuildingInfopanelCheats`); the fastest way to break/repair/malfunction
  a single building.
- `MultiCheat()` — unlock all buildings + sponsor buildings + deep scan + research all.
- `CheatResetTutorials/Achievements/Challenges()`.
- `dbg_IgnoreReqs`, `dbg_ForceWither`, `dbg_ChangeSoilQuality(n)` — vegetation.

## Not found (do not look again)
No cheat exists for: forcing a specific colonist command, teleporting units,
setting a colonist's residence/workplace directly, spawning a specific disaster on
a *chosen* object, or fast-forwarding game time by an interval. For those the Test
Kit manipulates state directly (`SetCommand`, `g_Consts` edits, label surgery) —
see `Code\90_Loggers.lua`.
