# Vanillahunt 03b — generated `Data/*` + caller audit

Read-only child report, 2026-09-10. This is evidence for the 03b parent, not a
defect verdict and not a filing decision. No repository, tagged TSV, archive,
game file, or running game was changed.

## Receipt and method

- Scope was derived mechanically from `INVENTORY.tagged.tsv` as `link == 03`
  plus `file like Data/*`: **184 rows, 184 distinct R keys, 35 files**. The six
  named `CALLERS.tagged.tsv` items are **6 rows, 6 distinct C keys**. Grand
  total: **190/190 fully read; missing 0; duplicate keys 0; not reached 0**.
- Every exact present span was read in both pinned trees:
  `O=C:/Dev/SMR-SrcArchive/1.0.7.396349/Src` and
  `N=C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`. Added rows were traced to the old
  behavior path; removed rows were traced to the new behavior path. Relevant
  enclosing presets, actual Lua consumers, and generated twins were read in
  both directions.
- Row shape: `added 81`, `body 50`, `body+sig 21`, `removed 32`; all 184 are
  `INDENTED`, 179 `MULTI`, 54 `NEWFILE`, 12 `ONE-LINE`, 3 `GONEFILE`, one
  `DECL-ONLY`, and **0 `SPAN-SUSPECT`**. Empty-old 81 and empty-new 32 exactly
  match added/removed. No malformed or hunk-only inventory row exists here.
  All six caller items are call-line/hunk items, but their complete caller and
  callee bodies were read.
- Classification used below: changed body/body+sig = class `(b)`; removed body
  = `(e)`; added body = `(f)`; unchanged caller across a changed signature =
  `(b-prime)` contract seam. Reach is `R1` ordinary play, `R2` shipped but
  configuration/event-dependent, or `R4` editor/debug/mod-author tooling.
- `SMELL/PERF` was applied to every body opened. Four source-tell clusters are
  preserved below. Outside them, **SMELL none; PERF none**: no new unbounded
  per-tick/per-object scan or multiplicative hot loop was established. This is
  source reading, not measured frame time or native/runtime behavior.

## Instrument drift and reconciliation

The principal drift is identity, not missing text. `MULTI` identifies repeated
nested anonymous members by file/name/ordinal. Insertions and reorderings can
therefore pair different logical preset members. The exact spans are real, but
179 rows must not automatically be described as a mutation of one logical
preset member. Concrete examples:

- `R04256` mechanically pairs old `FactionOpportunity.DismissFunc` with new
  `StarvingColonists.DismissFunc`; the logical new FactionOpportunity members
  are `R04257` and `R04283`.
- `R04164` mechanically pairs the old Earthsick-leaver handler with a new
  Building Codes handler; the logical Earthsick successor is `R04166`.
- `R04161` pairs old Underground Exploitation prerequisite with new Open Domes
  conflict. `R04311`–`R04318` similarly reflect a policy-list insertion shift.
- Many faction `eval` ordinals shifted after task-list insertions. Their exact
  predicates were read, but semantics were reconciled by enclosing task/preset,
  not ordinal alone.

Five `RENAME?` hints were treated only as search hints. The one declaration-only
row (`R04152`) is a genuine one-line value body. The 12 one-line spans were read
in their enclosing preset. The three `GONEFILE` bodies were found in their new
hand-written successors. There are no unresolved malformed, hunk-only,
span-suspect, or one-line items.

## Old-only/fixed source tells (non-current findings; no verdict)

Each cluster below describes behavior in the 1.0.7 body that the shipped 1.1.0
body already changes. They are retained as source evidence only: **none is a
current 1.1.0 defect lead, and no broader search is requested by this report**.

1. **Rival milestone rewards — `R04157`, `R04159`, R2 when either Milestones
   law is active.** Old handlers rewarded every `MilestoneCompleted`. Old
   `Lua/RivalColonies.lua:714-723` writes a rival into `MilestoneEnactors[id]`
   and emits the same message. New handlers require
   `MilestoneEnactors[id] == MainCity`. Actual old×new seam: a shared global
   event carried no enactor check → the data handler now filters ownership.
   Hard tell: producer/consumer self-contradiction plus the paired 1.1.0 repair.
   Falsifier: prove rival completion never reaches that old message in runtime,
   or that old milestone-law reactions were not registered. Non-owner impact:
   base law/rival code, no DLC dependency. Action: record as old-only/fixed; no
   current filing or broader search.

2. **Funding notification amount — `R04156`, `R04159`, `R04183`, R2 while the
   corresponding law is active.** Old handlers discard `ChangeFunding`'s
   returned modified amount and notify the requested base amount unconditionally.
   Both old and new `Lua/Funding.lua:44-70` return the actual modified amount
   and return nil when zero; new handlers display the return only when non-nil.
   Hard tell: discarded return/self-contradiction, repeated in three sibling
   repairs. Falsifier: establish all reachable funding modifiers are always
   exactly 100% and a zero return impossible. Non-owner impact: base laws and
   funding. Action: record as old-only/fixed; no current filing or broader search.

3. **Childcare chance boundary — `R04205`, R2 while the Childcare law is
   active.** `colonist:Random(100) <= chance` became `< chance`. With the
   established 0..99 convention, old behavior is `chance + 1` percent and even
   chance 0 succeeds for draw 0. New sibling handlers `R04206`–`R04210` and
   `R04212`–`R04214` use `>= chance` as the reject boundary. Hard tell: sibling
   arithmetic contradiction. Falsifier: prove this Random overload returns
   1..100, or the configured chance is outside the affected interval. Base law;
   no DLC dependency. Action: record as old-only/fixed; no current filing or
   broader search.

