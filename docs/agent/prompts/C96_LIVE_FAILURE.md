# C96 — the repair is INERT in play. Find out why, then decide the design.

## Must_Read_Header
<!-- RULES -->
Rule: Do not close this brief while `Fix_RoverSubclassManifest` is registered in `items.lua` and unproven in play. [A3: pass]
Rule: Treat every measurement in §2 as inherited; re-derive only what its falsifier shows has moved. [A3: pass]
<!-- /RULES -->

**Authored 2026-09-16 against `a36bb13`** (check staleness with `git log a36bb13..HEAD -- Code/Fix_RoverSubclassManifest.lua docs/agent/bugs/C96.md docs/agent/reports/C96_ROVER_SUBCLASS_BUILD.md`).
Lifecycle: **one-off — `git rm` this file when the work list below is complete**, unless the owner
says otherwise. Its map row in `prompts/README.md` goes with it.

⛔ **Start execution with `git log` and `git pull`.** Peers commit this tree every few minutes and
Codex is invisible to `ListAgents`.

⛔ **Open a live progress list before executing**, one item per commit-and-verify unit, exactly one
in progress, rewritten when reality changes. The owner reads that list to decide when to step in.

---

## 0 · The one-sentence state

`Fix_RoverSubclassManifest` is **registered in v11 and does nothing**: on an attended sitting
2026-09-16 a Seeker-only ESA colony still could not send a Commander-requiring anomaly expedition
with the module active, and `GatherAvailableRovers("RCRover", 1)` returned **0** with every one of
the module's own preconditions satisfied.

⚖️ **The owner ruled on 2026-09-16 (ck185 b) that C96 ships in v11.** That ruling was made before
this evidence existed. ⛔ **Do not pull it, re-register it, or re-rule it yourself** — surface the
tension and let the owner rule again. The record is `docs/PLAYTEST_CHECKLIST.md` item 185.

---

## 1 · Read path — by file

- [`docs/agent/bugs/C96.md`](../bugs/C96.md) — the entry.
- [`docs/agent/reports/C96_ROVER_SUBCLASS_BUILD.md`](../reports/C96_ROVER_SUBCLASS_BUILD.md) — the
  build, its 22 desk legs and the fixture derivation. ⛔ Do not re-derive its fixture section.
- [`Code/Fix_RoverSubclassManifest.lua`](../../../Code/Fix_RoverSubclassManifest.lua) — the module;
  the two hook bodies are lines 107-147.
- `tools/desk_c96_rover_subclass.py` — the desk suite that passed while the module was inert.
- Additional records: grep `docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md` for
  `rover`, `cargo`, `label`, `expedition`. ⛔ Never read either INDEX whole.
- Sibling precedent: **C95 / `Fix_HabitatExpeditionDraft`** shipped inert for a related-looking
  reason. ⛔ That reason is **not** this one — see §3 R1.

---

## 2 · Derived facts — inherited, with falsifiers

All measured **2026-09-16, game build 1.1.0.403908**, attended, on the owner's live ESA/Wildfire
fixture: `UniversalRocket(1050)` "Vega #1", expedition attached to a rolled anomaly named
"Project Cavalcade", one `RCSensor(2000000261)`, no `RCRover`. Source tree
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

| # | fact | how measured | falsifier |
|---|---|---|---|
| F1 | Module is live | console `SMRFixPack.IsActive("RoverSubclassManifest")` → `true` | rerun it |
| F2 | Colony holds 1 Seeker, 0 Commanders | `#labels.RCRover 0 · #labels.RCSensor 1` | rerun the label print |
| F3 | The Seeker passes the shipped availability filter | `idle true · controllable true · holder false · command Idle` | rerun the state print |
| F4 | The rocket is on the hooked path | `r.GatherAvailableRovers == g_Classes.CargoTransporterNew.GatherAvailableRovers` → **true**; same for `ListAvailableRovers` | rerun the identity compare |
| F5 | The hook's own preconditions pass | `IsKindOf(g_Classes.RCRover,"BaseRover")` true; `ClassDescendantsList("RCRover")` = `RCSensor`(1 unit), `RCSolar`(0) | rerun |
| F6 | The gather still returns nothing | `r:GatherAvailableRovers("RCRover", 1)` → `0` | rerun |
| F7 | A third gate exists and is unhooked | `GetTotalCargoAvailable(MainCity, GetCargoType("RCRover"), "RCRover")` → `0`; panel shows `RC Commander 0/1` + "Not enough Rovers" | rerun the cargo-available print |

