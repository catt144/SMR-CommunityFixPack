# 1.1.1 playtest plan — triaged for exposure, not coverage

## Must_Read_Header
<!-- RULES -->
Rule: Ship-blocking is phases 1–3 only; phase 4 is post-ship unless a phase 1–3 result implicates it. [A3: pass]
Rule: Run the unattended legs single-variable — the pack is the only difference between them. [A3: pass]
<!-- /RULES -->

Audience: the owner, at the controls. Ordered so the build can ship after phase 3.

## Why this is triaged rather than exhaustive

Every hour of testing is an hour thousands of users run the **current** build on game
1.1.1, and that build is not inert. It ships full-body replacements that cannot stand
themselves down:

| shipping now | harm while we test |
|---|---|
| `Fix_TrackSalvageWipe` (F124) | Overwrites 1.1.1's repair-site rehome and `repair_cgs` rebuild. **Silent and permanent in the save** — no error, no report, damage accumulates. |
| `Fix_GeneForging` (F123) | Double-pays the technology. Measured in retail: returns 100 against a live parameter of 50. Wrong gameplay every birth. |
| `Fix_VacuumWalks` (F125) | Overwrites the multi-leg migration state machine. Silent. |
| `Fix_DomeOverviewHighlight` (F122) | Marks an empty dome red. Loud, cosmetic. |
| `Fix_FounderTraitNotification` (F126) | Builds an unknown notification id from the base class. |

So delay is not neutral, and the plan is sized to **de-risk shipping**, not to reach full
coverage. Coverage continues after release.

## The risk asymmetry that shapes it

Sixteen retirements sound like more risk than three rebases. They are not:

- **A deletion reverts to vendor code**, which the vendor ships and tests. Its realistic
  failure is a dangling reference — a load error, a lost registration, an orphaned probe
  — and that is caught wholesale by one clean boot, not by testing sixteen behaviours
  one at a time.
- **A rebase is new code** written this session against a body that moved. That is where
  a regression would actually come from.

Hands-on time therefore goes to the rebases and to save compatibility. The retirements
ride on the boot census and their desk controls.

## Phase 0 · Unattended — costs you nothing but the launch

Two autorun legs, then walk away. Each performs the boot census, `DispatchReach` and
`SMRTest.RunAll()` across the current 83 probes, then quits itself.

```powershell
& "C:\Program Files (x86)\Steam\steam.exe" -applaunch 3215050 -smrautorun
```

**Run it single-variable this time.** The 2026-09-23 A/B could not be read cleanly
because the on-leg also carried the Opt-In pack and the Train Hub dev mod while the
off-leg did not. Keep TestKit on for both legs and change **only** the fix pack between
them; disable every other mod for both.

Let each leg quit itself before touching anything, then scan each finished log with
`python tools/logscan.py <log>`.

What this settles, with no attention from you: all sixteen retirements load clean, no
module is orphaned or double-registered, the module census reads 36, and the probe suite
runs. If this is clean, the retirements are done being a ship risk.

## Two different "old saves" — do not conflate them

Phases 1 and 4 move on different axes, and only one of them is ship-blocking.

| axis | what varies | where |
|---|---|---|
| **Pack version** | a save written with the old 52-module pack, loaded with the new 36-module pack, **both on game 1.1.1** | Phase 1, ship-blocking |
| **Game version** | a save written on game **1.1.0**, loaded on 1.1.1 — what F121's provenance condition keys on | Phase 4, post-ship |

**A 1.1.0 save does load on 1.1.1.** The only revision gate refuses a save whose
`required_lua_revision` *exceeds* the running game's (`CommonLua/Savegame.lua:228-230`,
`:970`), and `config.SavegameRequiredLuaRevision` is **402200 on both builds**
(`Lua/Config/config.lua:179`, identical in the archived 1.1.0.403908 and 1.1.1.405907
trees). 1.1.1 did not raise the bar, so the block is forward-only: a 1.1.1 save will not
open on 1.1.0, but the reverse is fine.

