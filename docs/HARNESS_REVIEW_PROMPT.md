# ONE-OFF PROMPT — repair the drone stress harness after its first run exposed a metric flaw

**Paste everything below into a FRESH session (any model).** One-off; delete it
once the harness has been repaired.

**Fire this with the game CLOSED** — the review is read-only, but any fix touches
loadable Lua, which does nothing until the next game launch.

**SEQUENCING: the QA review (`docs/QA_REVIEW_PROMPT.md`) has now RUN
(2026-07-29, fresh-context session) — its verdict is in hand and it changes
this review's aim.** The claim gate is kept but demoted ("component under
evaluation" — do not invest further until the instrument can score it), and
the instrument's redesign is now the front line: the QA verdict's central
finding is that **nothing in Track B should be built until the hauling leg is
decomposed into queue latency (demand posted → first supply claim) vs
execution (claim → pickup → unload)** — those imply opposite remedies
(dispatch/priority logic vs stat/depot levers). The recommended mechanism,
with every patch point verified against Src: chained wrappers on
`RequestAssignUnit` / `RequestUnitFulfill` (bare globals, `_TaskRequest.lua:352,412`;
`Drone.lua` holds no file-local alias) plus `StartDemandPhase` /
`StartWorkPhase` / `Repair` timestamps — TestKit-only, so no A/B pair owed.
Two more QA facts to carry in: the delivering-drone handoff is verified
structural (`RequiresMaintenance.lua:418-426` → `:190-198`
`SetCommandKeepQueue`), and `TaskRequestHub:FindTask` has exactly ONE caller
tree-wide (`Drone.lua:621`), so wrapping either end captures every claim.

> **STATUS UPDATE — this prompt was written before the first run; the run has
> now happened (2026-07-29) and CONFIRMED the top concern in §2.** The A/B
> executed cleanly end to end — no crashes, deterministic target set, both legs
> completed, output readable — so the harness *works mechanically*. But it
> returned a **null result** for the module under test and the run revealed
> **the headline metric is measuring the wrong thing**. Full numbers and
> analysis are on the **D06 entry** in `C:\Dev\SMR-BugFixPack\docs\BUGS.md`;
> read that first. Summary: with the module ON the claim gate fired **once**
> (`vetoed +1`) across 25 simultaneous malfunctions, the leg it arbitrates moved
> 58m → 57m, and **0 of 25 targets were `no_resource` maintenance** — so
> `MaintenanceDroneUnload` → `StartWorkPhase(drone)` handed the first repair
> tick to the **delivering** drone every time, bypassing `FindTask`. The metric
> counted **which hub delivered the resource**, not which hub won a claim.
> **Your job is therefore less "find bugs before first use" and more "make this
> instrument capable of scoring what it claims to score" — plus the ordinary
> correctness review below, which has still never been done.**

---

You are reviewing a test instrument that has been run exactly once and is used
to make engineering decisions. It is
`C:\Dev\SMR-BugFixPack-TestKit\Code\91_Stress.lua` in the Surviving Mars:
Relaunched "Community Fix Pack" project (`C:\Dev\SMR-BugFixPack`, with a
local-only TestKit companion repo at `C:\Dev\SMR-BugFixPack-TestKit`).

It was written in a single pass and has now been run **exactly once** (the
2026-07-29 A/B — see the status update above); its output is used to judge
whether an optional gameplay module works and to settle design questions in a
larger proposal. **A flaw in the instrument would quietly corrupt every
conclusion drawn from it.** That is what you are here to prevent — and one
such flaw has already been confirmed by the first run.

## What it is for

The pack ships `Opt_DroneOverhaul` (D06) — an opt-in module whose headline claim
is that **repair work in overlapping Drone Hub coverage goes to the CLOSEST hub's
fleet first** instead of whichever fleet's poll happened to land first. Until now
it has only been judged by eye and by counters.

The harness is meant to turn that into a controlled A/B:

1. Quicksave.
2. Toggle the module OFF; `SMRTest.Stress.Break{scope="overlap", n=25, seed=1}`
   breaks a deterministic seeded set of buildings and measures the repair.
3. Reload the quicksave; toggle the module ON; run the **identical** call.
4. `SMRTest.Stress.Compare()` prints both runs side by side.

Because the same save is reloaded and the target set is seeded and deterministic,
both legs are supposed to cover the identical buildings under identical colony
state, with the module as the only variable.

