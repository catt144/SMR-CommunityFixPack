# hubset 03: C117, keep in-flight colonists' hub endpoint through a disconnect

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.

## Authority and outcome

The owner approved fixing the hub set as one release; C117 is in it. Act on
[C117](../../bugs/C117.md) and the resweep's S5 row
([MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md),
"S3–S12" table and "Ranked follow-up shapes"). End state: a module on `hubset` that ensures a colonist
already crossing a hub passage when it is salvaged arrives on the hub with holder and marker set, not
outside. It comes with a desk harness whose controls fail with the fix removed, a dated build section
in C117 on `main`, and doccheck GREEN in both trees. Open a live todo list before the first write.

## The defect, briefly

With another exit to the hub still live, `WouldStrandHubColonists` lets demolition proceed
(`Passage.lua:1134-1138`). `OnDemolish` calls `DisconnectDomes` (:1181), which removes the tunnel
metadata (:1404, 1742-1750, 710). A colonist still traversing reads `element.is_pf_tunnel` only at
:1224, takes the non-hub branch and lands outside with no holder or marker. The elements are not
deleted at once: :1182-1184 waits for traversers before `Demolishable.lua:132-140` calls `DoneObject`.
All archived `1.1.1.405907`; re-derive every line. Not observed in play.

## What the design must hold (the resweep leaves the complete shape open; choosing it is this link's job)

- Two candidate directions: keep the arriving traverser's hub endpoint independent of the mutable
  tunnel metadata, or drain traversers before the disconnect while refusing new entries.
- Do not restore a removed PF tunnel just to keep its metadata.
- A plain wait-wrapper on `OnDemolish` can admit fresh traffic forever and adds a blocking frame.
  Any blocking or per-unit state needs a full §3a disposition: cancellation, save and reload mid-drain,
  new arrivals, and the last real escape left usable.
- Link 01's C42 member touches the same traversal destructor. Read 01's outbox before choosing; if your
  shape and C42's collide, reconcile in one place and say so in both entries.
- Controls for the harness: salvage one busy spoke with a sibling live (in-flight colonist lands on the
  hub), the last exit (native wait unchanged), cancelling the salvage mid-drain, a new colonist trying
  to enter the demolishing passage, and the module removed (the colonist lands outside).

## Scope

In: C117's module, its harness, registration on `hubset`, C117's build section on `main`. Out: C99's
last-exit predicate (keep it), `HasLocalAccess` and the marker (05), rescue rides (02), load order.

## Stops

- The least invasive complete shape needs a full copy of `TraverseTunnel` or `OnDemolish`, or a
  persisted field: report the options with their costs and let the owner choose.
- The shipped demolition or traversal shape differs from C117: route the facts.
- Link 02 is mid-flight on `metadata.lua` or `items.lua`: wait for its commit.

## Do not claim

The race is source-verified and unobserved in play. The desk proves the fix's decision logic, not
that players hit the race; 07 salvages a busy spoke in the real game.

## Close-out

Append your outbox to 05's inbox and 99's, strike your row, `git rm` this file, commit on `main`.

## Notes from upstream
