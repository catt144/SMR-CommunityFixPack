# Wildfire cure never reaches colonists served from home — investigate, file, repair if it holds

**Owner decision (2026-09-18):** investigate this as a possible code defect and file it if it holds.
The design-interaction reading — Feeding the Future delicacies simply make colonists too healthy — is
already set aside as a balance question, outside a bug-fix pack. What is open is whether 1.1.0 moved
medical benefits onto a route the cure's hook does not reach.

**Lifecycle:** one-off. `git rm` this file and delete its row in `prompts/README.md` in the same
commit that lands your result.

**Start:** `git log --oneline -5`, `git pull`. Authored at `bc6899b`; everything below was read on
game 1.1.0.403908 from `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src` (1.0.7 beside it).

## Report that started it

r/SurvivingMars, 2026-09-18, "Wildfire Crisis impossible to end with DLC": infected colonists never
visit a medical building, so the mystery cannot end, and *"colonists are gaining health bonuses from
medical centres without ever visiting them."* Players work around it by shutting hospitals or
draining sanity.

## The lead (read by the orchestrator, not verified end to end)

- The cure clears `Infected` in one place: `MedicalBuilding:Service`, once `g_StartVaccinating` is
  set (`Lua/Buildings/MedicalCenter.lua:36-39`; the flag is set by `Mystery8_BeginHealing`,
  `Lua/Traits.lua:1206-1229`). The mystery's text promises *"cured permanently after their first
  visit in a Medical Building"* (`Data/Scenario/Mystery 8.lua:204`), and it ends only when no
  colonist is infected (`:1045-1051`).
- `Service` is reached only through a physical visit (`Colonist:VisitService`,
  `Lua/Units/Colonist.lua:2482`). Colonists visit medical only when health is below
  `HighStatLevel` or sanity is low, with a new 16-hour cooldown (`:2206-2209`, `:2313-2333`).
  Infected loses 12 Health a day (`Data/TraitPreset.lua:144-157`).
- New in 1.1.0 (zero hits for either name in 1.0.7): `ApplyResidenceAdditiveStats`
  (`Lua/Stats.lua:622-647`, called on every rest at home, `Colonist.lua:2605`) pays each service
  category in `dome.serviced` through `AccumulateCategoryServiceStats`. `Dome:AddAssignedService`
  (`Lua/Buildings/Dome.lua:1424`) registers any service by category, and no medical exclusion was
  found. If medical Health flows through it, infected colonists get medical stats without calling
  `Service`, stay above the threshold, and are never cured.
- Separately, FtF delicacies add +5 Health a meal (`DLC/norman/Presets/Resource.lua:240`). That is
  the balance half and not the question.

## The question

Does the 1.1.0 at-home service route pay a medical building's stats without the cure's hook firing,
so that the Wildfire mystery cannot finish in ordinary play? Establish what fills a category's stat
values, whether medical buildings are in it, the magnitude per rest against −12 a day, and whether
the stall happens **without** Feeding the Future. Your call on how to read it and what to run; the
TestKit, desk harnesses and the log route (`WORKFLOW.md`) are all available. A lead is not a route:
refute it if the source says so.

## If it holds

File it through `smr-bug-library` with its control, then decide the repair under `FIX_POLICY.md`
(intent tell, reach tier, least-invasive technique, §3 savegame discipline). Your call whether the
cure should follow the at-home medical payment, or whether infected colonists should be made to
visit once vaccination starts; record the reasoning and the counter-reading in the entry. Build it
if it is clear-cut, with a desk harness that makes the unfixed body FAIL; the C107 fix
(`Code/Fix_DryFarmingFarms.lua`, `tools/desk_c107_dry_farming.py`) shows the house standard,
including the cold-boot load order that its first build got wrong. Append the outbox Pending entry
if you build.

## Scope and stops

- In: the Wildfire cure path and the at-home service route. Out: delicacy balance, other mysteries;
  a finding there goes in your report, not an edit.
- Stop and report if the route is unreachable on Steam or console, or if the fix would change how
  the game houses or services colonists generally. A stall that needs the DLC is still in scope
  (both are vanilla); say which it is.
- Do not claim the mystery is unwinnable; the report shows workarounds. The claim the evidence can
  carry is "cannot finish in ordinary play once colonists are served from home".

**Done:** an entry filed with its control (or the lead refuted, with what the refutation rests on),
a build if clear-cut, doccheck GREEN, committed with pathspecs and pushed, and this file removed.
