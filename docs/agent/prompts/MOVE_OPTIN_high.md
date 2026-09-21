# Move the opt-in pack and its assets to `B:\Dev\SMR`

**One-off, first pass of the tree move.** You are the doc orchestrator of the move. Fire from a fresh
session rooted at `C:\Dev\SMR-BugFixPack` (this prompt lives in the fix pack on purpose: the tree you
are moving would otherwise shift under you mid-job). You do not grade yourself: ONE audit grades the
whole move after its last pass (`MOVE_AUDIT_high.md`; owner, 2026-09-21), by which time the train
seat has been working in these trees for a while. **So your report is the only witness of the moment
of the move** — write it to `docs/agent/reports/MOVE_OPTIN_20260921.md`. Delete this file and its
`prompts/README.md` row in the commit that lands the result.

Start: `git pull` in both repos; `git log -1 --format=%h -- docs/agent/prompts/MOVE_OPTIN_high.md` is
the authoring sha. Put the work list in your todo tool before the first write, one item per
commit-and-verify unit, and keep it current — the owner reads it to decide when to step in.

## Decided by the owner, 2026-09-21 — build it, do not reopen it

**All SMR content moves to `B:\Dev\SMR`. Only a REPO may sit at that root**; everything else lives in
the repo that owns it or in a shared repo. **The opt-in pack and its related materials move FIRST**,
on their own, ahead of every other tree.

**Why this tree first: the train hub build is ON HOLD until it lands.** The queued entity imports are
deliberately waiting so they are born with the new paths. Your handover message (end state 7) is what
releases that work, so it is the deliverable, not a courtesy — get the trees moved, green and handed
over, and leave anything optional for afterwards.

This pass moves exactly two trees:

```
C:\Dev\SMR-OptInPack   ->  B:\Dev\SMR\SMR-OptInPack
C:\Dev\SMR-Assets      ->  B:\Dev\SMR\SMR-Assets
```

Everything else — the fix pack, the TestKit, the archived game source, the Workshop corpus,
`SMR-CommunityMods`, `SMR-CommunitySaveRescue`, the FR-1 folders — **stays on `C:` this pass** and
moves later. `B:\Dev\SMR` exists and is empty.

## Read first, and build on it rather than repeating it

`SMR-OptInPack/docs/agent/support/MOVE_PATH_INVENTORY_20260921.md` (`baaefd1`) already inventories
every absolute path in both trees and says who repoints each: **5 editor-held, 29 in scripts, 13 in
config, 134 in prose**, each named by file and line. Re-derive its counts at the head of your work
(the same grep it records) so you are acting on today's numbers, and say if they moved.

## The boundary — another seat owns part of this, and it is not negotiable

The train orchestrator holds the train hub's ongoing build. **Yours:** the move itself, every prose
path reference, the `docs/` maps, `doccheck.py` and the packaging tooling, and doccheck green
afterwards. **Theirs, and you do not edit the contents:**

- `tools/devmods/**` and `tools/prototypes/**` — move the files, never rewrite paths inside them.
  They are editor-generated and stamped "DO NOT EDIT MANUALLY".
