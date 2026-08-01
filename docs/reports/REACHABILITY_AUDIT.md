# Reachability Audit — can a player actually reach each defect?

Audit date 2026-07-30, out of the F24 close (`dd72923`). Question asked of
every fix in the pack: **can a player reach the defective state by playing the
shipped game — no mods, no console, no developer tooling?** Not "is the defect
real" (established per fix, file:line, in BUGS.md) — whether fixing it buys a
player anything. Game build audited: **1.0.7.396349** (fpk parity proven —
ENGINE_FACTS.md). Every call-site enumeration below was made against
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, not against
BUGS.md's own claims. The audit ran as seven parallel subsystem sweeps plus a
lead pass; every non-R1 verdict, every R3/R4 claim, and every DELETE candidate
was re-verified against Src by the lead before entering this file.

**Tiers:** R1 live (ordinary play) · R2 conditional (needs a real condition:
rule, sponsor, mystery, map, legacy save — still a genuine player experience) ·
R3 latent-by-data (path reachable, no shipped data exercises it) · R4
unreachable (no path in the shipped game) · U unknown (the settling
observation is named).

**Headline: the pack survives the audit almost intact.** Of 66 fix modules +
2 sanitizer passes: ~21 land R1, ~38 R2, five R3 (all kept — four are cheap
§1.1–§1.4 patches; the §1.5 ones are flagged below), one U (F11, kept with a
settling observation), and two R4 — of which only one is a deletion candidate.

---

## DELETE candidates (user decides — nothing was deleted by this audit)

| Fix | Cost/benefit |
|-----|--------------|
| **F28** `Fix_ReplaceTechCount.lua` | **R4, verified twice.** `Research:ReplaceTech` has **zero callers in all of Src** — the whole-tree grep returns exactly one hit, the definition (Research.lua:684). Data-embedded scripts, codegen, cheats and DLC are all covered by that textual sweep; unlike the R3 latents this cannot go live by new *data*, it needs new *calling code*. Carried as a §1.5 full replacement (37-line body copy) with per-game-update re-verification cost. Benefit in unmodded play: zero. The only keep-argument is mod-ecosystem support (another mod calling ReplaceTech gets the fixed counter) — the F29 precedent, but F29's carry cost is smaller. Recommendation: **delete** (rollback is one `git revert`, the F24 pattern); if kept, re-classify explicitly as mod-facing support, not a player fix. |

**Explicitly NOT delete candidates despite R4/R3 findings:**
- **F49(a)** (instant-track pipes palette) is R4, but it shares
  `Fix_TrainMinors.lua` with (d) stale `max_vehicles` — live R2, play-proven
  (PT-46 tail); the (a) hook is a cheap additive post-wrapper that is a no-op
  for correctly-painted elements. Optionally strip the (a) wrapper on the
  next touch of that file. *(Corrected by Challenge review: this bullet
  originally also cited (c), whose "live R2" was asserted, wrong, and is now
  tier I — closed `wontfix`, guard removed, `d03417b`.)*
- **F27, F31, F43** are R3 with §1.1–§1.4 patches — exactly the
  "latent-but-cheap" class the decision rules keep.
- **F29** is R3 on §1.5 replacements — kept per its existing mod-facing
  rationale, but flagged: it is the same class of carry cost as F28, only
  smaller. If the user ever wants a stricter line, F29 is the next candidate.
- **F57(a)** (FuelResource key mismatch) is R3 inside a module carried by its
  R1 (b) half.

---

## Verdict table

Technique: FIX_POLICY §1 tier (1 data patch · 2 additive OnMsg · 3 registry
surgery · 4 chained wrapper · 4b global replacement · 5 full replacement).
Provenance: src-diff = found by reading source, no player report.

| Fix | Module | Technique | Provenance | Tier | Recommendation |
|-----|--------|-----------|------------|------|----------------|
| F01 | Fix_CaveInsNoDisasters | §1.3 | player-report | R2 (NoDisasters rule + underground) | keep |
| F02 | Fix_MeteorFrequency | §1.5 | src-diff | R1 | keep |
| F03 | Fix_UpgradeModifierLeak | §1.5 | src-diff | R1 (PT-02 by play) | keep |
| F03s | 90_SaveSanitizer (leak sweep) | §1.2/1.3 | src-diff | R2 (pre-fix saves) | keep |
| F04 | Fix_NightShiftWork | §1.5 | src-diff | R1 | keep |
| F05 | Fix_MilestoneCrash | §4b | src-diff | R2 (NoTerraforming/NoPolitics) | keep |
| F06 | Fix_CrystalMysteryHang | §1.2 | src-diff | R2 (Mystery 10) | keep |
| F07/F15 | Fix_WispRewards | §4b | src-diff | R2 (Mystery 11) | keep |
| F08 | Fix_TouristApplicants | §1.5 | src-diff | R2 (tourism opt-in) | keep |
| F09 | Fix_TouristSatisfaction | §1.5 | src-diff | R1 | keep |
| F11 | Fix_TrainPlatformWedge | §1.5 | src-diff | **U** (engine-side desync producer) | keep + observation |
| F12 | Fix_LowStorageWarning | §1.5 | src-diff | R1 (PT-07 by play) | keep |
| F13 | Fix_CommandCenterNumbers | §1.3 | src-diff | R1 (PT-08 by play) | keep |
| F14 | Fix_DomeOverviewHighlight | §1.5 | src-diff | R1 (PT-09 by play) | keep |
| F16 | Fix_MirrorSphereSite | §1.4 | src-diff | R2 (Mystery 6) | keep |
| F17 | Fix_DustSicknessDamage | §1.1 | src-diff | R2 (Dust in the Wind rule) | keep |
| F18 | Fix_IndependenceTerraforming | §1.1 | src-diff | R2 (independence arc) | keep |
| F19 | Fix_GraphConsumedCaption | §1.4 | src-diff | R1 (PT-43 by play) | keep |
| F20 | Fix_MoraleComfortTooltip | §1.4 | src-diff | R1 (PT-43 by play) | keep |
| F21 | Fix_TrainWaitTime | §1.5 | src-diff | R2 (trains; PT-43 by play) | keep |
| F22 | Fix_GridGlobalStorage | §4b | src-diff | R1 (hourly from sol 1) | keep |
| F23 | Fix_FounderTraitNotification | §1.2 | src-diff | R1 | keep |
| F25 | Fix_TechDescriptionBuilding | §1.1 | src-diff | R2 (pre-1.0.6 legacy save) | keep |
| F26 | Fix_BombardmentSpread | §1.5 | src-diff | R2 (Mystery 7) | keep |
| F27 | Fix_StorageRateModifiers | §1.4 | src-diff | **R3** (no shipped rate modifier) | keep (cheap) |
| F28 | Fix_ReplaceTechCount | §1.5 | src-diff | **R4** (zero callers in Src) | **DELETE candidate** |
| F29 | Fix_SequenceLatents | §1.5 | src-diff | **R3** (confirmed; defaults mask both) | keep (flag: §1.5 latent) |
| F30 | Fix_LakeEntombment | §1.4 | mixed | R1 (deterministic on lake build) | keep |
| F31 | Fix_AnomalyCaveInMap | §1.4 | src-diff | **R3** (trigger and precondition mutually exclusive) | keep (cheap) |
| F33 | Fix_SmallLandscapeSites | §1.5 | src-diff | R1 (min-brush dab) | keep |
| F34 | Fix_LandscapeUnitFilter | §1.5 | src-diff | R2 (boarding drone under mark) | keep |
| F35s | 90_SaveSanitizer (turbine buff) | §1.2/1.3 | mixed | R2 (legacy save, report-backed) | keep |
| F36 | Fix_UniversityOvertraining | §1.5 | player-report | R2 (ExtractorAI breakthrough) | keep |
| F37 | Fix_GhostFarmOxygen | §1.4+1.2 | src-diff | R2 (not-working-window salvage) | keep |
| F38 | Fix_DestroyedTunnels | §1.4+1.2 | src-diff | R2 (destroyed tunnel + save/load) | keep |
| F40 | Fix_DustSicknessBiorobots | §1.1 | src-diff | R2 (DustInTheWind + Positronic Brain) | keep |
| F41 | Fix_GeneForging | §4b | mixed | R2 (Futurist + NewHorizons storybit chain) | keep |
| F43 | Fix_LayoutTechLock | §1.4 | src-diff | **R3** (only tech-locked entry is prefab-handled) | keep (cheap) |
| F44 | Fix_TrackSalvageWipe | §1.5 | mixed | R2 (trains; PT-03 by play) | keep |
| F45 | Fix_BrokenTrackSalvage | §1.4 | mixed | R2 (trains + meteor hit) | keep |
| F46 | Fix_TrainCargoDumping | §1.5 | mixed | R2 (trains; PT-23 by play) | keep |
| F47 | Fix_TrackSalvageRefund | §1.5+1.4 | src-diff | R2 (trains; PT-45 by play) | keep |
| F49 | Fix_TrainMinors | §1.4 | mixed | (a) **R4** · (d) R2 play-proven · (c) **I — wontfix, guard removed** *(corrected by Challenge review)* | keep module on (d); (a) optional strip |
| F50 | Fix_RocketDroneChurn | §1.5 | mixed | R2 (auto-mode toggle; PT-04 by play) | keep |
| F51 | Fix_ShuttleTransportCache | §4b | player-report | R1 (PT-12 organic) | keep |
| F52 | Fix_VacuumWalks | §1.5 | player-report | R1 (PT-13 by play) | keep |
| F53 | Fix_ArrivalDeaths | §1.5 | mixed | R2 (situational landings) | keep |
| F54 | Fix_ShuttleHubOffAvailable | §4b | src-diff | R1 (PT-34 by play) | keep |
| F55 | Fix_DroneUnreachableForever | §1.5 | player-report | R1 | keep |
| F57 | Fix_DroneTransportMinors | §1.2+1.5 | src-diff | (b) R1 · (a) **R3** | keep; flag (a) §1.5-latent |
| F58 | Fix_StaleReservations | §1.4+1.2 | mixed | R2 (stalled shuttle pipeline; dev fixup proves drift) | keep |
| F59 | Fix_FreedHousingNotice | §1.4 | src-diff | R1 | keep |
| F60 | Fix_DomeFreeSpaceMismatch | §1.5 | src-diff | R1 | keep |
| F64 | Fix_TrainsToVoid | §1.4 | mixed | R2 (salvage a station with trains) | keep |
| F65 | Fix_TrackTunnelPowerBridge | §1.2+1.4 | src-diff | R2 (station at tunnel mouth; PT-40 by play) | keep |
| F66 | Fix_TrackConnectorPingPong | §1.5+1.4 | mixed | R2 (1-hex-gap placement; PT-41 by play) | keep |
| F67 | Fix_LanderEmptyLaunch | §1.4 | mixed | R2 (auto mode + empty threshold window; PT-16 by play) | keep |
| F68 | Fix_LanderCargoRatchet | §1.5 | mixed | R2 (auto export; PT-17 by play) | keep |
| F69 | Fix_LanderReturnFuel | §1.4 | mixed | R1 (every manual asteroid landing; PT-16 by play) | keep |
| F70 | Fix_PayloadTemplateRefill | §1.5 | mixed | R1 (every zeroed templated row; PT-31 by play) | keep |
| F71 | (inside Fix_LanderCargoRatchet) | §1.5 | src-diff | R2 (competing auto exports; PT-32 by play) | keep (inseparable from F68) |
| F72 | Fix_AsteroidLanderAvailable | §4b | mixed | R1 (CmdUnload window; PT-33 by play) | keep |
| F73 | Fix_ShelterReflex | §1.5+1.4 | mixed | R2 (asteroid habitation; PT-19 by play) | keep |
| F74 | Fix_RocketInteractGuard | §1.4 | mixed | R2 (storybit/mystery event rocket + player order) | keep |
| F75 | Fix_LastTransmissionStorage | §1.1 | src-diff | R2 (Martian-faction stage of politics) | keep |
| F77 | Fix_ExtenderFlapChurn | §1.4 | mixed | R2 (extenders + routine power/maintenance edges) | keep |
| F78 | Fix_MeteorStormWedge | §1.3 | player-report | R2 (storm + residual-meteor condition; wedge seen live twice) | keep |
| F81a | Fix_DisasterPredictionLeak | §1.2+1.3 | mixed | R1 (every completed storm; proven on the 194-sol save) | keep |
| F81b | Fix_RainsDeadlock | §1.5 | mixed | R2 (rain band + disaster collision) | keep + observation |

Legend: F03s/F35s = the two sanitizer passes in `90_SaveSanitizer.lua`.
F71 ships inside F68's replacement of the same function — not separately
deletable. PT citations marked "by play" were checked against
PLAYTEST_ARCHIVE/BUGS status notes: the state was reached by playing, not
manufactured. PTs that used console setup are called out in the detail blocks
(F01, F05, F29→n/a, F36, F41, F45): for those the reachability verdict rests
on the source chain, not the PT.

---

## Method notes carried out of the audit

- A `tested` status was never accepted as reachability proof by itself; each
  cited PT was checked for console manufacturing. Six PTs proved the fix but
  not the path (noted per fix); none of those changed a verdict past R2.
- Every R4 verdict names the exhaustive search that grounds it. A state
  producible only by console/debug injection was treated as evidence FOR R4
  (the PT-46 lesson).
- The stance throughout was argue-to-save; U was preferred over a doubtful R4
  (F11 is the one U).

## Per-fix detail

The blocks below are the full audit records, grouped as audited. R1 blocks are
included too — they carry the call-site enumerations and PT checks.

### F49(a) — instant-built track painted with the pipes palette (lead pass)

- Module: Code/Fix_TrainMinors.lua (the (a) third of a three-part bundle) |
  Technique: §1.4 chained post-wrapper on `TrackGridElement:GameInit` |
  Provenance: source-diff (palette-call comparison; never a player report)
- Defect: `place_track` (Tracks.lua:386-415) paints every element it creates
  with `GetPipesPalette()` (:385, :412) where every other track path uses
  `GetTracksPalette()`.
- Call sites / gating, enumerated:
  * The defective body is the **instant** placement closure inside
    `PlaceTrackLine`. It executes only when a clear hex has
    `place_construction_site == false` (Tracks.lua:440-442). That flag is
    `elements_require_construction or #rocks > 0 or #stockpiles > 0`
    (Tracks.lua:234) — with `elements_require_construction` true it is always
    true, and the construction-group branch always produces a site
    (Tracks.lua:431-437), so the instant path **cannot fire** when
    construction is required.
  * `PlaceTrackLine` has exactly one caller: the grid-construction mode
    dispatch (GridConstruction.lua:607 → :1852), which passes the
    controller's `grid_elements_require_construction`. The controller value
    is overwritten on every dialog open with the dialog's own
    (GridConstruction.lua:35); the track dialog defaults it **true**
    (TrackConstruction.lua:8).
  * All four shipped entries into track mode pass no override:
    `SetMode("track_grid", { template = "Track"})` — Data\XDef\BMMiddle.lua:153,
    Data\XDef\GameShortcuts.lua:1778, and their generated twins
    (Lua\XDef\BMMiddle.generated.lua:160, GameShortcuts.generated.lua:1908).
  * The other two `TrackGridElement:new` sites in Src never run the defective
    palette line: the repair/expand path (TrackElement.lua:762) is painted by
    the completed-construction path with the tracks palette
    (TrackElement.lua:791); station connector elements
    (TrainTransport.lua:132) are outside `place_track` entirely.
- Falsification search: there is **no `InstantTracks` const** — the Instant*
  family is Cables/Passages/Pipes only (Lua\__const.lua:1043-1056). The two
  instant-build techs modify InstantCables/InstantPipes only
  (Data\TechPreset.lua:478, :493); the one sponsor perk modifies
  InstantPassages only (Data\MissionSponsorPreset.lua:739); the build menu
  hardcodes `require_construction = true` for tracks (BuildMenu.lua:1938).
  `Cheats.lua` contains zero track references — no track cheat exists. No
  shipped map-setup or fixup code calls `PlaceTrackLine`.
- Corroboration: the 2026-07-30 PT-46 incident — the only way found to produce
  instant track was injecting
  `SetMode("track_grid", {grid_elements_require_construction = false})`, an
  entry path with no player-facing control, and the injection itself left
  orphan-track debris. A state producible only by injection is evidence for R4.
- Tier: **R4** — no path in the shipped game executes `place_track`.
- Recommendation: **keep the module** — the bundle's other two thirds are
  live ((c) connector-hex salvage click, (d) stale `max_vehicles` after
  partial salvage), and the (a) wrapper is a cheap additive post-wrapper that
  is a no-op for correctly-painted elements. Optionally strip the (a) wrapper
  on the next touch; there is no §1.5 liability here.
- Mitigation worth recording: even if the state ever occurred, changing the
  colony colour scheme repaints every `TrackGridElement` with the correct
  palette (ColonyColorScheme.lua:120-121) — the defect self-corrects.

## Tracks & trains (F11, F21, F44-F47, F64-F66)

