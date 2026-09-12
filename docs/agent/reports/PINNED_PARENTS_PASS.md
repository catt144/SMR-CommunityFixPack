# The pinned-file `__parents` / `DefineClass` pass — checklist 163 (b), option (i)

**Ran and finished 2026-09-12** (`smr-bugfixpack-2e`). Commissioned by the owner's ruling of checklist
**163 (b)** — *"yes, take it"* — on the recommendation of `VANILLA_DIFF_DISPOSITION.md` §1b, which priced
option (i) at one desk session and listed ~8 rows to read.

⭐ **VERDICT: nothing found. No row changes what our hooks see, and no defect is filed.**
⇒ **Option (ii) is NOT triggered.** §1b's own rule is *"do it only if (i) finds anything"*, and (i) found
nothing. The full ≥1,281-hunk pass (option (iii)) was already recommended against and stays that way.

⚠️ **Two of the seven rows were WRONG IN THE REPORT THAT LISTED THEM.** See §3. Neither error changes the
verdict, but both matter for `HUNT_AUDIT` §8 item 2 (the `TABLE-HUNK` list `treediff` is supposed to grow),
because they are errors the *classifier* made, not a human.

---

## 0 · Cost, stated because the estimate was the reason this ran

Priced at "one desk session, both archives already on disk". **It took about fifteen tool calls.** The
reason is worth recording for the next pass of this kind: **the decisive question is a set intersection,
not a reading task.** "Does a new parent change what our hooks see?" decomposes into two mechanical tests —

1. does the new parent define a **method name we hook**? (name collision re-routes lookup)
2. does it define `Init` / `GameInit` / `Done`? (composition chain, `EF-058` / `EF-066`)

— and both are greps against two generated lists. Reading was needed only where a test came back positive
or where the report's own row was unsettled. ⛔ **Do not budget the next one as a reading pass.**

**Our surface, harvested from `Code/*.lua`:** 100 `(class, method)` target lines, **83 distinct method
names**. (`VANILLA_DIFF_DISPOSITION.md` says 105 targets; the difference is not material to this pass and
was not chased.)

## 1 · The rows, and what each resolved to

| # | row (as listed in §1b) | verdict |
|---|---|---|
| 1 | `Unit.lua` `__parents` gains `"ReactionObject"` | ✅ **CLEAN** |
| 2 | `BaseBuilding.lua` `__parents` gains `"ReactionObject"` | ✅ **CLEAN** |
| 3 | `WaterExtractor.lua` gains `"ContinuousOps"` | ✅ **CLEAN** |
| 4 | `Farm.lua` `FarmBase` **loses** `"InteriorAmbientLife"` | ✅ **CLEAN** |
| 5 | `Fireflies.lua:650` `Service` → `DecorationService` | ✅ **CLEAN** — and strictly additive |
| 6 | `Residence.lua` two `__parents` hunks, ⚠️ **UNSETTLED** in the report | ✅ **RESOLVED — re-composed, not re-scoped** |
| 7 | `Station.lua` new `DefineClass.TrainStationDepotCCP3`, `__parents = {"Door"}` | ⛔ **FALSE POSITIVE — see §3** |

### Rows 1–2 · `ReactionObject` onto `Unit` and `BaseBuilding`

The two rows the report flagged hardest, being the base classes of every colonist, drone, rover and
building. `DefineClass.ReactionObject` is `CommonLua/Reactions.lua` and defines **12 methods**.

- **Name collision with our 83 hooked method names: ZERO.**
- **Defines no `Init`, `GameInit` or `Done`** ⇒ it does not enter the composition chain at all, which is the
  mechanism `EF-058`/`EF-066` describe.

### Row 3 · `ContinuousOps` onto `WaterExtractor`

`Lua/Buildings/ContinuousOps.lua`, **7 methods**: `IsContinuousOpsEligible`, `ApplyContinuousOpsBonus`,
`RemoveContinuousOpsBonus`, `GetContinuousOpsProducerBonus`, `GetContinuousOpsProductionBonus`,
`GetContinuousOpsWaterBonus`, `BuildingUpdate`. **Zero collisions**, no `Init`/`GameInit`/`Done`. Our pin in
that file is `WaterExtractorBase:OnSetWorking` (`Fix_SilentHitMomentFX`), which is not among them.

### Row 4 · `Farm` loses `InteriorAmbientLife`

A **removal**, so the question is the opposite one: did we depend on what left?

- `InteriorAmbientLife` is **deleted tree-wide in 1.1.0** — the name returns nothing in `Lua/`,
  `CommonLua/` or `Data/`, and `Lua/Buildings/InteriorAmbientLife.lua` no longer exists. ⚠️ Checked as a
  *disappearance*, not inferred from the old name's absence in one file (that mistake has cost this project
  before): the 1.0.7 definition was located first, then its absence confirmed tree-wide.
- It provided exactly **two methods**: `AttachToSpotIdx` and `InitAmbientLife` — decorative interior life.
- **We reference neither**, in `Code/` or in the Test Kit.
- Our pin in that file is `FarmBase:ApplyOxygenProductionMod` (`Fix_GhostFarmOxygen`), unrelated.

