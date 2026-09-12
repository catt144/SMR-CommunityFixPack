# Fix_LayoutTechLock review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retirement.

## Disagreements first

- **SOURCE — vanilla now supplies the research/prefab gate on the normal entry
  route:** `GetLayoutConstructionMissingBuildings` checks every layout building
  for a research lock and sufficient owned prefabs. `GetLayoutConstructionLockedReason`
  reports missing entries; `UIGetBuildingPrerequisites` disables the layout before
  construction opens. The build shortcut uses that same gate. The pack's inner
  filter still works, and its consumers remain, but it is redundant with this
  new outer gate on the normal 1.1.0 route. This conclusion comes from the primary
  caller trace below; `PACK_1_1_0_REVERIFICATION.md:116` / `:156` already records
  the same A-5/K-35 redundancy, rather than granting an independent clearance.
- **SOURCE — public latent classification needs correction:** the site row at
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:611`–`:614` describes layout research
  bypass as one of three currently hidden defects (`:593`). On current 1.1.0,
  ordinary build-menu exposure of a future layout inherits the generic outer
  gate too; changing only its list of buildings does not bypass that gate
  at ordinary menu admission. Whole-layout prefab construction is deliberately
  exempt in both vanilla and this filter. Repeat placement is not a fresh filter
  invocation; it provides no additional repair for later inventory/research loss.
  Counting this row as a current repair hidden solely by shipped layout values
  is unsupported by the current caller. Recommend **RETIRE** for 1.1.0 normal
  play, or an explicit owner decision to retain a differently described inner
  guard. The coordinator owns the aggregate count and public edits.
- **SOURCE — the header's old latency explanation is false:**
  `Code/Fix_LayoutTechLock.lua:30`–`:35` says no layout entry has a tech requirement.
  The current populated layout has two Moisture Vaporators, and current
  `Data/Tech.lua:9642` unlocks them through Moisture Farming. Their unlocked
  resupply prefab route is what the old inner loop handles correctly. F43's
  2026-07-30 audit already refuted the no-tech-lock explanation; do not reuse it.
- **SOURCE rider / LIMIT:** F118 restores delete-on-load registration which
  this module's own teardown can clear. It does not provide an independent
  historical save healer. Removing the filter also removes this induced
  teardown; vanilla retains its layout registration. F118's player effect and
  the rider's in-play cure remain unmeasured; neither status is promoted.

**INHERITED constituency / scope limit:** the owner explicitly treats players on
1.0.7 receiving the live portal pack as a real population. This recommendation
establishes redundancy for the inspected current base 1.1.0 admission/activation
route; it does not establish that the inner guard could benefit nobody on 1.0.7.
That broader retention decision remains with the owner. Inventory loss between
a cached menu admission check and activation, custom entry routes, and live DLC
overrides are named limits below, rather than proof of universal redundancy.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_LayoutTechLock.lua | F43, F118 | yes — fresh boot applied; direct settled registry active | yes — placement reads skip_items/controllers and post-load reads restored registration; current base outer gate already prevents unsupported locked-entry admission, and whole-layout prefab builds bypass the filter too | no — current under-hood row omits vanilla's generic outer gate and treats this as a data-hidden current repair | partial — no dedicated headline; inclusion in aggregate three hidden repairs unsupported for this module on inspected base 1.1.0 entry route | RETIRE | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/LayoutConstruction.lua:215; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/X/BuildMenu.lua:784; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/LayoutConstruction.lua:451; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/Construction.lua:1054 | SOURCE | actual layout construction; runtime populated preset/cargo inventory including DLC overrides; custom scripted entry routes; inventory changes between cached menu gate and activation or during open dialog; F118 save/load cure and screen effect; live portal pack benefit on 1.0.7; complete aggregate hidden-repair count |

## Primary evidence

- **MEASURED installation, not benefit:** settled second boot logs applied at
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:116`.
  Direct settled registry read measures active at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:258`.
  No colony loaded or suite ran. The module matches the captured SHA256:
  `b89952744f452db50ec2ad04be35e31de6de18571949b0ecfe0312f0373923f2`.
- **SOURCE — current populated layout and prefab/tech data:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Data/LayoutConstruction.lua:5` identifies
  `SelfSufficientDome`; `:58` identifies the empty `testing` preset. The populated
  preset has nine entries and seven unique templates, with Moisture Vaporator
  at `:21` and `:38`; it is referenced by
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Data/BuildingTemplate/SelfSufficientDome.lua:4`.
  Current `Data/Tech.lua:9641`–`:9642` applies `Effect_TechUnlockBuilding` to
  Moisture Vaporator; the other layout template names appear as modifiers or
  upgrades, rather than building unlock effects. That effect records the
  requirement at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/MarsGameEffects.lua:47`.
  The vaporator template requires prefabs at `Data/BuildingTemplate/MoistureVaporator.lua:32`;
  its cargo preset at `Data/Cargo.lua:327`–`:336` has no lock or custom verifier.
  Cargo defaults to unlocked at `Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:177`;
  its default verifier returns true at `:160`. Current sponsor lock definitions
  do not name Moisture Vaporator. Thus the shipped inner loop already skips
  unresearched vaporators lacking owned prefabs; it does not need the pack for
  that populated case.