**Headline metric: percentage of first repair claims taken by the closest
covering hub.**

## Read these first

- `C:\Dev\SMR-BugFixPack-TestKit\Code\91_Stress.lua` — the harness. Its header
  comment states the engine facts it is built on; verify them, don't assume them.
- `C:\Dev\SMR-BugFixPack\Code\Opt_DroneOverhaul.lua` — the module under test.
  The harness deliberately mirrors its `closest_covering_hub` logic so it scores
  the module against the module's own notion of "closest". Check that mirror is
  faithful.
- `C:\Dev\SMR-BugFixPack\docs\PLAYTEST_CHECKLIST.md` — the stress-harness table
  in the Test Kit helpers section, and the PT-52 procedure.
- `C:\Dev\SMR-BugFixPack\docs\STATUS.md` — "Key technical facts". Several are
  load-bearing here, especially: mod code loads before classes are built; runtime
  patches must target the **leaf** class; `error()`/`assert()` **report and
  continue** rather than unwinding; post-wrappers on command methods never run.
- Game source, read-only, NEVER modify:
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

## Your job, in order

### 1. Will it even run?

It has never been executed. Look for anything that errors or silently does
nothing on first contact: nil indexing, wrong global names, functions that do not
exist at runtime, argument-order mistakes, `string.format` mismatches.

Pay particular attention to the fact that **`error()` does not unwind in this
engine** — a raising statement is skipped and execution continues, so a broken
line can produce *silence* rather than a crash. A previous console command in
this project printed nothing at all because `IsValidThread(nil)` raised inside a
loop body and every iteration's print was skipped. That failure mode is easy to
mistake for "no results".

**CORRECTED (2026-07-29 QA session): the shipped build IS Src.** The shipped
`Packs\Lua.fpk` was extracted in full and diffed against `ModTools\Src`:
**2,250 of 2,256 shipped Lua files are byte-identical**, including every
drone/maintenance/task-request file this harness touches; the only 5
divergences are engine/tooling files (camera state, GED stubs, async/sound/
xinput wrappers). Shipped build: `1.0.7.396349`. The earlier
"`GetCameraLookAtPassable` does not exist at runtime" proof was a misreading —
it is a **`local function`** (`Cheats.lua:42`), invisible from the console *by
design*, in Src and shipped alike. So: trust Src line numbers, but keep the
engine-behaviour cautions above (`error()` reports-and-continues, sandbox
blacklist) — those are real and unchanged.

### 2. Does it measure the right thing?

This matters more than whether it runs. Specific questions:

- **Claim capture.** It pre-wraps `Drone:Work` (`Drone.lua:898`) on the leaf class
  `Drone`, reasoning that (a) a base-class runtime wrap is invisible to built
  subclasses and (b) `Work` is a command method so a post-wrapper would never
  run. Is that right? Will the wrap actually fire for every repair claim? Are
  there repair paths that never route through `Drone:Work`?
- **The two-leg split.** The harness claims a malfunction runs a DEMAND leg (a
  drone hauls the maintenance resource in — untouched by the module) and then a
  WORK leg (the repair request — what the module arbitrates), and reports them
  separately. Verify against `RequiresMaintenance.lua`.
- **The delivering-drone shortcut — CONFIRMED, this is now the main work item.**
  `MaintenanceDroneUnload` → `StartWorkPhase(drone)` hands the first repair tick
  straight to the delivering drone via `SetCommandKeepQueue`, bypassing
  `FindTask`. The first run proved it empirically (0 of 25 targets were
  `no_resource`; 26 claims for 25 buildings; near-uniform ~57m "work→claim" in
  BOTH legs = a handoff, not a race). **So the headline metric scores which hub
  DELIVERED.** Verify the mechanism yourself, then answer: **what should the
  metric be instead?** Candidates already on the table — deliberately sample
  `no_resource`-maintenance buildings and dust/clean work (the only populations
  where the gate can act); instrument `TaskRequestHub:FindTask` outcomes
  directly rather than inferring from `Drone:Work`; or report the gate's own
  `vetoed`/`veto_expired` against offered-claim counts. **The QA review's
  recommended shape (2026-07-29): per-request lifecycle tracing** — timestamps
  at demand-posted, first `RequestAssignUnit`, unload/`RequestUnitFulfill`,
  work claim, and `Repair`, so every repair decomposes into queue-latency vs
  travel vs work; the no_resource/dust cohort then scores the gate on top of
  the same log. Propose the design you would trust, and say what it would have
  shown on the run just completed.
