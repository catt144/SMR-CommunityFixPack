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

Listed, not moved. Each is still live on the board until the owner answers. A
single "yes to all" is enough. Each entry says **what it actually does**, **what
it touches**, and **why park it** — the short names alone are not
self-explanatory.

---

### A. D08 — Drone Hub Extender overhaul + Command Center  ⭐ strongest candidate

**What it does.** Five independent layers, all unbuilt:
1. **Dispatcher** — today a building covered by an extender registers only to
   that extender's *uplink* hub; this makes it register to **every hub within
   legal drone reach**, and lets D06's existing claim gate arbitrate. No new
   scoring system.
2. **Cluster scoping** — a player-authored "these hubs are one logistics zone"
   grouping, as a *subset* of the geometric set.
3. **Adjustable extender radius** — the original request; today the hub slider
   can only ever SHRINK below default (max == default).
4. **Command Center drone tab** — a dedicated drone tab rather than columns
   bolted onto the Transportation tab.
5. **"Drone Command Center" building** — a unique building that owns dispatch.

**What it relates to.** D06 (`Opt_DroneOverhaul` — its claim gate is what layer
1 feeds), F77 (extender flap churn — the debounce pattern layer 1 would reuse),
PT-20 (layer 5 is gated on it), and the drone leash constant
`DroneRestrictRadius`, which is why job-relaying is permanently off the table.

**Why park it.** The largest scope sink still open and **nothing is built**.
Already gated on a QA review *and* PT-20. Critically, the whole document carries
a mandate-change banner: **every layer was designed BEFORE the reachability/§4a
turn**, so it needs re-reading against current policy before a line is written.
Parking costs nothing today.

**Material.** `DRONE_OVERHAUL_OPTIONS.md` (design record + risk table + five
open questions).

---

### B. Audit Phase 4 — core-helper extraction, module merges, deactivation surface  ⭐ second strongest

**What it does.** Three refactors of our own code, no gameplay change:
- **C2 helper extraction** — the `log()` helper is cloned in 11 files plus 5
  inline variants (6 copies missing the `%%` escaping that 00_Core documents as
  a crash class); ~154 self-check preflight sites share one loop shape; the
  status-gate prologue appears ×20; the LoadGame sweep skeleton ×6. Candidates:
  `Require{}`, `WhenActive(id, fn)`, `DataPatch(id, opts)`, `SetGlobal()`.
- **C3 merges** — the track-salvage trio F45/F44/F47, the DustSickness pair, the
  weather family F02/F78/F81, F55/F57b. *Audit's own finding: no fix was
  redundant and no load-order sensitivity was found.*
- **C4/C1 deactivation surface** — a user-visible "N fixes deactivated after
  game update" report, since 29 of 74 modules are full replacements pinned to
  build `1.0.7.396349`.

**What it relates to.** Every module in `Code/`. A `DataPatch` runner would also
fix audit finding A1 structurally rather than by hand.

**Why park it.** Pure refactor across 74 modules with **zero player-visible
benefit** and real regression risk, immediately before launch. Phases 1-3
already landed and were the part that mattered. The C1 replacement risk it would
mitigate is **already covered by a release gate** — the after-every-patch fpk
extraction diff.

**Material.** `docs/archive/AUDIT_FINDINGS.md` (C1-C4 + the PLAN).

---

### C. D01 export half — standing PreciousMetals demand (+ F56 auto-offload)

**What it does.** Restores the ORIGINAL game's behaviour where every landed
rocket carries a standing `PreciousMetals` export demand up to its
`max_export_storage`, gated by a per-rocket `allow_export` toggle — so drones
fill a parked rocket with rare metals without the player driving the payload
dialog. It also **owns F56** (auto RC Transports never offload into rockets),
which must be decided in the same pass so a player can't get emptying without
refilling.

**What it relates to.** `Opt_ClassicRockets` (the shipped fuel half rides the
same toggle), F56, and the same machinery as F50/F68/F70/F71.

**Why park it.** By D01's own verdict this is **not a defect** — it is fidelity
to the original. It needs three research questions answered, a build, a probe
and a playtest, and it edits a busy shared system. The *design* call is already
made (match the original, no invented thresholds), so nothing is lost by
waiting.

**Material.** D01 entry in `BUGS.md` (research questions listed).

---

### D. D01 `on_activate` demand refresh

**What it does.** Makes a mid-session enable of `ClassicRockets` take effect on
a rocket that is **already parked**, instead of only on rockets that land after
the flip. Today the wrap sits on `GetFuelResourceRequest`, which is only
consulted when `UpdateCargoResourceRequests` runs — and nothing re-triggers that
for a parked rocket. An `on_activate` would re-run it on parked,
destination-less player rockets.

**What it relates to.** `Opt_ClassicRockets`, D05's reconciler (this is
`on_activate`'s intended use per FIX_POLICY §5), PT-55 (which found it).

**Why park it.** The limitation is **already accepted by owner decision**
(2026-07-30) and documented; a parked rocket picks the behaviour up on its next
landing. Pure polish.

---

### E. D11 — shuttle same-pair passenger batching

**What it does.** Lets one shuttle carry several colonists on a trip when they
share the same origin→destination dome pair. Today the limit is **1 passenger
per shuttle and it is structural**, not a tunable: one `ColonistTransportTask`
per colonist, `transport_task.colonist` singular.

**What it relates to.** `ShuttleHub`; adjacent to the shuttle cargo limit (3,
modifiable) and shuttles-per-hub (10, modifiable), neither of which is the
constraint here.

**Why park it.** Low severity, never green-lit, and a feature rather than a fix
— and the "1 passenger" limit is structural, so it is not a small change.
Parking also clears a standing "ask the owner fresh" obligation off the board.
⚠️ **Multi-hop passenger routing stays REJECTED** — that is refused, not parked,
and must not be re-proposed.

---

### F. D06 structural iteration beyond knobs

**What it does.** The redesign options above the shipped core: **H-v2** demand
filter, **registration-H**, **balancer C**. The shipped D06 is the veto variant
of option H plus option A.

**What it relates to.** `Opt_DroneOverhaul`, and D08 layer 1 (which would feed
the same claim gate).

**Why park it.** D06's core is opt-in and **experimental**, and the structural
choice was always gated on measurement. **Knob tuning stays available** as an
ordinary mechanical change — only the redesign parks.

⚠️ **The PT-52 Trigger B2 stress re-run does NOT park with it.** That is a test
of code already shipped, and parking a shipped module's verification is barred
by this file's own rules.

---

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

### Decided and CLOSED — not parked, do not re-file

- **F79 — colonists never use trains for services.** `wontfix` 2026-07-31,
  owner decision: the risk of new issues exceeds the benefit, especially on a
  large multi-stop end-game map. Two facts on file back it — the train boarding
  layer already has an **open, unexplained** defect (F80), and the fix sketch
  post-wraps `Dome:GetService`, a hot path, adding a station walk that scales
  with exactly that map shape. **This is a decision, not a deferral: it is not
  parked, not owed, and F80 must be explained and closed before it could ever be
  revisited.** Full reasoning on the F79 entry in `BUGS.md`.
- **Multi-hop passenger routing** — REJECTED by the owner 2026-07-30. Refused,
  not parked. Do not re-propose.
