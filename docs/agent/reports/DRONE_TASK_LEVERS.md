# What can restrict what drones do — read 2026-09-20, build not taken

The owner asked for a TestKit button putting every drone into a "minimum safety state": maintenance
and food delivery to consumers only, everything else stopped, reversible. This is the source read
behind the answer. ⛔ **Nothing was built.** The owner's word, after the cost was stated:
*"This honestly seems like it maybe more complicated than its worth?"* They are deciding what they
actually need to observe and will come back. Cheaper alternatives offered, none chosen: delete most
drones with the new group buttons, shrink a hub's work radius, or a much smaller "freeze
construction" button (suspend construction work requests only, no restore list, no food logic).

Everything below is static reading of the archived 1.1.0.403908 tree, by a subagent whose
load-bearing claims were then spot-checked. Nothing was run in game.

## How a drone takes work

`Drone:TryTakeTask` (`Lua/Units/Drone.lua:591`) first scans `BrokenDrones` in radius through
`FindDroneToRepair` (`:321`) — no request involved — then calls the hub's `FindTask`
(`Lua/_TaskRequest.lua:74`), which is a thin wrapper over the **engine C** function
`Request_FindTask`. ⛔ The ranking, and the exact effect of every `rf*` flag, is therefore not
readable from this tree; the Lua side only shows what goes in and what comes back.

Requests reach the hub's queues by building, within `work_radius`
(`CommonLua/TaskRequest.lua:273-283`), and priority comes from the building, not the job
(`GetPriorityForRequest`, `CommonLua/TaskRequest.lua:183-189`).

## What is distinguishable, and what is not

- **Maintenance is identity, not name.** Its work request is `AddWorkRequest("repair", …)` and the
  same `"repair"` string is used by salvage of a destroyed building (`Lua/Buildings/Building.lua:1830`),
  rover repair, dome and passage fractures and cable/pipe repair. The only marker is the pair
  `maintenance_work_request` / `maintenance_resource_request`, both registered in
  `maintenance_request_lookup` (`Lua/RequiresMaintenance.lua:64-86`, checked).
- **Consumer food vs depot food is a flag.** A depot's demand carries `const.rfStorageDepot`
  (`Lua/Buildings/StorageDepot.lua:68`), a consumer's does not; consumers raise theirs in
  `FoodBuilding:InitFoodDemandRequests` (`Lua/Buildings/FoodServiceBuilding.lua:108-120`) and
  `HasConsumption:InitConsumptionRequest` (`Lua/HasConsumption.lua:76-90`). Consumer-food against
  consumer-anything-else is separable only by the resource id.
- `FoodResources` is `"Food"` plus the `MealIngredients` group (`Lua/Resources.lua:14`), while
  `IsFoodResource` answers true only for `"Food"` (`:553-555`). The two disagree; the group list is
  the real one.
- Food-consuming buildings cannot be enumerated from templates: `consumption_resource_type = "Food"`
  appears in no `Data/BuildingTemplate/` file. Enumerate at runtime instead.

## The lever, if it is ever built

`const.rfSuspended` on a request is how the game itself stops work: turning a building off suspends
its maintenance requests (`Lua/RequiresMaintenance.lua:745-749`, checked) and its food demands
(`Lua/Buildings/FoodServiceBuilding.lua:224-244`, checked), and a drone mid-delivery re-checks the
flag and re-targets (`Lua/Units/Drone.lua:1457`, checked). So the state is a sweep: suspend every
request except the maintenance pair, consumer-food demands, and the supply side (supplies are inert
without a demand pair, except those carrying `rfCanExecuteAlone`), then clear exactly what you set.

⚠️ The costs that made the owner stop, each from the bodies above:

- **It must keep sweeping.** Requests created while the state is on are never flagged
  (`RequiresMaintenance:CreateResourceRequest`, `Lua/Units/Drone.lua:1352`, new buildings).
- **The flag is in the savegame.** Save while it is on and the state reloads with the restore list
  gone. Recovery means recomputing the set, which also clears suspensions the game set for its own
  reasons.
- **Two jobs cannot be stopped this way at all**, because they never consult the queues: a drone
  repairing another drone (`Lua/Units/Drone.lua:321`, taken before `FindTask`) and self-recharge
  (`EmergencyPower`, `:1508`). Stopping those needs a wrapper on `Drone:TryTakeTask`.
- The game ships **no** emergency or disaster mode that narrows drone work: no `DustStorm` reference
  exists in `Drone.lua`, `DroneBase.lua` or `DroneControl.lua`.

Hooking `TaskRequestHub:FindTask` is **not** an alternative: rejecting its result does not advance to
the next candidate, so the hook degrades to "do nothing" rather than "do the allowed subset".

## Multi-selection, filed here because it came from the same sitting

The box-drag wrapper's members are the plain array `objects` (`Lua/MultiSelection.lua:109`). Only
unit classes declare `SelectionClass`, so **buildings can never be box-selected**; a mixed drag keeps
whichever class was found first and silently drops the rest (`MultiSelection.lua:33-35`), which reads
as "mixed selection does nothing" when the first class had one member. Vanilla already offers
Reassign, Salvage, Priority and On/Off for a wrapper (`Data/XDef/ipMultiSelect.lua:16-129`). The
group buttons built on 2026-09-20 (kit `3abab0a`) carry the rest of this in their comment block; the
witnesses they owe are in `tools/SMRTK.md`.
