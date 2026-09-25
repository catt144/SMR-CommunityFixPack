# hubset 99 — adversarial audit of the hub release set

## Must_Read_Header

Reader: the owner giving or withholding the go on the hub release set, and the merge session
acting on it. Verdict for the set: **SHIP WITH CHANGES**. Every change is named in §2, each is
small, and none needs another sitting. One change, C42, is the owner's decision under the
chain's "bring the owner the facts" ruling and FIX_POLICY §4; the audit recommends dropping it.
Audited on `main` `527a9cb` and `hubset` `7f6e6bf` (worktree `B:\Dev\SMR\SMR-BugFixPack-hubset`),
game source archived 1.1.1.405907, 2026-09-24, on Fable (the builds were on Codex). Method: four
tier-2 auditors on disjoint members plus the sittings, each cleared by one source check in this
seat; every harness, gate and ruling check re-run in this seat.

## 1 · Verdict and what it rests on

**SHIP WITH CHANGES.** Seven of the eight members repair a defect that exists on the archived
source, by the shape their entry states, with `Require` pairs on the declaring class, a
manifest pin that bodycheck reads OK, and a desk harness whose fix-removed control fails. Two
of them (C114, C117) were also discriminated in play in 07B, fix off and fix on, and one (C111)
was watched working by the owner. No two members wrap the same target, and no harmful
interaction was found on the traversal or rescue chains. The eighth, C42, repairs a defect that
cannot occur on any archived build.

Measured in this seat, worktree at `7f6e6bf` (each command `python tools/<harness>` from the
worktree; totals quoted from the run):

| harness | result | fix-removed control |
|---|---|---|
| `desk_c42_passage_stale.py` | 11 of 11 demands held | built in: "without the fix, the stale member is kicked" PASS |
| `desk_f127_arrival_booking.py` | 12 of 12 demands held | built in: full dome and full habitat, plus the old reserve-only mutant |
| `desk_c83_arrivals.py` | 12 of 12 demands held | (C83 regression, unchanged) |
| `desk_c111_rescue_text.py` | 11 PASS, 0 FAIL | `--without-fix`: 2 FAIL, exit 1; `--module-revision 7cf48a2`: 3 FAIL, exit 1 (the 07 refutation reproduced) |
| `desk_c115_home_rescue.py` | 12 PASS | built in: "fixed demand fails with module absent" PASS |
| `desk_c117_hub_salvage.py` | 17 of 17 demands held | built in: native outside branch after the same disconnect |
| `desk_c114_hub_access.py` | 25 of 25 demands held | built in: five "module removed" demands |
| `desk_c114_sitting_findings.py` | HELD (native false, fixed true at 24/25/28/29 hexes; controls false/false) | printed beside each row |
| `desk_c116_hub_marker.py` | 11 PASS | built in: "module-removed walk remains marked" PASS |
| `desk_hubset07_rehearsal.py` / `07b` | 58 of 58, 48 of 48 | declared VOID by design (fixtures only) |

Gates on the branch: `parsecheck.py` 44 files, 0 errors. `bodycheck.py --src <archive 1.1.1.405907> --all`:
every row for the eight members OK (ArrivalDeaths 15, HubLocalAccess 2, HubMarkerDeparture 2,
ObsoleteHomeRescue 2, PassageHubSalvageDrain 4, PassageStaleHolder 4, RescueReturnText 4,
VacuumWalks 6 incl. the two P3 pins); `Hubset_OnHubNow.lua` is a declared `SRC: none` helper
(NO-DEFECT, acceptable: it corrects nothing). The four non-OK rows (BODY-CHANGED
`Fix_HabitatExpeditionDraft`, `Fix_HabitatExpeditionReturn`, `Fix_RocketInteractGuard`;
DEFECT-GONE `90_SaveSanitizer`) are identical on `main` and belong to no member.
`harvest_wrap_targets.py --check`: 0 wrap sites outside Require. doccheck GREEN on both trees.

Rulings: `git log --oneline d6667dc..main -- Code metadata.lua items.lua` prints nothing
(positive control: 25 commits on that range overall), so no set code reached `main`. The
branch's `metadata.lua`/`items.lua` diff is code-list insertions only; "load order" in
`e11a131` and `LOAD_ORDER_CROSSCHECK_2026-09-24.md` means the pack's position among other mods,
untouched, and the VacuumWalks load-time guard is untouched (its diff is four comment lines).
The mod junction points at `B:\Dev\SMR\SMR-BugFixPack` (`main`). C111's wording carries the
owner's verbatim "the wording is fine" (C111.md, commit `527a9cb`); its source is the agent's
transcription, no owner-side artifact holds it, and ck216 was still open at audit time (removed
at this close-out, §5).

