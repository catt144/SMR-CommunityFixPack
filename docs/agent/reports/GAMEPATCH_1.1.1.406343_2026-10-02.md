# Game patch 1.1.1.406343 (build 25579348): sweep skipped by owner ruling

## Must_Read_Header

This is a ruling record, not a patch sweep. No `patchcheck.py` block exists for this build and
no count below is typed from one. A session that sees `--emit-fingerprint` report installed
build 25579348 reads this before raising `perma/GAME_PATCH_PROMPT.md`.

## The ruling

Owner, 2026-10-02, verbatim: *"I skipped this patch because it was a narrowly targeted hotfix
for linux users."*

So: the 1.1.1.406343 sweep is **not owed**. Do not raise it as a gap, a checklist item or an
owed step; do not run the prompt on this build on your own initiative.

## What is still true, and what reopens this

- The tree is archived at `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.406343\Src`, so any
  line read on the installed build is cited against it, with the build named.
- **The hotfix changed none of our pinned bodies.** Measured 2026-10-02:
  `python tools/bodycheck.py` against the live install (build 25579348) and
  `python tools/bodycheck.py --src "B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src"`
  print the same summary, `3 BODY-CHANGED, 1 DEFECT-GONE, 3 NO-DEFECT, 11 SRC-NONE, 188 OK`
  over 206 rows and 47 modules, and the same four non-OK rows by name:
  `Fix_HabitatExpeditionDraft.lua:30`, `Fix_HabitatExpeditionReturn.lua:15`,
  `Fix_RocketInteractGuard.lua:62` (all three on record in
  `GAMEPATCH_1.1.1.405907_2026-09-23.md` and the adjudication) and `90_SaveSanitizer.lua:82`
  (the F48 `DEFECT-GONE` its own header marks as expected and correct). The rows predate this
  build; nothing here is new.
- Reopen only on evidence: a `BODY-CHANGED` or `DEFECT-GONE` row, a log line from a module
  failing its self-check on this build, or a field report naming it. Then run the prompt and
  write the normal `GAMEPATCH_<build>_<date>.md` beside this one.
