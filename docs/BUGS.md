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
| F02 | Meteors strike ~every 6h instead of 35–115h              | P1  | high | fixed  |
| F03 | Upgrade buffs leak & stack after salvage/demolish        | P1  | high | fixed* |
| F04 | Night-shift workers never return to work after midnight  | P1  | high | fixed  |
| F05 | Milestone completion crashes (NoTerraforming/NoPolitics) | P1  | high | fixed  |
| F06 | Philosopher's Stone mystery can hang forever             | P1  | med+ | fixed  |
| F07 | St. Elmo's Fire "free wisps" gives ~1/1000 power         | P1  | high | fixed  |
| F08 | Tourist star-rating applicant bonus inverted             | P1  | high | fixed  |
| F09 | Tourist Satisfaction drifts down (asymmetric thresholds) | P1  | high | fixed  |
| F10 | Faction funding conditions always error (BlueSun/Brazil/Russia) | P1 | high | fixed |
| F11 | Train wedges at platform (`table.remove` misuse)         | P1  | high | fixed  |
| F12 | "Low Storage" warning never fires for Food/maintenance   | P2  | high | fixed  |
| F13 | Command Center resource rows show no numbers             | P2  | high | fixed  |
| F14 | Domes Overview red low-stat highlight dead               | P2  | high | fixed  |
| F15 | Mystery 11 wisp RP rewards double/silent                 | P2  | high | fixed* |
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
| F30 | Lake placement entombs RC builder + drones               | P1  | high | fixed  |
| F31 | Anomaly cave-in hardcodes UndergroundMap (cross-map)     | P2  | med  | todo   |
| F32 | Dismissed warnings re-add instantly (not suppressable)   | P2  | med  | todo   |
| F33 | Drone crash on small landscaping sites (nil-index)       | P2  | high | todo   |
| F34 | Landscape nil-guard bundle (latent crash paths)          | P3  | med  | todo   |
| F35 | Large Wind Turbine buff lost in old saves (fixup bug)    | P2  | high | todo   |
| F36 | Universities overtrain geologists (unmanned extractors)  | P2  | high | todo   |
| F37 | Ghost farm oxygen modifier survives salvage/demolish     | P1  | high | fixed  |
| F38 | Destroyed tunnels rejoin pathfinding after save/load     | P2  | high | todo   |
| F39 | Second Artificial Sun ignored by solar panels            | P2  | high | todo   |
| F40 | Dust Sickness infects Biorobots (androids)               | P2  | high | todo   |
| F41 | Gene Forging tech has no effect                          | P2  | high | todo   |
| F42 | Buildings placeable on active dust devils                | P3  | high | todo   |
| F43 | Layout construction bypasses tech locks                  | P3  | high | todo   |
| F44 | One-hex track salvage can delete the entire track        | P1  | high | fixed  |
| F45 | Damaged tracks can't be salvaged at all (sort crash)     | P1  | high | fixed  |
| F46 | Trains dump cargo at stations with resource disabled     | P2  | high | todo   |
| F47 | Track salvage refunds ~1 hex for whole track / 0 partial | P3  | high | todo   |
| F48 | Station-connector savegame fixup no-op (paren misplaced) | P3  | high | todo   |
| F49 | Train minors bundle (palette, split kills trains, etc.)  | P3  | med  | todo   |
| F50 | Auto-rockets kick approaching drones to Idle every hour  | P1  | high | fixed  |
| F51 | Transport-mode cache never sees new shuttles (homeless)  | P1  | high | fixed  |
| F52 | Colonists still walk ≤400m in vacuum past passages       | P1  | high | fixed* |
| F53 | Arrivals hike to unreachable "safety dome" and die       | P1  | high | fixed  |
| F54 | Switched-off shuttle hubs count as transport available   | P2  | med+ | todo   |
| F55 | Open domes: drone access lost + unreachable-forever cache| P1  | med  | fixed* |
| F56 | Auto RC Transports never offload rockets                 | P2  | high | todo   |
| F57 | Drone/transport minors bundle                            | P3  | med  | todo   |
| F58 | Invisible residence reservations never expire            | P1  | high | fixed* |
| F59 | Freed housing never notifies homeless (12h retry lag)    | P2  | med  | todo   |
| F60 | Dome free-space uses `working`, assignment `ui_working`  | P2  | med  | todo   |
| F61 | Home dome's migration toggle blocks outbound shopping    | P1  | med+ | fixed  |
| F62 | Services reach 1 passage hop only, never trains          | P2  | high | todo   |
| F63 | Universities invisible to emigration (no students)       | P2  | high | todo   |
| D01 | Rockets don't auto-refuel/auto-export rare metals        | dsgn| high | opt-in fix |
| F64 | Station demolition permanently leaks train prefabs       | P1  | high | fixed  |
| F65 | Station-at-tunnel never bridges the power grid           | P2  | med  | todo   |
| F66 | Station↔tunnel connector hex ping-pong (never connects)  | P2  | med+ | todo   |
| F67 | Auto-lander launches empty, ping-pongs Mars↔asteroid     | P1  | high | fixed  |
| F68 | Hourly auto-request ratchet unloads lander's own cargo   | P1  | high | fixed  |
| F69 | Manual landing dumps the return fuel (stranded landers)  | P1  | high | fixed  |
| F70 | Edit Payload silently refills from policy template       | P2  | med+ | todo   |
| F71 | Auto-export fills capacity alphabetically (waste rock)   | P2  | med  | todo   |
| F72 | "No available landers" while a lander sits on the pad    | P2  | med  | todo   |
| F73 | Asteroid colonists idle outdoors; no shelter reflex      | P1  | med+ | fixed  |
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

