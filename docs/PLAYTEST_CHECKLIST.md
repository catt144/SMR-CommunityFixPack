# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

**Completed tests live in [PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md)** — done so far
(35 sections): PT-01 … PT-09, PT-11 … PT-14, PT-16, PT-17, PT-19, PT-23, PT-24,
PT-26, PT-29, PT-31 … PT-34, PT-36, PT-38 … PT-41, PT-43, PT-45, PT-46 (the
F49(b) half), PT-49, PT-50, PT-51. This file carries **only un-run work**; when a test
completes, its whole section (with the result notes) moves to the archive.
(Cross-checked against the archive and the BUGS.md index 2026-07-29 — nothing
below re-tests anything already passed; PT-46's remaining halves are exactly
the two the archived run left "not separately exercised".)

## What a pass here means

The automated A/B probe runs (docs/archive/SESSION_LOG.md) prove the *wiring* across all waves:
patched functions install and return the right values under synthetic input.
This checklist is the **human-eyes half** — the things probes cannot see:

- how it *feels* in real play (cadence, pacing, does the colony actually recover),
- **visuals** (does the trimmed track leave a sane-looking remainder?),
- **UI** (does the number actually render in the panel?),
- **long-running behavior** (does it still hold after 3 sols, after a save/load?),
- emergent multi-system interactions the probes stub out.

**A pass here is what earns a fix `tested` status in BUGS.md.** Probe-verified ≠
tested. Nothing ships as "verified" on probe evidence alone. If a sitting starts
oddly, `SMRTest.RunAll` is the quick regression sanity check (expect the same
PASS/SKIP pattern as the last A/B leg; `[install]` probes SKIP on retail).

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
| `CheatMeteors("single"\|"multispawn"\|"storm", setting, pos)` | `Lua/Cheats.lua:62` | meteor strike. ⚠️ **RE-CORRECTED 2026-07-29 (QA session):** with no explicit `pos` it can silently do NOTHING — but the mechanism recorded earlier was wrong. `GetCameraLookAtPassable` is a **file-local helper** (`local function`, `Cheats.lua:42`) — invisible from the console *by design*, which is what the `attempt to call a nil value` probe actually proved; the shipped `Cheats.lua` is byte-identical to Src (full fpk diff, see ENGINE_FACTS.md). The real no-op path: the helper returns nil when no passable point exists within 100m of the camera look-at, and the body is `if pos then … end` with no else. **Always pass a position**, or drive the disaster directly: `*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`. Note `"storm"` reliably WEDGES (F78) — with the pack loaded, `Fix_MeteorStormWedge` heals it automatically ~2 game hours after the storm notification expires (PT-54); manual recovery remains `*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end` |
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
| `SMRFixPack.ListFixes` | per-fix status — all **68 default fixes** should read `active` (opt-in modules read `inactive` unless toggled ON; `Code/00_Core.lua`) |

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

## Save fixtures — create these once, reuse them

Make each one, then **save under the given name**. Every open test below names its
fixture. Keep a pristine copy of each (save-as with a `-base` suffix) so a
destructive test doesn't cost you the setup. (SAVE-C, the two-dome fixture, has
served its tests — PT-12/13/14 are archived — and is no longer needed.)

| Fixture | How to build it | Feeds |
|---|---|---|
| **SAVE-A — Sandbox colony** | New game, any sponsor, **default game rules** (disasters ON, meteors at least "Low"), Mars surface. Land, build one dome with ~20 colonists, a Medical Center, a Martian Express station with a short track, and a landed rocket. `MultiCheat()` + `CheatAddFunding(500000000)` to remove build gating. For PT-27/PT-28 the save also needs the **Dust In The Wind** game rule (set at new-game). | PT-10, PT-27, PT-28 |
| **SAVE-B — No-Disasters underground** | New game, tick the **No Disasters** game rule at setup (it cannot be added later). Then in-colony: `UIColony:UnlockUnderground()` and `CheatRevealDarkness()`, build a small underground presence. (PT-11 is done and archived — buildings turned out not to be needed for it at all.) | PT-25 |
| **SAVE-D — St. Elmo's Fire mystery** | Easiest: start a **new game and pick "The Power of Three / St. Elmo's Fire" (`LightsMystery`) as the mystery at setup**, then play/skip forward until Light Traps are buildable and have caught wisps. (Console alternative in PT-15.) | PT-15 |
| **SAVE-E — Frontier save (underground elevator + asteroid)** | From a healthy mid-game colony: `UIColony:UnlockUnderground()`, `CheatRevealDarkness()`, build an **Elevator** and an **underground dome with free housing**; then `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` and build/land an **Asteroid Lander** with a **MicroG Habitat** and a couple of colonists on the asteroid. `dbg_ToggleRocketInstantTravel()` when running lander tests. | PT-18 |
| **SAVE-F — Uninstall-safety copy** | Just a save made *while the fix pack is enabled* — copy of SAVE-A after ~1 sol of play is fine. | PT-20 |
| *(Mirror Sphere save)* | A game running the **Mirror Sphere** mystery, picked at new-game setup. | PT-30 |
| *(Live colony)* | The long-running real colony — the standing watches, the wave-6 disaster tests and the module partials all run there. | PT-52, PT-53, PT-54, PT-42, PT-44, PT-46 tail, PT-47, PT-48, PT-35, PT-37 |

Rough effort: SAVE-A ~20 min, SAVE-B ~15, SAVE-D ~20, SAVE-E ~30. SAVE-E is
the expensive one; do all its remaining work (PT-18) in one sitting.

---

# 1 · Standing watches — every sitting, alongside whatever else you play

## PT-22 — Log hygiene (after EVERY session, including every test below)

**Where:** `%AppData%\Surviving Mars Relaunched\logs` — take the newest
`Mars.exe-<date>-<time>.log`.

**Check for:**
1. Any line containing **`[CommunityFixPack]`** with the word `error`, `inactive`, or a
   deactivation reason. (Startup lines reporting fixes as `applied` are normal;
   the opt-in modules reporting `inactive (…opt-in…)` is normal unless you
   enabled them.)
