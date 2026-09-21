# Move the fix pack, the TestKit and the captures to `B:\Dev\SMR`

**One-off, second pass of the tree move.** You are the doc orchestrator of this pass. There is no
audit of your pass alone: ONE audit grades the whole move at the end (`MOVE_AUDIT_high.md`, owner
2026-09-21), long after the trees you touch have been worked in. **Your report is the only witness of
the moment of this move** — write it to `docs/agent/reports/MOVE_FIXPACK_20260921.md`. Delete this
file and its `prompts/README.md` row in the commit that lands it.

Start: `git pull`; `git log -1 --format=%h -- docs/agent/prompts/MOVE_FIXPACK_high.md` is the
authoring sha, and `git diff --stat <sha>..HEAD -- tools/ docs/README.md` empty means the facts below
still hold. Put the work list in your todo tool before the first write, one item per
commit-and-verify unit, and keep it current — the owner reads it to decide when to step in.

## Where you run from, and what it does and does not fix

**Root this session at `B:\Dev\SMR\SMR-OptInPack`** (owner, 2026-09-21) and fire this file by its
absolute path in the fix pack. That tree moved in pass one and is standardised on this repo, so the
same rules and skills load, and you sit outside every tree you move — which is what makes the final
rename yours to run instead of the owner's. Do not copy this prompt into that repo: its own prompt
map would reject an unmapped file. Write nothing into it beyond what a session unavoidably writes.

**The one cost: you will not have the fix pack's memory store** (77 memories keyed to
`C:\Dev\SMR-BugFixPack`; the fork's store holds 8, about train hub work). Everything from it that
bears on this job is in "Measured on this machine" below. Do not go hunting for the rest.

**If you are instead rooted in the fix pack itself**, two things change and both are traps. Windows
will not rename a directory that is a live process's working directory, so the fix pack's own rename
becomes a fenced block for the owner to run after your session ends. And this prompt deletes itself
per its lifecycle while living in the tree you are moving, so a later re-read of its path fails.

Either way:

- **The moment a copy verifies, the tree at `B:` is the live one.** Every later edit, commit and push
  happens THERE. Do not edit, pull or commit in `C:\Dev\SMR-BugFixPack` again, including this
  prompt's own deletion and your report. Say in your report which commits landed in which tree.
- **Other sessions are rooted in this tree too**, and both trees share one remote, so work can land
  in the copy that is about to be abandoned and two trees can race to push `main`. Run `ListAgents`
  and `git log --oneline origin/main..` in both trees at the switch; if a peer is live in the old
  tree, that is a stop — the owner closes it. Re-check immediately before the rename.
- **`core.hooksPath` is absolute on this machine**: `git config --local core.hooksPath` reads
  `c:\Dev\SMR-BugFixPack\tools\hooks` (09-21), and `.git/config` travels with a filesystem copy. So
  the new tree would run the OLD tree's hooks, and run none at all once the original is renamed —
  silently, with doccheck no longer gating a commit. Set it to the relative `tools/hooks` that
  `CLAUDE.md` documents, in BOTH new repos, and prove a hook fires from the new root.
## Measured on this machine — these are the memory-store facts that bear on this job

Each is silent when it bites, which is why they are here rather than left to be re-derived.

- ⛔ **Never `git checkout --` or `git restore` as a restore.** It restores to HEAD and has silently
  destroyed an uncommitted rewrite in this tree. The TestKit's dirty file is exactly that exposure:
  restore from a copy and sha256 it instead.
- **Commit with `git commit -F <msg> -- <paths>`.** The index is shared with any other session; on
  09-21 another session had 22 unrelated files modified here mid-job, and a bare `git commit -a`
  would have swept them into an unrelated commit.
- **A heredoc to Python or the shell eats backslashes**, so a Windows path written that way is
  silently wrong. Write scripts with the editor tool and re-read the path you wrote.
- **The tree is LF and a mixed file turns doccheck RED.** Python text mode writes CRLF on Windows —
  pass `newline="\n"`; `tools/doccheck.py --fix-eol` repairs it.
