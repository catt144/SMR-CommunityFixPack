# F46 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Game **1.1.0.403908**;
captured inputs and final direct registry in `CENSUS.json`. Recommendation:
**KEEP**. Installation and current Lua consumer paths are established. A later
coordinator-owned native control on the copied USA Sol-47 colony establishes
the positive suspended-cap premise on a real current Station demand. Basis is
**SOURCE**, supplemented by that **MEASURED** native value; actual unloading and
route recovery remain untested outcomes.

Disagreements first: the 2026-09-09 F46 entry's unestablished native premise is
now superseded for the measured real request. Adding `rfSuspended` disabled
Concrete while both actual and target amounts stayed 2500. The alternate
explanation that suspension already forces every native target to zero is
therefore false. Missing `IsResourceEnabled` in `UnloadAll` alone was insufficient
evidence; the current source plus this native control establishes its defective
positive-cap path. The row's guard and two disclosed exceptions agree with the
implementation. Its production ping-pong symptom and route cure were not
witnessed by this control, which changed only a request flag. The recopy retains
current nil guards and BlackCube accounting; the boot probe's missing-demand
case is separate from the later real-native measurement.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrainCargoDumping.lua | F46; F114 recopy/branch gate context | yes: final direct registry active at line 241; current depot-base gate and missing-demand probe accepted installation | yes: both TransferCargo unload calls still reach the replacement; station/demand and current route flags feed its guard; both loading siblings and BlackCube consumer remain | yes: source guard and disclosed exceptions match; a real disabled native demand retained target 2500, establishing the current positive-cap premise; actual unload and route cure remain unwitnessed | n/a: no dedicated F46 card headline or specific intro example | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Train.lua:795; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Train.lua:846; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Train.lua:992; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/MultiResourceDepot.lua:271; C:/Dev/SMR-BugFixPack/docs/archive/logs/stillneeded_f46_Mars.exe-20260912-01.00.26-6a91a190.log:224 | SOURCE; native cap MEASURED | actual current unload and route exceptions; F114 train departure cure; native constructor execution; fresh 1.0.7 decline; production save/load/uninstall; full cure probe |

Primary evidence (read-only **1.1.0.403908/Src**):

- **Current unload and both callers:**
  `Lua/Units/Train.lua:779-805` cancels inbound assignments with a nil guard at
  `:785-787`, reads the demand conditionally at `:794-795`, computes
  `Min(carried, station_cap)` at `:796`, and moves cargo at `:798-799`.
  It contains no resource-enabled test. `TransferCargo` calls this function
  directly at `:846` and again through a destructor at `:990-992` while reserving
  departure may require waiting. The replacement preserves these paths and the
  BlackCube hook at `:800-801`, adding its resource/route/stopping decision before
  movement. The later real-native control establishes a disabled positive cap
  of 2500, so this source path can move carried cargo despite the station switch.
- **Current station switch changes the native flag, not the demand amount:**
  Station inherits MultiResourceDepotBase at `Lua/Buildings/Station.lua:51`.
  Its disabled state at `:1046-1048` toggles `SetAcceptResource`.
  `Lua/Buildings/MultiResourceDepot.lua:242-247` implements
  `IsResourceEnabled = IsStoring` by testing the demand's `rfSuspended` flag.
  The off branch at `:264-273` interrupts/disconnects as needed, adds
  `rfSuspended` to demand, and makes supply non-depot/exportable. It does not
  remove demand, set its amount or zero it in Lua. Re-enable clears the demand
  flag at `:279`. `skip_reconnect=true` exits at `:285`, but the function still
  obtains the object's map LR manager at `:258`; a plain menu stub cannot be
  assumed to support that method safely.
- **Both loading siblings remain enabled-aware:**
  `Lua/Units/Train.lua:869-873` separates enabled storage from forbidden supply.
  Balance loading calculates an enabled destination target at `:920` before
  checking its demand cap at `:924`; forbidden-excess loading explicitly checks
  `dest:IsResourceEnabled(res)` at `:935` before its demand read at `:936`.
  Disabled stock is still considered for export at `:897` and `:910-912`.
  Existing stock can become forbidden when a player disables a previously filled
  station, so these siblings alone did not prove a positive disabled unload cap.
  The later native measurement supplies that premise independently; the actual
  repeating cycle was not replayed.
