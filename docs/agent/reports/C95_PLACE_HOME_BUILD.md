# C95 place-home rebuild: build report

Build authorized by the consumed brief `C95_PLACE_HOME_BUILD.md` (commit `39f5fa9`), at the owner's
2026-09-17 ruling in [C95](../bugs/C95.md). Replaces the route-gated build in
[C95_RETURN_HOME_BUILD.md](C95_RETURN_HOME_BUILD.md). Game 1.1.0.403908, executable `6a91a190`,
Steam 24995074. No upload and no version edit.

## Live work list

- DONE: orient and staleness. `git diff --stat a5f24bc..HEAD` on the brief's scope showed only the
  brief's own C95.md commit.
- DONE: placement in the return module (`8b1c296`).
- DONE: draft route gate retired (`8b1c296`, same commit as the return repair).
- DONE: desk suites, whole, with pre-fix harm legs and scratch-variant falsification (`8b1c296`).
- DONE: probe sweep. Before arming, `grep -rln TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/`
  had 0 hits. The only armed payload was `98_C95Place.lua`, declared here. After disarming, 0 hits
  and the kit tree was clean.
- DONE: live legs (`6e31aa2`).
- DONE: ck200 rewrite, entries, this report and the outbox. The owner-only legs are in ck200.

## Design

**Draft.** `HabitatExpeditionDraft` excludes habitat residents only while
`HabitatExpeditionReturn` is inactive. While it is active, the gather is vanilla's. The
predicate export and the route test are gone.

**Selector** (`Colonist:GetExpeditionReturnDome`, synchronous). The owner's scope condition is
fixed: `expedition_residence` must be a `MicroGHabitatBase`. The held habitat is added to the
colonist's private candidate list, whatever the route, when all of these hold:

- the reservation is still this colonist's;
- it is not already a candidate;
- it is valid and on the landing's map;
- it is working, accepting and has life support;
- `CanVisit(unit)` and `IsSuitable(unit)` pass.

The C102 wrapper sits inside this one. If the result is that home and the home is outside
`IsInWalkingDist` of the landing, the colonist is recorded in a weak-keyed, in-memory table.

**Placement** (`Colonist:SetCommand`, synchronous). This runs when a marked colonist is issued
`TransportByFoot` to that home, which is the tail of the native `ReturnFromExpedition` body after
the disembark animation. The mark is consumed, and inside `pcall` the colonist is set down at one
of the home's own entrance points. It re-checks first: reservation held, no holder, valid
position, home still usable, still outside walking range. The original dispatcher then runs;
native `Unit:EnterBuilding` walks the last step and calls `OnEnterUnit`. That is the same
entrance-point `SetPos` Unit:EnterBuilding performs for a unit without a position (`Unit.lua:380-389`).

**Rejoin.** The housing-before-employment hook on `UpdateWorkplace` is unchanged.

## Departures

1. **Seam and shape.** The placement hooks the walk order, not a command body. The colonist still
   disembarks at the rocket, and native entry takes them in. `RandPlaceColonist` was not used:
   for a habitat it is `Community:RandPlaceColonist` (`SetPos` plus `SetHolder`), which bypasses
   `OnEnterUnit`. The mark is not saved. A save and reload inside the disembark animation loses it,
   and that colonist then walks to the still-held home, as vanilla would once the home is selected.
   Desk-proven only.
2. **Place instead of walk.** Default kept: walk in range, place otherwise. Placing always would
   discard the live-proven walk for no gain.
3. **Train.** The module no longer queries or admits rail. For a far home, vanilla's dispatcher
   still books a train when `GetTransportRoute` finds one (desk leg). The final walk from the
   arrival station starts in range and is not placed. A real rail journey remains unobserved.
4. **Other maps.** Not admitted (`IsSameMap`); C102's fallback applies. Placement across maps would
   need a map transfer and a city and label move. `Colonist:SetDome` refuses a map with no elevator
   (`Colonist.lua:397-408`), and I did not read the colonist city migration an engine
   `TransferToMap` would need. A home reachable on foot through an elevator is already in vanilla's
   list and walks through `TransportByFoot`'s elevator branch.
5. **Covert ops.** Recruits are created fresh with `init_with_command = {"Disappear", ...}` and
   no residence (`CovertOps.lua:124-131`), and are never boarded through `EnterTransporter`. They
   cannot carry `expedition_residence`, so no scoping was needed. A desk leg drives one through the
   receiver and body, and it is not placed.
6. **Admission and player filters.** A residence filter that now forbids the colonist
   (`IsSuitable`, `filter_residents`) declines placement, and C102's fallback applies. Vanilla
   already drops the hold at boarding when that test fails (`Colonist.lua:5003-5007`). The dome
   trait filter (`traits_filter`) is not an admission test here, just as vanilla's in-range return
   ignores it.
   - Measured: in `BUG.savegame.sav` as it is on disk, every habitat has
     `filter_residents=Everyone`, and all 10 residents are geologists with a trait-filter score of
     1. The owner's sitting mutations (filters stripped, botanists imported) are not in that file,
     and this build used none.
   - The real gather was asked for a crew size with no specialization, so no expedition preset's
     crew requirement applied.
7. **Earth arrivals** landed through the same landed rocket's receiver: `GenerateArrivals` from
   `cargo.Passengers` inside `UnloadPassengers` (`CargoTransporterNew.lua:1073-1079`). It was not a
   flown passenger rocket.

## Desk evidence (HEAD `8b1c296`)

- `python tools/desk_c95_return_home.py`: 68/68. It runs the extracted shipped selector, chooser,
  both receivers, dispatcher, reservation bodies and the `ReturnFromExpedition` body, whose own
  tail issues the walk order. Pre-fix harm legs:
  - the vanilla selector loses the far home;
  - the dispatcher books a train;
  - the fallback reservation erases the hold;
  - the shipped body walks from the rocket.

  The brief's required legs are all present:
  - a far home placed, on both receivers;
  - an in-range home walked;
  - an unusable home falls to C102 and walks;
  - an Earth arrival, a migrant, a dome returnee and a covert recruit are never placed;
  - the reload residual walks.
- `python tools/desk_c95_habitat_draft.py`: whole suite passes. Pre-fix harm: the route-gated
  module from `39f5fa9` holds back residents with no route, on both receivers. The rebuild drafts
  them while the return repair is active and keeps exclusion when it is inactive.
- Falsification, scratch copies via `C95_RETURN_MODULE` / `C95_DRAFT_MODULE`:

  | variant | result |
  |---|---|
  | no `SetPos` | 63/68, the five placement legs failed |
  | placement without the habitat mark | 63/68, the arrival, migrant, covert and reload legs failed |
  | mark in range only | 68/68 (the placement-time range guard also holds) |
  | both range guards removed | 66/68, the in-range and rail-station legs failed |
  | prior build `39f5fa9` | failed no-route admission and placement, then threw in the C102 section |
  | draft: always exclude | failed "draft takes residents with no route home" |
  | draft: never exclude | failed "return veto retains exclusion" |

- `python tools/desk_c83_arrivals.py` 12/12; `python tools/desk_f117_argshape.py` 11/11.
- `bodycheck --module HabitatExpedition --all`: 28 rows OK. `--module ArrivalDeaths`: 11 OK.
  `harvest_wrap_targets --check`: 0 sites outside Require.

**No-yield re-check for each wrapped call.** `python tools/blocking_analysis.py tools/c95_blocking_targets.json`:

| wrapped call | callees in the added code | verdict |
|---|---|---|
| `GetExpeditionReturnDome` | `IsKindOf`, `table.find`, `IsValid`, `IsSameMap`, `HasLifeSupport`, `CanVisit`, `IsSuitable`, `IsInWalkingDist`, the original | all clear |
| `SetCommand` | the above, plus `GetEntrancePoints` (clear) and `Colonist:Random` | clear by hand, see below |
| `UpdateWorkplace` | unchanged | clear |
| both gathers | the draft's `IsActive` read | clear |

- **`Colonist:Random`:** the tool reports BLOCKS through a name collision with
  `LandingSiteObject:Random`. Read by hand, `Colonist:Random` goes to `CityObject.Random`, then
  `SessionRandom` or `city:Random`, and neither yields.
- **Engine calls:** `SetPos` is engine C.
- **The original `SetCommand`:** clear. When the order is issued from the colonist's own command
  thread, `DoSetCommand` deletes that thread (`CommandObject.lua:354-384`), so nothing of ours
  runs after it.

## Live evidence (HEAD `8b1c296`, unattended)

This is a retail `Mars.exe` receiver test, not a flown mission, archived as
[`c95_place_Mars.exe-20260917-11.03.48-6a91a190.log`](../../archive/logs/c95_place_Mars.exe-20260917-11.03.48-6a91a190.log)
(raw sha256 `ec36005f…083d20f9`, stored LF `6cd82dc7…f7b8116`).

- **Run setup.** Leg `tools/arming/legs/c95-place.json`, payload `98_C95Place.lua.txt`. Input:
  `C95PLACE.savegame.sav`, byte-identical to `BUG.savegame.sav` (sha256 `D844AFEB…4E970F`).
  Landed `UniversalRocket` 1061.
- **Habitat census.** 2096 is not walkable: path length 46400, so a foot path exists beyond the
  cap. It is 37 hexes away with 3 residents. 2669 and 2673 are walkable, with 4 and 3 residents.
  2351 is empty.
- **Draft.** The real `GatherAvailableColonists(10)` took all 10 habitat residents, including
  the three whose home has no walking route.
- **Far residents placed.** 2000000934, 2000000935 and 2000001919 each ran `ReturnFromExpedition`
  4 hexes from the rocket and 36 from home. At the next 20 ms poll they were in `TransportByFoot`
  with holder 2096, 1 hex from it, then `Roam` inside.
- **In-range residents walked.** The seven entered `TransportByFoot` at 29 and 20 hexes from home,
  with no holder.
