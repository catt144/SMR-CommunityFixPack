# hubset 99: adversarial audit, then the merge on the owner's go

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first. Fire only
when this file and the README are the only files left in `docs/agent/prompts/hubset/`. Run in fresh
context, on a different model or vendor from the one that built the links (owner routing: the builds
on Codex, this audit on Fable).

## Authority and outcome

Your job is to disbelieve the chain. Trust no link's summary, including its outbox and the entries'
build sections; check each against primary evidence (the branch diff, the archived `1.1.1.405907`
source, the desk harnesses re-run, the archived sitting logs). End state: a report at
`docs/agent/reports/HUBSET_AUDIT_<date>.md` with one verdict for the set: **SHIP**, **SHIP WITH
CHANGES** (each change named, small, and not needing another sitting) or **NO SHIP** (with what
would make it shippable). Then the close-out below. Open a live todo list before the first write.

## What to audit

- **Every member against its entry.** For C114, C115, C116, C117, C42, C111, F127 and P3: does the
  module fix the defect the entry states, by the shape and guards the entry and the resweep require,
  and nothing wider? Re-run each desk harness on the branch, and confirm its controls fail with the
  fix removed.
- **FIX_POLICY.** Technique ranking (§1), `Require` checks, MANIFEST pins and stand-down (§2), save and
  blocking-frame disposition (§3a), localisation (§6). Run `tools/bodycheck.py` on the branch.
- **Interactions.** C42, C116 and C117 all touch passage traversal, and C114, C115 and C116 all touch
  the rescue chain. Look for two members wrapping the same target in a noncommuting order, or one
  assuming state another changes.
- **The sitting.** Sample 07's verdicts against its archived logs. Every `tested-attended` needs the
  owner's observation in the log.
- **Drift.** Every instance in your inbox: was it routed or silently fixed?
- **The rulings.** Nothing from the set reached `main`'s `Code/`, `metadata.lua` or `items.lua` before
  this link. No load-order change is in the branch. C111's wording carries the owner's approval, or is
  flagged as still unapproved.
- **Owed work.** Anything a link said it would do and did not.

## Close-out

- **NO SHIP:** commit the report, route the verdict and its remedies to the owner, and leave the branch
  and worktree in place. Archive this README and remove the chain folder only when the owner closes the
  effort.
- **SHIP or SHIP WITH CHANGES:** give the owner the verdict and wait for their go in words. On the go:
  merge `hubset` into `main` (`git merge --no-ff hubset`, resolving `metadata.lua` and `items.lua`
  against anything `main` gained); run doccheck GREEN; append one filled `### Pending` entry per
  player-facing member to `docs/agent/prompts/perma/RELEASE_OUTBOX.md`, per its rules (P3 has no player
  surface); set each entry's status from its evidence; remove the worktree
  (`git worktree remove ../SMR-BugFixPack-hubset`) and delete the branch after the merge commit lands.
  The upload itself is the owner's, through `release_prompt.md`.
- Then the README's terminal lifecycle: archive it, remove the `hubset/` map row, `git rm` this file,
  and leave no live chain folder. End the report with the next chain's kickoff line, or say none is
  queued. The load-order decision the owner deferred until after the fixes is the natural next item;
  name it.

## Notes from upstream

### From hubset 01, 2026-09-24 — build and drift inbox

- Branch/worktree: `hubset` at `795aefa`, `B:\Dev\SMR\SMR-BugFixPack-hubset`. Main evidence
  landed through `6227f2f`. The four built members and subagent reports are in
  [the fan-out plan](../../reports/hubset/agents/PLAN_2026-09-24.md); P3 has its own
  [dated build record](../../reports/hubset/P3_BUILD_2026-09-24.md).
- P3 adds only two `SRC:` pins to `Fix_VacuumWalks`; archived 1.1.1.405907 bodycheck returned
  6 OK for the module. This verifies shape, not wrapper composition.
- C42's `Fix_PassageStaleHolder` mitigates teardown kicks by filtering invalid or mismatched
  passage-element members before the native Holder method. The raw `unit.holder = nil` in
  `TraverseTunnel` still creates stale entries. The desk held 11/11, including fix-absent harm;
  C42 stays `filed` pending play and an audit of whether the narrower mitigation suffices.
  Inspect its interaction with C116 and C117 when they touch traversal.
- F127's repaired `Fix_ArrivalDeaths` C83 branch cancels the rejected booking before reserving
  in a new destination. The archived desk held 12/12; the existing C83 desk held 12/12.
  F127 is `fixed` pending attended play. **Drift instance:** the first build only called
  `new_dome:ReserveResidence`, which left an orphan in a full Naturalist Habitat because its
  method cancels only when a slot is free. The final desk includes full-habitat and old-shape
  mutant controls. Audit the final code and those controls, not the initial passing matrix.
- C111 wraps only the synchronous UI getter. Proposed exact own-home wording for owner
  approval: `Returning to Dome: <h SelectEmigrationDome InfopanelSelect><em><EmigrationDomeDisplayName></em></h>`.
  Real relocations retain shipped T ID 4333 and the destination link. Checklist ck216 owns
  approval; `cand` remains until that word and attended play. Desk 8 pass and fix-removed
  own-home control fails; retail rendering and real save/reload are untested. Flag the wording
  as unapproved if ck216 is still open at audit time.
- Branch and main doccheck were GREEN after these builds. Link 07 still owes all in-game
  verification; no desk result is a play verdict. No load-order change or release surface was
  made. The ignored `local/` evidence folders had to be created empty in the new worktree for
  its inherited `local/README.md` gate; main's evidence stayed in main's `local/`.

### From hubset 04, 2026-09-24 — sitting measurement and drift inbox

- **Attended, fired before 05.** TheGodUncle's save (`New Horizons 2 83`), game `1.1.1.405907`,
  junction on `main` (unfixed code — none of this exercised the `hubset` branch), Passage Network
  off. Two console passes roughly eleven real minutes apart. Log archived at
  [`docs/archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log`](../../archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log).
  Full readings and verdicts are in [C114](../../bugs/C114.md), [C115](../../bugs/C115.md) and
  [C116](../../bugs/C116.md)'s 2026-09-24 sitting sections; summary below.
- **S4 (C114/C116 footprint) refuted, both passes.** 80 then 140 held units across four hubs, zero
  at `none`/`dz 0`. Discriminator handed to 05: hex ownership (hub or connected passage) OR
  `dz > 0`. Reconciliation (category counts sum to `held`) passed both times.
- **C115 anchor confirmed live**, independent of the desk harness: two colonists on the unfixed
  code showed the exact obsolete-pickup shape (physically at a dome hex, stored anchor at a passage
  hex, far apart) — one pre-departure (`outside false`), one mid-fatal-sequence (`outside` timer
  running, marker already gone), matching the field findings' colonist `2000011174` pattern.
- **C116 marker lifetime: reach confirmed (~11% of marked colonists indoors, far from their hub,
  both passes), but the harmful outside/vacuum combination was not observed in either pass** — every
  stale-marker case found was indoors. Audit that 05/07 don't over-read "reach confirmed" as "harm
  confirmed"; the entry itself is explicit that these are separate claims.
- **Drift instance:** the three per-hub console lines this link shipped with (footprint, markers,
  anchors) called a bare global `MapGet(...)`, which does not exist in this build — `MapGet` is a
  method mixed onto map objects only (`CommonLua/Core/map.lua:14`), called everywhere in the
  archived tree as `<map>:MapGet(...)`, aggregated over the global `LoadedMaps` array. The owner hit
  this live (`attempt to call a nil value (global 'MapGet')`) on the very first corrected-line
  attempt; corrected at the keyboard by wrapping each query in `for _, mp in ipairs(LoadedMaps) do
  ... mp:MapGet(...) ... end`. The desk "smoke-run" this link's own prompt claimed did not exercise
  a live map instance and so did not catch it. Corrected text is preserved in the C114/C115/C116
  sitting sections above (each cites the exact lines run); the retired prompt file itself was not
  hand-edited since it is `git rm`'d at this link's own close-out. Audit whether other
  "parsed and smoke-run on the desk" claims in this chain got the same kind of non-exercising
  smoke-run.
