# Game 1.1.1 build response — 2026-09-23

## Must_Read_Header

Reader: the owner and the separate audit seat reviewing the resulting diff against
archived game source. SOURCE means archived build 1.1.1.405907 unless stated;
desk-MEASURED means the named Lua harness, never a retail or played result.
The code response is complete at the desk. Separate owner audit and retail
checks remain open at ck209/ck210. This is not release approval.

## Work list

The session has no todo tool. This list and the coordinator's tool-state list carry
the brief's work units instead. Reconciliation and the result commit stayed with
the coordinator; independent module writers did not edit shared files or commit.

- [x] 1. Orient; compare the brief's baseline and confirm evidence inputs.
- [x] 2. Track: F124 rebase, BrokenTrackSalvage retirement, refund wrapper read.
- [x] 3. F125: direct and multi-leg migration repair and controls.
- [x] 4. F121: load-only legacy repair and falsifiable controls.
- [x] 5. Retirement traces and F122/F123/F126 two-sided controls.
- [x] 6. Manifest hygiene: BombardmentSpread, ExtenderFlapChurn, DryFarmingFarms.
- [x] 7. Shared-file reconciliation by name and generated counts.
- [x] 8. Independent internal review of the behaviour claims.
- [x] 9. Harnesses, selftests, doccheck, entries and owner play legs.
- [x] 10. Exact-path result commits; consume the brief and its map row; push.

## Baseline and limits

Started at `16ff1aae4c55a3c466496e49089824a6dafe7437`; `git pull` reported
already up to date and `git status --short` was empty. `git diff --stat
234a121..HEAD` shows only brief/map changes: the audit, adjudication, ranking,
filings and settled gates did not move. The live Steam manifest reports build
`25390750` (`rg -n 'buildid' A:/SteamLibrary/steamapps/appmanifest_3215050.acf`).
No game launch, save inspection, shipped-source edit, release or version change
is part of this work.

`python tools/gamepatch_111_census.py --live-source` also decoded the installed
build as `1.1.1.405907` and matched both live and archived source against
`MANIFEST.sha256`, digest
`d753f949af92e2b753f44163a2e47229e371f810ef3c2752d30a98953af2663c`.

## Challenges and departures

- F121 needs a saved-provenance condition as well as the exact reason and event
  interlocks. SOURCE: `Lua/ClassDefs/ClassDef-Effects.generated.lua:2772-2790`
  starts an anonymous Duration thread without storing its handle on the building;
  `Data/StoryBit/BuildingClogged.lua:6-8` disables its on-screen timer. The same
  saved fields can therefore describe a healthy 1.1.1 disable after the story
  finishes. `CommonLua/Savegame.lua:798-812` supplies the save metadata to
  `LoadGame`. The load-only repair accepts only pre-1.1.1 provenance.
  Already-resaved ambiguous state stays untouched. Independent review confirmed
  the provenance condition: `CommonLua/Savegame.lua:775` rewrites the saved
  revision, so an ordinary save of a healthy 1.1.1 timer cannot carry the older
  provenance. No save file was inspected.

- F125 uses input wrappers rather than a new migration-body copy. The dated F52
  1.1.0 note rejected a distance pre-wrapper because a general distance change
  could alter several predicates. The new bounded argument crosses only the
  passage lookup threshold and is checked against runtime constants. That
  evidence revises the old design conclusion; the owner's ck123 repair ruling
  is unchanged.
- F126's deciding consumer includes an assertion before the unknown-id fallback.
  The initial collector test bypassed it. Internal review required the archived
  `AddNotification` and `PropertyObject:CreateInstance` bodies; the corrected
  control now measures both under the explicit EF008 assert model.

## Results

### Track — F124, F44/F91/F116 and F45 retirement

SOURCE: the complete replacement is rebased on
`Lua/Buildings/TrackElement.lua:467-637`. It keeps the vendor's repair-site
exclusion, array-specific removal, rehome/`repair_cgs` rebuild and native
`ProcessAllElements` calls. Marked deltas retain curved/short salvage and shell
cleanup. `Fix_BrokenTrackSalvage` is deleted in this same response; its old stamp
is no longer needed when repair sites never enter physical ordering.

SOURCE: `Fix_TrackSalvageRefund` remains unchanged. Physical survivors still
live in `track.elements`; a repair-site click delegates to its broken element.
The snapshot therefore reaches the demolished physical elements, and the
`track.demolishing` guard prevents double refunds on whole-track removal.

desk-MEASURED: `python tools/desk_f124_track.py` covers curved and short
segments, repair ownership and `repair_cgs`, arrays, refunds, shell cleanup,
skip forwarding, old-pack reproduction and scratch guard reversals. Geometry,
validity and object lifetime are stubbed; native destruction/graph bodies are
extracted. Terrain rendering, station-created threads and saved-game round trips
remain unmeasured.

The branch guard uses the newly declared `Colonist.MigrateStep` shape because a
full split/processing probe would enter engine map and grid operations on fake
objects. Missing shape declines. This identifies the archived branch; it does
not validate future repair semantics. No replacement-owned thread, yielded
continuation, field or persisted function was added. Native connector threads
remain native; healed arrays are ordinary game state after removal.

### Legacy clogged buildings — F121 / C85

The daily repair and positive-Duration stand-down are removed. The synchronous
load handler requires positive numeric saved `lua_revision < 405907`, then the
exact reason `789863173059` and the original running-story, armed-follow-up and
queued-popup interlocks. Unknown provenance declines. The shipped setter still
earns its behaviour probe and preserves coexisting maintenance state.

desk-MEASURED: `python tools/desk_c85_clogged.py` exercises the current archived
setter, the anonymous native Duration effect using a coroutine, the pre-fix
module extracted from `16ff1aa`, idempotence, save provenance, vetoes, interlocks,
and the actual TestKit predicate probe with a live unrelated popup. The native
timer survives the simulated current-save load and releases the building itself.
`python tools/desk_c85_clogged.py --selftest` runs the complete suite against
scratch reversals of each decisive guard/cure and requires failures; production
bytes are checked unchanged. This does not exercise engine thread serialization
or localization userdata.

Save footprint/removal residue: no new thread, GameVar, persisted function or
object field. The existing vanilla disable/reason fields are healed once. No
retail upgrade or uninstall round trip was run.

### Manifest hygiene

Comment-only changes: `Fix_BombardmentSpread` now pins current `WaitBombard`
(`Lua/Bombardment.lua:52-150`) and matches direction reuse before/inside the loop;
the vendor deleted unused jitter but did not add spread. The existing extra
random draws remain unchanged. `Fix_ExtenderFlapChurn` adds the missing
`DroneHubExtenderBase:UpdateUplinkRequesters` pin (`:109-112`).
`Fix_DryFarmingFarms`'s regex no longer treats the added `FarmSmall` effect as
complete repair; it watches the still-missing `FarmSmallUnderground`,
`FarmUnderground` and `AutomatedFarm` labels. Any later partial repair still needs
a read. No save-exposed implementation changed in these modules.

### Vacuum migration — F125 / F52

The direct wrapper delegates every call to native `TryToEmigrateToDome`. For a
positive short vacuum walk it first checks `AreDomesConnectedWithPassage`, the
same read-only gate used by native `GetDomesPassagePath` (SOURCE:
`Lua/Passage.lua:1267-1274,1300-1303`). When runtime
`MaxDomeWalkDist + 1 < MinDistToIgnorePassage`, passing `MaxDomeWalkDist + 1`
crosses the lookup threshold while staying positive and below the later detour
choice. No-passage and unsafe-bound calls retain their input. Native ordering,
reservations, elevator logic, shuttle booking, migration destination and returns
are preserved (`Lua/Units/Colonist.lua:1894-1982`).

The blocking `MigrateStep` body stays native (`:2155-2221`). Its synchronous
`GetNextMigrationLeg` helper (`:3709-3717`) arms a weak marker only for a
nonfinal walk on the colonist's actual MigrateStep command thread. The immediately
following `IsInWalkingDistDome` consumes it before calling native and adjusts only
the distance used for passage lookup. The colonist, command/thread, both domes
and city must match. Unexpected callers and cancellation decline. Return arity
is preserved. Checked global installation precedes class-method installation;
failure leaves both native methods untouched.

desk-MEASURED: `python tools/desk_f125_vacuum.py` executes archived native direct
and intermediate bodies, old-pack reproduction from `16ff1aa`, breathable and
no-passage controls, threshold bounds, reservations, elevator/shuttle/train
continuation, cancellation, unrelated callers, failed installation and scratch
reversals. It also runs the actual TestKit VacuumWalks probe. The existing
`desk_migration_cluster.py` fixture was updated to supply native shuttle helpers
now reached by the preserved body. Require is deliberately bypassed in that
older cluster; the focused harness separately exercises actual Require.
Final fixture review restored passage connectivity before its breathable control
and counted calls through the native connection predicate. The cluster's
`--selftest` removes the atmosphere guard in a scratch module and requires that
specific control to fail, with production bytes unchanged.

Save/removal disposition: synchronous wrappers, no new game-object field,
persisted function, mod thread or yielded continuation. The consumed weak marker
is process-local and inaccessible after removal. Engine pathfinding, command
serialization and actual colonist survival remain owner-only measurements.

