# Fix_ExoticDepositSign — one-module still-needed review

Task/agent: `/root/module_a` · assigned module `Code/Fix_ExoticDepositSign.lua` · entry F102 · anchor `2983fac`.
Captured input: CENSUS module sha256 `4deeb3026468d8f617b9bfae5241e8dfb092c235ebc38bd8fb683df1f76f28b9` (current bytes match). CENSUS capture anchor is `8469ae453b3d6312128ab187f38305f62fa41b92`; the requested review anchor remains `2983fac`.

No disagreement or consumer drift established. The fresh settled boot resolves the sweep prompt's unknown active/inactive state: this module applies on 1.1.0. **KEEP is a recommendation under the existing disclaimered-cure decision.** The sign retarget remains consumed; that establishes a live effect, not an affected-hardware cure. The site's art/material assertions have not been independently renewed against 1.1.0's non-Lua packs, so row truth is partial rather than claiming that inspection happened.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ExoticDepositSign.lua | F102 | yes — archived settled boot line 125; no later module message | yes — UpdateEntity reads class entity; GameInit and LoadGame converge signs; locked deep deposits use unchanged disabled_entity | partial — retarget/gameplay/disclaimer supported; current material claims and affected-hardware harm not reverified | n/a — no dedicated card headline bullet | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/SubsurfaceDeposit.lua:395 | SOURCE | affected Linux/NVIDIA cure; current art/material/shader packs; 1.1.0 colony-load/render/uninstall; enable/reload path; exhaustive travel callers; whole-card/counts |

Primary evidence (all game paths below are pinned to **1.1.0.403908**):

- `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/SubsurfaceDeposit.lua:517` still declares `SubsurfaceDepositPreciousMinerals.entity = "SignPreciousMineralsDeposit"`. The replacement was not wired into this vanilla class. The sibling path at `:518` remains `SignUnexploitablePreciousMinerals` and is deliberately untouched.
- `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/SubsurfaceDeposit.lua:394` looks up `g_Classes[self.class]`; `:395` chooses that class's normal entity when depth is shallow or deep extraction is enabled, otherwise its disabled entity; `:396` calls `ChangeEntity(ent)`. This is the actual consumer of the module's one changed default, and it has not stopped reading it.
- New deposits retain the route: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Exploration.lua:421` calls `marker:PlaceDeposit`; `Lua/Buildings/DepositMarker.lua:162` dispatches `SpawnDeposit`; `Lua/Buildings/SubsurfaceDeposit.lua:97` places the class derived from the marker resource, carrying max amount/grade/reveal state; `Lua/Buildings/SubsurfaceDeposit.lua:228` runs `UpdateEntity` from `GameInit`. The module changes neither the marker resource nor those data fields.
- The second subfix remains reachable on load: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/Savegame.lua:808` emits `LoadGame` after successful engine load; `CommonLua/Core/map.lua:1125` defines `AllMapsForEach` and `:1127` forwards the filter/callback into each loaded map's `MapForEach`. The module's `WhenActive`-guarded handler calls each matching object's `UpdateEntity`. Vanilla independently uses the same class-filter-and-`UpdateEntity` convergence pattern at `Lua/Buildings/SubsurfaceDeposit.lua:473` and `:475` when extraction flags change. No colony loaded in this boot, so this is source reachability rather than a measured 1.1.0 sweep.
- Gameplay consumers still use resource/class/state: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/PreciousMineralsExtractor.lua:4` declares the deposit class and `:5` the exploitation resource; `Lua/Buildings/Deposit.lua:104` compares the exploiter resource and depletion state; `Lua/Buildings/SubsurfaceDeposit.lua:336` adds deep-extraction gating and `:338`–`:340` reveal/range checks. Amount extraction at `SubsurfaceDeposit.lua:301`–`:310` reads and updates amount/resource without using the entity string. The patch alters only the class entity and invokes vanilla entity refresh.
- A concrete normal-play data route remains: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Data/RandomMapPreset.lua:1529` selects `AsteroidDType_ExoticMinerals_High` for the D-type asteroid preset; `Data/ResourcePreset.lua:79` names resource `PreciousMinerals`, `:89` supplies three shallow deposits, and `:91` also supplies a deep deposit. The unchanged deep disabled-entity branch is a named coverage boundary, not a newly inferred defect.
- Runtime installation: `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:55` identifies build 1.1.0.403908; `:125` logs `ExoticDepositSign: applied`. This means its replacement-entity existence and original-default checks passed. No later F102 data/heal message appears. Both packs and TestKit were enabled; no colony or suite ran.
- Public surfaces: `C:/Dev/SMR-CommunityMods/content/fix-list.md:461`–`:475` describes the retarget and explicitly says the cure cannot be confirmed. That caveat remains necessary. `metadata.lua:3` has no F102-specific headline bullet. The generic whole-card assertions belong to the coordinator's separate surface pass.

What I did **NOT** check, by name:

- Freeze reproduction or cure on affected Linux/NVIDIA/Proton hardware on 1.1.0.403908.
- Current Materials.fpk vertex-animation uniqueness, replacement material cleanliness, mesh/texture parity, or shader/native renderer changes.
- 1.1.0 colony-load re-sign sweep, rendered/selectable sign, or uninstall playtest.
- Main-menu enable/reload path on 1.1.0.
- Whole-card consistency, repair counts, or other registered modules.
- Exhaustive enumeration of all discovery, map-generation, tutorial, and asteroid-travel callers.
