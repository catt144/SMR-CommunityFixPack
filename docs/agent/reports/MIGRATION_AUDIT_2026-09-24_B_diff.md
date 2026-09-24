# Audit B: colonist migration and transport, function-level diff 1.0.7 -> 1.1.0 -> 1.1.1

Read-only source diff, 2026-09-24. All citations are `file:line (build)`, paths relative to `Src/Lua/` of the archived tree for that build:

- 1.0.7.396349: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.0.7.396349\Src\Lua`
- 1.1.0.403908: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.0.403908\Src\Lua`
- 1.1.1.405907: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src\Lua`

Evidence labels: **SOURCE** = read in the archived tree. **INFERRED** = a reading of control flow that no run has checked.

## 0. Headline

1. **1.1.0 split choosing a destination from getting there.** The candidate set moved to a reachable graph that can see chained journeys: walk, then train, then elevator (`BuildReachableGraph`, `Units/Colonist.lua:3400-3423 (1.1.0.403908)`). Execution stayed single-hop through the cached `FindTransportationModeToCommunity` (`:3524-3526 (1.1.0.403908)`). So a dome that the graph reaches only by a chain could be chosen and then not travelled to (INFERRED).
2. **1.1.1 closes that gap.** `FindEmigrationDome` now returns `(dome, leg)`, where `leg` is the first hop along the graph's predecessor chain (`Units/Colonist.lua:3791-3821 (1.1.1.405907)`). The journey then runs one leg at a time:
   - `StartMigration` (`:2080-2116`) and `MigrateStep` (`:2155-2221`) drive the legs.
   - Shuttle legs to intermediate pads use `StartShuttleLeg`/`BookShuttleRide` (`:1986-2029`), with a new `ColonistTransportTask.migration_dest` field (`LRTransport.lua:27 (1.1.1.405907)`).
   - A train leg re-issues `MigrateStep` on arrival (`Units/ColonistTransport.lua:678-686, 702-703 (1.1.1.405907)`).
   - `Stranded` gained a multi-leg `TryToMigrateHome` (`Units/ColonistTransport.lua:848-867, 896 (1.1.1.405907)`).
3. **`FindTransportationModeToCommunity` and `g_TransportationModeToCommunityCache` are off the main 1.1.1 migration path.**
   - The only migration caller left is the `leg == false` fallback in `TryToEmigrate` (`Units/Colonist.lua:2060-2069 (1.1.1.405907)`).
   - The other three callers are rocket-departure code, and all three pass `shuttles_available=false`.
4. **Most tracked defect sites are byte-identical from 1.1.0 to 1.1.1:** F51 cache, F54 predicate, F58 reservations, F59 `RemoveResident`, F53/C83/C102 dome choice, C42 passage holder.
   - **F52's expression is now duplicated** into the new `MigrateStep` intermediate-walk branch (`Units/Colonist.lua:2199 (1.1.1.405907)`).
   - **F54's predicate now feeds more places:** the graph marks every landing pad shuttle-reachable per city (`:3639-3650 (1.1.1.405907)`).

## 1. Inventory

Status per step: `identical` (byte-identical body text; the line may have shifted); `whitespace only`; `body changed`; `signature changed` (the parameter list differs, and the body may also differ); `added`; `removed`; `n/a` (absent on both sides of that step). No declaration moved between files. Four were removed in 1.1.0 and replaced elsewhere; §2 names each replacement.

The rows were produced by `inv.py`. It extracts every top-level `function X(...)` / `local function X(...)` / `X = function(...)` from column 0 down to the next column-0 `end`, and compares the extracted texts. Declarations nested inside other functions are not rows. That covers the `PushDestructor` closures, `OnMsg` bodies written as locals, and `LRTransport.lua`'s `MapGameTimeRepeat` callback.

Row selection:
- `Units/ColonistTransport.lua` and `LRTransport.lua`: every declaration in the file.
- All other files: the named scope list in `inv.py` (the SEL table).

**Totals, 194 rows** (command: `python inv.py > inv_rows.md`, then `awk -F'|' '{print $7"->"$8}' inv_rows.md | sort | uniq -c`):

- 1.0.7 -> 1.1.0: identical 56, body changed 56, added 47, signature changed 8, whitespace only 7, removed 4, n/a 16 (these 16 are the 1.1.1-only additions). Sum 194.
- 1.1.0 -> 1.1.1: identical 157, added 16, body changed 16, signature changed 1, n/a 4 (the four removed in 1.1.0). Sum 194.
- Reconciliation: the 16 `n/a` in step 1 are exactly the 16 `added` in step 2. The 4 `removed` in step 1 are exactly the 4 `n/a` in step 2. There are 20 `n/a` cells in total (`grep -c "n/a" inv_rows.md` = 20).

Controls: independent `sed`-range diffs agreed with the extractor on five sites.
- `FindTransportationModeToCommunity` 1.1.0 :3170-3204 vs 1.1.1 :3374-3408: identical.
- `IsLRTransportAvailable`, 1.0.7 vs 1.1.1: identical.
- `PassageBase:TraverseTunnel`, 1.1.0 vs 1.1.1: identical.
- `Residence:RemoveResident`, 1.0.7 vs 1.1.1: identical.
- `_GameUtils.lua:390-501`, 1.1.0 vs 1.1.1: identical.

Absence control: `grep -rhoE 'MigrateStep|GetNextMigrationLeg|migration_dest'` counts 0 / 0 / 22 across the three builds. Single definition check: the key names are defined only under `Src/Lua` in both 1.0.7 and 1.1.1, with no override in `DLC/`, `Data/` or `CommonLua/`.

| Declaration | File | 1.0.7 | 1.1.0 | 1.1.1 | 1.0.7->1.1.0 | 1.1.0->1.1.1 |
|---|---|---|---|---|---|---|
| `Colonist:SetDome` | Units/Colonist.lua | 329-390 | 396-463 | 399-466 | body changed | identical |
| `Colonist:Abandoned` | Units/Colonist.lua | 1128-1184 | 1431-1491 | 1434-1494 | body changed | identical |
| `Colonist:Arrive` | Units/Colonist.lua | 1254-1300 | 1586-1632 | 1589-1635 | whitespace only | identical |
| `Colonist:TryToEmigrateToDome` | Units/Colonist.lua | 1546-1592 | 1886-1983 | 1894-1982 | body changed | body changed |
| `Colonist:BookShuttleRide` | Units/Colonist.lua | absent | absent | 1986-2012 | n/a | added |
| `Colonist:StartShuttleLeg` | Units/Colonist.lua | absent | absent | 2016-2029 | n/a | added |
| `Colonist:MigrateByTrain` | Units/Colonist.lua | 1594-1597 | 1985-1988 | 2031-2034 | identical | identical |
| `Colonist:TryToEmigrate` | Units/Colonist.lua | 1599-1615 | 1990-2019 | 2036-2077 | signature changed | body changed |
| `Colonist:StartMigration` | Units/Colonist.lua | absent | absent | 2080-2116 | n/a | added |
| `CanBoardTrainLeg` | Units/Colonist.lua | absent | absent | 2122-2126 | n/a | added |
| `Colonist:FailMigrationStep` | Units/Colonist.lua | absent | absent | 2129-2137 | n/a | added |
| `Colonist:AbortMigration` | Units/Colonist.lua | absent | absent | 2140-2151 | n/a | added |
| `Colonist:MigrateStep` | Units/Colonist.lua | absent | absent | 2155-2221 | n/a | added |
| `Colonist:CancelResidenceReservation` | Units/Colonist.lua | 1617-1622 | 2021-2026 | 2223-2228 | identical | identical |
| `Colonist:CancelWorkReservation` | Units/Colonist.lua | absent | 2028-2034 | 2230-2236 | added | identical |
| `Colonist:ClearTransportRequest` | Units/Colonist.lua | 1624-1635 | 2036-2054 | 2238-2256 | body changed | identical |
| `Colonist:Idle` | Units/Colonist.lua | 1770-1937 | 2212-2389 | 2411-2588 | body changed | identical |
| `Colonist:IsHomeless` | Units/Colonist.lua | 2274-2276 | 2881-2883 | 3085-3087 | identical | identical |
| `Colonist:UpdateHomelessLabels` | Units/Colonist.lua | 2278-2289 | 2885-2896 | 3089-3100 | whitespace only | identical |
| `Colonist:SetResidence` | Units/Colonist.lua | 2291-2307 | 2898-2917 | 3102-3121 | body changed | identical |
| `Colonist:UpdateResidence` | Units/Colonist.lua | 2309-2317 | 2919-2927 | 3123-3131 | body changed | identical |
| `Colonist:CheckForcedDome` | Units/Colonist.lua | 2320-2327 | 2930-2937 | 3134-3141 | identical | identical |
| `Colonist:CheckForcedResidence` | Units/Colonist.lua | 2329-2342 | 2939-2952 | 3143-3156 | body changed | identical |
| `Colonist:CheckForcedWorkplace` | Units/Colonist.lua | 2344-2356 | 2954-2966 | 3158-3170 | body changed | identical |
| `FindTransportationModeToCommunity_BeforeTrains` | Units/Colonist.lua | 2467-2476 | 3111-3120 | 3315-3324 | identical | identical |
| `OnMsg.TrainRoutesRebuilt` | Units/Colonist.lua | 2480-2482 | 3124-3126 | 3328-3330 | identical | identical |
| `OnMsg.DomesConnected` | Units/Colonist.lua | 2483-2485 | 3127-3129 | 3331-3333 | identical | identical |
| `OnMsg.DomesDisconnected` | Units/Colonist.lua | 2486-2488 | 3130-3132 | 3334-3336 | identical | identical |
| `InvalidateTransportCacheOnTrainLabel` | Units/Colonist.lua | absent | 3134-3138 | 3338-3342 | added | identical |
| `InvalidateTransportCacheForRocket` | Units/Colonist.lua | absent | 3142-3146 | 3346-3350 | added | identical |
| `SavegameFixups.InvalidateTransportModeToCommunityCache` | Units/Colonist.lua | absent | 3152-3154 | 3356-3358 | added | identical |
| `is_identical` | Units/Colonist.lua | 2490-2502 | 3156-3168 | 3360-3372 | identical | identical |
| `FindTransportationModeToCommunity` | Units/Colonist.lua | 2504-2538 | 3170-3204 | 3374-3408 | whitespace only | identical |
| `GetTransportationModeToCommunity` | Units/Colonist.lua | 2540-2553 | 3206-3219 | 3410-3423 | identical | identical |
| `CanReachByTrain` | Units/Colonist.lua | 2555-2567 | 3221-3233 | 3425-3437 | identical | identical |
| `Colonist:PickEmigrationCommunity` | Units/Colonist.lua | 2569-2578 | 3235-3244 | 3439-3448 | whitespace only | identical |
| `BeyondWalkRange` | Units/Colonist.lua | absent | 3254-3259 | 3458-3463 | added | identical |
| `CanUseNode` | Units/Colonist.lua | absent | absent | 3467-3475 | n/a | added |
| `AddReachableNode` | Units/Colonist.lua | absent | absent | 3478-3486 | n/a | added |
| `AddNodesInWalkDist` | Units/Colonist.lua | absent | 3261-3309 | 3488-3532 | added | body changed |
| `InitReachableNodes` | Units/Colonist.lua | absent | 3311-3324 | 3534-3554 | added | body changed |
| `AddReachableTrainDest` | Units/Colonist.lua | absent | 3326-3331 | 3556-3558 | added | signature changed |
| `AddReachableTrainDestsOnTrack` | Units/Colonist.lua | absent | 3334-3338 | 3561-3565 | added | body changed |
| `ExpandReachableNodesFrom` | Units/Colonist.lua | absent | 3340-3398 | 3567-3607 | added | body changed |
| `BuildReachableGraph` | Units/Colonist.lua | absent | 3400-3423 | 3609-3662 | added | body changed |
| `GetNextLegToward` | Units/Colonist.lua | absent | absent | 3667-3706 | n/a | added |
| `Colonist:GetNextMigrationLeg` | Units/Colonist.lua | absent | absent | 3709-3717 | n/a | added |
| `Colonist:GetBestReachableCommunities` | Units/Colonist.lua | absent | 3425-3495 | 3719-3789 | added | identical |
| `Colonist:FindEmigrationDome` | Units/Colonist.lua | 2581-2699 | 3497-3527 | 3791-3821 | signature changed | body changed |
| `TransportByFootDtor` | Units/Colonist.lua | absent | 3529-3539 | 3823-3833 | added | identical |
| `Colonist:TransportByFoot` | Units/Colonist.lua | 2705-2748 | 3541-3586 | 3835-3880 | body changed | identical |
| `IsTransportAvailableBetween` | Units/Colonist.lua | 2750-2760 | 3588-3598 | 3882-3892 | identical | identical |
| `Colonist:IsTransported` | Units/Colonist.lua | 2762-2773 | 3600-3613 | 3894-3907 | body changed | identical |
| `Colonist:IsWaitingTransport` | Units/Colonist.lua | 2775-2787 | 3615-3630 | 3909-3924 | body changed | identical |
| `Colonist:WaitTransport` | Units/Colonist.lua | 2791-2811 | 3634-3657 | 3928-3961 | body changed | body changed |
| `Colonist:Transport` | Units/Colonist.lua | 2813-2850 | 3659-3702 | 3963-4013 | body changed | body changed |
| `Colonist:CanReachByTrainOrOnFoot` | Units/Colonist.lua | 3199-3204 | 4005-4010 | 4319-4324 | identical | identical |
| `Colonist:CanReachDomeForBuilding` | Units/Colonist.lua | 3207-3230 | 4013-4036 | 4327-4355 | whitespace only | body changed |
| `Colonist:SetForcedDome` | Units/Colonist.lua | 3232-3236 | 4038-4042 | 4357-4361 | identical | identical |
| `Colonist:SelectEmigrationDome` | Units/Colonist.lua | 3318-3320 | 4117-4120 | 4437-4440 | body changed | identical |
| `Colonist:GetEmigrationDomeDisplayName` | Units/Colonist.lua | 3342-3344 | 4142-4145 | 4462-4465 | body changed | identical |
| `Colonist:Getui_command` | Units/Colonist.lua | 3498-3538 | 4351-4395 | 4672-4716 | body changed | body changed |
| `Colonist:GetExpeditionReturnDome` | Units/Colonist.lua | absent | 5047-5059 | 5389-5401 | added | identical |
| `SavegameFixups.RestartStrandedColonists` | Units/Colonist.lua | absent | 5423-5429 | 5765-5771 | added | identical |
| `IsUnitInDomeRange` | Units/ColonistTransport.lua | 19-28 | 19-28 | 19-28 | identical | identical |
| `Colonist:GetStartingPoint` | Units/ColonistTransport.lua | 30-37 | 30-37 | 30-37 | identical | identical |
| `IsInWalkingDistFixRocket` | Units/ColonistTransport.lua | 39-47 | 39-47 | 39-47 | identical | identical |
| `GetTransportRoute` | Units/ColonistTransport.lua | 49-81 | 67-105 | 67-105 | signature changed | identical |
| `Colonist:SearchFurtherForTransport` | Units/ColonistTransport.lua | 83-85 | 107-109 | 107-109 | identical | identical |
| `Colonist:GetTransportRoute` | Units/ColonistTransport.lua | 87-120 | 111-144 | 111-144 | body changed | identical |
| `Colonist:GetTravelDestination` | Units/ColonistTransport.lua | 122-124 | 146-148 | 146-148 | identical | identical |
| `Colonist:SelectTravelDestination` | Units/ColonistTransport.lua | 126-128 | 150-152 | 150-152 | identical | identical |
| `Colonist:GetTravelSrcStation` | Units/ColonistTransport.lua | 130-132 | 154-156 | 154-156 | identical | identical |
| `Colonist:SelectTravelSrcStation` | Units/ColonistTransport.lua | 134-136 | 158-160 | 158-160 | identical | identical |
| `Colonist:GetTravelDstStation` | Units/ColonistTransport.lua | 138-140 | 162-164 | 162-164 | identical | identical |
| `Colonist:SelectTravelDstStation` | Units/ColonistTransport.lua | 142-144 | 166-168 | 166-168 | identical | identical |
| `Colonist:GetTravelReason` | Units/ColonistTransport.lua | 152-155 | 176-179 | 177-180 | identical | identical |
| `Colonist:GetTravelTime` | Units/ColonistTransport.lua | 157-162 | 181-186 | 182-187 | identical | identical |
| `Colonist:GetTravelTimeInHours` | Units/ColonistTransport.lua | 164-166 | 188-190 | 189-191 | identical | identical |
| `Colonist:Idle_TransportDestination` | Units/ColonistTransport.lua | 168-170 | 192-194 | 193-195 | identical | identical |
| `Colonist:Arrive_TransportDestination` | Units/ColonistTransport.lua | 172-174 | 196-198 | 197-199 | identical | identical |
| `Colonist:Arrive_TicketDestination` | Units/ColonistTransport.lua | 176-178 | 200-202 | 201-203 | identical | identical |
| `Colonist:ReturnFromExpedition_TransportDestination` | Units/ColonistTransport.lua | 180-183 | 204-207 | 205-208 | identical | identical |
| `Colonist:Work_TransportDestination` | Units/ColonistTransport.lua | 185-187 | 209-211 | 210-212 | identical | identical |
| `Colonist:UseElevator_TransportDestination` | Units/ColonistTransport.lua | 189-191 | 213-215 | 214-216 | identical | identical |
| `Colonist:MigrateByTrain_TransportDestination` | Units/ColonistTransport.lua | 193-195 | 217-219 | 218-220 | identical | identical |
| `Colonist:MigrateByTrain_TicketDestination` | Units/ColonistTransport.lua | 197-199 | 221-223 | 222-224 | identical | identical |
| `Colonist:VisitService_TransportDestination` | Units/ColonistTransport.lua | 201-203 | 225-227 | 226-228 | identical | identical |
| `Colonist:LeavingMars_TransportDestination` | Units/ColonistTransport.lua | 205-207 | 229-231 | 230-232 | identical | identical |
| `Colonist:LeavingMars_CanReachTransportDestinationOnFoot` | Units/ColonistTransport.lua | 208-210 | 232-234 | 233-235 | identical | identical |
| `Colonist:LeavingMars_TicketDestination` | Units/ColonistTransport.lua | 212-214 | 236-238 | 237-239 | identical | identical |
| `Colonist:Rest_TransportDestination` | Units/ColonistTransport.lua | 216-218 | 240-242 | 241-243 | identical | identical |
| `Colonist:Roam_TransportDestination` | Units/ColonistTransport.lua | 220-222 | 244-246 | 245-247 | identical | identical |
| `Colonist:HasLocalAccess` | Units/ColonistTransport.lua | 224-264 | 269-299 | 270-300 | body changed | identical |
| `Colonist:DisembarkOnArrival` | Units/ColonistTransport.lua | 266-297 | 321-352 | 322-353 | identical | identical |
| `Colonist:StartTransport` | Units/ColonistTransport.lua | 299-315 | 354-371 | 355-372 | body changed | identical |
| `Colonist:SetCommand` | Units/ColonistTransport.lua | 325-411 | 381-502 | 382-503 | body changed | identical |
| `Colonist:ShouldBoardTrain` | Units/ColonistTransport.lua | 413-424 | 504-515 | 505-516 | whitespace only | identical |
| `Colonist:GoToDome` | Units/ColonistTransport.lua | 426-428 | 528-539 | 529-540 | body changed | identical |
| `Colonist:GoToStation` | Units/ColonistTransport.lua | 430-468 | 541-582 | 542-583 | body changed | identical |
| `Colonist:WaitForTransport` | Units/ColonistTransport.lua | 470-501 | 584-612 | 585-613 | body changed | identical |
| `Colonist:BoardVehicle` | Units/ColonistTransport.lua | 503-528 | 614-639 | 615-641 | identical | body changed |
| `Colonist:DiscardTransportTicket` | Units/ColonistTransport.lua | 530-538 | 641-658 | 643-660 | signature changed | identical |
| `Colonist:ExitVehicle` | Units/ColonistTransport.lua | 540-571 | 660-699 | 662-712 | body changed | body changed |
| `Colonist:EnterBuilding` | Units/ColonistTransport.lua | 573-619 | 701-751 | 714-764 | body changed | identical |
| `Colonist:SetHolder` | Units/ColonistTransport.lua | 621-631 | 753-763 | 766-776 | body changed | identical |
| `Colonist:TryToEmigrateByTrain` | Units/ColonistTransport.lua | 633-639 | 781-802 | 794-815 | body changed | identical |
| `CanTrainTravelBetween` | Units/ColonistTransport.lua | absent | 51-65 | 51-65 | added | identical |
| `IsDestinationInCommunityRange` | Units/ColonistTransport.lua | absent | 248-258 | 249-259 | added | identical |
| `HasAccessViaCommunity` | Units/ColonistTransport.lua | absent | 261-267 | 262-268 | added | identical |
| `Colonist:MarkServiceUnreachable` | Units/ColonistTransport.lua | absent | 303-314 | 304-315 | added | identical |
| `Colonist:IsServiceMarkedUnreachable` | Units/ColonistTransport.lua | absent | 316-319 | 317-320 | added | identical |
| `Colonist:TeleportToDomeOnRepeatedEnterFails` | Units/ColonistTransport.lua | absent | 519-526 | 520-527 | added | identical |
| `Colonist:KickFromBuilding` | Units/ColonistTransport.lua | absent | 765-770 | 778-783 | added | identical |
| `SavegameFixups.DiscardTicketsToDestroyedTrains` | Units/ColonistTransport.lua | absent | 772-779 | 785-792 | added | identical |
| `Colonist:GetReachableStrandedStation` | Units/ColonistTransport.lua | absent | 805-817 | 818-830 | added | identical |
| `Colonist:Stranded` | Units/ColonistTransport.lua | absent | 824-890 | 871-945 | added | body changed |
| `Colonist:IsInSafeAtmosphere` | Units/ColonistTransport.lua | absent | absent | 836-842 | n/a | added |
| `Colonist:TryToMigrateHome` | Units/ColonistTransport.lua | absent | absent | 848-867 | n/a | added |
| `BuildStorableResourcesArray` | LRTransport.lua | 7-44 | 7-18 | 7-18 | body changed | identical |
| `ColonistTransportTask:CanExecute` | LRTransport.lua | 58-64 | 35-41 | 36-42 | body changed | identical |
| `ColonistTransportTask:Cleanup` | LRTransport.lua | 66-78 | 62-83 | 63-84 | body changed | identical |
| `CreateColonistTransportTask` | LRTransport.lua | 80-101 | 85-123 | 86-124 | body changed | identical |
| `ColonistTransportTask:IsObsolete` | LRTransport.lua | absent | 43-60 | 44-61 | added | identical |
| `SavegameFixups.StampColonistTransportTaskCreationTime` | LRTransport.lua | absent | 132-139 | 133-140 | added | identical |
| `LRManager:AddColonistTransportRequest` | LRManager.lua | 43-45 | 42-44 | 43-45 | identical | identical |
| `LRManager:RemoveColonistTransportRequest` | LRManager.lua | 47-49 | 46-48 | 47-49 | identical | identical |
| `LRManager:ExpireColonistTransportTasks` | LRManager.lua | absent | 50-63 | 51-64 | added | identical |
| `SetNetwork` | Passage.lua | 1087-1094 | absent | absent | removed | n/a |
| `CreateDomeNetworks` | Passage.lua | 1096-1107 | absent | absent | removed | n/a |
| `AreDomesConnectedWithPassage` | Passage.lua | 1109-1119 | 1266-1273 | 1267-1274 | body changed | identical |
| `PassageWave` | Passage.lua | 1121-1141 | 1275-1297 | 1276-1298 | body changed | identical |
| `GetDomesPassagePath` | Passage.lua | 1143-1172 | 1299-1329 | 1300-1330 | body changed | identical |
| `PassageBase:TraverseTunnel` | Passage.lua | 1037-1066 | 1200-1247 | 1201-1248 | signature changed | identical |
| `PassageBase:DisconnectDomes` | Passage.lua | 1228-1253 | 1387-1404 | 1388-1405 | body changed | identical |
| `PassageBase:DisconnectDomePair` | Passage.lua | absent | 1406-1432 | 1407-1433 | added | identical |
| `PassageBase:DisconnectDomeFromHub` | Passage.lua | absent | 1434-1443 | 1435-1444 | added | identical |
| `PassageBase:TryConnectDomes` | Passage.lua | 1318-1346 | 1513-1526 | 1514-1527 | body changed | identical |
| `PassageBase:DoConnectDomes` | Passage.lua | absent | 1528-1554 | 1529-1555 | added | identical |
| `PassageBase:ConnectDomes` | Passage.lua | 1348-1369 | 1557-1570 | 1558-1571 | signature changed | identical |
| `PassageBase:ConnectDomePair` | Passage.lua | absent | 1572-1590 | 1573-1591 | added | identical |
| `PassageBase:ConnectDomeToHub` | Passage.lua | absent | 1592-1600 | 1593-1601 | added | identical |
| `GetNumConnectedDomes` | Passage.lua | 2099-2117 | 2397-2399 | 2398-2400 | body changed | identical |
| `GetNumDomesConnectedToDome` | Passage.lua | 2119-2125 | 2401-2403 | 2402-2404 | body changed | identical |
| `CheckWalkableDistance` | Buildings/Dome.lua | 177-199 | 209-231 | 209-231 | body changed | identical |
| `IsConnectedByFoot` | Buildings/Dome.lua | absent | 235-240 | 235-240 | added | identical |
| `CheckWalkableDistanceCached` | Buildings/Dome.lua | absent | 244-251 | 244-251 | added | identical |
| `IsInWalkingDist` | Buildings/Dome.lua | 240-242 | 295-297 | 295-297 | identical | identical |
| `IsInWalkingDistDome` | Buildings/Dome.lua | 244-262 | 299-319 | 299-319 | body changed | identical |
| `GetTransportThroughElevator` | Buildings/Dome.lua | 264-335 | 321-393 | 321-393 | body changed | identical |
| `AreDomesConnected` | Buildings/Dome.lua | 356-358 | absent | absent | removed | n/a |
| `Dome:InitPassageTables` | Buildings/Dome.lua | 560-565 | 678-684 | 678-684 | body changed | identical |
| `Dome:UpdateConnectedNetwork` | Buildings/Dome.lua | absent | 688-706 | 688-706 | added | identical |
| `Dome:GetConnectedDomes` | Buildings/Dome.lua | 619-644 | absent | absent | removed | n/a |
| `Dome:GetClusterDomes` | Buildings/Dome.lua | absent | 745-747 | 745-747 | added | identical |
| `Dome:IsInClusterWith` | Buildings/Dome.lua | absent | 749-751 | 749-751 | added | identical |
| `Dome:OnSetWorking` | Buildings/Dome.lua | 1620-1637 | 2029-2037 | 2069-2077 | body changed | identical |
| `Dome:OnSetUIWorking` | Buildings/Dome.lua | absent | absent | 1905-1912 | n/a | added |
| `Dome:CheckWorkForUnemployed` | Buildings/Dome.lua | absent | absent | 1914-1919 | n/a | added |
| `Dome:KickWorkersFromBlockedBuildings` | Buildings/Dome.lua | absent | absent | 1921-1935 | n/a | added |
| `Dome:TestColonistLRTransport` | Buildings/Dome.lua | 2175-2191 | 2535-2551 | 2575-2591 | whitespace only | identical |
| `Dome:HasFreeLivingSpace` | Buildings/Dome.lua | 2836-2838 | 3357-3359 | 3478-3480 | identical | identical |
| `Dome:ReserveResidence` | Buildings/Dome.lua | 2840-2851 | 3361-3372 | 3482-3493 | identical | identical |
| `ConsiderWorkplaceReservation` | Buildings/Dome.lua | absent | 3375-3391 | 3496-3512 | added | body changed |
| `Dome:ReserveWorkplace` | Buildings/Dome.lua | absent | 3395-3416 | 3516-3537 | added | identical |
| `Residence:AddResident` | Buildings/Residence.lua | 68-81 | 104-117 | 105-118 | identical | identical |
| `Residence:RemoveResident` | Buildings/Residence.lua | 83-90 | 119-126 | 120-127 | identical | identical |
| `Residence:CheckHomeForHomeless` | Buildings/Residence.lua | 124-132 | 160-168 | 161-169 | identical | identical |
| `Residence:CanReserveResidence` | Buildings/Residence.lua | 250-255 | 283-288 | 284-289 | body changed | identical |
| `Residence:ReserveResidence` | Buildings/Residence.lua | 257-274 | 290-307 | 291-308 | identical | identical |
| `Residence:CancelResidenceReservation` | Buildings/Residence.lua | 353-365 | 385-399 | 386-400 | body changed | identical |
| `SavegameFixups.RemoveReservedInSameResidence` | Buildings/Residence.lua | 591-599 | 634-642 | 635-643 | identical | identical |
| `Community:CanAcceptNewColonists` | Buildings/Community.lua | 61-63 | 96-98 | 96-98 | identical | identical |
| `Community:HasAnyFreeLivingSpace` | Buildings/Community.lua | absent | 366-384 | 366-384 | added | identical |
| `Community:HasFreeLivingSpaceFor` | Buildings/Community.lua | 334-351 | 402-418 | 402-418 | signature changed | identical |
| `Community:CanVisit` | Buildings/Community.lua | 353-355 | 420-422 | 420-422 | identical | identical |
| `Community:GetClusterDomes` | Buildings/Community.lua | absent | 569-571 | 569-571 | added | identical |
| `Workplace:CancelWorkReservation` | Buildings/Workplace.lua | absent | 532-551 | 538-557 | added | identical |
| `HasShuttleLandingSlots` | Buildings/ShuttleHub.lua | absent | 110-112 | 110-112 | added | identical |
| `IsLRTransportAvailable` | Buildings/ShuttleHub.lua | 350-359 | 410-419 | 410-419 | identical | identical |
| `CargoShuttle:TransportColonist` | Buildings/ShuttleHub.lua | 635-771 | 736-940 | 742-946 | body changed | identical |
| `GetDomesReachableByColonists` | _GameUtils.lua | 346-423 | 390-483 | 390-483 | body changed | identical |
| `ChooseDome` | _GameUtils.lua | 426-441 | 486-501 | 486-501 | signature changed | identical |
| `RocketBase:Disembark` | Buildings/RocketBase.lua | 1980-1991 | 1969-1988 | 1969-1988 | body changed | identical |
| `RocketBase:GenerateArrivals` | Buildings/RocketBase.lua | 2021-2094 | 2018-2092 | 2018-2092 | body changed | identical |
| `RocketBase:EjectColonists` | Buildings/RocketBase.lua | 2096-2116 | 2094-2117 | 2094-2117 | body changed | identical |
| `CargoTransporterNew:GenerateArrivals` | CargoTransporterNew.lua | 860-940 | 950-1032 | 953-1035 | body changed | identical |
| `CargoTransporterNew:EjectColonists` | CargoTransporterNew.lua | 942-962 | 1034-1059 | 1037-1062 | body changed | identical |
| `CargoTransporterNew:UnloadPassengers` | CargoTransporterNew.lua | 964-1000 | 1073-1118 | 1076-1121 | body changed | identical |
| `UniversalRocketBase:IsColonistValidForDeparture` | UniversalRocket.lua | absent | 2207-2217 | 2213-2223 | added | identical |
| `FindStopoverDomeForRocket` | UniversalRocket.lua | absent | 2219-2233 | 2225-2239 | added | identical |
| `UniversalRocketBase:GenerateDepartures` | UniversalRocket.lua | 1867-1911 | 2235-2270 | 2241-2276 | body changed | identical |
| `UniversalRocketBase:PurgeStopoverDepartures` | UniversalRocket.lua | absent | 2272-2310 | 2278-2316 | added | identical |
| `SupplyRocketBase:GenerateDepartures` | Buildings/SupplyRocket.lua | 31-78 | 31-78 | 31-78 | body changed | identical |

## 2. 1.0.7 -> 1.1.0 changes

Grouped by subsystem. Every step-1 row that is not `identical` is covered. Unless a line says otherwise, 1.0.7 line numbers are on the left and 1.1.0 on the right.

### 2.1 Choosing a destination: graph-based selection replaces per-candidate mode lookup

- **`Colonist:FindEmigrationDome`** `Units/Colonist.lua:2581-2699 (1.0.7)` -> `:3497-3527 (1.1.0)`, signature `(current_dome)` -> `(current_dome, force_leave)`.
  - **1.0.7:** builds the candidate list from `city.labels.Community` plus the communities in the other city of each valid elevator (`:2595-2618`). It keeps only candidates for which `FindTransportationModeToCommunity(community, pos, with_shuttles, source_city)` returns a mode (`:2662-2663`). Scoring happens inline, and `PickEmigrationCommunity` returns `(community, mode, dist, elevator)`.
  - **1.1.0:** candidates are the Community nodes of `BuildReachableGraph`, scored by the new `GetBestReachableCommunities`. Then **one** cached mode lookup is made for the chosen dome:

    ```lua
    local shuttles_available = not forced_dome and (chosen_dome.city == my_city) and IsLRTransportAvailable(my_city)
    local mode, mode_dist, elevator = FindTransportationModeToCommunity(chosen_dome, pos, shuttles_available, my_city)
    ```

    (`:3524-3525 (1.1.0)`). A forced dome still passes shuttles off, as 1.0.7 did (`nil` at `:2591 (1.0.7)`).
- **`Colonist:GetBestReachableCommunities`** (added, `:3425-3495 (1.1.0)`) is the 1.0.7 scoring loop moved out, with these changes:
  - scores via `GetScoreFor(self)` instead of `(traits)`;
  - the baseline is `g_Consts.CommunityEvalNone` instead of `-1`;
  - `force_leave` (Stranded) stops the home dome scoring as a "stay" option;
  - non-workers skip the workplace scans.
- **The reachable-graph helpers** are all added: `BeyondWalkRange` `:3254-3259`, `AddNodesInWalkDist` `:3261-3309`, `InitReachableNodes` `:3311-3324`, `AddReachableTrainDest` `:3326-3331`, `AddReachableTrainDestsOnTrack` `:3334-3338`, `ExpandReachableNodesFrom` `:3340-3398`, `BuildReachableGraph` `:3400-3423` (all 1.1.0). This is a BFS over:
  - the start dome;
  - domes, stations and elevators within `g_Consts.ColonistMaxDomeWalkDist` of the start (`AddNodesInWalkDist`, with a straight-line pre-reject);
  - cluster domes (`Dome:GetClusterDomes`), expanded only from a node that was not itself reached on foot;
  - stations connected to domes;
  - stations along tracks with at least one train (`GetTrainsOnRoute(track) > 0`);
  - elevator `other` ends.

  The graph stores only `node -> arrival mode`, with no predecessor. **Shuttle nodes are added once, after the BFS, for Communities only, in the colonist's own city, and are never expanded:**

  ```lua
  if arrived_by == "shuttle" then return end                         -- ExpandReachableNodesFrom :3342
  ...
  if IsLRTransportAvailable(colonist.city) then
      for _, community in ipairs(colonist.city.labels.Community) do  -- BuildReachableGraph :3408-3415
  ```

  The walk-distance pass from the current dome runs **after** the shuttle fill (`:3417-3420`). So a dome that is both walkable and shuttle-reachable keeps "shuttle" as its arrival mode in the graph. The mode is not used for execution in 1.1.0.
- **`Colonist:PickEmigrationCommunity`**: whitespace only. It has no caller in 1.1.0 (see §4).
- **`FindTransportationModeToCommunity`**: whitespace only. Cache key still `[community][pos]`, no shuttle flag (`:3197-3203 (1.1.0)`).
- **Cache invalidation added:**
  - `InvalidateTransportCacheOnTrainLabel` (`:3134-3138`) flushes the whole cache when a `Train` label object is added or removed;
  - `InvalidateTransportCacheForRocket` (`:3142-3146`) drops `cache[rocket]` on RocketLanded / RocketLaunched / RocketLaunchedAnywhere;
  - `SavegameFixups.InvalidateTransportModeToCommunityCache` (`:3152-3154`) runs a one-time flush;
  - `TryToEmigrateByTrain` also flushes when no route is found (`Units/ColonistTransport.lua:789 (1.1.0)`).

  There is still no flush on shuttle-hub construction, fuel or switching.

### 2.2 Executing the move (single-hop in both builds)

- **`Colonist:TryToEmigrate`** `:1599-1615 (1.0.7)` -> `:1990-2019 (1.1.0)`, gains `force_leave`. New early returns:
  - the colonist is mid `BoardVehicle`/`ExitVehicle` with a live vehicle (`:1991-1998`);
  - the colonist holds a `departure_rocket` shuttle task and this is not a forced leave (`:2001-2004`).

  `emigration_elevator` is cleared when no destination is found.
- **`Colonist:TryToEmigrateToDome`** `:1546-1592 (1.0.7)` -> `:1886-1983 (1.1.0)`. Changes:
  1. `need_work` workplace reservation, alongside every residence reservation (`:1896`, `:1920-1926`, `:1943-1949`, `:1972-1978`).
  2. The walk branch is skipped once a shuttle owns the task, unless an elevator is involved (`:1898`).
  3. Constants are read from `g_Consts` (`:1901-1902`).
  4. `transport_mode_dist < 0` (no outside route) is treated as `max_int`, which forces the passage lookup (`:1904-1907`).
  5. `DiscardTransportTicket()` runs before the walk (`:1918`).
  6. The existing-task ladder handles cross-map tasks, an unchanged destination, and pads missing at the destination (`HasShuttleLandingSlots`). It retargets `emigration_dome` while a `Transport` is under way (`:1932-1957`).
  7. The source pad is `current_dome` if it has pads, else the nearest pad-bearing Community other than the destination, else `self.dome` (`:1959-1968`).

  The vacuum threshold expression is unchanged from 1.0.7: `min_dist = GetAtmosphereBreathable(...) and dome_passage_dist or dome_walk_dist` (`:1560 (1.0.7)`, `:1903 (1.1.0)`).
- **`Colonist:TryToEmigrateByTrain`** `Units/ColonistTransport.lua:633-639 (1.0.7)` -> `:781-802 (1.1.0)`:
  - validates `emigration_elevator`;
  - resolves the route **before** committing (`GetTransportRoute(target, "MigrateByTrain")`) and flushes the transport cache on failure;
  - `DiscardTransportTicket`;
  - reserves the residence with `(residence.parent_dome or residence) ~= dest_dome`, which fixes the MicroG/habitat comparison;
  - reserves a workplace for job-seekers.
- **`Colonist:MigrateByTrain`**: identical. It re-issues `TransportByFoot(destination, ...)` after the train.
- **`Colonist:TransportByFoot`** `:2705-2748 (1.0.7)` -> `:3541-3586 (1.1.0)`:
  - the inline destructor becomes the named `TransportByFootDtor` (added, `:3529-3539`), which resets dome and outside state only when the colonist failed to reach the destination's map;
  - there is an early exit if the destination dies during passage traversal;
  - a failed `EnterBuilding` falls back to `TeleportToDomeOnRepeatedEnterFails(dest_dome)`.
- **`Colonist:ClearTransportRequest`** `:1624-1635 (1.0.7)` -> `:2036-2054 (1.1.0)`:
  - also cancels the workplace reservation;
  - if the colonist is already inside the shuttle, it unloads them (`SetCarriedResource("Colonist", -1)`, `LeaveColonist`);
  - it idles the shuttle **last**, because `SetCommand` from the shuttle's own thread kills the current thread.
- **`Colonist:CancelWorkReservation`** (added, `:2028-2034 (1.1.0)`) and **`Workplace:CancelWorkReservation`** (added, `Buildings/Workplace.lua:532-551 (1.1.0)`) are the workplace half of the reservation pair.
- **`Colonist:WaitTransport`** `:2791-2811 (1.0.7)` -> `:3634-3657 (1.1.0)`: the dome assignment on completion is wrapped in `if self.emigration_dome then -- we're emigrating, not being rescued`. Failure also cancels the workplace reservation. On `state == "done"` it still calls `SetDome(emigration_dome)` without checking where the ride actually went.
- **`Colonist:Transport`** `:2813-2850 (1.0.7)` -> `:3659-3702 (1.1.0)`:
  - returns if the task is gone;
  - sets `emigration_dome` only when `dest_dome ~= self.dome` (a rescue ride home is not an emigration);
  - re-checks the task after the walk to the pickup;
  - no longer writes `task.source_dome` / `task.dest_dome` at the end.
