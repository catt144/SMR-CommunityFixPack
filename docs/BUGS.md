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
| F03 | Upgrade buffs leak & stack after salvage/demolish        | P1  | high | tested |
| F04 | Night-shift workers never return to work after midnight  | P1  | high | fixed  |
| F05 | Milestone completion crashes (NoTerraforming/NoPolitics) | P1  | high | tested |
| F06 | Philosopher's Stone mystery can hang forever             | P1  | med+ | fixed  |
| F07 | St. Elmo's Fire "free wisps" gives ~1/1000 power         | P1  | high | fixed  |
| F08 | Tourist star-rating applicant bonus inverted             | P1  | high | tested |
| F09 | Tourist Satisfaction drifts down (asymmetric thresholds) | P1  | high | fixed  |
| F10 | Faction funding conditions always error (BlueSun/Brazil/Russia) | P1 | high | wontfix |
| F11 | Train wedges at platform (`table.remove` misuse)         | P1  | high | fixed  |
| F12 | "Low Storage" warning never fires for Food/maintenance   | P2  | high | tested |
| F13 | Command Center resource rows show no numbers             | P2  | high | tested |
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
| F36 | Universities overtrain geologists (unmanned extractors)  | P2  | high | tested |
| F37 | Ghost farm oxygen modifier survives salvage/demolish     | P1  | high | fixed  |
| F38 | Destroyed tunnels rejoin pathfinding after save/load     | P2  | high | fixed  |
| F39 | Second Artificial Sun ignored by solar panels            | P2  | high | folded into D04 `Opt_MultipleSuns` 2026-07-27 (latent in unmodded game; standalone fix deleted); absorbed fix play-verified — PT-50 PASS |
| F40 | Dust Sickness infects Biorobots (androids)               | P2  | high | fixed  |
| F41 | Gene Forging tech has no effect                          | P2  | high | fixed  |
| F42 | Buildings placeable on active dust devils                | P3  | high | blocked|
| F43 | Layout construction bypasses tech locks                  | P3  | high | fixed  |
| F44 | One-hex track salvage can delete the entire track        | P1  | high | tested |
| F45 | Damaged tracks can't be salvaged at all (sort crash)     | P1  | high | tested |
| F46 | Trains dump cargo at stations with resource disabled     | P2  | high | fixed  |
| F47 | Track salvage refunds ~1 hex for whole track / 0 partial | P3  | high | tested |
| F48 | Station-connector savegame fixup no-op (paren misplaced) | P3  | high | blocked|
| F49 | Train minors bundle (palette, split kills trains, etc.)  | P3  | med  | fixed* |
| F50 | Auto-rockets kick approaching drones to Idle every hour  | P1  | high | tested |
| F51 | Transport-mode cache never sees new shuttles (homeless)  | P1  | high | tested |
| F52 | Colonists still walk ≤400m in vacuum past passages       | P1  | high | tested*|
| F53 | Arrivals hike to unreachable "safety dome" and die       | P1  | high | fixed  |
| F54 | Switched-off shuttle hubs count as transport available   | P2  | med+ | tested |
| F55 | Open domes: drone access lost + unreachable-forever cache| P1  | med  | fixed* |
| F56 | Auto RC Transports never offload rockets                 | P2  | high | wontfix|
| F57 | Drone/transport minors bundle                            | P3  | med  | fixed* |
| F58 | Invisible residence reservations never expire            | P1  | high | fixed* |
| F59 | Freed housing never notifies homeless (12h retry lag)    | P2  | med  | fixed* |
| F60 | Dome free-space uses `working`, assignment `ui_working`  | P2  | med  | fixed  |
| F61 | Home dome's migration toggle blocks outbound shopping    | P1  | med+ | wontfix — superseded by D03 (PT-14: toggle is a quarantine by design); fix DELETED 2026-07-27 |
| F62 | Services reach 1 passage hop only, never trains          | P2  | high | wontfix|
| F63 | Universities invisible to emigration (no students)       | P2  | high | wontfix|
| D01 | Rockets don't auto-refuel/auto-export rare metals        | dsgn| high | opt-in fix |
| D02 | Dismissed "not working" warnings re-nag every 4 game h   | dsgn| med  | built 2026-07-27: `Opt_AcknowledgedWarnings` (opt-in, probe PASS in the opt-in leg; PT-48) |
| D03 | No way to block dome move-ins short of full quarantine   | dsgn| med  | tested 2026-07-28: `Opt_ResidencyControl` (opt-in; probe PASS + PT-49 PASS in full, archived) |
| D04 | Artificial Sun is build-once; second-sun support unused  | dsgn| low  | tested 2026-07-27: `Opt_MultipleSuns` (opt-in, absorbs F39's fix) — PT-50 PASS in full incl. reload + live limit off/on |
| D05 | Opt-in modules had no player-usable enable surface       | dsgn| high | tested 2026-07-27 late: native Mod Options toggles (live both ways, restart-persistent) — PT-51 PASS in full |
| D06 | Drone assignment has no cross-hub locality (far fleets claim near work) | dsgn| high | built 2026-07-28: `Opt_DroneOverhaul` core v1 (opt-in) — closest-fleet-first claim gate + repair moonlighting + DroneReport telemetry; PT pending (attended, multi-iteration) |
| F64 | Station demolition permanently leaks train prefabs       | P1  | high | fixed  |
| F65 | Station-at-tunnel never bridges the power grid           | P2  | med  | fixed  |
| F66 | Station↔tunnel connector hex ping-pong (never connects)  | P2  | med+ | tested |
| F67 | Auto-lander launches empty, ping-pongs Mars↔asteroid     | P1  | high | fixed  |
| F68 | Hourly auto-request ratchet unloads lander's own cargo   | P1  | high | fixed — over-draw finding 2026-07-28, mechanical repair queued (entry) |
| F69 | Manual landing dumps the return fuel (stranded landers)  | P1  | high | fixed  |
| F70 | Edit Payload silently refills from policy template       | P2  | med+ | fixed  |
| F71 | Auto-export fills capacity alphabetically (waste rock)   | P2  | med  | tested 2026-07-28 (PT-32: live two-resource priority inversion + probe order coverage) |
| F72 | "No available landers" while a lander sits on the pad    | P2  | med  | fixed  |
| F73 | Asteroid colonists idle outdoors; no shelter reflex      | P1  | med+ | fixed  |
| F74 | RC Transports can be ordered onto trade/refugee rockets  | P2  | high | tested |
| F75 | Last Transmission storage opinions inert; Oxygen reads Power | P2 | high | fixed |
| F76 | Depot resource picker renders off-cursor, unclickable    | P1  | high | todo (found live 2026-07-27; wave-6) |
| F77 | Extender working-flap tears down + rebuilds whole uplink hub; fleet Idle churn | P2 | med+ | fixed (built 2026-07-28 with the D06 core; PT pending) |
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

### F02 — Meteors strike ~every 6h instead of 35–115h  `[fixed*: Code/Fix_MeteorFrequency.lua — REOPENED by PT-01 FAIL; REWORKED 2026-07-26 with a stall watchdog + forensics; root cause NOT yet pinned, PT-01 re-run will capture it]`

**PT-01 FAIL (2026-07-25, user confirmed NO reloads):** Variant B, max-threat map.
Natural strikes at ~sol 5.5, 7.5 (+60h), 8.4 (+39h), 10.3 (+39h); 3 Sensor Towers built
~sol 10.5; warning received; strike at sol 12.5 (logger printed "+57 game hours") — then
**nothing through sol 36** (~560+ game hours of silence, band is 35-60h) with no reload
to re-roll the interval. The logger prints per MeteorsDisaster call, so silence = the
thread stopped calling, not a logging gap.

**Regression hunt (2026-07-26) — every static explanation FALSIFIED against the
playtest log (Mars.exe-20260725-19.04.10):**
- The session is one uninterrupted run: exactly one `Load Game:` marker (log:141) at
  boot, day counters monotonic 22→36 in the daily errors, wave-3 roster (the merge
  and all wave-4/5 fixes postdate the playtest). The load-time re-roll story is dead.
- No `[LUA ERROR]` anywhere near the stall (silent window ~0:45–1:11 real time shows
  story bits and Quick Builds but zero errors) — thread errors always log, so the
  loop did NOT die of an error. All logged errors are the PT-03 track-debris family,
  and the debris was created at day ~21, AFTER the silence began (due ≤ day ~14).
- The tower math is bounded: with 3 towers `GetDisasterWarningTime` = Min(6h+12h·3,
  75h) = 42h (`MapSettings.lua:94-98`, `_GameConst.lua:125-126`) and the fixed body's
  two sleeps total `Max(spawn−warning,1s) + Min(spawn,warning)` ≤ spawn+1s ≤ 60h on
  Meteor_VeryHigh (spawntime 1.05M+0..750k ms). It cannot oversleep.
- The descriptor re-read cannot go silently nil at sol 12: the only nil paths are
  mapdata `"disabled"` (strikes happened) and `OverrideDisasterDescriptor` returning
  nil past the **80%** Atmosphere `MeteorStormStop` threshold
  (`TerraformingDisasters.lua:69`, `TerraformingParam.lua:80-84`).
- Nothing in Src or either mod deletes/restarts the thread mid-game (the only
  `RestartGlobalGameTimeThread` callers are `_fixup.lua` PostNewGame and the fix's
  own LoadGame handler; `OnMsg.DoneGame` fires only when leaving the game).
- The first MeteorStorm was due in the SAME window (`birth_hour` = 250h + 0..25h,
  `Meteors.lua:316`; the tower-lengthened 42h warning also explains the "warning
  received ~sol 10.5" as the storm countdown) and no 1-3-sol storm was ever observed
  — so BOTH disaster threads went quiet around t≈8.2-8.3M. Whatever stopped them is
  outside both loop bodies (scheduler/persist side) and is only capturable live.

**Rework (2026-07-26):** the fixed body now heartbeats a phase marker
(`SMRFixPack.MeteorsBeat`, session-local, zero closure upvalues so the persisted
thread keeps the engine-proven persistence shape); the silent top-of-body exit logs;
a daily `OnMsg.NewDay` watchdog (`SMRFixPack.MeteorsWatchdogCheck`) restarts a
provably overdue thread — threshold spawntime+random+75h+1 sol, so no false
positives — and logs the pre-death state (**thread ALIVE-but-stuck vs DEAD** + last
phase), giving up loudly after 3 restarts; the LoadGame restart now logs a necropsy
of the persisted thread it replaces — loading the user's sol-36 save answers
dead-vs-stuck for the wedged thread directly. Probe reworked to `behavior` kind
(drives the watchdog with a synthetic descriptor + fabricated stale heartbeat, so it
discriminates in the retail sandbox instead of SKIPping as `[install]`).
**PT-01 re-run needed:** meteors resume on load; if the stall recurs, the watchdog
line names the phase and state — that IS the diagnosis.
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

### F03 — Upgrade buffs leak & stack after salvage/demolish  `[tested: Code/Fix_UpgradeModifierLeak.lua stops new leaks; Code/90_SaveSanitizer.lua clears the ones already in a save — PT-02 PASS 2026-07-25]`
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

### F05 — Milestone completion crashes (NoTerraforming/NoPolitics)  `[tested: Code/Fix_MilestoneCrash.lua — PT-05 PASS 2026-07-26 ("A dream fulfilled" popup at 18/18 with 9 terraforming milestones hidden; zero LUA errors in-log)]`
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

### F08 — Tourist star-rating applicant bonus inverted  `[tested: Code/Fix_TouristApplicants.lua — PT-06 PASS 2026-07-27, 5★ +23/$544.5M vs tanked ≤2★ +7/$94.5M]`
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

### F10 — Faction funding conditions always error  `[CLOSED wontfix 2026-07-27 — PT-36 PASS on a real save; premise falsified twice over]`
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
**PT-36 PASS (2026-07-27, Stargazer save, sol 45+):** all three
`GetLastSolsFundingByType(10, …)` calls printed `0` cleanly over a real save's
income history — a maximally nil-heavy window (the colony had idled past the
12-sol retention ring, `Funding.lua:86`, so nearly every hour entry was nil) —
with zero `Funding.lua` errors in the log. The `pairs(nil)` tolerance holds on
organic state. **CLOSED `wontfix`; `Fix_FactionFundingCheck.lua` deleted from
the repo and its commented metadata line removed** (rollback if ever needed =
restore both from git history, commit 40f51da or earlier). The TestKit
`FactionFundingCheck` probe is deliberately KEPT: it drives the SHIPPED
function and PASSes both A/B legs (it is the baseline's expected "1 PASS"), so
it now serves as a standing canary that a future game patch hasn't broken the
shipped body — expected A/B numbers stay unchanged.

### F11 — Train wedges at platform (`table.remove` misuse)  `[fixed: Code/Fix_TrainPlatformWedge.lua]`
`Lua\Units\ColonistTransport.lua:541-547` (`ExitVehicle` stale-passenger guard) —
`table.remove(vehicle.units, self)` needs an integer pos; intended API is
`table.remove_entry`. When the guard fires (dev comment: CargoTransporter abduction),
the error aborts before `DiscardTransportTicket`; `Train:UnloadTrain`
(`Units\Train.lua:443-453`) then spins forever → train permanently blocks platform.
**Fix:** replace `Colonist.ExitVehicle` with one-line-corrected copy (`table.remove_entry`).

## P2 — wrong numbers / notable misbehavior

### F12 — "Low Storage" warning never fires for Food/maintenance resources  `[tested: Code/Fix_LowStorageWarning.lua — PT-07 PASS 2026-07-27 on the repaired build: Food fires once/steady a sol/clears silently on organic recovery; Machine Parts fires once ("1 Sols, 12h") after forced-malfunction consumption; first run caught the second defect below]`
`Lua\ResourceTracking.lua:218-224, 229-234` — `supply*24/v*24` = `((supply*24)/v)*24`,
always 0 or ≥24 under integer division, guard requires `0 < x < 3` → unsatisfiable.
Grid branches (:259-303) are correct. Consts: `_GameConst.lua:4,10-11`. **Fix:** replace
`ResourceTracking.GatheredResourcesOnHourlyUpdate`: `MulDivRound(supply, HoursPerDay, v)`
vs `MinDays* × HoursPerDay`.

**Second defect found live in PT-07 (2026-07-27) — maintenance/food "Food"-key
collision; REPAIRED same day, A/B pending.** With the warning finally able to
fire, the user reported a flash + the "Warning! Insufficient resources" voice
replaying every game hour. Console instrumentation (wrapping AddNotification /
RemoveNotification / RemoveObjectFromNotification, then per-city tick markers)
pinned it: the notification was destroyed and recreated once per hour INSIDE the
surface city's own tick — remove first, add after. Root cause: `"Food"` appears
in `maintenance_resources_consumed_yesterday` too, and the maintenance loop and
the dedicated food branch write the SAME `"Food"` object key on the SAME
`InsufficientResources` notification. The maintenance loop runs first, computes
maintenance-based hours (guard fails for Food), takes its else-path and
`RemoveObjectFromNotification("Food", …)` — deleting the food branch's entry;
as the only object, that destroys the whole notification, and the food branch
recreates it a line later → FX + voice replay hourly (voice plays only on
whole-notification creation: `VoicePerObject` is false on this preset,
`NotificationUI.lua:197-207`). Latent in the shipped body — with the broken math
neither branch could ever add, so there was no entry to fight over. Diagnostic
red herrings ruled out on the way: user dismissal (the `dismissed` flag was
false on every destroy; the 2-real-minute `SuppressTime` re-nag is D02's
territory, not this), threshold flapping (reproduced with farms OFF, monotonic
70h < 72h), object validation (`IsObjValid`/`IsValidMapObject` both pass string
keys), and a second stale body (City and ResourceTracking dispatch the same
function address). **Repair:** the maintenance loop now skips `k == "Food"` —
the food branch owns that key (`-- FIX (F12, second defect)` block in the fix
file). PT-07 re-run + fresh A/B pair pending.

### F13 — Command Center resource rows show no numbers  `[tested: Code/Fix_CommandCenterNumbers.lua — PT-08 PASS 2026-07-27 (all 11 previously-blank rows show numbers; cross-checked against the HUD bar, exact match modulo live-sim drift)]`
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

### F18 — Independence terraforming tech gives 10% not 20%  `[fixed: Code/Fix_IndependenceTerraforming.lua — preset half + savegame sweep for already-researched saves (2026-07-26)]`
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
*Formerly-open half — saves where the tech was ALREADY researched kept the 10% —
CLOSED 2026-07-26 with a LoadGame sweep (design prompted by the user's "reset the
tech" suggestion, minus the reset).* `Effect_ModifyLabel:OnApplyEffect`
(`Lua\MarsGameEffects.lua:161-178`) stores the research-time Modifier on the colony
**keyed by the effect object** (`colony:SetLabelModifier(self.Label, self, …)`), so
the stale -10 modifier is directly addressable — no id reconstruction. The recorded
risk (the `parent` argument decides the Modifier's `id`) dissolved on reading the
shipped applier: `GameEffectsContainer:EffectsApply(player)` passes the CONTAINER
(the tech preset) as parent (`CommonLua\Classes\GameEffect.lua:36-40`), so the
sweep's `effect:OnApplyEffect(UIColony, tech)` is argument-identical to research
and replaces the stored modifier under the same key with the corrected -20.
Positive identification before acting: fix active, preset in its corrected state,
tech researched, stored modifier present and carrying exactly the old -10×scale —
anything else is left alone (unexpected amounts loudly). Idempotent by state, no
first-load flag needed; the engine's own
`SavegameFixups.Move_Effect_ModifyLabel_FromCitiesBackToColony` is precedent for
surgery on these tables. Exposed as `SMRFixPack.IndependenceTerraformingSweep`
(probe test hook takes a synthetic colony).
Probe: `IndependenceTerraforming` in `40_Probes_Wave4.lua` — preset check + drives
the sweep both ways (stale modifier replaced through the effect's own
OnApplyEffect; correct one untouched).

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

### F36 — Universities overtrain geologists (P2, high behavior-confirmed)  `[tested: Code/Fix_UniversityOvertraining.lua — PT-24 PASS 2026-07-27, both halves]`
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

### F39 — Second Artificial Sun ignored (P2, high)  `[folded into D04 (2026-07-27): the fix now ships inside Code/Opt_MultipleSuns.lua; standalone Fix_SecondArtificialSun.lua DELETED (latent in unmodded game, PT-26); the absorbed binding fix is play-verified — PT-50 PASS 2026-07-27]`
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
**PT-26 (2026-07-27) — premise UNREACHABLE in the unmodded game.** The Artificial Sun
template is `build_once` + `wonder`, enforced colony-wide across all maps including
construction sites (`Building.lua:3691`, `BuildMenu.lua:711-719` counting
`UIColony.labels`; the tester's build menu showed the "You can build this building only
once" refusal with sun #1 standing — screenshot on file). Two suns can never coexist, so
`labels.ArtificialSun[1]` is always the only sun and the broken branch cannot be taken.
The fix is pure latent hardening in vanilla — harmless (the wrapper acts only when the
shipped body left a panel unlit AND a second in-range sun exists) but unverifiable by
play, and the original report almost certainly came from a modded or B&B-era game. The
tester banked the single-sun vanilla baseline while investigating: panels beside the lit
sun produce at night at −21% atmospheric effect (3.6 vs 4 daylight small, 9 vs 10 large).
Key portability fact: however a mod lifts the limit, the resulting state is identical —
two suns in `city.labels.ArtificialSun` — and that state is all the fix reads, so the
hardening works for any limit-lifting mechanism.
**RESOLVED — user decision 2026-07-27: fold the fix into a new opt-in module (D04
`Opt_MultipleSuns`)** so the pack itself provides the condition the fix needs (build
limit lifted) instead of shipping a default-pack fix for an unreachable bug. See the D04
entry for the spec; the standalone `Fix_SecondArtificialSun.lua` is deleted in the same
game-free leg that builds the module.
**DONE (2026-07-27 build leg):** `Fix_SecondArtificialSun.lua` deleted, the wrapper +
LoadGame sweep moved unchanged into `Code/Opt_MultipleSuns.lua`, probe reworked to the
opt-in SKIP-unless-opted pattern (now in TestKit `60_Probes_Opt.lua`), and the A/B
numbers renumbered in the same leg (see the D04 entry).

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

### F44 — One-hex track salvage can delete the entire track (P1, high)  `[tested: Code/Fix_TrackSalvageWipe.lua — PT-03 PASS 2026-07-26 (trim + curve visuals + repeated rebuild cycles), post-rework]`
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
orphaned elements already baked into a save.

**PT-03 re-run (2026-07-26): the F44 halves PASS** — orphan sweep removed the 40
debris elements on load; repeated build → salvage → rebuild cycles on straight AND
curve-ended tracks clean, train survives, partial-salvage Metals refund observed
(F47). **New finding during the F45 attempt, repaired same day: the split branch's
blind seeds crash on a dead element.** Destroying a repair site inside the deletion
zone ALSO destroys its broken twin (`TrackGridElement:Done`,
`TrackElement.lua:200-201`); the twin shares the site's `node_idx`, so it can sit
just outside the zone at the seed index, and the shipped
`el1, el2 = all_elements[last], all_elements[first]` then feeds a destroyed element
to `ExpandTrackFromElement`, which dereferences its map (`TrackElement.lua:718-719`,
`map` nil — the user's mod-flagged MouseEvent error; unreachable in the shipped game
because broken tracks could not be salvaged at all before F45). Repairs: each side
now seeds from its first still-VALID survivor (walking outward), a side with no
survivor is tolerated (the just-created empty `new_track` is destroyed; the debris
sweep handles stragglers), and the `LoadGame` sweep additionally purges DESTROYED
entries left inside track arrays by a pre-repair aborted split (the log line now
reports both counts). A/B re-verified same night (baseline 1/58/11, fixed
59/0/11, 0 ERROR). **F45's salvage step still needs its clean run** (the crash
aborted it) — retry procedure in the checklist under PT-03.

### F45 — Damaged tracks can't be salvaged at all (P1, high)  `[tested: Code/Fix_BrokenTrackSalvage.lua — wrapper + LoadGame sweep; PT-03 PASS 2026-07-26 (ReportBrokenTrack 7 sites / 0 bad; broken element salvaged cleanly)]`
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

### F47 — Track salvage refund ~1 hex for whole track; 0 for partial (P3, high)  `[tested: Code/Fix_TrackSalvageRefund.lua — PT-45 PASS 2026-07-26 (refund = stamped sections × 100 on live colony tracks; partial-salvage stockpiles observed)]`
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

**Composition repairs (2026-07-26; the two wave-4/5-audit MEDIUMs, both under-refunds):**
1. *Trim-to-empty lost the refund.* Half B's stand-down test was `IsValid(track) and
   elements is a table`, which also stood down when the F44 trim EMPTIED the track —
   an emptied track dies through `CanDelete` → `DoneObject`
   (`TrackElement.lua:203-205`) WITHOUT running `OnDemolish`, so nothing had refunded
   the trimmed stamps. `TrackBase:OnDemolish` stamps `demolishing = true` on the track
   first (`Track.lua:250`), a Lua-side field that survives the object's destruction —
   half B now stands down on that stamp alone, and captures the map and drop position
   before the original runs (both the element and the track can be dead afterwards).
2. *Construction-site early-return was broader than its reason.* The early-return
   existed for the repair-site delegation (`TrackElement.lua:451-453`, which re-enters
   the wrapper through the broken element), but it also swallowed clicks on PLAIN
   under-construction elements — whose deletion zone can contain stamped COMPLETED
   elements (`DemolishAndSplitTrack` sorts both arrays into one physical line). Only
   the delegation case returns early now; a plain site falls through and is
   snapshotted. Its own spend is returned by the construction machinery and never
   carries a completion stamp, so accounting the zone cannot double-refund.

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

**(b) RESOLVED — no defect (PT-46 PASS, 2026-07-25/26).** Mechanism confirmed as
tracked (no branch of `DemolishAndSplitTrack` touches `assigned_vehicles`), but the
consequence is benign: the user repeatedly deleted track on ACTIVE lines across two
sittings — the train is stored back as a prefab, the count stays accurate, nothing
vanishes. The engine's storage path handles a train on a removed element correctly;
there is nothing to fix.

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

### F50 — Auto-rockets kick approaching drones to Idle every hour (P1, high)  `[tested: Code/Fix_RocketDroneChurn.lua — PT-04 PASS 2026-07-25 (smooth loading/unloading, no churn)]`
`UniversalRocketBase:HourlyUpdate` (`UniversalRocket.lua:1357-1370`) → `CreateAutoCargoRequest`
→ `SetCargoRequest` → `UpdateCargoResourceRequests` (`CargoTransporterNew.lua:1238-1271`)
does `DisconnectFromCommandCenters()` + reconnect EVERY HOUR while landed;
`DroneControl:OnRemoveBuilding` (`DroneControl.lua:720-729`) sets every drone heading
there to `Idle`. Trips > 1 game hour can never complete; priority irrelevant. Aggravators:
`starting_drones = 0`, `exclude_from_lr_transportation = true` (shuttles never help).
Explains "drones ignore rocket cargo". **Fix:** wrap `UpdateCargoResourceRequests` to
suppress the disconnect/reconnect churn (requests mutate in place via
`TaskRequester:AddRequest`); one-time connect if never connected.

### F51 — Transport-mode cache never sees new shuttles (P1, high)  `[tested: Code/Fix_ShuttleTransportCache.lua — PT-12 PASS 2026-07-26 (cached mode=false verdicts recomputed to "shuttle" when the hub went live, homeless emigrated; cache dumps before/after in the archived PT-12)]`
`Colonist.lua:2504-2537` caches `(community,pos) → mode` incl. `false`, but
`shuttles_available` is not in the key and cache only flushes on train/passage events
(:2480-2488). Building/refueling a Shuttle Hub never flushes → `FindEmigrationDome`
(:2657-2698) skips domes forever. Explains homeless-despite-free-housing and cross-dome
seniors. **Fix:** wrap `FindTransportationModeToCommunity` to key on shuttle flag + flush
cache on ConstructionComplete/TTL.

### F52 — Colonists still walk ≤400m in vacuum past passages (P1, high)  `[tested*: Code/Fix_VacuumWalks.lua — PT-13 PASS 2026-07-26 (colonist used the passage; after the passage was destroyed the surface walk correctly resumed — the designed fallback). The no-passage surface walk stays allowed by design (refusing it would strand colonists on shuttle-less maps) — that half stays open]`
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

### F54 — Switched-off shuttle hubs count as transport available (P2, med-high)  `[tested: Code/Fix_ShuttleHubOffAvailable.lua — PT-34 PASS 2026-07-27 (hubs off: homeless stayed put inside, nobody waited outdoors; hubs back on: emigration resumed immediately)]`
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

### F61 — Home dome's migration toggle blocks outbound shopping/work/training (P1, med-high)  `[wontfix (user decision 2026-07-27, PT-14) — superseded by D03; Fix_HomeDomeMigrationGate.lua DELETED 2026-07-27 (git history restores it)]`
`Dome:GetService` (`Dome.lua:2900-2916`; same at 2927/2947/2959, `ShiftsBuilding.lua:250-254`):
outbound cross-dome access requires `self.accept_colonists` — the HOME dome's
"accept colonists" MIGRATION policy. Turning it off on a residential dome (routine) silently
stops residents shopping/working/training through passages; target-dome checks are separate
and correct (`Dome.lua:2880-2882`). Best match for "refuse to shop through a passage".
**Fix:** override the four sites, dropping home-side `accept_colonists` from the condition.

**PT-14 (2026-07-27) — premise FALSIFIED; retirement + `wontfix` proposed (user
decision pending).** The live run answered a third way: the observed behavior is the
DESIGNED behavior, and this entry's premise — that `accept_colonists` is only a
"whether outsiders may move IN" migration policy — is wrong. Evidence:
* The toggle's OFF state is titled **"Quarantined"** and its rollover promises exactly
  the observed lockdown: "Set the Immigration policy for this Dome. **Colonists are not
  allowed to enter or leave quarantined Domes.**"
  (`Data/XDef/sectionDome.lua:176-208` — icon off at :183, title at :185, rollover
  T365 at :208; same text on MicroG habitats and the Command Center dome rows). The
  blocking is neither silent nor unexplained — the UI states it. The low translation
  ids (T365/T7660/T8736) are reused original-game ids, i.e. the quarantine wording is
  carried forward, not new.
* The engine enforces the same reading everywhere else: `Colonist:FindEmigrationDome`
  returns early with the literal comment "quarantine, no one enters or leaves"
  (`Colonist.lua:2632-2634`), and the target-side gate carries a `--quarantine` comment
  (`Dome.lua:2907`). The controls PT-14's FIXED case was looking for exist as their own
  per-dome toggles — `allow_work_in_connected` ("Use Passages for work") and
  `allow_service_in_connected` ("Use Passages for services") — and the dome trait
  filter covers blocking move-ins WITHOUT a lockdown (its tooltip says setting it
  removes a quarantine, T363).
* Tester's verbatim observation (toggle off on a live dome, fix pack active): "As soon
  as I turned off accept colonists no one could work there[,] people slow[ly] left jobs
  and services as they finished shifts, no one could enter or leave anymore" — the
  promised lockdown, delivered by the untouched target-side gate (`Dome.lua:2881`) and
  the FindEmigrationDome resettle gate.
**The shipped fix actively subverts that design:** with the home-side `accept_colonists`
term removed from the four commute gates, a QUARANTINED dome's residents can still be
offered — and assigned — work/services/training through passages (no other home-side
check exists on the outbound commute path; FindEmigrationDome only gates resettlement).
That violates the tooltip's "not allowed to leave" half. The entry's "proof"
(`HasFreeWorkplacesAround` walks connected workplaces without the flag) is the same
class of permissive advisory-function inconsistency recorded on F62/F63, not evidence
of intent.
**Quarantine's designed consumers (surveyed 2026-07-27 at the user's question "is the
plague its only use case?" — it is not):**
* **Wildfire mystery (Mystery 8 / TheMarsBug):** infection spread is dome-local — each
  infected colonist daily has a 30% chance to infect a random resident of THEIR OWN
  dome (`InfectedDailyUpdate`, `Traits.lua:1155-1173`, reads
  `colonist.dome.labels.Colonist`; vaccination flips `g_StartVaccinating` off it).
  Cross-dome carriage happens only when an infected colonist RESETTLES (their `.dome`
  changes) — exactly the vector quarantine's `FindEmigrationDome` gate closes. A
  scripted background drip also seeds one random colonist colony-wide every ~5 sols
  (`SA_AddTrait` on the city "Colonist" label, `Scenario/Mystery 8.generated.lua:291-306`),
  so containment is partial by design. NOTE: commuting does NOT carry infection in
  code (labels are residency-based), so the shipped fix doesn't break Wildfire's math —
  it breaks the visible promise (quarantined residents strolling out mid-plague).
* **TheRogueDome story bit (Renegades) — the strongest case, and MECHANICAL:** a dome
  declares independence, every resident becomes a Renegade, and the
  `SetBuildingRogueState` effect calls `Dome:SetUIInteractionState(false)`
  (`ClassDef-Effects.generated.lua:2790`), which FORCE-toggles `accept_colonists` off
  (`Dome.lua:1495-1498`); the event text announces "The Dome has become Quarantined."
  The seal on a hostile splinter state is meant to be total (the dome can't even be
  interacted with) — but with the home-side commute gates removed by this fix, the
  rogue dome's renegade residents can still be offered work/services/training in the
  player's own domes through connecting passages.
* **Arrival routing:** `is_welcoming_community` (`_GameUtils.lua:342-344`) requires
  `accept_colonists` — quarantined domes are excluded from
  `GetDomesReachableByColonists`, i.e. new arrivals are never routed into one.
* Narrative-only mentions: MedSt_Disease's "Seal the gates and establish quarantine"
  reply (scripted morale/standing costs) and DataDealer's computer-virus flavor.
**RESOLVED — user decision 2026-07-27: CLOSED `wontfix`, superseded by D03.** The user's
grounds: the underlying community ask ("shut down migration to a dome but keep
services/commuting") is one of the most-requested behaviors in the game, but it must not
come at quarantine's expense — the events above depend on the lockdown. Resolution:
**delete `Fix_HomeDomeMigrationGate.lua`** (git history restores it; deletion + metadata
line + probe rework + re-verified A/B are STAGED for the next game-free leg — F10
precedent; expected numbers shift by one probe) and **build the ask properly as D03**
(`Opt_ResidencyControl`, a NEW per-dome "closed to new residents" policy that leaves
`accept_colonists`/quarantine untouched — see the D03 entry). MOD_DESCRIPTION's F61
bullet is removed in the same change.
**Deletion DONE (2026-07-27 build leg):** `Fix_HomeDomeMigrationGate.lua` + its metadata
line removed; the TestKit `HomeDomeMigrationGate` probe DELETED too (it tested the
removed behavior — not an F10-style canary). A/B re-verified: baseline 1/56/14/0, fixed
57/0/14/0, 64/68 active.

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
*Half shipped, opt-in: `Code/Opt_ClassicRockets.lua`* (id `ClassicRockets`, enabled in
Options → Mod Options since D05, or via the pre-load `SMRFixPack_Optional` override; the
`Opt_` filename prefix marks it as not-a-fix). **Fuel half PLAY-VERIFIED 2026-07-27
late:** the user toggled the module on LIVE via Mod Options mid-session (the D05
activation path) and confirmed auto-refuel working on a parked rocket — informal
observation, no formal PT item; behavior matched spec with nothing beyond refuel,
as designed. It ships the **fuel half**: a chained wrapper on
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

**UI research fact (found live 2026-07-27 late, user asked where auto-export
went):** the Automated Mode toggle is HIDDEN — not disabled — on any rocket
without an assigned destination: `UIToggleAutoMode_Update` gates
`SetVisible` on `arrival_loc AND IsRocketLanded()` (+ IsAutoModeEditable =
player-controlled + destination flight policy allows automation,
`UniversalRocket.lua:2259-2264, :1826-1833`). So the vanilla replacement
automation is invisible in exactly the parked-no-destination state where the
original's auto behaviors used to act — strengthening this module's rationale,
and a constraint for the export-half build: the module must act (like the fuel
half) WITHOUT the vanilla automation UI being reachable in that state.
**Design decision (user, 2026-07-26): the export half MATCHES THE ORIGINAL GAME —
no invented thresholds or knobs.** The module exists because the original had this
behavior and Relaunched redesigned it away; fidelity to the original is the whole
point and also the only evidence-driven spec. The original's behavior is readable in
the dead legacy loader (`RocketBase:CreateExportRequests`, RocketBase.lua:1729-1736):
every landed rocket carries a standing `PreciousMetals` demand request up to its
`max_export_storage`, flags 0 (any drone serves it), gated by a per-rocket
`allow_export` toggle; fuel is the sibling standing request (the shipped half).
Build-leg research before writing it: (1) how the per-rocket `allow_export` toggle
maps onto UniversalRocket's UI/state; (2) whether the modern Earth-arrival path
sells metals that are aboard without a payload request (the legacy sell path is
also compatibility-nilled); (3) what the ORIGINAL did about RC-transport
auto-offload into rockets — that answer decides whether F56's behavior rides
along (original had it → ClassicRockets gets it) or stays closed (it did not).
Needs its own probe + a playtest item when built; stays behind the same
`ClassicRockets` flag as the fuel half.
*The export half now also owns F56.* F56 (auto RC Transports never offload rockets) closed
`wontfix` 2026-07-26 on the same "deliberately maintained design" grounds, with the note
that if it is ever revisited it belongs in THIS module rather than in one of its own — same
request ("rockets should load and unload themselves like they used to"), same machinery,
and shipping the two separately would let a player enable an emptying behaviour without the
refilling one. So whenever the export half gets its design decision, decide auto-offload in
the same pass and behind the same `ClassicRockets` flag.

### D02 — Dismissing a "Building Not Working" warning only silences it ~4 game hours — BY DESIGN, feels like a bug  `[built 2026-07-27: Code/Opt_AcknowledgedWarnings.lua (opt-in, off by default); probe PASS in the opt-in leg; PT-48]`
Spun out of F32's close (2026-07-26, user decision) — read that entry for the full trace.
Not a defect: the shipped suppression machinery works exactly as designed
(`Notifications.lua:41-43`, `:86-88`, `:141-146`). The design just has no answer for a
PERMANENTLY broken building: the window is **120,000 GAME-ms = 4 game hours**
(`SuppressTime = 120000`; **CORRECTED by PT-38, 2026-07-27** — the entry previously
claimed 2 REAL minutes, backwards: `GetTime()` resolves `self.GameTime and GameTime()
or RealTime()` and `GameTime` DEFAULTS TRUE, which the preset does not override,
`NotificationPreset.lua:65-66, :126-128`. Verified live with game/real timestamp
wrappers: three dismissal→return pairs measured 148,805 / 161,755 / 132,056 game-ms —
each exactly 120,000 + time-to-the-next re-add attempt, with every in-window attempt
observed BLOCKED; real-time durations varied with game speed, ~2 min at 1×, ~30 s at
the user's accelerated speed). It silences the whole notification id (new breakages
included) rather than the acknowledged building, and there is no per-building
acknowledgment at all. An unfixable building — F30's lake-entombed case is the
archetype — re-nags every 4 game hours for the rest of the game, which at ultra speed
is **every few real seconds** — the annoyance premise is STRONGER than originally
recorded, not weaker. **Players read this as "dismiss is broken"; it is not — it is a design gap.** The
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
**Gate:** ~~PT-38 first~~ **DONE 2026-07-27 — cadence verified (and corrected to 4
game hours, above); per-id suppression confirmed live (independent fuel-warning ids
untouched by dismissal; every same-id re-add attempt inside the window observed
BLOCKED). Build + probe unblocked for the next build leg.**
**BUILT (2026-07-27 build leg): `Code/Opt_AcknowledgedWarnings.lua`.** Implemented as
three chained wrappers on the notification helper globals (none is file-local in
Notifications.lua, so replacements are seen — F22 precedent): `SuppressNotification`
(the dismissal hook — its only caller runs under `notification.dismissed`) stamps every
listed building with `SMRFixPack_ack_notworking = true` and SKIPS the shipped whole-id
window for this one id; `AddObjectToNotification` drops re-adds of stamped buildings;
`RemoveObjectFromNotification` clears the stamp (recovery/destruction re-arms warnings).
Only `NotWorkingBuildings` is touched. Savegame footprint: the per-building flag,
absent-tolerant both ways (policy §3). Probe `AcknowledgedWarnings` (TestKit
`60_Probes_Opt.lua`) drives all three wrappers with stand-ins — PASS in the opt-in leg,
SKIP-with-reason otherwise. Playtest: PT-48.

### D03 — No way to block dome move-ins short of a full quarantine  `[tested 2026-07-28: Code/Opt_ResidencyControl.lua (opt-in, off by default); probe PASS in the opt-in leg; PT-49 PASS in full (archived) — arrivals/tourists proven against an adversarial pad-beside-the-closed-dome setup, quarantine independence, MicroG row (kept on asteroid habitats by user decision), uninstall shape live + reload]`
Filed 2026-07-27 (user decision, out of PT-14/F61's close — read that entry first). The
community's long-standing ask: **stop new residents from moving into a dome while its
residents keep commuting and using services normally.** The shipped game offers only the
blunt instruments: full quarantine (`accept_colonists` off — blocks enter AND leave;
load-bearing for Wildfire/RogueDome, see F61), the trait filter (indirect, trait-based,
and its tooltip says setting it REMOVES a quarantine), or turning off residences.
**Design — strictly additive, quarantine untouched:**
* **Flag:** `SMRFixPack_closed_to_new_residents` set directly on the Dome object —
  persists with the save, absent-tolerant (nil = vanilla = accepts), uninstall-clean
  (policy §3). Default off; every dome behaves 100% vanilla until the player flips it.
* **UI:** post-wrap `sectionDome:Init` (`Lua/XDef/sectionDome.generated.lua:16` — the
  infopanel section is a plain Lua class building its policy rows imperatively via
  `InfopanelActiveSection:new`, one call per row in a VList) to append a new
  "Accepts new residents / Closed to new residents" row cloned from the shipped
  accept-colonists row pattern: icon + title + rollover (`Untranslated`), left-click
  toggle, Ctrl+click broadcast, `RebuildInfopanel`. Same wrap for
  `sectionMicroGHabitat:Init` (asteroid habitats); the Command Center dome-overview row
  grid is optional follow-up. Icons: reuse shipped section icons or ship two PNGs.
* **Gates:** post-wrapper on `Community:CanAcceptNewColonists` (`Community.lua:62`) —
  shipped result AND NOT flag — closes voluntary resettlement (its caller
  `Colonist:FindEmigrationDome` filters candidates on it, `Colonist.lua:2658`).
* **Build-time survey (the real design work):** enumerate the remaining move-in paths
  and decide per-path — rocket/elevator ARRIVALS choosing a first home
  (`GetDomesReachableByColonists` filters on the file-local `is_welcoming_community`,
  `_GameUtils.lua:342-344` — file-local, so arrivals need their own patch point if the
  flag should block them; recommend it should), MANUAL player relocation (deliberately
  stays allowed — the player's own override), tourists/hotel-seeking (leave alone),
  births (in-dome, leave alone), homeless within their own dome (not a move-in, leave
  alone). Verify no other `CanAcceptNewColonists` callers exist.
* Own probe (drive `FindEmigrationDome`/`CanAcceptNewColonists` with the flag both
  ways), own playtest item, opt-in via `SMRFixPack_Optional.ResidencyControl`
  (FIX_POLICY §4, ClassicRockets precedent), MOD_DESCRIPTION section when it ships
  (explicitly: quarantine still exists and still means quarantine).
**BUILT (2026-07-27 build leg): `Code/Opt_ResidencyControl.lua`.** The move-in-path
survey resolved as speced, with one refinement found at build time:
* Voluntary resettlement: post-wrapper on `Community:CanAcceptNewColonists`
  (`Community.lua:61-63`) — verified its ONLY Src caller is `Colonist:FindEmigrationDome`'s
  candidate filter (`Colonist.lua:2658`).
* Arrivals: the patch point is the global **`ChooseDome`** (`_GameUtils.lua:426-446`),
  NOT `GetDomesReachableByColonists` — the reachability list also feeds
  construction-placement range display and worker checks, which must NOT see closed
  domes (existing residents still commute). `ChooseDome` is the single
  choose-a-new-home funnel (rocket arrivals ×3, lander/transporter ×3, factory-born
  androids, stranded colonists re-homing). The wrapper filters closed domes from the
  candidate list only; the `safety_dome` argument passes through untouched (a stranded
  colonist's last resort survives), and `traits.Tourist` skips the filter entirely
  (hotels untouched).
* UI: post-wraps on `sectionDome:Init` + `sectionMicroGHabitat:Init` append the policy
  row via the shipped `InfopanelActiveSection` pattern; the toggle rides the shipped
  `Community:TogglePolicy`/`SetPolicyState` machinery (`Community.lua:77-100`) — FX,
  Ctrl+click broadcast and the rogue-dome UI-interaction lock all come free. Closed
  state styled yellow/limit so it cannot be mistaken for the red quarantine row.
* Flag `SMRFixPack_closed_to_new_residents` on the Dome object, absent-tolerant (§3).
Probe `ResidencyControl` (TestKit `60_Probes_Opt.lua`) asserts both gates plus the
tourist and safety-fallback exemptions — PASS in the opt-in leg. Playtest: PT-49 (the
UI row needs eyes-on — it is the pack's first added infopanel row).
**PT-49 first sitting (2026-07-27 late): core behavior PASSing** — closed
high-comfort dome took zero move-ins while commute/services ran normally
(evidence in the checklist section). **One cosmetic finding, repaired same
day:** the appended row rendered at the section's END (below the stat bars)
because sectionDome:Init builds toggles first, then the Colonists/stat
InfopanelSections, and a post-wrap append lands last. Repair: after creation
the row is repositioned to just before the first plain InfopanelSection child
(= directly after the shipped accept-colonists toggle) — children are the
parent's array part and VList renders array order (XWindow.lua:719-739 is the
engine's own array-reorder precedent); falls back to end-of-section if the
shape ever differs. Position eyes-on re-check after the next relaunch.

### D04 — Multiple Artificial Suns — absorbs F39  `[tested 2026-07-27 (PT-50 PASS in full, archive): Code/Opt_MultipleSuns.lua (opt-in, off by default); night signature matched the banked baseline both sectors, sunless panels 0 at night, reload clean, limit off/on live via the D05 Mod Options toggle]`
Filed 2026-07-27 (user decision, out of PT-26/F39's premise finding — read F39 first).
The shipped game hard-limits the Artificial Sun to one per colony (`build_once` wonder,
enforced colony-wide incl. construction sites, `BuildMenu.lua:711-719`), which makes
F39's second-sun binding fix unreachable dead code in the default pack — but players DO
run "allow multiple wonders" mods, and any such mod walks straight into the vanilla
`labels.ArtificialSun[1]` panel-binding bug. This module makes the pack's story honest:
**it lifts the limit AND ships the fix that makes the lifted limit work**, saving users
a third-party mod.
**Design — strictly additive, off by default (`SMRFixPack_Optional.MultipleSuns`,
FIX_POLICY §4, ClassicRockets precedent):**
* **Limit lift:** set `BuildingTemplates.ArtificialSun.build_once = false` (preset
  patch — template tables exist only after DataLoaded; the build menu re-reads
  `CanBuildOnlyOnce()` live so no UI refresh is needed; verified live 2026-07-27 via a
  console toggle of the same flag). `wonder` stays true (sight category, placement-close
  behavior untouched).
* **Binding fix:** the whole of `Fix_SecondArtificialSun.lua` moves in unchanged — the
  `SolarPanelBase:GameInit` post-wrapper (walk the whole label, hand the first in-range
  sun to shipped `SetArtificialSun`) plus the LoadGame sweep for panels already dark
  beside a second sun in modded saves. With the module OFF, vanilla is untouched in both
  directions (the bug is unreachable without the lift).
* Probe: rework the existing SecondArtificialSun probe to the ClassicRockets pattern —
  SKIP with an opt-in reason unless the flag is set, assert both halves when it is.
  Default-pack expected A/B numbers change (one fewer armed probe) — land in the same
  game-free leg as the F61 deletion so the renumbering happens once.
* Own playtest item when built (reworked PT-26): enable the module, build sun #2 far
  from #1 through the NORMAL build menu, ignite, build panels AFTER it, night check for
  the −21%-atmospheric/night-production signature vs the banked single-sun baseline
  (archived PT-26); confirm the build menu allows repeat placement and the once-only
  refusal returns with the module off.
* MOD_DESCRIPTION gets a module section when it ships (feature framing, not bug-fix
  framing; note it exists because limit-lifting mods hit the vanilla binding bug).
**BUILT (2026-07-27 build leg): `Code/Opt_MultipleSuns.lua`.** Limit lift runs from
`OnMsg.DataLoaded`/`OnMsg.DataChanged` (templates exist only after DataLoaded; the
re-fired `DataChanged(false)` re-asserts idempotently — F75 lesson; the handlers gate on
the registry status, which covers both the opt-in flag and the `SMRFixPack_Disabled`
veto). The F39 wrapper + LoadGame sweep moved in unchanged; `Fix_SecondArtificialSun.lua`
deleted. Probe `MultipleSuns` (TestKit `60_Probes_Opt.lua`) asserts
`BuildingTemplates.ArtificialSun.build_once == false` on the live template AND the
binding behavior — PASS in the opt-in leg ("Artificial Sun build-once limit lifted"
logged at DataLoaded). Playtest: PT-50 (night-production signature vs the PT-26 banked
single-sun baseline).

### D05 — Optional modules had no player-usable enable surface  `[tested 2026-07-27 late (PT-51 PASS in full, archive): items.lua Mod Options toggles + metadata default_options + 00_Core bridge; probe OptionsMenu PASS in all armed legs; live both ways, restart-persistent, log clean]`
Found live 2026-07-27 late, when the user sat down to run Group 8: the briefed
enable route — "type `SMRFixPack_Optional = {...}` in the MAIN MENU console" —
was **falsified twice over**. (1) The user has no main-menu console (the TestKit
auto-open fires in-colony, and the shipped console binding is not active at the
menu). (2) It could never have worked anyway: every Opt_ module's gate runs
inside `SMRFixPack.Register`'s immediate `apply`, at **mod code load during game
startup — before the main menu exists** — which is exactly why the A/B harness
needed the temporary `97_OptInLeg.lua` flag FILE. The instruction was never
tested against the load order. Release context makes this a blocker, not a
nicety: the pack targets Steam Workshop AND Paradox Mods, and **Paradox Mods
delivers to PS/Xbox, which have no Lua console at all.**
**Resolution — the engine's native Mod Options (all verified in Src):**
* `ModItemOptionToggle` items in a new `items.lua` (loaded by `ModDef:LoadItems`,
  `Mod.lua:590-604`) put the pack on **Options → Mod Options** (page def
  `options.lua:775-776`, shown whenever an installed mod `HasOptions()`;
  gamepad-capable — the console-platform path). Four toggles, `name` ==
  registry id: ClassicRockets, AcknowledgedWarnings, ResidencyControl,
  MultipleSuns.
* `default_options` table added to metadata.lua (the field `HasOptions()` reads,
  `Mod.lua:473-475` — it is what makes the page list the pack; normally written
  by the Mod Editor at save time, `Mod.lua:970`).
* Values persist per-account in `AccountStorage.ModOptions[mod.id]` and are
  loaded BEFORE mod code so gates can read them (`Mod.lua:2128-2131`; on cold
  start `WaitLoadAccountStorage()` precedes `LoadDlcs()` → mods,
  `autorun.lua:435-436`). Exposed env-side as `CurrentModOptions`
  (`Mod.lua:1621`), values rawset directly for plain indexing (`:679-683`).
* **00_Core bridge (D05):** `SMRFixPack.OptionEnabled(id)` = pre-load
  `SMRFixPack_Optional[id]` OR the saved toggle — the gate line in all four
  Opt_ files. `SMRFixPack.IsActive(id)` — consulted by every optional module's
  wrappers PER CALL, so toggles are live in BOTH directions (off = installed
  hooks pass through; no unhooking needed). `OnMsg.ApplyModOptions` (fired on
  option load and every user Apply, `Mod.lua:746/:2170`) reconciles: turning ON
  re-arms installed hooks or runs the apply now (+ `def.on_activate`); turning
  OFF flips the registry status (+ `def.on_deactivate`). D04 uses the callbacks
  to flip `BuildingTemplates.ArtificialSun.build_once` on the spot (restore
  guarded by a we-lifted-it flag so a third-party limit mod is never stomped).
* Register defs gain optional extras: `optional`, `on_activate`,
  `on_deactivate`; defs now retained in `SMRFixPack.defs` for reconciliation.
**Also repaired in the same leg (found by the leg, pre-existing):** D04's
`lift_build_limit` wrote a scary "ArtificialSun not found — build limit NOT
lifted" detail when an early `DataChanged`/first `DataLoaded` fired before the
template existed, and the detail never cleared — `ListFixes` showed it forever
on an ACTIVE module. Now the miss is only recorded after DataLoaded has fired
AND the transient detail is cleared once the template is found. (Engine fact
observed: DataLoaded fires more than once during startup; the template can miss
the first pass and appear on a later one.)
**Verification (2026-07-27 late, logs Mars.exe-20260727-…):** parse sweep 82
files / 0 failures; baseline 21.20.32 = 1 PASS / **57 FAIL** / 14 SKIP / 0
ERROR (the new `OptionsMenu` probe FAILs discriminatingly — registry absent);
fixed 21.21.51 = **58/0/14/0**, 64/68 active, OptionsMenu PASS, all four gates
log the new "enable it in Options → Mod Options" reason; opt-in (re-run after
the detail repair) 21.34.28 = **61/0/11/0**, 67/68 active, all three module
probes + OptionsMenu PASS. **72 probes total now.**
**Playtest: PT-51** — the Mod Options page itself needs eyes-on (row rendering,
tooltips, live toggle both ways, persistence across restart) — first thing in
the Group 8 sitting, since it is now also the Group 8 enable mechanism.
**PT-51 first sitting (2026-07-27 late) — LATENT PACK BUG found at step 2 and
repaired same day:** `SMRFixPack.ListFixes()` crashed ("attempt to concatenate
a nil value (field 'detail')", 00_Core.lua:140). Root cause predates D05: the
2026-07-25 F75/F18 status-relabel repairs clear their entry detail with
`entry.detail = nil` on every DataLoaded
(Fix_IndependenceTerraforming.lua:88, Fix_LastTransmissionStorage.lua:165),
and ListFixes concatenated `f.detail` after a `~= ""` check that nil passes —
so the console helper has been crash-primed in EVERY session since; tonight's
PT-51 step 2 was simply the first in-colony ListFixes call since then (the
autorun harness and the probes use their own counters/FixStatus, which is why
no leg ever caught it). Repair: both writers now clear with `""`, and
ListFixes tolerates nil defensively (other mods can write these entries).
Parse-checked; takes effect on the next game launch. **A/B pair re-verify
queued for the next game-free window** (no probe reads ListFixes, so the
numbers cannot shift — the pair is policy hygiene).

### F64 — Demolishing a station vaporizes its trains ("trains go to void") (P1, high)  `[fixed: Code/Fix_TrainsToVoid.lua]`
*(Header restored 2026-07-26 — it was lost in an earlier doc edit; the entry body below
was always here, sandwiched between D02 and F65.)*
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

### F66 — Station↔tunnel connector hex ping-pong (P2, med-high)  `[tested: Code/Fix_TrackConnectorPingPong.lua — PT-41 PASS 2026-07-26 (shared hex stable, survivor reclaimed the link after demolition, plain-tile control clean)]`
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

**Recovery-gap repair LANDED (2026-07-26; user decision 2026-07-25: "rebuild instead
of half baking it").** The QA audit found that when the guard declines, the guarded
building owns no element on the contested hex, and after the WINNING building is
demolished nothing reschedules the survivor's rebuild — every engine trigger notifies
only the dying element's own station (`TrackElement.lua:193-199`; `Track.lua:179-183`;
`Msg("TrackDemolished")` only fires from player track demolition → global rebuild,
`TrainTransport.lua:156-159`) — so the survivor stayed connectorless until any track
demolish or a re-place. Implemented in the same fix file: post-wrap of
`TrackConnectedObjBase:Done` (declaring class, TrainTransport.lua:14 — an object
destructor, not a command method, so the post half runs). The wrap records the dying
building's connector hexes BEFORE the shipped body tears them down, runs the shipped
body, then `SMRFixPack.TrackConnectorReclaim` queries each contested hex with the
sandbox-safe `map:MapForEach(pos, "hex", 3, "TrackConnectedObjBase", …)` (connector
spots reach ≤ ~2 hexes, radius 3 covers every possible loser; NOT a global rebuild)
and schedules `CreateGameTimeThread` + in-thread revalidation — the engine's own
deferred idiom copied from `TrackElement.lua:194-198` — for every other live,
non-destructing candidate; the F66-guarded `CreateConnectorElements` makes re-runs
idempotent for buildings that already own their elements, and `done_map` teardown
early-returns exactly like the shipped body. Probe `TrackConnectorPingPong`
(`40_Probes_Wave4.lua`) extended: drives the exposed reclaim helper with a synthetic
map — exactly one rebuild scheduled (live neighbour), dying self and destructing
neighbours excluded, hexes deduplicated. Playtest: PT-41.

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
**FINDING (2026-07-28, PT-17 capacity-edge leg, live colony): the fix OVER-DRAWS
below the player's GET-WHEN-ABOVE threshold under active mining.** Observed via the
leaf-class TAP2 console tap: Rare Metals threshold 144, ground stock 184 (~40 units
exportable) — but the request ratcheted 40000 → 52000 → 72000 → 98000 → 100000 (the
hold cap) across the hourly recomputes as extractors replenished stock mid-load, and
the lander ultimately drained the asteroid to **84, sixty units below the keep-
threshold**. No churn, no dump, both resources delivered to Mars, the next leg
correctly excluded the now-below-threshold resource — the anti-churn ratchet itself
held (`req` never below `have` throughout). **Root cause: the fix implements the
anti-churn floor TWICE.** (1) `Fix_LanderCargoRatchet.lua:145-151` adds the aboard
amount into `amount_on_target_loc` before the threshold compare — so any bookkeeping
lag between ground totals and hold totals (drone-carried units, reservations, fresh
mining) inflates `to_transfer` every recompute and the request ratchets monotonically
to the hold cap; (2) `:169-174` is the clean post-hoc floor (`requested` never below
aboard) which alone prevents the unload flip. **Repair sketch (mechanical, queued —
game-free + re-verified A/B):** delete the (1) aboard-into-ground addition and let
the (2) explicit floor carry the whole F68 fix; expected behavior after: request =
max(aboard, current ground surplus) — no churn AND no over-draw (equilibrium lands
ground exactly at the threshold). PT-17 stays un-archived until the repair re-runs
the capacity-edge leg.

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

### F71 — Auto-export allocates capacity alphabetically (P2, med)  `[tested 2026-07-28: Code/Fix_LanderCargoRatchet.lua — folded into the F68 replacement of the same function. PT-32 live proof: two-export leg allocated PreciousMetals its full exportable stock FIRST and gave Concrete (alphabetically earlier) only the remainder, both delivered to Mars; when the valuable later grew to saturate the hold, Concrete was correctly squeezed to zero, never the valuable. Nothing-dropped check: both resources present in full in the initial allocation when the hold had room. Four-class order additionally probe-verified in isolation]`
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

### F74 — RC Transports can be ordered onto trade / refugee rockets (P2, high)  `[tested: Code/Fix_RocketInteractGuard.lua — PT-39 PASS 2026-07-27: cursor + route both refused a landed trade rocket; controls clean (F76 caveat on the entry)]`
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

### F76 — RC Transport depot resource picker renders far from the cursor and cannot be clicked (P1, high) `[todo — found live 2026-07-27 during PT-39 setup; wave-6 build candidate]`
**Player-visible symptom (how it was reported):** "I tried to take the transport to load
a resource — I get the icon but just a noise when I go to the depot to load machine
parts. It won't actually load them." Loading from GROUND piles works (that path issues
`PickupResource` directly); loading from any **StorageDepot** silently does nothing.
**What actually happens (live forensic session, all steps in the console log):**
clicking a depot in Load mode is SUPPOSED to open the `ResourceItems` picker at the
mouse position (`RCTransport:InteractWithObject` storage branch →
`OpenResourceSelector`, `RCTransport.lua:419-428`; pick a resource in it → the real
`TransferResources` command). On the tester's machine (ultrawide, ~3751px-wide window)
the picker:
* **opens and stays alive** — instrumented `OpenResourceSelector` fired; a delayed
  probe 2s later read `dialog ALIVE box=(886,13)-(1054,442) items=1` — but **renders as
  one giant detached hex button near the top of the screen**, nowhere near the cursor
  (screenshot on file: huge "Machine Parts" hex the tester described as "this giant
  machine parts logo isn't normal");
* **cannot be clicked where it is drawn** — clicks on the visual pass through to the
  WORLD (console trail: `SelectionChange → LifeSupportGridElement / StorageMachineParts
  / RCTransport` as the clicks selected the pipe/depot/transport behind it), and each
  selection change closes the picker via its own `OnMsg.SelectionChange` handler
  (`ResourceItems.lua:198-200`) — `dialog DEAD` on the follow-up probe.
**Suspected mechanism (to pin in the build leg):** coordinate-space mismatch.
`ResourceItems:Init` anchors at `terminal:GetMousePos()` (terminal pixels,
`ResourceItems.lua:11`) and `UpdateLayout` (:45-71) consumes that anchor in the scaled
UI/desktop space; the dialog's logical box lands at anchor/scale — the observed box ×
the tester's ~1.88 display scale maps back to the true mouse position. Visual placement
and hit-testing diverge from the cursor (and evidently from each other) whenever
terminal resolution ≠ UI space; at 1080p/scale≈1 the error is small enough to pass QA,
which is why this shipped. Data still to capture: `terminal.desktop.box`,
`terminal.desktop.scale`, game resolution + UI scale setting.
**Ruled out:** the fix pack (every wrapper tap was pass-through on this path — F74's
guard only matches the four trade/refugee rocket classes); data layer (12 selector items
built, gate inputs healthy: `hasM=true`, supply request live, `stored=164000`); pause
queue (reproduced unpaused); Lua errors (zero in the session log).
**Not just this dialog?** `OpenResourceSelector` also serves the multi-resource UNLOAD
path and transport-ROUTE resource choice (`RCTransport.lua:456/:468`) — all cursor
workflows through `ResourceItems` are equally affected. The `ItemMenuBase` siblings that
anchor the same way should be surveyed in the build leg.
**Workaround (verified live):** issue the picker's command directly —
`rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`.
**Fix sketch (wave-6):** convert the anchor into the layout's coordinate space in
`ResourceItems:Init` (or override `GetItemsRolloverAnchor`/layout to use the desktop-
space mouse position), leaving gamepad mode (`desktop.box:Center()`) untouched. Own
probe + playtest item on a scaled display.
**Release-messaging note (user, 2026-07-27): this WILL generate false reports against
the pack** — "transports can't load from depots" reads as a mod bug to anyone testing
with the pack installed. MOD_DESCRIPTION needs a "known vanilla issue" explainer (D02
precedent) whether or not the fix ships in the same release.
**Later same day — three escalations from the continued live session:**
* **Unload surface CONFIRMED by play** (was predicted above): with multiple resource
  types aboard, the unload click "just makes the sound and nothing unloads" — the
  multi-resource unload path opens the same broken picker; single-type unloads bypass
  it and work.
* **Environment pinned:** fullscreen 3840×2160, UI Scale slider ~80-85% (screenshot on
  file). No windowed resize involved.
* **The broken picker can HARD-LOCK the UI (Alt-F4 required) — severity carries a
  data-loss vector.** During a live-prototype attempt (an `Init` post-wrapper
  re-anchoring `align_pos`), the session locked with every mouse event erroring:
  `Error calling Lua function "MouseEvent" from C: CommonLua/X/XWindow.lua:1154:
  attempt to index a boolean value (local 'desktop')` — `XWindow:SetVisibleInstant`
  running on a DESTROYED window (`self.desktop == false`) still referenced by the
  modal/animation chain (the picker's open/close interpolations +
  `SetModal`/`RestoreModalWindow` teardown racing). Whether the wrapper contributed or
  only witnessed it, the teardown fragility is real.
* **Prototype learning that redirects the fix:** at `Init` time the dialog's own
  `self.scale` still reads `(1000,1000)` — the actual UI scale is applied by the
  parent AFTER Init — so converting the anchor in `Init` is a NO-OP. The repair must
  convert in/around `UpdateLayout` (use-time), or anchor from a value already in the
  layout's space. Anchor captured correctly: `(1731,665)` = true mouse on the
  4K desktop.
**Process decision: NO further live UI-internals prototyping on play sessions** — the
F76 repair is an attended, game-free build-leg task (MarsDebug or throwaway retail
session) where a lockup costs nothing.
**Surface extension (2026-07-27 late, found live in the Group 8 sitting): the RC
Terraformer (in-game "RC Dozer") hits the same broken picker.** Clicking a
waste-rock storage heap in Load mode opened the picker as a giant detached
"Waste Rock" hex near the top of the screen (screenshot on file — the exact
PT-39 rendering signature, one item). Path: the dozer's Load-on-WasteRock
interaction is VANILLA and intended (`RCTerraformer.storable_resources =
{"WasteRock"}`, `RCTerraformer.lua:33`; its CanInteractWithObject allows only
WasteRock piles, `:224-237`) and routes through `RCConstructorBase`'s static
calls into `RCTransport.InteractWithObject` (`RCTransport.lua:353` family) —
the same storage branch → `OpenResourceSelector` that every affected surface
shares. So the fix target is unchanged (`ResourceItems`/UpdateLayout — one
repair covers this too), but the affected-surfaces list is wider than
transports: **any vehicle whose click-load reaches a storage-depot-class
object**, dozer included. Loose rubble piles remain safe (direct
PickupResource, no picker). Command workaround works the same way on the dozer
(it has TransferResources — its own DumpCargo uses it):
`rc:SetCommand("TransferResources", <heap>, "load", "WasteRock", <amount*1000>, true)`.
Pack ruled out for this sighting explicitly: the F74 wrappers in that chain are
refuse-only (both early-return false for event rockets, everything else defers
to the shipped body) — verified in-session before filing.

### F77 — Extender working-flap tears down and rebuilds the entire uplink hub; fleet-wide Idle churn (P2, med-high)  `[fixed: Code/Fix_ExtenderFlapChurn.lua — chained wrapper on UpdateUplinkRequesters, rebuild deferred 2s + coalesced per root hub (chains resolved); built 2026-07-28 with the D06 core, PT pending. Accepted trade-off: registration stale up to ~2s during the window — the shipped flow already defers reconnects (SetWorkRadius uses DelayedCall(300)). Debounce thread is a mod game-time thread = not persisted (F06 precedent), so a save inside the window is clean]`
`DroneHubExtenderBase:OnSetWorking` (`DroneHubExtender.lua:171-178`) calls
`UpdateUplinkRequesters` (:109-112) on EVERY working transition, in BOTH directions
(off AND back on), and that helper is not incremental: it runs
`uplink:DisconnectTaskRequesters()` + `ConnectTaskRequesters()` — a full teardown and
rebuild of the WHOLE far hub's requester set, not just the extender's own slice
(`DroneControl.lua:441-450`, `:327-360`). The teardown walks every connected
requester: each `RemoveCommandCenter` → `DroneControl:RemoveBuilding` (`:731-757`) →
`OnRemoveBuilding` (`:720-729`), which scans the hub's whole drone list per building
and kicks every drone whose goto target is that building to `Idle` (aborting the trip
and, via the command destructors, releasing any held request claim). Consequences per
extender power-loss/restore, malfunction, repair completion, or manual toggle:
(a) every in-flight trip of the entire far fleet to ANY connected building is aborted
— F50's churn signature, but triggered by the extender and fired on BOTH edges of the
flap (two full cycles per blip); (b) O(B×D) drone-kick scans plus O(B×P) linear
`remove_entry` queue removals plus a full `MapGet` radius rescan on reconnect —
per flap, per extender; (c) requests vanish from the hub's queues for the window, so
drones that poll during it stamp the empty-queue throttle. Extenders are
maintenance-consuming, powered buildings (`maintenance_resource_type = "Electronics"`,
`electricity_consumption = 2000`, `DroneHubExtender.generated.lua:17,38`), so dust
storms, battery brownouts and ordinary malfunction cycles flap them in exactly the
big-colony scenarios where the far hub serves the most ground. This alone reproduces
both halves of the live 2026-07-27 report (drones dropping to Idle + degraded
throughput) whenever an extender flaps — no additional defect required — though the
cross-hub locality gap traced on the sweep bullet is a separate, co-existing mechanism.
**Fix sketch (FIX_POLICY §1 ranking; NOT built — user decision):**
(1) chained wrapper on `DroneHubExtenderBase:OnSetWorking` that debounces the
`UpdateUplinkRequesters` half — coalesce transitions within a few seconds into one
delayed reconnect thread per uplink (risk: a short stale-coverage window where
extender-only buildings stay registered while the extender is down — benign next to
the churn; savegame-neutral, no persisted state);
(2) diff-based reconnect (disconnect only requesters no longer covered by
`FindTaskRequesters`) — better endgame but full-replacement scale surgery on shared
`DroneControl` machinery (F50/F68/F70/F71 territory), not the first move.
Risk note: the wrap point is narrow (extender class only), but the effect surface is
every `DroneControl` descendant serviced by the uplink hub — must pass the F50
rocket-churn and F55 unreachable scenarios in playtest before shipping.

### D06 — Drone assignment has no cross-hub locality; far fleets claim near work (design, high)  `[built 2026-07-28: Code/Opt_DroneOverhaul.lua core v1 (opt-in, off by default, Mod Options toggle "Drone dispatch overhaul (experimental)"); PT pending — attended, multi-iteration]`
The design defect behind the 2026-07-27 live report (four idle drones parked beside a
malfunctioning building while a far hub serviced everything slowly): assignment is
pull-only and own-hub-only, requests sit in every covering hub's queues, claims are
first-poller-wins held through the whole approach, repair requests are max_units=1,
and no handoff/steal/distance-tiebreak exists anywhere. Full trace on the "Not yet
swept" DroneControl bullet; the option analysis (A-H, feasibility/risk/reward) is
`docs/DRONE_OVERHAUL_OPTIONS.md`. **Core v1 ships three parts** (all
per-call-gated on `IsActive`, hooks installed at classdef time; NO persisted state —
saves made with it load identically without it):
1. **Closest-fleet-first claim gate** — chained wrapper on `TaskRequestHub:FindTask`
   (`_TaskRequest.lua:72-83`; sole caller is the drone auto-Idle path, so player
   orders are structurally untouched). A repair/clean WORK request offered to a hub
   that is not the building's closest covering Drone Hub — extender-aware, reach-
   guarded — is withheld for that poll while the closest hub is working with idle
   drones. Per-request strike counter (4 polls, 30s decay) makes starvation
   impossible: if the near fleet doesn't claim, the far fleet serves.
2. **Repair moonlighting** — chained POST-wrapper on `Drone:Idle` (the body falls
   through exactly when no work was found, so the hook fires only for genuinely
   workless drones): scan other working hubs that are SATURATED (zero idle drones)
   for unclaimed repair/clean work within 30 hexes of the drone and inside its own
   movement restriction; take it exactly like the shipped own-hub maintenance branch
   (`Drone.lua:602-605`). Covers the ground the claim gate can't: buildings covered
   ONLY by the far hub.
3. **Telemetry** — `SMRFixPack.DroneReport()` (always available, module on or off):
   per-hub working/drones/idle/broken, lap-time load class, per-priority queue
   depths, work-request and unclaimed counts, extender chains, plus the module's
   vetoed/expired/moonlighted counters.
Out of scope v1 (deliberate): PickUp/Deliver hauling (H-v2/B in the options doc),
construction work (swarming desirable), rover/rocket fleets, the registration layer
(vanilla redundancy intact — toggling off is instant and complete). Tunables at the
top of the file (strike cap/TTL, moonlight radius, cache TTLs) are the playtest
iteration knobs. Shipped alongside: **F77**'s `Fix_ExtenderFlapChurn` (default-on
repair) so extender power flickers stop Idle-kicking whole fleets and muddying the
overhaul's observability.

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
  **(DroneControl half SWEPT — static source leg 2026-07-27 late; full verdict + trace
  + instrumentation plan appended at the end of this bullet. `ShuttleHub.lua` remains
  unswept.)**
  Prime suspect for live reports: "drones ignore rocket cargo at high priority",
  "RC transports don't auto-offload rockets", "late-game drones stop maintaining
  inside open domes / cluster stuck outside" (review-sourced).
  **FIRST-HAND EVIDENCE (user, 2026-07-27 late, screenshot on file — raise this
  to the top of the sweep):** with a large-range hub plus many drones and
  OVERLAPPING hub ranges, (a) **task assignment ignores locality across hubs** —
  a cluster of idle drones parked nearest a malfunctioning building (wrench
  icon up) and a Polymer storage did nothing while a hub near the SECOND dome,
  much farther away, serviced everything; work backed up and buildings sat
  disabled for short stretches; (b) **performance tanks** as hub range/drone
  count grows, worse with multiple hubs in range of each other — the user saw
  the same pattern in the ORIGINAL game, so the mechanism likely survived into
  Relaunched. Investigation angles when swept: how tasks are queued per-hub vs
  globally (does a request bind to the hub that noticed it rather than the
  nearest?), whether overlapping hubs share/steal work, whether idle drones
  ever scan for work themselves, and what in the per-tick request matching is
  O(range × drones). Distinct from F55 (unreachable-forever cache) — these
  drones CAN reach the work; they are never assigned it.
  **Live console reads (same sitting):** the FOUR closest drones to the
  serviced-too-slowly area each read `command = "Idle"` — genuinely idle in
  the assignment layer, not wedged mid-command and not F55-cached; and a
  PolymerPlant was caught at `performance = 0` with `auto_performance = 50`
  (the transient disable the user reported), its maintenance/repair requests
  showing `target:0` at read time (the far fleet does service things —
  slowly). Ownership answered: an idle drone's `command_center` read
  **`DroneHub`, handle 2608** — a regular hub (near the idle cluster), so the
  drones are correctly parented, and the user verified **no RC commander was
  nearby broadcasting a zone** (rover niche ruled out). Remaining crux for the
  sweep, only observable AT a starvation moment: which hub's queue holds a
  request while hub-2608's drones idle — i.e. whether requests bind to the
  noticing/registering hub's fleet with no cross-hub handoff.
  **User hypothesis (prior-game experience, same sitting): the REPEATER is the
  trigger** — in the original game the misassignment/performance pattern
  became prevalent once Drone Hub Extenders entered the colony, and this
  colony DOES run them (a DroneHubExtender maintenance request appeared in the
  same dump batch). Plausible mechanism to check in the sweep: an extender
  stretches a distant hub's effective service area over ground a nearer hub
  already covers, and whatever request→hub matching runs is
  extender-transparent (distance/priority measured hub-to-target, or
  first-registered-wins) so the extended far hub captures work the near fleet
  should take. Sweep pointers: extender machinery is in `DroneControl.lua`
  itself + `Drone.lua` (both already in this bullet) and
  `BuildingTemplate\DroneHubExtender.generated.lua` /
  `XDef\customDroneHubExtender.generated.lua`. Repro recipe for the sweep:
  hub A + hub B far apart, extender bridging B's range into A's area, break
  something in A's yard, watch which fleet answers.

  **INVESTIGATION VERDICT (game-free source leg, 2026-07-27 late).** The assignment
  architecture is **working-as-coded but has NO cross-hub locality anywhere**; the
  extender-transparency hypothesis is **CONFIRMED**; one adjacent provable defect was
  filed (**F77**, extender working-flap churn); the exact starvation trigger needs one
  attended console sitting to discriminate two proven-possible mechanisms (reads below).
  Trace, against the six kickoff questions:

  1. **Pull model, own-hub-only, engine-matched.** An idle drone polls ONLY its own
     hub: `Drone:Idle` (`Drone.lua:564-641`) calls `command_center:FindTask(self)`
     (`:621`) — the sole `FindTask` call site in the entire Src tree (grep-verified).
     `TaskRequestHub:FindTask` (`_TaskRequest.lua:72-83`) hands the hub's OWN
     priority/supply/demand queues to the C-side `Request_FindTask`; the match
     order/distance policy inside it is engine-internal and NOT visible in Src (no doc
     either — recorded as an engine-side unknown). The only distance knob visible from
     Lua is per-request `supply_dist_modifier` (`_TaskRequest.lua:96`) — distance is
     weighed when pairing supplies WITHIN a hub, but nothing weighs locality across
     fleets. Queues are per-hub Lua tables of shared C request objects, appended in
     insertion order (`CommonLua\TaskRequest.lua:242-256` queue layout;
     `DroneControl.lua:685-718` `AddBuilding`). Poll cadence ≈3s per idle drone
     (Sleeps inside Idle), gated on `hub.working` (`Drone.lua:612`) and on a 1s
     per-HUB empty-queue throttle `no_requests_time` (`:620,:631` — stamped only by a
     drone with zero unreachable-cache entries; reset only by `InterruptDrones`,
     `_TaskRequest.lua:301`).
  2. **Overlap = the same C request object sits in EVERY covering hub's queues; claim
     is first-poller-wins and held through travel; no handoff, no stealing, no
     rebalance exists.** A building registers with every hub whose radius covers it
     (`TaskRequester:AddCommandCenter`, `CommonLua\TaskRequest.lua:147-160`; both
     connect directions), and every new request posts into every registered center
     (`AddRequest`, `:123-137`). The claim happens when the winning drone's command
     starts, not at match time: `Drone:Work` calls `RequestAssignUnit` BEFORE the
     approach (`Drone.lua:898-924` — claim at `:901`, fulfil only on arrival `:920`),
     so the slot is locked for the entire trip. Maintenance repair requests are
     created with **max_units = 1** (`RequiresMaintenance.lua:82` —
     `AddWorkRequest("repair", 0, 0, 1)`): ONE claiming drone, however far, locks out
     every other fleet. The only cross-hub drone code in the game is refab gathering
     (`DroneHub.lua:53-74`) and orphan adoption — nothing load- or distance-based.
  3. **Extender transparency CONFIRMED in both connect directions.** Building-side:
     `FindDroneNodes` (`_TaskRequest.lua:251-257`) returns any `DroneNode` covering
     the building; an extender's `GetCommandCenter()` recurses to its uplink HUB
     (`DroneHubExtender.lua:156-160`), so the building registers the far hub ITSELF.
     Hub-side: `FindTaskRequesters` (`DroneControl.lua:315-325`) recurses through
     working linked extenders and connects finds to the hub. Extender-mediated
     coverage is structurally identical to native coverage in every queue — the
     extender leaves no trace on the request. What extenders do NOT extend: drone
     movement. `Drone:SetCommandCenter` restricts each drone to
     `const.DroneRestrictRadius` = 100 hexes-worth of world distance AROUND THE HUB
     POSITION (`Drone.lua:227-230`, `_GameConst.lua:71`). Post-SignalBoosters (hub
     +15 → 50, extender +15 → 50; `TechPreset.lua:3455-3482`) one max-stretched
     extender reaches exactly that boundary; a chain of two EXCEEDS it — buildings
     can be REGISTERED with a hub whose drones can never legally reach them
     (suspected F55-feeder: approach fails → unreachable-forever cache; `RestrictArea`
     enforcement is engine-side, unverifiable statically — flagged for the live
     sitting).
  4. **Idle drones never look for work themselves.** The Idle body is the only work
     search a drone performs, own hub only (plus special cases: own-hub repair,
     broken-drone repair, emergency power — `Drone.lua:593-618`). If its hub's queues
     don't hold the request, or the request is claim-locked, a drone parked ON TOP of
     the work idles forever, by construction.
  5. **Hot loops (the performance half).** (i) Every idle drone × every ≈3s × a
     C-side scan over its hub's full queue set; queue size grows with range² ×
     building density AND with overlap multiplicity — every shared building's
     requests appear in every covering hub's queues, so k-fold overlap ≈ k× the
     colony-wide scan work. The 1s empty-queue throttle cannot engage while any
     polling drone holds an unreachable-cache entry (`Drone.lua:630`) — i.e. exactly
     in cluttered late-game colonies. (ii) Reconnect storms: `SetWorkRadius`
     (`DroneControl.lua:760-777`), every extender working-flap (→ **F77**), and
     `OnMsg.DepositsSpawned` reconnecting EVERY hub in the city at once
     (`DroneHub.lua:188-199`). Each reconnect = per-building drone-kick scans
     (O(B×D), `OnRemoveBuilding` `:720-729`) + linear `remove_entry` over 5-priority
     queues + a full `MapGet` radius rescan. That is the reported range × drones ×
     requests degradation, and overlap worsens every term.
  6. **Reconciliation.** The observed picture (near fleet Idle, far fleet slowly
     servicing, transient `performance = 0` disables, requests reading `target:0`)
     is reproduced by the traced machinery under either of two mechanisms — the
     banked console evidence cannot yet discriminate:
     **(a) registration gap** — the starving buildings sit OUTSIDE hub 2608's
     35-50-hex circle while INSIDE the far hub's extender-stretched coverage. Then
     2608's queues never hold the requests and its drones idle legitimately (drones
     parked near the buildings prove nothing about the hub's circle — `GoHome` parks
     them relative to the HUB, `Drone.lua:636-638,643-674`). Everything runs
     as-coded; the failure is pure design — the extender grants the FAR fleet ground
     the NEAR fleet doesn't own.
     **(b) claim lockout** — the requests ARE in both hubs' queues; far drones claim
     first (max_units=1 + claim-held-through-travel) and the near fleet re-loses the
     race on every work chunk. The live `target:0` read is consistent with (b) at the
     read instant, but also with (a)+far-claim.
     **F77's flap churn additionally reproduces both observed halves on its own**
     whenever an extender flaps — and this colony runs extenders with a pending
     extender maintenance request in the same dump batch.

  **Live instrumentation plan (next attended sitting; F12/PT-38 timestamped-wrapper
  pattern; every name verified against Src and console-sandbox-safe — `HexAxialDistance`,
  `HandleToObject`, `ConsolePrint`, `MainCity`, `GameTime`, `guim` all non-blacklisted;
  `Drone.lua` holds no file-local alias of `RequestAssignUnit`, so a console global
  wrapper IS seen by drone code):**
  * **R1 — registration + geometry** (select the starving building first). Answers
    (a) instantly — is 2608 listed, and is `d ≤ radius`?
    `*r local b=SelectedObj local s={} for _,cc in ipairs(b.command_centers or empty_table) do s[#s+1]=cc.class..":"..cc.handle.." d="..HexAxialDistance(cc,b).."/"..cc.work_radius.." w="..tostring(cc.working) end ConsolePrint("[SMR reg] "..b.class..":"..b.handle.." -> "..table.concat(s," | "))`
  * **R2 — who holds the repair claim** (building still selected):
    `*r local b=SelectedObj local r=b.maintenance_work_request ConsolePrint("[SMR req] target="..r:GetTargetAmount().." actual="..r:GetActualAmount().." can="..tostring(r:CanAssignUnit())) for _,d in ipairs(b:GetMap().City.labels.Drone) do if d.w_request==r or d.d_request==r or d.s_request==r then ConsolePrint("[SMR holder] "..d.handle.." cmd="..tostring(d.command).." hub="..(IsValid(d.command_center) and d.command_center.handle or 0).." dist="..(d:GetDist2D(b)/guim).."m") end end`
  * **R3 — is the request in hub 2608's queues** (building selected; work requests
    are rfPostInQueue via the Mars `AddWorkRequest`, `_TaskRequest.lua:118-121`, so
    the priority_queue is the right place to look):
    `*r local h=HandleToObject[2608] local b=SelectedObj local n=0 for p=-1,3 do for i,r in ipairs(h.priority_queue[p]) do if r:GetSource()==b then n=n+1 ConsolePrint("[SMR q] prio="..p.." idx="..i) end end end ConsolePrint("[SMR q] hits="..n)`
  * **R4 — hub state**:
    `*r local h=HandleToObject[2608] ConsolePrint("[SMR hub] w="..tostring(h.working).." idle="..h:GetIdleDronesCount().."/"..#h.drones.." lap="..h:CalcLapTime().." nrt="..(GameTime()-h.no_requests_time))`
  * **R5 — extender chain map** (uplink chains + working states):
    `*r for _,e in ipairs(MainCity.labels.DroneHubExtender or empty_table) do local c={e.class..":"..e.handle} local cur=e.uplink while cur do c[#c+1]=cur.class..":"..cur.handle cur=cur:HasMember("uplink") and cur.uplink or nil end ConsolePrint("[SMR ext] "..table.concat(c," -> ").." w="..tostring(e.working)) end`
  * **R6 — live claim tap** (the timestamped wrapper; repair-only filter to bound
    spam; arm once per session, cleared by reload):
    `*r local orig=RequestAssignUnit RequestAssignUnit=function(req,unit,amount) local ok=orig(req,unit,amount) if ok and IsValid(unit) and unit.class=="Drone" and tostring(req:GetResource())=="repair" then ConsolePrint("[SMR "..GameTime().."] claim "..unit.handle.." hub="..(IsValid(unit.command_center) and unit.command_center.handle or 0).." src="..tostring(req:GetSource() and req:GetSource().handle)) end return ok end ConsolePrint("[SMR] claim tap armed")`
  * **R7 — controlled repro** (the banked recipe): hub A + hub B far apart, extender
    bridging B into A's yard. Arm R6; `Platform.cheats = true` then
    `SelectedObj:CheatMalfunction()` on a building in A's yard (verified command
    table); watch which hub's drone claims, then re-run R1-R4 at the claim moment.
    A-covered building claimed by a B drone while A idles = (b) proven; building
    missing from A's `command_centers` = (a) proven.

  **Fix directions (NOT built this leg — user decision; FIX_POLICY §1 ranking; the
  locality items are assignment-POLICY changes — D-item territory — while F77 is a
  plain repair):**
  * **If (a) — registration gap:** the least-dishonest mod-side lever is a cross-hub
    idle-pull: PRE-wrap `Drone:Idle` (must be pre — command methods kill post-wrappers,
    F73/STATUS fact) so that after the own-hub `FindTask` misses, the drone polls
    OTHER working hubs whose `work_radius` covers the DRONE's position. Requests are
    hub-agnostic C objects, so cross-hub execution is mechanically clean, and
    `RestrictArea` keeps the drone local anyway. Risks: lap-time/heavy-load
    accounting attributes foreign work to the wrong hub; battery/GoHome interplay;
    claim races (already atomic via `AssignUnit`).
  * **If (b) — claim lockout:** a near-idle-yield — chained pre-claim veto in
    `Drone:Work`/`Drone:PickUp`: skip claiming (the shipped miss path: Sleep +
    return) when the request's source building has a CLOSER working center with idle
    drones and the building inside that center's radius; yield-once-per-request memo
    (TTL) so a request whose near fleet can't actually serve is never starved. The
    match ORDER itself cannot be touched — `Request_FindTask` is C; only its Lua
    callers are patchable — so a veto+retry is the least-invasive lever that exists.
  * **F77 (independent of (a)/(b)):** debounce wrapper — see the F77 entry.
  * **Shared-machinery risk, stated per the kickoff:** this is the deepest shared
    machinery in the game — every `DroneControl` descendant (hubs, RCRovers, the
    rocket cargo path of F50/F68/F70/F71) runs through these queues. Any claim-path
    change must re-pass the F50 rocket-churn and F55 unreachable scenarios in
    playtest before shipping.
  * **Follow-up (2026-07-28, user-commissioned): full overhaul-toggle feasibility
    study in `docs/DRONE_OVERHAUL_OPTIONS.md`** — options A-G (repair moonlighting,
    full moonlighting, migration balancer, claim veto, true handoff, Lua-matcher
    rewrite [rejected], telemetry/F77/throttle supporting acts) ranked by
    feasibility/risk/reward with verified patch points and a recommended build
    order. Supersedes the two fix-direction sketches above as the design reference;
    still a USER DECISION.
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
