# ONE-OFF PROMPT — review the drone stress harness BEFORE its first run

**Paste everything below into a FRESH session (any model).** One-off; delete it
once the harness has been vetted and its first A/B has run.

**Fire this with the game CLOSED** — the review is read-only, but any fix touches
loadable Lua, which does nothing until the next game launch.

---

You are reviewing a **brand-new, never-executed** test instrument before it is
used to make an engineering decision. It is
`C:\Dev\SMR-BugFixPack-TestKit\Code\91_Stress.lua` in the Surviving Mars:
Relaunched "Community Fix Pack" project (`C:\Dev\SMR-BugFixPack`, with a
local-only TestKit companion repo at `C:\Dev\SMR-BugFixPack-TestKit`).

It was written in a single pass, has **never been run**, and its output is about
to be used to judge whether an optional gameplay module works and to settle
design questions in a larger proposal. **A flaw in the instrument would quietly
corrupt every conclusion drawn from it.** That is what you are here to prevent.

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

**Also note a proven hazard:** `ModTools\Src` is NOT the shipping build. The game
runs `Packs\Lua.fpk`. This was proven live — `GetCameraLookAtPassable` exists in
Src and does not exist at runtime. Any global the harness calls could be absent.

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
- **The delivering-drone shortcut.** It claims `MaintenanceDroneUnload` →
  `StartWorkPhase(drone)` hands the first repair tick straight to the delivering
  drone via `SetCommandKeepQueue`, bypassing `FindTask` entirely — which would
  mean most first claims never go through the mechanism under test, and only
  `no_resource`-maintenance buildings give a clean signal. **If that is true, is
  the headline metric measuring the module at all, or mostly measuring hauling?**
  This is the single most important question in this review.
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
