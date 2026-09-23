# Full-body replacements on game 1.1.1.405907 — priority report (2026-09-23)

Phase A of `docs/agent/prompts/GAMEPATCH_1_1_1_ADJUDICATION_high.md`, run on a different seat
from the one that produced `c7266f0` and `d45655c`. Written from HEAD `9073a06`.

## Must_Read_Header

Reader: the owner deciding which 1.1.1 follow-up work to start, and whoever executes either
1.1.1 follow-up brief. Every game citation is SOURCE on the archived `1.1.1.405907` tree unless
marked `1.1.0.403908`; `Code/` lines are the pack at `9073a06`. A figure marked desk-MEASURED
names the command that produced it. A retail line cites the owner's unattended on-leg log by
line number and carries that run's limits: the on-leg also loaded the Opt-In and Train Hub
mods, and neither leg met the zero-error gate. A KEEP here is a 1.1.1 judgement, not a
standing clearance. This report ranks and corrects the seed; it changes no code and no entry
status. The rest of the adjudication is the Phase B report.

## 1 · The population, re-derived

**Route.** Not the seed's. `python tools/replacecheck.py` (committed with this report) lists,
per module, every site that writes a function into a shipped table and every local that
captures a shipped function, with a file-wide count of the capture's invocations. That output
was then read module by module: every install body was opened for the modules with a capture,
to see whether the capture is called on every path and whether its result survives. The two
falsifying reads the brief required were run through the same output: modules with no pin or
with a wrapper classification were swept for an uncaptured install, and every called capture
was checked for a path that substitutes our own implementation.

**Criterion.** A module is a *full-body replacement* when it installs a function over a shipped
declaration and, on the paths where the module is active, never calls the shipped body it
displaced. A *partial replacement* calls the shipped body but overrides part of its work with
a copy of our own. A guard that returns early without calling the shipped body (a
pre-condition, a suppression) is not a replacement: it re-implements nothing.

**Result, desk-MEASURED.** 52 modules (`ls Code/Fix_*.lua | wc -l` = 51, plus
`90_SaveSanitizer`). Split: **13 full-body · 27 delegating wrappers or guards (two of them
partial) · 12 hooks, data patches and migrations** — 13 + 27 + 12 = 52. The seed's own split
(12 · 17 · 22) sums to 51, one short of its stated 52.

| module | replaced declaration | install | shipped body called on the active path? | 1.1.1 body | retail on-leg |
|---|---|---|---|---|---|
| `Fix_TrackSalvageWipe` | `TrackGridElement:DemolishAndSplitTrack` | `:111` | no capture | **changed** | applied `:87` |
| `Fix_VacuumWalks` | `Colonist:TryToEmigrateToDome` | `:218` | no capture | **changed** | applied `:94` |
| `Fix_DomeOverviewHighlight` | `Community:UICommandCenterStatUpdate` | `:36` | no capture | **changed** | applied `:98` |
| `Fix_TrainCargoDumping` | `Train:UnloadAll` | `:247` | no capture | **changed** | **inactive** `:99` |
| `Fix_WispRewards` | global `SetLightTrapMode` | `:39` | no capture | **changed** | applied `:81` |
| `Fix_BombardmentSpread` ⚠️ not in the seed | global `WaitBombard`, plus copies of the file-locals `GenerateDir` and `travel_dist` | `SetGlobal` `:202` | no capture | **changed** | applied `:121` |
| `Fix_ExtenderFlapChurn` ⚠️ not in the seed | `DroneHubExtenderBase:UpdateUplinkRequesters` — **not pinned**; the pin is its caller `OnSetWorking` | `:82` | captured `:81`, called **only when the module is inactive** `:83-84`; the active path re-implements the body in a debounced thread `:91-103` | identical | applied `:122` |
| `Fix_LandscapeUnitFilter` | global `LandscapeForEachUnit` | `:218` | no capture | identical | applied `:108` |
| `Fix_PayloadTemplateRefill` | `CargoRequestNew:Apply`, `CargoRequestNew:RetrieveRequests`, plus a copy of the file-local `resolve_loc_cargo_template` | `:237`, `:263` | no capture | identical | applied `:105` |
| `Fix_RocketDroneChurn` | `CargoTransporterNew:UpdateCargoResourceRequests` | `:102` | no capture | identical | applied `:89` |
| `Fix_ShuttleTransportCache` | global `FindTransportationModeToCommunity` | `:61` | no capture | identical | applied `:92` |
| `Fix_TrackConnectorPingPong` | `TrackConnectedObjBase:CreateConnectorElements` (its `Done` at `:225` is a wrapper) | `:144` | no capture | identical | applied `:111` |
| `Fix_TrackSalvageRefund` | `TrackBase:GetRefundResources` (its `Demolish` at `:195` is a wrapper) | `:124` | no capture | identical | applied `:118` |

