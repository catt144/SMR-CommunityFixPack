# Save-safety redesign — the F86 remedy

**Status: DECIDED 2026-07-31 (owner). The layer ordering is ADOPTED and now
lives in `FIX_POLICY.md` §3a as a hard rule. The layer-3 sweep is AUTHORISED
and is the critical path. F02 is HELD until that sweep reports. D10 and D12 are
sequenced BEHIND these rules.** Written 2026-07-31 immediately after the PT-20
leg that measured the defect; the four decisions were taken the same day and are
recorded in §4. The defect itself is `BUGS.md` **F86** (P1, blocks release);
this file is the *how*.

> **What is owed right now: the sweep (§4 decision 2), and nothing else.** It is
> game-free. No code may be written against this file until the sweep reports —
> that includes F02, which the owner explicitly held for it.

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
  yield — can never be captured. That is ~62 of 74 modules, safe by
  construction, with no work needed.
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

**Which other modules could take this shape is NOT yet swept.** One strong
candidate is confirmed; the remaining full-replacement modules have not been
examined for it. **That sweep is AUTHORISED (§4 decision 2, owner 2026-07-31),
is game-free, and is now the critical path** — F02 itself is held until it
reports.

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

## 3. Per-module disposition (13 exposed — was 12, see §4a)

| module | default? | route in | proposed layer |
|---|---|---|---|
| `Fix_MeteorFrequency` | yes | global GT thread body | **3** — delete the body (worked example above) |
| `Opt_DroneOverhaul` | opt-in* | `Drone:Idle`, work after the call | **2** — move moonlighting out of the command |
| `Fix_RainsDeadlock` | yes | `fixed_loop` → global `RainsDisasterLoop` | 3 if an input exists, else **1** |
| `Fix_ArrivalDeaths` | yes | `Colonist:Arrive` command + own `Sleep` | needs its own look — a command body replacement |
| `Fix_TrainWaitTime` | yes | `Colonist:BoardVehicle` command body | needs its own look |
| `Fix_TrainCargoDumping` | yes | `Train:UnloadAll` command body | needs its own look |
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

### 3. F02 — ⏸️ HELD until the sweep reports

The owner declined to take F02 module-by-module. **Do not touch
`Fix_MeteorFrequency` yet.** The whole layer-3 set lands as one designed change
once the sweep has scoped it. Accepted cost, stated at the time of the decision:
the measured, colony-killing leak stays shipped in the meantime.

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

## 4a. ⚠️ THE EXPOSURE LIST IS 13, NOT 12 — corrected by the sweep, 2026-07-31

**`Fix_DroneUnreachableForever` is a 13th exposed module and it was missing from
every earlier count**, including a "no 13th site" certification written earlier
the same day and committed in `23dd59d`. **That certification is WITHDRAWN.**

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

## 5. What is NOT proposed

- **No cleanup mod.** Parked (`FUTURE_IDEAS.md` entry 5). The remedy for damage
  already in a player's save is measured and simple: **reinstalling the pack
  revives a killed thread** (confirmed 2026-07-31 — our `LoadGame` restart runs
  and `IsValidThread(Meteors)` returns `true`). Uncomfortable, but real.
- ~~No FIX_POLICY edit yet~~ — **DONE 2026-07-31.** The owner adopted the
  ordering, so the rule landed in **`FIX_POLICY.md` §3a**, which is now
  authoritative for it. This file keeps the analysis and the per-module
  disposition.
- **No changes to the ~62 safe modules** *(beyond whatever the authorised
  layer-3 sweep proposes — the sweep may recommend converting a currently-safe
  full replacement to an input patch, but nothing is built without a further
  owner go)*.