- **`Colonist:IsTransported`** (`:3600-3613`) requires the ticket's vehicle to be valid. **`Colonist:IsWaitingTransport`** (`:3615-3630`) rejects a task whose `dest_dome` is invalid.
- **`Colonist:SelectEmigrationDome` / `GetEmigrationDomeDisplayName`** (`:4117-4120`, `:4142-4145`) fall back to `transport_task.dest_dome`. **`Colonist:Getui_command`** (`:4351-4395`) changes are cosmetic and service-related (expedition status, food-pile visit), not migration logic.

### 2.3 Triggers, homeless state and forced targets

- **`Colonist:Idle`** `:1770-1937 (1.0.7)` -> `:2212-2389 (1.1.0)`. The migration trigger is unchanged: the heavy update runs `UpdateWorkplace`, `UpdateResidence`, then `TryToEmigrate(current_dome)`. Otherwise `TryToEmigrate` runs when `user_forced_dome` is set (`:2348-2352 (1.1.0)`). The other changes are unrelated: comfort-notification deferral, medical/food gating, morale rename. The shuttle-commit hand-off at the top (`transport.shuttle.dest_dome` -> `SetCommand("Transport", ...)`) is unchanged.
- **`Colonist:Abandoned`** `:1128-1184 (1.0.7)` -> `:1431-1491 (1.1.0)`:
  - `ChooseDome(self, ...)`;
  - **new `return self:SetCommand("Stranded")` when no dome and no failed dome remain** (`:1460-1463 (1.1.0)`; `:1465-1466 (1.1.1)`);
  - cancels the workplace reservation.
