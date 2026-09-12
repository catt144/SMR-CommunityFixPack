# TrackSalvageRefund - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrackSalvageRefund.lua | F47 | yes: direct final registry line 257 active | yes: OnDemolish ReturnResources uses replaced getter; partial delete emits returned stamped costs | yes: whole-track one-stamp read and bare partial DoneObject remain | yes: card intro stub-based refund example supported; no dedicated headline | KEEP | 1.1.0.403908 Lua/Buildings/Track.lua:291; 1.1.0.403908 Lua/Buildings/Track.lua:271; 1.1.0.403908 Lua/Buildings/Building.lua:1004; 1.1.0.403908 Lua/Buildings/ConstructionSite.lua:2698; 1.1.0.403908 Lua/Buildings/TrackElement.lua:536; 1.1.0.403908 Lua/Buildings/TrackElement.lua:463 | SOURCE | Current whole/partial/trim-empty/mixed/repair salvage stockpile A/B and no-double-refund controls; Current runtime construction group costs/stamps, freeconstruction fallback and refund rounding; Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current TrackBase:GetRefundResources :291 still chooses last element only, while ConstructionGroupLeader:Complete :2679 suppresses individual marks and :2698 stamps group spend on last completed. The sum has a current producer and consumer; no replacement counts prior groups. Historical perhex cost sketch is not used to manufacture refund totals.

- TrackBase:OnDemolish :271 still calls ReturnResources, which resolves GetRefundResources in Building :1004. Whole-track getter correction is therefore read by actual stockpile return machinery. Partial branches still delete elements via bare DoneObject (TrackElement :536 and sibling branches); Demolish :463 dispatches that body. The wrapper observes deleted stamped completed elements and emits half-spend stockpiles; whole-track demolishing stamp :250 suppresses duplicate partial refund.

- Construction-site and repair-site reentry distinction remains as in module: repair delegation is at TrackElement :469-471; a plain construction site may delete stamped completed neighbours. Current F44 composition and no-positive-stamp estimate fallback remain intentionally carried, not replaced by perhex multiplication.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:345 and metadata intro compare whole-track cost with short-section refund and match both retained defects. Exact group billing/cost receipt and current dropped stockpiles are not freshly measured.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:257` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current whole/partial/trim-empty/mixed/repair salvage stockpile A/B and no-double-refund controls
- Current runtime construction group costs/stamps, freeconstruction fallback and refund rounding
- Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime
