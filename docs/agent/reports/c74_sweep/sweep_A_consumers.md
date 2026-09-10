# Sweep A — animation-moment consumers, NAME vs INDEX (desk census, read-only)

Trees: `1.1.0` = `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src`, `1.0.7` = `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`.
Every citation is `tree path:line`. Nothing was edited. The only file written is this report, plus the helper
script `scratchpad/fxdump.py` (it parses FXPreset PlaceObj blocks).

---------------------------------------------------------------------------------------------------
## 0. Headline

| rank | INDEX caller | entity it runs on | preset? | what a player loses today |
|---|---|---|---|---|
| 1 | `BaseBuilding:TrackMultipleHitMoments` 1.1.0 Lua/Buildings/BaseBuilding.lua:1045-1046, :1053, :1065 (1.0.7 :731-732, :739, :751) | tracked attach of MOXIE (MoxiePump) and PreciousMetalsExtractor (UniversalExtractorHammer); also Electrolyzer and MicroGExtractor | **none**: doubly broken | MOXIE `Working` hit-moment1/2 particles + sounds; Rare Metals extractor `Working` hit-moment1-4 particles + sounds (C74). Electrolyzer and MicroG have no hit-moment FX rows, so they lose nothing visible |
| 2 | `Metatron:StartAnimMomentsThread` 1.1.0 Lua/Mysteries/Metatron.lua:52-53, :57, :69 (1.0.7 same lines) | `Monolith` (Metatron.lua:23) | **none**: doubly broken | Mystery 12 (Metatron): the `MetatronRotation` End1-End7 particle FX never fire |
| 3 | `PairMarker:TriggerAfter` fallback 1.1.0 CommonLua/Classes/ClassDefs/ClassDef-PresetDefs.generated.lua:1286-1287 (1.0.7 :1672-1673) | none in SMR | n/a | nothing; the class is unreachable in SMR (§4.3) |

**No INDEX caller runs on an entity that has a preset.** There is no "broken today even without new presets" case.
Presence side: the three consumers that DO run on preset entities are all NAME-correct:
- StirlingGeneratorBase (AdvancedStirlingGenerator): TimeToMoment
- CaveInRubble (CaveIn_*): literal plus TimeToMoment
- BakeryHands: AnimMomentHook → TimeToNextMoment

See §3.

**Hook users without presets.** These are NAME-correct but their entity has no preset, so they get zero moments and
their FX never fire. All of them go through `TrackAllMoments`:
- RCDriller `Drill` Hit
- TheExcavator `ExcavatorDigging` Hit1-12 / Out1-12
- Shuttle `ShuttleHubEnter` / `ShuttleHubExit` Hit
- WaterExtractor / MicroGAutoWaterExtractor `working` Hit
- RCTerraformer `Construct` / `Load` Hit1

See §5.

---------------------------------------------------------------------------------------------------
## 1. Task A1 — AnimMoment.lua anatomy

1.0.7 and 1.1.0 `CommonLua/Classes/AnimMoment.lua` differ in exactly one line (:11, the `table.ifilter` callback
arity). Each tree matches its own `table.ifilter`:
- 1.0.7 CommonLua/Core/types.lua:346 calls `filter(i, obj, ...)`; 1.0.7 AnimMoment.lua:11 is `function(_, m, moment_type)`.
- 1.1.0 CommonLua/Core/types.lua:363 calls `filter(obj, ...)`; 1.1.0 AnimMoment.lua:11 is `function(m, moment_type)`.

**Not a defect.**

The single name-keyed lookup is `GetEntityAnimMoments` (1.1.0 AnimMoment.lua:5-16): `preset_group[anim]` at :8, with
no number conversion. Every function below funnels into it.

