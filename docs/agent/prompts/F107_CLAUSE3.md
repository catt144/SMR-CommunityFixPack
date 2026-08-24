# Prompt — add clause 3 to `LandscapeCostGuard` (the widening, measured)

Self-contained. Written 2026-08-24, after F107 was repaired (checklist 74(a),
commit `f6eba26`). **Instrument work only — you write NO `Code/*.lua` in the fix
pack.** Everything you touch is in the TestKit repo.

## Todo list — REQUIRED, update immediately per item

Open a todo list as your FIRST action, one entry per numbered step in §5, and
mark each done the moment it is done. The owner reads that list to decide when
to step in. Do not batch updates to the end.

## 1. Why this exists

`Fix_LandscapeCostRefresh` (fix pack, `Code/Fix_LandscapeCostRefresh.lua`) used
to install on three landscape LEAF classdefs and captured `prev` off each of
them. None declares the method, so `prev` was nil on every boot and the
delegation half was dead code that raised if reached — **F107**, measured.

The repair installs ONE chained wrap on `ConstructionSite`, the only class in
the tree that declares `RefreshConstructionResources`
(`Src/Lua/Buildings/ConstructionSite.lua:665`). The class builder copies it into
all 13 descendants, so the three leaves keep the guard by inheritance.

⇒ **The guard now runs for every construction site, not just landscape ones.**
That widening is a behaviour surface. The owner ruled it in. Two independent
static derivations (the 08-24 terminal audit, and the session that built the
repair) agree it can only ever prevent an error — **but both are READINGS of the
source. Nothing has ever executed that path with the pack loaded.** Clause 3
closes exactly that gap and nothing else.

## 2. The file, and what is already there

`C:\Dev\SMR-BugFixPack-TestKit\Code\64_Probes_Wave14.lua`, probe
`SMRTest.Register("LandscapeCostGuard", …)` (≈ line 467).

It loops `COST_LEAVES` (the three landscape classes) and per class runs:

* **clause 1** — `site_for(cls, false)`: `construction_costs_at_start = false`,
  the field state. The call must return without raising. Prints
  `SMRTEST-F105GUARD <cls>: unguarded-state call ok=<bool>`.
* **clause 2** — `site_for(cls, { WasteRock = 0 })`: a real cost table. The call
  must reach vanilla and do vanilla's work — `SetAmount(90)` and
  `construction_costs_at_start.WasteRock == 50` afterwards.

⛔ **Do not renumber, reword or restructure clauses 1 and 2, and do not change
their printed strings.** F107's entry and `reports/F106_DISPATCH_SWEEP.md` quote
them verbatim as the measurement of record.

## 3. What clause 3 must do

The same two states, on **`ConstructionSite` itself** — an ordinary building's
construction site, not a landscape one.

**3a — ungathered ordinary site.** Fields: `construction_resources = false`,
`construction_costs_at_start = false`, `supplied = false`,
`construction_group = false`, and `IsGameRuleActive` stubbed false (the existing
`call()` helper already does this). **Expected: the call returns ok.**
Rationale to put in the failure text: this is the exact state where vanilla's own
body indexes `construction_resources == false` at line 670 and raises, so
passing is the widening PREVENTING an error.

**3b — gathered ordinary site.** Fields as `site_for` builds them:
`construction_resources = { WasteRock = <request stub> }` and
`construction_costs_at_start = { WasteRock = 0 }`. **Expected: delegated,
identically to vanilla — `SetAmount(90)` was called and
`construction_costs_at_start.WasteRock == 50` afterwards.** Passing is the
widening CHANGING NOTHING where vanilla already works.

