# 03b progression/politics preset batch — read-only report

Date: 2026-09-10. Sources: archived `1.0.7.396349` and
`1.1.0.403908`; installed Steam build rechecked as `24995074`. Repository files,
tagged TSVs, source archives, and game files were not changed.

## Result and exact receipt

The requested filter is `link == 03` and class in the 14 registries named in
`SEAM_PRESETS_PLAN.md`'s progression/politics batch. It returns **548 rows**.
There are **548 unique `prid` values, zero duplicates, zero missing expected
keys, zero not-reached rows, and zero added/removed source files**. All fields
are present as complete preset fields in `PRESETS.tagged.tsv`; there are no
function-span/hunk-only rows. Churn classes are `none` 517,
`REINDEX-SWAP` 22, and `added-preset` 9. Registry reconciliation:

| registry | read |
|---|---:|
| FactionDef | 285 |
| TechPreset | 107 |
| LawDef | 78 |
| PolicyDef | 21 |
| CommanderProfilePreset | 15 |
| EffectDef | 8 |
| Tech | 8 |
| FlightPolicyDef | 6 |
| GameRuleDef | 5 |
| MissionSponsorPreset | 5 |
| Challenge | 4 |
| SponsorGoals | 3 |
| Milestone | 2 |
| TechFieldPreset | 1 |

No candidate with a `FIX_POLICY` §4 hard intent tell survived this batch.
There is no entry-ready DIFF-CAUSED or PASSING finding here. There is one
important instrument qualification: `presetdiff` identities the top-level
preset, but nested faction `likes[]`, `tasks[]`, and law `FactionLikes[]` only
by numeric path. Consequently a row can faithfully report a changed path while
pairing two different logical children after insertion/reordering. The 285
FactionDef rows comprise 152 `tasks[]`, 119 `likes[]`, 9 `approves`, and 5
`disapproves`; 71 are old-absent, 62 new-absent, 152 changed-value. The 22
explicit `REINDEX-SWAP` rows include 17 FactionDef and 5 LawDef rows. Whole-
preset/list reading, not a same-child field-mutation story, is the correct
interpretation. This is a limitation to retain for 99, not a defect in shipped
Lua.

## FR-2 first: live tech and deep-deposit route

