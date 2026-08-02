# Bug Tracker — Surviving Mars: Relaunched Community Fix Pack

Canonical record of every defect found in the game's shipped Lua source
(`<game>\ModTools\Src`), its evidence, and its fix status. **Update this file in
the same change that adds or edits a fix.** All line numbers refer to the
shipped source tree; the game executes `Packs\Lua.fpk`, **proven byte-identical
to Src for all gameplay Lua** (2,250/2,256 files, build 1.0.7.396349 — the
2026-07-29 extraction diff; the 5 divergences are engine/tooling only). Each
fix still self-checks its target at apply time — that guards *future* game
updates — and the extraction diff is re-run after every game update
(see `WORKFLOW.md`).

Statuses: `todo` → `fixed` (code written) → `tested` (verified in-game) | `wontfix` | `blocked`.

## Index

| ID  | Title                                                    | Sev | Conf | Status |
|-----|----------------------------------------------------------|-----|------|--------|
| F01 | Cave-ins ignore "No Disasters" rule                      | P1  | high | tested 2026-07-29 — PT-11 · **⭐ WITNESS RE-DERIVED 2026-08-01 (owner, logged-in Paradox browse): first-party report dated May 8 2026, Game Version 1.0.7, with steps to reproduce — the audit's "NOT re-derivable" is RETRACTED** (entry) |
| F02 | Meteors strike ~every 6h instead of 35–115h              | P1  | high | **tested 2026-08-01** — rewritten 2026-08-01 (F86 Tier-1, layer 3: keyed wrapper + vanilla body, one-shot latched heal) and **verified live by Tier-1 legs 1+2+5**: cadence gaps of 75 h, 83 h and 72 h all inside the designed 65–90 h roll; storm-warning timing proven UNCHANGED three independent ways (the `CurrentThread()` key's whole point); F88's per-load re-roll gone; and on uninstall the `Meteors` thread survives `valid=true` on vanilla's body (entry) |
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
| F14 | Domes Overview red low-stat highlight dead               | P2  | high | tested — PT-09 PASS 2026-07-28 (entry) |
| F15 | Mystery 11 wisp RP rewards double/silent                 | P2  | high | fixed* |
| F16 | Mirror Sphere site usable after completion               | P2  | med  | fixed  |
| F17 | Dust Sickness damage not randomized                      | P2  | med+ | fixed  |
| F18 | Independence terraforming tech gives 10% not 20%         | P2  | med  | fixed — index row corrected 2026-08-01 (was `fixed*`; the open half closed 2026-07-26, entry) |
| F19 | Graphs "Consumed" caption omits maintenance              | P2  | med+ | tested — PT-43 PASS 2026-07-28 (entry) |
| F20 | Morale tooltip shows unapplied +Comfort bonus            | P2  | high | tested — PT-43 PASS 2026-07-28 (entry) |
| F21 | Train travel-time penalty includes station waiting       | P2  | med  | fixed — was `tested`; F86 Tier-2 rewrite retired the body PT-43 exercised (entry) |
| F22 | `GetGridGlobalStorage` breaks Last Transmission gates    | P2  | med  | fixed  |
| F23 | Founder-gains-trait notification never fires             | P3  | high | tested |
| F24 | Dome pipe visuals corrupt on load (`MoveInside` typo)    | P3  | med  | wontfix — unreachable in vanilla, fix deleted 2026-07-30 (entry) |
| F25 | Tech description names wrong building (pre-1.0.6 saves)  | P3  | high | fixed  |
| F26 | Bombardment missiles fly parallel (cosmetic)             | P3  | med  | fixed  |
| F27 | Storage charge/discharge rate modifiers ignored (latent) | P3  | med  | fixed  |
| F28 | `Research:ReplaceTech` mishandles the field counter      | P3  | high | wontfix 2026-07-30 — mod-facing only, barred by FIX_POLICY §4a; fix + probe DELETED (entry) |
| F29 | SA/sequence latents: label filter, workshift wait, Diggers swap | P3 | high | fixed*|
| F30 | Lake placement entombs RC builder + drones               | P1  | high | fixed  |
| F31 | Anomaly cave-in hardcodes UndergroundMap (cross-map)     | P2  | med  | fixed  |
| F32 | Dismissed warnings re-add instantly (not suppressable)   | P2  | med  | wontfix|
| F33 | Drone crash on small landscaping sites (nil-index)       | P2  | high | fixed  |
| F34 | Landscape nil-guard bundle (latent crash paths)          | P3  | med  | fixed* |
| F35 | Large Wind Turbine buff lost in old saves (fixup bug)    | P2  | high | fixed  |
| F36 | Universities overtrain geologists (unmanned extractors)  | P2  | high | tested |
| F37 | Ghost farm oxygen modifier survives salvage/demolish     | P1  | high | fixed  |
| F38 | Destroyed tunnels rejoin pathfinding after save/load     | P2  | high | tested |
| F39 | Second Artificial Sun ignored by solar panels            | P2  | high | folded into D04 2026-07-27 — PT-50 PASS (entry) |
| F40 | Dust Sickness infects Biorobots (androids)               | P2  | high | fixed  |
| F41 | Gene Forging tech has no effect                          | P2  | high | tested 2026-07-29 — PT-29 |
| F42 | Buildings placeable on active dust devils                | P3  | high | wontfix — user decision 2026-07-25 (index row corrected 2026-08-01; it had gone stale as `blocked`) |
| F43 | Layout construction bypasses tech locks                  | P3  | high | fixed  |
| F44 | One-hex track salvage can delete the entire track        | P1  | high | tested |
| F45 | Damaged tracks can't be salvaged at all (sort crash)     | P1  | high | tested |
| F46 | Trains dump cargo at stations with resource disabled     | P2  | high | tested — PT-23 PASS 2026-07-28 (entry) |
| F47 | Track salvage refunds ~1 hex for whole track / 0 partial | P3  | high | tested |
| F48 | Station-connector savegame fixup no-op (paren misplaced) | P3  | high | blocked|
| F49 | Train minors bundle (palette, split kills trains, etc.)  | P3  | med  | fixed* — (d) tested 2026-07-30 PT-46; (c) wontfix + guard REMOVED (designed behaviour); (a) R4 NON-FIX, guard STRIPPED 2026-08-01 (owner; audit §2.4) — A/B code-gate leg RAN CLEAR 2026-08-01 (entry) |
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
| F61 | Home dome's migration toggle blocks outbound shopping    | P1  | med+ | wontfix 2026-07-27 — superseded by D03, PT-14 (entry) |
| F62 | Services reach 1 passage hop only, never trains          | P2  | high | wontfix|
| F63 | Universities invisible to emigration (no students)       | P2  | high | wontfix|
| D01 | Rockets don't auto-refuel/auto-export rare metals        | dsgn| high | opt-in fix |
| D02 | Dismissed "not working" warnings re-nag every 4 game h   | dsgn| med  | tested 2026-07-30 — PT-48 PASS in full (entry) |
| D03 | No way to block dome move-ins short of full quarantine   | dsgn| med  | tested — PT-49 PASS 2026-07-28 (entry) |
| D04 | Artificial Sun is build-once; second-sun support unused  | dsgn| low  | tested — PT-50 PASS 2026-07-27 (entry) |
| D05 | Opt-in modules had no player-usable enable surface       | dsgn| high | tested — PT-51 PASS 2026-07-27 (entry) |
| D06 | Drone assignment has no cross-hub locality (far fleets claim near work) | dsgn| high | built (v1) 2026-07-28, A/B NULL — ⭐ **REBUILD DECIDED 2026-07-31, top of the list**; 4 research gates owed, **playtest FROZEN** (entry) |
| D07 | Cohort housing: seniors/children never consolidate without filter micromanagement | dsgn| med | built 2026-07-28 — PT-53 3-of-5 PASS 2026-07-29, A/E owed (entry) |
| D09 | No player control over drone speed/carry (breakthrough lottery) | dsgn| med | tested 2026-07-30 — PT-56 PASS in full (entry) |
| D10 | Workshops: capacity can't scale late-game; unemployment's real cost invisible | dsgn| med | speced 2026-07-30, user-approved — **gate OPEN (PT-56 PASSED 2026-07-30), BUILDABLE NOW** (entry) |
| D11 | Shuttles fly ONE passenger per trip even for identical dome pairs | dsgn| low | candidate — feasibility on file, NOT green-lit: ASK the user (entry) |
| D12 | Homeless strand in specialist domes; emigration ties never move them | dsgn| med | SPECED 2026-07-30, user-approved, build owed (entry) |
| D13 | Save-exit deliverables: uninstall procedure + standalone save-rescue artifact | dsgn| high | directed 2026-07-31 (owner), prelaunch — **HARD LAUNCH DEPENDENCY (owner, 2026-08-01): the pack does not ship until this ships alongside it**; ⛔ **spec GATED on Tier 1/2 landing AND verifying** (target list = their output, never today's leak set — the gate is sequencing, not priority); also owns the **complete per-site disposition table** required before release (FIX_POLICY §3a) and **must DERIVE the exposed set itself rather than inherit any recorded count** (the docs carry an open lower bound, "at least 13", from a grep known blind to slot/global/preset assignments, and the builds have since changed the set) — **its derivation is authoritative and it updates every doc stating a count** (list on the entry); second-artifact costs + open player-story design question on the entry (entry) |
| F64 | Station demolition permanently leaks train prefabs       | P1  | high | fixed · **◑ 2026-08-01 (owner, logged-in Paradox browse): FAMILY witnessed live on Relaunched** (Jan 30 2026 — station removed, train bookkeeping wrong afterwards and stayed wrong), **but the verbatim "trains go to void" report was NOT located** — stop citing that phrase as a quote (entry) |
| F65 | Station-at-tunnel never bridges the power grid           | P2  | med  | tested — PT-40 PASS 2026-07-28 (entry) |
| F66 | Station↔tunnel connector hex ping-pong (never connects)  | P2  | med+ | tested |
| F67 | Auto-lander launches empty, ping-pongs Mars↔asteroid     | P1  | high | tested — PT-16 PASS 2026-07-28 (entry) |
| F68 | Hourly auto-request ratchet unloads lander's own cargo   | P1  | high | tested — PT-17 complete 2026-07-28 (entry) |
| F69 | Manual landing dumps the return fuel (stranded landers)  | P1  | high | tested — PT-16 PASS 2026-07-28 (entry) |
| F70 | Edit Payload silently refills from policy template       | P2  | med+ | tested — PT-31 PASS 2026-07-28 (entry) |
| F71 | Auto-export fills capacity alphabetically (waste rock)   | P2  | med  | tested — PT-32 PASS 2026-07-28 (entry) |
| F72 | "No available landers" while a lander sits on the pad    | P2  | med  | tested — PT-33 PASS 2026-07-28 (entry) |
| F73 | Asteroid colonists idle outdoors; no shelter reflex      | P1  | med+ | tested — PT-19 PASS 2026-07-28 (entry) |
| F74 | RC Transports can be ordered onto trade/refugee rockets  | P2  | high | tested · **⭐ RIVAL-ROCKET REPORT FOUND 2026-08-01 (owner, logged-in Paradox browse): same reporter twice — OG Sep 5 2022 (overflow trigger) and Relaunched May 2 2026 on 1.07 (halt-mid-load trigger), both ending in a PERMANENTLY bricked rocket.** Primary evidence replaces the paraphrase-grade dev note; our guard covers both triggers (entry) |
| F75 | Last Transmission storage opinions inert; Oxygen reads Power | P2 | high | fixed |
| F76 | Depot resource picker renders off-cursor, unclickable    | P1  | high | todo — found 2026-07-27, wave-6 candidate (entry) |
| F77 | Extender working-flap tears down + rebuilds whole uplink hub; fleet Idle churn | P2 | med+ | fixed 2026-07-28 — PT pending (entry) |
| F78 | MeteorsDisaster storm wedges forever in its unbounded drain loop | P1 | high | **tested 2026-08-01** — fixed 2026-07-29; StormWedgeHeal REORDERED 2026-08-01 (F86 Tier-1 orphan gate, §6.2a-D) and **BOTH §6.2a-D completion branches ran live on the reordered body** (Tier-1 leg 1 forced storm → release branch; the natural storm → force-clean branch; storms keep scheduling after each heal). PT-54 triggers C+D absorbed (entry) |
| F79 | Colonists never use trains for services (service search is passage-only) | P3 | high | **`wontfix` 2026-07-31 (owner)** — feature-completion DECLINED: risk of new issues exceeds the benefit, especially on large multi-stop end-game maps (entry) |
| F80 | Trains stop at a platform and skip valid waiting passengers | P2 | med | investigating — observed 2026-07-28 · **SOURCE AUDIT RUN 2026-08-02 (prompt 6c): enumeration theory SURVIVES with an exact predicate — `traverse_dir = next_idx - start_idx` is never normalised to ±1 (`TrainTransport.lua:374`) off two `table.find` first-occurrence lookups (`:369,:372`) into a `route` array the file itself says can hold a station twice (`:389`, `EnumRouteTracks:273-282`); any stride ≠ ±1 hits a missing `link_edge` and HARD-RETURNS (`:417`), silently dropping the tail.** Explains **both** symptoms from one function (`Train.lua:882` = waits; `Station:GetReachableStations` `:222-231` = walks). ⛔ **Trigger NOT proven — CANNOT DETERMINE, stays `investigating`.** ⚠️ Corrects the old "direction from canonical orientation" suspicion (wrong — it is the magnitude, not the sign). Two fix-binding side finds: the function is **not re-entrant** (`:365,:386-390`) and `GetReachableStations` has no cross-track dedup. Checklist rider rewritten to discriminate waits-vs-walks + a one-way-hole test (entry) |
| F81 | Stranded disaster-prediction flag gates ALL weather; rains loop also deadlocks on it | P1 | PROVEN | **tested 2026-08-01** — fixed 2026-07-29; rains half REWRITTEN 2026-08-01 (F86 Tier-1, layer-2 wrapper + version-stamped migration + C34 rider) and **verified live by Tier-1 legs 3+4**: a NATURAL collision re-rolled and rain returned, 'normal' migrated + stamped 1.0.1, C34 stale-ACTIVE healed through vanilla FinishRainProcedure, and the stranded-flag sweep cleared both with and without a reload while never touching a live warning. PT-54 triggers A+B+E absorbed (entry) |
| F82 | Split power/life-support grid notification lingers ~a sol after the grid is rejoined | P3 | med | **✅ MECHANISM FOUND 2026-08-02 (prompt 6c trace) — and it is neither option the entry weighed.** The notification has **no removal path at all** (`SupplyGrid.lua:1626-1629` is the only reference to `PowerGridSplit`/`LifeSupportGridSplit` in the tree) and registers a **position**, not the grid — so a rejoin is not an input. It clears only by the preset's `Expiration = 120000` with `GameTime = false`, which `Notifications.lua:188-217` runs on a **REAL-TIME** thread → **2 real minutes regardless of game speed**. Sibling tell: `PowerLeak`/`LifeSupportLeak` under the same parents carry no `Expiration`. ⚠️ Symmetric half not in the original report: an **unrepaired** split also stops being reported after 2 real minutes. Nothing built — key-matching design question **routed to prompt 7**; checklist rider rewritten around the real-time prediction (entry) |
| F83 | Minimized story popups lose their callback across a load — First Asteroid silently withholds 3 promised prefabs | P2 | PROVEN | **tested 2026-07-31** — PT-59 PASSED IN FULL on the keyboard (reload leg 1/1/1 + grant line; healthy leg 1/1/1 with the flag still `false`; 10 loads / 2 grants across the sitting). Built as the load-time heal (`Fix_FirstAsteroidPrefabs`) |
| F84 | Universal Tunnel description is wrong twice: claims rovers cannot use it (they can), omits life-support bridging | P3 | PROVEN | todo — filed 2026-07-30; rover half DISPROVEN BY PLAY during PT-25; nothing built; text-patch design is a USER DECISION (localization tradeoff), bundled into the D10 build (chain prompt 9) (entry) |
| F85 | Breakthrough choice popups + Assembly "Colony Values" choice ride real-time waiters — a save in their open window voids the choice | P3 | latent | filed 2026-07-30 by the popup audit — tier **U**, shielded by the modal window at default bindings; settling observation queued (rebind quicksave); NO fix until U resolves (entry) |
| F86 | **OUR OWN DEFECT** — pack code blocked on a persisted game-time thread is serialised INTO the player's savegame and outlives the mod's removal | P1 | **DECIDED — sweep reported** | open — filed 2026-07-31 by PT-20 — two sites proven live (`Fix_MeteorFrequency` kills the colony's meteors permanently; `Opt_DroneOverhaul` floods the log, and it leaked with its own toggle OFF), **durable exposed list re-derived 2026-08-01 (five-shape enumeration, Phase 1): 13** (the sweep had corrected the membership both ways — `Fix_DroneUnreachableForever` in, `Fix_TrainCargoDumping` out — and the re-run confirms it) **plus one inert route-(c) preset-field site** (`Fix_LastTransmissionStorage`, adjudication §4.4 closed — no build). Reproduces identically whether the pack is disabled OR fully removed. **Blocked release when filed; the gate is now PER-SITE — see the restatement at the end of this row.** Layer ordering 3→2→1 in **FIX_POLICY §3a**; build AUTHORISED (Tiers 1+2, layer 1 barred/gated); **ADJUDICATED twice 2026-07-31 (yes-with-changes; capture = value-reachability; exposed set ≥13 incl. compliant CaveIns) + prior-art survey run** (mechanism is documented engine design; community norm is accept-silence-heal; our guarantee unprecedented but achievable). **Plan of record: `F86_EXECUTION_PLAN.md`** — Phase 0 measured 2026-08-01 (GT creation DEFERS; autosave hook FIRES); **Phase 1 done 2026-08-01** (final Tier-1 spec `SAVE_SAFETY_REDESIGN.md` §6.2a; enumeration re-derived; §4.4 closed; build prompt written); **✅ TIER 1 BUILT AND VERIFIED 2026-08-01 (chain prompts 4 + 4b, build prompt consumed) — all four units shipped and all five legs ran; F02/F78/F81/F88 flipped to `tested`; leg 5 read Site 1 REPAIRED (the `Meteors` thread now survives uninstall alive on vanilla's body)**. ⚠️ **Site 2 (`Opt_DroneOverhaul`) STILL LEAKS** — leg 5 re-measured it at 80 orphan errors, newly observed to self-clear after one load; it is Tier-2 work (chain prompt 5). ⚖️ **RELEASE GATE RESTATED 2026-08-01 (owner): PER-SITE, not blanket** — every exposed site needs a recorded disposition (repaired in-pack where a layer 3/2 route exists; handed to the D13 cleaner where one provably does not). A site without a disposition blocks release; a site with one does not, whichever way it went. ⛔ **But the cleaner is NOT a scoping escape hatch: BUILD EVERYTHING REACHABLE NOW** — a hand-off is only valid *after* the in-pack attempt failed, never as a prediction, because D13's target list is the OUTPUT of the build work and cannot be designed before it. **Launch waits for D13; D13 does not wait for launch** (FIX_POLICY §3a). **✅ TIER 2 BUILT 2026-08-01 (chain prompt 5) — all four modules moved onto synchronous seams and **Site 2 is repaired**: `DroneUnreachableForever` → the sync consumer `Drone:CleanUnreachables`; `TrainWaitTime` → the sync `TransportStatistics:AddSpentTime`; `ArrivalDeaths` (b) → a layer-2 pre-wrapper on `Colonist:Idle` and (a) → the sync `Colonist:OnArrival` (**the design pass §6.2 booked as owed is RUN and found a route**); `Opt_DroneOverhaul` → the sync `Drone:CleanUnreachables` at vanilla's own Idle tail. Per-site dispositions recorded on each entry and in STATUS. ⚠️ **NOT YET VERIFIED — the one Tier-2 leg is specced and UNRUN (`PLAYTEST_CHECKLIST.md` PT-58, predictions written before the run), so the D10/D12 unhold is NOT recorded; chain prompt 5b carries both.** **✅ TIER 2 VERIFIED 2026-08-01 (PT-58, owner at the keyboard) — F86 SITE 2 IS CLOSED.** Uninstall log `Mars.exe-20260801-21.54.16`, test-2 lineage, 73 idle drones in the article: **ZERO `Opt_DroneOverhaul` orphan errors where leg 5 read 80** (98 when first measured), zero `[LUA ERROR]` of any kind, zero mentions of any Tier-2 module. **Both proven leak sites are now repaired and verified.** The leg verified SAVE SAFETY only — F53/F55/F21 stay `fixed`, since P1-P3 are fixture results and no live functional reading was taken. Next: the §5.4-A conversions (prompt 8) |
| F87 | **OUR OWN DEFECT** — `Fix_DustSicknessBiorobots` throws at apply when the player enables the mod (`HasTrait:new` before class flattening), so F40 is silently unfixed for that whole session | P2 | **OBSERVED** | **fixed 2026-07-31** — repaired in the shared `DataPatch` scaffold, not the one file: nothing runs before `ClassesBuilt`, and the enable path gets its own triggers. The sweep it earned found **3 more sites** silently dead on that path (TechDescriptionBuilding, MultipleSuns, FirstAsteroidPrefabs) — all repaired via the new `SMRFixPack.OnDataReady`. FIX_POLICY rule + ENGINE_FACTS written. ✅ **VERIFIED ON THE ENABLE PATH ITSELF, 2026-07-31 19.09** — the new leg ran with the owner ticking the box at the main menu: `68/74` → **63/0/15/0**, probe-for-probe identical to the cold boot bar two RNG lines, and the `DustSicknessBiorobots` probe (which reads live preset data) PASSed on the path that used to throw. Cold-boot A/B also CLEAR. ⚠️ Residual: the toggles were OFF, so the five `Opt_` probes SKIPped — a coverage gap on that path, closed by a second all-modules-ON leg. (An earlier claim that this leg verifies audit **A2** is WITHDRAWN — PT-55 answered A2 in play on 2026-07-30) (entry) |
| F88 | **OUR OWN DEFECT** — `Fix_MeteorFrequency` restarts the meteor timer on EVERY load, so a player who loads more often than the rolled 35-115h interval never gets a meteor | P2 | SOURCE-VERIFIED | **fixed 2026-08-01, VERIFIED by the defect's own repro** — filed 2026-07-31; fix BUILT 2026-08-01 (Tier-1 rewrite: the per-load restart is gone, one-shot version-latched heal in its place); **Tier-1 leg 2 met the named bar exactly** — strike #1 at `t=216351730` → quicksave → **3 loads with ZERO pack lines** → strike #2 at `t=218608231 (+2256501 ms = 75 game hours)`, i.e. the meteor arrived on the PRE-LOAD deadline (entry) |
| F90 | Surface dust storms break **underground** cables and pipes — the break pass rolls its victim from a cross-map (elevator-merged) grid fragment with no map filter | P2 | SOURCE-VERIFIED | **open — filed 2026-08-01 by the prompt-6 C04 sweep** (C04 closed and promoted). Chain read end to end: `City:HourlyUpdate` `City.lua:148-149` (gated `HasDustStorm`, which is **MainMap-only**, `DustStorm.lua:41`) → `RandomBreakSupplyGrid` :178-181 → `SupplyGrid:RandomBreakElements` `SupplyGrid.lua:1017-1021` → `table.rand(self.connectors, …)` :677 with no map filter. Underground connectors arrive because `SupplyGridFragment` **is** a `MultiMapSupplyGrid` (:337-338) and the elevator merges the two sides (`Elevator.lua:402-440` → `MergeGrids` :1635-1650 → `AddElement` :547-548), with the merged fragment registered on both cities' lists (:463-477). **Sibling tell**: the production pass 16 lines above guards the shared-fragment case and says so in a comment (:999-1001); the break pass does not. Independent Relaunched witness + working third-party fix (GromGor 3730839706, re-read from the archived FPK). **NOTHING BUILT** — body-copy shape vs FIX_POLICY §3a is the design question; decision package is chain prompt 7's (entry) |
| F89 | `MeteorsDisaster`'s unbounded drain loop wedges the METEORS thread on ordinary single/multispawn strikes — the colony silently loses ALL regular meteors, forever in vanilla | P2 | MEASURED | open — observed live 2026-08-01 (Tier-1 leg sitting): F78's drain-loop class on the singles path, INVISIBLE to the storm watchdog (no `g_MeteorStorm`); **covered by the F02 watchdog** (detected at its 189h threshold, `ALIVE but stuck`, restarted, ~6-8 sol latency); no direct fix routable — mid-function loop, body copy barred by F86 (entry) |
| C01 | `BreakthroughOrder` reshuffled on every map load         | ?   | cand | investigate |
| C02 | Cave-ins reported on asteroids — no Src code path found  | ?   | cand | runtime-check |
| C03 | Research screen softlock; research progress can exceed 100% | ? | cand | investigate |
| C04 | Surface dust storms damage underground pipes (cross-map leak) | ? | **CLOSED — promoted** | **✅ SWEPT AND CONFIRMED 2026-08-01 (prompt 6): full call chain read in Src, cross-map fragment mechanism proven → filed as F90** |
| C05 | Colonists repeatedly visit already-satisfied interest buildings | ? | cand | investigate |
| C06 | Colonist assigned to multiple workplaces simultaneously  | ?   | cand | investigate |
| C07 | Manual workplace assignment immediately discarded        | ?   | cand | investigate |
| C08 | Rare-metal extractor smokes forever after refab          | ?   | cand | investigate |
| C09 | Deterministic freeze near 90% breathable atmosphere      | ?   | cand | investigate (HIGH) |
| C10 | Last War mystery freezes at 54%; permanently blocks ALL imports | ? | cand | investigate (HIGH) |
| C11 | Game stops saving entirely (auto + manual)               | ?   | cand | needs a player log/save (HIGH) |
| C12 | Support Struts ignore Easy Maintenance game rule         | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C13 | Three FollowUp storybits mis-categorized, never fire     | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C14 | Fhtagn! option 2 cowards ALL colonists, not religious    | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C15 | Dust Sickness: Deaths morale penalty never applied       | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C16 | Flying drones malfunctioning mid-air stuck "flying"      | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C17 | The Man From Mars follow-up rewards nothing              | ?   | cand | filed 2026-08-01 (bug-list audit) — VERIFIED vs Src |
| C18 | XenoExtraction tech skips now-native ex-DLC extractors   | ?   | **✅ CLOSED — `wontfix` (intent)** | swept 2026-08-02 (prompt 6b): label mechanism read (`Building.lua:413-424,:427-444` — a building carries only `class` + `object_class`, never a parent's); `AutomaticMetalsExtractor` carries `AutomaticMetalsExtractor`/`AutomaticMetalsExtractorBase` and is displayed as a **differently-named building**, so the tech's four-name description promises it nothing. **Positive control found: when this game means "every extractor" it enumerates all of them** (`CommanderProfilePreset.lua:336-385`, ten labels). No promise broken → declined under the §4 bar (entry) |
| C19 | `AreDomesConnectedWithPassage` has no distance term      | ?   | **✅ CLOSED — declined, no defect in Relaunched** | swept 2026-08-02 (prompt 6b): the predicate is membership-only as charged, but it has **exactly two consumers** and the distance term lives at the consumer — `Dome.lua:256-259` gates it on `const.ColonistMinDistToIgnorePassage` (1200m, `_GameConst.lua:134`, *with* the design comment), and `Colonist.lua:1567` adds an 8-dome hop cap. Both escape branches are correct (open-air = safe outside; no shuttles = no alternative). The residual unbounded walk is the **no-passage** case, which is F52's deliberately-open half, not this. ⚠️ **Taking ChoGGi's OG shape would have narrowed F53's reachability test** (entry) |
| C20 | Philosopher's Stone sector count stalls while paused     | ?   | cand | **MECHANISM LOCATED 2026-08-02 (prompt 6b), harm not sized** — the ONLY emitter of `Msg("SectorScanned")` is a **game-time thread that opens with `Sleep(10)`** (`Exploration.lua:88-104`, spawned `:276-280`), so nothing is counted while game time is stopped; probe scanning has no pause gate (`OverviewModeDialog.lua:468-482`). Source cannot say whether the increment is **deferred or lost** → one checklist observation written. **✅ OBSERVATION TAKEN 2026-08-02 (owner, live): DEFERRED, NOT LOST → CLOSED, `wontfix — no player-visible cost`.** Paused: no signal. Unpaused: the **"Sector scanned" voice-over fired**, and `QueueVoice` sits inside `AddHUDNotification` at `:103`, immediately before the `Msg` at `:104` — so the message provably fired on unpause. ⭐ Internal control in the same scan: the synchronous `NewAnomalies` card behaved differently from the `Sleep(10)`-deferred `SectorScanned`. ⚠️ 6b's "on-screen toast" wording was **corrected** — `SectorScanned` is a `HUDNotificationPreset` on `idOverview` with a voice line, **not a popup card** (entry) |
| C21 | St. Elmo sinkholes destructible by meteors (soft-lock)   | ?   | cand | **DESTRUCTION ROUTE VERIFIED 2026-08-02 (prompt 6b) — the soft-lock is LOCATED, not proven** → prompt 7. `Sinkhole` carries **neither** `indestructible` **nor** `disasters_strike_immunity` (`Sinkhole.generated.lua:1-24`) and is the **only mystery set-piece in the game without the flag** — Crystals, Monolith, MirrorSphere, CaveOfWonders, JumboCave, ArkPod, MartianAssembly all have it. A large meteor reaches `DestroyBuildingImmediate` → `DoneObject` (`Meteors.lua:817-825` → `Building.lua:1371-1393` → `Demolishable.lua:132-141`). Best soft-lock candidate is the **unguarded `_sinkhole:GetMap()`** at `Mystery 11.generated.lua:146`. ⭐ Anomalies are NOT at risk — checked and ruled out (entry) |
| C22 | Saint trait dome-morale blessing never worked (label mismatch) | ? | cand | VERIFIED vs Src 2026-08-01 (fredware source recovered + read) |
| C23 | Dust devils: 3 scheduler defects (chance-as-count, CurrentMap read, DustStormsDisabled gap) | ? | cand | VERIFIED vs Src 2026-08-01 |
| C24 | Precedence bug: ordinary rockets count as asteroid landers (empty selection screen) | ? | cand | VERIFIED vs Src 2026-08-01 — complementary to F72 |
| C25 | Jumbo Cave reinforcements stuck on unreachable waste rock| ?   | cand | mechanism verified; trigger needs in-game repro — **minimal check WRITTEN 2026-08-02 (prompt 6b)** as a checklist rider. ⭐ Patch question answered from source: **1.0.6 replaced the whole Jumbo Cave scenario** (`Anomaly.lua:26-33` remaps to `…_106` when `UndergroundRework106`) **and left this wedge byte-identical** (old `:103` = new `:104`). ⚠️ **That flag is SAVE-VINTAGE gated, not build** (`UndergroundDome.lua:16-19`) — a pre-1.0.6 save runs the OLD script on our pinned build (entry) |
| C26 | Malfunctioned buildings stuck in perpetual maintenance   | ?   | **✅ CLOSED — `wontfix`, not reachable on current-build saves** | **SOURCE: CANNOT DETERMINE 2026-08-02 (prompt 6c); CLOSED THE SAME DAY ON LIVE EVIDENCE.** **THREE independent** colonies (`save_game_id` checked, not assumed), **347+ sols of combined history**, both **founded on the pinned build so the vendor fixups never ran** — `10 / 0` at sol 288, `2 / 0` at sol 59 (~50 of them organic pre-playtest), and `4 / 0` on a third lineage — non-zero controls in every one. Original source finding follows: **CANNOT DETERMINE** — no producer found in current Src, but the engine ships **two savegame heals for exactly this state** (`RequiresMaintenance.lua:531-566` `FixMaintenanceRequestsSources`, `:568-574` `FixMissingMaintenance`), so Haemimont saw it. ⚠️ Both are **old-save-only** — `AppliedSavegameFixups` is pre-seeded with every fixup name at new-game (`CommonLua\SavegameFixup.lua:10-16`, applied `:34-41`), so a save started on our build never runs them. Two obvious guesses checked and **ruled out** (rubble-shroud stranding; zero-threshold silent no-op). ⭐ **FIRST LIVE READING 2026-08-02 — CLEAN**: `10 buildings in maintenance or malfunction, 0 structurally broken` on a **sol-288** colony (log `Mars.exe-20260802-01.31.10:225`), the non-zero `10` acting as the control that the walk reached real candidates. **Points at CLOSE; held open for one confirming dump on a different colony.** ⚠️ A second clean dump (98 sols, `3 / 0`) was taken the same sitting and **does NOT count** — same `save_game_id`, i.e. an earlier point in the *same* playthrough. Vintage now CLOSED for that lineage by two agreeing mechanisms (`OrigLuaRev` = `LuaRevision` = 396349, `UndergroundRework106 = true`) (entry) |
| C27 | Signal Boosters never extend Drone Hub Extender radius   | ?   | **✅ CLOSED — no defect in Relaunched** | swept 2026-08-02 (prompt 6c). **6b's label lead RULED OUT**: `DroneHubExtender` is the template class name, so the label is carried and `Effect_ModifyLabel` lands (`Data\TechPreset.lua:3466-3471`). The extender's `work_radius` really is raised to 50, and the **commit step exists — it is just routed through the hub**: the tech's `Effect_Code` (`:3474-3481`) forces `SetUIWorkRadius` → `SetWorkRadius` → `DelayedCall(300, ReconnectTaskRequesters)` (`DroneControl.lua:759-777`), and `FindTaskRequesters` **recurses into `linked_extenders` reading each extender's live `work_radius`** (`:315-325`). Positive control: `CommandCenterMaxRadius = 50` = default 35 + `SignalBoostersBuff` 15 exactly (`_GameConst.lua:62-72`) (entry) |
| C28 | Transport Optimization tech never applied to RC Transport| ?   | **✅ CLOSED — no defect in Relaunched** | swept 2026-08-02 (prompt 6c). **6b's label lead RULED OUT again**: `RCTransport:AddToCityLabels` files every transport under `RCTransportAndChildren` (`Lua\Units\RCTransport.lua:88-90`), `City:AddToLabel` forwards to the **colony** container first (`Lua\City.lua:83-86`) which is the one `Effect_ModifyLabel` writes to (`MarsGameEffects.lua:161-172`), and `max_shared_storage` is modifiable at `scale = const.ResourceScale` with default `30` (`RCTransport.lua:14`) — so +15 lands exactly on SkiRich's promised **45**, and it is read live at `:118, :282, :311, :1709`. ⭐ **This sweep corrected the C18 label rule** — see the C18 row (entry) |
| C29 | Children-only buildings admit all age groups             | ?   | **✅ CLOSED — no defect in Relaunched** | swept 2026-08-02 (prompt 6c). All **three** `children_only` families enforce it at assignment time: residences via `exclusive_trait = "Child"` (`Residence.lua:26-28`) checked in `IsSuitable` `:162-167` / `CanReserveResidence` `:250-255`; training buildings via `CanTrain` → `IsSuitable` (`TrainingBuilding.lua:137-138, :367-376`) which `Workplace` consults at `:930, :1083`; services via `CanService`/`CanBeUsedBy` (`ServiceBase.lua:162-178`). Obvious guess **checked and ruled out**: the `Child` trait IS removed on ageing up (`Colonist.lua:1740-1756`, `RemoveTrait` at `:1747`) (entry) |
| C30 | Supply-pod reward pins stuck on HUD                      | ?   | **✅ CLOSED — no defect in Relaunched** | swept 2026-08-02 (prompt 6c). ⭐ **The stuck-pin MECHANISM is real and sits in the generic path**: `PinnableObject:Done` unpins via `TogglePin()` with **no force** (`PinnableObject.lua:160-164`) while the unpin branch requires `CanBeUnpinned() or force` (`:226`) — and `RocketBase:CanBeUnpinned()`/`UniversalRocketBase:CanBeUnpinned()` return **false unconditionally** (`RocketBase.lua:1476-1478`, `UniversalRocket.lua:1112-1114`). **Every affected class defends against it in its own `Done`**: `RocketBase:Done` → `SetPinned(false)` → `TogglePin("force")` (`:194-199` + `PinnableObject.lua:245-249`); `UniversalRocketBase:Done` → `SetPinOnMap(false)` → `TogglePin("force")` (`UniversalRocket.lua:1069-1074, :1158-1165`); the salvage paths repeat it (`SupplyPod.lua:145`, `UniversalPod.lua:145`). `OrbitalProbe` — the only other `CanBeUnpinned()==false` class — is covered by **`Done` ordering** (`procall_parents_last`, `PropertyObject.lua:1664`) (entry) |
| C31 | Meteor storms broken in 1.0.7.396349 (mechanism unknown) | ?   | cand | RESOLVED 2026-08-01 — his source read: effective half = F78-family StopMeteorStorm heal; GenerateDir half no-ops (entry) |
| C36 | "Inner Light" mystery does not complete for some players | ?   | **✅ SOLVED — not a new defect** | filed AND closed 2026-08-01: **it is a downstream victim of F81(a), which our pack already fixes.** `Dream.lua:20-34` — the mirage loop skips `Dream()` whenever `IsDisasterPredicted()`, the exact flag F81(a) strands permanently true, so the mystery stops advancing forever. **Explains the reporters' "for some people" precisely** (depends on whether a meteor storm completed). ⭐ One commenter gave two unconnected pieces of advice — "install the disasters mod" and "avoid Inner Light" — for one defect (entry) |
| C37 | Planetary anomalies don't pull colonists up the elevator — blocks a purely-underground colony | ?   | cand | filed 2026-08-01 from a **hours-old** Reddit thread (§10.6); specific, current, names the seam. **Same elevator boundary F90 just proved the code mishandles.** Single source, unverified. Next step: is the anomaly colonist-transfer path map-aware? (entry) |
| C35 | Edit Payload confirmed while units are on the cargo ramp tears down the rocket's command-centre connection **with no wait**, where the takeoff path doing the same thing waits | ?   | cand | filed 2026-08-01 by the prompt-6 fredware-#11 comparison — **real gap vs F67/F68/F70/F71 (different function, zero overlap), mechanism traced, HARM UNPROVEN**; ⚠️ not a prompt-7 package until a live repro exists (entry) |
| C32 | Buildings drop out of `ShiftsBuilding` label — stuck on last workshift forever | ?   | cand | **DOWNGRADED 2026-08-01 (prompt-6 Src sweep): no route in current Src; his fix's firing explained by destroyed buildings; 1.0.7 killed the named trigger, not the mechanism — and F04's reassignment lost its positive evidence** |
| C33 | Whole-track demolition leaks an undeletable invisible TrackBase shell — OUR F44 path reproduces it | ? | cand | VERIFIED vs Src 2026-08-01 (fredware source) — needs F-row decision (entry) |
| C34 | Stale-ACTIVE rain: `g_RainDisaster` set, main_thread dead — reads disaster-active forever | ? | cand | filed 2026-08-01 (fredware source held) — **ADOPTED as the Tier-1 rains-pass rider, BUILT 2026-08-01 into Fix_RainsDeadlock's migration pass (structure → FinishRainProcedure heal → migration; manual fallback for invalid values); VERIFIED live by Tier-1 leg 3 2026-08-01** — planted `g_RainDisaster="toxic"` with a dead main_thread, and on reload the log read `0:23:39 RainsDeadlock: stale-ACTIVE rain 'toxic' (main_thread dead) — healing through vanilla FinishRainProcedure (C34)`, with `g_RainDisaster` false afterwards (entry) |
| C38 | Astrogeologist's "Extractor production +10%" misses 2 of the 12 buildable extractors | ? | cand | filed 2026-08-02 by the C18 sweep — **VERIFIED vs Src**: `CommanderProfilePreset.lua:336-385` enumerates ten labels for an **unqualified** promise and omits `AutomaticMetalsExtractor` and `MicroGAutoWaterExtractor`, both currently buildable and both carrying the modified prop. Sibling tell is the enumeration itself. Not promoted — §4 decision is prompt 7's (entry) |

Severity: P1 = gameplay-breaking/major loss, P2 = wrong numbers or notable misbehavior, P3 = cosmetic/latent/mod-facing.

---

## P1 — gameplay-breaking

### F01 — Cave-ins ignore "No Disasters" rule  `[tested: Code/Fix_CaveInsNoDisasters.lua — PT-11 PASS 2026-07-29: two 20-game-hour legs either side of a save/reload, scheduler compressed to a ~1h interval and re-armed so it really was ticking, CaveInRubble count held at 27 throughout; positive control CheatTriggerUndergroundMarsquake() then took it to 36 (+9, one quake's worth — rubble_count = 10), proving the detector moves when a quake fires]`
`Lua\Marsquake.lua:306-325` — `MapGameTimeRepeat("UndergroundMarsquake", ...)` has no
`IsGameRuleActive("NoDisasters")` check; every other disaster has one (ColdWave.lua:222,
DustStorm.lua:413, DustDevils.lua:189, surface quake Marsquake.lua:43). Matches live
Paradox-forum report. **Fix:** wrap FUNC slot (index 3) of `PeriodicRepeatInfo["UndergroundMarsquake"]`.

**✅ WITNESS RE-DERIVED 2026-08-01 — the audit's "NOT re-derivable" is now
retracted, and the replacement evidence is BETTER than the claim it rescues.**
The owner ran the logged-in Paradox subforum browse that the audit booked as a
stop-and-ask (§7.1 item (a)); the Cloudflare block was the only thing hiding
this. Report by **Rubik** (member since Apr 18 2020), **May 8 2026**, on the
subforum's bug-report template:
> **Summary:** "Cave-ins occur when the No Disasters rule is used"
> **Description:** "I started playing a new game after the V1.0.7 update using
> the No Disasters game rule. I seem to remember that in previous versions of
> the game, that rule would prevent cave-ins from occurring in the underground.
> However, I am seeing periodic cave-ins in my current game."
> **Steps to reproduce:** "1.) Start a new game with the No Disasters game rule
> active. 2.) Research the Elevators tech to access the underground area. 3.) In
> the underground area, observe that cave-ins occur on a periodic basis."
> **Platform:** Steam · **Game Version:** 1.0.7

**Why this is stronger than the sentence it restores.** It is first-party, dated,
**version-stamped to 1.0.7** (our pinned build family), and carries steps to
reproduce — where the original record was an unattributed "matches live
Paradox-forum report" that no later session could find. It also matches the
mechanism on the one word that matters: the reporter says **"periodic"**, and
the defect is precisely a `MapGameTimeRepeat("UndergroundMarsquake", …)` with no
`IsGameRuleActive("NoDisasters")` term (`Marsquake.lua:306-325`). Three
independent witnesses now agree — this report, fredware's #9
(*"Prevents periodic underground Marsquakes and cave-ins when No Disasters is
enabled"*), and the sibling tell.
⚠️ **One thing this does NOT establish:** the reporter's *"in previous versions
that rule would prevent cave-ins"* is a recollection, not a measurement, and
nothing here says the OG build had the check. Our claim is and stays about
Relaunched source. **No code consequence — PT-11 already PASSed.** What changes
is provenance: the audit row and its §1 tier need to agree with this.

### F02 — Meteors strike ~every 6h instead of 35–115h  `[tested 2026-08-01 (Tier-1 legs 1+2+5, logs Mars.exe-20260801-16.42.31 and -17.11.08, uninstall -19.14.11 — cadence in the roll, warning timing unchanged three ways, watchdog proven live on a real wedge, thread survives uninstall on vanilla's body; see the leg note at the entry's end): Code/Fix_MeteorFrequency.lua — REOPENED by PT-01 FAIL; REWORKED 2026-07-26 with a stall watchdog + forensics; PT-01 silence ROOT CAUSE PINNED 2026-07-29 to F78 + F81, wave-6 fixes shipped; **REWRITTEN 2026-08-01 (F86 Tier-1, spec §6.2a-A): layer-3 keyed GetDisasterWarningTime wrapper, vanilla's own body — the body copy and its heartbeat surface are DELETED; the per-load restart (F88) replaced by a one-shot version-latched heal (SMRFixPack_MeteorLatch GameVar); watchdog liveness moved onto an additive OnMsg.MeteorDone timestamp. Verification rides the Tier-1 legs (A/B pair + F88 load-3× mini-leg)** — see the rewrite note at the entry's end]`

> 🔬 **ROOT CAUSE SHARPENED 2026-07-31 — it is not "a dead `if`", it is a
> COLLAPSED POLLING LOOP, and the `Min` is not the bug.**
> The broken first phase (`Meteors.lua:280-283`) is a fossil of the loop that
> still exists intact **40 lines below in the same file**, in `MeteorStorm`
> (`:319-341`): same `start_time`, same `GameTime() - start_time > X - warning_time`
> test, same magic `Sleep(5000)`. In the sibling that `Sleep(5000)` is the poll
> interval at the **bottom of a `while`**, and the `if` is the early exit that
> issues the warning and `break`s. In the meteor version the `while` is gone and
> the loop **body** has been pulled inside the `if`. Because `start_time` is
> assigned and read with no yield between, `GameTime() - start_time` is always 0
> and the test degenerates to `warning_time > spawn_time`, deciding nothing but a
> pointless five-second nap.
> - **The intended shape** (identical in `DustDevils.lua:168-173`) is a two-phase
>   wait whose total is always `spawn_time`: `Sleep(spawn - warning)` then
>   `Sleep(Min(spawn, warning))`. **`Min(spawn_time, warning_time)` is the correct
>   clamp** for when warning exceeds spawn — DustDevils has it verbatim. It only
>   looks like the bug because with phase 1 deleted it became the whole interval.
> - **Why the symptom inverts with tower count.** Interval = `Min(spawn, warning)`
>   and `GetDisasterWarningTime` = `Min(base + 12h × towers, 75h)`. No towers →
>   ~6 h between strikes (catastrophic). Several towers → 65-75 h, i.e. towers
>   **accidentally repair the cadence**. The players actually harmed are early
>   colonies with no Sensor Towers; a tower-rich late colony reads as "meteors
>   are rare", which is why the 2026-07-31 PT-20 fixture showed 75 h.
> - **Sensor towers contribute NOTHING to single-meteor warning, and that is
>   designed.** The "Incoming Meteor" notification is preset `MeteorImpact`,
>   raised only by `BaseMeteor:Predict()` (`Meteors.lua:430-441`) off
>   `meteors.prediction_time` — default **30 game seconds**, help text *"time
>   before appearance to be able to register a mark on the ground FX"* — which
>   does not scale with towers. `AddDisasterNotification` appears in `Meteors.lua`
>   only in the two **storm** paths (`:179`, `:328`). So there is no deleted
>   warning to restore: restoring phase 1 restores the *cadence* and nothing else
>   observable. **Owner decision 2026-07-31: 30 seconds is adequate for a single
>   meteor's risk; tower-scaled meteor warning is a FEATURE and is declined.**
> - **Consequence for the rewrite (see F86).** The fix needs no body of its own:
>   make `GetDisasterWarningTime` return `Max(orig, spawntime + spawntime_random)`
>   for the meteor descriptor and vanilla's own `Min` becomes `spawn_time`. That
>   also removes the tower dependence as a side effect rather than as a second
>   fix. `Fix_MeteorFrequency`'s current body is an F86 leak site and must go.

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

**RESOLUTION (2026-07-29): the PT-01 silence root cause is PINNED — and it was
never this fix's loop.** The live sitting traced it to the meteor STORM side:
a wedged MeteorStorm drain loop held the scheduler thread forever (F78), and
the ended storm's stranded `g_DisastersPredicted` flag gated the entire
weather system (F81) — "BOTH disaster threads went quiet" above was exactly
that. The F02 watchdog's silence-watch captured the evidence as designed.
Wave-6 fixes shipped: `Fix_MeteorStormWedge` (F78) +
`Fix_DisasterPredictionLeak` (F81) — full trace and evidence live on those
two entries. The F02 watchdog stays as a standing safety net.

**REWRITE (2026-08-01, F86 Tier 1 — spec `SAVE_SAFETY_REDESIGN.md` §6.2a-A).**
The body copy is gone: the fix is now a layer-3 wrapper on the synchronous
`GetDisasterWarningTime`, keyed on `CurrentThread() == rawget(_G, "Meteors")`
(a falsy global takes the orig path — defence in depth, measured not
load-bearing). On the keyed path it returns `Max(orig(descr), descr.spawntime
+ descr.spawntime_random)`, so vanilla's `Min(spawn_time, warning_time)`
(`Meteors.lua:291-292`) equals `spawn_time` and **vanilla's own body produces
the designed 35–115h schedule**. The MeteorStorm thread passes the same
descriptor and keeps vanilla warning timing (the key is what makes this not a
balance change). `GlobalGameTimeThreadFuncs.Meteors` stays vanilla's; the
heartbeat surface (`MeteorsBeat`/`MeteorsBeatSet`/`MeteorsNote`) died with the
copy. The per-load `OnMsg.LoadGame` restart — F88's defect — is replaced by a
**one-shot latched heal**: `GameVar("SMRFixPack_MeteorLatch", false)` holds
the last-healed pack version; PostLoadGame restarts the thread once per save
lineage per version and stamps the latch. The PT-01 watchdog keeps its
threshold, ladder and guards; its liveness input is now an additive
`OnMsg.MeteorDone` timestamp, and its restarts recreate vanilla's body.
Disclosed residuals: the dead `if` gains `Sleep(5000)` ≈ 10 game min/cycle
with warning > spawn (negligible), and the latch GameVar stays in saves as
inert data.

**✅ TIER-1 LEGS 1+2+5 RUN 2026-08-01 — this entry flips to `tested`** (owner
at the keyboard, one sitting; save lineage `save_game_id HdmSxGs6kyd0uz6-`,
map BlankBigCanyonCMix_09; logs `Mars.exe-20260801-16.42.31` (first load),
`-17.11.08` (main sitting), `-19.14.11` (uninstall)).

- **Cadence is in the designed roll (leg 1).** Three measured scheduler gaps:
  **75 h** (`t=216351730`→`218608231`, pristine), **83 h**
  (`227810769`→`230312200`, post-recovery), **72 h** (→`232476636`) — all
  inside 65–90 h, and a further 86.7 h gap interleaved with the natural storm.
  Gaps are only cadence when both prints are the scheduler's; event-spawned
  strikes were excluded by attribution (strike #3 at `t=225356557` traced to
  the Singularity story bit — event spawners enumerated from Src, only the
  story-bit line sits between #2 and #3).
- **Storm-warning timing is UNCHANGED — the keyed wrapper's whole reason for
  existing — proven three independent ways.** (a) The probe's keyed/unkeyed
  discrimination PASSes; (b) a live console read of
  `GetDisasterWarningTime(GetMeteorsDescr())` from a NON-Meteors thread
  returned **2250000** (the 75 h tower-cap, *not* the keyed 2700000), so the
  key really does scope the override to the Meteors thread alone; (c) the
  natural storm's own UI countdown read **"Starts in 3 Sols 2 h" ≈ 74 h**.
- **The one-shot heal is genuinely one-shot.** First load:
  `MeteorFrequency: one-shot heal — persisted Meteors thread was alive;
  restarting onto vanilla's body (latch false -> 1.0.1)`, exactly once.
  Reloads across the whole sitting: **no second heal** (leg 2's three loads
  produced zero pack lines) — the version latch is honoured round-trip.
- **The watchdog was not theatre — it fired on a real defect.** F89 was
  discovered mid-leg (drain-loop wedge on the *singles* path, 192 h of
  silence). The watchdog detected it at its 189 h threshold (`ALIVE but
  stuck`), restarted the thread, and cadence resumed. Keeping the watchdog
  through the rewrite was the right call, and this is the evidence.
- **Uninstall (leg 5).** With the pack disabled, FixtureCarry read
  `Meteors: thread: …, valid=true` and `Meteors body: function: …` — the
  thread survives on **vanilla's** body, which is precisely F86 Site 1's harm
  ("kills the colony's meteors permanently") no longer happening. The latch
  read `SMRFixPack_MeteorLatch = (absent)`, i.e. *below* the residual the spec
  budgeted for, and **zero lines or errors named this module**.

⚠️ **What leg 5 did NOT read, stated plainly:** the meteor logger
(`SMRTest.Log.Meteors`) is a per-session toggle and the full game restart
cleared it, so no meteor *cycle* was instrumented in the uninstalled state.
The owner observed a warning appear and the meteor never arrive — which is
ordinary **vanilla F89** with no watchdog present to heal it, and is the
expected post-uninstall behaviour rather than a finding. The uninstall claim
above rests on the thread/body read and the zero-error log, not on that
observation.

Cross-refs: F78, F81, F86, F88, F89.

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

**Audit 2026-08-01 (external witness): tier corrected GOLD → BRONZE-B2.** The
Steam thread "Buildings are stuck on night shift" was initially matched to
this entry, but GromGor's extracted Workshifts-FixUp source revealed a
*different* live mechanism that fits the thread better — buildings falling
out of `UIColony.labels.ShiftsBuilding` and never receiving `SetWorkshift`
again (**filed as C32**; the thread describes stuck BUILDINGS colony-wide,
with an asteroid-range correlation that fits label rebuilds, not our
colonist-side hour-window). F04's own defect claim is unchanged — the
shift-3 window arithmetic at :1758-1768 stands on the sibling tell
(shift-1/2 windows are correct) — but it currently has **no external witness
that discriminates it**, and the two mechanisms may co-produce the reported
symptom family.
⭐ **RE-EXAMINED 2026-08-01 (chain prompt 6 C32 sweep) — THE REASSIGNMENT'S
POSITIVE EVIDENCE DID NOT SURVIVE THE SOURCE PASS. Read this before treating
F04 as BRONZE-B2.** The demotion rested on C32 being the *better* mechanism
match. The sweep (BUGS C32, §§1-5) found **no route in current Src** for C32 as
filed, and specifically refuted the inference that carried the reassignment:
the audit reasoned that the reporter's "an asteroid had recently gone out of
range" fits *"label rebuilds on map transitions"*, but there is no label
rebuild on a map transition in Src — `OnMsg.PostDoneMap` →
`UIColony:ValidateLabels()` (`Lua\Colony.lua:116-120`) only purges **invalid**
objects, i.e. buildings *on the unloaded map*, and never touches a main-map
building. It also found that the one observable that made C32 look real —
GromGor's fix firing in the wild — is fully explained by destroyed-but-not-
rebuilt buildings (`Building:OnDestroyed` is empty while
`ShiftsBuilding:OnDestroyed` de-labels), which is not a defect at all. And the
onset condition itself cannot occur unattended on 1.0.7 (`Asteroids.lua:1,
:208, :331-348, :493-500`).
**What that does and does not do to F04.** It does **not** restore GOLD by
itself: the thread's reports are 1.0.6-era and this session read 1.0.7 only, so
neither mechanism is discriminated *for that reporter's build* by source alone.
What it does is remove the reason F04 lost the witness — the audit swapped a
GOLD witness onto a mechanism that now has no code behind it. **F04's own
defect claim is unchanged and stands on its sibling tell either way.**
**The tier decision is prompt 7's, not the sweep's**, and it needs to choose
between: (i) restore F04's witness and tier, (ii) leave both entries
witness-less, or (iii) hold pending the corrected live rider
(`PLAYTEST_CHECKLIST.md` §6, C32 row).
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

**Audit 2026-07-30 (reachability): R2 — and easier to hit than this entry says.**
The Epilogue popup arrives MINIMIZED by SA default (`SA_WaitMessage` inherits
`start_minimized = true`, SequenceAction.lua:207, and the Epilogue call passes
no override) and the pause layer engages only after the player opens it — so
the one-sol miss window passes in ordinary inattention at fast-forward;
"the player can minimise and ignore" understates. Full block in
REACHABILITY_AUDIT.md.
**⛔ EXTERNAL CORROBORATION CORRECTED 2026-08-01 — one of the two cited threads
is a RETRACTION.** The owner opened the `[S22]` threads the bug-list audit could
only see at title grade (`BUG_LIST_AUDIT.md` §10.4):
* **`1113731` "Crystal Entity / Philosophers Stone Mystery stuck"** (mgla, Aug 7
  2018) — the post's own first line is **"NOT A BUG: I missed a crystal."**
  **Struck; it was never corroboration.** It was counted as such because only
  its title had ever been read.
* **`1112166` "Philosopher's Stone Stuck on Finishing"** (Hockston, Jul 26 2018,
  v231.777) — **genuine, and it matches this entry's signature**: the big
  crystal formed, then *"I gave up on the mystery completing after a good while
  of waiting for the crystal to do something. It didn't get the green checkmark
  on new game mystery list either"* — i.e. the crystal never resolved and
  `MysteryEnd` never fired. **But grade it low:** OG-2018 (not Relaunched); the
  reporter had destroyed several crystals so the formation was *"not
  contiguous"* (a confound the post itself flags); and its only apparent second
  witness is **mgla, who retracted the identical report the same day**.

**Net: this entry's external support is ONE confounded OG report, not two.**
Nothing about the defect claim changes — it stands on Src, where
`Msg("CrystalFlyAway")` fires exactly once and `CrystalForceFlyAway` has **no
emitter anywhere**, neither of which any witness was ever load-bearing for.
*(Same post, unfiled lead: Hockston reports the **Spheres** mystery also failing
to mark complete on the same build — two different mysteries, one player, one
version, which hints at shared completion machinery rather than a crystal
bug.)*

**Popup audit 2026-07-30 (`POPUP_CONSEQUENCE_AUDIT.md`): F06 is NOT an F83-family
member.** Sequence threads are game-time and persist across saves with their
blocked popup waits (no shipped scenario sets `real_time`); this defect is a
**one-shot `Msg` fired while the sequence sat in a player-gated popup** — a
path-vs-state race needing no save/load at all. The re-broadcast fix remains the
right shape; nothing to re-scope.
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

### F10 — Faction funding conditions always error  `[wontfix — CLOSED 2026-07-27; PT-36 PASS on a real save; premise falsified twice over]`
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

**Audit 2026-07-30 (reachability): U — kept, settling observation recorded.**
The sole call site (Train.lua:447, UnloadTrain) is unconditional in train play,
but every Lua-visible path keeps `train.units` synced; the stale-passenger
state the guard exists for bottoms out in engine-side `TransferToMap`
(`Unit:EnterTransporter`, Unit.lua:1202-1209 — crew-gathering explicitly takes
BUSY colonists including riders, CargoTransporterNew.lua:221-234), which
source alone cannot settle. Observation that settles it: with a colonist
mid-ride, launch a crew expedition that dips into busy colonists, then inspect
`train.units` (or catch the shipped TrainsLogging "not in train" warn) — a
stale entry makes this R2. Playtest-item candidate. Full block in
REACHABILITY_AUDIT.md.
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

### F14 — Domes Overview red low-stat highlight dead  `[tested: Code/Fix_DomeOverviewHighlight.lua — PT-09 PASS 2026-07-28; archived]`
`Lua\X\ColonyControlCenter.lua:1309-1320` — builds red-tagged `tv`, then calls
`win.idLabel:SetText(v)`. **Fix:** override `Community.UICommandCenterStatUpdate`, end with
`SetText(tv)`.
*PT-09 observation (2026-07-28):* with the highlight restored, the overview's fifth stat
column (**Satisfaction**) reads red 0 on every dome of a mature colony — correct and
vanilla-intended: Satisfaction is the tourist-rating stat (`Colonist:ChangeSatisfaction`,
`Colonist.lua:3905-3918`, zeroes positive gains past the tourist sol window), so
long-resident populations average ~0 and the below-30 rule paints the column. The bug had
hidden that red along with the real ones; a vanilla design wart exposed, not caused.

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
**✅ EXTERNAL CITATION READ AND CONFIRMED 2026-08-02** (`BUG_LIST_AUDIT.md`
§10.4). The audit cited Paradox thread `1495056` for this entry at *title grade
only*; the owner opened it. **It holds up** — Homeshine, Oct 18 2021 (Below and
Beyond hotfix 4), *"After completing the mystery of the spheres, the dialog
never goes away for 'cold wave' and the dialog for 'Sphere countdown: 101%'"*,
save attached, self-declared reproducible. **Three corroborators, across three
different mysteries:** shannley (*"Same Problem"*), Candergart on **St. Elmo's
Fire**, omega telescope on **The Last War**. ⚠️ **OG-2021 — it corroborates the
incomplete-cleanup FAMILY, not the Relaunched build**, and this entry's own
defect claim rests on Src regardless. *(Contrast `1113731`, cited for F06, which
turned out to be a retraction — reading bodies moves citations both ways.)*
**Lead recorded, unassigned:** several mysteries failing to complete or clean up
suggests shared upstream state, and C36 proved one instance — Inner Light stalls
because it gates on `IsDisasterPredicted()`, which F81(a) strands. Whether other
mysteries gate the same way is an open, cheap grep. Full note in §10.4.

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

**Audit 2026-07-30 (reachability): R2 — gate previously unrecorded here.** The
DustSickness trait is granted ONLY by the DustSickness storybit family, and
the parent storybit requires the **Dust in the Wind** game rule
(Data\StoryBit\DustSickness.lua:19-21; plus sol ≤ 100, ≥ 30 colonists,
DustStormStart trigger). Within that rule the defect is near-certain — the
rule maximizes dust storms. Full block in REACHABILITY_AUDIT.md.
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

### F19 — Graphs "Consumed" caption omits maintenance  `[tested: Code/Fix_GraphConsumedCaption.lua — PT-43 F19 read PASS 2026-07-28: Machine Parts caption "Consumed (4)" tracked the ~4-6 per-sol bars (maintenance included; old behavior was near-zero beside them), Food caption "Consumed (116)" vs ~100-104 bars = real consumption unchanged, not over-broad]`
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

### F20 — Morale tooltip shows unapplied +Comfort bonus  `[tested: Code/Fix_MoraleComfortTooltip.lua — PT-43 F20 read PASS 2026-07-28: high-Comfort colonist showed NO phantom "Living in luxury" row with rows summing to the title (base 40 + 5 Health + 5 Sanity = 50 exact); a Comfort-0 colonist (driven low via ChangeComfort console line, logged reason) still showed the REAL penalty row "I cant live like this -10 (Comfort)" alongside +5 Health / -10 Sanity — penalty kept, fix not over-broad, Health/Sanity rows intact in both directions]`
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

### F21 — Train travel-time penalty includes station waiting  `[fixed: Code/Fix_TrainWaitTime.lua — ⚠️ DOWNGRADED FROM `tested` 2026-08-01: the F86 Tier-2 rewrite replaced the mechanism PT-43 exercised, so the pass below is evidence about a body that no longer ships. Re-flip only on a leg run against the wrapper. Prior reading, kept for the record — PT-43 F21 read PASS 2026-07-28: a 17+ hour platform wait produced ZERO travel Comfort entries; a migrant with a 16-hour total trip arrived at Comfort 99 (vanilla would have billed ~-16); the train's "Travel time (rolling average)" read 4.15 hours against riders with 16-17h queue-inclusive trips — the stats and the penalty both exclude waiting, one shared start_wait mechanism verified end-to-end. Setup detour surfaced F79 + F80 (entries)]`
`Lua\Units\ColonistTransport.lua:493,511,551-569` — `ticket.start_wait` set on reaching
platform, never reset at boarding; Comfort "travel time" penalty and train/track
"spent time" stats (TransportStatistics.lua:31-45) count waiting (double-counted vs
station stat). *(QA audit 2026-07-25 struck the "partially bypasses LuxuriousTrains"
claim — the tech gates the ENTIRE ChangeComfort at :555-557, so nothing bypasses it;
post-research the comfort half is simply moot.)* **Fix:** reset
`transport_ticket.start_wait = GameTime()` at boarding.
~~*Implemented as a full replacement, not a wrapper, because no wrapper can run in
time:* `Colonist:BoardVehicle` (`:503-528`) is issued as a command
(`Train.lua:967`) and the ride ends with `SetCommand("ExitVehicle")` killing the
thread inside the blocking loop — a post-wrapper would never run at all (the
command-method rule), and a pre-wrapper would erase the wait before `:511` credits
it to the station.~~ **That reasoning was right about `BoardVehicle` and wrong about the
repair: it only ever asked whether `BoardVehicle` itself could be wrapped.** It cannot;
nothing here needed it to be.
Only the boundary between "waiting" and "travelling" moves to where the colonist actually
boards — the station keeps the full wait either way.

**⭐ F86 TIER-2 REWRITE, 2026-08-01 — the restamp moves onto a synchronous input.**
`Colonist:BoardVehicle` blocks for the whole journey (`PlayPrg` inside
`while self.holder == vehicle`, `:525-527`), so a copy of it is F86 exposure route (a),
REPLACE-class. What the restamp actually needs is the MOMENT, and vanilla marks that moment
itself: `:511` calls `TransportStatistics:AddSpentTime` on the station — the line that pays
the station for the wait, immediately before the ride starts. That method is **verified
synchronous** (`TransportStatistics.lua:31-37`: `#`, `table.remove`, `table.insert`,
arithmetic; `tools/blocking_analysis.py` reports it `clear`), and its call sites are
enumerated: exactly three in the shipped source, `:511` on a **Station**, `:568` on the
Train, `:569` on the TrainTrack. `IsKindOf(self, "Station")` therefore keys the boarding
moment precisely and cannot reach the statistics calls. The boarding colonist is identified
exactly rather than guessed — `BoardVehicle` is a command (`Train.lua:967`), so it runs on
that colonist's own thread and the colonist is still in `station.waiting_for_train` at
`:511` (removed later, in the destructor at `:517`); one scan for
`command_thread == CurrentThread()` finds them, and no two objects can share a command
thread. Disclosed narrowing: the restamp now happens only where vanilla credits a Station
(`self.holder` truthy and a Station at `:510`) — every shipped boarding path gets there
(`GoToStation` enters the station before joining `waiting_for_train`, `:447-455`), so the
difference is unreachable in vanilla and fail-safe if a future path changes that.
**Disposition (FIX_POLICY §3a per-site gate): REPAIRED IN-PACK — layer 3, no residue,
nothing owed to D13.**
Probe: `TrainWaitTime` in `40_Probes_Wave4.lua` — ⚠️ realigned 2026-08-01 with this rewrite.
Playtest: PT-43.

### F22 — `GetGridGlobalStorage` breaks Last Transmission gates  `[fixed: Code/Fix_GridGlobalStorage.lua]`

**Audit 2026-07-30 (reachability): R1 — stronger than this entry implies.**
UndergroundMap is generated at new-game map generation for every surface game
(RandomMapGenerator.lua:819-820 → Picard.lua:263-292; only the
NoUndergroundAndAsteroids rule skips it), so the zero-demand sentinel corrupts
the sum from sol 1 — and the six Last Transmission conditions are evaluated
EVERY GAME HOUR by FactionsHolder:RecalcFactionsApproval over all FactionDef
presets (Factions.lua:690-697), gated only by NoPolitics. No "player opens the
Underground" step is needed. Full block in REACHABILITY_AUDIT.md.
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

### F23 — Founder-gains-trait notification never fires  `[tested 2026-07-30 — PT-44 PASS: Code/Fix_FounderTraitNotification.lua]`

**PT-44 PASS — 2026-07-30, live.** Trigger: `founder:AddTrait("Fit")` on a
Founder lacking it — the same call a shipped **Open Air Gym** makes
(`OpenAirGym.lua:10`), through the real `Colonist:AddTrait`, which emits
`Msg("ColonistAddTrait", …)` synchronously (`Units/Colonist.lua:427`).
Evidence, objective counter first:

| Check | Result |
|---|---|
| `SMRFixPack.FounderTraitNotification.fired` | **0 → 1** |
| `FindNotification("FounderGainsTrait")` | `false` → `true` |
| Notification rendered | **"Founder Has Trait" / "Ciara Grant: Fit"** — correct colonist, correct trait |
| Duplicate check | **exactly one** notification — the dead shipped handler stayed dead, so the dedupe guard was not even needed |
| Module status | `active` throughout |

**Path vs rendering, stated honestly:** the grant was console-injected, so this
run proves the notification *fires, renders and reads correctly* — which is
exactly what PT-44 exists to check ("probes cover the wiring; play confirms the
notification renders"). It does not itself prove the player path, but the path
was never the open question: the reachability audit graded F23 **R1** with a
full enumeration, and a re-grep confirms a dozen live shipped callers of
`AddTrait` on existing colonists — Martian University specializations
(`MartianUniversity.lua:30`), School / SchoolSpire, Sanatorium, Open Air Gym,
Project Morpheus, CovertOps, the Dome `Renegade` path, and storybit/faction
effect classes.

**Vanilla behaviour recorded so it is never filed as a defect:** PT-44 used to
say "clicking it selects them". That is only true when the colonist is
**visible**. A notification click runs `ViewCycledObj`
(`Lua/UI/OnScreenNotification.lua:1-19`), which calls `ViewAndSelectObject` only
for an object with `efVisible ~= 0`; a colonist inside a building (Ciara Grant
was "Resting in Living Complex") falls to the `ViewObjectMars` branch — camera
only, no selection. Correct by design: you cannot select a hidden unit. The
checklist wording was corrected accordingly.
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

### F24 — Dome pipe visuals corrupt on load (`MoveInside` copy-paste)  `[wontfix 2026-07-30 (user decision) — real defect, UNREACHABLE in the shipped game; fix file DELETED, module count 75→74 / 69→68 default-active]`

**CLOSED `wontfix` 2026-07-30 (user call), on a reachability proof built while
trying to run PT-44's F24 half.** The defect below is real and the diagnosis
stands — it was never a player report, it was found by diffing the water grid
against its electricity twin. But nothing in the shipped game can reach it, so
the pack was carrying a 34-line full-function replacement of
`LifeSupportGridObject:MoveInside` (a copy that would rot on any future patch to
that function) to guard a state vanilla cannot produce. **`Code/Fix_DomePipeMoveInside.lua`
deleted; removed from `metadata.lua`, `items.lua` (ModItemCode) and the README
fix table.** Rollback is `git revert` — the file is one commit away if a
counter-example ever turns up.

**The reachability proof (do not re-derive).** `MoveInside` has exactly two call
sites in all of `Src`:
1. **`MartianAssembly.lua:60`** — `AssemblyFakeBase:GameInit` teleports the real
   Assembly into the fake's dome and calls `MoveInside(self.parent_dome)`. Live
   and in-play, but **it cannot reach the buggy line**: `SpireBase.__parents =
   { "Building" }` and the `MartianAssembly` template declares no water or air,
   so `LifeSupportGridObject:MoveInside` is not in that class chain at all.
2. **`Dome:OnLoad` (`Dome.lua:896-899`)** — the repair sweep the original
   diagnosis names. It only acts on a building inside the dome's interior shape
   whose `parent_dome ~= self`, and the buggy loop body only executes when
   `SupplyGridRemoveBuilding` returns live connections — i.e. a **pipe-connected
   life-support building sitting inside a dome's interior hexes but not parented
   to that dome**.

That state cannot arise in vanilla, on three independent grounds:
* **A dome will not place over existing buildings** — confirmed in play
  2026-07-30 across multiple dome types, sizes and angles; the placement Status
  panel reads *"Objects underneath are blocking construction."*
* **No dome has an upgrade.** Every `Data/BuildingTemplate/*Dome*.lua` was
  checked — zero `upgrade1/2/3_id` values. The old PT-44 wording ("build or
  **upgrade** a dome") described a mechanic that does not exist.
* **A dome's interior shape never changes at runtime** — no `SetInteriorShape`
  and no `interior_shape` assignment anywhere in `Lua/`.

So the sweep's `parent_dome ~= self` branch is defensive code for states
produced by older versions, map scripts or other mods — not by play. Filed
alongside the same judgement call the pack already makes for F28 and F43
(real, latent), except here the user chose deletion over carrying it, because
this one costs a whole-function copy rather than a one-line patch.

**PT-44 consequence:** its F24 half was **unrunnable as written** and has been
removed; PT-44 now covers F23 only. That is the **third** PT procedure found
unrunnable by executing it (after PT-29 and PT-11) — the standing rule that an
un-run PT's procedure is unverified until executed once holds again.

**Original diagnosis, kept for the record:**
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
Probe: `[install]`-free — the fix was to be verified through F24's own playtest,
PT-44, because the behaviour needs a real dome absorbing a real pipe-connected
building. **That is exactly what proved impossible** (see the closure block at
the top of this entry). No TestKit probe ever existed for this fix, so its
deletion does not move the 77-probe A/B counts — only the module counts.

### F25 — Tech description names wrong building (pre-1.0.6 saves only)  `[fixed: Code/Fix_TechDescriptionBuilding.lua]`

**Audit 2026-07-30 (reachability): R2 (legacy save) — "pre-1.0.6 only"
CONFIRMED, one probe-label doubt.** `UndergroundRework106` is a persisted
GameVar set true only on OnMsg.NewGame (UndergroundDome.lua:16-19), so only
saves started pre-1.0.6 show the tech — a genuine R2 condition. But the
preset itself is placed unconditionally (the condition gates TREE MEMBERSHIP,
not preset existence), so the probe's stated SKIP reason "tech not present on
a current build" may be mislabeled — the patch target should exist on any
build. Low stakes; worth a look next TestKit pass. Full block in
REACHABILITY_AUDIT.md.
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

### F28 — `Research:ReplaceTech` mishandles the field counter  `[wontfix 2026-07-30 (user rule) — REACHABLE ONLY FROM MOD CODE, barred by FIX_POLICY §4a; Code/Fix_ReplaceTechCount.lua and its TestKit probe both DELETED; counts 74→73 registered / 68→67 default-active, probes 77→76]`

**CLOSED under the new hard rule, not on its merits.** The defect below is real
and the diagnosis stands. It is retired because **`Research:ReplaceTech` has
zero callers in all of Src** — independently re-verified 2026-07-30, the
whole-tree grep over `Lua/`, `Data/`, `CommonLua/` and `DLC/` returns exactly
one hit, the definition at `Research.lua:684`. Only mod code or the console can
reach it.

**This was never an oversight — and that is the point.** The entry's own second
line said *"No vanilla caller; hits mods/storybits/console"* the day it was
filed. It shipped anyway, on a "modder benefit" rationale, as a **§1.5 full
replacement** (37-line body copy) carrying per-game-update re-verification cost
forever, for a code path no player can execute. **FIX_POLICY §4a now bars that
rationale outright** (owner rule, 2026-07-30): this pack does not fix other
mods' problems, and a vanilla defect reachable only from mod code is not a
player fix. That rule, not this entry's evidence, is what closed it.

Distinguish it from **F24** (also deleted 2026-07-30): F24 was an *error* —
nobody knew it was unreachable until asked. F28 was a *decision*, and the rule
reversed the decision.

**Removed:** `Code/Fix_ReplaceTechCount.lua`, its `metadata.lua` code entry, its
`items.lua` ModItemCode entry, the README fix-table row, and the
`ReplaceTechCount` probe (TestKit `40_Probes_Wave4.lua`). The probe had to go
with it — it drives the real method and asserts the *fixed* counter, so with the
fix gone it would FAIL in every leg. *Optional future refinement:* it could be
rebuilt as a vanilla canary on the **F10 precedent** (`FactionFundingCheck`
survived F10's deletion and is now the single baseline PASS), which would give
a tripwire if a game patch ever wires `ReplaceTech` up. Not done — that is new
assertion code and nobody asked for it.

**Rollback** is one `git revert`, the F24 pattern.

**Original diagnosis, kept for the record:**
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

### F29 — Sequence-system latents (**NOT** mod-facing — see the 2026-07-30 correction)  `[fixed*: Code/Fix_SequenceLatents.lua — items 1 and 3; item 2 deliberately not fixed. KEPT: R3 latent-by-data, a real player fix under FIX_POLICY §4a]`

**✅ KEPT — and this entry's own self-description is WRONG. Correction
2026-07-30.** It was briefly flagged for removal under the new FIX_POLICY §4a
rule, on the strength of its own words below (*"mod-facing bundle"*, *"ship for
modder benefit"*, *"No shipped user"*). **Those words are false**, and the
reachability audit's enumeration proves it:

* **Item 1** (`SA_GetLabelToRegister`) has **four shipped callers**, all in
  Mystery 2 "Dredgers" (`Mystery 2.generated.lua:298, :315, :365, :369`), and
  **all four execute live in every Dredgers playthrough.** They are harmless
  only because none passes `random_count`/`random_percent`, so the defaults make
  the missing truncation a no-op. A grep of `random_count|random_percent` across
  all of `Data` returns zero presets setting either — **today**.
* **Item 3** (`AlienDigger:GameInit`) likewise **runs live for every digger
  Mystery 2 spawns**. The buggy swap branch needs
  `pre_hit_ground_t < pre_hit_ground_t_2`, and the shipped defaults (1000/500,
  `Diggers.lua:53-54`) are already ordered, so the lines never execute.

That makes F29 **R3 — latent-by-data**, not mod-only: the game runs this code in
ordinary play, and only the current *values* keep it benign. **A patch, a DLC or
new story content can expose it without any mod involved.** Under §4a's test —
*could a player be harmed, now or after a future patch?* — the answer is yes, so
it is a real fix and it ships. Same shape as F27, F31 and F43.

**The mistake is worth keeping on the record:** the flag came from trusting this
entry's self-description instead of the enumeration sitting in
`REACHABILITY_AUDIT.md` — precisely the failure mode that produced the wrong
F49(c) verdict, repeated on provenance rather than on intent. §4a now says
outright: judge by enumeration, never by the entry's own words.

**What F29 does still owe** is unrelated to §4a: it is R3 implemented as two
**§1.5 method replacements**, and ~~the *pending* §4 amendment would require~~ →
**the §4 amendment APPLIED 2026-08-01 now requires** an
explicit owner decision for that combination (latent benefit, permanent
maintenance cost). It is paired with **F57(a)** in that bucket. ~~No action unless
the owner wants the stricter line.~~
**⚠ ACTIVATED 2026-08-01.** The stricter line landed: FIX_POLICY §4 now reads
"**R3 ships only as a §1.1–§1.4 patch**; an R3 §1.5 full replacement needs an
explicit user decision (the F24 lesson)". F29 (items 1 and 3) and F57(a) are
the pack's only members of that combination, and neither has such a decision on
record. **Nothing is presumed either way** — the blanket pre-clearance covered
adopting the rule, not pre-deciding what the rule then asks. The decision is
**routed to chain prompt 7** (`docs/prompts/project/`), which is where §4-bar
decision packages are put to the owner: keep both as replacements (the shape is
already shipped, probe-covered and A/B-clean), convert to §1.1–§1.4 where a
wrapper can reach the defect, or drop the latent halves. It is a decision owed,
not a defect found — nothing here is claimed to be wrong.
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

**Audit 2026-07-30 (reachability): item (d) R2, one wording correction.**
Shipped Lua sets the "Embark" command only on DRONES (rocket/rover/transporter
boarding) — the fix header's "boarding colonists" overstates; colonists board
via other commands and were never protected by this filter in the vanilla
sibling either. The player-visible save is boarding drones plus the lost
dedup. Full block in REACHABILITY_AUDIT.md.
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
**✅ SCOPE QUESTION CLOSED 2026-08-01 — MEASURED, and the answer is that our
scope is RIGHT: the live label path works, for all three labels including
`WindTurbine_Large`.** Owner at the keyboard, log
`Mars.exe-20260801-14.59.57-6a22b86d.log`, a **pre-research save loaded fresh**
so our own pass could not have run first (it early-returns at
`90_SaveSanitizer.lua:58` when the tech is not researched — verified in the same
sitting) and **no reload anywhere in the measurement window**:
* **Before** (tech not researched): all three labels
  `NO MODIFIERS` — a clean baseline, nothing pre-supplied by anyone.
* **After** the tech landed: every one of `WindTurbine`, `WindTurbine_Large`,
  `WindTurbine_Diffuser` carries `prop=electricity_production percent=100`,
  **keyed by the vanilla `Effect_ModifyLabel` objects with `id=GameEffect` — NOT
  `SMRFixPack_F35_*`**, so it is the tech's own apply and demonstrably not our
  sanitizer's work.
* **And it reaches the buildings, not just the colony table** — Power doubled on
  all three, exactly: Wind Turbine 9.3 → 18.6, Large 18.6 → 37.2, Shrouded
  (Diffuser) 29.8 → 59.5. So label *membership* is intact for these classes too,
  and the +100% compounds with the 86% elevation boost multiplicatively
  (`5 × 1.86 × 2 = 18.6`) rather than adding.
* **Trigger stated exactly:** the tech was granted with
  `UIColony:SetTechResearched("FrictionlessComposites")`, not researched
  naturally — it is a **Breakthrough** (`TechPreset.lua:799`, `group =
  "Breakthroughs"`) and was not obtainable in that colony. That is the same
  funnel natural completion uses: `Research:SetTechResearched` →
  `tech:EffectsApply(UIColony)` (`Research.lua:313`) → `Effect_ModifyLabel:OnApplyEffect`
  (`MarsGameEffects.lua:161`) → `SetLabelModifier`; the natural paths
  (`Research.lua:803`, `:841`) reach line 313 through that same function and
  differ only in the `notify` flag, which only adds the popup.
* ⚠️ **A trap this sitting walked into, recorded so nobody repeats it:** the
  first "after" reading was taken while **Low-G Turbines** was completing, not
  Frictionless Composites. `LowGTurbines` (`TechPreset.lua:2830-2844`, group
  Physics) grants two `Effect_UnlockUpgrade` entries (Polymer Blades) and
  **no label modifier at all** — so its three `NO MODIFIERS` readings were
  correct and would have been mis-filed as a P1 defect. Low-G Turbines is the
  "polymer upgrade works" half of the witness's own sentence. Always confirm
  with `IsTechResearched("FrictionlessComposites")` before reading.
**Consequence: the fix is NOT aimed one layer too shallow.** F35 is the old-save
migration failure it was filed as, the pass is not quietly repairing a live
defect on every load, and "witnessed and fixed" is now claimable. What this does
NOT establish: that the Nov 2025 witness was mistaken about *their* game — this
measures build 1.0.7.396349's live path, not theirs.

**~~⚠ OPEN SCOPE QUESTION~~ — added 2026-08-01 by the bug-list audit (§2.2, row
F35, ⚠), closed the same day by the reading above.** The witness thread this entry cites ("polymer upgrade works now,
frictionless doesn't"; TheNightglow Nov 2025 [S27], Frictionless Composites
named with a player-derived formula) **may be describing a LIVE label miss in a
current game, not the old-save migration failure this fix repairs.** If so, our
scope is one layer too shallow: the pass would be quietly repairing on every
load something that should never have broken, and the player-visible defect
would persist for a whole session before the next load. **The rider that
decides it is in `PLAYTEST_CHECKLIST.md` §6** (bug-list-audit table) — research
the tech in a live session and read `UIColony.label_modifiers` **without
reloading**, because our own auto-running pass masks the answer the moment a
save is loaded. Until that reading exists, "witnessed and fixed" is not
claimable for F35.

**✅ SOURCE CROSS-CHECK RUN 2026-08-01 (chain prompt 6, job 3) — scope
CONFIRMED from the other side; nothing filed.** Prompt 2 settled the live half
by measurement, so this was the residual source pass. Three results, all read
in 1.0.7.396349 Src this session:
1. **The defect this entry claims is still present, verbatim.**
   `SavegameFixups.WindTurbine_Large_ReapplyModifiers`
   (`Lua\Buildings\WindTurbine.lua:78-88`) still reapplies **only**
   `WindTurbine_Diffuser` — one `SetLabelModifier` call, no `WindTurbine`, no
   `WindTurbine_Large`. The entry's cited lines are re-verified, not inherited.
2. **Nothing else in the game covers it.** `WindTurbine_Large` appears nowhere
   in any Lua `SetLabelModifier` or savegame fixup in the whole Src tree — a
   grep returns only its `BuildingTemplate` and FX presets. So the old-save
   miss has no vanilla repair on our pinned build and our pass is not
   redundant.
3. **The one 1.0.7 fixup that touches this machinery cannot cover F35 — but it
   does independently justify the PostLoadGame hook.**
   `SavegameFixups.Move_Effect_ModifyLabel_FromCitiesBackToColony`
   (`Lua\MarsGameEffects.lua:180+`) *relocates* existing `Effect_ModifyLabel`
   modifiers out of per-city containers and onto the colony; it never
   re-derives a missing one from a tech preset, so it is no substitute. What
   it does mean is that an old save can carry the turbine modifier on a
   **city** while `UIColony.label_modifiers` — the table our pass reads
   (`90_SaveSanitizer.lua:64`) — is still bare. Had the pass stayed on
   `OnMsg.LoadGame`, it would have run before that move (`Msg("LoadGame")`
   :810 → `FixupSavegame` :811 → `Msg("PostLoadGame")` :813,
   `CommonLua\Savegame.lua`), seen nothing, and double-applied. **That is the
   2026-07-25 QA repair's failure mode reached by a second, previously
   unrecorded route** — the repair holds against both; recorded so nobody
   "simplifies" the hook back.

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

**Audit 2026-07-30 (reachability): R2, frequency claim corrected.** The
header's "the demolish path skips UpdateWorking(false) for buildings without a
demolished state" does NOT apply to shipped farms — no farm template or class
sets `use_demolished_state` false (Building default is true, Building.lua:210),
so a WORKING farm's salvage or destruction DOES clear the modifier via the
Destroyed working-edge (Building:Destroy :1473 → UpdateWorking(false) :1483 →
OnSetWorking(false) → Farm.lua:122). The leak needs the modifier applied in a
NOT-working window: the default crop plants at GameInit regardless of workers
(Farm.lua:84-96 → :557), so salvage-before-first-spin-up (the "misplaced
building, undo it" move) or an off-state SetCrop followed by salvage orphans
it permanently. Fix unchanged and still worth carrying; "every rebuild adds
another" overstated the common case. Full block in REACHABILITY_AUDIT.md.
`FarmBase:ApplyOxygenProductionMod` (`Farm.lua:561-571`) puts negative `air_consumption`
modifier on `parent_dome` keyed `farm_id`; no `FarmBase:Done`, `Building:Done`/`SetDome(false)`
never clear it, and demolish path skips `UpdateWorking(false)` for non-`use_demolished_state`
buildings (`Building.lua:1457-1483`, `Demolishable.lua:139`). Dome keeps phantom O2 forever.
**Fix:** wrap `FarmBase` delete path (post-hook `Done` via class or `OnMsg` on demolish) to
remove the dome modifier; one-shot LoadGame sweep for orphaned `farm_id` modifiers.

### F38 — Destroyed tunnels rejoin pathfinding after load (P2, high)  `[tested 2026-07-30 — PT-25 PASS IN FULL: Code/Fix_DestroyedTunnels.lua]`

**PT-25 PASS IN FULL — 2026-07-30, live, on a surface save.** All four
observations, in order:

| Step | Result |
|---|---|
| Rover uses the Universal Tunnel pair as the short route | **confirmed** (and it disproved the shipped description — see F84) |
| Tunnel destroyed → rover takes the long way | **confirmed** (in-session removal was already correct in vanilla) |
| **Save / quit / load → rover STILL takes the long way** | **confirmed — this is the leak the fix closes** |
| Rebuilt → rover uses the tunnel again | **confirmed — the fix does not lock a repaired tunnel out** |

The third row is the defect and the fourth is the over-reach guard; both had to
pass. Source predicted the rebuild would be safe (`Building:Rebuild` yields a
NEW object whose `GameInit` registers normally, `Building.lua:1655`) but that
prediction was verified rather than assumed.

**Reachability re-checked 2026-07-30 (tester question at the keyboard: "the
underground has no tunnel option — is this another phantom fix?"). Answer: NO,
F38 is reachable; PT-25's SETUP LINE was wrong.**
- **The underground genuinely has no tunnel.** `UniversalTunnel` is the only
  tunnel in a player-facing build category (`Infrastructure`); `Tunnel` and
  `TrackTunnel` are `build_category = "Hidden"`. Tunnels are a **surface**
  building. PT-25's "SAVE-B / underground access" setup was a
  mis-specification and has been corrected in the checklist.
- **The buildable tunnel IS in the defect's scope.** `UniversalTunnel`'s
  `object_class` is **`TrackTunnelBase`**
  (`Data/BuildingTemplate/UniversalTunnel.lua`), and
  `TrackTunnelBase.__parents = { "TunnelBase", "TrackConnectedObjBase" }`
  (`Lua/Buildings/TrackTunnel.lua:1-5`) with **no override** of `AddPFTunnel` or
  `TraverseTunnel`. The leaking sweep iterates exactly that class:
  `AllMapsForEach("map", "TunnelBase", Tunnel.AddPFTunnel)`. So a destroyed
  Universal Tunnel regains its pathfinding shortcut on every load.
- Not a mod artifact: all of this is shipped `Src`, byte-identical to the running
  build per the fpk parity proof (ENGINE_FACTS.md).

**~~❓ OPEN QUESTION~~ — ANSWERED BY PLAY 2026-07-30: rovers DO use Universal
Tunnels**, so the shipped description ("Rovers cannot use this type of tunnel")
is wrong. Filed as **F84**. It also confirms F38's reach: the tunnel a player can
actually build carries rover pathfinding, which is exactly what the leaking
`LoadGame` sweep re-registers. The prediction from the unit-class mask
(`pf.AddTunnel(…, -1)` = all units, vs `Dome_Entrance`'s `2`/`1`) held.
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

**Audit 2026-07-30 (reachability): R2 — two gates previously unrecorded
here.** (1) The DustSickness storybit family requires the **Dust in the Wind**
game rule (Data\StoryBit\DustSickness.lua:19-21) — same gate as F17. (2) The
"Biorobots breakthrough" is named **The Positronic Brain** in shipped data
(TechPreset.lua:336-344). Both are ordinary content (a selectable rule + a
random breakthrough); a Dust-in-the-Wind colony that gets the breakthrough
will hit it. Full block in REACHABILITY_AUDIT.md.
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

### F41 — Gene Forging tech has no effect (P2, high)  `[tested: Code/Fix_GeneForging.lua — PT-29 PASS 2026-07-29: live console read on a colony with neither tech researched went nil → 50 (Gene Forging alone, was nil = the defect) → 150 (both), confirming the additive sum]`
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

**Audit 2026-07-30 (reachability): R3 confirmed — but the recorded REASON was
wrong.** "None of its entries carries a tech requirement" is FALSE:
MoistureVaporator IS tech-locked behind MoistureFarming
(Data\TechPreset.lua:2038-2045) and appears twice in the one populated layout.
The latency holds on different grounds: the template sets
`require_prefab = true` (Data\BuildingTemplate\MoistureVaporator.lua:11) and
its resupply cargo item ships unlocked (Data\Cargo.lua:334-343 — no `locked`
flag, no sponsor lock, no verifier), so the tech lock is routed into exactly
the `require_prefab` branch the shipped code handles (add = false). The
defect branch still needs a tech-locked entry with a MISSING or LOCKED
resupply item, which no shipped data provides. Also: the preset has nine
entries, seven unique templates (MoistureVaporator and life_support_grid
appear twice). STATUS.md's matching one-liner corrected the same day. Full
block in REACHABILITY_AUDIT.md.
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

### F46 — Trains dump cargo at stations with the resource disabled (P2, high)  `[tested: Code/Fix_TrainCargoDumping.lua — PT-23 PASS 2026-07-28 both halves on the live 5-station network; archived]`
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
*PT-23 observation (2026-07-28):* with the resource forbidden at EVERY station and no
drone coverage, an isolated station's forbidden stock stays put indefinitely — loading
only targets accepting destinations, so the stock has no train exit; drones are the only
mover. Expected statics, vanilla-consistent, not the fix; trains verifiably dump their
carried load (the designed branch) instead of stranding.

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

### F49 — Train minors bundle (P3, med)  `[fixed*: Code/Fix_TrainMinors.lua — item (d) ONLY since 2026-08-01; (d) TESTED (PT-46); (c) wontfix, guard REMOVED 2026-07-30 — designed behaviour; (a) R4 NON-FIX, guard STRIPPED 2026-08-01; (b)(e) screened and deliberately not fixed, see below]`

**2026-08-01 (owner direction, bug-list audit follow-through): the (a) palette
guard is STRIPPED from the module.** Grounds: the reachability audit's R4 was
already high-confidence and adjudicated (no player-reachable entry into
`place_track`; injection-only repro; self-corrects on colour-scheme change),
the audit's NON-FIX tier (BUG_LIST_AUDIT.md §2.4) formalized it, and the owner
directed removal so no adjudicated non-fix leaves live code behind. Removed in
the same change: the wrapper on `TrackGridElement:GameInit`, its three Require
entries, and the probe's palette half (TestKit `50_Probes_Wave5.lua` — probe
retained, cap half only; probe count stays 78; its PASS text changed, so the
next fingerprint diff will show that one line). Module title now "Train cap
follows track length".

**✅ The owed A/B code-gate leg RAN CLEAR — 2026-08-01, unattended, default
config** (log `Mars.exe-20260801-14.15.08-6a22b86d`, read this session; every
number below is quoted from it, not predicted). `[SMRAUTO] armed (flag file
Code/96_AutoRunFlag.lua)` → `BEGIN` → `END` → `done`, no TIMEOUT and no ERROR
stage.
* **Counts unchanged, as predicted:** `fix pack present: 68/74 fixes active` —
  68 `: applied` lines and exactly 6 `inactive (opt-in module, off by default)`,
  zero error / disabled / FAILED lines from `[CommunityFixPack]`.
* **Tally exactly the recorded default-config prediction: `---- 63 PASS, 0
  FAIL, 15 SKIP, 0 ERROR ----`**, over 78 verdict lines (probe count unchanged).
* **The TrainMinors probe PASSes on its new cap-only text:**
  `PASS TrainMinors [behavior] train cap recomputed 4->1, 40->2, 0->0`.
* **Fingerprint diff vs the last comparable default-config leg
  (`Mars.exe-20260731-18.44.38`, also 68/74 → 63/0/15/0) is THREE lines, and
  only ONE is a real change** — TrainMinors losing its palette clause, which is
  the one difference this strip was predicted to produce. The other two are the
  known RNG lines: `TouristApplicants` (160/312 → 159/308) and
  `FounderTraitNotification` (random trait pick Sexy → Whiner).
* **Noise is the documented set only:** 60 `Flight.lua objects_to_mark` /
  `objects_to_unmark` lines (documented ~50-60), three GameInit nil-calls
  (`CreateResourceRequests`, `ApplyToGrids`, `BuildWaypointChains`), 2
  `ResManager LawOfficeDoor` lines, the `no debug.getinfo` notice, and the
  `MeteorFrequency: WATCHDOG … probe-stall` line — that last one checked
  against the 2026-07-31 leg, which carries it identically, so it is prior
  known behaviour and not something this change introduced.
* **PROBE SWEEP:** armed `97_SaveHookProbe.lua` only (declared: chain prompt 2's
  instrument; it logged its load line and nothing else, since the leg starts a
  new game and never saves). `99_OrphanEnvProbe.lua` was deleted before the leg
  and no `SMRTEST-ORPHANENV` line appears anywhere in the log.

**Nothing is owed on the harness side for the F49(a) strip.** The leg measured
the default configuration; the all-ON prediction (68/0/10/0) was not exercised
and is not owed — the account was in default state and the reading, per the
standing rule, is the truth.

**Audit 2026-07-30 (reachability): (a) settled R4; (c)(d) live R2; module
kept.** The (a) trigger list "map setup, cheats, the instant-build rule"
contains ZERO player-reachable members: there is no `InstantTracks` const
(the Instant* family is Cables/Passages/Pipes only, __const.lua:1043-1056);
all four shipped entries into track mode inherit the track dialog's
`grid_elements_require_construction = true` default (TrackConstruction.lua:8);
`PlaceTrackLine`'s only caller is the construction-mode dispatch
(GridConstruction.lua:607/:1852); Cheats.lua has no track cheat; and with the
flag true the instant `place_track` closure cannot fire (Tracks.lua:234,
:431-442). The PT-46 injection incident corroborates: the state was producible
only by injecting a mode flag with no player-facing control. The (a) wrapper
is a cheap additive no-op for correctly-painted elements — keep or strip on
next touch, no §1.5 liability. Full proof in REACHABILITY_AUDIT.md (lead-pass
block).
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

**(d) PLAYTESTED PASS 2026-07-30 (PT-46 tail).** Live 305-sol colony, 7 tracks,
run on a read-only counter printing actual vs shipped-formula expected per
track. Track 3 went `els=43 cap=2` → `els=13 cap=1` across a partial salvage —
exactly the surviving-track case this fix exists for. All lines `OK` across four
runs; formula spot-checks 43→2, 113→4, 74→2, 13→1, 25→1. The salvage was
mid-track so it also SPLIT, producing a new track at `els=25 cap=1` correct on
its own — independent confirmation of the 2026-07-25 QA correction that the
split-off track was never the defect. Re-verified after a reload: post-load
baseline correct, and salvaging a freshly loaded track recomputed correctly.
*Explicitly NOT proven:* the `PostLoadGame` sweep REPAIRING an already-stale
cap — a healthy save cannot show that, since the in-session recompute has
already corrected it. The reload only showed the sweep is idempotent. Proving
the repair needs a save written with the fix vetoed
(`SMRFixPack_Disabled["TrainMinors"]`); queued as a TestKit probe.

**(a) NOT PLAYTESTED — PARKED 2026-07-30, and now a REACHABILITY question.**
The attempt is on record because it cost something. Reaching the instant
`place_track` path required injecting
`GetInGameInterface():SetMode("track_grid", {grid_elements_require_construction = false})`
— there is **no player-facing control that does this**. It misbehaved, and
cancelling left an orphan `TrackBase` with invisible elements blocking grid
hexes on the live colony (cleared by reload). That broke the project's own
no-live-UI-internals rule (F76 lesson). **The debris is an artifact of an
unreachable entry path, not a defect — it is not filed as one.** The question
that superseded the test — is `place_track` reachable at all? — is now
**ANSWERED: it is not. (a) is R4.** Settled by the reachability audit's
lead-pass block (`docs/reports/REACHABILITY_AUDIT.md`): there is **no `InstantTracks`
const** (the Instant* family is Cables/Passages/Pipes only,
`__const.lua:1043-1056`), all four shipped entries into track mode pass no
override and the track dialog defaults `grid_elements_require_construction`
**true** (`TrackConstruction.lua:8`), `PlaceTrackLine` has exactly one caller,
the build menu hardcodes `require_construction = true` for tracks
(`BuildMenu.lua:1938`), and `Cheats.lua` contains **zero** track references.
So "map setup, cheats, the instant-build rule" has **zero player-reachable
members**.
~~**Kept anyway, deliberately:**~~ **SUPERSEDED — the (a) guard was STRIPPED
2026-08-01 (owner direction); the paragraph below is the record of the position
it replaced.** The (a) hook was a cheap additive post-wrapper
that is a no-op for correctly-painted elements, and it rode a module retained
on (d)'s live R2. Strip it on the next touch of this file if you want the
stricter line. Note the drafted FIX_POLICY §4 says "R4 does not ship", which
would mandate stripping it — that contradiction is flagged for the user and
must be resolved before the amendment lands. **Both halves of that sentence
have since happened, in that order:** the guard came out (A/B code-gate leg ran
clear, `68/74` → `63/0/15/0`), and **the amendment landed 2026-08-01 with the
contradiction already gone** — FIX_POLICY §4 now carries "R4 does not ship"
against no shipped R4 code. It also self-corrects on any
colour-scheme change (`ColonyColorScheme.lua:120-121` repaints every
`TrackGridElement`), so the live impact was cosmetic and transient anyway.
*The test itself is sound if a safe route is ever found* — the palette control
passed on the live save: `tracks=4283130509/4283130509`,
`pipes=760202697884/966355804813`, `distinguishable=true`.

**(c) CLOSED `wontfix` 2026-07-30 (user decision) — GUARD REMOVED. It was
"fixing" DESIGNED BEHAVIOUR.** Started as a hunt for the missing play coverage
(no PT ever exercised the pre-guard) and ended by falsifying the premise. The
tester established at the keyboard what no amount of source reading would have
shown:
* Salvage mode targets **objects, never hexes** — a bare hex cannot be clicked
  and is not drawn.
* The cursor **always names what it will remove** (`Salvage Track`,
  `Salvage Train Station`, …), and a bare red `Salvage` means "no action
  permitted here". So a mis-resolved salvage target could never be a silent
  trap — the player is told before committing.
* The transition from `Salvage Train Station` to `Salvage Track` is
  **seamless, exact to the millimetre, with no third state in between**
  (two screenshots a few pixels apart, each correctly named).
* **A player cannot salvage a station's own track without salvaging the
  station.** No exposed control distinguishes them.

Station connector elements are real and station-owned — created with
`station = self` at the station's `Trackconnector` spots
(`TrainTransport.lua:132-139`) — so the guard was not inert by luck. **The
propagation to `self.station` that this item called a defect is exactly what
makes that boundary continuous.** Had the guard engaged it would have carved a
DEAD BAND into it: a strip reading red `Salvage` where nothing is targetable.
Best case it changed nothing observable; worst case it degraded the interface.
There was no wrong outcome for it to prevent.

Removed from `Code/Fix_TrainMinors.lua`: the `SelectionPropagate` pre-guard,
its apply-time self-check, and the "connector-hex salvage click neutralized"
clause in the Register title. (a) and (d) untouched.

**Method note — this is a DIFFERENT failure mode from F24, and a worse one.**
F24 was a real defect nobody could reach. This was a **non-defect**: the
shipped behaviour was intentional and the patch fought the design. The
reachability audit (`REACHABILITY_AUDIT.md`, `3398031`) rated (c) "live R2" —
but it never enumerated (c) at all; the tier was asserted in passing while
justifying the *module's* retention on (a)'s behalf. Its R1-R4 vocabulary also
has no way to express "reachable, but intended", because every tier
presupposes the shipped behaviour is wrong. Both gaps were put back to the
audit and are **ANSWERED** in `docs/reports/REACHABILITY_AUDIT.md` ("Challenge review
2026-07-30"): new tier **`I` — Intentional** was added with (c) reassigned to
it, every lettered sub-item is now its own audit subject by rule, and the
revised FIX_POLICY §4 ~~draft~~ (**APPLIED 2026-08-01**) demands a positive
intent statement backed by a hard tell — not merely a reachability tier.

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

**⭐ F86 TIER-2 REWRITE, 2026-08-01 — `Colonist:Arrive` is no longer replaced, and the
half-(a) design pass §6.2 flagged as OWED is RUN AND ANSWERED.** `Arrive` yields directly
(`Sleep(self:TimeToAnimEnd())` in the disembark destructor, `:1285`): route (a),
REPLACE-class. It also cannot be repaired from the inside — the destination is read into a
LOCAL at `:1260` before anything else runs, and the drop position is captured into an upvalue
at `:1281`, so no seam within the body can change either. The two halves therefore leave the
body in opposite directions:

- **(b) moves AHEAD of it — layer 2.** `Colonist:Idle` is the *only* issuer of `"Arrive"`
  in the shipped source (`:1791-1793`; `RocketBase.lua:2015`'s state enumeration confirms
  it), so a PRE-wrapper there keyed on `self.arriving` corrects
  `emigration_dome`/`emigration_elevator` while they are still fields, and vanilla's own
  `if not dome` branch (`:1293-1294`) delivers the "Confused Colonists" outcome. All work
  before the call, `return orig_idle(...)` with nothing after — the same shape
  `Fix_ShelterReflex` already uses on this method, which §5.3 classified *already
  compliant*. Accepted residual: one inert captured frame. The re-check is judged from the
  ROCKET's position, which is the reference point the original assignment used
  (`RocketBase.lua:1981`, `:2029`). Every function it calls reports `clear` under
  `tools/blocking_analysis.py`.
- **(a) moves BEHIND it — layer-3 class seam.** The design pass's answer is that the fix
  never needed to change `pos`; it needs the colonist to *end up* somewhere walkable, and
  `Colonist:OnArrival` is a shipped, arrival-specific, **verified synchronous** seam that
  runs immediately after the placement — via `:1299` on the notification path, and inside
  `SetCommand`'s destructor pass (`CommandObject.lua:225-235`) *before* `TransportByFoot`
  starts on the walking path. Body is an assert, three field writes,
  `UpdateHomelessLabels`/`UpdateEmploymentLabels`/`ChangeComfort` and `GameTime()`
  (`:1302-1311`); it and all three callees report `clear`. Our frame there exists only
  during synchronous execution and can never be captured.

**Not wrapped: `ChooseDome` itself**, although that is where the bad fallback is born. It has
eight shipped call sites (`DroneFactory.lua:224`, `RocketBase.lua:1985/:2068/:2105`,
`CargoTransporterNew.lua:907/:951/:975`, `Colonist.lua:1149`) and only the arrival ones are
F53's subject; suppressing an unreachable fallback globally would change android spawning and
the "Abandoned" path, which has its own oldest-failed-dome fallback and its own
walking-distance test (`:1149-1163`). No evidence stands behind either change (FIX_POLICY §4),
and §5.3 requires the narrowest key that separates the call sites — here, `self.arriving`.

**Coverage change, disclosed:** the (a) snap is gated on the harm being present (no holder,
valid position, position not passable) rather than on the call site, so it now also repairs
`Colonist:ReturnFromExpedition` (`:4168-4197`), which has the identical raw `SetPos(pos)`
disembark and was never covered by the old replacement. It cannot reach the spawn paths that
call `OnArrival` from `GameInit` (`:215-217`): those colonists either have a holder
(`DroneFactory.lua:230`) or have no position yet when it fires (`RocketBase.lua:2106-2112`
places them afterwards, already via `GetRandomPassableAroundOnMap`).
**Disposition (FIX_POLICY §3a per-site gate): REPAIRED IN-PACK — (a) layer 3, no residue;
(b) layer 2, accepted inert residual (a captured frame with nothing after the call), which
is tier 2 of the three-tier ethos and needs nothing from D13.**

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
attaches; ~~override approach-failure cache to store `GameTime()`~~ **superseded by the
F86 Tier-2 shape below** so `CleanUnreachables` retires entries.

**⭐ F86 TIER-2 REWRITE, 2026-08-01 — the repair moved from the writer to the reader.**
The shipped fix replaced `Drone:ApproachWrapper`, which blocks in `DroneApproach` and had
our code after the call — F86 exposure route (a), and a REPLACE-class one (an orphaned copy
means vanilla's own approach handling is gone too). The defect is only the VALUE, and its
reader `Drone:CleanUnreachables` is **verified synchronous** (`Drone.lua:879-896` — a
`pairs` walk plus `GameTime()`; `tools/blocking_analysis.py` reports it `clear`). So the
module now PRE-wraps `CleanUnreachables` and normalises the poison in place:
`ts > GameTime()` → `ts - max_int`, which recovers the exact original failure time because
`max_int` is the same constant vanilla added (`CommonLua\Core\lib.lua:69`). Vanilla's
`ApproachWrapper` is untouched and keeps writing its own value; vanilla's 5-sol expiry then
does what it was written to do. The normalisation is one-way, so stamps written by the
pre-2026-08-01 shipped fix (plain `GameTime()`) are left alone and existing saves migrate
themselves on the next call. **Disposition (FIX_POLICY §3a per-site gate): REPAIRED IN-PACK
— layer 3, no residue, nothing owed to D13.**

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
*Origin note:* the player report behind this entry is recorded in `docs/archive/RESEARCH.md` as
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
**⚠ §4 DECISION OWED ON THIS ITEM (2026-08-01).** (a) is **R3 latent-by-data
implemented as a §1.5 replacement** — the exact combination the §4 amendment,
applied today, now makes conditional on an explicit owner decision ("R3 ships
only as a §1.1–§1.4 patch"). It is paired with **F29** in that bucket and the
two are routed together to chain prompt 7. Note for whoever prepares that
package: (a)'s defect is a mid-function key write, so a §1.1–§1.4 route is not
obviously available — that is part of what the decision must weigh, not a
reason to skip the ask. (b) is unaffected (additive `OnMsg`, §1.2).

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

### F62 — Services reach exactly 1 passage hop, never trains (P2, high mechanism)  `[wontfix — carried-forward design, verified identical to the original game (provenance: original's Lua read 2026-07-26 at cited lines; that source is NOT on this machine — original ships Lua.hpk, no extractor in tools/ — so the claim is currently not re-derivable here; F86 adjudication round 2, item 9.2)]`
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

### F63 — Universities invisible to emigration (P2, high)  `[wontfix — carried-forward design, verified identical to the original game (provenance: original's Lua read 2026-07-26 at the file:lines cited in the entry; that source is NOT on this machine — original ships Lua.hpk, no extractor in tools/ — so the claim is currently not re-derivable here; F86 adjudication round 2, item 9.2)]`
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

### D01 — Rockets don't auto-refuel / auto-export rare metals — INTENTIONAL REDESIGN (verdict)  `[opt-in fix — fuel half shipped: Code/Opt_ClassicRockets.lua (id ClassicRockets, off by default); the standing Rare Metals export half is deliberately unwritten; PT-55 closed in full 2026-07-30; the parked-rocket activation limitation is documented, not owed. Heading tag ADDED 2026-08-01 — this entry had none, so its status could not be cross-checked against the index row]`

**PT-55 (2026-07-30) — live-toggle result; PT-55 CLOSED IN FULL the same day.** The audit's A2
repair is confirmed: the file-scope install works, and a rocket that LANDS after
a first mid-session enable starts filling immediately (no relaunch). But a
rocket **already parked** on the pad when the toggle flips does NOT begin
refuelling, and — unlike Opt_MultipleSuns' panel — **does not heal on a
save/reload either**. Cause, confirmed in source: the wrap is on
`GetFuelResourceRequest`, which is only consulted when
`CargoTransporterNew:UpdateCargoResourceRequests` runs
(`CargoTransporterNew.lua:1249-1265`); for an already-parked rocket nothing
re-triggers that, and the landing path is what does. The hook answers correctly
— nobody asks it. **DECIDED 2026-07-30 (user): accepted as a documented
limitation.** A first mid-session enable engages for rockets that land after
the flip; an already-parked rocket picks the behavior up on its next landing.
No `on_activate` demand refresh is built. **PARKED 2026-07-31 (owner) —
`docs/FUTURE_IDEAS.md` entry 2. `[FAQ]`** Owner's words: *"its not a high
priority, the mod functions flawlessly, besides a already parked rocket when
activated… Touching it just invites a regression."* Documented instead of built:
a player-facing note now sits in `MOD_DESCRIPTION.md` under the Classic rocket
behavior module. **This is not owed work and must not be reported as
outstanding.** The enhancement stays on record for post-launch: an `on_activate`
that re-runs `UpdateCargoResourceRequests` on parked destination-less player
rockets — the D05 reconciler's intended use of `on_activate` (state nudges that
are not a call path, FIX_POLICY §5) — would make the enable immediate. Building
it would be a normal mechanical change (A/B re-run + live re-verify), not a
reopening of this decision. **PT-55 closed 2026-07-30:** step 3 (ListFixes agreement + log
sweep) PASSed in the live sitting — statuses tracked a full OFF/ON/OFF Mod
Options cycle at every step, log clean per PT-22. Evidence archived with the
PT-55 section in PLAYTEST_ARCHIVE.md.

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

### D02 — Dismissing a "Building Not Working" warning only silences it ~4 game hours — BY DESIGN, feels like a bug  `[tested 2026-07-30: Code/Opt_AcknowledgedWarnings.lua (opt-in, off by default); probe PASS in the opt-in leg; PT-48 PASS in full — all five steps on console counters, archived]`
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
**PT-48 PASS IN FULL → `tested` (2026-07-30).** Live 297-sol colony, module
enabled mid-session with no relaunch. Every result is a console counter reading,
not an eyeball call; full evidence in PLAYTEST_ARCHIVE.md. Headlines:
* **Positive control run FIRST** (module OFF): dismissal armed
  `suppress_until = now + 120,000` exactly, and the notification RETURNED after
  the window — proving the no-power fixture generates re-add attempts, so the
  "stays quiet" steps could not false-PASS (the PT-29/PT-11 lesson applied).
* **Acked stay quiet:** `acked=true shouldshow=true in_notif=false` held for
  505,850 game-ms ≈ **16.9 game hours = 4.2 vanilla windows**, with
  `suppress_until=nil` throughout — the shipped whole-id window is skipped, so
  only the per-object filter accounts for the silence. `shouldshow=true` is the
  load-bearing half: the building actively qualified and was still excluded.
* **New breakage warns:** a fresh Triboelectric Scrubber warned while three
  acknowledged buildings sat broken; the notification listed only the scrubber.
  Placed while PAUSED, so it provably landed inside vanilla's silent window.
* **Recovery re-arms:** repowering the original three cleared all three stamps
  (`total_acked` 3 → 1) and re-breaking them re-warned all three. The one
  never-recovered building stayed filtered through two grid rebuilds and three
  neighbour break→recover→break cycles.
* **Save/reload:** the `SMRFixPack_ack_notworking` member persists — flagged
  pre-run as the likeliest failure, and it held.
* **Blast radius bounded by source:** exactly TWO presets in the game are
  `Suppressable` (`InsufficientResources`, `NotWorkingBuildings` —
  `Data/NotificationPreset.lua:546/:646`), so `InsufficientResources` is the only
  id where this module could differ from vanilla. Forced via
  `const.MinDaysFoodSupplyBeforeNotification`: it armed normally on two
  dismissals, self-cleared on expiry, and re-nagged — untouched.
* **Vanilla curiosity, unexplained, NOT a D02 issue:** `InsufficientResources`'
  suppression resolved on **RealTime**, while PT-38 measured
  `NotWorkingBuildings` on **GameTime** — despite both presets leaving
  `GameTime` at its default `true` (`NotificationPreset.lua:65-66/:126-128`).
  D02 never calls `GetTime()`, so nothing here touches this PASS, but if the
  notification INSTANCE rather than the preset supplies `GameTime`, PT-38's
  recorded 4-game-hour fact may need scoping. Worth a game-free look.
* **No first-enable defect here** (unlike D01/D03/D04 pre-audit-1.3): the three
  wrappers replace plain notification GLOBALS, not class methods, so runtime
  flattening never applies, and `OnMsg.ApplyModOptions` re-runs `apply()`
  (`00_Core.lua:129`) on a first mid-session enable.

### D03 — No way to block dome move-ins short of a full quarantine  `[tested 2026-07-28: Code/Opt_ResidencyControl.lua (opt-in, off by default); probe PASS in the opt-in leg; PT-49 PASS in full (archived) — arrivals/tourists proven against an adversarial pad-beside-the-closed-dome setup, quarantine independence, MicroG row (kept on asteroid habitats by user decision), uninstall shape live + reload; PT-55 PASS 2026-07-30 — mid-session first enable clean, "no issues at all"]`
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

### D04 — Multiple Artificial Suns — absorbs F39  `[tested 2026-07-27 (PT-50 PASS in full, archive): Code/Opt_MultipleSuns.lua (opt-in, off by default); night signature matched the banked baseline both sectors, sunless panels 0 at night, reload clean, limit off/on live via the D05 Mod Options toggle; PT-55 PASS 2026-07-30 — see the binding-timing note below]`

**PT-55 (2026-07-30) — binding timing, expected and self-healing.** On a first
mid-session enable, a panel built BEFORE the flip does NOT start tracking sun #2;
a panel built AFTER it binds immediately; a save/reload makes the pre-existing
panel snap to the sun. By construction: the binding half wraps
`SolarPanelBase:GameInit`, so a panel that already ran GameInit cannot be
retro-bound, and a reload re-runs GameInit (plus this module's own LoadGame
sweep). Not a defect — but worth saying in player-facing text, since "enable the
module and my existing panels ignore the second sun until I reload" reads like
one. Nothing owed in code.

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

**◑ PARTIAL RESULT 2026-08-01 — the FAMILY is witnessed live on Relaunched; the
exact "trains go to void" report is still not located.** Owner's logged-in
Paradox subforum browse (audit §7.1 item (a)). Honest grade: this corroborates
the counter-corruption mechanism, it does **not** retrieve the phrase this entry
quotes.

**Kopernikus79** (member since Feb 24 2011), **Jan 30 2026**:
> "I built my first 2 train stations with 2 trains. Everything worked perfectly.
> Some time later I crashed of the stations *[sic — reads as: demolished one of
> the stations]* and built another one somewhere else, connecting it to one of my
> first stations. After that, it told me that there are no trains, but looking
> into the station info, it counted the 2 from my previous connection. In the end
> I needed to built another one, to get the new line working, still showing that
> I have 1/2 trains working and in an additional line that I also owe 2 other
> trains. Looks like a bug?"

**What it does and does not confirm.** It matches this entry's mechanism where it
counts — a station is removed, and afterwards the colony's train bookkeeping is
wrong in a way that persists and forces the player to build replacements
(`city.available_prefabs["Train"]` never refunded, `City.lua:433-440`;
`Train:OnDemolish` skipped by the bare `DoneObject`, `Station.lua:163-171`). It
does **not** describe trains visibly vanishing, and the reporter's "crashed of
the stations" is ambiguous between demolition and a game crash. **Treat it as
family-level corroboration on the live build, not as the report this entry
cites.**

**Volume note (owner, same browse): there are MANY similar train reports, but
most are older than the forum's five-month necro threshold** — i.e. the train
cluster is widely reported and largely *stale*, which is itself a fact worth
having. It means (a) the family is not obscure, and (b) a future search should
not read the absence of *recent* posts as the defects being fixed.

**⚠️ Still open, and deliberately not claimed:** the verbatim "trains go to void"
report. This entry has quoted that phrase since it was written; one logged-in
browse did not find it. That is now *"searched with the Cloudflare block removed
and not located"* rather than *"unretrieved"* — enough to stop treating the
phrase as a citation. **If it is never found, the quotation marks should come off
it.** No code consequence either way — the fix is shipped and the mechanism is
Src-verified independently of any witness.

### F65 — Station attached to a train tunnel never bridges the power grid (P2, med)  `[tested: Code/Fix_TrackTunnelPowerBridge.lua — PT-40 PASS 2026-07-28, full procedure incl. salvage split, long-track control, reload]`
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
**PT-40 PASS — 2026-07-28, live colony.** Deliberate two-grid setup (grid 1
powered, grid 2 with NO active source), normal station at the tunnel, both
geometries: snugged directly against the entrance AND a couple of track
pieces between. Merge verified functionally — a fresh consumer (MDS Laser,
10 power) attached to the sourceless far grid ran off the near grid's
supply through the tunnel. Salvaging the short track split the grids
cleanly (far consumer went dark, nothing self-supplied stranded); the
long-track control (the already-working path) behaved unchanged; save →
quit → reload kept the merge. Log swept clean the same session:
`TrackTunnelPowerBridge: applied` at load and ZERO errors incl. through the
reload's PostLoadGame pass.

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

### F67 — Auto-lander launches empty and ping-pongs (P1, high)  `[tested: Code/Fix_LanderEmptyLaunch.lua — PT-16 PASS 2026-07-28]`
**PT-16 PASS — 2026-07-28, live colony, Galileo #1, automated mode with a
deliberately unsatisfiable GET rule (Metals get-when-above 100, Kayra AL10
stock 0; all else Ignore).** The repaired leaf-class CargoReady logger
captured its first live verdicts. Asteroid side — the spot where vanilla's
only brake was the 1-hour sleep: the gate held `IsCargoReady -> false`
through **~20 hourly empty recomputes (a full sol's dwell)**, then the
designed `AutoDepartTimerSols` forced exit flipped it true and the lander
flew home. Cadence: one round trip per sol-plus, no hourly fuel-burning
ping-pong. Mars-side observation (new engine fact, recorded): the quick
fueled departure with no SEND rules is DESIGNED — `CheckAutoDepart`
(`UniversalRocket.lua:1777-1781`) consults only the CURRENT side's rule set
(`import_below` on Mars, `export_above` on the target), so an empty
side-set means "nothing will ever load here — fly out and collect"; the fix
correctly defers to that (its gate only closes inside the wait window).
`UniversalRocketBase:IsCargoReady` (`UniversalRocket.lua:455-472`): `CheckAutoDepart()`
("wait for cargo") only yields the NON-blocking `"waiting_cargo"` issue
(`GetLaunchIssue` :883-885 returns no blocker); with an empty auto request
(nothing above export / below import threshold) every entry is 0 → status "ready" →
departs empty. Only mitigation: 1-hour sleep on asteroids (:227-229), none on Mars.
Endless empty round trips ~70 fuel each. **Fix:** wrap `IsCargoReady`: in auto mode with
CheckAutoDepart true and no non-fuel payload requested, return false (1-sol timer still
exits cleanly).
**⚠️ A CURRENT COMMUNITY CLAIM CONTRADICTS THIS ENTRY — recorded, not hidden
(2026-08-01).** In a Reddit thread hours old ([S38], `BUG_LIST_AUDIT.md`
§10.6c), a commenter states: *"**Landers and the elevator work much more
smoothly now. The old bugs don't happen because they've completely changed how
both work to be more straightforward.**"* **It moves nothing** — F67/F68/F70/F71
are Src-verified against 1.0.7.396349 and live-tested (PT-16/17/31/32), and the
standing rule is *"fixed in Relaunched" only from current Src*. It is recorded
because the **same threads** contain a player describing this exact defect
verbatim (*"my rocket would just fly back and forth until it was out of fuel and
got stuck on the asteroid"* — [S37]), which is the selection-bias caveat in
miniature: enthusiast "it's fixed" testimony is data about the speaker.

**⭐ PLAYER WITNESSES 2026-08-01** (Reddit thread, `BUG_LIST_AUDIT.md` §10.5,
[S36] — **hotfix-1.0.3-era, ~Dec 2025, NOT our pinned build; this is evidence
of harm, not of current presence**). Next_Interaction4335, twice, describing
this entry's exact headline: *"When you request to asteroid the Lander loads
with nothing and takes off leaving it to arrive with nothing on asteroid!!!"*
and *"When I send Landers they arrive at the astroid with nothing in making
them stranded."* The **stranding** consequence is worse than this entry states —
an empty arrival is not just wasted fuel, it can leave the asteroid operation
dead. Cross-ref F68: the same thread's players describe both halves together,
which is what the two defects do in combination.

### F68 — Hourly auto-request ratchet unloads the lander's own cargo (P1, high)  `[tested: Code/Fix_LanderCargoRatchet.lua — PT-17 complete 2026-07-28, incl. attended capacity-edge re-run post-repair]`
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
aboard) which alone prevents the unload flip. **REPAIRED same day (2026-07-28, game-free leg):**
the (1) aboard-into-ground addition DELETED; the (2) explicit floor now carries
the whole F68 anti-churn fix. The live TAP2 arithmetic sharpened the root cause
first: the observed requests matched `ground + 2×aboard − threshold` EXACTLY
(52/72/98 at aboard 12/32/58, final ground 184−100=84, zero mining assumptions),
proving **`GetTotalCargoAvailable` already counts the landed rocket's own hold**
— the addition double-counted every unit aboard. Post-repair the shipped
`available − threshold` is already aboard + ground surplus on the live path
(equilibrium lands ground exactly at the threshold), and the floor guarantees no
unload flip on any path where the hold is not counted. **A/B re-verified
2026-07-28: baseline 1/57/14/0, all-five-toggles 62/0/10/0 (70/70 applied, zero
pack errors); the LanderCargoRatchet probe passes through the floor path
(`request 300000 >= 300000 aboard`).** PT-17 stays un-archived until an attended
re-run of the capacity-edge leg (two exports + replenishing stock) confirms the
threshold holds live.
**⭐ PLAYER WITNESSES 2026-08-01** (Reddit thread, `BUG_LIST_AUDIT.md` §10.5,
[S36] — **hotfix-1.0.3-era, ~Dec 2025, NOT our pinned build**). Two independent
players describe this entry's mechanism in plain language, including the detail
that identifies it as the ratchet rather than ordinary drone churn:
> j1dopeman: *"drones will constantly unload resources particularly fuel even
> though there are multiple very close depots with tons of fuel. I'm not
> convinced they're taking it to other rockets, **I think they're just doing a
> circular unload/load**. Even if it says it is full when you click takeoff the
> number will drop."*
> turnipofficer: *"My rockets would constantly load and unload requested
> resources on mars, so I would have to manually launch them with typically some
> resources missing."*

*"Circular unload/load"* and *"it says full, then the number drops"* are the
request-shrinks-below-what-is-aboard signature this entry derived from source —
a player reconstructing the defect from the outside and landing on the same
shape. Also note the **workaround they invented** (*"you have to overfill with
that expectation. If you require 35 then make it 40"*), which is what players do
instead of reporting. Related in the same thread and belonging to **F70/F71**
rather than here: *"they load up on useless crap and never take enough of the
exotic minerals."*
**RE-RUN CONFIRMED — 2026-07-28, attended, live colony (Sphinx #2, fresh
relaunch with the repair loaded, repaired TestKit AutoCargo logger doing the
capture — no console tap needed):** Concrete above 0 (ground 210) + Rare
Metals above 140 (ground 222), extractors actively replenishing mid-load. The
request TRACKED instead of ratcheting: PreciousMetals req 90000→91000→92000
(creeping only by what the miners added; aboard 10000→89000 underneath),
Concrete req 8000→7000 settling equal to aboard — `req` never below `have`
anywhere, no unload flip, load completed and departed on schedule. Ground
after departure read **146 with miners still running = settled AT the 140
threshold and re-accumulating** (the old over-draw drained 60 BELOW). The
observed numbers match `aboard + current surplus above threshold` exactly —
the repaired single-floor implementation verified end-to-end. **F68 CLOSED
`tested`; PT-17 archived.**

### F69 — Manual landing dumps the return fuel (P1, high)  `[tested: Code/Fix_LanderReturnFuel.lua — PT-16 PASS 2026-07-28]`
`CmdLand` (`UniversalRocket.lua:414`) clears `arrival_loc` in manual mode →
`GetFuelResourceRequest` (:1639-1642) returns 0 → `CmdUnload` (:486-494) posts the
reserved return fuel (asteroid policy keeps half, `FlightPolicyDef.lua:208-211`,
`ConsumeFuel` :1664-1673) as EXCESS → drones unload it. No drones/hub on the asteroid →
stranded forever ("no fuel, no drones, can't send another lander"). **Fix:** override
`GetFuelResourceRequest`: lander type with no destination departing an asteroid keeps
`FuelResourceAmount` requested.
**PT-16 PASS — 2026-07-28, live colony: Galileo #1, MANUAL mode, no
destination at any point, landed on bare Kayra AL10 (no drones, no hub).**
Post-unload panel: Destination None, general fuel request 0/0, **"Return
trip fuel 15/15" held in reserve, nothing offered as excess** — then
launched home on that reserve and landed on Mars. The vanilla stranding
(fuel posted as excess on the drone-less rock) is gone. Method note: a
FIRST attempt via automated-mode landing was correctly discarded as
non-discriminating — auto mode retains `arrival_loc`, so vanilla keeps fuel
there too; only the manual-mode landing exercises the bug path. Adjacent
vanilla hazard recorded during the earlier attempt: the `RoughTouchDown`
storybit (RocketUnloaded trigger, asteroid environment) can malfunction a
lander into a 25-Metals repair on a rock with no metals and no drones — a
by-design permanent stranding untouched by `CleanAndFix`; verified console
recovery: `SelectedObj.maintenance_request:SetAmount(0)` (the same
`SetAmount` the shipped repair path uses, `UniversalRocket.lua:600/:614`).

### F70 — Edit Payload silently refills from the policy template (P2, med-high)  `[tested: Code/Fix_PayloadTemplateRefill.lua — PT-31 PASS 2026-07-28; the legacy LanderRocketCargoRequest copy is unreachable in Relaunched, see below]`
**PT-31 PASS — 2026-07-28, live colony: brand-new lander (Galileo #1),
brand-new asteroid destination (Kayra AL10), manual mode.** The fresh lander
showed the FULL policy prefill on first Edit Payload (20 Metals / 5 Polymers
/ 5 MachineParts / 5 Electronics / 5 Drones + 3 extractor prefabs — the
not-over-broad half). Metals set to 0 and confirmed: immediate re-open read
Metals 0 with everything else exactly as configured (26,000 KG); after the
full round trip (launch, land on the asteroid, unload) Edit Payload STILL
showed no Metals and no template resurrection. Both faces of the bug gone.
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

### F72 — "No available Asteroid Landers" with a lander on the pad (P2, med)  `[tested: Code/Fix_AsteroidLanderAvailable.lua — PT-33 PASS 2026-07-28, all three cases incl. the not-over-broad negatives]`
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
**PT-33 PASS — 2026-07-28, live colony, Sphinx #2 (the spare lander deleted
for isolation off a quicksave).** Case A (stalled unload: cargo aboard, no
drones, "No destination set"): VISIT ASTEROID opened the picker with the
lander listed "Ready" — the vanilla refusal is gone. Case B (maintenance
due, waiting for parts): same, picker offered it. Case C negatives BOTH
refused: committed to another site (PREPARE done) → picker empty, the
committed rocket NOT offered for a second expedition; departed/no lander at
the colony → same empty refusal. Fix confirmed permissive-only, not
over-broad. Live observation matching the entry's recorded vanilla quirk
(a): the refusal presented as an EMPTY picker rather than the popup — the
mis-parenthesized legacy `WaitLaunchOrder` branch lets the gate answer
"possible" while the (untouched, more-correct) list builder rightly excludes
the committed rocket; harmless, deliberately not touched.

### F73 — Asteroid colonists idle outdoors; nothing shelters the suffocating (P1, med-high)  `[tested: Code/Fix_ShelterReflex.lua — PT-19 PASS 2026-07-28]`
Chain: `MicroGHabitatAutoResolve:IsSuitable` requires `GetScoreFor > 0` ≈ `HasLifeSupport()`
(`MicroGHabitat.lua:154-156`, `Community.lua:367-398`) — any momentary life-support gap or
full habitat → colonist keeps `residence == false`; `Roam` (`Colonist.lua:1186-1205`) then
idles them OUTSIDE in vacuum; `CanService` requires residence == self (`MicroGHabitat.lua:130-132`);
and `Colonist:Idle` has NO seek-shelter branch on the oxygen timer (suffocation only
applies damage, `StatusEffects.lua:140-160`). Workers are safe inside the mine during
shifts; they die during idle stretches next to it. **Fix:** (a) habitat accepts residents
regardless of momentary life support; (b) Idle wrapper: outside > half of
OxygenMaxOutsideTime in vacuum → `SetCommand("Rest")`.
**PT-19 PASS — 2026-07-28, live colony (Douglasjay MicroG Habitat, 9
residents + Micro-G Metals Mining Station, independent power grids).** Gap
shape 1 (habitat toggled OFF a few game minutes) and gap shape 2 (habitat's
power supply cut, building on): identical result both times — **residence
never dropped** (panel showed Residence = Micro-G Habitat throughout), no
homeless flag, clean recovery on restore. Watch through shift end: workers
routed straight back INTO the habitat, nobody idled on the surface — the
vanilla death spiral (permanent homeless → Roam outside → suffocation) is
gone at its root since the residence never detaches. The (b) Rest-reflex
safety net was not observably triggered (nobody stayed outside long enough)
— its wrapper half is fully probe-verified (MarsDebug pass, 2026-07-25/26).
**Vanilla observation recorded, NOT a pack issue:** while the habitat's life
support was cut, colonists WORKING in the independently-powered mine flagged
Suffocating/Freezing/Dehydrated (+ Hypothermia notification) — the status
effects read the RESIDENCE's life-support state, not the building the
colonist occupies; cleared instantly on restore.

### F74 — RC Transports can be ordered onto trade / refugee rockets (P2, high)  `[tested: Code/Fix_RocketInteractGuard.lua — PT-39 PASS 2026-07-27: cursor + route both refused a landed trade rocket; controls clean (F76 caveat on the entry)]`

**Needs-eyes rider DOWNSIZED 2026-08-01 (bug-list audit §2.2, row F74).** The
outstanding observation was never about the fix — PT-39 proved the guard
refuses — it was "does the vanilla harm this prevents actually occur?", and
nobody had ever seen it. **Two outside answers landed with the audit:** a 1.0.7
dev note (*paraphrase-grade*: RC-Transporter rare-metals rocket-overload
exploit fixed, [S32]) and fredware's independent Relaunched fix #10 —
*"Prevents RC Transports from interrupting Universal Trade Rockets"* [S23],
which also makes F74 a ⚑ BRONZE→SILVER promotion. A fix author shipping the
same guard is evidence the harm is real. **So the rider stops being
load-bearing**: it was merged into the F53(a) row in `PLAYTEST_CHECKLIST.md`
§6 and now rides along on that row's never-modded fresh colony rather than
justifying one of its own. (Ours also remains a superset — his guard misses
`UniversalRefugeeRocket`, audit §9.)

**✅ THE RIVAL-ROCKET REPORT IS FOUND, 2026-08-01 — and it comes with its own
OG-era ancestor from the same reporter.** Owner's logged-in Paradox subforum
browse (audit §7.1 item (a)). **Homeshine** (member since Mar 29 2018) reported
this defect **twice, on two different games, nine years apart**:

*Relaunched, **May 2 2026**, **Game Version 1.07**, Steam:*
> **Summary:** "1.07 causes Rockets from other civilizations to glitch out
> permanently if refilled from an RC transport."
> **Description:** "Just updated to 1.07. If you trade with another
> country/civilization, and try to refill their rocket using an RC transport,
> and then stop, the rocket is permanently glitched out and becomes a launchpad
> paperweight for the entire rest of the game."
> **Steps:** "…direct an RC transport to begin loading the requested resource.
> Then, halt the RC transport. The rocket is never interactable by drones or an
> RC transport ever again ever. It will sit on the launchpad forever, unable to
> be filled with any resource."

*Original game, **Sep 5 2022** ("Trains hotfix 1"):*
> "Overflowing trade rocket never takes off again… if you use an RC transport to
> load resources into the trade rocket from the other country, instead the
> rocket breaks, it reads '0', and never gives you what you paid for or ever
> takes off again… It does this whenever the RC transport **'overflows'** the
> trade rocket with more of the export resource than it asked for."

**Read the two together — they are not the same trigger.** 2022's trigger is
*overflow* (loading more than the rocket asked for); 2026's is *halt mid-load*.
Same terminal state both times: a permanently non-interactable rocket stuck on
the pad for the rest of the game. **That matters for the 1.0.7 dev note.** The
audit cited [S32] at paraphrase grade as *"RC-Transporter rare-metals
rocket-overload exploit fixed"* — consistent with the **overflow** trigger being
addressed. The May 2 2026 report is a player who had *just updated to 1.07* and
hit the **halt** trigger anyway. So the honest reading is **not** "the patch note
was false"; it is that the note plausibly covers one trigger and this reporter
found another still live. (Not verified in Src by this session — recorded as a
reading of two reports, not a code claim.)

**Consequences.** (1) The "does the vanilla harm actually occur?" question that
the rider existed for is now answered by a first-party dated report on our own
build family — **paraphrase-grade evidence has been replaced by primary
evidence**, and the merged F53(a) rider carries no F74 weight at all any more.
(2) **Our guard covers both triggers by construction**: `Fix_RocketInteractGuard`
refuses the RC-Transport-onto-rocket order in the first place, so neither an
overflow nor a mid-load halt can be reached. (3) The player-visible cost is
worse than this entry previously said — not "an exploit", a **permanently
bricked rocket**, which raises what the fix is worth. **No code change; PT-39
already PASSed.**

**Audit 2026-07-30 (reachability): R2, one framing correction.** Rival-colony
trade-pad and foreign-aid rockets are plain class `UniversalRocket`
(RivalColonies.lua:242-247; PopupNotificationPreset-Default.lua:42-46) — they
were never covered by the shipped guard OR by F74, so PT-39's "rival-colony
trade offer" wording conflates rocket families: the refused rocket must have
been a storybit/mystery `UniversalTradeRocket`/`UniversalRefugeeRocket`
(spawners, enumerated: CallTradeRocket/CallRefugeeRocket storybit effects —
TheDoorToSummer family, ExportWasteRock_SplintersOfMars — and
SA_CallTradeRocketWithCargo/SA_CallRefugeeRocket in Mysteries 7/8/9). If the
original report's "rival colony rockets" meant trade-pad rockets, that surface
is untouched by F74 — possibly design parity, since the pre-Relaunched guard
never covered a mechanic that didn't exist. Full block in
REACHABILITY_AUDIT.md.
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
(1.07)" in `docs/archive/RESEARCH.md`.

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

### F78 — MeteorsDisaster hangs mid-strike; the colony never sees a meteor — and possibly no disaster/weather at all (P1, high)  `[tested 2026-08-01 (Tier-1 legs 1+4, log Mars.exe-20260801-17.11.08 — both §6.2a-D completion branches ran live; see the leg note below the PT-54 block): Code/Fix_MeteorStormWedge.lua — built 2026-07-29 after the QA review superseded the full-replacement plan: hourly watchdog detects the wedge signature (g_MeteorStorm set + no DisasterMeteorStorm notification + nothing falling, sustained 1h), heals via RestartGlobalGameTimeThread("MeteorStorm") + a guarded g_MeteorStormStop pulse + forced-state cleanup; 3 heals/session then loud give-up (F02 pattern); **PT-54 RETIRED unrun 2026-08-01 → verification rides the Tier-1 build leg** (note below); **StormWedgeHeal REORDERED 2026-08-01 (F86 Tier-1, spec §6.2a-D): orphan gate at body start and after every Sleep (resets g_MeteorStormStop INSIDE the gate), vanilla-state resets before every mod-name touch, logging last — closes the adjudication-predicted orphan stray where the heal died at a Note call after setting the stop flag; the reordered path is exercised by Tier-1 leg 1**. Wave-6 probe in TestKit 55_Probes_Wave6.lua — PASS in the 2026-07-29 pre-flight A/B, its first run against a fixed leg; until that run the probe silently reported SKIP (missing PASS verdict, repaired same day), so wave 6 had no recorded automated coverage before it]`
**⭐⭐ ORGANIC OCCURRENCE CAUGHT IN THE WILD 2026-08-02 — the wedge happened in
the owner's own playthrough, unprompted, and the heal fired on load.** Log
`Mars.exe-20260802-01.31.10:269-272`, loading a 98-sol save (lineage
`save_game_id: HdmSxGs6kyd0uz6-`, NASA/rocketscientist) during the C26
maintenance-dump sitting — nothing about that sitting touched meteors:

```
MeteorStormWedge: WEDGE confirmed - g_MeteorStorm set for 1h+ with no notification
  and nothing falling (scheduler thread alive but stuck); healing
MeteorStormWedge: scheduler thread restarted - future storms will schedule again
MeteorStormWedge: forced storm state clean (7 stray meteor object(s) removed)
```

**Why this matters more than another fixture run:** every previous confirmation
of this wedge came from a purpose-built fixture or a forced `CheatMeteors`
storm. This is the signature arising **in ordinary play**, detected by the
watchdog's own three-part test, with **7 stray meteor objects** left behind —
and the same load carried a stranded prediction flag for F81(a) (see that
entry). The two sibling defects co-occurred on one organic save.
⚠️ **One qualifier, stated so it is not over-read:** that save was written under
pack **`v0.00-001`** and loaded under **`v1.00-001`** (log `:235`), so the
wedged state accumulated under an **older pack build**. This is therefore strong
evidence that **the vanilla state occurs in real play** — it is *not* evidence
about whether the current pack prevents it, which it does not claim to do
anyway (the fix is a heal, not a prevention). The heal path itself is current
and it worked on first contact.

**⭐ SECOND ORGANIC OCCURRENCE THE SAME SITTING, ON AN INDEPENDENT COLONY**
(log `:315-316`): a **different playthrough** (`save_game_id: 91Wh-Fin5FhlZmaF`,
map `BlankBig_02`, sol 59 of which ~50 were organic pre-playtest play, not
opened in a long time) loaded with the **same wedge signature** —
`WEDGE confirmed … scheduler thread alive but stuck; healing` →
`scheduler thread restarted`.

**The four-load pattern, recorded with its confounds because it is suggestive
and easy to over-claim:**

| load | save | sol | pack ver in save | wedge? | F81(a) stranded flag? |
|---|---|---|---|---|---|
| 1 | colony A, late | 288 | current (no mismatch) | **no** | **no** |
| 2 | colony A, early | 98 | `v0.00-001` | **yes** | **yes** |
| 3 | colony B | 59 | `v0.00-001` | **yes** | **yes** |
| 4 | colony C, young/basic | low | `v0.00-001` | **no** | **no** |

⚠️ **CORRECTION, same sitting:** an earlier draft of this note said *"two for
two on independent old-pack-era saves."* **Load 4 makes it two of three.** A
fourth independent colony (`save_game_id: Dps_S53Fxrq6RJPv`, map `BlankBig_01`,
also `v0.00-001`) loaded carrying **neither** state — only the routine
`MeteorFrequency` migration fired. The plausible reason is mundane and worth
recording rather than glossing: it is a **young basic colony**, so it has most
likely not had a meteor storm at all yet, and no storm means no wedge and no
stranded prediction flag. **Prevalence is 2 of 3 old-pack saves, not 2 of 2.**

⛔ **What this does NOT establish, and must not be written as if it did:** that
the current pack *prevents* the wedge. Confounds, all live: load 1 is a **later
save of the same colony as load 2**, so its cleanliness may simply mean an
earlier load already healed it and none recurred since; n = 3; we have no
vanilla control; and this fix was never a prevention in the first place — it is
a detector plus heal, so "no wedge pending at save time" is the expected steady
state once it has run once. **What it DOES establish is prevalence**: the wedge
is not exotic, it sat in **two of three** real playthrough saves. See the
standing rule on keeping those two claims apart — a "the pack improves vanilla
stability" claim needs a control we do not have and belongs nowhere, least of
all `MOD_DESCRIPTION.md`.

**⛔ PT-54 RETIRED UNRUN 2026-08-01 → verification rides the F86 Tier-1 build
leg.** The test was withdrawn before it ever ran, by the project prompt chain,
because the F86 Tier-1 build reorders this fix's heal sequencing (the
orphan-gate rule, plus the meteor watchdog moving onto
`Msg("MeteorDone")`/`NewDay` restarting **vanilla's** body) and deletes the
`Fix_RainsDeadlock` body it was bundled with — running it would have verified
code that is about to stop existing. **What absorbs F78's half:** PT-54
Trigger C (the wedge heals itself) → the Tier-1 **A/B pair**, which must
exercise the reordered heal path; Trigger D (storms keep scheduling after a
heal) → the A/B pair **plus** the F88 load-3×-inside-a-rolled-interval
regression leg. Chain prompt 4 records those legs as PT-54's retirement made
good, and flips this entry's status through the normal protocol (index row +
heading tag, both). Full trigger text preserved in `PLAYTEST_ARCHIVE.md`;
absorption table in `PLAYTEST_CHECKLIST.md` §3. **No session may re-run PT-54
against the current bodies.**

**✅ TIER-1 LEGS RUN 2026-08-01 (owner at the keyboard) — PT-54's retirement is
made good, and this entry flips to `tested`.** Save lineage `save_game_id
HdmSxGs6kyd0uz6-`, map BlankBigCanyonCMix_09, log
`Mars.exe-20260801-17.11.08`. **Both §6.2a-D completion branches ran live on
the reordered body**, which is more than the leg asked for:
- **Release branch** (forced storm, leg 1): `0:20:28.442 WEDGE confirmed -
  g_MeteorStorm set for 1h+ with no notification and nothing falling (scheduler
  thread alive but stuck); healing` → `scheduler thread restarted - future
  storms will schedule again` → F81's handler cleared the prediction flag
  (`0:20:28.517`) → `0:20:29.230 wedged storm released through the vanilla end
  path`. **Logging LAST is visible in the ordering** — that is the §6.2a-D
  orphan-gate rule holding under observation.
- **Force-clean branch** (the scheduler's OWN natural storm, unforced):
  `1:56:48.368 WEDGE confirmed … healing` → `scheduler thread restarted` →
  `1:57:01.692 forced storm state clean (8 stray meteor object(s) removed)`.
  Vanilla-state resets precede every mod-name touch; the 13 s restart→Note
  spread is exactly the specced 10×4 s pulse window.
- **Trigger D (storms keep scheduling after a heal): PASS** — `IsValidThread
  (MeteorStorm)` true after the heal, and the natural storm above *is* the
  scheduler proving it, having been scheduled after the leg-1 heal. Regular
  meteor cadence continued around it (86.7 h scheduler gap interleaved).
- **Storms are 2-for-2 wedging in this colony** — F78's repro is robust, not
  incidental; the heal is what makes the colony survive it.

**Uninstall behaviour (leg 5, log `Mars.exe-20260801-19.14.11`):** with the
pack disabled, `MeteorStorm: thread valid=true` on vanilla's body and **zero
lines naming this module** — the reordered heal leaves nothing behind.

**User report (2026-07-28, save TEST 2G):** minimal-but-nonzero disaster map
settings, 194 sols played, ZERO disasters ever seen, and no weather effects at
all despite terraforming progressing well into the range where toxic rains
should occur. Save context: 3 maps loaded (surface `BlankBigCanyonCMix_09`,
underground, asteroid), `active_game_rules = {}` (verified from the save
header — NoDisasters is NOT set).
**Hard evidence (the PT-01 meteor silence-watch doing its job):** the F02
watchdog fired on the LIVE save repeatedly —
`WATCHDOG — Meteors thread silent for 183 game hours (last phase 'striking',
thread ALIVE but stuck); restarting` (log 2026-07-27 13:18), again at 182h
(15:19 same day), and `MeteorsWatchdog = { restarts = 1 }` in the 2026-07-28
live session. The watchdog's own preconditions rule out designed silence (it
checks the descriptor exists and is not forbidden before arming), and the
`striking` heartbeat is set IMMEDIATELY before the call into the shipped
`MeteorsDisaster(meteors, meteors_type)` (`Fix_MeteorFrequency.lua:105-106`,
placed there precisely to make this identifiable) — so **the hang is INSIDE
the vanilla strike routine** (`Lua\Meteors.lua`): the scheduler rolls and
waits correctly, enters the strike, and never returns (no `struck` heartbeat,
no visible meteors). The F02 fix machinery is working as designed — without
its restarts the thread would simply be dead with no trace.
**Scope suspicion:** the user reports ALL disaster/weather types silent, not
just meteors. The sibling disaster threads (dust storms, cold waves, dust
devils, the terraforming rains) have NO heartbeats — if they wedge the same
way they die invisibly. Multi-map is the prime suspect axis (strike target
selection / map iteration on a save with underground + asteroid maps loaded).
**Investigation plan (next session):** (1) game-free trace of
`MeteorsDisaster` (`Lua\Meteors.lua`) — find the non-returning path (loops
over target/sector selection, WaitMsg that can never fire, map-bound MapGet
on the wrong map); check the sibling disaster threads for the same shape;
(2) attended: console heartbeat taps on the sibling threads +
`SMRFixPack.MeteorsWatchdogCheck()` / `SMRFixPack.MeteorsBeat` reads at a
stall moment; (3) fix decision per FIX_POLICY once the stall line is known.
**TRACE DONE (2026-07-28 game-free, mid-sitting): PRIME SUSPECT ISOLATED.**
`MeteorsDisaster`'s final wait loop (`Meteors.lua:238-241`) runs
`table.validate(spawned)` — but `spawned` holds plain DESCRIPTOR tables
(`{meteor=obj, start=pt, pause=n}`, built by `SpawnMeteor` at `:109`), not
the meteor objects. The check the code needs is on `descr.meteor`. If the
C-side `table.validate` leaves non-object entries intact (its documented
sibling `table.validate_map` explicitly does, `CommonLua\LuaExportedDocs\
Global\table.lua:319`), `#spawned` can NEVER reach zero and the thread
spins on the 3s `WaitMsg` tick forever after its FIRST strike — matching
the watchdog exactly (phase `striking`, alive-but-stuck, silent 183h,
re-wedges after every restart; the meteors themselves fall in independent
`fall_thread`s at `:481-503`, so the first strike may even land visibly
while the scheduler never returns). **One-line live discriminator (run
next session):** `*r local t = { {meteor=1} } table.validate(t)
print("validate kept:", #t)` — `1` = confirmed (the loop is statically
un-exitable; fix = full replacement of the global `MeteorsDisaster`, F12
precedent, with `table.validate(spawned, function(d) return
IsValid(d.meteor) end)`); `0` = hypothesis dead, fall back to live console
taps on `SpawnMeteor`/`PlayStartMeteorStormFX` to bracket the stall. Note:
only Meteors.lua uses `table.validate` among the disaster files (grep
2026-07-28) — the sibling threads do NOT share this defect, so the
no-weather-at-all half of this report still needs its own trace (dust
storms/devils/cold waves/rains; separate leg).
**SCOPE NARROWED TO STORMS — measured live 2026-07-29.** Two natural single
strikes were seen in play, and the console read that followed settles which
thread is sick: `phase=long-sleep-done age=1h restarts=0`. **Zero watchdog
restarts** — so the strikes were genuine, the pack's repaired scheduler is
running its designed cycle, and the earlier guess that each strike came from a
watchdog restart is WRONG. The pack's thread only ever calls
`MeteorsDisaster(meteors, "single"|"multispawn")`
(`Fix_MeteorFrequency.lua:96-106`) and that path is demonstrably healthy.
**The wedge therefore lives in the vanilla `MeteorStormThread`
(`Meteors.lua:318-346`, calls `MeteorsDisaster(meteors, "storm")` at :346),
which carries no heartbeat and dies invisibly.** Consequences for this entry:
(1) the live repro must fire **`CheatMeteors("storm")`**, not `"single"` — the
single path will never reproduce it; (2) the storm branch is the only one that
adds the duration notification at :179, which is what strands the prediction
flag — see F81, where that stranding was CONFIRMED live and clearing it
restored weather instantly.
**WEDGE REPRODUCED ON DEMAND AND LOCALIZED TO THREE LINES (2026-07-29).**
Driven directly past the broken `CheatMeteors` entry point with
`CreateGameTimeThread(function() MeteorsDisaster(Presets.MapSettings.Meteor
["Meteor_High"], "storm", GetRandomPassable(MainMap)) end)` under console taps
on `MeteorsDisaster` / `SpawnMeteor` / `PlayStart|EndMeteorStormFX`:
```
ENTER MeteorsDisaster type=storm
spawned 25 / spawned 50 / StartFX after 73 spawns
(no EXIT, ever)          g_MeteorStorm=true stop=false
validate #10 n=2 … #140 n=2      DisasterMeteorStorm = true
```
**The stall is the drain loop, `Meteors.lua:238-241`:**
```lua
while not g_MeteorStormStop and #spawned > 0 do
    WaitMsg("MeteorDone", delta)      -- delta = 3000, so it spins every 3s
    table.validate(spawned)
end
```
`table.validate` is doing its job — 73 descriptors fell to **2** — but those
last two never go invalid, so `#spawned` never reaches 0 and the loop spins
forever. **Hypothesis 1 is therefore half right and half wrong:** the loop is
not statically un-exitable (validate DOES clear entries, matching the earlier
`kept: 0` probe), but it is unbounded, so a single meteor that never becomes
invalid wedges the whole storm permanently. Why two meteors stay valid is not
yet known (fall thread dying, MDS interception, an off-map impact are the
candidates) — **and the fix does not need that answer**: the loop simply must
not be unbounded, and the tail already does `DoneObject(descr.meteor)` on
whatever survives.
**Two control results from the same sitting:** `CheatMeteors("single")` printed
ENTER *and* EXIT (the single path completes cleanly, matching the healthy
scheduler), and the spawn loop terminated normally at 73 — killing the
unbounded-spawn hypothesis.
**TWO STORMS WERE WEDGED AT ONCE — and `g_MeteorStormStop` is a SHARED GLOBAL
(2026-07-29, observed live; this constrains any fix).** Setting
`g_MeteorStormStop = true` once released ONE thread (`EndFX` printed) while the
`validate n=2` traffic kept climbing; a `*g` loop pulsing the flag ten times
released a SECOND (`EndFX` **and** `EXIT`), after which validate traffic stopped
completely. So the user-triggered storm and a natural scheduled storm (the
"Meteor Storm 8h → 1h" countdown seen earlier the same sitting) were both stuck
in the drain loop simultaneously. Because `Meteors.lua:242` resets
`g_MeteorStormStop = false` immediately after the loop, **the first thread to
wake consumes the stop signal** and any concurrent storm keeps spinning.
**Consequences for the repair:** (a) the drain-loop bound must be
**per-invocation** (a local deadline), never a shared global; (b) the fix must
assume concurrent storms are possible rather than treating one storm as a
singleton; (c) `g_MeteorStorm` / `g_MeteorStormStop` are both process-global
state that concurrent invocations trample — worth auditing every other consumer
before replacing the function. The stop-flag pulse also doubles as the **live
recovery** for a wedged storm:
`*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end`.
**Side finding, resolved:** the first released thread printed `EndFX` with no
`EXIT`, which briefly looked like a second wedge inside
`Msg("MeteorStormEnded")`. The second thread printed `EndFX` **and** `EXIT`
back-to-back, so `Msg` does NOT block — the missing line was lost in the
validate spam. No defect there.
**Tooling fact worth keeping (RE-CORRECTED 2026-07-29 QA session):**
`GetCameraLookAtPassable` is a **file-local helper** (`local function`,
`Cheats.lua:42`) — the console's `attempt to call a nil value` proved only that
locals are invisible to console code, NOT that the shipped build differs (the
shipped `Cheats.lua` is byte-identical to Src; full fpk diff on the STATUS key
facts). A bare `CheatMeteors("storm")` can still silently no-op — the helper
returns nil when no passable point exists within 100m of the camera look-at,
and the body is `if pos then … end` with no else. Always pass an explicit
position, or drive `MeteorsDisaster` directly as above.
Note the dust-storm half of the original report is CLOSED: `GetDustStormDescr()`
returns nil at the save's terraforming level — designed silence, no defect.
**The "no weather at all" half is now EXPLAINED and split off — see F81**
(2026-07-29 trace): `RainsDisasterLoop` deadlocks permanently on an untimed
`WaitMsg("RainDisasterEnd")` the first time a rain roll collides with any
active OR merely predicted disaster, and terraforming changes do not restart
it. That is a SEPARATE defect from this one — meteors are not even part of
`IsDisasterActive()` — so F78 keeps only the meteor wedge. Note this also
means the two reports were never one root cause. Still unexplained by either
entry: the absence of dust storms and cold waves, whose loops use timed,
retrying waits and cannot deadlock this way (rule out map settings first).
Cross-refs: F02 (the scheduler fix + watchdog), F81 (the weather half of the
original report), PT-01 (the passive watch that caught this — record the
catch on its line when the checklist is next touched).

### F79 — Colonists never use trains for services; the service search is passage-only (P3, high confidence)  `[wontfix 2026-07-31 — OWNER DECISION, declined as feature-completion; reasoning below. Do NOT re-propose or park it]`

**⛔ DECIDED `wontfix` 2026-07-31 (owner).** *"I am cutting services for trains.
I think that introduces risks of more issues than it might fix, especially in a
large multi stop end game map."* This is a **decision, not a deferral** — it is
not parked in `FUTURE_IDEAS.md` and it is not owed to anyone. Two facts already
on file support it, and they are why the decision should stand rather than be
revisited casually:

1. **The train boarding layer has an open, UNEXPLAINED defect — F80.** A
   colonist with a fully valid ticket sat 17+ game hours while four trains
   stopped and left without boarding anyone, with ~19 colonists queued and no
   capacity branch ever running. F79's own "Cross-refs" line already pointed at
   it (same session). Teaching `GetService` to hand a whole new rider class
   (shoppers) to a boarding layer that demonstrably drops the riders it already
   has would stack a feature on unstable ground — and the failure would look
   like *our* bug.
2. **The fix sketch sits on a hot path and scales with exactly the map shape the
   owner named.** It post-wraps `Dome:GetService` — consulted for every
   colonist's service search — and on in-dome + passage failure adds a
   station-enumeration walk over train-reachable domes. On a large multi-stop
   end-game map (many domes × many stations × many unserviced colonists) that
   cost lands on the worst case, in the state where the colony is already
   struggling.

The gap itself is real and stays documented below as vanilla behavior. If it is
ever revisited, **F80 must be explained and closed first** — that is the
precondition, not a preference.
**Live observation (2026-07-28, F21 setup):** a dome stripped of services, with
a working 5-station train network to three service-rich domes, produced ZERO
service riders — colonists roamed their own dome "looking for places to shop"
indefinitely while trains ran outside. **Root, code-confirmed:** service
selection funnels solely through `Dome:GetService` (`Dome.lua:2900-2943`),
whose cross-dome branch walks only `GetConnectedDomes()` (`:619-630`) =
passage-connected domes (plus physically-in-range domes once the map is
open-air breathable). Stations/trains appear nowhere on that path. The
train-aware reachability that DOES exist — `Colonist:CanReachDomeForBuilding`
(`Colonist.lua:3207`, consults `GetTransportRoute`) — is consulted by
`Workplace.lua:522`, `TrainingBuilding.lua:148`, and `Residence.lua:292`
only: **trains carry workers, trainees, and migrants — never shoppers.** The
transport layer itself fully supports service trips (ticket commands, the
`CanColonistsFromDifferentDomesWorkServiceTrainHere` gate, boarding), so the
gap is precisely that `GetService` was never taught about stations. Player
impact: "build a leisure dome and connect it by rail" — a natural Martian
Express colony shape — silently does nothing for service needs; unserviced
colonists roam and bleed Comfort. **Fix sketch (D-item, user decision per
FIX_POLICY §4 — this is feature-completion, not defect repair):** post-wrap
`Dome:GetService` to, on in-dome + passage failure, enumerate train-reachable
domes (the same station walk `recursive_enum_dome_workplaces` uses,
`Dome.lua:646-687`) gated on `allow_service_in_connected` + the
WorkServiceTrain gate, returning a service the transport layer can already
ticket. Cross-refs: F80 (boarding anomaly found in the same session), PT-43
F21 (the test whose setup surfaced this).

### F80 — Trains stop at a platform and skip valid waiting passengers (P2, med)  `[investigating — observed live 2026-07-28; mitigated by adding trains; unexplained]`
**Observed (2026-07-28, live):** a colonist with a fully valid transport
ticket (`stage = Waiting`, both stations valid) sat at a station for 17+
game hours while at least four trains stopped, exchanged cargo, and left
without boarding anyone — with ~19 colonists in `waiting_for_train` at that
station and ZERO "full train" Comfort penalties logged (so the capacity
branch never ran either). Forensics that ruled out config: every one of the
five track routes contained BOTH her src and dst stations (console sweep);
every track's `transport_mode` read `all`; she was verifiably present in
`src_station.waiting_for_train` (index 19); stations working. **Suspected
mechanism (untested):** the stop-processing walk (`Train:TransferCargo` →
`ForEachStationAlongTrack(station, track, 0, ...)`, `Train.lua:882`) derives
its enumeration direction from the TRACK's canonical orientation at that
station (`TrainTransport.lua:371`) — NOT the train's travel direction — and
with flags 0 it neither wraps nor reverses; a destination lying "behind"
that fixed direction would be structurally unenumerable at that stop, in
both travel directions, forever (`ticket_dest == dest` can never match,
`Train.lua:962`). **Adding 3 more trains (2→5) got passengers moving**,
which is consistent with the theory (other tracks' orientations cover the
missing directions) but does not prove it. A ready console tap on the
global `ForEachStationAlongTrack` (prints each stop's enumerated dest set —
in the session log 2026-07-28) brackets it definitively if the symptom
recurs. **That tap is now a standing rider in `PLAYTEST_CHECKLIST.md` §6
(bug-list-audit table, added 2026-08-01), with one instruction attached: TAP
BEFORE MITIGATING** — adding trains is the known workaround and it destroys
the evidence. The audit (§4) rates F80 the strongest reported-but-unpinned
defect we hold: a Relaunched witness (*"they crowd a train station supposedly
waiting for it to take them to the dome they're right next to!"* —
reeses4brkfst, Nov 27 2025 [S34]) plus a dev note, and still no located
mechanism. Related vanilla wart, same session: the trip planner books tickets
over track REACHABILITY with no regard for train SERVICE — colonists queue
indefinitely at stations no train serves, with no UI hint. Cross-refs: F79,
PT-43 F21.

**⭐ WITNESS CLUSTER + TWO MECHANISM CONSTRAINTS, 2026-08-01 — from the Reddit
thread the owner exported (`BUG_LIST_AUDIT.md` §10.5, source [S36]).** F80 was
"one Relaunched witness and no mechanism". It now has a crowd, and two of them
narrow the search.

**⚠️ READ THE BUILD CAVEAT FIRST: the thread is hotfix-1.0.3-era (~Dec 2025),
FOUR hotfix generations before our pinned 1.0.7.396349.** None of it is evidence
about the current build. What it *is* evidence about is that the symptom family
is real, widespread and colony-lethal — which is the §4a "who benefits" question,
not the "does it still exist" question. Our source claim is unaffected either way.

The recurring report is not quite ours and that difference matters: players
describe colonists **declining the train and walking**, dying en route —
> Changlini (top comment, 44 pts): *"…too many people choosing to walk(suffocate)
> to the next station."*
> mortemdeus: *"just lost a colony from this glitch and had to restart. Way too
> many trying to walk between train stations and dieing."*
> Domagan: *"Colonists ignoring trains underground to walk the entire length of
> the map is still an issue."*
> RhebRed: *"still having issues with colonists walking along the train tracks
> and suffocating to death."*
> TelperionST: *"Trains are still a death trap waiting to happen."*
> [deleted]: *"…my geologist keep dieing when trying to get back."*

**Why that is plausibly the same defect wearing a different face.** This entry's
mechanism theory is that a destination lying "behind" the track's canonical
orientation is *structurally unenumerable at that stop, forever*. A colonist who
cannot be ticketed to a destination does not stand still — they walk. So "waits
forever at the platform" and "ignores the train and walks" may be two outcomes
of one unenumerable-destination bug, differing only in whether a ticket was ever
issued. **Not established — recorded as the hypothesis the tap can discriminate.**

**Two observations that constrain the mechanism, and both fit the theory:**
1. **Sorbicol:** *"It's only between two domes though as far as I can tell. My
   rail network currently includes 3 lines and multiple stations."* — a
   **specific origin/destination PAIR fails on a multi-line network while the
   rest works**. That is exactly the signature of a per-stop directional
   enumeration miss, and it is very hard to explain with a capacity, service or
   config theory.
2. **Berkzerker314:** *"I think its when the only rocket leaving is out of range
   of the train station. So they just Leroy Jenkins it across the map."* — a
   destination-selection trigger, i.e. the failure is tied to **which
   destination** is being routed to, not to train supply.

**Prior-art note (relevant to any fix shape):** two commenters recall ChoGGi
mods for this class in the ORIGINAL game — a train fix mod the OP was
recommended, and *"Choggi also had a fix for long walks so at least they didn't
suffocate in case they still walked stupid walks"*. That second one is the
**mitigation** shape (survive the walk) rather than the repair shape (fix the
routing), and it is adjacent to **C19**'s missing distance term. Worth knowing
before anyone designs a fix here.

**What this does NOT do: it does not locate the mechanism.** The console tap on
`ForEachStationAlongTrack` is still the only thing that settles it, and the
"TAP BEFORE MITIGATING" instruction stands.

**✅ SOURCE AUDIT RUN 2026-08-02 (prompt 6c). Result: the enumeration theory
SURVIVES and now has an exact predicate — but reachability is CANNOT
DETERMINE, so this stays `investigating` and the tap-before-mitigating
instruction is unchanged.** The audit was asked for **per-stop/per-pair
asymmetry, not a global break** (Sorbicol reports one origin/destination pair
failing inside an otherwise healthy 3-line network). That is the shape found.

- **The predicate, exactly.** `ForEachStationAlongTrack`
  (`Lua\TrainTransport.lua:367-447`) derives its walk direction once and never
  normalises it: `local traverse_dir = next_idx - start_idx` (`:374`), where
  **both indices come from `table.find`** (`:369`, `:372`) — i.e. the **first**
  occurrence in the `route` array. It then advances `idx = idx + traverse_dir`
  (`:445`) with **wrap-to-1 / wrap-to-n rather than modular arithmetic**
  (`:393-405`). Nothing anywhere constrains `traverse_dir` to ±1.
- ⚠️ **The route array can contain a station more than once, and the file says
  so itself.** The comment at `:389` — *"big stations can exist more than once
  in the same route if the track loops back into them"* — and `EnumRouteTracks`
  confirms it structurally: it appends `dest` unconditionally (`:282`) and only
  terminates on reaching **start_station via start_track** (`:273-279`), so a
  line that re-enters an intermediate station is appended twice.
- **Why a stride ≠ ±1 is fatal rather than merely lossy.** `route.edges` holds
  only **adjacent** pairs (built one per hop, `:255`, `:271`, `:291`). The loop
  looks up the edge for each consecutive pair and, finding none, does
  `if not link_edge then return end` (`:417`) — **a hard return, not a skip**.
  So the first non-adjacent step silently drops **every remaining station**, and
  the caller cannot tell an empty tail from a complete enumeration.
- ⭐ **This explains BOTH public symptoms from ONE function, which the late
  addition to this entry asked for.** `Lua\Units\Train.lua:882` uses it to
  decide `next_stop` / `has_any_work` → a destination never enumerated is a
  platform the train never stops at ("**colonists wait**"). `Station:GetReachableStations`
  (`Lua\Buildings\Station.lua:222-231`) uses it to decide which stations count
  as train-reachable at all → a truncated set means colonists never believe the
  train serves that station ("**colonists ignore the train and walk, and die**",
  the dominant symptom in the wild). Same enumeration, two faces.
- ⛔ **NOT PROVEN, and this is the honest limit: I could not show a buildable
  topology that puts the operative occurrence of a station at anything other
  than its first index.** The shape is real; the trigger is not demonstrated.
  Treat this as a sharpened hypothesis, not a located mechanism.
- **Checked and ruled out so it is not re-derived:** the three other `return`s
  in the walk (`:417` aside — `:421` a track segment under construction, `:428`
  a transport-mode conflict, `:434` passenger-through-cargo) are **hard aborts
  by design and correct**: `route` is a path, so anything beyond an
  untraversable edge genuinely is unreachable on that track. They are not the
  defect. Likewise the one-direction walk on a non-loop route (`:383`, `:396-404`)
  is correct at each call site — a mid-line station covers both directions
  because `ForEachConnectedTrack` runs the enumeration once per connected track.
- ⚠️ **CORRECTION to a suspicion this project had recorded.** The old checklist
  rider stated the suspected mechanism as *"the stop-processing walk takes its
  enumeration direction from the track's canonical orientation, not the train's
  travel direction, so a destination lying behind it is structurally
  unenumerable at that stop forever."* **That is wrong.** The direction is taken
  from the *track being enumerated* (`:371-374`), and every call site enumerates
  **once per connected track**, so both directions are covered at a mid-line
  station and an end station has only one direction to cover. The rider has been
  rewritten; the defect is the **magnitude** of `traverse_dir`, not its sign.

**Two side findings, recorded because they bind any fix WE write here:**

1. ⚠️ **`ForEachStationAlongTrack` is NOT re-entrant.** `stations_visited` is a
   single **file-local shared table** (`:365`), cleared at the top of every call
   (`:386-390`). A callback that enumerates — directly or through any helper —
   wipes the outer call's visited set and then the outer call resumes reading
   the inner call's. No current call site nests, so this is latent in vanilla;
   it becomes live the moment a mod's hook enumerates inside a callback. **If we
   ever wrap this function, our callback must not call it.**
2. `Station:GetReachableStations` (`Station.lua:222-231`) runs one enumeration
   **per connected track** into a shared accumulator, and since `stations_visited`
   is cleared per call there is **no cross-track dedup** — a station reachable on
   two tracks is appended twice. A duplicate, not a miss; harmless for the
   `CanColonistsFromDifferentDomesWorkServiceTrainHere` filter it feeds, but it
   would skew any count taken off that list.

**The settling observation has been rewritten around this** (`PLAYTEST_CHECKLIST.md`
§6) — it now discriminates **waits vs walks** and tests the predicted
**directional asymmetry** in one sitting, which is worth strictly more than
timing the waiting case alone.

### F81 — A stranded disaster-prediction flag silently gates the whole weather system; the rains loop also deadlocks on it (P1, PROVEN)  `[tested 2026-08-01 (Tier-1 legs 3+4, log Mars.exe-20260801-17.11.08 — natural collision re-roll, migration stamped, C34 heal, and the stranded-flag sweep proven BOTH ways with liveness held; see the leg note below the PT-54 block): Code/Fix_DisasterPredictionLeak.lua (additive OnMsg.MeteorStormEnded removal — the leak — plus a PostLoadGame reconciliation clearing any flag with no live notification behind it; safe because every disaster preset is Dismissable=false, so flag-without-notification is stranded by construction) + Code/Fix_RainsDeadlock.lua (**REWRITTEN 2026-08-01, F86 Tier-1 spec §6.2a-B: the loop replacement is DELETED — vanilla's RainsDisasterLoop stays; a layer-2 wrapper on RainsDisasterActivation mirrors the collision test BEFORE the call and posts Msg("RainDisasterEnd") on the early-return, so a collided cycle costs one re-roll; a version-stamped PostLoadGame migration pass (SMRFixPack_loop_version; resolves id-less entries by unique type match) moves every persisted loop onto vanilla's body and carries the C34 stale-state rider — structure repairs → stale-ACTIVE FinishRainProcedure heal → loop migration**). Leak half built 2026-07-29 post-QA; rains half rewritten 2026-08-01; **PT-54 RETIRED unrun 2026-08-01 → verification rides the Tier-1 build leg, except the (a) leak half's live legs, routed to chain prompt 3** (note below); wave-6 probes in TestKit 55_Probes_Wave6.lua — both PASS in the 2026-07-29 pre-flight A/B, their first run against a fixed leg; until that run they silently reported SKIP (missing PASS verdict, repaired same day), so wave 6 had no recorded automated coverage before it]`
**⭐⭐ F81(a) OBSERVED ON THE OWNER'S OWN SAVE 2026-08-02 — a stranded flag,
arising organically, cleared on load.** Log `Mars.exe-20260802-01.31.10:252`,
loading a 98-sol save (`save_game_id: HdmSxGs6kyd0uz6-`) during the C26
maintenance-dump sitting, which touched nothing weather-related:

```
DisasterPredictionLeak: cleared stranded prediction flag 'DisasterMeteorStorm'
  (no live notification behind it)
```

That is the reconciliation half firing on a real stranded flag — the exact state
this entry says gates the whole weather system — **found in ordinary play rather
than planted.** ⭐ **It is also C36's mechanism caught live**: `Dream.lua:20-34`
skips the Inner Light mirage loop for as long as `IsDisasterPredicted()` holds,
so this save was, until that load, silently unable to advance that mystery.
**The same load also healed a live F78 meteor-storm wedge** (`:269-272`) — the
two sibling defects co-occurred on one organic save, which is what the shared
`MeteorStorm` origin predicts.
⚠️ **Qualifier:** the save was written under pack `v0.00-001` and loaded under
`v1.00-001` (log `:235`), so the flag stranded under an **older pack build**.
Evidence that the **vanilla state occurs in real play**; not a statement about
the current pack's leak-prevention half, which is a separate claim tested by the
Tier-1 legs.

**⭐ SECOND ORGANIC OCCURRENCE THE SAME SITTING, INDEPENDENT COLONY** (log
`:300`): a different playthrough entirely (`save_game_id: 91Wh-Fin5FhlZmaF`, map
`BlankBig_02`, sol 59 with ~50 sols of organic pre-playtest play) loaded
carrying **another stranded `DisasterMeteorStorm` flag**, cleared the same way —
and **the same load also carried a live F78 wedge** (`:315-316`). **Two
independent colonies, both carrying both defects.** ⚠️ A **fourth** load the
same sitting (a third independent colony, young and basic, also `v0.00-001`)
carried **neither**, so the prevalence figure is **2 of 3 old-pack saves, not
2 of 2** — most likely because a young colony has not had a meteor storm yet. The co-occurrence is what
the shared `MeteorStorm` origin predicts, and it is now observed twice rather
than once. ⛔ **Prevalence, not prevention** — the full three-load table and its
confounds are recorded on the **F78** entry; do not read the pattern as evidence
that the pack prevents the leak, which needs a vanilla control we do not have.
⭐ **Reachability consequence worth naming:** two of three real playthrough saves
were, at the moment of loading, silently unable to advance **Inner Light**
(C36's mechanism, `Dream.lua:20-34`). That is no longer an inference.

**⭐ F81(a) IS NOW STANDARD COMMUNITY ADVICE — the strongest real-world
reachability signal this project has for any fix (2026-08-01).** Two **current**
Reddit threads the owner exported (`BUG_LIST_AUDIT.md` §10.6, [S37]/[S38];
~2026-07-30 and 2026-08-01, i.e. contemporaneous with our pinned build) show the
same regular telling two different newcomers, unprompted, to install a fix
**before they start playing**:
> *"It is buggy… **I recommend running the game with the disasters patch mod
> (Patch 1.0.7 No Disasters After Meteor Storms)**"* — and, to a second player,
> *"**disasters are broken but you can fix it with a mod**."*

**That mod is GromGor's workshop `3717125029`, already in our archive and
already read.** Its own `metadata.lua` description, re-verified this session:
*"After a meteor storm, **one of the keys may not be removed, preventing further
disasters from generating.** This mod fixes this issue."* — **this entry's (a)
half exactly**, the stranded `g_DisastersPredicted` key that silently gates the
whole weather system.

**Why it is worth recording separately from §9's code-level match.** §9 proved
his fix and ours manage the same key. This proves something §9 could not: **the
symptom is common enough, and recognised enough, that experienced players treat
the fix as a prerequisite for playing the game.** That is a §4a "who benefits"
answer from outside our own reasoning — and it is one of the few places where a
defect's real-world weight can be observed at all. ⚠️ Read `BUG_LIST_AUDIT.md`
§10.6's selection-bias caveat before quoting the threads for anything else;
enthusiast "no bugs" testimony in the same threads is data about the speaker,
not the build.

**⭐⭐ AND THE SAME COMMENTER, IN THE SAME BREATH, DESCRIBED A SECOND SYMPTOM OF
THIS SAME DEFECT WITHOUT KNOWING IT — (a) SILENTLY KILLS THE "INNER LIGHT"
MYSTERY. Verified in Src this session; this is a NEW player-visible consequence
for this entry.** Alongside "install the disasters mod", mizushimo twice tells
newcomers *"**Inner light is broken for some people** so pick a different
mystery."* Those are not two bugs.

`Lua\Mysteries\Dream.lua:20-34` — Inner Light is `DreamMystery` (`:4,:6`) and
advances by dreams. Its mirage thread is:
```lua
while UIColony.mystery.state == "running" do
    if IsDisasterPredicted() or IsDisasterActive() then
        Sleep(5000)
    else
        Dream(city) ; Sleep(...)
    end
end
```
**`IsDisasterPredicted()` is the flag this entry's (a) half strands permanently
true.** Once stranded, the loop takes `Sleep(5000)` forever, `Dream()` never
fires again, the scenario's `WaitMsg("MysteryDream")` (comment at `:24`) never
returns, and **an entire mystery playthrough dies silently** — no error, no
notification, just a story that stops.

**It also explains the reporters' "for some people" exactly**, which is what
lifts this above a guess: you are affected iff a meteor storm completed (or a
Capture Meteors POI fired) during your run. That is the same precondition this
entry's own reachability story already uses.

**Half of this was already on the books and nobody joined it up.**
`REACHABILITY_AUDIT.md`'s F81 block already listed *"the Inner Light dream
cycle"* among the leak's downstream victims — as a code inference, never
observed. The community supplied the observation; the source read above
confirms the path. **Consequence for this entry: (a)'s player-facing cost is
larger than "the weather stops" — it silently voids a mystery.** Filed and
closed as **C36**.
**Not proven:** nobody has watched Inner Light *recover* under our fix. Cheap
settling observation if wanted — stall it, apply the pack, see whether dreams
resume. Not scheduled.

**⛔ PT-54 RETIRED UNRUN 2026-08-01 — and this entry is the one that keeps a
LIVE OBLIGATION out of it.** The test was withdrawn by the project prompt
chain because the F86 Tier-1 build deletes and replaces the `Fix_RainsDeadlock`
body outright (`SAVE_SAFETY_REDESIGN.md` §6.2). **Absorbed:** Trigger E (rains
survive collisions) → the `Fix_RainsDeadlock` rewrite's own A/B leg, including
the migration pass and the C34 stale-ACTIVE rider; the rains-half settling
observation below rides that same leg (it previously said "PT-54 can carry
it"). **NOT absorbed:** Triggers **A** (load-time reconciliation heals a
stranded flag) and **B** (a genuine warning is never cleared — the liveness
test). Both test `Fix_DisasterPredictionLeak`, whose body Tier 1 keeps, so no
rewrite leg covers them by construction, and the wave-6 probe asserts that
mechanism only synthetically. They were **routed to chain prompt 3**
(2026-08-01) and were Tier-1 leg 4 (that build prompt has since been consumed;
leg 4's readings are recorded in this entry below). **The
pre-cleared mid-session reconcile prompt 3 held was TAKEN and BUILT
2026-08-01 (spec §6.2a-C): the same sweep now also runs on `OnMsg.NewDay`
(WhenActive-gated, pcall-wrapped), so trigger A changed shape — a stranded
flag must heal BOTH without a reload (within a sol) AND through the
load-time sweep; trigger B gains the matching liveness assertion (a genuine
warning survives a NewDay tick too).** Full trigger text
preserved in `PLAYTEST_ARCHIVE.md`. **No session may re-run PT-54 against the
current bodies.**

**✅ TIER-1 LEGS 3+4 RUN 2026-08-01 (owner at the keyboard) — PT-54's
retirement is made good, and this entry flips to `tested`.** Save lineage
`save_game_id HdmSxGs6kyd0uz6-`, log `Mars.exe-20260801-17.11.08`.

*Leg 3 — rains half (trigger E absorbed):*
- **The collision arrived NATURALLY, not forced** — `0:20:06 RainsDeadlock:
  rain activation collided with an active/predicted disaster — posting
  RainDisasterEnd so the loop re-rolls`, and rain returned; recurring
  on-and-off rains afterwards are the migrated loop lapping healthily. A
  second natural collision was handled the same way at `1:50:10`.
- **Migration:** `'normal' rain loop migrated onto vanilla's body (settings
  'Normal_VeryLow', version 1.0.1)` at first load, and NO re-migration on
  subsequent loads — the version stamp is honoured round-trip.
- **The id-less clause reads as AMENDED** (commit `70e6d0c`, owner-cleared):
  `toxic` is correctly silent, because that entry is vanilla's own empty
  fill-in; no "left as-is — settings unresolved" line anywhere.
- **C34 rider:** planted `g_RainDisaster="toxic"` with a dead main_thread →
  on reload `0:23:39 RainsDeadlock: stale-ACTIVE rain 'toxic' (main_thread
  dead) — healing through vanilla FinishRainProcedure (C34)`, and
  `g_RainDisaster` read false after.

*Leg 4 — leak half (triggers A and B, in their changed §6.2a-C shape):*
- **A(a) — heals with NO reload:** flag planted, next NewDay tick →
  `0:02:24 DisasterPredictionLeak: cleared stranded prediction flag
  'DisasterMeteorStorm' (no live notification behind it)`. This is the
  mid-session reconcile earning its place: a stranding now gates weather for
  at most one sol, not the rest of the session.
- **A(b) — heals on load too:** re-planted with no sol tick either side,
  cleared INSIDE the load block at `0:10:47`.
- **B — liveness holds against BOTH sweeps:** with a live storm countdown on
  screen, quicksave/reload produced NO clear line and the flag dumped
  `DisasterMeteorStorm = true`; a sol then ticked during the live countdown
  (owner confirmed) and it still read `true`. Genuine warnings are never
  touched by either sweep.

**Uninstall behaviour (leg 5, log `Mars.exe-20260801-19.14.11`):** with the
pack disabled, **zero lines and zero errors naming either module**. The only
rains residue is the allowed inert data — FixtureCarry read
`normal: loop_version=1.0.1 … thread_alive=true id=Normal_VeryLow` and
`toxic: loop_version=nil … thread_alive=false id=nil` — sitting in vanilla's
own `RainsDisasterThreads` entries with vanilla driving them.

**Audit 2026-07-30 (reachability): leak half R1, rains half R2 + settling
observation.** Reachability strengthener not previously recorded: the
**Capture Meteors POI** special project (Data\POI.lua:47-69) fires
`MeteorsDisaster("storm")` on ANY map — bypassing both the NoDisasters rule
and per-map storm settings — so even rule-protected colonies can strand the
prediction flag by launching that expedition. Rains-half settling observation
(~~PT-54 can carry it~~ → the Tier-1 `Fix_RainsDeadlock` A/B leg carries it,
PT-54 retired 2026-08-01): after a rain/disaster collision under the fix, rain
resuming within ≤7 sols — or a console read showing a blocked
`RainsDisasterThreads[type]` activation thread on a vanilla save — upgrades
the deadlock from statically-proven to observed. Full blocks in
REACHABILITY_AUDIT.md.

**LIVE CONFIRMATION (2026-07-29, the user's 194-sol save) — the whole chain,
end to end, in four console reads.** The prediction dump returned exactly what
the static trace predicted:
`DisasterMeteorStorm = true` / `predicted entries: 1`, with
`towers=6 warning=75h active=false rain=false` — **a stranded flag for a meteor
storm that is not running and has not run for a very long time.** Then the
decisive act: `RemoveDisasterNotifications("DisasterMeteorStorm", MainMap)`
→ `predicted entries: 0` → **rain began IMMEDIATELY** (console:
`CloudSeeding POI starts normal rain`; the user: "as soon as I unblocked it
started raining"). One stuck table entry had been suppressing every weather and
disaster system on that save. **This is no longer a hypothesis — the root
cause, the mechanism, and the recovery are all demonstrated.**
**THE LEAK IS UNIVERSAL — EVERY COMPLETED METEOR STORM STRANDS THE FLAG
(2026-07-29, source-exhaustive).** A grep of the whole Lua tree finds exactly
three removals of `DisasterMeteorStorm`:
- `Meteors.lua:227` — only inside the `g_MeteorStormStop` **break** branch
  (i.e. only when a storm is force-stopped, e.g. `CheatStopDisaster`);
- `Meteors.lua:344` — in `MeteorStormThread`, **before** the disaster runs
  (that one clears the *warning* notification);
- `TerraformingDisasters.lua:27` — `OnMsg.TerraformThresholdPassed`, when
  terraforming pushes Atmosphere past the "meteor storms end" threshold (80%).
**The normal completion path (`Meteors.lua:242-251`) never removes it.** It
plays the end FX, sends `MeteorStormEnded` and clears `g_MeteorStorm` — and
leaves `g_DisastersPredicted["DisasterMeteorStorm"] = true` set forever. So on
any map with meteor storms enabled, **the FIRST storm to run — wedged or
perfectly healthy — permanently kills that colony's cold waves and rains.** The
only vanilla escapes are force-stopping a storm or terraforming past 80%
Atmosphere. This is almost certainly why the user's save saw no weather for its
entire recorded history (Atmosphere 57%, no force-stop, storms enabled on
`Meteor_High`).
**SUPERSEDED HYPOTHESIS — kept for the record (Repro A, 2026-07-29).** This
block argued the stranding was a save/load persistence mismatch. **It was
tested and disproved the same sitting** — see "TESTED AND DISPROVED" below;
the notification and its thread both survive a reload. The real mechanism is
the unconditional leak documented above (no removal on any normal path). The
original reasoning, and its flaw, follow:
The stranding was thought to be a plain save/load persistence mismatch:
- `g_DisastersPredicted` is a **GameVar** (`MapSettings.lua:131`) — it is saved
  and restored with the game.
- The notification that would clear it is **not** restorable. The engine says so
  itself, in `SavegameFixups.DisasterNotifications` (:179-187): it reopens dust
  storm and cold wave notifications and then states
  `-- RainDisaster and MetheorStorm cannot be restored because they don't save
  their start/end times`.
- Nothing anywhere reconciles the table against live notifications on load.
**Live proof:** the user set `g_DisastersPredicted["DisasterMeteorStorm"] = true`
by hand (no notification, no meteors, no storm), quicksaved, reloaded — and the
dump came back `DisasterMeteorStorm = true / predicted entries: 1` with nothing
on screen. **A save/load inside a meteor-storm WARNING window is therefore
sufficient to gate that colony's entire weather system permanently**, and with
sensor towers pinning the warning window at 75 game hours (3+ sols) saving
inside one is close to unavoidable. The user's map is `Meteor_High`
(`MainMap.mapdata.MapSettings_Meteor`), so natural storms — and their warnings
— are enabled; only `Meteor_VeryLow` sets `storm_forbidden`
(`Data\MapSettings-Meteor.lua:10`).
**This simplifies the fix and decouples it from F78.** No wedge is required, so
the repair is a one-shot `OnMsg.LoadGame` reconciliation: clear any
`g_DisastersPredicted[id]` that has no live notification behind it. That is the
FIX_POLICY §3 one-shot-sweep shape, needs zero persisted state, and is
self-healing on every subsequent load. The `MeteorsDisaster` in-flight leak
(below) remains a real second stranding path worth closing, but it is no longer
the only — or even the likely — cause.
**FULL RECOVERY OBSERVED (2026-07-29, same sitting):** after the flag was
cleared the user received a **"Toxic rain approaching — starts in 3 Sols"**
notification. That is the complete chain working again — `RainsDisasterLoop`
rolled, `RainsDisasterActivation` passed the gate it had been failing for the
save's entire history, and the toxic band matched `Toxic_High` exactly as the
threshold reads predicted. **It also corroborates the sensor-tower maths
precisely: a 3-sol warning is ~72h against the measured
`GetDisasterWarningTime() = 75h` cap from 6 towers.**
**TESTED AND DISPROVED (2026-07-29): save/load is NOT a stranding path.** I
predicted that a quicksave+reload inside the 3-sol toxic-rain warning window
would strand `DisasterToxicRains` the way `DisasterMeteorStorm` was stranded.
The user ran it: after the reload the **toxic-rain notification was still on
screen and still counting down** ("Starts in 2 Sols 7 h") with
`DisasterToxicRains = true` — i.e. a completely healthy predicted state, not a
stranded one. Both the notification and its owning activation thread survive a
normal save/load (game-time threads are persisted — cf. the zero-upvalue
requirement in `Fix_MeteorFrequency.lua`), so `RainsDisasterActivation` resumes
its `Sleep` and clears the flag properly at
`TerraformingDisasters.lua:302`.
**Where I went wrong:** `SavegameFixups.DisasterNotifications`
(`MapSettings.lua:179-187`) is a **one-time legacy migration** that runs only
when loading a save older than the revision that added it — its
"RainDisaster and MetheorStorm cannot be restored" comment describes that
migration's limitation, NOT routine save/load semantics. I read it as the
latter. Consequently **Repro A proved only that a hand-planted GameVar entry
survives a save**, which is trivially true and is not evidence of any
real-world stranding mechanism. Downgraded accordingly.
**Two practical consequences:** (1) a reload-based playtest protocol (the PT-52
stress A/B) does **not** re-poison a colony — no cleanup needed; (2) the real
mechanism is narrower and cleaner than the save/load story, and is the one
documented immediately above: `MeteorsDisaster` adds the storm DURATION
notification at `Meteors.lua:179` and no normal path ever removes it. The
notification's own `expiration` makes it vanish from the UI while
`g_DisastersPredicted` keeps the flag forever — which is exactly the
flag-true-with-nothing-on-screen state found on this save.
Supporting reads from the same sitting:
- **The pack's meteor thread is HEALTHY** — `phase=long-sleep-done age=1h
  restarts=0`, and the user saw two NATURAL single strikes. So the wedge is
  NOT in the single/multispawn path the pack's F02 scheduler drives
  (`Fix_MeteorFrequency.lua:96-106`); it is in the **vanilla
  `MeteorStormThread`** (`Meteors.lua:318-346`), which has no heartbeat and
  therefore died invisibly — exactly the blind spot F78 named. **F78's live
  repro must use `CheatMeteors("storm")`, not `"single"`.**
- **Dust storms are designed-off at this terraforming level** —
  `GetDustStormDescr()` returned nil while `GetColdWaveDescr()` did not. So the
  dust-storm silence needed no bug at all (the user called this correctly);
  cold waves were possible all along and were blocked purely by the flag.
  **Corroborated from the in-game Atmosphere thresholds panel** (user
  screenshot, same sitting): "Dust storms end 50%" against a live Atmosphere of
  57.38% — over. The same panel independently confirms the rest of the picture:
  "Meteor storms end 80%" (so storms and their warnings are very much live at
  57%, as the user pointed out), "Toxic rains end 55%/55%/5%" against
  57.4/51.9/17.2 — NOT all three past their end, so toxic rain is still legal —
  and "Clear-water rains 40%/40%/10%", all three satisfied, which is exactly the
  normal rain that fired the moment the flag was cleared.
- **Sensor towers at the cap made it near-certain**: 6 towers →
  `GetDisasterWarningTime()` pinned at the 75h maximum, i.e. every disaster
  cycle carried a 3+ sol predicted window.
- **Rain thresholds at the time** (`A 57 need 25-55 | T 51 need 25-55 |
  W 14 need 0-5`) and `RainsDisasterThreads type=table keys=2` with BOTH
  entries empty — the "fill in non-activated rains" placeholders from :453-456,
  i.e. no activation threads existed. Consistent with `process()` early-return
  for the bands whose end thresholds all three params had passed. **Corollary
  worth keeping:** because no activation thread existed, the DEADLOCK described
  below had not yet bitten this particular save — the flag alone accounted for
  the observed silence. The deadlock remains a real latent defect (static proof
  below) that will bite any save whose rain bands ARE in range.
**User report that opened it (2026-07-29, live, same save as F78):** two single
meteor strikes finally seen — but still no other disaster and **no weather
effect of any kind**, and specifically **no toxic rain after BOTH greenhouse-gas
terraforming import events**, whose descriptions promise exactly that.
**The defect (a three-line deadlock, `Lua\TerraformingDisasters.lua`):**
```lua
function RainsDisasterLoop(settings)          -- :310-316
    while true do
        Sleep(settings.spawntime + AsyncRand(settings.spawntime_random))
        CreateGameTimeThread(RainsDisasterActivation, settings)
        WaitMsg("RainDisasterEnd")            -- :314  NO TIMEOUT
    end
end
```
`RainsDisasterActivation` (:276-308) opens with
`if IsDisasterActive() or IsDisasterPredicted() then return end` — it returns
**without starting a rain**, so `FinishRainProcedure`'s
`Msg("RainDisasterEnd")` (:268) never fires, and the untimed `WaitMsg` at :314
blocks **forever**. One collision kills that rain type for the rest of the save.
**The collision window is wide, not rare.** `IsDisasterActive()`
(`MapSettings.lua:127`) is true during any cold wave, dust storm, mystery dream
or other rain; `IsDisasterPredicted()` (:189) is true during the WARNING phase
of *any* disaster — `AddDisasterNotification` sets
`g_DisastersPredicted[base_id] = true` (:169) and only
`RemoveDisasterNotifications` clears it (:176). On a map with any disaster type
enabled, a rain roll landing inside some other disaster's warning window is a
matter of time; at 194 sols it is a near certainty.
**Nothing ever rescues it — including the user's terraforming events.**
`UpdateRainsThreads` (:340, fired via `OnMsg.TerraformParamChanged` :486-489 on
every Atmosphere/Temperature/Water change) REUSES the existing activation
thread whenever `IsValidThread(old_data.activation_thread) and old_data.id ==
settings.id` (:412) — **a thread blocked in `WaitMsg` is perfectly valid**, so
the wedged loop is preserved, not replaced. A new loop is only ever created
when the settings *id* changes (crossing into a different strength band). This
is exactly why importing greenhouse gases twice produced no rain.
**Sibling disasters cannot deadlock this way — but they ARE gated on the same
flag (correction to this entry's first draft, which called them unrelated).**
Dust storms and cold waves poll with TIMED, retrying waits and so never wedge:
`while IsDisasterActive() do WaitMsg("TriggerDustStorm", 5000) end`
(`DustStorm.lua:481-488`, `ColdWave.lua:243-250`). **However**, both scheduler
loops also spin on `IsDisasterPredicted()` — `DustStorm.lua:439-446` and
`ColdWave.lua:208-215` — and while it is true their helper simply pushes
`wait_time` forward by the elapsed delta each poll (`DustStorm.lua:464-465`,
`ColdWave.lua:228-229`). A permanently-true prediction flag therefore defers
them FOREVER without deadlocking anything. Same flag, two different failure
modes: rains deadlock, storms/waves starve.
**THE UNIFYING CANDIDATE — one stale flag would explain the entire report.**
`AddDisasterNotification` sets `g_DisastersPredicted[base_id] = true` for ANY
notification, warning or duration alike (`MapSettings.lua:169`), and only
`RemoveDisasterNotifications` clears it (:176). Inside `MeteorsDisaster` the
**storm** branch adds a `DisasterMeteorStorm` DURATION notification
(`Meteors.lua:179`) whose only removal sits in the `g_MeteorStormStop` break
branch (:227) — the scheduler's own removal at :344 has already run *before*
the call. So a meteor STORM that wedges in the F78 loop (:238-241) strands
`g_DisastersPredicted["DisasterMeteorStorm"] = true` permanently, which would
starve dust storms and cold waves AND trigger this entry's rains deadlock on
the very next rain roll: **one root cause, three dead systems.**
**Caveat that keeps this a candidate rather than a conclusion:** the pack's own
meteor scheduler passes only `"multispawn"` or `"single"`
(`Fix_MeteorFrequency.lua:96-106`) — neither reaches the :179 notification. The
stale flag therefore requires the *vanilla* `MeteorStormThread` (:318-346, no
heartbeat, invisible if it wedges) to have wedged on a storm. Unproven.
**ONE COMMAND DECIDES IT (run in-colony, nothing else needed):**
`*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`
A `true` with no matching disaster on screen = the unified root cause is real
and this entry is downstream of it. An EMPTY table = the systems failed
independently, rains by this deadlock and the dust-storm/cold-wave silence by
something still unfound (rule out map settings first).
**SENSOR TOWERS ARE A DIRECT AGGRAVATING FACTOR (user's question, 2026-07-29).**
`GetDisasterWarningTime(disaster)` returns
`Min(base_warning + const.SensorTowerPredictionAddTime * towers,
const.SensorTowerPredictionMaxTime)` = `Min(base + 12h * towers, 75h)`
(`MapSettings.lua:94-97`, `_GameConst.lua:125-126`). The prediction flag is set
for the WHOLE warning window (`AddDisasterNotification` … `Sleep(warning_time)`
… remove — e.g. `RainsDisasterActivation` :300-302), so each tower adds 12 game
hours during which `IsDisasterPredicted()` is true. At the 75h cap that is more
than THREE SOLS of "predicted" per disaster cycle, and every rain roll landing
in one of those windows deadlocks the rains loop permanently. A heavily
tower'd colony therefore hits this bug early and reliably — which fits a save
that has never once seen weather. Note this is the same inverted-role trap F02
documented for meteor intervals, in a different system.
**But removing towers is NOT a diagnostic and NOT a cure**: it cannot wake a
thread already blocked in `WaitMsg`, nor clear a stale predicted flag, so a
teardown would return an uninformative null while costing the buildings. If
tower count is ever reduced as a MITIGATION, note `GetNumberOfSensorTowers`
(:100-109) still counts a tower switched off within the last 12h
(`tower.turn_off_time - prediction_add_time_ago > 0`) — turning towers off
works but lags ~12 game hours; demolition is immediate.
**Manual recovery if a stale flag is found:**
`RemoveDisasterNotifications("<stale id>", MainMap)` clears it and lets dust
storms and cold waves resume on their own. Rains need that AND the
`CheatRainsDisaster` release below — their loop is already stuck in `WaitMsg`
and clearing the flag alone will not wake it.
**Live discriminator + player workaround (same command, run in-colony):**
`CheatRainsDisaster("<RainsDisaster settings id>")` (:491) runs `RainProcedure`
directly on a fresh thread, bypassing the activation gate. It both PROVES the
rain machinery itself is healthy and — because `FinishRainProcedure` ends with
`Msg("RainDisasterEnd")` — **releases the stuck `WaitMsg`**, restarting the
loop until the next collision. Read the stale prediction state first:
`*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`
(a lingering `true` with no disaster on screen is itself a second finding).
**Fix sketch (NOT built — user decision).** Least-invasive is a replacement of
the global `RainsDisasterLoop` (globals are replaceable from mod code — F22/F12
precedent) that bounds the wait, so a rain that never started costs one cycle
instead of the save: `WaitMsg("RainDisasterEnd", <timeout>)`. Two caveats that
make this more than a one-liner: (a) threads already created (from `CityStart`
or a loaded save) keep running the OLD body, so the fix needs a one-shot
`OnMsg.LoadGame` pass that recreates the activation threads from
`RainsDisasterThreads[rain_type].id`; (b) that pass must respect
`IsGameRuleActive("NoDisasters")` and the in-band threshold checks the way
`UpdateRainsThreads` does. Savegame discipline: zero new persisted state.
Cross-refs: F78 (same save, same report — this is the weather half), F02 (the
meteor scheduler watchdog precedent for exactly this class of thread wedge).

### F82 — Split power/life-support grid notification lingers ~a sol after the grid is rejoined (P3, med)  `[filed 2026-07-29 from live observation — needs its own trace]`
**User observation (2026-07-29, live, while running the F78 storm repro):**
"All notifications I have seen dismiss themselves after their issue is fixed,
except for split power grids — they do dismiss eventually but it takes a MUCH
longer time, close to an entire sol." Noted as felt-wrong even at ultra speed;
at normal or fast speed it would read as a stuck notification. Every other
notification type they have watched clears promptly on resolution.
**What the source says so far (not yet a diagnosis):** the notifications are
`PowerGridProblem` / `LifeSupportGridProblem`, registered at
`SupplyGrid.lua:1348-1349` via
`FixupObjectNotification("PowerGridProblem", "g_SplitSupplyGridPositions",
"SplitPowerGridNotif", empty_func)`. Those two lines are the ONLY references to
`g_SplitSupplyGridPositions` anywhere in `ModTools\Src` — i.e. they are legacy
savegame-fixup registrations for a variable the live code no longer uses, so
the actual add/remove path for the split-grid notification lives elsewhere
(shipped `Lua.fpk`, or a periodic sweep that has not been located yet).
**✅ TRACE FINISHED 2026-08-02 (prompt 6c) — MECHANISM FOUND, and the answer is
neither of the two options this entry was weighing.** There is no periodic
re-check and no missing on-rejoin removal call to restore. **The notification
has no removal path at all, and it is not state-driven in any sense: it clears
only by a fixed REAL-TIME expiry.**

- **It is added in exactly one place and removed nowhere.** The only reference
  to `PowerGridSplit` / `LifeSupportGridSplit` in the whole of `ModTools\Src` is
  `Lua\SupplyGrid.lua:1626-1629`, inside the grid-split pass:
  `AddObjectToNotification(self:GetPos(), GameTime(), notification_id, map)`.
  There is **no matching `RemoveObjectFromNotification`** anywhere for either
  id. (The two `FixupObjectNotification` lines this entry already cites,
  `:1348-1349`, are the *parent* ids and are legacy savegame plumbing — they are
  not the add/remove path and there is no hidden updater.)
- ⭐ **The object it registers is a POSITION, not the grid** — `self:GetPos()`,
  with `GameTime()` passed only as the sort key the preset's `GetObjectItem`
  reads. So there is nothing for anything to re-evaluate: the notification does
  not hold a reference to the grid, and **rejoining the grid is not an input to
  it**. This is the entry's own "clears from code paths, not from state" theme
  in its purest form.
- **What clears it is the preset's `Expiration`, and it runs on REAL time.**
  Both split presets carry `Expiration = 120000` with `GameTime = false`
  (`Data\NotificationPreset.lua` — `LifeSupportGridSplit` and `PowerGridSplit`),
  and `UpdateNotificationThread` branches on exactly that flag:
  `GameTime` true → `CreateGameTimeThread`, false → **`CreateRealTimeThread`**
  (`CommonLua\Libs\Notifications\Notifications.lua:188-217`, expiry fires at
  `:194-199`). So the lifetime is **120 000 ms of REAL time = 2 real minutes**,
  independent of game speed and independent of whether the grid was ever
  rejoined.
- **Sibling tell, the same shape that carried C04/F90.** The neighbouring
  children of the same two parents — `PowerLeak` and `LifeSupportLeak` — carry
  **no `Expiration` at all**; they are cleared by state when the leak is
  repaired. The split ones were deliberately given a timeout instead. One
  notification family, two clearing disciplines, in the same preset file.
- **The arithmetic reproduces the observation — and the observer's estimate was
  RIGHT.** One sol = `const.Scale.sols` = 720 000 ms of game time
  (`Lua\__const.lua:1454-1458`; `const.Scale.h` = 30 000, `:1438-1442` → 24
  h/sol). ⚠️ **CORRECTED 2026-08-02 by the live run — the max player speed is
  5×, not 20×.** `const.ultraGameSpeed = 20` exists
  (`Lua\_GameConst.lua:26-28`) but **`"ultra"` is appended to the speed-state
  list ONLY under `if Platform.debug`** (`Lua\X\HUD.lua:462-467` and
  `:481-487`), and the HUD wires buttons for `"play"`/`"medium"`/`"fast"` only
  (`Lua\XDef\HUD.generated.lua:226,:247,:269`). **On retail the fastest
  reachable speed is `const.fastGameSpeed` = 5×** — confirmed in game by the
  button's own tooltip, *"Fastest — Play at five times normal speed"*.
  So the real figures are: at **5×**, 120 real seconds spans **600 000 game ms =
  0.83 sols**; at **1×** it spans **120 000 game ms = 1/6 sol**. The game-time
  spread between slowest and fastest is **5×, not 20×**.
  ⛔ **WITHDRAWN: the earlier claim here that the observer's estimate "reads
  low".** It did not. 0.83 sols *is* "close to an entire sol", which is exactly
  what the 2026-07-29 report said. **The error was mine** — I took
  `ultraGameSpeed = 20` from source and assumed it was the speed the player
  meant, without checking that it is debug-gated and unreachable.
- ⭐ **That inversion is the discriminating prediction, and it is free to
  take:** the delay is **constant in real time and shrinks in game time as you
  speed up**. No state-cleared notification can behave that way. The checklist
  rider has been rewritten around it (see `PLAYTEST_CHECKLIST.md` §6) — stopwatch
  the *real* seconds, not the sols, and note the game speed.

**MEASURED LIVE 2026-08-02 - LEG 1 OF 2, AND IT LANDS ON THE PRESET VALUE TO
WITHIN 1 MILLISECOND.** Owner at the keyboard, No-Disasters save
(`save_game_id: 1f6oCbWfYS7IOPCY`, map `BlankUnderground_01`, sol 22) chosen so
that **nothing but the player could break a cable** - no dust storms, so no
random `RandomBreakSupplyGrid` splits to confound the reading. A cable was
salvaged, the split notification raised, and **nothing was repaired or
clicked**. A console watcher polled `FindNotification("PowerGridSplit",
CurrentMap)` (`CommonLua\Libs\Notifications\Notifications.lua:16-23`) and timed
both clocks:

```
F82 ARMED - notification seen
F82 CLEARED after 119999 real ms and 600000 game ms      (speed: 5x, retail max)
```

- **119 999 real ms against a preset `Expiration = 120000`.** The notification
  cleared on its **real-time** timer, to within a millisecond, **with the grid
  still split and nothing repaired**. The source read is now confirmed by
  measurement rather than inference.
- **600 000 game ms / 119 999 real ms = exactly 5.0x**, which independently
  recovers `const.fastGameSpeed` from the data - and is what forced the
  speed-ceiling correction recorded above.
- **Leg 2 (1x) is what completes the proof**: the prediction is the *same*
  ~120 000 real ms with game time five times smaller (~120 000 game ms). Real
  time constant plus game time variable is the signature that no state-cleared
  notification can produce.
- **Do not click the notification when re-running this.** `PowerGridSplit` does
  not set `Dismissable` and the property defaults to **`true`**
  (`CommonLua\Libs\Notifications\NotificationPreset.lua:60-61`), so a click can
  end the measurement early. (F81's note that disaster presets are
  `Dismissable = false` does not carry - those set it explicitly.)
- **Supporting tell for the package:** `GameTime = false` on both split presets
  is an **explicit override against a default of `true`**
  (`NotificationPreset.lua:65-66`), so the real-time expiry is the authors'
  deliberate choice, not an accident of defaults.

**Consequence and disposition.** The player is shown a live warning for a
condition that has ended, for up to 2 real minutes, with no way to dismiss it by
fixing anything — and, symmetrically, a split that is *not* repaired stops being
reported after 2 real minutes. The second half is the more serious one and was
not in the original report. **Nothing built** — the repair shape is not obvious,
because the notification is keyed by the break *position* and a rejoin does not
happen at a known position, so a `RemoveObjectFromNotification` heal needs a
key-matching design first. **Routed to chain prompt 7** as a §4 package
question. Stays **P3** until the rider returns; the "never clears an unrepaired
split" half may argue for P2.

Related in kind (not in mechanism) to F81/F78, where a notification
that is never removed gates whole systems — the recurring theme is that this
codebase clears notifications from specific code paths rather than from state.

### F83 — Minimized story popups lose their callback across a save/load; First Asteroid silently withholds three promised prefabs (P2, PROVEN mechanism)  `[tested 2026-07-31 — Fix_FirstAsteroidPrefabs, shape (i) the load-time heal; PT-59 PASSED IN FULL, archived]`

**✅ PT-59 PASSED IN FULL 2026-07-31 (keyboard, owner at the controls) — F83 is
`tested`.** Full record in `PLAYTEST_ARCHIVE.md`. The three triggers:

- **(A) the reload leg** — trigger fired, First Asteroid notification left
  unanswered, quicksave, reload: counters **1 / 1 / 1**, the flag latched
  `true`, and exactly one
  `FirstAsteroidPrefabs: First Asteroid prefabs recovered after a save/load (3 granted)`
  line. Answering the re-shown popup afterwards left the counters at 1/1/1.
- **(B) the healthy leg** — same trigger, popup answered with NO save/load:
  counters **1 / 1 / 1** (vanilla's own grant) and
  `SMRFixPack_FirstAsteroidPrefabs` **still `false`**, so our code never ran on
  the healthy path. That is the double-grant guard, and it is why the fix's
  first draft was rejected.
- **(C) reload twice** — subsumed and exceeded: the sitting logged **10 game
  loads and exactly 2 grants**, the two grants 14 minutes apart with **7
  non-granting loads between them**. The persistent flag holds across repeated
  loads, and the heal stays silent on loads with nothing to heal.

**Two things this sitting proved that the test was not designed to ask:**

1. **The heal discriminates against a near-neighbour popup.** The trigger
   actually raises **two** asteroid notifications from the same preset file —
   `ReconCenterDiscoveryAsteroid` (*"A new Asteroid has been discovered!"*, three
   buttons) and `FirstAsteroid` (single OK, carrying the
   `<effect> Gain Micro-G Auto Extractor Prefabs` line). Both sat in the corner
   list together and `find_stranded_notification` picked the right one every
   time — the loc-id match on the live preset is doing real work, not just
   finding the only candidate.
2. **8 of 10 loads granted nothing.** The no-op path is the common one and it is
   quiet.

⚠️ **Procedure defect found and FIXED in the checklist (it cost a leg).** PT-59
did not say *which* popup to answer. Answering `ReconCenterDiscoveryAsteroid`
produces **0/0/0**, which reads exactly like a fix failure and was initially
reported as one. The `FirstAsteroid` preset declares **no choices at all**
(`PopupNotificationPreset-Asteroid.lua:28-38`) and `WaitPopupNotification` runs
the grant callback unconditionally on any answer
(`PopupNotification.lua:302-304`) — so there is no wrong *button*, only a wrong
*popup*. This is a fresh instance of the standing playtest-method rule: an
un-run PT's procedure is unverified until it has been executed once.

**Found in play 2026-07-30**, mid-setup for PT-56. The tester got the
`FirstFounderEnthusiast` popup ("When Life Gives You Lemons…", Samuel Hayden has
the Enthusiast trait) as a corner notification, opened it, clicked **View** —
and nothing happened. Note the popup is a *scan* announcement, not a trait-gain
event (`CheckFirstColonistWithTrait` announces the first Founder who ALREADY has
one of six traits), so **this is unrelated to F23/PT-44**. It is also not ours:
the pack never references `WaitPopupNotification` for these presets,
`ViewAndSelectObject`, `SelectObj` or `ViewObjectMars`.

**Mechanism — proven end to end at the keyboard, same session.**
1. **These popups ALWAYS start minimized.** `ShowPopupNotification` takes the
   open-immediately branch only when `context.start_minimized == false`
   (`Lua/UI/PopupNotification.lua:261`) — an explicit `== false`. No
   `FirstFounder*` or `FirstAsteroid` preset defines the field and no call site
   passes it, so it is `nil`; `nil == false` is false; every one of them takes
   the else branch and becomes a corner notification.
2. **The waiter is a REAL-TIME thread.** `CreateRealTimeThread(function()
   WaitPopupNotification(…) end)` (`Lua/ColonyViability.lua:51`), and
   `WaitPopupNotification` blocks in `WaitMsg(context.async_signal)`
   (`PopupNotification.lua:293-306`).
3. **Neither the thread nor the context survives a load.** Real-time threads are
   not persisted, and `OnMsg.PersistSave` keeps only queue entries carrying a
   `sync_popup_id`; these are async (`bPersistable` nil → `context.async_signal
   = {}`), so the context is dropped from `g_PopupQueue` too.
4. **The minimized NOTIFICATION does survive** — observed. So after a reload it
   is still on screen and still clickable: `PressFunc` re-queues and opens the
   popup, any choice runs `host:Close(i)` → `PopupNotificationEnd` →
   `Msg(context.async_signal, i)` — **and nothing is listening.** The callback
   never runs. The popup just closes.

**Tester observations, 2026-07-30 (this is the evidence, in order):**
- *Organic:* popup arrived, View clicked, nothing — no selection, no camera move.
- *Isolation:* `ViewAndSelectObject(<the founder>)` called directly from the
  console **worked** — camera jumped, colonist selected. So the view helper is
  healthy and the failure is that the callback never delivered. (This also
  killed the first hypothesis, that the colonist was inside a building.)
- *Controlled repro, same session:* console `WaitPopupNotification` with the
  identical preset, params and callback → corner notification → open → View →
  **callback ran, camera jumped.** Machinery healthy live.
- *The decisive leg:* same repro, notification left minimized across a quicksave
  and load, then answered → **View dead.** Tester, verbatim: *"Correct view died
  after a load."*

**Scope — eight in-game call sites pass a callback** (`WaitPopupNotification`
over `Lua/`; the two `PreGameMission.lua` tutorial calls pass a `host` parent,
not a callback, and are excluded):

| Call site | Preset | What the callback does |
|---|---|---|
| `Asteroids.lua:415` | FirstAsteroid | **grants 3 prefabs** |
| `Discoveries.lua:126` | ReconCenterDiscoveryAsteroid | choice 1 opens planetary view; **choice 2 performs the paid Detailed Scan** |
| `ColonyViability.lua:52` | FirstFounder\<trait\> | `ViewAndSelectObject` |
| `ColonyViability.lua:173` | LastFounderDies | `ViewAndSelectObject` |
| `ColonyViability.lua:185` | FirstFounderDiesOfOldAge | `ViewAndSelectObject` |
| `ColonyViability.lua:199` | FirstColonistDeath | `ViewAndSelectObject` |
| `ColonyViability.lua:216` | LastFounderLeavingMars | `ViewAndSelectObject` |
| `ColonyViability.lua:260` | `class.popup_on_first` (status effects) | `ViewAndSelectObject` |

Six are cosmetic — a dead View button on a story popup. **Two are not.**

**Second consequential site — `ReconCenterDiscoveryAsteroid`
(`Discoveries.lua:117-136`), and it is the FREQUENT one.** It fires on *every*
asteroid discovery, not just the first (`OnMsg.SpawnedAsteroid` →
`ShowAsteroidPopupNotification`), so a player meets it repeatedly. Its choice 2
is **"Detailed Scan (Costs: N Electronics stored in Recon Centers)"** and runs
`PerformDetailedScan(asteroid)`, which spends the Electronics and sets
`asteroid.scanned = true`. Answered after a reload the callback never runs, so
the popup closes and **the player's paid action is silently refused** — no
Electronics spent (the cost lives inside the same callback, so nothing is
stolen) and no scan performed. Milder than the prefab loss and probably
recoverable through the planetary-view UI — *verify that before grading it* —
but it is a player-initiated action that silently does nothing, and it is
reachable far more often than the once-per-game FirstAsteroid popup.

**The FirstAsteroid case — permanent, silent loss of a promised reward.**
```lua
WaitPopupNotification("FirstAsteroid", nil, nil, nil, function()
    ColonyAddPrefabs("MicroGAutoExtractorExoticMinerals", 1, nil, MainCity)
    ColonyAddPrefabs("MicroGAutoExtractorMetals", 1, nil, MainCity)
    ColonyAddPrefabs("MicroGAutoExtractorRareMetals", 1, nil, MainCity)
end)
```
- **The popup's own text promises it:** `<effect> Gain Micro-G Auto Extractor
  Prefabs for every type of resource`
  (`Data/PopupNotifications/PopupNotificationPreset-Asteroid.lua:36`).
- The preset carries **`show_once = true`** (`:35`) and
  `g_ShownPopupNotifications[preset]` is set the moment the notification is
  opened — so once dismissed it never comes back.
- `OnMsg.SpawnedAsteroid` runs the block only at `UIColony.asteroid_count == 1`
  (`Asteroids.lua:412`). No retry, no second chance.
- No alternate grant path found for those ids; the only other `AddPrefabs` of
  them is `AutomaticMicroGExtractor.lua:15/25`, a different context (re-verify
  before relying on it).

Net: leave the First Asteroid corner notification alone, save, reload, then open
it — the game tells you that you gained three prefabs, and you did not. Nothing
reports the loss.

**⭐ OBSERVED IN PLAY — PT-58 PASS, 2026-07-30.** No longer an inference. Purpose-
built fixture (new game, `hydroengineer` profile, `NoUndergroundAndAsteroids`
off), pre-flight `asteroid_count=0 max=1 recon_researched=false`. Trigger was the
game's own: `UIColony:SetTechResearched("ReconCenter")`, which fires
`Msg("TechResearched", …)` → `Asteroids.lua:392` → `SpawnAsteroid`. Two legs off
one fixture, one variable:

| Leg | `MicroGAutoExtractorMetals` | `…RareMetals` | `…ExoticMinerals` |
|---|---|---|---|
| Popup answered **without** a reload | **1** | **1** | **1** |
| Saved with the notification **unanswered**, reloaded, then answered | **0** | **0** | **0** |

The notification **did survive the load** and opened normally; the choice closed
it and granted nothing. Confirms every step of the mechanism and the
consequence: **a player who leaves the First Asteroid notification in the corner
across a save/load permanently loses all three prefabs**, is told in the popup's
own text that they received them, gets no error, and — because the preset is
`show_once` and `OnMsg.SpawnedAsteroid` only fires at `asteroid_count == 1`,
a counter that never resets — has no second chance for the rest of that game.

**Intent — UNINTENDED, hard tell: self-contradiction.** The popup's own
`<effect>` line promises a reward its delivery path can silently fail to grant;
text and code disagree inside one feature. Secondary tell: the notification
survives the load and keeps offering a **View** affordance that cannot function
— a live control with a dead action. Not a design choice under any reading.

**Reachability — R1 (live), PLAY-PROVEN on both halves.** The minimized corner
notification is the *only* presentation these popups get, and leaving one sitting
and then saving/reloading is ordinary play. The mechanism was reached
organically first (the founder popup, unprompted, mid-setup for another test),
then reproduced under control, and the **consequence** was then observed on its
own purpose-built fixture (PT-58, above). The earlier caveat on this entry —
that the FirstAsteroid consequence was inferred from code shape and needed a
keyboard observation before any fix shipped — is **discharged**. It was the right
caveat to hold: it took one 10-minute fixture to convert, and the inference
turned out correct in every particular.

**Family:** the same trap as **F06** (Mystery 10's Epilogue arrives minimized by
SA default and a one-shot `CrystalFlyAway` is missed while it sits) — and F06's
audit note already says the minimized-by-default presentation makes it "easier
to hit than this entry says". F06 repaired its own one-shot by re-broadcasting;
F83 is the general case of the same shape. Also thematically adjacent to
F81/F78/F82: this codebase drives state changes from specific code paths rather
than from state, so anything that interrupts the path loses the change.

**~~⛔ FIX ON HOLD~~ — AUDIT COMPLETE 2026-07-30 (`docs/reports/POPUP_CONSEQUENCE_AUDIT.md`):
the hold is LIFTED and the narrow-decouple recommendation is REINSTATED.** The
owner asked whether FirstAsteroid is really the only thing a player can lose
this way, and the same-evening first dive said "no — storybits". **That storybit
alarm was WRONG, and wrong about the engine:** it assumed a
`CreateGameTimeThread` without `MakeThreadPersistable` dies on load. The
default is the opposite — **game-time threads persist BY DEFAULT with their full
blocked stacks; real-time threads do not** (three source proofs + the everyday
observed fact that units resume mid-command after every load; now an
ENGINE_FACTS entry). Storybits, mysteries, anomaly sequences and challenges all
wait in game-time threads and are save-safe by the engine's own design (the
storybit notification window even carries a forced-popup timeout backstop,
`const.StoryBits.NotificationTimeout`). What the dive got right and the audit
confirms: `choiceN_func` is safe, the return-value form is exposed exactly like
the callback form, and the exposure is real — but **only where the waiter is a
REAL-TIME thread**, which is exactly this entry's two consequential sites plus
one latent shielded class (filed **F85**). F06 is NOT this family (its defect is
a one-shot `Msg` missed while a sequence popup sat — no save/load involved; its
fix stands). **Corrections to this entry from the audit:** the eighth callback
site (`ColonyViability.lua:260`, `class.popup_on_first`) is a **game-time**
thread whose presets open immediately — safe on both axes, not part of the
exposed list; and the commented-out `AnomalyAnalyzed` wait
(`PlanetaryAnomaly.lua:299-305`) is dead code, not a live site. Full
enumeration, safety rule, and needs-eyes list in the audit file.

**Fix options (option 1 RECOMMENDED by the audit; ⭐ OWNER GAVE THE GO
2026-07-30 evening — "review and action on your findings" to the audit
session. ⭐ OPTION 1 IS NOW BUILT, in shape (i) — see the build record below
this list for what shipped and why (ii) was rejected).**
1. **Narrow, RECOMMENDED — but ⚠️ NOT as originally written here.** The
   original text ("additive `OnMsg.SpawnedAsteroid` granting the three prefabs
   once behind a persistent flag; the shipped handler can stay") has a
   **double-grant trap, caught 2026-07-30 late**: `WaitPopupNotification`
   ALWAYS `procall`s its callback — even when `ShowPopupNotification`
   early-returns on `show_once` (`PopupNotification.lua:249`, `:302-304`) —
   and the FirstAsteroid callback takes no args and grants unconditionally, so
   with vanilla's grant still live the healthy no-reload path would pay
   **2/2/2**. The claim that "the flag already stops a double grant" was wrong
   for the present-day case (the flag gates only OUR handler, not vanilla's
   callback). Corrected shapes (build session verifies both against Src and
   picks one — both stay FIX_POLICY §1.2-additive, smallest surface, no shared
   UI machinery):
   * **(i) LoadGame sweep:** grant behind the flag ONLY when the stranded
     state is detected on load (FirstAsteroid minimized notification still in
     the persisted `Notifications` GameVar, flag unset; match by T loc-id, not
     T identity). Healthy path untouched.
   * **(ii) show_once pre-mark:** additive handler shows the popup itself as
     display, then sets `g_ShownPopupNotifications.FirstAsteroid = true` in
     the same dispatch — the shipped RT thread's Show early-returns and its
     always-run callback grants IMMEDIATELY at spawn, before any wait exists.
     Residual window: the sub-frame before the shipped RT thread runs.
   **PT-58's fixture gives the A/B (filed as PT-59 at build time):** the
   reload leg must read 1/1/1 — and the no-reload leg must STILL read 1/1/1,
   not 2/2/2; that half now guards the trap above.
2. **General:** re-arm stranded async popup waiters on load. Fixes all eight at
   once but touches shared popup machinery, would rot on patches, and risks
   double-firing callbacks. **Not recommended.**
3. **`ReconCenterDiscoveryAsteroid`'s Detailed Scan** (the second consequential
   site) is untested — it needs a Recon Center holding enough Electronics for
   `CanPerformDetailedScan()` to be true, otherwise choice 2 renders disabled.
   Own fixture, own observation, not covered by PT-58.
4. **The six cosmetic View buttons:** low value on their own. Reasonable to
   document and leave, or to let option 2 carry them if it is ever taken.

**⭐ BUILT 2026-07-30 — `Code/Fix_FirstAsteroidPrefabs.lua`, Register id
`FirstAsteroidPrefabs`. Shape (i), the load-time heal.** Option 1's corrected
form; shape (ii) was verified against Src and REJECTED. What ships:

- **`OnMsg.LoadGame` sweep** (FIX_POLICY §1.2 additive handler + §3's sanctioned
  one-shot cleanup). If a FirstAsteroid popup notification is still sitting in
  the persisted `Notifications` table after a load, its real-time waiter is
  necessarily dead — nothing else produces that state. The sweep then, in order:
  **removes** the stranded notification, **grants** the same three prefabs
  through the same `ColonyAddPrefabs(..., 1, nil, MainCity)` calls in the
  shipped order, **latches** a persistent flag, and **re-shows** the popup as
  pure display so the player still gets the story text.
- **The healthy path is untouched** — no reload means no `LoadGame`, so a player
  who answers normally goes through vanilla and reads 1/1/1. This is what makes
  the double-grant trap unreachable: our code never runs on that path at all.
- **Removing the notification is load-bearing, not tidiness.** Its `PressFunc`
  closure is the only thing that can re-queue the dead context, so with it gone
  exactly one grant path exists. That holds even if a future patch moves the
  shipped waiter to a game-time thread (where it would persist and still be
  listening) — a bare additive grant would pay 2/2/2 in that world.
- **Identification** is by the FirstAsteroid preset's localization id, read from
  the LIVE preset at sweep time, never hardcoded. Two facts force it: the preset
  id is NOT on the notification instance (`ShowPopupNotification` nils
  `instance.id` at `PopupNotification.lua:286`, because `AddNotification` asserts
  an id-less instance), and T identity does not survive a load. **Correction to
  the audit's build note:** matching on `text[1]` would have worked only in a dev
  build — `T()` returns **light userdata**, not a table, whenever the id is in
  the translation table (`localization.lua:268`), which is the retail case. The
  accessor that handles both forms is `TGetID` (`localization.lua:48-65`).
- **Save footprint:** one GameVar, `SMRFixPack_FirstAsteroidPrefabs`, boolean.
  `GameVar` from mod code lands in the real `_G` and in `PersistableGlobals`
  (`lib.lua:1040-1055`); `ModEnvMeta.__newindex` explicitly permits writing a
  name registered there (`Mod.lua:1559`). A save made with the mod and loaded
  **without** it is unaffected — `OnMsg.PersistLoad` only restores names still
  listed in `PersistableGlobals` (`persist.lua:135-142`), so the stray value is
  ignored.
- **Why NOT shape (ii)** (the `show_once` pre-mark — show the popup ourselves,
  then set `g_ShownPopupNotifications.FirstAsteroid = true` in the same dispatch
  so the shipped thread's Show early-returns at `:249-251` and its
  `WaitPopupNotification` reaches `procall(callback, res)` at `:302-304`
  immediately). The mechanism is real and was confirmed in Src — it is exactly
  why a *naive* additive grant is wrong — but it was rejected on three counts:
  (1) its correctness rests on OnMsg handler order **and** on
  `CreateRealTimeThread` not running the body during the Msg dispatch, a C
  export whose scheduling is not verifiable from Src, and losing that race shows
  the player two corner notifications; (2) it moves the grant off the healthy
  path for every player, fixed or not (prefabs at spawn instead of on answer);
  (3) it cannot heal a save already sitting in the stranded state, which shape
  (i) does — including the owner's own PT-58 fixture.
- **Known limit, deliberate (§3 "conservative by default"):** a player who has
  already answered the dead notification after a reload is past detection — the
  notification is gone and "granted then spent" is indistinguishable from "never
  granted". Those saves are not healed. Nothing is guessed.
- **Probe:** `SMRTest.FirstAsteroidPrefabs` (TestKit `56_Probes_Wave7.lua`, a new
  wave file). Drives `SMRFixPack.HealFirstAsteroidPrefabs()` against planted
  globals over three legs — stranded (must grant 1/1/1, remove once, re-show
  once, latch), already-healed (must grant nothing — the no-double-grant
  assertion), and a decoy non-FirstAsteroid popup (must grant nothing and must
  not latch).

**⭐ THE FIX-VERIFICATION FIXTURE EXISTS AND IS KEPT (owner, 2026-07-30): a save
taken BEFORE the `ReconCenter` tech was ever researched**, on the PT-58 colony.
That is the reusable A/B fixture for whatever fix is built — load it, apply the
fix, grant the tech, leave the notification unanswered, save, reload, answer,
read the counters. **The reload leg must read 1/1/1.** Because it predates the
trigger it also restores `g_ShownPopupNotifications`, so the `show_once` popup
re-offers itself on every run — this fixture can be used indefinitely rather
than being consumed by one attempt. Do not lose it.

**~~PT-58 owed before any fix~~ — RUN AND PASSED 2026-07-30** (results in the
OBSERVED block above; archived in `PLAYTEST_ARCHIVE.md`). Fixture recipe worth
keeping, since the popup is `show_once` and one save gives one shot: new game,
commander profile **not** `SpaceMiner`, game rule `NoUndergroundAndAsteroids`
**off**, `ReconCenter` tech **unresearched**; verify with
`UIColony.asteroid_count` / `UIColony:IsTechResearched("ReconCenter")`; save
BEFORE triggering so the fixture can be regenerated (loading a pre-trigger save
also resets the `g_ShownPopupNotifications` GameVar, which is what makes the
`show_once` popup offer itself again); then
`UIColony:SetTechResearched("ReconCenter")`.

### F84 — Universal Tunnel's description is wrong on two counts (P3, PROVEN)  `[todo — text patch, but the localization tradeoff makes it a USER DECISION; nothing built]`

Shipped description (`Data/BuildingTemplate/UniversalTunnel.lua`, T 893478951171):

> *"The tunnel entrance and exit can connect tracks and power grids at different
> locations and different elevations. **Rovers cannot use this type of tunnel.**"*

Both halves are wrong.

**(a) Rovers CAN use it — DISPROVEN BY PLAY, 2026-07-30** (tester, during PT-25,
taken as a free rider on that setup). The tester built a Universal Tunnel pair on
the surface and confirmed **rovers route through it**. This matches the code
exactly: `UniversalTunnel`'s `object_class` is `TrackTunnelBase`
(`__parents = { "TunnelBase", "TrackConnectedObjBase" }`,
`Lua/Buildings/TrackTunnel.lua:1-5`) with **no override** of `AddPFTunnel`, and
`TunnelBase:AddPFTunnel` registers
`pf.AddTunnel(self, start_point, exit_point, weight, -1)` (`Tunnel.lua:208`).
The 5th argument is a unit-class mask: `Dome_Entrance` passes `2` with the
comment *"usable by people only"* and `1` *"usable by drones only"*
(`Dome_Entrance.lua:15-16`), so `-1` is every unit type. The sentence describes
a restriction the code does not implement.

**(b) It also bridges LIFE SUPPORT, which the description omits** (the "unfiled
candidate" previously noted in STATUS, now folded in here). `TunnelBase`'s
parents include **`LifeSupportGridObject`** (`Tunnel.lua:6`); it creates the
elements (`CreateLifeSupportElements`, `:178`), merges water grids across the
pair (`MergeGrids("water")`, `:88`), and registers itself on the water supply
connection grid (`:112-121`). So the tunnel joins water/life-support networks as
well as tracks and power — a genuinely useful property a player would want to
know and cannot learn from the text.

**Intent — UNINTENDED, hard tell: self-contradiction** between shipped text and
shipped code, with half of it now confirmed at the keyboard. **Reachability R1** —
build-menu and encyclopedia text, read by any player evaluating the building.
Player consequence is a real planning error in both directions: they avoid the
tunnel for rover routing when it would work, and they never learn it can carry
life support.

**⚠️ The fix is NOT free — this is why it is a user decision.** FIX_POLICY §6:
the pack ships **no localization tables**, and new player-visible strings must
use `Untranslated(...)`. Replacing this `T` therefore **converts a fully
localized description into English-only** for every language. That is a
regression for non-English players in exchange for correcting English text.
Options:
1. **Replace the whole description** with a corrected `Untranslated` string.
   Accurate, but English-only everywhere. Precedent exists (F25 is a description
   defect), but F25 should be re-checked for how it handled loc before this is
   treated as settled.
2. **Do nothing in game text; document it** in MOD_DESCRIPTION as a known vanilla
   text error. Zero localization cost, zero risk, no in-game benefit.
3. **Ship it only if D10 lands**, since D10's T1 is already a batch of workshop
   description repairs — one localization decision covering all of them rather
   than two separate calls.

**Recommendation:** decide it together with D10's T1 text repairs; they raise the
identical tradeoff and should not be answered twice differently.

### F85 — Breakthrough choice popups and the Assembly "Colony Values" choice ride real-time waiters; any save landing in their open window silently voids the choice (P3, LATENT — tier U)  `[filed 2026-07-30 by the popup audit — NOTHING BUILT, settling observation queued; no fix until U resolves]`

The F83 family's latent members — found by the popup/deferred-consequence audit
(`docs/reports/POPUP_CONSEQUENCE_AUDIT.md` §3.3, which is the full evidence; this entry
is the record of claim). Four popups carry heavyweight consequences in code
that runs **after** a `WaitPopupNotification` inside a **real-time** thread —
the thread class that does not survive a save/load:

- **`ShowBreakthroughChoicePopup`** (`Anomaly.lua:696-714`,
  `CreateRealTimeThread` :703): after the wait,
  `UIColony:SetTechDiscovered(techs[res].id)` (:708) + the caller's callback —
  **the breakthrough discovery itself**. Three callers/presets: subsurface
  anomaly (`Anomaly.lua:393`), planetary anomaly (`PlanetaryAnomaly.lua:268` —
  the anomaly is already consumed, `DoneObject` :351), and the Breakthrough
  law (`LawDef-Research.lua:78`).
- **`AssemblyChoicePopup`** (`Factions.lua:1191-1236`, spawned
  `CurrentMap:CreateRealTimeThread` from `AssemblyBase:GameInit`,
  `MartianAssembly.lua:8`): after the wait, `ApplyAssemblyChoice` (:1214) —
  faction weights, initial laws, colonist standings, `ElectMembers()`. The
  **entire politics initialization**; `GameInit` never re-runs, so a lost
  choice would leave the Assembly built and the politics system dead.

**Why this is latent rather than live — the modal shield.** All four presets
open immediately (`start_minimized = false`), modal + input-suppressed +
game-pausing (`PopupNotification:Init`). No autosave can fire (game time is
paused) and the quicksave shortcut (Ctrl-F9) is eaten by the popup's
`OnShortcut`. So in ordinary play **no save can exist inside the window**, and
loading any older save replays the trigger. The shield is UI reachability, NOT
the save system: `CanSaveGame` has no popup clause, and Quick Save is
`ActionBindable` while `PopupPropagateShortcuts`
(`MarsMessageQuestionBox.lua:1-9`) lets **F9 and F11 through the modal layer**
— a player who rebinds Quick Save onto one of those keys can produce the
poisoned save. **Settling observation (needs-eyes item 3 in the audit):**
rebind Quick Save to F9, open any choice popup, press it — if a save lands,
this is R2-by-rebind and worth an owner decision; if the binding or save is
refused, this drops to I/R4 and stays documentation.

**Intent — unintended (sibling contradiction):** every subsystem that carries
real consequences through a popup wait (challenges, storybits, sequences,
status-effect popups) waits in a **game-time** thread, which the engine
persists by default (ENGINE_FACTS); these sites chose the one thread class the
persist machinery cannot save. The modal shield makes the choice harmless
today, which is why this files at P3/U rather than P2.

**Also folded in here (audit §3.6, R3-edge, no fix proposed):** the game's one
`dont_pause` popup — the distress-call confirmation
(`RivalColonies.lua:535-555`) — is the only popup window where the game runs,
so a sol-change autosave can land under it. That save loses only the popup
itself (nothing is committed before its wait — self-healing, harm ≈ 0), but any
async popup **queued behind it** at that moment (including a storybit's, which
has no corner notification to resurrect it) is dropped from `g_PopupQueue`
with its game-time waiter left blocked forever — event lost, `g_StoryBitActive`
ghost, a non-OneTime storybit dead for that colony. Requires the player
mid-distress-flow at the exact autosave tick with a second popup queued —
recorded for completeness.

**No fix ships on this entry until the observation runs** (revised-§4
discipline: a U tier authorizes an observation, not a build). If it proves
real, the audit's §7.3 names the shape: move each consequence into a game-time
thread and let the real-time side only present UI — per site, no shared-
machinery surgery.

### F86 — OUR OWN DEFECT: pack code blocked on a persisted game-time thread is written INTO the player's savegame and keeps running after the mod is removed (P1, MEASURED)  `[open — filed 2026-07-31 by PT-20; blocked release when filed, gate now PER-SITE (2026-08-01, see below). Remedy DECIDED 2026-07-31 (owner, all four calls): layer ordering 3→2→1 adopted into FIX_POLICY §3a; F02 held for it; D10/D12 sequenced behind it. ~~layer-3 sweep authorised and OWED … Nothing built yet~~ — heading tag REFRESHED 2026-08-01, it had gone stale against the index row: the sweep RAN and reported (membership corrected both ways), the remedy was ADJUDICATED twice and benchmarked by the prior-art survey, and the plan of record is `F86_EXECUTION_PLAN.md`, now executing as project chain prompts 2→5 (Phase 0 measurements → Tier-1 spec → Tier-1 build → Tier 2). **REFRESHED AGAIN 2026-08-01 (prompt 4b), it had gone stale a second time — "still nothing BUILT" is dead: ✅ TIER 1 IS BUILT AND VERIFIED, all four units shipped and all five legs run, F02/F78/F81/F88 flipped to `tested`, Site 1 repaired. Site 2 (`Opt_DroneOverhaul`) still leaks and is Tier-2 work. The release gate is now PER-SITE (owner, 2026-08-01) and every reachable repair is built NOW rather than deferred to the cleaner — see the index row and FIX_POLICY §3a**. **REFRESHED A THIRD TIME 2026-08-01 (prompt 5): ✅ TIER 2 IS BUILT — Site 2 repaired, all four modules on synchronous seams, dispositions recorded. **✅ AND VERIFIED — PT-58 ran 2026-08-01 with the owner at the keyboard and F86 SITE 2 IS CLOSED: zero `Opt_DroneOverhaul` orphan errors against leg 5's 80, over an article carrying 73 idle drones. Both proven leak sites repaired and verified; the D10/D12 unhold is recorded**]`

> ## ⚖️ ADJUDICATED 2026-07-31 — `docs/reports/F86_ADJUDICATION.md` — read alongside this entry
>
> The two position documents were independently torn down against Src, `Code/`
> and the PT-20 logs. **Verdict: the authorised build is right,
> yes-with-changes.** What the adjudication corrects in THIS entry:
> - **"Synchronous code can never be captured" is true of the thread-stack
>   route only.** The full test is value-reachability (three routes); a mod
>   function held in a live local of a captured ENGINE frame also enters the
>   save. Concrete: `Fix_CaveInsNoDisasters` is capturable today (~1 in 9
>   Underground-map saves; inert — layer-2 shape; no build needed), so the
>   exposed set is **at least 13**, and the sweep's enumeration grep is proven
>   blind to slot/global/preset assignments.
> - **`Fix_BombardmentSpread`'s accepted residual was mis-stated** — not "one
>   broken volley" but a permanently wedged Mystery-7 bombardment loop
>   (untimed `WaitMsg("BombardEnd")`, `Mystery 7.generated.lua:942`). Owner
>   re-decision owed.
> - **Before Tier 1 is built**, one engine fact must be measured (does
>   `CreateGameTimeThread` run the body before the creating statement
>   continues?) — it gates both the F02 wrapper key and the entire rains
>   wrapper design — and the rains repair needs a migration pass for existing
>   saves' persisted `fixed_loop` threads.
>   **✅ MEASURED 2026-08-01 (F86 Phase 0, chain prompt 2, owner at the keyboard;
>   log `Mars.exe-20260801-14.59.57-6a22b86d.log`; ENGINE_FACTS carries the full
>   record): it DEFERS.** Two forms, the second creating the GT thread *from a GT
>   thread* and confirming the outer's `WaitMsg` actually received the inner's
>   `Msg` — the vanilla shape, so the answer is measured rather than generalised
>   off the console-context form. **The rains wrapper design is viable as
>   authorised (no synchronous-heal fallback), and the F02 wrapper's
>   defer-when-`_G.Meteors`-falsy guard is NOT load-bearing** — it is kept as
>   defence in depth. The migration pass is unaffected and still owed.
>   The same sitting closed the autosave leg of the save hook
>   (`SaveGameStart`/`SaveGameDone` fire with `autosave=true err=false`).
> - The per-load meteor restart (`Fix_MeteorFrequency.lua:187-197`) is
>   confirmed as a shipped player-facing defect; recommendation: own F-number,
>   fixed by the F02 rewrite via a one-shot latched heal (shipped precedent:
>   `RefreshRainsLoops`).
>
> **ROUND 2 (same day, `F86_ADJUDICATION.md` §8):** the orphan-env probe
> (measured) corrected the harm model — orphans resolve vanilla globals and
> die only on mod-created names, so **rains harm INVERTS** (uninstall keeps
> our loop forever, silently — save-integrity harm, not lost rains), the
> **Bombardment residual shrinks to ≈nothing** (the body is mod-name-free; a
> mid-volley orphan completes and `BombardEnd` posts — no Mystery-7 wedge),
> and the Tier-3 residuals shrink (three of four orphans end silently by
> themselves). The save/load **hook surface is now enumerated in
> ENGINE_FACTS** (PersistPostLoad carries `data`; CanSaveGameQuery exists and
> is barred). The layer-1 bar is restated as gated, not permanent — four
> named gates in §8.5. Verdict unchanged: yes-with-changes, same build, plus
> a version-stamped migration marker and id-less-entry handling for the rains
> pass (measured on the `test 2i` fixture).
>
> ## ✅ THE OWNER DECISION IS TAKEN (2026-07-31) — read this before the diagnosis below
>
> All four calls in `docs/reports/SAVE_SAFETY_REDESIGN.md` §4 were answered. **No
> measurements are owed and none may be designed** (see the cancelled tail-call
> experiment below). What is owed is **one game-free source sweep.**
>
> 1. **Layer ordering 3 → 2 → 1 — ADOPTED**, and it is now a hard rule in
>    **`FIX_POLICY.md` §3a**, binding on new fixes as well as repairs. That
>    section, not this entry, is the authoritative statement.
> 2. **The layer-3 sweep — AUTHORISED, full scope** (all full-replacement
>    modules, not just the 12 exposed). Game-free.
>    ✅ **RAN 2026-07-31 over the exposed set — result in
>    `SAVE_SAFETY_REDESIGN.md` §5.** Headline: **five of the twelve have a
>    layer-3 or layer-2 route out** (`MeteorFrequency`,
>    `DroneUnreachableForever`, `TrainWaitTime`, `RainsDeadlock` fully;
>    `ArrivalDeaths` by half), each via an input verified **synchronous**. Only
>    **four own-thread modules plus `BombardmentSpread`** are layer-1 candidates,
>    and `BombardmentSpread` has **no** layer-3 route (its defect is a discarded
>    local mid-function).
>    ✅ **The non-exposed half ran too — all 22 modules (§5.4).** 6 convert
>    cleanly to a chained wrapper, 4 have a route worth designing, 9 are
>    correctly full replacements, 3 are already optimal. **Decision 2 is
>    discharged; nothing further is owed on the sweep.**
> 3. **F02 — HELD until the sweep reports.** Do **not** touch
>    `Fix_MeteorFrequency`; the owner declined to take it module-by-module and
>    wants the layer-3 set to land as one designed change. Accepted cost, stated
>    at the time: the measured colony-killing leak stays shipped meanwhile.
> 4. **D10 and D12 — sequenced BEHIND the rules.** Neither approved build starts
>    until save safety is settled; both touch colonist assignment, which is
>    command-thread territory. The board's "confirm owner intent" on those two
>    items is answered: **not yet.**
>
> ⚠️ **A correction to this entry's own worked example landed with the
> decision.** The F02 wrapper must key on **`CurrentThread()`**, not on the
> meteor descriptor — `Meteors.lua:279` (the `Meteors` thread) and
> `Meteors.lua:326` (the **`MeteorStorm`** thread) pass the *same* descriptor, so
> descriptor-keying would fire the storm warning ~5 sols early instead of 6
> hours and make Sensor Towers irrelevant to it — a balance change barred by
> FIX_POLICY §4. Full enumeration of every call site, and a second smaller
> correction (the residual `Sleep(5000)` is ~10 game minutes, not zero), are in
> `SAVE_SAFETY_REDESIGN.md` §2 Layer 3.
>
> ⭐ **THE BUILD IS AUTHORISED (owner, 2026-07-31) — scope in
> `SAVE_SAFETY_REDESIGN.md` §6. Tiers 1 and 2; ⛔ LAYER 1 IS NOT TO BE BUILT.**
> The scope follows a severity tiering: exposure matters most where we
> **replaced a vanilla body**, because then uninstall leaves the player *worse
> than never installing* — as opposed to modules that **own their thread**, where
> the only cost is one log line for a fix the player just removed.
> - **Tier 1 (build first)** — `Fix_MeteorFrequency` (**measured**: meteors stop
>   permanently) and `Fix_RainsDeadlock` (**same shape, not previously called
>   out**: we replace the *global* `RainsDisasterLoop`).
> - **Tier 2** — `Fix_DroneUnreachableForever`, `Fix_TrainWaitTime`,
>   `Fix_ArrivalDeaths` half (b); plus `Opt_DroneOverhaul` ⛔ **blocked on the
>   drone carve-out**.
> - **NOT built** — the four own-thread modules and `Fix_BombardmentSpread`
>   (which has no layer-3 route at all). Accepted residual.
> - ~~**⚠️ `Fix_ArrivalDeaths` half (a)** — the raw `SetPos` with no passability
>   search — **has no route yet** and needs a design pass.~~ **→ DESIGN PASS RUN
>   2026-08-01 (chain prompt 5) AND IT FOUND A ROUTE, so it was built:** the fix
>   never needed to change `pos`, it needs the colonist to *end up* walkable, and
>   `Colonist:OnArrival` is a verified-synchronous, arrival-specific seam running
>   after the placement. Layer 3, no residue.
> - **F02's hold is LIFTED**; ~~D10/D12 stay held **until these repairs land**~~
>   **→ ⭐ D10/D12 UNHELD 2026-08-01.** The owner's condition was "repairs land
>   AND verify". Tier 1 landed and verified (five legs, `c6180ad`); Tier 2 landed
>   and verified (PT-58 PASS, F86 Site 2 closed at zero against leg 5's 80).
>   **Both D10 and D12 are runnable now** — chain prompts 9 and 10.
> - ⚠️ The tiering is **reasoned from the measured mechanism, not measured**.
>   The control, if ever wanted, is one PT-20-method leg against an own-thread
>   module.
>
> ⚠️ **THE EXPOSURE LIST IS 13, NOT 12 — corrected by the sweep the same day.**
> An earlier certification on this entry said "no 13th site"; it is
> **WITHDRAWN**. **`Fix_DroneUnreachableForever` is exposed**: it replaces
> `Drone:ApproachWrapper`, whose `building:DroneApproach(...)` call blocks (every
> implementation ends in `Goto`/`GotoBuildingSpot`/`EnterBuilding`, and
> `Unit:Goto` loops on `pfSleep`), it runs on drone **command** threads
> (`Drone:Work`/`PickUp`/`Deliver`/`EmergencyPower`), and **lines 52-77 of our
> replacement run after the blocking call** — the same layer-2 violation that was
> *measured* leaking in `Opt_DroneOverhaul:188-190`. Disposition: **layer 2**,
> and an easy one. Three earlier checks missed it because the module installs
> through an **alias** (`local D = Drone`) **indented inside `apply()`**, and it
> contains no yield of its own — it blocks through a callee. Full detail, the
> reliable enumeration method, and the ten other modules the sweep cleared:
> `SAVE_SAFETY_REDESIGN.md` §4a.

> ## ✅ THE ENUMERATION RE-RAN 2026-08-01 (F86 Phase 1, chain prompt 3) — all five assignment shapes, re-derived over the current `Code/` (post-F49(a)-strip), NOT inherited. **The durable list is the expected 13, plus one newly CLASSIFIED route-(c) site.**
>
> **Method:** alias-blind extraction of everything `Code/` assigns in each of
> the five shapes (class-method incl. aliased/indented defs; table-slot;
> global assignment incl. `SMRFixPack.SetGlobal`; preset-field; own-thread),
> then every extracted target run through `tools/blocking_analysis.py`
> (primitive-seeded, unambiguous-callee propagation — 15,106 names, 633 direct
> yielders) and every BLOCKS/AMBIGUOUS verdict resolved BY HAND against the
> specific class we patch. **Durable list and dispositions:**
>
> | # | module | shape | exposure | disposition |
> |---|---|---|---|---|
> | 1 | `Fix_MeteorFrequency` | table-slot (`GlobalGameTimeThreadFuncs.Meteors`) + persisted named GT thread | body IS a blocked GT thread body | **Tier 1 — rewritten** (spec §6.2a-A) |
> | 2 | `Fix_RainsDeadlock` | global assignment (`RainsDisasterLoop`, direct yield) + own threads via `RefreshRainsLoops` | persisted loops run our body | **Tier 1 — rewritten** (spec §6.2a-B, C34 rider) |
> | 3 | `Fix_ArrivalDeaths` | class-method (`Colonist:Arrive`, direct yield) | command body, yields | Tier 2 (half (b) layer 3; half (a) design pass owed) |
> | 4 | `Fix_TrainWaitTime` | class-method (`Colonist:BoardVehicle`, blocks via `PlayPrg`) | command body | Tier 2 (layer 3 via `AddSpentTime`) |
> | 5 | `Fix_DroneUnreachableForever` | class-method (`Drone:ApproachWrapper`, blocks via `DroneApproach`) | mod code after the blocking call | Tier 2 (layer 3 via consumer `CleanUnreachables`) |
> | 6 | `Opt_DroneOverhaul` | class-method (`Drone:Idle` wrapper) | **measured leak** — work after the call | Tier 2 (layer 2; carve-out granted) |
> | 7 | `Fix_BombardmentSpread` | global assignment (`WaitBombard`, direct yield) + own GT thread (`:137`) | replaced blocking body | NOT built — residual ≈ nil (round-2 measured; mod-name-free body completes the volley) |
> | 8 | `Fix_MeteorStormWedge` | own GT thread (`:119`, `StormWedgeHeal`) | mod-owned thread | Tier 3 accepted; **orphan-gate reorder specced** (§6.2a-D) |
> | 9 | `Fix_CrystalMysteryHang` | own GT thread (`:44`) | mod-owned thread | Tier 3 accepted (expires at frozen deadline) |
> | 10 | `Fix_ExtenderFlapChurn` | own GT thread (`:77`) | mod-owned thread | Tier 3 accepted (one-shot, completes silently) |
> | 11 | `Fix_TrackConnectorPingPong` | own GT thread (`:156`) | mod-owned thread | Tier 3 accepted (one-shot) — its `Done` wrapper's post-`orig` reclaim verified behind a **non-blocking** chain (see below) |
> | 12 | `Fix_ShelterReflex` | class-method (`Colonist:Idle` wrapper) | tail-return over a blocking body | compliant — no work (§4.5 accepted residual) |
> | 13 | `Fix_CaveInsNoDisasters` | table-slot (`info[FUNC]` into the engine's periodic-repeat entry) | route (b) — live engine local | compliant — no work (inert, layer-2 shape) |
> | +1 | `Fix_LastTransmissionStorage` | **preset-field** (`like.Condition.eval`, `:134`) | **route (c) — CONFIRMED 2026-08-01** by the §4.4 closure: `RecalcFactionsApproval` stores `likes_data` (entries carry `like = like_def`) into `g_FactionsHolder`, a **GameVar** (`Factions.lua:196/:659`), and preset permanents cover **roots only** (`CommonLua/Preset.lua:1362-1394`) — the sub-object and our closure serialise by value, precisely when a patched entry evaluates non-zero | **compliant/inert — no build.** The persisted copy is never invoked (consumers read plain fields; fresh evaluations use the live presets), and even if invoked it touches only vanilla names + own plain upvalues. Named, bounded, disclosed (§3a residual class) |
>
> **No non-compliant 14th** — the stop condition did not fire. Notable
> hand-resolutions, so the next re-run does not repeat them: the analysis
> tool's verdicts merge ALL same-name defs and count yields inside nested
> closures, so four of its BLOCKS flags were false for the class we patch —
> `MirrorSphereBuildingBase:StartAction` (its `WaitWakeup`s live in a
> vanilla-spawned inner thread; the outer body is sync),
> `RCTransport:InteractWithObject` (the blocking `AssignTrain` caller is
> `Station:InteractWithObject`), and `Fix_TrainsToVoid`/`Fix_TrackTunnelPowerBridge`
> (their pre-work `Train:DestroySilent` calls are **synchronous by
> construction** — it forces `demolishing_countdown = 0` immediately before
> `DoDemolish`, skipping the only yielding branch; zero yield primitives in
> the whole of `Track.lua`/`Tracks.lua`/`TrainTransport.lua`/`StationsLink.lua`).
> Everything else `Code/` assigns resolved clear (sync bodies, UI surfaces,
> class-table/permanent stores, `OnMsg` registrations, or RT threads — safe by
> construction).

**This is a defect in this pack, not in the game.** Found by executing PT-20's
mandatory step 5 for the first time. It is measured, not inferred, and it
reproduces identically whether the pack is *disabled in the Mod Manager* or
*physically removed from disk*.

**Mechanism.** A savegame captures every game-time thread **together with its
blocked stack** (ENGINE_FACTS). A mod function is not in
`PersistGatherPermanents`, so it is serialised **by value** — bytecode, upvalues
and all — not by name. Each mod's environment is registered as a permanent
(`Mod.lua:1642-1644`, `permanents["Mod/" .. mod.id] = mod.env`); with the mod
gone that permanent cannot resolve, and unpersist substitutes a fallback table:

```
Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback permanent: table: … [7]
```

The orphaned function therefore comes back **runnable**, with its `_ENV` replaced.
~~so every global lookup inside it — `SMRFixPack` included — resolves to
nothing.~~ ⚠️ **CORRECTED 2026-07-31 (orphan-env probe, measured with a clean
control):** the fallback is a fresh `LuaModEnv{}` whose metatable falls through
to the real `_G` (`Mod.lua:1647-1656`), so **vanilla globals resolve — an orphan
loses ONLY names its own mod creates**. `SMRFixPack` is nil after uninstall
because the pack never loaded to create it. Whether an orphan dies, expires, or
runs forever is a per-module property of the names its body touches
(ENGINE_FACTS; `docs/reports/F86_ADJUDICATION.md` §8.1-8.2). Both measured legs are
consistent: `Fix_MeteorFrequency` died at `SMRFixPack` (mod name);
`Opt_DroneOverhaul`'s wrapper died at its `SMRFixPack` gate — while
`Fix_RainsDeadlock`'s all-vanilla `fixed_loop` would run forever.

**The test that found it.** `PT-20TEST`, cut from the 288-sol `test 2i` colony.
The meteor descriptor's `spawntime` was compressed to 2 h and the thread
restarted, so its next wake was bounded and known; saved at sol 290 with the
thread parked in `Sleep`. Loaded with the pack gone.

**Site 1 — `Fix_MeteorFrequency`, the global `Meteors` game-time thread.** The
thread arrived **alive**, finished vanilla's `MeteorsDisaster`, returned into our
frame and died:

```
[LUA ERROR] attempt to index a nil value (global 'SMRFixPack')
  Mod/SMR_CommunityFixPack/Code/Fix_MeteorFrequency.lua(106):   <>
Locals:
   meteors | object MapSettings_Meteor 'Meteor_Low'
   spawn_time | number 60000      <-- the values WE injected before saving
   hit_time   | number 60000
```

The locals are conclusive: that stack frame, with its local variables, came out
of the savegame. **Player harm: the colony never gets another meteor.** It does
not self-heal — a save written after the death carries the dead thread, and
`_fixup.lua:54-55` only rebuilds a global GT thread when the save carries
*nothing* for that name (confirmed on a second save, `IsValidThread` returns no
value on load).

**Site 2 — `Opt_DroneOverhaul`, drone command threads.** 98 errors per short
session, `Opt_DroneOverhaul.lua(96)` ← `(190)` ← `sprocall` ←
`CommandObject.lua(246)`. Harm is log noise only: line 188 calls
`orig_idle(self)` first, so vanilla's `Idle` completes before line 190 throws,
and drones behave normally (observed at the keyboard). **Two things this proves
that matter more than the noise:** the module's own **opt-in toggle was OFF**
(the wrapper installs at file scope and only early-returns), so *any save made
while the pack is merely installed carries pack code; and it reached the save
through a **class-table** write (`Drone.Idle`), which the 2026-07-31 audit had
cleared as safe.

**🔁 RE-MEASURED 2026-08-01 (Tier-1 leg 5, the PT-20-method uninstall; log
`Mars.exe-20260801-19.14.11`, test-2 lineage, owner at the keyboard).** Site 2
is **unchanged and still leaking** — Tier 1 did not touch this module
(`Opt_DroneOverhaul.lua` is untouched since `89bd463`, pre-Tier-1), and the
signature reproduced byte-for-byte: `Opt_DroneOverhaul.lua:96: attempt to index
a nil value (global 'SMRFixPack')`, chain `(96)` ← `(190)` ← `sprocall` ←
`CommandObject.lua(246)`. **80 errors** this sitting (vs the 98 recorded above
— the count tracks how many drones happened to be mid-`Idle`, not severity).

**New this leg, and not previously recorded: the leak is FIRST-LOAD-ONLY and
self-clears.** All 80 errors fall inside the first load of the uninstalled save
(within ~2 s, Lua `0:00:26.493`→`0:00:26.7xx`), and a save-and-reload of that
same save produced **ZERO** — the erroring commands abort, vanilla re-issues
`Idle` on its own body, and the persisted pack closures are gone from the save
from then on. So the player-visible harm is one burst of log noise on the first
load after uninstalling, not an ongoing condition. **This does not make the site
compliant** — `[LUA ERROR]`s naming pack code after removal is exactly what F86
forbids, and the burst still lands in the log the player would send us — but it
bounds the harm and tells the Tier-2 fix what it has to beat.

The rest of leg 5 corroborates the diagnosis: with the pack disabled, drones
behaved normally throughout ~15 minutes of ordinary play (build, salvage, a sol,
save+reload), and `SMRTest.FixtureCarry()` found the drone GameVars **absent**
(`SMRFixPack_DroneSpeedDial`, `SMRFixPack_DroneCarryDial`) — the residue is the
in-flight command closures, nothing declarative.

~~**Disposition unchanged: Tier 2 (layer 2; carve-out granted), chain prompt 5.**~~
Confirmed with the owner 2026-08-01 during the Tier-1 close-out, which recorded
the observation and routed it rather than acting on it.

**⭐ REPAIRED 2026-08-01 (chain prompt 5, Tier 2) — and the shape beats what the
spec asked for.** §6.2 called for layer 2 ("move moonlighting out of the command
body"); what landed is a layer-3 class seam. The moonlight hook moved off
`Drone:Idle` and onto vanilla's own **last statement in the fall-through**,
`self:CleanUnreachables()` (`Drone.lua:640`), gated on `self.command == "Idle"` —
which selects that call site and not the two inside `Deliver` (`:1247`) and
`PickRechargeStation` (`:1287`). `Drone:CleanUnreachables` is **verified
synchronous** (`:879-896` is a `pairs` walk plus `GameTime()`;
`tools/blocking_analysis.py` reports it `clear`), so the frame now exists only
during synchronous execution and route (a) is closed outright rather than made
inert. Part 1's `TaskRequestHub:FindTask` wrapper was checked in the same pass and
is already on a synchronous C-backed seam (`_TaskRequest.lua:72-83`, `clear`), so
after this move the module has **no frame that a save can capture at all**.

**It is a call-position move and nothing else** — vanilla has literally no
statement between `self:CleanUnreachables()` and the end of `Idle`, so the trigger
condition, the ordering and the code that runs are unchanged, and no drone-design
judgement was needed. That was the exact limit of the owner's pre-granted
carve-out (chain README, and the DRONE_PROJECT_PROMPT 2026-08-01 addendum).

The module header's old **"Saves made with the module enabled load identically
without it"** claim was FALSE and has been corrected in place rather than quietly
dropped — Site 2 is the counter-example, and the header now carries the
measurement and the repair.
**Disposition (FIX_POLICY §3a per-site gate): REPAIRED IN-PACK — layer 3, no
residue, nothing owed to D13.**

**✅ SITE 2 IS CLOSED — VERIFIED 2026-08-01 (PT-58, owner at the keyboard).**
Uninstall log `Mars.exe-20260801-21.54.16`, same lineage and map as leg 5
(`HdmSxGs6kyd0uz6-`, `BlankBigCanyonCMix_09`), article `T2-UNINSTALL` cut from
`test 2i`. **ZERO `Opt_DroneOverhaul` lines. Leg 5 read 80 on this exact shape;
the first measurement was 98.** Zero `[LUA ERROR]` of any kind in the whole
session, and zero mentions of any other Tier-2 module.

**The fixture behind the zero, because a zero is only worth its denominator:
73 drones in command `Idle` at save time** (`SMRFixPack.DroneReport()` summed
over eleven hubs) — the same population that produced 80 last time. The
uninstall was genuine, not a half-disable: zero `[CommunityFixPack]` lines
anywhere, with `Unpersist missing permanent: Mod/SMR_CommunityFixPack` at Lua
`0:00:19` and `0:02:21`. **Leg 5's 80 errors landed at Lua `0:00:26`, inside
that first window.** A pack-written save was loaded twice, plus a save+reload,
across 10:08 of session — all clean, so there was not even the one-load
self-clearing burst this entry recorded above. Full reading: `PT-58`.

⚠️ **One thing the leg did NOT establish, recorded rather than glossed:** every
hub reported `unclaimed=0` and the module reported `moonlighted=0 vetoed=0`, so
the `self.command == "Idle"` gate had no opportunity to fire and is **untested
by this leg**. The save-safety claim does not depend on it — the frame is
uncapturable whether the gate fires or not — but D06 part 2's *functionality* is
unverified here. Its home is the frozen PT-52, not a save-safety sitting.

**What this overturns.** The audit asked *where is the function stored* and
cleared class tables ("restored as permanents by name") and UI windows. That is
true of the table and irrelevant to the outcome — the route into the save is a
**thread stack**. The correct test is:

> **Can this function be executing, or blocked, below a yield
> (`Sleep`/`WaitMsg`/`WaitWakeup`) on a GAME-TIME thread when the save is
> written?**

A save captures only *blocked* threads, so synchronous code — data patches,
getters, UI handlers, `Can…` predicates — can never be captured **through the
thread-stack route**. That bounds that route: **~62 of 74 modules are safe from
it by construction** *(adjudication 2026-07-31: capture is value-reachability —
see the box at the top of this entry; the stored-closure and live-local routes
also exist, and one compliant module is capturable today).*

**Exposure list (12 modules — membership corrected BOTH ways by the sweep 2026-07-31: `Fix_DroneUnreachableForever` ADDED, `Fix_TrainCargoDumping` REMOVED because `Train:UnloadAll` is fully synchronous. See the correction box above and `SAVE_SAFETY_REDESIGN.md` §5.2).** Proven: `Fix_MeteorFrequency`,
`Opt_DroneOverhaul`. High, same shape, unmeasured — all default-active:
`Fix_RainsDeadlock` (its `fixed_loop` is written to the global
`RainsDisasterLoop` and is blocked in our body nearly always),
`Fix_ArrivalDeaths` (`Colonist:Arrive` command + its own `Sleep`),
`Fix_TrainWaitTime` (`Colonist:BoardVehicle`), `Fix_TrainCargoDumping`
(`Train:UnloadAll`), `Fix_BombardmentSpread` (replaces the blocking
`WaitBombard`). At risk while their own threads live:
`Fix_MeteorStormWedge`, `Fix_CrystalMysteryHang`, `Fix_ExtenderFlapChurn`,
`Fix_TrackConnectorPingPong`. **Compliant, and NOT to be measured:**
`Fix_ShelterReflex` — it wraps `Colonist:Idle` but ends
`return orig_idle(self, ...)` with nothing after it.

> ⚠️ **An earlier draft of this entry said `Fix_ShelterReflex` "must be
> measured". Withdrawn 2026-07-31 — that measurement is IMPOSSIBLE, and the rule
> was restated so it is not needed.** A tail call has nothing after it, so a
> vanished frame and a surviving frame produce **identical silence**; any
> detector placed after the call stops it being a tail call. The experiment is
> unfalsifiable by construction and was cancelled rather than run.
> **The rule does not depend on it.** It was first justified as *"a tail call
> removes our frame from the stack"* — unobservable here, since the sandbox
> denies introspection. The sound form needs no engine guarantee:
> **no mod code after a call that can block** — then whether or not the frame is
> serialised, there is nothing left to execute after removal. By that test
> `Opt_DroneOverhaul:188-190` violates it (measured leak) and
> `Fix_ShelterReflex:73` complies. Residual, accepted: an inert serialised
> function may sit in a save as dead weight; it executes nothing and no read
> available to us can see it.

**The defence the pack already tried, and why it failed.** Both leaking files
say in their own headers that avoiding upvalues makes the thread safe —
`Fix_MeteorFrequency:51-54` ("the persistence shape the engine has already
proven it handles") and `Fix_RainsDeadlock:51-52` ("threads suspended inside it
persist **by the global name** this function is written to"). Persist does not
resolve mod functions by name. Avoiding upvalues only made the serialised
function smaller.

**Remedy — three layers, ordering ADOPTED 2026-07-31 (owner), nothing built yet.
The rule is `FIX_POLICY.md` §3a; the full spec and per-module disposition table
are `docs/reports/SAVE_SAFETY_REDESIGN.md`.**

1. **Patch a synchronous input instead of replacing a blocking body** (best;
   zero savegame footprint). Worked example for F02 below.
2. **Tail-call rule for wrappers** — do all work *before* the call and finish
   `return orig(...)`; never work after a call that can block. Move genuine
   post-work (D06's moonlighting) out of the command body into a message hook.
3. **`OnMsg.SaveGameStart` tear-down / `SaveGameDone` rebuild** for what 1 and 2
   cannot reach. **This is newly possible — see the ENGINE_FACTS correction: the
   "mods get no save hook" fact was wrong.** ⚠️ **Trap:** autosaves are the same
   `DoSaveGame` path (`Savegame.lua:1450-1453`, one flag), so they fire roughly
   once a sol; a tear-down that *restarts* a loop would reset a 35–115 h meteor
   timer before it ever expired — reintroducing PT-01's permanent-silence
   signature from our own code. Any tear-down must **re-arm from a persisted
   deadline**, never restart blind.

**Worked example — F02 needs no body at all.** Vanilla's interval is
`Min(spawn_time, warning_time)` (`Meteors.lua:291-292`). Wrap
`GetDisasterWarningTime` (a synchronous global, `MapSettings.lua:94`, never on a
blocked stack) to return `Max(orig, spawntime + spawntime_random)` for the meteor
descriptor; `Min` then equals `spawn_time` and **vanilla's own body** produces the
designed 35–115 h schedule. The PT-01 watchdog splits out as a second, also
save-safe module: vanilla emits `Msg("MeteorDone")` (`Meteors.lua:388`), so it can
time strikes from `OnMsg`, check `IsValidThread(Meteors)` on `NewDay`, and
`RestartGlobalGameTimeThread("Meteors")` — which now restarts *vanilla's* body.

**Controls run.** Junction physically removed (`1 mods installed`, Test Kit only)
reproduced the mod-manager result to the error count — 98 vs 98, same single
meteor error, same injected locals — the only difference being the engine's own
wording (`present, but not loaded` → `not present`). Steam verify / reinstall
rungs were judged unnecessary: no game-install state can invent our injected
`spawn_time 60000` inside our own function's frame.

**Not a defect (owner decision 2026-07-31):** single meteors' ~30-second
`Predict()` marker is adequate warning for the risk a single meteor poses.
Sensor towers extending single-meteor warning would be a **feature**, not a
repair, and is declined. See the F02 root-cause note for why towers currently
affect meteor *frequency* instead.

### F87 — OUR OWN DEFECT: `Fix_DustSicknessBiorobots` throws at apply on some load orders, silently leaving F40 unfixed (P2, OBSERVED)  `[fixed 2026-07-31 — repaired in the shared DataPatch scaffold; 3 further enable-path casualties found and repaired; FIX_POLICY + ENGINE_FACTS written. VERIFIED ON THE ENABLE PATH 19.09 (63/0/15/0, owner at the keyboard) and on a cold boot 18.44. The five Opt_ probes SKIPped there (toggles OFF) - coverage, not an open finding: the A2 claim is withdrawn, PT-55 answered it 2026-07-30]`

> ## ✅ WHAT LANDED 2026-07-31 (this entry's repair — read this before the diagnosis below)
>
> **The defect was in the shared scaffold, not in the one file.** `apply()` runs
> before class flattening on *every* path; the cold boot hid it because the
> presets are not loaded then either, so every pass returned early.
> `SMRFixPack.DataPatch` (`00_Core.lua`) now:
> - **runs nothing until `ClassesBuilt` has fired in this Lua load.** `g_Classes`
>   is not a usable test — a reload leaves the PREVIOUS build's classes standing
>   while the current ones are bare classdefs.
> - fires from **`ClassesBuilt` (the enable path's real trigger) / `DataLoaded`
>   (cold boot) / `ModsReloaded` (belt) / `DataChanged` (re-arm)**, all idempotent.
> - seeds `ctx.data_loaded` from the **engine's `DataLoaded` global**
>   (`Dlc.lua:51/:663`, `FirstLoad`-scoped so it survives a Lua reload) — without
>   it, a missing-target latch reads the enable path as "presets not loaded yet"
>   and never fires, which is the F75 gap through a different door.
> - **`pcall`s the pass.** `Msg` dispatches handlers through `procall`
>   (`cthreads.lua:20`), so a throw there is swallowed and the fix would go on
>   reporting `active` while doing nothing — the F87 failure mode with no log
>   line at all. It now reports `error`, logs, and C1 sees it.
> - `apply()`'s `patch()` call is kept as a **documented no-op**: a live Mod
>   Options re-apply happens long after `ClassesBuilt` and must do the work.
>
> `Fix_DustSicknessBiorobots` builds the filter with
> `PlaceObj("HasTrait", { "Trait", "Android", "Negate", true })` — the prop-list
> form the shipped data itself uses (`Data\StoryBit\DustSickness.lua:66-69`;
> `HasTrait` is a `Condition` and `Condition.StoreAsTable` is set false in
> `_fixup.lua:148-152`), and it fails soft where `:new` throws. The old guard
> tested `type(HasTrait) == "table"`, **which is true for an unflattened
> classdef — that is exactly why this shipped**; it now tests that the class is
> BUILT, and a `PlaceObj` refusal is counted and latched with its own reason
> instead of silently appending nothing.
>
> **Follow-up 1 (the sweep) — DONE, and it found three more.** All 75 files
> checked for both shapes. Constructor calls: 6 sites, every one at runtime
> inside a patched method or msg handler, none exposed. Preset patching: three
> sites hung off `OnMsg.DataLoaded` alone, outside the scaffold, each **silently
> dead for the whole session on the enable path** —
> **`Fix_TechDescriptionBuilding`** (the data patch itself; the description
> stayed wrong on every first run), **`Opt_MultipleSuns`** (the build-once limit
> lift; with the toggle already ON from account state the module ran half-live)
> and **`Fix_FirstAsteroidPrefabs`** (its preset self-check; it would have
> reported `active` on a preset it never verified). All three now use the new
> **`SMRFixPack.OnDataReady(fn)`** — DataPatch's trigger set without the
> latch/heal contract. One ordering trap documented at the call site: the global
> `DataLoaded` is set *after* `Msg("DataLoaded")` is posted, so the `DataLoaded`
> handler must call `fn` directly rather than test the flag.
>
> **Follow-up 2 (the rule) — DONE.** `FIX_POLICY` §2 carries the hard rule (no
> `apply()` may assume a cold boot; no class/preset construction at apply time;
> `OnMsg.DataLoaded` alone is not a sufficient trigger; both paths must be
> tested). `ENGINE_FACTS` carries the traced sequence so nobody re-derives it,
> plus the `procall` fact.
>
> **Follow-up 3 (the harness) — BUILT **AND RUN**, and it PASSED.** TestKit
> `Code/98_EnablePathLeg.lua`, armed like `96_AutoRunFlag`:
> boot with the pack OFF, the owner ticks it at the main menu, and the harness
> takes over from `ModsReloaded` — colony, full suite, quit. Recipe in
> `PLAYTEST_HELP.md`. **One click stays manual and cannot be automated:**
> `AccountStorage`, `SaveAccountStorage` and `ModsReloadItems` are all in
> `ModEnvBlacklist` (`Mod.lua:1270/:1279/:1392`) and there is no main-menu
> console, so nothing mod-side or console-side can flip the checkbox. The
> existing 78 probes are a real detector without any new probe: `FixMissing`
> FAILs any probe whose fix is not `active` (an `apply()` that threw) and the
> data-patch probes read live preset data (a patch that never ran).
>
> ### ✅ THE ENABLE-PATH LEG RAN AND PASSED — 2026-07-31 19.09 (owner ticked the box)
>
> **The first measurement this project has ever taken of a player's first
> session.** `fix pack present: 68/74 fixes active` → **63 PASS / 0 FAIL / 15
> SKIP / 0 ERROR** at 78 probes.
> - **Positive control on the leg's own premise:** the harness logged
>   `ENABLE-PATH: ARMED — the pack is OFF` at boot before the click, and
>   `ENABLE DETECTED — the pack loaded through an in-place mod reload` after it,
>   so this is provably not a cold boot. `95_AutoRun` logged `standing down`,
>   confirming the `-smrautorun` command line did not start a colony pack-less.
> - **The log carries the F87 fingerprint exactly** — two reload cycles in one
>   process, `Loaded mod items for: …TestKit` then `…TestKit, …CommunityFixPack`
>   — the same shape as the log that caught the defect, now with zero errors.
> - **The decisive probe:** `DustSicknessBiorobots` **PASS** — *"all 4 infection
>   effects filter Biorobots out"*. It reads the LIVE preset data, so it proves
>   the data patch actually ran on the path where `apply()` used to throw.
> - **Probe-for-probe identical to the cold-boot leg**, diffed: only 2 of 78
>   lines differ and both are RNG, not path — `CrystalMysteryHang` names a
>   different randomly generated mystery, `TouristApplicants` rolls 156/332 vs
>   160/312. Same noise profile (`objects_to_mark` 48, 2 `LawOfficeDoor`), zero
>   `[CommunityFixPack]` error/FAILED/disabled lines, no log line names our
>   `Code/`, 68 `applied` lines.
>
> ### ✅ AND AGAIN WITH EVERY OPTIONAL MODULE ACTIVE — 2026-07-31 19.24
>
> The 19.09 run had the toggles OFF, so all five `Opt_` probes SKIPped. Repeated
> with a temporary `Code/97_OptInLeg.lua` forcing `SMRFixPack_Optional` (the
> bridge overrides an OFF toggle and leaves account state alone):
> **`74/74` -> 68 PASS / 0 FAIL / 10 SKIP / 0 ERROR**, matching the all-ON
> cold-boot reference exactly, with all five optional-module probes PASSing on
> the enable path.
> - **A sweep repair caught in the act:** the log carries
>   `[CommunityFixPack] MultipleSuns: Artificial Sun build-once limit lifted`.
>   That line comes from `lift_build_limit()`, which on this path is driven ONLY
>   by the new `SMRFixPack.OnDataReady` — before today it hung off
>   `OnMsg.DataLoaded`, which never fires here, and the limit stayed in place.
>   `LastTransmissionStorage` and `IndependenceTerraforming` logging their own
>   pass lines likewise confirm the `DataPatch` scaffold ran on this path.
> - 74 `applied` lines, zero error/FAILED/disabled lines, same noise profile
>   (`objects_to_mark` 48, 2 `LawOfficeDoor`).
> - Temporary file and its metadata line deleted after the leg; the TestKit leg
>   is disarmed.
>
> 🔧 **TWO PROCEDURE FACTS LEARNED BY RUNNING IT** (both now in `PLAYTEST_HELP.md`):
> - **The leg's own click PERSISTS.** `ModsUIDialogEnd` calls
>   `SaveAccountStorage()` (`ModManager.lua:132`), so the pack is enabled in
>   account state from then on and **every** run must disable it again first. The
>   guard caught this rather than measuring a cold boot and reporting it as a
>   first-run result — it logged `ABORT — the fix pack was already enabled at
>   boot`.
> - **The first load-detector was wrong.** It read the `SMRFixPack` global, which
>   is rawset into the REAL `_G` and **survives a Lua reload**, so after the pack
>   was disabled it still looked loaded and the leg logged ABORT where it should
>   have logged ARMED. Now it reads `ModsLoaded`, which `ModsReloadItems` rebuilds
>   from scratch every reload. (It is the same survives-a-reload property the
>   leg's own SawPackOff marker relies on — which is why it could not also serve
>   as the detector.)
>
> 🛠 **CORRECTION, same evening — "this leg also verifies audit A2" was FALSE and
> is withdrawn.** That claim originated on this entry, was repeated into the
> prompt doc and STATUS, and was then restated as "A2 is still owed" after the
> toggles-OFF run — all on a premise nobody had re-checked. **A2 was already
> ANSWERED YES in play by PT-55 on 2026-07-30** (`PLAYTEST_ARCHIVE.md`: *"all
> three hooks install and run on a first mid-session enable, no relaunch"*, with
> per-module results), and the audit's own "one live confirmation still
> worthwhile" caveat was retired then. **A2's three are `Opt_ClassicRockets`,
> `Opt_ResidencyControl`, `Opt_MultipleSuns`** — not the set named earlier.
> A2 is also a **different path**: the MODULE toggle flipped mid-session, versus
> the PACK enabled at the main menu. So the all-modules-ON enable-path leg is
> **coverage, not the closing of an open finding.**
>
> **Cold-boot re-verification (2026-07-31 18.44, unattended, 78 probes):**
> `fix pack present: 68/74 fixes active` → **63 PASS / 0 FAIL / 15 SKIP / 0
> ERROR** — the current default-config reference exactly. 68 `applied` lines,
> `DustSicknessBiorobots: applied`, zero `[CommunityFixPack]`
> error/FAILED/disabled lines, no log line names our `Code/`, known noise only
> (`objects_to_mark` 48, 2 `LawOfficeDoor`, the TestKit GameInit nil-call pair).
> **This proves the repair did not regress the cold boot. It does NOT prove the
> enable path — only the leg above can.**

**Observed live 2026-07-31**, immediately after re-enabling the pack following
the PT-20 leg. The Phase-4 **C1 update-deactivation dialog** raised it at the
pregame menu — *"1 of this pack's fixes found that the game code they patch has
changed … Switched off: DustSicknessBiorobots"* — and the log gives the real
cause:

```
[CommunityFixPack] DustSicknessBiorobots: FAILED to apply:
  Mod/SMR_CommunityFixPack/Code/Fix_DustSicknessBiorobots.lua:73:
  attempt to call a nil value (method 'new')
```

Status is **`error`** (the `pcall` in `run_apply` caught a throw), not
`inactive` — so this is a crash, not a self-check latch. The C1 dialog's wording
("the game code they patch has changed") is therefore **misleading for this
case**; see the second follow-up below.

**Mechanism — the third instance of the F64 pre-flattening trap.**
Line 73 is `filters[#filters + 1] = HasTrait:new{ Trait = "Android", Negate = true }`.
The guard at `:90` only tests `type(rawget(_G, "HasTrait")) == "table"`, which
passes: the class table exists during file scope, but **it has not been flattened
yet, so `HasTrait.new` is nil**. Precedents: F64 itself, and D09's module
tripping the same trap on `Modifier.new` (2026-07-29). Three occurrences makes it
a pattern, not an incident.

**TRIGGER PINNED — and it is the path EVERY PLAYER TAKES ON THEIR FIRST RUN.**
(Two earlier drafts of this entry were wrong: the first blamed mod load order,
the second described it as a mid-*session* enable. Owner correction: the mod was
ticked **at the main menu**, and a mod is *never* auto-enabled — Workshop,
Paradox or local, the player always flips it on themselves, and the main menu of
the session they just launched is where they do it.)

The trigger is **enabling the pack at any point after the process has loaded its
data, which includes the main menu.** The log shows two reload cycles in one
process, at `Lua 0:00:28` — the game reaching the main menu and the box being
ticked, nothing to do with being in a colony:

```
:67  [SMRTest] test kit loaded          <- first pass, Test Kit ONLY
:72  Reloading done in 924 ms
:80  Loaded mod items for: SMR_CommunityFixPackTestKit
:98  [SMRTest] test kit loaded          <- second pass, after the pack was ticked
:102 [CommunityFixPack] CaveInsNoDisasters: applied
:188 Reloading done in 1158 ms
:190 Loaded mod items for: SMR_CommunityFixPackTestKit, SMR_CommunityFixPack
```

The process was already up with its data loaded; ticking the mod triggered an
**in-place mod reload**, and our code ran inside it. `apply()` calls `patch()`,
documented as *"no-op unless the presets are already loaded"*, and the file
header states *"presets load after mod code … hence the DataLoaded/DataChanged
handlers"*. **Both statements assume a cold boot.** On a reload `StoryBits` is
already populated, so the pass did real work during file scope — where
`HasTrait` exists but is not yet flattened. The Test-Kit-before-pack ordering
noted in an earlier draft is incidental: a side effect of the Test Kit loading
alone first and both together second.

**⚠️ SEVERITY — this is the first-run experience, not an edge case.** The only
way to enable a mod is for the player to do it, and they do it from the main
menu of a session that is already running. So **the broken path is the one every
player takes the first time they install this pack**: launch → Mods → enable →
play, with `Fix_DustSicknessBiorobots` dead for that entire session (Dust
Sickness keeps infecting Biorobots, who keep bleeding Health every dust storm).
Nothing prompts a restart, and the only visible sign is the C1 dialog. It
**self-corrects from the next launch onward**, because the mod is enabled before
the process starts.

**And it is exactly the path our harness has never tested.** Every A/B leg
launches with the pack already enabled, so all 74/74 measurements describe the
*second* session onward. The first session — the one a new player actually has —
has never been measured.

**The general defect is bigger than this one fix: apply-time code assumes a cold
boot.** This is the same hazard class the 2026-07-29 audit's finding **A2**
addressed when it moved three flattening-unsafe `Opt_` hooks to file-scope
install *"so a first mid-session enable works"*. That remediation fixed it for
those three modules; **the shared `SMRFixPack.DataPatch` scaffold has the same
exposure and was never covered.** The repair below fixes the reported symptom;
the sweep in follow-up 1 is what addresses the class.

**REPAIR — owner direction 2026-07-31: solve it so the player never needs to be
told anything.** A dialog explaining a broken first run is a worse outcome than a
first run that works, so the player-facing message below is a fallback, not the
fix.

⚠️ **The obvious guard does NOT work.** Skipping the construction and "letting
the `DataLoaded` pass handle it" fails on this exact path — `DataLoaded` has
already fired before the mod was enabled and does not fire again, so the fix
would simply never apply that session. The repair needs a genuine
post-flattening trigger.

**Two exist, both source-verified, neither blacklisted (`ModMsgBlacklist`,
`Mod.lua:1430-1440`) — UNTESTED, verify before relying on them:**
- **`OnMsg.ClassesBuilt`** (`CommonLua/Core/classes.lua:1099`) — *"post-built
  actions on the final classes"*, i.e. after flattening, which is precisely what
  `HasTrait:new` needs. `MsgClear`'d immediately after firing (`:1100`), so it is
  one-shot per build cycle and the handler must be registered at file scope —
  where our code already runs. **The crash itself proves the ordering works:**
  `HasTrait` was unflattened when our code ran, so classes had not yet been
  built, so a handler registered then still fires afterwards.
- **`OnMsg.ModsReloaded`** (`CommonLua/Classes/Mod.lua:2193`) — *"fired right
  after mods are loaded, unloaded or changed"*; the enable path specifically.

**Preferred shape — fix the class, not the instance.** Remove the cold-boot
assumption from the shared `SMRFixPack.DataPatch` scaffold rather than patching
this one file: do no work at apply time, register the full trigger set
(`DataLoaded` for cold boot, `ClassesBuilt` / `ModsReloaded` for the enable
path, `DataChanged` for re-fires), and let whichever fires first with **both**
presets loaded and classes flattened do the work once, idempotently. Every
`DataPatch` user inherits the fix. Construction should also use
`PlaceObj("HasTrait", { Trait = "Android", Negate = true })` rather than
`HasTrait:new{…}`; **a plain table will not do**, since those filters are
evaluated through their class metatable.

**Verification:** a re-verified A/B (~90 s unattended) **plus a leg on the enable
path** — boot with the pack off, enable it at the main menu, then run the probes.
That leg does not exist today and is the reason this hid (see follow-up 3).

**FALLBACK ONLY — the player-facing message, if something still slips through.**
The C1 dialog is entirely ours (`00_Core.lua:345-391`) and currently
misclassifies: `UpdateSuspects` treats `status == "error"` as patch rot, so a
fix that *threw* is reported with the vocabulary of a fix whose self-check found
changed game code. That is what produced "the game code they patch has changed"
when no such thing had happened, and it sends a player hunting for a mod update
that cannot help. Split it:
- `inactive` + update-suspect → genuine patch rot. Keep today's text. **Do not
  suggest a restart** — it will not help and sends them in circles.
- `error` → the fix crashed at startup. Different text, and the actionable line
  belongs here: *"If you just enabled this mod, restart the game to activate the
  affected fix(es). If this reappears after a restart, please report it."*
The enable path is also **detectable** — presets already populated at file scope
is exactly the trigger condition — so the message can state what happened rather
than hedge. **Fire only when something actually failed**; a dialog greeting every
player on install is worse than the bug it describes.

**Two follow-ups this earns, neither done:** ✅ **ALL THREE ARE NOW DONE OR
BUILT — see the "WHAT LANDED" block at the top of this entry. The sweep in 1
found three more casualties; 3 is built but unrun.** Original text kept below
because it states the reasoning:
1. **Sweep every `apply()` for cold-boot assumptions** — constructor calls
   (`:new{`, `PlaceObj`, class-table methods) and anything that behaves
   differently when presets are already loaded. Third occurrence of the
   pre-flattening trap, and the second hazard of the mid-session-enable class
   after audit finding A2, so the codebase should be checked rather than patched
   incident by incident. **Test both paths:** a cold boot AND a mid-session
   enable from the Mod Manager. Every leg we have ever run is a cold boot, which
   is precisely why this hid.
2. **`FIX_POLICY` needs the rule stated**: apply-time code runs before class
   flattening and may not construct preset/class objects, and **no apply() may
   assume a cold boot** — the player's first run is always the enable path.
3. **The harness has never tested the enable path — add a leg for it.** Every
   A/B leg ever run launches with the pack already enabled, so all `74/74`
   figures describe the second session onward. A leg that boots with the pack
   off, enables it at the main menu and then runs the probes would have caught
   this the day it was written, and ~~would also verify audit finding **A2**'s
   three `Opt_` modules, whose "a first mid-session enable works" remediation has
   never been checked end to end. **This is the widest-coverage item on the
   entry** — wider than the repair itself.

**Credit where due:** this is the C1 surface's first catch outside a synthetic
test, and it caught a defect that would otherwise have shipped silently. That
was the argument for building it.

### F88 — OUR OWN DEFECT: the per-load meteor restart re-rolls the timer, silently suppressing meteors for frequent loaders (P2, SOURCE-VERIFIED)  `[fixed 2026-08-01, VERIFIED by Tier-1 leg 2 — the defect's own repro is its regression test, and it passed: filed 2026-07-31; **fix BUILT 2026-08-01 in the F86 Tier-1 rewrite of Code/Fix_MeteorFrequency.lua: OnMsg.LoadGame's unconditional restart is DELETED; a one-shot latched heal (GameVar SMRFixPack_MeteorLatch = last-healed pack version, PostLoadGame, restart once per save lineage per version) replaces it. Leg 2 met the bar the entry itself named — 3 loads inside a rolled interval, meteor arrived on the PERSISTED deadline (log Mars.exe-20260801-17.11.08: t=216351730 → three Load Game blocks with zero pack lines → t=218608231, +2256501 ms = 75 game hours); see the leg note at the entry's end**]`

**Found by the owner during the F86 design review** (recorded first in
`F86_SESSION_FINDINGS.md` §1.4); independently confirmed by the adjudication
(§2.4) against the shipped file.

**Defect.** `Code/Fix_MeteorFrequency.lua:187-197`: `OnMsg.LoadGame` calls
`RestartGlobalGameTimeThread("Meteors")` gated only on the fix being active —
never on the persisted thread's health. The restarted body re-rolls
`spawn_time` from zero (`:90`, `SessionRandom:Random(spawntime, spawntime +
spawntime_random)` = 35-115 **game** hours ≈ 1.5-4.8 sols). So a player who
never plays a full rolled interval between loads **never receives a single
meteor — indefinitely and silently**, for as long as the pack is installed.
The file's own header saw the mechanism and stopped one inference short:
"worst case a pending strike/warning is rescheduled **once** on load" — true
per load, false in aggregate. Vanilla does NOT have this defect:
`OnMsg.PersistPostLoad` (`_fixup.lua:50-56`) resumes the persisted thread with
its remaining sleep intact and rebuilds only when the save carries nothing.

**The same restart is also the measured repair.** PT-20TEST-B measured that
reinstalling the pack revives a dead `Meteors` thread — that IS this restart.
Both effects are real: it revives dead threads (good) and re-rolls live timers
(this defect). "Put the mod back" remains honest advice for reviving a
damaged save, with this caveat attached until the fix ships. `[FAQ]`

**Fix (adopted 2026-07-31, owner):** the F86 Tier-1 rewrite replaces the
unconditional restart with a **one-shot latched heal** — restart once per save
lineage on first load under the new version (GameVar version latch), never
again — which fixes this defect, guards the upgrade path (old serialised
bodies calling deleted helpers), and clears old bodies out of existing saves
in one mechanism. Shipped precedent for the pattern:
`Fix_RainsDeadlock`'s `RefreshRainsLoops` marker. Spec:
`F86_EXECUTION_PLAN.md` Phase 1; regression leg (load 3× inside a rolled
interval, meteor must still arrive on the persisted schedule): Phase 2.

**✅ VERIFIED 2026-08-01 — Tier-1 leg 2, the defect's own repro run as its
regression test** (owner at the keyboard; save lineage `save_game_id
HdmSxGs6kyd0uz6-`, log `Mars.exe-20260801-17.11.08`). The bar this entry set
for itself was "load 3× inside a rolled interval, the meteor must arrive on the
persisted deadline". What the log reads:

- Strike #1 at `t=216351730`, then a quicksave.
- **Three `Load Game` blocks with ZERO pack lines between them** — no heal, no
  migration, no restart. Under the old body each of those loads would have
  re-rolled the timer; that is the whole defect, and it is absent.
- Strike #2 at `t=218608231 (+2256501 ms = 75 game hours)` — the meteor
  arrived on the deadline that was rolled BEFORE the three loads.

The one-shot latch behaved as designed across the sitting: the heal fired
exactly once, on the first load of the lineage (`MeteorFrequency: one-shot
heal — persisted Meteors thread was alive; restarting onto vanilla's body
(latch false -> 1.0.1)`, log `Mars.exe-20260801-16.42.31`), and **never again**
on any later load. Under uninstall (leg 5, log `Mars.exe-20260801-19.14.11`)
the latch GameVar read `SMRFixPack_MeteorLatch = (absent)` and the `Meteors`
thread was `valid=true` on vanilla's body — the replacement mechanism leaves
nothing behind that could re-roll anything.

Cross-refs: F02, F86.

### F89 — MeteorsDisaster's unbounded drain loop wedges the Meteors thread on ordinary strikes; the colony silently loses all regular meteors (P2, MEASURED)  `[open — filed 2026-08-01 mid-sitting (Tier-1 leg 1); vanilla defect, F78's class on the singles path; COVERED by the F02 watchdog (detect + restart at its 189h threshold, ~6-8 sol latency, proven live the same sitting); no direct fix routable: the loop is mid-function with no seam, and a body copy is barred by F86/FIX_POLICY §3a]`

**Defect (vanilla; same code F78 documented, different reachable state).** EVERY
`MeteorsDisaster` call — not just storms — ends in the unbounded drain tail
(`Meteors.lua:238-241`): `while not g_MeteorStormStop and #spawned > 0 do
WaitMsg("MeteorDone", delta) table.validate(spawned) end`. When a spawned entry
never becomes invalid, the CALL never returns. For a storm that wedges the
MeteorStorm scheduler (F78, fixed by `Fix_MeteorStormWedge`). For a **single or
multispawn strike** it wedges the **`Meteors` thread itself** — and
`Fix_MeteorStormWedge` is blind to it BY CONSTRUCTION: its signature requires
`g_MeteorStorm`, which ordinary strikes never set.

**Measured live 2026-08-01** (log `Mars.exe-20260801-17.11.08`, test-2 lineage,
owner at keyboard): strike printed at `t=218608231` (its impact destroyed 2
infrastructure — the call's meteors landed), then 192 game hours of silence with
`GetMeteorsDescr()` valid throughout (Atmosphere 59.37%, nowhere near the 80%
shutoff), thread reads `valid: true`, zero `[LUA ERROR]`, no loads after the
strike. The F02 watchdog crossed its threshold
(`spawntime+random+SensorTowerPredictionMaxTime+DayDuration` = 189h on this
map's 65+0-25h descriptor) and acted:
`WATCHDOG — no meteor resolved for 192 game hours (thread ALIVE but stuck);
restarting onto vanilla's body`.

**Retro-consistency — this class is likely PT-01's recurring stall.** The old
heartbeat died at phase `'striking'` (set immediately BEFORE the
`MeteorsDisaster` call, F02 entry) and TEST 2G's watchdog fired at 183h with
the same ALIVE-but-stuck read — both match a wedged drain call, not a dead
thread. F78+F81 remain real and fixed; this entry records that the drain-loop
class ALSO reaches the Meteors thread through ordinary strikes, where the
storm watchdog cannot see it.

**Disposition: watchdog-insurance IS the design (accepted, disclosed).** The
F02 watchdog detects (designed-silence guards keep it honest), diagnoses
alive-vs-dead, restarts onto vanilla's body (cost: one timer re-roll), gives up
loudly after 3. In vanilla, without the pack, this state is a permanent loss of
all regular meteors for the save. No layer-3 route exists into a mid-function
loop; bounding the loop would need a body copy — barred (F86, §3a).

**Two bounded caveats, measured the same sitting (accepted, disclosed):**
(1) **event strikes re-arm the watchdog's liveness clock** — ANY meteor posts
`Msg("MeteorDone")`, including story-bit/sequence/POI event spawns
(`MeteorsDisaster` has NINE call sites in Src; the event families fire outside
the 65-90h roll, unannounced) — so detection latency stretches during
event-heavy play; the conservative threshold absorbs it. (2) **strike
attribution needs the caller type**: the sitting's strike #3 was a Singularity
story-bit meteor masquerading as a scheduler strike until the story-bit log
line was correlated; the TestKit's Meteors logger now prints the
`meteors_type` argument to disambiguate ("single"/"multispawn" from the
scheduler or events, "storm" from the storm thread — sequence/POI singles
remain ambiguous without an accompanying story-bit line).
**Supporting sighting, uninstrumented (2026-08-01, Tier-1 leg 5).** With the
pack disabled for the uninstall leg, the owner watched a meteor warning appear
and the meteor never arrive, and none returned for the rest of the sitting —
the signature this entry describes, in pure vanilla with no watchdog present to
heal it. Recorded as an observation, **not** a measurement: the meteor logger
is a per-session toggle and the full game restart had cleared it, so log
`Mars.exe-20260801-19.14.11` carries no `MeteorsDisaster` print to confirm the
call entry. It does not add to the evidence above; it is noted because it is
what a player without the pack would see, and because a future session reading
that log should not mistake the silence for a pack defect.

Cross-refs: F02 (watchdog), F78 (class + storm half), F86 (why no body copy).

### F90 — Surface dust storms break UNDERGROUND cables and pipes: the break pass picks its victim from a cross-map grid fragment with no map filter (P2, SOURCE-VERIFIED)  `[open — filed 2026-08-01 by the chain-prompt-6 C04 sweep, promoted from candidate C04; full call chain read in Src this session; independent Relaunched witness + working third-party fix; NOTHING BUILT — decision package is chain prompt 7's]`

**The full call chain, every line read in `<game>\ModTools\Src` on 2026-08-01
(1.0.7.396349). This is the C04 lead's own sweep, and it closes it.**

1. `City:HourlyUpdate(hour)` — `Lua\City.lua:144-157`:
   `if HasDustStorm(self:GetMap()) and hour % const.BreakIntervalHours == 0
   then self:RandomBreakSupplyGrid() end` (:148-149).
2. `HasDustStorm(map)` — `Lua\DustStorm.lua:39-42`:
   `return (MainMap == map) and g_DustStorm`. **Dust storms are a MainMap-only
   phenomenon by construction**, and only the main city ever runs the break
   pass. Hold on to this line: it is the intent tell.
3. `City:RandomBreakSupplyGrid` — `City.lua:178-181` → `self.electricity
   :RandomBreakElements()` and `self.water:RandomBreakElements()`.
4. `SupplyGrid:RandomBreakElements` — `Lua\SupplyGrid.lua:1017-1021`: walks
   **that city's fragment list** and calls `RandomBreakConnection` on each.
5. `SupplyGridFragment:RandomBreakConnection` — `SupplyGrid.lua:669-683`: on a
   hit, `local element = table.rand(self.connectors, self:Random())` (:677) →
   `bld:Break()` (:680). **No map filter, no city filter, nothing.**

**How an underground connector gets into `self.connectors` — the other half the
C04 lead asked for, and it is not an accident: the class is named for it.**
`SupplyGridFragment` inherits **`MultiMapSupplyGrid`** (`SupplyGrid.lua:337-338`,
class defined :276-333), which exists precisely to let one fragment span
several maps. The join is the elevator: `MapPassageLinked:MergePassageGrids`
(`Lua\Buildings\Elevator.lua:402-408`) → `MergeGrids(supply_resource)`
(:412-440) → the global `MergeGrids` (`SupplyGrid.lua:1635-1650`), which walks
the far-side fragment's elements and calls `new_grid:AddElement(element)`
(:1644) — and `SupplyGridFragment:AddElement` pushes every cable/pipe straight
into the merged fragment's connector array: `if element.is_cable_or_pipe then
self.connectors[#self.connectors + 1] = element end` (:547-548). The
1.0.7 savegame fixup even sequences it explicitly: *"setup electricity and life
support grids for all maps **before handling elevators**"*
(`SavegameFixups.AAAA_InitSupplyGridCities`, :1687-1718).

**And the merged fragment really is on the surface city's list.**
`SupplyGridFragment:AddCityElement` (:463-477) registers the fragment into
`city[supply_resource]` the first time it gains an element from that city
(`if self.cities[city] == 1 then ... grid_list[#grid_list + 1] = self`,
:473-476). So one fragment sits in **both** cities' lists, holding **both**
maps' connectors — and step 4 above hands the whole thing to a map-blind
victim picker.

**Result: with an elevator built, a dust storm on the surface can break a cable
or pipe underground, where no dust storm exists or can exist.**

**Intent tell (two, and the second is a sibling contradiction).**
(a) `HasDustStorm` is hard-gated to `MainMap` (`DustStorm.lua:41`) — the
disaster is *designed* surface-only, and the break pass is its damage arm; the
damage escaping the map the gate just enforced is not a design choice.
(b) **Sixteen lines above the break pass, the same file's production pass
handles the multi-map case correctly and says so**: `ProductionThreadProc`
(`SupplyGrid.lua:992-1006`) guards with `if self.city ==
grid_fragment.cities[1] then` under the comment *"this grid only updates
fragments that were first added to this city / this prevents multiple
production calls when multiple cities share the same grid fragment"*
(:999-1001). `RandomBreakElements` (:1017-1021) carries **no** such guard.
The code knows fragments span cities; the break path was written as if they
did not.
*(The missing guard in (b) is currently inert on its own — `HasDustStorm`
means only the main city ever calls the pass, so a shared fragment is rolled
once, not twice. It is recorded as the tell, not as a second defect.)*

**External corroboration (independent, and it fixes exactly this).** GromGor's
"No Underground supply grid breaks" (workshop 3730839706): *"It's very strange
to experience supply grid breaks underground during dust storms on the
surface. This mod fixes it."* His FPK was re-extracted from the archive this
session and read in full — a whole-body replacement of
`SupplyGridFragment:RandomBreakConnection` that builds a `surface_connectors`
list filtered on `con.building.city:GetMap() == MainMap` and rolls the victim
from that. Same function, same line, same diagnosis, reached independently.

**Reachability.** Ordinary mid-game: underground unlocked, one elevator built
(which merges the grids automatically), a surface dust storm, `#connectors >
10` on the merged fragment (`IsBreakable`, :693-697), and the roll. No exotic
state, no game rule, no mod interaction.

**Two things the decision package must weigh (NOT decided here — prompt 7
owns decisions, and this session built nothing):**
- **Shape.** The defect sits mid-function at :677, inside a body whose first
  half computes the roll. A wrapper cannot reach the victim pick without
  re-implementing the roll, so this is a body-copy candidate — which
  **FIX_POLICY §3a / F86 constrain**. Whether a layer-2 route exists (e.g.
  wrapping `SupplyGrid:RandomBreakElements` and temporarily narrowing what the
  fragment exposes, or intercepting `BreakableSupplyGridElement:Break` and
  vetoing an off-MainMap break during a dust storm) is the real design
  question, and the `Break` interception is the cheaper-looking of the two.
- **Scope beyond the victim pick.** Both `IsBreakable`'s `#self.connectors <=
  10` test (:695) and the break probability itself, `((1000000 - break_chance)
  / 1000000.0) ^ #self.elements` (:673), are computed over the **merged**
  cross-map totals. So building an elevator also raises how often the *surface*
  breaks, by counting underground elements. GromGor left both alone. Whether
  that is a second defect or the intended "one grid" behaviour is an intent
  question, not a code one — flagged, not filed.
- Note for whoever writes the fix: GromGor's version would index a nil
  `element` if `surface_connectors` came back empty. Unreachable in practice
  (a purely-underground fragment is never on the main city's list), but our
  version must guard rather than inherit the shape.

Cross-refs: C04 (the lead this closes), F86/FIX_POLICY §3a (why the body copy
is not automatic), `BUG_LIST_AUDIT.md` §9 (mechanism-confirmed grading) and
§10.2 (this sweep).

### D06 — Drone assignment has no cross-hub locality; far fleets claim near work (design, high)  `[built 2026-07-28: Code/Opt_DroneOverhaul.lua core v1 (opt-in, off by default, Mod Options toggle "Drone dispatch overhaul (experimental)"); FIRST MEASURED A/B 2026-07-29 — NULL RESULT for the claim gate, and it exposed why: see below; INSTRUMENT REBUILT v2 2026-07-29 (lifecycle tracing, TestKit). ⭐ **REBUILD DECIDED 2026-07-31 — v1 is being REPLACED; see the plan of record immediately below. 4 research gates owed; PT-52 (incl. the B2 re-run) is FROZEN pending invalidation — do NOT run it**]`
*(Heading line restored by the popup-audit session 2026-07-30 — the F84 filing
commit `21b92cb` had spliced F84's text into this heading, leaving D06's whole
entry living under F84. Content untouched.)*

> ⚠️ **SAVE-SAFETY SURGERY LANDED ON THIS MODULE 2026-08-01 (chain prompt 5, F86
> Tier 2) — it is NOT drone work and changes NO drone behaviour.** F86 Site 2 was
> the moonlighting hook: a post-wrapper on `Drone:Idle`, whose frame sits below
> three `Sleep`s, so every drone parked in Idle at save time serialised our frame
> and threw `Opt_DroneOverhaul.lua:96: attempt to index a nil value (global
> 'SMRFixPack')` on the next load without the pack — **80** on the 2026-08-01
> uninstall leg, 98 when first measured. The hook moved to vanilla's own last
> statement in the same fall-through, `self:CleanUnreachables()`
> (`Drone.lua:640`), gated on `self.command == "Idle"`. Vanilla has **no statement
> between that call and the end of `Idle`**, so the trigger condition, the
> ordering and the code that runs are identical — a call-position move and
> nothing else, which is exactly the limit of the owner's pre-granted carve-out.
> The rebuild decision below is untouched by it, and PT-52 stays frozen.
> Full record: the F86 entry's Site 2 block. Verification: PT-58.

---

> 🚧 **DRONE WORK HAS ITS OWN PROMPT — `docs/prompts/DRONE_PROJECT_PROMPT.md`** (owner,
> 2026-07-31). It is re-runnable and owns D06, D08, D09, F77, the drone queue
> machinery, the consolidated drone playtest and the cleanup mod.
> `docs/prompts/FABLE_NEXT_PROMPT.md` is the **general** prompt and may answer drone
> questions but **may not start, plan or schedule drone work.** This entry is the
> plan of record; that prompt is how a session picks it up.

## ⭐ REBUILD DECIDED 2026-07-31 (owner) — this entry's shipped v1 is being replaced

**Drones moved to the TOP of the list, nothing about drones is deferred, and the
rebuild lands as ONE piece rather than another increment.** Owner's reasoning:
drones are the one part of the pack that has been iterated piece-by-piece, and
that is *why* it became cumbersome to test and reason about. Also, verbatim:
*"even though its not technically bugged, it is near the top of a top 10 list of
reasons people hate late game… I consider it to be an opt in only in terms of it
being technically not bugged, but as far as I am concerned its a non bugged core
developer failure."*

### The finding that reframes v1 (from this entry's own B2 data)

Hauling was **3h03m of a 3h27m total — 88% of elapsed time — and D06 exempts
hauling by design.** Within the remaining 12%, the claim gate fired **once in 25
malfunctions** and moved its leg by one minute, because
`MaintenanceDroneUnload` → `StartWorkPhase(drone)` hands the repair to the
**delivering** drone and bypasses `FindTask` entirely.

**v1's exemption line was drawn on a code seam, not on the player's problem.**
In the code, hauling is `rfSupplyDemand` pairing and repair is `rfWork` — two
systems. But for a building that needs a maintenance resource, **the haul IS the
repair.** That is a scoping error, not a tuning miss, and it is the case for
rebuilding rather than iterating.

### The root cause, and the full priority research

**→ `docs/reports/DRONE_PRIORITY_SYSTEM.md`** (source-verified 2026-07-31) is the
reference. Headline: there is **no hidden priority band**. The whole system is
five integers, `-1..3`; the player's scrollbar is `min 1, max 3, default 2`
(`Building.lua:199`); and the "fast repair" players notice is **two classes
auto-assigning themselves band 3** — `BreakableSupplyGridElement` (pipes/cables)
and `PassageGridElement` (dome fractures), both at
`GetPriorityForRequest`. Ordinary building maintenance has **no override at
all** and inherits the player's arrows.

**The developers' actual rule is not "repairs are urgent"** — track elements are
repairs and get no bump. It is **"life-support-critical repairs are urgent"**,
applied to the grid and the dome shell and never extended to the buildings that
*produce* the air and water. Extending it completes their policy rather than
inventing ours.

### The design shape (owner-directed; NOT yet approved to build)

**The core insight:** the player's arrows answer a **supply-allocation** question
(*"when resources are scarce, who gets them first?"*). The same number also
governs **repair urgency** — a question the player never answered. They answered
the first one once, early, and it silently adjudicates repairs forever. That is
the sol-12 setting still running a sol-400 colony, and it is the forum post.

| Band | Assigned by | Contents |
|---|---|---|
| **5** | auto | malfunctioned life-support — producers, plus the grid/dome tier the game already elevates |
| **4** | auto | every other **malfunctioned** building — decoupled from the arrows |
| **3** | player | supply allocation, "high" |
| **2** | player | supply allocation, "normal" (default) |
| **1** | player | supply allocation, "low" |

- **The split is `is_malfunctioned`** (`RequiresMaintenance.lua:41`, *"no work
  possible"*) — elevate **broken**, not merely degrading. Routine top-up
  genuinely *is* a supply question and stays on the player's scale. This is also
  the bound that stops repairs starving food and construction.
- **The claim gate is DROPPED** (not demoted). It arbitrates a 12% slice already
  decided by the deliverer handoff, and carries strike counters, TTLs and cover
  caches for a measured one-minute effect.
- **Food service buildings get a data-patched default priority of 3**
  (FIX_POLICY §1.1), fully player-overridable. Justification is **correct
  attribution of failure**, not throughput — owner's framing: full pallet in the
  dome reads *"this game sucks, drones are stupid"*; empty pallet reads *"I
  under-built"*. Same starving colonist, opposite conclusion, and only one ends
  up on a forum. That argument holds even when the player really is
  under-producing, which a throughput argument does not.
- **ONE TOGGLE, ALL OR NOTHING.** No sub-toggles inside the module. Separate
  toggles multiply the configuration matrix and every combination is an
  unmeasured product — which is exactly how v1 got here. **D09's stat dials stay
  separate**; they are a player-set value with a clean off position, already
  `tested`.
- **D08's layers are folded into this conversation**, not a separate project —
  layer 1 (the dispatcher) acts on registration, i.e. on the 88%, and the B2
  data promotes it from speculation to evidence-backed.

### ~~⛔ Four gates before any of this is designed further~~ — ALL ANSWERED 2026-07-31

> **HISTORICAL — kept for the reasoning, not as outstanding work.** All four
> answered; see the ANSWERED sections above and `DRONE_PRIORITY_SYSTEM.md`
> §8-§10. The Phase-4 sequencing note below is also spent: Phase 4 completed
> 2026-07-31 and the experiments ran after it.

**→ `docs/archive/DRONE_RESEARCH_BRIEF.md`** (now historical; keep it for the playtest
freeze rules and the disclaimer spec). The gates were: **Q1 can kill the band
scheme outright** — (1) does the C matcher honour a widened priority range?
(2) are hub queues persisted or rebuilt on load? (3) do the life-support and
Food-demand data tests identify what we think? (4) does changing a property
default reach buildings already in a save?

~~**Run them only AFTER the Phase 4 rebuild finishes**~~ — spent; Phase 4 is
complete and the experiments ran after it.

### ✅ ALL FOUR RESEARCH GATES ANSWERED 2026-07-31 — Q1 is **HONOURED**, the band scheme survives

> **Q1 — the C matcher HONOURS a widened priority range. Measured, not inferred.**
> Run on a **new game** (v2 instrument, `MaxBuildingPriority = 5`), where every
> hub allocates `-1..5` natively — `Status()` read
> `sample hub supply_queues keys: -1,0,1,2,3,4,5`, `4 hub(s) seen, 0 topped up`.
> Two identical **Stirling Generators** were armed at **band 3** and **band 4**
> and broken — same colony, same drones, same resources, one variable.
>
> | | band 3 (control) | band 4 (test) |
> |---|---|---|
> | malfunctioned → phase | `demand` → `work` | `demand` → `work` |
> | work request target | 45000 → 0 | **51000 → 11000 → 0** |
> | outcome | repaired | **repaired** |
>
> **The band-4 repair leg was claimed and worked to completion.** The positive
> control cleared alongside it, so the harness is known-good. That kills the
> "ignored" outcome: requests filed at 4 are **not** invisible and **not**
> silently lost.
>
> **✅ THE HAUL LEG IS ALSO CLOSED — second pair, no cheat.** The first pair
> above had its maintenance resource satisfied by `CheatFill`, so it evidenced
> the **work** request only. A second pair was then run on a symmetric fixture:
> two Stirling Generators on **opposite sides of a single hub, both at the very
> limit of its range**, equidistant, with Polymers stocked. Log
> `Mars.exe-20260731-14.09.07`; the cheat sits at line 329 and this pair was
> armed at lines **407 / 425**, i.e. entirely after it — **no cheat touched it**.
>
> - **Direct queue inspection**, not inference: `demand_queues[4][Polymers]`
>   held the band-4 building's request (and `demand_queues[3][Polymers]` the
>   control's). The demand queue at band 4 is real and populated.
> - **Both haul targets went `1000 → 0` by drone delivery.** The demand-queue
>   half — the half that carries **88% of elapsed repair time**, per the B2
>   finding that motivated the rebuild — works at band 4.
> - Band 4 then ran `work 80000 → 50000 → 25000 → 0` and cleared
>   (`malfunctioned=false`).
>
> **🔎 A precedence signal, offered as suggestive and NOT as proof.** From
> equidistant positions under a single hub, the band-4 building reached
> `phase=work` while the band-3 control was **still `phase=demand`**, and it
> finished (`malfunctioned=false`) while the control still had **52000** of
> repair outstanding. That is consistent with the C matcher *ordering* by the
> widened band rather than merely tolerating it — which is what
> `SupplyGridBreakable.lua:52`'s shipped comment claims for the normal range.
> **n=1 pair, no repeat, and drone-assignment luck is not excluded.** Ordering
> within and between bands remains on the "measure, do not assert" list
> (`DRONE_PRIORITY_SYSTEM.md` §7).

### ✅ Q2, Q3 and Q4 are ANSWERED (2026-07-31)

> **Q2 — hub queues are PERSISTED, not rebuilt on load. Answered the hard way.**
> The experiment module widened `const.TaskRequest.MaxBuildingPriority` to 5 at
> file scope; the owner loaded an existing save and **every `FindTask` in the
> colony threw**, drones froze in place while the UI reported "heavy load", and
> the log took tens of millions of error lines. **Nothing had been armed — the
> widening alone did it.** Cause: `TaskRequestHub:Init()`
> (`TaskRequest.lua:242-256`) allocates the queue tables at **construction** and
> never again, so a restored hub carries `-1..3` while the widened const makes
> vanilla's own removal loops iterate `-1..5` and index nil.
> **Full write-up, including three corrections to our own reference doc and the
> savegame-compatibility consequence for the band scheme:
> `DRONE_PRIORITY_SYSTEM.md` §8.** Q1 must be re-run on a **new game**, where
> every hub allocates the full range natively.

> 🧭 **OWNER DECISION 2026-07-31, in response to the Q2 finding — a save-safety
> wall does NOT kill this work, it RELOCATES it.** Verbatim: *"if we run into a
> hard this is a non save safe mod / or needs fresh game to play. That will not
> kill our work, but it will change our work. That will mean it transitions to a
> stand alone mod instead of an opt in for this mod."*
>
> **Consequences, so nobody re-litigates them:**
> - "Requires a new game" is a **shipping shape**, not a failure condition. It
>   moves the overhaul **out of the Community Fix Pack** into its own mod.
> - The Fix Pack's own promise is unaffected: the pack stays save-safe and
>   uninstall-clean, because the risky module would no longer live in it.
> - It also **retires the one-toggle-all-or-nothing constraint's hardest edge** —
>   a standalone mod has no configuration matrix to multiply against the pack's
>   68 default fixes.
> - The design-drift disclaimer (research brief) still applies, and gets
>   *stronger*: a standalone mod that requires a fresh colony must say so at the
>   top, not in a limits section.
> - **What this does NOT license:** shipping a known-broken save path inside the
>   pack "because it might move later". Until the overhaul actually relocates, it
>   stays opt-in-and-off, and D06 v1 remains the shipped thing.

> 💡 **OWNER PROPOSAL 2026-07-31, later the same session — THE CLEANUP MOD. This
> supersedes the "must go standalone" reading above: standalone is no longer
> assumed.** Verbatim: *"Yes we create a stand alone mod. But it becomes a
> cleanup mod. And it allows us to be straight forward in the game description,
> you must run this once after you remove our mod, and it will do a full cleanup.
> And whats better it allows us to safely cleanup anything in the future."*
>
> ⚠️ **CORRECTED 2026-07-31 (PT-20 leg) — THE PREMISE BELOW IS FALSE AND THIS
> ARGUMENT NEEDS RE-MAKING.** Mods **do** get a pre-save hook:
> `OnMsg.SaveGameStart` and `OnMsg.SaveGameDone` reach mod code (measured, with
> `OnMsg.LoadGame` as a positive control). Only `PersistSave`, `PersistLoad` and
> `PersistGatherPermanents` are blacklisted — `SaveGameStart` is not in
> `ModMsgBlacklist` (`Mod.lua:1430-1440`), and `DoSaveGame` fires it before the
> write (`Savegame.lua:1043`). **A tear-down-on-save / rebuild-on-load scheme is
> therefore implementable**, and the sentence below calling it "unimplementable"
> was wrong. That does not by itself kill the cleanup mod — a tear-down cannot
> reach residue already sitting in saves the player has, and it cannot rewind
> another thread's stack — but the cleanup mod can no longer be justified as
> *the only thing that can occupy that window*. Full detail: ENGINE_FACTS + F86.
>
> **Why it works, mechanically.** ~~The blocker was absolute: mods get **no save
> hook** (`PersistSave`/`PersistLoad`/`PersistGatherPermanents` are blacklisted,
> `Mod.lua:1430-1433`), and no mod code can run after its own removal~~ — the
> surviving half of that claim is that **no mod code can run after its own
> removal**, which is still true, so a save's mod-shaped residue is unreachable
> *by the pack itself*. **A second mod is the one thing that can occupy that
> window.** It runs on `OnMsg.LoadGame` — in a world where the pack is already
> gone.
>
> **Three conditions it must meet — recorded so they are not discovered late:**
> 1. **It is a remedy, not a guarantee.** The player has already removed the
>    pack; asking them to install a second mod will reach the diligent and not
>    everyone. So the primary design must still minimise what needs cleaning.
>    The cleaner is not a licence to strand things.
> 2. **It must identify our artifacts with our code absent.** Out-of-range queue
>    keys are self-identifying; an orphaned closure is not —
>    `rawget(obj, "GetPriorityForRequest")` returning a function does not say
>    whose. ⇒ **Design requirement on the PACK: leave deliberate, identifiable
>    markers on anything written into a save.** Prefer generic rules ("anything
>    outside the vanilla range") over a maintained list of known artifacts, which
>    would rot as the pack changes.
> 3. **Zero footprint of its own** — no GameVars, no closures on objects, purely
>    transient work plus a report. Otherwise it needs its own cleanup mod.
>
> **The strongest argument is the last one, and it is two-sided by design.**
> Owner, same session: *"the part about anything in the future is two sided, it
> doesn't mean we have to add other things to it but it gives us the option. But
> more importantly it gives us an option in the future to add things to it that
> we don't know about yet that could come in from beta reports."*
>
> - **It is a capability, not a backlog.** Existing merely permits future
>   cleanups; it does not create an obligation to find work for it, and nothing
>   may be scheduled into it speculatively.
> - **It is a BETA RESPONSE CHANNEL.** If beta surfaces save residue we did not
>   anticipate, the remedy ships **without** requiring players to reinstall the
>   pack and **without** us shipping a risky migration inside the pack itself.
>   That is a materially different posture from "we would have to patch the pack
>   and hope everyone updates".
> - **It preserves the ethos rather than relaxing it.** The standing rule stays
>   *make the mod clean*; the cleaner is for the cases where we hit a genuine
>   brick wall — ~~as here, where mods have **no save hook at all**~~ **(that
>   example is retired: we DO have `SaveGameStart`, see the correction above; the
>   surviving brick wall is residue already inside saves the player already
>   holds)** — not a general permission to leave residue.
>
> **Scope control:** this is a NEW SHIPPED ARTIFACT. It is owed *with the
> overhaul*, not with launch, and must not drift into a separate project
> (`FUTURE_IDEAS.md` exists because every three items closed were adding six).
> **Not approved to build — recorded as the current plan of record for the
> uninstall problem.**

Phase 4 is closed, so the gates are unblocked. **Q3 and Q4 turned out to be
source questions, not playtests, and both are now settled** — enumeration and
persistence are readable in `ModTools\Src` at build `1.0.7.396349`. What still
needs a running game is **Q1**, **Q2**, and a ~30-second confirmation read for
Q4. Nothing below authorises a build.

**Q4 — defaults ARE omitted. Changing a class default re-rates every existing
building in a loaded save, and reverts completely on uninstall.** The chain:

1. `DefineClass.TaskRequester` (`CommonLua/TaskRequest.lua:53-59`) carries
   `priority = DefBuildingPriority` as a **class member** — so `self.priority`
   resolves through the flattened class table, not through property metadata.
2. **No building template anywhere sets `priority`.** Swept all 288
   `Lua/BuildingTemplate/*.generated.lua` plus `Data/`: zero hits. The class
   member is the effective value for every building in the game.
3. The instance member is written **only on a real change**:
   `TaskRequester:SetPriority` (`:170-179`) early-outs on
   `if self.priority == priority then return end` before `self.priority = priority`.
   Moving the arrow to the value it already holds writes nothing.
4. A newly completed building does not get one either: `ConstructionSite:Complete`
   (`:1484-1521`) builds the `instance` table from
   `city / init_with_skin / name / orig_terrain* / construction_data` — no
   `priority`. The one exception is copy-paste (`Building:GatherCopyParams`
   `:3678` → `ApplyCopyParams` `:3683`), which routes through `SetPriority` and
   so still early-outs when equal.
5. Savegames are a **persisted Lua graph** and class tables are permanents keyed
   by name — `CommonLua/Core/persist.lua:157-165` registers every `g_Classes`
   entry. Instance tables serialise their own keys only; the class link is
   restored by name on load.

⇒ A saved building the player never re-prioritised has **no `priority` key at
all** and reads whatever the class default currently is. Player-set values are
explicit members and are preserved. That is the desirable half of both outcomes
the brief posed — but it is now a **known choice**, which is what Q4 asked for.

**✅ CONFIRMED LIVE 2026-07-31** (owner at the keyboard, real loaded save, both
branches in one sitting). On an untouched Small Grocer: `SelectedObj.class` →
`ShopsFood_Small`, `SelectedObj.priority` → **`2`**, and
`rawget(SelectedObj, "priority")` → **nil** — the key is genuinely absent, so the
2 is the class table's. Then, after moving that building's priority arrow to 3,
`rawget(SelectedObj, "priority")` → **`3`**. Both halves of the prediction, from
the live game rather than from source alone: the member materialises **only on a
real change**, so untouched buildings follow the class default and hand-set ones
keep the player's choice.

⚠️ **Trap found while proving it: `const.TaskRequest.DefBuildingPriority` is
dead for this purpose.** `DefineClass.TaskRequester` captures the module local at
**file-load** time (`:57`); `OnMsg.ClassesPreprocess` reassigns that local
**afterwards** (`:21-32`), by which point the classdef already holds 2. A default
change must therefore be written **on the class**, never through the const group.
`Min`/`MaxBuildingPriority` are unaffected — `InitRequestQueues` reads them at
call time — so **Q1's experiment is unharmed**.

**Q3a — use the shipped CLASS test, not the property test. It catches exactly
five buildings.**

- The game already has the test and uses it:
  `LifeSupportGridObject:ShowUISectionLifeSupportProduction`
  (`LifeSupportGrid.lua:272-276`) is `IsKindOf("AirProducer") or IsKindOf("WaterProducer")`.
- Both classes carry an engine docstring making a **completeness claim**: *"All
  buildings that produce water for the water grid are either of this class or a
  derived class"* (`LifeSupportProducer.lua:21-23`; the air twin at `:125-127`).
  That is source-authoritative, not an inference from a sweep.
- Full enumeration. Only four classes derive from them — `ElectrolyzerBase`,
  `MOXIEBase`, `MoistureVaporatorBase`, `WaterExtractorBase` — yielding five
  templates: **MOXIE** and **Electrolyzer** (air); **Water Extractor**,
  **Micro-G Water Extractor** and **Moisture Vaporator** (water). Nothing
  trivial is caught; there are no false positives.
- **The property test the brief proposed would have been worse.** Only 4 of the
  288 templates state `air_production`/`water_production` in data at all — the
  rest inherit the property default of `10000` (`LifeSupportProducer.lua:28,132`)
  — so a template-data sweep silently misses one producer.

Two judgements the enumeration hands the owner (**recorded, not decided**):

- **Storage is NOT caught.** `AirStorage`/`WaterStorage` (Oxygen Tank ×2, Water
  Tank ×2, `LifeSupportStorage.lua:305-323`) are a separate class family. A
  broken tank does not stop production; it drops buffer.
- **The power-plant question: OUT, and it should be.** An unpowered MOXIE is
  *not working*, not *malfunctioned* — a different state, and not what
  `is_malfunctioned` selects. Elevating by dependency also has no natural
  stopping point (every producer depends on power, which depends on maintenance,
  which depends on hauling). The shipped precedent agrees: §4a elevates the grid
  element itself, never its upstream.

**Q3b — the Food-demand test alone has two false positives; adding the
ServiceWorkplace test makes it exact (four buildings).**

- `consumption_resource_type = "Food"` across all 288 templates catches **six**:
  Diner, Mega Mall, Grocer (`ShopsFood`), Small Grocer (`ShopsFood_Small`) —
  **plus Micro-G Habitat and Naturalist Habitat**.
- Those two are **residences, not services**: `MicroGHabitatBase` is
  `{ LivingBase, LifeSupportConsumer, WaypointsObj, Community, … }`
  (`MicroGHabitat.lua:3-4`) and `NaturalHabitatBase` derives from it
  (`NaturalHabitat.lua:1-2`). They *consume* food rather than serving it.
- So the test to use is **`IsKindOf("ServiceWorkplace")` AND a Food demand
  request** → exactly **Diner, Mega Mall, Grocer, Small Grocer**. No other
  service qualifies: Casino, Spacebar, Temple, Medical Center, Low-G Amusement
  Park and the Electronics/Jewelry shops carry no Food demand.
- ⚠️ **Owner call parked, not made:** the two habitats are places colonists
  *live* that starve on the same queue. Excluding them is defensible — they are
  not services, and a hungry habitat is a different UI story — but it is a
  judgement, not a fact.
- **The owner's observation is CONFIRMED, and more strongly than it was put.**
  Food services do have the property (`Grocery` → `ServiceWorkplace` → … →
  `TaskRequester.priority = 2`), and the arrows do show (no service sets
  `prio_button = false`; the templates that do are decorations and anomalies).
  And per Q4 step 2, **no template in the entire game sets `priority`** — so
  every building on the map starts at exactly 2, and the only distinguishing
  signal in the whole system is the one the player supplies by hand.

### ⛔ Drone playtest FREEZE, and a mandatory disclaimer

**No drone playtesting until a final plan exists** (banner in
`PLAYTEST_CHECKLIST.md` §1). **PT-52 Triggers A/B/B2 are FROZEN pending
invalidation**; on approval they are archived as deprecated-by-redesign and
replaced by **ONE multi-step playtest**, not a family of them. **PT-10 (F55) is
NOT frozen** — different subject, shipped default-on fix. F77's defect is real
and unaffected; only its test packaging is caught, and it folds into the
consolidated PT.

**The rebuild does not ship without a design-drift disclaimer** in
MOD_DESCRIPTION (owner requirement; spec in the research brief). It cannot be
written until Q2 answers, because the honest uninstall claim depends on it.

---
**COMMANDER-PROFILE INTERACTION CHECKED 2026-07-30 (owner question) — NO
COLLISION between the `Inventor` profile and D06/D09/F77; the interaction is
purely one of measurement.** Enumerated rather than assumed:

- **Inventor** (`Data/CommanderProfilePreset.lua:152-186`) applies three
  `Effect_ModifyLabelOverTime` ramps to the **`Consts`** label —
  `DroneConstructAmount` +1%, `DroneBuildingRepairAmount` +1%,
  `DroneGatherResourceWorkTime` −1%, each every 2 sols × 50 reps (to Sol 100) —
  plus `Effect_GrantTech AutonomousHubs`.
- **`AutonomousHubs`** (`Data/TechPreset.lua:1332-1358`) sets
  `disable_electricity_consumption` and `disable_maintenance` on the **`DroneHub`**
  and **`DroneHubExtender`** labels.
- **D09** writes exactly two modifiers, by id, through
  `colony:SetLabelModifier`: `SMRFixPack_DroneSpeedDial` on label **`Drone`**
  prop `move_speed`, and `SMRFixPack_DroneCarryDial` on label **`Consts`** prop
  `DroneResourceCarryAmount`. It removes only those two ids, so it cannot touch
  a profile's or a tech's modifiers. **Label `Consts` is shared with Inventor but
  the props are disjoint** (`DroneResourceCarryAmount` vs the three above), and
  Inventor never touches `move_speed`. The two are complementary by accident:
  Inventor makes drones *work* faster, D09 makes them *move* faster and carry
  more.
- **D06 and F77 reference no power, maintenance or `disable_*` property at all**
  (grepped). D06 changes *who claims* work, never how fast work goes; Inventor
  changes *how fast*, never who claims. Orthogonal layers.

**What DOES change is measurement validity, and it matters for PT-52:**
1. Inventor's ramps mean **repair throughput on that colony drifts upward over
   time**. The B2 protocol survives this only because it reloads the same
   quicksave between legs, putting both at the same sol. **Never compare a
   stress run against one from an earlier sitting on an Inventor save.**
2. `AutonomousHubs` removes the two commonest causes of an extender's
   working-flag flapping, so **F77's trigger should be rare or absent there** —
   a quiet F77 half on an Inventor save is not evidence the fix does nothing.
   *(Inference from the effect data; not observed. Run the F77 half on a
   non-Inventor save if the result is to mean anything.)*

Recorded per the EXTERNAL VALIDITY rule: **log the commander profile with any
D06 measurement**, the same way run conditions are logged.

**FIRST MEASURED A/B — PT-52 Trigger B2, 2026-07-29.** Controlled run on the
user's live 9-hub colony: same quicksave reloaded between legs, identical seeded
target set (`scope="overlap"`, `n=25`, `seed=1`), **both legs at NORMAL speed**,
supply storages deliberately filled and spaced identically for both legs. Log
flushed and kept.

| Metric | Leg A (module OFF) | Leg B (module ACTIVE) | Δ |
|---|---|---|---|
| CLOSEST-HUB first claims | 8/25 (32%) | 10/25 (40%) | +2 buildings |
| **work→first claim** — *the only leg the gate arbitrates* | **58m** | **57m** | **−1m** |
| break→work (hauling; D06-exempt by design) | 3h03m | 2h05m | −58m |
| total | 3h27m | 2h53m | −34m |
| **`vetoed` delta** | +0 | **+1** | gate fired ONCE |
| repaired | 24/25 (12h timeout) | 25/25 (6h) | — |
| no-resource subset | **0 targets** | **0 targets** | — |
| repair claims / 25 buildings | 26 | 27 | ~1 each |

**Verdict: the claim gate did essentially nothing, and the run explains why.**
It intervened exactly once across 25 simultaneous malfunctions, and the leg it
can influence moved by one minute. A single veto cannot shift a mean by 34
minutes, so the total-time difference lives in the leg D06 does not touch —
i.e. it is colony variance, not treatment.

**Root cause of the inertness, visible in the data:** `no-resource subset: 0` —
every one of the 25 targets required a maintenance resource, so every one ran
demand → delivery → work, and `MaintenanceDroneUnload` → `StartWorkPhase(drone)`
(`RequiresMaintenance.lua:423,190`) hands the first repair tick straight to the
**delivering** drone via `SetCommandKeepQueue`, **bypassing `FindTask`
entirely**. The claim totals confirm it — 26 and 27 claims for 25 buildings, so
the deliverer performed the whole repair. The near-uniform ~57m "work→claim" in
BOTH legs is that handoff, not a race being won.
**Consequence for the instrument:** the harness's headline metric is measuring
**which hub delivered the resource**, not which hub won a repair claim. This was
flagged as the top risk in `HARNESS_REVIEW_PROMPT.md` §2 before the run and is
now confirmed empirically. The metric needs redesign before it can score the
gate (candidates: sample `no_resource`-maintenance buildings and dust/clean work
specifically; or instrument `TaskRequestHub:FindTask` outcomes directly rather
than inferring from `Drone:Work`).

**THE FINDING THAT MATTERS IS BIGGER THAN THE NULL RESULT.** Hauling is
**3h03m of a 3h27m total — 88% of the elapsed time**, and D06 exempts hauling by
design. This document's own escalation condition is therefore met: *"If the
delivery leg dominates the pain, that is the H-v2/B iteration"* (see
`DRONE_OVERHAUL_OPTIONS.md`). It also promotes **D08 layer 1 (the dispatcher)
from speculation to evidence-backed**, because **registration determines which
hubs can deliver** — so the dispatcher acts on the 88%, while the claim gate
acts on a 12% slice that is already decided by the deliverer handoff.

**EXTERNAL-VALIDITY CAVEAT — the strongest objection to this whole result, and
it comes from the user (2026-07-29):** *"We are speed testing bug fixes in a
manner not what an organic player would be experiencing. We fill resource depots
with resources, we space things out to test distances. And because of that we
don't meticulously build bases or major industry domes with 100s of workers,
dozens of factories, and layers of extractors. Under that lens we could be
saying our complex dispatcher is worthless but in a real world with no magic
storage refilling it may be a very different situation."*
This is correct and it is a serious qualification. The A/B was **internally**
valid (tight controls, identical seeded set, same save, same speed) but its
conditions are **not representative of deployment**:
- **Depots were deliberately pre-filled**, removing resource scarcity and
  depot-choice contention entirely — the two things most likely to dominate
  hauling in a real base with no magic refills.
- **Layout is spread for distance testing**, not built the way a player builds.
- **The colony is massively over-provisioned with drones.** The DroneReport in
  the same sitting shows hubs at 24-25 drones with 14-24 IDLE. **The claim gate
  only acts under contention** — it withholds work from a far hub while the near
  hub has idle drones — so a colony where nearly every hub always has spare
  idle drones has almost no races left to arbitrate. **That plausibly explains
  `vetoed +1` far better than "the gate does not work":** the near fleet was
  already winning on its own, so there was nothing to veto. The original symptom
  that motivated D06 (four idle drones parked while a far hub crawled over) was
  observed in ORGANIC play, not in a cheat-prepared colony.
**Consequence:** this run may have engineered away the very phenomenon it was
built to measure. A representative re-test would right-size drone counts toward
the advisory's suggestion (raising contention), NOT pre-fill depots, and run
against real industrial density during a genuine demand surge.
**What survives the objection regardless:** the delivering-drone handoff
(`StartWorkPhase(drone)` → `SetCommandKeepQueue`) is **structural**, not a
conditions artifact — it holds at any base density, so "the metric counted
deliveries, not claims" stands. The 88% hauling share could shift under scarcity
but is unlikely to invert.
**THE INVERSION — the same artificiality is evidence the problem is WORSE than
measured, not smaller (user, 2026-07-29):** *"the fact that I notice lags in a
cheat filled environment, the issue is vastly worse to a normal player."*
This is the right reading and the run contains its proof. **Under pre-filled
depots and hubs carrying 14-24 IDLE drones each — a best case a real colony
never sees — the numbers were still bad:**
- mean break→work **3h03m** just to get a maintenance resource delivered, from
  depots that could not run out;
- worst total **9h24m** (`PolymerPlant:2058`);
- **`MartianUniversity:2895` waited 11h48m for its resource and was still
  unrepaired when the run timed out at 12h.** With full depots and idle drones
  everywhere. That is not a scarcity failure; it is a dispatch/hauling failure,
  and it is the single most damning figure in the run.
A normal player has scarce Electronics, tight drone counts, and dense industry
competing for the same fleets. If the symptom is this visible at best case, the
lived experience is materially worse. **So the null result must NOT be read as
"the problem is small."** It says our *instrument* could not see the claim
gate's mechanism — while the surrounding data independently confirms the
underlying problem is severe.
**CORRECTION (2026-07-29, same sitting): the "layout may be inflating distance"
caveat is WITHDRAWN — the evidence contradicts it.** It was written on the
assumption that test spacing had spread the colony out. Screenshots of the
actual base show the opposite, and the user confirms the layout is deliberately
optimised for drone access:
- domes **clustered tightly and passage-linked**, not scattered;
- **depot and stockpile arrays sited directly against the dome perimeters**,
  with extractors and factories ringed close in — short haul legs by design;
- **depots run min-balance thresholds so shuttles rebalance them**, plus
  **2 shuttle hubs**, so stock is actively kept where it is needed;
- **paths built over passages** specifically so drones navigate cleanly.
So distance is **not** an aggravating artifact here — it is another axis on
which this colony is BETTER than a typical player's, alongside supply, drone
count and tech. **That makes the inversion argument stronger, not weaker:** the
3h03m mean delivery, the 9h24m worst case, and `MartianUniversity`'s 11h48m
unrepaired timeout all happened in a colony deliberately engineered to make
drone logistics easy. There is no remaining "the test was unfair to the drones"
explanation. Every environmental axis we can identify is favourable, and the
numbers are still bad.
**Interesting interaction worth building on:** the D08 drone-count advisory and
the claim gate are **complementary, not independent** — right-sizing fleets
increases contention, which is exactly the condition under which the gate earns
its keep. Over-provisioning is how players hide the dispatch problem, and it is
also how this test hid it.
**Caveats, stated so this is not over-read:** n=25 with a single run per leg, so
the +2 on closest-hub is well inside noise. Leg A contains one pathological
outlier (`MartianUniversity:2895`, break→work 11h48m, never repaired, run timed
out at 12h) which alone inflates its hauling mean — excluding it moves 3h03m to
roughly 2h41m and shrinks the headline gap considerably. The legs also ended on
different conditions (timeout vs all-repaired). **This run does NOT prove the
module is useless** — it proves this test cannot measure it, and that the
post-malfunction repair path it targets is mostly bypassed when maintenance
requires resources. Dust/clean work and `no_resource` buildings were not sampled
at all (0 of 25).
**QA REVIEW VERDICT + USER DECISION (2026-07-29, fresh-context session).** The
QA review verified every load-bearing claim above at source level (delivering-
drone handoff structural, `RequiresMaintenance.lua:418-426`/`:190-198`;
`FindTask` sole caller `Drone.lua:621`) and added two corrections: (1) the run's
colony was at the **vanilla drone-stat ceiling** — live `GetMoveSpeed() = 2304`
= 1440 × (+20% Low-G Drive, +40% Advanced Drone Drive breakthrough, additive),
2× carry via Artificial Muscles — so the 88% hauling share stands *despite*
maxed stats; (2) **the 88% does NOT by itself promote the D08 dispatcher** —
the targets were overlap-scope with idle drones at every covering hub, so
awareness was not the shortage; the number needs decomposing into queue-latency
vs travel before any structural build. **Decision:** the claim gate is kept but
demoted (no further investment until the instrument can score it); the overhaul
will ship **Mod Options stat dials** (speed ×1.0/1.5/2.0, carry +0/+1/+2 —
capability verified, `Mod.lua:2708-2771`) as player-facing relief; the
structural choice (maintenance priority escalation vs D08 layer-1 dispatcher)
is gated on the request-lifecycle instrumentation. Full record: the DECISION
section in `DRONE_OVERHAUL_OPTIONS.md`; instrument work:
`HARNESS_REVIEW_PROMPT.md` (executed and deleted — see the rebuild note below).
**INSTRUMENT REBUILT (v2) + TWO NEW STRUCTURAL FINDINGS (2026-07-29, harness
repair session).** `TestKit/Code/91_Stress.lua` was rebuilt around per-request
lifecycle tracing exactly as the QA review recommended: run-scoped chained
wrappers on the bare globals `RequestAssignUnit`/`RequestUnitFulfill`
(`_TaskRequest.lua:352,412` — ALL drone/rover/shuttle claim+fulfill traffic
routes through them, no caller aliases them) plus classdef-time chained
wrappers on `StartDemandPhase`/`StartWorkPhase`/`Repair`. Every repair now
decomposes into haul queue / haul exec / claim wait / travel / repair; the
closest-hub score is computed only over the FindTask-decided cohort; every
summary prints a run-conditions header (module, speed, live drone stats,
per-hub idle, shuttle fleet, pre-surge depot availability); stat-dial legs are
first-class (`label=`, condition-mismatch warnings in `Compare()`). Two source
facts found during the rebuild **change how the first run's numbers read**:
1. **`SetCommandKeepQueue` preempts immediately** (terminates the current
   command, keeps the queue — `CommonLua\Classes\CommandObject.lua:564-569`),
   so a successful deliverer handoff claims the repair within seconds of
   unload. **The near-uniform ~57m work→claim measured in BOTH legs therefore
   CANNOT have been the handoff** — the "26/27 claims ≈ deliverer performed
   the repair" reading above is inconsistent with a 57m gap. Something else
   produced it (candidate below; v1's poll-resolution anchors could not tell).
2. **Shuttle deliveries MISFIRE the handoff** — `ShuttleHub.lua:1014` passes
   the CargoShuttle itself to `DroneUnloadResource` → `StartWorkPhase(shuttle)`
   → `shuttle:SetCommandKeepQueue("Work", …)`, but `CargoShuttle` has **no
   `Work` method anywhere in its ancestry** (only `Drone:Work` and
   `BaseRover:Work` exist tree-wide). The repair request falls back into the
   normal hub queues, where `FindTask` — and therefore the claim gate — DOES
   arbitrate it. On a colony with 2 shuttle hubs and min-balance depots (this
   one), the gate may be far less bypassed than the null result implied; it
   also means **which unit type hauls decides whether the gate ever sees the
   claim**. (Also a vanilla defect candidate in its own right — a
   shuttle-delivered malfunction always takes the slow claim path, and likely
   logs an engine error per misfire; consider filing as its own entry.)
   The v2 harness records deliverer identity, handoff capability, and
   misfire counts per target, so the next run settles which story the 57m
   belongs to — and whether `vetoed +1` was "nothing to arbitrate" (all
   handoffs) or "gate conditions never matched" (FindTask claims the gate
   declined to veto).
The design defect behind the 2026-07-27 live report (four idle drones parked beside a
malfunctioning building while a far hub serviced everything slowly): assignment is
pull-only and own-hub-only, requests sit in every covering hub's queues, claims are
first-poller-wins held through the whole approach, repair requests are max_units=1,
and no handoff/steal/distance-tiebreak exists anywhere. Full trace on the "Not yet
swept" DroneControl bullet; the option analysis (A-H, feasibility/risk/reward) is
`docs/reports/DRONE_OVERHAUL_OPTIONS.md`. **Core v1 ships three parts** (all
per-call-gated on `IsActive`, hooks installed at classdef time; no GameVars, no
object fields — ~~NO persisted state — saves made with it load identically without
it~~ ⚠️ **THAT CLAIM WAS FALSE AND IS STRUCK, 2026-08-01.** It counted
*declarative* state only. Frames are persisted state too: the part-2 hook was
installed at FILE SCOPE and sat below `Drone:Idle`'s sleeps, so every drone parked
in `Idle` at save time serialised it — **F86 Site 2, 98 errors per session, and it
happened with the module's own toggle OFF.** Corrected in the module header the
same day; the mechanism now lives in `ENGINE_FACTS.md` ("OFF" is three different
things). Site 2 was repaired and verified 2026-08-01 (PT-58), but the *reasoning*
error is the thing to remember: **"no GameVars" is not "nothing in the save"**):
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

### D07 — Cohort domes: no way to consolidate seniors/children without filter micromanagement (design, med)  `[built 2026-07-28: Code/Opt_CohortHousing.lua (opt-in, off by default, Mod Options toggle "Cohort housing — Seniors & Children") — user go given the same evening after config confirmation; A/B pair clean; PT-53 3-of-5 PASS 2026-07-29 — cross-dome moves (trains/passages/shuttles by distance), graduation drain, and organic no-churn-when-no-slots all confirmed live, "worked wonderfully"; only the employed-senior exemption (A) and precedence/uninstall (E) still owed, so NOT yet tested]`
**FIRST LIVE ENABLE — PT-53 partial, 2026-07-29 (user, unprompted during the
disaster sitting): "it worked wonderfully."**
- **Trigger B (cross-dome move) — PASS, and stronger than the test asked for.**
  Children travelled from **every** dome to the children's dome, and seniors
  likewise, **using multiple transport modes — trains, passages, and shuttles —
  chosen by distance.** That exercises the whole cross-dome path: the
  `FindEmigrationDome` post-wrap picking the nearest reachable cohort slot, the
  tie rule bypassed, and the shipped trip machinery carrying them by whatever
  mode fits. No ping-ponging or stuck-mid-trip reported.
- **Trigger D (graduation drain) — PASS.** Children ageing up **briefly became
  homeless and then moved out of the dome**. That is the designed shape: the
  `ColonistBecameYouth` nudge frees the Nursery slot, the colonist is
  momentarily unhoused, and vanilla's need-work migration drains them toward
  production domes. **Recorded as an observation, not a defect** — a player
  watching the Homeless counter will see a transient spike on every graduation
  wave, and that is expected.
- **Bonus finding — live corroboration of F79.** Children in the cohort dome
  **used PASSAGES to reach the retirement dome for services.** That is exactly
  the mechanism F79 describes: `Dome:GetService` is passage-only, so
  service-seeking works over passages and never over trains. It also confirms
  the D07 scope note that a cohort dome still needs services reachable by
  passage or staffed locally.
- **Trigger C (leave-alone / no churn) — PASS, and observed ORGANICALLY.** Where
  there was not enough cohort housing, those colonists "continued staying in
  their previous residence with no hiccups." This is stronger evidence than the
  scripted version of the test: rather than deliberately filling every slot, the
  shortage arose naturally across a large multi-dome colony and the module
  simply went quiet — no repeated move attempts, no emigration churn, no log
  noise. That is the designed "completely untouched when no cohort slot exists"
  behaviour, confirmed at colony scale.
**STILL UNREPORTED — this is why the status is PARTIAL, not `tested`:**
Trigger A (an unemployed Senior re-homing to a free Retirement Home slot in the
SAME dome, and — the important half — an **EMPLOYED** Senior in that same dome
NOT moving), and Trigger E (manual residence assignment must win; toggle off =
instantly vanilla — ~~save with it ON and reload with it OFF loads clean~~
**→ save with it ON and reload with the pack disabled in the MOD MANAGER**).
⚠️ **METHOD CORRECTED 2026-08-01 — a toggle CANNOT answer an uninstall question.** With the module merely switched off the mod env is still present and the hooks are still installed, so any captured frame resolves `SMRFixPack`, reads inactive and no-ops: **it reads clean by construction, whether or not the module leaks.** `Opt_DroneOverhaul` leaked at 98 errors/session with its own toggle OFF — that is how F86 Site 2 was found. Use **Mod-Manager-disable** (measured equivalent to a real uninstall, PT-20: 98 vs 98 on the same save). `ENGINE_FACTS.md`, "OFF" IS THREE DIFFERENT THINGS.
Everything reported so far is either a positive case or the do-nothing case;
what remains is the "never moves someone it shouldn't" pair.
**The want (user, 2026-07-28, after building a live retirement dome):** a
dome whose PRIMARY role is absorbing a non-worker cohort (seniors, and
separately children with their schools/playgrounds) out of the production
domes — without making cohort housing mandatory colony-wide, and without
banning normal residents (service workers live there too). Vanilla's only
lever is trait-filter micromanagement, and the emigration eval's
strict-inequality rule (`FindEmigrationDome`, `Colonist.lua:2680` — ties
never move) means comfortable cohort members simply stay put even with
space available; the classic original-game frustration, mechanics
unchanged in Relaunched.
**Spec REVISED same day (user refinement): COLONIST/HOUSING-level rule, no
dome designation at all — `Opt_CohortHousing` (opt-in module, off by
default, one Mod Options toggle).** The rule: a cohort member living in
NON-cohort housing gets moved into cohort-specific housing (Retirement
Home / Nursery classes) wherever it has a free slot — same dome (plain
residence reassignment) or cross-dome (emigration); **left completely
alone when no cohort slot exists anywhere.** The "retirement dome" emerges
from where the player concentrates the cohort buildings; no UI to build,
ZERO persisted state.
- **Forced migration (cross-dome half):** post-wrap
  `Colonist:FindEmigrationDome` (plain method, single Src definition).
  Senior-trait colonists (EXEMPT if employed — Forever Young seniors keep
  their jobs) and Child-trait colonists route to the nearest reachable
  dome whose COHORT housing has a free slot — bypassing the tie rule —
  IFF it passes `CanAcceptNewColonists` (quarantine + D03 closed-toggle
  compose automatically) and a transport mode exists
  (`FindTransportationModeToCommunity` — walk/passage/shuttle/train all
  work, `MigrateByTrain` live-proven 2026-07-28). Player-forced domes
  (`CheckForcedDome`) keep absolute precedence. Cohort members already IN
  cohort housing are never touched.
- **In-dome half:** a periodic pass (or a hook on the residence
  re-evaluation) moves cohort members from normal residences into a free
  cohort slot in the SAME dome first — cheapest move wins; only when the
  local cohort housing is full does the cross-dome branch look further.
- **Graduation is free:** when the Child trait drops at age-up the pin
  releases and the now-jobless worker hits the vanilla `better_home_work`
  branch (need-work migration bypasses the tie rule) and drains to the
  production domes naturally. Optional polish: additive OnMsg on the
  age-group transition for an immediate re-eval instead of the periodic
  pass.
- **Player-facing caveat for the description:** a children's dome still
  needs staffed services unless designed serviceless — commuting adults
  cover it (work commutes are unaffected by F79; only service-seeking
  trips don't ride).
All patch points verified in Src this session; zero persisted state beyond
the two dome flags. Cross-refs: D03 (UI + policy pattern, closed-toggle
composition), F79/F80 (train findings from the same sitting), the
FindEmigrationDome walkthrough in the 2026-07-28 session record.
**BUILT as speced 2026-07-28 (game-free leg, user go given after confirming
the config: in-dome-first + cross-dome reach, Seniors+Children one toggle).**
Implementation notes (`Code/Opt_CohortHousing.lua`): in-dome pass =
post-wrapper on `Colonist:UpdateResidence` (declared on Colonist,
Colonist.lua:2309 — runs from the Idle heavy update, so no new scheduling);
cross-dome pass = post-wrapper on `Colonist:FindEmigrationDome` picking the
NEAREST reachable community with a free cohort slot (reuses the shipped
candidate gathering incl. elevator-linked cities and
FindTransportationModeToCommunity; overpopulated communities skipped,
mirroring HasFreeLivingSpaceFor's gate); graduation nudge = additive
`OnMsg.ColonistBecameYouth` (Colonist.lua:1751) triggering an immediate
UpdateResidence. ZERO persisted state (the earlier "two dome flags" wording
predates the housing-level revision — the built module writes nothing to any
object). Cohort detection = `residence.exclusive_trait` ("Child" via
children_only, Residence.lua:26-28; "Senior" from the SeniorsResidence
template). Employed-senior exemption reads IsValid(workplace) OR a pending
user_forced_workplace. TestKit probe drives both wrappers with stand-ins
(8 cases: both moves, tie-bypass, employed/forced/no-slot/quarantine/
non-cohort negatives). A/B 2026-07-28 late: baseline 1/57/15/0 ·
all-six-toggles 63/0/10/0 (71/71 applied), zero errors. PT-53 pending.

### D09 — Drone speed & carry capacity dials (design, med)  `[tested 2026-07-30 — PT-56 PASS IN FULL: Code/Opt_DroneStatDials.lua — Mod Options choice dials "Drone speed" (1x/2x/3x/5x) and "Drone carry capacity" (+0/+1/+2); base = vanilla; all four steps passed live incl. the stale-save reconcile]`

**PT-56 PASS IN FULL — 2026-07-30, live, on a one-speed-tech save.** All four
steps, exact numbers, no residue:

| Step | Read | Verdict |
|---|---|---|
| 1. Baseline (dials at base) | `speed=1728 carry=1 dials=active` | 1728 = 1440 × 1.2 (Low-G Drive only); no Artificial Muscles |
| 2. Speed 2x + carry +1, Apply | `speed=3168 carry=2 dials=active` | **+1440 exactly** — 100% of the 1440 BASE, additive with the tech, not a doubling of the current value; carry +1 |
| 3. Both dials back to base, Apply | `speed=1728 carry=1 dials=active` | exact restore, live, no relaunch; still `active` (armed-at-base, by design) |
| 4. **Stale-save reconcile** | save made with dials at 2x/+1 → dials set to base + Apply → **base confirmed live first** (`speed_dial=1x (base) carry_dial=+0 (base) speed=1728 carry=1`) → load that save → `speed=1728 carry=1` | **PASS** — the modifiers baked into the save were stripped on load to match the current dials |

Step 4 is the one no probe can reach, and it is the FIX_POLICY §3 requirement:
persisted modifiers from a save must not survive into a session whose dials say
base. **Method note worth keeping:** the first attempt at step 4 read
`3168/2` and looked like a FAIL — the dials had simply not been set back to base
before the load, so the reading was correct behaviour. It was caught by reading
the DIAL POSITIONS alongside the values
(`Mods["SMR_CommunityFixPack"].options.DroneSpeedDial`) instead of the values
alone. Any future re-run should verify the base state *going into* the load as
its own step; scoring step 4 without it is a coin flip.

**Log swept clean per PT-22** (log `Mars.exe-20260730-19.37.47`): every module
`applied`, zero `[CommunityFixPack]` error/inactive/disabled lines, and the only
`Error` lines in the whole session are the two known pre-existing `ResManager`
`LawOfficeDoor` animation entries. The four `MeteorFrequency: persisted Meteors
thread on load was DEAD — restarting with the fixed body` lines are F02's
watchdog doing its job across the four loads the sitting made, not a fault.

**Observability gap noted (not a defect):** the module logs nothing when it
reconciles, so the log cannot confirm whether a stale-save strip ran — the
verdict had to come from live reads. If D10 reuses this machinery, a one-line
`ModLog` on reconcile would make the same test self-evidencing.


**⚠️ LIVE STATE — read this before running PT-56.**

1. **RESOLVED 2026-07-30 19.32 — the owner set both dials to base** (and all six
   toggles off; the `67/73` leg confirms the toggles). **PT-56 can run as
   written.** The history is worth keeping because it will recur: the 17.25 leg
   read `DroneResourceCarryAmount = 3` where a techs-only save reads 2 — the
   carry dial had been left at **+1** by that day's playtest (the same account
   change that produced `74/74` toggles-on instead of a default-config `68/74`).
   Dials are account-persistent, so **one Mod Options visit puts this back**, and
   PT-56 step 1 would then record an already-modified value as its "baseline"
   with every later comparison off by the dial. **Re-read the state; do not
   trust this line.** Note a green D09 probe is NOT that confirmation — the
   repaired probe forces base internally and is immune to account state by
   design; it does now *report* the state it found on entry, which is the read
   to look for.

2. **~~The probe is STATE-DEPENDENT~~ — TESTKIT DEFECT, REPAIRED 2026-07-30
   late; verified green the same evening.** `60_Probes_Opt.lua` used to do
   `local base_carry = consts.DroneResourceCarryAmount` and then assert
   `base_carry + 1`, which only holds if the dial is already at base. With the
   dial at +1 it FAILed (`+1 carry dial: DroneResourceCarryAmount 3 → 2
   (want 4)`) while the module itself logged `applied` and the leg carried
   **zero** `[CommunityFixPack]` error/inactive lines — a probe defect, never a
   pack defect. **The probe now forces both dials to base through the real
   Apply path, takes its baseline from that state, and restores the leg's entry
   values**; its cleanup check compares against the value read on entry, so it
   is exact for any account state. Confirmed on the **2026-07-30 19.20 leg with
   the account dial still at +1** — the exact state that FAILed it hours
   earlier — reporting `carry +1 over probe-forced base 1`. Same family as the
   2026-07-29 falls-off-the-end-returns-SKIP trap: a probe whose verdict
   depended on ambient state it did not set. **A DroneStatDials probe verdict
   no longer depends on how the last playtest left the dials** (the human
   playtest's own baseline reads still do — see item 1).
Player-facing stat dials for drone speed and carry capacity, decided post-QA
2026-07-29 (`DRONE_OVERHAUL_OPTIONS.md` DECISION): relief for big colonies and
breakthrough-lottery insurance, NOT the fix for the structural hauling problem —
the A/B save was AT the vanilla stat ceiling and hauling was still 88% of
elapsed repair time. **Dial range widened from the DECISION's 1.0x/1.5x/2.0x to
1x/2x/3x/5x by user call the same day, pre-build, after the no-clamp probe.**
- **Mechanism — the techs' own machinery** (`Effect_ModifyLabel`,
  MarsGameEffects.lua:161-178). Speed: percent Modifier on UIColony label
  "Drone" prop `move_speed` (+100/+200/+400), identical to Advanced Drone
  Drive (TechPreset.lua:702-706, +40) / Low-G Drive (+20); percents stack
  ADDITIVELY on base (Modifiers.lua:100,112-113), worst case 5x + both
  breakthroughs = 1440 × 5.6 = 8064. Carry: amount Modifier on label "Consts"
  prop `DroneResourceCarryAmount` (base 1, __const.lua:637-641), identical to
  Artificial Muscles (TechPreset.lua:626-630, +1); consumed Drone.lua:719,
  auto-rebuilt via ConstValueChanged (Drone.lua:724). New drones inherit label
  modifiers automatically (LabelContainer:AddToLabel, LabelContainer.lua:17-28).
- **Reconcile points:** OnMsg.ApplyModOptions (live, both directions),
  OnMsg.CityStart (new game), OnMsg.PostLoadGame (stale persisted modifiers in
  a loaded save replaced/removed to match current dials). Idempotent via
  SetLabelModifier same-id replace (LabelContainer.lua:59-78). Modifier ids
  `SMRFixPack_DroneSpeedDial` / `SMRFixPack_DroneCarryDial`. Choice values
  arrive as the choice STRING itself (Mod.lua:2764-2771) — mapped in code;
  unknown/missing reads as base.
- **Not a toggle module:** option names ≠ Register id (`DroneStatDials`);
  registers WITHOUT `optional` (00_Core's boolean reconciler must not manage
  it); reports `active` whenever targets validate — active at base = armed,
  behavior byte-vanilla. FIX_POLICY §5 dial addendum covers the shape.
- **Save-safety (FIX_POLICY §3):** base position, veto or error status removes
  the modifiers BY ID, including cleaning stale ones out of loaded saves.
  Uninstalling with a dial active leaves benign vanilla `Modifier` residue
  (string keys, vanilla class — loads clean without the mod, keeps the boost
  permanently); set dials to base first — documented in MOD_DESCRIPTION.
- **C-side clamp check DONE live 2026-07-29 (user probe, screenshot on file):**
  `SelectedObj:SetMoveSpeed(10000)` → `GetMoveSpeed()` = 10000 — NO C-side
  clamp; at 10000 on ultra sim speed (~35x the dial's worst-case relative
  throughput) movement stayed clean: no frame skips, clipping, pathing
  failures or stuck states. Probe drone restored to 2304 afterwards. The 5x
  dial's headroom is proven, not inferred.
- Playtest: PT-56 (checklist §2) — apply/stack reads, live removal, stale-save
  reconcile. PASS flips this entry to tested (both places).
- **A/B 2026-07-29/30 (unattended set, 77 probes, all three legs):** baseline
  **1/61/15/0** (dial probe FAILs "fix pack not loaded" by design) · default
  config, six toggles OFF **62/0/15/0 at 69/75** · all-six-toggles
  **67/0/10/0 at 75/75** — the DroneStatDials probe drives the REAL Apply
  path (rawset on `Mods[pack].options` + `Msg("ApplyModOptions")`) and PASSes
  in BOTH fixed legs, both directions: 2x/+1 land as label modifiers
  (move_speed +100, carry +1), base removes both by id — the dials work
  independently of the toggle modules. Logs clean in every leg. **Two lessons
  paid for en route:** (1) the module's first install check read
  `Modifier.new` at file scope — the F64 pre-flattening trap (`new` is
  inherited, invisible on the classdef); presence-only at file scope,
  capability check moved to the reapply guard. (2) `CurrentModOptions` is
  per-mod-env — the probe's first version wrote the TestKit's own options
  object (ENGINE_FACTS fact added).
- **A/B 2026-07-30 late (log `Mars.exe-20260730-19.20.24`, unattended, 76
  probes): `73/73 fixes active`, `66 PASS / 0 FAIL / 10 SKIP / 0 ERROR`.** The
  first leg run after the F28 removal and after the probe repair, and it clears
  both: the counts land exactly where the removal predicted, and **the dial
  probe is GREEN with the account carry dial still at +1** — the state that
  FAILed it on the 17.25 leg. The account still had all six toggles ON, hence
  `73/73` rather than a default-config `67/73`. Zero `[CommunityFixPack]`
  error/inactive/disabled lines; no log line names our `Code/`; noise profile
  identical to the previous leg. **This does NOT flip D09 to `tested`** — only
  the playtest does that, and PT-56's stale-save reconcile step is beyond any
  probe.
- **A/B 2026-07-30 19.32 — default config** (log `Mars.exe-20260730-19.32.16`,
  76 probes, unattended after the owner set all six toggles OFF and both dials to
  base): **`67/73` active, `61 PASS / 0 FAIL / 15 SKIP / 0 ERROR`**, predicted
  before the run and landing exactly. **`DroneStatDials` PASSes here too**, with
  the five opt-module probes SKIPping as `inactive (opt-in)` around it — the
  dials are confirmed independent of the toggle modules in the shipping default
  configuration, not just with everything switched on.

### D10 — Workshops: capacity can't scale late-game; unemployment's real cost is invisible (design, med)  `[speced 2026-07-30, user-approved same day — ⭐⭐ **BUILD UNHELD 2026-08-01: the F86 save-safety hold is DISCHARGED** (owner's condition was "repairs land AND verify" — Tier 1 verified `c6180ad`, Tier 2 verified by PT-58 with F86 Site 2 closed at zero against leg 5's 80). Chain prompt 9 is runnable. GATE OPEN: PT-56 PASSED IN FULL 2026-07-30, so the build is UNBLOCKED and ready to start. (The gate existed because the capacity dial reuses D09's label-modifier machinery and its first live check hadn't run.) One Opt_ module, planned PT-57]`
**Problem (research session 2026-07-30, all source-verified).** The three
vocation Workshops (Art/VR/Biorobotics, build category "Workshops") are the
designed late-game employment+resource sink: they produce nothing, consume
Polymers/Electronics/MachineParts, and pay workers **+10 Morale**
(`WorkInWorkshopMoraleBoost` = 10000, `__const.lua:1737-1743`, applied
`Colonist.lua:3975-3976`) and up to **+5 Comfort** × performance per fulfilled
shift (`WorkInWorkshopComfortBoost` = 5000, applied `ArtWorkshop.lua:24-27`).
Two failures:
1. **Scale:** 6-10 workers/shift (VR 10, Biorobotics 6) against late-game
   unemployment in the hundreds — the "solution" is carpeting domes with
   copies.
2. **Legibility:** unemployment has NO colonist-level penalty
   (`StatusEffect_Unemployed` is icon-only, `StatusEffects.lua:74-81`; zero
   stat modifiers in Colonist.lua) — but in Relaunched EVERY faction def
   carries unemployment clauses, e.g. Workers' Party `CollectiveUnemployment`:
   a dome ≥10% unemployed costs **-900..-3000 approval**
   (`WorkersParty.lua:103-121`). Nothing in the building descriptions, the
   Unemployed rollover, or the build menu says any of this — the community
   still repeats the original game's "no penalty, ignore it" advice, and the
   Workshops flyout sits over the Stores row labeled only "Art Workshop",
   reading as a store variant (user observation, screenshot on file).

**Spec — one opt-in module (`Opt_WorkshopsRole`), two halves:**
- **T1 — text repairs (default-on within the module, vetoable):** append the
  real mechanics to the three workshop template descriptions (T(8821)/
  T(8818)/T(8827)) — the ≥10% unemployment faction-approval cost and the
  sink role — and to the `StatusEffect_Unemployed` rollover
  (`StatusEffects.lua:76-77`, classdef field patch). Template descriptions
  patch post-DataLoaded (F75 latch; TechDescriptionBuilding/MultipleSuns
  precedents). New strings via `Untranslated()` (FIX_POLICY §6). Repairs
  actively-misleading text — same family as F65's description drift.
  *Build-time option, default OFF: "Vocation:" display-name prefix to break
  the store association — cosmetic, user tunes at build.*
- **T2 — capacity dial (Mod Options choice, D09 pattern):** "Workshop
  capacity: base / +50% / +100%" → colony label modifiers (module-owned ids)
  on the three template-id labels `ArtWorkshop`/`VRWorkshop`/
  `BioroboticsWorkshop`, **paired props**: `max_workers` AND
  `consumption_amount`, same percent. The pairing is load-bearing:
  consumption is fraction-of-capacity × `consumption_amount`
  (`ArtWorkshop.lua:35-39`), so raising capacity alone silently CUTS
  per-worker resource cost; pairing keeps it exactly vanilla. Both props are
  modifiable (`consumption_amount`: `HasConsumption.lua:47` `modifiable =
  true`; `max_workers`: the workshops' own upgrade1 modifies it, so
  live-change incl. worker unassignment on dial-down is a vanilla path).
  Precedent for template-id colony labels: the vanilla WindTurbine fixup
  (`WindTurbine.lua:78-88`) and this pack's SaveSanitizer restore. Reconcile
  on ApplyModOptions/CityStart/PostLoadGame; base = modifiers removed by id =
  byte-vanilla; benign-residue uninstall story identical to D09.
- **Why a dial and not base-stat/tech changes (user's call, 2026-07-30):**
  a flat base increase would distort the mid-game era where 6-10 slots is
  meaningful; a new TechPreset drags in research-UI integration and a bigger
  playtest. The dial defaults to base and is account-scoped player intent.
- **PARKED UNTIL AFTER LAUNCH (owner, 2026-07-31 — `docs/FUTURE_IDEAS.md`
  entry 1):** seniors-in-workshops ("vocation in retirement") — needs
  work-eligibility surgery and interacts with D07's employed-senior exemption
  (senior workshop workers would stop cohort-migrating). **It is not a deferred
  decision any more, it is parked: not owed, not scheduled, and not to be
  reported as outstanding.** Do not build it as a rider on D10.

**Planned playtest (PT-57, added to the checklist at build time):** tooltip
reads (T1); dial infopanel check on a live workshop (slots and consumption
shift together, +50%/+100%); dial-down mid-shift → excess workers unassigned
cleanly; stale-save reconcile (PT-56 step-4 shape). Estimated one ~7-minute
sitting.

### D11 — Shuttles fly ONE passenger per trip, even when several colonists share the same dome pair (design, low)  `[candidate 2026-07-30 — feasibility research ON FILE, **NOT GREEN-LIT: the user explicitly directed that this filing is NOT approval. Before ANY build work, ASK the user fresh and get an explicit go.** Multi-hop passenger routing was REJECTED by the user the same day — do not re-propose it]`
**Shuttle-limits reference (research 2026-07-30, all source-verified):**
- Three separate limits: cargo/shuttle = `max_shared_storage` **3**
  (`ShuttleHub.lua:415`, modifiable); passengers/shuttle = **1, structural**
  (one `ColonistTransportTask` per colonist; `transport_task.colonist`
  singular, `TransportColonist` `ShuttleHub.lua:635+`); shuttles/hub =
  `max_shuttles` **10** (`ShuttleHub.lua:1335`, modifiable).
- Buffs that exist: **HighPoweredJets** +3 cargo (the game's ONLY cargo buff,
  `TechPreset.lua:3977-3992`); **CompactHangars** +6 shuttles/hub;
  **MartianAerodynamics** +33% speed; storybit-granted **ShuttleAfterburners
  1/2** +10%/+25% speed at +50%/+100% hub fuel + temperature per flight;
  Relaunched law **Policy_ShuttleFuelEfficiency** -20% fuel (-10% more w/
  ministry). **NO breakthrough touches shuttles**; no law touches shuttle
  cargo (trains got +50% via `TrainCargoStandards`, same prop name).
- Trip shape: task atom = `{prio, supply_req, demand_req, resource}` — one
  source, one destination, ONE resource type; load =
  min(capacity, supply, demand) (`ShuttleHub.lua:857`). Leftovers chain a
  SECOND destination for the same resource or get DUMPED as a ground pile
  (`ShuttleHub.lua:1185-1200` — shipped comment: "noone wants this..dump it
  and go home"). Colonists debit the hold 1 unit each (`ShuttleHub.lua:652`);
  dispatcher round-robins people/cargo so neither starves
  (`LRManager.lua:148-150`). `GetMaxCargoShuttleCapacity` sums colony label
  modifiers on the `CargoShuttle` label (`ShuttleHub.lua:1686-1699`) — the
  engine expects external capacity modifiers (D09/D10 machinery).

**Feasibility sketch — same-pair passenger batching (the tractable variant):**
- Grouping is a filter, not new bookkeeping: `ColonistTransportTask` already
  carries `colonist`/`source_dome`/`dest_dome`/`source_landing_site`
  (`LRTransport.lua:91-96`); co-travelers = same dome pair + `CanExecute()`
  over `lr_manager.colonist_transport_tasks`.
- Hold fits N passengers natively (1 unit each → 3 base / 6 with Jets; scales
  with any capacity modifier for free).
- Save-safety shape: each passenger KEEPS their vanilla task object; the
  shuttle claims several, extras tracked in an `SMRFixPack_*` field (no
  modded classes in the save — D07/D09 pattern).
- **The hard 20%:** (1) boarding synchronization — the single-passenger flow
  already interrupts/waits/revalidates constantly; N-way needs per-passenger
  timeouts + depart-with-whoever-boarded + release-the-rest; (2) cancellation
  — task removal wakes the shuttle and aborts the trip
  (`LRTransport.lua:68-72`); batched, losing one passenger must NOT abort the
  flight; (3) mod-removed-mid-flight — extra attached colonists with
  unclaimed tasks need a DESIGNED landing per FIX_POLICY §3 (narrow window,
  flights are seconds).
- Scale: medium D-item (> D09/D10 stat work — this rewires a command thread;
  < D06). Synergy: D07 cohort waves generate exactly the same-pair bursts
  this optimizes. Honest ceiling: wave speed + fuel, not a systemic fix —
  the round-robin already prevents passenger starvation.

## Candidates under investigation

### D12 — Homeless strand in specialist domes; emigration ties never move them  `[SPECED 2026-07-30, user-approved — ⭐⭐ **BUILD UNHELD 2026-08-01: the F86 save-safety hold is DISCHARGED** (Tier 1 verified `c6180ad`; Tier 2 verified by PT-58, F86 Site 2 closed at zero against leg 5's 80). Chain prompt 10 is runnable. Build owed. Own module, Opt_ResidencyControl as donor pattern only]`

**Origin: found in play 2026-07-30**, by deliberately stressing homelessness and
unemployment in a dedicated child dome. Observed live: nurseries at 5/26 and
3/26 (**68 free Child slots**) with **28 homeless in the dome — 26 Youth, 2
Adult** — while a Child in a neighbouring dome commuted in to the school and
went home to a Smart Apartment. `accept_colonists` read `true`, so the
quarantine was NOT involved.

**Root cause — a vanilla tie rule, not a mod defect.** The shipped emigration
eval explicitly permits a homeless colonist to move to a dome with no free
housing (`Colonist.lua:2676`, comment: *"if homeless, try changing community
even if doesn't have living space available"*). But the gate above it requires
the candidate to score **strictly better** unless home or work improves
(`:2675`, `:2680-2681`). With zero non-cohort free slots colony-wide
`better_home` is false everywhere; with unemployment saturated `better_work` is
false too. Every candidate **ties**, and ties never move anyone. This is the
same tie rule D07's header already cites as the reason cohort members never
consolidate — it strands the graduates for exactly the same reason.

**Why it compounds (the D07 deadlock).** The stranded homeless push the dome
over `IsOverpopulated` (`#labels.Homeless >= g_Consts.OverpopulatedDome`,
`Dome.lua:1026-1035`), and D07's own cross-dome `consider()` skips
`community.overpopulated` (`Opt_CohortHousing.lua:194`) — so the child dome is
permanently excluded as a destination and no new Children ever arrive. **The
module poisons its own destination, and it tightens with every child it
delivers.** D12 breaks the loop at the cause: drain the homeless, the flag
clears, D07 resumes unaided.

**Rejected alternatives (recorded so they are not re-proposed).** Dropping
`or community.overpopulated` from D07's `consider()` was the obvious one-clause
fix; the user rejected it — it only stops D07 *noticing* the problem and leaves
homeless colonists stranded. Refusing to deliver children into domes with no
non-cohort housing was also rejected: it does not heal an already-poisoned dome.
Both are still on file if D12 proves impractical.

**Also settled, and NOT a defect:** the homeless youths themselves.
`non-cohort free slots colony-wide: 0`, so total homelessness is set by
(population − housing capacity). D07 changes *which* colonist lacks a bed, not
how many, and arguably improves utilisation by freeing ordinary slots for
adults. No F-number.

## WHAT D12 SHIPS

A per-dome / per-habitat **"no homeless residents"** policy: when set, homeless
colonists in that dome are moved to the nearest community that accepts them,
using the shipped emigration machinery.

**Hard constraint (the trap that killed the first design).** The flag must be
its **own field with its own gate** and must **NOT** route through
`Community:CanAcceptNewColonists`. D03's existing "closed to new residents" row
wraps exactly that method (`Opt_ResidencyControl.lua:35-37`), and D07's
`consider()` calls it (`Opt_CohortHousing.lua:193`) — so reusing D03's gate
would block cohort delivery into the very dome we are trying to protect. The two
controls must act in **opposite directions on the same dome simultaneously**:

| Flag | Child dome | Effect |
|---|---|---|
| `SMRFixPack_closed_to_new_residents` (D03, existing) | **off** | children can still migrate in |
| `SMRFixPack_no_homeless` (D12, new) | **on** | graduates are pushed out before they pile up |

**Mechanism — reuse D07's proven wrapper shape:**
* Post-wrapper on `Colonist:FindEmigrationDome` (declared on Colonist,
  `Colonist.lua:2581`; called every heavy update from
  `Colonist.lua:1894-1898`, so no new scheduling). When the colonist
  `IsHomeless()` and their own dome carries the flag, pick the **nearest
  reachable community that does NOT carry the flag** and that
  `CanAcceptNewColonists()`, bypassing the tie. Reuse the shipped candidate
  gathering and `FindTransportationModeToCommunity` exactly as D07 does —
  walk / passage / shuttle / train / elevator.
* **Never expel to the surface.** If no candidate qualifies, return the shipped
  answer unchanged and the colonist simply stays. Best-effort only. A colonist
  put outside with no dome dies (F53 territory) — this is the one failure mode
  the design must make structurally impossible.
* Ping-pong guard: only consider destinations WITHOUT the flag, so two flagged
  domes can never trade the same colonist back and forth.
* UI: a second toggle row on the dome / MicroG-habitat infopanel via the shipped
  `Community:TogglePolicy` / `SetPolicyState` machinery (`Community.lua:77-100`)
  — same idiom as D03's row, including Ctrl+click broadcast and the rogue-dome
  UI lock.

**Packaging decision (user, 2026-07-30): its own module**, with
`Opt_ResidencyControl` as the **donor pattern only** — copy the row-append and
policy-toggle approach, share no gate. Rationale: D03 is `tested` and shipping
(PT-49 in full, plus PT-55), and duplicating the infopanel-row machinery is
cheaper than re-qualifying a shipped module. The two behaviours are distinct
concepts — block entry vs. force exit.

**Defaults and safety:**
* Every dome defaults to **allowing** homeless (flag absent = vanilla). A module
  that stranded a whole colony on first enable would be unshippable.
* Opt-in module, off by default, per-call `IsActive` gate, file-scope install
  (the A2 lesson — FIX_POLICY §5).
* Savegame footprint per FIX_POLICY §3: `SMRFixPack_no_homeless` on the
  Dome/Habitat object, absent-tolerant both ways; the unmodded game never reads
  it and a save carrying it loads fine with the module or the pack removed.

**Precedence:** quarantine (`accept_colonists` false) wins absolutely — a sealed
dome neither admits nor releases anyone, matching the shipped early-out at
`Colonist.lua:2632-2635`. Player-forced dome (`CheckForcedDome`) wins over the
policy. The D03 row composes independently.

**Open question for the build:** whether the push should apply to ALL homeless
or only to colonists the dome can never house (i.e. no residence in the dome is
`IsSuitable` for them). The narrow reading is more surgical and is what the
child-dome case actually needs; the broad reading is simpler to explain to a
player. Decide before coding.

**PT owed:** a new item covering — set the flag on a nursery-only dome with
stranded graduates and watch them drain; confirm the dome's `overpopulated`
clears and D07 resumes delivering children unaided; confirm NO colonist is ever
left outside a dome; confirm a flagged dome with no valid destination leaves
its homeless in place rather than expelling them; toggle off = instantly
vanilla; ~~save with it ON, reload with the module OFF, clean load~~ **→ save with
it ON, reload with the pack disabled in the MOD MANAGER, clean load.**
⚠️ **METHOD CORRECTED 2026-08-01 — a toggle CANNOT answer an uninstall question.** With the module merely switched off the mod env is still present and the hooks are still installed, so any captured frame resolves `SMRFixPack`, reads inactive and no-ops: **it reads clean by construction, whether or not the module leaks.** `Opt_DroneOverhaul` leaked at 98 errors/session with its own toggle OFF — that is how F86 Site 2 was found. Use **Mod-Manager-disable** (measured equivalent to a real uninstall, PT-20: 98 vs 98 on the same save). `ENGINE_FACTS.md`, "OFF" IS THREE DIFFERENT THINGS.

**CHAIN CONFIRMED END TO END (2026-07-30).** The inferred link (step 4) was
measured live: `g_Consts.OverpopulatedDome` = **20**, and the child dome read
`overpopulated=true homeless=20`. So the flag is latched by the stranded
graduates exactly as traced, and nothing in the chain is now inference.

**Knife-edge, and useful for testing D12:** the threshold is `>=`, and the dome
sat at **exactly 20** (down from 28 earlier the same sitting, as a few drained
or died). Two more departures would clear `overpopulated` and D07 would resume
delivering unaided. So the deadlock is genuine but marginal — a D12 test must
confirm the drain is what cleared it, not natural attrition. Take a homeless
count immediately before setting the flag and immediately after.

### D13 — Save-exit deliverables: the uninstall procedure + the standalone save-rescue artifact (design, high)  `[directed 2026-07-31 (owner) — prelaunch deliverable. ⭐⭐ **SIZING INPUT PENDING, 2026-08-01: chain prompt 12 JOB 0.** If the "OFF is three different things" doctrine holds, this artifact's target population is NOT "players who used a module" but **every player who ever had the pack installed, whatever their toggles were** — because a toggled-off module still has its hooks installed and still seeds frames. That changes how much work this is. Owner-ordered re-verification against primary evidence before anything is scoped on it ("we cannot be wrong about this"); see `ENGINE_FACTS.md`, and note two of the four sub-claims are INFERRED, not measured. ⛔ SPEC GATED: not specced, not built, until Tier 1/2 land AND verify — its target list is their OUTPUT. **PROMOTED 2026-08-01 (owner) to a HARD LAUNCH DEPENDENCY: the pack does not ship until this ships alongside it** — "we won't launch till it does". The gate is a sequencing fact, not a priority judgement: the cleaner is specced LAST because it can only be designed against the residual set the builds leave behind. Also now the owner of the **complete per-site disposition table** required before release (FIX_POLICY §3a). Moved here from FUTURE_IDEAS entry 5 (2026-08-01) so that file's "nothing here is work" rule stays true]`

**✅ CONSOLE-CHANNEL INPUT LANDED 2026-08-01 (owner ran the Paradox Mods check;
audit §7.1 item (b), recorded in `BUG_LIST_AUDIT.md` §10.4).** The audit booked
this because "whether fredware/GromGor mirror there matters for D13". Answers:

- **The channel is live and a Relaunched fix author already uses it.** GromGor
  mirrors to Paradox Mods — an **exact mirror** of his Steam workshop, same
  titles. **fredware does not; he is Steam-only** (so his removed mod has no
  console-side copy either, and our archived FPK stays the only recoverable
  form of it).
- **The sharpened question for D13, which nobody has answered yet:** if this
  pack ever publishes to Paradox Mods, the uninstall story is **not** the Steam
  one. That audience has no console, so any rescue path that assumes typing
  into a console does not exist for them — which bears directly on whether the
  "standalone save-rescue artifact" can be a console procedure at all, or has
  to be something a console player can actually run. **Decide the channel
  before speccing the artifact**, because the answer changes what the artifact
  is. Not a decision this entry makes.
- ⚠️ **Discovery problem, recorded as an observation and not yet re-checked:**
  the owner found that searching Paradox Mods for `bug` or `fix` returns **zero
  hits**, while searching the author name `gromgor` surfaces his bug-fix-titled
  mods immediately. If that holds, **a pack named for the words "bug" and "fix"
  is undiscoverable by its own keywords on that channel** — a naming and
  listing problem for `MOD_DESCRIPTION.md`, not a code one. One browse; re-check
  before anything leans on it.

**⛔ D13 DERIVES THE EXPOSED SET ITSELF — IT MAY NOT INHERIT ANY COUNT FROM
THESE DOCS (owner, 2026-08-01).** The recorded numbers are **not** a closed
answer and must not be treated as one:

- The count is written as an **open lower bound** — *"at least 13"*, *"≥13"* —
  never as a determination. It was **12** on 2026-07-31, corrected to **13**
  the same day, and the membership was corrected **both ways** in the process
  (`Fix_DroneUnreachableForever` added, `Fix_TrainCargoDumping` removed).
- **The enumeration grep is known blind** to slot/global/preset assignments
  (`F86_ADJUDICATION.md` §3.1) — that blindness is *why* the bound is open.
- Tiers 1 and 2 then **changed the set from underneath the numbers** by
  repairing modules, so even a correct pre-build count is stale by
  construction.

**So D13 runs its own enumeration from source, over the current `Code/`, and
that result is authoritative.** It supersedes every number below on sight —
if D13's derivation disagrees with a recorded count, the recorded count is
wrong, not D13. Do the derivation FIRST; do not spec the cleaner against an
inherited list.

**Then update every place that states a count or a per-module denominator.**
Known locations as of 2026-08-01 (re-sweep before trusting this list — it is a
starting point, not a guarantee):

| file | what is there |
|---|---|
| `BUGS.md` F86 index row + `:4474`, `:4525`, `:4527`, `:4578` | "13", "at least 13", "12 exposed", "five of the twelve", the 13-not-12 correction |
| `BUGS.md:4593` (Phase-1 re-run block) + `:4747` | the five-shape re-derivation; **"Exposure list (12 modules)"** — a stale denominator |
| `STATUS.md:321`, `:336`, `:348`, `:368`, `:369`, `:385` | "≥13", "13 plus one inert route-(c)", **"12 in total"**, "five of the twelve", "the exposure list grew: 13, not 12" |
| `agent/FIX_POLICY.md:291` | "the 13 and one additional inert route-(c) site" |
| `agent/ENGINE_FACTS.md:259` | "**13** after two same-day membership corrections" |
| `reports/SAVE_SAFETY_REDESIGN.md:15`, `:58`, **`:188` (§3 "12 exposed")**, `:226`, `:352` (§5.2) | the per-module disposition table and its denominator |
| `reports/F86_ADJUDICATION.md:290`, `:543` | "at least 13 by its own definition", "≥13 with CaveIns compliant" |
| `reports/F86_DISCOVERY_POSITION.md:113`, `:119`, **`:131` (§4 "The exposure list (12 modules)")** | the original 12-module framing |
| `reports/F86_SESSION_FINDINGS.md:201` | **"Exposed set — 5 of 12 have a route out"** |

The four bolded rows are the stale **12**-denominators; the rest are already
reconciled to 13 but still carry an open bound. **D13 closes the bound and
makes all of them agree with its own derivation**, and records the disposition
table (FIX_POLICY §3a) against that same list.

**The owner's directive (2026-07-31):** the pack ships with its exit paved —
prelaunch, ready for the community post-launch. Two deliverables:

1. **The uninstall procedure** (player-facing, MOD_DESCRIPTION): "update to
   the latest pack, load your colony, save, then uninstall" — true because
   the Tier-1 latched heal + rains migration clear our threads from the save.
   Backup-first advice, honest residual disclosure (inert layer-2 residue;
   irreversible history). `[FAQ]`
2. **The standalone save-rescue artifact** for saves that already lost the
   pack — the only remedy that works on console (Paradox Mods reaches
   Xbox/PS5; no logs, no console commands, no hex-editing there).

**⛔ THE SPEC GATE (owner concern, 2026-08-01): scope it against what is LEFT
after Tier 1/2 — never against today's leak set.** The F86 build exists to
stop creating residue; a cleaner specced now would be built to clean things
that won't exist when it ships, and would grow to fit. Sequencing therefore:
Tier 1/2 land → verify (their PT-20-method uninstall leg) → THEN freeze this
spec against the measured leftover classes (expected: pre-rewrite-lineage
saves — dead `Meteors` threads, old-body rains loops; `SMRFixPack_*` instance
fields — fixture-measured inventory 919× `reserved_at` + 8 others; GameVars
from any era). Building in parallel with Tier 1/2 means building it twice.

**Second-artifact costs (all owed by the release checklist, WORKFLOW):** own
metadata, preview image, description, PDX portal pass, console cert — plus
**version-skew management**: the cleaner must state which pack versions'
residue it handles, and its own residue must be ZERO (a cleaner that marks
saves is a farce — so: purely synchronous, no threads, no GameVars).

**⚠️ OPEN DESIGN QUESTION (owner, deliberately not yet answered): what does
the player actually DO?** (a) Run-after-removal — the promise depends on the
player remembering a second step at the exact moment they've decided to stop
using our mods (though the broken-save case is self-motivating: they arrive
because something is wrong). (b) Keep-installed — then it is not a cleaner
but a permanent runtime. (c) The pack is its own cleaner and the standalone
artifact serves ONLY the already-removed case. The choice shapes the whole
artifact; it is taken when the spec gate opens, not before.

**Primitives inventory (moved from FUTURE_IDEAS entry 5, still current):**
- Global GT threads: `RestartGlobalGameTimeThread(name)` swept over
  `GlobalGameTimeThreads` rebuilds each from `GlobalGameTimeThreadFuncs` —
  with the pack absent, that is **vanilla's body**. Fully generic across mods.
- Command threads: re-issuing `SetCommand` discards a stale stack carrying a
  vanished mod's frame (rarely needed — they self-clean per the LuaSavegame
  doc's "new invocations" rule).
- Named fields/GameVars: removable where identifiably named.
- **Trap 1 — some residue must SURVIVE:** `90_SaveSanitizer` writes
  `SMRFixPack_F35_<label>` modifiers that ARE the repair; a delete-everything
  cleaner re-breaks the save. Curated keep/remove list required.
- **Trap 2 — restarting a thread resets its interval** (35-115 h for
  Meteors); bounded as a one-shot, never blanket-repeated.
- Detection is the hard part: the 2026-07-31 `rawget` sweep false-positived
  on 192 buildings twice. Enumerate by curated list, never by pattern-guess.

**Playtest owed when built:** its own PT — damaged pre-rewrite fixture save →
run artifact → verify vanilla threads alive, fields/GameVars per keep-list,
zero artifact residue after ITS removal, on a save then loaded with no mods.

Cross-refs: F86, F88, `F86_EXECUTION_PLAN.md` Phase 5, WORKFLOW save-exit
gates, D06 (the beta-response-channel framing this composes with).

### C01 — `BreakthroughOrder` rebuilt+reshuffled on every map load
`Lua\Buildings\Anomaly.lua:652-682` (`City:InitBreakThroughAnomalies`), called from
`InitCity` on every `NewMapLoaded` (`City.lua:477`); `BreakthroughOrder` is a savegame
GameVar. With asteroids, maps load repeatedly mid-game. Same family as the original B&B
"no planetary anomaly breakthroughs" bug (ChoGGi's fix: run once). Need to trace: how
markers/planetary anomalies consume the order; whether reshuffle causes duplicate or lost
breakthroughs. Surface call also `DoneObject`s markers (planetary reservation :667-674,
excess :676-681).

### C03–C11 — leads promoted from RESEARCH.md before its archiving (2026-07-29, audit remediation 3.4)

None are source-verified yet; each needs its own sweep before any becomes an
F-row. Provenance and the fuller lead lists live in
`docs/archive/RESEARCH.md`.

- **C03 — Research screen softlock; research progress >100%.** From the
  ChatGPT dossier. 1.0.5 patch notes claimed fixes in this area — regression-
  check the current source (the project's other "patch notes said fixed"
  collisions all turned out real).
- **C04 — Surface dust storms damage underground pipes.** Cross-map disaster
  leak: a surface disaster's damage pass reaching objects on the underground
  map. Sweep the dust-storm damage iteration for a map filter.
  **Witness upgrade 2026-08-01 (bug-list audit): an independent Relaunched fix
  exists** — GromGor's "No Underground supply grid breaks" (workshop
  3730839706): *"It's very strange to experience supply grid breaks
  underground during dust storms on the surface. This mod fixes it."*
  **MECHANISM CONFIRMED same day (his FPK extracted + Src read):** vanilla
  `SupplyGridFragment:RandomBreakConnection` (`SupplyGrid.lua:669-683`) picks
  its break victim via `table.rand(self.connectors, …)` with **no map
  filter**; his rewrite selects only connectors whose building's city map is
  `MainMap`. His fix working in the wild implies fragments can span maps (or
  the break pass reaches underground fragments), exactly as the lead
  suspected. Our own sweep still owed before an F-row: trace WHO calls
  `RandomBreakConnection` during a surface dust storm and how an underground
  connector enters `self.connectors`.
  ✅ **SWEPT 2026-08-01 (chain prompt 6) — BOTH QUESTIONS ANSWERED, C04 IS
  CLOSED AND PROMOTED TO `F90`.** Caller chain: `City:HourlyUpdate`
  (`Lua\City.lua:148-149`, gated on `HasDustStorm(self:GetMap())`) →
  `City:RandomBreakSupplyGrid` (:178-181) → `SupplyGrid:RandomBreakElements`
  (`SupplyGrid.lua:1017-1021`) → the map-blind `table.rand(self.connectors, …)`
  at :677. Entry route for the underground connector: `SupplyGridFragment`
  inherits **`MultiMapSupplyGrid`** (:337-338) and the elevator merges the two
  sides' fragments (`Elevator.lua:402-440` → global `MergeGrids`,
  `SupplyGrid.lua:1635-1650` → `AddElement` :547-548), while `AddCityElement`
  (:463-477) registers the merged fragment on **both** cities' lists. Intent
  tell: `HasDustStorm` is hard-gated to `MainMap` (`DustStorm.lua:41`) and the
  sibling production pass 16 lines above the break pass **does** guard the
  shared-fragment case, with a comment saying why (:999-1001). Full evidence
  trail, reachability, fix-shape constraints and the two open scope questions
  are on the **F90** entry. No fix built — decision package is prompt 7's.
- **C05 — Colonists repeatedly visit already-satisfied interest buildings.**
  ChoGGi fixed this class in the original game — check whether the interest-
  satisfaction check survived into Relaunched.
- **C06 — Colonist assigned to multiple workplaces simultaneously.**
  Tremualin's original-game fix is prior art; sweep the workplace-assignment
  transaction for a missing un-assign.
  **Witness upgrade 2026-08-01 (bug-list audit):** the fix is confirmed to
  exist in Tremualin's Library (workshop 2588520023, upd 2025-06-09, GitHub
  MIT): *"Fixed a bug where colonists would end up with multiple workplaces."*
- **C07 — Manual workplace assignment immediately discarded.** The
  auto-assignment pass may not respect a fresh `user_forced_workplace`; same
  family as the F61 forced-residence precedence work.
- **C08 — Rare-metal extractor smokes forever after refab.** Old ChoGGi note;
  dossier says still reported post-1.0.7. FX stop pass on refab.
- **C09 — Deterministic freeze near 90% breathable atmosphere (HIGH).**
  Reproduces at the same point across reloads — smells like an infinite loop
  in a game-time thread on a terraforming-threshold crossing (Open Domes /
  breathability transition, `OpenAirBuilding.lua` skin swaps, rainfall).
- **C10 — Last War mystery freezes at 54%, permanently blocking ALL imports
  (HIGH).** Same one-shot-Msg hang class as F06/Crystals: the mystery
  presumably disables resupply during a sequence and hangs before re-enabling.
  Sweep the Last War sequence files for import-lock set/clear pairing.
- **C11 — Game stops saving entirely, auto + manual (HIGH).** Classic symptom
  of a Lua error during savegame persistence (one unpersistable object aborts
  the save). Cross-check against the pack's corruption-leaving families (F03,
  F30, F45); needs a player log/save to pin.

### C12–C31 — gaps filed by the external-witness audit (2026-08-01, `docs/reports/BUG_LIST_AUDIT.md` §5)

Bugs that verified fix authors fixed and we do not track. **[VERIFIED]** = the
audit read the Relaunched Src lines itself; **[author]** = fix-author witness
only, our Src check still owed. None is a fix commitment — each needs the
FIX_POLICY §4 intent/reachability pass before any code is written. Author
quotes verbatim; sources in the audit report §8.

- **C12 [VERIFIED] — Support Struts ignore Easy Maintenance.**
  `Lua\Buildings\SupportStruts.lua:17-22`: `AccumulateMaintenancePoints`
  overrides straight to `SetMalfunction()` with no
  `IsGameRuleActive("EasyMaintenance")` branch (the rule's soften path exists
  for other buildings). ChoGGi (OG): *"Devs didn't check for EasyMaintenance
  when overriding AccumulateMaintenancePoints for picard"* — body verified
  byte-identical in Relaunched.
- **C13 [VERIFIED] — three FollowUp storybits mis-categorized.**
  `Data\StoryBit\FreeWill_2.lua:4,8` (`Category = "TechResearched"`,
  `Enabled = true`) and `SurveyOffer_TechEffect.lua:4,18` same;
  `Cure4Cancer_RareOutcome.lua:4` same category, **no `Enabled` line** (chain
  behavior needs one more check). ChoGGi (OG): *"The bit is in the
  TechResearched category instead of the FollowUp, so it never shows up."*
- **C14 [VERIFIED] — Fhtagn! Fhtagn! option 2 cowards every colonist.**
  `Data\StoryBit\FhtagnFhtagn.lua:66-82`: outcome text promises *"all
  Religious Colonists become Cowards"*; the `ForEachExecuteEffects` over
  `Colonist` has **no Filters**, while the sibling outcome at :45-65 filters
  correctly (`HasTrait Child, Negate`). Sibling-contradiction tell.
- **C15 [VERIFIED] — Dust Sickness: Deaths advertises a morale penalty it
  never applies.** `Data\StoryBit\DustSickness_Deaths.lua`: declares
  `morale_penalty`/`lower_morale_penalty`/duration params and both texts
  promise the loss; the file contains **zero** `StoryBitOutcome`/`ModifyObject`
  effects. Same Dust-in-the-Wind gate as F17/F40.
- **C16 [VERIFIED] — flying drones malfunctioning mid-air stay "flying".**
  `Lua\Units\FlyingDrone.lua:141-154`: `Malfunction`/`Freeze`/`NoBattery` are
  `assert(self:IsLanded())` + parent call (asserts strip in retail builds);
  `Dead()` at :156-159 lands first. ChoGGi (OG): *"Flying drones that
  malfunction mid-air are stuck 'flying'."* Sibling-contradiction tell.
- **C17 [VERIFIED] — The Man From Mars follow-up rewards nothing.**
  `Data\StoryBit\TheManFromMars_FollowUp4.lua`: replies carry "all
  Nerd/Hippie Colonists gain Morale" texts; the file has **zero**
  `StoryBitOutcome`/`ActivationEffects` — and remaster QA stamps (2024-11,
  2025-04) show it was touched without repair. ChoGGi (OG): *"None of the
  options reward anything."*
- **C18 [author→Src-pointed] — XenoExtraction skips the now-native ex-DLC
  extractors.** `Data\TechPreset.lua:2568-2598`: four `Effect_ModifyLabel`
  entries (Water/Metals/PreciousMetals/Regolith) — the description names
  exactly those four, so **no promise is broken**; ChoGGi extended it to
  Automatic/Micro-G extractors + RC Harvester/Driller in OG. **Intent
  question, not a defect claim** — §4-amendment bar: needs a positive intent
  statement (does `AutomaticMetalsExtractor` carry the `MetalsExtractor`
  label players would expect?) before anything is written.
  **✅ ANSWERED AND CLOSED 2026-08-02 (prompt 6b sweep) — `wontfix — intent`,
  under the owner's blanket pre-clearance for recording this close.** The
  checkable fact the entry asked for, settled from source:
  - **The label mechanism is exact-string, never inherited.** A building
    registers under `self.class`, `self.object_class` (only when it differs),
    `default_label`, `label1..label5` and its build-menu categories —
    `Building:SetCustomLabels` / `ApplyCustomLabels` (`Lua\Buildings\
    Building.lua:370-425`) and `Building:AddToCityLabels` (`:427-444`);
    the roster generator agrees (`GetCityLabelsForClass`, `:641-661`).
    - ⚠️ **CORRECTED 2026-08-02 (prompt 6c, C28 sweep). The sentence
      originally written here — "No parent class ever contributes a label" —
      is WRONG as a general rule, and it was being carried forward into other
      sweeps.** `AddToCityLabels` is a **combined method**:
      `DefineCombinedMethod("AddToCityLabels", "call")`
      (`Lua\CityObject.lua:8`; machinery
      `CommonLua\Core\classes.lua:1499-1511`) makes the flattened method call
      **every** parent implementation, not just `Building`'s. Parents really do
      contribute labels — `BuildingDepositExploiterComponent` → `ResourceExploiter`
      (`Lua\Buildings\BuildingComponents.lua:49-51`), `ResourceProducer` →
      `ResourceProducer` (`:529-531`), `DroneControl` → `DroneControl`
      (`Lua\Buildings\DroneControl.lua:273-275`), `ColdSensitive` → `Frozen`
      (`ColdSensitive.lua:42-46`), `Community`, `BaseFarm`, `DustGenerator`,
      and for units `BaseRover` → `Unit`/`Rover`/`self.class`
      (`Lua\Buildings\BaseRover.lua:134-138`).
    - **C18's VERDICT IS UNAFFECTED, and this is why**: every parent-contributed
      label in the tree is a **role/component** name (`ResourceExploiter`,
      `ResourceProducer`, `Frozen`, `Rover`…), never a **building-type** name.
      XenoExtraction names four building-type labels — `WaterExtractor`,
      `MetalsExtractor`, `PreciousMetalsExtractor`, `RegolithExtractor`
      (`Data\TechPreset.lua:2578-2597`) — and no parent class anywhere emits any
      of those. So `AutomaticMetalsExtractor` still does not carry
      `MetalsExtractor`, and the close stands.
    - **The rule, restated correctly for future sweeps:** a building's label set
      is `self.class` + `self.object_class` (when it differs) + `default_label`
      + `label1..label5` + build-menu categories, **plus one label per parent
      class that defines its own `AddToCityLabels`**. Type-name labels come only
      from the first group; role labels come from the second. Matching on an
      exact string is still the rule — there is no inheritance *of a name*.
  - **So the answer is NO, and the reason is not a bug.**
    `AutomaticMetalsExtractor` has `object_class =
    "AutomaticMetalsExtractorBase"` (`Lua\BuildingTemplate\
    AutomaticMetalsExtractor.generated.lua:9`), where `MetalsExtractor` has
    `object_class = "MetalsExtractorBase"` (`MetalsExtractor.generated.lua:9`)
    — **disjoint label sets, by construction**, and the building is displayed
    as *"Automatic Metals Extractor"* (`:52`), a different building name from
    the *"Metals Extractor"* the tech's description names.
  - **The positive intent statement the §4 bar wanted exists, and it points
    the same way.** When this game means *every* extractor it **enumerates
    every extractor**: the Astrogeologist commander profile spends **ten**
    `Effect_ModifyLabel` entries (`Data\CommanderProfilePreset.lua:336-385`)
    where XenoExtraction spends four. Four labels for a four-name description
    is a deliberate match, not an oversight.
  **Verdict: no promise is broken; declined.** ChoGGi's OG extension was a
  buff, not a repair. ⭐ **The sweep did turn up a real defect on the way —
  but in the *other* preset: see `C38`** (the ten-label enumeration is missing
  two extractors while promising all of them). That is where this candidate's
  value actually was.
- **C19 [author→Src-pointed] — `AreDomesConnectedWithPassage` has no distance
  term.** `Lua\Passage.lua:1109-1119` is pure network membership; ChoGGi's OG
  fix added a `ColonistMaxDomeWalkDist` check. F52 fixed the ≤400m vacuum
  walk; whether the *long-walk-through-network* class survives in Relaunched
  is unswept. Interacts with F52/F53 — audit before touching.
  **✅ SWEPT AND CLOSED 2026-08-02 (prompt 6b) — DECLINED: the charge against
  the predicate is true and irrelevant, because Relaunched put the distance
  term at the consumer.** Trail:
  - **The predicate is membership-only, verbatim as charged**
    (`Lua\Passage.lua:1109-1119`), and its network cache is correctly
    invalidated on both connect and disconnect (`:1358-1362`, `:1244`) — no
    stale-network defect hiding behind it.
  - **It has exactly TWO consumers in the whole tree** (grep, `ModTools\Src`):
    `GetDomesPassagePath` (`Passage.lua:1143-1146`, a guard before
    path-building — policy is the caller's) and `IsInWalkingDistDome`
    (`Lua\Buildings\Dome.lua:244-262`). **Neither is distance-blind.**
  - **The distance term, in full** (`Dome.lua:256-259`):
    `dist[1] or AreDomesConnectedWithPassage(bld1,bld2) and
    (GetOpenAirBuildings(map) or not IsLRTransportAvailable(map.City) or
    dist[2] <= const.ColonistMinDistToIgnorePassage)`. That constant is
    **1200m** (`_GameConst.lua:134`) and it carries the design intent in a
    comment on the line: *"distance between two domes to provoke colos to
    request a shuttle, even if connected with passage."* **This is precisely
    what ChoGGi added to OG's predicate** — Relaunched has it, one call up,
    at 3× the walk cap. (720m under `Station.lua:1311-1312` / the
    `GameRuleDef.lua:201-202` rule.)
  - **A second, independent cap sits below it:**
    `Colonist:TryToEmigrateToDome` refuses a passage route of more than
    `const.ColonistMaxPassagePassthroughDomes` = 8 domes
    (`Colonist.lua:1567`, `_GameConst.lua:135`).
  - **Both escape branches are correct, not oversights.**
    `GetOpenAirBuildings(map)` is `map == MainMap and OpenAirBuildings`
    (`OpenAirBuilding.lua:167-169`), and that GameVar goes true **only** after
    the atmosphere is breathable and the player accepts *"Open the Domes"*
    (`LawDef-Research.lua:651-653`, `PopupNotificationPreset-GreenMars.lua:
    15-17`), and is forced false the moment breathability lapses
    (`Terraforming.lua:349`, beside the suffocation effects) — i.e. the
    unlimited walk is allowed exactly when walking outside is safe.
    `not IsLRTransportAvailable(city)` (`ShuttleHub.lua:350-358`) means there
    is no shuttle to hold out for — **the same reasoning our own F52 entry
    records for the half it deliberately left open.**
  **What survives, and it is not new.** The unbounded walk that remains is the
  **no-passage** case: vacuum, no shuttle coverage, domes not in one network →
  `GetDomesPassagePath` returns nil and vanilla walks the colonist across the
  surface. That is F52's second half, declined by us in writing ("refusing it
  would strand colonists on shuttle-less maps"). ⭐ **And it is what §10.5's
  commenters describe ChoGGi actually shipping** — a survivability mitigation
  *"so at least they didn't suffocate in case they still walked stupid
  walks"*, i.e. even the index-case author treated the walk as unfixable and
  softened the consequence. Prior art and our own disposition agree.
  **⚠️ The F53 interaction is a reason NOT to take the OG fix's shape.**
  `IsInWalkingDistDome` is the reachability test our `Fix_ArrivalDeaths`
  re-check consults. Capping `AreDomesConnectedWithPassage` at 400m would make
  every passage-connected dome pair beyond 400m read as *not reachable* — so
  arrivals bound for a dome that is perfectly reachable through the passage
  network would be re-checked, held under "Confused Colonists", or diverted.
  **A fix here would have degraded a shipped, tested fix.** Verdict: no F-row;
  no promotion to prompt 7.
- **C20 [author] — Philosopher's Stone sector-scan count stalls while
  paused.** ChoGGi (OG): *"The Philosopher's Stone doesn't update sector
  scanned count when paused."* The `registers._sectors_scanned` machinery is
  intact in Relaunched `Mystery 10.generated.lua`; pause behavior needs a
  live check. Distinct from F06 (the CrystalFlyAway one-shot hang).
  **⭐ MECHANISM LOCATED 2026-08-02 (prompt 6b) — the pause-stall is REAL in
  current Src, but what it costs the player is NOT settled and must not be
  written up as if it were.** Trail (Mystery 10 = Philosopher's Stone,
  `Data\Scenario\Mystery 10.lua:4-5`):
  - **The counter is purely event-driven.** `Sector Scanned Counter` is
    `while true do WaitMsg("SectorScanned"); _sectors_scanned =
    _sectors_scanned + 1 end` (`Lua\Scenario\Mystery 10.generated.lua:
    299-303`). Nothing recomputes the count from map state — **a missed
    message is a permanently missed count.**
  - **The only emitter of that message in the tree is a GAME-TIME thread that
    begins by sleeping.** `AddSectorScannedNotification` (`Lua\Exploration.lua:
    88-104`) opens with `Sleep(10)  -- allow newly placed deposits to GameInit
    properly` and ends with `AddHUDNotification("SectorScanned", …)` (`:103`)
    then `Msg("SectorScanned", …)` (`:104`); it is spawned as
    `self:CreateGameTimeThread(AddSectorScannedNotification, …)` by
    `MapSector:Scan` (`:276-280`). **Game time does not advance while the game
    is paused, so that thread cannot reach line 104.**
  - **And a scan CAN happen while paused.** `OverviewModeDialog:DeployProbe`
    (`Lua\UI\OverviewModeDialog.lua:468-482`) → `OrbitalProbe:ScanSector`
    (`Lua\OrbitalProbe.lua:88-100`) → `MapSector:Scan` for every sector in the
    probe pattern. **There is no pause check anywhere on that path** — the
    scan lands, the deposits reveal, and the counter does not move. That is
    ChoGGi's sentence, with a file:line.
  - **The stake:** the mystery's Trigger sequence blocks on `while not
    (_sectors_scanned > 4)` (`:63,:71-73`) and a later branch tests `> 15`
    (`:347`), so undercounting **delays the mystery's start silently**.
  **⚠️ What source CANNOT settle — and it is the whole severity question.**
  Whether the pending increment is merely **DEFERRED to unpause** (harmless;
  the thread wakes when time resumes) or **LOST**. Two source-visible routes
  to loss, neither confirmable without a run: (a) **save/reload while
  paused** — a suspended game-time thread does not survive a load, while
  `_sectors_scanned` does (it is a persisted scenario register, `:12-24`);
  (b) **re-scan of the same sector** — `MapSector:Scan` calls
  `DeleteThread(self.notify_thread)` (`:277`) before spawning the new one, so
  a pending notification for that sector is discarded outright. There is also
  an unresolved **multi-sector** question: one probe scans a whole pattern at
  once (`ScanSector` :96-100), every sector's thread wakes at the same game
  time, and a single `WaitMsg` loop may or may not be re-armed in time to see
  all of them. **Engine wake-up semantics are not readable from Lua source —
  CANNOT DETERMINE, deliberately.**
  ⭐ **The observation this needs is free, because the HUD notification is a
  perfect proxy.** `AddHUDNotification` (`:103`) is the line immediately before
  the `Msg` (`:104`), in the same thread with no yield between them — so **it
  fires if and only if the mystery counter ticks.** No console, no active
  Philosopher's Stone run, no TestKit needed.
  ⚠️ **CORRECTION 2026-08-02 (found mid-observation, by the reading itself):
  6b called this "the on-screen toast" and that wording is WRONG — it sent the
  observer looking for a popup card that does not exist.** `SectorScanned` is a
  **`HUDNotificationPreset`**, not a `NotificationPreset`
  (`Data\HUDNotificationPreset.lua:55-61`): `button_id = "idOverview"`, so it
  attaches to the **Overview button** and plays a **voice line** ("Sector
  scanned"), and there is **no popup card at all**. The voice is emitted inside
  `AddHUDNotification` itself (`QueueVoice`, `Lua\X\HUDNotifications.lua:33-36`),
  so it is just as tight a proxy — but you listen for it, or read
  `IsHUDNotificationShown("SectorScanned")` (`:111-118`), rather than watch for
  a card.

  **✅ OBSERVATION TAKEN 2026-08-02 (owner, live, 98-sol save, mystery not even
  active — the proxy needs no mystery). VERDICT: DEFERRED, NOT LOST. C20 IS
  CLOSED, `wontfix — no player-visible cost`.**
  - **Paused:** probe deployed onto an unexplored sector, scan landed. **No
    "Sector scanned" signal of any kind.**
  - **On unpause:** the **"Sector scanned" voice-over fired.** Since `QueueVoice`
    is inside `AddHUDNotification` at `:103`, immediately before the `Msg` at
    `:104` with no yield, **the message provably fired on unpause.** The
    increment is deferred by exactly the pause, then delivered.
  - **The stall in the pause window is REAL and stays confirmed** — the source
    trail above is unaffected. What is now settled is the half source could not
    reach: **it costs the player nothing**, because game time resuming is
    precisely what the sleeping thread was waiting for.
  - ⭐ **INTERNAL CONTROL, confirmed on timing by the observer** — this is the
    strongest part of the reading and it was free. The same scan raised **two**
    notifications and they split **exactly** on the pause boundary:
    **`NewAnomalies` appeared BEFORE the unpause** (a plain `NotificationPreset`
    raised synchronously on the reveal, `Lua\Buildings\Anomaly.lua:444`), while
    **`SectorScanned` fired the instant the game was unpaused and not before**
    (behind the `Sleep(10)` game-time thread, `Exploration.lua:88-104`).
    **What that additionally proves, and why it matters more than the voice
    alone:** the scan itself **executed under pause** — `MapSector:Scan` ran and
    the anomaly revealed — while the `Msg` did not fire. That is the source
    trail's claim *"the scan lands, the deposits reveal, and the counter does
    not move"* observed directly, and it rules out the rival reading that
    nothing happened while paused at all (e.g. the probe silently refusing to
    deploy). 6b's located mechanism demonstrated rather than argued.
  - ⛔ **NOT settled by this reading, and deliberately left open:** routes (a)
    save/reload while paused and (b) re-scan of the same sector
    (`DeleteThread(self.notify_thread)`, `:277`), plus the multi-sector
    re-arm question. **None of them is reachable in ordinary play the way the
    pause case is**, and the pause case — the actual charge in ChoGGi's
    sentence — is answered. If anyone wants (a) later, use
    `IsHUDNotificationShown("SectorScanned")` and **not** the voice:
    `QueueVoice` is rate-limited by `const.NotificationVoiceCooldown` = **120
    real seconds** per id (`HUDNotifications.lua:33-36`), so a repeat inside two
    minutes can be silent and read as a false "lost".
- **C21 [author] — St. Elmo sinkholes destructible by meteors → mystery
  soft-lock.** ChoGGi (OG): *"Stop meteoroids from destroying sinkholes and
  soft locking the mystery."* Relaunched `Fireflies.lua:116` sets no
  `indestructible`; whether the meteor damage path can still hit them is
  unchecked. Distinct from F07/F15 (wisp math).
  **⭐ SWEPT 2026-08-02 (prompt 6b): the meteor path CAN still hit them —
  verified end to end — and the soft-lock has a located candidate that is not
  the one anybody would have guessed. → routed to prompt 7 for the §4 call.**
  **1. The sinkhole has neither protection the engine offers.** The `Sinkhole`
  template (`Lua\BuildingTemplate\Sinkhole.generated.lua:1-24`) sets
  `can_demolish = false`, `use_demolished_state = false`, `count_as_building =
  false` — and **no `indestructible`** and **no `disasters_strike_immunity`**;
  both default false (`Building.lua:209`, `:282`). `can_demolish` only gates
  the *player's* demolish button (`Building.lua:888`); no disaster path reads
  it.
  **2. The full destruction chain, read this session.** `BaseMeteor:GetQuery`
  fetches `"Building"` among its classes (`Lua\Meteors.lua:405-409`); the
  filter rejects only in-dome objects, `disasters_strike_immunity` buildings,
  parented objects and `TrackBase` (`:393-399`) — a sinkhole passes all four.
  The **large**-meteor loop's building branch excludes only `Dome` and
  `ConstructionSite` (`:817-825`) and calls `DestroyBuildingImmediate`, whose
  **only** protection is `bld.indestructible` (`Building.lua:1371-1374`) →
  `DoDemolish` → `use_demolished_state` false → **`DoneObject(self)`**
  (`Demolishable.lua:132-141`). The object is deleted outright, so it also
  leaves `MainCity.labels.Sinkhole`. The **small**-meteor loop reaches the
  same object and calls `obj:SetMalfunction()` (`Meteors.lua:688-693`).
  **3. ⭐ The sibling-contradiction tell is unusually clean: every other
  mystery set-piece in the game is flagged, and only this one is not.**
  `indestructible = true` on `CrystalsBig`/`CrystalsSmall` (Philosopher's
  Stone), `BlackCubeMonolith`, `MirrorSphereBuilding`, `CaveOfWonders`,
  `JumboCave`, `JumboCaveReinforcementStructure`, `AncientArtifact`, `ArkPod`,
  `MartianAssembly`(`Fake`), `BottomlessPit` — grep of
  `Lua\BuildingTemplate\`. The property's own help text names meteors
  explicitly: *"Specify if the building can be destroyed at all (by
  demolishing, by explosions, by meteors, etc)"* (`Building.lua:209`).
  **4. The soft-lock: TWO routes located, neither proven — and the obvious
  one is the weaker.**
  - **(a) The unguarded object register, `Mystery 11.generated.lua:146`** —
    `PlaceResourceStockpile_Delayed(_sinkholePos, _sinkhole:GetMap(),
    "Polymers", polymers_reward, 0, true)`. `_sinkhole` is a **persisted
    scenario register** (`:14,:23,:32`) holding the spawned sinkhole, and the
    call has **no `IsValid` guard**. It runs after the player scans the first
    anomaly (`:122-126`), so the entire scan window is exposure. If a meteor
    deleted that sinkhole in the meantime this indexes a dead object — and the
    line sits on the **Trigger sequence, the mystery's spine**. ⚠️ The same
    line carries a vanilla-only hazard too: the placement cascade at
    `:632-675` can leave `_sinkhole` **`false`** after four failed attempts,
    and `false:GetMap()` is an unconditional Lua error.
  - **(b) The label-count gate, `:214`** — `while not
    (#MainCity.labels.Sinkhole > 2) do Sleep(...) end`, and destruction does
    reduce that count. **But this one largely self-heals**, and the reason is
    on the page: `Sinkhole Spawner: Repeater` re-runs the spawner every 1-2
    sols and **only breaks when `#MainCity.labels.Sinkhole > 9`**
    (`:689-704`), so while meteors eat sinkholes the spawner keeps replacing
    them. A stall, not a lock — unless the repeater has already exited.
  **5. ⭐ What is NOT at risk — checked, because it was the obvious guess and
  it is wrong.** The anomalies survive. `SubsurfaceAnomaly` is not a
  `Building` at all (`Lua\Buildings\Anomaly.lua:173-174`) and matches none of
  the classes `BaseMeteor:GetQuery` asks for (`Meteors.lua:408`), so the
  *"Wait Sinkhole N Scanned"* stages cannot be broken by a meteor removing
  their anomaly. **The soft-lock cannot come from there.**
  **Verdict: destruction route VERIFIED; harm LOCATED but UNPROVEN** — nobody
  has watched a meteor land on a sinkhole, and ChoGGi's OG sentence is the
  only witness. Route (a) is the one worth deciding on and it is cheap to make
  safe. **Promoted to prompt 7 as a package.**
- **C22 [VERIFIED 2026-08-01, source recovered] — the Saint trait's dome
  morale blessing has never worked: label-name mismatch.**
  `TraitPreset:AddDomeColonistsModifier`
  (`ClassDef-PresetDefs.generated.lua:1783-1789`) uses the raw trait string
  `"Religious"` as the dome label, but colonists are filed under
  `GetTraitLabel(trait_id)` = `"Trait" .. trait_id` → `"TraitReligious"`
  (`Traits.lua:1300-1302`; `"Religious"` is not in `fixed_labels`
  :1268-1298; filing site `Colonist.lua:373`). The +10 base_morale lands on
  an empty label — Saint's *"Raises the Morale of all Religious people in
  the Dome"* (`TraitPreset.lua:383-397`) has never applied to anyone.
  Airtight from Src; fredware's fix substitutes `GetTraitLabel("Religious")`
  and re-bases live Saints. *(fredware "Bug Fixes" was removed from the
  Workshop ~a day after upload, reason unstated — but the owner's
  subscription delivered the FPK and the full 22-file source was extracted
  and read 2026-08-01; these entries now cite held source, not a dead page.
  **All six mod FPKs — fredware's included, otherwise unrecoverable — are
  archived at `C:\Dev\workshop_fpk_archive\` (local, not in git; extract with
  `tools/flpk_extract.py`), so the workshop subscriptions are no longer
  needed.**)*
- **C23 [VERIFIED 2026-08-01] — dust devils: three scheduler defects in
  `DustDevils.lua`.** (1) The natural scheduler misuses `spawn_chance` as a
  count multiplier — `:216 Random(count_min,count_max) * spawn_chance / 100`
  (integer-truncating toward zero) — while the marker path uses it correctly
  as a probability (`:169 Random(100) < marker_spawn_chance`); sibling
  contradiction on the page. (2) `GetDustDevilsDescr` reads
  `CurrentMap.mapdata` (`:59,:64`) but the scheduler spawns on `MainMap`
  (`:198`) and re-reads every cycle (`:234-238`) — viewing the underground/
  asteroid while it re-reads picks up the wrong map's descriptor
  (`"disabled"` → nil → loop wedges in the day-long retry). (3) The marker
  spawn check `:169` has no `DustStormsDisabled` term while the main
  scheduler gates on it twice (`:209,:220`) — after terraforming permanently
  sets it (`TerraformingDisasters.lua:16`), feature-marker dust devils keep
  spawning forever (the player-facing symptom fredware's description names).
- **C24 [VERIFIED 2026-08-01] — operator-precedence bug makes ordinary
  rockets count as asteroid landers.** `PlanetaryView.lua:439`:
  `IsKindOf(rocket,"LanderRocketBase") and command=="Refuel" or
  command=="WaitLaunchOrder" or (command=="LoadAndLaunch" and not
  target_spot)` — precedence detaches the last two clauses from the
  `IsKindOf`, so any pad-idle supply rocket satisfies the asteroid-visit
  predicate and the consumer (`PlanetaryViewAsteroidResources.generated.lua:
  37-41`) opens an EMPTY lander-selection screen. Verified on the line
  2026-08-01. **Complementary to F72, not covered by it** — our
  `Fix_AsteroidLanderAvailable` wrapper fixes the false NEGATIVE and passes
  vanilla's `true` straight through, so this false POSITIVE survives our
  pack.
- **C25 [mechanism verified, trigger unproven] — Jumbo Cave reinforcements
  wedge on unreachable Waste Rock.** The wedge chain is real in Src: a
  failed `WasteRockObstructor:DroneApproach` (`WasteRock.lua:318-327`) files
  the rock in `unreachable_buildings` (`Drone.lua:818-826`), stalling the
  clear request the `JumboCaveReinforcementStructure` site blocks on
  (`BuriedWonder_Jumbo_Cave.generated.lua:103`). What Src alone cannot prove
  is that cave geometry actually produces an unreachable rock — fredware's
  fix fires only after observing a live approach failure, which is honest
  about the same limit. Old RESEARCH lead ("stuck at 'construction site is
  being cleared'") + his independent fix = witnessed; needs an in-game repro
  before an F-row.
  **⭐ SWEPT 2026-08-02 (prompt 6b) — the patch-note question is ANSWERED from
  source (better than notes), and the minimal check is written.**
  **1. Yes, a patch touched Jumbo Cave in the 1.0.4-1.0.7 window — 1.0.6
  replaced the ENTIRE scenario — and no, it did not touch this.** The tree
  ships **two** Jumbo Cave scenarios: `Lua\Scenario\
  BuriedWonder_Jumbo_Cave.generated.lua` and `…_106.generated.lua`. The
  selector is `FixSequenceList` (`Lua\Buildings\Anomaly.lua:26-33`): *"if
  `self.sequence_list == "BuriedWonder_Jumbo_Cave"` and `UndergroundRework106`
  then `self.sequence_list = "BuriedWonder_Jumbo_Cave_106"`"*. The template
  itself still names the old list (`Data\BuildingTemplate\JumboCave.lua:24`);
  the remap is what makes the new one live.
  **⚠️ And the gate is SAVE VINTAGE, not build.** `GameVar("UndergroundRework106",
  false)` with the shipped comment one line above it: *"UndergroundRework106 is
  false in old savegames, true in ones started at or after 1.0.6"*
  (`Lua\Buildings\UndergroundDome.lua:16-17`), set true only in
  `OnMsg.NewGame` (`:19`). **A save begun before 1.0.6 runs the OLD script on
  our pinned 1.0.7.396349** — a live external-validity constraint for any
  Jumbo Cave observation, and it generalises: the underground rework is gated
  the same way throughout (`Elevator.lua:830,:839`,
  `UndergroundDome.lua:41,:53`).
  **The wedge itself is untouched by the rework.** Both versions block on the
  same label with the same shape — old `:103` and new `:104` are the identical
  statement `while not (UndergroundMap.City.labels["JumboCaveReinforcementStructure"])
  do Sleep(3000 + …) end`. **1.0.6 rewrote the story around this and left the
  mechanism exactly where it was.** No fix to inherit, and no "fixed in
  Relaunched" close available.
  **2. The minimal in-game check (rider written to `PLAYTEST_CHECKLIST.md`).**
  What needs proving is only the TRIGGER — that cave geometry actually strands
  a rock. The read is one console line, taken **while the site is stuck**,
  **on the underground map** (`UICity` follows the map you are looking at,
  `Lua\_init.lua:12-14`): walk the underground drones' per-drone
  `unreachable_buildings` tables (`Lua\Units\Drone.lua:817-835` — weak-keyed,
  `[building] = timestamp`, capped at `const.MaxUnreachablesInTable` = 64) and
  count `WasteRockObstructor` entries (class confirmed,
  `Lua\WasteRock.lua:33-41`; `DroneApproach` at `:318-326` is the failing call
  the wrapper catches). ⚠️ Guard with `IsValid(b)` before `IsKindOf` — the
  table also carries a plain `version` key (`Drone.lua:826`). The rocks
  additionally carry `parent_construction` (`WasteRock.lua:40`), so a stranded
  rock can be tied to the blocked site rather than merely counted.
- **C33 [VERIFIED 2026-08-01 — and OUR OWN F44 PATH REPRODUCES IT] —
  whole-track demolition leaks an invisible, undeletable TrackBase shell.**
  `TrackGridElement:DemolishAndSplitTrack` calls `track_obj:OnDemolish()`
  directly at three sites (`TrackElement.lua:468,:506,:520`), bypassing the
  `Demolishable` flow that is the only place `OnDemolish` is followed by
  `DoneObject` (`Demolishable.lua:132-140`). `TrackBase:OnDemolish` sets
  `CanDelete = ret_false` + `demolishing = true` (`Track.lua:248-250`, read
  this session) and empties `elements`/`assigned_vehicles` to `false`
  (`:190-191`,`:165`); the element-side auto-delete requires
  `track_obj:CanDelete()` (`TrackElement.lua:203-205`) — now permanently
  false — so the invisible shell (`entity = "InvisibleObject"`, `Track.lua:35`)
  persists in the map and every save. A naive `DoneObject` on it RAISES
  (`Done` ripairs over the `false` fields, `Track.lua:69-76,:176-192`).
  **Our `Fix_TrackSalvageWipe` (F44) keeps the `track_obj:OnDemolish()` call
  on the mass-delete path, so our pack produces the same shells on
  Ctrl+click mass salvage.** The shell also pins `demolishing = true` — the
  field F47's half-B stands down on. fredware's repair: post-wrap
  `DemolishAndSplitTrack`, detect the exact four-field shell signature,
  install empty tables, `DoneObject`; plus a save sweep deleting existing
  shells. Needs its own F-row decision + a look at whether F44 should stop
  producing shells.
  **🔎 POSSIBLE LIVE PLAYER SYMPTOM, 2026-08-01 — a LEAD, not a verdict, and it
  must not be packaged as evidence until its provenance is nailed down.** During
  the owner's logged-in Paradox browse, a bug report surfaced whose shape fits
  this mechanism unusually well:
  > **Summary:** "Cannot add trains to tracks" — *"I redid my entire train
  > network with large train stations, and now I cannot assign trains to either
  > track. I get the green tooltip that says 'assign train to track', but when I
  > click nothing happens. I check the track and it says 0/10 trains. I have 7
  > trains in my inventory, but still can't assign any to the tracks."*

  **Why it is interesting here rather than under F64.** The reporter **has**
  trains (7 in inventory) — so this is *not* the F64 counter-at-zero symptom,
  which is the opposite failure. What they did first was **redo an entire track
  network**, i.e. mass track demolition — the exact path
  `DemolishAndSplitTrack` sits on — and what is broken afterwards is the
  **track's** ability to accept an assignment (`0/10` with a live tooltip that
  does nothing). A persistent `TrackBase` shell with `elements` /
  `assigned_vehicles` emptied to `false` and `CanDelete = ret_false` is a
  candidate explanation for a track that reports zero capacity-in-use and
  silently refuses assignment.
  **✅ PROVENANCE ESTABLISHED (owner, same browse): it IS a Paradox forum
  report.** The reporter's **in-game bug submitter failed with a 500** (that is
  the *"Sending bug report failed"* box in the image), so they screenshotted
  their own filled-in report form and posted the picture to the forum instead.
  So it reached Paradox, by hand. **Still missing: author, date and build** —
  the screenshot carries none, and those are what decide whether it is a
  Relaunched-era report at all. Get them before this is cited anywhere.
  📌 **Method fact worth more than this lead, recorded here because this is
  where it surfaced: at least one player found the in-game bug reporter
  returning HTTP 500 and had to route around it manually.** If that is not
  isolated, then *reported* volume systematically **undercounts** real
  incidence — some players will simply have given up at the error box. That
  weakens "no report found" as evidence one more notch, on top of the
  crawler-block lesson in `BUG_LIST_AUDIT.md` §10.4. One instance; not
  established as systemic.
  **⚠️ Two reasons this is still only a lead.** (1) **The chain is unverified** — nobody has traced
  the assignment path (`AssignTrain` / the track's vehicle slots) against a shell
  to confirm a shell actually produces this symptom. (2) **Alternatives are
  live** — F80's enumeration suspicion and ordinary route/track-state defects
  could produce the same surface.
  **⛔ WEAKENED HOURS AFTER FILING, 2026-08-01 — a competing explanation
  exists and it is already fixed.** The Reddit thread the owner exported the
  same evening ([S36], `BUG_LIST_AUDIT.md` §10.5) contains this, from
  Changlini, the thread's top comment:
  > *"Hotfix 2 allegedly fixed trains, in the sense that **you can place trains
  > on the train tracks again, which Hotfix 1 broke**."*

  **So "cannot place trains on tracks" was a known hotfix-1 REGRESSION, fixed in
  hotfix 2 — long before our pinned 1.0.7.396349.** If the screenshotted report
  dates from the 1.0.1/1.0.2 window, it is that regression and has nothing to do
  with track shells. **This is precisely why the lead was hedged on its missing
  date, and the date is now the whole question.** Do not cite it for C33 until
  someone reads the thread's date off the forum: **1.0.1/1.0.2 → discard;
  1.0.3 or later → the hotfix-2 explanation is spent and the lead is live
  again.**
  **What would settle the mechanism half, independently of the date:** trace
  what `assign train to track` checks and whether a shell-state `TrackBase`
  fails it silently. That is a cheap source question and it belongs to whoever
  packages C33 — but on current evidence **assume the lead is spent** rather
  than assume it is real.
  *(Same thread, same caveat, different item: Darganiss reports **"one of my two
  stations refuses to connect"** on 1.0.3 after previously having "zero problems
  on 1.0.0" — a station/track connection failure that is NOT the assignment
  symptom. Noted, not filed; it has no mechanism and no current-build evidence.)*
- **C34 [author, source held] — stale-ACTIVE rain state: `g_RainDisaster`
  set with a dead `main_thread` reads as disaster-active forever; nothing in
  our pack repairs it.** fredware's rains module heals it via vanilla's own
  `FinishRainProcedure(rain_type)` (`TerraformingDisasters.lua:247-274` —
  clears fields, label modifiers, notifications, sets `g_RainDisaster =
  false`, sends `Msg("RainDisasterEnd")`), with a manual fallback; he also
  recreates a missing `RainsDisasterThreads` GameVar table, clears dead
  `soil_thread`s and invalid `g_RainDisaster` values. Our F81b fixes the
  deadlock that *strands* the loop; this is the sibling class of stale state
  we do not touch. Candidate for the sanitizer/F81 family.
  **→ ADOPTED AND BUILT 2026-08-01 (F86 Tier-1, spec §6.2a-B3): rides
  `Fix_RainsDeadlock`'s PostLoadGame migration pass as a rider, no module of
  its own. Structure repairs (missing/non-table registry recreated, dead
  `soil_thread`s → false) → stale-ACTIVE heal through vanilla's own
  `FinishRainProcedure` → loop migration; invalid `g_RainDisaster` values
  that match no known rain type take the manual fallback (`= false` +
  `Msg("RainDisasterEnd")`, logged) because FinishRainProcedure's
  notif_prefix lookup would concatenate nil on them. Verification rides
  Tier-1 leg 3 (plant `g_RainDisaster` with a dead `main_thread` → heals
  through FinishRainProcedure).**
  **Id-less migration clause resolved 2026-08-01 (mid-sitting, owner
  cleared): `test 2i`'s `toxic id=nil` entry is vanilla's own empty fill-in
  (`UpdateRainsThreads` creates `{}` entries for inactive rain types,
  `TerraformingDisasters.lua:453-457`; live dump: `alive=false`) — nothing
  to migrate, correctly silent. A LIVE id-less thread is effectively
  unreachable (vanilla always stamps `id`; our old pass never removed one);
  the spec's unique-type resolution is dead code against the real preset
  group (classdef defaults `type="toxic"`, `:128` → 3 toxic + 3 normal,
  never unique), so a hypothetical live id-less entry takes the loud
  leave-and-log path — bounded by vanilla's next `UpdateRainsThreads`, which
  DeleteThreads every not-kept activation thread (id=nil can never be kept)
  and recreates the loop on its own body. Leg 3's PASS reading amended
  accordingly (build prompt carries the note).**
- **C26 [author] — malfunctioned buildings stuck in perpetual maintenance.**
  SkiRich (OG, workshop 2433157820, 4,100 subs): *"buildings that are
  malfunctioned and stuck in perpetual maintenance mode and nobody is willing
  to fix them. Most people think its a drone issue. It is not, it is a repair
  cycle issue with the building."*
  **→ SWEPT 2026-08-02 (prompt 6c). Verdict: CANNOT DETERMINE — the state is
  real and the engine heals it, but no producer exists in current Src that I
  could reach.**
  - **The engine ships two savegame heals named for exactly this symptom.**
    `SavegameFixups.FixMaintenanceRequestsSources`
    (`Lua\RequiresMaintenance.lua:531-566`) re-`SetSource`es orphaned
    maintenance requests **and re-inserts requests that fell out of
    `task_requests`** (`:540-548`) — a request missing from `task_requests` is
    never offered to a command centre, so **no drone can ever be assigned and
    the building stays malfunctioned forever**, which is SkiRich's sentence
    almost verbatim ("not a drone issue… a repair cycle issue with the
    building"). `SavegameFixups.FixMissingMaintenance` (`:568-574`) re-inits
    buildings that `DoesRequireMaintenance()` but hold **no work request at
    all**. Haemimont saw both states.
  - ⚠️ **Those heals are OLD-SAVE-ONLY, and this is the load-bearing fact.**
    `AppliedSavegameFixups` is a `GameVar` whose initializer marks **every
    fixup that exists at new-game time as already applied**
    (`CommonLua\SavegameFixup.lua:10-16`); `FixupSavegame` then runs only the
    unmarked ones (`:34-41`). A save **started** on our pinned build therefore
    never runs either fixup. Same shape as C25's vintage gate: presence in Src
    is not reachability in this save. **So these are heals for a producer, not
    a repair of one** — the C32 lesson ("his fix does something" ≠ the thing it
    does was needed) does not apply here, because the fixups are the *vendor's*
    and they name the state; but neither do they prove the producer survives.
  - **Obvious guess 1 — rubble-shroud stranding — CHECKED AND RULED OUT.**
    `IsMaintenancePrevented()` is exactly `IsShroudedInRubble()` (`:151-153`),
    and `TryRequestMaintenance` (`:155-162`) **sets
    `last_maintenance_points_full_ts` but skips `RequestMaintenance()` while
    prevented**, after which `BuildingUpdate` malfunctions the building a sol
    later (`:120-126`) and then early-returns forever on `IsMalfunctioned()`
    (`:112-114`) — a perfect stranding shape. It does not strand: `RubbleBase:OnClear`
    re-fires `TryRequestMaintenance()` on **every** shrouded object before
    deleting itself (`Lua\Buildings\RubbleBase.lua:140-149`), and rubble has no
    non-`OnClear` destruction route (`CanGetDamagedBy` → false `:50-52`,
    `CanDemolish` → false `:46-48`), so no dangling `shrouding_rubble`
    back-pointer can accumulate (`Lua\Shroudable.lua:8-18`).
  - **Obvious guess 2 — zero maintenance threshold — CHECKED AND RULED OUT.**
    `RequestMaintenance()` silently does nothing when
    `accumulated_maintenance_points == 0` (`:343-357`), and
    `AccumulateMaintenancePoints` clamps to `maintenance_threshold_current`
    (`:167`), so a zero threshold would make `SetMalfunction()` produce a
    malfunctioned building with **no request at all**. Unreachable in data: all
    18 templates that set `maintenance_threshold_base` sit at 50000-200000 (min
    `DefenceTower`/`RechargeStation`/`SensorTower`/`TriboelectricScrubber`
    50000), and although the prop **is** modifiable in the negative direction —
    the BadMOXIE storybits apply `Percent = -25`
    (`Data\StoryBit\BadMOXIE.lua:60-66`, `BadMOXIE_ColdWave.lua:100-109`) — the
    two stack to -50% at worst and are MOXIE-only, while every other modifier is
    positive (`Data\TechPreset.lua:2277-2283` SustainableArchitecture +20,
    `:2405-2411` ResilientArchitecture +20; `Data\CommanderProfilePreset.lua:140-150`
    citymayor +20/+20). The product cannot reach 0.
  - **What would settle it, cheaply:** the fixups tell you what the broken state
    *looks like*, so it is directly observable rather than derivable — on a
    long-running save, dump every `RequiresMaintenance` whose
    `maintenance_phase` is truthy or `is_malfunctioned` is set, and check
    (a) `maintenance_work_request` present, (b) present **in
    `task_requests`**, (c) `:GetSource() == obj`, (d) `rfSuspended` clear while
    `ui_working` is true. Any building failing (b)/(c) is the producer firing
    live on our build. That is a console sweep, not a source question, and it
    needs a heavily-loaded save — so it belongs to the playtest campaign, not
    to this chain. **Not promoted; stays `cand`.**
    **→ WRITTEN UP as a checklist rider 2026-08-02 (`PLAYTEST_CHECKLIST.md` §6,
    "C26 stranded-maintenance dump")** — one console line, four named failure
    reasons, and ⭐ **`bad = 0` on an old heavily-built colony is the useful
    result**: a couple of clean dumps close this entry, one dirty line earns it
    an F-row on the spot.
  - **✅ FIRST READING TAKEN 2026-08-02 (owner, live) — CLEAN.**
    Log `Mars.exe-20260802-01.31.10`, line 225, taken ~59 s after load on
    `BlankBigCanyonCMix_09` before anything perturbed state, **sol 288**, both
    mods on, save on the current patch:
    **`10 buildings in maintenance or malfunction, 0 structurally broken`** —
    and **zero individual reason lines**, no `[LUA ERROR]`, no `not understood`.
    ⭐ **The `10` is the control that makes the `0` mean something**: a `0, 0`
    result could not be told apart from a query that silently matched nothing,
    whereas ten live `RequiresMaintenance` objects in maintenance-or-malfunction
    state prove the walk reached real candidates and **none of them carried a
    stranded request** on any of the four axes the vendor fixups repair.
    **Reading: over 288 sols of play, the producer did not fire once.** That is
    the strongest evidence this entry has and it points at CLOSE.
  - ⚠️ **NOT closed on one reading, deliberately.** The rider asked for a couple,
    and the reason stands: a single dump is a snapshot, and a transient or
    self-healing state could be missed between samples. **What would close it:**
    one more clean dump on a **different colony** (different history, not the
    same save later), or a second clean dump on this save several sessions on.
    ✅ **The vintage qualifier was RESOLVED the same sitting, and it lands on
    the strong side.** `OrigLuaRev` is a `GameVar` that captures `LuaRevision`
    at new-game and persists it — the engine's own bug dump labels it *"Game
    Start Rev"* (`CommonLua\SavegameMetadata.lua:288-290`, `:301-302`). Read
    live: **`founded on rev 396349 | running rev 396349 | last saved on rev
    396349`** — i.e. founded on the pinned build **1.0.7.396349** itself. So
    both fixups were **pre-seeded into `AppliedSavegameFixups` at new-game and
    never ran on this save**, and all 288 sols are unhealed live evidence.
    ⚠️ **Known limit on that inference, stated so it is not over-read:**
    a `GameVar` missing from a save is initialized **at load**, so if
    `OrigLuaRev` itself postdates the save, an old colony would be stamped with
    today's revision and read as new. Source alone cannot exclude that.
    **It does not change the direction of the result** — in the worst case the
    fixups healed once at the first load on this build and every sol since is
    still live evidence. **Free independent cross-check if anyone wants it
    later:** `UndergroundRework106` is a GameVar defaulting to the literal
    `false` and set `true` only in `OnMsg.NewGame`
    (`Lua\Buildings\UndergroundDome.lua:16-19`) — the **opposite** failure mode,
    since an old save loading on a new build keeps `false`. `true` brackets the
    colony at ≥1.0.6 independently of `OrigLuaRev`.
  - ⚠️ **A SECOND DUMP WAS TAKEN THE SAME SITTING AND IT IS *NOT* READING 2 —
    recorded explicitly so nobody later mistakes it for the confirming sample.**
    Same log, line 274: **`3 in maintenance or malfunction, 0 structurally
    broken`** on a 98-sol save. Clean, control non-zero — **but it is the SAME
    COLONY LINEAGE.** Both loads print `save_game_id: HdmSxGs6kyd0uz6-` with the
    same sponsor (NASA), profile (`rocketscientist`), coordinates (`0N107E`) and
    map (`BlankBigCanyonCMix_09`): sol 98 is an *earlier point in the same
    playthrough* as sol 288, so its history is a **subset** of reading 1's, not
    an independent sample. It adds essentially nothing to the count.
    ✅ **What it did settle is the VINTAGE.** It returned
    `UndergroundRework106 = true` — the independent cross-check with the
    opposite failure mode, since a pre-1.0.6 save keeps `false` however often it
    is loaded. Two mechanisms now agree, so the "GameVar stamped at load" hole
    noted above **is closed**: the lineage really was started at/after 1.0.6 on
    the current build, and its sols are unhealed live evidence.
  - ✅ **READING 2 TAKEN 2026-08-02 ON A GENUINELY INDEPENDENT COLONY — CLEAN.**
    Same log, line 318. `save_game_id: 91Wh-Fin5FhlZmaF` (vs
    `HdmSxGs6kyd0uz6-`), coordinates `32S21W`, map `BlankBig_02` — a different
    playthrough, **checked in the log rather than assumed**, which is the step
    that caught the false reading 2 above. An **early-playtest save not opened
    in a long time, sol 59, of which ~50 sols were organic pre-playtest play**:
    **`2 in maintenance or malfunction, 0 structurally broken`**, zero reason
    lines. Taken cold within a minute of load (the owner's default 20-30 min
    warm-up deliberately overridden, for comparability with reading 1).
  - ⭐ **The masking condition was checked BEFORE the result was trusted, and it
    passed.** Both fixups run *at load*, so on a save that predated them a clean
    dump would mean *"they just healed it"* rather than *"nothing was broken"*.
    Vintage came back **`founded rev 396349 | running rev 396349`** — founded on
    the pinned build, so both were pre-seeded into `AppliedSavegameFixups` and
    **never ran here**; `UndergroundRework106 = true` corroborates on the
    independent mechanism. The clean result is real, not a heal artefact.
    *(Asymmetry worth keeping: only a CLEAN result needed this check — a dirty
    line would have been a finding whatever the vintage.)*

  **⛔ VERDICT 2026-08-02: CLOSED — `wontfix`, no defect reachable on
  current-build saves.** Three legs, and it is negative evidence, stated plainly
  rather than dressed up:
  1. **No producer exists in current Src** — the sweep above, with both obvious
     candidate mechanisms checked and ruled out in writing.
  2. **THREE independent colonies, 347+ sols of combined history** (288 + 59 + a
     third lineage, plus
     the ~50 organic pre-playtest sols inside the second), **both founded on the
     pinned build so neither was ever healed by the fixups**, both returning
     **zero** structurally broken maintenance requests across all four axes those
     fixups repair.
  3. **The control was non-zero in both** (10 and 2 buildings genuinely sitting
     in maintenance/malfunction), so the walk demonstrably reached live
     candidates instead of matching nothing — which is the failure mode this
     kind of dump usually dies of.
  - ⚠️ **A FOURTH DUMP WAS TAKEN AND IS VACUOUS — recorded so it is never
    counted as a third confirmation.** Log line 359, a genuinely independent
    third colony (`save_game_id: Dps_S53Fxrq6RJPv`, map `BlankBig_01`), returned
    **`0 in maintenance or malfunction, 0 structurally broken`**. **`n = 0` is
    the ambiguous case** — no candidates were found, so nothing was inspected,
    and it cannot be distinguished from a query matching nothing. It is a young
    basic colony, so nothing has yet accumulated enough maintenance to be in
    `maintenance_phase` or malfunctioned; that is expected, not surprising.
    **Neither supports nor undermines the close.** ⭐ **General rule this
    illustrates: a dump of this shape is only readable when `n > 0`** — always
    report `n` alongside `bad`, and treat `0 / 0` as "no measurement taken".
  - ✅ **READING 3 — A THIRD INDEPENDENT COLONY, ALSO CLEAN, AND THIS ONE HAS A
    HEALTHY CONTROL** (log line 443). `save_game_id: 1f6oCbWfYS7IOPCY`
    (NASA/politician, `15N130E`, map `BlankUnderground_01`, `game_rules:
    NoDisasters`) — a fourth distinct lineage, id checked in the log:
    **`4 in maintenance or malfunction, 0 structurally broken`**, zero reason
    lines, `founded rev 396349 | running rev 396349` so the vendor fixups never
    ran here either. **`n = 4` makes it readable**, unlike the vacuous `0 / 0`
    below. **Three independent colonies now agree.**
  ⚠️ **Limits, so this is not over-read:** three samples is three samples, and
  reading 2's control of `2` is thin. This closes C26 as **"not reachable in
  Relaunched on saves started at 1.0.7.396349"** — *not* as "impossible" — and it
  says nothing about saves old enough for the vendor fixups to have run, which is
  the vendor's own heal path and not our concern. **A dirty line on any
  current-build save reopens this immediately**, and the four reason strings each
  name a distinct producer.
- **C27 [author] — Signal Boosters never extend Drone Hub Extender radius.**
  SkiRich (OG, 2611877948): *"After researching Signal Boosters both the
  Drone Hubs and Drone Hub Extenders are suppose to have an additional 15 hex
  radius… the missing code… to make the Drone Hub Extenders have that extra
  15 hexes."* F77's file neighborhood — check Relaunched.
  **→ SWEPT 2026-08-02 (prompt 6c). Verdict: NO DEFECT IN CURRENT SRC —
  CLOSED. The "missing code" is present; it is just written on the hub instead
  of on the extender, so reading the extender's file alone makes it look
  absent.** (Nothing said here about OG — only that the current chain is
  complete.)
  - **6b's label lead: CHECKED AND RULED OUT — this is NOT the C22/C38
    empty-label class.** The tech carries two `Effect_ModifyLabel`s
    (`Data\TechPreset.lua:3462-3471`): `DroneHub`.`service_area_max` +15 and
    **`DroneHubExtender`.`work_radius` +15**. `DroneHubExtender` is the
    BuildingTemplate **class name**
    (`Lua\BuildingTemplate\DroneHubExtender.generated.lua:4`), so under 6b's
    rule the building is filed under it and the modifier lands on a non-empty
    set. `work_radius` is genuinely modifiable (`DroneControl.lua:40`,
    `DroneNode` property), and `Effect_ModifyLabel:OnApplyEffect` registers a
    **persistent colony label modifier** (`Lua\MarsGameEffects.lua:161-172`),
    so extenders built *after* the research inherit the +15 too.
  - **The real question was the COMMIT step, and it is covered.** Neither
    `DroneHubBase:OnModifiableValueChanged` (`Lua\Buildings\DroneHub.lua:88-92`)
    nor `DroneHubExtenderBase:OnModifiableValueChanged`
    (`Lua\Buildings\DroneHubExtender.lua:180-184`) does more than redraw the
    range ring, and only while the object is selected — so raising the number
    does not by itself rebuild anyone's serviced-building set, which is guarded
    by `are_requesters_connected` (`DroneControl.lua:328`, cleared only in
    `DisconnectTaskRequesters` `:441-450`). **The tech's third effect is what
    commits it** (`Data\TechPreset.lua:3474-3481`): it walks
    `colony.labels.DroneHub` and calls
    `hub:SetUIWorkRadius(hub.work_radius + const.SignalBoostersBuff)` →
    `SetWorkRadius` → `DelayedCall(300, ReconnectTaskRequesters)`
    (`DroneControl.lua:759-785`). ⭐ **And `FindTaskRequesters` recurses into
    `node.linked_extenders`, re-reading each extender's live `work_radius`**
    (`:315-325`) — so the hub's forced reconnect picks up every extender in the
    chain at its NEW radius. Extenders can only uplink to a hub or to another
    extender (`DroneHubExtender.lua:57-60`), so every extender chain roots at a
    `DroneHub` and every extender is reached. The value change is real
    (`hub.work_radius` is still 35 at that point — `GameInit` copies
    `service_area_max` once, `DroneHub.lua:39-44` — so `SetWorkRadius(50)`
    passes its equality guard at `:761`).
  - **Positive control that the engine expects the boosted extender radius:**
    `const.CommandCenterDefaultRadius = 35`, `const.SignalBoostersBuff = 15`,
    `const.CommandCenterMaxRadius = 50` (`Lua\_GameConst.lua:62-72`) — the
    outer search bound is **exactly** default + buff, and it is the bound used
    by both the building-side connect (`TaskRequester:FindDroneNodes`,
    `Lua\_TaskRequest.lua:251-257`, which filters on live `node.work_radius`)
    and the placement-time coverage test
    (`DoesAnyDroneControlServiceAtPoint`, `DroneControl.lua:1014-1020`). A
    50-hex extender is not clipped anywhere.
  - **Belt and braces:** extenders also fully reconnect their uplink on any
    working-state flip (`OnSetWorking` → `UpdateUplinkRequesters`,
    `DroneHubExtender.lua:171-178`, `:109-124`), on link/unlink (`:141-154`),
    and every hub reconnects on `OnMsg.DepositsSpawned`
    (`DroneHub.lua:188-199`, whose comment `--template name label` is itself an
    independent confirmation of 6b's label rule).
  - **Residual, named so it is not re-derived:** the `Effect_Code` rewrites
    `UIWorkRadius` to `work_radius + 15`, which silently **overrides a player's
    manually lowered hub range slider** on research completion. Cosmetic,
    upward-only, not a promise break — noted, not filed.
- **C28 [author] — Transport Optimization never applied to RC Transports.**
  SkiRich (OG, 2609028695): *"the missing code that is required to make the
  RC Transport obey the Tech upgrade Transport Optimization… should be able
  to carry 45 of every resource."*
  **→ SWEPT 2026-08-02 (prompt 6c). Verdict: NO DEFECT IN CURRENT SRC —
  CLOSED. Every link in the chain checks out, and SkiRich's own number (45) is
  the arithmetic the current data produces.**
  - **The tech** (`Data\TechPreset.lua:3577-3598`) carries two effects:
    `Consts`.`RCTransportGatherResourceWorkTime` **-50%** (the "harvest faster"
    half) and **`RCTransportAndChildren`.`max_shared_storage` +15**.
  - **Label check (6b's lead) — RULED OUT.** `RCTransport:AddToCityLabels`
    files the rover under `RCTransportAndChildren` explicitly
    (`Lua\Units\RCTransport.lua:88-90`); the label is declared
    (`Data\Label.lua:216-218`); and `RCHarvester` inherits `RCTransport`
    (`Lua\Units\RCHarvester.lua:4`) so it is one of the promised "children".
  - ⚠️ **The colony-vs-city container question — the one thing that could
    plausibly have broken this — is answered and it is safe.** The rover is
    added to the **city**, but `City:AddToLabel` forwards to
    `self.colony:AddToLabel` **first** (`Lua\City.lua:83-86`), and the colony
    container is exactly where `Effect_ModifyLabel:OnApplyEffect` registers its
    modifier (`Lua\MarsGameEffects.lua:161-172` → `SetLabelModifier`). Both
    directions are covered: `SetLabelModifier` walks the existing members
    (`Lua\LabelContainer.lua:59-78`) and `AddToLabel` replays the stored
    modifiers onto any member added later (`:17-28`). Rovers built after the
    research get the +15 too.
  - **Arithmetic control:** `max_shared_storage` is declared on `RCTransport`
    itself as `modifiable = true`, `scale = const.ResourceScale`, default
    `30 * const.ResourceScale` (`Lua\Units\RCTransport.lua:14`), and
    `Effect_ModifyLabel` multiplies `Amount` by that same scale
    (`MarsGameEffects.lua:166-171`). **30 + 15 = 45**, SkiRich's figure exactly.
    The value is read live on every capacity test (`RCTransport.lua:118, :282,
    :311, :1709`) — nothing caches it.
  - ⭐ **This sweep also overturned a rule 6b recorded — see the correction on
    the C18 entry.** The near-miss that produced it: `RCTransport` defines its
    own `AddToCityLabels` **without calling `BaseRover`'s** (`:134-138`, which
    adds `Unit`/`Rover`/`self.class`), which reads as a classic
    override-drops-the-parent defect. It is not one:
    `DefineCombinedMethod("AddToCityLabels", "call")`
    (`Lua\CityObject.lua:8`, machinery at
    `CommonLua\Core\classes.lua:1499-1511`) makes the flattened method call
    **every** parent's implementation. Checked and ruled out, written down so
    it is not re-derived.
- **C29 [author] — children-only buildings admit all age groups.** SkiRich
  (OG, 2428123536): *"the missing code that is required to make Child Only
  Buildings, such as the Nuseries, omit any other age group."*
  **→ SWEPT 2026-08-02 (prompt 6c). Verdict: NO DEFECT IN CURRENT SRC —
  CLOSED.** `children_only` is set on exactly five templates —
  `Nursery`, `LargeNurseryCCP1`, `Playground`, `School`, `SchoolSpireCCP1` —
  and those fall into **three** enforcement families, all of which filter at
  **assignment** time, not merely at use time:
  - **Residences** (`Nursery`, `LargeNurseryCCP1`). `Residence:GameInit`
    converts the flag into `exclusive_trait = "Child"`
    (`Lua\Buildings\Residence.lua:26-28`), which is then the operative filter in
    `IsSuitable` (`:162-167`), `CanReserveResidence` (`:250-255`),
    `ColonistInteract` (`:300`), the manual-assign UI (`:280-282`) and the
    home-scoring pass (`:388-389`). `IsSuitable` is an `"and"`-combined method
    (`Building.lua:14`) and `ChooseResidence` re-tests it on the *current* home
    (`:404`), so an aged-up colonist also stops qualifying.
  - **Training buildings** (`School`, `SchoolSpireCCP1`).
    `TrainingBuilding:CanTrain` rejects non-children when `children_only`
    (`Lua\Buildings\TrainingBuilding.lua:367-376`) and is reached from
    `TrainingBuilding:IsSuitable` (`:137-138`), which the workplace assignment
    consults at `Lua\Buildings\Workplace.lua:930` and `:1083` — so this is a
    hiring filter, not just a training-tick filter.
  - **Services** (`Playground`). `ServiceBase:CanService`
    (`Lua\ServiceBase.lua:172-178`) via `CanBeUsedBy` (`:162-170`).
  - **Obvious guess CHECKED AND RULED OUT — and it was the C22 shape, so it was
    worth checking.** If the age trait were only ever *added*, every adult would
    still carry `Child` and all three filters would pass for everyone. It is
    removed: `Colonist:UpdateAgeTrait` calls `self:RemoveTrait(cur_trait)`
    before adding the next (`Lua\Units\Colonist.lua:1740-1756`, removal at
    `:1747`). The key the filters read (`traits["Child"]`) is also the exact key
    `AddTrait`/`RemoveTrait` write — no C22-style string mismatch.
- **C30 [author] — supply-pod reward pins stuck on HUD.** SkiRich (OG,
  2636538587): *"Fixes an issue with vanilla code that causes supply pod pins
  to get stuck on the HUD."*
  **→ SWEPT 2026-08-02 (prompt 6c). Verdict: NO DEFECT IN CURRENT SRC —
  CLOSED. But this is the one of the five where the mechanism he describes is
  visibly present in the generic path, and only per-class guards close it** —
  worth recording because a future engine change that adds a pinnable class
  would re-open it.
  - **The hazard, exactly.** `PinnableObject:Done` unpins by calling
    `self:TogglePin()` with **no `force`** (`Lua\PinnableObject.lua:160-164`),
    and `TogglePin`'s unpin branch is gated `if self:CanBeUnpinned() or force`
    (`:226`). A class whose `CanBeUnpinned()` is false therefore **stays in
    `map.pinned` after destruction and its `PinButton` is never closed** —
    `pins_dlg:Unpin(self)` lives inside that same guarded branch (`:230-232`).
    `map.pinned` is a `MapVar` (`:6`), so the stale entry is saved, and
    `SortPins` does not drop it (its trailing "everything else" pass re-adds
    from the old list, `:72`, and it only runs at all when `#pinned > 1`,
    `:47`). That is a stuck HUD pin, verbatim.
  - **`CanBeUnpinned()` is false unconditionally for both rocket families** —
    `RocketBase:CanBeUnpinned()` (`Lua\Buildings\RocketBase.lua:1476-1478`) and
    `UniversalRocketBase:CanBeUnpinned()` (`Lua\UniversalRocket.lua:1112-1114`)
    — and supply pods are in both: `SupplyPod` → `SupplyPodBase` →
    `SupplyRocketBase` → `RocketBase` (`Lua\Buildings\SupplyPod.lua:2-3`), and
    `UniversalSupplyPod`/`UniversalDropPod` → `UniversalSupplyPodBase` →
    `UniversalRocketBase` (`Lua\UniversalPod.lua:2-4`).
  - **Both families close it in their own `Done`, and this is what makes the
    verdict "no defect" rather than "broken":**
    `RocketBase:Done` calls `self:SetPinned(false)` (`:194-199`), and
    `PinnableObject:SetPinned` toggles with **`"force"`**
    (`PinnableObject.lua:245-249`), bypassing the guard.
    `UniversalRocketBase:Done` calls `self:SetPinOnMap(false)`
    (`UniversalRocket.lua:1069-1074`), whose falsy-`target_map` branch is a
    forced `TogglePin("force")` (`:1158-1165`). The salvage/shutdown paths
    unpin ahead of destruction too (`SupplyPod.lua:145`,
    `UniversalPod.lua:145`), so the pod's pin is normally gone before the
    player ever demolishes the wreck.
  - **The third and last `CanBeUnpinned()==false` class was checked too, and it
    is saved by call ORDER rather than by a guard.** `OrbitalProbe:CanBeUnpinned`
    is `not label or not next(label)` (`Lua\OrbitalProbe.lua:119-122`), only the
    first probe is pinned (`:35-48`), and `ScanSector` destroys `label[#label]`
    (`:112`) — so the pinned probe is destroyed exactly when it is the last one.
    `OrbitalProbe:Done` removes it from the label (`:53-56`) and does **not**
    force-unpin, so this works only if the derived `Done` runs before
    `PinnableObject:Done`. **It does:**
    `DefineCombinedMethod("Done", "procall_parents_last", "InitDone")`
    (`CommonLua\PropertyObject.lua:1664`). By the time the parent runs, the
    label is empty, `CanBeUnpinned()` is true, and the pin is released.
  - ⭐ **Engine facts this settled, now in `ENGINE_FACTS.md`:** `Done` is a
    combined method running **most-derived first** (`procall_parents_last`)
    while `Init` runs **parents first** (`procall`, `PropertyObject.lua:1663`).
    That is what makes a class's own `Done` able to prepare state its parents'
    `Done` will read.
- **C31 [author→RESOLVED 2026-08-01] — meteor storms broken in 1.0.7.396349 —
  OUR PINNED BUILD.** GromGor (Relaunched, workshop 3745475097): *"The latest
  update broke the meteor storm mechanics in a strange way. I don't know the
  exact cause of this issue, but I think I've found a temporary solution."*
  **The owner subscribed and the FPK was extracted+read (2026-08-01):** his
  mod is (a) a one-shot `OnMsg.LoadGame` → `StopMeteorStorm()` heal behind a
  `MeteorsFixed` GameVar, and (b) a global `GenerateDir` clone. **(b) is a
  NO-OP for meteors** — vanilla's `GenerateDir` is a *file-local* in
  `Meteors.lua:43-55` (his clone is byte-identical to it INCLUDING the
  degenerate-case guard, so nothing is even changed), and vanilla call sites
  resolve the local, never his global. The effective ingredient is (a) — the
  same wedged-storm heal family as our F78. **Verdict: not a new mechanism;
  independent corroboration that the F78 wedge state still occurs in
  1.0.7.396349.** Side find: `Bombardment.lua:38-50` carries a sibling
  `GenerateDir` whose guard checks only `c == 0` and not the zero-dir case —
  minor, F26's neighborhood, noted not filed.
- **C32 — buildings drop out of the `ShiftsBuilding` colony label and stay
  stuck on their last workshift forever.** Filed 2026-08-01 from GromGor's
  "Patch 1.0.6 Workshifts FixUp" source (workshop 3676027320, extracted): his
  fix runs every `NewWorkshift` and re-adds any `ShiftsBuilding` present in
  `UICity.labels.Building` but missing from `UIColony.labels.ShiftsBuilding`,
  then delivers the missed `SetWorkshift(CurrentWorkshift)`. Implication:
  vanilla's workshift tick iterates `UIColony.labels.ShiftsBuilding` only, so
  a building that falls out of that label (map unload? relabel path?) never
  changes shift again. **This — not our F04 — is the better mechanism match
  for the Steam witness thread "Buildings are stuck on night shift"**
  (colony-wide BUILDING shift stuck; one reporter correlates onset with "an
  asteroid had recently gone out of range", which fits a label rebuilt on map
  transitions). Needs our own sweep: find the de-labeling path in Src,
  whether `AddToLabel` on re-registration is safe, **and — owner challenge
  2026-08-01 — whether 1.0.7 already fixed it**: GromGor's mod is titled
  "Patch **1.0.6** Workshifts FixUp", and this is the one packed-source
  finding NOT verified against current Src by this session (unlike
  C22-C24/C33, which were read in today's proven-parity source; game install
  confirmed unchanged since the parity proof — last Steam update 2026-06-24,
  parity run 2026-07-29). The witness thread's reports (Mar 13 / Apr 26) are
  post-1.0.6 but not provably post-1.0.7. F04's audit tier was corrected on
  this finding (see the F04 entry note) — if the sweep finds 1.0.7 fixed the
  label desync and the reports predate 1.0.7, re-examine F04's witness
  reassignment as well.
  **A live read now rides alongside the sweep** (`PLAYTEST_CHECKLIST.md` §6,
  bug-list-audit table, added 2026-08-01): after visiting and leaving an
  asteroid — the witness's own onset condition — count the `ShiftsBuilding`
  members of `UICity.labels.Building` missing from
  `UIColony.labels.ShiftsBuilding`; any non-zero count is the defect, observed
  on our pinned build. It does not replace the Src sweep (chain prompt 6) —
  a zero count proves nothing on its own — but a non-zero one settles the
  1.0.7 question in the direction that matters.
  ⚠️ **That rider was rewritten by the sweep below — its trigger no longer
  occurs automatically on 1.0.7, and its "any non-zero count is the defect"
  rule is WRONG.** Corrected row in `PLAYTEST_CHECKLIST.md` §6.

  ---

  ⭐ **SRC SWEEP RUN 2026-08-01 (chain prompt 6) — MECHANISM NOT CONFIRMED;
  C32 DOWNGRADED, AND THE OWNER'S 1.0.7 CHALLENGE IS ANSWERED "TRIGGER YES,
  MECHANISM NO".** Every line below was read this session in
  `<game>\ModTools\Src` (1.0.7.396349, install unchanged since the parity
  proof). GromGor's mod was re-extracted from the archived FPK
  (`C:\Dev\workshop_fpk_archive\3676027320`) and read in full — it is ten
  lines, `metadata.lua` `lua_revision 350453` / `saved_with_revision 387175`,
  i.e. authored against a pre-1.0.7 build.

  **1. The label has exactly ONE add site and ONE remove site in all of Src.**
  Add: `ShiftsBuilding:GameInit` → `self.city:AddToLabel("ShiftsBuilding",
  self)` (`Lua\Buildings\ShiftsBuilding.lua:50`), immediately followed by
  `self:SetWorkshift(CurrentWorkshift)` (:51). `City:AddToLabel`
  (`Lua\City.lua:83-86`) mirrors into `self.colony` — which is `UIColony`,
  assigned at `City.lua:44` — **and** the city's own container, so colony
  membership is established once per object lifetime and never renewed.
  Remove: `ShiftsBuilding:RemoveFromShiftsBuildingLabel` (:54-57), which
  **self-disables** (`self.RemoveFromShiftsBuildingLabel = empty_func`, :56),
  reached only from `OnDestroyed` (:59-61) and `Done(done_map)` (:63-66, which
  early-returns when the whole map is being torn down). The only other
  subtraction is the generic invalid-purge: `OnMsg.PostDoneMap` →
  `UIColony:ValidateLabels()` (`Lua\Colony.lua:116-120`) and
  `OnMsg.PostLoadGame` → `ForEachLabelInColony("ValidateLabels")` (:152),
  whose filter defaults to `IsValid` (`CommonLua\LabelContainer.lua:15-33`).

  **2. No route exists in current Src for the defect as this entry states it.**
  For a *valid, non-destroyed* building on a *loaded* map there is no path out
  of `UIColony.labels.ShiftsBuilding`: the single removal site requires
  `OnDestroyed`/`Done`, and `ValidateLabels` drops invalid objects only.
  Buildings never change maps — the `OnTransferToMap`/`OnTransferToMapDone`
  pair (`Lua\CityObject.lua:70-81`) is called for rockets, rovers and units,
  and `ShiftsBuilding` sits deliberately outside the
  `AddToCityLabels`/`RemoveFromCityLabels` combined methods anyway. One
  non-permanent path does exist: `WaitChangeWorkshift` (:78-87) walks the live
  label array by `ipairs` index and **yields** (`Sleep(50)` every 50
  buildings, :82-84), so a concurrent removal shifts the array left and skips
  buildings — **for that tick only**; they take the correct shift at the next
  `NewWorkshift`. It cannot produce "stuck forever".

  **3. What GromGor's predicate actually detects is a different, benign
  asymmetry — so "his fix works in the wild" is NOT evidence for this entry.**
  `ShiftsBuilding:OnDestroyed` de-labels, but `Building:OnDestroyed`
  (`Lua\Buildings\Building.lua:1366-1367`) is **empty** and
  `Building:RemoveFromCityLabels` (:446-460) is not called on destruction. So
  every **destroyed-but-not-yet-rebuilt** building is valid, still in
  `UICity.labels.Building`, and absent from `UIColony.labels.ShiftsBuilding` —
  matching his predicate exactly, on every workshift, in every colony that has
  ever been hit by a meteor. It is not a defect: `SetWorkshift` early-returns
  on `self.destroyed` (:90), and the rebuild path replaces the object entirely
  (`Building:Rebuild` → `PlaceConstructionSite` with `params.rebuild = self`
  → `DoneObject(self.rebuild)` at `ConstructionSite.lua:1539-1541`, so the
  fresh object runs `GameInit` and re-labels itself). Side effect, under his
  mod only: re-adding a destroyed shell makes the label entry permanent,
  because `RemoveFromShiftsBuildingLabel` has already self-disabled, so the
  later `DoneObject` cannot remove it and the colony label accumulates invalid
  entries until the next `ValidateLabels`.

  **4. Is `AddToLabel` re-registration safe? Guarded against double-add — and
  useless as a repair for the one desync it is meant to fix.**
  `City:AddToLabel` → `Colony:AddToLabel` → `LabelContainer:AddToLabel`
  (`Lua\LabelContainer.lua:17-28`) → `CommonLua\LabelContainer.lua:39-66`,
  which early-returns on the **key map** (`if objs[obj] then return end`, :44).
  So a stray re-add cannot duplicate the array entry and cannot double-apply
  label modifiers (`Lua\LabelContainer.lua:21-26`; no shipped
  `Effect_ModifyLabel` targets this label — grep over `Data/` — though
  `Data\Label.lua:268` declares it, so content could add one). **But that same
  guard means `AddToLabel` cannot re-insert an object whose key bit is still
  set while its array entry is gone.** GromGor tests membership with
  `table.find(UIColony.labels.ShiftsBuilding, bld)` — an **array** search — so
  in exactly that state his re-add silently no-ops and only his direct
  `bld:SetWorkshift(CurrentWorkshift)` does any work, every shift, forever.
  **Binding on any fix we ever write:** test membership the way the engine
  does (`UIColony:IsInLabel("ShiftsBuilding", bld)`,
  `CommonLua\LabelContainer.lua:106-109`) and repair the key map, never assume
  `AddToLabel` will re-insert.

  **5. Owner challenge — "did 1.0.7 already fix it?" ANSWER: 1.0.7 killed the
  TRIGGER the witness named, and left the mechanism untouched.** The onset
  condition in the thread ("an asteroid had recently gone out of range") is
  structurally dead on our pinned build: `Lua\Asteroids.lua:1` —
  `GameVar("AsteroidsNeverLeave107", false)  -- false in old savegames, true
  for 1.0.7 and later`, set true on `NewGame` (:5); `Asteroids:AddAsteroid`
  captures every asteroid at birth (`self:CaptureAsteroid(asteroid,
  "AsteroidsNeverLeave107")`, :208) and `CaptureAsteroid` clears `end_time`
  (:327); `GetRemainingTime` (:108-110) therefore returns false, so the expiry
  branch of `Asteroids:HourlyUpdate` (:147-158) — the only *automatic* caller
  of `RemoveAsteroid` → `RemoveAsteroidMapAsync` → `RemoveAsteroidMap` →
  `ChangeMapInSlot(map.slot, "")` (:56-67, :244) — never fires;
  `Asteroids:ReleaseAsteroid` (:331-348) has its **entire body commented
  out**; and old saves are retro-fixed by
  `SavegameFixups.AsteroidsNeverExpire` (:493-500). The surviving routes to an
  asteroid-map unload are the player's own `Asteroids:UIAbandonAsteroid`
  (:21-26) and `SavegameFixups.ClearInvalidAsteroids` (:450-468).
  **Against that, the label code is unchanged:** there is exactly **one**
  `OnMsg.NewWorkshift` handler in all of Src (`ShiftsBuilding.lua:73-76`), it
  still hands `WaitChangeWorkshift` nothing but `UIColony.labels
  .ShiftsBuilding`, and 1.0.7 added no membership check, no re-registration
  and no repair pass. So "1.0.7 fixed it" is true of the trigger and false of
  the code this entry describes.

  **Verdict: C32 stays a candidate, DOWNGRADED — no F-row, no fix.** Not
  closed: this session read 1.0.7 only, and the thread's reports (Mar 13 /
  Apr 26) are 1.0.6-era, where automatic asteroid expiry did unload maps. What
  is now established is that (a) the mechanism as written has no route in the
  code we ship against, (b) the evidence that made it look real — his fix
  firing in the wild — is fully explained by destroyed buildings, and (c) its
  named trigger cannot occur unattended on our build. Decision package is
  prompt 7's.
- **C36 — "Inner Light" does not complete for some players. ✅ SOLVED THE SAME
  DAY IT WAS FILED — it is NOT a new defect. It is a downstream victim of
  F81(a), and OUR PACK ALREADY FIXES IT.** Filed and closed 2026-08-01.
  **Filed from** two **current** Reddit threads (`BUG_LIST_AUDIT.md` §10.6,
  [S37]/[S38]), same commenter twice, days apart, as standing advice to
  newcomers: *"At least one mystery is broken for some people so **avoid Inner
  Light**"* and *"**Inner light is also broken for some people** so pick a
  different mystery."*
  **Solved by reading Src this session** (`Lua\Mysteries\Dream.lua:20-34`).
  Inner Light **is** `DreamMystery` (`:4` `scenario_name = "Mystery 4"`, `:6`
  `display_name = "Inner Light"`), and it advances by dreams. The mirage loop is:
  ```lua
  while UIColony.mystery.state == "running" do
      if IsDisasterPredicted() or IsDisasterActive() then
          Sleep(5000)
      else
          Dream(city) ; Sleep(...)
      end
  end
  ```
  **`IsDisasterPredicted()` is precisely what F81(a) strands permanently true** —
  every meteor storm that completes normally leaks `g_DisastersPredicted`
  (`MapSettings.lua:169/176`; `Meteors.lua:179` with no removal on the normal
  tail). Once stranded, this loop takes the `Sleep(5000)` branch **forever**, no
  `Dream()` ever fires again, the scenario's `WaitMsg("MysteryDream")` (see the
  comment at `:24`) never returns — **and the mystery silently stops advancing.**
  **It also explains the "for some people" qualifier exactly**, which is what
  makes this more than a guess: whether you are affected depends on whether a
  meteor storm has completed (or a Capture Meteors POI has fired) during your
  run. Players who never stranded the flag see Inner Light work fine.
  **This was half-recorded and never joined up.** `REACHABILITY_AUDIT.md` §F81
  already listed *"the Inner Light dream cycle"* among the leak's downstream
  victims. What was missing was that it lands in play — the community supplied
  that, and the source read confirms it. Recorded fact, now verified rather
  than inherited.
  ⭐ **The wider point, and it is the best illustration this project has of it:
  ONE commenter gave TWO separate pieces of advice — "install the disasters
  mod" and "avoid Inner Light" — for what is almost certainly ONE defect.**
  Players experience a single root cause as several unrelated "bugs" and never
  connect them (see `BUG_LIST_AUDIT.md` §10.6f).
  **Disposition: no F-row, no new fix.** F81's `Fix_DisasterPredictionLeak`
  removes the leak and sweeps stranded flags on load, so a pack user's Inner
  Light run should simply work. **What is NOT proven:** nobody has watched Inner
  Light recover live. **Cheap settling observation if anyone wants it** — on a
  save with the flag stranded, confirm the mystery is stalled, apply the pack,
  and see whether dreams resume. Recorded on F81, not scheduled here.
- **C37 — planetary anomalies do not pull colonists up the elevator, blocking a
  purely-underground colony (current build).** Filed 2026-08-01 from [S38], a
  thread **hours old** at the time of reading, from a commenter describing their
  own recent playthroughs (`BUG_LIST_AUDIT.md` §10.6): *"**You can't do a purely
  underground run right now because of planetary anomalies not pulling people up
  the elevator** — but my most recent Europe game was as an underground, trains
  only, no shuttles run and it was great."*
  **Why it is filed:** it is specific, current, names the mechanism location
  (the anomaly → colonist-transfer path across the elevator), and states a
  concrete gameplay consequence rather than a vibe. It also sits next to a
  proven cross-map defect of our own — **F90** showed the elevator's grid merge
  makes two maps one object in a way the surrounding code does not expect, and
  *"anomalies don't pull people up the elevator"* is the same seam.
  ⚠️ **Single source, no mechanism read, and the reporter is describing a
  limitation they worked around rather than filing a bug.** Not verified in Src
  by anyone. **Next step: find who moves colonists for a planetary anomaly and
  whether that path is map-aware at the elevator.**
- **C35 — applying an Edit Payload change while units are still on the cargo
  ramp tears down the rocket's command-centre connection with no wait, where
  every other path that does the same thing waits.** Filed 2026-08-01 by the
  chain-prompt-6 fredware-#11 comparison pass. **⚠️ NOT a decision package —
  it is a located mechanism with an UNPROVEN harm, and it must not go to
  prompt 7 until a live repro exists.**
  **Provenance.** fredware's Bug Fixes #11,
  `bf_restore_asteroid_lander_cargo_safety` (workshop 3775120166, re-extracted
  from the archive and read in full this session): *"Prevents v1.0.7 asteroid
  Lander payload changes from interrupting Drones or passengers while they are
  still using the cargo ramp."* His remedy wraps
  `LanderRocketBase:CanRequestPayload` and returns **false** whenever any of
  `drones_exiting` / `drones_entering` / `boarding` is non-empty — i.e. he
  disables the Edit Payload affordance rather than fixing anything downstream.
  **Verdict vs our lander family: a real GAP, zero overlap.** F67 wraps
  `IsCargoReady` (`UniversalRocket.lua:455-472`), F68/F71 wrap
  `CreateAutoCargoRequest` (:1742-1755), F70 replaces
  `CargoRequestNew:RetrieveRequests` and pre-wraps `:Apply`
  (`CargoRequestNew.lua:179-221`, :341-355). All three answer *what the payload
  contains*; his answers *when a payload change may be applied*. **None of ours
  reads the ramp lists at all** — and the nearest miss is our own: F70 already
  wraps `CargoRequestNew:Apply`, the exact call that fires the command switch
  below, and does not look at the ramp.
  **Mechanism, traced in Src this session.** The exposure window is real, not
  hypothetical: Edit Payload is offered exactly in the states where boarding is
  permitted — `CanRequestPayload` → `IsRocketLanded()` → `Refuel` /
  `WaitLaunchOrder` / `Idle` (`RocketBase.lua:2273-2275`; the lander adds
  `LoadAndLaunch`, `LanderRocket.lua:489-491`), while `IsBoardingAllowed`
  (`RocketBase.lua:2269-2271`) returns true for `Refuel` and `WaitLaunchOrder`.
  Confirming the payload then runs `CargoRequestNew:Apply` →
  `transporter:SetCommand("CmdLoad", self)` (`CargoRequestNew.lua:349`) →
  `UniversalRocketBase:CmdLoad` (`UniversalRocket.lua:424-449`) →
  `SetCargoRequest` (:436) → `CargoTransporter:SetCargoRequest`
  (`CargoTransporter.lua:1047-1050`) → `UpdateCargoResourceRequests`
  (:1016-1032), whose **first** statement is `self:DisconnectFromCommandCenters()`
  (:1017) and whose body re-sets every supply/demand amount from the new list
  (:1026-1028) before reconnecting (:1031).
  **The tell is a sibling asymmetry.** Vanilla's own takeoff path makes the
  identical call under the comment *"so no more drones climb the ramp"*
  (`RocketBase.lua:757`) and then **waits** — `while self:IsCargoRampInUse() do
  … Sleep(1000) end` (:762-768) — before going further. The payload path
  performs the same teardown with **no wait at all**. Vanilla also already
  ships the predicate fredware hand-rolled: `RocketBase:IsCargoRampInUse()`
  (:2277-2281), overridden with a dead-colonist sweep at
  `UniversalRocket.lua:1559-1569`; his `ramp_in_use` (his :84-92) is a
  re-implementation of it. **If we ever build this, call the engine's.**
  **Why this is NOT promoted, stated plainly.** (1) *The harm is not
  demonstrated.* Zeroing the demand for a resource the player just removed is
  the designed consequence of editing a payload; nobody has yet shown a drone
  or colonist ending up in a **bad** state rather than simply re-tasked.
  `OnRemovedFromTaskRequestHub` is empty in the base and has no Mars override
  (grep, whole tree), so the disconnect alone does not interrupt a drone that
  is already carrying. (2) *The author does not present it as settled either* —
  his catalog entry registers it `beta = true, default_enabled = false` (his
  :202-204). (3) *His remedy is a behaviour change, not a repair*: it removes a
  player action whenever any unit is on the ramp, which is FIX_POLICY §4
  territory and would have to clear that bar on its own merits.
  **Next step that would settle it (cheap, needs a sitting, NOT scheduled
  here):** with a lander landed and drones actively on the ramp, open Edit
  Payload, remove a resource that a drone is mid-delivery on, confirm — and
  watch whether that drone recovers or strands. Until that reading exists this
  stays a lead.
- **C38 [VERIFIED vs Src 2026-08-02] — the Astrogeologist commander profile
  promises "Extractor production increased by 10%" and pays it to 10 of the 12
  buildable extractors.** Filed by the C18 sweep (prompt 6b), which went
  looking for a *positive intent statement* about extractor label coverage and
  found one that does not keep its own promise.
  **The promise is unqualified.** `Data\CommanderProfilePreset.lua:333`:
  *"<bullet> Extractor production increased by 10%"* — no building is named,
  unlike XenoExtraction (C18), whose description names its four and pays
  exactly those four.
  **The payment is an enumeration of ten labels** (`:336-385`):
  `WaterExtractor`, `MetalsExtractor`, `PreciousMetalsExtractor`,
  `RegolithExtractor`, `MicroGExtractorMetals`, `MicroGExtractorRareMetals`,
  `MicroGExtractorExoticMinerals`, `MicroGAutoExtractorMetals`,
  `MicroGAutoExtractorRareMetals`, `MicroGAutoExtractorExoticMinerals`.
  **The two it misses are both real, buildable, currently-shipping
  extractors** — and since labels are exact-string with no inheritance
  (`Building.lua:413-424,:427-444`, established under C18), each is simply
  absent from the modifier:
  - **`AutomaticMetalsExtractor`** — *"Automatic Metals Extractor"*,
    `build_category = "MetalExtractors"` (a live build-menu subcategory,
    `Data\BuildMenuSubcategory.lua:445-447`), `production_per_day1 = 12000`
    (`Lua\BuildingTemplate\AutomaticMetalsExtractor.generated.lua:11,:52,:56`)
    — the exact prop the ten entries modify.
  - **`MicroGAutoWaterExtractor`** — *"Micro-G Water Extractor"*,
    `build_category = "LifeSupport"`, and its own upgrades modify
    `water_production` (`MicroGAutoWaterExtractor.generated.lua:21,:49,:53`) —
    the exact prop the `WaterExtractor` entry modifies. It shares
    `object_class = "WaterExtractorBase"` with `WaterExtractor` (`:9`), so a
    one-word change of the existing entry's label would cover both.
  **The sibling tell is the enumeration itself.** Ten entries hand-written in
  one preset is the game demonstrating it knows the full extractor roster;
  the two omissions are the two whose ids break the pattern the author was
  working down (base four, then the six `MicroG*Extractor<Resource>`), which
  is what an oversight looks like. Not a name-scoped promise like C18's.
  **Excluded as candidates, deliberately:** `MicroGExtractor` and
  `MicroGAutoExtractor` both carry `hide_from_build_menu = true`
  (`MicroGExtractor.generated.lua:18`, `MicroGAutoExtractor.generated.lua:19`)
  — legacy templates a player cannot build, so their absence is correct. The
  count is 10 of 12, not 10 of 14.
  **Not promoted.** Player-visible harm is a silent 10% shortfall on two
  buildings for one commander profile — real but small, and the §4 call
  (fix the omission vs. leave a balance number alone) is prompt 7's, not this
  sweep's. **If it is built, the shape is two added `Effect_ModifyLabel`
  entries or an `object_class`-level label, not a code patch.**

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
    study in `docs/reports/DRONE_OVERHAUL_OPTIONS.md`** — options A-G (repair moonlighting,
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
- Remaster player-report list (see `docs/archive/RESEARCH.md`) — several reports not yet mapped
  to code: seniors not auto-moving to retirement homes, mysteries not starting
  (Inner Light), no cold waves/dust storms triggering, asteroid lander launching empty,
  auto asteroid miners missing from build menu, Martian Express track salvage issues,
  universities training geologists after Extractor AI, Fast Rockets rule stopping,
  Single Party tension, can't rebuild on old building spots.
