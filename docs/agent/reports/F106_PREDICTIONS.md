# F106 dispatch chain — PREDICTIONS, written before the run

⭐ **This file exists to be falsifiable.** It is committed and pushed **before**
the autorun leg is armed; `git log` timestamps are the proof. A prediction
written after the log exists is worth nothing, so if this commit's timestamp is
later than `docs/archive/f106_*.log`'s own, the falsifiability claim is **void**
and the run must be graded without it.

Authored 2026-08-24 by chain `f106-dispatch` prompt `01_PROBE_opus.md`, after
building the instruments and before arming anything.

**PROBE SWEEP: clean** — `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`
returned zero hits in both repos (WORKFLOW element 7 hard gate).

---

## 0 · What is being run

One unattended autorun leg (`Code/96_AutoRunFlag.lua` appended to the TestKit
`metadata.lua` `code` list): boot → pre-game menu → **new** colony, no UI
touched → `SMRTest.RunAll()` → quit. `EF-056`'s autosave-rotation hazard does
not apply — no save is opened.

Instruments landed for it:

| commit | repo | what |
|---|---|---|
| `e896243` | TestKit | the F33 probe's dispatch repair, disclosed |
| `7478048` | fix pack | `tools/harvest_wrap_targets.py` |
| `4d3b851` | TestKit | `Code/64_Probes_Wave14.lua` — `DispatchReach` + `LandscapeCostGuard`, and the code-list entry |

---

## 1 · The repaired F33 probe, per leaf  *(prediction 1)*

**PREDICTED: FAIL on all three leaves.** `Fix_SmallLandscapeSites` wraps
`LandscapeConstructionSiteBase.GetClosestDests`; nothing in the chain
`ConstructionSite → LandscapeConstructionSiteBase → ClearWasteRockConstructionSite
→ LandscapeConstructionSite` (and the `TerrainPaintConstructionSite` sibling)
sets `__hierarchy_cache`, so each link copies. Expected verdict text names all
three: `LandscapeConstructionSite`, `ClearWasteRockConstructionSite`,
`TerrainPaintConstructionSite`.

Expected raise: `attempt to index a nil value` inside vanilla's
`for i = 1, top_count do top_dests[i] = dests[i].dest end`
(`LandscapeConstructionSiteBase.lua:186-190`) on the two-hex cache.

⚠️ **Clause 0 is predicted to still PASS** — the clamp's arithmetic is correct;
it is only unreachable. If clause 0 fails, the fix itself is broken and that is
a different and larger finding.

## 2 · `rawget(leaf, "GetClosestDests")`  *(prediction 2)*

**PREDICTED: non-nil on all three leaves, and a DISTINCT function from
`LandscapeConstructionSiteBase.GetClosestDests`** (which is our wrapper).
Expected log lines:

```
SMRTEST-F33DISPATCH LandscapeConstructionSite: rawget=own-copy resolved==base=false
SMRTEST-F33DISPATCH ClearWasteRockConstructionSite: rawget=own-copy resolved==base=false
SMRTEST-F33DISPATCH TerrainPaintConstructionSite: rawget=own-copy resolved==base=false
```

⛔ If any line reads `rawget=nil` **and** `resolved==base=true`, F106's mechanism
is **wrong for this hierarchy** and the entry gets rewritten, loudly, not
softened.

## 3 · Sweep totals  *(prediction 3)*

Derived from a static model of `classes.lua:693-729` built against
`ModTools\Src` (parse of 4,005 `DefineClass` declarations + 17 flagged
classdefs), crossed with a heuristic detection of which targets the pack
actually **assigns** to. ⚠️ **INFERRED, and the model has three known blind
spots**, all of which push the real numbers UP, not down:

* classes generated at runtime from `CompositeDef` presets are not in the parse
  (and `Composite.lua:553` sets `__hierarchy_cache` dynamically on one more
  class than the 17 the source literally spells out);
* the wrap-site detector is a regex over aliases and demonstrably misses some
  (e.g. `TunnelBase.RemovePFTunnel`, `UniversalRocketBase.ResolveAutoModeTarget`,
  `FarmBase.ApplyOxygenProductionMod` are all assigned but were not detected);
* DLC and other enabled mods add classes the static parse never sees.

| figure | predicted | note |
|---|---|---|
| targets enumerated | **105** | exact — the probe's table is generated |
| targets clean | **~85** (range 80–90) | model says 88 |
| targets with ≥1 unreached descendant | **~20** (range 15–25) | model says 17; detector under-counts wraps |
| descendants walked (total, summed per target) | **~10,500** (range 9,900–12,000) | model says 9,928 from Src alone |
| UNREACHED (non-multi-parent) | **~110** (range 85–160) | model says 80 copies + 8 overrides |
| MULTI-PARENT (reported separately) | **~8,000** (range 7,800–8,800) | model says 7,871 |
| …of which unreached | **~250** (range 200–400) | model says 211 |
| targets MISSING from the build | **0** | all 78 modules print `applied`, so every Require target resolved at boot |

⚠️ **The stop condition is live here.** The README says "more than ~15 wraps
come back broken → stop, route to the owner". The predicted ~20 will cross it.
⛔ It must not be reported as ~20 broken fixes: the sweep does not measure
instantiation, and several of those targets are shape-checks the pack never
writes to. The re-packaged checklist 74 carries that distinction or it is wrong.

**Per-target predictions worth grading individually:**