- **`Colonist:UpdateResidence`** (`:2919-2927`) and **`CheckForcedResidence`** (`:2939-2952`) accept a residence that is itself the community (`(home.parent_dome or home) ~= self.dome`), such as MicroG and habitats.
- **`CheckForcedWorkplace`** (`:2954-2966`) uses `dome:IsInClusterWith(service_dome)` in place of the removed `AreDomesConnected`.
- **`SetResidence` / `SetDome`** changes are comfort-notification deferral and trait-list iteration only (`:396-463`, `:2898-2917`).
- **`Colonist:Arrive` / `UpdateHomelessLabels` / `CanReachDomeForBuilding`**: whitespace only.
- **`Colonist:GetExpeditionReturnDome`** (added, `:5047-5059 (1.1.0)`): returns the dome of `expedition_residence`, else of `expedition_workplace`, when that dome is in the reachable list.
- **`SavegameFixups.RestartStrandedColonists`** (added, `:5423-5429`): restarts the `Stranded` command after a load.

### 2.4 Colonist transport lifecycle (`Units/ColonistTransport.lua`)

- **`GetTransportRoute`** `:49-81 (1.0.7)` -> `:67-105 (1.1.0)`, parameter `find_nearest` -> `allow_reachable`:
  - always picks the best (shortest) station pair instead of the first match;
  - remote stations default to the dome's cluster stations;
  - requires `CanTrainTravelBetween(s, rs)` (added, `:51-65`: a track with a train that actually visits both stations).

  `Colonist:GetTransportRoute` uses `GetClusterStations` for domes.
