# Playtest Archive — completed tests and their results

Completed items from `PLAYTEST_CHECKLIST.md`, moved here verbatim (full test
text + the tester's result notes) so the live checklist only carries un-run
work. `BUGS.md` is the canonical status record; this file is the evidence
trail. Ground rules, save fixtures and the verified command reference stay in
the checklist — consult it before re-running anything here.

**One section here is RETIRED UNRUN, not completed** (PT-54, below): it was
withdrawn before it ever ran because the code under it is being replaced. It
is kept for its trigger designs, which the replacing build's legs draw on. Its
banner says so; nothing in it is a result.

---

## ~~PT-54~~ — Disaster prediction leak, storm wedge, rains deadlock · covered **F78 `Fix_MeteorStormWedge`, F81 `Fix_DisasterPredictionLeak` + `Fix_RainsDeadlock`** — ⛔ **RETIRED UNRUN 2026-08-01, NO RESULTS**

> **This test was never run and must not be run.** Retired by the project
> prompt chain 2026-08-01 because the F86 Tier-1 build deletes and replaces
> `Fix_RainsDeadlock` and reorders the storm-wedge/meteor heal sequencing
> (`SAVE_SAFETY_REDESIGN.md` §6.2; chain prompts 3 and 4). Triggers **C, D and
> E** are absorbed by the Tier-1 build's own legs (A/B pair + the F88
> load-3×-inside-a-rolled-interval regression + the PT-20-method uninstall
> leg). Triggers **A and B** are NOT absorbed — they test
> `Fix_DisasterPredictionLeak`, which Tier 1 does not touch — and were routed
> to chain prompt 3 to be written into `F86_TIER1_BUILD_PROMPT.md` as legs.
> The retirement record and the trigger-by-trigger absorption table live in
> `PLAYTEST_CHECKLIST.md` §3 and on the BUGS F78/F81 entries.
>
> The text below is the test **as written on 2026-07-29**, preserved for its
> trigger designs and its console recipes. Read it as source material, never as
> a procedure to execute against current code.

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

`Result (A reconcile / B warning kept):` **NONE — retired unrun 2026-08-01**

`Result (C heal / D reschedule / E rains):` **NONE — retired unrun 2026-08-01**

---

## PT-59 — First Asteroid prefabs survive a save/load · covered **F83 `Fix_FirstAsteroidPrefabs`** — **PASS IN FULL 2026-07-31** → F83 `tested`

The A/B PT-58 already ran unfixed (**1/1/1** without a reload, **0/0/0** after
one). This is the same A/B with the fix in. **Both halves matter** — the
no-reload half is not a formality, it is the guard against the double-grant trap
that killed the fix's first draft.

**Fixture (kept by the owner, do not lose it):** the PT-58 colony saved BEFORE
the `ReconCenter` tech was ever researched. Loading it restores
`g_ShownPopupNotifications`, so the `show_once` popup re-offers itself on every
run and this test can be repeated indefinitely.

> ⚠️ **TWO asteroid popups arrive from this trigger and only ONE of them grants.**
> Learned the hard way 2026-07-31 — answering the wrong one produced a `0/0/0`
> that read exactly like a fix failure and cost a leg.
> - **`ReconCenterDiscoveryAsteroid`** — titled *"A new Asteroid has been
>   discovered!"*, three buttons **Plan Visit / Detailed Scan / Close**
>   (Detailed Scan is greyed until a Recon Center is built). **NOT the test.**
>   It is F83's *second* site and is graded separately (needs-eyes item 2).
> - **`FirstAsteroid`** — titled *"First Asteroid"*, a **single OK button**, and
>   its body ends in `Effect: Gain Micro-G Auto Extractor Prefabs for every type
>   of resource`. **THIS is the one under test.** The preset declares no choices
>   at all (`PopupNotificationPreset-Asteroid.lua:28-38`), and
>   `WaitPopupNotification` runs the grant callback unconditionally on any answer
>   (`PopupNotification.lua:302-304`) — so there is no "wrong button" *within*
>   this popup, only the wrong popup.
>
> Both sit in the corner list as separate entries. Answer the **First Asteroid**
> one; if the counters read `0/0/0`, check the other notification is still
> waiting before reporting a failure.

**Setup:** load the pre-trigger save. `SMRFixPack.ListFixes` (or the on-screen
loop) must show `FirstAsteroidPrefabs` **`active`**. Pre-flight reads, one line
each (bare expressions echo on screen):
`UIColony.asteroid_count` → expect `0`
`UIColony:IsTechResearched("ReconCenter")` → expect `false`
`SMRFixPack_FirstAsteroidPrefabs` → expect `false`

The counter read used in both legs, one line:
`*r for _, id in ipairs({"MicroGAutoExtractorMetals", "MicroGAutoExtractorRareMetals", "MicroGAutoExtractorExoticMinerals"}) do ConsolePrint(id .. " = " .. tostring(ColonyGetPrefabs(id, MainCity))) end`
(PT-58's own proven line — do not retype it a different way.)

**Trigger A — the reload leg (the fix's whole point).** Load the fixture, fire
the game's own trigger `UIColony:SetTechResearched("ReconCenter")`, leave the
First Asteroid corner notification **unanswered**, quicksave, reload.
   - **EXPECTED:** on load, a log line
     `FirstAsteroidPrefabs: First Asteroid prefabs recovered after a save/load
     (3 granted)`; the counters read **1 / 1 / 1**; `SMRFixPack_FirstAsteroidPrefabs`
     reads `true`; the notification is still in the corner (re-shown as display)
     and opening it shows the normal popup, whose choice closes it and changes
     nothing further.
   - **SURPRISE looks like:** `0/0/0` (the sweep did not identify the
     notification — dump `Notifications[""]` and report), or **2/2/2** (a double
     grant — report immediately, that is the trap).

**Trigger B — the healthy leg must be UNCHANGED.** Reload the fixture fresh,
fire the same trigger, and answer the popup **without** any save/load.
   - **EXPECTED:** counters read **1 / 1 / 1** — exactly vanilla — and
     `SMRFixPack_FirstAsteroidPrefabs` stays **`false`** (our code never ran).
   - **SURPRISE looks like:** `2/2/2`, or the flag reading `true` on a path that
     never reloaded.

**Trigger C — reload twice, still once.** From Trigger A's post-heal state (or
by repeating A), save again and load again.
   - **EXPECTED:** counters still **1 / 1 / 1**, no second
     `recovered after a save/load` line — the persistent flag holds.

Log hygiene: no `[LUA ERROR]` mentioning `FirstAsteroidPrefabs`,
`HealFirstAsteroidPrefabs` or `ColonyAddPrefabs`.

RESULT — **PASS IN FULL, 2026-07-31**, owner at the keyboard. Evidence read off
the sitting's own log (`Mars.exe-20260731-13.18.08`) as well as the counters:

- **(A) reload leg — PASS.** Pre-flight clean (`active` / `0` / `false` /
  `false`, counters `0/0/0`). After trigger + unanswered notification +
  quicksave + reload: counters **1 / 1 / 1**, flag `true`, and exactly one
  `FirstAsteroidPrefabs: First Asteroid prefabs recovered after a save/load (3 granted)`
  line. Answering the re-shown popup afterwards left the counters at 1/1/1.
- **(B) healthy leg — PASS.** Trigger fired, popup answered with no save/load:
  counters **1 / 1 / 1** and `SMRFixPack_FirstAsteroidPrefabs` **still `false`**.
  Vanilla granted; our code never ran. This is the double-grant guard.
- **(C) reload twice — PASS, and exceeded.** The sitting logged **10 game loads
  and exactly 2 grants**, the two grants 14 minutes apart with **7 non-granting
  loads between them**.
- **Log hygiene — clean.** Zero `[LUA ERROR]`, zero error/disabled/FAILED lines
  in the `[CommunityFixPack]` namespace, no `ColonyAddPrefabs` or
  `HealFirstAsteroidPrefabs` in any error.

**Two results the test was not designed to ask for, both worth keeping:**

1. **The heal discriminates against a near-neighbour popup.** The trigger raises
   TWO asteroid notifications from the same preset file, and they sat in the
   corner list together. `find_stranded_notification` picked the right one every
   time — the loc-id match against the live preset is doing real work, not
   merely finding the only candidate.
2. **8 of 10 loads granted nothing.** The no-op path is the common one and it is
   silent.

⚠️ **The procedure was WRONG as written and was corrected mid-sitting** — the
warning block above is the fix, and it is why this section is worth reading
before re-running anything in the family. PT-59 never said which popup to
answer; answering `ReconCenterDiscoveryAsteroid` yields **0/0/0**, which reads
exactly like a fix failure and was reported as one before the source settled it.
Another instance of the standing rule: an un-run PT's procedure is unverified
until it has been executed once.

---

## PT-25 — Destroyed tunnel after a reload · covered **F38** — **PASS IN FULL 2026-07-30** → F38 `tested`

> ⚠️ **The setup line in this test was WRONG and was corrected at the keyboard on
> the day it ran.** It used to say "SAVE-B (or any save with underground access
> — `UIColony:UnlockUnderground()` then `CheatRevealDarkness()`)". The tester
> noticed **the underground build menu has no tunnel at all** and asked whether
> the premise was flawed — the same question that killed F24 and F49(c). It was
> half right: `UniversalTunnel` is the only tunnel in a player-facing build
> category (`Infrastructure`), `Tunnel` and `TrackTunnel` are both
> `build_category = "Hidden"`, and **tunnels are a surface building**. The
> underground reference was pure mis-specification. Fourth PT procedure found
> faulty by executing it, after PT-29, PT-11 and PT-44's F24 half.
>
> **F38 itself survived the challenge:** the defect is
> `OnMsg.LoadGame` → `AllMapsForEach("map", "TunnelBase", Tunnel.AddPFTunnel)`
> (`Tunnel.lua:264-266`), and the buildable Universal Tunnel is in scope —
> `object_class` `TrackTunnelBase`, whose `__parents` include `TunnelBase`, with
> no override of `AddPFTunnel` or `TraverseTunnel`.

