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

Archived 2026-07-27 (later): PT-14 (DONE — **premise falsified**: the
accept-colonists toggle is a **quarantine** — its OFF state is titled
"Quarantined" and the rollover promises "Colonists are not allowed to enter or
leave" — so the lockdown the tester observed is designed behavior, not F61's
defect; F61 CLOSED `wontfix` same day by user decision, fix deletion staged,
community ask re-filed as D03 `Opt_ResidencyControl` — full evidence on the
F61 + D03 BUGS.md entries).

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

