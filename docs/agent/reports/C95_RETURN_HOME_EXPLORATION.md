# C95 return-home exploration

**Buildable for a valid, reachable home; the nearby case returned home in retail.**
The best candidate widens the synchronous home selector's input and lets the
shipped dispatcher handle travel. It needs no full-body replacement. This is an
unshipped exploration, authorized 2026-09-16, executed into 2026-09-17.

## Live work list

- DONE — Trace and compare repairs; source findings committed as `a216b58`.
- DONE — Build an unshipped prototype and exercise desk and retail paths; `194f4c3`.
- DONE — Finish this report, rewrite ck200, consume the prompt and verify documentation; final close-out commit.

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
The desk employment method is an observation stub and SetResidence only records
the chosen property; the extracted UpdateResidence establishes call order, not
full housing/job behavior. ChooseDome returns the declared fixture fallback
rather than scoring a colony. The retail pair supplies the actual allocation
and movement evidence; the harness makes no broader simulation claim.

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
The save comparison is reproducible while the local baseline remains present:

```powershell
python -c "from pathlib import Path; import hashlib,json; r=Path('C:/Users/stkot/Saved Games/Surviving Mars Relaunched/76561198020568696'); e=json.loads(Path('C:/Dev/SMR-C95Scratch/save-inventory-before.json').read_text()); bad=[n for n,h in e.items() if not (r/n).exists() or hashlib.sha256((r/n).read_bytes()).hexdigest()!=h]; print('members',len(e),'changed',bad); assert not bad"
```

## Outstanding evidence

Far habitat by train, an actual all-habitat colony, a habitat beside the EF-107
dome, a full mission, save/load and removal remain open. Ordinary dome homing and
both return receivers were checked at the desk. No C95 status change or shipping
authorization follows from this prototype.

## Candidate ranking and cost

| Candidate | Technique and save footprint | What it buys; why ranked here |
|---|---|---|
| **Selected: add only the returning colonist's held habitat to a private selector input; housing before jobs on rejoin** | FIX_POLICY §1.4 chained wrappers, §3a layer 3; no new persistent state | Repairs the observed nearby/full case and desk rail case, keeps original bodies and both receivers. Refuses to invent a route or recover an already lost home. The employment hook also affects an ordinary migrant rejoining a reserved habitat with no residence; that bounded widening applies the existing habitat job rule consistently. |
| Widen `GetDomesReachableByColonists` or `MicroGHabitatBase:CanVisit` globally | Global/class wrapper, potentially synchronous | A common reachable list has no returnee identity. Adding every full habitat or admitting anonymous visitors changes unrelated arrivals and capacity decisions. Still needs a train route rule. Inferior scope to the per-colonist selector. |
| Replace both receivers and the shared return command | §1.5 full replacements; blocking frames can enter saves | Can own fallback choice, disembark, travel and cleanup explicitly. Unnecessary for the demonstrated repair and adds save-exit duties; only revisit if native rail behavior cannot meet the remaining cases. |
| Return to a temporary dome, then migrate home | Deferred hook/thread or persistent destination | Loses the original reservation before the proposed hook, permits the EF-107 employment drift, and requires retry/expiry and removal handling. More state for a weaker guarantee. |
| Retain exclusion or allow habitat residents only as a draft fallback | Synchronous draft filter | The first still strands all-habitat expeditions; the second sends some residents through the same broken return. Neither repairs homecoming. |

No preset or additive message supplies the per-returnee destination before the
fallback reserves housing. A return-command wrapper alone is too late. The
source census `rg -n 'GetExpeditionReturnDome\(' <SRC> -g '*.lua'` found the
definition and the two receiver calls listed above; the selector is shared by
both, not an inference from the class hierarchy.

The measured full-copy surface would be **46 + 20 + 49 = 115 lines**:
`CargoTransporterNew:UnloadPassengers`, `RocketBase:Disembark`, and
`Colonist:ReturnFromExpedition`. Measurement used `luafn.find_bodies` on those
exact declarations in Steam build 24995074; reproduce with:

```text
python tools/luafn.py Lua/CargoTransporterNew.lua '^function CargoTransporterNew:UnloadPassengers'
python tools/luafn.py Lua/Buildings/RocketBase.lua '^function RocketBase:Disembark'
python tools/luafn.py Lua/Units/Colonist.lua '^function Colonist:ReturnFromExpedition\('
```

