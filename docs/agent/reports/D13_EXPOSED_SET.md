# D13 — the authoritative exposed-set derivation, disposition table and artifact spec

⭐ **THIS FILE IS THE AUTHORITATIVE RECORD.** It supersedes every count and
per-module denominator recorded before 2026-08-13 (§4 reconciles them one by
one, in both directions). Any doc that disagrees with it is wrong, and §4.3
lists the ones that were corrected to match.

**Lineage.** Derived by chain `d13-rescue` prompt 1 (2026-08-12) · re-derived
independently and adversarially by prompt 2 (2026-08-13, verdict **BUILD** with
MUST-FIXes — **membership survived with ZERO differences**; every fix is applied
in place below and tagged `[QA 2026-08-13]`, so a struck line is history, not an
instruction) · **promoted here unchanged by prompt 3 (2026-08-13), which added
§10, the frozen artifact spec, and built to it.** The chain's working copy stays
at `agent/prompts/d13-rescue/90_DERIVATION.md` until prompt 5 deletes that
folder; this is the copy that outlives the chain.

⛔ **The word "complete" belongs to prompt 5's re-derivation, not to this
document** (prompt 1 constraint, unchanged by promotion). ⛔ **Nothing here is
measured in a running game unless a row says MEASURED** — §10 in particular is
design tier throughout.

