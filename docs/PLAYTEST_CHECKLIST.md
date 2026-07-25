# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next Claude session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

## Why this document exists

All **30 fixes already passed the automated script probes** — the final A/B RunAll
pair flipped **19/19 discriminating probes FAIL→PASS** with zero FAILs and all 30
fixes reporting `applied` (STATUS.md → "FINAL A/B RunAll pair"). That proves the
*wiring*: the patched functions are installed and return the right values when
driven with synthetic input.

It does **not** prove any of the things only a human at the keyboard can see:

- how it *feels* in real play (cadence, pacing, does the colony actually recover),
- **visuals** (does the trimmed track leave a sane-looking remainder?),
- **UI** (does the number actually render in the panel?),
- **long-running behavior** (does it still hold after 3 sols, after a save/load?),
- emergent multi-system interactions the probes stub out.

**A pass here is what earns a fix `tested` status in BUGS.md.** Probe-verified ≠
tested. Nothing ships as "verified" on probe evidence alone.

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
4. **Achievements are off** while any mod is active (`ModManager.lua:78`) — expected,
   not a bug.
5. If a step's setup fails, write that down. "Could not set this up" is a valid and
   useful result.

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
| `CheatResearchAll()` | `Lua/Cheats.lua:78` | grant all techs |
| `MultiCheat()` | `Lua/Cheats.lua:328` | unlock all + deep scan + research all |
| `CheatSpawnNColonists(n, age_trait, backstory)` | `Lua/Cheats.lua:225` | spawn into selected dome, else spread |
| `CheatGenerateApplicants(n)` | `Lua/ApplicantsPool.lua:210` | applicant pool |
| `CheatUpdateAllWorkplaces()` | `Lua/Cheats.lua:210` | re-run job assignment now |
| `CheatToggleAllShifts()` | `Lua/Cheats.lua:192` | open/close every shift |
| `CheatToggleInfopanelCheats()` | `Lua/Cheats.lua:290` | per-building break/repair/malfunction buttons in the infopanel |
| `CheatMeteors("single"\|"multispawn"\|"storm", setting, pos)` | `Lua/Cheats.lua:62` | meteor strike at the camera look-at |
| `CheatTriggerMarsquake(settings_name)` | `Lua/Marsquake.lua:223` | surface quake |
| `CheatTriggerUndergroundMarsquake()` | `Lua/Marsquake.lua:292` | underground quake (**bypasses** the scheduler — see PT-11) |
| `CheatTriggerUndergroundCaveIn(pos)` | `Lua/Marsquake.lua:284` | cave-in at a position |
| `CheatStopDisaster()` | `Lua/Cheats.lua:74` | stop the running disaster |
| `CheatStartMystery(id)` | `Lua/Mysteries/Mysteries.lua:91` | **gated on `Platform.cheats`** — see PT-15 |
| `CheatMapExplore("scanned"\|"deep scanned"\|"scan queued")` | `Lua/Cheats.lua:5` | reveal deposits |
| `UIColony:UnlockUnderground()` | `Lua/Colony.lua:490` | underground access |
| `CheatRevealDarkness()` | `Lua/Cheats.lua:390` | generate + switch to the underground map |
| `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` | `Lua/Discoveries.lua:35`, call form at `Lua/XDef/GameCheatShortcuts.generated.lua:184` | asteroid discover + scan + unlock |
| `dbg_ToggleRocketInstantTravel()` | `Lua/Buildings/RocketUtilities.lua:451` | collapse flight time (Mars↔asteroid in seconds) |
| `SetTerraformParamPct(param, pct)` | `Lua/Terraforming.lua:210` | e.g. `SetTerraformParamPct("Atmosphere", 95)` |
| `CheatOpenAllDomes()` / `CheatCloseAllDomes()` | `Lua/Cheats.lua:414` / `:426` | opens domes **and** maxes terraforming + Open Domes policy |
| `OpenAllDomes(MainCity)` / `CloseAllDomes(MainCity)` | `Lua/Buildings/Dome.lua:3415` / `:3423` | open/close only, no side effects |
| `SetLightTrapMode("free"\|"destroy")` | `Lua/Mysteries/Fireflies.lua:674` | St. Elmo's Fire wisp disposition |
| `CompleteMilestone(id, res)` | `Lua/Milestones.lua:108` | complete a milestone by id |
| `ColonyGetPrefabs("Train", MainCity)` | `Lua/Colony.lua:681` | stored-prefab counter |
| `OpenCommandCenter()` / `CloseCommandCenter()` | `Lua/X/ColonyControlCenter.lua:1614` / `:1630` | Command Center UI |
| `SetGameSpeedState("ultra")` | `Lua/X/HUD.lua:528` | 20× (`const.ultraGameSpeed = 20`, `Lua/_GameConst.lua:28`) |
| `UIColony:SetGameSpeed(n)` | `Lua/Colony.lua:564` | arbitrary factor; `n = 20` == ultra. Higher values work (clamped at `const.MaxTimeFactor`) but stress the sim — prefer 20 |

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
| `SMRTest.Log.Meteors(true/false)` | prints each `MeteorsDisaster` call with the gap in game hours — **PT-01** |
| `SMRTest.Log.DroneChurn(true/false)` | prints how many drones a rocket's reconnect just kicked to Idle — **PT-04** |
| `SMRTest.Log.AutoCargo(true/false)` | prints each lander auto-cargo request + what's aboard — **PT-16/PT-17** |
| `SMRTest.Log.CargoReady(true/false)` | prints each `IsCargoReady` verdict — **PT-16** |
| `SMRTest.Log.WorkShift(true/false)` | prints shift-3 `ShouldLeaveForWork` verdicts |
| `SMRTest.ReportBrokenTrack` | counts track repair sites with a non-numeric `node_idx` — **PT-03** |
| `SMRTest.ReportReservations` | counts stale residence reservations — **PT-21** |
| `SMRTest.ReportTrains` | stored train prefabs vs trains on the map — **PT-21** |
| `SMRTest.RunAll` | re-run the whole probe suite (sanity check before/after a session) |
| `SMRFixPack.ListFixes` | confirm all 30 fixes report `applied` (`Code/00_Core.lua:56`) |

