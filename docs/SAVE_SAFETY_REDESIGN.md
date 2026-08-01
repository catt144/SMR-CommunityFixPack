# Save-safety redesign — the F86 remedy

**Status: DECIDED and the BUILD IS AUTHORISED (owner, 2026-07-31). The layer
ordering is ADOPTED and lives in `FIX_POLICY.md` §3a as a hard rule. The sweep
has RUN and is discharged (§5). The authorised build is §6 — Tiers 1 and 2,
with LAYER 1 EXPLICITLY NOT TO BE BUILT. F02's hold is LIFTED. D10 and D12 stay
held until these repairs land.** Written 2026-07-31 immediately after the PT-20
leg that measured the defect; the four decisions were taken the same day and are
recorded in §4. The defect itself is `BUGS.md` **F86** (P1, blocks release);
this file is the *how*.

> ✅ **THE SWEEP IS COMPLETE — §5, BOTH HALVES. Decision 2 is discharged and
> nothing further is owed on it.**
> - **Exposed set (§5.3):** one module was missing from the list and one never
>   belonged on it; **five of the twelve have a layer-3 or layer-2 route out**, so
>   only four own-thread modules plus `BombardmentSpread` are candidates for the
>   dangerous layer 1.
> - **Non-exposed set (§5.4, all 22):** **6 convert cleanly to a chained
>   wrapper**, 4 have a route worth designing, 9 are correctly full replacements,
>   3 are already optimal. None of it is urgent; none of it blocks F86.
>
> ⏸️ **BUILD PAUSED 2026-07-31 — nothing was written.** The owner is having this
> session's findings independently compared first:
> **`docs/F86_SESSION_FINDINGS.md`** (confidence labels per finding, the two
> discarded analysis methods, and the mistakes made). ⚠️ **It records a shipped
> defect not covered anywhere in this file** — `Fix_MeteorFrequency` restarts the
> meteor timer on **every** load, so frequent loading suppresses meteors
> indefinitely (§1.4 there). That also puts §6's retroactive-heal reasoning in
> question. **Read it before building.**
>
> ⭐ **THE BUILD IS AUTHORISED — §6. Scope: Tiers 1 and 2; LAYER 1 IS NOT TO
> BE BUILT.** F02's hold is **lifted** and it leads the build. `Opt_DroneOverhaul`
> is in scope but blocked on the drone carve-out. D10/D12 stay held until these
> repairs land.

---

## 1. The rule this is all built on

PT-20 measured pack code being serialised into a savegame and running after the
mod's removal. The mechanism (full evidence on F86, mechanics in
`ENGINE_FACTS.md`) reduces to one test:

> **Can this function be executing, or blocked, below a `Sleep` / `WaitMsg` /
> `WaitWakeup` on a GAME-TIME thread at the moment the save is written?**

Two properties make this tractable rather than terrifying:

- **A save captures only *blocked* threads.** Synchronous mod code — data
  patches, getters, `Can…` predicates, UI handlers, `OnMsg` bodies that do not
  yield — can never be captured *through the thread-stack route*. That is ~62
  of 74 modules, safe from that route by construction.
  ⚠️ **CORRECTED 2026-07-31 (adjudication): capture is value-reachability, not
  frame position alone** — a function value held in a live local of a captured
  engine frame, or stored in persisted state, also enters the save.
  `Fix_CaveInsNoDisasters` is capturable today via the engine's periodic-repeat
  `info` local (inert — layer-2 shape; no build needed), which makes the
  exposed-set count **at least 13** and proves the method grep blind to
  slot/global/preset assignments. `docs/F86_ADJUDICATION.md` §3.1/§5.1.
- **Real-time threads are not persisted at all.** `00_Core`'s update-report
  thread is a `CreateRealTimeThread` and is already fine.

Everything below concerns the remaining 12.

---

## 2. Three layers, in order of preference

### Layer 3 — patch a synchronous input, keep vanilla's body  ⭐ best

Where a defect can be repaired by changing what a shipped function *reads*
rather than replacing what it *does*, the pack has no body in the save at all
and the whole problem disappears for that module.

**Worked example, F02 — and it removes the pack's worst leak site entirely.**
Vanilla's meteor interval is `Min(spawn_time, warning_time)`
(`Meteors.lua:291-292`). `GetDisasterWarningTime` (`MapSettings.lua:94`) is a
plain synchronous global that can never sit on a blocked stack. Wrap it so a
meteor descriptor returns `Max(orig, spawntime + spawntime_random)`; `Min` then
equals `spawn_time`, and **vanilla's own body produces the designed 35–115 h
schedule**. The tower-count dependence disappears as a consequence rather than
as a second fix (see the F02 root-cause note).

`Fix_MeteorFrequency`'s replacement body — the site that killed a colony's
meteors in PT-20 — is then deleted outright.

