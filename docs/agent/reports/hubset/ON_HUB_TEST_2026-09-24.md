# On-hub test for C114 guard 3 and C116, derived from source, 2026-09-24

## Must_Read_Header

Hubset 04's desk output. It is written for link 05, which builds the test; for link 06, which turns
the readings into slots; and for link 99, which audits both. Every design claim is SOURCE on the
archived `1.1.1.405907` tree (`B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src`), unless it is
tagged INFERRED. Nothing here is MEASURED until 07 runs readings R1-R7. The retired sitting's footprint
verdict is void, and this note does not rely on it.

## The test

`OnHubNow(unit, hub)` is synchronous. It never yields, never runs a map query, and copies no
file-local helper.

```
precondition: IsValid(hub) and IsKindOf(hub, "PassageHubBase") and not hub.demolishing
              IsValid(unit) and unit:IsValidPos() and ResolveMap(unit) == ResolveMap(hub)
A (in a connected passage, in flight):
    p = unit.traversing_passage
    IsValid(p) and table.find(p.traversing_colonists, unit)
      and (hub.connected_passages[p] or hub.draining_passages[p])
B (standing on the hub):
    not IsValid(unit.traversing_passage)
    and (unit.holder == hub or unit.passage_hub == hub)
    and HexGridGetObject(hub:GetMap().object_hex_grid, WorldToHex(unit), "PassageHub") == hub
OnHubNow = precondition and (A or B)
```

The test never reads a dome hex (see "Dome hexes" below). Guard 4, the network check, stays separate
in 05.

## Why each input is live or fails closed

| Input | Source (archived 1.1.1.405907) | Why it can't be stale, or how it fails closed |
|---|---|---|
| `unit.traversing_passage` | Set at `Lua/Passage.lua:1206`. Cleared at :1238 in the same destructor that runs the whole walk (pushed at :1207, called at :1246). | The walk runs as a destructor. `SetCommand` on a thread that is running destructors waits for them to finish (`CommonLua/Classes/CommandObject.lua:363-367`, and :216-221 in the new command thread), so a job change cannot cut a crossing short. The flag is cleared at :1238 even when the passage goes invalid, because the loop at :1214 exits and the tail still runs. The fail-closed cross-check is that A also needs `unit` in `p.traversing_colonists`, which is inserted at :1205 and removed at :1239. Both sides must agree. |
| `hub.connected_passages` / `draining_passages` | Connect at `Passage.lua:1560-1561`, disconnect at :1394-1395, draining at :1159/:1172 (fields: `Lua/PassageHub.lua:13-15`). | Written by the hub's own lifecycle. A passage that has left both sets fails A. That includes the C117 disconnect edge, where 05 must decide whether a draining spoke counts. It counts here, because the unit is physically in it. |
| `unit.holder` | `Unit:SetHolderOnMap` (`Lua/Units/Unit.lua:805-822`) calls `holder:OnExitHolder` and `building:OnEnterHolder`, which keep `Holder.units` in step (`Lua/Buildings/Holder.lua:27-41`). | Only a corroborator, never the proof. It can outlive the stay, because `Dome:OnEnterUnit` is empty (`Lua/Buildings/Dome.lua:1850-1851`) and dome entry via `Dome_Entrance` never replaces it (`Lua/Buildings/Dome_Entrance.lua:39-76`). Without the hex check it would grant access far from the hub. |
| `unit.passage_hub` | Set at `Passage.lua:1228`, cleared only at :1235. | Only a corroborator. `ExitBuilding` clears the holder but not the marker (`BuildingWayPoints.lua:541-547`, `Unit.lua:419-466`). That is the C116 defect. |
| hub hex identity | `HexGridGetObject(object_hex_grid, q, r, "PassageHub")`, the same call the game uses to resolve a passage end on a hub (`Passage.lua:257`, :269, :1020). Unit-hex idiom: `IsUnitInDomeRange` (`Lua/Units/ColonistTransport.lua:22-23`). | This is the proof for B. A unit that has walked off the hub, ridden away or entered a dome is on a hex whose `PassageHub` object is nil or another hub, so B is false. The position is the logical position, which can lead the visual position by at most one move step. At the hub edge, B can therefore turn false one step early, which is the closed side. |

