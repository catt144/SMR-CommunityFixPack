# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

**Completed tests live in [PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md)** — done so far
(36 sections): PT-01 … PT-09, PT-11 … PT-14, PT-16, PT-17, PT-19, PT-23, PT-24,
PT-26, PT-29, PT-31 … PT-34, PT-36, PT-38 … PT-41, PT-43, PT-45, PT-46 (the
F49(b) half), PT-49, PT-50, PT-51, PT-55. This file carries **only un-run work**; when a test
completes, its whole section (with the result notes) moves to the archive.
(Cross-checked against the archive and the BUGS.md index 2026-07-29 — nothing
below re-tests anything already passed; PT-46's remaining halves are exactly
the two the archived run left "not separately exercised".)

## What a pass here means

The automated A/B probe runs (docs/archive/SESSION_LOG.md) prove the *wiring* across all waves:
patched functions install and return the right values under synthetic input.
This checklist is the **human-eyes half** — the things probes cannot see:

- how it *feels* in real play (cadence, pacing, does the colony actually recover),
- **visuals** (does the trimmed track leave a sane-looking remainder?),
- **UI** (does the number actually render in the panel?),
- **long-running behavior** (does it still hold after 3 sols, after a save/load?),
- emergent multi-system interactions the probes stub out.

**A pass here is what earns a fix `tested` status in BUGS.md.** Probe-verified ≠
tested. Nothing ships as "verified" on probe evidence alone. If a sitting starts
oddly, `SMRTest.RunAll` is the quick regression sanity check (expect the same
PASS/SKIP pattern as the last A/B leg; `[install]` probes SKIP on retail).

---

**All reference material lives in [PLAYTEST_HELP.md](PLAYTEST_HELP.md)** —
ground rules, the external-validity rule, cheat discipline, console facts,
the verified command table, Test Kit helpers + the stress harness, and the
save-fixture recipes. This file carries ONLY the tests and the reporting
protocol.

---

# 1 · Standing watches — every sitting, alongside whatever else you play

## PT-22 — Log hygiene (after EVERY session, including every test below)

**Where:** `%AppData%\Surviving Mars Relaunched\logs` — take the newest
`Mars.exe-<date>-<time>.log`.

**Check for:**
1. Any line containing **`[CommunityFixPack]`** with the word `error`, `inactive`, or a
   deactivation reason. (Startup lines reporting fixes as `applied` are normal;
   the opt-in modules reporting `inactive (…opt-in…)` is normal unless you
   enabled them.)
