# Game 1.1.0 "Services & Science" + *Feeding the Future* — impact on the pack

Written 2026-09-08, the day the patch shipped. Source-read only; **nothing here
has been confirmed in a running game.**

> ⚖️ **THE EVIDENCE RULE THIS REPORT IS BUILT ON (owner, 2026-09-08).**
> Anything Haemimont's patch notes call "Fixed" is a **CLAIM, and a claim is
> FALSE until we confirm it ourselves.** This report therefore keeps two
> registers strictly apart and never lets the second promote into the first:
>
> - **FACT** — something *we* read in the shipped 1.1.0 Lua on this machine,
>   with the file and the control that refuted the alternative.
> - **CLAIM** — something the patch notes assert. Recorded only so we know what
>   to go and test. ⛔ **No fix is retired, no entry is closed, and no `status`
>   moves on the strength of a patch note.**
>
> This binds the whole re-verification effort, not just this document.

## 0 · What happened, and the one thing that is already irreversible

Two Steam builds landed 2026-09-08: **24995074** (the free *Services & Science*
update, version **1.1.0**) and **24997558**. *Feeding the Future* is the first
paid DLC.

⚠️ **The rig auto-updated before anyone decided it should.**
`appmanifest_3215050.acf` reads `buildid 24995074`, `StateFlags 4`,
`LastUpdated` = 2026-09-08 09:38 UTC. Consequence, and it is not undone by
choosing anything now:

- **`ModTools\Src` has been overwritten.** 2747 of its 4715 `.lua` files carry
  today's mtime. The tree is 1.1.0 source.
- **Every `file:line` citation in `bugs/` and `facts/` was written against
  1.0.7.396349 and now points into a different file.** The citations are not
  wrong *about 1.0.7* — they are simply no longer resolvable against what is on
  disk. ⛔ Do not "correct" a single one of them in place; the entries record a
  defect in a stated version (`EF-014` pins it).
- **The 1.0.7 comparison base is gone from this machine.** Steam still offers it
  (below), but until someone re-downloads it, no A/B against 1.0.7 is possible.

**1.0.7 is still available on Steam** — the DLC announcement documents the route:
Library → right-click *Surviving Mars: Relaunched* → Properties → Game Versions
& Betas → select **1.0.7** (and *Default Public Version* to return). That is a
**dev claim about a store surface**; per the route-check rule it is not "you can
do this" until someone walks it. It is the subject of decision **98**.

## 1 · FACT — the mechanical sweep of every declared target

Method, so it can be re-run and challenged. `tools/harvest_wrap_targets.py
--list` yields the pack's declared `{class, method}` self-check targets;
`{global}`, `{path}` and bare `{class}` specs were harvested separately by grep
because that tool deliberately excludes them, and an under-sweep is the
expensive error. Each symbol was then looked for across the 1.1.0
`ModTools\Src` tree (4715 files).

⚠️ **What the sweep does and does not measure.** It measures **existence**. It
cannot see a function that still exists and now *means* something different —
which, given that this patch replaced the research and services systems
wholesale, is the larger risk and is §3's subject.

### 1a · Class/method targets — 106 of 107 intact

| target | module | finding |
|---|---|---|
| `Colonist.UpdateSatisfaction` | `Fix_TouristSatisfaction` (F09) | **GONE from the whole tree.** |

All 106 others still resolve on their declaring class. Two names the first pass
flagged were **refuted as static-analysis artefacts** and are fine:

- `PropertyObject.GetProperty` — defined by assignment, not `function`
  (`CommonLua/PropertyObject.lua:749`, `PropertyObject.GetProperty =
  PropObjGetProperty`).
- `HolidayRating.RewardApplicants` — present at `Lua/HolidayRating.lua:87`;
  `HolidayRating` is a plain table (`:1`), never a `DefineClass`, which is why a
  class-definition scan missed it.

### 1b · Global and const specs — 5 globals and 3 consts are gone

