# The drone task-priority system — full breakdown

Research 2026-07-31, requested by the owner before any priority work is
attempted: *"I know the game has a player toggled priority system and a hidden
priority system… If there is a life risk drones rapidly repair it… A crack in
the dome, a leak in an O2 pipe, all super fast."*

Every claim below was read from
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` at build
`1.0.7.396349`. Reference material for the drone rebuild — **not a spec, and
nothing here authorises a change.**

---

## Headline — the observation is correct, but there is NO hidden band

The fast-repair behaviour is real and you identified both instances of it. But
it is not a separate hidden priority tier. **It is two classes auto-assigning
themselves the top of the player's own scale.**

The entire priority system is **five integer bands, `-1` to `3`**, and the
player's scrollbar already reaches the top one.

| Band | Set by | What lives there |
|---|---|---|
| **3** | player (max) **and auto** for broken pipes/cables + dome fractures | "urgent" |
| **2** | player — **the default** | everything else, **including all building maintenance** |
| **1** | player (min) | deprioritised |
| **0** | engine only | storage-depot requests |
| **-1** | engine floor (`Clamp` argument) | reserved; nothing observed assigning it |

Higher is served first — the game says so itself in a code comment: *"we use our
priority to force our consumer element to be serviced first"*
(`SupplyGridBreakable.lua:52-53`).

---

## §1 The bands, and where they are defined

`CommonLua/TaskRequest.lua:15-18` (module locals, overridable from the Consts
editor group `const.TaskRequest`):

```lua
local MinBuildingPriority        = -1
local DefBuildingPriority        =  2
local MaxBuildingPriority        =  3
```

**The game does not override them** — a sweep for a `const.TaskRequest` settings
group found no hits, so the CommonLua defaults stand. Separately
`Lua/_GameConst.lua:56` sets `const.MaxBuildingPriority = 3`, with the shipped
comment `-- 1 normal, 2 - high, 3 - urgent`.

⚠️ **That comment is misleading and should not be trusted as the band map.** The
actual player default is **2**, not 1 — see §2.

**The queues exist only for those five values.**
`TaskRequestHub:InitRequestQueues` (`TaskRequest.lua:245-256`):

```lua
for priority = MinBuildingPriority, MaxBuildingPriority do
    self.priority_queue[priority] = {}
    self.supply_queues[priority]  = {}
    self.demand_queues[priority]  = {}
end
```

**A priority outside `-1..3` has no queue at all.** `_InternalAddRequest`
(`:310-320`) indexes `supply_queues[priority]` / `demand_queues[priority]`
directly — an out-of-range value yields nil and the subsequent index errors.
Because `error()` in this engine **reports and continues** (ENGINE_FACTS), the
practical outcome is a log line and a **silently lost request**, not a crash.
`SupplyGridBreakable.lua:51-52` carries the shipped warning in its own comment:
*"asserts will happen if we go above or below known priorities in DroneHub.lua
code."*

> **Hard constraint for any future work: every priority must be an integer in
> `[-1, 3]`. There is no room to invent a band above urgent.**

---

## §2 The player-facing control

`Lua/Buildings/Building.lua:199` — the property behind the infopanel arrows:

```lua
{ name = T(172, "Priority"), id = "priority", category = "General",
  editor = "number", default = 2, ui = "scrollbar",
  min = 1, max = const.MaxBuildingPriority }
```

So the player gets **three positions — 1, 2, 3 — defaulting to 2**, and band 3
("urgent") is **already reachable by hand**. Bands 0 and -1 are engine-only and
not exposed.

---

## §3 The one function that decides everything

`TaskRequester:GetPriorityForRequest(req)` — `CommonLua/TaskRequest.lua:181-187`:

```lua
function TaskRequester:GetPriorityForRequest(req)
    if req:IsAnyFlagSet(rfStorageDepot) then
        return 0
    else
        return self.priority
    end
end
```

That is the whole base policy: **storage-depot requests sink to 0; everything
else inherits the building's own player-set priority.**

Note the shape — a request-class special case, hardcoded, one branch. **That is
the precedent** any future request-class rule would follow, not a new mechanism.

**Where it is called:** `TaskRequestHub:_InternalAddRequest`
(`TaskRequest.lua:310-312`) and `DroneControl:AddBuilding`
(`DroneControl.lua:693`) — both at the moment a request **enters a hub's
queue**.

> ⚠️ **Priority is baked at queue-insert time.** `_InternalAddRequest` calls
> `GetPriorityForRequest`, then `request:SetPriority(priority)`, then files the
> request into `queue[priority]`. Calling `SetPriority` later does **not** move
> it between queues. Changing a live building's effective priority requires a
> **re-registration** — remove and re-add, which is what
> `DroneControl:ReconnectTaskRequesters` (`DroneControl.lua:779-785`) does and
> which vanilla already performs routinely (hub toggle, extender flap, radius
> change, nearby placement).

---

## §4 The "hidden" system — three overrides, and that is all of them

A whole-tree sweep for `GetPriorityForRequest` found exactly four definitions
(one base + three overrides) and two aliases.

### 4a. Broken pipes and cables → **3** — *your O2 leak*

`Lua/SupplyGridBreakable.lua:48-56`:

```lua
function BreakableSupplyGridElement:GetPriorityForRequest(req)
    if req == self.repair_resource_request or req == self.repair_work_request then
        return 3 --Drones automatically repair cables with the priority of cable construction.
    else
        return Clamp(TaskRequester.GetPriorityForRequest(self, req), -1, const.MaxBuildingPriority)
    end
