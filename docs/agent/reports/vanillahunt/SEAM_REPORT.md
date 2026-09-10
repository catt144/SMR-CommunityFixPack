# 03 — core food seam read and continuation contract

2026-09-10. Parent Codex `/root`; read-only chasers `food_seam`, `farm_seam`,
`resource_seam`. This is the parent's synthesis, not verbatim agent transcripts.
All verdicts and repository writes are the parent's. No game was launched;
no module, metadata, installed game file or archived source was changed.

## Result and evidence boundary

**MEASURED coverage:** 396 of the 1,289 tagged INVENTORY rows have complete
present spans read. An added row has no old same-file body; a removed row has
no new one. This is not 396 distinct functions or an exhaustive caller sweep.
The remaining 893 INVENTORY rows, all 1,618 PRESETS rows, 24 of 30 CALLERS
items and all 18 NOROWS text-diff items have explicit continuation owners.
Incidental preset/caller excerpts support findings but do not drain those queues.

**SOURCE candidates:** C56-C62, all `cand` / `source-read`. Five are
DIFF-CAUSED; C59 and C62 are PASSING. No fix is authorized by filing.
Candidate entries carry the full both-tree citations, route, non-owner answer,
independent recipe and falsifier. Fresh-fixture riders for C56/C57/C58/C60/C61
are in `docs/PLAYTEST_CHECKLIST.md`, under Decisions waiting on you.

| entry | concrete tell | non-owner answer | limit |
|---|---|---|---|
| C56 | ranch rounds each animal's output but forecast rounds the herd | base ranch and Chicken route exists | accepting desk producer only; no native storage/lifecycle observation |
| C57 | disabled ingredient omitted by menu/stat readers but consumed from residual stock | no normal base-only ingredient trigger found | actual DLC resource/recipe registration and game timing unobserved |
| C58 | piles/depots spoil reserved food while consumption hosts explicitly protect it | ordinary Food/piles/depots suffice | native request handling and later accounting outcome unknown |
| C59 | next-crop helper tests the same slot three times; planting sibling advances | base helper exists; literal caller search finds none | R4; bounded failure, not infinite loop or established player impact |
| C60 | ranch infopanel updater allocates/fills a list never read | base ranch panel callback exists | PERF tell only; cost and frame-time impact unmeasured |
| C61 | death popup still describes two lost applicants after base death path deletes the penalty | base route needs no DLC; owner overrides uninspected | consequence text contradiction, no implied balance repair |
| C62 | explosion helper fills `buildings_hit` and discards it | base helper and four wrappers exist | U for an instantiated player scenario; no measured cost |

Pin: `SEAM_PLAN.md` records the fresh appmanifest buildid 24995074 and the two
manifest hashes (4,448 / 4,717 files). Start HEAD `0f9f006`; plan commit
`7ed7ef3`; initial filing/desk commit `b28f133`. Manifest files were hashed,
not every source file. EF-085 establishes shipped-byte parity, not execution.
All source paths below are relative to the pinned `Src`, versions old=1.0.7.396349,
new=1.1.0.403908. Old DLC is incomplete and excluded from comparisons.

## Coverage receipt

`SEAM_COVERAGE.tsv` is the dated, row-keyed receipt. `python tools/seam_coverage.py`
reproduces and checks its 2,955 unique items against the tagged source ledgers;
`--write` emits the same snapshot. Its labels are reader attestations, not an
instrument that can infer whether someone read a body. Original tagged TSVs
remain unchanged. Future links append their own receipts and do not rewrite this
historical read snapshot to imply the original session read more.

| owner | INVENTORY | PRESETS | CALLERS | NOROWS |
|---|---:|---:|---:|---:|
| 03 completed | 396 hand | 0 | 6 | 0 |
| 03b pending | 360 generated | 1,618 | 6 | 0 |
| 03c pending | 284 hand | 0 | 2 | 0 |
| 03d pending | 249 hand | 0 | 16 | 18 |

