# Community Bug Catalog (research notes)

Compiled 2026-07-24 from community fix mods for the original Surviving Mars and
live Relaunched player reports. Use as a lead list: entries here are NOT
verified against Relaunched source unless promoted into BUGS.md.

## Primary sources

- ChoGGi "Fix Bugs" (original game): bug list + patched functions —
  https://github.com/ChoGGi/SurvivingMars_Mods/blob/master/Mods%20ChoGGi/Fix%20Bugs/MoreInfo.md
  (source: `.../Fix Bugs/Code/Script.lua`, ~3100 lines). ChoGGi's own comments track
  the remaster ("SMR"): `CargoTransporter:SpawnRovers()` typo marked fixed in SMR;
  most other fixes not confirmed either way.
- Relaunched bug-report forum: https://forum.paradoxplaza.com/forum/forums/surviving-mars-relaunched-bug-reports.1189/
- LukeH "Martian Express Patch" (original): Workshop 2801556344 / Fix Pack 2919738467 —
  trains blocking track demolition, undeletable track after station destruction,
  automated transports dropping resources at non-accepting stations.

## Relaunched player reports (Feb–Jul 2026) not yet mapped to code

- Asteroid lander launches empty (cargo selected, arrives with nothing).
- Drones ignore rocket cargo even at high priority; RC Transports don't
  auto-offload rockets (`RCTransport:TransferResources` family) — sweep
  `DroneControl.lua`/`ShuttleHub.lua`.
- Seniors don't auto-move to retirement homes.
- Mysteries not starting (Inner Light; also general reports) — old "Asylum never
  starts" class.
- No cold waves or dust storms ever trigger (weather scheduler) — note our F02
  found the meteor scheduler broken in the opposite direction; audit
  ColdWave/DustStorm spawn threads the same way.
- Jumbo Cave reinforcements stuck at "construction site is being cleared".
- Martian Express: can't salvage tracks, tracks won't connect to stations,
  rebuild blocked by raised terrain.
- Auto asteroid miners (Exotic Minerals/Precious Metals) missing from asteroid
  build menu — same class as old ShuttleHub `save_in` DLC-gating bug in
  `UIGetBuildingPrerequisites`.
- Changing rocket layout on asteroid traps drones inside rocket (1.07).
- Rival colony rockets glitch permanently if refilled from RC Transport (1.07).
- Outside ranch "too far from dome" when in range (`IsBuildingInDomeRange`).
- Universities train geologists once Extractor AI researched (cf. original
  `FilterCompatibleTraitsWith` school bug — schools training perks colonists
  already have, `School:OnTrainingCompleted`).
- Fast Rockets game rule stops working mid-game.
- Political party tension rises under Single Party law.
- Story rocket stuck unloading, can't take off (cf. original
  `StoryBitState:OnStartRunning` invalid-rocket fix).
- Can't build over spots where buildings previously stood (buildable grid not
  cleared after demolition).
- Colonists teleporting; new save has no rainfall (terraforming).

## Review-sourced reports (added 2026-07, from Steam reviews via user)

- **Late-game drone collapse with open domes**: drones stop maintaining buildings
  *inside* opened domes, cluster stuck right outside, colony decays. → Sweep
  `Buildings\DroneControl.lua` + dome open/passability interaction with drone
  work-request gathering.
- **Citizens stuck on terrain/Universal Depots and die walking rocket→dome** →
  pathing/passability around depots; possibly same family as long-walk suffocation.
- **Colonists suffocate walking between distant domes** → the original
  `AreDomesConnectedWithPassage` daily-interest/long-walk bug class; verify in
  Relaunched.
- **Citizens go unemployed every sol despite free worksites** → workplace
  auto-assignment (`UpdateWorkplaces` family), not yet swept.
- **Citizens homeless despite free housing in own + adjacent domes** → residence
  auto-assignment; related report: seniors not moving to retirement homes.