| function | line (both trees) | takes `anim`? | converts index→name internally? | caller-safe regardless of arg? |
|---|---|---|---|---|
| `GetEntityAnimMoments(entity, anim, type)` | :5 | yes | **no** | no |
| `GetEntityAnimMomentsCombo(entity, first)` | :19 | no (iterates group) | n/a | yes (0 callers) |
| `CObject:GetAnimMoments(anim, type)` | :35-37 | yes | **only when anim is nil** (`GetStateText()`) | only with nil |
| `CObject:IterateMoments(anim, ...)` | :39 | yes | **no** | no |
| `CObject:GetChannelData(channel, idx)` | :100-111 | channel | **YES** `GetStateName(self:GetAnim(channel))` :107 | yes |
| `CObject:TimeToMoment(channel, type, idx)` | :127-138 | channel | **YES** via GetChannelData :131 | **yes** |
| `CObject:TimeToAnimMoment(anim, type)` | :140-150 | yes | **no** | no (0 callers) |
| `CObject:WaitMomentTrackedAnim(state, ...)` | :168-279 | `state` | the loop is safe (GetChannelData :220); the `GetAnimMoments(state)` at :215 is **not** converted, but `state` has also gone through `HasState`/`SetState` | safe if `state` is a name |
| `PlayTimedMomentTrackedAnim` / `PlayAnimWithCallback` / `PlayMomentTrackedAnim` | :156/:160/:164 | `state` | as WaitMomentTrackedAnim | same |
| `CObject:TimeToNextMoment(channel, idx, anim, ...)` | :281-302 | channel (+ optional anim) | **YES when anim is nil** :282 | yes if anim is omitted |
| `CObject:TypeOfMoment(channel, idx)` | :304-307 | channel | **YES** via GetChannelData :305 | **yes** |
| `CObject:GetAnimMoment(anim, type, idx)` | :309-319 | yes | **no** | no |
| `CObject:GetAnimMomentType(anim, idx)` | :321-327 | yes | **no** | no (0 callers) |
| `CObject:GetAnimMomentsCount(anim, type)` | :329-331 | yes | **no** | no |
| `GetStateMoments(entity, anim)` | :334-340 | yes | **no** | no |
| `GetStateMomentsNames(entity, anim, first)` | :342-353 | yes | no (guards `GetStateIdx(anim) == -1` only) | no (0 callers) |
| `CObject:OnAnimMoment(moment, anim)` | :152-154 | receives a name from GetChannelData | n/a | yes |

**So: every caller of `TimeToMoment`, `TypeOfMoment`, and `TimeToNextMoment(channel, idx)` with no anim argument is
index-safe by construction.** Only callers of GetAnimMoment(s), GetAnimMomentsCount, IterateMoments,
GetEntityAnimMoments, GetStateMoments, GetAnimMomentType and TimeToAnimMoment have to be classified.

Other moment readers outside AnimMoment.lua, all in Lua:
- `AnimMomentHook:WaitAnimMoment` (1.1.0 CommonLua/Classes/AnimMomentHook.lua:55-64) uses TimeToMoment. Safe.
- `WaitTrackMoments` (:74-112) uses TimeToNextMoment(1, i), and gets the anim from `GetStateName(obj)`. Safe.
- `GetAllAnimMoments` (1.1.0 Lua/Buildings/Building.lua:3346-3362) converts at :3347 via `GetStateName(obj:GetAnim(1))`. Safe.
- `TrackAllMoments` (Building.lua:3364-3409) uses TypeOfMoment and TimeToMoment. Safe. It stores the raw index at :3370,
  but only to compare it at :3379, which is fine.
- `BaseBuilding:TrackMultipleHitMoments` is **broken** (§4.1).

**Only moment source = `Presets.AnimMetadata`.**
- Group list verified by grep of `PlaceObj('AnimMetadata'` across both trees:
  - 1.1.0 Data/AnimMetadata.lua:13/24/35/49 (AdvancedStirlingGenerator: closing, idle, idleOpened, opening; all `Hit`)
  - :60 CaveIn_Buildings.falling (`Hit`)
  - :71 CaveIn_UndergroundDome.falling (`Hit`)
  - :81 CaveIn_UndergroundMicroDome.falling (`Hit`)
  - 1.1.0 DLC/norman/Presets/AnimMetadata.lua:166-167 BakeryHands.workIdle (bread_raw_start/end, bread_baked_start/end)
- 1.0.7 Data/AnimMetadata.lua is byte-identical to 1.1.0 (diff). 1.0.7 has no DLC AnimMetadata. **5 groups in 1.1.0, 4 in 1.0.7: the brief's list is confirmed.**
- No runtime writer adds groups:
  - `AnimMetadata:new` appears only at AnimMoment.lua:360 (`__default__`, AnimComponents only, no Moments), and that
    object goes to the engine `LoadAnimMetaData` (:372), **not** into `Presets.AnimMetadata`.
  - No `Presets.AnimMetadata[x] =` exists in either tree.
- The 5 group names appear in `_EntityData.generated.lua` only as their own keys (1.1.0 :51, :1759, :1872, :1893;
  norman :73). No other entity names them.
- Premise caveat (untraceable from Lua, §8): CommonLua/LuaExportedDocs/Game/LuaExports.lua:204-211 documents an engine
  `GetStateMoments` for "moments embeded in the entity XML itself". AnimMoment.lua:334 defines a Lua global of the
  same name that reads presets only. So the whole Lua moment path ignores any XML-embedded moments; whatever an
  entity's XML carries, the Lua path sees zero moments for non-preset entities.

---------------------------------------------------------------------------------------------------
## 2. Task A2 — every call site (excluding definitions and AnimMoment.lua-internal plumbing unless noted)

Regex used on all `*.lua` files in each tree:
`GetAnimMoment|GetAnimMoments|GetAnimMomentsCount|GetAnimMomentTime|IterateMoments|TimeToMoment|TimeToNextMoment|WaitAnimMoment|GetEntityAnimMoments|GetStateMoments|TimeToAnimMoment|TypeOfMoment|GetAnimMomentType|MomentTrackedAnim|PlayAnimWithCallback|GetChannelData`

It is substring-based, so it covers both `obj:F(` and `F(obj,`. `GetAnimMomentTime(s)` and `WaitAnimMoment` as
standalone names: no such function exists apart from `AnimMomentHook:WaitAnimMoment`, which is listed.

| function | 1.1.0 external call sites | 1.0.7 external call sites | class |
|---|---|---|---|
| GetAnimMomentsCount | 4: BaseBuilding.lua:1046; CaveInRubble.lua:136; Building.lua:3350; Metatron.lua:53 | 4: BaseBuilding.lua:732; CaveInRubble.lua:127; Building.lua:3169; Metatron.lua:53 | INDEX / NAME / NAME / INDEX |
| GetAnimMoment | 9: BaseBuilding.lua:1053, :1065; Metatron.lua:57, :69; ClassDef-PresetDefs.generated.lua:1287; StateObject.lua:977, :985, :993, :1006 | 9: BaseBuilding.lua:739, :751; Metatron.lua:57, :69; ClassDef:1673; StateObject.lua:977/985/993/1006 | INDEX×2 / INDEX×2 / INDEX-fallback / NAME×4 |
| GetAnimMoments (CObject) | 4: CommonLua/Ged/XDefClasses/AnimMetadataEditorTimeline.generated.lua:412, :592; CommonLua/Data/XDef/AnimMetadataEditorTimeline.lua:443, :636 (source strings of the same code) | same 4 | NAME (nil anim → GetStateText), editor-only |
| GetAnimMoments internal | AnimMoment.lua:40, :215, :330 | same | — |
| IterateMoments | 0 external; internal :132, :143, :294, :306, :310, :322 | same | — |
| TimeToMoment | 11: CaveInRubble.lua:138; Building.lua:3374, :3383, :3387; StirlingGenerator.lua:65, :67; AnimMomentHook.lua:57, :61; ClassDef:1857, :1861, :1915 | 11: CaveInRubble.lua:129; Building.lua:3193, :3202, :3206; StirlingGenerator.lua:65, :67; AnimMomentHook.lua:57, :61; ClassDef:2233, :2237, :2291 | all SAFE (internal convert) |
| TimeToNextMoment | 5: AnimMomentHook.lua:83, :90, :100; CommonLua/Editor/AnimationMomentsEditor.lua:335, :346 (+ internal AnimMoment.lua:224, which passes a converted anim) | 5: AnimMomentHook.lua:83/90/100; AnimationMomentsEditor.lua:328, :339 | all SAFE (anim nil → convert) |
| TypeOfMoment | 2: Building.lua:3352, :3372 | 2: Building.lua:3171, :3191 | SAFE |
| AnimMomentHook.WaitAnimMoment | 4: AnimMomentHook.lua:134; BaseBuilding.lua:1072; Building.lua:3376, :3404 | 4: AnimMomentHook.lua:134; BaseBuilding.lua:758; Building.lua:3195, :3223 | SAFE (uses TimeToMoment) |
| GetEntityAnimMoments | 4: AnimTransition.lua:230; ActionFX.lua:1526; ClassDef:1975; _cobject.lua:1739 (+ internal AnimMoment.lua:36, :336, :345) | 3: AnimTransition.lua:230; ActionFX.lua:1450; ClassDef:2351 | NAME ×4 (editor/preset-load) |
| GetStateMoments | 2: ActionFX.lua:3159; CommonLua/Libs/DevToolsPublic/EntityViewer.lua:284 | 2: ActionFX.lua:3059; EntityViewer.lua:284 | NAME (editor/dev) |
| GetStateMomentsNames | **0** | **0** | control: the same regex hits the definition AnimMoment.lua:342 |
| GetEntityAnimMomentsCombo | **0** | **0** | control: the regex hits the definition :19 |
| TimeToAnimMoment | **0** | **0** | control: hits the definition :140 |
| GetAnimMomentType | **0** | **0** | control: hits the definition :321 |
| PlayTimedMomentTrackedAnim / PlayAnimWithCallback | **0** / **0** | 0 / 0 | control: hits the definitions :156 / :160 |
| PlayMomentTrackedAnim | 3: AnimTransition.lua:72; XPrg.lua:1184, :1186 (code generator) | same lines | NAME |
| WaitMomentTrackedAnim | 1: AnimTransition.lua:356 (+ recursion :187) | same | NAME |
| GetChannelData | internal only (:131, :220, :305) | same | — |
| Moment wrappers (not in AnimMoment.lua) | TrackAllMoments ×6: ShuttleHub.lua:1632, :1649; WaterExtractor.lua:115; TheExcavator.lua:120; RCTransport.lua:134; RCDriller.lua:105. GetAllAnimMoments ×1: Building.lua:3369. TrackMultipleHitMoments ×2: BaseBuilding.lua:929, :947. WaitTrackMoments ×1: AnimMomentHook.lua:127 | TrackAllMoments ×6: ShuttleHub.lua:1442, :1454; WaterExtractor.lua:86; TheExcavator.lua:124; RCTransport.lua:144; RCDriller.lua:105. GetAllAnimMoments: Building.lua:3188. TrackMultipleHitMoments: BaseBuilding.lua:621, :639 | wrappers are NAME-safe except TrackMultipleHitMoments |