- **Drift instance:** the prompt's instruction to rerun the anchor line "when a colonist's status
  shows 'Moving to a new Dome: Brussels'" was operationally infeasible — that status only appears in
  a selected colonist's info panel, with no notification or log surface, making a manual watch
  across ~867 colonists impractical. It was also unnecessary: `Colonist.lua:4647-4649` shows that
  status is generated whenever `cmd` is `Transport`/`TransportByFoot`/`MigrateStep`, which is
  exactly the population the anchor query (`t.dest_dome == c.dome`) already selects on every run —
  both passes already had full coverage of it. Audit whether 06/07 (which also carry attended
  in-game observation steps) have similar asks that should instead be phrased as "this is automatic,
  no watching needed."

### From hubset 02, 2026-09-24 — C115 build and drift inbox

- C115 branch commit `5a27e25` adds `Code/Fix_ObsoleteHomeRescue.lua`, its desk harness and
  registration; `52b6449` tightens the valid-home guard. Main's
  [C115 build section](../../bugs/C115.md) records the source route and
  §3a disposition. The branch and main doccheck gates were GREEN at close-out. C115 is `fixed`
  pending attended play and this audit; no code from the set landed on `main`.
- The wrapper bypasses only a task owned by the colonist, directed to its recorded home, with no
  source dome, shuttle, migration destination, departure rocket or emigration destination, an
  uncommitted task state, a valid home and a no-holder physical `IsUnitInDome` result equal to home. It calls
  native task `Cleanup` synchronously. Otherwise it returns native `Transport` directly. Audit
  whether this discriminator covers the real rescue without affecting later tasks or C111's
  synchronous command text. `bodycheck` gave two OK rows on archived 1.1.1.405907.
- The desk loads archived `Transport`, `WaitTransport`, `ColonistTransportTask:Cleanup` and
  `IsUnitInDome`. Obsolete skips the walk; remote, committed and multi-leg use native movement;
  removed module restores the old walk and fails the fixed demand. Extra native controls cover
  relocation, expedition, holder, task state, invalid home and cancellation. **Limit:** fixture geometry and
  movement cannot establish the actual pickup anchor or door route; links 04 and 07 own those.
- **Drift instance:** the first harness draft omitted a native `IsInWalkingDist` dependency on
  its relocation cleanup leg. It failed there, was corrected with an explicit fixture helper,
  and the full matrix was re-run GREEN. Audit that this stub cannot decide C115's bypass result;
  the result depends on `IsUnitInDome` before native movement.
- **Drift instance:** review found that the first build's equality guard could match false
  destination, home and position results on a malformed task. `52b6449` requires a valid
  destination and adds a native-delegation control for an invalid home. Audit the final guard,
  including the task's other ambiguous false/nil fields.

### From hubset 03, 2026-09-24 — C117 build and drift inbox

- C117 branch commit `38cd46c` adds `Code/Fix_PassageHubSalvageDrain.lua`, registration and
  `tools/desk_c117_hub_salvage.py`; main commit `f87aa5b` records the
  [C117 build](../../bugs/C117.md) and [desk output](../../../archive/logs/hubset_c117_desk_2026-09-24.txt).
  The module extends native pre-disconnect waiting for traversers already in a hub passage and
  returns false for fresh entries only while a usable sibling remains. No PF tunnel restoration,
  copied blocking body, persisted field or mod-owned thread. `bodycheck` reported matching pins for
  both targets; parsecheck and doccheck were GREEN on `hubset`, and main doccheck was GREEN.
- Fix-on and fix-absent controls discriminate the source race: with the module, the colonist has
  hub holder and marker before native disconnect; without it, the same interleaving lands outside.
  The desk also tests native last-exit parity, cancellation, fresh-entry `ClearPath`, reload from
  native fields, Require declines and chained returns. The scheduler and movement are fixtures;
  real-game rerouting, save serialization and natural reach remain for 07. Simultaneous salvage of
  all spokes retains native C99 behavior; no claim is made that its last-exit predicate is safe in
  that separate case.
