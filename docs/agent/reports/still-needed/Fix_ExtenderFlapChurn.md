# ExtenderFlapChurn - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

- Site :215-217 omits the two-second grouping condition; working edges separated by more than that window still cause separate interruptions
- Registered title promises no whole-hub rebuild, while the module intentionally runs one delayed full rebuild
- F77 opening entry incorrectly says blocked game-time debounce threads are not persisted; current module and EF-023 already correct this

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ExtenderFlapChurn.lua | F77 | yes: direct final registry line 263 active | yes: working edges still rebuild the root requester set; removal still sends matching drones to Idle | partial: one interruption requires events inside the two-second coalescing window; spaced edges still each rebuild | yes: defect headline is supported; registered title overstates removal of all rebuilds | KEEP-BUT-FIX-CLAIM | 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:109; 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:114; 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:147; 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:156; 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:184; 1.1.0.403908 Lua/Buildings/DroneHubExtender.lua:186; 1.1.0.403908 Lua/Buildings/DroneControl.lua:387; 1.1.0.403908 Lua/Buildings/DroneControl.lua:500; 1.1.0.403908 Lua/Buildings/DroneControl.lua:784; 1.1.0.403908 Lua/Buildings/DroneControl.lua:790; 1.1.0.403908 CommonLua/TaskRequest.lua:164; 1.1.0.403908 CommonLua/TaskRequest.lua:167 | SOURCE | Organic current extender working-flap interruptions and exact throughput gain; Gathered orphan drone behavior during the two-second stale-registration window; Current save/load during debounce, uninstall orphan gate, enable/reload and 1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- DroneHubExtenderBase OnSetWorking :184 still calls UpdateUplinkRequesters in both directions. The helper :109-111 disconnects/connects, delegating through uplinks :114-123. Link :156 and Unlink :147 also enter it. Current working=true GatherOrphanedDronesInRange :186 is additional, not a replacement of the teardown.

- DroneControl ConnectTaskRequesters :387 repopulates the root coverage; DisconnectTaskRequesters :500 removes each connected requester. CommonLua/TaskRequest.lua:164-167 calls center:RemoveBuilding, reaching DroneControl :795-796 -> OnRemoveBuilding :784. Matching goto targets still execute drone:SetCommand("Idle") at :790. The F60-style consumer disappearance did not occur.

- Code/Fix_ExtenderFlapChurn.lua uses DEBOUNCE=2000, one pending thread per resolved root hub, then runs the same full Disconnect/Connect after Sleep. Events while that thread is pending coalesce. Once it finishes, the next event schedules another rebuild. A power-off edge and later restoration more than two seconds apart therefore do not become a single interruption. Row :215-217 should say events within two game seconds share one delayed rebuild; the card defect headline remains true.

- The opening F77 historical sketch predates the installed wrapper and incorrectly denies by-value blocked-thread persistence. Current module explicitly incorporates EF-023 and checks SMRFixPack after Sleep before touching vanilla state. Preserve the historical dates and add a current freshness correction; do not re-promote untested PT status.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:263` measures active. Installation is not cure verification.

Not checked:

- Organic current extender working-flap interruptions and exact throughput gain
- Gathered orphan drone behavior during the two-second stale-registration window
- Current save/load during debounce, uninstall orphan gate, enable/reload and 1.0.7 runtime
