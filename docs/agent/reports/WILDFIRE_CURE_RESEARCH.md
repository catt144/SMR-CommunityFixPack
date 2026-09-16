# Wildfire cure investigation — 2026-09-16

**Outcome:** [F120](../bugs/F120.md) repairs a lost legacy cure discovery on
load. The actual module and shipped Lua pass the desk recovery controls.
**The Steam reporter's specific cause remains unresolved.** Ordinary retail
Steam loading blocks the archived legacy-save revision; a fresh current-build
reveal succeeds in the sampled desk state. No retail game was launched.

Baseline: installed **1.1.0.403908 / Steam build 24995074**, checked with
`python tools/doccheck.py --emit-fingerprint` at `7974ddb`. The prompt's
repo-side fact scope was unchanged from `481bbd7` (`git diff --stat
481bbd7..HEAD -- docs/agent/bugs/ Code/`, empty at orientation). `git pull`
completed. Shipped sources were read only; archived sources were read only.

## What was built and how an affected save recovers

**SOURCE + MEASURED:** [Fix_WildfireCureMigration.lua](../../../Code/Fix_WildfireCureMigration.lua)
adds a synchronous PostLoadGame recovery. A Wildfire colony must have positive
legacy `tech_status.WildfireCure.discovered`, field `Mysteries`, and a fully
hidden current cure family. The handler restores `WildfireCure_1`, the same
entrance selected by the current scenario's reveal remapping.

It initializes newly introduced lockable presets before inspecting them and
retains their processed markers. It changes only vanilla discovery state:
no free research, points, crop unlock, scenario completion, new saved field or
saved thread. Partially researched, completed and otherwise reopened chains
are untouched. A changed remapping or unsupported lock-reader behavior declines.
Both metadata and Mod Editor item lists include the module in the same position.

**Recovery method:** enable the updated pack, load the affected save on a
platform that permits it, and research the restored chain normally. Saving
then preserves vanilla lock state. A new colony or mystery restart is not
needed for this defect. The module does not bypass Steam's old-save block.

**MEASURED ceiling:** the already converted synthetic fixture recovered;
another load was idempotent; vanilla load handlers with the fix disabled kept
the entrance open; paying through the chain released an already suspended
`SA_WaitResearch`. This establishes a recovery method on the shipped bodies.
It does **not** establish a retail serialization round trip, a live player's
tech-tree rendering, crop production, or the state of Jäger's save. The owner
required affected-save recovery, not prevention alone; no prevention-only
result is being presented as a successful fix.

## Findings and disposition

