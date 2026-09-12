# Fix_LakeEntombment review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — narrow the site's exemption explanation:** the current scatter
  exemption requires RCConstructorBase, command Construct, and
  `construction_clearing == self` (`ConstructionSite.lua:1918`). That is the
  obstruction-clearing constructor, not every rover performing normal build
  work. RCConstructorBase sets that field during clearing at `:216`, clears it
  at `:233`, and later calls normal `RoverWork` at `:314`. The site at
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:233`–`:235` broadly says the pass
  exempts "the rover doing the building". Recommend **KEEP-BUT-FIX-CLAIM**:
  qualify this branch as obstruction clearing; keep the independent pre-basin
  timing problem and post-basin rescue separate.
- **SOURCE — agent/module prose is not the implemented scope:** F30's entry says
  a bbox sweep and teleport, but `Code/Fix_LakeEntombment.lua:58` scans the whole
  map for Unit objects and `:61` only assigns ExitImpassable. The current escape
  consumer uses a nearby passable point and `Goto(pt, "sl")`, not a new
  lake-specific teleport. The module header's battery-to-Freeze chain is also
  incorrect on current source: Drone battery depletion chooses NoBattery,
  whereas Freeze is entered by cold progress. The site's "ran out of power"
  wording does not have that error. No code/entry/public edit is made here.
- **SOURCE conditions / LIMIT:** the wrapper rescues valid, non-destructing,
  unheld Units with a valid position which the map reports impassable. It does
  not test lake membership or IsDead, and it can affect already-stuck units
  elsewhere on that map. ExitImpassable returns if no passable destination is
  found. The public post-fix outcome describes the intended normal rescue;
  current live movement, command acceptance and global side effects remain
  unmeasured, rather than a newly filed failure or retirement reason.
- **SOURCE — headline and veto ID agree:** the card's artificial-lake headline
  matches the remaining timing defect. Its `SMRFixPack_Disabled["LakeEntombment"]`
  example names this module's actual registration ID and the core checks that
  keyed table before applying the module. No save veto or separate old-save
  healer exists in this module; the game's rover-only save fixup is mitigation
  at a different lifecycle point.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_LakeEntombment.lua | F30 | yes — fresh boot applied and direct settled registry active | yes — lake GameInit calls wrapped PlacePrefab; assigned ExitImpassable dispatch reaches rover/drone wrappers and Unit nearby-point/straight-line escape | partial — pre-basin timing/rescue fits, but scatter exemption is only the obstruction-clearing constructor and successful escape has destination/eligibility conditions | yes — artificial-lake headline fits; keyed veto example uses actual LakeEntombment ID | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/LandscapeLake.lua:34; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/LandscapeLake.lua:343; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/ConstructionSite.lua:1918; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Unit.lua:777 | SOURCE | live lake construction and movement; footprint/passability geometry; command acceptance and destinations; already-stuck units elsewhere; held/dead units; old-save or veto runtime; fresh 1.0.7 behavior |

## Primary evidence

- **MEASURED installation, not cure:**
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:85`
  reports applied. Direct settled registry read at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:231`
  measures active. Both packs and TestKit were enabled; no colony loaded or lake
  built. Captured module SHA256:
  `35bc9237b92f43803ad5b01d9bcea4b896881617ec8566fa88d2476d28991e1d`.
- **SOURCE — current caller and post-basin seam:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/LandscapeLake.lua:32`–`:35`
  calls PlacePrefab from GameInit. The current body places the terrain prefab at
  `:287`, handles missing-prefab/error early returns at `:276`–`:290`, updates
  visuals at `:342`, and ends by rebuilding passability at `:343`. It contains
  no Unit rescue pass. The pack's chained post-wrapper calls that original
  first at `Code/Fix_LakeEntombment.lua:53`, then scans/commands eligible units
  at `:58`–`:61`. Both the call and the passability seam still exist. The post-pass
  also runs after an early-returning original call; no failed-prefab path was
  exercised here.