`XPrgPlayTrackedAnim`: the property `moment_tracking` appears only in CommonLua/X/XPrg.lua:1083-1196 (both trees).
No Prg data sets it. It is a generator with no users in SMR, and would emit a string literal (NAME) anyway.

---------------------------------------------------------------------------------------------------
## 3. Task A3 — classification, traced

**NAME — literal or state-name variable:**
- 1.1.0 CaveInRubble.lua:136 uses the literal `"falling"`. 1.0.7 :127 uses `state`, and `state = GetStateName(self:GetState())`
  (1.0.7 :124), which is a NAME. Entity `CaveIn_Buildings` (CaveInRubble.lua:6), or `CaveIn_UndergroundMicroDome`
  after `ChangeEntity` (:19, :54). **Both have presets**, and this path works. The FX gated are CaveInsHitDome and
  damage timing (`Sleep(t)` :140).
- Building.lua:3350 `GetAnimMomentsCount(anim)`: `anim = anim or GetStateName(obj:GetAnim(1))` at :3347, and the only
  caller (:3369) passes nil. NAME.
- StateObject.lua:977/985/993/1006: `anim = anim or state:GetAnimation(self)`, then `anim ~= "" and anim or
  self:GetStateText()` (:968-969), which are string state names. NAME. Unreachable in SMR anyway: the token grep for
  `StateObject"` hits only CommonLua/Classes/StateObject.lua and ActionFX.lua in both trees. No inheritor and no
  `class_parent`.
- AnimTransition.lua:230: `node.anims[1]` (:228), a preset string. :72: `anim` is a prop id via cheat. :356:
  `transition` is `transition.anim` (:347), a string. NAME.
- ActionFX.lua:1526 (GetError): `anim = self.Action`, validated by `EntityStates[anim]` (:1518). :3159: `o.Animation`
  with a HasState guard. NAME, editor.
- ClassDef:1975 `channels[channel].Animation`, a string. NAME, editor combo.
- _cobject.lua:1739 (1.1.0 only): `obj:GetProperty(anim_prop)` guarded by `GetStateIdx(anim) ~= -1`. NAME, editor combo.
- EntityViewer.lua:284: `state` is a dev-tool state name. NAME.

**SAFE by internal conversion** (§1): every TimeToMoment, TypeOfMoment, TimeToNextMoment(1, i) and WaitAnimMoment
site listed in §2.

**INDEX:** BaseBuilding.lua:1045-1046/1053/1065, Metatron.lua:52-53/57/69, and the ClassDef:1286-1287 fallback (§4).

**UNKNOWN:** none. Every `anim` argument was traced to its assignment or to its one caller hop.

Blind-spot closure for INDEX: a sweep of every `:GetAnim(` line not wrapped in `GetStateName(`, both trees (~35 lines
each). Each remaining raw index is used only in comparisons, `GetAnimDuration`, `SetAnim`, `GetStepLength` or
`IsStaticAnim`, except the three INDEX callers above. Examples:
- ActionFX.lua:3284/3301/3307 (1.0.7 :3178/3195/3201): comparison only
- Components.lua:295/313/319/322, ClassDef:1467/1471/1484/1724/1875 (1.0.7 :1853/1857/1870/2110/2251), Building.lua:3370/3379: not moment calls
- OmegaTelescope.lua:13/65/97 compare with `EntityStates.*`, which is correct