Source facts, same build — falsify with
`git diff --stat` is not available for the game tree; re-read the cited lines if the game updates:

- Three gates, not two. (1) source list `city.labels[class]`; (2) leaf compare `unit.class == class`
  (`Lua/CargoTransporterNew.lua:479`, `Lua/Buildings/CargoTransporter.lua:425`); (3) **availability
  count** — `GetNonResourceCargoWarning` → `GetCargoItemStatus` (`CargoTransporterNew.lua:1836-1847`)
  → `GetTotalCargoAvailable` → `get_city_cargo_available` → `#city.labels[class]`
  (`Lua/Cargo.lua:72-101`). ⭐ **The build covers 1 and 2 only.**
- ⛔ `get_city_cargo_available` is a **file-local** function (`Lua/Cargo.lua:72`). The only hookable
  seam on gate 3 is the global `GetTotalCargoAvailable`.
- `UniversalRocketBase` carries `CargoTransporterNew` and neither legacy class
  (`Lua/UniversalRocket.lua:28-42`). There is no purchasable Expedition Rocket in 1.1.0:
  `RocketExpedition` survives as a legacy class and as the **label name** for a universal rocket
  currently on an expedition (`g_RocketTypes.Expedition`, `UniversalRocket.lua:6`), and appears in
  no Cargo or sponsor resupply preset. ⇒ `RocketExpeditionBase:BeginExpedition` is **dead code for
  a 1.1.0 player**; do not reason from it.
- Rover label membership: `BaseRover:AddToCityLabels` registers each rover under `"Unit"`, `"Rover"`
  and **its own leaf class** (`Lua/Buildings/BaseRover.lua:123-127`). `RCRover` adds
  `"RCRoverAndChildren"` (`Lua/Units/RCRover.lua:112-114`), `RCSensor` adds `"SensorTower"` for its
  sensor object (`Lua/Units/RCSensor.lua:62-64`). These **combine** rather than override —
  `DefineCombinedMethod("AddToCityLabels", "call")` (`Lua/CityObject.lua:9`) — so a Seeker is in
  `Unit`, `Rover`, `RCSensor`, `RCRoverAndChildren`, and **not** in `RCRover`.
- ⭐ `RCRoverAndChildren` is a **shipped label already containing RCRover and every subclass**. It
  is not used by the cargo path. Consider it before inventing a new source list.
- `GatherAvailableRovers` (`CargoTransporterNew.lua:448-470`) is **pure** — it reads and returns a
  list, reserves nothing. Safe to call from the console as a probe.
- "RC Commander" is the display name of class `RCRover`; "RC Seeker" is `RCSensor`, ESA-gated.

---

## 3 · Refuted — ⛔ do not re-derive these

- **R1. "The hook never reaches the live class" (the C95 flattening shape) is REFUTED.** HG does
  flatten parent members into each concrete class at build time
  (`CommonLua/Core/classes.lua:1029-1033`), but F4 shows the rocket's resolved
  `GatherAvailableRovers` **is** the patched function. The pack installs early enough that
  descendants carry the patched copy. This was my first diagnosis and it was wrong.
- **R2. A direct `ListAvailableRovers("RCRover")` call proves nothing.** The lister widens only
  while `widening[self] == class`, a flag set **only inside** `GatherAvailableRovers`
  (`Fix_RoverSubclassManifest.lua:118-127`). A direct call returns 0 whether the fix works or not.
  ⛔ A brief that cites "avail: 0" from that call is citing a void measurement.
- **R3. "The Seeker was busy" is REFUTED** by F3.
- **R4. "The fixture was wrong / no expedition was attached" is REFUTED** — the panel showed
  `RC Commander 0/1` on a rocket with a live expedition.