Turn loggers **off** when a test is done — they print every tick and will bury the log.

---

## Save fixtures — create these once, reuse them

Make each one, then **save under the given name**. Every test below names its fixture.
Keep a pristine copy of each (save-as with a `-base` suffix) so a destructive test
doesn't cost you the setup.

| Fixture | How to build it | Feeds |
|---|---|---|
| **SAVE-A — Sandbox colony** | New game, any sponsor, **default game rules** (disasters ON, meteors at least "Low"), Mars surface. Land, build one dome with ~20 colonists, a Medical Center, a Martian Express station with a short track, and a landed rocket. `MultiCheat()` + `CheatAddFunding(500000000)` to remove build gating. | PT-01 … PT-10 |
| **SAVE-B — No-Disasters underground** | New game, tick the **No Disasters** game rule at setup (it cannot be added later). Then in-colony: `UIColony:UnlockUnderground()` and `CheatRevealDarkness()`, build a small underground presence. | PT-11 |
| **SAVE-C — Two-dome colony** | New game (any). Build **dome A** and **dome B ~350 m apart, joined by a passage**. Give A residents but **no** spare housing; give B **free housing and a shop/diner**. Keep atmosphere non-breathable (do NOT terraform). No Shuttle Hub yet. | PT-12 … PT-14 |
| **SAVE-D — St. Elmo's Fire mystery** | Easiest: start a **new game and pick "The Power of Three / St. Elmo's Fire" (`LightsMystery`) as the mystery at setup**, then play/skip forward until Light Traps are buildable and have caught wisps. (Console alternative in PT-15.) | PT-15 |
| **SAVE-E — Frontier save (underground elevator + asteroid)** | From a healthy mid-game colony: `UIColony:UnlockUnderground()`, `CheatRevealDarkness()`, build an **Elevator** and an **underground dome with free housing**; then `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` and build/land an **Asteroid Lander** with a **MicroG Habitat** and a couple of colonists on the asteroid. `dbg_ToggleRocketInstantTravel()` when running lander tests. | PT-16 … PT-19 |
| **SAVE-F — Uninstall-safety copy** | Just a save made *while the fix pack is enabled* — copy of SAVE-A after ~1 sol of play is fine. | PT-20 |

Rough effort: SAVE-A ~20 min, SAVE-B ~15, SAVE-C ~20, SAVE-D ~20, SAVE-E ~30.
SAVE-E is the expensive one; do it last and do all four of its tests in one sitting.

---

# Group 1 — SAVE-A (sandbox colony)

## PT-01 — Meteor cadence + Sensor Tower direction · covers **F02**

**Setup:** SAVE-A. Meteor setting at least "Low". Note the current sol/hour.