---------------------------------------------------------------------------------------------------
## 4. Task A4 — INDEX callers in detail

### 4.1 BaseBuilding:TrackMultipleHitMoments (C74). INDEX, doubly broken

- 1.1.0 BaseBuilding.lua:1045 `local anim = obj:GetAnim(1)` gives a number. At :1046, `GetAnimMomentsCount(anim, "Hit")`
  sends it to `preset_group[number]`, which is nil, so the count is 0 and :1047-1048 returns before any FX.
  :1053 and :1065 pass `obj:GetAnim(1)` raw as well.
- 1.0.7 :731/:732/:739/:751 are identical. The only diff is closure argument passing (:730 vs 1.1.0 :1044).
- **Even with a name, there is still no preset** for any entity involved, so the count stays 0. A fix needs the
  conversion **and** Hit moments for the tracked entity.

**Coordinator's lead: how `obj` is chosen.** `BaseBuilding:ChangeWorkingStateAnim` (1.1.0 :878-954):
1. It builds `att_arr = {self, attaches...}` (:891-892).
2. If `play_working_anim_on_this_attach` is set, it pins that class (:895-896). None of the five classes sets it
   (grep: only BaseBuilding.lua:50 default and Bakery.lua:9).
3. It picks the first element with `HasState(work_anim_start = "start")` (:902, default :52), and otherwise the first
   with `HasState(work_anim_loop = "working")` (:940, default :53).
4. `TrackMultipleHitMoments(obj, "Working", nil, <list-or-nil>, true)` runs at :928-929 after the start anim, or at
   :946-947.
5. `PlayFX("Working", hit_moment_table[i], self, obj)` (:1074): the actor is the building, the target is `obj`.

| base class (def) | flag value | inheritors (both trees, generated templates) | building entity | tracked `obj` (see note) | preset? | player-visible FX gated (1.1.0 Data/FXPreset) |
|---|---|---|---|---|---|---|
| ElectrolyzerBase (Lua/Buildings/Electrolyzer.lua:1-7, :5) | `true` → default `hit_moments` = {hit-moment1, hit-moment2} (BaseBuilding.lua:1025-1026) | 1: `Electrolyzer` (Lua/BuildingTemplate/Electrolyzer.generated.lua:5) | `Electrolyzer` (:32; 1.0.7 :32) | not resolved (no Lua auto-attach data) | no | **none**: no `Working` rows for actor Electrolyzer. Silent loss is inert today |
| MOXIEBase (MOXIE.lua:1-6, :5) | `true` → {hit-moment1, hit-moment2} | 1: `MOXIE` (MOXIE.generated.lua:5) | `Moxie` (:33) | `MoxiePump` attach (the FX Target field says so) | no | ActionFXParticles.lua:842 (hm1), :879 (hm2); ActionFXSound.lua:17136, :17146 (hm1, target MoxiePump), :17177 (hm2). **All dead** |
| MicroGExtractorBase (MicroGExtractor.lua:120-124, :123) | {hm1, hm2, hm3} | 4: MicroGExtractor, MicroGExtractorMetals, MicroGExtractorRareMetals, MicroGExtractorExoticMinerals (each `.generated.lua:5`) | `MicroGExtractor` (e.g. MicroGExtractor.generated.lua:77) | not resolved | no | **none**: no `Working` hit-moment rows for MicroG actors |
| PreciousMetalsExtractorBase (MetalsExtractor.lua:22-29, :25) | {hm1, hm2, hm3} | 1: `PreciousMetalsExtractor` (PreciousMetalsExtractor.generated.lua:5) | `UniversalExtractor` (1.1.0 :76; 1.0.7 :59) | `UniversalExtractorHammer` attach (FX Target) | no | ActionFXParticles.lua:860/:897/:916 (hm1-3); ActionFXSound.lua:17156, :17166, :17187, :17197, :17208, :17218 (hm1-3), :17229, :17239 (hm4, which is unreachable anyway because the override list has only 3). **All dead** (this is the C74 Rare Metals case) |
| PreciousMineralsExtractorBase (PreciousMineralsExtractor.lua:13-18, :17; 1.0.7 :18) | {hm1, hm2, hm3} | **0 in both trees**. The only hits for the string `PreciousMineralsExtractor` in all `*.lua` are its own DefineClass lines. Control: the same `__parents` regex finds `PreciousMetalsExtractorBase` in its template | — | — | — | dead code |

