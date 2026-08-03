---
kind: "notes"
source: "docs/BUGS.md, split 2026-08-03 by tools/split_bugs.py"
orphan_rows:
  - {"row": 112, "id": "C02", "title": "Cave-ins reported on asteroids — no Src code path found", "status": "cand", "status_source": "row-evidence", "priority": "?", "evidence": "cand", "row_status": "runtime-check", "note": "NO ENTRY TEXT (verified prompt 1, 2026-08-03)"}
---
# BUGS.md residue — everything that belonged to no entry

Split out of `docs/BUGS.md` on 2026-08-03 by `tools/split_bugs.py`.

Every line below the `---` is **byte-preserved** from that file, in source
order: the intro, the five `##` section dividers whose entries moved out
(P1, P2, P3, Phase 2, Candidates — they stack up here because nothing is
left between them), and the “Not yet swept” backlog.

The index table it also held is *not* here — `INDEX.md` replaces it, and
every cell of all 151 rows is preserved verbatim in entry front matter.

**C02 has an index row and no entry text anywhere in BUGS.md** (verified
twice, 2026-08-03): it keeps an INDEX row pointing at nothing rather than
getting an invented entry. Its row is in this file's front matter.

---

# Bug Tracker — Surviving Mars: Relaunched Community Fix Pack

Canonical record of every defect found in the game's shipped Lua source
(`<game>\ModTools\Src`), its evidence, and its fix status. **Update this file in
the same change that adds or edits a fix.** All line numbers refer to the
shipped source tree; the game executes `Packs\Lua.fpk`, **proven byte-identical
to Src for all gameplay Lua** (2,250/2,256 files, build 1.0.7.396349 — the
2026-07-29 extraction diff; the 5 divergences are engine/tooling only). Each
fix still self-checks its target at apply time — that guards *future* game
updates — and the extraction diff is re-run after every game update
(see `WORKFLOW.md`).

Statuses: `todo` → `fixed` (code written) → `tested` (verified in-game) | `wontfix` | `blocked`.


Severity: P1 = gameplay-breaking/major loss, P2 = wrong numbers or notable misbehavior, P3 = cosmetic/latent/mod-facing.

---

## P1 — gameplay-breaking

## P2 — wrong numbers / notable misbehavior

## P3 — cosmetic / latent / mod-facing

## Phase 2 findings — details (2026-07-24)

## Candidates under investigation

## Not yet swept (follow-up targets)