| symbol | module (entry) | verified absent |
|---|---|---|
| `GatherTransportableResources` | `Fix_LowStorageWarning` (F12) | 0 files, whole tree |
| `GetCommandCenterLifeSupportGrids` | `Fix_LowStorageWarning` (F12) | 0 files |
| `GetGridGlobalStorage` | `Fix_GridGlobalStorage` (F22), `Fix_LastTransmissionStorage` (F75) | 0 files |
| `PlanetaryAsteroidVisitPossible` | `Fix_AsteroidLanderAvailable` (F94) | 0 files |
| `RainsDisasterLoop` | `Fix_RainsDeadlock` (F81) | survives only as the *name* of a savegame fixup, `SavegameFixups.RainsDisasterLoopToRepeat2` (`Lua/TerraformingDisasters.lua:483`) — the global itself is gone |
| `const.MinDaysMaintenanceSupplyBeforeNotification` | `Fix_LowStorageWarning` (F12) | 0 files |
| `const.MinDaysFoodSupplyBeforeNotification` | `Fix_LowStorageWarning` (F12) | 0 files |
| `const.UnreachablesCleanupDeltaT` | `Fix_DroneUnreachableForever` (F55/F57) | 0 files |

**The control for the const rows**, because absence is the weak kind of
evidence: consts are declared by `DefineConstInt` in `Lua/_GameConst.lua`.
Group-mates of the missing three are still there (`ColonistMaxDomeWalkDist`,
`ColonistMinDistToIgnorePassage`), and the three appear **nowhere in the tree**,
while an engine-side const used as a counter-control (`HoursPerDay`) is absent
from `_GameConst.lua` yet present in 20 files. So the three are removals, not a
grep artefact. ⚠️ Residual: `Src` is the modding source drop; a const defined
only in packed binary data would not show. The runtime read in §4 settles it.

Nothing in `Code/` references any removed **tech or law** id
(`AdvancedMineralComposites`, `SelfSufficientLighting`, `DecommissionProtocol`,
`BirthRestrictions`, `Outsourcing`, `AdditionalSponsorResearch`): 0 hits.

### 1c · FACT — the failure mode is a clean self-disable, not a crash

Every one of the missing symbols sits **inside a `SMRFixPack.Require` gate**.
`Require` (`Code/00_Core.lua:117-166`) returns a reason string and sets
`update_suspect`, and the module does not apply. So on 1.1.0 these **6 modules
switch themselves off and say so in the boot log**:

`Fix_TouristSatisfaction` (F09) · `Fix_LowStorageWarning` (F12) ·
`Fix_GridGlobalStorage` (F22) · `Fix_RainsDeadlock` (F81) ·
`Fix_AsteroidLanderAvailable` (F94) · `Fix_DroneUnreachableForever` (F55/F57)

**`Fix_LastTransmissionStorage` (F75) was investigated as a crash risk and the
suspicion was REFUTED.** It has no `Require` gate and installs a closure that
calls `GetGridGlobalStorage` at *evaluation* time — which would throw, since F22
is what supplies that global and F22 now self-disables. But the closure is only
installed when `find_grid_check` finds a node of class
`ScriptCheckGridGlobalStorage` (`Fix_LastTransmissionStorage.lua:82-90`), and
that class **no longer exists anywhere in 1.1.0** (0 files). 1.1.0 rewrote those
faction likes: the test now sits in `Condition` already (so step (a) moves
nothing) and evaluates a new `ScriptFunc_DomesGridStorage` through a new
`ScriptCheckDomesGridStorage` (`Data/FactionDef/LastTransmission.lua:110-116`).
The pass therefore reaches `stats.seen > 0, moved = 0, retargeted = 0` and takes
the **benign latch** branch. No closure, no throw.

**Net: 73 of 80 modules keep every gate they declare; 6 self-disable; 1 latches
benign.** ⚠️ **"No crash path" held only until the sweep was widened from `Require`
specs to CALL SITES — see §6b and [[F113]]. Read that before trusting this §.** ⛔ This is a source-read prediction. The only valid read of what is
actually active is the live `fix pack present: N/N` line and
`SMRFixPack.ListFixes()` — §4.

### 1d · FACT — the pack is not flagged incompatible, by exactly one integer

1.1.0 sets `ModMinLuaRevision = 350453` (`CommonLua/Modding/Mod.lua:15`). Our
`metadata.lua` declares `lua_revision = 350453`. `ModDef:IsObsolete()` is
`self.lua_revision < ModMinLuaRevision` (`:915`) — a strict `<` — so we are
**not** obsolete, and `ModsUIIsModCompatible` (`UI/ModManager.lua:230-234`)
passes on `version >= ModMinLuaRevision and version <= LuaRevision`. Players get
no "not compatible with the current game version" prompt, and saves do not mark
the pack obsolete (`SavegameMetadata.lua:99`).

⚠️ **We are sitting exactly ON the floor.** Any future patch that raises
`ModMinLuaRevision` by one flips all three of those at once. This is now a thing
to check on every game update, not a settled property.

