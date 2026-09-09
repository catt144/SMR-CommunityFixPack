# 1.1.0 audit — every finding re-derived, and the safety triage

Audit run 2026-09-08, same day as the patch, against the shipped 1.1.0 tree.
Companion to `GAME_1_1_0_IMPACT.md`, which it audits. **32 of 32 claims PASS.**

> ⚖️ **WHY THIS DOCUMENT EXISTS.** The owner's rule — a dev "Fixed" line is a
> claim until we confirm it — applies to **our own findings too** (`recorded
> facts are claims`). Every assertion in the impact report was re-derived here
> from scratch, by a script that re-runs the harvest and re-greps the tree rather
> than re-reading the report. ⚠️ **This is a same-context self-audit and is
> therefore the WEAKER kind.** It catches arithmetic, scope and inherited-claim
> errors — it did catch two — but it cannot catch a framing error I made twice.
> A fresh-context adversarial pass is still owed and is step 0 of the "fix later"
> work.

## 1 · Verdict table

Script: `scratchpad/audit.py` (re-derive it, do not trust a stale copy). It
re-harvests the pack's targets, re-walks the 4715-file tree, and asserts each
claim independently — including negative controls, so a broken grep fails loudly
instead of silently "confirming" everything.

| # | claim | verdict |
|---|---|---|
| A1 | rig `buildid` = 24995074 | ✅ PASS |
| A2 | `Src` overwritten (2747 of 4715 `.lua` re-dated) | ✅ PASS |
| B1 | exactly 1 of 107 class/method targets missing | ✅ PASS |
| B1a | …and it is `Colonist.UpdateSatisfaction` | ✅ PASS |
| B2 | `PropertyObject.GetProperty` present (assignment form) — false alarm | ✅ PASS |
| B3 | `HolidayRating:RewardApplicants` present — false alarm | ✅ PASS |
| B4 | 5 globals gone (`GatherTransportableResources`, `GetCommandCenterLifeSupportGrids`, `GetGridGlobalStorage`, `PlanetaryAsteroidVisitPossible`, `RainsDisasterLoop`) | ✅ PASS ×5 |
| B5 | 3 consts gone | ✅ PASS ×3 |
| B5c | **negative control** — `ColonistMaxDomeWalkDist` still declared | ✅ PASS |
| C1 | `ModMinLuaRevision` == our `lua_revision` (350453) | ✅ PASS |
| C1a | `IsObsolete` uses a strict `<` | ✅ PASS |
| D1 | `IsOvertime` collapses the table to a boolean | ✅ PASS |
| D1a | `GetWorkersPerformance` calls `IsOvertime` | ✅ PASS |
| D1b | our code still indexes `self.overtime[shift]` | ✅ PASS |
| D2 | 1.1.0 takes `Max(workers, auto_performance)` | ✅ PASS |
| D2a | early auto-return only when `max_workers == 0` | ✅ PASS |
| D3 | `law_scale` gone tree-wide | ✅ PASS |
| D3a | `automation_workforce_reduction` only in `LawDef/` data | ✅ PASS |
| D3b | the 3 automation law ids still exist | ✅ PASS |
| D4 | `GetEarthExportResPossibleReward` absent from **everything** | ✅ PASS |
| D4a | replaced by `GetEarthAutomodeFundingState` | ✅ PASS |
| D4b | `HourlyUpdate` → `CreateAutoCargoRequest` when landed + automode | ✅ PASS |
| D4c | exactly 3 `CreateAutoCargoRequest` definitions | ✅ PASS |
| D4d | our fix is a full replacement of the base (no `orig`) | ✅ PASS |
| E3 | `self.overtime` is the **only** abandoned table field | ✅ PASS |
| E4 | count of no-`orig` definers | ⚠️ **CORRECTED — see §2c** |

## 2 · What the audit CHANGED

Two things, both worth more than the 32 passes.

**⚠️ 2a · F113's blast radius was overstated, and is now corrected.** The first
filing implied every automatic rocket. 1.1.0 defines `CreateAutoCargoRequest` in
**three** places, and the two subclass versions — `LanderRocketBase`
(`Lua/Buildings/LanderRocket.lua:639`) and `SpaceElevatorBase`
(`Lua/Buildings/SpaceElevator.lua:206`) — are **full overrides that never call
the base**. We replace the base only. So landers and the Space Elevator are
**not** affected; the seven `__parents = { "UniversalRocketBase" }` classes
(`UniversalRocket`, `UniversalDragonRocket`, `UniversalTradeRocket`,
`UniversalZeusRocket`, `UniversalRefugeeRocket`, `UniversalLanderRocket`,
`UniversalPod`) **are**. Narrower than claimed, still the ordinary Earth-supply
fleet, still not an edge case. `F113` has been amended.

