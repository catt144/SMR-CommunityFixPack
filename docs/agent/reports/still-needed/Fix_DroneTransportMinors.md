# F57 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Game **1.1.0.403908**;
captured inputs and final direct registry in `CENSUS.json`. Recommendation:
**KEEP** the remaining F57(a) pre-wrapper as R3 protection. Current shipped
rocket data still hide the defective key clear, and all three Lua consumer
paths remain live, including both native request-matcher siblings.

Disagreements first: no current implementation or public-row contradiction
found. The module's opening historical summary still says two items are fixed;
the later retirement note and actual implementation correctly leave only (a).
The site row's perpetual drone-work symptom is a conditional prediction from
the retained restrictor, not a fresh 1.1.0 gameplay observation. Native matcher
internals are absent from the Lua archive, so this review establishes their
live input paths rather than independently proving how long a departed or
destroyed rocket's request influences the native matcher. The shipped-data
latency claim is independently rechecked below, not inherited from the header.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_DroneTransportMinors.lua | F57(a); F57(b) already retired; F57(c) deliberately excluded | yes: final direct registry active at line 259; target method and defective key clear remain | yes: Drone delivery reads the resource key; FindDemandRequest and FindTask forward this table to native matchers from live drone callers; historical field cleanup has no ordinary shipped-data carrier | yes: conditional stale-key mechanism and current shipped Fuel latency; perpetual gameplay consequence remains inferred and unexercised | yes: no dedicated F57 headline; this module supports the shared three invisible repairs paragraph as one contributor; total count checked by coordinator | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/DroneControl.lua:674; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/DroneControl.lua:693; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/_TaskRequest.lua:59; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/_TaskRequest.lua:77; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/UniversalRocket.lua:47 | SOURCE | fresh non-Fuel rocket control; native matcher internals; fresh departure or destruction cure; historical field carrier control; save/load/uninstall; third-party content; excluded (b)/(c) re-audit; whole-card count |

Primary evidence (read-only **1.1.0.403908/Src**):

- **Current target still disagrees with its data key:**
  `Lua/Buildings/DroneControl.lua:672-698` clears only `r_t.Fuel` at `:674`.
  Legacy `RocketBase` requests write literal Fuel at `:682` and `:687`, but
  `UniversalRocketBase` reads `demand[r.FuelResource]` at `:691` and writes that
  variable key at `:693`. Removing the last non-Fuel rocket from
  `serviced_rockets` therefore does not clear its previously written key.
  Current F57(a) clears every key of the rocket-flag table before delegating;
  it does not clear the separate waste-rock-flag table.
- **Initialization, writer and caller remain current:**
  `Lua/Buildings/DroneControl.lua:196-199` initializes an empty rocket table;
  `:213` reaches it from `DroneControl:Init`. A full Lua search for
  `restrictor_tables` finds no other live writer to the rocket resource map.
  The separate dump map is initialized at `:202-205` and updated at `:650-669`.
  `:635-637` marks the rocket update pending; `RestrictorThreadBody` invokes
  `UpdateRocketsInternal` at `:624-625` before its wait at `:631`.
  Add and remove operations schedule that update at `:711` and `:715-716`.
  The pre-clear and original rebuild contain no Lua yield between them.
- **Real rocket departure/disconnection still reaches removal:**
  `Lua/UniversalRocket.lua:609` invokes `InterruptIncomingDronesAndDisconnect`
  during takeoff. That function disconnects at `:1854`; inherited
  `CommonLua/TaskRequest.lua:214-218` calls each `RemoveCommandCenter`.
  `UniversalRocketBase:RemoveCommandCenter` at
  `Lua/UniversalRocket.lua:2154-2156` removes the rocket from each center;
  `DroneControl:RemoveRocket` then removes membership and schedules rebuilding
  at `Lua/Buildings/DroneControl.lua:715-716`. These calls still fail to remove
  a non-Fuel resource key in unpatched vanilla. Destroyed-request cleanup also
  changes request sources (`CommonLua/TaskRequest.lua:80-84`); its effect inside
  the native matcher was not independently observed here.
