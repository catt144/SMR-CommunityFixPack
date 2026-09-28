# C120 build — a deport-law rocket that never launches

One-off build brief, authored 2026-09-28 at `e2fc169` plus the filing commit that adds it.
`git rm` this file and its prompt-map row in the commit that lands its result.
Reasoning need: high — two open facts must be settled by source reading before the design holds,
and the fix wraps rocket and colonist code paths with save-state consequences.

## Authority and outcome

The owner chose the fix shape on 2026-09-28 (quoted in [C120](../bugs/C120.md), "Fix shape"):
**K2 + E, no cap.** Do not reopen the shape or add a cap, timeout or count change; those were
considered and not chosen.

- **K2.** When an automated Earth-bound rocket is ready apart from departures, board every eligible
  colonist who can safely be taken now, through the game's own path for deportees who cannot reach the
  rocket, then let it launch. Colonists still walking or riding are released the way a manual Launch
  releases them, and catch the next rocket.
- **E.** A landed rocket with no destination drafts nobody.

**Done** means:
- a module on `main` implementing K2 and E, registered like its siblings (`items.lua`,
  `metadata.lua`, TestKit as applicable);
- desk controls under `tools/` that run the fix on and off against archived 1.1.1.405907 Lua and
  discriminate:
  - fix off: the pending count stays above zero under refilling inflow;
  - fix on: the rocket launches, and the boarded and released colonists are in clean states;
  - E: an idle rocket with no destination drafts nobody;
- C120 moved to `built` with its evidence field and header updated, and a `### Pending` entry in
  `perma/RELEASE_OUTBOX.md`.

## Starting state

Run `git log --oneline -5` and `git status --short`; peers share this tree. Re-derive every line
number below with `grep -n` on `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src` before
using it. The C120 entry holds the mechanism, citations and falsifying control, and the scratchpad
traces are not in the repo. Other records: `docs/agent/bugs/INDEX.md`, `docs/agent/facts/INDEX.md`
(EF-104 is the expedition draft).

## Settle first (C120 "Open before build")

These can refute the design; settle them in source before writing code.

1. **Manual Launch's release is clean.** For walkers (`LeavingMars` `rocket_left` branch), stopover
   riders (`StopDepartureThread`) and train riders (`GoToStation` legs), check that `leaving` ends
   false, transport tasks are released, and the colonist is eligible for the next rocket.
2. **The boarding fallback is safe in bulk.** `Colonist:LeavingMars`'s unreachable branch
   (`GetDehydratedData` → `insert(rocket.boarded, …)` → `CleanupLeavingColonist`): read
   `CleanupLeavingColonist` and `GetDehydratedData` whole and list every side effect (FIX_POLICY
   §1). The candidate filter is the expedition's (`CargoTransporterNew:GatherAvailableColonists`:
   `Idle`/`Abandoned`, or `CanChangeCommand()`, and no `thread_running_destructors`). Establish that
   the fallback is safe from every state that filter admits: residence, workplace, labels, a
   colonist on another map (compare `Unit:EnterTransporter`'s `TransferToMap`), the selection.
3. Also open, settle if the design depends on them: whether a committed stopover ride can hang
   forever; whether a train route leaves a stale stopover task on a second rocket; whether arriving
   Senior passengers are drafted on landing.

## Judgment delegated to you

Hook points, the "ready apart from departures" test, the per-colonist filter, how K2 treats
colonists already in `departures` or a stopover, and the desk-control design. Keep save residue to
none where you can; any game-time thread follows FIX_POLICY §1.4 (zero upvalues, orphan gate first).
Record your calls in the commit message.

## Scope

- **In:** the C120 module, its registration, its desk controls, C120's entry, one outbox entry.
- **Out:** C45 (a different error in the same function), other eligibility sources beyond sharing
  the code path, any draft cap, and in-game sittings. If a reading in the game is needed to ship,
  write it into C120 as a proposed SMRTK-preloaded sitting; the owner schedules it.
  Report other findings without editing them.

## Stops — report instead of building

1. Item 1 or 2 above fails in a way K2 cannot route around without a behaviour the owner did not
   choose (a cap, a timeout, stranding colonists).
2. The only workable hook is a whole-body replacement of a vanilla function; FIX_POLICY ranks
   it last, so bring the reason to the owner.
3. A peer has uncommitted work on the same module, registration lines or C120.

## Claim limits

"Desk-verified on archived 1.1.1 Lua" is supported. "Fixed in game" or `tested-*` is not, until
the owner plays it. Do not claim the fix-off stall was reproduced in game; only the desk model was.

## Working rules

- Use the todo tool before any write: one item per commit-and-verify unit, one in progress.
- Follow `CLAUDE.md`, `docs/agent/WORKFLOW.md` (committing in a shared tree, per-fix discipline,
  testing checklist) and `docs/agent/FIX_POLICY.md`.
- Invoke `doc-editing` before the entry and outbox edits and `smr-bug-library` for the status
  change. Run `python tools/doccheck.py --regen`, then doccheck GREEN; commit with pathspecs.
- If run unattended, a different owner-selected model audits the result before it enters the
  record.
