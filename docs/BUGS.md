# Bug Tracker — Surviving Mars: Relaunched Community Fix Pack

Canonical record of every defect found in the game's shipped Lua source
(`<game>\ModTools\Src`), its evidence, and its fix status. **Update this file in
the same change that adds or edits a fix.** All line numbers refer to the
shipped source tree; the game executes `Packs\Lua.fpk` (dated slightly newer),
so each fix must spot-verify its target function wasn't hotfixed (see
`WORKFLOW.md` → "fpk verification").

Statuses: `todo` → `fixed` (code written) → `tested` (verified in-game) | `wontfix` | `blocked`.

## Index

| ID  | Title                                                    | Sev | Conf | Status |
|-----|----------------------------------------------------------|-----|------|--------|
| F01 | Cave-ins ignore "No Disasters" rule                      | P1  | high | fixed  |
| F02 | Meteors strike ~every 6h instead of 35–115h              | P1  | high | todo   |
| F03 | Upgrade buffs leak & stack after salvage/demolish        | P1  | high | todo   |
| F04 | Night-shift workers never return to work after midnight  | P1  | high | todo   |
| F05 | Milestone completion crashes (NoTerraforming/NoPolitics) | P1  | high | todo   |
| F06 | Philosopher's Stone mystery can hang forever             | P1  | med+ | todo   |
| F07 | St. Elmo's Fire "free wisps" gives ~1/1000 power         | P1  | high | todo   |
| F08 | Tourist star-rating applicant bonus inverted             | P1  | high | todo   |
| F09 | Tourist Satisfaction drifts down (asymmetric thresholds) | P1  | high | todo   |
| F10 | Faction funding conditions always error (BlueSun/Brazil/Russia) | P1 | high | todo |
| F11 | Train wedges at platform (`table.remove` misuse)         | P1  | high | todo   |
| F12 | "Low Storage" warning never fires for Food/maintenance   | P2  | high | todo   |
| F13 | Command Center resource rows show no numbers             | P2  | high | todo   |
| F14 | Domes Overview red low-stat highlight dead               | P2  | high | todo   |
| F15 | Mystery 11 wisp RP rewards double/silent                 | P2  | high | todo   |
| F16 | Mirror Sphere site usable after completion               | P2  | med  | todo   |
| F17 | Dust Sickness damage not randomized                      | P2  | med+ | todo   |
| F18 | Independence terraforming tech gives 10% not 20%         | P2  | med  | todo   |
| F19 | Graphs "Consumed" caption omits maintenance              | P2  | med+ | todo   |
| F20 | Morale tooltip shows unapplied +Comfort bonus            | P2  | high | todo   |
| F21 | Train travel-time penalty includes station waiting       | P2  | med  | todo   |
| F22 | `GetGridGlobalStorage` breaks Last Transmission gates    | P2  | med  | todo   |
| F23 | Founder-gains-trait notification never fires             | P3  | high | todo   |
| F24 | Dome pipe visuals corrupt on load (`MoveInside` typo)    | P3  | med  | todo   |
| F25 | Tech description names wrong building (pre-1.0.6 saves)  | P3  | high | todo   |
| F26 | Bombardment missiles fly parallel (cosmetic)             | P3  | med  | todo   |
| F27 | Storage charge/discharge rate modifiers ignored (latent) | P3  | med  | todo   |
| F28 | `Research:ReplaceTech` crashes (latent, mod-facing)      | P3  | high | todo   |
| F29 | SA/sequence latents: label filter, workshift wait, Diggers swap | P3 | high | todo |
| F30 | Lake placement entombs RC builder + drones               | P1  | high | todo   |
| F31 | Anomaly cave-in hardcodes UndergroundMap (cross-map)     | P2  | med  | todo   |
| F32 | Dismissed warnings re-add instantly (not suppressable)   | P2  | med  | todo   |
| F33 | Drone crash on small landscaping sites (nil-index)       | P2  | high | todo   |
| F34 | Landscape nil-guard bundle (latent crash paths)          | P3  | med  | todo   |
| F35 | Large Wind Turbine buff lost in old saves (fixup bug)    | P2  | high | todo   |
| F36 | Universities overtrain geologists (unmanned extractors)  | P2  | high | todo   |
| F37 | Ghost farm oxygen modifier survives salvage/demolish     | P1  | high | todo   |
| F38 | Destroyed tunnels rejoin pathfinding after save/load     | P2  | high | todo   |
| F39 | Second Artificial Sun ignored by solar panels            | P2  | high | todo   |
| F40 | Dust Sickness infects Biorobots (androids)               | P2  | high | todo   |
| F41 | Gene Forging tech has no effect                          | P2  | high | todo   |
| F42 | Buildings placeable on active dust devils                | P3  | high | todo   |
| F43 | Layout construction bypasses tech locks                  | P3  | high | todo   |
| C01 | `BreakthroughOrder` reshuffled on every map load         | ?   | cand | investigate |
| C02 | Cave-ins reported on asteroids — no Src code path found  | ?   | cand | runtime-check |

Severity: P1 = gameplay-breaking/major loss, P2 = wrong numbers or notable misbehavior, P3 = cosmetic/latent/mod-facing.

---

## P1 — gameplay-breaking

### F01 — Cave-ins ignore "No Disasters" rule  `[fixed: Code/Fix_CaveInsNoDisasters.lua]`
`Lua\Marsquake.lua:306-325` — `MapGameTimeRepeat("UndergroundMarsquake", ...)` has no
`IsGameRuleActive("NoDisasters")` check; every other disaster has one (ColdWave.lua:222,
DustStorm.lua:413, DustDevils.lua:189, surface quake Marsquake.lua:43). Matches live
Paradox-forum report. **Fix:** wrap FUNC slot (index 3) of `PeriodicRepeatInfo["UndergroundMarsquake"]`.

### F02 — Meteors strike ~every 6h instead of 35–115h
`Lua\Meteors.lua:277-292` — the long wait `spawn_time - warning_time` was mangled into a
dead `if` (`GameTime() - start_time > ...` evaluated immediately after `start_time = GameTime()`,
always false); only remaining wait is `Sleep(Min(spawn_time, warning_time))` where
warning_time defaults to 6 game-hours (MapSettings.lua:11,94-98). Designed intervals:
35–90h + 0–25h random (`Data\MapSettings-Meteor.lua`). Sensor Towers (+12h warning each,
`_GameConst.lua:125-126`) *lengthen* intervals — inverted role. Correct two-phase pattern
survives in `DustDevils.lua:168-173` and the MeteorStorm thread (`Meteors.lua:322-342`).
**Fix:** re-register `GlobalGameTimeThread("Meteors", ...)` with repaired wait
(`while GameTime() - start_time < spawn_time - warning_time do Sleep(5000) end`).
Check how `GlobalGameTimeThread` re-registration behaves; may need thread deletion + respawn on load.

### F03 — Upgrade buffs leak & stack after salvage/demolish
`Lua\Buildings\Building.lua:1268-1274` — `StopUpgradeModifiers` iterates `upgrade_modifiers`
with `ipairs`, but the table is string-keyed (`ApplyUpgrade`, lines 1168-1170) → `TurnOff()`
never runs. Self-targeted modifiers die with the building; **LabelModifiers on other
containers leak permanently and stack on rebuild**: MedicalCenter/HospitalCCP1 "Holographic
Scanner" (+30 birth comfort on parent_dome), AncientArtifactInterface "Full System
Integration" (+1 colony-wide DroneResourceCarryAmount). Call sites: `Building:Done` (:510),
`Building:SetDome` (:675). No other cleanup path exists (`LabelModifier:TurnOff`,
Modifiers.lua:277, is the only remover). **Fix:** replace `Building.StopUpgradeModifiers`
with corrected iteration (`pairs` outer, `ipairs` inner, honoring `only_for_object`).
Consider optional one-shot savegame sweep for already-leaked modifiers (id pattern
`"%d+_upgrade%d_mod_%d"` with no live building).

### F04 — Night-shift workers never return to work after midnight
`Lua\Units\Colonist.lua:1758-1768` — `ShouldLeaveForWork` window for shift 3
(`DefaultWorkshifts = {{6,14},{14,22},{22,6}}`, `_GameConst.lua:370`) evaluates as
`hour >= 21 and hour <= 25`; hours 0-1 unreachable (hour is 0-23, no wrap). Shift-1/2 get a
5-hour catch-up window; shift-3 colonists idle after midnight skip the rest of their shift.
Only gate that sends colonists to work (`Colonist:Idle` :1911). **Fix:** override
`Colonist.ShouldLeaveForWork` using modular distance `(hour - start) % 24`, incl. the
`leave_early_for_work` branch.

### F05 — Milestone completion crashes (NoTerraforming/NoPolitics)
`Lua\Milestones.lua:87-100` — hidden-but-uncompleted milestones fall through to
`score_sum + milestone:GetScore()`; `GetScore()` returns nil when uncompleted (:23-28) →
arithmetic-on-nil inside `CompleteMilestone`. Hidden milestones are guaranteed under
NoTerraforming (9 milestones) / NoPolitics (Independence), so completing the last visible
milestone errors and the "AllMilestonesCompleted" popup is lost. **Fix:** the eval fn is a
local — override global `CompleteMilestone` with a copy using `(milestone:GetScore() or 0)`.

### F06 — Philosopher's Stone mystery can hang forever
`Lua\Mysteries\Crystals.lua:67-70` — composed crystal emits `Msg("CrystalFlyAway")` exactly
once (1 sol after completion; the `CrystalForceFlyAway` escape hatch has **no emitter
anywhere** in Src). Scenario (`Lua\Scenario\Mystery 10.generated.lua:232,243,271`) first
blocks on a player-gated minimized Epilogue popup; if unopened > 1 sol the one-shot message
is missed → mystery never completes, `Msg("MysteryEnd")` never fires. **Fix:**
`OnMsg.CrystalFlyAway` sets a persistent flag + game-time thread re-broadcasting until the
mystery ends, so late listeners catch it.

### F07 — St. Elmo's Fire "free wisps" gives ~1/1000 power
`Lua\Mysteries\Fireflies.lua:692` — `trap.el_prod_modifier:Change(#trap.fireflies)` missing
`* 1000`; sibling paths :346 and :479 have it. `ObjectModifier:Change` sets absolutely
(Modifiers.lua:321-331), so the broken value persists until wisp count changes (typically
next 4 AM). **Fix:** override `SetLightTrapMode`; in "free" branch multiply by 1000.

### F08 — Tourist star-rating applicant bonus inverted
`Lua\HolidayRating.lua:77` — `if Random(0,100) > bonus_chance` grants the bonus with
probability ~(100 − chance); rewards table (:2-11) is plainly a monotonic progression.
As shipped, 2-star tourists yield fewer applicants than 1-star. Codebase idiom elsewhere:
`Random(100) >= chance then return` (MonumentOfMarsLiberty.lua:21, ToxicPool.lua:182).
Called from RocketBase.lua:818, UniversalRocket.lua:2014. **Fix:** override
`HolidayRating.RewardApplicants`, flip to `<`.

### F09 — Tourist Satisfaction drifts down (asymmetric threshold crossings)
`Lua\Units\Colonist.lua:4014-4031` (`UpdateSatisfaction`) — down-crossings cumulative,
up-crossings exclusive (`+low` requires `new_value < high`; `+high` requires `< 100`).
Two-tier jumps are routine (service visits set Comfort directly; StressedOut recovery +50
Sanity, StatusEffects.lua:264) → satisfaction is path-dependent, drifts down, lowers
payouts. Visible as 2 red rows down / 1 green row up in the satisfaction log. **Fix:**
replace `Colonist.UpdateSatisfaction` (self-contained) with symmetric tier-based version
(tiers: <low / [low,high) / [high,100) / 100; apply signed sum of awards between tiers).

### F10 — Faction funding conditions always error
`Lua\Funding.lua:104-117` (`GetLastSolsFundingByType`) — `pairs(funding_gain_last_hours[hour])`
where the per-hour table only exists for hours with positive gain (`ChangeFunding` :52-65)
→ `pairs(nil)` error for most hours. Breaks `Data\FactionDef\BlueSun.lua:34,54`,
`Brazil.lua:42`, `Russia.lua:84` (export/tourism income gates never evaluate true).
**Fix:** redefine `Funding.GetLastSolsFundingByType` with `or empty_table` guards.