> ⚠️ **SCOPE CHECK CORRECTED 2026-07-31 — the original one here was wrong, and
> shipping against it would have caused a balance change.** It said the wrapper
> "must key on the meteor descriptor and defer to the original otherwise."
> **Keying on the descriptor does not separate the call sites.** Every caller of
> `GetDisasterWarningTime`, enumerated:
>
> | site | passes | affected |
> |---|---|---|
> | `Meteors.lua:279` — the `Meteors` thread | `GetMeteorsDescr()` | ✅ the target |
> | **`Meteors.lua:326` — the `MeteorStorm` thread** | **`GetMeteorsDescr()`** | ⚠️ **the same descriptor** |
> | `ColdWave.lua:231`, `:378`; `DustStorm.lua:467` | their own descriptors | no |
> | `SensorTower.lua:31`; `TerraformingDisasters.lua:285` | **no argument at all** | no |
>
> Both meteor threads pass the identical descriptor. Inflating `warning_time` to
> `spawntime + spawntime_random` (up to 115 h) would make the **meteor-storm
> warning notification fire ~5 sols early instead of 6 hours**, and would make
> Sensor Towers irrelevant to storm warning — a visible gameplay change, barred
> by FIX_POLICY §4, arriving as a side effect of a save-safety repair.
>
> **Key on the calling thread instead.** `GlobalGameTimeThread` parks each
> thread in a global of its own name (the current watchdog already relies on
> this: `rawget(_G, "Meteors")`), and `CurrentThread()` exists and is **not** in
> `ModEnvBlacklist`. So inflate only when
> `CurrentThread() == rawget(_G, "Meteors")` and defer everywhere else. Still
> fully synchronous, so it never enters a save — this stays layer 3.
>
> **Second correction, minor but it belongs in the eventual header:** "vanilla's
> own body produces the designed 35–115 h schedule" is fractionally off. Once
> `warning_time > spawn_time`, vanilla's dead `if`
> (`0 > spawn_time - warning_time`) stops being dead and adds `Sleep(5000)` —
> **10 game minutes** per cycle, since one game hour is 30,000 ms. Negligible
> against 35–115 h, but it is not exactly `spawn_time`.

**Which other modules can take this shape — ✅ SWEPT, §5.** Beyond F02, the
sweep found four more exposed modules with a layer-3/2 route (§5.3) and six
non-exposed full replacements that convert cleanly to a chained wrapper (§5.4
group A). **F02's hold was lifted 2026-07-31 and it leads the build (§6).**

### Layer 2 — no mod code after a call that can block

**Corrected 2026-07-31, and the correction matters.** This rule was first framed
as *"tail-call the original so our frame leaves the stack"*. That justification
is unobservable in this engine — the sandbox denies introspection, and a probe
cannot distinguish a vanished tail-call frame from a surviving one, because a
tail call has nothing after it to run either way. The sound version needs no
engine guarantee:

> **Do all work BEFORE the call, then `return orig(...)`. Never place mod code
> after a call that can block.** Then whether or not the frame is serialised,
> there is nothing left to execute after removal.

This separates the two wrappers we have exactly:

| site | shape | verdict |
|---|---|---|
| `Opt_DroneOverhaul:188-190` | `orig_idle(self)` as a statement, then work | **leaked, measured** — 98 errors/session |
| `Fix_ShelterReflex:73` | `return orig_idle(self, ...)`, nothing after | harmless either way |

Wrappers that genuinely need post-work — D06's moonlighting is the real case —
must move that work out of the command body into a message or periodic hook.

*Residual, accepted:* a serialised-but-inert function may sit in a save as dead
weight. It executes nothing and is invisible to any read available to us.

### Layer 1 — `SaveGameStart` tear-down / `SaveGameDone` rebuild

> ⛔ **NOT TO BE BUILT — owner decision 2026-07-31 (§6.3).** The four modules it
> would serve own their own threads, so nothing vanilla is lost when they die
> after uninstall — the cost is one log line each. The owner accepted that
> residual rather than build this layer. **Do not propose it again without new
> evidence that Tier 3 causes real harm.** The design below is retained only as
> a record of what was considered.

For what layers 2 and 3 cannot reach: the pack's own game-time threads.

**Newly possible.** `OnMsg.SaveGameStart` and `SaveGameDone` reach mod code —
measured, with `OnMsg.LoadGame` as a positive control. Only `PersistSave`,
`PersistLoad` and `PersistGatherPermanents` are blacklisted
(`Mod.lua:1430-1440`), and `DoSaveGame` fires `SaveGameStart` **before** the
write (`Savegame.lua:1043`). **This overturns the previously recorded fact that
mods have no save hook.**

Shape: on `SaveGameStart`, delete our threads and restore vanilla bodies to
`GlobalGameTimeThreadFuncs` / the globals we replaced; on `SaveGameDone` and
`LoadGame`, reinstall.

> ⚠️ **THE TRAP — read before designing any of this.** Autosaves are the same
> code path: `SaveAutosaveGame` (`Savegame.lua:1450-1453`) sets
> `params.autosave = true` and calls `DoSaveGame`. They fire roughly once a sol.
> **A tear-down that RESTARTS a loop would reset a 35–115 h meteor timer before
> it could ever expire** — recreating PT-01's permanent-silence signature out of
> our own code, and it would look exactly like the bug we are trying to fix.
> Any tear-down must **re-arm from a persisted deadline** (a GameVar holding the
> next-strike time), never restart blind.

This is the most powerful and the most dangerous layer. It should be built last,
only for what survives layers 2 and 3, and each module that uses it needs its own
A/B plus a long-interval soak.

---

## 3. Per-module disposition (12 exposed — membership corrected BOTH ways by the sweep: see §4a for the addition and §5.2 for the removal)

| module | default? | route in | proposed layer |
|---|---|---|---|
| `Fix_MeteorFrequency` | yes | global GT thread body | **3** — delete the body (worked example above) |
| `Opt_DroneOverhaul` | opt-in* | `Drone:Idle`, work after the call | **2** — move moonlighting out of the command |
| `Fix_RainsDeadlock` | yes | `fixed_loop` → global `RainsDisasterLoop` | 3 if an input exists, else **1** |
| `Fix_ArrivalDeaths` | yes | `Colonist:Arrive` command + own `Sleep` | needs its own look — a command body replacement |
| `Fix_TrainWaitTime` | yes | `Colonist:BoardVehicle` command body | needs its own look |
| ~~`Fix_TrainCargoDumping`~~ **NOT EXPOSED** | yes | ~~`Train:UnloadAll` command body~~ | ❌ **REMOVED by the sweep (§5.2)** — `UnloadAll` is fully synchronous, so a thread can never be blocked inside it. "It is a command body" was the wrong test |
| `Fix_BombardmentSpread` | yes | replaces blocking `WaitBombard` + own thread | 1 |
| `Fix_MeteorStormWedge` | yes | own `CreateGameTimeThread` | 1 |
| `Fix_CrystalMysteryHang` | yes | own thread, hourly `Sleep` loop | 1 |
| `Fix_ExtenderFlapChurn` | yes | own thread, short `Sleep` | 1 — narrow window |
| `Fix_TrackConnectorPingPong` | yes | own thread closure | 1 |
| `Fix_ShelterReflex` | yes | `Colonist:Idle` wrapper | **already compliant** with layer 2 |
| **`Fix_DroneUnreachableForever`** ⚠️ **added 2026-07-31 by the sweep** | yes | replaces `Drone:ApproachWrapper`; `building:DroneApproach(...)` blocks and **lines 52-77 run after it** | **2** — move the failure-record ahead of the call or into a hook. Same shape as the measured `Opt_DroneOverhaul` leak. See §4a |

\* `Opt_DroneOverhaul` leaked **with its own toggle OFF** — the wrapper installs
at file scope and only early-returns. Opt-in status is not protection.

---

## 4. The four decisions — ALL TAKEN 2026-07-31 (owner)

### 1. Layer ordering — ✅ ADOPTED, 3 → 2 → 1

Binding standing approach for every fix, new or repaired. **Written into
`FIX_POLICY.md` §3a**, which is now the authoritative statement of the rule;
this file keeps the analysis. Layer 1 is built **last**, only for what survives
layers 3 and 2, and every module that uses it needs its own A/B plus a
long-interval soak.

### 2. The layer-3 sweep — ✅ AUTHORISED, and it is the critical path

Game-free source pass over the remaining full-replacement modules, asking of
each: *is there a synchronous input we could patch instead of replacing a
blocking body?* The owner authorised the **full** scope (all full-replacement
modules), not just the 13 exposed — layer-3 wins on currently-safe modules are
worth having, because a module that keeps vanilla's body cannot regress into
this defect class later. **This is the only thing owed on F86 right now.**

### 3. F02 — ✅ HOLD LIFTED 2026-07-31 (was: held until the sweep reports)

~~The owner declined to take F02 module-by-module.~~ **The sweep has reported
(§5) and the hold is LIFTED: F02 is built with the rest of the authorised set.**
It is the only site with *measured* permanent harm, so it leads the build.

The design is settled and two corrections apply — see the boxed correction in §2,
Layer 3.

When it is unheld, the design is settled and two corrections apply — **the
wrapper keys on `CurrentThread()`, not on the descriptor** (see the boxed
correction in §2, Layer 3; descriptor-keying would change meteor-storm warning
timing), and the residual `Sleep(5000)` is ~10 game minutes, not zero. The PT-01
watchdog can split out as a second save-safe module: vanilla emits
`Msg("MeteorDone")` (`Meteors.lua:388` — verified), so it can time strikes from
`OnMsg`, check `IsValidThread(Meteors)` on `NewDay`, and restart **vanilla's**
body. Note the watchdog is already save-safe where it sits (`OnMsg` handlers,
no yield), so moving it is tidiness, not an F86 requirement.

### 4. Sequencing — ✅ SAVE-SAFETY RULES FIRST, then D10 and D12

Neither approved build starts until these rules are settled. Both touch
colonist assignment, which is command-thread territory, and building them first
risks adding new leak sites to a defect that already blocks release. This
supersedes the board's "confirm the owner's intent before starting one" for
these two items: the answer is **not yet**.

---

## 4a. ⚠️ `Fix_DroneUnreachableForever` IS EXPOSED — found by the sweep, 2026-07-31

**`Fix_DroneUnreachableForever` was missing from every earlier count**, including
a "no 13th site" certification written earlier the same day and committed in
`23dd59d`. **That certification is WITHDRAWN.**

> ⚠️ **On the COUNT specifically, read §5.2, not this section.** This module's
> addition was first published as "the list is 13". The same sweep then found
> that **`Fix_TrainCargoDumping` does not belong on the list at all**, so the
> total settles back at **12** with two membership changes rather than one. The
> addition below is solid; the interim "13" is superseded.

**The site.** `Code/Fix_DroneUnreachableForever.lua:46-78` replaces
`Drone:ApproachWrapper` wholesale. Line 51 calls
`building:DroneApproach(self, resource)` and **lines 52-77 run after it** —
table surgery, a `table.count`, and `self.command_center:UpdateConstructions()`,
then `return IsValid(building) and result`. Three legs, all verified in Src:

1. **`DroneApproach` blocks.** Every one of its ~20 implementations terminates in
   `drone:Goto` / `GotoBuildingSpot` / `GotoBuildingsSpot` / `EnterBuilding`, and
   `Unit:Goto` (`Unit.lua:130`) sits in a `while true` loop around
   `pfSleep(self, status)`.
2. **It runs on a game-time thread.** `ApproachWrapper`'s only four callers are
   `Drone:Work` (`:920`), `Drone:PickUp` (`:972`), `Drone:Deliver` (`:1239`) and
   `Drone:EmergencyPower` (`:1325`) — all drone **commands**, which run on
   `CreateGameTimeThread` command threads (`CommandObject.lua:100`).
3. **There is mod code after the blocking call** — the layer-2 violation.

This is the **same shape as the measured `Opt_DroneOverhaul:188-190` leak**, so
it is not a theoretical exposure: after uninstall the resumed frame reaches
`IsValid(...)` with an empty `_ENV` and throws on a drone work path.

**Why three earlier checks missed it, and the method that catches it.** A grep
for `^function Drone:` was defeated by two things at once: the module installs
via `local D = Drone` … `function D:ApproachWrapper` — an **alias** — and it does
so **indented inside `apply()`**, so the column-0 anchor failed too. A yield-grep
of `Code/` also misses it, because the module contains no yield of its own; it
blocks through a **callee**.

> **The reliable key is what each module ASSIGNS, extracted alias-blind:**
> `grep -oE 'function [A-Za-z_][A-Za-z_0-9]*:[A-Za-z_][A-Za-z_0-9]*\('` over
> `Code/`, then for each target read **vanilla's body in Src** and ask whether it
> or any callee can yield. Do **not** key on `SMRFixPack.Require{class=,method=}`
> — that declares a *self-check* target, not a replacement, and over-catches
> badly (`Fix_LakeEntombment` checks `Unit:ExitImpassable`, which does block, but
> never replaces it).

**Everything else the sweep checked came back CLEAR**, each against vanilla's
body rather than its name:

| module | assigns | verdict |
|---|---|---|
| `Fix_MirrorSphereSite` | `StartAction` | **safe** — vanilla's body creates the `WaitWakeup` thread; ours is a thin wrapper that ends `return orig(self, action, ...)` |
| `Fix_TrainPlatformWedge` | `Colonist:ExitVehicle` | **safe** — no yield in 32 lines |
| `Fix_VacuumWalks` | `Colonist:TryToEmigrateToDome` | **safe** — no yield in 47 lines |
| `Opt_CohortHousing` | `UpdateResidence`, `FindEmigrationDome` | **safe** — no yield (9 and 119 lines) |
| `Fix_TouristSatisfaction` | `Colonist:UpdateSatisfaction` | **safe** — no yield |
| `Fix_NightShiftWork` | `Colonist:ShouldLeaveForWork` | **safe** — no yield |
| `Fix_DroneTransportMinors` | `DroneControl:UpdateRocketsInternal` | **safe** — no yield; own file adds no thread |
| `Fix_LakeEntombment` | `LandscapeLake:PlacePrefab` | **safe** — no yield; it only *invokes* `ExitImpassable` via `SetCommand` on another unit |
| `Fix_SmallLandscapeSites` | `GetClosestDests` | **safe** — returns before the caller's `drone:Goto` |
| `Fix_RocketInteractGuard` | `CanInteractWithObject`, `InteractWithObject` | **safe** — both already layer-2 compliant |

**Disposition for the new site:** `Fix_DroneUnreachableForever` is a **layer 2**
case, and an easy one — the post-call block only records a failure timestamp, so
it can move ahead of the call or into a hook. It does **not** need layer 1.

## 5. THE LAYER-3 SWEEP — RESULT (2026-07-31, game-free, decision 2 discharged)

### 5.1 Method — and why the first two attempts were thrown away

The question per module: *is there a **synchronous** input we could patch instead
of replacing a blocking body?* That needs a sound answer to "can this function
block", and two attempts at that were discarded before one worked:

1. **Pattern-grepping for yields failed.** `Colonist:BoardVehicle` contains no
   `Sleep`/`WaitMsg`, yet it blocks for an entire train journey via
   `self:PlayPrg(...)` in its `while self.holder == vehicle` loop. Any fixed list
   of "blocking-looking" names will miss one.
2. **Transitive analysis resolved by bare function name failed harder** — it
   marked **7,621 of 15,106** names blocking, claiming `LandscapeForEachUnit`
   blocks "via `IsValid`". Common accessor names collide with unrelated blocking
   methods, and the result was noise.

**What works** (kept in the repo as `tools/blocking_analysis.py`, re-runnable
after any game update): seed from the engine's four
primitives — `Sleep` / `WaitMsg` / `WaitWakeup` / `PlayState`
(`PersistGatherPermanents`, `cthreads.lua:451-464`) — then propagate **only
through unambiguous callees**, where *every* definition of that name blocks.
Names with a mix are reported AMBIGUOUS and read by hand against the specific
class we patch. That gives **633 of 15,106 names yielding directly**, which is a
believable figure, and every ambiguous case resolved cleanly.

