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

## PT-47 — Bombardment volley shape (F26) — ⭐ **RAN 2026-08-10 (`corun-batch-2` leg R): PASS on every SAMPLED check** · NOT `tested` (volley forced) · moved here by the batch-2 terminal audit

**Result (sitting 2026-08-10, owner at the keyboard; full readings and the
three agent-side reader defects on `agent/bugs/F26.md`):** five forced
`StartBombard` volleys — spread reads as a **scatter** from a low camera
(owner: *"trails seemed scattered"*), volley **ENDS 5/5** (peaks 5/6/6/7/7,
each with its liveness witness), dome crack **POSITIVE** ("Hoffman #1 - 3
fractures"), "Incoming Missile" notification **appears**, interception
**POSITIVE** via the owner's own MDS-on/off A/B (peak 5/6 → 7 same dome, same
speed). Logs `archive/cb2sitting_Mars.exe-20260810-15.30.16.log`.

⚠️ **Residue, deliberately NOT owed anywhere:** decal fade is UNSAMPLED (no
working instrument on either side — the `DecRocketSplatter` read returns a
non-table) and the notification's CLEARING half was not separately confirmed.
Neither has a live checklist line: F26 stays `fixed`, the entry records both
gaps, and re-sampling them is only worth scheduling if F26 ever regresses.
⚖️ Audit note: one vanilla engine `[ERROR]` line sits in the leg's window
(→ `agent/bugs/C45.md`); it does not name pack code and no verdict rests on it.

The section as it stood on the live checklist, verbatim:

> ### PT-47 — Bombardment volley shape (F26) · **mode: co-run** (routing
> 2026-08-04 — your eyes: scatter-vs-rank; forcing + integrity checks rig-side)
> **Bug:** Mystery 7 bombardment missiles flew in a parallel rank instead of a
> scatter. The fix is the pack's largest copied function (100 lines), so
> "nothing else about a bombardment broke" is half the test. → F26
> **Requirements:** a Mystery 7 bombardment, or any save + the console force
> (the agent hands it, entry) / a low camera angle so the trails are visible.
> **Setup:**
> 1. Watch a volley arrive — scatter, not a rank.
> 2. The agent walks the five integrity checks from the entry (decals, dome
>    cracks, notification, interception, and the volley ENDING).
> 3. Log check for bombardment errors.
> **Good to have:** an off/on A/B of the spread — that is the reachability
> audit's settling observation for F26. *(The owner supplied exactly this,
> unprompted, by disabling the MDS lasers for volleys 4–5.)*

## Rider — popup-audit keystone: storybits survive save/load — ⭐⭐ **ANSWERED 2026-08-10 (`corun-batch-2` leg P): BOTH HALVES PASS** · moved here by the batch-2 terminal audit