## 2 · CLAIM — what the notes say they fixed, next to what we ship

⛔ **Read this table as a to-test list, never as a to-retire list.** Every right
column is a Haemimont assertion we have not tested. A fix of ours that "looks
superseded" stays shipped and stays `fixed` until *our* A/B says otherwise —
and the pack is defensive by construction, so a redundant fix is usually a
no-op, while a wrongly retired one is a regression we hand to players.

| our entry | the patch-note CLAIM | why it is not a verdict |
|---|---|---|
| **F81** rains-loop deadlock | a savegame fixup named `RainsDisasterLoopToRepeat2` exists; "Dust Storms still happening despite 100% Atmosphere" fixed | The *global* F81 wraps is gone and the module self-disables — but "restructured" is not "the deadlock is gone". Untested. |
| **F75** Last Transmission storage opinions inert | — (no note) | 1.1.0 demonstrably rewrote these likes (§1c). Whether the *defect* (opinions never counting) is gone is unmeasured. |
| **F93** dust-devil scheduler reads the wrong map | "Dust Storm effects now start only on maps that actually have them" | Adjacent wording, different mechanism. Not the same bug until shown. |
| **F90** cross-map (elevator-merged) grid break | "Drones building an Elevator would path to spots on another map" | Same *family* (cross-map leakage), different site. |
| **F44 / F91 / F64 / F66** track + station | "building a Train Station over an existing Track deleted the Track elements next to it" | Overlapping zone; our four are distinct defects. |
| **F69** manual landing dumps return fuel | new "Carry return trip fuel" toggle | A new toggle is not a fix to the dumping path. |
| **F71** auto-export fills alphabetically | new manual-mode export toggles | The note explicitly says amounts cannot be tweaked in manual mode. |
| **F43** layout construction bypasses tech locks | "Self-sufficient Domes could be constructed with missing life support" | Adjacent. |
| **F53 / F52 / F73** colonist death + shelter | "Colonists dying from Hypothermia while on an Expedition" | Adjacent. |
| **F58 / F59 / F60** residence + free space | "residences in the Underground were not counted when ordering a Passenger Rocket" | Adjacent. |
| **F12** low-storage warning | Food now **decays 4%/Sol**; the DLC adds Delicacy resources | Not a fix claim — a mechanic change landing squarely on this fix's subject. |
| **F110** Jumbo Cave waste-rock wedge | RC Dozer now searches a larger radius for Waste Rock, stops dumping it on the ground, clears cave-ins in automated mode | Our target `ConstructionSite.TestBlockerClearenceProgress` survives. Whether the wedge still reproduces is the open question. |
| **F09** tourist Satisfaction | "Removed the Tourist-exclusive Satisfaction Stat" | ⭐ The one row where a **FACT** (§1a: the method is gone) and the claim agree. The defect cannot exist in 1.1.0 because the stat does not. |

## 3 · The larger risk the sweep cannot see: redesigned systems

These fixes keep every declared target and will apply normally — into systems
whose semantics the patch rewrote. Existence proves nothing here.

- **Services redesign** (visits → aggregated per-Dome effects; Comfort/Morale
  gain a *Target*; capacity scales with open workshifts; most workplaces now
  drain stats): **F04** `Colonist.ShouldLeaveForWork` · **F20** Morale/Comfort
  tooltip · **F108** and **C39** `Workplace.GetWorkshiftPerformance` · **F92**
  `TraitPreset.AddDomeColonistsModifier` / `LabelContainer.SetLabelModifier` ·
  **F14**, **F60** dome stats and free space.
- **Research redesign** (tech tree replaced by a hex Tech-Point board, ~50 new
  technologies): **F18**, **F25**, **F41**, **F43**, **F15**.
- **Landscaping** (Drones can no longer landscape at all — RC Dozer only; times
  +15%; "Change Surface" 50% faster): **F33** (a *drone* landscaping crash),
  **F34**, **F30**, **F105**, **F107**, **F110**.
- **Supply grids** now shut down *all* consumers on an unbalanceable shortage:
  **F90**, **F27**, **F22**, **F75**.
- **Rockets and landers** (new workflow, toggles, 3-second grace period, Space
  Elevator automated-only): **F67**–**F72**, **F94**, **F50**.
- **Food** gains 4%/Sol decay and the DLC adds Delicacy resources: **F12**.