Note on `obj`: for MOXIE and PreciousMetals, `obj` is inferred from the FX preset `Target` fields (MoxiePump,
UniversalExtractorHammer) combined with `PlayFX(..., self, obj)` at :1074. The auto-attach lists themselves are not in
the Lua tree: a grep of `Data/**/AutoAttach*.lua` for these names returned 0. The entities `MoxiePump` and
`UniversalExtractorHammer` exist (1.1.0 _EntityData.generated.lua:15380, :26913) and are not preset groups. The answer
does not depend on which attach is tracked: no building or attach entity here is one of the 5 groups.

### 4.2 Metatron:StartAnimMomentsThread. INDEX, doubly broken

- 1.1.0 Lua/Mysteries/Metatron.lua:52 `local anim = self:GetAnim(1)` gives a number. :53 `GetAnimMomentsCount(anim,
  moment)` returns 0. `while ... number_of_hits > 0` (:56) never runs. :57 and :69 pass the same index.
- Started from Metatron.lua:138 after arrival. Two threads are created, for `"Start"` and `"End"` (:85-86).
- Entity `Monolith` (:23); _EntityData :15208; no preset.
- Gated FX: `PlayFX("MetatronRotation", moment .. i, self)` (:78), with FX rows MetatronRotation End1-End7 at
  ActionFXParticles.lua:5486-5601 (1.0.7 :5718-5833).
  - There are no `Start#` rows.
  - The `hit-moment1-7` MetatronRotation sounds (ActionFXSound.lua:7442-7514) are never emitted by this code, which
    only emits Start#/End#. So those sounds depend on some other emitter; I found none in the grep.
- Effect: **Mystery 12 rotation-end particles never play.** It is cosmetic, and only during that mystery.
- 1.0.7 is identical at the same lines. The Metatron diff touches only flags (:21) and storm/move threads.

### 4.3 PairMarker:TriggerAfter. INDEX on the fallback branch, unreachable

- 1.1.0 ClassDef-PresetDefs.generated.lua:1286 `local anim = channel and channel.Animation or
  obj:GetAnim(next_state.SyncMomentChannel)`. That is a number whenever the next state defines no animation for the
  sync channel, and :1287 `obj:GetAnimMoment(anim, SyncMoment, 1)` then returns nil. 1.0.7 :1672-1673 is the same.
- My first assignment regex (`=\s*x:GetAnim(`) missed this `or obj:GetAnim(` shape. The full `:GetAnim(` sweep in §3
  caught it.
- **Reach: zero.** `PairMarker` occurs in exactly one file per tree: ClassDef-PresetDefs.generated.lua, 54 hits
  each, a count grep over all file types. No preset data, no placement, no inheritor.

---------------------------------------------------------------------------------------------------
## 5. Task A3b — hook / tracker users (entity, moment types, preset)

How the hook obtains the anim: every hook path goes through NAME-safe primitives.
- `AnimMomentHook:WaitAnimMoment` (AnimMomentHook.lua:55-64) uses `TimeToMoment(1, moment)`, which converts
  internally.
- `WaitTrackMoments` (:74-112) takes `anim = GetStateName(obj)` (:81) and `TimeToNextMoment(1, i)` with anim nil
  (:83/:90/:100), which converts.
- `OnAnimMoment` (AnimMomentHook.lua:66-72 → AnimMoment.lua:152-154) receives that name, then runs
  `PlayFX(FXAnimToAction(anim), moment, self)`.

**The hook never passes an index.** Its only failure mode is a missing preset.