2. Any **`[LUA ERROR]`** block whose stack mentions a file under `SMR-BugFixPack\Code\`.
3. Any `[LUA ERROR]` in shipped game code that you did **not** see in a vanilla session
   — note the file:line even if it looks unrelated to us.
4. `SMRFixPack.ListFixes` output at load: **all 68 default fixes should read
   `active`** (plus whichever opt-in modules you have toggled ON). Any other
   `inactive`/`error` line means a fix silently self-deactivated (its apply()
   self-check failed) — that is a FAIL and needs reporting with the reason string.

Paste anything suspicious verbatim into your result line — the exact text matters more
than a summary.

`Result:` _____________________________________________

## Meteor watchdog (F02) — passive, no action needed

PT-01 passed and is archived, but its silence-watch continues in the background:
the watchdog self-reports (`WATCHDOG — Meteors thread silent …`) if the meteor
wedge ever recurs. **If you see that line in the log, report it verbatim.**

## PT-52 Trigger A — drone overhaul passive watch (whenever D06 is enabled)

Runs in the background of any sitting with the module ON — full procedure and
result lines live in the PT-52 section (§2 below). Short form: watch who
answers wrench icons near idle drones; `SMRFixPack.DroneReport` every ~30 min;
healthy = `vetoed` climbing, `veto_expired` low, `unclaimed` not building up.

---

# 2 · In progress — owed halves of partially-passed tests

## PT-55 — Opt-module live-toggle re-verify · covers **audit fix 1.3 (2026-07-29)**

The audit rework moved ClassicRockets' fuel wrap, ResidencyControl's dome
gate and MultipleSuns' panel-binding wrap to file-scope installs, so a FIRST
mid-session Mod Options enable now works without a relaunch (previously
silently dead until restart). One sitting, any healthy save, per module:

> ⚠️ **Setup state (CORRECTED 2026-07-29 latest): all six toggles are ON
> again** — re-enabled during the day's play session (the post-D09 A/B leg
> read 75/75 active, only possible with all six on). Toggles are
> account-persistent, so this test's required starting state is NOT set:
> **turn all six OFF and relaunch before step 1.** (The two D09 dials are
> separate, default to base, and don't affect this test.)

1. Start the session with the module **OFF**. Mid-session, toggle it **ON**
   (no relaunch) and confirm the behavior engages: ClassicRockets — a parked,
   destination-less player rocket starts requesting launch fuel;
   ResidencyControl — a closed dome stops voluntary move-ins (the infopanel
   row appears on the next panel open); MultipleSuns — a NEW panel built
   beside sun #2 binds to it (the limit lift itself was already live-safe).
2. Toggle **OFF** again: behavior reverts immediately (vanilla answers).
3. `SMRFixPack.ListFixes()` agrees with the toggle at each step; log clean
   (PT-22 rules).

PASS flips nothing on its own (the modules keep their D-entry gates) — it
retires the audit's A2 "live confirmation still worthwhile" caveat; record
the result on the D01/D03/D04 entries.

`Result:` _____________________________________________

## PT-56 — Drone stat dials · covers **D09 `Opt_DroneStatDials`** (built 2026-07-29)

Two Mod Options dropdowns: **Drone speed** (1x base / 2x / 3x / 5x, percent
added on BASE, additive with speed techs) and **Drone carry capacity**
(+0 base / +1 / +2 on `g_Consts.DroneResourceCarryAmount`). One sitting,
any healthy save with at least one drone (~5 min):

1. **Baseline reads:** select a drone —
   `SelectedObj:GetMoveSpeed()` and `g_Consts.DroneResourceCarryAmount`
   (with both speed techs expect 2304 = 1440 × 1.6; carry 2 with Artificial
   Muscles).
2. **Set speed 2x + carry +1 → Apply** (no relaunch): same reads — speed
   gains +1440 (100% of base, additive: 2304 → 3744 on the techs save),
   carry +1; drones visibly faster; log clean (PT-22 rules).
3. **Back to base → Apply:** both reads return to the step-1 numbers —
   live removal, no residue (`SMRFixPack.ListFixes()` still shows
   `DroneStatDials [active]` — active-at-base is the armed state, by design).
4. **Stale-save reconcile:** save with dials ON, set dials to base, reload
   that save → reads are the step-1 numbers (the persisted modifiers were
   removed on load).

PASS flips D09 to `tested` (both BUGS.md places). (The C-side clamp probe
originally queued here was run ahead of the build, 2026-07-29 live: no clamp —
`SetMoveSpeed(10000)` read back exactly — and movement stayed clean at 10000
on ultra. Recorded on the D09 entry; no need to repeat it.)

`Result:` _____________________________________________

## PT-53 — Cohort housing · covers **D07 `Opt_CohortHousing`** (built 2026-07-28)

Colonist/housing-level rule, NO dome designation: a Senior or Child living in
normal housing moves into a free Retirement Home / Nursery slot — own dome
first, any reachable dome second — and is left completely alone when no slot
exists. The moves ride the shipped machinery (residence reassignment +
emigration), so everything observable is ordinary game behavior.

**Progress (2026-07-29, first live enable — user verdict: "it worked
wonderfully").** Triggers **B, C and D PASS** (cross-dome moves over trains/
passages/shuttles chosen by distance; organic no-churn where no slots existed;
graduation drain with the designed transient-homeless blip). Full record on the
D07 entry. **Only A and E remain:**

**Trigger A — in-dome move + employed exemption:** find (or spawn) an
unemployed Senior housed in a normal residence in a dome that also has a free
Retirement Home slot.
- **EXPECTED:** within a heavy update they re-home to the Retirement Home
  (watch the Residence line of their infopanel). An EMPLOYED Senior in the
  same dome does NOT move.

**Trigger E — precedence + uninstall shape:** manually assign a Senior to a
normal residence (player order) — they must STAY. Toggle the module off —
everything is instantly vanilla; save with it ON, reload with it OFF —
clean load, no errors (zero persisted state).

Reference (already-passed scope, for context only — do not re-run): the module
never touches Tourists or employed Seniors; player orders, quarantine and the
D03 closed policy always win; arrival housing at the destination may take one
heavy update to slot into the cohort building (transient, by design).

`Result (A in-dome move + employed exemption):` _____________________________________________

`Result (E precedence + uninstall):` _____________________________________________

---

## PT-52 — Drone dispatch overhaul · covers **D06 `Opt_DroneOverhaul` core v1 + F77 `Fix_ExtenderFlapChurn`** (built 2026-07-28)

**This is NOT a 15-minute test.** It is a watch-and-judge item that runs in the
background of the WHOLE session (and future sessions) while other PT items are
played, plus one controlled A/B demonstration. Expect multiple iterations —
tuning knobs live at the top of `Code/Opt_DroneOverhaul.lua` (changes need a
relaunch); record every knob change and its observed effect on the D06 entry.

**What the module CAN do (judge it on these):**
- Repair and cleaning jobs in OVERLAPPING hub coverage go to the CLOSEST hub's
  fleet first; a far fleet only serves if the near one doesn't respond within
  a few of its polls (~10-15s worst case, by the strike cap).
- Idle drones help a NEIGHBORING hub that is saturated (zero idle drones of
  its own) with repair/clean jobs within 30 hexes of the drone.
- `SMRFixPack.DroneReport()` (console, works even with the toggle OFF): per-hub
  working/drones/idle/broken, lap load class, per-priority queue depths, work +
  unclaimed counts, extender chains, and the module counters
  `vetoed / veto_expired / moonlighted`.
- F77 (default-on fix, separate from the toggle): an extender power flicker /
  malfunction / repair no longer tears down and rebuilds the whole uplink
  hub's registration twice — one coalesced rebuild ~2s later instead. Fleet
  drones no longer ALL kick to Idle on every extender blip.

**What it CANNOT do (do not judge it on these — all deliberate v1 scope):**
- Resource HAULING (PickUp/Deliver, incl. the maintenance "fetch Electronics
  from a depot" leg) is untouched — a far drone can still win a delivery.
  If the delivery leg dominates the pain, that is the H-v2/B iteration
  (docs/DRONE_OVERHAUL_OPTIONS.md), not a bug in this one.
- Construction work is untouched (multi-fleet swarming on a site is wanted).
- RC rover fleets, rockets, shuttles: untouched by design.
- It does not MOVE drones between hubs (that is option C, the migration
  balancer) — a chronically under-drone'd hub still needs the player (or a
  future iteration) to rebalance; the module only redirects CLAIMS and lets
  idle neighbors help nearby.
- It cannot override or delay a PLAYER-ordered drone command (structurally —
  the claim gate sits on FindTask, which only the auto-Idle path calls).
- Toggling it OFF restores vanilla behavior instantly and completely
  (registration untouched, no persisted state; saves made with it ON load
  identically without it).

**Setup:** a colony with ≥2 Drone Hubs with overlapping coverage (the user's
live colony is ideal — it has the original symptom), extenders present, work
happening. Enable **Options → Mod Options → "Drone dispatch overhaul
(experimental)"**. `SMRFixPack.ListFixes` must show `DroneOverhaul [active]`
and `ExtenderFlapChurn [active]`. Run `SMRFixPack.DroneReport` once as the
session baseline (counters start at 0).

**Trigger A — passive watch (all session, while playing other PT items):**
1. Whenever a wrench/malfunction icon appears near parked idle drones, watch
   who answers. **EXPECTED:** the nearby fleet claims within seconds. Vanilla
   (the 2026-07-27 screenshots) was: near drones stay Idle, far fleet crawls
   over.
2. `SMRFixPack.DroneReport` at every suspicious moment and every ~30 min.
   **HEALTHY:** `vetoed` climbing while `veto_expired` stays LOW relative to
   it (near fleets actually take the yielded work); `moonlighted` > 0 if any
   hub saturates; `unclaimed` per hub not building up.
   **UNHEALTHY:** `veto_expired` ≈ `vetoed` (strike window too short or near
   fleets can't respond — raise STRIKES_MAX/STRIKE_TTL or investigate why the
   near fleet is dead); any hub's `unclaimed` growing over consecutive
   reports (possible starvation — capture DroneReport + the R1/R2 reads from
   the BUGS DroneControl bullet on the starving building IMMEDIATELY, then
   toggle the module off and watch whether vanilla clears it).
3. **BROKEN looks like:** wrench icons lingering LONGER than vanilla; drones
   ping-ponging between two jobs or two hubs; a far fleet fully idle while
   visible work exists beyond the near fleet's capacity; any log error
   mentioning `FindTask`, `Idle`, `UpdateUplinkRequesters`, or
   `[CommunityFixPack]`.

**Trigger B — controlled A/B demonstration (10 min, once per iteration) — UN-RUN:**
1. Pick (or build) hub A and hub B far apart, with an extender bridging B's
   coverage into A's yard. Both hubs need idle drones.
2. Toggle the module OFF. `Platform.cheats = true`, select a building in A's
   yard, `SelectedObj:CheatMalfunction()`. Watch which fleet answers and how
   long the wrench lasts. (This reproduces the vanilla far-capture when the
   race falls that way — it may take a few tries; the R6 claim tap from the
   BUGS bullet prints the claiming drone's hub if eyes aren't enough.)
3. Repair, toggle the module ON, repeat on the same building.
   **EXPECTED:** A's fleet answers every time; `vetoed` ticks up if B's fleet
   polled first and was held.
4. Extender flap check (F77): toggle the extender off and on (or let a dust
   storm brown it out). **EXPECTED:** B's drones do NOT all flash to Idle;
   coverage through the extender resumes within ~2-3s of the flap settling.
   **BROKEN looks like:** fleet-wide Idle flash on each flap edge (the fix
   isn't engaging) or extender coverage permanently lost after a flap
   (debounce dropped a rebuild — capture the log).

**Trigger B2 — the MEASURED stress A/B (the real verdict; ~30 min per pair) —
RE-RUN OWED with the v2 harness.**
Supersedes Trigger B's eyeball demo. Uses `SMRTest.Stress` (Test Kit helpers
section above — **v2 lifecycle tracing, rebuilt 2026-07-29**). Run at
**normal to 3× speed, not ultra**: timings are measured in game time so speed
does not change the numbers, but ultra stresses the sim and adds artifacts.

1. Confirm the harness loaded — `SMRTest.Stress ~= nil` must print `true`.
2. Clean the colony so both legs start identical (clears any pre-existing
   malfunctions that would skew the target pool and add background repair
   traffic): `SMRTest.Stress.HealAll()`
3. **QUICKSAVE.** This one save is the anchor for BOTH legs.
4. Dry run — see the target set without breaking anything:
   `SMRTest.Stress.Targets{scope = "overlap", n = 25}`
   If it reports far fewer than 25 eligible, widen the scope (`hub`, `radius`,
   `all`) and note which you used. **Also check the pure cohort:**
   `SMRTest.Stress.Targets{scope = "overlap", n = 25, pure_only = true}` —
   no-resource targets skip the haul leg and the deliverer handoff entirely,
   so they are the purest gate signal; if there are ≥10, run a pure pair too.
5. Toggle D06 **OFF** (Options → Mod Options). Verify:
   `SMRFixPack.fixes.DroneOverhaul.status` → must read `inactive`.
6. **LEG A:** `SMRTest.Stress.Break{scope = "overlap", n = 25, seed = 1}`
   Let it run to `RUN ENDED` — it prints its own summary. `HealAll()` aborts.
7. **Reload the quicksave** — identical colony state, identical target set.
8. Toggle D06 **ON**. Verify `SMRFixPack.fixes.DroneOverhaul.status` → `active`.
9. **LEG B:** the *exact same call* as step 6 — same scope, same n, same seed.
10. `SMRTest.Stress.Compare()` — both runs + deltas, with conditions headers.
11. `FlushLogFile()` and keep the log: the per-building trail is the evidence.
12. **One pair is not a verdict at n=25** — repeat with `seed = 2` and
    `seed = 3` before believing any delta; the harness keeps 6 runs
    (`Compare{a=, b=}` to pair them up).

**STAT-DIAL legs (drone overhaul ships with Mod Options stat dials):** same
protocol, but the ONE variable flipped between legs is a single dial (e.g.
speed 1.0x vs 1.5x, module state identical). Stamp each leg:
`Break{scope="overlap", n=25, seed=1, label="speed1.5x"}`. The conditions
header live-reads drone move_speed/carry, so the dial's actual effect is
recorded with the numbers; `Compare()` flags condition mismatches itself.

**Read the result on the `GATE-DECIDED first claims` line** — closest-hub
share over FindTask-decided claims is the only number that scores what the
claim gate claims to do. The lifecycle deltas (`haul queue` vs `haul exec` vs
`claim wait` vs `travel`) are what settle the D06/D08 structural question:
queue-latency dominance points at dispatch/priority logic, travel dominance at
stat/depot levers. Do NOT read total clearance time as a D06 score.
A reload-based protocol does **not** re-poison a save with a stranded disaster
flag — tested 2026-07-29, F81 — so no cleanup is owed afterwards.

`Result (B2 stress A/B — closest-hub % off vs on):` **FIRST RUN 2026-07-29 — NULL RESULT for the claim gate (v1 harness).** 32% (8/25) off vs 40% (10/25) on = +2 buildings, inside noise at n=25. The leg the gate actually arbitrates (work→first claim) moved 58m → 57m, and `vetoed` was +1 for the WHOLE leg — the module intervened once across 25 simultaneous malfunctions. The 34m total-time gain sits in the hauling leg, which D06 exempts by design, so it is variance not treatment. **Why: `no-resource subset: 0 of 25` — every target needed a maintenance resource, so `MaintenanceDroneUnload` → `StartWorkPhase(drone)` gave the first repair tick to the DELIVERING drone every time, bypassing `FindTask`. The metric measured which hub delivered, not which won a claim.** Full analysis + caveats on the D06 entry. Both legs normal speed, storages equalised, log kept. *SUPERSEDED NOTE (2026-07-29, harness repair session): the numbers stand as recorded, but two Src facts on the D06 entry change their reading — `SetCommandKeepQueue` preempts immediately, so the ~57m work→claim CANNOT have been the deliverer handoff; and shuttle deliveries MISFIRE the handoff (no `CargoShuttle:Work`), so shuttle-hauled repairs DID go through FindTask. A B2 re-run with the v2 lifecycle harness is owed; record its result on the line below.*

`Result (B2 re-run, v2 harness — closest-hub % off vs on):` _____________________________________________

**Trigger C — regression watch (shared machinery; spread across the session):**
- Rockets: drones still load/unload landed rockets normally (F50 territory —
  rockets are class-exempt from the claim gate, verify by watching one cargo
  cycle).
- Rovers: an RC Commander's drones behave vanilla (exempt).
- Construction: multiple fleets still swarm a construction site (work type
  exempt).
- A dome with in-dome maintenance: repairs still happen (dome-inherited
  registrations defer to vanilla in the closest-hub computation).
- PT-20-style uninstall shape at session end: save with the toggle ON, flip
  it OFF (or disable the pack), reload — everything vanilla, no errors.

**Progress (2026-07-28, first sitting):** module enabled LATE in the session
via Mod Options — **the first-ever live enable of D06, bridge VERIFIED**
(`SMRFixPack.fixes.DroneOverhaul.status` → `active` right after the toggle;
boot log correctly showed `inactive` from before the flip). First DroneReport
(6 hubs, screenshot on file): `unclaimed=0` on every hub, counters
`vetoed=4 / veto_expired=0 / moonlighted=0` — the healthy signature (all four
vetoed claims picked up by the near fleet inside the strike window);
`moonlighted=0` consistent with the one saturated hub (1078: 24 drones,
0 idle) having no unclaimed work for neighbors to take.
**Second reading (same sitting, ~end of the lander leg):** `vetoed=10 /
veto_expired=1 / moonlighted=0` — vetoed climbing with expiries staying low
(9 of 10 yielded claims taken by the near fleet inside the strike window =
the healthy signature holding); `unclaimed=0` on all six hubs throughout;
hub 1078 recovered from saturated to 7 idle. No starvation indicators all
sitting.
**Sitting 2 (2026-07-28 evening): healthy again.** Readings `vetoed 1→9 /
veto_expired 0→1 / moonlighted 0`, `unclaimed=0` on all SEVEN hubs (new hub
4230 integrated cleanly); counters correctly survived a save reload
(process memory) and correctly reset on the mid-session relaunch. Full
session log swept clean. **Trigger B still un-run.**
**Sitting 3 (2026-07-29): healthy under a real stress event.** DroneReport
taken deliberately right after a **marsquake damaged several buildings** —
the closest thing to an unplanned mass-repair test so far. **NINE hubs**
(1078, 1457, 2074, 2608, 3564, 4230, 4967, 6619, 4078 — three more than
sitting 2, all integrated cleanly), `unclaimed=0` on EVERY hub with work
counts up to 120, every lap class `low`, counters
`vetoed=3 / veto_expired=0 / moonlighted=0`. Reads as the healthy signature
under load: all three yielded claims taken by the near fleet inside the
strike window, zero expiries, and `moonlighted=0` is CORRECT here rather
than suspicious — moonlighting only fires for a neighbour hub with ZERO
idle drones, and every hub in this report has idle drones (lowest 4/6).

`Result (near fleet claims near work?):` _____________________________________________

`Result (counters healthy? vetoed/expired/moonlighted):` _____________________________________________

`Result (A/B demo, which fleet answered off vs on?):` _____________________________________________

`Result (F77 flap: no fleet Idle-flash?):` _____________________________________________

`Result (regressions: rockets/rovers/construction clean?):` _____________________________________________

`Knob changes made + effect:` _____________________________________________

---

## PT-46 tail — train cap + instant-track palette · covers **F49(d), F49(a)**

The main half — splitting a track under a running train, F49(b) — PASSed
2026-07-25/26 and is archived (resolved as no-defect: the engine stores the
train back as a prefab). The archived run explicitly left these two small
checks "not separately exercised":

**Steps:**
1. `print(MainCity.labels.TrackBase[1].max_vehicles)` on a track before and after
   you salvage most of it away. **EXPECTED:** the number drops (1 for a track under
   30 hexes, 0 for an empty one). Confirm you can still assign trains up to that
   number and no further.
2. Look at any track placed instantly by the map (not built by drones): it should be
   the same colour as track you built yourself, not pipe-coloured.

`Result (d — cap follows length):` _____________________________________________

`Result (a — instant track colour):` _____________________________________________

---

# 3 · Wave-6 disaster fixes (built 2026-07-29 post-QA) — live colony

## PT-54 — Disaster prediction leak, storm wedge, rains deadlock · covers **F78 `Fix_MeteorStormWedge`, F81 `Fix_DisasterPredictionLeak` + `Fix_RainsDeadlock`**

These three ship together and share machinery, so one PT covers them. The
wave-6 probes (`SMRTest.DisasterPredictionLeak()`, `SMRTest.MeteorStormWedge()`,
`SMRTest.RainsDeadlock()` — the rains one needs a loaded colony) assert the
mechanisms; this PT is the live half. The flag dump used throughout:
`*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`
(an empty print = no flags set).

**Setup:** the live 194-sol save (or any save with meteor storms enabled).
`SMRFixPack.ListFixes` must show `DisasterPredictionLeak`, `MeteorStormWedge`
and `RainsDeadlock` all `active`.

**Trigger A — reconciliation heals a stranded flag.** Hand-plant one
(`g_DisastersPredicted["DisasterMeteorStorm"] = true`, nothing on screen),
quicksave, reload.
   - **EXPECTED:** a `DisasterPredictionLeak: cleared stranded prediction flag`
     log line on load; the flag dump is clean.
   - **SURPRISE looks like:** the flag survives the reload (sweep did not run —
     check fix status first).

**Trigger B — a genuine warning is NEVER cleared.** Wait for (or reach) any
disaster warning countdown (toxic rain works — 3-sol window with 6 towers),
quicksave mid-countdown, reload.
   - **EXPECTED:** the notification is still on screen still counting AND its
     flag still reads `true` in the dump. The sweep must keep it.
   - **SURPRISE looks like:** flag cleared while the countdown is visible —
     that is a FAIL of the sweep's liveness test; report immediately.

**Trigger C — the wedge heals itself.** Drive a storm:
`*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`
Let it run to its wedge (validate-style stall after the last strikes; the
duration notification eventually expires). While the storm is HEALTHY
(notification visible), `SMRFixPack.StormWedgeCheck` must read
`storm notification live (healthy)` — the watchdog must never touch a live
storm. After the notification expires with the wedge in place:
   - **EXPECTED:** within ~2 game hours, `MeteorStormWedge: WEDGE confirmed …
     healing`, then either `released through the vanilla end path` (plus
     Fix_DisasterPredictionLeak's `storm ended` line) or `forced storm state
     clean`; the flag dump is clean afterwards; `g_MeteorStorm` reads false.
   - **SURPRISE looks like:** `StormWedgeCheck` stuck on `signature armed`
     forever, repeated heals (`restarts` climbing to give-up), or a healthy
     storm getting cut short.

**Trigger D — storms keep scheduling after a heal.** After Trigger C, confirm
the scheduler is alive: `IsValidThread(MeteorStorm)` reads true, and over a
long soak a NATURAL storm warning eventually appears (the pre-fix failure mode
was: never again).

**Trigger E — rains survive collisions.** On load expect
`RainsDeadlock: … rain loop moved onto the bounded body` lines IF the save had
live rain loops (zero lines is normal when the bands had no loops — e.g. after
the manual 2026-07-29 recovery). Over the soak: rain must occur again within a
few sols of a rain roll colliding with a warning window (pre-fix: that rain
type died permanently). Cheap forced check: while any warning countdown is up,
rains rolling during it must NOT kill later rains — watch for normal/toxic rain
in the sols after the warning resolves.

Log hygiene: no `[LUA ERROR]` mentioning `DisasterPredictionLeak`,
`MeteorStormWedge`, `RainsDeadlock`, `RainsDisasterLoop` or `StormWedgeHeal`.

`Result (A reconcile / B warning kept):` _____________________________________________

`Result (C heal / D reschedule / E rains):` _____________________________________________

---

# 4 · Fixture sittings — batch these by save

## SAVE-A sitting (sandbox; PT-27/28 need the Dust In The Wind rule)

### PT-10 — Open-roof drone observation · covers **F55** ❓ **OPEN QUESTION**

**This test has no expected answer.** The Lua half of F55 (the unreachable-forever
approach cache) is fixed and probe-verified. The *other* half — whether opening a
dome's roof destroys the dome-entrance attaches that carry the only drone pathfinding
tunnels into the dome — is **engine entity data we cannot read from Lua**
(`Lua/Buildings/Dome.lua:404`; see the F55 entry in BUGS.md). **Either answer is
useful data.** Record what you actually see.

**Setup:** SAVE-A, one dome with **interior buildings that need maintenance** and a
drone hub with drones parked outside the dome.

**Trigger:**
```
CheatOpenAllDomes()
```
(this also maxes terraforming and activates the Open Domes policy — the prerequisites;
`Lua/Cheats.lua:414-424`). Then let 1–2 sols pass at ultra speed and watch drones.

**Observe and write down:**
1. Do drones **physically enter** the open dome to service interior buildings? (Yes / No)
2. Do interior buildings accumulate **unserviced maintenance** while drones idle outside?
3. Do drones **cluster in a clump just outside** the dome entrance?
4. Now `CloseAllDomes(MainCity)` — do drones resume entering? Does the situation recover
   on its own, or only after a save/load?

- **If drones enter and maintain normally:** the entity-data concern is unfounded → F55
  can be closed as fixed on the Lua half alone.
- **If drones stay outside forever:** we have a confirmed engine-data bug and a new
  finding to file.

`Result (1):` __________  `Result (2):` __________  `Result (3):` __________  `Result (4):` __________

`Notes:` _____________________________________________

### PT-27 — Dust Sickness does not infect Biorobots · covers **F40**

**Setup:** SAVE-A (with the **Dust In The Wind** rule). You need **Biorobots**
and a **dust storm**. Biorobots come from the **The Positronic Brain**
breakthrough — `UIColony:SetTechResearched("ThePositronicBrain")` (NOT
`CheatResearchAll()`, which skips undiscovered breakthroughs — see the command
table), then spawn a batch and check the colonist list for the **Biorobot**
trait; if you cannot get any, write "could not set up" and skip the F40 half.

**Trigger:**
1. Note which colonists are Biorobots.
2. Wait for (or wait out) a **dust storm** with the "Dust Sickness" event active.
3. When the Dust Sickness event resolves, list who caught it.

- **BROKEN looks like:** Biorobots appear in the list of the newly sick, lose Health
  in every subsequent storm, and (on the "shouldn't work" answer) are flagged unable
  to work until the cure tech lands.
- **FIXED looks like:** only organic colonists catch it. Children are still excluded
  as before.
- **Existing-save check:** load a save where Biorobots are already sick and look for
  `[CommunityFixPack] DustSicknessBiorobots: cleared Dust Sickness from N Biorobot(s)`
  in the log; those colonists should lose the trait and the "unable to work" flag.

`Result (Biorobots spared?):` _____________________________________________

### PT-28 — Dust Sickness damage spread · covers **F17**

**Setup:** SAVE-A, during an active dust storm with several colonists carrying the
**Dust Sickness** trait (see PT-27 for how to get there).

**Trigger:** pick 4-5 sick colonists, write down each one's Health, run **one sol** at
`SetGameSpeedState("ultra")`, and compare the drops. (Health also moves for other
reasons — food, medical care — so use colonists in the same dome doing the same thing,
and look at the pattern rather than exact numbers.)

- **BROKEN looks like:** every sick colonist loses **exactly the same** Health per sol
  (a flat 10) — the damage roll the code computes is discarded.
- **FIXED looks like:** the per-colonist losses **differ**, spread over 5-14.

`Result:` _____________________________________________

## SAVE-B sitting (No Disasters, underground)

### PT-25 — Destroyed tunnel after a reload · covers **F38**

**Setup:** SAVE-B (or any save with underground access — `UIColony:UnlockUnderground()`
then `CheatRevealDarkness()`). Build a **tunnel pair** across an obstacle so that the
tunnel is the *short* route between two points, and park an **RC Rover** on one side
with an errand on the other (a deposit to mine, a building to service). Watch it use
the tunnel once so you know the route.

**Trigger:**
1. Destroy the tunnel. `CheatToggleInfopanelCheats()` gives you a per-building
   **break/destroy** button in the infopanel; a meteor strike on it works too
   (`CheatMeteors("single")` with the camera on the tunnel). Confirm both ends now
   show as **destroyed ruins**.
2. Send the rover across again. It should now take the long way round (or refuse).
3. **Save, quit to menu, and load that save.** This is the step that mattered.
4. Send the rover across again and watch its path.

- **BROKEN looks like:** after the reload the rover walks straight at the ruin and
  teleports through it as if the tunnel were intact — the shortcut came back on load.
- **FIXED looks like:** the rover takes the same long route after the reload as it did
  before it. The log shows a `[CommunityFixPack] DestroyedTunnels: closed N destroyed
  tunnel(s)` line if the save already had the bad state baked in.

**Then repair it** (the ruin's Rebuild button) and confirm the tunnel **works again** —
this is the check that the fix does not lock a repaired tunnel out permanently.

`Result (still closed after reload?):` _____________________________________________

`Result (works again after repair?):` _____________________________________________

## Mystery saves

### PT-15 — Wisp power output · covers **F07** (+ **F15** bonus read)

**Setup:** SAVE-D — the **St. Elmo's Fire** mystery (`LightsMystery`) active, with
**Light Traps built and holding wisps** (`#MainCity.labels.LightTrap` > 0 and traps
with `fireflies`).

> **How to get there without third-party mods.** `CheatStartMystery` self-gates on
> `Platform.cheats` (`Lua/Cheats.lua:1-3`, `Lua/Mysteries/Mysteries.lua:91`), which is
> false on retail. Two legitimate routes, in order of preference:
> 1. **Pick the mystery at new-game setup** (recommended — this is the realistic path
>    and the one described in the SAVE-D fixture).
> 2. From the console, flip the platform flag around the call and put it back:
>    ```
>    *r Platform.cheats = true CheatStartMystery("LightsMystery") Platform.cheats = false
>    ```
>    `Platform` is **not** blacklisted, so this does work from the retail console — but
>    it is a bigger hammer than route 1. If you use it, note that in your result.

**Trigger:** with wisps in the traps, choose the **"free the wisps"** option (or from
the console `SetLightTrapMode("free")`), then read a trap's power output:
```
*r local t = MainCity.labels.LightTrap[1] ConsolePrint(tostring(#t.fireflies).." wisps -> "..tostring(t.electricity_production))
```

- **BROKEN looks like:** you free a swarm of wisps into your traps and they generate a
  laughable trickle of power — a handful of units instead of kilowatts. The reward feels
  pointless.
- **FIXED looks like:** the traps produce **~1000× more** — roughly `1000 × wisp count`
  — a real power source, matching what the mystery's text promises.