**Trigger (console):**
```
SMRTest.Log.Meteors(true)
g_MeteorsGameDescr.spawntime = 40 * const.HourDuration
g_MeteorsGameDescr.spawntime_random = 0
SetGameSpeedState("ultra")
```
(`g_MeteorsGameDescr` is the live descriptor the thread re-reads each loop,
`Lua/Meteors.lua:271-278`; the change takes effect on the **next** interval, so let
one strike pass first.) Watch the console for `MeteorsDisaster at t=… (+N game hours)`
lines. Let 3–4 strikes go by.

Then the **direction check**: build 3 Sensor Towers (`CheatCompleteAllConstructions()`),
let 2 more strikes pass, and compare the gaps. Sensor Towers add warning time
(`const.SensorTowerPredictionAddTime = 12 * const.HourDuration`, `Lua/_GameConst.lua:125`).

- **BROKEN looks like:** meteors land roughly every 6 game hours, all game long — and
  putting up Sensor Towers makes the gaps *longer*, not the strikes more predictable.
- **FIXED looks like:** gaps sit near the 40 h you set (never far below it), and adding
  Sensor Towers does **not** stretch the gap further — it only lengthens the warning.

Turn the logger off (`SMRTest.Log.Meteors(false)`) and restore speed when done.

`Result:` _____________________________________________  (PASS / FAIL / notes / date)

---

## PT-02 — Upgrade-modifier leak across build → upgrade → salvage → rebuild · covers **F03**

**Setup:** SAVE-A, a dome with a **Medical Center**. `CheatAddFunding(500000000)`,
`CheatResearchAll()` so the **Holographic Scanner** upgrade is available.

**Trigger:**
1. Select the dome and record its modifier count:
   `*r local n=0 for l,m in pairs(SelectedObj.label_modifiers or {}) do for _ in pairs(m) do n=n+1 end end ConsolePrint("dome modifiers: "..n)`
   (select the **dome** first — `label_modifiers` lives on the label container,
   `Lua/LabelContainer.lua:59-63`.)
2. Buy the **Holographic Scanner** upgrade on the Medical Center. Re-run the count →
   should go **up by one**.
3. **Salvage the Medical Center.** Re-run the count.
4. Rebuild the Medical Center (`CheatCompleteAllConstructions()`), buy the upgrade
   again. Re-run the count.

- **BROKEN looks like:** the count never drops after salvage, and climbs by one more
  every rebuild — the dome keeps a phantom +30 birth-comfort bonus from buildings that
  no longer exist, stacking forever.
- **FIXED looks like:** the count returns to its pre-upgrade value after salvage, and
  after rebuild+re-upgrade sits at exactly **one** upgrade modifier — no stacking.

