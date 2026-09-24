# hubset 06: prepare the verification sitting

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.

## Authority and outcome

Every member is built on `hubset`. The owner verifies them in one attended sitting (07). This link
writes that sitting so it runs once, in order, with nothing decided on the day. End state: 07's body
filled in with a numbered script, predictions and the console lines to type; any TestKit probe it
needs, committed in the TestKit repo; a declared-VOID rehearsal of each new instrument on the desk;
doccheck GREEN. Open a live todo list before the first write.

## What the script must cover

For each member, fix on and fix off, with numbered predictions written before the run:

- **C114 / C115:** a natural interruption on a large dome's hub or passage (fire a worker, or switch
  off its work dome): no rescue ride for a colonist on the hub; an obsolete rescue already booked is
  dropped once the colonist is home; a remote colonist still gets its shuttle.
- **C116:** a colonist dumped on the hub walks off: marker cleared, outside timer runs; a colonist on
  the ramp keeps shelter.
- **C117:** salvage one busy hub spoke with a sibling live: in-flight colonists land on the hub.
- **C42:** traverse a dome-to-dome passage, then salvage it: no unrelated colonist teleported;
  `C42STALE` reads zero after traffic.
- **F127:** a rerouted arrival into a full dome appears on the Homeless list.
- **C111:** an own-home rescue shows the approved text; a real relocation still names its
  destination.
- **P3:** nothing to play; `tools/bodycheck.py` passes on the branch.

Use the reporter's save where it shows the shape (Brussels and its hubs), and the phase 2b fixture
(`docs/agent/reports/PLAYTEST_PLAN_1.1.1_2026-09-23.md`, "Phase 2b") or a new small colony where a controlled layout is needed; re-confirm each fixture's layout at prep
time. Follow `docs/agent/support/CO_RUNS.md` and WORKFLOW's test-design rules. Price the sitting in
owner minutes and say what drops first if it runs long.

The sitting points the junction at the worktree. Write the exact repoint and restore commands into
07, including `cmd /c rmdir` for the link (never `Remove-Item -Recurse` on a junction), and a
read-back that the game loaded the branch (the pack's log lines for each new module).

## Scope

In: 07's script, predictions, probes and rehearsal. Out: any code change to a member. A defect found
while preparing is routed to its link's entry and 99's inbox, not fixed here.

## Stops

A member cannot be exercised in the game without a fixture the owner must build by hand: price it and
route the choice.

## Close-out

Append your outbox to 07's inbox and 99's, strike your row, `git rm` this file, commit on `main`.

## Notes from upstream
