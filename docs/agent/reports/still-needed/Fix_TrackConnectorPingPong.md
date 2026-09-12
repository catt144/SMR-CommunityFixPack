# Fix_TrackConnectorPingPong review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — no material row/card disagreement found:** the site at
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:396` says "an occupied connector is
  left where it is". In context it refers to the ordinary two-building steal
  loop just described, and accurately describes that unforced competing-owner
  path. Both row and headline fit the remaining mechanism. Recommend **KEEP**.
- **SOURCE precision / INFERRED wording risk:** the implemented guard deliberately
  permits a **forced** takeover, including the current vanilla save fixups.
  Plain/unowned elements and elements whose owner is invalid or being destructed
  are also replaceable. Those are source conditions, not a demonstrated public
  falsehood in the ordinary-conflict context. An isolated reading of the final
  sentence could miss that context; this is an optional wording clarification,
  **INFERRED**, not a filed defect or required public change. The sanctioned
  force behavior is already repaired in-body and is not a new code request.
- **SOURCE — stop the loop, not shared-hex route support:** a denied building
  does not gain ownership of that connector. `GetConnectorElement` still returns
  the element at its spot regardless of owner, while track endpoints and
  StationsLink consume the element's actual `station` field. Distinct endpoint
  owners are required for a station connection. Neither the row nor the card's
  headline promises a route through a connector shared by two owners, so the
  broad two-train-building headline remains true for the remaining steal loop.
- **SOURCE — recovery occurs at actual object destruction:** the sibling wraps
  TrackConnectedObjBase.Done, not BuildingDemolished. It records connector hexes,
  lets vanilla cleanup run, and defers unforced rebuilds for eligible nearby
  survivors. A coincident-slot destructor can also remove the surviving owner's
  element because vanilla cleanup has no owner-equality check; existing owner
  retries plus the helper converge through the guard. Do not describe it as
  exclusively deleting the dying building's owned elements or as a measured
  instantaneous recovery at every demolition action.
- **INHERITED / LIMIT:** F66 retains its PT-41 2026-07-26 unforced-path result on
  1.0.7. The force override landed on 2026-09-09, with a desk control and an
  explicitly untested in-play forced pass. This sweep measures installation
  only and preserves those separate grades. No unrelated rebuild audit/status
  is reopened.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrackConnectorPingPong.lua | F66 | yes — fresh boot applied and direct settled registry active | yes — GameInit/retry/fixup callers reach replacement; grid lookup, actual-owner endpoint and station/tunnel route readers remain; Done/reclaim and orphan gate paths remain | yes — occupied-connector outcome describes the ordinary unforced competing-building case in context; maintenance force remains a source condition | yes — two-train-building fight headline fits; no promise that both own the one connector or that every route becomes usable | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TrainTransport.lua:128; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/TrackElement.lua:206; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Track.lua:195; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/StationsLink.lua:78 | SOURCE | live shared-hex geometry and route use; forced fixup execution; actual survivor rebuild/demolition timing; radius coverage; repeated force ordering; save/uninstall capture; fresh 1.0.7 rerun |

## Primary evidence

- **MEASURED installation, not cure:**
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:108`
  reports applied. Direct settled registry read at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:251`
  measures active. Both packs and TestKit were enabled; no colony loaded,
  connector built or forced pass run. Captured module SHA256:
  `94148290a1ec610878bd8590812970b93753d1b30bfb24bf48547b3f05fef020`.
- **SOURCE — current unforced steal and return leg:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TrainTransport.lua:11` calls
  CreateConnectorElements from GameInit. Its original per-spot branch at
  `:128`–`:131` destroys an element owned by another building, with only an
  assert at `:129`. Current `Lua/Buildings/TrackElement.lua:203`–`:208` defers
  CreateConnectorElements for that element's still-valid, non-destructing owner.
  Both the conflicting claim and the retry consumer remain. EF-008 supplies the
  inherited rule not to treat assert as a stopping branch; this sweep does not
  measure whether a retail assert produces a log message.
- **SOURCE — replacement still creates all vanilla connector state:**
  `Code/Fix_TrackConnectorPingPong.lua:144` replaces the current method. Its guard
  at `:160`–`:167` denies only an unforced take from another valid owner not being
  destructed. The subsequent creation keeps the current source's
  `TrackGridElement` station/q/r/track_obj/node_idx state
  (`Lua/TrainTransport.lua:134`–`:142`), position/orientation, permanent/visibility
  flags, grid application and AutoConnectTracks call (`:147`–`:152`). Current
  `TrackGridElement:AutoConnectTracks` at `TrackElement.lua:328`–`:355` consumes
  the element/owner/direction state when processing and connecting adjacent
  elements. The changed path is not a dead writer.
