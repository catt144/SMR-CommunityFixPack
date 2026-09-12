# ScanDowngrade - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ScanDowngrade.lua | C86 | yes: direct final registry line 261 active | yes: Advanced probe passes status to each pattern sector; sector status drives decal/UI/queue | yes: vanilla permits deep-to-scanned downgrade and wrapper preserves higher status | n/a: no dedicated metadata headline | KEEP | 1.1.0.403908 Lua/OrbitalProbe.lua:81; 1.1.0.403908 Lua/OrbitalProbe.lua:97; 1.1.0.403908 Lua/OrbitalProbe.lua:99; 1.1.0.403908 Lua/OrbitalProbe.lua:170; 1.1.0.403908 Lua/Exploration.lua:230; 1.1.0.403908 Lua/Exploration.lua:275; 1.1.0.403908 Lua/Exploration.lua:278; 1.1.0.403908 Lua/Exploration.lua:284 | SOURCE | Actual AdvancedOrbitalProbe object firing and overview entry refusal; Live no-mod downgrade A/B and player repeat-scan time/notification effects; Current TestKit firing, menu-enable/reload, save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- AdvancedOrbitalProbe still declares five-sector plus pattern (:170-176); GetAffectedSectors :81 accepts every in-map sector without a status filter. Without AdaptedProbes, mode :97 is scanned; :99 calls Scan on every accepted sector. No current caller replacement prevents the lower request.

- MapSector:Scan :230 excludes unexplored/equal requests only, then :275 assigns requested status and :278 updates the decal, :284 refreshes the infopanel. The corrected status still has concrete shipped consumers. Queue CanBeScanned :154-172 continues to read the scan state.

- The module returns early only for lower known ranks on exact MapSector; other calls delegate. Existing caller audit and current attended entry remain authoritative: the 09-11 seam run preserved X deep and scanned neighbourY. It was not an actual AdvancedOrbitalProbe object firing or a live fix-off A/B.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:309-320 describes already deep-scanned neighbours becoming scanned without AdaptedProbes. It matches current primary path; no claim correction found.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:261` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Actual AdvancedOrbitalProbe object firing and overview entry refusal
- Live no-mod downgrade A/B and player repeat-scan time/notification effects
- Current TestKit firing, menu-enable/reload, save/load/uninstall,1.0.7 runtime