| Finding | Evidence and home | Disposition / reopening condition |
|---|---|---|
| Lost discovery during migration | **MEASURED**, [F120 cause](../bugs/F120.md#cause-and-reachability); shipped converter excludes `Mysteries` | Built and desk-exercised in `d004494`; retail recovery remains untested |
| Platform reach | **MEASURED**, shipped `ValidateSaveMetadata` with config lines 174–175; Steam blocks revision 396349 below floor 402200, non-Steam offers Load anyway | R2, platform-conditional; cannot explain ordinary Steam migration |
| Report-specific cause | **INHERITED**, Steam Jäger report; no mystery stage, save or log | Unresolved; reopen when report-specific stage or runtime evidence becomes available; no reporter request or owner sitting queued |
| Wider migration class | **SOURCE**, group inclusion list omits all `Mysteries` | F120 owns the proven Wildfire member; inspect another member if an affected scenario is sampled. No broader fix or new queue was created |
| Existing-save recovery is part of success | **OWNER**, follow-up during this investigation | Recorded in [checklist](../../PLAYTEST_CHECKLIST.md) and [ruling](../../archive/PLAYTEST_ARCHIVE.md#affected-save-recovery-requirement-2026-09-16); applies beyond F120 |
| Prompt freeze override | **OWNER**, authorised while teardown was underway | [Ruling](../../archive/PLAYTEST_ARCHIVE.md#wildfire-investigation-override-2026-09-16); folder freeze subsequently removed by `7d63900` |

The wider omission is a concrete migration-class lead. C69's in-progress wait,
C79's discarded exact cost, C92's unreachable technology and C97's tutorial
flags do not thereby become one defect: they have different failed consumers.
No repair to those entries was included. The current Wildfire scenario text
explicitly describes tech points and medical advancement, so restoring old
per-tech pricing would be a design change, outside this fix.

## Negative results that constrain the next investigation

| Lead | Result and basis |
|---|---|
| Fresh reveal leaves no available node | **MEASURED not reproduced:** actual `SA_RevealTech` makes the head enabled, map-visible and researchable with a point. Full synthetic chain purchases complete the final tech |
| Zero points hide the node | **MEASURED refuted for the sampled state:** revealed head remains visible but unaffordable |
| Medical advancement cannot research hidden nodes | **MEASURED refuted:** shipped force-research opens a migrated hidden head and reveals the next node; grants complete intermediates without spending points |
| Medical grants finish the final cure for free | **MEASURED refuted:** after the intermediate grants the final is enabled, unresearched and still requires a point |
| Any migrated hidden family is permanently stuck | **MEASURED refuted:** a remaining medical grant can reopen it. **SOURCE** exhausted SpeedUpResearch loops have no remaining grant; retail loop exhaustion was not sampled |
| `Field = "Special"` blocks the wait | **MEASURED refuted:** the actual researched-state wait returns without using Field. **SOURCE** old saved field is `Mysteries`, from old AddTech, not the editor label |
| Rocket-to-Earth sequence completion gates reveal | **SOURCE:** generated Trigger starts the rocket and timeout sequences without waiting for completion, then sleeps and calls the reveal (`Lua/Scenario/Mystery 8.generated.lua:128-148`). Earlier anomaly/message stages and elapsed mystery time were not sampled in retail |
| `Unknown = true` conceals the revealed head's identity | **SOURCE:** the unknown icon/title branch is inside `state == "locked"` (`Lua/XDef/XTechNode.generated.lua:203-209`); the sampled revealed head is enabled. No visual rendering test was run |
| Mystery research is in a missing UI section | **SOURCE:** `TechGroupToSection` maps `Mysteries` to the section whose displayed label is SPECIAL (`Lua/TechTree.lua:3-14`). Navigation/off-screen position in the reporter's UI was not sampled |

The prompt's already-refuted prerequisite/reveal/remapping hypotheses were
inherited behind the unchanged baseline, not independently reopened. The
availability harness exercises that path as a positive control for migration.

## Verification and fixture limits

`python tools/desk_wildfire_cure.py` — **37/37 demands held**; the total is the
sum of the named PASS members in
[after evidence](../../archive/wildfire_cure_desk_after_20260916.txt).
[Before evidence](../../archive/wildfire_cure_desk_before_20260916.txt) preserves
the initial unpatched investigation. Each log records its command and HEAD;
source bodies are extracted by `deskbench` and printed with their SHA-256.
The after run was made against `74e3f16` plus the pending F120 changes, committed
as `d004494`; subsequent pre-commit edits changed comments only.

Shipped lock initialization, state reading, prerequisites, unlock, research,
grant, wait and migration bodies execute under Lua via lupa. The fixture narrows
the preset-processing universe to the actual Wildfire family, with a separately
initialized breakthrough control. Class flattening and scheduling are modeled;
presentation, notifications, accounting and crop effects have explicit sinks.
RP refunds are excluded; tech-point spending is the shipped decision. Synthetic
old status is created by the extracted old AddTech using the source-verified
old preset group. No fixture is represented as a real save.

During harness construction, the first chain test failed because its PlaceObj
shim had not decoded positional `TechTreeConnection` properties. Correcting the
shim restored the actual links; this was **not a game defect**. The first
full-registry fixture also encountered compiled prerequisites that the desk
class shim cannot compile, so processing was scoped to the cure family. These
limitations must survive any reuse of this harness.

`python tools/parsecheck.py --quiet`,
`python -X utf8 tools/bodycheck.py --module WildfireCureMigration --all`,
`git diff --check` and `python tools/doccheck.py` passed before the fix commit.
The source pin and expression match; the runtime repair still relies on the
named dependencies and must be reconsidered if they change. A green manifest
does not prove future compatibility.

## Close-out

The invoked one-off `prompts/WILDFIRE_CURE_RESEARCH.md` and its map row are
retired together with this report. No reply was drafted, nobody was contacted,
no save was requested, and no game/source archive was modified. Source and desk
results are preserved; retail recovery and the original Steam symptom remain
explicitly unconfirmed. No uploaded release is claimed.

Task commits: `fae8c9d` owner override; `80c9ebc` finding, initial harness and
recovery requirement; `d004494` recovery module, extended controls and entry.
Shared-tree changes `7d63900` (freeze removal) and `74e3f16` (C97 work) were
identified by diff and left outside this task's commits.

Executed model declaration: Codex / GPT-6, as supplied by the session
instructions. A more specific serving-model identifier is not exposed in this
transcript. No sub-agents were used.
