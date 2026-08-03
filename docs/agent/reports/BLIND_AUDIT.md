# Blind Audit — are these fixes actually needed?

**Date:** 2026-08-02
**Auditor:** fresh agent session, no prior context on this project
**Scope:** all 66 `Code/Fix_*.lua` modules, graded against the shipped game source
at `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`
**Commissioned as:** an audit task. No fix code and no game code was modified.

---

## 1. What this document is

An independent answer to one question, asked once per fix module:

> **Is the defect this fix claims to repair actually present in the shipped game
> code — or does the way the game has it look like it would work?**

That is deliberately *not* the same as "is this fix good", "is this fix correct",
or "is this fix safe". Those are different audits. This one grades the
**premise**, not the repair.

The permitted answers were fixed in advance: **Yes / No / Maybe yes / Maybe no /
I don't know.** "I don't know" was explicitly allowed, and it is used twice
below, because two fixes turn on behaviour that is not readable from Lua at all.

---

## 2. Methodology

### 2.1 The two-sweep structure

The audit was run in two passes, by instruction, to keep the project's own
written conclusions from contaminating the first read:

**Sweep 1 — blind.** Read each `Fix_*.lua`, extract its factual claim about the
game, then go read the named game source and decide. **`docs/` was off-limits
entirely** — no `BUGS.md`, no `ENGINE_FACTS.md`, no `FIX_POLICY.md`, no reports,
no archive. The only project files read were `Code/00_Core.lua` (to understand
the registration/patching harness) and the 66 fix modules themselves.

**Sweep 2 — informed.** Read `docs/agent/ENGINE_FACTS.md` and re-check every
sweep-1 verdict against it. Sweep 1's results were recorded before sweep 2
started and were **not** edited afterwards; where sweep 2 moved a verdict, both
are shown side by side and the delta is stated.

Sweep 2 was restricted to `ENGINE_FACTS.md`. `BUGS.md`, the reports directory and
the archive were never read in either sweep, so nothing here is downstream of the
project's own bug write-ups, playtest logs or prior audits.

### 2.2 What "verified" means in the tables below

Three grades of evidence are distinguished, and the distinction matters:

| Grade | Meaning |
|---|---|
| **Source-verified** | I read the exact shipped lines and the defect is visible in them. A control existed: usually a sibling function in the same file that does the same job correctly, or the value/table/type being misused. |
| **Structurally verified** | The mechanism is visible in source, but the *consequence* the fix claims (a colonist dies, a player notices, a save wedges) is one inference step beyond what the code shows. |
| **Unverifiable** | The decision turns on an engine C export with no Lua body, or on binary asset data. Marked "I don't know" and left there. |

Where a fix header made a claim I could not confirm, I said so rather than
inheriting it.

---

## 3. Limitations — read these before using this document

These are real and some of them are load-bearing.

1. **I never ran the game.** Every verdict is static reading. No save was
   loaded, no fix was installed, no behaviour was observed. Anything that
   depends on runtime state, timing, or scale is inference.

2. **Engine C exports are opaque.** `ModTools\Src` contains Lua only. Functions
   like `GatherResourceOverviewData`, `GatherTransportableResources`, `IsValid`,
   `table.validate`, `Landscape_ForEachObject`, `CreateGameTimeThread` and
   `pf.AddTunnel` exist as documentation stubs or not at all. **Two fixes turn
   entirely on such a function and are ungradeable from source** (§7).

3. **Entity/spot geometry is binary.** Anything that depends on where a
   building's attachment spots physically land — most notably
   `TrackTunnelPowerBridge` and `TrackConnectorPingPong` — cannot be decided
   from Lua. I graded what the code does with the geometry, not the geometry.

4. **Reachability is frequently undecidable from source.** "This code is wrong"
   and "a player will hit this code" are different claims. Where the second one
   needs a playthrough, I said "latent" or "maybe" rather than "yes".

5. **⚠️ Anchoring bias, disclosed.** The fix headers in this pack are
   unusually detailed — they cite file, function and line for every claim. That
   makes verification fast and it makes *confirmation* fast, which is not the
   same thing. My mitigation was to read the surrounding function rather than
   the cited line alone, and to look for the sibling/control the header often
   names. But a header that pointed me at the wrong line would have been caught;
   a header that pointed me at the right line for the wrong reason might not
   have been. **This audit is not adversarial about framing, only about
   fact.** Two verdicts below (`DroneUnreachableForever`,
   `DustSicknessBiorobots`) exist precisely because I disagreed with a framing
   whose facts were all correct.

6. **I did not audit the repairs.** Not whether the patch installs, not whether
   the self-check targets the declaring class, not whether the module is
   save-safe (the F86 class of concern), not whether it introduces regressions.
   A fix can be right about the bug and wrong about everything after that.
   Several modules in this pack replace substantial function bodies; none of
   those copies was diffed against the shipped original.

7. **Single-pass, single-auditor, no second opinion.** No verification agent, no
   adversarial re-check, no vote. Any individual verdict below should be treated
   as one careful reading, not as a finding.

8. **Multi-defect files are graded per file in the headline tally.** Six modules
   fix more than one thing and two of those split across verdict tiers. The
   splits are called out explicitly; the tally table shows both counts.

---

## 4. Verdict scale

| Verdict | Definition |
|---|---|
| **Yes** | The defect is present in the shipped source and a normal player can reach it. |
| **Yes (latent)** | The defect is present and provable in code, but no shipped data or shipped call path reaches it. Real for mods/DLC/future updates; invisible in vanilla today. |
| **Maybe yes** | The mechanism is verified in source; the harm, frequency or reachability is one inference beyond what the code shows. |
| **Contested** | The behaviour is verified, but the shipped code carries evidence that it is *deliberate*. Calling it a defect is a design judgment, not a code finding. |
| **I don't know** | The decision turns on an engine C export or binary data. Not gradeable from source. |

---

## 5. Tally

| Verdict | Files (of 66) | Distinct defect claims (of 72) |
|---|---|---|
| Yes | 50 | 51 |
| Yes (latent) | 3 | 6 |
| Maybe yes | 9 | 10 |
| Contested | 2 | 3 |
| I don't know | 1 | 2 |

