# CrystalMysteryHang - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

- Public after-fix promise covers any late answer, but module repeater stops after ten sols; narrow guarantee to actual repeated-message window

- F103 duplicate restored-thread lineage remains known/unrepaired, not reopened or promoted by this sweep

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_CrystalMysteryHang.lua | F06, F103 | yes: direct final registry line 239 active | yes: scenario waits for CrystalFlyAway after player popup before MysteryEnd | partial: original race remains; cure is bounded ten sols and cannot guarantee every arbitrarily late popup answer | partial: headline symptom supported; registered never-hang title omits ten-sol bound | KEEP-BUT-FIX-CLAIM | 1.1.0.403908 Lua/Mysteries/Crystals.lua:67; 1.1.0.403908 Lua/Mysteries/Crystals.lua:69; 1.1.0.403908 Lua/Mysteries/Crystals.lua:70; 1.1.0.403908 Lua/Scenario/Mystery 10.generated.lua:243; 1.1.0.403908 Lua/Scenario/Mystery 10.generated.lua:271; 1.1.0.403908 Lua/Scenario/Mystery 10.generated.lua:277 | SOURCE | Current organic PhilosopherStone finale and late-popup race; Live late answer beyond ten-sol window, repeated-message cure and historical probe; F103 restored-thread duplication, orphan/uninstall gate or current save/load; Menu enable/reload,1.0.7 runtime and other mystery completion routes |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- ComposeProc :67 announces completion then :69 waits one sol for CrystalForceFlyAway and :70 emits one CrystalFlyAway. Whole pinned tree search finds no CrystalForceFlyAway emitter. The current scenario blocks at popup :243 before its :271 WaitMsg, then :277 MysteryEnd. The race and exact message consumer both remain; no current replacement stores an already-departed state.

- The module additive departure handler starts hourly rebroadcasts; LoadGame sibling restarts for an active mystery with absent crystal. The actual repaired output is still consumed by that wait, and no new scenario consumer was found. Existing EF023 by-value restored-thread/F103 duplicate lineage remains a disclosed save limit; no harness or duplicate live measurement was run here.

- Code/Fix_CrystalMysteryHang.lua:74 gives deadline GameTime()+10*DayDuration. Each lineage stops on deadline, mystery end/change, or orphan gate. A stable playthrough answering after rebroadcasts expire can still miss the one-shot; that route/cure outcome is INFERRED from explicit bound, unmeasured. Source conclusively disproves an unlimited rebroadcast guarantee.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:507 says mystery finishes whether popup answered promptly or not, without the ten-sol bound. Metadata symptom headline is supported, but registered title can no longer hang forever is too absolute. Recommend conditional ten-sol wording; no thread/code rebuild in this task. Owner may separately commission a state-based repair; that is an idea, not a new verified defect.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:239` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current organic PhilosopherStone finale and late-popup race
- Live late answer beyond ten-sol window, repeated-message cure and historical probe
- F103 restored-thread duplication, orphan/uninstall gate or current save/load
- Menu enable/reload,1.0.7 runtime and other mystery completion routes
