# C95 return-home exploration

**Buildable for a valid, reachable home; the nearby case returned home in retail.**
The best candidate widens the synchronous home selector's input and lets the
shipped dispatcher handle travel. It needs no full-body replacement. This is an
unshipped exploration, authorized 2026-09-16, executed into 2026-09-17.

## Live work list

- DONE — Trace and compare repairs; source findings committed as `a216b58`.
- DONE — Build an unshipped prototype and exercise desk and retail paths; evidence below.
- IN PROGRESS — Finish this report, rewrite ck200, consume the prompt and verify the final commit.

## Source finding that changes the design

The brief's walking-only description stops too early. Both return receivers issue
`unit:SetCommand("ReturnFromExpedition", rocket, home)`. The declaring
`Colonist:SetCommand` in `Lua/Units/ColonistTransport.lua:381-502` first invokes
`ReturnFromExpedition_TransportDestination` (:204-207), which sets `arriving`.
It can book a train through `StartTransport` (:354-371) and run
`DisembarkOnArrival` (:321-352), then `GoToStation`, without entering the
`ReturnFromExpedition` body at all. This is source evidence, not a live result.

The smallest candidate therefore widens the synchronous home selector's input
for a valid, reserved habitat with a verified walking or train route. The shipped
command dispatcher can perform the journey. A separate concern is employment
while the bed is reserved: the normal picker consults actual residence, not the
reserved habitat. The train branch's cleanup also differs from the walking branch.
The prototype's housing hook runs `UpdateResidence` before `UpdateWorkplace`
when the colonist rejoins its reserved habitat. Both functions remain vanilla.
The live walking case passes; train cleanup and interrupted returns remain open.

The fallback reservation can destroy the old-home reference *before* the return
command: `Residence:ReserveResidence` calls `CancelResidenceReservation`, whose
body clears `expedition_residence` (`Residence.lua:290-307,385-399`). A wrapper on
the return command alone is consequently too late to recover that identity.

Evidence commands at HEAD `a0f9e1dee67c9034a7d7436c58760f84a4b69990`:

```text
python tools/luafn.py Lua/CargoTransporterNew.lua 'function CargoTransporterNew:UnloadPassengers'
python tools/luafn.py Lua/Buildings/RocketBase.lua 'function RocketBase:Disembark'
python tools/luafn.py Lua/Units/ColonistTransport.lua 'function Colonist:SetCommand\(' 'function Colonist:DisembarkOnArrival\('
python tools/luafn.py Lua/Buildings/Residence.lua 'function Residence:(ReserveResidence|CancelResidenceReservation)\('
```

The installed fingerprint reports Steam build 24995074. Its date-bearing EF-107
group is labeled MOVED despite naming 1.1.0.403908; the targeted source read above
uses the installed tree, rather than treating that parser label as an update.

## Probe hygiene

Initial `rg -n TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/` returned no matches.
`tasklist /FI "IMAGENAME eq Mars.exe"` found no running game. These are preflight
observations only; repeat the process check immediately before a launch.

Declared for the live leg: TestKit `97_C95Home.lua` (prototype) and
`98_C95Explore.lua` (driver), armed by `tools/arming/legs/c95-explore.json`.
Both must be disarmed before recording results. The driver suspends autosaves
before loading the designated `C95EXPLORE.savegame.sav` copy.

## Prototype and measured result

Prototype: `tools/arming/payloads/97_C95Home.lua.txt`. Driver:
`tools/arming/payloads/98_C95Explore.lua.txt`. Arming manifests:
`tools/arming/legs/c95-explore.json` and `c95-explore-control.json`.
`python tools/desk_c95_return_home.py` reports **30/30** demands held on extracted
1.1.0 bodies, Steam build **24995074**, prototype SHA-256
`3435d1ae01c727ee49e297187967bdf7c439517e66b03b120acccd4a6b0ccc25`.
That command emits the complete member list, source spans and hashes. Route
answers and engine scheduling are stubbed; this is not live rail evidence.