### Retirements

Every row is SOURCE on archived 1.1.1.405907 plus the explicitly named desk
controls in `python tools/desk_gamepatch_retirements.py`. F45's behavior is in
the track harness. Historical test files now read the deleted module from
`16ff1aa` and its intended archived source; they remain evidence about that
historical implementation, not the current native replacement.

| Removed module | Entry | Native replacement and consumer |
|---|---|---|
| BrokenTrackSalvage | F45 | `TrackElement.lua:467-637` and `Track.lua:466-474`: repair sites excluded from physical ordering, rehomed separately; F124 now preserves this. |
| FounderTraitNotification | F23 / F126 | The feature handler and preset were removed. `Notifications.lua:25-48` receives no unknown Founder id after deletion. Actual old handler reaches the unknown-id assertion and base fallback through
the archived constructor; native-only control does not. UI rendering remains unobserved. |
| BuildingCodesPrefab | C88 | `LawDef-Efficiency.lua:700-708,902-910`: both completion handlers apply the law-id modifier without skipping prefabs. |
| DestroyedTunnels | F38 | `Tunnel.lua:193-205`: either destroyed half prevents the pathfinding add, including the load-time call. |
| DomeOverviewHighlight | F14 / F122 | `ColonyControlCenter.lua:1290-1296`: the UI receives computed text with an empty-dome guard. Old pack makes empty zero red; native does not, while populated low stats still go red. |
| GeneForging | F41 / F123 | `Colonist.lua:4719-4728`, consumer `:4745`: each researched parameter is added once. Old wrapper double-pays; the native-only control actually calls the function. |
| GraphConsumedCaption | F19 | `ColonyControlCenter.lua:181-186`: caption adds consumption and maintenance, agreeing with the graph series. |
| MirrorSphereSite | F16 | `MirrorSphere.lua:786-825,828+`: completion refuses new action, while same-action cancellation happens before the refusal. |
| NightShiftWork | F04 | `Colonist.lua:2396-2403`, Idle consumer `:2561`: modular day-window arithmetic handles midnight. |
| OpenPastureStockpiles | C93 | `Animals.lua:1382-1526,1569-1583`: native pool rebuild and new fixups. The settled retail asset gate is preserved, not re-run or elevated into a clean-boot claim. |
| SinkholeIndestructible | F96 | `Sinkhole.generated.lua:4-25` and data preset `:15` declare the flag; `Building.lua:1464` checks it before destruction. |
| TradeRocketFuelRefresh | F119 | `UniversalRocket.lua:1922-1926` refreshes landed cargo rockets; `RocketCompatibility.lua:1139-1144` covers upgrade saves. Settled fixup enrollment remains SOURCE; the landed callback has an executable control. |
| TrainCargoDumping | F46 | `Train.lua:787-831`, TransferCargo consumer `:862/:872`: enabled-resource filtering and assignment preservation. |
| TrainsToVoid | F64 | `Station.lua:289-299`: the native demolition handler calls `DestroySilent` with the station. |
| TrainWaitTime | F21 | `ColonistTransport.lua:615-637`, ExitVehicle `:662`: boarding restamps the clock before journey time is consumed. |
| WispRewards | F07 / implemented half of F15 | `Fireflies.lua:712-738`: free-mode power is scaled and destroy mode omits the extra batch research grant. F15's historical silent-notification scope remains unchanged. |

F126 additionally runs `CommonLua/PropertyObject.lua:1472-1489`. The unknown
preset creates a base instance with an empty id in the desk shim, while the valid
preset control creates its own id. EF008's report-and-continue assertion behavior
is modeled explicitly; class/UI services are stubs, not an engine observation.

Removal residue: Building Codes can leave the normal law-id modifier; Pasture
can leave repaired native entity/pile state; Trade Fuel can leave native request
amounts; train and Wisp fixes can leave ordinary gameplay outcomes. Destroyed
Tunnels changes the runtime pathfinding graph, whose reconstruction is now
native. The retired notification, display, chance, caption, action-guard, shift,
Sinkhole and current Train Wait wrappers add no owned persisted state.
Before `44e6af2`, Train Wait replaced blocking `BoardVehicle`; an old serialized
frame below `PlayPrg` can remain until its ride ends, carrying the correct
restamp. The current `16ff1aa` implementation wraps synchronous `AddSpentTime`.
Deletion adds no executable residue; it does not prove old engine frames absent.

Executable controls use extracted native bodies/presets with positive and
scratch-broken cases, plus the actual old F122/F123/F126 modules. They do not
measure gameplay reach or rendering. The earlier F123 pack-off short circuit is
not a successful control and is not reused as one here.

