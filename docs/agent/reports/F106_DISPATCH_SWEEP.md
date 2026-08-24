# F106 dispatch-reach sweep — the measurement, the reversal, and the defect it found

⚠️ **A report is not authority.** Where this and an entry disagree, the entry
wins or this file is corrected. The entries are `F106` (closed, refuted),
`F107` (filed, new), `F105` (corrected), `F33` (cleared), and fact `EF-066`.
Primary evidence is the log, which outranks this summary:
**`docs/archive/f106_Mars.exe-20260824-02.32.27.log`**.

Written 2026-08-24 by chain `f106-dispatch`, prompt `01_PROBE_opus.md`.
Predictions committed and pushed beforehand: `reports/F106_PREDICTIONS.md`
(commit `e2759bd`, 2026-08-24 02:31:21 −0400; the log is `02.32.27`, so the
prediction landed **before** the run).

---

## 0 · Lead with what changes a decision

1. ⛔ **`F106` IS REFUTED.** The pack's class-method wraps DO reach subclass
   instances. `Fix_SmallLandscapeSites` (F33) is not a no-op and never was. The
   "~60 wraps may be silent" alarm is withdrawn.
2. ⛔ **A REAL DEFECT WAS FOUND INSTEAD — `F107`.** `Fix_LandscapeCostRefresh`
   (F105's fix, built the same day) captures `prev` as **nil** on all three
   landscape leaf classes. The guard works; the delegation is dead code that
   raises if reached. The pack's only instance. **It is the module the queued
   1.0.x upload exists to deliver.** Owner decision on checklist 74.
3. ✅ **`EF-066`'s three-week-old unswept question is now enumerated** — 105
   declared targets, 97 clean, and the unreached classes are shipped subclasses
   that re-declare the method. Under-coverage, never new harm.
4. ⛔ **Checklist 74's audit is NOT complete and cannot be completed by this
   instrument.** The sweep reports which classes do not reach a wrap; it does
   **not** report which of them are ever instantiated. No number here is a
   broken-fix count.

## 1 · Run health — the gate, before any reading is banked

| gate | required | measured |
|---|---|---|
| game build | `1.0.7.396349` (`EF-014` pin) | `Build version: 1.0.7.396349` ✅ |
| pack gate | `78/78 fixes active` | `[SMRTest] fix pack present: 78/78 fixes active` ✅ |
| `applied` lines | 78 (`doccheck --emit-counts`) | 78 ✅ |
| opt-in pack | OFF (checklist 43) | `opt-in pack NOT loaded` ✅ |
| save-rescue | absent by design | `save-rescue NOT loaded` ✅ |
| harness | armed, new colony, no save touched | `[SMRAUTO] armed (flag file Code/96_AutoRunFlag.lua)` → `BEGIN` → `END` → `done` ✅ |
| probe sweep | clean before testing | `grep -rln "TEMPORARY"` = 0 hits, both repos ✅ |
| suite | — | `---- 75 PASS, 1 FAIL, 24 SKIP, 0 ERROR ----` of 100 probes |

Gate healthy ⇒ readings banked. Harness **disarmed** after the run
(`metadata.lua` back to its shipped shape; TestKit tree clean).

### Unexplained log lines: none, and here is the accounting

60 `[LUA ERROR]` lines, **all** of one signature: 59 ×
`Lua/Flight.lua:465: attempt to index a boolean value (field 'objects_to_mark')`
plus 1 × `:479 (field 'objects_to_unmark')`.

⛔ Not dismissed as "not ours" — aged instead. This is the documented
synthetic-map noise set of the autorun harness, already named in
`TestKit/Code/96_AutoRunFlag.lua`'s own header and recorded on `F49:46` as
*"Noise is the documented set only: 60 `Flight.lua objects_to_mark`"* — the exact
count seen here. Age, measured against archived logs:

| leg | date | Flight.lua hits | total `[LUA ERROR]` |
|---|---|---|---|
| this leg | 2026-08-24 | 60 | 60 |
| `vl97a_*` (autorun, new colony) | 2026-08-19 | 49 | 49 |
| `u3suite_*` (autorun, new colony) | 2026-08-15 | 60 | 60 |
| `u2run3_*` (co-run, loads a save) | 2026-08-11 | 0 | 0 |
| `corun1_*` (co-run, loads a save) | 2026-08-04 | 0 | 0 |

⇒ It is an artefact of the harness's **generated** map, not of a save, not of
this leg, and not of the pack. ⚠️ It is nonetheless a genuine vanilla nil-guard
gap (`objects_to_mark` is a boolean class default being indexed) and it is
already carried on `F49` and `C47`; nothing new is claimed and nothing is filed.

## 2 · The reversal, and the source read that explains it

**`F106` said:** the class builder COPIES an unflagged parent's members into each
descendant at build time, and *"the pack, whose `00_Core` applies every fix after
`ClassesBuilt`"*, therefore patches a table those instances never consult.

**The copy branch is real.** The measurement confirms it directly — each leaf
class holds its own key:

```
SMRTEST-F33DISPATCH LandscapeConstructionSite:      rawget=own-copy resolved==base=true
SMRTEST-F33DISPATCH ClearWasteRockConstructionSite: rawget=own-copy resolved==base=true
SMRTEST-F33DISPATCH TerrainPaintConstructionSite:   rawget=own-copy resolved==base=true
```

**The premise is false.** `resolved==base=true` says the copy each leaf holds
**is the pack's own wrapper.** Re-derived at `ModTools\Src`:

| step | citation |
|---|---|
| `SMRFixPack.Register` calls `run_apply` **inline**, nothing defers it | `Code/00_Core.lua:452` (`run_apply` at `:387`) |
| mod files are loaded by `ModsLoadCode()` | `CommonLua/Core/autorun.lua:423` |
| `Msg("Autorun")` — which the class builder hangs off — is raised **later** | `autorun.lua:557`; builder at `CommonLua/Core/classes.lua:980` |
| at that moment `_G[classname]` is the raw **classdef**, with no metatable | `classes.lua` `define`: `rawset(_G, class, class_def)` |
| the builder then copies members down | `ResolveValues`, `classes.lua:693-729` |

⇒ **the pack patches classdefs, and the builder copies the pack's function into
every descendant.** Only `SMRFixPack.DataPatch` waits for `ClassesBuilt`
(`00_Core.lua:334`), for the unrelated F87 enable-path reason. F106 generalised
that half's comment across the whole file.

⭐ This is the **same capture** `EF-066` already recorded for combined
`Init`/`Done` (via `ClassesPreprocess` composition), now shown to hold for
**plain methods** by a different engine mechanism (the builder's member copy).

### Two citation corrections that outlive this report

* **`classes.lua:986-988` is INVERTED against the code.** The comment says
  *"class tables for which 'hierarchy_cache' is true are flattened"*; `:700-709`
  flattens when `parent_def.__hierarchy_cache == **nil**`. The code is
  authoritative. F106 followed the code correctly, but the comment must never be
  cited as corroboration. (Corrected on `F106`, `F105`, `EF-066`.)
* **`EF-066`'s "~60 (class, method) targets" was an estimate and is low.** The
  real figure, generated by `tools/harvest_wrap_targets.py`: **105 entries, 100
  distinct pairs, 46 classes.**

## 3 · The sweep

Probe `DispatchReach`, `TestKit/Code/64_Probes_Wave14.lua`. For every declared
target `{C, m}` it walks every descendant `D` of `C` and compares `D[m]` with
`C[m]` — a full metatable resolution, i.e. literally the lookup `site:m()`
performs. Every target is logged, clean ones included, so a sweep that crashed
early cannot pass for a sweep that found nothing.

```
SMRTEST-DISPATCH TOTAL targets=105 clean=97 with-unreached=8 missing=0
  | descendants=13127 reach=1981 UNREACHED=66
  | MULTI-PARENT=11080 (of which unreached=1328, reported separately,
                        NOT folded into either verdict)
```

### Every target with at least one unreached descendant

| module | target | link | desc | reach | UNREACHED | MULTI (unreached) |
|---|---|---|---|---|---|---|
| `Fix_MoraleComfortTooltip` | `PropertyObject.GetProperty` | chain | 7063 | 1189 | **52** | 5822 (23) |
| `Fix_TrainsToVoid` | `Building.OnDemolish` | chain | 575 | 93 | **4** `AsteroidCatcher(Base)`, `TradePad(Base)` | 478 (60) |
| `Fix_RocketInteractGuard` | `RCTransport.CanInteractWithObject` | copy | 4 | 0 | **2** `RCConstructor(Base)` | 2 (2) |
| `Fix_RocketInteractGuard` | `RCTransport.InteractWithObject` | copy | 4 | 0 | **2** `RCConstructor(Base)` | 2 (2) |
| `Fix_LandscapeCostRefresh` | `ConstructionSite.RefreshConstructionResources` | copy | 13 | 5 | **3** the three landscape leaves | 5 (0) |
| `Fix_LandscapeCostRefresh` | `ClearWasteRockConstructionSite.GatherConstructionResources` | copy | 1 | 0 | **1** `LandscapeConstructionSite` | 0 (0) |
| `Fix_LakeEntombment` | `Unit.ExitImpassable` | copy | 43 | 0 | **1** `Firefly` | 42 (13) |
| `Fix_ShuttleHubOffAvailable` | `BaseBuilding.GetWorkNotPossibleReason` | copy | 633 | 5 | **1** `UpgradeConsumption` | 627 (578) |

### Targets clean on the single-parent path but with multi-parent misses

| module | target | MULTI (unreached) |
|---|---|---|
| `Fix_ShuttleHubOffAvailable` | `BaseBuilding.GetWorkNotPermittedReason` | 627 (**578**) |
| `Fix_GhostFarmOxygen` | `Building.SetDome` | 478 (**40**) |
| `Fix_StaleReservations` | `Residence.ReserveResidence` / `.CancelResidenceReservation` | 25 (**4**) each |
| `Fix_RocketDroneChurn` | `CargoTransporterNew.UpdateCargoResourceRequests` | 11 (**11**) |
| `Fix_TrackConnectorPingPong` | `TrackConnectedObjBase.Done` | 6 (**6**) |
| `Fix_LanderCargoRatchet` | `CargoTransporterNew.GetCargoWeightCapacity` | 11 (**4**) |
| `Fix_AutomationLawCompensation` | `Shroudable.IsShroudedInRubble` | 592 (**3**) |

The remaining 90 targets are clean on every descendant. **0 targets missing from
the build** ⇒ every declared `{class, method}` still resolves to a function.

### What the unreached classes actually are — spot-checked at Src

Two hand re-derivations, one hit and one clean, as the audit brief requires:

* **HIT re-derived.** `Fix_RocketInteractGuard` wraps
  `RCTransport.CanInteractWithObject` / `.InteractWithObject`, unreached on
  `RCConstructor` and `RCConstructorBase` — because
  `Lua/Units/RCConstructorBase.lua:341` and `:356` **declare both methods
  themselves**. A re-declaration below a wrap is EF-066's original question, not
  F106's mechanism. RC Constructors keep vanilla behaviour there.
* **CLEAN re-derived.** `Fix_BrokenTrackSalvage` wraps
  `TrackBase.BreakTrackElement`, reported `link=copy desc=1 reach=1
  UNREACHED=0`. `BreakTrackElement` is declared on `TrackBase` and **nowhere
  else** (whole-tree grep: `Lua/Buildings/Track.lua:618`, single definition), and
  `TrackBase`'s classdef does not set `__hierarchy_cache`, so `Track` took a
  build-time COPY of it — and that copy is the pack's wrapper. ⭐ This is the
  reversal in miniature: a `link=copy` target whose descendant reaches the wrap
  anyway, which is impossible under F106's model and required under the measured
  one. A false negative here would be the expensive error, so it is worth stating
  what would have falsified it: `Track` holding a function ≠ `TrackBase`'s.
* ⚠️ **A spot check I got wrong, corrected here rather than dropped.** I first
  offered `Fix_GhostFarmOxygen Building.SetDome` as the clean case on the grounds
  that "nothing between re-declares `SetDome`". **That is false** — four classes
  under `Building` re-declare it: `BaseResearchLab` (`ResearchLab.lua:179`),
  `Residence` (`Residence.lua:171`), `TrainingBuilding`
  (`TrainingBuilding.lua:81`), `WaterReclamationSpire`
  (`WaterReclamation.lua:78`). The sweep still read `UNREACHED=0` for it, and the
  reason is that all four are **multi-parent** classes (`Residence.__parents =
  { "StatsChange", "Holder" }`; `TrainingBuilding.__parents = { "ShiftsBuilding",
  "Holder", "DomeOutskirtBld" }`), so they and their descendants land in the
  MULTI bucket — which is exactly where the target's `MULTI=478 (unreached 40)`
  comes from. ⇒ the reading was right, my explanation of it was not, and the 40
  are the four re-declaring subtrees. **`Fix_GhostFarmOxygen`'s wrap does not
  reach residences, research labs, training buildings or water reclamation
  spires.** Routed to `EF-066` / checklist 74 with the other re-declaration gaps;
  nothing filed, because whether it matters is a per-module question.
* **And the 578.** `Fix_ShuttleHubOffAvailable` wraps `BaseBuilding`, but
  `Building.lua:591`/`:598` **re-declare both** `GetWorkNot*Reason` below it
  (`BaseBuilding.lua:326`/`:355`). Everything under `Building` therefore
  dispatches Building's own body, not ours. ⇒ **the largest single coverage gap
  in the pack, and it is a re-declaration, not a dispatch failure.** Whether it
  matters is a per-module question this leg did not open.

### Readings taken rather than assumed

* **`ClassNonInheritableMembers` is UNREADABLE from mod code** — the sweep
  printed `{ UNREADABLE }`. It is a real global (`classes.lua:1-8`) but a mod
  environment cannot see it. The builder's other skip set, `noncopyable`
  (`= { __hierarchy_cache }`), is a file-local: not readable at all.
* **`__hierarchy_cache` is not readable at runtime**, so the probe does not try.
  It is in `noncopyable` (never written onto a built class) and `classdefs` is
  discarded at `classes.lua:1089`. The runtime substitute is the metatable link —
  `getmetatable(child) == parent` ⇒ that link chained — logged as
  `link=chain` / `link=copy` / `?` (no single-parent direct child exists).
* **2 classes carry an `__index` that is not the class itself** —
  `BrazeSession`, `ProtectedPropertyObject`. Instance dispatch there does not
  follow the model the sweep measures. Neither is a pack target.

### ⚠️ Two disclosures about the instrument itself

1. **The verdict test is `D[m] ~= C[m]`, not F106's `rawget(D, m) ~= nil`.** The
   rawget is the right sign but a strict subset: a descendant can hold no own
   copy and still miss the wrap because an intermediate class took the copy.
   Both are logged; the verdict uses the resolution. This is a deliberate
   departure from the brief's sketch and it is the stronger test.
2. **The probe's PASS text mislabelled one number in this very log.** It read
   *"(66 classes total, 1328 holding a build-time copy of their own)"* — the
   1,328 is the **multi-parent** unreached count, not a build-time-copy count.
   The numbers are right; that label was wrong. The `SMRTEST-DISPATCH TOTAL` line
   in the same log is correctly labelled and is **the line to quote**. Repaired
   and disclosed in TestKit `1d240a4`.

## 4 · `F107` — the defect the leg found

```
SMRTEST-F105GUARD LandscapeConstructionSite: unguarded-state call ok=true
SMRTEST-F105GUARD ClearWasteRockConstructionSite: unguarded-state call ok=true
SMRTEST-F105GUARD TerrainPaintConstructionSite: unguarded-state call ok=true
FAIL  LandscapeCostGuard  the guard no longer delegates on … (raised with a valid
  cost table: Mod/SMR_CommunityFixPack/Code/Fix_LandscapeCostRefresh.lua:81:
  attempt to call a nil value (upvalue 'prev')) × 3 leaves
```

The full derivation is on `F107`. In one line: because the pack wraps
**classdefs**, `local prev = C.RefreshConstructionResources` captures nil on a
class that does not itself declare that method — and none of the three leaves
does (`ConstructionSite.lua:665` does).

⭐ **Clause 2 is why this was caught.** Clause 1 alone (the guard returns without
raising) would have passed for a "fix" that returned unconditionally and
refreshed nothing. That clause exists because this chain was launched over two
probes that could not fail.

**Static audit of the pack** — every detected install site against `Src`
declarations: `Fix_LandscapeCostRefresh` is the **only** instance. The other
install sites that lack a matching `Require` entry
(`DroneControl.UpdateRocketsInternal`, `DroneHubExtenderBase.UpdateUplinkRequesters`,
`AlienDigger.GameInit`, `SA_GetLabelToRegister.SAExec`, `Colonist.Idle`,
`MicroGHabitatAutoResolve.IsSuitable`) all wrap a method their own class
declares, so their `prev` is real. ⚠️ **This audit is STATIC** (regex over
install patterns + a declaration grep), not measured; the measured pattern is
`LandscapeCostGuard`.

⭐ **The corollary worth keeping.** All 78 modules printed `applied` on this leg,
so every `{class, method}` the pack **self-checks** resolved non-nil at classdef
time — which means that class declares that method. The residual risk is exactly
the install sites that are *not* self-check sites, and that set is now
enumerated.

## 5 · Predictions, graded

`reports/F106_PREDICTIONS.md`, committed and pushed **before** arming.

| # | prediction | outcome |
|---|---|---|
| 1 | repaired F33 probe **FAILs** on all three leaves | ⛔ **WRONG** — PASS on all three. This is the reversal. |
| 2 | `rawget(leaf, …)` non-nil **and a distinct function** | **HALF RIGHT** — non-nil ✅, but the same function ⛔. The half I got wrong is the whole finding. |
| 3 | 105 targets ✅; ~85 clean, ~20 with hits, ~10,500 desc, ~110 unreached, ~8,000 multi, ~250 multi-unreached, 0 missing | targets **105** ✅, missing **0** ✅; clean **97** (predicted ~85), hits **8** (predicted ~20), desc **13,127** (predicted ~10,500), unreached **66** (predicted ~110), multi **11,080** (predicted ~8,000), multi-unreached **1,328** (predicted ~250). Every count wrong in the same direction as prediction 1, because the model assumed post-build application. |
| 4 | `75 PASS, 1 FAIL, 24 SKIP, 0 ERROR` of 100 | ✅ **EXACT — and misleading.** The counts matched; the FAIL is a **different probe** (`LandscapeCostGuard`, not `SmallLandscapeSites`). A tally can be right for the wrong reason. |
| 5 | fingerprint-diff lines | ✅ all appeared: F33's changed text, 3 F33DISPATCH lines, 2 new PASS/FAIL rows, 108 SMRTEST-DISPATCH lines, 3 F105GUARD lines, `78/78`, 78 `applied`, RNG churn (`TouristApplicants 1-star 171 < 2-star 308`, `FounderTraitNotification` Melancholic) |
| 6 | 78 `applied` | ✅ 78 |

⭐ **The prediction that failed is the one that produced the result.** Prediction
3's model rested on a stated rule — *"a wrap on `C` reaches `D` iff `C`'s
classdef sets `__hierarchy_cache`"* — which is correct **for a post-build wrap**
and irrelevant for a classdef-time one. Writing it down before the run is what
made the reversal legible in one reading instead of arguable.

## 6 · What is NOT settled, and by whom

* **Instantiation.** Which unreached classes ever exist on a map. Not measured,
  not measurable by this probe. **Checklist 74's audit stays half-open on this
  point permanently unless someone measures it directly.**
* **The 578-class `BaseBuilding` gap** and the other re-declaration gaps. Each is
  a per-module coverage question. None is a dispatch failure. Nothing filed —
  routed to `EF-066` and checklist 74.
* **F105's field route.** A levelling site on a real map plus a
  `*_Construction` cost tech (NeoConcrete / DomeStreamlining / MarsNoveau) has
  still never run. `LandscapeCostGuard` drives the mechanism and the guard on a
  synthetic object, nothing more.
* **`tested-attended` anything.** Nobody was at the keyboard. Screen events are
  not claimable at all.
* **A `WORKFLOW.md` rule for the false-green family.** Two independent instances
  now (`8feaf59`'s C50 probe; this chain's F33 probe). Explicitly `02_AUDIT`'s
  decision, not this prompt's.
