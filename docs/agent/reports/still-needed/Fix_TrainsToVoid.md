# Fix_TrainsToVoid review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — no material row/card disagreement found:** station demolition's
  current BuildingDemolished handler still bare-deletes trains whose
  `current_station` names it. Train cleanup still omits the prefab refund.
  The pre-hook reaches the legitimate storage/refund path before that event,
  and the returned count still enables later train assignment. The site covers
  docked trains and trains mid-leg from that station; the card's parked-train
  example describes a narrower valid subset. Recommend **KEEP**.
- **SOURCE precision limit:** returning a Train prefab preserves the ability to
  redeploy; it does not repair broken tracks or bypass destination, capacity and
  platform checks. The row's "can be redeployed" fits that conditional capability.
  Nor is count zero an irreversible inability to operate trains: vanilla can
  construct replacements for resources (`Station.lua:579`–`:587`). The deleted
  old prefabs are lost, but the module header's "disabled ... forever" overstates
  the operational result. Site/card do not promise automatic route rebuilding
  or say replacement construction is impossible.
- **SOURCE — distinguish implemented repair from entry proposals:** F64's entry
  mentions a Train.Done refund guard and compensation for corrupted saves. This
  module implements neither. It pre-hooks Building.OnDemolish for Station
  instances and stores matching live trains; there is no historical compensation
  handler. Keeping the immediate demolition repair does not claim recovery of
  already-lost train counts.
- **INHERITED witness / LIMIT:** F64 has family-level historical corroboration;
  its entry explicitly says the verbatim "trains go to void" report was not
  located and the reported station-removal wording is ambiguous. This sweep's
  fresh boot measures installation only. It does not newly reproduce deletion,
  storage, refund, notification or redeployment in play.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrainsToVoid.lua | F64 | yes — fresh boot applied and direct settled registry active | yes — station demolition reaches pre-hook; DestroySilent invokes refund/storage cleanup, and returned prefab count remains read by UI and valid-track assignment | yes — matching docked or mid-leg trains are stored before bare deletion; redeployment requires a suitable surviving/rebuilt route | yes — parked-train headline is a true narrower example of covered current_station matches | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Station.lua:293; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Train.lua:166; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Train.lua:190; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Track.lua:430 | SOURCE | actual demolition/refund/notification/redeployment; loaded passengers/cargo; transit and ruin-clear races; non-demolition station destruction; corrupted-save compensation; fresh 1.0.7 behavior |

## Primary evidence

- **MEASURED installation, not benefit:**
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:79`
  reports applied. Direct settled registry read at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:226`
  measures active. Both packs and TestKit were enabled; no colony loaded or
  station demolished. Captured module SHA256:
  `63aef6dd6c235fb208e8b44a5c0e056608ccd291c28309fc7fbd373f2d17d9ec`.
