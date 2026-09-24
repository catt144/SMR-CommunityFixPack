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