### F02 — Meteors strike ~every 6h instead of 35–115h  `[fixed: Code/Fix_MeteorFrequency.lua — replaces GlobalGameTimeThreadFuncs.Meteors + restart on LoadGame]`
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

### F03 — Upgrade buffs leak & stack after salvage/demolish  `[fixed*: Code/Fix_UpgradeModifierLeak.lua stops new leaks; one-shot savegame cleanup sweep for already-leaked modifiers still TODO]`
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

### F06 — Philosopher's Stone mystery can hang forever  `[fixed: Code/Fix_CrystalMysteryHang.lua]`
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

### F09 — Tourist Satisfaction drifts down (asymmetric threshold crossings)  `[fixed: Code/Fix_TouristSatisfaction.lua]`
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

### F11 — Train wedges at platform (`table.remove` misuse)  `[fixed: Code/Fix_TrainPlatformWedge.lua]`
`Lua\Units\ColonistTransport.lua:541-547` (`ExitVehicle` stale-passenger guard) —
`table.remove(vehicle.units, self)` needs an integer pos; intended API is
`table.remove_entry`. When the guard fires (dev comment: CargoTransporter abduction),
the error aborts before `DiscardTransportTicket`; `Train:UnloadTrain`
(`Units\Train.lua:443-453`) then spins forever → train permanently blocks platform.
**Fix:** replace `Colonist.ExitVehicle` with one-line-corrected copy (`table.remove_entry`).

## P2 — wrong numbers / notable misbehavior

### F12 — "Low Storage" warning never fires for Food/maintenance resources  `[fixed: Code/Fix_LowStorageWarning.lua]`
`Lua\ResourceTracking.lua:218-224, 229-234` — `supply*24/v*24` = `((supply*24)/v)*24`,
always 0 or ≥24 under integer division, guard requires `0 < x < 3` → unsatisfiable.
Grid branches (:259-303) are correct. Consts: `_GameConst.lua:4,10-11`. **Fix:** replace
`ResourceTracking.GatheredResourcesOnHourlyUpdate`: `MulDivRound(supply, HoursPerDay, v)`
vs `MinDays* × HoursPerDay`.

### F13 — Command Center resource rows show no numbers  `[fixed: Code/Fix_CommandCenterNumbers.lua]`
`Data\XDef\CommandCenterCategories.lua:226-328` (+ generated twin) — 11 tags like
`<metals(AvailableMetals)>` reference getters that don't exist (remaster refactored to
`GetAvailable("X")`, `ResourceOverview.lua:144`; other call sites converted, this preset
missed). Nil → `FormatResource` renders empty. **Fix:** define 11 shims
`ResourceOverview.GetAvailableX = function(self) return self:GetAvailable("X") end`.

### F14 — Domes Overview red low-stat highlight dead  `[fixed: Code/Fix_DomeOverviewHighlight.lua]`
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

### F30 — Lake placement entombs RC builder + drones (P1, high)  `[fixed: Code/Fix_LakeEntombment.lua]`
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

