# SinkholeIndestructible - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_SinkholeIndestructible.lua | F96 | yes: direct final registry line 265 active | yes: large meteor calls DestroyBuildingImmediate and instance/class indestructible blocks deletion | yes: row describes set-piece destruction without asserting unproved softlock | n/a: no dedicated metadata headline | KEEP | 1.1.0.403908 Lua/BuildingTemplate/Sinkhole.generated.lua:10; 1.1.0.403908 Lua/Buildings/Building.lua:237; 1.1.0.403908 Lua/Buildings/Building.lua:1445; 1.1.0.403908 Lua/Meteors.lua:964 | SOURCE | Current organic StElmo mystery plus large meteor on sinkhole hex; Current instance own-field overrides and forced destruction control; Reward-branch dead-object behavior or mystery softlock, full current flag-consumer inventory; Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current Sinkhole generated class still omits indestructible and disasters_strike_immunity and sets can_demolish/use_demolished_state false at :10/:11. Building default indestructible remains false at :237. The current bodycheck span confirms omission persists, and shared runtime measures installation after presets/classes resolve.

- Large meteor building branch :960-964 still passes this set-piece to DestroyBuildingImmediate; :1445 reads the instance flag before deletion. The two module writes cover class/default and template proxy; the former is load-bearing for inherited instance value. The protection therefore retains its ordinary destruction consumer.

- Other building guards already have false predicates on this template: can_demolish :914 and UseDemolishedState :1545. The patch does not promise a mystery softlock cure: the historical unguarded reward object use remains located/unproved, with engine dead-object semantics unmeasured.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:541 names meteor destruction of the sinkhole. No dedicated metadata headline. Existing historical forced PT60 class/instance control is kept with its date; no current spawned-object test is claimed.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:265` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Current organic StElmo mystery plus large meteor on sinkhole hex
- Current instance own-field overrides and forced destruction control
- Reward-branch dead-object behavior or mystery softlock, full current flag-consumer inventory
- Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime
