# hubset 06: prepare the verification sitting as a preloaded SMRTK sitting

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.

## Authority and outcome

Every member is built on `hubset`. Owner ruling 2026-09-24: **"One sitting only."** 07 is that
sitting. The owner verifies every member in it, once, in order, with nothing decided on the day.
Owner, 2026-09-24, on why this link was rewritten: *"all these commands are things that could have
been done in slots"* and *"smrtk has a build in 128x game speed for fire watch and fire after x in
game time."* The owner clicks; the attending session reads the log.

This brief **calls for preloaded slots**, so both halves of [tools/SMRTK.md](../../../../tools/SMRTK.md)
apply, including "Preloading a sitting" and its gates.

End state:

- The TestKit's `Code/80_AgentSlots.lua` rewritten for this sitting and committed in the TestKit repo:
  slots, triggers and `Run until` targets.
- 07's body filled in with a numbered script. Each step names the slot or button the owner presses,
  what they see, and how long it takes in real time.
- Numbered predictions, written before the run.
- A declared-VOID rehearsal of each new instrument on the desk, in which a scratch variant is shown
  to produce the refuting result.
- doccheck GREEN.

Open a live todo list before the first write.

## What the script must cover

For each member, fix on and fix off, with numbered predictions:

- **C114 / C115:** a natural interruption on a large dome's hub or passage (fire a worker, or switch
  off its work dome): no rescue ride for a colonist on the hub; an obsolete rescue already booked is
  dropped once the colonist is home; a remote colonist still gets its shuttle.
- **C116:** a colonist dumped on the hub walks off: marker cleared, outside timer runs; a colonist on
  the ramp keeps shelter.
- **C117:** salvage one busy hub spoke with a sibling live: in-flight colonists land on the hub.
- **C42:** traverse a dome-to-dome passage, then salvage it: no unrelated colonist is teleported;
  `C42STALE` reads zero after traffic. Check 99's inbox first: C42's premise is under an owner
  decision (hubset 03's note).
- **F127:** a rerouted arrival into a full dome appears on the Homeless list.
- **C111:** an own-home rescue shows the approved text; a real relocation still names its
  destination. This is the one step the owner reads on screen: give them the colonist to select, as
  a pinned or auto-selected unit, never a search.
- **P3:** nothing to play; `tools/bodycheck.py` passes on the branch.
- **04's live readings:** every numbered reading link 04 left in this inbox, run from a slot, with
  its refuting value.

## How the sitting is built (FIXED: owner requirements)

1. **Slots, not typing.** Every read, arm and act is a slot or trigger in `80_AgentSlots.lua`. A
   step that has the owner type a console line needs a stated reason in 07 why a slot cannot do it.
   A slot that fails mid-sitting is not patched with improvised console code. If the owner
   explicitly asks for one, record the exact text that ran in the entry that cites its result.
2. **No waiting in real time.** Every wait is a trigger or `Run until` at top speed (SMRTK's Run
   page). The same applies to a wait for game minutes, for shifts to turn over, or for a state to
   appear: arm a trigger that takes the reading when the state occurs. Never ask the owner to watch
   for a state among many objects.
3. **Owner-seat read.** Before close-out, read 07 as the owner at the keyboard, not as the attending
   session. For each step, confirm: which button they press, where the result appears (or "nothing
   for you; the agent reads the log"), and its real-time cost. Put the total in owner minutes at the
   top of 07, and say what drops first if it runs long.
4. **Predictions can fail.** Each prediction names the result that refutes it. The desk rehearsal
   shows that the instrument can produce that result: run a scratch variant, and require the
   prediction to read refuted. A category that cannot tell objects apart (a building class instead
   of an identity, or a height test every unit passes) is not an instrument.
5. **API shape is counted, not stubbed.** For every game function a slot calls, count its call
   shape in the archived 1.1.1.405907 tree (bare calls against `obj:Method(` calls). A stub run is
   not evidence that an API exists. `MapGet` and its family are map methods (`map:MapGet(...)`),
   not globals.

Everything else here is a DEFAULT. Depart from it with a reason stated in 07.

## Fixtures and junction

Use the reporter's save (TheGodUncle's, `New Horizons 2 83`) where it shows the shape (Brussels and
its hubs). Use the phase 2b fixture (`docs/agent/reports/PLAYTEST_PLAN_1.1.1_2026-09-23.md`,
"Phase 2b") or a new small colony where a controlled layout is needed. Re-confirm each fixture's
layout at prep time. Follow `docs/agent/support/CO_RUNS.md` and WORKFLOW's test-design rules. Where
those clash with the FIXED list above, the owner's requirements win.

The sitting points the junction at the worktree. Write the exact repoint and restore commands into
07, including `cmd /c rmdir` for the link (never `Remove-Item -Recurse` on a junction). Add a
read-back that the game loaded the branch: the pack's log lines for each new module.

Run `tasklist /FI "IMAGENAME eq Mars.exe"` before any TestKit `Code/` write. If the game is running,
finish the document work and wait.

## Scope

- **In:** 07's script, predictions, `80_AgentSlots.lua`, any TestKit probe the script needs, and
  the rehearsal.
- **Out:** any code change to a member. A defect found while preparing is routed to its link's entry
  and 99's inbox, not fixed here.

## Stops

- A member cannot be exercised without a fixture the owner must build by hand: price it and route
  the choice.
- A member cannot be driven from a slot: say why, price the typed alternative in owner minutes, and
  route the choice.

## Close-out

Append your outbox to 07's inbox and 99's. It carries both HEADs (main and TestKit), the slot labels
and the owner-minute total. Strike your row, `git rm` this file, and commit on `main`.

## Notes from upstream
