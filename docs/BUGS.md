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
| F03 | Upgrade buffs leak & stack after salvage/demolish        | P1  | high | fixed  |
| F04 | Night-shift workers never return to work after midnight  | P1  | high | fixed  |
| F05 | Milestone completion crashes (NoTerraforming/NoPolitics) | P1  | high | fixed  |
| F06 | Philosopher's Stone mystery can hang forever             | P1  | med+ | fixed  |
| F07 | St. Elmo's Fire "free wisps" gives ~1/1000 power         | P1  | high | fixed  |
| F08 | Tourist star-rating applicant bonus inverted             | P1  | high | fixed  |
| F09 | Tourist Satisfaction drifts down (asymmetric thresholds) | P1  | high | fixed  |
| F10 | Faction funding conditions always error (BlueSun/Brazil/Russia) | P1 | high | retiring |
| F11 | Train wedges at platform (`table.remove` misuse)         | P1  | high | fixed  |
| F12 | "Low Storage" warning never fires for Food/maintenance   | P2  | high | fixed  |
| F13 | Command Center resource rows show no numbers             | P2  | high | fixed  |
| F14 | Domes Overview red low-stat highlight dead               | P2  | high | fixed  |
| F15 | Mystery 11 wisp RP rewards double/silent                 | P2  | high | fixed* |
| F16 | Mirror Sphere site usable after completion               | P2  | med  | fixed  |
| F17 | Dust Sickness damage not randomized                      | P2  | med+ | fixed  |
| F18 | Independence terraforming tech gives 10% not 20%         | P2  | med  | fixed* |
| F19 | Graphs "Consumed" caption omits maintenance              | P2  | med+ | fixed  |
| F20 | Morale tooltip shows unapplied +Comfort bonus            | P2  | high | fixed  |
| F21 | Train travel-time penalty includes station waiting       | P2  | med  | fixed  |
| F22 | `GetGridGlobalStorage` breaks Last Transmission gates    | P2  | med  | fixed  |
| F23 | Founder-gains-trait notification never fires             | P3  | high | fixed  |
| F24 | Dome pipe visuals corrupt on load (`MoveInside` typo)    | P3  | med  | fixed  |
| F25 | Tech description names wrong building (pre-1.0.6 saves)  | P3  | high | fixed  |
| F26 | Bombardment missiles fly parallel (cosmetic)             | P3  | med  | fixed  |
| F27 | Storage charge/discharge rate modifiers ignored (latent) | P3  | med  | fixed  |
| F28 | `Research:ReplaceTech` crashes (latent, mod-facing)      | P3  | high | fixed  |
| F29 | SA/sequence latents: label filter, workshift wait, Diggers swap | P3 | high | fixed*|
| F30 | Lake placement entombs RC builder + drones               | P1  | high | fixed  |
| F31 | Anomaly cave-in hardcodes UndergroundMap (cross-map)     | P2  | med  | fixed  |
| F32 | Dismissed warnings re-add instantly (not suppressable)   | P2  | med  | wontfix|
| F33 | Drone crash on small landscaping sites (nil-index)       | P2  | high | fixed  |
| F34 | Landscape nil-guard bundle (latent crash paths)          | P3  | med  | fixed* |
| F35 | Large Wind Turbine buff lost in old saves (fixup bug)    | P2  | high | fixed  |
| F36 | Universities overtrain geologists (unmanned extractors)  | P2  | high | fixed  |
| F37 | Ghost farm oxygen modifier survives salvage/demolish     | P1  | high | fixed  |
| F38 | Destroyed tunnels rejoin pathfinding after save/load     | P2  | high | fixed  |
| F39 | Second Artificial Sun ignored by solar panels            | P2  | high | fixed  |
| F40 | Dust Sickness infects Biorobots (androids)               | P2  | high | fixed  |
| F41 | Gene Forging tech has no effect                          | P2  | high | fixed  |
| F42 | Buildings placeable on active dust devils                | P3  | high | blocked|
| F43 | Layout construction bypasses tech locks                  | P3  | high | fixed  |
| F44 | One-hex track salvage can delete the entire track        | P1  | high | fixed  |
| F45 | Damaged tracks can't be salvaged at all (sort crash)     | P1  | high | fixed  |
| F46 | Trains dump cargo at stations with resource disabled     | P2  | high | fixed  |
| F47 | Track salvage refunds ~1 hex for whole track / 0 partial | P3  | high | fixed  |
| F48 | Station-connector savegame fixup no-op (paren misplaced) | P3  | high | blocked|
| F49 | Train minors bundle (palette, split kills trains, etc.)  | P3  | med  | fixed* |
| F50 | Auto-rockets kick approaching drones to Idle every hour  | P1  | high | fixed  |
| F51 | Transport-mode cache never sees new shuttles (homeless)  | P1  | high | fixed  |
| F52 | Colonists still walk ≤400m in vacuum past passages       | P1  | high | fixed* |
| F53 | Arrivals hike to unreachable "safety dome" and die       | P1  | high | fixed  |
| F54 | Switched-off shuttle hubs count as transport available   | P2  | med+ | fixed  |
| F55 | Open domes: drone access lost + unreachable-forever cache| P1  | med  | fixed* |
| F56 | Auto RC Transports never offload rockets                 | P2  | high | wontfix|
| F57 | Drone/transport minors bundle                            | P3  | med  | fixed* |
| F58 | Invisible residence reservations never expire            | P1  | high | fixed* |
| F59 | Freed housing never notifies homeless (12h retry lag)    | P2  | med  | fixed* |
| F60 | Dome free-space uses `working`, assignment `ui_working`  | P2  | med  | fixed  |
| F61 | Home dome's migration toggle blocks outbound shopping    | P1  | med+ | fixed  |
| F62 | Services reach 1 passage hop only, never trains          | P2  | high | wontfix|
| F63 | Universities invisible to emigration (no students)       | P2  | high | wontfix|
| D01 | Rockets don't auto-refuel/auto-export rare metals        | dsgn| high | opt-in fix |
| D02 | Dismissing "not working" warnings only silences them 2min| dsgn| med  | planned opt-in |
| F64 | Station demolition permanently leaks train prefabs       | P1  | high | fixed  |
| F65 | Station-at-tunnel never bridges the power grid           | P2  | med  | fixed  |
| F66 | Station↔tunnel connector hex ping-pong (never connects)  | P2  | med+ | fixed  |
| F67 | Auto-lander launches empty, ping-pongs Mars↔asteroid     | P1  | high | fixed  |
| F68 | Hourly auto-request ratchet unloads lander's own cargo   | P1  | high | fixed  |
| F69 | Manual landing dumps the return fuel (stranded landers)  | P1  | high | fixed  |
| F70 | Edit Payload silently refills from policy template       | P2  | med+ | fixed  |
| F71 | Auto-export fills capacity alphabetically (waste rock)   | P2  | med  | fixed  |
| F72 | "No available landers" while a lander sits on the pad    | P2  | med  | fixed  |
| F73 | Asteroid colonists idle outdoors; no shelter reflex      | P1  | med+ | fixed  |
| F74 | RC Transports can be ordered onto trade/refugee rockets  | P2  | high | fixed  |
| F75 | Last Transmission storage opinions inert; Oxygen reads Power | P2 | high | fixed |
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

### F03 — Upgrade buffs leak & stack after salvage/demolish  `[fixed: Code/Fix_UpgradeModifierLeak.lua stops new leaks; Code/90_SaveSanitizer.lua clears the ones already in a save]`
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
*Sweep implemented* in `Code/90_SaveSanitizer.lua` (LoadGame), on exactly that id pattern.
`ApplyUpgrade` mints the id as `string.format("%s_upgrade%d_mod_%d", self.handle, tier, i)`
(`Building.lua:1155`), so the handle in the id is the OWNING building's and nothing else in
the game writes ids of that shape — an entry whose handle no longer resolves to a live
object is by construction a leak. Containers swept: `UIColony`, every city, and every dome
(the three things `ApplyUpgrade` can target, `:1152`). Conservative: a handle that still
resolves to anything valid is left alone even though handles can in principle be recycled —
a missed leak is cheap, stripping a live building's bonus is not. Idempotent.
Probe: `SaveSanitizerUpgradeLeak` in `30_Probes_Wave3.lua`.

### F04 — Night-shift workers never return to work after midnight  `[fixed: Code/Fix_NightShiftWork.lua]`
`Lua\Units\Colonist.lua:1758-1768` — `ShouldLeaveForWork` window for shift 3
(`DefaultWorkshifts = {{6,14},{14,22},{22,6}}`, `_GameConst.lua:370`) evaluates as
`hour >= 21 and hour <= 25`; hours 0-1 unreachable (hour is 0-23, no wrap). Shift-1/2 get a
5-hour catch-up window; shift-3 colonists idle after midnight skip the rest of their shift.
Only gate that sends colonists to work (`Colonist:Idle` :1911). **Fix:** override
`Colonist.ShouldLeaveForWork` using modular distance `(hour - start) % 24`, incl. the
`leave_early_for_work` branch.

### F05 — Milestone completion crashes (NoTerraforming/NoPolitics)  `[fixed: Code/Fix_MilestoneCrash.lua]`
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

### F07 — St. Elmo's Fire "free wisps" gives ~1/1000 power  `[fixed: Code/Fix_WispRewards.lua]`
`Lua\Mysteries\Fireflies.lua:692` — `trap.el_prod_modifier:Change(#trap.fireflies)` missing
`* 1000`; sibling paths :346 and :479 have it. `ObjectModifier:Change` sets absolutely
(Modifiers.lua:321-331), so the broken value persists until wisp count changes (typically
next 4 AM). **Fix:** override `SetLightTrapMode`; in "free" branch multiply by 1000.

### F08 — Tourist star-rating applicant bonus inverted  `[fixed: Code/Fix_TouristApplicants.lua]`
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

### F10 — Faction funding conditions always error  `[retiring — premise falsified; final wontfix gated on PT-36]`
`Lua\Funding.lua:104-117` (`GetLastSolsFundingByType`) — `pairs(funding_gain_last_hours[hour])`
where the per-hour table only exists for hours with positive gain (`ChangeFunding` :52-65)
→ `pairs(nil)` error for most hours. Breaks `Data\FactionDef\BlueSun.lua:34,54`,
`Brazil.lua:42`, `Russia.lua:84` (export/tourism income gates never evaluate true).
**Fix:** redefine `Funding.GetLastSolsFundingByType` with `or empty_table` guards.
*QA audit 2026-07-25 — the premise is falsified in this engine build:* the wave-3 A/B
baseline drove the SHIPPED body with a stand-in whose per-hour tables were all nil (240
`pairs(nil)` iterations) and it returned 0 without erroring — this engine tolerates
`pairs(nil)` exactly as it tolerates `next(nil)`/`ipairs(false)` (the engine-facts list;
that tolerance was established AFTER this wave-1 fix was written). There is no observable
defect for the fix to repair, and its probe (`FactionFundingCheck`) can therefore never
discriminate: it PASSes in both A/B halves and is not evidence. The wrapper is harmless
(same values, `empty_table` instead of nil). **Decision for the user:** retire the fix
(preferred — one fewer full replacement to maintain) or keep it as hardening; either way
the faction-gate symptom this entry attributed to the error needs a different explanation
if it recurs.
*Planned retire, 2026-07-26:* `Fix_FactionFundingCheck.lua` is commented out of
`metadata.lua` (the file stays in the repo; rollback = re-add one line). Final `wontfix`
is gated on **PT-36** — an in-person console check on a real long-running save that the
SHIPPED function returns a number over empty income hours, confirming the synthetic
baseline evidence on organic save state. If PT-36 ever errors, re-enable the fix and
reopen this entry.

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

### F15 — Mystery 11 wisp RP rewards double/silent  `[fixed*: Code/Fix_WispRewards.lua — double-grant removed so display == granted; the "silent" half stays open, see below]`
`Lua\Mysteries\Fireflies.lua:466-469` — code after `SetCommand("Die")` unreachable
(`DoSetCommand` kills current thread, CommonLua\Classes\CommandObject.lua:340-378); actual
RP from Die destructor (:540-542). Batch destroy path (:676-688) grants again → trapped
wisps pay 200 RP each while notification says 100; later catches pay 100 silently. **Fix:**
patch `Firefly.Drain` to notify/grant before `SetCommand("Die")` and remove the destructor
double-grant (or drop batch grant) so display == granted.
*Implemented half:* the batch grant is dropped, leaving the Die destructor as the single
payer — every wisp is now worth exactly the 100 RP the notification claims. *Open half:*
wisps caught AFTER the mode was set to "destroy" are drained one at a time and still pay
silently (no per-wisp notification). That is a UI addition rather than a defect repair
(FIX_POLICY §4), so it is deliberately not shipped.

### F16 — Mirror Sphere site usable after completion  `[fixed: Code/Fix_MirrorSphereSite.lua]`
`Lua\Mysteries\MirrorSphere.lua:823` — guard `self.progress == 100`, but scale is
0..`max_progress` (2^22; see :724-726, :734) → lockout never triggers; players can waste
drone work on finished site. **Fix:** override `StartAction`-holder method, compare
`self.progress >= self.max_progress`.
*Implemented as sketched* (pre-wrapper on `MirrorSphereBuildingBase:StartAction`, declared
at :813-870), with one correction: `MirrorSphereBuildingBase` has no `max_progress` member
— the file-local constant is published only on the `MirrorSphere` unit class (`:69`), so
the fix reads `MirrorSphere.max_progress` and deactivates if that is gone. Cancelling a
running action (`self.action == action`) is still let through, since that branch is a
`StopAction` and is unrelated to progress.

