# F105 investigation & fix — session report, 2026-08-24

Consumed brief: `docs/agent/prompts/F105_LANDSCAPE_COSTS.md` (git-rm'd in this
commit, per its own §11.6). **Where this report and `agent/bugs/F105.md` (or
`F106.md`) disagree, the entry wins or this report gets corrected in the same
change.** Everything below is the record of sweeps, negatives and process; the
derivations themselves live in the entries.

**Mid-session owner rulings (both delivered in-session, 2026-08-24):**
1. *"This is a number 1 fix priority"* → checklist 72 answered = build now; the
   deliverable upgraded from spec to shipped module.
2. Outside sources (forums, other mods) authorized for this job.

## What shipped

* `Code/Fix_LandscapeCostRefresh.lua` — module 78, guarded delegation on
  `RefreshConstructionResources` installed on the three landscape leaf classes.
* `items.lua` + `metadata.lua` `code` rows, hand-written in matching positions
  (H-10). ⚠️ `metadata.lua`'s `version` untouched — no editor save (H-02); the
  eventual upload sitting owns the bump, and until it runs **the live listings
  are one module behind this tree**.
* Entry `F105` rewritten to `fixed`; new entry `F106`; `EF-066` sharpened with a
  dated clause; checklist 72 receipted, new item 74 routed.

## Boot verification (the post-release price, in full)

* **PROBE SWEEP: clean** — `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`,
  0 hits in both repos, run BEFORE the leg (WORKFLOW hard gate).
* Leg: agent-driven Steam launch (`steam.exe -applaunch 3215050`, the proven
  co-run route), menu-only, **no save touched, no console used**, process
  closed at menu. `tested-unattended` grade.
* Reading: `[mod] [CommunityFixPack] LandscapeCostRefresh: applied` at
  Lua 0:00:17:941; **0** occurrences of `LUA ERROR` / `Error in mod` in the
  whole log. Archived: `docs/archive/f105_Mars.exe-20260824-00.08.38.log`.
* ⛔ NOT done: a crash-path repro (levelling site + cost tech). Never run on
  the rig, before or after the fix. It rides the next sitting — recipe in the
  F105 entry; the F106 settling probe (one console read) should ride the same
  boot.

## Sweeps run and their verdicts (details in `F105.md`)

1. **Reader sweep (brief clue 1)** — all 20 grep hits of
   `construction_costs_at_start`, every enclosing function read. Verdict:
   `ConstructionSite.lua:673` is the ONLY reachable unguarded reader for the
   landscape family; the checklist-72 shape question did NOT flip. Notables:
   `ResourceOverview.lua:812` is dead for landscape sites because city labels
   are keyed by LEAF class name (`Building.lua:438`); `:1615-1616` is dead
   because the landscape `Complete` never calls the base `Complete`.
2. **Subclass sweep (clue 2)** — whole-Src grep: the only
   `GatherConstructionResources` overrides are the landscape family's three;
   no other `ConstructionSite` subclass shares the gap. `RefreshConstructionResources`
   has exactly one definition in the tree (no shipped override anywhere).
3. **Trigger enumeration (clue 7)** — carriers of `Effect_ModifyLabel` with a
   `_Construction` label in ALL shipped Data: three techs (NeoConcrete —
   a Breakthrough, DomeStreamlining, MarsNoveau). **Negative results that
   correct the filed entry:** Efficiency laws (`LawEffectModifyLabel`) and
   story bits (`ModifyLabel`) only call `SetLabelModifier` — no sweep, NOT
   triggers; sponsors/rules/commanders carry no `_Construction` labels; DLC
   carries none.
4. **Caller sweep (clue 8)** — `RefreshConstructionResources` has 3 callers:
   the live trigger (`MarsGameEffects.lua:175`), `OnMsg.ConstructionCostChanged`
   (`:2832` — dead in shipped content: zero Data raisers of any
   `ModifyConstructionCost` route), `TrackElement.lua:875` (track leaders only).
5. **Pack self-clearance (clue 5)** — zero `Code/` hits for the field, both
   methods, and the Msg; the two landscape modules touch drone pathing and the
   unit sweep only. The pack is not a contributing cause.
6. **Naming route re-verified (context §4, verify-only)** — vanilla's
   `Msg("MilestoneCompleted", id)` is `Milestones.lua:135` (filed entry said
   :134), `OnMsg.MilestoneCompleted` is `:176-184` (filed said :175-183),
   `GrantResearchPoints` call `:180` = the stack frame. Byte-equivalence of the
   `Fix_MilestoneCrash` path holds; the misattribution mechanism (`EF-065`(a))
   stands. Checklist 73 untouched, per the brief's fence.
7. **Milestone identified** — `WorkersInWorkshops`, `Data/Milestone.lua:323-347`;
   `:340` is the reporter's stack frame, matching their own words.

## The load-bearing discovery (why the fix looks the way it does)

`Building.__hierarchy_cache = true` + un-flagged `ConstructionSite` ⇒ the class
builder copies `RefreshConstructionResources` by reference into every
descendant's built table (`classes.lua:700-705`; split documented `:986-988`).
The pack applies post-`ClassesBuilt`, so the "one wrap on ConstructionSite
covers every subclass" shape recommended on checklist 72 **could never have
fired** — the fix instead installs on each leaf class. Same mechanism makes
`Fix_SmallLandscapeSites` (F33) a suspect no-op → **F106**, filed not fixed
(brief §5 scope fence). Also verified before trusting class-table assignment:
`GetAllClassesMeta()` returns nil and the only `__newindex` guard is
developer-build-only — retail class tables accept plain writes.

## Prior art (owner-authorized outside check)

No community fix of this crash exists. ChoGGi's Fix Bugs (2018 lineage) touches
DomeStreamlining/MarsNoveau only to correct build-menu *display*, and its
"Landscaping Freeze" fix is a different defect. Sources consulted:
* https://github.com/ChoGGi/SurvivingMars_Mods/blob/master/Mods%20ChoGGi/Fix%20Bugs/MoreInfo.md
* https://steamcommunity.com/sharedfiles/filedetails/?id=2721921772
* Paradox forum / Steam discussion threads on landscaping bugs (searched for
  the symbol `construction_costs_at_start`: no hits; the 2021-era reports are
  cost-calculation bugs, not this crash).

## Process notes

* doccheck GREEN at baseline and at close; counts moved 78→79 files, 77→78
  modules, 170→171 rows. Both INDEXes regenerated by the project's own
  renderers (`split_bugs`/`split_facts.render_index`) — never hand-edited.
* STATE.md byte warn (9505 > 9216) predates this session and is already
  receipted verbatim on the checklist (item 73 block); the owner fires
  `agent/prompts/STATE_EVICTION.md`.
* The session ran without a harness todo tool; the brief's §1 live list was
  kept as a repo-root `F105_TODO.md`, deleted in the closing commit.