| user | how it hooks | entity | moments waited on | preset? | FX rows that therefore never fire (1.1.0; same rows in 1.0.7) |
|---|---|---|---|---|---|
| BakeryHands (1.1.0 DLC/norman/Code/Bakery.lua:1-4) | `AnimMomentHook`, `anim_moments_hook_all = true` → WaitTrackMoments (AnimMomentHook.lua:126-129) | `BakeryHands` (norman _EntityData.generated.lua:73) | all moments of `workIdle`: bread_raw_start/end, bread_baked_start/end | **YES** (norman AnimMetadata.lua:3-169) | none: works. FX `Anim:workIdle` bread objects (norman ActionFXObject.lua:3-29). **Positive control of the NAME path.** 1.1.0 only; 1.0.7 has no Bakery code |
| StepObject (AnimMomentHook.lua:360-370) | OnMomentFootLeft/Right | — | FootLeft / FootRight | — | **no SMR inheritor**: the token grep for `"StepObject"`/`"StepObjectBase"` hits only AnimMomentHook.lua:218/:361, and the `class_parent = "...StepObject..."` grep returns 0 |
| AutoAttachAnimMomentHookObject (AnimMomentHook.lua:395-402) | hook | — | — | — | no inheritor (same greps) |
| RCDriller (Lua/Units/RCDriller.lua:104-105) | `TrackAllMoments(self, "Drill")` | `RoverRussiaDriller` (:6; _EntityData :18894) | all moments of `workIdle` | **no** | `Drill` Hit particles ActionFXParticles.lua:6999 plus sound ActionFXSound.lua:5568 |
| TheExcavator (Lua/Buildings/TheExcavator.lua:120) | `TrackAllMoments(self.arm, "ExcavatorDigging", self.arm)` | `ExcavatorShovel` attach (:47; _EntityData :10535) | all moments of `working` | **no** | `ExcavatorDigging` Hit1-12 and Out1-12 particles, ActionFXParticles.lua:115-530 (24 rows) |
| ShuttleHub landing / take-off (ShuttleHub.lua:1632, :1649) | `TrackAllMoments(shuttle, "ShuttleHubEnter"/"ShuttleHubExit", shuttle, self)` | `Shuttle` (ShuttleHub.lua:461; _EntityData :19461) | moments of `landing`/`landing2`/`takeOff`/`takeOff2` (:1582-1604) | **no** | ShuttleHubEnter Hit sound ActionFXSound.lua:13480; ShuttleHubExit Hit particles ActionFXParticles.lua:8404, :8421 plus sound ActionFXSound.lua:13519 |
| WaterExtractorBase (WaterExtractor.lua:112-116) and MicroGAutoWaterExtractor (MicroGAutoWaterExtractor.generated.lua:5, inherits WaterExtractorBase) | `TrackAllMoments(pump, "working", self)` | `WaterExtractorPump` attach (_EntityData :27782) | moments of the pump's current anim | **no** | `working` Hit sounds: actor WaterExtractor at ActionFXSound.lua:20286, :20296; actor MicroGAutoWaterExtractor at :20276 |
| RCTerraformer (RCTerraformer.lua:35, :96-102 → RCTransport.lua:133-134) | `TrackAllMoments(self, fx, self, building)` when `anim_idle = "workIdle"` | `RoverTerraformer` (:6; _EntityData :18942) | moments of `workIdle` | **no** | `Construct` Hit1 particles ActionFXParticles.lua:6948; `Load` Hit1 particles :7119 plus sound ActionFXSound.lua:7031 (fx comes from LandscapeConstructionSite.lua:423/:427) |
| RCConstructor / RCConstructorBase (RCConstructor.lua:26, RCConstructorBase.lua:26) | same RCTransport path, `constructIdle` | `RoverIndiaConstructor` (:4/:6; _EntityData :18875) | moments of `constructIdle` | **no** | none found (no non-start/end rows for these actors), so inert |
| RCTransport / RCSafari / Train | `track_anim_moments = false` (RCTransport.lua:71, RCSafari.lua:62). Train.lua:51 declares only a thread field; no assignment was found | — | — | — | inert |
| Unit:PlayFXMoment (Unit.lua:89-93) ← Colonist.lua:4965, Drone.lua:1578 | **not a moment reader**: it does `PlayFX(self.fx, <literal moment>, ...)` with no lookup | — | — | — | out of scope. The MysteryDream `hit-moment` particle (ActionFXParticles.lua:5143) fires directly |

For the TrackAllMoments users, the failure is silent. `GetAllAnimMoments` returns `{}`, `TypeOfMoment(1, 1)` returns
false, so `next_m` is `""` (Building.lua:3372) and the loop is skipped (:3379).

---------------------------------------------------------------------------------------------------
## 6. Side findings (not INDEX, recorded so they are not re-discovered)

- **ActionFX `OnMsg.GatherFXMoments`**: 1.1.0 CommonLua/Classes/ActionFX.lua:1491-1492 (1.0.7 :1415-1416) assigns
  `entity = GetAnimEntity(entity, anim)` but then reads the unassigned `anim_entity`, so the moment combo is always
  empty for anim-specific FX. **Editor-only; no player effect.**
- **Plain StirlingGenerator** (entity `StirlingGenerator` / `StirlingGeneratorCP3`, StirlingGenerator.generated.lua:31,
  :42) has no preset. `TimeToMoment(1, "Hit")` returns nil, so there is no Sleep, and `hit-moment` plays at anim start
  (StirlingGenerator.lua:65-72). This is **inert**: the only `StirlingGenerator` `hit-moment` FX row has actor
  AdvancedStirlingGenerator (ActionFXParticles.lua:672), and that entity does have a preset, so its path works.
- `CaveIn_UndergroundDome.falling` preset (Data/AnimMetadata.lua:71) has no code consumer. CaveInRubble swaps to
  `CaveIn_UndergroundMicroDome` only (CaveInRubble.lua:19, :54); the per-dome line is commented out at :53.

