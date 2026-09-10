# 03d live progress — callers, services and rowless seams

Source pin: Steam build `24995074`; archived trees `1.0.7.396349` and
`1.1.0.403908`. The 03d receipt contains 283 items: 249 INVENTORY rows in 105
files, 16 CALLERS items, and 18 whole-file NOROWS diffs. Parent owns instruments,
verdicts, shared-file writes, re-derivation, and sampling; delegated work is
read-only and follows the README per-row return contract.

- [x] **COMPLETE — U0: pin and operating ledger.** Verified repository/build
  pins, create this exact-receipt plan, run all commit gates, commit, and verify
  the commit/worktree at `9a01598`; hook doccheck GREEN, both instrument
  selftests PASS, TestKit tree clean, and the historical kit-tree WARN did not
  recur. A peer-owned `PROGRESS_03C.md` edit appeared afterward and is excluded.
- [x] **COMPLETE — U1: complete source receipt.** Read the seven FR rows first,
  then all 283 assigned items and the minimum supporting owner/non-owner
  definitions, consumers, inheritors, and runtime data readers in both trees.
  Read-only partitions sized from the receipt: reader A handles 87 transport,
  rocket, cargo, station, stockpile, grid, passage, and trade items in 28 files;
  reader B handles 88 service, workplace, maintenance, terraforming, building,
  resource, research, and ambient-work items in 37 files; reader C handles 108
  scenario, tutorial, UI, configuration, modding, and remaining system items in
  62 files. Parent re-reads every FR surface and surviving lead. Record hunks-only,
  malformed, incidental, and not-reached spans explicitly. Commit the durable
  raw read receipts and verified coverage update. Completed 283/283 with zero
  not reached: A 87/87, B 88/88, C 108/108. Parent re-read all seven FR rows,
  every filed lead, and the deterministic six-item sample (seed 20260910).
- [x] **COMPLETE — U2: falsification and filing.** Parent re-derived every surviving
  candidate, runs applicable deskbench controls after a declared stale-probe
  sweep, files any first-class C entries/checklist decisions, and commits verified
  outputs. No eligible seed was scored 4/4: eligible count is zero. Filed
  C66-C73; the archived-body desk discriminates C67-C69 and records its clean
  stale-probe sweep. Routed all runtime choices to checklist decision 138.
- [x] **COMPLETE — U3: synthesis and close-out.** Appended the named TRIAGE
  section and complete 03b/04/99 outboxes, updated STATE and the README queue,
  removed the consumed prompt, and reran the desk and every required gate.
  The close-out commit carries this final ledger update; push and clean-tree
  verification follow that commit.

No game launch, module work, metadata/version edit, archived-source write, or
out-of-fence DLC/norman interior read is authorized.

## Exact read-only partitions

Reader A owns every 03d receipt item in these 28 files (87 items):
`Lua/UniversalRocket.lua`; `Lua/CargoTransporterNew.lua`;
`Lua/CargoRequestNew.lua`; `Lua/Buildings/CargoTransporter.lua`; `Lua/Cargo.lua`;
`Lua/RocketPayload.lua`; `Lua/UniversalPod.lua`; `Lua/RocketCompatibility.lua`;
`Lua/Buildings/RocketBase.lua`; `Lua/Buildings/SupplyRocket.lua`;
`Lua/Buildings/RocketUtilities.lua`; `Lua/Buildings/RocketTrade.lua`;
`Lua/Buildings/SpaceElevator.lua`; `Lua/Buildings/Elevator.lua`;
`Lua/Units/RCTransport.lua`; `Lua/Units/ColonistTransport.lua`;
`Lua/Units/Colonist.lua`; `Lua/Units/Train.lua`; `Lua/Buildings/Station.lua`;
`Lua/Buildings/ResourceStockpile.lua`; `Lua/WasteRock.lua`;
`Lua/Buildings/TradePad.lua`; `Lua/TradeRoutes.lua`;
`Lua/Buildings/ShuttleHub.lua`; `Lua/SupplyGrid.lua`;
`Lua/SupplyGridBreakable.lua`; `Lua/Passage.lua`; `Lua/CovertOps.lua`.

Reader B owns every 03d receipt item in these 37 files (88 items):
`Lua/Buildings/TerraformingBuilding.lua`; `Lua/Buildings/Workplace.lua`;
`Lua/Buildings/Service.lua`; `Lua/RequiresMaintenance.lua`;
`Lua/Buildings/BaseBuilding.lua`; `Lua/Buildings/ReconCenter.lua`;
`Lua/Buildings/Anomaly.lua`; `Lua/Buildings/LandscapeLake.lua`;
`Lua/Buildings/MegaMall.lua`; `Lua/Buildings/Factory.lua`;
`Lua/Buildings/AsteroidCatcher.lua`; `Lua/Buildings/DepositMarker.lua`;
`Lua/Buildings/BuildingComponents.lua`; `Lua/Buildings/ShiftsBuilding.lua`;
`Lua/Buildings/ArtWorkshop.lua`; `Lua/Buildings/MartianAssembly.lua`;
`Lua/Buildings/TerrainDeposit.lua`; `Lua/Buildings/SubsurfaceDeposit.lua`;
`Lua/Buildings/SensorTower.lua`; `Lua/Buildings/SpawnsOnCityInit.lua`;
`Lua/Buildings/MicroGHabitat.lua`; `Lua/ServiceBase.lua`; `Lua/Refabable.lua`;
`Lua/Buildings/Diner.lua`; `Lua/AmbientLife/VisitFastFoodRestaurant.lua`;
`Lua/AmbientLife/VisitFoodStand.lua`;
`Lua/AmbientLife/VisitGourmetRestaurant.lua`;
`Lua/AmbientLife/WorkFarmInsect.lua`; `Lua/AmbientLife/WorkFarmSmall.lua`;
`Lua/AmbientLife/WorkFoodStand.lua`;
`CommonLua/Libs/Resources/ClassDefs/ClassDef-Resources.generated.lua`;
`CommonLua/Libs/Resources/Resources.lua`;
`CommonLua/Libs/Research/ClassDefs/ClassDef-Conditions.generated.lua`;
`CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua`;
`CommonLua/Libs/Research/Data/ClassDef-Conditions.lua`;
`CommonLua/Libs/Research/Data/ClassDef-Effects.lua`;
`CommonLua/Libs/Research/Data/ClassDef-PresetDefs.lua`.

Reader C owns the exact complement: every 03d receipt item whose file is in
neither A nor B above (108 items in 62 files). The three sets are disjoint and
cover all 283 03d items.