Also check `SetLightTrapMode("destroy")` on a separate trapful: the research points
granted should **match the number shown in the notification** (F15 half — record it as
a bonus observation).

`Result (power):` _____________________________________________

`Result (RP matches notification):` _____________________________________________

### PT-30 — Finished Mirror Sphere site · covers **F16**

**Setup:** a game running the **Mirror Sphere** mystery (pick it at new-game setup;
`CheatStartMystery` is gated on `Platform.cheats` — see the note under PT-15). Play or
fast-forward until you have a **scanned excavation site** with a Drone Hub in range.

**Trigger:**
1. While the site is part-way done, confirm its actions (**Pierce the Shell**,
   **Communicate**, **Feed Power**) can be started — this is the control.
2. Let the excavation run to **100%** — the sphere launches and detaches.
3. Now open the finished site's infopanel and try each action again. If you have not
   used all three, at least one should still be un-completed.

- **BROKEN looks like:** the finished site still offers and accepts actions.
  "Pierce the Shell" connects it to your drone commanders and drones start walking
  over to work an excavation that cannot progress.
- **FIXED looks like:** the finished site starts nothing. Cancelling an action that was
  already running still works.

`Result:` _____________________________________________

## SAVE-E sitting (frontier: elevator + asteroid)

### PT-18 — Arrival deaths, including the elevator / multi-map path · covers **F53**