**Setup (corrected):** any healthy **surface** save. Build a **Universal Tunnel
pair** across an obstacle so the tunnel is the short route between two points,
park an **RC Rover** on one side with an errand on the other. Cost is 80k
Concrete / 20k Metals / 30k MachineParts, so `CheatFillAllStorages()` +
`CheatCompleteAllConstructions()` first.

**Trigger:** destroy the tunnel (infopanel cheat button, or a meteor), confirm
both ends read as destroyed ruins, send the rover across, then **save, quit to
menu, load**, and send the rover again.

`Result (rover uses the tunnel at all?):` **PASS — confirmed 2026-07-30.** Taken
as a free rider on the setup, because the shipped description claims *"Rovers
cannot use this type of tunnel."* **They can.** That prediction came from the
unit-class mask — `TunnelBase:AddPFTunnel` registers
`pf.AddTunnel(…, weight, -1)` where `Dome_Entrance` passes `2` for "people only"
and `1` for "drones only" — and play confirmed it. Filed as **F84** (description
defect, bundled with the same building's omission of its life-support bridging).

`Result (long way round once destroyed?):` **PASS** — in-session removal was
already correct in vanilla (`OnDestroyed` → `RemovePFTunnel`); this step only
establishes the baseline.

`Result (still closed after reload?):` **PASS — the defect this fix exists for.**
After a full save / quit-to-menu / load cycle the rover **still took the long
way**. Unfixed, the `LoadGame` sweep would have re-registered the destroyed
tunnel and the rover would have walked at the ruin and teleported through.

`Result (works again after repair?):` **PASS — the over-reach guard.** Rebuilt
via the ruin's Rebuild button, the rover **used the tunnel again normally**. The
fix does not permanently blacklist a repaired tunnel. Source predicted this
(`Building:Rebuild` yields a NEW object whose `GameInit` registers normally,
`Building.lua:1655`) but the prediction was verified, not assumed.

**Consequence:** F38 → `tested`. Also retires the **SAVE-B** fixture — PT-25 was
its last consumer, and it turned out not to need it.

---

## PT-58 — First Asteroid prefabs survive a reload? · settled **F83** — **PASS 2026-07-30** (the defect is real)

Purpose-built same-day to convert F83's FirstAsteroid consequence from an
inference into an observation. F83's *mechanism* was already play-proven on a
founder popup; what had never been seen was the one consequence that costs a
player anything.

**Fixture (recipe worth keeping — the popup is `show_once`, so one save gives
one shot):** new game; commander profile **not** `SpaceMiner` (used
`hydroengineer`); game rule `NoUndergroundAndAsteroids` **off**; `ReconCenter`
tech **unresearched**. Pre-flight read came back
`asteroid_count=0 max=1 recon_researched=false profile=hydroengineer`:
```
*r ConsolePrint("asteroid_count=" .. tostring(UIColony.asteroid_count) .. " max=" .. tostring(UIColony:GetMaxAsteroids()) .. " recon_researched=" .. tostring(UIColony:IsTechResearched("ReconCenter")) .. " profile=" .. tostring(g_CurrentMissionParams.idCommanderProfile))
```

**Trigger — the game's own, not a synthetic spawn.** `OnMsg.TechResearched` at
`Asteroids.lua:392-401` spawns the first asteroid the moment the `ReconCenter`
tech completes (unless the profile is `SpaceMiner`). `SetTechResearched` emits
`Msg("TechResearched", …)` (`Research.lua:318`), so granting the tech drives the
real path:
```
UIColony:SetTechResearched("ReconCenter")
```
**Save BEFORE triggering.** That pre-trigger save is the fixture regenerator —
loading it also restores the `g_ShownPopupNotifications` GameVar, which is what
lets the `show_once` popup offer itself again for a second leg.

Prefab read used at every step:
```
*r for _, id in ipairs({"MicroGAutoExtractorMetals", "MicroGAutoExtractorRareMetals", "MicroGAutoExtractorExoticMinerals"}) do ConsolePrint(id .. " = " .. tostring(ColonyGetPrefabs(id, MainCity))) end
```

`Result (control, no reload):` **PASS — 1 / 1 / 1.** Popup opened and answered in
the same session; all three prefabs granted.

`Result (after reload):` **PASS for the defect claim — 0 / 0 / 0.** Re-ran from
the pre-trigger save, granted the tech, **left the corner notification
unanswered**, saved, loaded that save, then opened and answered the popup. The
notification **did survive the load** and opened normally; the choice closed it
and granted nothing.

**Verdict: F83's FirstAsteroid consequence is REAL and observed.** One fixture,
one variable (the reload), 1/1/1 → 0/0/0. A player who leaves the First Asteroid
notification in the corner across a save/load permanently loses all three
prefabs, is told by the popup's own text that they received them, gets no error,
and has no second chance — `show_once` plus an `asteroid_count == 1` gate on a
counter that never resets.

**Not covered here:** the second consequential site,
`ReconCenterDiscoveryAsteroid`'s paid **Detailed Scan**. Its choice 2 renders
*disabled* unless `CanPerformDetailedScan()` is true, which sums Electronics
stored in Recon Centers — a brand-new fixture has the tech but no building. That
half needs its own fixture and its own observation.

**This PASS cleared the gate on F83's fix**, which is now a user decision
(recommended: decouple the grant via an additive `OnMsg.SpawnedAsteroid` behind
its own flag). PT-58 doubles as that fix's ready-made A/B — re-run the same two
legs and the reload leg must read 1/1/1.

---

## PT-44 — Founder trait notice · covered **F23** — **PASS 2026-07-30** → F23 `tested`

> The F24 half was REMOVED 2026-07-30 — it was unrunnable, and F24 is now
> `wontfix` (fix deleted, user call). The step asked you to "build or upgrade a
> dome so the building ends up inside", and the shipped game can do neither: a
> dome refuses to place over existing buildings ("Objects underneath are
> blocking construction", confirmed in play), no dome template carries any
> upgrade, and nothing mutates a dome's interior shape at runtime. Full
> reachability proof on the F24 BUGS.md entry. Third PT procedure found
> unrunnable by executing it (after PT-29 and PT-11).

**F23 — Founder gains a trait.** Probes cover the wiring; play confirms the
notification renders and reads correctly.

**Trigger used:** `founder:AddTrait("Fit")` on a Founder lacking it — the same
call a shipped **Open Air Gym** makes (`OpenAirGym.lua:10`), routed through the
real `Colonist:AddTrait`, which emits `Msg("ColonistAddTrait", …)` synchronously
(`Units/Colonist.lua:427`). `Fit` is `group = "Positive"`, so it passes the
handler's filter, and is benign (+5 DailyHealthRecover).

```
*r ConsolePrint("fired=" .. tostring(SMRFixPack.FounderTraitNotification.fired) .. " existing=" .. tostring(FindNotification("FounderGainsTrait") ~= nil) .. " status=" .. tostring(SMRFixPack.fixes.FounderTraitNotification.status))
```
```
*r local f for _, c in ipairs(MainCity.labels.Colonist or empty_table) do if c.traits and c.traits.Founder and not c.traits.Fit then f = c break end end if not f then ConsolePrint("no founder without Fit found") else ConsolePrint("granting Fit to " .. f:GetDisplayName()) f:AddTrait("Fit") end
```

`Result (notification appears once, names the right trait?):` **PASS —
2026-07-30.**

| Check | Result |
|---|---|
| `SMRFixPack.FounderTraitNotification.fired` | **0 → 1** |
| `FindNotification("FounderGainsTrait")` | `false` → `true` |
| Rendered notification | **"Founder Has Trait" / "Ciara Grant: Fit"** — correct colonist, correct trait |
| Duplicate check | **exactly one** — the dead shipped handler stayed dead |
| Module status | `active` throughout |

**Path vs rendering, stated honestly:** the grant was console-injected, so this
run proves the notification fires, renders and reads correctly — precisely what
this PT exists to check. It does not itself prove the player path, but the path
was never the open question: the reachability audit graded F23 **R1** with a
full enumeration, and a re-grep confirms a dozen live shipped callers of
`AddTrait` on existing colonists (Martian University specializations, School /
SchoolSpire, Sanatorium, Open Air Gym, Project Morpheus, CovertOps, the Dome
`Renegade` path, storybit and faction effect classes).

**Vanilla behaviour recorded so it is never filed as a defect.** This PT used to
say "clicking it selects them". That holds only when the colonist is **visible**.
A notification click runs `ViewCycledObj`
(`Lua/UI/OnScreenNotification.lua:1-19`), which calls `ViewAndSelectObject` only
for an object with `efVisible ~= 0`; a colonist indoors — "Resting in …",
working, at home — falls to the `ViewObjectMars` branch: camera pan, no
selection. Ciara Grant was "Resting in Living Complex" at the time. Correct by
design; you cannot select a hidden unit.

---

## PT-56 — Drone stat dials · covered **D09 `Opt_DroneStatDials`** — **PASS IN FULL 2026-07-30** → D09 `tested`

Two Mod Options dropdowns: **Drone speed** (1x base / 2x / 3x / 5x, percent
added on BASE, additive with speed techs) and **Drone carry capacity**
(+0 base / +1 / +2 on `g_Consts.DroneResourceCarryAmount`). One sitting, any
healthy save with at least one drone (~5 min). Run on a **one-speed-tech save**
(Low-G Drive only, no Artificial Muscles), all six opt-in toggles OFF and both
dials at base going in.

The read used at every step, one line, prints all three values:
```
*r local d = (MainCity.labels.Drone or empty_table)[1] ConsolePrint("speed=" .. tostring(d and d:GetMoveSpeed()) .. " carry=" .. tostring(g_Consts.DroneResourceCarryAmount) .. " dials=" .. tostring(SMRFixPack.fixes.DroneStatDials.status))
```

1. **Baseline reads** (dials at base).
   `Result:` **PASS — `speed=1728 carry=1 dials=active`.** 1728 = 1440 × 1.2,
   the Low-G Drive tech alone; carry 1, no Artificial Muscles.
2. **Set speed 2x + carry +1 → Apply** (no relaunch).
   `Result:` **PASS — `speed=3168 carry=2 dials=active`.** +1440 exactly, i.e.
   100% of the 1440 BASE added additively alongside the tech — **not** a
   doubling of the current 1728. Carry +1. This is the reading most likely to
   produce a false FAIL if the expectation is read as "2x the current value".
3. **Back to base → Apply.**
   `Result:` **PASS — `speed=1728 carry=1 dials=active`.** Exact restore, live,
   no relaunch, no residue; status still `active` (armed-at-base, by design).
4. **Stale-save reconcile:** save with dials ON, set dials to base, reload that
   save → reads must be the step-1 numbers.
   `Result:` **PASS — `speed=1728 carry=1`.** Sequence: saved as
   `PT56-dials-on` while the dials read 2x/+1 and the values read 3168/2 → both
   dials set to base + Apply → **base state confirmed live before loading**
   (`speed_dial=1x (base) carry_dial=+0 (base) speed=1728 carry=1`) → loaded
   `PT56-dials-on` → `speed=1728 carry=1`. The modifiers persisted inside that
   save were stripped on load to match the current dials.
5. **Log hygiene (PT-22).**
   `Result:` **PASS** — log `Mars.exe-20260730-19.37.47`: every module
   `applied`, zero `[CommunityFixPack]` error/inactive/disabled lines, and the
   only `Error` lines in the entire session are the two pre-existing
   `ResManager` `LawOfficeDoor` animation entries. Four `MeteorFrequency:
   persisted Meteors thread on load was DEAD — restarting with the fixed body`
   lines correspond to the four loads the sitting made — F02's watchdog working,
   not a fault.

**Method note earned here (applies to any dial re-run).** Step 4 was scored
wrong on the first attempt: it read `3168/2` and looked like a FAIL, but the
dials had simply not been set back to base before the load, so the reading was
correct behaviour. It was caught by reading the **dial positions** next to the
values —
`Mods["SMR_CommunityFixPack"].options.DroneSpeedDial` / `.DroneCarryDial` —
rather than the values alone. **Verify the base state going INTO the load as its
own step**; scoring step 4 without that check cannot distinguish a pass from a
fail. Combined read:
```
*r local o = Mods["SMR_CommunityFixPack"].options local d = (MainCity.labels.Drone or empty_table)[1] ConsolePrint("speed_dial=" .. tostring(o.DroneSpeedDial) .. " carry_dial=" .. tostring(o.DroneCarryDial) .. " speed=" .. tostring(d and d:GetMoveSpeed()) .. " carry=" .. tostring(g_Consts.DroneResourceCarryAmount))
```

The C-side clamp probe originally queued in this test was run ahead of the
build (2026-07-29 live): no clamp — `SetMoveSpeed(10000)` read back exactly —
and movement stayed clean at 10000 on ultra. Recorded on the D09 entry; it was
not repeated here.

**Consequences:** D09 → `tested` (both BUGS.md places); **the D10 workshops
build is un-gated** (it reuses this same label-modifier dial machinery, which
has now had its first live check).

---

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
   *(⚠️ 2026-08-03, chain-12 QA: the "disable the module" arm is VOID as an
   uninstall test — see the re-label on the result below.)*

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
⚠️ **RE-LABELLED 2026-08-03 (chain-12 QA, the "OFF is three different things"
doctrine): VOID as uninstall evidence, valid as live-toggle pass-through.**
The method was the Mod Options toggle, and a toggled-off module reads clean
by construction — the mod env is still present and `Opt_ResidencyControl`'s
`CanAcceptNewColonists` wrapper installs at FILE SCOPE, so it was still
installed and passing through during this leg. What the leg genuinely
verified: the live toggle restores vanilla behaviour and the reload is clean
*with the pack present*. D03's real-uninstall standing is DERIVED, not
measured (sync-only wrapper — no capturable frames; one plain persisted
dome field, absent-tolerant by design). **No Mod-Manager-disable leg has
ever been run for D03.** Result kept verbatim above; nothing deleted.
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


---

# PRE-REDESIGN SNAPSHOT — 2026-08-03 (entire live checklist, verbatim)

> Appended 2026-08-03 by the checklist redesign (`PT_REDESIGN_PROMPT.md`, owner
> design authority of the same date). The live `PLAYTEST_CHECKLIST.md` was
> rewritten from scratch after this snapshot: per-test format reduced to
> Bug/Setup/Requires/Good-to-have, tests regrouped by system instead of PT
> number, predictions/expected-readings/forensics moved to the agent session
> and the `agent/bugs/` entries. Nothing was lost: this snapshot IS the
> pre-redesign file, byte for byte. PT codes are unchanged across the redesign.

# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game. Fill in the
`Result:` line under each test, then hand the file back (commit it, or just tell the
next session *"read PLAYTEST_CHECKLIST.md results"*). See
**[Reporting protocol](#reporting-protocol)** at the bottom for what happens next.

## Decisions waiting on you

Things that need **your** call, not an agent's. One line each plus where the
reasoning lives; **an agent strikes a line the moment you decide** — just say so
in any session. Added 2026-08-03 by the docs-restructure chain (spec §7 / R10):
these used to be filed only in agent reports, which is where you never read.

- **The mod-page relabel package.** Five shipped fixes (F55 forever-mark, F40
  android dust sickness, F73(b) shelter reflex, F70 template refill, F97
  dust-devil gate) are correct repairs whose *bug-ness* is a design judgment.
  Proposal: a short "judgment calls" section in `MOD_DESCRIPTION.md` so they
  aren't presented identically to, say, F23 or F12. **The wording is yours.**
  → `docs/agent/reports/CHAIN_QA_REPORT.md` §3.
- **The dead `SMRFixPack_Disabled` veto on D03/D07.** The console veto lever
  does nothing for those two modules — only `IsActive` is consulted. Either
  honor it per-call in both, or record that the lever exists only for
  D12/F97-class modules. Nothing measures wrong today, but a future leg that
  used the lever on D03/D07 would silently run live and you'd read the result
  as a fix failure. → `CHAIN_QA_REPORT.md` §5.
- **F46 `Fix_TrainCargoDumping`: move group C → group B.** The record says "no
  route" and a route demonstrably exists (F90's approved shape); the honest
  ground for skipping is cost-benefit, not impossibility. Moving it does *not*
  commit you to ever doing the conversion. → `CHAIN_QA_REPORT.md` §7.
- **The C36-adjacent mysteries grep.** A cheap sweep of `Lua\Mysteries\` and
  `Scenario\` for `IsDisasterPredicted` gates, deliberately left unassigned:
  your call whether it becomes work at all. Not owed. → `CHAIN_QA_REPORT.md` §8.
- **The `DOC_STRUCTURE_REVIEW` recommendations this chain does not adopt** — R4
  (a round-trip step for state-transition claims), R7 (effect-evidencing
  verdicts), R9 (an agent/facts/ review cadence), R14 (a context budget for
  agent docs). Adopt, defer, or drop.
  → `docs/agent/reports/DOC_STRUCTURE_REVIEW.md` §3 and §6.
- **Feed `DOCS_RESTRUCTURE_REPORT.md` to a Fable session to redesign the
  standing prompts.** The docs restructure is done and verified, but
  `FABLE_NEXT_PROMPT.md` and `DRONE_PROJECT_PROMPT.md` still describe the old
  tree in prose — one of them tells every session to read the engine facts as a
  "whole file", which spends the tokens the restructure just saved. The report
  is written for that session as its whole picture. **Your call when to spend
  the top tier on it.** → `docs/agent/reports/DOCS_RESTRUCTURE_REPORT.md` §6.

⭐ **CONVENTION (added 2026-08-03, chain-12 QA, from `BUG_LIST_AUDIT.md`
§10.6f(i)): record the SESSION UPTIME next to any error COUNT.** Cross-arm
count comparisons (this leg's 0 vs that leg's 80) depend on comparable
exposure, and the owner's sessions run 1–6 hours — which makes zero-error
results *stronger* than they read, but only if the uptime is on the record.
One line per leg: "session ~Nh".

**Completed tests live in [PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md)** — 44
sections as of 2026-08-01, of which one (PT-54) is **retired unrun**, not
completed. This file carries **only un-run work**: when a test
completes, its whole section moves to the archive and is **deleted from here,
with no stub or pointer left behind** (see the reporting protocol). The archive
is the notes-and-documentation half; this file is the live work list.
(Cross-checked against the archive and the agent/bugs/ index 2026-07-29 — nothing
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

**A pass here is what earns a fix `tested` status in agent/bugs/.** Probe-verified ≠
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
⚠️ **METHOD CORRECTED 2026-08-01 — a toggle CANNOT answer an uninstall question.** With the module merely switched off the mod env is still present and the hooks are still installed, so any captured frame resolves `SMRFixPack`, reads inactive and no-ops: **it reads clean by construction, whether or not the module leaks.** `Opt_DroneOverhaul` leaked at 98 errors/session with its own toggle OFF — that is how F86 Site 2 was found. Use **Mod-Manager-disable** (measured equivalent to a real uninstall, PT-20: 98 vs 98 on the same save). `agent/facts/`, "OFF" IS THREE DIFFERENT THINGS. A clean read here bounds *that save on that path*; it is not a
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
  (docs/agent/reports/DRONE_OVERHAUL_OPTIONS.md), not a bug in this one.
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
  *(⚠️ METHOD NOTE 2026-08-03, chain-12 QA: the flip-it-OFF arm CANNOT answer
  the uninstall question — a toggled-off module reads clean by construction
  (agent/facts/, "OFF" IS THREE DIFFERENT THINGS). Only the disable-the-pack
  arm is an uninstall test. Line kept verbatim because this section is frozen;
  whoever unfreezes PT-52 must split the two arms into separate steps.)*

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
[PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under its RETIRED-UNRUN banner —
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
protocol (front matter **and** heading tag, both — `INDEX.md` is generated).

---

# 4 · Fixture sittings — batch these by save

## SAVE-A sitting (sandbox; PT-27/28 need the Dust In The Wind rule)

### PT-10 — Open-roof drone observation · covers **F55** ❓ **OPEN QUESTION**

**This test has no expected answer.** The Lua half of F55 (the unreachable-forever
approach cache) is fixed and probe-verified. The *other* half — whether opening a
dome's roof destroys the dome-entrance attaches that carry the only drone pathfinding
tunnels into the dome — is **engine entity data we cannot read from Lua**
(`Lua/Buildings/Dome.lua:404`; see the F55 entry in agent/bugs/). **Either answer is
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
| **P1** | ⚠️ **CORRECTED MID-LEG 2026-08-02 — the original wording was wrong.** It predicted **`73/79`** from `metadata.lua`'s all-`false` `default_options`. **The run read `79/79`**, because **Mod Options survive a Mod Manager disable** and six opt-in modules were left on in that profile (agent/facts/). The count to predict is therefore **79 registered**, with active = 73 + however many opt-in toggles are on — **read `CurrentModOptions` or `ListFixes()` before writing the number, never the defaults.** A miss on the *registered* half still means a module failed its self-check; read the detail string first | a module failed its self-check, or the count arithmetic is wrong — either way, read the `ListFixes()` detail string before anything else |
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
> ⚠️ **The RATE question is NOT settled** — see the per-preset table on agent/bugs/ F97.
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

## PT-62 — PARTLY RUN 2026-08-02 (attended). ⚠️ NOT PASSED — results and what is still owed

**Log `Mars.exe-20260802-22.28.07` (suite) and the sitting either side of it.
Fixture: the owner's live campaign, two flagged domes — `Sacagawea #2`
(retirement, DomeMega) and the nursery DomeMedium.**

### ⭐ The core result, and it is the one the module exists for

Same colonist, same moment, module toggled:

```
vanilla says   false nil
with D12       DomeBasic shuttle
```

Vanilla had **no** answer — the tie — and D12 supplied a reachable dome with
housing the colonist can use. `DomeBasic` reads `free 0`, which is the design
working as specified: **suitability, not free space**, or the module would be
inert in its own origin case.

⚠️ The tie had to be RESTORED first, and that is disclosed fixture
construction, not a found state. The save had drifted since 2026-07-30: two
domes offered free work, so `better_work` was true and vanilla was already
willing to move them (`vanilla says GeoscapeDome shuttle`). Quarantining
`GeoscapeDome` and one `DomeMedium` returned the reading to `false nil`. **Both
before/after readings are the evidence that the quarantines restored the tie
rather than manufactured the result.**

### What PASSED

| # | result |
|---|---|
| **P2 / P2b / P2c** | ✅ `78 PASS, 0 FAIL, 9 SKIP, 0 ERROR`; `DustDevilSpawnGate` PASSes (the 8c debt, discharged); the probe's own tie-control holds |
| **P5** | ✅ colonists go outside **only to board a train or shuttle** — the shipped transit path. Nobody stranded, no deaths |
| **P8b** | ✅ the row tracked correctly through a population surge: `28 moving out` against `43 homeless`, 15 exempt — the same proportion as before the surge |
| **P11** | ✅ **zero `[LUA ERROR]`** across the whole sitting, under an active drain and an inflow. The log carries nothing but the pack, the suite and the operator's own diagnostics |
| ⭐ exemption | ✅ observed live and unprompted: a dome with **17 homeless** showed **13 movable**, and the sample held back Seniors, the employed, and the transiently unable |

### ⛔ What did NOT establish, and why

**P4 and P6 are NOT established.** The drain was fighting an inflow the whole
time — `Sacagawea #2` went 20 → 43 homeless while flagged and draining, with
colonists arriving by train and walking straight back in. The numbers from this
sitting mean nothing for those two predictions and **must not be recorded as a
result either way.**

### ⭐⭐ THE FINDING: the policy pushed but never DECLINED, and the pair looped

Measured, not inferred — **6 colonists were en route INTO flagged domes** while
those domes were draining. The mechanism:

1. D12 pushes an unemployed colonist out of a flagged dome;
2. the dome drops below `IsOverpopulated`, so its free cohort slots start
   scoring ~97 again in `Community:GetScoreFor` (`Community.lua:376-391`);
3. vanilla offers **the same dome** straight back to the same colonist;
4. repeat — burning shuttle capacity and never converging.

The ping-pong guard only stopped **D12** choosing a flagged dome. It could not
stop **vanilla's own eval** choosing one.

### ⚠️ THREE CHANGES BUILT IN RESPONSE, ALL UNRUN

1. **The symmetric half** — a flagged dome now refuses to RECEIVE the class it
   pushes out (`FindEmigrationDome`). ⚠️ This is the **only** place the module
   overrides a positive shipped answer.
2. **The second entry path** — `ChooseDome` (rocket/lander arrivals, re-homing)
   was never guarded, so a landing could refill a draining dome. Now filtered,
   **trait-based**, because that seam has no workplace to read.
3. **The A/B lever was DEAD.** `SMRFixPack_Disabled.NoHomeless = true` was
   silently ignored — the module read only `IsActive`. ⚠️ Same shape as PT-61's
   `rawget` trap: *the failure would not have looked like a broken command, it
   would have looked like an ANSWER.* Caught because the owner asked whether the
   line was correct, before the leg leaned on it.

### What a re-run must do

⛔ **Restart first** — all three changes need it. Then:

1. `*r SMRTest.RunAll()` — expect `78 PASS, 0 FAIL, 9 SKIP, 0 ERROR`.
2. **The loop check, which is now the leading indicator:**
   `*r local bad = 0 for _, city in ipairs(Cities) do for _, c in ipairs(city.labels.Colonist or empty_table) do local d = c.emigration_dome if d and d.SMRFixPack_no_homeless then bad = bad + 1 end end end ConsolePrint(print_format("heading INTO a flagged dome", bad))`
   — must reach **0 and stay there, through a rocket landing**. The emigration
   veto alone would not survive one; that is what tests the `ChooseDome` half.
3. Only then are **P4 and P6** meaningful. Run them with D03's **"Closed to new
   residents"** on as well, so arrivals cannot refill the dome from a landing
   — that composition is HARD CONSTRAINT 1 in use and was never in the original
   plan.

---

## PT-62 (as written before the run) — D12 "no homeless residents" policy · covers **D12 `Opt_NoHomeless`** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 10

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

**Trap 1b — the dome must actually HAVE a Nursery or a Retirement Home built in
it** (owner precondition, 2026-08-02). No cohort housing means **no row at all**
and an inert flag, checked in the wrapper as well as the UI so the two cannot
disagree. Two consequences for this leg: a production dome is not a valid
subject no matter how many unemployed homeless it holds, and **Ctrl+click
broadcasts to Nursery/Retirement Domes only** — not to every dome in the city,
which is what the shipped broadcast would have done.

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
the PT-20 method (`agent/facts/`, "OFF" IS THREE DIFFERENT THINGS).

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

**⚠️ EXPECT THE HOTEL DOME TO BE A POPULAR DESTINATION, and do not report it as
a defect.** A Hotel set to **"Any Colonist"** has `exclusive_trait = false`
(`HotelBase:SetTouristOnly`, `Hotel.lua:6-27`), i.e. it is ordinary housing with
free beds — and hotels live in the best-services, best-comfort dome by
construction, because that is where players want tourists. D12 prefers a
destination that can house someone *now* over one that cannot, so pushed
jobseekers will tend to land there. **That is correct**: it is the only place
with an actual free bed, those colonists get housed rather than merely relocated,
and the player opened the hotel themselves. Two things to watch rather than
assume: whether it eats tourist capacity the player wanted kept, and whether a
Hotel left on **"Tourists Only"** is correctly never offered (it should be —
`IsSuitable` fails for a non-Tourist).

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
(`agent/bugs/` C40, mechanism verified vs Src, harm unproven). **D12 does not fix it
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
> being *called* afterwards (agent/facts/; drone Q1/Q2 sitting — the read
> returned `function: 000001E95D57A6B0` with the module uninstalled, and it
> re-filed queue entries using the vanished mod's logic, with **zero errors in
> the log**). A silent, error-free session therefore does **not** prove the pack
> left nothing behind.
>
> **Step 5 — hunt for surviving pack code, with the pack DISABLED:**
> - **`Fix_MeteorFrequency` is the specific suspect** and the reason this step
>   exists. It assigns our function to `GlobalGameTimeThreadFuncs.Meteors`
>   (`Code/Fix_MeteorFrequency.lua:70`), game-time threads persist **with their
>   blocked stacks** (agent/facts/), and the pack's own load line
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
CODE MEASURED AT TWO SITES. Filed as `agent/bugs/` F86 (P1, blocks release).**
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
> - **`debug.getinfo` is unavailable** (mod sandbox — agent/facts/, and it is why
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
taken; row struck through below, full record on agent/bugs/ F35).

| Subject | The one observation, and what it decides |
|---|---|
| ~~**F35 live-label check**~~ **✅ TAKEN AND CLOSED 2026-08-01 — no longer a rider.** Measured at the keyboard during the F86 Phase-0 sitting (log `Mars.exe-20260801-14.59.57-6a22b86d.log`): from a **pre-research save**, all three turbine labels read `NO MODIFIERS` before, and after the tech landed all three — **`WindTurbine_Large` included** — carried `prop=electricity_production percent=100` under the vanilla `Effect_ModifyLabel` keys (`id=GameEffect`, not `SMRFixPack_F35_*`), with **Power doubling on every one** (9.3→18.6 / 18.6→37.2 / 29.8→59.5). No reload in the window, so our pass could not have supplied it. **The audit’s live-miss suspicion is dead and F35’s scope is right.** Trigger: the tech was granted with `UIColony:SetTechResearched("FrictionlessComposites")` — it is a Breakthrough and was unobtainable in that colony — which is the same `EffectsApply` funnel natural completion uses (`Research.lua:313`). ⚠️ **Read the trap on the agent/bugs/ F35 entry before repeating this anywhere:** the first attempt read the labels while **Low-G Turbines** was completing, which grants upgrade unlocks and no label modifier at all, and its correct `NO MODIFIERS` result nearly got filed as a P1. Confirm `IsTechResearched("FrictionlessComposites")` first. Full record: agent/bugs/ F35 |
| **C32 label-membership read** ⚠️ **REWRITTEN 2026-08-01 by the prompt-6 Src sweep — the old row's trigger no longer occurs and its pass/fail rule was wrong; do not take the old version.** | **Trigger (corrected): you must ABANDON an asteroid** — the manual button, `Asteroids:UIAbandonAsteroid` — because on 1.0.7 asteroids never expire on their own (`Asteroids.lua:1, :208, :331-348, :493-500`), so "visiting and leaving" unloads no map and reads nothing. **Read (corrected): destroyed buildings must be excluded, or the first meteor strike will "confirm" C32** — `Building:OnDestroyed` is empty while `ShiftsBuilding:OnDestroyed` de-labels, so every destroyed-but-unrebuilt building legitimately sits in `UICity.labels.Building` and outside the colony label: `*r local n = 0 for _, b in ipairs(UICity.labels.Building or empty_table) do if IsKindOf(b, "ShiftsBuilding") and not b.destroyed and not b.demolishing and not b.bulldozed and not UIColony:IsInLabel("ShiftsBuilding", b) then n = n + 1 end end ConsolePrint("live ShiftsBuilding missing from the colony label: " .. n)` — and note it now tests membership with `IsInLabel` (the engine's own key-map test, `CommonLua\LabelContainer.lua:106-109`), not `table.find`, because the two disagree exactly in the array-vs-key desync case. **A non-zero count is the defect; a zero count still proves nothing** (`UICity` follows the current map, `Lua\_init.lua:12-14`, so read it on the map whose buildings you care about). Decides C32 (agent/bugs/ C32 entry, which the sweep DOWNGRADED — mechanism has no route in current Src) and feeds prompt 7's F04 tier decision |
| **F80 settling observation** ⭐ **REWRITTEN 2026-08-02 (prompt 6c source audit) — it now discriminates WAITS vs WALKS and tests a named directional prediction** | **Trigger: any train sitting where EITHER symptom appears** — colonists queued at a platform while trains come and go (*waits*), **or** colonists setting off overland past a working station (*walks*). The audit says these are two faces of one enumeration, so **the walk case is now equally valid evidence and is the commoner one in the wild** — do not skip the sitting because nobody is waiting. ⛔ **Tap before mitigating: adding trains destroys the evidence.** Take all three, in order: **(1) Classify.** Waiting or walking? Note which, and the origin/destination **pair** that fails — the audit predicts a *specific pair* failing inside an otherwise healthy network, **not** a network-wide break, so a global failure would falsify the theory outright. **(2) The ready console tap** on the global `ForEachStationAlongTrack` (recorded in the F80 entry) — it prints each stop's enumerated destination set. **(3) ⭐ The directional test, which is the new discriminator and is free**: call `GetReachableStations()` on **both** endpoints of the failing pair. **The predicted signature is a ONE-WAY HOLE** — A's list omits B while B's list contains A (or the mirror). **PASS/consistent-with-F80 = a one-way hole.** **FALSIFIES the enumeration theory = both lists name each other** (the walk is then a decision made downstream of a correct reachable set, and the mechanism is elsewhere entirely). Also record whether a **track segment was under construction** anywhere on the line at the time — that is a legitimate rival explanation the audit confirmed is by-design truncation (`TrainTransport.lua:421`), and it must be excluded before the reading counts. F80 is the audit's strongest reported-but-unpinned defect (§4): Relaunched witness, a dev note, an exact source predicate as of 2026-08-02, and still **no proven trigger** |
| **C25 Jumbo Cave trigger check** ⭐ **ADDED 2026-08-02 (prompt 6b) — waits for the situation; take it the moment a Jumbo Cave Reinforcement site sticks** | **Only the trigger is unproven** (the wedge chain is Src-verified on the C25 entry) — i.e. does cave geometry actually strand a waste rock? **Take the read WHILE the site is stuck, and while looking at the UNDERGROUND map** (`UICity` follows the current map, `_init.lua:12-14`): `*r local n, rocks, stuck = 0, {}, 0 for _, d in ipairs(UndergroundMap.City.labels.Drone or empty_table) do for b in pairs(d.unreachable_buildings or empty_table) do if IsValid(b) and IsKindOf(b, "WasteRockObstructor") then n = n + 1 if not rocks[b] then rocks[b] = true if b.parent_construction then stuck = stuck + 1 end end end end end local u = 0 for _ in pairs(rocks) do u = u + 1 end ConsolePrint("waste-rock entries in drone unreachable tables: " .. n .. " over " .. u .. " distinct rocks, " .. stuck .. " of them attached to a construction site")` — the `IsValid` guard is required because the table also holds a plain `version` key (`Drone.lua:826`). **Reading: a non-zero `attached to a construction site` count while the site is stuck is the trigger, and C25 earns its F-row; ZERO while stuck means the wedge is something else and C25's mechanism is not the cause** (record that too — it is the more useful result). ⚠️ **Also record the save's vintage.** 1.0.6 replaced the whole Jumbo Cave scenario and the swap is gated on `UndergroundRework106`, which is **false in any save started before 1.0.6** (`UndergroundDome.lua:16-19`) — so state whether this colony was begun pre- or post-1.0.6, or the observation cannot be placed. Decides C25 (agent/bugs/ C25 entry) |
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
| **F90 underground-break rider** ⭐ **ADDED 2026-08-02 — take it the first time a dust storm arrives on a colony that has an elevator** | **Why a rider and not a probe: the defect is a VICTIM DISTRIBUTION, not a single event.** "No underground break happened this session" is what an unfixed game looks like most sessions too, so a one-shot in-play check cannot discriminate; the probe covers the filter itself (it asserts what vanilla's body was handed). **Preconditions that must all hold or the reading is void:** underground unlocked, **at least one elevator built** (that is what merges the grids — without it there is nothing cross-map and the fix's fast path returns untouched), a surface dust storm running, and the merged fragment holding **more than 10 connectors** (`IsBreakable`, `SupplyGrid.lua:693-697`). **The read:** while the storm runs and for a while after, **zero NEW `PowerLeak` / `LifeSupportLeak` notifications on the UNDERGROUND map**. ⚠️ **Exclude cave-ins before counting anything** — marsquakes and `CaveInRubble` break underground elements *on purpose* (`CaveInRubble.lua:158` is one of `:Break()`'s eight call sites), and that is exactly why the cheaper `Break`-interception fix was rejected as unsound. A leak that follows a cave-in is not evidence. **Non-zero underground leaks during a surface-only storm = the filter is not holding.** ⚠️ **Known residual, do not file it as a miss:** surface cables on an elevator colony still break somewhat MORE often than on a non-elevator colony — the break *probability* counts `#self.elements` and stays cross-map by decision. Full reasoning: agent/bugs/ F90 |
| ~~**F93 dust-devil map rider**~~ ✅ **RUN AND PASSED 2026-08-02, in its STRONG form, as a free by-product of PT-61's vanilla half** — and it was the owner's own idea to switch maps mid-leg "to confirm waves spawn regardless of which map is focused". **The case taken was the strongest one on offer: `CurrentMap.mapdata.MapSettings_DustDevils` read `disabled` on the underground while `MainMap` read `DustDevils_VeryHigh_3`.** Without F93 that is not a wrong-intensity read, it is the **nil** branch — `GetDustDevilsDescr`'s first line returns nothing, and the scheduler enters `while not new_descr do Sleep(const.DayDuration) end`. **Observed instead: seven consecutive descriptor reads returning `DustDevils_VeryHigh_3` with the camera underground, and the 4-hour wave cadence unbroken from sol 8 h11 through sol 9 h12** (log `Mars.exe-20260802-16.25.43`). ⭐ **The cadence is what makes this decisive** — a day-long park is a 24-hour gap against a 4-hour rhythm and could not have been missed. ⚠️ Attribution note: the camera window is by the owner's report (switched after wave 2, still underground when the `CurrentMap` read was taken after wave 10); the log timestamps and the returned preset id are the hard evidence. Original rider text follows. | **Why a rider: the probe drives the getter with stand-in maps, which proves the read follows `MainMap` but not that the live scheduler benefits.** **The read:** with the camera on the **underground** map, `*r local d = GetDustDevilsDescr() ConsolePrint(d and (d.id or "descriptor with no id") or "NIL — the scheduler would park a day at a time")`, then switch to the surface and repeat. **The two must agree.** ⭐ **The strong version costs nothing extra**: do it on a map pair whose dust-devil settings actually DIFFER, or with the underground set to `disabled` — that is the case where vanilla returns `nil` and the surface scheduler stops producing dust devils a day at a time until the player looks back at the surface. A matching pair on two identically-configured maps proves much less; say which case was taken. Decides nothing on its own (the defect is source-verified and the fix is a 7-line copy) — it confirms the live path, and a **disagreement** would mean the replacement is not the function the scheduler calls. Full reasoning: agent/bugs/ F93 |

### From the chain-11 F76 sitting — one rider, because the entry was refuted and the residue still needs eyes

**Added 2026-08-02 by chain prompt 11.** The F76 attended sitting **falsified**
the entry's positioning claim by measurement and its load failure **did not
reproduce**; F76's disposition is routed to chain prompt 12 job 10 and is not
decided here. This rider exists for one reason: **if the symptom recurs during
the campaign, it must be captured with instrumentation and not as another verbal
report.** The nine-day detour F76 caused traces directly to a screenshot plus a
description, taken without the one line that would have settled it.

| Subject | The one observation, and what it decides |
|---|---|
| **F76 depot-picker recurrence rider** ⭐ **ADDED 2026-08-02 — take it ONLY if a depot/heap click-load misbehaves again; do NOT go looking for it** | ⛔ **The picker is VANILLA and was measured CORRECT** (`anchor (2051,887)` vs live `mouse (2058,885)`; box centred on the anchor x with its **bottom edge AT** the anchor y; every number matching prediction to the pixel). **It opens ABOVE the cursor by its own height (429px at 4K), which is intended** — do not report that as displacement, and do not avoid the picker on the strength of the old warning. **Preconditions:** an RC Transport or RC Dozer, a StorageDepot or waste-rock heap with stock, Load mode. **If it misbehaves, take BOTH lines before touching anything else** — the second one is the one nobody had: **(1)** `*r local n=0 local o=ResourceItems.UpdateLayout function ResourceItems:UpdateLayout(...) local r=o(self,...) if n<8 then n=n+1 local m=terminal.GetMousePos() ConsolePrint(print_format("F76#"..n, "anchor", self.align_pos, "box", self.box, "cont", self.idContainer and self.idContainer.box, "scale", self.scale, "mw", self.measure_width, "mh", self.measure_height, "mouse", m)) end return r end` — **read: does `anchor` equal `mouse`, and is `box` bottom-centred on it?** **(2)** `*r local o=ItemMenuBase.OnMouseButtonDown function ItemMenuBase:OnMouseButtonDown(pt,button) ConsolePrint(print_format("F76MISS", button, pt)) return o(self,pt,button) end` — **read: does `F76MISS L` print on a click that looked like it hit the hex?** If it does, the click missed the button and was forwarded to the world (`ItemsMenu.lua:510-518`), which selects an object, closes the picker via `OnMsg.SelectionChange`, and runs `ExecuteLoad` on an empty `to_load` → bare `return`: **a sound, nothing loaded, no error.** ⚠️ **Also record `terminal.desktop.box` and whether the game window is on a display that is NOT at the virtual desktop origin** — one pass in the sitting logged `mouse (6148, 2350)` outside a `(0,0)-(3840,2160)` desktop, and an out-of-range anchor is the one mechanism that WOULD slam the dialog into a screen corner (M5 on the F76 entry; unproven, and there is no persistent offset on the owner's machine). ⚠️ **A DIFFERENT symptom is also open and must not be confused with this one:** `BUG_LIST_AUDIT.md` §2.2's original-game witness is *"the icon which should appear … does NOT appear"* — no picker at all, against this entry's picker-in-the-wrong-place. If that is what you see, say so explicitly; it has never been reproduced. ⛔ **Both hooks above are READ-ONLY and that is deliberate** — the 2026-07-27 hard-lock happened under a wrapper that MUTATED `align_pos`, and the no-live-UI-internals-prototyping rule still binds. Full reasoning: agent/bugs/ F76 |
| **C40 Crowded Living capacity rider** ⭐ **RE-ROUTED HERE 2026-08-02 by chain prompt 11 (chain rule 2 — it was routed TO prompt 11, whose sitting was a sol-4 founder colony with no such law, so it was never available to take). Take it opportunistically the first time a colony has `Crowded Living` enacted AND a Ministry of Culture built.** | ⛔ **Not a defect hunt — the live gating is INTENDED and the ministry advertises it** (`MinistryWelfare.lua:23,:26`). What is open is the **law's own description**, which interpolates only the static `<capacity_increase>` (3), so a player is told "+3" while possibly receiving **+6**, with nothing saying that losing the ministry takes homes away from people who already have them. **The observation (one minute, no fixture):** with the law enacted and the ministry **working**, note a Residence's `capacity`; then stop the ministry (turn it off, or cut its power) and read the same Residence again. **Reading: capacity drops by 3 = both `LawEffectModifyLabel` and `LawEffectModifyLabelMinistryWorking` are live and the description under-reports by half.** ⚠️ **Then watch what the drop does** — `Residence:OnModifiableValueChanged` evicts tail residents colony-wide until each building fits its new capacity (`Residence.lua:224-235`), and re-houses from `dome.labels.Homeless` on the way back up (`:238-242`). **On a colony with no spare beds those colonists go homeless.** Record whether anyone was actually evicted, because **harm is unproven and frequency is unmeasured** and this entry deliberately does not guess. ⚠️ **Do not expect ordinary shift rotation to trigger it**: MinistryBase runs a single shift satisfied by any one worker (`FactionsBuildings.lua:360-362`), so it takes losing the whole shift, a power gap, or a maintenance stop. ⭐ Worth one line of context: C40 came from a **Reddit player's hypothesis** that a chain brief said to *check, not adopt* — the player was right about the mechanism, and checking it before building is what chose D12's narrow reading. Full reasoning: agent/bugs/ C40 |

---

## Rider — F11: can crew-gathering desync a train's passengers? · ✅ **RUN AND SETTLED 2026-08-03 (attended) — NO, IT CANNOT**

> Moved whole from `PLAYTEST_CHECKLIST.md` on 2026-08-03, the sitting that ran
> it. **This is the reachability audit's settling observation, delivered.** The
> answer refutes the hypothesis the rider was written to test: crew-gathering
> abduction keeps `train.units` synced on BOTH maps, so F11's guarded state has
> no demonstrated producer. Full write-up, citations and the corrected route:
> `docs/agent/bugs/F11.md`. Evidence log copied to
> `docs/archive/logs/Mars.exe-20260803-22.23.59-6a22b86d.log`.

### The rider as it stood (pre-run text, verbatim)

**Bug:** the train-wedge fix is shipped and probe-verified; what is left open
is whether the state it guards against — a passenger yanked out of a moving
train by a crew-gathering expedition — can actually occur. Either answer is
useful data. → [F11](../agent/bugs/F11.md)
**Requirements:** None / any colony with a running train carrying a passenger
+ an expedition ready to launch.
**Setup:**
1. In any sitting with a colonist mid-ride on a train, launch an expedition
   that crew-gathers busy colonists.
2. The agent inspects `train.units` afterwards (one read, on the entry).
**Good to have:** TrainsLogging on beforehand — its "not in train" warn
catches the desync on its own.

⛔ **That setup was NOT RUNNABLE AS WRITTEN, and that is the fifth time a PT's
own procedure has failed on first execution** (PT-29, PT-11, PT-25, PT-59, now
this). Two independent reasons: (a) which colonist the gatherer picks is a
lottery the tester cannot steer, and (b) the owner had exactly one manned
expedition left in the campaign, so a design that consumes an expedition per
attempt was unaffordable. The run below consumed **zero** expeditions.

### How it was actually run

**The gathering half was never played — it was settled by reading**, because
"can the picker reach a rider" is answerable from the pool construction at
`Lua/Buildings/CargoTransporter.lua:240-251`. Rebuilding that pool live gave
the rider at index **1513** of **1543**. Since an underground colonist cannot
be in `MainCity.labels.Colonist`, the only thing that could have put them there
is the `GetConnectedCitiesForColonists` append — so a surface rocket's crew
gathering **does** see underground train riders. Reachable, proven, no launch.

**The abduction half was driven by invoking the shipped call site directly** —
`col:SetCommand("EnterTransporter", rocket)`, verbatim the body of
`CargoTransporter:ExpeditionLoadCrew` (`CargoTransporter.lua:300-302`) — on a
chosen target instead of one the gatherer picked. That removes the lottery
without changing the mechanism.

### Readings

| reading | value | meaning |
|---|---|---|
| rider's command aboard | `BoardVehicle` | P1 ✓ — not Idle/Abandoned, so eligible as a busy colonist |
| `table.find(train.units, col)` before | `1` | the counter reads |
| pool index / pool size | `1513` / `1543` | P2 ✓ — reachable by a surface rocket's gatherer |
| `col:GetMap() == MainMap` | `false` | rider is underground |
| `rocket:GetMap() == MainMap` | `true` | transporter is on the surface |
| `col.city == MainCity` | `false` | rider belongs to the underground city |
| `col.holder == rocket` after | `true` | the abduction actually executed |
| `#train.units` after | `6` | the list is live and populated |
| **`table.find(train.units, col)` after** | **`nil`** | **the rider was removed cleanly** |

⭐ **The counter is honest and that was designed in, after PT-62's lesson that
"an objective counter is only objective if it can FAIL."** `#train.units` = 6
rules out an empty-or-nil-list artifact; `col.holder == rocket` = true rules out
"the call did nothing". A stale entry would have printed a number. It printed
`nil`.

### Verdict

**F11's abduction route does not produce the stale state.** `EnterTransporter`
→ `SetHolder` → `SetHolderOnMap` → `holder:OnExitHolder` → `Holder:OnExitHolder`
→ `table.remove_entry(self.units, unit)` (`Holder.lua:36-37`) — the correct API,
and it fires even when `TransferToMap` runs first on the cross-map path. The
audit's "bottoms out in engine-side `TransferToMap`" hypothesis is **refuted by
measurement**, and the "not R2" verdict now rests on evidence rather than
inference. The fix stays — it is a correct repair of a real `table.remove`
misuse in shipped code — but its hypothesised trigger is measured absent.

⚠️ **What it does NOT prove:** that `train.units` can never go stale by some
other producer. It proves the one producer the shipped dev comment names
(`--abducted by CargoTransporter?`) does not do it.

### Two corrections this run forced onto the record

1. **The old entry's citation was the wrong class in the wrong file** —
   `Lua\Units\CargoTransporterNew.lua:221-234`, where the live path is
   `Lua/Buildings/CargoTransporter.lua:272-285` and `CargoTransporterNew` is a
   separate class expedition rockets never touch. The conclusion survived; the
   route did not. Recorded on the entry rather than quietly fixed.
2. **The owner's witness explains the "expeditions never take busy colonists"
   appearance** — the stall is trait scarcity, not busy-refusal, cured by import
   or university training exactly as the owner described. Detail on the entry.

---

## Resolved decision records — moved from "Decisions waiting on you" (worked example, 2026-08-04)

> **Format note (unattended-1 terminal audit, 2026-08-04).** The checklist's
> documented archive rule covers completed *test sections*; struck-through
> *decision bullets* are a different shape with no precedent. These two are
> moved as a **worked example** of the proposed treatment — the resolved
> bullet moves here WHOLE, verbatim, no stub left behind, only when it is
> fully closed (nothing owed to the owner) and its durable content already
> lives in an entry, `SESSION_LOG.md`, or an archived log. **The general
> question — apply this to the rest of the resolved bullets? — is routed to
> the owner on the checklist.**

- ~~**Schedule co-run #0**~~ — ✅ **DONE 2026-08-04, you said go and it passed.**
  It cost you **~1.5 minutes** against the ~10 asked for: no Steam picker, no
  click needed, no modal, nothing to judge. The whole cycle was **79.9 seconds**
  launch to desktop, the 56 MB load took **10 seconds**, and there was not one
  `[LUA ERROR]` in the log. Your `TEST2H TRAIN` save is untouched; the copy and
  the probe are deleted. → `docs/archive/SESSION_LOG.md` 2026-08-04 (the spec
  was consumed at chain close 2026-08-04; full text in git,
  `git show 93088ba:docs/agent/prompts/corun-rig/CORUN_RIG_SPEC.md`).
- ~~**The vanilla `LawOfficeDoor` missing-asset error — file or ignore?**~~
  ✅ **DECIDED 2026-08-04: filed as `C44`, `wontfix`, closed.** You asked for a
  reason on it *"so another agent doesn't get distracted by it again"* — the
  entry now opens with a **STOP HERE** banner saying exactly that, above the
  evidence. Nothing is owed and nothing will be built. → `agent/bugs/C44.md`.
