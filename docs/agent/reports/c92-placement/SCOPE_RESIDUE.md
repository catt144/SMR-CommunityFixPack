# C92 scope, production semantics and residue

Report-only contribution, 2026-09-13. No module built, game launched, account
changed, or save edited. Parent report: [C92_PLACEMENT](../C92_PLACEMENT.md).

## Refutations first

**SOURCE + MEASURED offline: the previous +44% water-production claim is false.**
The two effects target different production paths. The ordinary underground
Water Extractor's `water_production` modifier gives +20% of base production;
the hardcoded `SingleResourceProducer` multiplier acts on stockpiled-resource
components. Water flows through the water-grid producer, not through that
component calculation. With a 5000 base and no other modifiers, both respective
paths produce 6000; water does not produce 7200.

**SOURCE + MEASURED offline: permanent/unremovable is too strong.** Disabling a
mod does not automatically undo researched state or applied vanilla modifiers,
but both can be removed explicitly. Clearing the researched flag stops the
hardcoded bonus; removing the existing label modifier also restores the water
output. Those are separate cleanup operations. They cannot undo water or ore
already produced and spent.

**MEASURED offline: an obsolete preset and an absent preset are different.**
Setting `Obsolete=true` while retaining the preset leaves the multiplier alive.
Deleting the preset while retaining its researched flag makes the unchanged
hardcoded consumer error at `BuildingComponents.lua:1362`. This is an offline
Lua error, not evidence of a retail crash or of a vendor patch that has shipped.
The scenario requires a future deletion without corresponding consumer/flag
migration.

## Evidence identity and limits

Commands run at repo HEAD `ccd4ff58762558ba79eef6065121d22ec138bea2`, installed
Steam app **3215050**, manifest `buildid=24995074`, source baseline
**1.1.0.403908**:

```text
python docs/agent/reports/c92-placement/scope_controls.py
python tools/desk_c92_achievement.py
```

The first command loads shipped bodies through the repository's existing
`tools/luafn.py` extractor into lupa, emits each source span and SHA256, and
passes **14** controls. The second existing harness passes **15/15** demands,
including ordinary/repeatable incompletion and the actual group-iterator
callback. The production result excerpt is [scope_controls.txt](scope_controls.txt).
Fixtures, shims and code are in [scope_controls.py](scope_controls.py).
Parent's [PACK_TRUTH.json](PACK_TRUTH.json) records the packed-source comparison.

The production harness supplies an abundant deposit, a working unupgraded water
extractor, no direct constant override, an Extractors-label membership fixture,
and a recording water grid. It uses the **actual** label effect, label removal,
modifier arithmetic, water callback, water supply and generic production
bodies. It does not simulate a city, geology, C++ supply-grid scheduling,
serialization, DLC ownership, or achievement providers. Its `IsKindOf` shim
only omits the optional modifier display identifier; it does not control any
production/refusal decision. No claim of attended or retail verification follows.

## Q1: recommendation

**INFERRED recommendation: retain the narrow achievement exemption as the
mod-side repair; send the inaccessible production technology to the developer.**
The reported achievement barrier is established independently of any placement
or balance choice. A targeted exception can preserve ordinary and repeatable
first-completion requirements and leave colony production unchanged. Finishing
the tech is plausible restoration, but its unlock dependency, position and
access timing are not established by this subtask. A normal research purchase
would also replace a law with upkeep by a lasting technology benefit: that
access/economy decision belongs in the scope choice.

The +44% allegation supplies **no** reason to reject restoration. Likewise,
vanilla-data residue does not automatically prohibit a fix under FIX_POLICY
3a. The sound reasons for the narrower recommendation are the proven player
harm, avoiding an invented access decision, and a smaller migration obligation.
No full restoration has been built or refused by policy in this pass. An owner
choice to restore it can proceed to design and tests; it must not inherit the
refuted double-application argument or call a future cleaner its disposition.

**INFERRED intent:** retirement of the law, the replacement preset and its live
consumer make unfinished integration a strong explanation. They do not reveal
the authors' mental state or logically exclude a temporary intentional bench.
Label that conclusion INFERRED, not SOURCE.

## Q3: what the effect actually covers

All current source spans below refer to `Project Spark/ModTools/Src`.