## 2 · The changes (SHIP WITH CHANGES)

Each is small and desk-verifiable. Items 1 and 3 need the owner's word; 2 and 4 are applied on
the branch by this link and re-run.

1. **C42 — owner decision; recommended: drop the module from the set and record C42
   `wontfix — unreachable`.** CONFIRMED on the archived 1.0.7, 1.1.0 and 1.1.1 trees:
   `Lua/Passage.lua:819` (1.1.x; 1.0.7 :733) sets `PassageGridElement.OnEnterUnit = empty_func`,
   and `LeadIn` reaches a holder only through `OnEnterUnit` (`BuildingWayPoints.lua:489-497`).
   The only writer of a `units` list is `Holder:OnEnterHolder` (`Holder.lua:27`), called only from
   `Unit:SetHolderOnMap` (`Unit.lua:819`); of 42 `SetHolder` call sites none passes a passage
   element (`Passage.lua:1227` passes the hub). So no colonist ever enters an element's `units`,
   the stale member C42 prunes cannot exist, and its harness inserts one by hand (`desk_c42_passage_stale.py:90`)
   without loading `:819`. Reachability tier R4. FIX_POLICY §4: "R4 does not ship: record it
   `wontfix — unreachable` with the search that proved it." The 07 census agrees:
   `boot_c42stale elements=271 entries=0 stale=0` after 41 and 66 walkers of traffic. The module
   is a no-op (first action `IsKindOf`, `units` never a table on an element), so it harms nothing
   at runtime; the harm is the record and the in-game title claiming a repair. Hubset 03 asked the
   owner to hold or retain C42 and no ruling is recorded; the scope cut set testing scope only.
   If the owner keeps it, the entry, title and `DEFECT:` pin (`unit:KickFromBuilding\(self\)` pins
   correct vanilla behaviour, the phrasing §2b forbids) must still change.
2. **C115 — call the original after the cleanup** (`Code/Fix_ObsoleteHomeRescue.lua`):
   `task:Cleanup()` then `return orig(self, dest_dome, ...)` instead of a bare `return`.
   Behaviour-identical: native `Transport` opens with `if not self.transport_task then return end`
   (`Colonist.lua:3964`) and `Cleanup` has just set it false (`LRTransport.lua:78-80`). It restores
   §1.4 "always call it" and keeps another mod's earlier `Transport` wrapper in the chain.
3. **C117 — count only valid traversers in the extended wait** (`Code/Fix_PassageHubSalvageDrain.lua`;
   applied on `hubset` after the second-seat review, see §5). A dead colonist whose traversal
   errored leaves its list entry (the native fixup `SavegameFixups.InvalidColonistsInPassages`,
   `Passage.lua:2627`, exists for this and runs once per save). On the played revision `7f6e6bf`,
   with a usable sibling, such an entry held the module's pre-disconnect wait indefinitely: the
   spoke stayed connected and every fresh entry was refused until the entry cleared. The guard's
   benefit is exactly that: an invalid entry no longer holds the wait this module adds, so the
   disconnect proceeds as shipped. It does not repair the inherited hang: native's own
   post-disconnect wait (`Passage.lua:1182`) still counts the unfiltered list, and the pre-disconnect
   predicate (`:1139`) has the same unvalidated count on the last exit; both are left as shipped.
   Desk: an invalid entry alone returns false, a live entry beside it returns true, the old-shape
   mutant (the played count) returns true on the invalid entry alone, and native returns false
   regardless. It changes the revision 07B played by a guard that returns true in fewer cases.
4. **C111 — add the probe's stub-contract comment** (`Code/Fix_RescueReturnText.lua`).
   `00_Core.lua:172-177` requires every probe to name what the stub must provide and why the
   target is safe to call on one; the C117 probe has one, the C111 probe does not. Comment only.

## 3 · Member findings (beyond the changes; recorded in the entries at this close-out)

