# Audit the opt-in pack's move to `B:\Dev\SMR`

**One-off, adversarial.** Fire in a fresh session after `MOVE_OPTIN_high.md` reports done. You did
not do that work and you do not fix it: you grade it, and a FAIL is a useful result. ⛔ Do not run
the mover's commands again as your method — re-running a copy proves a copy; you are looking for what
it missed. Delete this file and its `prompts/README.md` row in the commit that lands your report.

Root a session at `C:\Dev\SMR-BugFixPack` (it has not moved). The trees under audit are
`B:\Dev\SMR\SMR-OptInPack` and `B:\Dev\SMR\SMR-Assets`, with `C:\Dev\SMR-OptInPack__MOVED_20260921`
and `C:\Dev\SMR-Assets__MOVED_20260921` still present as the originals.

**Write nothing outside your report** (`docs/agent/reports/MOVE_OPTIN_AUDIT_20260921.md` in the fix
pack) and run no writing git command anywhere except the commit that lands it. If you find a defect,
it goes in the report with the command that shows it — you do not repair it, and you do not touch the
moved trees at all.

## What the move was supposed to achieve

The owner, 2026-09-21: all SMR content moves to `B:\Dev\SMR`; only a repo sits at that root; the
opt-in pack and its assets move first because the train hub build is on hold until they land. The
mover's brief is `MOVE_OPTIN_high.md` (read it) and the path inventory it builds on is
`docs/agent/support/MOVE_PATH_INVENTORY_20260921.md` in the moved repo (`baaefd1`): **5 editor-held,
29 in scripts, 13 in config, 134 in prose** on that date.

**Another seat owns part of the work**, and its items failing is NOT a defect of this move: the five
mod symlinks in `%APPDATA%\Surviving Mars Relaunched\Mods\`, the five editor-held paths under
`SourceData/`, the dev mod's test scripts, and the verification import. The mover was required to
LIST those, not fix them. Judge whether the list is complete and correct, not whether the items are
done. Likewise the Blender proof JSONs' `command` fields and the `_before_claude_pass2_20260918/`
snapshot are evidence of past runs: rewriting them would be the defect.

## What to establish, each with the command that shows it

1. **Nothing was lost.** File counts and total bytes, moved tree against its `__MOVED_` original, for
   both trees. Then the part a count cannot catch: `git fsck`, HEAD sha, every remote, every tag
   (`hub-model-final-untextured`, `hub-centre-lights-20260921`) and the working tree's dirty set —
   the train seat had files in progress and they must still be there, uncommitted and unchanged.
2. **Both trees actually work where they now live.** doccheck run from the new opt-in root, GREEN,
   with its selftests, PACK IGNORE PARITY and the LOCAL gate. The fix pack still GREEN. The pack
   predictor still excludes `local/` and `scratch/`.
3. **The path sweep, counted both ways.** Re-run the inventory's own grep over the moved trees and
   report what is left BY CLASS, naming who owns each survivor. A survivor inside the other seat's
   boundary is expected; a survivor in prose, a `docs/` map, `.claude/settings.json` or a script the
   mover owned is a finding. Also grep for the NEW path in the trees that did not move: a fix pack
   pointer still naming `C:\Dev\SMR-OptInPack` is a finding, and so is a record that was rewritten
   when it should have been left as a record.
4. **The environment block the owner was given.** Does it set the right variables to the right roots,
   does it leave the not-yet-moved trees on `C:`, and does the block actually run as pasted? Say
   whether the variables are set in THIS session's environment (`echo`), which tells you whether the
   owner has run it yet.
5. **The untouched boundary.** Prove the mover did not edit content it was told only to move:
   `git diff` the pre-move sha against HEAD for `tools/devmods/**` and `tools/prototypes/**` and show
   the result is empty of content changes.
6. **The handover message.** The train orchestrator asked for three things: the final paths of
   `tools/devmods/train_hub` and `tools/prototypes/train_hub`, the new root of `SMR-Assets`, and a
   ping that doccheck is green. Are all three in the mover's report, and are the paths the ones that
   exist on disk?
7. **What the move will break next time, not this time.** Name anything that resolves today only
   because a tree it points at has not moved yet.

## Your call

Where to look beyond the seven above; the inventory is a lead, not a fence. If the real risk is a
shape nobody here described, report that instead and say why it matters more. Rank findings by what
breaks first and for whom — the train hub's restart is what is waiting.

## Stops

A finding needs a change in a tree you may not write · the moved tree is missing something you cannot
prove was missing before the move (compare against the original, and against git) · doccheck REDs for
a reason you cannot attribute to the move.

## Do not claim

That the move is safe because doccheck is green: doccheck never reads the symlinks, the Mod Editor's
stored paths, or the game. That a path is unused because you did not find a caller — say where you
looked. That the train hub is unblocked: only the owner's verification import decides that, and it
runs in the Mod Editor, which you never open.
