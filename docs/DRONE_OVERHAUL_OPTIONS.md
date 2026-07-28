# D06 candidate — drone assignment overhaul, feasibility study (2026-07-28, game-free)

Commissioned by the user after the 2026-07-28 static investigation verdict (BUGS
DroneControl bullet + F77): *"what is even feasible if we want an optional overhaul
toggle — load balancing? handoff? distance/idle priority?"* Everything below is
static-analysis-verified against Src; **nothing is built**. The module would ship as
`Opt_*` behind a Mod Options toggle (D05 surface), off by default, per the D02-D05
convention.

## Ground rules — what is patchable and what is not (each verified)

These constraints shape every option:

1. **The C matcher cannot be reordered.** `Request_FindTask` / `Request_FindDemand` /
   `Request_FindSupply` are engine exports; their internal scan order is invisible and
   untouchable. Their **Lua callers** (`TaskRequestHub:FindTask` and friends,
   `_TaskRequest.lua:54-83`) are plain methods — wrappable, and callable BY US against
   any hub with any agent.
2. **Work requests (repair/clean/construct) live ONLY in `priority_queue`** — a plain
   per-hub Lua array of request userdata (`_TaskRequest.lua:118-121` adds
   `rfPostInQueue`; supply/demand queues only hold `rfSupplyDemand` requests). A Lua
   scan over them is legal and cheap; the userdata API we need (`IsAnyFlagSet`,
   `CanAssignUnit`, `GetTargetAmount`, `GetSource`, `GetResource`) is used from Lua
   game code everywhere.
3. **Claims are atomic and Lua-visible.** `RequestAssignUnit` is a global Lua function
   (`_TaskRequest.lua:352`); `Drone.lua` holds **no file-local alias** (grep-verified),
   so a wrapper installed from mod code IS seen by every drone claim. Claim happens
   inside `Drone:Work`/`PickUp` at command start (`Drone.lua:901,941`) with a benign
   failure path (Sleep + return to Idle).
4. **`Drone:Idle` falls through exactly when it found nothing** — the body ends with
   `Sleep(2000)` + `CleanUnreachables()` and returns; the command loop re-runs it. So a
   **chained post-wrapper runs precisely in the "idle with no work" case** (every ~2s
   per idle drone) — the natural dispatch hook. (When Idle DOES find work it
   SetCommands and the thread dies before our code — which is correct: vanilla own-hub
   priority is preserved for free.) The F73 "pre-wrap only" fact applies to command
   methods that always end in SetCommand (Colonist:Idle); Drone:Idle's fall-through is
   the exception that makes the post position usable.