4. **Skip Founder Stage reaction lookup — `R04168`, `R04169`, R2 while the law
   is active and founder approval remains pending.** Old code indexes
   `ActiveLaws[self]`; law activation stores `ActiveLaws[self.id]`
   (`O Lua/ClassDefs/ClassDef-Factions.generated.lua:1775-1791`,
   `N Lua/Factions/LawDef.lua:45-61`). `CommonLua/Reactions.lua:130-135,469-477`
   registers the preset instance beside the handler, so handler `self` is the
   preset object, not its id. New code uses `self.id`; birth additionally admits
   only producer tag `event == "born"` while arrival stays unconditional.
   Hard tell: key-type self-contradiction and paired repair. Falsifier: prove
   the native message dispatcher substitutes the string id despite the stored
   instance, or that `ActiveLaws` is also object-keyed at runtime. Base law and
   message emitters; no DLC dependency. Action: record as old-only/fixed; no
   current filing or broader search.

## Six caller contracts

- **C03052** — `Data/ClassDef-Effects.lua:1133 -> :1102`,
  `ResearchTechsCombo(self,{value="", text="-random-"})`; class `(b-prime)`.
  Old callee `Lua/_GameUtils.lua:213-224` accepts only `object`, so Lua silently
  ignores the second argument and creates its own blank sentinel. New callee
  `:235-250` accepts `...`, captures this table, and uses the supplied sentinel.
  R4 property-editor reach. The tagged explanation that passed arguments
  “arrive nil/keep old behavior” is false. Falsifier: editor never instantiates
  this property or varargs are stripped by the Lua runtime. Generated twin is
  C03057. Seam: changed utility contract activates an unchanged Data argument.
  Base tooling; non-owner safe as far as named dependencies go. SMELL/PERF none;
  action: correct parent interpretation, no defect inference.
- **C03053** — `Data/ClassDef-Effects.lua:3833 -> :3817`, same contract but
  sentinel `{value="random", text="-random tech-"}`. R4; exact old/new effect
  is ignored argument → active first combo entry. Falsifier/seam/impact and
  SMELL/PERF as C03052. Generated twin C03058.
- **C03057** — `Lua/ClassDefs/ClassDef-Effects.generated.lua:662 -> :638`, exact
  generated twin of C03052. `(b-prime)`, R4, same contract and falsifier. The
  Data/generated texts agree both versions; no twin drift.
- **C03058** — generated `:2438 -> :2419`, exact twin of C03053. `(b-prime)`,
  R4, same contract/falsifier; no twin drift.
- **C03743** — `Data/ClassDef-Effects.lua:4323 -> :4364` calls
  `building:Setexceptional_circumstances(self.Enabled)`. Old callee
  `Lua/Buildings/BaseBuilding.lua:183-188` has `(disabled)`; new `:470-480` has
  `(disabled, reason)`. The same preset's new enabling path passes a reason;
  this restore/disable path intentionally omits it, and new callee clears
  `exceptional_circumstances_reason` when disabling outside maintenance.
  `(b-prime)`, R2 effect-preset reach. Falsifier: an authored restore requires
  retaining a reason or the call is actually an enabling call. Base class;
  non-owner. SMELL/PERF none; action none from this batch.
- **C03753** — generated `Lua/ClassDefs/ClassDef-Effects.generated.lua:2762 ->
  :2779`, exact twin of C03743; same contract/reach/falsifier. No twin drift.

## Inventory contracts and per-key ledger

Every key below inherits its file's class from its tagged kind and its exact
span from the ledger. “No action” means no additional source tell beyond the
four clusters above; it is not a behavior-clearance verdict.

### Building, challenge, cheats, generated definitions, events

- `R03700 R03701` — old FungalFarm asteroid building condition reads
  `ActiveLaws.Policy_SpaceFarming`; new removes the `Condition` value/eval.
  Class `(e)`, R2 (asteroid building). New building still exists, with unlock
  routed through live Tech/policy data; old and new generated building twins
  match Data. Falsifier: find another retained old condition consumer. Seam:
  law-gated building → registry unlock route. Base/non-owner route does not
  require opening DLC internals; FungalFarm/FungalFarmBase names were not
  conflated. SMELL/PERF none; no action.
- `R03711` — removes EuropeResearchedBreakthroughs' blocking `WaitMsg` loop;
  `(e)`, R2 challenge. New challenge uses common counter/TickProgress plumbing.
  Falsifier: a retained preset still invokes the removed Run. Base/non-owner;
  no smell/perf action.
- `R03720` — EuropeResearchedTechs TickProgress changes direct
  `UIColony.tech_status` scan to `ForEachPreset("Tech")` plus
  `IsTechResearched`, excluding initiatives; `(b)`, R2. Consumer
  `Lua/Challenges.lua:27-47`. Falsifier: initiatives are intended to count or
  Tech iteration excludes playable technologies. Registry seam, base/non-owner;
  no smell/perf action.
- `R03794 R03801 R03806 R03807` — added cheats enact all laws, research all,
  reveal breakthroughs, and unlock all tech. `(f)`, R4/debug. Falsifier:
  shipped player UI exposes the cheats in ordinary play. Legislature/research
  registry seam; base/non-owner; no smell/perf action.
