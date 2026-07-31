# Future Implementation Ideas — parked until AFTER launch

Created 2026-07-31 by owner decision. This file exists because of one measured
problem: **mission creep.** Every three items fixed or tested were adding about
six more, so the finish line moved further away the more work got done. This is
where good ideas go so they stop competing with launch.

---

## ⛔ THE HARD RULE — read this before adding or reading anything below

**Nothing in this file is work.** Not owed, not scheduled, not queued, not
"pending", not counted against any gate, and not to be reported as outstanding.
An agent reading this file has read a wish list, not a backlog.

- **Nothing here gets built, further speced, estimated, researched or
  prototyped until the core mod has LAUNCHED.** Not "while we're in there
  anyway". Not "it's only small". Not as a rider on another task.
- **Un-parking an item is an explicit owner decision, one item at a time,
  after launch.** Filing something here is never partial approval, and an
  item's presence here is never evidence anyone wants it.
- **Do not use this file to justify new work elsewhere.** If an idea here
  makes some other in-scope task look incomplete, the other task is still
  scoped as written.
- **Adding to this file is not progress.** Prefer not filing at all over
  filing something speculative.

If an item genuinely blocks launch, it does not belong here — say so plainly
and put it on the real board instead.

---

## What belongs here

Enhancements, feature-completions, quality-of-life additions, and refactors
**with no proven player-facing defect behind them**. Things that are genuinely
good ideas — this is not a rejection bin.

## What NEVER belongs here

- **Defects.** A proven bug stays in `BUGS.md` with a real status (`todo`,
  `fixed`, `wontfix`). Deciding not to fix one is a **`wontfix` with written
  reasoning**, not a filing here. If defects start migrating into this file,
  `BUGS.md` stops being the authority on defect truth and the whole documented
  trail breaks. This is the one rule with no exceptions.
- **Verification owed on something already shipped.** PT items stay on the
  checklist. Shipping code and then parking its test is how a pack ships
  broken.
- **Rejected ideas.** Those get recorded where they were rejected, with the
  reason, so nobody re-proposes them. (Example: multi-hop passenger routing,
  rejected 2026-07-30 — it is not parked, it is refused.)
- **Release-blocking tasks** (store assets, portal rules, packaging). Those are
  launch work.

## How to add an entry

Six lines, no more: **what** it is · **why it is a good idea** · **why it is
parked** · **where the existing material lives** (so nothing is re-researched
from scratch later) · **rough cost** · **what it would need to un-park**.

---

# Parked items

## 1. Seniors in workshops — "vocation in retirement"

**What.** Let Seniors work the three vocation Workshops (Art / VR /
Biorobotics), which they currently cannot.

**Why it is a good idea.** The Workshops are the designed late-game
employment-and-morale sink, and Seniors are exactly the population with nothing
to do and a Comfort problem. Thematically it is the strongest fit in the game.

**Why it is parked.** Two real costs, neither small. It needs
**work-eligibility surgery** (not a knob), and it **collides with D07's
employed-senior exemption** — a senior who takes a workshop job would stop
cohort-migrating, which is the behaviour D07 exists to provide. So it is not an
addition to D10; it is a change to D07's contract.

**Where the material lives.** D10 entry in `BUGS.md` (the "Deferred (recorded,
NOT in this module)" bullet); D07 entry for the exemption it collides with.

**Cost.** Own module or an explicit D07 amendment + own decision + own
playtest. Not a rider on D10's PT-57.

**To un-park.** Owner decides the D07 interaction first — does an employed
senior still cohort-migrate, or not? Everything else follows from that answer.

---

# ⏸️ PROPOSED for parking — awaiting the owner's yes/no

Listed, not moved. Each is currently still on the live board, and each stays
there until the owner says otherwise. A single "yes to all" is enough.

**A. D08 — Drone Hub Extender overhaul + Command Center.** Five layers speced
in `DRONE_OVERHAUL_OPTIONS.md` with a risk table. *Strongest candidate on this
list:* it is the single largest scope sink still open, nothing is built, it is
already gated on both a QA review and PT-20, and the whole document carries a
mandate-change banner — it was designed **before** the reachability/§4a turn, so
it needs re-reading against current policy before a line is written. Parking it
costs nothing today.

**B. Audit Phase 4 — core-helper extraction, module merges, deactivation
surface.** Pure refactor across 74 modules with **no player-visible benefit**
and real regression risk, immediately before launch. *Second strongest
candidate.* Phases 1-3 already landed and are what actually mattered.

**C. D01 export half — standing PreciousMetals demand (+ F56 auto-offload).**
By its own entry's verdict this is **not a defect** — it is fidelity to the
original game. Needs three research questions answered, a design pass, a probe
and a playtest, and it must decide F56 in the same pass. The design decision
itself is already made (match the original, no invented thresholds), so nothing
is lost by parking it.

**D. D01 `on_activate` demand refresh.** Pure polish on an
already-accepted limitation (see the answer above). Small, but it is the
definition of "good idea, not needed now".

**E. D11 — shuttle same-pair passenger batching.** Low severity, never
green-lit, and it is a feature rather than a fix. Parking it also removes a
standing "ask the user fresh" obligation from the board.

**F. F79 — trains never serve service trips.** Confirmed vanilla gap, would be
a feature-completion D-item. Parking it converts an **owed decision** into a
parked idea, which reduces the decision load as well as the build load.

**G. D06 structural iteration beyond knobs** (H-v2 demand filter, registration-H,
balancer C). The shipped D06 core is opt-in and experimental; knob tuning stays
available as a mechanical change. Only the **redesign** would park. ⚠️ Note the
PT-52 B2 stress re-run is a **test of what is already built** and must NOT park
with it.

### Deliberately NOT proposed for parking

- **D10 and D12** — decided, approved, gate open. These are the launch build.
- **PT-59, PT-53 Trigger E, PT-54, PT-52 B2** — verification of shipped code.
- **The needs-eyes observations** (Detailed Scan recoverability, F85's tier,
  the storybit reconnect) — minutes each, and they grade **defects**.
- **The FIX_POLICY §4 amendment** — it is the rule that decides what is allowed
  to be built at all, and it currently carries a live contradiction affecting
  F49(a). Cheap, and it is itself a brake on scope creep.
- **F84 / D10 T1 localization call** — already bundled into a build that is
  happening; splitting it creates the second decision this pairing exists to
  avoid.
