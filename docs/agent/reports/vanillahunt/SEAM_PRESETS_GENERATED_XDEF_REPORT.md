# vanillahunt 03b — generated XDef / BuildingTemplate read-only audit

Date: 2026-09-10. Reader: `/root/03b_food_presets`. This is a source-reading
receipt, not a defect verdict. No game was launched and no repository, tagged
TSV, source archive, or installed-game file was changed.

## Scope, pin, and method

- Old (`O`): `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src`.
- New (`N`): `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.
- Exact filter: `SEAM_COVERAGE.tsv surface==INVENTORY && owner==03b` and file
  under `Lua/XDef/` or `Lua/BuildingTemplate/`, joined by key to
  `INVENTORY.tagged.tsv`.
- Receipt: coverage rows 84, unique coverage keys 84; joined inventory rows 84,
  unique joined keys 84; 82 `Lua/XDef` + 2 `Lua/BuildingTemplate`; 61 unique
  generated files. Missing keys 0, duplicate keys 0, extra keys 0.
- Kinds: 61 body, 17 added, 6 removed. Flags: 63 blank, 16 `NEWFILE`, 3
  `GONEFILE`, 1 `INDENTED`, 1 `INDENTED,ONE-LINE`.
- Every declared present span was read from first through last line, not merely
  its diff hunk. Every corresponding `Data/...` authoring twin was read in both
  trees where present. Each span bound was checked against the real file.
- Runtime direction: `CommonLua/X/XDef.lua:284-314` generates the companion
  class file from the Data XDef. `CommonLua/X/XTemplate.lua:1496-1508`
  preferentially instantiates a generated XDef class through `class.new`; the
  `Data/XDef` object is therefore the authoring twin, not a second runtime UI
  effect. `CommonLua/X/XShortcuts.lua:35-63` is the concrete registry reader
  for shortcut XDefs.
- In the ledger, `twin O/N`, `O/-`, or `-/N` means the Data twin has exactly the
  same lifecycle as the generated file. The twin path is obtained by replacing
  `Lua/` with `Data/` and `.generated.lua` with `.lua`.
- Reach labels follow FIX_POLICY §4: R1 normal player route, R2 conditional
  content/state, R4 absent new route, U not established from Lua. No runtime
  claim is made from those labels.

## Generated/Data twin reconciliation

All 61 generated files have the expected Data twin on every side on which the
generated file exists: 47 `O/N`, 3 `O/-`, 11 `-/N`; mismatches 0.

- `O/-`: `CommandCenterLifeSupportGridsOverview`,
  `CommandCenterLifeSupportGridsOverviewRow`, `ResearchDlg`.
- `-/N`: `CommandCenterOxygenGridsOverviewRow`,
  `CommandCenterWaterGridsOverviewRow`, `RolloverCropItem`,
  `RolloverRecipeIngredientHex`, `RolloverRecipeItem`, `XTechTree`,
  `sectionFactoryResearch`, `sectionFoodProducerStoredResources`,
  `sectionFoodService`, `sectionRecipeProductionBuilding`,
  `sectionResourceGroupStorage`.
- `O/N`: the other 47 files, including `FungalFarm_Asteroid`, the Power row,
  all law/politics and payload screens, all custom infopanels, and all remaining
  sections.

The two apparent removals are presence-side enumerated. The old combined life
support dialog/row becomes separate Power, Water, and Oxygen overview classes;
`Data/XDef/ColonyControlCenter.lua:90-104` and generated
`Lua/XDef/ColonyControlCenter.generated.lua:76-88` instantiate all three. The
old `ResearchDlg` becomes `XTechTree`; old `Lua/Research.lua:1201-1212` opens
`ResearchDlg`, while new `Lua/Research.lua:844-868` opens/closes `XTechTree`.

## Per-row ledger

Falsifier shorthand used below: **screen** = perform the named player action in
both builds with the stated state and compare visible text/state/click result;
**class** = instantiate the generated class with a controlled real context and
record method calls/fields; **absence** = search/load the new registry and show
the named class is not instantiated or that its replacement does not cover the
capability; **profile** = instrument call count/time during the named UI action.
These are recipes only; none was run.

### BuildingTemplate and Command Center

| key | file / function; class; lines O → N; twin | actual change | consumer, reach/action, falsifier | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|
| R05272 | `Lua/BuildingTemplate/FungalFarm_Asteroid.generated.lua` `Value@bb968b`; removed (e), one-line; 16 → —; twin O/N | Removes the nested value function used by the old template condition. | `BuildingTemplates` is read by construction (`Lua/Construction/Construction.lua:747,1090`) and the building remains unlocked by `Data/LawDef/LawDef-Research.lua:1915`; R2, own/unlock Space Farming and build asteroid farm; class/absence. | Old template-local condition → no template condition while the building body remains. Non-owner has the base definition but no established constructible asteroid route. Old one-line span is valid and distinct from R05273. No surviving tell; no SMELL/PERF. |
| R05273 | same file `eval@bb968b`; removed (e), indented; 12-14 → —; twin O/N | Removes old `IsTechResearched("SpaceFarming")` condition evaluator. | Same reader/reach/falsifier as R05272. | Same seam; new preset also changes storage, grid inputs, category/environment/work type outside these two nested spans. Non-owner route not established. No tell; no SMELL/PERF. |
| R11216 | `CommandCenterBuildingOverviewRow.Init`; body (a); 17-258 → 17-305; twin O/N | Rescopes the three workshift rows, passes `context` explicitly into their real-time setup thread, and adds Heavy Workload controls. | Instantiated by `CommandCenterBuildingsOverview.generated.lua:620`; R1, open Command Center > Buildings; screen/class. | Old captured context and shift-only UI → explicit thread argument plus law-aware workload toggle. Base UI; no DLC symbol. Explicit argument passage is a sibling-style correctness cue for the old path, not a new hard tell. Loops are fixed at three shifts; no PERF concern. |
| R11218 | `CommandCenterCategories.Init`; body (a); 11-409 → 11-409; twin O/N | Replaces per-resource formatters with generic `resource(GetAvailable(...))`; Seeds visibility now uses `IsSeedsResourceAvailable`. | `ColonyControlCenter.generated.lua:40`; R1, open Command Center categories; screen. | Old hard-coded availability tags/tech proxy → registry-aware resource reader. Non-owner gets only visible/available resources. No hard tell; finite category UI, no PERF. |
| R11225 | `CommandCenterDomeOverviewRow.Init`; body (a); 14-525 → 14-453; twin O/N | Reorders/hides deprecated passage toggles, removes Birth Restrictions law gating from birth policy, modernizes stat/immigration presentation. | `CommandCenterDomesOverview.generated.lua:218`; R1, Command Center > Domes; screen in birth/passages states. | Old law-gated birth control and two live passage controls → always-enabled birth control with deprecated passage controls hidden. Base UI; no named DLC dependency. Comments explicitly say both passage controls are deprecated (intent tell for removal, not a surviving defect); no PERF. |
| R11229 | `CommandCenterLifeSupportGridsOverview.Init`; removed (e); 12-164 → —; twin O/- | Removes combined life-support overview. | Replacement consumers are `ColonyControlCenter.generated.lua:82,88`; old route R4 in N, replacement R1 via Command Center Water/Oxygen; absence/screen. | Combined water+oxygen screen → two screens. Base feature. Presence side enumerated; no hard tell, old child loop bounded. |
| R11230 | `CommandCenterLifeSupportGridsOverviewRow.Init`; removed (e); 15-232 → —; twin O/- | Removes combined row that rendered both life-support grids. | Replaced by R11234/35 and R11248/49, each instantiated by its overview at line 125-126; R4 old/R1 replacements; absence/screen. | Combined row → per-resource rows. `SupplyGrid.lua:1018` states water and air share the life-support overlay, explaining both replacement rows' overlay route. Base; no tell/PERF. |
| R11234 | `CommandCenterOxygenGridsOverviewRow.Init`; added (f); — → 15-82; twin -/N | Adds Oxygen row layout. | `CommandCenterOxygenGridsOverview.generated.lua:125-126`; R1, Command Center > Oxygen grids; screen/class. | No old class; prior behavior was combined row. Base; no DLC. No tell/PERF. |
| R11235 | same file `OnContextUpdate`; added (f); — → 84-119; twin -/N | Computes oxygen balance, production, consumption, stored/capacity and warning styling. | Same overview; R1, open with positive/negative oxygen grids; class. | Generic SupplyGrid methods → oxygen formatting; double-click uses the shared life-support overlay. Base; no tell; constant work per row. |
| R11239 | `CommandCenterPowerGridsOverviewRow.Init`; body (a); 15-97 → 15-82; twin O/N | Simplifies Power row layout; computation moves to explicit update method. | `CommandCenterPowerGridsOverview.generated.lua:125-126`; R1, Command Center > Power grids; screen/class. | Template-bound old values → handler-populated values. Base; no tell/PERF. |
| R11240 | same file `OnContextUpdate`; added (f); — → 84-119; twin O/N | Adds explicit balance/production/consumption/storage formatting and deficit warning. | Same consumer; R1, open a power grid; class. | Old implicit bindings → explicit SupplyGrid calls. Base; no tell; constant work per row. |
| R11248 | `CommandCenterWaterGridsOverviewRow.Init`; added (f); — → 15-82; twin -/N | Adds Water row layout. | `CommandCenterWaterGridsOverview.generated.lua:125-126`; R1, Command Center > Water grids; screen/class. | No old class; combined-row predecessor. Base; no tell/PERF. |
| R11249 | same file `OnContextUpdate`; added (f); — → 84-119; twin -/N | Adds water balance/production/consumption/storage and warning update. | Same consumer; R1, open positive/negative water grid; class. | Explicit water view; double-click deliberately uses shared life-support overlay. Base; no tell; constant work per row. |

### Global HUD and shortcuts

| key | file / function; class; lines O → N; twin | actual change | consumer, reach/action, falsifier | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|
| R11268 | `GameShortcuts.Init`; body (a); 12-2084 → 12-2143; twin O/N | Broad shortcut regeneration: `GetVisible`→`IsVisible`, centralized speed APIs, adds building-variant shortcuts, makes resource-icon action developer-only, tightens control/route actions. | `CommonLua/X/XShortcuts.lua:35-63` enumerates XDef `Shortcuts` presets and constructs their classes; R1, use mapped keyboard/gamepad actions; screen. | Old direct state manipulation → shared APIs and new actions. Base registry; debug actions remain platform-gated. No single surviving hard tell; loops walk bounded action/button lists. |
| R11278 | `HUDMiddle.Init`; body (a); 18-417 → 18-426; twin O/N | Adds HUD notification updates, new research/resupply rollovers, Politics enable helper/shortcut id, fixes Assembly image spelling, renames Hints affordance Encyclopedia. | `HUD.generated.lua:383` constructs `HUDMiddle`; R1, ordinary HUD buttons; screen. | Old static bindings → notification-aware buttons. Base; Politics helper owns availability. Old Cyrillic `е` in `mars_assеmbly.png` versus new ASCII asset spelling is a strong correction tell, with no surviving new tell. Constant button count. |
| R11290 | `InfobarUI.Init`; body (a); 19-863 → 19-1149; twin O/N | Makes research opening modal-safe, switches Tech Point icon, separates Water/Oxygen buttons and hover grid selection, uses dynamic basic/advanced/other resource arrays, and adds Fuel/Food/Delicacies groups. | `Lua/X/Infobar.lua:84-86` opens/closes `InfobarUI`; R1, view/click infobar; screen across resource availability. | Fixed resource layout and combined life-support → registry-driven layout and distinct resource buttons. Norman Delicacies are gated by nonempty ingredient registry; Seeds by `IsSeedsResourceAvailable`; non-owners retain base resources. No hard tell. UI loops over finite resource registries; no unbounded hot-loop tell. |

### Laws and politics

All rows below are generated XDef UI classes consumed by `PoliticsDlg` and the
Legislature. `Lua/Factions/Elections.lua:17-28` opens/closes `PoliticsDlg`;
`PoliticsDlg.generated.lua` constructs the cards/entries. Their normal route is
R1 when Politics is enabled: open Politics, prepare/select/vote/revoke a law.
The falsifier for each is the matching **screen** state plus a controlled
Legislature method-call trace. These base files contain no direct DLC class
reference; availability is owned by Legislature/HUD state.

| key | file / function; class; lines O → N; twin | actual change | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|
| R11304 | `LawDevelopCard.Init`; body (a); 15-233 → 15-243; twin O/N | Resizes text, nil-hardens description, uses `CanBeginPolicyPreparation`, and calls `BeginPolicyPreparation` + `ApplyOfferAgenda`; adds disabled warning. | Old session-action preparation → timed policy preparation API. Base. “Missing description” is fallback text, not a defect marker. No PERF. |
| R11305 | `LawDevelopCard.OnContextUpdate`; body (a); 235-263 → 245-275; twin O/N | Clears vote-prediction UI when no single-law policy. | Old stale/implicit empty state → explicit empty update. Base. Sibling/self-contradiction cue supports the correction; no surviving tell/PERF. |
| R11306 | `LawDevelopCard.OnDelete`; removed (e); 271-278 → —; twin O/N | Removes card-local clearing of offered prepare agenda. | Card cleanup → dialog-level ownership (`PoliticsDlg.Open/Close`, R11409/R11401). Base. Presence side enumerated; no surviving tell. |
| R11308 | `LawEntry.GetRolloverLaws`; body (a); 213-229 → 216-232; twin O/N | Includes law list for locked state instead of suppressing it. | Locked UI becomes informative. Base. No tell/PERF; loop bounded by laws in one policy. |
| R11309 | `LawEntry.GetRolloverPostLawsText`; body (a); 231-256 → 234-262; twin O/N | Rewrites locked explanation and adds timed “preparing” state. | Old visible/prepared/enacted states → preparation lifecycle. Base. No tell/PERF. |
| R11312 | `LawEntry.GetState`; body (a); 158-169 → 168-182; twin O/N | Adds `IsPolicyPreparing` between prepared and raw state. | Session-action inference → Legislature-owned preparation state. Base. No tell/PERF. |
| R11313 | `LawEntry.Init`; body (a); 30-69 → 30-81; twin O/N | Adds active/preparing icon layout. | New preparing state gains an affordance. Base. No tell/PERF. |
| R11314 | `LawEntry.OnContextUpdate`; body (a); 71-104 → 83-120; twin O/N | Renders locked/preparing images explicitly and hides obsolete lock glyph. | New state enum → revised visuals. Base. UI rendering requires screen falsifier; no source-only verdict. No PERF. |
| R11315 | `LawEntry.OnPress`; body (a); 106-132 → 122-142; twin O/N | Removes early locked rejection and routes prepared/preparing/other to voting/in-development/develop. | Old local lock gate → mode chosen by Legislature state and enabled control. Base. Hit-testing/input validity remains runtime-only; no hard tell. |
| R11316 | `LawInDevelopmentCard.Init`; body (a); 15-162 → 15-164; twin O/N | Taller layout, multiline sizing, nil-safe description. | Static card → timed preparation presentation. Base. No tell/PERF. |
| R11317 | `LawInDevelopmentCard.OnContextUpdate`; body (a); 164-182 → 166-184; twin O/N | Adds formatted remaining preparation time to title. | Old name-only state → live timer. Base. No tell/PERF. |
| R11318 | `LawVoteDropdownList.Open`; body (a); 29-67 → 29-71; twin O/N | Adds Trait targets and uses generic target preset/name helpers plus rollovers. | Faction/Tech-only target selection → Faction/Tech/Trait. Base registry; a missing target would be falsified on screen. List bounded by target candidates. |
| R11319 | `LawVotingBar.GetRolloverFactionsOpinions`; body (a); 219-230 → 236-247; twin O/N | Passes `"votes only"` to opinion formatter. | General faction opinion → vote-specific display. Base. No tell/PERF. |
| R11321 | `LawVotingCard.Init`; body (a); 15-593 → 15-617; twin O/N | Adds trait/selected-target display, affordability/cooldown warnings, uses `EnactLaw`/`RevokeLaw`/`ApplyOfferAgenda`, and revises vote-preview state. | Old direct session fields/`EndSession` → Legislature public actions. Base. No surviving hard tell; quest/law loops are bounded UI work. |
| R11322 | `LawVotingCard.OnDelete`; body (a); 660-671 → 684-691; twin O/N | Stops clearing offered enact agenda locally while still clearing selected action state. | Cleanup ownership moves to `PoliticsDlg.Open/Close`. Base. Presence side enumerated; no tell/PERF. |
| R11393 | `PolicyEntry.SetRollover`; body (a); 68-89 → 68-88; twin O/N | Calls `UpdateVotePredictionUI(..., not rollover)` so rollover-off explicitly renders empty mode. | Implicit hide → explicit empty prediction. Base. No tell/PERF. |
| R11394 | `PolicyEntryActive.GetRolloverFactionsOpinions`; body (a); 186-188 → 194-199; twin O/N | Resolves wrapped context and decides whether to show prediction for active/targeted law. | Direct `self.context.id` → `ResolvePropObj` and state-aware formatter. Base. No tell/PERF. |
| R11395 | `PolicyEntryActive.GetRolloverText`; body (a); 179-184 → 180-192; twin O/N | Appends unaffordable upkeep text for inactive laws. | Vote text → vote plus cost constraint. Base. No tell/PERF. |
| R11396 | `PolicyEntryActive.OnContextUpdate`; body (a); 69-99 → 69-101; twin O/N | Disables visual state on policy cooldown or unaffordable upkeep. | Law conditions only → conditions + cooldown/cost. Base. No tell/PERF. |
| R11397 | `PolicyEntryActive.OnPress`; body (a); 101-122 → 103-123; twin O/N | Removes old “not in session” early return; selection state is now updated whenever the enabled entry is pressed. | Session-only interaction → preview/selection outside old session model. Base. Input behavior needs screen falsifier. No hard tell/PERF. |
| R11401 | `PoliticsDlg.Close`; body (a); 1307-1320 → 1432-1448; twin O/N | Clears `offered_agenda` on dialog close. | Card-local cleanup → dialog lifecycle cleanup. Base. Explicit symmetry with Open is a hard intent tell for cleanup placement; no surviving defect/PERF. |
| R11404 | `PoliticsDlg.Init`; body (a); 16-1275 → 18-1382; twin O/N | Large regeneration for preparation slots/timers, Open Floor agenda action, upkeep/title rollovers, controller focus, and council explanatory header. | One session-action card → multi-slot timed policy UI and public Legislature APIs. Base. UI correctness is runtime-only. Loops cover active laws, offers, controls, and faction seats; no unbounded simulation loop. |
| R11409 | `PoliticsDlg.Open`; body (a); 1296-1305 → 1417-1430; twin O/N | Clears stale offered agenda and emits `Msg("OpenPoliticsDlg")`. | Old restore-session mode → clean dialog entry plus tutorial/event hook. Base. Paired Open/Close clearing is explicit intent evidence, no surviving tell/PERF. |

### Payload, resupply, research, and rollovers

| key | file / function; class; lines O → N; twin | actual change | consumer, reach/action, falsifier | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|
| R11356 | `PGMissionPayloadRemastered.Init`; body (a); 24-466 → 24-431; twin O/N | Adds explanatory rollover, uses percent formatter, counts already-owned prefabs, replaces hand-built title decoration, adds gamepad details action. | `PGMission.generated.lua:33` and `Resupply.generated.lua:68`; R1, pregame payload/resupply cargo; screen with owned prefab. | Static cargo list → ownership-aware count and shared decoration. Base. No tell/PERF; list bounded by payload items. |
| R11357 | same file `Open`; body (a); 472-521 → 437-489; twin O/N | Adds gameplay Resupply help, uppercases destination, and no longer suppresses the Independence hint through `AccountStorage.ShownHints`. | Same consumers; R1/R2 (Independence state), open payload; screen. | One-time hint bookkeeping → state-driven hint. Base file; no direct DLC class. UI behavior needs observation; no PERF. |
| R11375 | `PayloadRequest.Init`; body (a); 17-423 → 17-423; twin O/N | Passes `self` explicitly into the selection thread; otherwise generated layout is stable. | Spawned inside automatic/manual payload request dialogs; R1/R2, choose payload item; class/screen. | Captured receiver → explicit thread parameter. Base. Strong sibling-style correctness cue for async lifetime, no surviving tell/PERF. |
| R11379 | `PayloadRollover.Init`; body (a); 15-266 → 15-193; twin O/N | Uses shared `RolloverTitleSection`, adjusts cap frame on layout, and changes title style. | `PropPayload.generated.lua:8` and `PropManualPayload` select `PayloadRollover`; R1, hover payload; screen. | Bespoke title subtree → shared component. Base. Rendering is runtime-only; no PERF. |
| R11411 | `PropPayload.Init`; body (a); 17-164 → 17-168; twin O/N | Adds repeat timing to plus/minus payload buttons. | `PGMissionPayloadRemastered.generated.lua:318` and PG challenge payload construct it; R1, hold payload buttons; screen. | Single clicks → repeating input. Base. Hit-testing/repeat timing requires runtime; no hard tell/PERF. |
| R11413 | `ResearchDlg.Init`; removed (e); 12-1256 → —; twin O/- | Removes old research dialog. | New `Lua/Research.lua:844-868` opens `XTechTree`; old `Lua/Research.lua:1201-1212` opened `ResearchDlg`; R4 old/R1 replacement, click Research; absence/screen. | Old project queue dialog → Tech Point/Wishlist tree. Base. Presence side complete; no tell. |
| R11421 | `ResupplyCategories.Init`; body (a); 14-391 → 14-431; twin O/N | Explicit cargo/passenger tutorial modes, passenger asteroid destinations, Space Elevator payload handoff, and revised pod/lander availability/rollovers. | `Resupply.generated.lua:56`; R1 base cargo/passenger, R2 asteroid/independence/elevator; open Resupply category; screen/class. | Boolean cargo tutorial and direct elevator cargo → typed rocket mode and object-driven payload. Nonowners cannot reach asteroid-only routes but base categories remain. No hard tell; destination loops bounded by landing spots. |
| R11424 | `ResupplyDestinations.Init`; body (a); 16-204 → 16-231; twin O/N | Adds passenger capacity/cost, direct lander dispatch, passenger destination branch, and purchase cancellation on Back. | `Resupply.generated.lua:62`; R1/R2, choose rocket/lander destination; screen/class. | Cargo-only destination flow → cargo/passenger/lander paths. Nonowner base cargo remains; asteroid branch requires lander. Dev comments explicitly state lander skips payload but pays destination cost and Back cancels purchase—intent tells, no surviving defect. |
| R11441 | `RolloverCropItem.Init`; added (f); — → 13-204; twin -/N | Adds crop-specific rollover title/description/traits/text/hint layout. | `sectionCrop.generated.lua` sets `RolloverTemplate="RolloverCropItem"`; R1, open farm crop selector and hover crop; screen. | Generic old rollover → crop-specific presentation. Base; no DLC dependency. No tell/PERF. |
| R11444 | `RolloverRecipeIngredientHex.OnContextUpdate`; added (f); — → 49-71; twin -/N | Resolves Resource/group styling, icon fallback, and amount visibility. | Constructed by `RolloverRecipeItem` for each input/output; R2, hover recipe in recipe producer; class/screen. | No old component; generic text preceded it. Base Resource registry; no tell, constant per hex. |
| R11445 | `RolloverRecipeItem.Init`; added (f); — → 17-418; twin -/N | Adds recipe input/output hexes, disabled text, and colony-available totals; group totals iterate leaf resources. | Selected as recipe-row rollover by `sectionRecipeProductionBuilding`; R2, build recipe producer and hover recipe; screen/profile. | No old class; replaces generic recipe text path. Base class, content-dependent. No hard tell. Work is bounded by one recipe's inputs and group leaves; PERF observation below threshold. |
| R11506 | `XTechTree.DoSearch`; added (f); — → 827-843; twin -/N | Fuzzy-searches translated, tag-stripped name and description of every `Tech`, caps results over 100, modifies dialog. | Search box/actions inside `XTechTree`; R1, Research > Search and type; screen/profile. | No old search path. Base. No hard tell. **PERF observation:** every query scans/translates every Tech preset; UI-only and finite, but profiling per keystroke is the falsifier. |
| R11508 | `XTechTree.Init`; added (f); — → 14-781; twin -/N | Adds full Tech Point/Wishlist research tree UI, initial-tech selection, zoom/section/search actions and research accounting. | `Lua/Research.lua:851` opens the class; R1, click Research; screen. | Replaces R11413 old dialog. Base. No hard tell. UI loops initial tech ids only; no separate PERF tell beyond R11506. |

### Custom infopanels

`Lua/XDef/sectionCustom.generated.lua:15-34` is the actual reader for every
`custom*` row below: it resolves `XDefs["custom"..context.class]`, falls back
through `BuildingTemplates[context.class].object_class`, then calls
`XTemplateSpawn`. Thus each route is the selected object's infopanel, and a
non-owner without the relevant object never constructs that custom class.

| key | file / function; class; lines O → N; twin | actual change | reach/action and falsifier | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|---|
| R11523 | `customJumperShuttleHub.Init`; body (a); 11-129 → 11-129; twin O/N | Corrects transport-mode rollover markup/alignment. | R2, select Jumper Shuttle Hub; screen. | Text-only; object-gated for nonowner. No tell/PERF. |
| R11524 | `customLanderRocket.Init`; body (a); 11-178 → 11-178; twin O/N | Aligns launch status, changes “commanded” to “controlled,” shows current/max drones. | R2, select asteroid lander; screen. | Presentation-only; nonowner lacks lander route. No tell/PERF. |
| R11526 | `customMagneticFieldGenerator.Init`; body (a); 10-41 → 10-34; twin O/N | Replaces selected-project progress/action with Tech Point progress on `UIPlayer`. | R2, select Magnetic Field Generator; screen. | Old research queue model → Tech Points. Object-gated nonowner. No tell/PERF. |
| R11529 | `customRocketExpedition.Init`; body (a); 11-439 → 11-439; twin O/N | Changes drone wording and count to current/max. | R2, select expedition rocket; screen. | Text/count presentation; content-gated. No tell/PERF. |
| R11531 | `customShuttleHub.Init`; body (a); 11-129 → 11-129; twin O/N | Corrects transport-mode rollover markup/alignment. | R1/R2, select Shuttle Hub; screen. | Text-only; absent object means no construction. No tell/PERF. |
| R11532 | `customSpaceElevator.Init`; body (a); 11-107 → 11-66; twin O/N | Replaces manual Resupply/export toggle with Automated Payload, next-course, load and unload manifests. | R2, build/select Space Elevator; screen/class. | Old instant resupply/export → automated courses. Object-gated. No tell/PERF. |
| R11534 | `customSupplyRocket.Init`; body (a); 11-261 → 11-261; twin O/N | Formatting/drone count updates; Seeds button now uses `IsSeedsResourceAvailable`. | R1, land/select supply rocket; screen. | Tech-name proxy → resource availability. Base rocket; nonowner sees only available resources. No tell/PERF. |
| R11535 | `customTradePad.Init`; body (a); 13-188 → 13-187; twin O/N | Uses `GetEnvironment(CurrentMap)`, `MissionSponsors`, and per-resource-scale black-market price formula. | R2, select active Trade Pad and change offer amount; class/screen against `TradePad.lua:7,109-131`. | Old mapdata/default preset/max-trade normalization → runtime environment/sponsor/per-unit scale. Object route conditional; no direct DLC symbol. New formula agrees with `TradePad.lua:122` consumer. No tell/PERF. |
| R11536 | `customUniversalRocket.Init`; body (a); 11-172 → 11-335; twin O/N | Adds drone pack/unpack, destination, refuel/return/auto-takeoff, per-resource export rows, expected funding, service area and reordered upgrades; load-manifest API changes. | R1/R2, select a supported universal rocket in each state; screen/class. | Sparse generic rocket IP → stateful universal actions. Base class with subtype capabilities; nonowners do not construct absent subtype routes. Export list bounded by returned resources; no tell/PERF. |

### General infopanels and sections

The principal consumer is `Lua/XDef/Infopanel.generated.lua`, which instantiates
registered infopanel content; `ipBuilding.generated.lua` directly constructs
the section classes named below. Where a narrower consumer exists it is cited.

| key | file / function; class; lines O → N; twin | actual change | consumer, reach/action, falsifier | seam; non-owner; tell / SMELL / PERF |
|---|---|---|---|
| R11538 | `ipBuilding.Init`; body (a); 18-452 → 18-493; twin O/N | Guards rocket upgrade/service sections, gates crop/workplace sections, adds food/recipe/multi-storage/factory-research sections, and makes salvage/refab/rebuild UI dynamic; removes Decommission tech gate. | Infopanel content root; R1, select buildings across supported classes; screen/class. | Old static class assumptions → capability/context guards. Base; Norman-specific Now Serving remains internally guarded. No hard tell; construction cost is fixed per open. |
| R11540 | `ipConstruction.Init`; body (a); 11-253 → 11-258; twin O/N | Uses percent formatters/dynamic shortcut names and changes construction section icon with error state. | Construction infopanel; R1, place valid/invalid construction and cycle variant; screen. | Literal key hints/static icon → bindings/state-aware UI. Base. No tell/PERF. |
| R11541 | `ipDrone.Init`; body (a); 16-177 → 16-171; twin O/N | “Reassign All”→“Reassign multiple,” “Commanded”→“Controlled,” and replaces custom title-hiding Open handlers with `ShowRightTitle=false`. | Drone infopanel; R1, select drone; screen. | Presentation refactor. Base. No tell/PERF. |
| R11547 | `ipMultiSelect.Init`; body (a); 16-161 → 16-161; twin O/N | Corrects priority explanation and right-aligns current priority/on-off status. | Multi-selection infopanel; R1, multi-select buildings; screen. | Text-only, base. No tell/PERF. |
| R11557 | `sectionBottomlessPitResearchCenter.Init`; body (a); 17-111 → 17-121; twin O/N | Adds Tech Point progress title/rollover/progress bar. | Constructed from building IP for Bottomless Pit center; R2, select it; screen. | Old Status → Tech Point research. Object-gated for nonowner. No tell/PERF. |
| R11559 | `sectionConsumption.Init`; body (a); 20-49 → 20-53; twin O/N | Adds `idRecipeInput` text target. | `ipBuilding` consumption section; R1/R2, select resource/recipe consumer; screen. | Adds recipe-aware output slot. Base. No tell/PERF. |
| R11560 | `sectionConsumption.OnContextUpdate`; body (a); 51-53 → 55-58; twin O/N | Uses `UpdateUISectionConsumption` return to hide empty section. | Same; R1/R2, select consumer with/without text; class. | Ignored return → visibility contract. This is a dead-result/sibling-style hard intent tell for the old presentation, no surviving new tell; constant work. |
| R11561 | `sectionCrop.Init`; body (a); 16-113 → 16-108; twin O/N | Uses `RolloverCropItem`, recipe-style production text, hides soil/storage block for hydroponics, and removes stored-resource line now owned by new section. | `ipBuilding.generated.lua:43`; R1, select farm/crop; screen. | Monolithic crop/storage → crop selector + `sectionFoodProducerStoredResources`. Base. No tell/PERF. |
| R11562 | `sectionDome.Init`; body (a); 16-346 → 16-341; twin O/N | Removes Birth Restrictions gating, adds stat rollovers/Command Center links, replaces tourist-satisfaction section with Services. | `ipBuilding.generated.lua` for Dome; R1, select Dome; screen. | Law-gated/static stats → direct policy and linked stats. Base. Input/UI behavior requires runtime. No PERF. |
| R11565 | `sectionFactoryResearch.Init`; added (f); — → 16-39; twin -/N | Adds distributed-research Tech Point progress for factories. | `ipBuilding.generated.lua:100-103`, gated by class, exclusion, and `DistributedResearchNodes`; R2, research tech/select factory; screen. | No old section. Base definitions; unavailable contexts do not construct it. No tell/PERF. |
| R11567 | `sectionFoodProducerStoredResources.Init`; added (f); — → 19-39; twin -/N | Iterates `GetUIStoredResourcesList` into group-aware stored rows. | `ipBuilding.generated.lua:47,62`; R1/R2, select Farm/Pasture; screen/profile. | Storage extracted from crop/pasture sections. Base. Bounded by building resource list; no PERF concern. |
| R11568 | same file `new`; added (f); — → 13-17; twin -/N | Returns only for FarmBase/Pasture contexts. | Same consumer/reach; class. | Explicit context gate protects other buildings/nonowners. No tell/PERF. |
| R11569 | `sectionFoodService.Init`; added (f); — → 16-109; twin -/N | Adds Food storage, ingredient toggles, Norman-only Now Serving courses, and meals-served counters. | `ipBuilding.generated.lua:76`; R1 for base FoodBuilding, R2 for Norman meal menus; screen/profile. | New `FoodBuilding` UI; Now Serving is explicitly `IsDlcAvailable("norman")`-guarded. Base `FoodBuilding:Init` populates `serveable_ingredients` before IP use. No hard tell. **PERF observation:** each of three course updates independently calls `GetNowServingMenu`; comment explicitly requires recompute on every update, but one UI refresh can rebuild the same menu three times. |
| R11570 | same file `new`; added (f); — → 11-14; twin -/N | Rejects non-`FoodBuilding` contexts. | Same consumer; R1/R2, select food service; class. | Explicit class gate, safe for nonowners. No tell/PERF separate from R11569. |
| R11576 | `sectionMicroGHabitat.Init`; body (a); 16-187 → 16-154; twin O/N | Modernizes immigration/stat rollovers and removes Tourist Satisfaction subsection. | `ipBuilding.generated.lua:37`; R2, select Micro G Habitat; screen. | Old static stats → shared stat formatters. Object-gated nonowner. No tell/PERF. |
| R11583 | `sectionPasture.Init`; body (a); 16-114 → 16-80; twin O/N | Recipe-style breed production, layout changes, removes stored Food block now owned by R11567. | `ipBuilding.generated.lua:58`; R2, select Pasture; screen. | Monolithic pasture/storage → separated storage section. Object-gated. No tell/PERF. |
| R11587 | `sectionRecipeProductionBuilding.Init`; added (f); — → 16-106; twin -/N | Builds one recipe-slot selector per slot, calls `UIRecipeSlotUpdate`, adds Food Service encyclopedia shortcut and stored-output section. | `ipBuilding.generated.lua:51`; `Buildings/RecipeProductionBuilding.lua:1061` explicitly names this XDef as caller contract; R2, select recipe building; class/screen/profile. | No old class; new recipe-production UI. Base class, content-dependent. Loops fixed by `RecipeSlots`; no hard tell/PERF beyond bounded UI work. |
| R11590 | `sectionResearchProject.Init`; body (a); 16-46 → 16-39; twin O/N | Removes “open research” button and selected-project progress; displays Tech Point progress and research modifiers. | `ipBuilding.generated.lua:98`; R1/R2, select research building; screen. | Research queue → Tech Points. Base. No tell/PERF. |
| R11594 | `sectionResourceGroupStorage.Init`; added (f); — → 22-93; twin -/N | Adds expandable group storage, leaf rows, and single-expanded-section behavior. | `contextResourceAcceptToggles.generated.lua:29-43`; also queried by `Lua/Resources.lua:184` and tutorial `Lua/TutorialsNew.lua:606`; R1/R2, open storage acceptance UI; screen/profile. | Flat storage → group-aware storage. Base Resource registry. Loop bounded by group items; no hard tell/PERF. |
| R11597 | `sectionResourceProducer.Init`; body (a); 19-51 → 20-60; twin O/N | Adds stable section id/new icon, guarded Replicator progress, generic stored-amount/waste text, removes layout-time icon mutation. | `ipBuilding.generated.lua:88`; R1/R2, select producer/Replicator; screen. | Specialized text/icon mutation → context methods and class guard. `g_Classes.ReplicatorBase` protects absent class for nonowners. No tell/PERF. |
| R11606 | `sectionVegetationPlant.Init`; body (a); 16-141 → 16-154; twin O/N | Adds production text, shared percent formatting, fixes “decrese,” and replaces separate Food/Seeds lines with `GetHarvestText`. | `ipBuilding.generated.lua:54`; R2, select vegetation/open farm; screen. | Hard-coded OpenFarm/Seeds fields → polymorphic harvest text. Content-gated nonowner. Old spelling error is a resolved hard tell; no surviving tell/PERF. |
| R11610 | `sectionWaterGrid.OnContextUpdate`; body (a); 42-47 → 42-49; twin O/N | Shows maximum production when current production is lower. | Constructed by `ipBuilding.generated.lua:180`, pipe/leak IPs; R1, select water-grid object under reduced production; class/screen. | Current-only text → current plus max. Base. No tell/PERF. |
| R11612 | `sectionWorkshifts.Init`; body (a); 16-85 → 16-125; twin O/N | Adds optional section title and Heavy Workload control; limits old footer to Workshops. A later `OnLayoutComplete` aligns fixed shift rows. | `ipBuilding.generated.lua:144`; R1, select workplace/workshop and toggle workload; screen/class. | Workshift-only UI → law-aware workload section. Base; law state controls visibility. Three-row loops are bounded; no tell/PERF. |

## Exceptions, malformed spans, and drift

- Complete exact rows: all 84 keys listed above.
- Not reached: none of the 84 declared present spans. Runtime rendering,
  hit-testing, native behavior and actual timing were not reached because this
  batch was source-only.
- Hunk-only reads: 0.
- Malformed spans: 0.
- `SPAN-SUSPECT`: 0.
- `MULTI`: 0.
- One-line: exactly R05272 (`Value@bb968b`, old line 16). The source line is
  self-closing, was read literally as one line, and was not allowed to absorb
  the following body.
- Indented: exactly R05272 and R05273. They are distinct nested functions in
  the old FungalFarm condition and do not overlap.
- Whole-file removal: R11229, R11230, R11413 (`GONEFILE`). Their replacement
  capability was enumerated above; they were not treated as feature deletion.
- New files: 16 flagged rows. R11240 is the seventeenth added function but is
  inside an existing file, so it correctly lacks `NEWFILE`.
- Twin drift: 0 lifecycle mismatches across 61 pairs.
- Queue drift: the supplied expected 82 + 2 = 84 matches exactly. No missing,
  duplicate, foreign-owner, or extra row.
- Semantic drift caught during reading: (1) Water and Oxygen both calling
  `ShowWaterOverlay` initially looked asymmetric, but `Lua/SupplyGrid.lua:1018`
  explicitly says water and air share the life-support overlay; (2) removed
  `ResearchDlg` and combined life-support names are replacements, not deleted
  capabilities; (3) `Data/XDef` and generated classes are authoring/runtime
  twins, not duplicate runtime effects; (4) FungalFarm_Asteroid's removed
  template condition does not remove its later `UnlockBuilding` reference.

## Surviving source observations (not verdicts)

No surviving FIX_POLICY §4 hard-tell lead was found in this 84-row batch. The
new bodies' explicit comments either explain intended behavior (deprecated
passage buttons, lander price/cancellation, menu recomputation) or support a
replacement/correction already made by 1.1.0. Two bounded performance
observations remain suitable only for measurement:

1. R11506: Tech search translates/strips and fuzzy-searches every Tech preset
   for each query; falsify by profiling a long search interaction and counting
   `ForEachPreset` invocations.
2. R11569: the three visible Now Serving course rows each recompute the same
   menu during one context refresh; falsify by counting `GetNowServingMenu`
   calls per refresh and measuring with the largest authored meal registry.

Neither observation supplies measured player harm or a source-level hard tell.