Partial replacements, recorded on the replacement side of the line the brief asked me to draw:

| module | what is delegated | what is replaced | 1.1.1 body |
|---|---|---|---|
| `Fix_GraphConsumedCaption` | `City:GetColonyStatsButtons` is captured `:86` and called `:88` | the returned panel's `caption` closure is overwritten with ours `:75-83` | changed (REMOVE row) |
| `Fix_ShuttleHubOffAvailable` | global `IsLRTransportAvailable` is captured `:76`; a `false` is honoured `:80` | on a `true`, the shipped loop is re-run from our own copy with a stricter condition `:81-90` | identical (`ShuttleHub.lua:410-419`) |

**Seed corrections, by name.**

- ⛔ `Fix_TradeRocketFuelRefresh` is **not** a full-body replacement. It captures
  `R.OnModifiableValueChanged` (`:86`), calls it on every path and returns its results
  (`:107-113`). The seed's twelve counted it; this report removes it. Its 1.1.1 status is in §3.
- ➕ `Fix_BombardmentSpread` replaces `WaitBombard` through `SMRFixPack.SetGlobal`, an idiom
  the seed's `function Class:Method(` test does not see. Its header says so in words
  (`:19-26`: "full replacement of `WaitBombard`").
- ➕ `Fix_ExtenderFlapChurn` replaces a declaration it never pinned, which is exactly the
  shape the brief's first falsifying read predicted. Its manifest pins the caller.

Net: seed 12 → **13** (− TradeRocketFuelRefresh, + BombardmentSpread, + ExtenderFlapChurn).
`Fix_BuildingCodesPrefab`, the module the brief named as outside the seed's test, installs
nothing: one additive `OnMsg.ConstructionComplete` handler (`:251`). It is a hook.

Membership was cross-checked against the retail on-leg census, which lists each module's
apply outcome by name (log `Mars.exe-20260923-10.39.06-6aad2d75.log`, lines 81-122, archived
with this report as `docs/archive/logs/ck208on_…`); every module above appears there with the
outcome in the last column.

## 2 · What 1.1.1 changed under each copy, and what shipping our copy reverts

Body spans are `python tools/bodycheck.py --src <archived tree> --all`, run on both archives
this session (19 BODY-CHANGED rows on 1.1.1, 0 on 1.1.0); diffs are the two archived bodies
compared with `tools/luafn.find_bodies` as the delimiter.

### 2.1 Targets 1.1.1 changed

**`Fix_TrackSalvageWipe`** — `TrackElement.lua:467-637` (1.1.0: `:467-618`). Four additions:
a live repair site is excluded from `all_elements` (`:484-488`); `remove_from_track_arrays`
takes any construction site out of `elements_under_construction` (`:517-524`); after the
split every surviving broken element is followed to rehome its repair site and rebuild each
track's `repair_cgs` (`:598-614`); `TrackBase:ProcessAllElements` is repair-aware
(`Track.lua:466-474`). Our copy carries none of them: zero hits for `repair_cgs` or
`insert_unique(el.track_obj` in the module, and the 1.1.0 array rule survives at `:257`.
Reverts: **a save-state repair** — repair-site ownership and `repair_cgs` are persisted
fields. Blast radius: **silent and permanent** in the save. Confirms F124.

**`Fix_VacuumWalks`** — `Colonist.lua:1894-1982` (1.1.0: `:1886-1983`). The transport-task
branch is rewritten (`same_dest`, `task.migration_dest = false`, `emigration_dome` follows a
journey under way), and the shuttle-booking block is replaced by `self:BookShuttleRide(...)`.
A new `Colonist:MigrateStep` (`:2155-2221`) calls this method for the final leg (`:2181`) and
repeats the breathable-or-vacuum threshold for an intermediate walk at `:2199`. Our copy has
zero hits for `BookShuttleRide`, `migration_dest` or `MigrateStep`. Reverts: **a repair players
would notice** (shuttle booking and reservations on the final leg; `migration_dest` never
cleared by our body). Blast radius: silent; colonist state, not save structure, but
`transport_task` persists. Confirms F125, including the second, unfixed site.