- `R03836 R03840 R03843` — removed generated editor-view functions from gone
  `Data/ClassDef-Conditions.lua`; exact logical successors are in new
  `Lua/Factions/LawDef.lua:757-805` and `Lua/ScriptBlocks.lua:489-526`.
  `(e)`, R4 editor. Falsifier: generated definitions are still loaded in new.
  Data→hand class migration; base/non-owner; no smell/perf action.
- `R03850` — added `has_allowed_version` helper inside resource-recipe editor
  validation; faithfully emitted in
  `Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1615-1643`. `(f)`, R4
  editor/mod-author. Falsifier: invoked during recipe execution, rather than
  GetError. Save-version validation seam; base/non-owner; no smell/perf action.
- `R03853 R03856` — added ClosedLoopDome event/follow-up evals validate the
  object, apply a -100% water modifier, schedule the follow-up, then restore it
  after a guarded delay. `(f)`, R2 event. `StartEvent` consumer is
  `CommonLua/Libs/TriggersAndEvents/ScriptEvents.lua:21-38`. Falsifier: closing
  or replacing event context prevents the follow-up's object from surviving;
  this requires runtime observation. Base/non-owner. No hard tell; no action.

### Faction task predicates

`R03875 R03876 R03883 R03884 R03886 R03887 R03888 R03892 R03925 R03926
R03937 R03941 R03943 R03944 R03951 R03996 R03997 R03998 R03999 R04000
R04001 R04002 R04003 R04025 R04026 R04031 R04033 R04034 R04035 R04036
R04039 R04040 R04043 R04045 R04046 R04047 R04048 R04049 R04052 R04053
R04079 R04080 R04111 R04112 R04115 R04116 R04117 R04118 R04121 R04122
R04126` were all read in their complete enclosing faction tasks. They are
classes `(b)/(e)/(f)` as tagged, R2 when the corresponding faction/task is
active. The authored rewrite replaces interest-based
`AreServiceBuildingsUnavailable` predicates with named
`AreServiceBuildingsAvailable/Insufficient` checks, splits Farm/Hydroponic/
FungalFarm/FarmInsect tasks, and adds food, tech, and law tasks. LastTransmission
`R04003` adds status-table guards and accepts Malnourished as well as Starving.
Consumers are faction task generation/success in
`Lua/Factions/FactionDef.lua:1132-1150,1222-1238` and legislature task paths
`Lua/Factions/Legislature.lua:1462,1485,1504`.

Old×new seam: task-list insertion/reordering plus a service-availability API
rewrite. Falsifier per row: identify its enclosing old/new logical task and show
the predicate contradicts that task's target or a valid label can be nil.
Non-owner: all base definitions load. References to InsectFarming/FarmInsect
are guarded: absent tech does not compare as researched, so the label branch is
not reached. No DLC interior was used as clearance. SMELL/PERF none across this
set; no action. Important: ordinal pairs are mechanical, not proof of same
logical member.

### Flight and game rules

- `R04127 R04128 R04129 R04130 R04132` — automatic/manual route resource lists
  are normalized, MysteryResource is conditional, Oligarch fuel is handled,
  Norman Sugar/Spices references are guarded, and probe cargo uses Cargo
  presets. `(b)`, R2 while that flight policy is selected. Consumer:
  `UniversalRocket:GetAllowedResources` at `Lua/UniversalRocket.lua:737-746`.
  Falsifier: a reachable policy returns a resource absent for non-owners or
  changes list shape expected by cargo UI. Base consumer; DLC names are guarded,
  no DLC function opened. SMELL/PERF none; no action.
- `R04146` — wait-in-orbit policy handler follows the revised route-resource
  contract; `(b)`, R2. Command consumer near `Lua/UniversalRocket.lua:304`.
  Same falsifier/seam/non-owner boundary; no smell/perf action.
- `R04152 R04154` — NoPolitics rule reads sponsor/challenge from `Game` instead
  of `g_CurrentMissionParams`. `(b)`, R2 when rule selected. Falsifier: Game is
  unset when these values are evaluated. Mission-parameter persistence seam;
  base/non-owner; no smell/perf action.

### Laws and policies

- `R04156 R04157 R04159` — Exploration/Milestone law handlers add actual-return
  notification handling and/or `MilestoneEnactors[id] == MainCity`; `(b)`, R2.
  See lead clusters 1–2 for delta, reach, falsifiers, seam, impact, tells/action.
- `R04161` — mechanical ordinal pair only: old Underground Exploitation checks
  NoUndergroundAndAsteroids; new Open Domes conflict checks active Open Domes.
  `(b+sig)`, R2. Falsifier: demonstrate these are the same logical condition.
  Policy prerequisite/conflict seam; base/non-owner; no smell/perf action.
- `R04164 R04165 R04166` — list insertion pairs old Earthsick funding with new
  BuildingCodesLax; new Strict/old Earthsick logical members were reconciled.
  Earthsick adds a `status_effects` guard; maintenance handlers skip prefabs,
  require an active law and `RequiresMaintenance`, then set a modifier. Classes
  `(b+sig)/(f)`, R2. Falsifier: enclosing IDs do not match the reconciliation or
  a supported building violates those guards. Law/event seam; base/non-owner;
  no smell/perf action.
- `R04168 R04169` — SkipFounder reactions change object-key lookup to id-key;
  birth reaction also requires event tag `born`. `(b)`, R2. See lead cluster 4.
