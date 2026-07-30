# Challenge prompt — your reachability audit got one wrong. Here is the evidence.

Paste into a fresh session, any Claude model. **Delete this file once the
challenge is answered and its findings are recorded.**

---

You produced `docs/REACHABILITY_AUDIT.md` (commit `3398031`) — 66 fix modules
plus 2 sanitizer passes, tiered R1/R2/R3/R4/U, a DELETE shortlist, and a drafted
FIX_POLICY §4 amendment. The audit's premise was catching fixes that repair
things a player cannot reach.

**Credit where it is due first:** the F49(a) lead-pass block is exemplary. The
`InstantTracks`-const search, the four track-mode entry points, the single
`PlaceTrackLine` caller, the zero track cheats — that is the standard, and it is
not in question here.

**One verdict in the same module is wrong**, and it was found by the project
owner at the keyboard within hours of the audit landing. The evidence is below.
Your job is not to re-find it. Your job is to explain **why your method
produced a confident wrong answer**, and to find everything else it did the same
thing to.

## The verdict at issue

Your table lists **F49(c)** — the demolish-mode guard on
`TrackGridElement:SelectionPropagate` — as **live R2**, and uses it (with (d))
as the reason to keep `Fix_TrainMinors.lua` despite (a) being R4.

Note *how* that verdict was reached: (a) received a full lead-pass enumeration
block. **(c) received none.** Its tier appears only in the verdict table and in
a passing clause justifying a different fix's recommendation. It was asserted,
not audited.

## The evidence you did not have

Observed live, 2026-07-30, on a 305-sol colony with the pack active:

1. **Salvage mode targets objects, never hexes.** A bare hex cannot be clicked
   and is not drawn.
2. **The cursor always names what it will remove** — `Salvage Track`,
   `Salvage Train Station`, `Salvage Power Cable`, `Salvage Wind Turbine`, and
   so on for everything on the map. Line-drawn objects add
   `CTRL + click — Salvage entire length`.
3. **The word `Salvage` alone in red means "no action permitted"** — nothing
   targetable under the cursor.
4. **The transition from `Salvage Train Station` to `Salvage Track` is
   seamless, exact to the millimetre, with no third state in between.** Two
   screenshots a few pixels apart flip cleanly between the two, each correctly
   named.
5. **The player cannot salvage a station's own track without salvaging the
   station.** No exposed control distinguishes them.

And from source, confirming the elements are real rather than absent:
station connector elements are created with `station = self` at the station's
`Trackconnector` spots (`TrainTransport.lua:132-139`). They exist. They are
station-owned. They sit flush against the station body.

## What that makes of the fix

The propagation to `self.station` that F49(c) treats as a defect **is what makes
that boundary continuous.** It is why the handoff is seamless and why a
station's track cannot be salvaged out from under it. It is designed behaviour.

The guard nulls that propagation in demolish mode. Had it engaged it would have
carved a **dead band** into the boundary — a strip where the cursor reads red
`Salvage` and nothing is targetable. Best case it changes nothing observable;
worst case it degrades the interface. There was no wrong outcome for it to
prevent.

F49(c) is closed `wontfix` by user decision and the guard is removed. That
decision is made; do not re-argue it. Explain the method failure.

## Task 1 — why did the method produce this?

Not "why was (c) unenumerated" — that is the surface answer. Go deeper:

Your evidence base was source code. Reachability is a claim about what a
**player** can reach, and parts of that are decided by things the Lua does not
tell you: which controls the interface exposes, how input resolves to objects,
what the game shows before the player commits, and **whether two things a player
might want to address separately are separable at all**.

For a defect of this shape, source reading does not leave you uncertain. It
gives you a confident wrong answer, because the code path plainly exists and
reads as reachable.

State this failure mode precisely enough that the §4 amendment can guard
against it.

## Task 2 — coverage self-audit

Go through every row of the verdict table. **Does a block exist below it that
enumerates that fix's own call sites and interrogates its own preconditions?**
Or was the tier asserted in passing, inherited from the BUGS.md entry's framing,
or carried over from a *sibling item in the same module*?

Produce the list of verdicts carrying a tier with **no enumeration of their
own**. Every one is unverified whatever tier it wears.

Your own prompt required an R4 verdict to state what was searched. **Apply that
symmetrically.** An unenumerated R1 or R2 is exactly as unproven as an unstated
R4 and far more dangerous, because "keep, it's live" is the verdict nobody
revisits. Bundled fixes are the prime suspects: enumerating one third of a
module proves nothing about the other two thirds — which is precisely how this
one got through.

## Task 3 — the blind-spot list

Identify **every verdict whose correctness depends on runtime or interface
behaviour not determinable from source**: UI affordances, hit-testing and
selection resolution, cursor and confirmation feedback, input modes, anything
where "the code path exists" and "a player can address it" come apart.

Mark each. For each, name the single observation that would settle it. This
list is the most valuable thing the challenge produces — it is the standing
list of verdicts that need eyes, not greps.

## Task 4 — your tier vocabulary is incomplete

R1/R2/R3/R4/U all classify **how reachable** a defect is. Every one of them
presupposes the shipped behaviour is defective, and the audit never tests that
presupposition. F49(c) is what happens when it fails: fully reachable, entirely
intentional, and the "fix" fights the design.

Propose the missing category. Then re-scan the table for other entries that
belong in it — particularly fixes whose BUGS.md provenance is `src-diff` and
whose "defect" is a behaviour a player would have to *notice and object to*
rather than a crash, a wrong number, or a dead code path.

Revise the drafted FIX_POLICY §4 amendment accordingly. It must now require
both a reachability tier **and** a positive statement that the shipped
behaviour is unintended — with the injection-is-evidence-for-R4 principle kept.

## Constraints

- Game source is **read-only**:
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`. Shipped build
  IS Src (fpk parity proven — `docs/ENGINE_FACTS.md`).
- **Change no fix code.** Findings only; code changes stay the owner's call.
  (The F49(c) guard is already removed — that one is done.)
- Do not run the game. The owner is not available to run observations; if a
  verdict can only be settled at the keyboard, say so and name the observation.
  Recognising which verdicts are in that class is most of Task 3.
- Read `docs/ENGINE_FACTS.md` before reasoning about class or hook behaviour.
- Do not trust `BUGS.md`'s framing, and trust a fix's own header comment even
  less — that is the *author's* hypothesis about why the code is wrong.
  F49(c)'s header asserted a defect that was never one.

## Deliverable

Append **"Challenge review 2026-07-30"** to `docs/REACHABILITY_AUDIT.md`:

1. Task 1's failure-mode statement.
2. The unenumerated-verdict list.
3. The source-blind-spot list, each with its settling observation.
4. The missing tier category, entries reassigned to it, and the revised §4
   amendment.
5. Any other verdict the above shakes loose.

Commit and push with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`.

Do not soften it. The audit used direct language on the fixes it examined; use
the same language on the audit.