The file groups in `SEAM_PLAN.md` define the original 396. The food chaser also
read all 25 Colonist rows originally assigned to the parent. Final reader counts:
food 152, farms 105, resources 91, parent 48. Parent reread candidate routes,
counterevidence, and the six randomly selected rows below. Bulk reads initially
truncated two parent spans, R05399/R05412; both old/new spans were subsequently
read in full before this receipt was finalized. None remains hunk-only.

Overlapping extractor spans count as rows, not distinct bodies: R10475's true
one-line `innate` body is new Colonist.lua:201, although its reported span runs
through :290. R06014/R06028 actual old Farm methods are one-line :579/:580 and
overlap CanService in the instrument. R06524 also overlaps a sibling old span.
The corresponding complete reported spans were read; this does not repair the
instrument's delimiter. Checklist 135 remains its own gate.

### food

127 added spans: FoodServiceBuilding, Meal and RecipeProductionBuilding. There
are no old files under those names. Related old Diner/Grocery service and
HasConsumption/Colonist contracts were opened for comparison. SOURCE seam:
base Diner/Grocery now inherit FoodServiceBuilding instead of ServiceWorkplace;
base FoodBuilding/InputResourceHost exist without norman. Default Food is base
content. Resource/ingredient masks, request creation/draining, meal reservation,
storage, recipe selection/production and UI callbacks were read. C57 survives
the setter/reader/consumer contradiction; a normal Food-only non-owner has no
registered delicacy mask to consume. A non-owner is not protected by absence of
the new base classes: those classes exist and execute on ordinary services.

SOURCE remaining limits: the base `Data/ResourceProductionRecipe.lua` is header
only; FoodProcessingPlantBase is a base class, but no constructible base template
and concrete recipe were established. Recipe input reservations (`RecipeProductionBuilding`
new1019-1032) are not subtracted by `CanExecuteRecipe :402-409` or
`ConsumeRecipeInput :517-532`; a real Food-input recipe plus accessible pile is
needed before calling that an exposed double-consumption defect. A class existing
in base is not proof a non-owner can build it. TAKEABLE WHEN DLC deep-check reads
the recipe preset, building template and colonist selection route together.

FoodService workshift capacity: new `OnChangeWorkshift :853-856` resets the count
while `ReturnMealPortion :877-884` adjusts current capacity. A reservation spanning
the shift is a hypothesis, not a filed defect: no hard contradictory outcome was
derived. TAKEABLE WHEN 03d traces cancellation/return across the workshift caller.
Meal score based on the allowed ingredient count rather than available stock is not by itself
an intent tell. `SameOldSlop` threshold remains TAKEABLE WHEN 03b reads the
achievement preset and consumer. New recipe selection adds periodic recipe/output
walks; cost is unmeasured and an actual processor remains conditional.

### farms

105 complete present spans: 66 Farm, 8 FungalFarm, 4 Crop, 27 Animals; 40 changed
pairs, 50 additions, 15 removals. SOURCE: crop storage moves from a scalar to
resource outputs; GetGrowthDuration/GetHarvestRemaining change from sols to
milliseconds, while GetGrowthTimes already used milliseconds and adds pause accounting;
producer callbacks replace named Food hooks; ranch output takes quantization.
The parent filed C56, C59 and C60 after following production and panel routes.

Contract checks: `GetGrowthTimes`' five retained call sites old277/380/416/666/674
-> new284/390/439/805/813 pass no removed index. New duration readers supply
DayDuration; old `GetGrowthDuration :156-162` -> new189-197 and crop updater
old832 -> new1085 were compared. `RecursiveCallMethods.OnSetWorking` at
Building.lua:1-3 explains the deleted explicit parent call. Old
BuildingComponents.lua:473-495 bound the named production callbacks; new
`:1289-1327,1331-1337` dispatches `OnProducerProduced`/`ProducerModifyCalcProductionAmount`.
ResourceProducer:SyncProducerSlots in BuildingComponents.lua:612-631 and Farm synchronization/crop transitions were
checked as the replacement path. Removed direct Farm service methods remain
TAKEABLE WHEN 03d enumerates remaining direct Farm receivers; the new pile path
does not prove every dynamic old receiver was eliminated.

