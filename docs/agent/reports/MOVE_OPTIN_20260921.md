# The opt-in pack and its assets moved to `B:\Dev\SMR` — first pass

Doc orchestrator, 2026-09-21, from `MOVE_OPTIN_high.md` (`fa2c2ca`), fired at fix pack `26b86e7`.
**One audit grades the whole move** (`MOVE_AUDIT_high.md`); this report is only the witness of the
moment, because by audit time these trees will have been worked in.

```
C:\Dev\SMR-OptInPack   ->  B:\Dev\SMR\SMR-OptInPack     copied, verified, original renamed
C:\Dev\SMR-Assets      ->  B:\Dev\SMR\SMR-Assets        copied, verified, original renamed
```

⛔ **Nothing was deleted.** The originals are `C:\Dev\SMR-OptInPack__MOVED_20260921` and
`C:\Dev\SMR-Assets__MOVED_20260921`, in place and untouched. **The owner deletes them after the
whole-move audit passes** — not this session, and not the train seat.

---

## 1 · Proof of an intact copy

Captured by one script run identically on both sides (`capture.sh`); the two outputs were diffed and
were **identical on every field except the root path**, for both trees.

| | `SMR-OptInPack` | `SMR-Assets` |
|---|---|---|
| files (incl. `.git`) | 3572 | 441 |
| files (excl. `.git`) | 315 | 217 |
| directories | 388 | 166 |
| bytes (incl. `.git`) | 99,902,680 | 504,509,686 |
| HEAD | `456a9401d4c48ebaf28252ea3d687fb65889ad5c` | `41890eb0496ecb3fb3d02adeacf6521ceb1f84b8` |
| branch | `main` | `main` |
| `git fsck` | exit 0, dangling objects only | exit 0, dangling objects only |
| `git status --porcelain` | 0 entries | 0 entries |
| remotes | `origin` → `SMR-CommunityOptInPack.git` | ⚠️ **none** |
| tags | 5, all resolving to identical commits | 5, all resolving to identical commits |
| working-tree sha256 | `344501d9…a5e1` | `7030b544…ccb1` |
| `.git` sha256 | `d482c652…54d6` | `cd75f04c…4ce8` |

The last two rows are a sha256 over the sha256 of every file, sorted — so a single changed byte
anywhere in either tree would have produced a different digest. Both matched.

Named tags required by the brief resolve on both sides: `hub-model-final-untextured`,
`hub-centre-lights-20260921`.

Copy method: `robocopy /MIR /COPY:DAT /DCOPY:DAT /XJ`, exit 1 (its success code), 0 FAILED and 0
Mismatch on both trees. Verified independently of robocopy's own summary by the table above.
Neither tree contains a symlink or junction, and `B:` is NTFS with 1.32 TB free, so the copy had
nothing to flatten.

### Two findings about the state of these repos

- ⚠️ **`SMR-Assets` has no git remote at all.** 504 MB, 441 files, five tags, existing **only on this
  disk**. The `__MOVED_` original is currently its only redundancy. Worth a remote before the
  originals are deleted.
- `SMR-OptInPack` is **4 commits ahead of `origin/main`** and unpushed (3 of them the train seat's,
  1 mine). Left unpushed deliberately: publishing another seat's commits is not mine to do.

### The dirty set the brief expected no longer existed

End state 2 anticipated the train seat's in-progress files staying dirty, to be listed with a sha256
each. **They were committed during this session instead**, so there was nothing to list and the copy
was taken from a clean tree — a better starting point than the brief assumed. Observed directly:
`baaefd1` at 10:32 (the inventory), then `60bee7c` at 11:27 ("the owner's first concept import") and
`456a940` at 11:30 ("Handoff: the gate is lifted, the move is next"), the last of which committed the
five `tools/devmods/train_hub/` files that had been dirty. Both `smr-optinpack-*` sessions had exited
by 11:33, so no session was rooted in either tree while it moved.

---

## 2 · The inventory, re-derived today

Re-run of the exact grep `MOVE_PATH_INVENTORY_20260921.md` (`baaefd1`) records, over both trees:

| class | recorded | today | moved? |
|---|---|---|---|
| editor-held | 5 | **5** | no |
| scripts | 29 | **29** (25 `.py` + 4 `.lua`) | no |
| config | 13 | **13** | no |
| prose | 134 | **136** | **+2** |
| total | 181 | **183** | +2 |

**The +2 is the inventory document itself**, which contains two `C:\Dev` references and was written in
the same commit the count was taken in — the count was taken just before the file existed. Every
other class reconciles exactly against its named members. Nothing else moved.

### The number that actually mattered is 63, not 183

