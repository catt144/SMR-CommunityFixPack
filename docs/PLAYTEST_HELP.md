# Playtest Help — setup, commands, reference

## Must_Read_Header
<!-- RULES -->
Rule: Keep this file limited to reference material for running `PLAYTEST_CHECKLIST.md` and keep tests in the checklist. [A3: pass]
<!-- /RULES -->

This companion contains setup guidance, console facts, command references,
Test Kit helpers, stress-harness notes, and save-fixture recipes.

---

### Console: what works and what silently does nothing

The toolkit's console control was witnessed in sitting 02 with the Mod Manager
closed: disabling ConsoleEnabled and rebuilding removed DE_Console; arming
ConsoleEnabled and rebuilding restored it. The logged result was
`SMRTK_CONSOLE_CONTROL discriminates=true negative=false positive=true status=OK`,
with independent `SMRTK_SHORTCUT console=false` then `console=true` witnesses
(`agent/reports/SMRTK_SKELETON_SITTING.md`, step 2). Use Enter / Alt-Shift-C or
Kit → Open console after loading; opening before load is no longer a workaround.
The legacy auto-open/Ctrl-Alt-C fallbacks remain. Its bootstrap still calls
ConsoleSetEnabled first and can show the overlay at boot; the judge's order
inversion is owed to a code link, and F9 clears the overlay meanwhile.
Toolkit marks/copy/flush give attributed file evidence. 02 witnessed the native
console-line tap and clipboard, not every new page's behavior; 08 checks those.

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
  | `~<expr>` | opens the object inspector on `<expr>` — ⚠️ **static risk on retail, unwitnessed** (corrected 2026-08-05 by the terminal audit), see the warning below |
- ⛔⛔ **DEV TOOLS THAT THROW ON RETAIL — measured live 2026-08-05, entry `F101`.**
  Retail core code calls dev-only globals that a shipped build does not define,
  and the callers throw rather than doing nothing:
  - **The infopanel spot-visibility dev toggle.** Pressing it throws
    `CommonLua/GedGameObjectEditor.lua:104: attempt to call a nil value (global
    'GetSpotNameColor')` — stack: `Infopanel.lua(47) OnAction →
    ToggleSpotVisibility (GedGameObjectEditor.lua:64) → EditorShowSpots (:104)`,
    plus a paired `MouseEvent` re-entry of the same line. `GetSpotNameColor`
    lives only in `CommonLua/Libs/DevToolsPublic/debug.lua:359`, and that
    **entire library is absent** from a retail build — this is not a
    `Platform.cheats` gate, so no cheat flag turns it on. Witnessed 2×.
    ⛔ **CORRECTION 2026-08-05 (terminal audit):** this block first attributed
    the 2 throws to *opening the object inspector `~<expr>`*. The archived
    stacks say otherwise, and the session's one GedInspector open
    (`1:45:12–1:45:32`) was **clean** — and came AFTER both throws. The
    inspector claim is therefore **demoted to a static lead**: `:104` is in the
    inspector's own file, so treat `~<expr>` as risky, but nothing has measured
    it throwing.
  - **The `!` console prefix** (`uiConsole.lua:357` → `ShowMe(...)`) has the
    same shape — `ShowMe` is also `DevToolsPublic`-only. **Not yet witnessed**;
    recorded as a lead, do not cite it as measured.
  - **Infopanel `Meteor Hit` cheat buttons.** `TestMeteor` exists only inside
    `if Platform.cheats then` (`Meteors.lua:1086`) but three ungated callers
    invoke it, including `Building:CheatMeteorHit` on the **base class** — so
    every building's Meteor-Hit button throws. Witnessed 3×. The neighbouring
    **`Break Element`** button (`TrackGridElement:CheatBreakElement` →
    `BreakTracks`, ungated) **does work** — use `SelectedObj:CheatBreakElement()`
    when you need to damage a specific track element.
