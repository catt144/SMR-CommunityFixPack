# Fix_SilentHitMomentFX review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — no material row/card disagreement found:** all seven named machines
  retain the tracker-to-FX consumer paths. Seven is the count of player-facing
  units, not entity groups or preset IDs: Water Extractor's two skins give eight
  entity groups, and Shuttle's four animations bring the installed total to
  eleven presets. The site row's skin caveats and card's seven-machine paragraph
  agree with this scope. Recommend **KEEP**.
- **SOURCE precision limit:** this restores the named effects, not every authored
  FX row. The hammer has two Hit markers; the original tracker cycles over their
  count and therefore emits `hit-moment1` and `hit-moment2`. Authored hammer rows
  keyed to `hit-moment3` or `hit-moment4` are not newly made reachable. Neither
  site nor card promises every authored row. Existing non-moment loop/start/end
  sounds also mean a machine can make other sounds before this repair.
- **MEASURED versus INHERITED:** this sweep measures installation and eleven
  missing preset additions on fresh main-menu boots, not the in-colony cure.
  C74 and C77 retain their earlier `tested-attended` receipts from 2026-09-10,
  including packed-module old-save replacement without a power cycle. Those
  historical results are inherited, not rerun or promoted by this sweep.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_SilentHitMomentFX.lua | C74, C77 | yes — fresh boot applied, eleven missing presets registered, direct final registry active | yes — both original trackers read added moments and emit matching current FX actions/moments; Water animation update and four old-save restarts still call those consumers | yes — seven named units and skin/old-save conditions fit current paths | yes — seven-machine paragraph counts player-facing units and qualifies hammer/MOXIE skins | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/Classes/AnimMoment.lua:8; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/BaseBuilding.lua:1074; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Building.lua:3385; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/WaterExtractor.lua:115 | SOURCE | live FX, timing/synchronization, current old-save healing, uninstall/save round trip, third-party presets/overrides, fresh 1.0.7 runtime, every unrelated animation consumer |

## Primary evidence

- **MEASURED installation:**
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:127`
  reports applied and `:155` reports eleven missing animation-moment presets
  registered. Direct settled registry read at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:268`
  measures active; `:152` independently reports the same eleven additions.
  Both packs and TestKit were enabled; no colony loaded or game FX fired.
  Captured module SHA256:
  `1acd92c6b8a09bd4232407d665c029b981b282a974e5271bcb07a532055477ff`.