- **C42 source conflict for owner disposition:** archived `Lua/Passage.lua:819` assigns
  `PassageGridElement.OnEnterUnit = empty_func`. `LeadIn` dispatches through that method
  (`BuildingWayPoints.lua:489-497`), so C42's recorded `LeadIn` → inherited `SetHolder(element)`
  path does not run. No other element-holder registration path was found in this source sweep.
  C42's teardown harness inserts a stale member synthetically; that control alone cannot prove
  the shipped creation path. The owner has been asked to hold C42 pending a live witness or retain
  it for audit. Audit the owner ruling and correct the C42 record before a release verdict.
- **Drift instances:** the first C117 fixture repeated the incorrect element-holder assignment in
  its `LeadIn` seam; source review removed it and the full harness passed again. Hubset 04's archive
  links in 05 and this inbox use `../../archive/`, but from `docs/agent/prompts/hubset/` the route
  is `../../../archive/`; verify the evidence through the latter path. The C117 module does not
  overlap C42's installed `Holder:KickUnitsFromHolder` wrapper.

### From the chain author, 2026-09-24: 04 retired, sitting model rewritten (owner's review)

- **Owner ruling, verbatim: "One sitting only."** 07 is the only attended link. The retired 04 sitting
  (grave `git show d6667dc:docs/agent/prompts/hubset/04_MEASURE_SITTING_owner.md`, closed `be69f7d`) is
  replaced by a desk link, `04_ON_HUB_TEST_high.md`, which derives the on-hub test from source.
- **Its footprint verdict is void.** "S4 refuted; hex ownership OR `dz > 0`" accepts all 195 `SMRFOOTU`
  rows (every row has `dz > 0`), `passage` never identified which passage, and 90 rows stand 10,000 or
  more game units from their hub. Corrections are appended to C114's, C115's and C116's 2026-09-24
  sections, and C114's row_status, evidence and fix shape no longer claim it. Audit that 05 built on
  04's source-derived test, not on the void one.
- **Drift, for the record:** the retired brief's console lines called a bare `MapGet` (not a global in
  1.1.x) after a stub "smoke-run"; it asked the owner to wait at normal speed and to watch ~867
  colonists for a status; and prediction 1 could not come out refuted. The closing session repeated
  the error by recording "clean, not mixed", and wrote in C116 that the anchor line selects everyone
  showing "Moving to a new Dome" (it selects own-home rescues only). The fix to the rails is with the
  documentation orchestrator, not this chain.
- **Rewritten:** 05 (gate, outcome, stop, inbox note), 06 (07 is built as a preloaded SMRTK sitting:
  slots and triggers, `Run until` at top speed, an owner-seat read, predictions that can fail,
  API shapes counted), 07 (second-seat check before the owner sits; no improvised console code) and
  the README (rulings, row 04, ordering). Audit 07 against 06's FIXED list.
- **Unreconciled, not fixed here:** C115's heading tag says "anchor unmeasured" while its row_status
  says "pickup anchor measured 2026-09-24 (04)".

### From hubset 04, 2026-09-24 — on-hub test derived from source (desk)

- **The test:** [ON_HUB_TEST_2026-09-24.md](../../reports/hubset/ON_HUB_TEST_2026-09-24.md). `OnHubNow(unit, hub)` =
  a live hub and **(A)** in flight on a connected passage (`traversing_passage` valid, cross-checked
  against that passage's `traversing_colonists`, and the passage in `hub.connected_passages` or
  `draining_passages`) **or (B)** standing on the hub (not traversing; `holder == hub` or
  `passage_hub == hub`; and `HexGridGetObject(object_hex_grid, WorldToHex(unit), "PassageHub") == hub`).
  Each input has an archived-1.1.1.405907 citation and a fail-closed case. The test is SOURCE, not
  measured: it becomes measured only when 07 runs readings R1-R7. It uses no map query, no
  file-local helper and no blocking body, so no stop fired.
