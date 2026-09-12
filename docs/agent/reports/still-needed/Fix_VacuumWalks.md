# Fix_VacuumWalks review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — card scope is less precise than the site row:** the headline in
  `metadata.lua:3` says “Colonists walked across the surface between domes and
  suffocated,” and the introductory example likewise mentions inter-dome
  suffocation without the passage condition. The module repairs bypassing an
  **available passage on a short positive-distance outside route in vacuum**;
  it still allows a surface walk when no passage exists. The site row at
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:46`–`:55` already describes the
  passage the player built and is sound within that scope.
  **INFERRED — reader risk:** under “SOME OF WHAT IT FIXES,” the unqualified card
  example can be read as repairing inter-dome suffocation generally. It is a
  true description of the original passage-bypass defect, rather than a proven
  false occurrence claim. Recommend adding the condition, for example:
  “Colonists ignored an available passage, walked between domes across the
  surface, and could suffocate.” Apply the same scope to the introductory example.
  This is a wording recommendation, not a newly filed defect.
- **SOURCE — no disagreement with the existing migration PARTIAL assessment:**
  `MIGRATION_DEV_REPORT.md:192`–`:229` and `MIGRATIONFIX_AUDIT.md:117` correctly
  retain the no-passage oxygen risk. This review does not reopen the hotfix-2
  re-copy or propose changing that designed fallback.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_VacuumWalks.lua | F52 | yes — fresh boot applied; settled direct registry active | yes — ordinary emigration calls the patched method, and TransportByFoot consumes the passage path | yes — row describes the available built-passage case; cure unverified on 1.1.0 | partial — true for passage bypass; standalone headline and intro omit the available-passage condition | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1903; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2018; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:3553; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:4577 | SOURCE | organic short-route passage use; death prevention; no-passage deaths; entrance queue timing; breathable and negative-distance controls in play; shuttle-owned task and long passage-chain controls in play; 1.0.7 runtime decline; whole-list card claims |

## Primary evidence

- **MEASURED installation, not cure:** the settled second boot logs
  `VacuumWalks: applied` at
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:91`.
  The coordinator's direct settled registry read measures active at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:236`.
  No colony loaded or suite ran. The module's SHA256 matches `CENSUS.json`:
  `a05c14f891a856d2c98d61f47d241263eb3bdea48718e25dfaf0c3da7ff05948`.
- **SOURCE — primary caller remains:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2006` obtains the
  chosen dome and transport mode; `:2018` calls `TryToEmigrateToDome` with those
  values. `FindEmigrationDome` uses the transport-mode selector at `:3525`.
  `FindTransportationModeToCommunity_BeforeTrains` returns walking mode and
  distance when walkable at `:3113`–`:3115`.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Dome.lua:220`–`:230`
  bounds the outside foot route by the walk cap. The default cap remains 400m at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/_GameConst.lua:149`.
- **SOURCE — the faulty threshold persists and its consumer has not drifted:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1903` still uses
  the dome walk cap as the vacuum passage-lookup threshold, and `:1908` asks for
  a passage only above it. A short positive outside distance therefore misses
  the lookup. The module changes that vacuum threshold to zero at
  `Code/Fix_VacuumWalks.lua:238`, obtains the path at `:245`, and forwards it to
  the same foot command. The primary game consumer receives it at
  `Lua/Units/Colonist.lua:1927`; `:3548` tests for it, `:3551` enters its first
  dome, and `:3553` enters the subsequent path domes. The path provider still
  checks network membership at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Passage.lua:1300` and returns the
  dome sequence at `:1328`.
- **SOURCE — retained sibling branches and limits:** the copied body preserves
  the work-reservation computation (`Lua/Units/Colonist.lua:1896`), shuttle-owned
  task guard (`:1898`), negative-distance conversion (`:1904`–`:1906`), train
  ticket discard (`:1918`), task retargeting (`:1950`), and landing-slot-aware
  request creation (`:1959`–`:1970`). Negative-distance pairs already trigger a
  passage lookup in vanilla; breathable maps retain the original threshold.
  The passage-chain/shuttle choice remains at `:1914`–`:1916`; this module does
  not promise passage use for every route under every transport precondition.
- **SOURCE residual / INFERRED harm frequency:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1914` still selects
  foot transport when the passage path is absent, and `:1927` passes the absent
  path. The module retains that branch at `Code/Fix_VacuumWalks.lua:249`.
  Neither this decision nor `TransportByFoot` checks elapsed outside time.
  The ordinary outside timer starts at `Lua/Units/Colonist.lua:3018`, and
  `:4577`–`:4578` still applies outside suffocation when its oxygen-time limit
  is reached in a non-breathable atmosphere. Actual delays, loss of Health,
  deaths, and their frequency on 1.1.0 were not observed here.

## Not checked, by name

- Organic short positive-distance migration using an available passage on 1.1.0.
- Oxygen loss, Health loss, or death prevention in a running colony.
- Actual no-passage suffocation/deaths or their frequency on 1.1.0.
- Entrance queues, route detours, movement duration, or a safe oxygen-budget cap.
- Breathable-map and negative-distance passage-only controls in play.
- Shuttle-owned tasks, elevator moves, and long passage-chain controls in play.
- Fresh runtime decline on 1.0.7.
- Whole-list card consistency and generic card claims, assigned to the coordinator.
