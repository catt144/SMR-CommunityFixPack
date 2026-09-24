# Audit C: how the pack meets 1.1.1 colonist migration

Scope: read-only. Repo HEAD `b06d6b8`, with the working tree as in the session status. Game source is the archived trees
`SMR-SrcArchive\1.1.1.405907\Src` (the default) and `...\1.1.0.403908\Src`. Each cite reads `file:line` on 1.1.1
unless it says otherwise. Paths in cites are relative to `Src\Lua` unless they start with `CommonLua`, `Data` or `Code/`.

**Version caveat that comes before every field conclusion.** Pack v15, the one carrying the 1.1.1 rebase of
`Fix_VacuumWalks`, was committed `45578d4` (2026-09-23 12:38) and closed `48a9559` (2026-09-23 16:00). Before that,
v14 shipped the 1.1.0 body copy (`7a401f1`), which F125 records as harmful on 1.1.1. Which version the reporters run
cannot be read from here. It decides several of the answers below (see FIELD SYMPTOMS and S2).

---

## TOUCH POINTS

Search: a grep of `Code/*.lua` for the migration vocabulary in the brief (46 terms), with comment lines filtered out.
Code-line hits per module: VacuumWalks 50, ArrivalDeaths 16, HabitatExpeditionReturn 12, FreedHousingNotice 9,
ShuttleTransportCache 9, StaleReservations 6, ShuttleHubOffAvailable 4, ShelterReflex 1, TrackSalvageWipe 1.
`90_SaveSanitizer.lua` had 0 hits for `colonist|reserv|emigrat|transport_task|passage`. As a control, `SMRFixPack` gets 9 hits
in that file. `Fix_HabitatExpeditionDraft` touches expedition drafting only (`FilterColonistsByTrait`,
`GatherAvailableColonists`), not migration.

| Module | Target(s) | Install kind | 1.1.1 status (bodycheck, archived 1.1.1 `--src`) |
|---|---|---|---|
| Fix_VacuumWalks | `Colonist.TryToEmigrateToDome` | input-only wrapper on the class: raises `transport_mode_dist` to `ColonistMaxDomeWalkDist+1`, then tail-calls | OK: pin matches Colonist.lua:1894-1982, DEFECT still shipped (:1911) |
| | `Colonist.GetNextMigrationLeg` | post-wrapper on the class: arms a one-call marker for each thread | **no pin** (1.1.1 body :3709-3717, would-be sha256 `deba3d79…`) |
| | global `IsInWalkingDistDome` | global swap (`SetGlobal`) of a wrapper that uses the marker and rewrites return 2 to `-1` | **no pin** (Dome.lua:299-319, would-be sha256 `3c297c41…`); body identical 1.1.0 and 1.1.1 |
| | `Colonist.MigrateStep` | not patched; pinned as the consumer | OK: pin matches :2155-2221, DEFECT still shipped (:2199) |
| | `Colonist.StartShuttleLeg` | probe target only | no pin (:2016-2029, `e38e22fb…`) |
| Fix_ShuttleHubOffAvailable | global `IsLRTransportAvailable` | post-filter by global swap: false passes through, true is rechecked with `ui_working` | OK: matches ShuttleHub.lua:410-419 |
| Fix_ShuttleTransportCache | global `FindTransportationModeToCommunity` | **full replacement** (the pin is 1.1.0-dated but the body is identical on 1.1.1) | OK: matches Colonist.lua:3374-3408 |
| Fix_StaleReservations | `Residence.ReserveResidence` | post-wrapper (stamp `SMRFixPack_reserved_at`) plus an additive `OnMsg.NewDay` sweep that cancels | OK: GetFreeSpace and ReserveResidence both match |
| Fix_FreedHousingNotice | `Colonist.SetResidence` | post-wrapper that defers a `CheckHomeForHomeless` game-time thread | OK, 8 rows |
| Fix_ArrivalDeaths | `Colonist.Idle` (pre, keyed on `self.arriving`), `Colonist.OnArrival` (pre), `Colonist.GetExpeditionReturnDome` (post, C102) | wrappers; one-shot probe at first use | OK, 11 rows |
| Fix_HabitatExpeditionReturn | `Colonist.GetExpeditionReturnDome`, `Colonist.SetCommand` (every command change), `Colonist.UpdateWorkplace` | wrappers | **1 BODY-CHANGED**: `Colonist:UpdateWorkplace` (1.1.1 :1797-1878; the diff is `ValidateWorkplace` and a type guard, not migration) |
| Fix_ShelterReflex | `Colonist.Idle` (pre); reads `transport_task`, `residence`, `outside_start` | wrapper | OK (Idle :2411-2588) |
| Fix_TrackSalvageWipe | reads `Colonist.MigrateStep` existence as a branch guard | `test` spec | OK (not migration) |
| Fix_HabitatExpeditionDraft | `GatherAvailableColonists`, `FilterColonistsByTrait` | wrappers | 1 BODY-CHANGED (`CargoTransporterNew:GatherAvailableColonists`); not migration |

Load order of the wrappers that share a target (metadata.lua:312-350): ShelterReflex → ShuttleTransportCache →
VacuumWalks → ArrivalDeaths → StaleReservations → ShuttleHubOffAvailable → FreedHousingNotice → … →
HabitatExpeditionReturn. So `Idle` = ArrivalDeaths(ShelterReflex(vanilla)), and `GetExpeditionReturnDome` =
HabitatExpeditionReturn(ArrivalDeaths(vanilla)).

---

## PER-MODULE FINDINGS

### Fix_VacuumWalks (F52/F125)

**a. Install.** (Fix_VacuumWalks.lua)
- Before Require: if any one of `MigrateStep/GetNextMigrationLeg/StartShuttleLeg` exists but not all three are functions,
  it returns `"the multi-leg migration methods are incomplete (game update changed them?)"` (:61-65).