`P02707` is the batch's only FR-tagged row. `EffectDef::SpawnSubsurfaceDeposits
::[5].code` changes only the conditioned random selector from
`AsyncRandomObjByConditionList` to `InteractionRandObjByConditionList(...,
"SpawnSubsurfaceDeposits")`; deposit construction, `resource`, `grade`,
`max_amount`, `depth_layer`, buildable/passable checks, `revealed=true`, and
`PlaceDeposit()` remain. Locations are old/new `Data/ClassDef-Effects.lua`
around the `SpawnSubsurfaceDeposits` preset (new `:5036-5098`; generated
runtime wrapper `Lua/ClassDefs/ClassDef-Effects.generated.lua`). It is a generic
script effect, not the ordinary sector/probe Deep Scanning switch.

The dual tech registry is resolved, not left as a name inference:

- Old `TechPreset` is the former live definition (`GlobalMap="TechDef"`). In
  1.1 it remains a legacy parameter sidecar at
  `Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1709-1729`.
- New `Tech` is the live registry (`GlobalMap="Techs"`) at
  `CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua:3-27`.
  Runtime research, UI, and effects use `Techs`/`Presets.Tech` (for example
  `Lua/Tech.lua:24-35`, `Lua/Research.lua:151`, and
  `Lua/TechTree.lua:928`).
- The old DeepScanning preset is old `Data/TechPreset.lua:2944-2961`. In 1.1,
  `Data/TechPreset.lua:847-852` is only its empty sidecar; the live definition
  is `Data/Tech.lua:3934-3961` and still contains both
  `Effect_ModifyLabel(Consts.DeepScanAvailable)` and
  `Effect_UnlockDeeperDeposits`.

Thus these preset rows support 03c's source result: the reported missing-deep-
resources symptom is **not explained by a disconnected DeepScanning preset**.
Orbital probes still have their separate AdaptedProbes requirement. Runtime
progression is unmeasured, so FR-2 is not closed. Falsifier: on a fresh 1.1
colony, observe `DeepScanAvailable`, the tech effects, and sector/probe reveal
state before/after DeepScanning and AdaptedProbes. Vacuous if an old blocked
save or an already-revealed sector is used.

## Registry dispositions and consumer contracts

### TechPreset, Tech, and TechFieldPreset — 116 rows

All 33 TechPreset ids touched by this batch have a corresponding live `Tech`
definition in new `Data/Tech.lua`; none is orphaned. The 107 legacy-sidecar rows
are mainly old descriptions/effects removed from `Data/TechPreset.lua` after
their migration to `Data/Tech.lua`. The eight `Tech::<preset>` additions are
the live counterparts for DomelessFarming, DryFarming, FarmAutomation,
GiantCrops, MoistureFarming, RemoteFarming, Space_Farming, and UtilityCrops;
the added TechFieldPreset is Hi-Tech. FarmAutomation deliberately corrects the
old sidecar id's shipped trailing space (`"FarmAutomation "`) to the live
`"FarmAutomation"` id. Selected executable migrations were checked in both
directions: DustRepulsion's old `OnResearched` assignment is the live Tech's
`OnTechResearched` at new `Data/Tech.lua:9295-9317`; PlanetarySurvey's code is
at new `:8288-8330`; NanoRefinement is now read on demand by
`BuildingComponents.lua:284` and `SubsurfaceDeposit.lua:24-31`; crop/building/
upgrade effects occur on the matching live Tech definitions.

Reach is R1/R2 through ordinary research or content-specific tech unlocks.
Non-owners execute the base `Tech` registry; DLC-only ids are absent rather
than shadowing base live ids. Falsifier: a touched old effect/description with
no matching live Tech content or a runtime reader still using only its stripped
TechPreset sidecar. None was found. Seam: research-tree migration plus farms,
food, cargo, and asteroid content. SMELL/PERF: none; no new cadence is authored
by these rows.

LowGFungi specifically is not a typo lead: the live new Tech is the source of
the FungalFarm unlock and its Underground_1 placement/prerequisites already
cited by the upstream seam report. The two P rows only show the old sidecar's
building/description fields being stripped.

### FactionDef — 285 rows

Locations are the same `Data/FactionDef/*.lua` preset files in both trees.
The rows describe the large 1.1 politics/content rewrite: approval/disapproval
copy, removed old law-category `table.icount` likes, service checks migrated
from interest-based `AreServiceBuildingsUnavailable` predicates to named
availability/label checks, and task/tech/law/resource lists replaced or
reordered. Runtime consumers are `FactionDef:EvalApproval` at new
`Lua/Factions/FactionDef.lua:51-115`, task definition evaluators at
`:1113-1562`, task generation/rechecks at
`Lua/Factions/Legislature.lua:1477-1516`, and the ordinary approval pass at
`Lua/Factions/Factions.lua:663-680`. This gives R1/R2 base politics reach.

The apparent non-owner DLC references were traced rather than cleared by name.
China and LastTransmission add InsectFarming/FarmInsect opportunity data
(`Data/FactionDef/China.lua:230-279`, LastTransmission `:547-574`). Direct dome
task generation short-circuits on
`GetTechState("InsectFarming") == "researched"`; a missing Tech maps to
`"enabled"`, not researched (`CommonLua/Libs/Research/Research.lua:51-53` plus
`CommonLua/Features/LockablePreset.lua:343-345`). Generic
`FactionTaskTechStatus:EvalTaskGenerateCondition` separately rejects a missing
`Techs[self.Tech]` at `FactionDef.lua:1541-1545`. The subsequent
`UIColony.labels.FarmInsect` access therefore is not reached by a non-owner.
InsidePasture has base class/template support. Base FungalFarm references are
not FungalFarmBase dependencies.

Falsifier: a generation path that bypasses `EvalGenerateCondition`, or a
missing-tech state reported as researched; neither appears. Seam: base faction
opportunities meeting new farm/tech/law content. Non-owner answer: no thrown or
live impossible task was derived; missing official techs are gated. SMELL/PERF:
none. The generic hourly politics consumers also establish the data reach behind
C64, but C64's cleanup defect is in the already-filed hand consumer, not a new
preset defect.

### LawDef and PolicyDef — 99 rows

Locations are `Data/LawDef/*.lua` and `Data/PolicyDef.lua` in both trees.
Changed callable fields are used by LawDef/PolicyDef and Legislature's ordinary
prepare/enact/vote/message paths. The batch includes Dhondt migration,
Childcare/Education/Exploration/Milestone handlers, law-effect class migration,
ResearchFocus's renamed fields, VoteOnly additions, and NativeFood/SpaceFarming
being made obsolete. The PolicyDef disable conditions are evaluated through
the left-to-right policy chain documented in EF-062; this is R1/R2 when
politics is enabled, not proof that every law is immediately available.

Five `REINDEX-SWAP` FactionLikes rows are nested-list reindexing around the new
AssemblyOfPlanets likes, not evidence that one faction value silently changed.
The base tree has no AssemblyOfPlanets FactionDef, but the consumers compare
`like.Faction` to an existing faction id and do not index the missing definition
(`Legislature.lua:313-330`, `:453-460`; `FactionDef.lua:87-100`). Non-owner
execution is therefore safe on the paths read. NativeFood and SpaceFarming are
explicitly `Obsolete=true`; this is an authored removal, not an accidental nil
path. Falsifier: a law consumer indexing `FactionDefs["AssemblyOfPlanets"]`
without a guard, or an active non-obsolete policy relying on a removed
prerequisite. None was found. SMELL/PERF: none.

### FlightPolicyDef — 6 rows

Old/new locations are `Data/FlightPolicyDef.lua`; the five resource-list
functions are new `:145-185`, `:274-293`, and `:458-503`, and the probe cargo
handler is the `our_colony` preset's `OnCmdWaitInOrbitBegin`. They are called
through `UniversalRocketBase:GetAllowedResources` at
`Lua/UniversalRocket.lua:737-746` and command dispatch at `:304`. The rewrite
normalizes endpoint lists and adds Sugar/Spices only inside
`IsDlcAvailable("norman")`. Non-owners retain the ordinary resource lists and
never receive those absent ids. R1/R2 when using multi-destination rockets;
otherwise conditional. Falsifier: Sugar/Spices emitted with norman unavailable,
or an allowed endpoint incorrectly returning nil/all. Neither is in the read
bodies. SMELL/PERF: none.

### Challenge — 4 rows

Old/new location is `Data/Challenge.lua`. Europe now enumerates live `Tech` and
excludes initiatives; Japan's custom Run is removed and TickProgress reads
`g_BreakthroughsResearched`; SpaceY reads `g_TechResearchedCount`. The challenge
thread invokes `TickProgress`/`Run` at new `Lua/Challenges.lua:27-47` (R2: only
the selected challenge). This matches the registry/count migration; no stale
TechDef consumer survives in these rows. Falsifier: either global omits a
researched eligible tech or counts an initiative contrary to the challenge
target. Runtime challenge progression is unmeasured. SMELL/PERF: none; WaitMsg
cadence is retained.

### EffectDef — 8 rows

Old/new location is `Data/ClassDef-Effects.lua`, with runtime generated wrappers
in `Lua/ClassDefs/ClassDef-Effects.generated.lua`. CallTradeRocket adds missing-
id/cargo early returns and proper display-name translation; DiscoverTech moves
to the live Techs/research APIs; PickCargo and SpawnSubsurfaceDeposits move to
named interaction RNG; RewardTech/RewardTechBoost read `Techs`/`DisplayName`;
RivalCallHelpRocket moves to `OpenRivalRocketPicker`; ModifyCargoPrice changes
formatting only. Reach is R2/R3 through an instantiated story/script effect.
Falsifier: an official instantiated effect with an incompatible context or a
live old-only registry lookup. No such row was established here. Non-owner:
none of these fields requires norman. SMELL/PERF: none.

### SponsorGoals — 3 rows

Old/new `Data/SponsorGoals.lua`. CompleteTechs' old blocking `Completed` loop is
replaced by the common `EvalProgress`/hourly condition model; EnactLaws likewise
moves from `Completed` and adds `EvalProgress`. `SetupMissionGoals` instantiates
and immediately evaluates at new `Lua/Colony.lua:416-433`, and the goal loop
re-evaluates hourly. R1 for a sponsor carrying the relevant goal, otherwise R2.
Falsifier: goal slots using these ids fail to advance under TechResearched or
LawActivated. No source disconnect was found. Non-owner: base sponsor goals do
not require DLC. SMELL/PERF: none; one common hourly goal pass replaces bespoke
blocking loops.

### CommanderProfilePreset — 15 rows

Old/new `Data/CommanderProfilePreset.lua`. Fourteen are player-facing effect
text updated for the redesigned profile bonuses; GeoEngineer also adds a
`Resource` item class. The complete presets' effect objects/fields correspond
to the new descriptions on the inspected profiles (including Spelunker,
TransportTycoon, astrogeologist, author, oligarch, politician, and rocket
scientist). Reach is R1 at mission setup and profile summary. Falsifier: a stated
bonus with no matching profile field/effect or an undisclosed functional bonus;
none surfaced in these 15 changed rows. Non-owner: base profiles. SMELL/PERF:
none.

### MissionSponsorPreset — 5 rows

Old/new `Data/MissionSponsorPreset.lua`. IMM, NewArk, and TerraInitiative update
effect text to match balance/bonus-tech changes; Independent's old effect text
is removed with its sponsor-state redesign; Paradox changes
`black_market_resource` from Food to Electronics. Reach is R1 for the selected
sponsor and its mission summary/effects, conditional for Independence. These
are explicit authored content changes with no sibling contradiction in the
opened presets. Falsifier: a displayed sponsor effect disagreeing with its
actual fields/effects. Non-owner: base sponsor paths. SMELL/PERF: none.

### GameRuleDef — 5 rows

Old/new `Data/GameRuleDef.lua`. ChaosTheory text reflects the redesigned tech
graph. NoPolitics moves mission setup reads from stale
`g_CurrentMissionParams` to `Game`, changes its law list, and continues to
replace AssemblyOfPlanets/politician selections. Reach is R2 when NoPolitics is
selected. Missing thomas content is handled by the rule's explicit replacement
logic. Falsifier: the rule running after sponsor/profile consumers have already
latched the forbidden selection, or leaving a politics law active. No such
ordering contradiction was derived from these data fields. SMELL/PERF: none.

### Milestone — 2 rows

Old/new `Data/Milestone.lua:123-139` / `:131-148`. ProduceFood gains explanatory
text and its unchanged `FoodProduced` reaction accepts the new trailing
`resource` argument. It still calls `CompleteMilestone`; the generic producer
message did not replace the Food-specific event. R1 when base food production
first occurs. Falsifier: a non-food producer emitting `FoodProduced`, or a food
producer no longer emitting it. No mismatch was found. Non-owner: ordinary
Food/farms. SMELL/PERF: none.

## Control score

Eligible seeded positives in this generated/preset queue: **0**, so the seed
score is **N/A (0 eligible)**, never 4/4.

A deterministic child sample used `System.Random(32003)` over the 548 filtered
rows in tagged-file order and selected `P02972 P03061 P04844 P05298 P21673
P21676`. The raw old/new field values match the archived presets **6/6** and the
runtime registry/consumer route is precise **6/6 after whole-preset
re-derivation**. The sample also caught the structural limitation: P02972 and
the two removed `likes[]` fields are not safely narratable as mutations of one
logical nested child; GiantCrops' two fields are old-TechPreset-to-live-Tech
migration, not feature deletion. Therefore a blind scorer using only the
field-path story would be 3/6 on semantic identity even while the mechanical
row values are 6/6. Parent sampling should score whole-preset interpretation.

## Exact key outbox

- FactionDef (285): P02770 P02783 P02793 P02831 P02848 P02855 P02875 P02876 P02880 P02881 P02883 P02884 P02901 P02902 P02915 P02927 P02928 P02946 P02948 P02959 P02962 P02964 P02967 P02971 P02972 P02989 P03030 P03036 P03043 P03057 P03061 P03073 P03098 P03100 P03120 P03147 P03217 P03218 P03231 P03243 P03261 P03263 P03265 P03266 P03270 P03286 P03313 P03318 P03326 P03383 P03385 P03386 P03407 P03420 P03432 P03443 P03565 P03567 P03568 P03571 P03596 P03612 P03620 P03625 P03630 P03639 P03656 P03662 P03666 P03670 P03677 P03680 P03687 P03689 P03703 P03708 P03713 P03720 P03725 P03729 P03733 P03743 P03747 P03750 P03754 P03758 P03759 P03762 P03769 P03772 P03778 P03782 P03783 P03786 P03790 P03792 P03796 P03797 P03803 P03807 P03809 P03816 P03831 P03832 P03833 P03859 P03869 P03932 P03976 P03988 P04000 P04032 P04054 P04058 P04061 P04085 P04119 P04125 P04142 P04156 P04167 P04177 P04187 P04199 P04246 P04311 P04313 P04317 P04320 P04391 P04414 P04426 P04427 P04431 P04433 P04438 P04445 P04449 P04451 P04454 P04455 P04456 P04459 P04469 P04470 P04473 P04478 P04479 P04480 P04492 P04493 P04498 P04596 P04609 P04620 P04639 P04672 P04688 P04692 P04694 P04696 P04738 P04741 P04749 P04752 P04760 P04763 P04771 P04777 P04786 P04793 P04800 P04809 P04819 P04822 P04829 P04830 P04844 P04848 P04857 P04860 P04866 P04867 P04873 P04897 P04899 P04917 P04920 P04927 P04930 P04931 P04942 P04945 P04953 P04956 P04971 P04972 P04978 P04982 P04998 P05001 P05009 P05013 P05015 P05019 P05020 P05024 P05026 P05030 P05031 P05034 P05044 P05048 P05057 P05061 P05063 P05067 P05068 P05074 P05080 P05084 P05091 P05101 P05197 P05204 P05209 P05214 P05221 P05228 P05235 P05242 P05245 P05273 P05286 P05292 P05296 P05298 P05305 P05306 P05310 P05312 P05316 P05335 P05337 P05378 P05399 P05408 P05435 P05447 P05457 P05475 P05487 P05600 P05619 P05643 P05657 P05693 P05695 P05699 P05701 P05706 P05720 P05723 P05727 P05730 P05734 P05736 P05740 P05741 P05745 P05747 P05751 P05752 P05758 P05769 P05773 P05782 P05786 P05788 P05792 P05793 P05799 P05804 P05806 P05813
- TechPreset (107): P20815 P20853 P20858 P20914 P20999 P21004 P21248 P21304 P21305 P21306 P21307 P21308 P21309 P21359 P21360 P21361 P21362 P21363 P21364 P21365 P21366 P21367 P21368 P21369 P21370 P21371 P21372 P21373 P21374 P21375 P21376 P21377 P21438 P21439 P21442 P21556 P21557 P21558 P21559 P21560 P21561 P21562 P21563 P21564 P21565 P21566 P21601 P21604 P21643 P21644 P21646 P21670 P21671 P21672 P21673 P21674 P21675 P21676 P21677 P21681 P21738 P21839 P21842 P22012 P22014 P22129 P22189 P22192 P22193 P22251 P22252 P22254 P22402 P22403 P22404 P22405 P22406 P22407 P22408 P22431 P22636 P22779 P22780 P22781 P22782 P22783 P22812 P22904 P22906 P22984 P22986 P22996 P22999 P23082 P23085 P23204 P23230 P23302 P23303 P23304 P23305 P23306 P23307 P23308 P23309 P23359 P23360
- Tech (8): P20103 P20111 P20131 P20144 P20244 P20290 P20320 P20379
- LawDef (78): P06068 P06132 P06168 P06174 P06208 P06224 P06282 P06427 P06428 P06437 P06508 P06513 P06540 P06609 P06617 P06629 P06658 P06665 P06719 P06752 P06758 P06888 P06891 P06899 P06902 P06907 P06908 P06909 P06910 P06911 P06912 P06913 P06977 P06980 P06995 P07089 P07147 P07150 P07204 P07241 P07270 P07278 P07279 P07280 P07299 P07330 P07348 P07360 P07418 P07428 P07429 P07430 P07431 P07432 P07433 P07434 P07435 P07436 P07437 P07497 P07547 P07563 P07595 P07626 P07627 P07631 P07632 P07695 P07697 P07698 P07723 P07724 P07725 P07726 P07727 P07728 P07729 P07798
- PolicyDef (21): P09408 P09409 P09411 P09412 P09413 P09425 P09426 P09428 P09429 P09434 P09456 P09460 P09461 P09462 P09466 P09474 P09475 P09481 P09491 P09505 P09506
- FlightPolicyDef (6): P05823 P05824 P05826 P05830 P05831 P05833
- CommanderProfilePreset (15): P02231 P02234 P02238 P02243 P02248 P02259 P02307 P02318 P02321 P02324 P02333 P02341 P02347 P02351 P02359
- SponsorGoals (3): P12621 P12669 P12670
- MissionSponsorPreset (5): P08417 P08424 P08438 P08471 P08477
- Challenge (4): P01983 P01992 P01994 P02005
- GameRuleDef (5): P05849 P05858 P05859 P05863 P05866
- EffectDef (8): P02597 P02607 P02610 P02639 P02643 P02646 P02647 P02707
- TechFieldPreset (1): P20506
- Milestone (2): P08355 P08356

## Outbox / retained limits

For the parent: mark all 548 listed P keys read, with no child remainder. Retain
the nested-list identity warning in 99's inbox. No new C filing is recommended
from this batch. The useful cross-link facts are: live Tech vs TechPreset is
resolved; DeepScanning remains connected; missing DLC farm tech/task references
are condition-gated for non-owners; FlightPolicy sugar/spice additions are
explicitly norman-guarded; C64's faction data reach is abundant but the defect
is in the hand cleanup consumer.

For dlccheck, TAKEABLE WHEN it opens the actual official definitions: confirm
InsectFarming/FarmInsect task availability and completion with norman loaded;
confirm Sugar/Spices cargo/resource registration against the guarded flight
lists; confirm official DLC Techs populate `Techs` rather than the legacy
TechPreset sidecar. These are conditional owner paths, not uninspected DLC
clearance.

Blind spots retained: native/C-only consumers, anonymous/dynamic dispatch,
actual execution, runtime timing/profiling, consoles, absent assets, and the
incomplete old DLC tree. No source read closes FR-2 or establishes global
non-owner safety outside the named routes.