### F37 — Ghost farm oxygen survives salvage (P1, high)  `[fixed: Code/Fix_GhostFarmOxygen.lua — SetDome hook + LoadGame sweep]`
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

### F44 — One-hex track salvage can delete the entire track (P1, high)  `[fixed: Code/Fix_TrackSalvageWipe.lua]`
Per-segment removal exists (`Construction.lua:2910-2911` → `TrackElement.lua:444-578`
`DemolishAndSplitTrack`), but: (a) click snaps up to ±5 hexes to nearest pillared element
(`SelectionPropagate`, `TrackElement.lua:281-307`); (b) deletion zone expands to nearest
"pillared AND straight" element each side (:479-486) — curves are pillared-but-never-
straight, so whole curved sections go; (c) remainder-viability fallbacks (:503-530) call
`track_obj:OnDemolish()` — ENTIRE track — whenever one side is too short (any ≤5-element
track, clicks near ends, curve-heavy tracks). `OnDemolish` (`Track.lua:248-284`) also
destroys all assigned trains. Element salvage is instant, no countdown (`:259-261`).
**Fix:** override `DemolishAndSplitTrack`: replace both whole-track fallbacks with
trimming only the short side (delete elements individually + `UpdateEndElements()`);
never touch the viable side.

### F45 — Damaged tracks can't be salvaged at all (P1, high)  `[fixed: Code/Fix_BrokenTrackSalvage.lua — wrapper + LoadGame sweep for existing saves]`
`TrackBase:BreakTrackElement` (`Track.lua:618-659`) copies element params to the repair
site but NOT `node_idx` → stays `false` (`TrackElement.lua:164`). Every salvage path then
hits `table.sort(all_elements, function(a,b) return a.node_idx < b.node_idx end)`
(`TrackElement.lua:458-464`) → boolean<number comparison error BEFORE any deletion; click
silently does nothing. Affects salvage click, Ctrl+click, infopanel Salvage button, and
clicking the repair site. Meteors routinely break tracks → matches "can't salvage /
undeletable track" reports (incl. after station destruction). **Fix:** wrap
`BreakTrackElement` to stamp `element.broken.node_idx = element.node_idx`; belt-and-braces
tolerant sort + LoadGame sweep stamping existing repair sites.

### F46 — Trains dump cargo at stations with the resource disabled (P2, high)
`Train:UnloadAll` (`Train.lua:783-803`) unloads everything with room, no
`station:IsResourceEnabled(res)` check (disable only removes the demand from
task_requests, `StorageDepot.lua:583-587,641-668`). Cargo planner then treats it as
"forbidden" stock and dispatches trains to haul it back out (`Train.lua:868,905-939`) —
resource ping-pong. **Fix:** override `UnloadAll` with enabled-check (allow dump if no
station on route accepts, to avoid stranding).

### F47 — Track salvage refund ~1 hex for whole track; 0 for partial (P3, high)
`TrackBase:GetRefundResources` (`Track.lua:286-307`) reads cost from ONE element (last);
`construction_cost_at_completion` set only on FIRST element (`Track.lua:524-525`) —
first/last mismatch; `DemolishAndSplitTrack` uses bare `DoneObject`, no refund (contrast
`Passage.lua:1217-1222`). Track cost 200 Metals/hex. **Fix:** multiply by `#self.elements`;
place return stockpile on partial salvage.

### F48 — Station-connector savegame fixup no-op (P3, high defect / low impact)
`Station.lua:1346`: `ProcessTrackElements(ResolveMap(track, track.elements))` — paren
misplaced, should be `ProcessTrackElements(ResolveMap(track), track.elements)`; migration
no-ops (may contribute to "tracks won't connect" on old saves). **Fix:** re-run corrected
pass in one-shot LoadGame sweep.

### F49 — Train minors bundle (P3, med)
(a) instant-built tracks use pipes palette (`Tracks.lua:385` vs `TrackElement.lua:791`);
(b) `DemolishAndSplitTrack` ignores `assigned_vehicles` — mid-transit trains silently
stored/self-destruct (`Train.lua:249-251,535-541`); (c) salvage click on invisible
connector hexes propagates to the STATION (`TrackElement.lua:299-300`); (d) `max_vehicles`
never recomputed after merge/split (`Track.lua:64-65`); (e) dead validation
(`TrackRequiresTwoStations` never inserted; `CanContinueTrack` never called).