- **SOURCE — lookup and current preset cases:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/Classes/AnimMoment.lua:5`–`:16`
  reads only `Presets.AnimMetadata[anim_entity][anim].Moments`; `:8` indexes by
  the supplied animation key and `:36` forwards it without index conversion.
  The current base `Data/AnimMetadata.lua:13`, `:60`, `:71`, `:81` names only
  Advanced Stirling Generator and three cave-in groups; the current DLC preset
  at `DLC/norman/Presets/AnimMetadata.lua:166` names BakeryHands. None names the
  eight patched groups. The fresh eleven-addition log independently confirms
  that all exact group/id cases were absent after the loaded data pass.
  `Code/Fix_SilentHitMomentFX.lua:127`–`:135` preserves an existing group/id;
  `:286` registers the data-ready pass. Current `CommonLua/Preset.lua:571` appends
  a preset object and `:575` replaces the named slot, so the absence guard still
  prevents duplicate registration.
- **SOURCE — shared consumers remain:** current
  `Lua/Buildings/BaseBuilding.lua:1045`–`:1048` feeds a numeric animation index
  to the name-keyed lookup and exits when count is zero; `:1053` and `:1065`
  repeat that argument shape. `:1074` emits the chosen `Working` hit moment with
  the building actor and animated attach target. Current
  `Lua/Buildings/Building.lua:3347` correctly converts to the state name;
  `:3369` reads all moment names and `:3383`–`:3387` waits/emits each matching
  action/moment. Thus the C74 conversion and the C74/C77 added metadata are both
  still consumed. The conversion is restricted to the hammer/MoxiePump classes
  at `Code/Fix_SilentHitMomentFX.lua:310`–`:315`; Metatron remains outside it.
- **SOURCE — Rare Metals Extractor hammer:** current
  `Lua/Buildings/MetalsExtractor.lua:25` enables the multiple-hit tracker with
  the `hit-moment1`–`hit-moment3` override; `BaseBuilding.lua:929` / `:947` starts
  it during working-animation selection. Current
  `Data/FXPreset/ActionFXSound.lua:17156` / `:17187` and
  `Data/FXPreset/ActionFXParticles.lua:860` / `:897` match the reachable first
  two moments with target UniversalExtractorHammer. The two added Hit markers
  feed that consumer. The tracker limits its cycle to `number_of_hits` at
  `BaseBuilding.lua:1054`; authored later hammer rows at
  `ActionFXSound.lua:17208` / `:17229` are not all restored. Current template
  `Data/BuildingTemplate/PreciousMetalsExtractor.lua:34`–`:35` retains both skins,
  with the card's seven default-drill sponsors at `:4`–`:12`.
- **SOURCE — MOXIE classic pump:** current `Lua/Buildings/MOXIE.lua:5` enables
  that same tracker. Current `ActionFXSound.lua:17136` / `:17177` target MoxiePump
  at `Working` / `hit-moment1` / `hit-moment2`; particles at
  `ActionFXParticles.lua:844`–`:854` and `:879`–`:891` use the supplied attach
  target's Steam2/Steam1 spots. Numeric conversion plus the two working Hit
  markers supplies these readers. Current `Data/BuildingTemplate/MOXIE.lua:28`–`:29`
  retains Moxie and MoxieCP3 skins; the module does not add MoxieCP3Pump markers.
- **SOURCE — Water Extractor, both pump skins:** current
  `Lua/Buildings/WaterExtractor.lua:113`–`:115` selects the pump and starts
  `TrackAllMoments(pump, "working", self)`. Matching building-actor sounds remain
  at `ActionFXSound.lua:20286` / `:20296`; the inherited MicroG auto-water actor
  has another matching row at `:20276`. Both WaterExtractorPump and
  WaterExtractorCP3Pump working presets are installed. Current
  `BaseBuilding.lua:1092` queues the working-animation update; `:945` restores
  animation speed during it. `AnimMoment.lua:117`–`:118` still returns max_int
  for zero combined speed. The module's post-update wrapper at
  `Code/Fix_SilentHitMomentFX.lua:324`–`:331` replaces the old tracker only after
  working state, pump animation/speed and Hit markers qualify (`:202`–`:213`).
  The new handle runs the same vanilla FX consumer; live scheduling/cure was
  not remeasured here.
- **SOURCE — Shuttle at a Shuttle Hub:** current `Lua/Buildings/ShuttleHub.lua:461`
  identifies Shuttle's entity. The classic cargo-shuttle hub skins select
  landing/takeOff and landing2/takeOff2 at `:1582`–`:1590`, then start
  `TrackAllMoments` with Shuttle actor and hub target at `:1632` / `:1649`.
  Current `ActionFXSound.lua:13480` / `:13519` match enter/exit Hit, and
  `ActionFXParticles.lua:8404` / `:8421` match exit Hit. The four added preset
  cases supply those readers. JumperShuttle has its own selection at
  `ShuttleHub.lua:1593`–`:1604`; the patch adds no JumperShuttle preset.
- **SOURCE — RC Driller:** current `Lua/Units/RCDriller.lua:6` uses
  RoverRussiaDriller; `:102` sets workIdle before `:105` starts its Drill tracker.
  Current `ActionFXSound.lua:5568` and `ActionFXParticles.lua:6999` match
  Drill / RCDriller / Hit. The added two workIdle Hit markers therefore still
  feed the drilling sound/steam consumer at each job start.
- **SOURCE — RC Dozer:** current `Lua/Units/RCTerraformer.lua:6` identifies
  RoverTerraformer, `:9` identifies the displayed RC Dozer name, and `:35`
  opts workIdle into tracking. `:101` passes workIdle through RCConstructorBase;
  `Lua/Units/RCConstructorBase.lua:2` inherits RCTransport. Current
  `Lua/Units/RCTransport.lua:132`–`:134` sets that state and starts the task's
  FX tracker. The added markers are **Hit1**, matching the shovel sound at
  `ActionFXSound.lua:7031` and Load particles at `ActionFXParticles.lua:7119`.
  The sound claim is for that Load/task path; unrelated Construct-only paths
  are not represented as newly cured.
- **SOURCE — The Excavator:** current `Lua/Buildings/TheExcavator.lua:47` selects
  ExcavatorShovel as the arm, `:58` sets working, and `:117` restores speed
  before `:120` starts `TrackAllMoments(arm, "ExcavatorDigging", arm)`.
  The current particle preset has all twelve matching Hit names at
  `ActionFXParticles.lua:115`–`:325` and all twelve Out names at `:343`–`:530`.
  The module supplies all 24 names in its sorted working preset. This is bucket
  dig/throw dust; Excavator's unrelated continuous sounds are not the repair.
- **SOURCE — old-save sibling paths:** `Code/Fix_SilentHitMomentFX.lua:263`–`:280`
  replaces eligible working hammer, MOXIE, Water and already-animating Excavator
  trackers. Multiple-hit startup still deletes its old tracker at
  `BaseBuilding.lua:1042` / `:1032`–`:1033`; Water/Excavator helpers delete their
  own handles before assigning vanilla `TrackAllMoments` (`Code:208`–`:213`,
  `:250`–`:254`). Vehicle readers restart on the current flight/job/task paths
  above. Current `CommonLua/Savegame.lua:808` posts LoadGame before PostLoadGame
  at `:811`. EF-028/EF-029 supply the inherited lifecycle/deferral facts; no new
  serialization or in-play safety measurement was performed.
- **SOURCE — public scope:** site `C:/Dev/SMR-CommunityMods/content/fix-list.md:288`–`:308`
  names all seven, describes missing marks plus the two lookup/order defects,
  and qualifies classic hammer/MOXIE skins and old-save versus vehicle restart.
  `metadata.lua:3`'s `SEVEN MACHINES THAT WORKED IN SILENCE` paragraph names the
  same seven and qualifies the two alternative skins. The count is consistent
  with the seven actual consumer paths above.

## Not checked, by name

- New live sound/particle output, animation timing or synchronization, doubled FX,
  visual/audio quality, or screenshots for any of the seven units or skins.
- Fresh old-save load healing, persisted-handle behavior, power-cycle-free cure,
  or one-tracker-only state in a running colony; earlier attended receipts inherited.
- Current uninstall, enable/disable, save round trip or persisted-frame safety.
- Foreign preset overrides, mod-defined entity/animation mappings, or double FX
  from a future independent code-driven game repair.
- Fresh 1.0.7 runtime or an exhaustive cross-version rerun; current primary trace
  is 1.1.0.403908 and earlier dual-tree derivation is inherited.
- Every unrelated animation-moment consumer, Metatron, JumperShuttle effects,
  unsupported alternative skins, or non-Load RC Dozer construction tasks.