- **C114** (`Fix_HubLocalAccess.lua`). The `hub_domes` loop is live: the field is a hybrid
  list-plus-map (`PassageHub.lua:10-12`, maintained at `Passage.lua:1436-1439`, `:1594-1599`), so
  `ipairs` yields each dome and `attached[dome]` is its passage count; a list-only or map-only
  fixture drops the harness to 19 of 25. Requires name the declaring class
  (`ColonistTransport.lua:270`). Covers hub-attached passages only, not dome-to-dome passages
  (the title's "in a passage beside a large dome" is wider than the fix). The entry's "Idle
  wrapper books the rescue" misattributes: the booking is in `Colonist:SetCommand`
  (`ColonistTransport.lua:382` on). 07B: `booked=true ended=ready_for_pickup` on `main`,
  `booked=false ended=safe in_dome_now=DomeMedium(3911)` on `hubset`, matched inputs
  (`exposed=true hub=PassageHub(2692) nearest=DomeMedium(3911) nearest_reach=false dist_hub=29`),
  two different subjects. The fixed subject entered a different dome than home, which the judge
  accepts and the 07B brief's "walks home" wording over-states. No owner observation of the
  outcome exists: the owner screenshot is the pre-fire "Going to work", and SMRTK_0079 is an
  automatic capture. Interaction with C117: while a spoke drains, its dome
  stays in `hub_domes`, so C114 grants access and C117 refuses the entry; failed walks instead of
  a rescue until the drain ends. Bounded by the drain once change 3 is applied; on the played
  revision an invalid leftover traverser made that drain, and so this interaction, persist until
  the entry cleared (second-seat review, 2026-09-24). Nit: `Fix_HubLocalAccess.lua:70-71` is a tab short.
- **C116** (`Fix_HubMarkerDeparture.lua`). `Unit.Step` is replaced before classes build and `Unit`
  is flattened (`Unit.lua:4`), so a live Colonist dispatches through it; `StopMoving`
  (`Colonist.lua:2963`) and `SetHolderOnMap` (`:3186`) are declared on Colonist. `departed()`
  cannot strip a real ramp: tunnel endpoints sit on the hub's own hex (`Passage.lua:247-257`,
  `:1655-1658`) and the ramp runs inside the traversal. `SetHolder(false)` is native
  `SetHolder()` (`Unit.lua:807`). Two record gaps: the module also drops a stale `holder == hub`
  (`:64`), which the entry's fix shape does not state (05's design call, disclosed only in the build
  section, never exercised in play: P5 NOT_SAMPLED ×4); and the entry's reader list omits
  `IsColonistExposedToDisaster` (`Colonist.lua:1279-1282`, called from `DustStorm.lua:131,324`,
  `DustDevils.lua:516`), so clearing a marker also restores disaster exposure for a departed
  colonist, the right direction, undisclosed. The harness does not isolate the explicit
  traversal guard (removing it still passes 11 of 11). "reach confirmed (~11%)" in `row_status`
  and evidence is stale against the chain author's "at least ~11%" correction.
- **C115** (`Fix_ObsoleteHomeRescue.lua`). Task states and defaults verified (`LRTransport.lua:23-29`;
  states set at `Colonist.lua:2010,3986`, `ShuttleHub.lua:887,935`, `_fixup.lua:2870`). `Cleanup`
  fully unbooks (`LRTransport.lua:63-84`); the early return lands in the idle command
  (`CommandObject.lua:250,274-282`) and cannot re-book, because native `HasLocalAccess` is true
  inside home (`ColonistTransport.lua:271-275`). The `not self.holder` guard is reachable: a
  dome-side passage exit clears the holder (`Passage.lua:1232-1234`). Limits: an obsolete walk
  already in flight on an existing save is not re-checked (layer 2 by design); on 1.1.0 the
  `migration_dest` test declines the module (safe, reason string does not say branch). The
  harness rarely isolates one guard. The entry's tag ("anchor unmeasured"), `row_status`
  ("pickup anchor measured (04)") and evidence ("HYPOTHESIS") disagree three ways; the 04 anchor
  reading was taken on unfixed code by a retired sitting whose footprint verdict is void, so the
  tag is right. P2's "no regression on remote rescues" is weak: the judge counts a task already
  `ready_for_pickup` at arm as served (all 16 resolved within 5,248 game ms), so the fixed
  `Transport` entry was probably never exercised; the C115 fix path (P1) was NOT_SAMPLED ×2.
- **C117** (`Fix_PassageHubSalvageDrain.lua`). Defect confirmed (`Passage.lua:1134-1136` sibling
  shortcut, `:1181` disconnect before the traverser wait at `:1182-1184`, `:1224-1235` late
  `is_pf_tunnel` read). Shape is the entry's option 2. Refused entry goes through `Unit:TraverseTunnel`
  (`Unit.lua:238-246`, `ClearPath`, return false) and `Movable:Goto` fails the walk; no retry
  loop inside Goto. Probe verified synchronous and side-effect free; a throw declines
  (`00_Core.lua:192-206`). Unlisted caller: `DestroyBuildingImmediate` (`Building.lua:1468`) also
  reads the predicate and skips destruction while it is true. 07B counts reconcile as aggregates
  only (no per-colonist rows): `main` `at_drain=68 hub_bound=43 hub_bound_unmarked=43`, `hubset`
  `at_drain=69 hub_bound=37 hub_bound_unmarked=0 entered_after=0`; 72 traversers at the press
  on `main` against 68 at drain, 68 against 69 on `hubset` (native admission before `hub_draining`,
  invisible to `entered_after`). "unmarked" is `not (holder == hub and passage_hub == hub)`, a
  composite; `outside` was never read, so the entry's "no holder, no marker" and "left all 43
  outside" over-read the instrument. `entered_after=0` on both builds does not show the guard
  fired. Log-read only; no owner eyes.
