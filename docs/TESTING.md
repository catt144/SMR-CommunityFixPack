# Testing Plan — forcing bugs instead of waiting for them

Goal: verify each fix without hours of normal play. Three instruments, in order
of preference:

1. **Script probes** — call the patched function directly from the console (or
   test kit) and assert on the result. No gameplay needed. Many of our fixes
   are pure-function repairs and are 100% verifiable this way.
2. **Cheat-triggered scenarios** — the game ships its debug arsenal in plain
   Lua (`Lua\Cheats.lua`, `Lua\XDef\GameCheatShortcuts.generated.lua`, plus
   verified helpers like `CheatTriggerMarsquake`, `CheatTriggerUndergroundMarsquake`,
   `CheatTriggerUndergroundCaveIn` in `Lua\Marsquake.lua:223-304`). We can also
   mutate `g_Consts`/preset timings at runtime to compress hours into seconds.
3. **Targeted manual checklists** — for the few fixes that need real UI
   interaction, a precise 2-minute setup instead of open-ended play.

## The Test Kit (companion mod — never shipped to players)

**BUILT** — `C:\Dev\SMR-BugFixPack-TestKit` (own git repo; see its README).
Junction it like the main mod and keep it out of any upload. It enables the Lua
console at load (`ConsoleSetEnabled(true)` + `ReloadShortcuts()`; open with Enter
or Alt-Shift-C) and provides `SMRTest.RunAll()`, `SMRTest.List()`,
`SMRTest.<ProbeId>()`, the `SMRTest.Log.*` toggles and the `SMRTest.Report*`
state dumps. Probes are tagged by kind:

| Kind | Meaning |
|------|---------|
| `behavior` | drives the patched code with synthetic input — a real fixed/unfixed discriminator, no gameplay needed |
| `install` | asserts the patched function now comes from the fix pack (used where calling the real code would fire a disaster, complete a milestone, demolish a track…) |
| `state` | inspects the loaded savegame; SKIPs when the save has no relevant objects |
| `manual` | always SKIPs, with setup steps |

`install` probes work by reading `debug.getinfo(fn).source`; the F06 probe instead
uses `GetStaticMsgNames()`, since the shipped game registers no `CrystalFlyAway`
handler at all.

Original spec, for reference:

- `SMRTest.RunAll()` — console smoke suite: runs every script probe below,
  prints one PASS/FAIL/SKIP line per fix id. Run it (a) with fix pack disabled
  → expect FAILs proving each bug still reproduces, (b) with fix pack enabled
  → expect all PASS. That before/after pair is our regression harness for every
  game patch.
- `SMRTest.<FixId>()` — individual scenario drivers (below).
- Observability toggles: wrappers that log decisions we need to see (e.g. log
  every `ShouldLeaveForWork` verdict for shift-3 colonists for one sol; log
  each auto-cargo request the lander computes). Enable per-test, print to
  console/log with a `[SMRTest]` prefix.
- First build task: inventory `Cheats.lua` + `GameCheatShortcuts.generated.lua`
  — **DONE**, see `docs/CHEATS_INVENTORY.md`. It also answers the console
  question (Enter / Alt-Shift-C, gated on `AreCheatsEnabled() or ConsoleEnabled`;
  a Mod Editor test session grants it for free) and records which `Cheat*`
  functions self-gate on `Platform.cheats` (only `CheatStartMystery` and
  `CheatChangeMap`).

## Script probes (no gameplay; go straight in RunAll)

