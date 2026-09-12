# Native F46 premise control - parked before firing

Coordinator `/root`, 2026-09-12. Agent `/root/module_b` traced the native request
selection and flag-only control independently. No false-owner native factory:
its safety at the menu is unestablished. Use a copied recent manual colony instead.

Source **1.1.0.403908**: `Lua/Buildings/Station.lua:1046-1048` delegates disabled
acceptance to `Lua/Buildings/MultiResourceDepot.lua:264-273`, adding rfSuspended
without changing demand amount. `Lua/Units/Train.lua:794-796` consumes its native
GetTargetAmount. `Lua/Buildings/LanderRocket.lua:1279-1280` uses SetFlags to restore
requests. EF-091 prohibits inferring a native target from actual amount alone.

Payload [97_StillNeededF46.lua.txt](97_StillNeededF46.lua.txt) waits for menu, loads
a byte copy of manual `USA Sol 47.savegame.sav` (2026-09-11), leaves it paused,
and seeks a real Station with an enabled positive native demand. No fixture or
load rejection logs that result and quits; no branch override or new object.
Baseline -> add rfSuspended -> clear it -> independent exact SetFlags restoration.
Read flags, enabled, actual, target. No resize, reconnection, actual unload, route
execution, save writing, game-speed change, account or portal action.

Before launch: confirm Mars absent and both Code marker sweeps clean; byte-copy
**every save** to an external backup and record names/hash/mtime (EF-056 includes
header-tagged autosaves with ordinary names). Stage the designated manual copy,
backup TestKit metadata byte-for-byte, arm via the existing file-backed harness,
read back/parse/declaration gates. Only the named F46 payload is declared.

After process exit: archive the complete log, disarm, restore metadata byte-exact,
delete the designated copy, reconcile every original save by hash and restore any
rotated originals from the external backup. Report any additional autosave by name.
No original manual save is overwritten; external recovery backup stays available.

A positive suspended native target establishes this premise on the sampled request.
A zero target closes this sampled flag-only path, requiring retirement review.
Neither result witnesses actual dumping, routing exceptions, or the fix's cure.
Execution result belongs in RUNTIME and F46's verbatim agent report.