### Trains: verified fixed / working-as-designed
Trains blocking demolition: FIXED (trains stored as prefabs, `Track.lua:159-166`).
Destroyed stations leaving undeletable track: addressed (`TrainTransport.lua:14-35`) —
lingering reports likely F45. "Won't connect to stations": strict geometric rules with
zero feedback, no coding error found (F48 for migrated saves). "Rebuild blocked by raised
terrain": design (endpoint/turn `max_z_delta` check, `Tracks.lua:35-65,281-284`).

### F50 — Auto-rockets kick approaching drones to Idle every hour (P1, high)  `[fixed: Code/Fix_RocketDroneChurn.lua]`
`UniversalRocketBase:HourlyUpdate` (`UniversalRocket.lua:1357-1370`) → `CreateAutoCargoRequest`
→ `SetCargoRequest` → `UpdateCargoResourceRequests` (`CargoTransporterNew.lua:1238-1271`)
does `DisconnectFromCommandCenters()` + reconnect EVERY HOUR while landed;
`DroneControl:OnRemoveBuilding` (`DroneControl.lua:720-729`) sets every drone heading
there to `Idle`. Trips > 1 game hour can never complete; priority irrelevant. Aggravators:
`starting_drones = 0`, `exclude_from_lr_transportation = true` (shuttles never help).
Explains "drones ignore rocket cargo". **Fix:** wrap `UpdateCargoResourceRequests` to
suppress the disconnect/reconnect churn (requests mutate in place via
`TaskRequester:AddRequest`); one-time connect if never connected.

### F51 — Transport-mode cache never sees new shuttles (P1, high)  `[fixed: Code/Fix_ShuttleTransportCache.lua]`
`Colonist.lua:2504-2537` caches `(community,pos) → mode` incl. `false`, but
`shuttles_available` is not in the key and cache only flushes on train/passage events
(:2480-2488). Building/refueling a Shuttle Hub never flushes → `FindEmigrationDome`
(:2657-2698) skips domes forever. Explains homeless-despite-free-housing and cross-dome
seniors. **Fix:** wrap `FindTransportationModeToCommunity` to key on shuttle flag + flush
cache on ConstructionComplete/TTL.

### F52 — Colonists still walk ≤400m in vacuum past passages (P1, high)  `[fixed*: Code/Fix_VacuumWalks.lua — passage route now always looked up in vacuum; the surface walk is still allowed when NO passage route exists (refusing it would strand colonists on shuttle-less maps) — that half stays open]`
`FindTransportationModeToCommunity_BeforeTrains` (`Colonist.lua:2467-2476`) returns "walk"
whenever ≤400m (`ColonistMaxDomeWalkDist`, `_GameConst.lua:133`); `TryToEmigrateToDome`
(:1555-1575) only computes passage path when `transport_mode_dist > min_dist` — walk mode
guarantees it isn't. 400m ≈ 100s walk vs `OxygenMaxOutsideTime` 120s (`__const.lua:1604`)
— exit/queue/detours push it over. The original long-walk bug, still present. **Fix:**
override `TryToEmigrateToDome`: in non-breathable atmosphere always try passage path
first; cap raw outside walks to an oxygen budget; else shuttle/stay.

### F53 — Arrivals hike to unreachable "safety dome" and die (P1, high)  `[fixed: Code/Fix_ArrivalDeaths.lua]`
`GetDomesReachableByColonists` (`_GameUtils.lua:346-395`): `safety_dome` = nearest by
distance even if NOT walkable; `ChooseDome` (:426-441) falls back to it; `Colonist:Arrive`
(`Colonist.lua:1293-1297`) sends `TransportByFoot` unconditionally, and drops colonists at
the `Colonistout` spot with no passable-point search (:1280-1291; contrast
`CargoTransporterNew:EjectColonists` which uses `GetRandomPassableAroundOnMap`). Explains
rocket→dome deaths and "stuck on Universal Depots". **Fix:** replace `Arrive`: snap drop pos
passable; re-check the destination only when it is neither in walking distance nor reachable
through the elevator assigned with it (`RocketBase.lua:2068-2071` → `TransportByFoot`,
`Colonist.lua:2724-2737`; cross-map pairs are never "in walking dist", `Dome.lua:248-251`).
On re-check take both `ChooseDome` returns and write `emigration_elevator` back, else wait
near rocket under "Confused Colonists" + retry dome selection.

