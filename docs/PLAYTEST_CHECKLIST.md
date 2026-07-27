# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next Claude session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

**Completed tests live in [PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md)** — done so
far: PT-01, PT-02, PT-03, PT-04, PT-05, PT-07, PT-08, PT-12, PT-13, PT-34,
PT-36, PT-38, PT-41, PT-45, and PT-46's F49(b) half. This
file carries only un-run work; when a test completes, its whole section (with
the result notes) moves to the archive.

## Why this document exists

The **30 wave-1/wave-2 fixes already passed the automated script probes** — the final
A/B RunAll pair flipped **19/19 discriminating probes FAIL→PASS** with zero FAILs and all
30 fixes reporting `applied` (STATUS.md → "FINAL A/B RunAll pair"). That proves the
*wiring*: the patched functions are installed and return the right values when
driven with synthetic input.

The **9 wave-3 fixes (PT-23 … PT-31, group 6)** have probes but **no A/B run yet**, so for
those this checklist is the first real evidence of anything. Run `SMRTest.RunAll` once
before starting group 6 and note any FAIL/ERROR lines.

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

### Cheating without contaminating results

Cheat the **setup**, never the **mechanism under observation**. The fixes patch
decision logic; cheats inject state (money, goods, people, buildings) — state
injection is exactly what the scenarios need. Each PT's Setup line names its
cheats; when one must stay OFF, the PT says so. Standing accelerators — use
freely: `CheatAddFunding`, `CheatCompleteAllConstructions`, `CheatFillAllStorages`,
`CheatResearchAll`, `CheatSpawnNColonists`, `CheatUpdateAllWorkplaces`,
`dbg_ToggleRocketInstantTravel`, `CheatToggleInfopanelCheats`, `MultiCheat`.
Four specific cautions:

- **PT-38** ~~runs on wall-clock time~~ **CORRECTED 2026-07-27 (measured live):** the
  dismissal window is **120,000 GAME-ms = 4 game hours** (`GameTime` defaults true on
  the preset), so it only *looks like* 2 real minutes at normal speed — higher game
  speed SHORTENS the wait (seconds at ultra).
- **PT-36**: run its three console calls **before** any `CheatAddFunding` in that
  sitting — cheat funding flows through the income-recording path the test reads.
- **PT-17/PT-32**: fill storages / instant travel freely (both prescribed), but do
  not hand-edit the lander's cargo request mid-observation — the request math IS
  the test subject.
- **PT-10 / F55**: use `OpenAllDomes()`, not `CheatOpenAllDomes()` — the Cheat
  variant also maxes terraforming params and muddies the observation.

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
| `CheatToggleInfopanelCheats()` | `Lua/Cheats.lua:290` | shows per-building cheat buttons — ⚠️ **on retail the buttons render but silently NO-OP** (they dispatch `NetSyncEvents.ObjCheat`, gated `AreCheatsEnabled()`, `Network.lua:218-219`; found live 2026-07-27). Either run `Platform.cheats = true` first (buttons work; set false after), or skip the panel and call the method directly on the selection: `SelectedObj:CheatMalfunction()` / `CheatAddMaintenancePnts()` / `CheatCleanAndFix()` (`Building.lua:1813-1849`). Second gotcha (2026-07-27): button presses ride the game-time sync queue (`ScheduleOfflineSyncEvent`) — they look DEAD while the game is paused and fire on unpause; the `ObjCheat <method>` console print confirms delivery |
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

> PT-01..PT-05 are DONE and archived in PLAYTEST_ARCHIVE.md. PT-01's passive
> silence-watch continues in the background — the watchdog self-reports
> (`WATCHDOG — Meteors thread silent …`) if the meteor wedge ever recurs; if
> you see that line in the log, report it verbatim.

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

## PT-24 — Universities after Extractor AI · covers **F36**

**Setup:** SAVE-A. You need **Metals Extractors on the map** (not Mines — the tech
targets `MetalsExtractor` / `PreciousMetalsExtractor`) and a **Martian University**.