| Fix | Probe | Bug behavior / fixed behavior |
|-----|-------|-------------------------------|
| F10 | `UIColony.funds:GetLastSolsFundingByType(10, "Exports")` on any ordinary save | error (pairs on nil) / returns a number |
| F04 | Save `UIColony.hour`, set to 0; take any shift-3 employed colonist; call `colonist:ShouldLeaveForWork()`; restore hour | nil / true |
| F08 | Stub `Random` to return fixed values around the threshold; call `HolidayRating:RewardApplicants` for a 5-star and a 1-star rating N times; compare bonus counts (undo stub) | 1-star ≥ 5-star / 5-star > 1-star |
| F02 | Assert `GlobalGameTimeThreadFuncs.Meteors == our replacement`; plus scenario timing test below | — |
| F03 | See scenario F03 below (needs one cheat-built building; assertion itself is a script: count matching label-modifier ids on the dome after salvage) | leaked modifier remains / removed |
| F05 | On a NoTerraforming save with all visible milestones completed except one, `pcall(CompleteMilestone, <last id>, true)` | error / popup thread created |
| F15 | Record `UIColony:GetEstimatedRP()`-style research total, run `SetLightTrapMode("destroy")` with N trapped wisps (mystery save), compare grant vs notification points | 2×100×N / 100×N, matches notification |
| F64 | `local before = ColonyGetPrefabs("Train", MainCity)` → demolish a station with a docked train (cheat-instant) → compare after | count drops permanently / count restored ("stored" notification shown) |
| F45* | On a save with meteor-broken track: verify repair site `node_idx` is a number; attempt `Demolish` via script | false + silent error / numeric + salvage works |
| F58* | Sweep `MainCity.labels.Residence`: sum `#r.reserved` vs colonists actually en route | phantom reservations / zero stale entries |

(*probes for queued fixes — write them now, they become the acceptance test.)

### Wave-2 probes (all written; `SMRTest.List()` for the current set)

| Fix | Probe id | Kind | What it proves |
|-----|----------|------|----------------|
| F67 | `LanderEmptyLaunch` | behavior | an auto rocket with an empty hold is not "ready", a loaded one still is |
| F68 | `LanderCargoRatchet` | behavior | the hourly request never falls below what is aboard |
| F69 | `LanderReturnFuel` | behavior | a lander parked on an asteroid keeps a fuel ration requested |
| F73 | `ShelterReflex` | behavior | a habitat with life support down still accepts residents; Idle carries the shelter branch |
| F45 | `BrokenTrackSalvage` | install + state | BreakTrackElement stamps node_idx; no repair site in the save lacks it |
| F44 | `TrackSalvageWipe` | install | DemolishAndSplitTrack replaced |
| F30 | `LakeEntombment` | install + state | PlacePrefab sweeps; counts units currently on impassable ground |
| F37 | `GhostFarmOxygen` | install + state | SetDome hooked; no dome carries a farm modifier with no live farm |
| F50 | `RocketDroneChurn` | behavior | a steady-state refresh does not cycle command centers; a new request still does |
| F51 | `ShuttleTransportCache` | behavior | the cached verdict changes when shuttles appear |
| F52 | `VacuumWalks` | behavior | a 300m move in vacuum looks up a passage route; breathable maps do not |
| F53 | `ArrivalDeaths` | install | Arrive replaced |
| F55 | `DroneUnreachableForever` | behavior | a failed approach is stamped now, not max_int in the future |
| F58 | `StaleReservations` | behavior + state | reservations are timestamped; reports stale slots in the save |
| F61 | `HomeDomeMigrationGate` | behavior | connected-dome workplaces are offered with migration closed |
| F06 | `CrystalMysteryHang` | install | a static CrystalFlyAway handler exists (vanilla has none) |
| F09 | `TouristSatisfaction` | behavior | 0→100 pays exactly what 100→0 charges |
| F11 | `TrainPlatformWedge` | behavior | dropping an absent passenger does not raise |
| F12 | `LowStorageWarning` | install | hourly update wrapped; prints the shipped vs correct Food window |
| F13 | `CommandCenterNumbers` | behavior | all 11 `GetAvailable*` getters exist and agree with `GetAvailable` |
| F14 | `DomeOverviewHighlight` | behavior | a below-threshold stat renders with its `<red>` tag |

Probes needing a loaded game SKIP without one (`g_Consts` is a GameVar), so run
`RunAll()` from inside a colony, not the main menu.

## Cheat-triggered scenarios