> Note: the fix stops **new** leaks. Modifiers already leaked into an *old* save are
> not swept yet (that's the queued `90_SaveSanitizer.lua`). Test on a save built with
> the pack active.

`Result:` _____________________________________________

---

## PT-03 — Track salvage: partial trim, curve visuals, broken-track salvage · covers **F44, F45**

**Setup:** SAVE-A with a Martian Express station and track. Build **two** test tracks:
a straight run of ~8 hexes, and a second run that **ends in a curve** (this is the
visual the audit specifically flagged). `CheatCompleteAllConstructions()`.

**Trigger — F44 (partial salvage):**
1. Assign a train to the straight track.
2. Salvage-click a **middle hex**.
3. Repeat on the **curve-ended** track, clicking a hex 2–3 in from the curved end.

- **BROKEN looks like:** clicking one hex deletes the whole track — and any train
  assigned to it vanishes with it.
- **FIXED looks like:** only the clicked segment (plus the short unusable stub on one
  side) disappears; the long viable side and the train survive.
- **VISUAL CHECK (the audit's specific concern):** after trimming near a curve, does
  the remaining track *look* right — pillars, rails and end-caps in sensible places, no
  floating hex, no rail stub hanging in the air, no missing end element?
  **Write down exactly what you see, and grab a screenshot.**

**Trigger — F45 (broken-track salvage):**
4. Aim the camera at a track hex and run `CheatMeteors("single")` until a meteor
   breaks a track element (a repair site appears on the track).
5. Run `SMRTest.ReportBrokenTrack` → note the "non-numeric node_idx" count.
6. Try to **salvage the broken element** (click it, and try the infopanel Salvage button).

- **BROKEN looks like:** the salvage click does absolutely nothing — no countdown, no
  feedback, the damaged track is permanently undeletable; the report shows sites with a
  non-numeric `node_idx`.
- **FIXED looks like:** report shows **0** bad sites, and the broken element salvages
  like any other.

`Result (F44 trim):` _____________________________________________

`Result (F44 curve visual):` _____________________________________________

`Result (F45 broken salvage):` _____________________________________________

---

## PT-04 — Rocket drone churn · covers **F50**

**Setup:** SAVE-A with a **landed rocket carrying cargo** and a **Drone Hub placed far
from it** — far enough that a drone's one-way trip takes more than a game hour (drop
the hub at the far edge of the buildable area; if drones still arrive too fast, use
ultra speed only *after* the drones are en route so you can watch them).

**Trigger:**
```
SMRTest.Log.DroneChurn(true)
```
Let 3+ game hours pass with drones actively hauling from the rocket. Watch the console.

- **BROKEN looks like:** every game hour a batch of drones heading for the rocket
  suddenly stops, turns around and goes idle — the rocket never gets unloaded, and the
  log fills with `OnRemoveBuilding(...) -> N drone(s) sent to Idle`.
- **FIXED looks like:** no hourly `-> N drone(s) sent to Idle` lines from the rocket
  path; drones keep walking and the cargo actually moves.

Turn the logger off afterwards.

`Result:` _____________________________________________

---

## PT-05 — Milestone completion popup · covers **F05**

**Setup:** **A new game started with the `NoTerraforming` game rule** (this is what
guarantees hidden-but-uncompleted milestones — 9 of them). One dome, minimal colony.
This is a 5-minute throwaway save; you do not need SAVE-A for it.

**Trigger:** complete the visible milestones from the console, leaving one for last:
```
CompleteMilestone("ScanAnomaly", true)
CompleteMilestone("ConstructDome", true)
CompleteMilestone("FirstHumanOnMars", true)
```
…and so on through the visible list (ids are in `Data/Milestone.lua`: `ScanAnomaly`,
`ReturnRocket`, `FindWater`, `ConstructDome`, `FirstHumanOnMars`, `Martianborn`,
`ProduceFood`, `ResearchBreakthrough`, `SponsorGoals`, `ScanAllSectors`,
`Population100`, …). Complete the **last** one and watch.

- **BROKEN looks like:** the final milestone silently does nothing — no celebration
  popup — and the log shows an "attempt to perform arithmetic on a nil value" error.
- **FIXED looks like:** the "all milestones completed" popup appears, and the log is
  clean.

`Result:` _____________________________________________

---

## PT-06 — Five-star tourist applicant jump · covers **F08**

**Setup:** SAVE-A. You need a tourist-carrying rocket to **depart**. Build a Hotel/
Spacebar so tourists arrive; ensure high Comfort so the group rates 5 stars (open the
infopanel and check the rating before departure). `CheatToggleInfopanelCheats()` gives
you per-building levers if you need to force a state.

**Trigger:**
1. Before the tourist rocket departs, note the **applicant pool size** (Colony
   Control Center → Applicants, or `#UIColony.applicants_pool`).
2. Let the rocket depart. Note the pool again.
3. Repeat once with a **deliberately bad (1-star)** tourist group (turn off the Hotel's
   power / let comfort tank).

- **BROKEN looks like:** the miserable 1-star tourist group brings you *more* new
  applicants than the delighted 5-star group — the reward is upside-down.
- **FIXED looks like:** the 5-star departure gives a clearly bigger applicant bump than
  the 1-star one.

`Result:` _____________________________________________

---

## PT-07 — Low-food warning · covers **F12**

**Setup:** SAVE-A with a colony that actually **consumes food** (colonists eating,
farms producing, at least one full sol of consumption history — the check reads
"consumed yesterday", `Lua/ResourceTracking.lua:228`). Threshold is 3 sols
(`const.MinDaysFoodSupplyBeforeNotification = 3`, `Lua/_GameConst.lua:11`).

**Trigger:** drain the Food stock below ~3 sols of consumption — salvage the food
depot contents, or dump food by demolishing storage. Then wait ≤1 game hour at
`SetGameSpeedState("ultra")`.

Repeat for a maintenance resource (Machine Parts): let stock drop under 3 sols of
maintenance consumption.

- **BROKEN looks like:** food (and Machine Parts) run down to nothing with **no warning
  at all** — the "insufficient resources" notification simply never fires for them.
- **FIXED looks like:** the low-supply notification appears within a game hour of
  crossing the 3-sol line, naming Food (and Machine Parts), with a sane hours estimate.
- **Also check:** while the warning is active, does it sit there quietly, or does it
  visibly flicker / replay its alert sound every game hour? (The F12 rework was
  specifically about killing that churn.) **The warning should be steady.**

`Result:` _____________________________________________

---

## PT-08 — Command Center resource rows · covers **F13**

**Setup:** SAVE-A with a real economy (some Metals, Concrete, Polymers, Food, Water,
Electronics, Machine Parts, Rare Metals in stock).

**Trigger:** `OpenCommandCenter()` (or the in-game button). Go to the resource
overview and read every resource row.

- **BROKEN looks like:** the resource rows show icons and labels but the **numbers are
  blank** — you cannot tell how much of anything you have from this screen.
- **FIXED looks like:** all 11 resource rows show numbers, and those numbers match what
  the HUD/resource overview says.

`Result:` _____________________________________________

---

## PT-09 — Domes Overview red low-stat column · covers **F14**

**Setup:** SAVE-A. Drive one dome's **average Health (or Comfort / Sanity / Morale)
below the low threshold** — cut its life support / medical building, or spawn a batch
of colonists into a dome with no services:
`CheatSpawnNColonists(30)` with that dome selected, then let a sol pass at ultra speed.

**Trigger:** `OpenCommandCenter()` → **Domes Overview** tab. Look at that dome's row.

- **BROKEN looks like:** the failing stat is rendered in ordinary white text, exactly
  like a healthy one — nothing on the overview tells you which dome is in trouble.
- **FIXED looks like:** the below-threshold value is highlighted **red** in its column,
  and normal values stay unhighlighted.

`Result:` _____________________________________________

---

## PT-10 — Open-roof drone observation · covers **F55** ❓ **OPEN QUESTION**

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

---

# Group 2 — SAVE-B (No Disasters, underground)

## PT-11 — Cave-ins under the No Disasters rule · covers **F01**

**Setup:** SAVE-B. Confirm the rule is on: `IsGameRuleActive("NoDisasters")` should
print `true`. Have some underground infrastructure that rubble would visibly damage.

**Trigger (console):**
```
g_Consts.MarsquakeSpawnTime = 1
g_Consts.MarsquakeRandomTime = 1
SetGameSpeedState("ultra")
```
(the underground quake repeat sleeps `MarsquakeSpawnTime * const.HourDuration` +
`Random(MarsquakeRandomTime * const.HourDuration)`, `Lua/Marsquake.lua:308,313`).
Let **20+ game hours** pass. Then save, reload, and let another 20 pass.

- **BROKEN looks like:** underground quakes and cave-in rubble keep happening on a save
  you explicitly started with disasters turned off.
- **FIXED looks like:** nothing. No quake, no rubble, no cave-in notification — forever,
  including after a save/load.

> Expected and **not** a failure: `CheatTriggerUndergroundMarsquake()` still fires a
> quake. It bypasses the scheduler on purpose; the fix gates the scheduler only
> (`Lua/Marsquake.lua:292`).

`Result:` _____________________________________________

---

# Group 3 — SAVE-C (two-dome colony)

## PT-12 — Shuttle-cache emigration · covers **F51**

**Setup:** SAVE-C. Dome **A** has homeless colonists and no spare housing; dome **B**
is **far away (out of walking range, no passage to A)** with plenty of free housing.
**No Shuttle Hub anywhere.** Let at least one full emigration evaluation cycle run at
ultra speed so the "no transport available" verdict gets cached — you should see
colonists stay homeless in A.

**Trigger:** now build and **fuel** a Shuttle Hub (`CheatCompleteAllConstructions()`,
`CheatFillAllStorages()`), then wait 1–2 game hours at ultra speed.

- **BROKEN looks like:** you build a Shuttle Hub, shuttles fly, and the homeless
  colonists in dome A *still* never move to the empty houses in dome B — the game
  decided once that there was no transport and never re-checked.
- **FIXED looks like:** within a cycle or two of the hub going live, homeless colonists
  start emigrating to dome B and the Homeless count drops.

`Result:` _____________________________________________

---

## PT-13 — Vacuum walk routing · covers **F52**

**Setup:** SAVE-C — domes A and B ~350 m apart (**under** the 400 m
`const.ColonistMaxDomeWalkDist`, `Lua/_GameConst.lua:133`) **joined by a passage**,
with the direct outdoor route also open. Atmosphere must be **non-breathable**: check
`GetTerraformParamPct("Atmosphere")` is low; if you terraformed by accident, use
`SetTerraformParamPct("Atmosphere", 5)`.

**Trigger:** force a colonist to move between the domes — set dome A to not accept
residents / turn off its life support briefly, or use a workplace in B. Then **follow a
colonist with the camera** for the whole trip.

- **BROKEN looks like:** the colonist strolls out the airlock and hikes across open
  vacuum between the domes, with the suffocation timer ticking — and some of them die
  en route.
- **FIXED looks like:** the colonist uses the **passage** (goes through the tube, no
  outdoor stretch) — or waits/refuses rather than walking exposed.

> Known partial: if there is **no** passage route at all, an outdoor walk is still
> allowed by design (refusing it would strand colonists on shuttle-less maps). Only the
> "passage exists but is ignored" case is a FAIL.

`Result:` _____________________________________________

---

## PT-14 — Cross-dome shopping with migration off · covers **F61**

**Setup:** SAVE-C — dome **A** (residents, no shop/diner) connected by **passage** to
dome **B** (has the shop/diner/university). Both domes healthy.

**Trigger:** on dome **A**, turn **"Accept Colonists" OFF** (the migration toggle in the
dome infopanel — `Community:ToggleAcceptColonists`, `Lua/Buildings/Community.lua:106`).
Leave dome B's toggle alone. Run 1–2 sols at ultra speed and watch A's residents.

- **BROKEN looks like:** switching off *migration* on the home dome also silently stops
  its residents from shopping, working or training in the connected dome — comfort and
  service satisfaction slide with no explanation.
- **FIXED looks like:** residents of A keep walking through the passage to shop/work/
  train in B; only actual **immigration into A** is blocked.

Also confirm dome **B** with its own toggle off still correctly **refuses** incoming
colonists — the fix must not open the wrong gate.

`Result:` _____________________________________________

---

# Group 4 — SAVE-D (St. Elmo's Fire mystery)

## PT-15 — Wisp power output · covers **F07**

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

---

# Group 5 — SAVE-E (frontier: elevator + asteroid)

Do all four of these in one sitting — SAVE-E is the expensive fixture.
Run `dbg_ToggleRocketInstantTravel()` once at the start of PT-16/PT-17.

## PT-16 — Asteroid lander: empty launch + return fuel · covers **F67, F69**

**Setup:** SAVE-E. An **Asteroid Lander** on the pad. `dbg_ToggleRocketInstantTravel()`.

**Trigger — F67 (empty launch):**
1. Enable **Automated Mode** on the lander and set **every** export/import threshold to
   "ignore" (so the auto request computes to nothing).
2. `SMRTest.Log.CargoReady(true)` and `SMRTest.Log.AutoCargo(true)`.
3. Run 1–2 sols at ultra speed.

- **BROKEN looks like:** the lander takes off with an empty hold and ping-pongs
  Mars↔asteroid forever, burning ~70 fuel a trip and delivering nothing.
- **FIXED looks like:** the lander **sits on the pad** while its cargo request is empty
  (`IsCargoReady -> false` in the log); it only launches once it has something to carry
  (or when the 1-sol auto-depart timer legitimately expires).

**Trigger — F69 (return fuel):**
4. Manually fly the lander to the asteroid and **land it manually** (no return
   destination set). Make sure there are **no drones and no drone hub** on the asteroid.
5. Watch the lander's fuel and its resource requests after `CmdUnload`.

- **BROKEN looks like:** on landing the lander dumps its reserved return fuel onto the
  ground as "excess" — with no drones there to put it back, the lander is stranded on
  the asteroid permanently.
- **FIXED looks like:** the lander **keeps a fuel ration requested/reserved** (≥ its
  `FuelResourceAmount`) and can fly home.

`Result (F67):` _____________________________________________

`Result (F69):` _____________________________________________

---

## PT-17 — Lander cargo ratchet + the capacity edge case · covers **F68**

**Setup:** SAVE-E, lander on an **asteroid** in Automated Mode, with resources
available to export. `SMRTest.Log.AutoCargo(true)`.

**Trigger — the ratchet:**
1. Set **one** export threshold (say Metals) so the lander loads cargo.
2. Let drones load the hold to roughly half.
3. Watch the `CreateAutoCargoRequest(...) request{...} aboard{...}` lines over
   2–3 game hours.

- **BROKEN looks like:** every hour the lander asks for *less* than it is already
  carrying, flips to "unloading", and drones haul the cargo it just loaded back out —
  it loads exotics then dumps them and leaves with junk or nothing.
- **FIXED looks like:** the `request{}` figures **never fall below** the matching
  `aboard{}` figures; the hold only fills.

**Trigger — the capacity edge (the specific thing the audit flagged as unverified):**
4. Now set **two or more** export thresholds — deliberately pick resources whose names
   sort so that an **alphabetically earlier** one is present in bulk (e.g. **Concrete**
   *and* **Metals**, or **Electronics** *and* **PreciousMetals**).
5. Load the hold **to capacity** (`CheatFillAllStorages()` on the asteroid side helps).
6. Watch the lander's **status** and whether it ever departs.

- **BROKEN looks like:** with the hold full and two exports configured, the lander gets
  stuck reading **"loading" forever** and the automated rocket just sits on the pad and
  never departs.
- **FIXED looks like:** the hold fills, the status advances to **"ready"**, and the
  lander departs on schedule.
- ⚠️ **This is the known-suspect case** (the requested floor may not debit remaining
  hold capacity, so an alphabetically-earlier resource's request can exceed what's
  left). **If it sticks at "loading", that is a real FAIL and needs a code change** —
  record the exact export pair, the hold contents and the status text.

`Result (ratchet):` _____________________________________________

`Result (capacity edge):` _____________________________________________

---

## PT-18 — Arrival deaths, including the elevator / multi-map path · covers **F53**

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

---

## PT-19 — Shelter reflex on an asteroid · covers **F73**

**Setup:** SAVE-E, on the **asteroid**: a **MicroG Habitat** with 2–4 colonists living
in it, and a mine they work.

**Trigger:**
1. `CheatToggleInfopanelCheats()` to get per-building levers.
2. **Cut the habitat's life support / power briefly** (a few game minutes), so colonists
   momentarily lose their residence, then restore it.
3. Run 1–2 sols at ultra speed and watch the colonists during their **idle** stretches
   (not their shifts — they're safe inside the mine while working).

- **BROKEN looks like:** after a momentary life-support blip the colonists are
  permanently homeless, wander around **outside on the asteroid surface**, and bleed
  health past the oxygen timer until they die — while an empty habitat sits right there.
- **FIXED looks like:** (a) the habitat **takes them back** as residents even though its
  life support had a gap, and (b) if a colonist is still outside past half the oxygen
  budget in vacuum, they **head indoors to rest** instead of loitering.

`Result (a — habitat re-accepts):` _____________________________________________

`Result (b — seeks shelter):` _____________________________________________

---

# Group 6 — wave-3 fixes

## PT-23 — Station resource switches vs. train unloading · covers **F46**

**Setup:** SAVE-A. Build a **three-station Martian Express line** A — B — C on one
track (`CheatCompleteAllConstructions()`), assign 1–2 trains, and let the line run
for a sol so routes are established. Then:

1. `CheatFillAllStorages()` — every depot **and station** now holds everything.
2. Open **station B**'s infopanel and switch **Metals OFF** (the per-resource
   accept toggles). Leave Metals **on** at A and C.
3. Note B's Metals stock, then run 3–4 sols at `SetGameSpeedState("ultra")`.

- **BROKEN looks like:** B's Metals count never settles. Trains haul the forbidden
  Metals out (correct) and then **bring Metals straight back in** at the next stop,
  because unloading ignores the switch entirely. The count sawtooths up and down
  for the rest of the game and the line is permanently busy moving one resource in
  circles.
- **FIXED looks like:** B's Metals drains to **0 and stays there**. Trains still
  carry Metals *through* B on their way to A/C, they just don't drop it off.

**Stranding check (the thing this fix could plausibly break):** while the line runs,
watch for a train **parked at a platform with cargo it never unloads**. Select a
train and read its cargo. Also switch Metals **off at all three stations** for one
sol — a train holding Metals must still be able to empty itself (nowhere accepts it,
so the dump is deliberately allowed) rather than sitting loaded forever.

`Result (ping-pong stopped?):` _____________________________________________

`Result (no stuck loaded trains?):` _____________________________________________

---

# Group 7 — cross-cutting (do these last, every session)

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

`Result:` _____________________________________________

---

## PT-21 — Long-save soak

**Setup:** any healthy colony (SAVE-A or SAVE-E is fine). All 30 fixes active —
confirm with `SMRFixPack.ListFixes` (all should say `applied`).

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
   PASS/SKIP pattern as the last A/B run — the 10 `[install]` probes SKIP on retail,
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

## PT-22 — Log hygiene (run after EVERY session, including every test above)

**Where:** `%AppData%\Surviving Mars Relaunched\logs` — take the newest
`Mars.exe-<date>-<time>.log`.

**Check for:**
1. Any line containing **`[CommunityFixPack]`** with the word `error`, `inactive`, or a
   deactivation reason. (Startup lines reporting fixes as `applied` are normal.)
2. Any **`[LUA ERROR]`** block whose stack mentions a file under `SMR-BugFixPack\Code\`.
3. Any `[LUA ERROR]` in shipped game code that you did **not** see in a vanilla session
   — note the file:line even if it looks unrelated to us.
4. `SMRFixPack.ListFixes` output at load: **all 30 should say `applied`**. Any
   `inactive` line means a fix silently self-deactivated (its apply() self-check failed)
   — that is a FAIL and needs reporting with the reason string.

Paste anything suspicious verbatim into your result line — the exact text matters more
than a summary.

`Result:` _____________________________________________

---

## Commands cited in TESTING.md that could NOT be verified — do not use

| Cited as | Verdict |
|---|---|
| **`hr.TimeScale`** (TESTING.md, F02 scenario: "set game speed high (cheat/`hr.TimeScale` — verify name)") | ❌ **UNVERIFIED / does not exist.** No `hr.TimeScale` anywhere in `ModTools\Src`. Use the verified `SetGameSpeedState("ultra")` (`Lua/X/HUD.lua:528`) or `UIColony:SetGameSpeed(20)` (`Lua/Colony.lua:564`) instead. |
| **Cheat keyboard shortcuts** (Alt-B for complete-all-constructions, Alt-Shift-A for asteroid unlock, etc., as listed in CHEATS_INVENTORY.md) | ⚠️ **Real in source but NOT bound on retail** — the whole shortcut tree is behind `local cond = Platform.cheats` (`Lua/XDef/GameCheatShortcuts.generated.lua:19-20`). Type the function call in the console instead. Every command in the reference table above is a verified callable function. |
| **`CheatStartMystery(id)`** | ⚠️ **Real (`Lua/Mysteries/Mysteries.lua:91`) but self-gated** on `Platform.cheats` (`Lua/Cheats.lua:1-3`). Use the new-game mystery pick, or the explicit `Platform.cheats` flip documented in PT-15. |
| **"Fast-forward game time by an interval"** | ❌ No such cheat exists (confirmed in CHEATS_INVENTORY.md "Not found — do not look again"). Use `SetGameSpeedState("ultra")` and wait. |

Everything else prescribed in this document was verified to exist in
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` at the file:line cited.

---

## Reporting protocol

**Tester (you):**
1. Fill in every `Result:` line — `PASS` / `FAIL` / `SKIP (reason)` — plus free-text
   notes and the **date**. Screenshots for anything visual (especially PT-03's curve
   check and PT-10).
2. Commit this file, or simply tell the next Claude session:
   **"read PLAYTEST_CHECKLIST.md results"**.

**Next Claude session — do exactly this:**
1. Read this file's `Result:` lines.
2. For every fix whose covering test(s) **PASSed**, flip its status to `tested`
   in `docs/BUGS.md` — **both places**:
   - the **index row** (`| F0x | … | fixed |` → `tested`), and
   - the **detail heading tag** (`` `[fixed: Code/Fix_X.lua]` `` → `` `[tested: Code/Fix_X.lua]` ``).
   A fix covered by more than one test (F44/F45, F67/F69) only goes `tested` when **all**
   its results pass. Partial fixes (F03, F15, F52, F55, F58 — marked `fixed*`) go to
   `tested*` and keep their open-half note.
3. Move the corresponding lines in `docs/MOD_DESCRIPTION.md` into the shipping fix list
   if that file segregates tested vs untested (only `tested` fixes ship in the final
   player-facing text — STATUS.md, header).
4. For every **FAIL**, do **not** flip the status. Instead:
   - record it as a **new finding** in `docs/BUGS.md` (new detail entry + index row, or
     an appended note on the existing entry if it's a regression of that same fix),
   - set the affected fix back to `todo`/`blocked` as appropriate with the tester's
     verbatim observation quoted,
   - add it to the "Next up" queue in `docs/STATUS.md`.
5. For **PT-10 (F55)**, whichever way it lands, record the observation on the F55 BUGS.md
   entry and resolve the open question in STATUS.md's "Waiting on the user" item 4.
6. Update the STATUS.md implementation header (currently "30 fixes DONE (probe-verified…;
   scenario `tested` passes still pending)") to reflect the new tested count.
7. Commit everything in one change, with the playtest date in the message.