- **Source facts that change earlier readings:** `hub.units` is exactly `holder == hub`
  (`Unit.lua:805-822`, `Holder.lua:27-41`). Passage elements never become holders (`Passage.lua:819`).
  So a hub-to-dome traverser keeps `holder == hub` across the whole passage and its ramp. That likely
  explains the retired log's far-away `units` rows (INFERRED; R2 checks it). Traversal cannot be
  interrupted, because `SetCommand` waits for running destructors (`CommandObject.lua:363-367`). But
  `Colonist:SetCommand` calls `HasLocalAccess` at `ColonistTransport.lua:416` on the caller's
  thread, so C114's wrapper is reached mid-passage and needs branch A.
- **Dome hexes:** guard 3 need not cover them. B reads only hub identity. Native access already
  handles a holder-less colonist on a dome hex.
- **Routed finding (05, 99, owner):** a stale `holder == hub` makes `IsUnitInDome` false even inside
  a dome, because `IsObjInDome(holder)` reads `hub.parent_dome`, and a hub has none
  (`Dome.lua:111-114`, :159-161). `Dome:OnEnterUnit` is empty (`Dome.lua:1850`), so entering a dome by
  `Dome_Entrance` keeps the hub holder. It also keeps `UpdateOutside` sheltered, so clearing
  C116's marker alone does not restore the timer for such a colonist. Reach is INFERRED: it needs an
  overland walk off the hub (R2, R6). 05 decides whether its C116 module drops a hub holder that
  fails `OnHubNow`, and says so either way.
- **For 06:** R1-R7 in the note are the slot readings, each with its object, field, expected and
  refuting value. Their API shapes are counted in the note. R3 and R5 want triggers
  (`traversing_passage` becoming false). R4 and R6 need a colonist dumped on a hub: fire a worker
  who just arrived there.
- **Drift for 99:** `MIGRATION_AUDIT_2026-09-24_D_hubs.md:75,110,351` still says `LeadIn → OnEnterUnit →
  SetHolder(el)` for passage elements, which `Passage.lua:819` contradicts. This is the premise
  03 flagged for C42, repeated in the audit's field-lifetime table. It is not corrected here.

### From the chain author, 2026-09-24: check of 04, one overstatement

04's test stands, and 05 may build on it. One SOURCE claim in the note is too strong: "`hub.units` is
exactly `holder == hub`". On a hub-to-dome crossing, the destructor's else branch
(`Lua/Passage.lua:1230-1235`, archived 1.1.1) calls `SetHolder()` (which does run `OnExitHolder`) only
when `passage_hub` is valid. It then sets `unit.holder = nil` directly, bypassing `OnExitHolder`. A unit
that holds the hub without the marker therefore leaves a stale entry in `hub.units` with `holder ~= hub`.
Whether any path sets `holder == hub` without `passage_hub` is unverified; the plain `LeadIn` into the
hub via `WaypointsObj:OnEnterUnit` is the lead. Consequences: `OnHubNow` never reads `hub.units`, so it
is unaffected. Do not use `hub.units` as a membership source in 05. The retired log's far-away `units`
rows may be stale list entries rather than colonists in flight; R1 and R2 in 07 decide which.

### From hubset 05, 2026-09-24 — C114/C116 build and drift inbox

- **Build to audit:** `hubset` `76d1ed8` adds a shared `OnHubNow` test, guarded
  `Colonist:HasLocalAccess` widening, and a synchronous marker/holder departure cleanup. The
  `7ebad3d` follow-up extends C114's harness through native `SetCommand` and its rescue-booking
  branch. The
  [C114](../../bugs/C114.md) and [C116](../../bugs/C116.md) build sections cite
  [archived desk output](../../../archive/logs/hubset05_c114_c116_desk_2026-09-24.txt).
  Rerun both harnesses and inspect the exact branch diff, including registration and the helper's
  `SRC: none` disposition. C116 drops a stale hub holder only after both logical and visual hub
  hexes are false; inspect whether any genuine ramp can be stripped by that test. The load-time
  sweep was omitted because restored traversal state at `OnMsg.LoadGame` was not established;
  existing idle markers can remain until a movement/holder event.