*The two counts differ because six modules fix more than one thing. Split
modules: `LanderCargoRatchet` (Yes + I-don't-know), `DroneTransportMinors`
(Yes + Yes-latent), `ShelterReflex` (Maybe yes + Contested), `SequenceLatents`
(two latent claims), `WispRewards` (two Yes claims), `ArrivalDeaths` (two claims,
both Maybe yes).*

**No verdict changed direction between sweeps.** Five moved in confidence, two
stayed stuck, and sweep 2 surfaced one stale line in `ENGINE_FACTS.md` itself
(§8.3).

---

## 6. Findings — Tier 1: Yes

Source-verified defects a player can reach. Each entry states the shipped
behaviour, then why I called it a defect rather than a design choice.

### 6.1 Dead code and discarded values

These are the strongest class in the pack: a value is computed, evidently on
purpose, and then not used. In every case there is a control — a sibling line, a
sibling function, or the computation's own existence.

| Fix | Shipped source | Reasoning |
|---|---|---|
| **UpgradeModifierLeak** (F03) | `Building:StopUpgradeModifiers` (`Building.lua:1268`) iterates `ipairs(self.upgrade_modifiers)`. `ApplyUpgrade` (`:1168-1171`) builds that table keyed by upgrade-id **string**. | `ipairs` over a purely string-keyed table iterates zero times, so `modifier:TurnOff()` never executes. **Control:** the immediately adjacent `ApplyUpgradeModifiers` (`:1254-1266`) iterates `pairs(self.upgrade_id_to_modifiers)` — the same author, the same job, done correctly, ten lines up. **Yes.** |
| **DustSicknessDamage** (F17) | `TraitPresets.DustSickness.daily_update_func` (`Data\TraitPreset.lua:85-91`): `local change = 5 + colonist:Random(trait.param)` then `colonist:ChangeHealth(-trait.param*const.Scale.Stat, trait.id)`. | `change` is written and never read. The randomiser exists for exactly one purpose. **Yes.** |
| **BombardmentSpread** (F26) | `WaitBombard` (`Bombardment.lua:82-83`): `local spawn_dir = GenerateDir(dir, angle)` then `local spawn_pos = dest_pos + SetLen(dir, travel_dist)`. | `spawn_dir` is never referenced again anywhere in the function. `GenerateDir(dir, angle)` exists only to jitter — its whole body re-rolls elevation around the passed angle. **Control:** `Meteors.lua:106-107` does the equivalent thing and uses the deviated direction. **Yes** (cosmetic severity). |
| **LandscapeUnitFilter** (F34d) | `LandscapeForEachUnit` (`Landscaping.lua:455-469`) builds `filter_embark` (dedup + `command ~= "Embark"`) and then calls `Landscape_ForEachObject(…, callback, …)`. | The filter is constructed and discarded. **Control:** `LandscapeForEachStockpile`, the function directly above (`:436-451`), is written identically and *does* pass its `filter_parent`. Copy-paste slip, not a decision. **Yes.** |
| **DomeOverviewHighlight** (F14) | `Community:UICommandCenterStatUpdate` (`ColonyControlCenter.lua:1309-1320`) builds `tv` with a `<red>` wrapper, then `win.idLabel:SetText(v)`. | Same shape: build the display value, pass the raw one. **Yes.** |
| **SequenceLatents (a)** (F29a) | `SA_GetLabelToRegister:SAExec` (`SA_Filters.lua:30-40`) computes `count` from `random_percent`/`random_count`, `table.shuffle`s, and `return objs` — the whole list. | The shuffle is the tell: it exists only to make a truncation fair, and there is no truncation. The editor text (`:20-27`) advertises "Get %s objects of label %s". **Yes** — but see Tier 2, it is mod-facing only. |
| **SequenceLatents (b)** (F29b) | `AlienDigger:GameInit` (`Diggers.lua:91-95`): `local t = a; a = b; b = a`. | `t` is saved and never read; both fields end up holding the larger value. Textbook broken swap. **Yes** — latent, see Tier 2. |
| **FounderTraitNotification** (F23) | `ColonyViability.lua:282-295`: `FounderGainsTraitCategories = { "Positive", "Negative", "Specialization" }`, consumed as `FounderGainsTraitCategories[TraitPresets[trait_id].group]`. | The strings are values at integer keys 1..3; the lookup by group name is always nil, so the condition is false for every trait and the notification can never fire. **Yes.** |

### 6.2 Wrong operator / wrong scale / wrong arithmetic

| Fix | Shipped source | Reasoning |
|---|---|---|
| **TouristApplicants** (F08) | `HolidayRating:RewardApplicants` (`HolidayRating.lua:77`): `if Random(0,100) > self.rewards[rating].bonus_chance`. Rewards table at `:2-11` has `bonus_chance` 40, 80, 25, 50, 75, 0, 50 ascending by star band. | With `>`, a higher `bonus_chance` means a *lower* payout probability: 1★ (40) pays ~60% of the time, 2★ (80) pays ~20%. The reward table is otherwise strictly monotonic in stars — money 2M→38M, fixed_applicants 0→2. A field named `bonus_chance` that inversely controls the bonus is not a design. **Yes.** |
| **TouristSatisfaction** (F09) | `Colonist:UpdateSatisfaction` (`Colonist.lua:4006-4032`). Up-crossings are gated exclusive (`new >= low and new < high and old < low`; `new >= high and new < 100 and old < high`); down-crossings are not (`new < low and old >= low`, etc.). | Traced 0→100: the low branch fails (`new < high` false), the high branch fails (`new < 100` false), only `+perfect` pays. Traced 100→0: all three penalties charge. So multi-tier jumps are asymmetric and satisfaction is path-dependent downward. Two-tier jumps are routine (a service visit sets Comfort directly). **Yes.** |
| **LowStorageWarning** (F12) | `ResourceTracking:GatheredResourcesOnHourlyUpdate` (`ResourceTracking.lua:218`, and again at `:230` for Food): `transportable_resources[k]*const.HoursPerDay / v*const.HoursPerDay`. Guard: `num_hours > 0 and num_hours < const.MinDaysMaintenanceSupplyBeforeNotification` (= 3, `_GameConst.lua:10`). | Parses as `((a*24)/v)*24`. With truncating integer division the inner term is either 0 (→ product 0, fails `> 0`) or ≥1 (→ product ≥24, fails `< 3`). The add branch is **unsatisfiable for every input**. So the "Insufficient Resources" warning is dead for Food and all maintenance resources. **Control:** the grid branches further down (`:247-310`) use a different, correct formula, which is why Power/Water/Air warnings do work. **Yes.** |
| **GridGlobalStorage** (F22) | `GetGridGlobalStorage` (`ResourceOverview.lua:891-899`) returns `GetGridGlobalStorageInSols(MainCity, X) + GetGridGlobalStorageInSols(UndergroundMap and UndergroundMap.City, X)`; the per-city function returns `1000 * const.HourDuration` when `required == 0`. | Two problems, both arithmetic: (1) adding two *ratios* is not a ratio — 1 sol of reserve on each map reads as 2 sols of reserve, which is true of neither; (2) the no-demand sentinel is 1000 **hours** (~41 sols), so an underground city with no demand yet contributes 20× the `> 2 sols` threshold on its own, permanently. Consumers are the six Last Transmission conditions and any `ScriptCheckGridGlobalStorage`. **Yes.** |
| **NightShiftWork** (F04) | `Colonist:ShouldLeaveForWork` (`Colonist.lua:1758-1768`): `hour >= workshift_start - 1 and hour <= workshift_start + 3`. `const.DefaultWorkshifts = {{6,14},{14,22},{22,6}}` (`_GameConst.lua:370`). | Shift 3 start = 22 → window 21..25 on a 0-23 clock. Hours 0 and 1 — the catch-up window for a colonist who was busy at shift start — are unreachable. **Control:** the codebase handles wrap-around correctly elsewhere (`IsDarkHour` uses `% 24`), and shifts 1 and 2 are unaffected, so the omission is specific to the wrapping shift. **Yes.** |
| **MirrorSphereSite** (F16) | `MirrorSphereBuildingBase:StartAction` (`MirrorSphere.lua:823`): `if not self:IsActionEnabled(action) or self.progress == 100 then return end`. `local max_progress = 2^22` (`:16`). | `progress` runs 0..2^22, which is why `GetProgressPct` divides and `SetProgress` clamps to `max_progress`. A `== 100` test on that scale is a 1-in-4-million coincidence, not a completion check. **Yes.** |
| **WispRewards (power)** (F07) | `SetLightTrapMode` (`Fireflies.lua:692`): `trap.el_prod_modifier:Change(#trap.fireflies)`. | **Control:** the only two other call sites of the same modifier, `:346` and `:479`, both do `Change(#…fireflies * 1000)`. Three wisps therefore produce 3 internal power units where a Solar Panel produces 2000. **Yes.** |
| **IndependenceTerraforming** (F18) | `TechPreset.lua:4798-4812`: `param1 = 20`, `param1comment = "decrease percent"`, `Effect_ModifyLabel{ Amount = -10, Prop = "SpecialProjectResourcesModifier" }`. | The preset disagrees with itself. **Control:** every other Independence tech has `param1` equal to the magnitude of the effect it drives (`Adaptivity` 5/-5, `MartianbornPerformance` 5/5, `RocketCapacity` 30000/30000, `Research` 20/20). Which side is authoritative is inference, but *that they disagree* is not. **Yes** (data inconsistency; the direction of repair is a judgment). |

### 6.3 Missing guard / missing check

| Fix | Shipped source | Reasoning |
|---|---|---|
| **MilestoneCrash** (F05) | `eval_complete_all_milestones` (`Milestones.lua:87-106`): `if not MilestoneCompleted[id] and not hidden then all_completed = false break end` then `score_sum = score_sum + milestone:GetScore()`. `Milestone:GetScore` (`:23-28`) returns `time and (...)` — nil when uncompleted. | A hidden **and** uncompleted milestone fails the break condition (because `not hidden` is false) and falls straight into `score_sum + nil`. Hidden milestones are guaranteed under NoTerraforming (9 of them) or NoPolitics. Arithmetic on nil is a genuine unwinding error, unlike an assert. **Yes** — a hard error on the last milestone. |
| **TrainPlatformWedge** (F11) | `Colonist:ExitVehicle` (`ColonistTransport.lua:545`): `table.remove(vehicle.units, self)`. | `table.remove(list, pos)` takes an integer; `self` is an object. Raises. The guard exists for the "abducted by CargoTransporter" path, so it fires exactly when something has already gone wrong, and aborts `ExitVehicle` before `DiscardTransportTicket`. **Control:** the codebase uses `table.remove_entry` everywhere else for value removal (`types.lua:143`) — including three lines away in `BoardVehicle` (`:517`). **Yes** (rare path, unambiguous error). |
| **BrokenTrackSalvage** (F45) | `TrackBase:BreakTrackElement` (`Track.lua:618-659`) copies `direction, q, r, station, pillared, connections, track_obj` onto the repair construction site — but not `node_idx`, whose class default is `false` (`TrackElement.lua:164`). Every salvage runs `table.sort(all_elements, function(a,b) return a.node_idx < b.node_idx end)` (`:464`). | `false < number` is a boolean relational compare. The sort raises before anything is deleted, so the salvage click silently does nothing — forever, for that track. **Yes.** *(Sweep 2 upgraded this from inference to certainty, §8.1.)* |
| **SmallLandscapeSites** (F33) | `LandscapeConstructionSiteBase:GetClosestDests` (`:178-192`): `for i = 1, top_count do top_dests[i] = dests[i].dest end`, `top_count` defaulting to 5, with no `#dests` clamp. | The cache is built from periphery hexes only, so a small blob has fewer than five. `dests[i]` is nil and `.dest` on it raises, inside the drone's own command thread. **Yes.** |
| **TrackSalvageWipe** (F44) | `TrackGridElement:DemolishAndSplitTrack` (`TrackElement.lua:448-578`). Two independent problems: the pillared+straight anchor search `repeat first = first + 1 until not all_elements[first] or (…pillared and IsTrackElementStraight(…))` walks off the array on a curve (curves are pillared but `IsTrackElementStraight` (`:52-65`) needs both connection deltas in {0,2}); and both short-remainder branches (`if n - first < 2` and `if last < 2`) call `track_obj:OnDemolish()`. | `TrackBase:OnDemolish` deletes the whole track, and `TrackBase:Done` `DestroySilent`s every assigned train. So salvaging one hex of a curved or short line deletes the line and its trains, instantly and with no countdown. This is the most severe verified finding in the pack. **Yes.** |
| **CaveInsNoDisasters** (F01) | The `MapGameTimeRepeat("UndergroundMarsquake")` body (`Marsquake.lua:306-325`) has no `IsGameRuleActive("NoDisasters")` test. | **Control:** the surface marsquake path checks it (`Marsquake.lua:42`), as do ColdWave, DustStorm and DustDevils. The underground scheduler is the only disaster in the game that doesn't. **Yes.** |
| **AnomalyCaveInMap** — see Tier 3 | | |
| **TrackConnectorPingPong** (F66) | `TrackConnectedObjBase:CreateConnectorElements` (`TrainTransport.lua:114-154`): `if IsValid(el) and (force or el.station ~= self) then assert(not IsValid(el.station) or IsBeingDestructed(el.station)); DoneObject(el); el = nil end`. | The assert **states the invariant** — "the element I am about to destroy has no live owner" — and the code then destroys it regardless. `TrackGridElement:Done` (`TrackElement.lua:193-199`) spawns a game-time thread telling the dying element's still-live owner to rebuild. Two buildings resolving to one hex therefore alternate forever, and whichever is currently element-less fails `GetConnectedTrack`. The assert is the author's own documentation of the missing check. **Yes** — with the caveat that whether two buildings *can* resolve to one hex is spot geometry (§3.3); the code hole is unconditional. |
| **DestroyedTunnels** (F38) | `OnMsg.LoadGame` (`Tunnel.lua:264-266`): `AllMapsForEach("map", "TunnelBase", Tunnel.AddPFTunnel)` with no `destroyed` test. `TunnelBase:AddPFTunnel` (`:197-209`) checks only `IsValid(self.linked_obj)`. | The destruction path is correct (`OnDestroyed` → `RemovePFTunnel`); the load path undoes it unconditionally. A destroyed building is still a valid object (it becomes a ruin), so a ruin re-registers a working pathfinding shortcut. **Yes.** |
| **TrainCargoDumping** (F46) | `Train:UnloadAll` (`Train.lua:783-803`) reads `station.demand[res]:GetTargetAmount()` with no `station:IsResourceEnabled(res)` check. `UniversalStorageDepotBase:SetAcceptResource` (`StorageDepot.lua:641-668`) only removes the request from `task_requests`; the demand object survives with a live target amount, and `storable_resources` is untouched. | So switching a resource off at a station does not stop trains dumping it there. **Control:** both *loading* paths do check `dest:IsResourceEnabled` — the author applied the rule on one side of the trip only. **Yes.** |
| **LayoutTechLock** — see Tier 2 | | |
| **ShuttleHubOffAvailable** (F54) | `IsLRTransportAvailable` (`ShuttleHub.lua:350-359`): `hub.working or hub:GetWorkNotPermittedReason() and not hub:GetWorkNotPossibleReason()`. `BaseBuilding:GetWorkNotPermittedReason` (`BaseBuilding.lua:355-361`) returns `"TurnedOff"` whenever `ui_working` is false. | The second clause is meant to tolerate a hub suspended for a self-lifting reason while physically capable. But the commonest reason it admits is the player's own off switch. Meanwhile nothing dispatches a shuttle from a non-`working` hub, so the colony believes in transport that will never arrive. **Yes.** |

### 6.4 Two code paths that disagree

| Fix | Shipped source | Reasoning |
|---|---|---|
| **AsteroidLanderAvailable** (F72) | Gate: `PlanetaryAsteroidVisitPossible` (`PlanetaryView.lua:433-444`) requires `not arrival_loc` **and** `command == "CmdWaitOrder"` (or `CmdOnEarth`). List: `LandingSiteObject:GetRocketsForExpedition` (`PlanetUI.lua:1623-1635`) requires not-a-supply-pod, `departure_loc == OurColony`, `not arrival_loc`, destination reachable — and never looks at `command`. | Strictly asymmetric: the list is a superset. A lander parked at the colony in `CmdUnload` (which runs indefinitely with no drones) is offered by one and refused by the other, producing "No available Asteroid Landers" while a lander sits on the pad. **Yes.** |
| **DomeFreeSpaceMismatch** (F60) | `GatherFreeLivingSpaces(residences, player_enabled)` (`_GameUtils.lua:475-495`) selects `player_enabled and "ui_working" or "working"`. `Dome:RefreshFreeLivingSpaces` (`Dome.lua:2832-2834`) calls it with **no second argument**. | Every assignment path uses the other member: `ChooseResidence` (`Residence.lua:412`) scores `home.ui_working and home:GetFreeSpace()`, `Colonist:UpdateResidence` rejects on `not home.ui_working`. **Control:** the two functions immediately above `GatherFreeLivingSpaces` in the same file — `GetFreeWorkplacesAround` and `GetFreeWorkplaces` — both tally on `ui_working`. So a power dip makes a dome report itself full to the birth and immigration gates while `ChooseResidence` carries on housing people there. **Yes.** |
| **GraphConsumedCaption** (F19) | Series: `ts_resource.consumed:AddValue(ro:GetConsumedByConsumptionYesterday(r) + ro:GetConsumedByMaintenanceYesterday(r))` (`ResourceTracking.lua:162`). Caption: `consumed = resource_overview_obj:GetConsumedByConsumptionYesterday(id) / const.ResourceScale` (`ColonyControlCenter.lua:184`). | These are separate accumulators (`ResourceOverview.lua:156-163`), not a rounding difference. For Machine Parts / Electronics in a developed colony, maintenance *is* the consumption, so the caption reads near-zero beside a full-height bar. **Yes.** |
| **MoraleComfortTooltip** (F20) | `Colonist:UpdateMorale` (`Colonist.lua:3963-3966`): the high-Comfort morale bonus is commented out with `-- remove for comfort policy to work`; the low-Comfort penalty directly below is live. The Morale tooltip walks `ColonistStatList` uniformly and prints a row whenever `value < low or value >= high`. | The comment settles which side is out of date: the removal was deliberate and its reason is named. The tooltip therefore credits a bonus the game does not apply, and the listed effects don't sum to the Morale shown above them. **Yes** (cosmetic, but the fix's choice of which side to change is well-grounded). |
| **RocketInteractGuard** (F74) | `RCTransport:CanInteractWithObject` (`Units\RCTransport.lua:341`): `if IsKindOfClasses(obj, "TradeRocketBase", "RefugeeRocketBase") then return false end`. `UniversalTradeRocket`/`UniversalRefugeeRocket` are `__parents = { "UniversalRocketBase" }` (generated templates), and `UniversalRocketBase`'s parent list (`UniversalRocket.lua:27-41`) contains no `RocketBase`. | The guard cannot match the classes the Relaunched game actually places. **Control:** five other rocket tests **in the same file** (`:314, :421, :731, :916, :1137`) were updated to name both families; only `:341` was missed. That pattern is a conversion slip, not a rule change. **Yes.** |
| **LastTransmissionStorage** (F75) | `FactionLikeGlobalCondition:Eval` (`ClassDef-Factions.generated.lua:843-849`) reads `self.Condition` and nothing else. The six storage likes in `Data\FactionDef\LastTransmission.lua` put their `ScriptConditionList` on **`Prerequisite`**. Separately, `TLEOxygenStorage2Sols` (`:166-174`) evaluates `GetGridGlobalStorage("Power")`. | With `Condition` unset, `Eval()` returns 0 unconditionally — the like can never contribute however well the colony does, while `EvalApproval` keeps advertising its `HowTo` as an outstanding goal. **Control:** the file contains 7 `Condition` uses and 7 `Prerequisite` uses, and one like sets *both* — so the author knew the difference. And `TLENoOxygenStorage`, the negative twin four lines later, sets `GridType = "Oxygen"` correctly. **Yes** — two independent defects, both source-verified. |