FungalFarm production/environment edits were not declared accidental balance
defects. New Fungal template :57 excludes Surface/Asteroid and uses 8000, while
old Fungal code varied production by environment. New LowGFungi in Data/Tech.lua
:10473-10496 explicitly uses Underground_1 (:10491), underground prerequisites
and icon (:10476): counterevidence to a simple mistaken ban. TAKEABLE WHEN 03b
reads the full preset/consumer relationship. Crop augmentation's base effect
callers MarsGameEffects.lua:146-149 and Lua/Factions/Laws.lua:844-851 exist, but a
concrete base instantiated effect was not established; DLC deep-check owns that
remaining reach question. Colony-wide farm synchronization and wider pet dome
enumeration are PERF shapes, without measured cost; pet 24-48 hour birth and
four-hour death cadences did not shorten. Apparent crop-effect string concatenation
failure was refuted by the game's localization `table.concat` override
(CommonLua/Core/localization.lua:480-496), not stock Lua semantics.

### resources

91 complete present spans: 28 old/new pairs, 54 additions and 9 removals, in the
12 resource/storage files listed in the plan. SOURCE: resource groups expand
into leaves; storage/overview/tracking enumerate the new resources; meal portion
methods separate reservation and fulfillment; spoilage is new. C58 survives a
direct contradiction with the protected host's in-transit comment. Native
`_TaskRequest.lua:391-399` receives an amount, not the colonist; no fabricated
native request implementation establishes underflow, interruption or clamping.

`AddResourceAmount` changes old(amount,notify) at ResourceStockpile.lua:430 to
new(amount,resource,notify) at :439. Literal base call sites were enumerated,
including BuildingComponents:963, Building:3642, DustStorm:313, Meteors:808/:952,
BlackCubes:232, RCDriller:115, ResourceStockpile:493/:531/:739/:1240,
StockpileController:304/:321/:388, MixedPoolStockpile:226,
RecipeProductionBuilding:1000, Station:219, StorageDepot:1293 and Spoilage:53/:61.
No stale boolean in the new resource slot was found. This is a call-line/alias
check, not complete surrounding-body coverage for every outside-file caller.
MixedPool aliases AddResource; UniversalStorageDepot aliases AddResourceAmount;
multi-resource forwarding was checked. `UpdateStockpileAmounts`' trailing
resource remains optional and WasteRock's omission uses its default.

Refuted missing-colon hypothesis: ResourceOverview.GetResearchRolloverItems
old406/new434 calls `UIColony.GetEstimatedRP_LawsUpkeep` with dot in both trees,
but Research.lua new707-713 never reads self. Expanded Terraforming tracking
uses the same preset iterator as `InitTimeSeries :132-140`; no stale initializer
was found. Base `IsFoodResource` is exact Food (Resources.lua:553-555).
ConsumptionResourceStockpile has a parent guard and protected parent reservation
accounting, but a fresh-game base template still consuming Food through that
older host was not found. Its protected code is counterevidence to C58, not a
claim a player can currently build every comparator host.

### colonists

25 complete present spans, including 13 existing old counterparts; food chaser
plus parent route review. SOURCE: Eat now takes the recorded meal amount and
returns no consumption total; three explicit base calls (new VisitService:2492,
MicroGHabitat:143, CheatEat:5213) do not read the return. The ingredient mask is
computed from the venue before ApplyIngredientStats:5351-5372; cleared meal
state is not a missing argument there. The `AssignMeals` wrapper has no explicit
base caller located; dynamic/DLC dispatch is not cleared.

