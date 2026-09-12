# Fix_ShelterReflex review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — public outcome claim needs its eligibility and timing limits:**
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:196`–`:197` promises that a colonist
  idling in vacuum heads home before oxygen runs out. The retained wrapper
  requires a valid **working residence**, no transport task, no dying state,
  a half-budget outside timer, and no attempt within the retry interval. It
  checks these only when `Idle` begins; it does not monitor continuously or
  verify that home entry succeeds before the timer expires.
  **SOURCE mechanism / INFERRED organic benefit:** it requests `Rest` for an
  eligible colonist. Whether that adds shelter or survival beyond vanilla on
  ordinary 1.1.0 play remains unverified. Recommend wording such as:
  “When an eligible colonist next idles in vacuum with a working home available,
  the pack requests a return home after half the outside oxygen budget is spent.”
  State that a colonist without a home cannot benefit and successful timely
  entry is not guaranteed.
- **SOURCE — judgment-call label is accurate:** the row at `fix-list.md:189`
  and `:199`–`:200` explicitly identifies an added behavior. Do not relabel it
  a verified vanilla coding error or a demonstrated latent defect hidden by
  shipped data. The site no longer promises the retired habitat-suitability
  override. There is no dedicated card headline for this module.
- **SOURCE — migration PARTIAL baseline stands:**
  `MIGRATION_DEV_REPORT.md:463`–`:500`, `MIGRATIONFIX_AUDIT.md:120`, and the
  current F73 entry already distinguish wrapper coverage from organic benefit.
  This review finds no reason to restore removed half (a) or retire retained
  half (b) solely because its organic effect has not been reproduced.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ShelterReflex.lua | F73 | yes — fresh boot applied; direct settled registry active | yes — command scheduler resolves current Idle; wrapper retains retry timestamp consumer and dispatches current Rest, which attempts home entry | partial — judgment-call label true; outcome omits working-home eligibility, Idle-entry timing, retry exclusions, and unverified timely entry | n/a — no dedicated headline | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/Classes/CommandObject.lua:277; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2578; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1498; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:4577 | SOURCE | organic eligible Idle trigger; added shelter vs vanilla Roam; timely entry and survival; retry timing in play; homeless/unpowered-home residuals in play; retired-half trait-filter control; cross-map applicability; fresh 1.0.7 boot; judgment-call and hidden-repair counts |

## Primary evidence

- **MEASURED installation, not cure:** the settled second boot reports applied at
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:82`.
  The final direct registry read measures active at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:228`.
  No colony loaded or suite ran. Module SHA256 matches `CENSUS.json`:
  `ae3c3f9a3f2aaf8be0d3ec709be7fec3f101036e063d0a6a96883313cd02abc4`.
- **SOURCE — independent primary caller:** after a command finishes and no
  queued/custom idle command is selected,
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/Classes/CommandObject.lua:276`
  selects `Idle` and `:277` reads `self.Idle`; the scheduler calls the selected
  command function at `:250`. Thus the current wrapped method remains on the
  ordinary command path. Current shipped `Idle` starts at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2212`, contains
  residence/work reevaluation and ordinary rest decisions, and ends in `Roam`
  at `:2388`; it contains no `outside_start`/oxygen-budget retreat branch.
  `CommonLua/Classes/CommandObject.lua:378` deletes the old command thread,
  supporting the retained pre-wrapper placement (EF-012), rather than a
  post-wrapper after the command switch.
- **SOURCE — every retained changed path has a consumer:** the wrapper reads
  outside timer and current oxygen budget at `Code/Fix_ShelterReflex.lua:99`–`:100`,
  checks home/task/dying eligibility at `:101`–`:102`, reads its own retry
  timestamp at `:104`, writes that timestamp at `:108`, and dispatches `Rest`
  at `:109`. The next `Idle` invocation consumes the timestamp to throttle
  retries at `:106`. It has no asteroid-class restriction; asteroid is the
  reported example, not the complete code scope.
  The primary destination consumer is
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2578`, which tries
  `EnterBuilding(self.residence)`; `:2579`–`:2581` idles, sleeps, and returns on
  failure. The navigation consumer checks building validity at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Unit.lua:317`, and for habitat
  entrances approaches the entrance at `:385` before entering. A working-home
  predicate alone does not prove reachable or timely shelter.
- **SOURCE control / INFERRED incremental benefit:** vanilla `Roam` already
  recognizes `self.dome == self.residence` at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1496` and attempts
  home entry at `:1498`. The wrapper can alter the command chosen for eligible
  outside state, but absence of an oxygen check in `Idle` does not establish
  that vanilla leaves that eligible state outside until death. The outside
  timer starts at `:3018`, clears on inside state at `:3023`, and suffocation
  remains triggered at `:4577`–`:4578`. No successful entry or survival was
  measured in this review.
- **SOURCE — retired sibling and named residuals:** half (a) is absent from
  this module. Shipped
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/MicroGHabitat.lua:166`–`:170`
  retains a suitable existing habitat even when it is full; `:174` uses the
  current colonist-based community score.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Community.lua:437` explicitly
  documents the no-life-support tier, and `:443` applies it. The wrapper does
  not change those housing decisions, assign a missing residence, fix an
  unpowered home, or override a failed entry. Those are distinct from the
  retained conditional command intervention.

## Not checked, by name

- Organic 1.1.0 eligible outside-state trigger at an actual `Idle` entry.
- Incremental shelter benefit compared with vanilla `Roam` home entry.
- Successful entry before the oxygen limit, Health preservation, or survival.
- Full scheduling and one-hour retry timing in play.
- Homeless colonists, unpowered homes, or unreachable-home residuals in play.
- Retired half (a)'s asteroid habitat trait-filter/no-throw control in play.
- Organic effects on every non-breathable map or colonist subclass.
- Fresh 1.0.7 runtime compatibility of the current wrapper.
- Whole-list judgment-call count, hidden-repair count, and generic card claims.