- **C111** (`Fix_RescueReturnText.lua`). `Getui_command` declared on Colonist (`Colonist.lua:4672`),
  T 4333 at `:4647-4649`, `emigration_dome` default false (`:106,329`), display name falls
  through to the task's destination (`:4462-4465`), `Untranslated` is an ordinary T table with tag
  expansion (`CommonLua/Core/localization.lua:342-348`; shipped precedent `TrainDisasterHandling.lua:154`).
  07B `hubset` line: `emigration_dome=false returning=true text="Returning to Dome: <h ...>Brussels</h>"`,
  owner screenshot `hubset07b_B_slot1_owner.jpg` shows "Returning to Dome: Brussels"; the judge's own
  verdict is NOT_SAMPLED because the fixed text has no T id, and HELD is a manual re-read that
  the fields support. Fix-off baseline is 07's A3a screenshot ("Moving to a new Dome: Brussels").
  The real-relocation control (P12) was never sampled in play; desk only. The rescue line is
  English-only for every language, the §6 consequence. Header says layer 3; it is a synchronous
  output wrapper, loose but harmless.
- **F127** (`Fix_ArrivalDeaths.lua` C83 branch). Booking callees verified (`Colonist.lua:2223-2228`,
  `Dome.lua:3482-3493`, `Residence.lua:291-308,386-398`, `MicroGHabitat.lua:85-88`); the final
  code cancels before reserving, and the harness's old-shape mutant fails on a full habitat.
  Gaps: no rejected-habitat case; the harness stubs the habitat's refresh. Out of set, filed
  as a lead: the F53 unreachable-dome branch of the same wrapper leaves the same kind of stale
  booking (lower risk: its `ChooseDome` picks domes with free space). Hygiene: `desk_c83_arrivals.py`
  run alone reads the live install, byte-identical to the archive today.
- **P3.** Four comment lines; both pins resolve and hash OK; the wrapped bodies are in the
  module's Require. Clean.

## 4 · The sittings, the drift inbox and the rulings

**Sittings.** Every 07 and 07B verdict is supported by its log line as the judge reported it
(read-backs `build=hubset`, six `applied`/`active` on the `hubset` segments, six `absent` on
`main`; 42 versus 36 `: applied` lines). Where entry or inbox summaries go further than the
judges, §3 says so (C117 "outside", C114 "watched"/"walks home", C115 P2). Under chain rule 8
only C111 has the owner's eyes on the fix working, plus a fix-off owner screenshot; C114 and
C117 are instrument-read on both builds with the owner present but not observing the outcome;
C115 and C116 never had their fix path exercised in play; F127 and P3 are desk-only by the
scope cut. An unrecorded confound: every segment's fingerprint lists two dev-only mods
(`SMR_RailShaftDev_20260923`, `SMR_TrainHubDev_20260918`) enabled; a grep of their Lua against
the set's targets found only comments and a `Drone:Getui_command` wrapper, so no overlap, but
no entry names them. **One unexamined artifact examined here:** 07's A6 owner observation
("multiple colonists with O2 readings") is SMRTK_0074, now archived as
`docs/archive/logs/hubset07_A6_SMRTK_0074.png`: on `main`, Colonist(2000023324), home Brussels,
status "Moving to a new Dome: Brussels", issues "Suffocating, Dehydrated", beside a hub passage.
That is the own-home rescue harm of C114/C115/C111 witnessed on unfixed code, and the C115 P2
judge counted it as "served". It is evidence for the defect, not for any fix.