- `Lua\Buildings\DroneControl.lua`, `ShuttleHub.lua` — drone/shuttle task assignment.
  **(DroneControl half SWEPT — static source leg 2026-07-27 late; full verdict + trace
  + instrumentation plan appended at the end of this bullet. `ShuttleHub.lua` remains
  unswept.)**
  Prime suspect for live reports: "drones ignore rocket cargo at high priority",
  "RC transports don't auto-offload rockets", "late-game drones stop maintaining
  inside open domes / cluster stuck outside" (review-sourced).
  **FIRST-HAND EVIDENCE (user, 2026-07-27 late, screenshot on file — raise this
  to the top of the sweep):** with a large-range hub plus many drones and
  OVERLAPPING hub ranges, (a) **task assignment ignores locality across hubs** —
  a cluster of idle drones parked nearest a malfunctioning building (wrench
  icon up) and a Polymer storage did nothing while a hub near the SECOND dome,
  much farther away, serviced everything; work backed up and buildings sat
  disabled for short stretches; (b) **performance tanks** as hub range/drone
  count grows, worse with multiple hubs in range of each other — the user saw
  the same pattern in the ORIGINAL game, so the mechanism likely survived into
  Relaunched. Investigation angles when swept: how tasks are queued per-hub vs
  globally (does a request bind to the hub that noticed it rather than the
  nearest?), whether overlapping hubs share/steal work, whether idle drones
  ever scan for work themselves, and what in the per-tick request matching is
  O(range × drones). Distinct from F55 (unreachable-forever cache) — these
  drones CAN reach the work; they are never assigned it.
  **Live console reads (same sitting):** the FOUR closest drones to the
  serviced-too-slowly area each read `command = "Idle"` — genuinely idle in
  the assignment layer, not wedged mid-command and not F55-cached; and a
  PolymerPlant was caught at `performance = 0` with `auto_performance = 50`
  (the transient disable the user reported), its maintenance/repair requests
  showing `target:0` at read time (the far fleet does service things —
  slowly). Ownership answered: an idle drone's `command_center` read
  **`DroneHub`, handle 2608** — a regular hub (near the idle cluster), so the
  drones are correctly parented, and the user verified **no RC commander was
  nearby broadcasting a zone** (rover niche ruled out). Remaining crux for the
  sweep, only observable AT a starvation moment: which hub's queue holds a
  request while hub-2608's drones idle — i.e. whether requests bind to the
  noticing/registering hub's fleet with no cross-hub handoff.
  **User hypothesis (prior-game experience, same sitting): the REPEATER is the
  trigger** — in the original game the misassignment/performance pattern
  became prevalent once Drone Hub Extenders entered the colony, and this
  colony DOES run them (a DroneHubExtender maintenance request appeared in the
  same dump batch). Plausible mechanism to check in the sweep: an extender
  stretches a distant hub's effective service area over ground a nearer hub
  already covers, and whatever request→hub matching runs is
  extender-transparent (distance/priority measured hub-to-target, or
  first-registered-wins) so the extended far hub captures work the near fleet
  should take. Sweep pointers: extender machinery is in `DroneControl.lua`
  itself + `Drone.lua` (both already in this bullet) and
  `BuildingTemplate\DroneHubExtender.generated.lua` /
  `XDef\customDroneHubExtender.generated.lua`. Repro recipe for the sweep:
  hub A + hub B far apart, extender bridging B's range into A's area, break
  something in A's yard, watch which fleet answers.

  **INVESTIGATION VERDICT (game-free source leg, 2026-07-27 late).** The assignment
  architecture is **working-as-coded but has NO cross-hub locality anywhere**; the
  extender-transparency hypothesis is **CONFIRMED**; one adjacent provable defect was
  filed (**F77**, extender working-flap churn); the exact starvation trigger needs one
  attended console sitting to discriminate two proven-possible mechanisms (reads below).
  Trace, against the six kickoff questions:

  1. **Pull model, own-hub-only, engine-matched.** An idle drone polls ONLY its own
     hub: `Drone:Idle` (`Drone.lua:564-641`) calls `command_center:FindTask(self)`
     (`:621`) — the sole `FindTask` call site in the entire Src tree (grep-verified).
     `TaskRequestHub:FindTask` (`_TaskRequest.lua:72-83`) hands the hub's OWN
     priority/supply/demand queues to the C-side `Request_FindTask`; the match
     order/distance policy inside it is engine-internal and NOT visible in Src (no doc
     either — recorded as an engine-side unknown). The only distance knob visible from
     Lua is per-request `supply_dist_modifier` (`_TaskRequest.lua:96`) — distance is
     weighed when pairing supplies WITHIN a hub, but nothing weighs locality across
     fleets. Queues are per-hub Lua tables of shared C request objects, appended in
     insertion order (`CommonLua\TaskRequest.lua:242-256` queue layout;
     `DroneControl.lua:685-718` `AddBuilding`). Poll cadence ≈3s per idle drone
     (Sleeps inside Idle), gated on `hub.working` (`Drone.lua:612`) and on a 1s
     per-HUB empty-queue throttle `no_requests_time` (`:620,:631` — stamped only by a
     drone with zero unreachable-cache entries; reset only by `InterruptDrones`,
     `_TaskRequest.lua:301`).
  2. **Overlap = the same C request object sits in EVERY covering hub's queues; claim
     is first-poller-wins and held through travel; no handoff, no stealing, no
     rebalance exists.** A building registers with every hub whose radius covers it
     (`TaskRequester:AddCommandCenter`, `CommonLua\TaskRequest.lua:147-160`; both
     connect directions), and every new request posts into every registered center
     (`AddRequest`, `:123-137`). The claim happens when the winning drone's command
     starts, not at match time: `Drone:Work` calls `RequestAssignUnit` BEFORE the
     approach (`Drone.lua:898-924` — claim at `:901`, fulfil only on arrival `:920`),
     so the slot is locked for the entire trip. Maintenance repair requests are
     created with **max_units = 1** (`RequiresMaintenance.lua:82` —
     `AddWorkRequest("repair", 0, 0, 1)`): ONE claiming drone, however far, locks out
     every other fleet. The only cross-hub drone code in the game is refab gathering
     (`DroneHub.lua:53-74`) and orphan adoption — nothing load- or distance-based.
  3. **Extender transparency CONFIRMED in both connect directions.** Building-side:
     `FindDroneNodes` (`_TaskRequest.lua:251-257`) returns any `DroneNode` covering
     the building; an extender's `GetCommandCenter()` recurses to its uplink HUB
     (`DroneHubExtender.lua:156-160`), so the building registers the far hub ITSELF.
     Hub-side: `FindTaskRequesters` (`DroneControl.lua:315-325`) recurses through
     working linked extenders and connects finds to the hub. Extender-mediated
     coverage is structurally identical to native coverage in every queue — the
     extender leaves no trace on the request. What extenders do NOT extend: drone
     movement. `Drone:SetCommandCenter` restricts each drone to
     `const.DroneRestrictRadius` = 100 hexes-worth of world distance AROUND THE HUB
     POSITION (`Drone.lua:227-230`, `_GameConst.lua:71`). Post-SignalBoosters (hub
     +15 → 50, extender +15 → 50; `TechPreset.lua:3455-3482`) one max-stretched
     extender reaches exactly that boundary; a chain of two EXCEEDS it — buildings
     can be REGISTERED with a hub whose drones can never legally reach them
     (suspected F55-feeder: approach fails → unreachable-forever cache; `RestrictArea`
     enforcement is engine-side, unverifiable statically — flagged for the live
     sitting).
  4. **Idle drones never look for work themselves.** The Idle body is the only work
     search a drone performs, own hub only (plus special cases: own-hub repair,
     broken-drone repair, emergency power — `Drone.lua:593-618`). If its hub's queues
     don't hold the request, or the request is claim-locked, a drone parked ON TOP of
     the work idles forever, by construction.
  5. **Hot loops (the performance half).** (i) Every idle drone × every ≈3s × a
     C-side scan over its hub's full queue set; queue size grows with range² ×
     building density AND with overlap multiplicity — every shared building's
     requests appear in every covering hub's queues, so k-fold overlap ≈ k× the
     colony-wide scan work. The 1s empty-queue throttle cannot engage while any
     polling drone holds an unreachable-cache entry (`Drone.lua:630`) — i.e. exactly
     in cluttered late-game colonies. (ii) Reconnect storms: `SetWorkRadius`
     (`DroneControl.lua:760-777`), every extender working-flap (→ **F77**), and
     `OnMsg.DepositsSpawned` reconnecting EVERY hub in the city at once
     (`DroneHub.lua:188-199`). Each reconnect = per-building drone-kick scans
     (O(B×D), `OnRemoveBuilding` `:720-729`) + linear `remove_entry` over 5-priority
     queues + a full `MapGet` radius rescan. That is the reported range × drones ×
     requests degradation, and overlap worsens every term.
  6. **Reconciliation.** The observed picture (near fleet Idle, far fleet slowly
     servicing, transient `performance = 0` disables, requests reading `target:0`)
     is reproduced by the traced machinery under either of two mechanisms — the
     banked console evidence cannot yet discriminate:
     **(a) registration gap** — the starving buildings sit OUTSIDE hub 2608's
     35-50-hex circle while INSIDE the far hub's extender-stretched coverage. Then
     2608's queues never hold the requests and its drones idle legitimately (drones
     parked near the buildings prove nothing about the hub's circle — `GoHome` parks
     them relative to the HUB, `Drone.lua:636-638,643-674`). Everything runs
     as-coded; the failure is pure design — the extender grants the FAR fleet ground
     the NEAR fleet doesn't own.
     **(b) claim lockout** — the requests ARE in both hubs' queues; far drones claim
     first (max_units=1 + claim-held-through-travel) and the near fleet re-loses the
     race on every work chunk. The live `target:0` read is consistent with (b) at the
     read instant, but also with (a)+far-claim.
     **F77's flap churn additionally reproduces both observed halves on its own**
     whenever an extender flaps — and this colony runs extenders with a pending
     extender maintenance request in the same dump batch.

  **Live instrumentation plan (next attended sitting; F12/PT-38 timestamped-wrapper
  pattern; every name verified against Src and console-sandbox-safe — `HexAxialDistance`,
  `HandleToObject`, `ConsolePrint`, `MainCity`, `GameTime`, `guim` all non-blacklisted;
  `Drone.lua` holds no file-local alias of `RequestAssignUnit`, so a console global
  wrapper IS seen by drone code):**
  * **R1 — registration + geometry** (select the starving building first). Answers
    (a) instantly — is 2608 listed, and is `d ≤ radius`?
    `*r local b=SelectedObj local s={} for _,cc in ipairs(b.command_centers or empty_table) do s[#s+1]=cc.class..":"..cc.handle.." d="..HexAxialDistance(cc,b).."/"..cc.work_radius.." w="..tostring(cc.working) end ConsolePrint("[SMR reg] "..b.class..":"..b.handle.." -> "..table.concat(s," | "))`
  * **R2 — who holds the repair claim** (building still selected):
    `*r local b=SelectedObj local r=b.maintenance_work_request ConsolePrint("[SMR req] target="..r:GetTargetAmount().." actual="..r:GetActualAmount().." can="..tostring(r:CanAssignUnit())) for _,d in ipairs(b:GetMap().City.labels.Drone) do if d.w_request==r or d.d_request==r or d.s_request==r then ConsolePrint("[SMR holder] "..d.handle.." cmd="..tostring(d.command).." hub="..(IsValid(d.command_center) and d.command_center.handle or 0).." dist="..(d:GetDist2D(b)/guim).."m") end end`
  * **R3 — is the request in hub 2608's queues** (building selected; work requests
    are rfPostInQueue via the Mars `AddWorkRequest`, `_TaskRequest.lua:118-121`, so
    the priority_queue is the right place to look):
    `*r local h=HandleToObject[2608] local b=SelectedObj local n=0 for p=-1,3 do for i,r in ipairs(h.priority_queue[p]) do if r:GetSource()==b then n=n+1 ConsolePrint("[SMR q] prio="..p.." idx="..i) end end end ConsolePrint("[SMR q] hits="..n)`
  * **R4 — hub state**:
    `*r local h=HandleToObject[2608] ConsolePrint("[SMR hub] w="..tostring(h.working).." idle="..h:GetIdleDronesCount().."/"..#h.drones.." lap="..h:CalcLapTime().." nrt="..(GameTime()-h.no_requests_time))`
  * **R5 — extender chain map** (uplink chains + working states):
    `*r for _,e in ipairs(MainCity.labels.DroneHubExtender or empty_table) do local c={e.class..":"..e.handle} local cur=e.uplink while cur do c[#c+1]=cur.class..":"..cur.handle cur=cur:HasMember("uplink") and cur.uplink or nil end ConsolePrint("[SMR ext] "..table.concat(c," -> ").." w="..tostring(e.working)) end`
  * **R6 — live claim tap** (the timestamped wrapper; repair-only filter to bound
    spam; arm once per session, cleared by reload):
    `*r local orig=RequestAssignUnit RequestAssignUnit=function(req,unit,amount) local ok=orig(req,unit,amount) if ok and IsValid(unit) and unit.class=="Drone" and tostring(req:GetResource())=="repair" then ConsolePrint("[SMR "..GameTime().."] claim "..unit.handle.." hub="..(IsValid(unit.command_center) and unit.command_center.handle or 0).." src="..tostring(req:GetSource() and req:GetSource().handle)) end return ok end ConsolePrint("[SMR] claim tap armed")`
  * **R7 — controlled repro** (the banked recipe): hub A + hub B far apart, extender
    bridging B into A's yard. Arm R6; `Platform.cheats = true` then
    `SelectedObj:CheatMalfunction()` on a building in A's yard (verified command
    table); watch which hub's drone claims, then re-run R1-R4 at the claim moment.
    A-covered building claimed by a B drone while A idles = (b) proven; building
    missing from A's `command_centers` = (a) proven.

  **Fix directions (NOT built this leg — user decision; FIX_POLICY §1 ranking; the
  locality items are assignment-POLICY changes — D-item territory — while F77 is a
  plain repair):**
  * **If (a) — registration gap:** the least-dishonest mod-side lever is a cross-hub
    idle-pull: PRE-wrap `Drone:Idle` (must be pre — command methods kill post-wrappers,
    F73/STATUS fact) so that after the own-hub `FindTask` misses, the drone polls
    OTHER working hubs whose `work_radius` covers the DRONE's position. Requests are
    hub-agnostic C objects, so cross-hub execution is mechanically clean, and
    `RestrictArea` keeps the drone local anyway. Risks: lap-time/heavy-load
    accounting attributes foreign work to the wrong hub; battery/GoHome interplay;
    claim races (already atomic via `AssignUnit`).
  * **If (b) — claim lockout:** a near-idle-yield — chained pre-claim veto in
    `Drone:Work`/`Drone:PickUp`: skip claiming (the shipped miss path: Sleep +
    return) when the request's source building has a CLOSER working center with idle
    drones and the building inside that center's radius; yield-once-per-request memo
    (TTL) so a request whose near fleet can't actually serve is never starved. The
    match ORDER itself cannot be touched — `Request_FindTask` is C; only its Lua
    callers are patchable — so a veto+retry is the least-invasive lever that exists.
  * **F77 (independent of (a)/(b)):** debounce wrapper — see the F77 entry.
  * **Shared-machinery risk, stated per the kickoff:** this is the deepest shared
    machinery in the game — every `DroneControl` descendant (hubs, RCRovers, the
    rocket cargo path of F50/F68/F70/F71) runs through these queues. Any claim-path
    change must re-pass the F50 rocket-churn and F55 unreachable scenarios in
    playtest before shipping.
  * **Follow-up (2026-07-28, user-commissioned): full overhaul-toggle feasibility
    study in `docs/reports/DRONE_OVERHAUL_OPTIONS.md`** — options A-G (repair moonlighting,
    full moonlighting, migration balancer, claim veto, true handoff, Lua-matcher
    rewrite [rejected], telemetry/F77/throttle supporting acts) ranked by
    feasibility/risk/reward with verified patch points and a recommended build
    order. Supersedes the two fix-direction sketches above as the design reference;
    still a USER DECISION.