New underfed severity is Hungry=1, Starving=2, Malnourished=3; missed-meal
aggregation starts at Starving. Idle's raw-food fallback flag is truthy for
Hungry too: do not require the StatusEffectStarving effect for C58's recipe.
C61's pool-mutation enumeration and all five direct ColonistDied handlers are
in its entry. A possible VisitService consumption after failed EnterBuilding was
not turned into a defect without the reached return/destructor path. TAKEABLE
WHEN 03d reads the ambient-life/enter/abort seam. No stock-Lua nil/false iteration
crash was filed; EF-005 applies.

### parent

48 complete present spans: Dome 20, Building 14, Community 9, Colony 3,
UpgradeUnlocks 2. SOURCE: Dome food selection now reserves meal portions through
the connected service-dome cluster (GetResidentServiceDomes new828-830,
GetFoodService :3460-3499, GetService :3501-3519 vs old2900-2943).
GetClosestFoodPile old2884-2893/new3449-3458 adds an optional best-so-far pile and
unreachable guard; the same-caller contract was checked. Preferring own-dome food
before a cluster alternative resembles the old policy; no intent contradiction
was established. Resource availability is not itself a pathfinding proof.

Community BuildingUpdate old115-122/new155-164 adds an hourly starvation-notification
scan; new Dome.GetFoodServiceFailures:2718-2745 walks residents and allocates a
failure list. Building's update interval is HourDuration (:268). PERF shape,
not measured frame-time harm. Community:533-534 keeps old Starving notification
aliases after the Underfed rename. Colony's tagged funding/initialization rows
and UpgradeUnlocks profile dictionary writes were read; neither requires the
named DLC class to exist. UpgradeUnlocks:99-111 uses literal keys and profile
comparison; ForceLockUpgrade:41-43 writes a dictionary, not a missing preset.

Building.Destroy old1457-1607/new1544-1694 defers dome UpdateColonists via Notify
and drops an explicit Origin attach spot; no missing DLC symbol in that body.
Native default attach placement/notification scheduling was not executed.
GetUIWarning old2775-2874/new2918-3031 handles dome state, recipe assignment,
FoodBuilding consumption and per-grid storage discharge; the referenced base
classes exist. Detailed warning presentation/ordering remains runtime territory.
BuildingBlowUp old3405-3511/new3588-3703 supplies C62's discarded list; actual
scenario reach is still U.

SavegameFixups.RecreateInteriorVolumesOnBuildings new4062-4115 conditionally
appends FarmInsect and PanoramicRestaurant only when g_Classes contains them.
Assigning nil at `#args+1` does not introduce a hole before the next append;
the callback stays after the dense arguments. Base OpenPasture, NaturalistHabitat,
LowGLab and PassageHub are not missing DLC classes. CommonLua/SavegameFixup.lua
:10-16 marks current fixups applied for new games; :24-39 runs only unapplied
ones. These are not newly recurring fresh-game colony scans.
ConstructionSite.lua:2098 was read as supporting evidence only: its FungalFarm
hint names a base class, not FungalFarmBase. There is no tagged ConstructionSite
body in this 03 set.

### callers

Six CALLERS items have both enclosing caller and contract read: C00579 (Dome)
and C00731-C00735 (Farm). C00595-C00597 have ResourceStockpile receivers whose
own GetCubePosRelative exists (new607); Station's same method name does not make
these Station calls. C03968's WasteRock call uses the optional default. These
four are `line-checked-body-pending`, deliberately assigned to 03d for the
surrounding body/callee-chain review. Twenty other CALLERS items are pending.
This conservative accounting does not turn an incidental Colonist/cargo call
excerpt into an independently completed contract audit.

### remaining