- **Large Wind Turbines unaffected by tech that names them** (Frictionless
  Composites not applying post-hotfix; also couldn't be rotated) → check the
  tech's modifier target label vs the LargeWindTurbine template/class label —
  same verification style as our F03/F18 work; very targeted, do early.
- **Asteroids routinely get cave-ins** (reviewer believes cave-map-only intended)
  → VERIFIED NOT from the underground marsquake repeat (its condition requires
  `Environment == "Underground"`; asteroids are `"Asteroid"` — Marsquake.lua:324,
  Asteroids.lua:459). Something else triggers them on asteroid maps — find it
  (asteroid map generation? scenario? a different caller of TriggerCaveIn?).
- **Artificial lake entombs rovers/drones** placed-over units die under lake;
  dismissal of the warning notification immediately re-triggers it → Landscape/
  lakes not yet swept; also check notification re-trigger loop.
- **"Lakes causing crashes"** (vague but repeated) → Landscape sweep target.
- **Inspiring Architecture freezing glitch, "present in the original"** →
  find original fix/mod references; sweep the InspiringArchitecture trait/dome
  interaction.
- **Trains: deleting one wrong hex of track deletes the entire track** →
  Martian Express track editing; LukeH's original patches are prior art.
- **UI buttons misaligned** → XTemplates layout; cosmetic, likely fixable via
  template patch; collect concrete screens/cases first.

## High-upvote review reports (added 2026-07, 100+ upvotes each)

Mapped to existing findings:
- "Domes with plenty of jobs/vacancy but homeless and unemployment notifications"
  → F51 (shuttle transport cache), F54 (off hubs count as transport), plus the
  three documented "unemployed every sol" mechanisms under F50-F57 notes.
- "All non-specialists stop working their jobs randomly" → same unemployment
  cluster; ALSO check by-design specialist displacement (workplaces evict
  non-specialists when specialists apply) misfiring with F36's inflated
  specialist demand. Needs repro save.

NEW leads (not yet traced — priority targets for next session):
- **Deterministic freeze near 90% breathable atmosphere** (reproduces at same
  point across reloads). Prime suspect: the Open Domes / breathability threshold
  transition (`OpenAirBuilding.lua` skin-swap and transition loops, terraforming
  threshold Msg handlers, rainfall). A same-point lockup smells like an infinite
  loop in a game-time thread triggered by a terraforming param crossing a
  threshold. HIGH priority — hard lock + likely widespread late-game.
- **The Last War mystery freezes at 54%, permanently blocking ALL imports** —
  the mystery presumably disables resupply during a sequence and hangs before
  re-enabling (same one-shot-Msg hang class as F06/Crystals). Sweep the Last War
  scenario/sequence files for import-lock set/clear pairing and WaitMsg hangs.
  HIGH priority — permanent economy kill.
- **Game stops saving entirely (auto + manual)** — classic symptom of a Lua
  error during savegame persistence (one corrupt/unpersistable object aborts
  the save). Cross-check against our corruption-leaving bugs (F03 leaked
  modifiers, F30 entombed units, F45 broken-track repair sites with false
  node_idx...). Need a player log/save to pin. HIGH priority.
- **Colonists disappear from dome UI lists while still working** — label
  registration desync (dome/city labels lose the colonist). Original game had
  exactly this class (cf. `SavegameFixups.ColonistsOutsideLabelsAfterInspiringArchitecture`,
  B&B wrong-map label counts). Find what de-registers without re-registering.
- **Rocket transporting tourists home disappears mid-flight** — tourist
  departure path (`RocketBase.lua:818` / `UniversalRocket.lua:2014` area, F08's
  neighborhood); check the depart/travel state machine for a Done() without
  respawn on the tourists-aboard path.
- **Train stations don't connect when attached to a train tunnel** — extend F48/
  AutoConnectTracks constraint analysis to tunnel connector elements.
- **Light sources stop working underground** — likely engine/rendering side;
  check Lua light-attach logic underground before writing it off as unfixable.

## Review batch 3 (added 2026-07-25)

Mapped to existing findings:
- "Trains swap random resources back and forth fully stacked, no readable sense"
  → F46 (dump-at-disabled-stations + forbidden-stock re-haul ping-pong) is very
  likely the whole story.
- "Rockets stuck in load/unload loop" (B&B asteroids) → F50 (hourly
  drone-churn/auto-cargo-request loop) + F56.
- "Colonists don't move for jobs cross-dome even with passages" → F51/F52/F54
  cluster + unemployment mechanisms.
- Popup notifications yank you out of the build GUI → UX design gripe; check if
  popups force-close the build dialog in Lua (may be patchable).
- "Old-timer died" spam every few minutes → QoL: make death-of-old-age
  notification suppressable/aggregated — same preset surgery as F32.

NEW leads:
- **Rockets no longer auto-refuel / auto-load Rare Metals** ("BIGGEST issue",
  community-hated). Determine design-change vs bug: check `UniversalRocketBase`
  auto/export logic, `CreateAutoCargoRequest` rare-metal handling, refuel request
  wiring (F50's neighborhood). If design change: candidate opt-in restore fix.
- **Asteroid lander cluster (B&B "unusable")**: (a) loads what it wants — edit
  payload ignored; (b) prioritizes WASTE ROCK over everything; (c) unloads
  everything, launches empty, returns to ASTEROID instead of Mars (fuel wasted,
  expedition lost); (d) sometimes loads nothing at all — refuels and sits (no
  drones/resources), stranding landers; (e) can't send second lander to rescue.
  Sweep the CargoTransporter/lander payload+destination state machine.
- **Colonists on asteroid don't use habitat, suffocate in the mine** — asteroid
  residence/oxygen assignment.
- **Same-dome housing failure**: can't find houses in a dome with >50% vacancy
  (NOT explained by F51 which is cross-dome) — sweep same-dome residence
  assignment for filter bugs.
- **University in separate dome never gets students** — student recruitment is
  cross-dome-gated? Check against F51 cache + student-specific path.
- **Colonists refuse to shop through passages** — service-seeking
  passage-connectivity check (original long-walk bug family, service branch).
- **Train tunnel doesn't transfer electricity despite description** — check
  tunnel template grid elements vs description text.
- **Post-1.01 "trains go to void"**: destroying station/track WITH trains on it
  permanently breaks ALL trains — can't assign trains to new tracks/stations
  even after full rebuild. A community micro-mod reportedly fixes it — find it
  for reference. Our F44/F49(b) territory: `DestroyAssignedTrains` stores trains
  as prefabs — suspect the stored-prefab/global-registry restore path corrupts
  (e.g. stored count never decremented, or train prefab list pinned to dead
  track). HIGH priority.
- Surface/underground UI "bouncing" — vague; park.

## Original-game fix list highlights to re-verify in Relaunched source

Drones/rovers: malfunctioning drones stuck at hub (`InvalidPos`), drones stuck in
pastures, flying drone mid-air malfunction (`Land()`), RC Harvester waste rock
(`RCHarvester:FindNextRouteSource`), RC route buttons
(`RCTerraformer/RCConstructor:ShouldShowRouteButton`), transport negative
resources, rover trapped in dome, expedition rover cleanup
(`RocketExpedition:KillExpedition/Done`), Marsgate rover repair/tower flags.

Shuttles: stuck mid-air on dead request (`req:UnassignUnit()` + GoHome),
underground pathing.

Colonists: suffocating in dome wearing suits (missed `OnEnterDome`), long-walk
daily interest (`AreDomesConnectedWithPassage`), expedition status "unknown"
(`WaitToAppear` missing from `ColonistCommands`), leftover `transport_ticket`
blocking residence assignment, Dust Sickness on Androids (can't die, keeps it
forever), wrong-map colonist counts (`Elevator:Disembark`).

Buildings: unrepairable at 0 accumulated maintenance (lightning during cold
wave), ghost farm oxygen (`Farm:Done`), nil `electricity.parent_dome` "No Power",
buildings placeable on dust devils, layout construction bypassing tech locks
(`LayoutConstructionController:Activate`), destroyed tunnels still pathable
(`Tunnel:AddPFTunnel`), second Artificial Sun ignored
(`SolarPanelBase:GameInit`), flatten-tool unbuildable terrain, Wind Turbine
locked by leftover `BuildMenuPrerequisiteOverrides`.

Rockets/etc.: meteor stuck on map (dead `fall_thread`), resupply menu not
opening, RC Safari missing from resupply (`ResupplyItemDefinitions`), blank
mission profile from removed modded rules, Sol 2983 `GameTime` int32 overflow.

Tech/storybits: Gene Forging `param1` never set, Eureka wrong category, Blank
Slate no-op, Twin Peeks `obj.revealed` vs `SetRevealed`, St. Elmo's sinkholes
destroyed by meteors (indestructible flag), Cyber War never pays, Fhtagn!
Coward-instead-of-religious, Man From Mars outcome 3 no reward.

B&B/underground: breakthrough init per-city (our C01), Bottomless Pit position,
cave-in rubble lag cap, Support Struts vs Easy Maintenance sponsor, Elevator
delivering non-existent resources, prefabs/deposits spawned on wrong map
(`TerrainDepositMarker:SpawnDeposit` active-realm bug), passage power-toggle
spam (`Dome:PropagateSetSupplyToPassages`).

UI: double-click select-all-of-type, pinned status icons
(`PinsDlg:GetPinConditionImage`), cursor ghosts stuck on map, Mirror Sphere
capture FX never ends.
