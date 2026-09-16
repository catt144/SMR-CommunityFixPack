# C96 - verify the repaired live rover-subclass path

## Must_Read_Header
<!-- RULES -->
Rule: Do not close this brief while `Fix_RoverSubclassManifest` is registered in `items.lua` and unproven in play. [A3: pass]
Rule: Treat every measurement in §2 as inherited; re-derive only what its falsifier shows has moved. [A3: pass]
<!-- /RULES -->

Updated 2026-09-16 during execution, starting from `76bf141`; code parent for the repair
is `fe5a2e8`. Start with `git log` and `git pull`, then inspect changes to
`Code/Fix_RoverSubclassManifest.lua`, its desk suite and the report since that parent.
Lifecycle: one-off; remove this file and its map row only after the remaining work is complete.

## Authority and live work list

The owner expressly authorized handling this task in any way, inspecting any file and rewriting
any part of the agent-authored brief. Checklist 185 records the exact instruction and condition.
**There is no remaining owner design-approval gate.** Do not revive the old sequencing stops or
the false R1 refutation from the original version of this prompt.

Open a progress list before execution, one item per commit-and-verify unit, exactly one in
progress. Update it when reality changes. Current remaining units:

1. DONE: repair and desk evidence committed at `efebdf7`.
2. DONE: retail restarted; rocket `1051` launched to an anomaly requiring `RCRover` with
   `RCSensor 2000000261` aboard. Actual cargo was Seeker 1/1, Commander 0/0. The owner reports
   return still a Seeker and looking correct. Log and exact lines are in the report.
3. IN PROGRESS: read the final prepared return tally after the owner flushes it; expect the
   same Seeker unheld, with no extra Commander. No output observed yet. Leave live removal/reload
   explicitly unclaimed. Record acceptance in C96, report and checklist 185, run doccheck, then
   consume this brief. Preserve checklist 185's independent C95 public-wording question.

## 2 - Read path and current facts

- `docs/agent/bugs/C96.md`: current summary first; later build sections are historical.
- `docs/agent/reports/C96_ROVER_SUBCLASS_BUILD.md`: source cause, design, limits and archived runs.
- `Code/Fix_RoverSubclassManifest.lua` and `tools/desk_c96_rover_subclass.py`.
- Search bug/fact INDEX rows by `rover`, `cargo`, `label`, `expedition`; do not read either whole.

| fact | evidence and falsifier |
|---|---|
| MEASURED retail exact-name listing works | At `76bf141`, log `Mars.exe-20260916-12.57.40-6a91a190.log`: `RCSensor list: 1`, `city same: true`, `connected label: 1`. Rerun the report's read-only line if the fixture changed. |
| SOURCE + MEASURED desk: old installer targeted the wrong tables | `g_Classes` is empty/stale before class build; named globals are definitions. `python tools/desk_c96_rover_subclass.py --module-ref 76bf141` fails the cold-registry leg. Comparing a rocket function with its built parent's function never established that either was patched. |
| MEASURED revised desk pass | `python tools/desk_c96_rover_subclass.py` emits its HEAD, build, module hash and reconciled leg list. Archived current run has 55 legs. Re-run if code/suite/source changed. No retail acceptance follows from this. |
| SOURCE: native unloading needs actual leaf cargo | `CargoTransporterNew:UnloadRovers` reads `cargo[rover.class]`; revised accounting transfers a fulfilled base request to the actual subclass line. Falsify with the suite's native unload-accounting leg. |
| INHERITED fixture | Retail 1.1.0.403908; Europe/ESA, Wildfire, Seeker `2000000261`, no Commander, UniversalRocket `1050`. Count/state probes must be refreshed after fixture changes. |

The earlier brief's flag-handoff diagnosis was an inference from an invalid "patched function"
claim. The source/desk loading-order finding supersedes it. The old optional closure-origin
probe was prepared but not observed; do not report it as run.

## Scope and evidence limits

C96 only: investigate any remaining failure in this repair and its native cargo lifecycle.
Other defects are filed, not fixed under this task. The release itself remains out of scope.
A launched expedition and correct return are live acceptance; a nonempty gather alone is not.
The panel may show Seeker 1/1 after substitution: preserving an apparent Commander amount would
be false accounting and would duplicate it on unload. No live save/removal verdict without a
retail observation. If the fixture is unavailable, record that dependency and retain this brief.

Before testing run the WORKFLOW probe sweep; the age rule is satisfied at the next playtest,
never used to refuse work. Read the newest retail file log; the owner says "flushed" when ready.
Do not ask for transcription. Preflight console lines with a Lua parser, one paste-safe line,
no `--` comments, `*r` for synchronous multi-statement reads. Record build and mutation scope.
Read presence from a running log; claim absence only after exit. MarsDebug is not retail evidence.

## Inherited fixture instructions

The following original fixture derivation is retained; do not re-derive it without a moved input.

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
