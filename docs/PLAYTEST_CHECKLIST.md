# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

**Completed tests live in [PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md)** — 44
sections as of 2026-08-01, of which one (PT-54) is **retired unrun**, not
completed. This file carries **only un-run work**: when a test
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
everything is instantly vanilla (that half is a BEHAVIOUR check and stands).
~~save with it ON, reload with it OFF — clean load, no errors (zero persisted
state)~~ → **save with it ON, then disable the Community Fix Pack in the MOD
MANAGER and load: clean load, no `[LUA ERROR]` naming pack code.**
⚠️ **METHOD CORRECTED 2026-08-01 — a toggle CANNOT answer an uninstall question.** With the module merely switched off the mod env is still present and the hooks are still installed, so any captured frame resolves `SMRFixPack`, reads inactive and no-ops: **it reads clean by construction, whether or not the module leaks.** `Opt_DroneOverhaul` leaked at 98 errors/session with its own toggle OFF — that is how F86 Site 2 was found. Use **Mod-Manager-disable** (measured equivalent to a real uninstall, PT-20: 98 vs 98 on the same save). `ENGINE_FACTS.md`, "OFF" IS THREE DIFFERENT THINGS. A clean read here bounds *that save on that path*; it is not a
general "zero persisted state" proof, and this line no longer claims one.

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

## ~~PT-54 — Disaster prediction leak, storm wedge, rains deadlock~~ ⛔ RETIRED UNRUN 2026-08-01

**Do not run this. Do not schedule a wave-6 disaster sitting for it.** Full
test text (all five triggers) preserved in
[PLAYTEST_ARCHIVE.md](PLAYTEST_ARCHIVE.md) under its RETIRED-UNRUN banner —
the trigger designs are the raw material the Tier-1 build prompt draws on.

**Why:** PT-54 tests the *current* `Fix_RainsDeadlock` body, which the F86
Tier-1 build deletes and replaces outright (`SAVE_SAFETY_REDESIGN.md` §6.2),
and the *current* `Fix_MeteorStormWedge`/`Fix_MeteorFrequency` heal sequencing,
which the same build reorders (the orphan-gate rule + the watchdog moving onto
`Msg("MeteorDone")`/`NewDay` restarting **vanilla's** body). Running it would
verify code that is about to stop existing.

**What absorbs its intent — named trigger by trigger** (project prompt chain
`4_f86_phase2_tier1_build_fable.md` §3, which states these legs *are* PT-54's
retirement made good):

| PT-54 trigger | absorbed by | ✅ RUN |
|---|---|---|
| **C** wedge heals itself | the Tier-1 **A/B pair** — it must exercise the reordered heal path, since that path is what changes | **RUN 2026-08-01, leg 1** (`Mars.exe-20260801-17.11.08`) — and better than asked: BOTH §6.2a-D completion branches ran live, the release branch on the forced storm (`0:20:28.442` → vanilla end path) and the force-clean branch on the scheduler's own natural storm (`1:56:48.368` → `8 stray meteor object(s) removed`) |
| **D** storms keep scheduling after a heal | the Tier-1 A/B pair **+ the F88 load-3×-inside-a-rolled-interval regression leg**, which is the sharper form of the same question | **RUN 2026-08-01, legs 1+2** (same log) — `IsValidThread(MeteorStorm)` true after the heal, and the natural storm that arrived later *is* the scheduler proving it; leg 2 read the sharper form, `t=216351730` → 3 loads → `t=218608231 (+2256501 ms = 75 game hours)` on the persisted deadline |
| **E** rains survive collisions | the `Fix_RainsDeadlock` rewrite's own A/B leg (incl. the migration pass and the C34 stale-ACTIVE rider) | **RUN 2026-08-01, leg 3** (same log) — the collision arrived NATURALLY (`0:20:06` re-roll posted, rain returned; a second at `1:50:10`), `'normal'` migrated + stamped 1.0.1, and the C34 stale-ACTIVE plant healed through vanilla `FinishRainProcedure` at `0:23:39` |

⚠️ **NOT absorbed, and carried forward rather than dropped: triggers A and B.**
They test `Fix_DisasterPredictionLeak` — the load-time reconciliation and its
liveness test — and no Tier-1 rewrite covers them by construction. Its wave-6
probe asserts the mechanism synthetically only. ✅ **RUN 2026-08-01 as leg 4,
in their changed shape** (`Mars.exe-20260801-17.11.08`): A(a) a planted flag
cleared on the next NewDay tick with NO reload (`0:02:24`); A(b) re-planted
with no sol tick either side, cleared inside the load block (`0:10:47`); B a
live storm countdown survived quicksave/reload with no clear line and a flag
dump of `DisasterMeteorStorm = true`, and survived a sol tick during the live
countdown too. ✅ **RESOLVED 2026-08-01
(prompt 3): both were written up as Tier-1 leg 4 (that build prompt has since
been consumed) — and the pre-cleared mid-session reconcile WAS taken**
(`SAVE_SAFETY_REDESIGN.md` §6.2a-C: an `OnMsg.NewDay` reconcile joins the
module in the Tier-1 build), **so A and B changed shape as anticipated**: A
asserts the stranded flag heals both without a reload (within a sol) and on
reload; B asserts a genuine warning survives both sweeps.

Status flips for F78/F81/F02/F88 ride the Tier-1 legs and the normal reporting
protocol (index row **and** heading tag, both).

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

## PT-58 — F86 **Tier-2** verification leg · covers **F86 Site 2, F53, F55, F21** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 5b

**One leg for the whole tier** (chain prompt 5, 2026-08-01). Tier 2 rebuilt four
modules onto synchronous seams; this is the sitting that decides whether that
worked. **Nothing in Tier 2 may be called verified, and the D10/D12 unhold may not
be recorded, until this leg's numbers are quoted.**

**⛔ PT-00 first.** Sweep result at build time (`ef7d49c`): **CLEAN — zero
`TEMPORARY` hits in both repos.** Re-run it at the keyboard anyway; that is the
rule. Both probes that asserted a replaced body (`ArrivalDeaths` drove
`FromFixPack(Colonist.Arrive)`, `DroneUnreachableForever` drove
`Drone:ApproachWrapper`) were **realigned onto the new seams** in TestKit
`7bfa274`, and `TrainWaitTime` in `6eb3c0b` — none of the three now asserts
behaviour the pack no longer replaces.

**⚠️ Turn the loggers on AFTER every restart** (`SMRTest.Log.<name>(true)`,
`SMRTest.Loggers()` lists state) — a game restart clears them, which is how Tier-1
leg 5 lost its meteor instrumentation.

### ⭐ PREDICTIONS — written 2026-08-01, BEFORE the leg runs

Record the reading against each one. A prediction that misses is the finding.

| # | prediction | what a miss means |
|---|---|---|
| **P1** | `*r SMRTest.RunAll()` with the pack ON: `DroneUnreachableForever` **PASS**, reporting the failure **normalised to roughly `now±0 ms`** (not `now + max_int`) | the consumer patch is not reaching the poisoned stamp |
| **P2** | same run: `ArrivalDeaths` **PASS**, reporting *"the impassable drop spot was snapped to a walkable one"* **and** *"Colonist.Arrive is vanilla's"* | either half (a) is not installed, or a pack body crept back onto `Arrive` |
| **P3** | same run: `TrainWaitTime` **PASS**, travel clock restarted at boarding. It **SKIPs** if run bare — use the `*r` form | the `AddSpentTime` key or the command-thread identification is wrong |
| **P4** | whole-session play with the pack ON: **zero** `[LUA ERROR]` lines naming any of `Fix_DroneUnreachableForever.lua`, `Fix_TrainWaitTime.lua`, `Fix_ArrivalDeaths.lua`, `Opt_DroneOverhaul.lua` | a wrapper is throwing on a live path a fixture cannot reach |
| **P5** | **the headline.** PT-20 method (play, park drones idle, save, disable the pack only, load): **ZERO** `Opt_DroneOverhaul.lua` orphan errors. Tier-1 leg 5 read **80** on this exact shape (`Mars.exe-20260801-19.14.11`), 98 when first measured. ⚠️ **A zero is only worth the idle-drone count behind it** — record the `DroneReport` total from step 3 alongside it, or the reading proves nothing | Site 2 is not repaired; the moonlight frame is still being captured |
| **P6** | same load: **zero** lines naming `Fix_DroneUnreachableForever.lua`, `Fix_TrainWaitTime.lua` or `Fix_ArrivalDeaths.lua` | a Tier-2 wrapper is on a blocking stack we did not account for |
| **P7** | `Fix_ArrivalDeaths`' half (b) is layer 2 — an **inert** captured `Colonist:Idle` frame may exist in the save. It must produce **no error and no behaviour**: nothing runs after `return orig_idle(...)`. `Fix_ShelterReflex` has had this exact shape through every prior leg and has never appeared in a log | an "inert" frame that is not inert — that would be a §3a finding, not a bug in this module alone |

### ⛔ Run this leg on the RETAIL build, not MarsDebug

Asked and answered at the keyboard 2026-08-01, before the run. An asserts build
would un-SKIP the `[install]` probes and let P2's second clause read — but:

- **Debug mode alone does not do it.** The mod sandbox applies on ALL builds
  including `MarsDebug.exe` (verified 2026-07-26; the "asserts build un-sandboxes
  mod code" assumption was tested and is wrong). What it un-sandboxes is the
  CONSOLE, so it also needs `SMRTest.EnableIntrospection(debug)` typed in and a
  re-run.
- **P5 is a comparison against 80, and that 80 was measured on retail.** An
  asserts build makes the `dbg()` calls inside `CommandThreadProc` itself live
  (`CommandObject.lua:208`, `:273`) — the exact loop this leg measures. Whether
  that changes what gets serialised is *unknown*, which is the reason not to find
  out on the leg that decides whether Site 2 is closed.
- **It is not needed.** P2's structural clause guards against a stale install,
  and P1/P3 already exclude that: both passed against seams that exist ONLY in
  the Tier-2 code. P6 then tests the same property live — a pack body on
  `Colonist:Arrive` would name `Fix_ArrivalDeaths.lua` in the uninstall log.

➡️ **Separate sitting worth having anyway (NOT this one):** a MarsDebug session
with `SMRTest.EnableIntrospection(debug)` clears the **eight `[install]` probes
that SKIP on every retail run** — standing coverage the project has never had.
Route it after the chain; it is TestKit coverage, not F86 work.

### Steps

1. **PT-00 sweep**, then load a save with the pack enabled. `*r SMRTest.RunAll()`
   → read P1/P2/P3 off the output.
2. Play ~15 minutes of ordinary colony: let drones work and go idle, let a rocket
   land if one is due, run a train if the save has one. Watch for P4.
3. **Park drones idle before saving** — P5 depends on drones being mid-`Idle` at
   write time; that is what made 80 frames last time. On a big colony (the
   2026-08-01 article is ~1k colonists over 6-7 domes) requests fire constantly
   and the fleet never settles on its own, so **switch the Drone Hubs OFF** for
   the last minute or two, verify, then save.
   - **Off, NOT salvage.** `Drone:Idle` gates its whole find-work block on
     `if command_center.working then` (`Drone.lua:612`), so a switched-off hub
     drops every drone straight through to `Sleep(2000)` + `CleanUnreachables()`
     (`:639-640`) — the capture site, and where the Tier-2 hook now lives. A
     salvaged/destroyed hub instead makes `command_center` invalid and sends
     drones to **`WaitingCommand`** (`:583-586`), a body the old wrapper never
     sat on: that would read zero for the wrong reason.
   - **Do not linger.** Idle drones keep draining, and at
     `battery <= DroneEmergencyPower * 2` they leave Idle for `EmergencyPower`
     (`:608`) with nothing recharging them. Off → settle → verify → save. Do not
     let a sol pass with the hubs down.
   - **Verify the precondition, do not eyeball it:** `SMRFixPack.DroneReport()`
     prints `idle=N` per hub, and that field is a literal count of drones with
     `command == "Idle"` (`DroneControl.lua:909-918`). Sum it; **record the
     total in the result** — a zero in P5 is only as strong as the number of
     capturable frames the save actually contained. Aim well above 80.
   - Hubs stay ON for step 2 — P4 needs the live drone paths exercised.
   Save.
4. Quit to menu, **disable the Community Fix Pack only** (Test Kit stays on),
   restart, load that save. **Count `Opt_DroneOverhaul` lines in the log** (P5),
   then grep the other three module names (P6/P7).
5. Play 10 minutes with the pack gone (build, salvage, a sol, save+reload once) —
   the save must behave normally, and the reload must stay at zero.
6. Re-enable the pack.

### Optional read that re-earns a status tag

**F21 was downgraded `tested` → `fixed`** when its body was retired, because
PT-43's pass measured a mechanism that no longer ships. If this sitting has a
working train line, re-take PT-43's two reads — a long platform wait producing
**no** "travel time" Comfort entry, and the train's *Travel time (rolling
average)* excluding the wait — and F21 goes back to `tested`. Skip it and F21
simply stays `fixed`; do not re-flip it on the probe alone.

`Result:` ⭐ **PASS — RUN 2026-08-01, owner at the keyboard, two sittings.**
Logs: `Mars.exe-20260801-21.27.58` (pack ON) and `Mars.exe-20260801-21.54.16`
(pack REMOVED). Lineage `save_game_id HdmSxGs6kyd0uz6-`, map
`BlankBigCanyonCMix_09` — the same save family and map as all five Tier-1 legs,
so P5's comparison is like-for-like. PT-00 sweep **clean** (zero `TEMPORARY`
hits, both repos). Article: **`T2-UNINSTALL`**, cut from `test 2i`.