The exact keys, source lines, FR tags and owners are in SEAM_COVERAGE.tsv.
Reason for every pending item: the required ~400-row split, not clearance.
03b owns all generated inventory and field-level presets, including material
cited incidentally above; 03c owns remaining Factions files and the enumerated
research/tech/mission/progression files in tools/seam_coverage.py; 03d owns all
other remaining hand rows plus the 18 original NOROWS files. Caller-only owners
follow the caller file, with six explicitly completed items removed first.
TAKEABLE WHEN each first-class continuation is run on the unchanged pin. They
may run independently of 04 and each other with coordinated shared writes;
no continuation may consume another's rows by silently changing the original tags.

## For dlccheck — base-side verdicts and unresolved dependency boundaries

The five read-group sections above are the full base-side seam contract; they
do not rule on whether DLC is mostly additive. Reuse their cited base bodies;
re-derive any actual DLC caller/override rather than inheriting base behavior.

| seam | base-side verdict | remaining DLC work / TAKEABLE WHEN |
|---|---|---|
| services, resource groups, meals, ingredients | base service migration executes without norman; ingredient mask is empty for ordinary Food; C57 conditional | DLC chain reads real ingredient registration, override and meal path |
| recipe inputs and storage | base classes/readers exist, concrete base recipe not established; reservation-vs-input debit unresolved | DLC chain opens recipe, building template, accessible Food pile and selection/consume route together |
| crop outputs, growth, producer hooks | callback/unit migrations have base counterparts; C59 literal caller absent | DLC subclasses are read against the new producer/crop contracts; inspect augmentation instances |
| FungalFarm / InsectFarm | base FungalFarm is not DLC FungalFarmBase; upgrade names are dictionary keys; intentional-underground counterevidence exists | full DLC class plus tech/template gate read; do not infer dependency from spelling |
| ranch meals/output/panel | base ranch route supports C56/C60; recipe/ingredient additions are conditional | DLC animal/meal overrides read, then an attended fresh fixture/profiling observation |
| spoilage and reservations | C58 ordinary Food path needs no DLC; downstream native result unmeasured | real fresh fixture straddles spoilage hook; DLC stockpile overrides require separate reading |
| colonist/dome food assignment | explicit base Eat callers adapted; connected-dome path exists | dynamic AssignMeals, specialized dining/enter/abort overrides are opened |
| Building fixup and UpgradeUnlocks | named conditional g_Classes checks / dictionary writes do not prove nil dereferences | DLC-only classes and loaded profile effects read separately |
| deaths / applicants | C61 base Lua mutation/handler enumeration contradicts old popup claim | DLC death hooks/overrides checked before extending base conclusion to all owners |
| research/laws/policies/cargo and other registries | not drained by 03 | 03b/03c/03d complete their explicit rows before DLC kickoff/99 |

MEASURED guard re-derivation: literal `IsDlcAvailable("norman")` calls in base
Lua alone = **3**, thomas = **1**. Including base Data = **10/1**. Norman hits:
Data/FlightPolicyDef.lua:160/:183/:290/:474/:500; Lua/Buildings/FoodServiceBuilding.lua:614;
Lua/XDef/sectionFoodService.generated.lua:46/:65; Data/XDef/sectionFoodService.lua:32/:43.
Thomas: Lua/Factions/Factions.lua:1393 (body deferred to 03c). The brief's 3/1
was accurate for Lua, not the whole Lua+Data base scope. Its inherited
"references in 12 files" lacks a reproducible name/dependency predicate and
is not used as a dependency proof. UI guards gate labels; they do not establish
that all service logic is DLC guarded. Preset guard bodies remain 03b work.

## FR-1(b), FR-2, FR-3

**FR-1(b):** original 03 has 10 FR-1(a) rows and zero measured explicit
DLC-guarded FR-1 rows. This pass read R05598 (Community underfed state), R07542
(Colony initialization) and R07544 (sponsor funding), with their present old/new
spans. These base bodies do not require owning norman; they remain on the
non-owner path where instantiated. No native/new-game crash is confirmed or
excluded. The other seven FR-1 rows are pending in the continuation receipt;
this subsection is not a ten-row clearance. FR-1's temporal-upscaler lead stays
with 04. Disabling DLC does not erase changed base code.