| target | predicted |
|---|---|
| `Fix_SmallLandscapeSites LandscapeConstructionSiteBase.GetClosestDests` | link=copy, 3 desc, **3 UNREACHED**, 0 multi |
| `Fix_GhostFarmOxygen Building.SetDome` | link=**chain**, ~574 desc, **0 UNREACHED**, ~477 multi of which **0 unreached** |
| `Fix_UpgradeModifierLeak Building.StopUpgradeModifiers` | link=chain, **0 UNREACHED** |
| `Fix_TrainsToVoid Building.OnDemolish` | link=chain, **~4 UNREACHED** (subclasses that override `OnDemolish`) |
| `Fix_MoraleComfortTooltip PropertyObject.GetProperty` | link=chain, ~3,900 desc, **0 UNREACHED** (the pack never assigns to it) |
| `Fix_DomeFreeSpaceMismatch Dome.RefreshFreeLivingSpaces` | link=copy, ~29 desc, **~29 UNREACHED** |
| `Fix_LanderCargoRatchet UniversalRocketBase.*` | link=copy, 10 desc, **10 UNREACHED** each |
| `Fix_StaleReservations Residence.ReserveResidence` | link=copy, ~25 desc, **0 non-multi UNREACHED, ~25 MULTI all unreached** |
| `Fix_LandscapeCostRefresh ConstructionSite.RefreshConstructionResources` | **0 UNREACHED** — the pack installs per leaf and never writes this table |

⭐ **The rule the model rests on, stated so it can be shot at.** My first pass
got it wrong and the corrected version is: a copy link copies the parent's
**own** table and sets `meta(child) = getmetatable(parent)`, **skipping the
parent**. So once any link chains, the member is no longer in any lower class's
own table and every deeper copy link carries nothing. ⇒ **a post-build wrap on
`C` reaches `D` iff the FIRST link `C → child` chains — i.e. iff `C`'s own
classdef sets `__hierarchy_cache` — and no class on the path re-declares the
method.** Only **`Building`** and **`PropertyObject`** are flagged among the
pack's 46 target classes. If the log contradicts this rule, the rule is wrong
and this file is the record of that.

## 4 · Suite tally and probe count  *(prediction 4)*

Tree is at **100 probes** (`doccheck --emit-counts`, re-emitted after the
commits above; was 98 — **delta +2**).

**PREDICTED: `---- 75 PASS, 1 FAIL, 24 SKIP, 0 ERROR ----`**

Arithmetic from the last comparable readings — 72/0/24/0 of 96 unattended
(`vl97a_*`, `vl97c_*`, 2026-08-19) and 74/0/24/0 of 98 attended (2026-08-20):
74 − 1 (`SmallLandscapeSites` flips PASS→FAIL) + 2 (both new probes PASS) = 75.

SKIP stays 24: the opt-in pack and the save-rescue mod are both OFF on the rig,
and the `[install]` probes SKIP for want of `debug.getinfo` (`EF-010`).

⚠️ **Branch:** if `DispatchReach` reports any target MISSING from the build it
FAILs by design, giving **74 PASS / 2 FAIL**. That would be a Require-shape
drift finding, not a dispatch finding.

## 5 · Fingerprint-diff lines expected  *(prediction 5)*

Pre-declared so the next diff reads as expected rather than alarming (the
precedent is F49's A/B leg):

1. `PASS  SmallLandscapeSites` → **`FAIL  SmallLandscapeSites`** with entirely
   new text. ⛔ This line changes **because the probe changed**, disclosed in
   TestKit `e896243`; it is not a regression in the game or the pack.
2. **New:** 3 × `SMRTEST-F33DISPATCH …` lines.
3. **New:** `PASS  DispatchReach`, `PASS  LandscapeCostGuard`.
4. **New:** ~108 × `SMRTEST-DISPATCH …` lines (2 header + 105 targets + 1 total,
   plus an `__index` line if any class carries an overridden `__index`).
5. **New:** 3 × `SMRTEST-F105GUARD …` lines.
6. `fix pack present: 75/75 fixes active` → **`78/78`**.
7. Three more `[CommunityFixPack] …: applied` lines than the 08-19 legs.
8. Known RNG churn, unchanged in kind: `TouristApplicants` counts and
   `FounderTraitNotification`'s random trait pick.

## 6 · `applied` count  *(prediction 6)*

**PREDICTED: 78** `[mod] [CommunityFixPack] <id>: applied` lines, and
`fix pack present: 78/78 fixes active`.

⛔ Re-emitted, never hand-typed — `python tools/doccheck.py --emit-counts`:

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 78 registered (78 default-active, 0 optional-gated files)
- Code/*.lua files: 79
- TestKit probes: 100
- BUGS index rows: 106 F + 12 D + 53 C
```

⛔ **If the run top disagrees** — a different module count, missing `applied`
lines, the pack gate off — the run is **VOID** and nothing is banked from it
(the `unattended-2` lesson).

---

## 7 · What this leg cannot answer, whatever the log says

* **Which unreached classes are ever instantiated.** Not measured, not
  measurable by this instrument. Checklist 74's audit stays half-open forever
  on this point unless someone measures it directly.
* **The F105 field route.** `LandscapeCostGuard` drives the mechanism and the
  guard on a synthetic object. A levelling site on a real map plus a
  `*_Construction` cost tech has still never run.
* **`tested-attended` anything.** Nobody is at the keyboard; screen events are
  not claimable at all.
