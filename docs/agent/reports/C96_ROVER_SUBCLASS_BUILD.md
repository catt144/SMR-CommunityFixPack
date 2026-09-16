# C96 repair: class-definition installation, availability, and native rover cargo

Updated 2026-09-16. **The revised repair launched the Commander-required expedition with
the original Seeker aboard at `efebdf7`. The owner reports it returned still a Seeker and
looking correct.** The numeric return/no-extra-Commander check is pending; live removal/reload
remains untested. The original repair's attended failure is preserved below.
Module: `Code/Fix_RoverSubclassManifest.lua`. Suite: `tools/desk_c96_rover_subclass.py`.
Entry: [C96](../bugs/C96.md). Remaining check: [live brief](../prompts/C96_LIVE_FAILURE.md).

## Authority and scope

Owner instruction in this diagnosis session: "You are clear to handle this in any way explore
or look at any file, rewirte any part of it you want". Condition: the owner was juggling other
work and expressly removed restrictions from the agent-authored brief. This authorizes choosing
and implementing the repair without another design-approval stop. Recorded at checklist 185.
The prior v11 ship ruling remains recorded; no release or publication is performed here.

## Cause and the earlier false refutation

**SOURCE**, installed 1.1.0.403908, Steam build 24995074: mod code loads before class construction
(`CommonLua/Core/autorun.lua:434`). `DefineClass` puts definitions into named globals
(`Core/classes.lua:71-73`); `g_Classes` is empty on first load (`:35-45`) or still holds old built
tables on reload. The build clears those old tables (`:1354-1363`) and rebuilds from the
separate definitions (`:1329-1335`, `:1436-1439`).

The old module's `install` selected `g_Classes[class_name]`. It silently skipped a missing
cold-boot entry, or patched an old table that was then cleared. `Require` checked the named
class definition, so it could pass while the installer targeted a different table. Its cargo
hook used the named class global and did not have this installation error.

**MEASURED desk falsifier:** separate the definition globals from the empty/old built registry
at module apply, then build from the definitions. The old module returns no rover; the old
shared-table fixture returns a Seeker. The revised installer takes `CargoTransporter` and
`CargoTransporterNew` directly, and passes both loading phases on both receivers.
[Initial failing run](../../archive/c96_registry_before_20260916.txt).

**The earlier live identity check did not prove that a hook was installed.** Comparing
`r.GatherAvailableRovers` with `g_Classes.CargoTransporterNew.GatherAvailableRovers` establishes
current dispatch identity, not the function's origin. Both can be vanilla. The brief's F4
measurement survives, but its "patched" interpretation and R1 refutation are withdrawn.
The separate closure-origin console check was prepared but has no observed result in this
session; the loading-order cause is established by source and the failing desk control.

## Current repair

| Surface | Implementation and bound |
|---|---|
| Installation | Patch the named class definitions before the engine builds descendants. |
| Available rover lists | Call the shipped lister by each descendant's own name. Reuse its drone, holder, control and idle predicates. Direct UI calls now see the same eligible subclasses. |
| Gather preference | First run the shipped gather with exact-class listing; keep that result if it fills the request. Only a shortfall admits subclasses. The temporary exact-only flag is restored after the protected call. |
| Mixed manifests | Reserve the rovers selected for stricter requested classes before offering them to a base request. A Seeker cannot satisfy both a Seeker line and a Commander line in one manifest. Recursion follows strict ancestry only. |
| Total availability | Wrap `GetTotalCargoAvailable`; for rover cargo, add the shipped count for each descendant. Connected-city counting remains shipped behavior. Non-rover types pass through. |
| Busy warning | Preserve any shipped warning; if the exact-label busy check missed a subclass, compare total and eligible subclass counts and return the shipped busy-rover translation. Both warning receivers are covered. |
| Loaded cargo | Move the fulfilled portion of the base request to the actual leaf cargo line, then call shipped `AddCargoAmount` on that leaf. No fictitious Commander amount is created. |

**SOURCE:** list/gather gates are in `Lua/Buildings/CargoTransporter.lua:394-432` and
`Lua/CargoTransporterNew.lua:448-486`. Gate 3 is the local `get_city_cargo_available` plus
`GetTotalCargoAvailable` in `Lua/Cargo.lua:72-101`. The warnings are
`CargoTransporter:GetPayloadWarning` and `CargoTransporterNew:GetNonResourceCargoWarning`.
Function hashes in the module pin every wrapped body.

**SOURCE correction to the original cargo analysis:** native `UnloadRovers` reads
`self.cargo[rover.class]` and decrements it before spawning residual cargo
(`Lua/CargoTransporterNew.lua:670-705`). The original repair instead credited `RCRover` for an
actual `RCSensor`; making its gather live would expose a missing cargo entry and an extra
Commander on unloading. `ForceUnloadRemainingCargo` makes the same leaf-key assumption
(`:1159-1190`). The new accounting keeps the physical and recorded class identical.
For a single substitution, `RCRover requested=1 amount=0` becomes `requested=0 amount=0`, and
`RCSensor requested=1 amount=1` is added. **The loaded manifest should therefore show a
satisfied Seeker line, rather than pretend that a Commander is aboard.** Launch still must
satisfy the original Commander-requiring anomaly.

## Design choice and removal

The owner's "let it be both" idea is applied at cargo queries rather than by changing the
city's permanent label membership. **SOURCE:** `LabelContainer:AddToLabel` also starts label
effects and reactions (`CommonLua/LabelContainer.lua:37-65`), and its game extension applies
modifiers (`Lua/LabelContainer.lua:17-27`). `CityObject:AddToCityLabels` is reached through
GameInit/map transfer and a named fixup; this review did not prove that every normal load
rebuilds labels. The brief's no-persistence expectation is not established evidence.
No exhaustive consumer audit is claimed or needed to recommend a membership mutation here,
because no membership mutation is being recommended or built.

The shipped `RCRoverAndChildren` label supplies an inclusive Commander pool, but does not by
itself change the lister's exact-class predicate, and is specific to that family. Calling the
shipped lister separately by leaf class preserves all its eligibility checks and handles other
shipped rover subclasses with the same mechanism. Summing native leaf counts repairs the
file-local availability gate through its existing global entry point.

**SOURCE / design bound:** no label, class identity, GameVar, thread, callback or custom saved
field is added. Request/amount changes use only native cargo fields. Removing the pack returns
unloaded base-class requests to vanilla matching; already-loaded substituted cargo remains a
native Seeker record. **MEASURED at the desk:** the unmodified accounting/spawn phase of native
`UnloadRovers` returns the Seeker without spawning a Commander. **UNRUN:** actual save
serialization, reload, animations and removal in retail. This is not a live save-safety verdict.

## Current diagnosis: live evidence

**MEASURED**, owner attended, retail `1.1.0.403908` (`6a91a190` suffix), repo `76bf141`:
`RCSensor list: 1 | city same: true | connected label: 1`, at `Lua 1:32:00:078`.
The exact-class lister can see and accept this Seeker. The prior empty Commander gather and
availability readings are inherited from the same sitting, not rerun by this line.

[RAN 2026-09-16, log Mars.exe-20260916-12.57.40-6a91a190.log]

```lua
*r local r = MainCity.labels.AllRockets[1] local l = r:ListAvailableRovers("RCSensor") print("RCSensor list:", l and #l or -1, "| city same:", r.city == MainCity, "| connected label:", #(GetCityLabelWithConnected(r.city, "RCSensor") or {}))
```

The line was parsed with `luaparser` and checked for one-line/no-comment paste safety.
[Retail log snapshot](../../archive/logs/c96_diagnosis_A_Mars.exe-20260916-12.57.40-6a91a190.log).
This is a snapshot of a running session, not a whole-session absence/error claim.
**MEASURED PROBE SWEEP:** `rg -n -F TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/` returned
no matches, corroborated by `python tools/doccheck.py --emit-fingerprint` at `76bf141`.

## Repaired retail run, 2026-09-16

**MEASURED**, owner attended, code commit `efebdf791d417bd811312ca26ef572a7f91d356e`,
retail `1.1.0.403908`, Steam build `24995074`, log
`Mars.exe-20260916-14.56.04-6a91a190.log`. Retail was restarted and the ESA/Wildfire
fixture reloaded; startup logged `RoverSubclassManifest: applied`. This is the existing
instrumented fixture with TestKit and OptInPack enabled, not a mod-free control. This
retest used read-only console lines and ordinary expedition controls; the earlier fixture
provisioning remains as described below. The preflight TEMPORARY sweep was clean at this HEAD.

[RAN 2026-09-16, same retail log, Lua 0:01:21:517-520]

```lua
*r print("C96 RETEST", "Commanders", #(MainCity.labels.RCRover or {}), "Seekers", #(MainCity.labels.RCSensor or {})) for _, r in ipairs(MainCity.labels.AllRockets) do local l = r:GatherAvailableRovers("RCRover", 1) print("C96 rocket", r.handle, r.command, "gather", #l, "available", GetTotalCargoAvailable(r.city, CargoType.Rover, "RCRover")) for key, item in pairs(r.cargo or {}) do if key == "RCRover" or key == "RCSensor" then print("C96 cargo", r.handle, key, "requested", item.requested, "amount", item.amount) end end end
```

The exact leaf-label counts were **Commanders 0, Seekers 1**. Rocket `1051` was already
in `CmdTakeOff`, recording `RCSensor requested 1 amount 1` and `RCRover requested 0 amount 0`.
Total Commander-compatible availability was 1. Its gather returned 0 because the Seeker was
already held aboard, as the next line establishes; this is not the original gather failure.
The owner reported: "flushed the rocket just took off". Rocket `1050` also appeared in the
snapshot but is not the successful expedition identified here.

[RAN 2026-09-16, same retail log, Lua 0:02:54:418]

```lua
*r for _, r in ipairs(MainCity.labels.AllRockets) do if r.handle == 1051 then local a, d = r.arrival_loc, r.departure_loc print("C96 flight", r.handle, r.command, r.RocketType, "to", r:GetArrivalLocType(), "from", r:GetDepartureLocType(), "to wants", a and a.requirements and a.requirements.rover_type or "none", "from wants", d and d.requirements and d.requirements.rover_type or "none") for _, v in ipairs(r.transported_rovers or {}) do print("C96 aboard", v.class, v.handle, "holder", v.holder == r, v.command) end end end
```

Output identified `1051 CmdFlyToLocation RocketExpedition`, from `our_colony` to `anomaly`,
destination `rover_type = RCRover`, carrying `RCSensor 2000000261 holder true WaitToAppear`.
This joins the actual Seeker to the original Commander-required destination.
At `Lua 0:03:56:214`, TestKit then attached its rover panel to that same `RCSensor(2000000261)`.
**OWNER OBSERVED after the requested return:** "Done and its still a seeker and looks correct".
The numeric return/no-extra-Commander check is pending. These readings are preserved in the
[flight and return-observation snapshot](../../archive/logs/c96_flight_return_observation_Mars.exe-20260916-14.56.04-6a91a190.log).
This is a running-session snapshot, not a whole-log absence/error verdict.

[PREPARED and parsed with `luaparser`; no observed output yet]

```lua
*r print("C96 RETURN", "Commanders", #(MainCity.labels.RCRover or {}), "Seekers", #(MainCity.labels.RCSensor or {})) for _, v in ipairs(MainCity.labels.RCSensor or {}) do print("C96 returned", v.handle, v.class, "held", not not v.holder, "command", v.command) end
```

## Regression suite

**Generator coverage, checked 2026-09-16 at `efebdf7`:** the solar-panel rover is the
RC Generator, `RCSolar` (`Lua/Units/RCSolar.lua:3-15`), which inherits `RCRover`.
The archived suite below explicitly passes `RCSolar also satisfies an RCRover request`
for both transporter receivers, plus the mixed-manifest leg reserving the Seeker while
the Solar fills the base request. The fix uses ancestry rather than a Seeker-specific exception.
Generator flight/return is not independently playtested.
**Fixture correction:** the earlier C96 entry called this rover sponsor-unlocked. The shipped
`Data/Cargo.lua:65-71` instead has `locked = true` and `verifier = sponsor == "CNSA"`.
Use China for an ordinary Generator fixture; it is not an unlocked substitute for ESA.

**MEASURED:** `python tools/desk_c96_rover_subclass.py`, checked parent HEAD `d1f262b`, installed Steam
build `24995074`, Lupa Lua 5.4: **55 legs pass**. The emitted TOTAL is reconciled against the
named PASS members in [the archived run](../../archive/c96_repair_checked_20260916.txt), which
also records the tested module SHA256 and the passing module-scoped bodycheck. The warning
body pin was emitted with bodycheck normalization after an initial raw hash retained trailing
whitespace; no shipped source changed. Harm legs run against unpatched shipped bodies.
The engine shims supply coordinates and fixture states, not actual pathing or serialization;
the shipped drone filters, connected-label query, cargo availability/status and warning bodies
are extracted rather than replaced with permissive stubs.

**MEASURED falsifier:** `python tools/desk_c96_rover_subclass.py --module-ref 76bf141` fails
`CargoTransporter cold class registry accepts the Seeker after class build`.
[Old-module failure](../../archive/c96_old_module_falsifier_20260916.txt).
The earlier suite aliased definitions and built classes, and omitted the total-availability,
warning and unload-accounting paths. Its old cargo-credit leg positively required the unsafe
base-class amount. That leg now requires an actual leaf record and a transferred request.
The original build's 22-leg/three-mutant claims are historical; the current run above is the
reproducible verification for this repair.

## Remaining live acceptance

Launch is proven and the owner's return observation is recorded above; do not repeat those
steps. The remaining check is the prepared numeric return line: expect no Commander, the
original Seeker `2000000261`, and no holder. Once flushed, preserve that snapshot, record the
bounded attended verdict, and consume the brief. Exact-Commander preference, reverse matching,
Generator substitution and mixed manifests remain desk-verified without independent retail
verdicts. Live removal/reload stays explicitly unclaimed, as the brief permits.