### F11 — Train wedges at platform (`table.remove` misuse)
- Module: Code/Fix_TrainPlatformWedge.lua | Technique: §1.5 replacement | Provenance: source-diff — API-misuse (`table.remove` given a value, not a position) found by reading the guard; no player report cited in the entry
- Defect: `Colonist:ExitVehicle` stale-passenger guard (ColonistTransport.lua:541-546) — `table.remove(vehicle.units, self)` raises (bad argument: value for integer position), aborting the colonist's command thread before `DiscardTransportTicket`, so `Train:UnloadTrain`'s `while #self.units > remaining_passengers` (Train.lua:451-453) spins forever and the train blocks its platform permanently.
- Call sites: 1 in Src: Train.lua:447 (`colonist:SetCommand("ExitVehicle", self)` inside UnloadTrain's destructor) — live; runs for every passenger at every station arrival. The defective BRANCH is gated on the anomalous state "colonist listed in `train.units` but `holder ~= train` (or different map)".
- Precondition & player path: base-game train system (no tech gate — see F21 Notes), a passenger aboard, plus a stale-passenger desync. Every ordinary holder change syncs `units` (`Unit:SetHolderOnMap` → `Holder:OnExitHolder`, Unit.lua:702-717, Holder.lua:36-41), death is handled (`RemoveDeadFromTransport`, TrainDisasterHandling.lua:41-54, OnMsg.ColonistDied :117-119), so the state needs a path that bypasses `SetHolder`. Leading concrete candidate — the one the dev comment itself blames: expedition/lander crew loading gathers BUSY colonists, explicitly including passengers currently riding (`CargoTransporterNew:GatherAvailableColonists` busy-colonist fallback, CargoTransporterNew.lua:221-234 → `SetCommand("EnterTransporter")` :440), and `Unit:EnterTransporter` does an engine-side `TransferToMap` BEFORE `SetHolder` (Unit.lua:1202-1209) — whether that engine step strips the old holder's `units` entry is not auditable from Lua. The devs wrote this dedicated guard with a `TrainsLogging.warn`, which is itself evidence they observed the state.
- Searched: all `ExitVehicle` callers; `SetHolder`/`SetHolderOnMap`/`OnExitHolder` chain; every direct `.holder =` assignment in Lua (Passage.lua:1055, Colonist.lua:4305, Train.lua:390 — none can strand a colonist in `train.units`); `ExitHolderImmediately`/`KickFromBuilding`; `CargoTransporterNew` crew gather; death/crash paths (TrainDisasterHandling.lua); tunnel traversal (TrackTunnel.lua:40-80 — trains never change maps, `SetPos` only).
- Tier: U — the sole call site is unconditional in train play and the punishment is permanent, but the guard-firing state's producer bottoms out in engine-side `TransferToMap`, unverifiable from source alone; every Lua-visible path keeps `units` synced.
- Recommendation: keep + record observation: with a colonist mid-ride, launch a crew-carrying expedition/lander that must dip into busy colonists, then inspect `train.units` — a stale entry (or the shipped log line "not in train") settles it as R2.
- Notes: even if never reached, the replacement is byte-faithful except the one corrected call, so the keep-cost is ~zero against a wedged-line failure mode; the guard's raise means any single occurrence in a colony is permanent in vanilla.

### F21 — Train travel-time penalty includes station waiting
- Module: Code/Fix_TrainWaitTime.lua | Technique: §1.5 replacement | Provenance: source-diff — accounting audit of the `start_wait` lifecycle; no player report cited
- Defect: `Colonist:BoardVehicle` (ColonistTransport.lua:503-528) — never restamps `ticket.start_wait` (stamped at platform arrival, :493), so `ExitVehicle`'s `travel_time = GameTime() - ticket.start_wait` (:551) charges wait+ride as Comfort penalty (:555-557) and double-counts the wait into train/track spent-time stats (:568-569, the station already got it at :511).
- Call sites: 1 in Src: Train.lua:967 (`SetCommand("BoardVehicle", self)` in TransferCargo's boarding loop) — live, every boarding; the spend side is Train.lua:447 (ExitVehicle, every arrival). Both unconditional in passenger operation.
- Precondition & player path: build two stations + track near domes (base-game, Sol 1); colonists then ride automatically (migration/commute, e.g. `TryToEmigrateByTrain`, ColonistTransport.lua:633-639). Any nonzero platform wait — i.e. essentially every trip — mis-charges. PT-43 (BUGS.md:485) reached it by playing: a live migrant's 17h queue-inclusive trip, stats and Comfort verified end-to-end.
- Searched: BoardVehicle/ExitVehicle callers; start_wait writes (ColonistTransport.lua:493 only).
- Tier: R2 — hits every passenger trip once the player opts into the base-game train system; the Comfort half is mooted only after the optional LuxuriousTrains tech (stats half never mooted).
- Recommendation: keep — universal mis-accounting within train play, playtest-proven live.

### F44 — One-hex track salvage can delete the entire track
- Module: Code/Fix_TrackSalvageWipe.lua | Technique: §1.5 replacement (+ §1.2 LoadGame sweep) | Provenance: mixed — source-confirmed, "matches the long-standing Martian Express reports"
- Defect: `TrackGridElement:DemolishAndSplitTrack` (TrackElement.lua:448-530) — the deletion-zone search demands a pillared AND straight anchor (:481-486); curves are never straight, so the search runs off the array, and the short-remainder fallbacks (:505-507, :519-521) call `track_obj:OnDemolish()` — whole track plus `DestroyAssignedTrains` (Track.lua:248-252), instantly, no countdown.
- Call sites: 2 in Src: TrackElement.lua:445 (`TrackGridElement:Demolish` — reached by the infopanel Salvage button via ToggleDemolish :259-261, the demolish-tool click Construction.lua:2911, and the repair-site delegation :451-453; CheatDelete :263-265 is console-only) — live; Construction.lua:1574 (track erased under a newly placed station, `mass_delete=false` so the same partial branches run) — live.
- Precondition & player path: salvage one hex of any track that is curved near the click, shorter than ~6 elements, or clicked near an end — i.e. routine rail maintenance on any realistic layout (any non-straight drag produces curves). PT-03 (BUGS.md:1080-1129) exercised exactly these clicks by playing on a live colony (curve-ended and straight tracks, train surviving).
- Searched: all `DemolishAndSplitTrack`/`:Demolish(` callers; `IsTrackElementStraight` definition claim; mass-salvage tool path.
- Tier: R2 — any player who builds tracks and later salvages a piece of a curved or short run hits it; only the train-system opt-in gates it.
- Recommendation: keep — highest-damage fix in the group (deletes trains, a colony-counted resource).
- Notes: the fix's orphan/`track_obj == false` sub-branches and the LoadGame debris sweep repair states created by the fix's own earlier version (PT-03 FAIL), not shipped-game states — correct to keep, but their reachability is mod-legacy, not vanilla.

### F45 — Damaged tracks can't be salvaged at all
- Module: Code/Fix_BrokenTrackSalvage.lua | Technique: §1.4 wrapper (+ §1.2 LoadGame sweep) | Provenance: mixed — source-confirmed, "matching the 'can't salvage / undeletable track' reports"
- Defect: `TrackBase:BreakTrackElement` (Track.lua:618-659) — copies direction/q/r/station/pillared/connections/track_obj to the repair site (:629-635) but not `node_idx`, which stays `false`; every later salvage's `table.sort` comparator (TrackElement.lua:464) then raises on `false < number` before any deletion — the click silently does nothing, forever.
- Call sites: 1 direct in Src, via `BreakTracks` (Meteors.lua:599-613): BaseMeteor:HitTracks (Meteors.lua:638, :772 — every meteor impact near a completed track element) — live; CaveInRubble.lua:172 (underground cave-in rubble) — live; TrackElement.lua:437 `CheatBreakElement` and Track.lua:606 `CheatBreakTrack` — console-only, eliminated.
- Precondition & player path: a meteor strikes a track (meteors are a routine base-game disaster on every landing spot; threat varies but is never absent short of rule/coordinate extremes), or an underground cave-in hits an underground rail (needs UndergroundTrains tech). From then on the whole track — click, Ctrl+click, infopanel Salvage, the repair site itself — is unsalvageable.
- Searched: all `BreakTrackElement`/`BreakTracks`/`HitTracks` callers in Src; confirmed the params copy at Track.lua:626-635 omits node_idx.
- Tier: R2 — train system plus one meteor hit, which is a when-not-if event over a colony's life.
- Recommendation: keep — retroactive sweep also rescues saves already carrying the state.
- Notes: PT-03's broken-track step likely used an aimed meteor (PLAYTEST_HELP "aim a meteor at the mouse pointer", commit 3b58f25), so the PT proves the fix, not reachability — reachability stands on the Meteors.lua/CaveInRubble.lua call sites instead.

### F46 — Trains dump cargo at stations with the resource disabled
- Module: Code/Fix_TrainCargoDumping.lua | Technique: §1.5 replacement | Provenance: mixed — source-confirmed, "the resource ping-pong players see"
- Defect: `Train:UnloadAll` (Train.lua:783-803) — unloads everything the station has room for with no `IsResourceEnabled` check; disabling a resource only removes the demand request from `task_requests` (StorageDepot.lua:641-668), the request object still reports a target, so the dump proceeds and the planner immediately schedules the stock back out (`TransferCargo` forbidden-excess handling, Train.lua:868).
- Call sites: 2 in Src: Train.lua:843 (TransferCargo — every station stop) — live; Train.lua:988 (destructor before departure wait) — live. Both unconditional in cargo operation.
- Precondition & player path: train network hauling cargo, then the player flips a station's per-resource accept toggle off (standard station infopanel UI) while a train already carrying that resource is en route — or demolishes/reassigns mid-trip (loading paths already check `IsResourceEnabled`, :905-912, :930-939, so only mid-trip changes create the state). PT-23 (BUGS.md:1142-1159) reproduced both halves by playing on a live 5-station network.
- Searched: UnloadAll callers; SetAcceptResource UI path.
- Tier: R2 — train system plus one ordinary UI toggle at the wrong moment; a common logistics action.
- Recommendation: keep — playtest-proven live, and the two escape hatches prevent regression stalls.

### F47 — Track salvage refund ~1 group for whole track; 0 for partial
- Module: Code/Fix_TrackSalvageRefund.lua | Technique: §1.5 replacement + §1.4 wrapper | Provenance: source-diff — refund-math audit (construction-group stamping traced through ConstructionSite.lua:2469-2489)
- Defect: `TrackBase:GetRefundResources` (Track.lua:286-307) — reads the stamp of `self.elements[#self.elements]` only (:291), so every construction group (5 hexes each) before the last is unrefunded; and `DemolishAndSplitTrack` deletes with bare `DoneObject` (TrackElement.lua:513, :527, :537-538) so partial salvage refunds nothing (`Demolishable:GetRefundResources` is an empty stub, Demolishable.lua:160).
- Call sites: half A via the refund machinery — Demolishable.lua:58 (`ReturnResources` ← `TrackBase:OnDemolish` Track.lua:270-272, every whole-track salvage) live; Building.lua:977, :1384 and ipTrack.generated.lua:154 (refund display) live; MultiSelection.lua:566 live. Half B: the same TrackGridElement:Demolish entry points as F44 (TrackElement.lua:259-261, Construction.lua:2911) — live on every partial salvage.
- Precondition & player path: salvage any track longer than 5 hexes (short-refunded) or any part of a track (zero-refunded) — routine once the player builds rail. PT-45 (BUGS.md:1161) verified by playing: refund = stamped sections × 100 on live colony tracks, partial-salvage stockpiles observed.
- Searched: all GetRefundResources overrides/callers; the group-leader stamping path.
- Tier: R2 — every track salvage beyond a 5-hex toy track mis-refunds; only the train-system opt-in gates it.
- Recommendation: keep — pure economy correction, retroactive on existing saves (stamps already present).

### F64 — Demolishing a station vaporizes its trains ("trains go to void")
- Module: Code/Fix_TrainsToVoid.lua | Technique: §1.4 wrapper | Provenance: mixed — source-confirmed, "matches 'trains go to void' exactly" (player-report phrase)
- Defect: `OnMsg.BuildingDemolished` (Station.lua:163-171) — bare `DoneObject` on every train with `current_station == station`, fired synchronously from `Building:OnDemolish` (Building.lua:882) before `Station:Done`'s proper `DestroySilent` storing loop (Station.lua:145-149) can run; no prefab refund (only `Train:OnDemolish` refunds, Train.lua:205-209), and `current_station` stays the departure station all trip (Train.lua:164-166) so mid-transit trains vaporize too.
- Call sites: 1 in Src: the OnMsg handler, fired by Building.lua:882 from `Demolishable:DoDemolish` — live; the only producer is demolition of a Station, a standard player salvage (`Building:CanDemolish`, Building.lua:885-889 — stations are not indestructible).
- Precondition & player path: player salvages a train station while any train is docked there or mid-trip out of it — i.e. any rail-network rework in a colony that runs trains. Once the colony train counter hits 0 the "Send out Train" button is dead everywhere (Station.lua:653-660) until new trains are constructed for Metals+Electronics.
- Searched: BuildingDemolished emitters (Building.lua:882 sole gameplay source); Station:Done loop ordering; Train:OnDemolish refund path.
- Tier: R2 — train system plus one ordinary salvage of a station; near-inevitable over a colony's life since players rearrange networks.
- Recommendation: keep — silent permanent loss of a colony-counted resource, matched to a named community report.

### F65 — Station attached to a train tunnel never bridges the power grid
- Module: Code/Fix_TrackTunnelPowerBridge.lua | Technique: §1.2 OnMsg (+ §1.4 wrapper on TrackBase:Done) | Provenance: source-diff — promise-vs-code audit of the tunnel description (Data\BuildingTemplate\TrackTunnel.lua:17, same text on UniversalTunnel.lua:17)
- Defect: `OnMsg.StationsConnected` (Track.lua:668-680) — skips `ConnectToGrids()` for ≤2-element tracks on the premise the buildings are "already adjacent", but a 2-element track IS the two buildings' connector elements, each on a hex outside its building (OrientConnectorElements, TrainTransport.lua:91-100), so the buildings sit two hexes apart, track elements carry no power (`TrackBase.ApplyToGrids = empty_func`, Track.lua:663), and the promised grid bridge never forms.
- Call sites: 1 in Src: the shipped OnMsg handler itself (message fired from TryConnectStations) — live; the defective else-branch (:674-676) executes exactly when `#track.elements <= 2`.
- Precondition & player path: build a station snugged directly against a Universal Tunnel entrance (UniversalTunnel: Infrastructure build category, no tech gate, UniversalTunnel.lua:4,18 — base-game) or against another station — the auto-created connector elements form the 2-element track. PT-40 (BUGS.md:2222-2232) built exactly this by playing on a live colony and demonstrated the shipped decline (far grid dark until the fix bridged it), including the salvage-split and reload legs.
- Searched: StationsConnected emitters; GetSupplyTunnelElement (Track.lua:567-574); tunnel unlock gating (no BuildingTechRequirements entry).
- Tier: R2 — train system plus the natural "put the station right at the tunnel mouth" placement, which the tunnel's own description invites.
- Recommendation: keep — playtest-proven live in the shipped geometry; the runtime different-grids test makes false positives impossible.

### F66 — Station↔tunnel connector hex ping-pong
- Module: Code/Fix_TrackConnectorPingPong.lua | Technique: §1.5 replacement (+ §1.4 post-wrap on Done) | Provenance: mixed — source-confirmed, matches the "tracks won't connect to stations" report with the known ≥2-hex-gap community workaround
- Defect: `TrackConnectedObjBase:CreateConnectorElements` (TrainTransport.lua:114-154) — destroys any element on its connector hex even when a live building owns it (:126-130; the assert at :127 states the invariant but cannot unwind in this engine), and the victim's `TrackGridElement:Done` schedules the owner's rebuild (TrackElement.lua:193-199), which steals the hex back — an endless loop leaving one building permanently connectorless, so no route forms.
- Call sites: 5 in Src: TrainTransport.lua:11 (GameInit — every station/tunnel placement) live, the trigger; TrackElement.lua:196 (element-Done rebuild thread) live — the loop's return leg; Track.lua:182 (station element destroyed during track demolish) live; TrainTransport.lua:158 (OnMsg.TrackDemolished global rebuild) live; Station.lua:1352 (SavegameFixups, `force`) live on load.
- Precondition & player path: place a station and a tunnel (or two stations) one hex apart so their Trackconnector spots resolve to the same hex — plain construction placement, nothing prevents it. PT-41 (BUGS.md:2234) built the shared-hex geometry by playing and verified stability plus the survivor reclaiming the hex after demolition.
- Searched: all CreateConnectorElements callers; TrackConnectedObjBase:Done special case (TrainTransport.lua:24-27); the rebuild triggers enumerated for the recovery gap.
- Tier: R2 — train system plus a 1-hex-gap placement, common enough that the community documented the gap workaround.
- Recommendation: keep — converts an infinite fight into the workaround's outcome, and the reclaim wrapper closes the shipped recovery gap.
- Notes: group-wide finding, applies to all nine fixes: the train system is base-game with no unlock — StationSmall (Data\BuildingTemplate\StationSmall.lua), Track, and UniversalTunnel have no BuildingTechRequirements entries (default shown+enabled, BuildMenu.lua:332-356; StationSmall's `require_prefab` is inert because its resupply cargo item is locked, Cargo.lua:1568-1577, making the flag evaluate false at BuildMenu.lua:700); only StationBig needs the BigStations tech (Station.lua:1317) and only underground rail needs UndergroundTrains. So "R2" for this group means exactly one condition: the player chooses to build the (optional but always-offered) train network.

## Rockets & landers (F08, F50, F67-F72, F74)

### F08 — Tourist star-rating applicant bonus inverted
- Module: Code/Fix_TouristApplicants.lua | Technique: §1.5 replacement | Provenance: source-diff — inverted `>` found by reading the monotonic rewards table against the codebase idiom
- Defect: HolidayRating:RewardApplicants (HolidayRating.lua:77) — `Random(0,100) > bonus_chance` grants the bonus with probability ~(100−chance), so higher star ratings yield fewer bonus applicants.
- Call sites: 1 in Src: HolidayRating.lua:21 (ApplyRewards, per boarded tourist) — live. ApplyRewards itself: UniversalRocket.lua:2014 via ApplyTouristRewards (:2011), invoked from the "earth" flight policy OnCmdFlyToLocationEnd (Data\FlightPolicyDef.lua:283) on every Earth arrival — live; RocketBase.lua:855→:818 and RocketExpedition.lua:569 — legacy rocket family, superseded in Relaunched, but the patch sits on the shared HolidayRating table so they are covered regardless. (The `RewardApplicants` EffectDef class in ClassDef-Effects is an unrelated global — not a call site.)
- Precondition & player path: colony has tourists and any rocket flies them home. One real gate: the passenger-manifest filter EXCLUDES the Tourist trait by default (recorded engine fact, docs\archive\SESSION_LOG.md:1293-1295), so the player must opt into tourism; after that every departure rolls the inverted chance. PT-06 (BUGS.md:260) reached it by playing: 5★ +23 applicants vs tanked ≤2★ +7.
- Searched: grepped `RewardApplicants` and `HolidayRating|ApplyTouristRewards` across Src; read HolidayRating.lua:1-95 and the earth-policy departure path.
- Tier: R2 — fires on every tourist departure, but tourists only exist if the player opts into the tourism mechanic (default manifest filter excludes them).
- Recommendation: keep — a whole revenue mechanic scales backwards for every tourism player.

### F50 — Auto-rockets kick approaching drones to Idle every hour
- Module: Code/Fix_RocketDroneChurn.lua | Technique: §1.5 replacement | Provenance: mixed — matches the "drones ignore rocket cargo" player report; mechanism established by source reading
- Defect: CargoTransporterNew:UpdateCargoResourceRequests (CargoTransporterNew.lua:1238-1271) — unconditional Disconnect/ConnectFromCommandCenters brackets (:1239-1241, :1268-1270); each disconnect runs DroneControl:OnRemoveBuilding (DroneControl.lua:720-729), Idling every drone en route to the rocket.
- Call sites: 20 in Src (excluding the distinct legacy `CargoTransporter:UpdateCargoResourceRequests(resources)`, Buildings\CargoTransporter.lua:1016, which RocketBase.lua:609 and LanderRocket.lua:794/:1304/:1354 call — eliminated, different function on the legacy class). Live groups: (a) the churn chain — HourlyUpdate (UniversalRocket.lua:1357-1370, :1364) → CreateAutoCargoRequest → SetCargoRequest (CargoTransporterNew.lua:1285-1303, :1302) — hourly while a player auto-mode rocket is landed (special-automode rockets excluded at :1727 via IsSpecialAutomode :1719-1724); (b) one-shot sites, all live but non-repeating: UniversalRocket.lua:494 (CmdUnload, every landing), :672 (SetFlightData), :1345 (auto-mode off), :1660 (OnModifiableValueChanged), :2128 (AddCargo), :1685 (delegating override — reads the class table at call time, so the patch covers it); (c) RocketCompatibility.lua:238/:346/:437/:552/:654/:779/:905 — one-shot legacy-save conversion.
- Precondition & player path: press the base-UI "Automated Mode" button on any Universal rocket (ToggleAutoMode from_ui, UniversalRocket.lua:1352-1355; infopanel button AutoMode.lua:24-32) and leave it landed with a cargo request — every drone trip longer than one game hour then never completes. PT-04 (BUGS.md:1394) reached it by playing.
- Searched: grepped `UpdateCargoResourceRequests` tree-wide; verified the shipped body, SetCargoRequest, HourlyUpdate, IsSpecialAutomode, and OnRemoveBuilding.
- Tier: R2 — needs only the Automated Mode toggle (one click, base Relaunched feature); within auto-mode play it is unconditional and hits every hour.
- Recommendation: keep — the defect makes a headline feature (automated cargo rockets) silently unusable at any drone distance over an hour.

### F67 — Auto-lander launches empty and ping-pongs
- Module: Code/Fix_LanderEmptyLaunch.lua | Technique: §1.4 wrapper | Provenance: mixed — "ping-pongs between Mars and the asteroid" player report, branch analysis from source
- Defect: UniversalRocketBase:IsCargoReady (UniversalRocket.lua:455-472) — final `return cargo_status == "ready"` (:471) is trivially true when the hourly auto request came out empty, and the "wait for cargo" state only yields the non-blocking "waiting_cargo" issue (GetLaunchIssue :883-885), so a refuelled auto rocket departs with nothing aboard.
- Call sites: 2 in Src: UniversalRocket.lua:441 (CmdLoad wait loop) — live, the defect path; Data\FlightPolicyDef.lua:705 (rival policy OnCmdUnloadEnd) — eliminated for the defective branch: it runs only for `g_RocketTypes.TradePad` rockets (:704), which are IsSpecialAutomode (UniversalRocket.lua:1719-1724), so the player-automode empty-request state never applies (and the fix's IsPlayerControlled/IsSpecialAutomode guards keep the wrapper inert there).
- Precondition & player path: enable Automated Mode on a rocket/lander with thresholds that currently produce an empty request — routine on any fresh asteroid auto-mining run (extractors haven't reached the GET-WHEN-ABOVE threshold yet) or any Mars-side rule set with nothing above/below threshold. PT-16 (BUGS.md:2291-2313) reached it BY PLAYING: live colony, GET rule set in the UI, ~20 hourly empty recomputes held closed, forced departure after 1 sol as designed.
- Searched: grepped `IsCargoReady` tree-wide; read CmdLoad, GetLaunchIssue :875-886, CheckAutoDepart :1768-1775, IsSpecialAutomode/IsPlayerControlled.
- Tier: R2 — auto mode plus an unmet threshold window; the window occurs naturally at the start of essentially every asteroid auto-mining cycle (asteroid content is Below & Beyond, shipped inside Relaunched).
- Recommendation: keep — ~70 fuel per phantom round trip, on a state every auto-lander passes through.

### F68 — Hourly auto-request ratchet unloads the lander's own cargo
- Module: Code/Fix_LanderCargoRatchet.lua (shared with F71) | Technique: §1.5 replacement | Provenance: mixed — "loads exotics, dumps them back, leaves with junk" player report; mechanism sharpened by PT-17 live forensics
- Defect: UniversalRocketBase:CreateAutoCargoRequest (UniversalRocket.lua:1727-1766, compare at ~:1742-1755) — hourly recompute can set `requested` below what is already aboard, flipping GetCargoResourcesStatus (CargoTransporterNew.lua:1124-1141) to "unloading" so drones haul the just-loaded cargo back out.
- Call sites: 6 in Src for the patched method: UniversalRocket.lua:433 (CmdLoad, auto branch) — live; :1364 (HourlyUpdate) — live, the hourly ratchet; Data\FlightPolicyDef.lua:316 (earth policy OnCmdFlyToLocationEnd) — live for automated Earth trade rockets. LanderRocket.lua:680/:887/:1061 — eliminated: they dispatch to the legacy LanderRocketBase's own override (:639), and the legacy lander class is unreachable in Relaunched (locked at NewGame LanderRocket.lua:1129-1132, only UniversalLanderRocketBuilding ever unlocked, Asteroids.lua:404-409; legacy saves converted, RocketCompatibility.lua:627-637).
- Precondition & player path: automated export leg (asteroid→Mars or Mars→Earth) with drones actively ferrying cargo while stock replenishes. PT-17's live forensics (BUGS.md:2324-2365) proved GetTotalCargoAvailable already counts the landed rocket's hold, so on the clean path request tracks aboard+surplus; the live flip mechanism is bookkeeping lag — units in a drone's hands are in neither the ground total nor the hold (GetTotalCargoAvailable → city resource overview, Cargo.lua:72-75) — plus any path where the hold is not counted. State reached BY PLAYING (Sphinx #2 re-run, extractors replenishing mid-load; the console tap was observation-only).
- Searched: grepped `CreateAutoCargoRequest` tree-wide; read HourlyUpdate, SetCargoRequest, GetTotalCargoAvailable, the earth policy block, and the legacy-lander lock evidence.
- Tier: R2 — automated export with concurrent hauling/replenishment, an ordinary state of auto-mode play; the player report and the PT both put it in real colonies.
- Recommendation: keep — the anti-churn floor is what stops loaded landers from self-emptying; the PT-verified repair is sound.
- Notes: the fix header and BUGS entry already record the v1 double-count repair; nothing stale found.

### F69 — Manual landing dumps the return fuel
- Module: Code/Fix_LanderReturnFuel.lua | Technique: §1.4 wrapper | Provenance: mixed — "no fuel, no drones, can't send another lander" player report; root cause from source
- Defect: state producer UniversalRocketBase:CmdLand (UniversalRocket.lua:414) clears `arrival_loc` in manual mode; UniversalRocketBase:GetFuelResourceRequest (:1639-1642) then short-circuits to 0, so CmdUnload (:486-494) posts the asteroid policy's reserved return ration (FlightPolicyDef.lua:208-211 returns `2*amount, amount`; ConsumeFuel :1664-1673 burns only the difference) as excess cargo.
- Call sites: ~25 in Src for GetFuelResourceRequest — grouped: the harm-bearing consumers are CargoTransporterNew.lua:1130 (GetCargoResourcesStatus → "unloading" verdict on unrequested fuel), :1250/:1506/:1558 (request/excess arithmetic) and ConsumeFuel :1667 — all live for any landed rocket; the remaining sites (City.lua:363, UniversalRocket.lua:1625/:1629/:1676/:1687-1690/:2037/:2053/:2287/:2315/:2475/:2604, FlightPolicyDef.lua:353) read the same value and are live but benign. The defective 0-return arises only in the no-arrival_loc state; the wrapper additionally narrows to LanderRocket type on an asteroid, so no other caller's behavior changes.
- Precondition & player path: fly a lander to an asteroid in MANUAL mode (the default state of a new lander — auto must be switched on) and land. Every manual asteroid landing produces the state; with no drones/fuel production on the rock it is a permanent stranding. Lander unlock is ordinary research (AdvancedPassengerModule + MicroGLanders, Asteroids.lua:404-409). PT-16 (BUGS.md:2375-2389) reached it BY PLAYING: manual landing on drone-less Kayra AL10; vanilla posts the fuel as excess, fix held "Return trip fuel 15/15".
- Searched: grepped `GetFuelResourceRequest` tree-wide; read CmdLand, CmdUnload, ConsumeFuel, the asteroid policy.
- Tier: R1 — every manual asteroid landing hits the state; asteroid landers are mainline content of Below & Beyond as shipped inside Relaunched, gated only by normal tech progression.
- Recommendation: keep — highest-severity outcome in the group (permanent stranding) on the default flight mode.

### F70 — Edit Payload silently refills from the policy template
- Module: Code/Fix_PayloadTemplateRefill.lua | Technique: §1.5 replacement (plus §1.4 pre-wrapper on Apply) | Provenance: mixed — "it loads what it wants" player report; intent evidence from the legacy dialog's guard
- Defect: CargoRequestNew:RetrieveRequests (CargoRequestNew.lua:179-221) — every row whose stored request is 0 is refilled from the flight policy's CargoTemplate (file-local resolve at :166-177, suppressed only during CmdLoad), and CmdUnload (UniversalRocket.lua:486-494) re-zeroes every request on each landing.
- Call sites: 1 in Src: CargoRequestNew.lua:117 (Init — every dialog open) — live; the dialog is what UniversalRocketBase opens for Edit Payload (UniversalRocket.lua:2232 per BUGS entry). CargoRequest.lua:114/:238 and LanderRocketCargoRequest.lua:94 are different classes' own methods — not call sites of the patched one (the legacy lander copy is unreachable, proven three ways in BUGS.md:2414-2431).
- Precondition & player path: open Edit Payload in manual mode, zero or lower a templated row, reopen the dialog (or land once and reopen). Templates exist for ALL THREE player destinations — arrival=asteroid (5 Drones/20 Metals/5 Polymers/5 MachineParts/5 Electronics/3 prefabs, FlightPolicyDef.lua:92-131), arrival=earth (PreciousMinerals+PreciousMetals 1000 "available", :220-231), arrival=our_colony (:378-388) — and GetFlightPolicy keys on arrival type (ClassDef-Default.generated.lua:99-101), so a Mars-only export player hits it too. PT-31 (BUGS.md:2391-2399) reached it BY PLAYING: zeroed Metals resurrected in vanilla, held at 0 with the fix across a full round trip.
- Searched: grepped `RetrieveRequests` and `CargoTemplate` tree-wide; read the dialog Init path, resolve_loc_cargo_template, GetFlightPolicy, all three templates.
- Tier: R1 — every manual payload edit that empties a templated row, on every route, with re-zeroing every landing; no special content required beyond flying rockets.
- Recommendation: keep — persistent override of an explicit player instruction, on the most-used dialog in rocket play.

### F71 — Auto-export allocates capacity alphabetically
- Module: Code/Fix_LanderCargoRatchet.lua (folded into the F68 replacement of the same function — two replacements of one method cannot coexist; Opt_ClassicRockets.lua mentions F71 only in a comment) | Technique: §1.5 replacement (shared) | Provenance: source-diff — `sorted_pairs` order read against the policies' own value-descending lists
- Defect: UniversalRocketBase:CreateAutoCargoRequest (UniversalRocket.lua:1727-1766, loop ~:1736-1758) — hands the shared weight budget out in `sorted_pairs` (alphabetical) order, so bulk (Concrete, Metals, WasteRock is a legal asteroid export, FlightPolicyDef.lua:393/:401) can consume the hold before PreciousMinerals/PreciousMetals are considered, and the 1-sol forced departure (:1401, CheckAutoDepart :1773-1775) ships whatever loaded first.
- Call sites: same 6 as F68 (same function): UniversalRocket.lua:433 and :1364 live, FlightPolicyDef.lua:316 live for Earth trade; LanderRocket.lua:680/:887/:1061 eliminated (legacy override :639, class unreachable).
- Precondition & player path: automated export leg with two or more resources above their thresholds competing for the 80,000 kg hold — e.g. an asteroid producing both WasteRock/Concrete-class bulk and exotic minerals with both export rules set. PT-32 (BUGS.md:2435) reached it BY PLAYING: two-export leg allocated PreciousMetals first, Concrete squeezed, both delivered; four-class order probe-verified in isolation.
- Searched: grepped `F71` in Code\ (only Fix_LanderCargoRatchet.lua implements it); grepped `GetAutoModeAllowedResources`/`sorted_pairs` context in FlightPolicyDef; same call-site sweep as F68.
- Tier: R2 — automated export with competing resources, a routine configuration of asteroid auto-mining (B&B content shipped in Relaunched); harmless when only one resource is exportable.
- Recommendation: keep — shares its module and function with F68; deleting it separately is not even possible without re-implementing F68's replacement.

### F72 — "No available Asteroid Landers" with a lander on the pad
- Module: Code/Fix_AsteroidLanderAvailable.lua | Technique: §1.4b wrapper (chained replacement of a global function) | Provenance: mixed — the popup is the player-facing report; the gate/list disagreement found in source
- Defect: PlanetaryAsteroidVisitPossible (PlanetaryView.lua:433-444) — additionally demands `command == "CmdWaitOrder"` (:436), while the picker it gates, LandingSiteObject:GetRocketsForExpedition (PlanetUI.lua:1623-1635), never looks at command — so a lander in CmdUnload or CmdWaitMaintenance is offered by the list but refused by the gate (PromptNoAvailableAsteroidLanders, PlanetaryView.lua:455-463).
- Call sites: 1 in Src: Lua\XDef\PlanetaryViewAsteroidResources.generated.lua:37 (the VISIT ASTEROID action; Data\XDef\PlanetaryViewAsteroidResources.lua:34 is the same site's source form) — live.
- Precondition & player path: player's lander returns from an asteroid and sits in CmdUnload (as long as drones need — indefinitely with no drones or full depots) or waits for maintenance parts; player opens Planetary View, picks an asteroid, clicks VISIT ASTEROID → wrongly told no landers are available. With a single lander (the normal early-asteroid fleet) the gate has no other rocket to pass on. PT-33 (BUGS.md:2502-2514) reached both trigger states by playing (spare lander removed only for isolation).
- Searched: grepped `PlanetaryAsteroidVisitPossible` tree-wide; read the gate, the list builder, and the XDef action.
- Tier: R1 — the CmdUnload window follows every return trip, and clicking VISIT ASTEROID inside it is the natural "send it out again" action; asteroid content ships in the Relaunched box.
- Recommendation: keep — pure false refusal of an available unit, repaired permissive-only.

### F74 — RC Transports can be ordered onto trade / refugee rockets
- Module: Code/Fix_RocketInteractGuard.lua | Technique: §1.4 pre-wrapper (×2, gate + action) | Provenance: mixed — found by source screening (F56 wave-4), matches the RESEARCH.md "rockets glitch permanently if refilled from RC Transport" report
- Defect: RCTransport:CanInteractWithObject (RCTransport.lua:341) — the refusal names only `TradeRocketBase`/`RefugeeRocketBase`, dead ends in Relaunched: event rockets are UniversalTradeRocket/UniversalRefugeeRocket with `__parents = { "UniversalRocketBase" }` (BuildingTemplate\UniversalTradeRocket.generated.lua:4-5), and UniversalRocketBase is not a RocketBase (UniversalRocket.lua:28-41, verified) — so the guard never matches and the load/unload cursor accepts event rockets.
- Call sites: dispatch into the guarded method whenever an RC Transport is the selected/controlled unit — UnitControl.lua:470/:480/:483 via UnitController:CanInteractWithObject (:635-646, cursor gating) and :401 via :649-653 (act on stored target); TransportRouteInteractionHandler.lua:50; MultiSelection.lua:342-344/:375-379; static class-table calls RCHarvester.lua:127/:139, RCConstructorBase.lua:353/:372 (RCTerraformer via RCConstructorBase:237/:242). All live; all funnel through the wrapped class fields.
- Precondition & player path: a UniversalTradeRocket/UniversalRefugeeRocket landed at the colony. Exhaustive spawn list (grepped both class names tree-wide): storybit effects CallTradeRocket/CallRefugeeRocket (ClassDef-Effects.generated.lua:154/:3134) used by the TheDoorToSummer refuel storybit family (6 variants) and ExportWasteRock_SplintersOfMars; sequence actions SA_CallTradeRocketWithCargo/SA_CallRefugeeRocket (SA_Gameplay.lua:2788/:2929) used by mystery scenarios Data\Scenario\Mystery 7/8/9; legacy-save conversion (RocketCompatibility.lua:522/:964/:1050). These rockets sit landed for sols (waiting for fuel or waste rock), and pushing cargo at them with an RC Transport is a plausible deliberate act — the SplintersOfMars offer literally asks for waste rock. PT-39 reached the state in a real save (landed trade rocket, refused by cursor and route — PLAYTEST_ARCHIVE.md:923-967).
- Searched: grepped `CanInteractWithObject|InteractWithObject` in Lua; grepped `UniversalTradeRocket|UniversalRefugeeRocket` and `CallTradeRocket|CallRefugeeRocket` tree-wide; read RivalColonies.lua:237-255 and PopupNotificationPreset-Default.lua:28-57 to test the rival-colony hypothesis.
- Tier: R2 — needs a base-game random event (storybit or mystery) to land the rocket plus a deliberate player order; both halves are genuine ordinary-play occurrences.
- Recommendation: keep — restores a shipped safety rule the class rename silently killed; five sibling tests in the same file prove the intent.
- Notes: rival-colony trade-pad and foreign-aid rockets are plain class "UniversalRocket" (RivalColonies.lua:242-247; PopupNotificationPreset-Default.lua:42-46), so neither the shipped guard nor F74 blocks them — PT-39's setup text ("rival-colony trade offer") conflates the families, and the PT's refused rocket must in fact have been a storybit/mystery UniversalTradeRocket or no refusal would have occurred. If the RESEARCH.md report's "rival colony rockets" meant trade-pad rockets, that surface is untouched by F74 (possibly by design parity — the pre-Relaunched guard never covered a mechanic that didn't exist). Worth a line on the F74 entry.

## Colonists, housing & transport (F04, F09, F36, F51-F54, F58-F60, F73)

### F04 — Night-shift colonists never return to work after midnight
- Module: Code/Fix_NightShiftWork.lua | Technique: §1.5 replacement | Provenance: source-diff — no-wrap window proven against the codebase's own `% 24` idiom (IsDarkHour)
- Defect: Colonist:ShouldLeaveForWork (Colonist.lua:1758-1768) — shift-3 window evaluates `hour >= 21 and hour <= 25` on a 0-23 clock, so the 0:00-1:59 catch-up hours are unreachable.
- Call sites: 1 in Src: Colonist.lua:1911 (inside Colonist:Idle) — live; this is the only gate that ever sends an idle colonist to work, executed by every idle employed colonist every Idle pass.
- Precondition & player path: a colonist on workshift 3 who is not at work when the clock passes midnight. Shift 3 is open by default on every workplace (`closed_workplaces` initialises empty, Workplace.lua:15/35) and colonists are auto-distributed across shifts from the first Extractor/factory; being busy at 22:00-23:59 (meal, rest, medical visit, fresh arrival) is routine Idle-interrupt behaviour. No special content needed.
- Searched: Workplace.lua shift-close defaults (only player/`AutoAdjustWorkplaces` calls CloseShift); grep confirmed no second caller of ShouldLeaveForWork.
- Tier: R1 — every colony staffs night shifts by default and mid-shift interruptions are constant, so shift-3 workers silently skip half-shifts in ordinary play.
- Recommendation: keep — cheap replacement of a 10-line method, repairs a universal silent understaffing.

### F09 — Tourist Satisfaction drifts down (asymmetric threshold crossings)
- Module: Code/Fix_TouristSatisfaction.lua | Technique: §1.5 replacement | Provenance: source-diff — up-crossings exclusive vs down-crossings cumulative, visible as 2-red-per-green in the satisfaction log
- Defect: Colonist:UpdateSatisfaction (Colonist.lua:4006-4032) — an upward jump across two thresholds pays only the top award while the matching fall charges every threshold, so satisfaction is path-dependent and ratchets down.
- Call sites: 4 in Src, all live: Colonist.lua:3814 (health), :3841 (sanity), :3859 (comfort), :3982 (morale) — every stat setter calls it; the body self-gates on `self.traits.Tourist` (verified at :4007).
- Precondition & player path: at least one Tourist in the colony. Tourists are a first-class passenger/cargo class (Cargo.lua:79, CargoTransporter.lua:153, ApplicantsPool.lua:125) feeding the Holiday-rating payout system (HolidayRating.lua:18,63-67) — a core, UI-promoted income loop. Two-tier stat jumps are routine: service visits set Comfort directly; StressedOut recovery restores +50 Sanity in one step (StatusEffects.lua:264).
- Searched: verified the shipped body at Colonist.lua:4006-4032; grep for Tourist production paths (ApplicantsPool, CargoTransporter, HolidayRating).
- Tier: R1 — fires on every stat change of every tourist; only a colony that never flies a single tourist avoids it, and tourism is a headline Relaunched system.
- Recommendation: keep — every holiday payout in a tourism colony is quietly depressed without it.

### F36 — Universities overtrain geologists after Extractor AI
- Module: Code/Fix_UniversityOvertraining.lua | Technique: §1.5 replacement | Provenance: player-report — "universities train geologists after Extractor AI", behaviour-confirmed per BUGS heading
- Defect: City:GetNeededSpecialist (City.lua:561-593) — demand tally never asks whether a workplace is automated, so `automation > 0` extractors keep contributing 4 geologists/shift forever.
- Call sites: 4 in Src (excluding Colony's own delegating definition at Colony.lua:612): Colony.lua:617 (MainCity) and :620 (Underground city) — live, aggregation path; MartianUniversity.lua:77 (CanTrain "train as needed") — live with that policy; MartianUniversity.lua:109 (infopanel needed-list) — live whenever the panel is read. Colony.lua:631 (GetMostNeededSpecialist → auto-specialisation on graduation, MartianUniversity.lua:27) consumes the aggregate.
- Precondition & player path: (1) draw and research the ExtractorAI breakthrough — shipped in the Breakthroughs deck (TechPreset.lua:1050-1083, `group = "Breakthroughs"`), obtainable via anomalies/Omega telescope in any game; (2) have Metals/Precious Metals Extractors built and `ui_working`; (3) run a Martian University on "auto" or "train as needed" (or just read its infopanel). All ordinary mid-game play.
- Searched: TechPreset.lua ExtractorAI entry (only shipped source of `automation` on the labels — grepped `automation` effects); MartianUniversity.lua:16-114 for the consuming policies.
- Tier: R2 — needs one specific breakthrough plus common buildings; a genuine, dev-authored game state, just not present in every campaign.
- Recommendation: keep — whenever the breakthrough lands, every auto university misallocates graduates indefinitely.
- Notes: PT-24 granted the breakthrough by console (`UIColony:SetTechResearched("ExtractorAI")`), so the playtest proves the fix, not the player path; the player path rests on the breakthrough deck, which is solid.

### F51 — Transport-mode cache never sees new shuttles
- Module: Code/Fix_ShuttleTransportCache.lua | Technique: §1.4b global replacement | Provenance: player-report — "homeless despite free housing", "seniors never move to the retirement dome"
- Defect: FindTransportationModeToCommunity (Colonist.lua:2504-2537) — memoises per (community,pos) including negative verdicts, but `shuttles_available` is not in the key and no shuttle-hub event flushes the cache.
- Call sites: 4 in Src (excluding the definition and the `_BeforeTrains` sibling): Colonist.lua:2591 (forced-dome check, passes nil) — live; Colonist.lua:2662 (FindEmigrationDome, passes fresh `IsLRTransportAvailable`) — live, the main victim; SupplyRocket.lua:68 and UniversalRocket.lua:1901 (colonists leaving Mars, pass false) — live, and cross-contaminate the same keyed entries with a different flag.
- Precondition & player path: found a second dome beyond walking range before owning a working Shuttle Hub (the standard expansion order), let one emigration evaluation cache `mode=false`, then build/fuel a hub. PT-12 confirmed the negative verdicts had cached organically on the live three-dome playtest colony before the hub existed.
- Searched: cache flush triggers (Colonist.lua:2480-2488 — TrainRoutesRebuilt/DomesConnected/DomesDisconnected only; elevator/station validation snapshot inside the function itself); no ConstructionComplete flush exists.
- Tier: R1 — the dome-before-hub ordering is how nearly every colony grows, and the poisoned verdict then persists for the rest of the game.
- Recommendation: keep — flagship fix; repairs a permanent, invisible colony-logistics failure.
- Notes: PT-12's cheats (`CheatCompleteAllConstructions`/`CheatFillAllStorages`) only accelerated hub construction/fuelling; the defective precondition itself formed by playing, so reachability is effectively play-proven.

### F52 — Colonists walk ≤400m in vacuum past existing passages
- Module: Code/Fix_VacuumWalks.lua | Technique: §1.5 replacement | Provenance: player-report — the original, community-known long-walk suffocation bug
- Defect: Colonist:TryToEmigrateToDome (Colonist.lua:1546-1592) — in non-breathable atmosphere `min_dist` is the same 400m cap that defines walk mode, so `transport_mode_dist > min_dist` can never pass (:1560-1561) and no passage path is ever looked up.
- Call sites: 1 in Src: Colonist.lua:1614 (Colonist:TryToEmigrate) — live; runs whenever emigration selects mode "walk", i.e. any dome pair within 400m.
- Precondition & player path: two domes within 400m joined by a passage on a non-breathable map — Mars is non-breathable from sol 1 until deep terraforming, and adjacent passage-linked domes are the default layout. Any colonist re-homing between them (retirement, work, housing pressure) takes the surface walk. PT-13 reached it by playing: the colonist demonstrably used the passage post-fix and resumed the surface walk when the passage was destroyed.
- Searched: verified shipped body at Colonist.lua:1555-1575; single caller confirmed by grep.
- Tier: R1 — the defective branch is the default state of every pre-terraforming colony with neighbouring domes.
- Recommendation: keep — direct repair of a widely reported suffocation cause; the no-passage half is deliberately left open in BUGS.
- Notes: BUGS' fix sketch mentioned "cap raw outside walks to an oxygen budget" — deliberately not implemented (behaviour change); entry already records this.

### F53 — Arrivals hike to an unreachable "safety dome" and die
- Module: Code/Fix_ArrivalDeaths.lua | Technique: §1.5 replacement | Provenance: mixed — player reports (rocket→dome deaths, "stuck on Universal Depots") plus the sibling tell (CargoTransporterNew:EjectColonists does the passability search Arrive omits)
- Defect: Colonist:Arrive (Colonist.lua:1254-1300) — (a) drops arrivals at the raw "Colonistout" spot with no passability search; (b) `SetCommand("TransportByFoot", dome)` unconditionally, where the ChooseDome fallback `safety_dome` is picked by raw distance without the walkability test (verified _GameUtils.lua:354-362: distance recorded whether or not `is_walking`).
- Call sites: 1 in Src: Colonist.lua:1792 (Idle, `if self.arriving`) — live for every rocket passenger; the defective branches are conditional within it.
- Precondition & player path: (a) land a passenger rocket where the disembark spot is blocked — next to a Universal Depot or on uneven ground (the exact shape of the player reports); (b) land passengers with no welcoming walkable dome in 400m — landing away from the colony, or nearby domes full/not accepting, while a distant dome exists to become `safety_dome`. Nothing in the landing UI forbids either; both are plain (mis)play.
- Searched: _GameUtils.lua:346-441 (safety_dome selection and ChooseDome fallback confirmed); RocketBase/CargoTransporterNew arrival assignment per the header's cites; confirmed the vanilla "ConfusedColonists" branch handles only the dome==nil case, not the unreachable-dome case.
- Tier: R2 — needs a situational landing (blocked spot or out-of-range/full domes), but those are ordinary player situations with matching community reports.
- Recommendation: keep — arrival deaths are unrecoverable losses; the fix falls back to the shipped "Confused Colonists" path when in doubt.

### F54 — Switched-off Shuttle Hubs still count as available transport
- Module: Code/Fix_ShuttleHubOffAvailable.lua | Technique: §1.4b global replacement | Provenance: source-diff — predicate audit of the transport chain; symptom (queuing at pickup spots) is player-visible
- Defect: IsLRTransportAvailable (ShuttleHub.lua:350-359, verified) — the permission-reason clause admits `"TurnedOff"` (player's `ui_working` switch), so an off hub counts as available while SendOutShuttles only runs under `working`.
- Call sites: 6 in Src, all live: Dome.lua:259 (dome walkability/passage discount — continuous), Colonist.lua:1569 (walk-branch of TryToEmigrateToDome), :2650 (FindEmigrationDome — every emigration pass), :2759 (IsTransportAvailableBetween), :2783 (transport-task wait loop), :2832 (transport request exec). Every consumer misjudges while any off hub with shuttles exists and no on hub does.
- Precondition & player path: switch the colony's hub(s) off — one routine toggle, standard during power crises and late-game power saving; with the common single-hub colony, one click produces the false verdict everywhere. PT-34 reached it by playing (hubs toggled off: nobody waited outdoors; back on: emigration resumed).
- Searched: dispatch sites (ShuttleHubBase:BuildingUpdate :1622-1630, CargoShuttle:LaunchDstr :509-513, per entry, both gated on `working`); the four admissible permission states enumerated in BUGS were re-checked against BaseBuilding.lua/RequiresMaintenance.lua cites.
- Tier: R1 — a single ordinary toggle available from the first hub onward; play-proven by PT-34.
- Recommendation: keep — strictly corrects a colony-wide predicate with six live consumers.

### F58 — Invisible residence reservations never expire
- Module: Code/Fix_StaleReservations.lua | Technique: §1.4 wrapper + §1.2 OnMsg sweep | Provenance: mixed — player report ("can't find houses in a >50% vacant dome") plus dev-shipped fixup as drift evidence
- Defect: reservation lifecycle around Residence:GetFreeSpace (Residence.lua:198-200) — slots reserved at emigration (Colonist.lua:1571/1579/1589; also ColonistTransport.lua:636, Residence.lua:318, MicroGHabitat.lua:92) are released only on arrival/death/re-home; no timeout exists (only the user-forced lock has one, Colonist.lua:2329-2342).
- Call sites: producers all live in ordinary play (every shuttle emigration reserves); the defect is the ABSENT release path, so the question is whether a reservation can orphan: yes — verified SavegameFixups.RemoveReservedInSameResidence (Residence.lua:591-599) exists, a dev-shipped repair proving the reserved list drifts in production, and it runs only on save-version load, never in-session.
- Precondition & player path: a shuttle emigration that stalls — hubs toggled off (F54's live state), a fuel drought grounding shuttles, or the shipped F51 cache keeping the pickup from ever resolving — leaves the waiting colonist holding a destination slot for sols while being excluded from the Homeless label (Colonist.lua:2284); the desync case needs nothing but the drift the devs already patch around.
- Searched: full grep of ReserveResidence/CancelResidenceReservation call sites (listed above); confirmed no timed release exists outside the user-forced lock; confirmed the dev fixup.
- Tier: R2 — needs a stalled shuttle pipeline or list desync, but both are genuine, common states (and near-universal in the shipped game, where F51/F54 themselves manufacture eternal waiters).
- Recommendation: keep — bounded, self-limiting sweep that also backstops the other transport fixes' residual cases.

### F59 — Freed housing never notifies the dome's homeless
- Module: Code/Fix_FreedHousingNotice.lua | Technique: §1.4 wrapper | Provenance: source-diff — call-site enumeration: every shipped CheckHomeForHomeless caller is a player action, none fires on organic vacancy
- Defect: Residence:RemoveResident (Residence.lua:83-89) frees a bed without calling CheckHomeForHomeless (:124-133), so homeless colonists wait for their own throttled heavy update.
- Call sites: shipped CheckHomeForHomeless callers verified by grep — Residence.lua:30 (GameInit), :137 (SetUIWorking on), :180 (SetDome), Hotel.lua:23 — all player-triggered; RemoveResident's only caller is Colonist:SetResidence (Colonist.lua:2298), the hook point, which fires on death, kick-out, re-home, dome-off evictions (Residence.lua:51/121/232, Colonist.lua:366/958/993/4151, TraitPreset.lua:762) — all live.
- Precondition & player path: a dome with at least one homeless colonist plus any organically freed bed (a resident dies or moves) — routine in any housing-pressured colony. The wait scales with `#colonists/300` hours, clamped to 12h (City.lua:118-120, verified), so it bites from ~300 population upward and hard at 3600+.
- Searched: grep of CheckHomeForHomeless/RemoveResident/SetResidence across Src (results above).
- Tier: R1 — vacancies-with-homeless is ordinary play; the defect is a universal delay whose magnitude grows with colony size.
- Recommendation: keep — cheap, guarded post-hook; the un-hooked reservation site is a documented, deliberate boundary (race with `assert` + unconditional insert).

### F60 — Dome free-space counts `working`, assignment uses `ui_working`
- Module: Code/Fix_DomeFreeSpaceMismatch.lua | Technique: §1.5 replacement (two-line) | Provenance: source-diff — sibling tally functions in the same file (`GetFreeWorkplaces*`, _GameUtils.lua:443-473) count on `ui_working`
- Defect: Dome:RefreshFreeLivingSpaces (Dome.lua:2832-2834, verified) omits the `"player_enabled"` argument to GatherFreeLivingSpaces (_GameUtils.lua:475), so the dome total counts only currently-`working` residences while ChooseResidence (Residence.lua:404-413) and Colonist:UpdateResidence assign by `ui_working`.
- Call sites: the method is the lazy refresher behind Community:GetFreeLivingSpace/HasFreeLivingSpaceFor (Community.lua:322-349, verified) — consumed by birth and immigration gates (Dome.lua:2240, :3295, :3325-3328, :3684 per entry); recomputed at read time, so any read during an outage takes the wrong tally. ResourceOverview.lua:615 shows the correct call pattern (passes `"player_enabled"`), reinforcing intent.
- Precondition & player path: any residence with `ui_working` true but `working` false at read time — a power deficit, dust-storm outage, broken cable, water/air shortage, or pending maintenance. Every colony experiences these repeatedly; birth/immigration checks run continuously.
- Searched: grep of GatherFreeLivingSpaces/RefreshFreeLivingSpaces callers (all listed above); confirmed the `player_enabled` parameter has exactly one Src caller (ResourceOverview.lua:615).
- Tier: R1 — outages are a core disaster loop and the mismatched tally is read by always-on gates.
- Recommendation: keep — one argument, zero risk, removes a routine births/immigration undercount.
- Notes: MicroGHabitatBase:RefreshFreeLivingSpaces (MicroGHabitat.lua:42-44) has the same omission, deliberately left to F73's domain — already recorded in BUGS.

### F73 — Asteroid colonists idle outdoors; nothing shelters the suffocating
- Module: Code/Fix_ShelterReflex.lua | Technique: §1.5 replacement (a) + §1.4 pre-wrapper (b) | Provenance: mixed — known asteroid suffocation complaints plus the source chain (no seek-shelter branch anywhere in Idle)
- Defect: (a) MicroGHabitatAutoResolve:IsSuitable (MicroGHabitat.lua:154-156) — `GetScoreFor > 0` collapses to HasLifeSupport(), so one tick without power/air evicts all residents; (b) Colonist:Idle (Colonist.lua:1770ff) has no branch for the oxygen timer, so homeless/idle colonists mill outdoors in vacuum until dead.
- Call sites: (a) IsSuitable is AutoResolve-combined ("and", Building.lua:14) into the habitat's IsSuitable, consumed at Residence.lua:69/162/404/413/544 and MicroGHabitat.lua:144-147 — live for any inhabited asteroid; (b) Idle is the universal colonist command — the wrapper's branch self-gates on outside-in-vacuum with a working residence.
- Precondition & player path: asteroid habitation is base Relaunched content on the standard research tree: MicroGLanders (`group = "ReconAndExpansion"`, TechPreset.lua:3157-3164) unlocks Asteroid Landers; AdvancedMicroGMiningOperations (TechPreset.lua:3434-3440) unlocks the Micro-G Mining Station and Micro-G Habitat "allow colonists to stay and work on Asteroids". Player path: research both, order a lander, land on a passing asteroid, build habitat + mining station, ferry colonists over. Only the optional NoUndergroundAndAsteroids game rule removes it. Life-support blips on an asteroid (independent tiny grids, no dome buffer) are the normal operating condition. PT-19 PASS was on a live colony save (real MicroG Habitat with 9 residents + mining station) — the state was reached by playing.
- Searched: Data\TechPreset.lua for the asteroid tech chain and its gating condition (`NoUndergroundAndAsteroids`); Data\BuildingTemplate\MicroGHabitat.lua (shipped template, build_category "Domes"); grep MicroGHabitatAutoResolve/IsSuitable across Src.
- Tier: R2 — requires deliberate but ordinary mid-game asteroid colonisation (two mainline techs + a lander trip); play-proven by PT-19.
- Recommendation: keep — asteroid crews are small and irreplaceable mid-mission; the (b) half's live trigger was not observed in PT-19 (the (a) fix prevents the producer), but it remains the safety net for the still-shipped homeless-outdoors path.
- Notes: PT-19 also recorded a vanilla quirk (status effects read the residence's life support, not the occupied building) — already captured in BUGS; not a pack defect.

## Disasters & landscaping (F01, F02, F26, F30, F31, F33, F34, F78, F81)

### F01 — Cave-ins ignore "No Disasters" rule
- Module: Code/Fix_CaveInsNoDisasters.lua | Technique: §1.3 registry-wrap (FUNC slot of `PeriodicRepeatInfo["UndergroundMarsquake"]`) | Provenance: player-report — matches a live Paradox-forum report per the BUGS entry.
- Defect: the `MapGameTimeRepeat("UndergroundMarsquake")` body (Marsquake.lua:306-322) — fires underground quakes with no `IsGameRuleActive("NoDisasters")` check, unlike every sibling (ColdWave.lua:222, DustStorm.lua:413, DustDevils.lua:189, surface path Marsquake.lua:43).
- Call sites: not a called function — a periodic repeat registered once (Marsquake.lua:306); its COND (Marsquake.lua:323-325) restricts ticking to maps with `Environment == "Underground"` and game logic, so it runs unconditionally on the underground map every `MarsquakeSpawnTime` hours. One live executor, zero eliminations.
- Precondition & player path: create a game with the No Disasters rule (and without "No Underground and Asteroids", so the underground map generates — RandomMapGenerator_Picard.lua:265-291); play the underground (Below & Beyond content ships inside Relaunched). Cave-ins then keep occurring despite the rule.
- Searched: repeat COND, GenerateAdditionalMaps rule gate; confirmed no NoDisasters check anywhere in Marsquake.lua's underground path.
- Tier: R2 — needs the No Disasters game rule plus underground play; within that combination it is unconditional and was reported by real players.
- Recommendation: keep.
- Notes: PT-11's PASS manufactured the tick cadence via console `g_Consts` compression and used `CheatTriggerUndergroundMarsquake()` as positive control, so the PT does not itself prove reachability — the forum report and the unconditional code path do.

### F02 — Meteors strike ~every 6h instead of 35–115h
- Module: Code/Fix_MeteorFrequency.lua | Technique: §1.5 replacement (repaired thread-body copy installed in `GlobalGameTimeThreadFuncs`, plus §1.2 watchdog/LoadGame handlers) | Provenance: source-diff — dead `if` proven against the intact twin patterns (DustDevils.lua:168-173, MeteorStorm thread).
- Defect: the "Meteors" global thread body (Meteors.lua:266-303) — `start_time = GameTime()` immediately followed by `if GameTime() - start_time > spawn_time - warning_time` (:280-281) is always false, so the only wait is `Sleep(Min(spawn_time, warning_time))` (:291-292) with a 6-game-hour default warning; Sensor Towers invert into interval-lengtheners.
- Call sites: thread body, not a callee — registered at Meteors.lua:266 and (re)started for every colony from `GlobalGameTimeThreadFuncs` on PostNewGame (Config\_fixup.lua). Only exits: NoDisasters rule (:267) and nil/forbidden descriptor (:271-275; `GetMeteorsDescr` returns nil only for `mapdata.MapSettings_Meteor == "disabled"`, :254-257). Live in every colony with any meteor threat.
- Precondition & player path: start any colony on a map with a nonzero meteor threat level and no No Disasters rule — the defective loop is the scheduler itself; strikes arrive ~every 6h from sol 1.
- Searched: Meteors.lua thread body and GetMeteorsDescr nil paths; Data\MapSettings-Meteor.lua (all five threat presets carry meteors).
- Tier: R1 — the broken wait is the only wait in a thread that runs in essentially every colony; the mis-cadence is immediately player-visible.
- Recommendation: keep.
- Notes: PT-01's first leg observed the fixed thread hitting designed cadence in live play (+60/+39/+39/+57h); the subsequent silence was root-caused to F78/F81, not to this defect — the BUGS status note already records this correctly.

### F26 — Bombardment missiles fly parallel (cosmetic)
- Module: Code/Fix_BombardmentSpread.lua | Technique: §1.5 replacement (100-line body copy of `WaitBombard`, one line corrected) | Provenance: source-diff — `spawn_dir` assigned at :82 and never read; intent proven by `GenerateDir`'s jitter purpose and Meteors.lua:106-107.
- Defect: `WaitBombard` (Bombardment.lua:55-154) — :83 builds `spawn_pos` from the volley-wide `dir` instead of the per-missile `spawn_dir` computed at :82, so all missiles arrive parallel.
- Call sites: 2 in Src: Bombardment.lua:158 (`StartBombard`, LIVE) and Bombardment.lua:176 (`TestBombard`, ELIMINATED — inside `if Platform.debug`, :173, not shipped-player-reachable). `StartBombard` in turn has exactly one gameplay caller: Mystery 7.generated.lua:941 (`StartBombard(RandomDome, 500*guim, 20, 2000, 6000)`), LIVE.
- Precondition & player path: play Mystery 7 "The Last War" (selectable at new-game or drawn at random) to its scripted "Earth Attacks!!!" beat (Mystery 7.generated.lua:278-291), which starts the "Bombardment" sequence (:921-948) — a loop that bombards a random dome every 2-4 game hours until war tension resolves, so a player in that mystery sees many defective volleys.
- Searched: whole-tree grep for `WaitBombard|StartBombard`; only Mystery 7 and the debug helper call it.
- Tier: R2 — needs one specific mystery, but within it the defect fires repeatedly and is the mystery's signature spectacle.
- Recommendation: keep — cosmetic but reliably seen by every Last War player; the §1.5 re-verify-on-update cost is already recorded in BUGS.

### F30 — Lake placement entombs RC builder + drones
- Module: Code/Fix_LakeEntombment.lua | Technique: §1.4 chained post-wrapper on `LandscapeLake:PlacePrefab` | Provenance: mixed — source analysis plus live evidence (the "lake-victim" player report referenced under F32, and the devs' own partial rover-rescue fixup `BaseRover.lua:736-745`, which only exists because this happened to players).
- Defect: two-part — `ConstructionSite:ScatterUnitsUnderneath` (ConstructionSite.lua:1722-1740) exempts the RC Constructor working the site (:1726), and the scatter runs before `LandscapeLake:GameInit` digs the basin (LandscapeLake.lua:32-35, 215+), when `ExitImpassable` still no-ops on passable ground — so the terrain drop seals rover and drones inside.
- Call sites: 1 in Src for the wrapped method: LandscapeLake.lua:34 (GameInit), LIVE — runs on every artificial-lake completion. (Global `PlacePrefab` and `CrystalsBuildingBase:PlacePrefab` are different functions/classes, untouched.)
- Precondition & player path: build any artificial lake from the stock Landscaping menu; the RC Constructor building it is by construction standing in the basin and is by code exempt from the scatter — the entombment is the default outcome, not a coincidence.
- Searched: grep `PlacePrefab` (whole Lua tree), `ScatterUnitsUnderneath|GetUnitsUnderneath`; read the exemption at ConstructionSite.lua:1726 and the scatter trigger at ClearWasteRockConstructionSite.lua:69-77.
- Tier: R1 — a stock, ungated player action (place a lake) reproduces it deterministically; the shipped rover-rescue savegame fixup is the developers' own admission of live incidence.
- Recommendation: keep.

### F31 — Anomaly cave-in hardcodes UndergroundMap
- Module: Code/Fix_AnomalyCaveInMap.lua | Technique: §1.4 chained wrapper (×2: `TriggerCaveIn`, `FindCaveInLocation`) | Provenance: source-diff — "hardcodes", cross-file call-site sweep, no player report.
- Defect: `TriggerCaveIn` (CaveInRubble.lua:94-117) guards `pos` but calls `map:MapFindNearest` unguarded (:101); `FindCaveInLocation` likewise indexes `map.object_hex_grid` unguarded (:21-27). Handed `UndergroundMap == false`, either raises and kills the running sequence thread.
- Call sites: 12 in Src. `TriggerCaveIn`: Marsquake.lua:266 (local `map`, always a real map — ELIMINATED for the defect) and :287 (`CurrentMap` — ELIMINATED); 8 scenario sites passing the global `UndergroundMap`: UndergroundAnomalies.generated.lua:240, BuriedWonder_Jumbo_Cave.generated.lua:340/539/769, BuriedWonder_Jumbo_Cave_106.generated.lua:339/538/768, BuriedWonder_Cave_Of_Wonders.generated.lua:430 — all EXECUTE in play, but none can execute with `UndergroundMap == false` (below). `FindCaveInLocation`: Marsquake.lua:263 (ELIMINATED, local map) and Cave_Of_Wonders:430 (same analysis).
- Precondition & player path: the crash needs a calling sequence to run while `UndergroundMap` is false — but every shipped trigger lives ON the underground map: the UndergroundAnomalies list is spawned there (BuildingAnomalies.generated.lua:56-93 arrival sequence; anomaly markers on underground maps), and the four Buried Wonders are placed only via `BuriedWonderMarker`s on underground maps (RandomMapGenerator_Picard.lua:111-127, const.BuriedWonders at UndergroundWonder.lua:24). `UndergroundMap` is assigned when that map is generated (Picard.lua:282-284) and is false only when generation was skipped — the "No Underground and Asteroids" rule (Picard.lua:266) — which also removes every trigger. The precondition and its trigger are mutually exclusive in shipped data.
- Searched: whole-tree grep `TriggerCaveIn|FindCaveInLocation|UndergroundAnomalies|BuriedWonder|GenerateAdditionalMaps`; anomaly sequence-list plumbing (Anomaly.lua:26-33, 99-126, 293-303; RandomMapGenerator.lua:4334-4369). Caveat: per-map `anomaly_sequence_list_names` live in binary mapdata, not greppable from Src — a shipped surface map declaring the UndergroundAnomalies list is the one hole I could not close, though every sequence in it is underground-themed content.
- Tier: R3 — the defective branch is reachable in principle (any future patch, scenario, or mod that calls `TriggerCaveIn` outside the underground, or a mapdata quirk) but no shipped Lua/Data path can produce map==false at a call site.
- Recommendation: keep — near-zero-cost pass-through wrapper whose decline branch is pure insurance; deleting buys nothing and forfeits protection for mod/patch content.
- Notes: the wrong-map half (rubble aimed at `UndergroundMap` from a sequence on another map) is also vacuous in shipped play for the same reason — the sequences only run on the underground map, so the hardcode happens to name the right map. BUGS already records that half as not fixable from Lua; this audit adds that it is also not reachable as a wrong-map bug in shipped data.

### F33 — Drone crash on small landscaping sites
- Module: Code/Fix_SmallLandscapeSites.lua | Technique: §1.5 replacement (15-line method copy, loop bound clamped) | Provenance: source-diff — unguarded `dests[i]` against a periphery-only cache.
- Defect: `LandscapeConstructionSiteBase:GetClosestDests` (LandscapeConstructionSiteBase.lua:178-192) — copies `top_count` (default 5) entries out of `dests` with no size check; `drone_dests_cache` holds only periphery hexes (`if border then`, :47-64), so a small site has <5 and `dests[i].dest` indexes nil, killing the drone's command thread.
- Call sites: 1 in Src: LandscapeConstructionSiteBase.lua:202 (`DroneApproach`), LIVE — runs for every drone approaching any landscape site type (clear/paint/level all inherit this base).
- Precondition & player path: make a small landscaping mark and let a drone work it. The texture-paint tool's minimum brush is 5m (LandscapeTexture.lua:25, `brush_radius_min = 5*guim`) — under one hex spacing — so a single min-brush dab yields a site of 1-3 border hexes; the general controller minimum is 10m (LandscapeConstructionController.lua:65), also small enough when clipped by obstructions. No rule, tech, or content gate.
- Searched: grep `GetClosestDests` (sole caller confirmed); brush-size floors in Lua\Landscape.
- Tier: R1 — an ordinary use of a stock tool at small brush size produces the crash deterministically on first drone approach.
- Recommendation: keep.

### F34 — Landscape unit sweep ignores its own filter (item d)
- Module: Code/Fix_LandscapeUnitFilter.lua | Technique: §1.5 replacement (global `LandscapeForEachUnit` body copy, one argument corrected) | Provenance: source-diff — copy-paste slip proven by the sibling `LandscapeForEachStockpile` (:436-451) and by `ConstructionSite:GetUnitsUnderneath`'s identical Embark filter (ConstructionSite.lua:1713-1714).
- Defect: `LandscapeForEachUnit` (Landscaping.lua:455-469) builds `filter_embark` (Embark exclusion + `passed` dedup) then passes the raw `callback` to `Landscape_ForEachObject` instead, so boarding units are swept and duplicates are not collapsed.
- Call sites: 1 in Src: LandscapeConstructionSite.lua:23 (`GetUnitsUnderneath`), LIVE — reached from `ScatterUnitsUnderneath` at every landscape site's GameInit (ClearWasteRockConstructionSite.lua:69-77). The function thus EXECUTES on every landscaping placement; the defective effect needs a filtered-out unit present.
- Precondition & player path: place a landscaping mark over a drone currently in the "Embark" command — i.e. boarding a rocket being loaded (RocketBase.lua:1926, LanderRocket.lua:1042), an RC rover (RCRover.lua:275), or a cargo transporter (CargoTransporterNew.lua:835) — and the scatter yanks it mid-board via `SetCommand("ExitImpassable")`; the lost dedup additionally re-interrupts any unit the engine sweep visits twice. Landscaping near an active rocket pad is ordinary play, but the overlap is a timing coincidence.
- Searched: grep `LandscapeForEachUnit` (sole consumer), `"Embark"` across Lua (who sets it), `ScatterUnitsUnderneath` triggers.
- Tier: R2 — the sweep runs in every landscaping job, but the harmful branch needs a boarding drone (or duplicate visit) under the mark at that moment: a real, unforced play situation, not an every-colony event.
- Recommendation: keep.
- Notes: shipped Lua sets "Embark" only on Drones — the fix title's/header's "boarding colonists" overstates; colonists board via other commands and were never protected by this filter in the vanilla sibling either. The player-visible save is boarding drones plus the dedup. Worth a one-word title tweak someday; behavior of the fix is correct regardless.

### F78 — Meteor storm wedges forever in its unbounded drain loop
- Module: Code/Fix_MeteorStormWedge.lua | Technique: §1.3 registry/thread surgery (hourly watchdog + `RestartGlobalGameTimeThread` + guarded stop-pulse + forced cleanup; no body copy) | Provenance: player-report — user's TEST 2G save, then reproduced and localized live 2026-07-29.
- Defect: the drain loop in `MeteorsDisaster` (Meteors.lua:238-241) — `while not g_MeteorStormStop and #spawned > 0 do WaitMsg("MeteorDone", delta); table.validate(spawned) end` is unbounded; in the live repro 73 descriptors drained to 2 that never invalidated, wedging the calling thread forever and (for storms) holding the scheduler so no storm is ever scheduled again.
- Call sites: `MeteorsDisaster` has 6 in Src (the drain loop is shared by all types): Meteors.lua:293 (Meteors thread, single/multispawn — LIVE, every meteor-enabled colony), Meteors.lua:346 (MeteorStorm thread, "storm" — LIVE on storm-enabled maps: all threat presets except Meteor_VeryLow's `storm_forbidden`, Data\MapSettings-Meteor.lua:10), Data\POI.lua:52 (Capture Meteors special-project completion fires a "storm" with Meteor_POI — LIVE, player-launched, not gated by NoDisasters), MapSettings.lua:283/286 + ClassDef-Effects.generated.lua:3374 (data-driven disaster effects — LIVE where storybit/sequence data uses them), Meteors.lua:1095 (ELIMINATED — `Platform.cheats` TestMeteor), Cheats.lua:69 (ELIMINATED — console).
- Precondition & player path: a meteor storm on any map with threat Low+ (natural scheduler, birth_hour ≈250-750h) or via the Capture Meteors expedition on any map; then the residual-meteor condition (cause unpinned — MDS interception, off-map impact, fall-thread death are the candidates). Reached BY PLAYING: the 2026-07-29 live session caught a naturally scheduled storm ("Meteor Storm 8h→1h" countdown) wedged in the drain loop alongside the console one, and the F02 watchdog had earlier caught the Meteors thread itself stuck at phase `striking` for 183h on the user's organically played save.
- Searched: grep `MeteorsDisaster\(`; read the full spawn/drain body (:131-252); storm gating (:307-316); POI data.
- Tier: R2 — needs a storm-enabled map (the large majority) plus the unpinned residual-meteor condition, but the wedge is proven in ordinary play on a real save, twice in one sitting.
- Recommendation: keep.
- Notes: the drain loop is shared by single/multispawn strikes too, and the TEST 2G evidence shows the Meteors thread wedging the same way — but the fix's wedge signature requires `g_MeteorStorm` set, so a wedged single/multispawn strike is covered by F02's watchdog, not this one. Division of labor is correct as built; worth keeping in mind if a non-storm wedge ever resurfaces without F02 active.

### F81 (prediction-leak half) — Stranded prediction flag gates all weather
- Module: Code/Fix_DisasterPredictionLeak.lua | Technique: §1.2 additive (OnMsg.MeteorStormEnded removal) + §1.3 one-shot PostLoadGame sweep | Provenance: mixed — user report (194-sol weatherless save) confirmed by a source-exhaustive trace, then proven live end-to-end.
- Defect: `AddDisasterNotification` sets `g_DisastersPredicted[base_id] = true` for every disaster notification (MapSettings.lua:169) and only `RemoveDisasterNotifications` clears it (:176); the storm DURATION notification (Meteors.lua:179) has no removal on the normal completion path (:242-251 — verified: the tail plays FX, sends MeteorStormEnded, clears `g_MeteorStorm`, never removes) — so every completed meteor storm strands the flag forever, making `IsDisasterPredicted()` permanently true.
- Call sites: the leak's producers: Meteors.lua:179 via the MeteorStorm thread (:346, LIVE on all storm-enabled maps) and via the Capture Meteors POI storm (Data\POI.lua:52, LIVE on any map, not NoDisasters-gated). The only shipped removals are the force-stop branch (Meteors.lua:227), the pre-storm warning clear (:344), and the 80%-Atmosphere threshold (TerraformingDisasters.lua:27) — none on the normal end. Downstream victims: dust storm/cold wave schedulers defer forever (DustStorm.lua:439-446/464-465, ColdWave.lua:208-215/228-229), the rains gate (below), `WaitCurrentDisaster` POI rewards, the Inner Light dream cycle.
- Precondition & player path: let one meteor storm run to its natural end — routine on any Meteor_Low/High/VeryHigh map within tens of sols, or one Capture Meteors expedition anywhere. Reached by playing, proven: the user's organically played 194-sol save carried exactly this stranded flag, and clearing it started rain within seconds.
- Searched: (relied on and spot-verified the entry's grep-exhaustive removal list; independently re-read Meteors.lua:215-251 tail and Data\MapSettings-Meteor.lua storm gating.)
- Tier: R1 — one healthy storm poisons the colony's whole weather/disaster system permanently; storms are on by default on all but the lowest-threat maps, and the POI path covers even those.
- Recommendation: keep.
- Notes: the POI storm path (Data\POI.lua:47-69) is not in the BUGS entry's reachability story and strengthens it: it bypasses both the NoDisasters rule and map storm settings, so even rule-protected colonies can strand the flag by launching Capture Meteors.

### F81 (rains half) — One collision kills a rain type for the save
- Module: Code/Fix_RainsDeadlock.lua | Technique: §1.5 replacement (7-line leaf global `RainsDisasterLoop`, one bounded WaitMsg) + §1.3 PostLoadGame thread swap | Provenance: mixed — user report (no rain after two greenhouse-gas import events), defect proven statically; deadlock itself not yet observed live.
- Defect: `RainsDisasterLoop` (TerraformingDisasters.lua:310-316) — untimed `WaitMsg("RainDisasterEnd")`; `RainsDisasterActivation` returns without raining if `IsDisasterActive() or IsDisasterPredicted()` (:277), so the message never comes and the loop blocks forever; `UpdateRainsThreads` reuses the blocked-but-valid thread (:411-415), so nothing ever rescues it.
- Call sites: 2 creators in Src: TerraformingDisasters.lua:419 (`UpdateRainsThreads`, LIVE — fired via OnMsg.TerraformParamChanged → DelayedCall, :486-489) and the CityStart-side initializer that seeds `RainsDisasterThreads` placeholders (:320-337). No other caller of the loop body.
- Precondition & player path: rains are gated by terraforming — `UpdateRainsThreads` creates a loop only when Atmosphere, Temperature AND Water are all at or above a rain band's start thresholds (:400-403; live-save panel: normal rains ≈40/40/10, toxic bands lower) and not all past its end (:407-410); toxic rains are additionally off under NoDisasters (:386-388). So: terraform into a rain band (GHG factories/imports, Forestation — normal mid/late-game play), then have one rain roll land inside any other disaster's active or warning window — with sensor towers pinning warnings at 75h (MapSettings.lua:94-98), a collision on a long save is close to certain. That rain type is then dead for the rest of the save.
- Searched: grep `RainsDisasterLoop|UpdateRainsThreads`; read :310-435 in full (band gating, thread reuse, NoDisasters branch).
- Tier: R2 — needs terraforming progress into a rain band plus any coexisting disaster; both are genuine, common player states, and the collision math makes the deadlock near-inevitable once they coexist, but it is not yet demonstrated live (the 194-sol save's rain threads were empty placeholders — the leak half alone explained its silence).
- Recommendation: keep + record observation: a live save whose rain loop is blocked in `WaitMsg` with a stale roll (console read of `RainsDisasterThreads[type].activation_thread` status, or simply rain resuming ≤7 sols after a collision under the fix) would upgrade this to proven; ~~the PT-54 leg already planned for F78/F81 can carry it~~ — **PT-54 was retired unrun 2026-08-01; the observation now rides the F86 Tier-1 `Fix_RainsDeadlock` rewrite's own A/B leg** (BUGS F81 entry).
- Notes: under NoDisasters, normal rains still run and toxic rains are never created — but collisions remain possible between concurrent rain types and mystery "dream" disasters, so the rule does not make the defect unreachable, only rarer.

## Mysteries, story & traits (F05-F07/F15, F16, F17, F23, F29, F40, F41, F75)

### F05 — Milestone completion crashes (NoTerraforming/NoPolitics)
- Module: Code/Fix_MilestoneCrash.lua | Technique: §1.4b global-replacement | Provenance: source-diff — nil-return analysis of GetScore(), no player report cited
- Defect: local `eval_complete_all_milestones` (Milestones.lua:87-106, reached only from `CompleteMilestone` :108-142) — hidden-but-uncompleted milestones fall through to `score_sum + milestone:GetScore()` where GetScore() is nil → arithmetic-on-nil aborts the thread, losing the "AllMilestonesCompleted" popup.
- Call sites: 30 in Src, all live: Milestones.lua:190,194 (FindWater eval, fires on water-deposit reveal) + 28 per-milestone completion triggers in Data\Milestone.lua (:15 through :664, one per milestone preset — each fires organically when its milestone condition is met). The defective branch inside the callee is what's gated, not the call sites.
- Precondition & player path: start a game with the **No Terraforming** or **No Politics** game rule — both verified as shipped, selectable GameRuleDefs (Data\GameRuleDef.lua:101-107 NoTerraforming; :39-57 NoPolitics; picked via the pre-game `idGameRules` param, PreGameMission.lua:94-102). 9 milestones carry `not IsGameRuleActive("NoTerraforming")` prerequisites and 1 carries NoPolitics (Data\Milestone.lua:386-672), guaranteeing hidden-uncompleted milestones; then complete the visible milestones by playing (long completionist game, but every trigger is organic).
- Searched: GameRuleDef presets for both rules; Milestone.lua prerequisites (9 + 1 confirmed); full-tree grep of `CompleteMilestone(` call sites.
- Tier: R2 — needs one specific, real, player-selectable game rule plus finishing all visible milestones; a genuine (if long) playthrough.
- Recommendation: keep — a hard error that silently eats the endgame celebration under two advertised rules.
- Notes: PT-05 (2026-07-26) PASSed on a save that organically had the rule active and 9 hidden milestones, but the completions themselves were issued from the console (PLAYTEST_ARCHIVE.md:333-364) — so PT-05 proves the fix works, not by-play reachability; the R2 verdict here rests on the source chain above, which is solid.

### F06 — Philosopher's Stone mystery can hang forever
- Module: Code/Fix_CrystalMysteryHang.lua | Technique: §1.2 additive | Provenance: source-diff — "CrystalForceFlyAway has no emitter anywhere" is a whole-tree-search tell
- Defect: `Crystal:ComposeProc` (Mysteries\Crystals.lua:45-84) emits `Msg("CrystalFlyAway")` exactly once, 1 sol after CrystalComplete (:67-70); the scenario (Mystery 10.generated.lua:232-271) blocks on the Epilogue popup first and only then does `WaitMsg("CrystalFlyAway")` (:271) — miss the one-shot and `Msg("MysteryEnd")` never fires.
- Call sites: message-consumer enumeration (whole-tree grep): `CrystalFlyAway` has exactly one consumer (Mystery 10.generated.lua:271, live); `CrystalForceFlyAway` has zero emitters in all of Src — confirmed, the escape hatch is dead.
- Precondition & player path: Philosopher's Stone (`CrystalsMystery`, Crystals.lua:3-13, order_pos 4) is directly selectable in the New Game Mystery picker or arrives via "Random" (PreGameMission.lua:81-92, :240-264; Mysteries.lua:17-44). Then the player must leave the Epilogue unanswered >1 sol — and this is MORE plausible than the fix documents: `SA_WaitMessage` inherits `start_minimized` default **true** (SequenceAction.lua:207,344-394) and the Epilogue call passes no override, so the popup arrives only as a corner "View Message" notification (PopupNotification.lua:267-289) with game time running — the pause layer engages only after the player opens it (:8-14). Not clicking a corner notification for one sol at fast-forward is a few real minutes of ordinary inattention.
- Searched: whole-tree greps for both message names; SA_WaitMessage/SA_WaitChoice class defaults; ShowPopupNotification minimized path.
- Tier: R2 — mystery-gated (selectable or random roll), and the trigger condition is passive player inattention, not an exotic action.
- Recommendation: keep — permanently un-completable mystery, and the reachability window is wider than the BUGS entry claims.
- Notes: evidence correction worth recording: BUGS.md:245-252 says the player "can minimise and ignore" the popup — in fact it *starts* minimized by SA default and never pauses the game until opened, which strengthens reachability.

### F07 + F15 — St. Elmo's Fire wisp power / RP rewards
- Module: Code/Fix_WispRewards.lua | Technique: §1.4b global-replacement | Provenance: source-diff — sibling-comparison (":346 and :479 have the `* 1000`") and unreachable-code-after-SetCommand tells
- Defect: `SetLightTrapMode` (Mysteries\Fireflies.lua:674-701) — "free" branch (:692) omits `* 1000` on the power modifier (F07); "destroy" branch double-grants RP on top of the Die destructor's +100 (:540-542) while the notification claims 100 (F15).
- Call sites: 2 in Src, both live and mutually exclusive: Mystery 11.generated.lua:440 (`SetLightTrapMode("free")`, choice 1) and :471 (`"destroy"`, choice 2). Data\Scenario\Mystery 11.lua:526,570 are the source data of the same generated file, not extra runtime callers.
- Precondition & player path: St. Elmo's Fire (`LightsMystery`, Fireflies.lua:1-10, order_pos 8) — selectable at New Game or via Random. The mystery script forces the reachable state: after 30 wisps are trapped (:426-428) the player is given a binary choice, "Symbiotic coexistence" → F07's branch, "Experiment upon them" → F15's branch (:429-471). Every playthrough of the mystery that reaches the choice hits exactly one of the two defects.
- Searched: whole-tree grep of SetLightTrapMode (5 hits: 1 definition, 2 generated callers, 2 data twins).
- Tier: R2 (both halves) — mystery-gated; once in the mystery, hitting one defect or the other is unavoidable.
- Recommendation: keep — both branches are terminal player rewards of a whole mystery arc.

### F16 — Mirror Sphere site usable after completion
- Module: Code/Fix_MirrorSphereSite.lua | Technique: §1.4 chained-wrapper | Provenance: source-diff — progress-scale analysis (100 vs 2^22)
- Defect: `MirrorSphereBuildingBase:StartAction` (Mysteries\MirrorSphere.lua:813-870) — guard `self.progress == 100` (:823) compares against a 0..2^22 scale (GetProgressPct divides, :724-726; SetProgress clamps to max_progress, :733-734), so a finished site never locks out.
- Call sites: 3 in Src, all live: MirrorSphereInfopanel.lua:15 (ActionPierceTheShell), :18 (ActionCommunicate), :21 (ActionFeedPower) — the site's infopanel buttons. Eliminated: MirrorSphereInfopanel.lua:55,58,61 call `PowerDecoyBase:StartAction`, a separate method (MirrorSphere.lua:960) that the fix does not touch; DumbAI.lua's AIStartAction is unrelated.
- Precondition & player path: the "Spheres" mystery (`MirrorSphereMystery`, MirrorSphere.lua:538-547, order_pos 6) — selectable or random. In-mystery: scan the sphere site, perform at least one action to start progress, excavation then also advances passively (BuildingUpdate :766-771) to max_progress, which fires the sphere launch and kills the update thread (:748-763). `IsActionEnabled` (:773-800) blocks only *completed* actions — actions never performed remain enabled on the finished site, the infopanel still shows them, and clicking "Pierce the Shell" connects real drone commanders to a dead work request (:830-834).
- Searched: whole-tree grep of StartAction; IsActionEnabled body for any post-completion lockout (there is none besides the broken :823 guard).
- Tier: R2 — mystery-gated; the finished-site-with-leftover-actions state is the normal end-state of the excavation, since passive progress outruns the action list.
- Recommendation: keep — cheap wrapper preventing real wasted drone-hours in a shipped mystery.

### F17 — Dust Sickness damage not randomized
- Module: Code/Fix_DustSicknessDamage.lua | Technique: §1.1 data-patch | Provenance: source-diff — dead-local (`change` never read) tell
- Defect: `TraitPresets.DustSickness.daily_update_func` (Data\TraitPreset.lua:85-91) — computes `change = 5 + Random(param)` then deals flat `-trait.param` (10) instead, every sol of every dust storm per sick colonist.
- Call sites: 1 consumer — the colonist daily tick reads the preset's daily_update_func live (Colonist.lua:528-536); executes for every colonist carrying the trait while `g_DustStormStart` is set.
- Precondition & player path: the trait is granted ONLY by the DustSickness story-bit family, and the parent storybit is gated on `CheckGameRuleActive "DustInTheWind"` plus sol ≤ 100, ≥30 colonists, DustStormStart trigger (Data\StoryBit\DustSickness.lua:18-30,36). "Dust in the Wind" is a shipped, selectable game rule (GameRuleDef.lua:366-372, challenge_mod 50 — max dust-storm rating). Path: select the rule → grow to 30 colonists before sol 100 → a dust storm rolls the event → sick colonists then bleed max damage every storm for the rest of the game (until the cure tech).
- Searched: whole-tree grep of `DustSickness` — the trait is granted nowhere outside the three storybits' ForEachExecuteEffects (files: DustSickness.lua, _GeneratSick, _GeneratSickNotWorking; _Deaths/_Cure/_CureFound don't add it); GameRuleDef for the rule.
- Tier: R2 — requires the Dust in the Wind game rule; within it the defect is near-certain (the rule maximizes dust storms).
- Recommendation: keep — under the rule this deals flat max damage instead of the 5-14 spread on every sick colonist every storm sol.
- Notes: neither the BUGS entry (:399-410) nor the fix header records the DustInTheWind rule gate — worth adding; it is the single fact that makes this R2 rather than R1.

### F23 — Founder-gains-trait notification never fires
- Module: Code/Fix_FounderTraitNotification.lua | Technique: §1.2 additive | Provenance: source-diff — array-indexed-by-group-name dead-code tell
- Defect: `OnMsg.ColonistAddTrait` (ColonyViability.lua:282-296) — `FounderGainsTraitCategories` is an array indexed with the trait's group string → always nil → notification can never be added.
- Call sites: message emitter is `Colonist:AddTrait` (Colonist.lua:427) — fires on every trait addition in the game, unconditionally live.
- Precondition & player path: Founders exist in every colony — every colonist landing before colony approval gets `traits.Founder = true` (ColonyViability.lua:127). Founders gaining Positive/Negative/Specialization traits post-init is routine ordinary play: Martian University specializations, sanity-breakdown flaws, storybit trait grants (e.g., NewHorizons hands out Guru/Workaholic/ChronicCondition), Playground/Youth trait rolls. No rule, DLC, or mystery required.
- Searched: emitter grep; Founder-trait assignment path in ColonyViability.lua.
- Tier: R1 — every colony has Founders and Founders gain qualifying traits in normal play; the notification is silently missing for everyone.
- Recommendation: keep.

### F29 — Sequence-system latents (mod-facing bundle)
- Module: Code/Fix_SequenceLatents.lua | Technique: §1.5 method-replacements (two) | Provenance: source-diff — explicitly found as dead/no-shipped-user code
- Defect: (a) `SA_GetLabelToRegister:SAExec` (Sequences\SA_Filters.lua:30-40) computes `count`, shuffles, then returns the whole list — `random_count`/`random_percent` ignored; (b) `AlienDigger:GameInit` (Mysteries\Diggers.lua:87-96) broken two-variable swap leaves both timings holding the larger value.
- Call sites: (a) 4 in Src, all in Mystery 2 ("Dredgers", DiggersMystery, Diggers.lua:1-4): Mystery 2.generated.lua:298, :315, :365, :369 — all four execute live in every Dredgers playthrough but pass neither `random_count` nor `random_percent`, so defaults (0/100 → count = #objs) make the missing truncation a no-op; verdict eliminated-as-defective for all 4. (b) GameInit runs live for every AlienDigger/AlienDiggerBig spawned by the Mystery 2 scenario (SA_PlaceObject `class_name = "AlienDigger"`, e.g. :396,:407,:555+), but the swap branch requires `pre_hit_ground_t < pre_hit_ground_t_2` and shipped defaults are 1000/500 — already ordered (Diggers.lua:53-54); the buggy lines never execute.
- Precondition & player path: none in the shipped game for either half. Both would need data that doesn't ship: (a) a sequence setting non-default sampling params; (b) a spawn/subclass inverting the timings — `AlienDiggerBig` (Diggers.lua:350-362), the only subclass, overrides neither field.
- Searched: (a) whole-tree grep of `SA_GetLabelToRegister` (4 runtime callers + data twins); grep of `random_count|random_percent` across all of Data — zero preset sets either. (b) whole-tree grep of `AlienDigger` (all spawns are bare class-name placements) and of `pre_hit_ground` (only Diggers.lua + unrelated rocket fields with their own assert-guarded ordering, RocketBase.lua:461).
- Tier: R3 — classification CONFIRMED with the searches above: both code paths run in a real mystery, but no shipped data can make the defective behavior observable; a scenario mod or future patch data would light either up.
- Recommendation: keep (flag: §1.5 latent) — matches its tracked mod-facing rationale; the two replacements are tiny and independently self-checked, so carry cost is low.
- Notes: the deliberately-unfixed third item (SA_WaitMarsTime generator inversion, SA_Gameplay.lua:2705) also verified as compile-time-only — no runtime surface; leaving it unfixed remains correct.

### F40 — Dust Sickness infects Biorobots
- Module: Code/Fix_DustSicknessBiorobots.lua | Technique: §1.1 data-patch (+LoadGame sweep) | Provenance: source-diff — filter-list analysis
- Defect: the four `ForEachExecuteEffects` that grant DustSickness (Data\StoryBit\DustSickness.lua:63-77,:103-117; DustSickness_GeneratSick.lua:5-26; _GeneratSickNotWorking.lua:5-26) filter out only `Child` — Android colonists are in the Colonist label and get infected.
- Call sites: same single consumer chain as F17 — the storybit outcome effects, all downstream of the DustInTheWind-gated parent storybit.
- Precondition & player path: two named gates, both real: (1) the **Dust in the Wind** game rule (parent storybit prerequisite, DustSickness.lua:19-21) with a dust storm, ≥30 colonists, sol ≤ 100; (2) **The Positronic Brain** breakthrough (TechPreset.lua:336-344 — "Biorobots can be constructed in the Drone Assembler"), obtained via normal breakthrough research/anomalies, plus actually building Biorobot colonists so Androids are in the label when the storybit's effect sweeps it. Stacked but entirely organic; a Dust-in-the-Wind colony that gets the breakthrough will hit it.
- Searched: same DustSickness whole-tree grep as F17 (no other trait source); TechPreset for the Biorobots-granting tech.
- Tier: R2 — two independent conditional gates, both ordinary content (a selectable rule + a random breakthrough).
- Recommendation: keep — androids permanently bleeding Health with no cure path (the cure tech chain assumes human patients) is a real loss state, and the LoadGame sweep also rescues existing saves.
- Notes: as with F17, the DustInTheWind gate is absent from the BUGS entry (:968-980); "Biorobots breakthrough" in the tracker is actually named **The Positronic Brain** in shipped data.

### F41 — Gene Forging tech has no effect
- Module: Code/Fix_GeneForging.lua | Technique: §1.4b global-replacement | Provenance: mixed — community-known (ChoGGi shipped a fix) plus source confirmation
- Defect: `GetRareTraitChance` (Colonist.lua:3541-3550) consults only GeneSelection; researching GeneForging (TechPreset.lua:1556-1564, param1=50) changes nothing.
- Call sites: 2 in Src, both live: Colonist.lua:3559 (`GenerateTraits` — every applicant/colonist trait generation, runs constantly) and Data\TraitPreset.lua:748 (Youth age-transition apply_func, playground bonus trait). Neither is gated; the defective *branch* (the missing tech) matters only once GeneForging is researched.
- Precondition & player path: GeneForging is a **Storybits-field tech** unlocked only by the NewHorizons storybit (Data\StoryBit\NewHorizons.lua): prerequisites GeneSelection breakthrough researched + a Biorobotics Workshop built (Creative Biorobotics, ordinary Biotech tree tech, TechPreset.lua:1958-1967) + not on Asteroid, trigger after founder stage; and the reply that unlocks the tech ("We will research their idea further") carries `IsCommander "author"` — the **Futurist** commander profile (CommanderProfilePreset.lua:293-299), selectable at New Game (and forced by several shipped Challenges, Challenge.lua:11,86,338,778). Then the player must still research the discovered tech (10,000 RP).
- Searched: whole-tree grep of `GeneForging` (TechPreset + NewHorizons.lua only) and of `GetRareTraitChance` (2 callers).
- Tier: R2 — a long but fully-shipped chain: Futurist commander + GeneSelection breakthrough + Biorobotics Workshop + storybit roll + research; every step is a normal player action.
- Recommendation: keep — a tech the game lets the player pay 10,000 RP for and then ignores is exactly the class of defect worth carrying.
- Notes: PT-29's PASS used console reads with force-researched techs — it validates the fix's arithmetic, not by-play reachability; the Futurist-only reply gate is not recorded in the BUGS entry (:982-995) and is the strongest reachability constraint.

### F75 — Six Last Transmission storage opinions never count; one reads the wrong grid
- Module: Code/Fix_LastTransmissionStorage.lua | Technique: §1.1 data-patch | Provenance: source-diff — found while implementing F22; sibling-property comparison within the same file
- Defect: six likes in Data\FactionDef\LastTransmission.lua:94-192 put their condition on `Prerequisite` instead of `Condition`, so `FactionLikeGlobalCondition:Eval` (ClassDef-Factions.generated.lua:843-849) returns 0 forever; `TLEOxygenStorage2Sols` additionally measures Power (GridType default).
- Call sites: the consumer is `FactionsHolder:RecalcFactionsApproval` (Factions.lua:640-662), which runs `EvalApproval` over every FactionDef preset — hourly via `OnMsg.NewHour` (:690-697) and in the daily `FactionsUpdate` (:664-677) — in every game where NoPolitics is not active. Unconditionally live as code; the question is when the result is player-visible.
- Precondition & player path: politics is on by default (NoPolitics is an opt-in rule). Last Transmission Evangelicals is a base-game FactionDef, group "Martian" (LastTransmission.lua:11-19) — not a sponsor faction, so it enters the visible game after the Martian Assembly stage: `IsSponsorFactions()` is true only until the Martian Assembly building exists (Legislature.lua:651-653); afterwards active factions come from colonist support (Factions.lua:508-540) and Martian factions gain supporters via laws/assembly-choice standings (Factions.lua:18-48). A normal long campaign that pursues the Martian-politics arc gets Last Transmission active, at which point six of its approval goals silently contribute nothing and the goal display behaves perversely (shown as unmet while met — BUGS.md:2609-2613).
- Searched: activation logic (ElectMembers sponsor branch :655-707 — only `MissionSponsors[].faction` Earth factions get early seats); the hourly EvalApproval loop; confirmed LastTransmission ships in base Data\FactionDef, not the "thomas" DLC folder.
- Tier: R2 — base-game content, no rule or DLC needed, but it requires reaching the Martian-faction stage of the political campaign with politics enabled.
- Recommendation: keep — a third of one faction's entire approval system is inert; the data patch is minimal and self-deactivating on a game hotfix.
- Notes: the defective `Eval` calls actually execute hourly in every non-NoPolitics colony from sol 1 (the whole-preset loop), so any future patch that surfaces all-faction approval earlier would promote this toward R1.

## Latent / data / tech — the priority batch (F03+pass, F18, F22, F25, F27, F28, F35 pass, F43)

### F03 — Upgrade buffs leak & stack after salvage/demolish
- Module: Code/Fix_UpgradeModifierLeak.lua | Technique: §1.5 replacement (one 7-line method, modeled on its adjacent twin) | Provenance: source-diff — "its twin ApplyUpgradeModifiers iterates correctly" sibling tell, later confirmed in play (PT-02)
- Defect: Building:StopUpgradeModifiers (Building.lua:1268-1274) — iterates the string-keyed `upgrade_modifiers` table with ipairs, so TurnOff() never runs and dome/colony-targeted upgrade modifiers outlive the building.
- Call sites: 2 in Src: Building.lua:510 (Building:Done — LIVE: every salvage, demolish, and disaster destruction of any building) and Building.lua:675 (Building:SetDome — LIVE: building leaving its dome). HasConsumption.lua:407/:496 and Building.lua:1084/:1223 call the different, correct StopUpgradeModifiersForUpgrade — excluded as not this function.
- Precondition & player path: build any building whose upgrade targets another container — confirmed in shipped data: Medical Center "Holographic Scanner" has `'upgrade1_mod_target_1', "parent_dome"` (Data\BuildingTemplate\MedicalCenter.lua:15-19); ApplyUpgrade mints a LabelModifier on the dome (Building.lua:1152-1163) — then salvage it (or lose it to a meteor). PT-02 (docs\PLAYTEST_ARCHIVE.md:169-195) reproduced the leak and the fix BY PLAYING the build→upgrade→salvage→rebuild cycle; cheats were used only to accelerate funding/research.
- Searched: full-tree grep for StopUpgradeModifiers; MedicalCenter template data; ApplyUpgrade id-minting code.
- Tier: R1 — ordinary play (salvaging or losing any upgraded building with dome/colony-target modifiers) executes the broken body directly.
- Recommendation: keep — direct playtest proof of reachability; the §1.5 cost is a 7-line method with a correct sibling to diff against.

### F03 (sanitizer pass) — leaked upgrade modifiers already baked into a save
- Module: Code/90_SaveSanitizer.lua (sweep_leaked_upgrade_modifiers, :128-178) | Technique: §1.2/§1.3 additive PostLoadGame handler doing conservative table surgery | Provenance: source-diff — follow-on cleanup for F03's proven live defect
- Defect: same as F03; this pass removes LabelModifiers whose minted id `"%d+_upgrade%d+_mod_%d+"` (Building.lua:1155) names a handle that no longer resolves to a live object.
- Call sites: n/a (repair pass) — runs from OnMsg.PostLoadGame on every load, on UIColony, every city, and every dome (the three ApplyUpgrade targets, Building.lua:1152).
- Precondition & player path: a save from vanilla (or pre-pack) play in which an upgraded building with dome/colony-target modifiers was salvaged or destroyed. Since the live defect is R1, any mid-campaign adopter who ever salvaged an upgraded Medical Center / Hospital / Ancient Artifact Interface — or lost one to a disaster — carries the state.
- Searched: verified nothing else in Src writes ids of that shape (grep for `_upgrade.*_mod_` pattern usage — only Building.lua:1155 mints it); verified LabelModifier:TurnOff is the only remover per BUGS entry and the sweep's positive-identification gate.
- Tier: R2 — needs a pre-fix save, but ordinary vanilla play produces that save; this is exactly the population the pack targets.
- Recommendation: keep — cheap, idempotent, conservative (leaves any resolving handle alone); it is the half of F03 that helps adopters rather than only new play.

### F18 — Independence terraforming tech gives 10% not 20%
- Module: Code/Fix_IndependenceTerraforming.lua | Technique: §1.1 data patch + LoadGame sweep for already-researched saves | Provenance: source-diff — the tech's own param1=20 vs Amount=-10, with four sibling Independence techs agreeing with themselves
- Defect: Data\TechPreset.lua:4798-4812 — `Independence_TerraformingProjects` declares a 20% discount (param1) but its Effect_ModifyLabel carries Amount -10 on Consts.SpecialProjectResourcesModifier.
- Call sites: consumption is MarsSpecialProject:GetRocketResources (SpecialProjects.lua:95-109, the modifier read at :98/:105) — LIVE once the tech is researched; applied at research time via Effect_ModifyLabel:OnApplyEffect (MarsGameEffects.lua:161-178). No other consumer of SpecialProjectResourcesModifier found.
- Precondition & player path: complete the Martian Independence arc — all IndependenceProgress stages (founder stage, 50 colonists, Assembly, "Path to Independence" law, sponsor goals, payment) → UnlockIndependenceTechs() discovers the five Independence techs (Factions\Independence.lua:111-121, :136-138) → research Independence_TerraformingProjects → launch any terraforming special project → rocket resource cost is discounted 10% where the tooltip's param says 20%. The GreenNOW and GreenMarsCoalition factions even carry FactionTaskTechStatus tasks pointing the player at this exact tech (Data\FactionDef\GreenNOW.lua:438-441, GreenMarsCoalition.lua:564).
- Searched: full-Src grep for Independence_TerraformingProjects (grant path, faction tasks); Independence.lua for the unlock trigger; NoTerraforming rule excludes the tech (Independence.lua:23-32).
- Tier: R2 — a genuine, guided late-game arc: independence + one research + one special project. Excluded only by the NoTerraforming game rule.
- Recommendation: keep — cheap §1.1 preset patch that self-deactivates if a hotfix lands; the sweep is state-gated and idempotent.
- Notes: the framing "Independence sponsor" is imprecise — this is the independence storyline/faction system, not a mission sponsor.

### F22 — `GetGridGlobalStorage` breaks Last Transmission gates
- Module: Code/Fix_GridGlobalStorage.lua | Technique: §1.4b global-function replacement | Provenance: source-diff — sentinel/sum-of-ratios analysis
- Defect: GetGridGlobalStorage (ResourceOverview.lua:891-899) — sums two per-map ratios and lets a zero-demand map contribute the 1000-hour (~41 sol) sentinel from GetGridGlobalStorageInSols (:885-887), so `> 2 sols` is permanently true and `== 0` permanently false once UndergroundMap exists.
- Call sites: 7 in Src: six generated condition closures in Data\FactionDef\LastTransmission.lua:103, :118, :135, :151, :169, :184 — ALL LIVE: FactionsHolder:RecalcFactionsApproval runs `ForEachPreset("FactionDef", ...)` over every faction including LastTransmission and evaluates each like via FactionDef:EvalApproval (Factions.lua:639-660; ClassDef-Factions.generated.lua:165-195), called every game hour by OnMsg.NewHour (Factions.lua:690-697), gated only by the NoPolitics game rule; plus the ScriptCheckGridGlobalStorage code template (ClassDef-Conditions.generated.lua:2040) — eliminated as a direct site (codegen, its only shipped instantiations are the six above).
- Precondition & player path: none needed beyond starting a normal game. The Underground map is generated at new-game map generation for every surface game (RandomMapGenerator.lua:819-820 → GenerateAdditionalMaps → RandomMapGenerator_Picard.lua:263-292), skipped only by the NoUndergroundAndAsteroids rule — so UndergroundMap is truthy from sol 1, its empty city has required==0, and every hourly faction-approval recalculation feeds the corrupted number into Last Transmission's approval, polarization, tension, and "How to achieve" goals.
- Searched: full-Src grep for GetGridGlobalStorage (all callers); GenerateAdditionalMaps callers; faction evaluation loop and its NoPolitics gate; FactionDef LastTransmission preset. PT-42 exists but is UNRUN (blank result lines, PLAYTEST_CHECKLIST.md:800-832) — this verdict rests on source, not playtest.
- Tier: R1 — the broken function executes hourly in every game with default rules; the player-visible corruption (Last Transmission goals/approval) is part of the standard politics feature.
- Recommendation: keep — the §1.4b replacement is small, input-aggregating, and the shipped callers resolve the global at call time.
- Notes: confirmed en route that LastTransmission's "Oxygen for more than 2 sols" like tests **Power** (LastTransmission.lua:169) — the independent defect BUGS.md files as F75. STATUS/BUGS could upgrade F22's justification: reachability is stronger than the entry implies (UndergroundMap exists from game start, not "once the player opens the Underground").

### F25 — Tech description names wrong building (pre-1.0.6 saves only)
- Module: Code/Fix_TechDescriptionBuilding.lua | Technique: §1.1 data patch (same-translation-id T replacement) | Provenance: source-diff — display_name, unlock effect, buildinginfo tag, and sentence all agree against the one wrong bolded name
- Defect: Data\TechPreset.lua:1484-1493 — the `UndergroundLargeDome` preset (display_name "Underground Medium Dome") describes its unlock as "Jumbo Cave Reinforcements" while unlocking UndergroundDomeMedium.
- Call sites: n/a (data) — the description renders wherever the tech appears in the research UI; gating is the preset's `condition = function(self) return not UndergroundRework106 end` (:1485), consumed via Research:TechAvailableCondition (Research.lua:165-168).
- Precondition & player path: the defective text IS in the current shipped Data\TechPreset.lua — the latent classification is not wrong about the data, but about visibility: `UndergroundRework106` is a persisted GameVar defaulting false and set true only on OnMsg.NewGame (UndergroundDome.lua:16-19), so every game started on ≥1.0.6 excludes the tech from the tree, while a save started pre-1.0.6 keeps the var false forever and shows the tech — with the wrong description — when loaded in the current build. Player path: continue any pre-1.0.6 campaign.
- Searched: all five UndergroundRework106-conditioned presets (TechPreset.lua:1485, :3186, :3255, :3286, :3309); the GameVar's only assignment site; TechAvailableCondition consumption.
- Tier: R2 — legacy-save-only, which is a genuine player condition (the tiers list "legacy save" under R2 explicitly); "pre-1.0.6 saves only" is CONFIRMED, but that is R2-conditional, not unreachable.
- Recommendation: keep — cheapest technique in the pack, localisation-safe, self-declining.
- Notes: STATUS.md's "its probe SKIPs on a current build" is worth a re-check: the preset (and thus TechDef.UndergroundLargeDome) is placed unconditionally by Data, so patch() should find the tech table and the wrong literal even on a current build — the condition gates tree membership, not preset existence. Low stakes, but the stated SKIP reason "tech not present (post-1.0.6 save)" may be mislabeled.

### F27 — Storage charge/discharge rate modifiers ignored (latent)
- Module: Code/Fix_StorageRateModifiers.lua | Technique: §1.4 chained post-wrappers (x3 classes, independent) | Provenance: source-diff — handler listens for four props, copies only two ("dead validation" shape)
- Defect: ElectricityStorage:OnModifiableValueChanged (ElectricityStorage.lua:47-63), WaterStorage:… (LifeSupportStorage.lua:25-42), AirStorage:… (:131-148) — each fires for the rate props but never copies them to element.max_charge/max_discharge, which the grid reads every tick (SupplyGrid.lua:167-168; seeded once at NewSupplyGridStorage, :64-76).
- Call sites: the three methods are invoked from the Modifiable machinery (Modifiers.lua:84 and :126) whenever any modifier or SetBase changes a property — LIVE in shipped play for capacity/efficiency (e.g. tank-label techs, TechPreset.lua:2221-2231); the defective BRANCH (prop == a rate) requires a rate modifier, and no shipped source exists.
- Precondition & player path: none in the shipped game. A modifier targeting max_electricity_charge/discharge or the water/air equivalents would have to come from a tech effect, law, story bit, or cheat — none does.
- Searched: full-Src grep for all six rate property names — every hit is the class property declaration, template base values (AtomicBattery, Battery_WaterFuelCell, OxygenTank[_Large], [Large]WaterTank), creation-time seeding, UI max-output strings, and ResourceOverview discharge sums (:458, :468); no Effect_ModifyLabel, SetLabelModifier, ObjectModifier, story bit, or Cheats.lua path touches them. (ArtificialSun.lua:5 declares its own unrelated max_water_charge on a non-storage class.)
- Tier: R3 — the surrounding handler runs constantly in real play; one shipped data row (an Effect_ModifyLabel with a rate Prop) or any mod/DLC modifier makes the missing branch live immediately.
- Recommendation: keep — textbook R3-with-cheap-patch: three no-op-unless-triggered chained wrappers, no replacement cost.
- Notes: only ElectricityStorage's rate props carry `modifiable = true` (ElectricityStorage.lua:11-12); the water/air rate props do not (LifeSupportStorage.lua:9-10, :114-115) — though the modifier machinery fires OnModifiableValueChanged regardless of the flag, so the wrapper's coverage of all three is still right.

### F28 — `Research:ReplaceTech` mishandles the field counter (latent)
- Module: Code/Fix_ReplaceTechCount.lua | Technique: §1.5 full replacement (37-line method copy, one line corrected, asserts rationalized) | Provenance: source-diff — `next(<comparison>)` vs the correct shape in Research:SetTechUndiscovered (:246-249)
- Defect: Research:ReplaceTech (Research.lua:715) — `if not next(g_TechFieldResearchedCount[field_id] == 0)` hands next() a boolean; either the call raises before SetTechResearched or the field counter is dropped while researched techs remain.
- Call sites: 0 in Src. Full-tree grep (Lua, Data, CommonLua, DLC) for "ReplaceTech" returns exactly one hit — the definition at Research.lua:684. That textual sweep also covers OmegaTelescope, story bits (embedded Lua in Data presets is plain text), sponsor perks, Cheats.lua, and generated ClassDefs: none call it.
- Precondition & player path: none exists. The function is only reachable from mod code or the console, both excluded by the audit's criterion.
- Searched: whole-Src grep for the name (any textual occurrence would catch data-embedded script, codegen templates, and dynamic-dispatch strings); confirmed the Src root contains Lua, Data, CommonLua, and DLC, all covered.
- Tier: R4 — no shipped code or data path invokes the function; unlike F27 this cannot go live by data alone, it needs new calling code.
- Recommendation: DELETE-candidate — flag for the user: zero benefit in unmodded play against a §1.5 full replacement carrying per-update re-verification cost; the counter-argument is the pack's own precedent of shipping mod-facing latents (F29), but those were small overrides, not function copies. If kept, keep for the mod-ecosystem rationale explicitly, not for players.
- Notes: STATUS.md's "latent, mod-facing" is confirmed accurate; the QA-added `if not tech_def then return end` guard is likewise only exercisable by a mod caller.

### F35 (sanitizer pass) — Large Wind Turbine buff lost in old saves
- Module: Code/90_SaveSanitizer.lua (repair_turbine_buff, :59-108) | Technique: §1.2/§1.3 additive PostLoadGame handler, preset-driven label surgery | Provenance: mixed — player report ("polymer upgrade works now, frictionless doesn't") plus source diff of the fixup against the tech's three effects
- Defect: SavegameFixups.WindTurbine_Large_ReapplyModifiers (WindTurbine.lua:78-88) — re-applies only the WindTurbine_Diffuser label, while the current tech grants all three of WindTurbine / WindTurbine_Large / WindTurbine_Diffuser at +100% electricity_production (Data\TechPreset.lua:796-821, verified: three Effect_ModifyLabel entries, Percent 100); the three labels are disjoint per Building:AddToCityLabels (Building.lua:427-443).
- Call sites: n/a (savegame fixup) — the shipped fixup runs exactly once, on the first load of any save predating its registration; the sanitizer pass runs on every PostLoadGame after fixups (CommonLua\Savegame.lua:810-813 ordering).
- Precondition & player path: a save that researched the FrictionlessComposites breakthrough in a build whose tech data was broken, later loaded in the current build. The save-vintage cannot be dated from Src alone, but two independent proofs establish the population exists: the devs shipped a migration fixup specifically for these saves, and the pack's originating player report describes exactly the residual symptom the fixup leaves (Large turbines unbuffed). Note this is F35's OWN vintage — "before the FrictionlessComposites data correction" — distinct from F25's pre-1.0.6 gate; the two should not be conflated in STATUS.md.
- Searched: WindTurbine.lua fixup body; TechPreset.lua current effects; AddToCityLabels label disjointness; Savegame.lua fixup ordering.
- Tier: R2 — legacy-save condition with in-the-wild evidence; once loaded, the damage is permanent for that campaign without this pass.
- Recommendation: keep — conservative ("any percent modifier present → skip"), idempotent, preset-driven so a game update retunes it automatically; this is the pass with the strongest player-report backing in the batch.

### F43 — Layout construction bypasses tech locks
- Module: Code/Fix_LayoutTechLock.lua | Technique: §1.4 chained post-wrapper on Activate | Provenance: source-diff — tech_enabled computed then consulted only through the narrow require_prefab case ("dead validation")
- Defect: LayoutConstructionController:Activate (LayoutConstruction.lua:231-252, decision at :238-242) — a tech-locked entry whose template lacks a usable resupply prefab item falls through `add = not require_prefab or self.prefab` into add = true, placing it with no research gate.
- Call sites: 1 shipped trigger: placing the SelfSufficientDome layout building (Data\BuildingTemplate\SelfSufficientDome.lua:16, object_class LayoutConstructionBuilding, build menu "Domes") activates the one populated LayoutConstruction preset (Data\LayoutConstruction.lua:3-54; the second preset "testing", :56-59, is empty and referenced by no template — inert). Per-entry verdicts: DomeBasic, MOXIE, OxygenTank, WaterTank, StorageFood, 2x life_support_grid — eliminated, no BuildingTechRequirements rows anywhere (writers enumerated: Tech.lua:133/MarsGameEffects.lua:39-42 from Effect_TechUnlockBuilding, RoverBuilding.lua:35-36 rover classes only, Station.lua:1317 StationBig only; no Effect_TechUnlockBuilding names any of these five). MoistureVaporator (2 entries) — tech-locked behind MoistureFarming (Data\TechPreset.lua:2038-2045) but ELIMINATED from the defect branch: its template has `require_prefab = true` (Data\BuildingTemplate\MoistureVaporator.lua:11) and its cargo item (Data\Cargo.lua:334-343) ships with no `locked` flag, no verifier, and no sponsor lock (all lock_nameN rows in Data\MissionSponsorPreset.lua cover rovers/drones/Stirling/Seeds only; runtime lock writers are only ResupplyItems.lua:114-126 and the unlock-only MarsGameEffects.lua:339-341), so `require_prefab` evaluates true and the shipped code correctly skips the entry (add = false) — the very case the template's own red hint text describes.
- Precondition & player path: none on shipped data — the defect branch needs a tech-locked entry with a missing or locked resupply item, and the only tech-locked entry always has an unlocked one. Would go live the moment a patch, DLC, or mod ships a layout containing any tech-locked non-prefab building (or locks MoistureVaporator's cargo item).
- Searched: all LayoutConstruction presets in Data and DLC (glob + grep — exactly one file, two presets); every BuildingTechRequirements writer; every Effect_TechUnlockBuilding for the six templates; every resupply lock source (sponsor locks, cargo `locked`, verifiers, runtime assignments); LayoutList references.
- Tier: R3 — the surrounding function runs in ordinary play (Self-Sufficient Dome is a normal early-game purchase); only data stands between the defect branch and live, and the wrapper is a provable no-op on shipped data (locked-out entries are already in skip_items before the wrapper's loop sees controllers).
- Recommendation: keep — cheap chained wrapper, no-op today, exactly the F27-class insurance the pack's policy endorses.
- Notes: correction for BUGS.md:1046-1051 and STATUS.md:126-127 — "none of its entries carries a tech requirement / no tech-locked entry" is factually WRONG: MoistureVaporator IS tech-locked (MoistureFarming). The latent conclusion survives, but on different grounds: the lock is routed into the handled require_prefab branch by an always-unlocked cargo item. The docs should restate the reason. Also the entry counts "seven entries" — the preset has nine (MoistureVaporator and life_support_grid appear twice); seven unique templates.

## UI, drones & buildings (F12-F14, F19, F20, F37, F38, F55, F57, F77)

### F12 — "Low Storage" warning never fires for Food/maintenance resources
- Module: Code/Fix_LowStorageWarning.lua | Technique: §1.5 replacement | Provenance: source-diff — the broken maintenance/food formula was found by contrast with the correct grid-branch formula in the same function (ResourceTracking.lua:247-310).
- Defect: ResourceTracking:GatheredResourcesOnHourlyUpdate (ResourceTracking.lua:211) — un-parenthesized `supply*24/v*24` under truncating `/` yields 0 or ≥24, so the `0 < num_hours < 3` guards for maintenance (:218-224) and Food (:229-234) are unsatisfiable and the warning can never be added.
- Call sites: 1 in Src: City.lua:145 (City:HourlyUpdate) — live, unconditional, every game hour for every city; no guard, class filter, or data gate in between.
- Precondition & player path: colony consumes Food or maintenance resources and stock falls below the 3-sol window — every food or spare-parts shortage in ordinary play hits the dead branch silently. PT-07 (2026-07-27) reached the Food state BY PLAYING (organic depletion and recovery); the Machine Parts case was manufactured via forced malfunction, but the Food half alone proves live reachability.
- Searched: call-site grep of GatheredResourcesOnHourlyUpdate over the whole Src tree (2 hits: definition + City.lua:145); read City:HourlyUpdate for guards (none).
- Tier: R1 — unconditionally executed hourly tick; the defective branches govern a warning every colony relies on.
- Recommendation: keep.
- Notes: the second defect (Food-key collision) is only expressible once the first is fixed; it is a defect of the repaired state, correctly handled inside the same replacement.

### F13 — Command Center resource rows show no numbers
- Module: Code/Fix_CommandCenterNumbers.lua | Technique: §1.3 additive shims (class-table addition, nothing replaced) | Provenance: source-diff — "other call sites were converted, this preset missed" is the remaster-refactor tell.
- Defect: eleven `GetAvailable<Res>` getters referenced by tags like `<metals(AvailableMetals)>` (Data\XDef\CommandCenterCategories.lua:226-328 + generated twin) do not exist; nil renders as an empty row.
- Call sites: the 11 preset tags in Data\XDef\CommandCenterCategories.lua:226-328 and Lua\XDef twin — live whenever the Command Center resource category is open; grep for `GetAvailableMetals|GetAvailableConcrete|GetAvailableFood` over all of Src returns zero definitions, confirming every one of the 11 rows is dead.
- Precondition & player path: open the Command Center and look at the resources page — a UI every player uses. PT-08 PASS 2026-07-27 by playing (all 11 rows cross-checked against the HUD bar).
- Searched: brief — getter-name grep across Src (0 hits) plus tag grep in the preset.
- Tier: R1 — a stock UI panel, no gating condition at all.
- Recommendation: keep.

### F14 — Domes Overview red low-stat highlight dead
- Module: Code/Fix_DomeOverviewHighlight.lua | Technique: §1.5 replacement (13-line method) | Provenance: source-diff — computed `tv` discarded in favor of `v` is a pure code-reading find.
- Defect: Community:UICommandCenterStatUpdate (ColonyControlCenter.lua:1309-1320) — builds the `<red>` text and then calls `win.idLabel:SetText(v)` with the raw value.
- Call sites: 2 in Src (same UI def twice): Data\XDef\CommandCenterDomeOverviewRow.lua:37 and Lua\XDef\CommandCenterDomeOverviewRow.generated.lua:56 — live, context is the dome (a Community), fires for every stat cell of the Domes Overview. The dispatcher at ColonyControlCenter.lua:489-491 and Colonist:UICommandCenterStatUpdate (:510) serve the colonist/tourist rows, not this method.
- Precondition & player path: open Domes Overview with any dome stat below LowStatLevel (30). PT-09 (2026-07-28, by playing) showed the Satisfaction column reads ~0 on every dome of a mature colony (vanilla tourist-stat decay, Colonist.lua:3905-3918), so the should-be-red state exists in essentially every established colony that opens the panel.
- Searched: call-site grep of UICommandCenterStatUpdate across Src (10 hits, triaged above).
- Tier: R1 — stock panel plus a low-stat state PT-09 proved ubiquitous.
- Recommendation: keep.

### F19 — Graphs "Consumed" caption omits maintenance
- Module: Code/Fix_GraphConsumedCaption.lua | Technique: §1.4 post-wrapper | Provenance: source-diff — caption (ColonyControlCenter.lua:180-188) vs plotted series (ResourceTracking.lua:162) comparison.
- Defect: the caption closure built in City:GetColonyStatsButtons (ColonyControlCenter.lua:8, caption :180-188) uses consumption-only while the bar series adds maintenance — the label describes a different quantity than the graph.
- Call sites: 2 in Src (same UI def twice): Data\XDef\CommandCenterColonyStats.lua:80 and Lua\XDef\CommandCenterColonyStats.generated.lua:78 — live whenever the Command Center graphs page is opened.
- Precondition & player path: open the graphs page in any colony with nonzero maintenance consumption of a stockpile resource (Machine Parts/Electronics/Metals/Polymers) — universal past the first domes. PT-43 (2026-07-28, by playing) confirmed both the discrepancy scale and that real Food consumption is unchanged.
- Searched: call-site grep of GetColonyStatsButtons across Src (3 hits: definition + the two UI defs).
- Tier: R1 — stock panel, universally-true data precondition.
- Recommendation: keep.

### F20 — Morale tooltip shows unapplied +Comfort bonus
- Module: Code/Fix_MoraleComfortTooltip.lua | Technique: §1.4 post-wrapper (wraps the installed rollover closure) | Provenance: source-diff — the shipped comment "remove for comfort policy to work" (Colonist.lua:3963-3966) vs the un-updated tooltip loop.
- Defect: the Morale rollover built by Colonist:UIStatUpdate (Colonist.lua:2932, Morale branch :2981-3008) prints a bonus row for any stat `>= high`, including Comfort, whose high-stat bonus UpdateMorale deliberately no longer grants.
- Call sites: 2 in Src (same UI def twice): Data\XDef\ipColonist.lua:134 and Lua\XDef\ipColonist.generated.lua:148 — live for every stat row of every colonist infopanel; the defective row needs Comfort ≥ g_Consts.HighStatLevel = 70 (__const.lua:1478-1484).
- Precondition & player path: select any colonist with Comfort ≥ 70 — routine in any colony with decent housing and services. PT-43 (2026-07-28): the phantom-row side was verified on a naturally high-Comfort colonist BY PLAYING (rows summed exactly); only the penalty-side non-regression check used a console-driven Comfort-0 colonist.
- Searched: call-site grep of UIStatUpdate across Src; HighStatLevel value in __const.lua.
- Tier: R1 — ordinary infopanel use plus a stat level most colonies reach.
- Recommendation: keep.

### F37 — Ghost farm oxygen survives salvage
- Module: Code/Fix_GhostFarmOxygen.lua | Technique: §1.4 chained pre-wrapper (Building:SetDome) + §1.2 OnMsg.LoadGame sweep | Provenance: source-diff — "no FarmBase:Done / SetDome knows nothing about this modifier" cleanup-audit find; no player report cited.
- Defect: FarmBase:ApplyOxygenProductionMod (Farm.lua:561-571) writes a farm-keyed negative air_consumption modifier on the parent dome; no removal path clears it when the farm is removed, and every shipped crop carries OxygenProduction ≥ 100 (Data\CropPreset.lua:12 ff.), so any planted in-dome farm has one.
- Call sites: 3 in Src for the modifier writer: Farm.lua:122 (FarmBase:OnSetWorking — live, both edges) | Farm.lua:557 (PlantNextCrop — live; runs at GameInit :95, on SetCrop :618-620 and the harvest cycle :285/:315, with NO working-state gate) | Farm.lua:575 (OnModifiableValueChanged "oxygen_production_efficiency" — latent, no shipped modifier targets that property).
- Precondition & player path: remove an in-dome farm whose modifier was applied while the farm was NOT working. Concretely: a farm's default crop is planted the moment construction completes (GameInit, Farm.lua:84-96 → :557 applies the modifier immediately, workers or not); salvage that farm before it ever works — e.g. the common "misplaced building, undo it" move — and no working true→false edge ever fires, so the modifier survives Destroy, and rubble-clear (Done → SetDome(false)) orphans it forever. Same for a crop change (SetCrop, :602-624) made while the farm is off, followed by salvage while still off. Each rebuild gets a new farm_id, so phantoms accumulate.
- Searched: traced the working-farm salvage path: Building:Destroy sets destroyed=true (:1473) then UpdateWorking(false) (:1483) → CanWork false via "Destroyed" (Building.lua:602-604) → SetWorking edge (BaseBuilding.lua:179-180) → OnSetWorking(false) → Farm.lua:122 clears the modifier — so the working-farm case self-cleans; also grepped use_demolished_state (farm templates inherit the Building default TRUE, Building.lua:210) and oxygen_production_efficiency modifiers (none shipped).
- Tier: R2 — reachable through a genuine, fairly ordinary sequence (salvage a farm during a not-working window, most simply right after construction), but not the every-salvage leak the header describes.
- Recommendation: keep — the leak is permanent and cumulative when hit, the hook is idle otherwise, and the LoadGame sweep repairs old saves.
- Notes: stale evidence in the fix header/BUGS entry — the claim "the demolish path skips UpdateWorking(false) for buildings without a demolished state" does not apply to shipped farms (no farm template or class sets use_demolished_state; Building's default is true), so a WORKING farm's salvage/meteor destruction does clear the modifier via the Destroyed working-edge. The fix remains correct; only the stated frequency ("every rebuild adds another") is overstated for the common case. Worth a one-line correction on the F37 entry.

### F38 — Destroyed tunnels rejoin pathfinding after load
- Module: Code/Fix_DestroyedTunnels.lua | Technique: §1.4 chained pre-wrapper (TunnelBase:AddPFTunnel) + §1.2 OnMsg.LoadGame sweep | Provenance: source-diff — "re-adds ... with no destroyed test" sweep-audit find.
- Defect: OnMsg.LoadGame (Tunnel.lua:264-266) re-registers PF tunnels for ALL TunnelBase; AddPFTunnel (:197-209) checks only IsValid(linked_obj), and a destroyed tunnel is a valid ruin.
- Call sites: 2 in Src reach TunnelBase:AddPFTunnel: Tunnel.lua:85 (GameInit Notify — legitimate, new tunnels; wrapper passes it through) | Tunnel.lua:265 (LoadGame sweep — the defective caller, live on every save load). The generic PFTunnel LoadGame sweep (CommonLua\Movable.lua:623-625) does NOT hit tunnels — TunnelBase is not a PFTunnel (Tunnel.lua:5-6; contrast Dome_Entrance.lua:6).
- Precondition & player path: a tunnel in the `destroyed` ruin state at save time, then load. What destroys tunnels in play: (1) a large meteor — BaseMeteorLarge:Explode destroys any Building except Dome/ConstructionSite in its query area (Meteors.lua:817-824 → DestroyBuildingImmediate → DoDemolish → Building:Destroy; the Tunnel template is not indestructible and inherits use_demolished_state=true, so it becomes a ruin); meteors are on under default disaster settings. (2) Player salvage of a tunnel takes the same DoDemolish → Destroy path and also leaves a destroyed ruin until the wreckage is cleared or rebuilt. Both then need only an ordinary save/load — the ruin persists indefinitely (Rebuild is a manual action; auto-clear needs the DecommissionProtocol tech, Building.lua:879-881), so the save-in-window is easy to hit.
- Searched: grep of AddPFTunnel across Src (all 25 hits triaged — Passage/Dome_Entrance/TunnelMarker are separate classes); grep of DestroyBuildingImmediate callers (meteors, dome death, defence-tower misses, drone explosion); indestructible/use_demolished_state defaults (Building.lua:209-210) vs the Tunnel template.
- Tier: R2 — needs a destroyed tunnel (meteor hit or player salvage, both named and routine) plus a save/load; both are ordinary play for anyone who builds tunnels.
- Recommendation: keep.

### F55 — Drone unreachable-forever cache
- Module: Code/Fix_DroneUnreachableForever.lua | Technique: §1.5 replacement (31-line method) | Provenance: player-report — "late-game drones stop maintaining buildings and cluster outside," BUGS marks it "matches report exactly."
- Defect: Drone:ApproachWrapper (Drone.lua:819-849) stores a failed approach as `GameTime() + max_int` (:840), which the shipped 5-sol expiry in CleanUnreachables (:879-896, const at :868) can never retire.
- Call sites: 4 in Src, all live core drone commands with no gate before the defective branch: Drone.lua:920 (Drone:Work) | :972 (Drone:PickUp, load leg) | :1239 (deliver retry loop) | :1325 (Drone:EmergencyPower recharger approach). The defective line executes whenever `ExitHolder and building:DroneApproach` fails — i.e., any pathfinding failure (TaskRequester:DroneApproach is just GotoBuildingSpot, _TaskRequest.lua:234-236).
- Precondition & player path: any drone ever failing to path to a task target — construction site placed beyond a cliff before its ramp/tunnel exists, a blocked dome entrance, transient obstruction. The shipped expiry mechanism plus eviction cap are themselves evidence the developers expected failures routinely; the only shipped resets are BumpDroneUnreachablesVersion from landscaping completion (Landscaping.lua:326) and a Building.lua:523 site — not per-passability-change, so "forever" really holds between those events. Status is `fixed*`, no PT — reachability rests on the matching player report plus the ubiquitous call sites.
- Searched: call-site grep of ApproachWrapper (5 hits, 1 definition); grep of g_DroneUnreachablesVersion/BumpDroneUnreachablesVersion to check how often the shipped escape fires.
- Tier: R1 — every colony's drones run these commands constantly and approach failures are ordinary; the live report matches the mechanism exactly.
- Recommendation: keep.
- Notes: per assignment, the entry's other half (open-air dome entrance attaches) was ruled not actionable and is not in this module; nothing in this audit disturbs that.

### F57 — Drone/transport minors bundle (a: rocket fuel restrictor; b: passability-change table corruption)
- Module: Code/Fix_DroneTransportMinors.lua | Technique: (b) §1.2 additive OnMsg + (a) §1.5 replacement (27-line method) | Provenance: source-diff — wave-5 screening bundle; (a)'s latency was established by data grep, (c) deliberately unfixed.
- Defect: (b) OnMsg.OnPassabilityChanged (Drone.lua:851-864) swaps in a plain `{}` per drone — weak-keys metatable lost, unreachable_buildings_count never recomputed. (a) DroneControl:UpdateRocketsInternal (DroneControl.lua:613-639) clears only the literal "Fuel" key while the UniversalRocketBase branch writes `r_t[r.FuelResource]` (:632-634).
- Call sites: (b) the handler is invoked by the engine-broadcast OnPassabilityChanged message — no Lua `Msg(...)` raise exists (grep: 0 hits), but pass-edit brackets pervade gameplay code (55 ResumePassEdits sites across 32 files) and sibling handlers (Landscaping.lua:91, Flight.lua:1330, Pass.lua:7/42) exist precisely because it fires in play. (a) UpdateRocketsInternal is called from the hub update loop (DroneControl.lua:566 via UpdateRockets :576, :652, :657) — live routinely, but the defective key mismatch requires `FuelResource ~= "Fuel"`.
- Precondition & player path: (b) any past failed drone approach (creates the table — see F55, ordinary) followed by any passability change (construction/demolition/meteor/landscaping — many per sol). The copied table keeps its `version` key (string keys survive the map filter: ResolveMap("version") is nil → kept), so CleanUnreachables' version check does NOT self-heal it; drones whose table was still `false` get a versionless `{}` and DO self-heal at the next CleanUnreachables — the lasting corruption targets exactly the drones with real entries. (a) no shipped data sets FuelResource: it is a template property defaulting to "Fuel" (UniversalRocket.lua:47) and a full-Src grep shows reads only, no template assignment — the branch never diverges in the shipped game.
- Searched: Msg("OnPassabilityChanged") raise grep (0 — engine-side), ResumePassEdits count, FuelResource grep across Src (30 hits, all reads + the default-"Fuel" declaration).
- Tier: R1 — carried by (b), whose two preconditions are both ordinary-play staples; (a) alone is R3.
- Recommendation: keep; flag (a) as §1.5-latent (R3 — goes live only if a patch or mod ships a rocket with a non-"Fuel" FuelResource, the stated F27/F28 rationale).
- Notes: the self-heal asymmetry above (versionless fresh tables reset cleanly; populated tables never do) is a small sharpening of the BUGS entry, not a contradiction.

### F77 — Extender working-flap tears down and rebuilds the whole uplink hub
- Module: Code/Fix_ExtenderFlapChurn.lua | Technique: §1.4 chained wrapper (debounce + coalesce) | Provenance: mixed — source trace built to explain a live 2026-07-27 player report (drones dropping to Idle, degraded throughput); a co-existing mechanism is acknowledged.
- Defect: DroneHubExtenderBase:OnSetWorking (DroneHubExtender.lua:171-178) calls UpdateUplinkRequesters (:109-112) on EVERY working edge, both directions; that is a full uplink DisconnectTaskRequesters + ConnectTaskRequesters (DroneControl.lua:441-450, :327-360), each removal kicking every en-route drone of the whole hub to Idle (OnRemoveBuilding :720-729).
- Call sites: 3 in Src, all on the wrapped method: DroneHubExtender.lua:175 (OnSetWorking — the flap surface, live on every power/malfunction/toggle edge) | :144 (Unlink) and :153 (Link) — live but one-shot at uplink changes; all three funnel into the same whole-hub rebuild, and all are covered by the wrapper. The rebuild only reaches a hub when the extender has a valid uplink (:115, :121) — which a functioning extender always has (SignNoConnection otherwise, :167).
- Precondition & player path: build a Drone Hub Extender — a stock base-game build-menu building (build_category "DroneHubs", DroneHubExtender.generated.lua:22-24; also orderable as rocket cargo, Data\Cargo.lua:704-707) — linked to a hub with drones. Flap sources in ordinary play: it consumes 2000 power (template :38) so dust-storm battery brownouts and the dust-storm cable-break tick (City:RandomBreakSupplyGrid, City.lua:148-150) cut it; it takes Electronics maintenance (template :17) so routine malfunction/repair cycles toggle it; manual on/off does too. Each blip = two full teardown/rebuild cycles per extender.
- Searched: call-site grep of UpdateUplinkRequesters (4 hits, 1 definition); template for build-menu availability and consumption/maintenance data.
- Tier: R2 — needs the player to build extenders (optional but common infrastructure); once one exists, routine power/maintenance events exercise the defect constantly, in exactly the big-colony scenarios the report describes.
- Recommendation: keep — PT still pending per the entry; that playtest, not reachability, is the open question.
- Notes: even a single working transition (first power-up, one malfunction) executes the defective full-rebuild path; the debounce also coalesces the Link/Unlink sites, which is behaviorally fine since ConnectTaskRequesters reads current topology at fire time.

---

## Proposed FIX_POLICY §4 amendment (draft — not applied; user go-ahead required)

**SUPERSEDED — the Challenge review 2026-07-30 (end of this file) revises this
draft to also require a positive intent statement and the tier `I` vocabulary.
Use that version.** Original draft kept for the record:

Replace the current §4 ("Only fix proven defects") with:

> ## 4. Only fix proven, reachable defects
>
> Every fix links to a BUGS.md entry with file:line evidence **and a recorded
> reachability verdict**. Before a fix ships:
>
> - **Enumerate every call site** of the defective function in Src; eliminate
>   the ones that cannot execute the defective body (class chain, guards,
>   early returns, template data); for each survivor **name the concrete
>   player action** that produces the precondition — a building, a game rule,
>   a sponsor, a mystery, a disaster, a milestone, a map path, a savegame
>   fixup.
> - **Record a tier on the BUGS entry:** R1 live · R2 conditional · R3
>   latent-by-data · R4 unreachable · U unknown (naming the observation that
>   would settle it).
> - R1/R2 ship normally. **R3 ships only as a §1.1–§1.4 patch** (data patch,
>   additive handler, registry surgery, chained wrapper); an R3 §1.5 full
>   replacement needs an explicit user decision (latent benefit, permanent
>   maintenance cost — the F24 lesson). **R4 does not ship**; record the
>   defect in BUGS.md as `wontfix — unreachable` with the search that proved
>   it. **U ships only with the settling observation queued** as a playtest
>   item.
> - A `tested` status proves reachability only if the playtest reached the
>   state **by playing**; console surgery, `g_Consts` compression or `Cheat*`
>   calls prove the fix, not the path.
> - A state producible **only by console/debug injection is evidence for R4**,
>   never a demonstration of reachability (the PT-46 track-injection lesson).
> - No balance changes, no "improvements", no opinions — those belong in
>   other mods. When intent is ambiguous, prefer the reading proven by
>   sibling code in the same file (the F07/F08/F02 pattern).

---

## Findings en route (recorded on the BUGS.md entries, flagged "audit 2026-07-30")

Corrections and sharpenings this audit added to BUGS.md — pointers only, the
substance lives on each entry:

- **F06** — evidence *strengthened*: the Epilogue popup arrives minimized by
  SA default (`start_minimized` true, SequenceAction.lua:207) and does not
  pause the game until opened; the entry's "player can minimise and ignore"
  understates how easily the one-sol window passes.
- **F17 / F40** — the DustSickness storybit family is gated on the
  **Dust in the Wind** game rule (Data\StoryBit\DustSickness.lua:19-21);
  neither entry recorded that gate. F40's "Biorobots breakthrough" is named
  **The Positronic Brain** in shipped data.
- **F22** — reachability is *stronger* than the entry implies: UndergroundMap
  exists from new-game map generation (not "once the player opens the
  Underground"), and the six Last Transmission conditions are evaluated
  hourly from sol 1.
- **F25** — "pre-1.0.6 saves only" confirmed, but the probe's SKIP label
  ("tech not present") may be mislabeled: the preset is placed
  unconditionally; the `UndergroundRework106` condition gates tree
  membership, not preset existence.
- **F34** — the fix title's "boarding colonists" overstates: shipped Lua sets
  "Embark" only on Drones; the protected population is boarding drones plus
  the lost dedup.
- **F37** — the header's "the demolish path skips UpdateWorking(false)" does
  not apply to shipped farms (no farm sets `use_demolished_state` false; a
  WORKING farm's salvage does clear the modifier via the Destroyed
  working-edge). The leak needs a not-working window (most simply: salvage
  before first spin-up). Fix unchanged; frequency claim corrected.
- **F43** — the recorded latency *reason* was wrong: "no tech-locked entry"
  is false — MoistureVaporator IS tech-locked (MoistureFarming). The latent
  conclusion survives on different grounds: its template's
  `require_prefab = true` plus an always-unlocked cargo item route it into
  the branch the shipped code handles.
- **F49** — (a) settled R4 (this file, lead-pass block); the F49 entry's
  "map setup, cheats, the instant-build rule" trigger list is now known to
  contain zero player-reachable members.
- **F74** — PT-39's "rival-colony trade offer" framing conflates rocket
  families: rival trade-pad/foreign-aid rockets are plain `UniversalRocket`
  and were never covered by the shipped guard or by F74; the refused rocket
  must have been a storybit/mystery `UniversalTradeRocket`.
- **F81** — the Capture Meteors POI storm (Data\POI.lua:47-69) strands the
  prediction flag on ANY map, bypassing both the NoDisasters rule and map
  storm settings — a reachability strengthener not in the entry.
- **F11** — settling observation recorded (see its block): crew-gathering a
  busy train passenger and inspecting `train.units` settles U → R2.
- **F81 (rains)** — settling observation recorded (see its block); ~~the
  planned PT-54 leg can carry it~~ → **the F86 Tier-1 `Fix_RainsDeadlock` A/B
  leg carries it (PT-54 retired unrun 2026-08-01).**

---

# Challenge review 2026-07-30

The audit above carried a wrong verdict: **F49(c) was tabled "live R2" and
used to justify keeping its module — it was designed behaviour.** The owner
found it at the keyboard within hours (salvage cursor names its target for
everything on the map; the station↔track handoff is seamless and exact; the
propagation the fix nulled is what MAKES that boundary continuous; the guard,
had it engaged, would have carved a dead band of red `Salvage` into it). F49(c)
is closed `wontfix` by user decision and the guard is removed (`d03417b`).
This section answers the challenge (`AUDIT_CHALLENGE_PROMPT.md`, deleted after
recording): why the method produced a confident wrong answer, what else it did
the same thing to, and what changes.

## 1. The failure mode, stated precisely

Three distinct failures stacked. Each alone would have been survivable;
together they published a wrong verdict in the audit's own showcase module.

**(i) Bundle inheritance.** `Fix_TrainMinors` bundles three lettered items.
The lead reserved the module (pulling it from the tracks sweep), enumerated
(a) exhaustively — and then let (c) and (d) wear tiers derived from nothing
but the module header's own claims. A tier with no enumeration behind it is
not a verdict; it is the fix author's hypothesis wearing the audit's clothes.
Every lettered sub-item of a bundle is a separate audit subject. Enumerating
one third of a module proves nothing about the other two thirds — that is
exactly how this got through, in the one module that got the most attention.

**(ii) The defectiveness presupposition, and why source made it worse, not
better.** Every tier in R1/R2/R3/R4/U grades *how reachable* a defect is. All
five presuppose the shipped behaviour is defective — and the audit never
tested that presupposition; it inherited it from BUGS.md and from fix
headers, which are the *author's* hypothesis about why the code is wrong.
For most of the pack the presupposition is carried by hard evidence (a crash,
a wrong number, dead code). F49(c) had none of those. Its "defect" was a
claim about interface intent — and intent of that shape lives in facts the
Lua does not carry: what the cursor names before the click, how input
resolves to objects, whether two adjacent things are separately addressable
at all. On such a claim, source reading does not return "uncertain." It
returns a **confident wrong answer**, because the code path plainly exists,
plainly executes, and reads exactly like every reachable defect the audit
correctly confirmed. Source evidence is decisive for reachability and
near-mute on intent; a method that grades only reachability will wave
intended behaviour through as a live defect with full confidence, every time
the author's hypothesis was wrong. That is the failure §4 must guard against.

**(iii) The evidence base went stale during the audit itself.** Two commits
landed while the sweeps were running: `c3c4383` (16:34 — PT-46 tail:
F49(d) **PASS by play** on a live 305-sol colony, and an explicit note that
*"F49(c) has no play coverage either"*) and `ba1e88b` (16:50 —
PLAYTEST_HELP salvage-cursor facts, whose reference entry **names F49(c) as
its immediate case**). The audit committed at 17:00 against its session-start
snapshot and never re-read `git log` before publishing. The falsifying
evidence — and the play-proof for (d) that the audit instead asserted — were
both already in the repo when the verdict shipped. The project already owned
this rule ("playtest commits land after docs are written; check git log
first") and the audit applied it to BUGS.md's past, not to its own present.
**Method rule going forward: re-run `git log` between assembling verdicts and
publishing; anything landed mid-run is part of the evidence base.**

## 2. Coverage self-audit — verdicts that had no enumeration of their own

Sweep standard: does a block exist that enumerates *that item's* call sites
and interrogates *its* preconditions? Result over every table row:

- **Enumerated:** every module's primary item received its own block from a
  subsystem sweep, including both halves of the multi-defect modules that
  were audited as pairs (F07+F15, F29 a/b, F53 a/b, F57 a/b, F73 a/b, F81's
  two modules, F12's two formulas, F47's two halves, both sanitizer passes).
- **Unenumerated — tier worn with nothing behind it:** exactly two, both in
  the module the lead kept for itself:
  * **F49(c)** — asserted "live R2" from the module header; never audited;
    wrong. Closed `wontfix` (designed behaviour), guard removed.
  * **F49(d)** — asserted "live R2" from the same header. The tier happens to
    survive its late enumeration (below), and the play-proof was already in
    the repo (`c3c4383`) — which makes the assertion no better as method:
    right by luck plus unread evidence.

The asymmetry the challenge names is real and is now policy (see §4
revision): the original prompt required an R4 to state its search, and let
R1/R2 pass unstated. An unenumerated "keep, it's live" is exactly as
unproven as an unstated R4 and more dangerous, because nobody ever revisits
a keep.

### F49(d) — the late enumeration (module's remaining live justification)

- Defect: `TrackBase:GameInit` (Track.lua:62-67) computes `max_vehicles` from
  the element count once; Track.lua:65 is the ONLY assignment in Src
  (verified: whole-tree grep returns the class default StationsLink.lua:8,
  the read :29, and the one assignment). A partial salvage shortens the
  surviving track, which never re-runs GameInit — the cap stays sized to a
  length the track no longer has (stale-HIGH only; the split-off track
  recomputes correctly via deferred GameInit, the 2026-07-25 QA correction).
- Consumers: `StationsLink:GetMaxVehicles` → `CanAddVehicle`
  (StationsLink.lua:28-34), gating `AddTransportLink` (:36-39) — i.e. how
  many trains the player can assign to the track. Live in all train play.
- Intent: the formula visibly derives the cap from length, and the engine
  recomputes it for the split-off half but not the survivor — an asymmetry
  with no design reading, unlike (c). Intent tell: self-inconsistency.
- Reachability: R2 — train play plus any partial salvage (same entry points
  as F44/F47: TrackElement.lua:259-261, Construction.lua:2911). **Play-proven
  before the audit shipped:** PT-46 tail (`c3c4383`), live colony, els=43
  cap=2 → els=13 cap=1 across a partial salvage under the fix; formula
  spot-checks 43→2, 113→4, 74→2, 13→1, 25→1; reload-stable. The PostLoadGame
  sweep's *repair* of an already-stale save remains unproven (needs a
  fix-vetoed save; TestKit probe queued — recorded honestly in `c3c4383`).
- Verdict: **R2, keep.** The module now ships (a) + (d) after the (c)
  removal; (d) alone carries the keep, with (a) as a cheap no-op rider.

## 3. The source-blind-spot list — verdicts that need eyes, not greps

Every verdict below depends on runtime or interface behaviour source cannot
determine: hit-testing, affordances, cursor/confirmation feedback, engine
placement, visual outcomes. For each, the single observation that settles it.
None of these is currently believed wrong; all of them are believed on
source-shaped evidence that F49(c) just demonstrated can lie.

| Fix | What source cannot see | Settling observation |
|-----|------------------------|----------------------|
| F16 | whether a finished sphere site's actions are truly still offered and clickable in the live infopanel (enabled-state could differ from the IsActionEnabled read) | finish the excavation in a Spheres game; open the site's infopanel; click "Pierce the Shell"; watch whether drones engage a dead request |
| F38 | whether units actually ROUTE through a destroyed tunnel's restored PF shortcut after load, or the engine declines it for other reasons | destroy a tunnel (meteor or salvage), save/load in vanilla, order a colonist/rover across — watch the route |
| F34(d) | whether a mid-"Embark" drone swept by the landscape scatter is visibly yanked/broken or recovers silently | drop a landscape mark over a rocket actively loading drones; watch the boarding drone |
| F74 | the ORIGINAL harm claim — does pushing cargo at an event rocket actually glitch it in vanilla? (PT-39 proved the fix refuses; nobody has observed the vanilla harm) | in vanilla, order an RC Transport onto a landed storybit trade rocket; observe |
| F53(a) | whether a blocked "Colonistout" spot actually strands arrivals at runtime (engine placement/passability at the moment of disembark) | in vanilla, land a passenger rocket flush against a Universal Depot; watch the arrivals |
| F06 | whether the Epilogue really arrives minimized and unpaused on current build (source-read of SA defaults; the pause layer is UI code) | reach the Mystery 10 finale; ignore the corner notification for one sol at fast-forward |
| F26 | the visual claim itself (parallel volley vs jittered spread — cosmetic intent) | watch one Last War volley with the fix off, one with it on |
| F22 | where the corrupted number is player-visible before the Martian Assembly stage | open the Last Transmission faction goals panel in a young politics-enabled colony |
| F77 | the churn's player-visible magnitude (the fix's PT is already pending on the entry) | the queued PT: flap an extender during hub activity; watch fleet Idle-kicks with/without |
| F11 | engine-side `TransferToMap` semantics (already recorded as U) | crew-gather a busy train passenger; inspect `train.units` |
| F81b | the rain deadlock live (already recorded) | blocked `RainsDisasterThreads` activation thread on a vanilla save after a collision, or rain resuming ≤7 sols under the fix |

## 4. The missing tier, reassignments, and the revised §4 amendment

**New tier: `I` — Intentional.** The shipped behaviour is deliberate; the
"defect" is the fix author's misreading; reachability grading is moot (the
behaviour is typically fully reachable — that is what makes the misreading
expensive). A fix against an `I` behaviour fights the design and must not
ship. The project has used this category informally all along — F42, F56,
F62, F63 were closed on exactly these grounds — the audit's vocabulary just
failed to contain it, so nothing prompted the question.

**Reassigned to `I`:** F49(c) (closed `wontfix`, guard removed). Re-scan of
the full table for others: no further reassignments. The re-scan keyed on the
challenge's criterion — src-diff provenance where the "defect" is behaviour a
player must *notice and object to*, with none of the hard tells. Three
entries carry a **flag (intent believed, not proven — tell is soft)** rather
than a reassignment:

- **F59** (freed housing doesn't notify homeless): the organic-vacancy lag
  could be read as deliberate load-shedding; the tell is only the asymmetry
  that every player-caused vacancy gets the fast path. Soft. Observation:
  none crisp short of dev word; the fix is additive and cheap, keep-with-flag.
- **F77** (extender flap rebuilds the hub): the full rebuild is explicitly
  written code, not a slip; the defect claim rests on consequence (Idle-kick
  of unrelated drones) plus the live symptom report. Kicking a fleet off its
  tasks twice per power blip has no plausible design reading, but the tell is
  consequence, not code. The pending PT doubles as the intent observation.
- **F49(d)** (stale cap): intent tell is the recompute asymmetry —
  self-inconsistency, moderate. Play-proof covers the mechanism; flag noted
  in its block above.

Entries whose intent was checked and PASSES on hard tells, for the record:
F26 (dead local — `spawn_dir` computed and discarded), F72 (gate and list
contradict each other), F20 (explicit dev comment), F16/F23/F28/F43/F75
(dead validation), F18/F25 (self-contradiction within one preset), F02/F04/
F07/F08/F12 (sibling contradiction), F36/F51/F52/F55/F78/F81 (player-reported
harm).

### Revised FIX_POLICY §4 amendment (supersedes the draft above) — ✅ **APPLIED 2026-08-01**

**This draft is spent.** The text below was copied verbatim into
`docs/agent/FIX_POLICY.md` §4 on 2026-08-01, replacing the old three-sentence
"Only fix proven defects" rule; **FIX_POLICY is now the authority for it and
this block is only the record of where it came from.** Authority for the
adoption: the owner's blanket pre-clearance (`docs/prompts/project/README.md`),
which removed the approval step for audit-derived items. The blocker that held
it — the draft's "R4 does not ship" against F49(a)'s shipped no-op R4 rider —
died the same day when that guard was stripped from `Fix_TrainMinors` (BUGS
F49). One live consequence recorded on adoption: **F29 and F57(a)** are R3
defects fixed by §1.5 method replacements, which the R3 bullet now makes
conditional on an explicit owner decision; both entries carry it and the
decision is routed, not assumed.

> ## 4. Only fix proven, reachable, UNINTENDED defects
>
> Every fix links to a BUGS.md entry with file:line evidence, **a recorded
> reachability tier, and a positive intent statement**. Before a fix ships:
>
> - **Intent first.** State why the shipped behaviour is unintended, citing
>   at least one hard tell: (1) player-reported harm; (2) dead code / dead
>   validation — a computed value discarded, a guard that cannot fire, a
>   message nothing emits; (3) sibling contradiction — the same author wrote
>   it correctly elsewhere; (4) self-contradiction within one function or
>   preset; (5) an explicit dev comment. **No tell → the defect claim is a
>   hypothesis, and it needs a keyboard observation before any fix is
>   written.** UI/affordance behaviours — anything whose wrongness lives in
>   hit-testing, cursor feedback, input modes, or whether two things are
>   separately addressable — are in this class BY DEFAULT: source reading
>   gives confident answers with no validity there (the F49(c) lesson). A
>   behaviour found intentional is tier **I**: record it, close it, write no
>   fix.
> - **Then reachability.** Enumerate every call site of the defective
>   function in Src; eliminate the ones that cannot execute the defective
>   body (class chain, guards, early returns, template data); for each
>   survivor name the concrete player action that produces the precondition.
>   Record the tier: R1 live · R2 conditional · R3 latent-by-data · R4
>   unreachable · U unknown (naming the observation that would settle it).
> - **Symmetry of proof.** Every tier states its evidence — an unenumerated
>   R1/R2 is exactly as unproven as an unstated R4, and more dangerous,
>   because "keep, it's live" is the verdict nobody revisits. **Every
>   lettered sub-item of a bundled fix is a separate audit subject**;
>   enumerating one item proves nothing about its siblings.
> - R1/R2 ship normally. **R3 ships only as a §1.1–§1.4 patch**; an R3 §1.5
>   full replacement needs an explicit user decision (the F24 lesson). **R4
>   does not ship**; record it `wontfix — unreachable` with the search that
>   proved it. **U ships only with the settling observation queued** as a
>   playtest item.
> - A `tested` status proves reachability only if the playtest reached the
>   state **by playing**; console surgery, `g_Consts` compression or `Cheat*`
>   calls prove the fix, not the path. A state producible **only by
>   console/debug injection is evidence for R4** (the PT-46 track lesson).
> - **Evidence freshness:** re-check `git log` between assembling a verdict
>   and recording it — playtest evidence lands continuously, and this
>   project has now twice been burned by writing against a stale snapshot.
> - No balance changes, no "improvements", no opinions — those belong in
>   other mods. When intent is ambiguous, prefer the reading proven by
>   sibling code in the same file (the F07/F08/F02 pattern).

## 5. Shaken loose

- **The F49 verdict-table row and the "NOT delete candidates" bullet above
  were corrected in place** (marked "corrected by Challenge review"): the
  module is now (a) R4 no-op rider + (d) R2 play-proven; (c) is tier I,
  closed, code removed. The original lead-pass prose stands as the record of
  what was claimed.
- **The audit's "PT citations checked" claim gains a caveat:** those checks
  ran against the session-start snapshot. Two commits (`c3c4383`, `ba1e88b`)
  landed mid-audit; one of them contained a play-PASS the audit re-asserted
  as an unproven tier, the other the facts that falsified a tabled verdict.
- **F49(d)'s PostLoadGame sweep repair remains unproven** (idempotence shown,
  repair not — needs a fix-vetoed save; TestKit probe queued, per `c3c4383`).
- **The blind-spot list (§3) is standing work**: eleven verdicts currently
  rest on source-shaped evidence for claims with runtime components. None is
  suspected wrong; F49(c) is the proof that "not suspected" is not the same
  as "checked".