This is the fix that was **reworked after the audit found it broken**, and the elevator
path is exactly the case that was broken. Test that path deliberately.

**Setup:** SAVE-E — an **underground dome with free housing**, reachable only via the
**Elevator**, plus a surface rocket landing pad.

**Trigger — case A (surface arrival):**
1. Bring a rocket of colonists down on the surface, some distance from any dome.
   Watch where they walk and whether any die or go "Abandoned".

**Trigger — case B (the elevator / cross-map arrival — the important one):**
2. Make the **underground dome the only one with free housing** (fill or close the
   surface domes' housing / turn their Accept Colonists off).
3. Land a rocket of new colonists on the surface.
4. Follow them: do they walk to the **Elevator**, ride it down, and reach the
   underground dome?

**Trigger — case C (nasty variant):**
5. Land a rocket where the nearest dome by straight-line distance is **not** walkable
   (across impassable terrain / a canyon) while a walkable dome exists further away.

- **BROKEN looks like:** newly arrived colonists set off toward a dome they can't
  actually reach, mill about outside, get flagged Abandoned/Confused, and die of
  suffocation — or, in the elevator case, every legitimate elevator arrival gets
  re-routed, loses its elevator assignment and is abandoned on the pad.
- **FIXED looks like:** arrivals are dropped on passable ground, elevator-destined
  colonists actually ride the elevator down and move in, and unreachable-dome arrivals
  either pick a reachable dome or wait safely near the rocket under a "Confused
  Colonists" notification and retry — **nobody dies on arrival**.

`Result (A surface):` _____________________________________________

`Result (B elevator):` _____________________________________________

`Result (C unreachable-nearest):` _____________________________________________

## Any-save items (live colony or any healthy save)

### PT-35 — Save sanitizer passes · covers **F35, F03 (sweep half)**

Both passes only act on damage that is *already* in a save, so a fresh colony
proves nothing about them beyond "they ran and broke nothing". Treat the first
two steps as the real test and the third as the only one that needs a fixture.

**Setup:** any save. The pack's passes run automatically on load; the two are also
callable by hand from the console:
`SMRFixPack.Sanitizer.RepairTurbineBuff()` and
`SMRFixPack.Sanitizer.RepairLeakedUpgradeModifiers()` — each returns how many
things it repaired.

**Trigger — case A (does no harm):**
1. Load a healthy save with at least one Large Wind Turbine and one upgraded
   Medical Center in a dome. Note the turbine's Power production and the dome's
   birth-comfort figure.
2. Run both console calls. Both should return **0** and nothing on screen should
   change.
3. Save, reload, check again — still unchanged. (Running twice must never stack a
   bonus; that is the failure this checks for.)

**Trigger — case B (F03 sweep, forced):**
4. Follow the archived PT-02 procedure to build + upgrade + salvage a Medical
   Center **with the fix pack disabled**, so a bonus really leaks. Save.
5. Re-enable the pack and load that save. The dome's birth-comfort bonus should
   drop back to its unbuffed value, and the log should carry
   `SaveSanitizer: removed N leaked upgrade modifier(s)`.

**Trigger — case C (F35, needs a fixture — skip if unavailable):**
6. A save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture. If a community save is donated, load it and
   check a Large Wind Turbine's Power production against a Shrouded one: unfixed
   the Large one is missing the +100%; fixed they match.

- ⚠️ If step 3 shows a bonus that grew on the second run, that is a FAIL and the
  pass is not idempotent — record the exact figures.

`Result (case A no-op):` _____________________________________________

`Result (case B leak cleared):` _____________________________________________

`Result (case C, or "no fixture"):` _____________________________________________

### PT-37 — F48 unblock test · decides whether the **F48** repair can ship

F48 is **not implemented** — this test is what decides whether it can be. The shipped
migration fixup (`Station.lua:1339-1355`) mis-parenthesises one call, so it re-orders
nothing; the *corrected* call runs `OrderTrackElements`, which rebuilds every element's
`connections` and `node_idx` on the track it is given, with a non-unwinding `assert` as
its only failure handling. Before that ever ships in the sanitizer, it has to be seen
behaving on a real save — both on a healthy network and on the one thing most likely to
break it: a meteor-damaged track.

**Setup:** a save with **two or more stations** connected by track, at least one route
with a running train, **and** one track broken by a meteor (trigger one via
`CheatTriggerMarsquake()` near a track, or play until one lands). Extending SAVE-A
works. Console open (Enter / Alt-Shift-C).

**Trigger — case A (healthy track):**
1. Pick an intact track and note its endpoints:
   `qa_t = MainCity.labels.TrackBase[1]`
   `print(qa_t.start_el, qa_t.end_el, #qa_t.elements)`
2. Run the CORRECTED call the F48 repair would ship:
   `ProcessTrackElements(ResolveMap(qa_t), qa_t.elements)`
   `qa_t.start_el = qa_t.elements[1]  qa_t.end_el = qa_t.elements[#qa_t.elements]`
3. Re-print the endpoints; check the route still forms, the train still runs, and
   nothing visual changed. **Save, reload, check again.**

**Trigger — case B (the damaged track — the risky one):**
4. Repeat steps 1-3 with `qa_t` set to the meteor-damaged track (pick the right
   index from `MainCity.labels.TrackBase`). Expect the console to print the
   "unable to find the expected number of track elements" assert — that is fine
   *if nothing corrupts*: after it, check the repair site is still salvageable
   (F45), the rest of the network still routes, and a **save + reload** comes back
   clean.

- **UNBLOCKS F48 looks like:** case A is a stable no-op-or-better and case B fails
  *cleanly* (assert printed, network intact after reload) → the repair ships in
  `90_SaveSanitizer.lua` behind a one-shot flag, skipping tracks that carry repair
  sites.
- **CONFIRMS THE BLOCK looks like:** case B leaves a track that will not route, a
  train stuck, or a save that reloads broken → F48 closes as
  `wontfix — repair riskier than the defect`, record exactly what broke.

`Result (case A healthy):` _____________________________________________

`Result (case B damaged):` _____________________________________________

### PT-42 — Last Transmission notices your reserves · covers **F22, F75**

Probes prove the presets are wired correctly and the reserve maths is right;
only play can show the approval actually moving and the UI goal clearing.

**Setup:** a game where **Last Transmission** is an active faction, ideally with
the Underground map opened (that is what made the old maths hopeless). Open the
faction panel and note the current approval and the listed "How to achieve"
goals.

**Steps:**
1. Look for goals like "Have Power for more than 2 sols stored", "Have Water for
   more than 2 sols stored", "Have Oxygen for more than 2 sols stored".
2. Build up **Power** storage until you comfortably hold more than 2 sols'
   worth, and let a day pass.
   - **EXPECTED:** the Power goal stops being listed as outstanding and the
     faction's approval rises; the reason appears in the approval breakdown.
   - **SURPRISE looks like:** the goal stays listed forever no matter how much
     you bank (that is the old behaviour).
3. Repeat for **Water**, then for **Oxygen**. The Oxygen one is the important
   check — it used to be satisfied by having Power stored.
   - **EXPECTED:** stocking Oxygen (and only Oxygen) clears the Oxygen goal.
4. Now drain one of them to zero — switch off or salvage the storage.
   - **EXPECTED:** the matching penalty ("No Power stored" etc.) appears and
     approval falls. Before the fix this was unreachable once a second map was
     loaded.
5. Check the log for `GridGlobalStorage: applied` and
   `LastTransmissionStorage: ... storage condition(s) made effective`.

`Result (goals clear when stocked?):` _____________________________________________

`Result (Oxygen goal needs Oxygen / penalties reachable at zero?):` _____________________________________________

### PT-44 — Founder trait notice and dome pipe cleanup · covers **F23, F24**

**F23 — Founder gains a trait.** Probes cover the wiring; play confirms the
notification renders and reads correctly.
1. Play until one of your **Founders** gains a trait (age, a story event, or the
   Gene Forging / trait-granting paths).
   - **EXPECTED:** a "Founder gains trait" notification appears, naming the
     colonist and the trait, and clicking it selects them.
   - **SURPRISE looks like:** nothing appears (the old behaviour), or two
     notifications appear for the same event.

`Result (notification appears once, names the right trait?):` _____________________________________________

**F24 — dome absorbing a pipe-connected building.** This one has no probe: it
needs a real dome and real pipes.
2. Build a life-support building **outside** a dome and connect it with pipes
   (Water Extractor, Moisture Vaporator, Water Tank, or an Oxygen tank).
3. Now build or upgrade a **dome** so that the building ends up **inside** the
   dome's footprint (the game moves it "inside" the dome's grid).
   - **EXPECTED:** the pipe stubs and connection graphics at the old boundary
     disappear cleanly; the building keeps working on the dome's grid; no
     orphaned plug graphics are left floating.
