# The fix pack, the TestKit and the captures moved to `B:\Dev\SMR` — last pass

Doc orchestrator, 2026-09-21, from `MOVE_FIXPACK_high.md` (authoring sha `69b4bbc`; `git diff --stat
69b4bbc..HEAD -- tools/ docs/README.md` was empty at the start, so the brief's facts held). Session
rooted at `B:\Dev\SMR\SMR-OptInPack`, model **Claude Opus 5 (`claude-opus-5[1m]`)**, from the
transcript. **One audit grades the whole move** (`MOVE_AUDIT_high.md`); this report only witnesses the
moment of the move.

```
C:\Dev\SMR-BugFixPack          ->  B:\Dev\SMR\SMR-BugFixPack          copied, verified — ⚠️ original NOT renamed (§7)
C:\Dev\SMR-BugFixPack-TestKit  ->  B:\Dev\SMR\SMR-BugFixPack-TestKit  copied, verified, original renamed
C:\Dev\SMR-ScreenCaptures      ->  B:\Dev\SMR\SMR-ScreenCaptures      copied, verified, original renamed
```

⛔ **Nothing was deleted.** `C:\Dev\SMR-BugFixPack-TestKit__MOVED_20260921` and
`C:\Dev\SMR-ScreenCaptures__MOVED_20260921` are in place. `C:\Dev\SMR-BugFixPack` could not be renamed
because another process holds it; the owner's block is in §7. **The `B:` trees have been live since the
copies verified.** Every commit below landed on `B:`, and nothing was written, pulled or committed in
`C:\Dev\SMR-BugFixPack` after the copy. (One `git fetch` ran there during the switch check. A re-capture
taken afterwards was byte-identical to the pre-copy capture, so it changed nothing.)

## 1 · Proof of an intact copy

`capture.py` ran identically on both sides. It walks without following reparse points and hashes every
file (sha256 of the relative path, size and file hash for every row, sorted). The before and after
outputs were diffed, and every row matched in all three trees. The one exception was the fourth junction,
which was recreated separately (§2). Copy method: `robocopy /MIR /COPY:DAT /DCOPY:DAT /XJ` for all three
trees, exit 1 (robocopy's success code), 0 failed.

| | `SMR-BugFixPack` | `SMR-BugFixPack-TestKit` | `SMR-ScreenCaptures` |
|---|---|---|---|
| files (of which `.git`) | 6945 (4841) | 1185 (1148) | 81 (0) |
| directories | 480 | 266 | 1 |
| bytes (of which `.git`) | 186,349,325 (77,187,778) | 3,784,088 (2,993,672) | 1,112,959,418 |
| rows digest, both sides | `7e979806…33533de4` | `27e8793f…29e9e789b` | `b1b91c00…09a5b81f` |
| HEAD at copy | `69b4bbce953c2ed882b6e4b463f6ec3c948b5a45` `main` | `3abab0a306e0523d2e71297b5d2a2987006392c8` `master` | not a repo |
| `git fsck` | exit 0, 0 non-dangling lines, both sides | exit 0, 0 non-dangling lines, both sides | — |
| refs digest (`for-each-ref`) | `a21617e2…` both sides | `be56cc84…` both sides | — |
| remote | `origin` → `catt144/SMR-CommunityFixPack.git`, unchanged | **none**, unchanged | — |
| `status --porcelain` | 0 entries | `M Code/80_AgentSlots.lua` only | — |

- The brief's HEADs (`26b86e7`, `3abab0a`) were re-derived. The fix pack had advanced to `69b4bbc`, the
  commit that authored the brief, with nothing unpushed (`git log origin/main..` empty). The TestKit
  HEAD matched.
- **The TestKit's dirty file** (the train seat's live sitting) went across uncommitted and was never
  staged, committed or restored. Its sha256 is `1881b1ccaed82ff476d0b665bbfbde73b6d16c4b7f8da7d0727eba6b4d0458cc`,
  identical at `C:` before the copy, at `B:` after it, and at `C:` again at the switch.
- **`SMR-ScreenCaptures` was hashed in full**, all 81 files, rather than sampled.
- **Git-ignored material came with the filesystem copy.** No clone was involved, so `local/`, `.claude/`,
  `zz-owner/` and `scratch/` are covered by the same row digest. doccheck at the new root reads
  `LOCAL SIZE: 866 file(s), 52.7 MB under local/`.
- Size: `du -sh` of the new fix pack, which does not follow junctions, is **191M**, against the brief's
  "about 195 MB".

## 2 · The four junctions

`cmd /c dir /A:L /S /B` over the old tree listed exactly the four the brief names, with no extras. The
TestKit and the captures folder had none. `/XJ` kept all four out of the bulk copy, and each was
recreated with `mklink /J`. The sweep of the new tree, with PowerShell `LinkType`:

```
B:\Dev\SMR\SMR-BugFixPack\saves\backup              | Junction | C:\Users\stkot\AppData\Roaming\Surviving Mars\76561198020568696
B:\Dev\SMR\SMR-BugFixPack\saves\game                | Junction | C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696
B:\Dev\SMR\SMR-BugFixPack\zz-owner\all-claude-memory | Junction | C:\Users\stkot\.claude\projects
B:\Dev\SMR\SMR-BugFixPack\zz-owner\claude-memory     | Junction | C:\Users\stkot\.claude\projects\b--Dev-SMR-SMR-BugFixPack\memory
```

The two `saves` targets and `all-claude-memory` are unchanged. **`claude-memory` is repointed** at the
store's new key and was created after that store was copied (§5). Its `MEMORY.md`, read through the
junction, hashes `24708539…6347909`, the same as the source. No save file was read, written or copied.

## 3 · `core.hooksPath`, and the hook proven

- Fix pack: before the change, `git config --local core.hooksPath` read `c:\Dev\SMR-BugFixPack\tools\hooks`
  in the copied `.git/config`. **It is now the relative `tools/hooks`** at `B:`. It was proven by the
  first commit landed there (`af0c7dd`), which printed doccheck's `COUNTS:` block and `doccheck: GREEN`
  from inside the pre-commit hook.
- **TestKit: nothing to set.** It has no `tools/hooks/` directory and no `core.hooksPath` at any scope.
  The brief's "BOTH new repos" has no second target there. The fork already reads `tools/hooks`, and its
  hook fired on both of this pass's fork commits (`doccheck: GREEN` in each).

## 4 · What was repointed

**The in-code defaults are sibling-relative now**, so the next move cannot strand them. Every one
resolves to an existing path (checked by importing or evaluating each):

| where | default now | resolves to |
|---|---|---|
| `tools/doccheck.py:62`, `aliascheck.py:63`, `deskbench.py:73` | `SMR_TESTKIT` → `<parent of repo>\SMR-BugFixPack-TestKit` | `B:\Dev\SMR\SMR-BugFixPack-TestKit` ✅ |
| `tools/doccheck.py` PUSH_SET memory row | `SMR_MEMORY` → key derived from `REPO` (`_memory_project_key`, the fork's `ba53835` form) | `…\projects\b--Dev-SMR-SMR-BugFixPack\memory\MEMORY.md`, 16,152 LF-bytes ✅ |
| `tools/store_screenshots.py:19` | `<parent>\SMR-ScreenCaptures\c74_skins` | exists ✅ |
| TestKit `Code/74_SMRTK_Agent.lua:109` | `B:/Dev/SMR/SMR-ScreenCaptures/` (the engine takes an absolute folder) | read through the mod junction ✅ |
| fork `tools/sync_from_fixpack.py:52` / `:338` | `SMR_FIXPACK` / `SMR_TESTKIT` → siblings of the fork's `REPO` | the sync report reads `this repo <- B:\Dev\SMR\SMR-BugFixPack`, no SKIPPED line ✅ |

**No `SMR_*` variable is set** in User, Machine or Process scope (measured). No `setx` was run, per the
owner's 09-21 ruling.

### Commits, by tree

| tree | commit | what |
|---|---|---|
| fix pack (`B:`) | `af0c7dd` | the four tools above, `SMRTK.md` (4: the location line and three gate commands), `docs/README.md` ("Outside the repo" TestKit + captures entries, plus one Path translation line), and **32 scripted substitutions**: `WORKFLOW.md` (3), `TESTKIT.md` (2), `arming/README.md` (1), the ten `arming/legs/*.json` `kit`/`park` keys (20), `still-needed/F46_NATIVE_LEG.json` `kit`/`park` (2: a runnable leg's config, not its citations), live prompts `fixtoggles/08` (1), `perma/HANDOFF_ORCHESTRATOR` (1), `smrcf-verify/C35_DETECTOR` (1), and `bugs/C74.md:55` (the full-res originals' location) |
| fix pack (`B:`) | *this report's commit* | this report, plus the deletion of `MOVE_FIXPACK_high.md` and its `prompts/README.md` row |
| TestKit (`B:`) | `d199eb2` | `74_SMRTK_Agent.lua:109` and `README.md`'s `mklink` install line. Committed by pathspec; `80_AgentSlots.lua` untouched |
| fork | `f7ae2e4` | `sync_from_fixpack.py` (51, 337, docstring), `CLAUDE.md` (2) with `AGENTS.md` `--regen`'d, `.claude/skills/{doc-editing,smr-bug-library}` (1 each) with the `.agents/` mirrors regenerated, `docs/README.md` (4, plus a Path translation sentence), `WORKFLOW.md` (4), `gamepatch/README.md` (3), `KNOWLEDGE_SYNC_PASS.md` (5), `RELEASE_SYSTEM_high.md` (2), `DRONE_REBUILD_BUILD_high.md` (2), `FIX_D02_D03_D04_1_1_0_medium.md` (2) |
| fork | `7ce3a85` | `support/CO_RUNS.md:151`, a runnable `git -C` line |

The scripted substitutions ran with a per-file expected count. The guard fired once:
`RELEASE_SYSTEM_high.md` held **2** live references, not 1 (line 8 is a staleness-check command), and
the file was re-run at 2. `CO_RUNS.md` was **missed by the first grep sweep** and caught by the by-class
recount below.

**Git-ignored, on disk, no commit:** fix pack `.claude/settings.json` (4 permission entries) and
`.claude/agents/doc-surgeon.md:9` (1); fork `.claude/settings.json` (4).

### For the coordinator seat: every `.claude/` line changed

```
B:\Dev\SMR\SMR-BugFixPack\.claude\settings.json:4-7   git -C C:\\Dev\\SMR-BugFixPack[-TestKit] ...  ->  B:\\Dev\\SMR\\SMR-BugFixPack[-TestKit] ...  (4 entries)
B:\Dev\SMR\SMR-BugFixPack\.claude\agents\doc-surgeon.md:9   `C:\Dev\SMR-BugFixPack`  ->  `B:\Dev\SMR\SMR-BugFixPack`
```

Nothing else in `.claude/` was touched. `HANDOFF_PROMPT.md:3`'s `Fire with:` already named `B:`.
**Its line 5 is now stale prose** ("If it has not, the tree is still `C:\Dev\SMR-BugFixPack`"), and so
are its move-pass lines 54–61 and 85. They are the seat's prose and are left to it.

### ⚠️ A knowledge sync pass is OWED — on the owner's yes, fired from the fork

The fork's `sync_from_fixpack.py --tools` now reports `DRIFT` on the two mirrored docs,
`tools/SMRTK.md` and `tools/TESTKIT.md`, and `RECHECK` on `doccheck.py`, among others. Per the brief,
neither mirrored doc was hand-edited in the fork. **Until that pass runs, the fork's
`tools/doccheck.py:66` still defaults to `C:\Dev\SMR-BugFixPack-TestKit`**, and now that the original
is renamed the fork's TestKit legs report `TestKit not found` / `TESTKIT TREE: not checked`. The fork
stays GREEN; this was measured by running its doccheck with `SMR_TESTKIT` pointed at a missing path. The
donor's `aliascheck.py` and `deskbench.py` are `TOOLS_NOT_PORTED` in the fork, so nothing is owed for
them.

## 5 · The Claude memory store

```
from  C:\Users\stkot\.claude\projects\c--Dev-SMR-BugFixPack         (still present, untouched)
to    C:\Users\stkot\.claude\projects\b--Dev-SMR-SMR-BugFixPack
```

| | source | destination |
|---|---|---|
| files / dirs | 669 / 138 | **669 / 138** |
| bytes | 699,046,373 | **699,046,373** |
| rows digest | `d46a6bd6…cde1e4f` | **`d46a6bd6…cde1e4f`** |
| `memory/` files | 77 | **77** |
| `memory/MEMORY.md` sha256 | `24708539…6347909` | **identical** |

**Transcripts came across with the store, not only `memory/`.** The session transcripts are what
`--resume` and the history view read from the new root. The cost is disk on `C:` until the owner deletes
the old key, and the old key is kept for the audit anyway. That matches pass one, which copied its whole
store. The source's newest transcript was written at 13:20, before this pass began, so no session was
writing into it during the copy. No memory file was edited.

**The key name is derived, not yet observed.** The rule reproduces the whole destination path, which
gives `b--Dev-SMR-SMR-BugFixPack`. The new doccheck derives the same key from `REPO` and reads the
copied `MEMORY.md` through it. **Confirming it is the first session rooted at
`B:\Dev\SMR\SMR-BugFixPack`: check that the memories load.**

## 6 · The mod junctions

```
SMR-BugFixPack          | Junction | B:\Dev\SMR\SMR-BugFixPack               (was C:\Dev\SMR-BugFixPack; recreated)
SMR-BugFixPack-TestKit  | Junction | B:\Dev\SMR\SMR-BugFixPack-TestKit       (was C:\Dev\...; recreated)
SMR-OptInPack           | Junction | B:\Dev\SMR\SMR-OptInPack                (train seat's; not touched)
SMR-TrainHubDev         | Junction | B:\Dev\SMR\SMR-OptInPack\tools\devmods\train_hub     (not touched)
SMR-TrainHubPrototype   | Junction | B:\Dev\SMR\SMR-OptInPack\tools\prototypes\train_hub  (not touched)
SMR_FR1TempWorkaround   | real folder                                        (FR-1's; left, owner ruling)
```

Each junction was proven by reading a file **through it** that differs between the trees.
`Mods\SMR-BugFixPack\docs\README.md:122` reads `` `B:\Dev\SMR\SMR-BugFixPack-TestKit` `` (the old tree
still says `C:`), and `Mods\SMR-BugFixPack-TestKit\Code\74_SMRTK_Agent.lua` shows the `B:` capture
folder. Both sha256s equal the `B:` files. The old fix pack junction was **still resolving** to the
unrenamed `C:` tree, so without this step the game would have kept loading the stale copy without any
error.

## 7 · Owner block — one step needs your hands

`C:\Dev\SMR-BugFixPack` refused to rename twice: `The process cannot access the file because it is
being used by another process`. No process command line names it. The likely holder is a VS Code window
or a terminal opened on that folder. **Already run by me:** every copy, every junction, the two other
renames, the memory store copy and every commit listed here. **Left for you**, once whatever has
`C:\Dev\SMR-BugFixPack` open is closed:

```bat
cd /d C:\Dev
git -C C:\Dev\SMR-BugFixPack status --porcelain
git -C C:\Dev\SMR-BugFixPack log --oneline -1
ren "C:\Dev\SMR-BugFixPack" "SMR-BugFixPack__MOVED_20260921"
dir /B C:\Dev\SMR-BugFixPack__MOVED_20260921\saves
```

The first two lines should print nothing and `69b4bbc`. Anything else means work landed in the
abandoned tree after the copy, and it needs carrying across before the rename. Renaming the parent does
not touch the four junctions inside it or their targets. Do **not** delete through it.

**Done later on 09-21 by the post-move coordinator seat, at the owner's request.** Before the rename,
`status --porcelain` printed nothing and `log -1` printed `69b4bbc`. The holder was nine orphaned
MSYS log watchers from dead agent sessions (`tail -f` / `grep --line-buffered` on game logs, the
oldest from 08-11, plus one looping `bash` from 09-15). `readlink /proc/*/cwd` in Git Bash showed
their working directory was inside the tree. They were stopped, and the rename succeeded:
`C:\Dev\SMR-BugFixPack__MOVED_20260921` exists, `C:\Dev\SMR-BugFixPack` does not, and its `saves`
lists `backup`, `game` and `reporters`.

## 8 · doccheck

- **Fix pack, run from `B:\Dev\SMR\SMR-BugFixPack`: `doccheck: GREEN`**, with every selftest passing,
  `TOOLS COMPILE: PASS (70 …)`, `PACK IGNORE PARITY: PASS — 18 filters`, `LOCAL: PASS`, `EOL: PASS`,
  `PARSE: 33 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s)` (the sibling-relative default at
  work), and **`PARENT FILES (B:\Dev\SMR): none`**.
- `ALIASCHECK` shows 10 `UNKNOWN` findings (report-only). They are pre-existing: the same 10 appear
  against the old `C:` TestKit.
- **Fork: GREEN** on both of its commits.

## 9 · What is left, by class

`count_refs.py` walks without following junctions and skips `.git`, `saves/` and `zz-owner/`. It
counts `C:\Dev\SMR-BugFixPack*` and `C:\Dev\SMR-ScreenCaptures` in every slash and escape form. Counted
before this report existed and before the brief was deleted:

| class | fix pack | TestKit | fork | verdict |
|---|---|---|---|---|
| live, deliberate: Path translation blocks | 2 | — | 3 | they name the old paths on purpose |
| live, flagged: `metadata.lua:504` comment | 1 | — | — | a shipped file: changing it changes the upload's bytes, so it rides a real release change |
| live, OWED to the sync pass (§4) | — | — | 7 (`SMRTK.md` 4, `TESTKIT.md` 2, `doccheck.py:66` 1) | mirrored/adapted; the donor is already changed |
| train seat: `tools/devmods/` | — | — | 3 (`read_leg.json`, `smoke_leg.json` `kit`; `record_evidence.py:23` saves path) | theirs; ⚠️ the two legs now point at a renamed kit |
| this brief (deleted in this report's commit) | 7 | — | — | gone with the file |
| records: `docs/agent/reports/` | 41 | — | 10 | past commands, citations, and the earlier move reports |
| records: `docs/archive/` | 40 | — | 221 | append-only |
| records: `docs/agent/bugs/` | 0 | — | 3 (`D06`/`D07`/`D12`, retired entries' kit-line citations) | untouched |
| git-ignored: `.claude/` | 16 | — | 0 | coordinator's records and evidence; the live 5 are done (§4) |
| git-ignored: `local/`, `scratch/` | 1 + 9 | — | — | a one-shot script and handoff snapshots |
| **total** | **117** | **0** | **248 → 247** after `7ce3a85` | |

Presence side: `B:\Dev\SMR\SMR-(BugFixPack|ScreenCaptures)` occurs 58 times in the fix pack, 2 in the
TestKit and 35 in the fork, counted at the same moment and before `7ce3a85` (which adds one to the fork).

Records stay records. The pass-one warning held: rewriting the 41 report and 40 archive references would
have been the defect.

## 10 · Pushes

- **Fix pack:** pushed from `B:` with this report's commit. `origin/main` then carries `af0c7dd` and the
  report commit.
- **Fork: not pushed.** It is 7 commits ahead of `origin/main`, and 5 of them are other seats'
  (`4126be3` … `0d32f52`). Pass one declined to publish other seats' commits and pass two published them.
  The disagreement is the owner's to settle, so I did not pick a side. Mine are `f7ae2e4` and `7ce3a85`.
- **TestKit:** no remote, by design.

## 11 · Not claimed

- **That the move is complete.** `MOVE_AUDIT_high.md` grades it, and `C:\Dev\SMR-BugFixPack` still
  carries its original name until the §7 block runs.
- **That no reference to the old paths remains.** §9 counts 117 / 0 / 247 by class, and 7 of the fork's
  wait on the sync pass.
- **That the mods load.** Nothing launched the game. A junction that resolves is not a loaded mod.
- **That the memory key is right.** It is derived and cross-checked by doccheck, not yet observed by a
  session rooted there (§5).