Derived 2026-08-12 at fix-pack `155869a` / opt-pack `a90d128` / TestKit
`62f03da` (staleness check run; all three clean, all three at the commits this
chain was authored against). Trees read: `C:\Dev\SMR-BugFixPack\Code\` (75 Lua
files) and `C:\Dev\SMR-OptInPack\Code\` (9). The TestKit ships nowhere and is
out of scope by the prompt's own fence.

⛔ **No count was inherited.** The membership below was rebuilt from the shipped
`Code/` of both trees over all five assignment shapes UNION FIX_POLICY §3a's
three capture routes. Where it disagrees with a recorded number, §4 says so and
explains the delta in both directions.

---

## 1. Method, and what the instrument found that hand-reading did not (and vice versa)

### 1.1 The mechanical sweep (all 84 shipped files, both trees)

Five shapes, each swept with its own alias-blind pattern, then every hit read at
source:

| shape | pattern | raw hits |
|---|---|---|
| class-method wrap | `function <X>[:.]<m>(` at any indent (catches the `local D = Drone` alias that defeated three earlier greps — SAVE_SAFETY_REDESIGN §4a) | 112 (both trees, incl. 30 `SMRFixPack.`/`SMROptInPack.`/`OnMsg.` non-targets) |
| table-slot write | `<t>[<k>] =` | 66, of which **2** store a function value |
| global assignment | `SetGlobal(` / `_G[…] =` / `rawset(_G` | **17** distinct replaced globals |
| preset-field write | function-value assignment to a non-local target | **1** (`like.Condition.eval`) |
| own thread | `CreateGameTimeThread` / `CreateRealTimeThread` / `GlobalGameTimeThread` / `MakeThreadPersistable` | **6 GT sites, ~~2~~ 3 RT sites** `[QA 2026-08-13: fix 00_Core:498 + opt 00_Core:498 + Fix_MilestoneCrash:40]` |
| route (c) named state | `SMRFixPack_*` / `SMROptInPack_*` token sweep | ~~**14**~~ **16** distinct persisted names (15 rows; the `F35_<label>` family counted once, D15 counted as two) + 2 non-persisted option tables `[QA 2026-08-13]` |

### 1.2 The instrument

`tools/blocking_analysis.py` was run over a hand-built 80-row target list
covering every method and global either tree assigns (list preserved at
`scratchpad/d13_targets.json`; reproduce with
`python tools/blocking_analysis.py <list>`). Universe: 15,106 names, 633
yielding directly somewhere, 711 blocking on every definition.

**Verdicts: 6 BLOCKS · 10 AMBIGUOUS · 6 `clear?` · 57 clear · 1 NOT FOUND.**

### 1.3 ⭐ The reconciliation — this is the evidence the sweep was real

**What the instrument flagged and hand-reading REFUTED (4 false positives, all
the same defect class — the tool keys on the bare method NAME and aggregates
every class that declares it):**

| instrument verdict | hand verdict | why the instrument was wrong |
|---|---|---|
| `MirrorSphereBuildingBase:StartAction` → **BLOCKS** ("direct yield in all 2 defs") | **no yield in its own frame** | both `WaitWakeup()` calls sit inside the `CreateGameTimeThread(function() … end)` the body creates at `MirrorSphere.lua:836` — textually inside the function, semantically a different frame. `PRIM.search(body)` cannot tell those apart. |
| `RCTransport:InteractWithObject` → **BLOCKS** (via `AssignTrain`) | **no yield**, lines 387-480 read | `AssignTrain` is reached by some *other* class's `InteractWithObject`; RCTransport's own body ends in `commandf(…)`/`OpenResourceSelector` and never yields. |
| `TrackConnectedObjBase:Done` → **BLOCKS** (via `ChangeState`/`DestroyAssignedTrains`/`DestroySilent`) | **no yield** (`TrainTransport.lua:14-35`) | name-level aggregation over ~100 `Done` definitions. |
| `TrackBase:Done` → **BLOCKS** (same three) | **no yield** (`Track.lua:69-76`) | its only yielding-looking callee is `Train:DestroySilent` → `Demolishable:DoDemolish`, whose `Sleep(fx_sleep)` loop is inside `if self.demolishing_countdown > 0`, and `DestroySilent` sets `self.demolishing_countdown = 0` **on the line before the call** (`Train.lua:181-182`). The fixpoint cannot see a guard that makes a callee's yield unreachable. |

⚠️ The last row matters beyond bookkeeping: `Fix_TrackConnectorPingPong` runs
mod code **after** `orig_done(...)` (`:185-188`). Had the instrument been right,
that would be a live layer-2 violation. It is not — but the reason is a
one-line guard three calls down, which is exactly the kind of thing a "BLOCKS"
verdict must never be allowed to settle either way.

**All 10 AMBIGUOUS rows resolved to "no direct yield in the class we patch"**
(`TunnelBase:AddPFTunnel`, `LayoutConstructionController:Activate`,
`SA_GetLabelToRegister:SAExec`, `AlienDigger:GameInit`,
`SolarPanelBase:GameInit`, `Building:OnDemolish`, `sectionDome:Init`,
`sectionMicroGHabitat:Init`, and both `Colonist:Idle` rows — see below).
Likewise all 6 `clear?` rows. One `NOT FOUND` (`UndergroundMarsquake`) is a
`MapGameTimeRepeat` registration, not a named function — the instrument has no
way to see it, which is the original CaveIns blindness restated.

**What hand-reading found that the instrument structurally CANNOT (3 classes):**

1. **`Colonist:Idle` — AMBIGUOUS by name, but the class we patch DOES yield.**
   `Colonist.lua:1770-…` contains `Sleep(1000)` (`:1783`) and `Sleep(2000)`
   (~~`:1795`~~ `:1796` `[QA 2026-08-13: re-read; :1795 is the if-line]`), and it is a **command**, so it runs on a persistable command GT
   thread. The instrument reported "8 of 24 defs yield directly:
   AlienDigger, Metatron, MirrorSphere, PastureAnimal" — Colonist was not
   among the four it named, so a reader trusting the summary line would have
   cleared both `Fix_ArrivalDeaths` and `Fix_ShelterReflex`. **Two exposed
   sites recovered by hand.**
2. **The function-VALUE route (b) is invisible to a blocking analyser.**
   `Fix_CaveInsNoDisasters`' `info[FUNC] = function…` and
   `Fix_LastTransmissionStorage`' `like.Condition.eval = function…` are not
   "blocking" anything; they are reachability facts. §2 rows E8 and E11.
3. **The 17-global closure test (§1.4) is a value-flow question**, not a
   yield question.

### 1.4 ⭐ The global-replacement question, closed exhaustively

17 vanilla globals are replaced across the two trees. A replaced global can
enter a save by exactly two routes, and both were tested against `Src`:

* **Registered persistence.** `OnMsg.PersistSave` writes `rawget(_G, k)` for
  every truthy key of `PersistableGlobals` (`CommonLua/Core/persist.lua:117-134`).
  **None of the 17 names appears in `PersistableGlobals` anywhere in `Src`** —
  checked name by name. Route closed for all 17.
* **Held as a value by a captured frame.** Grepped `Src` for every use of each
  of the 17 names that is *not* a call. **Exactly one hit in the entire
  source tree:**
  `CreateGameTimeThread(RainsDisasterActivation, settings)`
  (`Lua/TerraformingDisasters.lua:313`). (The only other non-call hit,
  `ExpandTrackFromElement` at `TrackElement.lua:536`, is inside a comment.)

⇒ **Sixteen of the seventeen global replacements can never enter a savegame.**
The seventeenth is site E1, and it is exposed for a precise reason: vanilla's
rains loop passes the *function value* to a thread constructor, so our wrapper
becomes that thread's entry body. This is the one derivation result I would most
like prompt 2 to attack, because it turns a whole shape from "assumed exposed"
into "proven not exposed, except here".

---

## 2. The exposed set — 27 sites

Rule 6a's definition: *every site where anything of ours can enter a savegame*.
That is deliberately broader than the historical list, which counted capturable
**code** only; §4 reconciles the two. Provenance is per row (R3): **MEASURED**
= read back off a real save; **SOURCE** = derived from shipped Lua read at the
cited lines; **INFERRED** = argued from engine semantics not observed here.

### 2a. Capturable CODE — 12 sites

| # | repo/module | file:line | shape / route | what persists | orphan question (dies / expires / runs on — would anyone notice) | §3a gate? | repaired by Tier 1/2? | prov |
|---|---|---|---|---|---|---|---|---|
| E1 | FP `Fix_RainsDeadlock` | `:102-113` | global assignment → **(a)** | `activation_wrapper` as the entry body of the `activation_thread` (vanilla passes the value, `TerraformingDisasters.lua:313`) | **dies harmlessly** — layer-2 shaped: `return orig(settings)`, nothing after; and `orig` in an orphan is vanilla's own | n/a (layer 2) | ✅ Tier 1 rewrite `0efb87e`-era — the `fixed_loop` body copy is gone | SOURCE |
| E2 | FP `Fix_BombardmentSpread` | `:90-192` | global assignment (`WaitBombard`) → **(a)** | the whole replacement body; yields at `:173` `Sleep`, `:185` `WaitMsg` | **runs on and completes correctly** — body + upvalues (`GenerateDir`, `travel_dist`) are all-vanilla; the volley finishes and `BombardEnd` posts (adjudication §3.2 as corrected by §8.1). Nobody notices, and that is the *good* outcome | none (never needed one) | no — accepted, D3 "keep the fix" | SOURCE |
| E3 | FP `Fix_BombardmentSpread` | `:137-172` | own GT thread (per missile) → **(a)** | the per-missile closure; yields at `:141`, `:163` | **runs on and completes** — upvalues `missile`/`travel_time`/`dir`/`dome*`/`map`, all vanilla | none | no | SOURCE |
| E4 | FP `Fix_MeteorStormWedge` | `:134` → `:142-198` | own GT thread → **(a)** | `SMRFixPack.StormWedgeHeal` frame; `Sleep(4000)` ×≤10 (`:155`) | **dies cleanly at the gate**, vanilla state reset first | ✅ **yes** — `:145` and re-armed `:156` | Tier-1 §6.2a-D reorder landed | SOURCE |
| E5 | FP `Fix_CrystalMysteryHang` | `:44-54` | own GT thread → **(a)** | the repeater closure **plus, by value, the module-local function `crystals_mystery_active`** (upvalue) | ⛔ **runs on** — every name it touches is vanilla or an upvalue; it keeps posting `Msg("CrystalFlyAway")` hourly until its **frozen 10-sol deadline**. Bounded, silent, and arguably still doing its job | ⛔ **NONE** | no | SOURCE |
| E6 | FP `Fix_ExtenderFlapChurn` | `:77-84` | own GT thread → **(a)** | the debounce closure; upvalues `pending`, `DEBOUNCE` | ⛔ **runs on once** — `Sleep(DEBOUNCE)` then one all-vanilla hub rebuild, then ends | ⛔ **NONE** | no | SOURCE |
| E7 | FP `Fix_TrackConnectorPingPong` | `:156-160` | own GT thread → **(a)** | the reclaim closure. ⚠️ **The body contains no yield**, so this rests on a created-but-not-yet-run GT thread being persisted (creation defers, `EF-029`) | ⛔ **runs on once** if captured — all-vanilla body | ⛔ **NONE** | no | ⚠️ **INFERRED** — see §6 doubt 1 `[QA 2026-08-13: held, and DEFANGED — see the doubt]` |
| E8 | FP `Fix_CaveInsNoDisasters` | `:35-43` | **table-slot** → **(b)** + (a) | our FUNC-slot wrapper, held in the engine's live `info` local across the yielding vanilla `UndergroundMarsquake` FUNC. ~1 in 9 Underground-map saves | **dies harmlessly** — layer-2 shaped tail call | n/a (layer 2) | no — "compliant, no work" | SOURCE (adjudication §3.1, route re-read) |
| E9 | FP `Fix_ArrivalDeaths` | `:171-…` | class-method wrap → **(a)** | the `Colonist:Idle` wrapper frame, below `Sleep(1000)`/`Sleep(2000)` on a command GT thread | **dies harmlessly** — work before, `return orig_idle(...)` after | n/a (layer 2) | ✅ Tier 2 (half b is layer-3'd; the Idle hook is layer-2 compliant) | SOURCE `[QA 2026-08-13: likely OVER-included — both wrappers end in a strict tail call with yield-free pre-work, and a proper tail call elides the frame before vanilla's Sleep. Kept: the historical counts used the same basis, and either reading changes no disposition. Unmeasured; do not cite as capture-proven]` |
| E10 | FP `Fix_ShelterReflex` | `:58-74` | class-method wrap → **(a)** | same frame, second wrapper | **dies harmlessly** — layer 2 | n/a | no — "already compliant" | SOURCE `[QA 2026-08-13: same tail-call observation as E9]` |
| E11 | FP `Fix_LastTransmissionStorage` | `:134-136` | **preset-field** → **(c)** | the `Condition.eval` closure (upvalues: a comparator, a grid-type string, a number), reached via `g_FactionsHolder` **GameVar** (`Factions.lua:196`) → `factions_approval[id].likes_data[i].like` = the preset **sub-object** (`ClassDef-Factions.generated.lua:180`; permanents gather preset **roots** only) | **inert** — nothing ever calls `.eval` on the persisted copy; fresh evaluations go through live presets. Even if invoked: vanilla names only, zero errors | n/a | no — disclosed-no-build (§4.4) | SOURCE (route re-derived from Src this session, not inherited) |
| E12 | FP `Fix_MoraleComfortTooltip` | `:101-110` | instance-field → **(c)**, *bounded* | a `GetProperty` closure `rawset` onto a **Colonist instance**, restored 9 lines later | **cannot be captured** so long as the window stays synchronous: `pcall(shipped, w)` is the only thing between set and restore, and Lua here is cooperative — no save can interleave without a yield | n/a | no | SOURCE — ⚠️ conditional, see §6 doubt 2 |

### 2b. Persisted NAMED DATA — 15 sites (no function values)

| # | repo/module | file:line | name | carrier | value | after uninstall | prov |
|---|---|---|---|---|---|---|---|
| D1 | FP `Fix_MeteorFrequency` | `:76`, `:184` | `SMRFixPack_MeteorLatch` | **GameVar** | version string / `false` | inert data — `[QA 2026-08-13: and SELF-CLEARING: PersistLoad restores only names still in `PersistableGlobals` and PersistSave writes only registered names (`persist.lua:119-143`), so a load without the registering mod drops the value and the next save omits it]` | **MEASURED** (`= 1.0.1`, `spd2`/`spe` dumps) |
| D2 | FP `Fix_FirstAsteroidPrefabs` | `:104`,`:115` | `SMRFixPack_FirstAsteroidPrefabs` | **GameVar** | boolean | inert data — `[QA 2026-08-13: SELF-CLEARING, same mechanism as D1 — and therefore UNREACHABLE by a cleaner: the value never survives the load into a cleaner-equipped session unless the cleaner re-registers the name, which would re-persist it]` | **MEASURED** (`= false`) |
| D3 | FP `Fix_RainsDeadlock` | `:196` | `SMRFixPack_loop_version` | field inside a `RainsDisasterThreads` GameVar entry | version string | inert data | SOURCE |
| D4 | FP `Fix_RainsDeadlock` | `:197` | `SMRFixPack_fixed_loop` (**legacy**) | same | boolean | inert; **the pack clears it as entries migrate** | SOURCE |
| D5 | FP `Fix_StaleReservations` | `:52`, `:83` | `SMRFixPack_reserved_at` | Colonist instance field | GameTime number | inert data | **MEASURED — 1257 / 1260 / 1336 objects** |
| D6 | FP `Fix_ShelterReflex` | `:65`,`:69` | `SMRFixPack_shelter_try` | Colonist instance field | GameTime number | inert data | **MEASURED — 0–1 objects** |
| D7 | FP `Fix_PayloadTemplateRefill` | `:76`,`:97` | `SMRFixPack_payload_set` | transporter instance field | boolean | inert data | **MEASURED — 3 objects** |
| D8 | FP `Fix_DroneTransportMinors` | `:203-204` | `SMRFixPack_rocket_fuel_key` (**legacy**) | DroneControl instance field | any | **the module deletes it from existing saves** | **MEASURED — 0 objects** (the deletion works) |
| D9 | FP `Fix_DustDevilSpawnGate` | `:151`,~~`:173`~~`:201` (write), `:209` (guard) `[QA 2026-08-13: cite corrected]` | `SMRFixPack_spawn_gate` | field on a plain-data descriptor copy held in vanilla's scheduler-thread local | boolean | self-replaces with vanilla data **within one wave** | **MEASURED** (PT-61 P9/P10) |
| D10 | FP `90_SaveSanitizer` | `:84-89` | `SMRFixPack_F35_<label>` | LabelModifier ids in `colony.label_modifiers` | `{amount, percent, prop, id}` | ⭐ **THE RESIDUE IS THE REPAIR** | SOURCE — ⚠️ **not sampled**, see §6 doubt 3 |
| D11 | FP `90_SaveSanitizer` | `:226`,`:339` | `SMRFixPack_F48_StationConnectors` | `UIColony` field | boolean | inert one-shot latch | **MEASURED** (`= true`) |
| D12 | OP `Opt_AcknowledgedWarnings` | `:68`,`:105` | `SMRFixPack_ack_notworking` | Building instance field | boolean | inert (nothing reads it) | **MEASURED — 4 objects, byte-identical across a save round trip** |
| D13 | OP `Opt_ResidencyControl` | `:60`,`:67` | `SMRFixPack_closed_to_new_residents` | Dome/Habitat field | boolean | inert | **MEASURED — 11 objects, byte-identical round trip** |
| D14 | OP `Opt_NoHomeless` | `:53`,`:205` | `SMRFixPack_no_homeless` | Dome/Habitat field | boolean | inert | **MEASURED — 11 objects, byte-identical round trip** |
| D15 | OP `Opt_DroneStatDials` | `:64-65`, `:128`,`:133` | `SMRFixPack_DroneSpeedDial`, `SMRFixPack_DroneCarryDial` | **vanilla `Modifier` objects** in `UIColony.label_modifiers` under our string ids | live modifier tables | ⛔⛔ **THE BOOST SURVIVES UNINSTALL PERMANENTLY** — the module's own header says so | **MEASURED** (both ids, as tables, on multiple containers) |

⭐ **D15 is the only genuinely HARMFUL residue in either pack** — three-tier
ethos level 3, accepted only *paired with its remedy*, and that remedy is this
chain's artifact. It is also the one item that makes the artifact worth
building rather than nice to have. (The module's disclosed workaround — "set
both dials to base, or load once with the mod, before uninstalling" — is
exactly the advice a player who has *already* uninstalled cannot take.)

### 2c. Swept and NOT exposed — the negative half, stated so it can be attacked

* **16 of 17 replaced globals** (§1.4) — proven, not assumed.
* **Every class-table method wrapper whose target does not yield** — class
  tables are permanents (§5.1); the frame is the only route, and it needs a
  yield. `Fix_MirrorSphereSite`, `Fix_RocketInteractGuard`,
  `Fix_TrackConnectorPingPong:Done`, `Fix_TrackTunnelPowerBridge:Done`,
  `Fix_TrainCargoDumping`, `Fix_DroneUnreachableForever`, `Fix_TrainWaitTime`,
  `Opt_DroneOverhaul` (both hooks) and the rest all read clear at source.
* **`Fix_GraphConsumedCaption:66`** — `panel.caption = function…` looks like a
  route-(c) write, and is not: `City:GetColonyStatsButtons`
  (`ColonyControlCenter.lua:8`) builds a **fresh table literal on every call**
  and caches nothing; vanilla puts its own closures in the same slots.
* **`Fix_MoraleComfortTooltip:82`** (`win.GetRolloverText`) and the opt pack's
  `OnContextUpdate`/`OnActivate` writes — **UI windows are not persisted**.
* **`Fix_CommandCenterNumbers:41`** (`RO[name] = function…`) and
  **`Fix_StorageRateModifiers:54`** (`class.OnModifiableValueChanged = …`) —
  writes onto **class tables**, which are permanents.
* ~~**Both**~~ **All three real-time threads** (`00_Core:498` in each pack,
  `Fix_MilestoneCrash:40`) `[QA 2026-08-13: count corrected]` — real-time
  threads are persisted only when flagged `threadPersist`
  (`persist.lua:128-131`); none of ours is flagged (`MakeThreadPersistable`
  appears nowhere in either tree) and none is referenced from persisted data.
* **`SMRFixPack_Disabled` / `SMRFixPack_Optional` / `SMROptInPack_*`** — plain
  mod-created globals, absent from `PersistableGlobals`; they are a
  console/other-mod veto surface, **not** save state. They are not on the
  cleaner's list and must not be.
* **Writes of vanilla-valued data into vanilla persisted globals**
  (`g_MeteorStorm*`, `MilestoneCompleted`, `MilestoneEnactors`,
  `RainsDisasterThreads` structure, `g_RainDisaster`,
  `g_TransportationModeToCommunityCache`, `UIColony.mystery.lighttrap_mode`) —
  the values are indistinguishable from vanilla's own and carry nothing of
  ours. **The cleaner must not touch these**; they are not residue.
* **The whole opt pack has no game-time thread and no GameVar.** Its entire
  save footprint is D12-D15.

---

## 3. ⛔ Rule 6f — three sites ROUTED, not dispositioned

Constitution 6f: a newly derived site with an apparently reachable in-pack
repair and no existing repair **may not** be handed to the cleaner in advance.
E5, E6 and E7 are one family and get one routing.

**The finding.** FIX_POLICY §3a's orphan gate is written as a universal:
*"Every mod-owned thread body opens each wake with an explicit orphan gate —
`if not SMRFixPack then return end` — and resets any vanilla state it set
BEFORE its first mod-created-name touch. Long loops re-check the gate after
every yield."* Four modules own a game-time thread body. **One complies**
(`Fix_MeteorStormWedge`, gated at `:145` and re-armed at `:156` by the Tier-1
§6.2a-D reorder). **Three do not**, and all three are all-vanilla bodies —
which under the corrected orphan-reach rule (`EF-023`) is precisely the case
that *keeps executing* after uninstall rather than dying:

| site | what an orphan does today | one-line repair |
|---|---|---|
| E5 `Fix_CrystalMysteryHang:44-54` | hourly `Msg("CrystalFlyAway")` for up to **10 sols** of a save the pack no longer occupies | gate after the `Sleep` at `:47` |
| E6 `Fix_ExtenderFlapChurn:77-84` | one full hub disconnect/reconnect cycle | gate after the `Sleep` at `:78` |
| E7 `Fix_TrackConnectorPingPong:156-160` | one connector-element rebuild (if a deferred, never-run thread is captured at all — §6 doubt 1) | gate as the body's first statement |

**Harm today: low but not nil.** None of the three can error, none loops
forever, and E5's behaviour is arguably the fix still working. But all three
are *undisclosed* — they appear in no residual list, no header states them, and
"the pack's one mod-owned GT thread in Tier-1 scope" (`Fix_MeteorStormWedge`
header, `:65`) reads as a completeness claim that these three falsify.

**Cost of the in-pack repair:** three one-line insertions, no behaviour change
on the installed path (reading a nil global is safe; the gate is false only
when the mod is gone), no new persisted state, no playtest beyond a parse sweep
and the existing baseline. Estimated one short build prompt.

**Recommendation: BUILD IT IN-PACK, as an inserted prompt between prompt 2 and
prompt 3.** `[AUDIT 2026-08-13: DONE — the owner took the recommendation
(checklist 19) and prompt 2b built all three gates plus the fourth
(comment-only) item in commit 91fc5d0; the terminal audit re-read all three
gate lines and the corrected Fix_MeteorStormWedge comment in shipped source,
and EF-023's "nothing in Code/ states it any more" was re-trued the same day.
§7's three rows now read repaired-in-pack.]` The alternative — dispositioning three orphan bodies to a cleaner
that by construction cannot reach them (a cleaner runs on load; these bodies
run *from* the save the moment it loads) — is the "cleaner as scoping escape
hatch" that FIX_POLICY §3a bars in the owner's own words.

**Fourth item, routed with them (comment-only, no behaviour):**
`Fix_MeteorStormWedge.lua:138-141` still carries the **disproven** persistence
model — *"A global function (persist-safe by name) … the thread it runs on is a
mod game-time thread and is not persisted"* — which contradicts its own
rewritten header 80 lines above (`:53-66`, "a save made during the pulse window
persists this thread"). Adjudication §3.4 named this file as the third one
needing re-commenting in the Tier-1 build; the header was rewritten and this
inline comment was not. ⚠️ **`EF-023`'s closing line — "nothing in `Code/`
states it any more" — is therefore FALSE and must be corrected**, along with
the fact's "two shipped file headers" count.

---

## 4. Reconciliation against every historical number, both directions

**Recorded lineage:** 12 (2026-07-31) → 13 (same day) → back to 12 (§5.2, two
membership changes) → "at least 13 / ≥13" (adjudication, CaveIns added) → "the
13 and one additional inert route-(c) site" (FIX_POLICY §3a:303-308, Phase-1
five-shape re-derivation). Every one is an **open lower bound over capturable
code in the fix pack only**.

**Derived here: 27 sites over both trees — 12 capturable-code + 15 persisted-data.**
The numbers are not comparable as stated, and that is itself a finding: the
historical count answers *"how many modules can put code in a save"*, while
D13's release gate asks *"every site where anything of ours can enter a
savegame"*. The like-for-like comparison is **12 code sites (both trees) vs the
recorded 13+1 (fix pack only)**.

### 4.1 Like-for-like: the recorded 13+1 vs this derivation's 12

| recorded member | here | why |
|---|---|---|
| `Fix_MeteorFrequency` | ⬇️ **REMOVED** | ✅ **Tier 1 repaired it.** Layer 3: no mod-owned thread body exists any more; the wrapper is synchronous and `GetDisasterWarningTime` is not in `PersistableGlobals` and is never held as a value (§1.4). Residue is now D1, a GameVar. |
| `Fix_RainsDeadlock` | ✅ **KEPT (E1)**, but for a **different reason** | Tier 1 deleted the `fixed_loop` body copy. It stays exposed only because vanilla passes `RainsDisasterActivation` *by value* to a thread constructor — the sole surviving instance of that route in the whole of `Src`. Layer-2 inert now, where before it was a forever-orphan. |
| `Fix_DroneUnreachableForever` | ⬇️ **REMOVED** | ✅ **Tier 2 repaired it.** The module no longer replaces `Drone:ApproachWrapper`; it patches the consumer `Drone:CleanUnreachables`, which is synchronous (`Drone.lua:879-896`). |
| `Fix_TrainWaitTime` | ⬇️ **REMOVED** | ✅ **Tier 2 repaired it.** Now a wrapper on `TransportStatistics:AddSpentTime` (synchronous); the `BoardVehicle` body replacement is gone. |
| `Fix_ArrivalDeaths` | ✅ **KEPT (E9)** | half (b) went layer-3, but the module still wraps `Colonist:Idle`, which yields. Layer-2 compliant, so inert — but still capturable, and the historical list counted compliant sites (it counted `ShelterReflex`). |
| `Opt_DroneOverhaul` | ⬇️ **REMOVED** | ✅ **Tier 2 repaired it** — and it now lives in the other repo. The `Drone:Idle` post-call work moved to `Drone:CleanUnreachables` / `TaskRequestHub:FindTask`, both synchronous. |
| `Fix_BombardmentSpread` | ✅ **KEPT — and SPLIT into E2 + E3** | the `WaitBombard` replacement and the per-missile closure are two independently capturable bodies with different lifetimes. The record counted one. |
| `Fix_MeteorStormWedge` | ✅ **KEPT (E4)** | unchanged in kind; now orphan-gated. |
| `Fix_CrystalMysteryHang` | ✅ **KEPT (E5)** | unchanged — **and §3 finds it ungated.** |
| `Fix_ExtenderFlapChurn` | ✅ **KEPT (E6)** | unchanged — **and ungated.** |
| `Fix_TrackConnectorPingPong` | ✅ **KEPT (E7)** | unchanged — **ungated**, and its route is the derivation's weakest (§6). |
| `Fix_ShelterReflex` | ✅ **KEPT (E10)** | unchanged, compliant. |
| `Fix_CaveInsNoDisasters` | ✅ **KEPT (E8)** | unchanged, compliant. |
| `Fix_LastTransmissionStorage` (the "+1") | ✅ **KEPT (E11)** | route re-derived from `Src` this session rather than inherited. |
| ~~`Fix_TrainCargoDumping`~~ | already off | correctly removed by §5.2 — `Train:UnloadAll` is synchronous; re-confirmed clear. |

~~**Removed: 5** (…) 14 − 5 + 1 = **10**… and the derived code count is 12. The
two extra are **E12** (…) and the E9/E10 pair being counted as **two sites on
one method** rather than two modules.~~
`[QA 2026-08-13: the summary arithmetic contradicted its own table (4 ⬇️ rows,
not 5) and double-counted the split. Superseded:]` **Removed: 4**
(MeteorFrequency, DroneUnreachableForever, TrainWaitTime, DroneOverhaul — all
Tier 1/2 repairs). 14 − 4 = **10** kept from the record (E9/E10 were already
two members there: ArrivalDeaths and ShelterReflex). **Added: 2** — **E3** (the
Bombardment per-missile closure; the record counted the module once) and
**E12** (the MoraleComfortTooltip instance-closure window, never keyed at all).
10 + 2 = **12**. The additions are definitional and stated rather than
smoothed.

### 4.2 The direction the old greps were blind in

Nothing in the 15 persisted-DATA sites (§2b) was ever on an "exposed set" list,
because the historical enumeration key — `function C:m(`, then the five
assignment shapes — is a key for *code*, not for *state*. The FixtureCarry
dumps measured the state independently and were never reconciled against the
count. §2b is that reconciliation, and it is where the artifact's actual work
lives.

### 4.3 Docs that state a count and must be corrected (prompt 3)

The D13 entry's table is 2026-08-01-era with pre-restructure paths. Re-swept,
translated, and re-verified live this session
`[QA 2026-08-13: independently re-swept (stale-count patterns over docs/ of all
three repos + loose numeric sweep of the three files my patterns missed): all 9
files confirmed, NO unlisted file found; TestKit and opt-pack docs clean;
archive + chain-internal hits correctly excluded]`:

| file (current path) | what is there |
|---|---|
| `agent/bugs/F86.md` index row + entry | "13", "at least 13", "12 exposed", "five of the twelve" |
| `agent/bugs/D13.md` | the whole "known locations" table (pre-restructure paths) + "at least 13" |
| `agent/STATE.md` | any surviving "≥13" / "12 in total" |
| `agent/FIX_POLICY.md:303-308` | "**13** after two same-day membership corrections … the 13 and one additional inert route-(c) site" |
| `agent/facts/EF-023.md:68-76` | "**13** after two same-day membership corrections"; **and the false "nothing in `Code/` states it any more"** (§3) |
| `agent/reports/SAVE_SAFETY_REDESIGN.md` §3 heading, §5.2, §5.3, §3:188 | "12 exposed", "at least 13", "5 of the 12" |
| `agent/reports/F86_ADJUDICATION.md:290, :543` | "at least 13 by its own definition", "≥13 with CaveIns compliant" |
| `agent/reports/F86_DISCOVERY_POSITION.md` §4 | "The exposure list (12 modules)" |
| `agent/reports/F86_SESSION_FINDINGS.md:201` | "Exposed set — 5 of 12 have a route out" |

⛔ **Archive files are append-only and are NOT corrected** — they record what
was believed when written.

---

## 5. The curated KEEP / REMOVE lists (constitution 6b/6c)

Detection is **by this list only** — never by `SMRFixPack_*` pattern match. The
2026-07-31 `rawget` sweep false-positived on 192 buildings twice; and a pattern
sweep would delete D10, which is the repair.

### KEEP — removing it breaks something

| name / site | why kept | what breaks if removed |
|---|---|---|
| **`SMRFixPack_F35_<label>`** (D10) | ⭐⭐ **the residue IS the repair.** These LabelModifiers are the Frictionless Composites buff the shipped `WindTurbine_Large_ReapplyModifiers` fixup never re-applied | the Large Wind Turbine buff vanishes from the save — F35 returns, permanently, and the pack is no longer installed to redo it |
| **`SMRFixPack_F48_StationConnectors`** (D11) | inert one-shot latch, but removing it is a *silent* invitation to re-run a track re-ordering pass on a save that has already had one | nothing immediately; but the guarantee "this save was re-ordered exactly once" is lost |
| **`SMRFixPack_MeteorLatch`** (D1) | same shape: the latch records that this save lineage was healed under a given pack version. `[QA 2026-08-13: KEEP is also the only executable call — a mod-registered GameVar is dropped on any load without its registering mod (persist.lua:136-142), so the cleaner never sees it; it self-clears on the first modless save cycle regardless]` | a reinstalling player pays one extra meteor-timer re-roll. Harmless, but it is data the pack authored *about* the save, and deleting it makes the pack lie to itself later |
| every **captured frame** in §2a | not removable by a cleaner at all — see §6 doubt 4 | n/a |

### REMOVE — safe, and here is why

| name / site | why safe to remove | what reads it | a save that never had it |
|---|---|---|---|
| **`SMRFixPack_DroneSpeedDial`** (D15) | ⭐ **the headline target.** A vanilla `Modifier` under our string id; `SetLabelModifier(label, id, nil)` is the vanilla removal path the module itself uses at base position | only `Opt_DroneStatDials`, which is gone | is exactly vanilla — this *restores* vanilla drone speed |
| **`SMRFixPack_DroneCarryDial`** (D15) | same | same | same |
| **`SMRFixPack_reserved_at`** (D5) | a timestamp read only by `Fix_StaleReservations`' daily sweep; the module itself treats absence as "start the clock now" | only that sweep | vanilla reservation behaviour, unchanged |
| **`SMRFixPack_shelter_try`** (D6) | a rate-limit timestamp read only by the `Colonist:Idle` shelter branch | only that branch | vanilla |
| **`SMRFixPack_payload_set`** (D7) | a boolean read only by `Fix_PayloadTemplateRefill:97`; absence is the pre-fix state the module already tolerates | only that module | vanilla |
| **`SMRFixPack_rocket_fuel_key`** (D8) | **already legacy** — the current module deletes it (`:203-204`). The cleaner needs it only for saves that never loaded under the current build | nothing, in any shipped build | vanilla |
| **`SMRFixPack_loop_version`** (D3) | a version stamp inside a `RainsDisasterThreads` entry; vanilla ignores unknown fields on reuse | only `MigrateRainsState` | vanilla |
| **`SMRFixPack_fixed_loop`** (D4) | **legacy**, cleared by the current migration | nothing | vanilla |
| **`SMRFixPack_ack_notworking`** (D12) | boolean stamp; the module's own header states stale stamps are inert | only `Opt_AcknowledgedWarnings` | vanilla warning behaviour |
| **`SMRFixPack_closed_to_new_residents`** (D13) | boolean; nil means vanilla by the module's own contract | only `Opt_ResidencyControl` | vanilla |
| **`SMRFixPack_no_homeless`** (D14) | boolean; nil means vanilla | only `Opt_NoHomeless` | vanilla |
| **`SMRFixPack_spawn_gate`** (D9) | ⚠️ **listed, but the cleaner should NOT hunt it** — it lives in a scheduler-thread local, self-replaces within one wave (PT-61-measured), and reaching it means touching a vanilla thread's locals | nothing after one wave | vanilla |
| ~~**`SMRFixPack_FirstAsteroidPrefabs`** (D2)~~ | ~~⚠️ **judgement call — see below**~~ | | |

~~⚠️ **The one list placement I am least sure of is D2.** … I have put it on
REMOVE because the cleaner's population is *already-removed* players; prompt 2
should second-guess it.~~

`[QA 2026-08-13: D2's REMOVE row is struck — the judgement call DISSOLVES ON
MECHANISM. D2 is a mod-registered GameVar: `OnMsg.PersistLoad` restores only
names still present in `PersistableGlobals` and `OnMsg.PersistSave` writes only
registered names (persist.lua:119-143, verified at source this session). A
cleaner that does not register the name can neither see nor remove the value —
and registering it in order to remove it would persist the name as the
artifact's own residue, violating 6d. The value self-clears on the player's
first save/load cycle without the pack. Disposition: NO ACTION — self-clearing,
unreachable by construction. The reinstall/double-grant corner the row worried
about is thereby untouched by the artifact either way, and remains the narrow,
low-harm corner the module's own flag ordering (:174-206) already bounds.]`

**Nothing is on neither list.** Every one of the ~~14~~ **16** persisted names
(15 rows, F35 family as one, D15 as two `[QA 2026-08-13]`) and every one of the
12 capturable bodies has a row above or in §2a — D2's row is the NO-ACTION
entry above, not an absence.

⛔ **Never rename, never rewrite** — persisted names are save contract in both
packs (opt pack `PROVENANCE.md` §2). The five opt-side names keep the legacy
`SMRFixPack_` prefix deliberately; the cleaner honours that and must not
"tidy" them to `SMROptInPack_`.

---

## 6. Where I am uncertain — attack these first

1. ⚠️ **E7, and the general question behind it: is a created-but-never-run
   game-time thread captured by a save?** Creation defers (`EF-029`), the body
   has no yield, and the persist machinery for threads is C-side
   (`threadPersist` flag, `cthreads.lua:224`) — I could not settle it from Lua
   source. If the answer is "no", E7 leaves the set and its routing (§3) is
   optional tidiness. ~~If "yes", the same reasoning may add sites I dismissed.
   **This is the derivation's single load-bearing INFERRED row.**~~
   `[QA 2026-08-13: HELD as INFERRED but DEFANGED — it is not load-bearing.
   The own-thread axis is exhaustive: both trees create exactly 6 GT threads,
   and E7's is the ONLY yield-free body (the other five are E3/E4/E5/E6 plus
   RainsDeadlock:195, whose entry value is vanilla's own `RainsDisasterLoop`,
   read live from _G at create time — the pack never replaces that global).
   So a "yes" answer adds NO site beyond E7 itself, and a "no" answer removes
   only E7. Neither answer changes any list, any disposition, or the 6f gate
   repair (which E5/E6 need regardless and which covers E7's worst case).
   Optional: prompt 4 could measure it cheaply — probe-create a yield-free GT
   thread, save before unpausing, load back and look for it — but nothing
   gates on the answer.]`
2. ⚠️ **E12's synchronicity argument.** I claim no save can interleave
   `rawset` … `pcall(shipped, w)` … `rawset` because nothing there yields. That
   rests on `Colonist:UIStatUpdate`'s 201-line body and its rollover path being
   yield-free, which I checked for *direct* yields only.
   `[QA 2026-08-13: extended — a token scan of the whole body (:2932-3133)
   finds zero `Sleep`/`Wait*` of any kind, and the wrapper runs in UI/rollover
   context where the save command shares the same cooperative thread domain.
   Indirect-helper yields remain unaudited; the row's "conditional" tag
   stands. Disclosed residue, not a gate item.]`
3. ⚠️ **D10 was never sampled.** The FixtureCarry dumps show no
   `SMRFixPack_F35_*` — but those saves may simply not be affected saves
   (F35 fires only when Frictionless Composites is researched and the label is
   unbuffed). **Absent ≠ refuted**; I have not measured the modifier that the
   whole KEEP list's headline entry is about.
   `[QA 2026-08-13: STANDS — still unsampled (this prompt was game-free). The
   mechanism was source-verified instead (write shape at 90_SaveSanitizer:84-89,
   re-add guard at :69-76). ROUTED to prompt 4: its damaged-fixture leg must
   SAMPLE the condition — plant or manufacture an F35-affected witness
   (synthetic residue via probe is acceptable) and read the modifier back, per
   the house rule that "refuted/measured" requires the condition sampled, not a
   zero count.]`
4. ⚠️ **Can a cleaner do anything at all about §2a's captured frames?** My
   working assumption is no — the frames are inside vanilla threads' stacks,
   `debug` is blacklisted, and adjudication §8.5 confirms there is no lever to
   clear a frame from another thread's stack. If that holds, §2a's entire
   disposition is "inert-accepted", and the artifact's real scope is §2b.
   I believe this is right and it materially shrinks the artifact — which is
   exactly why it deserves a hostile read.
   `[QA 2026-08-13: SUSTAINED for what it claims — no lever reaches a frame
   inside another thread's stack, so §2a is inert-accepted wholesale. ⛔ But
   the conclusion drawn from it in §8.3 ("no thread surgery whatsoever") does
   NOT follow and is corrected there: captured FRAMES are not the same thing
   as whole ORPHANED THREADS with stale entry bodies (pre-rewrite-lineage
   `Meteors` / old-body rains loops), which ARE reachable — vanilla's own
   `RestartGlobalGameTimeThread` / `FinishRainProcedure` / `DeleteThread`+
   recreate-onto-vanilla-body primitives — and which the artifact's population
   (saves the current pack never touched) still carries.]`
5. ⚠️ **`SMRFixPack_Disabled`/`_Optional` exclusion.** I proved they are not in
   `PersistableGlobals`, so not save state. If that is wrong, five more names
   join the table.
   `[QA 2026-08-13: SETTLED — the whitelist mechanism itself was verified at
   persist.lua:119-143 (save writes and load restores iterate
   `PersistableGlobals`, never the data), and the option tables are created by
   plain assignment, never `GameVar`. Not save state.]`
6. ⚠️ **Site-vs-module counting.** E9/E10 are two wrappers on one method; E2/E3
   are two bodies in one module. A reviewer could defensibly call that 10 code
   sites, or 12. I chose the finer grain because the disposition table is
   per-site.

---

## 7. The disposition table (FIX_POLICY §3a release gate) — DRAFT

| site | disposition | reason |
|---|---|---|
| E1 RainsDeadlock wrapper | **repaired-in-pack** (Tier 1, `SAVE_SAFETY_REDESIGN` §6.2a-B) + **inert-accepted** | the harmful body copy is gone; what remains is a layer-2 frame with nothing after it |
| E2 Bombardment `WaitBombard` | **inert-accepted** (level 2) | no layer-3 route (§5.3); orphan completes correctly; D3 = keep the fix |
| E3 Bombardment per-missile | **inert-accepted** (level 2) | same |
| E4 StormWedgeHeal | **repaired-in-pack** (Tier 1 §6.2a-D orphan-gate reorder) | gated; dies cleanly |
| **E5 CrystalMysteryHang** | ~~⛔ **ROUTED** (rule 6f)~~ **repaired-in-pack** `[AUDIT 2026-08-13: the routing was CONSUMED — owner answered checklist 19 and prompt 2b built the §3a orphan gate in-pack, commit 91fc5d0; gate verified in shipped source at Fix_CrystalMysteryHang.lua:78 by the terminal audit. Installed path unchanged (74/74 + suite PASS, r0/r1). The orphan path itself is source-tier: it can only execute in an uninstalled player's save, where no log reaches us]` | was: ungated mod-owned thread body; one-line in-pack repair reachable — §3 |
| **E6 ExtenderFlapChurn** | ~~⛔ **ROUTED** (rule 6f)~~ **repaired-in-pack** `[AUDIT 2026-08-13: same — gate at Fix_ExtenderFlapChurn.lua:96, commit 91fc5d0]` | same |
| **E7 TrackConnectorPingPong** | ~~⛔ **ROUTED** (rule 6f)~~ **repaired-in-pack** `[AUDIT 2026-08-13: same — gate at Fix_TrackConnectorPingPong.lua:179, commit 91fc5d0; doubt 1 stays INFERRED and defanged either way]` | same, pending doubt 1 |
| E8 CaveIns FUNC slot | **inert-accepted** (level 2) | compliant; ~1 in 9 Underground saves; dead weight |
| E9 ArrivalDeaths Idle | **repaired-in-pack** (Tier 2, half b) + **inert-accepted** | layer-2 compliant |
| E10 ShelterReflex Idle | **inert-accepted** (level 2) | already compliant, nothing owed |
| E11 LastTransmission eval | **inert-accepted** (level 2, disclosed) | adjudication §4.4; route re-derived |
| E12 MoraleComfort GetProperty | **inert-accepted** (level 2) | window is one synchronous call — pending doubt 2 |
| D1 MeteorLatch | **KEEP** | latch semantics — `[QA 2026-08-13: also self-clearing and cleaner-unreachable (mod-registered GameVar); KEEP = no action, trivially satisfied]` |
| D2 FirstAsteroidPrefabs | ~~**cleaner-target (REMOVE)** ⚠️ least-certain list placement~~ **NO ACTION — self-clearing, cleaner-unreachable** `[QA 2026-08-13: mod-registered GameVar, dropped on any modless load and never re-saved (persist.lua:136-142); a cleaner would have to re-register the name to touch it, which 6d bars. The least-certain placement dissolves]` |
| D3 loop_version | **cleaner-target (REMOVE)** | inert stamp |
| D4 fixed_loop | **repaired-in-pack** (cleared on migration) + **cleaner-target** for never-migrated saves | legacy |
| D5 reserved_at | **cleaner-target (REMOVE)** | 1257×-measured; inert |
| D6 shelter_try | **cleaner-target (REMOVE)** | inert |
| D7 payload_set | **cleaner-target (REMOVE)** | inert |
| D8 rocket_fuel_key | **repaired-in-pack** + **cleaner-target** for never-loaded saves | measured 0× today |
| D9 spawn_gate | **inert-accepted** — ⛔ *not* a cleaner target | self-replaces within one wave (PT-61-measured); reaching it would mean touching vanilla thread locals |
| D10 F35 modifiers | ⭐ **KEEP** | the residue is the repair |
| D11 F48 flag | **KEEP** | one-shot latch |
| D12 ack_notworking | **cleaner-target (REMOVE)** | inert |
| D13 closed_to_new_residents | **cleaner-target (REMOVE)** | inert |
| D14 no_homeless | **cleaner-target (REMOVE)** | inert |
| **D15 dial modifiers** | ⭐ **cleaner-target (REMOVE) — the artifact's reason to exist** | the only residue that keeps *changing the game* after uninstall |

Every one of the 27 sites has a call. No site is unrecorded, so nothing here
blocks release by default — three sites block on the **owner's answer to the
6f routing**, which is a decision, not a gap.

---

## 8. The channel argument, verified — and the artifact sketch

### 8.1 Q-B: the channel question dissolves (README rule 7), verified from the D13 entry's own findings

Not from vibes. The entry records an **owner-run Paradox Mods check
(2026-08-01, audit §7.1(b), `BUG_LIST_AUDIT.md` §10.4)**:

* the channel is live, and a Relaunched fix author already mirrors there
  (GromGor, exact mirror of his Steam workshop);
* **that audience has no console** — "no logs, no console commands, no
  hex-editing there" (entry, deliverable 2);
* therefore *"any rescue path that assumes typing into a console does not exist
  for them"*.

The entry then asks "decide the channel before speccing the artifact, because
the answer changes what the artifact is." **It does not — if the artifact is
built as a mod.** A mod-shaped cleaner installs through whichever channel the
player already uses (Steam Workshop *or* Paradox Mods, PC *or* Xbox/PS5), so it
is the only shape that reaches console players **at all**, and its reach is
strictly a superset of a console-command procedure's on every platform. A
console procedure reaches a subset of PC players and nobody on console.
⇒ **The channel decision stops gating the artifact.** It still matters for the
release checklist (metadata, portal pass, cert) — just not for the spec.

⚠️ Unrelated and still open, recorded so it is not lost: the entry's
**discovery observation** — searching Paradox Mods for `bug` or `fix` returned
zero hits while the author name did not. One browse, never re-checked; it is a
`MOD_DESCRIPTION`/listing problem, not a code one.

### 8.2 Q-A: the derivation's own answer is (c), and §2 is why

The entry's option (c) — *the pack is its own cleaner and the standalone
artifact serves ONLY the already-removed case* — is the one the data supports,
and the support is specific rather than architectural:

**What the pack already cleans, on load, by itself** (so an installed player
needs no artifact): the Meteors one-shot latched heal restarts onto vanilla's
body (`Fix_MeteorFrequency:164-187`); the rains migration moves persisted loops
onto vanilla's `RainsDisasterLoop` and clears `fixed_loop`
(`Fix_RainsDeadlock:180-206`); `Fix_DroneTransportMinors:203-204` deletes its
own legacy field. Those are the three residues that ever *did* anything.

**What it provably does not clean:** all 15 rows of §2b except D4/D8 — and, in
particular, **D15**, whose own module tells the player to fix it *before*
uninstalling. A player who has already uninstalled cannot run any in-pack pass,
by definition. **That is the artifact's population, and it is not empty.**

So (c) is confirmed **against the Job 1/4 data, not assumed** — with one
sharpening the entry does not contain: option (a)'s weakness ("will the player
remember a second step?") mostly evaporates, because under (c) the artifact is
not a step in a healthy uninstall at all. The healthy uninstall is
*"update, load, save, uninstall"* — already true, already documented. The
artifact is a **rescue**, and rescues are self-motivating.

### 8.3 The sketch — shared mechanism core

* **Detection: the curated list of §5, embedded as data.** Never a pattern
  sweep (6b). One table: `{name, carrier-kind, disposition}` where
  carrier-kind ∈ {GameVar, object-field, label-modifier-id, GameVar-entry-field}.
* **The clean pass: purely synchronous, ordered, one `OnMsg.PostLoadGame`.**
  Order: label modifiers (`SetLabelModifier(label, id, nil)` — vanilla's own
  removal path) → object fields (`obj[name] = nil`, walked by class label, not
  by `AllMapsForEach` pattern) → GameVar-entry fields → GameVars last.
  **KEEP entries are never touched**, and the pass reads its own list rather
  than deriving anything.
* **Thread restarts: one-shot and bounded, or not at all.** Trap 2 stands —
  restarting `Meteors` resets a 35-115 h interval. ~~Under doubt 4 the artifact
  may need *no* restart at all: the two thread classes that mattered are
  already vanilla-bodied in any save the current pack touched, and §2a's
  remaining frames are unreachable. **If prompt 2 sustains doubt 4, the
  artifact has no thread surgery in it whatsoever** — which would make it
  dramatically smaller and safer than every prior sizing.~~
  `[QA 2026-08-13: doubt 4 IS sustained, and the conclusion still does not
  follow — it conflates unreachable captured FRAMES (§2a, true, no surgery
  possible) with reachable ORPHANED THREADS carrying stale entry bodies. The
  qualifier "in any save the current pack touched" excludes exactly the
  artifact's population: a save whose pack was removed BEFORE the Tier-1/2
  era never ran the meteor latched heal or the rains migration, and carries
  the D13 entry's named legacy classes (dead/old-body `Meteors`, old-body
  rains loops). SUPERSEDED BY: the spec KEEPS two one-shot bounded heals,
  both via vanilla primitives and vanilla bodies only (6d-compatible, no
  artifact code enters the save): (1) `RestartGlobalGameTimeThread("Meteors")`
  ONLY when the scheduler thread is dead or its body is not vanilla-reachable
  — cost: one 35-115 h interval re-roll, stated to the player; (2) the rains
  heal — stale-ACTIVE via vanilla `FinishRainProcedure`, dead/foreign
  `activation_thread` via `DeleteThread` + `CreateGameTimeThread(RainsDisasterLoop,
  settings)` with vanilla's own global, the pack's proven C34/migration recipe
  — cost: one rain re-roll. Never blanket-repeated; skip-and-report when
  detection is ambiguous. Prompt 3's Job 1 already requires the per-thread
  interval cost in the frozen spec.]`
* **Reporting:** a `WaitMessage` dialog (the same gamepad-native surface
  `00_Core:509-515` already uses, so it reaches console), naming counts per
  name — *"removed 1257 reservation timestamps, 2 drone dials, 11 dome
  flags; kept 3 turbine repairs"* — plus the same line to `ModLog`.
  `[QA 2026-08-13, spec requirement: the dialog MUST ride a REAL-TIME thread
  exactly as 00_Core:498 does — `WaitMessage` yields, and a yield on the
  load-path game-time frame would be a blocked GT frame, the precise shape
  this artifact exists to avoid. The clean pass itself stays synchronous;
  only the report detaches.]`
* **Self-removal story:** residue-zero by construction (6d) — no threads, no
  GameVars, no persisted names of its own, no `optional` machinery, nothing
  after any call that can block. Its own uninstall is "delete it"; the R8
  verification leg is a load-back with the artifact junction pulled (`EF-055`).
* **Version skew:** it states which pack versions' residue it handles, as a
  literal list in its description and a logged line. The list above is
  fix-pack `ada5cbb` / opt-pack `a90d128` era.

**What actually differs per Q-A branch** (so the owner's answer *selects*
rather than respecifies):

| | (a) run-after-removal | (b) keep-installed | ⭐ (c) already-removed only |
|---|---|---|---|
| trigger | player-invoked, once | every load, forever | `PostLoadGame`, once per save, latched |
| latch | needed (don't re-clean) | none — it is a runtime | needed, and it is the artifact's *own* only persisted state ⚠️ which violates 6d unless the latch is session-only |
| KEEP list | identical | identical | identical |
| the D15 fix | same | same | same |
| extra surface | an invoke UI (console-hostile) | a permanent presence — **not a cleaner** | none |
| honest name | "Save Cleanup Tool" | "Compatibility Runtime" | **"Save Rescue"** |
| cost | + an invoke path that must work on a gamepad | + forever-maintenance, + its own residue question | smallest |

⚠️ Note the one real tension (c) creates and (a) does not: a once-per-save
latch is persisted state, and 6d says the artifact carries none. Resolution I
recommend: **no latch — make the pass idempotent instead** (removing an absent
field is a no-op; the counts simply read zero on the second load). That keeps
6d intact and costs nothing.

### 8.4 Repo and packaging proposal

* **Working name:** `SMR-SaveRescue` → mod id `SMR_CommunitySaveRescue`,
  namespace `SMRSaveRescue`, log tag `[CommunitySaveRescue]`. ⛔ It must **not**
  write any `SMRFixPack_*`/`SMROptInPack_*` name — it only *removes* them.
* **Third junction**, installed the same way as the opt pack's, so `EF-055`'s
  agent-side pull works for its own verification legs. Local git, **no remote
  unasked** — ⚠️ **and the opt-pack precedent has since MOVED: the owner ruled
  its remote PUBLIC on 2026-08-13** (`github.com/catt144/SMR-CommunityOptInPack`).
  That ruling was for THAT repo and does not carry to this one; a third public
  repo is still its own ask, and the rule as written stands.
* **Scaffolding depth — deliberately LESS than the opt pack's.** It needs:
  `metadata.lua`, `Code/00_Core.lua` (a much smaller one — registry + log +
  `Require`; **no** Mod Options page, **no** `optional` machinery, **no**
  `DataPatch`/`OnDataReady` scaffold, **no** `ApplyModOptions` reconciler),
  one cleaner module, `docs/` with a `PROVENANCE.md` naming this derivation as
  its source of truth. It does **not** need: an options page (nothing to
  toggle), a `WhenActive` wrapper family (one module), or its own bug/fact
  indexes (its findings belong in the fix pack's records).
* **TestKit:** probes ride the existing kit (it already reads two registries
  per `17a7cf9`; a third is the same change).

---

## 9. What this document does not claim

* Not **complete** — prompt 2's verdict and prompt 5's re-derivation own that
  word.
* Not **safe to remove** for D2 beyond the caveat written into its own row.
* Not **already repaired** for anything without the tier named in §4.1 or §7.
* No blanket provenance — every row in §2 carries its own tag, and the four
  INFERRED/conditional ones are listed again in §6 so they cannot be read past.

---

# 10. ⭐ THE FROZEN SPEC (chain prompt 3, 2026-08-13) — Save Rescue v0.1.0

**Status: FROZEN.** Written from §2/§5/§7 as corrected by the prompt-2 QA pass,
plus the owner's Q-A = **(c)** and Q-B = **mod-shaped** rulings (checklist items
17/18, 2026-08-13). This section is the build contract: `10.2`'s table is the
detection data, `10.3` is the pass, and prompt 4's matrix reads `10.9`. ⛔ Every
claim in §10 is **SOURCE/design tier — nothing was launched** to write it.

## 10.0 Identity, shape, and what it is not

| | |
|---|---|
| display name | **Save Rescue** (owner-ratified 2026-08-13) |
| mod id | `SMR_CommunitySaveRescue` · namespace `SMRSaveRescue` · log tag `[CommunitySaveRescue]` |
| repo | `C:\Dev\SMR-CommunitySaveRescue` → `github.com/catt144/SMR-CommunitySaveRescue` (owner pre-created, PUBLIC) |
| shape | a MOD (Q-B), so it reaches Paradox Mods / Xbox / PS5 — §8.1 |
| trigger | `OnMsg.PostLoadGame`, once per load, **no latch, idempotent** (§8.3's resolution of the 6d tension) |
| audience | Q-A (c): saves whose pack is **already gone**. It is a rescue, not a step in a healthy uninstall |
| ⛔ not | a runtime, a toggle surface, an options page, a pattern sweep, a renamer |

## 10.1 ⭐ The stand-down gate — per-pack, not global

The artifact serves the already-uninstalled (Q-A c). A residue row therefore
**runs only when the mod that wrote it is ABSENT from this session**:

```
FP rows act only if  rawget(_G, "SMRFixPack")   == nil
OP rows act only if  rawget(_G, "SMROptInPack") == nil
```

Per-pack rather than one global gate, because the mixed case is real and common:
a player who removed the opt-in pack but kept the fix pack has permanent dial
residue (D15) and no in-pack cleaner for it. A single "any pack present → stand
down" gate would strand exactly the population D15 exists for.

Why the gate at all — three reasons, in order of weight:

1. **The packs already do this work better** (§8.2): a loaded pack heals its own
   threads on load, and `Opt_DroneStatDials` reconciles its own modifiers on
   `PostLoadGame`. Stripping a live module's field is churn at best and a fight
   at worst (both write on the same message; order is not guaranteed).
2. **The likely user error is installing the rescue WITHOUT removing the pack.**
   The gate makes that safe and the report says what to do instead.
3. It keeps the verification matrix honest: with the rig's normal config (both
   packs loaded) the artifact is a **measurable no-op**, which is prompt 4's
   cheapest leg.

⚠️ **Disclosed limitation, by construction:** "loaded" is the `pack=n/n` sense of
off-state doctrine 6e, i.e. states (1) and (2) read as PRESENT. A player who
merely toggled a module off, or disabled the pack without a full restart, gets a
stand-down and no clean. That is correct — they still have the pack — but it
means the rescue is not a substitute for uninstalling, and the report says so.

The clean pass is also **vetoable** for A/B legs: `SMRSaveRescue_Disabled = true`
before our code loads (a plain mod global, §2c's class — not save state).

## 10.2 Detection: the curated table, embedded as data (6b)

⛔ **Detection is BY THIS TABLE ONLY** — never by an `SMRFixPack_*` pattern
(6b: the 2026-07-31 `rawget` sweep false-positived on 192 buildings twice, and a
pattern sweep deletes D10, which is the repair — 6c). All **16 persisted names /
15 rows** of §2b appear below: every one carries an action, so a name absent from
the table is a derivation gap and not a judgement call.

| id | owner | name | carrier kind | where | **action** | why |
|---|---|---|---|---|---|---|
| D15a | OP | `SMRFixPack_DroneSpeedDial` | label-modifier id | `UIColony`, label **"Drone"** | ⭐ **REMOVE** | the headline: the only residue that keeps CHANGING the game after uninstall |
| D15b | OP | `SMRFixPack_DroneCarryDial` | label-modifier id | `UIColony`, label **"Consts"** | ⭐ **REMOVE** | same |
| D5 | FP | `SMRFixPack_reserved_at` | object field | label `Colonist` | **REMOVE** | timestamp; only `Fix_StaleReservations` read it |
| D6 | FP | `SMRFixPack_shelter_try` | object field | label `Colonist` | **REMOVE** | rate-limit timestamp; only the Idle shelter branch read it |
| D7 | FP | `SMRFixPack_payload_set` | object field | label `AllRockets` (the `CargoRequestNew.transporter`, `UniversalRocket.lua:2232`) | **REMOVE** | boolean; absence IS the pre-fix state |
| D8 | FP | `SMRFixPack_rocket_fuel_key` | object field | label `DroneControl` | **REMOVE** | legacy; the current pack already deletes it |
| D12 | OP | `SMRFixPack_ack_notworking` | object field | label `Building` | **REMOVE** | inert stamp |
| D13 | OP | `SMRFixPack_closed_to_new_residents` | object field | label `Community` (Dome/Habitat) | **REMOVE** | nil = vanilla, by the module's own contract |
| D14 | OP | `SMRFixPack_no_homeless` | object field | label `Community` | **REMOVE** | nil = vanilla |
| D3 | FP | `SMRFixPack_loop_version` | field inside a vanilla GameVar entry | `RainsDisasterThreads[<type>]` | **REMOVE** | inert stamp; vanilla ignores unknown fields on reuse |
| D4 | FP | `SMRFixPack_fixed_loop` | same | same | **REMOVE — but LAST** | ⭐ it is also the heal's only DETECTOR (10.4) — read in 10.3 step 1, removed in step 4 |
| D10 | FP | `SMRFixPack_F35_<label>` | label-modifier id | `UIColony`, any label | ⛔ **KEEP** | ⭐⭐ **the residue IS the repair** — removing it re-breaks F35 permanently |
| D11 | FP | `SMRFixPack_F48_StationConnectors` | colony field | `UIColony` | ⛔ **KEEP** | one-shot latch; dropping it invites a second re-ordering pass |
| D1 | FP | `SMRFixPack_MeteorLatch` | **GameVar** | — | **NONE — unreachable** | mod-registered GameVar: dropped on any load without its registering mod (`persist.lua:136-142`). KEEP anyway, so this is trivially satisfied |
| D2 | FP | `SMRFixPack_FirstAsteroidPrefabs` | **GameVar** | — | **NONE — unreachable** | same mechanism; reaching it would mean re-registering the name, which 6d bars |
| D9 | FP | `SMRFixPack_spawn_gate` | field on a descriptor copy in a vanilla scheduler thread's local | — | ⛔ **NOT HUNTED** | self-replaces within one wave (PT-61-measured); reaching it means touching a vanilla thread's locals |

⛔ **Never rename, never rewrite.** Persisted names are save contract in both
packs; the five opt-side names keep the legacy `SMRFixPack_` prefix and the
rescue honours those bytes exactly (opt-pack `PROVENANCE.md` §2).

**Object-field enumeration** is a **label walk**, not a map pattern sweep: for
each city in `Cities`, every list in `city.labels`, each object visited once
(identity-keyed `seen` set), and for each visited object only the exact names
above are tested with `rawget` and cleared. Labels are named in the table for
documentation; the walk covers **every** label, so a mis-guessed label name
cannot silently skip a carrier.

⚠️ **Known incompleteness, disclosed rather than hidden:** an object in no label
is not visited — the real case is a colonist riding a rocket
(`CargoTransporter.keep_cargo_in_labels = false`, `CargoTransporter.lua:9`, so
cargo colonists leave the labels). Their `reserved_at`/`shelter_try` timestamps
survive that load. The pass is idempotent and runs on **every** load, so they are
cleaned on the first load after they disembark. Inert data either way (§2b).

## 10.3 The clean pass — synchronous, ordered, one `PostLoadGame`

Order is load-bearing at exactly one place (step 1 before step 4).

| # | step | scope | notes |
|---|---|---|---|
| 0 | gates | — | veto → `UIColony`/`Cities` present → per-pack stand-down (10.1) |
| 1 | **thread heals** | FP | rains first (reads D4), then meteors — 10.4 |
| 2 | **label modifiers** | OP | `UIColony:SetLabelModifier(label, id, nil)` — vanilla's own removal path, the one `Opt_DroneStatDials` itself uses at base position (`:128-137`) |
| 3 | **object fields** | FP + OP | the label walk of 10.2 |
| 4 | **GameVar-entry fields** | FP | D3/D4 inside `RainsDisasterThreads` entries |
| 5 | **GameVars** | FP | **no-op by construction** — D1/D2 are unreachable; the step exists as a stated fact, not as code that registers anything |
| 6 | report | — | 10.5 |

Every step is wrapped in its own `pcall`, so a step that raises costs that step
and not the pass (`90_SaveSanitizer:326-341`'s discipline). FIX_POLICY binds:
fail-safe, never loud; self-checks return reasons, never error.

## 10.4 The two one-shot bounded heals — vanilla bodies only, with their price

Both exist for **pre-rewrite-lineage saves** — the population that uninstalled
BEFORE F86 Tier 1/2, which never ran the pack's own latched heal or rains
migration (QA correction to §8.3; §6 doubt 4 is sustained for captured FRAMES,
which remain unreachable and untouched). Both use vanilla primitives and vanilla
entry bodies, so nothing of the artifact can enter the save.

**(1) Rains — detector-driven, therefore precise.**

* *stale-ACTIVE:* `g_RainDisaster` truthy while its `RainsDisasterThreads` entry
  has no valid `main_thread` → vanilla `FinishRainProcedure(<type>)`
  (`TerraformingDisasters.lua:247-274`); unknown rain type → the pack's manual
  fallback (`g_RainDisaster = false` + `Msg("RainDisasterEnd", MainMap, "normal")`).
  **Cost: the phantom rain ends — that IS the repair.**
* *legacy loop body:* an entry with a **valid** `activation_thread` **and**
  `SMRFixPack_fixed_loop == true` is running the pack's OLD replaced loop body,
  captured by value. `DeleteThread` + `CreateGameTimeThread(RainsDisasterLoop,
  settings)` — vanilla's own global, read live at create time.
  **Cost: one rain re-roll for that type** (the recreated loop restarts its
  `Sleep(spawntime + AsyncRand(spawntime_random))`).
* *settings resolution:* `Presets.MapSettings.RainsDisaster[data.id]`, else a
  UNIQUE `settings.type == rain_type` match, else **leave and report** — the
  pack's proven recipe (`Fix_RainsDeadlock:180-206`).
* ⭐ **Why no stamp is needed and none is written:** the detector (D4) is
  REMOVED by step 4 of the same pass, so a second load cannot re-fire the heal.
  The heal consumes its own evidence. That is what keeps 6d intact — a stamp
  would be the artifact's own persisted name.
* ⚠️ An entry with `SMRFixPack_loop_version` set and no `fixed_loop` was already
  migrated onto vanilla's body by the pack: **thread untouched**, stamp removed.

**(2) Meteors — dead/absent only.**

`RestartGlobalGameTimeThread("Meteors")` (rebuilds from
`GlobalGameTimeThreadFuncs`, which with no pack loaded is **vanilla's body**)
**only when** all of: `IsValidThread(rawget(_G,"Meteors"))` is false ·
`GlobalGameTimeThreadFuncs.Meteors` is a function · a map is loaded ·
`IsGameRuleActive("NoDisasters")` is false · `GetMeteorsDescr()` returns a
descriptor that is not `forbidden`. The last three are `Fix_MeteorFrequency`'s
own designed-silence guards (`:123-127`) — without them the tool would "repair"
a map that is supposed to be quiet.

**Cost, stated to the player verbatim: one meteor re-roll — the next strike is
drawn afresh from the descriptor's 35–115 h window, and a pending warning is
lost.** Never repeated: the restart happens only on a load that finds the thread
dead, and a restarted thread is alive on the next load.

⛔ **Ambiguity → SKIP AND REPORT, never guess.** A **live** `Meteors` thread
whose body is a captured pack-era body is **not detectable from Lua** (there is
no lever that reads another thread's entry function), so a live thread is left
alone and the skip is logged. Restarting a healthy thread on every load would
re-roll the timer forever — trap 2, exactly what 6d bans.

## 10.5 What the player sees

A `WaitMessage` dialog — the gamepad-native surface that reaches console
(`00_Core:509-515`'s precedent) — **and the same content to `ModLog`**.

⛔ **The dialog MUST ride a real-time thread** (`CreateRealTimeThread`, the
`00_Core:498` pattern): `WaitMessage` yields, and a yield on the load-path
game-time frame would be a blocked GT frame — the precise shape this artifact
exists to avoid. The **clean pass stays synchronous**; only the report detaches.
RT threads are persisted only when flagged `threadPersist`
(`persist.lua:128-131`) and nothing here flags one, so the report thread cannot
enter a save.

**When it appears:** only when the pass actually did something (removed or
repaired ≥ 1). A load that finds nothing is **silent** (log line only) — that,
plus idempotence, is what replaces the latch §8.3 rejected. Second load of a
cleaned save: nothing found, no dialog, no state.

**Text (frozen; counts substituted, empty groups omitted):**

> **Save Rescue**
>
> This save still carried leftovers from the Community Fix Pack mods. They are
> now removed. Nothing was added to your save.
>
> Removed: 2 drone stat dials (drone speed and carry capacity are back to the
> game's own values) · 1257 reservation timestamps · 11 dome flags · 4 building
> flags
>
> Repaired: the meteor timer was restarted — the next meteor is re-rolled from
> its normal 35–115 hour window · 1 rain cycle restarted on the game's own
> timer (one re-roll)
>
> Kept on purpose: 3 wind turbine repairs. These entries repair a bug in your
> save; deleting them would bring it back.
>
> You can remove Save Rescue whenever you like — it stores nothing in your save.

**Stand-down text (10.1), shown once per session, never per load:**

> **Save Rescue**
>
> The Community Fix Pack (or its Opt-In Modules) is still installed, so there is
> nothing for this tool to do: while those mods are installed they clean up after
> themselves. Uninstall them first, then load this save again.

### ⛔ CORRECTED 2026-08-14 BY RE-DERIVATION (chain `release-3` prompt 1, Job 0) — the frozen REPORT text above is not what the build prints

The blocks above are the **design** text and are preserved as written. The built
`report_text()` (`10_SaveRescue.lua:508-537`, rescue repo) differs from the
report block in **four** places — the eyes at the sitting found one; re-deriving
both sides at their sources found the other three. ⭐ **The second is confirmed
by the WITNESSED dialog itself**, not by reading code alone.
⚠️ The **stand-down** block is word-for-word what the code shows
(`10_SaveRescue.lua:712-713`); it differs only by a paragraph break. Nothing
below touches it.

| # | frozen §10.5 says | the build prints | class |
|---|---|---|---|
| 1 | `2 drone stat dials (drone speed and carry capacity are back to the game's own values)` | `2 drone stat dials` | ⛔ SUBSTANTIVE — the one non-inert residue loses its explanation |
| 2 | groups in table order — the drone dials FIRST | `join()` runs `table.sort` over the already-formatted `"N noun"` strings, so groups order by the **digits of each count read as characters** | ⛔ SUBSTANTIVE — the line that matters lands wherever its first digit sorts |
| 3 | `35–115 hour window` (en dash) | `35-115 hour window` (ASCII hyphen) | cosmetic |
| 4 | `(one re-roll)` | `(one re-roll each)` | cosmetic — and the **build's is better**: it is correct in the plural, which the design text is not |

**Evidence for #2, from the sitting's own witness — not from reading the code.**
The report dialog witnessed 2026-08-14 (the reading that carries D13 `tested`)
reconciles as `1 + 1533 + 2 + 22 + 4 + 4 = 1566` (D13 entry, dialog reading 1).
Those six counts *in that order* are exactly `table.sort` over
`"1 rain loop stamp"`, `"1533 reservation timestamps"`, `"2 drone stat dials"`,
`"22 dome flags"`, `"4 building flags"`, `"4 rocket payload flags"` — the noun
sums the `CSSWEEP` pass line produces. ⇒ On the only witness that has ever
carried what a real player's save really holds, **the line this tool exists for
printed THIRD of six, wedged between 1533 reservation timestamps and 22 dome
flags, with no indication of what it meant.** That is worse than the gap as
first written, and it is measured, not inferred.

### The resolution — SPEC-AMEND, PROVISIONAL, and why the code was not touched

**This section is now a record of two texts: the design text (above, frozen,
superseded as a quotable source) and the built text (below, authoritative).**
⛔ **No player surface may quote the frozen block.** ③ quotes the built text or
nothing.

The trade was priced, not assumed:

* **A code fix re-opens a witnessed claim.** The witness is *"text matching
  `report_text()` exactly"* — the code was the reference. Changing the string
  keeps the mechanism claim (function output reaches the screen verbatim) but
  leaves the **new** string unsampled. ⛔ And the new string is the risk: the
  gloss adds ~60 characters to one line of a **gamepad-native `WaitMessage`**,
  and wrapping/overflow on that surface is a screen-only property **no log can
  ever adjudicate** (the terminal audit's own ruling, D13). It also happened
  that the sitting's screenshot was **partly covered by Test Kit `print()`
  output** (harness defect 1), so the dialog's rendering at full width is the
  least-observed thing about it. A longer line is precisely the change that
  needs eyes.
* **The re-witness is an owner visit**, and `EF-055`'s measured LIMIT says a
  junction round trip cost one Mod-Manager visit + restart on 2026-08-14 with
  two candidate causes still undistinguished. So the floor is one owner visit,
  not zero.
* **The audience may not exist.** The rescue artifact's publish is itself a
  release-time call (checklist 17, "build ≠ publish").
* **The evidence campaign is FROZEN pre-release** (owner, checklist 14).

⇒ Spec-amend is the **no-cost branch** and it is taken, marked provisional; the
owner call is routed as one line (`PLAYTEST_CHECKLIST.md`, "Decisions waiting on
you", item 28) and **bundled with checklist 17**, because "is better dialog text
worth an owner visit?" is downstream of "is this being published at all?"

⭐ **What ③ does about the substance, at zero cost:** the information the gloss
carried does not depend on the dialog. It is the same fact D13's uninstall text
already states — *a non-base Drone speed/carry dial keeps working forever after
uninstall* — so ③ carries it in **words on the rescue description and in the
uninstall story**, surfaces ③ owns outright and no code touches. The player who
installs the tool has read why before the dialog ever raises.

### ⭐ The built report text — AUTHORITATIVE, this is what ③ may quote

Derived from `report_text()` (`10_SaveRescue.lua:508-537`) at 2026-08-14, with
the sitting's own witnessed counts substituted so the ordering is visible:

> **Save Rescue**
>
> This save still carried leftovers from the Community Fix Pack mods. They are
> now removed. Nothing was added to your save.
>
> Removed: 1 rain loop stamp · 1533 reservation timestamps · 2 drone stat dials ·
> 22 dome flags · 4 building flags · 4 rocket payload flags
>
> Kept on purpose: 1 track re-order latch. These entries repair a bug in your
> save; deleting them would bring it back.
>
> You can remove Save Rescue whenever you like — it stores nothing in your save.

Rules the build follows, so a quoter can reconstruct any case: **empty groups
are omitted** entirely (the witnessed run had no *Repaired* section at all,
because `heals` were `0, 0, 0`); groups are joined with ` · `; each group is
`N noun` with an `s` added when `N ~= 1`; the *Repaired* line, when it appears,
reads `the meteor timer was restarted — the next meteor is re-rolled from its
normal 35-115 hour window` and/or `N rain cycle(s) restarted on the game's own
timer (one re-roll each)` and/or `N rain(s) that the save thought was still
running was ended`.

## 10.6 Version skew — answered by disclosure, because detection is impossible

⛔ **The artifact CANNOT know which pack version wrote a save.** The only stamp
that carried a version (`SMRFixPack_MeteorLatch`, D1) is a mod-registered
GameVar and is dropped on the first load without the pack (`persist.lua:136-142`)
— by the same mechanism that makes D1/D2 unreachable. So version skew is handled
by **stating** coverage, never by sniffing it:

* **Covered:** every persisted name either shipped pack has written up to
  fix-pack `cdbcd9d` / opt-pack `e17586b` (2026-08-13) — the 16 names of 10.2,
  **including the two legacy names** (`SMRFixPack_fixed_loop`,
  `SMRFixPack_rocket_fuel_key`) that only older builds wrote, which is precisely
  the too-old case handled.
* **Too old:** a pre-release build that wrote a name not in the table is left
  untouched — the tool removes only what it can name. It never sweeps.
* **Too new:** a pack version newer than this table may write names the tool
  does not know. The tool logs its own version and derivation stamp on every
  run, and its description says: if you used a Fix Pack released after this
  tool, check for a newer Save Rescue.
* **Console surfaces:** `SMRSaveRescue.ListResidue()` prints the whole table
  with actions; `SMRSaveRescue.Scan()` counts what is present without removing
  anything. Both are read-only.

## 10.7 Self-removal, and the constitution-6d compliance argument

6d: *"the artifact is residue-zero BY CONSTRUCTION: purely synchronous, no
threads, no GameVars, no persisted names of its own, no `optional` machinery."*
Point by point, with the mechanism each rests on:

| 6d clause | how the build satisfies it | mechanism / cite |
|---|---|---|
| no GameVars | it never CALLS `GameVar` — no registration anywhere, not even to reach D1/D2 `[AUDIT 2026-08-13: wording corrected — the STRING does appear in comments and as the table's "gamevar" kind-tag (00_Core.lua:8, 10_SaveRescue.lua:99-102 etc.); what the audit verified is zero `GameVar(` call sites in the tree]` | §5's QA ruling; `persist.lua:119-143` |
| no persisted names of its own | it performs **no write of any name**: every mutation is `field = nil` or `SetLabelModifier(label, id, nil)`. Its two globals (`SMRSaveRescue`, `SMRSaveRescue_Disabled`) are plain mod globals, absent from `PersistableGlobals` — §2c's proven class, not save state | `persist.lua:117-134` |
| no threads (in the save) | the clean pass is synchronous inside `PostLoadGame`. The ONE thread it creates is the report's **real-time** thread, and RT threads persist only when flagged `threadPersist`; `MakeThreadPersistable` appears nowhere in the tree | `persist.lua:128-131`, §2c |
| — the rains heal creates a GT thread | ⚠️ stated plainly: it does, and it is **vanilla's**. `CreateGameTimeThread(RainsDisasterLoop, settings)` takes the entry body from vanilla's own global read live at create time, and stores it in vanilla's own `RainsDisasterThreads` entry field. Nothing of the artifact is captured — the same argument, and the same recipe, the pack's own migration already ships | `Fix_RainsDeadlock:195`; §6 doubt 1's exhaustive own-thread axis |
| no `optional` machinery | no Mod Options page, no `default_options`, no toggle reconciler, no `WhenActive` family — one module, always armed, gated only by 10.1 | 10.0 |
| purely synchronous | nothing between the first and last mutation yields; the only yield in the mod is inside the detached report thread | 10.5 |
| thread restarts one-shot and bounded | 10.4: one restart per dead thread per load, never blanket-repeated, each priced | trap 2 |

**Self-removal story.** Delete the mod (or pull its junction — `EF-055`). There
is nothing to undo: the artifact writes no field, no modifier id, no global into
the save, and holds no reference the save can capture. A save loaded once with
Save Rescue and then loaded without it differs only by the residue it removed —
which is the point. The R8 verification leg is exactly that: clean, save, pull
the junction, load back, read the same names (prompt 4).

⛔ **What this argument is NOT:** it is not "residue-zero" as a measured claim.
That is prompt 4's, from a real load-back. This is the compliance ARGUMENT — no
thread, no GameVar, no field, no closure — each line cited.

## 10.8 The probe surface (why the API exists at all)

The rig's normal config is both packs loaded, where 10.1 makes the automatic
pass a deliberate no-op — so a probe that only waited for `PostLoadGame` could
never sample the pass. The module therefore exposes what the passes do, the way
`SMRFixPack.Sanitizer` already does (`90_SaveSanitizer:290-300`), and for the
same recorded reason (the PT-35 lesson: a direct call that short-circuits on its
own gate returns a zero that samples nothing):

* `SMRSaveRescue.RunPass(opts)` — runs the pass and returns a counts table;
  `opts.force = true` bypasses **only** the 10.1 stand-down (never the KEEP
  list, never the ambiguity skips).
* `SMRSaveRescue.Scan()` — read-only census of the table against this save.
* `SMRSaveRescue.ListResidue()` — prints the table and its actions.
* `SMRSaveRescue.HealThreads(opts)` — the 10.4 heals alone.

## 10.9 The verification contract prompt 4 must read

1. **KEEP survives:** after a forced pass, `SMRFixPack_F35_<label>` modifiers and
   `SMRFixPack_F48_StationConnectors` are still present, unchanged. A KEEP name
   missing after a clean is a stop-the-leg condition (README stop conditions).
2. **REMOVE goes:** the 11 REMOVE names of 10.2 read absent after the pass, and
   a save/reload round trip still reads them absent (EF-049: disk bytes +
   load-back).
3. **The no-op:** with a pack loaded, the automatic pass performs **zero**
   mutations and says so in the log — the counts line prints its zero
   (`90_SaveSanitizer:280-284`'s rule: an absence of lines cannot be told from an
   absence of the pass).
4. **Artifact-absent:** with the rescue's junction pulled, the save loads with
   zero lines naming it and zero `[LUA ERROR]`.
   ⛔ **CORRECTED 2026-08-13 BY MEASUREMENT (`D13_VERIFICATION.md` §4.5, log
   `archive/rs_r3_Mars.exe-20260813-11.54.59.log`): "zero lines naming it" is
   FALSE as written.** Zero `[LUA ERROR]` held, and zero lines came from the
   artifact's own code — but the ENGINE prints one:
   `Savegame references Mod Save Rescue (id SMR_CommunitySaveRescue,
   v0.01-000) which is not present`. It is a standing behaviour, not this
   artifact's: the same pair printed for **Community Fix Pack** and **Community
   Opt-In Pack** when a pack-written save was loaded with the packs pulled
   (`archive/rs_r2pre_…:140-141`), because every mod loaded at save time is
   recorded in the savegame's mod-reference list. ⭐ **It self-clears on the
   first save without the mod** — that list is regenerated from whatever is
   loaded when the save is written, so both pack references were gone from the
   very next save (`mods: SMR_CommunityFixPackTestKit`). ⇒ The true clause is
   *zero lines from the artifact's own code, and one engine line that every mod
   including both packs produces and that disappears on the next save.*
   ⚠️ Player-facing consequence, and it belongs in the description rather than
   here: someone who uninstalls sees one notice on their next load, so the
   report's *"it stores nothing in your save"* is true about STATE (measured:
   zero artifact-namespace names over 4510 objects, `UIColony`, every rains
   entry and all 440 `PersistableGlobals` names) but should not be read as
   "you will see nothing".
5. **Bounds:** the meteor restart happens at most once per load, and not at all
   when the thread is alive; a second consecutive load of the same save performs
   **no** heal and **no** removal (idempotence, which is what replaces the latch).
6. **Fixtures:** `PT35FIXTURE` carries fields + `MeteorLatch` per the split
   matrix's FixtureCarry dumps. ⛔ **No save in the folder is known to carry
   PRE-REWRITE-lineage rains/meteor residue** (`SMRFixPack_fixed_loop`, a dead
   `Meteors` thread) — that class must be **manufactured by a probe writing
   synthetic residue**, and D10's condition must be SAMPLED, not assumed absent
   (§6 doubt 3's routing).