- **Current route input and disclosed escape hatches:**
  `Lua/Units/Train.lua:837-840` reads the route from
  `city.train_track_routes[track]`; `Lua/TrainTransport.lua:371-372` uses the same
  station route table for iteration. The module scans its current track's route
  directly and checks each other station's demand plus current enabled method,
  rather than using old `task_requests` membership. It only suppresses a
  positive unload while another station accepts the resource and the train is
  not stopping. The no-other-destination and refab exceptions are retained.
  Current `Train:DestroySilent` still calls demolition at
  `Lua/Units/Train.lua:164-166`; the exception's actual cargo outcome was not
  replayed here.
- **Native request factory and owner contract:**
  `CommonLua/TaskRequest.lua:111-113` adds `rfDemand`; `:125-138` calls the
  factory, records the request and posts it to connected centers.
  `Lua/_TaskRequest.lua:25` binds `Request_New = MarsRequest_New`, and the
  actual game factory at `:156-157` passes a real owner plus resource, amount,
  flags, max units default -1, desired amount default 0 and supply distance
  modifier. Current station resource registration creates native supply/demand
  through that path at `Lua/Buildings/MultiResourceCubeVisuals.lua:381-391`,
  including the reciprocal supply link. The native methods are exported as
  permanents at `CommonLua/TaskRequest.lua:36-46`; they are not Lua methods that
  this review may monkeypatch to establish their behavior.
- **No supported absent-owner constructor control was found:** a full source
  search finds no `Request_New(false/nil, ...)` or
  `MarsRequest_New(false/nil, ...)` call. The shipped native request test requires
  a loaded map at `Lua/Dev/GameTests.lua:476-479`, places legitimate CargoShuttle
  owners on it with auto-connect disabled at `:486-492`, and uses those owners
  for `MarsRequest_New` at `:514`, `:517`, `:519`. This provides a safe loaded-map
  precedent, not a supported menu-only factory. `pcall` cannot make an unproved
  absent-owner native argument safe from an engine failure.

The site row `C:/Dev/SMR-CommunityMods/content/fix-list.md:356-367` describes the
historical symptom, current guard and two deliberate exceptions accurately.
The required positive suspended-cap premise is now measured on 1.1.0, supporting
**KEEP**. This is source-established behavior with a measured native link, not
a witnessed production unload or proof of every route configuration.
No dedicated F46 card headline or intro example was found; broad train/cargo
coverage and the whole-card repair count are the coordinator's scope.

The 2026-09-09 F46 entry authorized recopy on top of the branch gate, retained
both exceptions, and left the native-cap control owed. That specific premise
gate is now satisfied by the archived 2026-09-12 control below; the old
`tested` status still belongs to 1.0.7 PT-23 and is not a new unloading witness.
The earlier desk control supplied a positive-cap stub, so it verified conditional
Lua behavior but not native semantics. The coordinator owns the entry update.
This review does not reopen the rejected metatable patch or persisted-property
conversion.

Direct final registry
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:241`
reports active; the settled second boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:96`.
Those menu installation launches loaded no colony or suite. The later bounded
native control loaded a copied colony; it did not run the cure suite or invoke
actual unloading.

Coordinator-owned native control, executed after the initial parked plan:

The complete archived log is
`docs/archive/logs/stillneeded_f46_Mars.exe-20260912-01.00.26-6a91a190.log`,
SHA-256 `a24941a12a7ae1269a62a65587c6fd829405f5be983dc6b69635b3feac4260db`
(verified directly by this reviewer). `:177` records the copied USA Sol-47
load and no speed change/save; `:180-181` records revision 403908; `:212` and
`:217` confirm the loaded colony/map.

