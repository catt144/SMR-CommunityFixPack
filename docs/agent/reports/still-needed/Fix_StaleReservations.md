# F58 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Captured inputs:
`CENSUS.json`, game **1.1.0.403908**. The module and site row still match the
captured byte hashes. Final settled registry evidence supersedes raw boot
status parsing; `StaleReservations` is active at registry-log line 238.

Disagreements:

- The narrowed site row still presents **colonists who set off on foot** as a
  demonstrated residual that F58 covers (`fix-list.md:115-116`). The ordinary
  dome-changing foot path calls `SetDome(dest_dome)` before walking;
  `SetDome` immediately calls `UpdateResidence`, which adopts the reservation
  as an actual residence; `AddResident` cancels the reservation. Reading only
  `TransportByFootDtor` misses this earlier cleanup. This directly weakens that
  named residual; unusual blocked or interrupted paths remain unmeasured.
- The row's **a reservation whose journey can no longer complete** promise
  (`fix-list.md:112`) overstates the module's test. The sweep checks invalid,
  desynchronized, dying or old holders; its age branch has no journey-state or
  abandonment test. An old non-expedition reservation is expired whether or
  not its journey could eventually complete. Committed-task exemption from one
  vanilla timeout is source-proven, but organic permanent limbo and F58's
  practical benefit remain unproven after the other cleanup paths are counted.
- The card has a dedicated F58 headline, **A dome sat half empty and still
  refused to house anyone**, mapping to `fix-list.md:105`. Its connection to
  the original defect is correct; whether that symptom is still produced and
  cured by the remaining 1.1.0 residuals is unknown. The routine foot path cannot
  supply that evidence, and the committed permanent-hold case is unverified.
  This is an evidence limit, not proof that the headline is false or that
  vanilla fixed every residual.

Recommend **KEEP-BUT-FIX-CLAIM**, conditional on the owner's existing keep ruling:
the modified reservation list still feeds live admission and assignment, and a
global vanilla resolution of all residual stale states has not been established.
Describe the daily stale/age cleanup and expedition age exemption precisely;
do not present foot journeys or forever-held committed rides as proven current
defects. The owner should adjudicate whether the remaining unverified benefit
justifies keeping the module. This report does not establish a new filed defect
or a retirement clearance.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_StaleReservations.lua | F58 | yes: direct settled registry active at line 238; no colony sweep or cure measured | yes: GetFreeSpace and Community admission still consume reservations; assignment, Homeless labeling and expedition return still read reservation state; organic residual benefit unknown | partial: ordinary-wait expiry caveat is true; foot residual ignores immediate reservation conversion; sweep does not test whether a journey can complete; committed permanent limbo unverified | unknown: dedicated half-empty-dome F58 headline maps to fix-list.md:105; current residual production/cure of that symptom is unverified; fallen-vacant-bed headline is separately F59 | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Residence.lua:233; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Community.lua:412; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:3546; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:449 | SOURCE: state consumers and counted cleanup; surviving organic stale-lifetime defect remains INFERRED | organic stuck committed ride; foot interruption retaining a reservation; MainCity daily sweep; fresh expedition preservation; invalid/desynchronized holder controls; non-MainCity cleanup; fresh save/load/uninstall |

Primary evidence (game citations are read-only **1.1.0.403908/Src**):

- **Reservation writers remain shipped and reachable.**
  `Lua/Buildings/Residence.lua:290-304` writes the array, hash membership and
  `unit.reserved_residence`; `Lua/Buildings/Dome.lua:3361-3369` delegates to it.
  Emigration writes at `Lua/Units/Colonist.lua:1919`, `:1942`, `:1971`; train
  migration and stranded-foot fallback write at
  `Lua/Units/ColonistTransport.lua:795`, `:878`. Applicant/returnee paths also
  write through the dome at `Lua/CargoTransporterNew.lua:1006`, `:1051`, `:1092`
  and `Lua/Buildings/RocketBase.lua:1982`, `:2073`, `:2109`; rocket-departure
  stopover writes at `Lua/UniversalRocket.lua:2260`. Manual cross-dome Set
  Residence uses `Lua/Buildings/Residence.lua:340-351`. The sibling stand-alone
  habitat implementation explicitly calls `Residence.ReserveResidence` at
  `Lua/Buildings/MicroGHabitat.lua:85-87`, so this method path did not disappear.
- **Live consumers still make reservation release meaningful.**
  `Lua/Buildings/Residence.lua:232-234` subtracts reserved slots;
  `Lua/Buildings/Community.lua:366-383`, `:402-417` use that result for current
  admission; and `Lua/Buildings/Residence.lua:283-287` uses it for reservation
  eligibility. `Lua/Units/Colonist.lua:2921-2926` reads the colonist's held home,
  and `:2891-2894` suppresses adding a reserved homeless colonist to the
  Homeless labels. `Lua/Buildings/Residence.lua:408-413` still shows capacity
  and actual residents, not reservations. Unlike F60, the modified quantity
  has not been bypassed by the current admission gate.
