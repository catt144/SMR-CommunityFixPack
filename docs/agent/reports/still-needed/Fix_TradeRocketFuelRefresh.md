# TradeRocketFuelRefresh - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TradeRocketFuelRefresh.lua | F119 | yes: direct final registry line 234 active | yes: live fuel requirement determines cargo status; resized supply/demand drives drones and CmdLoad wait | yes: landed Earth Trade fuel-cost changes still excluded by vanilla player-only modifier callback | yes: Earth Trade fuel wedge headline supported | KEEP | 1.1.0.403908 Lua/UniversalRocket.lua:1917; 1.1.0.403908 Lua/UniversalRocket.lua:2633; 1.1.0.403908 Data/FlightPolicyDef.lua:568; 1.1.0.403908 Lua/CargoTransporterNew.lua:1295; 1.1.0.403908 Lua/CargoTransporterNew.lua:1457; 1.1.0.403908 Lua/CargoTransporterNew.lua:1458; 1.1.0.403908 Lua/UniversalRocket.lua:500 | SOURCE | Full current Wildfire mystery cure loop or player stuck save; Fuel-cost rise and ministry/law/other modifier trigger routes; Actual1.0.7 runtime, other rocket families and foreign subclasses; Current TestKit firing, menu enable/reload and additional save/load/uninstall |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- UniversalRocketBase:OnModifiableValueChanged :1917 still refreshes FuelResourceAmount only for player control. IsPlayerControlled :2633-2637 omits Trade. Trade landing branch FlightPolicyDef :561-568 enters CmdLoad with cargo request. No renamed/replacement callback fixes this omission.

- CargoTransporterNew:GetCargoResourcesStatus :1295 reads the live GetFuelResourceRequest value; mismatched amount returns unloading/loading and UniversalRocket CmdLoad :500 waits for readiness. The updater :1457/:1458 writes supply/demand amount targets, which retain ordinary drone consumers. F50 replacement retains those calculations and does not create the missing refresh trigger.

- The post-wrapper calls vanilla first then refreshes only exact UniversalTradeRocket loading state for a fuel-cost property change. LoadGame sibling refreshes only mismatched exact loading Trade objects. Both paths affect live request amounts read by status/delivery, rather than estimates alone.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:477 and metadata headline match this remaining Earth Trade wedge. Existing 09-11 attended A/B reproduced the actual AdvancedMartianEngines trigger and observed both heal/prevention rockets leave. No current rerun is claimed; Wildfire full mystery/new laws and player save remain named limits.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:234` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Full current Wildfire mystery cure loop or player stuck save
- Fuel-cost rise and ministry/law/other modifier trigger routes
- Actual1.0.7 runtime, other rocket families and foreign subclasses
- Current TestKit firing, menu enable/reload and additional save/load/uninstall