---

## 4 · Scope

**In scope.** Find why the widened retry returns nothing (§5 A); decide and implement the design
(§5 B); close the desk-suite gap (§5 C); update the entry and build report with the live result.

**Out of scope.** Any other fix; the v11 release itself; C97's ten uncorrected errors
(`reports/C97_RECHECK.md`); the Wildfire/cure work. ⛔ Finding a defect elsewhere does not authorize
fixing it — file it in `docs/agent/bugs/` and carry on.

---

## 5 · The work

### A · Name the cause — do this first, it is cheap and it may make B unnecessary

The next measurement, **not yet run**, is whether the shipped lister can see the Seeker when asked
by its own exact name from that rocket. This needs no widening, so it reads straight:

```
*r local r = MainCity.labels.AllRockets[1] local l = r:ListAvailableRovers("RCSensor") print("RCSensor list:", l and #l or -1, "| city same:", r.city == MainCity, "| connected label:", #(GetCityLabelWithConnected(r.city, "RCSensor") or {}))
```

- `RCSensor list: 1` ⇒ the shipped lister is fine and the fault is in the **flag handoff** between
  the two hooks. Read `Fix_RoverSubclassManifest.lua:111-147` for `self` identity across
  `orig_gather` → `self:ListAvailableRovers`, and for `...` forwarding of `quick_load`.
- `RCSensor list: 0` **with** `connected label: 1` ⇒ the shipped filter rejects the Seeker even by
  exact name, and the defect is **larger than C96 describes**. Re-file accordingly.
- `city same: false` or `connected label: 0` ⇒ the rocket reads a different city than the one
  holding the Seeker. Follow `GetCityLabelWithConnected`.

⛔ **Stop and report** if the answer is not one of these three. Do not start B on a guess.

### B · The design decision — ⚖️ the owner raised it and it is theirs to settle

Owner's words, 2026-09-16: *"Why is the answer not just giving the seeker a commander flag, let it
be both?"* and *"this shouldn't be that difficult."*

The concrete form is: add the Seeker to `labels.RCRover` in `RCSensor:AddToCityLabels` **and** widen
the leaf compare. Present the owner with a recommendation and the evidence, do not just build it.

⭐ **What makes it attractive:** it fixes the label lookup in *both* its uses at once, including
gate 3, which no function hook can reach cleanly because `get_city_cargo_available` is file-local.
One registration replaces three hooks. The engine is already subclass-aware nearly everywhere —
almost every other consumer asks `IsKindOf(x, "RCRover")`, which a Seeker already satisfies.

⛔ **What makes label-membership-alone WORSE than the bug:** it does not touch `unit.class == class`.
The availability count would read 1 and the warning would clear, while the lister still filters the
Seeker out and never loads it — a rocket sitting at `0/1` **with no warning at all**. A silent hang
replacing an honest refusal. ⇒ **label membership without the compare change must not ship.**

**What must be established before recommending it:**
1. Enumerate every consumer of `labels.RCRover` and of dynamic `labels[<rover class>]` lookups.
   A single grep pass found no other direct reader — all others go through `IsKindOf` — but
   ⛔ that is one pass over a construct grep under-counts. Count the presence side.
2. Confirm label membership does not reach a save. `AddToCityLabels` is called on load, so the
   expectation is no persistence — prove it rather than assume it.
3. Say what breaks for a player who removes the pack mid-save.
4. Compare against the alternative of sourcing from the shipped `RCRoverAndChildren` label.

### C · The desk suite gap — required, not optional

22 legs and three mutants passed while the module was inert in play. Whatever A finds, add a leg
that **fails** against the current module, and say in the report what class of defect the suite was
blind to. ⛔ A fix invalidates its own tests: re-base the harm legs on the pre-fix body and rerun
the whole suite, not only the new leg.

### D · Record

Update `bugs/C96.md` and `reports/C96_ROVER_SUBCLASS_BUILD.md` with the live result. The build
report currently says "Not reproduced in play, and not tested in a game" — that is now false in the
second half: **it was tested, and it failed.** Route the owner-facing outcome to
`docs/PLAYTEST_CHECKLIST.md` item 185, not only to agent docs.