### F54 — Switched-off shuttle hubs count as transport available (P2, med-high)
`IsLRTransportAvailable` (`ShuttleHub.lua:350-359`) counts hubs with
`GetWorkNotPermittedReason()` truthy (= player toggled OFF) as available, but
`SendOutShuttles` only runs when `working`. All-hubs-off (late-game power saving) →
colonists queue on pickup spots outside for shuttles that never come; walkability logic
also skewed (`Dome.lua:256-259`). **Fix:** predicate counts only self-lifting suspensions.

### F55 — Open domes: drone access lost + unreachable-forever cache (P1, med — matches report exactly)  `[fixed*: Code/Fix_DroneUnreachableForever.lua — the unreachable-forever cache (3) is fixed; the open-air entrance half (1) is NOT actionable, see below]`
(1) Open-air skin swaps dome entity with `skin[2] = empty_table`
(`OpenAirBuilding.lua:216-237`) → `Dome_Entrance` attaches destroyed
(`Building.lua:2409-2430`) → their PF tunnels (only drone routes in,
`Dome_Entrance.lua:15-16`) removed (`Movable.lua:602-605`). (2) Same moment, inside
buildings START needing maintenance (`OpenDome_Maintenance`, `OpenAirBuilding.lua:114-123`).
(3) Failed approaches cached `GameTime() + max_int` = unreachable forever
(`Drone.lua:819-849`), only reset by passability edits, then re-fail. (4) `Drone:GoHome`
filters park spots by `GetPointOutsideDomesIn` (`Dome.lua:2505-2507`) → fleet clusters
just outside the dome. Caveat: final passability of `*_Open` entities is engine data —
unverifiable from Lua. **Fix:** override `Dome:CalcOpenAirSkin` to preserve entrance
attaches; override approach-failure cache to store `GameTime()` so `CleanUnreachables`
retires entries.

### F56 — Auto RC Transports never offload rockets (P2, high)
`RCTransport.lua`: `Automation_Gather` (:884-908) sources only surface deposits;
`Automation_Unload` (:910-941) excludes rockets as destinations. Manual load/routes work —
players correctly perceive AUTO as broken. Combined with F50 + shuttle exclusion, remote
rockets have no automated unloader at all. **Fix:** extend `ProcAutomation`: when empty,
seek landed `UniversalRocketBase` with status "unloading", `TransferAllResources`.

### F57 — Drone/transport minors bundle (P3, med)
(a) `DroneControl:UpdateRocketsInternal` (`DroneControl.lua:613-639`) clears only
`r_t.Fuel`, writes `r_t[r.FuelResource]` — stale restrictor for non-"Fuel" rockets (latent);
(b) `OnMsg.OnPassabilityChanged` (`Drone.lua:851-864`) rebuilds unreachable table without
weak-keys meta and doesn't recompute count; (c) `recursive_enum_dome_workplaces`
(`Dome.lua:674-675`) skips quarantine check, saved only by `Workplace:IsSuitable` re-check.

### Assignment systems: investigated, no single defect (leads recorded)
- "Unemployed every sol": no smoking gun; three verified contributing mechanisms —
  (1) Open-domes cross-dome employment uses DAILY-recomputed 400m walk distances
  (`Dome.lua:203-238,910-914`) — boundary flips fire commuters (`Colonist.lua:1498-1499`);
  (2) `Dome:OnSupplyInterrupted` (`Dome.lua:1584-1618`) fires all cross-dome commuters
  after 1 sol of any supply interruption; (3) re-employment throttled to 12h at ≥3600
  colonists (`City.lua:118-120`). Needs a repro save.
- Same-dome seniors→retirement: working as designed (comfort scoring, `Residence.lua:382-423`);
  cross-dome is F51.