4. **Save, quit to the menu, and reload.** The repair sweep that runs on load
   exercises the same code path.
   - **EXPECTED:** still clean — no stale pipe visuals reappear, and pipes can
     still be connected in that area afterwards.
   - **SURPRISE looks like:** leftover plugs/pipe ends, or a spot where new pipe
     refuses to connect.
5. Check the log for errors mentioning `DestroyConnection` or `LifeSupportGrid`.

`Result (clean at absorption / clean after reload / pipes still connectable?):` _____________________________________________

### PT-47 — Bombardment volley shape · covers **F26**

The probe can prove the game computes a different direction per missile; only eyes
can confirm the volley looks like a scatter rather than a rank. This fix is the
pack's largest copied function (100 lines of `WaitBombard`), so the point of this
test is as much "nothing else about a bombardment broke" as it is the spread.

**Setup:** a Mystery 7 bombardment, or force one from the console:
`StartBombard(UIColony:GetCityAtMap(MainMap), 40*guim, 8, 500, 1500)`
(any valid object or point works as the first argument; 8 missiles makes the shape
obvious). Watch from a low camera angle so the incoming trails are visible.

**Trigger:**
1. Watch a volley arrive.
   - **EXPECTED:** the missiles come in from visibly different angles — a scatter,
     not a rank of parallel trails.
   - **SURPRISE looks like:** still perfectly parallel (the old behaviour).