### Shared inventory

`tools/gamepatch_111_census.py` compares file members, editor items, metadata
order, source registrations and TestKit declarations by name. Its output prints
the members and reconciliation equations; the receipt below retains it.
The retired load rows are the entire metadata change. Existing ignore patterns
already cover the new tools, scratch material and report. Store strings and
version fields remain the preceding release's state, as the brief requires;
the release outbox carries the later surface reconciliation.

Retired TestKit registrations and capture rows are removed. `WispPower` and
`WispResearch` both belonged to `WispRewards`. `OpenPastureStockpiles` and
`TradeRocketFuelRefresh` had no existing kit registration to remove. The shell
probe now skips geometry processing on its fake track; the clogged probe checks
save provenance and controls ambient popup state. Surviving probes are parsed
and counted, not assumed from their old wave headers.

### Internal review and suggestions

A tier-2 reader independent of both builders compared the complete track body,
refund assumptions, archived branch shape and F121 save provenance/cure. No
blocking semantic issue was found. F121's provenance restriction is valid
because vanilla rewrites `metadata.lua_revision` on every save; a healthy 1.1.1
timer cannot retain old save metadata through an ordinary 1.1.1 save. Engine
serialization remains an owner leg. A separate retirement reader checked the
native replacements and consumers, the historical test pinning, and the corrected
F126 control. The repair reader also cleared F125 after requiring preservation of
the native nil return, policy-compliant orig delegation and safe install failure.
The final implementation resolves those findings. These internal reviews do not
replace the owner's separate different-vendor audit.

Suggestion not acted on: C55's historical duplicate-geometry premise may now
be obsolete because native processing excludes repair sites. Closing its engine
grid claim is outside this build; this report does not turn the track desk shim
into an engine observation. No new KEEP audit or unrelated cleanup was done.


A minor F125 observation was not expanded into a change: an incomplete multi-leg
shape safely declines before Require without setting `update_suspect`. No behavior
depends on that diagnostic flag. The obsolete ck193 request to re-earn the removed
Train Wait wrapper's tested status is deleted. The retired Mirror Sphere half of
ck195 is removed while the unrelated Mystery 10 condition and opened date survive.

## Validation and remaining owner work

The [command receipt](GAMEPATCH_1.1.1_BUILD_checks_2026-09-23.txt) preserves each
command, HEAD, exit status and output, plus final pack/tool and companion Lua
fingerprints. Inputs are the archived trees named by each harness. Commands run:

- `python tools/desk_f124_track.py`
- `python tools/desk_f125_vacuum.py`, `python tools/desk_migration_cluster.py`
  (also `--selftest`) and `python tools/desk_migration_observations.py`
- `python tools/desk_c85_clogged.py` and its `--selftest`
- `python tools/desk_gamepatch_retirements.py`
- Historical `desk_c88_prefab.py`, `desk_c93_open_pasture.py`,
  `desk_f119_trade_fuel.py`, `desk_c90_datapatch.py`, `c90_scratch_verify.py`
- Pack and TestKit `parsecheck.py`; `bodycheck.py --selftest`; the six changed
  module/comment manifests via `bodycheck.py --all --module <name>`;
  `patchcheck_selftest.py`; `gamepatch_111_census.py --live-source`
- `python tools/doccheck.py --regen --emit-counts` and `git diff --check`

The census compares the exact retired names against baseline `16ff1aa`, final
disk files, metadata order, editor items, Register declarations and TestKit
declarations. The receipt prints every member and separate reconciliation
equations. It measures declarations, not a retail registration boot.

`aliascheck.py` is report-only. Its findings name `SMRTest.order`, `probes` and
`last` in unchanged `76_SMRTK_Kit.lua`; these fields are defined in the table
constructor in `00_TestCore.lua:19-21`, a form the member detector omits. No
unbound helper was reported. No unrelated toolkit change was made.

The owner-only work is ck209 (separate Claude audit) and ck210 (focused retail
pack-off/on, main-menu enable, migration/track/event behavior and save/remove/load).
The earlier retail A/B retains its single-variable and error-gate limitations.
The completed code response does not clear the untouched KEEP set, authorize a
release, or update published strings. A filled release-outbox entry carries the
later surface work.

The one-off build brief and its exact map row are consumed in the result commit.
A concurrently authored audit prompt/map addition belongs to separate work and
is preserved using WORKFLOW's private-index commit procedure. Doccheck ran
explicitly with the consumed brief removed from a temporary index; its rule scan
otherwise tries to read the unstaged deleted file. The real shared index is
preserved. TestKit reconciliation is local commit `aa47d3e`; the pack result is
pushed. The result commit is discoverable by this report's path.