Of the 183, only **63 name the two trees that moved** (`SMR-Assets` 39, `SMR-OptInPack` 24). The
other **120 name trees that stay on `C:` this pass** — `SMR-SrcArchive` (45), `SMR-BugFixPack` (32),
`SMR-BugFixPack-TestKit` (25), and others — and are still correct. Rewriting them, as a literal
reading of "the 134 prose references" would have done, would have pointed 120 correct references at
nothing.

---

## 3 · What was repointed, and what remains

**46 repointed in the moved trees** — 32 prose, 10 script lines, 4 config keys. Applied by a script
carrying a per-file expected count, so a drifted file fails loudly instead of being half-edited;
every file matched. A second such run in the fix pack caught a real drift (below).

Reconciling those 46 against the commits, because they do not add up on their face:

| | count | how to re-derive |
|---|---|---|
| substitutions written | 46 | the two script runs' own totals |
| of those, in **git-ignored** files | 5 | `.claude/settings.json` (2), `.claude/agents/doc-surgeon.md` (1), `local/retired-modules/README.md` (2) — on disk, no commit |
| therefore tracked | 41 | `C:` occurrences removed by `f2ec95d` (28) + `9f2c201` (13) |
| `B:` occurrences added | 39 | 2 fewer, because `hub_oracle.py`'s three literal paths collapsed into one `_TRAIN_ASSETS` line feeding three `os.path.join` calls |

**17 remain in the moved trees, by class:**

| # | what | why it stays | whose |
|---|---|---|---|
| 5 | `SourceData/GFXMaterial` (4) + `SourceData/SIE_ImportItem` (1) | editor-held; the Importer reasserts them over a drag | **train orchestrator** |
| 1 | `tools/devmods/train_hub/tests/traffic_smoke.py` | inside `tools/devmods/**` | **train orchestrator** |
| 4 | 3 Blender proof JSONs + `_before_claude_pass2_20260918/README.md` | evidence of a past run, not configuration | nobody — keep |
| 6 | `TRAIN_HUB_BUILD_20260918.md` (3), `READINESS_REVIEW_0831.md`, `TRAIN_HUB_SITTING_20260919.md`, `TRAIN_LOGISTICS_DESIGN` §1027 | records of commands that ran, and results produced, at a path that was true then | nobody — keep |
| 1 | `TRAIN_HUB_MODEL_high.md:152` | see below | **owner** |

The rule used inside the moved trees: **repoint a path a reader must follow to something that still
exists and is still used; leave a path that records what a past run did.**

⛔ **`TRAIN_HUB_MODEL_high.md:152` was left alone on purpose.** It says the old assets path "is
already a junction to `C:\Dev\SMR-Assets\trainhub`", but `SMR-Assets/README.md` records that junction
as **deleted on 2026-09-21**. The sentence was already false before this move. Repointing it would
have laundered a false claim into looking current, so it is flagged rather than edited — it needs
rewriting or deleting, which is a content decision, not a move.

### The fix pack

**38 live pointers repointed**, under the narrower rule the brief sets for this repo: the map's
tombstone forwarding line, `WORKFLOW.md`'s sibling-mods line, `FIX_POLICY.md`, `FUTURE_IDEAS.md`,
`EF-071` (2), the nine `D` tombstones' `moved_to:` front matter and body forwarding line (18), three
live prompts, three live delivery/forwarding reports, `tools/patchcheck.py`'s usage example,
`items.lua`'s comment, and `.claude/HANDOFF_PROMPT.md`'s three (two of them runnable `git -C` lines).

Records were left as records: dated reports, `_before`/`BEFORE` snapshots, the A/B evidence
artefacts, the decisions log, `mkmarkers.py`'s dated comment. `MOVE_AUDIT_high.md`'s references to
the `__MOVED_` originals are correct as written and untouched.

Same reconciliation as above: of those 38, **3 are in `.claude/HANDOFF_PROMPT.md`, which is
git-ignored here too** — on disk, carrying no commit. So `411fdf0` adds 35 `B:` occurrences and
removes 37 `C:` ones; the extra 2 removed are the move table inside `MOVE_OPTIN_high.md`, deleted
with the file. A count of `B:\Dev\SMR` across this repo reads 7 higher than 38 because
`.claude/DECISIONS.md` (5) and two further lines in `.claude/HANDOFF_PROMPT.md` were written by the
sessions that authored the move briefs, not by this pass.

- `moved_to:` is **not read by `doccheck.py`** (checked), so repointing it is informational only.
- `EF-071.md` is **mirrored between the two repos**; both copies were repointed and remain
  byte-identical (`22aa9e1b…`), so `sync_from_fixpack.py` still sees parity.