1. `CheatMapExplore("deep scanned")`, build 2–3 **Metals Extractors** on deposits and
   `CheatCompleteAllConstructions()`. Leave them **staffed and working** for a sol so
   they are `ui_working`.
2. Build a **Martian University**, set specialization to **Auto** and training policy
   to **"train as needed"**. Feed it unspecialized colonists (`CheatSpawnNColonists(20)`).
3. Read the university's infopanel **needed-specializations list** and note it.
4. Now research the **Extractor AI** breakthrough. On a retail build the simplest route
   is `CheatResearchAll()` (it grants breakthroughs too); confirm afterwards that the
   extractors show **Automation** in their infopanel and keep working with their
   workers removed.
5. Re-read the university's needed-specializations list, then run 3–4 sols at
   `SetGameSpeedState("ultra")` and watch what it graduates.

- **BROKEN looks like:** after Extractor AI the extractors run themselves, but the
  university's list still shows a large **geologist** demand (4 per shift per
  extractor) and "auto" keeps graduating geologists — while the specialists you are
  actually short of never get trained.
- **FIXED looks like:** geologist demand from the automated extractors **drops out of
  the list** the moment the tech lands, and "auto" starts training whatever the colony
  is genuinely short of. Manned workplaces (medics for the Medical Centre, botanists
  for farms, and geologists for ordinary **Mines**, which are not automated) still
  appear in the list normally.

> Sanity check on over-reach: with Extractor AI researched, an **unstaffed** extractor
> must NOT raise a "needs workers" warning, and a Mine (no automation) must still ask
> for geologists.

`Result (geologist demand gone?):` _____________________________________________

`Result (other specialists still trained?):` _____________________________________________

---

## PT-25 — Destroyed tunnel after a reload · covers **F38**

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

---

## PT-26 — Second Artificial Sun · covers **F39**

**Setup:** SAVE-A with `MultiCheat()` + `CheatAddFunding(500000000)` (the Artificial
Sun is a late-game building and needs Water).

**Trigger:**
1. Build **Artificial Sun #1** somewhere, and a Solar Panel next to it.
   `CheatCompleteAllConstructions()`. Confirm the panel's infopanel shows the
   Artificial Sun bonus (its power output is higher than a panel out in the dark,
   and it keeps producing at night).
2. Build **Artificial Sun #2** far away, out of range of everything.
3. Now build **new Solar Panels around sun #2** and complete them. **Order matters** —
   the panels must be built *after* the sun.
4. Compare a panel next to sun #2 with a panel next to sun #1, and with one in
   neither's range. Night is the clearest comparison.

- **BROKEN looks like:** the panels around sun #2 behave as if there were no sun at
  all — no bonus, no night production — while the identical panels around sun #1 are
  fine. (Panels that were *already standing* when sun #2 was built do work; that
  direction was never broken.)
- **FIXED looks like:** panels around sun #2 produce exactly like panels around sun #1.

**Existing-save check:** if you have a save that already has this problem, load it with
the pack enabled and look for `[CommunityFixPack] SecondArtificialSun: reconnected N
solar panel(s)` in the log — those panels should start producing immediately.

`Result:` _____________________________________________

---

## PT-27 — Dust Sickness does not infect Biorobots · covers **F40**

**Setup:** SAVE-A. You need **Biorobots** and a **dust storm**. Biorobots come from
the Biorobots tech/resupply — `CheatResearchAll()` then spawn a batch and check the
colonist list for the **Biorobot** trait; if you cannot get any, write "could not set
up" and skip the F40 half.

**Trigger:**
1. Note which colonists are Biorobots.
2. Wait for (or wait out) a **dust storm** with the "Dust Sickness" event active —
   the game rule **Dust In The Wind** is a prerequisite, so this needs a save started
   with that rule if the event has not fired yet.
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

---

## PT-28 — Dust Sickness damage spread · covers **F17**

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

---

## PT-29 — Gene Forging · covers **F41**

**Setup:** SAVE-A. This one is mostly a console read — the effect is statistical and
not worth grinding out by eye.