- **SOURCE — replacement gate and ordinary callers, independently traced:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/LayoutConstruction.lua:208`
  exempts a whole-layout prefab. Otherwise `:215` checks each building's tech
  status, and `:228` compares the number of missing buildings with owned
  prefabs. `:270` obtains that missing list and `:296` returns the lock text.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/X/BuildMenu.lua:743` calls this
  layout-specific lock helper; `:784`–`:786` sets `can_build = false` for its
  lock reason. The action refuses disabled non-prefab construction at `:845`
  before mode activation at `:859`. The primary shortcut at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/XDef/GameShortcuts.generated.lua:2069`
  obtains the same prerequisites and passes `can_build` into that action at
  `:2082`. Generic mode startup then calls the selected controller's `Activate`
  at `Lua/Construction/Construction.lua:303`.
- **SOURCE — whole-layout prefab and repeat-placement routes:** the menu action
  sets `params.prefab = true` for an owned whole-layout prefab at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/X/BuildMenu.lua:839`.
  Layout activation copies that flag at `Lua/Construction/LayoutConstruction.lua:316`;
  the pack immediately exempts it at `Code/Fix_LayoutTechLock.lua:75`, matching
  vanilla's inner permission at `LayoutConstruction.lua:339`. Placement passes
  the package flag and avoids consuming per-building prefabs at `:480`–`:481`,
  consumes one package at `:494`, and closes the dialog when the package supply
  is exhausted at `:495`–`:507`. There is no filter-induced difference on this
  deliberately allowed path. Multiple-placement clicks call the existing
  controller's `Place` at `Lua/Construction/Construction.lua:394` and close only
  according to `:397` / `:213`–`:215`. Layout `Place` calls `PlaceCursors` at
  `LayoutConstruction.lua:562`; it does not call `Activate` or this filter again.
  Owned-prefab/skip decisions remain cached from activation (`:321`–`:343`).
  Thus subsequent research or prefab loss is not repaired by the filter either.
  **LIMIT / INFERRED:** an inventory change between a cached menu check and
  activation could admit a future non-purchasable locked entry that the filter
  subsequently catches. No such race, custom layout, or live DLC override was
  reproduced. The current populated layout's unresearched vaporators already
  receive vanilla's narrow inner prefab check.
- **SOURCE — inner expression and all changed consumers remain:** the original
  narrow inner decision still exists at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/LayoutConstruction.lua:338`–`:339`.
  The pack writes `skip_items[entry]` and removes the controller at
  `Code/Fix_LayoutTechLock.lua:123`–`:124`. `PlaceCursors` still reads the skip
  marker at `Lua/Construction/LayoutConstruction.lua:451`, obtains the controller
  at `:456`, and places through it at `:484`. Other preview/status/rotation loops
  iterate the retained controller table. These are live consumers; redundancy
  arises from the outer admission check, not from a removed placement reader.
- **SOURCE — F118 sibling fully separated:** vanilla registers the layout for
  delete-on-load at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Construction/LayoutConstruction.lua:385`.
  Sub-controller teardown clears the registration at
  `Lua/Construction/Construction.lua:1227`. The pack remembers it at
  `Code/Fix_LayoutTechLock.lua:118` and restores it only if it was the layout
  itself at `:144`–`:145`. The primary persisted-state consumer at
  `Lua/Construction/Construction.lua:1053`–`:1056` deletes the registered object
  on post-load and clears the variable. This rider preserves vanilla behavior
  when the wrapper tears down a controller; it is not a separate reason to keep
  a redundant parent filter.

## Not checked, by name

- Actual layout placement or research enforcement in a running colony.
- Runtime layout/cargo/tech preset inventory, including DLC overrides; current
  archived base data was inspected, not a live colony's resolved preset tables.
- Custom scripted `SetMode`/controller entry routes or custom lock callbacks.
- Live inventory changes between a cached menu gate and activation, or while an
  already-open layout dialog persists; the repeated placement caller was inspected.
- F118 save/load cleanup cure, leaked-controller state, cursor/ghost effect, or screen result.
- Fresh 1.0.7 runtime behavior and benefit for players receiving the live portal
  pack on that game version; their constituency is not excluded by this recommendation.
- Complete aggregate count of the other under-hood repairs; only F43's contribution assessed.