### F58 — Invisible residence reservations never expire (P1, high)  `[fixed*: Code/Fix_StaleReservations.lua — timestamp + daily stale sweep using g_Consts.ForcedByUserLockTimeout; the infopanel display of #reserved is deliberately NOT added (UI addition, FIX_POLICY §4)]`
`Residence:GetFreeSpace` (`Residence.lua:198-200`) subtracts `#self.reserved`, but the UI
(`GetUICapacity`/`GetUIResidentsCount`, :374-380) never shows reservations. Emigration
reserves slots (`Colonist.lua:1571-1589` → `Dome.lua:2840-2851`) cleared only on arrival/
death/re-home — NO timeout (only user_forced has one, `Colonist.lua:2329-2342`). Colonists
stuck waiting for shuttles (F51/F54!) hold destination slots forever AND are excluded from
the Homeless label (`Colonist.lua:2284`). Devs shipped a reserved-list fixup already
(`Residence.lua:591-599`) — the list drifts in production. Explains "can't find houses in
a >50% vacant dome". **Fix:** cancel reservation in `UpdateResidence` when not actively en
route; sol-tick sweep of stale `reserved` entries; show `#reserved` in infopanel.

### F59 — Freed housing never notifies homeless (P2, med)
`RemoveResident` (`Residence.lua:83-90`) and `CancelResidenceReservation` (:353-365) never
call `CheckHomeForHomeless`; homeless rely on Idle heavy-update throttled to 12 game hours
at 3600+ pop (`City.lua:118-120`). **Fix:** post-hook `RemoveResident` →
`CheckHomeForHomeless()`.

### F60 — Dome free-space uses `working`, assignment uses `ui_working` (P2, med)
`Dome:RefreshFreeLivingSpaces` (`Dome.lua:2832-2834`) omits `player_enabled` →
`GatherFreeLivingSpaces` counts by `working` (`_GameUtils.lua:475-483`); unpowered
residences count 0 for births/immigration gates while `ChooseResidence` (:412) still
assigns to them. Power flicker desyncs the two views. **Fix:** pass consistent member.

### F61 — Home dome's migration toggle blocks outbound shopping/work/training (P1, med-high)  `[fixed: Code/Fix_HomeDomeMigrationGate.lua]`
`Dome:GetService` (`Dome.lua:2900-2916`; same at 2927/2947/2959, `ShiftsBuilding.lua:250-254`):
outbound cross-dome access requires `self.accept_colonists` — the HOME dome's
"accept colonists" MIGRATION policy. Turning it off on a residential dome (routine) silently
stops residents shopping/working/training through passages; target-dome checks are separate
and correct (`Dome.lua:2880-2882`). Best match for "refuse to shop through a passage".
**Fix:** override the four sites, dropping home-side `accept_colonists` from the condition.

### F62 — Services reach exactly 1 passage hop, never trains (P2, high mechanism)
`GetService` iterates `GetConnectedDomes()` = direct adjacency refcounts (`Dome.lua:619-644`,
`Passage.lua:1237-1247`), not the transitive `dome_networks` (`Passage.lua:1096-1119`);
workplace search additionally enumerates train-reachable domes (`Dome.lua:646-690`).
Hub-and-spoke: spoke→spoke shops invisible. **Fix:** extend service search to the passage
network (and optionally train-reachable domes) — flag as behavior change, default on.

### F63 — Universities invisible to emigration (P2, high)
Training is pull-only from student side, 1 hop, F61-gated (`Colonist.lua:1505-1507`,
`Dome.lua:2945-2955`); `FindEmigrationDome` scores only `labels.Workplace`
(`Colonist.lua:2644,2672`, `Workforce.lua:53-64`) — `TrainingBuilding` is a different label
(`TrainingBuilding.lua:26,38`) = zero score. Nobody relocates to study; shuttle-only
university sits empty forever. Only unspecialized colonists qualify
(`MartianUniversity.lua:65-67`). **Fix:** include free training slots (colonist `CanTrain`)
in emigration scoring; walk full passage network in `ChooseTraining`.

### D01 — Rockets don't auto-refuel / auto-export rare metals — INTENTIONAL REDESIGN (verdict)
Not a bug: legacy always-on PreciousMetals loader exists only in dead legacy class
(`RocketBase.lua:1730-1734`; `RocketCompatibility.lua:58-59,97-98` nils old fields).
UniversalRocket: `auto_mode_on = false` default (`UniversalRocket.lua:113`); manual mode
requests cargo only via payload dialog; `GetFuelResourceRequest` returns 0 with no
`arrival_loc` (:1639-1642) — idle rockets request NO fuel until a destination is picked
(slow self-synthesis :1621-1637 fills only existing demand). Old behavior gated behind
Automated Mode + per-resource `export_above` thresholds (:1727-1766, defaults `false`) +
$1000M funding floor (:1399,1762-1765). Community hates it → ship an OPT-IN "classic
rocket behavior" fix (disabled by default per policy §4): standing PreciousMetals demand +
fuel request while landed/manual; document the gates in README either way.