- Specs in order (:115-141): class `Colonist.TryToEmigrateToDome`; test `has_110_helpers` (`HasShuttleLandingSlots`,
  `Dome.ReserveWorkplace`, `Colonist.CancelWorkReservation`); globals `GetAtmosphereBreathable`,
  `AreDomesConnectedWithPassage`; paths `const.Colonist.ColonistMaxDomeWalkDist`/`…MinDistToIgnorePassage` (number);
  test `thresholds_have_expected_order` (walk+1 < passage); probe (`StartShuttleLeg` carries `migration_dest` on 1.1.1,
  or the `need_work` probe on 1.1.0). On 1.1.1 it adds class checks for MigrateStep, GetNextMigrationLeg and StartShuttleLeg; globals
  `IsInWalkingDistDome`, `IsUnitInDome`, `CurrentThread`; and paths `table.pack` and `table.unpack`.
- **Any** decline sets `update_suspect` unless the 1.0.7 shape is present (:143-149). This includes the `test` and `probe`
  failures, which Core deliberately does not mark (00_Core.lua:241-249). So a decline caused by a mod's constants or by a mod's
  wrapper produces the "game code changed" dialog. See S1.
- Then: `SetGlobal("IsInWalkingDistDome", …)` is checked by read-back. Only after it succeeds does it assign the two class wrappers
  (:188-250). The desk confirms a failed SetGlobal leaves both targets untouched.

**b. Pins.** TryToEmigrateToDome and MigrateStep bodies match, and both DEFECT regexes still match (bodycheck exit 0).
GetNextMigrationLeg and IsInWalkingDistDome are wrapped **without** a pin, so a body change there is invisible to
bodycheck. The behaviour both wrappers rely on is their return shape and their argument order at :2198.

**c. Callers on 1.1.1 (all re-read).**
- `TryToEmigrateToDome`: Colonist.lua:2068 (legacy mode, forced dome), :2074 (leg is shuttle-to-dest or final walk),
  :2181 (MigrateStep final/shuttle), ColonistTransport.lua:864 (TryToMigrateHome). All four are live.
- `GetNextMigrationLeg`: Colonist.lua:2166 (MigrateStep), :3803 (FindEmigrationDome, forced dome), :4330
  (CanReachDomeForBuilding), ColonistTransport.lua:679 (ExitVehicle destructor), :853 (TryToMigrateHome).
- `IsInWalkingDistDome`, direct: Dome.lua:296, ColonistTransport.lua:863, Colonist.lua:1473, 2072, 2178, 2198, 3317
  (7; the header is exact). **But** Dome.lua:296 is `IsInWalkingDist`, which fans out to 21 more call sites
  (Dome.lua:342/426/439; Colonist.lua:1156/3870/3945/3949/4320/4349; ColonistTransport.lua:43/45/129/234/723/727/753/822;
  _GameUtils.lua:401/417/451/465). All of them pass through the wrapper and pay `CurrentThread()` plus a `table.pack` per call.
- Is the repaired path live? Yes. The 1.1.1 migration reaches the native passage decision at :1916-1924 (direct) and :2199-2202
  (intermediate), and the module feeds both. The reachable graph (:3488-3662) makes its own walk decisions
  (`CheckWalkableDistanceCached`, :3503; `GetClusterDomes`, :3593) that **no pack module touches**. VacuumWalks changes *how* a
  planned walk leg is walked, never *whether* a walk leg is planned.

**d. Guards against the 1.1.1 bodies.**
- Direct wrapper early returns (:157-165) versus the native walk-branch gate (:1906): `(task.shuttle and not
  emigration_elevator)` is the exact negation of the native `(not task.shuttle or emigration_elevator)`. Non-walk,
  non-number, `<=0`, `> ColonistMaxDomeWalkDist`, breathable and unsafe-gap calls all pass the original input through.
  `AreDomesConnectedWithPassage(nil, x)` returns false (Passage.lua:1268), so an outside start passes through as well.
  `current_dome` always comes from `IsUnitInDome` (a Dome or `parent_dome`, Dome.lua:111-165; Idle :2484), so a
  MicroGHabitat, which has no `dome_network`, never reaches `d1.dome_network[d2]` (Passage.lua:1273). I checked this because a
  habitat there would throw.
- After the raise, the native body computes `GetDomesPassagePath`. With < 8 intermediate domes
  (`const.ColonistMaxPassagePassthroughDomes = 8`, _GameConst.lua:151) the colonist walks through the passage. With ≥ 8 and shuttles
  available it falls through to the task block and `BookShuttleRide` (:1940-1981). When `BookShuttleRide` returns nil there,
  nothing happens at all (S4).
- Marker: it is keyed by `CurrentThread()` and weak. It is armed only when `self.command == "MigrateStep"`,
  `self.command_thread == thread`, `IsUnitInDome(self)` is truthy and the leg is a non-final `walk` with a `dome` (:226-244).
  In MigrateStep the non-final walk leg always falls to the `else` at :2195. With `current_dome` truthy, :2198 is the
  **first** statement to run after :2166. The call is `IsInWalkingDistDome(leg.dome, current_dome, self.city)`, which matches the wrapper's
  `leg_dome == bld1`, `current_dome == bld2`, `city == source_city`. Nothing runs between arming and consumption.
- Calling GetNextMigrationLeg again in the same step clears the marker first (`pending_by_thread[thread] = nil`, :230), so a stale
  marker cannot survive a loop iteration. The walk, elevator and passage branches all yield (EnterBuilding, UseElevator) only
  after :2198 has consumed the marker.
- The header's "only :2166 runs with command MigrateStep" is imprecise. The ExitVehicle destructor at ColonistTransport.lua:679
  runs on the **new** command's thread with `self.command` already set to it (CommandObject.lua:349, :231-237). If that new command is
  MigrateStep, :679 can arm, but only when `IsUnitInDome` is truthy for a colonist whose holder is a station, and
  :2166 resets the marker before :2198 either way. The only possible consumer before that is a 3-argument call with exactly the
  marker's domes and city. I found no such call in the destructor tail (:680-702). So the practical risk is nil, but it is not
  proven by the header's argument.
- Conversion: only when `0 < dist <= ColonistMaxDomeWalkDist`, in vacuum, with a safe gap. MigrateStep then asks
  `GetDomesPassagePath` (:2200-2201). If that returns nil it walks outside exactly as vanilla does. `-1` is never cached,
  because the consumer at :2198 is not under `FindTransportationModeToCommunity`.
- Intermediate passage paths have **no passthrough cap** in MigrateStep (:2204-2209). A ≤400 m outside leg can become a long
  passage detour. That is safe in vacuum, but slow.

### Fix_ShuttleHubOffAvailable (F54)

- a. Global post-filter (:78-92). It declines if `IsLRTransportAvailable`, `BaseBuilding.GetWorkNotPermittedReason` or
  `…GetWorkNotPossibleReason` is missing. It is strictly narrower than vanilla. The two differ only for a hub with
  `ui_working == false`, which vanilla admits through the "TurnedOff" permission reason (ShuttleHub.lua:413).
- b. The pin matches 1.1.1. The header's consumer list (Colonist.lua:1569, :2650, …) is 1.0.7-era and stale.
- c. 1.1.1 consumers: Dome.lua:316 (IsInWalkingDistDome walkable verdict); Colonist.lua:1924 (walk vs shuttle), :1991
  (BookShuttleRide pad search), :2062 (legacy mode), :3639 (**BuildReachableGraph shuttle fill**), :3891
  (IsTransportAvailableBetween, called by :2007, :4350 and UniversalRocket.lua:2260), :3920 (IsWaitingTransport), :3992 (Transport
  pickup wait); ColonistTransport.lua:463, :897 (rescue and stranded rides). All of them call the global at call time. There is no `local`
  alias anywhere in the 1.1.1 tree (grep, 0 hits).
- d. What a switched-off hub now does to leg planning, when every people-carrying hub is off:
  - The graph adds no shuttle landings (:3639). Destinations reachable only by shuttle drop out of
    `GetBestReachableCommunities`, and no shuttle legs are planned.
  - :1924 forces the walk branch (with `passage_path` when one exists), including ≥ 8-dome chains.
  - :2007 refuses tasks, so `StartShuttleLeg` returns false → `FailMigrationStep` (a planned shuttle leg whose hub was switched
    off between planning and execution), and after 5 tries `AbortMigration` releases the reservations (:2129-2151).
  - :3992: a colonist already at a pickup gives up at once. `WaitTransport` cancels its reservations and may
    `SetDome(false)` (:3948-3953), leaving it outside at the pad. Vanilla would instead wait up to `ColonistMaxWaitShuttlePickupTimeMs`
    = one sol (_GameConst.lua:143).
  - Dome.lua:316: passage-connected cached dome pairs read as walkable at any distance.

  By construction the module can only remove shuttle options and add walks. The walks it adds use passages whenever
  `GetDomesPassagePath` finds one, because `not passage_path` already forced a walk in vanilla.

### Fix_ShuttleTransportCache (F51)

- a. Full replacement. It adds `entry.smr_shuttles` to the cache key and declines if FTMC, GTMC or ValidateBuilding is missing.
- b. The body is identical to 1.1.1 (:3374-3408). The new 1.1.1 invalidation handlers (:3328-3358: train label, rocket landed or launched,
  savegame fixup) write the same GameVar and stay compatible. `UniversalRocket.lua:4043` and `ColonistTransport.lua:802` also
  flush it.
- c. **The repaired dimension is nearly dead on 1.1.1.** FTMC callers: Colonist.lua:2063 (TryToEmigrate, only when
  `FindEmigrationDome` returned no leg), UniversalRocket.lua:2229 and :2251, and SupplyRocket.lua:68, where the last three pass a
  literal `false`. At :2062, `shuttles_available = not self:CheckForcedDome() and …`. A forced dome, the usual reason for a
  missing leg per :2061/:3819, pins it to `false`. The non-forced case with a missing leg arises only from
  `GetNextLegToward`'s station branch `return false` (:3701). In 1.1.0, FindEmigrationDome called FTMC with a live flag
  (1.1.0 Colonist.lua:3525). 1.1.1's `FindEmigrationDome` (:3791-3821) builds the graph and reads `IsLRTransportAvailable`
  live each time, so F51's "cached unreachable" cannot arise on the main path. The module repairs a path migration no longer
  uses. It is a retire or re-scope candidate, not a harm.
- d. The "cache flush versus CheckWalkableDistanceCached" question: they are different caches. `CheckWalkableDistanceCached` reads
  `g_DomeToDomeDist` (Dome.lua:244-251, maintained by `UpdateDistToDomes`), which the pack never touches. Residual: FTMC's
  cached "walk" verdict still depends on `IsLRTransportAvailable` *inside* `IsInWalkingDistDome` (Dome.lua:316), and the key does
  not capture that. On the forced-dome path the flag is always false, so a hub switched on or off does not refresh a cached
  passage-pair verdict until a DomesConnected, TrainRoutesRebuilt or similar flush. Low reach.

### Fix_StaleReservations (F58)

- a. Post-wrapper `Residence.ReserveResidence` (stamp), plus a NewDay sweep over `MainCity.labels.Residence` only. A slot counts as stale if
  the colonist is invalid, desynced or dying, or older than `g_Consts.ForcedByUserLockTimeout` (3,600,000 ms, __const.lua:176).
  Expedition holds are exempt.