2. Any **`[LUA ERROR]`** block whose stack mentions a file under `SMR-BugFixPack\Code\`.
3. Any `[LUA ERROR]` in shipped game code that you did **not** see in a vanilla session
   — note the file:line even if it looks unrelated to us.
4. `SMRFixPack.ListFixes` output at load: **all 69 default fixes should read
   `active`** (plus whichever opt-in modules you have toggled ON). Any other
   `inactive`/`error` line means a fix silently self-deactivated (its apply()
   self-check failed) — that is a FAIL and needs reporting with the reason string.

Paste anything suspicious verbatim into your result line — the exact text matters more
than a summary.

`Result:` _____________________________________________

## Meteor watchdog (F02) — passive, no action needed

PT-01 passed and is archived, but its silence-watch continues in the background:
the watchdog self-reports (`WATCHDOG — Meteors thread silent …`) if the meteor
wedge ever recurs. **If you see that line in the log, report it verbatim.**

## PT-52 Trigger A — drone overhaul passive watch (whenever D06 is enabled)

Runs in the background of any sitting with the module ON — full procedure and
result lines live in the PT-52 section (§2 below). Short form: watch who
answers wrench icons near idle drones; `SMRFixPack.DroneReport` every ~30 min;
healthy = `vetoed` climbing, `veto_expired` low, `unclaimed` not building up.

---

# 2 · In progress — owed halves of partially-passed tests

## PT-56 — Drone stat dials · covers **D09 `Opt_DroneStatDials`** (built 2026-07-29)

Two Mod Options dropdowns: **Drone speed** (1x base / 2x / 3x / 5x, percent
added on BASE, additive with speed techs) and **Drone carry capacity**
(+0 base / +1 / +2 on `g_Consts.DroneResourceCarryAmount`). One sitting,
any healthy save with at least one drone (~5 min):

1. **Baseline reads:** select a drone —
   `SelectedObj:GetMoveSpeed()` and `g_Consts.DroneResourceCarryAmount`
   (with both speed techs expect 2304 = 1440 × 1.6; carry 2 with Artificial
   Muscles).
2. **Set speed 2x + carry +1 → Apply** (no relaunch): same reads — speed
   gains +1440 (100% of base, additive: 2304 → 3744 on the techs save),
   carry +1; drones visibly faster; log clean (PT-22 rules).
3. **Back to base → Apply:** both reads return to the step-1 numbers —
   live removal, no residue (`SMRFixPack.ListFixes()` still shows
   `DroneStatDials [active]` — active-at-base is the armed state, by design).
4. **Stale-save reconcile:** save with dials ON, set dials to base, reload
   that save → reads are the step-1 numbers (the persisted modifiers were
   removed on load).

PASS flips D09 to `tested` (both BUGS.md places). (The C-side clamp probe
originally queued here was run ahead of the build, 2026-07-29 live: no clamp —
`SetMoveSpeed(10000)` read back exactly — and movement stayed clean at 10000
on ultra. Recorded on the D09 entry; no need to repeat it.)

`Result:` _____________________________________________

## PT-53 — Cohort housing · covers **D07 `Opt_CohortHousing`** (built 2026-07-28)

Colonist/housing-level rule, NO dome designation: a Senior or Child living in
normal housing moves into a free Retirement Home / Nursery slot — own dome
first, any reachable dome second — and is left completely alone when no slot
exists. The moves ride the shipped machinery (residence reassignment +
emigration), so everything observable is ordinary game behavior.

**Progress (2026-07-29, first live enable — user verdict: "it worked
wonderfully").** Triggers **B, C and D PASS** (cross-dome moves over trains/
passages/shuttles chosen by distance; organic no-churn where no slots existed;
graduation drain with the designed transient-homeless blip). Full record on the
D07 entry. **Only A and E remain:**

**Trigger A — in-dome move + employed exemption:** find (or spawn) an
unemployed Senior housed in a normal residence in a dome that also has a free
Retirement Home slot.
- **EXPECTED:** within a heavy update they re-home to the Retirement Home
  (watch the Residence line of their infopanel). An EMPLOYED Senior in the
  same dome does NOT move.

**Trigger E — precedence + uninstall shape:** manually assign a Senior to a
normal residence (player order) — they must STAY. Toggle the module off —
everything is instantly vanilla; save with it ON, reload with it OFF —
clean load, no errors (zero persisted state).

Reference (already-passed scope, for context only — do not re-run): the module
never touches Tourists or employed Seniors; player orders, quarantine and the
D03 closed policy always win; arrival housing at the destination may take one
heavy update to slot into the cohort building (transient, by design).

`Result (A in-dome move + employed exemption):` **PASS — 2026-07-30**, run as a
controlled A/B on one save rather than two observations. The tester granted
**Forever Young** (`g_SeniorsCanWork`, `Colonist.lua:1461-1462`) so the seniors
took jobs, then enabled the module mid-session: **employed seniors did NOT
move** — the designed exemption (`IsValid(colonist.workplace)`,
`Opt_CohortHousing.lua:87-94`, whose header names Forever Young explicitly).
Reloading the pre-tech quicksave left the same seniors **unemployed**, and over
1-2 sols they **re-homed into the Retirement Home**. One save, one variable
(employment), both halves of the trigger in a single controlled run.
**Module status confirmed `active` at the time of the employed observation** —
the tester ran that check (not screenshotted); without it the negative half
would have been uninformative, since "did not move" is equally consistent with
"module never engaged".

`Result (E precedence + uninstall):` _____________________________________________

---

## PT-52 — Drone dispatch overhaul · covers **D06 `Opt_DroneOverhaul` core v1 + F77 `Fix_ExtenderFlapChurn`** (built 2026-07-28)

**This is NOT a 15-minute test.** It is a watch-and-judge item that runs in the
background of the WHOLE session (and future sessions) while other PT items are
played, plus one controlled A/B demonstration. Expect multiple iterations —
tuning knobs live at the top of `Code/Opt_DroneOverhaul.lua` (changes need a
relaunch); record every knob change and its observed effect on the D06 entry.

**What the module CAN do (judge it on these):**
- Repair and cleaning jobs in OVERLAPPING hub coverage go to the CLOSEST hub's
  fleet first; a far fleet only serves if the near one doesn't respond within
  a few of its polls (~10-15s worst case, by the strike cap).
- Idle drones help a NEIGHBORING hub that is saturated (zero idle drones of
  its own) with repair/clean jobs within 30 hexes of the drone.
- `SMRFixPack.DroneReport()` (console, works even with the toggle OFF): per-hub
  working/drones/idle/broken, lap load class, per-priority queue depths, work +
  unclaimed counts, extender chains, and the module counters
  `vetoed / veto_expired / moonlighted`.
- F77 (default-on fix, separate from the toggle): an extender power flicker /
  malfunction / repair no longer tears down and rebuilds the whole uplink
  hub's registration twice — one coalesced rebuild ~2s later instead. Fleet
  drones no longer ALL kick to Idle on every extender blip.

**What it CANNOT do (do not judge it on these — all deliberate v1 scope):**
- Resource HAULING (PickUp/Deliver, incl. the maintenance "fetch Electronics
  from a depot" leg) is untouched — a far drone can still win a delivery.
  If the delivery leg dominates the pain, that is the H-v2/B iteration
  (docs/DRONE_OVERHAUL_OPTIONS.md), not a bug in this one.
- Construction work is untouched (multi-fleet swarming on a site is wanted).
- RC rover fleets, rockets, shuttles: untouched by design.
- It does not MOVE drones between hubs (that is option C, the migration
  balancer) — a chronically under-drone'd hub still needs the player (or a
  future iteration) to rebalance; the module only redirects CLAIMS and lets
  idle neighbors help nearby.
- It cannot override or delay a PLAYER-ordered drone command (structurally —
  the claim gate sits on FindTask, which only the auto-Idle path calls).
- Toggling it OFF restores vanilla behavior instantly and completely
  (registration untouched, no persisted state; saves made with it ON load
  identically without it).

**Setup:** a colony with ≥2 Drone Hubs with overlapping coverage (the user's
live colony is ideal — it has the original symptom), extenders present, work
happening. Enable **Options → Mod Options → "Drone dispatch overhaul
(experimental)"**. `SMRFixPack.ListFixes` must show `DroneOverhaul [active]`
and `ExtenderFlapChurn [active]`. Run `SMRFixPack.DroneReport` once as the
session baseline (counters start at 0).

**Trigger A — passive watch (all session, while playing other PT items):**
1. Whenever a wrench/malfunction icon appears near parked idle drones, watch
   who answers. **EXPECTED:** the nearby fleet claims within seconds. Vanilla
   (the 2026-07-27 screenshots) was: near drones stay Idle, far fleet crawls
   over.
2. `SMRFixPack.DroneReport` at every suspicious moment and every ~30 min.
   **HEALTHY:** `vetoed` climbing while `veto_expired` stays LOW relative to
   it (near fleets actually take the yielded work); `moonlighted` > 0 if any
   hub saturates; `unclaimed` per hub not building up.
   **UNHEALTHY:** `veto_expired` ≈ `vetoed` (strike window too short or near
   fleets can't respond — raise STRIKES_MAX/STRIKE_TTL or investigate why the
   near fleet is dead); any hub's `unclaimed` growing over consecutive
   reports (possible starvation — capture DroneReport + the R1/R2 reads from
   the BUGS DroneControl bullet on the starving building IMMEDIATELY, then
   toggle the module off and watch whether vanilla clears it).
3. **BROKEN looks like:** wrench icons lingering LONGER than vanilla; drones
   ping-ponging between two jobs or two hubs; a far fleet fully idle while
   visible work exists beyond the near fleet's capacity; any log error
   mentioning `FindTask`, `Idle`, `UpdateUplinkRequesters`, or
   `[CommunityFixPack]`.

**Trigger B — controlled A/B demonstration (10 min, once per iteration) — UN-RUN:**
1. Pick (or build) hub A and hub B far apart, with an extender bridging B's
   coverage into A's yard. Both hubs need idle drones.
2. Toggle the module OFF. `Platform.cheats = true`, select a building in A's
   yard, `SelectedObj:CheatMalfunction()`. Watch which fleet answers and how
   long the wrench lasts. (This reproduces the vanilla far-capture when the
   race falls that way — it may take a few tries; the R6 claim tap from the
   BUGS bullet prints the claiming drone's hub if eyes aren't enough.)
3. Repair, toggle the module ON, repeat on the same building.
   **EXPECTED:** A's fleet answers every time; `vetoed` ticks up if B's fleet
   polled first and was held.
4. Extender flap check (F77): toggle the extender off and on (or let a dust
   storm brown it out). **EXPECTED:** B's drones do NOT all flash to Idle;
   coverage through the extender resumes within ~2-3s of the flap settling.
   **BROKEN looks like:** fleet-wide Idle flash on each flap edge (the fix
   isn't engaging) or extender coverage permanently lost after a flap
   (debounce dropped a rebuild — capture the log).

**Trigger B2 — the MEASURED stress A/B (the real verdict; ~30 min per pair) —
RE-RUN OWED with the v2 harness.**
Supersedes Trigger B's eyeball demo. Uses `SMRTest.Stress` (Test Kit helpers +
stress-harness reference in PLAYTEST_HELP.md — **v2 lifecycle tracing, rebuilt
2026-07-29**). Run at
**normal to 3× speed, not ultra**: timings are measured in game time so speed
does not change the numbers, but ultra stresses the sim and adds artifacts.

1. Confirm the harness loaded — `SMRTest.Stress ~= nil` must print `true`.
2. Clean the colony so both legs start identical (clears any pre-existing
   malfunctions that would skew the target pool and add background repair
   traffic): `SMRTest.Stress.HealAll()`
3. **QUICKSAVE.** This one save is the anchor for BOTH legs.
4. Dry run — see the target set without breaking anything:
   `SMRTest.Stress.Targets{scope = "overlap", n = 25}`
   If it reports far fewer than 25 eligible, widen the scope (`hub`, `radius`,
   `all`) and note which you used. **Also check the pure cohort:**
   `SMRTest.Stress.Targets{scope = "overlap", n = 25, pure_only = true}` —
   no-resource targets skip the haul leg and the deliverer handoff entirely,
   so they are the purest gate signal; if there are ≥10, run a pure pair too.
5. Toggle D06 **OFF** (Options → Mod Options). Verify:
   `SMRFixPack.fixes.DroneOverhaul.status` → must read `inactive`.
6. **LEG A:** `SMRTest.Stress.Break{scope = "overlap", n = 25, seed = 1}`
   Let it run to `RUN ENDED` — it prints its own summary. `HealAll()` aborts.
7. **Reload the quicksave** — identical colony state, identical target set.
8. Toggle D06 **ON**. Verify `SMRFixPack.fixes.DroneOverhaul.status` → `active`.
9. **LEG B:** the *exact same call* as step 6 — same scope, same n, same seed.
10. `SMRTest.Stress.Compare()` — both runs + deltas, with conditions headers.
11. `FlushLogFile()` and keep the log: the per-building trail is the evidence.
12. **One pair is not a verdict at n=25** — repeat with `seed = 2` and
    `seed = 3` before believing any delta; the harness keeps 6 runs
    (`Compare{a=, b=}` to pair them up).

**STAT-DIAL legs (drone overhaul ships with Mod Options stat dials):** same
protocol, but the ONE variable flipped between legs is a single dial (e.g.
speed 1.0x vs 1.5x, module state identical). Stamp each leg:
`Break{scope="overlap", n=25, seed=1, label="speed1.5x"}`. The conditions
header live-reads drone move_speed/carry, so the dial's actual effect is
recorded with the numbers; `Compare()` flags condition mismatches itself.

**Read the result on the `GATE-DECIDED first claims` line** — closest-hub
share over FindTask-decided claims is the only number that scores what the
claim gate claims to do. The lifecycle deltas (`haul queue` vs `haul exec` vs
`claim wait` vs `travel`) are what settle the D06/D08 structural question:
queue-latency dominance points at dispatch/priority logic, travel dominance at
stat/depot levers. Do NOT read total clearance time as a D06 score.
A reload-based protocol does **not** re-poison a save with a stranded disaster
flag — tested 2026-07-29, F81 — so no cleanup is owed afterwards.

`Result (B2 stress A/B — closest-hub % off vs on):` **FIRST RUN 2026-07-29 — NULL RESULT for the claim gate (v1 harness).** 32% (8/25) off vs 40% (10/25) on = +2 buildings, inside noise at n=25. The leg the gate actually arbitrates (work→first claim) moved 58m → 57m, and `vetoed` was +1 for the WHOLE leg — the module intervened once across 25 simultaneous malfunctions. The 34m total-time gain sits in the hauling leg, which D06 exempts by design, so it is variance not treatment. **Why: `no-resource subset: 0 of 25` — every target needed a maintenance resource, so `MaintenanceDroneUnload` → `StartWorkPhase(drone)` gave the first repair tick to the DELIVERING drone every time, bypassing `FindTask`. The metric measured which hub delivered, not which won a claim.** Full analysis + caveats on the D06 entry. Both legs normal speed, storages equalised, log kept. *SUPERSEDED NOTE (2026-07-29, harness repair session): the numbers stand as recorded, but two Src facts on the D06 entry change their reading — `SetCommandKeepQueue` preempts immediately, so the ~57m work→claim CANNOT have been the deliverer handoff; and shuttle deliveries MISFIRE the handoff (no `CargoShuttle:Work`), so shuttle-hauled repairs DID go through FindTask. A B2 re-run with the v2 lifecycle harness is owed; record its result on the line below.*

`Result (B2 re-run, v2 harness — closest-hub % off vs on):` _____________________________________________

**Trigger C — regression watch (shared machinery; spread across the session):**
- Rockets: drones still load/unload landed rockets normally (F50 territory —
  rockets are class-exempt from the claim gate, verify by watching one cargo
  cycle).
- Rovers: an RC Commander's drones behave vanilla (exempt).
- Construction: multiple fleets still swarm a construction site (work type
  exempt).
- A dome with in-dome maintenance: repairs still happen (dome-inherited
  registrations defer to vanilla in the closest-hub computation).
- PT-20-style uninstall shape at session end: save with the toggle ON, flip
  it OFF (or disable the pack), reload — everything vanilla, no errors.

**Progress (2026-07-28, first sitting):** module enabled LATE in the session
via Mod Options — **the first-ever live enable of D06, bridge VERIFIED**
(`SMRFixPack.fixes.DroneOverhaul.status` → `active` right after the toggle;
boot log correctly showed `inactive` from before the flip). First DroneReport
(6 hubs, screenshot on file): `unclaimed=0` on every hub, counters
`vetoed=4 / veto_expired=0 / moonlighted=0` — the healthy signature (all four
vetoed claims picked up by the near fleet inside the strike window);
`moonlighted=0` consistent with the one saturated hub (1078: 24 drones,
0 idle) having no unclaimed work for neighbors to take.
**Second reading (same sitting, ~end of the lander leg):** `vetoed=10 /
veto_expired=1 / moonlighted=0` — vetoed climbing with expiries staying low
(9 of 10 yielded claims taken by the near fleet inside the strike window =
the healthy signature holding); `unclaimed=0` on all six hubs throughout;
hub 1078 recovered from saturated to 7 idle. No starvation indicators all
sitting.
**Sitting 2 (2026-07-28 evening): healthy again.** Readings `vetoed 1→9 /
veto_expired 0→1 / moonlighted 0`, `unclaimed=0` on all SEVEN hubs (new hub
4230 integrated cleanly); counters correctly survived a save reload
(process memory) and correctly reset on the mid-session relaunch. Full
session log swept clean. **Trigger B still un-run.**
**Sitting 3 (2026-07-29): healthy under a real stress event.** DroneReport
taken deliberately right after a **marsquake damaged several buildings** —
the closest thing to an unplanned mass-repair test so far. **NINE hubs**
(1078, 1457, 2074, 2608, 3564, 4230, 4967, 6619, 4078 — three more than
sitting 2, all integrated cleanly), `unclaimed=0` on EVERY hub with work
counts up to 120, every lap class `low`, counters
`vetoed=3 / veto_expired=0 / moonlighted=0`. Reads as the healthy signature
under load: all three yielded claims taken by the near fleet inside the
strike window, zero expiries, and `moonlighted=0` is CORRECT here rather
than suspicious — moonlighting only fires for a neighbour hub with ZERO
idle drones, and every hub in this report has idle drones (lowest 4/6).

`Result (near fleet claims near work?):` _____________________________________________

`Result (counters healthy? vetoed/expired/moonlighted):` _____________________________________________

`Result (A/B demo, which fleet answered off vs on?):` _____________________________________________

`Result (F77 flap: no fleet Idle-flash?):` _____________________________________________

`Result (regressions: rockets/rovers/construction clean?):` _____________________________________________

`Knob changes made + effect:` _____________________________________________

---

## PT-46 tail — train cap + instant-track palette · covers **F49(d), F49(a)**

The main half — splitting a track under a running train, F49(b) — PASSed
2026-07-25/26 and is archived (resolved as no-defect: the engine stores the
train back as a prefab). The archived run explicitly left these two small
checks "not separately exercised":

**Steps:**
1. `print(MainCity.labels.TrackBase[1].max_vehicles)` on a track before and after
   you salvage most of it away. **EXPECTED:** the number drops (1 for a track under
   30 hexes, 0 for an empty one). Confirm you can still assign trains up to that
   number and no further.
2. Look at any track placed instantly by the map (not built by drones): it should be
   the same colour as track you built yourself, not pipe-coloured.

`Result (d — cap follows length):` _____________________________________________

`Result (a — instant track colour):` _____________________________________________

---

# 3 · Wave-6 disaster fixes (built 2026-07-29 post-QA) — live colony

## PT-54 — Disaster prediction leak, storm wedge, rains deadlock · covers **F78 `Fix_MeteorStormWedge`, F81 `Fix_DisasterPredictionLeak` + `Fix_RainsDeadlock`**

These three ship together and share machinery, so one PT covers them. The
wave-6 probes (`SMRTest.DisasterPredictionLeak()`, `SMRTest.MeteorStormWedge()`,
`SMRTest.RainsDeadlock()` — the rains one needs a loaded colony) assert the
mechanisms; this PT is the live half. The flag dump used throughout:
`*r for k, v in pairs(g_DisastersPredicted) do ConsolePrint(tostring(k) .. " = " .. tostring(v)) end`
(an empty print = no flags set).

**Setup:** the live 194-sol save (or any save with meteor storms enabled).
`SMRFixPack.ListFixes` must show `DisasterPredictionLeak`, `MeteorStormWedge`
and `RainsDeadlock` all `active`.

**Trigger A — reconciliation heals a stranded flag.** Hand-plant one
(`g_DisastersPredicted["DisasterMeteorStorm"] = true`, nothing on screen),
quicksave, reload.
   - **EXPECTED:** a `DisasterPredictionLeak: cleared stranded prediction flag`
     log line on load; the flag dump is clean.
   - **SURPRISE looks like:** the flag survives the reload (sweep did not run —
     check fix status first).

**Trigger B — a genuine warning is NEVER cleared.** Wait for (or reach) any
disaster warning countdown (toxic rain works — 3-sol window with 6 towers),
quicksave mid-countdown, reload.
   - **EXPECTED:** the notification is still on screen still counting AND its
     flag still reads `true` in the dump. The sweep must keep it.
   - **SURPRISE looks like:** flag cleared while the countdown is visible —
     that is a FAIL of the sweep's liveness test; report immediately.

**Trigger C — the wedge heals itself.** Drive a storm:
`*r local d = Presets.MapSettings.Meteor["Meteor_High"] local p = GetRandomPassable(MainMap) CreateGameTimeThread(function() MeteorsDisaster(d, "storm", p) end)`
Let it run to its wedge (validate-style stall after the last strikes; the
duration notification eventually expires). While the storm is HEALTHY
(notification visible), `SMRFixPack.StormWedgeCheck` must read
`storm notification live (healthy)` — the watchdog must never touch a live
storm. After the notification expires with the wedge in place:
   - **EXPECTED:** within ~2 game hours, `MeteorStormWedge: WEDGE confirmed …
     healing`, then either `released through the vanilla end path` (plus
     Fix_DisasterPredictionLeak's `storm ended` line) or `forced storm state
     clean`; the flag dump is clean afterwards; `g_MeteorStorm` reads false.
   - **SURPRISE looks like:** `StormWedgeCheck` stuck on `signature armed`
     forever, repeated heals (`restarts` climbing to give-up), or a healthy
     storm getting cut short.

**Trigger D — storms keep scheduling after a heal.** After Trigger C, confirm
the scheduler is alive: `IsValidThread(MeteorStorm)` reads true, and over a
long soak a NATURAL storm warning eventually appears (the pre-fix failure mode
was: never again).

**Trigger E — rains survive collisions.** On load expect
`RainsDeadlock: … rain loop moved onto the bounded body` lines IF the save had
live rain loops (zero lines is normal when the bands had no loops — e.g. after
the manual 2026-07-29 recovery). Over the soak: rain must occur again within a
few sols of a rain roll colliding with a warning window (pre-fix: that rain
type died permanently). Cheap forced check: while any warning countdown is up,
rains rolling during it must NOT kill later rains — watch for normal/toxic rain
in the sols after the warning resolves.

Log hygiene: no `[LUA ERROR]` mentioning `DisasterPredictionLeak`,
`MeteorStormWedge`, `RainsDeadlock`, `RainsDisasterLoop` or `StormWedgeHeal`.

`Result (A reconcile / B warning kept):` _____________________________________________

`Result (C heal / D reschedule / E rains):` _____________________________________________

---

# 4 · Fixture sittings — batch these by save

## SAVE-A sitting (sandbox; PT-27/28 need the Dust In The Wind rule)

### PT-10 — Open-roof drone observation · covers **F55** ❓ **OPEN QUESTION**

**This test has no expected answer.** The Lua half of F55 (the unreachable-forever
approach cache) is fixed and probe-verified. The *other* half — whether opening a
dome's roof destroys the dome-entrance attaches that carry the only drone pathfinding
tunnels into the dome — is **engine entity data we cannot read from Lua**
(`Lua/Buildings/Dome.lua:404`; see the F55 entry in BUGS.md). **Either answer is
useful data.** Record what you actually see.

**Setup:** SAVE-A, one dome with **interior buildings that need maintenance** and a
drone hub with drones parked outside the dome.

**Trigger:**
```
CheatOpenAllDomes()
```
(this also maxes terraforming and activates the Open Domes policy — the prerequisites;
`Lua/Cheats.lua:414-424`). Then let 1–2 sols pass at ultra speed and watch drones.

**Observe and write down:**
1. Do drones **physically enter** the open dome to service interior buildings? (Yes / No)
2. Do interior buildings accumulate **unserviced maintenance** while drones idle outside?
3. Do drones **cluster in a clump just outside** the dome entrance?
4. Now `CloseAllDomes(MainCity)` — do drones resume entering? Does the situation recover
   on its own, or only after a save/load?

- **If drones enter and maintain normally:** the entity-data concern is unfounded → F55
  can be closed as fixed on the Lua half alone.
- **If drones stay outside forever:** we have a confirmed engine-data bug and a new
  finding to file.

`Result (1):` __________  `Result (2):` __________  `Result (3):` __________  `Result (4):` __________

`Notes:` _____________________________________________

### PT-27 — Dust Sickness does not infect Biorobots · covers **F40**

**Setup:** SAVE-A (with the **Dust In The Wind** rule). You need **Biorobots**
and a **dust storm**. Biorobots come from the **The Positronic Brain**
breakthrough — `UIColony:SetTechResearched("ThePositronicBrain")` (NOT
`CheatResearchAll()`, which skips undiscovered breakthroughs — see the command
table in PLAYTEST_HELP.md), then spawn a batch and check the colonist list for the **Biorobot**
trait; if you cannot get any, write "could not set up" and skip the F40 half.

**Trigger:**
1. Note which colonists are Biorobots.
2. Wait for (or wait out) a **dust storm** with the "Dust Sickness" event active.
3. When the Dust Sickness event resolves, list who caught it.

- **BROKEN looks like:** Biorobots appear in the list of the newly sick, lose Health
  in every subsequent storm, and (on the "shouldn't work" answer) are flagged unable
  to work until the cure tech lands.
- **FIXED looks like:** only organic colonists catch it. Children are still excluded
  as before.
- **Existing-save check:** load a save where Biorobots are already sick and look for
  `[CommunityFixPack] DustSicknessBiorobots: cleared Dust Sickness from N Biorobot(s)`
  in the log; those colonists should lose the trait and the "unable to work" flag.

`Result (Biorobots spared?):` _____________________________________________

### PT-28 — Dust Sickness damage spread · covers **F17**

**Setup:** SAVE-A, during an active dust storm with several colonists carrying the
**Dust Sickness** trait (see PT-27 for how to get there).

**Trigger:** pick 4-5 sick colonists, write down each one's Health, run **one sol** at
`SetGameSpeedState("ultra")`, and compare the drops. (Health also moves for other
reasons — food, medical care — so use colonists in the same dome doing the same thing,
and look at the pattern rather than exact numbers.)

- **BROKEN looks like:** every sick colonist loses **exactly the same** Health per sol
  (a flat 10) — the damage roll the code computes is discarded.
- **FIXED looks like:** the per-colonist losses **differ**, spread over 5-14.

`Result:` _____________________________________________

## SAVE-B sitting (No Disasters, underground)

### PT-25 — Destroyed tunnel after a reload · covers **F38**

**Setup:** SAVE-B (or any save with underground access — `UIColony:UnlockUnderground()`
then `CheatRevealDarkness()`). Build a **tunnel pair** across an obstacle so that the
tunnel is the *short* route between two points, and park an **RC Rover** on one side
with an errand on the other (a deposit to mine, a building to service). Watch it use
the tunnel once so you know the route.

**Trigger:**
1. Destroy the tunnel. `CheatToggleInfopanelCheats()` gives you a per-building
   **break/destroy** button in the infopanel; a meteor strike on it works too
   (`CheatMeteors("single")` with the camera on the tunnel). Confirm both ends now
   show as **destroyed ruins**.
2. Send the rover across again. It should now take the long way round (or refuse).
3. **Save, quit to menu, and load that save.** This is the step that mattered.
4. Send the rover across again and watch its path.

- **BROKEN looks like:** after the reload the rover walks straight at the ruin and
  teleports through it as if the tunnel were intact — the shortcut came back on load.
- **FIXED looks like:** the rover takes the same long route after the reload as it did
  before it. The log shows a `[CommunityFixPack] DestroyedTunnels: closed N destroyed
  tunnel(s)` line if the save already had the bad state baked in.

**Then repair it** (the ruin's Rebuild button) and confirm the tunnel **works again** —
this is the check that the fix does not lock a repaired tunnel out permanently.

`Result (still closed after reload?):` _____________________________________________

`Result (works again after repair?):` _____________________________________________

## Mystery saves

### PT-15 — Wisp power output · covers **F07** (+ **F15** bonus read)

**Setup:** SAVE-D — the **St. Elmo's Fire** mystery (`LightsMystery`) active, with
**Light Traps built and holding wisps** (`#MainCity.labels.LightTrap` > 0 and traps
with `fireflies`).