### F64 — Station demolition permanently leaks train prefabs ("trains go to void") (P1, high)
Trains are a colony-counted resource (`city.available_prefabs["Train"]`, `City.lua:433-440`)
— consumed on deploy (`Track.lua:428-457`), refunded ONLY via `Train:OnDemolish`
(`Train.lua:205-209`), which only runs through `Demolishable:DoDemolish`. Bare
`DoneObject(train)` never refunds. The bug: `OnMsg.BuildingDemolished` handler
(`Station.lua:163-171`) hard-`DoneObject`s every train with `current_station == station`
— synchronously BEFORE `Station:Done`'s proper storing loop (`Station.lua:145-149`,
`DestroySilent` = refund + notification), which then finds nothing (dead code on demolish
path). Aggravators: `current_station` stays = departure station all trip (`Train.lua:164-166`)
so mid-transit trains elsewhere vaporize too; no notification. At counter 0: "Send out
Train" disabled at every station (`Station.lua:653-660`), `AssignTrain` early-outs —
permanent, survives rebuilding everything. Matches "trains go to void" exactly. Recovery
in vanilla: construct new trains for Metals+Electronics (`Station.lua:573-611`) — players
don't know the stored ones are gone. **Fix:** pre-hook `Station:OnDemolish` to
`DestroySilent` docked/registered trains BEFORE the message fires; belt-and-braces
`Train.Done` refund guard; compensation prefabs for corrupted saves not exactly
recoverable (count unrecorded).