**Loading a pre-1.1.1 save does not spend it** — corrected 2026-09-23 by observation,
after this plan first said to copy every fixture before loading. The revision F121 keys
on (`Code/Fix_CloggedBuildingRelease.lua:97-98`, `lua_revision < 405907`) is rewritten on
the next **write** (`CommonLua/Savegame.lua:775`), and the game writes manual saves and
autosaves as new files. `Japan Sol 490` is byte-unchanged at 2026-09-18 18:37 after being
loaded and played. ⚠️ The real rule is narrower: **do not save over a 1.1.0 file you want
to keep.** Supply is not tight either — 60 saves in `saves/game/` predate 2026-09-23.

Measured by the audit seat on 2026-09-23, reading five of the owner's saves as bytes:
1.1.1 saves carry `lua_revision 405907` with `orig_lua_revision 403908`; the 09-17
`C95*` saves carry `403908`. So the pre-1.1.1 fixtures in `saves/game/` are real and the
discriminator is live — candidates run 09-11 to 09-20, including `F119stuck` and the
`C95*` set.

## Phase 1 · The one test that cannot be skipped — ~10 minutes

**Load a save made with the old pack under the new pack.** Every existing user performs
this the moment they update, automatically, without choosing to. Sixteen modules have
just disappeared from under their saves. It is the highest-blast-radius path in the
release and it has never been exercised.

A **1.1.0-era** save is the better fixture: it exercises both axes at once, which is the
real user path — someone who last played before the patch and updates both game and pack.
`Japan Sol 490` (2026-09-18) was used. Avoid `Autosave Sol 493`: the owner reports an
Opt-In test asset live in that colony, which would confound the reading.

Load it, let it run a few sols, and watch for errors and for track or routing state that
looks wrong. Then do the reverse — save with the repaired pack, remove the pack, restart
fully and load — which is what a user who unsubscribes will do.

## Phase 2 · The two rebases — the irreducible hands-on work

This is new code and the only place a real regression is likely.

**Track salvage (F124).** Curved and short track salvage with a **live repair site
spanning the split** — the vendor semantics the rebase had to preserve. Check survivors,
refunds and shells. This one matters most: its failure mode is silent and lands in the
save.

**Vacuum migration (F125).** A direct final leg and an intermediate leg, with breathable
and no-passage controls. Check reservations and shuttle/train continuation, and cancel
a migration mid-route.

## Phase 3 · Sixty-second confirmations

Each is a single observation. Do them in whatever game state phase 2 leaves you in.

- **F123** — call the chance function with only Gene Forging researched. It must return
  the live parameter (50), not 100. One console line, and it is the defect with measured
  retail evidence against the current build.
- **F122** — open an empty dome's overview. The zero average must not be red.
- **F126** — no founder-trait notification appears where the removed one used to.

**After phase 3 the build can ship.**

## Phase 4 · Post-ship, or earlier only if implicated

**F121, the legacy clogged migration.** It is *inactive on 1.1.1* — the retail on-leg
logged it declining — so it cannot harm a current player. It only acts when loading a
save written before 1.1.1 that carries a stuck building. Testing it properly needs a
pre-1.1.1 fixture with that exact state, which is slow to construct and narrow in reach.
Pick a fixture from the 60 pre-2026-09-23 saves and simply avoid saving over it; loading
does not spend it (see "Two different old saves").