**Trigger (console), before researching anything:**
```
*r local u = MainCity.labels.Colonist[1] ConsolePrint("rare bonus: " .. tostring(GetRareTraitChance(u)))
```
Then grant **Gene Forging** on its own — `UIColony:SetTechResearched("GeneForging")`
(`Lua/Research.lua:276`) — and re-run the line. Then grant `"GeneSelection"` as well and
re-run it a third time. (`CheatResearchAll()` would grant both at once and hide the
isolated reading.)

- **BROKEN looks like:** `rare bonus: nil` with Gene Forging researched, and `100` once
  Gene Selection is researched no matter what else you have.
- **FIXED looks like:** `50` for Gene Forging alone, `100` for Gene Selection alone,
  `150` with both.

**Optional feel check:** with both researched, generate a big applicant batch
(`CheatGenerateApplicants(100)`) and eyeball how many carry rare traits versus a
pre-research batch. Statistical, so only note it if it looks obviously wrong.

`Result:` _____________________________________________

---

## PT-30 — Finished Mirror Sphere site · covers **F16**

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

---

## PT-31 — Edit Payload sticks · covers **F70**

**Setup:** SAVE-E. An **Asteroid Lander** on the Mars pad, in **manual** mode (not
automatic), with an asteroid destination selected. `dbg_ToggleRocketInstantTravel()`.

**Trigger:**
1. Open **Edit Payload**. A brand-new lander should show the policy defaults
   (roughly 5 Drones, 20 Metals, 5 Polymers, 5 Machine Parts, 5 Electronics and a
   few extractor prefabs) — that prefill is intended and must still happen.
2. Set **Metals to 0** and everything else to whatever you actually want. Confirm.
3. **Re-open Edit Payload immediately.** Metals must still be 0.
4. Let the lander fly, land and unload. Open **Edit Payload** again.

- **BROKEN looks like:** Metals is back at 20 in step 3 — and after step 4 the whole
  policy template has reappeared, so the lander loads a cargo you never asked for.
- **FIXED looks like:** what you set is what you see, in step 3 and after the round
  trip in step 4.

> Note the intended prefill in step 1 is the check that this fix is not over-broad —
> if a *fresh* lander shows an all-zero payload, that is a FAIL too.

`Result (row stays empty?):` _____________________________________________

`Result (fresh lander still prefilled?):` _____________________________________________

---

## PT-32 — Auto-export loads the valuables first · covers **F71**

The probe proves the allocation order in isolation; only play shows what actually
ends up in the hold when drones, stock levels and the one-sol departure timer all
compete. Do this straight after PT-17 — same save, same lander.

**Setup:** SAVE-E, lander on an **asteroid** in **Automated Mode**.
`SMRTest.Log.AutoCargo(true)`.

**Trigger:**
1. Make sure the asteroid has a large stock of a **bulk** resource (Waste Rock,
   Concrete or Metals) *and* a smaller stock of **Rare Metals / Exotic Minerals**.
   `CheatFillAllStorages()` on the asteroid side is the quick way.
2. Set export thresholds so **both** the bulk resource and the valuables are
   exported (threshold 0 / "export anything above" on each).
3. Read the next `CreateAutoCargoRequest(...) request{...}` line, then let the
   lander load and depart.

- **BROKEN looks like:** the request is dominated by whichever resource comes
  first **alphabetically** — Concrete/Metals ahead of PreciousMetals and
  PreciousMinerals, and Waste Rock still getting a share. The lander leaves on the
  one-sol timer full of bulk while the valuables sit on the ground.
- **FIXED looks like:** the request lists **PreciousMinerals, Electronics,
  PreciousMetals, MachineParts** first and only spends what is left on Polymers,
  Food, Fuel, Metals, Concrete and finally Waste Rock. The lander arrives on Mars
  carrying the valuables.

> Not over-broad: with the hold big enough for everything, **every** configured
> export must still appear in the request. A resource that disappears entirely is
> a FAIL.

`Result (order):` _____________________________________________

`Result (nothing dropped when there is room for all?):` _____________________________________________

---

## PT-33 — "No available Asteroid Landers" with a lander on the pad · covers **F72**

