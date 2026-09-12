# LandscapeUnitFilter - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

- Site row and registered module title still name boarding colonists; entry has explicitly corrected this to drones since2026-07/08

- F115 entry front/current tag still claims gate-only and no repair, despite hotfix2 recopied/rearmed1.1.0body; append current entry-home note without promoting cure status

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_LandscapeUnitFilter.lua | F34(d), F115 | yes: direct final registry line 249 active | yes: ClearWasteRock site collects units and ScatterUnitsUnderneath issues ExitImpassable | no: affected Embark units are drones, not colonists; RCCommander route still exists | n/a: no dedicated metadata headline; registered title has same colonist overclaim | KEEP-BUT-FIX-CLAIM | 1.1.0.403908 Lua/Landscape/Landscaping.lua:517; 1.1.0.403908 Lua/Landscape/Landscaping.lua:522; 1.1.0.403908 Lua/Landscape/ClearWasteRockConstructionSite.lua:81; 1.1.0.403908 Lua/Buildings/ConstructionSite.lua:1915; 1.1.0.403908 Lua/Buildings/ConstructionSite.lua:1928; 1.1.0.403908 Lua/Units/RCRover.lua:279 | SOURCE | Current live RCCommander drone embark plus landscaping mark and dedup behavior; Full current Embark-setter and obstruction path inventory across DLC/remaster; Current landscaping cure and F115 in-play no-throw control, menu enable/reload, save/load/uninstall; Actual1.0.7 branch decline and runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current LandscapeForEachUnit :517 still builds the valid/not-passed/not-Embark filter, but :522 gives Landscape_ForEachObject raw callback. ClearWasteRockConstructionSite :81 collects through that global; ScatterUnitsUnderneath :1915 reads the list and :1928 sends ExitImpassable. This is the actual consumer lost filtering/dedup still affects.

- The map/signature movement was repaired by hotfix2: current module copy uses map.Landscapes[mark] and corrected filter callback. Boot active means both branch gates/probe passed. Current source matches the two manifest spans; do not rederive/re-copy what hotfix2 cleared.

- RCRover:DroneEnter :279 still sets Embark on its drone argument. Source searches on current Colonist/Train/Shuttle files do not find a colonist Embark setter. F34 entry2026-08-12 already records the actual RCCommander drone route and historical owner staging, distinguishing rocket obstructions/fictional train-shuttle routes. This sweep does not elevate that historical route witness into a current live cure.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:242-251 says colonists yanked out of vehicles. The module registered title still repeats boarding colonists. Queue drone/RCCommander wording through held release/public workflow; no loadable title or public file edited here.

- F34(a/b/c) remain unpatched. F115 own-defect entry still prominently says gate-only/no-repair; current hotfix2 body and installation supersede that build-state claim. Append current-game source/build-state note and preserve original reproduction/gate record; no tested status promotion.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:249` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current live RCCommander drone embark plus landscaping mark and dedup behavior
- Full current Embark-setter and obstruction path inventory across DLC/remaster
- Current landscaping cure and F115 in-play no-throw control, menu enable/reload, save/load/uninstall
- Actual1.0.7 branch decline and runtime