- The five mod symlinks in `%APPDATA%\Surviving Mars Relaunched\Mods\`. Three of them
  (`SMR-OptInPack`, `SMR-TrainHubDev`, `SMR-TrainHubPrototype`) die the moment you move the tree and
  **the mod silently ceases to exist for the game** until they are recreated.
- The five editor-held paths in `SourceData/`, the dev mod's test scripts, and the verification
  import with the owner.

⛔ **Why, measured 2026-09-21:** the Mod Editor *stores* absolute paths and *reasserts* them over a
drag — drop a different FBX on the Importer and it silently imports the stored one, no error, nothing
visibly wrong. It cost the owner an import and an hour. Those files are repointed with the editor
closed and proven by reading the Importer's header, which is not a bulk find-and-replace.

**Do not "fix" these:** the three Blender proof JSONs under `trainhub/blender/` whose `command` field
records the path a past run executed at, and `_before_claude_pass2_20260918/` plus
`export/build_workfile_build3.py`, which are historical snapshots carrying a donor path that predates
this tree. They are evidence, not configuration.

## End state

1. **Nothing is deleted this pass.** Copy each tree to its destination, verify, then rename the
   original to `<name>__MOVED_20260921` in place. The owner deletes the originals after the
   whole-move audit passes; say so in your report.
2. **Proof of an intact copy**, per tree: file count and total bytes before and after, `git fsck`
   clean, `git status -sb` matching the pre-move state (the train seat's in-progress files stay dirty
   — list them with a sha256 each, do not commit them: the audit cannot re-observe a dirty set that
   has since been worked on), HEAD sha identical and written down, remotes unchanged, and every tag
   still resolving (`hub-model-final-untextured`, `hub-centre-lights-20260921`).
3. **The environment variables do most of the work.** `doccheck.py:66` and
   `sync_from_fixpack.py:51,333,337-338` already read `SMR_TESTKIT`, `SMR_FIXPACK`, `SMR_SRCARCHIVE`
   and `SMR_TRAINASSETS`. Prefer extending that pattern over hard-coding a new absolute path
   anywhere. Deliver the owner ONE fenced copy-paste block that sets them (user scope, `setx`), with
   `SMR_TRAINASSETS` pointing at the new assets root and the rest still on `C:` this pass.
4. **Prose, maps and config repointed** in the moved trees: the 134 prose references, the `docs/`
   maps including the "Outside the repo" block, `.claude/settings.json`'s six permission entries, and
   the two test JSONs' `kit`/`park` keys. In the FIX PACK, repoint only LIVE pointers to the moved
   trees (its map's "Outside the repo" block, any live prompt); a record that says where something
   was is a record — leave it.
5. **The hard-coded scripts the inventory lists as needing a rewrite** — but only the ones outside
   the other seat's boundary. `SMR-Assets/_shared/geometry/*` and
   `trainhub/blender/build_workfile.py` are yours; anything under `tools/devmods/**` or
   `tools/prototypes/**` is theirs, including `tests/traffic_smoke.py` and `tests/record_evidence.py`.
   Where a path you may not edit is wrong after the move, LIST it for them instead.
6. **doccheck GREEN in the moved opt-in pack, run from its new root**, with its selftests, PACK
   IGNORE PARITY and LOCAL gate passing, and the fix pack still GREEN.
7. **A handover message to the train orchestrator**, in your report, giving exactly what they asked
   for: the final paths of `tools/devmods/train_hub` and `tools/prototypes/train_hub`, the new root
   of `SMR-Assets`, and confirmation that doccheck is green. They then recreate the symlinks, set
   their own paths and run the verification import with the owner.

If budget runs out, drop in this order: the fix pack's pointers, then the config keys, then prose in
reports. Never drop the copy verification, the environment block or the handover message.

## Your call

How you copy (robocopy, `cp -a`, a clone plus working-tree copy) and how you prove the copy is
faithful, as long as the proof is a command's output and not an assertion. Whether the two repos move
in one commit-and-verify unit or two. Whether `.claude/` (git-ignored, local) moves with the tree or
is recreated — say which you did and why, and note that Claude Code's own memory store for a project
is keyed by the project path, so a moved tree starts with an empty memory unless its memory folder is
carried across; flag that to the owner rather than deciding it for them.

## Scope

In: the two trees, their paths, their gates, the owner's environment block, the handover message.
Out: the fix pack's own move, the TestKit, the game source archive, the Workshop corpus, FR-1, the
Mod Editor, the game, and anything inside the other seat's boundary.

## Stops — report instead of pushing on

A file you must change is one the train orchestrator owns · a copy's count, bytes or HEAD does not
match and you cannot show why · doccheck REDs at the new root for a reason that is not a path you
introduced.

## Do not claim

That the move is complete: the whole-move audit grades it and the symlinks are not yours. That no reference
to the old path remains — count both sides and give the number that is left, by class, naming which
belong to the other seat. That the game or the mod works: nothing here launches either.