- b. Pins match 1.1.1.
- c. 1.1.1 reservation sites go through `Dome:ReserveResidence` → `Residence:ReserveResidence` (Dome.lua:3482-3493). The direct
  callers are MicroGHabitat.lua:86 (`Residence.ReserveResidence(self,…)`, which gets stamped too), Residence.lua:351 and Colonist.lua:5347.
  Migration sites: Colonist.lua:1927/1954/1973 (TryToEmigrateToDome), :2100 (StartMigration), ColonistTransport.lua:808
  (MigrateByTrain), :933; arrivals RocketBase.lua:1982/2073/2109, CargoTransporterNew.lua:1006/1051/1092 (present on 1.1.0
  too); departures UniversalRocket.lua:2266.
- d. **Per-leg calls do not restamp.** `Dome:ReserveResidence` returns early when the colonist already holds a slot in that
  dome (Dome.lua:3483-3485), and StartMigration or TryToEmigrateToDome re-reserve into the same destination. So the stamp is the
  *first* reservation. A multi-leg journey that runs longer than 3,600,000 ms loses its destination slot to the sweep partway through the journey.
  The journey continues because `emigration_dome` is untouched, and on arrival the colonist is re-housed only if space remains (S7). `AbortMigration` →
  `CancelResidenceReservation` (:2147, :2223-2228) and `ClearTransportRequest` (:2238-2240) are vanilla releases. They do not
  collide with the sweep, because Residence:CancelResidenceReservation is idempotent (:387-389).

### Fix_FreedHousingNotice (F59)

- a. Post-wrapper `SetResidence` → deferred `CheckHomeForHomeless` when the old home still has free space after the stack unwinds.
- b. 8 rows OK. `SetResidence`, `UpdateResidence` and `CheckHomeForHomeless` are identical between 1.1.0 and 1.1.1 (difflib, this
  session). 1.1.1 still has 11 `SetResidence` call sites (Colonist.lua:438/1258/1300/3130/5337; Residence.lua:86/158/266/349;
  NaturalHabitat.lua:7; Data/TraitPreset.lua:772). The header's line numbers are from 1.1.0.
- d. Mid-journey: `CheckHomeForHomeless` walks `parent_dome.labels.Homeless` (Residence.lua:161-169). `UpdateResidence` checks
  only `CanChangeCommand` (:3124), which is `not dying/leaving/disappeared and not IsTransported()` (:2889-2891). That is true for
  a colonist in `MigrateStep` or `TransportByFoot` who is walking, and false while riding (`IsTransported`).
  - A migrant with a **valid reservation** is not in the Homeless label (:3095), so it is untouched.
  - A **homeless** migrant with no reservation stays in its OLD dome's label during `MigrateStep`, because `self.dome` changes only at
    `TransportByFoot` :3840. The notice can give it a bed in the old dome while it walks away. `SetDome(dest)` then drops that bed on
    arrival (:438) and notifies again. That is a transient hold that can pre-empt a staying homeless neighbour. The same happens on vanilla's own
    `CheckHomeForHomeless` triggers; the pack adds triggers (S6).
  - A `Transport` rider is protected while `IsTransported`. While walking to a pickup it is not.

### Fix_ArrivalDeaths (F53/C83/C102)

- The live path is intact: Idle is still the only issuer of `Arrive` (:2432-2433), and `Arrive` reads `emigration_dome` at :1595.
  A separate train arrival path, `DisembarkOnArrival` (ColonistTransport.lua:322-352, issued at :371), bypasses Idle. It goes to a
  station, and the OnArrival wrapper still applies.
- Arrival and stopover versus the module: `UniversalRocket.lua:2225-2270` is **departure** stopover booking (colonists leaving
  Mars). ArrivalDeaths does not touch it. It is reached only through `FindTransportationModeToCommunity` (ShuttleTransportCache's
  replacement, flag false) and `IsTransportAvailableBetween` (ShuttleHubOffAvailable). `Dome.lua:2587` is inside
  `Dome:TestColonistLRTransport`, a test helper with **no Lua caller** in the 1.1.1 tree. Neither is on the live
  migration path.
- **The reservation does not follow the reroute.** 1.1.1 (and 1.1.0) reserve in the ChooseDome result before the colonist's first Idle
  (RocketBase.lua:2072-2074; CargoTransporterNew.lua:1006/1051). The Idle wrapper rewrites `emigration_dome`
  (Fix_ArrivalDeaths.lua:485-486) but leaves `reserved_residence` in the rejected dome (S5).
- C102 `GetExpeditionReturnDome` runs before the receiver's reservation (RocketBase.lua:1974 → :1982), so it is placed correctly.

### Fix_HabitatExpeditionReturn (C95) and Fix_ShelterReflex (F73b): migration relevance only

- HER's `SetCommand` wrapper affects only colonists in its weak `placing` table (expedition returnees to a MicroGHabitat
  out of range). A migration `SetCommand` is untouched unless such a colonist gets `TransportByFoot` with `dest == home`.
- ShelterReflex (Idle pre-wrapper) acts on a colonist whose Idle runs while it is outdoors ≥ ½ `OxygenMaxOutsideTime`, holds a working
  residence and has no `transport_task`. It sends that colonist to `Rest`, which means its **old** home. Mid-journey idles happen after
  `FailMigrationStep` (:2135-2136) or after a shuttle leg drop (`WaitTransport` keeps `emigration_dome`, :3941-3960). The journey
  is then abandoned for the old home until the next heavy update re-plans it. The reservation in the destination stays held.

---

## CROSS-MODULE INTERACTIONS

1. **VacuumWalks + ShuttleHubOffAvailable.** With hubs off, `IsLRTransportAvailable` is false. The graph plans no shuttle legs
   (:3639), and a raised-distance direct call chooses the passage walk even for ≥ 8-dome chains (:1924). The two modules agree,
   and VacuumWalks' passage route becomes the only option. With hubs on, a ≥ 8-dome chain gets a shuttle booking, and if that booking fails,
   nothing moves (S4). There is no case where the pair removes the shuttle and also withholds the passage.
2. **VacuumWalks + ShuttleTransportCache.** On the legacy path (:2063 → pack FTMC → IsInWalkingDistDome wrapper) the command is
   Idle, so the marker cannot arm and no `-1` can be cached. They are independent.
3. **StaleReservations + multi-leg.** No restamp per leg (Dome.lua:3483-3485), so journeys longer than 3.6 M ms lose the slot (S7).
4. **StaleReservations + ArrivalDeaths.** The orphan reservation left in a rejected arrival dome is released by the sweep only after
   3.6 M ms, or when the colonist settles (`AddResident` → `CancelResidenceReservation`, Residence.lua:111) (S5).
5. **FreedHousingNotice + MigrateStep.** A homeless migrant can be re-housed in its origin dome mid-walk (S6). It deliberately does not hook the
   sweep's `CancelResidenceReservation` (Fix_FreedHousingNotice.lua:192-197), so there is no feedback loop with F58.
6. **ShelterReflex + MigrateStep.** An outdoor mid-journey idle sends the colonist back to its old home (above).
7. **ArrivalDeaths + HabitatExpeditionReturn** on `GetExpeditionReturnDome`: HER (outer) appends the habitat, and ArrivalDeaths
   (inner) re-validates `result[1]` with `accept_colonists/ui_working/HasLifeSupport/CanAcceptNewColonists`
   (Community.lua:96-98 = `ui_working and accept_colonists`), a subset of HER's `home_usable`. Consistent; no conflict found.
8. **Failure mode of the pair VacuumWalks-declined + everything else active.** This is exactly vanilla F52: short vacuum walks and
   intermediate legs go outside. It is relevant to the field reports below.

---

## DESK COVERAGE GAPS

`python tools/desk_f125_vacuum.py`: 25/25 demands held (exit 0).
`python tools/desk_migration_cluster.py`: 16/16 held (exit 0).

**desk_f125_vacuum.py exercises:**
- a pre-fix control
- SetGlobal failure
- a direct vacuum final leg (event order), the no-passage fallback, breathable, and a long detour to a *successful* booking
  (with `ColonistMaxPassagePassthroughDomes = 1`)
- runtime-threshold equal/cross
- native retarget, and a committed shuttle
- MigrateStep intermediate followed by final, breathable intermediate, no-passage intermediate, shuttle leg, train leg, cancellation
- two marker falsifiers (a wrong next call; the command changed to Idle), the different-map one-value return, and the real TestKit probe.

It does **not** exercise:
1. The real `BuildReachableGraph`/`GetNextLegToward`. Both are stubs that return queued legs (:171-172), so the planning of walk legs,
   and `IsLRTransportAvailable`'s role in it, is never run.
2. The pack's `ShuttleHubOffAvailable` wrapper composed with VacuumWalks. The shipped `IsLRTransportAvailable` is loaded and no hub is
   ever switched off.
3. A failed `BookShuttleRide` after the raise. `HasShuttleLandingSlots` → `o.landing` (true) and `IsTransportAvailableBetween` →
   always true (:157-158). S4 is untested.
4. The TryToMigrateHome (ColonistTransport.lua:853-864) and TryToEmigrate (:2068/:2074) callers.
5. A foreign GetNextMigrationLeg caller that arms on the MigrateStep thread (ColonistTransport.lua:679 destructor running on the new command
   thread). Only "command set to Idle" and "wrong domes" are tested.
6. Real `Require` and `Register`: the desk supplies its own Require (:113-137) that never marks `update_suspect`. No leg reaches
   Fix_VacuumWalks.lua:143-149 (the dialog path) through the thresholds test, the probe, the const paths or the method specs.
7. The apply-time `const.Colonist` ordering check with mod-altered constants. Only the runtime `g_Consts` guard is tested.
8. Cached `g_DomeToDomeDist` entries with `dist[1] == false` (`-1`, over the cap, `too_far`). `set_dist` always writes `{true, d}`
   (:225-230), and the `not IsLRTransportAvailable` clause of Dome.lua:316 is not reached.
9. A failed `EnterBuilding` on a passage hop. The stub always succeeds and teleports (:195-199), so the "passage hop fails → outside"
   risk (S8) is untested.
10. Two or more intermediate walk legs in one step, and elevator → intermediate walk.
11. More than one thread, or a yield between arming and consumption. There is a single `THREAD` constant.

**desk_migration_cluster.py exercises:**
- F51: cache recompute on flag flip, on stubbed `IsInWalkingDistDome`
- F52 on the direct wrapper
- F54 predicate
- the retired F60.

Its VacuumWalks leg runs with `Colonist = {}` (:39), so `has_multileg` is false and the **1.1.0 single-wrapper install**
is what gets measured. The 1.1.1 install and MigrateStep are never loaded there, even though the file says it targets
1.1.1.

It does not exercise F58, F59, ArrivalDeaths or any interaction. Require is a no-op (:43). F51 is tested only as a cache
property, not on a 1.1.1 caller (see the dead-path finding above).

**TestKit `20_Probes_Wave2.lua:569-634` (VacuumWalks)** drives only the direct `TryToEmigrateToDome` wrapper, with a stub colonist and
overridden globals. It does not cover MigrateStep, the marker, `IsInWalkingDistDome`, the hub-off composition or the decline paths.

