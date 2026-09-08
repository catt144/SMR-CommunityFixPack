# PACK-WIDE 1.1.0 RE-VERIFICATION — what to FIX, REMOVE, or AUGMENT

Audit run 2026-09-08 against the shipped 1.1.0 tree
(`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, build
1.1.0.403908) by a fresh session (`smr-bugfixpack-1e`). Brief:
`prompts/PACK_1_1_0_REVERIFICATION.md`. Tree at `cc6f740`, clean. **No code
was written.** Every line number below is the 1.1.0 tree unless it names a
`Code/` file; `Code/` line numbers are the tree at `cc6f740`.

> ⚖️ **Method.** Every verdict rests on a body read of the shipped 1.1.0
> function beside our module, not on a name or a count. Where a verdict rests on
> something else (a recorded clearance, a C-side function I cannot read), the
> row says so. ⛔ **A source read is never `tested`.** Nothing here moves a
> status; the in-play controls are named where they matter.

## 0 · Status of this document

| pass | scope | state |
|---|---|---|
| 1 | the full-body replacements (22 grep hits; 17 real replacements + 5 that are wrappers today) | ✅ DONE — every one opened |
| 2 | the 17 modules that self-disable on 1.1.0 | ✅ DONE — every one opened |
| 3 | wrappers, `SetGlobal`, `DataPatch`, `F111` second look — the remaining 47 modules | ⏳ IN PROGRESS (checkpoint 1 commits passes 1–2 first) |
| 4 | the self-check design | ⏳ PENDING |

Sections 1–2 are complete for passes 1–2. Section 3 (not checked) is exact as
of this checkpoint and shrinks as pass 3 lands.

## 1 · The four buckets

Every module I opened lands in exactly one row. **Bold** = the verdict is
player-visible today. The `evidence` column is what I read; the `Code/` column
is where our side of it lives.

### 1a · FIX — broken or wrong on 1.1.0, ranked

| # | module (defect) | what is wrong on 1.1.0 | evidence (1.1.0 tree) | ours (`Code/`) | shape |
|---|---|---|---|---|---|
| F-1 | **`SaintBlessing` (F92)** | **1.1.0 FIXED the defect and our data patch now BREAKS the blessing.** `TraitPreset:AddDomeColonistsModifier` applies `GetTraitLabel(trait)` itself now; our pass has already rewritten `Saint.modify_trait` from `Religious` to `TraitReligious`, so vanilla computes `GetTraitLabel("TraitReligious")`, which returns `false` (no such preset) and the function returns without registering anything. With the pack on, **no Saint blesses anyone**; with it off, 1.1.0 works. The module ends the boot ACTIVE (`gated110_*.log:186` `corrected 1 … of 2`) — the 17-inactive count hides this. | `Lua/TraitPreset.lua:85-86` (`GetTraitLabel(trait)`; `if not label then return end`); `Lua/Traits.lua:1325-1328` (`if not TraitPresets[trait_id] then return false end`); `Data/TraitPreset.lua:404-405` (shipped value still `Religious`) | `Fix_SaintBlessing.lua:100-103` (the rewrite), `:151-181` (the LoadGame re-base does the same on saves) | gate on BEHAVIOUR, not on a name: after DataLoaded call the real `AddDomeColonistsModifier` on a stub unit/dome that captures the label, patch only if it captures `Religious` (1.0.7 shape), decline as "already handled" if it captures `TraitReligious`. Silent, wrong-number class ⇒ P2. |
| F-2 | **`PayloadTemplateRefill` (F70)** | Our 1.0.7 copy of `RetrieveRequests` reverts three 1.1.0 changes: (a) the **new tutorial's** rocket 2 is meant to be pre-filled from `AsteroidTutorialExpectedCargo` — our `resolve_loc_cargo_template` has no tutorial branch, so the tutorial rocket shows the ordinary flight-policy template; (b) a dialog opened from a **destination pick** (`prev_flight_data`) is meant to ignore stored cargo and re-apply the template even in `CmdLoad` — ours reads stored cargo and, once `SMRFixPack_payload_set` is set, suppresses the template; (c) the automode branch gained a nil guard on `cargo_items[id]` that ours lacks (`self.cargo_items[id].mode` on a nil entry raises). The F70 defect itself persists (`:216-234` still template-fills every zero row outside `CmdLoad`). | `Lua/CargoRequestNew.lua:169-192` (tutorial branch `:183-189`, `from_destination_pick` `:174`), `:199-213` (nil guard), `:215-217` (`requests = not from_destination_pick and transporter.cargo`); `Lua/TutorialsNew.lua:1019-1025` | `Fix_PayloadTemplateRefill.lua:57-68`, `:85-93`, `:97-99` | re-copy on the 1.1.0 body with the F70 gate applied only to the non-destination-pick path; or gate the module off on 1.1.0 (`AsteroidTutorialExpectedCargo ~= nil` is a real discriminator, not a proxy — it is the branch we lack). |
| F-3 | **`RocketDroneChurn` (F50)** | 1.1.0 added a player toggle "stop drones refuelling this rocket" and the request loop honours it with `not self.refuel_disabled`; our copy of the same loop does not, so with the pack on a rocket the player switched off **still requests fuel** every hour. The F50 defect itself persists (`:1431-1433`/`:1460-1462` still disconnect unconditionally), so the fix is still wanted. | `Lua/CargoTransporterNew.lua:1442`; `Lua/UniversalRocket.lua:70` (the property, "player stopped Drones from refueling"), `:3320` (the toggle) | `Fix_RocketDroneChurn.lua:63` | one clause: `is_refuel_resource and not self.refuel_disabled and …` — but as a re-copy of the 1.1.0 body, not a patch of the 1.0.7 one (the rest of `:1430-1463` is otherwise identical to ours). |
| F-4 | `LandscapeUnitFilter` (F34d) | Gated and correctly inactive (F115). The defect is still shipped: the body builds `filter_embark` and then passes `callback` to `Landscape_ForEachObject`. Players on 1.1.0 have the F34(d) defect back. | `Lua/Landscape/Landscaping.lua:509-522` (`:522` passes `callback`) | `Fix_LandscapeUnitFilter.lua` (body untouched, gate at the `Require` block) | repair the body on the `(map, mark, callback, ...)` signature reading `map.Landscapes[mark]`, KEEP the gate. Route (b) of F115, owner-ruled deferred (ck109). |
| F-5 | `VacuumWalks` (F52) | Correctly inactive — by ACCIDENT: the `const.ColonistMaxDomeWalkDist` path spec fails because 1.1.0 turned both walk constants into `g_Consts` entries. The defect line is unchanged (`min_dist = breathable and passage_dist or walk_dist`), so the fix is still wanted — but 1.1.0 REWROTE the rest of the function (work-slot reservation, `-1` = passage-only distance, shuttle-slot checks, `DiscardTransportTicket`), so re-arming our 1.0.7 copy would revert all of it. | `Lua/Units/Colonist.lua:1903` (defect), `:1896`, `:1904-1907`, `:1918-1926`, `:1932-1957`, `:1959-1968` (new); `:1901-1902` + `Lua/_GameConst.lua:149-150` (`DefineConstInt` ⇒ `g_Consts`) | `Fix_VacuumWalks.lua:41-44` (the accidental gate), `:49-98` (the 1.0.7 body) | re-derive on 1.1.0: either a re-copy of the new body with the one-line change, or a PRE-wrapper that hands `orig` a modified `transport_mode_dist` (needs a control — the shuttle branch reacts to the value). Reads `g_Consts` at call time. Convert the accidental gate into a deliberate one. |
| F-6 | `TrainCargoDumping` (F46) | Correctly inactive (F114). The F46 defect plausibly persists: 1.1.0's `UnloadAll` still has no enabled-resource check, and the new `SetAcceptResource` SUSPENDS the demand request (`rfSuspended`) instead of removing it — so a suspended request presumably still reports a target amount and the dump goes through. ⚠️ `GetTargetAmount` on a suspended request is C-side; I could not read it. | `Lua/Units/Train.lua:792-804`; `Lua/Buildings/MultiResourceDepot.lua:242-246` (`IsResourceEnabled = IsStoring`, `rfSuspended`), `:251-290` | `Fix_TrainCargoDumping.lua` (gated) | re-copy on the 1.1.0 body (`:779-805`, which also carries the BlackCube bookkeeping our copy lacks) with `station:IsResourceEnabled(res)` in the loop; keep the gate as the discriminator for the NEXT change. Nuisance class (ping-pong), not a stall. |

### 1b · REMOVE — the defect is gone, or the target is gone, and the module is now pure risk

⛔ Each row states WHY the defect is gone, with the shipped line. "It is
inactive" appears nowhere in this table as a reason.

| # | module (defect) | why the defect is gone on 1.1.0 | evidence (1.1.0 tree) | today | what removal costs |
|---|---|---|---|---|---|
| R-1 | `LowStorageWarning` (F12) | 1.1.0 **deleted** the Food and maintenance branches from `GatheredResourcesOnHourlyUpdate`; the "Insufficient Resources" notification now covers Power/Water/Air only, split into three grid families. Reinstating a warning the developers removed is a feature, not a repair. The gate is load-bearing: forced on, it throws hourly (`EF-081`). | `Lua/ResourceTracking.lua:222-310` (no `maintenance_resources`, no `Food`); `Data/NotificationPreset.lua:1019-1028` | inactive (gate) | nothing on 1.1.0. Keep only if a 1.0.7 line is kept (decision 98). |
| R-2 | `LanderCargoRatchet` (F68 + F71) | 1.1.0 rewrote `CreateAutoCargoRequest`: the export comparison now adds the loaded hold back (`GetLoadedCargoNotInOverview`) — that is F68 — and the weight budget is a fair-share allocation by desired weight, not alphabetical — that is F71 in a different shape. Both defects addressed upstream. | `Lua/UniversalRocket.lua:2046` (F68), `:2069-2086` (F71), `:2537-2546` | inactive (F113 gate) | nothing on 1.1.0. |
| R-3 | `TouristSatisfaction` (F09) | The Satisfaction stat is gone: `UpdateSatisfaction`, `ChangeSatisfaction`, `SatisfactionLowStatPenalty` have **zero** hits in the 1.1.0 Lua tree. Tourism itself survives (`HolidayRating:RewardApplicants`, `Lua/HolidayRating.lua:87`). | tree-wide grep, 0 hits; `sigcheck` ABSENT | inactive | nothing. |
| R-4 | `AutomationLawCompensation` (C39, F112) | 1.1.0 deleted vanilla's automation-law compensation entirely (`law_scale` 0 hits tree-wide); the laws still cut `max_workers` and nobody is compensated. Paying the eight families now manufactures the asymmetry C39 removed. (F112 has the full derivation.) | `Lua/Buildings/Workplace.lua:269-294` | inactive (`test` gate) | nothing — unless the owner wants to REBALANCE, which `FIX_POLICY` §4a bars. |
| R-5 | `UpgradeModifierLeak` (F03) | 1.1.0 fixed `StopUpgradeModifiers` — it now iterates with `pairs` over the id-keyed table. Our post-wrapper then calls `TurnOff` a second time on every modifier. Both `TurnOff`s are idempotent, so today this is harmless and useless. | `Lua/Buildings/Building.lua:1303-1311`; `CommonLua/Classes/Modifiers.lua:479-484` (`if not self.is_applied then return end`); `Lua/Modifiers.lua:277-280` | applied | nothing. ⚠️ `90_SaveSanitizer`'s F03 leaked-modifier sweep is a separate pass-3 row. |
| R-6 | `SmallLandscapeSites` (F33) | 1.1.0 rewrote `GetClosestDests` to delegate to `GetTopClosestDests`, which bounds-checks (`if count <= top_count then return table.icopy(dests)`). Worse than useless: our clamp passes `Min(top_count or 5, n)`, so with the pack on a large site's drones get the top **5** destinations where 1.1.0's default is **10**. | `Lua/Landscape/LandscapeConstructionSiteBase.lua:204-208`, `:171-177` (`top_count = top_count or 10`) | applied | nothing; removal RESTORES vanilla's 10. |
| R-7 | `DroneTransportMinors` **(b) only** (F57b) | 1.1.0 no longer swaps the unreachables table on passability change — the handler just bumps a per-map version, the table keeps its metatable, and `unreachable_buildings_count` is "kept for savegame compatibility" with **zero** readers. Our additive handler re-applies a metatable that is already there and writes a dead field, on every passability change, for every drone. **(a) stays** — see KEEP. | `Lua/Units/Drone.lua:935-937`, `:73`, `:943-945`; grep of `unreachable_buildings_count`: 1 hit (the declaration) | applied | remove the `OnPassabilityChanged` handler + `repair_unreachables`; keep the `UpdateRocketsInternal` wrapper. |
| R-8 | `DroneUnreachableForever` (F55) | The mechanism it corrected is gone: `MarkUnreachable` stamps `GameTime()` (no `+ max_int`), the 5-sol expiry and `const.UnreachablesCleanupDeltaT` are gone, and the table is reset on every passability/building change via the version bump. The "forever" the fix addressed no longer exists. | `Lua/Units/Drone.lua:889-911`, `:971-976`; `Building.lua:546`, `Landscaping.lua:328` (extra bump sites) | inactive | nothing. |
| R-9 | `MeteorFrequency` (F02, F88) | The dead `if` is gone with the thread: 1.1.0 schedules meteors as a `MapGameTimeRepeat` that stores `g_NextMeteorsTime = GameTime() + Random(spawntime, spawntime + spawntime_random)` and sleeps until it — the designed 35–115 h. `_G.Meteors` is now `GameVar("Meteors", false) -- required only for the savegame fixup`, so our thread-keyed wrapper could never match; the watchdog's `RestartGlobalGameTimeThread("Meteors")` would call `CreateGameTimeThread(nil)`. The fixup also migrates old saves. | `Lua/Meteors.lua:293-322`, `:388`, `:390-412` (`SavegameFixups.MeteorsThreadToRepeat2`) | inactive | the `SMRFixPack_MeteorLatch` GameVar stays in saves as inert data (already disclosed). |
| R-10 | `MeteorStormWedge` (F78) | The observed wedge — descriptors that never became invalid — is addressed: the drain loop now validates on `IsValid(descr.meteor)`; the scheduler is a `MapGameTimeRepeat` (our `RestartGlobalGameTimeThread("MeteorStorm")` heal would fail the same way as R-9); and the savegame fixup kills any thread inside `MeteorsDisaster` on load and ends a stuck storm. ⚠️ Residual: the loop is still unbounded if a meteor object stays valid forever without posting `MeteorDone`; not the case we measured. | `Lua/Meteors.lua:267-270`, `:329-386`, `:390-412` | inactive | nothing measured. If the owner wants the residual covered, that is a NEW module on the new mechanism, not this one re-armed. |
| R-11 | `AsteroidLanderAvailable` (F72 + F94) | The gate and the list can no longer disagree: both are built on `IsRocketAvailableForFlight` + `GetAvailableFlightLocations()`. `PlanetaryAsteroidVisitPossible` no longer exists. | `Lua/PlanetaryView.lua:245-252`, `:258-265`; `Lua/UI/PlanetUI.lua:1701-1710`; `Lua/XDef/PlanetaryViewAsteroidResources.generated.lua:41-45` | inactive | nothing. |
| R-12 | `GridGlobalStorage` (F22) | `GetGridGlobalStorage` is gone; the replacement is per-dome (`ScriptFunc_DomesGridStorage`) and never sums ratios or uses the 1000-hour sentinel. | `Lua/ScriptBlocks.lua:387-419` | inactive | nothing. |
| R-13 | `LastTransmissionStorage` (F75) | ⭐ The brief's seed example, confirmed: every storage like now sets `'Condition'` (not `Prerequisite`) with a `ScriptCheckDomesGridStorage` whose `Resource` is right — the Oxygen entries say Oxygen. The "already correct" latch IS 1.1.0 having fixed it. | `Data/FactionDef/LastTransmission.lua:104-260` (`:245` `Resource = "Oxygen"`) | inactive (benign latch) | nothing. |
| R-14 | `RainsDeadlock` (F81b + C34 rider) | The untimed `WaitMsg` loop is gone: rains run as a repeat cycle that creates a fresh activation thread whenever none is alive. Re-arming would be HARMFUL: our wrapper posts `Msg("RainDisasterEnd")` on a collision, and 1.1.0 binds that message to a lightmodel handler; our migration pass calls `RainsDisasterLoop`, which no longer exists. | `Lua/TerraformingDisasters.lua:363-395`, `:142`, `:191-194` | inactive | the C34 stale-state heal goes with it; if wanted, re-derive against `:485-500`. |
| R-15 | `DustSicknessDamage` (F17) | `daily_update_func` has **zero** hits in 1.1.0 Lua and Data — the function that discarded `change` is gone with its defect. Where dust-sickness damage is computed now was NOT located (not needed for this verdict; it is a re-derivation if anyone suspects the new path). | tree-wide grep, 0 hits | inactive | nothing. |
| R-16 | `IndependenceTerraforming` (F18) | The tech is self-consistent now: `param1 = -10` and the effect's `Amount` is BOUND to `param1`. There is no contradiction to repair; the LoadGame sweep also has nothing to correct (it stands down on "fix not active"). | `Data/Tech.lua:3557-3562`, `:3571-3577` (`param_bindings = { Amount = "param1" }`) | inactive | nothing. |
| R-17 | `UniversityOvertraining` (F36) | The DEFECT LINE is unchanged, but the fix's premise is false on 1.1.0: automation is now a FLOOR — a staffed automated extractor performs at `Max(workers, auto_performance)` (vanilla's own comments: "excludes the automation floor", "the automation floor exceeds (or matches) the crew's output"). Specialists at an automated extractor DO raise output, so counting those posts is no longer overtraining. Keeping F36 is now a balance opinion, and our copy also reverts 1.1.0's cache-reusing rewrite. | `Lua/Buildings/Workplace.lua:283-287`, `:249`, `:433-434`; `Lua/City.lua:636-661` (rewrite), `:648` (the line) | applied | ⚖️ owner call — this is the one REMOVE that is a judgement, and I state it as one. |

### 1c · AUGMENT — the fix works, but its self-check cannot see the failure that bites

| # | module | what the check misses | what it should test instead |
|---|---|---|---|
| A-1 | `GeneForging` (F41) | Works on 1.1.0 (see K-4), but reads the bonus from `TechDef.GeneForging.param1` — the LEGACY preset map. 1.1.0 computes tech values from `Techs.<id>:ResolveValue("param1")` (modifiable). If a patch drops `TechDef` or a mod modifies the parameter, our bonus silently becomes 0. | read `Techs.GeneForging:ResolveValue("param1")` when `Techs` exists, fall back to `TechDef`; add `{ global = "Techs", kind = "table" }` as a soft check that LOGS rather than declines. |
| A-2 | every `DataPatch` benign latch | "the shipped presets are already correct" is filed as HEALTHY. R-13 shows it is the REMOVE signal. | make the benign latch line say so: `inactive (already correct — RETIRE candidate: the game may have fixed this)`, and have `logscan.py` list benign latches under their own heading. |
| A-3 | `logscan.py` verdict logic | "last verdict wins" misses a `DataPatch` heal: `SaintBlessing` logs `inactive` at `:166` and `corrected …` at `:186` and ENDS ACTIVE, but the tool (and the "17 inactive" headline) count it inactive. The true end-of-boot count on `gated110_*` is **16**. | treat `corrected` / `made effective` / `re-based` lines as a heal (status active) in the tool; print both the first-pass and final counts. |
| A-4 | `sigcheck.py` | Reads `function Name(...)` definitions only; the 15 `SetGlobal` sites and anonymous `X = function(...)` literals are outside it (F115 entry). | extend to `SetGlobal("Name", <expr>)` sites by resolving the local the expression names. (Pass 4 carries the design.) |

### 1d · KEEP — verified fine, with the reason

| # | module (defect) | why it is fine on 1.1.0 | evidence (1.1.0 tree) |
|---|---|---|---|
| K-1 | `BombardmentSpread` (F26) | Body byte-identical to our copy; the defect is still shipped (`spawn_dir` computed at `:82`, `dir` used at `:83`). The only nearby change is `g_IncomingMissiles` becoming a `MapVar`, which both bodies already read as `map.g_IncomingMissiles`. | `Lua/Bombardment.lua:38-50`, `:53`, `:55-154` (`:82-83`), `:52` |
| K-2 | `DomeFreeSpaceMismatch` (F60) | Still calls `GatherFreeLivingSpaces(self.labels.Residence)` with no second argument; `GatherFreeLivingSpaces` still keys the member on it; the sibling contradiction stands (`GetFreeWorkplaces` and `ResourceOverview` use `ui_working`/`"player_enabled"`, `ChooseResidence` and `UpdateResidence` test `ui_working`). Our two-line copy is the shipped body plus the argument. | `Lua/Buildings/Dome.lua:3353-3355`; `Lua/_GameUtils.lua:535-558` (`:541`), `:526`; `Lua/ResourceOverview.lua:687`; `Lua/Buildings/Residence.lua:452`; `Lua/Units/Colonist.lua:2923` |
| K-3 | `DomeOverviewHighlight` (F14) | Body byte-identical to our copy; `win.idLabel:SetText(v)` still discards `tv`. | `Lua/X/ColonyControlCenter.lua:1290-1300` |
| K-4 | `GeneForging` (F41) | `GetRareTraitChance` still knows only `GeneSelection`; `GeneForging` has no consumer in Lua. 1.1.0 dropped the parameter (`function GetRareTraitChance()`), and both callers pass nothing — our wrapper's `unit` is nil and takes the `MainCity` path it already had. `TechDef` is still a populated `GlobalMap` (`Data/TechPreset.lua` still places `GeneForging` with `param1 = 50`; `Research.lua:358` still reads it), so the bonus resolves. See A-1. | `Lua/Units/Colonist.lua:4398-4402`, `:4419`; `Lua/Traits.lua:1049`; `Data/TechPreset.lua:1311-1314`; `Data/Tech.lua:8971-8976`; `ClassDef-PresetDefs.generated.lua:1729` |
| K-5 | `ShuttleHubOffAvailable` (F54) | `IsLRTransportAvailable` is byte-identical; the lax `GetWorkNotPermittedReason` clause is still there; `hub.shuttle_infos` / `transport_mode` unchanged. | `Lua/Buildings/ShuttleHub.lua:410-419` |
| K-6 | `ShuttleTransportCache` (F51) | Body identical to ours bar the fix; the cache is still keyed on `(community, pos)` only. 1.1.0 ADDED flush sites (Train label add/remove, RocketLanded/Launched) — none for a Shuttle Hub, so the defect stands. | `Lua/Units/Colonist.lua:3156-3204` (`:3199-3202`), `:3122-3153` |
| K-7 | `TrainWaitTime` (F21) | The three `AddSpentTime` call sites are unchanged (station at boarding, train + track at exit), `BoardVehicle` still does not restamp `start_wait`, `ExitVehicle` still measures from it; `waiting_for_train` and `command_thread` still exist as class defaults. ⚠️ The Comfort half of F21 is GONE from vanilla (`ExitVehicle` no longer charges "travel time" Comfort) — that changes nothing about the wrapper, which only moves the timestamp. | `Lua/Units/ColonistTransport.lua:614-639` (`:622`), `:660-699` (`:671`, `:696-697`); `Lua/TransportStatistics.lua:31-37`; `Station.lua:79`, `:123`; `CommandObject.lua:90` |
| K-8 | `DroneTransportMinors` **(a)** (F57a) | `UpdateRocketsInternal` still clears only `r_t.Fuel` and still writes `r_t[r.FuelResource]` on the `UniversalRocketBase` branch (now via `table.get(r, "demand", r.FuelResource)`). R3-latent as before. | `Lua/Buildings/DroneControl.lua:672-698` (`:674`, `:691-693`), `:13`, `:196-200` |
| K-9 | `TrackSalvageRefund` (F47) | ⚠️ **On record, not re-read here:** cleared line-for-line bar its own fix by the trains sitting 2026-09-08 (F114 entry). `sigcheck` OK on both sites. I did not re-diff it. | `agent/bugs/F114.md` (the clearance) |
| K-10 | `TrackConnectorPingPong` (F66) | ⚠️ **On record, not re-read here:** cleared as a copy of 1.1.0's `CreateConnectorElements` by the same sitting (F114 entry). | `agent/bugs/F114.md` |
| K-11 | `TrackSalvageWipe` (F116) | Repaired in-body 2026-09-08; two deliberate divergences remain and are owner-facing (orphan policy, mixed-array post-processing). Not reopened, per the brief. | `agent/bugs/F116.md` |
| K-12 | `TrainCargoDumping`, `LandscapeUnitFilter`, `LanderCargoRatchet` (gates) | The gates are correct and measured (`gated110_*`). Their fixes are re-filed above as F-6, F-4 and R-2. | `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log:84`, `:105`, `:119` |

### 1e · Pass-1 census, so the count stops being "~17 of ~22"

`grep -rln 'full replacement\|fully replaces\|a copy of' Code/Fix_*.lua` returns
22 files. Six of them are **wrappers today** whose headers still describe the
replacement they were converted from (2026-08-02): `DroneTransportMinors`,
`GeneForging`, `ShuttleHubOffAvailable`, `SmallLandscapeSites`,
`TrainWaitTime`, `UpgradeModifierLeak`. `AsteroidLanderAvailable` is a
replacement the grep does NOT catch (a `SetGlobal` body copy). So the real
full-body replacement set is **17**: Bombardment, DomeFreeSpace, DomeOverview,
LanderCargoRatchet, LowStorageWarning, PayloadTemplateRefill, RocketDroneChurn,
ShuttleTransportCache, TouristSatisfaction, UniversityOvertraining, VacuumWalks,
TrainCargoDumping, LandscapeUnitFilter, TrackSalvageWipe, TrackSalvageRefund,
TrackConnectorPingPong, AsteroidLanderAvailable. All 17 are now dispositioned
(15 read here, 2 on the trains sitting's record). **Of the 17: 3 KEEP, 4 REMOVE,
5 FIX, 2 gated-and-REMOVE/FIX, 3 on record.** The pre-audit hit rate held: of
the twelve replacements nobody had diffed, seven needed action.

## 2 · Ranked recommendations

1. **`SaintBlessing` (F-1) — P2, silent, player-visible, and OURS.** A player with
   the pack on 1.1.0 has a Saint whose blessing reaches nobody; 1.1.0 without
   the pack works. Same class as F112 (a correct 1.0.7 transform applied on top
   of vanilla's own fix). Cost: one behavioural probe in the `DataPatch` pass, a
   parse sweep, one boot log (the module should read `inactive (already
   handled)`), and a 5-minute attended control (a Saint in a dome with Religious
   colonists: with the pack, do they carry "Blessed by a Saint"?).
2. **`RocketDroneChurn` (F-3) — P3, player-visible.** The new "stop refuelling"
   toggle is half-ignored with the pack on. Cost: a re-copy of the 1.1.0 body
   with the F50 change (the bodies differ by exactly the one clause), one boot.
3. **`PayloadTemplateRefill` (F-2) — P3, player-visible, and it touches the new
   tutorial.** Cost: a re-copy on the 1.1.0 body, or a gate. Recommend the GATE
   first (the tutorial discriminator is real), the re-copy with a control.
4. **The REMOVE list (R-1…R-17) — one owner decision, then cheap.** Sixteen
   modules do nothing useful on 1.1.0, two of them do something wrong (R-6, R-7),
   and every one of them is a body to re-verify at the next patch. Each removal is
   an `items.lua` + `Code/` deletion (H-10) plus a patch note. ⚠️ Removing a
   module also removes its 1.0.7 behaviour; if decision 98 keeps a 1.0.7 line,
   the removal is a gate, not a deletion. R-17 is a judgement and is marked so.
5. **The three re-derivations (F-4, F-5, F-6)** are correctly OFF today and cost
   real design work each. None is urgent; F-4 has the most player value (F34(d)
   was reproduced 20/20 on PT-60).
6. **A-3 first among the augments** — it is a tool edit, and the "17 inactive"
   headline is already wrong by one.

## 3 · What I did NOT check — named, not counted

⛔ A module not in this list is not a module that passed.

**Pass 3 has not started at this checkpoint.** The following 47 modules were
NOT opened in passes 1–2 and carry NO verdict yet: `AnomalyCaveInMap`,
`ArrivalDeaths`, `AstrogeologistExtractors`, `BrokenTrackSalvage`,
`CaveInsNoDisasters`, `CommandCenterNumbers`, `CrystalMysteryHang`,
`DestroyedTunnels`, `DisasterPredictionLeak`, `DustDevilSpawnGate`,
`DustDevilsDescrMap`, `DustSicknessBiorobots`, `DustStormUndergroundBreaks`,
`ExoticDepositSign`, `ExtenderFlapChurn`, `ExtractorStaffedPerformance` (F111,
second look owed), `FirstAsteroidPrefabs`, `FounderTraitNotification`,
`FreedHousingNotice`, `GhostFarmOxygen`, `GraphConsumedCaption`,
`JumboCaveReinforcementWedge`, `LakeEntombment`, `LanderEmptyLaunch`,
`LanderReturnFuel`, `LandscapeCostRefresh`, `LayoutTechLock`,
`LocalizedUIText`, `MilestoneCrash`, `MirrorSphereSite`,
`MoraleComfortTooltip`, `NightShiftWork`, `RocketInteractGuard`,
`SequenceLatents`, `ShelterReflex`, `SinkholeIndestructible`,
`SpaceYDroneCapBullet`, `StaleReservations`, `StorageRateModifiers`,
`TechDescriptionBuilding`, `TouristApplicants`, `TrackTunnelPowerBridge`,
`TrainMinors`, `TrainPlatformWedge`, `TrainsToVoid`, `WispRewards`,
`90_SaveSanitizer`.

**Within passes 1–2, the limits of what was read:**
- `TrackSalvageRefund` and `TrackConnectorPingPong` were NOT re-diffed by me;
  their KEEP rests on the trains sitting's record (F114 entry).
- `TrainCargoDumping` (F-6): whether a `rfSuspended` request still reports a
  positive `GetTargetAmount` is C-side and unread; "plausibly persists" is the
  honest strength.
- `DustSicknessDamage` (R-15): where 1.1.0 computes dust-sickness damage now was
  not located. The REMOVE verdict does not depend on it; a claim that the NEW
  path is defect-free would.
- `MeteorStormWedge` (R-10): the residual (a valid meteor that never posts
  `MeteorDone`) was not chased.
- `VacuumWalks` (F-5): I did not derive the semantics of a wrapper that passes a
  modified distance; the shuttle branch reacts to it, and that needs a control.
- No 1.0.7 comparison anywhere — the tree is gone (`EF-075`). Every "1.1.0
  changed X" above is supported by the 1.1.0 line plus our module's own header
  or a bug entry as the record of the 1.0.7 shape, never by a 1.0.7 read.
- Nothing was run in a game. The one runtime source is the archived boot log.

## 4 · Pass 4 — the self-check design

⏳ PENDING at this checkpoint. Seeds already on the table from passes 1–2:
- F-1's shape (a behavioural probe on a stub, after DataLoaded) is the general
  answer to "test the thing": a `Require` `{ probe = function() ... end }` form
  that CALLS the target on a captured stub and compares the effect, which
  `debug.getinfo` cannot give us and a name cannot either.
- R-13/A-2: a benign latch is a retire signal, and the pack has no bucket for
  "vanilla fixed it".
- A-3/A-4: the two tools each have a named blind spot found this pass.

## 5 · For `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"

Drafted, NOT yet filed (a sibling session is editing the checklist for
112/113; I will file after pass 3 so the owner gets one item, not two):
- **114 — the REMOVE list.** Retire on 1.1.0 (delete vs gate depends on
  decision 98): R-1…R-16 as a block, R-17 as a separate yes/no.
- **115 — `SaintBlessing` repair shape.** Behavioural probe (recommended) vs
  retire the module (1.1.0 has the fix; the module only matters for a 1.0.7 line).
- **116 — the two small re-copies** (`RocketDroneChurn`, `PayloadTemplateRefill`)
  now, or gate them and re-copy later.

## 6 · Offer

If asked, I would write fix prompts for: (1) `SaintBlessing` probe-gate,
(2) `RocketDroneChurn` + `PayloadTemplateRefill` re-copies, (3) the REMOVE
block as one `items.lua`/`Code/` prompt with its patch note, (4) `logscan.py`
A-3. ⛔ Not written unprompted.
