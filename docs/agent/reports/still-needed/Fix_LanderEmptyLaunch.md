# LanderEmptyLaunch - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

- Current vanilla minimum one-hour automode delay applies in IsCargoReady on both sides; header/oldentry only-asteroid brake prose is stale, without changing retained defect

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_LanderEmptyLaunch.lua | F67 | yes: direct final registry line 227 active | yes: CmdLoad and flight policy call IsCargoReady before loading end/departure | yes: empty request still ready inside noninstant normal auto wait window after one-hour minimum | yes: automatic empty-launch symptom maps to retained row | KEEP | 1.1.0.403908 Lua/UniversalRocket.lua:500; 1.1.0.403908 Lua/UniversalRocket.lua:554; 1.1.0.403908 Lua/UniversalRocket.lua:558; 1.1.0.403908 Lua/UniversalRocket.lua:2106; 1.1.0.403908 Lua/UniversalRocket.lua:2110; 1.1.0.403908 Lua/CargoTransporterNew.lua:1305 | SOURCE | Organic current auto-lander empty request and live gate/timer dwell on both sides; Current cargo/passenger and instant/special-mode controls, actual fuel waste; Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- CmdLoad :500 and :509 still consume IsCargoReady and wait before OnCmdLoadEnd :514. GetCargoResourcesStatus :1305 returns ready for equal/empty requests. After the minimum-hour delay at IsCargoReady :554, :558 still accepts the empty automatic flight during CheckAutoDepart wait window. No caller replacement removes this use.

- CheckAutoDepart :2106 permits forced departure after the configured timer for player rockets; :2110 permits departure for an empty current-side threshold set. The wrapper preserves those designed exits and instant/special/nonplayer branches; it refuses only an empty nonfuel flight inside an actual remaining wait window.

- Current :554 implements a minimum one-hour automode wait in shared IsCargoReady. The old header/entry only-asteroid sleep/noMars-brake explanation is obsolete. This does not cure premature departure before the larger cargo wait expires, and the player-facing row does not claim that exact initial-hour cadence.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:427 and metadata headline describe automatic rocket/lander empty launches. They remain supported with the current wait-window scope. Historical PT16 full-sol dwell/forced exit and current-side rule-set caveats are preserved with their original dates.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:227` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Organic current auto-lander empty request and live gate/timer dwell on both sides
- Current cargo/passenger and instant/special-mode controls, actual fuel waste
- Current behavior firing, menu enable/reload, save/load/uninstall,1.0.7 runtime