---

## FIELD SYMPTOMS

**(a) "Colonists decide to move to a new dome which is the same dome they live in."**
No pack module chooses the destination on the 1.1.1 path, by construction.
- `FindEmigrationDome` → `BuildReachableGraph` → `GetBestReachableCommunities` → `GetNextLegToward` (:3478-3821) are unwrapped.
- The destination filter `community ~= my_dome` (`self.dome`, :3720/:3752) is vanilla, and no module writes `self.dome` except through
  vanilla calls.
- Pack inputs to that computation: `IsLRTransportAvailable`, which is stricter and can only *remove* shuttle-reachable candidates;
  nothing else.
- The pack sets destinations only for arrivals (ArrivalDeaths) and expedition returns (ArrivalDeaths C102, HER), and a return
  to one's own home there is intended.
- FreedHousingNotice changes a residence, never a destination.

Vanilla mechanisms that match the report (HYPOTHESIS, for audits A and B):
- `TransportByFoot` sets `self.dome = dest` **before** walking (:3840), so the infopanel reads "lives in X, moving to X" for the
  whole walk. VacuumWalks lengthens that window by choosing passage detours over short outside walks.
- A colonist visiting dome B (`self.dome = A`) can choose B. It then "moves" in place (walk leg with dist 0 → :2074 →
  TransportByFoot).
- A departure stopover can be the home dome by design (UniversalRocket.lua:2263-2264).

**(b) "Walk outside and get stuck near passages and near certain production buildings and suffocate."**
- VacuumWalks never removes a passage route and never adds an outside walk as a *decision*.
- ShuttleHubOffAvailable adds walks only where `not passage_path` already forced one, or with a passage path.
- One contributing mechanism exists (HYPOTHESIS, S8): VacuumWalks replaces one ≤400 m outside walk with a chain of per-dome
  `EnterBuilding` calls whose results are ignored (:2204-2209 in MigrateStep; :3842-3849 in TransportByFoot). If a hop cannot use its passage,
  for example because the passage entrance is blocked by a building, the next `EnterBuilding` may path outside, possibly further than the
  original walk. "Near passages and near certain production buildings" fits that shape, but engine pathing is not source-verifiable
  here.
- ShelterReflex can pull an outdoor mid-journey colonist back toward its old home (a longer outdoor leg).
- ArrivalDeaths leaves an arrival with no reachable dome waiting by the rocket, outdoors, by design.
- The **most direct** explanation is the pack **not** acting: VacuumWalks declined, as on the users who see the dialog, or v14
  installed, where the intermediate leg :2199 was unfixed (F125). Both give vanilla F52.

**(c) "Other colonists do not use passages when moving between domes."**
No active pack module can reduce passage use, by construction:
- VacuumWalks only moves inputs *into* the passage lookup (the raise to `cap+1`, or `-1`).
- ShuttleHubOffAvailable only forces walks, taking the passage when one is found.

Explanations:
- **VacuumWalks inactive** (the dialog) or **v14**: vanilla F52 walks outside for ≤400 m in vacuum (:1911, :2199).
- Breathable maps: vanilla walks outside under 1200 m by design (:1911 uses the passage threshold). The pack leaves that alone.
- ≥ 8 intermediate domes with hubs on: a shuttle, by design (:1922).
- Vanilla 1.1.1 graph limit (SOURCE-VERIFIED reading, HYPOTHESIS as to the field, S9): cluster domes are added only from a node not
  reached by walking (:3590-3596). A dome two or more passage hops away and more than 400 m outside is not walk-reachable at all. It becomes shuttle-only or
  unreachable, so colonists fly or never go, instead of walking the passage. On 1.1.0 that pair was "walk" via
  `IsInWalkingDistDome`'s passage clause.

**Dialog naming the vacuum-walk fix on other rigs.** On stock 1.1.1 with v15, every VacuumWalks check is pure Lua against
code-defined values (`const.Colonist.*` come from _GameConst.lua:149-150, `DefineConstInt`, loaded before mods). So a
difference between rigs needs a **mod, a mod-altered constant, another game build, or pack v14**. Each spec that could trip,
with its log line (`[CommunityFixPack] ` prefix; every one below also sets `update_suspect` through Fix_VacuumWalks.lua:145-148,
so the dialog lists it):

