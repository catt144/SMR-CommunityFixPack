# Chain prompt 2 — the batched co-run sitting (the owner is HERE)

**Read `README.md` in this folder first — binding chain rules apply.** This
prompt runs ONLY with the owner present and starts when they say so. Start
with `git log --oneline -10` + `git pull` + the PT-00 probe sweep. Todo list
up front; the owner watches it live.

**Read path**: this folder's README · the brief in "Notes from upstream"
below (prompt 1's product — the measure-moments list is the contract) · each
leg's entry at the moment you run it (briefs cite entries; you ACT on the
entry) · `PLAYTEST_HELP.md` verified table for every console line you hand
the owner.

## The shape of the sitting

- **The owner's attended cost is the measure-moments list, nothing else.**
  Between moments they are free; tell them when the next moment is ~1 min
  away. Batch their moments; never make them wait through agent-side reads.
- **One command per line, from the entry, via the verified table.** Nothing
  improvised at the console mid-leg; if a leg needs an unverified call, that
  is a finding and the leg stops.
- **Predictions were written in prep — read each leg's aloud (in chat)
  BEFORE running it.** A miss is a finding, not an embarrassment.
- **Run-conditions header before every leg; FORCED/ORGANIC named in every
  recorded finding.** Session uptime next to every error count.