**The fixture, stated first, because a zero is only worth its denominator:
73 drones in command `Idle` at save time** (`SMRFixPack.DroneReport()` summed
over eleven hubs: 20+14+9+9+7+6+5+3, with `DroneHub:1078`, `:1457`, `:8470` at
zero). Leg 5's 80 came from the same shape. The hub-off technique specced above
was **not needed** — the colony settled to 73 idle with every hub still
`w=true`. It stays on record for a save that does not.

| # | reading | verdict |
|---|---|---|
| **P1** | `DroneUnreachableForever` **PASS** — *failure normalised to now+0 ms; expires after 3600000 ms*. Vanilla's `GameTime() + max_int` poison undone exactly, and the entry then sits inside the shipped 5-sol window | ✅ **MET** |
| **P2** | `ArrivalDeaths` **PASS** — *the impassable drop spot was snapped to a walkable one*. ⚠️ **The second clause could NOT be read**: retail has no `debug.getinfo`, so `FromFixPack(Colonist.Arrive)` returned *SMRTest:no-introspection*. Not a miss — **unmeasurable in this build**, and the build question was asked and answered before the run (see the retail-build box above). P6 tests the same property live | ✅ **MET** / ⚠️ one clause unmeasurable |
| **P3** | `TrainWaitTime` **PASS** — *station keeps the 90000 wait; the travel clock restarts at boarding (0)*. The `IsKindOf(self,"Station")` key and the `command_thread == CurrentThread()` identification both work against the live class. This was the piece flagged as likeliest to be subtly wrong | ✅ **MET** |
| **P4** | **One** `[LUA ERROR]` in the ON session, with **zero pack files in its stack**: `HGE::l_GetVisualPos: Expected luaGameObject` ← `Colonist.lua(3282)` ← `ViewObjectAndChangeMap` ← `MarsNotifications.lua(265)` ← NotificationUI `CycleItems`. Fired at Lua `0:12:42`, two seconds after an `ObjCheat CheatDelete`. **Owner-attributed at the keyboard to an accidental cheat click, unrelated to the pack.** Recorded so a later reader does not find a `[LUA ERROR]` inside the Tier-2 leg log and reopen it; **not filed** — a cheat-induced dangling reference is not a player-reachable path (FIX_POLICY §4) and an uninstrumented sighting does not become a defect | ✅ **MET** |
| **P5** | ⭐ **THE HEADLINE — ZERO.** Not one `Opt_DroneOverhaul` line in the uninstalled session. **Leg 5 read 80 on this exact shape**, 98 when first measured. **F86 Site 2 is CLOSED** | ✅ **MET** |
| **P6** | **ZERO** mentions of `Fix_DroneUnreachableForever.lua`, `Fix_TrainWaitTime.lua` or `Fix_ArrivalDeaths.lua`. This is also what answers P2's unmeasurable clause: a pack body left on `Colonist:Arrive` would have named its own file here | ✅ **MET** |
| **P7** | **ZERO `[LUA ERROR]` of ANY kind**, whole session. The layer-2 residual `Fix_ArrivalDeaths` (b) leaves — an inert captured `Colonist:Idle` frame — produced no error and no behaviour, exactly as `return orig_idle(...)` with nothing after it predicts | ✅ **MET** |

**The uninstall was genuine, not a half-disable.** Zero `[CommunityFixPack]`
lines anywhere in the log, and `Unpersist missing permanent:
Mod/SMR_CommunityFixPack` fired at Lua `0:00:19` and again at `0:02:21` — the
engine reporting that the save held a reference to the pack's env and the env is
gone. **Leg 5's 80 errors landed at Lua `0:00:26`, inside that same window.** A
pack-written save was loaded **twice**, plus a save-and-reload of a pack-free
save, across 10:08 of session. All clean.

### Method note — `Opt_DroneOverhaul` was toggled ON for this leg, and that is fine