**FR-2:** none of the seven tagged 03 FR-2 rows was in this slice. 03c owns
four research/tech/mission consumers, 03d the other three tagged bodies;
03b owns relevant presets. Deep-scan progression is
not answered here.

**FR-3:** 11 of the original 21 tagged rows were read (13 unique FR rows total
in the current slice, overlapping FR-1). C60 is the hard dead-allocation tell.
Community hourly resident scans, colony-wide farm synchronization, widened pet
dome enumeration and recipe selection loops were noted as PERF shapes; no
hard unintended cost or root cause was established. ResourceStockpile.GameInit
changes closure capture to an explicit self argument, not a new periodic thread.
Fixups are not recurring new-game work. The 2025 report predates 1.1.0, so added
work cannot establish its original cause. Checklist 136 and actual profiling
remain necessary; no report was closed.

## Controls and verification

PROBE SWEEP: clean (doccheck and explicit `rg -l TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/`).
`tools/desk_seam_food.py` loads actual archived Lua bodies through deskbench/luafn.
`SEAM_DESK.txt` records the run. The script names shims: rounding, producer collector,
resource registration, localization/UI capture and request scheduling stand-ins.
C56 old Chicken really has food=200; new Chicken's OutputResources contains
Food amount=100. At 48 performance and 25
animals, old producer/forecast = 2400/2400; new = 2500/1200, UI expectation1200.
Zero/full-performance controls agree. A counterfactual identity quantizer makes
the new result1200 and falsifies the discrepancy assertion. This is a desk
mutation control, not a proposed patch. C57 disabled/enabled/empty-registry/vegan
controls exercise the base methods with a synthetic ingredient. C59's gap and
adjacent-slot cases run both versions. None executes the game or DLC loading.

Reader control: **0 eligible seeded positives**, so no seed hit-rate denominator;
01/02's four-seed score is not 03's score. Parent random sample uses a fresh
`random.Random(20260910).sample(rows, 2)` for each original food/farms/resources
TSV group in INVENTORY order. Reproducible six rows: R06416, R06056, R05989,
R06006, R06516, R08365. **6/6 actual-change descriptions agree; route precision
5/6 before correction.** R05989's generic UI route was too broad; a renewed
literal search finds two declarations and zero callers, so its route is now U.
The nil-preset hypothesis is refuted by Farm.lua:15's actual nil guard.
R06006 is reached by UICropUpdate:1096-1098; R06416 needs a real processor/recipe;
R06056 is called by FoodBuilding.Init and migration fallbacks; R06516 is a
one-shot GameInit thread; R08365's Food-consuming parent instance is unresolved.
No sample claims a game behavior PASS or universal non-owner safety.

`SEAM_GATES.txt` records the clean explicit probe sweep, complete final
doccheck/instrument/desk/coverage-verifier outputs, and their exit codes (trailing
spaces stripped from captured log lines; warning text retained). It
preserves doccheck's existing frozen-index advisory lines as well.
Required doccheck, treediff selftest and presetdiff selftest passed at each
commit boundary. A repeated commit-hook warning differed from standalone
doccheck's clean kit check; preserve it verbatim:

```text
  WARN kit-tree state is UNKNOWN on this run — re-run doccheck before trusting a clean kit tree
```

Standalone doccheck was rerun and reported the kit tree clean. No hook change
was made to suppress the warning. Gates do not substitute for candidate runtime
falsifiers, engine semantics or the terminal audit.

## Drift and audit inbox

- User path had an extra directory separator (`03/_SEAM.md`); existing `03_SEAM.md`
  was the resolved task. The required ~400-row split was taken, not treated as
  permission to call 2,907 inventory/preset rows finished.