⚠️ A second-order consequence worth its own line: because those overrides bypass
our replacement, **F68/F71's repair no longer reaches landers or the Space
Elevator at all** — whether it ever did on 1.0.7 is unverifiable now that the
source is gone. That is a re-derivation question, not a safety one.

**✅ 2b · An inherited claim was caught and re-derived.** "Re-run every hour
while landed" came from **our own 1.0.7-era header comment** — exactly the kind
of borrowed assertion the project has been burned by. Re-derived against 1.1.0
and it holds: `UniversalRocketBase:HourlyUpdate` (`Lua/UniversalRocket.lua:1556`)
runs `IsRocketLanded()` → `IsAutoModeEnabled()` → `CreateAutoCargoRequest()`.
Likewise the trigger guard: `GetArrivalLocType()` reads
`arrival_loc.spot_type` (`:952`), `"earth"` is a live spot type, and
`PlanetaryView.lua:331` branches on `spot_type == "earth" and
rocket:IsRocketLanded()`. ✅ And the `and` short-circuits, so a rocket not at
Earth never evaluates the dead call.

Also confirmed, closing a gap the impact report left open: **C39 really does
fire on 1.1.0.** `find_automation_law` needs `self.modifications.max_workers`,
`ActiveLaws`, and law effects carrying `Prop = "max_workers"` — all three
present (`LawDef-Technology.lua:14`, `:107`, `:194`; `ActiveLaws` in 76 files,
`modifications` in 25). So F112 is live, not theoretical.

