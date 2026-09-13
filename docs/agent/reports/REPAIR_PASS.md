# Repair pass - groups A and B landed; group C stopped

2026-09-13 - implementor Codex - baseline `2f732c1` - no push or release.
Adjudication belongs to a different session. The executable brief remains at
`docs/agent/prompts/REPAIR_PASS.md` because its deletion/grave is explicitly the
commit landing group C, which did not land.

## Not done, and why

- **Group C as a whole:** stopped before any Group C write under the brief's
  sections 5/8 rule: a defect in sections 2-4 that does not reproduce requires stopping.
  C2 says the pilot's live payload still directs a boot/prototype and its
  removal awaits the owner. The file is absent; `cf8d51f` removed it on the
  owner's word before this pass. This refutation depends on that deletion
  remaining in the tree. No pilot was recreated or removed by this pass.
- **C1:** the mandatory marker-update sentence was not homed in WORKFLOW.
- **C2:** no retirement banners or route edits were made, including in ignored
  `.claude/IMPLEMENT_PROMPT.md` and `.claude/PLAN_TODO.md`. The report's affirmative
  pilot routes and the handoff's stale removal recommendation remain.
- **C3:** the shipped comment wording and wrap defects remain.
- **Brief consumption:** no prompt deletion or prompt-map status change.
- **Owner choices:** no marker semantics, checklist/entry status changes,
  ck170 accounting/reading-route choices, archival apply, or CLAUDE edits.
- **Attended checks:** no game boot, Lua runtime change, packing or upload.
  Separate-session adjudication has not happened.

## Anchor and emitted results

Commands: `git status -sb`, `git log --oneline -1`,
`python tools/doccheck.py --emit-fingerprint`,
`python tools/flpk_extract.py --selftest`, `python tools/pack_predict.py .`.
Baseline branch line: `## main...origin/main`; baseline working tree was clean.
Baseline and final verdicts, captured directly:

```text
before: doccheck: GREEN
after: doccheck: GREEN
```

Baseline had no MARKER INTEGRITY line. Final warning and all locations:

```text
MARKER INTEGRITY: 46 on disk, 45 parsed; WARN; RED only after an owner ruling adopts vocabulary and uniqueness enforcement
  warn line 73: unparsed <!-- ck:169 status:part-ruled owner:yes -->
  warn line 73: unknown status part-ruled
  warn duplicate ck:144 at lines 2257, 2331
  warn duplicate ck:169 at lines 73, 111
```

Fingerprint output before (`2f732c1`) verbatim:

```text
FINGERPRINTS — derived_at across 93 facts; installed game build 24995074
  game 1.0.7.396349               55 fact(s) (54 inferred)  MOVED — installed is 24995074, so these line citations describe a tree that is not on disk (1.0.7 archived, EF-083)
  game 1.1.0 build 24995074       18 fact(s) (16 inferred)  HOLDS — this IS the installed build; no re-read needed
  repo shas (11 distinct)         20 fact(s) (20 inferred)  all behind HEAD by 123–1199 commits — re-check before quoting
      08e47d4+1199  aa7150e+751  55b1d5e+379  ce4d972+1000  e8c31b3+1075  349a81b+123  7355f70+763  82add71+628  8908367+708  a0c75bc+733  f4e5409+203
  → a group that HOLDS needs no re-read; re-derive only what moved.
```

Fingerprint output after the repair commits (validation HEAD `b74a84f`) verbatim:

```text
FINGERPRINTS — derived_at across 93 facts; installed game build 24995074
  game 1.0.7.396349               55 fact(s) (54 inferred)  MOVED — installed is 24995074, so these line citations describe a tree that is not on disk (1.0.7 archived, EF-083)
  game 1.1.0 build 24995074       18 fact(s) (16 inferred)  HOLDS — build identity matches; routing aid only, check claim scope and source dependencies
  repo shas (11 distinct)         20 fact(s) (20 inferred)  all behind HEAD by 126–1202 commits — re-check before quoting
      08e47d4+1202  aa7150e+754  55b1d5e+382  ce4d972+1003  e8c31b3+1078  349a81b+126  7355f70+766  82add71+631  8908367+711  a0c75bc+736  f4e5409+206
  → route by build identity; HOLDS does not verify claims, scope or source dependencies.
```