Its builder made the departure with the largest unexamined surface: a saved-provenance
condition resting on `CommonLua/Savegame.lua:775` rewriting the saved revision, with **no
save file inspected**. The audit seat inspected five on 2026-09-23 and the condition
holds. `orig_lua_revision` is **not** a usable alternative key: it records the colony's
origin, not the event's, so a fresh `BuildingClogged` firing on 1.1.1 inside a colony
started on 1.1.0 writes the same saved fields as a genuinely stranded one, and keying on
origin would release it and cut the vendor's one-hour disable short. `lua_revision <
405907` is the widest safe reach.

Its real-world reach is narrower than that suggests, which is the other reason this is
post-ship: **with the pack present at the first 1.1.1 load, a stranded building is healed
on that load, before the rewrite.** The under-heal only bites a player who updated, saved
once *without* the pack, and noticed afterwards.

Also here: the thirteen benign retirements' individual behaviours, which revert to
vendor code and have their desk controls.

## What would stop the ship

Phase 0 showing a load error, a module census other than 36, or a probe regression.
Phase 1 showing errors or wrong state on an old-pack save. Phase 2 showing lost vendor
semantics — survivors, refunds, `repair_cgs` or routing wrong. Anything else is a
finding to file, not a hold.

## Claim limits

Passing these phases supports "no regression observed on the paths played", not "tested".
The unattended legs are desk-MEASURED on their own configuration. Nothing here inspects
a save file's stored fields, so F121's provenance condition stays unproven either way.

## Results — phases 0 and 1, run 2026-09-23

Recorded from the owner's runs. Every figure here is from a named log; nothing is
estimated.

### Phase 0 · unattended, both legs

| leg | log | mods actually mounted | probes |
|---|---|---|---|
| off | `Mars.exe-20260923-13.21.34` | TestKit only — single-variable | 25 PASS · 30 FAIL · 24 SKIP · 4 ERROR = 83 |
| on | `Mars.exe-20260923-13.36.18` | TestKit + fix pack + Opt-In | 54 PASS · 6 FAIL · 20 SKIP · 3 ERROR = 83 |

The off leg is genuinely single-variable: only `SMR_CommunityFixPackTestKit` has a
`Loaded mod items for` line, so the Train Hub and Opt-In packs that spoiled the
2026-09-23 10:39 A/B were inert. The on leg carried Opt-In by the owner's choice, so the
two legs are not single-variable *against each other*; the on-leg comparison below is
instead against the pre-build on-leg (`ck208on_…10.39.06`), which also had Opt-In.

**Census: 36 modules seen, applied 36.** `SaintBlessing` reads inactive at `:130` and
ends active at `:147`; a first-pass read would have said 35/1.

**No new failures.** All six on-leg FAILs — `DomeFreeSpaceMismatch`, `LayoutTechLock`,
`AnomalyCaveInMap`, `C47OpenFarmSeedBufferShape`, `DryFarmingFarms`, `OptionsMenuOptIn`
— were already failing on the pre-build on-leg, which had eleven. Five cleared:
`GeneForging`, `CloggedBuildingRelease`, `SinkholeIndestructible`, `TrainCargoDumping`,
`UpdateReport`.

⚠️ **Correction, 2026-09-23.** This plan first read `GeneForging` leaving the FAIL list
as retail evidence that F123 was repaired. That was wrong. The `GeneForging` probe was
**deleted with its module** — it is absent from the TestKit and did not run on the
post-build leg. Its disappearance is an absence of evidence, not a pass. The same
caution applies to any of the five cleared names whose probe retired with its module;
only a name whose probe still exists and now passes is evidence.

Probe delta reconciles exactly: 98 → 83 is 15 probes retired, and −7 PASS −5 FAIL
−3 SKIP −0 ERROR = −15.

All four off-leg ERRORs (`LanderCargoRatchet`, `DroneUnreachableForever`,
`AutoExportPriority`, `FactionDomeSizeGate`) are pre-existing. `BuildingCodesPrefab`
dropped out because its module and probe were retired together. ⚠️ `logscan` matched
only the `[nil index]` shape and missed `FactionDomeSizeGate`'s `rawget` error, so it
reported 6 error-shaped lines where the probe summary says 4 ERROR; the summary is
authoritative.

The on leg's 44 error-shaped lines are dominated by synthetic Opt-In object-destruction
errors, all raised from `60_Probes_Opt.lua:246`. They are the likely source of the
game's on-screen mod warning the owner saw, and they appear only because Opt-In was on.

### Phase 1 · both halves, attended

| half | log | result |
|---|---|---|
| 1.1.0 save + new pack | `Mars.exe-20260923-13.42.02` | **0 error-shaped lines**; 36/36 applied |
| new-pack save, pack removed | `Mars.exe-20260923-13.51.55` | **0 error-shaped lines**; 0 `[CommunityFixPack]` lines |

Fixture: `Japan Sol 490` (2026-09-18 18:37), a genuine 1.1.0-era save. The owner ran
several sols, saved anew, reloaded and ran more, on both halves. Colony
`save_game_id: 55afqP8zZV1vEYMb` throughout.

No retired module leaves residue: a grep of all sixteen names over the with-pack log
returns three hits, all false positives — two are the game's own `MirrorSphereMystery`
in the save header, one is a vendor fixup name.

**The 1.1.0 fixture bought two gates that a 1.1.1 save could not.** The load applied 28
vendor savegame fixups, among them:

- **`ZZZ_UpdateRefuelRequests`** — the trade-rocket enrolment gate, previously settled
  only at the desk from `CommonLua/SavegameFixup.lua:24-48`. It is now **observed
  running in retail on a real 1.1.0 save**, so `Fix_TradeRocketFuelRefresh`'s removal
  premise is no longer desk-only.
- **`MoveOpenPasturePilesOffOrigin2`** — the Open Pasture migration half.

`CloggedBuildingRelease` reports `applied`, which is installation, not a heal: this
colony carries no stranded building, so **F121's repair path remains unexercised** and
phase 4 still needs a 1.1.0 save with an actually stuck building.

### Fixture supply — correcting this plan's own caution

Loading a save does **not** spend it; only writing over it does, and the game writes
autosaves and manual saves as new files. `Japan Sol 490` is byte-unchanged at its
original 2026-09-18 18:37 after being loaded. `saves/game/` holds **60** saves written
before 2026-09-23 against 3 after, so pre-1.1.1 fixtures are plentiful. The rule is
narrower than "copy the fixture first": do not *save over* a 1.1.0 file you want to keep.

### Claim limits on these results

Phases 0 and 1 support "no regression observed on the paths run", not "tested". The
phase 1 sessions were attended, so `SMRTest` did not run in them and the probe evidence
is the two autorun legs alone. The on-leg carried Opt-In, so its error counts are not
comparable to the off-leg's. Nothing here exercises the track or vacuum rebases, which
are phase 2.

### Phase 2a · Track salvage (F124) — PASS, 2026-09-23

Log `Mars.exe-20260923-13.59.45-6aad2d75.log`. Fixture built with the TestKit World
page's meteor leaf (the real vendor path — `Lua/Meteors.lua:718` is the only caller of
`BreakTrackElement`), not `CheatBreakTrack`, so the strike could be placed deliberately.
Running it also witnesses a World leaf owed in `tools/SMRTK.md` "Still owed".

| step | `SMRTest.ReportBrokenTrack()` |
|---|---|
| baseline | 0 site(s); 0 non-numeric `node_idx` |
| after meteor | 8 site(s); 8 non-numeric `node_idx` |
| after salvage, repairs complete | 0 site(s); 0 non-numeric `node_idx` |

`tracks 11 · elements 141 · orphaned elements 0`. **No error-shaped lines** across the
whole operation.

The salvage was taken on an undamaged element inside the damaged run, so the split
separated repair sites onto both resulting tracks — the only geometry that reaches the
vendor's rehome block (`TrackElement.lua:598-614`, *"repair sites are not in
all_elements, so follow each surviving broken element to its new track"*). Salvaging a
damaged segment directly short-circuits at `Fix_TrackSalvageWipe.lua:52-54` and never
exercises it.

What the result proves, in order of strength:

1. **`orphaned elements 0`** — the split's safeguard loop assigned every element to a
   track. This is the failure that would sit silently in a save rather than throw.
2. **8 → 0 repair sites, completed by drones** — each site followed its damaged element
   onto the correct new track *and* kept a working construction group. A site that lost
   its `repair_cgs` entry would stall at a non-zero count forever; the count reached zero.
3. **Drones left the salvaged stretches alone** while repairing the damaged ones, which
   is the correct split of intent between removal and repair.
4. **The retirement of `Fix_BrokenTrackSalvage` is validated in retail.** That module
   existed only to stamp `node_idx` at break time. The entire cycle — meteor, split,
   rehome, repair, completion — ran without it.

⚠️ **The TestKit's F45 message is stale on 1.1.1 and should be reworded.** It prints
"N with a non-numeric node_idx (track unsalvageable)", but the detector counts repair
sites (`is_construction_site and IsValid(el.broken)`), and both the vendor body
(`TrackElement.lua:485-487`) and the rebase (`Fix_TrackSalvageWipe.lua:67-69`) exclude
repair sites from the ordering before any `node_idx` check runs. A non-numeric
`node_idx` on a repair site therefore blocks nothing. The orchestrator seat drew the
wrong conclusion from that wording once during this run before checking the source; the
next reader will too.

### Phase 2b · Vacuum migration (F125) — PASS, 2026-09-23

Log `Mars.exe-20260923-13.59.45-6aad2d75.log`. Fixture: Tesla #1, Sacagawea #1 and
Fuller #1 on a non-terraformed colony.

Preconditions read before testing, so the repair was known to be eligible rather than
assumed — every decline condition at `Fix_VacuumWalks.lua:157-173` cleared:

```
breathable false   walkcap 40000   ignore 120000   domes 3
1 2 101421 passage          (Tesla-Sacagawea: none)
1 3 118769 passage          (Tesla-Fuller: none)
2 3  17348 passage true     (Sacagawea-Fuller: usable)
```

Sacagawea–Fuller at 17348 sits inside the 40000 walk cap with a passage, in vacuum, and
`walkcap + 1 < ignore` holds. That is the exact band where the defect lives: in vacuum
the shipped code compares against `ColonistMaxDomeWalkDist` instead of
`ColonistMinDistToIgnorePassage`, so a colonist who should take the passage crosses the
surface.

| site | route | result |
|---|---|---|
| `TryToEmigrateToDome` (F52's original site) | Fuller ↔ Sacagawea, direct | **passage** |
| `MigrateStep` (new in 1.1.1) | Fuller → Tesla, intermediate hop | **passage**, then train to Tesla |

**The second site was proven live before it was run.** A shuttle or train leg never
produces the walk result the repair arms on, so a migration that left by shuttle would
have looked like a pass while testing nothing. `GetNextMigrationLeg` was queried
read-only first and returned `kind walk · dome Sacagawea #1 · final false` — walk, and
non-final, which is the only shape `MigrateStep` arms for. The vendor's own ordering is
why: `Colonist.lua:3617-3619` adds walkable domes *before* the shuttle fill "so directly
walkable domes keep the more specific arrival mode", and nodes are write-once.