---

## 6 · Re-running the fixture from scratch

Everything below is **measured**, not a plan. ⛔ Do not re-derive it.

Fixture: sponsor **Europe** = preset `ESA` (the Seeker's `verifier`), mystery **Wildfire** =
`Mystery 8`/`TheMarsBug`. Own **at least one RC Seeker and no RC Commander** — a Commander makes
every leg vacuous. Any expedition-capable rocket works: all player rockets in 1.1.0 are
`UniversalRocketBase` variants, and one re-types itself to Expedition when sent to an anomaly.

A Commander-requiring anomaly can be **spawned outright** — no waiting on a story bit and no
scanning for luck. This produces the same object shape the shipped `CreatePlanetaryAnomaly` effect
produces (`Lua/ClassDefs/ClassDef-Effects.generated.lua:483-520`: a `PlaceObjectIn` with a preset
`requirements` table, and `PlanetaryAnomaly:Init` skips its random roll when `requirements` is
already set). Setting `custom_id` also excludes it from rival contest
(`Lua/RivalColonies.lua:738-746`):

```
*r local lat, long = GenerateMarsScreenPoI("anomaly") local a = PlaceObjectIn("PlanetaryAnomaly", MainMap, {custom_id = "C96Test", display_name = Untranslated("C96 SEEKER TEST"), init_name = false, reward = "research", latitude = lat, longitude = long, requirements = {rover_type = "RCRover"}}) print(a.custom_id, a.requirements.rover_type, a.latitude, a.longitude)
```

`reward = "research"` is a deliberate choice, to keep a breakthrough popup or a story-bit event off
the reading; drop the field for the shipped roll. `requirement_type` stays `false`, which matches
the shipped story-bit anomalies. It registers on the planetary view immediately
(`MarsScreenPointOfInterest:Init` → `InsertMarsLandingSpot`); open that view with
`*r OpenPlanetaryView()`. ⚠️ It is the **planetary** view — anomalies are not drawn on the local
surface sector map.

⭐ Deterministic organic route, if a spawn is unwanted: play toward the `BrineDeposit` or
`ColdResistantBacteria` story bits, which both set `required_rover = "RCRover"` outright.

---

## 7 · Evidence and reporting rules

- ⛔ **Read the log, do not ask the owner to transcribe it.** Newest
  `%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-*.log`; the owner says "flushed" when a line
  has run. SMRTK screenshots land in `C:\Dev\SMR-ScreenCaptures\`.
- Preflight every owner-typed line as one paste-safe line with no `--` comment. `*r` for
  multi-statement work. Read presence from the file log; claim absence only after exit.
- Run the probe-sweep step before testing, per `WORKFLOW.md` Probe hygiene. The freshness gate is
  an age satisfied at the next playtest — ⛔ it never refuses work.
- Label every probe tally with its build. ⛔ Never use a MarsDebug pass as retail evidence
  (`EF-044`).
- The owner cheats buildings, funding and supplies on this fixture and that is fine; name every
  mutation, and reject one that intersects the mechanism being measured.

**What may not be claimed.** ⛔ Do not write that C96 is repaired, verified, or shipping-ready on a
desk pass — that is exactly the claim this brief exists to correct. A run that loads the Seeker
proves the gather; only a **launched expedition with the Commander line reading satisfied** proves
the whole path, because the cargo-credit half (`AddCargoAmount`) can fail on its own. If the
evidence supports only the narrower statement, write the narrower statement.

**Stop conditions — permission to report rather than push on.** Stop and report if: A returns an
answer outside its three branches; the design decision in B needs the owner; the cause turns out to
sit in shipped code that no hook can reach; or the fixture cannot be restored to
one-Seeker-no-Commander.

**Completion.** The cause is named with a measurement, the owner has ruled on the design, the entry
and build report carry the live result, item 185 carries the owner-facing outcome, the desk suite
has a leg that would have caught this, `python tools/doccheck.py` is GREEN, and this file is
`git rm`'d with its `prompts/README.md` row.