### 5.2 ⚠️ The exposed set is ~~12~~ **at least 13 (adjudication 2026-07-31)**, and the membership changed BOTH ways

> ⚠️ **Adjudication correction:** `Fix_CaveInsNoDisasters` is capturable (live
> `info` local in the engine's periodic-repeat loop while the yielding
> UndergroundMarsquake FUNC runs — ~1 in 9 Underground-map saves) and belongs on
> this list with disposition **compliant — no work**, alongside
> `Fix_ShelterReflex`. Both sweeps missed it because their enumeration keys
> (`function C:m(` grep; full-replacement scope) cannot see table-slot
> assignments. The build scope is unchanged; the count and the method are what
> this corrects. `docs/F86_ADJUDICATION.md` §3.1, §6 step 7.

The count returns to 12, but it is not the original 12:

- **ADDED — `Fix_DroneUnreachableForever`** (§4a): replaces
  `Drone:ApproachWrapper`, which blocks in `DroneApproach` and has our code after
  the call.
- **REMOVED — `Fix_TrainCargoDumping`**: `Train:UnloadAll`
  (`Train.lua:783-803`) is **fully synchronous** — read line by line, it is
  `pairs`/`ipairs` table work over `RequestUnassignUnit`, `GetStoredAmount`,
  `GetTargetAmount`, `AddResource`, none of which yields, and the analysis agrees.
  A thread can never be *blocked inside it*, so a save cannot capture it. It was
  listed on the assumption that a command body is exposed by virtue of being a
  command body; **that assumption is wrong — the test is whether it yields.**

> The general lesson, worth more than either correction: **"it is a command
> method" is not the test, and neither is "it contains no `Sleep`".** The test is
> whether the function can be on the stack while the thread is blocked — which
> means reading what it *calls*, transitively.

### 5.3 Result — 5 of the 12 have a layer-3 or layer-2 route out

Every "input" named below was checked and is **synchronous**, so each is a
legitimate layer-3 target rather than a guess.

| module | why it is exposed today | sweep verdict |
|---|---|---|
| `Fix_MeteorFrequency` | replaces the global `Meteors` GT thread body | **LAYER 3** — wrap `GetDisasterWarningTime` (sync), keyed on `CurrentThread()`; delete the body. *(F02 — HELD by decision 3)* |
| **`Fix_DroneUnreachableForever`** | `ApproachWrapper`, work after a blocking call | ⭐ **LAYER 3 — patch the CONSUMER, not the writer.** The defect is only the timestamp value; its reader `Drone:CleanUnreachables` is **synchronous**. Normalise the poisoned future timestamps there and our code leaves the drone command thread entirely |
| `Fix_ArrivalDeaths` | `Colonist:Arrive`, direct yield | **LAYER 3 for half (b)** — the unwalkable `safety_dome` comes from `ChooseDome` / `GetDomesReachableByColonists`, **both synchronous**. Half (a), the raw `SetPos` with no passability search, still needs a design pass |
| `Fix_TrainWaitTime` | `BoardVehicle`, blocks via `PlayPrg` for the whole journey | **LAYER 3** — the restamp can come from a wrapper on `TransportStatistics:AddSpentTime` (**sync**), which vanilla calls at the exact boarding moment (`:511`); the triple-spend site `ExitVehicle` is **also sync** |
| `Fix_RainsDeadlock` | replaces the global `RainsDisasterLoop` (direct yield) | **LAYER 2, and vanilla's loop stays** — the deadlock is `RainsDisasterActivation` returning early on collision without posting `RainDisasterEnd`. Wrap it: work before, `return orig(...)`. `IsDisasterActive`, `IsDisasterPredicted` and `FinishRainProcedure` are all sync |
| `Opt_DroneOverhaul` | `Drone:Idle`, work after the call | **LAYER 2** — move moonlighting out of the command body (unchanged) |
| `Fix_ShelterReflex` | `Colonist:Idle` wrapper | **already compliant** — nothing owed |
| `Fix_BombardmentSpread` | replaces blocking `WaitBombard` + own GT thread | **NO LAYER 3.** The defect is one discarded local (`spawn_dir`) mid-function with no seam near it; there is no input whose value fixes it. Layer 1, or accept |
| `Fix_MeteorStormWedge` | own `CreateGameTimeThread` (`:119`) | Layer 1 |
| `Fix_CrystalMysteryHang` | own `CreateGameTimeThread` (`:44`) | Layer 1 |
| `Fix_ExtenderFlapChurn` | own `CreateGameTimeThread` (`:77`) | Layer 1 — narrow window |
| `Fix_TrackConnectorPingPong` | own `CreateGameTimeThread` (`:156`) | Layer 1 |

**Sizing answer for the owner: five modules can leave the exposed set without
layer 1** — `MeteorFrequency`, `DroneUnreachableForever`, `TrainWaitTime`,
`RainsDeadlock` by a full route, `ArrivalDeaths` by half. What genuinely needs
the dangerous `SaveGameStart` layer is **four own-thread modules plus
`BombardmentSpread`** — and each of those four should first be asked whether its
thread is needed at all, which this sweep did not do.