| Evidence | Consequence |
|---|---|
| SOURCE `Data/Tech.lua:10635-10660`: underground extractors wording; 20 parameter; effect label `UndergroundWaterExtractor`, property `water_production` | SOURCE The declarative effect is the water half of the implementation. The parameter comment is only `Production Buff`; this preset has no authored `Comment`, `TODO`, `SortKey`, `Condition`, or `save_in`. |
| SOURCE `Lua/Buildings/BuildingComponents.lua:1356-1366`: parent must be in `Extractors`, underground environment, researched flag | SOURCE + MEASURED offline Stockpiled resource production gets its own +20% multiplier. The source does not restrict it to a Water Extractor class. |
| SOURCE `Lua/BuildingTemplate/WaterExtractor.generated.lua:10`: its stockpile resource is `WasteRock`; water is the separate `water_production` property | SOURCE Treating this `SingleResourceProducer` as the water-output path is the earlier error. |
| SOURCE `Lua/Buildings/WaterExtractor.lua:56-64`, `:73-86`, `:105-129` | SOURCE Underground objects join the water label. SOURCE + MEASURED offline Modifier changes update grid production directly; actual supplied water goes straight to extraction/waste generation without the hardcoded tech multiplier. |
| SOURCE `Lua/Modifiers.lua:41-104` | SOURCE Percent modifiers on the same property add. +20 means +20% of its current base, not necessarily 20% above an already upgraded output. |
| SOURCE `Lua/MarsGameEffects.lua:248-287`, `Lua/LabelContainer.lua:59-78` | SOURCE This non-stackable effect uses the effect object as its key. SOURCE + MEASURED offline Reapplying the same effect replaces the old modifier; it does not compound another +20%. |

**SOURCE conclusion:** code and text are consistent with a buff to underground
extractors generally, implemented through two resource systems. Do not narrow
the text to water or delete either half on a supposed duplicate-effect theory.
The hardcoded branch also has no `resource_produced ~= "WasteRock"` guard; do
not infer that its own reach is only the desirable ore output. Measuring every
byproduct, prediction UI and deposit-depletion interaction is outside this pass.

**SOURCE history:** archived 1.0.7 `Lua/Buildings/BuildingComponents.lua:1081-1089`
checks the law and underground environment, without the new Extractors-label
guard. The archived law at `Data/LawDef/LawDef-Economy.lua:1090-1106` has the
same +20% wording and a `NoUndergroundAndAsteroids` prerequisite, plus upkeep.
That old body establishes a broader underground stockpile-production path,
not a measured old water bonus. It must not be called byte-for-byte equivalent
to the current production scope. Old water output does not pass through that
generic component calculation either.

**SOURCE migration:** current `Lua/Factions/Laws.lua:773-775` removes the old
active law. The implication for a carried law is conditional on successfully
migrating a save. This pass did not measure such a migration, and STATE records
that normal 1.0.7 saves cannot load on 1.1.0. Do not present carried-save loss as
a new player observation. The current branch's unreachable bonus in new
colonies is the relevant source-derived claim.

**SOURCE missing rule condition:** unlike `UndergroundDeepMining`
(`Data/Tech.lua:10571`) and `UndergroundWaterExtraction` (`:10709`), this preset
has no `Condition`; it inherits `return_true` (`Lua/TechTree.lua:264-265`). Its
old law condition was explicitly `not IsGameRuleActive("NoUndergroundAndAsteroids")`.
Restoring that guard is a reasonable proposal for the developer, **not proof
of intended tree placement**. `Research:TechAvailableCondition` calls the
condition (`Lua/Research.lua:78-80`), but the achievement's group iterator and
filter do not. Merely adding a condition therefore does not repair the
achievement census.

`rg -n UndergroundExploitation <Src>/DLC` finds no source DLC reference. This
is a source-tree negative only; the parent's packed pass supplies the compressed
data control. No DLC-only placement or ownership requirement was established.

## Q5: builder-ready achievement contract

This is a **proposed implementation contract**, not a built module or a passed
new self-check. The existing offline achievement harness establishes the
predicate seam and its controls; a future builder must implement and test the
decline cases below.

1. Keep vanilla's listener intact. Add a synchronous local recheck called by an
   additive `OnMsg.TechResearched` and by `OnMsg.PostLoadGame`. A repeat completion
   must be allowed to recheck: the current listener's `first_time` early return
   otherwise strands the reporter's completed save. `PostLoadGame` is after
   `LoadGame` and fixups (`CommonLua/SaveGame.lua:799-811`). The research preview
   queue clears on `LoadGame` (`TechTree.lua:1068-1070`), and normal research
   commits clear it before replay (`:993-1007`). No game-time sleeping thread is
   needed.
