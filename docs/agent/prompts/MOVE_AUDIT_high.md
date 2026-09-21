# Audit the whole move to `B:\Dev\SMR`

**One-off, adversarial, and NOT fired per pass.** Owner, 2026-09-21: the opt-in pack moves, the rest
of the move follows, and then ONE audit grades the whole thing. Fire in a fresh session after the
last move pass reports done. You did none of that work and you do not fix it: you grade it, and a
FAIL is a useful result. ⛔ Do not run a mover's commands again as your method — re-running a copy
proves a copy; you are looking for what was missed. Delete this file and its `prompts/README.md` row
in the commit that lands your report.

Root the session wherever the fix pack lives by then. The trees under audit are every tree a move
report names: the reports are `docs/agent/reports/MOVE_*` in the fix pack, and each pass's brief was
deleted when it fired, so read it from history
(`git log --diff-filter=D --name-only -- docs/agent/prompts/`). The first pass moved
`SMR-OptInPack` and `SMR-Assets`; its originals are `C:\Dev\SMR-OptInPack__MOVED_20260921` and
`C:\Dev\SMR-Assets__MOVED_20260921`, kept until you pass them.

**Write nothing outside your report** (`docs/agent/reports/MOVE_AUDIT_<date>.md` in the fix pack) and
run no writing git command anywhere except the commit that lands it. A defect goes in the report with
the command that shows it — you do not repair it, and you do not touch a moved tree at all.

## The moved trees are LIVE by the time you run

The first pass released the train hub build, so `SMR-OptInPack` and `SMR-Assets` have been worked in
since they landed: new commits, new files, a different dirty set, possibly a session writing while
you read. **A difference between a moved tree and its original is a finding only when the tree's own
history since the move does not explain it.** Each move report records the pre-move HEAD sha and the
dirty set with a sha256 per file, because you cannot re-observe them; anchor on those, attribute
every later change by commit and diff, and never grade the train seat's work as the mover's.

## What the move was supposed to achieve

The owner, 2026-09-21: all SMR content moves to `B:\Dev\SMR`; only a repo sits at that root;
everything else lives in the repo that owns it or in a shared repo. The opt-in pack and its assets
went first because the train hub build was on hold until they landed. The first pass's path inventory
is `docs/agent/support/MOVE_PATH_INVENTORY_20260921.md` in the opt-in pack (`baaefd1`): **5
editor-held, 29 in scripts, 13 in config, 134 in prose** on that date.