**`Fix_DomeOverviewHighlight`** — `ColonyControlCenter.lua:1290-1295`. Vanilla now writes the
computed text and defines red as `#colonists > 0 and v < low`. Ours is the 1.1.0 copy.
Reverts: the empty-dome guard. Blast radius: **loud and visible, cosmetic** (an empty dome
reads red 0). Confirms F122.

**`Fix_TrainCargoDumping`** — `Train.lua:787-831` (1.1.0: `:779-805`), rewritten: a
`room_for` helper that checks `IsResourceEnabled`, assignment preservation, an `unload_cargo`
helper. Ours is the 1.1.0 copy plus a guard; zero hits for `room_for` or `unload_cargo`. On
1.1.1 retail the module's behaviour probe **declined** and the copy was not installed (log
`:99`: "this copy is written for game 1.1.0 and stands down on a different body"). Reverts
nothing while it declines; if it ever applied, it would revert the vendor's
assignment-preserving unload (player-noticeable, not permanent). Blast radius today: inert by
a genuine decline.

**`Fix_WispRewards`** — `Fireflies.lua:712-738` (1.1.0: `:677-704`). Exactly two lines
changed: `UIColony:AddResearchPoints(reward)` removed, `Change(#trap.fireflies * 1000)`. Those
are our F15 and F07 edits (`Code/Fix_WispRewards.lua:52-54`, `:59`). Reverts: **nothing** —
our body is behaviour-identical to the vendor's. Blast radius: inert. The REMOVE row is
housekeeping.

**`Fix_BombardmentSpread`** — `Bombardment.lua:52-150` (1.1.0: `:55-153`). Two hunks:
`local spawn_dir = GenerateDir()` replaces `local dir, angle = GenerateDir()`, the
per-missile `GenerateDir(dir, angle)` line is deleted, and `spawn_pos` uses `spawn_dir`. The
vendor removed the dead per-missile jitter rather than using it, so vanilla 1.1.1 still fires
a whole volley along one direction — the triage's KEEP reasoning holds. Reverts: a dead-code
cleanup; our copy keeps the per-missile spread (`:126-128`) and consumes more `SessionRandom`
draws per volley than 1.1.1 does. Blast radius: **cosmetic** (Mystery 7 visuals). Hygiene owed:
its manifest now reads BODY-CHANGED and DEFECT-GONE on every `bodycheck` run (the regex at
`:45` names the deleted line), which is noise a future reader will have to re-derive; restamp
it deliberately with this read recorded, or re-copy onto the 1.1.1 body. No behaviour work.

### 2.2 Targets 1.1.1 left byte-identical — inert this patch, standing exposure

| module | 1.1.1 span (bodycheck OK) | this-patch caveat |
|---|---|---|
| `Fix_LandscapeUnitFilter` | `Landscaping.lua:509-523`, data `:505-507` | none found; `LandscapeConstructionSite.lua` changed (patchcheck ANON) outside the pinned body |
| `Fix_PayloadTemplateRefill` | `CargoRequestNew.lua:196-245`, `:171-194`, `:370-387` | none; `FlightPolicyDef.lua` changed (CITE) — template data, not the copied bodies |
| `Fix_RocketDroneChurn` | `CargoTransporterNew.lua:1437-1470` | ⚠️ two **new vendor callers** run our copy: `UniversalRocket.lua:1922-1926` now refreshes any landed rocket with cargo, and the new fixup `SavegameFixups.ZZZ_UpdateRefuelRequests` (`RocketCompatibility.lua:1139-1144`) calls it for landed non-player rockets on load. Our copy's non-player behaviour is meant to equal vanilla's; that is SOURCE, untested |
| `Fix_ShuttleTransportCache` | `Colonist.lua:3374-3408` | none; `VisitService` changed (CITE), a consumer |
| `Fix_TrackConnectorPingPong` | `TrainTransport.lua:116-156` | none (no patchcheck row) |
| `Fix_TrackSalvageRefund` | `Track.lua:286-307` | ⚠️ coupled to the track unit: its `Demolish` wrapper (`:195-250`) snapshots `track.elements` and treats a repair site as delegating through `track.elements` (`:204-207`); those assumptions must be re-read against the 1.1.1 array rules once the F124 rebase changes which split body runs |
| `Fix_ExtenderFlapChurn` | `DroneHubExtender.lua:109-111`, identical in both trees | the replaced declaration is unpinned, so the next time it moves nothing reports it; pin it |