2. Treat **registry not ready** as deferred/unknown, never as an absent-preset
   positive. Install no waiver from that observation. At the post-data apply
   seam, an initialized registry with the target genuinely absent is a **decline**.
   Recheck live registry state at every event; do not permanently cache the
   preset object as proof. Verify initialized player/colony and lock state before
   any achievement call. Empty/malformed registries must never yield a vacuous
   all-complete award.
3. Match this one known orphan: exact id and current ordinary group, base-game
   counted status, nonobsolete, nonrepeatable, researchable, default hidden,
   `Unknown=true`, and no connections. Read the final graph, including incoming
   connections or graph postprocessing, rather than the unprocessed source
   property alone. A new connection, changed group/counting status, visible
   default, retirement or absence **declines**. At the live call also decline if
   `GetTechState` is not hidden, `IsVisibleOnMap` is true,
   `CheckUnlockPrerequisites(UIPlayer)` is true, or `UIPlayer:CanResearch(id)`
   is true. Probe functions must be present and return an understood result;
   throws/unknown cannot mean apply. **Normalize each function's documented
   false-like results separately:** the known orphan's
   `CheckUnlockPrerequisites` returns literal `false` at `TechTree.lua:454-457`,
   and `IsVisibleOnMap` returns a boolean. In contrast, `Player:CanResearch`
   legitimately returns `nil` for insufficient tech points (`:868-874`). If
   verified numeric `TechPoints < const.TechPointResearchCost`, that nil is an
   understood affordability refusal, not an unknown or evidence of an orphan.
   It may coexist with the independent hidden-state/prerequisite proof. With
   enough points and the already-verified existing researchable preset, require
   its boolean result; an unexpected nil declines. Unknown initialization,
   missing methods or a nil prerequisite-check result still decline. The final
   composed behavior probe returns literal `true` only when all these decisions
   succeed. Tests run against fresh disposable fixtures, never by
   unlocking/researching the real colony.
4. Use the real `UIColony:IsTechGroupResearched(group_id, filter)` seam with
   vanilla's tracked group set. Its filter receives **`tech, group`**, where
   `group` is the preset-group table; it is not a group-id string
   (`CommonLua/Preset.lua:1802-1815`). Preserve
   `(tech.save_in or "") == "" and not IsInitiative(tech.id)` and exclude only
   the identity checked in step 3. Also require a census with no exemption to
   fail, the exemption census to pass, and the checked target to have actually
   been visited and counted. This both pins the barrier and avoids treating a
   removed cluster as completion. Retain the repeatables' first-completion
   requirement and do not add Terraforming to vanilla's tracked list.
5. Finish through `AchievementUnlock("ResearchedAllTechs")`. Never write
   `AccountStorage` directly, override blockers, or call a provider directly.
   `CommonLua/Classes/Achievement.lua:65-100,140-152` preserves platform, title,
   tutorial, DLC and already-unlocked checks. This is the normal achievement
   award requested by the repair, not permission to attempt it in this report.

The event code must not assume `OnMsg.TechResearched` fires after all effects:
`TechTree.lua:1221` emits it before `EffectsApply` at `:1228`. This repair only
reads research state, which is already recorded at `:1213`; it does not need
production effects to have run. It should also decline while an uncommitted
`TechnologiesUndoQueue` remains, rather than credit preview-only completion.

**PROPOSED / INFERRED** builder acceptance cases, using a recording-only
achievement sink; none is a newly executed implementation test:

| Fixture change | Required result |
|---|---|
| INFERRED Current registry; only verified orphan missing; initialized post-load | Exactly one request; no tech unlock, research, modifier, or colony-state write |
| INFERRED Same fixture; repeat `TechResearched(..., false)` | Recheck succeeds despite first-time flag; normal provider deduplicates |
| INFERRED Same valid orphan fixture, but zero tech points and the expected `CanResearch` nil | Still permits the achievement recheck; inability to afford research does not nullify the independent orphan proof |
| INFERRED One ordinary tech incomplete, or one repeatable never completed | No request |
| INFERRED Another hidden tech incomplete | No request; there is no general hidden-tech exemption |
| INFERRED Orphan gains a graph connection, becomes visible/enabled, or its live prerequisite check succeeds | Decline the waiver |
| INFERRED Orphan becomes obsolete or disappears after registry initialization | Decline without nil dereference; leave normal achievement handling intact |
| INFERRED Tech/TechGroup registry not initialized or lacks a tracked cluster | Defer/decline; no vacuous award |
| INFERRED Target absent from iterator though `Techs[id]` still points at a stale object | Decline |
| INFERRED Game rules/cheats/platform prevent normal award | Provider/title path still refuses; do not clear blockers |
| INFERRED Preview-only completion; live methods missing/throw/return unexpected nil or unknown | No request |