**Another seat owns part of the work**, and its items failing is NOT a defect of the move: the mod
symlinks in `%APPDATA%\Surviving Mars Relaunched\Mods\`, the editor-held paths under `SourceData/`,
the dev mod's test scripts, and the verification import. A mover was required to LIST those, not fix
them. Judge whether the list was complete and correct, not whether the items are done. Likewise the
Blender proof JSONs' `command` fields and the `_before_claude_pass2_20260918/` snapshot are evidence
of past runs: rewriting them would be the defect.

## What to establish, per moved tree, each with the command that shows it

1. **Nothing was lost.** The pre-move HEAD is an ancestor of today's; `git fsck`; every remote; every
   tag (the opt-in pack: `hub-model-final-untextured`, `hub-centre-lights-20260921`). Every file in
   the `__MOVED_` original is in the moved tree byte-identical, or changed or removed by a commit you
   can name. The recorded dirty set arrived: each file matches its recorded sha256, or a later commit
   carries it. A tree that was not a repo gets counts and hashes against its original instead.
2. **Every tree works where it now lives.** doccheck GREEN from each new root that has one, with its
   selftests, PACK IGNORE PARITY and the LOCAL gate. The pack predictor still excludes `local/` and
   `scratch/`. A GREEN that carries a `not found` or `not checked` leg did not run that leg: the
   fork's doccheck stayed GREEN on 09-21 while its TestKit legs read `TestKit not found`, because
   its `doccheck.py:66` default waits on the owed sync pass. Name each such leg and whose it is.
3. **The path sweep, counted both ways.** Grep every moved tree for every OLD root and report what is
   left BY CLASS, naming who owns each survivor. ⛔ **Exclude junctions from every count** (`grep
   --exclude-dir`): `zz-owner/all-claude-memory` walks into every Claude project on the machine, and
   following it turned one pass's 2,649 real hits into a reported 31,255. A survivor inside the other seat's boundary is
   expected; a survivor in prose, a `docs/` map, `.claude/settings.json` or a script a mover owned is
   a finding, and so is a record that was rewritten when it should have been left as a record. Tools
   outside git count: the TestKit hard-codes its capture folder in `Code/74_SMRTK_Agent.lua` with a
   silent fallback to `AppData/`.
4. **The in-code defaults are the configuration** — the owner ruled on 09-21 that no `SMR_*` variable
   is set, so a default that points at a dead path breaks silently with nothing to override it.
   Confirm no `SMR_*` variable is set in THIS session (`echo`), then resolve every default in both
   repos' `tools/` and show each points at a path that exists. `SMR_SRCARCHIVE` is the ONE name for
   the archive ROOT in both repos (unified 09-21); a tool still reading `SMR_SRC_ARCHIVE` is a finding.
5. **The untouched boundary.** Over each MOVER's commits only, `git diff` for `tools/devmods/**` and
   `tools/prototypes/**` is empty of content changes. The train seat's own later commits there are
   theirs and expected.
6. **The handover message.** The train orchestrator asked for three things: the final paths of
   `tools/devmods/train_hub` and `tools/prototypes/train_hub`, the new root of `SMR-Assets`, and a
   ping that doccheck is green. Were all three in the first pass's report, and were the paths right?
7. **Nothing resolves by accident.** Anything that still works only because an old root, a `__MOVED_`
   original or a stale variable is still on disk. The owner deletes the originals on your pass, so
   say plainly, per original, whether it is safe to delete. ⚠️ **A faithful copy is not the same as
   safe to delete.** Check each moved tree for a remote, and where there is none, say that deleting
   the original takes redundancy to zero and name what would be lost. `SMR-Assets` (504 MB, five
   tags) and the TestKit both have no remote. That is deliberate and owned elsewhere — report the
   consequence for the delete decision and do not propose a remote, a backup or a policy. The
   originals include each moved tree's OLD Claude memory store key (for the fix pack,
   `~\.claude\projects\c--Dev-SMR-BugFixPack`, 699 MB with transcripts), kept for you and owed a
   verdict like any `__MOVED_` folder. **A held original is a finding too:** `C:\Dev\SMR-BugFixPack`
   would not rename because nine orphaned `tail -f | grep` log watchers from dead agent sessions
   (the oldest from 08-11) had their working directory inside it. In Git Bash,
   `readlink /proc/*/cwd` lists every MSYS process's working directory, which a command-line search
   cannot see. Anything still running inside an original blocks its deletion.
8. **The root rule.** `B:\Dev\SMR` holds repos and nothing else, with ONE exception the owner cleared
   on 2026-09-21: `B:\Dev\SMR\SMR-ScreenCaptures`, their capture drop folder, shared because the
   TestKit writes to it. Check that the TestKit and `tools/store_screenshots.py` both write THERE —
   a capture landing in `AppData/` is the kit's silent fallback, and it is the finding.
9. **Every junction, counted both ways** — the check nothing else makes, because Git Bash `ls -l`
   misreports a junction as a symlink and a dangling junction fails silently rather than loudly.
   Sweep each moved tree with `cmd /c dir /A:L /S /B` (it does not follow them) and classify each hit
   with PowerShell `LinkType`. The fix pack held four on 09-21 — `saves/game`, `saves/backup`,
   `zz-owner/all-claude-memory`, `zz-owner/claude-memory` — and the TestKit and `SMR-ScreenCaptures`
   held none. A real folder where a junction belongs is a finding: for `saves/*` it is a stale copy
   of the owner's live saves, and the tree's size gives it away. `zz-owner/claude-memory` must point
   at the store's NEW location, not the old one. Then every entry in
   `%APPDATA%\Surviving Mars Relaunched\Mods\` (six on 09-21 after the three train links were
   recreated: five junctions and one real folder, `SMR_FR1TempWorkaround`, which the owner ruled on
   09-21 stays a real folder — not a finding): resolve each target and read a file THROUGH it,
   **choosing a file whose bytes differ between the moved tree and its original**. A read of an
   identical file proves nothing: until pass two recreated it, the fix pack's mod junction still
   pointed at the unrenamed `C:` tree, and the game loaded the stale copy with no error. Any file
   changed by a post-move commit will do. A mod whose junction dangles does
   not exist for the game, and only the owner launching it proves the mod actually loads.
10. **What a filesystem copy loses quietly.** The git-ignored material a clone would have dropped is
   present: `local/` with its tracked README gate, `.claude/`, `zz-owner/`. Each moved tree's Claude
   memory store exists under the new root's derived name and holds its memories. `core.hooksPath` is
   relative, or absolute to the tree it sits in — never to a `__MOVED_` original, which would mean
   the hooks silently stopped gating commits. ⭐ **The route between the two packs still resolves:**
   the fork's `tools/sync_from_fixpack.py` reads `SMR_FIXPACK`, `SMR_SRCARCHIVE`, `SMR_TESTKIT` and
   `SMR_TRAINASSETS`, each with an in-code default and none of those variables set on this machine.
   Run it and read its output — a donor it cannot find makes it SKIP, so the two packs quietly stop
   exchanging tools and facts while every other gate stays green. Check too that no mover hand-edited
   the fork's copy of a mirrored tool instead of the donor's: that is drift the ledger did not
   declare, and it surfaces as an undeclared difference in the same run.

## Your call

Where to look beyond the ten above; the inventory is a lead, not a fence. If the real risk is a
shape nobody here described, report that instead and say why it matters more. Rank findings by what
breaks first and for whom.

## Stops

A finding needs a change in a tree you may not write · a moved tree is missing something that neither
its original nor its history explains · doccheck REDs for a reason you cannot attribute to the move.

## Do not claim

That the move is safe because doccheck is green: doccheck never reads the symlinks, the Mod Editor's
stored paths, or the game. That a path is unused because you did not find a caller — say where you
looked. That a live tree is intact because it matches its original: it should not match by now; say
which differences you attributed and to what. That the train hub works: only the owner's verification
import decides that, and it runs in the Mod Editor, which you never open.