**Leg 5 ran with the module's Mod Options toggle OFF; PT-58 ran with it ON.** A
deliberate owner choice at the keyboard ("I wanted it to be as toxic as possible
before the uninstall leg"), and a **deviation from the brief that was declared,
not hidden** — which is why it could be reasoned about instead of discovered
later in a diff.

**It does not weaken the like-for-like comparison against 80, and the reason is
Site 2's own founding finding: the leak happened with the toggle OFF.** The old
post-wrapper installed at FILE SCOPE and called `orig_idle(self)` unconditionally,
so the frame entered the save whether the module was doing anything or not — the
toggle never gated persistence, only behaviour. Capturable population is set by
how many drones sit in `Idle`, which is why both legs are measured by that
number (80 then, 73 now) and not by the toggle.

**What the ON state DID buy, and it is worth having:** Part 1's
`TaskRequestHub:FindTask` wrapper does real work on every claim when active —
`closest_covering_hub`, the extender recursion, the strike counters, the caches —
and short-circuits at `module_active()` when not. So this sitting pushed the
module's busiest live path through thousands of calls and produced **zero
errors**, which is P4 evidence the toggle-off shape could not have given.
(`vetoed=0` means the veto branch never *fired*; the wrapper around it ran
constantly.)

### ⚠️ What this leg did NOT establish — recorded, not glossed

1. **No status flip is earned by it.** `F53`, `F55` and `F21` stay `fixed`. P1-P3
   are **fixture** results, not live readings: no arrival was observed being
   re-routed, no drone was observed re-trying a building it had written off, and
   the optional train re-take did not run (the sitting had no suitable line).
   The leg verified **save safety**, which is what F86 asked of it. The
   functional re-tests are still owed and belong to ordinary playtesting.
2. **The `self.command == "Idle"` moonlight gate was never exercised.** Every hub
   reported `unclaimed=0`, and the module reported `moonlighted=0 vetoed=0` —
   there was no unclaimed work anywhere for a drone to take, so the gate had no
   opportunity to fire. **P5 does not depend on it** (the frame is uncapturable
   whether the gate fires or not), but D06 part 2's *functionality* is untested
   by this leg. Its proper home is the frozen PT-52, not here — do not chase it
   from a save-safety sitting.
3. **A clean uninstall here is not a general Tier-3 clearance.** Zero errors
   means no accepted-residual module happened to be in a state that errors
   (`StormWedgeHeal` only dies at a `SMRFixPack.*` touch, i.e. mid-heal). This
   leg bounds the pack's uninstall behaviour on this save; it does not retire
   the Tier-3 residual, which stays accepted by owner decision.

## PT-60 — The chain-8b batch leg · covers **F90-F96 AND prompt 8's eight unrun conversions** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 8b

**One leg for the whole batch.** Two independent bodies of work land on it and
neither has ever executed in a game:

* **the seven approved fixes** — F90-F96, built 2026-08-02 (`a5b9db0`, `eb4c6d6`,
  `b22dda5`, `3966fb3`, `125783e`, `08b5d84`, `b5628a7`);
* **prompt 8's eight §5.4/package-0 conversions** — `69c02b9`, `26f0b57`,
  `ab7d432`, `388c72a`, `21990fb`, `1471533`, `8f58f30`. ⚠️ **These are
  technique-only changes carrying written byte-equivalence arguments, and an
  argument is not an observation.** No converted module may be called verified
  until this leg's numbers are quoted.

**⛔ PT-00 first.** Sweep result at build time (`b5628a7` + TestKit `2ef64a4`):
**CLEAN — zero `TEMPORARY` hits in both repos.** Re-run it at the keyboard
anyway; that is the rule.

**⚠️ Turn the loggers on AFTER every restart** (`SMRTest.Log.<name>(true)`) — a
restart clears them.

### ⚠️ Read this before taking any morale or production reading on this save

**F92 changes real gameplay.** Saints now actually raise Religious colonists'
morale by +10 in their dome, and the *"Blessed by a Saint"* line appears on those
colonists — behaviour the game has always advertised and never delivered. **F95
likewise adds 10% production to two extractor types** for an Astrogeologist
colony, applied at load on an existing save. Neither is a balance change, but a
morale or production A/B taken across this leg that does not account for them
will read them as drift.

### ⭐ PREDICTIONS — written 2026-08-02, BEFORE the leg runs

Record the reading against each one. **A prediction that misses is the finding.**
The counts below are derived, not inherited: 74 registered modules before this
batch, `+5` new files (F91 and F94 landed inside modules that already existed),
6 opt-in modules unchanged.

| # | prediction | what a miss means |
|---|---|---|
| **P1** | ⚠️ **CORRECTED MID-LEG 2026-08-02 — the original wording was wrong.** It predicted **`73/79`** from `metadata.lua`'s all-`false` `default_options`. **The run read `79/79`**, because **Mod Options survive a Mod Manager disable** and six opt-in modules were left on in that profile (ENGINE_FACTS). The count to predict is therefore **79 registered**, with active = 73 + however many opt-in toggles are on — **read `CurrentModOptions` or `ListFixes()` before writing the number, never the defaults.** A miss on the *registered* half still means a module failed its self-check; read the detail string first | a module failed its self-check, or the count arithmetic is wrong — either way, read the `ListFixes()` detail string before anything else |
| **P2** | `SMRFixPack.ListFixes()`: the **five new modules** — `SaintBlessing`, `DustDevilsDescrMap`, `AstrogeologistExtractors`, `SinkholeIndestructible`, `DustStormUndergroundBreaks` — all report **`active`** with an empty detail | a self-check is targeting the wrong class, or a preset pass latched |
| **P3** | same list: **all eight conversions' modules report `active`** — `SmallLandscapeSites`, `NightShiftWork`, `GeneForging`, `ShuttleHubOffAvailable`, `UpgradeModifierLeak`, `SequenceLatents` (F29 items 1+3), `DroneTransportMinors` (F57(a)) | a conversion's new self-check or `SetGlobal` read-back is failing where the old §1.5 copy did not |
| **P4** | the **seven new probes** all **PASS**: `TrackShellLeak`, `SaintBlessing`, `DustDevilsDescrMap`, `AsteroidVisitPrecedence`, `AstrogeologistExtractors`, `SinkholeIndestructible`, `DustStormBreakMapFilter`. Probe total is **85** (78 + 7) | read each failure message — every one of them names the specific mechanism it drove |
| **P5** | **no probe that passed before this batch now fails.** The two at risk are `AsteroidLanderAvailable` (F94 rewrote the body it drives) and any probe touching `Fix_TrackSalvageWipe` | F94's brackets narrowed the wrong clause, or F91's deletion reached a path it should not |
| **P6** | whole-session play with the pack ON: **zero `[LUA ERROR]` lines naming any of the five new files**, and **zero naming any of the seven converted modules' files** | this is the whole point of the leg for the conversions — a technique change that throws on a live path a fixture cannot reach |
| **P7** | **the conversions produce no visible behaviour change at all.** Night shifts, gene forging, shuttle-hub availability, landscaping sites, upgrade modifiers, sequence latents and rocket refuelling all behave as they did before `69c02b9` | a byte-equivalence argument was wrong; the module and the argument both go back to prompt 12 |
| **P8** | on a save that predates this batch, the load logs **at most one line each** from `TrackSalvageWipe` (shell heal), `SaintBlessing` (re-base) and `AstrogeologistExtractors` (bonus heal) — and a **second load of the same save logs none of them** | a heal is not idempotent, which is the one property all three were designed around |
| **P9** | `SMRFixPack_rocket_fuel_key` is **absent** from `DroneControl` after one load-and-save (`8f58f30` clears it, including from saves that already carry it) | the field-removal half of F57(a)'s conversion did not run |

**Not predicted, and deliberately so:** the exact PASS/SKIP split of the whole
suite. It moves with what the save contains (several probes SKIP without a
suitable colony) and with the retail sandbox's eight standing `[install]` SKIPs.
Quote the header line and the seven new verdicts; do not chase a total.

### What this leg does NOT cover

* **F90's live half.** The defect is a *victim distribution*, not a single
  event, so "no underground break happened this session" proves nothing. The
  honest test is the checklist rider: after a surface dust storm on an elevator
  colony, **zero new `PowerLeak`/`LifeSupportLeak` notifications on the
  underground map**. The probe covers the filter itself.
* **F93's live half.** Needs a deliberate map switch — see the rider.
* **F96 in play.** R2 needs a large meteor to land on the sinkhole's hex during
  St. Elmo's Fire. The probe asserts the flag; nobody should wait for the
  coincidence.
* **A general Tier-3 uninstall clearance.** F90 adds a wrapper on a method the
  city's hourly game-time thread calls, but the call is **synchronous with no
  yield inside it** (traced end to end on the F90 entry), so it adds no §3a
  route-(a) exposure and this leg is not a save-safety leg. If the session ends
  with an uninstall read anyway, it is a bonus observation, not the verdict.

### Steps

1. **PT-00 sweep.** Then load a save that predates this batch with the pack
   enabled — that is what makes **P8** and **P9** readable at all. Note the log
   lines from the three heals immediately.
2. `*r SMRTest.RunAll()` → read **P1, P2, P4, P5** off the output.
   `SMRFixPack.ListFixes()` → read **P3**.
3. Play ~15-20 minutes of ordinary colony. Watch for **P6** and **P7**. If the
   save has an elevator and a dust storm arrives, take the F90 rider reading.
4. Save, load the same save again, and confirm **P8**'s second half: none of the
   three heal lines reappears.
5. ⛔ **Report every unexplained log line with its age.** The logs span hours of
   ordinary play, "not caused by our leg" is an attribution verdict and not a
   dismissal, and every previous pushback on one of these lines has turned up a
   vanilla defect that was not on our list (WORKFLOW.md).

## ~~PT-61 — F97 dust-devil spawn gate~~ ✅ **RUN 2026-08-02 WITH THE OWNER — ALL TEN PREDICTIONS MET**

> **Result, in one place.** Save `d10test1`, `Atmosphere 0`, storms disabled at the
> map, natural scheduler only. Logs `Mars.exe-20260802-16.25.43` (A/B) and
> `-17.02.15` (uninstall).
> **Vanilla, 9 waves: 3, 3, 4, 3, 3, 3, 3, 4, 3 — never 0, never 6-8.**
> **F97, 20 waves: 0 ×7, 6 ×4, 7 ×7, 8 ×2 — 20/20 MATCH.**
> **P6 met twice** (waves 24 and 27 attempted 8, which vanilla cannot compute).
> **P9**: the persisted copy survived a save boundary and drove the far-side wave
> (`predicted 6..8 | ATTEMPTED 6 | MATCH`).
> **P10**: with the pack removed the colony produced **8 devils** from the
> carryover copy and the next descriptor read `gated=no (vanilla numbers)` —
> self-healed inside one wave, **zero `[LUA ERROR]`**.
> ⭐ **Two riders closed for free:** F93's live half (the underground read
> `disabled` while `MainMap` read `VeryHigh_3` — the nil branch, and the 4-hour
> cadence never broke), and the defect observed on the save's **own shipped
> preset** post-uninstall (`DustDevils_Low`, authored `1..2`, computing `0..1`).
> ⚠️ **The RATE question is NOT settled** — see the per-preset table on BUGS F97.
> **Lessons that changed the tooling mid-leg are recorded in the steps below;
> keep them — three of them would each have cost a sitting.**

## PT-61 (as written before the run) — F97 dust-devil spawn gate · covers **F97 (C23 item 1)** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 8c