"Inert" here means the copy reverts nothing on 1.1.1 because the body it displaced did not
move. Each is "not yet broken" in the standing sense: every one pins a 1.1.0 body it will keep
reinstating on the next patch, and `bodycheck` will say so only for the declarations they pin.

### 2.3 The seed's wrong row

**`Fix_TradeRocketFuelRefresh`** (wrapper). Pinned body `UniversalRocket.lua:1922-1926` changed:
the condition is now `self.cargo and self:IsRocketLanded()`, dropping `IsPlayerControlled()`.
On the on-leg the module's probe threw (`IsRocketLanded` is nil on the probe's stub, log
`:90`) and the module went inactive (`:91`). That is an accidental decline that happens to be
the right outcome; as a wrapper it would otherwise have ridden the vendor change and
refreshed a loading trade rocket twice. REMOVE stands on its premise; the enrolment gate on
the new fixup is Phase B.

## 3 · The track pair

Claim under test: `Fix_TrackSalvageWipe` and `Fix_BrokenTrackSalvage` both pin
`TrackGridElement:DemolishAndSplitTrack` at sha `7466b940…`, the former replaces it, and the
REMOVE brief's premise for retiring the latter is only true after F124's rebase.

**Re-derived.** Both pins are at those lines and that sha (`grep -n -- "-- SRC:" Code/*.lua`:
`Fix_TrackSalvageWipe.lua:90`, `Fix_BrokenTrackSalvage.lua:35`). `Fix_BrokenTrackSalvage` does
**not** replace the split body: it wraps `TrackBase:BreakTrackElement` (`:56-66`, capture
called `:58`) to stamp `node_idx` on a new repair site, and stamps legacy sites in a
`LoadGame` sweep (`:71-84`). Its second pin is a dependency pin: its DEFECT regex names the
sort inside the split body (`:37`). Its `Require` test, `TrackGridElement.node_idx == false`
(`:47-51`), still passes on 1.1.1 (`TrackElement.lua:173`), so it applies (log `:86`).

**What 1.1.1 did about F45.** `BreakTrackElement` is byte-identical on 1.1.1
(`Track.lua:628-663`, bodycheck OK): the vendor did not add `node_idx` to the copied
parameters. F45's crash cannot occur in vanilla 1.1.1 for a different reason: the split body
excludes repair sites from the list it sorts (`TrackElement.lua:484-488`) and
`ProcessAllElements` excludes them too (`Track.lua:466-474`). So "1.1.1 excludes and rehomes
repair sites, including old unstamped saves" is a true statement about the vendor's body.

**What runs in a shipping pack.** Until F124 lands, the split body that runs is
`Fix_TrackSalvageWipe`'s 1.1.0 copy. It puts repair sites into `all_elements` under the old
array rule (`:257`) and, before sorting, stamps a missing `node_idx` from `el.broken`
(`:181-185`), declining the salvage if any stays non-numeric (`:186-190`). Consequences:

- Removing `Fix_BrokenTrackSalvage` before F124 is **crash-safe** — the pre-sort stamp covers
  an unstamped site — but the REMOVE premise is not what runs: the repair site is still
  sorted and salvaged as a physical element, which is F124's defect, not F45's.
- After F124, the premise holds, the stamp is redundant, and the LoadGame sweep has nothing
  to do.
- The pin coupling is real: F124 restamps `Fix_TrackSalvageWipe.lua:90`; the identical pin at
  `Fix_BrokenTrackSalvage.lua:35` stays at the 1.1.0 sha and reads BODY-CHANGED for as long as
  the file exists (its regex still matches the 1.1.1 sort line, so no DEFECT-GONE will mask
  it). A pack with F124 landed and `Fix_BrokenTrackSalvage` still present carries a permanent
  false alarm in the very instrument that routes the next patch.

**Verdict: one unit, owned by the FIX brief.** The F124 work item should (1) rebase
`Fix_TrackSalvageWipe` on the 1.1.1 body, (2) retire `Fix_BrokenTrackSalvage` in the same
change, preserving its F45 evidence in the entry, and (3) re-verify `Fix_TrackSalvageRefund`'s
`Demolish` wrapper against the rebased split body (`:204-207` assumes a repair site delegates
through `track.elements`; `:233` reads `track.demolishing`). The REMOVE brief drops its
`Fix_BrokenTrackSalvage` row and can fire for its other fourteen independently of F124. The
alternative — leave the row in REMOVE and gate it on F124 — is workable but leaves the pin
alarm in place between the two commits and splits one behaviour across two auditors.