Pack prediction, emitted via `--json` (baseline predictor reconstructed from
`git show 2f732c1:tools/pack_predict.py` against the unchanged packed paths):

```text
before count: 52
after count: 51
removed: [".rgignore"]
added: []
```

Only `.rgignore` left the predicted set; no packed path was added.
`git diff 2f732c1..03fc504 -- Code/` is empty. metadata.lua's B diff also adds
its previously absent final newline; no Lua logic changed.

Commits and diff-stats (`git show --stat --oneline <sha>`):

```text
424075c Report checklist marker integrity and compare fingerprint builds exactly
 tools/doccheck.py             |  59 ++++++++++++++++++++----
 tools/repair_pass_selftest.py | 101 ++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 151 insertions(+), 9 deletions(-)

03fc504 Exclude .rgignore from player packs and gate ignore-list parity
 metadata.lua                  |  3 ++-
 tools/doccheck.py             | 37 ++++++++++++++++++++++++++
 tools/pack_predict.py         |  1 +
 tools/repair_pass_selftest.py | 60 +++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 100 insertions(+), 1 deletion(-)
```

Final counts (`python tools/doccheck.py --emit-counts`):

```text
BUILD STATE (emitted by tools/doccheck.py)
- modules: 46 registered (46 default-active, 0 optional-gated files)
- Code/*.lua files: 47
- TestKit probes: 97
- BUGS index rows: 119 F + 13 D + 93 C
```

