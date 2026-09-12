# TrackSalvageWipe - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

- F116 original unresolved-divergence prose is superseded by owner-ruled hotfix2 rehome/combined processing already present; append entry build-state annotation, no new repair/status promotion

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrackSalvageWipe.lua | F44, F45 rider, F91, F116 | yes: direct final registry line 230 active | yes: player/station split calls decide surviving elements and assigned trains; shells still enter daily TrackBase walk | yes: vanilla curve/short-side branches still demolish entire track and trains | yes: one-piece salvage deleting line/trains headline supported | KEEP | 1.1.0.403908 Lua/Buildings/TrackElement.lua:506; 1.1.0.403908 Lua/Buildings/TrackElement.lua:529; 1.1.0.403908 Lua/Buildings/TrackElement.lua:543; 1.1.0.403908 Lua/Buildings/Track.lua:252; 1.1.0.403908 Lua/Buildings/TrackElement.lua:491; 1.1.0.403908 Lua/ResourceTracking.lua:198; 1.1.0.403908 Lua/Buildings/TrackElement.lua:471 | SOURCE | Current curve/near-end/mass/mixed/repaired/station-build salvage and train-survival A/B; Current F91 shell cleanup/load heal and C55 connection/assert effects; F116 rehome/combined processing and skip_process live controls; Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current partial salvage expansion :506/:509 still requires pillared AND straight; short-side checks :529/:543 call whole-track OnDemolish, and Track :252 destroys assigned trains. Player Demolish :463 and station-construction direct call Construction :1692 remain consumers. Module trim/split keeps viable survivors and preserves intentional mass-delete whole-track behavior. This is actual topology/train deletion consumer, not an estimate.

- F45 tolerant-sort rider still stamps repair node from broken element and declines unsafe nonnumeric partial sort. Vanilla pre-sort ProcessAllElements :475 remains in current copy (F116); skip_track_process forward :471 remains. Existing C55 midtrack failed hex-walk residue remains unmeasured, not claimed fixed.

- F91 sibling: vanilla mass-delete :490-492 calls OnDemolish and immediately returns without deleting TrackBase shell. Track :249 falsifies CanDelete while :280 destroys elements; ResourceTracking :198 still enumerates TrackBase assigned_vehicles daily. Module completes shell deletion and LoadGame purges old shells/orphan elements. These surviving world/label/save objects retain current readers and cleanup significance.

- Owner-ruled1.1.0 split rehome (:580-595) and combined postprocessing (:609-613) are already carried by module F116/ck111/ck119 blocks. LoadGame orphan deletion was explicitly ruled to remain; no recreation/rehome change is authorized here. F116 entry old prose no repair/two remaining divergences needs current build-state annotation rather than a new code ticket.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:324 and metadata headline match unexpected whole-line/train deletion. It does not promise Ctrl-click retains trains; mass-delete scope remains intentional. Historical tested F44/PT03 and F91 forced control are kept dated; F116 repaired source status is not upgraded to current tested.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:230` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current curve/near-end/mass/mixed/repaired/station-build salvage and train-survival A/B
- Current F91 shell cleanup/load heal and C55 connection/assert effects
- F116 rehome/combined processing and skip_process live controls
- Current behavior firing,menu enable/reload,save/load/uninstall,1.0.7 runtime
