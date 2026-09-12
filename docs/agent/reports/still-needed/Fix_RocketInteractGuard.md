# RocketInteractGuard - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_RocketInteractGuard.lua | F74 | yes: direct final registry line 250 active | yes: unit-control cursor, direct orders and transport routes consume the wrapped predicate/action | yes: guard still names legacy rocket family and misses Universal event classes | n/a: no dedicated metadata headline | KEEP | 1.1.0.403908 Lua/Units/RCTransport.lua:412; 1.1.0.403908 Lua/BuildingTemplate/UniversalTradeRocket.generated.lua:5; 1.1.0.403908 Lua/BuildingTemplate/UniversalRefugeeRocket.generated.lua:5; 1.1.0.403908 Lua/UnitControl.lua:481; 1.1.0.403908 Lua/UnitControl.lua:412; 1.1.0.403908 Lua/TransportRouteInteractionHandler.lua:50 | SOURCE | Current live event-rocket refusal, cursor/route and controls; Current halt-mid-load/overflow terminal harm and plain UniversalRocket rival trade-pad behavior; Static subclass callers, menu enable/reload, save/load/uninstall, 1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Vanilla CanInteractWithObject still names TradeRocketBase and RefugeeRocketBase. Both current generated event classes descend from UniversalRocketBase; the two class families remain separate. The module blocks the current event classes then delegates all other interactions.

- UnitControl at :481 stores a target only after the predicate returns truthy; :412 dispatches an order using the stored target. The transport-route handler :50 dispatches through the same UnitController. Its :657 and :664 call the unit methods. Both changed methods still have ordinary consumers.

- Primary Lua/Sequences/SA_Gameplay.lua places the Universal event classes directly. The scope remains event trade/refugee rockets: the historical entry distinguishes plain UniversalRocket rival trade-pad rockets, which this fix never covered.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:452 describes the accepted event-rocket orders and current-class guard. No row or headline correction found.

Direct registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:250` measures active. `BODYCHECK.txt` matches the target body and defect expression. Installation is not a cure observation.

Not checked:

- Current live event-rocket refusal, cursor/route and controls
- Current halt-mid-load/overflow terminal harm and plain UniversalRocket rival trade-pad behavior
- Static subclass callers, menu enable/reload, save/load/uninstall, 1.0.7 runtime