- **Explain the ~57m "work→first claim" figure.** If the delivering-drone
  handoff is immediate (`SetCommandKeepQueue` at `RequiresMaintenance.lua:198`),
  a near-uniform ~57m from "work phase" to "claim" in both legs is suspicious —
  it likely means the harness's event anchors measure from malfunction (or the
  drone finishes its queued commands first), not from work-request fill. Pin
  down the exact event semantics; they decide what every published number
  meant.
- **Record run conditions with the results.** The 2026-07-29 run's colony was
  at the vanilla drone-stat ceiling — +60% move speed (Low-G Drive + Advanced
  Drone Drive, live-read 2304 vs base 1440) and 2× carry (Artificial Muscles) —
  on top of full depots and 14-24 idle drones per hub. Per the EXTERNAL
  VALIDITY rule in `PLAYTEST_CHECKLIST.md`, the harness output should state
  such conditions itself (a conditions header in `Compare()` would do) so no
  future run's numbers are read without them.
- **Should the harness measure the HAULING leg instead or as well?** The run
  found hauling is **3h03m of a 3h27m total — 88% of elapsed time**. Yes — but
  note the QA review's caution against the easy inference: the run's targets
  were `overlap`-scope (already registered to multiple hubs, all with idle
  drones), so **the 88% does NOT by itself promote D08's registration
  dispatcher** — awareness wasn't the shortage in that run. What the 88% needs
  is the decomposition above: queue-latency dominance points at dispatch/
  priority logic (e.g. the maintenance priority-escalation option — vanilla
  precedent `SupplyGridBreakable.lua:48-56`), travel dominance at stat/depot
  levers. The instrument's job is to make that split measurable.
- **Observer effect.** The wrap adds work to a hot path. Breaking 25 buildings at
  once is a demand *surge*, not steady state — is surge behaviour representative
  of the problem the module exists to fix?

### 3. Is the A/B actually controlled?

- **Determinism.** Targets are handle-sorted then shuffled with a seeded
  Park-Miller LCG. Does the same save + same seed truly produce the identical set
  across a reload? Are object handles stable across save/load?
- **Cross-leg contamination.** `Opt_DroneOverhaul` keeps module-local state
  (`strikes`, `cover_cache`, `hub_miss`, `stats`) in **process memory**, which
  survives a save reload. The harness snapshots `stats` deltas — but does any
  other retained state let leg A influence leg B?
- **Toggle cleanliness.** Is flipping the Mod Options toggle between legs
  genuinely equivalent to the module having been off/on the whole time?
- **Sample size.** One run of 25 per leg. Is that enough to distinguish a real
  effect from noise, given repair timing varies with drone position and traffic?
  If not, say what would be.

### 4. Is it safe to run on a live colony?

It calls `SetMalfunction()` on real buildings. Default exclusions are drone hubs
and extenders (never break the system under test), domes, life support, power
producers and storage. Are those exclusions sufficient and correctly expressed?
Can a run plausibly kill colonists or cascade? Is `HealAll()` a genuine recovery?
Does the watcher thread terminate cleanly in every path, including reload
mid-run?

### 5. Deliver

1. **Go / no-go** on running the A/B as written.
2. **Bugs found**, ranked, each with the fix — apply them if they are clear
   mechanical corrections.
3. **Measurement-validity verdict** — especially the delivering-drone question in
   §2. If the headline metric is not measuring the module, say so plainly and
   propose what would.
4. **A recommended run procedure** if you would change the one above (scope,
   `n`, seed count, repeat runs, game speed).
5. **Anything you could not verify** and what it would take.

Then **stop and report to the user.**

## Constraints

- TestKit changes are **local-only** and owe **no A/B probe pair** (that
  obligation applies to fix-pack `Code/` changes). Do not touch
  `C:\Dev\SMR-BugFixPack\Code\` in this review — the module under test must not
  change, or the A/B is meaningless.
- Confirm `Mars.exe` is not running (`tasklist`) before editing loadable Lua;
  edits do nothing until the next launch.
- Parse-sweep any file you change:
  `python -c "import luaparser.ast as ast; ast.parse(open(r'<path>',encoding='utf-8-sig').read())"`
- Commit in the TestKit repo with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`.
  **Do not push it** — the TestKit is local-only by decision.