- **`Colonist:HasLocalAccess`** (`:269-299`) goes through the added `IsDestinationInCommunityRange` / `HasAccessViaCommunity` (`:248-267`), which use cluster domes instead of `GetConnectedDomes`. It also tries the home dome when the nearest community refuses.
- **`Colonist:SetCommand`** (`:381-502`): train legs need `CanTrainTravelBetween`; an unreachable service is cooled down by `MarkServiceUnreachable` (added, `:303-314`). **New rescue chain when home is unreachable:** a shuttle task to home (`CreateColonistTransportTask(self, false, home)`), otherwise `SetCommand("Stranded", home)` (`:460-481 (1.1.0)`).
- **`Colonist:Stranded`** (added, `:824-890 (1.1.0)`):
  - adds a notification and status effect;
  - **immediately walks into the nearest reachable Station** (`GetReachableStrandedStation`, added `:805-817`), else `ExitBuilding()`;
  - loops, trying in order: `HasLocalAccess(home)`; a single-hop train route home; a shuttle task home; `TryToEmigrate(nil, "stranded")`; finally a foot walk to the nearest `ChooseDome` pick if `IsConnectedByFoot` and the path is within `ColonistMaxDomeWalkDist * (100 + StrandedMaxWalkDistIncreasePercent)/100` (50 %).
- **`Colonist:TeleportToDomeOnRepeatedEnterFails`** (added, `:519-526`): after `dome_enter_fails >= 100`, calls `dome:RandPlaceColonist`. Callers are `GoToDome` (changed, `:528-539`) and `TransportByFoot`.
- **`DiscardTransportTicket`** (`:641-658`) gains a `mode` parameter ("arrived" / "rebooking"). It returns an outstanding meal and removes the colonist from the station queues, and no longer forces `Idle` from `GoToStation`.
- **`ExitVehicle`** (`:660-699`): handles an invalid station or vehicle (kick, `GoToDome`, or `Die`) and stamps `last_train_travel`.
- **`StartTransport`** (`:354-371`) discards the old ticket as "rebooking".
- **`GoToStation`** (`:541-582`) returns to `Idle` if the ticket vanished while walking.
- **`WaitForTransport`** (`:584-612`) replaces an inline route scan with `CanTrainTravelBetween`.
- **`SetHolder`** (`:753-763`) lets `PassageHub` hold a ticketed colonist.
- **`EnterBuilding`** (`:701-751`) skips elevators with `dist < 0`.
- **`KickFromBuilding`** (added `:765-770`) discards the ticket when kicked from a Train. **`SavegameFixups.DiscardTicketsToDestroyedTrains`** (added `:772-779`). **`ShouldBoardTrain`**: whitespace only.

### 2.5 Shuttle task struct and lifecycle (`LRTransport.lua`, `LRManager.lua`, `ShuttleHub.lua`)

- **`ColonistTransportTask`** gains `departure_rocket`, `lr_manager` and `creation_time` (`LRTransport.lua:20-33 (1.1.0)`).
  - **`CanExecute`** (`:35-41`) allows `source_dome = false` (a rescue ride) and validates `dest_dome`.
  - **`Cleanup`** (`:62-83`) tolerates an invalid colonist by searching every map's manager.
  - **`IsObsolete`** (added `:43-60`): the task is obsolete if it has no shuttle and has aged past `const.ColonistTransportTaskExpirationTime` (`= const.DayDuration`, `_GameConst.lua:144 (1.1.0)`), or if the colonist, destination or source is invalid, or the departure rocket is.
  - **`LRManager:ExpireColonistTransportTasks`** (added, `LRManager.lua:50-63 (1.1.0)`) runs hourly (`LRTransport.lua:125-130`, `const.ColonistTransportTaskExpirationCheck = const.HourDuration`). For a colonist not in `Transport` it calls `colonist:ClearTransportRequest() -- also releases the residence and workplace reservations`.
  - **`SavegameFixups.StampColonistTransportTaskCreationTime`** (added) stamps creation times on existing tasks.
  - **`BuildStorableResourcesArray`** (changed) is a resource-list helper that shares the file. It is not colonist transport.