- **SOURCE — direct station-to-station and tunnel readers:** current
  `Lua/Buildings/Station.lua:56` includes TrackConnectedObjBase and
  `Lua/Buildings/TrackTunnel.lua:2` includes the same base. Current
  `Lua/TrainTransport.lua:176`–`:181` gets an element by connector-spot hex,
  without verifying that element's owner equals the caller. Current
  `Lua/Buildings/Track.lua:194`–`:199` reads the actual endpoint elements'
  station fields; `:339`–`:352` requires the caller to be an endpoint to return
  the other station. `:532` calls StationsLink.ConnectStations, whose current
  `Lua/Buildings/StationsLink.lua:76`–`:79` broadcasts connection only for two
  distinct endpoint owners. Station.GetConnectedTrack reads an element tagged
  with that station at `Station.lua:932`, then tests connector direction and
  GetDestStation at `:938`–`:954`. Tunnel.GetConnectedTrack reads its opposite
  tunnel's connector/track at `TrackTunnel.lua:7`–`:9`; the tunnel resolver at
  `Track.lua:331` traverses ForEachConnectedTrack, which consumes connector and
  destination fields at `TrainTransport.lua:70`–`:74`. These readers remain live
  for direct stations and tunnels. One contested element with one station tag
  does not itself establish distinct owners for both buildings.
- **SOURCE — repeated ownership calls and sanctioned force:** if A owns a hex,
  its repeated unforced call does not destroy its own element, and B's unforced
  call leaves A's element valid without creating a B-owned one. Both outcomes
  follow `Code:167` and the following valid-element test. With force, B destroys
  A's element and creates its own; the old owner's deferred unforced retry from
  `TrackElement.lua:206` is then denied by that same guard. Repeated *forced*
  calls can intentionally transfer ownership again; no mutual-sharing model is
  added. Current `TrackElement.lua:987`–`:997` forces every station's connector
  rebuild at `:992`, then forces track reconnection at `:995`. The older current
  Station fixup at `Station.lua:1510` also passes true. The current assert at
  `TrainTransport.lua:129` explicitly permits force; the pack's force override
  therefore preserves those primary callers. This is source branch reasoning,
  not a new live forced-pass or ordering measurement.
- **SOURCE — destructor/reclaim sibling still has a consumer:** current
  `TrackConnectedObjBase:Done` at `TrainTransport.lua:14`–`:37` reads each
  connector-slot hex and deletes/disconnects the found element/track without a
  `el.station == self` restriction. Its two-stationed-element special case
  defers whole-track deletion at `:24`–`:26`; otherwise it disconnects/deletes
  at `:28`–`:31`. Current Track.DestroyTrackElements at `Track.lua:179`–`:182`
  schedules the deleted element's owner, not a generic connectorless neighbour.
  The pack's Done wrapper at `Code:225`–`:245` records spots before cleanup and
  calls TrackConnectorReclaim afterward. The helper at `:199`–`:216` deduplicates
  candidates across recorded hexes, queries radius three for TrackConnectedObjBase,
  excludes the dying/invalid/destructing candidate, and revalidates inside a
  deferred unforced CreateConnectorElements call. Existing survivor elements
  make repeated calls idempotent; if vanilla coincident-slot cleanup removed a
  surviving owner's element, its own retry and the helper both use the same
  guarded creator. The map-teardown branch at `Code:226`–`:228` delegates without
  reclaim, preserving the vanilla early return at `TrainTransport.lua:15`.
- **SOURCE / inherited safety limit:** the reclaim thread's first statement is
  the `if not SMRFixPack then return end` orphan gate at `Code:214`; the body then
  only revalidates and calls the synchronous creator. EF-023/EF-029 provide the
  inherited persistence/deferral facts. Capture of a created-before-first-run
  thread and current uninstall/save behavior are not newly established here.
- **SOURCE — public text:** site
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:388`–`:396` describes the ordinary
  two-building fight and a surviving occupied connector; that context supplies
  the ordinary competing-owner scope. The card's
  `metadata.lua:3` bullet names the same two-train-building fight and fits the
  remaining mechanism. The current module title's station/tunnel example is a
  subset of the generic base-class guard, not an exclusion of two stations.

## Not checked, by name

- Current live shared-hex connector positions, station-to-station/tunnel train
  routes, repeated rebuild timing, stability or screenshots.
- In-play forced save-fixup execution, order of repeated force ownership changes,
  cross-platform old-save triggering or a new forced-path test result.
- Actual survivor recovery after demolition/removal, ruin waiting for clearance,
  concurrent element/track destruction or radius-three coverage of all current
  native/foreign connector spots.
- New save/uninstall round trip, pending-before-first-run thread capture or orphan
  execution; the first-statement gate was source-read only.
- Double-turn placement restrictions, shared-owner redesign, unrelated salvage
  rebuild status, every possible rail topology or fresh 1.0.7 runtime rerun.
