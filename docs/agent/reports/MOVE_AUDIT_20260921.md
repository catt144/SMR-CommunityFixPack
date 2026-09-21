# Whole move audit — FAIL

Independent audit, 2026-09-21, run from fix-pack `b58d14a`. This grades all three move
reports and their deleted briefs. It did not repair a moved tree, rerun a mover, open the Mod
Editor or game, or test the owner's verification import.

## Verdict

**FAIL.** The copies and Git histories are intact, the new root and junction topology are sound,
and the remote-backed repositories are current. The move is not ready for its held originals to be
deleted, for six ranked reasons:

1. **Player-pack leak:** the fix pack's predictor would ship three files from `scratch/`, despite the
   move-audit requirement that `scratch/` remain excluded. `doccheck` stays GREEN because
   `metadata.lua` and `pack_predict.py` omit the same filter, so PACK IGNORE PARITY agrees on the
   same defect.
2. **Broken FR-1 tools:** five runnable Python files in `SMR-FR1` retain nine literals for moved,
   now-missing roots.
3. **Incomplete fork gate:** the opt-in pack's TestKit default still names the missing C: kit. Its
   GREEN doccheck explicitly says `TestKit not found` and `TESTKIT TREE: not checked`. The same owed
   sync leaves six stale commands in the two mirrored TestKit docs.
4. **Stale live documentation:** CommunitySaveRescue has three live directions to missing C: roots.
5. **Held-original evidence changed:** the old opt-in Claude store no longer matches the move
   report; its entire `memory/` directory is gone.
6. **Mover crossed the train-seat boundary:** first-pass commit `f2ec95d` changed two files under
   `tools/devmods/**`, where the brief required an empty mover diff.

The first four break the result promised by the move. Finding 5 prevents a clean preservation
verdict. Finding 6 is an ownership/procedure failure even though its two path substitutions are
functionally correct.

## Ranked findings and commands

### 1 · `scratch/` would ship in the fix pack

Command:

```powershell
python tools/pack_predict.py B:\Dev\SMR\SMR-BugFixPack --json
```

Filtered result:

```text
packed from local/:   0
packed from scratch/: 3
scratch/HANDOFF_PROMPT_before_20260921.md
scratch/HANDOFF_PROMPT_before_close_20260921.md
scratch/HANDOFF_PROMPT_before_postmove_20260921.md
```

`rg -n 'scratch|local' tools/pack_predict.py metadata.lua` finds `*/local/*` in both fix-pack
files but no `*/scratch/*`. The same command in the fork finds both filters, and its predictor packs
neither directory. The defect reaches the next fix-pack build: internal handoff snapshots become
player payload. It also explains why `PACK IGNORE PARITY: PASS — 18 filters` is not a falsifier.

### 2 · Five FR-1 scripts have nine dead moved-root literals

Command:

```powershell
rg -n --hidden --no-ignore --glob '!**/.git/**' `
  'C:[\\/]+Dev[\\/]+SMR-' B:\Dev\SMR\SMR-FR1
```

The live moved-root subset is:

| file | dead literals | missing target(s) |
|---|---:|---|
| `SMR-FR1-TempMod-2026-09-11/tools/tempmod_harness.py` | 3 | TempMod, CacheRoute-V2, SrcArchive |
| `SMR-FR1-TempMod-2026-09-11/tools/make_preview.py` | 1 | TempMod |
| `SMR-FR1-TempMod-2026-09-11/tools/identify_dump_names.py` | 2 | CacheRoute-V2, TempMod |
| `SMR-FR1-CacheRoute-V2-2026-09-11/make_receipt.py` | 2 | BugFixPack, SrcArchive |
| `SMR-FR1-CacheRoute-V2-2026-09-11/probe_harness.py` | 1 | SrcArchive |

`Test-Path` is false for every direct C: root named above. The surviving 55 FR-1 old-path
occurrences are captured command/evidence fields in `rays-coverage.json` and `zip-audit.json` and
remain records. Other scripts also name older FR-1 inputs that were already absent and were not
among the moved roots; this audit does not turn those into move defects.

### 3 · Fork doccheck is GREEN with its TestKit legs skipped

Commands and result:

```powershell
Get-ChildItem Env: | Where-Object Name -like 'SMR_*'
[Environment]::GetEnvironmentVariables('User')    # filter SMR_*
[Environment]::GetEnvironmentVariables('Machine') # filter SMR_*
# all three scopes: no SMR_* entries