### F17 — Dust Sickness damage not randomized  `[fixed: Code/Fix_DustSicknessDamage.lua]`
`Data\TraitPreset.lua:87-91` — `local change = 5 + colonist:Random(trait.param)` dead;
always deals flat `trait.param` (10)/sol instead of 5-14. **Fix:** patch
`TraitPresets.DustSickness.daily_update_func` (data patch at ClassesPostprocess — very
mod-friendly).
*Implemented as sketched*, but hooked on `DataLoaded`/`DataChanged` rather than
`ClassesPostprocess`: presets are read from `Data\` during `LoadData`
(`CommonLua\Dlc.lua:640-662`), after mod code has loaded, so the preset does not exist
at `ClassesPostprocess`. The corrected body uses the `change` the shipped code already
computes (5 + `colonist:Random(param)` = 5-14 for param 10). Note the mod sandbox has no
introspection, so an already-hotfixed `daily_update_func` cannot be told from the broken
one; the fix deactivates only if the preset or its `param` is missing.

### F18 — Independence terraforming tech gives 10% not 20%  `[fixed*: Code/Fix_IndependenceTerraforming.lua — the preset half; already-researched saves keep 10%, see below]`
`Data\TechPreset.lua:4798-4812` — `param1 = 20` ("decrease percent") but
`Effect_ModifyLabel Amount = -10` on `Consts.SpecialProjectResourcesModifier` (100-based,
consumed `Lua\SpecialProjects.lua:105`). All sibling Independence techs have param == amount.
**Fix:** patch the effect's `Amount = -20` before research (ClassesPostprocess), only if
tech not yet researched — else apply delta modifier.
*Sibling evidence enumerated:* `Independence_Adaptivity` param1 5 / Amount -5;
`Independence_MartianbornPerformance` param1 5 / Percent 5; `Independence_RocketCapacity`
param1 30000 / Amount 30000; `Independence_Research` param1 20 / Amount 20. Only
`Independence_TerraformingProjects` disagrees with itself.
*Implemented as the preset half only.* The patch runs from `OnMsg.DataLoaded` (+
`DataChanged`) and finds the effect by what it does (Label "Consts", Prop
"SpecialProjectResourcesModifier"), not by index; an Amount already at -20 leaves the fix
inactive.
*Open half — saves where the tech is ALREADY researched keep the 10%.*
`Effect_ModifyLabel:OnApplyEffect` (`Lua\MarsGameEffects.lua:161-178`) computes
`amount = self.Amount * scale` at research time and stores a Modifier on the colony keyed by
the effect object; that stored Modifier is what the save carries, and correcting the preset
afterwards does not touch it. A repair would be idempotent (same key, so re-applying
replaces rather than stacks), but `OnApplyEffect`'s `parent` argument also determines the
Modifier's `id`, and getting that wrong would leave an unidentifiable modifier in every
affected save. Deferred to a later sanitizer pass rather than shipped untested for a
10-point discount.
Probe: `IndependenceTerraforming` in `40_Probes_Wave4.lua`.

### F19 — Graphs "Consumed" caption omits maintenance  `[fixed: Code/Fix_GraphConsumedCaption.lua]`
`Lua\X\ColonyControlCenter.lua:180-188` vs `ResourceTracking.lua:162` — caption uses
consumption only; plotted series adds maintenance. Near-zero caption next to a tall bar for
Machine Parts/Electronics/Metals/Polymers. **Fix:** wrap `City.GetColonyStatsButtons`,
correct the caption closure.
*Implemented as sketched.* Post-wrapper on `City:GetColonyStatsButtons`; the shipped
function builds the whole descriptor table and the wrapper rewrites only the caption
closure of the stockpile-resource produced/consumed panels. The panel is found by
STRUCTURE — its `data[2]` must be `city.ts_resources[id].consumed`, the very series the
caption describes — so a rearranged UI fails to match and deactivates the fix instead of
relabelling the wrong graph. The replacement keeps the shipped translation (T id 8979) and
sums the two raw accumulators before scaling once, which is what the plotted series does
(it passes raw values with `scale = const.ResourceScale`).
Probe: `GraphConsumedCaption` in `40_Probes_Wave4.lua`. Playtest: PT-43.

### F20 — Morale tooltip shows unapplied +Comfort bonus  `[fixed: Code/Fix_MoraleComfortTooltip.lua]`
`Lua\Units\Colonist.lua:2983-3007` (tooltip) vs :3963-3969 (`UpdateMorale`, bonus
deliberately commented out: "remove for comfort policy to work") — tooltip still lists
"Living in luxury +5" for Comfort ≥ 70; listed effects don't sum to shown Morale. **Fix:**
override `Colonist.UIStatUpdate`; skip `value >= high` row for Comfort only.
*Confirmed and narrowed:* `UpdateMorale` keeps the LOW-Comfort penalty (`:3967-3969`) and
drops only the high-Comfort bonus (`:3963-3966`), while the tooltip loop (`:2985-3008`)
prints a row for every stat on `value < low or value >= high` alike. Exactly one row is
wrong. The shipped comment names the removal as intentional, so only the tooltip is
changed and no Morale number moves.
*Implemented differently, on better evidence:* the sketch's "override `UIStatUpdate` and
skip the row" is not reachable — the row is built inside the ~130-line `win.GetRolloverText`
closure the shipped function installs, and the `low`/`high` bounds it compares against are
read once for all stats (`:2983-2984`), so there is no per-stat seam to hook. Instead the
fix post-wraps `UIStatUpdate`, then wraps the closure it just installed, and answers the one
comparison the row hinges on: for the duration of that call the colonist carries an
instance-level `GetProperty` reporting Comfort as one below the high mark when it is at or
above it. The value only ever moves DOWN to just under the threshold, so the low-Comfort
penalty row is untouched, no other stat is affected, the override is removed in the same
call under `pcall`, nothing in the builder yields, and only Morale tooltips are wrapped.
Probe: `MoraleComfortTooltip` in `40_Probes_Wave4.lua`. Playtest: PT-43.

### F21 — Train travel-time penalty includes station waiting  `[fixed: Code/Fix_TrainWaitTime.lua]`
`Lua\Units\ColonistTransport.lua:493,511,551-569` — `ticket.start_wait` set on reaching
platform, never reset at boarding; Comfort "travel time" penalty and train/track
"spent time" stats (TransportStatistics.lua:31-45) count waiting (double-counted vs
station stat). *(QA audit 2026-07-25 struck the "partially bypasses LuxuriousTrains"
claim — the tech gates the ENTIRE ChangeComfort at :555-557, so nothing bypasses it;
post-research the comfort half is simply moot.)* **Fix:** reset
`transport_ticket.start_wait = GameTime()` at boarding.
*Implemented as a full replacement, not a wrapper, because no wrapper can run in
time:* `Colonist:BoardVehicle` (`:503-528`) is issued as a command
(`Train.lua:967`) and the ride ends with `SetCommand("ExitVehicle")` killing the
thread inside the blocking loop — a post-wrapper would never run at all (the
command-method rule), and a pre-wrapper would erase the wait before `:511` credits
it to the station. The copy is byte-identical except the one added line, placed immediately after the
station is paid, so the station keeps the full wait and only the boundary between "waiting"
and "travelling" moves to where the colonist actually boards.
Probe: `TrainWaitTime` in `40_Probes_Wave4.lua`. Playtest: PT-43.

### F22 — `GetGridGlobalStorage` breaks Last Transmission gates  `[fixed: Code/Fix_GridGlobalStorage.lua]`
`Lua\ResourceOverview.lua:880-899` — zero-demand map returns sentinel `1000 sols` and
per-map sols are **summed**; once Underground loads, `== 0` conditions in
`Data\FactionDef\LastTransmission.lua:103-184` unsatisfiable, `> 2 sols` always true.
**Fix:** redefine: zero-demand map contributes 0; combine with Min (or demand-weighted).
*Correction to the entry:* the sentinel is `1000 * const.HourDuration` — 1000 **hours**,
not sols (`const.HourDuration` = 30000ms; `const.DayDuration` = 720000, and the shipped
"2 sols" threshold is 1440000 = 48 hours, `ClassDef-Conditions.generated.lua:2030-2031,
:2044`). It is ~41 sols, still ~20x the threshold, so the conclusion stands.
*Implemented as demand-weighted (the entry's own second option), not "contributes 0".*
The replacement aggregates the INPUTS — sum stored and sum required across the two cities
the shipped function names — and takes a single ratio. Three deliberate properties:
`stored == 0` returns 0 (this is what makes `== 0` reachable, and it is literally true);
the "unlimited" sentinel survives for the case it was written for, a colony with real
storage and no demand anywhere; and `GetGridGlobalStorageInSols` is left untouched, since
its per-city semantics are self-consistent and it is a public global. Arithmetic is copied
exactly, truncating `/` included, so a single-map colony faces the identical threshold.
Asteroid maps are deliberately NOT added to the aggregate — that would change how hard the
shipped conditions are to satisfy (FIX_POLICY §4). Replacing the global works because
`ModEnvMeta.__newindex` rawsets into the real `_G` (`Mod.lua:1557-1563`) and the callers
are generated closures resolving the name at call time; apply() reads the global back to
confirm the write landed.
*What fixing this exposed:* the six Last Transmission conditions this entry names are ALSO
broken by a second, independent defect that this fix alone would not have cured — filed and
fixed as **F75** below.
Probe: `GridGlobalStorage` in `40_Probes_Wave4.lua`. Playtest: PT-42.

## P3 — cosmetic / latent / mod-facing

### F23 — Founder-gains-trait notification never fires  `[fixed: Code/Fix_FounderTraitNotification.lua]`
`Lua\ColonyViability.lua:282-295` — array `FounderGainsTraitCategories` indexed with group
string → always nil. Handler can't be replaced (OnMsg is additive; original is dead and
harmless). **Fix:** add our own `OnMsg.ColonistAddTrait` with a proper set
(`{Positive=true,Negative=true,Specialization=true}`) + dedupe via existing-notification check.
*Implemented exactly as sketched.* Conditions copied verbatim from the shipped handler,
`init` guard and single-notification guard included. Handlers run in registration order and
the shipped one is registered first, so a future game hotfix that repairs the array makes
the shipped handler add the notification and its own `not FindNotification(...)` guard is
then what stops ours from adding a second.
Probe: `FounderTraitNotification` in `40_Probes_Wave4.lua`. Playtest: PT-44.

### F24 — Dome pipe visuals corrupt on load (`MoveInside` copy-paste)  `[fixed: Code/Fix_DomePipeMoveInside.lua]`
`Lua\LifeSupportGrid.lua:304` — passes `dome` where electricity twin
(`ElectricityGrid.lua:291`) passes `self` to `DestroyConnection`. Triggered from
`Dome:OnLoad` (Dome.lua:896-899) repair sweep; stale plugs/connections block future
`ConnectPipe` visuals. **Fix:** override `LifeSupportGridObject.MoveInside`, `dome`→`self`.
*Confirmed:* `WaterGrid.DestroyConnection(pt1, pt2, building1, building2, test)`
(`LifeSupportGrid.lua:157-161`) takes the owner of `pt1` as `building1`, and the two loops
are otherwise line-for-line identical. So the moving building is never told its own
connection at `pt` is gone and the dome is told about a hex it does not own.
*Implemented as a full replacement of `LifeSupportGridObject:MoveInside`
(`:282-316`)*, byte-identical except the one argument: the call is inside a loop in the
middle of the function, so no wrapper position reaches it, and wrapping
`WaterGrid.DestroyConnection` instead cannot work — a wrapper there has no way to know
which caller handed it the wrong owner. The shipped `assert(IsKindOf(dome, "Dome"))` is
dropped from the copy (asserts do not unwind; the statements after it already require a
real dome).
Probe: `[install]`-free — the fix is verified through F24's own playtest, PT-44, because
the behaviour needs a real dome absorbing a real pipe-connected building.

### F25 — Tech description names wrong building (pre-1.0.6 saves only)  `[fixed: Code/Fix_TechDescriptionBuilding.lua]`
`Data\TechPreset.lua:1486` (`UndergroundLargeDome`, gated `not UndergroundRework106`) —
description says "Jumbo Cave Reinforcements", tech unlocks `UndergroundDomeMedium`.
**Fix:** ClassesPostprocess description patch. Low priority (legacy saves only).

Confirmed, and which half is wrong is unambiguous: the preset's own `display_name` is
"Underground Medium Dome" (`:1487`), its single unlock is
`Effect_TechUnlockBuilding{ Building = "UndergroundDomeMedium" }` (`:1491-1493`), that
building's own display_name is "Underground Medium Dome"
(`Data\BuildingTemplate\UndergroundDomeMedium.lua:22`), the `<buildinginfo('UndergroundDomeMedium')>`
tag in the same sentence is correct, and the rest of the sentence ("A medium-sized Dome")
describes the unlocked building. Only the bolded name is wrong.

Patched from `OnMsg.DataLoaded` (+ `DataChanged` for editor reloads) rather than
ClassesPostprocess — presets do not exist when mod code loads.

**Localisation note (deliberate):** the replacement is `T(841885693955, "<corrected
English>")` — the *same* translation id. A localised build resolves the id in its own
translation table and is completely unaffected; only an English build, which falls back to
the literal, sees the correction. Minting a fresh T would have replaced every translated
description with an English paragraph — a worse regression in every other language than the
one wrong word. The fix declines (with a reason) if the literal it expects is not there.

### F26 — Bombardment missiles fly parallel (cosmetic)  `[fixed: Code/Fix_BombardmentSpread.lua]`
`Lua\Bombardment.lua:82-83` — deviated `spawn_dir` computed, then `spawn_pos` uses base
`dir` (compare Meteors.lua:106-107). Mystery 7 bombardments look uniform. **Fix:** override
`WaitBombard`, use `GenerateDir(dir, angle)` in `spawn_pos`.

Confirmed exactly as tracked. `spawn_dir` is assigned at `:82` and never read again
anywhere in the 100-line function; `GenerateDir(dir, angle)` exists solely to jitter the
elevation by up to ±10° around the volley angle (`:38-50`), so the intent of `:82` is
unambiguous and `:83` names the wrong variable.

*Cost recorded honestly:* this needed the pack's sixth full replacement, and it is the
largest — 100 lines — for its least valuable defect. There is no seam: by the time any
hook can reach the missile, `missile:SetPos(spawn_pos)` has already placed it (`:85`) and
the visual axis is derived from the same local (`:93-96`), so a post-hoc correction would
leave a missile flying along one line while pointing down another. Two file-locals had to
be copied in as well — `GenerateDir` (`:38-50`, verbatim, so it consumes the same
`SessionRandom` draws in the same order and volleys stay deterministic) and `travel_dist`
(`:53`). One deliberate divergence: the shipped `assert(false, "Failed to find bombard
pos!")` at `:59` is dropped, since `assert` does not unwind mod code — the `return false`
beside it is what handles the case and is kept. **Re-verify this copy on every game
update** (FIX_POLICY §1.5).

### F27 — Storage charge/discharge rate modifiers ignored (latent)  `[fixed: Code/Fix_StorageRateModifiers.lua]`
`Lua\ElectricityStorage.lua:47-63`, `Lua\LifeSupportStorage.lua:25-42,131-148` —
`OnModifiableValueChanged` fires for `max_*_charge/discharge` but never copies to
`element.max_charge/max_discharge` (read in SupplyGrid.lua:164-170). No vanilla modifier
touches rates; breaks the documented modding surface. **Fix:** post-hook the three
`OnModifiableValueChanged`s, copy both fields before `UpdateStorage()`.
*Implemented as sketched, with the copy AFTER the shipped body rather than before it* — the
shipped body ends with its own `element:UpdateStorage()`, so a post-wrapper that copies the
rates and calls `UpdateStorage()` again is the smallest change that gets the new rates into
the same pass. Exact fields confirmed: `NewSupplyGridStorage` (`SupplyGrid.lua:64-76`) seeds
`max_charge`/`max_discharge` once at creation and `SupplyGridElement:UpdateStorage`
(`:167-168`) is what reads them every tick. The wrapper no-ops unless the property that
changed is one of the two rates, and each of the three classes is wrapped independently, so
one missing target cannot take the other two down.
Probe: `StorageRateModifiers` in `40_Probes_Wave4.lua`.

### F28 — `Research:ReplaceTech` mishandles the field counter (latent)  `[fixed: Code/Fix_ReplaceTechCount.lua]`
`Lua\Research.lua:715` — `if not next(g_TechFieldResearchedCount[field_id] == 0)` →
`next()` applied to a boolean. No vanilla caller; hits mods/storybits/console. Correct
pattern at :246-249. **Fix:** override `Research.ReplaceTech`
branch with `if g_TechFieldResearchedCount[field_id] == 0 then ... = nil end`.
*Title corrected — the pack does not claim a crash it has not observed (the F10 lesson).*
Either `next(false)` raises, in which case the function dies before the very next line's
`self:SetTechResearched(tech_id_new, "notify")` and the replacement tech is never marked
researched; or this engine tolerates it as it tolerates `next(nil)`, in which case it
returns nil, `not nil` is true, and the field's counter entry is dropped even while techs in
that field are still researched. Both are wrong; both are repaired by writing the comparison
`Research:SetTechUndiscovered` (`:246-249`) already writes. The probe reports whichever it
observes. Implemented as a full replacement of `ReplaceTech` (`:684-720`) since the defect is
mid-function; the FOUR shipped `assert` lines (`:686/:690/:711/:713` — an earlier count of
three missed one) are dropped from the copy (they cannot unwind, and `if not status then
return end` right after the first is the real guard). *(QA repair 2026-07-25: the `:690`
assert was load-bearing through its ARGUMENT — `tech_def.group` raises on an unknown
`tech_id_new` BEFORE any state mutation; the copy now keeps that ordering with an explicit
`if not tech_def then return end` guard.)*
Probe: `ReplaceTechCount` in `40_Probes_Wave4.lua`.

### F29 — Sequence-system latents (mod-facing bundle)  `[fixed*: Code/Fix_SequenceLatents.lua — items 1 and 3; item 2 deliberately not fixed, see below]`
1. `Lua\Sequences\SA_Filters.lua:30-40` — `SA_GetLabelToRegister` ignores
   `random_count`/`random_percent` (returns full list after shuffle). No shipped user.
2. `Lua\Sequences\SA_Gameplay.lua:2705` — `SA_WaitMarsTime` *generated-code* path inverts
   the workshift wait (`==` should be `~=` vs interpreted `StopWait` :2626). No shipped user.
3. `Lua\Mysteries\Diggers.lua:91-95` — broken two-variable swap; unreachable with shipped
   defaults, bites subclasses. **Fix:** all three are small overrides; ship for modder benefit.
*Item 1 fixed:* the shipped body computes `count`, shuffles (which exists only to make a
truncation fair) and then returns the whole list — `count` is dead. The action's own editor
text advertises both parameters (`:20-27`). The replacement truncates to `count`.
*Item 3 fixed:* `local t` is saved and never read, so `self.pre_hit_ground_t_2 =
self.pre_hit_ground_t` copies the value the line above just overwrote and both fields end up
holding the LARGER one. The replacement assigns `t`.
*Item 2 deliberately NOT fixed.* It is real — the generator emits `while CurrentWorkshift ==
target_workshift ...`, the inverse of the interpreted `StopWait` (`:2617-2631`) — but it is a
CODE GENERATOR: it runs when a sequence is compiled in the Mod Editor, not while playing,
and mod code cannot regenerate sequences that were already compiled. Repairing it would mean
replacing the whole multi-branch generator for a path with no shipped user and no runtime
effect. Revisit only if a scenario author reports it.
Probe: `SequenceLatents` in `40_Probes_Wave4.lua` (covers items 1 and 3).

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

### F31 — Anomaly cave-in hardcodes UndergroundMap (P2, med)  `[fixed: Code/Fix_AnomalyCaveInMap.lua]`
`Scenario\UndergroundAnomalies.generated.lua:240` (same in Cave_Of_Wonders data):
`TriggerCaveIn(UndergroundMap, anomaly_pos)` while every sibling action uses the
sequence-local `map` (sequence runs on the anomaly's own map, `Anomaly.lua:293-303`).
Wrong-map rubble; crash risk if `UndergroundMap` false (`CaveInRubble.lua:101`).
**Fix:** wrap `TriggerCaveIn(map, pos)`: reject `map.mapdata.Environment ~= "Underground"`.

Confirmed, and **wider than recorded — eight call sites, not two**:
`UndergroundAnomalies.generated.lua:240`, `BuriedWonder_Jumbo_Cave.generated.lua:340,539,769`,
`BuriedWonder_Jumbo_Cave_106.generated.lua:339,538,768`, and
`BuriedWonder_Cave_Of_Wonders.generated.lua:430` (which passes the global twice — also to
`FindCaveInLocation`). The engine's own callers do it correctly: `Marsquake.lua:266`
passes the local `map`, `:287` passes `CurrentMap`.

The crash risk is confirmed and named: `UndergroundMap` is a **GameVar defaulting to
`false`** (`RandomMapGenerator_Picard.lua:263`) which stays false whenever the underground
map was never generated — `GenerateAdditionalMaps` returns immediately under the "No
Underground and Asteroids" game rule (`:266`). `TriggerCaveIn` guards its `pos` argument
(`CaveInRubble.lua:95-98`) and then calls `map:MapFindNearest` (`:101`) with no check at
all; handed `false` that raises, and the raise takes the running anomaly sequence with it.
Same shape as F66: the function states the invariant for one argument and does not enforce
it for the other.

*Implemented differently, on better evidence:* the sketch's environment test would break
the game's own cave-ins — `Marsquake.lua:266,287` trigger them on whatever map the quake is
on, so rejecting non-`Underground` environments there would silently cancel every marsquake
cave-in. The defect is an unchecked argument, not a wrong environment, so the fix checks
only the argument: a chained wrapper on the global `TriggerCaveIn` that declines a map it
cannot use, exactly as the shipped body declines a missing `pos`. When the map is real,
nothing changes.

**Not fixable from Lua, recorded:** the wrong-map half. Those eight calls are baked into
generated sequence code (`Data\Scenario\*.lua` `'expression'` strings, e.g.
`UndergroundAnomalies.lua:195`) compiled when the scenario preset loads, with no hook for
the map argument; and `TriggerCaveIn` cannot recover the sequence's map from the inside,
since it receives only a position and positions carry no map. The wrapper deliberately does
**not** substitute `CurrentMap` — rubble on the wrong map is a worse failure than no
rubble, and guessing is not licensed by FIX_POLICY §4.

### F32 — Dismissed warnings re-add instantly (P2, med mechanism-certain)  `[wontfix — the game hotfixed the one defective mechanism; the residual UX gap is D02]`
Object-status notifications (`NotWorkingBuildings`, `DestroyedInfrastructure`,
`RoverDamaged`) are not `Suppressable` (`Data\NotificationPreset.lua:771-781`); any
`SetWorking()` on any building re-creates them (`BaseBuilding.lua:165-169` →
`Notifications.lua:231-236`). Dismissal while a persistent bad state exists → instant
re-add. Matches lake-victim report. **Fix:** set `Suppressable = true` +
`SuppressTime = const.DayDuration` on those presets (data patch, very compat-friendly).
*Blocked 2026-07-25 (wave 3) — code re-read, entry no longer matches:*
* **`NotWorkingBuildings` already carries the fix.** `Data\NotificationPreset.lua:636-655`
  now has `Suppressable = true` and `SuppressTime = 120000`. This is the one preset the
  described mechanism actually applies to — `BaseBuilding:SetWorking` →
  `UpdateNotWorkingBuildingsNotification` (`:137-139`) → `UpdateObjectInNotification`
  re-adds it on every working-state change — and the game has hotfixed it. Suppression
  works exactly as the entry assumed: `TryDismiss` (`NotificationUI.lua:67-75`) sets
  `dismissed` then removes, `RemoveNotification` (`Notifications.lua:87`) opens the
  suppression window, and `AddNotification` (`:41-43`) refuses while it is open.
* **The other two are not re-added at all.** `DestroyedInfrastructure` is added once, at
  the moment of destruction, behind a flag that is cleared in the same statement
  (`Building.lua:1474-1478`; also `DestroyBuildingImmediate` :1377 and `BaseRover` :342),
  and removed on rebuild/demolish. `RoverDamaged` is added from
  `BaseRover:MalfunctionNotification` (`:216-218`) and removed by the malfunction
  destructor (`:246-248`). Both are one-shot event adds with no periodic path, so a
  dismissal holds until a genuinely new event — which is the correct behaviour. Making
  them `Suppressable` would suppress *new* destructions and malfunctions for the window,
  i.e. hide real events, with no defect to justify it (FIX_POLICY §4).
**Disposition — CLOSED `wontfix` 2026-07-26 (user decision).** As a defect there is
nothing left: the reported mechanism is hotfixed by the game, and the other two presets
work as designed. What remains is a real but *by-design* annoyance for PERMANENTLY broken
buildings, fully traced this session: the suppression window is **2 minutes of REAL time**
(`SuppressTime = 120000`, preset sets no `GameTime` so `NotificationPreset:GetTime()`
→ `RealTime()`, `NotificationPreset.lua:126-128`), suppression is **per-notification-id**
(the whole category goes quiet, including genuinely new breakages,
`Notifications.lua:41-43/141-146`), and there is no per-building "I know" — so an
unfixable building (the F30 lake-entombment case) re-nags every 2 real minutes forever.
That gap is filed as **D02** (per-object acknowledgment, planned opt-in module) — see its
entry; cadence verification is **PT-38**.

### F33 — Drone crash on small landscaping sites (P2, high)  `[fixed: Code/Fix_SmallLandscapeSites.lua]`
`Landscape\LandscapeConstructionSiteBase.lua:186-190`: `for i = 1, top_count do
top_dests[i] = dests[i].dest` — nil-index when site periphery has < 5 hexes (tiny
clear/paint blobs) → error in drone command thread. **Fix:** `Min(top_count, #dests)`.
*Implemented as sketched*, as a full replacement of `GetClosestDests` (`:178-192`) — the
fault is inside the loop, so neither a pre- nor a post-wrapper can reach it. Confirmed
`drone_dests_cache` holds only PERIPHERY hexes (`GameInit` :47-64, `if border then`), which
is what makes a small blob fall under five, and that the sole caller is `DroneApproach`
(`:194-205`), running in the drone's own command thread — so the raise kills that thread.
The shipped `assert(self.drone_dests_cache)` is dropped from the copy (assert does not
unwind in mod code); with the clamp, a missing cache yields an empty list, which
`drone:Goto` already handles. Probe: `SmallLandscapeSites` in `30_Probes_Wave3.lua`.

### F34 — Landscape nil-guard bundle (P3, med/latent)  `[fixed*: Code/Fix_LandscapeUnitFilter.lua — item (d) only; (a)(b)(c) verified NOT actionable, see below]`
(a) `ClearWasteRockConstructionSite:GameInit` (`:60-63`) unguarded `Landscapes[self.mark]`;
(b) `LandscapeMarkEnd` (`Landscaping.lua:200-206`) unguarded nil mark;
(c) lake `landscape_grid` overlap only assert-guarded (`LandscapeConstructionController.lua:502-507`,
release asserts stripped → silent corruption);
(d) `LandscapeForEachUnit` dead embark filter (`Landscaping.lua:455-469`).
*Re-read 2026-07-25 (wave 3). Only (d) is a defect that reaches the player, and it is not
merely a nil guard:*
* **(d) — FIXED.** The local `filter_embark` is built and then `callback` is handed to
  `Landscape_ForEachObject` instead. That it is a copy-paste slip and not a decision is
  settled twice over: `LandscapeForEachStockpile` immediately above (`:436-451`) is written
  identically and DOES pass its `filter_parent`; and the ordinary construction site applies
  exactly the same Embark rule to exactly the same question —
  `ConstructionSite:GetUnitsUnderneath` passes `exit_impassable_filter` = `obj.command ~=
  "Embark"` (`ConstructionSite.lua:1713-1720`). Two things were lost: the Embark exclusion
  and the `passed` de-duplication every sibling keeps. Live consumer:
  `LandscapeConstructionSite:GetUnitsUnderneath` (`LandscapeConstructionSite.lua:21-27`) →
  `ScatterUnitsUnderneath` (`ConstructionSite.lua:1722-1740`) →
  `SetCommand("ExitImpassable")`, so landscaping over a boarding point drags colonists out
  of the vehicle they are entering, repeatedly for any duplicate. Full replacement of the
  global, reproducing the file-local `foreach_params_unit`.
  Probe: `LandscapeUnitFilter` in `30_Probes_Wave3.lua`.
* **(a) — not actionable.** Unreachable as written: `GameInit` is a combined method
  (`DefineCombinedMethod("GameInit", "procall", "Object")`), so even if `Landscapes[self.mark]`
  were nil the error is swallowed by `procall`; and no shipped path creates the site without
  its mark. Adding a guard means replacing a method for no player-visible effect.
* **(b) — not actionable.** Both shipped callers are already guarded:
  `LandscapeConstructionController:Deactivate` returns early on `not landscape`
  (`:242-246`) before reaching `LandscapeMarkEnd` (`:251`), and `:515` runs only after
  `LandscapeMarkStart` returned a landscape (`:493-496`). Latent / mod-facing only.
* **(c) — not a guard, a redesign.** `assert(landscape_grid:get(sx, sy) == 0)` followed by
  an unconditional `set` means an overlapping mark is silently overwritten. Making it safe
  requires deciding what to do with the contested hexes (skip them, and the site has a
  hole; refuse the placement, and the player loses an action that works today). That is a
  behavior change, not a nil guard (FIX_POLICY §4). Left recorded.

### F35 — Large Wind Turbine buff lost in old saves (P2, high)  `[fixed: Code/90_SaveSanitizer.lua]`
Current `FrictionlessComposites` data is CORRECT (`Data\TechPreset.lua:796-821` targets
WindTurbine, WindTurbine_Large, WindTurbine_Diffuser). But the migration fixup
`SavegameFixups.WindTurbine_Large_ReapplyModifiers` (`Buildings\WindTurbine.lua:78-88`)
only reapplies the `WindTurbine_Diffuser` label — never `WindTurbine_Large`. Saves that
researched the tech pre-hotfix keep unbuffed Large Turbines forever. Matches review
report ("polymer upgrade works now, frictionless doesn't"). Rotation lock is by design
(`can_rotate_during_placement = false`). **Fix:** one-shot LoadGame sweep: if tech
researched and no colony label-modifier for `WindTurbine_Large.electricity_production`,
add it (mirror the fixup, corrected).
*Implemented as sketched*, in the consolidated sanitizer, and generalised one step: the
pass is driven by the tech preset's OWN `Effect_ModifyLabel` entries rather than a
hard-coded label list, so it restores whatever the tech says it grants (today: all three of
WindTurbine / WindTurbine_Large / WindTurbine_Diffuser at +100% `electricity_production`)
and does nothing if a game update changes them. Confirmed the three labels are disjoint —
a building is added to a label named after its own class (`Building:AddToCityLabels`,
`Building.lua:427-443`), and the three turbine templates are separate classes — so nothing
else was covering Large turbines. Conservative: any existing percent modifier for that
property on that label counts as "already buffed" and the label is skipped, so the pass
cannot double-buff, and it is idempotent across loads.
*QA audit 2026-07-25 — one HIGH defect found and repaired:* the pass originally hooked
`OnMsg.LoadGame`, but `UnpersistGame` fires `Msg("LoadGame")` BEFORE `FixupSavegame`
(`CommonLua\Savegame.lua:810-813`). On the first load of a save the shipped
`WindTurbine_Large_ReapplyModifiers` fixup had not yet been applied to, the pass ran ahead
of it, saw the Diffuser label bare, buffed it — and then the fixup unconditionally added
its own +100% (`WindTurbine.lua:80-87` has no already-buffed check): +200% baked into the
save permanently. Repair: the handler now hooks `OnMsg.PostLoadGame`, which fires after
fixups (`Savegame.lua:813`); the "any percent modifier → skip" guard then holds in every
ordering. Also hardened while in there (latent, dormant today): `amount` is now scaled via
`GetModifiablePropScale(prop)` the way the live tech apply scales it (`Tech.lua:298-301`) —
all three shipped effects have Amount 0, but the pass is preset-driven by design. The
LoadGame-vs-fixup ordering cannot be discriminated by the probe (it drives the pass
directly); PT-35 case C remains the only true fixture.
Probe: `SaveSanitizerTurbineBuff` in `30_Probes_Wave3.lua`.

### F36 — Universities overtrain geologists (P2, high behavior-confirmed)  `[fixed: Code/Fix_UniversityOvertraining.lua]`
`City:GetNeededSpecialist` (`City.lua:561-593`) counts every `ui_working` workplace incl.
extractors (`specialist="geologist"`, `max_workers=4`); ExtractorAI only sets
`g_ExtractorAIResearched`, used solely to silence a construction warning
(`BaseExtractor.lua:60-68`) — worker demand never zeroed. Auto-mode universities
(`MartianUniversity.lua:24-29`) keep producing geologists for unmanned extractors.
**Fix:** wrap `GetNeededSpecialist`: skip extractor workplaces when ExtractorAI researched
(match its actual gameplay meaning).
*Implemented differently, on better evidence:* `g_ExtractorAIResearched` is the wrong key —
its only use in the whole codebase is silencing that construction warning. The tech's real
effect is `Effect_ModifyLabel automation = 1` / `auto_performance = 50` on the
MetalsExtractor and PreciousMetalsExtractor labels (`Data\TechPreset.lua:1050-1075`), and
`automation > 0` makes `Workplace:GetWorkshiftPerformance` return `auto_performance`
regardless of staffing (`Workplace.lua:197-199`). The fix therefore excludes any workplace
with `automation > 0` from the demand tally — precise, and correct for automated workplaces
generally. Full replacement of `City:GetNeededSpecialist` (the gate is inside the
accumulation loop). Fixing this one function covers all three consumers: `CanTrain`'s
"train as needed" policy, the auto specialization pick on graduation, and the infopanel
list.

### F37 — Ghost farm oxygen survives salvage (P1, high)  `[fixed: Code/Fix_GhostFarmOxygen.lua — SetDome hook + LoadGame sweep]`
`FarmBase:ApplyOxygenProductionMod` (`Farm.lua:561-571`) puts negative `air_consumption`
modifier on `parent_dome` keyed `farm_id`; no `FarmBase:Done`, `Building:Done`/`SetDome(false)`
never clear it, and demolish path skips `UpdateWorking(false)` for non-`use_demolished_state`
buildings (`Building.lua:1457-1483`, `Demolishable.lua:139`). Dome keeps phantom O2 forever.
**Fix:** wrap `FarmBase` delete path (post-hook `Done` via class or `OnMsg` on demolish) to
remove the dome modifier; one-shot LoadGame sweep for orphaned `farm_id` modifiers.

### F38 — Destroyed tunnels rejoin pathfinding after load (P2, high)  `[fixed: Code/Fix_DestroyedTunnels.lua]`
`Tunnel:OnDestroyed` correctly calls `RemovePFTunnel` (`Tunnel.lua:153-155`), but
`OnMsg.LoadGame` (:264-266) re-adds PF tunnels for ALL `TunnelBase` with no `destroyed`
check (`AddPFTunnel` :197-209 checks only `IsValid(linked_obj)`; ruins are valid).
`TraverseTunnel` (:215-262) same. Rovers path through dead tunnels after any save/load.
**Fix:** wrap `Tunnel.AddPFTunnel`: bail if `self.destroyed or (self.linked_obj and
self.linked_obj.destroyed)`; on load also `RemovePFTunnel` for destroyed ones.
*Implemented as sketched*, wrapping the DECLARING class `TunnelBase` so the shipped
handler's `Tunnel.AddPFTunnel` lookup resolves to it. In-session destruction was already
correct (`OnDestroyed` -> `RemovePFTunnel`, and `TunnelBase:Destroy` takes the linked half
with it, :33-38) — the LoadGame sweep is the only leak. Repair is unaffected:
`Building:Rebuild` (`Building.lua:1655`) yields a NEW object whose `GameInit` registers
normally.

### F39 — Second Artificial Sun ignored (P2, high)  `[fixed: Code/Fix_SecondArtificialSun.lua]`
`SolarPanelBase:GameInit` (`SolarPanel.lua:8-14`): only `labels.ArtificialSun[1]` tested
with `TestSunPanelRange`. Panel built in range of sun #2 only never registers (reverse
direction works, `ArtificialSun.lua:35-47`). **Fix:** wrap GameInit: iterate the whole
label, register first sun in range.
*Implemented as sketched* (post-wrapper; the shipped body runs first and we only act if it
left `artificial_sun` false, handing the sun to the shipped `SetArtificialSun` so production
refreshes). `GameInit` is a combined method (`DefineCombinedMethod("GameInit", "procall",
"Object")`, `CommonLua\Classes\_object.lua:22`) assembled from the classdefs when classes
are built — after mod load — so writing onto `SolarPanelBase` reaches every panel class and
RCSolar. Added a LoadGame sweep: `artificial_sun` is persisted and never re-evaluated, so
panels already built beside sun #2 stay dark in existing saves without one.

### F40 — Dust Sickness infects Biorobots (P2, high)  `[fixed: Code/Fix_DustSicknessBiorobots.lua]`
`Data\StoryBit\DustSickness*.lua` filters exclude only `Child`; `Android` trait not
excluded, `DustSickness.incompatible = {}`; androids bleed Health every dust storm via
`daily_update_func` until cure tech. (Same trait also hit by F17 randomization bug.)
**Fix:** data patch: add Android to the storybit filters / trait incompatibility.
*Implemented as the filter half only, on evidence:* `Colonist:AddTrait`
(`Colonist.lua:426-453`) never consults `incompatible`, so the incompatibility half would
change nothing. Four `ForEachExecuteEffects` hand out the trait — two in
`DustSickness.lua` (:63-77, :103-117, one per outcome) and one each in
`DustSickness_GeneratSick.lua`/`_GeneratSickNotWorking.lua` (:5-26) — and the fix appends
`HasTrait{Trait="Android", Negate=true}` to each filter list, found by structure rather
than index. LoadGame pass removes the trait (and the paired
`StatusEffect_UnableToWork`) from biorobots already infected in a save.

### F41 — Gene Forging tech has no effect (P2, high)  `[fixed: Code/Fix_GeneForging.lua]`
`Colonist:GetRareTraitChance` (`Colonist.lua:3541-3550`) reads only
`TechDef.GeneSelection.param1`; `GeneForging` (`TechPreset.lua:1556-1564`, param1=50)
referenced nowhere in gameplay code. **Fix:** wrap `GetRareTraitChance`: add GeneForging
param when researched (ChoGGi's original approach: bump GeneSelection.param1 to 150).
*Implemented as an additive sum, not the param1 bump:* bumping GeneSelection only pays out
when that OTHER tech is researched, so Gene Forging on its own would still do nothing.
The value is a percentage bonus on the rare traits' draw weight (`GetRandomTrait` does
`rare_weight_mod = 100 + (rare_weight_mod or 0)`, `Traits.lua:1001-1022`), which is why
GeneSelection's 100 reads as "double" — so the two techs add: Forging alone +50, both +150.
Note `GetRareTraitChance` is a global function, not a Colonist method as this entry said.
Scope: only the "have" half. Rare traits GAINED later (schools, sanity breakdowns) call
`GetRandomTrait` with no `rare_weight_mod` at all, so neither tech has ever affected them
— separate defect, not touched.

### F42 — Buildings placeable on active dust devils (P3, high)  `[wontfix — user decision 2026-07-25, F56/F62/F63 grounds: designed scope, not a defect]`
`AreThereBlockingUnitsUnderneath` (`Construction.lua:1895-1914`) queries only
Drone/BaseRover; `BaseDustDevil` inherits `Object` (`DustDevils.lua:245-247`) — never
checked anywhere in Construction\. **Fix:** wrap `ConstructionController:UpdateConstructionStatuses`-
family to add a dust-devil proximity check (or extend the blocking query).

*Screened in the wave-5 build leg — the observation is correct, the verdict is not.*
Every factual claim in the entry holds: `ConstructionController.BlockingUnitClasses` really
is `{"Unit"}` (`Construction.lua:1905`), `BlockingUnitsFilter` really admits only disabled
Drones and BaseRovers (`:1895-1897`), `BaseDustDevil` really is a plain `Object`, and
`Construction\` really never mentions a dust devil. What is missing is any evidence that
it was ever supposed to. Weighing the F56 signals:
* **The guard has a different job.** It exists to stop a unit being entombed under a new
  building — hence *disabled* Drones (the ones that cannot walk away) and BaseRovers.
  A dust devil has no hex footprint, no collision and no grid presence; it follows a
  trajectory (`DustDevils.lua:326`) and deletes itself on a watchdog (`:312`). It can be
  neither trapped nor harmed, so the guard's purpose does not reach it. Compare F30, where
  entombment of a real rover *was* the defect.
* **The omission is named and overridable.** `BlockingUnitClasses` and
  `BlockingUnitsFilter` are declared class members, exactly the shape the F56 screen calls
  "designed scope, stated in a place a modder can change".
* **No shipped text promises it.** There is no dust-devil `ConstructionStatus`; the only
  "can't build here" weather text, `DontBuildHere` — *"Can't build on dust geysers"*
  (`Construction.lua:62`) — is about static geyser terrain (`Geysers.lua:1-26`, marked into
  the object hex grid at map load) and is implemented and working.
* **The sibling does it the other way, deliberately.** The game models exactly one
  weather-gated placement rule — `RocketLandingDustStorm`, *"Rockets can't land during
  Dust Storms"* (`Construction.lua:85`) — and implements it. Building through meteors,
  cold waves, dust storms and dust devils is otherwise normal play: a devil passing over a
  new site dusts it, which is what dust devils are for.

Adding a placement block would be a new rule, not a repair — FIX_POLICY §4.
**CLOSED `wontfix` 2026-07-25 (user decision, wave-4/5 QA session)** on the same
grounds as F56/F62/F63: deliberately maintained design, breaks nothing, no shipped
text promises the block. No opt-in module planned.

### F43 — Layout construction bypasses tech locks (P3, high)  `[fixed: Code/Fix_LayoutTechLock.lua — latent in the shipped game, see below]`
`LayoutConstructionController:Activate` (`LayoutConstruction.lua:231-263`): tech-locked
building with no prefab item → `require_prefab=false` → `add=true`, sub-controller
placed with no research gate. **Fix:** wrap `Activate`: filter items where
`not tech_enabled and not self.prefab`.

Confirmed against the shipped body: `tech_enabled` is computed at `:238` and consulted
only through `require_prefab` at `:241`, which covers one case — "locked but purchasable
as a resupply prefab". Locked-and-unobtainable has no branch and falls through the `or`
at `:242` into `add = true`. Outside a layout the tech gate is the build menu
(`GetBuildingTechsStatus`, `X\BuildMenu.lua:321-356`), which a layout entry never passes
through, so nothing else catches it.

**Latent — reachability stated for the record:** exactly one layout ships,
`SelfSufficientDome` (`Data\LayoutConstruction.lua:3-54`, used by
`Data\BuildingTemplate\SelfSufficientDome.lua:16`), and none of its seven entries carries
a `BuildingTechRequirements` row, so no vanilla layout can reach the hole. Fixed on the
same grounds as F27/F29 — the next layout, from a mod or a future update, inherits it. On
the shipped data the fix is a provable no-op.

*Implemented slightly differently:* the sketch's filter (`not tech_enabled and not
self.prefab`) drops entries the shipped code deliberately keeps — those covered by a
prefab the colony already owns, which `:244-248` re-enables through a stateful
`prefab_counters` handout. The wrapper instead re-reads what the shipped loop recorded
(`self.prefab_items[entry]`, `self.prefab`, `self.skip_items[entry]`), so the extra
condition is exactly `tech_enabled or self.prefab or an owned prefab`, and the counter
never has to be re-derived. Dropped controllers get the same teardown
`LayoutConstructionController:Deactivate` (`:310-317`) uses, and are marked in
`skip_items`, which is what `PlaceCursors` (`:341-342`) consults.

Deliberately untouched: `GetLayoutConstructionBuildingCost` (`:469-491`) and the
description builder (`:570-584`) walk the whole preset and already ignore `skip_items`
for the shipped prefab skip too — a separate cosmetic inconsistency, not this defect.

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

**PLAYTEST FAIL (PT-03 curve visual, 2026-07-25) → REWORKED same day.** The user's
curve-end salvage left the track "broke itself, became immune, multiple warnings"
(screenshots on file): the session log shows `Fix_TrackSalvageWipe.lua:60: attempt to
index a boolean value (local 'track_obj')` on every later click, plus a shipped
`Track.lua:556` raise on a dead track. Diagnosis: the split branch clears every
element's `track_obj` and relies on two `ExpandTrackFromElement` walks to reclaim
survivors; when the sorted order diverges from physical order (possible exactly when a
`node_idx` is non-numeric — the state the old "tolerant" comparator sorted as -1 and
CARRIED ON with), the deletion zone lands on physically scattered elements and strands
fragments no seed can reach. Those orphans sit in no track's arrays, render as debris,
and raise on every salvage click. Repairs (all in the fix file): (1) an orphan clicked
in demolish mode is simply deleted; (2) the comparator rework — stamp a repair site's
`node_idx` from its broken element, and if anything is STILL non-numeric, decline the
partial salvage before deleting anything (the shipped abort point, minus its raise);
(3) post-split orphan sweep + `IsValid` guards on the `UpdateEndElements` /
`UpdatePos` / `ProcessTrackElements` tail; (4) a `LoadGame` sweep that removes
orphaned elements already baked into a save. **Needs a fresh PT-03 run** — including
on the damaged save, which should log
`TrackSalvageWipe: removed N orphaned track element(s)` on load.

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

### F46 — Trains dump cargo at stations with the resource disabled (P2, high)  `[fixed: Code/Fix_TrainCargoDumping.lua]`
`Train:UnloadAll` (`Train.lua:783-803`) unloads everything with room, no
`station:IsResourceEnabled(res)` check (disable only removes the demand from
task_requests, `StorageDepot.lua:583-587,641-668`). Cargo planner then treats it as
"forbidden" stock and dispatches trains to haul it back out (`Train.lua:868,905-939`) —
resource ping-pong. **Fix:** override `UnloadAll` with enabled-check (allow dump if no
station on route accepts, to avoid stranding).
*Implemented as sketched:* full replacement of `Train:UnloadAll` with the enabled check;
the dump is still allowed when no other station on `city.train_track_routes[train.track]`
accepts the resource, and always when `is_stopping` (a refabbed train destroys its cargo,
`Train.lua:85-86,457-458`). Loading was already correct (both paths check
`dest:IsResourceEnabled`, `Train.lua:905-912,930-939`), so undeliverable cargo only arises
when something changes mid-trip.

### F47 — Track salvage refund ~1 hex for whole track; 0 for partial (P3, high)  `[fixed: Code/Fix_TrackSalvageRefund.lua]`
`TrackBase:GetRefundResources` (`Track.lua:286-307`) reads cost from ONE element (last);
`construction_cost_at_completion` set only on FIRST element (`Track.lua:524-525`) —
first/last mismatch; `DemolishAndSplitTrack` uses bare `DoneObject`, no refund (contrast
`Passage.lua:1217-1222`). Track cost 200 Metals/hex. **Fix:** multiply by `#self.elements`;
place return stockpile on partial salvage.

*Implemented differently, on better evidence:* the sketch's cost model is wrong in both
halves, and following it would have refunded up to five times what a track cost.
Screening the real code found:
1. **Track hexes are not billed per hex.** They are built in construction GROUPS of at
   most `const.ConstructiongGridElementsGroupSize` = 5 elements (`Tracks.lua:359`, `:426`;
   `_GameConst.lua:480`), and the group leader is charged
   `construction_cost_multiplier` × one element's cost — which `Tracks.lua:463` leaves at
   100, i.e. **200 Metals per group, not per hex** (contrast `Passage.lua:1969`, which
   sets `(#construction_group - 1) * 100`, and `LifeSupportGrid.lua:1426`'s 0.2/pipe).
   So a 30-hex track costs six groups' worth, and `#self.elements * 200` would refund 30.
2. **`Track.lua:524-525` is not where the stamp comes from.** That line only runs under
   the `FreeConstruction` game rule, and it stamps `Concrete` — which a track does not
   cost — so its value is 0. The real stamp is written by
   `ConstructionGroupLeader:Complete`, which suppresses every member's own
   `MarkSpentResources` (`ConstructionSite.lua:2469`) and then stamps the group's whole
   spend onto the element it completed LAST (`:2479-2489`, comment: "mark spent resources
   in 1 building so refunds would be correct"). One stamp per group, each holding that
   group's real expenditure. There is no first/last mismatch — a track of ≤5 hexes is one
   group whose stamp does land on `elements[#elements]`, and its refund is already exactly
   right.
3. **The defect is therefore a missing sum, not a missing multiplier.** `Track.lua:291`
   reads one element's stamp, so every construction group before the last one is
   uncounted; the refund does not grow with the track at all. The fix sums
   `construction_cost_at_completion` over all `self.elements`. Because each stamp is a
   recorded expenditure, the total is exactly what was spent and can never exceed the
   shipped 50%. When no element carries a positive stamp (Free Construction, instant
   tracks) the shipped estimate-from-one-element fallback runs unchanged.
4. **Partial salvage** is fixed as sketched but hooked one level up: a chained wrapper on
   `TrackGridElement:Demolish` (the player-salvage entry point — `ToggleDemolish`,
   `TrackElement.lua:259-261`, and the mass-salvage tool, `Construction.lua:2911`) snapshots
   the stamped elements, calls the original, and refunds the stamps of the elements the
   call actually destroyed. Observing the outcome avoids re-deriving the three deletion
   branches. `DemolishAndSplitTrack` itself is deliberately not wrapped: its other caller
   (`Construction.lua:1574`, track erased from under a newly placed station) is not a
   salvage. Whole-track demolition is skipped by the wrapper — `OnDemolish` clears
   `track.elements` to false (`Track.lua:190`) after it has already refunded through the
   replaced getter — so no refund is ever paid twice, and a stamp dies with its element.

**Existing saves:** fully retroactive. The stamps are already in every save; only the
reading of them changes.

### F48 — Station-connector savegame fixup no-op (P3, high defect / low impact)  `[blocked — the corrected pass is too invasive to ship untested; see below]`
`Station.lua:1346`: `ProcessTrackElements(ResolveMap(track, track.elements))` — paren
misplaced, should be `ProcessTrackElements(ResolveMap(track), track.elements)`; migration
no-ops (may contribute to "tracks won't connect" on old saves). **Fix:** re-run corrected
pass in one-shot LoadGame sweep.
*Blocked 2026-07-25 (wave 3), during the sanitizer build.* The defect is confirmed exactly
as written — `ResolveMap(track, track.elements)` returns one value, `elements` arrives nil,
`#elements == 0` is true for nil in this engine (`Tracks.lua:808`) and the function returns
immediately, so `SavegameFixups.A_StationConnectorElements3` (`Station.lua:1341-1354`)
re-orders nothing. What blocks the repair is what the corrected call actually does:
`ProcessTrackElements` → `OrderTrackElements` (`Tracks.lua:520-624`) **clears and rebuilds
`el.connections` and rewrites `node_idx` on every element**, then the caller repositions
every element in Z and recomputes pillars and sections (`:840-900`). Its only failure
handling is `assert(false, "unable to find the expected number of track elements")`, and
assert does not unwind in this engine — so a track it cannot walk (a broken element, a
repair site — i.e. exactly F45's situation) has its connections half-rewritten and
execution continues. Running that over every track of every save on load, with no way to
test it in-game from this seat, risks more than the P3 it repairs.
**To unblock:** an in-game test on a save with (a) a healthy multi-station network and
(b) a meteor-damaged track, comparing `track.start_el`/`end_el` and route formation before
and after. If it holds up, the pass belongs in `90_SaveSanitizer.lua` behind a one-shot
`SMRFixPack_*` flag on `UIColony` so it cannot re-run every load.
*2026-07-26: that test is now written up as **PT-37** in `docs/PLAYTEST_CHECKLIST.md`
(exact console commands for both cases) and sits on the user's in-person list. PASS on
both cases → implement in the sanitizer, skipping tracks that carry repair sites; a dirty
FAIL on the damaged-track case → close `wontfix — repair riskier than the defect`.*

### F49 — Train minors bundle (P3, med)  `[fixed*: Code/Fix_TrainMinors.lua — items (a), (c) and (d); (b)(e) screened and deliberately not fixed, see below]`
(a) instant-built tracks use pipes palette (`Tracks.lua:385` vs `TrackElement.lua:791`);
(b) `DemolishAndSplitTrack` ignores `assigned_vehicles` — mid-transit trains silently
stored/self-destruct (`Train.lua:249-251,535-541`); (c) salvage click on invisible
connector hexes propagates to the STATION (`TrackElement.lua:299-300`); (d) `max_vehicles`
never recomputed after merge/split (`Track.lua:64-65`); (e) dead validation
(`TrackRequiresTwoStations` never inserted; `CanContinueTrack` never called).

**Screened item by item in the wave-5 build leg. Two fixed, three not — and none of
the three is a no-op waiting to be written.**

**(a) FIXED.** Confirmed: `Tracks.lua:385` captures `GetPipesPalette()` and `:412`
applies it to every element the instant `place_track` path creates. Every other track
path uses `GetTracksPalette()` — the completed-construction path
(`TrackElement.lua:791`), the construction cursor (`GridConstruction.lua:220`) and,
decisively, the colony colour-scheme refresh, which repaints *every* `TrackGridElement`
on every map with it (`ColonyColorScheme.lua:120-121`). The palettes really do differ
(`ColonyColorScheme.lua:69-77`). Consequence: instant track is pipe-coloured until the
player changes colour scheme, at which point it silently corrects itself — which is also
why the scheme refresh is the authority on the right answer. Fixed with a post-wrapper on
`TrackGridElement:GameInit` applying exactly what the refresh applies; construction sites
are skipped, as the shipped GameInit skips them.

**(d) FIXED.** Confirmed and slightly worse than tracked: `Track.lua:65` is the **only**
assignment to `max_vehicles` anywhere in the game (elsewhere it is read only, via
`StationsLink:GetMaxVehicles` → `CanAddVehicle`, `StationsLink.lua:28-32`; class default
2, `:8`), and it runs once, in `TrackBase:GameInit`. Salvage shortens or splits a track
(`TrackElement.lua:503-541`). *(Corrected by the QA audit 2026-07-25: an earlier version
of this paragraph claimed the split-off `new_track` runs GameInit before it has elements
— backwards; GameInit is deferred to a game-time thread (`_object.lua:187-192`), so the
split-off track's cap is computed correctly. The residual defect is the SURVIVING track,
which never re-runs GameInit — and that is what the fix covers.)* Fixed by recomputing
with the shipped formula on element-set changes — `TrackBase:UpdateEndElements` (called
from all three partial-salvage branches, `:516`, `:530`, `:556-557`, always after the
arrays are repopulated) and `ExpandTrackFromElement` (the merge/expand path) — plus a
`PostLoadGame` sweep for saves already carrying a stale cap (PostLoadGame, not LoadGame:
`SavegameFixups.RemoveTrackDoubleTurns`, `TrackElement.lua:839-843`, re-processes track
elements after `Msg("LoadGame")`). *Known coverage gap (QA audit, accepted): the
`TrackGridElement:AutoConnectTracks` merge path (`TrackElement.lua:381-409`) and
instant-build reuse of an existing `track_obj` (`Tracks.lua:307/:318/:327`) recompute
nothing, so a merged/extended track's cap can stay stale in-session until the next
load's sweep. The fix never sets a wrong value; it just doesn't catch every change
point yet.*

**(b) NOT FIXED — mechanism confirmed, consequence not establishable from source.**
Nothing in any of the three partial branches of `DemolishAndSplitTrack` reads or writes
`assigned_vehicles`; the surviving `track_obj` keeps its whole train list while its
element set shrinks, and the `new_track` that takes the other half is created with none.
The whole-track branch is fine — `TrackBase:OnDemolish` → `DestroyAssignedTrains`
(`Track.lua:159-166`) handles it, and trains are stored as prefabs rather than lost. What
a train physically standing on a removed or re-homed element then does cannot be read off
the source. **Playtest item PT-46.**

**(c) FIXED (user decision 2026-07-25: "the click does nothing").** The mechanism is real:
`TrackGridElement:SelectionPropagate` returns `self.station` for a connector element
(`TrackElement.lua:297-300`), and `SelectionMouseObj` runs every candidate through
`SelectionPropagate` (`SelectionModeDialog.lua:44-50`), so in demolish mode the object
handed to `DemolishModeDialog:OnMouseButtonDown` could be the station, which is a Building
and gets `ToggleDemolish()` (`Construction.lua:2903-2906`). The shipped code contains
**two** demolish-mode guards against exactly this class of propagation and they prescribe
*different* remedies: `:54-56` throws the object away (`precise, terrain_cursor_obj =
false, false`) while `:84-88` substitutes the underlying element — both about `TrackBase`,
neither covering the station — so the choice was screened to the user, who picked the
`:54-56` shape. Implemented as a pre-guard on `SelectionPropagate`: in demolish mode a
station-owned element propagates to nothing. Normal-mode selection (connector click
selects the station) and salvaging the station via its own footprint are unchanged.

**(e) NOT FIXED — dead code whose revival is a redesign.**
`GridConstructionController:CanContinueTrack` (`GridConstruction.lua:478-491`) is never
called from anywhere (its passage twin `CanContinuePassage` is, at `:449`), and
`ConstructionStatus.TrackRequiresTwoStations` is referenced only from inside it — so the
authored error "The Track must start and end at a Station." can never appear. Notable
detail: the shipped file marks its three sibling statuses `-- unused` and leaves this one
unmarked (`TrackGridConstruction.lua:1-27`), i.e. the author believed it live. Reviving it
needs BOTH an invented call site in the drag/placement flow AND an invented condition that
inserts the status (without which `CanContinueTrack` returns false forever). That is two
pieces of new design, not a repair.

### Recorded latent (wave-5 screening, no fix): `DivRound(cost, res)` in `BreakTrackElement`
`Track.lua:643-652` — under the SafeTransport tech the repair-cost loop reads
`reduced_costs[res] = DivRound(cost, res)`, dividing by the **resource-id string** instead
of by 2. It is a real typo and would raise (arithmetic on a string) if it ever ran, but it
does not: the loop only runs when `cgl.construction_costs_at_start` is a non-empty table,
and it never is at that point. `BreakTracks` (`Meteors.lua:599-613`) reuses one
`broken_cg` across every element of a track in a strike, so the first call finds the leader's
`construction_costs_at_start` still `false` (the group was just created) and assigns `{}`,
and every later call in the same synchronous loop iterates that empty table.
`GatherConstructionResources` cannot populate it in between — nothing yields. A second
strike starts a fresh group. **Also checked and NOT a defect:** the halving above it does
not compound across calls, because `:642` reassigns `construction_cost_multiplier` from
`(#cg - 1) * 100` absolutely before each halving. No entry filed and no fix written — the
line is unreachable, and writing a fix for it would be the F10 mistake.

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

### F54 — Switched-off shuttle hubs count as transport available (P2, med-high)  `[fixed: Code/Fix_ShuttleHubOffAvailable.lua]`
`IsLRTransportAvailable` (`ShuttleHub.lua:350-359`) counts hubs with
`GetWorkNotPermittedReason()` truthy (= player toggled OFF) as available, but
`SendOutShuttles` only runs when `working`. All-hubs-off (late-game power saving) →
colonists queue on pickup spots outside for shuttles that never come; walkability logic
also skewed (`Dome.lua:256-259`). **Fix:** predicate counts only self-lifting suspensions.
*Implemented as sketched*, as a full replacement of the global with one added term
(`hub.ui_working`), because the defect is mid-condition and the function returns a single
colony-wide boolean — a wrapper that sees `true` cannot tell which hub produced it.
Verified both ends of the sketch: `SendOutShuttles` is reached only from
`ShuttleHubBase:BuildingUpdate` under `if self.working` (`:1622-1630`) and from
`CargoShuttle:LaunchDstr` under `if hub.working` (`:509-513`), so a switched-off hub
never dispatches. Enumerating what the shipped second clause actually admits (permission
reason set, no physical reason) gives exactly four states: `"TurnedOff"` (`ui_working`
false — the player's switch, not self-lifting), `"DomeNotWorking"` (`Building.lua:591-596`
— also a player switch, but unreachable for a Shuttle Hub, which is an outside building
with no parent dome), `"ExceptionalCircumstancesDisabled"` (`BaseBuilding.lua:359`) and
`"ExceptionalCircumstancesMaintenance"` (`RequiresMaintenance.lua:129-133`). The last two
are set and cleared by the game itself, so they are kept; only the player's switch is
excluded, which `hub.ui_working` expresses directly and without matching reason strings.
Probe: `ShuttleHubOffAvailable` in the Test Kit's `30_Probes_Wave3.lua`.

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

### F56 — Auto RC Transports never offload rockets  `[wontfix — user decision 2026-07-26: deliberately maintained design, breaks nothing; same grounds as F62/F63]`
`RCTransport.lua`: `Automation_Gather` (:884-908) sources only surface deposits;
`Automation_Unload` (:910-941) excludes rockets as destinations. Manual load/routes work —
players correctly perceive AUTO as broken. Combined with F50 + shuttle exclusion, remote
rockets have no automated unloader at all. **Fix:** extend `ProcAutomation`: when empty,
seek landed `UniversalRocketBase` with status "unloading", `TransferAllResources`.

*Screened before implementing (wave 4) — the code matches the entry, but the remedy is a
feature, not a repair.* Three findings, in order of weight:
1. `Automation_Gather` sources `self:GetAutoGatherDeposits()` (:880-882), a method that
   returns exactly the four `SurfaceDeposit*` classes. A named, overridable accessor is a
   declared scope, not a forgotten case.
2. The rocket exclusion in `Automation_Unload` is `not IsRocketClass(d, "UniversalRocketBase")`
   (:916). `IsRocketClass` is the Relaunched compatibility shim
   (`RocketCompatibility.lua:1037-1046`) that matches BOTH the legacy `RocketBase` family
   and the new `UniversalRocketBase` one — i.e. a Relaunched developer deliberately
   re-stated this exclusion for the new class tree. Maintained intent, not an oversight.
3. The feature's own promise is narrow: the auto-mode rollover reads "the RC Transport
   will **gather resources** automatically" (`RCTransport.lua:1697`) — no rocket claim.
   The manual paths that DO service rockets exist and work, exactly as the entry says
   (`CanLoad` :310-324 admits `UniversalRocketBase`; `InteractWithObject` :419-429 opens
   the resource selector on one; `TransferAllResources` :1217-1300 is class-agnostic).
Adding rocket pickup to automation is therefore new capability — FIX_POLICY §4 territory,
the same class as D01/D02.

**CLOSED `wontfix` 2026-07-26 (user decision), on the same grounds as F62/F63:**
deliberately maintained design, breaks nothing. The rocket exclusion was consciously
carried into Relaunched (point 2 above is the proof — a developer re-stated it through the
new compatibility shim), and the manual paths the entry itself credits are the intended
way to service a rocket with an RC Transport.

*If it is ever revisited, it does NOT get a standalone module.* An auto-offload option
belongs **alongside D01's unwritten Rare Metals export half**, in `Opt_ClassicRockets`, not
in an `Opt_AutoRocketOffload` of its own. Both are the same request wearing two hats —
"make rockets load and unload themselves again, the way the original game did" — both are
opinions about rocket logistics rather than repairs, and both touch the same machinery
(`SetCargoRequest`, the payload dialog, Automated Mode's `export_above` thresholds, and the
F50/F68/F70/F71 request path). Shipping them separately would let a player enable half a
behaviour and get a colony where rockets are emptied but never refilled. So this rides on
whatever design decision D01's export half eventually gets — same module, same opt-in flag,
same playtest — or it stays closed.
*Origin note:* the player report behind this entry is recorded in `RESEARCH.md` as
"**Drones** ignore rocket cargo even at high priority; RC Transports don't auto-offload
rockets". The drone half is the load-bearing complaint and is already addressed by F50.
*What screening DID find:* three rocket tests in the same file were never converted to the
Relaunched classes — filed and fixed as **F74** below. That is the real defect in this area.

### F57 — Drone/transport minors bundle (P3, med)  `[fixed*: Code/Fix_DroneTransportMinors.lua — items (a) and (b); (c) deliberately not fixed, see below]`
(a) `DroneControl:UpdateRocketsInternal` (`DroneControl.lua:613-639`) clears only
`r_t.Fuel`, writes `r_t[r.FuelResource]` — stale restrictor for non-"Fuel" rockets (latent);
(b) `OnMsg.OnPassabilityChanged` (`Drone.lua:851-864`) rebuilds unreachable table without
weak-keys meta and doesn't recompute count; (c) `recursive_enum_dome_workplaces`
(`Dome.lua:674-675`) skips quarantine check, saved only by `Workplace:IsSuitable` re-check.

**Screened item by item in the wave-5 build leg.**

**(b) FIXED — and it is the biggest of the three.** Both halves confirmed. The handler
builds `local unreachable = {}` (`:855`) and assigns it at `:862`, so the table loses the
`weak_keys_meta` every other creation site gives it (`Drone:ApproachWrapper` `:826`,
`Drone:ResetUnreachablesTable` `:875`) — from the first passability change onward each
drone holds a **strong** reference to every building it once failed to reach, keeping
salvaged and destroyed buildings alive and still yielding them from `pairs` in
`CleanUnreachables` (`:890`) and the recharger scan (`:1281`). And
`unreachable_buildings_count` is never recomputed although the table just shrank; that
number gates the eviction path (`:827-838`, against `const.MaxUnreachablesInTable`) and
the DroneControl idle clock (`:630`), and `CleanUnreachables` then decrements the stale
value further (`:893`). **The F10 screen was applied and does not bite:** no
nil-iteration crash is claimed here — `unreachable_buildings` can legitimately be `false`
and this engine tolerates `pairs(false)`. The defect is the state left behind, not a
raise. Fixed with an additional `OnMsg.OnPassabilityChanged` (OnMsg is additive; ours
runs after the shipped one) that re-applies `weak_keys_meta` and recounts with
`table.count`, exactly as `ApproachWrapper` recounts at `:841`.

**(a) FIXED, latent.** Confirmed: `r_t.Fuel = nil` clears one key while the Relaunched
branch writes `r_t[r.FuelResource]` (`:634`), so any fuel resource other than the literal
`"Fuel"` is never cleared and a departed rocket's request restricts drone work forever.
Latency stated for the record: `FuelResource` has **no assignment anywhere in
`ModTools\Src`** (only `FuelResourceAmount` is set per template, e.g.
`Lua\BuildingTemplate\UniversalRocket.generated.lua:29`), and the legacy `RocketBase`
branch hardcodes `"Fuel"` — so on shipped data the two keys coincide and nothing leaks.
Fixed for the F27/F28 reason: a mod or a future rocket with its own fuel resource
inherits the leak. The replacement also clears the key it wrote last time, remembered in
an absent-tolerant `SMRFixPack_rocket_fuel_key` field on the DroneControl.

**(c) NOT FIXED — redundant with the assignment-time check, and a §1.5 replacement to
reach.** The mechanism is exactly as tracked: `can_work_here = work_or_train or (cdome ==
colonist.dome)` (`Dome.lua:674`) short-circuits the quarantine test away for reason
"work" and "training", even though the function it skips is named
`CanColonistsFromDifferentDomesWorkServiceTrainHere` and the service path calls it with
the comment `--quarantine` (`Dome.lua:2907`). *(Rationale corrected by the QA audit
2026-07-25: an earlier version claimed fixing this "would undo F61" — wrong. The skipped
check sits on `cdome`, the TARGET dome; F61 removes the HOME dome's own
`accept_colonists` term and deliberately keeps the target-side check at assignment time,
`Fix_HomeDomeMigrationGate.lua:71/:93/:113/:142`. No conflict.)* The screening outcome
stands on the grounds that do hold: the enumeration only produces candidates,
`Workplace:IsSuitable`/`TrainingBuilding:IsSuitable` re-run `CanWorkTrainHereDomeCheck`
before anyone is assigned (`Workplace.lua:493-494`, `TrainingBuilding.lua:137-138`), so
an enumeration-time check adds only redundancy — and implementing it would need a §1.5
full replacement of `GetCommutableWorkplaces` recreating the file-local
`recursive_enum_dome_workplaces`. Left as a recorded inconsistency, like the four in the
STATUS.md "recorded but deliberately untouched" list.

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

### F59 — Freed housing never notifies homeless (P2, med)  `[fixed*: Code/Fix_FreedHousingNotice.lua — the RemoveResident half; the CancelResidenceReservation site is deliberately not hooked, see below]`
`RemoveResident` (`Residence.lua:83-90`) and `CancelResidenceReservation` (:353-365) never
call `CheckHomeForHomeless`; homeless rely on Idle heavy-update throttled to 12 game hours
at 3600+ pop (`City.lua:118-120`). **Fix:** post-hook `RemoveResident` →
`CheckHomeForHomeless()`.
*Implemented one level up, on better evidence:* the post-hook is on
`Colonist:SetResidence` (`Colonist.lua:2291-2307`), the only caller of `RemoveResident`.
Same event, but the notification then runs when the move is FINISHED. `RemoveResident` is
called from the MIDDLE of `SetResidence`, before `home:AddResident(self)` and before
`self.residence` is updated; waking the homeless there lets one of them take the slot the
colonist in hand is about to occupy, and the next shipped statement is
`assert(self:GetFreeSpace() > 0)` followed by an unconditional insert (`Residence.lua:
74-77`) — assert does not unwind in this engine, so that is an over-capacity residence.
The hook no-ops unless a home was actually left and `GetFreeSpace() > 0` in it.
*Open half:* `Residence:CancelResidenceReservation` is NOT hooked. `Residence:AddResident`
releases the incoming colonist's reservation (`:74`) one line before the same
`assert(self:GetFreeSpace() > 0)`, so a notification from there reintroduces exactly that
race. The reservation case is instead bounded by F58's daily stale-reservation sweep plus
the normal heavy update. Probe: `FreedHousingNotice` in `30_Probes_Wave3.lua`.

### F60 — Dome free-space uses `working`, assignment uses `ui_working` (P2, med)  `[fixed: Code/Fix_DomeFreeSpaceMismatch.lua]`
`Dome:RefreshFreeLivingSpaces` (`Dome.lua:2832-2834`) omits `player_enabled` →
`GatherFreeLivingSpaces` counts by `working` (`_GameUtils.lua:475-483`); unpowered
residences count 0 for births/immigration gates while `ChooseResidence` (:412) still
assigns to them. Power flicker desyncs the two views. **Fix:** pass consistent member.
*Implemented as sketched* — a full replacement of the two-line method passing
`player_enabled`; there is nothing to wrap, the fix IS the argument. Which member is the
intended one is settled three ways: `ChooseResidence` (`Residence.lua:404-412`) and
`Colonist:UpdateResidence` (`Colonist.lua:2309-2316`) both gate on `ui_working`, and the
two functions immediately above `GatherFreeLivingSpaces` in the same file —
`GetFreeWorkplacesAround` (`:443-455`) and `GetFreeWorkplaces` (`:457-473`) — tally
capacity on `b.ui_working` unconditionally. The `player_enabled` parameter has no caller
anywhere in Src, so nothing else changes meaning.
*Deliberately not touched:* `MicroGHabitatBase:RefreshFreeLivingSpaces`
(`MicroGHabitat.lua:42-44`) has the identical omission, but a habitat's `working` state is
its life support — F73's subject, not this defect.
Probe: `DomeFreeSpaceMismatch` in `30_Probes_Wave3.lua`.

### F61 — Home dome's migration toggle blocks outbound shopping/work/training (P1, med-high)  `[fixed: Code/Fix_HomeDomeMigrationGate.lua]`
`Dome:GetService` (`Dome.lua:2900-2916`; same at 2927/2947/2959, `ShiftsBuilding.lua:250-254`):
outbound cross-dome access requires `self.accept_colonists` — the HOME dome's
"accept colonists" MIGRATION policy. Turning it off on a residential dome (routine) silently
stops residents shopping/working/training through passages; target-dome checks are separate
and correct (`Dome.lua:2880-2882`). Best match for "refuse to shop through a passage".
**Fix:** override the four sites, dropping home-side `accept_colonists` from the condition.

### F62 — Services reach exactly 1 passage hop, never trains (P2, high mechanism)  `[wontfix — carried-forward design, verified identical to the original game]`
`GetService` iterates `GetConnectedDomes()` = direct adjacency refcounts (`Dome.lua:619-644`,
`Passage.lua:1237-1247`), not the transitive `dome_networks` (`Passage.lua:1096-1119`);
workplace search additionally enumerates train-reachable domes (`Dome.lua:646-690`).
Hub-and-spoke: spoke→spoke shops invisible. **Fix:** extend service search to the passage
network (and optionally train-reachable domes) — flag as behavior change, default on.
*Blocked 2026-07-25 (wave 3), after reading the code.* Everything in the entry re-verified
and correct: `Dome:GetService` (`:2900-2941`) and `Dome:ChooseTraining` (`:2945-2955`) walk
`GetConnectedDomes()` only, and `Dome:GetCommutableWorkplaces` (`:682-689`) reaches two dome
levels plus train-reachable stations at each. What did NOT survive contact is the premise
that one-hop is a mistake:
* the codebase uses direct adjacency for cross-dome work AND service **consistently** —
  `AreDomesConnected` (`Dome.lua:356-358`) is `connected_domes[bld2]`, direct only, and it
  is what gates `ShiftsBuilding:CanWorkTrainHereDomeCheck` (`:252`),
  `Colonist:CheckForcedWorkplace` (`:2351`), `Colonist:UpdateWorkplace` (`:1485`) and
  `Workplace.lua:567`. The transitive `AreDomesConnectedWithPassage` has exactly two
  callers in all of Src (`Dome.lua:258` walkability, `Passage.lua:1144` pathing);
* so there is no "the same author wrote it correctly elsewhere" proof of intent
  (FIX_POLICY §4) — extending the service search would be a design change with balance and
  performance consequences (the service search runs constantly), which the sketch itself
  already conceded by asking for it to be "flagged as a behavior change".
The one genuine internal inconsistency worth recording: `IsInWalkingDistDome`
(`Dome.lua:244-261`) answers TRUE for any two domes in the same passage network, so the
walkability model says A↔C is walkable while the service model says C is invisible from A.
**To unblock:** a decision that this is in scope. If taken, it belongs in an opt-in module
alongside D01, not in the default pack.
*Verified against the ORIGINAL game 2026-07-26 (official `HaemimontGames/SurvivingMars`
source release): SAME AS ORIGINAL.* The original's `Dome:GetService`
(`Lua/Buildings/Dome.lua:2817-2857`) is the same algorithm — own dome, then one
`GetConnectedDomes()` hop gated on `allow_service_in_connected` — and its
`connected_domes` is the same per-pair passage refcount
(`Lua/Passage.lua:998-1013`). Even `AreDomesConnectedWithPassage` existed there with the
SAME two callers (walkability `Dome.lua:251`, pathing `Passage.lua:1097`). Relaunched's
version is a cosmetic refactor with identical reach: one-hop service is a carried-forward
design across both games, not a regression. Any change here is a mod feature by
definition.
**CLOSED `wontfix` 2026-07-26 (user decision):** not breaking anything, not making play
extremely hard, and original to the devs' vision in both games. No opt-in module planned;
the recorded internal inconsistencies (walkability-vs-service, permitted-vs-offered
training) stay on this entry for the record.

### F63 — Universities invisible to emigration (P2, high)  `[wontfix — carried-forward design, verified identical to the original game]`
Training is pull-only from student side, 1 hop, F61-gated (`Colonist.lua:1505-1507`,
`Dome.lua:2945-2955`); `FindEmigrationDome` scores only `labels.Workplace`
(`Colonist.lua:2644,2672`, `Workforce.lua:53-64`) — `TrainingBuilding` is a different label
(`TrainingBuilding.lua:26,38`) = zero score. Nobody relocates to study; shuttle-only
university sits empty forever. Only unspecialized colonists qualify
(`MartianUniversity.lua:65-67`). **Fix:** include free training slots (colonist `CanTrain`)
in emigration scoring; walk full passage network in `ChooseTraining`.
*Blocked 2026-07-25 (wave 3), after reading the code.* Both halves confirmed and both are
additions rather than repairs:
* emigration scoring really does read only `labels.Workplace`
  (`Workforce:HasFreeWorkplacesAroundForSpecialist` / `WorkplacesEval`,
  `Workforce.lua:53-64`, `:66`), and `TrainingBuilding` really is its own label
  (`TrainingBuilding.lua:26,38`). But there is no broken hookup to repair — there is no
  `TrainingEval` anywhere, dead or alive, next to `WorkplacesEval` and
  `Community:ResidencesEval` (`Community.lua:489`). Training was never a term in the
  emigration score, so adding one is a new feature and a balance change (FIX_POLICY §4);
* "walk full passage network in ChooseTraining" is the same behavior change as F62.
Recorded for the record, since it IS an inconsistency: `ShiftsBuilding:CanWorkTrainHereDomeCheck`
falls through to `GetTransportRoute(his_dome, self)` (`ShiftsBuilding.lua:253`), so a
colonist is PERMITTED to train at a train-reachable school that `Dome:ChooseTraining` will
never offer them.
**To unblock:** same decision as F62 — an opt-in module, not the default pack.
*Verified against the ORIGINAL game 2026-07-26: SAME AS ORIGINAL.* The original's
`FindEmigrationDome` (`Lua/Units/Colonist.lua:1987-2064`) scores exactly trait filter +
free housing + `HasFreeWorkplacesAround` — which reads only `labels.Workplace`
(`:1960-1977`); no training/university term exists anywhere in the original's emigration
paths (repo-wide grep), and no `TrainingEval` existed there either. Its training search
(`Colonist.lua:1122-1131` + `Workplace.lua:841-881`) is the same own-dome-then-one-hop
walk Relaunched hoisted onto `Dome:ChooseTraining`. Nobody could ever emigrate to study,
in either game. Adding it is a new mechanic, not a repair.
**CLOSED `wontfix` 2026-07-26 (user decision), same grounds as F62.**

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
*Half shipped, opt-in: `Code/Opt_ClassicRockets.lua`* (id `ClassicRockets`, enabled with
`SMRFixPack_Optional = { ClassicRockets = true }` before the mod loads; the `Opt_` filename
prefix marks it as not-a-fix). It ships the **fuel half**: a chained wrapper on
`GetFuelResourceRequest` that, only where the shipped function already answers 0, keeps the
launch ration requested for a player-controlled rocket parked at the colony with no
destination. Verified the mechanism end to end —
`CargoTransporterNew:UpdateCargoResourceRequests` feeds
`additional_amount = is_refuel_resource and self:GetFuelResourceRequest()` straight into the
drone demand (`CargoTransporterNew.lua:1249-1265`), and neither notification branch fires in
this state because both require `arrival_loc` — they live in the
`UniversalRocketBase:UpdateCargoResourceRequests` override (`UniversalRocket.lua:1687-1692`;
citation corrected by the QA audit 2026-07-25) — so there is no refuel spam. F69's asteroid-lander reserve is untouched — the wrapper only acts when the
chain below it returned 0.
*Export half deliberately NOT shipped.* "Standing PreciousMetals demand" is a gameplay
system rather than a hook: the modern request is driven by `SetCargoRequest`, the payload
dialog and Automated Mode's `export_above` thresholds, so injecting a permanent demand
means editing the same machinery as F50, F68, F70 and F71 — with no way to test the result
in-game from the build seat, and for a change that is by this entry's own verdict not a
defect. It needs a design decision (what threshold? which resources? what interaction with
Automated Mode?) plus a playtest before it is written.
*The export half now also owns F56.* F56 (auto RC Transports never offload rockets) closed
`wontfix` 2026-07-26 on the same "deliberately maintained design" grounds, with the note
that if it is ever revisited it belongs in THIS module rather than in one of its own — same
request ("rockets should load and unload themselves like they used to"), same machinery,
and shipping the two separately would let a player enable an emptying behaviour without the
refilling one. So whenever the export half gets its design decision, decide auto-offload in
the same pass and behind the same `ClassicRockets` flag.

### D02 — Dismissing a "Building Not Working" warning only silences it for 2 real minutes — BY DESIGN, feels like a bug (planned opt-in)
Spun out of F32's close (2026-07-26, user decision) — read that entry for the full trace.
Not a defect: the shipped suppression machinery works exactly as designed
(`Notifications.lua:41-43`, `:86-88`, `:141-146`). The design just has no answer for a
PERMANENTLY broken building: the window is 2 REAL minutes (`SuppressTime = 120000`, real
time — the preset sets no `GameTime`, `NotificationPreset.lua:126-128`), it silences the
whole notification id (new breakages included) rather than the acknowledged building, and
there is no per-building acknowledgment at all. An unfixable building — F30's
lake-entombed case is the archetype — re-nags every 2 real minutes for the rest of the
game. **Players read this as "dismiss is broken"; it is not — it is a design gap.** The
released mod description must carry that explanation (a dedicated note exists in
`MOD_DESCRIPTION.md`), both so players stop reporting it as a bug and so the module below
is understood as a preference, not a repair.
**Planned remedy — `Opt_AcknowledgedWarnings` (opt-in module, NOT the default pack, per
FIX_POLICY §4):** per-object acknowledgment. On dismissal of `NotWorkingBuildings`,
snapshot the buildings it contained (`notification.objects` is an `array_set`; dismissal
is cleanly detectable — `SuppressNotification` runs only under `notification.dismissed`,
`Notifications.lua:86-88`; `Msg("AddNotificationObject")` / `Msg("RemoveNotificationObject")`
fire per object, `:247/:283`). Filter acknowledged buildings out of re-adds until the
building recovers (`ShouldShowNotWorkingNotification()` false, `BaseBuilding.lua:134`) —
recovery resets it, so a LATER breakage of the same building notifies again; new buildings
always notify immediately. Strictly better than the shipped window on both axes: the
acknowledged wreck stays quiet forever, new events are never hidden even for 2 minutes.
Ack set persisted as an absent-tolerant `SMRFixPack_*` handle set (policy §3).
`DestroyedInfrastructure` / `RoverDamaged` are deliberately untouched — one-shot adds
where dismissal already holds (F32 trace).
**Gate:** PT-38 first (verify the 2-real-minute cadence in play — the design assumption
this module answers), then build + probe in a wave-4+ leg.
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

### F65 — Station attached to a train tunnel never bridges the power grid (P2, med)  `[fixed: Code/Fix_TrackTunnelPowerBridge.lua]`
`TrackTunnel` description promises power transfer (`Data\BuildingTemplate\TrackTunnel.lua:17`);
class machinery identical to working `Tunnel`. Defect: `OnMsg.StationsConnected`
(`Track.lua:668-680`) skips `ConnectToGrids()` when `#track.elements <= 2` ("adjacent
anyway" assumption) — station attached directly to tunnel connects via exactly 2 connector
elements → supply tunnel never created, no power link. Caveat: TrainTunnel entity spot
data is binary, unverifiable from Lua. **Fix:** additional `OnMsg.StationsConnected`
handler: if 2-element track touches a `TrackTunnelBase`, call `track:ConnectToGrids()`;
LoadGame pass re-asserting masks/merges.
*Confirmed against the code, and the shortcut's premise is checkable:* a 2-element track's
two elements ARE the two buildings' connector elements (`TrackBase:GetSupplyTunnelElement`,
`Track.lua:567-574`, returns `elements[1]` and `elements[#elements]`), and a connector
element sits on a hex OUTSIDE its building — `OrientConnectorElements` records the
connection back toward the building at `conq - dq, conr - dr` (`TrainTransport.lua:91-100`).
So when the shortcut fires the buildings are two hexes apart with the connector hexes
between them, and track elements carry no power (`TrackBase.ApplyToGrids = empty_func`,
`:663`; "Since we're not an ElectricityGridObject", `:98`). The description promise is
real and literal: "connect tracks **and power grids** at different locations and different
elevations" (`Data\BuildingTemplate\TrackTunnel.lua:17`).
*Implemented differently, on better evidence:* whether the two buildings genuinely end up
adjacent is entity spot geometry — binary data, unreadable from Lua, exactly the caveat
above. So the fix does not assume: the added `OnMsg.StationsConnected` handler bridges only
when the two stations demonstrably sit on **different live electricity grids** after the
shipped handler has run. If the shortcut's premise holds they already share a grid and the
fix is a no-op. That runtime test also removes the reason to restrict it to
`TrackTunnelBase` — the same shortcut fails identically for two stations a short track
apart — so the scope is any ≤2-element track; the tunnel is just the case with a written
promise attached. On success the handler clears `stations_connected` so the track's state
matches a >2-element track's exactly (`Track.lua:506`, `:511`, `:682-684`,
`Station.lua:1224-1234`). The savegame pass runs on **`OnMsg.PostLoadGame`**, not LoadGame:
`Msg("LoadGame")` fires before `FixupSavegame` (`Savegame.lua:810-813`) and the shipped
`SavegameFixups.ConvertTrackPowerLinks` (`Station.lua:1395-1420`) tears down and rebuilds
these very links — a LoadGame-time pass would race it (the F35 lesson).
Probe: `TrackTunnelPowerBridge` in `40_Probes_Wave4.lua`. Playtest: PT-40.

### F66 — Station↔tunnel connector hex ping-pong (P2, med-high)  `[fixed: Code/Fix_TrackConnectorPingPong.lua]`
With a 1-hex gap, both buildings project their connector element onto the SAME hex;
`TrackConnectedObjBase:CreateConnectorElements` (`TrainTransport.lua:126-130`) deletes the
other's element (assert assumes never two live owners) → victim's `Done` reschedules its
own `CreateConnectorElements` → infinite steal loop; whichever lacks the element fails
`GetConnectedTrack`/`GetDestStation` (`Track.lua:320-355`) → no route ever forms. Also:
double-turn constraint refuses connections silently (`TrackElement.lua:336-345`).
Workaround: ≥2-hex gap. **Fix:** patch `CreateConnectorElements` to not delete elements
owned by a live non-destructing building (breaks ping-pong); full shared-hex support more
invasive.
*Confirmed, and the loop's return leg is now pinned down:* `TrackGridElement:Done`
(`TrackElement.lua:193-199`) spawns a game-time thread calling
`station:CreateConnectorElements()` for any still-live `self.station`, so destroying a
neighbour's connector is precisely what makes the neighbour rebuild it and take the hex
back. The shipped `assert(not IsValid(el.station) or IsBeingDestructed(el.station))`
(`TrainTransport.lua:127`) already STATES the invariant the loop violates — and asserts do
not unwind in this engine, so it is a log line and the steal proceeds anyway. The fix is
therefore to enforce the shipped assert's own condition, nothing more: a hex whose element
belongs to a different building that is alive and not being destructed is left alone.
Implemented as a full replacement of `CreateConnectorElements` (`TrainTransport.lua:114-154`)
because the decision is inside the per-spot loop; the copy is token-identical except that one
condition, and the assert line is dropped (it cannot unwind, and its other-owner condition is
now enforced by the guard. *Corrected by the QA audit 2026-07-25: an earlier version said
keeping it "would print on every legitimate clear of an abandoned element" — false; the
assert is TRUE (silent) for a dead or destructing owner. The case where it would print is a
`force` rebuild of the building's own live element, e.g. Station.lua:1352.*). Ordinary
clears are untouched: a plain track element on the hex has `station == false`, so
`IsValid(el.station)` is false and it is still removed, and `force` still rebuilds the
building's own element. The second building then simply gets no connector on that hex — the
same outcome as the ≥2-hex-gap workaround, without the fight. Genuinely sharing one hex
between two owners is a redesign of the connector model, not a defect repair (FIX_POLICY §4).
The "double-turn constraint refuses connections silently" half (`TrackElement.lua:336-345`)
is NOT addressed — it is a separate placement rule, not part of this loop.
Probe: `TrackConnectorPingPong` in `40_Probes_Wave4.lua`. Playtest: PT-41.

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

### F70 — Edit Payload silently refills from the policy template (P2, med-high)  `[fixed: Code/Fix_PayloadTemplateRefill.lua — the legacy LanderRocketCargoRequest copy is unreachable in Relaunched, see below]`
`CargoRequestNew:RetrieveRequests` (`CargoRequestNew.lua:194-212`): rows with stored
request 0 are refilled from the flight-policy cargo template every dialog open (template
suppressed only during `CmdLoad`; every landing zeroes requests via `CmdUnload`). Mars→
asteroid template: 5 Drones, 20 Metals, 5 Polymers, 5 MachineParts, 5 Electronics, 3
extractor prefabs (`FlightPolicyDef.lua:93-131`). Legacy first-trip guard also broken
(`LanderRocketCargoRequest.lua:116` checks flag on wrong object). "Loads what it wants."
**Fix:** first-use flag on the transporter gating `resolve_loc_cargo_template`.
*Implemented as sketched* for `CargoRequestNew` (the dialog `UniversalRocketBase` opens,
`UniversalRocket.lua:2232`): full replacement of `RetrieveRequests` (:179-221) with the
template read gated on a new `transporter.SMRFixPack_payload_set`, plus a pre-wrapper on
`CargoRequestNew:Apply` (:341-355, the payload-confirm path) that sets it. The file-local
`resolve_loc_cargo_template` (:166-177) had to be reproduced — a file-local is unreachable
— and the shipped `assert(transporter, ...)` on :181 is dropped, since assert does not
unwind in mod code and the very next line already returns.
*Second copy of the defect, resolved as NOT ACTIONABLE 2026-07-25 (wave 3).* The legacy
`LanderRocketCargoRequest:RetrieveRequests` (`:94-129`) has the same bug — its guard reads
`self.initial_landing_completed` where `self` is the DIALOG, while the flag lives on the
rocket (`LanderRocket.lua:16,1081-1082`), so it is always nil and the template always
refills. The queued question was whether the legacy class is reachable in Relaunched at
all. It is not, on three independent counts:
* that dialog is constructed only from `LanderRocket.lua:502` and `:1295`, both methods of
  `LanderRocketBase`;
* no new `LanderRocketBase` can be built — `OnMsg.NewGame` locks BOTH lander buildings
  (`LanderRocket.lua:1129-1132`) and only `UniversalLanderRocketBuilding` is ever unlocked
  again (`Asteroids.lua:406-411`, on AdvancedPassengerModule + MicroGLanders).
  `LockBuilding("LanderRocketBuilding")` has no matching `UnlockBuilding` anywhere in Src;
* any legacy lander in an old save is migrated away before it can be used —
  `SavegameFixups.UpdateOldRockets` → `convert_lander_rocket` →
  `rocket:ChangeClass("UniversalLanderRocket")` (`RocketCompatibility.lua:627-637`, :972).
  Nothing places the legacy class directly; even the Space Miner commander's free lander is
  a `UniversalLanderRocket` (`CommanderProfilePreset.lua:54`).
So the one-word correction would patch a dialog no reachable object can open. Not shipped —
patching dead code costs compatibility and buys nothing (FIX_POLICY §4). F70 is therefore
complete, not partial.

### F71 — Auto-export allocates capacity alphabetically (P2, med)  `[fixed: Code/Fix_LanderCargoRatchet.lua — folded into the F68 replacement of the same function]`
`CreateAutoCargoRequest` iterates `sorted_pairs` (`UniversalRocket.lua:1736-1758`) —
alphabetical: Concrete..Metals..Polymers before PreciousMetals/PreciousMinerals; WasteRock
is a legal export (`FlightPolicyDef.lua:393,401`). 80,000kg budget consumed by bulk before
valuables; 1-sol forced depart (`AutoDepartTimerSols`, :1773-1775) ships whatever loaded
first. **Fix:** value-ordered allocation (resupply price descending) in override.
*Implemented differently, on better evidence:* no price sort is needed — the game already
publishes the intended order, and does so per flight policy. Every
`GetAutoModeAllowedResources` returns the same value-descending list —
`{ PreciousMinerals, Electronics, PreciousMetals, MachineParts, Polymers, Food, Fuel,
Metals, Concrete, WasteRock }` (`FlightPolicyDef.lua:133-141`, `:232-240`, `:390-396`;
`Seeds` last where it appears) — and `UniversalRocketBase:GetAllowedResources` (`:649-658`)
already calls that very function for this rocket, discarding the order only because it
wants a set (`table.invert`). The fix therefore walks the threshold table in the policy's
own order and falls back to the shipped `sorted_pairs` order for anything the policy does
not list (including the `return -- all` policies), so the SET of resources considered is
unchanged and only the sequence moves. A resupply-price sort would additionally have been
wrong for the asteroid→Mars leg, where the Earth import price is not what the cargo is
worth. The policy lookup is wrapped in `pcall`: the policy functions read back from the
rocket (`GetDepartureLocType`), so an unexpected rocket state degrades to the shipped
order instead of erroring.
*Scope note:* the reordering also covers the import direction (`import_below`) — it is the
same loop and the same shared weight budget, and importing Concrete ahead of Electronics
wastes the hold the same way.
*Folded into `Fix_LanderCargoRatchet.lua`* rather than shipped as its own file, because F68
already fully replaces `CreateAutoCargoRequest` and two independent replacements of one
function cannot coexist. The shipped `assert(res_type == "Resource")` is dropped from the
copy in the same pass (assert does not unwind in mod code; it would only add log noise).
Probe: `AutoExportPriority` in the Test Kit's `30_Probes_Wave3.lua`.

### F72 — "No available Asteroid Landers" with a lander on the pad (P2, med)  `[fixed: Code/Fix_AsteroidLanderAvailable.lua]`
`PlanetaryAsteroidVisitPossible` (`PlanetaryView.lua:433-444`) and
`GetRocketsForExpedition` (`PlanetUI.lua:1623-1651`) exclude any lander that is busy
(CmdLoad/CmdUnload) or has stale `arrival_loc` (payload dialog Cancel skips CancelFlight
during CmdLoad, `CargoRequestNew.lua:389-399`). No per-asteroid occupancy lock exists
(`IsDifferentAsteroidLocation` compares Map to MapDescriptor — never false,
`PlanetUI.lua:1696-1699`). **Fix:** accept landed re-targetable landers in both checks.
*Implemented as the gate half only, on better evidence.* The two functions are not
equally at fault — they DISAGREE, and only one of them blocks the player:
* `GetRocketsForExpedition` (`PlanetUI.lua:1623-1635`) keeps every non-supply-pod
  `UniversalRocketBase` with `departure_loc == OurColony`, no `arrival_loc`, and the
  selected spot among its available destinations. It never looks at `command`.
* `PlanetaryAsteroidVisitPossible` — the gate the VISIT ASTEROID action consults before
  opening that list (`PlanetaryViewAsteroidResources.generated.lua:37-41`) — additionally
  demands `command == "CmdWaitOrder"`.
So a lander parked at the colony with nothing assigned but running any other command is
offered by the list and refused by the gate. The everyday case is `CmdUnload`
(`UniversalRocket.lua:478-510`), which lasts as long as the drones take to empty the hold
and forever when there are no drones or nowhere to put the cargo; `CmdWaitMaintenance`
(`:586-630`) is the other. The fix is a chained post-wrapper on the gate (permissive only:
the shipped predicate runs first and its every acceptance is preserved) whose extra scan
mirrors the list builder's predicate, supply-pod exclusion included. `GetRocketsForExpedition`
itself is left alone — it is the more correct of the two and needs no widening.
*Not actionable as stated:* the "stale `arrival_loc`" half. `UICancelManualModeRequest`
(`CargoRequestNew.lua:389-399`) does skip `CancelFlight` while the rocket is in `CmdLoad`,
but the resulting state is a rocket genuinely committed to a destination and loading for
it, not a stale flag — both the gate and the list are right to exclude it, and the player
cancels that flight from the rocket's own infopanel. Changing the dialog's Cancel
semantics would be a redesign, not a defect repair (FIX_POLICY §4).
*Observed, deliberately not touched* (both are permissive failures, neither blocks):
(a) the gate's legacy `LanderRocketBase` branch mis-associates — `IsKindOf(rocket,
"LanderRocketBase") and rocket.command == "Refuel" or rocket.command == "WaitLaunchOrder"
or (...)` parses as `(A and B) or C or D`, so the class test guards only the first term;
(b) `IsDifferentAsteroidLocation` (`PlanetUI.lua:1696-1699`) compares `city:GetMap()` with
`selected_spot.map`, which is a MapDescriptor on an asteroid spot, so it always answers
"different" and the action's disable branch never fires.
Probe: `AsteroidLanderAvailable` in the Test Kit's `30_Probes_Wave3.lua`.

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

### F74 — RC Transports can be ordered onto trade / refugee rockets (P2, high)  `[fixed: Code/Fix_RocketInteractGuard.lua]`
*Found by screening F56 in wave 4.* `RCTransport:CanInteractWithObject`
(`Lua\Units\RCTransport.lua:338-385`) opens with a hard refusal —
`if IsKindOfClasses(obj, "TradeRocketBase", "RefugeeRocketBase") then return false end`
(:341) — that no Relaunched rocket can match. Trade and refugee rockets are now
`UniversalTradeRocket` / `UniversalRefugeeRocket`, generated with
`__parents = { "UniversalRocketBase" }`
(`Lua\BuildingTemplate\UniversalTradeRocket.generated.lua:4-5`,
`UniversalRefugeeRocket.generated.lua:4-5`), whereas the named classes sit on the other
branch: TradeRocketBase/RefugeeRocketBase → `SupplyRocketBase` → `RocketBase`
(`RocketTrade.lua:1-2`, `RocketRefugee.lua:1-2`, `SupplyRocket.lua:1-2`), and
`UniversalRocketBase` is not a `RocketBase` (`UniversalRocket.lua:28-40`). The guard is
dead in every Relaunched game, not only converted saves: new event rockets are placed as
the Universal classes (`SA_Gameplay.lua:2788`, `:2929`;
`ClassDef-Effects.generated.lua:154`, `:3134`) and old saves are converted to them on load
(`RocketCompatibility.lua:522`, `:964`, `:1050`).

Conversion slip, not a design change — five sibling rocket tests in the SAME file were
updated to name both families and only this one was missed: `:314`, `:421`, `:731`,
`:1137` (all `IsKindOfClasses(x, "SupplyRocketBase", "UniversalRocketBase")`) and `:916`
(the `IsRocketClass` shim, `RocketCompatibility.lua:1037-1046`). FIX_POLICY §4's
"the same author wrote it correctly elsewhere" test, five times over.

Player-visible: the RC Transport load/unload cursor accepts an event rocket, so cargo can
be pushed into or pulled out of a rocket with no player cargo bookkeeping. Matches the
Relaunched report "rival colony rockets glitch permanently if refilled from RC Transport
(1.07)" in `RESEARCH.md`.

**Fix:** pre-wrappers (FIX_POLICY §1.4) on `CanInteractWithObject` and — belt-and-braces —
`InteractWithObject`, restating the shipped rule for the Relaunched class names before
deferring to the original. The gate is complete on its own: `UnitDirectionModeDialog`
stores an interaction target only when `CanInteractWithObject` answers truthy
(`UnitControl.lua:470-471`, `:488`), and both the direct-order path (`:401`) and the
transport-route path (`TransportRouteInteractionHandler.lua:50`) act on that stored target.
Wrapping the class field also covers `RCHarvester` (`:127`, `:139`) and `RCConstructorBase`
(`:353`), which call these through the class table.

*Two sibling stale reads found and deliberately NOT changed:* `CanUnloadAt` (`:265`) and
`FullAndCanUnload` (`:285`) still test `IsKindOf(depot, "SupplyRocketBase")`, so their
export-request-aware rocket branch is likewise dead for Universal rockets and both fall
through to the generic depot branch. Restoring those would REMOVE a capability Relaunched
clearly intends — `CanLoad` (`:314`) and `TransferResources` (`:1137`) were converted
precisely so an RC Transport can service a lander, which is core asteroid play. The
resulting behaviour is permissive (a manual unload into a player rocket that is not
exporting is allowed where the original demanded a matching export request), and permissive
failures do not block a player. Recorded here so a later pass does not "fix" it blind.
Probe: `RocketInteractGuard` in the Test Kit's `40_Probes_Wave4.lua`. Playtest: PT-39.

### F75 — Six Last Transmission storage opinions never count; one reads the wrong grid (P2, high)  `[fixed: Code/Fix_LastTransmissionStorage.lua]`
*Found by implementing F22, which names these conditions as its victims — repairing F22
alone would not have made any of them work.*

**(a) inert.** `FactionLikeGlobalCondition:Eval`
(`Lua\ClassDefs\ClassDef-Factions.generated.lua:843-849`) consults exactly one property:
`if not self.Condition or not self.Condition.eval(UIColony) then return 0 end`. The six
storage entries in `Data\FactionDef\LastTransmission.lua:94-192` —
`TLEPowerStorage2Sols`, `TLENoPowerStorage`, `TLEWaterStorage2Sols`, `TLENoWaterStorage`,
`TLEOxygenStorage2Sols`, `TLENoOxygenStorage` — put their `ScriptConditionList` on
**`Prerequisite`** instead. `Prerequisite` is real but is only a gate:
`FactionLikeBase:EvalPreconditions` (`:672-688`) calls it to decide whether the like is
considered, and `FactionDef:EvalApproval` (`:190-197`) then adds `like:Eval()` — which is 0
forever. The slip is local to these six: the other seven `FactionLikeGlobalCondition`s in
the same file set `Condition` (`:208, :224, :240, :256, :281, :298, :313`) and the one at
`:266-292` sets BOTH, so the distinction was understood; a sweep of all 29 shipped
FactionDefs found the pattern nowhere else. Not a quiet failure either — `EvalApproval`
(`:181-187`) surfaces the `HowTo` of any positive like that evaluated to 0 as an
outstanding goal. *(Wording corrected by the QA audit 2026-07-25: the `Prerequisite`
gate (`:682`) HIDES the like while storage is low, so the goal appears only AFTER the
player satisfies it — the like is shown as unmet precisely while it is met, and
disappears again when storage drops. Same defect, perverse in the opposite direction
from the earlier "permanently advertises" phrasing.)*

**(b) wrong grid.** `TLEOxygenStorage2Sols` (`:160-175`) measures POWER. Explanation, HowTo
and Id all say Oxygen, but its nested `ScriptCheckGridGlobalStorage` never sets `GridType`,
which defaults to `"Power"` (`ClassDef-Conditions.generated.lua:2034-2035`), and the
generated `eval` faithfully reads `GetGridGlobalStorage("Power")`. Its negative twin
`TLENoOxygenStorage` sets `GridType = "Oxygen"`, as do both Water entries — only this one
was missed.

**Fix:** preset data patch (FIX_POLICY §1.1) from `OnMsg.DataLoaded` (+ `DataChanged`):
(a) move the condition list from `Prerequisite` to `Condition`, leaving `Prerequisite`
false — the same test, in the place `Eval` reads, leaving the entries structurally
identical to their working siblings; (b) set the missing `GridType` and rebuild only that
entry's `eval` from the corrected fields, mirroring the shipped CodeTemplate
`"GetGridGlobalStorage(self.GridType) $self.Condition $self.Value"`
(`ClassDef-Conditions.generated.lua:2040`). Every other entry keeps its shipped eval. An
entry that already carries a `Condition` is left exactly as found, so a game hotfix simply
deactivates the fix.
Probe: `LastTransmissionStorage` in `40_Probes_Wave4.lua`. Playtest: PT-42.

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