- Guard count scope differs as documented above. Original tagged ledgers were
  not retagged and no new untagged body was reassigned away from 04.
- Food chaser enumerated eight DLC ingredient definitions and recipe excerpts
  beyond the single-function base-call fence. This scoped lookup was broader
  than the brief permits; no DLC behavior clearance rests on it and further DLC
  reading stopped. The pending DLC routes remain explicit.
- Initial ranch reasoning predicted a zero output; reading the positive minimum
  in RoundResourceAmountToTenth (Resources.lua:78-83) refuted it. An initial old1200 comparison ignored old
  Chicken food=200; actual-preset desk execution corrected old to2400 before filing.
  Chaser also corrected old lifecycle/UI line citations before filing.
- Initial C57 consumer search named one caller; MicroGHabitat made it two.
  Ingredient registry is populated by group==MealIngredients, not an invented
  is_ingredient flag. FoodResources is a separate wider registry. All corrected
  before initial filing. Final QA refined the supply-drain citation to354-376.
- Initial desk read assumed old FoodServiceBuilding existed and raised FileNotFound;
  absence is now a checked control, not a fabricated old delicacy comparison.
- Parent rejected the stock-Lua string-concat and Research dot-self false positives.
  EF-005 prevents stock-Lua nil/false iteration from becoming an engine crash claim.
- Resource chaser initially excluded Hungry from the fallback recipe; parent traced
  the truthy flag and corrected it. Final wording removes ambiguous "starving" and
  spells out the old clamp rather than quoting an abbreviated expression.
- C61's no-desk explanation was too categorical. A shimmable death harness is
  possible; none was run. Such a harness cannot enumerate unknown runtime handlers.
  Owner exposure is now explicitly conditional on uninspected overrides.
- Bulk-output truncation was caught; parent reread both complete Building.Destroy
  and GetUIWarning counterparts before counting them full. The random sample
  narrowed GetCropName's supposed UI route to no literal caller found.
- First coverage-generator run used `file` for NOROWS; its actual column is `path`.
  It failed before writing; corrected and rerun. Source instruments and tagged
  inputs were not modified.
- The receipt verifier initially compared raw bytes despite this clone's CRLF
  checkout policy. Before commit it was changed to compare newline-normalized
  text, so a later checkout cannot produce false receipt drift.
- Staged whitespace checking flagged valid empty terminal TSV cells and raw
  trailing spaces in the selftest log. The same empty FR cells are retained,
  with the evidence field moved last; only trailing log spaces were trimmed.
  The receipt verifier was rerun after the serialization change.
- Final synthesis QA corrected method names (AssignMeals,
  ProducerModifyCalcProductionAmount, SyncProducerSlots, RoundResourceAmountToTenth),
  the Laws.lua path, ingredient count versus mask, old/new Chicken field shapes,
  and which growth helpers changed units. Scratch count printing had an unmatched
  parenthesis; a patch briefly appended a stray sentence. Both were corrected
  before close-out. The TXT records results; shim definitions are in the script.
  A final prose-spacing helper also failed to match a Unicode section marker
  through PowerShell stdin; an explicit Unicode escape fixed the read, before writes.
- The first two commit messages omitted the required explicit PROBE SWEEP line.
  Before relying on the result in close-out, the parent reran the explicit clean
  sweep, the desk control and all chain gates; the close-out commit records it.
- The hook kit-tree warning above recurred although standalone checks were clean.
  99 must retain this limitation instead of reporting a warning-free commit hook.

Blind spots remain: absent assets/localizations, native engine and timing, console
platforms, actual execution, incomplete old DLC, anonymous/dynamic callers, and
presets consumed only in native code. Body reading and the desk controls do not
close any of them. **99 waits for 03b, 03c, 03d and 04 (and any declared children)
before the DLC deep-check kickoff.**