- Colonist auto-assignment: workplaces (`UpdateWorkplaces` family — "unemployed
  every sol"), residences ("homeless despite free housing", "seniors don't move"),
  dome-to-dome walking/passage checks (`AreDomesConnectedWithPassage` — suffocation
  on long walks; stuck on Universal Depots).
- `Landscape\` (terraforming) — "lakes causing crashes", artificial lake entombing
  rovers + notification retrigger loop.
- Asteroid cave-in trigger — NOT the underground marsquake repeat (asteroids are
  `Environment == "Asteroid"`, gate requires `"Underground"`); find actual source.
- Martian Express track editing (single-hex delete removes whole track) — LukeH
  prior art.
- Large Wind Turbine tech modifiers not applying (Frictionless Composites) —
  targeted label/template check, do early.
- Inspiring Architecture freeze (also in original); `RandomMap\`; `Construction\`
  beyond F-items; UI XTemplate layout (misaligned buttons — cosmetic).
- Remaster player-report list (see `docs/archive/RESEARCH.md`) — several reports not yet mapped
  to code: seniors not auto-moving to retirement homes, mysteries not starting
  (Inner Light), no cold waves/dust storms triggering, asteroid lander launching empty,
  auto asteroid miners missing from build menu, Martian Express track salvage issues,
  universities training geologists after Extractor AI, Fast Rockets rule stopping,
  Single Party tension, can't rebuild on old building spots.