⭐ **Where 90 and 50 come from — hand-derived from vanilla's arithmetic, and they
must stay that way.** The `GetConstructionCost` stub returns `50`; `old_cost` is
`0` from the seeded table; the `GetActualAmount` stub returns `40`. Vanilla then
does `delta = 50 - 0`, `new_amount = Max(0, 40 + 50) = 90`, and writes the start
cost back as `50` (`ConstructionSite.lua:665-683`). ⛔ **Never compute an
expectation by calling the fix, or by re-deriving it from the fix's source.** A
probe that marks its own homework is the failure family this whole chain was
launched over (WORKFLOW: a probe must reach code the way production reaches it
and must not compute its expectation with the fix's own logic).

## 4. Hard constraints — each is a recorded incident, not style

1. ⛔ **Instantiate NO game object.** Use the existing `site_for` pattern: a
   plain table with the built class as its metatable. F49's PT-46 incident left
   orphan objects blocking grid hexes on a live colony. The probe file's own
   header (lines 9-14) states this and cites `classes.lua:730` for why the
   metatable route resolves methods identically.
2. ⛔ **Do not use `SMRTest.SourceOf` / `FromFixPack` / `GetDebug`.** They need
   `debug.getinfo`, absent in mod code (`EF-010`, `debug` is on
   `ModEnvBlacklist`), and they DEFER A SKIP — an unattended run comes back
   inconclusive. Probe header, lines 16-20.
3. ⛔ **EXTEND the existing probe. Do NOT add a new `SMRTest.Register(`.**
   doccheck counts probes as `SMRTest.Register(` occurrences minus one
   (`tools/doccheck.py:546`). A new probe makes the count 101 and forces a STATE
   build-state re-emit and a doc-churn commit for no gain. Keep it 100.
4. ⛔ **Touch no fix-pack `Code/*.lua`.** The repair is committed and verified
   static; this task adds measurement, not code.
5. **SKIP, do not FAIL, when the target is absent.** If `ConstructionSite` is
   not a table or `RefreshConstructionResources` is not a function on it, follow
   the file's existing SKIP style rather than reporting a failure.
6. **Clause 3's verdict folds into the probe's single return.** One
   PASS/FAIL/SKIP for `LandscapeCostGuard`, as now. Name in the FAIL text which
   clause and which state failed — never a bare total.
7. **Keep the PASS string honest.** It currently ends by saying the field route
   (a levelling site on a real map plus a `*_Construction` cost tech) is NOT
   tested here. **That is still true after clause 3** — keep the disclaimer, and
   extend it to say the widening IS now covered at the mechanism level.

## 5. Steps

1. Read the whole probe (`64_Probes_Wave14.lua`, from
   `SMRTest.Register("LandscapeCostGuard"` to its closing `})`), and the vanilla
   body at `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src\Lua\Buildings\ConstructionSite.lua`
   lines 636-684. ⚠️ The Steam `installdir` is literally `Project Spark`
   (`EF-014`), which is why searches under a "Surviving Mars" folder name miss
   the whole install.
2. Write clause 3 per §3, honouring every constraint in §4.
3. Re-read your diff against §4 line by line. State in your report which
   constraint each part of your change answers.
4. `python tools/doccheck.py` in `C:\Dev\SMR-BugFixPack` — must print
   **GREEN** and `100 probes`, with `TESTKIT TREE` the only thing that turns
   dirty. ⛔ If the probe count moved off 100 you violated §4.3; fix that, do
   not re-emit STATE.
5. Commit in the TestKit repo with a message saying what clause 3 measures and
   why it is not covered elsewhere. ⛔ **TestKit is local-only BY DESIGN — it has
   no git remote and never has. Commit locally and say so. Never report it as
   pushed, and never list the missing remote as an owed item.**
6. Report back: the diff, the constraint-by-constraint check from step 3, and
   ⛔ **anything you could not verify.**

## 6. ⛔ Do NOT

* Do not launch the game or ask the owner to. A separate attended boot runs
  `SMRTest.RunAll()` after this lands; your job ends at a committed diff.
* Do not "improve" clauses 1 and 2, the `site_for` helper's shape, or the
  printed strings.
* Do not add probes for the field route, for `EF-066` coverage, or for anything
  else you notice. File what you find; build only clause 3.
* Do not edit `docs/agent/STATE.md` (it is over its byte warn threshold and
  eviction is owner-fired) or any bug entry. The session that reads your result
  updates the record.

## 7. Done means

`LandscapeCostGuard` measures, on `ConstructionSite` itself, both that the
widened guard returns in the state where vanilla raises, and that it delegates
identically in the state where vanilla succeeds — committed in TestKit, doccheck
GREEN at 100 probes, no fix-pack code touched, and a report naming anything
unverified.