> **How to get there without third-party mods.** `CheatStartMystery` self-gates on
> `Platform.cheats` (`Lua/Cheats.lua:1-3`, `Lua/Mysteries/Mysteries.lua:91`), which is
> false on retail. Two legitimate routes, in order of preference:
> 1. **Pick the mystery at new-game setup** (recommended — this is the realistic path
>    and the one described in the SAVE-D fixture).
> 2. From the console, flip the platform flag around the call and put it back:
>    ```
>    *r Platform.cheats = true CheatStartMystery("LightsMystery") Platform.cheats = false
>    ```
>    `Platform` is **not** blacklisted, so this does work from the retail console — but
>    it is a bigger hammer than route 1. If you use it, note that in your result.

**Trigger:** with wisps in the traps, choose the **"free the wisps"** option (or from
the console `SetLightTrapMode("free")`), then read a trap's power output:
```
*r local t = MainCity.labels.LightTrap[1] ConsolePrint(tostring(#t.fireflies).." wisps -> "..tostring(t.electricity_production))
```

- **BROKEN looks like:** you free a swarm of wisps into your traps and they generate a
  laughable trickle of power — a handful of units instead of kilowatts. The reward feels
  pointless.
- **FIXED looks like:** the traps produce **~1000× more** — roughly `1000 × wisp count`
  — a real power source, matching what the mystery's text promises.