### F11 — Train wedges at platform (`table.remove` misuse)
`Lua\Units\ColonistTransport.lua:541-547` (`ExitVehicle` stale-passenger guard) —
`table.remove(vehicle.units, self)` needs an integer pos; intended API is
`table.remove_entry`. When the guard fires (dev comment: CargoTransporter abduction),
the error aborts before `DiscardTransportTicket`; `Train:UnloadTrain`
(`Units\Train.lua:443-453`) then spins forever → train permanently blocks platform.
**Fix:** replace `Colonist.ExitVehicle` with one-line-corrected copy (`table.remove_entry`).

## P2 — wrong numbers / notable misbehavior

### F12 — "Low Storage" warning never fires for Food/maintenance resources
`Lua\ResourceTracking.lua:218-224, 229-234` — `supply*24/v*24` = `((supply*24)/v)*24`,
always 0 or ≥24 under integer division, guard requires `0 < x < 3` → unsatisfiable.
Grid branches (:259-303) are correct. Consts: `_GameConst.lua:4,10-11`. **Fix:** replace
`ResourceTracking.GatheredResourcesOnHourlyUpdate`: `MulDivRound(supply, HoursPerDay, v)`
vs `MinDays* × HoursPerDay`.

### F13 — Command Center resource rows show no numbers
`Data\XDef\CommandCenterCategories.lua:226-328` (+ generated twin) — 11 tags like
`<metals(AvailableMetals)>` reference getters that don't exist (remaster refactored to
`GetAvailable("X")`, `ResourceOverview.lua:144`; other call sites converted, this preset
missed). Nil → `FormatResource` renders empty. **Fix:** define 11 shims
`ResourceOverview.GetAvailableX = function(self) return self:GetAvailable("X") end`.

### F14 — Domes Overview red low-stat highlight dead
`Lua\X\ColonyControlCenter.lua:1309-1320` — builds red-tagged `tv`, then calls
`win.idLabel:SetText(v)`. **Fix:** override `Community.UICommandCenterStatUpdate`, end with
`SetText(tv)`.

### F15 — Mystery 11 wisp RP rewards double/silent
`Lua\Mysteries\Fireflies.lua:466-469` — code after `SetCommand("Die")` unreachable
(`DoSetCommand` kills current thread, CommonLua\Classes\CommandObject.lua:340-378); actual
RP from Die destructor (:540-542). Batch destroy path (:676-688) grants again → trapped
wisps pay 200 RP each while notification says 100; later catches pay 100 silently. **Fix:**
patch `Firefly.Drain` to notify/grant before `SetCommand("Die")` and remove the destructor
double-grant (or drop batch grant) so display == granted.

### F16 — Mirror Sphere site usable after completion
`Lua\Mysteries\MirrorSphere.lua:823` — guard `self.progress == 100`, but scale is
0..`max_progress` (2^22; see :724-726, :734) → lockout never triggers; players can waste
drone work on finished site. **Fix:** override `StartAction`-holder method, compare
`self.progress >= self.max_progress`.

### F17 — Dust Sickness damage not randomized
`Data\TraitPreset.lua:87-91` — `local change = 5 + colonist:Random(trait.param)` dead;
always deals flat `trait.param` (10)/sol instead of 5-14. **Fix:** patch
`TraitPresets.DustSickness.daily_update_func` (data patch at ClassesPostprocess — very
mod-friendly).

### F18 — Independence terraforming tech gives 10% not 20%
`Data\TechPreset.lua:4798-4812` — `param1 = 20` ("decrease percent") but
`Effect_ModifyLabel Amount = -10` on `Consts.SpecialProjectResourcesModifier` (100-based,
consumed `Lua\SpecialProjects.lua:105`). All sibling Independence techs have param == amount.
**Fix:** patch the effect's `Amount = -20` before research (ClassesPostprocess), only if
tech not yet researched — else apply delta modifier.

### F19 — Graphs "Consumed" caption omits maintenance
`Lua\X\ColonyControlCenter.lua:180-188` vs `ResourceTracking.lua:162` — caption uses
consumption only; plotted series adds maintenance. Near-zero caption next to a tall bar for
Machine Parts/Electronics/Metals/Polymers. **Fix:** wrap `City.GetColonyStatsButtons`,
correct the caption closure.

