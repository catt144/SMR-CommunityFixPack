# Audit A: colonist migration, native Lua, build 1.1.1.405907

Tree: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src\Lua`. Every cite below is `file:line (1.1.1.405907)` on that tree, relative to `Src\Lua` unless it starts with `CommonLua/`. To keep the text readable, cites are written as `file:line` and the build is implied. Read-only audit. No game run and no log inspection was done.

Terms: *graph* means BuildReachableGraph. *Leg* means a GetNextLegToward result. `CD` means `IsUnitInDome(self)`, the dome the colonist stands in, which differs from `self.dome`, the dome the colonist is registered to.

---

## 1. Entry points

| Entry | Caller(s) and condition | Frequency |
|---|---|---|
| `Colonist:TryToEmigrate(cd, force)` Units/Colonist.lua:2036 | Idle heavy update: `if time > self.next_heavy_update` then `TryToEmigrate(current_dome)` :2538-2548 | once per `city.colonist_heavy_update_time` per colonist, inside Idle |
| | Idle every pass while `self.user_forced_dome` is set :2550-2551 | **every Idle pass**, not throttled. Each pass builds a full graph via FindEmigrationDome, then GetNextMigrationLeg :3803 |
| | `Stranded` loop `TryToEmigrate(nil, "stranded")` Units/ColonistTransport.lua:917 | once per `WaitMsg("TrainRoutesRebuilt", HourDuration)` :943 |
| | OpenCity `OnMsg.BreathableAtmosphereChanged` (air turning unbreathable) for each OpenCity colonist that `CanChangeCommand` Buildings/OpenCity.lua:397-401 | event; runs on the message thread, not the colonist's |
| `FindEmigrationDome` :3791 | only from TryToEmigrate :2052 (plus the debug stat :5328) | as above |
| `TryToEmigrateToDome` :1894 | TryToEmigrate legacy branch `if not leg` :2068; TryToEmigrate direct-final branch :2071-2074; MigrateStep final leg :2177-2181; TryToMigrateHome walk-final branch Units/ColonistTransport.lua:861-864 | as the callers |
| `StartMigration` :2080 | TryToEmigrate :2076 (multi-leg); TryToMigrateHome Units/ColonistTransport.lua:866 | as the callers |
| `MigrateStep` command :2155 | StartMigration `SetCommand("MigrateStep")` :2115, or via the train ticket :2113 (`StartTransport("MigrateStep", ...)`); re-issued by ExitVehicle `CommandObject.SetCommand(self, ticket.reason, ...)` Units/ColonistTransport.lua:703 or chained into the next train :685; re-issued by Transport after a delivered shuttle leg :4010-4011; MigrateStep itself re-issues a train leg :2187 | once per journey start and once per train or shuttle leg |
| `TryToMigrateHome(home)` Units/ColonistTransport.lua:848 | only from Stranded :896 | throttled by `stranded_migration_gt` to one per `stranded_retry_interval = HourDuration` :832, :849-851 |
| `Stranded(home)` Units/ColonistTransport.lua:871 | Colonist:SetCommand wrapper, when a command's destination is unreachable by foot, train and shuttle, and `command ~= "Work"` Units/ColonistTransport.lua:461-483; Abandoned when no dome is found :1465-1466; savegame fixup :5765-5770 | event. The wrapper runs on **every** `SetCommand("Idle")`, because `Idle_TransportDestination` returns `self.dome` Units/ColonistTransport.lua:193-195 |
| `Transport(dest)` command :3963 | Idle, when a committed shuttle exists: `transport.shuttle.dest_dome` :2451-2455; SetCommand wrapper rescue ride Units/ColonistTransport.lua:464-472; Stranded :900-902; test cheat Buildings/Dome.lua:2587-2588; fixup _fixup.lua:2885. A shuttle taking the task calls `colonist:InterruptCommand()` Buildings/ShuttleHub.lua:799-801, and the next Idle turns that into Transport | event |
| `TransportByFoot(dest, passage_path)` :3835 | TryToEmigrateToDome walk branch :1935; MigrateStep settle-in :2216-2218; MigrateByTrain :2031-2033 (after the train, or at once if the destination is locally reachable Units/ColonistTransport.lua:406-420); Stranded fallback Units/ColonistTransport.lua:939; Arrive :1631; ReturnFromExpedition :5463 | event |
| Forced dome | `SetForcedDome` :4357-4361, called from Residence assign Buildings/Residence.lua:352, TrainingBuilding assign Buildings/TrainingBuilding.lua:185 and Workplace assign Buildings/Workplace.lua:918. It sets `user_forced_dome = {dome, GameTime()}` and then `InterruptCommand`. After that, every Idle pass calls TryToEmigrate :2550. The lock expires after `ForcedByUserLockTimeout` (3600000) :3134-3141; __const.lua:174-176 | every Idle pass until the lock expires |
| `TryToEmigrateByTrain` Units/ColonistTransport.lua:794 | TryToEmigrate legacy `mode == "train"` :2065-2066; Abandoned :1473-1475; TransportByFoot after an elevator :3870-3873 | event |

No DLC or CommonLua override exists. The command `grep -rln -E 'TryToEmigrate|FindEmigrationDome|MigrateStep|TransportByFoot|GetNextMigrationLeg|Getui_command|TryToMigrateHome' DLC CommonLua` returned nothing. The same pattern family counts 28 lines in Units/Colonist.lua.

## 2. State

"Persisted" means the value is a plain field on the Colonist, which is a saved object: class defaults at :86-175. Upvalues such as `max_migration_legs_per_step`, `max_migration_step_fails`, `shuttle_landing_labels`, `walk_dist_slack`, `stranded_retry_interval` and `dome_enter_fails_before_teleport` are constants and are not persisted. The reachable graph is a per-call local and is never cached.

| Field | Set | Cleared | Persisted |
|---|---|---|---|
| `emigration_dome` (:106) | StartMigration :2110; MigrateStep :2160; TryToEmigrateToDome retarget :1964-1967; TransportByFoot :3837; Transport when `dest ~= self.dome` and not a leg :3968-3970; RocketBase:2065/2104, CargoTransporterNew:1001/1049 | AbortMigration :2141; TransportByFootDtor :3825; WaitTransport :3958-3960 (unless a leg was delivered); Arrive :1596; ReturnFromExpedition :5438; Done :329. **Not** cleared by FailMigrationStep :2129-2137, by a failed train leg (GoToStation :575-583, WaitForTransport :592-599), or by StartShuttleLeg's return :2176 | yes |
| `emigration_elevator` (:107) | TryToEmigrate legacy :2064; Abandoned :1474; Stranded :938; rocket/cargo code | TryToEmigrate :2054/:2070; StartMigration :2111; TryToMigrateHome :860; TransportByFootDtor :3826 | yes |
| `transport_task` (:104) | CreateColonistTransportTask LRTransport.lua:121 | ClearTransportRequest :2246; Task:Cleanup LRTransport.lua:80-82 (called by WaitTransport :3956) | yes (plain field that references a ColonistTransportTask) |
| task `.dest_dome` / `.source_dome` | creation LRTransport.lua:113-120; retarget :1962 | with the task | yes |
| task `.migration_dest` (LRTransport.lua:27) | StartShuttleLeg :2027 | TryToEmigrateToDome :1963; AbortMigration :2145 | yes |
| task `.shuttle` | the shuttle, Buildings/ShuttleHub.lua:1298 | ClearTransportRequest :2244; shuttle destructor ShuttleHub.lua:784 | yes |
| task `.state` | :2010 `almost_ready_for_pickup`; :3986 `ready_for_pickup`; ShuttleHub.lua:887 `transporting`, :935 `done` | n/a | yes |
| `shuttle` (:105) | ShuttleHub.lua:892 | ShuttleHub.lua:731 | yes |
| `migration_step_fails` (:108) | FailMigrationStep :2131 | AbortMigration :2142; every successful leg :2174/:2180/:2186/:2214. **Not** reset by StartMigration, so it carries across journeys | yes |
| `migration_start_gt` (:109) | StartMigration :2096 | never | yes |
| `stranded_migration_gt` (:110) | TryToMigrateHome :859 | never | yes |
| `reserved_residence` (:91) | Residence:ReserveResidence Buildings/Residence.lua:301, reached through Dome:ReserveResidence Buildings/Dome.lua:3482-3493 | CancelResidenceReservation :2223-2228 (called by ClearTransportRequest :2239); Residence:AddResident Buildings/Residence.lua:111; Residence.lua:94/:393 | yes |
| `reserved_workplace` / `_shift` (:88-89) | Workplace.lua:531, reached through Dome:ReserveWorkplace Buildings/Dome.lua:3516-3537 | CancelWorkReservation :2230-2236 (called by ClearTransportRequest :2240); Workplace.lua:547 | yes |
| `user_forced_dome` (:116) | :4359 | CheckForcedDome on expiry or an invalid dome :3140; Done :326. **Not** cleared on arrival | yes |
| `failed_domes` (:147) | OnEnterDomeFail :1419-1421 (a weak-keys table) | SetOutsideEffects(false) :3229; TeleportToDomeOnRepeatedEnterFails Units/ColonistTransport.lua:524 | yes. Whether the weak metatable survives a load was not checked |
| `dome_enter_fails` (:146) | :1417 | :3228; Units/ColonistTransport.lua:523 | yes |
| `was_abandoned` (:175) | Abandoned :1470; Stranded Units/ColonistTransport.lua:873 | OnEnterDomeSuccess :1427 | yes |
| `dome` | Colonist:SetDome :399-466. Migration sets it in TransportByFoot **at the start of the walk** :3840, in WaitTransport on arrival :3947, in Abandoned :1472, and in Idle :2506-2508 | SetDome(false): TransportByFootDtor (another map) :3829; WaitTransport :3949-3951; Abandoned :1483 | yes |
| `command` / `command_thread` | CommandObject:DoSetCommand CommonLua/Classes/CommandObject.lua:349-358 | same | `command` is a field. Threads also appear to be persisted: "fixup for savegames which still have sleeping threads" _fixup.lua:2889 |
| `transport_ticket` (:159) | StartTransport Units/ColonistTransport.lua:357 | DiscardTransportTicket :659 | yes |
| `outside_start` (:94) | SetOutsideEffects :3222 | :3227 | yes |

## 3. Planner

**Node kinds.** Community (Dome and MicroGHabitat), Station and Elevator. Usability is decided by `CanUseNode` :3467-3475: a Community needs only `Community.CanVisit`, a Station needs `CanWork`, anything else needs `ValidateBuilding`.

**Arrival modes** (`reachable[node]`):
- `start`: the current dome :3538. Also Communities found by the walk scan when that scan starts from a point, a Station, an Elevator or a non-Dome object :3504 (`from_dome and "walk" or "start"`). A Station root seeded by Init gets `walk` :3546.
- `walk`: cluster neighbours :3594; connected stations :3598/:3507; walk-scan stations and elevators :3518/:3528; elevators in walk range of a dome :3601-3604; domes within walk range of the current dome :3620.
- `train`: stations along tracks that have at least one train :3561-3565; a station's Communities and Elevators, but only when the station itself was not reached by `walk` :3571-3578.
- `elevator`: `node.other` :3585.
- `shuttle`: every landing pad in every visited city whose LR transport is "available" :3638-3651.

**Prev chain.** `AddReachableNode` refuses a node that is already present :3479, so `prev` is written once and the chains cannot form a cycle. Roots have `prev == false` (written by `AddReachableNode` with no `from_node`) or `nil` (Init seeds). Shuttle nodes in the colonist's own city hang off `false`, which makes them a direct leg from wherever the colonist stands. Shuttle nodes in other cities hang off the first node reached in that city :3630-3643.

**Cluster expansion (important).** `Dome:GetClusterDomes()` returns `self.connected_domes` Buildings/Dome.lua:745-747. That field is `{self, neighbour1, ...}`, meaning **direct passage neighbours only** (Buildings/Dome.lua:534; its array part is built at :1013-1016). The transitive network lives in `dome_network` (:535, :688-706), which the graph never reads. A dome's cluster is expanded only when that dome arrived by some mode other than `walk` :3591. A neighbour added as `walk` therefore never expands its own neighbours. Net effect: passages carry the planner **one hop** from a start, train, elevator or shuttle-arrival dome, and no further.

**Walk expansion.** `AddNodesInWalkDist` :3488-3532 uses the cap `ColonistMaxDomeWalkDist` (400, _GameConst.lua:149). It pre-rejects with a straight-line check :3458-3463, then calls `CheckWalkableDistance[Cached]`. That function returns false when the straight line or the path exceeds 400 Buildings/Dome.lua:218-229, and it never consults passages. After the first BFS, the current dome runs this expansion for domes only (stations and elevators skipped) :3619-3621.

**Shuttle fill.** It runs `repeat` until no new node appears :3624-3659. `IsLRTransportAvailable` counts a hub as available when `hub.working or (GetWorkNotPermittedReason() and not GetWorkNotPossibleReason())` Buildings/ShuttleHub.lua:410-418. That includes a hub the player **switched off** (`"TurnedOff"` Buildings/BaseBuilding.lua:658-659).

**Leg shapes** (GetNextLegToward :3667-3706). The function walks `prev` back from the destination to the first node whose `prev` is falsy or equals `start_dome`:
- first node `shuttle` → `{shuttle, landing}`
- Station with a Station ahead → `{train, src, dst}`
- root Station with an Elevator or Community ahead → `{elevator}` or `{walk, dome, final}`
- any other Station → `false`
- Elevator → `{elevator}`
- anything else → `{walk, dome=node, final=node==dest}`

If the destination equals the start dome, the result is `{walk, dome=start, final=true}`.

**Edge cases.**
- **Outside a dome.** `pos = GetNavigationPos()`; Communities in walk range become `start` roots and do expand their clusters.
- **Inside a passage or passage hub.** `IsUnitInDome` falls through to the holder's `parent_dome` (Buildings/Dome.lua:111-114, 160-161), which is nil. The colonist is treated as outside, standing at a point.
- **In a station.** The station is seeded as a `walk` root :3544-3547. Communities around it get `start` with `prev = station`.
- **On another map.** Reached only through Elevator nodes :3585-3589; the shuttle fill hangs other-city pads off their entry node.
- **Destination in the same cluster.** A direct neighbour gives a `walk` final leg. A neighbour two or more passages away is missing from the graph unless it lies within 400 of the current dome by outdoor path, or can be reached by train or shuttle. With shuttles it becomes a direct `shuttle` leg; without them it is not a candidate at all.
- **Destination only via a dome beyond the walk cap.** It is reached only through a direct passage neighbour, a train, an elevator or a shuttle.
- **No shuttles.** No shuttle nodes exist. Legacy routing `FindTransportationModeToCommunity` (:3374-3423) is used only when `leg == false` :2060-2068. Legacy routing does honour transitive passages, because `IsInWalkingDistDome` treats `AreDomesConnectedWithPassage` (the `dome_network`) as walkable Buildings/Dome.lua:315-316; Passage.lua:1267-1274.
- **Switched-off hubs.** They still count as available, so shuttle legs are generated, but the shuttle Idle only takes tasks when `hub.working` or when nothing blocks it `not hub:GetNotWorkingReason()` Buildings/ShuttleHub.lua:1378-1386. The tasks sit unserved until `ColonistTransportTaskExpirationTime = DayDuration` _GameConst.lua:144; LRTransport.lua:48.

## 4. Execution per leg (MigrateStep :2155-2221)

The loop runs at most `max_migration_legs_per_step = 8` :2118, :2161. Each iteration rebuilds the full graph :2166.
- **Shuttle to an intermediate pad** :2170-2176. `StartShuttleLeg` :2016-2029 keeps a task that already has a shuttle or already targets this landing. Otherwise it calls `ClearTransportRequest` and `BookShuttleRide` :1986-2012, which picks as source the current dome's pad, else the nearest pad of any kind, else `self.dome`. The task is set to `almost_ready_for_pickup` and `migration_dest = emigration_dome` :2027. MigrateStep then **returns**, and the colonist falls back to Idle. When a shuttle commits it interrupts the colonist; Idle :2451-2454 starts Transport, and after delivery WaitTransport keeps the destination :3941-3942 and Transport re-issues MigrateStep :4010-4011.
- **Shuttle to the destination, or a final walk** :2177-2181. Goes to `TryToEmigrateToDome(cd, dest, mode, walk_dist or -1)`.
- **Train** :2182-2187. Checked by `CanBoardTrainLeg` :2122-2126, then `StartTransport("MigrateStep", ...)` Units/ColonistTransport.lua:355-372 → GoToStation → WaitForTransport → BoardVehicle → ExitVehicle, which chains a follow-up train from the same station :678-686 or re-issues MigrateStep :703.
- **Elevator** :2188-2194. `self:UseElevator(leg.elevator)` is called inline (Unit:UseElevator Units/Unit.lua:1045-1067: Goto the entrance, then ride). A map-slot mismatch afterwards → FailMigrationStep.
- **Intermediate walk** :2195-2213. A passage path is used only if `dist` is missing, below 0, or greater than `min_dist` (1200 when the air is breathable, else 400) :2198-2202. Each passage hop is an `EnterBuilding` whose **result is ignored** :2204-2209. The final `EnterBuilding(leg.dome)` failing → FailMigrationStep :2210-2212.
- After the loop: inside the destination → `TransportByFoot(dest)` to settle :2216-2218. Otherwise, including after 8 legs, → FailMigrationStep :2220.

**TryToEmigrateToDome walk branch** :1906-1937:
- A negative distance becomes `max_int` :1912-1915.
- A passage path is computed only when `dist > min_dist` :1916-1920.
- The colonist walks (with the passage path if one exists) when there is no passage path, OR (dist < 1200 and fewer than 8 domes to pass through), OR an elevator is involved, OR no LR transport is available :1922-1924. Otherwise the code falls through to the shuttle booking at :1972.
- On the walk path it calls `ClearTransportRequest` and `DiscardTransportTicket`, reserves a residence (and work if the colonist needs it) at the destination, then `TransportByFoot`.

**TransportByFoot** :3835-3880:
1. Sets `emigration_dome` and pushes the destructor.
2. **`SetDome(dest)` before moving** :3840.
3. Enters each passage-path dome, ignoring results :3842-3849.
4. Uses the elevator if one was given :3857-3862.
5. On the wrong map: destructor, then `SetCommand("Abandoned")` **with no `return`** :3863-3867.
6. May switch to a train :3870-3873.
7. `EnterBuilding(dest)`; on failure `TeleportToDomeOnRepeatedEnterFails` :3876-3878. That teleports only when `dome_enter_fails >= 100` Units/ColonistTransport.lua:518-527.

Without a passage path, the move is a single `Goto_NoDestlock` to an interior point of the dome Units/Unit.lua:348-376. Passages are pathfinder tunnels (Passage.lua:1201-1248, `is_pf_tunnel`), so whether that Goto goes through a passage or across open ground is decided by the engine pathfinder, not by Lua.

**EnterBuilding failure.** `Unit:EnterBuilding(Dome)` calls `OnEnterDomeFail`, which increments `dome_enter_fails` and records `failed_domes[dome]` :1416-1423. During `Abandoned`, `Colonist:EnterBuilding` refuses a dome outside walk range: it sleeps `HourDuration/10`, then `SetCommand("Idle", true)` Units/ColonistTransport.lua:753-760, **without** recording a failure.

**Failure bound.** `max_migration_step_fails = 5` :2119, compared as `>=` :2132.

## 5. Failure and abort: what each path releases

| Path | Releases | Leaves behind |
|---|---|---|
| FailMigrationStep :2129-2137 | nothing; after Sleep(1000) goes to Idle | `emigration_dome`, `reserved_residence`, `reserved_workplace` and any booked task. Idle does **not** resume MigrateStep; only the next heavy-update TryToEmigrate re-plans, possibly to a different dome. Idle :2556-2557 → `UpdateResidence` :3123-3131 cancels the foreign reservation only if `SetResidence` actually changes the residence (AddResident cancels it, Buildings/Residence.lua:111) |
| AbortMigration :2140-2151 | `emigration_dome`, `migration_step_fails`, residence and work reservations | the transport task, with `migration_dest = false`. If a shuttle later serves it, the colonist is flown to the intermediate pad. If that pad is a Community other than `self.dome`, Transport sets `emigration_dome = pad` :3968 and WaitTransport registers the colonist there :3946-3947 with no reservation. If the pad is a Station or Elevator, the colonist is left there |
| TransportByFootDtor :3823-3833 | `emigration_dome`, `emigration_elevator`; `SetDome(false)` only if on the wrong map | the reservations. Also leaves `self.dome == dest`, because SetDome ran at :3840, even when interrupted halfway across open ground |
| WaitTransport :3928-3961 | on a failed ride: reservations, and possibly SetDome(false) :3948-3954; `emigration_dome` unless a leg was delivered | nothing further |
| Train leg failure (GoToStation :575-583, WaitForTransport :592-599) | the ticket | `emigration_dome` and the reservations. The command ends, ChooseIdleCommand runs, and the journey is silently dropped without counting a failure |
| Stranded :871-945 | its status effect and notification (destructor :878-881) | Its fallback `TransportByFoot(dome)` :939 reserves only `if dome ~= residence dome`; the home case reserves nothing |
| TryToMigrateHome :848-867 | nothing itself; hands off to StartMigration (ClearTransportRequest, then re-reserves at home) or to TryToEmigrateToDome | `stranded_migration_gt` throttle |
| TeleportToDomeOnRepeatedEnterFails Units/ColonistTransport.lua:520-527 | `dome_enter_fails`, `failed_domes` | fires only at 100 or more failures |
| Abandoned :1434-1494 | ClearTransportRequest :1451 (task and reservations); on an enter failure, SetDome(false) plus both reservations :1483-1485 | n/a |

## 6. Reservations across a journey

- They are made only for the **final** destination: StartMigration :2099-2109, TryToEmigrateToDome :1927-1934/:1954-1961/:1972-1980, TryToEmigrateByTrain Units/ColonistTransport.lua:807-813, Stranded fallback :932-937, UniversalRocket stopover UniversalRocket.lua:2265-2267.
- No leg reserves at an intermediate dome. StartShuttleLeg/BookShuttleRide reserve nothing :2016-2029, :1986-2012.
- The final-leg `TryToEmigrateToDome` re-reserves. `ClearTransportRequest` cancels first :2239-2240, and `Dome:ReserveResidence` then takes the **first** residence that can accept the colonist Buildings/Dome.lua:3487-3491. That drops a user's `user_forced_residence` pick made through Buildings/Residence.lua:351-352: the StartMigration and TryToEmigrateToDome paths cancel it before re-reserving elsewhere.
- Abort mid-journey: AbortMigration cancels both reservations. FailMigrationStep, a failed train leg and TransportByFootDtor do **not** cancel (section 5).

## 7. What the player sees

- Status line: `Status<right><ui_command>` :4514-4515. The Dome line reads `self.dome` through `GetDomeDisplayName` :4446-4450 (XDef/ipColonist.generated.lua:108).
- `Getui_command` :4672-4716. Transport, TransportByFoot and MigrateStep all map to `"Moving to a new Dome: <EmigrationDomeDisplayName>"` :4647-4649.
- The dome name comes from `GetEmigrationDomeDisplayName` :4462-4465, which returns `self.emigration_dome or self.transport_task and self.transport_task.dest_dome`.
- The guard `... and self.emigration_dome` :4676 has no effect. When it fails, the chain reaches `else return tcommand` :4713-4714, which is the **same** "Moving to a new Dome" text.

Can it show `self.dome`? **Yes**, on these code paths (all SOURCE-VERIFIED):
1. **Every TransportByFoot.** `emigration_dome = dest` :3837, then `SetDome(dest)` :3840. For the whole walk the Dome line and the "Moving to a new Dome" line name the same dome. SetDome also drops the old residence and workplace :437-438 before the colonist has left.
2. **A shuttle rescue ride home.** The SetCommand wrapper builds `CreateColonistTransportTask(self, false, home)` with `home = self.dome` Units/ColonistTransport.lua:446, :464-471; Stranded does the same at :900-902. Transport does not set `emigration_dome` when `dest == self.dome` :3968. The UI then falls back to `transport_task.dest_dome == self.dome` and shows "Moving to a new Dome: <home>".
3. **Stranded → TryToMigrateHome(home = self.dome).** Goes to StartMigration (`emigration_dome = home` :2110, command MigrateStep) or to TryToEmigrateToDome → TransportByFoot(home).
4. **Stranded fallback.** `ChooseDome` is called with no `exclude` Units/ColonistTransport.lua:924-925, so it can return `self.dome` (by score or as the safety dome, _GameUtils.lua:486-500) → `TransportByFoot(self.dome)` :939.
5. **Arrive / ReturnFromExpedition** → `TransportByFoot(self.emigration_dome or self.dome)` :1595/:1631, :5463.
6. **`self.dome = X` while standing in Y.** FindEmigrationDome excludes only `my_dome` :3752, so Y can be chosen. The leg is `{walk, Y, final}` :3705, then TransportByFoot(Y): "Moving to a new Dome: Y" while already inside Y. That is not `self.dome`, but it reads the same to a player.

A stale `emigration_dome` left by FailMigrationStep or a failed train leg (section 5) outranks `transport_task.dest_dome` in the name lookup :4463. A later rescue ride to home then displays the stale journey's dome.

## 8. Field symptoms

**(a) "Moving to a new dome that is the dome they live in."** Paths 1-6 in section 7.
- Most plausible for the frequent case: **path 1**, because it fires on every foot migration by construction (:3837 + :3840).
- Most plausible when it co-occurs with (b): **paths 2-4**. A colonist stuck outside, beyond `DefaultOutsideWorkplacesRadius` (20 hexes, __const.lua:1946-1948) from home, fails `HasLocalAccess(self.dome)` Units/ColonistTransport.lua:270-300 on every `SetCommand("Idle")`. That leads to a rescue shuttle to home (path 2) when shuttles exist, otherwise to Stranded → TryToMigrateHome (path 3) or the fallback (path 4). Every one of those displays the home dome as "new".

**(b) Walking outside, stuck near passages and buildings, suffocating.** `OxygenMaxOutsideTime = 120000` __const.lua:1756-1758; the effect is applied at :4901-4904.
- **b1 (SOURCE-VERIFIED loop):**
  1. TransportByFoot fails to enter the destination (engine Goto, Units/Unit.lua:361-376) → `OnEnterDomeFail` → the command ends.
  2. `self.dome` is already the destination (:3840) and `dome_enter_fails > 0`, so Idle → Abandoned :2501-2503.
  3. Abandoned keeps `dome = self.dome` :1452 and calls `EnterBuilding` :1477.
  4. If `IsInWalkingDist(self, dome)` is false (a path over 400, or no path from a pocket), the Abandoned guard sleeps and sets Idle Units/ColonistTransport.lua:753-760. No failure is recorded and there is no Goto.
  5. This repeats every `HourDuration/10` while `HasLocalAccess(self.dome)` holds (within 20 hexes). The colonist stands still until suffocating. The teleport rescue needs 100 failures, which this loop never records.
- **b2.** Passage hops ignore the result of `EnterBuilding` (:3845-3848, :2205-2208). A failed hop continues from wherever the colonist stopped, possibly outside.
- **b3.** In unbreathable air, TryToEmigrateToDome computes no passage path when the outdoor distance is at most 400 (:1911, :1916). The single Goto may then go over open ground (the pathfinder's choice).
- **b4 (HYPOTHESIS).** Abandoned :1458 runs `pairs(self.failed_domes)` when ChooseDome returns nil. `failed_domes` can be `false` (class default :147) or `nil` (reset at :3229). If `pairs(false)` raises, CommandThreadProc catches it (CommonLua/Classes/CommandObject.lua:250-261), Idle → Abandoned repeats, and the colonist is stuck outside.
- **Most plausible: b1.** It is fully traced, it needs only an engine Goto failure near buildings or passages (the reported location), and nothing in it moves the colonist again.

**(c) Other colonists do not use passages.**
- **c1 (SOURCE-VERIFIED):** the graph expands passages only to direct neighbours, and only from non-`walk` domes (:3591-3596 with `connected_domes`, Buildings/Dome.lua:534). A dome two or more passages away becomes a direct `shuttle` leg (prev false :3643-3647 → :3685-3686) when shuttles exist. That goes to TryToEmigrateToDome with `"shuttle"`, which skips the walk branch and calls BookShuttleRide :1972. Without shuttles the dome is simply unreachable.
- **c2 (SOURCE-VERIFIED):** for a passage-connected destination with outdoor distance of 1200 or more, or with no outdoor route (-1 becomes `max_int` :1912-1915), the walk branch is skipped whenever `IsLRTransportAvailable`, and the colonist books a shuttle :1922-1924.
- **c3 (SOURCE-VERIFIED):** `IsLRTransportAvailable` counts switched-off hubs :413. This forces c1/c2 onto shuttle routes that no shuttle serves, because the shuttle Idle requires working (ShuttleHub.lua:1378-1386). Colonists then wait up to a sol per attempt.
- **c4:** passage paths are used only above `min_dist` (:1916, :2200). Below it, the route is up to the pathfinder.
- **c5:** a colonist on a passage hub or in a passage counts as outside (section 3), so no passage path is built.
- **Most plausible: c1 + c2.** The code routes passage-connected domes by shuttle by design, and the multi-hop gap is a structural difference from the legacy walk test, which used `dome_network` (Buildings/Dome.lua:315).

## 9. Suspects

| # | Defect | Line | Trigger | Falsifying control | Status |
|---|---|---|---|---|---|
| S1 | The Abandoned walk-cap guard puts a colonist into a permanent Idle↔Abandoned loop, standing still outside | Units/ColonistTransport.lua:753-760 with Colonist.lua:2501-2503, :1452, :1477 | `self.dome` set, `dome_enter_fails > 0`, colonist within 20 hexes of home, `CheckWalkableDistance(colonist, dome)` false | a colonist in that state moves or reaches a dome with no other command intervening; or the log shows Abandoned re-entering with an increasing `dome_enter_fails` | SOURCE-VERIFIED |
| S2 | Cluster expansion is one hop and uses `connected_domes` (neighbours), not `dome_network` | Colonist.lua:3591-3596; Dome.lua:745-747 | domes A–B–C chained by passages, C more than 400 outdoors from A | from A, the graph contains C with mode `walk` | SOURCE-VERIFIED |
| S3 | UI "Moving to a new Dome" shows the home dome; the `emigration_dome` guard is dead because `else` returns the same text | Colonist.lua:4676, :4713-4714, :4463 | rescue ride home (Units/ColonistTransport.lua:464-471) | a rescued colonist's status shows anything other than "Moving to a new Dome: <home>" | SOURCE-VERIFIED |
| S4 | TransportByFoot registers the colonist in the destination (and drops the old home and job) before walking | Colonist.lua:3840, :437-438 | any foot migration | the Dome line mid-walk shows the origin | SOURCE-VERIFIED |
| S5 | A passage-only link (dist -1) is treated as infinitely far, so a shuttle is preferred over the passage | Colonist.lua:1912-1915, :1922-1924 | two domes linked only by a passage, with a hub available | the colonist walks through the passage while a hub is available | SOURCE-VERIFIED |
| S6 | `IsLRTransportAvailable` treats a TurnedOff hub as available, but shuttles do not serve from it | ShuttleHub.lua:413 vs :1378-1386 | all hubs switched off, shuttles present | an available shuttle hub is reported only while one is actually working | SOURCE-VERIFIED |
| S7 | FailMigrationStep and a failed train leg leave `emigration_dome` and the reservations; Idle does not resume the journey | Colonist.lua:2129-2137; Units/ColonistTransport.lua:575-583, :592-599 | a leg fails once | the reservation is cancelled before the next heavy-update re-plan | SOURCE-VERIFIED (whether a leak persists depends on UpdateResidence :3123-3131) |
| S8 | AbortMigration keeps the booked task, so the colonist can be flown to an intermediate pad and registered there with no reservation, or left at a station or elevator | Colonist.lua:2143-2146; :3968; :3946-3947 | abort while a shuttle leg is booked but uncommitted | the task is cleared, or never executed, after an abort | SOURCE-VERIFIED |
| S9 | Passage-hop `EnterBuilding` results are ignored | Colonist.lua:3845-3848, :2205-2208 | a passage removed mid-walk | a hop failure stops the walk | SOURCE-VERIFIED |
| S10 | TransportByFoot `SetCommand("Abandoned")` has no `return`, so a second `PopAndCallDestructor` can follow if SetCommand returns | Colonist.lua:3866-3879 | a wrong-map arrival | the engine kills the current thread inside DoSetCommand (CommonLua/Classes/CommandObject.lua:378-385) | HYPOTHESIS (engine `DeleteThread` semantics) |
| S11 | `pairs(self.failed_domes)` runs on false or nil | Colonist.lua:1458 | Abandoned with `self.dome` false, no safety dome, no recorded failures | the log has no error at Colonist.lua:1458 | HYPOTHESIS |
| S12 | The GetNextLegToward Station→Station first hop is always `train`, even when the next station was reached on foot | Colonist.lua:3690-3691 | a colonist held in station S0 with S1 in walk range but not on S0's line | CanBoardTrainLeg rejects it (ExitVehicle :680 guards; StartMigration :2085 returns silently) | SOURCE-VERIFIED (impact low) |
| S13 | The `g_TransportationModeToCommunityCache` key omits `shuttles_available` and is not invalidated when LR availability changes | Colonist.lua:3401-3407; Dome.lua:316 | a forced-dome or rocket call (false) followed by an emigration call (true) for the same pair | the cached mode differs by caller | SOURCE-VERIFIED |
| S14 | Forced dome runs TryToEmigrate (a full graph build) on every Idle pass, and FailMigrationStep → Idle → StartMigration repeats about every second until the lock expires | Colonist.lua:2550-2551, :2092-2096, :2135 | a forced dome that cannot be reached | the log or a profiler shows one attempt per heavy update | SOURCE-VERIFIED (a loop bounded by sleeps, not a spin) |
| S15 | Legacy forced-dome routing sets `shuttles_available = false`, but TryToEmigrateToDome books a shuttle anyway when mode is false | Colonist.lua:2062, :1972 | an unreachable forced dome with a hub | no shuttle task is created | SOURCE-VERIFIED |
| S16 | Re-reserving through `Dome:ReserveResidence` ignores the player's forced residence | Colonist.lua:2097-2100; Dome.lua:3487-3491; Residence.lua:351-352 | assigning a colonist to a residence in another dome | the chosen residence stays reserved through StartMigration | SOURCE-VERIFIED |
| S17 | `UpdateResidence` dereferences `self.dome` without a guard | Colonist.lua:3128 | Idle with `reserved_residence` set, `self.dome` false and an active forced dome (Idle :2506 skips SetDome) | no error at Colonist.lua:3128 | HYPOTHESIS |
| S18 | An intermediate walk leg into a MicroGHabitat (holder, `parent_dome` false) can never count as "in dome", so the same leg repeats until 8 legs, then fails | Colonist.lua:3504-3508, :2162-2166; Dome.lua:111-114 | outside colonist, destination behind a station connected to a MicroGHabitat | the next iteration plans past the habitat | HYPOTHESIS |
| S19 | The `SetForcedDome` assert `self.dome ~= dome` can be hit from Workplace.lua:918 when `col_dome` is nil | Colonist.lua:4358 | a homeless colonist | n/a; the assert is debug-only | HYPOTHESIS (low) |

## 10. Commands run and not done

Run (Bash, working directory `...\1.1.1.405907\Src\Lua` unless noted):
- `awk`/`sed -n` line reads:
  - Units/Colonist.lua: 60-175, 300-345, 399-470, 1400-1640, 1860-2258, 2395-2600, 3102-3245, 3290-3440, 3440-3990, 3985-4020, 4300-4370, 4435-4470, 4620-4720, 5320-5470, 5755-5775
  - Units/ColonistTransport.lua: 60-300, 330-960
  - Buildings/Dome.lua: 111-125, 155-400, 525-540, 670-760, 995-1025, 2560-2600, 3482-3545
  - Passage.lua: 1130-1340
  - LRTransport.lua: 1-140
  - Buildings/ShuttleHub.lua: 105-125, 405-430, 742-990, 1280-1420
  - LRManager.lua: 160-200
  - _GameUtils.lua: 380-530
  - Units/Unit.lua: 120-150, 300-470, 1045-1075
  - Buildings/Elevator.lua: 961-1010
  - Buildings/Residence.lua: 105-125, 284-356
  - Buildings/TrainingBuilding.lua: 178-188
  - Buildings/Workplace.lua: 905-922
  - UniversalRocket.lua: 2240-2275
  - Buildings/OpenCity.lua: 385-410
  - _fixup.lua: 2870-2890
  - CommonLua/Classes/CommandObject.lua: 213-275, 341-420
- `grep -rn -E` searches over `--include=*.lua .`:
  - the entry-point, field and constant family: `FindEmigrationDome|TryToEmigrate|...|emigration_elevator`
  - `_TransportDestination|_CanReachTransportDestinationOnFoot|_TicketDestination`
  - `emigration_dome`
  - `connected_domes`
  - `ColonistMinDistToIgnorePassage|ColonistMaxDomeWalkDist|...`
  - `passage_hub|goto_dome`
  - `outside_start|...OxygenMaxOutsideTime`
  - `dome_enter_fails`
  - `failed_domes|was_abandoned`
  - `g_TransportationModeToCommunityCache`
  - `migration_dest|TransportColonist|...`
  - `colonist_transport_tasks|...`
  - `SetForcedDome|StatusEffect_Stranded`
  - `EmigrationDomeDisplayName|...`
  - reservation and shuttle field writes
  - helper-definition locator
  - `GetWorkNotPermittedReason`
- Absence control: `grep -rln -E 'TryToEmigrate|FindEmigrationDome|MigrateStep|TransportByFoot|GetNextMigrationLeg|Getui_command|TryToMigrateHome' DLC CommonLua` (working directory `Src`) returned 0 files. Presence side: `grep -rc -E 'TryToEmigrate|MigrateStep|TransportByFoot' Lua/Units/Colonist.lua` returned 28.

Not done:
- No game run, no log read, no save inspection. Engine behaviour is not verified from Lua: pathfinder tunnel choice, `pairs(false)`, `DeleteThread(CurrentThread())`, persistence of weak metatables and threads.
- Not read: `GetScoreFor`, `HasFreeLivingSpaceFor`, the global `ChooseResidence` (this decides whether S7's reservation actually leaks), `GetNavigationPos`, `Station:ForEachConnectedTrack`, `ForEachStationAlongTrack`, `Community:CanVisit`, `CanAcceptNewColonists`, `LeaveColonist`, the `RocketBase`/`CargoTransporterNew` arrival paths beyond the grep hits, `GoToRandomPos`.
- No comparison against vanilla Surviving Mars or earlier builds. "Regression versus legacy" in S2 means only the in-tree legacy function `FindTransportationModeToCommunity`.
