# Move everything but the fix pack to `B:\Dev\SMR`

**One-off.** Fires after the opt-in pass (done, `411fdf0`) and ⚠️ **before the fix pack's move**. No
audit grades this pass alone: one audit grades the whole move at the end (`MOVE_AUDIT_high.md`).
**Your report is the only witness of the moment of this move** — write it to
`docs/agent/reports/MOVE_REST_20260921.md`. Delete this file and its `prompts/README.md` row in the
commit that lands it.

Start: `git pull`; `git log -1 --format=%h -- docs/agent/prompts/MOVE_REST_high.md` is the authoring
sha. Put the work list in your todo tool before the first write, one item per commit-and-verify unit,
and keep it current — the owner reads it to decide when to step in.

**Root this session at `C:\Dev\SMR-BugFixPack`.** It is not moving in this pass, it holds the tools
you edit and this seat's memory store, and you are outside every tree you move.

## Decided by the owner — build it, do not reopen it

**All SMR content moves to `B:\Dev\SMR`; only a REPO sits at that root.** (The one cleared exception,
`SMR-ScreenCaptures`, belongs to the last pass.)

**Everything that is left moves in ONE pass** (09-21): these trees are small beside the fix pack, and
every separate pass would edit the fix pack's map and tools again. One pass means **the fix pack is
touched once before its own move** — it is the game's loadable mod and its coordinator seat lives in
it, so it goes down once, with every tree it points at already at its final address.

**`SMR-Shared` is one shared repo, pull-only, for long-term material both mods reference.** No
per-repo folders and no rule scaffolding until something proves it needs them — *"see if it becomes
a problem before we tie it up in rules and complications."*

**FR-1's workaround mod becomes its own repo, local-only with no remote**: its source copy, its desk
tools and the dev package. It is a mod, so it sits at the root like any other.

```
NEW REPO   B:\Dev\SMR\SMR-Shared
             C:\Dev\SMR-SrcArchive         (93 MB, plain: 1.0.7.396349, 1.1.0.403908, README.md)
             C:\Dev\workshop_fpk_archive   (11 MB, plain)
NEW REPO   B:\Dev\SMR\SMR-FR1   (local-only, NO remote)
             C:\Dev\SMR-FR1-TempMod-2026-09-11         (317 KB, plain)
             C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11   (17 MB, plain)
             C:\Dev\SMR-FR1-DevPackage                 (223 KB, plain)
             C:\Dev\SMR-FR1-DevPackage.zip             (47 KB, the loose file doccheck reports)
MOVE       C:\Dev\SMR-CommunityMods       -> B:\Dev\SMR\SMR-CommunityMods        (185 MB, repo, GitHub remote)
           C:\Dev\SMR-CommunitySaveRescue -> B:\Dev\SMR\SMR-CommunitySaveRescue  (340 KB, repo, GitHub remote)
```

Sizes, plain-vs-repo and remotes are `du -sh` and `git remote -v` on 09-21 — re-derive at the head of
your work and say if they moved. **Out of this pass:** the fix pack, the TestKit and
`SMR-ScreenCaptures`, which move last together.

⛔ **No remote for the two new repos, and do not propose one.** Local-only is a settled class in this
project, not an oversight, and raising it is a repeat offence.

## End state

1. **Nothing is deleted this pass.** Copy, verify, then rename each original to
   `<name>__MOVED_20260921` in place. The owner deletes originals after the whole-move audit.
2. **The two new repos exist with their content committed** (about 104 MB and 18 MB, overwhelmingly
   text). No `.gitignore`, README policy or per-repo structure unless something concrete proves one
   is needed.
3. **The two existing repos move as repos**: `git fsck` clean, HEAD sha and branch identical and
   written into your report, remotes unchanged, every tag still resolving. ⭐ **Both have GitHub
   remotes, and that is what will make their originals safe to delete** — the trees in items 1-2 do
   not, so their `__MOVED_` copy is their only redundancy. Say which is which in your report; the
   owner decides deletions, and do not propose a remote or a backup for the ones without.
4. **Proof of an intact copy, per tree**: counts and total bytes both sides. For `SMR-SrcArchive`,
   ⭐ **re-verify its own sha256 manifest at the new location** — a real integrity check rather than
   a count. Find it first: there is no `MANIFEST.sha256` at its top level, so locate what actually
   covers each build tree, and where nothing does, hash both sides yourself.