---------------------------------------------------------------------------------------------------
## 7. Task A6 — 1.0.7 vs 1.1.0

| item | 1.0.7 | 1.1.0 |
|---|---|---|
| Preset groups | 4 (Data only) | 5 (+ DLC/norman BakeryHands) |
| AnimMomentHook user BakeryHands | absent (no Bakery code in 1.0.7 DLC/norman/Code) | present, works |
| TrackMultipleHitMoments | INDEX at :731-732/:739/:751; flagged classes and templates are the same 5 / 8 | INDEX at :1045-1046/:1053/:1065; only closure-arg passing differs |
| Metatron | INDEX, same lines | INDEX, same lines |
| PairMarker fallback | ClassDef :1672-1673 | ClassDef :1286-1287 |
| CaveInRubble | `GetAnimMomentsCount(state, "Hit")` with `state` = GetStateName(...) (:124, :127) | literal `"falling"` (:136); both NAME |
| GetEntityStateMomentItems (_cobject.lua:1728) | absent | present (editor, NAME) |
| AnimMoment.lua | ifilter 3-arg callback | ifilter 2-arg callback; each matches its own types.lua |
| FX rows gated | same set; MicroGAutoWaterExtractor `working` Hit has 2 rows (ActionFXSound.lua:22030, :22040) | 1 row (:20276) |

**No INDEX caller was added or removed between branches.**

---------------------------------------------------------------------------------------------------
## 8. Controls run

1. Main moment regex (§2) hits the known broken lines: 1.1.0 BaseBuilding.lua:1046/1053/1065 and Metatron.lua:53/57/69;
   1.0.7 BaseBuilding.lua:732/739/751.
2. Inline-index regex `(<moment fns>)\([^)]*(GetAnim\(|GetState\(\))` hits exactly BaseBuilding.lua:1053/1065 (1.1.0)
   and :739/:751 (1.0.7). Nothing else matches.
3. Multi-line split-call regex `(Moment[A-Za-z]*|MomentTrackedAnim|PlayAnimWithCallback|GetChannelData)\(\s*$` returns
   **0**. The anchor control `DefineClass\.AnimMomentHook =\s*$` hits both trees at AnimMomentHook.lua:34, so the
   `\s*$` form works on these files.
4. Zero-caller functions (GetStateMomentsNames, GetEntityAnimMomentsCombo, TimeToAnimMoment, GetAnimMomentType,
   PlayTimedMomentTrackedAnim, PlayAnimWithCallback): the same regex hits each definition line.
5. Full `:GetAnim(` sweep minus `GetStateName(` (both trees). It closed the `or obj:GetAnim(` blind spot and found
   ClassDef:1286 / 1.0.7 :1672.
6. PreciousMineralsExtractorBase has 0 inheritors. Control: the identical regex finds PreciousMetalsExtractorBase in
   its template.
7. PairMarker reach: a count grep over **all** file types finds 54 hits per tree, all in one file.
8. Hook-class reach: the token grep `"AnimMomentHook"|"StepObject"|"StepObjectBase"|"AutoAttachAnimMomentHookObject"`
   finds Bakery.lua (1.1.0) plus CommonLua only. The `class_parent = "...(AnimMomentHook|StepObject|...)"` grep
   returns 0.
9. FX gating comes from `fxdump.py` over `**/FXPreset/*.lua`: 10 files in 1.1.0 (85 rows), 7 files in 1.0.7 (86 rows),
   filtered to non-start/end moments for the tracked actions.

## 9. Could NOT trace

- **Auto-attach membership**, i.e. which attach `obj` is for Electrolyzer and MicroGExtractor. The spec is not in the
  Lua tree. For MOXIE and PreciousMetals, `obj` was inferred from FX `Target` fields. The answer does not change the
  verdict, because no candidate entity is a preset group.
- **The engine `GetAnimEntity(entity, anim)` redirect**, i.e. whether some entity borrows animations from another.
  Lua evidence only: the 5 group names occur in EntityData solely as their own keys.
- **XML-embedded moments** (LuaExports.lua:204-211). The Lua path ignores them by construction, but I cannot see
  whether e.g. `Moxie` or `Monolith` XML carries Hit moments. A live `GetStateMoments` call from the engine side, if
  the C export is still reachable, would tell.
- **Load order of the Lua `GetStateMoments`** (AnimMoment.lua:334) vs the engine export. I assume the Lua global
  wins; this is unverified.
- The emitter of the MetatronRotation `hit-moment1-7` sounds (ActionFXSound.lua:7442-7514). I did not find one; it
  may be dead data or come from a path I did not grep.