- **Earth arrivals walked.** 2000002869, 2000002870 and 2000002871 took C83's reroute from Novo #1
  to habitat 2669 and walked there: 20 hexes out at their walk order, 11 to 14 after reload, then
  entered. None was placed.
- **Mid-return save and reload.** Saved as `C95PLACEMID.savegame.sav` (sha256 `B5F46C2E…7BE141`)
  while all seven in-range residents were walking. Reloaded: they continued and entered 2669 and
  2673, and the placed three stayed in 2096. After a 20 s soak all 10 were inside with their own
  residence.
- **Logscan.** `python -X utf8 tools/logscan.py <archived log>`: 50 of 50 pack modules applied,
  0 error-shaped lines.

**Instrument history (runs 1 to 4, not archived; kept in `C:\Dev\SMR-C95PlaceScratch\`).**

1. The census read a label that does not exist and skipped.
2. The observer wrapper logged only after the original call. The original deletes the calling
   command thread, so it never logged. The position poll replaced it.
3. Run 2's game quit two seconds after a colonist infopanel opened, before its final lines,
   consistent with someone at the keyboard.

Results of runs 2 to 4 agree with run 5.

**Save folder.** `C:\Dev\SMR-C95PlaceScratch\save-inventory-before.json`: 41 of 43 members are
unchanged by sha256. New members are exactly `C95PLACE` and `C95PLACEMID`. `account.dat` and
`account.dat.bak` were rewritten by the game's own launches and exits, which this brief did not
anticipate. No owner save was written.

## Owner sitting

ck200 in [the checklist](../../PLAYTEST_CHECKLIST.md) holds the gates. Each console line is
paste-safe; first-screen witnesses are stated per leg.

**Leg 1: UI expedition, far habitat.** Copy `BUG.savegame.sav` to a new slot and load it with the
pack enabled. Its residents are geologists, so choose an expedition whose crew geologists satisfy.
If none is offered, name any mutation you make. Paused, run:

```lua
SMRC95H=HandleToObject[2096]; SMRC95C=table.icopy(SMRC95H.colonists); print("C95 START",BuildVersion,SMRFixPack.IsActive("HabitatExpeditionReturn"),SMRC95H.class,#SMRC95C); for _,c in ipairs(SMRC95C) do print("C95 RESIDENT",c.handle,c.command,c.residence and c.residence.handle) end
```

Witness: `C95 START ... true NaturalistHabitat 3` and three residents of 2096. Send the expedition
through the UI. At departure and after it returns, run:

```lua
for _,c in ipairs(SMRC95C) do print("C95 WITNESS",c.handle,c.command,c.expedition_residence and c.expedition_residence.handle,c.residence and c.residence.handle,c.holder and c.holder.handle,c.workplace and c.workplace.class) end
```

Departure witness: at least one resident has holder = the rocket and expedition home 2096. Return
witness: that resident is shown in 2096 moments after stepping off, with residence 2096. If no 2096
resident was drafted, this leg does not count.

**Leg 2: pack-disabled cold restart mid-return.** Disable the pack in Mod Manager, exit fully,
restart and load `C95PLACEMID.savegame.sav` (accept the missing-mod warning). Run:

```lua
for _,id in ipairs({2000000934,2000000931,2000002869}) do local c=HandleToObject[id]; print("C95 COLD",SMRFixPack~=nil,id,c and c.command,c and c.residence and c.residence.handle,c and c.holder and c.holder.handle) end
```

Witness: the second field is `false` on every line. Unpause for a sol and repeat. Expected:
2000000934 stays in 2096, 2000000931 finishes walking into 2673, the arrival keeps its own path, and
no error dialog appears. Re-enable afterwards.

## Suggestions

- `tools/arm_leg.ps1` `Strip-LegLines` drops any metadata line naming a `mustNotBeListed` entry,
  commented or not. Every arm and disarm deleted the kit's disarmed `97_ForceInactive` note. It was
  restored byte-for-byte from kit HEAD (sha256 `08b4c6ca…6a47a4`). The tool is outside this brief;
  it wants a leg that keeps a commented `mustNotBeListed` line.
- An observer that logs after a command dispatch is silent for orders issued inside the command
  thread. Log before the call and read positions afterwards.
- The draft module is a no-op while the return repair is active; it keeps only the inactive-return
  safety. Retiring it is a later owner call, not made here.
- Arrivals that C83 sent into habitat 2669 later left for DomeHexa 2770. That is
  [C106](../bugs/C106.md)'s territory, routed there and not fixed.

## Not opened

- A flown expedition or UI mission, and a rail journey.
- The cross-map city and label migration.
- Opt-In Residency Control composition live (it is inactive in every run).
- Main-menu enable path.
- The reporter's pack version.
- The lander, elevator and asteroid paths (unchanged).
- Whether `GetEntrancePoints` can return nil for a Micro-G habitat (Micro-G is unrun; nil walks).

Executed model: Claude Opus 5 (`claude-opus-5[1m]`), from this session's transcript. No subagents.
