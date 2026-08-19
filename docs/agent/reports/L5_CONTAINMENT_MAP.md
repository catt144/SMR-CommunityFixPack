# L5 — the containment map: what catches a throw, and what the player sees

**Link 5 of the pre-launch sweep chain, lens L5 (failure & containment),
2026-08-19.** Instrument `tools/l5_containment.py`; every count below is emitted
by it or measured from the archive, none is inherited. Configuration of every
measured number: **dev tree, unpacked, source-derived at `ModTools\Src`
(1.0.7.396349) + 73 archived retail logs**. ⛔ **No launch was taken** — §7 says
why.

---

## 0 · The question this lens exists to ask, and the one it actually asked

`02_LENS_NOTES.md` L5 asks three questions: does one `apply` throwing spare the
other 74 · is *"fail safe, never loud"* true **in aggregate** · how many modules
could be silently doing nothing. All three are asked **about the pack's own
code**, and the answer to all three turns out to depend on something the pack
does not contain.

> ⭐⭐ **THE QUESTION NOBODY HAD ASKED — and it generalises past L5: WHO OWNS THE
> FAILURE SURFACE?** The pack's whole fail-safe story is told about `apply`
> (`FIX_POLICY` §2: *"apply runs under pcall; an error deactivates only that
> fix"*). That sentence is TRUE and it covers **one of six** entry classes. Ask
> instead *"for each way the engine can enter our code, who is holding the
> pcall?"* and the map inverts: the loudest failure surfaces this pack has are
> **raised by the engine, keyed on our mod's `content_path`, with no call site of
> ours involved at all** (`EF-065`, recorded this session). L4 censused 17 screen
> call sites in `Code/` and correctly concluded the pack mints no surface of its
> own — and a census of our code **cannot see** the two boxes that name us.
>
> ⇒ **Generalisation for any later lens: a component's failure surface is not
> necessarily in the component.** Enumerate the entries, then ask who holds the
> pcall at each one — never ask the component what it does when it fails.

---

## 1 · The six entry classes, and the catcher at each

Re-derived at Src this session by symbol, not inherited.

| # | how the engine enters our code | count | who holds the pcall | on a throw, the player… | the registry… |
|---|---|---|---|---|---|
| **E1** | **file scope** — a code file's top-level statements | **234** statements, 76 files | `pdofile` (`lib.lua:242-251`), i.e. the ENGINE, one pcall per FILE | ⛔ **sees a message box** (`ModsLoadCode`, `Mod.lua:2254-2275`) | ⛔ **the module is ABSENT — not `inactive`** |
| **E2** | `apply` via `Register` | **75** | ours — `run_apply` (`00_Core.lua:388`) | sees nothing | `status="error"`, logged, C1-suspect ✅ |
| **E3** | a `DataPatch` pass | **10** | ours — `00_Core.lua:309` | sees nothing | `status="error"`, logged ✅ |
| **E4** | an `OnDataReady` callback | **3** | ⛔ **nobody** — `00_Core.lua:372` calls `fn()` bare | sees nothing | ⛔ **still `active`**, no log line |
| **E5** | an `OnMsg` handler | **29** module-level (+9 core) | the engine's `procall` (`cthreads.lua:20`) — swallows, reports nothing | sees nothing | ⛔ **still `active`**, no log line |
| **E6** | an installed wrapper / replaced global / thread body | **53** method wraps · **14** `SetGlobal` · **6** game-time + **2** real-time threads · **1** `PeriodicRepeatInfo` slot | the caller's context — **unknown per call site** | ⛔ **may see a message box** (`EF-065`(a)) | unchanged — `active` |

**Read across the bottom two rows: E4, E5 and E6 together are where the fix work
actually lives, and none of them can put a failure into the registry.**

### 1a · What E1's answer means, and it is not the obvious one

The good news is real: **`ModDef:LoadCode` (`Mod.lua:490-520`) calls `pdofile`
once per file**, so a file-scope throw in `Fix_X.lua` costs `Fix_X.lua` and the
other 75 files load normally. The blast radius is one file, by engine design.

⛔ **The bad news is that the surviving state is worse than `inactive`.** The
throwing module's `Register` never ran, so its id is in neither
`SMRFixPack.fixes` nor `SMRFixPack.order`. Therefore:

* `ListFixes()` cannot print it — it walks `order`;
* `UpdateSuspects()` cannot flag it — it walks `order`; the stand-down dialog is
  structurally blind to this failure mode;
* the log carries **no `applied` line and no `inactive` line** for it — only an
  absence, and the pack has never published a "should be 75" number to the log;
* the only positive evidence is the engine's `Errors while loading mod` line and
  the player's message box.

⇒ **The one instrument that would catch it is the TestKit's `75/75` gate, and
the TestKit is OFF in configuration B — the release gate.** Run B's criterion 2
already asks for install witnesses **by name, ⛔ not a total**, which is exactly
the right shape; this is a second, independent reason that wording matters.

### 1b · How much of the pack is exposed at E1 — the census

234 column-0 statements over 76 files:

| kind | n | can it throw? |
|---|---|---|
| `SMRFixPack.Register(` | 75 | via `Register`'s body — see §3 |
| `local …` | 70 | 65 literal/`rawget`/`SMRFixPack.*`; 5 read at source, all safe |
| `local function` | 29 | no — declaration only |
| `function SMRFixPack.X` / `function OnMsg.X` | 26 | no — both receivers are guaranteed |
| `OnMsg.X = …` | 19 | no — RHS is a literal `function` or `SMRFixPack.WhenActive` |
| field/global assignment | 9 | all onto `SMRFixPack.*` or a file-local |
| bare calls | 4 | `CreateRealTimeThread` ×1, `GameVar(…)` ×2, `OnDataReady` ×1 |
| `do` / `if` blocks | 2 | `Fix_ExtenderFlapChurn:71,78` — see below |

⭐ **`Fix_ExtenderFlapChurn` is the pack's only module that installs a class-method
wrapper at file scope, outside apply's pcall** (`:78-104`) — and it is built
exactly as `FIX_POLICY` §5 bullet 2 prescribes: a `do` block probes the target
into `install_error` (`:70-75`), the install is gated `if not install_error`, and
`apply` just `return install_error`. **A missing target degrades to a reason
string; it cannot throw.** ✅ Correct, and it is the donor shape for anything
that ever needs to install outside apply again.

---

## 2 · ⛔ FINDING L5-F1 — `OnDataReady` does not do what its sibling eleven lines above it does

`SMRFixPack.DataPatch` wraps its site's pass in a `pcall` and says why, in a
comment that states this lens's exact concern (`00_Core.lua:305-318`):

> *"the passes now run from a message handler, and `Msg` calls handlers through
> `procall` (`cthreads.lua:20`) — a throw there would be swallowed and the fix
> would keep reporting `active` while having done nothing. That is the **F87
> failure mode** … so own the error the way `run_apply` does."*

`SMRFixPack.OnDataReady`, defined **eleven lines later** for "the sites that
patch preset data WITHOUT the runner's latch/heal contract", calls its callback
bare (`00_Core.lua:369-382`):

```lua
local function fire()
    if classes_built and rawget(_G, "DataLoaded") == true then fn() end   -- :372
end
OnMsg.ClassesBuilt = function() classes_built = true fire() end
OnMsg.DataLoaded   = function() classes_built = true fn() end             -- :380
```

**Same dispatcher, same `procall`, same swallow — no pcall, no status write, no
log line.** A throw in either of its two consumers leaves the module reporting
`active` with `detail = ""` and the log clean.

* **Consumers:** `Fix_FirstAsteroidPrefabs:237`, `Fix_TechDescriptionBuilding`
  (×2). ⚠️ `Fix_TechDescriptionBuilding` is **already recorded as a fix that has
  never changed anything** (`F98`/`EF-039` — the re-used translation id), so the
  live exposure is small; that is luck about *which* modules use it, not a
  property of the runner.
* **Hard tell (`FIX_POLICY` §4):** sibling contradiction — the same author wrote
  it correctly in the same file, for the same reason, against the same engine
  route.
* **Route:** ⛔ **record only** (spec §4). Not launch-blocking: no known input
  makes either consumer throw, and 72 pack-carrying archived logs show neither.

---

## 3 · ⛔ FINDING L5-F2 — `Register` indexes `SMRFixPack_Disabled` without the type guard its two siblings use

`00_Core.lua` adopts three globals another mod (or the console) may already have
written, and keeps whatever it finds if it is truthy:

```lua
SMRFixPack_Disabled = rawget(_G, "SMRFixPack_Disabled") or {}   -- :11
SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}   -- :15
SMRFixPack          = rawget(_G, "SMRFixPack")          or {…}  -- :17
```

Two of the three readers then **type-check before indexing**, and say why:

| site | reads | guard |
|---|---|---|
| `WhenActive` `:187-188` | `SMRFixPack_Disabled` | ✅ `type(disabled) == "table"` |
| `DataPatch.run` `:302-303` | `SMRFixPack_Disabled` | ✅ `type(disabled) == "table"` |
| **`Register` `:446`** | `SMRFixPack_Disabled` | ⛔ **none — `if SMRFixPack_Disabled[id] then`** |
| `OptionEnabled` `:55` | `SMRFixPack_Optional` | ⛔ none (dormant: no `Opt_` module ships here) |
| `:24-25` | `SMRFixPack` | ⛔ none — `SMRFixPack.defs = SMRFixPack.defs or {}` |

**Consequence, and it is the pack's single widest blast radius.** `Register` is
called at every module's file scope, so a non-table truthy `SMRFixPack_Disabled`
throws in **all 75 files at E1** — 75 absent modules and a message box listing
75 errors. A non-table `SMRFixPack` throws at `00_Core.lua:24`, i.e. **before the
logger exists**, taking the whole pack down with 76 errors.

* **Reachable how?** Only by a pre-load write from another mod or the console.
  ⚠️ The README advertises `SMRFixPack_Disabled["<FixId>"] = true` as the veto,
  and the plausible misreading — `SMRFixPack_Disabled = true` for "turn the whole
  thing off" — lands exactly here, taking effect at the next `ReloadLua`, which a
  player reaches by opening and closing the Mod Manager.
* **Route:** ⛔ **record only.** Not launch-blocking (needs a foreign write). ⚠️
  **Overlaps L8** — flagged here so L8 does not spend its budget re-deriving it;
  what L8 still owns is whether a foreign mod would plausibly *pick* these names.

---

## 4 · ⭐ FINDING L5-F3 — three load-time repairs walk player data with no per-item guard, and the pack already contains the fix

Census 5 of the instrument: **14 message handlers iterate a collection.** They
are entered through `Msg`'s `procall`, so a throw inside one is swallowed
entirely — no log line, no status change, entry still `active`. The only defence
available is a **per-item** `pcall`, and **the pack already uses it in two
places**:

```lua
-- Fix_TrainMinors.lua:141  /  Fix_TrackTunnelPowerBridge.lua:164
local ok, after = pcall(recompute_max_vehicles, track)
```

⭐ **That is the benchmark shape for this lens** — the L5 analogue of link 1's
`Fix_DustDevilSpawnGate:250-258` save/restore discipline. One bad object costs
one object. Measured against it:

| handler | iterates | guard | if item *k* throws |
|---|---|---|---|
| `Fix_TrainMinors:133` | every track in every city | ✅ per item | one track lost |
| `Fix_TrackTunnelPowerBridge:157` | every track in every city | ✅ per item | one track lost |
| `Fix_TrackTunnelPowerBridge:151` | one track | ✅ | contained |
| `Fix_DroneTransportMinors:158` | unreachables | ✅ | contained |
| `90_SaveSanitizer:325` | 6 loops | ✅ 4 pcalls | mostly contained |
| `Fix_DisasterPredictionLeak:108,114` | predictions | ⚠️ per **pass** | pass aborts, **but it is logged** |
| `Fix_RainsDeadlock:210` | rains entries | ⚠️ per **pass** | pass aborts, **but it is logged** |
| ⛔ `Fix_SaintBlessing:151` | **every Colonist on every map** | ⛔ **none** | rest of the colony never re-based, **silently** |
| ⛔ `Fix_TrackSalvageWipe:304` | **every `TrackGridElement` on every map** | ⛔ **none** | rest of the orphans never cleared, **silently** |
| ⛔ `Fix_StaleReservations:61` | **every Residence × its `reserved` list** | ⛔ **none** | rest of the residences never released, **silently** |
| `Fix_AstrogeologistExtractors:174` | module-local `owned` (≈2) | none | bounded |
| `Fix_IndependenceTerraforming:171` | one preset's effects | none | bounded |
| `Fix_FirstAsteroidPrefabs:256` | module constant `PREFABS` | none | bounded |

⚖️ **Severity splits, and one half of it is UNMEASURED.** `Fix_SaintBlessing` and
`Fix_TrackSalvageWipe` reach their objects through `AllMapsForEach` →
`map:MapForEach`, and **`MapForEach` is a C export** (`CommonLua/Core/map.lua:1047`
forwards; the body is documented at `LuaExportedDocs/Game/MapQueries.lua:30`).
⛔ **Whether the C loop `procall`s the Lua callback per object is not derivable
from Lua**, so for those two the choice is "one colonist lost" vs "the rest of
the colony lost" and **this session cannot say which**. `Fix_StaleReservations`
uses a plain Lua `for`, so for that one there is no ambiguity: **the remainder of
the sweep is abandoned, certainly, and silently.**

⇒ One console line settles it for all three at once, and it is routed to the
owner batched onto the sitting checklist 44 already owes (§7).

* **Route:** ⛔ **record only.** Not launch-blocking: nothing in 72 pack-carrying
  logs shows any of these three throwing, and each is a *repair* pass — an
  abandoned repair leaves vanilla's own state, not a corrupted one.

---

## 5 · ⛔ FINDING L5-F4 — run B, the release gate, is specified to fail a healthy build

`98_LAUNCH_REHEARSAL.md` §4 lists run B's pass criteria and closes with
**"Any of 1–7 failing blocks the upload."** Criterion 3 read, verbatim:

| 3 | `0 [LUA ERROR]` | log |

**That condition is unsatisfiable on this rig and always has been.** Measured
this session:

| corpus | `[LUA ERROR]` |
|---|---|
| all 73 archived `docs/archive/*.log` | **418 ×** `Lua/Flight.lua:465` + **7 ×** `:479` + 4 one-offs (§6) |
| `vl97a` (08-19, shipping configuration) | **49** = 48 + 1 |
| `vl97b` (08-19) | **60** = 59 + 1 |
| `vl97c` (08-19) | **49** = 48 + 1 |

`01_LINK.md` §6 was corrected on 2026-08-19 for exactly this — *"this rule used
to say 'any `[LUA ERROR]`', which was unrunnable"* — and **the correction was
applied to the link brief and not to the rehearsal, which is the document that
actually runs the gate.**

⭐ **And the interlude's own attribution needs one word changed.**
`reports/97_VERIFICATION_LAUNCH.md` R5 says *"the 48/1 split is identical to the
08-15 baseline leg's … Attribution: vanilla, aged ≥16 days, **count
reproduced**"* — while disclosing `×59 / ×1 in L-B` in the same sentence. **48,
59, 48 across three legs of one configuration on one build is not a reproduced
count**; `Flight:Mark` fires per marked object, so the number tracks session
activity (L-B is also the longest log: 1209 lines vs 1070 / 1074). The
attribution is right; the stated reason is not, and the wrong reason is the one
run B would apply. ⇒ **the stable signature is the SHAPE — exactly two sites,
both `Flight.lua` — never the count.**

* **Route:** ⛔ **FIXED IN THIS COMMIT**, because it is a **record**, not shipped
  behaviour (spec §4, clarified 2026-08-19), and because leaving the release
  gate's own criterion unsatisfiable is not a thing to hand to a later link.
  `98_LAUNCH_REHEARSAL.md:156` now reads *"no NEW / UNATTRIBUTED `[LUA ERROR]`"*
  with the measured baseline, the shape rule, and the `EF-065` escalation.
  ⛔ **Not** launch-blocking — nothing about the pack changed.

---

## 6 · Every `[LUA ERROR]` in the archive, attributed by name — ⛔ none dismissed

`01_LINK.md` §6: *"not caused by our leg" is an attribution verdict you must
show.* All 73 logs, every distinct message:

| message | n | attribution | age |
|---|---|---|---|
| `Lua/Flight.lua:465: attempt to index a boolean value (field 'objects_to_mark')` | 418 | vanilla; `Flight:Mark` reads `self.objects_to_mark` on a `Flight` whose fields are `false`; documented synthetic-map noise | since 2026-08-03 |
| `Lua/Flight.lua:479: … (field 'objects_to_unmark')` | 7 | same function pair, same cause | since 2026-08-03 |
| `Lua/GridObject.lua:77: attempt to call a nil value (method 'GetShapePoints')` | 2 | vanilla; stack shows `[C] global procall / classes.lua(227): field GameInit` — the engine's own `GameInit` dispatch, **MarsDebug build only** | 2026-08-03 |
| `Attempt to create a new global 'IsNearDome'` | 1 | ⚠️ **the TESTKIT's own `set_global`** — stack names `SMR_CommunityFixPackTestKit/Code/00_TestCore.lua(172)` from `50_Probes_Wave5.lua(415)`. Not the fix pack; absent in configuration B | 2026-08-03 |
| `Attempt to create a new global 'AddAreaRubble'` | 1 | same site, same probe | 2026-08-03 |
| `attempt to index a boolean value (upvalue 'old_threads')` | 1 | **vanilla, and a real vanilla defect** — see below | 2026-08-04 |

⭐ **The `old_threads` line is worth keeping, and it is not ours.**
`UpdateRainsThreads` (`Lua/TerraformingDisasters.lua:340`) opens with
`local old_threads = RainsDisasterThreads` (`:376`) and indexes it at `:411`.
`RainsDisasterThreads` is a **`GameVar`** (`:323`), so it is `false` when no game
session is live. The function has **exactly one caller tree-wide** —
`DelayedCall(0, UpdateRainsThreads, …)` at `:488` — and `DelayedCall` runs its
target in a deferred real-time thread (`lib.lua:1811`). The archived instance
fires immediately after a save/load step, with the locals dump showing
`old_threads | boolean false`. ⇒ **vanilla schedules a deferred read of a GameVar
that the session teardown can invalidate first, and never re-checks.**

* **Attribution against our leg, shown not asserted:** the pack's only contact
  with this state is `Fix_RainsDeadlock`, which wraps `RainsDisasterActivation`
  (a different global) and, in `MigrateRainsState:126-134`, **repairs** a
  non-table `RainsDisasterThreads` back to `{}`. No pack site assigns the
  container. The one caller is vanilla's. 1 occurrence in 73 logs, aged 15 days.
* ⚠️ **What I cannot show:** that our leg did not change the *timing* that opened
  the window. One occurrence is not a rate.
* **Route:** a **candidate vanilla defect**, recorded in `SWEEP_FINDINGS.md` with
  this evidence. ⛔ Deliberately **not** filed as a new `bugs/` row mid-chain —
  the terminal audit files with the whole set visible, and a candidate row minted
  now churns the counts `STATE.md` publishes for no benefit before launch.

---

## 7 · ⛔ The launch obligation (spec §6.5) — REFUSED, and exactly why

L5 has accumulated three "needs a running game" items: **(i)** does
`MapForEach`'s C loop `procall` its callback per object (§4) · **(ii)** does an
uncaught throw in one of our wrappers really pop `EF-065`(a)'s box · **(iii)**
what a player sees when a file throws at E1. I am not taking a launch, and the
reason is not cost:

> ⛔ **Every one of the three requires the pack to THROW, and there is no legal
> way for this link to make it throw.** (1) Editing `Code/` to inject a fault is
> barred twice over — spec §4 record-only, and the explicit *"add an instrument to
> `Code/` — it would contaminate the tree under test"*. (2) A TestKit probe is
> barred by the suite-count rule (96 is on the store card). (3) The remaining
> route is one console line, and **an unattended session cannot type into the
> console** — the same wall checklist 44 hit.

⚠️ **And (ii)/(iii) are screen events**, which by standing rule may not be
witnessed unattended at all, so even a legal fault injection would not close them
tonight.

⭐ **What I did instead, which costs the owner nothing extra:** the one console
line that settles (i) for all three affected modules at once is appended to the
sitting **checklist 44 already owes**, alongside a second line that settles
whether `EF-065`(a)'s reporting path is even enabled on this rig. A launch that
re-measured the 08-19 baseline for the fourth time would have produced a number
this report already contains.

---

## 8 · What this lens did NOT reach

* ⛔ **No launch.** Every verdict here is source-derived or measured from
  archived logs; nothing in this report was observed happening.
* ⛔ **The C side of `MapForEach`** — the severity of two of the three §4 findings
  is undetermined until one console line runs.
* ⛔ **Whether `OnMsg.OnLuaError` is raised for a THREAD error.** `cthreads.lua:137-141`
  raises `OnThreadError`; `ReportModLuaError` hangs off `OnLuaError` only. If the
  C engine raises only the former for threads, the pack's 8 own threads are
  *quieter* than its wrappers — an asymmetry with real design consequences, and
  not derivable from Lua.
* ⛔ **`content_path` in the PACKED case.** `EF-065`(a) matches on a substring of
  our content path; whether the packed mount produces the same string is
  untested, so the box may behave differently in configuration B — **the gate**.
* ⛔ **Neither engine box has ever been rendered** by anything in this project, so
  wording, placement, and whether either can stack with the pack's own stand-down
  dialog are unknown.
* ⛔ **The 53 method wrappers were not individually traced to their callers**, so
  "who holds the pcall at E6" is answered structurally (*the caller's context*)
  and not per site. That is a real, mechanical, ~53-row job a re-take owes.
* ⛔ **`FIX_POLICY` §2's veto rule is not met by 4 delegated bodies.**
  `MeteorsWatchdogCheck:121`, `IndependenceTerraformingSweep:127`,
  `StormWedgeCheck:98` each test `status == "active"` but **not**
  `SMRFixPack_Disabled[id]`, and `Fix_CrystalMysteryHang:105` (`OnMsg.MysteryEnd`
  → `stop_repeater`) tests neither. §2 requires **both**. Pre-load vetoes are
  covered (Register latches `status="disabled"`), so the gap is **mid-session
  veto only** — console/foreign-mod territory. ⚠️ `Fix_MeteorFrequency:164-169`
  does both, in the same file as `:157`, which does not: another
  sibling contradiction. Enumerated, not adjudicated further.
* ⛔ **TestKit tree excluded a FIFTH time** (`Code/` only) — and this lens has a
  specific reason to want it, since the TestKit is the one component measured to
  have produced `[LUA ERROR]` lines of its own (§6).
* ⛔ **Runtime cost of failure** — nothing here measures what a swallowed throw
  costs in frame time.
* ⛔ L6 (promise vs behaviour), L7 (environment & namespace), L8 (adversarial) —
  **entire**, except the L8 overlap explicitly flagged in §3.

---

## 9 · The negatives worth inheriting so they are not re-derived

* ✅ **`run_apply`'s containment is real and complete.** `pcall(def.apply)` at
  `00_Core.lua:388`, three exhaustive branches, every one writes a status AND a
  log line. One module's `apply` throwing cannot touch the other 74.
* ✅ **`ModDef:LoadCode` pcalls per FILE**, so E1's blast radius is one file, not
  the mod. (The surviving state is still bad — §1a.)
* ✅ **Zero engine mod-error surfaces have ever fired.** `Error in mod` /
  `Mod-related problem` / `Errors while loading mod`: **0 occurrences in all 73
  archived logs**, 72 of them pack-carrying, including the three 08-19 legs.
* ✅ **Zero pack failures have ever been logged.** `FAILED to apply` /
  `FAILED to patch data`: **0** in the three 08-19 verification legs.
* ✅ **Every `log(...)` call in all 76 files uses a string LITERAL as its format**
  — checked mechanically. `SMRFixPack.Log` does `string.format("[CommunityFixPack] " .. fmt, ...)`,
  so a variable format string carrying a stray `%` would throw inside the
  logger; no site does it. The `%`-escape for ModLog's second format pass is at
  `:35` and is correct.
* ✅ **`Fix_ExtenderFlapChurn` is the donor shape** for a file-scope install
  (§1b). ✅ **`Fix_TrainMinors:141` is the donor shape** for a per-item guard (§4).
