# Drone project prompt (model-agnostic) — the ONLY prompt for drone work

**Written 2026-07-31 late, after the research sitting that answered all four
gates.** Paste this into a fresh session when the owner wants to work on drones.
**This prompt is RE-RUNNABLE — it does NOT delete itself.** Update it in place at
the end of every drone session.

> 📁 **DOCS LAYOUT (reorganised 2026-08-01) — read `docs\README.md` if unsure
> where something lives or where a new document goes.**
> `docs/` root = daily truth (`STATUS`, `BUGS`, the playtest files,
> `FUTURE_IDEAS`, `MOD_DESCRIPTION`) · `docs\agent\` = the binding rules
> (`ENGINE_FACTS`, `FIX_POLICY`, `WORKFLOW`) · `docs\prompts\` = the two
> standing prompts + live one-offs · `docs\reports\` = reports, plans,
> specs, surveys · `docs\archive\` = spent, plus `SESSION_LOG.md`.
> **New rules/engine facts go in `agent\`, not buried in a report. Defects go
> in `BUGS.md`, never a report and never `FUTURE_IDEAS.md`. Reports are not
> authority — if a report and `BUGS`/`ENGINE_FACTS` disagree, the root/agent
> document wins.**

> 🚧 **This prompt owns drone work exclusively.** `docs\prompts\FABLE_NEXT_PROMPT.md` is
> the general prompt; it may *answer questions* about drones but it no longer
> drives drone work. If you were started from that prompt and the session turns
> into drone work, **stop and load this file instead.**

**⛔ THE STALE-PROBE GATE (HARD RULE, owner, 2026-08-01) — before ANY test this
session runs or records, attended or unattended:** run
`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`, put the result
in the todo list, and record NOTHING unless it is clean or every hit is
declared by the test design; every result commit carries a `PROBE SWEEP:`
line. Full rule: `WORKFLOW.md` "Probe hygiene".

**Staleness check — do this FIRST:** `git log --oneline -10` + `git pull`. This
file was written at **`bd8d831`** and patched at **`bdc2c27`** (the PT-20 leg).
If commits landed after that, read them before trusting anything below — this
project has already had a prompt go stale mid-job.

> 🛑 **F86 CHANGED THE GROUND UNDER THIS PROMPT — read `BUGS.md` F86 and
> `docs\reports\SAVE_SAFETY_REDESIGN.md` before touching the D06 decision.** PT-20
> (2026-07-31) measured **pack code being serialised into the savegame and still
> running after the mod is removed**, and **`Opt_DroneOverhaul` is one of the two
> proven sites** — 98 errors per session after removal, and it leaked **with its
> own opt-in toggle OFF**, because the `Drone:Idle` wrapper installs at file
> scope and only early-returns.
>
> **Three claims below were written before that and are now wrong. They are
> corrected in place; this banner exists so you do not trust a stale memory of
> them:**
> 1. *"uninstall is safe and silent"* — it is **not silent**. The data half is
>    still lossy-but-quiet; the **code** half floods the log.
> 2. *"Option 2 is uninstall-clean by construction / nothing mod-shaped ever
>    enters the save"* — **false as written.** Staying inside `-1..3` keeps the
>    *priority data* clean; it does nothing about the module's own **code**
>    entering the save via a persisted thread stack. Option 2's advantage is real
>    but narrower than stated.
> 3. The **cleanup mod's justification** — *"mods get no save hook"* — is
>    **false**. `OnMsg.SaveGameStart` / `SaveGameDone` reach mods (measured). A
>    tear-down-on-save scheme is implementable, so the cleanup mod is no longer
>    "the only thing that can occupy that window".
>
> **None of this picks a side in the D06 decision, and neither may you.** It
> changes the inputs, not the verdict. F86's remedy is an **owner decision that
> has not been made** — do not assume any layer will be adopted.

---

## 1 · Scope fence — read before doing anything

**IN scope:** D06 (the overhaul, v1 shipped + the rebuild), D08 (extender
overhaul), D09 (stat dials, `tested`), F77 (extender flap churn), the drone
priority/queue machinery, the consolidated drone playtest, and the **cleanup
mod** insofar as it exists to serve the overhaul.

**OUT of scope — everything else in the pack.** D10, D12, F76, the wave-6
disaster fixes, the needs-eyes list, PT-20, the FIX_POLICY §4 amendment, the
possible pack split.

**If you find something interesting out of scope: FILE IT, DO NOT FIX IT.** Add a
BUGS.md entry (or a line on the relevant existing entry) with the evidence and
stop there. A drone session that quietly fixes a colonist bug is how this project
got a mission-creep rule in the first place (`docs\FUTURE_IDEAS.md`).

**⛔ DO NOT BUILD ANY PART OF THE OVERHAUL until the design decision in §3 is
settled by the owner.** Not "while we're in there", not a prototype, not a
"quick sketch to see how it feels".

---

## 2 · Where the drone project actually stands

**All four research gates are ANSWERED (2026-07-31).** Nothing on the research
side is owed. Evidence lives on the **D06 entry** in `BUGS.md` and in
`docs\reports\DRONE_PRIORITY_SYSTEM.md` §8-§10.

| Gate | Answer |
|---|---|
| **Q1** — does the C matcher honour a widened range? | **HONOURED, both legs.** A band-4 *repair* and a band-4 *haul* were consumed by drones; the haul on a cheat-free symmetric pair with `demand_queues[4][Polymers]` inspected directly. |
| **Q2** — are hub queues persisted or rebuilt? | **PERSISTED.** Allocated in `TaskRequestHub:Init()` at construction, never on load. |
| **Q3** — do the data tests identify what we think? | **Yes, with corrections.** Use the game's own class test `IsKindOf("AirProducer"/"WaterProducer")` → exactly **5** buildings. Food service = `ServiceWorkplace` **AND** a Food demand → exactly **4**. |
| **Q4** — does a default change reach existing saves? | **Yes.** Defaults are omitted from saves; live-confirmed both branches. **No template in the game sets `priority`.** |

**Also settled and not to be re-litigated** (carried from the 2026-07-31 planning
session):

- **The drone insight:** the player's arrows answer a **supply-allocation**
  question. Repairs inherit that answer without the player ever being asked.
  **Repairs move off that scale.** The split is `is_malfunctioned` — elevate
  **broken**, not degrading.
- **The claim gate is DROPPED, not demoted.** B2 measured it intervening once in
  25 malfunctions, moving its leg by one minute.
- **Hauling is 88% of elapsed time and D06 v1 exempts it by design.** A scoping
  error, not a tuning miss — and the reason this is a rebuild.
- **ONE TOGGLE, ALL OR NOTHING.** No sub-toggles. **D09's dials stay separate**
  (clean off position, already `tested`).
- **The developers' own rule is *"life-support-critical repairs are urgent"*** —
  they applied it to pipes and dome fractures and never extended it to the
  buildings that produce the air. Extending it **completes their policy**. That
  framing is the module's whole defence; do not weaken it by bolting on
  preferences.
- **C3 merges: NEVER.** **F79: CLOSED `wontfix`** — do not re-propose or park it.

---

## 3 · ▶️ THE NEXT ACTION — the design decision (OWNER CALL, not yours)

The band scheme **passed** Q1, but the sitting that proved it also found **two
constraints that did not exist when the five-band table was drafted**. Both are
written up neutrally. **No side has been picked, and you must not pick one.**

**Constraint A — the widened DATA is silent but LOSSY** (§9). A widened save
loads into vanilla with **zero errors from the priority data** (wide tables,
narrow loops — the mirror of the incident that broke a live save). But elevated
work is **stranded**, and the heal path expires: `DepositsSpawned` re-registers
every hub, but only fires from a sector scan that places deposits, and **sector
status is a one-way ladder with no re-scan**. Clearing the map is an early act;
removing a mod is a late one. **The hub UI toggle does NOT re-register**
(measured).

> ⚠️ **CORRECTED 2026-07-31 (F86): "uninstall is safe and silent" is no longer
> true of the module as a whole.** The sentence above is now scoped to the
> *priority data* only. Separately and additionally, **`Opt_DroneOverhaul`'s own
> code enters the save** on drone command-thread stacks and throws 98 errors per
> session after removal — measured, and with the module's toggle OFF. That is
> F86, it applies to **every** option below equally, and it is not a reason to
> prefer one band scheme over another.

**Constraint B — the duplicate leak, and it bites with the mod INSTALLED** (§10).
`DroneControl:RemoveBuilding` iterates using a **file-local pinned at 3**
(`DroneControl.lua:8`) that mod code cannot reach. A re-registration heals the
building but never removes the old band-4 entry — measured `4 → 6`.
Re-registration is routine in play, so bands 4-5 accumulate dead references
without bound.

### The three options, as they stand

1. **Keep bands 4-5.** Add a `LoadGame` sweep so an installed colony stays tidy;
   ship the **cleanup mod** as the uninstall remedy. **Cost:** closing the
   duplicate leak needs a **full replacement of `DroneControl:RemoveBuilding`**
   (FIX_POLICY §1.5) in the most shared queue code in the game — one of the
   highest patch-rot exposures available.
2. **Work inside `-1..3`.** ⚠️ **CLAIM NARROWED 2026-07-31 (F86)** — this option
   is uninstall-clean **in its priority data**, not "by construction" overall:
   vanilla recomputes every priority at insert, so **no mod-shaped *data* enters
   the save** and the file-local becomes irrelevant. It does **not** stop the
   module's own **code** entering the save via a persisted thread stack, which is
   F86 and which affects all three options equally. **Cost:** band 3 stops
   distinguishing a broken oxygen factory from a dome breach *and* from anything
   the player hand-set to max (`DRONE_PRIORITY_SYSTEM.md` §6.2). That cost was
   judged too high when the alternative looked free. **It is no longer free.**
3. **A merged-view overlay.** Keep hub queues at vanilla `-1..3`; hold band 4-5
   in **non-persisted mod-side tables**; wrap `TaskRequestHub:FindTask`
   (`_TaskRequest.lua:72`) to pass a merged view to `Request_FindTask`. Would
   sidestep **both** constraints. **UNPROVEN AND UNSCOPED** — `FindTask` is hot
   (every idle drone, constantly), so it needs caching and invalidation, and
   every other queue path must agree with the overlay.

**Your job:** present these accurately, answer questions from source, and — if
the owner asks — run a **time-boxed feasibility pass on option 3**, because it is
the only one that could deliver the bands *and* clean uninstall. **Report what
you measure. Do not advocate a design into existence.**

---

## 4 · After the decision — what the build looks like

Only once the owner has chosen:

1. **Write a build brief** against the chosen design (a separate doc, following
   `WORKFLOW.md`'s required elements). Nobody builds from this prompt directly.
2. **The design-drift disclaimer is MANDATORY** and ships with the module
   (spec in `docs\archive\DRONE_RESEARCH_BRIEF.md`). It can now be written honestly,
   because Q2 is answered: **the rebuild cannot inherit D06 v1's *"savegame
   footprint: none"*.** State what was actually done, the limits without hedging,
   and the off-ramp. **Not legal cover** — "use at your own risk" tells a player
   nothing.
3. **ONE multi-step playtest replaces PT-52 entirely.** One item, numbered steps,
   one sitting, covering the overhaul as a single product — matching how it ships.
   **Do NOT create a family of drone PTs. That is the failure mode the freeze
   exists to end.** On approval, the frozen PT-52 sections are **deleted** from
   the checklist and recorded in `PLAYTEST_ARCHIVE.md` as
   **deprecated-by-redesign** — obsolete, *not* un-run, and never reported as
   outstanding coverage.

**⛔ THE DRONE PLAYTEST FREEZE IS STILL IN FORCE.** PT-52 Triggers A/B/B2 test
D06 v1's design and the design is unsettled. **Do not run them.** **PT-10 is
explicitly NOT frozen** (F55, dome entity data — untouched by any dispatch
redesign). F77's defect is real and ships default-on; only its *test packaging*
is caught in the freeze.

---

## 5 · Reading order for any drone session

1. `docs\agent\ENGINE_FACTS.md` — whole file. **It now carries the closure-persistence
   fact**, which is why the overlay option (3) must never store a function on a
   game object.
2. **`BUGS.md` D06 entry** — the plan of record, including the owner decisions on
   relocation and the cleanup mod.
3. **`docs\reports\DRONE_PRIORITY_SYSTEM.md` — §8, §9 and §10 especially.** These are the
   new, decisive sections. §1 and §7 carry corrections to earlier claims.
4. `docs\archive\DRONE_RESEARCH_BRIEF.md` — now historical (all gates answered); keep it
   for the freeze rules and the disclaimer spec.
5. `docs\reports\DRONE_OVERHAUL_OPTIONS.md` — only if D08 or D06-structural comes up.
6. `docs\agent\FIX_POLICY.md` §1.5 and §3 — replacements and savegame footprint.
7. `docs\FUTURE_IDEAS.md` — the scope brake.

**Game source (read-only, NEVER modify):**
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
**Check `Mars.exe` is NOT running BEFORE touching loadable code** (`tasklist`),
as its own step — not in the same command as the edit.

---

## 6 · Live progress list — REQUIRED

**Create a todo list covering the whole job before you start**, and keep it
current. The owner reads it to decide **when to step in** — a stale list actively
misleads that decision.

- **⚠️ GRANULARITY IS THE RULE THAT ACTUALLY FAILS: one item per
  commit-and-verify unit.** If a stage produces its own commit or its own
  verification run, it gets its own checkbox. Never bundle several behind one.
  *(Phase 4 carried four waves, four commits and four legs behind a single item,
  and the owner lost visibility across the longest stretch of the job.)*
- **If a stage turns out to contain more units than expected, expand it in the
  list at that moment.**
- **Mark each item done the moment it completes** — never as a batch at the end.
- Exactly **one item in progress** at a time.
- Put useful state in the item text (which stage, what the last read said).

---

## 7 · Stop conditions — permission, not failure

**Stop and report** rather than pushing through, when:

- **The owner has not chosen a design** and the next step would commit to one.
- **A measurement contradicts a claim in the docs.** Three doc corrections came
  out of the last sitting; the docs are not above the evidence. Correct the doc
  in the same commit as the finding.
- **An experiment would touch a save the owner cares about.** Use a throwaway or
  a new game. The last experiment **broke a live colony** because a header
  asserted "inert" without testing it.
- **You are about to widen the priority range on an existing save.** Don't —
  every hub in it has narrow tables (§8). New game, or top up every hub first.
- **A fix would store a function on a persisted game object.** That is a
  permanent, un-removable savegame modification (ENGINE_FACTS).
- **The work is drifting out of scope** (§1).

---

## 8 · What may NOT be claimed

If you cannot cite evidence, **say the narrower true thing instead.**

- **Do not claim "no behaviour changed"** from a green harness leg. Probes drive
  planted globals and cannot see a real colony.
- **Do not claim band ordering.** Q1 proved bands 4-5 are *visible and consumed*.
  A **precedence** signal was seen once (band 4 finished while band 3 still had
  52000 outstanding) and is recorded as **suggestive, n=1, assignment luck not
  excluded**. It is not a proven ordering guarantee.
- **Do not claim the duplicate leak's magnitude.** It read `4 → 6` once, on one
  hub, in one save. The mechanism is source-backed and the arithmetic fits; a
  second observation on a clean fixture would make it solid.
- **Do not claim uninstall safety at all — the module is a PROVEN F86 leak
  site.** The old wording here ("loads clean, no errors, work stranded, heal path
  expires") described the *priority data* and is still true of it. It is **not**
  true of the module: `Opt_DroneOverhaul`'s `Drone:Idle` wrapper is serialised
  into the save and throws 98 errors per session after removal, toggle OFF
  included. Measured 2026-07-31, `BUGS.md` F86.
- **Do not report a module `tested`** without a playtest. Only the playtest flips
  that status.
- **Do not describe the cleanup mod as approved.** It is **not approved to
  build** — and note its stated justification ("mods get no save hook") is
  **false**; `SaveGameStart` reaches mods. If you repeat the cleanup-mod case,
  make it on grounds that survive that correction.
- **Do not assume any F86 remedy.** The three-layer redesign in
  `docs\reports\SAVE_SAFETY_REDESIGN.md` is a **proposal awaiting an owner decision**.
  Do not build against it, and do not treat D06's shape as constrained by a
  layer that has not been chosen.

---

## 9 · Commit and close-out

Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only). Commit messages via
`git commit -F <file>` — **no embedded double quotes** (PowerShell 5.1 splits
them). Parse sweep before any commit touching Lua: python + luaparser,
`ast.parse(open(f, encoding='utf-8-sig').read())`.

**End of a drone session:** record findings on the D06 entry and in
`DRONE_PRIORITY_SYSTEM.md`, add a `SESSION_LOG` leg, **update this prompt in
place**, and — if the general state changed — say so in `STATUS.md`. Then
summarize for the owner.