- **SOURCE — timing branch remains independent of the clearing exemption:**
  current `Lua/Buildings/ConstructionSite.lua:1712` creates the completed building
  through PlaceBuildingIn. `:1766` scatters units before the GameInit work which
  the same primary body explicitly describes as called from a thread at
  `:1770`–`:1771`. Lake GameInit subsequently creates/rebuilds its basin at the
  seam above. The old scatter assigns ExitImpassable at `ConstructionSite.lua:1928`;
  current `Lua/Units/Unit.lua:740`–`:742` returns when its current position is
  passable and no dome was requested. A pre-basin scatter therefore cannot
  enforce escape from the later basin. This source timing mechanism supports
  keeping the post-basin rescue; no in-play recurrence was measured.
- **SOURCE — exact exemption and normal constructor work:** current
  `ConstructionSite.lua:1918` only exempts an RCConstructorBase whose command is
  Construct and whose `construction_clearing` equals this site. Current
  `Lua/Units/RCConstructorBase.lua:211`–`:216` sets the field for obstruction
  clearing; `:233` clears it before ordinary work at `:314`. The ordinary
  `ConstructionSite:RoverWork` path invokes Complete from its destructor at
  `ConstructionSite.lua:1567`–`:1573`. Thus this explicit exemption is not proof
  that the normal finishing builder is always exempt. The wrapper covers the
  timing branch without depending on which earlier scatter branch ran.
- **SOURCE — command consumer and rover/drone siblings:** current
  `CommonLua/Classes/CommandObject.lua:250` executes the selected command method.
  `Lua/Buildings/BaseRover.lua:93`–`:99` forwards ExitImpassable through
  DroneBase and additionally ejects a rover from a dome. Current
  `Lua/Units/DroneBase.lua:109`–`:115` forwards to Unit and additionally handles
  a dome construction site. `Lua/Units/Unit.lua:770` / `:772` obtains a nearby
  passable point, `:774`–`:775` returns if none exists, and `:777` performs
  `Goto(pt, "sl")`. These are still the primary consumers of the command the
  wrapper assigns; no lake-specific teleport is inserted. Existing drone
  MoveSleep at `Lua/Units/Drone.lua:1747` excludes ExitImpassable from movement
  battery usage, so that command-specific consumer remains too.
- **SOURCE — power/"dead" precision:** current `Drone.lua:1768`–`:1778` chooses
  EmergencyPower or NoBattery based on battery level. Cold progress chooses
  Freeze at `:1717`, and `:1723`–`:1730` defines the freezing command. Current
  `Drone.lua:3083`–`:3084` reports IsDeadUI only for command Dead. The field-report
  phrase "reading as dead" is not promoted into a measured present-day IsDeadUI
  discriminator by this sweep.
- **SOURCE — existing save fixup is a separate mitigation:** current
  `Lua/Buildings/BaseRover.lua:764`–`:771` defines
  SavegameFixups.FixStuckRoversInDomes2. It iterates BaseRover objects on loaded
  maps, excludes dead rovers, and assigns ExitImpassable to those in domes/sites
  or on impassable ground. It does not cover drones and is not called by the
  current Lake PlacePrefab body. This fixup's continued presence does not replace
  the immediate post-basin Unit pass; the module supplies no LoadGame handler.
- **SOURCE — public row/headline/veto:** site
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:229`–`:240` describes the lake
  symptom, pre-basin scatter and game escape outcome; `:233`–`:235` needs the
  clearing-exemption qualification above. The artificial-lake bullet and veto
  example both live in `metadata.lua:3`. The exact ID is registered at
  `Code/Fix_LakeEntombment.lua:41`; `Code/00_Core.lua:510`–`:513` declines
  application for a truthy keyed veto. This is source verification of the
  shipped example, not a new veto execution test.

## Not checked, by name

- Actual lake completion, rover/drone entombment recurrence or successful rescue,
  motion, power survival or screenshots in a running colony.
- Native prefab/terrain geometry, footprint clearance, straight-line path behavior,
  nearby destination availability or passability refresh timing in play.
- ExitImpassable acceptance for uninterruptible commands, queued jobs, held units,
  already-dead/depleted units, or destructor effects after reassignment.
- Map-wide effects on units already impassable elsewhere, or failed/missing-prefab
  calls which still trigger the wrapper's post-pass.
- Fresh old-save recovery/save-fixup invocation, separate historical lake healing,
  uninstall behavior or a runtime veto test.
- Fresh 1.0.7 source/runtime comparison, every lake size/skin or foreign overrides.