**Result:** a storybit popup-carrying thread **survives a save/load**
(`g_StoryBitActive=1` before and after with the read taken immediately before
the save; run_thread handle rebuilt …ACC4F98 → …C596698 across the load) **and
answering it after the reload still applies the outcome** (`ArcadiaCross`
reply 1 taken; its named consequence — an RC Explorer removed — verified by
the owner's eyes against the pre-answer save: *"yes it disappears"*). This is
`POPUP_CONSEQUENCE_AUDIT.md` §8 item 1, answered: storybit popups are NOT in
F85's voidable class — they wait in game time.

⚠️ **Run 1 (`AnythingForLove`) was VOID as a keystone sample** — no read
between activation and save (the gap was ~15 min by the log's own timestamps,
not the ~8 min the sitting recorded). ⚖️ **Audit attribution 2026-08-10:** the
sitting's "unattributed modal at ~16:02, in no log" IS in the log —
`Story bits: Reply selected - I can't say no to a hopeless romantic…`
(`cb2sitting…log:378`, 0:32:15 ≈ 16:02:31): run 1's own storybit, whose popup
was opened and answered ~95 s after a reload whose read said
`g_StoryBitActive=0`. The bit reached its popup phase rather than vanishing;
what that active=0-but-answerable state IS was never read and stays an open
mechanism question on the keystone's margin — it does not touch run 2's PASS.

The rider as it stood, verbatim:

> ### Rider — popup-audit keystone: storybits survive save/load · **mode:
> co-run ride-along** (routing 2026-08-04)
> **Bug:** the ~5-minute console check that a popup-carrying storybit thread
> survives a save taken under its corner notification, and that answering it
> afterwards still applies the outcome. Settles the popup audit's keystone.
> → `docs/agent/reports/POPUP_CONSEQUENCE_AUDIT.md` §8 (procedure).
> **Requirements:** any save / console open.

## Rider — F85: quicksave under a choice popup — ⛔⛔ **RAN 2026-08-10 (`corun-batch-2` leg P): DEFECT CONFIRMED, ROUTE REFUTED — third cell, owner decision** · moved here by the batch-2 terminal audit

**Result:** the rider as written cannot run — **there is no save action in the
retail key-bindings screen at all** (owner read it twice), so "rebind Quick
Save to F9" is not a route on this build. A timer-driven save then **landed
39 s inside the open `ShowBreakthroughChoicePopup` modal** and reloading it
**voided the choice** (popup gone, available techs still 50). Defect real,
named route dead — the entry's two-way fork cannot express it. **Severity and
disposition are the owner's: "Decisions waiting on you" item 5.** Full
readings: `agent/bugs/F85.md`. The §3.6 distress-call corner is now the
interesting half and stays live on the checklist.

The rider as it stood, verbatim:

> ### Rider — F85: quicksave under a choice popup · **mode: co-run moment**
> (routing 2026-08-04 — the rebind + keypress are hands)
> **Bug:** rebind Quick Save to F9, open any choice popup (a launch-issue
> prompt is cheapest), press it — does a save land, and does loading it void
> the choice? → F85
> **Requirements:** any save / a cheap choice popup.

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

## ~~PT-60 — The chain-8b batch leg~~ ✅ **RUN 2026-08-12 WITH THE OWNER (`corun-pt60`) — P1–P6 + P8 MET, P7 met at its own strength, P9 a held negative control; AUDIT SUSTAINED 2026-08-12**

> **Result, in one place.** Fixture: a staged byte copy of the owner's own
> campaign save `USA Sol 302` (written 2026-08-01, the latest save predating the
> 2026-08-02 batch — the only save that could give P8). Log
> `cp60sitting_Mars.exe-20260812-13.38.15.log` (1,082 lines, MD5-verified,
> byte-compared full-length at audit). Every verdict below re-derived by the
> terminal audit from the archived file, not inherited.
> **P1** 81/81 registered/active, all 8 opt-ins read `active` · **P2** 5/5 new
> modules `active`, empty detail (the `:163` `SaintBlessing: inactive` line is a
> first-pass boot artifact that resolved — a grep for `inactive` files a FALSE
> miss) · **P3** 7/7 conversion modules `active` (8 conversions;
> `SequenceLatents` holds F29 items 1+3) · **P4** 7/7 new probes PASS · **P5**
> no regression: `77 PASS, 0 FAIL, 10 SKIP, 0 ERROR`, identical to the 08-11
> retail baseline (`u2run3`), all 10 SKIPs matched BY NAME, the
> `AsteroidLanderAvailable` message byte-identical · **P6** 0 `[LUA ERROR]` in
> the whole archived file (3 `LUA-ERROR` strings are the harness's own
> ERRORWATCH sentence) · **P7** owner verbatim in the log (`:1033`, general
> whole-session normalcy — NOT elicited per system; per-system support is the
> probes') · ⭐⭐ **P8 THE DECIDER: `SaintBlessing: re-based 10 dome blessing(s)`
> fired ONCE (`:329`, load 1), ZERO on the reload; effect 10-of-10 held through
> the round trip; F91 a controlled zero (0 shells / 7 tracks both loads); the
> F95 half non-discriminating (rocketscientist commander, heal returns early).
> The two boot look-alikes fired once each at `:174`/`:178`, before any load —
> the trap held. ⚠️ A third look-alike the audit added: the module-registration
> line `AstrogeologistExtractors: applied` (`:146`) also matches a naive grep**
> · **P9** 0 carriers / population 19 — negative control held (prep Src-proved
> the field unwritable on shipped data; never "the removal half ran").
> **Unplanned:** F48 repaired 3 of 7 tracks on the owner's campaign and the
> repair PERSISTED (R4) · F34(d)'s route re-derived on the owner's two
> challenges — RC Commander is the ONE live route (audit closed the last three
> Embark sites too), and the staged rider closed the "unobserved in play" gap
> 20/20 · EF-053 (mix-in walks; `RocketBase` silent-zero trap) · cheats-ruling
> → WORKFLOW rule · trains agenda → `agent/reports/TRAIN_SHIP_READY_ROUTE.md`.
> **Owner time: promised 40–60 min, actual ~95** — ~45 min was the owner's own
> challenges/staging (all three challenges changed the record), ~10 min ours (a
> brief defect: main-menu console executes but does not echo). Full record:
> entries F03/F04/F29/F33/F34/F41/F48/F54/F57/F90–F96, `archive/SESSION_LOG.md`
> 2026-08-12, checklist items 12/13.

### PT-60 — the checklist tracker section as it stood at close (moved whole from `PLAYTEST_CHECKLIST.md` by the audit, 2026-08-12, per the house rule)

> ### PT-60 — The chain-8b batch leg (F90-F96 + eight conversions) · Status: unrun · ⭐ attended · **mode: co-run** (routing 2026-08-04 — suite/reload/log halves rig-side; you keep the 15–20 min ordinary-play segment) · ⭐⭐ **QUEUED 2026-08-12 — the `corun-pt60` chain is AUTHORED** (`agent/prompts/corun-pt60/`, your order): a staged COPY of your `USA Sol 302` (now a protected file — the original is never touched), the 2026-08-02 prediction set annotated for today's build, riders (F21/F34(d)/F90/C42) taken only if their situation arises during your play. Your part: **~40–60 min** including the 15–20 min of ordinary play. Kickoff: a session on `01_OPUS_PREP.md` (unattended); the sitting runs when you sit. ⚠️ Steam Cloud is ON by your 08-12 note — staged-save deletions record "deleted, listing verified" until you announce the untick · ⭐⭐ **PREP RAN 2026-08-12 — the sitting is ready to go and nothing more is owed by you before it.** Your copy is staged and MD5-verified against the original; the harness, the arm script and the annotated predictions are parked. Two things prep found that change what the leg can promise, stated here rather than buried: **(a)** one of the nine predictions (**P9**, the cleared rocket-fuel key) turns out to be **unfalsifiable on any normal save** — the field it looks for could never have been written, so that read becomes a free negative control instead of evidence; **(b)** two of the three "heal" lines the leg greps for have look-alikes that print on **every launch** before any save loads, so the brief now names both wordings — an earlier reading would have scored the leg a pass on the wrong lines. Nothing here needs a decision from you
> **Bug:** seven approved fixes and eight technique-only conversions have never
> executed in a game; a byte-equivalence argument is not an observation. Nothing
> from that batch may be called verified until this leg's numbers are quoted.
> → entries F90–F96; the conversions and the dated prediction set: this snapshot.
> **Requirements:** a save PREDATING 2026-08-02 (that is what makes the heal and
> idempotence predictions readable) / pack on / **~40-60 attended minutes**, of
> which 15-20 is your ordinary play — the rest is console driving, which is your
> time too and is counted here. *(This line read "~30-40 minutes" until 2026-08-12;
> it predated the co-run routing and did not count the console driving.)*
> ⭐ The pre-batch save is already staged for you: a byte copy of `USA Sol 302`.
> **Setup:**
> 1. Load the pre-batch save; note the heal log lines immediately.
> 2. Suite run + `ListFixes()` — the agent reads the counts and probe verdicts
>    against the prediction set written 2026-08-02 (preserved in the snapshot —
>    use it, do not re-derive it after the fact).
> 3. 15-20 minutes of ordinary play — zero pack-named errors, zero visible
>    behaviour change from the conversions.
> 4. Save and reload — no heal line repeats; the cleared rocket-fuel key stays
>    absent.
> 5. Log review per the protocol.
> **Good to have:** the F90 rider if a storm arrives on an elevator colony.
> ⚠️ F92/F95 change real morale/production numbers on load — do not read them as
> drift in any A/B taken across this leg.

## PT-60 (as written before the run) — The chain-8b batch leg · covers **F90-F96 AND prompt 8's eight unrun conversions** ⭐ ATTENDED, OWNED BY CHAIN PROMPT 8b

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

---

## PT-37 — Can the F48 track repair ship? · ✅ RAN 2026-08-05 (corun-batch-1 sitting, attended) — case A PASS, better than a no-op; case B UNSAMPLED, the DECIDER refused

> **Result (recorded by the sitting, audited against the archived log by the
> terminal prompt the same week).** Log:
> `docs/archive/cb1sitting_Mars.exe-20260805-14.28.49.log`; save `CB1STAGE`, a
> `Copy-Item` of `TEST2H TRAIN`; full readings on `agent/bugs/F48.md`
> (2026-08-05 block).
>
> **Case A (healthy 280-element track): PASS, and it is a repair, not merely a
> no-op.** `ProcessTrackElements(ResolveMap(t), t.elements)` — first execution
> ever, `pcall` ok — left `start_el`/`end_el`/element count/`node_idx` sequence
> untouched and moved `connections_total` **559 → 558**, exactly the clean-chain
> value (2 × 279); the 558 **survived save + reload**. Labelled an inference
> from a count on the entry (no per-connection dump). Owner Tier-A verbatim:
> *"I seen a train pass through every station atleast once."*
>
> **Case B (meteor-damaged track): THE DECIDER IS UNSAMPLED.** A forced meteor
> broke 8 elements (8 repair sites), and the pre-mutation gate read every
> element's own hex: `shadowed=0 missing=0` — the hex grid hands the walk the
> **hidden original element**, so `OrderTrackElements` SUCCEEDS on a damaged
> track and the assert F48 is blocked on is unreachable via meteor damage. The
> harness **refused to run the call** rather than produce a clean pass that
> proved nothing. This contradicts F48's blocking premise for its cited
> scenario (F45's situation does not make a track unwalkable) — it does NOT
> prove the repair safe in general.
>
> **Disposition:** F48 stays `blocked` pending the owner's ship/hold call —
> `PLAYTEST_CHECKLIST.md` "Decisions waiting on you", item 1 (2026-08-05).

The test as written, moved here whole per the documented rule:

### PT-37 — Can the F48 track repair ship? · Status: unrun · **mode: co-run** (routing 2026-08-04 — your eyes: route formation + the salvage cursor; break staged, reloads rig-driven)
**Bug:** the game ships a savegame fixup meant to repair track connections on
old saves, but a misplaced parenthesis makes it do nothing. The corrected call
rebuilds every track element's connections, and its only failure handling is
an assert that does not stop execution — so before it can ship it must be seen
behaving on a real save, especially on a meteor-damaged track. This test
DECIDES F48: clean → the repair ships in the sanitizer; dirty fail → closes
`wontfix`. → `agent/bugs/F48.md`
**Requirements:** Any train colony (SAVE-A extended works) / ≥2 connected
stations + a running train / one meteor-broken track / console open.
**Setup:**
1. Load a save with two or more stations connected by track and at least one
   route with a running train (extending SAVE-A works).
2. Get one track meteor-damaged: `CheatTriggerMarsquake()` near a track, or
   play until one lands.
3. Console open. The agent hands the case-A (healthy track) commands, then the
   case-B (damaged track) repeat — full procedure is on the entry.
4. Save + reload after each case; the agent reads endpoints, route formation
   and the log against its predictions.
**Good to have:** after case B, a quick check that the repair site is still
salvageable (F45 territory — the agent will prompt it).


### Moved 2026-08-10 — the archive-decision-bullets rule ADOPTED and first applied

**The rule (owner, 2026-08-10):** fully-closed decision bullets move here whole,
exactly like completed test sections — but ONLY when nothing is owed to the
owner; anything on-hold or holding an owed input stays live. The seven records
below were the first application. Two closed the same day they moved:
**F46** (owner decision: group C → group B — a route exists and is skipped on
§3a cost-benefit; recorded on gent/bugs/F46.md and
SAVE_SAFETY_REDESIGN.md §5.4, counts now 5/5/9/3, nothing scheduled) and
**the C36-adjacent mysteries grep** (owner said go; it RAN 2026-08-10 and came
back CLEAN — 9 references to `IsDisasterPredicted` in all of Src, the only
Mysteries hit is Dream.lua:26, C36's own site; no `Scenario\` tree exists;
every other hit already on F81's victim list; nothing new filed — full record
on the C36 row, gent/bugs/C12-C38.md).

- ~~**CO-RUN #1 IS PREPPED AND WAITING ON YOUR ~7 MINUTES**~~ ✅ **RAN
  2026-08-04. It cost you about 6 minutes against the 15–20 asked for**, across
  two launches (398 s and 85 s, zero `[LUA ERROR]` in either). Three of the four
  payload items settled, one narrowed. **Your `TEST2H TRAIN` is untouched**
  (same bytes, same timestamp); the copy and both probes are deleted.
  → `agent/reports/CORUN1_EVIDENCE_CARDS.md` for the four cards.
  - ⭐ **F11's cross-map question is ANSWERED** — the one the entry said could
    not be proven from Lua. It is **route (a)**; the removal was watched
    happening, not inferred afterwards. → `agent/bugs/F11.md`.
  - ⭐ **F99's last unknown is MEASURED** — the hex returns the hidden element,
    which is what the seven crashes implied. Still `cand`, nothing built.
  - ⭐ **C41 got its first real mechanism, and you were right to make me close
    it.** Your mouse genuinely reports coordinates outside the game's own window
    box (up to `x=7665` against a box ending at `3840`) — because `GetMousePos`
    spans both monitors while the game's box is just the G7. Feeding that to the
    picker fires the clamps. I first recorded the bottom-right-corner case as
    **refuted**, on a reason that was simply wrong; it was **unsampled**. Your
    third run sampled it and the box came back at
    **`(2224,1731)-(3840,2160)` — the exact four numbers predicted before the
    picker opened.** ⛔ **The picker still appeared 52 times out of 52**, so the
    "icon does not appear" symptom did *not* reproduce: this is a mechanism,
    not a confirmation, and `C41` stays `cand`.
- ~~**DECISION: may the load-heal sweep use a COPY of your CAMPAIGN save?**~~
  ✅ **WITHDRAWN the same day, 2026-08-04 — nothing needed from you.** I asked
  whether `TEST2H TRAIN` carries the conditions the pack's load-time heal passes
  repair; you said you did not know. That was the right answer, and the fix was
  to stop needing to know. **The record already knew:** three archived co-run #1
  loads of a copy of that save (81/81 active) fired **zero** heal lines between
  them — so the sweep would have measured a save with nothing to heal. **And two
  of the six heal families turn out to be forceable on any save at all** (the
  meteor latch and the C34 rains structure are both shipped persistent
  variables), so the sweep now creates the defect state deliberately and watches
  the heal fire once and only once. It samples something real whatever the save
  contains, on `TEST2H TRAIN`, with no copy of your campaign involved.
  → `agent/prompts/unattended-1/02_OPUS_RUN.md` §2.
- ~~⭐⭐ **DECISION FOR YOU: adopt the co-run sign-off tiers?**~~ ✅ **ADOPTED
  2026-08-04 — you wrote `----Approved` on this item in your own hand;
  integrated by the unattended-1 terminal audit the same day.** The tiers are
  now **standing policy** in `agent/WORKFLOW.md` (sign-off tiers block): Tier A
  witness / Tier B evidence card (incl. the HANDS-ONLY sub-class) / Tier C
  delegated, with the visible-demotion rule. ⛔ In the item's own words,
  adoption does **not** touch: *"`tested` still means a pass at the keyboard
  per WORKFLOW, and no already-granted status is reclassified."* The adopted
  proposal, kept for the record of what was decided:
  (routed 2026-08-04 by the corun-rig chain's terminal prompt.) The problem it
  solves is the one you named: for log-only defects you never see the bug or
  the fix, so per-item sign-off is ceremony. The proposal, finalized against
  co-run #1's four REAL evidence cards rather than the draft's guesses:
  - **Tier A — WITNESS.** Your eyes genuinely add information the log cannot
    carry; you attend the measure moment. Unchanged from today.
  - **Tier B — EVIDENCE CARD.** Log-demonstrable; you quick-read a one-screen
    card — scenario, what was forced vs organic, the raw before/after log
    lines, run conditions, and the one-sentence falsifier — and OK it. Under a
    minute each. ⭐ **New sub-class the run exposed: HANDS-ONLY** — a leg that
    needs your *hands* (park the cursor on the other monitor, click launch)
    but none of your *eyes*. You do the named act, then read the card like any
    Tier B. The draft rule ("would eyes add information?") could not classify
    this at all, and it was the cheapest ask in the whole payload.
  - **Tier C — DELEGATED.** Mechanically self-verifying (the probe-suite
    class): ships on the suite verdict; you get a one-line digest per batch
    and keep the veto; you are not asked per item.
  **What the real cards showed:** Card 1 (the F11 train watch, classed A) —
  your eyes added nothing; the 340-removal counter over 7 trains was strictly
  stronger than watching one, so that rider class should be **A → B**, and the
  general rule is: when a designed-A item's card turns out stronger than the
  eyes, the demotion is stated on the card and applies to the NEXT instance —
  never silently. Cards 2 and 4 (the two ride-along reads) needed no eyes and
  the cards alone settle them — the clean Tier B/C cases.
  **What changes if you adopt:** log-only items stop needing per-item attended
  sign-off; you read cards (B) or batch digests (C) instead; Tier A is
  untouched. **What does NOT change without your word:** `tested` still means
  a pass at the keyboard per WORKFLOW, and no already-granted status is
  reclassified. **Recommendation: adopt, with the hands axis and the
  visible-demotion rule.** → `agent/reports/CORUN1_EVIDENCE_CARDS.md` (the
  four cards — transient sign-off artifacts per your anti-sprawl rule; their
  durable content already lives in the entries and archived logs).
  *(Your `----Approved` marker stood here; consumed into the ✅ heading above
  once the policy landed in WORKFLOW.)*


- **F46 `Fix_TrainCargoDumping`: move group C → group B.** The record says "no
  route" and a route demonstrably exists (F90's approved shape); the honest
  ground for skipping is cost-benefit, not impossibility. Moving it does *not*
  commit you to ever doing the conversion. → `CHAIN_QA_REPORT.md` §7.


- **The C36-adjacent mysteries grep.** A cheap sweep of `Lua\Mysteries\` and
  `Scenario\` for `IsDisasterPredicted` gates, deliberately left unassigned:
  your call whether it becomes work at all. Not owed. → `CHAIN_QA_REPORT.md` §8.
- ⭐ **DECISION FOR YOU: archive resolved decision bullets the way completed
  test sections are archived?** (routed 2026-08-04 by the unattended-1
  terminal audit, per your stale-records ask.) The checklist's documented rule
  — a completed section moves WHOLE to `PLAYTEST_ARCHIVE.md`, deleted here, no
  stub — covers *test sections*; the growing layer of struck-through ✅
  DONE/DECIDED **decision bullets** has no rule. **Two clear cases were moved
  as a worked example** (co-run #0, and the `LawOfficeDoor`/C44 call — both
  fully closed, durable content already in `SESSION_LOG`/entries; see the
  archive's "Resolved decision records" banner). **My recommendation:** adopt
  the same treatment for the rest — move only bullets that are fully closed
  with nothing owed to you; anything holding an open ask, an on-hold, or an
  owed input (the relabel wording) stays here no matter how struck-through it
  looks. Applying it today would move ~4 more bullets (~60 lines), including
  the 41-line probe-gate record; cost is one commit. Say go/no-go.
- ~~**The probe-gate blocker**~~ ✅ **DECIDED 2026-08-04 — you asked for the
  safest option and that is what was adopted: the tool was NOT loosened.**

  No escape hatch was added to `doccheck.py`. The sweep stays absolute — any
  `TEMPORARY` marker in `Code/` is red, full stop — because a hatch a hurried
  session can open without saying so is how 2026-07-31 happened.

  **What changed instead is when a probe is allowed to exist at all.** New
  binding rule (`WORKFLOW.md` probe hygiene, rule 5): **a probe file is present
  in `Code/` only while its run is actually happening.** Placing it and running
  are the same act; deleting it and recording the answer are the same commit.
  There is no state in between, so **no armed probe can outlive the sitting that
  needed it** — which is the failure you told me to design against.

  **It costs nothing.** Prep still commits early: the staged save, the
  measure-moments list, the doc edits, and the probe's *source* as a code block
  in the brief. A probe parked in a doc physically cannot run — the mod only
  loads files listed in `metadata.lua`, all under `Code/` — so it is inert by
  construction, not merely unused. If a sitting slips, nothing is stranded and
  nothing is armed.

  ⚖️ **One-time override granted 2026-08-04, recorded here so it is not
  invisible.** You gave prompt 3 an override of this rule **for its prep only**.
  It may commit armed probes in **one named commit**, using the `--no-verify`
  bypass with a body stating exactly what is red and why — and ⛔ **if the
  sitting does not happen in the same working session it must delete the probes
  before it stops.** That deadline is the condition the grant rests on: an armed
  probe never survives a session boundary, which is the situation you said you
  did not want back. Not precedent, not carried to any later co-run, and prompt
  4 audits every condition against git.

  ⚖️ **You asked for it to be rechecked — DONE 2026-08-04 (prompt 4): your
  decision holds and the rule stands as written.** The diagnosis re-verified
  from the tool and the hook themselves. The one claim that had been asserted
  without source was verified: the game loads **only** the files listed in
  `metadata.lua` `code` (`Mod.lua:490-521` — both load loops iterate that list,
  nothing scans directories), so a parked probe genuinely cannot run. The
  feared cost was measured away — the parse sweep works on the parked file, so
  prep loses nothing — and declining your override measured what any escape
  hatch would have bought: **0.4 seconds of machine time and none of yours.**
  No recommendation to change anything; the safest option was also free.
- ~~**One cheap hardening from the same investigation, your call:** nothing
  checks the TestKit repo's working tree — a doccheck line that *reports* (not
  blocks on) a dirty tree would close the gap.~~ ✅ **GO given and BUILT
  2026-08-04.** Every doccheck run now prints a `TESTKIT TREE:` line — `clean`,
  or each uncommitted file as a `WARN`. Report-only per your word: it never
  blocks a commit, so TestKit work-in-progress cannot jam the pack. Verified
  on both paths (clean, and a planted temp file).


### Moved 2026-08-10 — decision drive round 2 (F11 pair + the veto lever)

**Verdicts (owner, 2026-08-10):** the F11 pre-wrapper rider **CLOSES on 2-of-3
readings** (the wrapper's own behaviour is witnessed; the third reading tests
vanilla's lines and is untakeable on this save — if it ever becomes takeable it
is one free ride-along, recorded on the entry). **F11's priority drops P1 → P2**
(correct repair of a real `table.remove` misuse, but the guarded state has no
demonstrated producer and no wedge was ever seen live). **The
`SMRFixPack_Disabled` veto limit is RECORDED, not coded** — the lever covers
only D12/F97-class modules; test briefs toggling D03/D07 use `IsActive`
(notes on D03, D07, and WORKFLOW Co-runs). Records as they stood:

- ⭐ **DECISION FOR YOU: does the F11 pre-wrapper rider close on two of its
  three readings?** (2026-08-04) You wrote the rider, so this is yours. Two
  readings passed cleanly — `TrainPlatformWedge [active]`, and 7 trains
  completing full unload cycles with 340 passenger removals and **zero** wedges,
  with you watching one. **The third cannot be taken on that save**:
  `LuxuriousTrains` is researched so the travel-time comfort call is skipped by
  design, and no train runs a forest track, so both stat counters read `0` —
  and `0` is what a working fix and a broken one both produce there.
  **My recommendation, not a decision:** the two expressions in question are
  *vanilla's own lines*, so checking they still fire checks vanilla rather than
  our wrapper — and the wrapper's own behaviour is now witnessed. Closing on two
  of three looks right to me. **If you'd rather have the third**, it needs a
  save without `LuxuriousTrains` or a train on a forest track, and it is one
  ride-along in any future co-run. → `agent/bugs/F11.md`.

- **Does F11 keep `P1`?** The F11 rider ran 2026-08-03 and the state its fix
  guards against has **no demonstrated producer** — crew-gathering abduction
  keeps `train.units` synced on both maps. The fix is still a correct repair of
  a real `table.remove` misuse in shipped code, so it is not a removal
  question; it is a priority question, and it is not an agent's call.
  → `docs/agent/bugs/F11.md`.
  *(Update 2026-08-03, chain close: the fix's SHAPE changed — the ~30-line full
  copy became a 10-line pre-wrapper, so it no longer freezes the two balance
  expressions a game patch would most plausibly touch. The P1 question is
  unchanged; the conversion is behaviour-preserving by construction but NOT yet
  verified at the keyboard — see the rider below.)*

- **The dead `SMRFixPack_Disabled` veto on D03/D07.** The console veto lever
  does nothing for those two modules — only `IsActive` is consulted. Either
  honor it per-call in both, or record that the lever exists only for
  D12/F97-class modules. Nothing measures wrong today, but a future leg that
  used the lever on D03/D07 would silently run live and you'd read the result
  as a fix failure. → `CHAIN_QA_REPORT.md` §5.

### Rider — F11: verify the pre-wrapper conversion · Status: ⚖️ **TWO OF THREE READINGS PASSED 2026-08-04 (co-run #1, you attended)** — the third is unavailable on that save; **your call whether it closes** (decision above). Remainder is **TAKEABLE WHEN** a sitting runs on a save WITHOUT `LuxuriousTrains`, or with a train on a `seen_forest` track
**What ran.** `TrainPlatformWedge` read `active`; 7 trains completed full
`GotoStation → UnloadTrain → LoadTrain → GotoStation` cycles over 238 s, **340**
passenger removals from train holders, **0** wedge candidates, and you watched
one unload and leave. ⛔ **The stat reading could not be taken** — both shipped
branches are switched off on that save by design, so `0` and `0` mean nothing.
⛔ **`tested` is NOT claimed.** Card 1 in `agent/reports/CORUN1_EVIDENCE_CARDS.md`.


**Change, not a bug:** 2026-08-03 the F11 fix was converted from a ~30-line full
method copy to a 10-line pre-wrapper (same repaired branch, original method
called for everything else). It is behaviour-preserving **by construction** and
has NOT been verified live — this rider is what earns that back.
→ [F11](agent/bugs/F11.md)
**Requirements:** pack ON, any train line that actually moves colonists. No
cheats, no save juggling — an organic warm-up leg is enough.
**Setup:** none beyond playing. Watch three things during normal train use:
`SMRFixPack.ListFixes()` shows `TrainPlatformWedge [active]`; trains unload and
LEAVE stations normally; passenger comfort/sanity still move on disembark (the
travel-time penalty and the forest bonus now run vanilla's own lines instead of
our copy).
**The check can fail:** a train wedged at a platform, or disembark stat changes
that stopped happening, falsifies the conversion — say so and the copy form
comes back from git (`3a6512f^`).

### Moved 2026-08-10 — decision drive round 3 (our own noise, the F100 hold, PT-20)

**Verdicts (owner, 2026-08-10):** **C43 → option 2** — `set_global` will be
restricted to names that already exist, with probes SKIPping (stated reason)
when their stub target is undeclared; queued into the next unattended chain,
which verifies it against a live suite run. **F100's hold is LIFTED and the
repair is the reason-string fix ONLY** — the boot log stops crying wolf; the
preflight target itself waits for D12's own review; same chain, verified by a
live boot. **PT-20: REDO NOW** — a dedicated redo co-run is queued (disable
click + FULL RESTART + ~10 min play are the owner's; the rest rig-side); its
result supersedes the possibly-mixed-state 98-vs-98. Records as they stood:

- **F100 — how do we repair the `NoHomeless` self-check?** It names `Community`
  for a method `Workforce` declares, so the module reports itself `inactive` in
  every boot log and then applies anyway. Three options on the entry: point the
  `Require` at `Workforce` (checks a different surface than the module calls);
  teach `00_Core`'s `Require` to accept an inherited method (correct, but
  changes self-check semantics for **all 81 modules** and needs a suite run
  either side); or fix only the misleading reason string. ⚠️ It sits on D12,
  which is under review. → `docs/agent/bugs/F100.md`.
  ⏸️ **ON HOLD (your `---on hold`, in your own hand, 2026-08-04).** Not a
  decision — the item stays OPEN and stays counted; nobody builds any of the
  three options until you lift the hold and pick one.

- **C43 — how do we stop the TestKit printing `[LUA ERROR]` into your logs?**
  Two Wave-5 probes install stubs through `set_global`, which trips the engine's
  strict-global guard on `IsNearDome` and `AddAreaRubble`; both probes then PASS,
  so the cost is entirely two alarming lines in the log next to real errors.
  ⚠️ **Second instance in one day** of the pack logging its own authoring noise
  (F100 is the first). Three options on the entry. → `docs/agent/bugs/C43.md`.

### Moved 2026-08-11 — decision drive round 4 (F99 severity + the save-folder policy)

**Verdicts (owner, 2026-08-11):** **F99 → PASSIVE WATCH** — stays `cand`,
zero work: every future log is grepped for `TrackElement.lua:805` (already
routine); one ORGANIC throw reopens it as real work; cheat-driven throws stay
out of scope, consistent with the F101 dev-tools ruling. Four organic
completions and three forced cells, all zero, bound the rate. **Save folder →
KEEP DELETING + VERIFY** — the close-out directory listing is the standing
gate (it held on the audit re-check); the Steam-Cloud hypothesis stays parked
until a deleted save ever returns. **F85's disposition stayed OPEN by owner
challenge** (the "no retail quicksave" claim is an inference chain — the
10-second Ctrl-F9 empirical check now rides the PT-20 redo sitting; live
record on the checklist item and the entry). The F99 record as it stood:

- **F99 severity, and whether it becomes work at all.** New 2026-08-03 from
  your own log: 14 `TrackElement.lua:805` errors, every one under
  `CheatCompleteAllConstructions()` during your underground build-out.
  Reachable **without** the cheat is unproven and deliberately not claimed. The
  cheap discriminator is one no-cheat track completion on a disturbed element
  list — say the word and it becomes a rider; otherwise it stays `cand`.
  → `docs/agent/bugs/F99.md`.
  *(2026-08-04: the discriminator is **leg C of the `unattended-1` chain** —
  kicking that chain off is the word. Its RESULT lands back on this line as
  input; the severity decision stays yours either way.)*
  ⭐ **THE DISCRIMINATOR RAN, 2026-08-04. Result: ZERO occurrences in 4 organic
  completions — and that is a rate bound, not an all-clear.** Four track
  elements broken with `BreakTracks` (the meteor's own funnel, lottery removed),
  each break **witnessed** as real damage (`broken=true sites=1 repair_cgs=1`),
  each repair finished **by drones with no cheat on the stack**, `0 [LUA ERROR]`
  in the whole log. Fixture: 244 drones (81 idle), 15 hubs, two tracks (4 and 23
  elements). Log: `docs/archive/u1c4_Mars.exe-20260804-17.12.54.log`.
  **What it means for your call:** no-cheat reachability is still **UNPROVEN**,
  so F99 stays `cand` and nothing gets built — but the failure is now bounded:
  it did not appear in four clean organic repairs, against seven appearances in
  ~1 h of your own cheat-driven build-out. **The decision in front of you is
  unchanged in shape** — severity, and whether this becomes work at all — with
  one more piece of evidence under it. ⚠️ Four is a small N and the leg can be
  re-run cheaply on a bigger one if you want a tighter bound; say so and it is
  ~1 min of machine time per four more.
- ⚠️ **CORRECTION to the line above, and it cuts both ways.** The second-opinion
  chain re-read the log: **the count is 7, not 14** — the 14 matching lines are
  7 `[LUA ERROR]` headers each paired with a C-side `Error calling Lua function
  "exec" from C` report of the same throw. The old figure is left standing above
  rather than edited, per the drift-evidence rule. Two things the re-read also
  found, pulling severity in opposite directions: the auto-connect work
  **self-heals** (the queue entry is set one line *before* the throw and the
  engine's own 500 ms repeater redoes it correctly), which makes it milder than
  filed; but each throw escaped the console `exec`, so the rest of that cheat
  pass never ran and `ResumeTerrainInvalidations` was skipped **seven times**.
  Also new: the `if not self.broken` guard on the failing block **can never be
  false** — the line above it already cleared the field. → `docs/agent/bugs/F99.md`
  ("Mechanism settled by reading"; the chain folder is deleted — its sealed
  derivation survives in git at `28c253f`).
  *(Chain close 2026-08-03: the terminal prompt settled the mechanism from
  source — the element list was empty BEFORE the rebuild call; the filed
  "rebuild comes back empty" route is refuted, and the drain is the engine's
  own track-merge absorb-walk. This does not change the decision in front of
  you: no-cheat reachability is still unproven, nothing is built, and the
  cheap discriminator offer stands.)*

### Moved 2026-08-11 — decision drive round 5 (F48, D07, the doc-review remainder)

**Verdicts (owner, 2026-08-11):** **F48 → SHIP** (evidence beat the criterion;
build queued into the next unattended chain, covered by PT-35's do-no-harm
run — entry + `SAVE` records on `agent/bugs/F48.md`). **D07 → NO DOME
PIN**, the owner's 2026-08-10 typed line confirmed as the ruling (recorded on
`agent/bugs/D07.md`; closed items 2 and 8 together). **DOC_STRUCTURE_REVIEW:
R4 + R7 ADOPTED as binding WORKFLOW rules** (state-transition claims carry a
save/reload round-trip step; verdicts evidence their EFFECT, not just their
execution), **R9 + R14 DROPPED** (standing maintenance overhead with no
incident behind them). The bullet as it stood:

- **The `DOC_STRUCTURE_REVIEW` recommendations this chain does not adopt** — R4
  (a round-trip step for state-transition claims), R7 (effect-evidencing
  verdicts), R9 (an agent/facts/ review cadence), R14 (a context budget for
  agent docs). Adopt, defer, or drop.
  → `docs/agent/reports/DOC_STRUCTURE_REVIEW.md` §3 and §6.

---

# Moved whole from PLAYTEST_CHECKLIST.md on 2026-08-11 by the `corun-pt15` terminal audit

Two blocks, verbatim as they last stood on the checklist. (1) The completed
PT-15 section with the C46 discovery note and the pre-sitting setup/march text
that the sitting consumed; results audit-sustained 2026-08-11 — the C39-repair
and C46 decisions stay live on the checklist. (2) The closed 2026-08-11
"BOTH TICKS DONE" block, confirmed by the audit (two post-untick launches
restored nothing; EF-051 closed, "never say gone" retired).

## (1) PT-15 — Wisp power output (completed 2026-08-11)

### PT-15 — Wisp power output (F07, + F15 bonus) · Status: ✅✅ **PASSED 2026-08-11 — F07 is now `tested`, F15 confirmed too**
**Bug:** freeing the wisps rewarded ~1/1000 of the promised power — a trickle
instead of kilowatts. Fixed: ~1000 × wisp count, a real power source.
→ [F07](agent/bugs/F07.md), [F15](agent/bugs/F15.md)

⭐⭐ **RESULT — you played the whole mystery and the fix works.** Your Light Trap
held **95 wisps and produced 95 power** on a 218.5 grid — **43% of your colony's
entire supply, about 47 Solar Panels' worth.** Vanilla's line would have given
**0.095**. It survived a save/reload unchanged. Your verdict, kept verbatim:
*"the screen shot is what I see, so it is working."*

**F15 also passed**, on the same trapful: destroying 15 wisps posted **zero**
research points at the instant of the kill (the vanilla double-grant is gone) and
the notification's **1,500** matched `wisps × 100` exactly.

⛔ **Two honest limits** — the fix is verified, but the *broken* behaviour was
never seen (the pack was on throughout), and the final enact had to be **forced**
by us because your organic click landed at 2 PM with an empty trap. That last
part was our scheduling error, not yours; see the entry.

🗄️ **Two saves were kept at your request** (they are not strays — do not delete):
* **`CP15PT15.savegame.sav`** — 95 wisps held, mode `free`. Rebuilding it
  organically costs another ~3-hour mystery playthrough.
* **`CP15F15.savegame.sav`** — the post-destroy state that evidences C46 below.

### ⚖️ NEW 2026-08-11 — a defect we found by accident, and it needs your call
**C46 — an emptied Light Trap keeps producing power forever.** Choosing
*"Experiment upon them"* kills every wisp but never clears the trap's power
modifier, and the same choice stops all wisp spawning, so nothing ever resets it.
Measured: **0 wisps, still 15 power, indefinitely** — and it scales with whatever
the trap held when you clicked (95 wisps would leave 95 power standing).
→ [C46](agent/bugs/C46.md)
**It's vanilla, and our own fix inherits the omission.** The sign favours the
player (free power), so it's a plausibility defect rather than a harm.
**Your call: is this worth fixing at all?** Nothing is built. ⚠️ One cheap gap if
you say yes — we saved the state but never reloaded it, so whether the phantom
power survives a save/load is still untested; that costs one load of
`CP15F15.savegame.sav`.
**Requirements:** SAVE-D — St. Elmo's Fire mystery with Light Traps holding
wisps (pick the mystery at new-game setup; the console route is on the entry —
disclose if used).
⭐ **QUEUED 2026-08-11 — you built the fixture yourself** (`PT-15.savegame.sav`,
mystery selected, tech un-cheated): the **`corun-pt15`** chain runs this as its
front on a staged COPY (`CP15STAGE.savegame.sav`, byte-identical, MD5-verified —
your save is protected and survives), with the C39 law observation and the F85
Ctrl-F9 check riding the same sitting.

⭐ **Where the save is, 2026-08-11 (your report):** *"The save just came out of
the founder stage I think."* That means the mystery's first timer is **running**,
so the opening beat is **10–20 sols away and no more** — the wait has a
guaranteed end (~12 real minutes at ultra). ⚠️ The game keeps no record of *when*
approval fired, so your report is the only source for it and the rig treats it as
your word, not a reading; it will say so out loud if the save disagrees.
⇒ **Useful consequence: roughly the first 10 sols are dead time.** The sitting
should spend them on the C39 law observation and the Ctrl-F9 check rather than
watching an empty map.

⚠️⚠️ **READ THIS BEFORE YOU SIT DOWN — the mystery is much longer than this
section used to say, and the correction came from reading the whole sequence
rather than its first beat** (prep 2026-08-11, `Mystery 11.generated.lua`).
That first beat is only the beginning. Between it and the wisp choice the
sequence sleeps **another ~30–60 sols** in four more scripted waits (the largest
is 15–30 sols on its own) and gates on things only you can do: **scan two
sinkhole anomalies**, **build a Large Water Tank and fill it to 80%**, **build a
Light Trap**, and then reach **30 wisp catches** (`fireflies_caught > 29` is the
literal gate on the choice).
⇒ **A single sitting is still unlikely to reach the wisp choice.** Derived, not
measured: 40–80 sols of scripted sleep alone is ~25–50 real minutes at ultra
(1 sol = 720,000 game-ms, measured; ultra = 20×), before any of the player-gated
stages.
⭐ **Two things that make it cheaper than that sounds.** (1) The 30 is **catch
events, not 30 different wisps** — wisps fly home at 4 AM and come back the next
night, so the same few keep counting; a correction to prep's own first estimate,
which was an order of magnitude too pessimistic. (2) Three of the five stages
above have standing accelerators: `CheatCompleteAllConstructions` and
`CheatFillAllStorages` cover the water tank and the Light Trap outright.
⇒ **The one thing that really controls the wisp rate is placement: build the
traps hard against the sinkholes** (they are only found within 400m of one) and
keep them powered.
**What the sitting therefore does:** reads exactly where the mystery stands
(`CP15.MysteryWhere()` — the founder stage is measurable to the game-second; the
10–20 sol sleep is **not** exposed to Lua and is reported as a bound, never as a
number), marches at ultra as far as it gets, and if the choice is not reached it
saves the progress under a chain name and hands PT-15 to a follow-up sitting.
C39 and the Ctrl-F9 check do not depend on any of this and complete regardless.
**Requirements for the sitting:** the staged copy is already made; ultra speed is
FORCED and disclosed; **you** play the colony and answer the mystery's choice
prompts — the rig only reads. Nothing is injected into wisps, traps or the
mystery sequence (the mystery is played, not forced).
**Setup:**
1. Choose "free the wisps" **at the game's own choice prompt** when it appears.
2. The agent reads the trap **immediately** (`CP15.TrapRead(...)`): output equal
   to the wisp count = broken, 1000× the wisp count = fixed.
   ⚠️ **Immediately matters.** The broken value is overwritten by the next wisp
   event — typically the 4 AM release — because every other code path already
   multiplies correctly. A late read shows a healthy number either way.
**Good to have:** on a separate trapful, destroy mode — the research points
granted must MATCH the notification's number (the F15 half). ⚠️ Two things prep
found: the reward arrives **3.3 game hours late** (each wisp's death sleeps
first), and once destroy mode is on **no further wisps spawn at all** — so it is
a one-shot rider, taken last.

⚖️ **Two calls that are yours to make DURING the sitting** (your order,
2026-08-11 — both built and parked, neither runs unless you say so; the agent
will put each to you once, at the moment it would help):

1. **Measure how fast this save can safely run.** "Ultra" is 20× by UI
   convention only — the engine allows far more, and the march is mostly
   waiting. Costs ~2 minutes, and it is nearly free because it runs during the
   countdown's dead window, so the measuring *is* the marching. ⚠️ It has to be
   measured rather than guessed: past a certain speed the game skips the hourly
   check that spawns wisps, and it does so **silently** — no error, just a night
   where nothing appears. The rig finds the fastest setting where that never
   happens.
2. **Fill the sinkholes with wisps.** There is an unused developer function that
   tops a sinkhole up to 30. It would collapse the 30-catch gate to a night or
   two. The wisps still have to wake up, fly out and get caught normally, and it
   does not touch the power maths the test is actually about — but it does mean
   we can no longer say the wisps arrived the way a player's would, so a full
   `tested` verdict would have to name it. **Your call, not ours**; it is the one
   thing here that overrides a standing rule of the chain.


## (2) ✅ BOTH TICKS DONE — added 2026-08-11 by `unattended-2`, closed the same day, CONFIRMED by the corun-pt15 audit

Not decisions; things only your hands could do. Both are done; the block stays
until the next launch confirms the second one stuck. *(It did — audit,
2026-08-11.)*

**1. ~~The Community Fix Pack is DISABLED in your Mod Manager~~ ✅ DONE — you
re-enabled it at 01:57 and the re-run measured `81/81 active`.** Recorded
because it cost the night's first launch and because the cause is worth knowing:
`corun-batch-2`'s last leg turned the pack off on purpose to test the uninstall
on 2026-08-10 and nothing turned it back on, so **anything you played between
Sunday evening and last night ran without the pack.** ⚠️ For next time: after
any leg that disables the pack, re-enabling it is part of that leg's close-out —
the rig cannot do it (`AccountStorage`, `SaveAccountStorage` and
`ModsReloadItems` are all engine-blacklisted for mod code, and there is no
console at the main menu), so it has to be handed back to you explicitly.
**Everything it was blocking is now verified and closed.**

**2. ~~Steam Cloud is putting your deleted staged saves back~~ ✅ DONE — you
unticked it 2026-08-11 ("Steam settings done"), and the strays are cleared.**
The save-folder gate that "failed twice" was never a diligence problem: we
delete the files, and Steam restores them at the next launch — measured on two
independent launches, 14 saves restored with creation stamps inside the launch
window and week-old modification dates, all written **before the game process
even started**. Details: `agent/facts/EF-051`.
✅ **Cleanup executed right after your untick:** all **14 strays deleted**
(`CB1STAGE`, `CB2STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`, `CB2F85`, `CB2PKEY`,
`CB2PKEY2`, `CB2UNINSTALL`, `U1C0PROOF`, `U1C1HEAL`, `U1C2PT35`, `U1C6FORCED`,
`U1C6HEALED`), **732 MB reclaimed**, directory verified at **55 `.sav` files**
— the exact pre-restore baseline — with `PT35FIXTURE` and `TEST2H TRAIN` both
MD5-verified untouched.
⭐⭐ **AND THAT READING IS IN — it was your own launch this morning, and it
passed.** You unticked and we cleared at **09:43**; Steam's launch marker was
rewritten at **09:47**; you then played (two autosaves and `PT-15`). **Not one
of the 14 came back.** So the restore mechanism looks dead. The formal
retirement of our "never say gone" rule is the chain audit's call — it needs to
check our working, not take our word — but nothing is owed from you.
*(Audit 2026-08-11: working re-checked and confirmed; retired. A third data
point landed free — the strays were still absent after the sitting's own 15:09
launch.)*

✅ **The one loose thread is closed too — nothing is missing.** The count looked
two short (55 before; afterwards 53 old ones plus the 3 you made). You confirmed
you hadn't deleted anything, so we went looking, and an earlier session had
already written the answer down: the game had two rolling autosaves of its own,
**`Autosave Sol 351` and `Autosave Sol 356`**, noted at the time as files that
"rotate out on their own". Your new colony's autosaves — **Sol 11 and Sol 16**,
the same two slots, the same 5-sol spacing — replaced them.
It reconciles exactly: 55 − 2 rotated out + 2 new autosaves + `PT-15` = 56.
⇒ **No file left that folder except by the game's own housekeeping.** Nothing
for you to do; the audit re-checked the working and it holds.

---

## ck- -- archived 2026-09-14 (was checklist status:closed): ✅ v7 IS LIVE on both stores (your word). Nothing to decide; three things to tell me when convenient.


> **Read from here:** the Steam page (updated Sep 10 @ 3:59pm, 325.512 KB, "Forty-eight
> repairs", all three gallery images, the whole description down to its last link), and the
> Change Notes carry all three v7 lines. Steam's delivered file: 325,512 bytes, md5
> `c58eea7e3b51de227adf1759e7bbc61e`. The site's fix list shows 48 entries. `metadata.lua` has
> its comments back; version 7 kept exactly as the upload left it.
>
> ✅ **Your answer, same night:** "Everything seems to be correct, I had to use the copy and
> paste ones to get the formatting right" — both pages carry the pasted, formatted text, and
> Steam shows no version number. The upload itself accepted the 6,206-character description.
> Nothing more is asked here (the Paradox version display is never chased, item 71).
>
> ✅ **Posted** (your word, 2026-09-12): the two Steam replies for the C74 and C83 reporters
> went up with the v7 update. Recorded in `FIELD_REPORT_REPLIES.md` → "What was actually
> posted" → the Steam table, marked owner-stated (there is no API for a Steam comment).


---

## ck139 -- archived 2026-09-14 (was checklist status:closed): ✅✅ 139 BUILT + TESTED-ATTENDED: all seven silent units (C74 hammer + MOXIE, C77's five), Metatron left out. `Fix_SilentHitMomentFX.lua`; old saves heal without a power cycle; staged for the next…


> **Build receipt:** the first packed-module load caught a real flaw in the
> proposed old-save gate: persisted tracker handles could still look live while
> their resumed threads were about to exit. You were right to reject a
> power-cycle workaround. The corrected load pass replaces those cosmetic
> trackers exactly once, using the game's own tracker bodies. On the final run
> it restored four trackers on each of two loads; you listened to every intended
> effect and reported **"they are all functioning, no power cycling"**. The
> module applied, all 11 guarded marker presets registered, the fresh RC Dozer
> task fired four `Load`/`Hit1` calls, and both archived logs contain zero Lua
> errors. The drill Rare Metals skin and white CP3 MOXIE remain silent by design.

Original question, kept as asked: C74, the Rare Metals Extractor's hammer (and the MOXIE pump) play no strike sounds. You proved the fix live: the game's own code plays them once two small things are added. **Decision: build it for hotfix 3, or file and watch. Recommendation: build it — small, save-clean, and the game does the work, not a timer of ours.**

> **What you measured and proved (2026-09-10, thank you):** the sounds, the
> steam puffs and their wiring all work when fired by hand. Two game bugs stop
> them firing on their own: the game stores no "strike" markers for the hammer
> (or the MOXIE pump), and the code that looks for markers asks with the
> animation's *number* while they are stored by *name*, so it would never find
> them anyway. With both patched in the console, you heard the thunks and saw
> the puffs "perfectly in sync".
>
> **The drill skin is not broken.** NASA, SpaceY, BlueSun, Brazil, Roscosmos,
> Japan and ISRO colonies place the drill model by default. It spins and never
> strikes, and the developers gave it its own steady steam instead. The white
> (CP3) MOXIE is silent by design the same way.
>
> **What the fix is:** one small code correction (look markers up by name) plus
> strike markers for the hammer (times already proven), the classic MOXIE pump
> (✅ **proven with you 2026-09-10: "works and in sync"** at the first try) and,
> if wanted, the rare Metatron. Nothing goes into your saves; removing the mod removes it
> cleanly. Cosmetic only; production is untouched.
>
> **For the reporter**, if you want to reply: *Confirmed. It's a bug in the
> game's own hammer animation, not a mod. If your sponsor is NASA, SpaceY,
> BlueSun, Brazil, Roscosmos, Japan or ISRO, you get a drill model by default,
> which is meant to be silent; use "Change Skin" to get the hammer.* Details:
> `agent/bugs/C74.md`.
>
> **If we fix it, the patch note has to explain the two skins**, or drill-skin
> players will report the fix as broken. Your three screenshots are saved for
> that (`agent/reports/c74_skins/`: drill default → Change Skin button →
> hammer).
>
> ⭐ **Update 2026-09-10 (desk sweep): the same silence reaches five more units**
> ([C77](agent/bugs/C77.md)). Each has sounds and effects that are written and
> packed with the game but never play: **The Excavator's** 24 dust puffs, the
> **shuttle's** landing and take-off sounds at a Shuttle Hub, the **Water
> Extractor** pump, the **RC Terraformer** and the **RC Driller**. It is the same
> missing strike-marker data, but their code already asks for markers the right
> way, so each unit needs only its markers, not the code correction. ✅ **You
> confirmed the Water Extractor (2026-09-10):** its water-running loop plays, but
> the pump-stroke "peak" sound only plays when fired by hand, never on its own.
> ✅ **And you proved its fix on both skins the same day ("both are working now
> and match").** The Water Extractor needs one more piece than the others: it
> starts listening for markers a moment before its pump starts moving, so it
> never hears them. The fix restarts it once the pump is running. ✅ **The
> shuttle is measured too (2026-09-10):** with the other sounds muted, about 12
> landings and 8 take-offs, and the game never once played the touchdown or
> take-off sound; you heard both land and lift off silently. Then, with only
> the markers added, you **heard both, distinctly** (16 of 16 landings and
> take-offs). Markers alone fix the shuttle. ✅ **The RC Driller too:** drill
> hits with the markers, none with them removed (your A/B). It's a Roscosmos-only
> rover for normal players; your colony can build it because of a cheat. ✅ **And
> the RC Dozer** (the game's name for the RC Terraformer): with the markers, its
> shovel sound plays on every scoop while it loads rock (the blue-arrow phase);
> you heard it, and the log shows 5 of 5. ✅ **And The Excavator** (you built one
> for the test): no dust at its buckets before; with the markers, every bucket
> bites and throws dirt, "exactly as predicted", and the log shows all 24 effects.
> Nothing is left unproven.
>
> **Recommendation now (2026-09-10): build all seven proven units together for
> hotfix 3** — hammer, classic MOXIE, both Water Extractor skins, the Shuttle Hub
> shuttle, the RC Driller, the RC Dozer and The Excavator. Every one is heard or
> seen working by you; it's one module, cosmetic only, and nothing goes into saves. Still worth a
> glance when convenient, not required: whether the shuttle's touchdown/lift-off
> and the Dozer's shovel land exactly on the motion (first-guess timings). ~~So the decision grows: **build the hammer + MOXIE only,
> or all of them?** Each extra unit costs one "find the times by ear" step with
> you. Recommendation: keep 139 as the hammer + MOXIE, and decide C77 after one
> check in the MOXIE sitting below.~~ *(Earlier wording, superseded the same day by the recommendation above; you ruled: all seven.)*
>
> **In the same MOXIE sitting (about 1 extra minute):** one console line prints
> which of these units your colony has and how many strike markers each one
> sees. The agent hands it over; a zero on a unit that is visibly moving proves
> it. Report: `agent/reports/C74_SOUND_SWEEP.md`.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ✅ `100_DOCSWEEP` IS DONE: the words now match the pack that ships. The hotfix-2 chain is closed; the only thing left is your upload sitting.


> **Receipts for 126, 127 and 128 — carried out, not just ruled.**
> * **126 (F95 pass STAYS) ⇒ 128.** The change note's second bullet now says the
>   leftover Astrogeologist bonus *"is removed the next time that save loads"*
>   instead of *"cannot take back"*, and the site FAQ's save-repair list names
>   the pass. Moved together in `metadata.lua`, the paste backups in
>   `UPLOAD_WORKFLOW` §3, and the site (`7830134`; site `dc892d1`), proven
>   identical by script. ⚠️ Still a claim: the pass has never met a save that
>   carried the residue (your sitting read `removed 0 … left 0`). If a
>   `LEFT n … ALONE` line ever appears, that is the one to report — unchanged
>   from your 126 block.
> * **127(a) (F117 fixed first).** The fourth bullet gains *"an error popup that
>   could appear when new arrivals had no dome within walking distance and their
>   only route to one was a passenger train is gone"*. Written against `777249d`,
>   the repair on `main`, in the words of the re-derived recipe (the
>   passenger-station layout), not the withdrawn "ordinary mid-game" one.
>   ⛔ "Is gone" is a claim until the F117 control runs; the note's last bullet
>   says so in your words, as it does for everything else in it.
> * **The one sitting instruction that survives — 129:** upload → check or paste
>   both store pages (`UPLOAD_WORKFLOW` §3) → **then** publish the site (§4), in
>   the same sitting. The committed site now says the store pack is built
>   against game 1.1.0.403908 and points 1.0.7 players at the frozen build; the
>   live site keeps saying 1.0.7 until you publish, which is right for the v5
>   people have today.
>
> **Three things fixed on the way, nothing to decide:** the site's front page had
> carried a *"Nothing here is published yet"* note since 2026-08-20 — removed;
> the modder page's example named a fix hotfix 2 deleted (`DustDevilSpawnGate`)
> — now `LakeEntombment`, the example the store card already uses (your item
> **47**'s two wordings on that page are untouched and still yours); and the
> retired-phrase sweep over the store strings, both backups and the whole site
> came back with zero hits.
>
> ⛔ Not clearance (`H-04`). Nothing ran in a game, no status word moved,
> `version` untouched. `tools/upload_preflight.py` reads 0 FAIL; the store
> strings and both backups are byte-identical by script.


---

## ck- -- archived 2026-09-14 (was checklist status:ruled): ✅ RULED AND APPLIED. The hazard is reworded; nothing blocks the update but your sitting.


75. ✅ **RULED 2026-08-24, in-session, and APPLIED the same hour.** Your words:
    *"if we have open bug reports and we are preparing a patch that should be
    assumed we are off a freeze."* ⭐ **That is a better rule than the one I
    drafted**, and it names what was actually wrong with `editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`: it was written
    as a *state* ("frozen at 1.0.0") when it should have been about *who and
    how*. A freeze that survives into a patch cycle blocks the thing the pack
    exists to do.
    **`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)` now reads:** the version is the **sitting's** to set, never an
    agent's and never by hand; open field reports plus a patch in preparation
    means a patch cycle and **no freeze is assumed**.
    ⛔ **What I kept, because it is mechanical rather than policy** — an agent
    never opens the Mod Editor (every save runs `version = version + 1`,
    `Mod.lua:967`, and `ValidateModBeforeUpload` force-saves a dirty mod), and an
    agent never hand-sets the version numbers, because the sitting bumps
    automatically and a hand-set value on top **double-bumps** and widens the
    portal gap item 71 says never to chase.
    ✅ Every other hand edit to `metadata.lua` — the `code` list, `last_changes`,
    descriptions — is ordinary agent work and always was.
    ⚠️ **One thing left before the sitting, and it is mine:** `last_changes` still
    says `"Initial release."` That string ships inside the mod and is the patch
    note players read. It is a text-only hand edit, no bump — say go and it is
    two minutes.

    <details><summary>The original item, kept for the record</summary>

    ⛔ **`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)` forbids the 1.0.x update as written. It needs your ruling before
    any agent can prepare the upload.**
    The hazard reads *"`metadata.lua` is FROZEN at 1.0.0 — no version bump, no Mod
    Editor save."* It existed to protect the 1.0.0 upload from an accidental bump.
    **A real update requires exactly that bump**, so as written it blocks the thing
    it was never meant to block. An agent obeying STATE will refuse; an agent
    ignoring a hazard is worse. ⇒ **Rule it, don't leave it ambiguous.**
    ❓ **The call:** does `editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)` become *"frozen except at an owner-run upload
    sitting"*, or is it discharged like `H-04` was and replaced by a successor
    that guards the same accident? ⚖️ I'd take the first — the accident it
    prevents (a stray editor save silently bumping the version between sittings)
    is still real between updates.

    ℹ️ **Everything else about the deploy is already written down and needs no
    decision from you** — this item exists only because a hazard cannot be lifted
    by an agent. The sequence, the two-portal version mechanics, and the three
    checks still owed from the *first* upload are in
    [agent/reports/RELEASE_PORTAL_PREP.md](agent/reports/RELEASE_PORTAL_PREP.md)
    §0.5(c)(d)(f) and §1; the pack route is Mods Manager → Edit (`Ctrl-E`) →
    File → Pack Mod (⛔ the console is not a route).
    ⚠️ **Item 74 comes first** — it decides whether the module you are uploading
    is the repaired one.
    ✅ **Item 74 is now done (ruled (a), built — item 76), so 75 is the only
    thing between the tree and the upload.**

    ℹ️ **Drafted so this is a yes/no, not a writing task.** If you take the
    reword, `editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)` in [agent/STATE.md](agent/STATE.md) becomes, verbatim:
    > **editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)** `metadata.lua` is **FROZEN between sittings** — no version bump,
    > no Mod Editor save, ever, EXCEPT inside an owner-run upload sitting, where
    > the bump is the point (every editor save runs `version = version + 1`,
    > `Mod.lua:967`). ⛔ The accident this still prevents is a stray editor save
    > silently bumping the version while no upload is happening, which desyncs
    > the two portals further (checklist 71). An agent may never open the editor;
    > only the owner, at a sitting, and the sitting ends the exemption.
    ⛔ **An agent cannot apply this** — it is your ruling to make, which is the
    whole reason this item exists. Say the word and it lands in one edit.

    </details>

    ⚠️ **Unrelated, and it needs your hands too — the reporter's GitHub issue
    numbers were never captured.** F104 and F105 both cite "GitHub, Keelai" with
    no issue number, so neither entry can be found from the issue or vice versa,
    and F105's issue is titled something like *"Error when completing
    milestone"* while our entry is titled after the cause — the two do not match
    by search. Paste the two numbers/URLs and they go into the entries' front
    matter.


---

## ck- -- archived 2026-09-14 (was checklist status:ruled): ⚖️⚖️ YOU RULED THE POST-RELEASE TESTING MODEL, and corrected a cost I had been quoting wrong.


57. ⚖️ **STANDING RULING — the release gate was a one-time cost, not a per-change
    tax.** Your words: *"I do not plan to do a major lens sweep and b leg like we
    did for pre release unless we have to do a major overhaul of the mod again…
    My post release plans is basic checks from patch notes to see if we need to
    remove, or change fixes, and add new fixes if there are new bugs. We won't
    most likely run multi day tests ever again."*

    ⛔ **This corrects me, and future sessions should not repeat my error.** I
    priced a single UI-text module using `FIX_POLICY` §3a's per-module cost —
    save-safety pass, probe, suite re-measure, three store surfaces. Most of that
    was the **release gate amortised across 75 modules**, and it does not recur
    for one added fix on a shipped mod. Quoting it made a cheap change look
    expensive, which is the opposite of useful.

    ✅ **What a normal post-release change actually owes**, and it is short:
    * the `items.lua` entry for any new module (**module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py)** — this is the one that
      would have shipped a fix that never loads; it is a ten-second check, and it
      is not ceremony);
    * one boot log showing the new module reports `applied`;
    * a language-switched look **only** for a fix that cannot be seen in English
      (`C51` is the sole example on the books);
    * `doccheck` counts re-emitted, never hand-typed.

    ⛔ **What does NOT recur:** run B, the eight-lens sweep, the terminal audit,
    the multi-day gate. Those bought a first impression, which happens once.
    ⇒ They come back only for what you named: **a major overhaul.**

    ℹ️ Your other observation, recorded because it is the pack's premise: *"if
    paradox tested as extensively as we do as the actual paid developer, there
    would be no need for us."* The bar being higher than the developer's was right
    for the launch; it is not right for every later line of text.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ✅ your two rulings are carried out. Nothing owed back; this is the receipt.


55. ✅ **Both sibling decisions are done, in the siblings' own repos, and neither
    touched the fix pack's shipping files.** Your words: *"You can mirror the two
    core fixes for the opt in. For the rescue mod I would just note it in its
    file system as a gate if we ever need to launch it."*

    * ✅ **Opt-in pack — the two core fixes are mirrored** (`SMR-OptInPack`
      `2cedf7d`). Both repairs landed in its own `00_Core.lua`, parse-swept and
      doccheck green, and the mirror was *checked* rather than assumed: with
      comments stripped and the namespace normalised, the three edited sites are
      now code-identical to ours. ⚠️ **Not verified in a running game there** —
      nothing was launched, and its STATE now carries the one boot check its
      launch session owes (that its eight modules register once each after a
      script reload). ⚠️ One honest split you should know: the double-name fix is
      the half that was actually *measured* on that mod (its `NoHomeless` is the
      module the dialog named twice); the false-alarm fix is **pre-emptive**
      there, because no module of its own currently uses the code path that
      leaves the stale mark. It is mirrored anyway — same design, and the next
      module to use that path would inherit the defect.
    * ✅ **Rescue mod — the gate is written where a launch session cannot miss
      it** (`SMR-CommunitySaveRescue` `9c912b3`, in its `CLAUDE.md`, the file
      every session reads first). It states the verified fact (no `items.lua`,
      2-entry code list), the mechanism as *our claim with its citations*, and —
      in the words that stop it being repeated as fact — that **the consequence
      is still not derived**: nobody has read what the game does when the file is
      *missing* rather than *incomplete*, and it may simply refuse to rebuild,
      which would be harmless. The gate's outcome is binary: a citation-backed
      showing that absence is harmless, or an `items.lua` written and re-verified
      after the forced save.
    * ℹ️ **A small gift to that future session, bought by my own detour:** the
      game source is under an install folder literally named **`Project Spark`**;
      the old `Surviving Mars` folder has a `ModTools` with *no* `Src` and is a
      decoy. `EF-014` said so and I walked into it anyway, so the exact path is
      now pasted into the gate. The derivation is minutes, not the twenty I
      quoted you, if you ever want it done early — say the word.

    ⇒ **Your remaining list is unchanged and short: re-tick the three mods, then
    upload — Paradox first.**


---

## ck- -- archived 2026-09-14 (was checklist status:ruled): ✅✅ STATE.md WAS EVICTED ON YOUR DIRECTION, AND YOU RULED THE CAPS THE SAME DAY. Nothing here is owed from you.


42. ⭐ **What happened.** The agents' one mandatory-read file had quietly grown
    to **~130KB (~33,000 tokens)** — every session paid that before doing any
    work, and its 60-line budget was being satisfied while being defeated
    (single lines had become thousand-word walls). On your direction it was
    evicted: STATE.md is now a kernel (current position · hazards · your
    rulings in force · pointers), the six days of closed history moved to the
    session log as digests with grep tags, nothing was deleted (the full old
    file is readable forever via git), and a standing cleanup prompt
    (`agent/prompts/perma/STATE_EVICTION.md`) exists so you can fire future
    evictions with one line.

    **The measured numbers you asked for: old file 71,077 bytes = 33,066
    tokens (its emoji-heavy prose cost ~2.2 bytes/token); clean kernel 4,524
    bytes ≈ 1,200–2,000 tokens** — a 16–27× cut.

    ✅✅ **RULED SAME DAY** — you asked whether the line budget still matters
    (*"Is the line budget even important anymore if we are capping the token
    size?"*) and ruled: *"format it in the most efficient and safest way
    possible because the token cap will do the read job."* **Applied:** the
    60-line budget is RETIRED; doccheck now enforces **warn 9KB** (the flag
    line must be copied verbatim into your after-run report; you fire the
    eviction prompt at your leisure), **hard 18KB** (commit blocks — even
    ignored, a boot read stays under ~8,400 tokens at the old file's worst
    density vs this week's 33,000), and a **200-byte per-line cap** so walls
    can never return inside the budget. STATE.md was reflowed to
    one-fact-per-line, the eviction prompt carries your formatting rule, and
    both new checks were falsifier-proven before this note was written. All
    three numbers are adjacent constants in `tools/doccheck.py` — retuning
    is one edit whenever you want.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ THE RENAME IS DONE, EVERYWHERE A PERSON LOOKS. ✅ Your two calls came back the same day; nothing is owed.


36. ✅ **RULED 2026-08-17, both calls, same sitting.** (1) **You searched the
    in-game Mod Manager and "Relaunched Fix Pack" is free** — the one check no
    tool could run, done; the name is committed. (2) **Sibling titles: "rename
    them now"** — applied the same hour, one title line in each repo: the
    opt-in `metadata.lua` now says *"Relaunched Fix Pack: Opt-In Modules"* and
    Save Rescue's says *"Relaunched Fix Pack: Save Rescue"* (the family form
    you pre-approved in item 26, landing early on your word). ⛔ Title lines
    only, per the fence — each file's `description` still names the old family
    and carries a comment forcing that sweep before it ever uploads.
    ~~Search the in-game Mod Manager for "Relaunched Fix Pack" before it goes
    out — the Paradox Mods catalogue is the one place I genuinely cannot read.~~

    ✅ **The rename itself is DONE, same day** — every live surface in both
    repos now says **Relaunched Fix Pack**: the `metadata.lua` title that
    ships, the store card and its source record (re-proven identical by diff),
    the site's five pages, both playtest docs, the launch sheet, the in-game
    "fixes stood down" dialog, README and LICENSE. The true count was **113
    occurrences in 43 files** against the prompt's surveyed 72 — line-wrapped
    names hide from search — **and two of them were pictures: both preview
    images had the old name painted into the art.** They are re-lettered in
    the same design and typeface, and the originals are kept beside them.
    Every count the text moved was re-measured (title 18 → 19 characters; card
    body 10,781 → 10,782; nothing else moved), and **⛔ no GitHub repo, remote
    or org was touched**, exactly as you ruled. Historical records keep the old
    name on purpose — CLAUDE.md now carries the translate-mentally note.

    ✅ ~~The one timing call routed to you: the other two mods' internal
    titles~~ — **ruled above: renamed now, applied.** ⭐ **And your follow-up
    ("fix any references that you recommend") finished the job the same
    sitting:** both sibling repos are now swept end to end — metadata strings,
    the on-screen dialogs and rollover titles, code headers, READMEs, LICENSEs
    and their own CLAUDE notes all say *Relaunched Fix Pack*, with
    translate-mentally notes added so their records keep the old name honestly.
    Two genuinely stale non-name claims found on the way were fixed and
    annotated: the opt-in's `Opt_DroneOverhaul` header (old path, missing
    suffix) and the rescue `CLAUDE.md` still claiming the attended pass was
    owed (it passed 2026-08-14). ⚠️ One consequence carried forward, not
    hidden: the rescue tool's dialog text changed after its witnessed readings,
    so if that contingency ever fires, the already-required item-28 re-witness
    launch covers the new wording too. **This repo's README was also rewritten
    to current truth** — the ghost optional-modules section is gone, every
    count is this sitting's emitted number, and the false "disable via
    console" claim is replaced with the real veto-mod mechanism.

    ⚠️ **One small call I did not make for you.** The mod's internal id and its
    log tag both still say `CommunityFixPack`. Neither is something a player
    ever searches. **My recommendation is to leave both alone** — for the same
    reason you gave about GitHub: risk without reward. Every archived log and
    every baseline this project compares against greps that exact bracketed
    token, the Save Rescue tool removes things by name, and changing it would
    make no future test comparable to any past one. A bug reporter might
    briefly wonder why the log says one thing and the mod says another; that
    is the entire downside.

    ⭐ **For the record, since it will come up:** we are not the ones who
    copied. Our first commit is **24 July** with the tracker already carrying
    29 findings; his repository starts **4 August**. Two people reached for the
    same plain words. This rename is courtesy and clarity, and **no public page
    of ours mentions his mod or explains why we renamed.** *(While in there:
    two records cited his mod as Paradox Mods 153410 — that is his older *Bug
    Fixes* mod; corrected to 154004 per your screenshot.)*

    ⇒ **Owed from you: the Mod Manager search above, and the sibling-titles
    timing call. Nothing else.**


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⛔⛔ SOLO LAUNCH: ✅ the parking work is DONE; one question left before you upload


35. ✅ **The prep prompt ran the same evening and everything mechanical is
    done.** Every public surface now describes the fix pack standing alone —
    landing page, install, FAQ, fix list, for-modders, site README, the site's
    search-result description, the store card, and **both `metadata.lua`
    player strings** (not just the changelog — the description also named the
    opt-in mod, which the 22-reference survey had missed; the real count was
    ~46 passages, most saying "optional mod" in words no opt-in-shaped search
    catches). Nothing is lost: **every removed passage is stored VERBATIM,
    byte-compared before deletion, in
    `agent/reports/PARKED_OPTIN_REFERENCES.md`** with the restore trigger
    (*the opt-in publishes*) and a step-by-step restore checklist — the F85
    shelf treatment, as promised. Store card ↔ source record re-proven
    identical after the edits; every count re-measured (card body 11,209 →
    10,781 chars; the description 844 → 779; changelog now just "Initial
    release.", 16); doccheck and the site's strict build both GREEN; and the
    code was checked, not assumed — nothing in `Code/` behaves differently
    with or without the opt-in mod. **Release tag `fixpack-v1.0.1` is placed
    on this tree** per the new WORKFLOW procedure.

    **Q1 — "coming soon" vs silence: ✅ SILENCE IS APPLIED as the reversible
    default** (my recommendation — a teaser is an undated promise on a mod you
    called not ready, and it re-couples the products). Say the word and a
    one-line "coming soon" goes in exactly ONE place, the site FAQ — never the
    store card or `metadata.lua`, the two expensive-to-change surfaces.
    Nothing else moves if you flip this.

    ✅ **Q2 — RULED 2026-08-17 ("lets go with 1.0.0") AND APPLIED THE SAME
    HOUR:** `metadata.lua` now renders **1.0.0** (`version=0`), the tag moved
    to `fixpack-v1.0.0` (the interim `fixpack-v1.0.1` deleted, local and
    remote), and the ④ sheet says so. **Nothing on this item is owed any
    more — ④ is decision-free: upload the fix pack, link, Pages.** Your
    follow-up question was also acted on: the opt-in repo's STATE now carries
    the restore obligation, so the session that launches that mod cannot miss
    `PARKED_OPTIN_REFERENCES.md`.

    ✅ **Already done earlier, no action needed:** release procedure in
    `WORKFLOW.md` (tags mark what shipped), stale `wave4` branch deleted.


Things that need **your** call, not an agent's. One line each plus where the
reasoning lives; **an agent strikes a line the moment you decide** — just say so
in any session. Added 2026-08-03 by the docs-restructure chain (spec §7 / R10):
these used to be filed only in agent reports, which is where you never read.
⭐ **And fully-CLOSED decision records move whole to `PLAYTEST_ARCHIVE.md`
(rule adopted by you 2026-08-10)** — same treatment as completed test
sections, but only when nothing is owed to you; anything on-hold or holding an
owed input stays here no matter how struck-through it looks.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW the C39 repair you ruled turns out to touch TWICE as many buildings as the ruling pictured. ✅ CONFIRMED THE SAME DAY.


30. ✅ **RULED 2026-08-15: SHIP AS BUILT — all eight families, no list.** Your
    words: *"Lets go with whatever is supposed to be true to the code, which
    fits this mod as a true to code bugfix as much as possible."* You also
    challenged the framing first (*"I thought we decided on this awhile ago?"*)
    and you were right — 08-12 already ruled "extend the compensation" and
    widened the sweep yourself; this was a confirm on the size of what the
    sweep returned, not a re-opening.
    ⭐ **Why the principle picks this option and not a narrower one.** The
    shipped module carries **no building list at all**: at runtime it asks the
    building in front of it two questions — does it carry *this active law's own
    effect object* as a `max_workers` modifier, and does it fail all three class
    gates — and pays back exactly the delta vanilla's own loop would have
    produced. Coverage is therefore "whatever actually has the defect", which is
    what true-to-code means here. **Restricting it to the four Workshops would
    have required ADDING a hardcoded template list that does not exist today**,
    purely to leave identically-broken buildings broken. That is the less
    faithful option, not the safer one.
    ⭐ **And it is faithful to the law's own player-facing text**, which is the
    other half of "true to code": the law reads *"Service buildings require 50%
    less workers"* — the trade is labour, nothing else. The declined delabel
    alternative would have made the law quietly not apply to those buildings,
    contradicting its own description; extending the compensation keeps the
    promise the law prints. (Comfort is not the law's trade — it is merely what
    the four *Workshops* happen to produce with their performance, which is why
    the 08-11/08-12 conversations were all about comfort.)
    ⇒ **Nothing to do. No code change, no re-run.** Prompt 03 writes the card
    and fix-list text against the real eight-family footprint.
    ~~Ship the repair as built, or restrict it to the four Workshops?~~ — the
    original question and its full breakdown are kept below for the record.

    **Why you are being asked at all.** Your ruling explicitly widened the
    scope — *sweep all three automation labels and cover every mismatch found* —
    so what shipped **is** what you ruled. But the picture in front of you at
    the time was "four Workshops whose Comfort payment is short", and the honest
    version of that picture is now bigger, so you get to see it before it
    reaches a store page.

    **The defect, unchanged:** all three Automation laws cut a building's
    workers by **label**, while the code that pays the workers back keys on
    **class**. Buildings on the wrong side of that line lose half their staff
    and get nothing back — roughly half their output. The game's own comment
    says the two lists are assumed to match.

    | | what the law halves | what it costs today |
    |---|---|---|
    | Art / Biorobotics / VR Workshop | ✅ already known | the Comfort their shift pays |
    | TV Studio (CCP) | ✅ **measured 08-11** | Comfort **+ TV-show progress** |
    | ⭐ **Security Station** | new | **renegades neutralised** — half the security you paid for |
    | ⭐ **Security Post (CCP)** | new | same |
    | ⭐ **Drone Assembler** | new | **drone and android build time** |
    | ⭐ **Bottomless Pit Research Center** | new | **resources processed into research** |

    The last four sit on `Service Automation` (the Security pair) and
    `Factory Automation` (the other two) — the Factory law had never been swept.
    Research Automation is clean.

    **What the fix does to them:** exactly what the game already does for a
    Diner or an Electronics Factory under the same law — nothing new, no new
    number, no balance invention. Each affected building rides to roughly double
    performance on half the staff, which is the "overall performance is
    maintained" the code says it is aiming for.
    **Recommendation: ship as built.** ✅ **This is what you ruled.** Restricting
    it to Workshops would mean deliberately leaving Security Stations and the
    Drone Assembler broken while fixing their neighbours, with no principle
    separating them.
    ⚠️ **What you should know either way:** these are gameplay-visible numbers
    (security, drone throughput, research), so a player who has been running
    Automation laws will notice the difference. That is the repair working — but
    it is a bigger visible change than "Workshops pay slightly more Comfort",
    and prompt 03 will have to say so on the store card. ⛔ **That disclosure
    survives the ruling** — shipping as built settles the SCOPE, not whether the
    card mentions it.
    ⭐ **Mitigating fact, from the sweep:** all three Automation laws share the
    `Automation` policy slot, so **at most one can be active at a time**. In any
    one game the repair reaches the four Workshops + two Security buildings
    (Service law) *or* the Drone Assembler + Bottomless Pit (Factory law) —
    never all eight at once.
    ⚠️ **Evidence honesty, unchanged by the ruling:** only `TVStudioWorkshopCCP1`
    is MEASURED (08-11 unfixed, 08-15 fixed). The other seven are SOURCE — a
    class-graph resolution with every row re-read by hand at its declaring file.
    The runtime discriminator bounds the risk: the code can only fire on a
    building that genuinely carries the cut and genuinely fails the gates.
    → the full sweep, every class chain re-read at source, and the design
    reasoning: `agent/bugs/C39.md` §2026-08-15.

ℹ️ **Also for awareness, no call needed:** the **F85** fix you ruled on 08-12
is built the same evening — the distress-call dialog's non-pausing flag is
cleared so the game's own code builds its pause layer. ✅ **2026-08-15: both
builds are VERIFIED** — the suite passed in a real launch (80/0/16/0 of 96)
and both repairs were read working in a second launch on your own colony copy;
both entries now carry `tested-unattended` under your 26b vocabulary. ⚠️ The
same day's route check found the dialog itself is dead-coded on retail —
item 31 above owns what that means for the two player-facing descriptions.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ NEW D13 CHAIN CLOSED; the ONE combined sitting is READY (step ② — the release line's next move is yours)


26b. ✅✅✅ **THE COMBINED SITTING RAN 2026-08-14 AND ALL THREE MOMENTS PASSED.
    ⭐⭐ D13 IS `tested`. NOTHING HERE IS OWED BY YOU ANY MORE.**
    **Your cost: 34 minutes** of parked handover time measured off the harness
    heartbeats, against a 30–45 promise — inside a ~67-minute wall clock whose
    difference is your own landscaping lead and one stalled launch. Six logs
    archived byte-verified (`archive/cs_*`). **0 `[LUA ERROR]` in every cell.**
    * **F102's minute** → item 11 above, struck. Sign renders, selectable.
    * **PT-20 redo** → state 3 confirmed (`pack=0/0` + `opt-in=0/0`, kit alone in
      `Loaded mod items for:`), all 8 pack-naming lines accounted, ~21 min of your
      ordinary play + a save + a reload, **zero errors in the flushed file**.
      Recorded as **superseding** the old 98-vs-98, not confirming it — that was an
      error count from the F86 era and F86 is repaired.
    * ⭐⭐ **D13 after-sweep** → `removed 1566` by name on a NATIVE witness,
      **matching a prediction committed before the sitting row for row and skip for
      skip**; the F48 repair kept; `heals: 0, 0, 0` because nothing was broken. And
      the three readings no log can ever hold: **report dialog raised** with the
      right text, **cleaned reload silent** (with `save-rescue=1/1 active` beside
      it, so the silence means something), **stand-down exactly once**.
    ⚠️ **Three things went wrong and none of them was the mod.** (1) Save Rescue
    came back from its junction round trip **not enabled** — that cost you one
    Mod-Manager visit and a launch, and it contradicts `EF-055`; two candidate
    causes recorded, neither ruled out. (2) The frozen spec promises the dialog
    says *"(drone speed and carry capacity are back to the game's own values)"* and
    the code prints a bare *"2 drone stat dials"* — step ③ would have shipped a
    text the build does not produce. (3) Two defects in my own instruments (the
    Test Kit's on-screen output covered the dialog it was there to witness; a
    reader applied the removal contract in a packs-present cell and cried wolf).
    ℹ️ Your landscaping-overlay lead is carried as a rider and costs you nothing.
    *The prep note that preceded it:*
    ~~⭐⭐ **THE COMBINED SITTING'S PREP IS *DONE AND MEASURED* — IT IS WAITING ON
    YOUR CHAIR ONLY** (2026-08-13). Three unattended dry-run launches have
    already happened with the game closed and nobody at the keyboard; every
    fixture is verified to exist, the harness is proven, and the predictions
    are committed. **Sit down and say "run the combined sitting"** on a session
    opened at `agent/prompts/perma/COMBINED_SITTING.md`. **Your part: ~30–45 min, four
    launches, two Mod-Manager visits.** The measure-moments (full table in the
    brief):
    * **F102's minute** (packs ON). ⛔ **Two corrections you would otherwise have
      hit at the keyboard.** There is **no save called `Sylmacaink BH25`** — all
      88 were read at their headers and nothing carries that name. And there is
      **ONE** deposit sign on your campaign's asteroid, not three. ⭐ The rig
      switches to the asteroid map and *selects the deposit for you*; you only
      look. Everything else is already measured: the fix's LoadGame sweep fired
      on it (`1 … re-signed onto the clean entity`), the deposit reads the new
      entity, and `ExoticDepositSign [active]` is in the log. Your words:
      **"sign renders: yes/no"**, **"selectable: yes/no"**. Closes item 11's
      local half.
    * **PT-20 redo done RIGHT**: your Mod-Manager disable of **both** packs
      (Test Kit stays) + **full restart** (state 3 — the old 98-vs-98 may have
      measured the half-disabled state) + ~10 min ordinary play + one save and
      reload; every rig reading carries its `pack=0/0` gate line.
    * ⭐ **D13 attended after-sweep, same state-3 window**: you load a staged
      big-save copy and WATCH — the two dialogs write no log line, so your
      eyes are the only instrument that can ever sample them (report dialog
      raises with the frozen text; second load silent; stand-down dialog once
      after you re-enable). **A clean run here is what finally grants D13
      `tested`.** ⭐ The staged save carries **both Drone stat dials natively**,
      so you will watch the artifact take off the one piece of residue that keeps
      changing a player's game after they uninstall.
    * Optional: the CAPTURE_SITTING passes that fold in (item 24) — prep worked
      out which pass rides which launch, and they cost no extra restarts.
    ℹ️ **Two things prep found and fixed, no decision owed.** (1) Leaving Save
    Rescue installed for the PT-20 leg would have silently voided it — it would
    have stripped the very leftovers PT-20 exists to prove are harmless. It is
    now pulled for that leg and restored afterwards, agent-side, at no cost to
    you. (2) ⛔ **A byte copy of an autosave is still an autosave to the game's
    rotation, and it deleted this sitting's own fixture *and* your held
    `Autosave Sol 311` during prep.** `Sol 311` was **restored byte-exact** from
    the pre-copy; the fixture was re-staged from a save that is not an autosave;
    `EF-056` is amended. Nothing of yours is lost.~~
    ⚠️ **The autosave rotation fired twice more DURING the sitting** — it took
    `Autosave Sol 311` and `Autosave Sol 311(2)` while you played, and wrote
    `Autosave Sol 316`. **Both restored byte-exact**, and every autosave was
    re-verified at close-out. That is the amended rule paying for itself three
    times in two days, and it is why it now says reconcile after *every* launch
    rather than reason about which one will fire.
    ✅✅ **RULED 2026-08-15, AND THEN AMENDED THE SAME DAY BY YOU — THE SPLIT IS
    ADOPTED AND IT IS ALREADY BUILT.** Your first answer was "a sitting with me
    at the keyboard earns `tested`", which would have left every unattended
    verification stuck at `fixed`. You then backtracked on exactly that
    consequence: *"If we are changing rules I think I would be more comfortable
    with labeling things tested - unattended / tested attended. It still gives
    unattended appropriate weight, but allows the attended tested to have more
    serious weight if we are troubleshooting, because that has the approval of
    the agent and human hands on."* **Adopted as written.** The vocabulary now
    has three words and `doccheck` enforces them:
    * **`tested-attended`** — you were at the keyboard. The strongest word the
      project has, and the one a troubleshooting session is entitled to lean
      on: agent instrumentation *and* human eyes.
    * **`tested-unattended`** — real launches, nobody watching. Full weight for
      anything an instrument can read; ⛔ **never for a screen event** — "the
      flag read false" is a measurement, "the popup visibly paused" is not.
    * ⛔ **bare `tested`** — LEGACY, closed to new work. See the honest caveat
      below.
    ⭐ **Applied immediately, and it pays today:** `F85` and `C39` were verified
    unattended last night with real launches and zero errors, and they move
    **`fixed` → `tested-unattended`** rather than being stranded. No evidence
    changed; the word for it did. What `tested-attended` would still buy is
    named on each entry (F85: the screen witness — does the popup visibly
    pause; C39: seven of eight families still SOURCE, and the law was enacted
    directly rather than voted).
    ⚠️ **The honest caveat, and it is why the old word survives.** 46 entries
    already carry bare `tested` and **their attendance was never recorded** —
    29 at least cite a sitting or co-run, but **17 carry the literal word
    `tested` and no narrative at all** (`F03`, `F44`, `F66` and 14 others).
    Retro-labelling them would mean stamping an attendance claim on entries
    whose record cannot support one, which is the exact failure mode the
    evidence bar exists to stop. So bare `tested` now means **"attendance
    unaudited"** — not "attended" — and no agent may read it as the stronger
    word or promote it without re-deriving from the archived record.
    ✅ **RULED 2026-08-15: NO RETRO-PASS.** The 46 legacy labels are left exactly
    as they are and are never upgraded in bulk. ⛔ **Standing consequence, for
    any agent reading one:** bare `tested` is an unaudited label — cite it as
    "recorded `tested`, attendance unknown", never as evidence a human watched.
    If a specific legacy entry ever becomes load-bearing in a real
    investigation, re-derive that ONE entry from the archived record; do not
    reason from the word. ~~whether you want that retro-pass done at all.~~
    ~~the status vocabulary has no word for "verified-unattended" (`doccheck`
    rejects `verified`), so that truth lives in narrative only.~~
    ℹ️ Also for your awareness, no decision owed: the audit FILED **F103**
    (our Crystals-mystery repeater can double its hourly broadcast after a
    mid-mystery load — harm nil, one consumer that wants the message,
    self-limiting three ways; remedy sketch recorded) as post-release WATCH
    under your frozen ship line.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ F105 IS FIXED ON YOUR WORD, AND BUILDING IT EXPOSED A NEW QUESTION. One receipt, one call.


**The receipt (item 72 — RULED by you, in-session: "This is a number 1 fix
priority").** `Fix_LandscapeCostRefresh` is built, registered, and boot-verified
the same session: `[CommunityFixPack] LandscapeCostRefresh: applied`, zero error
lines, menu-only leg, no save touched (log
`docs/archive/f105_Mars.exe-20260824-00.08.38.log`; PROBE SWEEP: clean). The
investigation also **corrected two things the filed entry believed**: the
Efficiency laws are NOT triggers (only three techs are — NeoConcrete,
DomeStreamlining, MarsNoveau), and `ClearWasteRockConstructionSite` (plain
rock-clearing jobs) crashes the same way, not just levelling.
→ [agent/bugs/F105.md](agent/bugs/F105.md) · report `agent/reports/F105_INVESTIGATION.md`
**Three things to know, none urgent:**
* ⚠️ **The live listings are now one module behind this tree** (78 modules vs
  the shipped 77). Whenever you want it live, it is the normal update sitting:
  editor save (bumps the version), pack, upload — both portals. Nothing else is
  queued behind it.
* `metadata.lua` gained ONE hand-written `code` row (the new module), version
  untouched — no editor save happened, so editor/version rail (agent/prompts/perma/RELEASE.md § Release rails) held.
* ⛔ Still never reproduced on the rig. The 10-minute repro (place a levelling
  site, research a dome-cost tech, watch `ConstructionSite.lua:673` stay
  silent) rides your next sitting if you want the attended upgrade.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐⭐ F105 IS REPRODUCED ON OUR OWN RIG, AND THE FIX WAS WATCHED TO STOP IT. Nothing is owed; this is a receipt.


77. ⭐⭐ **The one thing every F105 document said had never been done, is done —
    and you did it in about twenty minutes.** Until today the whole of F105 was
    read off the shipped Lua against a stranger's log. Now:
    * **Leg A, pack OFF — the defect fires. 14 raises of
      `ConstructionSite.lua:673`** (`docs/archive/f105_legA_Mars.exe-20260824-15.28.06.log`,
      lines 147-388). A real Flatten job, worked by real drones to
      `state = clean` with a live WasteRock request, **state verified at the
      console before firing rather than assumed**, then a cost tech researched.
    * **Leg B, pack ON — it does not.** Zero `:673` in the entire session
      (`f105_legB_Mars.exe-20260824-16.07.29.log`), with a landscape site active
      and **Mars Nouveau researched** — which you confirmed on the tech screen.
    ⭐ **Your mid-leg re-tick covered a third thing for free.** Enabling the pack
    on an already-running process is the `F87` **enable path** — presets loaded,
    classes not yet built — which `FIX_POLICY` §2 calls "every player's first
    run". The unattended harness leg was a cold boot; both paths are now covered
    for this module.
    ⭐ **A third pack-OFF leg (leg C) came in after the write-up and CORRECTED
    the write-up.** `f105_legC_*.log`: 12 raises, and `[CommunityFixPack]` appears
    **zero** times — the cleanest control of the three, no re-tick to explain.
    ⛔ **It also refuted something I had just told you.** I wrote that the console's
    `pcall` meant the raise "never reached the engine's uncaught handler". Wrong:
    every raise is logged **twice**, adjacent — 6 uncaught `[LUA ERROR]` plus 6
    console-caught in leg C, and 7 + 7 in leg A when I went back and counted.
    ⭐ **Which makes item 73 cheaper than I told you.** The thing that has never
    fired is not the uncaught path — it is `ReportModLuaError`. `Mod Flagged` is
    zero in all three legs simply because with the pack OFF there is no mod name
    in the stack to match. So seeing the real player popup needs **pack ON with
    this one module disabled** — no console trickery required, and the uncaught
    path is already measured firing.
    ⭐⭐ **And a fourth leg you designed, which is the one that matters to players.**
    You saved *after* the defect had fired (`Post 105-dirty`), ticked the pack on,
    fully exited, relaunched and loaded it — the exact position of someone who hits
    this bug and *then* installs the pack. **Applied, zero errors.**
    ⇒ **A player does not need a clean save.** They can hit F105, install the pack
    afterwards, and carry on in the same colony. That is measured evidence for the
    store page's "safe to add to a save you have already played" — for this defect.
    ⛔ I tried to caveat that the guard might not have been *called* during that
    load; **you were right that this is semantics against effect** and I dropped it.
    The wrap is a permanent shield on the reader, so called-or-not it is installed
    for every later call and no future trigger can raise while the pack is on.
    ⛔ Still not a repair: the site stays broken and the guard makes it harmless, so
    uninstalling brings the defect back — which is what the store text already says.
    ⭐ It also settles **item 72**'s shape question with a measurement instead of an
    argument: shape (b), initialising the writer, could never have helped that save,
    because the gatherer ran long before it existed. Only guarding the reader does.
    → [agent/bugs/F105.md](agent/bugs/F105.md), section "THE FIELD ROUTE, REPRODUCED"
    ℹ️ ⚠️ One loose thread I am not dropping: leg A's log line 107,
    `Unpersist missing permanent: Mod/SMR_CommunityFixPack`. It is what PROVED
    the pack was off — but it also says a save carries a persisted reference to
    our code, and `FIX_POLICY` §3a's posture is that it should not. Filed for a
    look after the upload; nothing about it blocks anything.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐⭐ IT IS PUBLISHED, ON BOTH PORTALS. The ids are committed. One number came out differently on each store, and that was mechanical, not a mistake.


71. ⭐⭐⭐ **Live.** Paradox Mods **156049** · Steam Workshop **3787202810**. Both
    ids are now in `metadata.lua` and committed — ⛔ **that is how every future
    update finds the listings instead of creating a second one.**

    ⚠️ **The two stores show different version numbers for identical code, and
    nothing went wrong.** Paradox saves *after* the upload returns, so it got the
    package built at `version 0` → **1.0.0**, exactly as you ruled. Steam saves
    *before* it packs, so its bump landed **inside** the archive → **1.0.2**.
    Running both in one sitting is what produced the gap; the sheet predicted it
    (§0.5(c)) and it is now on the record rather than a mystery for later.
    ⇒ **This retires item 37 Q2** — Steam's number was decided by circumstance.
    ⛔ **Do not re-upload to tidy it.** Another upload bumps again and makes the
    two further apart, not closer.

    ℹ️ Steam's file is **385,131 B** against our packed **391,567 B**. Also
    expected: that same forced save stripped every comment out of `metadata.lua`
    and `items.lua` before packing them. **The 78 code files are byte-identical
    on both portals** — only one integer and two files' comments differ.
    ⇒ The delivered-bytes check (§0.5(f)) now says so: md5 **against Paradox
    only**; Steam reconciles by entry list, not by hash.

    ✅ **Repaired here, and it is the writeback the sheet warned about:** the
    saves stripped ~140 lines of comments from those two files. `items.lua` had
    **zero** value changes and was restored whole; `metadata.lua` kept its six new
    fields and its `version 2` and got every comment back, with the split above
    written into the file where the next reader meets it.

    ⛔ **One tool defect found while doing it.** `upload_preflight` reported
    **20 checks before the upload and 18 after** — `SaveDef` omits properties at
    their default, so publishing deleted `version_minor`, and the guard printing
    *"PackVersion a player sees"* silently dropped both version lines. The tool
    went quiet about the version at the exact moment the version got complicated.
    Fixed: a missing minor now reads as `0`, mirroring the engine's own default
    (`Mod.lua:265`). It reads **20 checked · 0 FAIL** again, and prints
    `PackVersion 1.0.2`.

    ✅⭐ **YOU SUBSCRIBED, SO THE DELIVERED-BYTES CHECK RAN — the first time this
    project has ever verified what a player actually receives.** Every byte check
    before it stopped at the file we upload.

    **Steam: checked, and clean.** The downloaded copy is **385,131 B**, matching
    the page; **82 entries**; and against our tree **80 are byte-identical and
    exactly 2 differ — `metadata.lua` and `items.lua`**, the two files that save
    rewrote. ⇒ **All 78 code files a Steam player gets are byte-for-byte the ones
    you watched working.** I read `version` out of the archive itself: **`2`**, so
    Steam is confirmed **1.0.2** by measurement rather than reasoning.

    ⏳ **Paradox needs one more thing from you, and it is small.** Subscribing on
    the website downloads nothing — `PdxMods\` holds only an empty `temp_pdx`; the
    game fetches it at startup. ⇒ **Next time you launch, it lands on disk and I
    read its version the same way**, which closes the question below for good.

    ⛔⛔ **AND ONE THING I TOLD YOU ABOVE MAY BE WRONG — I am flagging it rather
    than leaving it.** I said Paradox holds 1.0.0. The Paradox browse card reads
    **376 KB**, which is Steam's 385,131 B in KiB — *not* our 391,567 B pack. If
    Paradox received the same stripped, bumped archive Steam did, then it is
    **not** 1.0.0 and the version story is one number, not two. The counter-
    evidence is real: `pdx_version` came back `"1"`, which is only reachable if
    Paradox saved *after* uploading a version-0 tree. ⇒ **One download settles
    it** — §0.5(f) already asks you to pull the published copy; when you do, I
    read the `version` inside its `metadata.lua` and correct the record either
    way. ⚠️ Until then, do not repeat "Paradox is 1.0.0" as settled, including
    anywhere on the store pages.

    ℹ️ **Also on that card, worth your eye, not mine to change:** the author
    renders as **`cat144`**, while `metadata.lua` says `catt144`. Portals
    usually show the *account* name rather than the metadata field, so this is
    probably just your Paradox account — but if it is a typo in the account, it
    is the kind of thing that is easier to fix on day one than later.

    ⇒ **Still owed on the live listings, all yours:** §0.5(d) the required game
    version **350453** on the Paradox page if it offers the field · §0.5(f) the
    download checksum · then the site: I put both store links in, you switch
    Pages on, and the site link goes back onto the two store pages (§1 steps
    2–4). ⭐ **Say the word and I'll do the store-links step now** — I have both
    ids; I only need the Paradox page URL in the form your browser shows it,
    because I will not construct a store URL from a pattern.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⚠️ C50 IS BUILT, AND IT TOUCHES THREE SCREENS RATHER THAN THE TWO ITS BRIEF NAMED. Your sitting in link 4 changes slightly.


59. ⚠️ **What I found, and the call I made without stopping you.** The brief for
    `C50` named two places SpaceY's description gets assembled and said to append
    at both. I re-derived that list before building — the brief told me to prove
    the caller counts myself — and **it was wrong in both directions**:

    | screen | what happens now |
    |---|---|
    | the pre-game **mission summary panel** | bullet added ✅ *(in the brief)* |
    | the **rollover when you hover a sponsor** in the picker | bullet added ✅ *(NOT in the brief — a live screen the record had never named)* |
    | the **challenge landing-spot screen** (3 shipped Challenges use SpaceY) | bullet added ✅ *(NOT in the brief either)* |
    | the "in-game mission profile" the brief listed | ⛔ **left alone — that function has zero callers anywhere in the game.** It is dead code; the in-game profile dialog does not show sponsor effects at all. |

    **My call:** build all three live screens, skip the dead one. Fixing one of
    three would have left the defect visible on the other two, and `FIX_POLICY`
    §4a bars shipping code for a function no shipped caller reaches (the F28
    lesson — we retired a fix over exactly that once). ⚖️ **If you would rather
    it stayed to the two the brief named, say so and I will cut it back** — the
    third site is one wrapper and comes out cleanly.

    ⚖️⚖️ **RULED 2026-08-20: KEEP all three sites** (owner: *"keep 59"*). ⇒ No code
    changes; the challenge landing-spot wrapper ships. ⭐ **Looking at it during the
    sitting stays optional** — §2a of the test brief says that if it is not opened,
    the report names it as an unobserved site rather than counting it as a pass.

    ⭐ **What changes for your ~30-minute sitting (link 4).** The bullet is now
    visible in **two places without starting a game**: the sponsor summary panel
    *and* the hover rollover on the sponsor list — so you get two independent
    looks for free while you are already on that screen. The third, the challenge
    landing spot, needs a SpaceY **Challenge** started; ⚖️ **that is the one I
    would skip unless you want it** — it is the same code on a screen you would
    otherwise have no reason to open, and the probe already checks the wrapper is
    installed there.

    ⛔ **Nothing about this moves the store card's "five judgment calls" count** —
    your 08-20 ruling that `C50` is a plain repair still stands and is untouched.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ THE PLAN CHANGED ON YOUR RULING: C50+C51 ship IN 1.0.0, C52 is frozen, and the chain that closes this repo is written and waiting.


58. ⭐⭐ **Your ruling, and what is now sitting ready.** *"C52 is going frozen may
    revisit at a later date. C50-C51 we are going to close out and launch. With
    basic testing. One chain to do both, with a testing chain right before the
    fable audit… I don't want to upload and move right into 1.0.1 work. I would
    rather shift resources and start working on the opt in."*

    ✅ **`C52` is `parked` — frozen, reversible, and fenced.** No session may open
    it without a fresh word from you. ⚠️ One piece of it is *not* parked because it
    is not a code fix: the mod browser caches preview art on **id + version**, so
    if you ever replace the preview after publishing **without a version bump**,
    everyone who already saw it keeps the old picture forever. That lives on the
    upload sheet now.

    ⭐ **The chain is written: `agent/prompts/closeout-1.0.0/`, five links.**

    | # | link | needs you? | what it does |
    |---|---|---|---|
    | 1 | build `C51` | no | the three untranslatable strings |
    | 2 | build `C50` | no | the SpaceY bullet |
    | 3 | surfaces | no | the two fix-list entries, counts, the stale pack fingerprint |
    | 4 | ⭐ **the sitting** | **YES, ~30 min** | the only eyes either fix ever gets |
    | 5 | Fable audit | no | breaks it, moves the tag, rules ship-or-revert |

    **Kick off link 1 with:** `docs/agent/prompts/closeout-1.0.0/01_BUILD_C51.md`
    — each link ends by handing you the next line, and link 5 ends by handing you
    the opt-in.

    ⭐ **What your sitting in link 4 actually is:** one launch. Check both modules
    say `applied`; look at SpaceY's description on the sponsor screen (the new
    bullet, *and* the first bullet's cargo number, which is the one thing that
    could have broken); glance at the terraforming panel and the rocket's *Back to
    Earth* rollover, where you should see **no change at all**; then switch the
    game to German, look at the same three things, and switch back. ⭐ That German
    look is the only way `C51` is visible to anybody, and it is also the first time
    this project will have watched a translated string render in another language
    — a gap our own records have carried open since 2026-08-02.

    ⚠️ **Two consequences of building before launch, stated up front, neither a
    surprise:** the release tag will **move** in link 5 (it currently marks bytes
    measured in run B, and two new modules invalidate that), and the recorded pack
    fingerprint — the md5 you were told to checksum your download against — goes
    stale, so link 3 rewrites that check to use the md5 recorded when *you* pack.
    ⛔ Nothing about the upload route changes: still Paradox first, still
    `IsDirty()` false and 1.0.0 on screen before anything is pressed.

    ⇒ **After link 5 this repo is closed** — nothing queued, nothing owed, until a
    player report, a real problem, or a game patch. Which is the point.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⚠️ the SAME defect class, in the third mod. Not today's problem; do not let it be forgotten.


48. ⚠️ **The Save Rescue mod has no `items.lua` at all**, against a 2-entry code
    list (`Code/00_Core.lua`, `Code/10_SaveRescue.lua`). Item 46 explains why that
    file matters: uploading forces the editor to save, and the save **rebuilds the
    list of code files to load from the items file alone — it never looks at the
    disk.** The fix pack had one item missing and would have shipped a fix that
    never loaded. The rescue mod has **no items file whatsoever**.

    ✅ **This does not touch tonight.** The rescue mod is the held-in-reserve
    contingency (item 17) and is not publishing. The opt-in pack was checked and is
    **correct** (9 for 9).

    ⛔ **But it must be settled before that mod ever uploads**, and the sweep
    chain's own rules forbid its sessions from touching sibling repos, so this
    would otherwise be lost. ⚠️ I have **not** derived what the game actually does
    when the file is absent — it may refuse to rebuild rather than rebuild empty,
    which would be harmless. **That question is the work**, and it is twenty
    minutes with the source, not a guess to be recorded as a fact.

    ⇒ **Folded into your item 37 Q1** (*"mirror the core fixes into the opt-in pack
    now, or leave them?"*): whatever you rule there, the same visit should carry
    this. **Recommendation unchanged — do the sibling work in one pass**, while the
    diagnosis is fresh, rather than making each mod's launch session rediscover it.
    ℹ️ Nothing owed beyond that ruling.

    ⚖️ **RULED 2026-08-20: record it as a gate in that mod's own repo, do not
    derive it now.** Written into `SMR-CommunitySaveRescue`'s `CLAUDE.md`
    (`9c912b3`) — the undecided consequence is carried openly as undecided, and
    the source path for whoever discharges it is pasted in. Receipt: **item 55**.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⚠️ the launch test's own first question could not fail. Already fixed; nothing owed unless you disagree.


49. ⚠️ **The final launch test had a check that was incapable of failing, and I
    changed it.** ⇒ **Nothing to do** — this is the "what happened" note, and a
    single call is yours only if you dislike the change.

    **What happened, in plain words.** Before this mod goes out, there is a final
    test — "run B" — that loads the mod **the way a player receives it**: zipped
    into a single package file, rather than through the shortcut we develop
    against. It has ten pass criteria and the **first** one is *"the mod loads
    packed"*, because if that is wrong, the other nine measured the wrong thing.

    The way that first check was written, it was satisfied by *"the mod printed
    its usual lines in the log"* — which it does **either way**. So if the
    shortcut had been left in place by mistake, the test would have quietly
    measured our development copy, ticked the box, and every number after it
    would have been wrong while looking right.

    **What I changed.** The game itself writes down which way it loaded the mod,
    in one log line, in plain words: `packed` or `unpacked`. The check now reads
    that line. ⭐ **And I checked our own history: 66 recorded sessions carry that
    line, and all 66 say `unpacked`.** So "this mod has never once been loaded
    the way a player will load it" is no longer something we believe — it is
    something the logs say, in a line anyone can search for.

    I also wrote down a related trap in the test's instructions: if the shortcut
    **and** the packaged copy are both present, the game silently prefers the
    **shortcut**. So "remove the shortcut first" is not tidiness, it is the
    difference between a real test and a fake one.

    ℹ️ **The only thing that is yours:** if you would rather the first check stay
    loose, say so and I will put it back. Otherwise nothing is owed here.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⚠️ run B now has an ATTENDED moment in it. Nothing to decide; something to know.


45. ⚠️ **The launch rehearsal is no longer zero-cost to you, and finding that out
    early is the good news.** The verification launch measured something nobody
    knew: **pulling a mod's junction disables it in account state, and putting the
    junction back does NOT re-enable it** — proven across two relaunches, and the
    mod vanishes *silently*. Run B was written to pull the fix pack's junction the
    same way, so as designed it would have shown the pack **absent** and read as a
    catastrophic failure of the mod — when it was a failure of my procedure.
    ⇒ Run B now budgets **one Mod-Manager tick from you** after the swap, and
    reads the gate line before believing any other number.

    ⭐ **Two console lines ride along on that same visit, and they are the last
    outstanding verification of the two fixes that paused this upload.** The
    console is blacklisted in unattended runs, so this visit is the only place
    they can happen — and they now cost nothing extra:
    `print(SMRFixPack.fixes.SaintBlessing.update_suspect)` (expect `nil`) and a
    duplicate check on the module list after forcing a second script load.

    ⛔ **Why they were not done already, and it is not an oversight:** the
    falsifier I wrote for those fixes could not work. It used the pack's own
    `UpdateSuspects()`, which reads the suspect mark **only** on modules that are
    switched off — so a stale mark on a *working* module is invisible to it. The
    verification session ran it, got a clean `0`, and **refused to call the fixes
    verified**, which is exactly right and better than the brief it was given.

    ℹ️ **Nothing owed by you** beyond being at the keyboard for that one moment.

    ⚖️ *Recorded so nobody does it casually later:* the obvious permanent fix —
    add a Test Kit probe that checks this every run — is **post-launch work**.
    Adding a probe moves the suite count 96 → 97, and *"a suite of 96 checks"* is
    printed on the store card. That number has already been wrong twice.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⛔⛔ THE UPLOAD IS PAUSED ON YOUR OWN WORD. Two defects found at the sitting and fixed; two questions for you.


37. ⛔ **What happened, in plain words.** You opened the Mod Editor to upload,
    and a dialog appeared from the *other* mod saying *"2 of this mod's modules
    found that the game code they patch has changed… Switched off: NoHomeless,
    NoHomeless"*. You asked whether that was only there because the opt-in mod
    was switched on. It was — five separate controls confirm it, and **a player
    installing the fix pack alone could never see that particular box.** But
    reading *why* it said the same name twice found **two real defects in code
    the fix pack ships too**, and you overrode the recommendation to ship and
    fix later: *"I don't want to launch with an immediate planned 1.0.1 fix
    routed for launch. I want us to be clean period."* Both are now fixed.

    * **The false alarm.** A module that fails one start-up pass and succeeds on
      the next — normal, documented, happens every launch — kept a "suspect"
      mark that nothing cleared. Any later stand-down then read that stale mark
      and would have shown a player a box on a **brand-new release** claiming
      the game's code had changed and inviting them to go find a newer version,
      about a fix that had just worked. It never fired, by timing rather than by
      correctness. ⛔ It would have been a bad first impression that was also
      simply false.
    * **The double name.** Our own registry appended a module twice whenever the
      game reloaded its scripts, so one module was counted and listed twice.
      That is why it said "2" and named NoHomeless twice when only one module
      had stood down.

    ✅ **Both fixed in `Code/00_Core.lua` (`2f077e8`); `metadata.lua` untouched,
    so this is NOT a 1.0.1 — nothing has been published, and 1.0.0 is simply
    what 1.0.0 now is.** ⛔ **Nothing is verified yet in a running game**, and
    the release tag is deliberately parked one commit behind until it is.

    ⭐⭐ **Your chain is built and waiting: `agent/prompts/prelaunch-sweep/`** —
    your design, *"a chain that is self replicating… it doesn't stop until a
    chain finds nothing,"* with three changes I'd argue for and you can overrule:

    * ⛔ **Blinding the next session does not work in this repo** — our own rules
      make it read `git log` and STATE, and our commit messages are essays. So
      links are blind on **findings** (`SWEEP_FINDINGS.md`, forbidden) and
      sighted on **coverage** (`SWEEP_LEDGER.md`, required). Chain commits use
      deliberately boring one-line subjects so a staleness check can't leak.
    * ⭐ **Vary the question, not the sweep.** Eight lenses, one per link. The
      reason is your own observation: tonight's finds came from asking something
      no brief had asked, not from sweeping harder. Five identical sweeps mostly
      re-cover the comfortable ground.
    * ⚠️ **"Until one finds nothing" is not safe on its own** — silence has two
      causes, and one of them is a shallow sweep. So it stops on *nothing new in
      **unswept** territory*, or two cosmetic-only links, or a cap of 5 — and the
      terminal audit must **name which**, because reporting a cap as a clean bill
      is the worst thing this design could do.

    Links 1–2 may fix; 3+ record only (each fix adds risk to a release
    candidate), except launch-blocking findings, which are fixed at any link.
    **Each link reports to you and stops; you kick off the next.** The Fable
    terminal audit reads everything, re-reads today's fixes hostilely, does its
    own final sweep, and issues the upload verdict.

    ⭐ **Plus the two things you added, which are the best part of it.** The
    launch **dry run** (`98_LAUNCH_REHEARSAL.md`): ⛔ nothing may touch a portal
    API — the first API call is the one that *creates the listing*, so "every
    step up to publish" isn't the safe line — but the upload's **validation** is
    separable from its transmission, so `tools/upload_preflight.py` now runs all
    six Paradox guards plus Steam's size limits locally, **in seconds, forever.**
    I proved it catches tonight's blocker by deleting the field again. And your
    A/B call is written in as you framed it: **A is information, B is the gate.**
    ⛔ B is the first time in this project's history the mod will be run the way a
    player receives it — **packed, junction pulled, TestKit and opt-in off.**
    Every gate number we own was taken unpacked with a third mod loaded that
    rewrites globals.

    ❓ **Q1 — mirror the two fixes into the opt-in pack now, or leave them?**
    Both defects are identical in that mod's own core — it is where the dialog
    came from. It is parked and not uploading, so this does not gate tonight.
    **Recommendation: yes, now**, while the diagnosis is fresh; the alternative
    is that its launch session rediscovers this from scratch. ⚠️ Its own gates
    would need re-running, which is why it is your call and not mine.

    ⚖️ **RULED 2026-08-20: yes, mirror them.** Done in `SMR-OptInPack`
    (`2cedf7d`), nothing in this repo touched — the receipt, including what is
    measured there versus pre-emptive, is **item 55**.

    ✅ **Q2 — Steam's version number: CLOSED, no decision needed.** Retired by
    circumstance at the 08-20 dual upload, and doubly moot since: from the 08-24
    sitting on, an UPDATE bumps once and Steam packs after Paradox's save, so
    **both listings now ship the same `version` 4** — measured in the delivered
    Steam archive 2026-08-29 (`EF-068`). ⇒ item 37 is closed in full.

    <details><summary>The original question</summary>

    ❓ **Q2 — Steam's version number.** ⛔ Decide **after** Paradox, not now.

    </details>
    Paradox Mods saves *after* it uploads, so it receives a clean **1.0.0**.
    Steam saves *before* it packs, so a straight second upload would ship
    **1.0.1**. Getting Steam to 1.0.0 as well costs one extra restart and a
    one-field edit. **Recommendation: take the extra restart** — you ruled a
    clean first number for exactly the reason it is worth keeping on both
    stores — but it is genuinely a shrug either way and you lose nothing by
    deciding when you get there.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ SWEEP CHAIN, LINK 1 REPORTED. Nothing blocks launch. One small call for you, and it can wait.


38. ⭐ **Link 1 of your chain is done — lens 1 of 8, "structure & collision".**
    The question it asked, which no brief here had asked before: **do our own 75
    modules step on each other?** To answer it properly I built the thing the
    project has always described and never produced — a map of *every symbol the
    pack patches and which module patches it* — and then checked it against the
    game's own class tree. It is committed as
    `agent/reports/L1_COLLISION_MAP.md`.

    ✅ **Nothing blocks launch, and I changed no code.** The pack does not fight
    itself: 16 global replacements, 16 different globals; no two modules write
    the same preset field; no two share a thread. The eleven modules that all
    hook "game loaded" don't overwrite each other — the engine appends them —
    which I re-derived from the engine source rather than trusting the comment.

    **Three things worth knowing, none urgent:**

    * ⚠️ **Two fixes wrap the same colonist function, and which one wins depends
      on the order they are listed in `metadata.lua`.** Right now the order is
      the *safe* one — but by luck, not by design, and nothing anywhere says so.
      If that list is ever reordered, alphabetised, or regenerated, one fix could
      start silently skipping the other. ⛔ I have **not** proven a player can
      actually hit the overlap; that needs a running game.
    * ⚠️ **Two fixes cover slightly less than you'd assume.** The asteroid-habitat
      fix doesn't reach the *Naturalist Habitat* building, and the track-connector
      fix's secondary "let the neighbours reclaim the hex" step doesn't run when a
      **Station** is destroyed — in both cases the game defines its own version of
      the function we patched, so ours is never consulted. ⭐ **Both are "we do
      less than we could", never "we do something wrong",** and the *main*
      track-connector repair does reach stations.

    ✅ **RESOLVED SAME DAY — nothing is owed, and you do not need to answer this.**
    You asked whether the fix was mine or the final audit's. It was mine (links
    1–2 may fix), and asking the question exposed that **my recommendation was
    answering the wrong version of it.** I had priced "pin the order" as *a
    comment in a file that ships* — which is why I said wait. There is a version
    that ships **nothing**: `*/tools/*` is excluded from the package, so a guard
    in `tools/doccheck.py` touches no byte a player receives.

    ⭐ **So it is enforced now, not documented.** `doccheck` fails **red** if
    those two entries are ever reordered, and prints the reason. That is strictly
    better than the comment I was hesitating over: a comment explains the rule to
    whoever happens to read it, and the guard stops the mistake.

    **Proven, not asserted:** I swapped the two entries — doccheck went red and
    exited 1 (so the commit hook blocks it); restored — `metadata.lua` is
    **byte-identical to HEAD** and doccheck is green. `upload_preflight` still
    passes 20/20. ⛔ **Zero shipped files changed**; the release candidate is the
    same bytes it was this morning.

    ⛔ **What link 1 did NOT look at,** so this is not read as a clean bill:
    nothing was run in a game; the two 08-17 core fixes still have not executed
    once; save footprint, uninstall, what a player sees, failure containment,
    packed-vs-unpacked, and any other mod are all untouched — those are lenses
    2–8. The chain has **not** converged; it has finished one lens of eight.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ NEW "ONE MOD FIX ALL": I checked the other community mod against the game's code. Four real bugs we had missed. **One call from you: build them now, or after launch?**


34. ❓ **THE ONLY QUESTION: do these get built before you upload, or after?**
    You said you'd like ours to be *"fully fledged, one mod fix all"*, so I took
    `fredware`'s **SMR Community Fixes** — 15 fixes, 8 of which we already
    cover — and adjudicated the other **seven** against the game's own code. I
    did **not** install their mod (a third mod would have wrecked the baselines
    every gate in this project is measured against); I read a copy of their
    source to find out *where to look*, then reached every verdict myself from
    the shipped game files. **No fix code was written and nothing under `Code/`
    changed.**

    **Four are real bugs we had missed, and are now on the record:**
    * **`C51` — three bits of the interface can never be translated, and the
      translations are sitting right there in the game's own files.** This is
      the strongest one and the only one I could *prove* rather than argue: I
      opened the shipped German language pack and the German text for
      "OVERALL TERRAFORMING PROGRESS" and the rocket's "Back to Earth" button
      **is in there** — the game just never asks for it. Nine languages ship;
      any non-English player sees three English strings in an otherwise
      translated UI. Repairing this loses nothing in any language.
    * **`C52` — the in-game Mod Manager can never show a mod's screenshots.**
      The download loop reads a variable that has gone out of scope one screen
      earlier, so it fails on the first image, every time — and the developers
      left `-- todo: this is not working` in the file twice, directly above it.
      ⚠️ **One piece of this touches your upload:** the thumbnail cache is keyed
      on mod id + version and never re-checks. **If you ever swap a preview
      image after publishing without also bumping the mod version, players who
      already saw it keep the old picture forever.** Nothing to decide — just
      worth knowing before step ④.
    * **`C50` — SpaceY gives +20 Drone Hub command capacity and never says so.**
      It is the only sponsor in the game with a bonus its description hides; the
      other five that have bonuses all describe every one of theirs, three with
      the exact number. ⚠️ The obvious fix is a trap — replacing that text would
      hand eight languages an English description to gain one English line.
    * **`C49` — a soil-overlay bug that is real in the code and unreachable by
      any player.** The function that picks the overlay has a misplaced
      bracket — but the mode it fails to guard has **no button, no keybind and
      no caller anywhere in the game**. Filed honestly as latent. This is the
      third time here that "it's in the source" turned out not to mean "a player
      can hit it".

    **One I rejected**: their *Restore Clustered Lights* blames an assertion
    that lives in the engine's C++, not in any code we can read. I could not
    confirm or refute it, their own module says it is unproven, and their remedy
    changes behaviour rather than repairing a defect. Written up with reasons
    rather than filed.

    **Two we already knew about** (Jumbo Cave `C25`, Lander cargo `C35`).
    ⭐ The Lander one **paid off**: their module named a function ours had not
    followed, I re-checked, and **they were right and our record was
    incomplete** — confirming a payload edit doesn't just disconnect drones, it
    actively interrupts them, and the game's own code contains an assertion
    saying a drone on the ramp must never reach that line. Our entry is
    corrected and strengthened.

    ⇒ **My recommendation, and it is only a recommendation: investigate now
    (done), build after launch.** Adding four to five modules is not a tidy-up —
    each one costs a save-safety pass, a probe, a suite re-measure and three
    store surfaces, which is a release-delaying body of work. Nothing here is a
    release gate and nothing is broken by waiting. **"One mod fixes all" stays
    the direction either way.**
    → `agent/reports/SMRCF_COVERAGE_SWEEP.md`, entries `C49`–`C52`.

    ⭐⭐ **UPDATE, same day — THE CHAINS ARE WRITTEN AND WAITING. Nothing has
    been built and nothing has run.** You asked for chains for everything we can
    fix, simple ones combined, complex ones standalone, and the underground
    cave on its own. That is four chains, 13 prompts, drafted and committed:

    | chain | subject | prompts | **your time** |
    |---|---|---|---|
    | **A** `smrcf-verify` | answers every open question at once, arms two detectors | 2 | **zero** |
    | **B** `smrcf-text` | SpaceY + localization (+ dust devils if A clears it) | 3 | ~15 min |
    | **C** `smrcf-modbrowser` | the mod browser's three defects | 4 | ~15 min |
    | **D** `jumbo-cave` | the underground cave, solo as you asked | 4 | one playthrough segment |

    **A runs first and costs you nothing.** Three of the four currently rest on
    questions nobody has answered — are those dust-devil markers actually on the
    map, does the screenshot downloader exist, can we drive map generation from
    Lua. A settles all of them in one unattended launch, and if the answers come
    back wrong then B, C and D get smaller or disappear. **B, C and D are
    independent of each other and can run in any order.**

    ⭐ Your "stack the deck" idea is written into D as its method, with the one
    line it must not cross: **we turn up the rock density the game's own
    generator reads and let the game place them — we never place a rock
    ourselves**, because then we would only be testing our own placement. And
    the confound you would have hit is pre-registered: at high density rocks can
    block rocks, so when one strands we record what is *around* it. Terrain means
    the bug is real; other rocks means we only proved the consequence.

    ⇒ **Still nothing owed from you except the original question: now or after
    launch?** My answer is unchanged — after. ⛔ And one small thing is owed
    from me either way: **`C49` should be flipped to `wontfix — unreachable`**,
    which is what our own policy says for a defect no player can reach. Say the
    word and it is a one-line change.
    ✅ **RULED AND DONE 2026-08-20 — `C49` is retired `wontfix — unreachable`.**
    The C50/C51/C52 complexity you asked about the same day is measured in
    **item 56**; the "now or after" question here is still open.
    → `agent/prompts/SMRCF_CHAIN_SET.md` has the map and the kickoff lines.

    ⚠️⚠️ **AND ONE THING THAT IS *NOT* POST-LAUNCH — I FOUND STALE TEXT ON THE
    LIVE PAGES WHILE WRITING THESE.** You asked for a checkup of the public
    docs; ten minutes into scoping it, three things were already wrong:
    * **The FAQ contradicts itself about how many fixes are judgment calls** —
      it says *"Six fixes are judgment calls"* in one paragraph and *"Five"*
      fifteen lines later, and five is correct. That is the F85 removal sweep
      missing an instance, and it is on a page a player reads.
    * **"A suite of 95 checks"** appears on the store card **and** in its source
      record. The measured number is **96**. 95 was a prediction we made when
      F85 came out; the real re-measurement came back higher because the farm
      probe landed. This number has now been wrong twice.
    * Assume more survived the same sweep — counts moved on six surfaces at once
      that day.

    ✅✅ **THE CHECKUP RAN 2026-08-16 AND IS CONSUMED** (brief deleted; grave
    `git show <sha>:docs/agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md`). What it
    found beyond the three seeds, all fixed the same sitting:

    * **The removal sweep had missed more than one sentence.** The FAQ's
      balance answer also said *"in three of them the game's code is not
      wrong"* (now **two**), and the **landing page** still said six judgment
      calls (now **five**). Both were player-visible.
    * **A third stale record:** the metadata-strings report still quoted the
      fix-pack blurb saying "Six" as *"as shipped"*, when the live file says
      Five. Corrected, with the miss recorded.
    * **A fourth find, on your launch sheet:** the fix-pack card's body size
      was wrong — the 08-15 re-measure (11,542 characters / 2,011 words)
      never subtracted the deleted distress bullet. Measured today: **11,209 /
      1,957**, by the same method that reproduces the other two cards' cells
      exactly. Smaller, so no character-limit risk moves.
    * **Verified rather than inherited:** the achievements wording is the
      correct "Steam and other PC versions" form on every public surface
      (re-read at the game's own code, not from our records) · the item-29
      notice STRIKE held everywhere · no public page has grown load-order
      advice · the `%AppData%` log path the pages name exists on a real
      machine · both STORE↔RELEASE card pairs re-proven **VERBATIM** by
      actual diff after the edits · all twelve metadata string counts match
      the sheet · `doccheck` and `mkdocs --strict` GREEN.
    * **Readability, since you asked for it explicitly:** read cold as a
      stranger arriving from a store link, the five pages hold — one voice,
      problem-first FAQ order, searchable fix list. That is a judgment, not a
      measurement; no accurate sentence was traded for a smoother one, and
      zero pure-style edits were made.

    ⭐ The preview-image note is now **on the ④ sheet itself** (§0(a)): the mod
    browser caches preview images by mod id **and version only**, so swapping
    a preview after publishing without a version bump leaves everyone who
    already saw it on the old picture. Upload-day image choice is unaffected.

    ⇒ **The pages are ready to upload as they now stand.**


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ NEW (late) — WE MEASURED YOUR OPEN FARM CASE ON YOUR OWN SAVE, AND IT DID NOT REPRODUCE. One sentence from you would explain that.


33. ✅✅ **ANSWERED BY YOU THE SAME EVENING, AT THE KEYBOARD — and then you went
    considerably further than the question.** Your answer was *"nothing but
    normal maintenance, not player build construction ongoing"*, which rules out
    the free-hex transient I had proposed. We then watched your save together and
    **the symptom reproduced**: your Potato farm was **stopped for 52% of the
    session** with its seed buffer hitting a true zero, while your other farm and
    all 36 Forestation Plants never stopped for want of Seeds. *(Audit precision,
    2026-08-15: late in the sitting one Forestation Plant did stop twice — for
    power/malfunction, nothing to do with seeds.)* You typed the banner sighting
    into the log, so for the first time this project can say a player *saw* it
    rather than that a counter fired.

    ⭐ **And you found the thing underneath it, which none of my instruments
    would have caught.** You noticed drones fetching single seed crates out of the
    landscape while a full 4,000 depot stood beside the farm, and guessed there
    was "a hidden rate at which vegetation offers seeds". There is — it is called
    `seed_cooldowns`, and grown plants offer their seeds to your drones through an
    invisible requester object. **That requester gets no distance penalty at all**,
    while the one comparable scattered source in the game was deliberately given a
    50% penalty by the developers. So on your carpeted map, hundreds of one-plant
    trickles compete with your depot on equal footing. You also explained why one
    farm is always silent — it sits in sparser ground with less drone-extender
    coverage, so its drones fall back on the depot.

    ⇒ **Filed as `C48`, credited to you, and it may be the real defect** — in
    which case enlarging the farm's buffer would only have hidden it. ⛔ **No fix
    will be built for either case until `C48` is measured**, which is a
    zero-cost unattended run I have already built the instrument for.
    → `agent/bugs/C48.md`, and the original question is kept below.

    ℹ️ **Update, 2026-08-15 late (the test you authorized — no decision owed):**
    the intervention ran. We applied the developers' own 50% distance penalty to
    every vegetation seed offer on a staged copy — all 3,390 of them, provably —
    and **the routing did not change at all**: your farms went right on eating
    280-seed crumbs from the landscape while 12.4 million seeds sat in storage.
    So the "just add the missing brake" fix is dead — on a map as green as
    yours, distance isn't why drones choose the landscape. The cause sits
    deeper (in the engine's own supply pairing, which modding can't read), the
    trickle costs you drone efficiency but never starved a farm in any
    unattended window, and the seeds-only "top-up" idea parked in the opt-in
    mod is now the one remedy still standing. Nothing is built; nothing new is
    owed from you. → `agent/bugs/C48.md` (the full readings).

    ⭐⭐ **CASE CLOSED — mechanism proven, 2026-08-16 (your go, your controls):**
    we put a log on the exact spot where every drone receives its assignment
    and watched **985 real decisions** on your own colony. For seeds, the
    matchmaker picked the landscape over storage **479 times out of 479** — and
    in **399** of those, a *full, available* depot sat **closer to the drone**
    and lost anyway (one drone flew 7× past a stocked depot for a single bush).
    Your reading was right on every count: **storage depots are a hard last
    resort** — the network only touches them when no loose source exists, which
    for food happens constantly (so your diners get bulk deliveries and never
    starve — we measured one draining ~48,000/sol and keeping up fine) but for
    seeds on a terraformed map happens *never*, because the bushes never run
    out. Your "desired amount" understanding was also confirmed with data (it
    withholds nothing from consumers), and your depots turn out to *restock
    themselves from bushes* — that's why your seed hoard keeps growing. **This
    is deliberate engine machinery with a cost the designers never priced on a
    terraformed map. Whether that's a bug or a design cost is your ruling to
    make, whenever you want to make it — nothing ships either way, and the
    top-up ("gleaner") idea in the opt-in mod remains the remedy that fixes
    the waste without touching the choice.** → `agent/bugs/C48.md`.

    ✅✅ **AND YOU CLOSED THE LAST LOOSE END THE SAME EVENING, 2026-08-16 —
    nothing owed, recorded here because it is your call and it kills an option
    nobody should reach for again.** Your words: *"I don't think a buffer will
    fix it because they don't fill the current buffer as of now"* and *"we can
    retire that for the bug fix mod, and leave it solely for the opt in mod."*
    ⇒ **The "just give the farm a bigger seed buffer" fix is dead**, and it was
    the cheapest-looking one on the list. You are right and our own numbers say
    so: the farm never fills the 5000 it already has, because every delivery is
    one bush's 280 seeds against a drone that can carry 3000. Raising the
    ceiling to 10000 would leave a bigger buffer sitting at 400. ⇒ **The old
    warning "don't fix C47 until C48 is measured, a bigger buffer would hide
    it" is retired with it** — a buffer that never fills can't hide anything.
    ⇒ The whole farm family is now **solely the opt-in mod's**, the buffer shape
    is struck there too so the gleaner work can't inherit it, and the fix pack
    keeps only the records and the probe. Nothing is built, nothing is owed.
    → `agent/bugs/C47.md` (shapes section), opt-in
    `agent/reports/SEED_LOGISTICS_HANDOFF.md` §2.

    ~~**When you saw the endless "waiting for Seeds" popups — had you just done
    something to those farms?**~~

    **Why it is the only thing left to ask.** We ran your save `C47FARM` seven
    times unattended tonight (your cost: zero) and watched both of your Open
    Farms for 15 in-game hours — about 51 planting ticks. **The sampled buffer
    never once read empty** *(the sitting later proved it did touch zero
    briefly — 2, 0 and 4 times across the runs — between our polls; the point
    that this is nothing like what you saw still stands)*. The Potato farm's
    lowest reading was 305 of 5000; the
    other farm's was 1661, and that one never raised a single "not working"
    event in any run. The Potato farm raised 2, then 0, then 4. That is nothing
    like what you saw.

    **We also found out why, and it is a real correction to our own filing.** We
    had assumed a farm plants 3–5 hexes every tick and pays for all of them. It
    doesn't: it only pays when it finds an EMPTY hex, or one growing the wrong
    crop. Your farms are fully planted, so they averaged **2.2 hexes a tick and
    spent nothing at all on about a quarter of the ticks** — roughly 40% of what
    we told you. Which means the drain we described is real but it is the rate a
    farm hits when it has hexes to fill: right after you build it, enlarge it,
    change its crops (every existing hex becomes "wrong" at once), or after a
    wither. **A terraforming speed-run is when a player does all of those.**

    ⇒ If the answer is "yes, I'd just been fiddling with them", the case is
    explained and we can talk about whether it is worth repairing. If the answer
    is "no, they were untouched", then something we have not found yet is going
    on, and it is worth another look.
    ⛔ **Nothing is built, nothing is decided, and no repair is proposed** — this
    is still a candidate, not a confirmed defect.
    → full readings, every prediction and how it fared, and the three defects we
    found in our own instruments: `agent/bugs/C47.md`.

**Two smaller things worth knowing, neither needing a decision:**

* **Your drones carry 3 loads, not 1** (the Drone carry capacity dial in Mod
  Options, set to +2). So a Seeds trip is 3000, not the 1000 we quoted you. It
  makes your observation more striking, not less.
* **That save cannot be run past Sol 385 by an agent.** At the sol boundary the
  game opens a popup, which pauses the clock, and with nobody at the keyboard it
  stays paused forever. It is normal game behaviour; it just caps how far any
  unattended run of ours can get on that colony.

<details><summary>The original source answer, from earlier the same day — kept because the two numbers in it are still exactly right</summary>

ℹ️ **No decision was owed on this part** — it is your rider, recorded so your own
testing has something to argue with. You asked two questions and for a
comparison; all three are answered at source, on the pinned build.

* **Is the storage right?** ⛔ **It was never set.** `OpenFarm.lua` has no
  `consumption_max_storage` line at all, so it takes the editor default of
  **5** — which is the `0/5` on your screen.
* **Is the consumption right?** ⭐ **The consumption is the half that WAS
  deliberately tuned**, which is what makes the pair look wrong. Open Farm
  overrides its planting interval from the class default **2.0 in-game hours to
  0.3** (a 6.7× speed-up), plants **3–5 hexes every tick**, and at **Potato**
  each hex costs **600** — so a single tick can cost **3000 against a 5000
  buffer**. It can never bank two ticks, and a drone only carries **1000** per
  trip. That is why a full depot and 24 idle drones do not help.
* **The comparison you asked for, and it is decisive.** The only other Seeds
  consumer and only other plant-building, **`ForestationPlant`, SETS its storage
  to 10000 explicitly, keeps the 2.0 h tick, and plants ONE hex** (two under the
  Forestation Effort law). Runway on a full buffer: **~40 in-game hours for
  Forestation vs ~0.5 for the Open Farm — about 80×.** Even your cheapest crop
  (Cover Crops) only buys ~3 hours.
* **Across the whole game:** 287 templates, 29 consumers. Ten leave the storage
  at default — but ⭐ **Open Farm is the only one of those that also tuned its
  consumption cadence.** Everyone who made a building drink faster also made
  the cup bigger. One half of a paired change, the same shape as `C39`.

⛔ **What I am NOT claiming.** No code comment ties the two fields, so this is
an *unset field*, not the self-contradiction `C39` was — "farms are meant to be
supply-hungry" is a defensible reading, and the popup is the game correctly
reporting a genuinely empty buffer. And **nobody has measured it in game** —
your observation is the only runtime evidence. So it is filed as a candidate,
not a defect, and **nothing is built**.
→ full derivation, every citation, and three unranked repair shapes (size the
buffer · debounce the notification only · document and do nothing):
`agent/bugs/C47.md`.

⚠️ **Superseded the same night by the measurement above, in two places:** the
"3–5 hexes every tick" and the runway figures that follow from it describe a
farm with hexes to fill, not a planted one; and the "80×" comparison is a
template ratio, which the run could not turn into a measured multiple because
the control never flapped at all. The two template numbers — the buffer that was
never set and the cadence that was — are confirmed in the running game and a
permanent check now re-tests them on every run.

</details>


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⛔⛔ NEW (later) — pricing your "quick playtest?" question found that the F85 dialog CANNOT BE OPENED IN THE GAME AT ALL, and two player-facing pages describe it as if you had seen it


31. ✅✅ **RULED 2026-08-15 — REMOVE IT, BUT KEEP IT RE-APPLIABLE. DONE THE SAME
    DAY, ACROSS EVERY SURFACE.** Your words: *"I think we remove it but document
    it, so we can easily re apply it as a fix, if something ever player facing
    comes out we already know how to fix it."*
    ⭐ **The shelf record is `agent/reports/SHELVED_F85_DISTRESS_PAUSE.md`** — it
    carries the module and its probe **verbatim** (byte-compared before the
    originals were deleted), the trigger that would make them worth shipping
    again, a 30-second source check that answers that trigger, a six-step
    re-apply checklist, and a table of everything already proven so none of it
    is ever redone. ⛔ Deliberately NOT "it's in git history" — that is the
    hand-wave the file exists to prevent.
    **What moved:** module deleted (and its row pulled from `metadata.lua`'s
    file list — that one would have broken the mod); probe deleted; this entry
    → `wontfix`; the judgment bullet gone from the card and the whole entry gone
    from the site fix list; the judgment-call count five→six→**five** again in
    all six places it appears; suite **96 → 95**; modules **76 → 75**. doccheck
    GREEN, `mkdocs build --strict` GREEN.
    ⇒ ✅ **Item 5 closes with it** — `P3` / LATENT / tier U is exactly right for a
    defect that is real, reproduced and unreachable.
    ⛔ **One number is PREDICTED, not measured, and I will not quote it as a
    reading:** the suite baseline should become `79/0/16/0 of 95` and the gate
    `75/75`. No launch has run since the removal — the next unattended leg
    measures it. Nothing is owed by you either way.
    *The question as it stood, kept for the record:*
    ~~The distress-call dialog is dead-coded out of the shipped game. The fix
    is fine; the two places that describe it to players are not.~~
    **How this surfaced:** you asked whether I was proposing a quick playtest for
    F85. Pricing that meant working out how anyone *raises* that dialog — a route
    nobody had ever checked, because the record simply said "open it from the
    console". The answer is that **nothing can raise it**.
    **What the game's own code says**, re-read at Src today and traced
    exhaustively: the dialog has exactly **one** caller in the entire tree — the
    `DISTRESS CALL` button on the rival-colony action bar — and that button sits
    inside a condition the shipped executable compiles to the literal
    `local cond = false / if cond then …`. The button is never built. Every other
    piece of the feature (the cooldown, the "allowed?" check, the resource
    request) is used by that dead button and nothing else. **The developers
    switched the whole feature off and left the code in place.**
    ⚠️ **This is the second time in this one entry.** The same shape retired the
    Quick Save route on 08-11 (`idQuickSave` compiled out behind
    `Platform.cheats`). You are the one who forced that check, against a
    confident source citation, and you were right then too.
    ⇒ **NO, there is no playtest to propose** — see item 5 for the whole answer.
    ⇒ **The fix still ships and is not touched.** It is a wrapper that pauses any
    popup declaring itself non-pausing; it is measured idempotent, measured not
    to disturb popups that already pause, and it no-ops if the flag ever
    disappears. On this game version it has **no live symptom** — it is a defence
    of the rule ("no save lands inside an open popup"), not a repair of something
    you could ever hit.
    ⛔ **What is actually wrong is the writing, on two surfaces**, and it is the
    same class as item 29 which you ruled STRIKE — a claim about what a player
    *sees*, resting on a mechanism that is real in source and absent from the
    retail screen:
    * the **store card** (`RELEASE_DESCRIPTION_FIXPACK.md`): *"every other popup
      window pauses the game while it is open; the confirmation for broadcasting
      a distress call deliberately did not"* — present tense, about a window no
      player can open.
    * the **site fix list** — worse: its entry opens **"What you saw:"** and then
      describes the clock running behind a window nobody can raise.

    ⭐⭐ **AND YOU IMMEDIATELY ASKED THE BIGGER QUESTION, WHICH I SHOULD HAVE
    ASKED FIRST:** *"if that is a button not built, and not something a player
    can ever get to — why are we building a fix for it?"* **I do not have a good
    answer, and I now think we should not be.** The question is no longer how to
    word the description; it is whether the module ships at all.

    **The case against keeping it, which I find decisive:**
    * ⛔ **It repairs nothing.** This repo's own premise (CLAUDE.md) is that
      *every fix repairs a verified defect in the game's shipped Lua*. On
      1.0.7.396349 no reachable popup sets the flag, so the branch that does the
      work **can never execute**. It is not a small fix; it is a dead one.
    * ⛔ **It is not free — it sits in a hot path.** The wrapper patches
      `PopupNotification:Init`, so it runs for **every popup the player ever
      sees**, forever, to evaluate a condition that is provably false. Zero
      benefit, non-zero surface. That trade is the wrong way round.
    * ⛔ **It overrides a deliberate developer choice to no effect.** We
      disclosed it as a design-judgment tweak precisely because the game's code
      is not wrong. Overriding a dev decision to fix something reachable is a
      judgment call; overriding it to fix nothing is just noise in the tree.
    * ⛔ **The one case where it CAN fire is arguably a harm.** Its own
      disclosure says so: *"a popup created by a future patch — or by another
      mod — that sets `dont_pause` would also be paused by this module."* Since
      no vanilla popup can reach it, **the only live scenario left is us
      silently overriding another modder's deliberate choice.**
    * ⛔ **This entry's own rule already prescribed the answer.** F85's original
      fork read: route real → owner decision; *"if the binding or save is
      refused, this drops to I/R4 and stays documentation."* Every route is now
      refused. The entry's own discipline says documentation.
    * ⚠️ **And your 08-12 ruling rested on a fact that has since been falsified.**
      You ruled build-it on the basis that *"the distress dialog is the game's
      ONLY non-pausing popup, so pausing it closes this entry's entire reachable
      surface"*. The first half is still true. The unstated half — that the
      surface is **reachable** — is false. Recommending removal is not
      overturning your judgment; it is reporting that the ground under it moved.

    **The case for keeping it**, stated fairly so you are not being nudged: it is
    a cheap class defence, so if a future patch re-enables the distress feature
    or introduces a new non-pausing popup, we are already covered. ⚠️ But that is
    exactly the "perpetual rider" class **you already ruled on** in item 14 —
    things that keep failing to produce their own precondition become
    post-release WATCH items rather than freight. A precondition that *cannot
    occur on the shipped build* is the limit case of that ruling.

    | | what happens | cost |
    |---|---|---|
    | **A. REMOVE the module ← recommendation** | delete `Fix_DistressPopupPause.lua` + its probe; F85 becomes documentation-only (`wontfix`, real defect / no reachable route); card bullet and fix-list entry deleted because there is no fix to describe | counts move 76→75 modules and 96→95 probes, and the suite gate re-baselines — ⭐ **prompt 03 was already re-truing every one of those numbers**, so this is close to free if ruled now. Reversible: if a patch ever revives the feature, the module is one file in git history. |
    | B. Keep it, ship it silently | module stays; card bullet + fix-list entry struck (item 29 treatment) | the fix list would then describe 75 fixes while 76 ship — an undisclosed module, which is its own small dishonesty, and the dead branch stays in every popup's constructor. |
    | C. Keep and describe it honestly | *"a dialog the shipped game no longer uses…"* | ⛔ worst of both: keeps the cost, and spends a player's attention explaining a non-event. |
    | D. Ship exactly as written | nothing changes | ⛔ present-tense false statement on a store page, plus a **"What you saw:"** for something nobody saw. Not recommended. |

    **Recommendation: A — remove it.** ⇒ ⭐ **Ruling A also CLOSES item 5**: with
    no fix, F85 is a documented, reproduced, unreachable defect, which is exactly
    `P3` / LATENT / tier U as already labelled. One word from you settles both.
    → the full derivation, every grep and the generated-file quote:
    `agent/bugs/F85.md` §2026-08-15 (later).
    ℹ️ *(Terminal-audit addendum, same day: the judgment-call COUNT rides this
    ruling too. It was settled at SIX this morning across the card, the
    mod-page blurb, the site FAQ, the landing page and the fix list; under A
    or B it reverts to FIVE on every one of those surfaces, under C it stays
    six. The full surface map is staged, the sweep is minutes. The C39
    disclosure paragraph and the "96 checks" sentence are independent of this
    item — though A also moves "96 checks" to 95 when the probe goes.)*


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW (later) — ④ IS CUT: your launch afternoon reads ONE sheet, and the audit found one more call that comes before any paste


**The release-3 chain is closed** — both cards paste-ready and diff-proven
verbatim to their audited sources, the third card written and gated, the
uninstall story reconciled, the metadata strings applied and counted, the
packaging measured. **When you sit down for launch, read
`agent/reports/RELEASE_PORTAL_PREP.md` top to bottom — it is the whole
afternoon in order** (upload → links → Pages → fill-ins), and it names
everything below in context.

✅✅ **ALL FIVE CALLS RULED 2026-08-14, applied the same day:**
**29** strike → the notice paragraph is deleted from both cards, the rescue
card, the assembly and the site FAQ, with the source records corrected ·
**17** hold off → Save Rescue not published at launch, held as a contingency
for post-release reports; its fill-in marker and the assembly's rescue section
deleted per their defaults · **28** closes with 17 → ship as built ·
**cleanliness sentence** Reading A (the pack alone) → no text change, the
card's deliberate absence stands · **opt-in version** → **1.0.0 applied** in
its `metadata.lua`. ✅ **And the preview art is CHOSEN the same day — C1 for
both mods** (item 24's floor, built as designed Mars backdrops without a game
launch; `agent/reports/preview_art/FINAL_*.png`, both ~40 KB against a 1 MB
limit; alternates kept, vista-swap possible later). ⇒ **④ is fully prepared:
upload two mods with their previews → links → Pages. Nothing waits on a
decision.**
⭐ **Ordering, your word (2026-08-14 evening): the F85 + C39 builds run
FIRST** — "finish the f85 first since its all unattended." The `unattended-3`
chain is authored (`agent/prompts/unattended-3/`, Opus builds → Opus verifies →
Fable audits, including re-truing every card/site count the two new modules
move) and ④ follows its close. Also done on your word the same evening:
**Steam Cloud re-untick recorded** — the 17 strays the hold window restored
(888 MB) are deleted, the save directory re-listed by name at 76 files, and
"gone" claims are legal again (`EF-051`).
✅✅ **2026-08-15: THE `unattended-3` CHAIN IS CLOSED — terminal audit consumed,
folder empty.** Both builds sustained end to end (routes re-derived at source,
the C39 coverage list reproduced by an independent sweep, both launch logs
re-counted line by line), and every count the two modules moved is re-trued on
the cards, the mod-page blurb, the site and the portal sheet. ⛔ **One thing
now stands between you and the ④ paste: item 31 above** — the same-day route
check found the F85 dialog dead-coded, so rule 31 (one word; it also closes
item 5) and the staged minutes-scale sweep trues the last surfaces. C39's
disclosure and everything else on the sheet are ready as written.

29. ✅ **RULED 2026-08-14: STRIKE — and struck the same day on every surface**
    (both cards, the rescue card, the assembly, the site FAQ; trace rows and
    the §10.9(4)/D13 source records corrected so it cannot be re-inherited).
    The question as it stood: both store cards promised an on-screen notice
    the game never shows for our mods. The sentence: *"the first time you load a save that was made with
    any mod you have since removed, the game itself prints a notice that the
    save refers to a mod that is not there."*
    **What the route shows:** the measured evidence behind it is a **log-file
    line** (`Savegame references Mod … which is not present` — engine
    bookkeeping, written to the log only). The one thing the game puts **on
    screen** for missing mods is the "missing or outdated mods" warning, and it
    deliberately skips mods marked *optional* — **which all three of ours are**
    (the same flag that stops the game nagging players who removed the mod,
    set on purpose in all three `metadata.lua` files). A player who removes our
    mods sees **nothing**: no notice, nothing to dismiss, nothing that
    "disappears when you save". The record's "you will see one notice" was an
    inference from rig logs — the rig draws the log on screen; a retail player
    has no such overlay. Nobody has ever watched a retail-shaped load show one.
    **Recommendation: strike it** (or let the for-modders page alone carry the
    accurate log-line version). One agent sweep fixes every surface the same
    way once you rule — cards, rescue card, assembly, site FAQ (site edits are
    FILED, awaiting exactly this ruling). Shipping it as written is the
    harmless direction (players told to expect a notice just never see one),
    but it is a false statement of fact on every card, which is the exact class
    the whole evidence bar exists to keep off a store page.
    → route + evidence: `RELEASE_DESCRIPTION_RESCUE.md` audit section (engine
    cites: `Mod.lua:1199`, `SavegameMetadata.lua:97-99`); `D13_EXPOSED_SET.md`
    §10.9(4) is where the log measurement lives and where the "you will see"
    aside crept in.

ℹ️ **Also fixed by the audit, no call needed:** the rescue tool's instructions
("load once … delete it again") never said to **save** — and the clean pass
only edits the loaded colony; the player's save is what writes it into the
file. Corrected on every editable surface (rescue card, its `metadata.lua`,
the opt-in card's Save Rescue fill-in sentence). ⚠️ The rescue's **on-screen
dialog** has the same omission ("You can remove Save Rescue whenever you like")
— a code string. ✅ With 17 ruled hold-off and 28 closed **ship as built**,
nothing ships with it; ⛔ **if the contingency ever fires, re-open the dialog
text before upload and add the save-step line in the same one-launch
re-witness** (recorded on item 17 and in the rescue card's header).


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW the release descriptions are being written: ONE question, and it is bundled with a call you already owe


28. ⚖️ **The Save Rescue dialog buries the one line it exists to print. Fix the
    code (costs you one launch) or ship it as built (costs nothing)?**
    **Answer this together with item 17** — whether the rescue tool publishes at
    all — because better dialog text is only worth anything if a player ever
    sees it. If the tool does not publish, this is already answered: ship as
    built, and say so and I strike the line.
    **What you saw at the sitting**, reconstructed exactly from the counts in
    your own dialog:
    > Removed: 1 rain loop stamp · 1533 reservation timestamps · **2 drone stat
    > dials** · 22 dome flags · 4 building flags · 4 rocket payload flags

    The tool exists for the **drone dials** — they are the one leftover that
    keeps changing your game after you uninstall; everything else on that line
    is inert. It printed **third of six**, with no explanation, next to 1533
    timestamps. That is not a design choice: the groups are sorted as *text*, so
    they line up by the digits of their counts, and the drone line lands wherever
    its "2" happens to sort.
    **What the fix would look like:**
    > Removed: **2 drone stat dials (drone speed and carry capacity are back to
    > the game's own values)** · 1 rain loop stamp · 4 building flags · …

    **What it costs you:** the changed text has never been on a screen, and the
    only instrument that can ever check a dialog is your eyes — no log records
    one. The gloss also makes that line much longer on a dialog built for a
    gamepad, and whether it wraps badly is exactly the thing a log cannot tell
    us. So: I re-stage the save (my time, but note it is the copy-an-autosave
    hazard again, so it is not free of risk to *your* saves), you take **one
    launch, one Mod-Manager visit, and about five minutes** reading one dialog.
    **My recommendation: decide item 17 first.** Publishing → do the fix, it is
    the tool's entire user interface and it is currently unreadable at the one
    place it matters. Not publishing → ship as built.
    ℹ️ **Nothing is blocked either way.** The descriptions being written now do
    not quote the dialog; they say in plain words, on the page you read *before*
    installing, that a non-base drone speed/carry dial keeps working forever
    after uninstall. And your `tested` verdict on the rescue tool is untouched —
    it was granted against the text the build really prints, which is still
    exactly what it prints. → `agent/reports/D13_EXPOSED_SET.md` §10.5's
    correction block (three more mismatches found there, all cosmetic bar this
    one), `agent/bugs/D13.md`.
    ℹ️ **Your launch-day sheet exists:** `agent/reports/RELEASE_PORTAL_PREP.md`.
    The full ④ picture — the five calls in order, the preview-art blocker, and
    one more audit finding that touches this item's "fix the dialog" branch —
    is the **④ IS CUT** block above this one.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW the SITE is built (unpublished): one small question, and two things for your awareness


ℹ️ **2026-08-14 — the site chain is CLOSED; nothing here is owed by you.** The
terminal audit read all five pages and both store cards as a player, re-ran the
"which shipped module delivers this?" control firewalled from the ledger
(**clean — no new false claim**), re-verified the exposure gate and that both
issue trackers are really open, and applied the one correction routed to it:
the store card's patch-retirement sentence is narrowed to its accurate
shape-of-the-code version, under your 22d item-1 approval. Still nothing on the
web; publishing remains yours. Open decisions stay at 3.
*(Superseded the same day: the release-description chain added **item 28**
above, so open decisions became **4** — its terminal audit added **item 29**
for **5** — and the owner then ruled all five release calls in one sitting
(29 strike · 17 hold-off · 28 ship-as-built · cleanliness A · opt-in 1.0), so
open decisions are back to the **3** standing non-release items.)*

27. ~~⚖️ **WHERE DOES A BUG REPORT GO?**~~ ✅ **DECIDED 2026-08-13, same session:
    BOTH, COMMENTS NAMED FIRST — and it is written into the site already**
    (`content/faq.md` → "Where do I tell you?"). The mod page's comments are the
    main route, read first, needing no account a player does not already have
    and working on every platform; the project's issue tracker is named once,
    for the reporter who has a **save file or a log**, because a comment section
    cannot carry either. One tracker covers both mods. ⚠️ **What you took on:**
    a tracker is a place you have said you will look — issues are open on both
    mod repos (verified live). ⛔ The store-page link is still a hole until you
    upload. ℹ️ Offered, not built: a short issue form that asks for platform,
    when it started, whether it survives a save and reload, and the save — say
    the word and it is ten minutes of agent time.
    ℹ️ **Awareness, no decision owed — the frozen description has TWO MORE false
    claims than the four on record, and both are the `F76` shape.** Writing the
    fix list meant asking, for each of its bullets, *which shipped module
    delivers this?* — and two had no module at all: the **dome-plumbing**
    bullet describes `F24` and the **research-counter** bullet describes `F28`,
    both closed `wontfix` on 2026-07-30 with their code files deleted. Neither
    ever reached a store card. ⛔ They are recorded in
    `agent/reports/SITE_BUILD_AUDIT.md` so the release-prep rebuild of that file
    cannot inherit them.
    ℹ️ **Awareness — the Sensor Tower sentence in that same file is backwards,
    and so was the site's own specimen.** It says towers *made meteors worse*;
    the code says the opposite — towers added warning time, warning time WAS the
    interval, so towers accidentally spaced strikes out and the players actually
    hurt were early colonies without them. The site now says the true version.
    Nothing shipped is affected: neither store card mentions Sensor Towers.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ NEW THE SHIP LINE (three rulings, decided in the process-audit review session)


14. ~~**⚖️ Is `fixed` + suite + self-checks enough to ship, or does the
    evidence campaign finish first?**~~ ✅ **DECIDED 2026-08-12, your ruling:
    "I don't want to drop quality, but I think in some ways we are over
    testing… if there are things that we can say 90+% chance this is good, I
    am not sure its worth the added hours."** Three parts, all recorded:
    * **The `fixed`→`tested` evidence campaign is FROZEN until after release.**
      The shipping bar is what already runs mechanically — the automated suite
      (⛔ **RE-MEASURED 2026-08-13** — the suite is now **94** probes and the
      both-mods read is **78 pass / 0 fail / 16 skip / 0 error**, the six extra
      skips being the new Save Rescue probes standing down because that mod is
      not part of your standing rig; with it loaded the same run reads
      **84/0/10/0**. Log `archive/rs_r0_Mars.exe-20260813-11.42.08.log`. The
      88-probe 78/0/10/0 this ruling was made against is the same bar, and the
      pre-split 77/0/10/0-of-87 before that — the only verdict change in the
      whole sequence is the deliberate Mod-Options check split),
      per-fix runtime self-checks, the
      fail-safe registry and per-fix veto, and the completed save-safety tier
      (F86 Tiers 1+2, verified). Keyboard re-witnessing stops being scheduled work;
      it may resume against the released mod if you still want it.
    * **Perpetual riders → post-release WATCH items** (C42, F99, F80, the
      F96 meteor coincidence): each has failed to produce its own precondition
      3+ times; they leave every chain's freight. A symptom appearing in your
      game still takes its tap.
    * **D13 stays BLOCKING, at hours-scale.** You challenged the audit-review
      estimate ("adds a week") and you were right — testing is: build the
      artifact, probe it, uninstall on a big save, run the after-sweep — a few
      hours unless it finds something. The heavy part is agent-side (the
      authoritative exposed-set derivation + the curated keep/remove list —
      some residue IS the repair and must survive). ⚠️ One design question is
      yours at spec time, deliberately reserved on the entry: what the player
      DOES with the artifact (run-after-removal / keep-installed /
      pack-is-own-cleaner). The spec session asks it; nothing owed before then.
    **What this buys: the release front is now the only main line** — D13
    chain + `unattended-3` in parallel (agent), then ONE combined sitting
    (PT-20 redo + D13 verify + the F102 minute), then MOD_DESCRIPTION +
    disposition table (agent), then your ~1–2 h of launch tasks. → the review
    that prompted this: your process-audit artifact + `agent/reports/`
    replies, SESSION_LOG 2026-08-12.

15. ✅ **DECIDED 2026-08-12, your order: the 8 opt-in modules split into a
    STANDALONE opt-in mod** (ClassicRockets, AcknowledgedWarnings,
    ResidencyControl, MultipleSuns, DroneOverhaul, CohortHousing, NoHomeless,
    DroneStatDials — the `optional = true` files). **Sequenced BEFORE D13, by
    D13's own rule:** the cleaner's exposed-set derivation must see the FINAL
    module sets, or it gets done twice. What the split chain owns: map the
    shared-framework coupling first (registry, logging, Mod Options bridge —
    the standalone mod needs its own slim copy or a deliberate dependency);
    move the files + their probes; re-derive every baseline the split resets
    (gate reads 81/81 → main + opt-in pairs, suite tally, doccheck counts).
    ⚠️ Scope you accepted with it: a second mod = its own metadata,
    description, preview image and portal pass at launch, and the D13 rescue
    artifact covers residue from BOTH mods (one artifact — spec-time detail).
    Nothing owed by you until its verification lands in the combined sitting.
    ⭐ **CHAIN AUTHORED 2026-08-12, same session, to your sharpened order**
    (*"true standalone… work with or without the bug fix mod… all our hard
    fault work makes it over… cleanly load its folders and just work on it"*):
    `agent/prompts/split-optins/` — design → fresh-context QA gate → build →
    three-cell verification matrix (+ a save-compat witness on a `CP15PT15`
    copy) → terminal audit with a no-retraining acceptance test run from the
    new repo alone. Binding invariants: zero `SMRFixPack` references in the
    standalone; **persisted names keep their exact bytes** (your saves are the
    contract); module behaviour unchanged. Three small calls come back to you
    later, none blocking: the mod's display name (launch prep), whether the 8
    default ON or stay opt-in-OFF in their own mod (design will recommend),
    and a one-minute Mod Options re-tick after the split (new mod id = fresh
    toggle state).
    ⭐ **DESIGN'S RECOMMENDATION IS IN (2026-08-12, chain prompt 1): keep them
    OFF by default — one line from you either way, and the build proceeds with
    OFF unless you say otherwise.** Why: flipping the default is itself a
    behaviour change (outside the chain's scope fence), and three of the eight
    are not things you'd want on unasked — `DroneOverhaul` is labelled
    *experimental* on its own toggle and is frozen pending PT-52,
    `NoHomeless` moves colonists between domes with an unwind that is still
    unverified, and `CohortHousing` re-homes Seniors and Children.
    `ResidencyControl` and `NoHomeless` also each add a row to every Dome
    infopanel. Installing the mod buys the *choice*; the page costs one visit,
    which the re-tick above already asks of you once. ⚠️ Counter-argument,
    recorded so it is your call and not a fait accompli: everyone who installs
    that mod has already opted in once, so a second opt-in per module is
    friction — and if you prefer ON it is two lines per module in
    `items.lua` + `metadata.lua`, **nothing in `Code/`**, so it stays cheap to
    revisit after release. Reasoning: `agent/prompts/split-optins/90_DESIGN.md`
    §3.7.
    ⭐ **Your standing condition, recorded 2026-08-12:** *"Once we get it
    seperated I will keep the opt ins loaded in as they make testing easier."*
    → now a dormant WORKFLOW rule the split's audit activates: both-mods
    -loaded is the rig's NORMAL config; agents expect it, attribute opt-in
    lines instead of flagging them, name a confound only where a reading
    intersects what an opt-in changes, and any leg needing the opt-ins OFF
    declares it in its brief (a Mod-Manager toggle needs a full restart).
    Your ordinary play doubles as the continuous both-mods compatibility
    soak. Nothing owed.
    ⭐⭐ **BUILT 2026-08-12 (chain prompt 3), and ✅✅ VERIFIED THE SAME EVENING
    (prompt 4): the whole matrix is GREEN and it cost you ZERO minutes.**
    ✅ **Your minute is already spent — you did it at 18:30, before the leg ran**
    (enabled the mod, re-ticked the seven toggles and both dials at `5x` / `+2`).
    Nothing further is owed here, and ⭐ **your run turned out to be evidence**:
    it is the only recording that will ever exist of the fresh-default state, and
    it read exactly the predicted `1/8` with all seven modules `inactive`.
    **What the verification proved, in your terms:**
    * **Your saves are fine, and this was tested two different ways.** Four of
      your saves were read back (a copy of `CP15PT15`, a copy of `CP60RT`, a copy
      of `Autosave Sol 311`, and the PT-35 fixture): every dome policy and every
      drone dial the old single-mod pack ever wrote into them is still found, by
      the new mod, under its exact original name. Then the leg *wrote* all three
      policy fields onto 11 domes and 4 buildings, saved, reloaded, and got every
      one of them back on the same objects — **0 of 3 broke**.
    * **The bug-fix pack is untouched.** Across all 88 automated probes the only
      difference from before the split is the one deliberate change (the Mod
      Options check split in two, because there are two pages now). 86 of 86
      shared results are identical.
    * **Both mods work alone and together.** The opt-in mod ran with the fix pack
      completely uninstalled, and the fix pack ran with the opt-in mod completely
      uninstalled, both clean, no errors anywhere.
    ⚠️ Two smaller things the build learned, neither needing a call: the fix
    pack now has **no Mod Options page at all** (it has no options left, so the
    engine correctly stops listing it — do not report it as missing), and the
    display name above is still a PLACEHOLDER awaiting your launch-prep call.
    ⚖️⚖️ **AUDITED AND CLOSED 2026-08-12 (chain prompt 5, terminal audit): every
    matrix verdict re-derived from the archived logs and SUSTAINED.** All nine
    logs byte-compared identical to their originals and read whole; every tally
    recounted from the verdict lines themselves; the standalone claim re-proven
    by my own greps (fix-pack global nil in cell b; zero `SMRFixPack` references
    in the new mod's code); every persisted name re-derived from the shipped
    code and matched to the save readings name-by-name; the junction route
    (EF-055) re-derived from Src leg by leg. Two precision corrections, neither
    touching a verdict: "86 byte-identical rows" means 86 identical VERDICTS
    (5 rows' message text differs benignly — save-state/RNG, one of them
    independently confirming your dial change), and the 18:30 log you produced
    is now archived in the repo (it was load-bearing and only on the rotation).
    ✅ ~~Still yours, none blocking: the display name · the OFF default~~
    **BOTH DECIDED 2026-08-13, your rulings:** display name =
    **"Community Fix Pack: Opt-In Modules"** *(the family prefix was renamed by
    your 2026-08-17 ruling, item 36 — the name is now "Relaunched Fix Pack:
    Opt-In Modules")* (family-prefixed so the two mods
    sort together — swept the same day across all 15 player-visible sites in
    11 files, parse sweep GREEN, pushed `e17586b`; mod id / global / log tag
    unchanged, they are save contract) · **default-OFF RATIFIED** (as built
    and verified; two-line flip stays cheap post-release if you change your
    mind). The re-tick minute is spent; nothing else is owed.
    ✅ ~~whether the new repo gets a GitHub remote~~ **DECIDED 2026-08-13, your
    ruling: PUBLIC, same as the fix pack.** Live at
    `github.com/catt144/SMR-CommunityOptInPack` — all 6 commits pushed, tree
    clean, `git pull` resolves (so the D13 chain's staleness check reads it
    without tripping). ⚠️ **One thing that came out of doing it, and it is not
    caused by it:** your Windows username and SteamID64 were written into the
    public docs of BOTH repos (a hard-coded save-folder path in `EF-050` and
    `PLAYTEST_HELP`), and a SteamID64 resolves to your Steam profile. ✅ **SCRUBBED
    2026-08-13 at your word** — every live doc in both repos now says
    `%USERPROFILE%\Saved Games\Surviving Mars Relaunched\<steam-id>\`, which is
    equally usable. ⛔ **Read the sibling item below before assuming that closed
    it: the string is still in git HISTORY on both public repos.**


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW public documentation: platform decided, one question back to you


21. ✅ **DECIDED 2026-08-13, your ruling: GITHUB PAGES** for the player-facing
    docs site. A working scaffold is committed at `public-site/` (MkDocs +
    Material — the sidebar tree, `Ctrl K` search, right-hand page TOC, dark
    theme and callout boxes you saw on the peer GitBook site). It is **free**
    on a public repo, and everything stays as markdown in the repo, which is
    how you already work.
    ⛔ **Nothing is on the public web.** The build workflow is manual-trigger
    only and Pages is not enabled on the repo, so the site does not exist
    publicly until you choose to turn it on. The four pages in it are marked
    LAYOUT SPECIMENS on their own face — they are there so you can judge the
    feel, not to be published.
    **To look at it, either** (⭐ paths updated for the move — these are the
    live ones, run them from `C:\Dev\SMR-CommunityMods`)**:**
    * **locally** — `python -m pip install mkdocs-material` then
      `python -m mkdocs serve`, open the address it prints; or
    * **live but private-ish** — Settings → Pages → Source: *GitHub Actions*,
      then run *Publish docs site* from the Actions tab. ⚠️ That URL is public
      the moment it builds, so do this only if you are content for specimens to
      be visible for a while.
    ✅✅ **TOPOLOGY DECIDED 2026-08-13, your ruling: ITS OWN REPO — and you
    created it the same evening.** Live at
    `github.com/catt144/SMR-CommunityMods`, public, and the scaffold is already
    moved: local clone `C:\Dev\SMR-CommunityMods`, `mkdocs.yml` and `content/`
    now sit at that repo's root, the manual publish workflow moved with them,
    and both are **gone from the fix pack repo**. ⛔ **Still nothing on the
    public web** — the workflow is still `workflow_dispatch` only and Pages is
    still not enabled; the four pages are still marked layout specimens.
    ⭐ **Two things fixed on the way in, and one deliberately left broken:** the
    sibling mod's decided display name replaced the dead working title, and this
    page stopped claiming that name was unchosen. ⛔ The line about whether an
    opt-in toggle needs a restart is now labelled *do not publish* rather than
    guessed at — two of our own documents claim it both ways and neither has
    been checked against the code. The `public-docs` chain settles it.
    **Nothing further owed by you here.** ~~The ask as it stood:~~
    ⚖️ ~~**THE ONE THING BACK TO YOU: which repo should host the site?**~~
    * **Its own repo** (e.g. `SMR-CommunityMods`) ← **my recommendation.** One
      site covering both mods and the rescue tool later, a neutral URL, and
      nothing ships inside either mod. It is also how the peer site works —
      "Dash's Vault" is one site with a mod tree under it. Costs you the same
      15 seconds as the last repo; the scaffold was built to move in one command.
    * **Leave it in the fix pack repo.** No new repo, but this repo *is* the mod
      (the game's Mods folder is a junction into it), so the site rides along
      inside the fix pack, and the URL would read `…/SMR-CommunityFixPack/` for
      a site that also documents the opt-in pack.
    Nothing is blocked on this — the `public-docs` chain can start either way.
    ⭐ **UPDATE 2026-08-13 (the chain's design prompt ran): the recommendation
    is unchanged but the argument got harder.** I checked whether extra folders
    in this repo actually reach the file players download — see item 23 — and
    they do. So "leave it in the fix pack repo" now also means "remember to
    keep the site out of the upload, forever"; its own repo makes that
    impossible to forget. Still your call, still 15 seconds either way.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⚖️ NEW your Steam ID is scrubbed from the live docs, but NOT from git history


20. ✅ **DECIDED 2026-08-13, your ruling: LEAVE IT.** No history rewrite, ever,
    unless you re-open this: the ID is already on your public Steam profile,
    the live docs are scrubbed so it spreads no further, and every sha
    citation in three repos stays valid. CLOSED — nothing is scheduled and
    nothing rides prompt 5. The ask as it stood:
    ⚖️ **Do we rewrite the public repos' history to remove your SteamID64, or
    leave it?** The live files are clean as of today; the string is still in the
    commits behind them, and GitHub serves those to anyone.
    **Measured, both public repos:** fix pack **104 of 828 commits**, across 9
    files — `PLAYTEST_HELP`, `PLAYTEST_CHECKLIST`, `EF-050`, and six consumed
    prompt/spec docs (`corun-pt15`, `corun-pt60` ×2, `corun-rig`,
    `split-optins` ×2). Opt-in repo **7 of 7 commits**, one file (`EF-050`,
    which arrived by the whole-facts-folder copy at the split). The TestKit is
    clean and has no remote anyway.
    **What removing it costs, and this is the real reason it is your call:**
    it means `git filter-repo` + a force-push, which **rewrites every sha in
    both repos**. This project cites shas constantly — `90_DERIVATION.md:11`
    pins the D13 derivation to fix-pack `155869a` / opt-pack `a90d128` /
    TestKit `62f03da`; SESSION_LOG and the archived records cite dozens more;
    several docs tell a future session to run `git show <sha>:<path>` to
    recover a consumed prompt. **Every one of those pointers would break**, and
    the D13 chain is mid-flight right now.
    **The three ways out:**
    * **Leave it.** Costs nothing, breaks nothing. A SteamID64 is not a secret
      in the way a token is — it is on your public Steam profile already; what
      it adds is a link between this GitHub account and that profile.
    * **Rewrite after D13 ships**, when no chain is mid-flight and the sha
      citations can be re-pinned in the same pass. Cheapest safe version.
    * **Rewrite now** — I would not recommend it while D13 is live.
    ⚠️ Whichever you pick, the scrub already done stops it spreading further.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⛔ NEW I DELETED ONE OF YOUR AUTOSAVES. Telling you straight.


16. ⛔ **`Autosave Sol 306` is gone and I cannot get it back. `Autosave Sol 311`
    is fine — I restored it byte-for-byte.** No decision is owed; this is a
    report, and the only thing you might want to do is check whether Steam Cloud
    puts `Sol 306` back next time you launch (cloud is still ON).
    **What happened.** The verification leg loaded *copies* of `CP60RT` and
    `Autosave Sol 311` to read your dome policies back off real saves. Copies are
    the rule precisely so your originals are never touched — and the originals
    weren't. But a copy of your campaign **is still your campaign**, so the
    game's own autosave timer kept running, wrote a fresh `Autosave Sol 311(2)`,
    and its rotation then deleted the older autosaves to stay under your autosave
    count. That is vanilla behaviour (`Savegame.lua:1484-1528`), triggered by me.
    **`Sol 311` survived only by luck** — the leg happened to be holding a byte
    copy of it as a witness, so I put it back with its exact bytes and its
    original timestamp. `Sol 306` was never copied, so there is nothing to
    restore from.
    **What stops it recurring:** recorded as `agent/facts/EF-056` — any future
    leg that loads a copy of a real campaign must byte-copy every autosave first
    and list them by name at close-out. "Use a designated copy" protected the
    file; it did not protect the folder, and nothing in the rules had noticed
    that gap before tonight.
    ⚖️ **Audit check, 2026-08-12 evening: `Sol 306` has NOT come back** — the
    save folder re-listed by name during the terminal audit; 79 `.sav`, no
    `Autosave Sol 306`, `Autosave Sol 311` still byte-exact (MD5 re-read), the
    leg's own `Autosave Sol 311(2)` still present (inventoried for the
    post-untick cleanup). The Steam-Cloud check at your next launch stays live.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW asteroid Exotic-Minerals freeze (decided in-session; one owed minute)


11. ✅✅ **DONE 2026-08-14 — THE OWED MINUTE IS PAID, nothing further owed by you.**
    Moment C of the combined sitting. ⛔ Two things the item had wrong and you
    would have hit at the keyboard: **there is no save called `Sylmacaink BH25`**
    (all 88 read at their headers) and your campaign's asteroid carries **ONE**
    deposit sign, not three. The rig switched maps and selected it for you.
    **Your verdict: the sign RENDERS and is SELECTABLE** — it opened
    `Underground Exotic Minerals · 14,935/14,935 · Grade: Very high`, whose number
    is the log's `amount=14935000` read a second way. Log side: `ExoticDepositSign
    [active]`, `1 … re-signed onto the clean entity`, 0 `[LUA ERROR]`.
    ⭐ **One already-placed deposit beat three spawned ones**: it exercised the
    `OnMsg.LoadGame` sweep that the 2026-08-12 console-spawn leg never touched.
    ⭐⭐ **And moment A threw in a free measurement**: with both packs disabled the
    same deposit reverted to the vanilla sign with zero re-sign lines, so
    "uninstall is clean" stops being a source argument and becomes a reading.
    ⛔ **The CURE is still unverified and still ships disclaimered** — that has not
    moved and only a Linux/NVIDIA player's report moves it. → `agent/bugs/F102.md`.
    *The original item, for the record:*
    ~~**⚖️ `F102` — the community-witnessed asteroid freeze (Linux/NVIDIA):
    ship our entity-retarget fix without being able to verify the cure?**~~
    ✅ **DECIDED 2026-08-12, your ruling in-session: "Lets do option 3, its the
    easiest and safest, and we will just disclaimer it."** Built the same day:
    `Code/Fix_ExoticDepositSign.lua` re-signs subsurface Exotic Minerals
    deposits onto the remaster's own orphaned sign asset; gameplay untouched;
    safety verified (both sign entities ship in vanilla, saves carry nothing
    of ours, harmless if the freeze lives elsewhere). Your two test legs
    (Windows rig + Steam Deck, both clean) established the freeze is
    configuration-gated to hardware we don't own — the disclaimer text for the
    mod page is drafted in the entry, ready for launch prep (MOD_DESCRIPTION
    stays frozen till then). The outreach alternative (asking the community
    mod's author to test on a freezing save) stays available any time you want
    the cure confirmed. → `agent/bugs/F102.md`.
    **Owed: one minute, next time you're in game with the pack updated** —
    load the D-type asteroid save (`Sylmacaink BH25`), eyeball the three
    crystal deposit signs: new art renders, deposits still selectable, and
    `SMRFixPack.ListFixes()` shows `ExoticDepositSign [active]`. That closes
    the local (safety) half; the entry then waits only on witness-class
    reports.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW raised by you mid-sitting during `corun-pt60`


**Cost, stated honestly: the brief promised ~40–60 attended minutes and the
sitting took about 95** (13:38 launch → 15:15 quit). **Roughly 45 of those
minutes were your own three challenges and two staged attempts, and every one of
them changed the record** — the trains question became item 12 below, and your two
F34 challenges (the rocket's reserved pad zone, then transports) rewrote that
fix's route documentation from three wrong claims to one correct route. That is
not overrun and is not scored against you. **Ours is about 10 minutes:** the
brief's console order could not be run as written (it assumed a console at the
main menu), and I compounded it by concluding main-menu input didn't work at all
— the log shows it *did* execute and simply never echoed to the screen, so the
extra load I asked you for was avoidable. The measurement legs themselves ran to
budget. ⭐ **What your minutes bought: the P8 decider, which was unrepeatable —
it needed a save written before 2026-08-02, and `USA Sol 302` was the only one.**

12. ~~**⚖️ TRAINS — do the remaining train items get any more of your attended
    time, or do we stop?**~~ ✅ **DECIDED 2026-08-12 — OPTION A: the train
    group ships at `fixed`; the verification queue is CLOSED.** F21 stays
    `fixed` (its restamp was already witnessed organically 08-10), F64 ships
    on the family-witnessed evidence, F11/F48/F91 were at their honest ceiling
    regardless (`agent/reports/TRAIN_SHIP_READY_ROUTE.md`). F80's tap survives
    ONLY as a symptom-triggered watch — no chain may schedule a train leg
    again. ⭐ One correction in your favor found during the audit review: F65
    and F66 (station↔tunnel grid + connector) are ALSO train-group entries and
    both are already `tested` — the group was more keyboard-verified than the
    inventory below said. The original question and record, kept for the
    reasoning:
    Your words, spoken during the PT-60 sitting and
    recorded here rather than only in an agent doc: *"I feel like I have been
    working on trains since day one of this mod and we still aren't done trying
    to fix and verify trains."* **That is a fair reading of the record, and here
    is the record so the call is yours on facts, not on mood.** Fifteen entries
    in `agent/bugs/` are train/track/platform defects — **`tested` (4):** F44,
    F45, F46, F47 · **`fixed`, never owner-witnessed as `tested` (5):** F11,
    F21, F48, F64, F91 · **`fixed*` (1):** F49 · **`wontfix` (2):** F62, F79 ·
    **still open (3):** F80 `investigating`, F99 `filed`, C45 `filed`. Four of
    the checklist's own test legs are train legs. **What that inventory says:
    the train FIXES are done — twelve of fifteen are built or deliberately
    written off, and nothing on the list is waiting on a train repair.** What
    keeps trains coming back to you is **verification**, not fixing: F21's
    re-earn rider, F80's symptom-triggered tap, and the two `filed` items that
    are rate questions. ⚠️ **F80 is the one that would genuinely cost you** —
    it can only be taken WHEN the symptom appears in your own game, and its
    entry says tapping must happen before you mitigate. **Your call, and any of
    these is a legitimate answer:** (a) close the train verification queue —
    F21 stays `fixed` forever, F80 stays `investigating`, and no future chain
    proposes a train leg; (b) keep only F80's opportunistic tap, drop the rest;
    (c) keep the queue as it stands. This sitting declined F21's rider on its
    own (no instrument in the armed harness) and **nothing here is blocked on
    your answer** — it decides what future chains are allowed to ask you for.
    → the sitting's own record lands in `agent/reports/` at close-out.
    ⭐⭐ **YOUR EXPLICIT ASK, 2026-08-12 — an AGENDA ITEM for the PT-60 audit,
    not a note.** You want the audit session to work out **a route that moves
    the train items into the ready-to-ship column**, instead of every chain
    re-proposing a train leg. ⚠️ **Two corrections the audit must carry into
    that discussion, because they change the question being asked:** (1)
    **nothing train-related blocks the release today** — F21 already ships as
    `fixed` and PT-62's remainder is explicitly NOT a release gate, so this is
    a question about what STANDARD you want (is `fixed` enough to ship, or do
    you want owner-witnessed `tested` on the train fixes before launch?), not
    about unfinished repairs; (2) **C42 is NOT a train item** — it is
    `PassageBase:TraverseTunnel` (dome passages), and it sat beside F21 in this
    sitting's skip list only because both fail for the same reason, a missing
    instrument in the armed harness. ⛔ **The audit does not get to answer the
    standard question itself.** What it owes you is a COSTED ROUTE per
    remaining train item — which instrument each read needs, whether it can
    ever be organic or is forced-only, and what it would cost you in attended
    minutes — so that the ship/no-ship standard becomes one decision in one
    sitting instead of a recurring ask.
    ✅ **ROUTE DELIVERED 2026-08-12 — `agent/reports/TRAIN_SHIP_READY_ROUTE.md`
    (the PT-60 audit).** The one-paragraph version: **three of the five
    unwitnessed `fixed` items (F11, F48, F91) cannot honestly be upgraded by
    any leg at any price** — their guarded states have no organic producer, so
    `fixed` on mechanism evidence is their ceiling and the report says why per
    item. **The two that CAN be bought are F21 (~10–15 min) and F64
    (~5–10 min), together one ~20–30 min rider block on any co-run that stages
    `TEST2H TRAIN`** — the natural host is the PT-20 redo already in the
    queue. F80/F99/C45 stay watch-only (zero scheduled minutes). **So the
    standard question collapses to one decision: ship the train group at
    `fixed` (option A, 0 minutes) or buy the F21+F64 block first (option B,
    one rider block).** Either answer closes the queue; nothing re-proposes
    afterwards.

13. ~~**⚖️ Are cheats on a playtest save a confound that needs defending every
    time?**~~ ✅ **DECIDED 2026-08-12, your ruling mid-sitting — NO, they are
    the normal condition and there is now a standing rule.** Your words:
    *"We really need a standing rule that these saves are play testing saves
    with colonies that are over sized and underindustrialized. They cannot
    support themselves so cheats are needed to keep the colonies alive and
    functional… And unless a chain truely needs a no cheat setup we will
    continue to have to use it, and we will need to prep a save with alot of
    reasouces if we need a no cheat run."* Written into
    `agent/WORKFLOW.md` as a binding rule: cheat markers are **expected** in a
    playtest log and get attributed, not excused; the reason is asked **once**;
    a cheat is a confound **only** where the reading intersects what it changed,
    and the agent must name the intersection or say there is none; and a leg
    that truly needs a no-cheat run must **declare it in its brief and prep a
    resource-rich save**, never improvise on an existing playtest colony.
    **Nothing is owed by you** — this is recorded so no future sitting spends
    your minutes re-litigating it. Trigger: six `ObjCheat CheatFill` markers in
    the PT-60 sitting log, which cost you an explanation you should not have
    had to give.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐⭐ NEW from the `corun-pt15` SITTING (two calls, both yours)


**Cost, stated honestly: the brief promised ~45–90 attended minutes and the
sitting took about 3h10m.** The overrun is ours except the march itself — that
was you playing your own colony through the mystery, and prep had already
warned the mystery was far longer than the plan first assumed. Itemised on the
session record: our stop-instruction lost the organic wisp reading (recovered
forced — same trap, same 95 wisps, but no longer "your own click"), a speed
instrument recommended the wrong rung and had to be overridden, the HUD kept
silently dropping the march to 1×, and the cheat disclosure took three asks.
**Your deviations (the extra passenger rocket, activating all three shifts)
are what made C39 readable at all and are not scored against you.**

9. ~~**⚖️ `C39` — the four Workshops lose half their staffing with NO
   offsetting uplift whenever Service Automation passes. Repair or not?**~~
   ✅✅ **DECIDED 2026-08-12 — EXTEND THE COMPENSATION, plus the sibling-label
   sweep your questions surfaced.** Ruled after a full walkthrough: the
   Workshops DO take the cut (measured 12→6) and only miss the payback; the
   dev comment states the assumption they violate; performance feeds only the
   shift-end Comfort payment (consumption scales with staffing fraction and is
   untouched, so balance exposure ≈ nil — the fix restores the exact
   conservation your Diner already gets). ⭐ Your questions also found that
   **sibling automation laws exist for `FactoryBuildings` (confirmed in data)
   and `ResearchBuildings`**, never swept for the same label-vs-class
   mismatch — the build enumerates all three labels and covers every mismatch
   found, not just the four Workshops. The delabel alternative (your
   employment-sink intent theory) was considered and declined in favour of the
   dev comment's stated intent. Queued into the next unattended build chain;
   verification re-runs the same paused bracket on a `CP15PT15` staged copy
   (it holds the measured TV Studio Workshop). → `agent/bugs/C39.md`.
10. ~~**⚖️ `C46` — re-graded 2026-08-12 after your challenge: the phantom-power
    state we measured cannot be reached by normal play.**~~ ✅ **DECIDED
    2026-08-12 — WONTFIX, your ruling in your own words:** *"Lets just write
    that one off since its not a true bug."* Your challenge was what caught
    it: the omission is real in the shipped code, but every path that writes
    the trap's power value only runs in "free" mode and the once-only choice
    means the game can never reach the free→destroy sequence our rig forced —
    so organically there is no phantom. Nothing is built; the defensive
    one-liner was declined with this ruling. `CP15F15.savegame.sav` is no
    longer needed for any open question — keep or delete it as you like.
    → `agent/bugs/C46.md`.


---

## ck- -- archived 2026-09-14 (was checklist status:closed): ⭐ NEW from `corun-batch-2` prep (nothing needs your call; two are cleanup already done)


**FYI, and it is a gap in our own gate.** Four agent-created staged saves —
`CB1STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`, about **223 MB**, all byte-identical
copies of `TEST2H TRAIN` — were still sitting in your save folder and in your
in-game load list, while `corun-batch-1`'s terminal audit had recorded *"all
staged/throwaway saves gone from the save dir"*. **Deleted this session**, with
`TEST2H TRAIN` re-verified byte-identical (MD5 `103B320A…8958`, mtime unchanged).
⛔ **The cause is structural, not a slip:** the co-run close-out gate runs
`git status` in both repos and **never looks at the save directory at all**, so
a staged copy that outlives its commit is invisible to every check we have. The
next chain's close-out is told to check it; whether that becomes a standing
WORKFLOW rule is worth one line from you if you care.

**Also, two entries had results that never reached them** — C42's and F21's
2026-08-05 readings were on their checklist riders only. Both entries corrected;
the archive cross-check rule you got from batch-1 caught both on its first use.
**And F21's "penalty half unmeasured" turned out to be our reader**: `spent_time`
is not a field on any class in the game, so that `nil` was guaranteed. The real
statistic reads fine — station rolling average **516,309** against its trains'
**47,968–183,186**, which is the shape F21 predicts.

**Not decisions, just so you know where things stand:** D07 is **4-of-5**, not
3-of-5 — trigger A passed on 2026-07-30 with your Forever Young A/B and the
entry had been stale for five days; you caught that from memory during the
sitting. PT-47, M5 and M7 never ran and stay routed. F99 did not fire once in
two hours; the one condition it names is still untested and the recipe for
building it is on the entry.

- **The mod-page relabel package** — ✅ **proposal ADOPTED 2026-08-04 (your
  `--approved`, in your own hand), ⚠️ but NOT closed: the wording is still
  owed by you.** Five shipped fixes (F55 forever-mark, F40 android dust
  sickness, F73(b) shelter reflex, F70 template refill, F97 dust-devil gate)
  are correct repairs whose *bug-ness* is a design judgment; the adopted
  proposal is a short "judgment calls" section in `MOD_DESCRIPTION.md` so they
  aren't presented identically to, say, F23 or F12. **The wording is yours** —
  the item said so, and approval adopts the proposal, not the words.
  `MOD_DESCRIPTION.md` is **FROZEN until launch prep**, so this is now a
  **launch-prep instruction with an owed input**: when the freeze lifts, the
  section goes in with your wording. This line stays until that wording
  exists. → `docs/agent/reports/CHAIN_QA_REPORT.md` §3.
⭐ **CONVENTION (added 2026-08-03, chain-12 QA, from `BUG_LIST_AUDIT.md`
§10.6f(i)): record the SESSION UPTIME next to any error COUNT.** Cross-arm
count comparisons (this leg's 0 vs that leg's 80) depend on comparable
exposure, and the owner's sessions run 1–6 hours — which makes zero-error
results *stronger* than they read, but only if the uptime is on the record.
One line per leg: "session ~Nh".

⭐ **CONVENTION (added 2026-08-04, owner): CO-RUNS — a rider class where the
agent drives and you are on call, not on duty.** For items with heavy setup and
a short measure, or intermittent triggers you'd never catch in hours of
organic play: the agent preps everything unattended (scripts, staged save
copy, a measure-moments list), launches and drives the game, and you attend
ONLY the minutes where eyes or a judgment call are needed. Such riders are
tagged **TAKEABLE IN a co-run**. Protocol and the forced-vs-organic evidence
rule: `docs/agent/prompts/perma/CO_RUNS.md` (moved 2026-09-12, D5). First candidates: the F11
pre-wrapper watch (below), C41's vanishing picker (amplified spawn/open loop),
F99's no-cheat discriminator (forced break, organic drone repair), plus the
two C-side console reads that need no eyes at all.

⭐ **ROUTING SWEEP 2026-08-04 (post-rig; the block above predates the rig).**
Every open item re-triaged under WORKFLOW's routing rule now that the rig is
proven. ✅ **ADOPTED by the owner same day** — each item's Status line now
carries its mode; ⚠️ each converted test still gets its setup re-derived in
rig terms by the session that runs it — the designs below were written
assuming the owner drove everything.

⚖️ **Execution rule for unattended work (owner, 2026-08-04):** a truly
unattended item runs as a **two-prompt chain — Opus executes, Fable audits**.
Batched unattended work runs as a **full chain: Opus throughout** (top tier
mid-chain only where something is genuinely complicated), **closed by a
terminal Fable audit**. Full form: `agent/WORKFLOW.md` routing triage.

⚠️ **CORRECTED same day, and it upgrades two verdicts:** the sweep first
claimed "no verified command forces a dust storm". **Wrong — table-staleness,
not a source fact.** `CheatDustStorm(storm_type, setting)` exists, ungated,
with `"normal"` / `"great"` / `"electrostatic"` types (`DustStorm.lua:540`),
and a **static-charged dust devil** can be forced outright (both now in the
HELP verified table, `[NEVER RUN]`). So **F90 moves from organic-only to
co-run STAGEABLE**, and PT-27/PT-28 no longer wait sols for a storm.

| verdict | items | what you still do |
|---|---|---|
| → **UNATTENDED** | **PT-35** (all reads are numbers + save/reload — the "nothing changes on screen" check becomes "the read-back numbers don't change", which is the entry's own claim) · **F99 residue rider** (the rig can STAGE break + cheat + pre-reload read deliberately — it no longer waits for a sitting to happen to use the cheat) · **F99 no-cheat discriminator** (forced break, organic drone repair at speed, log watch — no eyes; still gated on your go, it feeds your severity call) · **load-heal sweep** (Do-first #2 — was ~1 h of you; save/reload cycles are the rig's proven core; re-scope first) — ⭐ **all four are now the `unattended-1` chain** (`agent/prompts/unattended-1/`, built 2026-08-04, Opus×2 + Fable audit per your rule), plus the two `[NEVER RUN]` command verifications and a C42 ride-along | kick off the chain |
| → **CO-RUN** (was full playtest) — ⭐ **the front four + ride-alongs are now the `corun-batch-1` chain** (`agent/prompts/corun-batch-1/`, built 2026-08-04: PT-37 · PT-47 · PT-42 · PT-53 E + F21/C42/popup-trio rides + the optional PT-35 fixture build; Opus prep → your ONE sitting, est. 15–25 attended min → Fable audit. Kickoff: Opus on `01_OPUS_PREP.md`; the sitting runs when you sit) | **PT-37** (break staged via the proven `BreakTrackElement` route, reload cycles rig-driven; your eyes: route formation + the salvage-cursor check) · **PT-47** (agent forces the volley + runs the 5 integrity checks; your eyes: scatter-vs-rank, the one thing that is eyes by nature) · **PT-27/PT-28** (provisioning is the real cost; catch-lists and Health-drop patterns are console reads; PT-28 rides PT-27's storm nearly free) · **PT-42** (agent stages stock/drain at speed; your eyes: the faction panel goals at 3–4 moments) · **PT-53 E** (two hands moments — manual assign, Mod-Manager disable; the load-clean read is log) · **PT-18** (agent stages the landings on a SAVE-E copy; deaths/stranding are counters; ⚠️ SAVE-E itself is still ~30 min of your provisioning) · **PT-10** (setup rig-driven; your eyes: clumping + screenshots) · **PT-15** (reads scripted, `SetLightTrapMode` is a verified command; fixture still needs the mystery pick) · **F74+F53(a)** (harness builds the fresh colony unattended; you: the pack-disable click + the two UI acts) · **PT-60** (suite/reload/log halves rig-side; you keep only the 15–20 min ordinary-play segment) · **PT-20** (you keep the disable click + 10 min play) · riders **F21 · F34(d) · F85 · F38 · popup keystone · §3.6** (each a hands-moment or ride-along once staged) | minutes, named per brief |
| **stays PLAYTEST** | **PT-62 remainder** (the campaign gate — behavioural drain judgment through a landing; rig can carry P12's save/disable/load mechanics) · **PT-21** (organic play IS the test) · **PT-30** (mystery playthrough, UI actions) · **C39** (explicitly a keyboard judgment) · **doctrine C-sitting** (likely co-runnable — re-scope against `CHAIN_QA_REPORT.md` §1.3 before promising) | the sitting |
| **stays ORGANIC-ONLY rider** | **F80 · C25 · F06 · F83 · C40 · C32 · F76/C41 recurrence** (situation must arise; the READS are one-line co-run/console asks when it does) · ~~F90~~ (moved to co-run — see the correction above) | tap when it happens |

Two consequences worth knowing: **your dominant remaining cost shifts from
sittings to fixture provisioning** (SAVE-A/D/E builds — cheats are
scriptable but building placement is UI, so those stay co-op sessions); and
since co-runs ARE attended, a co-run pass you witness can earn `tested`
exactly as a sitting does — F11's watch was denied only by a fixture gap,
not by the format.



## STATE cleanup scope override — 2026-09-15

Condition: briefs `zz-owner/08_STATE.md` and `zz-owner/09_STATE_DOOR.md` were
removing content that failed the owner's STATE admission tests. The agent
stopped at a generated count block: it failed reach, but doccheck required
its presence and regeneration would restore it. The agent proposed removing
that stored copy and its requirement while retaining on-demand counts and
the underlying consistency checks, then asked for authorization.

Owner, verbatim:

> You have an owner override to do any and all tasks related to the scope of your prompt, that is extended to anything that makes docu check go red

This authorizes completing the STATE cleanup and related doccheck repairs,
including removal of the mandatory count copy, its regeneration code and
obsolete region tests. Verified counts remain available through
`python tools/doccheck.py --emit-counts`; count derivation, membership checks
and withholding the verified block on RED remain. Related count-location
instructions are corrected in the same change. The protected owner-register
idioms remain in STATE. No further owner action is owed for this change.

Evidence and disposition: `docs/agent/reports/STATE_DOOR_APPLICATION.md`.


## STATE admission door installation 2026-09-15

Condition: STATE cleanup and removal of its mandatory generated-count copy
were complete at `07b7ca6`, but the reusable eviction prompt still carried
only a three-part test scoped to Hazards. The complete September 15 rulings
lived in gitignored `.claude/DECISIONS.md`.

The owner requested, under the same scope override, that the completed door
be written into `docs/agent/prompts/perma/STATE_EVICTION.md` as its durable
home. It applies to every section: HARM names a victim with a moderate floor;
REACH asks whose job and who needs to know, both everyone, with self-consuming
chain work excluded by construction; GATE cites an existing machine check
instead of restating its duty; VOLATILITY refuses settled records. The tests
are AND-ed, never OR-ed: one failure is enough. The prompt preserves the
owner's verbatim reach and volatility words and the complete operational test.

The owner also requested correcting doccheck's stale "mandatory read"
diagnostic: STATE is pull-only. The corresponding docs-map description is
corrected with it. No owner action is owed. The operative door is in the
prompt; execution evidence is in `docs/agent/reports/STATE_DOOR_APPLICATION.md`.

## Wildfire investigation override 2026-09-16

While the prompts-folder freeze was being torn down, the owner invoked
`WILDFIRE_CURE_RESEARCH.md`. Asked whether that lifted the freeze for this
investigation, the owner replied:

> Yes its being tore down now, if you run into any friction in the tree in the mean time, you have a direct owner over ride

This authorises the Wildfire investigation to proceed during the teardown,
including resolving tree-policy friction under this direct instruction. The
brief's cause-and-fix scope and evidence requirements remain the work to do.
No further owner action is owed for this authorisation.

## Affected-save recovery requirement 2026-09-16

During the Wildfire cause-and-fix investigation, after a legacy migration
failure was identified, the owner stated:

> One quick follow up, if we cannot figure out a way to unstick a save via some method when we fix a bug, that is by definition a failure.

A successful bug fix must include a way to recover an already affected save.
Preventing the trigger in future games alone does not meet this requirement.
The method may be built into the fix or another demonstrated recovery route;
if no recovery method can be established, report the fix as incomplete rather
than successful. F120 is the current application. No further decision is owed
from the owner on this requirement.

## Do not build a fix for a version players cannot play 2026-09-16

After the Wildfire cure investigation (F120) built a repair for a defect that
exists only in a colony carried from 1.0.7 into 1.1.0, the owner ruled:

> do not build a fix for a patch a player cannot play. 1.0.7 cannot load except on a very few installs not steam and not console. this was a fix designed for player that force update there save from 1.0.7 to 1.1.0

Landed the same day as a header rule in `docs/agent/FIX_POLICY.md` and as item 11
of the `prompt-authoring` skill, in one wording:

> Rule: Do not build a fix for a version players cannot play; a defect that lives only in a save Steam and console cannot load stops before the build brief. [A3: pass]

The reach question — which platforms can reach the state, and whether the cause
produces the reporter's case — is the quiet side of the same rule and rides
inside it. No further owner action is owed.

## C93 diagnosis scope 2026-09-16

Condition: the first C93 probe found that the save's repeated entity-less drone
approach targets were MegaMalls, while the owner knew the colony carried a mod
related to malls. Those targets were not the Outside Ranch or its piles.

The owner instructed:

> Stopped you, ignore the megamall, I think they had a mod related to malls and
> thats the broken part there, the ranch only unloads resources after a build
> phase, does the probe need to run during that phase?

The investigation excluded the MegaMall noise, filed no mall defect, and replaced
the probe with a ranch-only pile-placement and pickup reading spanning a production
cycle. That reading identified three Origin piles whose pickup approaches fail and
six real-spot piles whose pickup approaches succeed. The ruling is scoped to this
diagnostic separation; it does not classify vanilla MegaMall behavior. No further
owner action is owed for the scope decision.

## LF tree and RED mixed line endings 2026-09-16

A peer found `.claude/tools/archive_settled.py` dead for a day: checklist item 189
landed 25 LF lines in a CRLF file, the tool split on CRLF, lost headers, and its
header-count invariant refused every run while doccheck stayed GREEN. The cause
was this clone checking text out as CRLF while most writing tools write LF, and
git hiding the mix because both forms store as one blob. Asked what the real issue
was, the owner said:

> Whats the real issue and is it fixed, i don't want it to continue to happen

Offered three layers (an LF tree, a RED gate on mixed files, readers that tolerate
mixed input), the owner ruled:

> lets do all 3

Landed the same day. `.gitattributes` carries `* text=auto eol=lf` and the clone's
local `core.autocrlf` is false; every tracked text file was converted to LF and
proved identical to its stored blob, archived game logs excepted as raw evidence.
doccheck's EOL section is RED on a mixed file, with `--fix-eol` as the cure. The
shared generator writes LF. The archive tool splits on LF and strips a trailing CR,
proved on a rebuilt incident: the old tool refused, the new one produced the same
plan as on a clean file. No further owner action is owed.
