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

**SOURCE + MEASURED:** [Fix_MysteryTechMigration.lua](../../../tools/held/Fix_MysteryTechMigration.lua)
(built as `Fix_WildfireCureMigration.lua`; renamed and widened by the audit below)
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

`python tools/desk_wildfire_cure.py` (since renamed `tools/desk_mystery_tech_migration.py`) — **37/37 demands held**; the total is the
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

## Cross-vendor audit — 2026-09-16, fired on Fable (`prompts/F120_AUDIT.md`, consumed)

**Verdict: SHIP WITH CHANGES.** The mechanism, the platform reach and the
repair contract held under re-derivation; the fix was too narrow by its own
logic. Changes made, all desk-exercised, none retail-exercised:

1. **Widened from the cure to the whole `Mysteries` field.** The converter drops
   the field, not one tech; the archived 1.0.7 registry has **17** techs there
   (`LEGACY` line of the harness), the harness hides and recovers every one.
   Entrance = `MysteryTechRevealRemapping[id] or id`; the colony-mystery gate was
   dropped because `DefenseTower` has no `Mystery` preset property.
2. **Module renamed** `Code/Fix_WildfireCureMigration.lua` →
   `Code/Fix_MysteryTechMigration.lua`, id `MysteryTechMigration`; `items.lua`
   and `metadata.lua` follow, same position. `SRC:`/`DEFECT:` pin unchanged.
3. **Harness renamed and widened** to `tools/desk_mystery_tech_migration.py`,
   **85/85** ([evidence](../../archive/mystery_tech_desk_after_20260916.txt));
   `SMR_DESK_MODULE` lets a scratch variant be required to fail. Two
   one-guard-reverted variants each failed exactly one named leg.
4. **Entry amended** with the class, the completed-research case, the reach
   verdict, and the listeners the unlock reaches (`Mystery.lua:65` discovers and
   notifies `Mystery_N`), which the original contract did not mention.
5. **Release ledger:** `RELEASE_OUTBOX.md` had no Pending row for F120 despite
   its header rule; one was added.