- **Drift instance:** 04's report and 06/99 inherited inbox wrote
  `HexGridGetObject(object_hex_grid, WorldToHex(unit), "PassageHub")`. Lua expands only the first
  return from a nonfinal argument expression, so that call passes the class string as `r`, not
  the second hex coordinate. The built helper correctly takes `local q, r = WorldToHex(unit)`
  first. The original report is left intact for audit; do not treat its pseudo-call as tested.
- **Audit focus:** C114's desk control proves only an unrelated station still reaches the
  train-search gate. A destination that is in the attached dome network might still need a train
  for a route condition Lua topology does not expose; 07's valid station commute is the decisive
  control. C116's `Unit:Step` wrapper is installed before class flattening; check that a live
  colonist dispatches through it after classes build, and that the visual-position guard retains
  shelter for the full ramp. Neither desk harness proves the game's door/tunnel route or a
  real-game outside timer. Keep the C42 source conflict in this inbox separate from those checks.

### From hubset 06, 2026-09-24 — sitting prepared, and its drift inbox

- **Heads:** TestKit `66288da` (`Code/80_AgentSlots.lua`, sha256 prefix `4081e6a66c43c2bc`),
  `hubset` `7cf48a2` (adds `tools/desk_hubset07_rehearsal.py`), `main` at this close-out commit
  (parent `371aad5`). The script, predictions P1-P13 and R1-R7, junction commands and owner-seat
  read are in 07's `## The script` section.
- **Slot labels:** Scratch `Boot: build, fixture, census (read only)`; 1 `C115: follow own-home
  rescues from load`; 2 `Pause on a far-home worker landing on a hub (R3)`; 3 `Pause on a far-home
  worker mid-spoke (R5)`; 4 `Fire the paused worker and follow it (C114/C116)`; 5 staged
  `[1] C117 1/2: pause on a busy hub spoke` / `[2] C117 2/2: salvage the paused spoke, follow`;
  6 staged `[1] C111 1/3: select an own-home rescue` / `[2] C111 2/3: select a real relocation` /
  `[3] R7 3/3: marker clear per hex class (segment A only)`. Triggers: `h7_rescues`,
  `h7_hub_arrival`, `h7_mid_spoke`, `h7_follow`, `h7_busy`, `h7_drain`.
- **Owner minutes: about 30, an estimate, not measured** (A 13, B 12, relaying words 5). Two boots:
  fix off on `main`, fix on on `hubset`. No module can be switched off at runtime.
- **Rehearsal (declared VOID):** [archived output](../../../archive/logs/hubset06_rehearsal_2026-09-24.txt).
  58 of 58 demands held, every prediction's scratch variant read REFUTED, and nothing armed at load.
  A mutant that forces P7's hubset judge to HELD failed the harness (57 of 58, exit 1). SMRTK gates:
  parsecheck 0 errors; both `rg` gates matched 0 lines with exit 1, beside a positive control on
  the same scope. P3: bodycheck on `hubset` gave 6 OK.
- **Stop routed to the owner: F127 has no leg.** Its C83 branch needs a passenger arrival whose chosen
  dome turns unwelcoming, with a full fallback. That is a hand-built fixture: about 5-8 owner
  minutes per segment plus rocket transit, at unknown odds. Only P13, a read-only hidden-homeless
  census, is built. The owner chooses to build that fixture as a 07 amendment, or to leave F127
  desk-verified.
- **Not played, routed to 99:** 05's other C114 controls (small dome, unrelated destination, stale
  marker or holder off the hub, disconnected spoke, cross-map, outdoor, full-service and valid
  station commute). 05 called the station commute decisive. Also not played: C116 save/reload, and
  R4's visual hex and holder-list membership. The follow records only the logical hub hex at the
  dump. An idle stale marker at load is counted by place in the census, not followed.
- **C42:** no stand-alone leg. P10 (`C42STALE` after traffic) is the live witness for the owner
  decision still open in 99's inbox. P9 samples a kick only if a stale element member exists.
- **Drift:** `tools/SMRTK.md` says "A pack lane does not commit in it" of the TestKit, while 06's
  brief requires the slots "committed in the TestKit repo". The brief was followed (`66288da`); the
  tension is not resolved here.