- **`CreateColonistTransportTask`** `LRTransport.lua:80-101 (1.0.7)` -> `:85-123 (1.1.0)`:
  - refuses a destination on another map or with no landing slots (`HasShuttleLandingSlots`, added `Buildings/ShuttleHub.lua:110-112 (1.1.0)`: `IsKindOf(obj, "ShuttleLanding") and #obj.landing_slots > 0`, so Stations and Elevators with pads qualify as destinations);
  - allows `source_dome = false` (pickup at the colonist's position);
  - no longer asserts on a missing landing slot.
- **`CargoShuttle:TransportColonist`** `Buildings/ShuttleHub.lua:635-771 (1.0.7)` -> `:736-940 (1.1.0)`: 227 changed lines (`python dfn.py ... | grep -cE "^[-+][^-+]"`). It delivers a passenger who is already loaded, does not drop a passenger mid-route, and clears the colonist's request on an invalid task. It is identical in 1.1.1.

### 2.6 Walk distance, passages and clusters (`Buildings/Dome.lua`, `Passage.lua`)

- **`CheckWalkableDistance`** `Buildings/Dome.lua:177-199 (1.0.7)` -> `:209-231 (1.1.0)`: changes from `local` to global, reads `g_Consts.ColonistMaxDomeWalkDist`, and drops the path-length cap argument to `PathLenCached`. The comparison `len > dome_walk_dist` stays.
- Added: **`IsConnectedByFoot`** (`:235-240`: uncapped `PathLenCached`, `-1` when not connected) and **`CheckWalkableDistanceCached`** (`:244-251`: reads `g_DomeToDomeDist` first).
- **`IsInWalkingDistDome`** (`:299-319 (1.1.0)`): reads `g_Consts.ColonistMinDistToIgnorePassage`. The returned walkability is unchanged: `dist[1] or AreDomesConnectedWithPassage(...) and (open air or not IsLRTransportAvailable(...) or dist[2] <= min_dist_to_ignore_passage)`. The new comment documents that `dist[2] == -1` (no outside route) stays walkable via passage.
- **`GetTransportThroughElevator`** (`:321-393`): `g_Consts`, and a train leg with no foot route ranks `max_int`.
- **Removed:** `AreDomesConnected` (`:356-358 (1.0.7)`, which checked `bld1.connected_domes[bld2]` or open-air range), replaced by `Dome:IsInClusterWith` (added `:749-751`). `Dome:GetConnectedDomes` (`:619-644 (1.0.7)`) is replaced by `Dome:GetClusterDomes` (added `:745-747`: `return self.connected_domes`, **the dome plus its direct passage neighbours**).
- **`Dome:InitPassageTables`** (`:678-684`): `connected_domes` becomes `{ self }` with an array part, and there is a new `dome_network = { self, [self] = true }`. **`Dome:UpdateConnectedNetwork`** (added `:688-706`) recomputes the transitive closure on connect and disconnect.
- **Passage.lua:**
  - `SetNetwork` / `CreateDomeNetworks` (the city-level `dome_networks`, `:1087-1107 (1.0.7)`) are **removed**;
  - `AreDomesConnectedWithPassage` (`:1266-1273 (1.1.0)`) now reads `d1.dome_network[d2]`;
  - `PassageWave` and `GetDomesPassagePath` iterate `connected_domes` from index 2 (the array) instead of `pairs`;
  - `ConnectDomes` changes to `(b1, b2)` and gains hub support through the added `DoConnectDomes`, `ConnectDomePair`, `ConnectDomeToHub`, `DisconnectDomePair` and `DisconnectDomeFromHub`;
  - `GetNumConnectedDomes` / `GetNumDomesConnectedToDome` become `#dome.dome_network`;
  - `PassageBase:TraverseTunnel` (`:1200-1247 (1.1.0)`) gets the signature `(unit, end_point, end_point_map, param, element)`, lazy waypoint chains, and a PassageHub exit branch that uses `SetHolder`. The non-hub branch keeps `unit.holder = nil` (C42, §6).
- **`Dome:OnSetWorking`** (`:2029-2037`) drops the consumer and marker calls. Dome switch-off emigration is not a Dome method in any build: it is the `my_dome.ui_working or GameTime() - my_dome.ui_working_changed < wait_dome_turned_off` gate inside the emigration scoring (`:2637 (1.0.7)`, `GetBestReachableCommunities :3730 (1.1.1)`). **`Dome:TestColonistLRTransport`** (the `CreateColonistTransportTask` caller at `:2587 (1.1.1)`, a debug or test action) changed only in whitespace.
- **`Dome:ReserveWorkplace` / `ConsiderWorkplaceReservation`** (added, `:3375-3416 (1.1.0)`) hold the best free slot in the cluster, preferring a specialist match, then priority.

### 2.7 Residence and Community reservation helpers

- **`Residence:CanReserveResidence`** (`:283-288 (1.1.0)`) uses `IsSuitable(unit)` instead of the exclusive-trait test.
- **`Residence:CancelResidenceReservation`** (`:385-399`) also clears `unit.expedition_residence`.
- `ReserveResidence`, `RemoveResident`, `AddResident` and `CheckHomeForHomeless` are identical.
- **`Community:HasFreeLivingSpaceFor(traits)` -> `(colonist)`** (`Buildings/Community.lua:402-418 (1.1.0)`) now walks residences with `working`, `GetFreeSpace() > 0` and `IsSuitable`. `HasAnyFreeLivingSpace` is added (`:366-384`), and so is `Community:GetClusterDomes` (`:569-571`).

### 2.8 Arrival, expedition return and departure dome choice

- **`GetDomesReachableByColonists`** `_GameUtils.lua:346-423 (1.0.7)` -> `:390-483 (1.1.0)`:
  - skips communities with `dist < 0` for the safety pick;
  - the safety dome must have `can_be_safety_dome`;
  - elevator candidates with no foot route are kept only when a train reaches them, ranked `no_foot_route_dist`;
  - train-reachable domes expand to their cluster domes.

  **`ChooseDome(traits, ...)` -> `(colonist, ...)`** (`:486-501`) uses the `CommunityEvalNone` baseline.
- **`RocketBase:Disembark`** (`Buildings/RocketBase.lua:1969-1988 (1.1.0)`) and **`CargoTransporterNew:UnloadPassengers`** (`:1073-1118`) try `unit:GetExpeditionReturnDome(domes)` first, then `ChooseDome`, and reserve the chosen dome so the next returnee sees reduced space. **`GenerateArrivals` / `EjectColonists`** on both classes use `ChooseDome(applicant, ...)` and reserve the result.
- **`UniversalRocketBase:GenerateDepartures`** (`UniversalRocket.lua:2235-2270 (1.1.0)`):
  - eligibility moves to `IsColonistValidForDeparture` (added `:2207-2217`);
  - a colonist who cannot walk or ride a train to the rocket gets a **stopover** shuttle ride: `FindStopoverDomeForRocket` (added `:2219-2233`) picks the nearest dome from which `FindTransportationModeToCommunity(rocket, dome, false, city)` is walk or train. That becomes `CreateColonistTransportTask(colonist, src_dome, stopover)` with `departure_rocket = self`.
  - `PurgeStopoverDepartures` (added `:2272-2310`) bounds how long the rocket waits.
- **`SupplyRocketBase:GenerateDepartures`** (`Buildings/SupplyRocket.lua:31-78`) only adds a nil guard.

## 3. 1.1.0 -> 1.1.1 changes: the multi-leg migration rewrite

Thirty-three rows changed in this step: 16 added, 16 body changed, 1 signature changed. 157 are identical. Everything the rewrite touches is in `Units/Colonist.lua`, `Units/ColonistTransport.lua` and one field in `LRTransport.lua`. `Buildings/Dome.lua` has four additions (`OnSetUIWorking`, `CheckWorkForUnemployed`, `KickWorkersFromBlockedBuildings`, `SavegameFixups.KickWorkersFromTurnedOffDomes`, at `:1905-1943`); they kick workers out of a switched-off dome's blocked workplaces and do not start emigration. `ConsiderWorkplaceReservation` swaps `ValidateBuilding` for `ValidateWorkplace` (`:3497`). The rest of the 1.1.0 -> 1.1.1 changes in `Buildings/Dome.lua` are UI or stats code, outside this scope.

### 3.1 Old model (1.0.7, and 1.1.0 execution) versus new model (1.1.1)

**Old: one destination, one transport mode, decided up front.** `TryToEmigrate` obtains `(dest, mode, dist, elevator)`. That tuple comes from `FindTransportationModeToCommunity`, cached per `[dest][start dome]`. The mode is one of:

- `walk`: straight into the destination, optionally through a passage path, optionally through one elevator whose far side is walkable;
- `shuttle`: one ride;
- `train`: one station pair (`GetTransportRoute` / `CanReachByTrain`), optionally after one elevator;
- `false`.

Execution is a single command: `TransportByFoot`, a shuttle task, or `MigrateByTrain`, which becomes `TransportByFoot` at the far station. The colonist carries no journey state apart from `emigration_dome` and `emigration_elevator`. In 1.1.0 the candidate set came from the multi-hop graph, but this single-mode execution was unchanged.

**New: plan a route, execute the first leg, re-plan at every stop.**

- `BuildReachableGraph` now records a predecessor for every node (`reachable.prev`, written once by `AddReachableNode`, `Units/Colonist.lua:3478-3486 (1.1.1)`).
- `GetNextLegToward` (`:3667-3706`) walks that chain back from the destination to the first node after the start. It returns one of `{kind="walk", dome, final}`, `{kind="train", src_station, dst_station}`, `{kind="elevator", elevator}` or `{kind="shuttle", landing}`.
- `FindEmigrationDome` returns `(dome, leg)` (`:3791-3821`).
- `StartMigration` reserves the residence and workplace at the **final** destination, sets `emigration_dome`, and executes the first leg.
- `MigrateStep` loops up to `max_migration_legs_per_step = 8` legs per invocation (`:2118`). For each leg it **rebuilds the graph** through `GetNextMigrationLeg(dest)` (`:3709-3717`), then:
  - walk and elevator legs run inline;
  - a train leg hands over to the ticket system, which re-issues `MigrateStep` on arrival;
  - a shuttle leg to an intermediate pad books a ride and returns; the ride, when it lands, re-issues `MigrateStep` from `Transport`;
  - the final shuttle or walk leg goes through the old `TryToEmigrateToDome`.

Journey state lives in:

- `emigration_dome`;
- `migration_step_fails` (`max_migration_step_fails = 5`, `:2119`);
- `migration_start_gt`, a guard against starting twice in the same millisecond (`:2092-2096`);
- `stranded_migration_gt`, an hourly throttle for `TryToMigrateHome`;
- `task.migration_dest` on the shuttle task.

The class defaults are at `:106-110`.

Decisive excerpts (1.1.1):

```lua
-- TryToEmigrate :2052-2076
local dest_dome, leg = self:FindEmigrationDome(current_dome, force_leave)
...
if not leg then
    -- not routable through the reachable graph (forced dome, usually): legacy single-mode routing
    local shuttles_available = not self:CheckForcedDome() and (dest_dome.city == self.city) and IsLRTransportAvailable(self.city)
    local mode, mode_dist, elevator = FindTransportationModeToCommunity(dest_dome, current_dome or self:GetNavigationPos(), shuttles_available, self.city)
    ...
end
self.emigration_elevator = nil
if leg.kind == "shuttle" and leg.landing == dest_dome or leg.kind == "walk" and leg.final then
    local _, walk_dist = IsInWalkingDistDome(dest_dome, current_dome or self:GetNavigationPos(), self.city)
    local mode = leg.kind == "shuttle" and "shuttle" or "walk"
    return self:TryToEmigrateToDome(current_dome, dest_dome, mode, walk_dist or -1)
end
return self:StartMigration(dest_dome, leg)
```

```lua
-- StartShuttleLeg :2016-2029
task = task or self:BookShuttleRide(current_dome, landing)
...
-- where the colonist carries on to after the drop-off; the ride itself only gets him to the pad
task.migration_dest = self.emigration_dome ~= task.dest_dome and self.emigration_dome or false
```

```lua
-- Transport :4009-4012 (tail)
-- only a delivered leg leaves the emigration dome set; carry the journey on from the drop-off
if IsValid(self.emigration_dome) then
    return self:SetCommand("MigrateStep", self.emigration_dome)
end
```

### 3.2 Declaration by declaration

- **`BuildReachableGraph`** `:3400-3423 (1.1.0)` -> `:3609-3662 (1.1.1)`:
  1. The walk-distance pass from the current dome now runs **before** the shuttle fill, so a directly walkable dome keeps `walk` (`:3617-3621`).
  2. Shuttle landings are **every** `Community`, `Station` and `Elevator` with landing slots (`shuttle_landing_labels`, `:1892`), not only Communities.
  3. The shuttle fill repeats until nothing new is added, **per city**: every city reached so far is checked with `IsLRTransportAvailable(city)`. A pad in another city hangs off the node that brought the colonist into that city (`entry_node`), never off the start (`:3623-3659`).
  4. Nodes reached by shuttle are expanded afterwards. In 1.1.0 `ExpandReachableNodesFrom` returned immediately for `arrived_by == "shuttle"`.
- **`ExpandReachableNodesFrom`** `:3340-3398 (1.1.0)` -> `:3567-3607 (1.1.1)`:
  - every add goes through `AddReachableNode(..., from_node)`;
  - onward train expansion from a Station is gated on `CanUseNode(node)` (`ValidateBuilding and CanWork()`) instead of `CanColonistsFromDifferentDomesWorkServiceTrainHere()`;
  - an Elevator reached by `shuttle` as well as `elevator` adds walk-distance nodes on its side (`:3586-3589`);
  - the early return for shuttle-reached nodes is gone.
- **`CanUseNode`** (added `:3467-3475`) and **`AddReachableNode`** (added `:3478-3486`):
  - a Community must pass `Community.CanVisit(node)` (in 1.1.0, communities were added unvalidated);
  - a Station must satisfy `ValidateBuilding and CanWork()`;
  - anything else must pass `ValidateBuilding`;
  - `prev` is write-once, which keeps the chains acyclic.
- **`AddNodesInWalkDist`** (`:3488-3532`) and **`InitReachableNodes`** (`:3534-3554`):
  - record predecessors;
  - stations and elevators must pass `CanUseNode`;
  - an object start (the Station, Community or Elevator holding the colonist) is seeded as a root, so the walk scan cannot rediscover it with a predecessor.
- **`AddReachableTrainDest`**: the signature gains `from_station`. **`AddReachableTrainDestsOnTrack`** passes the station as the predecessor.
- **`GetNextLegToward`** (added `:3667-3706`) returns `false` in three cases:
  - the destination is not in the graph;
  - the chain's first hop is a Station with a predecessor followed by a non-Station (`:3688-3701`);
  - the backtrack guard trips (`assert`, `:3681-3684`).

  A first node reached by `shuttle` yields a shuttle leg. That applies whichever node type it is, so a shuttle to an Elevator or Station on the way is a leg.
- **`Colonist:GetNextMigrationLeg`** (added `:3709-3717`) rebuilds the graph from `current_dome`, or else the Station holding the colonist, or else the navigation position.

  Its callers are `MigrateStep :2166`, `FindEmigrationDome :3803` (forced dome), `ExitVehicle` (`ColonistTransport.lua:679`), `TryToMigrateHome :853` and `CanReachDomeForBuilding :4330`.
- **`Colonist:FindEmigrationDome`** `:3497-3527 (1.1.0)` -> `:3791-3821 (1.1.1)`:
  - a **forced dome is now routed through the graph** (`leg = self:GetNextMigrationLeg(chosen_dome, pos)`, `:3803`);
  - scored picks take `GetNextLegToward(reachable, chosen_dome, current_dome)` from the same graph they were chosen from (`:3812`);
  - the `FindTransportationModeToCommunity` call is gone.

  The return changes from `(dome, mode, dist, elevator)` to `(dome, leg)`.
- **`Colonist:TryToEmigrate`** `:1990-2019 (1.1.0)` -> `:2036-2077 (1.1.1)`: dispatches on `leg`, as in the excerpt above. The single-mode lookup survives only for `leg == false`.
- **`Colonist:StartMigration`** (added `:2080-2116`):
  - refuses while a shuttle carries the colonist;
  - refuses when the train leg cannot be boarded (`CanBoardTrainLeg`, added `:2122-2126`);
  - refuses when the shuttle ride for this leg is already booked;
  - refuses when a journey already started this millisecond;
  - otherwise clears the transport request and ticket, reserves the residence and workplace at `dest_dome`, and sets `emigration_dome`;
  - then it either calls `StartTransport("MigrateStep", dest, nil, src, dst)` or `SetCommand("MigrateStep", dest)`.
- **`Colonist:MigrateStep`** (added `:2155-2221`). Per leg:
  - **shuttle to an intermediate landing** -> `StartShuttleLeg`, then `return` (the colonist waits in `Idle` for a shuttle to commit);
  - **shuttle to the destination, or final walk** -> `TryToEmigrateToDome(current_dome, dest, mode, walk_dist or -1)`;
  - **train** -> `StartTransport("MigrateStep", ...)`;
  - **elevator** -> `UseElevator` inline, which fails if the colonist is not on the far map;
  - **intermediate walk** -> an optional passage path, then `EnterBuilding(leg.dome)`.

  Reaching `dest_dome` hands over to `TransportByFoot(dest_dome)` to settle in (`:2216-2218`). Any failure goes to `FailMigrationStep`. The intermediate walk has its own threshold:

  ```lua
  local min_dist = GetAtmosphereBreathable(self:GetMap()) and g_Consts.ColonistMinDistToIgnorePassage or g_Consts.ColonistMaxDomeWalkDist  -- :2199
  if not dist or dist < 0 or dist > min_dist then
      passage_path = GetDomesPassagePath(current_dome, leg.dome)
  ```

  This branch applies **no** `ColonistMaxPassagePassthroughDomes` cap and **no** `IsLRTransportAvailable` alternative. It walks the passages or walks outside.
- **`Colonist:FailMigrationStep`** (added `:2129-2137`): `Sleep(1000)` then `Idle`, where the next heavy update re-plans. After 5 consecutive failures it calls **`AbortMigration`** (added `:2140-2151`), which clears `emigration_dome` and `migration_step_fails`, sets `task.migration_dest = false`, and cancels the residence and workplace reservations.
- **`Colonist:BookShuttleRide`** (added `:1986-2012`) is the 1.1.0 booking block of `TryToEmigrateToDome` (`:1959-1981 (1.1.0)`) extracted and generalised. Its landing can be any pad, and its source is the nearest pad of any label, preferring the closer across labels (`:1995-2002`). It no longer reserves anything itself; the caller does.
- **`Colonist:StartShuttleLeg`** (added `:2016-2029`): drops a task booked elsewhere with no shuttle committed, books the ride, and stamps `migration_dest`.
- **`Colonist:TryToEmigrateToDome`** `:1886-1983 (1.1.0)` -> `:1894-1982 (1.1.1)`:
  - the walk branch (`:1906-1938`) is byte-for-byte the same, including the F52 expression at `:1911`;
  - the existing-task ladder is restructured (`:1940-1970`). A committed ride now holds only against a **cross-map** or **different** destination. The case `same_dest and task.shuttle` falls through to retarget, which rewrites `task.dest_dome` (unchanged), sets `task.migration_dest = false`, and re-reserves. `emigration_dome` follows only if a journey is already under way (`self.emigration_dome or self.command == "Transport"`);
  - booking is delegated to `BookShuttleRide`, and reservations are made only on success.
- **`Colonist:WaitTransport`** `:3634-3657 (1.1.0)` -> `:3928-3961 (1.1.1)`:
  - **arrival registration now requires the ride to have gone to the emigration dome** (`state == "done" and transport_task.dest_dome == dest_dome`);
  - a delivered leg (`migration_dest` set and `done`) keeps the dome, the reservations and `emigration_dome`;
  - an undelivered leg ride releases them, as before.
- **`Colonist:Transport`** `:3659-3702 (1.1.0)` -> `:3963-4013 (1.1.1)`: `emigration_dome` is set only for a non-leg ride to a `Community`. After the destructor, a still-valid `emigration_dome` (a delivered leg) re-issues `MigrateStep`.
- **`Colonist:ExitVehicle`** (`Units/ColonistTransport.lua:662-712 (1.1.1)`): on arrival with `ticket.reason == "MigrateStep"`, if the next leg is a train from **this** station, the colonist rebooks without leaving the building (`:677-687`). Otherwise the existing tail re-issues `ticket.reason` (`MigrateStep`) with `ticket.destination` (`:702-703`).
- **`Colonist:BoardVehicle`** (`:615-641`): after charging the station's waiting time, `start_wait` is reset to board time, so the travel time measured later excludes the platform wait.
- **`Colonist:TryToMigrateHome`** (added, `Units/ColonistTransport.lua:848-867`): throttled to one plan per `const.HourDuration`. It takes a leg from `GetNextMigrationLeg(home)`, declines when there is no leg or the leg is a shuttle straight home (the caller's next option), handles a final walk via `TryToEmigrateToDome`, and otherwise calls `StartMigration(home, leg)`.
- **`Colonist:IsInSafeAtmosphere`** (added `:836-842`): the sky is breathable, or the colonist is inside a Community with life support.
- **`Colonist:Stranded`** `:824-890 (1.1.0)` -> `:871-945 (1.1.1)`:
  1. The unconditional "walk into the nearest Station" at entry is replaced by a one-time shelter step inside the loop, taken only if `not self:IsInSafeAtmosphere()` (`:909-915`).
  2. `self:TryToMigrateHome(home)` runs before the shuttle rescue (`:895-896`).
- **`Colonist:CanReachDomeForBuilding`** (`:4327-4355`): for a Residence with a parent dome ("forced migration" in the UI), the answer is `GetNextMigrationLeg(bld.parent_dome)`, which allows chained routes.
- **`Colonist:Getui_command`** (`:4672-4716`): `MigrateStep` shows the emigration status. The string is at `:4649`.

### 3.3 Situations the old code handled differently (INFERRED from source unless noted)

| Situation | 1.0.7 | 1.1.0 | 1.1.1 |
|---|---|---|---|
| Destination has a foot route of 400 m or less, or is in the passage network (IsInWalkingDistDome true) | `walk` -> `TransportByFoot`, optionally via passages | Same execution. Selection by graph; the graph's walk test is `CheckWalkableDistanceCached` (foot, 400 m or less) plus cluster neighbours | Final `walk` leg -> the same `TryToEmigrateToDome` walk branch; `walk_dist` from `IsInWalkingDistDome` instead of the cache |
| Only a shuttle reaches the destination | `shuttle` if hubs are available **and** the cache entry was made with shuttles on (F51); else not a candidate | Graph candidate if the destination has pads; the booking in `TryToEmigrateToDome` works even with a cached `false` mode | Shuttle leg with `landing == dest` -> `TryToEmigrateToDome(...,"shuttle")` -> `BookShuttleRide` |
| One direct train route | `train` -> `MigrateByTrain` -> `TransportByFoot` at the far station | Same | Train leg -> `StartTransport("MigrateStep")`; on arrival `MigrateStep` re-plans (final walk -> `TransportByFoot`) |
| Several trains with transfers, or walk -> station -> train -> walk to a non-adjacent dome | Not a candidate unless a shuttle serves it | **Chosen by the graph but not executable by the cached single mode:** falls to shuttle booking or nothing; no reservation is made when nothing is booked, and the pick repeats at the next heavy update | Executed leg by leg; a same-station transfer happens inside `ExitVehicle` |
| Elevator to another map | One elevator via `GetTransportThroughElevator` (walk, or one train, on each side); `TransportByFoot` uses the elevator, then maybe `TryToEmigrateByTrain` | Same execution; the graph sees elevator chains | Elevator leg inline in `MigrateStep`; the far side is re-planned from the new map |
| Elevator or station out of walking range but on a shuttle pad | Not representable | Not representable (shuttle only to Communities; shuttle nodes never expanded) | Shuttle leg to the pad (`StartShuttleLeg`, `migration_dest`), then the journey continues |
| Shuttles in the city on the far side of an elevator | Not considered (`with_shuttles` false across cities) | Not considered (shuttle fill only for `colonist.city`) | Pads there are added, hung off the entry node |
| User-forced dome | `FindTransportationModeToCommunity(forced, pos, nil)`: no shuttle | Same, `shuttles_available = not forced_dome` = false | Graph routing including shuttles; single-mode fallback only if the graph cannot route |
| Stranded (added 1.1.0) | n/a | Shelter in a Station first, even when inside a safe dome; single-hop only | Multi-leg home journey first (hourly throttle); shelter only when unsafe |
| A ride delivered to a different place than `emigration_dome` | `SetDome(emigration_dome)` on `done` regardless | Same | Registers the dome only if `task.dest_dome == emigration_dome`; a leg ride keeps the journey |
| Journey keeps failing | No journey state; `TransportByFoot` destructor / `Abandoned`; the shuttle task never expired (1.0.7) or expires after 1 sol (1.1.0) | Same | `FailMigrationStep` retries; the 5th failure `AbortMigration` releases the reservations |
| When the destination's residence and workplace are reserved | At the walk start or task booking | Same, plus the workplace | At journey start (`StartMigration`), **held across every leg**, including delivered shuttle legs |

### 3.4 Observations from reading the 1.1.1 code (INFERRED, not verified in play)

- **Passage reach in the graph.** `Dome:GetClusterDomes` returns `connected_domes`, which is the dome plus its **direct** passage neighbours (`Buildings/Dome.lua:745-747`; built pairwise by `ConnectDomePair`, `Passage.lua:1573-1591 (1.1.1)`). `ExpandReachableNodesFrom` expands the cluster only from a node **not** reached by `walk` (`:3591-3596`). So the graph's explicit passage expansion is one hop from the start dome, or from a train, elevator or shuttle arrival. Deeper passage chains enter the graph only through `AddNodesInWalkDist`'s foot test (`CheckWalkableDistanceCached`, which is at most `ColonistMaxDomeWalkDist`).
  - I did not check whether `PathLenCached` counts passage PF tunnels.
  - 1.0.7 reached the whole passage network through `AreDomesConnectedWithPassage` (city-level network) inside `IsInWalkingDistDome`.
  - This narrowing dates from 1.1.0 and is unchanged in 1.1.1.
- **Reservation window.** `StartMigration` reserves at the final destination before the first leg (`:2099-2109`). A delivered shuttle leg keeps those holds (`WaitTransport :3948`, `elseif not leg_delivered`). The holds are released only by `AbortMigration` (5 failed steps), by task expiry through `ClearTransportRequest`, or on arrival. This lengthens the time a reservation is held (see F58).
- **Legacy residue.** `TryToEmigrateToDome`'s walk-branch condition still reads `self.emigration_elevator` (`:1906`, `:1923`). The graph path sets it to `nil` (`:2070`, `:2111`), so only the legacy fallback, `Abandoned` and `Stranded` can reach the elevator arm of `TransportByFoot` (§4).

## 4. Dead or rerouted in 1.1.1

Caller lists come from `grep -rnE "<name>\(" Src/Lua --include=*.lua` in the 1.1.1 tree, excluding definition lines. Each hit is attributed to its enclosing function with `within.py`.

### 4.1 `FindTransportationModeToCommunity` and `g_TransportationModeToCommunityCache`

**Not on the main migration path in 1.1.1.**

- In **1.1.0**, 4 callers: `Colonist:FindEmigrationDome` `Units/Colonist.lua:3525` (the migration path, every emigration); `SupplyRocketBase:GenerateDepartures` `Buildings/SupplyRocket.lua:68`; `FindStopoverDomeForRocket` `UniversalRocket.lua:2223`; `UniversalRocketBase:GenerateDepartures` `UniversalRocket.lua:2245`.
- In **1.1.1**, 4 callers. The `FindEmigrationDome` call is gone, replaced by one in the fallback:
  1. `Colonist:TryToEmigrate` `Units/Colonist.lua:2063 (1.1.1)`. Reached only when `FindEmigrationDome` returns a dome with `leg == false`. That happens for a forced dome the graph cannot reach (`:3803`), or when `GetNextLegToward` declines (see §3.2). Here `shuttles_available = not self:CheckForcedDome() and same city and IsLRTransportAvailable(city)`, which is `false` for every forced dome.
  2. `SupplyRocketBase:GenerateDepartures` `Buildings/SupplyRocket.lua:68 (1.1.1)`: `(self, colonist, false, colonist.city)`.
  3. `FindStopoverDomeForRocket` `UniversalRocket.lua:2229 (1.1.1)`: `(rocket, dome, false, city)`.
  4. `UniversalRocketBase:GenerateDepartures` `UniversalRocket.lua:2251 (1.1.1)`: `(self, colonist, false, colonist.city)`.
- **Cache keys by caller (INFERRED from `:3374-3408`).** The rocket callers write under `cache[rocket]` with `shuttles_available = false`, so their keys never collide with emigration keys (`cache[dest_dome]`). The only key that can be written with both flag values is `cache[dest_dome][start]` from caller 1: `false` from a forced-dome fallback, and `true` from a non-forced `leg == false` fallback while hubs are available.
- Even a stale mode there is mostly harmless. With mode `false` or `"shuttle"`, `TryToEmigrateToDome` goes on to `BookShuttleRide` (`:1972`). Only `"train"` (sent to `TryToEmigrateByTrain`, `:2065-2066`) and a `"walk"` that takes the walk branch (`:1922-1937`) skip the booking.
- **Cache writers and flushers in 1.1.1:** `OnMsg.TrainRoutesRebuilt` / `DomesConnected` / `DomesDisconnected` (`:3328-3336`); `InvalidateTransportCacheOnTrainLabel` (`:3338-3344`); `InvalidateTransportCacheForRocket` (`:3346-3353`); `SavegameFixups.InvalidateTransportModeToCommunityCache` (`:3356-3358`); `TryToEmigrateByTrain` on no route (`Units/ColonistTransport.lua:802`); `SavegameFixups.ZZZZ_FixRocketStationConnections` (`UniversalRocket.lua:4043`).
- **Helpers used only through this function:** `GetTransportationModeToCommunity` (callers: `FindTransportationModeToCommunity` `:3380`, `:3384`, `:3404` only), `FindTransportationModeToCommunity_BeforeTrains` (only `GetTransportationModeToCommunity :3411`) and `GetTransportThroughElevator` (only `GetTransportationModeToCommunity :3414`). They are live only through the four callers above.

### 4.2 Train emigration: `Colonist:TryToEmigrateByTrain` / `Colonist:MigrateByTrain`

Bypassed by the graph path. Train legs now use `StartTransport("MigrateStep", ...)` (`:2113`, `:2187`) and the `ExitVehicle` re-issue.

- `TryToEmigrateByTrain` callers in 1.1.1: `Colonist:Abandoned` `:1475`, `Colonist:TryToEmigrate` `:2066` (legacy fallback only) and `Colonist:TransportByFoot` `:3873` (after an elevator, only when `emigration_elevator` is set).
- `"MigrateByTrain"` still appears in `DisembarkOnArrival` `ColonistTransport.lua:351`, `StartTransport` `:360` (arrivals: `reason = self.arriving and "MigrateByTrain"`), `SetCommand` `:437` and `TryToEmigrateByTrain` `:799`, `:814`. **Rocket arrivals still use the old single-hop train path.**

### 4.3 `emigration_elevator` and the elevator arm of `TransportByFoot`

The graph path clears the field (`TryToEmigrate :2070`, `StartMigration :2111`). Writers that set a value in 1.1.1:

- `TryToEmigrate :2064` (legacy fallback);
- `Abandoned :1474`;
- `Stranded` `ColonistTransport.lua:938`;
- the arrival and return code: `RocketBase:Disembark :1980`, `RocketBase:GenerateArrivals :2066`, `RocketBase:EjectColonists :2105`, `CargoTransporterNew:GenerateArrivals :1002`, `EjectColonists :1050`, `UnloadPassengers :1093`.

So `TransportByFoot`'s `UseElevator` branch (`:3856-3874`) now serves only arrivals, returns, rescue and the legacy fallback. Graph elevator legs run in `MigrateStep :2188-2194`.

### 4.4 Declarations with no caller at all in 1.1.1

- **`Colonist:PickEmigrationCommunity`** (`:3439-3448 (1.1.1)`): the only match for its name in both 1.1.0 and 1.1.1 is its definition. Dead since 1.1.0; its sole caller was 1.0.7 `FindEmigrationDome :2698`.

### 4.5 Rerouted, still live with a narrower role

- **`TryToEmigrateToDome`**: now the final step only. Callers: `TryToEmigrate :2068` (legacy) and `:2074` (direct shuttle or final walk), `MigrateStep :2181`, `TryToMigrateHome` `ColonistTransport.lua:864`. Its inline shuttle booking moved to `BookShuttleRide`.
- **`CreateColonistTransportTask`**, callers in 1.1.1: `BookShuttleRide :2007` (replaces `TryToEmigrateToDome :1970 (1.1.0)`), `Colonist:SetCommand` `ColonistTransport.lua:464` (rescue home), `Stranded :900`, `UniversalRocketBase:GenerateDepartures` `UniversalRocket.lua:2260` (stopover) and `Dome:TestColonistLRTransport` `Buildings/Dome.lua:2587` (debug).
- **`IsTransportAvailableBetween`**, callers: `BookShuttleRide :2007`, `CanReachDomeForBuilding :4350` and `UniversalRocketBase:GenerateDepartures` `UniversalRocket.lua:2260`.
- **`GetDomesPassagePath`**, callers: `TryToEmigrateToDome :1918` and **new** `MigrateStep :2201`. In 1.1.0 the only caller was `TryToEmigrateToDome :1910`.
- **`CanReachByTrain`**, callers: `GetTransportThroughElevator` `Buildings/Dome.lua:346`, `LeavingMars :1156`, `Abandoned :1473`, `GetTransportationModeToCommunity :3419`, `TransportByFoot :3870`, `CanReachByTrainOrOnFoot :4323` and `GetDomesReachableByColonists` `_GameUtils.lua:418`. None is on the graph migration path; the graph uses `GetTrainsOnRoute` / `ForEachStationAlongTrack` / `CanBoardTrainLeg` instead.
- **`TransportByFoot`** (`"TransportByFoot"` issuers): `Arrive :1631`, `TryToEmigrateToDome :1935`, `MigrateByTrain :2033`, **`MigrateStep :2218`** (settling in after the last leg), `ReturnFromExpedition :5463` and `Stranded` `ColonistTransport.lua:939`. `Getui_command :4676` compares against the command name.

## 5. Walk and transport constants

Command: `grep -rnE "ColonistMaxDomeWalkDist|ColonistMinDistToIgnorePassage|ColonistMaxPassagePassthroughDomes|ForcedByUserLockTimeout|OxygenMaxOutsideTime" --include=*.lua .` from `Src/` of each build. Readers are attributed to their enclosing function with `within.py`.

Storage mechanics:

- `DefineConstInt(group, id, value, scale)` registers the value in `const.<group>.<id>` (`CommonLua/Core/ConstDef.lua:349-378, 504-510 (1.1.1)`; `DefineConst` writes `const_group[id]`).
- `DefineConst{group=..., id=...}` in `__const.lua` does the same.
- `g_Consts` is the modifiable `Consts` instance (`Lua/Modifiers.lua:463-471 (1.1.1)`). Game code reads it, and game rules modify it through `Effect_ModifyLabel` with `Label = "Consts"`.

| Constant | 1.0.7.396349 | 1.1.0.403908 | 1.1.1.405907 | Default |
|---|---|---|---|---|
| `ColonistMaxDomeWalkDist` | `const.ColonistMaxDomeWalkDist` (`_GameConst.lua:133`), a plain global field | `DefineConstInt("Colonist", ...)` (`_GameConst.lua:149`) -> `const.Colonist.ColonistMaxDomeWalkDist`; read as `g_Consts.ColonistMaxDomeWalkDist` | same as 1.1.0 (`_GameConst.lua:149`) | 400 m (`400 * guim` / `400, "m"`) |
| `ColonistMinDistToIgnorePassage` | `const.ColonistMinDistToIgnorePassage` (`_GameConst.lua:134`) | `DefineConstInt("Colonist", ...)` (`:150`); read as `g_Consts.` | same (`:150`) | 1200 m |
| `ColonistMaxPassagePassthroughDomes` | `const.ColonistMaxPassagePassthroughDomes = 8` (`_GameConst.lua:135`) | same plain `const.` (`:151`) | same (`:151`) | 8 |
| `ForcedByUserLockTimeout` | ConstDef group Colonist (`__const.lua:152-158`), `g_Consts.` | same (`__const.lua:171-177`) | same (`__const.lua:171-177`) | `value = 3600000`, `scale = "sols"` |
| `OxygenMaxOutsideTime` | ConstDef group Stat (`__const.lua:1604-1610`), `g_Consts.` | same (`__const.lua:1753-1759`) | same (`__const.lua:1753-1759`) | `value = 120000`, `scale = "h"` (`const.HourDuration = const.Scale.h`, `_GameConst.lua:5`) |

The Restricted Foot Walk game rule differs by build.

- **1.0.7:** an `Effect_Code` overwrites `const.ColonistMaxDomeWalkDist = 240 * guim` and `const.ColonistMinDistToIgnorePassage = 720 * guim` (`Data/GameRuleDef.lua:201-202 (1.0.7)`), and again on `OnMsg.LoadGame` (`Lua/Buildings/Station.lua:1311-1312 (1.0.7)`). It applies `-40 %` to `OxygenMaxOutsideTime` through `Effect_ModifyLabel` (`Data/GameRuleDef.lua:192`).
- **1.1.0 / 1.1.1:** all four props (`OxygenMaxOutsideTime`, `WaterMaxOutsideTime`, `ColonistMaxDomeWalkDist`, `ColonistMinDistToIgnorePassage`) take `Effect_ModifyLabel` `Percent = -40` on `Consts` (`Data/GameRuleDef.lua:190-206 (1.1.1)`; the Prop lines are 191/196/201/206). `SavegameFixups.RestrictedFootWalkWalkDistModifiers` (`Lua/_fixup.lua:2695` in both 1.1.0 and 1.1.1) applies the modifiers to old saves. The `Station.lua` `LoadGame` write is gone (0 hits in either tree).

Readers in scope. The 1.1.1 count per constant is reconciled against its reader list.

- **`ColonistMaxDomeWalkDist`**:
  - 1.0.7, 3 readers: `CheckWalkableDistance` `Buildings/Dome.lua:188`; `GetTransportThroughElevator` `Buildings/Dome.lua:282`; `TryToEmigrateToDome` `Units/Colonist.lua:1558`. The other 2 grep hits are the RestrictedFootWalk writes at `Station.lua:1311` and `Data/GameRuleDef.lua:201`.
  - 1.1.0, 5 readers: `Dome.lua:220` (CheckWalkableDistance), `Dome.lua:339` (GetTransportThroughElevator), `Colonist.lua:1901` (TryToEmigrateToDome), `Colonist.lua:3269` (AddNodesInWalkDist), `ColonistTransport.lua:875` (Stranded foot fallback, times 150 %).
  - **1.1.1, 6 readers:** `Dome.lua:220`, `Dome.lua:339`, `Colonist.lua:1909` (TryToEmigrateToDome), **`Colonist.lua:2199` (MigrateStep, new)**, `Colonist.lua:3496` (AddNodesInWalkDist), `ColonistTransport.lua:930` (Stranded).
- **`ColonistMinDistToIgnorePassage`**:
  - 1.0.7, 2 readers: `IsInWalkingDistDome` `Dome.lua:256`; `TryToEmigrateToDome` `Colonist.lua:1559`.
  - 1.1.0, 2 readers: `Dome.lua:311`, `Colonist.lua:1902`.
  - **1.1.1, 3 readers:** `Dome.lua:311`, `Colonist.lua:1910`, **`Colonist.lua:2199` (MigrateStep, new)**.
- **`ColonistMaxPassagePassthroughDomes`**: 1 reader in every build, `TryToEmigrateToDome` (`Colonist.lua:1567 (1.0.7)`, `:1914 (1.1.0)`, `:1922 (1.1.1)`). **The new `MigrateStep` passage walk does not read it.**
- **`ForcedByUserLockTimeout`**: 3 readers in every build: `CheckForcedDome`, `CheckForcedResidence` and `CheckForcedWorkplace` (`Colonist.lua:2323/2332/2347 (1.0.7)`, `:2933/2942/2957 (1.1.0)`, `:3137/3146/3161 (1.1.1)`). No new reader in 1.1.1.
- **`OxygenMaxOutsideTime`**: 1 reader in `Units/Colonist.lua` in every build, `Colonist:HourlyUpdate` (`:3730 (1.0.7)`, `:4577 (1.1.0)`, `:4903 (1.1.1)`). No migration function reads it; no walk is budgeted against it in any build.
- Related, new in 1.1.0: `StrandedMaxWalkDistIncreasePercent`, `DefineConstInt("Gameplay", ..., 50, "%")`, defined **inside** `Units/ColonistTransport.lua:820 (1.1.0)` / `:833 (1.1.1)`. It is read as `const.Gameplay.` (not `g_Consts.`) at `ColonistTransport.lua:930 (1.1.1)`.
- Related, new in 1.1.0: `const.ColonistTransportTaskExpirationTime = const.DayDuration` and `const.ColonistTransportTaskExpirationCheck = const.HourDuration` (`_GameConst.lua:144-145`), both plain `const.`.

## 6. Relevance to the tracked library entries

I read each entry at `B:\Dev\SMR\SMR-BugFixPack\docs\agent\bugs\<ID>.md` only for what it claims; none was edited. "Site unchanged" means byte-identical from 1.1.0 to 1.1.1, confirmed by the extractor, with `sed`-range controls where §1 names them.

| ID | Claim, short | Did 1.1.1 change the site? | 1.1.1 location and consequence |
|---|---|---|---|
| **F51** | The `FindTransportationModeToCommunity` cache key omits `shuttles_available` | **Function unchanged; its callers changed.** Cache and key are byte-identical (`Units/Colonist.lua:3374-3408 (1.1.1)`; control diff vs 1.1.0 `:3170-3204` IDENTICAL). No flush on shuttle-hub events was added. | **Off the main migration path:** `FindEmigrationDome` no longer calls it (§4.1). The only migration caller is the `leg == false` fallback in `TryToEmigrate :2060-2069`, mostly forced domes with `shuttles_available = false`. The 3 rocket callers always pass `false` under `cache[rocket]` keys. INFERRED: a stale entry can still flip a legacy-fallback result between `"shuttle"` and elevator or `false`, but `TryToEmigrateToDome` books a ride for a `false` mode anyway (`:1972`). The 1.0.7 "domes skipped forever" mechanism (per-candidate filter at `FindEmigrationDome :2662-2663 (1.0.7)`) has had no counterpart since 1.1.0. |
| **F52** | The vacuum walk threshold uses `ColonistMaxDomeWalkDist` where it should use `ColonistMinDistToIgnorePassage` | **The TryToEmigrateToDome site is unchanged; a second copy was added.** `TryToEmigrateToDome :1911 (1.1.1)`: `local min_dist = GetAtmosphereBreathable(self:GetMap()) and dome_passage_dist or dome_walk_dist`. **New:** `MigrateStep :2199 (1.1.1)`, same expression with `g_Consts.` operands. | The new copy guards intermediate-dome walks. It has no `ColonistMaxPassagePassthroughDomes` cap and no shuttle alternative (`:2195-2212`). Walk selection in the graph (`AddNodesInWalkDist`, `:3496`) is capped by the same 400 m `ColonistMaxDomeWalkDist`. The final-walk input to `TryToEmigrateToDome` now comes from `IsInWalkingDistDome` (`:2072`, `:2178`, and `ColonistTransport.lua:863` for `TryToMigrateHome`), with `-1` as the "passages only" value. |
| **F54** | `IsLRTransportAvailable` counts switched-off hubs | **Unchanged** (`Buildings/ShuttleHub.lua:410-419 (1.1.1)`; the clause `hub.working or hub:GetWorkNotPermittedReason() and not hub:GetWorkNotPossibleReason()` is at `:413`; control vs 1.0.7 IDENTICAL). | **More consumers depend on it:** 10 call sites in 1.1.1, against 6 in 1.0.7 and 10 in 1.1.0 (list: §7, command C11). New in 1.1.1: `BookShuttleRide :1991`, the `TryToEmigrate` legacy fallback `:2062`, and the **per-city** shuttle fill in `BuildReachableGraph :3639`. That fill marks every pad in the city as shuttle-reachable. INFERRED: with all hubs switched off, the graph can plan journeys whose shuttle legs no ship serves. The 1.1.0 task expiry (1 sol) and the 1.1.1 5-failure `AbortMigration` bound the wait. |
| **F58** | Residence reservations never expire | **Residence functions unchanged** (`Buildings/Residence.lua` `ReserveResidence :291-308`, `CanReserveResidence :284-289`, `CancelResidenceReservation :386-400`, `Dome:ReserveResidence` `Buildings/Dome.lua:3482-3493`, all identical 1.1.0 -> 1.1.1). Still no timestamp or expiry on `Residence.reserved`. | **Colonist-side release paths grew:** `AbortMigration :2140-2151` after 5 failed steps, and task expiry via `LRManager:ExpireColonistTransportTasks` (1.1.0, unchanged). **Holds also lengthen** (INFERRED): `StartMigration :2099-2101` reserves at the final destination before the first leg, and a delivered shuttle leg keeps it (`WaitTransport :3948`). A multi-leg journey therefore holds a slot for its whole duration. |
| **F59** | `Residence:RemoveResident` does not call `CheckHomeForHomeless` | **Unchanged** (`Buildings/Residence.lua:120-127 (1.1.1)`; control vs 1.0.7 `:83-90` IDENTICAL). | `CheckHomeForHomeless` callers are the same set in all three builds: `Residence.lua:65`, `:174`, `:215` and `Hotel.lua:23` (1.1.1 lines). There are 0 calls from `RemoveResident` or `CancelResidenceReservation`. |
| **F53 / C83 / C102** | Arrival and expedition-return dome choice (safety-dome fallback, switched-off dome) | **All unchanged 1.1.0 -> 1.1.1:** `GetDomesReachableByColonists` `_GameUtils.lua:390-483` and `ChooseDome` `:486-501` (control IDENTICAL); `Colonist:GetExpeditionReturnDome` `Units/Colonist.lua:5389-5401`; `CargoTransporterNew:UnloadPassengers` `:1076-1121`; `RocketBase:Disembark` `Buildings/RocketBase.lua:1969-1988`; `RocketBase:GenerateArrivals :2018-2092` / `EjectColonists :2094-2117`; `CargoTransporterNew:GenerateArrivals :953-1035` / `EjectColonists :1037-1062`; `Colonist:Arrive :1589-1635`. | These paths do not use the new graph. They still choose with `GetDomesReachableByColonists` + `ChooseDome` and walk through `TransportByFoot`, or through the old `MigrateByTrain` for arrivals (`StartTransport :360`). `Stranded`'s foot fallback (`ColonistTransport.lua:924-925 (1.1.1)`) also consumes `ChooseDome`'s safety pick, capped by `IsConnectedByFoot` at 150 % of the walk distance. It is unchanged from 1.1.0 apart from its position in the loop. |
| **C42** | Passage traversal clears `unit.holder` directly | **Unchanged** (`PassageBase:TraverseTunnel` `Passage.lua:1201-1248 (1.1.1)`; the raw `unit.holder = nil --last el would be holder, ...` is at `:1234 (1.1.1)`, `:1233 (1.1.0)`, `:1055 (1.0.7)`; control 1.1.0 vs 1.1.1 IDENTICAL). The PassageHub exit branch (1.1.0+) uses `SetHolder`; the dome exit branch does not. | INFERRED, more exposure: 1.1.1 adds a new passage-traversing caller, `MigrateStep :2204-2209` (`EnterBuilding` over `GetDomesPassagePath`). It runs in addition to `TransportByFoot :3842-3849`, so passage traversals on migration routes can only be more frequent. |

## 7. Commands run, and what was not done

All commands ran in Git Bash against the archived trees (`A=/b/Dev/SMR/SMR-Shared/SMR-SrcArchive`). The helper scripts are in `...\scratchpad\ab\`:

- `fx.py`: extracts top-level Lua declarations and reports per-step status;
- `dfn.py`: unified diff of one declaration between two builds;
- `within.py`: maps a `file:line` to its enclosing declaration;
- `s.sh`: numbered line range;
- `inv.py`: generates the table in §1.

| # | Command (abridged) | Result used |
|---|---|---|
| C1 | `find $A/<build>/Src/Lua -path "*<file>"` and `wc -l` for the 10 in-scope files in the 3 builds | File locations. `Passage.lua` is at the root of `Lua/`, as are `LRTransport.lua`, `UniversalRocket.lua` and `CargoTransporterNew.lua` |
| C2 | `python fx.py <file> '<regex>'` for Colonist, ColonistTransport, LRTransport, Dome, Residence, Passage, ShuttleHub, _GameUtils, RocketBase, CargoTransporterNew, UniversalRocket, Community, Workplace, MicroGHabitat, LRManager, Station, SupplyRocket | Per-declaration lines and status |
| C3 | `grep -rnE "^(local )?function <names>" --include=*.lua` in each build | Where the helpers are declared (Dome/Passage/Residence/ShuttleHub/_GameUtils/RocketBase) |
| C4 | `python dfn.py <file> <decl> 0 1` and `... 1 2` for each changed in-scope declaration | Excerpts in §2 and §3 |
| C5 | `sh s.sh <build> <file> a b` over `Units/Colonist.lua` 1546-1635 / 2440-2850 (1.0.7), 1886-2054 / 3246-3540 (1.1.0), 1894-2256 / 3310-3907 / 3928-4013 / 1445-1500 / 2446-2560 (1.1.1); `ColonistTransport.lua` 794-945 (1.1.1); `LRTransport.lua` (1.0.7, 1.1.1); `Passage.lua` 1085-1175 (1.0.7), 1260-1332 / 1514-1601 (1.1.1); `Dome.lua` 205-320 / 678-750 / 1900-1944 / 2575-2591 / 3482-3537 (1.1.1); `Residence.lua` 105-169 / 284-308 (1.1.1); `UniversalRocket.lua` 2213-2316 (1.1.1) | Full bodies read |
| C6 | `grep -rnE "ColonistMaxDomeWalkDist\|ColonistMinDistToIgnorePassage\|ColonistMaxPassagePassthroughDomes\|ForcedByUserLockTimeout\|OxygenMaxOutsideTime" --include=*.lua .` from `Src/` of each build | §5 readers and writers. Hit counts from `... \| wc -l`: 1.0.7 **22**, 1.1.0 **23**, 1.1.1 **24**. Reconciliation for 1.1.1: GameRuleDef 3 + Dome 3 + Colonist 9 + ColonistTransport 1 + _fixup 1 + _GameConst 3 + `__const` 4 (`help` + `id` lines) = 24. For 1.1.0: 3+3+8+1+1+3+4 = 23. For 1.0.7: GameRuleDef 3 + Dome 3 + Station 2 + Colonist 7 + _GameConst 3 + `__const` 4 = 22 |
| C7 | `grep -n -B6 -A4 'id = "<const>"' __const.lua`; `sed -n 185,215p Data/GameRuleDef.lua`; `ConstDef.lua:349-385, 500-510`; `Modifiers.lua:440-500` | §5 defaults and storage |
| C8 | `grep -rnE "FindTransportationModeToCommunity\|GetTransportationModeToCommunity\|g_TransportationModeToCommunityCache\|CanReachByTrain\(\|TryToEmigrateByTrain\(\|..."` in each build | §4 caller lists |
| C9 | A loop over 16 patterns (`PickEmigrationCommunity`, `"TransportByFoot"`, `CreateColonistTransportTask\(`, ...) in 1.1.1, `grep -vE ":(local )?function "`, each hit through `within.py`; the same for 4 patterns in 1.1.0 | §4 attribution. `PickEmigrationCommunity`: definition only in 1.1.0 and 1.1.1 |
| C10 | `grep -rnE "emigration_elevator\s*=[^=]"` in 1.1.1 plus `within.py` | §4.3, 17 hits (1 class default, 16 assignments) |
| C11 | `grep -rn "IsLRTransportAvailable(" ... \| grep -v "function IsLRTransportAvailable"` in each build, plus `within.py` | 1.0.7: 6; 1.1.0: 10; 1.1.1: 10. Members listed in the transcript: 1.1.1 = `Dome.lua:316`, `Colonist.lua:1924`, `:1991`, `:2062`, `:3639`, `:3891`, `:3920`, `:3992`, `ColonistTransport.lua:463`, `:897` |
| C12 | `grep -rn "CheckHomeForHomeless\|:RemoveResident("` in each build | F59 (§6) |
| C13 | `grep -n "unit.holder = nil" Passage.lua` in each build | C42 lines: 1055 / 1233 / 1234 |
| C14 | Controls: `diff <(sed -n a,bp old) <(sed -n c,dp new)` for FTMTC, `IsLRTransportAvailable`, `TraverseTunnel`, `RemoveResident` and `_GameUtils.lua:390-501` | All 5 printed IDENTICAL |
| C15 | Absence control: `grep -rhoE 'MigrateStep\|GetNextMigrationLeg\|migration_dest' $A/<b>/Src/Lua --include=*.lua \| wc -l` | 0 / 0 / 22 |
| C16 | Present-side scale: `diff 1.1.0/Colonist.lua 1.1.1/Colonist.lua \| grep -c '^[<>]'` | 636 changed lines |
| C17 | Override check: `grep -rlE "function (Colonist[:.](TryToEmigrate\|FindEmigrationDome\|TransportByFoot\|MigrateStep\|Stranded)\|FindTransportationModeToCommunity\|IsLRTransportAvailable\|CreateColonistTransportTask)\b" $A/<b>/Src` for 1.0.7 and 1.1.1 | Hits only under `Lua/`; no DLC or Data override |
| C18 | `python inv.py > inv_rows.md`; `awk -F'\|' '{print $7"->"$8}' inv_rows.md \| sort \| uniq -c`; `grep -c "n/a" inv_rows.md` | §1 totals: 194 rows; 20 `n/a` cells |
| C19 | Read the fix-pack entries F51, F52, F53, F54, F58, F59, C83, C102, C42 (first ~3.5 KB each; F52's section list and its 1.1.0/1.1.1 sections) | Claims only |

**Not done:**

- No game run and no in-game observation. Every behavioural statement labelled INFERRED is a reading of the source, not a run.
- `PathLenCached` was not checked for whether it counts passage PF tunnels, which bears on the §3.4 passage-reach observation.
- The shuttle-side executor `CargoShuttle:TransportColonist` was not read line by line. Its 1.0.7 -> 1.1.0 diff is 227 changed lines; I read it only for how it ends the task (`state = "done"` at `Buildings/ShuttleHub.lua:935 (1.1.1)`, identical in 1.1.1).
- The four 1.1.1 `Dome.lua` additions were not traced into `KickAllWorkers` / `InterruptUnitsInHolder`.
- `Colonist:Arrive`, `ReturnFromExpedition` and `LeavingMars` were not audited beyond their status rows.
- `DbgShowDomeNetworks` and the passage PF-tunnel functions are outside the SEL list, so they have no rows.
- No file under `B:\Dev\SMR\SMR-BugFixPack` was edited. No git command, doccheck or hook was run.
