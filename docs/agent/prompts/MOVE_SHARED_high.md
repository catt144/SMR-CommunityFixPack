# Create `SMR-Shared` and move the two shared trees into it

**One-off.** Fires after the opt-in pass (done, `411fdf0`) and ⚠️ **before the fix pack's move** —
that order is the point of this pass, see below. No audit grades this pass alone: one audit grades
the whole move at the end (`MOVE_AUDIT_high.md`). **Your report is the only witness of the moment of
this move** — write it to `docs/agent/reports/MOVE_SHARED_20260921.md`. Delete this file and its
`prompts/README.md` row in the commit that lands it.

Start: `git pull`; `git log -1 --format=%h -- docs/agent/prompts/MOVE_SHARED_high.md` is the
authoring sha. Put the work list in your todo tool before the first write, one item per
commit-and-verify unit, and keep it current — the owner reads it to decide when to step in.

**Root this session at `C:\Dev\SMR-BugFixPack`.** It is not moving in this pass, it holds the tools
you edit and this seat's memory store, and you are outside both trees you move.

## Decided by the owner — build it, do not reopen it

**`SMR-Shared` is one shared repo, pull-only, for long-term material both mods reference** (09-21).
**No per-repo folders and no rule scaffolding until something proves it needs them** — *"see if it
becomes a problem before we tie it up in rules and complications."* A gate comes later if it turns
out to need one. It is a repo because only a repo may sit at the `B:\Dev\SMR` root.

**Why it goes before the fix pack** (owner, 09-21): five files in the fix pack's `tools/` read the
archive by name, so moving it afterwards would break them and force the fix pack open a second time.
The fix pack is the game's loadable mod and its coordinator seat lives there — it goes down once,
with every tree it points at already at its final address.

```
C:\Dev\SMR-SrcArchive        ->  B:\Dev\SMR\SMR-Shared\SMR-SrcArchive         (93 MB)
C:\Dev\workshop_fpk_archive  ->  B:\Dev\SMR\SMR-Shared\workshop_fpk_archive   (11 MB)
```

Neither is a git repo today (no `.git` in either, 09-21); `SMR-Shared` is a new one. The archive
holds `1.0.7.396349`, `1.1.0.403908` and `README.md`. Sizes are `du -sh` on 09-21 — re-derive.

⛔ **No remote, and do not propose one.** Local-only is a settled class in this project, not an
oversight, and raising it is a repeat offence.

## End state

1. **Nothing is deleted this pass.** Copy, verify, then rename each original to
   `<name>__MOVED_20260921` in place. The owner deletes originals after the whole-move audit.
2. **`SMR-Shared` is a git repo with its content committed.** About 104 MB, overwhelmingly text.
   Commit it whole; add a `.gitignore` only if something concrete proves one is needed.
3. **Proof of an intact copy.** Counts and total bytes both sides, and ⭐ **re-verify the archive's
   own sha256 manifest at the new location** — that is a real integrity check rather than a count.
   Find it first: there is no `MANIFEST.sha256` at the archive's top level, so locate what actually
   covers each build tree, and where nothing does, hash both sides yourself and compare.
4. **Live consumers repointed — in the DONOR, not in both copies.** ⛔ Re-derive the list; two
   recorded lists disagree and neither is authoritative. The owner's register names `patchcheck`,
   `treediff`, `presetdiff` and `bodycheck`; a 09-21 grep of `tools/` returned `deskbench.py`,
   `patchcheck.py`, `treediff.py`, `l6_promise_map.py` and `TESTKIT.md`. Grep both repos and
   reconcile what you find against both.
   ⚠️ **`tools/` is shared, and the fix pack is the donor.** The fork keeps a ledger of which tools
   are adapted, not ported or local-only (`TOOLS_ADAPTED`, `TOOLS_NOT_PORTED`, `TOOLS_LOCAL_ONLY` in
   its `tools/sync_from_fixpack.py`). ⛔ **Do not hand-edit the fork's copy of a mirrored tool** — it
   reads as undeclared drift on the next sync and may overwrite a deliberate adaptation. Change the
   fix pack's copy, then say in your report that a sync pass is OWED. The fork's
   `prompts/perma/KNOWLEDGE_SYNC_PASS.md` carries it across on the owner's yes; it is the owner's to
   fire and not yours to run.
   **One fork file IS yours**, because it is the fork's own and mirrored from nothing:
   `tools/sync_from_fixpack.py:333`, whose `SRC_ARCHIVE` default is `C:\Dev\SMR-SrcArchive`. Repoint
   it in the same pass — it degrades loudly rather than silently (the script prints a SKIPPED line
   naming the missing donor path), but a knowledge route that skips is still a broken one.
5. **⚠️ The environment variable has two spellings in the tree.** `doccheck.py` reads
   `SMR_SRCARCHIVE`; `deskbench.py:12` documents `SMR_SRC_ARCHIVE`. Establish which each consumer
   actually reads before you rely on either, and remember pass one's finding: **none of the five
   `SMR_*` variables is set on this machine**, so the in-code default is what resolves and repointing
   defaults is the load-bearing change.
6. **Records stay records; the map does the translating.** The source-line citations — 127 files
   under `docs/agent/reports/`, plus the `Code/Fix_*.lua` comments — name the build they were read
   on, and that is what makes them re-findable. The drive letter is not. ⛔ Rewriting them is the
   defect. Instead add the archive's new root to `docs/README.md`'s **Path translation** block
   (line 131 on 09-21) and to the fork's equivalent, so a reader can translate an old citation.
   Repoint the "Outside the repo" map entries in both packs, which ARE live pointers.
   ⚠️ **Sweep the fork as well as this repo**: 49 references there named `C:\Dev\SMR-SrcArchive` on
   09-21. Split live from records the same way, and remember that editing the fork's `CLAUDE.md`
   drifts its `AGENTS.md` and REDs that tree, so edit and `--regen` in one commit.
7. **Prove the tools still work, not that the strings changed.** Run at least `treediff.py` and
   `patchcheck.py` against the archive at its new home and show their output.
8. **doccheck GREEN in both packs**, with selftests, and `TOOLS COMPILE` passing after your edits.

If budget runs out, drop in this order: the fork's prose, then the `Path translation` wording. Never
drop the manifest verification, the consumer repoint or the tool run in item 7.

## Your call

How you copy and how you prove it faithful, as long as the proof is a command's output. Whether the
two trees keep their own folder names inside `SMR-Shared` or you flatten them — say which and why,
remembering the owner's "no scaffolding until something proves it needs it". Whether the repo lands
in one commit or two. Whether a consumer gets an environment variable or a plain absolute default.

## Scope

In: the two trees, the new repo, every live consumer and map entry in both packs, your report.
Out: the fix pack's own move, the TestKit, `SMR-ScreenCaptures`, FR-1, the community repos, the Mod
Editor, the game, and the opt-in pack's own mod content.

## Stops — report instead of pushing on

A consumer cannot be repointed without entering another seat's boundary · a manifest or hash does not
verify and you cannot show why · doccheck REDs in either pack for a reason that is not a path you
introduced.

## Do not claim

That no reference to the old paths remains — count both sides and give what is left, by class,
separating records from live pointers. That the archive is intact because the file counts match: say
which hash covered which tree. That `SMR-Shared` needs a gate, a remote, a README policy or per-repo
structure — the owner ruled simplest-thing-first and a later problem is what earns any of those.
