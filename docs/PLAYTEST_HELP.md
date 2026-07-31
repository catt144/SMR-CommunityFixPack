# Playtest Help — setup, commands, reference

Companion to [PLAYTEST_CHECKLIST.md](PLAYTEST_CHECKLIST.md), which carries
ONLY the tests. Everything here is reference material for running them:
ground rules, the external-validity rule, cheat discipline, console facts,
the verified command table, Test Kit helpers, the stress harness, and the
save-fixture recipes. Split out of the checklist 2026-07-30 so tests are
findable there and commands are findable here.

---

## Ground rules

1. **NO third-party mods.** Not ChoGGi's library, not anything else. The only tools
   allowed are:
   - the **game's own console** (the Test Kit enables it at load — open with
     **Enter** or **Alt-Shift-C**),
   - the game's **shipped `Cheat*` functions** (see the verified table below),
   - **`g_Consts` / `const` tweaks** from the console,
   - the **Test Kit's own helpers** (`SMRTest.Log.*`, `SMRTest.Report*`,
     `SMRTest.RunAll()`).
2. **Both mods stay enabled** for every test except PT-20 (uninstall safety), which
   disables *the fix pack only* and keeps the Test Kit on.
3. **The Test Kit must NEVER be uploaded anywhere** — not Workshop, not Paradox Mods,
   not the public repo release. It is a dev-only companion.
4. **Achievements stay ON with mods on PC** (they are mod-blocked only on
   console/MS Store — `DoModsBlockAchievements()`, `Achievement.lua:61-63`), so an
   unlock during playtesting is normal. Cheat use is logged per save and blocks
   that save's further unlocks on retail (`Network.lua:241-255`) — so cheated
   fixture saves police themselves; you may still pop legitimate achievements in
   the minutes before the first cheat.
5. If a step's setup fails, write that down. "Could not set this up" is a valid and
   useful result.
6. **The console AUTO-OPENS shortly after a colony is up — loads AND new
   games** (Test Kit; the 2026-07-26 build waits for the loading screen to
   close, fixing the dead console every NEW save used to get — takes effect
   from the next game launch). If closed, reopen with **Ctrl-Alt-C** (the
   kit's own binding, rebuild-proof) or Enter / Alt-Shift-C (the shipped
   binding — worked in the same verification, but one earlier session had it
   inexplicably dead, hence the fallbacks). Last resort: a Mod Editor test
   session grants the console unconditionally.

### ⚠️ EXTERNAL VALIDITY — how far our results generalise (added 2026-07-29)

**Everything in this document is tested under conditions no ordinary player
experiences**, and that needs saying once, plainly, so no result is over-read.
Our evidence comes from either (a) purpose-built fixture saves, or (b) a live
colony with **all techs researched, cheat-filled depots, heavily over-provisioned
drone fleets, and layouts arranged for the test at hand** — e.g. domes placed to
exercise cross-dome migration, distances set up to exercise range logic. That is
the right way to force a scenario quickly; it is not the way anyone plays.

**Read results through this split:**
- **Correctness claims generalise.** A nil-iteration bug, a dead `if`, an
  unremoved notification, an unbounded loop — these are condition-independent.
  If the code path is wrong it is wrong at any base size. Most `Fix_*` modules
  are in this class and their `tested` flags mean what they say.
- **Behavioural and timing claims do NOT generalise automatically.** Anything
  about speed, contention, throughput, assignment quality or "does the player
  notice" depends on scarcity, fleet size, density and layout — all of which our
  test conditions distort. **State the conditions whenever such a result is
  recorded**, and treat the result as a measurement of *that* colony, not of the
  game.

**Worked example, D06 (2026-07-29):** the drone A/B returned a null result for
the claim gate — but the colony had pre-filled depots and 14-24 idle drones per
hub, i.e. almost no contention for the gate to arbitrate. The measurement was
internally valid and externally misleading. The same sitting's numbers
nonetheless showed severe hauling delays *despite* every environmental axis
being favourable, which is a condition-independent signal pointing the other
way. Full analysis on the D06 entry — it is the model for how to write these up.

### Cheating without contaminating results

Cheat the **setup**, never the **mechanism under observation**. The fixes patch
decision logic; cheats inject state (money, goods, people, buildings) — state
injection is exactly what the scenarios need. Each PT's Setup line names its
cheats; when one must stay OFF, the PT says so. Standing accelerators — use
freely: `CheatAddFunding`, `CheatCompleteAllConstructions`, `CheatFillAllStorages`,
`CheatResearchAll`, `CheatSpawnNColonists`, `CheatUpdateAllWorkplaces`,
`dbg_ToggleRocketInstantTravel`, `CheatToggleInfopanelCheats`, `MultiCheat`.
Two standing cautions:

- **Notification/warning windows run on GAME time**, not wall-clock (measured
  live 2026-07-27: the "Building Not Working" dismissal window is 120,000
  game-ms = 4 game hours) — higher game speed SHORTENS such waits, it does not
  stretch them.
- **PT-10 / F55**: use `OpenAllDomes()`, not `CheatOpenAllDomes()` — the Cheat
  variant also maxes terraforming params and muddies the observation.

### ⚠️ Compressing a scheduler with `g_Consts` — the false-PASS trap (learned running PT-11, 2026-07-29)

**Lowering a `g_Consts` interval does NOT shorten the sleep already in flight.**
A `MapGameTimeRepeat` body computes its next interval at the END of each tick
and then sits in `Sleep(sleep)` (`CommonLua/Core/lib.lua:1590-1592`), so the
running thread keeps whatever interval it was handed *before* your edit.

This silently invalidates any "nothing should happen" test. PT-11's defaults are
`MarsquakeSpawnTime = 384` hours and `MarsquakeRandomTime = 96`
(`Lua/__const.lua:1085-1094`) — **16 sols**. Waiting the prescribed 20 hours
after setting them to 1 would have watched a thread still asleep on the old
16-sol interval and scored it a PASS whether or not the fix worked.

**Always re-arm after compressing, and prove the thread is live:**
```
RestartPeriodicRepeatThread("UndergroundMarsquake", CurrentMap)
IsValidThread(CurrentMap.RepeatThreads.UndergroundMarsquake)
```
The restart does not bypass a fix that wraps the repeat — the wrapper lives in
`PeriodicRepeatInfo`, which the fresh thread re-reads every loop. **Repeat the
restart after every save/reload:** repeat threads are persistable
(`MakeThreadPersistable`, `lib.lua:1595`), so a reload restores the old sleep.

**Pair every negative result with a positive control.** A cheat that forces the
event, run at the END, proves the map can produce it and that your detector
actually moves. Without one, a negative test cannot distinguish "the fix worked"
from "nothing would have happened anyway". Prefer an **objective counter** over
eyes — e.g. `CurrentMap:MapGet("map", "CaveInRubble")` — since events at ultra
speed are easy to miss.

### Salvage mode — how to read the cursor (observed 2026-07-30, applies to EVERY salvage test)

Reported by the tester while running PT-46(c), and general to the whole map —
not a train-station quirk. Any test that involves salvaging or demolishing
should be read through these three facts:

1. **Salvage mode targets OBJECTS, never hexes.** You cannot click a bare hex.
   If no live object occupies the spot, there is nothing to click and the hex
   itself is not drawn.
2. **The cursor always NAMES what it is about to remove**, for everything:
   `Salvage Stirling Generator`, `Salvage Power Cable`, `Salvage Wind Turbine`,
   `Salvage Track`, `Salvage Train Station`. Line-drawn things add
   `CTRL + click — Salvage entire length`. There is therefore no such thing as
   a silent mis-target in salvage mode: whatever the tool is going to destroy,
   it says so first.
3. **The word `Salvage` alone, rendered in RED, means "no action permitted
   here"** — nothing targetable under the cursor. It draws at the true mouse
   position (screenshots do not capture the cursor itself, so the red label is
   where the pointer actually was).

**Why this matters beyond one test.** Fact 3 gives a positive read for
"nothing is targetable", which turns several otherwise eyes-only checks into
definite observations — e.g. F49(c), where the fix makes a station-owned
connector element propagate to nothing in demolish mode: red `Salvage` over a
connector position is the fix engaging, whereas `Salvage Train Station` over a
hex that is not the station body would be the guard failing. Fact 2 also bears
on **severity** assessments: a defect that mis-resolves a salvage target is
announced to the player before they commit, so it can never be a silent trap.

### Console: what works and what silently does nothing

On a retail build the console runs inside the **mod sandbox** (`CommonLua/console.lua:27-56`:
non-asserts + `config.Mods` → `g_ConsoleFENV = LuaModEnv(...)`, and its `__index`/`__newindex`
both return/drop anything in `ModEnvBlacklist`). Consequences you must know:

- Reads and writes of **non-blacklisted** names go straight to the real `_G`
  (`console.lua:48,53`) — so `g_Consts.X = 1`, `CheatFoo()`, `UIColony:Bar()` all
  work normally.
- **Blacklisted names read back as `nil` with no error** (`CommonLua/Classes/Mod.lua:1267-1428`).
  Do not use these in console snippets — they will look like the game is broken:
  `debug`, `io`, `os`, `package`, `lfs`, `_G`, `rawget`, `getmetatable`, `setfenv`,
  `getfenv`, `load`/`loadstring`/`dostring`/`dofile`/`require`, `collectgarbage`,
  `ConsoleExec`, **`Msg`**, **`OnMsg`**, and all `Async*` file/web calls.
  (`setmetatable` and `rawset` ARE available.)
- Console input forms (`CommonLua/UI/Dev/uiConsole.lua:355-366`):
  | You type | What happens |
  |---|---|
  | `SMRFixPack.ListFixes` | bare dotted name → auto-**called** and printed |
  | `UIColony.day` | expression → printed |
  | `g_Consts.MarsquakeSpawnTime = 1` | statement → executed |
  | `*r <code>` | runs `<code>` in a **real-time thread** (use for multi-statement snippets) |
  | `*g <code>` | runs `<code>` in a **game-time thread** (use when you need `Sleep`) |
  | `~<expr>` | opens the object inspector on `<expr>` |
- ⚠️ **NEVER put a `--` comment in a `*r` / `*g` snippet** (found the hard way
  2026-07-29). Those rules splice your code into a template **on one line**:
  `CreateRealTimeThread(function() %s end) return` (`uiConsole.lua:360`). A
  trailing comment therefore swallows the closing `end) return`, the chunk will
  not compile, no rule matches, and the console answers **`not understood`**
  (`console.lua:24`). The same goes for annotations like `--> nil` pasted from
  documentation.
- ⚠️ **The console input is ONE LINE.** Pasting a multi-line block concatenates
  the lines into a single command — e.g. `... --> nil` + `UIColony:Set...` came
  through as `--> nilUIColony:Set...`. Paste one command at a time. Write
  snippets in docs WITHOUT trailing comments so they stay paste-safe.
- **Prefer a bare expression over `*r ConsolePrint(...)` for a simple read.**
  Rule `{ "(.*)", "ConsolePrint(print_format(%s))" }` (`uiConsole.lua:363`)
  wraps ANY input that compiles as an expression, so typing
  `GetRareTraitChance()` prints its value by itself. `*r` is only needed for
  multi-statement snippets or ones that must not block.
- `g_Consts` is a **GameVar** — it does not exist at the main menu. Run everything
  from inside a loaded colony.

### Verified command reference (every entry checked in `ModTools\Src`)

| Command | Source | Use |
|---|---|---|
| `CheatCompleteAllConstructions()` | `Lua/Cheats.lua:118` | "cheat-build": place it, then finish it instantly |
| `CheatCompleteAllWiresAndPipes()` | `Lua/Cheats.lua:99` | same, cables/pipes |
| `CheatFillAllStorages()` | `Lua/Buildings/StorageDepot.lua:2020` | fill every depot |
| `CheatAddFunding(n)` | `Lua/Cheats.lua:132` | funding |
| `CheatUnlockAllBuildings()` / `CheatUnlockAllSponsorBuildings()` | `CommonLua/Features/LockablePreset.lua:626` / `Lua/Cheats.lua:337` | ignore build-menu locks |
| `CheatResearchAll()` | `Lua/Cheats.lua:78` | grant all techs — **EXCEPT undiscovered breakthroughs** (the loop skips non-`discoverable` fields unless the tech is already discovered, `Cheats.lua:84`; verified live 2026-07-27). Grant a specific breakthrough directly: `UIColony:SetTechResearched("<Id>")` (discovers it itself, `Research.lua:285`); or `CheatUnlockAllBreakthroughs()` first, THEN `CheatResearchAll()` |
| `MultiCheat()` | `Lua/Cheats.lua:328` | unlock all + deep scan + research all |
| `CheatSpawnNColonists(n, age_trait, backstory)` | `Lua/Cheats.lua:225` | spawn into selected dome, else spread |
| `CheatGenerateApplicants(n)` | `Lua/ApplicantsPool.lua:210` | applicant pool |
| `CheatUpdateAllWorkplaces()` | `Lua/Cheats.lua:210` | re-run job assignment now |
| `CheatToggleAllShifts()` | `Lua/Cheats.lua:192` | open/close every shift |
| `CheatToggleInfopanelCheats()` | `Lua/Cheats.lua:290` | shows per-building cheat buttons — ⚠️ **on retail the buttons render but silently NO-OP** (they dispatch `NetSyncEvents.ObjCheat`, gated `AreCheatsEnabled()`, `Network.lua:218-219`; found live 2026-07-27). Either run `Platform.cheats = true` first (buttons work; set false after), or skip the panel and call the method directly on the selection: `SelectedObj:CheatMalfunction()` / `CheatAddMaintenancePnts()` / `CheatCleanAndFix()` (`Building.lua:1813-1849`). Second gotcha (2026-07-27): button presses ride the game-time sync queue (`ScheduleOfflineSyncEvent`) — they look DEAD while the game is paused and fire on unpause; the `ObjCheat <method>` console print confirms delivery |
| `CheatMeteors("single"\|"multispawn"\|"storm", setting, pos)` | `Lua/Cheats.lua:62` | meteor strike. **AIM IT AT THE MOUSE (added 2026-07-30 — this is the form you usually want):** `pos` is the **THIRD** argument, so you cannot just append it — pass `nil` for `setting` to keep the map default. Fire at the pointer, with 3 real seconds to aim first (your mouse is over the console when you press Enter, so a bare call would strike there): `*r Sleep(3000) CheatMeteors("single", nil, GetTerrainCursorClamped())`. `GetTerrainCursorClamped()` (`CommonLua/Classes/MapData.lua:25-30`) is safer than raw `GetTerrainCursor()` — it clamps into the play area so an off-map cursor cannot hand you a bad position. To hit a SPECIFIC building instead, select it and skip the mouse: `CheatMeteors("single", nil, SelectedObj:GetPos())`. `"single"` completes cleanly; `"storm"` is the one that wedges (below). The cheat drives the disaster directly, so it fires even under the **No Disasters** rule — by design, same as `CheatTriggerUndergroundMarsquake`. ⚠️ **RE-CORRECTED 2026-07-29 (QA session):** with no explicit `pos` it can silently do NOTHING — but the mechanism recorded earlier was wrong. `GetCameraLookAtPassable` is a **file-local helper** (`local function`, `Cheats.lua:42`) — invisible from the console *by design*, which is what the `attempt to call a nil value` probe actually proved; the shipped `Cheats.lua` is byte-identical to Src (full fpk diff, see ENGINE_FACTS.md). The real no-op path: the helper returns nil when no passable point exists within 100m of the camera look-at, and the body is `if pos then … end` with no else. **Always pass a position**, or drive the disaster directly: `*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`. Note `"storm"` reliably WEDGES (F78) — with the pack loaded, `Fix_MeteorStormWedge` heals it automatically ~2 game hours after the storm notification expires (PT-54); manual recovery remains `*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end` |
| `CheatTriggerMarsquake(settings_name)` | `Lua/Marsquake.lua:223` | surface quake |
| `CheatTriggerUndergroundMarsquake()` | `Lua/Marsquake.lua:292` | underground quake (**bypasses** the scheduler on purpose — which is what makes it a sound positive control for any "no disasters" watch; PT-11, archived) |
| `CheatTriggerUndergroundCaveIn(pos)` | `Lua/Marsquake.lua:284` | cave-in at a position |
| `CheatStopDisaster()` | `Lua/Cheats.lua:74` | stop the running disaster |
| `CheatStartMystery(id)` | `Lua/Mysteries/Mysteries.lua:91` | **gated on `Platform.cheats`** — see PT-15 |
| `CheatMapExplore("scanned"\|"deep scanned"\|"scan queued")` | `Lua/Cheats.lua:5` | reveal deposits |
| `UIColony:UnlockUnderground()` | `Lua/Colony.lua:490` | underground access |
| `CheatRevealDarkness()` | `Lua/Cheats.lua:390` | generate + switch to the underground map |
| `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` | `Lua/Discoveries.lua:35`, call form at `Lua/XDef/GameCheatShortcuts.generated.lua:184` | asteroid discover + scan + unlock |
| `dbg_ToggleRocketInstantTravel()` | `Lua/Buildings/RocketUtilities.lua:451` | collapse flight time (Mars↔asteroid in seconds). ⚠️ **It is a TOGGLE, and `config.RocketInstantTravel` is not a GameVar** — a second call turns it back OFF, and it resets to OFF on every relaunch. **Verify the state, never assume:** type `config.RocketInstantTravel` (bare expression → prints `true`/`false`). Two mechanisms, both real: the flag makes `AdjustFlightTime` / `ApplyRocketTravelTimeModifier` return **0** for flights launched while it is on (`RocketBase.lua:921-923`, `UniversalRocket.lua:675-677`), and toggling ON also fires `Msg("RocketInstantTravel")` once, which wakes rockets **already** in flight (`WaitMsg("RocketInstantTravel", flight_time)` — `LanderRocket.lua:541`, `RocketBase.lua:288/:962`); `UniversalRocketBase:SleepFlight` additionally re-checks the flag every ~5 s. Its own `print("Rocket Instant Travel:", …)` confirmation is on-screen only, never in the log |
| `SetTerraformParamPct(param, pct)` | `Lua/Terraforming.lua:210` | e.g. `SetTerraformParamPct("Atmosphere", 95)` |
| `CheatOpenAllDomes()` / `CheatCloseAllDomes()` | `Lua/Cheats.lua:414` / `:426` | opens domes **and** maxes terraforming + Open Domes policy |
| `OpenAllDomes(MainCity)` / `CloseAllDomes(MainCity)` | `Lua/Buildings/Dome.lua:3415` / `:3423` | open/close only, no side effects |
| `SetLightTrapMode("free"\|"destroy")` | `Lua/Mysteries/Fireflies.lua:674` | St. Elmo's Fire wisp disposition |
| `CompleteMilestone(id, res)` | `Lua/Milestones.lua:108` | complete a milestone by id |
| `ColonyGetPrefabs("Train", MainCity)` | `Lua/Colony.lua:681` | stored-prefab counter |
| `OpenCommandCenter()` / `CloseCommandCenter()` | `Lua/X/ColonyControlCenter.lua:1614` / `:1630` | Command Center UI |
| `SetGameSpeedState("ultra")` | `Lua/X/HUD.lua:528` | 20× (`const.ultraGameSpeed = 20`, `Lua/_GameConst.lua:28`) |
| `UIColony:SetGameSpeed(n)` | `Lua/Colony.lua:564` | arbitrary factor; `n = 20` == ultra. Higher values work (clamped at `const.MaxTimeFactor`) but stress the sim — prefer 20 |
| `CheatRemoveAllFunding()` | `Lua/Cheats.lua:144` | zero the funding (poverty setups) |
| `CheatUnlockAllTech()` / `CheatUnlockAllBreakthroughs()` | `Lua/Cheats.lua:166` / `:281` | discovery only, no research points granted |
| `CheatUnlockBreakthroughs()` | `Lua/Cheats.lua:264` | resolves every breakthrough anomaly on the map |
| `CheatClearForcedWorkplaces()` | `Lua/Cheats.lua:214` | drops every `user_forced_workplace` |
| `CheatDustDevil(major, setting)` | `Lua/Cheats.lua:47` | dust devil at the camera look-at |
| `CheatFinishMystery(id)` | `Lua/Mysteries/Mysteries.lua:142` | complete the running mystery. Mystery class ids (from the DevMenu tree): `AIUprisingMystery`, `UnitedEarthMystery`, `DreamMystery`, `MarsgateMystery`, `MetatronMystery`, `CrystalsMystery` (Philosopher's Stone — F06), `MirrorSphereMystery` (F16), `LightsMystery` (St. Elmo's Fire — F07/F15), `DiggersMystery`, `BlackCubeMystery`, `TheMarsBug`. Starting a mystery while one runs auto-finishes the old one |
| `CheatSpawnPlanetaryAnomalies()` / `CheatBatchSpawnPlanetaryAnomalies()` | `Lua/Cheats.lua:26` / `:38` | planetary anomalies (C01 material) |
| `CheatChangeTerraformingParamPct(param, delta)` / `GetTerraformParamPct(param)` | `Lua/Cheats.lua:343` / `Lua/Terraforming.lua:219` | relative terraforming nudge / read-back |
| `g_Consts.MarsquakeSpawnTime = 1` + `g_Consts.MarsquakeRandomTime = 1` | `Lua/Marsquake.lua` scheduler consts | compress the underground-quake schedule (PT-11 setup). ⚠️ **Setting the const is NOT enough on its own — see the rule below** |
| `RestartPeriodicRepeatThread("<RepeatName>", CurrentMap)` | `CommonLua/Core/lib.lua:1637` | **re-arm a `MapGameTimeRepeat` after compressing its consts.** Verify with `IsValidThread(CurrentMap.RepeatThreads.<RepeatName>)` → `true` |
| DevMenu "Max All Stats (Temp)" equivalent | inline per colonist | set comfort/health/sanity to `100*const.Scale.Stat` directly — the satisfaction lever for F08/F09 setups |