5. **`Drone:Work` and `ApproachWrapper` never consult `command_center`**
   (`Drone.lua:898-938`, `:819-849` — only an optional `UpdateConstructions` ping).
   Requests are hub-agnostic C objects. **A drone can execute another hub's request
   with zero bookkeeping surgery.** Movement stays bounded by the engine's own
   RestrictArea (100 hexes-worth around the drone's OWN hub, `Drone.lua:227-230`).
6. **Drone migration between hubs is vanilla-blessed**: the player's reassign
   interaction is `Drone:SetCommandCenterUser(obj)` → `SetCommandCenter` + Idle/Reset
   (`Drone.lua:2687-2694`); orphan gathering and refab use the same primitives. Caps
   via `CanHaveMoreDrones()` (`g_Consts.CommandCenterMaxDrones`).
7. **The load signal already exists**: `CalcLapTime()` vs `const.DroneLoadLow/
   MediumThreshold` is the game's own heavy-workload metric (`DroneControl.lua:
   955-971`), and `GetIdleDronesCount()` is cheap. No new bookkeeping needed to know
   who is starved and who is slack.
8. **Coverage checks must be extender-aware.** A hub's effective area = own circle +
   every WORKING linked extender's circle, recursively (`FindTaskRequesters`,
   `DroneControl.lua:315-325`). Any option that asks "does hub H cover point P" must
   recurse `linked_extenders` the same way — a naive `HexAxialDistance(hub, P) ≤
   work_radius` silently ignores exactly the extender geometry this whole
   investigation is about.
9. **Savegame discipline is easy here**: every option below keeps only transient
   module-state (memos, ledgers) — nothing persisted, toggle-safe both directions via
   the D05 `IsActive`-per-call pattern.

## The options

### A. Repair-work moonlighting — idle drones serve neighboring saturated hubs' WORK queues
**What:** post-chain `Drone:Idle` (ground rule 4). When vanilla found nothing: skip if
the drone's controller is an RCRover/rocket (player-zoned fleets) or hub not working.
Otherwise iterate the city's `DroneHubBase`s (labels filter), take those that are
working, not own, **saturated** (`GetIdleDronesCount() == 0` — if the owner has idle
drones they'd take the work themselves), and scan their `priority_queue` high→low
priority for `rfWork` requests with `CanAssignUnit()` and target > 0 whose SOURCE is
(i) within a modest radius of the DRONE (25-35 hexes — near work only), (ii) inside
the drone's own RestrictArea with margin, and (iii) not in the drone's unreachable
cache. First hit → `SetCommand("Work", req, req:GetResource(),
Min(DroneResourceUnits[res], target))` — byte-parallel to vanilla's own maintenance
branch (`Drone.lua:602-605`).
**Feasibility: HIGH** — every piece verified above; no pairing logic, no C
reimplementation; the claim stays vanilla-atomic inside Work.
**Risk: LOW.** Worst case the claim fails (race) or approach fails (feeds the
unreachable cache exactly as vanilla does; F55's fix already retires those). Perf:
scan runs only in drones with literally nothing to do, ~every 2s, gated by the
saturation check + a per-hub last-miss memo (mirror of vanilla `no_requests_time`).
Accounting: forign work never touches the foreign hub's `lap_time` (we bypass its
FindTask), and our drone's own hub keeps its idle count until the command flips —
cosmetic at worst.
**Reward: HIGH for hypothesis (a) and for general idle-fleet utilization** — the four
observed drones would have picked up the PolymerPlant repair within ~2s. **Does NOT
help (b)** (a request already claimed by a far drone reads `CanAssignUnit() == false`
— see D/E).
**Effort:** small module (~100 lines + option toggle).

### B. Full moonlighting — delegate to the foreign hub's own matcher (haulage included)
**What:** same hook as A, but instead of a Lua queue scan, call
`foreignhub:FindTask(self)` — the C matcher does priority + supply/demand pairing,
so idle drones also *haul* for saturated neighbors, not just repair.
**Feasibility: HIGH** (one call), with two warts A doesn't have: it perturbs the
foreign hub's `lap_time` bookkeeping (`_TaskRequest.lua:77-81` — feeds the
heavy-workload notification), and the returned request can target the FAR END of the
foreign hub's territory (no max_dist parameter on FindTask), so a post-return distance
check + skip-memo is mandatory to avoid claim-then-unreachable churn (skip BEFORE
SetCommand — the claim only happens inside Work, so a skip is free).
**Risk: MEDIUM** — same class as A plus the two warts; the skip-memo must be
per-drone with TTL or the same far request is returned every poll.
**Reward: HIGH** if live data shows starved *haulage* (deliveries), not just repair.
**Recommendation:** ship A first; A's hook and gates are a strict subset — B is a
drop-in upgrade of the "find" step if the R1-R7 reads or the playtest show starved
supply/demand requests too.

### C. Idle-drone migration balancer — the "load balancing poll" (user's suggestion)
**What:** a slow periodic sweep (game-time thread, every 1/2 sol, or on the existing
`BuildingUpdate` cadence): for each pair (overloaded hub H, slack hub S) where H's
`CalcLapTime() ≥ DroneLoadMediumThreshold`, S has ≥ N idle drones, H
`CanHaveMoreDrones()`, and the hubs are within a distance budget — migrate
`min(idle-1, deficit)` idle drones S→H via the vanilla `SetCommandCenter` path with
hysteresis (max one move per pair per sol; never drain S below a floor; never touch
rover/rocket fleets or disabled drones).
**Feasibility: HIGH** — all vanilla primitives (ground rules 6-7); this is literally
automating what the player does by hand today.
**Risk: MEDIUM, but of a different kind — intent, not mechanism.** It *permanently*
rewrites the player's fleet distribution; a player who deliberately parked 12 drones
at a quiet hub will watch them walk away. Mitigations: opt-in toggle (given),
conservative thresholds (only act on the game's own "Medium/Heavy load" signal),
migrate only genuinely-Idle drones, and a Mod Options aggressiveness knob if wanted.
No sync/savegame risk (SetCommandCenter is save-clean).
**Reward: MEDIUM-HIGH and hypothesis-independent** — it fixes chronic imbalance at
the FLEET level, which neither A nor D can (they redistribute work, not workers), and
it reduces the far fleet's average haul length, which is the performance complaint.
Weakness: reacts on lap-time scale (slow), useless for acute single-building
starvation — that's A's job. A and C compose cleanly: A = fast/tactical,
C = slow/strategic.
**Effort:** small-medium (~150 lines; the care is all in hysteresis tuning).

### D. Near-idle claim veto — "distance/idle priority" at the only injectable point
**What:** the match order is C-side (ground rule 1), so preference can only be
injected at claim time: chain-wrap `Drone:Work`/`Drone:PickUp` (or `RequestAssignUnit`
itself) — before claiming, if the request's source building has a DIFFERENT covering
command center (extender-aware, rule 8) that is meaningfully closer AND has idle
drones, yield once (the shipped miss path: Sleep + return) and memo the request so the
second encounter claims normally (starvation-proof by construction).
**Feasibility: HIGH** mechanically.
**Risk: MEDIUM.** It inserts a delay into EVERY claim decision colony-wide (the memo
bounds it to one 1-2s yield per request per drone, but the code path is the hottest
in the domain); "closer hub's idle drone will take it" is a *prediction* — if that
drone's Idle poll misses (its own hub's C-scan picks a different request first —
order unknowable, rule 1), the yield bought nothing; and it perturbs F50/F68/F71
adjacent machinery (rocket cargo claims) unless class-filtered to repair work.
**Reward: targeted at hypothesis (b) ONLY — and (b) is unproven.** If R1/R3 show (a)
(registration gap), this option is dead weight.
**Recommendation:** do NOT build until the live reads confirm (b). If (b) is
confirmed, build it repair-work-only first.

### E. True handoff — reassign already-claimed work to a closer idle drone
**What:** wrap `RequestAssignUnit`/`RequestUnassignUnit` to keep a claim ledger
(request → holder, claim time). A watchdog (every ~10s) looks for `rfWork` claims
where the holder is still en route, far (say > 40 hexes from target), and an idle
drone of ANY covering hub sits within ~10 hexes of the target. Then:
`holder:SetCommand("Reset")` (vanilla interrupt — the Work destructor unassigns,
`Drone.lua:905-911`; `InterruptDrones` precedent `_TaskRequest.lua:290-314`) and
immediately `neardrone:SetCommand("Work", req, ...)` — whose own claim is atomic; if
it loses a race, both drones just re-idle.
**Feasibility: MEDIUM-HIGH** — all public primitives, but the most moving parts of
any option: ledger correctness across savegame load (ledger is transient — rebuild
lazily), holder state edge cases (restrict to `rfWork` claims only — NEVER touch
PickUp/Deliver claims, a resource-carrying drone must not be Reset), ping-pong
control (distance-ratio gate ≥ 3-4× + never hand off the same request twice per
X hours).
**Risk: MEDIUM-HIGH.** Reset mid-command is the F50 churn primitive — used
surgically it's fine, used wrongly it IS the bug we fixed. Player-visible U-turns.
**Reward:** the only option that rescues work already locked by a far claim — i.e.
the definitive (b)-killer, and the observed `target:0` reads suggest (b) moments
exist even if (a) is the root.
**Recommendation:** tier 3 — only after A (+D if (b)) prove insufficient, and only
with C's telemetry in place.

### F. Rewrite the matcher in Lua with distance-weighted scoring — REJECTED
Replacing `TaskRequestHub:FindTask` with a Lua matcher that scores
priority × distance × idle-time is the "real" overhaul — and the wrong move:
the C matcher's semantics (supply↔demand pairing, `rfWaitToFill`, restrictor tables,
`under_construction` gating, deficit interplay, `supply_dist_modifier`) are only
partially visible from Lua; a reimplementation guesses at engine behavior the
investigation explicitly recorded as unverifiable, runs in Lua at the hottest
call site (every idle drone × 2s × whole queue set — the exact loop the user already
reports as a perf problem), and rots on every game patch. All of A-E get the
locality wins without owning the matcher. Rejected on FIX_POLICY grounds
(full replacement of engine-opaque machinery, maximum rot surface).

### G. Supporting acts (cheap, mostly independent of the toggle)
* **F77 debounce** (extender flap churn) — a plain repair, ships as `Fix_*` regardless
  of the overhaul decision; sketch on the F77 entry. Without it, any overhaul fights
  periodic whole-fleet Idle-kicks whenever an extender blips.
* **`SMRFixPack.DroneReport()`** — console/TestKit telemetry: per hub — handle, class,
  working, drones idle/broken/total, `CalcLapTime` vs thresholds, per-priority queue
  depths, extender chains. Zero risk, ~40 lines, makes the next playtest *measure*
  instead of eyeball, and is the tuning instrument every option above needs. Build
  first whatever else is decided.
* **`no_requests_time` nudge** — wrap `TaskRequester:AddRequest` to clear covering
  hubs' empty-queue throttle when a new request posts: shaves up to ~1s off reaction
  time. Trivial, marginal, fold into the module if built.

## Recommended shape (user decision)

**Build order for an `Opt_DroneOverhaul` module (each independently toggleable in
spirit, one Mod Options switch in practice):**
1. **G-telemetry (`DroneReport`)** — before anything, so the next sitting quantifies
   the problem and every later change has a before/after.
2. **A (repair moonlighting)** — highest reward/risk ratio in the set; directly kills
   the observed four-idle-drones-next-to-a-wrench scene under hypothesis (a).
3. **C (migration balancer)** — the strategic half; conservative thresholds,
   sol-scale cadence.
4. **B (full moonlighting)** — upgrade A's find step if starved haulage shows up.
5. **D / E** — only if the R1-R7 live reads confirm (b) claim lockout; D first
   (repair-only), E as the last resort.
6. **F77 fix** — separate `Fix_`, ships with the next wave independent of all above.

**What still gates this:** the R1/R3 reads at a live starvation moment. They cost two
console pastes and decide whether the (b)-targeted options (D/E) are needed at all —
worth doing before committing to anything past step 3.

**Global risk statement (unchanged from the verdict):** this is the deepest shared
machinery in the game — hubs, rovers, and the rocket cargo path (F50/F68/F70/F71) all
run through these queues. Whatever subset is approved must re-pass the F50
rocket-churn and F55 unreachable scenarios, plus a new probe set (moonlight
claim/execute, migration hysteresis) in the A/B harness before it ships.
