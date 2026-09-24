# hubset 04: derive the on-hub test from source (desk)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first. Unattended
and read-only in code; it can fire now. It replaces the retired attended measurement sitting
(grave: `git show d6667dc:docs/agent/prompts/hubset/04_MEASURE_SITTING_owner.md`, closed in
`be69f7d`). Authored on `main` after `300e40f`.

## Authority and outcome

Owner ruling 2026-09-24: **"One sitting only."** The chain's only attended sitting is 07. Nothing
this link finds may schedule another. C114's guard 3 and C116's clearing both need one synchronous
answer to *"is this colonist physically on this live hub, or in one of its connected passages, right
now?"* in which a stale field fails closed. The retired 04 tried to answer it by hand-measuring a
positional footprint. Its verdict is void (Evidence below).

End state:

- A design note at `docs/agent/reports/hubset/ON_HUB_TEST_<date>.md` naming the test 05 builds.
  Give each input's archived-1.1.1.405907 source citation, and say why that input cannot be stale
  or how it fails closed when it is.
- Anything only the running game can confirm, written as numbered readings for 07. Each gives the
  object, the field, the expected value and the value that would refute it. 06 turns these into
  preloaded SMRTK slots.
- Both appended to 05's, 06's and 99's inboxes and committed on `main`, with doccheck GREEN.

Open a live todo list before the first write.

## Evidence (re-derive before relying on it)

- **The retired verdict cannot decide anything.** It read "S4 refuted; on-hub = hex ownership (hub
  or connected passage) OR `dz > 0`". In the archived log
  (`docs/archive/logs/hubset04_footprint_Mars.exe-20260924-15.34.30-6aad2d75.log`), every one of the
  195 `SMRFOOTU` rows has `dz > 0`, so that test accepts all of them. Its `passage` category is the
  building class under the unit, never which passage. MEASURED; falsifier:
  `grep SMRFOOTU <log> | awk '{for(i=1;i<=NF;i++) if($i=="dz") z=$(i+1); if(z==0) n++} END{print NR, n+0}'`
  must print `195 0`.
- **A hub's `units` list holds colonists far from it.** 90 of the 195 rows stand 10,000 or more game
  units from their hub (72 of them on `passage`; the farthest is 18,295). They are doing `Work`,
  `VisitService`, `Rest` and `Roam`, some inside domes. MEASURED from the same log. Reading this as
  stale membership is INFERRED until source says what `units` means and when an entry leaves it.
  Rows span two passes, so a colonist can appear twice.
- **The `passage_hub` marker outlives the crossing.** About 11% of marked colonists sat inside domes
  with the marker still set ([C116](../../bugs/C116.md), 2026-09-24 section). MEASURED.
- **The guard's own text:** neither `passage_hub` nor `holder == hub` alone proves presence
  ([C114](../../bugs/C114.md), fix shape, guard 3).
- **API shape:** in Relaunched, `MapGet`, `MapForEach` and `MapCount` are `MapInterface` methods
  (`CommonLua/Core/map.lua`, the `DefineClass.MapInterface` table), called as `map:MapGet(...)`. The
  archived 1.1.1 tree has 0 bare `MapGet(` calls. EF-096's "open names" list is stale on this point
  and is being corrected elsewhere; do not cite it for these names.

## The question

Which synchronous, source-backed signal says "on this hub or its connected passage, now"? The
following are leads, not hypotheses to prove:

- the colonist's current command and its arguments during hub and passage traversal
  (`Passage.lua`, `BuildingWayPoints.lua`);
- the holder together with the holder's own bookkeeping for this unit;
- hex **identity**: the building on the unit's hex is this hub, or a passage element whose passage
  is attached to this hub. A class category is not identity.

Also settle **whether guard 3 needs to cover a dome hex at all.** `IsUnitInDomeRange` already
returns true for a unit standing on a hex of the *destination* dome (`Lua/Units/ColonistTransport.lua:19-28`,
archived 1.1.1). If native access already passes for a ramp overhanging that dome, the test can fail
closed there; say what happens over any other dome's hex. For C116,
say what the native outside recomputation does on that hex, and whether clearing the marker there
is safe.

Prefer state to position. If position is needed, use identity, and state the fail-closed case.

## Scope

- **In:** reading source for the test; the design note; the 07 readings.
- **Out:** any code, harness or TestKit change (05 builds it and 06 writes the slots); C115, C117
  and C42; load order.

## Stops

- No signal is both present during a real crossing and cleared or ignorable after it: report the
  options with their cost and route them to the owner. Do not propose a second sitting.
- The only usable signal lives in a file-local helper or a blocking body that would have to be
  copied: report the cost.

## Do not claim

A desk-derived test is SOURCE, not "sound" or "measured". It becomes measured only when 07 reads it
live. Do not re-read the retired log as a footprint answer.

## Close-out

Append your outbox to 05's, 06's and 99's inboxes, strike your row, `git rm` this file, and commit
on `main`.

## Notes from upstream