- **Audit focus:** the judges in `SMRTK.H7` decide every verdict. Check each against its prediction
  row, and check that no instrument selects on the field it then reports. Selection is by the
  passage's list, the holder and the marker; hex, flag and outcome are read afterwards.

### From the owner, 2026-09-24, after 06 closed: scope cut

Verbatim: "anything that was a minor addon that isn't what this chain was created for are desk
verified only." "We are doing the bare minimal testing in game needed to ship these new fixes."
C42, F127 and P3 ship desk-verified; audit them against their desk harnesses, not play. 06's F127
stop and its "not played, routed to 99" list (05's other C114 controls, C116 save/reload, R4's extra
fields) are withdrawn by this ruling, not owed. R7 is not run.

### From hubset 07, 2026-09-24 — the sitting ran; verdicts and drift inbox

Both segments ran on New Horizons 2 83 (sol 125): A on `main`, B on `hubset` `7cf48a2`, TestKit `66288da`.
The B2 read-back held: `build=hubset`, all six modules `active` and `applied`. Evidence is in `docs/archive/logs/`:
`hubset07_segA_main_2026-09-24.log`, `hubset07_segB_hubset_2026-09-24.log`, the owner relay
`hubset07_owner_relay_2026-09-24.md` and two owner screenshots (`hubset07_A3a/B3a_owner_screenshot.jpg`).
Each member's entry carries a dated "hubset 07 sitting" section. **No entry is `tested-attended`**: the owner
watched no fix work.

| # | member | `main` | `hubset` |
|---|---|---|---|
| P1 | C115 | NOT_SAMPLED (no own-home rescue at load) | NOT_SAMPLED (same) |
| P2 | C115 | HELD (16 of 16) | HELD (16 of 16) |
| P3 | C114 hub | **REFUTED** (defect absent: no booking, safe end) | HELD (same outcome) |
| P4 | C114 mid-spoke | **REFUTED** (same) | HELD (same outcome) |
| P5 | C116 | NOT_SAMPLED ×2 | NOT_SAMPLED ×2 |
| P6 | C116 ramp | HELD ×2 | HELD ×2 |
| P7, P8 | C117 | NOT_SAMPLED (watch timeout) | NOT_SAMPLED (watch timeout) |
| P11 | C111 | HELD (owner screenshot) | **REFUTED** (still T 4333; owner screenshot) |
| P12 | C111 | NOT_SAMPLED (no relocation) | NOT_SAMPLED |
| R1-R6 | 04 on-hub test | all HELD (R1/R2 at boot and after traffic) | all HELD |

**Owner decisions (no standing rule; facts in the entries):**
- **C111:** the fix did not change the live text. Cause not found; candidates are in the entry.
- **C114:** the sitting cannot discriminate it, because the defect did not reproduce with the fix off.
- **C117:** unobserved. The C115 own-home path and C116's clear path were also not exercised.

**Drift and instrument defects:**
- **`h7_drain` cannot sample at 128x.** Its 3-game-hour window (`80_AgentSlots.lua:776`) ends after
  90,368 game ms, but the salvage countdown ticks in real time (`Demolishable.lua:108,117`, 1.1.1.405907).
  At factor 128000 it needs about 640,000 game ms (INFERRED), so `OnDemolish` never ran in either segment.
  The 06 rehearsal's scratch variants did not model the countdown.
- **No chime.** Every trigger logged `sound=true`, but the owner heard no chime at A4. The self-pause was
  used as the signal instead.
- **Step 1 did not hold.** At the pre-sitting check, Mars.exe was already running at the main menu,
  booted on `main` with the slots loaded and no save loaded. The owner proceeded on it. The fixture was
  backed up before load (sha256 `036e130d…`, identical after the sitting), and no save was written.
- **Label collision.** The script's prediction "P3" (C114 hub) shares a name with member P3 (the
  VacuumWalks pins), which the scope cut says gets no reading.
- **Owner observation, A6:** "multiple colonist on the screen with o2 readings". Captured as SMRTK
  screenshots 0074-0076 (`SMR-ScreenCaptures`); unexamined. The followed subjects had `open_seen=false`.
- **A3b was NOT RUN in both segments**, so the relocation subject never existed on this fixture.
