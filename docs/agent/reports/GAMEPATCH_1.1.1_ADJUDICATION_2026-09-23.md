# Adjudication of the 1.1.1 triage — `c7266f0`, `d45655c`, `9073a06` (2026-09-23)

Phase B of `docs/agent/prompts/GAMEPATCH_1_1_1_ADJUDICATION_high.md`, run on a second seat.
Phase A is `FULL_BODY_PRIORITY_2026-09-23.md` (committed `083cf2b`). Judged on the diffs and
the archived `1.1.0.403908` and `1.1.1.405907` trees, never on the triage's summary of itself.

## Must_Read_Header

Reader: the owner deciding what to fire, and whoever executes either 1.1.1 follow-up brief.
Verdicts are per area: **confirmed**, **corrected** (the record was changed in this commit),
or **unproven** (the claim stands only as a claim). Game citations are SOURCE on the archived
`1.1.1.405907` tree unless marked `1.1.0.403908`; retail lines cite the two unattended
2026-09-23 logs, archived as `docs/archive/logs/ck208off_…` and `ck208on_…` in `083cf2b`,
and carry that run's limits (§4). A KEEP is a 1.1.1 judgement, not a standing clearance.
Nothing here launched the game or changed code. The corrections are in the records
themselves; this report says which.

## 0 · Outcome in one screen

| area | verdict | what changed / what the owner decides |
|---|---|---|
| F121–F125 | **confirmed**, all five | an "Adjudicated 2026-09-23" paragraph in each entry names what was checked |
| REMOVE premises (15) | 14 **confirmed**; `Fix_BrokenTrackSalvage` **corrected** to one unit with F124 | row moved to the FIX brief; `Fix_FounderTraitNotification` added to REMOVE (F126) |
| Open Pasture gate | **confirmed** cleared, within the A/B's limits — **narrowed 2026-09-23 by the build audit** (§3): Lua and fixup half confirmed, asset half **unproven** | ck211: read the three spots in-game |
| trade-rocket gate | **settled at the desk**: the new fixup is enrolled | REMOVE brief clause annotated; runtime check is confirmatory |
| retail A/B | **confirmed as bounded**; one record gap corrected | logs archived; which claims survive is §4 |
| FIX premises (3) | **confirmed**, incl. F121's load-only half | FIX brief annotated |
| KEEP verdicts (34) | 33 **confirmed** at surface; `Fix_FounderTraitNotification` **corrected** to REMOVE | **F126 filed**; owner may set its priority |
| the two briefs | REMOVE: one row moved, one added, one clause discharged; FIX: F124 unit widened | both edited in this commit |
| `bodycheck.py` self-test | **confirmed**: still fails a tool that is RED on everything (two broken variants measured) | one residual noted, §8 |
| opt-in outbox row | brief premise **unproven**: no `<<PENDING-RUN>>` exists there | what is owed is §9 |
| ck207 | **corrected** in place: stale A/B bullet, missing evidence for the full read | ruling still the owner's, §10 |

## 1 · The five filings

Each `evidence:` field was tested against the archived tree by this seat's own route (the
body diffs and greps below, not the entries' citations). All five hold; each entry now carries
an adjudication paragraph with the exact spans re-derived here.