### F20 — Morale tooltip shows unapplied +Comfort bonus
`Lua\Units\Colonist.lua:2983-3007` (tooltip) vs :3963-3969 (`UpdateMorale`, bonus
deliberately commented out: "remove for comfort policy to work") — tooltip still lists
"Living in luxury +5" for Comfort ≥ 70; listed effects don't sum to shown Morale. **Fix:**
override `Colonist.UIStatUpdate`; skip `value >= high` row for Comfort only.

### F21 — Train travel-time penalty includes station waiting
`Lua\Units\ColonistTransport.lua:493,511,551-569` — `ticket.start_wait` set on reaching
platform, never reset at boarding; Comfort "travel time" penalty and train/track
"spent time" stats (TransportStatistics.lua:31-45) count waiting (double-counted vs
station stat); partially bypasses LuxuriousTrains. **Fix:** post-hook `Colonist.BoardVehicle`
to reset `transport_ticket.start_wait = GameTime()`.

### F22 — `GetGridGlobalStorage` breaks Last Transmission gates
`Lua\ResourceOverview.lua:880-899` — zero-demand map returns sentinel `1000 sols` and
per-map sols are **summed**; once Underground loads, `== 0` conditions in
`Data\FactionDef\LastTransmission.lua:103-184` unsatisfiable, `> 2 sols` always true.
**Fix:** redefine: zero-demand map contributes 0; combine with Min (or demand-weighted).

## P3 — cosmetic / latent / mod-facing

### F23 — Founder-gains-trait notification never fires
`Lua\ColonyViability.lua:282-295` — array `FounderGainsTraitCategories` indexed with group
string → always nil. Handler can't be replaced (OnMsg is additive; original is dead and
harmless). **Fix:** add our own `OnMsg.ColonistAddTrait` with a proper set
(`{Positive=true,Negative=true,Specialization=true}`) + dedupe via existing-notification check.

### F24 — Dome pipe visuals corrupt on load (`MoveInside` copy-paste)
`Lua\LifeSupportGrid.lua:304` — passes `dome` where electricity twin
(`ElectricityGrid.lua:291`) passes `self` to `DestroyConnection`. Triggered from
`Dome:OnLoad` (Dome.lua:896-899) repair sweep; stale plugs/connections block future
`ConnectPipe` visuals. **Fix:** override `LifeSupportGridObject.MoveInside`, `dome`→`self`.

### F25 — Tech description names wrong building (pre-1.0.6 saves only)
`Data\TechPreset.lua:1486` (`UndergroundLargeDome`, gated `not UndergroundRework106`) —
description says "Jumbo Cave Reinforcements", tech unlocks `UndergroundDomeMedium`.
**Fix:** ClassesPostprocess description patch. Low priority (legacy saves only).

### F26 — Bombardment missiles fly parallel (cosmetic)
`Lua\Bombardment.lua:82-83` — deviated `spawn_dir` computed, then `spawn_pos` uses base
`dir` (compare Meteors.lua:106-107). Mystery 7 bombardments look uniform. **Fix:** override
`WaitBombard`, use `GenerateDir(dir, angle)` in `spawn_pos`.

### F27 — Storage charge/discharge rate modifiers ignored (latent)
`Lua\ElectricityStorage.lua:47-63`, `Lua\LifeSupportStorage.lua:25-42,131-148` —
`OnModifiableValueChanged` fires for `max_*_charge/discharge` but never copies to
`element.max_charge/max_discharge` (read in SupplyGrid.lua:164-170). No vanilla modifier
touches rates; breaks the documented modding surface. **Fix:** post-hook the three
`OnModifiableValueChanged`s, copy both fields before `UpdateStorage()`.

### F28 — `Research:ReplaceTech` crashes for researched techs (latent)
`Lua\Research.lua:715` — `if not next(g_TechFieldResearchedCount[field_id] == 0)` →
`next(boolean)` error; replacement effects never apply. No vanilla caller; hits
mods/storybits/console. Correct pattern at :246-249. **Fix:** override `Research.ReplaceTech`
branch with `if g_TechFieldResearchedCount[field_id] == 0 then ... = nil end`.