- `R04173` — founder-stage prerequisite reads `Game.challenge_id` rather than
  mission params; `(b)`, R2. Falsifier: evaluated before Game exists. Mission
  persistence seam; base/non-owner; no additional smell/perf action.
- `R04174 R04175 R04176 R04177` — election handlers use handle-keyed Dhondt and
  faction-specific `DhondtFactions`; `(b)`, R2. Consumer is
  `Lua/Factions/Legislature.lua:837-900`. Falsifier: result consumers require
  preset objects rather than handles or faction vote maps are generic maps.
  Legislature allocation seam; base/non-owner. No new tell here; the known hand
  consumer issue is owned elsewhere.
- `R04180 R04181 R04182` — Education adds target selection, validates target
  faction/removes obsolete ministry scaling in one handler, and makes research
  notifications selectable with the colonist object. `(f)/(b)`, R2. Falsifier:
  target is deliberately allowed stale, or notification consumer rejects obj.
  Law target/notification seam; base/non-owner; no smell/perf action.
- `R04183` — Terraforming funding uses actual `ChangeFunding` return/guard;
  `(b)`, R2. See lead cluster 2.
- `R04201` — Childcare adds majority-faction ChooseTarget; `(f)`, R2.
  Falsifier: law should not target a faction. Base/non-owner; no extra tell.
- `R04205` — chance comparator repair; `(b)`, R2. See lead cluster 3.
- `R04206 R04207 R04208 R04209 R04210 R04212 R04213 R04214` — added societal
  value handlers: require active law and Martianborn, use the matching chance
  boundary, filter compatible traits, then add one. `(f)`, R2. Falsifier:
  message fires for non-colonists or `traits` may be nil on a valid recipient.
  Law/trait seam; base/non-owner. These siblings supply R04205's tell; no PERF.
- `R04211` — polarization switches global `AsyncRand()` to colonist-local
  `colonist:Random()`; `(b)`, R2. Falsifier: deterministic colonist RNG is not
  required by save/replay semantics. RNG seam; base/non-owner; no hard tell.
- `R04305 R04306 R04308 R04309 R04310 R04311 R04312 R04313 R04314 R04315
  R04316 R04318` — removed one-line Values and shifted/added policy condition
  evals for QualityRest, NightShiftCompensations, Apportionment, AssemblyType,
  Dictatorship and post-independence. Classes `(e)/(b)/(f)`, R2. Falsifier:
  reconcile by policy id and show a retained conflict/prerequisite disappeared.
  Old×new seam is authored policy-list restructuring, not same-ordinal mutation.
  Base/non-owner; SMELL/PERF none; no action.

### Notifications, sponsor goals, stats and status effects

- `R04243` adds food-service items to StarvingColonists; `R04256` is the false
  ordinal pair noted above; `R04257/R04283` are the logical new
  FactionOpportunity dismiss/press handlers, clearing or selecting its task.
  `(f)/(b)`, R2 notifications. Falsifier: NotificationPreset member dispatch
  associates a different enclosing id. Base/non-owner. No new tell; notification
  cleanup hand-consumer issue is owned elsewhere. No PERF.
- `R04324 R04333 R04378` — old sponsor goal-specific blocking Completed loops
  for tech/laws are removed and EnactLaws gains common EvalProgress. `(e)/(f)`,
  R2 when selected as a sponsor goal. Consumers are SetupMissionGoals and Colony
  hourly goal evaluation. Falsifier: common goal evaluator does not initialize
  or call this member. Base/non-owner; no smell/perf action.
- `R04509 R04510 R04515 R04518 R04530 R04532` — new StatsImpact definitions
  for BiomeEngineering, FounderPrivilege, NightShift and Food expose Condition
  and ApplyStats. `(f)`, R1/R2 depending tech/law. Consumer
  `Lua/Stats.lua:153-156,879,888` and `Lua/Units/Colonist.lua:2536,2543` gates
  ApplyStats through Condition. Falsifier: a call bypasses Condition or runs on
  an object without the required fields. Base/non-owner; no smell/perf action.
- `R04535 R04536 R04540 R04541 R04542 R04546` — new Hungry/Malnourished/
  Starving OnStart/OnStop functions remove Stuffed/update dome starvation
  notification; Malnourished applies its performance penalty. `(f)`, R1 status
  lifecycle; consumer `Lua/StatusEffectPreset.lua:134-145`. Falsifier: lifecycle
  invokes these without a colonist/dome contract. Base/non-owner; no smell/PERF.

### Tech/TechPreset/Trait migration

- `R04569` adds HumanAlteration law reaction that unlocks its initiative when
  the law is active. `(f)`, R2. Falsifier: live Tech instances do not register
  msg reactions. Base/non-owner; no smell/perf action.
- `R04571 R04572 R04573 R04574 R04575 R04576 R04577 R04578 R04579 R04592
  R04593` add Wildfire Cure variant OnApplyEffect unlocks; `R04595 R04596
  R04597 R04598 R04599 R04603 R04604 R04605 R04606 R04607 R04608` add matching
  OnInitEffect locks. `(f)`, R2 Wildfire progression. Falsifier: these Cure ids
  are not live Tech presets or init/apply order can leave a researched variant
  locked. Base/non-owner; no smell/perf action.