python tools/doccheck.py   # from B:\Dev\SMR\SMR-OptInPack
```

```text
NOTE: TestKit not found at C:\Dev\SMR-BugFixPack-TestKit — probe count skipped
TESTKIT TREE: not checked (no repo at C:\Dev\SMR-BugFixPack-TestKit)
doccheck: GREEN
```

`tools/doccheck.py:66` is the stale default. The remaining default routes in both repos resolve:
the fix pack's sibling TestKit, archive root, Steam install and manifest, both derived memory keys,
the fork's donor/archive/TestKit/train-assets sync routes, and the screenshot destinations.
No tool reads `SMR_SRC_ARCHIVE`; code uses the unified `SMR_SRCARCHIVE` name.

The read-only `python tools/sync_from_fixpack.py` does find the donor at
`B:\Dev\SMR\SMR-BugFixPack` and emits no donor `SKIPPED` line, but reports:

```text
DRIFT tools/SMRTK.md
DRIFT tools/TESTKIT.md
```

Those files retain four and two C: TestKit commands respectively. This is the previously declared
knowledge-sync debt, owned by the fork's sync pass on the owner's yes, not an undeclared edit by the
mover. It still prevents this audit from calling the fork's gate complete.

### 4 · CommunitySaveRescue's live directions name missing roots

Command:

```powershell
rg -n 'C:[\\/]+Dev[\\/]+SMR-' CLAUDE.md docs/PROVENANCE.md
```

Result: `CLAUDE.md:56` sends the reader to the fix-pack D13 report at its missing C: root;
`docs/PROVENANCE.md:16` does the same for the frozen spec, and line 51 states the repo folder is the
missing C: path. These are prose consumers the rest-pass mover owned, not dated command output.

### 5 · The held old opt-in memory store was altered

Command:

```powershell
Get-ChildItem <store> -Recurse -File -Force | Measure-Object
Test-Path <store>\memory\MEMORY.md
Get-FileHash <store>\memory\MEMORY.md -Algorithm SHA256
```

| store | files now | `memory/MEMORY.md` |
|---|---:|---|
| old `c--Dev-SMR-OptInPack` | 94 | **missing** |
| new `b--Dev-SMR-SMR-OptInPack` | 104 | present, `A467CEAF…C65DF` |
| old `c--Dev-SMR-BugFixPack` | 669 | `24708539…47909` |
| new `b--Dev-SMR-SMR-BugFixPack` | 670 | same `24708539…47909` |

The first-pass report recorded 102 files and a 794-byte `MEMORY.md` in both opt-in stores, hash
`438766D1…E517`, and said the source remained held. The new store's later growth is expected from
live use. The old store's loss of eight files and `memory/` is unexplained by Git and means it is no
longer the retained source witnessed by the report. No audit file was written there.

### 6 · A mover changed two train-seat files

Command:

```powershell
git -C B:\Dev\SMR\SMR-OptInPack diff-tree --no-commit-id --name-status -r `
  f2ec95d -- tools/devmods tools/prototypes
```

Result:

```text
M tools/devmods/train_hub/tests/read_leg.json
M tools/devmods/train_hub/tests/smoke_leg.json
```

The commit changed each `park` field from the old opt-in root to the new one. The first-pass report
declared this exception, but the audit brief says the mover was to list the train test scripts and
leave their content unchanged. All other identified mover commits have an empty diff over
`tools/devmods/**` and `tools/prototypes/**`.

## Copy, history, dirty-set and remote proof

For each repository, `git merge-base --is-ancestor <reported-pre-move-head> HEAD` exited 0. It was
run for OptIn `456a940`, Assets `41890eb`, FixPack `69b4bbc`, TestKit `3abab0a`, and both community
repos (whose current HEADs remain exactly the reported ones). `git fsck --full --no-progress` exited
0 in all eight repos. OptIn, Assets and FixPack report only dangling objects; no run emitted
`error`, `fatal`, `bad`, `missing` or `broken`.

The retained-original comparison hashed every working-tree file with SHA-256 while excluding
`.git` and reparse points:

| moved content | result against held original | later difference attribution |
|---|---|---|
| OptIn | no missing original file; 51 changed, 1 added | 38 tracked paths have post-move commits; generated textures/pyc and the mover-reported ignored settings explain the rest |
| Assets | no missing original file | 10 tracked paths in `9f2c201`/`df9bb50`; generated exports/pyc explain ignored differences |
| CommunityMods | 1,765 files byte-identical | none |
| CommunitySaveRescue | 8 files byte-identical | none |
| SrcArchive | 9,168 files byte-identical | initial `SMR-Shared` commit |
| Workshop corpus | 6 files byte-identical | initial `SMR-Shared` commit |
| FR-1 TempMod | 25 files byte-identical | initial `SMR-FR1` commit |
| FR-1 CacheRoute-V2 | 547 files byte-identical | initial `SMR-FR1` commit |
| FR-1 DevPackage | 12 files byte-identical | initial `SMR-FR1` commit |
| FR-1 DevPackage.zip | SHA-256 `216c313b…1760b9d` identical | initial `SMR-FR1` commit |
| FixPack | one moved brief removed, 32 changed, 2 added | `af0c7dd`, `c2fa9dc`, `b58d14a`; ignored `.claude`/scratch/pyc as reported |
| TestKit | 2 changed | `d199eb2` |
| ScreenCaptures | all 81 files byte-identical | none |

The TestKit dirty set is preserved: `Code/80_AgentSlots.lua` is the only dirty tracked file in both
copies and hashes `1881b1cc…0458cc`, exactly the report's value.

Remote and tag check:

- `git ls-remote --heads --tags origin` shows current `main` for FixPack, OptIn,
  CommunityMods and CommunitySaveRescue. FixPack's two tags are remote.
- OptIn's five local tags, including `hub-model-final-untextured` and
  `hub-centre-lights-20260921`, match the held original but are not advertised by its remote.
- Assets, TestKit, Shared and FR1 have no remote. Assets and OptIn each retain all five reported
  local tags; the remaining local-only repos have none.

No content loss or broken Git object was found. That is not the same as safe deletion; see below.

## Gates and tool routes

Fix-pack `python tools/doccheck.py` is fully GREEN: all selftests, 70-tool compile, 18-filter PACK
IGNORE PARITY, LOCAL, 33-file TestKit parse, and `PARENT FILES (B:\Dev\SMR): none` ran. Its predictor
finding above independently refutes the meaning of the parity result.

Opt-in `python tools/doccheck.py` is GREEN with its selftests, 27-tool compile, 16-filter parity and
LOCAL gate, but the TestKit probe count and tree leg did not run. Its own predictor currently finds
no packed `local/` or `scratch/` file.

The TestKit tries `B:/Dev/SMR/SMR-ScreenCaptures/` before its deliberate `AppData/` fallback, and
`tools/store_screenshots.py` resolves to the existing sibling `SMR-ScreenCaptures/c74_skins`.
Nothing here launched the game, so this is source/configuration proof, not proof that the TestKit
took the first runtime branch.

## Old-root sweep, counted both ways

The exact-root sweep covered all thirteen reported old roots in slash, backslash and JSON-escaped
forms. It used `rg --hidden --no-ignore --pcre2`, excluding `.git/**`, `saves/**` and `zz-owner/**`
so no junction was traversed.

| current tree | exact old-root occurrences / files | current B:-root occurrences / files |
|---|---:|---:|
| OptIn | 309 / 46 | 99 / 38 |
| Assets | 28 / 12 | 12 / 10 |
| Shared | 0 / 0 | 0 / 0 |
| FR1 | 64 / 7 | 0 / 0 |
| CommunityMods | 0 / 0 | 0 / 0 |
| CommunitySaveRescue | 3 / 2 | 0 / 0 |
| FixPack | 2,047 / 216 | 176 / 61 |
| TestKit | 0 / 0 | 2 / 2 |
| ScreenCaptures | 0 / 0 | 0 / 0 |
| **total** | **2,451 / 283** | **289 / 111** |

A broader `C:\Dev\SMR-*` sweep finds 2,467 occurrences in 288 files; its extra 16 occurrences name
older FR-1 inputs and other roots that were not among the thirteen moved originals. Classification
of that broader presence side reconciles as follows:

| class | occurrences | owner / verdict |
|---|---:|---|
| fix-pack report/archive/history | 1,981 | dated record; keep |
| fix-pack prose | 24 | path-translation and dated context; no runnable stale route found |
| fix-pack live-code/config | 6 | historical source comments; records, not configuration |
| fix-pack ignored/local | 52 | coordinator evidence, snapshots and dated local output; keep, except the three snapshots must not pack |
| opt-in report/archive/history | 287 | dated record; keep |
| opt-in prose | 14 | path translation/dates; keep |
| opt-in ignored/local | 2 | records; keep |
| opt-in live/train boundary | 6 | train seat; three live stale routes named below |
| Assets live/config + other text + prose | 28 | proof commands/output and the recorded first home; keep |
| FR1 code/config | 9 | **rest-pass mover; finding 2** |
| FR1 captured JSON evidence | 55 | past commands/results; keep |
| CommunitySaveRescue prose | 3 | **rest-pass mover; finding 4** |
| **total** | **2,467** | reconciled |

The train-seat survivors are not defects of the move under the owner's boundary: the two test-leg
JSONs still name the old TestKit in `kit`, and `record_evidence.py:23` names the old fix-pack saves
path. The train seat owns those. The editor-held SourceData fields have since been repointed by that
seat. The Blender proof JSON `command` fields and `_before_claude_pass2_20260918/` remain unchanged
records, as required.

## Root, junctions, ignored material and handover

`Get-ChildItem -Force B:\Dev\SMR` finds exactly nine directories and no loose files: eight repos
plus the one cleared exception, `SMR-ScreenCaptures`. Every reported B: destination exists and every
old unsuffixed C: root is absent.

`cmd /c dir /A:L /S /B <tree>` finds exactly four junctions across the moved content, all in the
fix pack. PowerShell classifies all four as `Junction`, and all targets exist:

```text
saves/backup              -> AppData\Roaming\Surviving Mars\76561198020568696
saves/game                -> Saved Games\Surviving Mars Relaunched\76561198020568696
zz-owner/all-claude-memory -> C:\Users\stkot\.claude\projects
zz-owner/claude-memory     -> ...\b--Dev-SMR-SMR-BugFixPack\memory
```

The TestKit, ScreenCaptures and the other moved trees have zero junctions.

The AppData Mods folder has exactly six entries: five live junctions to B: and the owner-cleared real
folder `SMR_FR1TempWorkaround`. Reads through four junctions used files whose bytes differ between
new and held trees; their through-link hashes equal the B: files and differ from the C: originals
for FixPack `docs/README.md`, TestKit `Code/74_SMRTK_Agent.lua`, OptIn `docs/README.md`, and the dev
hub GFXMaterial file. The prototype junction explicitly targets B:, but its entire target subtree is
byte-identical to the held original, so the prescribed differing-byte witness does not exist; the
reparse target itself is the evidence for that one.

FixPack has `.claude/`, `local/`, `zz-owner/`, `scratch/` and tracked `local/README.md`. OptIn has
`.claude/`, `local/`, `scratch/` and tracked `local/README.md`; no report claimed an OptIn
`zz-owner/`. Effective `core.hooksPath` is relative `tools/hooks` in both packs and resolves inside
each B: tree. No repository points hooks at an original.

The first-pass handover contains all three requested paths and the GREEN ping. All three paths exist:

```text
B:\Dev\SMR\SMR-OptInPack\tools\devmods\train_hub
B:\Dev\SMR\SMR-OptInPack\tools\prototypes\train_hub
B:\Dev\SMR\SMR-Assets
```

## Original-by-original deletion verdict

No MSYS process has a working directory under a `__MOVED_20260921` tree; the nine old watchers no
longer block deletion. This read-only audit did not attempt a rename/delete, so it cannot exclude an
unrelated Windows handle.

"No" below means deletion reduces preserved material to one local copy or removes the only
full-tree rollback copy. It does not propose a remote, backup or policy.