| # | Spec (order) | Plausible third-party trigger | Log line |
|---|---|---|---|
| 0 | pre-check :61-65 | a mod sets one of MigrateStep, GetNextMigrationLeg or StartShuttleLeg to a non-function | `VacuumWalks: inactive (the multi-leg migration methods are incomplete (game update changed them?))` |
| 1 | class Colonist.TryToEmigrateToDome | replaced by a non-function | `VacuumWalks: inactive (Colonist.TryToEmigrateToDome not found (game update changed it?))` |
| 2 | test has_110_helpers | HasShuttleLandingSlots, Dome.ReserveWorkplace or Colonist.CancelWorkReservation removed (if HasShuttleLandingSlots is nil *and* `const.ColonistMaxDomeWalkDist` is a number, there is no dialog) | `VacuumWalks: inactive (the shipped emigration code has no work-slot reservation or shuttle landing slots; this repair stands down on the older body)` |
| 3-4 | globals GetAtmosphereBreathable, AreDomesConnectedWithPassage | replaced by a non-function | `VacuumWalks: inactive (AreDomesConnectedWithPassage not found (game update changed it?))` |
| 5-6 | const.Colonist.* numbers | a mod `__const.lua` (loaded by ConstDef.lua:408-411) redefines them as non-numbers or in another group | `VacuumWalks: inactive (walk-distance constants not found at const.Colonist.* (game update changed them?))` |
| **7** | test thresholds_have_expected_order | **PLAUSIBLE**: a "walk further" mod that raises `const.Colonist.ColonistMaxDomeWalkDist` to ≥ `ColonistMinDistToIgnorePassage` − 1, or lowers the passage threshold, before the pack loads | `VacuumWalks: inactive (there is no safe integer gap between the dome walk and passage-detour thresholds; the selective distance input is unsafe)` |
| **8** | probe StartShuttleLeg | **PLAUSIBLE**: a 1.1.1-aware transport mod loaded earlier wraps or replaces `Colonist.StartShuttleLeg` and touches the stub (it has only `transport_task`/`emigration_dome`) | if it throws: `VacuumWalks: behaviour probe declined (threw: …)` then `VacuumWalks: inactive (the shipped multi-leg migration body does not carry migration_dest through StartShuttleLeg; this repair stands down on an unknown shape)` |
| 9 | class MigrateStep, GetNextMigrationLeg, StartShuttleLeg | unreachable after #0 | `… Colonist.MigrateStep not found (game update changed it?)` |
| 10 | globals IsInWalkingDistDome, IsUnitInDome, CurrentThread | replaced by a callable table | `VacuumWalks: inactive (IsInWalkingDistDome not found (game update changed it?))` |
| 11 | table.pack, table.unpack | overwritten | `VacuumWalks: inactive (table.pack not found (game update changed it?))` |
| 12 | SetGlobal read-back | a mod guards `_G` writes (a `__newindex` on _G) | `VacuumWalks: inactive (could not install the IsInWalkingDistDome wrapper)` |
| 13 | throw in an unprotected `test` | metamethods on `const` or a classdef | `VacuumWalks: FAILED to apply: …` (status `error`) |

Then the report line: `update report: N fix(es) deactivated over a game-code change: …, VacuumWalks`.

On **v14**, the probe calls 1.1.1 `TryToEmigrateToDome` with a table stub. That reaches `IsSameMap(stub, {})` at :1943, a C
export (CommonLua/LuaExportedDocs/Game/realm.lua:95 declares it with an empty body). Its verdict on Lua tables may depend on engine or map state (S2). The v14 decline
line would be `VacuumWalks: inactive (the shipped TryToEmigrateToDome does not compute a work-slot reservation up front — this copy is written for game 1.1.0 and stands down on a different body)`,
optionally preceded by `behaviour probe declined (threw: …)`.

---

## SUSPECTS

- **S1.** VacuumWalks reports a mod-caused decline (thresholds test or behaviour probe) as game-code rot, so players are told a
  game update broke it.
  - Line: Fix_VacuumWalks.lua:143-149 (versus 00_Core.lua:241-249).
  - Triggering input: a mod raising `const.Colonist.ColonistMaxDomeWalkDist` to ≥ passage − 1, or wrapping `StartShuttleLeg`.
  - Falsifying control: a clean 1.1.1 + v15 run logs `VacuumWalks: applied`. Adding a scratch mod that sets
    `const.Colonist.ColonistMaxDomeWalkDist = const.Colonist.ColonistMinDistToIgnorePassage` makes the dialog name the fix. If the
    dialog stays absent, S1 is wrong.
  - **SOURCE-VERIFIED** (code path). The field linkage is HYPOTHESIS.
- **S2.** The pre-F125 (v14) probe's verdict on 1.1.1 hinges on the C function `IsSameMap` applied to Lua tables. It can either apply the 1.1.0 body
  over 1.1.1 (the F125 harm) or decline with the dialog, depending on engine state rather than on code.
  - Line: `git show 45578d4^:Code/Fix_VacuumWalks.lua` probe → 1.1.1 Colonist.lua:1940-1954. A falsy result returns with `asked == true`, so the module applies.
    A truthy result reaches `dest_dome:ReserveResidence` on `{}` and throws; so does a C throw. Either way it declines.
  - Triggering input: pack v14 on game 1.1.1.
  - Falsifying control: the users' logs show which v14 line fired. In the console at the main menu and in-game, run
    `print(pcall(IsSameMap, {}, {}))`. The same result in both states refutes the state dependence.
  - **HYPOTHESIS.**
- **S3.** ShuttleTransportCache's F51 repair is almost unreachable on 1.1.1. The only migration caller passes a flag pinned false for
  forced domes, and FindEmigrationDome no longer calls FTMC.
  - Line: Colonist.lua:2060-2063, :3791-3821; 1.1.0 :3525.
  - Triggering input: any 1.1.1 migration.
  - Falsifying control: a 1.1.1 FTMC call site with a varying truthy `shuttles_available`. The grep found none besides :2063.
  - **SOURCE-VERIFIED.** It is a retire or re-scope candidate, not a harm.
- **S4.** After VacuumWalks' raise, a ≤400 m vacuum pair with ≥ 8 intermediate passage domes, shuttles "available" and a failing
  `BookShuttleRide` does nothing: no command, no reservation and no FailMigrationStep. At :2181 MigrateStep has already cleared
  `migration_step_fails` (:2180), so the colonist re-plans every Idle and never moves. Vanilla would have walked outside.
  - Line: Fix_VacuumWalks.lua:179-180 → Colonist.lua:1922-1924, :1972-1981.
  - Triggering input: that geometry, plus `IsTransportAvailableBetween` false or `HasShuttleLandingSlots(dest)` false.
  - Falsifying control: a desk leg with a ≥ 8-dome chain and `IsTransportAvailableBetween = false` that ends in `command:TransportByFoot`
    refutes S4.
  - **SOURCE-VERIFIED** path; reach HYPOTHESIS.