- `R04581/R04594` GiantCrops, `R04584/R04600` MartianVegetation,
  `R04588/R04601` UtilityCrops, and `R04589/R04602` GeneAdaptation add paired
  apply/init unlock-lock behavior. `(f)`, R1/R2 research. Their removed legacy
  TechPreset counterparts are respectively `R04666/R04673`,
  `R04661/R04677`, `R04667/R04674`, and `R04669/R04675`. Falsifier: both
  registries execute effects, causing double application, or neither live Tech
  consumes them. Registry seam: one-time migration, not duplication.
- `R04611` adds NanoRefinement OnResearched deposit-exploiter refresh; old
  `R04683` removes the legacy copy. `(f)/(e)`, R1 research. Falsifier: the new
  Tech OnResearched is not called or old TechPreset remains live. Base/non-owner;
  no smell/perf action.
- `R04662` removes old PlanetarySurvey apply behavior; logical new Tech behavior
  is at `N Data/Tech.lua:8314-8324` and uses parent ResolveValue/MainMap.
  `R04671/R04676` remove Wildfire Cure legacy base init/apply members.
  `R04693` removes DustRepulsion legacy OnResearched; new Tech at
  `N Data/Tech.lua:9295-9317` uses `self:ResolveValue`. `R04698` removes obsolete
  AdvancedMicroG comfort-food hint; `N Lua/Hints.lua:946-948` has the explicit
  cleanup fixup. `(e)`, R1/R2. Falsifier: legacy TechPreset effects remain in
  the live research path. Base/non-owner; no smell/perf action.
- Live-registry evidence: new `Lua/TechTree.lua:510-512` initializes every
  `Tech`; `:1200-1239` applies its Effects and calls preset OnResearched.
  `CommonLua/Classes/GameEffect.lua:29-39` supplies EffectsInit/EffectsApply.
  The old TechPreset is a sidecar/legacy registry; migrated functions are not a
  second runtime effect. This independently agrees with the 03c DeepScanning
  handoff: live `N Data/Tech.lua:3934-3961` owns both DeepScan effects, while
  `N Data/TechPreset.lua:847-852` is an inert id/group stub. Source connects the
  route but does not close FR-2.
- `R04769` removes Martianborn trait's per-colonist modifier application;
  MartianbornIngenuity is now a label modifier at `N Data/Tech.lua:1379-1406`,
  with explicit migration fixup `N Lua/_fixup.lua:2682-2689`. `(e)`, R1.
  Falsifier: old saves miss the fixup or label modifier excludes living
  Martianborn colonists. Base/non-owner. Explicit migration intent; no smell/PERF.

### Tutorial

- `R04893 R04957 R05046 R05047` are added members in new Step08_Food (despite
  shifted ordinals): wait for a tutorial popup, then test HydroponicFarm,
  ShopsFood_Small, or StorageFood. `(f)`, R2 tutorial only. Falsifier: enclosing
  Step id or condition dispatch differs from the read definition. Tutorial
  step/UI seam; base/non-owner. No smell/perf action.

## Exact span ledger (184 inventory rows)

The contract descriptions above apply to every listed key. Blank side means the
body is genuinely absent on that side, not unread.

