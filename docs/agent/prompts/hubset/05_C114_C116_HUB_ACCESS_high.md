# hubset 05: C114 access fallback and C116 marker lifetime, on one physical on-hub test

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first. **Fire only
after link 04 has recorded its footprint verdict, and after 02 and 03 have closed.**

## Authority and outcome

The owner approved the C114 direction in principle and the whole set as one release. C114 is the
set's lead fix. Act on [C114](../../bugs/C114.md) and [C116](../../bugs/C116.md) and the resweep's
S1 and S3 sections
([MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md)).
End state, on `hubset`:

- One shared, synchronous physical test: this colonist stands on a live hub, or on or in one of its
  connected passages, built on link 04's measured footprint.
- **C114:** a result-widening wrapper on `Colonist:HasLocalAccess` that keeps every native true and
  adds true only under the entry's four guards.
- **C116:** the hub marker cleared on verified departure from the physical hub or passage, followed by
  the native outside recomputation.
- Desk harnesses whose controls fail with each fix removed, dated build sections in both entries on
  `main`, doccheck GREEN in both trees. Open a live todo list before the first write.

## The four guards for C114 (from the entry; keep all four)

1. The destination is a Dome, or a building with a valid Dome `parent_dome`. No random outdoor
   target, habitat, station or elevator gains access by proximity.
2. It is the current-position query. The home-relative call (`ColonistTransport.lua:447`, re-derive)
   keeps its meaning.
3. The colonist is physically on a live hub or passage, by the shared test. Neither `passage_hub` nor
   `holder == hub` alone proves this; stale traversal fields fail closed.
4. A still-connected endpoint dome's `dome_network` contains the destination dome. A hub has
   `hub_domes`, not `dome_network`, so derive the network through an attached dome
   (`Passage.lua:1593-1601`, `Dome.lua:688-706`, re-derive).

It must not widen work assignment (`SetWorkplace`), service capacity or the train graph, raise the
global radius, or widen `GetClusterDomes`. The resweep's "Effects beyond migration" table lists what
it does change for Work, services, stations and Stranded. Check each row against your build.

## C116 constraints

Never clear the marker on every `ExitHolder`: the native comment protects a real dump onto the hub.
Prefer a synchronous lifecycle hook to a polling thread. A colonist on a real ramp keeps its shelter;
clearing it there falsifies the fix. A load-time cleanup of stale markers is a separate question:
decide whether it is needed and give its §3a disposition, or leave it out and say why.

## Controls the harness must carry (the resweep's S1 list, plus C116's)

A large-dome interrupted crossing (access granted, no rescue booked), a small dome (native already
passes), an unrelated destination, a stale marker or holder off the hub (no grant), a removed last
connection, a cross-map destination, an outdoor workplace, a service denied by native policy, a valid
station commute (train not suppressed), a marked colonist that walked off the hub (marker cleared), a
colonist on a ramp (marker kept), and each module removed.

## Scope

In: the shared test, the C114 and C116 modules, their harnesses, registration on `hubset`, both
entries' build sections. Out: rescue tasks already booked (C115, link 02), passage demolition
(C117, link 03), C99's predicate, load order.

## Stops

- 04's footprint verdict is mixed or missing: do not guess a discriminator; route it to the owner.
- The only route is a copy of a file-local helper chain or a blocking body: report the cost.
- The resweep's falsifiers fire on the desk (a grant from a stale origin, a suppressed needed train):
  stop and route the facts.

## Do not claim

`access == true` is not success. Success is safe entry without a rescue loop, which only 07 can
show. The engine's door-versus-tunnel route after access is granted is not decided by Lua.

## Close-out

Append your outbox to 06's inbox and 99's, strike your row, `git rm` this file, commit on `main`.

## Notes from upstream

### From hubset 04, 2026-09-24 — hub-footprint, marker and anchor readings

- **Footprint verdict for the shared physical test (condition 3): clean, not mixed.** Two console
  passes on TheGodUncle's save, unfixed code, archived at
  [`docs/archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log`](../../archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log).
  S4 refuted both passes: zero held units at `none`/`dz 0` across 80 then 140 held units on hubs
  2692, 4113, 1908 and 2026. The sound discriminator is **hex ownership (the hub's own hex or a
  connected passage/PassageRamp hex) OR `dz > 0`** — the hub's ramps do reach over dome hexes while
  still elevated. Full breakdown in [C114](../../bugs/C114.md)'s 2026-09-24 sitting section.
  `holder == hub` was not directly exercised; do not read this as validating it alone.
- **C116 marker lifetime: reach confirmed, harm not yet caught live.** Across the same two passes,
  ~11% of marked colonists (8/74, then 14/133) sat inside a dome, `outside false`, far from their
  marked hub — the marker does outlive hub departure at a measurable rate. But no marked colonist
  in either pass was on open ground (`none`) with the timer suppressed, so the specific harmful
  combination (shelter in vacuum) is still unmeasured. Full detail in [C116](../../bugs/C116.md)'s
  2026-09-24 sitting section — worth keeping in mind when picking your clearing hook's trigger
  point, since indoor drift is the common case you'll see in the harness/controls, not open-ground
  exposure.
- Reconciliation held for both `SMRFOOT` and `SMRMARK` totals in both passes (category counts sum
  to the reported total; no mismatch) — the readings are trustworthy, not a partial sample that
  needs re-taking.

### From hubset 03, 2026-09-24 — C117 drain build and C42 source conflict

- C117 code and desk harness are committed on `hubset` at `38cd46c`; the dated
  [C117 build record](../../bugs/C117.md) and [desk output](../../../archive/logs/hubset_c117_desk_2026-09-24.txt)
  are on `main` at `f87aa5b`. `Fix_PassageHubSalvageDrain` widens native `WouldStrandHubColonists`
  synchronously while a traverser is in flight; it refuses new `TraverseTunnel` entries only when
  another active, non-demolishing, non-draining spoke can take traffic. It copies neither blocking
  body and adds no persisted field. It does not wrap C42's `Holder:KickUnitsFromHolder` target.
- The desk loads archived 1.1.1.405907 demolition, traversal and disconnect bodies. Busy-spoke
  fix-on arrival sets hub holder and marker before disconnect; the module-absent control arrives
  outside. It also holds native last-exit waiting, cancellation, admission/`ClearPath`, fresh-runtime
  drain state, shape declines and chained returns. Real game rerouting, save serialization and the
  player-visible race are for 07. Both trees were doccheck GREEN after the commits.
- **Source conflict, owner decision pending.** `PassageGridElement.OnEnterUnit = empty_func`
  (`Lua/Passage.lua:819`, archived 1.1.1.405907) overrides the inherited registration that
  [C42](../../bugs/C42.md) says `LeadIn` calls. `BuildingWayPoints.lua:489-497,531-535` confirms
  that `LeadIn` dispatches through `OnEnterUnit`. C42's claimed stale element-list producer is
  therefore contradicted on this build; no other source registration path was found. The owner
  has been asked whether to hold C42 pending a live witness or retain it for audit. Do not infer
  C42 is source verified from its synthetic teardown harness while this is unsettled.
- **Drift instance for audit:** the first C117 fixture wrote `unit.holder = element` inside its
  `LeadIn` seam, repeating C42's incorrect premise. Source review caught it; the fixture now
  follows `Passage.lua:819`, and the whole desk harness passed again. The earlier 04 archive-log
  links in this inbox use `../../archive/`; from this folder the correct route is
  `../../../archive/`. The linked evidence still exists at `docs/archive/logs/`.