### F29 — Sequence-system latents (mod-facing bundle)
1. `Lua\Sequences\SA_Filters.lua:30-40` — `SA_GetLabelToRegister` ignores
   `random_count`/`random_percent` (returns full list after shuffle). No shipped user.
2. `Lua\Sequences\SA_Gameplay.lua:2705` — `SA_WaitMarsTime` *generated-code* path inverts
   the workshift wait (`==` should be `~=` vs interpreted `StopWait` :2626). No shipped user.
3. `Lua\Mysteries\Diggers.lua:91-95` — broken two-variable swap; unreachable with shipped
   defaults, bites subclasses. **Fix:** all three are small overrides; ship for modder benefit.

## Phase 2 findings — details (2026-07-24)

### F30 — Lake placement entombs RC builder + drones (P1, high)
Two-part defect. (a) `ConstructionSite:ScatterUnitsUnderneath` (`ConstructionSite.lua:1722-1737`)
exempts the RC Constructor building the site. (b) Scatter runs at `Complete` (:1574-1580)
BEFORE `LandscapeLake:GameInit` digs the basin (`LandscapeLake.lua:32-35,215-292`);
`Unit:ExitImpassable` (`Units\Unit.lua:642-649`) no-ops while ground is still passable, so
even scattered drones stay; terrain then drops + `RebuildPassability` seals them. Drones
drain battery → Freeze (`Drone.lua:1478-1524`), read as dead. Devs ship a partial rescue
fixup for rovers only (`BaseRover.lua:736-745`). **Fix:** wrap `LandscapeLake:PlacePrefab` —
after its `RebuildPassability`, sweep units in bbox with `not map:IsPassable(unit)` →
`SetCommand("ExitImpassable")` / teleport to `GetPassablePointNearby`.