- **Ordering is binding** (README): reads → PT-53 manual-assign → PT-37 →
  PT-47 → popup trio → leg-5 fixture (optional, owner's call live) → PT-53
  uninstall half DEAD LAST.
- **Sign-off per the ADOPTED tiers:** Tier-A moments get the owner's verdict
  words recorded verbatim; HANDS-ONLY moments record the act + the card;
  Tier-B results fill the prepped card skeletons. A witnessed pass CAN earn
  `tested` — claim it only where the owner's eyes were on the thing the
  entry's claim is about, and say which moment carried it.
- **Stop conditions per README.** The owner leaving mid-batch is a clean
  stop, not a failure; record actuals for what ran.

## Jobs

**Job 1 — run the batch per the brief.** For each leg: predictions read →
run-conditions header → the leg → readings recorded against predictions →
owner verdict words (where tiered) → next. Keep the game's log flushed; note
the `Lua H:MM:SS:mmm` markers at leg boundaries (EF-045's instrument — that
is how prompt 3 re-times everything).

**Job 2 — record, same session.** Results go on the ENTRIES (dates, uptime,
run conditions, log citations); status flips follow the recording rules
(front matter + heading tag; INDEX is generated); every cited log archived
`git add -f` in the same commit; probes deleted in their recording commits;
`PROBE SWEEP:` line; staged copy + throwaway saves deleted (the leg-5
FIXTURE save survives, named). Checklist sections this sitting completes move
WHOLE to `PLAYTEST_ARCHIVE.md` per the documented rule — PT-37 and PT-47 are
candidates if their cases actually complete.

**Job 3 — the log review (PT-22), together, before the owner leaves.**
Newest `Mars.exe-*.log`: every unexplained line verbatim with its age;
never-discount rule binds.

**Job 4 — hand off.** Append to `03_FABLE_AUDIT.md` "Notes from upstream":
per-leg verdicts with their logs · actuals vs predictions (wall time AND
owner-minutes vs the brief's estimates) · every deviation/surprise/retry in
an unforeseen-issues ledger (the co-run program's second batch of evidence —
unattended-1's ledger is the baseline; what recurred, what is new?) · owner
decisions taken live (verbatim) vs still open · routed gaps. Commit, delete
this file in the same commit, update the manifest row, doccheck green, push.

## ⛔ What you may not claim

- `tested` only where the owner's eyes were on the entry's own claim at the
  moment it held — named moment, named claim, or it is not `tested`.
- Nothing about legs that were SKIP'd or cut — they stay routed.
- No owner-time verdicts ("this saved you X") — report actuals vs estimate;
  prompt 3 audits both.

## Notes from upstream

*(Appended by chain prompt 1, 2026-08-04 — the sitting brief. Everything below
was derived from the ENTRIES against `ModTools\Src`, not from the checklist,
per the routing-sweep warning. One unattended confirm cycle RAN on the staged
copy; its log is the evidence for every "MEASURED" claim here.)*

### 0. What prep actually did, and what it did not

**RAN:** one confirm cycle on `CB1STAGE.savegame.sav` (a `Copy-Item` of
`TEST2H TRAIN`, game closed, MD5-identical: `103B320A1434513BC8773553096A8958`).
Launch 20:29:59 → log `Mars.exe-20260804-20.30.21-6a22b86d.log`, cold load
**9,493 ms** by the engine's own line, whole process **49,996 ms**, **zero
engine error lines**, all reads, **no mutations**. Probes disarmed in the same
act; sweep clean in both repos.

⛔ **Nothing here is `tested`. Nothing is "ready" beyond what that cycle read.**
The minutes below are an ESTIMATE prompt 3 audits against actuals, not a
promise.

### 1. Fixture confirm — every reading AS READ

| What | Reading | Consequence |
|---|---|---|
| pack count | **81/81 active** | matches expectation |
| `Opt_CohortHousing` **by name** | registered id is **`CohortHousing`** = `active` (there is no id `Opt_CohortHousing` — that is the FILE name) | leg 4 is live; ⚠️ the prompt's own wording was wrong, corrected here |
| map / speed | `BlankBigCanyonCMix_09`, speed set + read back 0→3 | C4 holds |
| **Last Transmission** | **NOT active.** `active_factions` = ChurchOfTheNewArk, FlatMars, MartianFirst, ProsperityForMars, UnitedColonistFront (5). Legislature seats: MartianFirst 32 · ProsperityForMars 40 · UnitedColonistFront 26 · ChurchOfTheNewArk 1 · FlatMars 1. LastTransmission holds **0 seats**. It *does* carry a `factions_approval` record (approval 300, polarization 7500, 11 likes) with `TLEWaterStorage2Sols`=1500 and `TLEOxygenStorage2Sols`=1500 | ⇒ **LEG 3 = `SKIP — Last Transmission is not an active faction on this save (0 of 5 active, 0 legislature seats); the leg's owner moments are faction-panel goals that do not exist here.`** Stays routed. |
| Seniors / residences / cohort slots | 108 residences (18 cohort / 90 normal). Free slots: **cohort 86** (Child 55, Senior 31), normal 384. **184 Seniors**, all housed, **23 of them in a NORMAL residence**, **0 employed** | leg 4's fixture is PRESENT (23 × 31 ≠ 0). ⚠️ 0 employed Seniors ⇒ D07 **trigger A's employed-senior exemption stays UNSAMPLED** — that is trigger A, not this leg's trigger E, but do not let the sitting claim it |
| tracks / stations / trains | **17 tracks, 926 elements, 0 broken, 0 repair sites**; **11 stations**; **8 trains**, all sampled ones on `command=GotoStation` carrying 9–12 passengers; **13 healthy multi-element tracks**, longest sampled 43 elements | leg 1 case A fixture PRESENT; F21 ride-along fixture STRONG |
| passages | **4 passages, 50 elements, 0 unit entries** post-load | C42 `APPLICABLE=false` — identical to leg F. The within-session read is the only thing that can help |
| **dust defences** | **0 defence towers** (13 domes) | ⇒ **PT-47's interception reading is `UNSAMPLED`**, and the card must say so rather than "no interception seen" |
| cheap choice popup | 6 rockets; 5 report a launch issue — **4 × `no_target`, 1 × `fuel` (on Earth)**. `no_target` is **not** a key of `RocketBase:GetLaunchIssuePopups` (`RocketBase.lua:2210-2219`: missions_suspended / not_landed / fuel / maintenance / disabled / unloading). And `GetLaunchIssuePopups` **RAISED on every rocket queried** (`ok=false` — printed, per G3) | ⇒ **the documented cheapest route is NOT available here.** Src-verified alternative below |
| PT-35 turbine fixture | `FrictionlessComposites` **researched=false**, **0 Large Wind Turbines**, 6 turbines of any kind | leg 5's fixture build is valid and still needed |
| F21 baseline | **11 stations holding 117 colonists waiting for a train**, 8 trains | strong |

**Popup route, replaced.** `ShowBreakthroughChoicePopup(popup_preset, techs,
callback, ...)` (`Anomaly.lua:696-714`) with preset
`"SubsurfaceAnomalyBreakthrough"` (`Anomaly.lua:393`) — one of **F85's own four
sites**, not a stand-in. ⚠️ Precondition: `UIColony:UpdateAvailableBreackthroughTechs()`
must be non-empty (`:698` returns immediately otherwise) — **unverified on this
save**, so `CB1.PopupOpen()` prints the count and refuses rather than opening
nothing. ⚠️ Answering it discovers a breakthrough; staged copy only.

### 2. Job 2 — the two `[NEVER RUN]` instruments, Src-verified

#### `StartBombard` — `Lua/Bombardment.lua:156-161`

- Plain global, file scope, **not** in `ModEnvBlacklist`, **not** gated on
  `Platform.cheats` (only `TestBombard` at `:175` sits behind `Platform.debug`).
- It only spawns a **game-time thread** and returns — safe to call anywhere,
  but **nothing happens while the game is paused** (C4).
- Args (`WaitBombard:57`): `pos = IsValid(obj) and obj:GetPos() or IsPoint(obj)
  and obj or GetRandomPassable(map)`; `radius` feeds
  `GetRandomPassableAroundOnMap` per missile; `count` = missiles; `delay_min/max`
  = game-time ms between spawns.
- ⛔⛔ **THE ENTRY'S LITERAL RECIPE RAISES.** `UIColony:GetCityAtMap` **does not
  exist anywhere in Src** — zero hits across the whole tree. Colony's real
  accessors are `GetCityLabels` / `GetActiveColonyMaps`; a map's city is
  `map.City` (`_init.lua:22`) and the surface city is the global `MainCity`. As
  documented, F26's recipe throws `attempt to call method 'GetCityAtMap' (a nil
  value)` and the leg produces nothing. **Second chain running to find a
  documented `[NEVER RUN]` recipe broken as written** (unattended-1's
  `table.copy` devil row was the first) — rule 10 earning itself again.
- ⛔ **And the obvious repair is also wrong.** `City.__parents` includes `Object`
  (`City.lua:1-2`), so `IsValid(MainCity)` is TRUE and `MainCity:GetPos()`
  resolves — but a City is never placed, so that position is meaningless.
  `GetRandomPassableAroundOnMap` then either returns nil (→ the per-missile
  fallback `GetRandomPassable(map)`: **8 missiles scattered across the whole
  map**, none in the owner's camera) or garbage. Either way the Tier-A read is
  destroyed.
- ✅ **Corrected form: pass a DOME** — a valid placed Object, in the camera, and
  the only way `missile:HitsDome` (`:86`) makes the dome-crack check reachable.
  `CB1.Leg2Bombard(<dome>)` does exactly this and refuses if the game is paused.
- The volley runs the **pack's** `WaitBombard`: `Fix_BombardmentSpread` replaces
  the global and `StartBombard` resolves the name at call time (`:158`).

#### `ProcessTrackElements` — `Lua/Tracks.lua:807`

- Plain global, file scope, not blacklisted ⇒ **reachable from the console and
  the mod env**. Leg 1's shape does not have to change.
- Signature is `(map, elements, start_element, adjust_iter)` — **the first
  argument is a MAP.** F48's corrected call `ProcessTrackElements(ResolveMap(qa_t),
  qa_t.elements)` is right; `ResolveMap` is a C global taking **one** argument
  (`CommonLua/LuaExportedDocs/Game/realm.lua:92`), which is precisely why the
  shipped `ResolveMap(track, track.elements)` silently drops `elements`.
- ⭐ **CORRECTION TO F48.md — the failure path is NARROWER than the entry says.**
  `OrderTrackElements`' failure branch (`Tracks.lua:614-620`) is
  `assert(false, "unable to find the expected number of track elements")` →
  (EF-008: does not unwind) → **restores the original element order** from the
  `table.copy` taken at `:569` → `return` nil. `ProcessTrackElements` then hits
  `if not OrderTrackElements(...) then return end` (`:818`) and returns **before
  any Z-repositioning, section building or pillar work.** The entry's stated risk
  — *"the caller repositions every element in Z and recomputes pillars and
  sections"* — **does not happen on the failure path.**
- ⚠️ **But the entry UNDER-states the residue.** The restore fixes the array
  order only. Permanent, and saved: `start_el.connections = {}` plus a rewritten
  `connections` on every element the walk reached (`:578-580`, `:606-617`); a
  forced `start_el.node_idx = 1` (`:579`) while the success-path renumbering
  (`:632-635`) never runs — **a duplicate `node_idx` is the signature**; and
  leftover hash keys `elements[<el>] = true`, never cleared.
- ⛔⛔ **AND CASE B MAY NOT SAMPLE THE FAILURE PATH AT ALL — Src cannot settle
  it.** `BreakTrackElement` (`Track.lua:618-659`) does **not** remove the element
  from `track.elements`: it sets `element.broken = <site>`, hides it, and places
  a `TrackConstructionSite`, whose `__parents` are `{ "ConstructionSite",
  "TrackGridElement" }` (`TrackElement.lua:580-583`). **Two `TrackGridElement`s
  now occupy the broken hex**, while the walk's `HexGetTrackGridElement` is
  `hex_grid:GetObject(q, r, "TrackGridElement")` (`TrackElement.lua:1-3`) and
  returns exactly one. Which one is a C-side question.
  - returns the hidden original → the walk **succeeds** → case B is case A again
    and **the decider is UNSAMPLED**;
  - returns the construction site → `is_track_element[e]` is false → the walk
    stalls → the assert fires → case B is real.
  ⇒ `CB1.ReadWalkability(track)` answers this **before** any mutation, and
  `CB1.Leg1CaseB()` **refuses to run** unless the gate says the walk will fail.
  A clean pass on a track that was never unwalkable is not a pass.
- ⚠️ **Do NOT hand-assign `start_el`/`end_el`** the way F48's procedure line
  does. `ProcessTrackElements` sets both itself on the success path
  (`:820-822`), so the assignment is redundant there — and on the FAILURE path it
  would write endpoints the shipped repair would never write, making case B look
  *more* destructive than the repair is. The library runs what would ship.

### 3. The measure-moments list — the contract

Ordering is the README's, and it is binding. **⚠️ One ordering consequence the
README does not spell out: the C42 within-session read must be taken BEFORE any
save or load in the session** (a load may rebuild `Holder.units` empty — that is
what made leg F's zero UNSAMPLED), and leg 1 case A ends with a save+reload. So
C42 rides the warm-up, not leg 1's tail.

| # | Leg | Owner does / looks at | Verdict words to say | Tier | Min |
|---|---|---|---|---|---|
| M1 | **PT-53 E, manual-assign half** (module live, runs EARLY) | Select a Senior living in a NORMAL residence; manually assign them a residence. Then leave it running. | *"assigned"* / *"it moved them anyway"* | **HANDS-ONLY** | **3** |
| M2 | **PT-37 case A** (healthy track, after the corrected call + save/reload) | Does the route still form, does the train still run, does anything look different? | *"route forms / train runs / no visual change"* or name what broke | **A** | **2** |
| M3 | **PT-37 case B** (damaged track, after the assert) | Is the repair site still salvageable (F45 cursor read — `PLAYTEST_HELP` "Salvage mode"), does the rest of the network still route, does a save+reload come back clean? | *"salvageable / network routes / reload clean"* → UNBLOCKS F48 · anything else → CONFIRMS THE BLOCK | **A** | **4** |
| M4 | **PT-47 bombardment** (camera LOW on the chosen dome, before the call) | Do the missiles arrive from visibly different angles, or as a rank of parallel trails? | *"scatter"* (fix works) / *"parallel"* (old behaviour) | **A** | **3** |
| M5 | **Popup keystone + F85** | Options → Key Bindings, rebind Quick Save to **F9**; open the choice popup; press F9. Did a save land? | *"save landed"* → F85 is R2-by-rebind, owner decision · *"refused"* → F85 drops toward I/R4 | **HANDS-ONLY** | **4** |
| M6 | **PT-35 fixture (OPTIONAL)** | Place ONE Large Wind Turbine; apply ONE building upgrade | *"placed"* | **HANDS-ONLY** | **4** |
| M7 | **PT-53 E, uninstall half — LAST ACT** | Mod Manager → disable Community Fix Pack → load the save made with it ON | *"loads clean"* / name what broke | **HANDS-ONLY** | **4** |

**Total attended estimate: ~24 minutes.** That is at the TOP of the README's
15–25 band, not over it, so nothing is silently trimmed. If the owner wants it
shorter, **M6 is the one to drop** (−4 min → ~20): it is explicitly optional and
its consumer is a separate 2-prompt unattended chain that does not exist yet.
**Leg 3's SKIP already removed its 3–4 minutes** — do not spend them elsewhere
without saying so.

Everything else in the batch is agent-side and costs the owner nothing: the
fixture reads, the C42 and F21 ride-alongs, the five PT-47 integrity readings,
the leg-1 snapshots, the log review's mechanical half.

### 4. Predictions, numbered, written before anything runs

**Leg 1 — PT-37 / F48**
1. Case A's corrected call leaves the track's SNAP signature **unchanged**
   (`start_el`/`end_el` already are `elements[1]`/`elements[#elements]`, so the
   success path re-assigns the same objects). *Falsifier:* any change to
   `start_el`, `end_el`, or a duplicate `node_idx` appearing on a healthy track.
2. Case A survives save+reload with the same signature. *Falsifier:* a different
   signature after reload, or a train that stops running.
3. On the damaged track, `CB1.ReadWalkability` reports **shadowed > 0** and the
   assert fires. *Falsifier:* `shadowed = 0` and `missing = 0` — in which case
   the decider is UNSAMPLED and leg 1 records that, not a pass. **This
   prediction is genuinely 50/50 and prep says so.**
4. If the assert does fire, the residue is `connections` + a duplicate
   `node_idx`, and **no** Z/pillar change. *Falsifier:* element positions moving,
   which would mean prep mis-read the early return at `:818`.

**Leg 2 — PT-47 / F26**
5. `StartBombard` with a dome as `obj` returns without raising and 8 missiles
   appear. *Falsifier:* the `TRY` line reports `ok=false`.
6. The owner sees a **scatter**. *Falsifier:* parallel trails — which would mean
   `Fix_BombardmentSpread` is not doing what the entry claims.
7. The volley **ENDS** (peak in-flight > 0, then 0). *Falsifier:* the 3-minute
   bound with peak > 0 — the entry says revert the fix in that case.
8. Scorch decals appear; ≥1 dome reads as cracked. *Falsifier:* zero decals after
   ground impacts.
9. The interception reading is **UNSAMPLED** (0 towers). *This is not a
   prediction that can miss — it is a measured absence, stated so nobody later
   reads it as "no interception happened".*

**Leg 4 — PT-53 E / D07**
10. ⚠️ **The interesting one.** Prep measured **23 Seniors in normal residences
    while 31 free Senior cohort slots exist and `CohortHousing` reads `active`**.
    Prediction: those 23 are in domes with no *reachable* free Senior slot
    (`FindTransportationModeToCommunity` / `CanAcceptNewColonists` gating), i.e.
    the module is behaving. *Falsifier:* a Senior in a normal residence in the
    **same dome** as a free Senior slot — that would be the in-dome pass failing,
    and it is a defect, not a fixture note.
11. Manual assignment WINS: after the owner's assignment the colonist stays put
    across a run at speed. *Falsifier:* the module moves them back.
12. Mod-Manager-disable + load: the save loads clean, no pack residue.
    *Falsifier:* errors naming pack code, or a broken colony.

**Ride-alongs**
13. C42 within-session, after real passage traffic: **unit entries > 0**, and
    stale entries ≈ one per traversal on the last element entered. *Falsifier:*
    unit entries still 0 after traffic — which would mean `LeadIn` is not doing
    what leg F's trace concluded, and C42's row would be back in question.
14. F21: platform waiting does not appear in the travel-Comfort penalty or the
    rolling-average stat. *Falsifier:* a rider with a long queue arriving with a
    matching Comfort loss.
15. F85: the F9 rebind is accepted and a save lands under the popup.
    *Falsifier:* the binding UI refuses F9, or `CanSaveGame` blocks.

### 5. Per-leg run-conditions template

Fill this before every leg; a finding without it is not admissible (EXTERNAL
VALIDITY rule):

```
LEG <n> — <PT-id> / <entry>
  build ........ 1.0.7.396349 retail Mars.exe
  save ......... CB1STAGE.savegame.sav (COPY of TEST2H TRAIN, MD5 103B32…8958)
  map / speed .. <read back, never assumed>
  loads ........ <this process>
  pack count ... <AS READ, e.g. 81/81>  + <modules named for this leg>
  FORCED ....... <exactly what this leg made happen that would not have>
  ORGANIC ...... <what stayed the game's own>
  uptime ....... <session uptime beside any error count>
  log .......... Mars.exe-<stamp>.log
```

**SKIP lines produced by the confirm cycle, verbatim, for the record:**

- `LEG 3 (PT-42, F22/F75): SKIP — Last Transmission is not an active faction on
  CB1STAGE (0 of 5 in g_FactionsHolder.active_factions; 0 legislature seats).
  Fixture-gated per README; stays routed, never a re-choice of save.`
- `LEG 2 (PT-47) interception reading: UNSAMPLED — 0 DefenceTowerBase on the
  save. Not "no interception observed".`
- `POPUP TRIO: the documented cheapest route (rocket launch-issue prompt) is NOT
  available on CB1STAGE — 4 of 6 rockets report no_target, which has no popup
  entry, and GetLaunchIssuePopups raised on every rocket. Substitute route is
  ShowBreakthroughChoicePopup; if UpdateAvailableBreackthroughTechs() is empty
  the trio is SKIP <no choice popup reachable>.`
- `D07 trigger A (employed-senior exemption): UNSAMPLED — 0 of 184 Seniors are
  employed on this save. Not this leg's trigger; recorded so nobody claims it.`

### 6. Evidence-card skeletons (Tier B — fill, do not compose live)

```
CARD — <leg>: <one-sentence claim>
  scenario ......... <what was set up, in one line>
  FORCED / ORGANIC . <named explicitly>
  raw before ....... <the log line, verbatim>
  raw after ........ <the log line, verbatim>
  run conditions ... <the block from §5>
  falsifier ........ <the one sentence that would have made this wrong>
  verdict .......... PASS / FAIL / UNSAMPLED  (UNSAMPLED needs its population)
```

Cards owed regardless of outcome: **leg 1 case A** (Tier-B half: the SNAP
before/after pair) · **leg 2 integrity** (decals, dome crack, notification,
interception=UNSAMPLED, volley ENDED) · **C42 within-session** · **F21 reads** ·
**leg 4 precedence**. Tier-A moments (M2/M3/M4) get the owner's verdict words
recorded **verbatim** beside the card, not paraphrased.

### 7. Arming, launch, and the stall bound

**Arm with the parked script, never inline** (`CB1_ARM.ps1.txt` in this folder;
copy to a scratch `.ps1`):

```
.\CB1_ARM.ps1 arm      # writes 97_CB1Common.lua + 99_CB1Legs.lua, arms metadata,
                       # then READS EVERYTHING BACK OFF DISK (ARM GATE) and
                       # exits non-zero rather than let an unarmed launch happen
.\CB1_ARM.ps1 disarm    # in the commit that records the answers
```

⚠️ **Never pipe that script's output** (C11 corollary — a piped consumer can
terminate the upstream pipeline before the write runs). ⚠️ It writes UTF-8
**without** BOM deliberately; see the ledger below.

**Resolution cross-check (G1), run this session over the parked sources —
GREEN, quoted:**

```
PARSE GREEN  97_CB1Common.lua.txt / 98_CB1Confirm.lua.txt / 99_CB1Legs.lua.txt
RESOLUTION GREEN - USED minus (DEFINED + FIELDS) is EMPTY
```

Re-run it before the sitting's launch — the sources may be edited between now
and then, and a parse sweep is a *syntax* verdict, not a resolution one.

**Launch:** `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050` —
no `-smrautorun`. **⚠️ Logs live in `%APPDATA%\Surviving Mars Relaunched\logs`
(Roaming), not Local — prep wasted ten minutes polling the wrong directory.**

**Expected first output, MEASURED this session:** launch → new log file in
**~22 s**; the game reaches the main menu and `95_AutoRun` stands down by
itself. `99_CB1Legs` prints nothing until called — that is by design, so the
liveness check at the sitting is **the main menu appearing within ~60 s**, not a
banner. Cold load of the 56 MB copy **9.5 s**; a second load of the same map
~6 s. ⇒ **If no window and no log after 60 s, something is wrong — say so out
loud rather than waiting.** (unattended-1's I2: the owner beat the rig's own
bound to a stall. Do not make that necessary twice.)

**Console entry points — one line per moment.** `CB1.Leg1Read()` ·
`CB1.Leg1CaseA()` · `CB1.Leg1Damage()` · `CB1.Leg1CaseBCheck()` ·
`CB1.Leg1CaseB()` · `CB1.PickDome(n)` · `CB1.Leg2Bombard(CB1.dome)` ·
`CB1.Leg3Gate()` · `CB1.Leg4Before(SelectedObj)` / `CB1.Leg4After()` ·
`CB1.Leg5Grant()` / `CB1.Leg5Save()` · `CB1.RideC42()` · `CB1.RideF21()` ·
`CB1.PopupOpen()`.

### 8. Unforeseen-issues ledger from PREP (prompt 3 compares against
unattended-1's 8-entry baseline)

Six entries, **zero of them the game's fault** — the same shape as last night.

| # | What | Class |
|---|---|---|
| P1 | `UIColony:GetCityAtMap` does not exist; F26's documented `[NEVER RUN]` recipe raises | **recurrence** of unattended-1's I-class "a Src-verified documented recipe is broken" (the `table.copy` devil row) |
| P2 | The first `ReadTrackFixture` counted "trains with a route" as 0 of 8 while the F21 reader on the SAME load showed all sampled trains on `GotoStation` with 9–12 passengers. A bad READER, not a bad fixture — corrected visibly in the harness | **new**: a reader whose negative result is indistinguishable from an absent fixture |
| P3 | `CB1.ErrorWatchNote`'s text contained the literal token an error sweep greps for, so the marker **matched its own search** — the confirm cycle's error grep returned 2 hits, both of them that sentence. Inherited from unattended-1's `U1.ErrorWatchNote`, where the same defect existed unnoticed | **new**, and it is retroactive: any hand-run error grep over the unattended-1 logs counted 7 phantom hits |
| P4 | PowerShell 5.1's `Set-Content -Encoding utf8` silently prefixed a **UTF-8 BOM** onto `metadata.lua`. The game tolerated it; git did not. Restored with `git checkout`; the parked script now uses `WriteAllLines` with an explicit no-BOM encoder | **new**: an arming script corrupting the file it arms |
| P5 | `RocketBase:GetLaunchIssuePopups` **raised** on all 6 rockets. Only visible because G3 forced the `pcall` result to print — a nil return and a raise print identically | **recurrence** of unattended-1's I3 (`pcall` discarded), caught this time by the rule that came out of it |
| P6 | `track.stations_connected` read 0 of 17 and looks like "no track connects two stations". It is set only on the `<=2`-element branch (`Track.lua:668-677`); the reading is correct and meaningless | **new**: a field whose name promises more than it stores |

**What that says about the guardrails:** G3 caught P5 outright, and G1 caught
nothing here **because prep wrote the payloads and the harness together** — G1's
value is at the sitting, where the library was written hours earlier. P2, P3 and
P6 are all the same family: *a reader that cannot fail is not a measurement*, the
leg-design rule applied to prep's own instruments rather than to the legs.