The extracted inclusive spans are 1073–1118, 1969–1988, and 5076–5124. The chosen
prototype instead copies none of those bodies. A game patch to copied bodies
would require re-verification and could otherwise be masked by the old copy.
`bodycheck` can pin each named body with `--pin <path> <selector>`, detect body
drift and watch the defective membership expression. It cannot establish that
an added guard elsewhere repairs an absence, or detect all changed callee
semantics. The desk harness already emits dependency hashes; production would
also need manifests for selection, habitat admission, dispatch and housing order.

The prototype is deliberately not a release module: it lacks Register/Require,
veto handling, branch discrimination and reload/idempotence qualification. Its
current behavior is evidence for a design, not permission to paste it into Code/.

## Scenarios and boundaries

| Scenario | Evidence and disposition |
|---|---|
| Nearby, full habitat | **Retail A/B passed** on the original resident and unmodified habitat. Anonymous capacity rejection was the discriminating condition. |
| All-habitat colony | **Desk only:** both extracted receivers return a held habitat resident with no other destination. Removing the v11 exclusion would restore ordinary draft eligibility, subject to vanilla crew/specialization/liveness requirements. The live colony contained domes; no mass reassignment was used to manufacture this case. |
| Far habitat with rail | **Desk dispatch only:** selected home yields a native MigrateByTrain ticket and DisembarkOnArrival. No physical rail journey was observed. The provided fixture reports no station route from its rocket to its habitat. |
| Habitat beside a dome | The live control demonstrates displacement and new employment, but the specific EF-107 habitat beside DomeMega was not loaded. The synchronous rejoin hook prevents the desk picker from seeing a temporarily homeless returnee as an ordinary dome worker. Long transit beside that dome is untested. |
| Ordinary dome resident | Selector delegates unchanged. Housing hook requires a reserved habitat, so it does not alter dome residence. Desk control passes; no live dome-return regression leg was run. |
| Habitat destroyed, closed, unwelcoming or no longer suitable | Prototype delegates; it does not claim to preserve an invalid home. Rejected variants are desk tests. Safe fallback is still owed. |
| Habitat unreachable by walking or a verified same-map train route | Prototype delegates. It cannot make a physical route exist. No long walk, teleport or new shuttle path was added. Cross-map and shuttle-only homes are outside the admitted extension. |
| Already away when installed | Can help if vanilla's `expedition_residence` and matching bed reservation still exist. No new departure marker is required. A reference already cleared by the fallback cannot be reconstructed; no retrospective reassignment is attempted. |

**The v11 exclusion should be retired when a qualified return repair replaces it.**
Keeping it as an unconditional guard defeats the all-habitat case; inverting it
merely leaves the first residents admitted by the fallback exposed to the defect.
For the replacement, the difficult case is an unavailable home at return time.
This exploration has not chosen between waiting aboard, safe temporary shelter,
or refusing a departure lacking a return route. That changes player behavior and
needs the owner's decision, recorded in ck200. No such rule was invented here.

## Saves and travel hazards

The selected prototype owns no command body, game-time thread, GameVar, callback
stored on a unit, or new persisted class. Its private candidate table is used
synchronously and discarded. `UpdateResidence` uses the normal reservation and
forced-residence rules; the original `UpdateWorkplace` is always called and all
returns are passed through. Native disembark commands and native `TransportTicket`
objects own the blocking journey. That is §3a layer 3, avoiding new captured mod
frames by keeping all prototype execution synchronous.

`python tools/blocking_analysis.py C:/Dev/SMR-C95Scratch/blocking-targets.json`
reported `clear` for GetExpeditionReturnDome, UpdateWorkplace, UpdateResidence,
CanChangeCommand, CanVisit, CanReserveResidence, HasLifeSupport, GetTransportRoute,
SetResidence and ChooseResidence. The JSON consists of `["C95 prototype", name]`
pairs for that exact list. This is a source audit aid, not an engine serialization
test; direct source reads and the retail trace bound the claim. A yielding
third-party wrapper would invalidate that synchronous premise.

A save between selection and home carries vanilla destination/reservation/ticket
state. Removing the prototype leaves vanilla travel available, with ordinary
wrong-home or employment behavior able to return when the missing hook would
have run. No orphan cleanup code was introduced. **Mid-return save/reload and a
cold process restart with the prototype removed were not run**; they remain
release gates, and this report makes no measured removal claim.

