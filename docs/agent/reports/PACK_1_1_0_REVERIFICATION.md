# PACK-WIDE 1.1.0 RE-VERIFICATION — what to FIX, REMOVE, or AUGMENT

Audit run 2026-09-08 against the shipped 1.1.0 tree
(`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, build
1.1.0.403908) by a fresh session (`smr-bugfixpack-1e`). Brief:
`prompts/PACK_1_1_0_REVERIFICATION.md`. Tree at `cc6f740`, clean. **No code
was written.** Every line number below is the 1.1.0 tree unless it names a
`Code/` file; `Code/` line numbers are the tree at `cc6f740`.

> ⚖️ **THE HEADLINE.** All 80 modules were opened against the shipped 1.1.0
> body they wrap, replace or patch. **10 need a FIX, 35 should be REMOVED on
> 1.1.0, 35 KEEP.** Of the 35 removals, 32 are modules whose defect the
> developers fixed themselves and whose self-check passed anyway; **no
> instrument the project owns can see "vanilla fixed it"**, which is why the
> REMOVE bucket had never been used. Of the 10 fixes, **five are modules that
> APPLY today and do something wrong** — four of them are the F112 shape (a
> correct 1.0.7 transform applied on top of a vanilla redesign), one is a
> throw.

> ⚖️ **Method.** Every verdict rests on a body read of the shipped 1.1.0
> function beside our module, not on a name or a count. Where a verdict rests
> on something else (a recorded clearance, a C-side function nobody can read),
> the row says so. Pass 3's 37 wrapper/data modules were read by four parallel
> sub-readers under a written brief (`scratchpad/AGENT_BRIEF.md`, the same
> eight questions per module); I re-opened the shipped lines behind every
> action verdict they returned and behind the two claims that touched my own
> pass-1 rows. Their KEEP/REMOVE rows stand on their quoted evidence, which I
> did not re-open line by line — §3 says so. ⛔ **A source read is never
> `tested`.** Nothing here moves a status; the in-play controls are named where
> they matter.

## 0 · Status of this document

| pass | scope | state |
|---|---|---|
| 1 | the full-body replacements (22 grep hits; 17 real replacements + 5 that are wrappers today) | ✅ DONE — every one opened |
| 2 | the 17 modules that self-disable on 1.1.0 | ✅ DONE — every one opened |
| 3 | wrappers, `SetGlobal`, `DataPatch`, `F111` second look — the remaining 47 modules | ✅ DONE — 10 read by me, 37 by sub-readers, action rows re-verified |
| 4 | the self-check design | ✅ DONE — §4 |

## 1 · The four buckets

Every module lands in exactly one row (`DroneTransportMinors` is split by
half, and named in both). **Bold** = the verdict is player-visible today. The
`evidence` column is what was read; the `Code/` column is where our side lives.

### 1a · FIX — broken or wrong on 1.1.0, ranked

| # | module (defect) | what is wrong on 1.1.0 | evidence (1.1.0 tree) | ours (`Code/`) | shape |
|---|---|---|---|---|---|
| F-1 | **`SaintBlessing` (F92)** | **1.1.0 FIXED the defect and our data patch now BREAKS the blessing.** `TraitPreset:AddDomeColonistsModifier` applies `GetTraitLabel(trait)` itself now; our pass has already rewritten `Saint.modify_trait` from `Religious` to `TraitReligious`, so vanilla computes `GetTraitLabel("TraitReligious")`, which returns `false` (no such preset) and the function returns without registering anything. With the pack on, **no Saint blesses anyone**; with it off, 1.1.0 works. The module ends the boot ACTIVE (`gated110_*.log:186` `corrected 1 … of 2`) — the 17-inactive count hides this. | `Lua/TraitPreset.lua:85-86` (`GetTraitLabel(trait)`; `if not label then return end`); `Lua/Traits.lua:1325-1328` (`if not TraitPresets[trait_id] then return false end`); `Data/TraitPreset.lua:404-405` (shipped value still `Religious`) | `Fix_SaintBlessing.lua:100-103` (the rewrite), `:151-181` (the LoadGame re-base does the same on saves) | gate on BEHAVIOUR, not on a name: after DataLoaded call the real `AddDomeColonistsModifier` on a stub unit/dome that captures the label, patch only if it captures `Religious` (1.0.7 shape), decline as "already handled" if it captures `TraitReligious`. Silent, wrong-number class ⇒ P2. |
| F-2 | **`StaleReservations` (F58)** | 1.1.0 added a LEGITIMATE long-lived reservation our sweep cannot tell from a stale one: a colonist boarding an expedition rocket reserves their home (`expedition_residence`) and the residence panel promises "will return to this residence". Our post-wrapper stamps that reservation at boarding and the `NewDay` sweep cancels it after the 5-sol lock — and 1.1.0's `CancelResidenceReservation` now also wipes `expedition_residence`, so `ReturnFromExpedition` finds nothing to keep. Expeditions routinely exceed the lock (flight 1.2–3 M ms one way, plus pad wait, plus return). The F58 defect itself (no timeout on ordinary reservations) is still shipped. | `Lua/Units/Colonist.lua:5003-5008` (the hold), `:5076-5081` (the return); `Lua/Buildings/Residence.lua:392-394` (cancel wipes the hold); `Data/POI.lua:139, :438, :480, :521` (`expedition_time`); `sectionResidenceList.generated.lua:66-73` (the promise) | `Fix_StaleReservations.lua:49-54`, `:69-71` and the age branch of the sweep | exempt `colonist.expedition_residence` (truthy) / disappeared-on-expedition colonists from the sweep. One clause. P2, silent: crew back from a long expedition are re-homed at random or homeless. |
| F-3 | **`ShelterReflex` (F73), half (a)** | `Community:GetScoreFor` now takes the COLONIST, not its traits; our replacement `IsSuitable` still passes `colonist.traits`. Inside, `TraitFilterColonist(self.traits_filter, traits.traits)` indexes `nil` for every habitat with a trait filter, and `residence:IsSuitable(traits)` / `GetResidenceComfort(residence, traits)` index `nil` for any filtered residence — a throw on every residence evaluation for that habitat. Where neither filter is set it does not throw but no longer does what it claims: 1.1.0 made "no life support" a deliberate −400 TIER (`CommunityEvalNoLifeSupport`, help text: "so the player can still force colonists into an unpowered dome"), and our `+100` cannot lift it. Half (b) (the Idle pre-wrapper) reads only fields that still exist. | `Lua/Buildings/Community.lua:442-460` (`:445`, `:451-453`), `:436-437`; `Lua/Filter.lua:113-121` (`obj_attributes[attrib]`); `Lua/Traits.lua:1122-1124`; `Lua/Buildings/MicroGHabitat.lua:173-174` (vanilla passes `colonist`) | `Fix_ShelterReflex.lua:43-46` | drop half (a) — the tier is vanilla's stated design; keep (b). P2 (a throw, but only on an asteroid habitat with a trait filter or a filtered residence; the sub-reader rated it P1). |
| F-4 | **`FirstAsteroidPrefabs` (F83)** | The defect is gone AND the grant with it: `OnMsg.SpawnedAsteroid` now waits on a GAME-TIME thread (persisted, so an unanswered popup survives a load), and no `ColonyAddPrefabs` of the three Micro-G prefabs exists anywhere in the tree — the popup now says they "can be ordered from Earth". Our LoadGame sweep still matches the minimized notification, REMOVES it (orphaning the live waiter blocked on `WaitMsg` forever), GRANTS three prefabs vanilla no longer gives, and re-shows the popup. | `Lua/Asteroids.lua:418-423`; `Lua/UI/PopupNotification.lua:342`; tree-wide grep `ColonyAddPrefabs` (no Micro-G grant); `Data/PopupNotifications/PopupNotificationPreset-Asteroid.lua:36` | `Fix_FirstAsteroidPrefabs.lua:155-168`, `:173-210`, `:256-258` | REMOVE = the fix. Reachable by anyone who saves with the first-asteroid popup unanswered. P2 silent (free content + a leaked thread). |
| F-5 | **`AstrogeologistExtractors` (F95)** | 1.1.0 REWROTE the profile: the ten-entry enumeration is gone, replaced by two label-wide effects (`Extractors` `performance +20`, `Extractors` `water_production +20%`; text "Extractor performance increased by 20"). Our pass finds two `Effect_ModifyLabel`s (so its shape check passes), finds neither of its two target labels, and APPENDS `production_per_day1 +10%` for `AutomaticMetalsExtractor` and `water_production +10%` for `MicroGAutoWaterExtractor` — the boot log confirms it (`gated110_*.log:181` `added 2 missing … (2 already present)`). `MicroGAutoWaterExtractor` carries the `Extractors` label, so with the pack it gets +30% water where 1.1.0 gives +20%. The LoadGame heal applies the same to existing saves. F112 shape. | `Data/CommanderProfilePreset.lua:335-352`; `Data/BuildingTemplate/MicroGAutoWaterExtractor.lua:34` (`label3 = "Extractors"`) | `Fix_AstrogeologistExtractors.lua:103-114`, `:117-142`, `:174-218` | REMOVE = the fix; if kept for a 1.0.7 line, gate on the enumeration's shape (`existing >= 10`). P3 (favourable wrong number). |
| F-6 | **`PayloadTemplateRefill` (F70)** | Our 1.0.7 copy of `RetrieveRequests` reverts three 1.1.0 changes: (a) the **new tutorial's** rocket 2 is meant to be pre-filled from `AsteroidTutorialExpectedCargo` — ours has no tutorial branch; (b) a dialog opened from a **destination pick** (`prev_flight_data`) is meant to ignore stored cargo and re-apply the template even in `CmdLoad` — ours reads stored cargo and, once `SMRFixPack_payload_set` is set, suppresses the template; (c) the automode branch gained a nil guard on `cargo_items[id]` that ours lacks. The F70 defect itself persists (`:216-234`). | `Lua/CargoRequestNew.lua:169-192` (`:174`, `:183-189`), `:199-213`, `:215-217`; `Lua/TutorialsNew.lua:1019-1025` | `Fix_PayloadTemplateRefill.lua:57-68`, `:85-93`, `:97-99` | re-copy on the 1.1.0 body with the F70 gate on the non-destination-pick path; or gate the module off on 1.1.0 (`AsteroidTutorialExpectedCargo ~= nil` is the branch we lack, not a proxy). P3. |
| F-7 | **`RocketDroneChurn` (F50)** | 1.1.0 added a player toggle "stop drones refuelling this rocket" and honours it in the request loop with `not self.refuel_disabled`; our copy of the same loop does not, so a switched-off rocket **still requests fuel** hourly. The F50 defect persists (`:1431-1433` / `:1460-1462` still disconnect unconditionally). | `Lua/CargoTransporterNew.lua:1442`; `Lua/UniversalRocket.lua:70`, `:3320` | `Fix_RocketDroneChurn.lua:63` | one clause, as a re-copy of the 1.1.0 body (otherwise identical). P3. |
| F-8 | `LandscapeUnitFilter` (F34d) | Gated and correctly inactive (F115). The defect is still shipped: the body builds `filter_embark` and then passes `callback`. 1.1.0 players have F34(d) back. | `Lua/Landscape/Landscaping.lua:509-522` (`:522`) | body untouched, gate in `Require` | repair the body on `(map, mark, callback, ...)` reading `map.Landscapes[mark]`; KEEP the gate. Route (b) of F115, owner-deferred (ck109). |
| F-9 | `VacuumWalks` (F52) | Correctly inactive — by ACCIDENT (the `const.ColonistMaxDomeWalkDist` path spec fails because both walk constants became `g_Consts` entries). The defect line is unchanged, but 1.1.0 REWROTE the rest of the function (work-slot reservation, `-1` = passage-only distance, shuttle-slot checks, `DiscardTransportTicket`), so re-arming our copy would revert all of it. | `Lua/Units/Colonist.lua:1903` (defect), `:1896`, `:1904-1907`, `:1918-1926`, `:1932-1957`, `:1959-1968`; `:1901-1902` + `Lua/_GameConst.lua:149-150` | `Fix_VacuumWalks.lua:41-44`, `:49-98` | re-derive on 1.1.0 (re-copy, or a pre-wrapper handing `orig` a modified distance — needs a control, the shuttle branch reacts to it); read `g_Consts` at call time; make the gate deliberate. |
| F-10 | `TrainCargoDumping` (F46) | Correctly inactive (F114). The F46 defect plausibly persists: `UnloadAll` still has no enabled-resource check and the new `SetAcceptResource` SUSPENDS the request (`rfSuspended`) rather than removing it. ⚠️ `GetTargetAmount` on a suspended request is C-side, unread. | `Lua/Units/Train.lua:792-804`; `Lua/Buildings/MultiResourceDepot.lua:242-246`, `:251-290` | gated | re-copy on the 1.1.0 body (`:779-805`) with `station:IsResourceEnabled(res)`; keep the gate for the NEXT change. Nuisance class. |

### 1b · REMOVE — the defect is gone, or the target is gone, and the module is now pure risk

⛔ Each row states WHY the defect is gone, with the shipped line. "It is
inactive" appears nowhere as a reason. Rows R-18 onward are pass 3; those
marked ◇ were read by a sub-reader and their evidence was not re-opened by me.

| # | module (defect) | why the defect is gone on 1.1.0 | evidence (1.1.0 tree) | today | what removal costs |
|---|---|---|---|---|---|
| R-1 | `LowStorageWarning` (F12) | 1.1.0 **deleted** the Food and maintenance branches; "Insufficient Resources" now covers Power/Water/Air only. Reinstating a warning the developers removed is a feature. The gate is load-bearing (`EF-081`). | `Lua/ResourceTracking.lua:222-310`; `Data/NotificationPreset.lua:1019-1028` | inactive | nothing on 1.1.0; keep only for a 1.0.7 line (decision 98). |
| R-2 | `LanderCargoRatchet` (F68 + F71) | The rewrite adds the loaded hold back (F68) and allocates the budget by fair share (F71, different shape). | `Lua/UniversalRocket.lua:2046`, `:2069-2086`, `:2537-2546` | inactive (F113 gate) | nothing. |
| R-3 | `TouristSatisfaction` (F09) | The Satisfaction stat is gone: `UpdateSatisfaction`, `ChangeSatisfaction`, `SatisfactionLowStatPenalty` have zero hits. | tree-wide grep; `sigcheck` ABSENT | inactive | nothing. |
| R-4 | `AutomationLawCompensation` (C39, F112) | Vanilla deleted the compensation entirely; paying the eight now manufactures the asymmetry. | `Lua/Buildings/Workplace.lua:269-294`; `law_scale` 0 hits | inactive (`test`) | nothing unless the owner wants a REBALANCE (§4a bars it). |
| R-5 | `UpgradeModifierLeak` (F03) | `StopUpgradeModifiers` now iterates with `pairs`; our second `TurnOff` is idempotent and useless. | `Lua/Buildings/Building.lua:1303-1311`; `CommonLua/Classes/Modifiers.lua:479-484`; `Lua/Modifiers.lua:277-280` | applied | nothing. |
| R-6 | `SmallLandscapeSites` (F33) | `GetClosestDests` delegates to `GetTopClosestDests`, which bounds-checks; our clamp passes `Min(top_count or 5, n)` where 1.1.0's default is **10** — we narrow drones to 5 destinations. | `Lua/Landscape/LandscapeConstructionSiteBase.lua:204-208`, `:171-177` | applied | removal RESTORES vanilla's 10. |
| R-7 | `DroneTransportMinors` **(b)** (F57b) | The passability handler only bumps a per-map version now; the table keeps its metatable; `unreachable_buildings_count` has zero readers. Our handler rewrites a dead field for every drone on every change. (a) stays — K-8. | `Lua/Units/Drone.lua:935-937`, `:73`, `:943-945` | applied | remove the handler + `repair_unreachables`. |
| R-8 | `DroneUnreachableForever` (F55) | `MarkUnreachable` stamps `GameTime()` (no `+ max_int`); the expiry mechanism and its const are gone; the table resets on every passability/building change. | `Lua/Units/Drone.lua:889-911`, `:971-976`; `Building.lua:546`; `Landscaping.lua:328` | inactive | nothing. |
| R-9 | `MeteorFrequency` (F02, F88) | The dead `if` went with the thread: a `MapGameTimeRepeat` stores `g_NextMeteorsTime = GameTime() + Random(spawntime, spawntime + spawntime_random)`. `_G.Meteors` is now `GameVar("Meteors", false) -- required only for the savegame fixup`; our thread-keyed wrapper could never match and the watchdog's `RestartGlobalGameTimeThread("Meteors")` would call `CreateGameTimeThread(nil)`. | `Lua/Meteors.lua:293-322`, `:388`, `:390-412` | inactive | `SMRFixPack_MeteorLatch` stays in saves as inert data. |
| R-10 | `MeteorStormWedge` (F78) | The drain loop validates on `IsValid(descr.meteor)` (the descriptors-never-invalid mechanism we measured); the scheduler is a `MapGameTimeRepeat`; the savegame fixup kills any thread inside `MeteorsDisaster` and ends a stuck storm. ⚠️ Residual: still unbounded if a meteor object stays valid without posting `MeteorDone`. | `Lua/Meteors.lua:267-270`, `:329-386`, `:390-412` | inactive | nothing measured; a residual module would be NEW code on the new mechanism. |
| R-11 | `AsteroidLanderAvailable` (F72 + F94) | Gate and list are both built on `IsRocketAvailableForFlight` + `GetAvailableFlightLocations()`; they cannot disagree. | `Lua/PlanetaryView.lua:245-252`, `:258-265`; `Lua/UI/PlanetUI.lua:1701-1710`; `PlanetaryViewAsteroidResources.generated.lua:41-45` | inactive | nothing. |
| R-12 | `GridGlobalStorage` (F22) | Replaced by per-dome `ScriptFunc_DomesGridStorage`; no sum of ratios, no sentinel. | `Lua/ScriptBlocks.lua:387-419` | inactive | nothing. |
| R-13 | `LastTransmissionStorage` (F75) | ⭐ The brief's seed, confirmed: every storage like sets `'Condition'` with a `ScriptCheckDomesGridStorage` whose `Resource` is right. The "already correct" latch IS the vanilla fix. | `Data/FactionDef/LastTransmission.lua:104-260` (`:245`) | inactive (benign) | nothing. |
| R-14 | `RainsDeadlock` (F81b + C34) | Rains run as a repeat cycle; no untimed `WaitMsg`. Re-arming would be HARMFUL: our wrapper's `Msg("RainDisasterEnd")` now drives a lightmodel handler, and the migration calls the absent `RainsDisasterLoop`. | `Lua/TerraformingDisasters.lua:363-395`, `:142`, `:191-194` | inactive | the C34 heal goes with it. |
| R-15 | `DustSicknessDamage` (F17) | `daily_update_func` has zero hits in Lua and Data — the function went with its defect. | tree-wide grep | inactive | nothing. |
| R-16 | `IndependenceTerraforming` (F18) | `param1 = -10` and `Amount` is BOUND to `param1`; self-consistent. | `Data/Tech.lua:3557-3562`, `:3571-3577` | inactive | nothing. |
| R-17 | `UniversityOvertraining` (F36) | Defect line unchanged, premise false: automation is a FLOOR now (`Max(workers, auto_performance)`; vanilla's comments say so), so specialists at an automated extractor DO raise output. Keeping F36 is a balance opinion; our copy also reverts a perf rewrite. ⚖️ A judgement, marked as one. | `Lua/Buildings/Workplace.lua:283-287`, `:249`, `:433-434`; `Lua/City.lua:636-661` | applied | owner call. |
| R-18 | `CaveInsNoDisasters` (F01) | The repeat's condition now ends `and not IsGameRuleActive("NoDisasters")`. Our slot-3 wrapper is redundant. | `Lua/Marsquake.lua` (`MapGameTimeRepeat("UndergroundMarsquake", …)` condition); `CommonLua/Core/lib.lua:1559-1575` | applied | nothing. |
| R-19 | `CommandCenterNumbers` (F13) | Rows render `<resource(GetAvailable('Metals'), 'Metals')>`; `AvailableMetals` and siblings have zero consumers. Our eleven shims are read by nothing. | `Data/XDef/CommandCenterCategories.lua:226-244` | applied | nothing. |
| R-20 | `DisasterPredictionLeak` (F81a) | `EndMeteorStorm` removes the notification first, and `OnMsg.RemoveNotification` clears the flag on EXPIRY — the exact stranded state the module existed for. | `Lua/Meteors.lua:1204-1212`; `Lua/MapSettings.lua:223-228` | applied | the load/NewDay sweep polices an invariant vanilla keeps. |
| R-21 ◇ | `DustDevilSpawnGate` | The scheduler gates then counts itself; our wrapper re-rolls the same gate and burns extra `SessionRandom` draws per tick. | `Lua/DustDevils.lua:256`, `:235-237` | applied | nothing. |
| R-22 ◇ | `DustDevilsDescrMap` | Vanilla `GetDustDevilsDescr` already reads `MainMap`; our copy is byte-identical. | `Lua/DustDevils.lua:59`, `:64` | applied | nothing. |
| R-23 ◇ | `DustStormUndergroundBreaks` | `RandomBreakConnection(map)` filters connectors AND elements by the city's map; our swap is redundant and makes `IsBreakable` stricter. | `Lua/SupplyGrid.lua:1097`, `:1108-1114`, `:1134-1138`, `:1520` | applied | removal restores vanilla's filter. |
| R-24 | `ExtractorStaffedPerformance` (F108, F111) | Vanilla now does `Max(workers, auto_performance)` — the floor ruling verbatim; our branch is provably dead except under the new rubble guard, where it returns a POSITIVE performance for a rubble-shrouded extractor vanilla intends to be 0. (F111's guard stays correct; the module is inert-plus-one-wrong-case.) | `Lua/Buildings/Workplace.lua:270-272`, `:279-287`; `Lua/Units/Colonist.lua:794-796` | applied | nothing. |
| R-25 ◇ | `LanderReturnFuel` | Upstream now requests one ration with no destination for player-controlled rockets; our first return is identical, our second unreachable. | `Lua/UniversalRocket.lua:1891-1895`, `:436`, `:441` | applied | nothing. |
| R-26 ◇ | `LandscapeCostRefresh` (F107) | Upstream added the identical `construction_costs_at_start` guard. | `Lua/Buildings/ConstructionSite.lua:721` | applied | nothing. |
| R-27 ◇ | `LocalizedUIText` (C51) | The heading ships with `T(914616772802, …)`; `idBackToEarth` and both unenrolled ids are gone from the XDef tree; the module installs, declines every call, logs two "nothing changed" lines. | `Lua/XDef/TerraformingOverall.generated.lua:56-57`; `customUniversalRocket.generated.lua:11-126`; `GameShortcuts.generated.lua:1429-1446` | applied | nothing. ⚠️ Sub-reader flags a possible NEW untranslated string (`T(192345398558, "Back to Earth")`) outside this module's claim. |
| R-28 ◇ | `MilestoneCrash` (F05) | Vanilla now has `(milestone:GetScore() or 0)`; our copy is identical. | `Lua/Milestones.lua:116`, `:125-159` | applied | nothing. |
| R-29 ◇ | `MoraleComfortTooltip` (F20) | Morale/tooltip rewritten to an Outlook breakdown; no threshold-bonus row exists to hide; the override never fires. | `Lua/Units/Colonist.lua:3851-3855`, `:4862-4884`; `Lua/Stats.lua:814-925` | applied | nothing. |
| R-30 ◇ | `SpaceYDroneCapBullet` (C50) | Vanilla reworded the id to say "can control up to 40 Drones"; every runtime gate passes so we print a DUPLICATE bullet. | `Data/MissionSponsorPreset.lua:631`, `:702-705`; `Lua/UI/PlanetUI.lua:365`; `Lua/PreGameMission.lua:261`, `:284` | applied | removal removes a duplicate bullet (P3 today). |
| R-31 ◇ | `StorageRateModifiers` (F27) | Electricity leg fixed upstream (+ a sync fixup); the water/air rate props are not `modifiable`, so those legs can never fire. | `Lua/ElectricityStorage.lua:55-56`, `:240-249`; `Lua/LifeSupportStorage.lua:9-10`, `:109-110`; `CommonLua/Classes/Modifiers.lua:106-109`, `:286` | applied | nothing. |
| R-32 ◇ | `TechDescriptionBuilding` (F25) | Description corrected upstream under the same T id; the `TechDef` entry is a stub with no `description`, so the patch declines every run. | `Data/Tech.lua:6737-6747`; `Data/TechPreset.lua:512-515` | applied (dead) | nothing. |
| R-33 ◇ | `TouristApplicants` (F08) | Roll fixed upstream as `Random(0,99) < chance`; our `Random(0,100)` copy is marginally WORSE. | `Lua/HolidayRating.lua:87-106` (`:92`) | applied | removal restores vanilla's roll. |
| R-34 ◇ | `TrainMinors` (F49d) | The train cap is now the route's station count (`GetTrainsOnRoute`); `max_vehicles` is display-only. I re-read `Track.lua:424` (`local trains, cap = GetTrainsOnRoute(self)`). | `Lua/Buildings/Track.lua:423-426`, `:62-67`, `:596`; `Lua/TrainTransport.lua:492-537` (`:519-521`) | applied | the x/max display number stops refreshing after salvage (cosmetic). |
| R-35 ◇ | `TrainPlatformWedge` (F11) | The `table.remove_entry` guard shipped upstream; our wrapper duplicates it. I re-read `ColonistTransport.lua:660-667`. | `Lua/Units/ColonistTransport.lua:660-667`; `Lua/Units/Train.lua:424-451` | applied | nothing. |
| R-36 ◇ | `90_SaveSanitizer` (F35, F03, F48) | Every pass repairs state a 1.0.7 defect left behind, and no 1.0.7 save can load on 1.1.0 (`EF-079`): F35 reads an empty `TechDef` stub; F03's source is fixed (R-5) and vanilla ships its own leak fixup; F48's paren is fixed and new games are pre-marked. | `Lua/Buildings/WindTurbine.lua:95-105`; `Building.lua:1303-1311`, `:1313-1345`; `Station.lua:1497-1513`; `CommonLua/SavegameFixup.lua:10-37`; `Tracks.lua:520`, `:615-622` | applied | nothing on 1.1.0. |

### 1c · AUGMENT — the fix works, but its self-check cannot see the failure that bites

| # | module / tool | what the check misses | what it should test instead |
|---|---|---|---|
| A-1 | `GeneForging` (F41) | Works (K-4), but reads `TechDef.GeneForging.param1` — the LEGACY stub map (still populated: 274 `TechPreset` placements, `GeneForging` carries `param1 = 50`). 1.1.0 computes tech values from `Techs.<id>:ResolveValue("param1")`. A patch that empties the stubs (R-32 shows one already is) silently zeroes our bonus. | read `Techs.GeneForging:ResolveValue("param1")` when `Techs` exists, fall back to `TechDef`. |
| A-2 | every `DataPatch` benign latch | "already correct" is filed as HEALTHY. R-13 shows it is the REMOVE signal. | log it as `inactive (already correct — RETIRE candidate)`; `logscan.py` lists benign latches under their own heading. |
| A-3 | `logscan.py` | "last verdict wins" misses a `DataPatch` heal: `SaintBlessing` logs `inactive` at `:166`, `corrected …` at `:186`, and ENDS ACTIVE — the "17 inactive" headline is really **16**, and F-1 hid behind it. | treat `corrected` / `made effective` / `re-based` / `added … missing` lines as heals; print first-pass AND final counts. |
| A-4 | `sigcheck.py` | Reads `function Name(...)` definitions only; the 15 `SetGlobal` sites and anonymous literals are outside it. | resolve the local named in `SetGlobal("Name", <expr>)`. |
| A-5 | `LayoutTechLock` (F19) ◇ | Still correct, but 1.1.0 locks the layout at the build menu whenever any entry is tech-locked and un-prefabbed, so the wrapper agrees with the gate in every case; the header is stale. | retitle or retire at the owner's pleasure — equally safe either way. |

### 1d · KEEP — verified fine, with the reason

| # | module (defect) | why it is fine on 1.1.0 | evidence (1.1.0 tree) |
|---|---|---|---|
| K-1 | `BombardmentSpread` (F26) | Body byte-identical; `spawn_dir` computed at `:82`, `dir` used at `:83`. `g_IncomingMissiles` became a `MapVar`, read as `map.g_IncomingMissiles` in both bodies. | `Lua/Bombardment.lua:38-50`, `:53`, `:55-154`, `:52` |
| K-2 | `DomeFreeSpaceMismatch` (F60) | Still no second argument; `GatherFreeLivingSpaces` still keys the member on it; the sibling contradiction stands. | `Lua/Buildings/Dome.lua:3353-3355`; `Lua/_GameUtils.lua:535-558`, `:526`; `Lua/ResourceOverview.lua:687`; `Residence.lua:452`; `Colonist.lua:2923` |
| K-3 | `DomeOverviewHighlight` (F14) | Byte-identical; `SetText(v)` still discards `tv`. | `Lua/X/ColonyControlCenter.lua:1290-1300` |
| K-4 | `GeneForging` (F41) | `GetRareTraitChance` still knows only `GeneSelection`; the parameter was dropped and both callers pass nothing — our nil `unit` takes the `MainCity` path it already had. See A-1. | `Lua/Units/Colonist.lua:4398-4402`, `:4419`; `Lua/Traits.lua:1049`; `Data/TechPreset.lua:1311-1314`; `Data/Tech.lua:8971-8976` |
| K-5 | `ShuttleHubOffAvailable` (F54) | `IsLRTransportAvailable` byte-identical; the lax clause stands. | `Lua/Buildings/ShuttleHub.lua:410-419` |
| K-6 | `ShuttleTransportCache` (F51) | Identical bar the fix; cache still keyed on `(community, pos)`; 1.1.0's new flush sites cover trains and rockets, not hubs. | `Lua/Units/Colonist.lua:3156-3204`, `:3122-3153` |
| K-7 | `TrainWaitTime` (F21) | The three `AddSpentTime` sites, the un-restamped `start_wait`, `waiting_for_train` and `command_thread` are all unchanged. The Comfort half of F21 is gone from vanilla — no effect on the wrapper. | `Lua/Units/ColonistTransport.lua:614-639`, `:660-699`; `Lua/TransportStatistics.lua:31-37`; `Station.lua:79`, `:123`; `CommandObject.lua:90` |
| K-8 | `DroneTransportMinors` **(a)** (F57a) | `UpdateRocketsInternal` still clears only `r_t.Fuel` and writes `r_t[r.FuelResource]`. | `Lua/Buildings/DroneControl.lua:672-698`, `:13`, `:196-200` |
| K-9 | `TrackSalvageRefund` (F47) | ⚠️ On record, not re-read: cleared line-for-line by the trains sitting (F114 entry). | `agent/bugs/F114.md` |
| K-10 | `TrackConnectorPingPong` (F66) | ⚠️ On record, not re-read: cleared by the same sitting. | `agent/bugs/F114.md` |
| K-11 | `TrackSalvageWipe` (F116) | Repaired in-body; two owner-facing divergences remain. Not reopened. | `agent/bugs/F116.md` |
| K-12 | `AnomalyCaveInMap` (F31) | `TriggerCaveIn` still guards `pos` only; `FindCaveInLocation` still indexes `map.buildable` unguarded; all eight scenario sites still pass the global. | `Lua/Buildings/CaveInRubble.lua:103-109`, `:21-24`; the eight `Lua/Scenario/*.generated.lua` sites |
| K-13 | `ArrivalDeaths` (F53) | `Arrive` same shape; `Idle` still the sole issuer; `OnArrival` synchronous; `safety_dome` still picked by distance before the `is_walking` test; return signature matches our unpack. | `Lua/Units/Colonist.lua:1586-1639`, `:2233-2234`; `Lua/_GameUtils.lua:398-412`, `:482`, `:486-501` |
| K-14 | `BrokenTrackSalvage` (F45) | `BreakTrackElement` still omits `node_idx`; default still `false`; 1.1.0's pre-sort revalidation bails without restamping on a disconnected track, so F45 stays the backstop (F116's reasoning). | `Lua/Buildings/Track.lua:631-640`; `TrackElement.lua:173`, `:474-476`, `:487` |
| K-15 | `CrystalMysteryHang` (F06) | The race is unchanged; `CrystalForceFlyAway` still has no emitter. | `Lua/Mysteries/Crystals.lua:28-31`; `Lua/Scenario/Mystery 10.generated.lua:271` |
| K-16 | `DestroyedTunnels` (F38) | `AddPFTunnel` still tests only `IsValid(linked_obj)`; the LoadGame sweep re-adds every tunnel. | `Lua/Buildings/Tunnel.lua:193-205`, `:260-262`, `:211-214` |
| K-17 | `DustSicknessBiorobots` (F40) | All three storybits still filter on `Child` only; `Android` exists. | `Data/StoryBit/DustSickness*.lua`; `Data/TraitPreset.lua:461` |
| K-18 ◇ | `ExoticDepositSign` | Class default still the wrong sign; replacement entity registered. | `Lua/Buildings/SubsurfaceDeposit.lua:517`, `:393-397`, `:473-479` |
| K-19 ◇ | `ExtenderFlapChurn` (F77) | `OnSetWorking` still runs the full teardown/rebuild; the new `are_requesters_connected` guard composes. | `Lua/Buildings/DroneHubExtender.lua:181-184`, `:109-112`; `DroneControl.lua:500-509`, `:784-793` |
| K-20 ◇ | `FounderTraitNotification` (F23) | Array-indexed-by-name defect shipped verbatim. | `Lua/ColonyViability.lua:300-309`; `Colonist.lua:527` |
| K-21 ◇ | `FreedHousingNotice` | `RemoveResident` still wakes nobody. | `Lua/Buildings/Residence.lua:119-126`, `:111`; `Colonist.lua:2898-2917` |
| K-22 ◇ | `GhostFarmOxygen` | Farm modifier still dome-keyed with no cleanup; our zeroing idempotent. | `Lua/Buildings/Farm.lua:639-641`; `Building.lua:696-729` |
| K-23 ◇ | `GraphConsumedCaption` | Caption still omits maintenance while the series adds it. | `Lua/X/ColonyControlCenter.lua:184`, `:188`, `:192`; `ResourceTracking.lua:162` |
| K-24 ◇ | `JumboCaveReinforcementWedge` (F110) | Spin loop, random approach and unreachable marking unchanged. | `BuriedWonder_Jumbo_Cave.generated.lua:103-105`; `WasteRock.lua:126-131`, `:328-342`; `Drone.lua:909`; `ConstructionSite.lua:533-541` |
| K-25 ◇ | `LakeEntombment` | RC exemption and scatter-before-dig ordering unchanged. | `ConstructionSite.lua:1918`, `:1766`; `LandscapeLake.lua:34`, `:343`; `Unit.lua:737-744` |
| K-26 ◇ | `LanderEmptyLaunch` (F67) | Tail still `return cargo_status == "ready"`; an empty request still "ready". | `Lua/UniversalRocket.lua:554-558`, `:2088-2093`, `:1006-1008` |
| K-27 ◇ | `MirrorSphereSite` (F16) | `progress == 100` on a 0..2^22 scale still shipped. | `Lua/Mysteries/MirrorSphere.lua:836`, `:16`, `:70`, `:585-588` |
| K-28 ◇ | `NightShiftWork` (F04) | No-wrap window verbatim. | `Lua/Units/Colonist.lua:2194-2204`, `:2361`; `_GameConst.lua:4`, `:395` |
| K-29 ◇ | `RocketInteractGuard` (F74) | Guard still names only legacy classes. | `Lua/Units/RCTransport.lua:412`, `:409`, `:458`; `UniversalRocket.lua:28-42` |
| K-30 ◇ | `SequenceLatents` (F29) | Both latent defects verbatim; still no-ops on shipped data. | `Lua/Sequences/SA_Filters.lua:33-39`; `Lua/Mysteries/Diggers.lua:91-95` |
| K-31 ◇ | `SinkholeIndestructible` (F96) | Sinkhole still unflagged; guard and meteor branch unchanged. | `Lua/BuildingTemplate/Sinkhole.generated.lua:4-25`; `Building.lua:1445`; `Meteors.lua:960-964` |
| K-32 ◇ | `TrackTunnelPowerBridge` (F65) | Two-element shortcut verbatim; `Done` still lacks grid teardown. | `Lua/Buildings/Track.lua:667-679`, `:69-76`, `:97-157`; `TrainTransport.lua:14-37`, `:82-114` |
| K-33 ◇ | `TrainsToVoid` (F64) | `BuildingDemolished` still `DoneObject`s every train at the station. | `Lua/Buildings/Station.lua:289-299`, `:264-279`; `Building.lua:899-909`; `Train.lua:157-192` |
| K-34 ◇ | `WispRewards` (F07 + F15) | Missing `* 1000` and the double RP grant both verbatim. | `Lua/Mysteries/Fireflies.lua:677-704` (`:690`, `:695`) |
| K-35 ◇ | `LayoutTechLock` (F19) | See A-5: correct, redundant with a new build-menu gate. | `LayoutConstruction.lua:335-339`, `:206-235`; `BuildMenu.lua:743`, `:784-786` |
| — | `TrainCargoDumping`, `LandscapeUnitFilter`, `LanderCargoRatchet` (gates) | The gates are correct and measured (`gated110_*`); their fixes are F-10, F-8 and R-2. | `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log:84`, `:105`, `:119` |

### 1e · Census

`grep -rln 'full replacement\|fully replaces\|a copy of' Code/Fix_*.lua`
returns 22 files; six are wrappers today whose headers still describe the
replacement they were converted from (`DroneTransportMinors`, `GeneForging`,
`ShuttleHubOffAvailable`, `SmallLandscapeSites`, `TrainWaitTime`,
`UpgradeModifierLeak`), and `AsteroidLanderAvailable` is a replacement the
grep does not catch. Real full-body replacements: **17**, all dispositioned.

**Totals over the 80 registered modules: FIX 10 · REMOVE 35 · KEEP 35** (the
split module counts once, as KEEP). The pre-audit hit rate held on the
replacements — seven of the twelve nobody had diffed needed action — and the
wrappers were not the safe half: of the 47 pass-3 modules, **19 do nothing on
1.1.0 and 4 do something wrong**.

## 2 · Ranked recommendations

1. **`SaintBlessing` (F-1) — P2, silent, OURS, applies today.** Same class as
   F112. Cost: one behavioural probe in the `DataPatch` pass, a parse sweep,
   one boot (expect `inactive (already handled)`), and a 5-minute attended
   control (a Saint in a dome with Religious colonists: with the pack, do they
   carry "Blessed by a Saint"?).
2. **`StaleReservations` (F-2) — P2, silent, applies today.** One exemption
   clause. Control: send an expedition, wait past 5 sols, check the crew's
   residence on return with the pack on.
3. **`ShelterReflex` half (a) (F-3) — throw on asteroid habitats with filters.**
   Delete the replacement; keep half (b). One boot.
4. **`FirstAsteroidPrefabs` (F-4) and `AstrogeologistExtractors` (F-5) — the
   two removals that are also harms today.** Each is an `items.lua` +
   `Code/` deletion (H-10) or, for a 1.0.7 line, a gate.
5. **`RocketDroneChurn` (F-7) and `PayloadTemplateRefill` (F-6) — P3,
   player-visible.** A re-copy each (F-7 is one clause); F-6 touches the new
   tutorial, so gate first, re-copy with a control.
6. **The REMOVE block (35 modules) — one owner decision, then cheap.** Every
   one is a body to re-verify at the next patch for zero benefit, four of them
   are marginally worse than vanilla today (R-6, R-23, R-30, R-33). ⚠️ Delete
   vs gate depends on decision 98 (a 1.0.7 line keeps them as gates).
   R-17 is a judgement and is marked so.
7. **The three gated re-derivations (F-8, F-9, F-10)** are correctly OFF and
   cost design work each; F-8 has the most player value (F34(d) reproduced
   20/20 on PT-60).
8. **A-3 first among the augments** — a tool edit, and the "17 inactive"
   headline is already wrong by one.

## 3 · What I did NOT check — named, not counted

- **Read by sub-readers, not re-opened by me (◇ rows):** every KEEP and REMOVE
  in pass 3 except those I name in the row (`TrainMinors` `Track.lua:424`,
  `TrainPlatformWedge` `ColonistTransport.lua:660-667`, `TechDef` population,
  the four FIX rows). Their quoted lines are in `scratchpad/pass3_[A-D].md`;
  those files are session scratch and are NOT in the repo — the rows above
  carry the citations.
- `TrackSalvageRefund`, `TrackConnectorPingPong`: KEEP on the trains sitting's
  record (F114 entry), not re-diffed.
- `TrainCargoDumping` (F-10): whether a `rfSuspended` request still reports a
  positive `GetTargetAmount` is C-side and unread — "plausibly persists".
- `DustSicknessDamage` (R-15): where 1.1.0 computes the damage now was not
  located; the REMOVE verdict does not depend on it.
- `MeteorStormWedge` (R-10): the residual (a valid meteor that never posts
  `MeteorDone`) was not chased.
- `VacuumWalks` (F-9): the semantics of a wrapper that passes a modified
  distance were not derived; the shuttle branch reacts to it.
- `ShelterReflex` (F-3): whether `pred(nil)` in every `ColonistFilterFunc`
  throws or returns falsy was not traced (the `traits_filter` path throws
  regardless).
- `StaleReservations` (F-2): `const.Scale.sols` and
  `g_Consts.TravelTimeExpeditionReturn` are not in the Lua tree; the
  ms-to-ms comparison stands on `__const.lua:175` and `Data/POI.lua`.
- Sub-reader "NOT CHECKED" items per module (e.g. `Colony.lua:863`
  `ColonyAddPrefabs` body, the `ExtractorPerformance` mix-in on
  `AutomaticMicroGExtractor`) are in the scratch files and none bears on a
  verdict.
- No 1.0.7 comparison anywhere — the tree is gone (`EF-075`). Every "1.1.0
  changed X" is the 1.1.0 line plus our module's own header or a bug entry as
  the record of the old shape.
- Nothing was run in a game. The one runtime source is the archived boot log.

## 4 · Pass 4 — the self-check design

**What actually broke, by class, with counts from this audit:**

| class | what changed under us | instances | what sees it today |
|---|---|---|---|
| (a) signature | same name, new parameter list | F115 | `sigcheck.py` (after the fact) |
| (b) body under a copy | same name/arity, body edited | F114, F116, F-6, F-7, F-9 | nothing |
| (c) semantics under a wrapper or data patch | the target's meaning or its data shape moved | F111, F112, F-1, F-2, F-3, F-5 | nothing |
| (d) vanilla fixed it | our correction is now redundant or double-applied | **32 modules** (R-5…R-36 less the target-gone rows) + F-1, F-5 | nothing — and the pack has no bucket for it |
| (e) target gone | the name no longer exists | 13 of the 17 inactive | `Require` (correctly) |

The existence checks cover (e) and nothing else. Class (d) is the largest by
an order of magnitude and was invisible by design: a module whose check
passes and whose transform is now applied on top of vanilla's own fix is the
F-1/F-5 shape, and it is silent.

**Recommendations, concrete and costed:**

1. **A behavioural `probe` form in `Require`** — `{ probe = function() … end,
   reason = … }` that CALLS the target on a stub and compares the effect,
   evaluated at apply time for pure functions and, via the `DataPatch` runner,
   after DataLoaded for preset-bound ones. `debug.getinfo` is absent, but
   calling a function on a stub is not. What it would have caught: F115
   (calling `LandscapeForEachUnit(stub_mark, cb)` on 1.1.0 indexes
   `map.Landscapes` on a non-map and throws ⇒ decline); F114 (`UnloadAll` on a
   stub station with a storable resource and no demand ⇒ nil index ⇒ decline);
   F111 (`GetWorkshiftPerformance` on a stub with `workers > auto` returns the
   workers' value ⇒ "already handled"); F-1 (the label capture in §1a); F-3
   (`GetScoreFor(traits_table)` throws on a stub with a filter). Constraints:
   only for targets verified synchronous and side-effect-free on a stub, and
   the stub contract is written next to the probe. Cost: ~10 lines per module,
   one afternoon for the 10 FIX rows; the rest opportunistically.
2. **A pinned-defect manifest and `tools/bodycheck.py`** — the runtime cannot
   read the game's source, but the repo can. Each module header gains two
   machine-readable lines: `-- SRC: Lua/Units/Train.lua Train:UnloadAll
   sha256=<hash of the shipped body at pin time>` and `-- DEFECT: <the literal
   shipped expression the module corrects, as a regex>`. `bodycheck.py` walks
   the live tree and reports, per module: `BODY-CHANGED` (hash differs ⇒ class
   b), `DEFECT-GONE` (the expression no longer appears in the target ⇒ class d,
   a REMOVE candidate), `TARGET-ABSENT`. Together with `sigcheck.py` (class a)
   that is the whole table this audit produced by hand, as a five-second run.
   Cost: one script (~150 lines, the harvest logic exists in
   `harvest_wrap_targets.py`), plus one header line pair per module — the
   hashes can be taken from the current 1.1.0 tree for the KEEP set as the new
   pin.
3. **Policy on replacement vs wrapping** — keep §1.4b's preference but stop
   treating wrappers as safe: 6 of the 10 FIX rows are wrappers or data patches
   (class c). The rule that actually discriminates is not the technique but
   whether the module carries a **discriminator for its own obsolescence** —
   the DEFECT line above. A module that cannot state the shipped expression it
   corrects cannot be re-verified and should not ship.
4. **The benign latch is a retire signal** (A-2): rename it in the log and in
   `logscan.py`, and have `bodycheck.py`'s `DEFECT-GONE` list feed the same
   REMOVE bucket. The pack needs the bucket the brief noticed nobody had used.
5. **Tools, so the next update is a run and not a week:** `sigcheck.py`
   extended to `SetGlobal` sites (A-4); `logscan.py` heal-aware (A-3);
   `bodycheck.py` (item 2). The update-day checklist becomes: run three
   tools, read one table, write the REMOVE/FIX prompts from it.
6. **The player dialog** should keep saying only what it can see (ck112's
   wording); the honesty limit does not shrink, the tooling around it does.

## 5 · For `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"

Filed as items 114–116 (same commit).

## 6 · Offer

If asked, I would write fix prompts for: (1) the five applies-today repairs
(F-1 probe-gate, F-2 exemption, F-3 half (a) deletion, F-4 and F-5 removal),
(2) the two re-copies (F-6, F-7), (3) the REMOVE block as one `items.lua` /
`Code/` prompt with its patch note, (4) `bodycheck.py` + the header manifest,
(5) `logscan.py` A-3. ⛔ Not written unprompted.