Call shapes counted on the archived tree, including definitions: `HexGridGetObject(` 27 bare / 0
method, `WorldToHex(` 291 / 0, `IsUnitInDome(` 39 / 0, `:UpdateOutside(` 11 method. Command:
`grep -rhoE` over `--include=*.lua` on the archived `Src`, with the pattern `(^|[^.:A-Za-z_])NAME\(`
for bare calls and `[.:]NAME\(` for method calls.

## What the leads showed

- **Command and arguments.** Not a signal. `TraverseTunnel` runs inside the move loop of whatever
  command is walking (`CommonLua/Movable.lua:415`, `Lua/Units/Unit.lua:238-246`), so `Work`, `Roam`
  and `Rest` all cross passages. No command names the crossing.
- **Holder and the holder's bookkeeping.** These are one fact, not two. `hub.units` holds exactly
  the units whose `holder == hub` (`Unit.lua:805-822`, `Holder.lua:27-41`), which agrees with C99's
  measurement that all 71 listed units matched their holder. Passage elements never become holders:
  `PassageGridElement.OnEnterUnit = empty_func` (`Passage.lua:819`) overrides the `SetHolder` in
  `WaypointsObj:OnEnterUnit` (`BuildingWayPoints.lua:489-497, 531-535`). So a unit crossing from the
  hub toward a dome keeps `holder == hub` for the whole passage, including ramp hexes over the
  destination dome, until `Passage.lua:1231-1235`. This is why the retired log's `units` lists name
  units up to 18,295 game units from the hub. That those 90 rows were in flight is INFERRED; R2
  checks it.
- **Hex identity.** Needed only for B, the standing case. State cannot separate a colonist dumped on
  the hub (holder cleared, marker set) from one that has left (marker still set).

## Dome hexes: guard 3 need not cover them

- **In flight, A.** A covers every hex of a connected passage by membership, including ramp hexes
  over an endpoint dome, and reads no position. This matters for C114: `Colonist:SetCommand`
  (`ColonistTransport.lua:382`) calls `HasLocalAccess(destination)` at :416 on the caller's thread.
  So a dome shutdown or a job change evaluates access while the colonist is mid-passage.
- **Standing, B.** A standing colonist on a dome hex is never on the hub, so B fails closed.
  - With no holder, native already decides. `IsUnitInDome` returns that dome by position
    (`Lua/Buildings/Dome.lua:159-165`), and `HasLocalAccess` grants the same dome or a
    cluster-connected one (`ColonistTransport.lua:271-275`, :262-268, :249-259).
  - The destination dome's own hex also passes through `IsUnitInDomeRange` (:19-28), but only when
    that dome is the nearest community or the home (:282-290).
  - Over any other dome's hex, B is false and native decides.
- **Finding, routed rather than fixed.** A colonist with a stale `holder == hub` standing inside a
  dome is invisible to `IsUnitInDome`. That function answers from `IsObjInDome(holder)`, which is
  `hub.parent_dome`, and a hub has none (`Dome.lua:111-114`, :159-161; `dome_forbidden`,
  `Lua/BuildingTemplate/PassageHub.generated.lua:12`). `HasLocalAccess` then measures from the hub
  (:282, :293). OnHubNow correctly refuses this colonist. The native denial stays, so the colonist
  can still be booked a ride. Whether a unit keeps a hub holder into a dome at all is INFERRED: it
  needs an overland walk off the hub, since trains and shuttles `SetHolder` their own vehicle. R2
  decides. This routes to 05 and 99 and to the owner; it is not in this link's fence.

## C116: the native outside recomputation, and when clearing is safe

- `Unit:UpdateOutside` (`Unit.lua:468-471`) computes
  `outside = not holder and not IsValid(passage_hub) and not IsUnitInDome(self)`.
  `Colonist:SetOutsideEffects` (`Colonist.lua:3217-3237`) starts or stops `outside_start`.
- **On a dome hex, holder nil:** clearing the marker and recomputing gives `outside == false`
  (the dome, by position). This is safe, and shelter is kept.
- **On open ground, holder nil:** the recompute gives `outside == true` and the timer starts. This is
  C116's intended repair.