Also check `SetLightTrapMode("destroy")` on a separate trapful: the research points
granted should **match the number shown in the notification** (F15 half — record it as
a bonus observation).

`Result (power):` _____________________________________________

`Result (RP matches notification):` _____________________________________________

### PT-30 — Finished Mirror Sphere site · covers **F16**

**Setup:** a game running the **Mirror Sphere** mystery (pick it at new-game setup;
`CheatStartMystery` is gated on `Platform.cheats` — see the note under PT-15). Play or
fast-forward until you have a **scanned excavation site** with a Drone Hub in range.

**Trigger:**
1. While the site is part-way done, confirm its actions (**Pierce the Shell**,
   **Communicate**, **Feed Power**) can be started — this is the control.
2. Let the excavation run to **100%** — the sphere launches and detaches.
3. Now open the finished site's infopanel and try each action again. If you have not
   used all three, at least one should still be un-completed.

- **BROKEN looks like:** the finished site still offers and accepts actions.
  "Pierce the Shell" connects it to your drone commanders and drones start walking
  over to work an excavation that cannot progress.
- **FIXED looks like:** the finished site starts nothing. Cancelling an action that was
  already running still works.

`Result:` _____________________________________________

## SAVE-E sitting (frontier: elevator + asteroid)

### PT-18 — Arrival deaths, including the elevator / multi-map path · covers **F53**

