# Chain prompt 1 — prep (game closed, no launch)

**Read `README.md` in this folder first — binding chain rules apply.**
Start with `git log --oneline -10` + `git pull`. Todo list up front, updated
per item. Everything here is game-closed; the launch belongs to prompt 2.

## Jobs

**Job 1 — re-derive the routes (recorded facts are claims).**
Read `agent/bugs/F07.md`, `F15.md`, `C39.md`, `F85.md`, the checklist's PT-15
section, and the README's Src citations. Re-derive, marking each line
Src-verified or trust-carried:

* **PT-15 reads.** What exactly does the sitting read off a Light Trap and
  the power grid when the wisps are freed? Find the shipped fix's numbers
  (`Code/` WispRewards module + its entry) and the vanilla read surface
  (trap object fields, grid production). Script the read as numbers off
  named objects, not screen impressions — the owner's eyes are the verdict
  tier, the instrument is the record. Same for F15's destroy-mode research
  reward (rider only; needs a SECOND trapful, may be N/A).
* **C39 reads.** The observation set, per the entry: for one Workshop
  (ArtWorkshop family) and one in-family Service control (Diner/Spacebar,
  same dome): `max_workers` per shift (before/after law), workers present,
  `performance`, and the Comfort the shift pays (`ArtWorkshop.lua:24-27`
  route). Decide the shift-boundary question from Src: WHEN does
  `GetWorkshiftPerformance` recompute (`Workplace.lua:205-217` callers) —
  the sitting must know whether readings need a shift change and say so in
  the brief's timeline.
* **The countdown read.** Design the sequence-player read that reports where
  the St. Elmo trigger is on the live save: approval passed or not, and if
  armed, how much of the 10–20-sol sleep remains (the seq thread's wake time
  vs `GameTime()`). First-execution discipline — this read has never been
  run; find the actual tables (`SequenceListScript`/seq player state) in Src
  and print raw values beside every derived number.
* **F85 check.** One line: press Ctrl-F9 in a colony; the read is whether a
  quicksave lands (disk listing + in-game notification), EF-049/EF-050 aware
  (witness = the on-disk file). Nothing else — the decision is the owner's.

**Job 2 — author the instruments, parked.**
`97_CP15Common.lua.txt` + `98_CP15Sitting.lua.txt` + `CP15_ARM.ps1.txt` in
this folder. Resurrect from `e5dca6f`'s unattended-2 harness (gate, Load/Save
with the EF-050 guard, `Applicable`, `Try`/`TryYield`, `ErrorWatchNote`, the
MODE/REHEARSAL pattern) — a sitting is attended, so the payload is a menu of
callable legs (`CP15.CtrlF9Note()`, `CP15.C39Before()`, `CP15.C39Enact()`,
`CP15.C39After()`, `CP15.C39Revert()`, `CP15.MysteryWhere()`,
`CP15.TrapRead()`, …) rather than an autostarting flow — the owner plays
between calls. Every leg prints R7 effect reads and its FORCED/ORGANIC label.
ARM gate: C11 script file, resolution cross-check (every `CP15.*` the brief
tells the agent to call must be defined), TEMPORARY markers, both-repo sweep.

**Job 3 — stage and pre-flight.**
* Stage `CP15STAGE.savegame.sav` as a byte-copy of `PT-15.savegame.sav`
  (verify MD5s of all THREE protected files first and record them).
* Take the PRE-launch save-dir listing (the EF-051 baseline for item 4 —
  expected 55 + `CP15STAGE` + anything the owner saved since; LIST it, don't
  assume).
* Checklist edits: PT-15 section gets its sitting Requirements line (the
  staged copy, ultra speed, what the owner does vs what the rig reads);
  the F85 decision item gets the re-route note (appended, the owner's text
  untouched); C39's entry gets a "sitting scheduled" line. doccheck GREEN.

**Job 4 — outbox.** Append to `02_OPUS_SITTING.md` `## Notes from upstream`:
the verified read surfaces with citations, the C39 shift-boundary answer, the
staged-file names, the listing baseline, anything that surprised you. Commit;
delete this file in the same commit.

## Stop conditions

- A read surface cannot be Src-verified (field moved, method gone) → mark the
  leg's read DEGRADED with what IS readable; never ship a guessed reader.
- `PT-15.savegame.sav` missing → STOP, tell the owner; nothing to stage.