- The fix pack's **"Outside the repo" block needs no change this pass** — it lists only
  `SMR-BugFixPack-TestKit`, `SMR-SrcArchive`, `workshop_fpk_archive`, `SMR-ScreenCaptures` and the
  three FR-1 folders, all still on `C:`. It never named the two sibling repos. (`SMR-Assets` is
  arguably shared material that belongs in that block; that is a content call, not a move.)
- One guard fired: `RELEASE_DESCRIPTION_OPTIN.md` held **2** references where 1 was expected. The
  second is a dated `--emit-counts` measurement from 2026-08-14 with its result — a record. The file
  was left unwritten by the script and the live line edited by hand.

---

## 4 · The environment variables

⚠️ **Measured, not assumed: none of the five variables is set on this machine, in user or process
scope.** Every script has therefore been resolving through its **in-code default**, which is why
repointing those defaults was the load-bearing change and this block is a belt, not the braces.

```bat
setx SMR_TESTKIT     "C:\Dev\SMR-BugFixPack-TestKit"
setx SMR_FIXPACK     "C:\Dev\SMR-BugFixPack"
setx SMR_SRCARCHIVE  "C:\Dev\SMR-SrcArchive"
setx SMR_TRAINASSETS "B:\Dev\SMR\SMR-Assets\trainhub"
setx SMR_OPTINPACK   "B:\Dev\SMR\SMR-OptInPack"
```

`setx` writes user scope and affects **new** processes only — existing terminals keep the old value.

- **`SMR_TRAINASSETS` points at the `trainhub` subfolder, not the repo root.** The brief says "the new
  assets root", but its only consumer (`sync_from_fixpack.py:385`) indexes it as a citation-resolution
  root and its default has always been `…\SMR-Assets\trainhub`. A move pass changes locations, not
  semantics, so the value above preserves the existing meaning exactly. Widening it to
  `B:\Dev\SMR\SMR-Assets` would make more citations resolve and may well be right — it is a separate
  decision, not a move.
- **`SMR_OPTINPACK` is new.** Two `SMR-Assets` scripts reach across into the opt-in pack;
  extending the existing pattern was preferable to hard-coding a second absolute path. Its in-code
  default is already correct, so nothing breaks if it is never set.

---

## 5 · The Claude Code memory store

Copied per the owner's added instruction, after the tree copy verified. **Copied, never moved** — the
original stays, like the `__MOVED_` trees, until the audit passes.

```
from  C:\Users\stkot\.claude\projects\c--Dev-SMR-OptInPack     (still present)
to    C:\Users\stkot\.claude\projects\b--Dev-SMR-SMR-OptInPack
```

| | source | destination |
|---|---|---|
| files | 102 | **102** |
| bytes | 187,890,713 | **187,890,713** |
| `memory\MEMORY.md` sha256 | `438766D1…E517` (794 B) | **`438766D1…E517` (794 B)** |

No memory file was edited. Several name `C:\Dev` paths; they are records of what was true.

### ⛔ The destination name is NOT the one the instruction gave

The instruction named `b--Dev-SMR-OptInPack` **and** said the name is *derived, not observed*, giving
the derivation rule and a witness folder. Those two disagree, and the rule wins:

- The rule reproduces the witness exactly: `B:\SteamLibrary\steamapps\workshop\content\1158310\2273832430`
  → `b--SteamLibrary-steamapps-workshop-content-1158310-2273832430`. Confirmed by running it.
- Applied to the tree's **actual** destination, `B:\Dev\SMR\SMR-OptInPack` → **`b--Dev-SMR-SMR-OptInPack`**
  (double `SMR`).
- `b--Dev-SMR-OptInPack` would derive from `B:\Dev\SMR-OptInPack` — the repo sitting directly at
  `B:\Dev`, which is not where it went and would breach "only a REPO may sit at that root".

Neither candidate existed beforehand, so the stop condition did not fire. **The name is confirmed
only when the first session rooted at `B:\Dev\SMR\SMR-OptInPack` loads these memories — that check is
the owner's, not mine.** If it comes up empty, the fix is one rename, and the source is untouched.

---

## 6 · Handover to the train orchestrator

**Your work is released.** The queued glass and themed-reactor imports can now be born with the new
paths.

```
tools/devmods/train_hub      ->  B:\Dev\SMR\SMR-OptInPack\tools\devmods\train_hub
tools/prototypes/train_hub   ->  B:\Dev\SMR\SMR-OptInPack\tools\prototypes\train_hub
SMR-Assets root              ->  B:\Dev\SMR\SMR-Assets
```

All three verified present at those paths. **doccheck is GREEN** in the moved opt-in pack, run from
its new root, with the selftests, `PACK IGNORE PARITY` and the `LOCAL` gate passing; the fix pack is
GREEN too.

**Three of the five mod symlinks are dead as of now** — verified by reading each link's target:

| symlink | state |
|---|---|
| `SMR-OptInPack` | ⛔ dead |
| `SMR-TrainHubDev` | ⛔ dead |
| `SMR-TrainHubPrototype` | ⛔ dead |
| `SMR-BugFixPack` | alive (stays on `C:`) |
| `SMR-BugFixPack-TestKit` | alive (stays on `C:`) |

Until they are recreated, **the opt-in mod and both train hub mods do not exist for the game.**
Recreate from an elevated prompt (`%APPDATA%\Surviving Mars Relaunched\Mods\`):

```bat
rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-OptInPack"
rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-TrainHubDev"
rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-TrainHubPrototype"
mklink /D "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-OptInPack" "B:\Dev\SMR\SMR-OptInPack"
mklink /D "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-TrainHubDev" "B:\Dev\SMR\SMR-OptInPack\tools\devmods\train_hub"
mklink /D "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-TrainHubPrototype" "B:\Dev\SMR\SMR-OptInPack\tools\prototypes\train_hub"
```

**Still yours, and still wrong on disk** — six references I did not touch because they are inside your
boundary:

- `tools/devmods/train_hub/SourceData/GFXMaterial/SMROptInTrainHub6.lua:4-7` — `BaseColor`, `Normal`,
  `RM`, `SI`, all four pointing into `C:\Dev\SMR-Assets\trainhub\blender\textures\concept\`.
- `tools/devmods/train_hub/SourceData/SIE_ImportItem/SMROptInTrainHub6.lua:6` — `ScenePath`, into
  `C:\Dev\SMR-Assets\trainhub\blender\export\concept\`.
- `tools/devmods/train_hub/tests/traffic_smoke.py` — one line naming the moved tree. (Its other
  `C:\Dev` line names `SMR-SrcArchive`, which stays on `C:` and is still correct.)

Repoint the five editor-held paths **with the Mod Editor closed**, then reopen and read the
Importer's header before importing anything. A wrong header there means stop.

**I did edit two files under `tools/devmods/`**, and you should know: `tests/read_leg.json` and
`tests/smoke_leg.json`, `park` key only. End state 4 assigned them to me explicitly, and neither
carries the `DO NOT EDIT MANUALLY` stamp — checked; the 8 stamped files under `tools/devmods/**` and
`tools/prototypes/**` are all editor-generated and none was touched. Their `kit` key still points at
`C:\Dev\SMR-BugFixPack-TestKit`, which is correct: the TestKit stays on `C:` this pass.

---

## 7 · Decisions I made that the brief left to me

- **Copy method**: `robocopy /MIR`, proven by an independent re-capture rather than robocopy's own
  summary. **One commit-and-verify unit per repo**, two in total.
- **`.claude/` moved with the tree** rather than being recreated: `SMR-OptInPack/.claude/settings.json`
  holds the six permission entries end state 4 requires repointing, which only makes sense if it
  travels. It is git-ignored, so those edits — and `.claude/agents/doc-surgeon.md` and
  `local/retired-modules/README.md` — are on disk but carry no commit. Verified present at the new
  root after the copy.
- **The memory store** is covered in §5; the derived-name discrepancy is the one thing in this report
  that most needs the owner's eye.

## 8 · Flagged, not fixed

- `TRAIN_HUB_MODEL_high.md:152` claims a junction that was deleted on 2026-09-21 (§3).
- `SMR-Assets` has **no remote** (§1) and **`core.autocrlf=true` with no `.gitattributes`**, unlike
  `SMR-OptInPack` (`autocrlf=false` + `.gitattributes`). Three of its files are whole-CRLF; my edits
  preserved their endings byte-for-byte (verified against the originals: 99/38/93 CRLF lines before
  and after). Both are pre-existing and out of scope for a move pass.
- `SMR-OptInPack` has 4 unpushed commits; `SMR-Assets` cannot be pushed at all.
- doccheck's own pre-existing warnings are unchanged by this pass: 3 whole-CRLF files under
  `docs/archive/` (append-only, untouched), and 1 uncommitted TestKit change (`Code/80_AgentSlots.lua`,
  report-only, another seat's).

## 9 · Not claimed

**That the move is complete** — `MOVE_AUDIT_high.md` grades it, the symlinks are the train
orchestrator's, and the fix pack, TestKit, game source archive, Workshop corpus and FR-1 folders all
still sit on `C:` by design this pass.

**That no reference to the old path remains** — 17 remain in the moved trees, itemised by class in
§3, of which 6 belong to the train orchestrator. In the fix pack, references in records were left
deliberately and were not counted as debt.

**That the game or the mod works** — nothing here launched the game, the Mod Editor or Blender. Three
mod symlinks are dead until recreated, and no import was run or verified.