### F31 — Anomaly cave-in hardcodes UndergroundMap (P2, med)
`Scenario\UndergroundAnomalies.generated.lua:240` (same in Cave_Of_Wonders data):
`TriggerCaveIn(UndergroundMap, anomaly_pos)` while every sibling action uses the
sequence-local `map` (sequence runs on the anomaly's own map, `Anomaly.lua:293-303`).
Wrong-map rubble; crash risk if `UndergroundMap` false (`CaveInRubble.lua:101`).
**Fix:** wrap `TriggerCaveIn(map, pos)`: reject `map.mapdata.Environment ~= "Underground"`.

### F32 — Dismissed warnings re-add instantly (P2, med mechanism-certain)
Object-status notifications (`NotWorkingBuildings`, `DestroyedInfrastructure`,
`RoverDamaged`) are not `Suppressable` (`Data\NotificationPreset.lua:771-781`); any
`SetWorking()` on any building re-creates them (`BaseBuilding.lua:165-169` →
`Notifications.lua:231-236`). Dismissal while a persistent bad state exists → instant
re-add. Matches lake-victim report. **Fix:** set `Suppressable = true` +
`SuppressTime = const.DayDuration` on those presets (data patch, very compat-friendly).

### F33 — Drone crash on small landscaping sites (P2, high)
`Landscape\LandscapeConstructionSiteBase.lua:186-190`: `for i = 1, top_count do
top_dests[i] = dests[i].dest` — nil-index when site periphery has < 5 hexes (tiny
clear/paint blobs) → error in drone command thread. **Fix:** `Min(top_count, #dests)`.

### F34 — Landscape nil-guard bundle (P3, med/latent)
(a) `ClearWasteRockConstructionSite:GameInit` (`:60-63`) unguarded `Landscapes[self.mark]`;
(b) `LandscapeMarkEnd` (`Landscaping.lua:200-206`) unguarded nil mark;
(c) lake `landscape_grid` overlap only assert-guarded (`LandscapeConstructionController.lua:502-507`,
release asserts stripped → silent corruption);
(d) `LandscapeForEachUnit` dead embark filter (`Landscaping.lua:455-469`).

### F35 — Large Wind Turbine buff lost in old saves (P2, high)
Current `FrictionlessComposites` data is CORRECT (`Data\TechPreset.lua:796-821` targets
WindTurbine, WindTurbine_Large, WindTurbine_Diffuser). But the migration fixup
`SavegameFixups.WindTurbine_Large_ReapplyModifiers` (`Buildings\WindTurbine.lua:78-88`)
only reapplies the `WindTurbine_Diffuser` label — never `WindTurbine_Large`. Saves that
researched the tech pre-hotfix keep unbuffed Large Turbines forever. Matches review
report ("polymer upgrade works now, frictionless doesn't"). Rotation lock is by design
(`can_rotate_during_placement = false`). **Fix:** one-shot LoadGame sweep: if tech
researched and no colony label-modifier for `WindTurbine_Large.electricity_production`,
add it (mirror the fixup, corrected).

### F36 — Universities overtrain geologists (P2, high behavior-confirmed)
`City:GetNeededSpecialist` (`City.lua:561-593`) counts every `ui_working` workplace incl.
extractors (`specialist="geologist"`, `max_workers=4`); ExtractorAI only sets
`g_ExtractorAIResearched`, used solely to silence a construction warning
(`BaseExtractor.lua:60-68`) — worker demand never zeroed. Auto-mode universities
(`MartianUniversity.lua:24-29`) keep producing geologists for unmanned extractors.
**Fix:** wrap `GetNeededSpecialist`: skip extractor workplaces when ExtractorAI researched
(match its actual gameplay meaning).

### F37 — Ghost farm oxygen survives salvage (P1, high)
`FarmBase:ApplyOxygenProductionMod` (`Farm.lua:561-571`) puts negative `air_consumption`
modifier on `parent_dome` keyed `farm_id`; no `FarmBase:Done`, `Building:Done`/`SetDome(false)`
never clear it, and demolish path skips `UpdateWorking(false)` for non-`use_demolished_state`
buildings (`Building.lua:1457-1483`, `Demolishable.lua:139`). Dome keeps phantom O2 forever.
**Fix:** wrap `FarmBase` delete path (post-hook `Done` via class or `OnMsg` on demolish) to
remove the dome modifier; one-shot LoadGame sweep for orphaned `farm_id` modifiers.

### F38 — Destroyed tunnels rejoin pathfinding after load (P2, high)
`Tunnel:OnDestroyed` correctly calls `RemovePFTunnel` (`Tunnel.lua:153-155`), but
`OnMsg.LoadGame` (:264-266) re-adds PF tunnels for ALL `TunnelBase` with no `destroyed`
check (`AddPFTunnel` :197-209 checks only `IsValid(linked_obj)`; ruins are valid).
`TraverseTunnel` (:215-262) same. Rovers path through dead tunnels after any save/load.
**Fix:** wrap `Tunnel.AddPFTunnel`: bail if `self.destroyed or (self.linked_obj and
self.linked_obj.destroyed)`; on load also `RemovePFTunnel` for destroyed ones.

### F39 — Second Artificial Sun ignored (P2, high)
`SolarPanelBase:GameInit` (`SolarPanel.lua:8-14`): only `labels.ArtificialSun[1]` tested
with `TestSunPanelRange`. Panel built in range of sun #2 only never registers (reverse
direction works, `ArtificialSun.lua:35-47`). **Fix:** wrap GameInit: iterate the whole
label, register first sun in range.

### F40 — Dust Sickness infects Biorobots (P2, high)
`Data\StoryBit\DustSickness*.lua` filters exclude only `Child`; `Android` trait not
excluded, `DustSickness.incompatible = {}`; androids bleed Health every dust storm via
`daily_update_func` until cure tech. (Same trait also hit by F17 randomization bug.)
**Fix:** data patch: add Android to the storybit filters / trait incompatibility.

