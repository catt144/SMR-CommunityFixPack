# 04-A skim — turf

Banner: plan brief `41672f1`; units given: 112 inventory-bearing files + 9 NOROWS files; date: 2026-09-10.

This is the owner-authorized file-level diff skim, not a row audit. A `nothing odd` line means only that the changed hunks showed no promoted tell at skim depth.

## Skim table

- `Lua/BuildableGrid.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/AdvancedStirlingGenerator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/AutomaticMicroGExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/BaseElevator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/BaseExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/BaseRover.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/BuildingComponents.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/BuildingWayPoints.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/CaveInRubble.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Constructable.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/ConstructionSite.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Deposit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/DroneControl.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/DroneFactory.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/DroneHub.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/DroneHubExtender.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/EffectDeposit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Elevator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/LandscapeLake.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/MetalsExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/MicroGExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Mine.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/MoholeMine.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/MoistureVaporator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/PreciousMineralsExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RareMetalsRefinery.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RechargeStation.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Refinery.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RegolithExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RegolithMineVisualCP3.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/ResourceStockpile.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RoverBuilding.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/RubbleBase.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/SharedStorageBaseVisualOnly.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/ShuttleHub.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/SolarPanel.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Station.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/StationsLink.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/StirlingGenerator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/StockpileController.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/StorageDepot.lua` — FLAG: R11004 lead — the current universal-storage branch around `ColonyControlCenter.lua:894-953` treats Seeds specially while MultiResourceDepot filtering changed. Drilled: REJECT; shipped multi-resource templates do not accept Seeds.
- `Lua/Buildings/SubsurfaceDeposit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/SurfaceDeposit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/TerrainDeposit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/TheExcavator.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Track.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/TrackElement.lua` — FLAG: F116 control — `TrackGridElement:DemolishAndSplitTrack` changed old `:448` / current `:467`, including the pre-sort processing and split behavior. Drilled: the seeded patch-divergence control.
- `Lua/Buildings/TriboelectricScrubber.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/Tunnel.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/TunnelBlockerRubble.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/WaterExtractor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/WaterReclamation.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Buildings/WindTurbine.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/Construction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/GridConstruction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/GridSwitchConstruction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/LayoutConstruction.lua` — FLAG: F118 lead — controller activate/deactivate changed old `:217/:310` to current `:313/:411`, and current owns `s_ConstructionControllerDeleteOnLoad` at `:385/:412`. Drilled: REJECT; controller-level deactivation clears the slot and no vanilla child-only route was found.
- `Lua/Construction/LevelPrefabBuilding.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/OpenCityConstruction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/TrackConstruction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Construction/TunnelConstruction.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ConstructionCost.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/DepositRevealer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ElectricityConsumer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ElectricityGrid.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ElectricityProducer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ElectricityStorage.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Elevation.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Flight.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Geysers.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/GridObject.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/GridTunnelConnector.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LRManager.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LRTransport.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/ClearWasteRockConstructionSite.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeClearWasteRock.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeConstructionController.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeConstructionSite.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeConstructionSiteBase.lua` — FLAG: EF-083 lead — current `ShouldAddRequestToCommandCenter:40` refuses drone-command registration where old landscaping sites exposed drone work. Drilled: REJECT; the new RC Dozer-only contract is explicit.
- `Lua/Landscape/LandscapeRamp.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeTerrace.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/LandscapeTexture.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Landscape/Landscaping.lua` — FLAG: F115 control — signature/body moved old `LandscapeForEachUnit:455` to current `:509`; current `:516-522` still constructs `filter_embark` then passes raw `callback`. Drilled: existing F34(d).
- `Lua/Landscape/TerrainPaintConstructionSite.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LifeSupportConsumer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LifeSupportGrid.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LifeSupportProducer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/LifeSupportStorage.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/MultiSelection.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Pathfinding.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ResourceOverview.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ResourcePile.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/ResourceTracking.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Resources.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/SupplyGrid.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/SupplyGridBreakable.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/SupplyGridSwitch.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Tracks.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/TrainDisasterHandling.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/TrainTransport.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/UnderconstructionSign.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/UnitControl.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/Drone.lua` — FLAG: EF-083 lead — old landscape interaction `:2031/:2055/:2123` became current `:2276/:2301/:2337`. Drilled: REJECT; current check returns false and the handler is deliberately a no-op.
- `Lua/Units/DroneBase.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/Drone_TrailblazerSkins.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/FlyingDrone.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/JumperShuttle.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCConstructor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCConstructorBase.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCDriller.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCHarvester.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCRover.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCSensor.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCSolar.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCTerraformer.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/RCTransport.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/Units/Train.lua` — FLAG: F114 control — `Train:UnloadAll` changed at old `:783` / current `:779`; the new nil guards do not restore the per-resource enable test. Drilled: existing F46 remains the vanilla defect.
- `Lua/Units/Unit.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/WasteRock.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/_TaskRequest.lua` — nothing odd in the file-level changed-hunk skim.
- `Lua/hex.lua` — nothing odd in the file-level changed-hunk skim.

## Ranked flags and drills

1. `Lua/Landscape/Landscaping.lua` — F115/F34(d), PASSING defect retained; old `:455-468`, current `:509-522`.
2. `Lua/Units/Train.lua` — F114/F46, current vanilla still omits the resource-enabled check; old `:783`, current `:779`.
3. `Lua/Buildings/TrackElement.lua` — F116 positive control; changed body old `:448`, current `:467`; this is a pack-copy divergence, not a new C entry.
4. `LayoutConstruction.lua`, `LandscapeConstructionSiteBase.lua`, `Drone.lua`, `StorageDepot.lua` — F118/EF-083/R11004 all REJECT after route reads described in their table lines.

## SMELL keep/drop

- R05485 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05537 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05542 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05563 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05568 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05624 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05637 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05890 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05929 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R05943 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06205 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06503 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06511 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06678 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06694 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06703 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06788 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06799 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06800 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06802 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06804 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06808 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06820 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06823 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06853 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06965 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06979 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06980 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06987 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R06991 — KEEP: promoted to the F115/F116 control drill above.
- R06996 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R07644 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R07647 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R07680 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R07717 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08275 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08277 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08460 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08464 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08468 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08470 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08479 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08487 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08497 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08516 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08530 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08560 — KEEP: promoted to the F115/F116 control drill above.
- R08584 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08586 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08589 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R08593 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R09159 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R09653 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R09654 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R09656 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R09890 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10232 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10506 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10534 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10651 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10711 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10713 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R10755 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.
- R11667 — DROP: not promoted from the skim; no current harmful player route was established within the ranked drill budget.

## Limits and control

- NOT skimmed: none of the 121 assigned file units.
- Flagged, not drilled: the 62 SMELL rows marked DROP above; no named file flag was left undrilled.
- Parent reopen sample: `Lua/Buildings/SolarPanel.lua` and `Lua/Units/RCSensor.lua`, 2/2 still `nothing odd` at the same file-level depth.
- Positive controls: F114, F115 and F116 were all FLAGGED here. F117 belongs to 04-B.