### F65 — Station attached to a train tunnel never bridges the power grid (P2, med)
`TrackTunnel` description promises power transfer (`Data\BuildingTemplate\TrackTunnel.lua:17`);
class machinery identical to working `Tunnel`. Defect: `OnMsg.StationsConnected`
(`Track.lua:668-680`) skips `ConnectToGrids()` when `#track.elements <= 2` ("adjacent
anyway" assumption) — station attached directly to tunnel connects via exactly 2 connector
elements → supply tunnel never created, no power link. Caveat: TrainTunnel entity spot
data is binary, unverifiable from Lua. **Fix:** additional `OnMsg.StationsConnected`
handler: if 2-element track touches a `TrackTunnelBase`, call `track:ConnectToGrids()`;
LoadGame pass re-asserting masks/merges.

### F66 — Station↔tunnel connector hex ping-pong (P2, med-high)
With a 1-hex gap, both buildings project their connector element onto the SAME hex;
`TrackConnectedObjBase:CreateConnectorElements` (`TrainTransport.lua:126-130`) deletes the
other's element (assert assumes never two live owners) → victim's `Done` reschedules its
own `CreateConnectorElements` → infinite steal loop; whichever lacks the element fails
`GetConnectedTrack`/`GetDestStation` (`Track.lua:320-355`) → no route ever forms. Also:
double-turn constraint refuses connections silently (`TrackElement.lua:336-345`).
Workaround: ≥2-hex gap. **Fix:** patch `CreateConnectorElements` to not delete elements
owned by a live non-destructing building (breaks ping-pong); full shared-hex support more
invasive.

### F67 — Auto-lander launches empty and ping-pongs (P1, high)  `[fixed: Code/Fix_LanderEmptyLaunch.lua]`
`UniversalRocketBase:IsCargoReady` (`UniversalRocket.lua:455-472`): `CheckAutoDepart()`
("wait for cargo") only yields the NON-blocking `"waiting_cargo"` issue
(`GetLaunchIssue` :883-885 returns no blocker); with an empty auto request
(nothing above export / below import threshold) every entry is 0 → status "ready" →
departs empty. Only mitigation: 1-hour sleep on asteroids (:227-229), none on Mars.
Endless empty round trips ~70 fuel each. **Fix:** wrap `IsCargoReady`: in auto mode with
CheckAutoDepart true and no non-fuel payload requested, return false (1-sol timer still
exits cleanly).

### F68 — Hourly auto-request ratchet unloads the lander's own cargo (P1, high)  `[fixed: Code/Fix_LanderCargoRatchet.lua]`
`CreateAutoCargoRequest` (`UniversalRocket.lua:1742-1755`, hourly): `to_transfer =
GetTotalCargoAvailable(...) - threshold`, but loaded cargo is NOT "available" — every
hour the request shrinks by what was just loaded; `requested` drops below what's aboard →
status "unloading" → drones haul the just-loaded cargo back out. Worst phase: request
collapses to {} with cargo aboard → full unload → F67 empty launch. Explains "loads
exotics, dumps them back, leaves with junk/nothing". **Fix:** in override, add own cargo
back before threshold compare; never lower `requested` below `cargo[res].amount` on the
automode target loc.

### F69 — Manual landing dumps the return fuel (P1, high)  `[fixed: Code/Fix_LanderReturnFuel.lua]`
`CmdLand` (`UniversalRocket.lua:414`) clears `arrival_loc` in manual mode →
`GetFuelResourceRequest` (:1639-1642) returns 0 → `CmdUnload` (:486-494) posts the
reserved return fuel (asteroid policy keeps half, `FlightPolicyDef.lua:208-211`,
`ConsumeFuel` :1664-1673) as EXCESS → drones unload it. No drones/hub on the asteroid →
stranded forever ("no fuel, no drones, can't send another lander"). **Fix:** override
`GetFuelResourceRequest`: lander type with no destination departing an asteroid keeps
`FuelResourceAmount` requested.

### F70 — Edit Payload silently refills from the policy template (P2, med-high)
`CargoRequestNew:RetrieveRequests` (`CargoRequestNew.lua:194-212`): rows with stored
request 0 are refilled from the flight-policy cargo template every dialog open (template
suppressed only during `CmdLoad`; every landing zeroes requests via `CmdUnload`). Mars→
asteroid template: 5 Drones, 20 Metals, 5 Polymers, 5 MachineParts, 5 Electronics, 3
extractor prefabs (`FlightPolicyDef.lua:93-131`). Legacy first-trip guard also broken
(`LanderRocketCargoRequest.lua:116` checks flag on wrong object). "Loads what it wants."
**Fix:** first-use flag on the transporter gating `resolve_loc_cargo_template`.

### F71 — Auto-export allocates capacity alphabetically (P2, med)
`CreateAutoCargoRequest` iterates `sorted_pairs` (`UniversalRocket.lua:1736-1758`) —
alphabetical: Concrete..Metals..Polymers before PreciousMetals/PreciousMinerals; WasteRock
is a legal export (`FlightPolicyDef.lua:393,401`). 80,000kg budget consumed by bulk before
valuables; 1-sol forced depart (`AutoDepartTimerSols`, :1773-1775) ships whatever loaded
first. **Fix:** value-ordered allocation (resupply price descending) in override.

### F72 — "No available Asteroid Landers" with a lander on the pad (P2, med)
`PlanetaryAsteroidVisitPossible` (`PlanetaryView.lua:433-444`) and
`GetRocketsForExpedition` (`PlanetUI.lua:1623-1651`) exclude any lander that is busy
(CmdLoad/CmdUnload) or has stale `arrival_loc` (payload dialog Cancel skips CancelFlight
during CmdLoad, `CargoRequestNew.lua:389-399`). No per-asteroid occupancy lock exists
(`IsDifferentAsteroidLocation` compares Map to MapDescriptor — never false,
`PlanetUI.lua:1696-1699`). **Fix:** accept landed re-targetable landers in both checks.

### F73 — Asteroid colonists idle outdoors; nothing shelters the suffocating (P1, med-high)  `[fixed: Code/Fix_ShelterReflex.lua]`
Chain: `MicroGHabitatAutoResolve:IsSuitable` requires `GetScoreFor > 0` ≈ `HasLifeSupport()`
(`MicroGHabitat.lua:154-156`, `Community.lua:367-398`) — any momentary life-support gap or
full habitat → colonist keeps `residence == false`; `Roam` (`Colonist.lua:1186-1205`) then
idles them OUTSIDE in vacuum; `CanService` requires residence == self (`MicroGHabitat.lua:130-132`);
and `Colonist:Idle` has NO seek-shelter branch on the oxygen timer (suffocation only
applies damage, `StatusEffects.lua:140-160`). Workers are safe inside the mine during
shifts; they die during idle stretches next to it. **Fix:** (a) habitat accepts residents
regardless of momentary life support; (b) Idle wrapper: outside > half of
OxygenMaxOutsideTime in vacuum → `SetCommand("Rest")`.

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