### 6.5 State that is never cleaned up

| Fix | Shipped source | Reasoning |
|---|---|---|
| **GhostFarmOxygen** (F37) | `FarmBase:ApplyOxygenProductionMod` (`Farm.lua:561-571`) registers the crop's oxygen as a negative `air_consumption` modifier on `self.parent_dome`, keyed by `self.farm_id` (assigned once in `Init`, `:80`). `FarmBase` declares no `Done`. | Nothing in `Building:Done` or `Building:SetDome` knows that key, so a salvaged farm leaves the dome permanently breathing phantom oxygen — and a rebuild adds another under a fresh id. **Yes.** |
| **DisasterPredictionLeak** (F81) | `AddDisasterNotification` sets `g_DisastersPredicted[base_id] = true` (`MapSettings.lua:169`); only `RemoveDisasterNotifications` clears it (`:176`). The meteor storm's start adds one (`Meteors.lua:179`); its normal end path (`:242-251`) plays FX, posts `MeteorStormEnded` and clears `g_MeteorStorm` — and never calls the remover. | The notification's own `Expiration` removes the *UI entry* via `RemoveNotification`, which never touches the flag. So the flag sticks true forever, and `IsDisasterPredicted()` (`:189`) then gates rains, dust storms, cold waves, three POI reward sequences and the Inner Light dream cycle. **Control:** every other disaster removes its notifications on every path (ColdWave `:148,:174`; DustStorm `:163,:180`; TerraformingDisasters `:261,:300-302`). The meteor storm is the sole exception. **Yes** — and the largest blast radius in the pack. |
| **StaleReservations** — see Tier 3 | | |
| **DroneTransportMinors (b)** (F57b) | `OnMsg.OnPassabilityChanged` (`Drone.lua:851-864`) rebuilds each drone's `unreachable_buildings` as a plain `{}` and swaps it in. | Two things are lost. (1) The **weak-keys metatable** — every other construction site uses `setmetatable({version=…}, weak_keys_meta)` (`:826`, `:875`), so from the first passability change onward each drone holds a strong reference to every building it failed to reach, keeping salvaged buildings alive. (2) The **count** — `unreachable_buildings_count` is not recomputed, while `ApproachWrapper` compares it against `MaxUnreachablesInTable` and `CleanUnreachables` decrements it (possibly negative). **Yes.** |