### F41 — Gene Forging tech has no effect (P2, high)
`Colonist:GetRareTraitChance` (`Colonist.lua:3541-3550`) reads only
`TechDef.GeneSelection.param1`; `GeneForging` (`TechPreset.lua:1556-1564`, param1=50)
referenced nowhere in gameplay code. **Fix:** wrap `GetRareTraitChance`: add GeneForging
param when researched (ChoGGi's original approach: bump GeneSelection.param1 to 150).

### F42 — Buildings placeable on active dust devils (P3, high)
`AreThereBlockingUnitsUnderneath` (`Construction.lua:1895-1914`) queries only
Drone/BaseRover; `BaseDustDevil` inherits `Object` (`DustDevils.lua:245-247`) — never
checked anywhere in Construction\. **Fix:** wrap `ConstructionController:UpdateConstructionStatuses`-
family to add a dust-devil proximity check (or extend the blocking query).

### F43 — Layout construction bypasses tech locks (P3, high)
`LayoutConstructionController:Activate` (`LayoutConstruction.lua:231-263`): tech-locked
building with no prefab item → `require_prefab=false` → `add=true`, sub-controller
placed with no research gate. **Fix:** wrap `Activate`: filter items where
`not tech_enabled and not self.prefab`.

### Verified FIXED in remaster (do not fix; note in release credits/research)
- Schools training already-owned perks (`FilterCompatibleTraitsWith`, `Traits.lua:1051-1074`).
- Unrepairable building at 0 accumulated maintenance (malfunction paths force-fill points,
  `RequiresMaintenance.lua:230-262`).
- Colonists suffocating in domes wearing suits (outside-state reworked to recompute on
  every stop, `Colonist.lua:2152-2155`).
- Eureka storybit wrong tech category (`Boost9_Eureka.lua:79-167` now 5 weighted outcomes).
- Inspiring Architecture freeze (stateless recompute now; savegame fixups clean old saves —
  `Dome.lua:3222-3256`, `_fixup.lua:1905-1930`).
- `CargoTransporter:SpawnRovers` typo (per ChoGGi's own SMR note).
- Sol 2983 GameTime overflow: indeterminate from Lua (engine-side); circumstantial evidence
  of 64-bit time. Park unless players report it.

## Candidates under investigation

### C01 — `BreakthroughOrder` rebuilt+reshuffled on every map load
`Lua\Buildings\Anomaly.lua:652-682` (`City:InitBreakThroughAnomalies`), called from
`InitCity` on every `NewMapLoaded` (`City.lua:477`); `BreakthroughOrder` is a savegame
GameVar. With asteroids, maps load repeatedly mid-game. Same family as the original B&B
"no planetary anomaly breakthroughs" bug (ChoGGi's fix: run once). Need to trace: how
markers/planetary anomalies consume the order; whether reshuffle causes duplicate or lost
breakthroughs. Surface call also `DoneObject`s markers (planetary reservation :667-674,
excess :676-681).

## Not yet swept (follow-up targets)

- `Lua\Buildings\DroneControl.lua`, `ShuttleHub.lua` — drone/shuttle task assignment.
  Prime suspect for live reports: "drones ignore rocket cargo at high priority",
  "RC transports don't auto-offload rockets", "late-game drones stop maintaining
  inside open domes / cluster stuck outside" (review-sourced).
- Colonist auto-assignment: workplaces (`UpdateWorkplaces` family — "unemployed
  every sol"), residences ("homeless despite free housing", "seniors don't move"),
  dome-to-dome walking/passage checks (`AreDomesConnectedWithPassage` — suffocation
  on long walks; stuck on Universal Depots).
- `Landscape\` (terraforming) — "lakes causing crashes", artificial lake entombing
  rovers + notification retrigger loop.
- Asteroid cave-in trigger — NOT the underground marsquake repeat (asteroids are
  `Environment == "Asteroid"`, gate requires `"Underground"`); find actual source.
- Martian Express track editing (single-hex delete removes whole track) — LukeH
  prior art.
- Large Wind Turbine tech modifiers not applying (Frictionless Composites) —
  targeted label/template check, do early.
- Inspiring Architecture freeze (also in original); `RandomMap\`; `Construction\`
  beyond F-items; UI XTemplate layout (misaligned buttons — cosmetic).
- Remaster player-report list (see `docs/RESEARCH.md`) — several reports not yet mapped
  to code: seniors not auto-moving to retirement homes, mysteries not starting
  (Inner Light), no cold waves/dust storms triggering, asteroid lander launching empty,
  auto asteroid miners missing from build menu, Martian Express track salvage issues,
  universities training geologists after Extractor AI, Fast Rockets rule stopping,
  Single Party tension, can't rebuild on old building spots.