## 4 · Rank order — what to start first

Ranked by: does the copy install on 1.1.1 retail; did 1.1.1 change what it displaced; is the
reverted vendor work a save-state repair, a player-noticeable repair, or cosmetic; is the
failure silent and permanent, loud, or inert.

1. **The track unit — F124 rebase of `Fix_TrackSalvageWipe`, retiring `Fix_BrokenTrackSalvage`
   with it, and the `Fix_TrackSalvageRefund` wrapper re-read.** First because it is the only
   row that is applied on 1.1.1, reverts a save-state repair, and fails silently and
   permanently; and because it blocks a REMOVE row.
2. **F125 rebase of `Fix_VacuumWalks`.** Applied on 1.1.1; reverts the multi-leg migration
   rewrite; silent; and the new `MigrateStep` site is a second copy of F52 that no module
   reaches.
3. **Retire `Fix_DomeOverviewHighlight` (F122).** Applied, reverts the empty-dome guard, loud
   and cosmetic; a file deletion plus registrations.
4. **Retire `Fix_WispRewards`, `Fix_TrainCargoDumping`, `Fix_TradeRocketFuelRefresh`** — all
   inert on 1.1.1 (identical body; declined; declined). Housekeeping inside the REMOVE brief;
   nothing player-facing waits on them.
5. **`Fix_BombardmentSpread` manifest.** KEEP; restamp or re-copy after recording the read in
   §2.1, so `bodycheck` stops reporting a defect that a reader must re-derive to dismiss.
6. **`Fix_ExtenderFlapChurn`: pin `DroneHubExtenderBase:UpdateUplinkRequesters`.** A
   manifest-only change that closes an unpinned standing exposure. `Fix_ShuttleHubOffAvailable`
   is the same shape in one direction and can wait.
7. **The six identical-target copies.** No 1.1.1 action. `Fix_RocketDroneChurn` earns one
   probe in the next A/B for its two new vendor callers.

The FIX brief's third item, F121 `Fix_CloggedBuildingRelease`, is a hook and a sweep, not a
full-body replacement, and is outside this ranking; Phase B reads it. The retail on-leg shows
it inactive on 1.1.1 (log `:279`), which is the stand-down F121 describes.

## 5 · What this changes for the two follow-up briefs

- **REMOVE brief.** Its `Fix_BrokenTrackSalvage` row names the vendor body as the replacement;
  that body does not run in a shipping pack until F124. Move the row to the FIX brief (§3).
  The other fourteen rows are unaffected by Phase A; their premises are Phase B.
- **FIX brief.** Its F124 item should absorb the retirement of `Fix_BrokenTrackSalvage` and
  the re-verification of `Fix_TrackSalvageRefund`'s `Demolish` wrapper. Its F125 item is
  confirmed as scoped, including the second site.
- **Neither brief** is falsified by the population correction: `Fix_TradeRocketFuelRefresh`
  stays REMOVE (as a wrapper, for a different reason than the seed gave), and the two added
  full-body modules are KEEP rows with hygiene items only.

## 6 · Claim limits and not opened

- Everything on the vendor side is SOURCE on the archived trees; nothing here was run in
  the game by this seat. The on-leg census lines are the owner's unattended run and carry
  its limits (Must_Read_Header).
- "Inert" for the six identical-target copies is a body-identity claim, not a compatibility
  claim: a changed callee or caller can move semantics under an identical body, and the
  `Fix_RocketDroneChurn` new-caller note is exactly that shape.
- Not opened: whether `Fix_RocketDroneChurn`'s copy behaves as vanilla's for a non-player
  rocket; whether `Fix_TrackSalvageRefund`'s snapshot survives the 1.1.1 array rules (owed to
  the track unit); the `MigrateStep` intermediate-leg path beyond reading its threshold line.
- The script `tools/replacecheck.py` is a router: it misses an install written as
  `X.M = helper(...)` (`Fix_HabitatExpeditionDraft`, whose captures it still prints as called
  on every path) and cannot judge what a body does with a captured value. The per-module
  verdicts above are reads, not its output.