⚠️ **`Fix_MeteorFrequency` (F02/F88) deserves its own line.** Meteors were
rebalanced (less Metal, can now drop Rare Metals and Exotic Minerals). F88 was
*our own* defect in the timer-restart path. Meteor work is organic-playtest
gated (`STATE`), so it cannot be cleared by a source read.

## 4 · The reads that would settle this, in order

1. **`SMRFixPack.ListFixes()` and the boot `fix pack present: N/N` line on
   1.1.0.** The highest-value read in this document. It converts §1c's
   *predicted* six self-disables into a measured list and would expose any
   module the source sweep missed. ⛔ Counts are READ, never assumed. The
   STALE-PROBE GATE is currently **CLEAN** (`doccheck`: `TEMPORARY SWEEP: 0
   hit(s)`).
2. **Whether the 1.0.7 branch route actually works** (decision 98) — this is
   what makes any A/B possible at all.
3. Per-fix re-verification, which is a programme and not a session — §5.

## 5 · This is a chain, not a session

Re-verifying 82 shipped fixes across two rewritten systems is far past the
~2-session line, so per `CHAIN_METHOD.md` it should be a self-consuming prompt
chain with a terminal backward QA, not an open-ended sweep. Proposed shape, for
the owner to accept or reshape (decision **101**):

- **C1 — baseline.** Settle the branch question (98), stand up whichever
  baseline wins, take the `ListFixes()` read, reconcile it against §1c.
- **C2 — the dead six.** For each self-disabling module, establish whether the
  *defect* still exists in 1.1.0, independently of whether our fix runs. Some
  will be genuinely obsolete (F09 is already there on a fact, not a claim);
  others will be live defects whose repair now needs a different seam.
- **C3 — the redesigned systems.** §3's list, worst-consequence first.
- **C4 — the claim table.** §2, one control per row.
- **C5 — terminal backward QA**, fresh context, adversarial.

## 6 · The semantic audit has started, and it is finding things (2026-09-08, same day)

§3 predicted that the real damage would be in fixes whose targets survived but
whose systems were rewritten. **Two checks were run against that list. Both
found a defect in our own code.** That is the calibration that matters more than
either finding: the existence sweep's reassuring "73 of 80 keep every gate" says
nothing about correctness, and the hit rate on the first two semantic probes was
2 for 2.

- **[[F111]]** — `Fix_ExtractorStaffedPerformance` (F108) **throws** on 1.1.0.
  The new `Workplace:IsOvertime()` (`Workplace.lua:718-729`) *collapses*
  `self.overtime` from a per-shift table to a boolean, `orig` calls it before we
  do, and our reconstruction still writes `self.overtime[shift]` — indexing a
  boolean. Trigger: automated + `MetalExtractorWorkplace` + overtime on any
  shift. **And the defect F108 repaired is gone**: 1.1.0's
  `GetWorkshiftPerformance` now does `Max(GetWorkersPerformance(shift),
  auto_performance)` — the exact floor-not-ceiling rule the owner ruled on
  08-28. The patch notes never mention it; we read it in the shipped Lua.
- **[[F112]]** — `Fix_AutomationLawCompensation` (C39) now **over-pays**.
  1.1.0 deleted vanilla's automation-law compensation outright (`law_scale`: 0
  hits tree-wide; `automation_workforce_reduction` survives only in `LawDef/`
  data), while the laws still cut `max_workers`. C39 still pays its uplift to
  the 8 out-of-class families and still returns 0 for Factory / ResearchBuilding
  / Service as "already paid by the shipped gate" — a gate that no longer
  exists. So the eight are now the only buildings in the game receiving
  automation compensation: C39 has become the inverse of itself, player-visible,
  in any colony running an automation law.

⚠️ **The shape of the risk this exposes, for the rest of the audit.** Both
defects live in **body-copies of vanilla logic** — the `FIX_POLICY` §1.5
reconstruction disclosures. Those are the fixes a patch can silently invalidate,
because they freeze a snapshot of code the devs are free to change. Ten modules
carry one: `Fix_AsteroidLanderAvailable`, `Fix_AutomationLawCompensation`,
`Fix_DisasterPredictionLeak`, `Fix_DroneTransportMinors`,
`Fix_DroneUnreachableForever`, `Fix_ExtractorStaffedPerformance`,
`Fix_MeteorFrequency`, `Fix_MeteorStormWedge`, `Fix_SmallLandscapeSites`,
`Fix_TrainWaitTime`. Three of those ten are already accounted for (two filed
here, and `Fix_AsteroidLanderAvailable` + `Fix_DroneUnreachableForever`
self-disable). **The remaining ones are the highest-yield place to look next**,
ahead of the §2 claim table. F108's own header says it: *"Re-check this loop
against that block on every game update."*