## Inherited fixture derivation

The following derivation is inherited from the original build, not re-derived this session.

### The fixture is cheaper than a random anomaly hunt — MEASURED 2026-09-16

⭐ **A Commander-requiring anomaly is guaranteed by construction, not rolled for.** There are
**two** sources of an anomaly's requirements and only one is random:

- **Random:** `PlanetaryAnomaly:InitRequirements` (`Lua/Buildings/PlanetaryAnomaly.lua:229-252`)
  — a rover requirement at all is a 25% roll, then `table.rand` over
  `GetAvailableResupplyRovers()`. Per-anomaly odds of drawing `RCRover` specifically are low.
- ⭐ **Deterministic:** the `CreatePlanetaryAnomaly` story-bit effect sets `required_rover`
  outright (`Lua/ClassDefs/ClassDef-Effects.generated.lua:483-500`). Shipped users:
  **`BrineDeposit.lua:74` and `ColdResistantBacteria.lua:62` both specify `"RCRover"`**
  (`RedMars_2:44` and `TreasureHunt_2:10` use `RCTransport`; `WindsOfChange_0:11` uses
  `ExplorerRover`). Neither RCRover bit contains any `Mystery` reference — they are gated on
  terraforming parameters and resources, i.e. ordinary play.

⇒ **Play toward `BrineDeposit` or `ColdResistantBacteria`** rather than scanning for luck.

⭐ **Rivals cannot take that anomaly.** They do contest anomalies (`AIContestAnomaly`), but the
contestable pool is `not item.scanned_by and not item.custom_id`
(`Lua/RivalColonies.lua:738-746`), and the story-bit effect creates its anomaly with
`custom_id = self.id`. **A story-bit anomaly is excluded from rival contest by construction**, so
a rival-heavy fixture does not endanger this leg — only the random-roll anomalies, which are not
the ones this test needs.

**Fixture identity, MEASURED so it is not re-derived at setup time:**
the sponsor shown as **"Europe"** in Mission Setup is preset **`id = "ESA"`**
(`Data/MissionSponsorPreset.lua:542,569`), which is what the Seeker's
`verifier = sponsor == "ESA"` requires · the mystery shown as **"Wildfire"** is
**`Mystery 8` / `TheMarsBug`** (`Data/Scenario/Mystery 8.lua:4-5`, class
`Lua/Mysteries/TheMarsBug.lua:1`), and `mystery_id` is set from the setup choice at colony
creation (`Lua/Mysteries/Mysteries.lua:41-43`) — so a colony created with Wildfire selected needs
**no `CheatStartMystery`** to be running it.
⚠️ **This corrects a claim made in session:** a per-anomaly odds figure was quoted as though it
governed a whole playthrough, which it does not — the owner's report that every playthrough
produces a Commander expedition is correct, and the story-bit path is why.

⭐ **A mystery does NOT interfere with this leg.** `if self.requirements then return end
-- preinitialized by story bit` (`:230`) is real, but **MEASURED**: `Mystery 8` (`TheMarsBug`)
contains **0** `CreatePlanetaryAnomaly` and **0** `required_rover`. Starting it cannot preset a
rover requirement, so a co-run investigation that starts that mystery does not confound this
test. ⛔ Do not re-raise a conflict here without naming a story bit that actually presets one.


### Recreate the attended anomaly

Retained from the live brief's measured fixture instructions; not re-derived here.
Use Europe (`ESA`), Wildfire (`Mystery 8` / `TheMarsBug`), at least one Seeker and no
Commander. Any expedition-capable player rocket can be retyped for this mission; the
successful retest used `1051`, while the original fixture named `1050`.
The following line mutates the fixture by creating an anomaly with the shipped preset
requirements shape (`Lua/ClassDefs/ClassDef-Effects.generated.lua:483-520`).

```lua
*r local lat, long = GenerateMarsScreenPoI("anomaly") local a = PlaceObjectIn("PlanetaryAnomaly", MainMap, {custom_id = "C96Test", display_name = Untranslated("C96 SEEKER TEST"), init_name = false, reward = "research", latitude = lat, longitude = long, requirements = {rover_type = "RCRover"}}) print(a.custom_id, a.requirements.rover_type, a.latitude, a.longitude)
```

`reward = "research"` avoids a breakthrough popup or story-bit reward; omit it for the
shipped roll. `requirement_type = false` matches shipped story-bit anomalies. The custom
ID excludes rival contest. It registers immediately in the planetary view, opened by
`*r OpenPlanetaryView()`; the surface sector map does not show planetary anomalies.
The organic alternatives remain `BrineDeposit` and `ColdResistantBacteria` above.

Executed model for this diagnosis and repair: **GPT-6** (session developer identity).
No delegated agents. The original build and fixture derivation were recorded as Claude Opus 5.
