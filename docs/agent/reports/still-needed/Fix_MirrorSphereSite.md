# MirrorSphereSite - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_MirrorSphereSite.lua | F16 | yes: direct final registry line 245 active | yes: infopanel actions call StartAction and the PierceTheShell branch creates drone work | yes: finished raw progress still bypasses vanilla percentage comparison | n/a: no dedicated metadata headline | KEEP | 1.1.0.403908 Lua/Mysteries/MirrorSphere.lua:16; 1.1.0.403908 Lua/Mysteries/MirrorSphere.lua:70; 1.1.0.403908 Lua/Mysteries/MirrorSphere.lua:747; 1.1.0.403908 Lua/Mysteries/MirrorSphere.lua:836; 1.1.0.403908 Lua/Mysteries/MirrorSphere.lua:844; 1.1.0.403908 Lua/Mysteries/MirrorSphereInfopanel.lua:15 | SOURCE | Current mystery-to-completion route and unfinished-site controls; Live finished-site drone requests/action cancellation and infopanel rendering; Current behavior firing, menu enable/reload, save/load/uninstall, 1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- The file-local finished value remains 2^22 (:16), published on MirrorSphere (:70). SetProgress clamps to it (:747), stops the current action and launches the sphere at that value (:764 onward). BuildingUpdate :780 stops progressing a completed site.

- IsActionEnabled :786 checks running/completed individual actions and proximity, without a global finished-site gate. StartAction :836 still compares raw progress to 100. Its PierceTheShell arm :844 resets a work request and :845 connects command centers. The corrected comparison is therefore still consumed.

- MirrorSphereInfopanel.lua :15, :18 and :21 call StartAction for the three actual actions. The wrapper blocks new work at finished progress and preserves the running-action cancellation branch :827.

- C:/Dev/SMR-CommunityMods/content/fix-list.md:551 describes actions offered/accepted after completion. The module does not hide buttons; the row specifically promises a finished site stops accepting work. No correction found.

Direct registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:245` measures active. `BODYCHECK.txt` matches the target body and defect expression. Installation is not a cure observation.

Not checked:

- Current mystery-to-completion route and unfinished-site controls
- Live finished-site drone requests/action cancellation and infopanel rendering
- Current behavior firing, menu enable/reload, save/load/uninstall, 1.0.7 runtime