5. **Live consumers repointed once, in the fix pack AND the fork.** ⛔ Re-derive the list; two
   recorded lists disagree and neither is authoritative. The owner's register names `patchcheck`,
   `treediff`, `presetdiff` and `bodycheck`; a 09-21 grep of `tools/` returned `deskbench.py`,
   `patchcheck.py`, `treediff.py`, `l6_promise_map.py` and `TESTKIT.md`. The fork held 49 references
   naming `C:\Dev\SMR-SrcArchive` on 09-21. Grep both repos and reconcile against both lists.
   ⚠️ **`tools/` is shared and the fix pack is the donor.** The fork keeps a ledger of which tools are
   adapted, not ported or local-only (`TOOLS_ADAPTED`, `TOOLS_NOT_PORTED`, `TOOLS_LOCAL_ONLY` in its
   `tools/sync_from_fixpack.py`). ⛔ **Do not hand-edit the fork's copy of a mirrored tool** — it reads
   as undeclared drift and may overwrite a deliberate adaptation. Change the fix pack's copy, then
   report that a sync pass is OWED; the fork's `prompts/perma/KNOWLEDGE_SYNC_PASS.md` carries it on
   the owner's yes and is theirs to fire. **One fork file IS yours**, being the fork's own and
   mirrored from nothing: `tools/sync_from_fixpack.py:333`, whose `SRC_ARCHIVE` default is
   `C:\Dev\SMR-SrcArchive`. It degrades loudly — the script prints a SKIPPED line — but a knowledge
   route that skips is still broken. ⚠️ Editing the fork's `CLAUDE.md` drifts its `AGENTS.md` and REDs
   that tree: edit and `--regen` in one commit, exactly as here.
6. **⚠️ The environment variable has two spellings in the tree.** `doccheck.py` reads
   `SMR_SRCARCHIVE`; `deskbench.py:12` documents `SMR_SRC_ARCHIVE`. Establish which each consumer
   actually reads before relying on either, and remember pass one's finding: **none of the five
   `SMR_*` variables is set on this machine**, so the in-code default is what resolves and repointing
   defaults is the load-bearing change.
7. **Records stay records; the map does the translating.** The source-line citations — 127 files
   under `docs/agent/reports/`, plus the `Code/Fix_*.lua` comments — name the build they were read
   on, and that is what makes them re-findable. The drive letter is not. ⛔ Rewriting them is the
   defect. Add the new roots to `docs/README.md`'s **Path translation** block (line 131 on 09-21) and
   the fork's equivalent, and repoint the "Outside the repo" map entries in both packs, which ARE
   live pointers.
8. **`LINUX_DISPATCH.md`'s binding needs this migration's edit.** It reads *"the mod lives outside
   git; it never goes into `Code/` or the fix pack"* — the spirit holds and FR-1 still never enters
   the fix pack, but "outside git" stops being true the moment FR-1 is a repo. It is a perma prompt:
   use the `doc-editing` skill and preserve the obligation while fixing the wording.
9. **Prove the tools still work, not that the strings changed.** Run at least `treediff.py` and
   `patchcheck.py` against the archive at its new home and show their output.
10. **doccheck GREEN in both packs**, with selftests and `TOOLS COMPILE` passing. Its `PARENT FILES`
   gate reported one loose file in `C:\Dev` (`SMR-FR1-DevPackage.zip`); once that is inside
   `SMR-FR1`, say what the gate reports.
11. **One fenced copy-paste block for the owner** with any `setx` variable this pass changed, saying
   which lines you already ran.

If budget runs out, drop in this order: the fork's prose, then the `Path translation` wording, then
item 8. Never drop the manifest verification, the consumer repoint, the tool run or item 3's
remote-vs-no-remote accounting.

## Your call

How you copy and how you prove it faithful, as long as the proof is a command's output. Whether the
moved folders keep their own names inside `SMR-Shared` and `SMR-FR1` or you flatten them — say which
and why, remembering "no scaffolding until something proves it needs it". Whether each repo is its
own commit-and-verify unit or the pass is one. Whether a consumer gets an environment variable or a
plain absolute default.

## Report, do not act

`%APPDATA%\Surviving Mars Relaunched\Mods\SMR_FR1TempWorkaround` is a real folder, not a junction —
the only mod installed by copy rather than by link. Whether it should become a junction into the new
`SMR-FR1` repo is the owner's call, and FR-1 is winding down. Describe what you found and leave it.

## Scope

In: the six trees, the two new repos, every live consumer and map entry in both packs, the
`LINUX_DISPATCH.md` wording, your report.
Out: the fix pack's own move, the TestKit, `SMR-ScreenCaptures`, the Mod Editor, the game, the
`%APPDATA%` mod entries, and the opt-in pack's own mod content.

## Stops — report instead of pushing on

A consumer cannot be repointed without entering another seat's boundary · a manifest, hash or HEAD
does not verify and you cannot show why · doccheck REDs in either pack for a reason that is not a
path you introduced.

## Do not claim

That no reference to the old paths remains — count both sides and give what is left, by class,
separating records from live pointers. That a tree is intact because its file count matches: say
which hash covered which tree. That `SMR-Shared` or `SMR-FR1` needs a gate, a remote, a README policy
or per-repo structure — the owner ruled simplest-thing-first, and a later problem is what earns any
of those.