- **S5.** The ArrivalDeaths reroute leaves the arrival-time reservation in the rejected dome. Until the colonist settles or
  3.6 M ms pass, it is kept out of the Homeless label, and the rejected dome scores as "has a home" for it.
  - Line: Fix_ArrivalDeaths.lua:485-486 versus RocketBase.lua:2072-2074, Colonist.lua:3095, :3748-3758.
  - Triggering input: an arrival whose ChooseDome dome had a reservable slot but was unreachable or unwelcoming.
  - Falsifying control: after the Idle wrapper runs, `reserved_residence.parent_dome == new emigration_dome` (or nil) would refute S5.
  - **SOURCE-VERIFIED** mechanism; consequence HYPOTHESIS.
- **S6.** FreedHousingNotice can house a homeless MigrateStep migrant in its origin dome mid-journey. The bed is freed at arrival and
  may pre-empt a staying homeless colonist.
  - Line: Fix_FreedHousingNotice.lua:284-288 → Residence.lua:161-169 → Colonist.lua:3123-3130, :3840, :438.
  - Triggering input: a vacancy in dome A while a homeless, unreserved migrant from A is in MigrateStep.
  - Falsifying control: a desk leg in which the migrant stays homeless after RunDeferred refutes S6.
  - **SOURCE-VERIFIED** path; vanilla has the same exposure through its own triggers.
- **S7.** StaleReservations cancels a live multi-leg journey's destination slot after 3.6 M ms, because re-reservations into the
  same dome never restamp.
  - Line: Fix_StaleReservations.lua:107-114, :159-160; Dome.lua:3483-3485.
  - Triggering input: a journey longer than `ForcedByUserLockTimeout`, for example a stranded station wait.
  - Falsifying control: a restamp observed on each StartMigration refutes S7.
  - **SOURCE-VERIFIED**; low reach.
- **S8.** Forcing a passage path turns one short outside walk into sequential per-dome `EnterBuilding` hops with unchecked results.
  A blocked passage can yield a longer outside walk than the one avoided.
  - Line: Colonist.lua:2204-2209 and :3842-3849 (reached via Fix_VacuumWalks.lua:179-180, :219).
  - Triggering input: a passage-connected pair whose passage entrance is obstructed.
  - Falsifying control: an owner in-game test with an obstructed passage in which the colonist stays inside or fails the hop without exiting.
  - **HYPOTHESIS** (engine pathing).
- **S9.** (vanilla, outside the pack) The 1.1.1 reachable graph expands passage clusters only from non-walk nodes, so domes two or more
  passage hops away and more than 400 m outside are not walk-reachable.
  - Line: Colonist.lua:3590-3596, :3500-3504.
  - Triggering input: A–P–B passages, with A–B outside > `ColonistMaxDomeWalkDist`.
  - Falsifying control: B appearing in `BuildReachableGraph` as "walk" refutes S9.
  - **SOURCE-VERIFIED** reading; symptom (c) linkage HYPOTHESIS.

---

## COMMANDS RUN

- Reads: `cat -n` / `sed -n` / `awk 'NR>=a && NR<=b'` on Code/00_Core.lua, the Fix_* modules named above, metadata.lua:312-350,
  tools/desk_f125_vacuum.py, tools/desk_migration_cluster.py, TESTKIT.md:125-172, the TestKit `20_Probes_Wave2.lua:569-634`,
  docs/agent/bugs/F125.md:1-60, and archived 1.1.1 and 1.1.0 source spans cited above.
- Greps (`grep -rn` over the 1.1.1 `Src` tree): callers of TryToEmigrateToDome, GetNextMigrationLeg, IsInWalkingDistDome,
  IsInWalkingDist, IsLRTransportAvailable, IsTransportAvailableBetween, FTMC, ReserveResidence, SetResidence,
  CheckHomeForHomeless, GetExpeditionReturnDome, CreateColonistTransportTask, TestColonistLRTransport; local aliases (1 hit,
  `CurrentThread` in cthreads.lua:564); walk constants in all three builds.
- `python tools/bodycheck.py --src B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src --all --module <M>` for VacuumWalks,
  ShuttleHubOffAvailable, ShuttleTransportCache, StaleReservations, FreedHousingNotice, ArrivalDeaths,
  HabitatExpeditionReturn (exit 1: 1 BODY-CHANGED), HabitatExpeditionDraft (exit 1: 1 BODY-CHANGED), ShelterReflex,
  TrackSalvageWipe. All others exited 0.
- `python tools/bodycheck.py --src … --pin` for GetNextMigrationLeg, IsInWalkingDistDome and StartShuttleLeg (hashes above).
- `python tools/desk_f125_vacuum.py` → 25/25 held, exit 0. `python tools/desk_migration_cluster.py` → 16/16 held, exit 0. Both on HEAD b06d6b8.
- A Python difflib script run from a **heredoc on stdin** (I disclose the brief deviation: the script contained no backslashes). It compared
  UpdateWorkplace, IsInWalkingDistDome, GetNextMigrationLeg, SetResidence, UpdateResidence and CheckHomeForHomeless across 1.1.0 and 1.1.1.
- `git log`/`git show 45578d4^:Code/Fix_VacuumWalks.lua`/`git rev-parse` (read-only).
- Housekeeping: the bodycheck outputs were first written to `/tmp/bc_*.txt` rather than the scratchpad. I deleted them.

## NOT DONE

- No in-game or engine run. That leaves the C behaviour of `IsSameMap` and `CurrentThread`, engine passage pathing (S8) and performance of the
  `table.pack` per IsInWalkingDist call unmeasured.
- No doccheck, no hooks, no git writes, no edits under the repo.
- Did not read desk_f59_*, the other bug entries (F51/F52/F54/F58/F59), or reports.
- Did not verify which pack version the reporters or the owner run, or their logs.
- Did not trace Unit.EnterBuilding's passage use, PassageHub topology in `GetDomesPassagePath`, or `OpenCity.lua:400`.