| held original | safe to delete now? | consequence |
|---|---|---|
| `SMR-OptInPack__MOVED_20260921` | **No** | remote `main` is current, but all five tag refs and ignored material would have only the B: copy |
| `SMR-Assets__MOVED_20260921` | **No** | no remote; 504 MB repository, history and five tags fall to one copy |
| `SMR-SrcArchive__MOVED_20260921` | **No** | `SMR-Shared` has no remote; archive falls to one copy |
| `workshop_fpk_archive__MOVED_20260921` | **No** | same local-only Shared repo |
| `SMR-FR1-TempMod-2026-09-11__MOVED_20260921` | **No** | `SMR-FR1` has no remote |
| `SMR-FR1-CacheRoute-V2-2026-09-11__MOVED_20260921` | **No** | `SMR-FR1` has no remote |
| `SMR-FR1-DevPackage__MOVED_20260921` | **No** | `SMR-FR1` has no remote |
| `SMR-FR1-DevPackage.zip__MOVED_20260921` | **No** | `SMR-FR1` has no remote |
| `SMR-CommunityMods__MOVED_20260921` | **Yes, for repository recovery** | clean tree, no tags, current `main` is on origin |
| `SMR-CommunitySaveRescue__MOVED_20260921` | **Yes, for repository recovery** | clean tree, no tags, current `main` is on origin |
| `SMR-BugFixPack__MOVED_20260921` | **No as a full-tree rollback** | tracked history and both tags are remote, but load-bearing ignored material is not; deleting leaves its current ignored content single-copy |
| `SMR-BugFixPack-TestKit__MOVED_20260921` | **No** | no remote; deleting takes repository/history and the preserved dirty file to one copy |
| `SMR-ScreenCaptures__MOVED_20260921` | **No** | not a repo; 81-file capture set falls to one copy |
| old opt-in Claude key `c--Dev-SMR-OptInPack` | **No** | already diverged from the witnessed source and still contains 94 files absent from any remote contract |
| old fix-pack Claude key `c--Dev-SMR-BugFixPack` | **No** | no remote; deleting reduces the 669-file witnessed store to the one live new-key copy |

## Limits and final call

- The game and Mod Editor were not opened. Resolving junctions is not proof a mod loads.
- The owner-only verification import remains owed and is not a move defect.
- The TestKit source prefers the B: capture directory, but only a live game run proves it did not
  take the AppData fallback.
- The exact prototype junction read-through requirement could not use differing bytes because no
  file in that target changed after the move; target inspection and whole-subtree equality are
  reported instead of pretending an identical read distinguishes roots.

The move preserved bytes and history, but the live result is **not operationally complete** and its
held originals are **not generally safe to delete**. The useful outcome of this audit is therefore
FAIL.

## Coordinator adjudication, 2026-09-21 (added after the audit, for its recheck)

Each finding was cleared with its own check before the ruling.

| # | ruling | where |
|---|---|---|
| 1 | **Fixed.** `*/scratch/*` added to `metadata.lua` `ignore_files` and `pack_predict.py`. The predictor packs 57 files, 0 from `scratch/` or `local/`; PACK IGNORE PARITY reads 19 filters. This gap predates the move: `scratch/` was homed on 09-21 and only the fork got the filter. The `metadata.lua` comment's captures path is now sibling-relative too. | fix pack, this commit |
| 2 | **Fixed**: the nine literals, each checked to exist at its new target. Literals for FR-1 inputs that were already gone before the move are left alone. | `SMR-FR1` `0ab8d4a` (no remote) |
| 3 | **Fixed for the move.** The fork's `doccheck.py` takes the donor's sibling-relative TestKit default, and `SMRTK.md`/`TESTKIT.md` are byte copies of the donor. The fork's doccheck now runs the TestKit probe count, parse and tree legs; both DRIFT lines are gone. `RECHECK` on six adapted tools remains, and it belongs to the full knowledge sync pass, not the move. | fork `4a5fd9b` |
| 4 | **Fixed**: the three lines; 0 old-root hits remain in the repo. | `SMR-CommunitySaveRescue` `5d653a1` |
| 5 | **Accepted, no loss.** The old store's directory changed at 12:38 on 09-21; the actor is unknown. The new store holds exactly eight memory files, matching the eight missing from the old one, so the content survives there. Only the untouched witness copy is gone, and it cannot be restored. | — |
| 6 | **Accepted.** The first-pass report declared both edits, and each is a correct path change. Nothing is to be undone. | — |

The deletion verdicts stay the owner's call.