- **SOURCE — current demolition caller still reaches the wrapper:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Demolishable.lua:133` calls the
  object's OnDemolish before eventual removal at `:139`.
  Current `Lua/Buildings/Station.lua` declares no OnDemolish; its inherited
  building implementation at `Lua/Buildings/Building.lua:899`–`:908` restores
  terrain, destroys the building and broadcasts BuildingDemolished. The pack
  pre-hook at `Code/Fix_TrainsToVoid.lua:52`–`:61` first stores valid matching
  trains and then calls that original. It is installed at mod-code time; EF-058's
  inherited pre-flattening rule applies rather than a runtime-only base wrapper.
  Foreign/non-Station objects delegate before any station field reads.
- **SOURCE — faulty deletion and cleanup still differ:** current
  `Lua/Buildings/Station.lua:289`–`:299` iterates city Train labels and bare-calls
  DoneObject at `:293` for `current_station == bld`. The Station.Done storage
  loop at `:271`–`:274` separately requires `train.at_station` and calls
  DestroySilent; it cannot refund objects already removed by the demolition
  event. Current `Lua/Units/Train.lua:86`–`:97` kicks passengers out, unassigns
  its track, drops stockpiled cargo and releases platform occupancy, with no
  ColonyAddPrefabs call. CityObject.Done at `Lua/CityObject.lua:35`–`:37` removes
  the object's city labels. Bare deletion therefore still bypasses the refund
  which only Train.OnDemolish supplies on this destruction path.
- **SOURCE — storage/refund/notification siblings remain:** current
  `Lua/Units/Train.lua:157`–`:166` guards invalid/already-destroyed trains, removes
  a valid track transport link, sets zero-countdown demolition and synchronously
  calls DoDemolish. `Lua/Demolishable.lua:133` invokes Train.OnDemolish;
  `Train.lua:188`–`:191` calls `ColonyAddPrefabs("Train", 1, nil, self.city)`.
  Demolishable's current default `use_demolished_state = false` at
  `Demolishable.lua:11` leads to DoneObject at `:139`, before the station's later
  deletion event. The station reason selects the existing storage notification
  text at `Train.lua:170`–`:183`. The legitimate cleanup and label-removal paths
  above remain its consumers; no custom counter or notification is introduced.
- **SOURCE — actual count write and readers:** current `Lua/Colony.lua:867`–`:869`
  routes a positive refund to the single city; `:842` calls City.AddPrefabs,
  and `Lua/City.lua:480`–`:481` increases `available_prefabs`. Current
  `Colony.lua:830`–`:831` calls the count helper, whose `:816` reads City.GetPrefabs
  and whose `:817`–`:824` can add the connected map's count. Current
  `City.lua:475` reads the stored count. Station's send-out button reads
  `ColonyGetPrefabs("Train", self.city) > 0` at `Station.lua:789`; its available
  train value remains the same getter at `:1306`–`:1307`. Current
  `Lua/Buildings/Track.lua:430` refuses assignment at zero prefabs and `:436`
  consumes one to deploy a new Train. The restored count thus remains consumed.
- **SOURCE — valid assignment is a separate condition:** current
  `Station.lua:834`–`:856` checks valid/non-demolishing connected track, repair
  state, a different reachable station, route capacity and a free platform.
  `:864`–`:865` invokes AssignTrain only after those checks; current
  `Track.lua:433` checks capacity/occupancy again before consuming the count.
  Returning the prefab makes later eligible deployment possible; it does not
  by itself make the demolished route eligible or automatically recreate it.
  Vanilla replacement construction also increases the count at
  `Station.lua:579`–`:587`, so "forever" is not the actual train-operation rule.
- **SOURCE — docked and moving current_station matches:** current
  `Track.lua:446` initializes current_station on spawn. `Station.lua:1117`–`:1119`
  sets the arrived station and docked state. `:1207`–`:1209` clears arrival/docked
  flags on departure without clearing current_station; current
  `Train.lua:362`–`:372` departs then traverses the track with that field still
  naming the departed station. `Station.lua:1093` updates it on station traversal
  and `:1117` updates it on arrival. Thus the deletion event and pre-hook can
  match a train traveling on a leg from the demolished station, with no
  `at_station` restriction. The field need not name the origin of an entire
  multi-station journey; public "mid-trip from it" fits the current leg.
- **SOURCE — public row/headline:** site
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:369`–`:376` describes silent count
  loss, docked/mid-trip matching trains and legitimate storage/redeployment.
  The card bullet at `metadata.lua:3` says demolition permanently deleted trains
  parked there, a narrower covered case. Neither text promises historical
  compensation, general station-destruction protection or repair of train motion.

## Not checked, by name

- New live station demolition, exact prefab-count delta, storage notification,
  availability UI refresh or successful subsequent deployment.
- Trains carrying passengers/cargo, dead/destroyed-train edge cases, concurrent
  arrival/departure, destruction callback order or station ruin clearance in play.
- Non-demolition station destruction, disasters, direct DoneObject routes,
  malformed Train labels, foreign Station.OnDemolish overrides or enable-after-load wiring.
- Damaged-track repair, rebuilt-route eligibility, route capacity, platform races,
  or unrelated train movement/passenger bugs beyond the cited assignment readers.
- Historical compensation for already-corrupted saves or a Train.Done refund
  guard; neither exists in this assigned module.
- Fresh 1.0.7 comparison or a renewed search for the unlocated verbatim field report.
