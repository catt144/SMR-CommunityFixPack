# JumboCaveReinforcementWedge - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_JumboCaveReinforcementWedge.lua | F110 | yes: direct final registry line 267 active | yes: rock deletion removes blocker and readiness advances construction to scenario label | yes: drone-proven unreachable rock remains blocker outside vanilla permanent-building cleanup | yes: JumboCave waste-rock wedge headline supported | KEEP | 1.1.0.403908 Lua/WasteRock.lua:330; 1.1.0.403908 Lua/Units/Drone.lua:926; 1.1.0.403908 Lua/WasteRock.lua:129; 1.1.0.403908 Lua/Buildings/ConstructionSite.lua:534; 1.1.0.403908 Lua/Buildings/ConstructionSite.lua:631; 1.1.0.403908 Lua/Scenario/BuriedWonder_Jumbo_Cave_106.generated.lua:104; 1.1.0.403908 Lua/WasteRock.lua:182 | SOURCE | Fresh1.1.0 JumboCave geometry producing stranded rock and organic proactive cure; Current NewHour timing/drone attempt availability and field-save heal; Current permanent-building cleanup residual incidence and stockpile controls; Current behavior firing, menu enable/reload,save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current WasteRock approach :330 chooses ring angle randomly and :338 paths to it; Drone:ApproachWrapper :926 still marks failed targets unreachable. Current table uses timestamp/LRU and per-map version rather than old GameTime+maxint value; module only asks presence, so the representation change retains its reader.

- WasteRock OnDeleted :129 calls each valid parent construction OnWasteRockObstructorCleared; ConstructionSite :534 removes the rock, :631 tests remaining list, :598 transitions when clear. Scenario Jumbo106 :104 still waits for completed Reinforcement label; old Jumbo :103 has sibling wait. Both NewHour proactive and LoadGame reactive passes target same live blocker consumer.

- Vanilla now also deletes rocks underneath permanent buildings at ConstructionSite :371 and save-fixup :3194. WasteRock:IsUnderneathPermanentBuilding :182 requires a Building on the rock hex; that does not cover arbitrary impassable cave geometry, nor is it based on drone-proven unreachability. The replacement is partial, not an all-stranded-rock cure. Current geometry/field1.1.0 occurrence remains unmeasured.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:510 and metadata headline describe a reinforcement stuck on unreachable waste rock and conditional clear. Module intentionally waits for a drone attempted/flagged rock; no drone attempt means no clear. Historical field-save attended cure remains1.0.7 evidence and EF079 prevents importing that save to1.1.0.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:267` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Fresh1.1.0 JumboCave geometry producing stranded rock and organic proactive cure
- Current NewHour timing/drone attempt availability and field-save heal
- Current permanent-building cleanup residual incidence and stockpile controls
- Current behavior firing, menu enable/reload,save/load/uninstall,1.0.7 runtime