**No cheat exists** (inventoried 2026-07; do not look again) for: forcing a
specific colonist command, teleporting units, setting a colonist's
residence/workplace directly, spawning a disaster on a *chosen* object, or
fast-forwarding game time by an interval. For those, manipulate state directly
(`SetCommand`, `g_Consts` edits, label surgery — the TestKit's
`Code/90_Loggers.lua` has patterns).

⚠️ **The cheat keyboard shortcuts (Alt-B, Alt-Shift-A, …) do NOT exist on a retail
build** — the whole DevMenu shortcut tree is gated on `local cond = Platform.cheats`
(`Lua/XDef/GameCheatShortcuts.generated.lua:19-20`), and `CheatsEnabled()` returns
only `Platform.cheats` (`Lua/Cheats.lua:1-3`). Always type the **function call** in
the console instead. (The *console* itself is separate — the Test Kit turns it on
with `ConsoleSetEnabled(true)` + `ReloadShortcuts()`.)

### Test Kit helpers (names read from `TestKit\Code\90_Loggers.lua` / `00_TestCore.lua`)

| Call | What it does |
|---|---|
| `SMRTest.Loggers` | list every logger and whether it's ON |
| `SMRTest.Log.Meteors(true/false)` | prints each `MeteorsDisaster` call with the gap in game hours |
| `SMRTest.Log.DroneChurn(true/false)` | prints how many drones a rocket's reconnect just kicked to Idle |
| `SMRTest.Log.AutoCargo(true/false)` | prints each lander auto-cargo request + what's aboard |
| `SMRTest.Log.CargoReady(true/false)` | prints each `IsCargoReady` verdict |
| `SMRTest.Log.WorkShift(true/false)` | prints shift-3 `ShouldLeaveForWork` verdicts |
| `SMRTest.ReportBrokenTrack` | counts track repair sites with a non-numeric `node_idx` |
| `SMRTest.ReportReservations` | counts stale residence reservations — **PT-21** |
| `SMRTest.ReportTrains` | stored train prefabs vs trains on the map — **PT-21** |
| `SMRTest.RunAll` | re-run the whole probe suite (sanity check before/after a session) |
| `SMRFixPack.ListFixes` | per-fix status — all **67 default fixes** should read `active`, incl. `DroneStatDials` (active-at-base = armed, vanilla behavior) (opt-in modules read `inactive` unless toggled ON; `Code/00_Core.lua`). **67, not 69, since 2026-07-30** — `DomePipeMoveInside` (F24) and `ReplaceTechCount` (F28) were both deleted that day |