**Reach (the owner's direction B):** public Steam builds went 1.0.7 → 1.1.0 with
nothing between (Steam news API, app 3215050, read 2026-09-16); the floor is
402200 and 1.0.7 saves are 396349 (EF-080). A Steam reporter's legacy colony is
refused before conversion, so **the fix does not answer Jäger's report**, which
stays open. Candidates for a fresh 1.1.0 colony that no desk leg can settle:
the reveal sits three game-hours plus a random delay after the infection
message (`Mystery 8.generated.lua:141-148`), the chain lives in the tree's
SPECIAL section, and `Unknown = true` nodes render unnamed only while locked.

| Negative result (audit) | Basis |
|---|---|
| The repair contract's "no-op" claims are false somewhere | **MEASURED refuted:** all nine no-op legs, the first-load ordering leg and the disabled-fix persistence leg held on the widened body |
| `LockablePresetsInitialized` is unset on a first legacy load, so the fix declines forever | **SOURCE refuted:** 1.0.7 stored it as a GameVar (`LockablePreset.lua:350-351`, archived); the 1.1.0 fixup `LockablePresetStatesToOwners` (`:783-798`) moves it onto the player before `PostLoadGame` (`CommonLua/Savegame.lua:808-811`) |
| Mystery techs were auto-discovered at colony start in 1.0.7, so every legacy save carries markers | **SOURCE refuted:** the field is `discoverable = false` (`Data/TechFieldPreset.lua:286-291`, archived); `InitResearch` discovers only discoverable fields |
| The other remapped chains (buried wonders) share the hole | **MEASURED refuted:** their field is `BuriedWonders`, preserved; the converter unlocks the final node directly, entrance still hidden. A shortcut in the player's favour; not filed |
| A public Steam build between 402200 and 403908 lets Steam saves reach the converter | **INHERITED refuted (feed, not sampled):** no such build in the Steam news feed; first 1.1.0 boot 2026-09-08 read 403908 |
| C69 / C79 / C92 / C97 share this defect | **SOURCE not reproduced:** different consumers; nothing new added to those entries |
| The recovery re-applies the reveal's popup and cost boost | **SOURCE, true and accepted:** neither is re-applied; the converter does the same for sibling groups |

Retail was not launched: a Steam retail load of a legacy save needs the
old-save block overridden, which EF-080 rules unattributable, and no 1.0.7
save with a revealed mystery tech exists on this machine (the `Saved Games`
folder holds 1.1.0-era saves only, listed in the audit transcript). The
reporter was not contacted.

**Owner ruling after the audit, same day: PULLED FROM THE SHIP SET** (checklist
187). The owner's reach figures decide it: about three quarters of subscribers
are on Steam, which refuses the 1.0.7 load before the converter runs; console
cannot do it; only a PC copy from the Paradox store could reach the repaired
state, and the owner's Steam copy cannot test it. The module moved to
`tools/held/`, unregistered; the harness still runs against it. The retained
value is the evidence above. Lesson for triage, recorded in memory: measure who
can reach the affected state before building, not after.

Executed model declaration: Claude Fable 5.1 (`claude-fable-5-1`), as reported
by the session environment. No sub-agents were used.

## Leg A of checklist 188 — RUN ATTENDED 2026-09-16: the fresh 1.1.0 path is HEALTHY

⭐ **Jäger's report is not explained by a failed reveal, an off-screen node, or a broken chain.**
Run with the owner at the keyboard on their live ESA/Wildfire colony, game 1.1.0.403908,
`mystery_id = TheMarsBug`, Main tree researched out, **0 tech points** at the baseline read.

⛔ **Not yet mirrored into `PLAYTEST_CHECKLIST.md` item 188** — a peer session held uncommitted
edits to that file at the time of writing. The marker update is owed.

**MEASURED, in order.**

| leg | command / action | result |
|---|---|---|
| baseline | `print(UIColony.mystery_id, GetTechState("WildfireCure_1", UIPlayer), UIPlayer.TechPoints)` | `TheMarsBug hidden 0` |
| reveal | `SA_RevealTech.SAExec{tech = "WildfireCure", cost = 90000}` — the scenario's own call (`Lua/Scenario/Mystery 8.generated.lua:145`) | no error |
| read-back | the eleven-node `GetTechState` loop | `WildfireCure_1 enabled`, the other **ten** `hidden` |
| visibility | opened the tech tree | ⭐ the node was **on screen with no panning**, in the MYSTERIES cluster; the owner zoomed only to photograph it |
| chain | 20 tech points granted, then each node clicked in turn | every link opened as its predecessor was taken, through to the final `WildfireCure` |

⭐ **The `.SAExec` form in the checklist is correct even though the scenario uses `:SARun`** —
`SA_RevealTech:SAExec` reads only `self.tech` and `self.cost`, which the dot-call table supplies
(`Lua/Sequences/SA_Gameplay.lua:1196-1215`). `MysteryTechRevealRemapping.WildfireCure =
"WildfireCure_1"` (`:1187-1194`) is why the reveal lands on `_1` and not on the parent node.

### Two claims made during the sitting and WITHDRAWN — ⛔ do not reason from them

- ⛔ **"The tooltip's `14,580` is a price the game charges instead of the scenario's 90,000."**
  **FALSE.** It is a **discount**, not a price. `TFormat.TechDiscountRollover` renders only for a
  boosted, unresearched tech, and its number is `MulDivRound(UIPlayer.TechPointCost, percent, 100)`
  (`Lua/TechTree.lua:1630-1645`). **MEASURED in play: `TechPointCost` = 72,900, boost = 20%,
  20% of 72,900 = 14,580 exactly.**
- ⛔ **"`ChangeResearchCost` discarding its `points` argument is a candidate defect."**
  **WITHDRAWN.** 1.0.7 did `status.cost = points` (archived tree `Lua/Research.lua:353-360`); 1.1.0
  replaces it with `BoostTech(tech_id, 20)` (`Lua/Research.lua:225-227`). Per-tech research prices no
  longer exist — `Research:TechCost()` returns `0` — so there is nothing for the argument to set, and
  the shim converts the intent into a working discount that is **displayed and actually paid**.

### How the 1.1.0 research economy actually works — inherit this, it was expensive to establish

- Research points accumulate toward the **next tech point**; the tree header renders
  `<AccumulatedResearchPoints>/<TechPointCost>` (`Lua/XDef/XTechTree.generated.lua:557`), and the game
  states it outright at `Lua/ResourceOverview.lua:412`.
- **Every tech costs the same flat `const.TechPointResearchCost` tech points and completes
  instantly** — `UIResearch` subtracts the point and calls `ResearchTech` on the next line
  (`Lua/TechTree.lua:1210-1213`). ⇒ ⛔ **A chain researched back-to-back with banked points is NOT a
  missing lock.** There is no research-over-time left to pace it.
- A boost pays out as a **refund of research progress after the purchase**:
  `if IsTechDiscounted(tech_id) then self:AddResearchPoints(GetTechDiscountAmount(tech_id)) end`
  (`Lua/TechTree.lua:1222-1225`), which `TryGainTechPoint` may convert on the spot. The queue preview
  mirrors the same arithmetic (`Player:AdvanceSimResearch`, `:913-937`).
- ⭐ **The cure is eleven tech points.** The nodes chain `WildfireCure_1 → _2 → … → _10 →
  WildfireCure` by `To` links (`Data/Tech.lua:6790-6890`), and the scenario waits on the **final**
  node before lifting the building locks (`Mystery 8.generated.lua:180-196`). At 72,900 research per
  point and rising, ⇒ **a player may experience the cure as unaffordable rather than unavailable** —
  that distinction belongs in any reply.

### What Leg A does NOT establish

- ⛔ **Not proof the node is visible for every player.** The tech tree does **not** auto-centre on
  open — that path returns early (`Lua/XDef/XTechTree.generated.lua:862-873`) — so it restores a
  saved scroll position. This was one player, one saved position, one resolution.
- ⛔ **The scenario payoff was not observed.** Because the reveal was force-called, the Trigger
  sequence is still parked at an earlier gate, so `RemoveBuildingLock("StorageMysteryResource")`,
  the Mechanized Depot unlock and the infection stop did not fire. Expected on a forced fixture.
- ⛔ **The organic trigger chain is untested.** That is Leg B, and §Leg B below names the gate that
  makes it worth running.

## Leg B — the organic chain, and the gate that makes it worth running

⭐ **The sharper target than "timing".** Mapped from `Lua/Scenario/Mystery 8.generated.lua:38-148`.
The Trigger sequence is `autostart`, so it is already running on any Wildfire colony:

1. **Blocks until ≥100 colonists** — `while not (CountObjectsByLabel(UIColony, "Colonist") >= 100)`, polled ~5 s.
2. Sleep `3750000 + rand(3750000)`.
3. `Msg("MysteryBegin")`, sleep `30000 + rand(60000)`.
4. **Spawns a surface anomaly** — `SA_SpawnAnomaly`, outside domes, within 25000 of a Building,
   `scan_msg = "Mystery8_AnomalyAnalyzed"`.
5. ⛔⛔ **`WaitMsg("Mystery8_AnomalyAnalyzed")` — BLOCKS FOREVER until a rover scans that anomaly.**
   ⇒ **A player who never scans it never gets the cure revealed at all.** This is the strongest
   candidate for Jäger's report that any leg has produced, and it is not a defect.
6. **Popup "Anomaly Analyzed"** must be dismissed.
7. Sleep `3600000 + rand(3600000)`; three colonists gain **Infected**.
8. **Popup "Wildfire: Infection!"** must be dismissed.
9. Starts `Rocket To Earth` and `Earth Infected Timeout`; sleep `10800000 + rand(3600000)`.
10. **`SA_RevealTech{tech = "WildfireCure", cost = 90000}`** — the same call Leg A made by hand.

⇒ Three player-dependent gates: the colonist count, **the anomaly scan**, and two dismissable popups.
Everything else is a timed sleep.

**Progress probe** — reads which sequences are live, so the run is measured rather than watched
(`GetSequenceListPlayer`, `CommonLua/Libs/Sequences/SequenceListPlayer.lua:589`; scenario id
`"Mystery 8"`, `Lua/Mysteries/TheMarsBug.lua:4`):

```
*r local p = GetSequenceListPlayer("Mystery 8") for _, n in ipairs{"Trigger","Init","Contaminated Lab","Infection Trait Spread","Rocket To Earth","Earth Infected Timeout","Cannot Be Prevented"} do print(n, p and p:IsSequenceRunning(n) and "RUNNING" or "-") end
```

⛔ **Leg B must start from a save taken BEFORE the Leg A reveal** — the owner took one. ⚠️ Read
`const.HourDuration` and `const.DayDuration` in-game rather than converting the sleeps by hand.