F52/F53 were read before choosing the route. The prototype does not replace
TransportByFoot or ask it to walk to a distant habitat. For a far home it requires
a connected station pair before admitting the home, then relies on the existing
dispatcher. F53's OnArrival passability correction remains active. F58 keeps the
bed while away; F59's deferred housing notification remains active. Both packs
were present in the retail pair, with the same opt-in state.

The rail path skips the ordinary ReturnFromExpedition cleanup. In particular,
DisembarkOnArrival classifies expedition rockets using the legacy class and does
not explicitly clear the expedition fields. Residence:AddResident clears the
held residence through its normal cancellation path, but workplace cleanup,
interrupted journeys, destroyed stations and retargeting need a real rail leg.
This is a source-level difference requiring qualification, not a newly proven
independent defect or permission to change those systems.

The desk refusal leg is intentionally preserved: if CanChangeCommand prevents
UpdateResidence, the hook delegates with no fabricated assignment. The live
walking return allowed allocation. A shipping design must test the train rejoin
and interruptions rather than assuming the same timing.

## C102

**The design prevents the bad fallback for a valid reachable held habitat, but
does not close C102 generally.** A dome returnee, a lost reservation, an invalid
home or a home without an admitted route still reaches ChooseDome's unsafe
fallback. A separate safe-destination decision is required before its reservation
is placed. A receiver replacement could put both decisions together, but that is
not sufficient reason to copy it while the smaller C95 seam works.

The old C102 explanation that returnees never set `arriving` is false:
ReturnFromExpedition_TransportDestination sets it. The actual coverage gap is
that F53/C83's destination recheck is in **Idle**, whereas normal return dispatch
goes directly to ReturnFromExpedition or DisembarkOnArrival and runs OnArrival
before a subsequent Idle. No dead-dome suffocation was induced in this job.

## Remaining sitting and owner decision

ck200 now points here. The next takeable action, after the owner chooses the
unavailable-home policy, is a production-shaped unshipped build with the draft
exclusion retired only in that test configuration, proper registration and
branch checks, followed by the remaining live gates.

The shortest owner-assisted sitting uses a **copy** with an already inhabited
habitat connected by rail to a distant landing pad. Keep the original beds and
network. Pin a resident, send an ordinary crewed expedition through the UI, then
observe the resident's home, reserved bed and concrete rocket class on boarding;
on return record the native ticket/stations, physical habitat entry and workplace.
Use the actual all-habitat colony for the draft case if available. Save a test slot
mid-return, reload, then repeat from that slot after a full restart without the
prototype. The unavailable-route and dead-dome legs depend on the owner's policy.
No forced housing or teleported returnees count as these acceptance legs.

**Where this run stopped:** the normal-speed receiver A/B completed; no flown
mission, rail fixture, all-habitat fixture or save-removal leg was attempted. The
driver bypassed the existing draft exclusion to isolate the return mechanism.
Those are explicit departures from end-to-end coverage, not a claim that the
remaining native travel has been observed or that the UI cannot be automated.

## Departures, suggestions and unread material

**DEPARTURES:** the supplied path was normalized to the mapped root prompt.
The walking-only premise and `arriving` explanation were overturned by the
dispatcher read. A full nearby habitat was the live trigger. The prototype used
native controlled boarding/unloading rather than a mission flight so the shipping
filter and fixture housing stayed intact; flight/draft coverage remains owed.
The accelerated exploratory run was replaced by the normal-speed acceptance pair.

**SUGGESTIONS:** qualify a safe return destination for C102 alongside the next
build, and test the native rail cleanup before expanding scope to shuttles or
elevators. Neither suggestion authorizes implementation. No independent defect
outside this investigation was established.

**Not opened:** archived 1.0.7 source, packed Lua/DLC contents, the reporter's save
or external account/version data, the actual all-habitat colony, other campaign
fixtures, MarsDebug, achievement/research behavior, and portal/upload tooling.
The live source, named defect/fact passages, adjacent fixes, TestKit/arming code,
this fixture and these logs bound the investigation.

Close-out validation: `python tools/doccheck.py` GREEN; `git diff --check` clean;
`git diff --exit-code a0f9e1d -- Code/ items.lua metadata.lua` empty. C95/C102 and
EF-103/EF-104 hold the corrected source facts, this report holds the prototype and
remaining tests, and ck200 holds the owner's decision. The one-off and its map
row are consumed. No shipping files changed, no prototype is armed, and no game
process remains. Local save copy/baseline backups remain at the paths above.

Executed model: GPT-6 (Codex), as supplied by this session's transcript. No subagents.
