# C95 return-home and C102 safe fallback build

Build authorized by the consumed C95_RETURN_HOME_BUILD brief at `0da1256`.
Game fingerprint: Steam build 24995074, 1.1.0.403908 / executable 6a91a190.
No release or version edit is authorized by this work.

## Live work list

- DONE — Orientation/staleness: clean tree, pull current, scoped diff only C95 archive citation.
- DONE — Register HabitatExpeditionReturn; private selector input and housing-before-work hook.
- DONE — Extend ArrivalDeaths with C102's nearest safe fallback before reservation.
- DONE — Conditional HabitatExpeditionDraft; v11 archive verified byte-identical.
- DONE — Whole desk suites, pinned manifests, C83/F117 regressions and doccheck.
- DONE — Retail nearby/full A/B, corrected real draft and save/reload; C102 fixture lacks
  a live reachable alternative. Cold removal remains the owner's protected-folder step.
- DONE — Final evidence, entries, pending outbox, ck200 sitting and consumed brief/map row;
  this report lands with the scoped build commit. Remote verification is reported in the session close.

Probe sweep before live arming: `rg -n TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/`
had no hits at HEAD `0da1256`. Declared live payloads: `98_C95Build.lua` for receiver A/B,
then `98_C95Save.lua` for draft and save/reload, and `98_C102Return.lua` for the
dead-dome fixture check. All are disarmed; the final sweep has no hits and the TestKit
tree is clean. No prototype was armed. Save baseline and metadata backups:
`C:/Dev/SMR-C95BuildScratch/`.

## Design

`HabitatExpeditionReturn` adds only this colonist's valid reserved habitat to a private
candidate list, with the prototype's walking or verified same-map train route. It calls
the captured selector and preserves its return tuple. At a reserved habitat rejoin,
native UpdateResidence precedes the captured UpdateWorkplace. This also covers ordinary
migrants with that same reserved-habitat state, as the brief permits.

`HabitatExpeditionDraft` uses the return module's CanReturnHome predicate at the departure
rocket. If that module is inactive, it retains exclusion. Both automatic gather receivers
remain independently optional. All-habitat colonies whose homes have no admitted route
still cannot fill an automatic crew; the owner's shortage question remains open.
The occupied bed qualifies before boarding if the colonist is actually on that habitat's
resident list and the home remains suitable. Requiring spare reservation capacity at
that moment rejected a resident of a full habitat; the first live draft caught this and
the final predicate and extracted CanReserveResidence desk leg correct it.

C102 extends `ArrivalDeaths`, reusing `is_welcoming_arrival_dome`. Its synchronous selector
wrapper keeps a welcoming selected home; otherwise it selects the minimum measured
distance among welcoming reachable domes, irrespective of spare housing. This happens
before both receivers reserve a fallback residence. With none, vanilla's result survives
and a one-time log records the unruled case. This uses the existing ArrivalDeaths veto.

The v11 archive is `docs/archive/code/Fix_HabitatExpeditionDraft.v11-4ec3e32.lua.txt`.
Byte comparison against `git show 4ec3e32:Code/Fix_HabitatExpeditionDraft.lua` passed;
SHA-256 `064a5cb6cb6bf3917c7b02c831240605c339b0224e463c182792ead8b52c613d`.

## Route bounds and save safety

The bounded shuttle read is `ColonistTransport.lua:381-502`: the return destination gets
walking/train dispatch. The shuttle rescue branch at 460-477 targets `self.dome`, not
the expedition destination, and needs that dome. Boarding has cleared it. No shuttle
route is admitted by this repair.

The departure test is not a guarantee of the return location. `UniversalRocketBase:CmdWaitInOrbit`
(`UniversalRocket.lua:301-337`) automatically lands at its reserved site only in auto mode;
otherwise it waits for a landing order. `CmdLand(landing_site, from_ui)` accepts a supplied
site and adds it at 340-346. Return selection therefore repeats the route test at the
actual arrival origin; a changed site/route can cause safe fallback.

Layer 3 for new hooks: no new persistent state, game-time threads, saved callbacks or
command body copies. `python tools/blocking_analysis.py tools/c95_blocking_targets.json`
at HEAD `0da1256` reports clear for GetExpeditionReturnDome, UpdateWorkplace, UpdateResidence,
CanVisit, CanReserveResidence, IsSuitable, HasLifeSupport, CanAcceptNewColonists,
IsInWalkingDist, GetTransportRoute, GetDomesReachableByColonists, SetResidence,
GatherAvailableColonists and FilterColonistsByTrait. The initial prototype-target
recheck also covered CanChangeCommand and ChooseResidence. The source reads confirm UpdateResidence may refuse;
the repair does not force assignment. SetResidence does not call either update method,
so the ordering hook cannot recurse through it. Native dispatch and receivers own their
blocking travel; none is wrapped by the new module. The draft's temporary filter swap
retains its synchronous gather premise. Third-party yielding wrappers would invalidate it.

## Desk evidence

Commands at HEAD `0da1256` plus this build, Steam 24995074:

- `python tools/desk_c95_return_home.py`: 50/50 demands, individual members emitted.
- `python tools/desk_c95_habitat_draft.py`: whole suite passes, including conditional
  admission, inactive-return exclusion, both receivers and one-receiver-only preflight.
- `python tools/desk_c83_arrivals.py`: 12/12 demands; existing arrival behavior preserved.
- `python tools/desk_f117_argshape.py`: 11/11 demands, both source branches and UNKNOWN.
- `python -X utf8 tools/bodycheck.py --module HabitatExpedition --all` and the same with
  `--module ArrivalDeaths`: every declared pin and defect expression matches.
- `python tools/doccheck.py`: GREEN before live arming.

The return harness extracts the shipped selector, chooser, receiver, dispatcher and
housing bodies. Routing, score/space predicates and employment are explicit fixture
inputs; it does not simulate pathfinding or serialization. Pre-fix bodies are the harm
controls. C102's shipped chooser retains the dead fallback when live alternatives are
full; the wrapper chooses the nearest safe alternative. Non-habitat C95 delegation
preserves arguments and nil-bearing return tuples.

## Live evidence

All runs used retail Mars.exe, 1.1.0.403908 / 6a91a190, HEAD `0da1256` plus the
working build, speed 3, the same `hab test A` bytes copied to `C95BUILD.savegame.sav`,
and autosaves suspended before loading. The fixture has NaturalistHabitat(2692), full,
13 hexes from UniversalZeusRocket(1053). Dome 1076 is walkable (distance 27200);
1637 and 2535 are not (111948 and 131560). The C102 route census found no train
route from the pad to any of those domes. No subject was teleported or re-housed by
the harness; native boarding disappears the passenger as vanilla does.

| Leg / archived log | Result and limit |
|---|---|
| [Registered nearby/full](../../archive/logs/c95_build_home_Mars.exe-20260917-01.10.57-6a91a190.log) | `MODULE return=true`; original list omitted home, selector chose 2692. Resident 2000002122 physically entered it and retained it through the soak, with no workplace. Native LoadPassengers/UnloadPassengers; no mission. |
| [Module-absent control](../../archive/logs/c95_build_control_Mars.exe-20260917-01.12.28-6a91a190.log) | Only HabitatExpeditionReturn omitted from items/code list for this boot, then restored. `return=false`, C102 still active; selected nil, apartment 2733 in dome 1076 and MetalsExtractor job; timed out waiting for original home. Same driver and copy. |
| [First draft attempt](../../archive/logs/c95_build_draft_rejected_Mars.exe-20260917-01.15.05-6a91a190.log) | SKIP: no habitat resident selected. Exposed the occupied-bed predicate error described above, not accepted evidence for the final draft. |
| [Corrected draft/save/reload](../../archive/logs/c95_build_save_Mars.exe-20260917-01.17.28-6a91a190.log) | Real GatherAvailableColonists selected habitat residents 2000001502, 2000002097 and 2000002122 alongside ordinary residents 2000001472 and 2000002081. Native boarding/unloading of that crew, no flight. Subject 2000001502 saved mid-TransportByFoot, no holder, home 2692. Reload returned no error; `HOME_AFTER_RELOAD` records physical entry into 2692 with no workplace. |
| [C102 fixture check](../../archive/logs/c102_build_fixture_Mars.exe-20260917-01.18.43-6a91a190.log) | Ordinary resident boarded, then **only setup mutation: dome 1076 switched off**. `safety=1076 safe_count=0 selected=nil`; positive safe-alternative leg SKIPPED. No suffocation or safe physical arrival was tested. |

Save monitoring ran in real time and waited for the temporary game-time boarding and
unloading threads to finish before saving. Only native travel was in progress at the
save. `C95MID.savegame.sav` SHA-256:
`84691211e7aca7da7c37f3acde8b9d5134582bd8f028519638f0ee70de170ad0`.
The save/reload leg is same-process with the pack enabled; it is not removal evidence.

The baseline comparison command reads `C:/Dev/SMR-C95BuildScratch/save-inventory-before.json`
and hashes each named file under the owner save directory. It reconciled **37/37**
pre-existing `*.sav` members unchanged; new members are exactly `C95BUILD.savegame.sav`
and `C95MID.savegame.sav`. No owner save was overwritten.

`python -X utf8 tools/logscan.py <the five archived log paths in the table>` reports
5 logs, 0 error-shaped lines. This is a Lua-log result, not an absence of every error:
the rejected draft process displayed a native shutdown assertion in
`A:\spark-release\HSL\external\tlsf\tlsf.c:764`,
`block_is_free(prev) & "prev block is not free though marked as such"`.
UI Automation read the dialog from that test's process 77180; it was stopped after
its DONE/SKIP lines. Cause unresolved; not attributed to this Lua change. The rerun
resumed before quit and exited normally, but that does not establish causation.
Startup Braze DNS errors are also present and outside logscan's gameplay-error filter.
The Opt-In Pack was present; ResidencyControl, CohortHousing and NoHomeless were
inactive in every log. No TestKit probe-suite tally is claimed by these driver legs.

## Owner sitting: remaining release gates