- **Historical vanilla infopanel finding, 2026-08-05:** the enabled vanilla
  wrapper reached TrackElement before throwing; a visible button did not imply
  retail debug services existed. The toolkit now calls supported leaves directly
  without that wrapper. ConsoleEnabled enables input, not AreCheatsEnabled or
  Platform.cheats. Use the toolkit section; never restore the old enable paste.
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
| `CheatToggleInfopanelCheats()` | Historical vanilla menu route (`EF-095`/`EF-097`) | Retired for toolkit playtesting. Use the SMR Tool Kit Selected section; the vanilla object wrapper records cheat taint. ConsoleEnabled does not enable that menu. |
| `CheatMeteors("single"\|"multispawn"\|"storm", setting, pos)` | `Lua/Cheats.lua:62` | meteor strike. **AIM IT AT THE MOUSE (added 2026-07-30 — this is the form you usually want):** `pos` is the **THIRD** argument, so you cannot just append it — pass `nil` for `setting` to keep the map default. Fire at the pointer, with 3 real seconds to aim first (your mouse is over the console when you press Enter, so a bare call would strike there): `*r Sleep(3000) CheatMeteors("single", nil, GetTerrainCursorClamped())`. `GetTerrainCursorClamped()` (`CommonLua/Classes/MapData.lua:25-30`) is safer than raw `GetTerrainCursor()` — it clamps into the play area so an off-map cursor cannot hand you a bad position. To hit a SPECIFIC building instead, select it and skip the mouse: `CheatMeteors("single", nil, SelectedObj:GetPos())`. `"single"` completes cleanly; `"storm"` is the one that wedges (below). The cheat drives the disaster directly, so it fires even under the **No Disasters** rule — by design, same as `CheatTriggerUndergroundMarsquake`. ⚠️ **RE-CORRECTED 2026-07-29 (QA session):** with no explicit `pos` it can silently do NOTHING — but the mechanism recorded earlier was wrong. `GetCameraLookAtPassable` is a **file-local helper** (`local function`, `Cheats.lua:42`) — invisible from the console *by design*, which is what the `attempt to call a nil value` probe actually proved; the shipped `Cheats.lua` is byte-identical to Src (full fpk diff, see agent/facts/). The real no-op path: the helper returns nil when no passable point exists within 100m of the camera look-at, and the body is `if pos then … end` with no else. **Always pass a position**, or drive the disaster directly: `*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`. Note `"storm"` reliably WEDGES (F78) — with the pack loaded, `Fix_MeteorStormWedge` heals it automatically ~2 game hours after the storm notification expires (**measured live 2026-08-01 on the Tier-1 REORDERED heal path**: `WEDGE confirmed` → scheduler restart → released through the VANILLA end path, `MeteorStormEnded` fired and F81's handler cleared the flag, heal logging last); manual recovery remains `*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end` |
| `CheatTriggerMarsquake(settings_name)` | `Lua/Marsquake.lua:223` | surface quake |
| `CheatTriggerUndergroundMarsquake()` | `Lua/Marsquake.lua:292` | underground quake (**bypasses** the scheduler on purpose — which is what makes it a sound positive control for any "no disasters" watch; PT-11, archived) |
| `CheatTriggerUndergroundCaveIn(pos)` | `Lua/Marsquake.lua:284` | cave-in at a position |
| `CheatStopDisaster()` | `Lua/Cheats.lua:74` | stop the running disaster |
| `CheatStartMystery(id)` | `Lua/Mysteries/Mysteries.lua:91` | **gated on `Platform.cheats`** — see PT-15 |
| `CreateGameTimeThread(function() SA_CallTradeRocketWithCargo:SARun{rocket_id="<id>", cargo=PlaceObj("ResourceCargoList", {Food=5000})} end)` | `Lua/Sequences/SA_Gameplay.lua:2831` | ✅ **[RAN 2026-09-11, F119 sitting]** summons an Earth-sent **Trade** rocket — the class Mysteries 7/8/9 send — with NO mystery running; needs a thread (`SAExec` ends in `Sleep(1)`). Lands wherever you put it. ⚠️ It launches the INSTANT its cargo reads ready (`EF-091`), so trigger anything while it is still loading. Per-object A/B from the same sitting: `rawset(obj, "<method>", fn)` shadows a class method for ONE object; remove it with `rawset(obj, "<method>", nil)` BEFORE any save — a function on a persisted object enters the save (`EF-022`). Record: `agent/bugs/F119.md` |
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

### Harness quick facts (relocated 2026-08-04 from the standing prompt)

- **Baseline** = the fix-pack `metadata.lua` with an **emptied `code` list** —
  keep `default_options`; restore from a saved copy, NOT `git checkout`; never
  `git commit -a` while that edit is in the tree.
- **Probe-authoring:** every probe ends with an explicit `return "PASS", …`
  (nil → silent SKIP). Stand-in probes assert the MODULE's action, never
  vanilla bookkeeping around stubs.
- Launch timing: a leg ≈75 s but `Mars.exe` may take minutes to appear —
  never kill on a short timeout (25-min guard).

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