**Our own threads, inventoried:** six modules call `CreateGameTimeThread`
(`BombardmentSpread:137`, `CrystalMysteryHang:44`, `ExtenderFlapChurn:77`,
`MeteorStormWedge:119`, `RainsDeadlock:56/:93`, `TrackConnectorPingPong:156`).
`00_Core:485` and `Fix_MilestoneCrash:40` use `CreateRealTimeThread` and are
**safe by construction** — real-time threads are not persisted.

### 5.4 The non-exposed half — SWEPT 2026-07-31, all 22 modules

**First, what this half is and is not for.** These 22 modules are **already save-
safe** — every one is synchronous, so F86 cannot reach them and nothing here is a
defect. The benefit is different and worth stating plainly, because it changes
how the results should be read:

- **Fewer body copies to re-verify per game update.** FIX_POLICY §1.5 full
  replacements are the ones that rot, and the fpk extraction diff is a release
  gate (WORKFLOW.md). Every conversion is one less body to re-check forever.
- **A wrapper degrades gracefully; a body copy does not.** If a future patch
  fixes the vanilla bug, a chained wrapper becomes a harmless no-op, whereas a
  §1.5 copy silently reinstates the old body's shape and can *undo* the official
  fix. This is the stronger argument of the two and it is not currently written
  down anywhere.

**Scope correction:** the outstanding set is **22**, not the "~17" estimated in
§5.4 — that figure was a guess and is superseded.

#### A. Convert to a chained wrapper — no body copy, verified feasible (6)

Each was checked against the shipped body, not inferred from our header.

| module | current | the wrapper that replaces it |
|---|---|---|
| ⭐ `Fix_SmallLandscapeSites` | replaces `GetClosestDests` | **The cleanest in the pack.** `GetClosestDests(drone, top_count)` *already takes* the bound as a parameter and the only caller never passes it, so it defaults to 5 and over-runs a short `drone_dests_cache`. A wrapper clamping `top_count` to `#self.drone_dests_cache` fixes it with **zero** copied logic |
| `Fix_NightShiftWork` | replaces `ShouldLeaveForWork` | Vanilla returns `true`/nil and the fix only ever needs to return true in **more** cases (the unreachable hours 0-1). `local r = orig(self) if r then return r end return <wrap-around window>`. **Shift 1/2 behaviour is then identical by construction**, which is strictly stronger than the current copy's hand-verified "bit-identical" claim |
| `Fix_GeneForging` | replaces global `GetRareTraitChance` | Vanilla returns `nil` or `TechDef.GeneSelection.param1`; the two techs are meant to **add**. `return (orig(unit) or 0) + <GeneForging param1 if researched>`. Downstream does `100 + (x or 0)`, so nil-vs-0 is equivalent |
| `Fix_ShuttleHubOffAvailable` | replaces global `IsLRTransportAvailable` | Vanilla returns a boolean and the fix only makes it **stricter**, so `false` from the original is already correct. Re-validate only on the `true` path |
| `Fix_UpgradeModifierLeak` | replaces `StopUpgradeModifiers` | Vanilla iterates a string-keyed table with `ipairs`, so **the original is a verified no-op**. A post-wrapper that runs the correct `pairs` loop is sufficient (and must honour `only_for_object`) |
| `Fix_TrainCargoDumping` | replaces `Train:UnloadAll` | **Layer 3**: the disabled-resource cap comes from the demand request's `GetTargetAmount` (**verified synchronous**). Return 0 for a disabled resource and vanilla's `Min(carried, station_cap)` yields 0 by itself |

#### B. Real route, but needs a design pass before anyone commits (4)

| module | route | the open question |
|---|---|---|
| `Fix_LanderCargoRatchet` | wrap `GetTotalCargoAvailable` to count what is already aboard | It is a global with **14 callers**; needs narrow keying to the auto-cargo path |
| `Fix_ShuttleTransportCache` | additive `OnMsg` flush of `g_TransportationModeToCommunityCache` on shuttle-hub state change | A flush is **coarser than the correct fix** (the real defect is a cache key missing `shuttles_available`); trades correctness-of-key for a smaller footprint |
| `Fix_RocketDroneChurn` | wrapper pair — flag on `AddCargoDemandRequest`, no-op the Connect/Disconnect unless set | Two coupled wrappers replacing one body; may not be simpler |
| `Fix_LandscapeUnitFilter` | wrap `Landscape_ForEachObject` and apply the dropped filter to the callback | Must key on the unit params so the **stockpile** path, which already passes its own filter correctly, is untouched |

#### C. No route — the body copy is the right technique (9)

`Fix_LowStorageWarning` (its header already proves a wrapper cannot work: the
unreachable add-branch means vanilla's else-branch *removes* the entry every
hour) · `Fix_TouristSatisfaction` (path-dependence mid-function; a correcting
wrapper risks double-accounting) · **`Fix_TrackSalvageWipe`** (a **130-line**
copy — the pack's single largest rot exposure — but the defect is a missing
bounds check on a `repeat…until`, and no input bends it) · `Fix_TrackSalvageRefund`
(multi-target refund accounting) · `Fix_TrainPlatformWedge` (`table.remove` vs
`table.remove_entry` mid-function; also a §1.5 **reconstruction**, recreating the
file-local `stat_scale`) · `Fix_VacuumWalks` (the gate compares against a const
used elsewhere) · `Fix_WispRewards` (a missing `* 1000` inside a branch; wrapping
`Modifier:Change` is far too broad) · `Fix_PayloadTemplateRefill` (the template
comes from a **file-local** resolver, unreachable) · `Fix_UniversityOvertraining`
(the tempting input is `ValidateBuilding` — **checked, and it has 55 callers**,
so patching it would reach story bits and staffing; rejected).

#### D. Already optimal — do not touch (3)

- **`Fix_IndependenceTerraforming`** — already a pure **data/preset patch**
  (FIX_POLICY §1.1, the most preferred technique). Caught by the sweep's
  header grep, not actually a full replacement.
- **`Fix_DomeFreeSpaceMismatch`** — the "replacement" is a **two-line** method
  where *the fix is literally the argument*. An input patch on
  `GatherFreeLivingSpaces` would be **worse**: it would also hit
  `MicroGHabitatBase:RefreshFreeLivingSpaces`, which this module **deliberately
  excludes for a recorded reason** (an asteroid habitat's `working` state is its
  life support — F73's subject). Leave it.
- **`Fix_DroneTransportMinors`** — mixed, and its larger half is already ideal:
  item **(b) is an additive `OnMsg.OnPassabilityChanged` handler** (§1.2). Only
  (a) replaces `UpdateRocketsInternal`, and no input route was found for it.

#### Bottom line for this half

**6 of 22 convert cleanly** to a chained wrapper with verified feasibility,
**4 more have a route worth designing**, **9 are correctly full replacements**,
and **3 are already at the best available technique**. None of it is urgent and
none of it blocks F86 — but the 6 in group A are cheap, individually testable,
and each permanently removes a body copy from the per-update re-verification
gate. `Fix_TrackSalvageWipe` is worth knowing about for the opposite reason: it
is the biggest copied body we carry and it has **no** way out.

### 5.5 Decision 2's full scope — ✅ DISCHARGED

The owner authorised the sweep over **all** full-replacement modules. Both
halves are now done: the **exposed set** in §5.3 and the **22 non-exposed
modules** in §5.4. Nothing further is owed on the sweep.

*Two guesses recorded here before that second half ran are superseded by it: the
outstanding count was estimated at "~17" and is actually **22**; and
`Fix_DomeFreeSpaceMismatch` was floated as a layer-3 candidate but is
**rejected** on inspection — an input patch there would over-reach into MicroG
habitats, which the module deliberately excludes (§5.4 group D).*

## 6. ⭐ THE BUILD — AUTHORISED SCOPE, owner 2026-07-31

**Scope: Tiers 1 and 2. Layer 1 is NOT to be built.** The tiering below is the
reason, and it is the thing to understand before touching any of it.

### 6.1 The tiering that set the scope

Exposure severity is **not** about the module — it is about whether we replaced
something vanilla would otherwise keep running:

- **We ADD a thread** (a heal loop, a watchdog) → after uninstall it resumes,
  errors once and dies. The player loses the fix, which they lose by
  uninstalling anyway. **Net harm ≈ one log line.**
- **We REPLACE a vanilla body** → our version is what got serialised, so when it
  errors after uninstall **vanilla's behaviour is gone too**. The player ends up
  **worse than if they had never installed the pack.**

> ⚠️ **ROUND-2 CORRECTION (2026-07-31, measured): "errors once and dies" only
> happens when the body touches a mod-created name.** Orphans resolve vanilla
> globals through the fallback env, so per-module (adjudication §2.11/§8): the
> ADD-class four end by themselves — CrystalMysteryHang expires at its frozen
> 10-sol deadline, ExtenderFlapChurn and TrackConnectorPingPong complete
> one-shots silently, StormWedge alone dies at a `SMRFixPack.*` touch (after
> restarting vanilla's storm thread; can leave one stray `g_MeteorStormStop`)
> — while a REPLACE-class body with only-vanilla names (`fixed_loop`) **keeps
> running our code forever, silently**, which is worse than the loud loss the
> table above describes. The dimension that matters: *who waits on the promise
> this frame keeps, and would anyone ever notice the orphan working.*

> ⚠️ **This tiering is REASONED from the measured mechanism, not itself
> measured.** Only two sites have ever been observed leaking
> (`Fix_MeteorFrequency`, `Opt_DroneOverhaul`). If Tier 3's residual is ever
> challenged, the control is one PT-20-method leg against a single own-thread
> module: block it, save, uninstall, load, count errors. The owner accepted the
> residual without requiring that leg.

### 6.2 What gets built

**Tier 1 — uninstall leaves the player worse than vanilla. Build first.**

| module | harm | route |
|---|---|---|
| `Fix_MeteorFrequency` | **MEASURED** — colony's meteors stop permanently, no self-heal | Layer 3: wrap `GetDisasterWarningTime`, keyed on `CurrentThread()`; delete the body; split the PT-01 watchdog onto `Msg("MeteorDone")` |
| `Fix_RainsDeadlock` | ⚠️ ~~its death stops that rain type for the save~~ **CORRECTED (round 2, measured orphan behaviour): `fixed_loop` touches only vanilla names, so it does NOT die — an uninstalled player keeps our rains loop FOREVER, silently. The harm is save-integrity (pack code becomes unremovable), not lost rains** | Layer 2: wrap `RainsDisasterActivation` to post `RainDisasterEnd` on the collision early-return — ⚠️ **shape gated on the GT-creation-ordering probe** (if a new GT thread runs at creation, the Msg fires before the loop reaches `WaitMsg` and the wrapper does nothing — adjudication §4.1/§8). **Plus the MIGRATION PASS (owed, or the repair means nothing for existing saves): a `RefreshRainsLoops`-style swap of persisted loops onto VANILLA's `RainsDisasterLoop`, keyed on a VERSION-STAMPED marker (the shipped boolean now means "old fixed body"), and handling id-less entries the current pass skips (`Fix_RainsDeadlock.lua:88-91`; the `test 2i` fixture's `toxic` entry has `id=nil`)** |

**Tier 2 — a unit's command thread dies; recoverable but noisy.**

| module | route |
|---|---|
| `Fix_DroneUnreachableForever` | Layer 3 — patch the **consumer** `Drone:CleanUnreachables` (sync); stop replacing `ApproachWrapper` |
| `Fix_TrainWaitTime` | Layer 3 — restamp from a wrapper on the sync `TransportStatistics:AddSpentTime`; stop replacing `BoardVehicle` |
| `Fix_ArrivalDeaths` | Layer 3 for **half (b)** via `ChooseDome` / `GetDomesReachableByColonists`. ⚠️ **Half (a) — the raw `SetPos` with no passability search — has NO route yet and needs a design pass before this module is finished** |
| `Opt_DroneOverhaul` | Layer 2 — move moonlighting out of the command body. ⛔ **DRONE-OWNED: blocked until the owner grants the carve-out** |

### 6.3 What is deliberately NOT built

**Tier 3 — accepted residual, by owner decision.** `Fix_MeteorStormWedge`,
`Fix_CrystalMysteryHang`, `Fix_ExtenderFlapChurn`, `Fix_TrackConnectorPingPong`.
Each owns its thread, so nothing vanilla is lost; each would cost **one error
line**, not the 98/session `Opt_DroneOverhaul` produced (that figure came from
*many* drone command threads, one per drone). None has a layer-3 route.

`Fix_BombardmentSpread` is also **not built**: it has **no layer-3 route at all**
(the defect is a discarded local mid-function with no seam), bombardments are a
rare Mystery-7 event, ~~and the damage is one broken volley~~.
⚠️ **HARM STATEMENT CORRECTED TWICE — final state (round 2): the residual is
≈ NOTHING, and no re-take is owed.** Round 1 replaced "one broken volley" with
a permanent Mystery-7 wedge (untimed `WaitMsg("BombardEnd")`,
`Mystery 7.generated.lua:941-942`). Round 2's measured orphan behaviour
falsified that in turn: the replacement body references **no mod-created
name**, so a mid-volley orphan resolves vanilla globals through the fallback
env, **completes the volley, and `BombardEnd` posts** — Mystery 7 proceeds.
Keep the fix; the untimed-WaitMsg contract stays on record as the pattern to
check on any future module. `docs/F86_ADJUDICATION.md` §3.2 (as amended), §8.3.

⛔ **LAYER 1 IS NOT TO BE BUILT.** The owner declined it explicitly. Its own spec
calls it the most dangerous layer, and the autosave-restart trap could recreate
PT-01's permanent-silence signature out of our own code. **Do not propose it
again without new evidence that Tier 3 causes real harm.**

### 6.4 Sequencing

1. Tier 1 (`MeteorFrequency`, then `RainsDeadlock`).
2. Tier 2, `Opt_DroneOverhaul` only if the carve-out is granted.
3. **Then** the six wrapper conversions of §5.4 group A, as **one batch with a
   single A/B leg** — deliberately after, so the F86 legs stay clean of
   unrelated change.
4. **D10 and D12 remain HELD until these repairs land and verify** — the owner
   confirmed the hold means *until built*, not *until the rules were written*.

## 7. What is NOT proposed

- ~~**No cleanup mod.** Parked (`FUTURE_IDEAS.md` entry 5).~~ ⭐ **SUPERSEDED
  by owner directive 2026-07-31: the save-exit deliverables are now
  PRELAUNCH — filed as `BUGS.md` D13** (the FUTURE_IDEAS entry was MOVED
  there 2026-08-01, keeping that file's "nothing here is work" rule true).
  ⛔ D13's spec is **gated on Tiers 1+2 landing AND verifying** — the
  cleaner is scoped against their measured output, never today's leak set.
  The "reinstall revives the thread" remedy stays true but carries the F88
  caveat (the revive mechanism re-rolls timers until the Tier-1 rewrite
  ships). Plan: `F86_EXECUTION_PLAN.md` Phase 5; record: D13.
- ~~No FIX_POLICY edit yet~~ — **DONE 2026-07-31.** The owner adopted the
  ordering, so the rule landed in **`FIX_POLICY.md` §3a**, which is now
  authoritative for it. This file keeps the analysis and the per-module
  disposition.
- **No changes to the ~62 safe modules** *(beyond whatever the authorised
  layer-3 sweep proposes — the sweep may recommend converting a currently-safe
  full replacement to an input patch, but nothing is built without a further
  owner go)*.