- **BASELINE `:223`:** real Station Concrete demand, native userdata; full flags
  1548, `rfSuspended=65536`, suspended false, enabled true, actual 2500, target
  2500.
- **SUSPENDED `:224`:** full flags 67084, suspended true, enabled false; actual
  and target both remain 2500. This is the demand-flag change performed by the
  current station-off source path, without an amount resize or cargo transfer.
- **CLEARED `:225` and RESTORED `:226`:** flags return to exactly 1548, enabled
  true, actual 2500, target 2500. **CONTROL `:227`** reports `ok=true`,
  `restore=true`, and nil errors. `:231` and `:236` record graceful exit.

The coordinator reports no new objects, no actual unload, no additional
autosaves, all 121 original saves hash-verified unchanged, staged copy deleted,
and TestKit metadata restored byte-for-byte. These file-reconciliation checks
are coordinator-reported operational evidence, not facts printed in the native
control log. This reviewer only read the archived output and wrote this pair.

The original bounded recipe is preserved for reproduction; it was a native
link control, not a production dumping witness:

- Use a byte copy of a current manual colony save with all save files backed up
  and reconciled by the coordinator, or a throwaway new colony. Pause before
  the control, advance no game time, save nothing and quit afterwards.
  The executed USA Sol-47 copy did contain a suitable Station; USA Sol-35 was
  not needed or assessed by this control.
- Enumerate actual current-map Stations. Prefer Concrete demand, then Metals
  or WasteRock. Require a valid owner, native userdata, an enabled resource,
  no `rfSuspended`, and positive `GetTargetAmount`; otherwise log **NO_FIXTURE**
  and quit. Do not synthesize a false owner or provision an unproved menu object.
- Capture `req:GetFlags()`, target and actual amount before mutation. Add exactly
  `const.rfSuspended`, read flags/disabled state/actual/target, clear that same
  bit and read again. This is the exact demand-flag change that the station
  off branch performs. Do not resize the existing request or assign a train.
  EF-091's negative-target observation warns that resizing while claims exist
  can confound amount reads; a naturally positive baseline avoids that setup.
- Restore the complete saved flags with `req:SetFlags(saved_flags)` in a
  separate protected cleanup even if the experiment fails. This native API is
  used by shipped code at `Lua/Buildings/LanderRocket.lua:1279-1280`.
  Verify exact flags and target match baseline. On failed restoration, remain
  paused and quit without saving. Log numeric `rfSuspended` and all full flag
  values rather than inventing an undocumented flag-bit number.
- An optional private constructor control requires that same legitimate owner
  on a loaded map. The exact factory is
  `owner:CreateRequest("Concrete", 5000, bor(const.rfDemand,
  const.rfStorageDepot, const.rfSpecialSupplyPairing), -1, 0)`.
  The 5000 is internal amount (five resource units on the current 1000 scale).
  Calling `CreateRequest`, not `AddRequest`, avoids posting it to task lists or
  hubs. Require an initial positive target before interpreting its flag test.
  This private unpaired request is secondary evidence: actual station demand
  carries its normal reciprocal and desired-state context and is preferred.
  Set its source false when discarding, consistent with
  `CommonLua/TaskRequest.lua:146`, and exit without saving.
- The measured restored positive-cap baseline and still-positive suspended
  target establish the F46 native premise for this instance. This does not test
  actual unloading, route exceptions, delayed transfers, ping-pong rate or the
  F114 departure cure. One real request is a named instance, not proof of every
  request configuration. The optional private constructor was not executed.

What I did NOT check, by name:

- Native constructor execution or other resource/request configurations.
- Actual 1.1.0 unloading, accepting-elsewhere, nowhere-accepts and refab outcomes.
- Current F114 train departure and BlackCube accounting in play.
- Absent-owner native constructor safety or fresh-colony Station provisioning.
- Independent remeasurement or save-backup/reconciliation checks by this reviewer.
- Full TrainCargoDumping cure probe, native metatable patch or `RunAll()`.
- Production save/load/uninstall, fresh 1.0.7 decline, other modules and aggregate claims.