end
```

Both legs — the **resource haul** and the **repair work** — jump to 3.

### 4b. Dome fractures → **3** — *your crack in the dome*

`Lua/Passage.lua:485-491`: identical shape, for `fracture_demand_request` and
`fracture_work_request`.

### 4c. Track elements → **no bump**

`Lua/Buildings/TrackElement.lua:172-174` overrides the method but only to apply
the `Clamp`; it grants no urgency. Tracks are **not** in the fast-repair club.

### 4d. Aliases

`Lua/Buildings/ConstructionSite.lua:2082` and `:2199` set
`GetPriorityForRequest = RequiresMaintenance.GetPriorityForRequest` — an
inherited reference, not a distinct policy.

---

## §5 THE GAP — ordinary building maintenance has no override at all

`Lua/RequiresMaintenance.lua` **defines no `GetPriorityForRequest`.** Its two
requests therefore fall through to the base function and inherit `self.priority`
— the player's arrows, default **2**:

- `maintenance_resource_request` — the **demand/haul** leg (`StartDemandPhase`);
- `maintenance_work_request` — the **repair** leg (`StartWorkPhase`).

**Consequence:** a malfunctioned Oxygen Factory's parts delivery is filed at
priority 2, competing on exactly equal footing with routine resource shuffling
from every other default-priority building on the map. A cracked pipe beside it
is at 3 and jumps the whole queue.

**This is the mechanism behind the measured 3h03m hauling leg** (PT-52 B2 — see
the D06 entry): the delivery is not slow because hauling is slow, it is slow
because **nothing marks it as more important than routine traffic.**

### The developers' actual rule, read off their own code

The pattern in §4 is **not** "repairs are urgent". Tracks are repairs and get
nothing. The rule they implemented is narrower and more specific:

> **Life-support-critical repairs are urgent.**

They applied it to the **grid** (pipes and cables carrying air and water) and to
the **dome shell** (fractures venting atmosphere) — and never extended it to the
**buildings that produce** the air and water. A broken Oxygen Factory is exactly
as life-threatening as the pipe leading out of it, and sits a full band lower.

**That framing matters for policy.** Extending the rule to life-critical
producers is *completing a policy the developers started*, not inventing one —
a materially different argument from "we think repairs should be faster", and
the difference is the one FIX_POLICY §4 cares about.

---

## §6 Landmines for anyone implementing against this

1. **The `-1..3` ceiling.** No new band. Any bump is *into* an existing band,
   and the only headroom above the default is **one step: 2 → 3**.
2. **Band 3 is not exclusive.** Putting maintenance at 3 makes it
   indistinguishable from a dome breach *and* from any building the player set
   to max by hand. A flat bump therefore flattens two distinctions at once.
3. **Priority is baked at insert.** A dynamic "urgent while broken" needs a
   re-registration to take effect (§3), not a `SetPriority` call.
4. **Instance-level method flattening.** `RequiresMaintenance.lua:94` does
   `self.GetPriorityForRequest = g_Classes[self.class].GetPriorityForRequest or
   TaskRequester.GetPriorityForRequest` — but **only in the `else` branch**, for
   buildings that do *not* accumulate maintenance. Maintenance buildings keep
   normal method lookup, so a class-level override reaches them. Non-maintenance
   buildings that took that branch hold a direct function reference and would
   **not** see a later class patch. Not a hazard for maintenance work; record it
   before touching anything else through this method.
5. **Overriding the player.** `self.priority` is the arrows the player set. Any
   automatic bump overrides an explicit player choice. Deciding whether a bump
   is *absolute* (always 3) or *relative* (preserves the player's ordering among
   affected buildings) is a design decision with real UX consequences, not an
   implementation detail.
6. **Starvation, mirrored.** Whatever is promoted, something else is demoted.
   Promoting maintenance colony-wide can starve food delivery and construction
   in a colony with many simultaneous breakdowns — the same failure D06's
   claim gate already carries a strike/TTL valve for, one layer up.
7. **The matcher is C-side.** The per-priority queue *structures* are Lua and
   readable; the matching pass that consumes them is not. Ordering claims beyond
   "higher is served first" (evidenced by the shipped comment at
   `SupplyGridBreakable.lua:52`) should be **measured, not asserted.**

---

## §7 What this does and does not settle

**Settled, from source:** the band range and its hard ceiling; the player's
control and its default; the single function that assigns priority; every
override that exists; that building maintenance has none; that priority is baked
at insert; that the developers' rule is life-support-criticality rather than
repair-ness.

**NOT settled, and not to be assumed:** the C matcher's exact ordering within a
band; whether a bump to 3 measurably shortens the 3h03m haul leg in play (that
is a measurement, and PT-52's harness must be re-pointed first — the current
metric measures *which hub delivered*, not which won a claim); and how much
routine traffic a colony-wide promotion would displace.
