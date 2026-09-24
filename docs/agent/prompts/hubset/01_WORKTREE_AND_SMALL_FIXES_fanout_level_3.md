# hubset 01: branch, worktree and the four small members (fan-out)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.

## Authority and outcome

The owner ruled that the hub set ships as one release and that P3 and F127 (was P2) join it. This
link builds the four members that need no new measurement: P3, C42, F127 and C111. End state:

- A `hubset` branch cut from `main` at your start, checked out in the worktree
  `B:\Dev\SMR\SMR-BugFixPack-hubset` (`git worktree add ../SMR-BugFixPack-hubset -b hubset`). If a
  `hubset` branch or that folder already exists, stop and report; do not reuse or delete it.
- The four members built and committed on `hubset`. C42, F127 and C111 each carry a desk harness
  under `tools/` that passes, with a control that fails with the fix removed; P3 passes
  `tools/bodycheck.py`.
- Each member's entry on `main` gets a dated build section: branch SHA, harness, what the desk proves,
  what still needs play.
- Doccheck GREEN in both trees.

## How to run it

The four members touch different targets, so they suit parallel subagents, each given one member,
its entry and this brief's facts. You coordinate: each subagent writes its module or edit and
harness in the worktree and reports verbatim. **You alone** edit the shared files, `metadata.lua`'s
`code` list and `items.lua`, one change at a time, and commit. Commit the plan and each subagent's
verbatim report under `docs/agent/reports/hubset/agents/` on `main` as they land; mark an unrun
subagent NOT RUN. A resumed run continues from what is committed. Open a live todo list before the
first write: one item per member plus the worktree and the close-out.

## The members

**P3: the two missing pins in `Fix_VacuumWalks`.** The module wraps `Colonist:GetNextMigrationLeg`
and the global `IsInWalkingDistDome` but pins only the two caller bodies. Add `SRC:` pins for both,
in the existing MANIFEST format, hashed the way the existing pins were, and confirm with
`tools/bodycheck.py` that every pin in the module verifies against archived `1.1.1.405907`. Header
metadata only: no behaviour change. The cross-check located the bodies at `Colonist.lua:3709-3717` and
`Dome.lua:299-319`; re-derive them.

**C42: the raw holder clear.** Read [C42](../../bugs/C42.md), especially its 2026-09-24 section.
`PassageBase:TraverseTunnel`'s destructor ends a dome-side exit with a raw `unit.holder = nil`
(`Lua/Passage.lua`, now :1234), skipping `OnExitHolder`, so the last element keeps a stale entry.
The fix direction in the entry is to route that exit through `SetHolder`. The destructor is a
closure inside a blocking method, so work out the least invasive technique that reaches it
(FIX_POLICY §1) and its save and blocking-frame disposition (§3a). If the only route is a full copy of
`TraverseTunnel`, stop and report the cost instead of building it: C117 (link 03) and C116 (link 05)
also touch traversal, and a copy here would fix their shape for them. The entry's narrower
mitigation, a synchronous filter of invalid or mismatched members before the element's `Done`, is an
acceptable first build if the root route is too invasive; say which you chose and why.

**F127: our arrival reroute's orphan booking.** Read [F127](../../bugs/F127.md). First validate its
full-destination branch on the desk: a rerouted arrival into a full dome keeps `reserved_residence` in
the rejected dome and is missing from the Homeless label. `tools/desk_c83_arrivals.py` already drives
this code; extend it or add a sibling. If the desk refutes the branch, stop that member and route the
facts. If it holds, cancel or move the reservation inside the C83 branch of
`Code/Fix_ArrivalDeaths.lua` (:485-486 at `21a16ec`), leaving the unrerouted path native.

**C111: the rescue text.** Read [C111](../../bugs/C111.md) and its 2026-09-24 section. An own-home
rescue ride reads "Moving to a new Dome: <home>". Make an own-home rescue read as returning or
rescue, while a real relocation still names its destination. Prefer command-text or getter work
(§1.3); do not copy a movement command. Keep the destination hyperlink, localisation (§6) and reload
behaviour. The wording is the owner's to approve: build your best proposal, put the exact strings in
your outbox and in 99's inbox, and route an approval item to `docs/PLAYTEST_CHECKLIST.md` ("build it,
not locked; the audit reviews"). Do not wait for the answer.

## Scope

In: the worktree, these four members, their harnesses and their entries' build sections. Out: C114,
C115, C116, C117, any load-order change, the VacuumWalks load-time guard, `metadata.lua`'s description
and version, and any release surface.

## Stops

- A member needs a full-body copy of a blocking method, or a new persisted field: report its cost.
- The desk refutes F127's branch, or a member's target shape differs from its entry: route the facts.
- The worktree or branch already exists, or `main` carries a foreign uncommitted change to a file you
  must write.

## Do not claim

A desk pass is not play: no entry goes past `fixed`-pending-play. C111's wording is a proposal until
the owner approves it. Pins verify shape, not that the wrapper still composes.

## Close-out

Append your outbox (branch SHA, per-member result, anything 02, 03 or 05 must know about shared
targets) to 02's inbox and 99's, strike your row in the README, `git rm` this file, and commit those
on `main` together.

## Notes from upstream