This is the fix that was **reworked after the audit found it broken**, and the elevator
path is exactly the case that was broken. Test that path deliberately.

**Setup:** SAVE-E — an **underground dome with free housing**, reachable only via the
**Elevator**, plus a surface rocket landing pad.

**Trigger — case A (surface arrival):**
1. Bring a rocket of colonists down on the surface, some distance from any dome.
   Watch where they walk and whether any die or go "Abandoned".

**Trigger — case B (the elevator / cross-map arrival — the important one):**
2. Make the **underground dome the only one with free housing** (fill or close the
   surface domes' housing / turn their Accept Colonists off).
3. Land a rocket of new colonists on the surface.
4. Follow them: do they walk to the **Elevator**, ride it down, and reach the
   underground dome?

**Trigger — case C (nasty variant):**
5. Land a rocket where the nearest dome by straight-line distance is **not** walkable
   (across impassable terrain / a canyon) while a walkable dome exists further away.

- **BROKEN looks like:** newly arrived colonists set off toward a dome they can't
  actually reach, mill about outside, get flagged Abandoned/Confused, and die of
  suffocation — or, in the elevator case, every legitimate elevator arrival gets
  re-routed, loses its elevator assignment and is abandoned on the pad.
- **FIXED looks like:** arrivals are dropped on passable ground, elevator-destined
  colonists actually ride the elevator down and move in, and unreachable-dome arrivals
  either pick a reachable dome or wait safely near the rocket under a "Confused
  Colonists" notification and retry — **nobody dies on arrival**.

`Result (A surface):` _____________________________________________

`Result (B elevator):` _____________________________________________

`Result (C unreachable-nearest):` _____________________________________________

## Any-save items (live colony or any healthy save)

### PT-35 — Save sanitizer passes · covers **F35, F03 (sweep half)**

Both passes only act on damage that is *already* in a save, so a fresh colony
proves nothing about them beyond "they ran and broke nothing". Treat the first
two steps as the real test and the third as the only one that needs a fixture.

**Setup:** any save. The pack's passes run automatically on load; the two are also
callable by hand from the console:
`SMRFixPack.Sanitizer.RepairTurbineBuff()` and
`SMRFixPack.Sanitizer.RepairLeakedUpgradeModifiers()` — each returns how many
things it repaired.

**Trigger — case A (does no harm):**
1. Load a healthy save with at least one Large Wind Turbine and one upgraded
   Medical Center in a dome. Note the turbine's Power production and the dome's
   birth-comfort figure.
2. Run both console calls. Both should return **0** and nothing on screen should
   change.
3. Save, reload, check again — still unchanged. (Running twice must never stack a
   bonus; that is the failure this checks for.)

**Trigger — case B (F03 sweep, forced):**
4. Follow the archived PT-02 procedure to build + upgrade + salvage a Medical
   Center **with the fix pack disabled**, so a bonus really leaks. Save.
5. Re-enable the pack and load that save. The dome's birth-comfort bonus should
   drop back to its unbuffed value, and the log should carry
   `SaveSanitizer: removed N leaked upgrade modifier(s)`.

**Trigger — case C (F35, needs a fixture — skip if unavailable):**
6. A save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture. If a community save is donated, load it and
   check a Large Wind Turbine's Power production against a Shrouded one: unfixed
   the Large one is missing the +100%; fixed they match.

- ⚠️ If step 3 shows a bonus that grew on the second run, that is a FAIL and the
  pass is not idempotent — record the exact figures.

`Result (case A no-op):` _____________________________________________

`Result (case B leak cleared):` _____________________________________________

`Result (case C, or "no fixture"):` _____________________________________________

### PT-37 — F48 unblock test · decides whether the **F48** repair can ship

F48 is **not implemented** — this test is what decides whether it can be. The shipped
migration fixup (`Station.lua:1339-1355`) mis-parenthesises one call, so it re-orders
nothing; the *corrected* call runs `OrderTrackElements`, which rebuilds every element's
`connections` and `node_idx` on the track it is given, with a non-unwinding `assert` as
its only failure handling. Before that ever ships in the sanitizer, it has to be seen
behaving on a real save — both on a healthy network and on the one thing most likely to
break it: a meteor-damaged track.

**Setup:** a save with **two or more stations** connected by track, at least one route
with a running train, **and** one track broken by a meteor (trigger one via
`CheatTriggerMarsquake()` near a track, or play until one lands). Extending SAVE-A
works. Console open (Enter / Alt-Shift-C).

**Trigger — case A (healthy track):**
1. Pick an intact track and note its endpoints:
   `qa_t = MainCity.labels.TrackBase[1]`
   `print(qa_t.start_el, qa_t.end_el, #qa_t.elements)`
2. Run the CORRECTED call the F48 repair would ship:
   `ProcessTrackElements(ResolveMap(qa_t), qa_t.elements)`
   `qa_t.start_el = qa_t.elements[1]  qa_t.end_el = qa_t.elements[#qa_t.elements]`
3. Re-print the endpoints; check the route still forms, the train still runs, and
   nothing visual changed. **Save, reload, check again.**

**Trigger — case B (the damaged track — the risky one):**
4. Repeat steps 1-3 with `qa_t` set to the meteor-damaged track (pick the right
   index from `MainCity.labels.TrackBase`). Expect the console to print the
   "unable to find the expected number of track elements" assert — that is fine
   *if nothing corrupts*: after it, check the repair site is still salvageable
   (F45), the rest of the network still routes, and a **save + reload** comes back
   clean.

- **UNBLOCKS F48 looks like:** case A is a stable no-op-or-better and case B fails
  *cleanly* (assert printed, network intact after reload) → the repair ships in
  `90_SaveSanitizer.lua` behind a one-shot flag, skipping tracks that carry repair
  sites.
- **CONFIRMS THE BLOCK looks like:** case B leaves a track that will not route, a
  train stuck, or a save that reloads broken → F48 closes as
  `wontfix — repair riskier than the defect`, record exactly what broke.

`Result (case A healthy):` _____________________________________________

`Result (case B damaged):` _____________________________________________

### PT-42 — Last Transmission notices your reserves · covers **F22, F75**

Probes prove the presets are wired correctly and the reserve maths is right;
only play can show the approval actually moving and the UI goal clearing.

**Setup:** a game where **Last Transmission** is an active faction, ideally with
the Underground map opened (that is what made the old maths hopeless). Open the
faction panel and note the current approval and the listed "How to achieve"
goals.

**Steps:**
1. Look for goals like "Have Power for more than 2 sols stored", "Have Water for
   more than 2 sols stored", "Have Oxygen for more than 2 sols stored".
2. Build up **Power** storage until you comfortably hold more than 2 sols'
   worth, and let a day pass.
   - **EXPECTED:** the Power goal stops being listed as outstanding and the
     faction's approval rises; the reason appears in the approval breakdown.
   - **SURPRISE looks like:** the goal stays listed forever no matter how much
     you bank (that is the old behaviour).
3. Repeat for **Water**, then for **Oxygen**. The Oxygen one is the important
   check — it used to be satisfied by having Power stored.
   - **EXPECTED:** stocking Oxygen (and only Oxygen) clears the Oxygen goal.
4. Now drain one of them to zero — switch off or salvage the storage.
   - **EXPECTED:** the matching penalty ("No Power stored" etc.) appears and
     approval falls. Before the fix this was unreachable once a second map was
     loaded.
5. Check the log for `GridGlobalStorage: applied` and
   `LastTransmissionStorage: ... storage condition(s) made effective`.

`Result (goals clear when stocked?):` _____________________________________________

`Result (Oxygen goal needs Oxygen / penalties reachable at zero?):` _____________________________________________

### PT-44 — Founder trait notice and dome pipe cleanup · covers **F23, F24**

**F23 — Founder gains a trait.** Probes cover the wiring; play confirms the
notification renders and reads correctly.
1. Play until one of your **Founders** gains a trait (age, a story event, or the
   Gene Forging / trait-granting paths).
   - **EXPECTED:** a "Founder gains trait" notification appears, naming the
     colonist and the trait, and clicking it selects them.
   - **SURPRISE looks like:** nothing appears (the old behaviour), or two
     notifications appear for the same event.

`Result (notification appears once, names the right trait?):` _____________________________________________

**F24 — dome absorbing a pipe-connected building.** This one has no probe: it
needs a real dome and real pipes.
2. Build a life-support building **outside** a dome and connect it with pipes
   (Water Extractor, Moisture Vaporator, Water Tank, or an Oxygen tank).
3. Now build or upgrade a **dome** so that the building ends up **inside** the
   dome's footprint (the game moves it "inside" the dome's grid).
   - **EXPECTED:** the pipe stubs and connection graphics at the old boundary
     disappear cleanly; the building keeps working on the dome's grid; no
     orphaned plug graphics are left floating.
