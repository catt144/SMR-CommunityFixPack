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
5. ⛔ **NO live UI-internals prototyping in a play session — HARD RULE**
   (relocated 2026-08-04 from the standing prompt; the story was living there
   as an F76 block long after F76 closed). The 2026-07-27 hard-lock
   (`XWindow:SetVisibleInstant` on a destroyed window, every mouse event
   erroring, Alt-F4) happened under a wrapper that **MUTATED `align_pos`**.
   The one sanctioned pattern, used by the chain-11 sitting: **read-only
   hooks** — call `orig` first, print, mutate nothing. Anything more is a
   MarsDebug/fixture job, never a live colony.
6. If a step's setup fails, write that down. "Could not set this up" is a valid and
   useful result.
5a. ⭐ **ON A ONE-OFF CHECK THE DEFAULT IS A WARMED-UP SAVE, NOT AN AS-SAVED ONE — this
   governs how a rider must be WRITTEN** (owner, stated directly 2026-08-02). Before a
   **one-off** test the owner **nearly always plays the save organically for 20–30
   minutes**, deliberately, *"setting things up so that there is activity, and log
   noise, things happening before a test"* — **unless the instruction says not to.**
   ⚠️ **This is a DIFFERENT practice from the hours of solo provisioning that precede a
   new heavy-playtest setup — the two are not additive, and which applies depends on
   what you asked for.** A single dump or single observation is the one-off case.
   Three consequences, all binding on whoever authors a check:
   - **If you need the AS-SAVED state, say so explicitly** ("take this within the first
     minute of load, before playing"). A bare "load the save and read X" will normally
     be read against a warmed-up colony, and for state-dump checks that is a different
     measurement.
   - ⛔ **Never write "play for a while first to generate activity."** That is already
     the default; asking for it wastes the owner's time. State only the *deviation*.
   - **Record which one the reading actually got, and do not credit a warm-up the
     instruction suppressed.** A cold dump rests on the save's accumulated history; a
     warmed one also has live play behind it. Both are real evidence; they are not the
     same claim. (Worked example: the C26 dumps of 2026-08-02 were taken ~1 minute after
     load *because the instruction said to* — their strength is the colony's 288 sols of
     history, not live play during the reading.)
7. **The console AUTO-OPENS shortly after a colony is up — loads AND new
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

**Sanctioned speed techs** (relocated 2026-08-04 from the standing prompt):
`AdvancedDroneDrive`, `LowGDrive`, `MartianAerodynamics` — setup accelerators
with no bearing on any fix under test. Everything else: judge by the rule
below.

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
- ⛔ **Read the LOG FILE, never the screen, and make `nil` visible** (adopted
  2026-08-04, from the first campaign sittings): two live explanations from
  on-screen readings were wrong and the log refuted both. A bare console
  expression that renders as empty is NOT a reading — wrap uncertain reads as
  `print_format("label: <1>", tostring(expr))` so a `nil` arrives as a token
  you can see and quote.
- ⛔ **An OS-side measurement from a non-DPI-aware process is not a
  measurement** (same failure shape as reading the screen; added 2026-08-04,
  co-run #1). A PowerShell `System.Windows.Forms.Screen` read at 150% Windows
  scaling returned logical units (`2560×1440` for a `3840×2160` display) and
  briefly produced a false three-way coordinate mystery. Monitor geometry
  comes from the Windows display settings readout or a DPI-aware tool — never
  from a default PowerShell process. (`agent/facts/EF-046`.)
- **ONE command per line** — a pasted multi-line block silently concatenates
  into one line and fails `not understood`. And `not understood` means the
  line did not COMPILE — overwhelmingly a `--` comment inside a `*r`/`*g`
  snippet (they splice onto one line); never write a console snippet with a
  trailing comment. Bare expression for simple reads; `*r`/`*g` for
  multi-statement snippets and assignments (an assignment is not an
  expression).
- **`ModLog(...)` is the ONLY path proven to reach the log file**; the buffer
  flushes at exit, and `FlushLogFile()` forces it mid-session.
- **Runtime console wrappers must target the LEAF class** (pre-build patches
  propagate through flattening; runtime ones do not — `EF-002`).
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
- ⛔ **`ConsolePrint` takes exactly ONE argument, and it must be a string**
  (`CommonLua\LuaExportedDocs\Global\LuaSharedLib.lua:7` — a native binding,
  `function ConsolePrint(text)`). **A multi-argument call, or one passing a
  number, prints NOTHING AND REPORTS NO ERROR.** Found the hard way 2026-08-02
  (PT-61): a setup-confirmation line passing eight numbers produced pure silence
  and read as a console that had stopped responding. Wrap the values in
  **`print_format(...)`** (`CommonLua\Core\lib.lua:95`) — which is exactly what
  the console's own expression rule does — or concatenate into one string
  yourself:
  `*r local p = … ConsolePrint(print_format(p.a, p.b, p.c))` ✅
  `*r local p = … ConsolePrint(p.a, p.b, p.c)` ⛔ silent no-op
- **Prefer a bare expression over `*r ConsolePrint(...)` for a simple read.**
  Rule `{ "(.*)", "ConsolePrint(print_format(%s))" }` (`uiConsole.lua:363`)
  wraps ANY input that compiles as an expression, so typing
  `GetRareTraitChance()` prints its value by itself. `*r` is only needed for
  multi-statement snippets or ones that must not block.
- `g_Consts` is a **GameVar** — it does not exist at the main menu. Run everything
  from inside a loaded colony.
- **The bare console has NO thread context** (measured 2026-08-01, Tier-1
  sitting): a bare `SMRTest.RunAll()` executes straight from `ConsoleExec`, so
  `CurrentThread()` is falsy inside probes. Probes that need a real thread
  identity (the F02 keyed-wrapper sub-check) skip with a note. **Run
  `*r SMRTest.RunAll()` for full probe coverage.**
- **Log-flush discipline for unattended log reading** (2026-08-01): TestKit
  `[SMRTest]` lines flush to disk per line; the PACK's `[CommunityFixPack]`
  lines and ConsolePrint output do NOT — they sit in the buffer until exit.
  When someone reads the log while the game runs, flush first:
  `FlushLogFile()` (bare call works; `*r pcall(FlushLogFile)` is the guarded
  form).

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
| `CheatMeteors("single"\|"multispawn"\|"storm", setting, pos)` | `Lua/Cheats.lua:62` | meteor strike. **AIM IT AT THE MOUSE (added 2026-07-30 — this is the form you usually want):** `pos` is the **THIRD** argument, so you cannot just append it — pass `nil` for `setting` to keep the map default. Fire at the pointer, with 3 real seconds to aim first (your mouse is over the console when you press Enter, so a bare call would strike there): `*r Sleep(3000) CheatMeteors("single", nil, GetTerrainCursorClamped())`. `GetTerrainCursorClamped()` (`CommonLua/Classes/MapData.lua:25-30`) is safer than raw `GetTerrainCursor()` — it clamps into the play area so an off-map cursor cannot hand you a bad position. To hit a SPECIFIC building instead, select it and skip the mouse: `CheatMeteors("single", nil, SelectedObj:GetPos())`. `"single"` completes cleanly; `"storm"` is the one that wedges (below). The cheat drives the disaster directly, so it fires even under the **No Disasters** rule — by design, same as `CheatTriggerUndergroundMarsquake`. ⚠️ **RE-CORRECTED 2026-07-29 (QA session):** with no explicit `pos` it can silently do NOTHING — but the mechanism recorded earlier was wrong. `GetCameraLookAtPassable` is a **file-local helper** (`local function`, `Cheats.lua:42`) — invisible from the console *by design*, which is what the `attempt to call a nil value` probe actually proved; the shipped `Cheats.lua` is byte-identical to Src (full fpk diff, see agent/facts/). The real no-op path: the helper returns nil when no passable point exists within 100m of the camera look-at, and the body is `if pos then … end` with no else. **Always pass a position**, or drive the disaster directly: `*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`. Note `"storm"` reliably WEDGES (F78) — with the pack loaded, `Fix_MeteorStormWedge` heals it automatically ~2 game hours after the storm notification expires (**measured live 2026-08-01 on the Tier-1 REORDERED heal path**: `WEDGE confirmed` → scheduler restart → released through the VANILLA end path, `MeteorStormEnded` fired and F81's handler cleared the flag, heal logging last); manual recovery remains `*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end` |
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
| `CheatDustDevil(major, setting)` | `Lua/Cheats.lua:47` | dust devil at the camera look-at. ⭐ **A STATIC-CHARGED devil can be forced by deleting the lottery** — ✅ **`[RAN 2026-08-04, log `docs/archive/u1c5_Mars.exe-20260804-17.21.26.log`]`**, and **the recipe below is the CORRECTED one; the original was executed and it does not work.** The electro roll is `SessionRandom:Random(100) < descr.electro_chance` on a plain preset table (`DustDevils.lua:138`). ⛔ **What this row used to say — `local d = table.copy(Presets.MapSettings.DustDevils[…])` — RAISES.** Measured: **34 of 40 calls** threw `Lua/DustDevils.lua:134: attempt to perform arithmetic on a nil value (field 'duration')`. `table.copy` copies only **own keys**, and a `MapSettings_DustDevils` preset barely has any: `DustDevils_Low`'s `PlaceObj` data (`Data/MapSettings-DustDevils.lua:21-36`) sets only `SortKey`, `strength`, `spawntime*`, `spawn_chance`, `count_*`, `major_chance`, `major_minions_*`, `marker_*`. `duration` is a **class property default** (`8 * const.HourDuration`, `DustDevils.lua:13`) reached through the PropertyObject's `__index`, so the copy loses it. Two-sided control from the run: `table.copy(preset).duration=nil vs preset.duration=240000` and `table.copy(preset).electro_chance=nil vs preset.electro_chance=5` — direct indexing sees defaults, `table.copy` does not. **Build the descr by READING the fields instead:** `*r local b = Presets.MapSettings.DustDevils[CurrentMap.mapdata.MapSettings_DustDevils] or Presets.MapSettings.DustDevils["DustDevils_VeryLow"] local d = {} for _, f in ipairs{"duration","duration_random","speed","speed_random","movement_range","major_chance","electro_chance","electro_battery","devil_radius","devil_malfunction_radius","devil_dust","major_devil_radius","major_devil_malfunction_radius","major_devil_dust","major_minions_min","major_minions_max","major_minions_radius","colonist_health","drone_speed_down"} do d[f] = b[f] end d.electro_chance = 100 local dev = GenerateDustDevilIn(GetRandomPassable(CurrentMap), CurrentMap, d) if dev then dev:Start() end` — that form produced a devil on **attempt 1**, at the very position that had raised with the old recipe, which is what proves the descr and not the terrain was the fault. Confirmed off the object: `fx_actor_class=DustDevilElectro`, `drone_battery=5000`, still valid and still electro 20 s later. Do NOT use `GetCameraLookAtPassable` (file-local, invisible from console — see the meteor row). *(⚠️ Row corrected 2026-08-04 by `unattended-1` prompt 1, re-read against Src: the roll is `SessionRandom:Random(100)`, not the bare `Random(100)` this row said — conclusion unchanged, 0..99 `< 100` is always true, but the row named a function that is not on the line.)* ⛔ **Two things this row does not say and an UNATTENDED run needs:** `GetTerrainCursorClamped()` is useless with no one at the mouse — pass a chosen point (`GetRandomPassable(MainMap)`) instead; and `GenerateDustDevilIn` **returns nil early** when `VegetationAround(pos, map, range or 10*guim)` is true (`DustDevils.lua:129-131`), so a bad point silently produces nothing — retry and report the attempt count. ⚠️ **That early-out is real but it is a MINORITY cause and was very nearly mis-recorded as the whole story:** with the broken descr the accounting was **34 raises to 6 vegetation nils**, and a first probe that discarded `pcall`'s result reported all 12 of its failures as the vegetation early-out because a swallowed raise and a nil return print identically. Whatever calls this, **capture and print `pcall`'s error** — `VegetationAround` is file-local (`:114`) and cannot be called to check directly, so the raise/nil split is the only evidence available. Read the electro variant off the OBJECT, not the screen: `devil.fx_actor_class == "DustDevilElectro"` / `"DustDevilMajorElectro"` (`:152-154`), `devil.drone_battery` non-nil (`:148`) |
| `CheatDustStorm(storm_type, setting)` | `Lua/DustStorm.lua:540` | **force a dust storm NOW** — `storm_type` = `"normal"` / `"great"` / `"electrostatic"`; pass `setting` (a `Presets.MapSettings.DustStorm` key, e.g. `"DustStorm_High"`) for a deterministic start — with no `setting` and a storm already scheduled it only nudges the scheduler. Ungated (no `Platform.cheats` read in the body, unlike `CheatStartMystery`); calls `CheatStopDisaster()` first, so it ENDS the currently running disaster. ✅ **`[RAN 2026-08-04, log `docs/archive/u1c5_Mars.exe-20260804-17.21.26.log`]` — works exactly as this row describes, both halves confirmed and reproduced across two runs.** `CheatDustStorm("normal", "DustStorm_High")` on a save with no storm running (`g_DustStorm=false`, `stopped=true`) produced `g_DustStorm=<table>`, `type=normal` (i.e. the `storm_type` argument took), `stopped=false`, with real `start`/`end`/`duration` values — **within 0.5 s**, not the 3 min the leg was willing to wait. `StopDustStorm()` then returned it to `g_DustStorm=false`, `stopped=true`, also within 0.5 s. ⚠️ The one thing the deterministic form does NOT need is patience: budget seconds, not minutes |
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
| `SMRFixPack.ListFixes` | per-fix status. ⭐ **The denominator is the REGISTERED total, not the default-active one** — the leg line is `log("fix pack present: %d/%d fixes active", active, #SMRFixPack.order)` (`TestKit/Code/00_TestCore.lua:286`), so `#SMRFixPack.order` = **81** today. **Default config reads `74/81`**; a config with every opt-in toggled ON reads **`81/81`** — ⭐ **MEASURED 2026-08-03 on the owner's campaign: `fix pack present: 81/81 fixes active`, suite `78 PASS, 0 FAIL, 9 SKIP, 0 ERROR`** (log `Mars.exe-20260803-22.23.59`). The **8** `Opt_` modules read `inactive` unless toggled ON, except `DroneStatDials`, which is active-at-base = armed, vanilla behavior (`Code/00_Core.lua`). ⚠️ **Account state is READ, never assumed** — the owner's campaign currently runs every opt-in ON, which is NOT default config, so never compare a leg's number against another leg's without checking the toggles. `agent/STATE.md` holds the authoritative registered/default-active counts (`python tools/doccheck.py --emit-counts`). *(This row said `68/74` until 2026-08-03 — an era stale, and it was the row an agent consults before reading a live `ListFixes`. Corrected against a measured reading, not against arithmetic.)* |

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

### Harness quick facts (relocated 2026-08-04 from the standing prompt)

- **Baseline** = the fix-pack `metadata.lua` with an **emptied `code` list** —
  keep `default_options`; restore from a saved copy, NOT `git checkout`; never
  `git commit -a` while that edit is in the tree.
- **Probe-authoring:** every probe ends with an explicit `return "PASS", …`
  (nil → silent SKIP). Stand-in probes assert the MODULE's action, never
  vanilla bookkeeping around stubs.
- Launch timing: a leg ≈75 s but `Mars.exe` may take minutes to appear —
  never kill on a short timeout (25-min guard).

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

## The MarsDebug `[install]` pass — how to get the last 9 probes to report

**✅ EXECUTED ONCE, 2026-08-03 — the procedure is verified, not merely written**
(the standing rule: a test's own procedure is unverified until it has been run).
It produced **`87 PASS, 0 FAIL, 0 SKIP, 0 ERROR`** — the first complete probe
coverage this project has had. Log:
`docs/archive/logs/MarsDebug.exe-20260803-23.14.05-6a22b8b3.log`.

**Why it exists.** On retail, 8 `[install]` probes SKIP with `introspection
unavailable (retail sandbox)`: they call `SMRTest.SourceOf(fn)` to confirm the
patched function's source lives in the fix pack's folder, and `debug.getinfo` is
unreachable from mod code (`agent/facts/EF-010`). The console is sandboxed with
the same blacklist, so the bridge cannot be typed either — and `ConsoleExec` is
itself blacklisted, so it cannot be automated from mod code. **Only an asserts
build un-sandboxes the console** (`console.lua:36-44`), which is what makes this
leg possible at all. Rationale in `TestKit/Code/00_TestCore.lua:60-80`.

1. Game fully closed (`tasklist`). Arm **both**: uncomment
   `"Code/96_AutoRunFlag.lua"` in the TestKit metadata `code` list, AND
   uncomment `SMRTest_AutoRunSetupOnly = true` inside that file. SetupOnly is
   what makes it attended — the harness builds the colony, stops its watchdog,
   and hands over instead of running the suite and quitting
   (`95_AutoRun.lua:293-296`).
2. Launch via **Steam's own launch picker → "Play Surviving Mars: Relaunched
   (debugging mode for mod creators)"**. Leave "Always use this option"
   unticked. (Running `MarsDebug.exe` directly also works but skips Steam's
   environment setup; prefer the picker.) `-applaunch 3215050` starts
   **`Mars.exe`** and is the wrong path for this leg.
3. ⚠️ **EXPECT MODAL `Assert failed` DIALOGS, and expect more of them AFTER the
   `SETUP-ONLY: colony ready.` line prints.** Click **Ignore All** on every one
   (never Debug, never Exit Game); the asserts still reach the log. This is the
   one thing the written procedure did not warn about and it is why the leg kept
   getting deferred. They are **vanilla synthetic-map noise the retail build
   swallows silently** — the 2026-08-03 run had exactly TWO distinct asserts,
   `Flight.lua:465 objects_to_mark` and `Flight.lua:479 objects_to_unmark`, and
   every dialog was a repeat of those. No Lua switch suppresses them (the assert
   dialog is an engine binding). If they become unmanageable, PAUSE the game —
   the source is game-time rocket-flight code, and `*r SMRTest.RunAll()` runs in
   a real-time thread so it still executes while paused.
4. At the console:
   `SMRTest.EnableIntrospection(debug)` — **must print `true`.** Anything else
   and the leg is void: it would mean the asserts build's console is still
   sandboxed and `00_TestCore.lua`'s premise is wrong. Then
   `*r SMRTest.RunAll()` (the `*r` matters — a bare call has no thread context).
   Then `FlushLogFile()`.
5. **Disarm afterwards**: re-comment both lines.

### ⛔ NEVER read a MarsDebug tally as a retail tally

**The debug build's `87/87` is not a better version of retail's `78 PASS / 9
SKIP` — it is a DIFFERENT measurement, and for at least one probe a misleading
one.** `TechDescriptionBuilding` SKIPs on retail (`the tech has no description
T`) and **PASSes on MarsDebug** (`description names Underground Medium Dome`).
That is not the probe improving: it is **F98** — `T(id, text)` discards the
replacement literal in a non-dev build (`localization.lua:250-252`) but keeps it
in a dev build, so `Fix_TechDescriptionBuilding` genuinely works here and is a
no-op in the build players use. The probe therefore reports green in the only
environment where the fix works and is silent in the one that matters.
**Quoting "87 PASS" as evidence the pack is healthy on retail would be wrong,
specifically about F25/F98.** Retail coverage is `78/87` and the 9 that do not
report there are a known, enumerated set — that is the number to quote.

---

## The co-run rig — how an agent-driven launch actually runs

**✅ EXECUTED FOUR TIMES, 2026-08-04** (co-run #0 walking skeleton + co-run #1
runs 1–3) — every step below ran, none is merely written. Raw logs:
`docs/archive/corun0_*.log`, `corun1_*.log`, `corun1b_*.log`, `corun1c_*.log`.
Protocol rules (binding): `agent/WORKFLOW.md` "Co-runs" — this section is the
mechanics.

1. **Stage the save, game CLOSED:** `Copy-Item` the designated save (owner's
   pick: `TEST2H TRAIN`) to a new name in
   `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\`.
   The engine lists the copy by FILENAME (`CORUN0.savegame.sav` loads as
   `"CORUN0.savegame.sav"`); the display name inside is cosmetic. The campaign
   save is never written; the copy dies in the result commit.
2. **Arm at the sitting, not in prep** (probe hygiene rule 5): write the probe
   file into TestKit `Code/97_*.lua`, add its `metadata.lua` line, parse sweep.
   Arming measured at **0.4 s**; the parse sweep is location-independent, so
   prep sweeps the parked source. ⛔ The edit is a script FILE, never an inline
   PowerShell one-liner (rule C11 — an inline edit silently failed and a run
   launched unarmed).
3. **Launch:** `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050`
   — **no `-smrautorun`** (95_AutoRun stands down by itself). No Steam picker
   interposes: launch→log measured 1–5.2 s across four launches.
4. **Inside the probe** (patterns: the three co-run #1 harnesses, in git at
   `git show 93088ba:docs/agent/prompts/corun-rig/97_CoRun1.lua.txt`, `…1b…`,
   `…1c…`): real-time thread + own watchdog; per-line-flushed `ModLog` markers;
   poll `GetPreGameMainMenu()`, then `LoadGame("<COPY>.savegame.sav", {})` in
   the thread. **The loaded save arrives PAUSED** — set a speed
   (`UIColony:SetGameSpeed(3)`) before any game-time work, or it is dead on
   arrival. Readiness is synchronous with `LoadGame`'s return; **15 s settle is
   the measured-sufficient datum** (30 s bought nothing).
5. **Timing discipline:** the load is timed by the engine's own
   `Game loaded on map … in N ms` line, the cycle by `Time (ms)` at shutdown,
   the launch by OS timestamps. ⛔ Never print or trust `RealTime()` deltas
   across a loading screen (`agent/facts/EF-045` — 11.5× understatement).
6. **Cost shape, measured:** a cycle is **~30 s of fixed overhead + the
   payload** (menu poll 2.5 s, load stable 9.5–10 s on the 56 MB save, settle
   15 s, flush/quit ~1.5 s). Whole cycles ran 64 s / 80 s / 85 s / 398 s.
   Owner cost is the measure moments only — measured ~1.5 min (co-run #0) and
   ~6.5 min (co-run #1, three launches).
   ⭐ **Three numbers added 2026-08-04 by unattended-1 cycle 0** (log
   `docs/archive/u1c0_Mars.exe-20260804-16.37.16.log`; all read off the log's own
   `Lua H:MM:SS:mmm` markers, which DO survive a loading screen — `EF-045`):
   **(a) an in-run `SaveGame` of the 56 MB save costs 0.60 s** — the one cost
   nobody had measured, predicted at 10–20 s by analogy with the load, and the
   prediction was wrong by more than an order of magnitude, so save/reload legs
   are far cheaper to plan than assumed. **(b) A second load of the same map in
   the same process costs 5.9 s against the cold load's 10.1 s** — budget
   ~6 s, not ~10 s, for every load after the first. **(c) Boot to main menu is
   ~19.4 s of the cycle** and is the single largest fixed cost, which is the
   real argument for batching legs per launch rather than per cycle.
7. **Close-out:** delete the probe + its `metadata.lua` line + the staged copy
   in the commit that records the answers; `PROBE SWEEP:` line; archive any
   cited log with `git add -f`; **`git status` in BOTH repos** (WORKFLOW
   co-run close-out rule).

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
| *(Live colony)* | The long-running real colony — the standing watches, the wave-6 disaster work and the module partials all run there. (PT-54 was retired unrun 2026-08-01; the wave-6 disaster verification is now the F86 Tier-1 build's own legs.) | PT-52, PT-53, PT-42, PT-44, PT-46 tail, PT-47, PT-48, PT-35, PT-37 |

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
