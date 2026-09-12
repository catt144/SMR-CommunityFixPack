# DestroyedTunnels - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_DestroyedTunnels.lua | F38 | yes: direct final registry line 242 active | yes: load rebuilds pf tunnel; TraverseTunnel consumes valid ruin links without destroyed guard | yes: destroyed linked objects still regain pathfinding unless corrected | yes: destroyed-tunnel shortcut headline supported | KEEP | 1.1.0.403908 Lua/Buildings/Tunnel.lua:193; 1.1.0.403908 Lua/Buildings/Tunnel.lua:204; 1.1.0.403908 Lua/Buildings/Tunnel.lua:212; 1.1.0.403908 Lua/Buildings/Tunnel.lua:261; 1.1.0.403908 Lua/Buildings/TrackTunnel.lua:2; 1.1.0.403908 Data/BuildingTemplate/UniversalTunnel.lua:25 | SOURCE | Current live destroyed tunnel save/quit/load and rover/colonist long route; Current rebuilt-tunnel control and native pf.AddTunnel/RemoveTunnel behavior; Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- LoadGame at Tunnel.lua:261 still calls Tunnel.AddPFTunnel for all TunnelBase objects. AddPFTunnel :194 checks linked validity only and :204 inserts pf link. TraverseTunnel :212 checks both valid objects but no destroyed flag before moving a unit through. Destruction removes links in-session; load still reintroduces the valid-ruin link.

- UniversalTunnel remains object_class TrackTunnelBase (Data template :25); TrackTunnelBase :2 inherits TunnelBase without AddPFTunnel/TraverseTunnel override. The current player template build_category is Tunnels (:4), different from the historical entry Infrastructure label; its consumer family is unchanged.

- The wrapper blocks self or linked destroyed flags before delegation. The LoadGame sibling removes any already-added ruined link through pf.RemoveTunnel :208. Current rebuild creates construction-group replacements at Tunnel :140-151 and GameInit notifies AddPFTunnel at :83. No replacement consumer makes either correction redundant.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:267 and metadata headline name destroyed tunnel shortcuts after load and match the remaining defect. The historical PT25 four-step rover/save/rebuild control remains dated and is not a current-game witness.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:242` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current live destroyed tunnel save/quit/load and rover/colonist long route
- Current rebuilt-tunnel control and native pf.AddTunnel/RemoveTunnel behavior
- Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime
