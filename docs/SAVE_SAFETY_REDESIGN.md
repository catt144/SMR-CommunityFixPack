# Save-safety redesign — the F86 remedy, for owner decision

**Status: PROPOSAL. Nothing here is built, approved or owed.** Written
2026-07-31 immediately after the PT-20 leg that measured the defect. The defect
itself is `BUGS.md` **F86** (P1, blocks release); this file is only the *how*.

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

*Scope check:* `GetDisasterWarningTime` serves other disasters and the tower UI
text, so the wrapper must key on the meteor descriptor and defer to the original
otherwise.

**Which other modules could take this shape is NOT yet swept.** One strong
candidate is confirmed; the remaining ~24 full-replacement modules have not been
examined for it. That sweep is a game-free pass and is the single highest-value
piece of follow-up work here.

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

## 3. Per-module disposition (12 exposed)

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

\* `Opt_DroneOverhaul` leaked **with its own toggle OFF** — the wrapper installs
at file scope and only early-returns. Opt-in status is not protection.

---

## 4. What the owner is actually deciding

1. **Adopt the layer ordering** (3 → 2 → 1) as the standing approach, or not.
2. **Authorise the game-free sweep** of the ~24 remaining full-replacement
   modules for layer-3 opportunities. This is the highest-value follow-up and
   needs no game time.
3. **F02 specifically** — approve deleting `Fix_MeteorFrequency`'s body in favour
   of the `GetDisasterWarningTime` input patch. Note the PT-01 watchdog splits
   out as a second, also save-safe module: vanilla emits `Msg("MeteorDone")`
   (`Meteors.lua:388`), so it can time strikes from `OnMsg`, check
   `IsValidThread(Meteors)` on `NewDay`, and restart **vanilla's** body.
4. **Sequencing against the launch build.** D10 and D12 are approved builds. If
   they land before these rules are settled, they may add new leak sites — both
   touch colonist assignment, which is command-thread territory.

## 5. What is NOT proposed

- **No cleanup mod.** Parked (`FUTURE_IDEAS.md` entry 5). The remedy for damage
  already in a player's save is measured and simple: **reinstalling the pack
  revives a killed thread** (confirmed 2026-07-31 — our `LoadGame` restart runs
  and `IsValidThread(Meteors)` returns `true`). Uncomfortable, but real.
- **No FIX_POLICY edit yet.** The rule belongs there once the owner picks the
  ordering. Drafted wording: *no mod function may be reachable below a yield on
  a game-time thread; prefer patching a synchronous input over replacing a
  blocking body; never place mod code after a call that can block.*
- **No changes to the ~62 safe modules.**