- **F01 cave-ins vs No Disasters**: new underground-visit save with No Disasters.
  Console: `g_Consts.MarsquakeSpawnTime = 1` (and RandomTime = 1) → the
  UndergroundMarsquake repeat fires within a game hour. Unfixed: quake + rubble.
  Fixed: nothing, forever. (Note: `CheatTriggerUndergroundMarsquake` bypasses the
  repeat and will still work — that's expected; the fix gates the scheduler.)
- **F02 meteor cadence**: instrument the thread (test kit wraps `MeteorsDisaster`
  to log timestamps), set game speed high (cheat/`hr.TimeScale` — verify name),
  run 20 game-hours. Unfixed: strike ≈ every warning-time (6h). Fixed: no strike
  before `spawntime - warning_time` elapses. Bonus check: build 3 Sensor Towers,
  verify interval does NOT shrink further (it lengthened pre-fix… inverted).
- **F03 upgrade leak**: cheat-build Medical Center + Holographic Scanner upgrade
  in a dome; note dome birth-comfort modifier count; salvage; assert modifier
  gone; rebuild + re-upgrade; assert exactly one modifier (no stacking).
- **F07 wisp power**: St. Elmo's Fire save (cheat-start mystery — verify cheat),
  traps with N wisps, `SetLightTrapMode("free")`, read
  `trap.electricity_production`. Unfixed: ≈N. Fixed: N×1000.
- **F44/F45 tracks**: cheat-build a 5-hex track → salvage-click middle hex.
  Unfixed: whole track (and train) gone. Fixed: partial trim only. Then
  meteor-break a track (`CheatTriggerMarsquake` or spawn meteor at pos — verify)
  and salvage it (F45).
- **F67-F69 landers**: asteroid save; enable automode with all thresholds
  "ignore" → unfixed launches empty within ~1 sol; fixed waits. Manual-land on
  asteroid → unfixed unloads return fuel to ground stockpile; fixed keeps ≥35
  fuel requested. Hourly ratchet: load lander to ~half, watch `requested` values
  over 2 game hours (test-kit logger). Set `g_Consts`-side AutoDepartTimerSols
  stays vanilla — we're testing request math, not the timer.
- **F73 shelter reflex**: asteroid save, power off the habitat briefly so a
  colonist loses residence, fast-forward; unfixed: colonist idles outside past
  the oxygen timer and bleeds health; fixed: forced Rest/shelter before damage.
- **F50 rocket drone churn**: landed auto-rocket with cargo, and a drone hub whose
  service circle covers the rocket **near its outer edge** — NOT "far away". Drones
  only service what is inside `work_radius` (`const.CommandCenterDefaultRadius` = 35
  hexes; `DroneControl.lua:1019`) and the rocket carries none of its own
  (`starting_drones = 0`), so a hub placed out of range dispatches nothing and the test
  silently proves nothing. The kick hits whichever drones are walking to the rocket when
  the hourly update fires, so what matters is having many drones in transit, not a long
  trip. Logger on `SetCommand("Idle")` calls for drones targeting the rocket. Unfixed:
  hourly wave of aborts. Fixed: none from the reconnect path. Full procedure: PT-04.
- **F51 shuttle cache**: two far domes, no shuttles, homeless colonist in A,
  free housing in B → let one emigration eval fail → build+fuel Shuttle Hub →
  unfixed: still homeless indefinitely (cache); fixed: emigrates within the next
  update cycle.
- **F52 vacuum walks**: two domes ~350m apart connected by passage, atmosphere
  non-breathable; direct outside route left open. Move a colonist (filter/home
  swap). Unfixed: walks outside; fixed: passage route (or refuses).

## Manual checklists (2-minute setups)

- **F05**: NoTerraforming game, cheat-complete milestones, finish last one → popup appears, no log error.
- **F08**: depart a 5-star tourist group (cheat-set comfort/satisfaction) → applicant pool jumps.
- **F12* (when implemented)**: set Food stock to <3 sols of consumption → warning appears within an hour.
- **F13***: open Command Center → resource rows show numbers.
- **F14***: dome with average health < 30 → red column in Domes Overview.
- **F61***: dome A `accept_colonists = off`, shop in dome B via passage → residents still shop in B.
- Log hygiene after every session: no `[CommunityFixPack]` errors, no new engine errors in `%AppData%\Surviving Mars Relaunched\logs`.

## Standard test matrix (per release)

Run RunAll + the scenario set on: (1) fresh sandbox save, (2) a real long-running
save (ask community for donated broken saves — they're our best fixtures, esp.
for the save-sanitizer, trains-to-void restitution, and the three untraced leads),
(3) save made WITH the mod → disable mod → load clean (uninstall safety, policy §3).
Keep donated repro saves in `C:\Dev\SMR-BugFixPack-TestSaves\` (outside the repo,
they're large) with a README mapping save → bugs it exhibits.