**⚠️ 2c · THE "31 FULL REPLACEMENTS" FIGURE WAS WRONG, AND THE CORRECTION IS NOT
A BETTER NUMBER.** The detector tested `\borig\b`, which does not match
`orig_update_end` — so chained wrappers using an `orig_<something>` upvalue were
misfiled as replacements. Re-run with `\w*(orig|prev|base_fn|inner)\w*`: **12
flagged (~11 vanilla, `00_Core.lua` being the pack's own core)**, not 31.
⛔ **But the detector errs in BOTH directions**: `Fix_TrackConnectorPingPong`
carries a full body copy of `CreateConnectorElements` and still classifies as
"chained" because the word appears elsewhere in the file. So the true population
of body-copies is **somewhere between ~11 and ~31 and cannot be settled by any
regex** — it needs a per-module read. Recorded as a caution against the next
tempting one-line classifier, not as a replacement number.

**⛔ 2d · A PLAYER FOUND A BREAKAGE EVERY SWEEP HERE PASSED.** [[F114]] arrived
while this audit was being written: trains do not move between stations with the
pack loaded on 1.1.0, reporter-run A/B. Every instrument in §1 is **clean on
every train/track module** — targets resolve, no dead calls, `recompute_max_vehicles`
byte-identical to 1.1.0's formula, `CreateConnectorElements` a line-for-line match
bar its own F66 guard. The sweeps measure existence and call validity, never
behaviour. ⛔ **From here on, "the sweeps are clean" says nothing about
correctness** — and F114 outranks everything in §3 because it is the only item a
real player has actually hit.

## 3 · FIRST FIXES — get back to safety

The bar for this tier: **the pack is actively doing something wrong on 1.1.0
right now.** Not "might be wrong", not "needs re-checking". Four qualify — and
the first is not a fix at all.

**FF-0 · [[F114]] — the trains field report. Ranked first, and deliberately NOT
given a repair.** A player has hit it; nobody has hit FF-1..3. But no cause is
pinned, every desk sweep passed clean on that surface, and there is no player
module toggle to bisect with — so the first-tier action is **narrowing**
(reproduce, bisect agent-side, ask for the log), not shipping. ⛔ A speculative
train repair is the single worst thing available here.

Every recommendation below is deliberately the *smallest* change that stops the
harm, invents no behaviour, and is `FIX_POLICY` §3a **Layer 2** (nothing
persisted, class-table only, uninstall-clean). ⛔ None of them decides whether a
fix is retired — that is decision **99**, the owner's.

### FF-1 · `F113` — stop the hourly throw (P1)

**Harm:** throws every hour on an automode rocket landed at Earth, after the
cargo request is written, so the low-funding auto-stop is lost; and silently
reverts a function 1.1.0 rewrote.

**Fix — add one spec to `Fix_LanderCargoRatchet`'s `Require` list:**

```lua
{ class = "UniversalRocketBase", method = "GetEarthExportResPossibleReward",
  reason = "the Earth export-reward query is gone (game update changed it?)" },
```

**Why this shape.** It is the pack's own designed failure mode: the module
declines to install rather than installing a body that raises. It also kills the
silent revert in the same stroke, which a targeted repair of the call would not.
⚠️ Use the `{class, method}` form, **not** a `{ test = … }` — `Require` sets
`update_suspect` for shape failures but deliberately not for `test` entries, and
this *is* patch rot that should be flagged for the update report.

⛔ **Do NOT instead swap the call to `GetEarthAutomodeFundingState`.** That fixes
the throw and leaves the whole-function revert in place — the larger harm.

### FF-2 · `F111` — stop the boolean-index throw (P2)

**Harm:** throws when a staffed automated metals extractor has overtime on any
shift, because 1.1.0's `IsOvertime()` collapsed `self.overtime` to a boolean
under our reconstruction.

**Fix — one line in `staffed_performance` (`Code/Fix_ExtractorStaffedPerformance.lua:68`):**

```lua
-- was:  if self.overtime and self.overtime[shift] then
if type(self.overtime) == "table" and self.overtime[shift] then
```

**Why this shape.** ⭐ It is **assumption-free** — correct on 1.0.7 (table) and
on 1.1.0 (boolean) alike, needs no version detection, and changes no outcome on
either. A gate that self-disables the module would *also* be defensible, since
the audit confirms 1.1.0 fixed F108's defect upstream — but that is a retirement
decision, and this tier only stops the harm. Take the one-liner now; let 99 rule
on retirement.

### FF-3 · `F112` — stop the silent over-payment (P2)

**Harm:** not a crash — worse in one way. C39 pays an automation-law uplift that
1.1.0 gives **nobody**, so the 8 out-of-class families become the only
compensated buildings in the game. Player-visible, silent, in any colony running
an automation law.

**Fix — gate the module on the 1.1.0 shape so it self-disables:**

```lua
{ test = function()
        -- C39 corrects an asymmetry in vanilla's law_scale compensation.
        -- 1.1.0 deleted that compensation outright (`law_scale`: 0 hits
        -- tree-wide) while the laws still cut max_workers, so paying the
        -- out-of-class families would CREATE the asymmetry this fix removes.
        local W = rawget(_G, "Workplace")
        return not (type(W) == "table" and type(W.GetWorkersPerformance) == "function")
    end,
  reason = "vanilla no longer compensates the automation-law worker cut for anyone (1.1.0) — nothing to correct" },
```

**Why `test` here and not `{class, method}`.** This is an "already handled?"
content check, which is precisely what `Require`'s comment reserves `test` for —
and it correctly does **not** raise `update_suspect`, because the module going
quiet here is healthy, not rot.

⚠️ **THE ONE ASSUMPTION IN THIS TIER, STATED PLAINLY.** The discriminator is
"1.1.0 extracted the per-worker loop into `Workplace:GetWorkersPerformance`",
inferred from our own F108 header, which describes 1.0.7's loop as *inline* at
`Workplace.lua:219-228`. **That inference cannot be verified — the 1.0.7 source
is gone from disk.** Bounded downside if it is wrong and 1.0.7 also had that
method: C39 self-disables on 1.0.7 too, returning those players to vanilla's
known asymmetry — the pre-fix state, not a new harm. Acceptable, but **re-check
it the moment a 1.0.7 branch exists** (decision 98).

## 4 · FIX LATER — everything else, in priority order

⛔ None of these is safe to guess at, and none is urgent in the way §3 is.

1. **A fresh-context adversarial review of the impact report + this audit**
   before any of the below is acted on. §0's caveat is why.
2. **The body-copy modules** (§2c: ~11 confirmed full replacements, and an
   unknown number of chained wrappers that still embed a copied body). The
   highest-yield target in the project. Each substitutes a 1.0.7-era body for
   whatever 1.1.0 ships, and F113 proves the class is real. ⛔ A replacement whose
   calls all still resolve is invisible to every sweep in these two reports — and
   ⛔ **the count cannot be settled by a regex**; they must be read one by one.
3. **The 6 self-disabled modules** (F09, F12, F22, F81, F94, F55/F57): does the
   underlying defect still exist in 1.1.0? Only F09 is settled, and by a fact.
4. **Disposition rulings** — decision 99, covering F108/F111, C39/F112,
   F68/F71/F113, and the six above.
5. **The redesigned-systems list** (`GAME_1_1_0_IMPACT.md` §3): F04, F20, F92,
   the landscaping group, F90, F08.
6. **The §2 claim table** — 13 rows, one control each, lowest priority precisely
   because it is built on dev claims.
7. **The live `SMRFixPack.ListFixes()` read**, which supersedes every prediction
   in both reports. Gated on decision 98.

## 5 · What this tier does NOT do

⛔ It does not decide whether any fix is retired. ⛔ It does not touch
`items.lua` (no module is added, renamed or dropped, so `H-10` is not engaged).
⛔ It does not bump `version` and no agent opens the Mod Editor (`H-02`).
⛔ It does not re-upload: three gated modules do not justify a release cycle,
and shipping on a two-probe audit is the expensive mistake `GAME_1_1_0_IMPACT`
§5 warns about. The build brief is `prompts/SAFETY_FIRST_FIXES.md`.