Existing budget warnings, verbatim (outside this pass's lane):

```text
    smr-bug-library           3685 B  ⚠ over the 3072 B target
    smr-orientation           3312 B  ⚠ over the 3072 B target
PUSH SET: 42199 B in 5 file(s) ≈ 19k tokens (budget 40960 B)  ⚠ OVER
```

## Per-defect adjudication trail

### A1 - silent marker loss, unused vocabulary, duplicate identifiers

**SOURCE / reproduced.** Baseline MARKER_RE only accepts `[a-z]+` statuses;
MARKER_STATUSES had only its definition reference. The live `part-ruled` comment
fails the parser; both ck144 and ck169 occur on multiple lines. Detection now
scans checklist comments independently, reports disk/parsed counts, malformed
comments, unknown status words using MARKER_STATUSES, and duplicate numeric IDs
with every location. `ck:-` remains an unnumbered marker and is not a duplicate
numeric ID. The old MARKER_RE and register selection stay unchanged; the WAITING
output and generated register remained byte-identical.

This is **WARN**, with the owner's future vocabulary/uniqueness ruling named in
the output and code comment. No policy was chosen and no checklist marker changed.

Proof commands:

```text
python tools/repair_pass_selftest.py
python tools/doccheck.py
```

The durable harness exercises malformed IDs, hyphenated/unrecognised statuses,
and duplicates, with a valid marker as control. A scratch copy reverting
integrity reporting to its previous silence passes the no-warning control and
fails each demand separately. The live checker stays GREEN while emitting WARN.

### A2 - substring fingerprint identity

**SOURCE / reproduced.** The baseline `elif build in bare` accepts the installed
prefix ID against the longer pinned ID. Now the decimal ID following `build` is
parsed and compared exactly. The MOVED wording is unchanged. HOLDS, the function
header and closing line now describe routing by identity, with explicit limits
on claim scope and source dependencies.

Proof: `python tools/repair_pass_selftest.py` runs exact-ID and unreadable controls,
prefix and longer-ID demands, and the entire check again after restoring the
scratch source. Reverting the comparison to `build in bare` passes the exact
control and fails the prefix demand. Final routing: `python tools/doccheck.py
--emit-fingerprint` (quoted above).

### A3 - dead prose_defer

**SOURCE / reproduced.** `rg -n prose_defer tools/doccheck.py` at the baseline
finds only the flag assignment; it has no consumer. Removed the assignment.
The unrelated prose parsing and classification were retained. Captured baseline
and Group A checker output were compared after excluding only A1's new diagnostic
lines and A2's intentionally rewritten HOLDS/closing lines; every remaining line
was identical. The WAITING result did not change. Final absence command:
`rg -n prose_defer tools/doccheck.py` (exit 1 / no matches).

### B1 - .rgignore in the predicted player pack

**SOURCE / reproduced.** Initial pack output lists `.rgignore` as a root file.
Added `*.rgignore` beside `*.gitignore` in both metadata.lua and the prediction
mirror. Before editing, a Python line scan emitted comment totals independently
for metadata.lua and items.lua; both were nonzero, so no upload restore was owed.
Commands: `python tools/pack_predict.py . --json`,
`python -c "from luaparser import ast; from pathlib import Path;
ast.parse(Path('metadata.lua').read_text(encoding='utf-8-sig'))"`,
`git diff 2f732c1..03fc504 -- Code/`.
Pack membership is compared as sets as well as totals (emitted above).

### B2 - duplicated pack filters without a parity gate

**SOURCE / reproduced.** No parity gate existed. Added PACK IGNORE PARITY to the
normal doccheck boolean chain. It parses literal shipped filter strings and the
predictor's AST IGNORE assignment without executing either file, checks string
list shape and exact order, and emits RED on disagreement or unreadable/malformed
input. Unlike A1, this is a hard gate: filter drift changes player downloads.

Proof command: `python tools/repair_pass_selftest.py`. It copies the actual lists
to a temporary root, exercises a matching control, removes `.rgignore` on one
side, swaps the first two filters, restores exact bytes and verifies SHA256.
A second scratch mutant replacing the gate with an always-PASS result passes the
control but fails the drift demand. Then the entire repaired harness runs again.

A full CLI falsifier also copied the checkout to a temporary snapshot, excluding
only `.git` and `__pycache__`; the live checkout was never drifted. The command
below is the reproducible version of that run:

```python
from pathlib import Path
import hashlib, shutil, subprocess, sys, tempfile
root = Path.cwd()
with tempfile.TemporaryDirectory(prefix="smr-repair-cli-") as directory:
    snapshot = Path(directory) / "snapshot"
    assert snapshot.resolve().parent == Path(directory).resolve()
    shutil.copytree(root, snapshot,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    predictor = snapshot / "tools/pack_predict.py"
    original = predictor.read_bytes()
    def check():
        return subprocess.run([sys.executable, str(snapshot / "tools/doccheck.py")],
                              cwd=snapshot, capture_output=True)
    assert check().returncode == 0
    drift = original.replace(b'    "*.rgignore",\n', b"").replace(
        b'    "*.rgignore",\r\n', b"")
    assert drift != original
    predictor.write_bytes(drift)
    broken = check()
    assert broken.returncode == 1 and b"PACK IGNORE PARITY: RED" in broken.stdout
    predictor.write_bytes(original)
    assert check().returncode == 0 and predictor.read_bytes() == original
    print(hashlib.sha256(predictor.read_bytes()).hexdigest())
```

Full CLI transcript:

```text
CONTROL exit=0
PACK IGNORE PARITY: PASS — 15 filters agree in order
doccheck: GREEN
DRIFT exit=1
PACK IGNORE PARITY: RED — metadata.lua ignore_files and pack_predict.py IGNORE differ in membership or order
doccheck: RED
RESTORED exit=0
PACK IGNORE PARITY: PASS — 15 filters agree in order
doccheck: GREEN
RESTORED pack_predict.py SHA256 694167d7d7688e3d8b25721d351c7f3ba7deefe4d3608066798edb546af38876
```

### C1 - marker obligation lacks its authoring home

**SOURCE / reproduced, unrepaired.** `rg -n --glob '*.md' 'updating its marker'
docs/agent` enumerates an audit query, this brief, and HANDOFF_ORCHESTRATOR section 4;
it finds no WORKFLOW instruction. The affirmative obligation remains only in
that handoff (the audit/brief describe the gap). Its sentence reads:
**changing an item's status ALSO means updating its marker**. No new-home quote
is available because group C did not land.

### C2 - retired executable prompts and firing routes

**SOURCE / partially refuted; stop triggered.**

- `Test-Path docs/agent/prompts/SELFCHECK_PILOT.md` emits False;
  `git log --diff-filter=D --oneline -- docs/agent/prompts/SELFCHECK_PILOT.md`
  identifies `cf8d51f`. The brief's live-payload and awaiting-removal premise is
  stale. STATE and the prompt map already record the owner's removal.
- `rg --files --hidden --no-ignore -g '*IMPLEMENT_PROMPT.md' -g '*PLAN_TODO.md'
  -g '*SELFCHECK_PILOT.md' -g '!.git/**'` locates the ignored files under
  **.claude/**, not docs/agent/prompts/. `git check-ignore` confirms both are
  ignored. IMPLEMENT opens with **Fire with** and has no retirement banner;
  PLAN_TODO still says **Fire .claude/IMPLEMENT_PROMPT.md**. Its historical
  four-errors narrative was found, but the four old implementation claims were
  not independently re-audited in this pass.
- `rg -n -B5 -A6 SELFCHECK_PILOT
  docs/agent/reports/SELFCHECK_PROMISE_COMBINED.md` finds affirmative pilot routes
  in precondition C, section 6's exact-chunks instruction and the continuation reference.
- HANDOFF_ORCHESTRATOR opens with a shipped/no-launch notice and says its removal
  condition is met, but continues to carry the sole-home marker obligation and
  the stale **removal recommended, not done** pilot row. It remains actionable.

No C2 change was made after the refuted premise was verified.

### C3 - shipped comment grammar, consistency and wrap

**SOURCE / reproduced, unrepaired.** Exact affected comments and emitted lengths:

```text
metadata.lua:159 (136 chars): -- to their accurate versions"); text-only, no behaviour, and `editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)` as
metadata.lua:180 (134 chars): -- behaviour, and editor/version rail (agent/prompts/perma/RELEASE.md § Release rails) leaves the version bump to the upload sitting.
items.lua:203 (136 chars): -- above and module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py): a module absent from this file SHIPS ABSENT.
```

The metadata subject/verb interruption and inconsistent backticks are present;
the items comment also exceeds nearby wrapping. The referenced RELEASE.md and
its Release rails heading exist. No comment was rewritten because C stopped.

## Scratch proof transcript

`python tools/repair_pass_selftest.py` after group B, verbatim:

```text
PASS A1/A2 controls and all demands on repaired copy
PASS A1 reverted scratch demand 0: control passes, demand FAILS
PASS A1 reverted scratch demand 1: control passes, demand FAILS
PASS A1 reverted scratch demand 2: control passes, demand FAILS
PASS A1 reverted scratch demand 3: control passes, demand FAILS
PASS A2 reverted scratch: exact control passes, prefix demand FAILS
CONTROL PACK IGNORE PARITY: PASS — 15 filters agree in order
MEMBERSHIP PACK IGNORE PARITY: RED — metadata.lua ignore_files and pack_predict.py IGNORE differ in membership or order
ORDER PACK IGNORE PARITY: RED — metadata.lua ignore_files and pack_predict.py IGNORE differ in membership or order
RESTORED PACK IGNORE PARITY: PASS — 15 filters agree in order
RESTORED metadata.lua SHA256 2ee8af9d4df520ddefedd4d6d2b1722a2d96e9692deef57911cadb40dc18bcf2
RESTORED pack_predict.py SHA256 694167d7d7688e3d8b25721d351c7f3ba7deefe4d3608066798edb546af38876
CONTROL PACK IGNORE PARITY: PASS (mutant)
PASS B2 reverted scratch: control passes, drift demand FAILS
CONTROL PACK IGNORE PARITY: PASS — 15 filters agree in order
MEMBERSHIP PACK IGNORE PARITY: RED — metadata.lua ignore_files and pack_predict.py IGNORE differ in membership or order
ORDER PACK IGNORE PARITY: RED — metadata.lua ignore_files and pack_predict.py IGNORE differ in membership or order
RESTORED PACK IGNORE PARITY: PASS — 15 filters agree in order
RESTORED metadata.lua SHA256 2ee8af9d4df520ddefedd4d6d2b1722a2d96e9692deef57911cadb40dc18bcf2
RESTORED pack_predict.py SHA256 694167d7d7688e3d8b25721d351c7f3ba7deefe4d3608066798edb546af38876
RESTORED doccheck.py SHA256 516f4e33efd1a6091751bd8fe574b7abcee9602e4529620ac32ab6acb3afa3a7
```

The SHA256 for restored doccheck is over the UTF-8 scratch source (normalised
newlines on read); copied metadata/predictor hashes are over restored raw bytes.
The harness initially caught a CRLF-vs-LF scratch hash mismatch; byte writes fixed
that harness issue, after which controls, mutants, demands and restores all pass.

## Shared-tree close-out

The only foreign working-tree edit observed after group B was
`docs/agent/prompts/C92_ACHIEVEMENT_BUILD.md`; it was left untouched and excluded
from every commit. The peer subsequently committed it as `b74a84f`,
which is the final validation HEAD here. Each repair commit names exact owned paths. No archive file,
CLAUDE/AGENTS source or mirror, checklist marker, bug status, or game file changed.
All load-bearing results of this stopped pass are recorded here.


## Group C, completed

2026-09-13. Follow-up baseline `cda31de`; Part 1 completed. The corrected
REPAIR_PASS_C stop rule treats a refuted item as a finding to skip while
continuing independent repairs. The initial report above remains historical;
this section supersedes its Group C completion state.

### Item 1 - marker obligation: reproduced and repaired

Claim: the status-change/marker-update rule had no canonical authoring home.
`rg -n --glob '*.md' 'updating its marker' docs/agent` found the affirmative
instruction only in the retired handoff, with audit/brief descriptions elsewhere.
Now WORKFLOW rule 5, beside owner-decision mirroring, says:

> **Changing an item's status ALSO means updating its marker.** Update the

Its next lines require the marker and owner-action field to change in the same
edit and route regeneration to WORKFLOW's shared-tree section. The handoff's
old sole-home claim, copied generation instructions and recorded coverage counts
were replaced with the canonical pointer. Final lookup:
`rg -n 'updating its marker' docs/agent/WORKFLOW.md`.

### Item 2 - ignored implementation prompt: reproduced and repaired

Claim: `.claude/IMPLEMENT_PROMPT.md` still opens with a live firing route and
has no spent banner. Direct read confirmed both. Its opening now says
**SPENT - DO NOT FIRE (2026-09-13)** above **Historical firing route (disabled)**;
the executable `task` line and **Fire with** label were removed. Historical
instructions remain as a record. `git check-ignore .claude/IMPLEMENT_PROMPT.md`
confirms it is ignored: this edit exists on disk and is intentionally not in
any commit. A Python opening-line check confirms SPENT precedes the historical
route and the old firing label is absent. The historical four-error narrative
was not re-audited; only the executable-entry defect was repaired.

### Item 3 - handoff pilot claim and retirement residue: reproduced and repaired

Claim: HANDOFF_ORCHESTRATOR still recommends a removal that already happened.
`Test-Path docs/agent/prompts/SELFCHECK_PILOT.md` is False and
`git log --diff-filter=D --oneline -- docs/agent/prompts/SELFCHECK_PILOT.md`
identifies `cf8d51f`. Its retained row now reads:

> **`prompts/SELFCHECK_PILOT.md`** - **REMOVED 2026-09-13 on the owner's word, `cf8d51f`.**

The pilot's supposed live payload is refuted and was skipped. No pilot was
recreated. The handoff has a **RETIRED - DO NOT FIRE** banner at its executable
entry, routes current work to DISPATCH and the generated owner queue, and no
longer asks the owner to schedule its deletion as another task. Its remaining
content is explicitly a retained snapshot. The prompt map carries the same
retirement route. Unique retained notes and the archive-citation warning remain;
file removal is still the owner's call.

### Item 4 - shipped comment grammar and wrapping: reproduced and repaired

Claim: the metadata subject/verb interruption, inconsistent backticks and
items.lua module-list comment exceeded surrounding wrapping. Direct reads
confirmed each. Both metadata comments now use the consistent short reference
`RELEASE.md` with its Release rails section, with the full resolving path beside
the first use. The subject/verb grammar is repaired, and the items gate citation
wraps across comment lines without changing its meaning. New reference lines:

```text
metadata.lua:73: -- ⭐ 2026-09-10, v7 words (`RELEASE.md` step 1): count word Forty-six → FORTY-EIGHT
metadata.lua:81: -- ⭐ 2026-09-12 for v10 (`RELEASE.md` step 1 over the outbox's Held + 3 Pending):
metadata.lua:160: -- rail (`RELEASE.md § Release rails`), reworded 2026-08-24, puts hand edits
metadata.lua:162: -- owner's sitting. Reference: docs/agent/prompts/perma/RELEASE.md.
metadata.lua:181: -- behaviour. The editor/version rail (`RELEASE.md § Release rails`) leaves
metadata.lua:211: -- ⭐ REWRITTEN WHOLESALE 2026-09-10 for v7 (`RELEASE.md` step 1, from `RELEASE_OUTBOX.md`).
metadata.lua:221: -- (`RELEASE.md` step 1, from `RELEASE_OUTBOX.md`): the F59 repair, named as the pack's OWN
metadata.lua:226: -- ⭐ REWRITTEN 2026-09-12 for v10 (`RELEASE.md` step 1, from `RELEASE_OUTBOX.md`'s three
metadata.lua:304: -- restored by merge the same night (v8 close-out inside the `RELEASE.md` run for v9).
items.lua:203: -- above and the module-list gate (tools/doccheck.py MODULE SETS +
items.lua:204: -- tools/upload_preflight.py): a module absent from this file SHIPS ABSENT.
```

Before writing, independent comment scans emitted nonzero totals for both Lua
files, so no POST_UPLOAD_CLOSE restore was owed. Verification compared Lua lexer
default-channel tokens to `git show cda31de:<file>` and parsed both edited files
with luaparser: executable tokens are identical and syntax passes. Every added
Lua line is a comment within the requested wrap. The referenced RELEASE.md and
its `## Release rails` heading exist. `git diff cda31de -- Code/` is empty.

### Marker output and checks

`python tools/doccheck.py --emit-counts` before Part 1, verbatim:

```text
MARKER INTEGRITY: 46 on disk, 45 parsed; WARN; RED only after an owner ruling adopts vocabulary and uniqueness enforcement
  warn line 73: unparsed <!-- ck:169 status:part-ruled owner:yes -->
  warn line 73: unknown status part-ruled
  warn duplicate ck:144 at lines 2257, 2331
  warn duplicate ck:169 at lines 73, 111
```

After Part 1, verbatim (unchanged, as required while 170(a) is open):

```text
MARKER INTEGRITY: 46 on disk, 45 parsed; WARN; RED only after an owner ruling adopts vocabulary and uniqueness enforcement
  warn line 73: unparsed <!-- ck:169 status:part-ruled owner:yes -->
  warn line 73: unknown status part-ruled
  warn duplicate ck:144 at lines 2257, 2331
  warn duplicate ck:169 at lines 73, 111
```

Checker verdict: `doccheck: GREEN`; `git diff --check` passes. No gate or
threshold was added in Part 1, so no new gate falsifier is required. Part 1
repairs delete no file. Brief deletion is a separate consumed-prompt close-out.

Emitted counts:

```text
BUILD STATE (emitted by tools/doccheck.py)
- modules: 46 registered (46 default-active, 0 optional-gated files)
- Code/*.lua files: 47
- TestKit probes: 97
- BUGS index rows: 119 F + 13 D + 93 C
```

Existing budget warnings, verbatim:

```text
    smr-bug-library           3685 B  ⚠ over the 3072 B target
    smr-orientation           3312 B  ⚠ over the 3072 B target
PUSH SET: 42199 B in 5 file(s) ≈ 19k tokens (budget 40960 B)  ⚠ OVER
```

### Not done and why

- **Part 2:** checklist 170(a) is still open. Its marker is
  `<!-- ck:170 status:open owner:yes -->` and its body still asks the owner to
  choose the vocabulary. Command: `rg -n -A10 'ck:170'
  docs/PLAYTEST_CHECKLIST.md`. No marker, duplicate rule, vocabulary enforcement,
  checker threshold or checklist/entry status changed. The on-disk/parsed gap
  remains visible until a ruling authorizes reconciliation.
- **Pilot:** already removed in `cf8d51f`; the live-payload claim was refuted,
  recorded and skipped rather than halting the group.
- **HANDOFF_ORCHESTRATOR deletion:** not authorized by this follow-up; retained
  with the explicit retirement banner and canonical routes.
- **Other historical routes:** the combined self-check report was outside this
  follow-up's enumerated Part 1 edits and retains its historical pilot references.
  PLAN_TODO was observed changing to HISTORY ONLY during review; it was not edited.
  Its remaining call to IMPLEMENT reaches the now-spent executable entry.
- **Ignored-file distribution:** IMPLEMENT_PROMPT is repaired locally; ignored
  material is deliberately not force-added to Git.
- **Attended or external actions:** no boot, runtime test, pack, upload, portal
  call or push. Independent adjudication remains a different session's work.

Commit identity and diff-stats are recorded in the consumed-prompt close-out
below, after the Part 1 commit exists. All load-bearing findings are on disk.


### Group C commit and consumed-prompt close-out

Part 1 landed in `9e4691d` with the following emitted diff-stat:

```text
9e4691d Complete repair-pass C authoring and retirement repairs
 docs/agent/WORKFLOW.md                           |   5 +
 docs/agent/prompts/README.md                     |   2 +-
 docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md |  26 ++--
 docs/agent/reports/REPAIR_PASS.md                | 150 +++++++++++++++++++++++
 items.lua                                        |   3 +-
 metadata.lua                                     |  10 +-
 6 files changed, 175 insertions(+), 21 deletions(-)
```

The separate close-out consumes only `prompts/REPAIR_PASS.md` and
`prompts/REPAIR_PASS_C.md`, as both executable briefs instruct, and updates
`prompts/README.md` to their fired outcomes. The retired handoff and ignored
implementation record remain on disk. The Part 1 no-deletion condition was
satisfied before this administrative close-out.

Part 2's deferred proposal and verification recipe are preserved in Git:
`git show cda31de:docs/agent/prompts/REPAIR_PASS_C.md`, section 3. Only the
owner-adopted choices may be implemented; the open 170(a) call was not answered
by this pass. Marker diagnostics remain unchanged and checker validation is
`doccheck: GREEN`. The close-out commit is discoverable with
`git log -1 --oneline -- docs/agent/prompts/REPAIR_PASS_C.md`.
