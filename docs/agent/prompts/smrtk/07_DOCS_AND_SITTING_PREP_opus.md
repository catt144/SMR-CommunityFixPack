# smrtk 07 — the documentation, the standing slot prompt, and 08's preparation

Link 07 of `smrtk`. README rules 1–20 are yours. After 03, 03b, 04, 05 and 06 have all closed (read all five
outboxes first — they carry the final button lists).

## Job A — the rules the owner asked for ("we need rules about cheats in the documentation")

1. **`agent/WORKFLOW.md` § "Cheats on playtest saves"** — append a dated block: the toolkit replaces the vanilla menu
   for playtesting; `[SMRTK] SMRTK_<Verb>` lines are **intentional test actions, attributed by construction — never
   ask the owner about one**; a vanilla `ObjCheat`/`Cheat` marker in a NEW log is now the exception worth one
   question; the achievement-eligibility strip is the detector for a tainted save. Cite `EF-095`.
2. **`agent/WORKFLOW.md` § "Writing in a shared tree"** or the reading path — one line: `80_AgentSlots.lua` is
   agent-owned, rewritten per sitting, never edited by a build link.
3. **`docs/PLAYTEST_HELP.md`** — replace § "Cheating without contaminating results" and amend § "Console: what works…"
   with the panel: plain numbered steps (memory: player-facing steps must be plain), the hotkey, each page in one
   line each, F9, "you never need the Mod Manager open to test", and the two things the panel cannot do (clear an
   achievement — `EF-094`; run code from a string — `EF-096`). Retire the "load with the console open" workaround
   wherever it is written (grep `console` across `docs/` including `archive/` on purpose; do not edit the archive).
4. **`C:\Dev\SMR-BugFixPack-TestKit\README.md`** — the panel section, the file map, the slot contract.
5. **`prompts/perma/SMRTK_SLOTS.md`** — the standing prompt an agent fires to **pre-load a sitting**: read the sitting's
   brief, write `80_AgentSlots.lua` (legs as slots: MARK → set up → act → DUMP → MARK), write the predictions, hand
   the owner one line: "start the game; the Agent tab is loaded". Add its row to `prompts/README.md` `perma/` table.
6. **`agent/FIX_POLICY.md`** — nothing; the toolkit is not a fix. Say so in 99's inbox if you were tempted.

## Job B — 08's preparation

7. **Predictions** `reports/SMRTK_FULL_SITTING_PREDICTIONS.md` — numbered, per button class (not per button): the
   log line expected, and for the stamp (06's inbox) the placed/skipped counts predicted from a dry run.
8. **08's script** into `08_FULL_SITTING_owner.md`'s inbox per rule 13: every page, one representative of each button
   class, a Delete and a Destroy on scratch buildings, a save/load round trip through slot A with the guard tripped
   once on purpose, one trigger firing, one screenshot+mark opened afterwards, one capture + stamp, a run-until.
   Price it in minutes. The fixture: a 1.1.0 colony with a dome, a depot, a drone hub and a rocket in flight.

## Scope fence

IN: the files named above. OUT: any code (route a defect found while documenting to the link's grave + 99's inbox and
fix it only if it is a one-line label).

## What may NOT be claimed

That any documented behaviour was seen in play — 08 sees it; write "as built" not "as tested".

## Close-out

`python tools/doccheck.py` GREEN (PROMPT MAP gate: the new perma row + file land together). Commit per unit.
Outbox to 08 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (03, 03b, 04, 05, 06 append here)