**Tested-unattended, controlled boarding and return, not a flown mission.**
The unchanged `hab test A.savegame.sav` was copied to `C95EXPLORE.savegame.sav`.
The log identifies fixture `lD1jaGcMJOxaiFcU`. No housing, station, track, colonist
position or residence was edited by the driver. It chose an existing habitat
resident, switched the pad rocket to expedition type, and called the shipped
`LoadPassengers` and `UnloadPassengers` on **UniversalZeusRocket(1053)**.
The production draft was bypassed to select the subject; the v11 filter stayed
installed in both legs. Boarding's disappearance is native expedition behavior.
Flight, mission selection and scanning were not exercised.

Both accepted legs use `SetGameSpeed(3)` and game **1.1.0.403908**, executable
build **6a91a190**, repo **a216b58** plus the working prototype, TestKit **4cd18e6**
plus the declared payloads. The earlier fast exploratory pass used
`SetGameSpeed(10000)` and is not the accepted timing/control leg.

With the prototype, [the accepted log](../../archive/logs/c95_home_Mars.exe-20260917-00.05.53-6a91a190.log)
records:

```text
[C95HOME] BEFORE unit=2000002122 home=2692 residence=2692 rocket=UniversalZeusRocket(1053)
[C95HOME] ROUTE walk=true stations=nil,nil distance=13
[C95HOME] BOARDED disappeared=true reserved=2692 expedition_home=2692 holder=1053
[C95HOME] SELECT original_list_contains_home=false chosen=2692
[C95HOME] TRANSIT TransportByFoot holder=false residence=2692 dome=2692 ticket=false workplace=false
[C95HOME] HOME unit=2000002122 residence=2692 holder=2692
[C95HOME] SOAK residence=2692 dome=2692 workplace=false
```

The [control log](../../archive/logs/c95_home_Mars.exe-20260917-00.07.16-6a91a190.log),
same untouched copy and driver with the home prototype absent, records:

```text
[C95HOME] BOARDED disappeared=true reserved=2692 expedition_home=2692 holder=1053
[C95HOME] SELECT original_list_contains_home=false chosen=nil
[C95HOME] TRANSIT TransportByFoot holder=false residence=2733 dome=1076 ticket=false workplace=MetalsExtractor
[C95HOME] TIMEOUT physical home arrival
```

The control watched for eight game hours; the prototype observed physical entry
then waited another game hour. `ROUNDTRIP ok=true` means the driver did not throw,
not that the subject returned: the `HOME` and `TIMEOUT` lines discriminate.

This also falsifies the brief's suggestion that walking distance was the only
relevant gate. The near habitat was absent because `CanVisit()` received no
colonist and its occupied/reserved capacity was full. The real
`MicroGHabitatBase:CanVisit(unit)` accepts the held resident; the anonymous call
rejects it. The desk harness extracts that body and checks both answers.

`python tools/logscan.py` on the two accepted archived logs reports no
error-shaped lines. Startup Braze DNS failures occur before the test and remain
unresolved; the scanner does not classify them as gameplay errors. The fixture
was already cheat-tainted; both legs load the same bytes. The opt-in pack was
loaded, with ResidencyControl, CohortHousing and NoHomeless inactive; the same
configuration applied in both legs.

After process exit, the payloads were disarmed and `rg -n TEMPORARY Code/
../SMR-BugFixPack-TestKit/Code/` returned no matches. The armer removed a previously
commented ForceInactive line; the exact isolated metadata diff was restored.
TestKit is clean. A SHA-256 comparison of all **36** pre-existing `*.sav` members
against `C:/Dev/SMR-C95Scratch/save-inventory-before.json` found no changed or
missing owner saves. The two autosave-tagged files were backed up before launch;
`config.AutosaveSuspended=true` was logged before each run. Only the named copy
was added. Census and the superseded fast-run logs are archived beside the pair.

## Outstanding evidence

Far habitat by train, an actual all-habitat colony, a habitat beside the EF-107
dome, a full mission, save/load and removal remain open. Ordinary dome homing and
both return receivers were checked at the desk. No C95 status change or shipping
authorization follows from this prototype.

Executed model: GPT-6 (Codex), as supplied by this session's transcript. No subagents.
