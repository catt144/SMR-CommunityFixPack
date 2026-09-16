# C96 build — rover requests accept a rover's own subclass

**Authored 2026-09-16** on the owner's instruction (*"Go ahead and author the fix"*), which
**lifted their own 2026-09-15 ruling** that the repair wait for a playtest reproduction
(*"file it as a fix that needs playtesting then. Don't author the fix yet"*). ⛔ The lift is
the owner's, not an agent's reading of an expired gate. Game acceptance is still UNRUN.

Module `Code/Fix_RoverSubclassManifest.lua`, registered as `RoverSubclassManifest`.
Desk suite `tools/desk_c96_rover_subclass.py`. Entry [C96](../bugs/C96.md).

## What the repair does

Both gates, both receivers, and nothing else.

| gate | shipped body | what the module does |
|---|---|---|
| source list | `self.city.labels[class]` (`CargoTransporter.lua:428`) · `GetCityLabelWithConnected(self.city, class)` (`CargoTransporterNew.lua:481`) | calls the **shipped lister once per descendant class**, so each subclass is fetched from its own label |
| leaf compare | `unit.class == class` (`:425` / `:479`) | satisfied untouched — each call passes a subclass its **own** name |

⭐ **The shipped availability filter is reused verbatim** (drones, `CanBeControlled`, `holder`,
`IsIdle`). Nothing is reimplemented, so the module cannot drift from a copy we maintain.

⭐ **It widens ONLY on shortfall.** `GatherAvailableRovers` runs vanilla first and returns its
result untouched whenever the request is already satisfiable; the widened retry is kept only
when it is strictly longer. A colony holding the exact rover keeps vanilla's nearest-first
pick and the module is invisible. **Directional by construction**: a subclass satisfies a
request for its base, never the reverse.

⭐ **The cargo line is credited to the REQUESTED class.** `CargoTransporterNew:LoadRovers`
credits `AddCargoAmount(rover.class, 1)` (`:444`) and `AddCargoAmount` is a guarded no-op when
no line exists for that exact id (`:87`). A Seeker loaded against an `RCRover` line would
credit nothing, leaving `requested - amount` short (`:1837`) and the rocket still asking for a
rover it already carries. The remap fires only when the exact line is absent **and** a base
line exists — a combination vanilla never produces, since vanilla only ever loads exact-class
rovers.

**No object field, GameVar, thread, migration or saved callback is added.** The widen flag is
a weak-keyed module local, so nothing reaches a save. **MEASURED:** all four hooked bodies are
free of `Sleep` / `WaitMsg` / `WaitWakeup` / thread creation — asserted by the desk suite, so
a future shipped body that starts yielding fails the run rather than passing silently.

## The C95 lesson, applied

⛔ This module hooks **both** `CargoTransporter` and `CargoTransporterNew`. Hooking only the
legacy pair is exactly how `Fix_HabitatExpeditionDraft` shipped inert
([C95 sitting](C95_SITTING_20260916.md)): 1.1.0 expeditions run through `UniversalRocketBase`,
which carries `CargoTransporterNew` and neither legacy class. Both implementations carry both
gates identically, so both are repaired.

## Desk suite — 22 legs, and it is falsifiable

`python tools/desk_c96_rover_subclass.py` runs the **shipped bodies** against synthetic
fixtures, before and after the module applies. Harm legs are based on the pre-fix body.

Source-premise assertions (these fail if the defect is ever fixed upstream): both listers
still carry the leaf compare **and** the leaf-label source list · `BaseRover:AddToCityLabels`
still registers `Unit` + `Rover` + the leaf class with nothing walking `__parents` ·
`RCSensor` and `RCSolar` still derive `RCRover` · `AttackRover` still does not.

Behaviour legs, run for **each** receiver: vanilla refuses a Seeker for an `RCRover` request ·
the fix accepts it · a satisfiable request keeps vanilla's pick unchanged · a base does not
satisfy a request for its subclass · `AttackRover` is never offered · `RCSolar` is accepted ·
an unfillable request stays empty · a two-rover request fills from both nearest-first · a
non-rover class is never widened. Plus three cargo-credit legs and a no-throw leg.

⭐ **Falsified with three mutants**, each failing exactly its intended leg:

| mutant | leg that failed |
|---|---|
| never widen | `fixed accepts the Seeker` |
| widen unconditionally (drop the shortfall gate) | `satisfiable request keeps vanilla pick` |
| drop the cargo-credit remap | `fixed credits the RCRover line` |

**LIMIT, declared:** no game boot, real colony, pathing, UI, launch readiness or save
serialization is measured. Label membership and idleness are stated by the fixture.

## Two corrections this build made to the entry

1. ⭐ **The "one thing to read" is SETTLED and benign on the legacy path.** C96 flagged an
   unread risk: whether any bookkeeping re-checks the loaded rover by exact class. Both load
   loops simply append what the gather returns without re-checking
   (`CargoTransporter.lua:175-182`, `CargoTransporterNew.lua:146-153`), and the one place a
   class is read back takes it from the loaded object itself
   (`RocketExpedition.lua:844`). ⛔ **But the New path had a second, unflagged half** — the
   `AddCargoAmount` keying above — which this module repairs.
2. **Citation drift.** C96 attributes the leaf-only label registration to `BaseRover:GameInit`.
   `GameInit` does no label work at all (`BaseRover.lua:102-117`); the registration is
   `BaseRover:AddToCityLabels` (`:123-127`), which also adds `Unit` and `Rover`. The substance
   is unchanged — nothing walks `__parents`.

## What is NOT claimed

- ⛔ **Not reproduced in play, and not tested in a game.** The defect is source-verified on
  both trees and the repair is desk-verified only.
- ⛔ The ESA fixture the entry asks for has not been provisioned; the acceptance legs in
  checklist 185 (b) are unrun.
- ⛔ Nothing here says the repair ships. `ck185` (b) remains the owner's.

## Acceptance, when it runs

⭐ **The reach lesson from C95 applies to the test as much as the build:** the fixture's
expedition rocket must be the one the player actually uses. Name the concrete rocket class in
the save before reading a result, and arm a trace on the gather that actually runs.

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
⚠️ **This corrects a claim made in session:** a per-anomaly odds figure was quoted as though it
governed a whole playthrough, which it does not — the owner's report that every playthrough
produces a Commander expedition is correct, and the story-bit path is why.

⭐ **A mystery does NOT interfere with this leg.** `if self.requirements then return end
-- preinitialized by story bit` (`:230`) is real, but **MEASURED**: `Mystery 8` (`TheMarsBug`)
contains **0** `CreatePlanetaryAnomaly` and **0** `required_rover`. Starting it cannot preset a
rover requirement, so a co-run investigation that starts that mystery does not confound this
test. ⛔ Do not re-raise a conflict here without naming a story bit that actually presets one.

Legs: an anomaly expedition requiring an RC Commander, a colony holding **only** a Seeker →
the Seeker loads and the rocket launches · the cargo panel shows the Commander line satisfied
(this is the half the desk found) · a colony holding both keeps taking the Commander · an
anomaly wanting a Seeker still refuses a Commander · removal leg: disable the pack, restart,
reload, vanilla refusal returns and the save is intact.
