# F86 — the discovery session's position, stated for adversarial review

> ⛔ **EVERY COUNT IN THIS FILE IS SUPERSEDED (2026-08-13) by
> `agent/reports/D13_EXPOSED_SET.md`** — 27 sites over BOTH shipped trees (12
> capturable-code + 15 persisted-data), derived from source with no inherited
> number. "12 modules" / "only 12 exposed" / "62 safe" below are this session's
> **open lower bound**, and §3's own warning that the bound rests on an
> untested inference is precisely what that derivation went and tested. The
> position's *reasoning* is left intact; only its arithmetic is retired.

**Written 2026-07-31 by the session that found F86 (the PT-20 leg), at the
owner's request, to be compared against `docs/reports/F86_SESSION_FINDINGS.md` by an
independent reviewer.**

## How to read this document

This is **not** a summary of the project's current state — `STATUS.md`,
`BUGS.md` F86 and `SAVE_SAFETY_REDESIGN.md` are that, and they have been edited
by a later session. This is a statement of **what this session concluded and on
what evidence**, written deliberately *without* consulting the other session's
findings, so the two can be compared as independent positions.

Where a later session has since corrected something I claimed, **I have left my
original claim standing** rather than silently adopting the correction. Adopting
it would destroy the thing the owner is trying to measure. Section 7 lists the
places I most expect to be wrong.

**Every claim below is labelled:**

- **MEASURED** — observed in the game, with the observation reproducible from the
  record (log line, console read, or both legs of a control).
- **SOURCE** — read from `ModTools\Src` or the pack's own code. Not observed
  running.
- **INFERRED** — an argument built on MEASURED or SOURCE facts. This is where
  the risk lives.

---

## 1. The defect

**The claim:** pack code is serialised into the player's savegame and keeps
running after the mod is removed.

**MEASURED — two sites, one leg (`PT-20TEST`, cut from the 288-sol `test 2i`,
saved at sol 290).**

Site 1, `Fix_MeteorFrequency`:

```
[LUA ERROR] attempt to index a nil value (global 'SMRFixPack')
  Mod/SMR_CommunityFixPack/Code/Fix_MeteorFrequency.lua(106):   <>
Locals:  meteors | object MapSettings_Meteor 'Meteor_Low'
         spawn_time | number 60000
         warning_time | number 2250000
         hit_time   | number 60000
```

The strongest single piece of evidence in the whole leg is the **locals**.
`spawn_time 60000` and `hit_time 60000` are values *this session injected by hand
into that thread's stack* minutes before saving (by compressing the meteor
descriptor to 2 h and restarting the thread). They came back out of the savegame
inside our own function's frame. No game-install state, no stale file and no
mod-manager quirk can produce those numbers.

Site 2, `Opt_DroneOverhaul`: 98 occurrences of

```
Opt_DroneOverhaul.lua:96 attempt to index a nil value (global 'SMRFixPack')
  Opt_DroneOverhaul.lua(96): upvalue module_active
  Opt_DroneOverhaul.lua(190): <>
  [C](-1): global sprocall
  CommonLua/Classes/CommandObject.lua(246): <>
```

**Controls run (MEASURED).** The same save was loaded twice: once with the pack
disabled in the Mod Manager, once with the junction physically removed
(`1 mods installed`, Test Kit only). **98 vs 98 drone errors, one meteor error
each, identical locals.** The only difference in either log was the engine's own
wording (`present, but not loaded` → `not present`). Steam-verify and reinstall
rungs were stood down by agreement, on the grounds above.

**MEASURED — it does not self-heal.** A save written *after* the thread died
came back with `Meteors` as a thread object for which `IsValidThread` returns no
value. `_fixup.lua:54-55` only rebuilds a global GT thread when the save carries
*nothing* for that name, and a dead thread still counts as something.

**MEASURED — reinstalling the pack repairs it.** `PT-20TEST-B` loaded with the
pack restored: `IsValidThread(Meteors)` → `true`, our own `OnMsg.LoadGame`
restart having run.

## 2. The mechanism

**SOURCE.** `GlobalGameTimeThread` sets `PersistableGlobals[name] = true`
(`Lua\Config\_fixup.lua:15`). `OnMsg.PersistPostLoad` (`:50-56`) re-creates a
global GT thread **only when the save carries nothing** for it. Persist
serialises blocked stacks — `PersistGatherPermanents` (`cthreads.lua:451-464`)
registers `Sleep`/`WaitMsg`/`WaitWakeup` as sleeping functions found in thread
stacks. Each mod's environment is a permanent:
`permanents["Mod/" .. mod.id] = mod.env` (`CommonLua/Classes/Mod.lua:1642-1644`).

**MEASURED corroboration.** With the mod gone, the engine logged
`Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback permanent:
table: … [7]`, and the orphaned function then failed on *global* lookups
specifically (`SMRFixPack`), which is what an env-substitution predicts.

**INFERRED:** a mod function is not in `PersistGatherPermanents`, so it is
serialised **by value** rather than resolved by name, and comes back with its
`_ENV` replaced by that fallback table.

## 3. The filter — the load-bearing claim

> **Can this function be executing, or blocked, below a
> `Sleep`/`WaitMsg`/`WaitWakeup` on a GAME-TIME thread at the moment the save is
> written?**

**INFERRED.** It follows from §2 if — and only if — a save captures *blocked
threads and nothing else*. Two consequences I drew:

- **Synchronous mod code can never be captured** (data patches, getters, `Can…`
  predicates, UI handlers, non-yielding `OnMsg` bodies). This is what bounds the
  problem to **12 of 74 modules**, with ~62 safe **by construction and needing no
  work at all**.
- **Real-time threads are irrelevant** — not persisted (ENGINE_FACTS, and
  `00_Core`'s update-report thread is one).

**This is the single most load-bearing inference in my position.** Everything
about scope — "only 12 exposed", "62 safe", the entire triage — rests on it. It
was never tested in the negative direction: **I never demonstrated that a
synchronous mod function cannot end up in a save.** I argued it from how persist
works. If that argument is wrong, the exposure list is wrong.

**It also overturned a prior clearance (MEASURED).** The 2026-07-31 audit had
asked *where is the function stored* and cleared class tables as "restored as
permanents by name". `Opt_DroneOverhaul` writes `Drone.Idle` — a class-table
write — and leaked anyway, because the route into the save was a **thread
stack**, not the storage location. That is the correction that makes the filter
necessary.

## 4. The exposure list (~~12 modules~~) `[⛔ SUPERSEDED 2026-08-13 — D13_EXPOSED_SET.md §2/§4.1: 12 capturable-code sites over both trees, plus 15 persisted-data sites this key could never see]`

**INFERRED, built by grep + reading, NOT by testing each module.** Method:
`Sleep|WaitMsg|WaitWakeup` across `Code/`, every `CreateGameTimeThread`, every
`GlobalGameTimeThreadFuncs` write, and wrappers on methods confirmed to be
command bodies via `SetCommand("<name>")` in Src.

Proven: `Fix_MeteorFrequency`, `Opt_DroneOverhaul`. Asserted-exposed:
`Fix_RainsDeadlock`, `Fix_ArrivalDeaths`, `Fix_TrainWaitTime`,
`Fix_TrainCargoDumping`, `Fix_BombardmentSpread`, `Fix_MeteorStormWedge`,
`Fix_CrystalMysteryHang`, `Fix_ExtenderFlapChurn`, `Fix_TrackConnectorPingPong`.
Asserted-compliant: `Fix_ShelterReflex`.

⚠️ **Known hole in the method, and I flagged it during the session:** the test is
**transitive**. Our function does not need to contain the yield itself — it only
needs to be on the stack when something *deeper* yields. A grep for
`Sleep|WaitMsg` in `Code/` cannot find that. **The list is therefore a lower
bound, not an enumeration**, and I did not close it.

## 5. The proposed remedy

### Layer 3 — patch a synchronous input, keep vanilla's body

**SOURCE, untested.** Vanilla's meteor interval is
`Min(spawn_time, warning_time)` (`Meteors.lua:291-292`) because the first phase
of a two-phase wait was destroyed (§6). `GetDisasterWarningTime`
(`MapSettings.lua:94`) is synchronous and can never sit on a blocked stack, so
wrapping it to return `Max(orig, spawntime + spawntime_random)` makes `Min`
equal `spawn_time` and **vanilla's own body** produce the designed schedule.
`Fix_MeteorFrequency`'s replacement body is then deleted, removing the only site
with measured permanent harm.

**My scope caveat, stated as I stated it:** *"`GetDisasterWarningTime` serves
other disasters and the tower UI text, so the wrapper must key on the meteor
descriptor and defer to the original otherwise."* I did **not** enumerate its
callers. **I consider this the weakest untested claim I made** — see §7.

**Not swept.** I identified the *criterion* and one worked example. I explicitly
did not sweep the other ~24 full-replacement modules for layer-3 opportunities,
and said so.

### Layer 2 — no mod code after a call that can block

**INFERRED, and deliberately re-derived to avoid depending on an unmeasurable.**
I first justified this as *"tail-call the original so our frame leaves the
stack"*. That justification is **unobservable in this engine**, and I cancelled
the experiment I had designed to test it rather than run it: a tail call has
nothing after it, so a vanished frame and a surviving frame produce **identical
silence**, and any detector placed after the call stops it being a tail call.
The rule was restated to need no engine guarantee:

> Do all work **before** the call, then `return orig(...)`. Never place mod code
> after a call that can block — then whether or not the frame is serialised,
> there is nothing left to execute after removal.

`Opt_DroneOverhaul:188-190` violates it (MEASURED leak). `Fix_ShelterReflex:73`
complies (INFERRED harmless; by the argument above this is not testable).

**Residual I accepted:** an inert serialised function may sit in a save as dead
weight. It executes nothing, and no read available to us can see it.

### Layer 1 — `SaveGameStart` tear-down

**MEASURED that the hook exists.** A Test Kit probe logged `SaveGameStart FIRED
— SavingGame=true` and `SaveGameDone FIRED`, with `OnMsg.LoadGame` as a positive
control. `ModMsgBlacklist` (`Mod.lua:1430-1440`) blocks only `PersistSave`,
`PersistLoad`, `PersistGatherPermanents` and five non-save messages;
`DoSaveGame` fires `SaveGameStart` before the write (`Savegame.lua:1043`).
**This falsified a recorded project "fact"** that mods get no save hook and that
tidying up on save is unimplementable.

**SOURCE, NOT measured:** autosaves are the same path — `SaveAutosaveGame`
(`:1450-1453`) sets one flag and calls `DoSaveGame`. **No autosave was ever
observed firing the hook.** The probe is still armed for that reason.

**INFERRED trap, and I consider it the most dangerous thing in the design:**
autosaves fire ~once a sol, so a tear-down that *restarts* a loop would reset a
35–115 h meteor timer before it could expire — reproducing PT-01's
permanent-silence signature **out of our own repair**, and looking exactly like
the bug being fixed. Any tear-down must re-arm from a persisted deadline.

**Nothing about layer 1 is built or tested.**

## 6. F02's root cause (asked separately, affects layer 3)

**SOURCE.** Not "a dead `if`" — a **collapsed polling loop**. The fossil at
`Meteors.lua:280-283` is the loop that still exists intact 40 lines below in
`MeteorStorm` (`:319-341`): same `start_time`, same
`GameTime() - start_time > X - warning_time` test, same `Sleep(5000)`, but with
the `while` removed and the loop body pulled inside the `if`. Because
`start_time` is assigned and read with no yield between, the test degenerates to
`warning_time > spawn_time`.

`Min(spawn_time, warning_time)` is **not** the bug — it is the correct clamp for
when warning exceeds spawn, and `DustDevils.lua:171` carries it verbatim in
working code.

**Consequence (SOURCE):** interval = `Min(spawn, warning)` and
`GetDisasterWarningTime` = `Min(base + 12h × towers, 75h)`, so towers
*accidentally repair* the cadence — no towers gives ~6 h, several gives 65–75 h.
The players harmed are early colonies without towers.

**Owner decision recorded:** single meteors' ~30-second `Predict()` marker is
adequate; tower-scaled meteor warning is a feature and is declined.

## 7. Where I expect to be wrong

Listed for the reviewer's benefit, strongest doubt first.

1. **"Synchronous code can never be captured" (§3)** — the inference the entire
   scope rests on, never tested in the negative.
2. **The exposure list is a lower bound (§4)** — the transitive case defeats the
   grep method and I did not close it. There may be more than 12.
3. **The layer-3 scope caveat (§5)** — I asserted that keying on the meteor
   descriptor separates the call sites, **without enumerating the callers of
   `GetDisasterWarningTime`**. If another caller passes the same descriptor, my
   proposed wrapper changes gameplay as a side effect of a save-safety fix, which
   FIX_POLICY §4 bars. This is a specific, checkable claim and I did not check it.
4. **Layer 3 is untested in game.** The whole "vanilla's own body produces the
   right schedule" argument is read from source.
5. **`ClassesBuilt` / `ModsReloaded`** were SOURCE-only when I proposed them for
   F87, and I said so at the time.
6. **The autosave path (§5, layer 1)** is source-only.
7. **`Fix_ShelterReflex` compliance is an argument, not a measurement**, and by
   my own reasoning cannot be made one.

## 8. What this session got wrong before catching itself

Included because a reviewer should weight my reliability, and because each was
caught by a control rather than by reasoning.

- **`debug.getinfo`** — proposed as the decisive read. It is absent in the mod
  sandbox, which `ENGINE_FACTS.md:69` already recorded and the Test Kit logs on
  every boot. I should have read the facts file.
- **`Wakeup(Meteors)`** — proposed to shorten an in-flight `Sleep`. It only wakes
  `WaitWakeup` sleepers (`thread.lua:62-71`). Killed by its own positive control
  before it could produce a false pass.
- **The 192 "orphan closures"** — I reported a `rawget` sweep finding as possible
  residue. It is vanilla: `RequiresMaintenance.lua:94` flattens
  `GetPriorityForRequest` onto every instance that does not require maintenance.
  My follow-up "discriminator" then false-positived on all 192 as well.
- **F87's trigger, twice.** I blamed mod load order (wrong), then a mid-*session*
  enable (wrong). The owner's correction settled it: the mod is ticked at the
  main menu, and since a mod is never auto-enabled, that is **every player's
  first run** — which raised the severity rather than lowering it.

Four errors, all corrected the same session, three of them by running a control
and one by the owner pushing back. That is the pattern I would weight this
document by.
