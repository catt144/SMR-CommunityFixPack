# BombardmentSpread - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_BombardmentSpread.lua | F26 | yes: direct final registry line 262 active | yes: mystery starts volley; missile position/axis/travel use corrected spawn position | yes: vanilla still discards per-missile elevation direction | n/a: no dedicated metadata headline | KEEP | 1.1.0.403908 Lua/Bombardment.lua:82; 1.1.0.403908 Lua/Bombardment.lua:83; 1.1.0.403908 Lua/Bombardment.lua:85; 1.1.0.403908 Lua/Bombardment.lua:93; 1.1.0.403908 Lua/Bombardment.lua:158; 1.1.0.403908 Lua/Scenario/Mystery 7.generated.lua:949 | SOURCE | Organic 1.1.0 Mystery7 volley, visible spread and no-mod A/B; Current decal fade, notification clearing, interception, dome cracks, volley finish; Current random-draw parity and TestKit firing, menu-enable/reload, save/load/uninstall,1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- WaitBombard computes spawn_dir at :82 but uses base dir at :83. The missile is placed with this position at :84/:85; its subsequent direction and axis use it at :93-96. The correction still changes actual flight data read by vanilla; no updated consumer supersedes it.

- StartBombard resolves WaitBombard at call time (:158). Mystery7 generated :949 remains an ordinary caller, beyond console forcing. The replacement retains the shipped body except the documented spawn_dir correction and dropped non-unwinding assert. Current manifest matches; hotfix2 cleared copying and this review does not re-audit every unchanged effect.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:33 accurately describes identical directions and use of each computed angle. This is elevation jitter; organic current-game timing/spread and integrity remain unmeasured. Historical PT47 sampled five forced volleys on1.0.7 with decal/notification limits and defective readers; those remain dated evidence.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:262` measures active. Bodycheck passes; installation is not cure verification.

Not checked:

- Organic 1.1.0 Mystery7 volley, visible spread and no-mod A/B
- Current decal fade, notification clearing, interception, dome cracks, volley finish
- Current random-draw parity and TestKit firing, menu-enable/reload, save/load/uninstall,1.0.7 runtime
