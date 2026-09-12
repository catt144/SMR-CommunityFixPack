# BrokenTrackSalvage - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_BrokenTrackSalvage.lua | F45, C55 | yes: direct final registry line 229 active | yes: salvage combined-list sort still reads repair-site node_idx after partial prepass | yes: current repair copy still omits node_idx and midtrack duplicate hex defeats normal restamping | yes: damaged-track unsalvageable headline supported | KEEP | 1.1.0.403908 Lua/Buildings/Track.lua:634; 1.1.0.403908 Lua/Buildings/Track.lua:641; 1.1.0.403908 Lua/Buildings/TrackElement.lua:475; 1.1.0.403908 Lua/Buildings/TrackElement.lua:487; 1.1.0.403908 Lua/Tracks.lua:616; 1.1.0.403908 Lua/Tracks.lua:633 | SOURCE | Current midtrack damaged-site salvage and end-break self-heal control; Native HexGetTrackGridElement duplicate-hex walk and C55 visible connection/assert effects; Current LoadGame repair-site stamp and healthy numeric controls; Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- BreakTrackElement :634-640 copies direction/location/station/connections/track_obj, still omitting node_idx. Repair site and hidden broken element share hex (:641-644). Both post-break wrapper and LoadGame sibling stamp missing number from original element, which remains part of the live sort input.

- Current DemolishAndSplitTrack :469-471 delegates a repair-site click to the real element, :475 first runs ProcessAllElements, :481/:484 combines completed/underconstruction lists and :487 sorts node_idx. Existing F45/C55 current-source note is accepted: hex walk can bail at Tracks :616 before :633 stamps numbers for midtrack duplicate hex. The new prepass is a partial vanilla replacement; end-break self-heal remains unmeasured. The module therefore retains a residual and actual consumer, rather than merely clean attachment.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:335 and metadata headline name damaged-track unsalvageability. They match remaining midtrack case. Existing C55 partial-connection rewrite/assert is vanilla residue carried by F116; this task does not fix or runtime-grade it. Historical PT03 remains dated1.0.7 witness.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:229` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current midtrack damaged-site salvage and end-break self-heal control
- Native HexGetTrackGridElement duplicate-hex walk and C55 visible connection/assert effects
- Current LoadGame repair-site stamp and healthy numeric controls
- Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime
