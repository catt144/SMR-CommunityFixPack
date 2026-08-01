# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

**Completed tests live in [PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md)** — 40
sections as of 2026-07-30. This file carries **only un-run work**: when a test
completes, its whole section moves to the archive and is **deleted from here,
with no stub or pointer left behind** (see the reporting protocol). The archive
is the notes-and-documentation half; this file is the live work list.
(Cross-checked against the archive and the BUGS.md index 2026-07-29 — nothing
below re-tests anything already passed.)

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

## PT-00 — ⛔ The stale-probe gate (BEFORE every sitting; HARD RULE, owner, 2026-08-01)

Before the game is even launched for a test — attended or unattended — the
assisting session runs:

```
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

**CLEAN** = zero hits, or every hit is a probe this sitting's test design
explicitly declares. Not clean → delete the stale probe (+ its metadata/items
lines), commit, re-run the sweep — or the sitting does not test. **No result
from this checklist may be recorded without the sweep having run first**; the
`PROBE SWEEP:` line goes in the result commit (see the reporting protocol).
Rationale + full rule: `WORKFLOW.md` "Probe hygiene" — stale probes contaminate
both the measurement and the log it is read from, and are how false facts got
recorded before.

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
4. `SMRFixPack.ListFixes` output at load: **all 68 default fixes should read
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

## ~~PT-52 Trigger A — drone overhaul passive watch~~ ⛔ FROZEN 2026-07-31

**Do not run this. Do not enable D06 to run it.** See the drone freeze below.

Historical short form, kept only so the archived results stay readable: watch
who answers wrench icons near idle drones; `SMRFixPack.DroneReport` every
~30 min; healthy = `vetoed` climbing, `veto_expired` low, `unclaimed` not
building up.

---

# ⛔ DRONE PLAYTEST FREEZE — owner decision, 2026-07-31

**No drone playtesting of any kind until a final drone plan is in place.**

**Why.** Drones are the one part of this pack that has been iterated
piece-by-piece, and the testing has followed the same pattern: *"they keep
getting new playtests, and every time I get one half done we have another."*
Half-finished tests of superseded designs are worse than no tests — they cost a
sitting and produce evidence about a thing that is being replaced.

**What is frozen — everything that tests D06's DESIGN:**

- **PT-52 Trigger A** — passive watch (above).
- **PT-52 Triggers B and B2** — the controlled A/B and the stress re-run (§2).

These are pending **invalidation and rewrite**. `Opt_DroneOverhaul`'s claim gate
is expected to be dropped or demoted by the rebuild, which would make every
result they produce evidence about code that no longer exists.

**What is NOT frozen — these test shipped BUG FIXES, not the overhaul:**

- **PT-10** (F55, open-roof drone observation) — that is dome entrance/entity
  data, untouched by any dispatch redesign. Run it normally.
- **F77 `Fix_ExtenderFlapChurn`'s own behaviour.** The defect is real and the
  fix ships default-on. Its check currently rides along inside PT-52, which is
  why it is caught in the freeze — but F77 is *not* invalidated, only its
  test's packaging. It gets folded into the consolidated PT below.

**What happens when the plan lands.** If `docs/archive/DRONE_RESEARCH_BRIEF.md` answers
its four questions and a rebuild design is approved:

1. The frozen PT-52 sections are **archived as deprecated-by-redesign** —
   deleted from this checklist per the archived-sections-are-deleted-outright
   rule, with the reason recorded in `PLAYTEST_ARCHIVE.md`. They are not
   "un-run"; they are obsolete.
2. **ONE multi-step drone playtest replaces all of them.** Not a family of PTs.
   One item, numbered steps, run start to finish in a single sitting, covering
   the whole overhaul as one product — which is also how the module ships
   (**one toggle, all or nothing**; D09's dials stay separate).

**Until then:** if a drone anomaly shows up organically mid-sitting, it is still
worth capturing — file it on the D06 entry or as a new F-number. Observing is
not playtesting. Just do not go looking, and do not start a scheduled drone
test.

---

# 2 · In progress — owed halves of partially-passed tests

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

## ⛔ ~~PT-52 — Drone dispatch overhaul~~ — FROZEN 2026-07-31, PENDING INVALIDATION

> **Do not run any part of this section.** Owner decision 2026-07-31: no drone
> playtesting until a final drone plan is in place — full reasoning in the
> **DRONE PLAYTEST FREEZE** banner in §1 above.
>
> This section tests **D06's design**, and that design is being rebuilt. The
> claim gate it exercises is expected to be dropped or demoted, which would make
> every result here evidence about code that no longer exists. When the rebuild
> lands, this section is **archived as deprecated-by-redesign** and replaced by
> **one multi-step drone playtest**, not by a new family of them.
>
> Kept below unchanged, for two reasons only: the B2 protocol is the instrument
> the rebuild's own verification will be derived from, and the CAN/CANNOT lists
> record what was learned about judging this module. **Reference material, not a
> to-do.**

### Historical section — covers **D06 `Opt_DroneOverhaul` core v1 + F77 `Fix_ExtenderFlapChurn`** (built 2026-07-28)

**This is NOT a 15-minute test.** It is a watch-and-judge item that runs in the
background of the WHOLE session (and future sessions) while other PT items are
played, plus one controlled A/B demonstration. Expect multiple iterations —
tuning knobs live at the top of `Code/Opt_DroneOverhaul.lua` (changes need a
relaunch); record every knob change and its observed effect on the D06 entry.

> ⚠️ **RECORD THE COMMANDER PROFILE, and be careful with `Inventor`**
> (added 2026-07-30). The **Inventor** profile
> (`Data/CommanderProfilePreset.lua:152-186`) does two things that bear on this
> test, neither of which is interference with our modules — see the D06 entry
> for the collision analysis — but both of which affect what you can *measure*:
> 1. **Three `Effect_ModifyLabelOverTime` ramps on the `Consts` label** —
>    `DroneConstructAmount` +1%, `DroneBuildingRepairAmount` +1%,
>    `DroneGatherResourceWorkTime` −1%, each **every 2 sols × 50 repetitions**,
>    i.e. drifting until Sol 100. **Repair throughput on an Inventor colony is
>    not constant over time.** The B2 protocol is safe *because* it reloads the
>    same quicksave between legs, putting both legs at the same sol — but any
>    comparison of runs taken at **different sols** on such a save is invalid.
>    Never compare a stress run to one from an earlier sitting.
> 2. **It grants `AutonomousHubs`**, which sets `disable_electricity_consumption`
>    and `disable_maintenance` on both the `DroneHub` and `DroneHubExtender`
>    labels. That removes the two commonest causes of an extender's working-flag
>    flapping, so **F77's trigger should be rare or absent on an Inventor save**
>    — a quiet F77 half there is NOT evidence the fix does nothing. (Inference
>    from the effect data, not yet observed; run the F77 half on a
>    non-Inventor save if you want it to mean anything.)

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
  (docs/reports/DRONE_OVERHAUL_OPTIONS.md), not a bug in this one.
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

> **SCOPE CUT 2026-07-31 (owner decision on the sanitizer, + assistant
> pushback).** The sanitizer is **not a launch gate** and its repair half ships
> as-specced-but-unproven — see the honest wording in `MOD_DESCRIPTION.md`.
> **Cases B and C are PARKED** (`FUTURE_IDEAS.md` entry 4): case C needs a
> donated community save that may never arrive, and case B needs a
> deliberately-broken fixture built with the pack disabled.
> **⚠️ Case A stays IN, and it is the only part that was ever about risk.**
> These two passes run **automatically on every load for every player**, and the
> F03 pass **removes** label modifiers from persisted colony state. Case A is
> the do-no-harm check on that, it needs **no fixture at all** (any healthy
> save), and it takes about five minutes. Parking it would mean shipping
> auto-running save-writing code with no live observation — which is the one
> shape this project has repeatedly learned not to trust on source reasoning
> alone. Both passes ARE probe-covered (`SaveSanitizerTurbineBuff`,
> `SaveSanitizerUpgradeLeak`), so this is cheap insurance on top, not a
> substitute for missing coverage.

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

**~~Trigger — case B (F03 sweep, forced)~~ — PARKED 2026-07-31, do not run:**
4. Follow the archived PT-02 procedure to build + upgrade + salvage a Medical
   Center **with the fix pack disabled**, so a bonus really leaks. Save.
5. Re-enable the pack and load that save. The dome's birth-comfort bonus should
   drop back to its unbuffed value, and the log should carry
   `SaveSanitizer: removed N leaked upgrade modifier(s)`.

**~~Trigger — case C (F35, needs a donated community save)~~ — PARKED 2026-07-31:**
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

> ⚠️ **NEW MANDATORY STEP 5, added 2026-07-31 — "it does not break" is NO LONGER
> A SUFFICIENT PASS.** A mod-authored closure stored on a persisted game object
> was **measured** going into a save, surviving the mod's removal, and still
> being *called* afterwards (ENGINE_FACTS; drone Q1/Q2 sitting — the read
> returned `function: 000001E95D57A6B0` with the module uninstalled, and it
> re-filed queue entries using the vanished mod's logic, with **zero errors in
> the log**). A silent, error-free session therefore does **not** prove the pack
> left nothing behind.
>
> **Step 5 — hunt for surviving pack code, with the pack DISABLED:**
> - **`Fix_MeteorFrequency` is the specific suspect** and the reason this step
>   exists. It assigns our function to `GlobalGameTimeThreadFuncs.Meteors`
>   (`Code/Fix_MeteorFrequency.lua:70`), game-time threads persist **with their
>   blocked stacks** (ENGINE_FACTS), and the pack's own load line
>   (`MeteorFrequency: persisted Meteors thread on load was alive — restarting
>   with the fixed body`) proves that thread survives a save. If our body is in
>   the save, it runs after uninstall in a world with **no `SMRFixPack` global**,
>   so every `SMRFixPack.MeteorsBeatSet(...)` call inside it would index nil.
>   Read, with the pack disabled:
>   `*r ConsolePrint("Meteors body: " .. tostring(GlobalGameTimeThreadFuncs and GlobalGameTimeThreadFuncs.Meteors))`
>   then let **a meteor cycle pass** (35-115h) and re-check the log for
>   `attempt to index a nil value` naming `SMRFixPack`.
> - **`rawget` spot-checks on objects the pack touches** — a function where
>   vanilla has none is residue.
> - ⚠️ **This is an INFERENCE, not a measured defect.** The closure-persistence
>   mechanism is proven; that it applies to `GlobalGameTimeThreadFuncs` is not.
>   **Either result is a real finding** — if the body does NOT survive, record
>   that too, because it bounds the hazard to instance members only.
>
> Cleared by this step, from a 2026-07-31 audit of every `= function` site in
> `Code/`: `Fix_GraphConsumedCaption` (`panel.caption`) and
> `Fix_MoraleComfortTooltip` (`win.GetRolloverText`) write to **XWindows**, which
> are not savegame-persisted; `Opt_ResidencyControl` (`self.OnActivate` /
> `OnAltActivate` / the `ProcessToggle` rawset) is likewise a UI section; and
> `Fix_StorageRateModifiers` writes to a **class table**, restored as a permanent
> by name rather than serialised as instance data. **`Fix_MeteorFrequency` is the
> only unresolved one.**

`Result (steps 1-4):` **PASS 2026-07-31** — `PT-20TEST` (cut from the 288-sol
`test 2i`, saved at sol 290) loaded and played normally with the pack gone. No
missing-class/missing-function errors on load, colony fully functional, drones
observed operating normally (they resumed work the moment construction was
ordered). The save is not corrupted and is not held hostage.

`Result (step 5 — surviving pack code):` 🛑 **FAIL 2026-07-31 — SURVIVING PACK
CODE MEASURED AT TWO SITES. Filed as `BUGS.md` F86 (P1, blocks release).**
`Fix_MeteorFrequency.lua(106)` errored on a nil `SMRFixPack` with **our injected
locals still in its frame** (`spawn_time 60000`), killing the `Meteors` thread —
that colony gets no further meteors, and it does not self-heal.
`Opt_DroneOverhaul.lua(190)` threw 98 times in one short session via drone
command threads (`CommandObject.lua:246` → `sprocall`), **with its own opt-in
toggle OFF**. Harm there is log-only (line 188 runs vanilla's `Idle` first).

> **PROCEDURE CORRECTIONS EARNED BY RUNNING THIS TEST — read before the next run.**
> - **Step 2's "disable in the Mod Manager" is now MEASURED equivalent to a real
>   uninstall** for this hazard. Both were run against the same save file: 98 vs
>   98 `Opt_DroneOverhaul` errors, the same single `Fix_MeteorFrequency` error
>   with the same locals. The only difference is the engine's own wording
>   (`present, but not loaded` → `not present`). Either method is valid; say
>   which one you used.
> - **The suggested `GlobalGameTimeThreadFuncs.Meteors` read is NOT decisive** —
>   that table is rebuilt from vanilla at load, so it reads clean whether or not
>   the body leaked. Do not treat a clean read as a pass.
> - **`debug.getinfo` is unavailable** (mod sandbox — ENGINE_FACTS, and it is why
>   the `[install]` probes SKIP). No introspection reads.
> - **`Wakeup(Meteors)` does NOT shorten a `Sleep`** — it only wakes
>   `WaitWakeup` sleepers (`thread.lua:62-71`). Do not plan around it.
> - **What DID work, and is the recommended method:** compress the next roll
>   (`local d = GetMeteorsDescr() d.spawntime = 60000 d.spawntime_random = 0`)
>   then `RestartGlobalGameTimeThread("Meteors")`, confirm the phase advances to
>   `long-sleep-done`, pause, save. The wake is then bounded to ~2 game hours, so
>   a null result is interpretable instead of "maybe it hasn't woken yet".
> - **Take a positive control with the pack ON before saving.** It is what caught
>   the dead `Wakeup` approach before it could produce a false pass.
> - **The `rawget` spot-check needs a discriminator, not a presence test.**
>   `rawget(b, "GetPriorityForRequest")` returns a function on **192** buildings
>   in a healthy vanilla colony — `RequiresMaintenance.lua:94` flattens it onto
>   every instance that does not require maintenance. Comparing against the class
>   value false-positived on all 192 too. Presence proves nothing here.

## PT-21 — Long-save soak

**Setup:** any healthy colony (SAVE-A or the live colony is fine). All **68
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

# 6 · Needs-eyes list — settling observations from the reachability audit

**Added 2026-07-30.** These are not full PTs. Each is a **single observation**
that settles a verdict currently believed on source-shaped evidence — the exact
kind of evidence F49(c) proved can lie. Source is decisive about whether a code
path can execute and **near-mute about whether what it does is wrong**; every
row below turns on runtime or interface behaviour the Lua does not carry
(hit-testing, affordances, cursor and confirmation feedback, engine placement,
visual outcome).

**None of these is currently believed wrong.** Treat them as cheap
opportunistic riders — if you are already in a save that qualifies, take the
observation and record it. Full reasoning per row is in
`REACHABILITY_AUDIT.md` §3 (Challenge review 2026-07-30).

| Fix | The one observation that settles it |
|---|---|
| **F16** | Finish a Mirror Sphere excavation, open the finished site's infopanel, click "Pierce the Shell" — do drones engage a dead request? (overlaps PT-30) |
| **F38** | Destroy a tunnel, save/load **in vanilla**, order a colonist or rover across — does the route still use the ruin? (overlaps PT-25) |
| **F34(d)** | Drop a landscape mark over a rocket actively loading drones — is a mid-"Embark" drone visibly yanked, or does it recover silently? |
| **F74** | **In vanilla**, order an RC Transport onto a landed storybit trade rocket — does the original harm actually occur? PT-39 proved the fix refuses; nobody has ever observed the vanilla damage it prevents |
| **F53(a)** | **In vanilla**, land a passenger rocket flush against a Universal Depot — do arrivals actually strand? (overlaps PT-18) |
| **F06** | Reach the Mystery 10 finale and ignore the corner notification for one sol at speed — does the Epilogue really arrive minimized and unpaused? |
| **F26** | Watch one Last War volley with the fix off and one with it on — is the spread visible? (this IS PT-47's first result line) |
| **F22** | Open the Last Transmission faction goals panel in a young politics-enabled colony — where is the corrupted number player-visible before the Martian Assembly stage? (overlaps PT-42) |
| **F77** | Flap an extender during hub activity, with and without — how big is the fleet Idle-kick? (this IS PT-52 Trigger B's F77 half) |
| **F11** | Crew-gather a busy train's passenger, then inspect `train.units` — the U-tier settling read |
| **F81b** | On a vanilla save, catch a blocked `RainsDisasterThreads` activation after a collision; or under the fix, rain resuming within ~7 sols (overlaps PT-54 Trigger E) |

**Added 2026-07-30 late by the popup audit (`POPUP_CONSEQUENCE_AUDIT.md` §8 —
full reasoning there; these four settle ITS verdicts):**

| Subject | The one observation that settles it |
|---|---|
| **Audit keystone (storybits/sequences safe)** | `ForceActivateStoryBit("<popup-carrying bit>", MainMap)` (not immediate) → save with the corner notification up → load → `IsValidThread(g_StoryBitActive[1] and g_StoryBitActive[1].run_thread)` should print **true** → click the notification → the popup must open, and answering it must apply the outcome (~5 min, console) |
| **F83 second site** | After declining/losing a `ReconCenterDiscoveryAsteroid` popup, is the paid Detailed Scan reachable anywhere else (planetary view)? Needs a Recon Center holding ≥ `g_Consts.DiscoveryScanCost` Electronics for `CanPerformDetailedScan()` |
| **F85 (U tier)** | Rebind Quick Save to **F9**, open any choice popup (a launch-issue prompt is cheapest), press it — does a save land, and does loading it void the choice? |
| **§3.6 corner (optional)** | With the distress-call popup left open, does the sol-change autosave fire under it? |

**Six of the eleven ride along on PTs already in this file** (F16→PT-30,
F38→PT-25, F53(a)→PT-18, F26→PT-47, F22→PT-42, F77→PT-52B, F81b→PT-54E) — take
them while you are there rather than scheduling anything. The genuinely new
ones are **F34(d)**, **F74** and **F06**, plus **F11**'s console read.

**Two of these are "does the vanilla harm exist at all" checks** (F74, F53(a)),
and they need the pack **disabled** to be meaningful. ~~Bundle them into the next
PT-20 uninstall-safety sitting~~ — **that bundling is RETIRED as of 2026-07-31,
and the reason is F86.** They were attempted in the PT-20 leg and dropped
unrun: a save whose colony has ever been played with the pack installed carries
pack code on its persisted thread stacks, so **turning the pack off does not
produce a vanilla control.** These two rows need a colony that has **never** had
the pack installed — a fresh ten-minute save is enough for both, and it is the
only true negative control the project has. Do not record a reading for them
taken on a pack-lineage save.

`Results (record per fix, with the date):` _____________________________________________

---
## Reporting protocol

**⛔ Gate on the whole protocol (owner, 2026-08-01): no result below is valid
unless PT-00's stale-probe sweep ran BEFORE the sitting.** Every commit that
records a result carries its `PROBE SWEEP: clean` (or `armed: <files>,
declared by <test>`) line. A result recorded without it gets re-verified
before anything builds on it — treat it as unrecorded.

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
   ⛔ **DELETE the section outright — do NOT leave a ~~struck-through~~ stub,
   summary or "moved to the archive" pointer behind** (owner instruction,
   2026-07-30). This file is the live work list and nothing else; the archive is
   where the notes and documentation live. Any fact worth carrying forward from
   a completed test goes on its **BUGS.md entry** or into the archived section —
   never a residue line here. The same applies to §6 needs-eyes rows once they
   are settled.