- **PowerShell 5.1 mangles commit-message quoting and writes UTF-8 with a BOM**, and
  `Compress-Archive` writes backslash paths. Prefer the Bash tool for git and for archives.
- **An empty `rg` is not proof of absence here**: a root `.rgignore` hides `docs/archive/`. Confirm
  with `grep -r` or `rg --no-ignore` before claiming a path no longer appears anywhere.

## Before you copy anything

**The owner closes every session in the moving tree and has its work committed before a move fires**
— that is how pass one was run, and they do the same here. So this is a verification, not a warning:
confirm it, and if it does not hold, stop rather than repairing it yourself. `git status` clean in
all three trees, except the TestKit's one known dirty file. `git log --oneline origin/main..` empty
in the fix pack, because an unpushed commit in a tree about to be abandoned is the thing that gets
lost. Pass one landed at `411fdf0` and repointed this tree's opt-in pointers already; its report is
`docs/agent/reports/MOVE_OPTIN_20260921.md` and you read it before starting.

## Decided by the owner, 2026-09-21 — build it, do not reopen it

All SMR content moves to `B:\Dev\SMR`; only a REPO sits at that root. **One exception is cleared:
`SMR-ScreenCaptures`**, the owner's capture drop folder, because it is a shared tool's folder that
the TestKit writes to. This pass moves exactly three trees:

```
C:\Dev\SMR-BugFixPack          ->  B:\Dev\SMR\SMR-BugFixPack
C:\Dev\SMR-BugFixPack-TestKit  ->  B:\Dev\SMR\SMR-BugFixPack-TestKit
C:\Dev\SMR-ScreenCaptures      ->  B:\Dev\SMR\SMR-ScreenCaptures
```

**Why these three together, not one at a time:** `doccheck.py:61`, `aliascheck.py:62` and
`deskbench.py:72` each default to the TestKit at a hard-coded `C:\Dev` sibling, and the TestKit's
capture path is hard-coded at `Code/74_SMRTK_Agent.lua:109`. Splitting them leaves a repointed tree
pointing at one that has not moved.

⚠️ **Passes before yours have already moved things you point at.** The opt-in pack and `SMR-Assets`
went first; `MOVE_SHARED_high.md` then put the archived game source and the Workshop corpus into
`B:\Dev\SMR\SMR-Shared`, precisely so your repoint happens once. Read each earlier report
(`docs/agent/reports/MOVE_*`) and derive every tree's CURRENT address from disk rather than from this
list. Still on `C:` and none of your business: the FR-1 folders, `SMR-CommunityMods`,
`SMR-CommunitySaveRescue`. `SMR-OptInPack` and `SMR-Assets`
moved in pass one — read its report (`docs/agent/reports/MOVE_OPTIN_20260921.md`) before you start,
and do not redo what it already did to this tree's pointers.

## ⛔ Four junctions inside the fix pack — the one way to do real damage here

They are **junctions**, not symlinks, and `ls -l` in Git Bash misreports them as symlinks. Classify
with PowerShell `LinkType`, and enumerate with `cmd /c dir /A:L /S /B <tree>`, which does not follow
them. Measured 2026-09-21 — re-derive, and treat any junction not in this list as a finding:

| junction | target | what a following copy pulls in |
|---|---|---|
| `saves/game` | the owner's live save folder | 1.8 GB |
| `saves/backup` | the owner's save backup folder | 668 MB |
| `zz-owner/all-claude-memory` | `C:\Users\stkot\.claude\projects` | **every Claude project on this machine** |
| `zz-owner/claude-memory` | this project's `memory\` | 229 KB |

**`robocopy` follows junctions by default.** An unguarded copy turns a 195 MB tree into many
gigabytes, replaces the owner's live saves with stale duplicates that silently diverge from the real
ones — and agents do not touch the owner's saves (owner, 2026-09-18) — and rakes every unrelated
Claude project on the machine into a git repo. Exclude them from the bulk copy (`/XJ`) and recreate
each one deliberately, or prove your copy tool preserved them as junctions.

**Proof required:** after the copy, the `dir /A:L /S /B` sweep of the new tree lists the same four,
each `LinkType` is `Junction` with the same target, and the new tree measures about 195 MB.