4. **Save, quit to the menu, and reload.** The repair sweep that runs on load
   exercises the same code path.
   - **EXPECTED:** still clean — no stale pipe visuals reappear, and pipes can
     still be connected in that area afterwards.
   - **SURPRISE looks like:** leftover plugs/pipe ends, or a spot where new pipe
     refuses to connect.
5. Check the log for errors mentioning `DestroyConnection` or `LifeSupportGrid`.

`Result (clean at absorption / clean after reload / pipes still connectable?):` _____________________________________________

### PT-47 — Bombardment volley shape · covers **F26**

The probe can prove the game computes a different direction per missile; only eyes
can confirm the volley looks like a scatter rather than a rank. This fix is the
pack's largest copied function (100 lines of `WaitBombard`), so the point of this
test is as much "nothing else about a bombardment broke" as it is the spread.

**Setup:** a Mystery 7 bombardment, or force one from the console:
`StartBombard(UIColony:GetCityAtMap(MainMap), 40*guim, 8, 500, 1500)`
(any valid object or point works as the first argument; 8 missiles makes the shape
obvious). Watch from a low camera angle so the incoming trails are visible.

**Trigger:**
1. Watch a volley arrive.
   - **EXPECTED:** the missiles come in from visibly different angles — a scatter,
     not a rank of parallel trails.
   - **SURPRISE looks like:** still perfectly parallel (the old behaviour).