### Data/BuildingTemplate/FungalFarm_Asteroid.lua (2)
- R03700 `Value@1a66e7` [removed]; O14-14; N—; flags INDENTED,ONE-LINE
- R03701 `eval@1a66e7` [removed]; O10-12; N—; flags INDENTED
### Data/Challenge.lua (2)
- R03711 `Run@71e825#12` [removed]; O795-806; N—; flags INDENTED,MULTI
- R03720 `TickProgress@71e825#6` [body]; O327-336; N172-181; flags INDENTED,MULTI
### Data/CheatDef.lua (4)
- R03794 `run@337c67#62` [added]; O—; N748-764; flags INDENTED,MULTI,NEWFILE
- R03801 `run@337c67#69` [added]; O—; N854-864; flags INDENTED,MULTI,NEWFILE
- R03806 `run@337c67#73` [added]; O—; N902-910; flags INDENTED,MULTI,NEWFILE
- R03807 `run@337c67#74` [added]; O—; N919-929; flags INDENTED,MULTI,NEWFILE
### Data/ClassDef-Conditions.lua (3)
- R03836 `DefGetEditorView@545d4c#10` [removed]; O3310-3312; N—; flags GONEFILE,INDENTED,MULTI
- R03840 `DefGetEditorView@545d4c#5` [removed]; O3183-3185; N—; flags GONEFILE,INDENTED,MULTI
- R03843 `DefGetEditorView@545d4c#8` [removed]; O3244-3246; N—; flags GONEFILE,INDENTED,MULTI
### Data/ClassDef-PresetDefs.lua (1)
- R03850 `has_allowed_version@2fd553` [added]; O—; N2996-3008; flags INDENTED
### Data/Event/ClosedLoopDome.lua (1)
- R03853 `eval@67b385#2` [added]; O—; N38-44; flags INDENTED,MULTI,NEWFILE
### Data/Event/ClosedLoopDome_FollowUp.lua (1)
- R03856 `eval@67b385#2` [added]; O—; N19-22; flags INDENTED,MULTI,NEWFILE
### Data/FactionDef/China.lua (5)
- R03875 `eval@1e46ea#10` [body+sig]; O229-231; N229-231
- R03876 `eval@1e46ea#11` [added]; O—; N247-249
- R03883 `eval@1e46ea#6` [body+sig]; O151-153; N153-155
- R03884 `eval@1e46ea#7` [body]; O161-163; N175-177
- R03886 `eval@1e46ea#9` [body+sig]; O219-221; N206-208
### Data/FactionDef/ChurchOfTheNewArk.lua (3)
- R03887 `eval@1e46ea#10` [body+sig]; O232-234; N253-255
- R03888 `eval@1e46ea#11` [body+sig]; O261-263; N275-277
- R03892 `eval@1e46ea#15` [body]; O339-341; N331-333
### Data/FactionDef/GreenMarsCoalition.lua (2)
- R03925 `eval@1e46ea#22` [body+sig]; O462-464; N441-443
- R03926 `eval@1e46ea#23` [body+sig]; O488-490; N459-461
### Data/FactionDef/GreenNOW.lua (1)
- R03937 `eval@1e46ea#20` [added]; O—; N420-422
### Data/FactionDef/HeritageTrust.lua (4)
- R03941 `eval@1e46ea#1` [body]; O49-51; N51-53
- R03943 `eval@1e46ea#11` [body+sig]; O214-216; N228-230
- R03944 `eval@1e46ea#12` [body]; O229-231; N238-240
- R03951 `eval@1e46ea#2` [body+sig]; O68-70; N69-71
### Data/FactionDef/LastTransmission.lua (8)
- R03996 `eval@1e46ea#26` [added]; O—; N463-465
- R03997 `eval@1e46ea#28` [added]; O—; N503-505
- R03998 `eval@1e46ea#29` [added]; O—; N528-530
- R03999 `eval@1e46ea#30` [added]; O—; N551-553
- R04000 `eval@1e46ea#31` [added]; O—; N569-571
- R04001 `eval@1e46ea#32` [added]; O—; N586-588
- R04002 `eval@1e46ea#34` [added]; O—; N621-623
- R04003 `eval@1e46ea#4` [body]; O85-87; N87-89
### Data/FactionDef/NewSol.lua (17)
- R04025 `eval@1e46ea#10` [body]; O227-229; N231-233
- R04026 `eval@1e46ea#11` [body]; O246-248; N249-251
- R04031 `eval@1e46ea#17` [body]; O332-334; N359-361
- R04033 `eval@1e46ea#20` [body+sig]; O361-363; N412-414
- R04034 `eval@1e46ea#21` [body]; O378-380; N422-424
- R04035 `eval@1e46ea#22` [body+sig]; O413-415; N437-439
- R04036 `eval@1e46ea#23` [body]; O428-430; N447-449
- R04039 `eval@1e46ea#26` [body]; O490-492; N502-504
- R04040 `eval@1e46ea#27` [body]; O501-503; N512-514
- R04043 `eval@1e46ea#3` [body]; O80-82; N84-86
- R04045 `eval@1e46ea#31` [removed]; O551-553; N—
- R04046 `eval@1e46ea#32` [removed]; O565-567; N—
- R04047 `eval@1e46ea#33` [removed]; O576-578; N—
- R04048 `eval@1e46ea#4` [body]; O122-124; N102-104
- R04049 `eval@1e46ea#5` [body+sig]; O141-143; N120-122
- R04052 `eval@1e46ea#8` [body]; O189-191; N193-195
- R04053 `eval@1e46ea#9` [body]; O208-210; N211-213
### Data/FactionDef/ProsperityForMars.lua (2)
- R04079 `eval@1e46ea#17` [body]; O364-366; N367-369
- R04080 `eval@1e46ea#18` [body]; O380-382; N382-384
### Data/FactionDef/UnitedColonistFront.lua (1)
- R04111 `eval@1e46ea#8` [removed]; O157-159; N—
### Data/FactionDef/WorkersParty.lua (8)
- R04112 `eval@1e46ea#11` [body]; O259-261; N261-263
- R04115 `eval@1e46ea#15` [body+sig]; O316-318; N349-351
- R04116 `eval@1e46ea#16` [body+sig]; O354-356; N359-361
- R04117 `eval@1e46ea#17` [body+sig]; O365-367; N380-382
- R04118 `eval@1e46ea#18` [body+sig]; O385-387; N390-392
- R04121 `eval@1e46ea#21` [body+sig]; O427-429; N455-457
- R04122 `eval@1e46ea#22` [body+sig]; O447-449; N465-467
- R04126 `eval@1e46ea#8` [body]; O150-152; N151-153
### Data/FlightPolicyDef.lua (6)
- R04127 `GetAutoModeAllowedResources@3bfead#1` [body]; O133-142; N145-166
- R04128 `GetAutoModeAllowedResources@3bfead#2` [body]; O232-241; N271-296
- R04129 `GetAutoModeAllowedResources@3bfead#3` [body]; O390-397; N463-480
- R04130 `GetManualModeAllowedResources@3bfead#1` [body]; O143-152; N167-189
- R04132 `GetManualModeAllowedResources@3bfead#3` [body]; O398-407; N481-506
- R04146 `OnCmdWaitInOrbitBegin@3bfead#2` [body]; O482-491; N582-592
### Data/GameRuleDef.lua (2)
- R04152 `Value@153a91#1` [body]; O16-16; N16-16; flags DECL-ONLY,ONE-LINE
- R04154 `eval@153a91` [body]; O6-13; N6-13
### Data/LawDef/LawDef-Earth.lua (3)
- R04156 `Handler@5f2abf#2` [body]; O790-800; N821-833
- R04157 `Handler@5f2abf#4` [body]; O1060-1068; N1110-1118
- R04159 `Handler@5f2abf#6` [body]; O1214-1224; N1280-1292
### Data/LawDef/LawDef-Economy.lua (1)
- R04161 `eval@5f2abf` [body+sig]; O1092-1094; N287-289
### Data/LawDef/LawDef-Efficiency.lua (3)
- R04164 `Handler@5f2abf#1` [body+sig]; O637-641; N699-704
- R04165 `Handler@5f2abf#2` [added]; O—; N907-912
- R04166 `Handler@5f2abf#3` [added]; O—; N1125-1129
### Data/LawDef/LawDef-Founder Stage.lua (3)
- R04168 `Handler@5f2abf#2` [body+sig]; O190-195; N210-215
- R04169 `Handler@5f2abf#3` [body]; O199-204; N219-224
- R04173 `eval@5f2abf#2` [body]; O170-173; N190-193
### Data/LawDef/LawDef-Governance.lua (4)
- R04174 `Handler@5f2abf#1` [body]; O77-99; N81-103
- R04175 `Handler@5f2abf#2` [body]; O210-231; N206-227
- R04176 `Handler@5f2abf#3` [body]; O316-326; N316-326
- R04177 `Handler@5f2abf#4` [body]; O427-431; N421-425
### Data/LawDef/LawDef-Research.lua (4)
- R04180 `ChooseTarget@5f2abf` [added]; O—; N519-521
- R04181 `Handler@5f2abf#1` [body]; O312-326; N589-595
- R04182 `Handler@5f2abf#2` [body]; O405-420; N664-679
- R04183 `Handler@5f2abf#5` [body]; O1906-1922; N2326-2344
### Data/LawDef/LawDef-Welfare.lua (11)
- R04201 `ChooseTarget@5f2abf#1` [added]; O—; N107-109
- R04205 `Handler@5f2abf#1` [body]; O80-89; N91-100
- R04206 `Handler@5f2abf#10` [added]; O—; N2966-2974
- R04207 `Handler@5f2abf#11` [added]; O—; N3065-3073
- R04208 `Handler@5f2abf#12` [added]; O—; N3159-3167
- R04209 `Handler@5f2abf#13` [added]; O—; N3249-3257
- R04210 `Handler@5f2abf#14` [added]; O—; N3347-3355
- R04211 `Handler@5f2abf#2` [body]; O171-180; N193-202
- R04212 `Handler@5f2abf#7` [added]; O—; N2681-2689
- R04213 `Handler@5f2abf#8` [added]; O—; N2775-2783
- R04214 `Handler@5f2abf#9` [added]; O—; N2873-2881
### Data/NotificationPreset.lua (4)
- R04243 `AddItems@85b2b4#19` [added]; O—; N1388-1390
- R04256 `DismissFunc@85b2b4#1` [body]; O1214-1216; N1391-1393
- R04257 `DismissFunc@85b2b4#2` [added]; O—; N1927-1930
- R04283 `PressFunc@85b2b4#9` [added]; O—; N1933-1939
### Data/PolicyDef.lua (12)
- R04305 `Value@b7125f#1` [removed]; O404-404; N—; ONE-LINE
- R04306 `Value@b7125f#2` [removed]; O416-416; N—; ONE-LINE
- R04308 `Value@b7125f#4` [removed]; O496-496; N—; ONE-LINE
- R04309 `Value@b7125f#5` [removed]; O899-899; N—; ONE-LINE
- R04310 `Value@b7125f#6` [removed]; O964-964; N—; ONE-LINE
- R04311 `eval@b7125f#10` [body]; O895-897; N782-784
- R04312 `eval@b7125f#12` [body]; O960-962; N888-890
- R04313 `eval@b7125f#15` [added]; O—; N950-952
- R04314 `eval@b7125f#3` [body]; O400-402; N229-231
- R04315 `eval@b7125f#4` [body]; O412-414; N383-385
- R04316 `eval@b7125f#5` [body]; O467-469; N392-394
- R04318 `eval@b7125f#9` [body]; O559-561; N476-478
### Data/SponsorGoals.lua (3)
- R04324 `Completed@67f446#12` [removed]; O230-247; N—
- R04333 `Completed@67f446#20` [removed]; O406-420; N—
- R04378 `EvalProgress@67f446#18` [added]; O—; N483-489
### Data/StatsImpact.lua (6)
- R04509 `ApplyStats@8429e4#2` [added]; O—; N72-74
- R04510 `ApplyStats@8429e4#3` [added]; O—; N82-84
- R04515 `Condition@32ad74#3` [added]; O—; N172-172; ONE-LINE
- R04518 `Condition@8429e4#10` [added]; O—; N85-85; ONE-LINE
- R04530 `Condition@8429e4#7` [added]; O—; N53-53; ONE-LINE
- R04532 `Condition@8429e4#9` [added]; O—; N75-75; ONE-LINE
### Data/StatusEffectPreset.lua (6)
- R04535 `OnStart@5dfae0#1` [added]; O—; N87-91
- R04536 `OnStart@5dfae0#2` [added]; O—; N118-121
- R04540 `OnStart@5dfae0#6` [added]; O—; N268-271
- R04541 `OnStop@5dfae0#1` [added]; O—; N92-95
- R04542 `OnStop@5dfae0#2` [added]; O—; N122-124
- R04546 `OnStop@5dfae0#6` [added]; O—; N272-274
### Data/Tech.lua (32)
- R04569 `Handler@347971#7` [added]; O—; N8126-8130
- R04571 `OnApplyEffect@347971#10` [added]; O—; N6865-6867
- R04572 `OnApplyEffect@347971#11` [added]; O—; N6893-6895
- R04573 `OnApplyEffect@347971#12` [added]; O—; N6921-6923
- R04574 `OnApplyEffect@347971#13` [added]; O—; N6949-6951
- R04575 `OnApplyEffect@347971#14` [added]; O—; N6977-6979
- R04576 `OnApplyEffect@347971#15` [added]; O—; N7005-7007
- R04577 `OnApplyEffect@347971#16` [added]; O—; N7033-7035
- R04578 `OnApplyEffect@347971#17` [added]; O—; N7061-7063
- R04579 `OnApplyEffect@347971#18` [added]; O—; N7089-7091
- R04581 `OnApplyEffect@347971#2` [added]; O—; N1002-1012
- R04584 `OnApplyEffect@347971#22` [added]; O—; N9980-9985
- R04588 `OnApplyEffect@347971#4` [added]; O—; N2378-2384
- R04589 `OnApplyEffect@347971#5` [added]; O—; N2420-2432
- R04592 `OnApplyEffect@347971#8` [added]; O—; N6807-6809
- R04593 `OnApplyEffect@347971#9` [added]; O—; N6837-6839
- R04594 `OnInitEffect@347971#1` [added]; O—; N1013-1023
- R04595 `OnInitEffect@347971#10` [added]; O—; N6980-6982
- R04596 `OnInitEffect@347971#11` [added]; O—; N7008-7010
- R04597 `OnInitEffect@347971#12` [added]; O—; N7036-7038
- R04598 `OnInitEffect@347971#13` [added]; O—; N7064-7066
- R04599 `OnInitEffect@347971#14` [added]; O—; N7092-7094
- R04600 `OnInitEffect@347971#15` [added]; O—; N9986-9991
- R04601 `OnInitEffect@347971#2` [added]; O—; N2385-2391
- R04602 `OnInitEffect@347971#3` [added]; O—; N2433-2445
- R04603 `OnInitEffect@347971#4` [added]; O—; N6810-6812
- R04604 `OnInitEffect@347971#5` [added]; O—; N6840-6842
- R04605 `OnInitEffect@347971#6` [added]; O—; N6868-6870
- R04606 `OnInitEffect@347971#7` [added]; O—; N6896-6898
- R04607 `OnInitEffect@347971#8` [added]; O—; N6924-6926
- R04608 `OnInitEffect@347971#9` [added]; O—; N6952-6954
- R04611 `OnResearched@347971#11` [added]; O—; N1462-1473
### Data/TechPreset.lua (14)
- R04661 `OnApplyEffect@b017ab#12` [removed]; O4442-4445; N—
- R04662 `OnApplyEffect@b017ab#13` [removed]; O4477-4487; N—
- R04666 `OnApplyEffect@b017ab#3` [removed]; O656-663; N—
- R04667 `OnApplyEffect@b017ab#4` [removed]; O1841-1844; N—
- R04669 `OnApplyEffect@b017ab#6` [removed]; O1935-1944; N—
- R04671 `OnApplyEffect@b017ab#8` [removed]; O2687-2689; N—
- R04673 `OnInitEffect@b017ab#1` [removed]; O664-671; N—
- R04674 `OnInitEffect@b017ab#2` [removed]; O1845-1848; N—
- R04675 `OnInitEffect@b017ab#3` [removed]; O1945-1954; N—
- R04676 `OnInitEffect@b017ab#4` [removed]; O2690-2692; N—
- R04677 `OnInitEffect@b017ab#5` [removed]; O4446-4449; N—
- R04683 `OnResearched@b017ab#14` [removed]; O597-608; N—
- R04693 `OnResearched@b017ab#23` [removed]; O2891-2893; N—
- R04698 `OnResearched@b017ab#28` [removed]; O3429-3433; N—
### Data/TraitPreset.lua (1)
- R04769 `apply_func@88ad57#4` [removed]; O554-558; N—
### Data/TutorialStep.lua (4)
- R04893 `Code@318434#89` [added]; O—; N3098-3100
- R04957 `Value@318434#55` [added]; O—; N3145-3145; ONE-LINE
- R05046 `eval@318434#157` [added]; O—; N3093-3096
- R05047 `eval@318434#158` [added]; O—; N3139-3142

## Final limits and drift outbox

- Runtime timing, UI behavior, native message dispatch details, anonymous or
  dynamic consumers, consoles, assets absent from Src, and actual DLC override
  interiors remain unmeasured. No game launch or probe was warranted.
- No owner/non-owner failure was established. Base Data and consumers load for
  non-owners; DLC-named tech/resource/label references encountered here were
  gated. This does not clear DLC overrides.
- FR-2: Tech/TechPreset duplicate-registry semantics and the DeepScanning route
  were independently connected as above; source still does not explain or close
  the intermittent field report.
- LowGFungi is consistently an Underground tech and the FungalFarm task checks
  underground environment; no typo tell survived.
- No SameOldSlop row occurred in this exact 190-item batch.
- Drift to correct upstream: four ResearchTechsCombo caller explanations say
  the explicitly passed sentinel “arrives nil”; old ignores it, new captures it.
  Also, anonymous-member ordinal pairs must not be interpreted as same-preset
  deltas without enclosing-ID reconciliation.