- **Consumer 1, explicit resource-key read:**
  `Lua/Units/Drone.lua:1411-1415` looks up the rocket restrictor map and compares
  `rrt[resource]` with the selected demand request, scheduling a rocket update
  when its target amount reaches zero. The pre-wrapper preserves this table's
  identity, clears stale keys and lets vanilla rebuild the selected request.
- **Both sibling native consumer entry points remain live:**
  `Lua/_TaskRequest.lua:55-61` forwards `self.restrictor_tables` into
  `Request_FindDemand_C` at `:59`; `:73-78` forwards it into
  `Request_FindTask_C` at `:77`. Ordinary task acquisition calls `FindTask` at
  `Lua/Units/Drone.lua:593-609`, specifically `:602`. Demand improvement calls
  `FindDemandRequest` at `:843`; delivery without an existing demand request
  calls it at `:1383`. Both native calls receive the same table the fix changes;
  neither is an obsolete or editor-only sibling. Lua source does not expose
  the native matcher implementation.
- **Current presets still leave the repair latent:**
  `Lua/UniversalRocket.lua:47` declares the template property `FuelResource`
  with default `"Fuel"`. All six direct generated rocket classes inherit
  `UniversalRocketBase` at line 5 of
  `Lua/BuildingTemplate/UniversalRocket.generated.lua`,
  `UniversalDragonRocket.generated.lua`, `UniversalLanderRocket.generated.lua`,
  `UniversalZeusRocket.generated.lua`, `UniversalTradeRocket.generated.lua`, and
  `UniversalRefugeeRocket.generated.lua`. None overrides `FuelResource`.
  Their editable presets change `FuelResourceAmount` at line 4 of each
  corresponding `Data/BuildingTemplate/*.lua`, not the resource identifier.
  Exact-token searches of all `Data/**/*.lua`, `Dlc/**/*.lua`, and
  `Lua/BuildingTemplate/**/*.lua` find respectively one, zero and zero
  `FuelResource` occurrences. The one Data occurrence is a reader at
  `Data/FlightPolicyDef.lua:339`. A full `Src/**/*.lua` search finds the default
  declaration and readers, with no resource assignment or setter. Thus current
  ordinary shipped rockets select the same Fuel key that vanilla clears;
  the defect becomes observable when later data select another resource.
- **Historical field cleanup is conditional, not another visible repair:**
  the current module clears `SMRFixPack_rocket_fuel_key` if present, then
  delegates. The F57 entry's 2026-08-12 audit records that the superseded
  implementation wrote this field only for non-Fuel rockets. The current
  primary default/preset trace still excludes that carrier in ordinary shipped
  data. A constructed carrier or third-party rocket would be needed to test
  removal of an existing value; absence in an ordinary campaign is only a
  negative control, not a witnessed field-removal cure.

Public row `C:/Dev/SMR-CommunityMods/content/fix-list.md:597-603` correctly makes
the stale-key case conditional on a non-Fuel rocket and identifies current
Fuel data as its concealment. Its **never happened to anyone** claim is read
in the paragraph's shipped-game scope; this source review does not establish
third-party players' histories. The conditional permanent gameplay symptom
remains inferred from the persistent input table rather than newly witnessed.
The card has no dedicated F57 headline. Its **three repairs you cannot see at
all today** paragraph is supported by this module as one latent contributor;
the other contributors and aggregate count belong to the coordinator.

`HOTFIX_2_AUDIT.md:188-190` already records deletion of (b) and correct
whole-module decline behavior on a missing (a) prerequisite. This review does
not reopen that known retirement or the deliberately excluded (c).
Direct final registry
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:259`
reports active; the settled second boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:117`.
These establish installation, not a non-Fuel symptom or cure. No colony loaded
or suite ran for this review.

What I did NOT check, by name:

- Fresh non-Fuel rocket controls, departure/destruction symptom or cure.
- Native Request_FindDemand / Request_FindTask matcher internals.
- Constructed `SMRFixPack_rocket_fuel_key` carrier and removal control.
- Fresh DroneTransportMinors TestKit probe or `RunAll()`.
- Save/load/uninstall or fresh 1.0.7 execution.
- Third-party rockets, indirect external data edits, future patch/DLC presets.
- Re-audit of already retired F57(b) or deliberately excluded F57(c).
- Other modules, aggregate card count, fenced prelaunch sweep verdict reports.