2. Check that everything else about the volley still works, because the whole
   function was replaced:
   - impacts leave scorch decals that fade out;
   - a missile that hits a dome cracks it instead of exploding on the ground;
   - the "Incoming Missile" notification appears and clears;
   - missiles shot down by defences explode in the air;
   - the bombardment ENDS (the sequence continues afterwards) — if the volley
     never finishes, that is a FAIL and the fix should be reverted.
3. Check the log for errors mentioning `Bombardment`, `BombardMissile` or
   `WaitBombard`.

`Result (spread visible?):` _____________________________________________

`Result (decals / dome hits / notification / interception / volley ends?):` _____________________________________________

### PT-48 — Acknowledged warnings · covers **D02 `Opt_AcknowledgedWarnings`**

Dismissal now means "I've seen THESE buildings" instead of "silence the whole
category for 4 game hours". **Enable route:** Options → Mod Options →
Community Fix Pack → **Acknowledged warnings** (takes effect on Apply, no
restart); `SMRFixPack.ListFixes` must show it `active`. This is a FEATURE, not
a fix — the question is "does it behave as advertised", plus the usual
"nothing else broke".

**Setup:** break two buildings in ways that won't self-heal (e.g. turn off their
power supply, or use a permanently entombed/unsupplied building if the save has
one). Wait for the "Building Not Working" notification listing both.