**Drone dispatch STRESS HARNESS** (`Code/91_Stress.lua`, added 2026-07-29;
**v2 lifecycle-tracing rebuild 2026-07-29** after the first run proved the v1
headline metric scored deliveries, not claims — turns PT-52 from
watch-and-judge into a measured A/B). Breaks a **deterministic** seeded set of
buildings and traces each one's FULL request lifecycle via chained wrappers on
`RequestAssignUnit`/`RequestUnitFulfill` plus
`StartDemandPhase`/`StartWorkPhase`/`Repair` timestamps. Reload the same save,
flip ONE variable (the D06 toggle, or one stat dial), run the identical call,
and the two legs cover the identical targets.

| Call | What it does |
|---|---|
| `SMRTest.Stress.Targets{scope=, n=, seed=}` | dry run — what WOULD be broken, breaks nothing |
| `SMRTest.Stress.Break{scope=, n=, seed=}` | break the set and start watching (defaults `scope="overlap"`, `n=25`, `seed=1`; also `pure_only=` no-resource targets only, `label=` free text stamped on the run, e.g. `"speed1.5x"` for a stat-dial leg) |
| `SMRTest.Stress.Report()` | current or last summary (also prints itself when a run ends) |
| `SMRTest.Stress.Compare()` | last two runs side by side + deltas — **the A/B verdict** (`Compare{a=,b=}` picks other history entries; keeps 6) |
| `SMRTest.Stress.HealAll()` | panic button: repair everything, end the run |
| `SMRTest.Stress.Stop()` | end early, keep the numbers |