This one is pure UI flow — the probe proves the predicate, only play proves the
button behaves.

**Setup:** SAVE-E. **Exactly one** Asteroid Lander, on the Mars pad, **manual**
mode, **no destination assigned**, and a scanned asteroid available in the
Planetary View.

**Trigger — case A (the reported case):**
1. Land the lander with cargo aboard and **do not let it finish unloading** —
   pause, or take the drones away so unloading stalls. Its status should read
   *unloading*.
2. Open **Planetary View → the asteroid → VISIT ASTEROID**.

- **BROKEN looks like:** the "No available Asteroid Landers" popup, offering to
  open the Resupply screen — while the lander is visibly parked on the pad.
- **FIXED looks like:** the rocket picker opens and the lander is in the list.

**Trigger — case B (maintenance):**
3. Let a landed lander fall due for maintenance (or wait for one to). With its
   status showing it is waiting for parts, repeat step 2.
- Same expectation as case A.

**Trigger — case C (not over-broad — the important negative):**
4. Assign the lander a destination and confirm a payload so it is **loading for a
   flight**. Repeat step 2.
- **Expected:** you still get "No available Asteroid Landers" (or an empty list).
  A rocket already committed to a flight must NOT be offered for a second
  expedition. If it is, that is a FAIL.
5. With **no lander at all** (send it away, or a save that has none), repeat
   step 2 — the popup must still appear.

`Result (case A unloading):` _____________________________________________

`Result (case B maintenance):` _____________________________________________

`Result (case C committed lander / no lander still refused?):` _____________________________________________

---

## PT-35 — Save sanitizer passes · covers **F35, F03 (sweep half)**

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
4. Follow PT-02 to build + upgrade + salvage a Medical Center **with the fix pack
   disabled**, so a bonus really leaks. Save.
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

---

## PT-37 — F48 unblock test · decides whether the **F48** repair can ship

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

---

# Group 8 — wave-4 fixes

## PT-39 — RC Transport vs. a visiting rocket · covers **F74**

Probes prove the guard refuses a trade rocket; only play can show the cursor and
the order behave as they should, and that nothing ELSE the RC Transport does got
caught by the same net.

**Setup:** a save where a trade rocket or a refugee rocket is landed (rival-colony
trade offer, or the refugee story event). Have an RC Transport with some cargo
aboard and some free space, parked near it.

**Steps:**
1. Select the RC Transport and hover the cursor over the landed **trade/refugee**
   rocket, both in plain move mode and with the Load and Unload interaction modes.
   - **EXPECTED:** no "Load Resource" / "Unload Resource" prompt appears, and
     clicking does not send the rover to the rocket (it should read as ordinary
     terrain — a move order, or nothing).
   - **SURPRISE looks like:** the prompt still appears, or the rover drives over
     and starts a transfer.
2. Try to start a **transport route** whose source or destination is that rocket.
   - **EXPECTED:** the rocket cannot be picked as either end.
3. **Control test — this must still work.** Hover the same RC Transport over a
   normal **player** rocket or asteroid lander that is landed with cargo, and over
   an ordinary Universal Storage Depot.
   - **EXPECTED:** Load/Unload prompts appear as before and the transfer runs.
     If this broke, the fix is over-broad — report it, it is worse than the bug.
4. Check the log for `[CommunityFixPack] RocketInteractGuard: applied`.

`Result (trade/refugee rocket refused?):` _____________________________________________

`Result (control test — player rocket + depot still work?):` _____________________________________________

---

## PT-40 — Train tunnel carries power · covers **F65**

The fix only acts when the two ends really are on different power grids, so this
test has to create that situation deliberately.