### 6.6 Behaviour that repeats when it should not

| Fix | Shipped source | Reasoning |
|---|---|---|
| **RocketDroneChurn** (F50) | `CargoTransporterNew:UpdateCargoResourceRequests` (`CargoTransporterNew.lua:1238-1270`) brackets its whole body with unconditional `DisconnectFromCommandCenters()` / `ConnectToCommandCenters()`. Chain verified: `UniversalRocketBase:HourlyUpdate` (`UniversalRocket.lua:1357-1370`) → `CreateAutoCargoRequest` → `SetCargoRequest` (`:1302`) → `UpdateCargoResourceRequests`. `DroneControl:OnRemoveBuilding` (`DroneControl.lua:720-729`) does `drone:SetCommand("Idle")` for every drone whose `goto_target` resolves to the removed building. | So a landed automatic rocket idles every drone en route to it, once per game hour, forever. Any trip longer than an hour can never complete. Inside the function, the disconnect is only *needed* when a request must be created; the rest of the body calls `SetAmount` on existing objects. **Yes.** |
| **ExtenderFlapChurn** (F77) | `DroneHubExtenderBase:OnSetWorking` (`DroneHubExtender.lua:171-178`) calls `UpdateUplinkRequesters` on every working transition in both directions, and that helper (`:109-112`) is a full `DisconnectTaskRequesters()` + `ConnectTaskRequesters()` on the uplink hub. | Same funnel as F50: the teardown walks the whole hub's requesters and each removal idles drones. One power flicker therefore costs two whole-hub rebuilds. **Yes** (severity scales with hub size; the mechanism is not in doubt). |
| **MeteorFrequency** (F02) | `GlobalGameTimeThread("Meteors")` (`Meteors.lua:277-292`): `local start_time = GameTime(); if GameTime() - start_time > spawn_time - warning_time then Sleep(5000) end` … `local hit_time = Min(spawn_time, warning_time); Sleep(hit_time)`. | The condition compares `GameTime()` against itself — always `0 > spawn - warning`, false in the normal case. So the only real wait is `Min(spawn_time, warning_time)`. Arithmetic checked against the data: `MapSettings-Meteor.lua` sets `spawntime` 1050000-2700000 and `spawntime_random` 750000-1500000 with `const.HourDuration = const.Scale.h`; dividing gives 35-90h + 0-50h. No Meteor preset sets `warning_time`, so `GetDisasterWarningTime` (`MapSettings.lua:94-98`) falls back to `MapSettings.warning_time`, whose declared default is `6 * const.HourDuration` (`:11`). **Meteors therefore strike every ~6 hours instead of every 35-115.** And Sensor Towers, which add warning time, *lengthen* the interval — inverting their own purpose, which is the clincher. **Yes** — arithmetically proven end to end. |
| **RainsDeadlock** (F81b) | `RainsDisasterLoop` (`TerraformingDisasters.lua:310-316`): `Sleep(...)` → `CreateGameTimeThread(RainsDisasterActivation, settings)` → `WaitMsg("RainDisasterEnd")` with **no timeout**. `RainsDisasterActivation` opens `if IsDisasterActive() or IsDisasterPredicted() then return end` (`:277`). | On the collision early-return no rain starts, so `FinishRainProcedure`'s `Msg("RainDisasterEnd")` (`:267`) never comes and the loop blocks permanently. Nothing rescues it: `UpdateRainsThreads` reuses any *valid* activation thread, and a thread blocked in `WaitMsg` is perfectly valid. The collision window is every other disaster's active phase plus every warning window. **Yes.** |
| **FirstAsteroidPrefabs** (F83) | `OnMsg.SpawnedAsteroid` (`Asteroids.lua:411-422`) wraps `WaitPopupNotification("FirstAsteroid", nil, nil, nil, <grants 3 prefabs>)` in a **`CreateRealTimeThread`**. `ShowPopupNotification` (`PopupNotification.lua:245-291`) opens immediately only on an explicit `context.start_minimized == false`; the `FirstAsteroid` preset (`PopupNotificationPreset-Asteroid.lua:31-38`) does not set it, so the popup always arrives as a corner notification. `OnMsg.PersistSave` (`:346-355`) keeps only entries with a `sync_popup_id`. | So the async popup context is dropped from the save while the notification itself persists (a `GameVar`). After a reload the notification is still on screen and still clickable, and answering it posts `Msg(context.async_signal, …)` with nobody listening — the callback, and the three Micro-G extractor prefabs its own `<effect>` line promises, are lost silently and permanently (`show_once`, and the handler only fires at `asteroid_count == 1`). **Yes.** *(Sweep 2 raised this from high confidence to certain, §8.1.)* |
| **TrainMinors (d)** (F49d) | `TrackBase:GameInit` (`Track.lua:62-67`) computes `max_vehicles` from the element count. | A repo-wide grep found exactly three references to `max_vehicles`: the class default (`StationsLink.lua:8`), one read (`:29`), and this single assignment. Nothing recomputes it when salvage shortens or splits a track. **Yes** (minor gameplay weight; the code fact is clean). |

### 6.7 The rocket/lander cluster