Scopes: `overlap` (default — only buildings covered by 2+ hubs, the population
the claim gate arbitrates), `hub` (selected hub's coverage), `dome`, `radius`,
`all`. Protected classes are never broken unless `include_all = true`: drone
hubs AND extenders (never break the system under test), domes, life support,
power. Buildings with no covering hub — or maintenance-prevented (rubble) —
are counted and skipped. A save load mid-run aborts the run cleanly (history
kept — that is what makes the cross-reload `Compare()` work).

**Reading the report (v2).** Every repair decomposes into
`haul queue` (demand posted → first haul claim — dispatch latency) ·
`haul exec` (claim → delivered) · `claim wait` (work posted → first repair
claim) · `travel` (claim → repairer arrived) · `repair`. The gate verdict is
the **GATE-DECIDED first claims** line: closest-hub share computed ONLY over
claims that actually went through `FindTask`. Deliverer **handoffs** (a drone
that delivered takes the first repair tick directly, bypassing FindTask —
`claim wait` ≈ 0) and handoff **MISFIRES** (a SHUTTLE delivered;
`CargoShuttle` has no `Work` command, so `StartWorkPhase(shuttle)` fizzles
and the claim falls back to FindTask — verified vs Src 2026-07-29) are
counted separately, with the deliverer mix. Every summary carries a
**run-conditions header** (module state, game speed, live drone
move_speed/carry, per-hub idle counts, shuttle fleet, pre-surge depot
availability) — per the EXTERNAL VALIDITY rule, never read a run's numbers
without it. Total clearance time is still NOT a D06 score.

Turn loggers **off** when a test is done — they print every tick and will bury the log.

---

## The ENABLE-PATH leg — the session shape the harness never measured (added 2026-07-31, F87)

**Every A/B leg we have is a COLD BOOT** — the game launches with the pack
already enabled, so all `N/74` figures describe the *second session onward*. **A
player's first session is a different load order**: a mod is never auto-enabled,
so they tick it at the main menu of a running process, the engine does an
in-place reload, and our code runs with the **presets already loaded and the
classes not yet built**. F87 shipped in that gap. This leg closes it.

**It needs a human for exactly one click, and nothing else.** The enable itself
cannot be scripted: `AccountStorage`, `SaveAccountStorage` and `ModsReloadItems`
are all in `ModEnvBlacklist` (`Mod.lua:1270/:1279/:1392`), and there is no
console at the main menu — so no mod-side or console-side path exists.

1. In the Mod Manager, leave the **fix pack DISABLED** and the **Test Kit
   ENABLED**. (The leg aborts with a log line if the pack is already on — that
   would just be a cold boot wearing this leg's name.)
   ⚠️ **EVERY run needs this step, including the second one in a row.** The
   click in step 4 **persists**: `ModsUIDialogEnd` calls `SaveAccountStorage()`
   (`ModManager.lua:132`), so the pack is enabled in account state from then on.
   Learned by tripping the guard, 2026-07-31 19.19. **Disable it and quit the
   game fully** — do not untick and re-tick inside one process, which is a third
   load order (the pack's code has already been in that process once).
2. Arm it: uncomment `"Code/98_EnablePathLeg.lua"` in the TestKit metadata
   `code` list. Do **not** arm `96_AutoRunFlag.lua` as well.
3. Launch as usual (`-smrautorun` is carried by habit and is ignored — the leg
   stands the normal autorun down so it cannot start a colony pack-less).
4. At the main menu: **Mods → tick "Community Fix Pack" → close the dialog.**
5. Walk away. The harness sees `ModsReloaded`, builds a colony, runs the whole
   probe suite and quits, exactly like an unattended leg.
6. Disarm by re-commenting the line.

**Reading it:** expect the same totals as the equivalent cold-boot leg for the
same toggle state — so read the `fix pack present: N/74 fixes active` line
first, as always; the opt-in toggles are account state and this leg does not
touch them. The suite is a real detector for this defect class: `FixMissing`
FAILs any probe whose fix is not `active` (catching an `apply()` that threw) and
the data-patch probes read live preset data (catching a patch that silently
never ran) — the two F87 symptoms.

**✅ EXECUTED ONCE, 2026-07-31 19.09 — the procedure above is verified, not
merely written** (the standing rule: a test's own procedure is unverified until
it has been run). It produced `68/74` → `63/0/15/0`, probe-for-probe identical to
the cold boot bar two RNG lines. Two log lines are the leg's own positive
control and you should look for both: `ENABLE-PATH: ARMED — the pack is OFF`
before the click and `ENABLE DETECTED — the pack loaded through an in-place mod
reload` after it. `95_AutoRun` logs `standing down` at boot.

⚠️ **A toggles-OFF run leaves the optional modules uncovered.** All five `Opt_`
probes SKIP. To exercise them on this path, do NOT ask the owner to flip
toggles — drop a temporary `Code/97_OptInLeg.lua` into the FIX PACK right after
`00_Core` setting `SMRFixPack_Optional`, which overrides an OFF toggle
(`OptionEnabled`, `00_Core.lua:51-55`, checks the bridge first) and leaves
account state alone. Delete the file and its metadata line after the leg.
*(This does NOT bear on audit A2, which PT-55 answered in play 2026-07-30 — a
different path, the module toggle rather than the pack.)*

---

## Save fixtures — create these once, reuse them

Make each one, then **save under the given name**. Every open test below names its
fixture. Keep a pristine copy of each (save-as with a `-base` suffix) so a
destructive test doesn't cost you the setup. (SAVE-C, the two-dome fixture, has
served its tests — PT-12/13/14 are archived — and is no longer needed.)

| Fixture | How to build it | Feeds |
|---|---|---|
| **SAVE-A — Sandbox colony** | New game, any sponsor, **default game rules** (disasters ON, meteors at least "Low"), Mars surface. Land, build one dome with ~20 colonists, a Medical Center, a Martian Express station with a short track, and a landed rocket. `MultiCheat()` + `CheatAddFunding(500000000)` to remove build gating. For PT-27/PT-28 the save also needs the **Dust In The Wind** game rule (set at new-game). | PT-10, PT-27, PT-28 |
| ~~**SAVE-B — No-Disasters underground**~~ **RETIRED 2026-07-30** | Both consumers are done: PT-11 archived 2026-07-29 (its buildings turned out not to be needed at all), and **PT-25 never needed the underground in the first place** — its setup line was mis-specified and corrected at the keyboard: tunnels are a **surface** building and the underground build menu has none. Do not build this fixture. | — |
| **SAVE-D — St. Elmo's Fire mystery** | Easiest: start a **new game and pick "The Power of Three / St. Elmo's Fire" (`LightsMystery`) as the mystery at setup**, then play/skip forward until Light Traps are buildable and have caught wisps. (Console alternative in PT-15.) | PT-15 |
| **SAVE-E — Frontier save (underground elevator + asteroid)** | From a healthy mid-game colony: `UIColony:UnlockUnderground()`, `CheatRevealDarkness()`, build an **Elevator** and an **underground dome with free housing**; then `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` and build/land an **Asteroid Lander** with a **MicroG Habitat** and a couple of colonists on the asteroid. `dbg_ToggleRocketInstantTravel()` when running lander tests. | PT-18 |
| **SAVE-F — Uninstall-safety copy** | Just a save made *while the fix pack is enabled* — copy of SAVE-A after ~1 sol of play is fine. | PT-20 |
| *(Mirror Sphere save)* | A game running the **Mirror Sphere** mystery, picked at new-game setup. | PT-30 |
| *(Live colony)* | The long-running real colony — the standing watches, the wave-6 disaster tests and the module partials all run there. | PT-52, PT-53, PT-54, PT-42, PT-44, PT-46 tail, PT-47, PT-48, PT-35, PT-37 |

Rough effort: SAVE-A ~20 min, SAVE-D ~20, SAVE-E ~30 (SAVE-B is retired). SAVE-E is
the expensive one; do all its remaining work (PT-18) in one sitting.

---

## Commands cited in the archived TESTING.md that could NOT be verified — do not use

| Cited as | Verdict |
|---|---|
| **`hr.TimeScale`** (archived TESTING.md, F02 scenario: "set game speed high (cheat/`hr.TimeScale` — verify name)") | ❌ **UNVERIFIED / does not exist.** No `hr.TimeScale` anywhere in `ModTools\Src`. Use the verified `SetGameSpeedState("ultra")` (`Lua/X/HUD.lua:528`) or `UIColony:SetGameSpeed(20)` (`Lua/Colony.lua:564`) instead. |
| **Cheat keyboard shortcuts** (Alt-B for complete-all-constructions, Alt-Shift-A for asteroid unlock, etc., as listed in the archived CHEATS_INVENTORY.md) | ⚠️ **Real in source but NOT bound on retail** — the whole shortcut tree is behind `local cond = Platform.cheats` (`Lua/XDef/GameCheatShortcuts.generated.lua:19-20`). Type the function call in the console instead. Every command in the reference table above is a verified callable function. |
| **`CheatStartMystery(id)`** | ⚠️ **Real (`Lua/Mysteries/Mysteries.lua:91`) but self-gated** on `Platform.cheats` (`Lua/Cheats.lua:1-3`). Use the new-game mystery pick, or the explicit `Platform.cheats` flip documented in PT-15. |
| **"Fast-forward game time by an interval"** | ❌ No such cheat exists (confirmed in the archived CHEATS_INVENTORY.md "Not found — do not look again"). Use `SetGameSpeedState("ultra")` and wait. |

Everything else prescribed in this document was verified to exist in
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` at the file:line cited.
