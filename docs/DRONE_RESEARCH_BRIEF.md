# Drone rebuild — the four experiments that must run BEFORE any design is fixed

Queued 2026-07-31. **Do not start this while the Phase 4 rebuild is in flight** —
that job is rewriting `Code/`, these experiments need temporary modules in the
same directory, and running both at once produces a fingerprint diff nobody can
explain. Wait for Phase 4 to report, then run this.

---

## Why this exists

D06 was built, shipped, and *then* measured — and the measurement returned a
null result that said nothing about the design, because the instrument was
pointed at the wrong leg. **That is the mistake this brief exists to not
repeat.** Four questions currently gate the drone rebuild's design. Three of
them can kill or reshape it. None of them is expensive.

**Nobody writes the rebuild brief until these are answered.** If an answer makes
the intended design impossible, that is a success — it cost one sitting instead
of one module.

---

## The design these questions gate (context only — NOT approved)

Working shape, owner-directed 2026-07-31:

| Band | Assigned by | Contents |
|---|---|---|
| **5** | auto | malfunctioned life-support — producers, plus the grid/dome tier the game already elevates |
| **4** | auto | every other **malfunctioned** building — decoupled from the player's arrows |
| **3** | player | supply allocation, "high" |
| **2** | player | supply allocation, "normal" (default) |
| **1** | player | supply allocation, "low" |
| 0 | engine | storage depots |

Plus a **data-patched default of 3 for food service buildings** (see Q3).

The reasoning behind it is in `DRONE_PRIORITY_SYSTEM.md`. Two points from it
that these experiments must respect:

- The **player's arrows answer a supply-allocation question**, not a repair
  question. Repairs currently inherit that answer, set once, early, and never
  revisited. Elevating repairs out of the player's scale restores the arrows to
  meaning what a player thinks they mean.
- The split is on **`is_malfunctioned`** (`RequiresMaintenance.lua:41`, *"no work
  possible"*) — elevate **broken**, not merely degrading. Routine maintenance
  top-up genuinely *is* a supply question and stays on the player's scale.

**Ship discipline, owner decision:** the overhaul is **one toggle, all or
nothing**. No sub-toggles. Separate toggles multiply the configuration matrix
and every combination is an unmeasured product — which is how D06 got here.
D09's stat dials stay separate; they are a player-set value with a clean off
position and are already `tested`.

---

## Q1 — Does the C matcher honour a widened priority range? **(decisive)**

**Why it decides everything.** The design needs two automatic bands above the
player's three. The Lua half is configurable by design: `MinBuildingPriority` /
`DefBuildingPriority` / `MaxBuildingPriority` are module locals read from the
`const.TaskRequest` settings group at `ClassesPreprocess`
(`CommonLua/TaskRequest.lua:20-30`), the game **does not currently define that
group**, and mod code loads before `ClassesPreprocess` fires. Queue allocation
follows the bounds (`TaskRequest.lua:251-255`), as does the player's scrollbar
(`Building.lua:199`, `max = const.MaxBuildingPriority`).

**But the matcher is C.** `TaskRequestHub:FindTask` (`Lua/_TaskRequest.lua:71-83`)
passes `priority_queue`, `supply_queues` and `demand_queues` **as tables** into
`Request_FindTask`. Whether the C side discovers the key range or has `-1..3`
baked in **is not readable from source**.

**The experiment.** Temporary module: set `const.TaskRequest` with
`MaxBuildingPriority = 5` at file scope. Confirm the hub allocates queues at 4
and 5. Then place one real request at priority 4 and observe whether a drone
ever takes it.

**Outcomes:**
- **Honoured** → the band scheme is viable; proceed to Q2.
- **Ignored** → requests filed at 4-5 are invisible to the matcher and would be
  **silently lost**. The band scheme is dead as designed, and the rebuild falls
  back to working inside `-1..3` (which means using band 3 for life-critical
  repairs only, and accepting that it is shared with the player's own maximum).
  **Report this immediately — it changes everything downstream.**

⚠️ Do not conclude "honoured" from queue allocation alone. Allocation is Lua;
consumption is the question. A drone must actually perform the work.

---

## Q2 — Are hub queues persisted, or rebuilt on load?

**Why it matters.** This is the uninstall-safety question, and it is also open
question #1 in the D08 section of `DRONE_OVERHAUL_OPTIONS.md`, so it pays for
itself twice.

The design keeps `building.priority` inside `1..3` always, so the **persisted
property** is vanilla-safe and reverts cleanly when the mod is removed. The
residual is whether the **hub queues themselves** persist carrying bands 4-5.

**Outcomes:**
- **Rebuilt on load** → completely clean. Vanilla recomputes every request
  through its own `GetPriorityForRequest`, everything lands in `1..3`, nothing
  to find. No further mitigation needed.
- **Persisted** → requests sitting at 4-5 at save time land in tables vanilla
  never iterates, and `_InternalRemoveRequest` also loops `-1..3` so it cannot
  clear them. That is an **orphaned entry, not corruption**, and it should
  self-heal on the next `ReconnectTaskRequesters` (which vanilla triggers
  routinely). Confirm the self-heal actually happens rather than assuming it.

---

## Q3 — Do the two data tests cleanly identify what we think they do?

Both classifications must be **data tests, not hardcoded lists** — a list needs
maintaining and silently misses anything a patch or DLC adds. This is the same
reasoning that makes an R3 finding shippable where an R4 is not.

**3a. Life-support producers.** `air_production` and `water_production` are real
building properties (`Building.lua:2637-2640`); `LifeSupportConsumer` and
`LifeSupportGridObject` are real classes. Enumerate every building the test
catches and **eyeball the list**. Questions it must answer: does it catch the
obvious producers? Does it wrongly catch something trivial? What about a power
plant feeding an oxygen factory — in or out, and why?

**3b. Food service buildings.** There is **no "food service" class** — `Grocery`
and `DinerBase` are both plain `ServiceWorkplace` (`Diner.lua:1-6`), which also
covers non-food services. Proposed test: **any service carrying a demand request
for `Food`**. Enumerate what it catches and confirm it does not sweep in
unrelated services.

**Owner's observation to verify while here:** food service buildings *do* have a
`priority` property (default 2, player-settable) — what they lack is anything
distinguishing them, so they are outranked the moment a player raises a few
other buildings, without ever touching food. Confirm that reading.

---

## Q4 — Does changing a property default reach buildings already in a save?

**Why it matters.** `priority` is a property with `default = 2`
(`Building.lua:199`). Property objects commonly omit default-valued properties
when persisting. So:

- **Defaults omitted from saves** → changing the default silently re-rates
  **every existing Grocery** in a loaded save, and reverts cleanly on uninstall.
  Probably the desired behaviour — but it must be a known choice, not a
  surprise.
- **Values stored explicitly** → only newly-built buildings change; existing
  colonies see nothing at all.

Those are two materially different products. **Do not ship a description
claiming either until this is measured.** The owner rates this the cheapest
playtest on the board: load a save, read a Grocery's priority.

---

## The design goal Q3b and Q4 actually serve — state it correctly

The food default is **not** primarily a throughput change, and it should not be
justified as one. Owner's framing, 2026-07-31, and it is the better one:

> A player who hits the food warning and jumps to the dome sees one of two
> things. **Full pallet** → *"this game sucks, drones are stupid."* **Empty
> pallet** → *"I under-built, I need to fix this."* Same starving colonist,
> opposite conclusion, and only one of them ends up on a forum.

The goal is **correct attribution of failure**: a full pallet next to hungry
colonists should stop being a state the game reaches casually. That
justification holds even when the player genuinely *is* under-producing, which a
throughput argument does not.

---

---

## ⛔ The drone playtest freeze — in force NOW, and what these answers obligate

**Owner decision 2026-07-31: no drone playtesting until a final drone plan is in
place.** The banner lives in `PLAYTEST_CHECKLIST.md` §1; this is the pointer.

**Why it exists.** Drones are the one part of the pack that was iterated
piece-by-piece, and testing followed the same pattern — *"they keep getting new
playtests, and every time I get one half done we have another."* A half-finished
test of a superseded design costs a sitting and produces evidence about code
that is being replaced.

**Frozen (they test D06's design):** PT-52 Trigger A, Trigger B, Trigger B2.
**Not frozen (they test shipped bug fixes):** PT-10 (F55 — dome entity data,
untouched by any dispatch redesign). F77's defect is real and ships default-on;
only its *test packaging* is caught in the freeze, because it currently rides
inside PT-52.

**These experiments are NOT playtesting and are NOT frozen** — they answer
mechanism questions with temporary instrumentation. That distinction is the
whole point: measure the machine now, judge the product once, later.

**What a successful outcome obligates.** If these four questions answer and a
rebuild design is approved:

1. The frozen PT-52 sections are **archived as deprecated-by-redesign** —
   deleted from the checklist per the archived-sections-are-deleted-outright
   rule, reason recorded in `PLAYTEST_ARCHIVE.md`. They are **obsolete, not
   un-run**, and must not be reported as outstanding coverage.
2. **ONE multi-step drone playtest replaces all of them.** One item, numbered
   steps, run start to finish in a single sitting, covering the overhaul as a
   single product — matching how it ships (**one toggle, all or nothing**; D09's
   dials stay separate). **Do not create a family of drone PTs. That is the
   failure mode this freeze exists to end.**

---

## Rules for whoever runs this

- **Answer the questions. Do not design.** The rebuild brief is written *after*,
  against real answers. If you find yourself sketching the module, stop.
- **Do not build any part of the overhaul**, not even "while we're in there".
- **Temporary modules only**, clearly marked, deleted when the sitting ends.
  Nothing from this brief ships.
- **Report a negative result as loudly as a positive one.** Q1 returning
  "ignored" is the single most valuable outcome available here — it saves a
  module.
- Record every answer on the D06 entry in `BUGS.md` and in
  `DRONE_PRIORITY_SYSTEM.md` (§7 lists what was explicitly unsettled — move
  items out of it as they are settled).
- **Check `Mars.exe` is not running before touching loadable code.**