| Fix | Shipped source | Reasoning |
|---|---|---|
| **LanderEmptyLaunch** (F67) | `UniversalRocketBase:IsCargoReady` (`UniversalRocket.lua:455-472`) ends `return cargo_status == "ready"`. `GetCargoResourcesStatus` (`CargoTransporterNew.lua:1124-1141`) returns `"ready"` when every entry's amount equals its requested amount — trivially true when the auto request came out empty. `GetLaunchIssue` (`:882-885`) returns `"waiting_cargo"` **without** the blocker flag, so `IsCargoReady`'s early `launch_issue and blocker` guard doesn't stop it either. | Traced the full path: thresholds set but nothing currently over them → empty request → empty hold → `"ready"` → launch. On asteroids the only brake is a 1-hour sleep; on Mars there is none. **Yes.** |
| **LanderReturnFuel** (F69) | `CmdLand` (`UniversalRocket.lua:414`): `self:SetFlightData(self.arrival_loc, self:IsAutoModeEnabled() and self.departure_loc)` — in manual mode the second argument is `false`, clearing `arrival_loc`. `GetFuelResourceRequest` (`:1639-1642`) then short-circuits to 0. `CmdUnload` (`:486-494`) sets `cargo_item.requested = 0` for every entry including fuel. `GetCargoResourcesStatus` special-cases fuel by adding `GetFuelResourceRequest()` — which is now 0. | So fuel in the hold that nobody asked for reads as `"unloading"` and the drones haul the reserved return ration down the ramp. On an asteroid with no fuel production that is permanent. The asteroid flight policy deliberately loads a double ration and reserves half (`FlightPolicyDef.lua:208-211`), which is what makes the loss meaningful. Automatic mode is unaffected. **Yes.** |
| **LanderCargoRatchet — F71 half** | `CreateAutoCargoRequest` (`UniversalRocket.lua:1727-1766`) iterates `sorted_pairs(...)` — alphabetical: Concrete, Electronics, Food, Fuel, MachineParts, Metals, Polymers, PreciousMetals, PreciousMinerals, WasteRock — decrementing a shared `cargo_capacity` as it goes. | The game states the intended priority in every flight policy: `GetAutoModeAllowedResources` returns `{PreciousMinerals, Electronics, PreciousMetals, MachineParts, Polymers, Food, Fuel, Metals, Concrete, WasteRock}` — value-descending, WasteRock last, **identical in all three policies** (`FlightPolicyDef.lua:133-141, 232-241, 390-397`). That is the same function `GetAllowedResources` already calls for this rocket; it only discards the order because it wants a set (`table.invert`). And WasteRock is a legal auto-export from an asteroid, so a lander can fill 80 tonnes with tailings and leave the exotics behind. **Yes.** *(The F68 half of this same file is Tier 5 — see §7.)* |

---

## 7. Findings — Tier 2: Yes, but latent

Verified code defects that no shipped data or shipped call path reaches. Real for
mods, DLC and future updates; invisible in vanilla today. Each fix's own header
already says so, which I note approvingly — this is the pack being honest about
its own scope.

| Fix | Defect | Why it cannot fire today |
|---|---|---|
| **StorageRateModifiers** (F27) | `ElectricityStorage:OnModifiableValueChanged` (`ElectricityStorage.lua:47-63`) and its Water/Air twins fire for `max_*_charge` and `max_*_discharge`, then copy only `charge_efficiency` and `storage_capacity` to the grid element. The rates live on the element as `max_charge`/`max_discharge`, set once at creation, and are what the grid reads every tick. | A grep for assignments to those four properties across `Lua/` and `Data/` found none. No shipped tech or law modifies them. They are declared `modifiable`, which makes this part of the documented modding surface — a fair reason to fix, not a player-facing bug. |
| **SequenceLatents (a)+(b)** (F29) | See §6.1. | (a) is a Mod-Editor sequence action with no shipped user; (b) is unreachable with the shipped `AlienDigger` defaults, which are already in order. |
| **LayoutTechLock** (F43) | `LayoutConstructionController:Activate` (`LayoutConstruction.lua:231-252`) computes `tech_enabled` and consults it only through `require_prefab = not tech_enabled and prefab_item and not prefab_item.locked`, then `add = not require_prefab or (not not self.prefab)`. A building that is tech-locked **and has no resupply item** makes `prefab_item` false → `require_prefab` false → `add = true`. | Exactly one layout ships (`SelfSufficientDome`), and none of its entries carries a tech requirement. Provable no-op on shipped data. The surrounding logic shows the author's rule was "don't hand out a building the player would have to buy"; a building obtainable by no route simply has no branch. |
| **DroneTransportMinors (a)** (F57a) | `DroneControl:UpdateRocketsInternal` (`DroneControl.lua:613-639`) clears `r_t.Fuel` but the `UniversalRocketBase` branch writes `r_t[r.FuelResource]`. | `FuelResource` is a building-template property with **no assignment anywhere in `ModTools\Src`** (grep: the only hit is a comparison in `CargoTransporterNew.lua:1248`). The legacy branch hardcoding `"Fuel"` tells you what the value is. So the two keys coincide on shipped data. |

---

## 8. Findings — Tier 3: Maybe yes

Mechanism verified in source; the harm, frequency or reachability is one
inference beyond what the code shows. I would not defend these as *proven*
without a playtest, but the code half of each is solid.

| Fix | Verified in source | The inference I could not close |
|---|---|---|
| **ArrivalDeaths** (F53) | (a) `Colonist:Arrive` (`Colonist.lua:1284-1290`) does a raw `self:SetPos(pos)` from the rocket's `"Colonistout"` spot with no passability search — while its sibling `CargoTransporterNew:EjectColonists` uses `GetRandomPassableAroundOnMap` for the same job (`:956`). (b) `Arrive` ends `return self:SetCommand("TransportByFoot", dome)` unconditionally, and `ChooseDome` (`_GameUtils.lua:426-441`) defaults `best_dome = safety_dome`, which `GetDomesReachableByColonists` (`:346-423`) picks by raw distance in a branch that runs *before* the `is_walking` test. | Whether arrivals actually land in unwalkable ground, and whether the safety-dome hike actually kills them. Both are plausible; neither is provable from Lua. The asymmetry with `EjectColonists` is a real control for (a). |
| **StaleReservations** (F58) | `Residence:GetFreeSpace` (`Residence.lua:198-200`) subtracts `#self.reserved`. `ReserveResidence`/`CancelResidenceReservation` (`:257-271`, `:353-365`) release only on arrival, death or re-home. No timeout exists anywhere in the family; the one timed lock (`CheckForcedResidence`) is the user-forced kind. | How often reservations actually strand. The fix header notes the devs ship a savegame fixup for this list drifting out of sync, which is decent circumstantial evidence, but I did not read that as proof. |
| **FreedHousingNotice** (F59) | `Residence:CheckHomeForHomeless` is called from `GameInit`, `SetUIWorking` and `SetDome` — all player-initiated — and **not** from `RemoveResident`, which only updates the counter. | This is a latency improvement, not a broken path: the homeless do eventually notice on their own heavy update. Whether that wait is bad enough to call a defect is a judgment. |
| **LakeEntombment** (F30) | `ConstructionSite:ScatterUnitsUnderneath` (`:1722-1741`) explicitly exempts the `RCConstructorBase` that is building the site: `if not u:IsKindOf("RCConstructorBase") or u.command ~= "Construct" or u.construction_clearing ~= self`. So the one rover guaranteed to be standing there is never moved. | The claimed ordering — scatter at `Complete`, *before* `LandscapeLake:GameInit` digs the basin — I did not trace end to end. The exemption itself is unambiguous, and the devs shipping a rovers-only savegame rescue (`BaseRover.lua:736-745`) is suggestive. |
| **AnomalyCaveInMap** (F31) | `TriggerCaveIn` (`CaveInRubble.lua:94-117`) guards `pos` and then calls `map:MapFindNearest` unguarded. Eight scenario `'expression'` strings pass the global `UndergroundMap` rather than the sequence's own map (verified by grep across `Data/Scenario/`), and `UndergroundMap` is a GameVar defaulting to `false`. **Control:** the engine's own callers pass a local `map` or `CurrentMap` (`Marsquake.lua:266`, `:287`). | Whether those scenarios can actually run in a game whose underground map was never generated. If they cannot, the hole is real but unreachable. I could not settle this from source. |
| **TrackTunnelPowerBridge** (F65) | `OnMsg.StationsConnected` (`Track.lua:668-680`) skips `ConnectToGrids()` for `#track.elements <= 2` on the stated premise that "the connected buildings are already adjacent and can connect without the track", and just sets `stations_connected = true`. Track elements carry no power of their own (`TrackBase.ApplyToGrids = empty_func`). | **Whether the premise is false is entity spot geometry — binary data, §3.3.** The fix's response is the right shape given that: it bridges only when the two stations demonstrably sit on different live grids after the shipped handler has run, so if the premise holds it does nothing. But I cannot certify the premise fails. |
| **ShelterReflex (a)** (F73a) | `MicroGHabitatAutoResolve:IsSuitable` (`MicroGHabitat.lua:154-156`) is `self:GetScoreFor(colonist.traits) > 0`, and `Community:GetScoreFor` (`Community.lua:367-393`) contributes its entire 100-point base **only** under `HasLifeSupport()` (`:396-398`). With a default trait filter the remaining terms are 0. | So one tick without power or air makes the habitat score 0 and read "unsuitable". What I did not verify is that losing `IsSuitable` actually *evicts* an existing resident, as opposed to only blocking new assignment. |
| **CrystalMysteryHang** (F06) | `Crystal:ComposeProc` (`Crystals.lua:45-83`): `Msg("CrystalComplete")` → `WaitMsg("CrystalForceFlyAway", const.DayDuration)` → `Msg("CrystalFlyAway")` once. **A repo-wide grep found the string `CrystalForceFlyAway` exactly once in the entire source — at the `WaitMsg` itself. Nothing anywhere emits it.** So the escape hatch the authors left themselves is dead, and the one-sol timeout always fires. | Whether the scenario's Epilogue popup can really hold a player past one sol, which requires reading generated scenario code I did not verify. Leaning strongly yes: an author-provided escape hatch with no emitter is a loose end by definition. |
| **PayloadTemplateRefill** (F70) | `CargoRequestNew:RetrieveRequests` (`CargoRequestNew.lua:179-221`) fills every row whose stored request is 0 from the flight policy's `CargoTemplate`, suppressed only while the transporter is in `CmdLoad` (`resolve_loc_cargo_template`, `:166-177`). And `CmdUnload` zeroes every request on every landing. | The behaviour is exactly as described — a deliberately emptied row is refilled next time the dialog opens. Whether "template as a running correction" is a defect or a convenience is a design judgment. The fix's supporting evidence (the legacy dialog gated the same template on "has not landed yet") is a decent argument, not a proof. |