| entry | route | result |
|---|---|---|
| F121 | whole-tree `grep -rn 789863173059` on 1.1.1 (1 file, `Data/StoryBit/BuildingClogged.lua:8`; the same grep on 1.1.0 finds the same file, so the instrument sees it); `SavegameFixups` grep for `exceptional_circumstances` (none); `SetBuildingEnabledState:__exec` read (`ClassDef-Effects.generated.lua:2772-2790`) | confirmed: the Duration thread exists only for firings after the patch; no migration; the module's stand-down is at `Code/Fix_CloggedBuildingRelease.lua:209-221`, and the retail on-leg shows it inactive (`ck208on_…:279`) |
| F122 | body diff `Community:UICommandCenterStatUpdate` 1.1.0 `:1290-1300` → 1.1.1 `:1290-1295` | confirmed; full-body copy, applied on the on-leg (`:98`) |
| F123 | body diff `GetRareTraitChance` 1.1.0 `:4398-4402` → 1.1.1 `:4719-4728`; `Data/Tech.lua` `param1` GeneSelection 100, GeneForging 50; on-leg `:389`, off-leg `:277`; grep of both extra on-leg mods for the function (0 files) | confirmed, arithmetic included; the pack-on figure is not confounded by the mixed mod set; the pack-off line is an assumption, as the entry says |
| F124 | body diff `DemolishAndSplitTrack` 1.1.0 `:467-618` → 1.1.1 `:467-637`; module grep for `repair_cgs` (0) | confirmed; spans re-derived at `:484-488`, `:519-525`, `:598-614`, `:628-632`, `Track.lua:466-474` (the entry's `484-487` and `517-524` are one line off at an edge; left as leads) |
| F125 | body diff `TryToEmigrateToDome` 1.1.0 `:1886-1983` → 1.1.1 `:1894-1982`; `MigrateStep` `:2155-2221`; grep of the module for `BookShuttleRide`, `migration_dest`, `MigrateStep` (0) | confirmed, both sites (`:1911`, `:2199`) |

## 2 · The fifteen REMOVE premises

Each replacement body was opened in both trees and its consumer named; a disappearance was
not accepted as proof. Verdicts:

| module | replacement (1.1.1) | consumer traced | verdict |
|---|---|---|---|
| `Fix_BrokenTrackSalvage` | split body excludes repair sites (`TrackElement.lua:484-488`), rehomes them (`:598-614`); `BreakTrackElement` itself unchanged (`Track.lua:628-663`, bodycheck OK) | the split body — which, in a shipping pack, is `Fix_TrackSalvageWipe`'s 1.1.0 copy until F124 lands | **corrected**: premise true of vanilla, not of the pack; one unit with F124 (Phase A §3). Row moved to the FIX brief |
| `Fix_BuildingCodesPrefab` | both handlers dropped `from_prefab` and the early return (`LawDef-Efficiency.lua:704-708`, `:906-910`; 0 hits for `from_prefab` on 1.1.1, 2 on 1.1.0) | the `MsgReaction` handlers are the consumer | confirmed; module declined on the on-leg (`:167`) |
| `Fix_DestroyedTunnels` | `TunnelBase:AddPFTunnel` rejects `self.destroyed or self.linked_obj.destroyed` (`Tunnel.lua:194`) | the load-time tunnel sweep that calls it | confirmed |
| `Fix_DomeOverviewHighlight` | §1 F122 | UI stat update | confirmed |
| `Fix_GeneForging` | §1 F123 | birth trait roll | confirmed |
| `Fix_GraphConsumedCaption` | caption sums consumption + maintenance (`ColonyControlCenter.lua:181-186`) | the graph panel's caption closure | confirmed; our wrapper overwrites that closure with an equivalent sum (Phase A partials) |
| `Fix_MirrorSphereSite` | `IsActionEnabled` rejects `progress >= max_progress` (`MirrorSphere.lua:791-792`) | `StartAction` cancels a same-action first (`:829-832`) and only then consults `IsActionEnabled` (`:838`); the infopanel XDef consults it too (`Data/XDef/ipMirrorSphereBuilding.lua:53,72,91`) | confirmed, cancellation intact |
| `Fix_NightShiftWork` | modular-day window (`Colonist.lua:2396-2402`) | the shift-leave decision | confirmed; equivalent to our wrapper's window |
| `Fix_OpenPastureStockpiles` | `RebuildPastureStockpilePool` (`Animals.lua:1382-1526`) run by two fixups, `SharePastureStockpilePools2` (`:1569-1573`) and `MoveOpenPasturePilesOffOrigin2` (`:1579-1583`); neither name exists on 1.1.0 (0 hits) | `FixupSavegame` enrols both on an older save's first load (§3) | confirmed; gate §3 |
| `Fix_SinkholeIndestructible` | `indestructible = true` in the generated class (`Lua/BuildingTemplate/Sinkhole.generated.lua:13`) and the data preset (`Data/BuildingTemplate/Sinkhole.lua:15`); absent from both on 1.1.0 | `Building.lua:925`, `:1465`, `:1565` read the flag, same text as 1.1.0 `:914`, `:1445`, `:1545` | confirmed; the brief's "class" is the generated `Sinkhole`, not `SinkholeBase` (`Fireflies.lua`), which never carried the flag |
| `Fix_TradeRocketFuelRefresh` | `OnModifiableValueChanged` refreshes any landed rocket with cargo (`UniversalRocket.lua:1922-1926`); `SavegameFixups.ZZZ_UpdateRefuelRequests` (`RocketCompatibility.lua:1139-1144`) | fixup enrolment §3; the module is a wrapper, not a copy (Phase A), and declined on the on-leg by a probe throw (`:90-91`) | confirmed |
| `Fix_TrainCargoDumping` | rewritten `Train:UnloadAll` (`Train.lua:787-831`), `room_for` checks `IsResourceEnabled` (`:789-793`) | the unload call | confirmed; module declined on the on-leg (`:99`) |
| `Fix_TrainsToVoid` | `OnMsg.BuildingDemolished` calls `train:DestroySilent("station", bld)` (`Station.lua:293`) | station demolition | confirmed |
| `Fix_TrainWaitTime` | `BoardVehicle` resets `transport_ticket.start_wait` after `AddSpentTime` (`ColonistTransport.lua:624`) | the ticket clock | confirmed |
| `Fix_WispRewards` | `SetLightTrapMode` (`Fireflies.lua:712-738`): research grant removed, `* 1000` added — our two edits exactly | the mystery's trap mode | confirmed; inert while it ships |

Added by this adjudication: `Fix_FounderTraitNotification` (§6, F126).

## 3 · The two gates

**Open Pasture — cleared, and the clearance survives the A/B's limits.** The module's own
`Require` test reads the shipped class and entity spot lists (`Code/Fix_OpenPastureStockpiles.lua:133-149`)
and declined on the on-leg (`ck208on_…:135`). That is a data probe of the shipped asset, not a
behaviour comparison, so neither limit of the run touches it: the zero-error gate is about
other lines, and the mixed mod set matters only if a loaded mod alters that entity. Neither
extra mod does — a grep for `pasture`, `ranch` or `OpenAir` over the Train Hub dev mod's
`Code/` finds one comment line about `Train:TransferCargo`, and over the Opt-In pack's `Code/`
one comment in `00_Core.lua`; the Train Hub mod's `Entities/` holds hub entities only. The
native migration was re-read (§2): present, absent on 1.1.0, enrolled by the fixup mechanism.

**Corrected 2026-09-23 by the build audit (`GAMEPATCH_1.1.1_AUDIT_2026-09-23.md` §5): the
clearance above is narrower than written.** The probe it rests on
(`16ff1aa:Code/Fix_OpenPastureStockpiles.lua:132-148`) returns `false` at the first of
`Resourcepile7..9` whose closed-entity range is missing or whose open-entity range exists, so
the retail decline proves that `OpenPasture_Open` differs from the nine-versus-six shape at
one or more of those spots, not that all three were added. The Lua tree cannot show entity
spots (`_EntityData.generated.lua` is byte-identical across the two builds), and nothing
native re-homes piles at runtime: `RebuildPastureStockpilePool` (`Animals.lua:1382-1560`) runs
only from the two save fixups (`:1569-1583`). The Lua and save-migration half of the gate
stands; the asset half is UNPROVEN until the three spots are read in-game (ck211).

**Trade rocket — settled at the desk.** `FixupSavegame` (`CommonLua/SavegameFixup.lua:24-48`,
called from `CommonLua/Savegame.lua:809` on load) iterates every `SavegameFixups` entry in
name order and runs each one absent from the save's `AppliedSavegameFixups`, then marks it.
That table is pre-filled with every known fixup only for a new game (`:10-16`). A fixup new
in 1.1.1 therefore runs once on any older save's first load: *enrolled*, not merely present.
Residual, SOURCE only: the fixup acts on `UIColony.labels.AllRockets` members that are
`UniversalRocketBase`, not player-controlled, with cargo, and landed; a loading trade rocket
is landed by `IsRocketLanded`'s definition (the module header, `Code/Fix_TradeRocketFuelRefresh.lua:20-22`).
The REMOVE brief's clause was annotated; its runtime check is confirmatory.

## 4 · The retail A/B and what survives its limits

Verified from the archived logs, not from the report: off-leg loaded mod items = TestKit only
(`ck208off_…:96`); on-leg = TestKit, Fix Pack, Opt-In, Train Hub dev (`ck208on_…:202`);
totals `31/36/26/5` and `61/11/23/3` (`:573`, `:969`; each sums to 98); `logscan` re-run on
the archived copies: 6 and 46 error-shaped lines, matching the report. Census: the on-leg
prints "fix pack present: 46/52 fixes active" (`:294`); by unique module name 49 print
`applied` and 7 print `inactive`, four print both (data patches that apply at registration
and decline at data-ready), and `SaintBlessing`'s inactive line (`:150`) is transient — its
re-base arms at `:172` and its probe passes at `:447` — so the six inactive at census are
`BuildingCodesPrefab`, `CloggedBuildingRelease`, `OpenPastureStockpiles`,
`SinkholeIndestructible`, `TradeRocketFuelRefresh`, `TrainCargoDumping`. 46 + 6 = 52.

| claim drawn from the run | survives? | why |
|---|---|---|
| Open Pasture gate cleared | yes | §3: a shipped-asset probe, unconfounded |
| F123 pack-on 100 vs 50 | yes, as pack-on | deterministic arithmetic; no extra mod names the function |
| F123 pack-off | no — never measured | the probe printed "fix pack not loaded (bug reproduces)" without calling the function (`ck208off_…:277`); the entry and report say so |
| module apply/decline outcomes (46/52, the six declines) | yes | facts of that configuration; a decline is a `Require` result, not a suite result |
| clean boot, retail compatibility, release readiness | no | neither leg met the zero-error gate; the on-leg carried two extra mods; the report claims none of these |

**Record gap, corrected.** `d45655c` cited `Mars.exe-20260923-10.39.06-6aad2d75.log:135` in an
entry, a brief and the report without archiving it, while the game keeps about twenty logs;
both legs are now in `docs/archive/logs/` (`083cf2b`). No record overstates the run: the F123
evidence field says "pack-on … pack-off short-circuited"; the report's §4 says "not a
single-variable A/B" and "no clean-boot … claim"; the REMOVE brief says "bounded results".
The report's `[x]` on work item 6 ("launch line … and logscan") is fair: both were done.

**Needs a focused re-run** (owner play, after the FIX/REMOVE work): F123's two-sided control
after removal; a clean-boot census with the pack alone; the track unit's repair-site salvage.

## 5 · The three FIX premises

- **F121.** The retained load-only half survives the whole-tree search (§1): no shipped
  migration clears the reason, and the Duration thread is created only at firing. The FIX
  brief's falsifying read is annotated with this result; it remains worth re-running by the
  builder, since the tree it reads is the same one.
- **F124 / F125.** Confirmed in Phase A §2.1 and §1 here. The F124 item now also owns
  `Fix_BrokenTrackSalvage`'s retirement and the `Fix_TrackSalvageRefund` wrapper re-read.

## 6 · The KEEP verdicts, at surface

Route: `bodycheck --src` on both archives (19 BODY-CHANGED, 13 DEFECT-GONE, 1 TARGET-ABSENT
on 1.1.1; none on 1.1.0), the patchcheck block, and the Phase A population. Rows whose
instruments moved were opened; the rest stand as the triage's reads.

**Escalated and corrected: `Fix_FounderTraitNotification` → REMOVE, F126 filed.** bodycheck
reports its pin TARGET-ABSENT and patchcheck reports the handler "moved+body" to
`Factions.lua:1466` — which is a different handler on the same message (Dictatorship's
renegade check, `:1466-1473`), not the Founder notification moved. The triage read that far
and kept the module because "no working Founder notification replaced it". What it did not
read: the `FounderGainsTrait` notification preset is gone from `Data/NotificationPreset.lua`
(0 files on 1.1.1, 2 on 1.1.0). The vendor deleted the feature. Our additive handler still
fires (`ck208on_…:115`, `:421`) and asks `AddNotification` for an id that no longer has a
preset; the engine asserts and builds the instance from the base class
(`CommonLua/Libs/Notifications/Notifications.lua:32-48`). The retail PASS at `:421` does not
see this: the probe stubs both globals (`40_Probes_Wave4.lua:985-1012`). WORKFLOW's own rule
applied here: a zero-hit grep for the old name proved a deletion only once the capability's
preset was searched too. Filed at P3; the REMOVE brief gained the row.

Other rows opened, all KEEP confirmed:

- `Fix_BombardmentSpread` (BODY-CHANGED, DEFECT-GONE): Phase A §2.1 — a dead-code cleanup;
  manifest hygiene owed.
- `Fix_DryFarmingFarms` (DEFECT-GONE on `Data/Tech.lua`): the regex's negative lookahead
  excludes `FarmSmall`, which 1.1.1 added to the effect list, so the router now reports a
  false "gone" for a defect the triage shows is three-quarters present. Hygiene: restate the
  regex against the three still-missing farms.
- `90_SaveSanitizer` (DEFECT-GONE on `A_StationConnectorElements3`): the F48 paren already
  triaged in D14; unchanged since 1.1.0 (same row on the 1.1.0 run).
- `Fix_HabitatExpeditionDraft`, `Fix_HabitatExpeditionReturn`, `Fix_RocketInteractGuard`
  (BODY-CHANGED under wrappers): the diffs are a Child filter for expeditions
  (`CargoTransporterNew.lua:242-244`), `ValidateWorkplace` in place of `ValidateBuilding`
  plus a type guard (`Colonist.lua:1809`, `:1822-1824`), and `IsValid(obj.shared_depot)`
  (`RCTransport.lua:438`); none touches what the wrappers add.
- The six identical-target copies and `Fix_ExtenderFlapChurn`: Phase A §2.2.

## 7 · The two follow-up briefs

Clauses that could not fire as written, and what was done:

- **REMOVE, `Fix_BrokenTrackSalvage` row.** Its premise names a body that does not run in the
  pack until F124. Row removed; a dated note explains the move; the FIX brief's F124 unit
  absorbs the retirement (Phase A §3). The set is still fifteen because
  `Fix_FounderTraitNotification` joined it.
- **REMOVE, trade-rocket clause.** Discharged at the desk (§3); annotated, runtime check kept
  as confirmatory.
- **REMOVE, prompt-map row.** Still said "gated on the Open Pasture asset and trade-rocket …
  controls" after `d45655c` cleared the first; rewritten.
- **FIX, F124 item and scope.** Widened to the unit; the F121 falsifying read carries the
  adjudication's result. Nothing in the FIX brief was falsified.
- **Phase A's population correction** falsifies neither brief: `Fix_TradeRocketFuelRefresh`
  stays REMOVE as a wrapper; the two added full-body modules are KEEP rows with hygiene items.

## 8 · The `bodycheck.py` self-test change

`c7266f0` rewrote the OK control from asserting F46's expression (which 1.1.1 repaired) to a
patch-stable regex on the declaration line itself. The question was whether the self-test can
still fail. Measured, desk: two copies of `tools/bodycheck.py` were broken in a scratch
directory (the working copy's sha256 `abcc9339…` was checked unchanged before and after) —
variant A makes every pin read BODY-CHANGED (`got = "0" * 64`), variant B makes every
`DEFECT:` read DEFECT-GONE (`if False:` at the regex search). `--selftest` on the real tool:
PASS, exit 0. Variant A: three FAIL rows, exit 1. Variant B: exactly one FAIL row,
`Fix_SelftestOk` (expected `OK`, got `DEFECT-GONE,OK`), exit 1. So the rewritten control is
precisely the row that catches a regex engine that never matches, and the hash half is caught
by the same row plus two others. **Verdict: confirmed, the control can fail.**

Residual, stated: the Train row no longer asserts that a *gameplay* defect expression is still
shipped; that duty now rests on the DataPatch fixture alone (`modify_trait = "Religious"` on
`Data/TraitPreset.lua`, F-1's premise). If a later patch repairs the Saint preset, that row
will need the same treatment, and the self-test will then have no real-expression OK control
left. Worth a fixture from a defect the vendor is unlikely to touch, when someone is in the file.

## 9 · The opt-in outbox row

The brief's premise is unproven: there is no `<<PENDING-RUN>>` in the opt-in outbox entry
(`SMR-OptInPack/docs/agent/prompts/perma/gamepatch/1.1.1.405907_2026-09-23.md`, committed
`d372c1f`), in the fix-pack triage report, or in F121–F125. The only pending-run markers in
the opt-in tree belong to the Train Hub prototype report. The triage's own unfinished row was
work item 6 ("launch line … pending owner"), which `d45655c` completed. What the outbox entry
does owe, and to whom: a body read in both trees and a KEEP/FIX/REMOVE verdict filed in the
opt-in `bugs/` for its three flagged modules (`AcknowledgedWarnings`, `DroneStatDials`,
`MultipleSuns`), by the opt-in seat's own game-patch job. Nothing was written there from here.

## 10 · ck207, as the owner will read it

It states the 12-module / 1,000-declaration proposal with the routing numbers behind it
(M=43, T=315, B=0, D3=0, verbatim from the patchcheck block) and is honest that the
declaration limit went unexercised. Two things were missing and are now in the item:

- the one datum that shows the full read was *necessary*, not merely forced:
  `Fix_OpenPastureStockpiles` had no patchcheck row at all and is a REMOVE, because vanilla's
  repair is a save fixup outside every body it pins;
- the A/B bullet was stale: it asked for the A/B to run first, and it has, bounded — a
  focused re-run after the FIX/REMOVE work is the real gate.

Is "stop the deep sweep here" still sound? As sequencing, yes: nothing the A/B returned
bears on a tree-wide search for new vendor defects, and this adjudication's two population
corrections were both modules the triage had already read and classified correctly. The
2–3 session estimate remains unmeasured, and the item says so. The ruling is the owner's.

## 11 · What the owner must decide

1. Fire the FIX brief with the track unit first (Phase A §4 ranking), or reorder.
2. Accept the REMOVE brief's changed set: `Fix_BrokenTrackSalvage` out (to F124),
   `Fix_FounderTraitNotification` in (F126, filed P3; raise it if a blank notification is
   worse than that).
3. ck207 as amended.
4. Three manifest-only hygiene items in `Code/` comments, which this brief could not touch:
   restamp `Fix_BombardmentSpread` after the Phase A read; pin
   `DroneHubExtenderBase:UpdateUplinkRequesters` in `Fix_ExtenderFlapChurn`; restate
   `Fix_DryFarmingFarms`'s DEFECT regex. Cheap to fold into whichever brief fires first.
5. The opt-in seat owes its three-module read (§9).

## 12 · Claim limits and not opened

- Every vendor-side statement is SOURCE on the archived trees; this seat ran nothing in the
  game. The census and F123 lines are the owner's unattended run with the limits in §4.
- "Enrolled" for the trade-rocket fixup is a read of the applier, not a load of a 1.1.0 save.
- F126's player-visible shape is unobserved; its mechanism is SOURCE and its trigger is
  measured through stubs.
- Not opened: the fifteen REMOVE modules' TestKit probes (the brief's own item 5); the
  `ProcessAllElements` consumers beyond the split body; the `MigrateStep` intermediate-leg
  path beyond its threshold line; whether `assert` prints in a retail log (it did not appear
  on the on-leg because the probe stubbed the call, not because it was silent).
- Stops: none triggered. No newer build landed; Phase A did not falsify the full-body
  framing (it corrected membership, not the class); no shared path had peer changes.
