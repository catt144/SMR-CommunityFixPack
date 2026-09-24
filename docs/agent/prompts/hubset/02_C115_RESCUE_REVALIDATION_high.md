# hubset 02: C115, stop an obsolete own-home rescue

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.

## Authority and outcome

The owner approved fixing the hub set as one release; C115 is in it. Act on
[C115](../../bugs/C115.md) and the resweep's S2 section
([MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md)).
End state: a module on the `hubset` branch that, when `Transport` starts for an uncommitted own-home
rescue, drops the pickup if the colonist is already physically safe at home, and otherwise leaves
`Transport` native. It comes with a desk harness whose controls fail with the fix removed, a dated
build section in C115 on `main`, and doccheck GREEN in both trees. Open a live todo list before the
first write.

## The defect, briefly

The Idle wrapper books an own-home rescue (`ColonistTransport.lua:461-474`). With no source dome,
`CreateColonistTransportTask` captures `colo:GetPos()` as the pickup (`LRTransport.lua:106-111`), and
the passage walk can finish before the command changes (`Passage.lua:1205-1246`,
`CommandObject.lua:363-368, 441-459`). `Transport` then exits the holder, walks to a passable point
near that pickup and waits up to a sol (`Colonist.lua:3973-3986, 4000-4006`) without asking whether
home was reached. The owner watched a colonist die on this route. All archived `1.1.1.405907`;
re-derive every line.

## What the design must hold (from the resweep; the approach is yours)

- A guarded command bypass with native task cleanup and tail delegation to the shipped `Transport`
  (FIX_POLICY layer 2), not a copy of the animation or wait body, and not an always-call §1.4 chain.
- Act only on an uncommitted own-home rescue: `transport_task.dest_dome == self.dome`, no source dome,
  no shuttle committed. Leave committed shuttles, real relocation, multi-leg tasks, expeditions and
  remote rescues native.
- "Physically safe at home" must be a real position test (inside the home dome), not a marker or a
  holder.
- Rejected shapes: returning nil for every hub rescue (strands colonists after a disconnect) and
  shortening the one-sol wait (only shortens exposure).
- Disposition per §3a: what happens on save and reload mid-`Transport`, and on cancellation.
- Controls for the harness: an obsolete rescue after reaching home (bypassed), a remote colonist that
  still needs rescue (native), a committed shuttle already approaching (native), a multi-leg task
  (native), and the module removed (the obsolete walk-out returns).

Link 05's C114 fix will cut how often these rescues are booked, but it cannot clean up tasks already
booked, so C115 stands alone. Do not wait for 05.

## Scope

In: C115's module, its harness, `metadata.lua`/`items.lua` registration on `hubset`, C115's build
section on `main`. Out: `HasLocalAccess` (05), the hub marker (05), passage demolition (03), load order.

## Stops

- The only route is a full copy of `Transport`, or the fix needs a persisted field: report the cost
  and a narrower option.
- The shipped `Transport` or task shape differs from C115: route the facts.
- Link 03 is mid-flight on `metadata.lua` or `items.lua` in the worktree: wait for its commit.

## Do not claim

The desk proves the bypass decision, not the engine's walk path or the pickup anchor on a real save.
The anchor read in link 04 and the sitting in 07 decide those.

## Close-out

Append your outbox to 03's inbox and 99's, strike your row, `git rm` this file, commit on `main`.

## Notes from upstream

### From hubset 01, 2026-09-24

- The `hubset` worktree is `B:\Dev\SMR\SMR-BugFixPack-hubset`; branch HEAD `795aefa`
  builds P3, C42, F127 and C111. Code and harnesses are committed there. Main's dated
  entries and [P3 build record](../../reports/hubset/P3_BUILD_2026-09-24.md) are in `6227f2f`.
- C111 now wraps only `Colonist:Getui_command` for an own-home `Transport` rescue; it does not
  change `Transport`, its task or movement. Its text is a proposal pending checklist ck216;
  link 02 should keep C115's own movement and task controls independent of that UI result.
- C42 filters stale `PassageGridElement.units` entries synchronously before
  `Holder:KickUnitsFromHolder`, while vanilla's raw clear in `TraverseTunnel` remains. Link 03
  and 05 must account for that remaining traversal state; no full traversal copy was built.
- F127 changes only the C83 arrival reroute's booking path in `Fix_ArrivalDeaths`; it does not
  alter the own-home rescue path. A full habitat exposed an initial reserve-only omission;
  final build cancels the rejected hold first and the desk has a failing old-shape control.
- Link 01's branch gate and main gate were GREEN. The branch is unplayed; link 07 and link 99
  still own game verification and audit.