2. Check that everything else about the volley still works, because the whole
   function was replaced:
   - impacts leave scorch decals that fade out;
   - a missile that hits a dome cracks it instead of exploding on the ground;
   - the "Incoming Missile" notification appears and clears;
   - missiles shot down by defences explode in the air;
   - the bombardment ENDS (the sequence continues afterwards) — if the volley
     never finishes, that is a FAIL and the fix should be reverted.
3. Check the log for errors mentioning `Bombardment`, `BombardMissile` or
   `WaitBombard`.

`Result (spread visible?):` _____________________________________________

`Result (decals / dome hits / notification / interception / volley ends?):` _____________________________________________

### PT-48 — Acknowledged warnings · covers **D02 `Opt_AcknowledgedWarnings`**

Dismissal now means "I've seen THESE buildings" instead of "silence the whole
category for 4 game hours". **Enable route:** Options → Mod Options →
Community Fix Pack → **Acknowledged warnings** (takes effect on Apply, no
restart); `SMRFixPack.ListFixes` must show it `active`. This is a FEATURE, not
a fix — the question is "does it behave as advertised", plus the usual
"nothing else broke".

**Setup:** break two buildings in ways that won't self-heal (e.g. turn off their
power supply, or use a permanently entombed/unsupplied building if the save has
one). Wait for the "Building Not Working" notification listing both.