`saves/*` and `all-claude-memory` keep their targets, which do not move. ⚠️ **`zz-owner/claude-memory`
must be repointed** to the store's new location from item 6, or the moved tree quietly reads the old
one. The TestKit and `SMR-ScreenCaptures` hold no reparse points at all (same sweep, 09-21).

## The boundary — another seat's work is in these trees

- **TestKit `Code/80_AgentSlots.lua` is dirty with the TRAIN seat's live sitting** (rewritten
  2026-09-20, 172 insertions / 683 deletions; it now reads "train hub centre/transition prototype").
  Carry it across uncommitted, hash it, and leave it. ⛔ Never commit it, never `git restore` it
  (the 2026-08-03 orphan lesson; doccheck says so every run).
- **The TestKit has no remote.** `git -C <testkit> remote -v` is empty, so a botched copy has nothing
  to restore from. It gets the strictest copy proof of the three.
- **In `%APPDATA%\Surviving Mars Relaunched\Mods\` exactly two of the six entries are yours**:
  `SMR-BugFixPack` and `SMR-BugFixPack-TestKit`. `SMR-OptInPack`, `SMR-TrainHubDev` and
  `SMR-TrainHubPrototype` are the train seat's; `SMR_FR1TempWorkaround` is a real folder and FR-1's.
- **`.claude/` is the coordinator seat's.** Repoint literal path strings there and nothing else; its
  prose and its rulings are not yours to rewrite. Four files hold `C:\Dev` (`HANDOFF_PROMPT.md` 4
  hits, `IMPLEMENT_PROMPT.md` 5, `FRESH_SESSION_PROMPT.md` 3, `CHECKLIST_MARKERS_REVIEW.md` 2), plus
  one under `.claude/briefs/` and four permission entries in `.claude/settings.json`. List what you
  changed, line by line, for that seat to check.

## End state

1. **Nothing is deleted this pass.** Copy, verify, then rename each original to
   `<name>__MOVED_20260921` in place. The owner deletes originals after the whole-move audit.
2. **Git-ignored material is load-bearing here and a `git clone` loses all of it.** On disk today:
   `local/` 56 MB (866 files, its README a tracked gate), `.claude/` 3.4 MB, `zz-owner/` 156 KB,
   `scratch/` 16 KB. Use a filesystem copy, or a clone plus every ignored path, and prove which.
3. **Proof of an intact copy, per tree**: file count and total bytes before and after, `git fsck`
   clean, HEAD sha identical and written into your report (fix pack `26b86e7` main, TestKit `3abab0a`
   master, both measured 09-21 — re-derive, do not trust these), remotes unchanged, and the dirty set
   listed with a sha256 per file. The audit cannot re-observe any of it. `SMR-ScreenCaptures` is not
   a repo (1.1 GB): it gets counts and a hash sample instead.
4. **The hard-coded roots repointed, in the NEW trees.** `doccheck.py:61`, `aliascheck.py:62`,
   `deskbench.py:72` (TestKit default), `doccheck.py:759` (`SMR_MEMORY`, whose default points at the
   Claude memory store that moves in item 6), `tools/store_screenshots.py:18`, TestKit
   `Code/74_SMRTK_Agent.lua:109`, the three command lines in `tools/SMRTK.md`, and `docs/README.md`'s
   "Outside the repo" block (every entry, at whatever address it actually has by then: the shared
   trees are in `SMR-Shared`, the FR-1 folders are still on `C:`). ⚠️ **The in-code defaults are the
   load-bearing part: pass one found that NONE of the five `SMR_*` variables is actually set on this
   machine**, so every script has been resolving through its default and the owner's `setx` block is
   a belt, not the braces. A sibling-relative default is the one that never breaks on the next move.
5. **Records stay records, and an absolute-path count is not a work list.** 106 tracked files carry a
   `C:\Dev` path and 104 of them are under `docs/agent/reports/` — source-line citations in
   `still-needed/*.json`, past commands, evidence of where something was read. ⛔ Rewriting those is
   the defect, not the fix. Pass one is the warning: of its 183 references only 63 named a tree that
   was moving, so obeying its inventory's "134 prose references" literally would have pointed 120
   correct ones at nothing. Filter to references that name a tree in YOUR three, then split live
   pointers from records, and give the count you changed against the count you left.
6. **The Claude memory store follows the tree, or this seat starts empty — and this is one of your
   LAST steps**, because your own session writes into it while you work and an early copy loses
   whatever you write afterwards. The store is keyed by
   root path: `%USERPROFILE%\.claude\projects\c--Dev-SMR-BugFixPack` (77 memory files, 229 KB;
   663 MB with session transcripts) becomes **`b--Dev-SMR-SMR-BugFixPack`** — the doubled `SMR` is
   correct, because the rule reproduces the whole destination path and the destination is
   `B:\Dev\SMR\SMR-BugFixPack`. Pass one applied that rule and its output is the witness; still
   confirm it on the first session at the new root and say so. **Copy, never move**, and do not edit
   a memory file: several name `C:\Dev` and are records.
7. **The two mod junctions recreated and proven.** `%APPDATA%\Surviving Mars Relaunched\Mods\`
   held six entries on 09-21: `SMR-BugFixPack` and `SMR-BugFixPack-TestKit` are **yours**, both
   junctions to `C:\Dev`; `SMR-OptInPack` and `SMR-TrainHubPrototype` are junctions and
   `SMR-TrainHubDev` a true symbolic link, all three the train seat's; `SMR_FR1TempWorkaround` is a
   real folder and FR-1's. If yours are wrong the fix pack silently ceases to exist for the game.
   `mklink /J` needs no elevation, so recreate them yourself and prove each by reading a file THROUGH
   the junction. ⚠️ Delete the stale one first: a junction whose target is renamed keeps pointing at
   the dead path rather than failing. Report the state of the other four; do not touch them.
8. **doccheck GREEN, run from the new fix pack root**, with its selftests, PACK IGNORE PARITY, the
   LOCAL gate and the TestKit parse pass, plus the new `PARENT FILES` reading now that the parent is
   `B:\Dev\SMR`.
9. **One fenced copy-paste block for the owner**: the `setx` environment block (`SMR_TESTKIT` and
   `SMR_FIXPACK` to the new roots, `SMR_SRCARCHIVE` still on `C:`, `SMR_TRAINASSETS` as pass one left
   it), plus any rename or symlink step you could not run yourself. Say which lines you already ran.

If budget runs out, drop in this order: the `.claude/` strings, then prose in reports, then the
`docs/README.md` polish. Never drop the copy verification, the saves proof, the memory store, the
symlinks or the owner's block.

## Your call

How you copy and how you prove it faithful, as long as the proof is a command's output. Whether the
three trees are one commit-and-verify unit or three. Whether the TestKit default becomes an
environment variable or a sibling-relative path. Whether the memory store's session transcripts come
across with it or only `memory/`, given the 663 MB — decide and say why.

## Scope

In: the three trees, their paths, their gates, the two mod symlinks, the memory store, the owner's
block, your report.
Out: every tree still on `C:`, `SMR-Shared`, FR-1, the Mod Editor, the game, the opt-in pack, and the
train seat's files listed above.

## Stops — report instead of pushing on

A copy's count, bytes, HEAD or symlink shape does not match and you cannot show why · another session
is live in the old tree at the switch, or an unpushed commit exists in a tree you are about to
abandon · doccheck REDs at the new root for a reason that is not a path you introduced.

Measured 09-21 and NOT dangers, so do not spend the budget re-deriving them: `B:` is a fixed internal
NTFS volume (`Win32_LogicalDisk` DriveType 3, no `subst`), so the mod's symlink target survives a
reboot; and the longest path in the tree is 118 characters against a 260 limit, with the new root
only 8 characters longer.

## Do not claim

That the move is complete: the whole-move audit grades it. That no reference to the old path remains
— count both sides and give what is left, by class, separating records from live pointers. That the
mod loads: nothing here launches the game, and a resolving symlink is not a loaded mod.