**Trigger:**
1. Dismiss the notification (right-click it / its dismiss control).
   - **EXPECTED:** it goes away and STAYS away — play several game hours at high
     speed; the two acknowledged wrecks never re-nag (vanilla re-nags every 4
     game hours ≈ every few real seconds at ultra).
2. While it is quiet, break a THIRD building.
   - **EXPECTED:** a new "Building Not Working" notification appears promptly
     for the new one — no 4-hour category silence (this is the module's other
     half; vanilla would keep it quiet for the rest of the window).
   - The new notification lists only the new building, not the acknowledged two.
3. Repair one of the acknowledged buildings, let it run, then break it AGAIN.
   - **EXPECTED:** it notifies again — recovery re-arms the warning.
4. Save, reload, and confirm the still-broken acknowledged building stays quiet
   after the load (the stamp persists).
5. Other warnings (fuel, DestroyedInfrastructure, rover damage) must behave
   exactly as vanilla — dismiss one and confirm nothing odd.

`Result (acked stay quiet / new one warns / re-break warns / survives reload?):` _____________________________________________

---

# 5 · Cross-cutting — do these last, once per era of the pack

## PT-20 — Uninstall safety · covers **all fixes / FIX_POLICY §3**

The pack must never hold a save hostage.

**Steps:**
1. Play SAVE-F (or any save) **with the fix pack enabled** for a few sols; save it.
2. Quit to the main menu, open the **Mod Manager**, and **disable the Community Fix
   Pack only**. Leave the Test Kit enabled.
3. Restart the game and **load that save**.
4. Play **10 minutes** of ordinary gameplay: build something, salvage something, let a
   sol pass, save and reload once.

- **BROKEN looks like:** the save refuses to load, throws missing-class/missing-function
  errors on load, or the colony visibly misbehaves (buildings inert, colonists frozen)
  because something the pack created is now dangling.
- **FIXED looks like:** the save loads and plays completely normally — the original bugs
  come back, which is expected and fine, but nothing is corrupted or crashing.

**Then check the log** (`%AppData%\Surviving Mars Relaunched\logs`, newest
`Mars.exe-*.log`) for any error mentioning our code.

Re-enable the fix pack before continuing.

> Note for the next run: the 2026-07-29 audit flagged the wave-6 fixes as the
> newest un-cycled persisted state (`Fix_RainsDeadlock` persists its loop
> threads by global name; `SMRFixPack_fixed_loop` markers) — make sure the
> save used for this test post-dates wave 6 so the cycle covers them.

`Result:` _____________________________________________

## PT-21 — Long-save soak

**Setup:** any healthy colony (SAVE-A or the live colony is fine). All **69
default fixes** active (incl. `DroneStatDials`, active-at-base) — confirm with
`SMRFixPack.ListFixes` (opt-in modules read `inactive` unless you enabled
them).

**Steps:**
1. Play a **normal session** — 45–60 minutes of real play, no cheats, mixed speeds,
   at least one full save/reload partway through. Just play the game.
2. During play, note anything that feels off: stuck colonists, drone clusters, trains
   that don't move, notifications that flicker, unexplained deaths.
3. At the end, run the state reports:
   ```
   SMRTest.ReportReservations
   SMRTest.ReportTrains
   SMRTest.ReportBrokenTrack
   ```
4. Optionally `SMRTest.RunAll` for a regression sanity check (expect the same
   PASS/SKIP pattern as the last A/B run — the `[install]` probes SKIP on retail,
   that is normal and not a failure).
5. Quit and read the log (see PT-22).

- **BROKEN looks like:** `[CommunityFixPack]` errors in the log, stale reservation
  counts climbing over the session, train prefab counts drifting down, or engine errors
  that don't appear in a vanilla session.
- **FIXED looks like:** zero `[CommunityFixPack]` errors, `ReportReservations` reporting
  0 clearly-stale slots, `ReportBrokenTrack` reporting 0 bad `node_idx`, and no new
  engine error signatures.

`Result (gameplay feel):` _____________________________________________

`Result (ReportReservations):` __________  `(ReportTrains):` __________  `(ReportBrokenTrack):` __________

`Result (log clean?):` _____________________________________________

---
## Reporting protocol

**Tester (you):**
1. Fill in every `Result:` line — `PASS` / `FAIL` / `SKIP (reason)` — plus free-text
   notes and the **date**. Screenshots for anything visual (especially PT-10).
2. Commit this file, or simply tell the next session:
   **"read PLAYTEST_CHECKLIST.md results"**.

**Next session — do exactly this:**
1. Read this file's `Result:` lines.
2. For every fix whose covering test(s) **PASSed**, flip its status to `tested`
   in `docs/BUGS.md` — **both places**:
   - the **index row** (`| F0x | … | fixed |` → `tested`), and
   - the **detail heading tag** (`` `[fixed: Code/Fix_X.lua]` `` → `` `[tested: Code/Fix_X.lua]` ``).
   A fix covered by more than one test only goes `tested` when **all** its
   results pass. Partial fixes (marked `fixed*`) go to `tested*` and keep
   their open-half note. Behavioural/timing results also record their
   conditions per the EXTERNAL VALIDITY rule (PLAYTEST_HELP.md).
3. Move the corresponding lines in `docs/MOD_DESCRIPTION.md` into the shipping fix list
   if that file segregates tested vs untested (only `tested` fixes ship in the final
   player-facing text).
4. For every **FAIL**, do **not** flip the status. Instead:
   - record it as a **new finding** in `docs/BUGS.md` (new detail entry + index row, or
     an appended note on the existing entry if it's a regression of that same fix),
   - set the affected fix back to `todo`/`blocked` as appropriate with the tester's
     verbatim observation quoted,
   - add it to the "Next gates" line in `docs/STATUS.md`'s header.
5. For **PT-10 (F55)**, whichever way it lands, record the observation on the F55 BUGS.md
   entry and resolve the open question in STATUS.md's "Waiting on the user" item.
6. Update STATUS.md's current-state header (counts / next gates) to reflect
   the new results, and append the sitting as a new leg at the top of
   `docs/archive/SESSION_LOG.md`.
7. Commit everything in one change, with the playtest date in the message.
8. Move each completed test's section — test text plus the filled-in results —
   from this file into `docs/PLAYTEST_ARCHIVE.md`, so this checklist only
   carries un-run work. (A partially-passed test stays here with its passed
   triggers recorded, like PT-52/PT-53 above.)