The colonist also completed Fuller → Sacagawea → train → Tesla without stalling at the
intermediate dome. That matters beyond F52: the retired module installed the 1.1.0
`TryToEmigrateToDome` body, which erased 1.1.1's task-retarget, `BookShuttleRide` and
`migration_dest` machinery. An arrival by train continuation is direct evidence the
rebase composed with that machinery instead of replacing it.

**Not run:** the cancel-mid-route control and the explicit no-passage fallback. The
no-passage path is exercised incidentally — Tesla has no passage to either dome and
routed correctly — but neither was run as a deliberate control, so both remain owed.

### Phase 3 and ck211, 2026-09-23

**ck211 — CLOSED, gate confirmed.** Log `Mars.exe-20260923-13.59.45`:

```
Resourcepile7 111 111
Resourcepile8 112 112
Resourcepile9 113 113
```

All three spots resolve to real ranges; none returns `-1`.

**The control was then shown able to fail**, because the whole reading rests on
`GetSpotRange` being capable of returning `-1`:

```
bogus spot        -1 -1            GetSpotRange("OpenPasture_Open","idle","Resourcepile99")
closed 7..9      109 110 111 111   OpenPasture, the known-good nine-anchor reference
```

(The closed line prints four numbers because only the last call in a Lua argument list
expands both return values: 7 → 109, 8 → 110, 9 → 111,111.)