**Setup:** two separate power grids with no cable between them. On grid 1, a
Station; on grid 2 (far away, e.g. across terrain a cable can't cross), the other
end. Build a **Train Tunnel** pair linking the two areas and attach a station
**directly** to the tunnel entrance — close enough that the connecting track is
only one or two tiles long.

**Steps:**
1. Before completing the short track, note each side's power surplus/deficit
   (select a building on each grid; the two must read as separate grids).
2. Complete the short track so the station and tunnel connect.
   - **EXPECTED:** the two grids become one — the surplus/deficit numbers merge,
     and a shortage on one side is now fed by the other.
   - **SURPRISE looks like:** the track connects for trains but the grids stay
     separate.
3. Now **salvage the short track** again.
   - **EXPECTED:** the grids split back apart cleanly, no error in the log, no
     building left permanently unpowered that has its own supply.
4. Repeat step 2 with a **long** track (10+ tiles) between two stations — this is
   the path the game already handled; it must be unchanged.
5. Save, quit to menu, reload the save.
   - **EXPECTED:** the grids are still merged, and the log shows no errors from
     our PostLoadGame pass.

`Result (grids merge on connect?):` _____________________________________________

`Result (split cleanly on salvage / survive reload?):` _____________________________________________

---

## PT-42 — Last Transmission notices your reserves · covers **F22, F75**

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

---

## PT-43 — Numbers and tooltips trio · covers **F19, F20, F21**

Three small, independent reads. Any established colony will do — one with trains
and a few sols of history.

**F19 — Command Center graph caption.**
1. Open the **Command Center**, switch to the **Machine Parts** graph (Electronics
   works too), and look at the "Produced ... and Consumed ..." caption above it.
   - **EXPECTED:** the Consumed figure is in the same ballpark as the height of
     the Consumed bar — it now includes maintenance, which is most of your
     Machine Parts usage.
   - **SURPRISE looks like:** a near-zero figure beside a tall bar (the old
     behaviour), or a figure that is now clearly larger than the bar.
2. Sanity-check **Food**, where consumption is real and maintenance is nil — the
   number should be essentially unchanged from before.

`Result (Machine Parts caption vs bar / Food unchanged?):` _____________________________________________

**F20 — Morale tooltip.**
3. Find a colonist whose **Comfort** is high (green, at or above the high mark).
   Select them and hover the **Morale** stat.
   - **EXPECTED:** no "+Comfort" style bonus row is listed, and the rows shown
     add up to the Morale value in the title.
   - **SURPRISE looks like:** the bonus row is still there, or a row that SHOULD
     be there is gone.
4. Find a colonist whose **Comfort is low** (red) and hover Morale.
   - **EXPECTED:** the Comfort PENALTY row is still listed — that one is real.
     If it disappeared, the fix is over-broad; report it.
5. Hover Morale on a colonist with high **Health** or **Sanity**.
   - **EXPECTED:** those bonus rows are untouched.

`Result (high-Comfort row gone / low-Comfort row kept / Health+Sanity intact?):` _____________________________________________

**F21 — Train waiting time.**
6. Pick a station where colonists queue for a while. Select a colonist about to
   travel, note their **Comfort**, and watch them wait, board, ride and arrive.
   - **EXPECTED:** the Comfort drop on arrival reflects the ride, not the wait.
     A long wait followed by a short hop should cost little.
   - **SURPRISE looks like:** a big Comfort hit after a long wait and a one-stop
     ride.
7. Open the **train's** and the **track's** infopanels and check the travel/spent
   time statistics over a few sols.
   - **EXPECTED:** they no longer include platform waiting (the station's own
     waiting statistic still does, and should be unchanged).

`Result (Comfort hit matches the ride / train+track stats exclude waiting?):` _____________________________________________

---

## PT-44 — Founder trait notice and dome pipe cleanup · covers **F23, F24**

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

---

# Group 9 — wave-5 fixes

## PT-46 — F49 tail: train cap + instant-track palette · covers **F49(d), F49(a)**

The main half of this test — splitting a track under a running train, F49(b) —
PASSed 2026-07-26 and is archived in PLAYTEST_ARCHIVE.md (resolved as no-defect:
the engine stores the train back as a prefab). Two small checks remain:

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

## PT-47 — Bombardment volley shape · covers **F26**

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
4. `SMRFixPack.ListFixes` output at load: **all 39 should say `applied`**. Any
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
8. Move each completed test's section — test text plus the filled-in results —
   from this file into `docs/PLAYTEST_ARCHIVE.md`, so this checklist only
   carries un-run work.
