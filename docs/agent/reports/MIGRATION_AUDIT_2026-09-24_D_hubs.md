# Audit D: Passage Hubs and passage traversal (game build 1.1.1.405907)

> **Correction, 2026-09-24 (hubset 03 and 99):** the premise `LeadIn → OnEnterUnit → SetHolder(element)` at lines 77, 89, 112 and 353 (75, 87, 110 and 351 before this note was inserted) is contradicted by `Lua/Passage.lua:819`, `PassageGridElement.OnEnterUnit = empty_func`. Passage elements never become holders. Rows built on that premise (element-holder lifetime, C42's stale member) are void; see `HUBSET_AUDIT_2026-09-24.md` §2.1.

Read-only source audit. Unless marked otherwise, every citation is `file:line` in the archived
**1.1.1.405907** tree `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src\Lua` (paths relative to
`Lua/`, or `CommonLua/` where stated). Citations marked (1.1.0) are from `...\1.1.0.403908\Src\Lua`.

**The brief's Passage.lua anchors are 1.1.0 line numbers.** 1.1.1 inserted one line at
`Passage.lua:1009` (1.1.1) (the `air.unavoidable_consumption` line), so everything after it moved down
by one. In 1.1.1: `WouldStrandHubColonists` is :1131-1152 (the dump comment is :1147-1148, the filter
:1149-1151), `OnDemolish` is :1163-1185, `TraverseTunnel` is :1201-1248 (the dome-branch
`unit.holder = nil` is :1234), `DisconnectDomeFromHub` is :1435-1444 and `ConnectDomeToHub` is
:1593-1601. `Colonist:SetOutsideEffects` starts at `Units/Colonist.lua:3217`; the brief's :3223-3231
range is its `else` branch.

Classes used below: **SOURCE-VERIFIED** means every link was read at the cited lines.
**HYPOTHESIS** means at least one link depends on engine data or behaviour that this tree cannot show
(entity waypoints, passability of the hub mesh, C functions).

---

## 1. The piece

### 1.1 Data

- **`PassageHubBase`** (`PassageHub.lua:1-18`) has the parents `ElectricityGridObject`,
  `LifeSupportGridObject` and `Building`, and the flag `efWalkable = true` (:5). `Building` inherits
  `BaseBuilding`, and `BaseBuilding.__parents = { "Holder", ... }` (`Buildings/BaseBuilding.lua:10`).
  **So a hub is a `Holder` and a `WaypointsObj`, and `hub.units` is a real holder list.**
- `hub_domes` (:10-12, created in `Init` :21) is a hybrid table: an array of domes plus
  `{[dome] = number of passages from that dome}`.
- `connected_passages` (:13, :22) is `{[passage]=true}`. `ConnectDomes` writes it
  (`Passage.lua:1560-1561`) and `DisconnectDomes` clears it (`Passage.lua:1394-1395`). It also gates
  hub demolish and refab (`PassageHub.lua:43-49`).
- `draining_passages` (:15, :23) is `{[passage]=true}`. `OnDemolish` writes it (`Passage.lua:1170-1172`);
  `ClearHubDraining` clears it (:1154-1161), called from `Done` (:1337) and on a cancelled salvage (:1104).
- `units` (inherited, `Buildings/Holder.lua:3`) is maintained **only** by `Holder:OnEnterHolder`
  and `OnExitHolder` (`Holder.lua:27-41`). Those two are reached only through `Unit:SetHolderOnMap`
  (`Units/Unit.lua:804-822`).
- On the passage: `traversing_colonists` (`Passage.lua:860`, created at :1253); `hub_draining`
  (:884); `domes_connected = {b1, b2}` (:1559), where either endpoint can be a hub. `GetConnectedHub`
  (:1119-1124) returns that hub. The tunnel elements `elements[1]` and `elements[#]` carry
  `is_pf_tunnel = <arrival building>` (:1737, :1739) until `RemovePFTunnel` sets it to nil (:710).
- On the colonist: `passage_hub` (`Units/Unit.lua:18`), `holder` (:17) and `traversing_passage`
  (`Units/Colonist.lua:151`).

### 1.2 What a hub does to the cluster and the network

A hub never enters `connected_domes`. `ConnectDomeToHub` (`Passage.lua:1593-1601`) refcounts
`hub_domes[dome]`. When that count goes from 0 to 1, it calls `ConnectDomePair(dome, other)` for
every dome already on the hub, then appends the dome. `ConnectDomePair` (:1573-1591) refcounts
`connected_domes` in both directions and rebuilds `dome_network` (`Buildings/Dome.lua:688-706`) on
the first link.

**Every pair of domes on one hub therefore becomes direct neighbours.** That puts them in each
other's `GetClusterDomes()` (`Dome.lua:745-747`), in `IsInClusterWith` (:749-751), in services (F62)
and in the passage path `GetDomesPassagePath` (`Passage.lua:1300-1330`), which returns `[d1, d2]`
and leaves the physical detour through the hub to the pathfinder. Supply grids are joined by the
hub's own footprint, which is star-connected (`PassageHub.lua:51-76`).

### 1.3 Pathing, entering, traversing and exiting

- **Tunnel.** `AddPFTunnel` (`Passage.lua:1651-1740`) registers two engine tunnels. Each starts at
  a point on the departure building and exits on the arrival building's hexes. For a hub, `FixPt`
  keeps the exit on the hub's hexes (:1634-1649). The tunnel weight is
  `1*guim*#elements` scaled to the default pass cost (:1733-1734), and the comment there says
  "passages are considered very short". A hub endpoint gets no `passage_entrances/exits` tables
  (:1714-1731, "a hub is a passthrough").
- **Enter.** A colonist on any Goto hits the tunnel. `Movable:TryContinueMove` calls
  `Movable:TraverseTunnel` (`CommonLua/Movable.lua:413-417, 465-476`), which calls
  `PassageGridElement:TraverseTunnel` (`Passage.lua:807-809`), which calls
  `PassageBase:TraverseTunnel` (:1201-1248).
- **Traverse.** :1205 inserts the colonist into `traversing_colonists` and :1206 sets
  `traversing_passage`. Then the **whole walk runs inside a pushed destructor that is popped at
  once** (:1207, :1246). `LeadIn` goes element by element (:1214-1222), and each `LeadIn` runs
  `OnEnterUnit → SetHolder(el)` (`Buildings/BuildingWayPoints.lua:489-497, 531-535`). Because
  `PopAndCallDestructor` marks the thread as `thread_running_destructors`
  (`CommonLua/Classes/CommandObject.lua:441-461`), **any SetCommand issued during the walk is
  deferred.** `DoSetCommand` returns without deleting the thread (CommandObject.lua:363-368), the walk
  completes, and the old thread then halts (:458-459).
- **Exit at a hub** (:1225-1229): `SetHolder(hub)` removes the colonist from the last element's
  `units` and appends it to `hub.units`. Then `passage_hub = hub` and `UpdateOutside()`.
  `Colonist:SetHolder` lets a ticketed colonist keep its train ticket across a hub
  (`Units/ColonistTransport.lua:766-776`). The Goto then continues across the hub surface to the
  next tunnel **with holder = hub for that whole walk**.
- **Exit at a dome** (:1230-1236): `SetHolder()` runs only if a valid `passage_hub` exists. Then comes
  a raw `unit.holder = nil` and `passage_hub = nil`. `UpdateOutside` is **not** called.
- **Leaving the hub by the next passage.** The first `LeadIn` calls `SetHolder(el)`, which runs
  `hub:OnExitHolder` and keeps the lists correct.

### 1.4 What the access rules and planner see for a colonist on a hub

| Test | Colonist with holder = hub | Colonist dumped (holder nil, passage_hub set) |
|---|---|---|
| `IsUnitInDome` (`Dome.lua:159-166`) | `IsObjInDome(hub)` = `hub.parent_dome` = false (:113-114) | `GetDomeAtPoint(pos)` = nil |
| `UpdateOutside` (`Unit.lua:468-471`), `StopMoving` (`Colonist.lua:2963-2966`), `OnExitUnit` (`BuildingWayPoints.lua:541-547`) | sheltered | **sheltered, wherever it stands** |
| `IsColonistExposedToDisaster` (`Colonist.lua:1278-1282`) | not exposed | **not exposed** |
| `HasLocalAccess` (`ColonistTransport.lua:270-300`) | community is the one nearest the **hub** (:282); range is measured hub to community centre (:263) or `to_check` = hub (:293) | nearest to the unit; unit to centre (:19-28, :263); `to_check` = unit |
| `GetStartingPoint` (:29-35) | returns the **hub** | returns the unit |
| `IsInSafeAtmosphere`, new in 1.1.1 (:836-842) | false (a hub is not a `Community`) | false |
| `Idle` (`Colonist.lua:2501-2503`) | not in a dome, so `Abandoned` if `not dome or dome_enter_fails > 0` | same |

---

## 2. State and lifecycle

| Field | Set | Cleared | Persisted |
|---|---|---|---|
| `unit.passage_hub` | `Passage.lua:1228` only | `Passage.lua:1235` only (dome-side exit) | yes (Lua member) |
| `unit.holder` = hub | `Passage.lua:1227` | any `SetHolderOnMap`: next passage `LeadIn`, `ExitBuilding/LeadOut` (`BuildingWayPoints.lua:541-544`), `ExitHolderImmediately` (`Unit.lua:1196-1205`), `KickFromBuilding` (`Unit.lua:288-305`), `Unit:Done` (`Unit.lua:54-59`), entering any other holder | yes |
| `unit.holder` = element | `LeadIn` → `OnEnterUnit` | next element; hub exit (:1227); dome exit via `SetHolder()` **only if the marker is valid** (:1231-1233); otherwise the raw nil at :1234 | yes |
| `unit.traversing_passage` | :1206 | :1238, inside the destructor | yes |
| `passage.traversing_colonists[]` | :1205 | :1239, inside the destructor; `SavegameFixups.InvalidColonistsInPassages` (:2627-2631, runs once per save) | yes |
| `hub.units[]` | `Holder:OnEnterHolder` via `SetHolderOnMap` | `Holder:OnExitHolder`; `KickUnitsFromHolder` on hub `Done` | yes |
| `element.units[]` | same | same, **except the raw `holder = nil` at :1234, which leaves the entry** | yes |
| `hub.hub_domes` | :1594-1600 | :1436-1443 | yes |
| `hub.draining_passages[p]`, `p.hub_draining` | :1170-1172 | `ClearHubDraining` :1154-1161 (from `Done` :1337, cancel :1104) | yes |
| `element.is_pf_tunnel` | :1737, :1739 | `RemovePFTunnel` :710, from `DisconnectDomes` :1404 and element `Done` :683 | runtime; re-added on load (:1607-1631) |

**Lists a colonist can be left in:** `element.units` (C42, see §7), `hub.units` (while it carries
holder = hub; see S4) and `traversing_colonists` (only if the destructor throws; see S9). Separately,
`passage_hub` can stay on a colonist indefinitely: it is cleared only at :1235.

---

## 3. Interruption

**Mechanics.** An interrupt is `Unit:InterruptCommand` (`Unit.lua:860-865`) or a direct
`SetCommand`. `Colonist:SetCommand`, the wrapper at `ColonistTransport.lua:382-503`, **runs in the
caller's thread and evaluates access against the colonist's state at that moment.** Only the thread
switch is deferred.

| Where the colonist is | What the interrupt does | State left |
|---|---|---|
| **Inside a passage**, mid-`LeadIn` | `InterruptVisit` sees `lead_in_out`, sets `lead_interrupted`, and returns nil (`Unit.lua:874-878`), so `InterruptCommand` calls `SetCommand("Idle")` at once. The wrapper runs **with holder = passage element**. The thread switch is deferred (CommandObject.lua:363-368). `LeadInDestructor` repeats the interrupt (`BuildingWayPoints.lua:481-487`). | The walk completes. Hub side: holder = hub, marker = hub. Dome side: holder nil, marker nil. Then the new command starts. |
| **On the hub surface**, walking (holder = hub) | The Goto thread is deleted (CommandObject.lua:378). | holder = hub, marker = hub, standing where it was. |
| New command then calls `ExitHolder`: `Transport` (`Colonist.lua:3974`), `Unit:EnterBuilding` (`Unit.lua:317-322`), `Abandoned` (`Colonist.lua:1435`), `Stranded` (`ColonistTransport.lua:912`), `GoToRandomPos` (`Unit.lua:706`), `UseElevator` (`Unit.lua:1051`) | **This is "the dump".** `Unit:ExitBuilding(hub)` (`Unit.lua:419-466`) calls `hub:GetEntrance`: a waypoint chain if the entity has one, else `GetEntranceFallback`, which walks from the hub origin along its facing until passable (`BuildingWayPoints.lua:234-257, 259-277`). Then it walks to the entrance, runs `LeadOut`, and `OnExitUnit` clears the holder. `SetOutside(not parent_dome and not IsValid(passage_hub))` gives false (:541-547). | **holder nil, passage_hub = hub**, standing at the hub entrance or origin. The dump code is `Unit:ExitBuilding` plus `WaypointsObj:OnExitUnit`. **Nothing in any exit path touches `passage_hub`.** |
| Death | `Colonist:Die` destructor → `ExitHolderImmediately` (`Colonist.lua:1302`; `Unit.lua:1196-1205`), which places the body at the hub exit position | holder nil, **marker kept**. The corpse stays for `Sleep(8*hour_duration)` (`Colonist.lua:1323`) before `DoneObject`. |
| Shift or firing | `Workplace:RemoveWorker` (`Workplace.lua:473-483`, `:480`) and `Colonist:SetWorkplace(false)` (`Colonist.lua:1756-1758`) → `InterruptCommand` for a worker in `Work`, wherever it is | as the rows above |
| Dome switched off (**new in 1.1.1**) | `Dome:OnSetUIWorking(false)` → `KickWorkersFromBlockedBuildings` (`Dome.lua:1905-1935`) → `KickAllWorkers` (`Workplace.lua:962-974`) → `SetWorkplace(false)` → `InterruptCommand` | **a mass interrupt of every en-route worker** |
| Passage disconnect | `DisconnectDomePair` → `FireWorkersFromOutsideCluster` (`Passage.lua:1418-1427`; `Dome.lua:2121-2133`) → `SetWorkplace(false)` → interrupt | mass interrupt when a hub passage leaves domes out of cluster |
| Shuttle takes a task | `colonist:InterruptCommand()` (`Buildings/ShuttleHub.lua:800`) | as above |
| Hub power loss or refab | `InterruptUnitsInHolder` (`Building.lua:904-908`) → `InterruptVisit`. For a colonist walking across a hub it is a no-op: `lead_in_out` is false on the hub and there is no `visit_end_time`. Hubs also have no consumption (`PassageHub.lua:34-41`). | nothing |
| Demolish of **this** passage while colonists are mid-traversal | `DisconnectDomes` (:1181) → `RemovePFTunnel` (:1404) sets `element.is_pf_tunnel = nil`. A traverser then reads `exit_building = nil` (:1224) and **takes the dome branch at a hub**. | **on the hub with holder nil and marker nil**, so outside by every test; the last element's `units` is left stale (see S5) |
| Hub removed | `Building:Done` → `KickUnitsFromHolder` (`Building.lua:529-533`; `Holder.lua:11-25`) → `KickFromBuilding`: `SetPos` to the hub exit, `SetHolder(false)`, `SetCommand("Idle")` (`Unit.lua:288-305`) | holder carriers are **teleported to the hub**; dumped colonists are not in `units` and are untouched |

---

## 4. After the dump

**The wrapper.** Every Idle entry goes through it. A finished command falls to `self.Idle` with no
argument (CommandObject.lua:274-278), which calls `SetCommand("Idle","checked")`
(`Colonist.lua:2429-2431`). The wrapper then forces `dest = "checked"` (`ColonistTransport.lua:389-390`),
takes `Idle_TransportDestination` = `self.dome` (:193-195), and evaluates `can_reach = HasLocalAccess(home)` (:416).

**The access test, from a hub.**
1. `current_dome` = nil.
2. `community = FindNearestObject(Community label, holder or self)` (:282). The engine picks by
   object position, which for a dome is its centre (`CommonLua/LuaExportedDocs/Game/GameObject.lua:1200`).
3. `HasAccessViaCommunity(community, home)` (:260-268) needs `IsBuildingInDomeRange(hub, community)`
   or `IsUnitInDomeRange(unit, community)`. Both are `HexAxialDistance(community centre, hub or unit) <= 20`
   (`Workforce.lua:131-136`, `Dome.lua:2349-2351, 2361-2363`; `ColonistTransport.lua:19-28`).
   If that holds, `IsDestinationInCommunityRange(community, home)` passes, because home is in its
   own cluster (:249-258).
4. If home is not the nearest community, the same test is repeated against home (:287-290).
5. Fallback: `20 >= HexAxialDistance(holder or unit, home)` (:293-299).

**Pass condition.** A colonist on a hub has local access to its home **only if the hub (or the unit)
is at most 20 axial hexes from the centre of the nearest community, or of home.** Passage connectivity
is never consulted for the colonist's own position.

- **Small dome.** A hub at the shell of a dome of radius R passes whenever R + (shell-to-hub
  distance) is at most 20, which holds for any small dome with a short passage.
- **Radius-19 dome.** Nothing outside the shell ring is within 20 of the centre, except a hex at
  exactly 20. The measured 24-28 fails. It also fails for most of every passage element on Brussels'
  side, when the check happens mid-passage (§3, row 1).
- **Nearest-community exception.** If the hub is nearer (by centre) to a small work dome whose
  centre is within 20, access passes through that dome's cluster.

**The rescue ride.** After a failed test:
1. There is no train route, and `destination ~= home` is false for Idle (:447).
2. `elseif home` (:453) → `GetTransportRoute(home)` (:455) finds nothing → `not HasLocalAccess(home)` (:461)
   → `IsLRTransportAvailable` (:463) → `CreateColonistTransportTask(self, false, home)` (:464).
3. **The pickup is the colonist's position at that instant** (`LRTransport.lua:106-111`): on the hub,
   or **inside the passage** if the interrupt landed mid-traversal.
4. `SetCommand("Transport", home)` (:471).
5. `Colonist:Transport` (`Colonist.lua:3963-4010`): `pickup_pos = GetPassablePointNearby(landing)`
   (:3973). For an in-passage landing this is the nearest passable ground beside the tube, which is
   outside. Then `ExitHolder` (the dump), `Goto(pickup)`, and `state = "ready_for_pickup"` (:3986).
6. It leaves at once if `IsLRTransportAvailable` is false (:3992). Otherwise it waits
   `while IsWaitingTransport() and elapsed < ColonistMaxWaitShuttlePickupTimeMs` (:4000-4006), where
   that constant is `const.DayDuration`, i.e. **one sol** (`_GameConst.lua:143`).
   `IsWaitingTransport` (:3909-3923) quits early only when no shuttle is committed **and**
   `IsLRTransportAvailable` is false.
7. When the wait ends, `WaitTransport` cleans up and the next Idle repeats the same test. That is a
   loop for as long as the colonist stands out of range.

**Without shuttles**, the wrapper sends a non-Work command to `Stranded` (:480-483). `Stranded` in
1.1.1 re-tests `HasLocalAccess` (:888), tries a train, then `TryToMigrateHome` (:896, new), and only
then books a shuttle. `IsInSafeAtmosphere` is false on a hub, so it may `ExitBuilding` or walk to a
station (:909-914) even though the marker keeps the colonist oxygen-safe. Whether
`GetNextMigrationLeg` yields a final walk leg from a hub, and so a walk home, was **not traced**.

**When the oxygen timer starts.** `outside_start` is set only by `SetOutsideEffects(true)`
(`Colonist.lua:3217-3238`):
- With the marker valid, `UpdateOutside` (`Unit.lua:469`), `StopMoving` (`Colonist.lua:2965`) and
  `OnExitUnit` (`BuildingWayPoints.lua:546`) all pass false. **A marked colonist never starts the
  timer**, and each stop clears it (`Colonist.lua:3223-3228`).
- Only unconditional `SetOutside(true)` calls start it, such as the dome-door exit
  (`Buildings/Dome_Entrance.lua:71`).
- The timer is checked at `Colonist.lua:4901-4905` against `OxygenMaxOutsideTime` = 120000
  (`__const.lua:1753-1758`).

**What the pack's `Fix_ShuttleHubOffAvailable` (F54) changes.** It filters `IsLRTransportAvailable`
to false when every people-capable shuttle hub is switched off. The effects:
- the wrapper books no ride and goes to `Stranded` (:463, :482);
- `Transport` abandons a pickup immediately (:3992);
- `IsWaitingTransport` stops waiting without a committed shuttle (:3919);
- `IsInWalkingDistDome` treats more passage-network pairs as walkable (`Dome.lua:315-316`).

**It does not touch the access test.** With a switched-on hub, behaviour is identical to vanilla.

---

## 5. Demolish and disconnect (C99)

**Flow.** `Demolishable:ToggleDemolish` starts `DoDemolish` (`Demolishable.lua:33-50`). After the
countdown, `DoDemolish` sets `demolishing = nil`, calls `OnDemolish`, then `DoneObject`
(:90-140). `PassageBase:OnDemolish` (`Passage.lua:1163-1185`):
1. re-sets `demolishing = true`;
2. registers in `hub.draining_passages`;
3. **blocks in `while WouldStrandHubColonists() do WaitWakeup(1000)`** (:1175-1177);
4. then `DisconnectDomes`, then waits on its own `traversing_colonists` (:1182-1184).

During the block the UI shows "waiting for colonists to exit" (:1187-1190). Cancelling kills the
thread (`Demolishable.lua:43-50`) and `OnSetDemolishing(false)` reconnects (:1093-1110). Passage salvage
dispatches no drones, so "the drones don't react" is expected and says nothing about the loop.

**The clauses** (:1131-1152):

| Clause | Reading | What makes it permanently true |
|---|---|---|
| Escape: any sibling with `elements[1].is_pf_tunnel` (:1134-1138) | A demolishing sibling **stays active until its own `DisconnectDomes`**, so siblings do not wait on each other. Whichever passage checks first leaves at once. **Only the last exit waits.** | Nothing. **C99's mutual-wait reading is refuted.** |
| 1 · own `traversing_colonists` (:1139) | cleared at :1239 inside the destructor | only if the destructor throws before :1239 (HYPOTHESIS, S9) |
| 2 · `#hub.units > 0` (:1139) | `hub.units` is kept exact by `SetHolderOnMap`. No raw holder write targets a hub (§10, command 6). | a colonist that **keeps holder = hub** while stationary or away: off-hub carriers and shuttle riders (S4, HYPOTHESIS), or colonists living on an island hub |
| 3 · a sibling in `draining_passages` with traversers (:1142-1146) | transient | same as clause 1, via the sibling |
| 4 · any Colonist within `hub:GetRadius()*2` with `passage_hub == hub` (:1149-1151) | **the marker is cleared only at :1235** | any marked colonist that stays near the hub: rescue waiters on the hub (a one-sol wait that re-books, §4), `Stranded` colonists waiting there (`ColonistTransport.lua:943`), corpses for 8 h (§3), colonists at the neighbouring dome's shell next to the hub. `MapHasAny` probably skips colonists detached inside buildings (engine behaviour, unverified). |

**Refcounts.**
- `ConnectDomeToHub` / `DisconnectDomeFromHub` (:1593-1601, :1435-1444) are symmetric. A pair is
  formed when a dome's count goes 0→1 and dissolved at 1→0. `ConnectDomePair` / `DisconnectDomePair`
  keep their own per-pair count (:1573-1591, :1407-1433), so a hub pair and a direct passage between
  the same two domes coexist correctly.
- **No refcount defect found.**

**Dome removal.** `Dome:CanDemolish` requires `#connected_domes <= 1` (`Dome.lua:1791-1793`). **It
does not look at `connected_passages`.** A dome whose only passage goes to a hub carrying no other
dome has `connected_domes = {self}`. Whether the passage elements block it through `labels.Building`
was not traced (S11, HYPOTHESIS).

**Hub removal.** Allowed only with no connected passages (`PassageHub.lua:43-45`). `Done` kicks
holder carriers (§3). Dumped colonists keep a marker to a dead hub and become "outside" at the next
`UpdateOutside`.

**Save and load.**
- Every field in §2 is an ordinary Lua member and persists. So does the demolish thread, a game-time
  thread (`Demolishable.lua:42`), and with it the wait loop.
- PF tunnels are re-added after load (`TryAddPFTunnel` / `PostLoadGame`, `Passage.lua:1607-1631`).
  `passage_entrances/exits` are reset on load (:1618-1624).
- `InvalidColonistsInPassages` (:2627-2631) is a one-time fixup, so it does not clean a stale
  `traversing_colonists` created later.
- **A stuck state survives save and load unchanged.**

---

## 6. 1.1.0 → 1.1.1

Commands: `diff` per file, and `diff -u -F '^function'` for hunk names (§10). Changed-line counts
(`diff | grep -c '^[<>]'`):

| File | Changed lines |
|---|---|
| `PassageHub.lua` | 0 |
| `Buildings/Holder.lua` | 0 |
| `Passage.lua` | 3 |
| `Units/Unit.lua` | 12 |
| `Buildings/BuildingWayPoints.lua` | 10 |
| `Construction/GridConstruction.lua` | 4 (T-id only) |
| `Units/ColonistTransport.lua` | 71 |
| `Buildings/Dome.lua` | 154 |
| `Units/Colonist.lua` | 636 |

**Unchanged hub and traversal code.** Every hub and traversal declaration is unchanged:
`PassageHubBase` (whole file), `TraverseTunnel`, `WouldStrandHubColonists`, `OnDemolish`, the
connect/disconnect family, `AddPFTunnel`, `GetDomesPassagePath` and `UpdateConnectedNetwork`. Also
unchanged: the `SetCommand` wrapper, `HasLocalAccess` and its helpers, `Colonist:Idle`, `Abandoned`,
`SetOutsideEffects`, `TransportByFoot`, `KickFromBuilding` and `SetHolder`. **The centre-measured
access rule and the stale marker are 1.1.0 defects that ship in 1.1.1.**

**Changes that touch this surface:**
- `Passage.lua:1009`: passage air consumption marked unavoidable. Not a traversal change.
- `BuildingWayPoints.lua:500-518`: `LeadOutDestructor` now clears `lead_in_out` before its
  `IsValid` early-return. That is on the dump path (`ExitBuilding` → `LeadOut`) and makes it safer
  for a unit deleted mid-exit.
- `Unit.lua:658-686`: hardening in `GoToRandomPosInDome` for an invalid dome or position.
- `Dome.lua:1905-1943` **(new)**: `OnSetUIWorking(false)` → `KickWorkersFromBlockedBuildings`. This
  is a new mass-interrupt source (§3).
- `ColonistTransport.lua`:
  - `MigrateStep` status text (:173-174);
  - `start_wait` (:624);
  - train-leg transfer (:677-687);
  - `IsInSafeAtmosphere` (:836-842), false on a hub;
  - `TryToMigrateHome` (:848-867);
  - `Stranded` reordered (:871-944): shelter only when `not IsInSafeAtmosphere()`.
- `Colonist.lua`: the multi-leg migration.
  - `BookShuttleRide`: the pickup is the nearest pad of any kind, measured from `holder or self`, so
    from the hub for a hub holder.
  - Also `StartShuttleLeg`, `StartMigration`, `FailMigrationStep`, `AbortMigration`, `MigrateStep`
    (:2155-2216), and the `WaitTransport` / `Transport` leg handling (:3928-4010).

**The new traverser: `MigrateStep` (`Colonist.lua:2155-2216`).**
- For an intermediate walk leg it builds `GetDomesPassagePath(current_dome, leg.dome)` (:2201) and
  calls `EnterBuilding` for every dome on it **with each result ignored** (:2204-2209). Only the final
  `EnterBuilding(leg.dome)` is checked (:2210-2212). This copies `TransportByFoot`
  (`Colonist.lua:3843-3848`), which is identical in 1.1.0.
- A hop that fails part-way leaves the colonist wherever its Goto stopped, which can be a hub (holder
  = hub). `OnEnterDomeFail` then raises `dome_enter_fails` (`Colonist.lua:1416-1423`). The next hop's
  `EnterBuilding` dumps it (`Unit.lua:321`) and tries again from there.
- A final failure goes to `FailMigrationStep`, which sleeps 1 s and issues `SetCommand("Idle")`
  (:2129-2138). That Idle runs the wrapper **from the hub** (§4). With `dome_enter_fails > 0`,
  `Idle` sends it to `Abandoned` (`Colonist.lua:2501-2503`), which is C109's entry path.
- Up to 8 legs per step (:2118) and 5 fails before `AbortMigration` (:2119).
- **Hub-specific consequence.** Because hub pairs are direct neighbours, a migration from Brussels to
  a work dome is one "hop" whose physical route crosses a hub. A migrating colonist therefore
  traverses Brussels' hubs just as often as commuters do.

---

## 7. Library cross-check

**C42 (stale `element.units` entry).** *Confirms the mechanism on 1.1.1 and narrows it.*
- 1.1.0 added `if IsValid(unit.passage_hub) then unit:SetHolder() end` (:1231-1233). So the stale
  entry now arises only on a dome-side exit **without** a valid marker: dome↔dome passages, and
  hub→dome after the marker was lost.
- A hub-side exit uses `SetHolder(hub)` (:1227) and is clean.
- *Adds:* a demolish-time route (S5). `DisconnectDomes` nils `is_pf_tunnel` while colonists are still
  inside, so colonists arriving at a hub take the dome branch and leave stale entries. The same
  passage's elements are then deleted (`CleanupHackedConnections` → `DoneObject(e)`, :1377-1383)
  **straight away**, so `KickUnitsFromHolder` teleports those colonists back to the element and
  forces Idle. **That is the first concrete, frequent trigger for C42's teleport.**
- C42's "one untraced link" is closed on 1.1.1 too:
  `LeadIn → OnEnterUnit → SetHolder` (`BuildingWayPoints.lua:489-497, 531-535`).
- C42's three empty samples came from a 1.0.7 save and bear on that save only.

**C99 (hub passages undismantlable).** *Confirms the loop. Corrects two of its four clause readings.
Adds the causes.*
- Clause 3's mutual-wait reading is **refuted**: a demolishing sibling counts as an active exit until
  it disconnects (§5).
- Clause 2 is **not** the C42 shape: `hub.units` has no raw writer. A positive count is colonists who
  really carry holder = hub, including off-hub carriers if S4 holds.
- Clause 4 is **confirmed and located**: the marker is cleared only at `Passage.lua:1235`.
- The standing causes are rescue waiters and `Stranded` colonists on the hub, which the access defect
  (S1) produces, and corpses for 8 h.
- It only bites the **last** exit. C99's reporter replacing a dome would hit it when the hub's final
  passage is salvaged.

**C109 (stand-still loop near home).** *Confirms, and qualifies it for hubs.*
- C109 is right that `HasLocalAccess` has community and passage routes. For a colonist on or near a
  hub, **those routes also reduce to centre distances**. Near a radius-19 dome, access fails and the
  rescue chain (S1) runs **instead of** C109's loop. That is exactly C109's own "vacuous if" condition.
- C109's loop applies to hubs whose access passes, meaning small domes, where
  `IsInWalkingDist` through the cheap tunnel should also pass.
- *Adds:* `MigrateStep` / `TransportByFoot` ignored hops can supply the `dome_enter_fails > 0`
  precondition on a hub (§6).
- C109's note that a valid `passage_hub` suppresses the timer is correct, and §4 extends it: **no
  exit path clears the marker**.

**C111 (status names own dome).** *Confirms.* The hub-triggered rescue ride home
(`ColonistTransport.lua:464-471` with `home = self.dome`) is a large source of "Moving to a new Dome:
<home>" in the reporter's layout. That status is the 12 "rides to their OWN home dome".

**F62 / F79 (services and trains across passages).** *Confirms.* `ConnectDomeToHub` pairs every hub
dome (`Passage.lua:1593-1601`), so services between hub spokes are one cluster hop, and no train path
is involved. *Adds:* every cross-hub service or work trip is a traversal that exposes the colonist to
S1 and S2 when an interrupt lands. The more of a colony's services sit across hubs, the more often S1
fires.

---

## 8. Suspects, ranked by player harm

**S1 · Centre-measured local access makes a colonist on or near a large dome's hub or passage
"unable to reach home", and books a shuttle rescue ride or `Stranded` instead of the walk the passage
provides.** SOURCE-VERIFIED.
- Lines: `ColonistTransport.lua:19-28, 260-268, 282, 293-299, 461-483`; `Workforce.lua:134`;
  `Dome.lua:2349-2351`.
- **Help-text contradiction.** `DefaultOutsideWorkplacesRadius` is documented as "Colonists search
  this far (in hexes) **outside their Dome**" (`__const.lua:1944-1949`), but it is measured from the
  dome **centre** (`Workforce.lua:134`, `ColonistTransport.lua:27, 299`). For radius 19 the
  "outside" band is about one hex.
- **Trigger:** interrupt a colonist on a Brussels-side hub or in a Brussels-side passage (fire it,
  switch off its work dome).
- **Falsifying control:** the same interrupt on a hub at the shell of a small dome must **not** book
  a ride. On Brussels' hub, `c:HasLocalAccess(c.dome)` must be false and `c.transport_task.dest_dome == c.dome`.
- **Hookable:** `Colonist.HasLocalAccess` (method); globals `IsUnitInDomeRange`,
  `IsBuildingInDomeRange`; `Dome.GetOutsideWorkplacesDist`. `HasAccessViaCommunity` and
  `IsDestinationInCommunityRange` are **file-local and not patchable**, so a fix wraps
  `HasLocalAccess`, for example by granting access when the colonist is on a hub or in a passage
  whose `dome_network` contains the destination's dome.

**S2 · An interrupt during a passage walk books the rescue pickup at the in-passage position, which
resolves to ground beside the tube. A colonist that finishes the walk inside its dome then walks out
through a dome door to wait there, with the oxygen timer running.** Rescue booking is
SOURCE-VERIFIED; the door route and the death are HYPOTHESIS, because the pathfinder's choice
between the door and the tunnel was not traced.
- Lines: `Unit.lua:860-878`; CommandObject.lua:363-368 (deferral); `LRTransport.lua:106-111`;
  `Colonist.lua:3973-4006`; `Dome_Entrance.lua:71`; `Colonist.lua:4901-4905`.
- **Trigger:** fire a worker while it is inside a Brussels-side passage heading home.
- **Falsifying control:** `transport_task.source_landing_site[1]` lies on a passage hex, and after
  arrival the colonist leaves Brussels to wait outside, with `outside_start` set and `passage_hub` nil.
- **Hookable:** `Colonist.SetCommand`, `CreateColonistTransportTask` (global) and `Colonist.Transport`
  can re-anchor or cancel the pickup.

**S3 · `passage_hub` is cleared only at a dome-side passage exit.** SOURCE-VERIFIED (2 writers).
- Lines: `Passage.lua:1228, 1235`; readers at `Unit.lua:469`, `Colonist.lua:1281, 2965`,
  `BuildingWayPoints.lua:538, 546`, `Passage.lua:1150`.
- **Effects:** a dumped colonist, and any colonist that leaves a hub by foot, shuttle or death, keeps
  the marker indefinitely. It is then immune to the oxygen timer and to disasters anywhere, keeps
  C99's clause 4 true near the hub, and contradicts `IsInSafeAtmosphere`.
- **Trigger:** any dump, then the colonist walks to open ground.
- **Falsifying control:** `c.passage_hub` is still valid with `c.outside_start == false` while the
  colonist stands outside, well away from the hub.
- **Hookable:** `Unit.UpdateOutside`, `Colonist.StopMoving`, `WaypointsObj.OnExitUnit` (methods). A
  fix must avoid starting the timer on a colonist who really is on the hub.

**S4 · holder = hub is carried off the hub.** HYPOTHESIS: it depends on the hub's walkable surface
joining terrain passability, which the field line "leaving a hub for its pickup spot" supports.
- **Mechanism:** tunnels are near-free (`Passage.lua:1733-1734`). If the hub surface joins the
  terrain, Gotos to outside points near a hub route through passage and hub and then walk off with
  holder = hub.
- **Consequences:**
  - `hub.units` counts them anywhere on the map;
  - they are sheltered outside;
  - `HasLocalAccess` and `GetStartingPoint` use the **hub's** position;
  - a later dump walks them **back** to the hub entrance;
  - shuttle pickup and drop never clear the holder (`ShuttleHub.lua:686-735, 880-895`), so a rescued
    colonist lands at home still "in the hub" and re-books a rescue;
  - hub demolish teleports them back.
- **Trigger:** a work or pickup target just outside a hub.
- **Falsifying control:** every `u` in `hub.units` has `u:GetDist2D(hub) <= hub:GetRadius()`.
- **Hookable:** `PassageBase.TraverseTunnel` (full method replacement, since the destructor closure is
  internal) or a `Colonist.StopMoving` / `Movable` hook that drops holder = hub when the colonist
  stands off the hub's hexes.

**S5 · Salvaging a hub passage that still has other exits disconnects it while colonists are inside.**
SOURCE-VERIFIED.
- Lines: `Passage.lua:1134-1138, 1181, 1404, 710, 1224, 1234`.
- **Effects:** traversers bound for the hub read `is_pf_tunnel = nil` and arrive **outside**: no
  holder, no marker, invisible to C99's guard. They also leave stale `element.units` entries, which
  the element deletion moments later turns into teleports back into the passage and a forced Idle
  (`Holder.lua:11-25`, `Unit.lua:288-305`), with asserts.
- **Trigger:** salvage one of two hub passages during shift traffic.
- **Falsifying control:** colonists arriving on the hub right after the disconnect have
  `passage_hub == nil`.
- **Hookable:** `PassageBase.OnDemolish` (wait on `traversing_colonists` **before** `DisconnectDomes`)
  or `PassageBase.TraverseTunnel`.

**S6 · C42 dome-side stale holder entry.** SOURCE-VERIFIED at `Passage.lua:1234`.
- **Trigger:** any dome↔dome passage traversal, then demolish that passage.
- **Control:** count `el.units` entries with `u.holder ~= el` after traffic, taken within the session.
- **Hookable:** `PassageBase.TraverseTunnel` (replacement) or `PassageGridElement:Done` (validate
  `units` before `Building.Done`).

**S7 · C99 permanence.** SOURCE-VERIFIED for the loop and clause 4. The cause is S1 + S3, via rescue
or stranded waiters and corpses near the last hub exit.
- **Trigger:** salvage a hub's last passage while a marked colonist stands within 2 × radius.
- **Control:** `MapHasAny` with the clause-4 filter returns true, and the colonist's command is
  `Transport` or `Stranded`.
- **Hookable:** `PassageBase.WouldStrandHubColonists`. For example, exclude dead colonists and those
  not on hub hexes, and clear stale markers first.

**S8 · Ignored hop results in `MigrateStep` and `TransportByFoot` can leave a colonist on a hub with
`dome_enter_fails > 0`, feeding `Abandoned` (C109) or S1.** SOURCE-VERIFIED for the ignoring
(`Colonist.lua:2204-2209, 3843-3848`); the reach is HYPOTHESIS.
- **Trigger:** break a passage while a migrant walks the network.
- **Control:** `dome_enter_fails` rises while `command == "MigrateStep"`.
- **Hookable:** `Colonist.MigrateStep`, `Colonist.TransportByFoot` (methods; full-body replacement).

**S9 · A throw inside the traversal destructor strands the entry in `traversing_colonists` for good.**
HYPOTHESIS. The destructor runs under `sprocall`, and the only cleanup is a one-time save fixup. A
throw leaves C99's clauses 1 and 3 and `OnDemolish`'s second wait (:1182) true forever.
- **Trigger:** delete a colonist mid-traversal.
- **Control:** `#p.traversing_colonists > 0` with no valid member.
- **Hookable:** `WouldStrandHubColonists` / `OnDemolish` (validate the list).

**S10 · `IsInSafeAtmosphere` is false on a hub while the marker makes the colonist oxygen-safe.**
SOURCE-VERIFIED (`ColonistTransport.lua:836-842, 909-914` vs `Unit.lua:469`). `Stranded` may walk a
safe colonist to a station through open ground. Low harm. Hookable: `Colonist.IsInSafeAtmosphere`.

**S11 · A dome whose only passage goes to an otherwise empty hub may pass `Dome:CanDemolish`**
(`Dome.lua:1791-1793`), which ignores `connected_passages`. That would leave `hub_domes` and the
passage pointing at a dead dome. HYPOTHESIS: the `labels.Building` membership of passage elements was
not traced. Hookable: `Dome.CanDemolish`.

**S12 · A shuttle drop at a radius-19 dome's own pad may fail the 20-hex centre test, so the
colonist re-books a rescue home from outside its own dome.** HYPOTHESIS, borderline. `FindDropPos`
excludes dome hexes (`ShuttleHub.lua:647-682`), so the drop is at distance 20 or more. Control:
`HasLocalAccess(home)` evaluated at the drop point.

Ranking by harm: **S1 > S2 > S7 (C99, progression) > S4 > S5 > S3 > S8 > S6 > S9 > S12 > S10 > S11.**
S3 alone protects from oxygen but causes S7. S1 and S2 are the death route; S2's death link is still
a hypothesis.

---

## 9. The field symptom

**Main chain.** Brussels has radius 19; the hub is 24-28 hexes from its centre; shuttles exist.
Lines are 1.1.1.
1. A mass interrupt hits colonists crossing Brussels' side. Candidate sources: firing or reassignment
   (`Workplace.lua:480`, `Colonist.lua:1756`), a work dome switched off (`Dome.lua:1905-1935`, new),
   or a cluster change on a passage disconnect (`Passage.lua:1419-1426`).
2. Colonists mid-passage finish the walk under deferral (CommandObject.lua:363-368). Those on the hub
   stop there with holder = hub and marker = hub (§3).
3. `SetCommand("Idle")` runs the wrapper. `HasLocalAccess(home)` is false because the hub or element
   is 24-28 from Brussels' centre and Brussels is the nearest community (`ColonistTransport.lua:282,
   287-299`). `CreateColonistTransportTask(self,false,home)` books a pickup at the colonist's own
   position (`LRTransport.lua:111`), and the wrapper issues `Transport` home (`ColonistTransport.lua:461-471`).
   **This is "twelve colonists at once in a rescue ride to their own home dome".**
4. `Transport` dumps each one (`Colonist.lua:3974`; `Unit.lua:419-466`; `BuildingWayPoints.lua:541-547`)
   onto the hub surface and walks it to the pickup, which is on the hub for a hub-booked ride. **This
   is "standing on a hub surface with holder nil, passage_hub set, 24-28 hexes out, HasLocalAccess
   false".**
5. It waits up to a sol (`_GameConst.lua:143`), then Idle re-books (§4). Meanwhile C99's clause 4
   holds for that hub.
6. **Hub 2692 at 53-59 units.** Live crossings of the busiest Brussels hub hold holder = hub from the
   tunnel exit to the next tunnel entry (`Passage.lua:1227`). S4 carriers would add to that. The reading
   finds no leak of `hub.units` entries.

**The one measurement this chain does not reproduce.** A colonist that *left a hub* with its marker
set cannot start the oxygen timer (`Unit.lua:469`, `Colonist.lua:2965`, `BuildingWayPoints.lua:546`).
**So the watched colonist's 71 s of 120 s means its marker was nil.** Candidates:
- **(a) S2:** its booking was made mid-passage while inbound to Brussels. It reached Brussels (marker
  cleared, :1235), and its pickup beside the tube was reached through a Brussels door
  (`Dome_Entrance.lua:71`). The path may have crossed the hub surface.
- **(b) S5:** it arrived on the hub through a passage being salvaged, with the marker never set.
- **(c)** it walked onto the hub surface from terrain, not through a tunnel (S4's passability premise).
- **(d)** the Passage Network mod run: its code was not read.

A single read of `c.passage_hub`, `c.outside_start`, `c.transport_task.source_landing_site[1]` and
`c.command` on such a colonist discriminates (a)-(d). **Colonists die** only on routes (a)-(c).
Marked hub waiters are oxygen-safe. Their harm is lost work, service and rest, the rescue loop, and
C99.

**Alternative chain for the count and the rides: S4 (HYPOTHESIS).** Rescue waiters reach their
pickup through a tunnel and so still hold holder = hub off the hub. They ride home still "in the hub",
and the next Idle measures from the hub and re-books. This fits the high `hub.units` on one hub and
repeated home rides. Its falsifier is in S4.

---

## 10. Commands run, and what was not done

All `rg` runs were on archived trees. Output was read in full unless stated.
1. `cat -n PassageHub.lua` and `diff` against 1.1.0: prints SAME (0 changed lines).
2. `rg -n --no-ignore "passage_hub|hub_domes|traversing_colonists|draining_passages|PassageHub|..."`
   over the 1.1.1 `Src` (full hit list read; reconciled in §2).
3. `rg -n --no-ignore "passage_hub\s*=[^=]" Lua CommonLua` (1.1.1): **2** assignments
   (`Passage.lua:1228`, `:1235`) plus the class default `Unit.lua:18`.
   Presence side: `rg -c "passage_hub"`, which returns `BuildingWayPoints 2`, `Passage 5`,
   `Colonist 2`, `Unit 2` and `PassageHub.generated 1`. The last is the icon string
   `passage_hub.png`, not the field, so there are 11 field mentions. They reconcile: 2 writes +
   1 default + 8 reads/comments (`BuildingWayPoints:538, 546`; `Passage:1147 (comment), 1150, 1231`;
   `Colonist:1281, 2965`; `Unit:469`).
4. `rg -n "function [\w\.:]*(SetHolder|ExitHolder|InterruptUnitsInHolder|KickFromBuilding|KickUnitsFromHolder|PopAndCallDestructor|PushDestructor)\b"`,
   then `rg -n "InterruptUnitsInHolder|KickUnitsFromHolder"` (callers read).
5. `rg -n "\"Holder\""`: shows that `BaseBuilding` has `Holder` as a parent, so a hub is a Holder.
6. `rg -n --no-ignore "\.holder\s*=[^=]" Lua CommonLua`: **6** hits. `Passage.lua:1234` and
   `Unit.lua:817` (inside `SetHolderOnMap`) are the unit-holder writes that matter. `Colonist.lua:5601`
   clears before `SetHolder`. `Train.lua:376` is the train's own holder. `SurfaceDeposit.lua:154, 426`
   are unrelated. **None of the six assigns a hub.**
7. `for f in ...; diff 1.1.0/$f 1.1.1/$f | grep -c '^[<>]'` for 9 files (counts in §6). Then the full
   `diff` of Passage, ColonistTransport, Unit, BuildingWayPoints and GridConstruction, and
   `diff -u -F '^function'` hunk lists for Colonist.lua and Dome.lua, with the migration, VisitService,
   CanReachDomeForBuilding and OnSetUIWorking hunks read.
8. `rg -n "^function (PassageBase:...)"` on both builds: the one-line offset (1.1.0 +1 = 1.1.1) for
   everything after `Passage.lua:1008`.
9. Direct `sed -n` reads: `Passage.lua` 240-280, 448-470, 655-720, 840-900, 1000-1340, 1340-1470,
   1540-1790, 2615-2876; `ColonistTransport.lua` 1-60, 240-560, 700-944; `Colonist.lua` 1270-1500,
   1905-1930, 2155-2216, 2411-2600, 2655-2675, 2955-2972, 3180-3240, 3820-4030; `Unit.lua` 1-60,
   262-520, 668-710, 780-850, 860-925, 1196-1340; `Holder.lua` (whole); `BuildingWayPoints.lua`
   149-300, 480-560; `Dome.lua` 92-173, 525-540, 680-760, 1139-1150, 1605-1660, 1791-1870,
   1905-1935, 2121-2133, 2349-2363, 299-319; `CommandObject.lua` 1-470; `Movable.lua` 400-480;
   `Demolishable.lua` 30-160; `ShuttleHub.lua` 410-419, 655-735, 790-990; `LRTransport.lua` 86-124;
   `Workplace.lua` 473-483, 962-974, 1160-1180; `Dome_Entrance.lua` 60-75; `Community.lua` 460-480;
   `Tunnel.lua` 85-100, 205-245; `__const.lua` 1935-1955, 1753-1758; `_GameConst.lua:143`.
10. Library entries C42, C99, C109, C111, F62 and F79, read in full, not edited.
11. Pack code: `rg "passage_hub|ShuttleHubOffAvailable|IsLRTransportAvailable" -g *.lua` over the
    repo (HEAD `9c34d38`), a read of `Code/Fix_ShuttleHubOffAvailable.lua`, and
    `rg "outside_start|UpdateOutside|SetOutsideEffects|TraverseTunnel|WouldStrandHubColonists|holder" Code`.
    **No pack module touches `passage_hub`, traversal or hub demolish.**

**Not done.**
- No game run, no save read, no measurement. Every figure above is a source line or a grep count.
- The following were not traced:
  - the hub entity's waypoint chains (binary entity data);
  - whether the hub's walkable surface joins terrain passability (S4's premise);
  - the engine behaviour of `FindNearestObject`, `HexAxialDistance`, `MapHasAny` on detached units,
    and `GetPassablePointNearby` near passage tubes;
  - `GetNextMigrationLeg` / `BuildReachableGraph` from a hub (whether `Stranded` walks home);
  - `labels.Building` membership of passage elements (S11);
  - `FindDropPos` ring distances (S12);
  - `Colonist:Roam` and `Rest` from a hub;
  - the `StatusEffect_Stranded` health effect;
  - `UseElevator` beyond its `ExitHolder` (`Unit.lua:1051`).
- The Passage Network mod's code was not read.
- No git write, no doccheck, and nothing edited under `B:\Dev\SMR\SMR-BugFixPack`.
