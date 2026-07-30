# Playtest Archive — completed tests and their results

Completed items from `PLAYTEST_CHECKLIST.md`, moved here verbatim (full test
text + the tester's result notes) so the live checklist only carries un-run
work. `BUGS.md` is the canonical status record; this file is the evidence
trail. Ground rules, save fixtures and the verified command reference stay in
the checklist — consult it before re-running anything here.

Archived 2026-07-26: PT-01 (F02 cadence + tower lead verified live; the
passive silence-watch continues via the watchdog), PT-02 (F03 → tested),
PT-03 (F44/F45 → tested), PT-04 (F50 → tested), PT-05 (F05 → tested — the
"A dream fulfilled" popup at 18/18), PT-07 (F12 → tested 2026-07-27 — fires
once, steady a sol, silent organic clear; Machine Parts half via forced
malfunctions; its first run caught and fixed the F12 "Food"-key collision),
PT-08 (F13 → tested — all 11 resource
rows show numbers, HUD cross-checked), PT-12 (F51 → tested — cached mode=false
recomputed to "shuttle" when the hub went live), PT-13 (F52 → tested* — passage
used in vacuum; surface walk correctly resumed once the passage was destroyed),
PT-34 (F54 → tested — hubs off: homeless stayed put inside; hubs on:
emigration resumed), PT-36 (F10 gate DONE 2026-07-27 — three funding calls
returned 0 cleanly over a maximally nil real-save history; F10 CLOSED wontfix,
fix file deleted, TestKit probe kept as canary), PT-38 (D02 gate DONE 2026-07-27 — cadence measured and CORRECTED to 120,000
GAME-ms = 4 game hours, not wall-clock; per-id suppression confirmed;
Opt_AcknowledgedWarnings build unblocked), PT-41 (F66 → tested), PT-45 (F47 →
tested), PT-46 (F49(b) resolved as no-defect; its (d)/(a) tail remains in the
checklist as un-run).

Archived 2026-07-29 (later): PT-11 (F01 → tested — two 20-game-hour legs either
side of a save/reload with the rubble count frozen at 27, then a positive control
quake taking it to 36. Running it exposed that the test as written could not
work: compressing a `g_Consts` interval does not shorten the sleep already in
flight, so the old procedure would have false-PASSed regardless of the fix. The
general rule is now in the checklist's ground rules).

Archived 2026-07-29: PT-29 (F41 → tested — `nil` → `50` → `150` console read;
Gene Forging alone now contributes its `param1 = 50` and the two techs add.
Running it exposed and fixed two documentation defects: the trigger was
literally unrunnable, and the doc's `--> nil` annotations broke the console —
see the section's result note).

Archived 2026-07-30: PT-55 (audit fix 1.3 live re-verify → CLOSED — first
mid-session enable works for all three reworked opt-modules; D04 binding
timing self-healing; D01 parked-rocket limitation accepted by user call;
ListFixes tracked a full OFF/ON/OFF toggle cycle with a clean log), PT-48
(D02 → tested — all five steps PASS on console counters, opened with a
positive control that proved the fixture could re-nag; the acked building held
16.9 game hours = 4.2 vanilla windows, the stamp survived save/reload, and
`InsufficientResources` — the game's ONLY other suppressable id — was shown
still arming its vanilla window untouched).

Archived 2026-07-27 (later): PT-14 (DONE — **premise falsified**: the
accept-colonists toggle is a **quarantine** — its OFF state is titled
"Quarantined" and the rollover promises "Colonists are not allowed to enter or
leave" — so the lockdown the tester observed is designed behavior, not F61's
defect; F61 CLOSED `wontfix` same day by user decision, fix deletion staged,
community ask re-filed as D03 `Opt_ResidencyControl` — full evidence on the
F61 + D03 BUGS.md entries), PT-24 (F36 → tested — geologist demand 11 → 0 at
the ExtractorAI grant with all other rows identical, before/after screenshots;
38 engineers + 2 medics + zero geologists across multiple cheat-graduation
rounds on two universities; also caught the CheatResearchAll
breakthrough-skip gotcha, command table corrected), PT-06 (F08 → tested —
5★ departure +23 applicants/$544.5M vs tanked ≤2★ group +7/$94.5M, the clear
split; early Earthsick leavers confirmed counted by the departure reward),
PT-26 (RESOLVED-UNRUNNABLE — the unmodded game cannot build a second
Artificial Sun (build-once wonder, colony-wide incl. sites), so F39's fix is
latent; user decision: fold it into the new D04 `Opt_MultipleSuns` opt-in that
lifts the limit AND ships the binding fix; single-sun night-production
baseline banked for the module's future playtest), PT-39 (F74 → tested —
landed trade rocket refused by cursor AND by route (route endpoint fell back
to a ground position, cargo dumped at the pad, rocket untouched); controls
clean; the setup's depot half surfaced the NEW vanilla F76 finding, tracked
separately).

---

## PT-01 — Meteor cadence + Sensor Tower direction · covers **F02**

**Setup:** SAVE-A. Meteor setting at least "Low". Note the current sol/hour.

**Trigger (console):**
```
SMRTest.Log.Meteors(true)
g_MeteorsGameDescr.spawntime = 40 * const.HourDuration
g_MeteorsGameDescr.spawntime_random = 0
SetGameSpeedState("ultra")
```
(`g_MeteorsGameDescr` is the live descriptor the thread re-reads each loop,
`Lua/Meteors.lua:271-278`; the change takes effect on the **next** interval, so let
one strike pass first.) Watch the console for `MeteorsDisaster at t=… (+N game hours)`
lines. Let 3–4 strikes go by.

Then the **direction check**: build 3 Sensor Towers (`CheatCompleteAllConstructions()`),
let 2 more strikes pass, and compare the gaps. Sensor Towers add warning time
(`const.SensorTowerPredictionAddTime = 12 * const.HourDuration`, `Lua/_GameConst.lua:125`).

- **BROKEN looks like:** meteors land roughly every 6 game hours, all game long — and
  putting up Sensor Towers makes the gaps *longer*, not the strikes more predictable.
- **FIXED looks like:** gaps sit near the 40 h you set (never far below it), and adding
  Sensor Towers does **not** stretch the gap further — it only lengthens the warning.

Turn the logger off (`SMRTest.Log.Meteors(false)`) and restore speed when done.

**Timing fact (explains a quiet start):** the fix restarts the Meteors thread on
every save **load** (by design — a running save would otherwise resume the old
broken thread), and a restart re-rolls the full interval from that moment. First
natural strike lands `spawntime`..`spawntime+random` game hours after the LAST
load/new-game: Very Low 90–140h, Low 65–90h, High 50–75h, Very High 35–60h
(`Data/MapSettings-Meteor.lua`, hours = value / 30000). Five quiet sols on Low
with a reload in the middle is on schedule. To re-roll NOW with edited values:
`RestartGlobalGameTimeThread("Meteors")` — same restart the fix does on load.

**Variant B — natural cadence on a high-threat map (better evidence, no console
edits):** start a throwaway colony on a landing spot with **maximum meteor
threat** (Very High → first strike sol 1.5–2.5, then every 35–60h). Logger on
from sol 0, ultra speed, let 3–4 natural strikes accumulate — gaps must sit in
the 35–60h band (never collapse toward 6h, never stop entirely; strikes
continuing IS the "fix didn't kill spawns" proof). Then build the 3 Sensor
Towers and let 2 more strikes pass: **gaps stay in the 35–60h band and do NOT
lock to ≤42h** — under the broken code with 3 towers the gap is
`Min(spawn, 42h)` and can never exceed 42h, so any gap over 42h is by itself
proof the repaired wait is running. (CORRECTED 2026-07-26: do NOT expect an
earlier warning banner for single strikes — the shipped singles thread posts no
disaster notification at all; the only per-meteor warning is the impact marker
~30 s before impact, and only when something sits in the blast area. The
towers' +12h/tower lead shows up in the Meteor STORM countdown banner, not on
single meteors.)
Variant A (above) remains the quick check for any save; either variant alone is
a valid PASS, B is preferred for the record.
Landed at 1 SOL
First strike No towers SOL 

`Result:` ____________Fail ended test at SOL 36 still no meteor strike after =57 mark_________________________________  (PASS / FAIL / notes / date)

Starting log at SOL 2.5
Meteor strike around 5.5 SOL
2nd Sol 7.5 (printed =60 game hours)
3rd Sol 8.4 ish (Printer =39 game hours)
4th sol 10.3 ish (printed =39 game hours) 
-build 3 sensor towers at around sol 10.5
rec meteor warning
meteor strike sol 12.5 (printed =57 game hours) 



2nd Pass meteors at t=26423435
meteor =49 game hours t=27910297

> Second pass, 2026-07-26 (sol-36 save, watchdog build): on load the necropsy
> printed "persisted Meteors thread on load was **alive**" — the PT-01 wedge was a
> live thread whose wake-up never came (scheduler/persist side), NOT a dead thread.
> Natural gaps this pass: **+49h, +40h** (t=26423435 → 27910297 → 29120125), both in
> the 35–60h band — and >42h is impossible under the broken code with 3 towers, so
> the cadence direction check is satisfied. `SMRFixPack.MeteorsWatchdogCheck()`
> reported `healthy`. Later `MeteorsDisaster` prints from the forced F45 meteors
> (t=30146007 onward) are console-triggered — do not count them as cadence. PT-01
> verdict pending only a longer silence-watch; the watchdog self-reports if the
> wedge recurs.
> **Tower warning lead VERIFIED (2026-07-26):** storm schedule shortened to 45h
> via the descriptor + `RestartGlobalGameTimeThread("MeteorStorm")` (game's own
> thread, real warning machinery) → countdown banner "Meteor Storm — Starts in
> 1 Sol 17 h" appeared ~3h in — the full ~42h tower-extended lead (6h + 12h×3,
> matching the Sensor Tower panel's "Disaster Early Warning: 1 Sol 18h"); stock
> lead without towers would read "Starts in 6 h". Towers lengthen WARNING, not
> gaps — the PT-01 direction check is closed on live evidence. (Storm timings
> restored to stock afterwards; the storm's own MeteorsDisaster logger print is
> console-triggered — not cadence.)
---

## PT-02 — Upgrade-modifier leak across build → upgrade → salvage → rebuild · covers **F03**

**Setup:** SAVE-A, a dome with a **Medical Center**. `CheatAddFunding(500000000)`,
`CheatResearchAll()` so the **Holographic Scanner** upgrade is available.

**Trigger:**
1. Select the dome and record its modifier count:
   `*r local n=0 for l,m in pairs(SelectedObj.label_modifiers or {}) do for _ in pairs(m) do n=n+1 end end ConsolePrint("dome modifiers: "..n)`
   (select the **dome** first — `label_modifiers` lives on the label container,
   `Lua/LabelContainer.lua:59-63`.)
2. Buy the **Holographic Scanner** upgrade on the Medical Center. Re-run the count →
   should go **up by one**.
3. **Salvage the Medical Center.** Re-run the count.
4. Rebuild the Medical Center (`CheatCompleteAllConstructions()`), buy the upgrade
   again. Re-run the count.

- **BROKEN looks like:** the count never drops after salvage, and climbs by one more
  every rebuild — the dome keeps a phantom +30 birth-comfort bonus from buildings that
  no longer exist, stacking forever.
- **FIXED looks like:** the count returns to its pre-upgrade value after salvage, and
  after rebuild+re-upgrade sits at exactly **one** upgrade modifier — no stacking.

> Note: the fix stops **new** leaks. Modifiers already leaked into an *old* save are
> not swept yet (that's the queued `90_SaveSanitizer.lua`). Test on a save built with
> the pack active.

`Result:` ____________PASS_________________________________

---

## PT-03 — Track salvage: partial trim, curve visuals, broken-track salvage · covers **F44, F45**

**Setup:** SAVE-A with a Martian Express station and track. Build **two** test tracks:
a straight run of ~8 hexes, and a second run that **ends in a curve** (this is the
visual the audit specifically flagged). `CheatCompleteAllConstructions()`.

**Trigger — F44 (partial salvage):**
1. Assign a train to the straight track.
2. Salvage-click a **middle hex**.
3. Repeat on the **curve-ended** track, clicking a hex 2–3 in from the curved end.

- **BROKEN looks like:** clicking one hex deletes the whole track — and any train
  assigned to it vanishes with it.
- **FIXED looks like:** only the clicked segment (plus the short unusable stub on one
  side) disappears; the long viable side and the train survive.
- **VISUAL CHECK (the audit's specific concern):** after trimming near a curve, does
  the remaining track *look* right — pillars, rails and end-caps in sensible places, no
  floating hex, no rail stub hanging in the air, no missing end element?
  **Write down exactly what you see, and grab a screenshot.**

**Trigger — F45 (broken-track salvage):**
4. Aim the camera at a track hex and run `CheatMeteors("single")` until a meteor
   breaks a track element (a repair site appears on the track).
5. Run `SMRTest.ReportBrokenTrack` → note the "non-numeric node_idx" count.
6. Try to **salvage the broken element** (click it, and try the infopanel Salvage button).

- **BROKEN looks like:** the salvage click does absolutely nothing — no countdown, no
  feedback, the damaged track is permanently undeletable; the report shows sites with a
  non-numeric `node_idx`.
- **FIXED looks like:** report shows **0** bad sites, and the broken element salvages
  like any other.

`Result (F44 trim):` PASSs

`Result (F44 curve visual):` PASS

> Re-run 2026-07-26 on the sol-36 save (rework a38cbf2 + F47 composition d3fbf54;
> the load's orphan sweep removed the 40 debris elements from the first attempt):
> repeated build → salvage → rebuild cycles on BOTH straight and curve-ended
> tracks, multiple times — trim takes only the clicked segment, the train
> survives and keeps running, no immune debris, no warning spam, curve visuals
> clean. **Metals refund stockpile confirmed on partial salvage** (the F47
> partial-refund half observed live). First-attempt FAIL notes preserved in git
> history (09af088 era) — that state is what the orphan sweep cleans.

`Result (F45 broken salvage):` PASS — 2026-07-26: forced meteor broke the track
(repair site, "Outside Drone Commander range" so nothing repaired it);
`SMRTest.ReportBrokenTrack` printed **7 track repair site(s); 0 with a
non-numeric node_idx**; the broken element salvaged instantly and the split
completed cleanly — proper end pillars both sides, no debris, no errors (the
same click that no-op'd in the shipped game and crashed the split pre-seed-repair).

> F45 retry procedure (2026-07-26 — the first attempt crashed mid-split on the
> shipped blind-seed bug, repaired same day; the fix is active from your next
> game launch):
> 1. Load the save — the sweep line should report BOTH counts:
>    `removed N orphaned track element(s) and M dead track-list entr(y/ies)`.
> 2. Turn the Drone Hub OFF (so repairs don't race you).
> 3. Select a mid-track hex (away from station/dome), console:
>    `CreateGameTimeThread(function() MeteorsDisaster(GetMeteorsDescr(), "single", SelectedObj:GetPos(), "force") end)`
> 4. When the wrench/repair site appears: `SMRTest.ReportBrokenTrack` → want **0**
>    non-numeric node_idx.
> 5. Salvage the broken element — should salvage instantly like any piece, with a
>    refund drop. Turn the Drone Hub back on when done.

---

## PT-04 — Rocket drone churn · covers **F50**

> **Setup corrected 2026-07-26.** An earlier version of this test said to put the
> Drone Hub "far from the rocket, at the far edge of the buildable area". That does
> not work and would have produced a false PASS: drones only ever service what is
> **inside** their command centre's `work_radius` (`const.CommandCenterDefaultRadius`
> = **35 hexes**, +15 with Signal Boosters; the gate is
> `HexAxialDistance(center, pt) <= center.work_radius`, `DroneControl.lua:1019`).
> A rocket outside that circle gets **no drones at all**, so nothing is ever kicked and
> the log stays empty whether the fix is present or not. The rocket brings none of its
> own either — `starting_drones = 0` (`UniversalRocket.lua:74`). The maximum drone trip
> is therefore capped by the hub radius, and no placement can extend it.
>
> The test does not need a long trip. The kick fires on the hourly update against
> **every drone that happens to be walking to the rocket at that moment**, so what you
> actually need is *drones in transit when the hour ticks* — which means many drones and
> a decent distance **within** the circle, not a long one outside it.

**Setup:** SAVE-A with a **landed rocket carrying cargo to unload**, and a **Drone Hub
positioned so the rocket sits near the outer edge of the hub's service circle but
clearly inside it** (the circle is drawn while you place the hub). Give the hub a full
complement of drones — the more that are in transit at any moment, the more obvious the
effect. Make sure **no second hub** also covers the rocket, or its drones will quietly
take over the hauling and mask the kicks.

**Precondition check — do this before you start, or the result is meaningless:**
watch for a few seconds and confirm drones really are walking to and from the rocket. If
nothing moves, the rocket is outside the hub's radius and the test proves nothing.

> **Do you need a Drone Hub Extender?** No. It does work — an extender is a `DroneNode`,
> so a rocket inside *its* circle connects fine, and `GetCommandCenter()` chains up to the
> uplink hub (`DroneHubExtender.lua:155-159`), which is what still owns the drones and
> still gets the `OnRemoveBuilding` call. So the bug reproduces through one. It just buys
> you nothing here and adds two ways to get a silent false PASS: an extender with no power
> or an out-of-range uplink returns no command centre at all
> (`GetWorkNotPossibleReason`, `:192-201`), and extenders carry their own recharge
> stations, so drones drift out to them and the extra walking distance you built it for
> partly evaporates. Skip it unless you already have one — and if you do use one, make
> sure it is linked to **the hub you are watching**, not a second one.

**Trigger:**
```
SMRTest.Log.DroneChurn(true)
```
Let 3+ game hours pass with drones actively hauling from the rocket. Watch the console.
The logger only prints when it has something to report, so an empty log is a real
result. Ultra speed is fine once the drones are en route.

- **BROKEN looks like:** once per game hour, a batch of drones heading for the rocket
  stops, turns around and goes idle, and the log gets a
  `DroneControl:OnRemoveBuilding(...) -> N drone(s) sent to Idle` line. Unloading still
  limps along — **do not read slow progress as a PASS.** The hourly line is the finding.
  (The extreme case, where the haul can never finish at all, needs a trip longer than a
  game hour; whether the 35-hex cap allows that is a question for the in-game clock, not
  for this test.)
- **FIXED looks like:** **no** `-> N drone(s) sent to Idle` lines naming the rocket, for
  the whole run; drones keep walking and the cargo moves without interruption.

> Lines naming some *other* building are not this bug — the fix only suppresses the
> rocket's hourly cargo-request churn. Check the class name the logger prints.

Turn the logger off afterwards.

`Result:` __________________Passed no issues, smooth unloading and unloading, no logs___________________________

---

## PT-05 — Milestone completion popup · covers **F05**

**Setup:** **A new game started with the `NoTerraforming` game rule** (this is what
guarantees hidden-but-uncompleted milestones — 9 of them). One dome, minimal colony.
This is a 5-minute throwaway save; you do not need SAVE-A for it.

**Trigger:** complete the visible milestones from the console, leaving one for last:
```
CompleteMilestone("ScanAnomaly", true)
CompleteMilestone("ConstructDome", true)
CompleteMilestone("FirstHumanOnMars", true)
```
…and so on through the visible list (ids are in `Data/Milestone.lua`: `ScanAnomaly`,
`ReturnRocket`, `FindWater`, `ConstructDome`, `FirstHumanOnMars`, `Martianborn`,
`ProduceFood`, `ResearchBreakthrough`, `SponsorGoals`, `ScanAllSectors`,
`Population100`, …). Complete the **last** one and watch.

- **BROKEN looks like:** the final milestone silently does nothing — no celebration
  popup — and the log shows an "attempt to perform arithmetic on a nil value" error.
- **FIXED looks like:** the "all milestones completed" popup appears, and the log is
  clean.

`Result:` PASS — 2026-07-26. Run on the live Paradox playtest save rather than a
fresh NoTerraforming throwaway — valid fixture regardless: 27 presets, 18 shown,
so the 9 terraforming milestones were hidden-but-uncompleted (exactly the F05
crash condition). Setup wrinkle worth keeping: ScanAnomaly had been FAILED by
the rival colony ("Scan an Anomaly — Japan", red X) which permanently blocks
the popup, and `CompleteMilestone` refuses failed milestones — recovered from
console with `MilestoneCompleted.ScanAnomaly = nil` then re-completing it. On
the final completion (18/18, score 83,420) the **"A dream fulfilled" popup
appeared immediately** (screenshots taken); log Mars.exe-20260726-15.03.01 has
**zero [LUA ERROR]** — no "arithmetic on a nil value" anywhere.

---

## PT-06 — Five-star tourist applicant jump · covers **F08**

**Setup:** SAVE-A. You need a tourist-carrying rocket to **depart**. Build a Hotel/
Spacebar so tourists arrive; ensure high Comfort so the group rates 5 stars (open the
infopanel and check the rating before departure). `CheatToggleInfopanelCheats()` gives
you per-building levers if you need to force a state.

**Trigger:**
1. Before the tourist rocket departs, note the **applicant pool size** (Colony
   Control Center → Applicants, or `#UIColony.applicants_pool`).
2. Let the rocket depart. Note the pool again.
3. Repeat once with a **deliberately bad (1-star)** tourist group (turn off the Hotel's
   power / let comfort tank).

- **BROKEN looks like:** the miserable 1-star tourist group brings you *more* new
  applicants than the delighted 5-star group — the reward is upside-down.
- **FIXED looks like:** the 5-star departure gives a clearly bigger applicant bump than
  the 1-star one.

`Result:` PASS — 2026-07-27 (user, two departures, screenshots):
**5★ half (2026-07-27 early):** 10 pampered tourists paid at Earth arrival
"Tourism: $544.5 M, **+23 applicants**" (2.3/head = the top reward tier).
**Tanked half (same day, later):** a **25-tourist** group (size clarified by
the user after the initial record) landed into a stripped dome (hotels +
services off) — homeless, Stressed Out; several fled Earthsick at sol 1-5
("Leaving the Colony" — early leavers ARE counted: the reward walks every
boarded Tourist at departure, `RocketBase.lua:815-855`, no sols/reason
filter). Payout: "Tourism: **$94.5 M, +7 applicants**" —
**per head that is 0.28 applicants/$3.78M vs the 5★ group's 2.3/$54.45M: an
8× applicant split, the clear 5★ > tanked result the test demands.**
Interpretation notes: with sanity/comfort in the red every head is capped at
the 2★ tier (`HolidayStatCapRating` = 2 whenever any of health/sanity/comfort
< `HolidayCapThreshold` 30, `HolidayRating.lua:43-55`); $3.78M/head sits
between the 1★ $2M and 2★ $7M payouts = a 1★/2★ mixture (the $0.5M tail
suggests a small extra contributor in the Tourism funding bucket — not
decomposable from the notification alone). The applicant rate is itself fix
evidence: a mostly-1★ group under the CORRECTED 40% roll expects ~10±2 from
25 (7 observed, in band); under the shipped INVERTED roll (~59% at 1★) it
would expect ~15 — the observed 7 is ~3σ below that, inconsistent with the
broken math.
Side observations, both by-design/cosmetic: the infobar "Cycle overstaying
Tourists" button silently no-ops when the sol-10+ bucket is empty (list from
`sols >= TouristSolsOnMarsMax` only, `Infobar.lua:452-466`; cycles the current
map only), and the sols-based tooltip buckets label early-leavers "Enjoying
their holiday (sol 1-5)" while they walk to the rocket.

---

## PT-07 — Low-food warning · covers **F12**

**Setup:** SAVE-A with a colony that actually **consumes food** (colonists eating,
farms producing, at least one full sol of consumption history — the check reads
"consumed yesterday", `Lua/ResourceTracking.lua:228`). Threshold is 3 sols
(`const.MinDaysFoodSupplyBeforeNotification = 3`, `Lua/_GameConst.lua:11`).

**Trigger:** drain the Food stock below ~3 sols of consumption — salvage the food
depot contents, or dump food by demolishing storage. Then wait ≤1 game hour at
`SetGameSpeedState("ultra")`.

Repeat for a maintenance resource (Machine Parts): let stock drop under 3 sols of
maintenance consumption.

- **BROKEN looks like:** food (and Machine Parts) run down to nothing with **no warning
  at all** — the "insufficient resources" notification simply never fires for them.
- **FIXED looks like:** the low-supply notification appears within a game hour of
  crossing the 3-sol line, naming Food (and Machine Parts), with a sane hours estimate.
- **Also check:** while the warning is active, does it sit there quietly, or does it
  visibly flicker / replay its alert sound every game hour? (The F12 rework was
  specifically about killing that churn.) **The warning should be steady.**

> First run 2026-07-27 (Stargazer save): the Food warning FIRED correctly
> ("2 Sols, 22h" — that half works) but the steadiness check FAILED — user:
> "I get a flash and a voice over the says 'warning insufficient resources' on
> repeat every hour or so". Diagnosed live via console instrumentation to a
> "Food"-key collision between the maintenance loop and the food branch inside
> the fixed updater (full record on the F12 entry); repaired same day in
> Fix_LowStorageWarning.lua. **Re-run this test from scratch on the repaired
> build (next game launch): expect the warning to fire AND sit steady, plus the
> Machine Parts half.**

`Result:` PASS — 2026-07-27, re-run on the repaired build (post-35f7246).
**Food half:** warning fired at the 3-sol crossing, announced exactly ONCE, then
sat steady with the warning active for "maybe at least one full sol" (user; the
old churn repeated hourly, so 24+ quiet hours is decisive); cleared
**automatically and silently** on an organic recovery (food supply pod fired +
farms turned back on — no cheat fill); a re-drain re-announced exactly once.
**Machine Parts half:** maintenance consumption generated via forced turbine
malfunctions, drained under 3 sols → warning fired naming Machine Parts
("Less than 1 Sols, 12h of storage remain"), sane figure, **no repeats**;
refilled via supply pods → the Machine Parts warning also **cleared
automatically and silently** (both branches confirmed on the recovery side).
Setup discoveries recorded in the command table: infopanel cheat buttons
no-op on retail without `Platform.cheats = true`, and their presses queue on
the game-time sync — they look dead while PAUSED and fire on unpause (the
`ObjCheat <method>` console print is the tell).

---

## PT-08 — Command Center resource rows · covers **F13**

**Setup:** SAVE-A with a real economy (some Metals, Concrete, Polymers, Food, Water,
Electronics, Machine Parts, Rare Metals in stock).

**Trigger:** `OpenCommandCenter()` (or the in-game button). Go to the resource
overview and read every resource row.

- **BROKEN looks like:** the resource rows show icons and labels but the **numbers are
  blank** — you cannot tell how much of anything you have from this screen.
- **FIXED looks like:** all 11 resource rows show numbers, and those numbers match what
  the HUD/resource overview says.

`Result:` PASS — 2026-07-27 (Stargazer save, sol 33, 101 colonists). All 11 rows
that render blank in the shipped game showed numbers: Metals 424, Concrete 592,
Food 117, Rare Metals 240, Polymers 221, Machine Parts 407, Fuel 408,
Electronics 341, Seeds 60, Exotic Minerals 60, Waste Rock 921. Cross-checked
against the HUD bar moments later: six exact matches (424 / 240 / 60 / 221 /
408 / 60), the rest off by single digits in consuming directions (Food 117→104,
Waste Rock 921→903 etc.) — live-sim drift between screenshots, same source
values. Screenshots of both screens taken.

---

## PT-11 — Cave-ins under the No Disasters rule · covers **F01**

**Setup:** SAVE-B, standing on the underground map. Confirm all three
preconditions (bare expressions, one line at a time):
```
IsGameRuleActive("NoDisasters")
CurrentMap.mapdata.Environment
SMRFixPack.fixes.CaveInsNoDisasters.status
```
Expect `true` / `Underground` / `active`. If the rule is not active the test is
void — it can only be set at new-game. Underground *buildings* are NOT required:
`FindEpicentre` is `GetRandomPassable` → `GetPlayableAreaNearby`
(`Marsquake.lua:237-241`), so quakes fire on a bare map and their rubble lands
near a random epicentre, not near your colony. Watching a dome for damage is the
wrong detector.

**Detector — an objective count, not eyes** (events at ultra speed are easy to
miss). Take this before, between and after every leg:
```
*r local l = CurrentMap:MapGet("map", "CaveInRubble") or {} ConsolePrint("rubble: " .. #l)
```

**Trigger (console):**
```
g_Consts.MarsquakeSpawnTime = 1
g_Consts.MarsquakeRandomTime = 1
RestartPeriodicRepeatThread("UndergroundMarsquake", CurrentMap)
IsValidThread(CurrentMap.RepeatThreads.UndergroundMarsquake)
SetGameSpeedState("ultra")
*g Sleep(20 * const.HourDuration) ConsolePrint("20h elapsed")
```
**The restart is mandatory, not optional** — see the "Compressing a scheduler
with `g_Consts`" rule in the checklist's ground rules. Without it the thread is
still asleep on the default 384+96-hour (16-sol) interval and 20 hours proves
nothing. `IsValidThread` must print `true`.

Then save, reload, **re-run the restart and the IsValidThread check** (repeat
threads are persistable, so the reload restores the old sleep), and let another
20 pass. Finish with the positive control:
```
CheatTriggerUndergroundMarsquake()
```

- **BROKEN looks like:** the rubble count climbing across either leg; cave-in
  notifications and camera shakes during the watch.
- **FIXED looks like:** the count frozen across both legs, then jumping on the
  control — proving the scheduler really was ticking and being suppressed.

> Expected and **not** a failure: `CheatTriggerUndergroundMarsquake()` still
> fires a quake. It bypasses the scheduler on purpose; the fix gates the
> scheduler only (`Lua/Marsquake.lua:292`). That is exactly why it makes a
> sound positive control.

`Result:` **PASS — 2026-07-29.** Preconditions verified live: `true` /
`Underground` / `active`. Baseline **27** rubble. Consts compressed to 1, thread
re-armed, `IsValidThread` → `true`. **Leg 1:** 20 game hours at ultra → **27**,
unchanged. Save + reload; `g_Consts.MarsquakeSpawnTime` read back `1` (GameVar
survived), rule still `true`, thread re-armed and valid, count still **27**.
**Leg 2:** another 20 game hours → then the control
`CheatTriggerUndergroundMarsquake()` → **36**.

*Why that closes it:* +9 is exactly one quake's worth — `rubble_count = 10`
(`Marsquake.lua:235`) with one `FindCaveInLocation` returning nil, which is
normal. So at most ONE quake occurred across the whole run, and the control
fired it. Had leg 2's ~10-20 compressed ticks produced even a single scheduler
quake the count would sit near 45; an unfixed pack would be in the hundreds.
Leg 2 therefore contributed zero, and the control proves the counter moves when
a quake really happens — the two 27s are the fix suppressing live ticks, not a
dead observation method. → **F01 `tested`.**

*Test defect found and repaired by running it:* the original procedure set the
consts and waited, which cannot work — a `MapGameTimeRepeat` computes its next
interval at the end of each tick, so the in-flight sleep still ran on the
384+96-hour defaults. Followed literally, the old text would have returned a
false PASS for any fix state. The restart step, the objective counter and the
positive control are all new, and the general rule is now in the ground rules.

## PT-12 — Shuttle-cache emigration · covers **F51**

**Setup:** SAVE-C. Dome **A** has homeless colonists and no spare housing; dome **B**
is **far away (out of walking range, no passage to A)** with plenty of free housing.
**No Shuttle Hub anywhere.** Let at least one full emigration evaluation cycle run at
ultra speed so the "no transport available" verdict gets cached — you should see
colonists stay homeless in A.

**Trigger:** now build and **fuel** a Shuttle Hub (`CheatCompleteAllConstructions()`,
`CheatFillAllStorages()`), then wait 1–2 game hours at ultra speed.

- **BROKEN looks like:** you build a Shuttle Hub, shuttles fly, and the homeless
  colonists in dome A *still* never move to the empty houses in dome B — the game
  decided once that there was no transport and never re-checked.
- **FIXED looks like:** within a cycle or two of the hub going live, homeless colonists
  start emigrating to dome B and the Homeless count drops.

`Result:` PASS — 2026-07-26. Run on the live playtest colony (three domes) rather
than SAVE-C; DomeBasic#1506 was the isolated dome. Cache dump BEFORE the hub:
every #1506 pair `mode=false, cached with shuttles=false` — the "no transport"
verdict confirmed cached. Built + fuelled the Shuttle Hub (no station/elevator
changes mid-test, so no wholesale cache flush could fake the pass). Dump AFTER:
every #1506 pair flipped to `mode=shuttle, cached with shuttles=true`, and the
user's observation: "They have all transported out from what I can tell" — the
homeless emigrated. The smr_shuttles stamp mismatch forcing the recompute is
the fix's mechanism working as designed; screenshots of both dumps taken.

---

## PT-13 — Vacuum walk routing · covers **F52**

**Setup:** SAVE-C — domes A and B ~350 m apart (**under** the 400 m
`const.ColonistMaxDomeWalkDist`, `Lua/_GameConst.lua:133`) **joined by a passage**,
with the direct outdoor route also open. Atmosphere must be **non-breathable**: check
`GetTerraformParamPct("Atmosphere")` is low; if you terraformed by accident, use
`SetTerraformParamPct("Atmosphere", 5)`.

**Trigger:** force a colonist to move between the domes — set dome A to not accept
residents / turn off its life support briefly, or use a workplace in B. Then **follow a
colonist with the camera** for the whole trip.

- **BROKEN looks like:** the colonist strolls out the airlock and hikes across open
  vacuum between the domes, with the suffocation timer ticking — and some of them die
  en route.
- **FIXED looks like:** the colonist uses the **passage** (goes through the tube, no
  outdoor stretch) — or waits/refuses rather than walking exposed.

> Known partial: if there is **no** passage route at all, an outdoor walk is still
> allowed by design (refusing it would strand colonists on shuttle-less maps). Only the
> "passage exists but is ignored" case is a FAIL.

`Result:` PASS — 2026-07-26 (user, confirmed 2026-07-27): "I watched them do it
in a passage and I destroyed the passage and watched them do a space walk to
make sure both worked." Both halves observed on the live colony: with the
passage standing, the colonist routed through it in vacuum (the F52 fix); with
the passage destroyed, the surface walk resumed — the designed no-passage
fallback (kept so shuttle-less maps cannot strand colonists), NOT a failure.

---

## PT-14 — Cross-dome shopping with migration off · covers **F61**

**Setup:** SAVE-C — dome **A** (residents, no shop/diner) connected by **passage** to
dome **B** (has the shop/diner/university). Both domes healthy.

**Trigger:** on dome **A**, turn **"Accept Colonists" OFF** (the migration toggle in the
dome infopanel — `Community:ToggleAcceptColonists`, `Lua/Buildings/Community.lua:106`).
Leave dome B's toggle alone. Run 1–2 sols at ultra speed and watch A's residents.

- **BROKEN looks like:** switching off *migration* on the home dome also silently stops
  its residents from shopping, working or training in the connected dome — comfort and
  service satisfaction slide with no explanation.
- **FIXED looks like:** residents of A keep walking through the passage to shop/work/
  train in B; only actual **immigration into A** is blocked.

Also confirm dome **B** with its own toggle off still correctly **refuses** incoming
colonists — the fix must not open the wrong gate.

`Result:` DONE 2026-07-27 — **neither BROKEN nor FIXED: the test's premise is
falsified.** Tester (toggle off on a live dome, fix pack active, screenshot on
file): "As soon as I turned off accept colonists no one could work there[,]
people slow[ly] left jobs and services as they finished shifts, no one could
enter or leave anymore." That full lockdown is the game's DOCUMENTED design,
not a defect: the toggle's OFF state is titled **"Quarantined"** (visible in
the tester's screenshot and in `Data/XDef/sectionDome.lua:185`, T8736) and its
rollover says outright "Colonists are not allowed to enter or leave quarantined
Domes" (T365). The engine enforces the same reading in
`Colonist:FindEmigrationDome` ("quarantine, no one enters or leaves",
`Colonist.lua:2632-2634`) and in the target-side gate the fix never touched
(`Dome.lua:2881`). The migration-independent commute controls PT-14 was looking
for exist as their own toggles — "Use Passages for work" /
"Use Passages for services" (`allow_work_in_connected` /
`allow_service_in_connected`) — and the dome trait filter covers
"stop move-ins without a lockdown" (its tooltip even says setting it removes a
quarantine, T363). **Resolution (user decision, same day): F61 CLOSED `wontfix`,
fix deletion staged, and the underlying community ask filed as D03
(`Opt_ResidencyControl` — a NEW "closed to new residents" dome policy that
leaves quarantine intact).** See the F61 + D03 BUGS.md entries.

---

## PT-24 — Universities after Extractor AI · covers **F36**

**Setup:** SAVE-A. You need **Metals Extractors on the map** (not Mines — the tech
targets `MetalsExtractor` / `PreciousMetalsExtractor`) and a **Martian University**.

1. `CheatMapExplore("deep scanned")`, build 2–3 **Metals Extractors** on deposits and
   `CheatCompleteAllConstructions()`. Leave them **staffed and working** for a sol so
   they are `ui_working`.
2. Build a **Martian University**, set specialization to **Auto** and training policy
   to **"train as needed"**. Feed it unspecialized colonists (`CheatSpawnNColonists(20)`).
3. Read the university's infopanel **needed-specializations list** and note it.
4. Now research the **Extractor AI** breakthrough:
   `UIColony:SetTechResearched("ExtractorAI")` — **NOT `CheatResearchAll()`**, which
   skips undiscovered breakthroughs (corrected 2026-07-27, found live in this test;
   see the command-table row). Confirm afterwards that the
   extractors show **Automation** in their infopanel and keep working with their
   workers removed.
5. Re-read the university's needed-specializations list, then run 3–4 sols at
   `SetGameSpeedState("ultra")` and watch what it graduates.

- **BROKEN looks like:** after Extractor AI the extractors run themselves, but the
  university's list still shows a large **geologist** demand (4 per shift per
  extractor) and "auto" keeps graduating geologists — while the specialists you are
  actually short of never get trained.
- **FIXED looks like:** geologist demand from the automated extractors **drops out of
  the list** the moment the tech lands, and "auto" starts training whatever the colony
  is genuinely short of. Manned workplaces (medics for the Medical Centre, botanists
  for farms, and geologists for ordinary **Mines**, which are not automated) still
  appear in the list normally.

> Sanity check on over-reach: with Extractor AI researched, an **unstaffed** extractor
> must NOT raise a "needs workers" warning, and a Mine (no automation) must still ask
> for geologists.

`Result (geologist demand gone?):` PASS — 2026-07-27 (user, screenshots both ways):
before ExtractorAI the university's list read **Geologists 11** (Engineers 47,
Medics 5, Officers 5); the user reloaded a pre-tech save to capture it after the
post-tech reading showed **Geologists 0 with every other row identical**. The
delta is exactly the automated extractors' posts dropping out. Bonus: the fix
pack was active in the before-save, so the fix provably does NOT over-exclude —
non-automated extractors still contribute geologist demand (the 11). Setup note:
`CheatResearchAll()` does NOT grant undiscovered breakthroughs — the direct
grant `UIColony:SetTechResearched("ExtractorAI")` was used (command table
corrected same day).

`Result (other specialists still trained?):` PASS — 2026-07-27 (user, multiple
`CheatCompleteTraining` rounds across two universities; tallies read from the
universities' own `trained_specialists` records, captured in log
Mars.exe-20260727-15.19.26 at Lua 2:35): **38 engineers + 2 medics, ZERO
geologists** — auto training follows the colony's genuine shortages (engineers
topped demand at 47; the two medic picks show the auto choice moving when the
per-moment demand ordering shifted). Both halves PASS → F36 `tested`.

---

## PT-26 — Second Artificial Sun · covers **F39**

**Setup:** SAVE-A with `MultiCheat()` + `CheatAddFunding(500000000)` (the Artificial
Sun is a late-game building and needs Water).

**Trigger:**
1. Build **Artificial Sun #1** somewhere, and a Solar Panel next to it.
   `CheatCompleteAllConstructions()`. Confirm the panel's infopanel shows the
   Artificial Sun bonus (its power output is higher than a panel out in the dark,
   and it keeps producing at night).
2. Build **Artificial Sun #2** far away, out of range of everything.
3. Now build **new Solar Panels around sun #2** and complete them. **Order matters** —
   the panels must be built *after* the sun.
4. Compare a panel next to sun #2 with a panel next to sun #1, and with one in
   neither's range. Night is the clearest comparison.

- **BROKEN looks like:** the panels around sun #2 behave as if there were no sun at
  all — no bonus, no night production — while the identical panels around sun #1 are
  fine. (Panels that were *already standing* when sun #2 was built do work; that
  direction was never broken.)
- **FIXED looks like:** panels around sun #2 produce exactly like panels around sun #1.

**Existing-save check:** if you have a save that already has this problem, load it with
the pack enabled and look for `[CommunityFixPack] SecondArtificialSun: reconnected N
solar panel(s)` in the log — those panels should start producing immediately.

`Result:` RESOLVED-UNRUNNABLE — 2026-07-27 (user): **the unmodded game cannot
build a second Artificial Sun.** The template is a `build_once` wonder enforced
colony-wide across all maps including construction sites (`Building.lua:3691`,
`BuildMenu.lua:711-719`); with sun #1 standing the build menu refuses with "You
can build this building only once" (screenshot on file) — the tester raised the
premise question after igniting sun #1. F39's fix is latent hardening in
vanilla. **Single-sun baseline banked while investigating:** panels beside the
lit sun keep producing at night with a −21% atmospheric effect (small panel 3.6
vs 4 daylight, large 9 vs 10) — reference numbers for the D04 module's future
playtest. **Resolution (user decision, same day): D04 `Opt_MultipleSuns`** —
opt-in module that lifts the build limit AND carries the F39 binding fix, so
the condition the fix needs is provided by the pack itself. Console fact
verified live: toggling `BuildingTemplates.ArtificialSun.build_once` is read by
the build menu immediately (the D04 patch mechanism).

---

## PT-34 — Shuttle Hub switched off · covers **F54**

The probe proves the predicate; only play shows what the colony then does with
the answer.

**Setup:** SAVE-C (the two-dome colony) with a **Shuttle Hub built, fuelled and
holding at least one shuttle** — PT-12 already has you build one, so run this
straight after it. Dome A has residents and no spare housing, dome B has free
housing.

**Trigger:**
1. With the hub **on**, confirm shuttle transport works — the colonist is picked
   up and moved.
2. Now **switch every Shuttle Hub off** from its infopanel.
3. Create the same demand again (make a colonist homeless in A with housing only
   in B). Let a few sols pass.

- **BROKEN looks like:** the colony still behaves as though shuttles were
  available — the colonist is marked for a shuttle ride and stands on a pickup
  spot outside, waiting indefinitely for a shuttle that no switched-off hub will
  ever launch.
- **FIXED looks like:** with all hubs off, the colony treats shuttle transport as
  unavailable — the colonist stays inside / uses a walkable or passage route, or
  simply stays put, rather than waiting outdoors.

**Trigger — not over-broad:**
4. Switch a hub back **on** and confirm shuttle rides resume normally.

> Second, harder-to-see effect: with hubs off, dome-to-dome **walkability**
> (`Dome.lua:256-259`) is also re-evaluated. Watch for colonists suddenly using
> passages they previously ignored — that is the fix working, not a new bug.

`Result (all hubs off):` PASS — 2026-07-27 (Stargazer save, reusing the PT-12
infrastructure). Hubs switched off, an apartment destroyed to create homeless
with free housing only in shuttle-reachable domes (no passage/tunnel access):
"they just got the homeless tag and did not go outside, they just stayed put" —
nobody committed to a ride or stood at an outdoor pickup spot. Under the
shipped predicate the hub's mere existence would have marooned them outside.

`Result (hub back on):` PASS — 2026-07-27: "once I started shuttle hub up
again people started moving out" — rides resumed within a cycle, homeless
emigrated to the free housing. Not over-broad: re-enabled hubs re-qualify
immediately.

---

## PT-36 — F10 retirement check · confirms **F10** is safe to close `wontfix`

F10 (faction funding conditions "always error") is **retiring**: the QA A/B baseline
proved the shipped `GetLastSolsFundingByType` tolerates its `pairs(nil)` hours in this
engine, so the fix repairs nothing. The fix is already commented out of `metadata.lua`.
This check confirms that finding on a **real** save's organic income history — the one
thing the synthetic baseline could not cover — and is the gate for closing the entry.

**Setup:** your longest-running real save (SAVE-B or better; a donated community save
is ideal). Fix pack loaded as normal — the retired fix is simply absent, so the
console drives the SHIPPED function. Two minutes.

**Trigger:**
1. Open the console (Enter / Alt-Shift-C — the Test Kit enables it) and run, one at
   a time:
   `UIColony.funds:GetLastSolsFundingByType(10, "Exports")`
   `UIColony.funds:GetLastSolsFundingByType(10, "Tourist Profits")`
   `UIColony.funds:GetLastSolsFundingByType(10, "Exports + Tourist Profits")`
2. Play (or fast-forward) a few game hours with **no export/tourism income**, then
   run all three again — this maximises the nil per-hour entries the old entry
   claimed would crash.
3. Skim the session log for any new `[LUA ERROR]` mentioning `Funding.lua`.

- **RETIREMENT CONFIRMED looks like:** every call prints a **number** (0 is fine, and
  expected with no recent income) and the log stays clean → report PASS; F10 closes
  as `wontfix` and `Fix_FactionFundingCheck.lua` is deleted from the repo.
- **ROLLBACK looks like:** any call errors (`pairs`/nil in `Funding.lua:110`) → report
  FAIL with the exact error text and your save's sol count; re-add the
  `Fix_FactionFundingCheck.lua` line in `metadata.lua` and the F10 entry reopens.
- Bonus, if the save's sponsor has faction goals: open the faction/goals screen and
  confirm the "made profits from exports/tourism in the last 10 sols" conditions
  render and evaluate (either state) without errors.

`Result:` PASS — 2026-07-27, Stargazer save (sol 45+, long-idled at high speed).
All three calls printed **0** with no error text and no `Funding.lua` entries in
the log — and this history was maximally hostile: the colony had run past the
12-sol retention ring (`Funding.lua:86` prunes hourly entries), so nearly every
hour the loop touched was nil. The shipped `pairs(nil)` tolerance holds on
organic save state, matching the synthetic A/B baseline. **F10 CLOSED `wontfix`;
`Fix_FactionFundingCheck.lua` deleted; commented metadata line removed** (both
restorable from git history). The TestKit `FactionFundingCheck` probe stays as
a canary on the shipped function — expected A/B numbers unchanged (it is the
baseline's "1 PASS").
**Both-ways bonus (same day, later):** after a 10-tourist group departed and
paid out at Earth arrival ("Tourism: $544.5 M, +23 applicants"),
`GetLastSolsFundingByType(10, "Tourist Profits")` printed **544500000** — the
shipped function reads real NONZERO income correctly too, not just the
nil-tolerant zero case. Retirement evidence complete in both directions.

---

## PT-38 — Dismissed "Building Not Working" cadence · gates **D02** (planned opt-in)

Nothing to fix here — this measures the SHIPPED behavior that D02 (per-building
acknowledged warnings, planned opt-in module) is designed to answer. F32 closed
`wontfix` because the game hotfixed the actual defect; the claim left to verify is
that a permanently broken building re-nags every **2 minutes of real time** after
each dismissal.

**Setup:** any save. Make one building permanently not-working — cut its power and
leave it, or use a building that genuinely cannot recover (a lake-entombed one, per
F30, is the archetype). Wall clock or phone timer handy; leave game speed at normal.

**Trigger:**
1. Wait for the "Building Not Working" notification, then **dismiss** it. Note the
   real-world time.
2. Do not fix the building. Watch for the notification to return.
3. When it returns, dismiss again and time the second interval too.
4. Bonus: while inside the quiet window, break a SECOND building (cut its power).
   Note whether its warning is also swallowed until the window ends — that is the
   per-category (not per-building) suppression D02 also addresses.

- **EXPECTED (design confirmed):** the warning returns ~2 real minutes after each
  dismissal, forever, and a second breakage inside the window stays silent until
  the window closes. Record the measured intervals → D02 proceeds as specced.
- **SURPRISE looks like:** it stays away much longer / for good (then D02 is
  unnecessary — record what actually happened), or it returns in seconds (then the
  F32 close needs a re-read — record the exact timing).

`Result (interval 1 / interval 2):` MEASURED, with a premise correction —
2026-07-27, Stargazer save; fixture = a Triboelectric Scrubber + a Concrete
Extractor, both maintenance-failed OUT of drone repair range (genuinely
unrecoverable). By feel first: "slightly longer than 2 mins" at normal speed,
then "~45 seconds" at higher speed — the speed-dependence prompted console
timestamp wrappers (game + real stamps on AddNotification/RemoveNotification).
Three dismissal→return pairs: **148,805 / 161,755 / 132,056 game-ms** — each
exactly **120,000 game-ms (4 game hours) + time to the next re-add attempt** —
with every in-window attempt printing `attempt BLOCKED (suppressed)` and the
first post-expiry attempt creating. Real-time deltas ~30/32/26 s at the user's
accelerated speed. **The window is GAME time, not wall-clock** (the caution
above and D02's premise were corrected): `GetTime()` = `GameTime()` because the
preset leaves `GameTime` at its true default (`NotificationPreset.lua:65-66,
:126-128`). At ultra the re-nag returns every few REAL seconds — D02's case is
stronger than premised. Also: pausing freezes the window and the re-add (both
game-time), and the infopanel cheat-button/pause gotchas found en route are in
the command table.

`Result (second breakage hidden in window?):` YES for the same id, NO across
ids — 2026-07-27. Cross-id: a happy accident ran fuel-starvation warnings for
the Shuttle Hub + factories concurrently; dismissing those never touched the
"Building Not Working" cycle ("the issues are tracked separately" — user) —
suppression is stored per notification id (`SuppressedNotifications[id]`).
Same-id: both broken buildings rode ONE notification, and the wrapper showed
EVERY re-add attempt for the id blocked during the window — a new same-id
breakage inside the window is swallowed with it (`AddNotification`
early-returns while suppressed, `Notifications.lua:52-54`). Exactly the
per-category gap Opt_AcknowledgedWarnings addresses → **D02 build proceeds,
with the corrected 4-game-hour spec.**

---

## PT-39 — RC Transport vs. a visiting rocket · covers **F74**

Probes prove the guard refuses a trade rocket; only play can show the cursor and
the order behave as they should, and that nothing ELSE the RC Transport does got
caught by the same net.

**Setup:** a save where a trade rocket or a refugee rocket is landed (rival-colony
trade offer, or the refugee story event). Have an RC Transport with some cargo
aboard and some free space, parked near it.

**Steps:**
1. Select the RC Transport and hover the cursor over the landed **trade/refugee**
   rocket, both in plain move mode and with the Load and Unload interaction modes.
   - **EXPECTED:** no "Load Resource" / "Unload Resource" prompt appears, and
     clicking does not send the rover to the rocket (it should read as ordinary
     terrain — a move order, or nothing).
   - **SURPRISE looks like:** the prompt still appears, or the rover drives over
     and starts a transfer.
2. Try to start a **transport route** whose source or destination is that rocket.
   - **EXPECTED:** the rocket cannot be picked as either end.
3. **Control test — this must still work.** Hover the same RC Transport over a
   normal **player** rocket or asteroid lander that is landed with cargo, and over
   an ordinary Universal Storage Depot.
   - **EXPECTED:** Load/Unload prompts appear as before and the transfer runs.
     If this broke, the fix is over-broad — report it, it is worse than the bug.
   - **CAUTION (2026-07-27, F76 — vanilla, NOT the pack):** clicking a depot in
     Load mode opens a resource-picker dialog that on scaled/wide displays
     renders as a giant detached hex far from the cursor and cannot be clicked
     (clicks fall through to the map). The depot half of this control was run
     live and is BLOCKED on F76 — the prompt appears (guard not over-broad ✓),
     the picker opens (proven by instrumentation), but the pick can't be made
     by mouse. Use a ground pile for the "transfer runs" half, or the direct
     command: `rc:SetCommand("TransferResources", depot, "load", "<Res>",
     30000, true)`. Full trail on the F76 entry.
4. Check the log for `[CommunityFixPack] RocketInteractGuard: applied`.

`Result (trade/refugee rocket refused?):` PASS — 2026-07-27 (user, landed TRADE
rocket): "it ignores it completely[,] it treats it like normal terrain and
drives right through it" — no Load/Unload prompt, the click was a plain move
order, no transfer. Exactly the EXPECTED refusal. (Cosmetic aside, not F74's
scope: the rover clips through the landed rocket's model while driving past —
possible missing obstruction footprint on Universal event rockets, noted only.)
Refugee rocket not separately exercised (same class family + same guard, probe-
verified). **Step-2 route check PASS (same sitting):** "if I create a transport
route to the rocket it just dumps them on the ground" — the route handler only
stores targets the interaction check approves, so the refused rocket silently
became a ground POSITION endpoint and the route dumped at the pad instead of
feeding the rocket (screenshots: loaded transport at the depot; pile on the
ground beside the rocket, rocket cargo untouched). Exactly the guard holding on
the route path.

`Result (control test — player rocket + depot still work?):` PASS (with the F76
caveat) — 2026-07-27: ground-pile pickup works (direct `PickupResource` path);
the depot Load prompt appears (guard not over-broad); depot LOADING verified
via route mode — the transport loaded Machine Parts from the depot normally
(route path skips the F76-broken picker for single-resource depots,
`RCTransport.lua:466-476`; cursor-load stays blocked by vanilla F76, tracked
separately). Player-rocket half not separately exercised (exact 4-class guard
+ probe cover it). Bonus observation recorded on the result above: rover
clips through the landed event rocket's model (cosmetic, vanilla).

---

## PT-41 — Two train buildings one hex apart · covers **F66**

**Setup:** open ground with room for a station and a train tunnel entrance.

**Steps:**
1. Place a **Station**. Then place a **Train Tunnel** entrance so that exactly
   **one hex** separates them — the layout that used to refuse to connect.
2. Watch the connector tiles between them for a minute of game time.
   - **EXPECTED:** the connector tile settles on ONE owner and stays there. No
     flicker, no track piece appearing and vanishing repeatedly.
   - **SURPRISE looks like:** the piece keeps blinking in and out, or the log
     fills with repeated track-element messages.
3. Try to complete a route through that pair.
   - **EXPECTED:** either it connects, or it plainly does not — but the game is
     stable and the infopanel is consistent. (One of the two buildings not
     getting a connector on the shared hex is the intended outcome; the endless
     fight was the bug.)
4. **Control:** build a station where a plain, unowned track tile already lies on
   its connector hex.
   - **EXPECTED:** the station still claims that tile normally. If it can't, the
     fix is over-broad — report it.
5. Demolish one of the two buildings.
   - **EXPECTED:** the survivor picks up the freed hex within a few seconds.

`Result (flicker stopped?):` PASS — 2026-07-26 (user): "It stayed stable, I
could not determine which building owned it no matter how I clicked on it."
Log check same sitting (Mars.exe-20260726-11.48.31): zero connector/track-element
churn lines — the old bug would have filled the log.

`Result (control — station still claims a plain track tile / survivor claims the freed hex?):` PASS —
2026-07-26 (user): demolished one of the pair and the connector "became its own
node but stayed connected to the remaining building with no weird visuals" —
the survivor held the link without any other demolish or re-place (the F66
reclaim repair working). Control also run: a station placed where a plain,
unowned track tile lies on its connector hex still claims it.

---

## PT-45 — Track salvage refund · covers **F47**

Probes prove the arithmetic; only play can show the Metals actually arriving on the
ground, and that the figure the Salvage button advertises is the figure you get.

**Setup:** a save with a **long** track — more than about 6 hexes between two
stations, the longer the better (a 20-30 hex line makes the difference obvious).
Note that track is built in sections of up to 5 hexes, and the whole line cost
roughly 200 Metals per section.
**The track MUST be drone-built with real Metals (2026-07-26):** refunds pay back
recorded spending, and `CheatCompleteAllConstructions()` / Quick Build completes
sections without ever paying — an instantly-built line carries no cost records,
reads an empty/flat refund, and CANNOT show the scaling (that is the designed
fallback for free track, not a FAIL). Drag the line, deliver the Metals, let
drones finish it; speeding time is fine.

**Trigger — case A (whole track):**
1. Select the track (click the rail line between pillars, not a station — the
   panel that lists Stations/Trains/Passengers is the whole-track selection).
   **CORRECTED 2026-07-26:** the Salvage tooltip shows NO refund figure in
   Relaunched, so read it from the refund function directly (console, with the
   track selected):
   `*r local t = SelectedObj:GetRefundResources() for _, r in ipairs(t) do ConsolePrint(r.resource .. " " .. r.amount) end`
   - **EXPECTED:** the figure scales with the length of the line — a 25-hex track
     reads roughly 5× what a 5-hex stub does (≈100 Metals per built section),
     not the same ~100 for both.
   - **SURPRISE looks like:** a long line and a short stub reading the same
     number (the old behaviour), or a figure larger than half the track's cost.
2. Salvage it and watch the ground.
   - **EXPECTED:** Metals stockpiles appear near the track, totalling roughly the
     figure read in step 1, and drones start collecting them. The assigned train
     returns to the train pool (F64's live check rides along here).

**Trigger — case B (partial salvage):**
3. On another long track, Ctrl+click (or use the Salvage button on a single track
   piece) to remove **a few hexes in the middle**, splitting the line in two.
   - **EXPECTED:** the removed section leaves a Metals stockpile behind where it
     stood — it used to leave nothing at all. The amount may be zero for some
     picks (only one hex per built section carries the section's cost record);
     over the whole line it can never add up to more than half of what the line
     cost.
   - **SURPRISE looks like:** a refund appearing for hexes that were NOT removed,
     the same section paying out twice, or a stockpile appearing when a train
     station is built over track (that is not a salvage and must stay silent).
4. Salvage what is left of that track afterwards and confirm the totals still look
   sane — the pieces already refunded must not be paid for a second time.
5. Check the log for errors mentioning `Track`, `Demolish` or `ResourceStockpile`.

`Result (case A figure scales / stockpiles arrive):` PASS — 2026-07-26: map-wide
console read printed `track 1: 22 elements, 6 stamped, refund Metals 600` /
`track 2: 47 elements, 9 stamped, refund Metals 900` — exactly stamps × 100
(half of each section's 200-Metal cost), scaling with paid sections where the
old code advertised ~100 flat for any length. Whole-line salvage earlier the
same sitting dropped stockpiles that drones collected into storage. (Selection
gotcha for next time: the infopanel can show "Track" while `SelectedObj` is a
node — the map-wide `MapForEach("map","TrackBase",…)` read is the reliable way.)

`Result (case B partial refund / no double pay):` PASS — 2026-07-26: partial
salvage drops a Metals stockpile where the removed piece stood (observed across
repeated build/salvage/rebuild cycles); zero refund on unstamped picks is the
designed per-section bookkeeping; totals stayed sane across cycles (no double
pay, no refund for surviving hexes); log clean of Track/Demolish/
ResourceStockpile errors all session.

---

## PT-46 — Splitting a track under a running train · covers **F49(b)**, checks **F49(a)/(d)**

F49(b) is **not fixed** — this test is what decides whether there is anything to fix.
Nothing in any of the three partial-salvage branches of `DemolishAndSplitTrack` reads
or writes the track's `assigned_vehicles`, so the surviving track keeps its whole train
list while its elements shrink, and the new half is created with none. What a train
standing on a removed or re-homed element actually does cannot be read off the source.

**Setup:** a long track (20+ hexes) between two stations with **at least one train
running on it**. Console open (Enter / Alt-Shift-C) for the counts.

**Trigger:**
1. With a train **mid-journey, out on the open track**, salvage a few hexes in the
   middle so the line splits in two.
   - **EXPECTED (the benign outcome):** the train is stored back as a prefab, or it
     re-routes; either way you can account for every train you owned.
   - **SURPRISE looks like:** the train vanishes with no notification, sits frozen
     on a dead stub forever, drives through the gap, or the log shows a
     `[LUA ERROR]` mentioning `Train`, `Track` or `RebuildTrainRoutes`.
2. Count them: before and after, run
   `local n = 0 for _, t in ipairs(MainCity.labels.TrackBase) do n = n + #t.assigned_vehicles end print(n)`
   and compare with the trains you can actually see plus your stored train prefabs.
3. Repeat with the train **stopped at a platform** rather than out on the line.

**While you are here — the two halves of F49 that ARE fixed:**
4. `print(MainCity.labels.TrackBase[1].max_vehicles)` on a track before and after
   you salvage most of it away. **EXPECTED:** the number drops (1 for a track under
   30 hexes, 0 for an empty one). Confirm you can still assign trains up to that
   number and no further.
5. Look at any track placed instantly by the map (not built by drones): it should be
   the same colour as track you built yourself, not pipe-coloured.

`Result (b — train accounted for after split / after platform split):` PASS —
2026-07-25/26 (user report): across multiple sittings, deleting track on an
ACTIVE line stored the train back as a prefab, the train count stayed accurate,
and no train ever vanished — the benign outcome, observed repeatedly across the
build/salvage/rebuild cycles. F49(b) resolved: nothing to fix (the engine's
storage path handles a train on a removed element correctly). Steps 4-5
(max_vehicles recompute, instant-track palette) not separately exercised —
fold into a later sitting if desired.

`Result (d — cap follows length):` _____________________________________________

`Result (a — instant track colour):` _____________________________________________

---

## PT-50 — Multiple Artificial Suns · covers **D04 `Opt_MultipleSuns`** (absorbs F39)

Reworked PT-26: the module lifts the build-once limit AND ships the panel
binding fix that makes sun #2 actually light panels. The single-sun baseline
for comparison is banked in the PT-26 archive section: night production beside
the lit sun at −21% atmospheric was small 3.6 (vs 4 daylight), large 9 (vs 10).

**Setup:** module on; a colony with one Artificial Sun already lit (SAVE from
PT-26 works). Research/cheat whatever the second sun needs
(`UIColony:SetTechResearched` for its tech if not already there; cheat-fund the
build).

**Trigger:**
1. Open the build menu with sun #1 standing.
   - **EXPECTED:** the Artificial Sun is offered normally — no "You can build
     this building only once" refusal.
2. Build sun #2 FAR from #1 (out of #1's range) through the normal build menu,
   fuel and ignite it.
3. Build solar panels AFTER it, in range of sun #2 only.
   - **EXPECTED:** at night those panels produce at the banked signature
     (≈ −10% of daylight at the PT-26 map's −21% atmospheric: 3.6/9-style
     numbers), i.e. sun #2 lights them exactly like sun #1 lights its own.
   - **SURPRISE looks like:** panels beside sun #2 dead at night (the vanilla
     F39 binding bug — the absorbed fix failed).
4. Save with both suns + panels, reload — panels stay lit (the LoadGame sweep
   and persistence both fine).
5. Turn the module OFF (fresh session, no opt-in flag), load a NO-second-sun
   save: the build menu refuses a second sun again (limit restored).

`Result (menu allows #2 / #2 lights its panels / survives reload / off restores limit?):` **PASS
in full — 2026-07-27 late (the module's first sitting, enabled through the new
D05 Mod Options toggles).** (1) Build menu offered the sun normally with #1
standing; sun #2 built through the normal menu, **multiple map sectors away**
from #1 (sector-map screenshot on file). (2) Night production beside a sun
matched the banked PT-26 signature exactly: small panel **3.6 @ −21%
atmospheric**, large **9 @ −21%** (vs 4/10 daylight); the other sector's
sun-side large panel read **10 @ 0% atmospheric** (different map, no
atmospheric penalty there — full-rate night production, consistent).
(3) Control held — panels **away from any sun closed and dropped to 0** when
night fell, so the binding fix is not over-broad. (4) **Save → reload: both
sets of panels working correctly** (tester verbatim). (5) The off-restores-limit
half was verified LIVE mid-session via the Mod Options toggle: switching the
module off brought back the "You can build this building only once" refusal
instantly, switching it on lifted it again (screenshot on file; also part of
PT-51's live-toggle evidence). **D04 → tested; the absorbed F39 binding fix is
play-verified.**

---

## PT-51 — Mod Options page · covers **D05** (the enable step for the optional modules)

The pack's entry on the game's own Options screen — first release-facing UI
the pack has ever added there.

**Checks:** (1) page lists the pack with exactly four toggles, defaults off,
sane tooltips; (2) toggles wire to the registry (`ListFixes` tracks); (3) live
toggle both directions; (4) settings survive a full restart, modules
self-activate; (5) log clean.

`Result (page+tooltips / live both ways / survives restart / log clean?):` **PASS
in full — 2026-07-27 late, the D05 build's first sitting.** (1) All four
toggles present, off by default, tooltips read sensibly (tester). (2) The
three Group 8 modules enabled via the page came up `active`; the first
`ListFixes()` call hit the LATENT nil-detail crash (pre-D05 bug, found by this
step, repaired same day — trail on the D05 entry); post-repair the listing
printed 2×68 clean lines, zero inactive/error, all four opt-ins `active`.
(3) Live BOTH ways proven twice: ClassicRockets toggled ON mid-session →
activated immediately (auto-refuel then observed working in play, D01 note);
MultipleSuns toggled OFF → build menu's "only once" refusal returned
instantly, ON → lifted again (screenshots). (4) Full game shutdown + relaunch:
all toggles still ON, and the startup log shows all four modules `applied` at
code load purely from the saved values — no console, no flag file. (5) Log
swept twice: zero `[LUA ERROR]`, zero apply failures (the known transient
MultipleSuns pre-DataLoaded line logged once and self-cleared, as designed).
**D05 → tested. The Mod Options page is the release enable path (PC + the
console platforms Paradox Mods delivers to).**

---


## PT-49 — Closed to new residents · covers **D03 `Opt_ResidencyControl`**

A new per-dome policy row: block move-ins WITHOUT quarantining. The UI row is
the pack's first added infopanel row — look at it critically.

**Setup:** a colony with ≥2 connected domes (passage) plus spare housing in
both, and a rocket of applicants on the way (or use the sponsor resupply).

**Trigger:**
1. Select a dome → the dome infopanel. At the bottom of the policy rows there
   should be a new row: **"Accepts new residents"** (green). Click it.
   - **EXPECTED:** flips to **"Closed to new residents"** (yellow, limit-style
     back — visually distinct from the red "Quarantined" row), FX plays,
     rollover text explains the policy. Ctrl+click broadcasts to all domes —
     verify on a second dome, then Ctrl+click back to open everywhere except
     the test dome.
2. With the test dome CLOSED and clearly the better home (more free housing,
   services), let colonists look for homes:
   - land new arrivals → **EXPECTED:** everyone routes to OTHER domes; nobody
     moves into the closed one.
   - wait a few sols of voluntary resettlement → **EXPECTED:** the closed
     dome's population never grows from move-ins.
3. The point of the module — the closed dome's OWN residents keep living
   normally: they still commute out through the passage to work/shop/train
   (watch a shift change), services stay available, nobody is locked in or out.
   - **BROKEN looks like:** any F61-style lockdown symptom (residents stuck,
     jobs across the passage abandoned).
4. Manual relocation INTO the closed dome (select a colonist → relocate) —
   **EXPECTED:** still works; the player's own order overrides the policy.
5. If the save has a hotel in the closed dome: tourists still check in.
6. The quarantine toggle still works independently: quarantine the closed dome,
   un-quarantine it, confirm both rows keep their own state.
7. MicroG habitat (asteroid): confirm the row appears on its infopanel too.
8. Uninstall shape: save with a closed dome, disable the module (or the pack),
   reload — **EXPECTED:** the dome accepts residents again, nothing errors.

**Progress (2026-07-27 late, first sitting):** core behavior PASSing — a
prepped high-comfort dome (Smart Apartment 0/20, comfort 70) closed to new
residents took ZERO move-ins over the observation window while its
commuters/visitors carried on normally (workers present; Mega Mall, Electronics
Store, Grocer, Open Air Gym all showing active visitors — screenshots on file).
Tester's one complaint, cosmetic: the row rendered at the BOTTOM of the dome
section (below the stat bars) instead of with the policy toggle group.
**Repaired same day** (row now inserts directly after the shipped
accept-colonists toggle — array reposition in append_policy_row); **position
VERIFIED after the relaunch** ("UI good for dome", 2026-07-27 late).
**Progress (2026-07-28, PT-52 sitting):** manual relocation VERIFIED both
directions — the player's own relocate order moves colonists INTO the closed
dome (policy override works, step 4 PASS) and OUT of it as normal.
Also that sitting: an unexpected child resident (Martianborn, age 1) appeared
in the closed dome's full Smart Apartment — investigated and CLEARED as
in-dome birth, the designed exemption (engine stores NO parent link —
`GenerateColonistData` rolls children fresh, so no UI can show parentage;
proof was indirect: dome `born_children` = 14, colonist age 1 at ultra speed,
and `CanAcceptNewColonists()` read **false** live on the closed dome, so the
voluntary-move-in path was structurally shut — gate 1 confirmed enforcing,
births the only open path).
**Arrivals + tourists VERIFIED (same sitting, deliberately adversarial
setup):** tester built a NEW landing pad right beside the closed dome to make
it the most likely candidate, then landed a rocket carrying both applicants
and tourists — every colonist bypassed the adjacent closed dome and walked to
the farther open dome (steps 2 arrivals PASS, screenshot on file); the
tourists made a beeline INTO the closed dome and checked into its active
hotel (step 5 PASS — the traits.Tourist exemption behaves exactly as
designed).
**Quarantine independence VERIFIED (same sitting):** quarantining the closed
dome triggered full vanilla seal behavior — commuter workers immediately left
their jobs and vacated the dome — while both policy rows kept their own state
(step 6 PASS; the D03 row and quarantine are demonstrably separate
mechanisms). **Uninstall shape VERIFIED (same sitting):** module toggled off
→ the dome accepts residents again, and the save reloads cleanly with
identical behavior — no errors either way (step 8 PASS, live toggle AND
reload both exercised).
**Step 7 (MicroG row) PASS after a false alarm (same sitting):** the row
first appeared missing on the asteroid Micro-G Habitat infopanel — the
tester then caught the cause themselves: the save had been reloaded WITHOUT
the module toggle on (the step-8 uninstall-shape reload). With the toggle
re-enabled the row renders in position under the vanilla Accepts Colonists
row and functions on the habitat panel (screenshot on file). The sighting
still prompted a design review — does the policy belong on asteroid
habitats at all, when crews are hand-picked rocket deliveries? Source
answer: two automatic move-in paths DO exist there (voluntary resettlement
between habitats on the same asteroid — habitats are full Communities in
`FindEmigrationDome`'s candidate set — and stranded re-homing through
`ChooseDome` after a habitat is lost or full); births cannot happen there
(`birth_policy = Forbidden` in the classdef, MicroGHabitat.lua:13).
**USER DECISION (2026-07-28): KEEP MicroG support** — it hurts nothing,
and the niche is real on multi-habitat asteroids.

`Result (row looks right / arrivals+resettle blocked / commute+services intact / manual+tourists work?):` **PASS in full — steps 1-3 on the 2026-07-27 first sitting (incl. the same-day row-reposition repair, re-verified), steps 4-8 on 2026-07-28 (PT-52 sitting), every step exercised against a deliberately adversarial setup where applicable. D03 → tested; section archived 2026-07-28.**

---

## PT-32 — Auto-export loads the valuables first · covers **F71**

The probe proves the allocation order in isolation; only play shows what actually
ends up in the hold when drones, stock levels and the one-sol departure timer all
compete. Do this straight after PT-17 — same save, same lander.

**Setup:** SAVE-E, lander on an **asteroid** in **Automated Mode**.
`SMRTest.Log.AutoCargo(true)`.

**Trigger:**
1. Make sure the asteroid has a large stock of a **bulk** resource (Waste Rock,
   Concrete or Metals) *and* a smaller stock of **Rare Metals / Exotic Minerals**.
   `CheatFillAllStorages()` on the asteroid side is the quick way.
2. Set export thresholds so **both** the bulk resource and the valuables are
   exported (threshold 0 / "export anything above" on each).
3. Read the next `CreateAutoCargoRequest(...) request{...}` line, then let the
   lander load and depart.

- **BROKEN looks like:** the request is dominated by whichever resource comes
  first **alphabetically** — Concrete/Metals ahead of PreciousMetals and
  PreciousMinerals, and Waste Rock still getting a share. The lander leaves on the
  one-sol timer full of bulk while the valuables sit on the ground.
- **FIXED looks like:** the request lists **PreciousMinerals, Electronics,
  PreciousMetals, MachineParts** first and only spends what is left on Polymers,
  Food, Fuel, Metals, Concrete and finally Waste Rock. The lander arrives on Mars
  carrying the valuables.

> Not over-broad: with the hold big enough for everything, **every** configured
> export must still appear in the request. A resource that disappears entirely is
> a FAIL.

`Result (order):` **PASS — 2026-07-28, live colony (via the leaf-class TAP2
console tap; TestKit logger blind, see PT-17 warning). Two-export leg:
PreciousMetals allocated its FULL exportable stock first, Concrete
(alphabetically earlier — the resource vanilla would have favored) got only
the remainder; when mid-load replenishment grew the valuable's claim to the
whole hold, Concrete was the one squeezed (48000 → 38000 → floor), never the
valuable. Both delivered to Mars (Mars Rare Metals +~100). The single-export
legs corroborate: a valuables-only request correctly saturated the hold at
100 units. Four-class order (PreciousMinerals/Electronics/PreciousMetals/
MachineParts) additionally probe-verified in isolation.**

`Result (nothing dropped when there is room for all?):` **PASS — the initial
co-fill allocation carried BOTH configured exports in full (PreciousMetals
40000 + Concrete 48000, hold had room); a resource only ever left the
request when its stock sat below the player's threshold (next-leg Concrete-
only load with Rare Metals ground at 84 < 144 — correct exclusion, verified
by the payload delivered).**

---

## PT-17 — Lander cargo ratchet + the capacity edge case · covers **F68**

**Setup:** SAVE-E, lander on an **asteroid** in Automated Mode, with resources
available to export. `SMRTest.Log.AutoCargo(true)`.
> ⚠️ **2026-07-28: `SMRTest.Log.AutoCargo` is BLIND to real landers** — it
> wraps `UniversalRocketBase` at runtime, but the live lander class
> `UniversalLanderRocket` carries its own baked copy of the method (STATUS
> engine facts, flattening corollary), so no request lines are ever logged.
> **Both flaws REPAIRED 2026-07-28 (same day, game-free leg):** the logger now
> wraps `UniversalLanderRocket` and reads `self.cargo[res].requested` after the
> call (output `res=req:N/have:M`); a second flaw — printing `request{}` from
> the method's always-nil RETURN value — fixed in the same pass. From the next
> relaunch `SMRTest.Log.AutoCargo(true)` works on real landers; no console tap
> needed.

**Trigger — the ratchet:**
1. Set **one** export threshold (say Metals) so the lander loads cargo.
2. Let drones load the hold to roughly half.
3. Watch the `CreateAutoCargoRequest(...) request{...} aboard{...}` lines over
   2–3 game hours.

- **BROKEN looks like:** every hour the lander asks for *less* than it is already
  carrying, flips to "unloading", and drones haul the cargo it just loaded back out —
  it loads exotics then dumps them and leaves with junk or nothing.
- **FIXED looks like:** the `request{}` figures **never fall below** the matching
  `aboard{}` figures; the hold only fills.

**Trigger — the capacity edge (the specific thing the audit flagged as unverified):**
4. Now set **two or more** export thresholds — deliberately pick resources whose names
   sort so that an **alphabetically earlier** one is present in bulk (e.g. **Concrete**
   *and* **Metals**, or **Electronics** *and* **PreciousMetals**).
5. Load the hold **to capacity** (`CheatFillAllStorages()` on the asteroid side helps).
6. Watch the lander's **status** and whether it ever departs.

- **BROKEN looks like:** with the hold full and two exports configured, the lander gets
  stuck reading **"loading" forever** and the automated rocket just sits on the pad and
  never departs.
- **FIXED looks like:** the hold fills, the status advances to **"ready"**, and the
  lander departs on schedule.
- ⚠️ **This is the known-suspect case** (the requested floor may not debit remaining
  hold capacity, so an alphabetically-earlier resource's request can exceed what's
  left). **If it sticks at "loading", that is a real FAIL and needs a code change** —
  record the exact export pair, the hold contents and the status text.

`Result (ratchet):` **PASS — 2026-07-28, live colony (not SAVE-E), single
Waste Rock export on the purchased lander Sphinx #2 (class confirmed
`UniversalLanderRocket`; the pack's replacement confirmed in the live
dispatch path via `rawget` → `Fix_LanderCargoRatchet.lua(124)`). Via the
leaf-class console tap (TestKit logger blind, see warning above): across 4
automated Mars↔asteroid cycles the asteroid-side request held PINNED at the
full-hold 80000 through every hourly recompute while aboard climbed
monotonically (0→11000→33000→59000→78000→79000) — req never below have, no
unloading flip, departure on schedule every cycle; request zeroes only at
load-complete and the intended Mars unload leg. Reserved-site auto-landing
also verified across all cycles after the one vanilla-required manual first
landing.**

`Result (capacity edge):` **Wedge criterion PASS / NEW FINDING on the fix —
2026-07-28.** Two-export co-fill leg (Concrete above 0 + Rare Metals above
144, stock 184): both resources allocated together (PreciousMetals 40000 +
Concrete 48000), status advanced and the lander departed on schedule — no
stuck-"loading" wedge in either two-export leg. BUT the request ratcheted
monotonically to the hold cap as extractors replenished stock mid-load and
the lander drained the asteroid to 84 — sixty units BELOW the player's
keep-threshold. Full forensics + root cause (the fix's aboard-into-ground
addition at Fix_LanderCargoRatchet.lua:145-151 double-implements the
anti-churn floor) + repair sketch on the F68 entry. **F68 NOT flipped.
REPAIR LANDED same day (2026-07-28, game-free leg, A/B re-verified —
baseline 1/57/14/0, all-five-toggles 62/0/10/0, 70/70 applied): the
aboard-into-ground addition deleted, the explicit floor carries the fix
(full trail on the F68 entry). This section stays un-archived until an
ATTENDED re-run of this capacity-edge leg (two exports + replenishing
stock) confirms the threshold holds live — expected post-repair: request
stays at aboard + current ground surplus, asteroid ground settles AT the
threshold, still no unload flip.**

`Result (capacity edge, attended re-run):` **PASS — 2026-07-28, live colony,
Sphinx #2, fresh relaunch with the repair loaded; captured by the repaired
TestKit AutoCargo logger (first live use — logger validated, no console tap
needed). Setup: Concrete above 0 (ground 210) + Rare Metals above 140
(ground 222), extractors actively replenishing mid-load. The request TRACKED
instead of ratcheting — PreciousMetals req 90000→91000→92000 (creeping only
by what the miners added, aboard 10000→89000 underneath), Concrete req
8000→7000 settling equal to aboard; `req` never below `have`, no unload
flip, departure on schedule. Ground after departure: 146 with miners still
running = settled AT the 140 threshold and re-accumulating (the pre-repair
run drained 60 below). F68 → `tested`; section archived.**

---

## PT-19 — Shelter reflex on an asteroid · covers **F73**

**Setup:** SAVE-E, on the **asteroid**: a **MicroG Habitat** with 2–4 colonists living
in it, and a mine they work.

**Trigger:**
1. `CheatToggleInfopanelCheats()` to get per-building levers.
2. **Cut the habitat's life support / power briefly** (a few game minutes), so colonists
   momentarily lose their residence, then restore it.
3. Run 1–2 sols at ultra speed and watch the colonists during their **idle** stretches
   (not their shifts — they're safe inside the mine while working).

- **BROKEN looks like:** after a momentary life-support blip the colonists are
  permanently homeless, wander around **outside on the asteroid surface**, and bleed
  health past the oxygen timer until they die — while an empty habitat sits right there.
- **FIXED looks like:** (a) the habitat **takes them back** as residents even though its
  life support had a gap, and (b) if a colonist is still outside past half the oxygen
  budget in vacuum, they **head indoors to rest** instead of loitering.

`Result (a — habitat re-accepts):` **PASS — 2026-07-28, live colony
(Douglasjay MicroG Habitat, 9 residents; mine on an independent power
grid). Two gap shapes tested: habitat toggled OFF, and habitat's power
supply cut with the building on — identical result both times: residence
NEVER dropped (stronger than re-accept — the panel showed Residence =
Micro-G Habitat throughout), no homeless flag, clean recovery on restore.
Vanilla observation (not the pack): workers inside the independently-powered
mine flagged Suffocating/Freezing/Dehydrated while the habitat's life
support was down — the status effects read the residence's supply, not the
occupied building; recorded on the F73 entry.**

`Result (b — seeks shelter):` **PASS — 2026-07-28. Watched through shift
end: workers routed straight back into the habitat, nobody idled on the
asteroid surface at any point — the death-spiral precondition (homeless →
Roam outside) never arises since residence never detaches. The Rest-reflex
safety net itself was not observably triggered (nobody stayed outside past
the threshold); its wrapper half is fully probe-verified (MarsDebug pass
2026-07-25/26).**

---

## PT-33 — "No available Asteroid Landers" with a lander on the pad · covers **F72**

This one is pure UI flow — the probe proves the predicate, only play proves the
button behaves.

**Setup:** SAVE-E. **Exactly one** Asteroid Lander, on the Mars pad, **manual**
mode, **no destination assigned**, and a scanned asteroid available in the
Planetary View.

**Trigger — case A (the reported case):**
1. Land the lander with cargo aboard and **do not let it finish unloading** —
   pause, or take the drones away so unloading stalls. Its status should read
   *unloading*.
2. Open **Planetary View → the asteroid → VISIT ASTEROID**.

- **BROKEN looks like:** the "No available Asteroid Landers" popup, offering to
  open the Resupply screen — while the lander is visibly parked on the pad.
- **FIXED looks like:** the rocket picker opens and the lander is in the list.

**Trigger — case B (maintenance):**
3. Let a landed lander fall due for maintenance (or wait for one to). With its
   status showing it is waiting for parts, repeat step 2.
- Same expectation as case A.

**Trigger — case C (not over-broad — the important negative):**
4. Assign the lander a destination and confirm a payload so it is **loading for a
   flight**. Repeat step 2.
- **Expected:** you still get "No available Asteroid Landers" (or an empty list).
  A rocket already committed to a flight must NOT be offered for a second
  expedition. If it is, that is a FAIL.
5. With **no lander at all** (send it away, or a save that has none), repeat
   step 2 — the popup must still appear.

`Result (case A unloading):` **PASS — 2026-07-28, live colony, Sphinx #2
(spare lander deleted for isolation off a quicksave). Stalled unload state
(Concrete/Metals/Rare Metals aboard, 0 drones, "No destination set"):
VISIT ASTEROID opened the rocket picker with Sphinx #2 listed "Ready".**

`Result (case B maintenance):` **PASS — 2026-07-28. Maintenance due via
AddMaintenancePnts, waiting for parts: picker still offered the lander.**

`Result (case C committed lander / no lander still refused?):` **PASS both
halves — 2026-07-28. Committed to another site (through PREPARE): picker
EMPTY, the committed rocket not offered for a second expedition; after
departure with no lander at the colony: same empty refusal. Not over-broad.
Note: the refusal presents as an empty picker rather than the popup — the
documented vanilla gate quirk (mis-parenthesized WaitLaunchOrder branch,
F72 entry observation (a)); the list builder correctly excludes, so nothing
blocks and nothing is wrongly offered.**

---

## PT-40 — Train tunnel carries power · covers **F65**

The fix only acts when the two ends really are on different power grids, so this
test has to create that situation deliberately.

**Setup:** two separate power grids with no cable between them. On grid 1, a
Station; on grid 2 (far away, e.g. across terrain a cable can't cross), the other
end. Build a **Train Tunnel** pair linking the two areas and attach a station
**directly** to the tunnel entrance — close enough that the connecting track is
only one or two tiles long.

**Steps:**
1. Before completing the short track, note each side's power surplus/deficit
   (select a building on each grid; the two must read as separate grids).
2. Complete the short track so the station and tunnel connect.
   - **EXPECTED:** the two grids become one — the surplus/deficit numbers merge,
     and a shortage on one side is now fed by the other.
   - **SURPRISE looks like:** the track connects for trains but the grids stay
     separate.
3. Now **salvage the short track** again.
   - **EXPECTED:** the grids split back apart cleanly, no error in the log, no
     building left permanently unpowered that has its own supply.
4. Repeat step 2 with a **long** track (10+ tiles) between two stations — this is
   the path the game already handled; it must be unchanged.
5. Save, quit to menu, reload the save.
   - **EXPECTED:** the grids are still merged, and the log shows no errors from
     our PostLoadGame pass.

`Result (grids merge on connect?):` **PASS — 2026-07-28, live colony.
Two-grid setup with grid 2 having NO active source; normal station, both
geometries (snugged directly to the tunnel entrance AND a couple of track
pieces between): a fresh consumer (MDS Laser, 10 power) attached to the
sourceless side ran off the far grid's supply through the tunnel.**

`Result (split cleanly on salvage / survive reload?):` **PASS — 2026-07-28.
Salvaging the short track split the grids cleanly (far consumer went dark,
nothing self-supplied stranded); long-track control unchanged; save → quit
→ reload kept the merge. Log swept same session: `TrackTunnelPowerBridge:
applied` and zero errors incl. the reload's PostLoadGame pass.**

---

## PT-29 — Gene Forging · covers **F41**

**Setup:** any colony — **no colonists needed, and it does not matter what else
you have researched.** (Both corrected 2026-07-29 after the original text proved
unrunnable: it said "before researching anything" while reading
`MainCity.labels.Colonist[1]`, and you cannot have a colonist before the game
has auto-researched something.) Two facts make it easy:

- `GetRareTraitChance(unit)` takes an **optional** unit —
  `local city = unit and unit.city or MainCity` (`Colonist.lua:3542`, preserved
  verbatim by the fix). Call it bare and it reads MainCity, so it works from
  sol 1 with an empty colony.
- The function consults **exactly two techs** and is blind to every other:
  `GeneSelection` (shipped) and `GeneForging` (added by the fix). So the only
  real precondition is that *those two* are unresearched — and neither can
  arrive by accident, because **GeneSelection is a Breakthrough** (needs anomaly
  discovery; `CheatResearchAll()` skips undiscovered breakthroughs) and
  **GeneForging is a Storybit tech** (granted by a story event).

**Trigger (console) — one line at a time, nothing else on the line:**
```
UIColony:IsTechResearched("GeneForging")
UIColony:IsTechResearched("GeneSelection")
GetRareTraitChance()
UIColony:SetTechResearched("GeneForging")
GetRareTraitChance()
UIColony:SetTechResearched("GeneSelection")
GetRareTraitChance()
```

- **BROKEN looks like:** still `nil` after Gene Forging is researched, then
  `100` once Gene Selection lands — i.e. Gene Forging contributed nothing.
- **FIXED looks like:** `nil` → **`50`** after Gene Forging → **`150`** after
  Gene Selection as well.

`Result:` **PASS — 2026-07-29** (run on the SAVE-B no-disasters fixture).
Preconditions confirmed live: both techs read `false` before starting. Readings
went **`nil` → `50` → `150`**, exactly the fixed signature — Gene Forging alone
now contributes its `param1 = 50` where it previously contributed nothing, and
the two techs **add** rather than one masking the other (the defect ChoGGi's
param1-bump approach would have left in place). `SetTechResearched` returned
`true` for both grants. → **F41 `tested`.**

*Two documentation defects were found and repaired by running this test.*
(1) The original trigger was unrunnable — see the Setup note above. (2) The
first attempt pasted the doc's `--> nil` annotations into the console and got
`not understood` three times: the `*r` / `*g` rules splice the typed code into
`CreateRealTimeThread(function() %s end) return` **on one line**
(`uiConsole.lua:360-361`), so a `--` comment swallows the closing `end) return`
and nothing compiles (`console.lua:24`). Compounded by the console input being
a single line, so a pasted multi-line block concatenates. Both traps are now
recorded in the checklist's console section and the continuation prompt, along
with the corollary that a bare expression is auto-wrapped in
`ConsolePrint(print_format(...))` (`uiConsole.lua:363`) — so a simple read
needs neither `*r` nor `ConsolePrint`.

*Not exercised (optional, statistical):* the applicant-batch feel check
(`CheatGenerateApplicants(100)` before/after). The console read is definitive
for F41 — the fix's entire claim is the value `GetRareTraitChance` returns, and
the path from there into trait generation is shipped code the fix does not
touch.

## PT-31 — Edit Payload sticks · covers **F70**

**Setup:** SAVE-E. An **Asteroid Lander** on the Mars pad, in **manual** mode (not
automatic), with an asteroid destination selected. `dbg_ToggleRocketInstantTravel()`.

**Trigger:**
1. Open **Edit Payload**. A brand-new lander should show the policy defaults
   (roughly 5 Drones, 20 Metals, 5 Polymers, 5 Machine Parts, 5 Electronics and a
   few extractor prefabs) — that prefill is intended and must still happen.
2. Set **Metals to 0** and everything else to whatever you actually want. Confirm.
3. **Re-open Edit Payload immediately.** Metals must still be 0.
4. Let the lander fly, land and unload. Open **Edit Payload** again.

- **BROKEN looks like:** Metals is back at 20 in step 3 — and after step 4 the whole
  policy template has reappeared, so the lander loads a cargo you never asked for.
- **FIXED looks like:** what you set is what you see, in step 3 and after the round
  trip in step 4.

> Note the intended prefill in step 1 is the check that this fix is not over-broad —
> if a *fresh* lander shows an all-zero payload, that is a FAIL too.

`Result (row stays empty?):` **PASS — 2026-07-28, live colony: Galileo #1
(purchased new for the test), destination Kayra AL10 (fresh asteroid),
manual mode. Metals 20 → 0, confirmed; immediate re-open read Metals 0 with
the rest exactly as configured (26,000 KG); after the full round trip
(launch, land, unload) Edit Payload still showed no Metals and no template
resurrection.**

`Result (fresh lander still prefilled?):` **PASS — the brand-new lander's
first Edit Payload showed the full policy defaults (20 Metals / 5 Polymers /
5 Machine Parts / 5 Electronics / 5 Drones + 3 extractor prefabs) — the
intended prefill still happens; the fix is not over-broad.**

---

## PT-16 — Asteroid lander: empty launch + return fuel · covers **F67, F69**

**Setup:** SAVE-E. An **Asteroid Lander** on the pad. `dbg_ToggleRocketInstantTravel()`.

**Trigger — F67 (empty launch):**
1. Enable **Automated Mode** on the lander and set **every** export/import threshold to
   "ignore" (so the auto request computes to nothing).
2. `SMRTest.Log.CargoReady(true)` and `SMRTest.Log.AutoCargo(true)`.
3. Run 1–2 sols at ultra speed.

- **BROKEN looks like:** the lander takes off with an empty hold and ping-pongs
  Mars↔asteroid forever, burning ~70 fuel a trip and delivering nothing.
- **FIXED looks like:** the lander **sits on the pad** while its cargo request is empty
  (`IsCargoReady -> false` in the log); it only launches once it has something to carry
  (or when the 1-sol auto-depart timer legitimately expires).

**Trigger — F69 (return fuel):**
4. Manually fly the lander to the asteroid and **land it manually** (no return
   destination set). Make sure there are **no drones and no drone hub** on the asteroid.
5. Watch the lander's fuel and its resource requests after `CmdUnload`.

- **BROKEN looks like:** on landing the lander dumps its reserved return fuel onto the
  ground as "excess" — with no drones there to put it back, the lander is stranded on
  the asteroid permanently.
- **FIXED looks like:** the lander **keeps a fuel ration requested/reserved** (≥ its
  `FuelResourceAmount`) and can fly home.

`Result (F67):` **PASS — 2026-07-28, live colony, Galileo #1, automated
mode, unsatisfiable GET rule (Metals get-when-above 100, Kayra stock 0).
Asteroid-side gate held `IsCargoReady -> false` through ~20 hourly empty
recomputes (a full sol, captured by the repaired leaf-class CargoReady
logger's first live outing), then the designed 1-sol timer exit — cadence
one round trip per sol-plus, no hourly ping-pong. Mars-side quick fueled
departure with no SEND rules confirmed DESIGNED (CheckAutoDepart consults
only the current side's rule set — engine fact recorded on the F67
entry).**

`Result (F69):` **PASS — 2026-07-28, live colony: manual mode, no
destination, landed on bare Kayra (no drones/hub). Post-unload: Return
trip fuel 15/15 held in reserve, general fuel request 0/0, nothing offered
as excess — then launched home on the reserve and landed on Mars. First
attempt via auto-mode landing correctly discarded (auto retains
arrival_loc — non-discriminating); RoughTouchDown storybit hazard +
verified console recovery recorded on the F69 entry.**

---

## PT-43 — Numbers and tooltips trio · covers **F19, F20, F21**

Three small, independent reads. Any established colony will do — one with trains
and a few sols of history.

**F19 — Command Center graph caption.**
1. Open the **Command Center**, switch to the **Machine Parts** graph (Electronics
   works too), and look at the "Produced ... and Consumed ..." caption above it.
   - **EXPECTED:** the Consumed figure is in the same ballpark as the height of
     the Consumed bar — it now includes maintenance, which is most of your
     Machine Parts usage.
   - **SURPRISE looks like:** a near-zero figure beside a tall bar (the old
     behaviour), or a figure that is now clearly larger than the bar.
2. Sanity-check **Food**, where consumption is real and maintenance is nil — the
   number should be essentially unchanged from before.

`Result (Machine Parts caption vs bar / Food unchanged?):` **PASS —
2026-07-28, live colony (Command Center graphs). Machine Parts: caption
"Consumed (4)" beside per-sol consumed bars of ~4-6 (Sol 221 tooltip 6/4)
— maintenance now included, no near-zero caption. Food sanity check:
"Consumed (116)" vs bars ~100-104 (Sol 223 tooltip 60/104) — real
consumption unchanged; not over-broad. F19 → tested; F20/F21 reads still
un-run, section stays.**

**F20 — Morale tooltip.**
3. Find a colonist whose **Comfort** is high (green, at or above the high mark).
   Select them and hover the **Morale** stat.
   - **EXPECTED:** no "+Comfort" style bonus row is listed, and the rows shown
     add up to the Morale value in the title.
   - **SURPRISE looks like:** the bonus row is still there, or a row that SHOULD
     be there is gone.
4. Find a colonist whose **Comfort is low** (red) and hover Morale.
   - **EXPECTED:** the Comfort PENALTY row is still listed — that one is real.
     If it disappeared, the fix is over-broad; report it.
5. Hover Morale on a colonist with high **Health** or **Sanity**.
   - **EXPECTED:** those bonus rows are untouched.

`Result (high-Comfort row gone / low-Comfort row kept / Health+Sanity intact?):`
**PASS all three — 2026-07-28, live colony. High-Comfort colonist (Hugo
Fifth, Health/Sanity/Comfort all ≥ high): tooltip listed ONLY "+5 (Health)"
and "+5 (Sanity)" — no phantom Comfort bonus — and summed exactly (40 base
+ 5 + 5 = 50 title). Low-Comfort negative (Obi Jetson, Comfort driven to 0
via the ChangeComfort console line, reason logged in the stat tooltip):
"I can't live like this -10 (Comfort)" STILL listed — the real penalty
kept, fix not over-broad — alongside "+5 (Health)" and "Severely stressed
-10 (Sanity)", proving both directions of the other stats intact. F20 →
tested; only the F21 train-waiting read remains.**

**F21 — Train waiting time.**
6. Pick a station where colonists queue for a while. Select a colonist about to
   travel, note their **Comfort**, and watch them wait, board, ride and arrive.
   - **EXPECTED:** the Comfort drop on arrival reflects the ride, not the wait.
     A long wait followed by a short hop should cost little.
   - **SURPRISE looks like:** a big Comfort hit after a long wait and a one-stop
     ride.
7. Open the **train's** and the **track's** infopanels and check the travel/spent
   time statistics over a few sols.
   - **EXPECTED:** they no longer include platform waiting (the station's own
     waiting statistic still does, and should be unchanged).

`Result (Comfort hit matches the ride / train+track stats exclude waiting?):`
**PASS — 2026-07-28, live colony (5-station network built for the test).
Comfort half: a colonist queued 17+ game hours logged ZERO travel Comfort
entries while waiting; a migrant whose total trip ran 16 hours arrived at
Comfort 99 (the vanilla -1/hour-incl-waiting math would have billed ~-16).
Stats half: the train's "Travel time (rolling average)" read 4.15 hours
against riders with 16-17h queue-inclusive trips — ride-scale, waiting
excluded; the track stat reads the same per-trip start_wait accounting
(TransportStatistics), verified via the entry's mechanism. Setup notes for
posterity: service-seeking colonists will NEVER ride (F79 — vanilla
service search is passage-only; use WORK commuters or migrants as
subjects), and an under-served network can strand valid passengers
indefinitely (F80) — both found and filed during this read's setup.**

---

## PT-23 — Station resource switches vs. train unloading · covers **F46**  `[ARCHIVED 2026-07-28 — PASS both halves, F46 → tested]`

**Setup:** SAVE-A. Build a **three-station Martian Express line** A — B — C on one
track (`CheatCompleteAllConstructions()`), assign 1–2 trains, and let the line run
for a sol so routes are established. Then:

1. `CheatFillAllStorages()` — every depot **and station** now holds everything.
2. Open **station B**'s infopanel and switch **Metals OFF** (the per-resource
   accept toggles). Leave Metals **on** at A and C.
3. Note B's Metals stock, then run 3–4 sols at `SetGameSpeedState("ultra")`.

- **BROKEN looks like:** B's Metals count never settles. Trains haul the forbidden
  Metals out (correct) and then **bring Metals straight back in** at the next stop,
  because unloading ignores the switch entirely. The count sawtooths up and down
  for the rest of the game and the line is permanently busy moving one resource in
  circles.
- **FIXED looks like:** B's Metals drains to **0 and stays there**. Trains still
  carry Metals *through* B on their way to A/C, they just don't drop it off.

**Stranding check (the thing this fix could plausibly break):** while the line runs,
watch for a train **parked at a platform with cargo it never unloads**. Select a
train and read its cargo. Also switch Metals **off at all three stations** for one
sol — a train holding Metals must still be able to empty itself (nowhere accepts it,
so the dump is deliberately allowed) rather than sitting loaded forever.

`Result (ping-pong stopped?):` **PASS — 2026-07-28, live colony (run on the
user's 5-station network from the PT-43 build, superset of the 3-station
procedure). Metals forbidden at a single station: its stock drained to 0/60
and STAYED there (screenshot on file — the X'd Metals row holding 0/60 while
every other resource sat at fill levels); no sawtooth, no re-drop, trains
carried Metals through to the accepting stations.**

`Result (no stuck loaded trains?):` **PASS — two stranding legs, 2026-07-28.
Leg 1 (drones on, single forbidden station): all Metals cleared out. Leg 2
(the hard case — Metals forbidden at ALL FIVE stations, station drones
off): the lone previously-forbidden station emptied in ~0.5 sol; stations
inside external drone coverage had their Metals cleared by drones;
ISOLATED stations with no drone coverage kept their Metals in place
(screenshot: forbidden station holding 57/60) — EXPECTED, not a defect:
loading only targets accepting destinations (Train.lua:905-939, untouched
by the fix), so with nowhere accepting, forbidden stock has no train exit
and no drone rebalance — vanilla-consistent statics. The critical
criterion held: NO train parked or roamed with a loaded hold — trains
dumped carried Metals rather than stranding, the fix's designed
no-accepting-station dump branch observed live.**

---

## PT-09 — Domes Overview red low-stat column · covers **F14**  `[ARCHIVED 2026-07-28 — PASS, F14 → tested]`

**Setup:** SAVE-A. Drive one dome's **average Health (or Comfort / Sanity / Morale)
below the low threshold** — cut its life support / medical building, or spawn a batch
of colonists into a dome with no services:
`CheatSpawnNColonists(30)` with that dome selected, then let a sol pass at ultra speed.

**Trigger:** `OpenCommandCenter()` → **Domes Overview** tab. Look at that dome's row.

- **BROKEN looks like:** the failing stat is rendered in ordinary white text, exactly
  like a healthy one — nothing on the overview tells you which dome is in trouble.
- **FIXED looks like:** the below-threshold value is highlighted **red** in its column,
  and normal values stay unhighlighted.

`Result:` **PASS — 2026-07-28, live colony (Hoover #1 driven down by cutting the
dome's utilities, finished with the verified ChangeComfort console loop). The
below-threshold cell rendered RED (Comfort 0 in red while the same row's
Sanity 66 and Morale 49 stayed white — per-CELL highlight, not per-row) and
every healthy dome's values stayed plain white; on recovery (Comfort back to
high 80s) the cell returned to white. Setup notes: the peril statuses
(Suffocating/Freezing/Dehydrated/Starving) share a 12-36 game-hour per-colonist
GRACE window (StatusEffects.lua:93-98) before any Health damage — cutting
utilities moves nothing for at least half a sol; the ChangeComfort loop is the
fast, casualty-free path. OBSERVATION, researched and resolved same session:
the fifth overview column (Satisfaction) reads red 0 for EVERY dome in a
mature colony — correct data, vanilla-intended red. Satisfaction is the
tourist-rating stat: Colonist:ChangeSatisfaction (Colonist.lua:3905-3918)
zeroes all positive gains once a colonist is past the tourist sol window, so
long-resident populations sit at the 0 default and the restored below-30
highlight paints the whole column red permanently. A vanilla design wart the
fix EXPOSED, not caused; the header icons having no rollover is also vanilla.**

---

## PT-55 — Opt-module live-toggle re-verify · covers **audit fix 1.3 (2026-07-29)**

The audit rework moved ClassicRockets' fuel wrap, ResidencyControl's dome
gate and MultipleSuns' panel-binding wrap to file-scope installs, so a FIRST
mid-session Mod Options enable now works without a relaunch (previously
silently dead until restart). One sitting, any healthy save, per module:

> ✅ **Setup state (2026-07-30): all six toggles are OFF** — the user flipped
> them for the default-config A/B leg (verified in that leg's log: 69/75
> active, all six `inactive (opt-in)`). Toggles are account-persistent, so
> unless they have been changed since, this test's required starting state is
> already set — go straight to step 1. (The two D09 dials are separate,
> default to base, and don't affect this test.)

1. Start the session with the module **OFF**. Mid-session, toggle it **ON**
   (no relaunch) and confirm the behavior engages: ClassicRockets — a parked,
   destination-less player rocket starts requesting launch fuel;
   ResidencyControl — a closed dome stops voluntary move-ins (the infopanel
   row appears on the next panel open); MultipleSuns — a NEW panel built
   beside sun #2 binds to it (the limit lift itself was already live-safe).
2. Toggle **OFF** again: behavior reverts immediately (vanilla answers).
3. `SMRFixPack.ListFixes()` agrees with the toggle at each step; log clean
   (PT-22 rules).

PASS flips nothing on its own (the modules keep their D-entry gates) — it
retires the audit's A2 "live confirmation still worthwhile" caveat; record
the result on the D01/D03/D04 entries.

`Result:` **2026-07-30 — the audit's A2 question is ANSWERED YES: all three
hooks install and run on a first mid-session enable, no relaunch.** Per module:

- **ResidencyControl (D03) — PASS, clean.** Mid-session flip worked with no
  issues at all.
- **MultipleSuns (D04) — PASS with a documented, self-healing limitation.** A
  panel built BEFORE the flip did not start tracking sun #2; a panel built
  AFTER it bound immediately; after a save/reload the pre-existing panel
  snapped to the sun. **Expected by construction:** the binding fix wraps
  `SolarPanelBase:GameInit`, so a panel that already ran GameInit cannot be
  retro-bound — and a reload re-runs GameInit (plus the module's own LoadGame
  sweep), which is what heals it. Nothing owed.
**Step 2 (toggle OFF) — REPORTED VERIFIED 2026-07-30.** The tester confirms all
three revert immediately on toggle-off — ClassicRockets stops requesting fuel on
a destination-less parked rocket, ResidencyControl's closed dome accepts
move-ins again, MultipleSuns' build menu refuses a second sun again. *Provenance
note: verified during a parallel session and reported here rather than captured
separately, so there are no per-module screenshots for this half.* The OFF
direction is the cheap half structurally — every hook consults
`SMRFixPack.IsActive` per call, so OFF is the pass-through path.

- **ClassicRockets (D01) — hook PROVEN LIVE, but step 1 as written FAILS.** A
  rocket already parked on the pad did NOT begin refuelling after the flip, and
  — unlike the panel — **did not heal on a save/reload either**. A rocket that
  LANDED after the flip started filling immediately. Cause: the wrap is on
  `GetFuelResourceRequest`, which is only consulted when
  `CargoTransporterNew:UpdateCargoResourceRequests` runs; for an already-parked
  rocket nothing re-triggers that, and landing is what does (the tester's own
  "on-land interaction" guess, confirmed in source). So the file-scope install
  is working — the demand refresh is what is missing. **DECIDED 2026-07-30:
  accepted as a documented limitation (user call)** — no `on_activate` refresh
  built; an already-parked rocket picks the behavior up on its next landing.
  The enhancement path stays on record on the D01 entry. With this decision,
  step 1 is CLOSED for all three modules and only step 3 remains for PT-55.

**Step 3 (`ListFixes` agreement + log sweep) — PASS 2026-07-30. PT-55 CLOSED.**
Run in the live sitting (session log `Mars.exe-20260730-12.03.01`); the full
evidence chain is on disk. Mod Options cycle: all six opt-ins `applied`
(sitting's first enable) → `deactivated via Mod Options` ×6 → `re-activated
via Mod Options` ×6 → `deactivated` ×6 — with an on-screen status read AND a
full `SMRFixPack.ListFixes()` block agreeing at every step: the six opt-ins
tracked the toggles exactly, and all 69 default-active modules (incl.
DroneStatDials) stayed `active` throughout. Log clean per PT-22: zero
`[LUA ERROR]` blocks, zero pack errors or failed activations; only
known-benign noise (Braze telemetry DNS failures, the two LawOfficeDoor
ResManager lines). Bonus capture: on the mid-sitting reload,
`MultipleSuns: reconnected 1 solar panel(s) to an Artificial Sun in range` —
the D04 self-heal observed in the log itself.

**Closure summary:** step 1 resolved per module (D03 clean; D04 self-healing
binding timing, expected by construction; D01 parked-rocket limitation
ACCEPTED by user call, `4f5f61e`), step 2 reported verified, step 3 PASS
above. Retires the audit's A2 caveat (AUDIT_FINDINGS.md). Flips no fix
statuses — the modules keep their D-entry gates.

*Tooling fact (earned closing this test):* while Mars.exe holds the log open,
the logs DIRECTORY shows a stale 0-byte size for it — NTFS directory metadata
only updates on handle close. `FlushLogFile()` works; open or copy the file
to read the flushed content instead of trusting the listing.

---

## PT-48 — Acknowledged warnings · covers **D02 `Opt_AcknowledgedWarnings`**

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

`Result (acked stay quiet / new one warns / re-break warns / survives reload?):`
**PASS IN FULL — 2026-07-30**, all five steps, on the live 297-sol
SAVE-B-derived no-disasters colony. **D02 → `tested`.**

**Conditions (EXTERNAL VALIDITY rule).** Cheat-developed colony, ~166
colonists, full depots, normal game speed throughout except the step-1 soak.
Module enabled mid-session via Mod Options with **no relaunch** — D02 does NOT
have the audit-1.3 first-enable defect, because its three wrappers replace
plain notification GLOBALS rather than class methods, so class flattening never
applies, and `OnMsg.ApplyModOptions` re-runs `apply()` on the tick
(`00_Core.lua:129`). Every claim below is a console counter reading, not an
eyeball judgement.

**The counter** (re-run at every step; select the building first):
`*r local b = SelectedObj local n = FindNotification("NotWorkingBuildings", b:GetMap()) ConsolePrint("acked=" .. tostring(b.SMRFixPack_ack_notworking) .. " shouldshow=" .. tostring(b:ShouldShowNotWorkingNotification()) .. " in_notif=" .. tostring(n and n.objects and n.objects[b] ~= nil) .. " notif_objs=" .. tostring(n and n.objects and #n.objects or 0) .. " suppress_until=" .. tostring(SuppressedNotifications["NotWorkingBuildings"]) .. " now=" .. tostring(GameTime()))`

Whole-ack-set enumeration:
`*r local n = FindNotification("NotWorkingBuildings", CurrentMap) local c = 0 for _, b in ipairs(CurrentMap:MapGet("map", "Building") or empty_table) do if b.SMRFixPack_ack_notworking then c = c + 1 ConsolePrint(c .. " " .. b.class .. " shouldshow=" .. tostring(b:ShouldShowNotWorkingNotification()) .. " in_notif=" .. tostring(n and n.objects and n.objects[b] ~= nil)) end end ConsolePrint("total_acked=" .. c .. " notif_objs=" .. tostring(n and n.objects and #n.objects or 0))`

**Fixture:** three buildings left off the power grid (a Concrete Extractor among
them) as the ack set, plus a newly built Triboelectric Scrubber as the "third
building", plus cabling for the recovery leg. Power-cut damage was chosen over
PT-38's out-of-range maintenance failure precisely because step 3 needs damage
that can be UNDONE.

**POSITIVE CONTROL FIRST (module OFF)** — steps 1 and 2 are "nothing should
happen" tests, and this project has twice been burned by those (PT-29, PT-11).
With D02 off, dismissal armed `suppress_until = 211,856,285` against
`now = 211,736,285` — **exactly +120,000**, i.e. `SuppressTime` to the
millisecond — and the notification RETURNED after the window expired. That
proves the no-power fixture genuinely generates re-add attempts, so a later
"it stayed quiet" cannot be a false PASS. It also verified D02's pass-through
direction while inactive (`acked=nil`, shipped window armed normally).

**Step 1 — acked stay quiet: PASS.** With D02 ON, dismissal stamped the
buildings and left `suppress_until=nil` — the module deliberately skips the
shipped whole-id window, so nothing but the per-object filter is holding
anything back. The extractor then held at
`acked=true shouldshow=true in_notif=false` from `now=211,940,495` to
`now=212,446,345` = **505,850 game-ms ≈ 16.9 game hours = 4.2 vanilla windows**;
vanilla would have re-nagged four times in that span. `shouldshow=true`
throughout is the load-bearing half: the building actively QUALIFIED for the
notification the whole time and was still excluded.

**Step 2 — new breakage still warns: PASS.** A freshly built Triboelectric
Scrubber warned immediately while three acknowledged buildings sat broken;
the notification listed **only** the scrubber (`objs=1`, `ack=nil`). Placement
was done PAUSED, so game time never advanced and the warning provably landed
inside the window vanilla would have been silent for.

**Step 3 — recovery re-arms: PASS.** Reconnecting power to the original three
genuinely recovered them, which routed each through the `RemoveObjectFromNotification`
wrapper and cleared all three stamps (**`total_acked` 3 → 1**). Splitting the
cable again re-broke them and all three re-warned (`notif_objs=3`). Stronger
than the step asks for: the one building that never recovered (the scrubber,
stamped in a later dismissal) stayed correctly filtered out through two power-grid
rebuilds and three neighbour break→recover→break cycles, with `notif_objs`
climbing 1 → 2 → 3 and the acknowledged one never leaking in.

**Step 4 — survives save/reload: PASS.** Flagged before the run as the likeliest
failure, since `SMRFixPack_ack_notworking` is a plain member on the Building
object and its persistence had only ever been asserted in design, never
exercised. Quicksave + reload returned
`1 TriboelectricScrubber shouldshow=true in_notif=false / total_acked=1` — the
stamp persisted and the acknowledged building stayed out of a live notification
after the load.

**Step 5 — other warning ids behave vanilla: PASS.** Source fact established
first: **exactly two notification presets in the whole game are `Suppressable`**
— `InsufficientResources` and `NotWorkingBuildings` (`Data/NotificationPreset.lua`
:546/:646). D02's guard is a literal `notification.id == ID`, so
`InsufficientResources` is the ONLY id in the game where the module could
possibly cause a visible difference; `PowerGridProblem` and friends are not
suppressable at all, which is why dismissing one leaves
`SuppressedNotifications` empty (correct, not a failure — cost one inconclusive
reading before it was understood). Forced the real check with
`const.MinDaysFoodSupplyBeforeNotification = 1000000` (restored to **3**
afterwards; `const` is static config, not a GameVar, so nothing persists).
The resulting **"Low Storage"** warning (that is `InsufficientResources`'
Title — it does not say "Insufficient Resources" on screen) armed
`SuppressedNotifications["InsufficientResources"]` normally on **two separate
dismissals** (7,992,065 then 8,167,605, +175,540 apart), the entry
**self-cleared on expiry** (absent at `RealTime=8,220,479`), and the warning
**re-nagged on schedule**. Pure vanilla. `NotWorkingBuildings` never appeared in
that table at any point — the module's intended asymmetry, visible side by side
with an untouched id in the same session.

**VANILLA ENGINE OBSERVATION recorded en route — not a D02 issue, unexplained.**
`InsufficientResources`' suppression clock reads as **REAL time, not game
time**: its stored values sat in the 8.0-8.2M range and expired against
`RealTime()=8,220,479` while `GameTime()` was 213.5M. Yet
`NotificationPreset:GetTime()` is `self.GameTime and GameTime() or RealTime()`
with `GameTime` **defaulting true** (`NotificationPreset.lua:65-66/:126-128`),
and neither preset overrides it — and PT-38 measured `NotWorkingBuildings` on
GAME time three times over. So two presets with identical `Suppressable`/
`SuppressTime`/`GameTime` settings appear to resolve different clocks. D02
never consults `GetTime()`, so nothing here affects the module or this PASS,
but it is worth a look in a game-free sitting; if the instance rather than the
preset supplies `GameTime`, PT-38's recorded fact may need scoping.

**Why this test sat open so long:** the early D02 work everyone remembers is
**PT-38**, the *gate* — it measured the shipped cadence and corrected the
premise from "2 real minutes" to 120,000 GAME-ms. That is archived and done.
The module was then BUILT the same day (2026-07-27) and its only coverage since
was the TestKit stand-in probe. PT-48 is the play half, and it had never been
run once until now.

---

## PT-46 tail — train cap + instant-track palette · covers **F49(d), F49(a)**

The main half — splitting a track under a running train, F49(b) — PASSed
2026-07-25/26 and is archived (resolved as no-defect: the engine stores the
train back as a prefab). The archived run explicitly left these two small
checks "not separately exercised":

**Steps:**
1. Read every track's element count and cap, salvage most of one away, read again.
   **EXPECTED:** the cap follows the shipped formula (`Track.lua:65`) — 0 elements
   → 0, 1-29 → 1, 30+ → `2 * Max(1, DivRound(n, 50))`. Confirm you can still assign
   trains up to that number and no further. Paste-safe counter (read-only, prints
   actual vs expected for every track):
   `*r for i, t in ipairs(MainCity.labels.TrackBase or empty_table) do local u = t.elements_under_construction or empty_table local r = t.repair_cgs or empty_table local n = #(t.elements or empty_table) + ((#r > 0) and 0 or #u) local exp = (n == 0) and 0 or (n < 30) and 1 or 2 * Max(1, DivRound(n, 50)) ConsolePrint(i .. " els=" .. n .. " cap=" .. tostring(t.max_vehicles) .. " expected=" .. exp .. " trains=" .. #(t.assigned_vehicles or empty_table) .. (t.max_vehicles == exp and " OK" or " MISMATCH")) end`
2. ~~Look at any track placed instantly by the map~~ — **PARKED 2026-07-30, see
   the (a) result line below.**

> ⚠️ **Known accepted coverage gap — do NOT report as a regression.** The
> `AutoConnectTracks` merge path and instant-build reuse of an existing
> `track_obj` recompute nothing in-session; a MERGED track's cap can read
> `MISMATCH` until the next load's sweep corrects it. Salvage is the covered
> path. Full note on the F49 entry.

`Result (d — cap follows length):` **PASS — 2026-07-30**, live 305-sol colony,
7 tracks, `TrainMinors` confirmed `active`. Run entirely on the read-only
counter above (actual vs shipped-formula expected, per track), not on eyes.
**The headline:** track 3 went `els=43 cap=2` → `els=13 cap=1` across a partial
salvage. That is precisely the residual defect the fix covers — the SURVIVING
track never re-runs `GameInit` and would have kept a cap of 2 for a 13-element
track. Every line read `OK` in all four runs. Formula spot-checks all correct:
43→2, 113→4, 74→2, 13→1, 25→1.
**Both sides of the mechanism came out in one run.** The salvage was mid-track,
so it SPLIT: a new track 8 appeared at `els=25 cap=1`, correct on its own via
the engine's deferred `GameInit` — which independently confirms the 2026-07-25
QA correction to the entry (the split-off track was never the defect; the
survivor was).
**Also verified across a reload:** the post-load baseline read correct (`43/2`),
and salvaging again on the freshly loaded track recomputed correctly (`13/1`),
so the fix works on a track object that has just come off disk, not only one
that has been alive in-session. Train counts shuffling between tracks is the
stored-as-prefab behaviour = F49(b), already resolved as no-defect.
*Not proven, and it cannot be from a healthy save:* the `PostLoadGame` sweep's
actual REPAIR of an already-stale cap. Our in-session caps were already correct,
so the reload only demonstrated the sweep is idempotent and does no harm. Proving
the repair needs a save written with the fix absent
(`SMRFixPack_Disabled["TrainMinors"] = true` pre-load) — a relaunch-level
fixture, queued as a TestKit probe rather than a live-save chore.

`Result (a — instant track colour):` **PARKED 2026-07-30 — not run, and
deliberately not attempted again on a live save.** Reaching the instant
`place_track` path needed
`GetInGameInterface():SetMode("track_grid", {grid_elements_require_construction = false})`
— an injection with **no player-facing equivalent**. It misbehaved, and
cancelling out of it left an orphan `Track` with invisible elements blocking
grid hexes on the 305-sol colony (cleared by reload). That violated the
project's own no-live-UI-internals rule (the F76 lesson). **The debris is an
artifact of an unreachable entry path, not a defect in anything — do not file
it.** Superseding question raised by the user and settled by the reachability audit
(`REACHABILITY_AUDIT.md`, lead-pass block): instant-placed track is documented as coming
from "map setup, cheats, the instant-build rule", and **nobody has verified any
of the three is player-reachable**. If none is, F49(a) is in F24's category.
Settle that game-free before any further live attempt; note it also self-heals
on any colour-scheme change. The palette control DID pass, so the test is viable
if a safe route exists: `tracks=4283130509/4283130509 pipes=760202697884/966355804813
distinguishable=true`.

**SECTION CLOSED 2026-07-30 — nothing left to run.** (d) PASSED (above).
(a) settled **R4** by the reachability audit: no `InstantTracks` const exists,
all four track-mode entries default to requiring construction, `PlaceTrackLine`
has exactly one caller, and `Cheats.lua` contains zero track references — so
"map setup, cheats, the instant-build rule" has **zero player-reachable
members**. The (a) wrapper stays only as a cheap no-op rider on a module kept
by (d). (c) closed `wontfix` and its guard REMOVED (`d03417b`) — tier `I`,
designed behaviour, on the tester's live salvage-cursor evidence. F49 holds at
`fixed*` carried by (d).