**Drift.** The inbox carries 21 drift bullets; every one has a record (inbox, entry or commit);
none was silently fixed. Left as found, now named: the `HexGridGetObject(..., WorldToHex(unit), ...)`
pseudo-call stands unflagged in `ON_HUB_TEST_2026-09-24.md:26,116` (the built helper is correct);
`MIGRATION_AUDIT_2026-09-24_D_hubs.md:77,89,112,353` (75,87,110,351 before the correction note) still state the `LeadIn → OnEnterUnit →
SetHolder(element)` premise that `Passage.lua:819` contradicts (annotated at this close-out);
the corrected `LoadedMaps` console lines from the retired 04 sitting survive nowhere (the
inbox's "preserved in the C114/C115/C116 sections" is false; C114 points back at the inbox);
the SMRTK.md commit-rule tension was resolved by `9fe9516` but the inbox still says unresolved;
07B's pre-sitting steps 5 and 6 and the TestKit sha/listing have no record of running; no
second-seat read of 07B is recorded (`CHAIN_METHOD.md:6`). `STATE.md` says "STILL OPEN: none"
while the checklist's Decide section holds five items (out of this chain's fence, routed to the
owner here).

**Owed work found.** 06B's dated pointer into C111, C114 and C117 (added at this close-out).
03's C42 owner ask (this report, §2.1). ck216 removal on the owner's approval (done here).
The C42 record correction 03 required "before a release verdict" (done here, pending the ruling
on the module).

## 5 · Close-out actions taken by this link (before the go)

- Branch `hubset`: change 2 (C115 delegates after cleanup) and change 4 (C111 probe comment)
  applied as `hubset` `86d03d8` and its harnesses re-run; totals in the commit message.
- Second-seat review (owner-relayed, 2026-09-24) agreed SHIP WITH CHANGES, recommended dropping
  C42 and applying change 3, and corrected two claims of this report: the C117 guard's benefit is
  confined to the module's own wait, and the C114/C117 interaction was unbounded on the played
  revision. Both corrected in §2.3 and §3. Change 3 applied as `hubset` `bd4d9dd`
  (`desk_c117_hub_salvage.py` 21 of 21, old-shape mutant included). C42's drop and the merge
  still wait on the owner's go in words.
- `main`: this report; entry corrections named in §3 for C114, C115, C116, C117, C42 (record
  only), F127; 06B pointers; ck216 removed; SMRTK_0074 archived; the D_hubs premise annotated.
  Statuses are not changed before the go; §6 lists the statuses the evidence supports.

## 6 · On the owner's go

Status each entry will receive, from its evidence: C111 `tested-attended` (owner watched the fix
on, owner screenshot of the fix off); C114 and C117 `tested-unattended` (instrument-read on both
builds in 07B, owner present, outcome not observed by eye); C115, C116, F127 `fixed` (desk, fix
path not exercised in play); C42 per the owner's ruling (`wontfix — unreachable` if dropped);
P3 has no entry. Then the merge, doccheck, one `### Pending` per player-facing member (C111,
C114, C115, C116, C117, F127; C42 if kept; not P3), worktree and branch removal, and the chain
folder's terminal lifecycle. The owner's questions, in words: (a) drop C42 or keep it; (b) apply
the C117 valid-count hardening or ship the revision 07B played.

**Next chain:** none is queued. The natural next item is the load-order decision the owner
deferred until after the fixes (`e11a131`, `LOAD_ORDER_CROSSCHECK_2026-09-24.md`).

## 7 · Close-out record (owner's go, 2026-09-24: "Go with the recommendations")

- `hubset` `acd89f0` dropped `Code/Fix_PassageStaleHolder.lua` and its two registrations; C42 is
  `wontfix — unreachable (R4)`. The 07/07B rehearsal harnesses and the TestKit slot file
  `80_AgentSlots.lua` still name `PassageStaleHolder` in their read-back fixture list; both model
  the sittings as played and are left as records.
- Merge `8cb1727` (`git merge --no-ff hubset`, no conflicts: the branch touched only `Code/`,
  `items.lua`, `metadata.lua`, `tools/`). Post-merge on `main`: parsecheck 43 files 0 errors,
  MODULE SETS agree (43 files, 41 registered), WRAP CHECK 0 outside Require, doccheck GREEN.
- Statuses set at `3eb0a43`: C111 `tested-attended`; C114, C117 `tested-unattended`; C115, C116,
  F127 `fixed`; C42 `wontfix`.
- This close-out commit: `tools/desk_c42_passage_stale.py` retired with the tool catalog
  regenerated; six `### Pending` entries appended to `RELEASE_OUTBOX.md` (C114, C115, C116, C117,
  C111 as new rows; F127 as a respecification of the C83 row); the chain README archived to
  `docs/archive/prompts/hubset/README.md`; the `hubset/` map row removed; `99_AUDIT_high.md` and
  the live README `git rm`'d; worktree `../SMR-BugFixPack-hubset` removed and the local `hubset`
  branch deleted (`origin/hubset` left for the owner).
- The upload is the owner's, through `release_prompt.md`. Nothing was pushed.