---

## 9. Findings — Tier 4: Contested

Behaviour verified. The shipped code carries evidence it is **deliberate**.
Calling these defects is a design position, and the pack should own it as one.

### 9.1 DroneUnreachableForever (F55)

**Verified:** `Drone:ApproachWrapper` (`Drone.lua:840`) writes
`unreachable_buildings[building] = GameTime() + max_int`, and
`Drone:CleanUnreachables` (`:879-896`) expires entries on
`now - ts >= const.UnreachablesCleanupDeltaT` (5 sols). A timestamp `max_int` in
the future makes that difference hugely negative, so the entry never expires.
All of that is exactly as the fix describes.

**Why contested:** the shipped line carries its own comment —

> `-- mark it so it is basically unreachable forever, changing the passability version will reset it`

That is an explicit statement of intent, naming the intended reset mechanism
(`g_DroneUnreachablesVersion`), which does exist and does work. Under that
reading the 5-sol expiry in `CleanUnreachables` is vestigial *by design*, not by
accident — a leftover from an earlier scheme, kept alive because the version
reset superseded it.

The fix's gameplay argument (a dome briefly unreachable is written off
permanently by that drone) may well be right, and the repair is minimal and
one-way. But **"the developers forgot" is not the reading the source supports.**
This is a balance change wearing a bug fix's clothes, and it should be labelled
that way.

### 9.2 DustSicknessBiorobots (F40)

**Verified:** the three storybits that grant the trait
(`DustSickness.lua`, `DustSickness_GeneratSick.lua`,
`DustSickness_GeneratSickNotWorking.lua`) each use a `ForEachExecuteEffects` over
the `Colonist` label whose only filter is `HasTrait{Trait="Child", Negate=true}`.
Androids are ordinary Colonists in that label, so they are eligible.

**Why contested:** there is no code error here. The filter does what it says. The
claim is that Biorobots *ought* to be excluded — which is an argument from
theme ("a robot shouldn't catch a dust sickness"), not from the code. There is no
sibling control showing the author excluded androids elsewhere from this family.
A reasonable designer could have made either call. **Real behaviour, design
judgment.**

### 9.3 ShelterReflex half (b) (F73b)

**Verified:** `Colonist:Idle` (`Colonist.lua:1770+`) has branches for hunger,
medical care, panic and darkness, and **no branch for the oxygen timer**.
Suffocation is applied purely as damage.

**Why contested:** this is an *absence*, not a mistake. Nothing computes a
shelter decision and discards it; nothing states an invariant it then violates.
Half (b) adds a behaviour vanilla never had. That may be a good idea — colonists
bleeding out next to a habitat they could walk into is poor play — but it is a
**feature, not a repair**, and this audit's answer for "is the fix needed to
correct a defect" is **leaning no**.

---

## 10. Findings — Tier 5: I don't know

Both of these turn on an engine C export with no Lua body. Neither is gradeable
from source, in either direction. Recording them as unknown rather than guessing.

### 10.1 LanderCargoRatchet — the F68 half

**The claim:** `CreateAutoCargoRequest` is re-run hourly and recomputes the whole
request from `GetTotalCargoAvailable(target_city, "Resource", res) - threshold`.
Resources already loaded into the rocket are no longer "available" in the city,
so the request shrinks by exactly what the drones just loaded; once `requested`
drops below what is aboard, `GetCargoResourcesStatus` reports `"unloading"` and
the drones carry it straight back out.

**What I verified:** the function body is exactly as quoted
(`UniversalRocket.lua:1727-1766`); it is re-run hourly (`HourlyUpdate`); and
`GetCargoResourcesStatus` does flip to `"unloading"` when `amount > requested`.

**Where it stops.** The entire defect hinges on **whether
`GetTotalCargoAvailable` counts the landed rocket's own hold.** That resolves as
`GetTotalCargoAvailable` (`Cargo.lua:72`) → `GetCityResourceOverview(city)` →
`ResourceOverview:GetAvailable` (`:144`) → `self.data[resource_type]`, and
`self.data` is filled by **`GatherResourceOverviewData`** — a C export, called
via `pcall` at `ResourceOverview.lua:10` and `:33`, with **no Lua definition
anywhere in `ModTools\Src`**. The doc-comment on `GetAvailable` says "stockpiles
+ carried by drones + carried by rovers + carried by shuttles" and does not
mention rockets, which is weak evidence *for* the defect.

I worked the arithmetic both ways:

* **If the hold is NOT counted:** ground `G`, threshold `T`, request starts at
  `G-T`. After loading `x`, request is `G-x-T` while aboard is `x`. The flip to
  `"unloading"` happens at `x > (G-T)/2` — i.e. every automatic export would
  reverse itself around half load. Severe and constant.
* **If the hold IS counted:** available stays `G` as resources move from ground
  to hold, the request never shrinks, and the ratchet **cannot happen at all**.

**And the fix file's own repair note says the second one is true** — a 2026-07-28
entry records live forensics showing the observed request tracked
`ground + 2×aboard − threshold` exactly, which is only consistent with
`available` already including the hold (v1 of the fix added it a second time and
over-exported). That note was written by this project, not by me, and I could not
independently confirm it — but it is the only evidence either way, and it points
away from the defect.

**Verdict: I don't know**, leaning toward "the F68 half is a belt-and-braces
guard for a state the engine may never produce." The **F71 ordering half of the
same file is separately and definitely needed** (§6.7).

### 10.2 MeteorStormWedge (F78)

**The claim:** the storm's drain loop (`Meteors.lua:238-241`)

```lua
while not g_MeteorStormStop and #spawned > 0 do
    WaitMsg("MeteorDone", delta)
    table.validate(spawned)
end
```

is unbounded, and in a live repro 73 spawned descriptors drained to 2 which never
became invalid, so the loop spun forever and held the storm scheduler.

**What I verified:** the loop is exactly as quoted and has no timeout or
iteration cap. `MeteorsDisaster` is called inline from the `"MeteorStorm"` global
thread, so a wedge there really does block all future storms. `g_MeteorStorm` and
`g_MeteorStormStop` are GameVars and the scheduler is a persisted named global,
so a wedge would follow the save.