**Bound:** these tests detect changed data and already-effective unlock routes.
They cannot prove that a future vendor has added a delayed scripted grant while
leaving all inspected preset and current hidden-state behavior identical. No
generic behavior test can distinguish identical observations. Keep the
ordinary shipped-source update review; do not promise universal automatic
retirement from four field comparisons alone.

## Per-site residue inventory for a hypothetical finish route

These are design findings, **not release dispositions for a built module**.
The full finish route is not recommended or implemented here, so no site is
preassigned to a hypothetical cleaner. FIX_POLICY 3a requires attempting the
available in-pack repair before such a handoff.

| Site | Persistence and exit consequence | Available remedy / bound |
|---|---|---|
| Runtime preset position, icon, connection, defaults | SOURCE Preset/class edits alone do not serialize as a new mod class/function. However vanilla unlock processing writes player state. | INFERRED Restore original runtime fields on withdrawal; separately handle resulting lock state. A preset-only claim does not discharge the next rows. |
| `Player.PresetLockStates.Tech[group][id]` | SOURCE Visibility/unlock data can outlive mod removal. INFERRED A later group move may leave old keyed state. | SOURCE `ResetLockablePresetState` clears and recalculates a target (`LockablePreset.lua:402-414`). INFERRED Ownership/provenance and correct current group must be known before resetting somebody's official progress. |
| `Player.tech_researched[id]` | SOURCE Survives removal and drives the all-vanilla stockpile consumer. SOURCE + MEASURED offline `ResearchQueue:IsTechResearched` checks the flag without validating the preset. | INFERRED Clear only a proven mod-owned completion during a deliberate retirement migration; refund/counter handling is a design decision. The developer can instead officially adopt the research and retain it. |
| Colony label modifier plus building `modifications.water_production` | SOURCE Water modifier survives independently of researched flag; affects current and future label members. MEASURED offline Clearing the flag alone retains the fixture's water modifier. | SOURCE + MEASURED offline `SetLabelModifier("UndergroundWaterExtractor", actualStoredEffectKey, nil)` subtracts/recalculates existing members and clears the container entry. SOURCE This also removes future label application. INFERRED Do not delete only the colony dictionary; if the preset disappeared, recover the stored key by verified effect identity/content, rather than assuming the new preset has the old object identity. |
| Tech point spent, count/history/notifications, earned resources and consumed deposits | SOURCE Vanilla consequences of the purchase and ongoing production. INFERRED Uninstall is not time reversal. | INFERRED Disclose retained ordinary history. A compensating refund is possible only with provenance. Resources already used cannot be selectively rolled back safely. No destructive historical rollback is proposed. |
| Account achievement | SOURCE Account/provider state, not colony save residue, for either route after a legitimate award. | INFERRED Expected persistent result; do not revoke on uninstall. |

**SOURCE caution:** `Tech:UnresearchSelectedCheat` clears the researched flag
(`TechTree.lua:365-391`) and invokes `OnRevertEffect` only where supplied.
`Effect_ModifyLabel` has no such callback in the examined body. That cheat by
itself does not remove this water modifier. The normal explicit modifier API
does, as the offline control measures. No save-rescue artifact is built here.

The relevant vendor scenarios are: officially connect the same technology
(existing completion may remain legitimate); mark it obsolete while retaining
the consumer (bonus remains); remove/rename the preset without cleaning the
consumer and flag (conditional Lua error); or migrate effects and state together
(potentially clean). The current tree does not determine which future scenario
the developer will choose.

## Not opened / not measured

- No real production run, saved finish-route colony, disable/load leg, account
  award, or console-platform leg.
- No UI hit testing, geometry placement, icon art or external developer intent
  evidence in this contribution; sibling contributions own those questions.
- No exhaustive byproduct/depletion/prediction-UI audit; no claimed water +44%.
- No full serialization trace for an absent preset's stored effect-object key;
  removal is measured in an in-memory fixture, persistence remains source-derived.
- No official migration of a 1.0.7 colony; the normal branch-load limitation
  remains in force.
- No newly implemented callback/decline self-check or release module; the
  acceptance matrix above is work for the builder if the owner selects bypass.