⛔ Still unaudited, and not safe to assume clean: `Fix_NightShiftWork` (F04),
`Fix_MoraleComfortTooltip` (F20), `Fix_SaintBlessing` (F92), the landscaping
group (F33/F34/F30/F105/F107/F110) against Drones losing landscaping entirely,
`Fix_DustStormUndergroundBreaks` (F90) against the new all-consumers grid
shutdown, and `Fix_TouristApplicants` (F08) against tourists now being rated on
Comfort/Morale.

### 6b · The crash/error sweep — enumerated, not sampled (2026-09-08)

§1c claimed "no crash path was found". **That claim was wrong, and it was wrong
because it was scoped to `Require` specs rather than to call sites.** A proper
sweep of every call our `Code/` makes, checked against the 1.1.0 tree:

| what was swept | checked | dead in 1.1.0 | reachable? |
|---|---|---|---|
| bare global calls | 106 names | 3 (`GatherTransportableResources`, `GetCommandCenterLifeSupportGrids`, `GetGridGlobalStorage`) | **No** — all in modules that self-disable, or in F75's never-installed closure |
| `const` / `g_Consts` reads | 28 names | 3 (`MinDaysFoodSupplyBeforeNotification`, `MinDaysMaintenanceSupplyBeforeNotification`, `SatisfactionLowStatPenalty`) | **No** — same modules |
| method calls `obj:M(...)` | 174 names | 2 absent entirely (`UpdateSatisfaction`, `ChangeSatisfaction`) + 1 **(`GetEarthExportResPossibleReward`)** | ⛔ **YES for the third** → [[F113]] |
| fields we index as tables | 30 sites | 1 (`self.overtime`) | ⛔ **YES** → [[F111]] |

Six further method names (`GetMapSlot`, `GetPassablePointNearby`, `GetPosXYZ`,
`GetSpotPosHex`, `SetAmount`, `SetRolloverTitle`) have no Lua definition but are
used throughout 1.1.0 — engine-side, present, not a risk.

✅ **The bounded good news.** `self.overtime` is the **only** field in the pack
whose table-ness 1.1.0 abandoned: every other field we index (`self.workers`,
`self.demand`, `self.supply`, `self.labels`, `grid.elements`, …) 1.1.0 still
indexes itself 11–194 times. F111 is the sole instance of its class, not the
first of many. And outside the self-disabling modules there is exactly **one**
dead call in the whole pack — F113.

⛔ **THE UNBOUNDED BAD NEWS, and the real answer to "what is dangerous now".**
**~11 modules define a vanilla method with no `orig` captured — full body
replacements.** (⚠️ First stated as 31; that detector missed `orig_<name>`
upvalues. It errs both ways — see `GAME_1_1_0_AUDIT.md` §2c. The population
cannot be settled by a regex.) On 1.1.0 each one substitutes a 1.0.7-derived body for whatever
the developers now ship, so *anything the patch improved inside a replaced
function, we silently undo*. F113 is the proof: it replaces
`CreateAutoCargoRequest`, a function 1.1.0 visibly rewrote, and was caught only
because one of its calls happened to be a name that vanished. **A replacement
whose every call still resolves is completely invisible to every sweep in this
report** — it just quietly reverts the patch. The 31 are the highest-yield audit
target in the project, above the §1.5 reconstruction list and far above §2's
claim table.

### 6a · Correction to §0 — the rollback path IS dev-authorized

The owner's read was that Steam gives no way back unless the developer
specifically authorizes multiple builds. **That authorization is exactly what
happened here**, in the *Feeding the Future* announcement, verbatim: "if you are
playing on Steam and would prefer to continue your current playthrough, **Patch
1.0.7 will remain available through the 1.0.7 Branch**", via Properties → Game
Versions & Betas → 1.0.7. ⚠️ It stays a **claim about a store surface** until
someone opens that dropdown — an attempt to confirm it from Steam's local
`appcache/appinfo.vdf` found no branch block to read, so the only control is the
UI itself. Decision **98**.

⛔ The pack is **published and live on both portals at version 5**, and every
player who auto-updated is on 1.1.0 now. Nothing in this document is a reason to
ship in a hurry: 73 of 80 modules keep their gates, the other 7 fail safe, and
no player-facing incompatibility flag fires (§1d). The expensive mistake
available here is a rushed re-upload built on patch-note claims.
