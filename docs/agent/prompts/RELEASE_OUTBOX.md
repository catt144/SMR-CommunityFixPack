# Release outbox — player-facing changes staged for the NEXT upload

**What this is.** A running ledger of every change that has landed in the tree
**since the last upload** and must appear on a player surface when the next
version ships. It is the single answer to "what is in the next release?" — the
`last_changes` change note, the new fix-list rows, and the store-card count word
all come from here. `RELEASE.md` reads it, applies every entry to the surfaces,
and **clears it** (moves the entries to *Released* below) once the upload is done.

**Live tree version:** `metadata.lua` `version` — read it, never hand-set (H-02).
**Live count word:** whatever `metadata.lua`'s `description` currently says
(`grep -o 'Eighty[a-z-]* repairs' metadata.lua`). Each pending fix that has a
player surface bumps it by one on release.

## How to use it
- **When a player-facing fix lands** (added, retired, or materially re-scoped —
  the `PUBLIC_SURFACE_SWEEP.md` §0.4 test): append a `### Pending` entry below,
  filled in. A pack-internal fix that never shipped broken (the F107 case) gets
  **no entry** — it has no player surface.
- **When the owner is ready to upload:** run `RELEASE.md`. It consumes every
  `### Pending` entry, then rewrites this file with those entries moved under
  *Released in vN* and the *Pending* section empty.
- ⛔ Never delete a pending entry by hand — that silently drops a fix from the
  change note. Retire one only through a release (it moves to *Released*) or by
  recording explicitly why it was withdrawn.

---

## Pending — goes out with the next upload

### Pending · F110 · `Fix_JumboCaveReinforcementWedge`
- **Symptom sentence (player words, drives the fix-list row + change note):** A
  Jumbo Cave mystery could get stuck forever "clearing the site of waste rock" —
  a waste rock the drones could not reach blocked the Reinforcement, so it never
  built and the mystery never completed.
- **Change-note line (`last_changes` style):** `- Fixed a base-game issue where a
  Jumbo Cave's Reinforcements could stay stuck clearing waste rock forever — a rock
  the drones could not reach blocked the site and the mystery never completed.
  Safe to install on a save where this is already happening; the stuck rock is
  cleared automatically.`
- **Fix-list section:** mysteries / storylines (a player meets it as a stuck
  underground mystery, not as a drone or construction bug).
- **Headliner?** Candidate yes — a permanent, unrecoverable mystery soft-lock is
  the kind of thing that hardly-miss headliners are for; the sweep decides.
- **Judgment call?** No — a mechanical repair (no rebalance).
- **Count impact:** +1 (bumps the card's count word by one).
- **Module:** added to `items.lua` + `metadata.lua` `code` list already (H-10).
- **Entry / evidence:** `agent/bugs/F110.md`; verified attended
  (`archive/f110_attended_…16.41.16.log`).

---

## Released — history, newest first (cleared here by RELEASE.md)

*(none yet — the v4 release predates this ledger. The first entry to land here
will be whatever ships in the version after v4.)*
