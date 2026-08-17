# D·02 — stack the deck and stage the colony · UNATTENDED · owner cost ZERO

**Read `README.md` first — ⛔ THE LINE and the ⚖️ discriminator bind you.**
Then `STATE.md`, then this, then your `## Notes from upstream`.

## 0 · Staleness check
```
git log --oneline -10
git pull
```

## 1 · 🗒 Live todo list from your first action.

## 2 · The job — generate the venue, hand the owner a save

### Job 1 — the elevated-density generation
Using 01's parameter and 01's winning seed: generate the same map with the
**deposition density raised**, and let the game place every rock.

⛔⛔ **THE LINE, restated because this is the prompt that could cross it:** you
raise a number the game's own scatter reads. **You do not choose a single rock's
position.** If you find yourself writing a coordinate, stop — you have changed
the experiment into one that cannot answer the question.

Record, against 01's baseline: rock count near the cave, the distribution, and
whether the cave's own geometry is unchanged (it must be — same seed, same
terrain; only scatter density moved). **If the terrain differs, the comparison
is void** and you re-plan rather than proceed.

### Job 2 — verify the detector is live on this colony
Chain A armed the `DroneApproach` detector. Prove it on THIS save before handing
it over: `EF-058`, every carrying class patched, wiring proven **off live
instances**, and the neighbour-hex capture demonstrably firing. A detector that
is armed but silent is indistinguishable from one that is broken.

⛔ **If you cannot demonstrate it firing, say so plainly in the handover.** The
owner is about to spend a playthrough segment on this; they are entitled to know
whether the instrument is proven or merely installed.

### Job 3 — stage it for the owner
Get the colony to the point where the owner's part is as short as possible:
underground unlocked, the `JumboCaveReinforcementBuilding` tech available or
granted, drones and resources sufficient to actually build the Reinforcements.
**Cheats are normal on playtest saves** (owner rule 2026-08-12) — use them, name
every one used in the handover, and flag any reading a cheat could touch.

⚠️ **Every cheat used is a confound only where a reading intersects what it
changed.** Drone count and resources do not touch pathfinding. Say so explicitly
rather than leaving the owner to wonder.

### Job 4 — write the owner's script
`03_SITTING_owner.md` is a **priority queue, not a schedule**
(`CHAIN_METHOD` §3). Fill it in with: the save name, the exact steps, what to
look at, and — ordered so a truncated sitting still banks the decider first.
Re-confirm the fixture exists **at handover time**, not at authoring time; a
prep-measured fixture has evaporated before and cost 25 minutes of owner time.

## 3 · Predictions before the run
Numbered, falsifiable, committed and pushed first. Include: expected rock count
at elevated density, expected number of stranded rocks (**your honest prior may
be zero** — say so), and the discriminator you expect to fire.

## 4 · Scope fence
**IN:** the elevated-density generation, verification, staging, the owner script.
**OUT:** ⛔ playing the colony far enough to place the Reinforcements yourself —
that is the owner's part and the whole point of 03 · ⛔ any fix code · ⛔ hand-
placing a rock · ⛔ modifying the game installation.

## 5 · Stop conditions
- Terrain differs between baseline and elevated run → **the comparison is void.**
  Re-plan; do not hand over a save whose control is broken.
- The detector cannot be shown firing → hand over **with that stated**, or stop.
- Any `[LUA ERROR]` naming our code → void, fix, re-arm, archive the voided log
  beside the good one.
- `EF-056` fires → restore from the pre-copy, disclose it, continue.

## 6 · ⛔ What may not be claimed
- ⛔ **"The deck is stacked fairly."** State the density multiple and let the
  audit judge whether it stayed inside the game's own distribution.
- ⛔ **Any trigger claim.** Even a stranded rock found during staging is
  *unadjudicated* until the discriminator is applied — and that is 04's call,
  not yours.
- ⛔ **"The save is ready"** without naming every cheat used and every step the
  owner still has to perform.
- ⛔ `tested-*` of any flavour. Nothing here is a fix.

## 7 · Close-out
One commit: `03_SITTING_owner.md` filled in with the real save name and steps ·
outbox to `04_AUDIT` · staged save named and disclosed · logs archived
`git add -f` · manifest row struck · `git rm` this file · doccheck GREEN · grave
named · push.

⭐ **And put the sitting on the checklist** — `WORKFLOW` R10: an owner-facing
ask recorded only in an agent doc *is not considered asked*. One line, plus what
it costs them, plus the pointer.

## Notes from upstream