⚠️ **`Fix_GhostFarmOxygen` is still shipping today.** Checklist 156 ruled it retires, but that retirement is
staged for v10 and has not landed — the module is in `Code/` and in `items.lua` as of this pass. So this row
was checked as live, not waved off as moot.

### Row 5 · `Fireflies` — `Service` → `DecorationService`

The re-parented class is `FlowerLamp` (`Lua/Mysteries/Fireflies.lua:649-651`). And the change is **strictly
additive**: `DecorationService.__parents = { "Decoration", "Service" }` (`Lua/Buildings/Decoration.lua:6-8`),
so `FlowerLamp` keeps everything `Service` gave it and gains `Decoration`. Our target in that file is the
**global** `SetLightTrapMode` (`Fix_WispRewards` replaces it, a copy of `:674-701`), which references neither
`FlowerLamp` nor `Service`. Its `SRC:` pin is `OK` on today's `bodycheck`, so the shipped body is unchanged.

### Row 6 · `Residence` — the unsettled one, and the one with the most exposure

The report left this **⚠️ UNSETTLED** (*"the block shifted; I did not resolve which parents actually
moved"*), and it is where the pack is most exposed: we hook **4 Residence methods** and **6 `Building`
methods**. Resolved:

| tree | `Residence.__parents` | the stats parent |
|---|---|---|
| **1.0.7** | `{ "StatsChange", "Holder" }` | `StatsChange.__parents = { "StatsChangeBase", "Building" }` (`Service.lua:55-57`) |
| **1.1.0** | `{ "StatValues", "Building", "Holder" }` | `StatValues.__parents = { "PropertyObject" }` (`Stats.lua:10-11`) |

⇒ **`Building` moved from a TRANSITIVE ancestor to a DIRECT parent**, and the stats parent was swapped for
one that no longer drags `Building` behind it. **`Building` is in `Residence`'s ancestry in BOTH trees** — our
`Building` hooks reached Residences before this change and still do. Our four Residence targets
(`CheckHomeForHomeless`, `GetFreeSpace` — `Fix_FreedHousingNotice`; `ReserveResidence`,
`CancelResidenceReservation` — `Fix_StaleReservations`) are all defined **on `Residence` itself**, so lookup
resolves them first either way.

**Residual, named rather than cleared:** the *order* of resolution changed, and `StatsChangeBase` left the
ancestry. We hook nothing in `StatsChange`, `StatsChangeBase` or `StatValues`, so neither is reachable from
our surface — but "order changed" is a real difference and this pass did not enumerate every name defined in
more than one ancestor.

## 2 · Our `Station` "targets" are not method hooks

Worth recording because it shrinks the exposure the report attributed to us: both `Station` entries
(`Fix_TrainWaitTime.lua:88`, `Fix_TrainsToVoid.lua:44`) are **class-existence checks** —
`{ class = "Station", reason = "Station class not found (game update changed it?)" }` with **no `method`
field at all**. They assert the class exists; they hook nothing on it.

## 3 · ⛔ Two errors in the row list itself — for `HUNT_AUDIT` §8 item 2

Row 7 as published reads: *"new `DefineClass.TrainStationDepotCCP3`, `__parents = {"Door"}` — additive on
today's read."* **Both halves are wrong**, and neither is a judgment call:

1. **It is not new.** `TrainStationDepotCCP3` exists in 1.0.7 at `Station.lua:7` and in 1.1.0 at `:9`. The
   block **moved down two lines**; nothing was added. It is also referenced by 1.0.7's own
   `Station.lua:1084`, so it was live code, not a stub introduced by the patch. Its comment — *"kept here for
   savegame compatibility"* — says the same thing.
2. **Its parent is not `Door`.** It is `__parents = {"BuildingEntityClass"}`. The `{"Door"}` classes nearby
   are `TrainStationDoorCCP3` and `TrainStationLargeDoor1CCP3` (`:14`, `:19`) — **both also present in
   1.0.7** (`:12`, `:17`). The row conflated adjacent `DefineClass` blocks.

⇒ **The whole `Station` row is a line-shift artefact.** Nothing in it is new in 1.1.0.

⭐ **The transferable finding, and it is the useful output of this pass:** the unaccounted-hunk classifier
reports **pre-existing blocks that merely moved** as new declarations, and attributes `__parents` across
adjacent blocks. Any `TABLE-HUNK` list `treediff` grows must therefore **compare content between trees, not
position** — a hunk that is only a line shift has to be filtered before a human is asked to read it, or the
list will spend reader attention on rows like this one. Three of the seven rows here cost nothing to check;
this one cost the most and contained no change at all.

## 4 · What this pass did NOT do

⛔ Stated so nobody reads a wider clearance out of it.

- It is a **name-collision and composition** test. A parent that changes the *behaviour* of a method we do
  not hook but depend on would not show up here. That is what option (ii) is for, and (ii) is not triggered.
- It covers the **7 rows §1b listed**, not all **157** unaccounted hunks in the 29 pinned files, and not the
  ≥1,281 tree-wide.
- Row 6's resolution-order residual is named, not measured.
- No game was launched. No `Code/` file changed. Nothing was re-pinned.