So the Outside Ranch open entity does carry spots 7–9, where the deleted module's own
probe *required* them to be **absent** from `OpenPasture_Open`. The vendor repaired the
asset; the asset half of the Open Pasture gate holds and retiring
`Fix_OpenPastureStockpiles` was safe.

Note for a future reader: the live ranch may still render closed, as the owner observed.
That is irrelevant to this gate. `GetSpotRange` reads the entity definition, not a live
object, and a ranch only swaps to the `_Open` skin once the Open Domes law runs
`SetOpenAirBuildings`. This closes the one correction the audit raised
(`GAMEPATCH_1.1.1_AUDIT_2026-09-23.md`, C93), which had found the retail decline proved
the entity changed at *one or more* of the three rather than that all three exist.

**F123 — retail confirmation NOT achieved; desk evidence stands.**

```
GeneSelection false GeneForging false chance 0 forging param1 50
```

Neither technology is researched in that colony, so `chance 0` is correct and trivial:
the retired module only ever added its bonus *when researched*, so an unresearched state
returns 0 with or without the defect. The read confirms the live function is the vanilla
body with `param1 = 50`, and nothing more.

The decisive retail leg — GeneForging researched, expecting 50 rather than 100 — remains
unrun. What supports F123 is the audit seat's two-sided desk control
(`GAMEPATCH_1.1.1_AUDIT_2026-09-23.md` §6, pack-off leg calling the archived native
body). To close it in retail, grant tech points with the handoff's fixture and research
GeneForging on a scratch copy, then re-read.