- **The vanilla cancellation path remains the right state mutation.**
  `Lua/Buildings/Residence.lua:385-399` removes array/hash membership, clears
  the colonist's reservation and expedition-hold pointers, and resets dome
  free-space cache. Successful arrival/reassignment reaches it through
  `Residence:AddResident` at `:110`, called by
  `Lua/Units/Colonist.lua:2907-2912`. Capacity changes and closing beds also
  cancel at `Lua/Buildings/Residence.lua:137`, `:262`; destruction drops all
  residence holds and expedition pointers at `:90-100`. The load fixup at
  `:634-640` only removes holds in the colonist's already occupied residence;
  it is not a generic age sweep.
- **Ordinary waits now have vanilla cleanup.**
  `Lua/_GameConst.lua:143-145` sets one-sol pickup wait/task expiry and hourly
  checks. `Lua/LRTransport.lua:43-59`, `:125-130` tests uncommitted-task expiry;
  `Lua/LRManager.lua:50-62` releases the matching request through
  `Lua/Units/Colonist.lua:2036-2038`, whose first action cancels residence and
  work holds. Pickup waiting is bounded at `:3694-3701`; its destructor
  `WaitTransport` cancels failed-emigration reservations at `:3640-3654`.
- **The foot residual is not established by its destructor.**
  `Lua/Units/Colonist.lua:1917-1927` clears the transport request, reserves the
  destination residence and starts `TransportByFoot`. That command immediately
  calls `SetDome(dest_dome)` at `:3546`. When the assigned dome changes,
  `SetDome` calls `UpdateResidence` at `:449`; `UpdateResidence` selects the
  held home at `:2921-2926`; and `Residence:AddResident` cancels the reservation
  at `Lua/Buildings/Residence.lua:110`. `CanChangeCommand` at
  `Lua/Units/Colonist.lua:2685-2687` does not exclude an ordinary foot command.
  The destructor at `:3529-3539` has no local cancellation, but the ordinary
  new-dome walk has already converted the hold. Cross-map failure also switches
  to `Abandoned` at `:3569-3572`; that command clears requests at `:1448` and
  explicitly cancels holds after failed re-entry at `:1480-1482`.
- **Committed rides are exempt from expiry, with additional cleanup counted.**
  `Lua/LRTransport.lua:44-45` exempts committed tasks, and
  `Lua/LRManager.lua:55` skips command `Transport`. These local exemptions do
  not prove a forever hold: `Lua/Buildings/ShuttleHub.lua:751-753` clears an
  invalid-destination request; `:761-784` installs a destructor that unloads
  the passenger and clears shuttle commitment; `:904-907` invokes it on failed
  delivery flight. `LeaveColonist` detaches and wakes the colonist at
  `:724-729`. `Lua/Units/Colonist.lua:3637-3654` then waits only while genuinely
  transported and cancels failed-emigration holds. Ordinary `Idle` invokes
  `UpdateResidence` at `:2344`, `:2357-2358`, and death/map-transfer cleanup
  calls `ClearTransportRequest` at `:1288`, `:389`. A still-running committed
  ride that never reaches these exits remains an inferred possibility, not a
  reproduced or globally traced lifetime defect.
- **The expedition age exemption matches a legitimate long-lived consumer.**
  `Lua/Units/Colonist.lua:5027-5030` records the expedition home;
  `:5003-5005` retakes it through the wrapped method after disappearing.
  `Lua/Units/Unit.lua:1222-1225` detaches the unit from the map and marks it
  disappeared rather than deleting it. Returning crew prefer the held dome
  via `Lua/Units/Colonist.lua:5046-5053`; `:5076-5082` retains a matching
  destination hold and cancels an unreachable one. F58 correctly exempts this
  state from its age branch because cancellation would also erase
  `expedition_residence` (`Lua/Buildings/Residence.lua:394`). Invalid,
  desynchronized and dying branches still precede the exemption. The reused
  lock duration is 3,600,000 ms at `Lua/__const.lua:171-176`.

F58's wrapper still stamps every successful `Residence:ReserveResidence` call;
its additive daily sweep still reads that stamp and iterates only
`MainCity.labels.Residence`. That loop's invalid/desync/dying and age tests are
independent of transport-command completion. A reservation lacking a stamp gets
a grace period; an expedition hold skips age expiry. Those code paths have not
been executed by the menu-only measurement.

Runtime installation: direct settled registry log
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:238`
reports active; the prior archived boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:93`.
No F58 release/heal message appears. Captured bodycheck pin success does not
cover the current cleanup chains independently traced above.

What I did NOT check, by name:

- Organic committed-shuttle limbo retaining a residence beyond all cleanup.
- Interrupted/blocked foot journeys retaining a reservation after `SetDome`.
- Fresh colony execution of the MainCity daily sweep or TestKit F58 probe.
- Fresh long-expedition preservation and crew residence recovery in play.
- Invalid, dying, desynchronized or old-but-still-viable holder runtime controls.
- Non-MainCity residence sweep, new-map/DLC label coverage or map unloading.
- Save/load/uninstall behavior and fresh 1.0.7 behavior.
- F59's later repair in play, portal rendering or whole-card surface counts.
- Any other module or fenced prelaunch sweep verdict reports.
