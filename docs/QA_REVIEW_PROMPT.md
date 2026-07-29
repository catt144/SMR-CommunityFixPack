# ONE-OFF QA REVIEW PROMPT — adversarial review of the 2026-07-29 session

**Paste everything below into a FRESH session (any model — Opus or Fable).**
This is a one-off. Delete it once its verdict has been folded into the docs.

---

You are doing an **adversarial QA review** of a heavy investigation-and-design
session on the Surviving Mars: Relaunched "Community Fix Pack"
(`C:\Dev\SMR-BugFixPack`). Everything below was produced in one long live
session. Some of it was proven live, some is static analysis, some is design
that has never been built. **Your job is to find what is wrong with it, not to
agree with it.**

You have a fresh context. That is the point — the session that produced this had
strong momentum and confirmation pressure, and at least two confident claims were
later disproved by test. Assume more are wrong.

## Your mission, in order

1. **Verify or refute every load-bearing claim below** against the game source
   (`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, read-only,
   NEVER modify). Cite `file:line`. Say plainly which claims you could not
   verify.
2. **Hunt hidden dangers** in the proposed fixes — especially save-safety,
   concurrency, and "this worked in the test but the test was unrepresentative".
3. **Propose better approaches** where you see them. You are not required to
   accept the shape we chose.
4. **Deliver a finalized plan or a set of options** with a clear recommendation
   and an explicit build order.
5. **On the user's go-ahead, implement it.**

## How to work

- **Read first:** `docs/BUGS.md` entries F78, F81, F82, D06, D08 (D08 lives in
  `docs/DRONE_OVERHAUL_OPTIONS.md`); `docs/FIX_POLICY.md` (binding);
  `docs/STATUS.md` "Key technical facts"; `docs/PLAYTEST_CHECKLIST.md` ground
  rules + verified command table.
- **Check the game is not running** (`tasklist` for `Mars.exe`) before touching
  loadable code. Edits to loaded Lua do nothing until relaunch.
- **There is a measurement instrument you can ask for, and it has never been
  run.** `C:\Dev\SMR-BugFixPack-TestKit\Code\91_Stress.lua` (local-only repo,
  built 2026-07-29) breaks a deterministic seeded set of buildings and records
  which hub's drone answered each repair and how long each leg took — see the
  stress-harness table in `docs/PLAYTEST_CHECKLIST.md`. **Its A/B has not been
  executed**, so several D08 open questions (queue bloat, polling cost, whether
  the claim gate measurably changes closest-hub service) are currently
  speculation that this tool could settle. If your review would benefit from
  real numbers, say so — the user can run it.
- Do NOT trust this document's claims. It is a summary written by the session
  that made the mistakes.

## THE META-DANGER — read this before evaluating anything

**All static analysis in this project is done against `ModTools\Src`, but the
game executes `Packs\Lua.fpk`, which is NOT identical.** This was proven live
this session: `CheatMeteors` calls `GetCameraLookAtPassable()` at
`Lua\Cheats.lua:63` in Src, and that global **does not exist at runtime** — the
console returns `attempt to call a nil value`. The shipped `CheatMeteors` is a
different function from the one in Src.

Every conclusion below derived purely from Src reading is therefore provisional,
and every fix needs an **apply-time self-check against the shipped shape** that
returns a reason string rather than patching blind (FIX_POLICY §2). Please
actively look for other places where our Src-based reasoning may not match the
shipping build.

---

# TRACK A — the disaster findings

## Claim A1 (PROVEN LIVE): a stranded prediction flag gates the entire weather system

`g_DisastersPredicted` (`MapSettings.lua:131`, a GameVar) had a stale
`DisasterMeteorStorm = true` entry on the user's 194-sol save with no storm
running and nothing on screen. `IsDisasterPredicted()` (`:189`) therefore
returned truthy forever, which:

- makes `RainsDisasterActivation` (`TerraformingDisasters.lua:277`) early-return
  every time, so no rain ever starts;
- makes the dust-storm and cold-wave schedulers spin forever, because both loops
  gate on `IsDisasterPredicted()` and their helpers push `wait_time` forward by
  the elapsed delta on each poll (`DustStorm.lua:439-446,464-465`;
  `ColdWave.lua:208-215,228-229`).

**Live proof:** `RemoveDisasterNotifications("DisasterMeteorStorm", MainMap)` →
`predicted entries: 0` → **rain began immediately** (`CloudSeeding POI starts
normal rain`), and a "Toxic rain — starts in 3 Sols" warning followed. A
marsquake also fired shortly after.

**QA it:** is the flag really the only gate? Is there any other consumer of
`g_DisastersPredicted` we missed? Are there other disaster types (mysteries,
`g_MysteryDream`, dust devils) affected or not?

## Claim A2 (grep-verified, NOT live-verified): the leak is unconditional

A tree-wide grep found only three removals of `DisasterMeteorStorm`:
`Meteors.lua:227` (only in the `g_MeteorStormStop` break branch),
`Meteors.lua:344` (the *warning* clear, before the disaster runs), and
`TerraformingDisasters.lua:27` (terraforming past the 80% Atmosphere threshold).

**The normal completion path — `Meteors.lua:242-251` — never removes it.** It
plays the end FX, sends `MeteorStormEnded`, clears `g_MeteorStorm`, and leaves
the flag set. The notification's own `expiration` makes it vanish from the UI
while the flag persists, which is exactly the observed state.

**If true, every meteor storm on every map with storms enabled permanently kills
that colony's cold waves and rains** — wedged or clean. This is the single
highest-impact claim in the session. **Verify it hard.** Check the shipped fpk
possibility. Check whether any `OnMsg` handler, notification-expiry path, or
`ReplaceNotification` behaviour clears the flag indirectly.

## Claim A3 (REPRODUCED LIVE): the storm thread wedges in an unbounded drain loop

Driven with taps on `MeteorsDisaster`/`SpawnMeteor`/`PlayStart|EndMeteorStormFX`:

```
ENTER MeteorsDisaster type=storm
spawned 25 / spawned 50 / StartFX after 73 spawns
(no EXIT)     g_MeteorStorm=true stop=false
validate #10 n=2 … #410 n=2      DisasterMeteorStorm = true
```

The stall is `Meteors.lua:238-241`:
```lua
while not g_MeteorStormStop and #spawned > 0 do
    WaitMsg("MeteorDone", delta)      -- delta = 3000
    table.validate(spawned)
end
```
`table.validate` works (73 descriptors fell to 2) but **two meteors never become
invalid**, so `#spawned` never reaches 0. Cause of the two survivors is
**unknown** (candidates: fall thread died, MDS interception, off-map impact).
Controls: `CheatMeteors("single")` printed ENTER *and* EXIT; the spawn loop
terminated normally at 73.

## Claim A4 (OBSERVED LIVE, not yet in a fix design): TWO storms wedged at once

`g_MeteorStormStop = true` released one thread (`EndFX`) while `validate n=2`
kept climbing; a `*g` loop pulsing the flag ten times released a second
(`EndFX` + `EXIT`), after which validate traffic stopped entirely. So a
user-triggered storm and a natural scheduled storm were **both wedged
simultaneously**, and `g_MeteorStormStop` is a **single global shared by
concurrent invocations** — `Meteors.lua:242` resets it to `false` right after
the loop, so the first thread to wake consumes the signal.

**This is a real hazard for any fix**: a bounded drain loop must be bounded
**per invocation**, not via a shared global, and the fix must assume concurrent
storms are possible. Please check whether the vanilla design ever intended
concurrent storms, and what else keys off `g_MeteorStorm` / `g_MeteorStormStop`.

## Claim A5 (DISPROVED — recorded so it is not re-derived)

We predicted that a save/load inside a disaster **warning window** would strand
the flag, reasoning from `SavegameFixups.DisasterNotifications`
(`MapSettings.lua:179-187`) and its comment that RainDisaster and MeteorStorm
"cannot be restored". **Tested and false:** a quicksave+reload inside a 3-sol
toxic-rain warning came back with the notification still on screen and still
counting down. `SavegameFixups.*` is a **one-time legacy migration** for saves
older than the revision that added it, not routine load behaviour. Game-time
threads persist, so the activation thread resumes and clears the flag normally.

**Lesson to carry:** do not treat `SavegameFixups` comments as descriptions of
normal save/load semantics.

## Claim A6 (context, verified): sensor towers widen every window

`GetDisasterWarningTime()` = `Min(base + 12h × towers, 75h)`
(`MapSettings.lua:94-97`, `_GameConst.lua:125-126`). The user's 6 towers pin it
at the 75h cap — a 3-sol warning window, corroborated by the observed "Toxic
rain — starts in 3 Sols". Dust storms were separately confirmed **designed-off**
at their terraforming level (`GetDustStormDescr()` nil, in-game panel: "Dust
storms end 50%" vs Atmosphere 57.4%), so that half of the original report needs
no bug.

## Proposed fixes for Track A — tear these apart

1. **Replace the global `MeteorsDisaster`** (full replacement, F12/F22
   precedent) with: (a) a **per-invocation bounded** drain loop, and
   (b) `RemoveDisasterNotifications("DisasterMeteorStorm", map)` guaranteed on
   every exit path. The existing tail already `DoneObject`s survivors.
2. **One-shot `OnMsg.LoadGame` reconciliation** clearing any
   `g_DisastersPredicted[id]` with no live notification behind it — this is what
   heals the saves already poisoned.
3. **Bounded `WaitMsg` in `RainsDisasterLoop`** (`TerraformingDisasters.lua:310-316`),
   which today blocks forever if activation early-returns. Note: `UpdateRainsThreads`
   (`:412`) *reuses* a wedged-but-`IsValidThread` activation thread, so terraform
   changes never rescue it.

**Specific dangers we want you to probe:**

- **How do you tell a stranded flag from a legitimate one** in fix #2? Clearing a
  genuine warning would make a disaster fire with **no warning** — arguably worse
  than the bug. Is there a reliable "is this notification live" test?
- Does removing the notification on completion break any UI or storybit that
  expects it (`MeteorStormEnded` maps to a storybit trigger,
  `MarsStoryBits.lua:31`)?
- Does bounding the drain loop cause `DoneObject` on meteors still visually
  falling? Any artifact, or a crash on a meteor mid-`Fall`?
- Concurrency (Claim A4) — is a per-invocation bound actually achievable given
  the shared globals?
- Is a **less invasive** option available than replacing `MeteorsDisaster`
  wholesale? A watchdog on the notification (the F02 precedent) may be safer than
  a full-body copy that rots on every game patch.

---

# TRACK B — the D08 drone design

**Read `docs/DRONE_OVERHAUL_OPTIONS.md` § D08 in full.** It contains the verified
fact table, five proposed layers, a risk table, and five open questions. Summary
of what most needs challenge:

- **The leash argument** — `Drone:RestrictArea(const.DroneRestrictRadius, ...)`
  (`Drone.lua:227-231`) means jobs cannot be relayed and the candidate set must
  be geometric, not topological. Is that right? Is `IsRestrictingDroneWorkRadius()`
  ever false, and what happens then?
- **Layer 1 (dispatcher)** — register extender-covered requesters to every hub in
  legal reach instead of only the uplink. Claimed near-zero save risk because all
  references are to vanilla hub objects. **Open question we did NOT resolve: is
  `command_centers` persisted or rebuilt on load?** Also unassessed: queue-size
  and polling cost on a 9-hub / 437-building colony; the dome early-return path
  (`_TaskRequest.lua:266-271`); `auto_connect` and `ConstructionSite`
  special-casing.
- **Layer 3 (adjustable radius)** — the only layer with save residue (modifiers
  persist on the object). Combined 85-hex coverage is inside the 100-hex travel
  cap but 70% past the engine's own 50 ceiling.
- **Layer 4 (Command Center tab + drone-count advisory)** — claimed zero save
  risk. Advisory derives from `CalcLapTime()` and the game's own load thresholds.
  Is the `target ≈ current × (current_lap / target_lap)` heuristic defensible, or
  will it mislead?
- **Layer 5 (a new building)** — the only layer with real save risk; gated on a
  PT-20 uninstall test. Is our read of the uninstall failure mode right?

---

# What to deliver

1. **A verdict table** — every claim above marked CONFIRMED / REFUTED / UNPROVEN,
   with `file:line` evidence.
2. **Hidden dangers found**, ranked by severity, each with the scenario that
   triggers it.
3. **Better alternatives** where you have them — including "don't build this".
4. **A finalized plan**: what to build, in what order, with what self-checks,
   what probes, and what playtest gates. Or a small set of options with a
   recommendation if a real decision remains.
5. **Explicitly list what you could not verify** and what would be needed to.

Then **stop and report to the user.** Implement only on their go-ahead.

## Binding constraints

- `docs/FIX_POLICY.md` governs all code: least-invasive technique that works;
  apply-time self-check returning a reason string; respect `SMRFixPack_Disabled`;
  no new persisted state unless unavoidable; never break a save for someone who
  later removes the mod.
- STATUS.md "Key technical facts" are hard-won — read them, do not re-derive.
  Especially: mod code loads before classes are built; runtime patches must
  target the **leaf** class; `error()`/`assert()` report and continue rather than
  unwinding; post-wrappers on command methods never run.
- Fix-pack code changes owe a fresh A/B probe pair (harness notes in
  `docs/FABLE_NEXT_PROMPT.md`). TestKit-only changes do not.
- No live UI-internals prototyping during a play session (F76 hard-lock lesson).
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  push the fix pack; the TestKit stays local-only.