- **On the hub (B true) or in flight (A true):** do not clear. The native comment at
  `Passage.lua:1147-1148` and :1228 protects a real dump.
- **Stale `holder == hub`, off the hub:** clearing the marker alone changes nothing, because
  `not holder` keeps `outside == false` (`Unit.lua:469`, `Colonist.lua:2965`). Whether 05's C116
  module should also drop a hub holder that fails OnHubNow is 05's design call. Report it either way.
  It is the same stale-holder finding as above.
- **The hook is 05's call.** Candidates that fire synchronously on departure are
  `Holder:OnExitHolder` for the hub and `Dome_Entrance:TraverseTunnel` on the way in. There is no
  native hook for a pure walk off the hub if the hub is walkable to open ground (R6).

## Stops checked

- A signal exists that is present during a real crossing and cleared or ignorable after it: A for
  flight, and B, identity-gated, for standing. No stop fires.
- No file-local helper or blocking body is needed. The test uses engine globals and fields only.
  `GetPassageAttachedBuilding` (`Passage.lua:247`) is file-local and is not used.

## Readings for 07 (SOURCE predictions; 06 turns each into a preloaded slot)

Each reading gives the object, the field or call, the expected value and the refuting value.
"On-hub hex" means `HexGridGetObject(map.object_hex_grid, WorldToHex(c), "PassageHub") == h`.

1. **R1 - `units` mirrors `holder`.** Object: every hub `h`, every `c` in `h.units`.
   Expected: `c.holder == h` for all. Refuted by any `c.holder ~= h`, which would mean `Holder.units`
   has a writer outside `SetHolderOnMap`.
2. **R2 - every hub member is in flight or on the hub.** Object: every `c` in `h.units`. Classify
   each as (a) A true, (b) on-hub hex with `traversing_passage` false, or (c) neither. Expected
   (c) = 0. Refuted by (c) > 0: a hub holder survived a walk off the hub. That confirms the
   stale-holder finding and the overland walk-off. OnHubNow still fails closed there.
3. **R3 - arrival lands on a hub hex.** Object: a colonist on the tick its dome-to-hub crossing
   ends. Arm a trigger on `traversing_passage` becoming false with `holder == h`.
   Expected: on-hub hex true. Refuted by false: the tunnel exit is outside the hub's registered
   hexes, and B would refuse real arrivals.
4. **R4 - a dump stays on the hub.** Object: a colonist arrived on the hub (`holder == h`), then
   interrupted, for example by firing it. Fields after `ExitHolder`: `holder`, `passage_hub`, the
   on-hub hex check, and `h:GetEntrance(c)` with its last point's hex.
   Expected: `holder` false or nil, `passage_hub == h`, on-hub hex true. Refuted by an on-hub-hex
   false: `ExitBuilding(hub)` walks the unit off the footprint, and B would miss the dump that C114
   exists for.
5. **R5 - the flight flag is live and clears.** Object: a colonist mid-crossing on a spoke of `h`.
   Expected mid-passage: `IsValid(c.traversing_passage)`, `c` in its `traversing_colonists`, and the
   passage in `h.connected_passages`. After arrival: `traversing_passage == false`, and `c` is absent
   from the list. Refuted by the flag being false mid-passage or still set after arrival.
6. **R6 - can a colonist walk off the hub?** Object: a dumped colonist (R4) given a `Goto` to an
   open-ground point 5 or more hexes off the hub on the side away from every spoke.
   Expected (INFERRED from the `Passage.lua:1147-1148` comment "still need this exit to leave"): it
   cannot, so the path goes through a passage tunnel (`pf.GetPathTunnel(c)` non-nil while it
   walks) or fails. Refuted by an overland walk with no tunnel. That is the C116 walk-off, and it has no
   native hook.
7. **R7 - the outside recomputation per hex class.** Object: a marked colonist (`passage_hub`
   valid), fix off. Set `passage_hub = false`, call `c:UpdateOutside()`, read `c.outside_start`.
   Expected: false inside a dome, a game time on open ground with holder nil, and false with
   `holder == h`. Refuted by any other combination. The case with `holder == h` and `outside_start`
   set would also refute the stale-holder analysis.
