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

## 2. D01 `on_activate` demand refresh — parked 2026-07-31  **[FAQ]**

**What.** Make a mid-session enable of `ClassicRockets` take effect on a rocket
that is **already parked**, instead of only on rockets that land after the flip.
Today the wrap sits on `GetFuelResourceRequest`, which is only consulted when
`CargoTransporterNew:UpdateCargoResourceRequests` runs — and nothing re-triggers
that for an already-parked rocket; the landing path is what does. The hook
answers correctly, nobody asks it. An `on_activate` would re-run it on parked,
destination-less player rockets.

**Why it is a good idea.** It would make the toggle feel instant instead of
"works from the next landing".

**Why it is parked.** Owner, 2026-07-31: *"its not a high priority, the mod
functions flawlessly, besides a already parked rocket when activated… Touching
it just invites a regression."* The limitation was already **accepted by owner
decision on 2026-07-30** and is self-correcting — the rocket picks the behaviour
up on its next landing. **Documented instead of built:** a player-facing note is
in `MOD_DESCRIPTION.md` under the Classic rocket behavior module.

**Where the material lives.** D01 entry in `BUGS.md` (PT-55 found it; cause
confirmed in source).

**Cost.** Small — but it touches a working module's activation path, which is
the regression surface the owner named.

**To un-park.** Only if the limitation actually grates in play.

---

## 3. D11 — shuttle same-pair passenger batching — parked 2026-07-31

**What.** Let one shuttle carry several colonists on a trip when they share the
same origin→destination dome pair. Today the limit is **1 passenger per shuttle
and it is structural, not a tunable**: one `ColonistTransportTask` per colonist,
`transport_task.colonist` singular (`ShuttleHub.lua:635+`). For contrast, the
limits that ARE modifiable are cargo/shuttle (3) and shuttles/hub (10) — neither
is the constraint here.

**Why it is a good idea.** Owner, 2026-07-31: *"I love this idea."* Shuttle
passenger throughput is a real late-game pinch, and no breakthrough, law or tech
in the game touches it.

**Why it is parked.** Owner, same message: *"I think its something that has
decent risk."* Correct — because the 1-passenger limit is **structural**, this is
not a knob change; it means reworking the transport task model that colonist
movement depends on.

**Where the material lives.** D11 entry in `BUGS.md` (full shuttle-limits
research, all source-verified).

**To un-park.** Post-launch, and only with a clear-eyed look at the task-model
rework first.

⚠️ **Multi-hop passenger routing is REJECTED, not parked** — refused by the
owner 2026-07-30. Do not re-propose it as part of this.

---

## 4. Save-rescue framework — proving and extending it — parked 2026-07-31  **[FAQ]**

**What.** The pack ships two automatic save-repair passes (F35 Large Wind
Turbine buff, F03 leaked upgrade modifiers) plus per-fix LoadGame repairs in
eight other modules. Parked here: **proving the repair half against real broken
saves**, and extending the framework to damage patterns we have not seen yet
(F48's station-connector fixup is the known one we deliberately left out).

**Why it is a good idea.** Rescuing a save someone has put 200 sols into is the
single most valuable thing this pack could do for an individual player.

**Why it is parked.** Owner, 2026-07-31: *"I like the core idea of rescuing
saves, but I think unless we have player saves to test it's hard. And shouldn't
be a launch gate."* Agreed on both counts — the F35 fixture in particular
requires a save that researched Frictionless Composites **before the game
patched the tech**, which only a donated community save can provide. Shipping
the framework as-specced with **honest wording** is the right call: the
`MOD_DESCRIPTION.md` section now says plainly that it is a genuine attempt and
not a guarantee, that a save broken another way may get no benefit, and that we
intend to improve it as real cases turn up.

**Specifically parked:** PT-35 **case B** (forced F03 leak — needs a fixture
built with the pack disabled) and **case C** (F35 — needs a donated save).

**⚠️ NOT parked — PT-35 case A**, the do-no-harm check. Both passes run
automatically on **every load for every player**, and F03 **removes** modifiers
from persisted colony state. Case A needs no fixture (any healthy save), takes
~5 minutes, and is the only live observation that the framework does not damage
a colony it was not meant to touch. Parking a shipped module's do-no-harm check
is barred by this file's own rules.

**Where the material lives.** `Code/90_SaveSanitizer.lua` (both passes, with the
conservatism argument in the header and the F48 exclusion reasoned out); PT-35
in the checklist; F03/F35/F48 entries in `BUGS.md`.

**To un-park.** A donated broken save, or a credible player report after launch.

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



### F. D06 structural iteration beyond knobs

**Plain English first.** D06 is the opt-in "drone dispatch overhaul". The
problem it attacks: a hub on the far side of the map can claim a job that a
nearby hub's idle drones should have taken, because drones are leashed to their
own hub and cannot relay work. **What actually shipped is a narrow version** —
a *veto* at the moment of claiming, plus letting idle drones help a neighbouring
hub that has none. "Structural iteration" means the **bigger redesigns that were
speced but deliberately NOT built**, each of which changes how work is
distributed rather than just tuning the shipped behaviour:

| Option | What it would do | Status |
|---|---|---|
| **H (registration)** | Instead of vetoing a bad claim *after* the fact, control which hubs a request is ever **visible** to — closest hub first, escalating outward only if it is overloaded. Hooks `ShouldAddRequestToCommandCenter`. | The *veto* variant of H shipped; **full registration-H did not** |
| **H-v2 (demand filter)** | Narrower still — filter by demand. Only worth it if live data shows the **delivery** leg (depot→building) dominating. Needs the shuttle deficit-table ripple assessed first. | Not built |
| **B (full moonlighting)** | Hand the whole job to the neighbouring hub's own matcher, **including haulage** — much broader than the shipped repair-only help. | Not built |
| **C (migration balancer)** | A slow sweep (every ½ sol) that physically **migrates idle drones** from a slack hub to an overloaded one, so imbalance self-corrects instead of just being survivable. | Not built |
| **D / E** | Largely superseded by H; E (reassigning already-claimed work) stays a last resort. | Not built |

**What it relates to.** `Opt_DroneOverhaul`; D08 layer 1 (which would feed the
same claim gate); and the rocket cargo path F50/F68/F70/F71, because these are
**the deepest shared queues in the game**.

**Why park it.** Three reasons, all on file. The shipped core is **opt-in and
explicitly experimental**. The structural choice was **always gated on
measurement** — the PT-52 B2 stress re-run — and that measurement has not
happened, so choosing now would be guessing. And the design doc's own **global
risk statement** says any subset approved must re-pass the F50 rocket-churn and
F55 unreachable scenarios plus a new probe set before shipping — that is a large
verification bill for an experimental opt-in module, immediately pre-launch.

**Knob tuning stays available** (STRIKES_MAX, STRIKE_TTL, MOONLIGHT_MAX_HEXES,
cache TTLs) as an ordinary mechanical change. Only the redesign parks.

⚠️ **The PT-52 Trigger B2 stress re-run does NOT park with it.** That is a test
of code already shipped, and parking a shipped module's verification is barred
by this file's own rules. It also stays useful independently: it tells you
whether the shipped core is doing anything at all.

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
