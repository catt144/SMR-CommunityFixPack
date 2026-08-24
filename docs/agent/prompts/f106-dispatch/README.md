# Chain `f106-dispatch` — does a post-build parent wrap actually reach subclass instances?

**One unattended launch settles F106, F33's real status, and most of checklist
74's audit. Owner cost: ZERO** (the owner arms and starts it; nobody watches).

## Manifest

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| ~~01~~ | ~~`01_PROBE_opus.md`~~ **CONSUMED 2026-08-24** — grave: deleted in commit `f106: 01 consumed`; its record is that commit's message plus `reports/F106_DISPATCH_SWEEP.md` and `reports/F106_PREDICTIONS.md`. ⚠️ It could not `git rm` itself: this folder was UNTRACKED until that same commit. | volume tier | **no** | fixes the false-green F33 probe, builds the dispatch sweep + the F105 guard probe, commits PREDICTIONS, runs the leg, records |
| 02 | `02_AUDIT_fable.md` | top tier | no | adversarial backward QA against the archived log; integrates; empties the folder |

Strike a row the moment its prompt self-consumes.

⚖️ **Two prompts is the FLOOR, not a shortcut** — owner rule 2026-08-04: even a
single truly unattended item is a minimum chain of two, volume tier executes,
top tier audits adversarially against the archived logs. `CHAIN_METHOD.md` §4.0.

## Why this chain exists

`F106` says a `{class, method}` wrap installed after `ClassesBuilt` is invisible
to subclass instances when the method's declaring class does not set
`__hierarchy_cache` — because the class builder **copies** the parent's members
into each descendant's table instead of chaining
(`CommonLua/Core/classes.lua:700-709`). If true, `Fix_SmallLandscapeSites` (F33)
has never run, and an unknown share of the pack's ~60 class wraps are silent
no-ops.

**It is DERIVED, not measured.** And the reason nobody caught it is instructive
and directly in scope: the F33 probe calls
`LandscapeConstructionSiteBase.GetClosestDests(fake_table, …)` — straight off the
table we patched, with a hand-built table as `self`. It tests the wrapper's logic
and never tests dispatch, so it **cannot fail on a broken dispatch.** It has been
printing PASS the whole time.

⚠️ **This is the SECOND false-green of this family.** The TestKit's own last
commit (`8feaf59`) reads *"the C50 probe derived its number with the fix's own
arithmetic, so it passed over the defect."* Two independent instances is a
pattern, and `02_AUDIT` decides whether a general rule belongs in `WORKFLOW.md`.

## Binding chain rules

1. **Staleness check first.** `git log --oneline -10` + `git pull` in **both**
   repos (`SMR-BugFixPack` and `SMR-BugFixPack-TestKit` — separate git repos,
   shared kit) before anything.
2. **Inbox / outbox.** Nothing owed lives in a session's memory. Append every
   handoff to `02_AUDIT`'s `## Notes from upstream` in the same commit that
   deletes your own file.
3. **Route, don't drop.** Unsure whether something is yours? **STOP AND ASK.**
   A discovered item goes to a named owner (this chain's later prompt, an entry,
   or the checklist) before you close.
4. **Self-split at a clean commit boundary** rather than running a context window
   to the edge. A shrinking folder is progress.
5. **File defects you trip over, including in our own instruments.**
   ⛔ **A silently-corrected instance is destroyed evidence** — the false-green
   probe gets DISCLOSED on an entry, never quietly fixed.
6. **`WORKFLOW.md` "Authoring a prompt" elements 1–7 bind**, including the
   stale-probe gate before any recorded result.
7. ⭐ **Predictions before runs.** Commit AND push the predicted readings BEFORE
   arming the launch. `git log` timestamps are the falsifiability proof. A
   prediction written after the log exists is worth nothing.
8. **Archive the log in the same commit that cites it** — `git add -f`, the
   `.gitignore` drops `*.log` silently.
9. ⛔ **This chain writes NO fix code.** It repairs an instrument, adds probes,
   and measures. **Re-installing the missed wraps is checklist 74's decision,
   not this chain's** — even if the sweep proves twenty of them broken.
10. **Push both repos after committing** (owner 2026-08-14: pushing is standing
    allowed; `git push` ≠ publishing).

## Scope fence

**IN:** the F33 probe's dispatch repair; a new dispatch-reach sweep probe; a new
F105 guard regression probe; predictions; one unattended launch (more if a run is
voided and re-armed); recording into `F106`/`F33`/`EF-066`/checklist 74;
`items.lua` upkeep in the TestKit.

**OUT:** any `Code/*.lua` change in the fix pack. Re-installing missed wraps.
Checklist 73 (the blame surface). F104 / Passage Network. The queued 1.0.x upload
sitting. Any owner time.

**Something interesting out of scope → FILE IT, DO NOT FIX IT.**

## Stop conditions — permission, not failure

- **The pack gate reads wrong at run top** (module count, `applied` lines) →
  **STOP.** Do not bank readings about code that did not execute. That is the
  `unattended-2` lesson and it is binding.
- **The sweep says F106's mechanism is WRONG** (leaves chain, the wrap reaches
  them) → that is a **result**, and the best one available. Rewrite `F106`, say so
  loudly, and hand `02_AUDIT` the reversal. Do not soften it.
- **The sweep needs to instantiate a real game object to answer** → **do not.**
  F49's PT-46 incident left orphan objects blocking grid hexes on a live colony
  by injecting a construction mode; the no-live-UI-internals rule came from it.
  Record the limit and hand the question on.
- **More than ~15 wraps come back broken** → the audit is a defect *class* with
  release implications, not a probe result. Stop, route to the owner with a
  recommendation, let `02_AUDIT` still run.
- **A probe cannot answer without `debug.getinfo`** → it is the wrong probe.
  Rebuild it on function identity (see `01`'s §3) or drop it.

## What may NOT be claimed by either prompt

- ⛔ **Never `tested-attended`** — nobody is at the keyboard. `tested-unattended`
  is the ceiling, and **screen events are not claimable at all**.
- ⛔ **Never "F33 is broken" from a derivation.** Only the measured identity
  comparison settles it; until then `suspect`.
- ⛔ **Never a count, md5 or byte figure you did not compute.**
- ⛔ **Never "the audit is complete"** — the sweep reports which classes hold a
  stale copy, **not which are instantiated**. That gap is real and stays stated.
- ⛔ **Refuted requires the condition was SAMPLED**, not that a count was zero.
- ⛔ Do not report an unexplained log line as "not caused by our leg". Report it
  with its age. Every pushback on that habit here has found a real defect.

## Self-consumption

Each prompt `git rm`s itself in its closing commit, naming its grave. `02_AUDIT`
deletes this README and the folder with it.
