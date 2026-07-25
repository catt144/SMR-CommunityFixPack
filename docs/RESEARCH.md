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