**Trigger:**
1. Dismiss the notification (right-click it / its dismiss control).
   - **EXPECTED:** it goes away and STAYS away — play several game hours at high
     speed; the two acknowledged wrecks never re-nag (vanilla re-nags every 4
     game hours ≈ every few real seconds at ultra).
2. While it is quiet, break a THIRD building.
   - **EXPECTED:** a new "Building Not Working" notification appears promptly
     for the new one — no 4-hour category silence (this is the module's other
     half; vanilla would keep it quiet for the rest of the window).
   - The new notification lists only the new building, not the acknowledged two.
3. Repair one of the acknowledged buildings, let it run, then break it AGAIN.
   - **EXPECTED:** it notifies again — recovery re-arms the warning.
4. Save, reload, and confirm the still-broken acknowledged building stays quiet
   after the load (the stamp persists).
5. Other warnings (fuel, DestroyedInfrastructure, rover damage) must behave
   exactly as vanilla — dismiss one and confirm nothing odd.

`Result (acked stay quiet / new one warns / re-break warns / survives reload?):` _____________________________________________

---

# 5 · Cross-cutting — do these last, once per era of the pack

## PT-20 — Uninstall safety · covers **all fixes / FIX_POLICY §3**

The pack must never hold a save hostage.

**Steps:**
1. Play SAVE-F (or any save) **with the fix pack enabled** for a few sols; save it.
2. Quit to the main menu, open the **Mod Manager**, and **disable the Community Fix
   Pack only**. Leave the Test Kit enabled.
3. Restart the game and **load that save**.
4. Play **10 minutes** of ordinary gameplay: build something, salvage something, let a
   sol pass, save and reload once.

- **BROKEN looks like:** the save refuses to load, throws missing-class/missing-function
  errors on load, or the colony visibly misbehaves (buildings inert, colonists frozen)
  because something the pack created is now dangling.
- **FIXED looks like:** the save loads and plays completely normally — the original bugs
  come back, which is expected and fine, but nothing is corrupted or crashing.

**Then check the log** (`%AppData%\Surviving Mars Relaunched\logs`, newest
`Mars.exe-*.log`) for any error mentioning our code.

Re-enable the fix pack before continuing.

> Note for the next run: the 2026-07-29 audit flagged the wave-6 fixes as the
> newest un-cycled persisted state (`Fix_RainsDeadlock` persists its loop
> threads by global name; `SMRFixPack_fixed_loop` markers) — make sure the
> save used for this test post-dates wave 6 so the cycle covers them.

`Result:` _____________________________________________

## PT-21 — Long-save soak

**Setup:** any healthy colony (SAVE-A or the live colony is fine). All **68
default fixes** active — confirm with `SMRFixPack.ListFixes` (opt-in modules
read `inactive` unless you enabled them).

**Steps:**
1. Play a **normal session** — 45–60 minutes of real play, no cheats, mixed speeds,
   at least one full save/reload partway through. Just play the game.
2. During play, note anything that feels off: stuck colonists, drone clusters, trains
   that don't move, notifications that flicker, unexplained deaths.
3. At the end, run the state reports:
   ```
   SMRTest.ReportReservations
   SMRTest.ReportTrains
   SMRTest.ReportBrokenTrack
   ```
4. Optionally `SMRTest.RunAll` for a regression sanity check (expect the same
   PASS/SKIP pattern as the last A/B run — the `[install]` probes SKIP on retail,
   that is normal and not a failure).
5. Quit and read the log (see PT-22).

- **BROKEN looks like:** `[CommunityFixPack]` errors in the log, stale reservation
  counts climbing over the session, train prefab counts drifting down, or engine errors
  that don't appear in a vanilla session.
- **FIXED looks like:** zero `[CommunityFixPack]` errors, `ReportReservations` reporting
  0 clearly-stale slots, `ReportBrokenTrack` reporting 0 bad `node_idx`, and no new
  engine error signatures.

`Result (gameplay feel):` _____________________________________________

`Result (ReportReservations):` __________  `(ReportTrains):` __________  `(ReportBrokenTrack):` __________

`Result (log clean?):` _____________________________________________

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

---

## Reporting protocol

**Tester (you):**
1. Fill in every `Result:` line — `PASS` / `FAIL` / `SKIP (reason)` — plus free-text
   notes and the **date**. Screenshots for anything visual (especially PT-10).
2. Commit this file, or simply tell the next session:
   **"read PLAYTEST_CHECKLIST.md results"**.

**Next session — do exactly this:**
1. Read this file's `Result:` lines.
2. For every fix whose covering test(s) **PASSed**, flip its status to `tested`
   in `docs/BUGS.md` — **both places**:
   - the **index row** (`| F0x | … | fixed |` → `tested`), and
   - the **detail heading tag** (`` `[fixed: Code/Fix_X.lua]` `` → `` `[tested: Code/Fix_X.lua]` ``).
   A fix covered by more than one test only goes `tested` when **all** its
   results pass. Partial fixes (marked `fixed*`) go to `tested*` and keep
   their open-half note. Behavioural/timing results also record their
   conditions per the EXTERNAL VALIDITY rule.
3. Move the corresponding lines in `docs/MOD_DESCRIPTION.md` into the shipping fix list
   if that file segregates tested vs untested (only `tested` fixes ship in the final
   player-facing text).
4. For every **FAIL**, do **not** flip the status. Instead:
   - record it as a **new finding** in `docs/BUGS.md` (new detail entry + index row, or
     an appended note on the existing entry if it's a regression of that same fix),
   - set the affected fix back to `todo`/`blocked` as appropriate with the tester's
     verbatim observation quoted,
   - add it to the "Next gates" line in `docs/STATUS.md`'s header.
5. For **PT-10 (F55)**, whichever way it lands, record the observation on the F55 BUGS.md
   entry and resolve the open question in STATUS.md's "Waiting on the user" item.
6. Update STATUS.md's current-state header (counts / next gates) to reflect
   the new results, and append the sitting as a new leg at the top of
   `docs/archive/SESSION_LOG.md`.
7. Commit everything in one change, with the playtest date in the message.
8. Move each completed test's section — test text plus the filled-in results —
   from this file into `docs/PLAYTEST_ARCHIVE.md`, so this checklist only
   carries un-run work. (A partially-passed test stays here with its passed
   triggers recorded, like PT-52/PT-53 above.)