**No upload until these are closed or the owner explicitly changes the gates.**
No new code here has an attended verdict. Start with a copy and the new pack enabled.
For the ordinary UI expedition, select an inhabited habitat while paused and run:

```lua
SMRC95Home=SelectedObj; SMRC95Crew=table.icopy(SMRC95Home.colonists); print("C95 START",BuildVersion,SMRFixPack.IsActive("HabitatExpeditionReturn"),SMRC95Home.handle,#SMRC95Crew); for _,c in ipairs(SMRC95Crew) do print("C95 RESIDENT",c.handle,c.command,c.residence and c.residence.handle) end
```

First-screen witness: active repair, chosen habitat and each original resident printed.
Send a normal crewed expedition through the UI. On departure and after return, run:

```lua
for _,c in ipairs(SMRC95Crew) do print("C95 WITNESS",c.handle,c.command,c.expedition_residence and c.expedition_residence.handle,c.residence and c.residence.handle,c.holder and c.holder.handle,c.workplace and c.workplace.class) end
```

At least one resident must actually be aboard, and later physically inside the same
habitat with the original residence and no new dome job. If none was drafted, that
sitting does not cover the case. The harness's controlled unload is not a flown mission.

For rail, **provision** a colony with an inhabited distant habitat and working passenger
stations at the habitat and pad. The present fixture has no such route. Reuse the
habitat line above, select the rocket, and run this before sending the UI expedition:

```lua
local r=SelectedObj; local a,b=GetTransportRoute(r,SMRC95Home,true,false); print("C95 RAIL",r.class,r.handle,HexAxialDistance(r,SMRC95Home),IsInWalkingDist(SMRC95Home,r:GetPos(),r.city),a and a.handle,b and b.handle)
```

First-screen witness: walking false and both station handles present. Observe the
actual train journey, physical habitat entry and workplace using the witness line.
This closes no rail gate if the resident merely walks, or the stations are missing.

For C102, provision a reachable working dome farther from the pad than the nearest
dome. Select the rocket and record the starting layout:

```lua
SMRC102Rocket=SelectedObj; local ds,safety,dist=GetDomesReachableByColonists(SMRC102Rocket.city,SMRC102Rocket:GetPos()); print("C102 START",SMRC102Rocket.handle,safety and safety.handle,#ds); for _,d in ipairs(ds) do print("C102 DOME",d.handle,dist[d],d.ui_working,d:HasLifeSupport()) end
```

First-screen witness: the farther live reachable alternative appears. Track an ordinary
resident of the nearest dome who actually joins the UI expedition; select that resident:

```lua
SMRC102Unit=SelectedObj; print("C102 SUBJECT",SMRC102Unit.handle,SMRC102Unit.residence and SMRC102Unit.residence.handle,SMRC102Unit.dome and SMRC102Unit.dome.handle)
```

While away, switch the nearest dome off through the UI. Do not reassign or teleport the
subject. On return, observe physical entry into the live dome, then run:

```lua
local c=SMRC102Unit; print("C102 ARRIVAL",c.handle,c.command,c.dome and c.dome.handle,c.holder and c.holder.class,c.dome and c.dome.ui_working,c.dome and c.dome:HasLifeSupport())
```

For removal, disable the pack in Mod Manager, exit fully, restart, and load our
`C95MID.savegame.sav` test slot (accept the missing-mod warning). Select its returning
resident by this read, then watch the physical result:

```lua
local c=HandleToObject[2000001502]; print("C95 COLD",SMRFixPack~=nil,BuildVersion,c and c.command,c and c.residence and c.residence.handle,c and c.holder and c.holder.handle,c and c.workplace and c.workplace.class)
```

First-screen witness must say pack global false; repeat after travel. Re-enable through
the main menu and check the active module and another return. That enable path is also
unrun. The agent did not change `AccountStorage.LoadMods`/`account.dat`: persisting that
normal manager switch writes the protected owner save folder, forbidden by this brief.

## Departures, suggestions and unopened scope

DEPARTURES: supplied nested task path normalized to the mapped prompt filename.
The shared predicate accepts an already-occupied suitable bed at draft time, because
the first live run proved that asking for a spare reservation slot defeats the chosen
rule. C102's positive live leg stopped at the measured fixture gap; provisioning is
the owner's action. Cold-disabled restart and main-menu enable remain unrun under
the protected-folder boundary. The UI mission and rail journey remain owner gates as
specified. No other default was changed; no new no-dome or shortage rule was invented.

SUGGESTIONS: qualify a real rail return before calling train travel tested. The named
fixture lacks the route; this requires provisioning by the owner, not a scripted railway.

Not opened: external report accounts, retail portal/upload tools, unrelated defects,
the reporter's all-habitat colony, or other saves. No version field changed.

Executed model: GPT-6 (Codex), as supplied by this session's transcript. No subagents.

Close-out checks: `python tools/doccheck.py` GREEN; staged `git diff --check`
excluding `docs/archive/logs/*` is clean (native logs retain their whitespace),
both complete C95 desk suites pass and all scoped body pins match. No game process
or armed temporary payload remains. Source changes and evidence are committed together;
remaining owner gates are preserved in ck200 and the pending release entry.
