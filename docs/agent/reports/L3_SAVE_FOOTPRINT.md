# L3 — the aggregate save footprint, the load-time pass order, and the exit

**Pre-launch sweep chain, link 3, lens L3 "save & exit" (2026-08-18).** Produced
against `da703a0`, tree clean, `doccheck` GREEN, `upload_preflight` 20 checked /
0 FAIL / 1 UNCHECKABLE, probe sweep 0 hits.

⛔ **Nothing here was run in a game.** Every row is derived from the shipped
`Code/` tree read at the cited lines plus `ModTools\Src` re-read by symbol. Where
a claim rests on a route rather than a citation, the route is stated and was
re-derived this session — not inherited (`WORKFLOW` R3, and the standing rule
that a recorded fact is a claim).

**Instrument:** `tools/l3_save_footprint.py`, run over all **76** `Code/*.lua`
in `metadata.lua` `code` order. It is lexical and therefore an over-reporter; it
resolves the file-local alias first (the L1 lesson), and every row it emitted in
a bucket that can reach a savegame was read at source before it appears below.

> ⚠️ **Own-instrument defect, disclosed.** The first draft matched only
> `OnMsg.X = f` and missed the `function OnMsg.X() … end` declaration form,
> hiding **two** `PostLoadGame` passes (`Fix_MeteorFrequency:164`,
> `Fix_MeteorStormWedge:217`) from the load-order table. Caught by cross-checking
> the census against a plain grep; fixed, and the fix is commented in the script.
> A second draft scanned string-blanked lines for `SMRFixPack_*` tokens and so
> lost the 4 names that live only inside string literals. Both counts below are
> post-fix. ⛔ Neither defect changed a verdict, but a load-order table that
> silently omits two passes is worse than no table.

---

## 1 · What the whole pack puts into one savegame

| shape | count | where |
|---|---|---|
| game-time threads created (persisted by default, `EF-019`) | **6** | §4 |
| real-time threads (never persisted) | **2** | `00_Core:560`, `Fix_MilestoneCrash:40` |
| `GameVar` declarations of our own | **2** | `Fix_MeteorFrequency:76`, `Fix_FirstAsteroidPrefabs:115` |
| distinct `SMRFixPack_*` tokens | **13** | of which **2** are the non-persisted veto surfaces (`_Disabled`, `_Optional`) ⇒ **11 persisted names** |
| persisted keys that do **not** use the `SMRFixPack_*` convention | **1** | §3 — `smr_shuttles` |
| `OnMsg.SaveGameStart` / `SaveGameDone` registrations | **0** | §5 |
| load-time passes (`LoadGame` + `PostLoadGame`) | **18** | §6 |
| assignment sites with a non-local target | **294** | bucketed in §2 |

**The 11 persisted names re-derived independently this session reproduce D13's
fix-pack rows D1–D11 exactly, with zero membership difference.** That is a
re-derivation, not an inheritance: the census was built from the tree, then
compared. ⭐ It also means the two module changes since D13 was written
(`Fix_DistressPopupPause` added and removed 2026-08-15;
`Fix_AutomationLawCompensation` added 2026-08-15) **added no persisted name** —
C39's header declares "Layer 2 by construction, nothing persisted"
(`:96-102`) and the census agrees: it writes no instance field, creates no
modifier, no `GameVar` and no thread.

## 2 · Write sites, by receiver kind

| bucket | sites | function values | can it reach a save? |
|---|---|---|---|
| `local?` | 111 | 2 | no — file-locals |
| `instance` | 57 | 0 | ⭐ **yes** — read individually |
| `engine` | 43 | 12 | only where the global is itself persisted |
| `unknown` | 40 | 1 | adjudicated by reading; 37 are `ctx.*` on the `DataPatch` scaffold's own table |
| `modtable` | 35 | 2 | no — mod env |
| `global?` | 6 | 1 | adjudicated by reading |
| `ui` | 2 | 2 | no — UI windows are not persisted |

Of the 57 `instance` rows, **21 are `entry.*` on `SMRFixPack.fixes[id]`** — a mod
table the classifier could not distinguish from a game object, and not persisted.
The remainder are writes onto real game objects, all of vanilla-valued data into
vanilla-named fields except the five `SMRFixPack_*` instance fields (D5, D6, D7,
D8, and `Fix_ShelterReflex`'s) and the one in §3.

## 3 · ⭐ The one persisted key that breaks the naming rule — and why that matters

`FIX_POLICY` §3: *"No new persisted classes or GameVars unless unavoidable; if
needed, name them `SMRFixPack_*`."* The authoritative exposed-set derivation
swept route-(c) persisted state with **exactly that token as its grep key**
(`D13_EXPOSED_SET.md` §1.1, row "route (c) named state"). ⇒ **the naming rule is
not a style preference; it is the key the census runs on, and a site that breaks
it is structurally invisible to the census.**

The decisive test needs no convention: a field name we write onto a non-local
carrier either exists somewhere in the shipped tree or it does not. Run over
**4,446** Src `.lua` files / **131,363** distinct tokens, against the **66** field
names the pack writes on non-local carriers:

**9 absent from the whole shipped tree · 6 follow the convention · 3 do not:**

| name | site | verdict |
|---|---|---|
| `ever_changed` | `ctx.ever_changed` ×5 | ❌ not persisted — `ctx` is the `DataPatch` scaffold's own table |
| `update_suspect` | `entry.update_suspect` ×4 | ❌ not persisted — `entry` is `SMRFixPack.fixes[id]` |
| **`smr_shuttles`** | `Fix_ShuttleTransportCache:88` | ⭐ **PERSISTED** |

**The route, re-derived at Src rather than cited.**
`g_TransportationModeToCommunityCache` is declared `GameVar(…, false)` at
`Lua\Units\Colonist.lua:2478`. Our `Fix_ShuttleTransportCache` replaces
`FindTransportationModeToCommunity` and writes `entry.smr_shuttles = with_shuttles`
(`:88`) onto the cache entry table stored at `t[pos]` inside that GameVar.
⇒ a mod-authored boolean under a mod-authored key travels in every savegame.

⛔ **`D13_EXPOSED_SET.md` §2c lists `g_TransportationModeToCommunityCache` among
globals whose contents are "indistinguishable from vanilla's own and carry
nothing of ours." For this global that is false**, and it is false for the
precise reason the derivation could not have caught: its key was the naming
convention this one site does not follow.

**What the site actually costs, adjudicated honestly:**

* vanilla's body reads `if not t[pos] then … end; return table.unpack(t[pos])`
  (`Colonist.lua:2533-2537`). `table.unpack` takes the array part; a hash key
  cannot affect it. ⇒ **inert after uninstall**, exactly as the module's own
  header claims (`:22-24`), which is accurate and was written deliberately.
* the whole cache is dropped wholesale on `TrainRoutesRebuilt` /
  `DomesConnected` / `DomesDisconnected` (`:2480-2488`) ⇒ the residue is
  **transient**, not permanent.

⇒ **Three-tier ethos level 2 at worst (non-harmful trace), plausibly level 1
(it does not outlive the next flush). It is not a defect in behaviour.** What it
*is*, is an **exposed site with no recorded disposition**, and `FIX_POLICY` §3a
is explicit: *"A site with no recorded disposition blocks release by default; a
site with one does not, whichever way it went."* ⇒ routed to the checklist, with
the disposition proposed rather than asserted (§9).

## 4 · The six game-time threads, and §3a's orphan gate in aggregate

`FIX_POLICY` §3a's orphan gate is written as a universal: *"Every mod-owned
thread body opens each wake with an explicit orphan gate."* Answered over all six
sites, not per module:

| # | site | entry body | orphan gate |
|---|---|---|---|
| 1 | `Fix_CrystalMysteryHang:71` | our closure | ✅ `:78` |
| 2 | `Fix_TrackConnectorPingPong:174` | our closure | ✅ `:179` |
| 3 | `Fix_ExtenderFlapChurn:90` | our closure | ✅ `:96` |
| 4 | `Fix_MeteorStormWedge:138` | `SMRFixPack.StormWedgeHeal` | ✅ `:154` **and re-armed `:165`**, resetting `g_MeteorStormStop` before it returns |
| 5 | `Fix_RainsDeadlock:195` | ⭐ **`RainsDisasterLoop` — a vanilla global** | n/a by construction: no mod code is in that thread |
| 6 | `Fix_BombardmentSpread:137` | our closure | ⛔ **none** |

⭐ **D13 §3's open Rule-6f routing is DISCHARGED and nothing on record says so.**
That routing named E5/E6/E7 (`CrystalMysteryHang`, `ExtenderFlapChurn`,
`TrackConnectorPingPong`) as having **no** gate. All three carry one today, each
module's header dating the rewrite to 2026-08-13. Re-derived by reading, not by
trusting the headers.

Site 6 is the one un-gated mod closure, and it has a recorded disposition (D13
E3, accepted): its body touches only vanilla names — `AddObjectToNotification`,
`Msg`, `PlayFX`, `WaitMsg`, missile methods, `map.g_IncomingMissiles` — so an
orphan **completes the volley and cleans up after itself** (`:152-153`) rather
than stranding state. Disposition unchanged; re-derived, not inherited.

## 5 · ⛔ There is no layer-1 tear-down anywhere in the pack

**0 registrations of `OnMsg.SaveGameStart` and 0 of `OnMsg.SaveGameDone`**, over
all 76 files, mechanically.

`FIX_POLICY` §3a layer 1 offers exactly that hook for *"what layers 3 and 2
cannot reach"*, with the instruction *"build it last, and only for what survives
the other two layers"*. Zero usage is therefore a **positive result**, not a gap:
the pack concluded that nothing needed it. But it has a consequence worth stating
in one sentence, because it is what "aggregate save footprint" actually means
here:

> ⭐ **Nothing is torn down before a save. The pack's save footprint is, exactly
> and only, whatever is live at the moment the player saves** — which for the
> capturable half means "however many of the six game-time threads happen to be
> awake", and there is no upper bound in the code that a reader can point to.

## 6 · The 18 load-time passes, in the order they actually run

`OnMsg` is additive (`cthreads.lua:64-72`), so every one of these registers; the
run order is registration order, which is `metadata.lua` `code` order. `LoadGame`
fires before `FixupSavegame`, `PostLoadGame` after it
(`CommonLua\Savegame.lua:810-813`).

| # | msg | module | entry |
|---|---|---|---|
| 1 | PostLoadGame | `Fix_MeteorFrequency:164` | F02 |
| 2 | LoadGame | `Fix_BrokenTrackSalvage:56` | F45 |
| 3 | LoadGame | `Fix_TrackSalvageWipe:304` | F44 |
| 4 | LoadGame | `Fix_GhostFarmOxygen:51` | F37 |
| 5 | LoadGame | `Fix_CrystalMysteryHang:109` | F06 |
| 6 | LoadGame | `Fix_DestroyedTunnels:58` | F38 |
| 7 | LoadGame | `Fix_DustSicknessBiorobots:167` | F40 |
| 8 | LoadGame | `Fix_IndependenceTerraforming:171` | F18 |
| 9 | PostLoadGame | `Fix_DisasterPredictionLeak:108` | F81 |
| 10 | PostLoadGame | `Fix_MeteorStormWedge:217` | F78 |
| 11 | PostLoadGame | `Fix_RainsDeadlock:210` | F81b |
| 12 | LoadGame | `Fix_FirstAsteroidPrefabs:256` | F83 |
| 13 | LoadGame | `Fix_SaintBlessing:151` | F92 |
| 14 | LoadGame | `Fix_AstrogeologistExtractors:174` | F95 |
| 15 | LoadGame | `Fix_ExoticDepositSign:84` | F102 |
| 16 | PostLoadGame | `90_SaveSanitizer:325` | F35+F03+F48 |
| — | PostLoadGame | `Fix_TrackTunnelPowerBridge:157` | F65 — registered **inside `apply()`** |
| — | PostLoadGame | `Fix_TrainMinors:133` | F49 — registered **inside `apply()`** |

### 6.1 The `SavegameFixups` gating, re-derived

`FixupSavegame` (`CommonLua\SavegameFixup.lua:24-50`) walks
`sorted_pairs(SavegameFixups)` — **alphabetical**, which is why the devs named one
`A_StationConnectorElements3` — and runs each only `if not
AppliedSavegameFixups[fixup]`. **`AppliedSavegameFixups` is itself a `GameVar`
(`:10`)**, so the table is per save lineage and each of the **237** shipped
fixups runs **once**, on the first load of a save that predates it.

⇒ the "our `LoadGame` pass runs before a shipped fixup" hazard — which
`90_SaveSanitizer:315-324` documents, having been bitten by it once (the F35
double-buff, found by the wave-3 QA audit 2026-07-25) — is live on **exactly one
load per save**: the first load of a save old enough to still owe that fixup.
That is precisely the population the repair passes target, so the hazard is not
theoretical.

### 6.2 What was checked for interference, and what was not

⭐ Five modules mutate track state at load time (#2, #3, #16, and both nested
rows), which is the densest cluster and the one a per-module review cannot see.
Read at Src:

* `SavegameFixups.SyncTracksAndElements` (`TrackElement.lua:845-867`) deletes
  `TrackGridElement`s whose `track_obj` is invalid — **the same act** as
  `Fix_TrackSalvageWipe`'s `LoadGame` pass (`:307-312`). Ours runs first, so the
  fixup finds nothing; **redundant, not conflicting.**
* `SavegameFixups.RemoveTrackDoubleTurns` (`:839-843`) calls
  `ProcessTrackElements(ResolveMap(track), track.elements, track.elements[1])`
  on every track. `OrderTrackElements` (`Tracks.lua:520-639`) does **not** sort
  by `node_idx` — it walks the hex grid and renumbers at `:632-633` — so the F45
  `false < number` sort defect is **not** reachable through it. ⛔ A hypothesis
  that the SaveSanitizer's F48 pass could trip the F45 defect was formed and
  **refuted** at source; it is recorded here so it is not re-formed.
* F48's own decision to run at `PostLoadGame` rather than `LoadGame` is correct
  for the reason its header gives, and the gating in §6.1 is what makes that
  reason load-bearing.

⛔ **Not checked:** the other 13 passes were not each cross-read against the 237
shipped fixups. The clusters that remain unswept for interference are
meteors/storms (#1, #10), rains/disasters (#9, #11) and the three preset-patch
heals (#8, #13, #14). Those go in the ledger's unreached column.

## 7 · ⭐⭐ The exit, in one law

Every persisted name of ours, and whether it is still there after the player
removes the pack and saves again. **`OnMsg.PersistSave` writes `data[k]` for
every key of `PersistableGlobals`, and `OnMsg.PersistLoad` restores only keys of
`PersistableGlobals`** (`CommonLua\Core\persist.lua:119-143`, read this session).
`GameVar` is what puts a name in that table — and `GameVar` only runs when our
file loads.

| name | carrier | carrier registered by | survives a save made without the pack |
|---|---|---|---|
| `SMRFixPack_MeteorLatch` | **our** GameVar | us | ❌ **dropped** |
| `SMRFixPack_FirstAsteroidPrefabs` | **our** GameVar | us | ❌ **dropped** |
| `SMRFixPack_loop_version` | field in a `RainsDisasterThreads` entry | vanilla | ✅ |
| `SMRFixPack_fixed_loop` (legacy) | same | vanilla | ✅ — the pack clears it as entries migrate |
| `SMRFixPack_reserved_at` | Colonist field | vanilla | ✅ |
| `SMRFixPack_shelter_try` | Colonist field | vanilla | ✅ |
| `SMRFixPack_payload_set` | transporter field | vanilla | ✅ |
| `SMRFixPack_rocket_fuel_key` (legacy) | DroneControl field | vanilla | ✅ — the module deletes it |
| `SMRFixPack_spawn_gate` | descriptor copy in a scheduler-thread local | vanilla | self-replaces within one wave |
| `SMRFixPack_F35_<label>` | LabelModifier on the colony | vanilla | ✅ — **the residue is the repair** |
| `SMRFixPack_F48_StationConnectors` | `UIColony` field | vanilla | ✅ |
| **`smr_shuttles`** | entry in `g_TransportationModeToCommunityCache` | vanilla | ✅ until the next cache flush |

> ⭐ **THE LAW, and it has not been stated anywhere: a persisted name of ours
> survives uninstall if and only if its CARRIER is vanilla's. The only two that
> vanish are the two whose carrier is a `GameVar` we registered ourselves.**

This is the exact inverse of what one shipped module header says, and §8 is that
finding.

## 8 · The consequences of the law that nobody has drawn

### 8.1 A shipped header states the mechanism backwards

`Fix_MeteorFrequency:36-37` discloses, as an accepted residual: *"the
SMRFixPack_MeteorLatch GameVar stays in the save after uninstall as inert
data."* By §7 it does the opposite — it is not restored on a load without the
pack and is not written into the next save. The same file repeats it at `:69-70`.

⚠️ **Precisely:** the save file the player already has still physically contains
the value in its blob; it is dropped at the first save written without the pack,
and is invisible to the game before then. So the header is not merely imprecise —
it discloses a residual the pack does not leave.

⭐ **The pack contains both the wrong and the right statement of the same
mechanism.** `Fix_FirstAsteroidPrefabs:95-101` gets it exactly right, citing
`persist.lua:135-142`. The player-facing route is also already correct:
`RELEASE_UNINSTALL_ASSEMBLY.md` §1 records *"the one version-stamped name is
dropped by the engine on the first load without the pack."* ⇒ **the defect is
confined to a shipped code comment; no player surface repeats it.**

### 8.2 The meteor heal's stated invariant is not what the mechanism delivers

`Fix_MeteorFrequency:42-51` promises *"one restart per save lineage per
version"*: the latch holds the last-healed pack version, and a version bump
re-heals once. By §7 the latch is erased by any save written without the pack.

⇒ on the **uninstall → play → save → reinstall** route (and on the Mod-Manager
disable → enable route that spans one save — `EF-002`'s state (4), and `D13`'s),
the latch reads `false ≠ version`, the heal runs again, and
`RestartGlobalGameTimeThread("Meteors")` **re-rolls the 35–115 h meteor timer**.

**Severity, stated fairly:** that is one re-roll per reinstall cycle, not per
load. F88 — the defect this design exists to prevent — was one re-roll **per
load**, which is what made it silent and permanent. A single re-roll on reinstall
is bounded, arguably even correct (a reinstall *should* clear persisted old
bodies). ⛔ **Not harmful, not launch-blocking.** What is wrong is the stated
invariant: the guarantee is per save lineage per version **per continuous
installation**, and no record says so.

### 8.3 `90_SaveSanitizer`'s F48 latch is set before its work, not after

`:337-342`:

```lua
if type(colony) == "table" and not colony[F48_FLAG] then
    colony[F48_FLAG] = true
    ok, err = pcall(repair_station_connectors)
```

`repair_station_connectors` has a **decline** branch (`:249-252`) that returns 0
and logs when `ProcessTrackElements`/`ResolveMap` are not found as globals — the
deliberate "a game update moved them, decline rather than deactivate F35 and F03"
design. The flag is already `true` by then, and it lives on `UIColony`, so the
decline is **permanent for that save**: a later pack build that handles the moved
API would find the flag set and never run.

The same is true of a raise the `pcall` swallows. The flag's own stated contract
(`:212-214`) is *"a save this pass has already re-ordered is never re-ordered
again"* — but it is also set on a save the pass **declined to re-order**.

⚠️ Reachable only after a game update moves those two globals, so it is latent,
and F35/F03 are unaffected either way. The one-line shape that would fix it —
set the flag on the success path — is a code change, and this link is record-only.

## 9 · `90_SaveSanitizer`'s scoping header is stale in both directions

`:5-7`: *"Fixes with a live half carry their own LoadGame pass in their own file
(F02, F45, F37, F58, F06, F38, F39, F40). This module is for the remainder."*

Measured against the tree (§6): **17** modules carry a load-time pass, not 8.

* **11 unlisted:** F44, F18, F81, F78, F81b, F83, F92, F95, F102, F65, F49.
* **F39 has no module in `Code/` at all** — the id appears in the shipped tree
  only inside this comment; `bugs/INDEX.md` records it `folded`.
* **F58's pass is `OnMsg.NewDay`** (`Fix_StaleReservations:59`), not a load pass.

The sentence is a scoping note, not a coverage claim, so nothing behaves wrongly.
But it is a factual list inside shipped code that is wrong in both directions,
and it is the only place a reader is told where the boundary of this module sits.

## 10 · What this document does not claim

* ⛔ Not *"the save footprint is N bytes"*, and not *"measured"*. Nothing here
  was read off a real save this session. The measured provenance in the D-row
  table belongs to the D13 chain, is cited as theirs, and was not re-taken.
* ⛔ Not *"the pack is save-safe in aggregate"*. §5 is the honest form of that
  question: nothing is torn down, so the footprint at any save is whatever is
  live, and the six game-time threads' simultaneous liveness has never been
  measured by anything.
* ⛔ Not a claim that the 18 load passes do not interfere. Three were checked
  against the shipped fixups; the rest are in the ledger's unreached column.
* ⛔ Not a re-derivation of D13's **measured** object counts (D5's 1257/1260/1336,
  D12–D15's round trips). Those need a running game.
