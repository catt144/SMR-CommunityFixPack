# hubset 05: C114 access fallback and C116 marker lifetime, on one physical on-hub test

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first. **Fire only
after link 04 has recorded its desk-derived on-hub test, and after 02 and 03 have closed.**

## Authority and outcome

The owner approved the C114 direction in principle and the whole set as one release. C114 is the
set's lead fix. Act on [C114](../../bugs/C114.md) and [C116](../../bugs/C116.md) and the resweep's
S1 and S3 sections
([MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md)).
End state, on `hubset`:

- One shared, synchronous physical test: this colonist stands on a live hub, or on or in one of its
  connected passages, built on link 04's desk-derived on-hub test.
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

- 04's on-hub test is missing, or 04 routed it to the owner: do not guess a discriminator; wait for
  the owner.
- The only route is a copy of a file-local helper chain or a blocking body: report the cost.
- The resweep's falsifiers fire on the desk (a grant from a stale origin, a suppressed needed train):
  stop and route the facts.

## Do not claim

`access == true` is not success. Success is safe entry without a rescue loop, which only 07 can
show. The engine's door-versus-tunnel route after access is granted is not decided by Lua.

## Close-out

Append your outbox to 06's inbox and 99's, strike your row, `git rm` this file, commit on `main`.

## Notes from upstream

### From the chain author, 2026-09-24: the retired 04 sitting's verdict is void

The note the retired sitting link left here (grave: `git show be69f7d:docs/agent/prompts/hubset/05_C114_C116_HUB_ACCESS_high.md`)
declared the footprint "clean, not mixed" and named the discriminator "hex ownership OR `dz > 0`".
**Do not build on it.** All 195 `SMRFOOTU` rows in its archived log
(`docs/archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log`) have `dz > 0`, so
the test accepts every unit. Its `passage` category never identified which passage. And 90 rows stand
10,000 or more game units from the hub that lists them. The owner ruled "One sitting only", and link
04 is now a desk derivation of the on-hub test. Its outbox, when it lands below, replaces this note.

Still usable from that sitting, as data rather than verdicts: the C116 marker counts (about 11% of
marked colonists inside domes with the marker set) and the hub `units` lists naming far-away
colonists. Both are in [C114](../../bugs/C114.md)'s and [C116](../../bugs/C116.md)'s 2026-09-24
sections, with their corrections.

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