**Where it stops.** `table.validate(t, filter, ...)` removes entries failing
`IsValid` (`LuaExportedDocs/Global/table.lua:307`). But `spawned` holds **plain
Lua tables** — `SpawnMeteor` (`Meteors.lua:91-110`) returns
`{ meteor = …, start = …, pause = 0 }`, and `table.insert(spawned, meteor)` at
`:194` inserts that descriptor, not a game object. `IsValid` is a C export
documented as "returns if the given param is a valid object". So:

* if `IsValid(<plain table>)` is **false**, `table.validate` empties `spawned` on
  the very first pass and the loop exits after one `WaitMsg` — **it cannot
  wedge**, and the post-loop `DoneObject(descr.meteor)` cleanup would also never
  run (which would be its own bug);
* if it is **true**, `spawned` never shrinks and the loop wedges **every single
  time**, not occasionally.

Neither reading produces "73 drained to 2". Something about how descriptors leave
that array is not visible to me, and it is exactly the thing that decides whether
the fix is needed.

**Verdict: I don't know.** The loop is genuinely unbounded as written, which is a
fair thing to defend against; whether it actually wedges is not readable from
Lua.

---

## 11. Sweep 2 — what changed after reading ENGINE_FACTS.md

Sweep 1 verdicts were fixed before this pass. **No verdict changed direction.**
Five moved in confidence, two stayed stuck, and the doc itself has one stale
entry.

### 11.1 Confidence upgrades

| Fix | Sweep 1 | Sweep 2 | Engine fact that closed the gap |
|---|---|---|---|
| **BrokenTrackSalvage**, **TrackSalvageWipe** | Yes — I *inferred* that `false < number` raises | **Yes, certain** | *"Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` … but NOT boolean relational compares."* That is precisely the `node_idx` sort. My inference was load-bearing and is now a recorded, project-proven fact. |
| **LowStorageWarning** | Yes — I *derived* that `/` truncates from the guard being unsatisfiable | **Yes, certain** | *"`/` truncates (integer division); that is what makes F12's `a*24/v*24` unsatisfiable."* Independent arrival at the same conclusion, which is the best kind of agreement. |
| **FirstAsteroidPrefabs** | Yes (high confidence) | **Yes, certain** | Two facts: *"GAME-TIME THREADS PERSIST BY DEFAULT — real-time threads do not"*, and *"every shipped popup is ASYNC … `PersistSave` always saves an EMPTY popup queue."* The doc also records that the F83 investigation once assumed the opposite and **retracted a fix recommendation on it** — a useful warning that this one is easy to get backwards. |
| **WispRewards (RP half)** | Yes | **Yes, certain** | *"A post-wrapper on a command method never runs — `DoSetCommand` kills the calling thread."* This confirms the second RP grant at `Fireflies.lua:466-469` (written after `SetCommand("Die")`) is unreachable, which is why the destructor at `:542` is the sole payer and the batch grant at `:690` is genuinely a double. |
| **all 66** | read against `ModTools\Src` | **materially strengthened** | *"PARITY PROVEN 2026-07-29: the shipped build IS Src"* — the full `Lua.fpk` was extracted and diffed, 2,250 of 2,256 files byte-identical, the 5 divergences engine/tooling only, build stamp `1.0.7.396349`. This retires my single largest blanket worry: that I audited source the game does not run. |

### 11.2 Still unresolved after sweep 2

`LanderCargoRatchet` (F68 half) and `MeteorStormWedge` stay **I don't know**.
`ENGINE_FACTS.md` confirms the general hazard — it names
`GatherTransportableResources` as *"a genuine engine C export"* defined in
neither Src nor the shipped Lua — but says nothing about
`GatherResourceOverviewData`, `IsValid` on a plain table, or `table.validate`.
Both pivots remain closed.

The three Tier-4 contested verdicts are also unchanged: nothing in
`ENGINE_FACTS.md` addresses designer intent, which is what they turn on.

### 11.3 A stale entry found in ENGINE_FACTS.md

The doc warns (≈ line 300):

> ⚠️ The disproven by-name persistence belief still sits in TWO shipped file
> headers — `Fix_MeteorFrequency.lua:53` and `Fix_RainsDeadlock.lua:52` (named
> here 2026-08-01 so nobody inherits them as facts).

I read both files in sweep 1. **Neither header carries that claim any more.**
Both were rewritten by the F86 Tier-1 pass — `Fix_MeteorFrequency`'s header now
describes a synchronous `GetDisasterWarningTime` wrapper with no mod-owned thread
body, and `Fix_RainsDeadlock`'s states outright that `fixed_loop` and the
`RainsDisasterLoop` replacement are **deleted**. The warning has outlived its
subject.

Worth flagging because it is the same failure mode the document flags against
itself twice elsewhere (*"an earlier 'queued' note here had gone stale"*,
*"an earlier 'repair in progress' note here had outlived its resolution"*). A
doc that corrects itself three times in one file is a doc that needs a review
cadence, not more corrections.

---

## 12. Shortlists

**Verified, load-bearing, defensible anywhere.** If the pack ever has to justify
itself in one screen, use these:

`MeteorFrequency` · `DisasterPredictionLeak` · `RainsDeadlock` ·
`TrackSalvageWipe` · `TrainsToVoid` · `LowStorageWarning` · `GridGlobalStorage` ·
`MilestoneCrash` · `UpgradeModifierLeak` · `LastTransmissionStorage` ·
`RocketDroneChurn` · `ShuttleTransportCache` · `VacuumWalks` ·
`FirstAsteroidPrefabs` · `BrokenTrackSalvage` · `TouristApplicants` ·
`FounderTraitNotification` · `GeneForging`

**Worth re-labelling before defending them as bug fixes** (facts fine, framing
contestable):

`DroneUnreachableForever` (vanilla comment says the forever-mark is intended) ·
`ShelterReflex` half (b) (adds a branch vanilla never had) ·
`DustSicknessBiorobots` (design judgment, not a code error) ·
`PayloadTemplateRefill` (template-as-default is arguably designed)

**Worth an evidence check before shipping as a fix:**

`LanderCargoRatchet` F68 half — the file's own forensic note suggests it guards a
state the engine may not produce. The F71 half is unaffected and should stay
either way.

---

## Closing thoughts

**The pack's hit rate is high, and the misses are honest ones.** Fifty of
sixty-six modules repair a defect I could point at in the shipped source and
explain in one sentence. Another three are real code defects that happen to be
unreachable on shipped data, and every one of those says so in its own header
before I got there. That is a better ratio than I expected going in blind, and
the failure modes are not "invented a bug" — they are "graded a design choice as
a defect" (three cases) and "could not see the engine" (two cases).