**F122 and F126** are visual and produce no log output; record them from observation.

### FINDING — removal residue from `Fix_OpenPastureStockpiles`, 2026-09-23

Discovered in retail during phase 3, on a colony with Open Domes enacted. **Not filed as
an entry yet; this is the evidence record.**

Observed, in order:

| step | result |
|---|---|
| Ranch under Open Domes, new pack | renders **closed** |
| `print(OpenAirBuildings)` | `true` — the law *is* enacted |
| `r:GetEntity()` | `OpenPasture` (closed) |
| `r.open_air` / `r:GetCurrentSkin()` | `true` / `OpenPasture_Open` — both say open |
| forced `r:ChangeSkin("OpenPasture_Open", palette)` | **opens** — state is recoverable |
| destroy and rebuild the ranch | **opens** correctly |

An old ranch stays shut; a newly built one opens. That is the discriminator, and it rules
out a vanilla 1.1.1 defect: a ranch placed now takes `OpenAirBuilding:OnPlace`, which
applies the open skin, while the pre-existing object is never revisited.

**Mechanism (inference, not measured).** Vanilla swaps entities only when
`SetOpenAirBuildings` fires on the law *changing* state, and it early-returns when the
flag already matches (`OpenAirBuilding.lua:109-111`). Loading a save whose law is already
enacted therefore never re-fires the swap. Under vanilla that is harmless, because the
ranch was opened when the law passed and stays open. It was closed here only because
`Fix_OpenPastureStockpiles` forced the closed entity for both sides — C93 records that as
its *"declared tradeoff"*. Delete the module and nothing ever reopens what it pinned shut.

**Impact.** Cosmetic only: the closed entity carries spots 7–9 (109/110/111), so all nine
anchors exist and no pile strands — the old module's tradeoff still holds after its
removal. But it is permanent on affected saves and not self-correcting; a player cannot
clear it without rebuilding the ranch or toggling the law. Bounded to saves that ran the
old module with Open Domes enacted. New ranches are unaffected.

**Why it matters beyond the cosmetics.** Both the build report and the audit state that
removal residue was recorded for every changed exposed site. This is removal residue that
neither caught, on a module whose retirement was already the one correction the audit
raised (C93/ck211). The gap is in the method, not only in this module.

**Not claimed:** no numeric pile reconciliation was read on the reopened ranch, and the
mechanism above is an inference from source plus the new-versus-old discriminator, not a
traced load sequence.