**One fix, its own leg, because the item earned one.** F97 changes how many dust
devils a wave produces. It is the only item in the chain whose approval was
explicitly **provisional** (owner, 2026-08-02: *"build it … it's not locked. I
want the QA run to personally review it"*), so the leg has to produce numbers a
reviewer can argue with, not a green tick.

**⛔ PT-00 first.** Sweep result at build time (`b43f1d9` + TestKit `7733f79`):
**CLEAN — zero `TEMPORARY` hits in both repos.** Re-run it at the keyboard.

### ⛔ TWO SETUP TRAPS. Either one costs the whole sitting and both look like the fix failing.

**Trap 1 — dust devils are OFF on a terraformed colony, for reasons that have
nothing to do with this fix.** `MapSettings_DustDevils` shares the `Atmosphere` /
`DustStormStop` gate with dust storms (`TerraformingDisasters.lua:34-52`) and
`OverrideDisasterDescriptor` **returns nil** once the parameter passes the
threshold (`:69`), after which the scheduler parks in
`while not new_descr do Sleep(const.DayDuration) end`. **Check before choosing a
colony — two bare expressions, one at a time:**

```
DustStormsDisabled
GetTerraformParamPct("Atmosphere")
```

⛔⛔ **DO NOT use the `rawget(_G, "DustStormsDisabled")` form that chain prompt
8c's addendum carried — IT CANNOT WORK IN THE CONSOLE, and it was never run.**
Both `rawget` and `_G` are in `ModEnvBlacklist` (`Mod.lua:1267-1428`, verified
2026-08-02: `_G = true`, `rawget = true`, while `setmetatable`/`rawset` are
deliberately left available). The console runs inside that same sandbox
(`console.lua:27-56`), so the snippet calls a nil value. **The failure would not
have looked like a broken command — it would have looked like an answer**, and
the whole point of the check is to stop the sitting when it says `true`.
`DustStormsDisabled` is an ordinary non-blacklisted global, so a **bare read
reaches the real `_G`** and is the correct form. ⚠️ This is the same class of
mistake as the rest of the prompt-7-era detail defects: the reasoning was right
and the mechanism was wrong.

`true` means that colony **cannot produce dust devils at all**. ⛔ The campaign's
deep colony (`TEST 2H`, sol 285) is past the threshold and **cannot host this
leg** — use a young colony or a fresh sandbox.

**Trap 2 — do NOT turn dust storms off by setting `DustStormsDisabled`.** The
scheduler's own first statement each cycle is
`while HasDustStorm(map) or DustStormsDisabled do Sleep(5000) end`
(`DustDevils.lua:209`), so that flag **parks the whole scheduler** and you would
read zero devils forever and call it a regression. The rider's "dust storms off"
means *no storm occurring* — set the map's storm preset to `"disabled"` instead
(`MainMap.mapdata.MapSettings_DustStorm = "disabled"`) and confirm with
`HasDustStorm(MainMap)`. A storm arriving mid-wave also truncates the burst
(`:220-222`), which would under-count a **passed** gate specifically.

### Setup — console-produced, and disclosed as such

The shipped cadence is unusable for a leg: `DustDevils_VeryHigh_3` sleeps
`spawntime 1350000` between waves and `warning_time` again **per devil** inside
the burst, so one wave of 8 would take most of an evening. The leg therefore
**compresses the preset in the console** and records that it did.

**Paste one line at a time. The console input is ONE LINE and a `--` comment
anywhere in a `*r` snippet makes the whole chunk fail to compile.**

```
SMRTest.Log.DustDevils(true)
MainMap.mapdata.MapSettings_DustDevils = "DustDevils_VeryHigh_3"
MainMap.mapdata.MapSettings_DustStorm = "disabled"
*r local p = Presets.MapSettings.DustDevils.DustDevils_VeryHigh_3 p.spawntime = 4 * const.HourDuration p.spawntime_random = 0 p.warning_time = 1000 p.spawn_delay_min = 1000 p.spawn_delay_max = 1000
*r RestartGlobalGameTimeThread("DustDevils")
*r MainMap:MapForEach(true, "PrefabFeatureMarker", function(m) if m.FeatureType == "Dust Devils" and m.thread then DeleteThread(m.thread) m.thread = false end end)
```

**Confirm the setup took before relying on it** — and note the `print_format`
wrapper, for the reason given under the smoke test:

```
*r local p = Presets.MapSettings.DustDevils.DustDevils_VeryHigh_3 ConsolePrint(print_format(p.id, p.spawntime, p.spawntime_random, p.warning_time, p.spawn_chance, p.count_min, p.count_max))
```

⛔ **`spawn_chance 50`, `count_min 6`, `count_max 8` must be untouched** — those
three are the discriminator, and the leg proves nothing if any of them moved.

**Why each line is there, because three of them are not optional:**

* ⛔ **The restart is mandatory or the leg does not start.** The scheduler is
  already asleep inside `Sleep(Max(spawn_time - warning_time, 1000))` with the
  OLD `spawntime`, and a preset edit cannot shorten a sleep already in progress —
  the first compressed wave would otherwise be ~270 game hours away.
  `RestartGlobalGameTimeThread("DustDevils")` re-creates the thread from
  `GlobalGameTimeThreadFuncs`, which is **vanilla's body** (F97 owns no body), so
  this is not touching pack code. ⚠️ It re-rolls the pending wave timer — the F88
  cost — which is harmless *here* because we are deliberately re-timing the
  scheduler anyway, and is exactly the cost F97 avoids paying in shipped code.
* ⛔ **The marker sweep is mandatory or the count is contaminated.** The
  scheduler's opening block creates a marker thread per `PrefabFeatureMarker`
  (`DustDevils.lua:200-206`) and **assigns over `marker.thread` without deleting
  the old one**, so every restart leaves an orphan marker thread spawning devils
  on its own schedule. Marker devils spawn with a position and are
  indistinguishable from wave devils in the log. Run the sweep **after** the
  restart, and re-run it after any further restart.
* **`MapSettings_DustStorm = "disabled"`** is how storms are turned off. See
  Trap 2 — the flag is not.

### ⭐ If the save has a dust storm WARNING baked in (added 2026-08-02)

**Usable, and it is mild evidence FOR the save** — but the pending storm has to
be cancelled, and `MapSettings_DustStorm = "disabled"` does **not** cancel it.

* **A warning by itself does not block dust devils.** The scheduler gates only on
  `HasDustStorm(map)` and `DustStormsDisabled` (`:209`, `:220`); a *predicted*
  storm sets neither. Nothing is wrong with starting the leg with a warning up.
* ⛔ **But the storm it is warning about will land, and that WILL corrupt the
  reading in the direction that matters.** `OnMsg.DustStorm` → `StopDustDevils`
  wipes every devil on the map, the scheduler parks at `:209` until the storm
  ends, and a storm arriving mid-burst `break`s the loop at `:220-222`. That
  **truncates a passed gate specifically** — a wave that should have shown 6-8
  shows fewer, which reads exactly like the fix not working.
* ⛔ **The preset edit does not reach it.** `DustStormThread` holds its
  descriptor from `:417`/`:456` and `NewDustStorm:452` calls `StartDustStorm`
  unless `DustStormsDisabled`; `WaitNewDustStorm` (`:525-534`) only re-reads
  `GetDustStormDescr` **after** the storm has fired. So `"disabled"` bites on the
  *next* cycle, not this one.
* ✅ **The cancel, and it is one line** — run it in the setup block right after
  `MainMap.mapdata.MapSettings_DustStorm = "disabled"`:

```
*r RestartGlobalGameTimeThread("DustStorm")
RemoveDisasterNotifications("DisasterDustStorm", MainMap)
```

  `DustStormThread` re-reads at `:417`, gets nil because the map is now
  `"disabled"`, and **returns immediately** — the thread exits and no storm ever
  fires. The second line clears the stale warning from the UI. Both are reverted
  by a reload, so **re-run them after every load** with the rest of the setup.
  ⚠️ **This only works for a PREDICTED storm.** If one is already ACTIVE, restart
  does not stop it — use `CheatStopDisaster()` and wait for it to clear first.
* ⭐ **Why the warning is mild evidence FOR this save:** when terraforming passes
  the `DustStormStop` threshold, `OnMsg.TerraformThresholdPassed` sets
  `DustStormsDisabled = true` **and** calls
  `RemoveDisasterNotifications("DisasterDustStorm", map)`
  (`TerraformingDisasters.lua:16-22`). A **surviving** dust storm warning
  therefore means the colony is still below the threshold — which is exactly what
  Trap 1 requires. **Run the one-word check anyway**; this is corroboration, not
  a substitute.

⚠️ **After ANY reload, re-apply the two `MainMap.mapdata` lines, the storm-thread
cancel above (if it applied), the restart and
the marker sweep.** `OnMsg.LoadGame` → `ApplyDisasterSettings` rewrites
`MainMap.mapdata[disaster]` from the `g_DisastersSettings` GameVar
(`MapSettings.lua:36-60`), so the map edits do not survive a load. The **preset**
edits do survive a load (presets are session state) but not a game restart.

### ⭐ Sixty-second smoke test — do this before committing to the long leg

The repair is visible without waiting for a single wave, because the descriptor
getter is pure. Run this a dozen times:

```
*r local d = GetDustDevilsDescr() ConsolePrint(print_format(d and d.id, d and d.spawn_chance, d and d.count_min, d and d.count_max, d and d.SMRFixPack_spawn_gate))
```

⛔ **`ConsolePrint` takes exactly ONE string argument** (`LuaSharedLib.lua:7`, a
native binding). A multi-argument call **prints nothing at all and reports no
error** — found the hard way on 2026-08-02, when PT-61's own setup-confirmation
line silently produced no output and looked like a console that had stopped
responding. Wrap the values in **`print_format(...)`** (`lib.lua:95`), which is
exactly what the console's own expression rule does, or concatenate into one
string yourself. This applies to every `*r ... ConsolePrint(...)` snippet in this
document.

**Expect `DustDevils_VeryHigh_3  100  6  8  true` and
`DustDevils_VeryHigh_3  100  0  0  true` in roughly equal numbers.** With
`SMRFixPack_Disabled.DustDevilSpawnGate = true` expect
`DustDevils_VeryHigh_3  50  6  8  nil` every time.
If that does not happen, stop — the leg cannot succeed and the fault is upstream
of any timing. ⚠️ Each call consumes one `SessionRandom` draw and does **not**
touch the running scheduler (it holds its own descriptor); a dozen draws is
noise, a thousand is not.

⚠️ **This is fix verification, not reachability evidence** (FIX_POLICY §4a) — the
same standing F96's manufactured sinkhole has. The *defect* is source-verified
and R1 on shipped data; what the leg proves is that the repair does what it
claims on the live scheduler. **The edits are session-only** (presets are rebuilt
from `Data\` at Lua load) — but they are edits to a **shared preset object**, so
do not save-and-keep this save as a fixture.
⚠️ **Only `spawn_chance 50` and `count 6..8` may be left alone.** Changing either
destroys the discriminator.

### ⭐ THE A/B IS WITHIN ONE SESSION, ON ONE COLONY — use it

F97's wrapper consults `SMRFixPack_Disabled` **per call**, and the scheduler
re-reads its descriptor once per wave, so the fix can be switched off and back on
**live**, with everything else held constant:

```
*r SMRFixPack_Disabled.DustDevilSpawnGate = true    -- vanilla from the NEXT wave
*r SMRFixPack_Disabled.DustDevilSpawnGate = false   -- fix from the NEXT wave
```

⚠️ **"From the next wave", not immediately** — the wave now in flight already
holds its descriptor. Watch the logger's `WAVE descriptor` line for `gated=YES`
/ `gated=no` to know which body produced which burst; that line is the ground
truth for attribution, not the toggle command.

### ⭐ PREDICTIONS — written 2026-08-02, BEFORE the leg runs

Record the reading against each one. **A prediction that misses is the finding.**
Counts re-derived, not inherited: **80 registered modules** (79 + `DustDevilSpawnGate`),
**74 default-active**, **86 probes** (85 + `DustDevilSpawnGate`). ⚠️ The *active*
number depends on which opt-in toggles the profile has on — **Mod Options survive
a Mod Manager disable**, so read `ListFixes()` before writing it (PT-60's P1
missed on exactly this, with no defect behind it).

| # | prediction | what a miss means |
|---|---|---|
| **P1** | `SMRFixPack.ListFixes()`: **80 registered**, and `DustDevilSpawnGate` reports **`active`** with an empty detail | the `OverrideDisasterDescriptor` preflight or the `SetGlobal` read-back failed, or the preset self-check latched — read the detail string first |
| **P2** | `SMRTest.RunAll()`: the new probe `DustDevilSpawnGate` **PASSes**; probe total **86**; **no probe that passed under PT-60 now fails** — the one at risk is `DustDevilsDescrMap`, since F93 and F97 sit on the same call chain | the two dust-devil fixes interfere, which is the exact thing prompt 8c was gated on `8b` to prevent |
| **P3** | **VANILLA HALF** (fix disabled): every `WAVE descriptor` line reads `spawn_chance=50 count=6..8 gated=no`, and every wave spawns **3 or 4** positioned devils. **Never 0, never 6, never more than 4** | the defect is not what the source says it is — stop and re-derive before touching the fix |
| **P4** | **FIXED HALF**: every `WAVE descriptor` line reads `spawn_chance=100` and `gated=YES`, with `count` reading either **`6..8`** or **`0..0`** and nothing else | the copy is not reaching the scheduler, or a field was lost in it |
| **P5** | **FIXED HALF, observed bursts**: each wave spawns **either 0 or 6-8** positioned devils, matching the `count` on that wave's own `WAVE` line. Over ~10 waves both outcomes appear, roughly half and half | a mismatch between the predicted and observed count means something between the descriptor and the spawn loop is interfering — a storm (check `HasDustStorm`), vegetation refusals (the logger prints `REFUSED`), or `GetRandomPassableAwayFromBuilding` returning nil and breaking the loop early (`:224-226`) |
| **P6** | ⭐ **the discriminator, stated as one number: `count_max` becomes reachable.** At least one wave in the fixed half spawns **8**. Vanilla cannot produce 8 from this preset under any roll | if no wave ever reaches 8 over ~10 waves, the repair is not doing the one thing it exists to do |
| **P7** | **zero `[LUA ERROR]` naming `Fix_DustDevilSpawnGate`**, across the whole sitting and both halves — including the wave immediately after each toggle flip | the wrapper throws on a path the probe's stand-in preset does not reach; the property-list copy is the suspect |
| **P8** | **the other three disasters are untouched.** Meteors, dust storms and cold waves behave as they did — they share `OverrideDisasterDescriptor` and the wrapper is keyed on `original.class` alone | the class key is wrong or a preset carries an unexpected `class`, and three unrelated disaster schedulers are being rewritten |
| **P9** | **SOAK / save-boundary:** save mid-wave, reload, and the scheduler continues — `WAVE` lines resume and devils keep spawning. On the reloaded save the **first** wave may still carry a pre-roll made before the save; from the second it is business as usual | the descriptor copy did not survive persistence, which would mean a value the property walk copied is not plain data |
| **P10** | **UNINSTALL:** with the pack removed, the same save keeps producing dust devils, and within **one wave** the `WAVE` line (kit still installed) reads vanilla numbers again — `spawn_chance=50 count=6..8 gated=no` | ⛔ this is the `Fix_MeteorFrequency` failure mode (F86 Site 1). It should be impossible here — we own no body and no thread — so a miss means the §3a reasoning on the F97 entry is wrong |

**Not predicted, and deliberately so:** the exact ratio of gated-off to gated-on
waves. Ten waves is far too small a sample to say anything about a 50/50 gate, and
a run of four zeroes is unremarkable. **Do not read the ratio as evidence either
way** — P6 is the discriminator, and it needs only one wave of 8.

### Steps

⚠️ **Use a throwaway save or a sandbox.** The compressed cadence puts 6-8 dust
devils on the map every ~4 game hours for the length of the leg; they dust
buildings, trigger malfunctions and hurt colonists in the open. That is the
behaviour under test, not a side effect to design around — but do not run it on
a campaign save you care about.

1. **PT-00 sweep.** Then pick a colony and run the **Trap 1** terraforming check
   before anything else. If `DustStormsDisabled` prints `true`, change colony.
2. `*r SMRTest.RunAll()` → **P2**. `SMRFixPack.ListFixes()` → **P1**.
   ⚠️ Use the `*r` form — a bare `SMRTest.RunAll()` runs with no thread context
   and some probes skip.
3. Apply the setup block, then the **sixty-second smoke test**. Confirm
   `HasDustStorm(MainMap)` is false and `DustStormsDisabled` is still `false`
   (**Trap 2**).
4. **Vanilla half first** — `SMRFixPack_Disabled.DustDevilSpawnGate = true`, then
   `*r RestartGlobalGameTimeThread("DustDevils")` and the marker sweep again so
   the change takes effect at once. Let ~5 waves run at high speed; count
   positioned spawns between `WAVE` lines → **P3**.
5. **Re-enable** (`SMRFixPack_Disabled.DustDevilSpawnGate = false`, restart,
   marker sweep), let ~10 waves run → **P4, P5, P6**. Watch **P7** throughout.
6. Save mid-wave, reload, **re-apply the setup**, continue a wave or two → **P9**.
7. Check the other disasters are still arriving normally → **P8**. (A meteor or
   cold wave in the log is enough; do not wait for one.) ⚠️ Dust storms are off on
   this map by construction — read P8 off meteors and cold waves only.
8. Quit, remove the pack (Mod Manager; **keep the Test Kit on**), load the same
   save, re-apply the setup, run a wave → **P10**.
9. `FlushLogFile()` before reading the log while the game is still running —
   `ConsolePrint` output and the pack's own lines sit in the buffer otherwise.
9. ⛔ **Report every unexplained log line with its age.** "Not caused by our leg"
   is an attribution verdict and not a dismissal, and every previous pushback on
   one of these lines has turned up a vanilla defect that was not on our list
   (`WORKFLOW.md`). ⚠️ Expect noise from the compressed preset itself: a 20-second
   `duration` makes devils expire almost immediately, which is not a defect.

### What this leg does NOT settle

⛔ **The rate question.** This leg can prove the authored range is reachable and
that the gate fires at its stated chance. It cannot say whether the resulting
frequency is the one the game was tuned for — `DustDevils_Low` accidentally
approximates a gate today (50% × 1..2 truncates to 0-or-1), so the shipped rates
*may* have been tuned around the truncation. **That is chain prompt 12's job 8,
and reversal is a legitimate outcome no matter how cleanly this leg passes.**

## PT-62 — D12 "no homeless residents" policy · covers **D12 `Opt_NoHomeless`** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 10

**Written 2026-08-02 with the build, predictions BEFORE any run. The module is
UNRUN and claims nothing until this leg does.**

**⛔ PT-00 first.** Sweep result at build time: **CLEAN — zero `TEMPORARY` hits in
both repos.** Re-run it at the keyboard.

### ⛔ THIS LEG NEEDS A PROVISIONED FIXTURE, AND THAT IS THE EXPENSIVE PART

Do not treat the setup as a five-minute job. The behaviour under test only exists
in a colony that has reached a specific, uncomfortable state: **a specialist dome
holding colonists it can never house, in a colony with essentially no spare beds
anywhere.** That is either

* **the campaign save that produced the original observation** (2026-07-30: the
  child dome read `overpopulated=true homeless=20`, nurseries at 5/26 and 3/26,
  `accept_colonists true`) — cheapest by far **if it still exists and still sits
  in that state**; check before planning around it, because the entry itself
  notes the dome was on a knife edge and *"two more departures would clear
  `overpopulated`"*; or
* **a constructed fixture**, which means: a dome whose ONLY residences are
  Nurseries, children raised in it to Youth, and the rest of the colony's housing
  filled. That is a solo provisioning sitting, not a warm-up.

⚠️ **The as-saved state is what is being tested.** Do not substitute a fresh
sandbox with hand-placed buildings and call it equivalent unless the free-bed
count colony-wide is genuinely at or near zero — the tie the module bypasses only
occurs when `better_home` is false **everywhere**.

### ⛔ FOUR SETUP TRAPS. The first one will read exactly like the fix doing nothing.

**Trap 1 — the subjects must be UNEMPLOYED, and workforce-age.** ⚠️ **RULE
CHANGED 2026-08-02, after the owner described the real setup** — the module no
longer asks whether the dome could ever house them. It moves a homeless colonist
iff vanilla's own `need_work` is true: `CanWork()` and no workplace and no
pending player-forced workplace. So the dome's building mix is irrelevant, and
these stay put no matter what:

* anyone **employed** there — the staff its ordinary housing exists for;
* **Seniors and Children** — `CanWork()` is false for them, and a homeless one
  is the build-more-housing signal, not a defect to clear;
* anyone sick, StressedOut, Earthsick or otherwise unable to work.

Confirm the population before starting, with the dome selected:

```
*r local d = SelectedObj local n = 0 for _, c in ipairs(d.labels.Homeless or empty_table) do if c:CanWork() and not IsValid(c.workplace) and not c.user_forced_workplace then n = n + 1 end end ConsolePrint(print_format(d.class, "homeless", #(d.labels.Homeless or empty_table), "movable", n))
```

⛔ **`movable` must be > 0** or the leg measures nothing. **The row itself also
shows this number** — `off (N would move)` — so it can be read without the
console, and that is deliberate.

**Trap 2 — the DESTINATION must have housing of a kind they can use.** The module
will not send a grown Youth from one Nursery-only dome to another. If every dome
in the colony is specialist, nothing moves and that is **correct behaviour**, not
a failure — it is P9, and it must be distinguished from P4 by checking the other
domes before starting.

**Trap 3 — the module is OPT-IN and off by default.** Enable it in
Options → Mod Options → Community Fix Pack ("No homeless residents (per Dome)").
⚠️ **Mod Options survive a Mod Manager disable** — PT-60's P1 missed on exactly
this — so read `SMRFixPack.ListFixes()` for the truth rather than assuming.

**Trap 4 — turn D07 `CohortHousing` OFF for this leg, or use grown Youths only.**
D07 wraps the same method and moves Children and unemployed Seniors toward cohort
slots. If the stranded population is Children, the two modules become
indistinguishable in the result. The original observation was **26 Youths and 2
Adults**, which D07 ignores entirely — that population is the clean one.

### The A/B

Within-session, honoured per call, both directions:

```
SMRFixPack_Disabled.NoHomeless = true
SMRFixPack_Disabled.NoHomeless = false
```

⚠️ The UI row also disappears from **newly opened** infopanels while the module
is inactive; a panel already open does not rebuild until re-selection. That is
expected, not a defect.

⛔ **The uninstall half is a MOD-MANAGER DISABLE, never the toggle.** With the
module merely switched off the mod env is still present and the hooks are still
installed, so any captured frame resolves `SMRFixPack`, reads inactive and
no-ops: **it reads clean by construction whether or not the module leaks.** Use
the PT-20 method (`ENGINE_FACTS.md`, "OFF" IS THREE DIFFERENT THINGS).

### ⭐ PREDICTIONS — written 2026-08-02, BEFORE the leg runs

Record the reading against each one. **A prediction that misses is the finding.**
Counts re-derived by counting, not inherited: **81 registered modules**
(80 + `NoHomeless`), **74 default-active** (`NoHomeless` is opt-in and adds
none), **87 probes** (86 + `NoHomeless`).

| # | prediction | what a miss means |
|---|---|---|
| **P1** | `SMRFixPack.ListFixes()`: **81 registered**, and `NoHomeless` reports **`active`** with an empty detail once enabled in Mod Options | a preflight check failed — read the detail string first; it names which target went missing |
| **P2** | `*r SMRTest.RunAll()`: the new probe `NoHomeless` **PASSes**; probe total **87**; **no probe that passed under PT-61 now fails** | the wrapper is over-broad or the shipped emigration shape moved |
| **P2b** | ⛔ **OWED TO CHAIN 8c, SECOND HOP:** in that same `RunAll()`, **`DustDevilSpawnGate` still PASSes.** 8c added a `forbidden` early-return to `Fix_DustDevilSpawnGate` after PT-61 that is behaviour-neutral **by construction but not by measurement**, and it has been looking for a suite run ever since | the early-return changed behaviour; report it against F97, not D12 |
| **P2c** | ⛔ **the probe's own CONTROL case passes** — i.e. the `NoHomeless` probe does not FAIL with the *"vanilla moved a stranded homeless colonist with the policy OFF"* verdict | that verdict means **the vanilla tie no longer holds** and D12's whole premise needs re-deriving before any other reading here is trusted |
| **P3** | **VANILLA HALF** (`SMRFixPack_Disabled.NoHomeless = true`, or the flag simply not set): over ~2 sols the specialist dome's `#labels.Homeless` does **not** fall — it holds or grows | the strand is not reproducing on this save; the fixture is wrong, not the fix |
| **P4** | **FIXED HALF** (flag ON via the infopanel row): the same count **falls**, and reaches **0** unless P9 applies. Take the count immediately before setting the flag and immediately after, per the entry's knife-edge note | the push is not firing — check Trap 1 first, then whether any destination passes Trap 2 |
| **P5** | ⛔ **NOBODY IS EVER OUTSIDE.** Total colony population is unchanged across the drain, every colonist that left the dome is inside another dome, and there are **zero** deaths attributable to the move | this is the one failure mode the design was built to make structurally impossible (F53 territory). A miss here stops the leg immediately |
| **P6** | the source dome's **`overpopulated` clears**, and the drain is what cleared it — the before/after homeless counts bracket `g_Consts.OverpopulatedDome` (**measured at 20**, `>=`) | if it cleared without the count crossing 20, natural attrition did it and the leg proves nothing about D12 |
| **P7** | with `overpopulated` cleared, **D07 resumes delivering Children into that dome unaided** (D07 on, its `consider()` no longer skipping it) | ⚠️ this is the entry's **design rationale**, not a claim the build makes. A miss is a finding about the unwind, not about the push — and neither outcome flips any status |
| **P8** | ⭐ **SUBJECT CONTROLS, all on the flagged dome, all at once:** homeless **Seniors** stay · homeless **Children** stay · **employed** colonists stay · only the workforce-age **unemployed** move | the subject test is not `need_work`. A Senior or Child moving is the serious miss — it deletes the build-more-housing signal the owner named as the reason they must stay |
| **P8b** | **the row reads its own consequence** before any click: title `Nursery / Retirement Dome` in both states, right-hand value `off (N would move)` → `N moving out`, and the count matches the console reading from Trap 1. ⛔ The OFF state must **not** render red | a mismatch between the row's number and the behaviour means the UI and the wrapper disagree about who is a subject — fix before trusting any other reading |
| **P9** | **NO-DESTINATION CONTROL:** flag ON with every other dome either quarantined, flagged, or lacking suitable housing → **nobody moves and nobody is expelled**; the colonists simply stay | best-effort is not being honoured; see P5 |
| **P10** | **PING-PONG CONTROL:** flag ON on two domes at once → no colonist is traded between them repeatedly | the destination filter is not excluding flagged communities |
| **P11** | **zero `[LUA ERROR]`** naming `Opt_NoHomeless` or `NoHomeless`, across the whole sitting and both halves | — |
| **P12** | **UNINSTALL (Mod Manager disable, not the toggle):** save with the flag ON, disable the pack, load the same save → clean load, **zero** orphan errors, and the colony behaves as vanilla. The `SMRFixPack_no_homeless` field is still on the dome and is inert | the module leaks. It should not be able to: no threads, no GameVars, no globals, one plain boolean field |
| **P13** | **toggle off = instantly vanilla**, same session, no reload — set `SMRFixPack_Disabled.NoHomeless = true` mid-drain and the pushes stop | the per-call `IsActive` gate is not being consulted somewhere |

**Not predicted, and deliberately so:** how *fast* the dome drains. Emigration
runs off the colonist heavy update and the destination search is best-effort;
anything from "over a few hours" to "over a sol" is unremarkable. **Do not read
the rate as evidence either way.**

### ~~One extra reading, owed from chain prompt 9~~ ✅ **RUN 2026-08-02 — `userdata`**

⭐ **The F98 localisation control is DISCHARGED.** `*r ModLog(type(T(8821,
"ZZZ")))` printed **`userdata`** (log `Mars.exe-20260802-20.28.19`), confirming
that a re-used translation id is discarded at `T()` construction and that our
shipped `Fix_TechDescriptionBuilding` never worked in retail. `table` would have
refuted it and forced F25's restoration in both places. **F98 no longer rests on
source alone; do not re-run this.**

### Steps

1. **PT-00 sweep.** Then confirm the fixture with the Trap 1 command, and check
   the other domes for Trap 2 before committing to the sitting.
2. `*r SMRTest.RunAll()` → **P2, P2b, P2c**. `SMRFixPack.ListFixes()` → **P1**.
   ⚠️ Use the `*r` form — a bare `SMRTest.RunAll()` runs with no thread context
   and some probes skip.
3. ~~Take the loc reading above~~ — already discharged 2026-08-02, skip.
4. **Vanilla half first.** Leave the flag unset, run ~2 sols → **P3**. Record the
   homeless count at the start and the end.
5. Select the specialist dome, **set the flag from the infopanel row** (this also
   look-checks the row: title, icon, rollover text, and that it sits with the
   other toggles rather than below the stat blocks). Record the count
   immediately, then watch → **P4, P5, P6**. Watch **P11** throughout.
6. With `overpopulated` cleared and D07 on, watch for children arriving → **P7**.
7. Run the three controls → **P8, P9, P10**. **P9** is the important one; if the
   colony cannot naturally produce a no-destination case, make one by
   quarantining the candidate domes.
8. Mid-drain, `SMRFixPack_Disabled.NoHomeless = true` → **P13**.
9. Save with the flag ON. Quit, **disable the pack in the Mod Manager** (keep the
   Test Kit on), load the same save → **P12**.
10. `FlushLogFile()` before reading the log while the game is still running.
11. ⛔ **Report every unexplained log line with its age.** "Not caused by our leg"
    is an attribution verdict and not a dismissal, and every previous pushback on
    one of these lines has turned up a vanilla defect that was not on our list
    (`WORKFLOW.md`).

### What this leg does NOT settle

⛔ **It does not settle C40, and it is not aimed at it.** The Reddit-reported
symptom that travelled with this item — colonists *flickering* between housed and
unhoused as the Ministry of Culture's staffing changes — is a **churn** mechanism
(`BUGS.md` C40, mechanism verified vs Src, harm unproven). **D12 does not fix it
and this leg cannot measure it.** If the fixture colony happens to have Crowded
Living enacted, expect capacity to move under you and say so in the report; that
is C40's own keyboard observation, which is still owed.

⛔ **It does not license the word "homelessness" anywhere player-facing.** What
passes here is *colonists stranded in a dome that cannot house them get out*.

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

# 6 · Needs-eyes list — one-observation riders

**Three intakes now feed this list**, and they do not all mean the same thing —
read the block above each table before taking a reading:

1. **The reachability audit (2026-07-30)** — verdicts believed on source-shaped
   evidence. **None of these is currently believed wrong.**
2. **The popup audit (2026-07-30 late)** — same shape, its own four verdicts.
3. **The bug-list audit (2026-08-01)** — these are different: two of them
   (**F35**, **C32**) exist because an external witness suggests something we
   believe may be *incomplete or misattributed*, and two (**F80**, **F82**)
   are evidence-gathering on open defects with no located mechanism. Each row
   says what it decides. ⭐ **Updated 2026-08-02 (prompt 6c): F82's mechanism
   IS now located from source, so its row is no longer evidence-gathering — it
   is a one-shot confirmation of a named number (≈120 REAL seconds), and it can
   fail in a way that would force a correction to the entry. F80's row is
   sharpened but its mechanism is still open.**

None of these is a full PT. Each is a **single observation**, taken
opportunistically: if you are already in a save that qualifies, take it and
record it.

### From the reachability audit — settling observations

Each settles a verdict currently believed on source-shaped evidence — the exact
kind of evidence F49(c) proved can lie. Source is decisive about whether a code
path can execute and **near-mute about whether what it does is wrong**; every
row below turns on runtime or interface behaviour the Lua does not carry
(hit-testing, affordances, cursor and confirmation feedback, engine placement,
visual outcome).

**None of these is currently believed wrong.** Full reasoning per row is in
`REACHABILITY_AUDIT.md` §3 (Challenge review 2026-07-30).

| Fix | The one observation that settles it |
|---|---|
| **F16** | Finish a Mirror Sphere excavation, open the finished site's infopanel, click "Pierce the Shell" — do drones engage a dead request? (overlaps PT-30) |
| **F38** | Destroy a tunnel, save/load **in vanilla**, order a colonist or rover across — does the route still use the ruin? (overlaps PT-25) |
| **F34(d)** | Drop a landscape mark over a rocket actively loading drones — is a mid-"Embark" drone visibly yanked, or does it recover silently? |
| **F74 + F53(a)** *(merged 2026-08-01)* | **One never-modded fresh colony, two observations, one sitting** — see the fresh-colony note below, which is the whole cost of both. **(1)** Order an RC Transport onto a landed storybit trade rocket — does the original harm actually occur? **(2)** Land a passenger rocket flush against a Universal Depot — do arrivals actually strand? (F53(a) also overlaps PT-18.) ⬇ **F74's half is downsized to exactly this** (bug-list audit 2026-08-01, `BUG_LIST_AUDIT.md` §2.2 row F74): its "is the vanilla harm real at all" question now has two outside answers — a 1.0.7 dev note (*paraphrase-grade*: RC-Transporter rare-metals rocket-overload exploit fixed, [S32]) and fredware's independent Relaunched fix #10, *"Prevents RC Transports from interrupting Universal Trade Rockets"* [S23] — so the observation is no longer load-bearing for the verdict. It rides along only because the fresh colony is already there for F53(a) |
| **F06** | Reach the Mystery 10 finale and ignore the corner notification for one sol at speed — does the Epilogue really arrive minimized and unpaused? |
| **F26** | Watch one Last War volley with the fix off and one with it on — is the spread visible? (this IS PT-47's first result line) |
| **F22** | Open the Last Transmission faction goals panel in a young politics-enabled colony — where is the corrupted number player-visible before the Martian Assembly stage? (overlaps PT-42) |
| **F77** | Flap an extender during hub activity, with and without — how big is the fleet Idle-kick? (this IS PT-52 Trigger B's F77 half) |
| **F11** | Crew-gather a busy train's passenger, then inspect `train.units` — the U-tier settling read |
| **F81b** | On a vanilla save, catch a blocked `RainsDisasterThreads` activation after a collision; or under the fix, rain resuming within ~7 sols. ~~(overlaps PT-54 Trigger E)~~ → **carried by the F86 Tier-1 `Fix_RainsDeadlock` A/B leg** (PT-54 retired 2026-08-01) |

### From the popup audit

**Added 2026-07-30 late by the popup audit (`POPUP_CONSEQUENCE_AUDIT.md` §8 —
full reasoning there; these four settle ITS verdicts):**

| Subject | The one observation that settles it |
|---|---|
| **Audit keystone (storybits/sequences safe)** | `ForceActivateStoryBit("<popup-carrying bit>", MainMap)` (not immediate) → save with the corner notification up → load → `IsValidThread(g_StoryBitActive[1] and g_StoryBitActive[1].run_thread)` should print **true** → click the notification → the popup must open, and answering it must apply the outcome (~5 min, console) |
| **F83 second site** | After declining/losing a `ReconCenterDiscoveryAsteroid` popup, is the paid Detailed Scan reachable anywhere else (planetary view)? Needs a Recon Center holding ≥ `g_Consts.DiscoveryScanCost` Electronics for `CanPerformDetailedScan()` |
| **F85 (U tier)** | Rebind Quick Save to **F9**, open any choice popup (a launch-issue prompt is cheapest), press it — does a save land, and does loading it void the choice? |
| **§3.6 corner (optional)** | With the distress-call popup left open, does the sol-change autosave fire under it? |

### From the bug-list audit — two scope checks and two evidence-gathering reads

**Added 2026-08-01 by the bug-list audit (`BUG_LIST_AUDIT.md`) and the entries
named on each row — four cheap riders, no sitting of their own. Unlike the two
tables above, these are not "believed right, verify anyway":**
**⬇️ THREE REMAIN — the F35 row was taken and closed 2026-08-01** (it rode the
F86 Phase-0 keyboard sitting, exactly the opportunistic way it was written to be
taken; row struck through below, full record on BUGS.md F35).

| Subject | The one observation, and what it decides |
|---|---|
| ~~**F35 live-label check**~~ **✅ TAKEN AND CLOSED 2026-08-01 — no longer a rider.** Measured at the keyboard during the F86 Phase-0 sitting (log `Mars.exe-20260801-14.59.57-6a22b86d.log`): from a **pre-research save**, all three turbine labels read `NO MODIFIERS` before, and after the tech landed all three — **`WindTurbine_Large` included** — carried `prop=electricity_production percent=100` under the vanilla `Effect_ModifyLabel` keys (`id=GameEffect`, not `SMRFixPack_F35_*`), with **Power doubling on every one** (9.3→18.6 / 18.6→37.2 / 29.8→59.5). No reload in the window, so our pass could not have supplied it. **The audit’s live-miss suspicion is dead and F35’s scope is right.** Trigger: the tech was granted with `UIColony:SetTechResearched("FrictionlessComposites")` — it is a Breakthrough and was unobtainable in that colony — which is the same `EffectsApply` funnel natural completion uses (`Research.lua:313`). ⚠️ **Read the trap on the BUGS F35 entry before repeating this anywhere:** the first attempt read the labels while **Low-G Turbines** was completing, which grants upgrade unlocks and no label modifier at all, and its correct `NO MODIFIERS` result nearly got filed as a P1. Confirm `IsTechResearched("FrictionlessComposites")` first. Full record: BUGS.md F35 |
| **C32 label-membership read** ⚠️ **REWRITTEN 2026-08-01 by the prompt-6 Src sweep — the old row's trigger no longer occurs and its pass/fail rule was wrong; do not take the old version.** | **Trigger (corrected): you must ABANDON an asteroid** — the manual button, `Asteroids:UIAbandonAsteroid` — because on 1.0.7 asteroids never expire on their own (`Asteroids.lua:1, :208, :331-348, :493-500`), so "visiting and leaving" unloads no map and reads nothing. **Read (corrected): destroyed buildings must be excluded, or the first meteor strike will "confirm" C32** — `Building:OnDestroyed` is empty while `ShiftsBuilding:OnDestroyed` de-labels, so every destroyed-but-unrebuilt building legitimately sits in `UICity.labels.Building` and outside the colony label: `*r local n = 0 for _, b in ipairs(UICity.labels.Building or empty_table) do if IsKindOf(b, "ShiftsBuilding") and not b.destroyed and not b.demolishing and not b.bulldozed and not UIColony:IsInLabel("ShiftsBuilding", b) then n = n + 1 end end ConsolePrint("live ShiftsBuilding missing from the colony label: " .. n)` — and note it now tests membership with `IsInLabel` (the engine's own key-map test, `CommonLua\LabelContainer.lua:106-109`), not `table.find`, because the two disagree exactly in the array-vs-key desync case. **A non-zero count is the defect; a zero count still proves nothing** (`UICity` follows the current map, `Lua\_init.lua:12-14`, so read it on the map whose buildings you care about). Decides C32 (BUGS C32 entry, which the sweep DOWNGRADED — mechanism has no route in current Src) and feeds prompt 7's F04 tier decision |
| **F80 settling observation** ⭐ **REWRITTEN 2026-08-02 (prompt 6c source audit) — it now discriminates WAITS vs WALKS and tests a named directional prediction** | **Trigger: any train sitting where EITHER symptom appears** — colonists queued at a platform while trains come and go (*waits*), **or** colonists setting off overland past a working station (*walks*). The audit says these are two faces of one enumeration, so **the walk case is now equally valid evidence and is the commoner one in the wild** — do not skip the sitting because nobody is waiting. ⛔ **Tap before mitigating: adding trains destroys the evidence.** Take all three, in order: **(1) Classify.** Waiting or walking? Note which, and the origin/destination **pair** that fails — the audit predicts a *specific pair* failing inside an otherwise healthy network, **not** a network-wide break, so a global failure would falsify the theory outright. **(2) The ready console tap** on the global `ForEachStationAlongTrack` (recorded in the F80 entry) — it prints each stop's enumerated destination set. **(3) ⭐ The directional test, which is the new discriminator and is free**: call `GetReachableStations()` on **both** endpoints of the failing pair. **The predicted signature is a ONE-WAY HOLE** — A's list omits B while B's list contains A (or the mirror). **PASS/consistent-with-F80 = a one-way hole.** **FALSIFIES the enumeration theory = both lists name each other** (the walk is then a decision made downstream of a correct reachable set, and the mechanism is elsewhere entirely). Also record whether a **track segment was under construction** anywhere on the line at the time — that is a legitimate rival explanation the audit confirmed is by-design truncation (`TrainTransport.lua:421`), and it must be excluded before the reading counts. F80 is the audit's strongest reported-but-unpinned defect (§4): Relaunched witness, a dev note, an exact source predicate as of 2026-08-02, and still **no proven trigger** |
| **C25 Jumbo Cave trigger check** ⭐ **ADDED 2026-08-02 (prompt 6b) — waits for the situation; take it the moment a Jumbo Cave Reinforcement site sticks** | **Only the trigger is unproven** (the wedge chain is Src-verified on the C25 entry) — i.e. does cave geometry actually strand a waste rock? **Take the read WHILE the site is stuck, and while looking at the UNDERGROUND map** (`UICity` follows the current map, `_init.lua:12-14`): `*r local n, rocks, stuck = 0, {}, 0 for _, d in ipairs(UndergroundMap.City.labels.Drone or empty_table) do for b in pairs(d.unreachable_buildings or empty_table) do if IsValid(b) and IsKindOf(b, "WasteRockObstructor") then n = n + 1 if not rocks[b] then rocks[b] = true if b.parent_construction then stuck = stuck + 1 end end end end end local u = 0 for _ in pairs(rocks) do u = u + 1 end ConsolePrint("waste-rock entries in drone unreachable tables: " .. n .. " over " .. u .. " distinct rocks, " .. stuck .. " of them attached to a construction site")` — the `IsValid` guard is required because the table also holds a plain `version` key (`Drone.lua:826`). **Reading: a non-zero `attached to a construction site` count while the site is stuck is the trigger, and C25 earns its F-row; ZERO while stuck means the wedge is something else and C25's mechanism is not the cause** (record that too — it is the more useful result). ⚠️ **Also record the save's vintage.** 1.0.6 replaced the whole Jumbo Cave scenario and the swap is gated on `UndergroundRework106`, which is **false in any save started before 1.0.6** (`UndergroundDome.lua:16-19`) — so state whether this colony was begun pre- or post-1.0.6, or the observation cannot be placed. Decides C25 (BUGS C25 entry) |
| **C20 pause-scan observation** ✅ **DONE 2026-08-02 — VERDICT: DEFERRED, NOT LOST; C20 CLOSED** | **Result, kept for the record.** Paused, probe deployed on an unexplored sector: **no `SectorScanned` signal**. On unpause: the **"Sector scanned" voice-over fired**, which proves the `Msg` fired, because `QueueVoice` sits inside `AddHUDNotification` (`HUDNotifications.lua:33-36`) at `Exploration.lua:103`, immediately before `Msg` at `:104`. ⭐ **Internal control, timing confirmed by the observer**: `NewAnomalies` appeared **before** the unpause (synchronous `NotificationPreset`, `Anomaly.lua:444`), `SectorScanned` fired **the instant the game unpaused and not before**. One scan, two notifications, split exactly on the pause boundary — which also proves the scan itself executed under pause and rules out the rival reading that the probe simply never deployed. ⚠️ **This row's original wording was WRONG and cost the observer a step**: it said watch for an "on-screen toast". `SectorScanned` is a **`HUDNotificationPreset`** (`Data\HUDNotificationPreset.lua:55-61`, `button_id = "idOverview"`) — it badges the Overview button and plays a voice line, **there is no popup card**. ⚠️ If anyone ever re-runs the save/reload variant, read `IsHUDNotificationShown("SectorScanned")` and **not** the voice: `QueueVoice` is rate-limited at `const.NotificationVoiceCooldown` = **120 real seconds** per id, so a repeat inside two minutes is silently absent and reads as a false "lost"
| **F82 timing observation** ✅ **DONE 2026-08-02 — PASSED; MECHANISM PROVEN BY MEASUREMENT** | **Result.** Run on a No-Disasters save so nothing but the player could break a cable. A console watcher on `FindNotification("PowerGridSplit", CurrentMap)` timed both clocks, grid left **unrepaired** in both legs: **`119999` real ms / `600000` game ms at 5x**, and **`120001` real ms / `120000` game ms at 1x**. Against a preset `Expiration = 120000`: **real time constant to within 2 ms across a 5x speed change, game time varying by exactly 5.000x.** ⭐ Both legs left the split **unrepaired and the notification vanished anyway**, so the symmetric half — the colony stops reporting a break that is still there — is measured, not inferred. ⚠️ Method notes for any re-run: **do not click the notification** (`PowerGridSplit` does not set `Dismissable`, which defaults to `true`, so a click ends the measurement), and **stay on the map you cut on** (the preset is `PerMap`)
| **C26 stranded-maintenance dump** ✅ **DONE 2026-08-02 — BOTH READINGS CLEAN; C26 CLOSED** | **Result, kept for the record.** Two **independent** colonies (`save_game_id` compared in the log, not assumed): **`10 / 0`** at sol 288 and **`2 / 0`** at sol 59 (~50 of those sols organic pre-playtest). Zero reason lines in both. ⭐ **Non-zero controls in both** — 10 and 2 buildings genuinely in maintenance/malfunction — which is what makes the zeros readable; a `0 / 0` could not be told apart from a query matching nothing. ⭐ **Masking condition checked before trusting either**: both vendor fixups run *at load*, so on a pre-fixup save a clean dump would mean “they just healed it”. Both colonies returned `OrigLuaRev` = `LuaRevision` = 396349, so the fixups were pre-seeded and never ran. ⚠️ **A false reading 2 was caught and discarded** — a 98-sol save that turned out to share `save_game_id` with the 288-sol one, i.e. the same playthrough earlier. **Always compare the id before counting a dump.** ⚠️ Both were taken **cold**, within a minute of load, deliberately overriding the 20-30 min warm-up default for comparability

### From the chain-8b build — two live halves the probes deliberately do not claim

**Added 2026-08-02 by chain prompt 8b.** Both fixes are probed for their
*mechanism*; these two riders are the parts a script cannot honestly assert. They
are cheap and opportunistic — no sitting of their own — and PT-60 says so rather
than pretending its probe result covers them.

| Subject | The one observation, and what it decides |
|---|---|
| **F90 underground-break rider** ⭐ **ADDED 2026-08-02 — take it the first time a dust storm arrives on a colony that has an elevator** | **Why a rider and not a probe: the defect is a VICTIM DISTRIBUTION, not a single event.** "No underground break happened this session" is what an unfixed game looks like most sessions too, so a one-shot in-play check cannot discriminate; the probe covers the filter itself (it asserts what vanilla's body was handed). **Preconditions that must all hold or the reading is void:** underground unlocked, **at least one elevator built** (that is what merges the grids — without it there is nothing cross-map and the fix's fast path returns untouched), a surface dust storm running, and the merged fragment holding **more than 10 connectors** (`IsBreakable`, `SupplyGrid.lua:693-697`). **The read:** while the storm runs and for a while after, **zero NEW `PowerLeak` / `LifeSupportLeak` notifications on the UNDERGROUND map**. ⚠️ **Exclude cave-ins before counting anything** — marsquakes and `CaveInRubble` break underground elements *on purpose* (`CaveInRubble.lua:158` is one of `:Break()`'s eight call sites), and that is exactly why the cheaper `Break`-interception fix was rejected as unsound. A leak that follows a cave-in is not evidence. **Non-zero underground leaks during a surface-only storm = the filter is not holding.** ⚠️ **Known residual, do not file it as a miss:** surface cables on an elevator colony still break somewhat MORE often than on a non-elevator colony — the break *probability* counts `#self.elements` and stays cross-map by decision. Full reasoning: BUGS F90 |
| ~~**F93 dust-devil map rider**~~ ✅ **RUN AND PASSED 2026-08-02, in its STRONG form, as a free by-product of PT-61's vanilla half** — and it was the owner's own idea to switch maps mid-leg "to confirm waves spawn regardless of which map is focused". **The case taken was the strongest one on offer: `CurrentMap.mapdata.MapSettings_DustDevils` read `disabled` on the underground while `MainMap` read `DustDevils_VeryHigh_3`.** Without F93 that is not a wrong-intensity read, it is the **nil** branch — `GetDustDevilsDescr`'s first line returns nothing, and the scheduler enters `while not new_descr do Sleep(const.DayDuration) end`. **Observed instead: seven consecutive descriptor reads returning `DustDevils_VeryHigh_3` with the camera underground, and the 4-hour wave cadence unbroken from sol 8 h11 through sol 9 h12** (log `Mars.exe-20260802-16.25.43`). ⭐ **The cadence is what makes this decisive** — a day-long park is a 24-hour gap against a 4-hour rhythm and could not have been missed. ⚠️ Attribution note: the camera window is by the owner's report (switched after wave 2, still underground when the `CurrentMap` read was taken after wave 10); the log timestamps and the returned preset id are the hard evidence. Original rider text follows. | **Why a rider: the probe drives the getter with stand-in maps, which proves the read follows `MainMap` but not that the live scheduler benefits.** **The read:** with the camera on the **underground** map, `*r local d = GetDustDevilsDescr() ConsolePrint(d and (d.id or "descriptor with no id") or "NIL — the scheduler would park a day at a time")`, then switch to the surface and repeat. **The two must agree.** ⭐ **The strong version costs nothing extra**: do it on a map pair whose dust-devil settings actually DIFFER, or with the underground set to `disabled` — that is the case where vanilla returns `nil` and the surface scheduler stops producing dust devils a day at a time until the player looks back at the surface. A matching pair on two identically-configured maps proves much less; say which case was taken. Decides nothing on its own (the defect is source-verified and the fix is a 7-line copy) — it confirms the live path, and a **disagreement** would mean the replacement is not the function the scheduler calls. Full reasoning: BUGS F93 |