**The strongest findings share a shape, and it is worth naming.** The most
defensible entries here are all cases where the shipped code *computes something
and then does not use it*: `change` in Dust Sickness, `spawn_dir` in
Bombardment, `tv` in the Domes Overview, `filter_embark` in Landscaping, `count`
in the sequence action, the whole `upgrade_modifiers` walk. In each, the discarded
value is its own witness — nobody writes `local change = 5 + Random(param)` for
fun. Where the pack reaches for a subtler argument (intent, balance, "the
player would expect"), the verdicts get softer fast. That correlation is the most
useful thing in this report: **the evidence tier tracks the argument type almost
perfectly.**

**Two verdicts are stuck behind the same wall, and it is not going to move.**
`GatherResourceOverviewData` and `IsValid` are C. No amount of further reading
will grade F68's ratchet or F78's drain loop. If either matters, the answer costs
one instrumented playtest each and nothing less will do — which is presumably why
this project runs playtests at all. I would not spend more static-analysis time
on them.

**On the three contested verdicts.** I want to be precise about what I am and am
not saying. `DroneUnreachableForever`, `DustSicknessBiorobots` and
`ShelterReflex` half (b) are not wrong, and I am not recommending their removal.
Each may well improve the game. What I am saying is that the shipped code
contains no error in those three places — one of them contains an explicit
comment stating the current behaviour is intended — and a pack that calls itself
a *fix* pack pays a credibility cost for every entry where a reader can go look
and find working code. Relabelling costs nothing. Being caught costs more than
the feature is worth.

**On the anchoring risk, honestly.** The fix headers made this audit fast and
they made it comfortable, and those are not the same virtue. Every claim I could
check, checked out — including several where the header pre-emptively corrected
its own earlier version, which is a good sign about the process behind them. But
I found the three contested verdicts by asking a question the headers do not ask
themselves: *not "is this claim true" but "would a designer have written this on
purpose".* That question is not expensive and it is not in the current
methodology. It would be worth adding.

**And one structural note.** `ENGINE_FACTS.md` corrects itself three times in one
file and carries a fourth correction that is itself now stale (§11.3). That is
not a criticism of the corrections — self-correcting on primary evidence is
exactly right, and the withdrawn "PROVEN DIVERGENT" entry is a model of it. It is
an observation that the document has outgrown append-only maintenance. A doc
whose whole purpose is "do not re-derive these" fails at the margin the moment a
reader cannot tell which entries are current, and the warning I found stale
today was written yesterday.

---

*Audit performed 2026-08-02 against game build `1.0.7.396349`. Sweep 1 read no
project documentation. Sweep 2 read `docs/agent/ENGINE_FACTS.md` only. No game
code and no fix code was modified. This audit graded defect premises, not
repairs — patch correctness, install correctness and save safety were explicitly
out of scope.*

---

# ANNEX — the informed examination (chain prompt 12, job 6b, 2026-08-03)

**Appended by the chain-12 QA session — the only prompt authorised to open this
document. The body above is a record of an independent exam and has not been
edited.** This annex grades the audit's verdicts against the evidence base it
was forbidden to see: the witness grades in `BUG_LIST_AUDIT.md` §2/§9/§10, the
reachability enumerations, and the play-proven results. Every judgment below was
re-derived from primary sources this session (Src reads, log files, witness
rows), not inherited.

## 0. Independence caveats — read first

1. **The "sealed key" was ingested before this exam ran.** The 2026-08-02
   informed review's findings were embedded in chain prompt 12's own brief
   (inside a `<details>` block), so they entered this session's context the
   moment the brief was read. The exam below was still performed against primary
   evidence — every verdict cites the Src line, log, or witness row it rests
   on, and one of the key's claims is **rejected** below on that evidence — but
   the comparison cannot be called unanchored, and pretending otherwise would
   be the exact failure this project stamps out.
2. **The seal held, with two recorded exceptions, both scoped.** (a) Prompt 8b
   recorded a `git add -A` staging slip, amended out before any push — a
   staging pattern, not a read. (b) Prompt 7's brief carried a deliberate,
   targeted disclosure: a section quoting this audit's §7 F29(a) grading, as an
   inheritance guard for package 0, authored by the informed-review session.
   That disclosure was *defensive* (it warned prompt 7 **against** inheriting
   the audit's provenance reasoning) and left the merit review to this job —
   but it means prompt 7's F29 record was not blind to this audit's F29
   verdict. Prompts 8c and 11 recorded clean seals; no prompt's handoff admits
   a broad-search surfacing.
3. **Scope drift, benign:** the audit covers the 66 `Fix_*` modules as of
   2026-08-02 morning. The seven fix modules built later that day (F90–F97 era)
   and `Opt_NoHomeless` are outside its scope by construction.

## 1. Verdict-by-verdict, where the audit disagrees with or qualifies the record

| audit verdict | informed-exam result | evidence |
|---|---|---|
| **F29(a) "a Mod-Editor sequence action with no shipped user" (§7)** | **REASON OVERTURNED, CONCLUSION CONFIRMED.** There are exactly **four shipped users**, all in Mystery 2 — re-verified this session at `Data\Scenario\Mystery 2.lua:235, :252, :280, :284`. The latency conclusion still holds: all four pass only `label`/`register` and never the truncating `random_percent`/`random_count` params, so the defect cannot fire on shipped data (R3 latent-by-data, exactly as the F29 entry records). The audit's own §3.5 anchoring warning predicted this failure shape. |
| **F55 Contested (§9.1)** | **CONFIRMED AS A GENUINE FINDING — the strongest in the report.** The vanilla intent comment (`Drone.lua:840`) is real (re-read this session) and the BUGS entry never weighed it (the module header cites it without treating it as an intent tell). Counterweights the audit could not see: the GOLD Relaunched witness (gjscott1996 [S8]); the named recovery (passability-version reset) being ineffective for exactly the witnessed harm (re-fail, re-mark forever); and the shipped 5-sol expiry being equally shipped code — *which* of the two shipped mechanisms is vestigial is the genuine ambiguity, and the audit stated only one side of it. The entry now carries both tells; the mod-page label goes to the owner. |
| **F40 Contested (§9.2)** | **CONFIRMED IN CORE, QUALIFIED.** The grant filters contain no code error, and the "no sibling control" claim verifies (only `NutsAndBolts.lua` filters on `Android`, positively). What the audit could not see: ChoGGi's years-shipped Relaunched fix for exactly this ([S29], SILVER) and the fix's save-heal half. One informed-review claim is **REJECTED on evidence**: the 2026-08-02 key asserted the harm is "androids-never-cured" via an unenumerated cure path — enumerated this session, `DustSickness_CureFound.lua` fires on `TechResearchedTrigger`/`DustSicknessCure` and removes the trait from **every** carrier, androids included. "Never cured" is not supported by shipped data; ChoGGi's "doesn't always cure" remains an unlocated observation. Entry annotated; label to the owner. |
| **F73(b) Contested (§9.3)** | **CODE FACT CONFIRMED, INTENT INFERENCE UNDERCUT.** Half (b) is an added behavior — the audit's code reading is right. But "deliberate absence" is itself an inference, and the witness evidence cuts against it: a **developer replied in the GOLD witness thread** (schrolock [S16]) and the official notes fixed a sibling in the same family (starving at stocked Naturalist Habitats [S5]). Entry annotated; label to the owner. |
| **F68 "I don't know, leaning belt-and-braces" (§10.1)** | **METHODOLOGICALLY RIGHT, AND ITS TENSION-SPOT IS A REAL FINDING.** The F68 entry's lead mechanism paragraph ("loaded cargo is NOT available") contradicted the fix file's own 2026-07-28 forensics (`ground + 2×aboard − threshold`, i.e. the hold IS counted) and had stood unreconciled since — now annotated. What the audit could not see: the GOLD witness set is **hotfix-1.0.3-era** and the official notes record a dev-side lander-churn fix, so the reconciled story is build-vintage — churn real then; the trigger state possibly retired on 1.0.7; the post-hoc floor is the load-bearing half and is PT-17-verified. The fix and its witnesses stand. |
| **F78 "I don't know" (§10.2)** | **QUALIFIED BY PLAY EVIDENCE.** The static puzzle (how `spawned` drains under `table.validate`) is genuinely open. But "whether it actually wedges" has an observed answer: the 73→2 drain the audit quotes is this project's own live capture, and both heal branches ran live 2026-08-01 (Tier-1 legs; F78 `tested`). The "one instrumented playtest" the audit prescribed was already done. |
| **§11.3 stale ENGINE_FACTS warning** | **CONFIRMED.** The two-headers warning was struck in `ENGINE_FACTS.md` on 2026-08-02, explicitly citing this audit. |
| **§12 shortlists; the closing "would a designer have written this on purpose" question** | **ENDORSED.** The intent-first question independently reinvents the FIX_POLICY §4 amendment's bar (adopted 2026-08-01) — convergent validation of the adopted policy by a session that had never read it. |

**Also verified in passing:** the tally arithmetic is internally consistent;
the two Tier-5 pivots remain genuinely closed from Lua; the §11.1 parity
concern was retired by the recorded fpk diff exactly as stated.

## 2. Entry-record updates made (chain-12 QA, same commit)

- **F55**: intent-tell block added — both tells now on the entry; label question routed to the owner.
- **F40**: framing note added — no code error in the filters; ChoGGi witness; cure-path caution against over-claiming; label question routed.
- **F73**: framing note on half (b) — added behavior; dev-reply and patch-note counterweights; label question routed.
- **F68**: lead paragraph reconciled with its own forensics; build-vintage story stated.
- The **mod-page relabel question (F55 / F40 / F73b / F70)** is packaged as an owner decision in `CHAIN_QA_REPORT.md`, with this session's recommendation.

## 3. The two structural observations, handed to job 7 as taxonomy evidence

1. **§11.3 + closing**: `ENGINE_FACTS.md` corrects itself repeatedly in one
   file, and a correction written one day went stale the next. The diagnosis —
   a doc that has outgrown append-only maintenance and needs a review cadence
   rather than more corrections — is adopted as direct evidence in
   `DOC_STRUCTURE_REVIEW.md`.
2. **Closing**: "the evidence tier tracks the argument type almost perfectly" —
   discarded-value defects grade hard, intent/balance arguments grade soft. A
   portable reviewing heuristic, fed to job 7's recommendations (a one-line
   intent-tell field per entry would have prevented the F55 omission this annex
   corrects).

*Annex written 2026-08-03. The seal (chain README rule 8) dissolves with this
chain; this document is committed to the repository alongside the annex so the
record survives file rotation.*
