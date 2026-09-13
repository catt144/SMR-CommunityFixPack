# GATE_WIRING — both repairs landed, falsified and restored

Executed 2026-09-13. Two repair commits ⛔ ("independently revertible" is CORRECTED
below — they revert as a pair, B before A):
**`f2b1898`** (A, wire the orphaned falsifiers) and **`a5f7719`** (B, regenerate
STATE's counts). This report and removal of the consumed brief plus its map row
land in a separate close-out commit. No game test or shipped Lua change.

## Anchor and inherited claims

`git pull` returned already up to date at **`5db516f`**; baseline
`python tools/doccheck.py` was GREEN. `git diff --stat 7ca25b9..HEAD -- tools/
docs/agent/STATE.md` was empty. The authored repairs were still applicable.
`git status --short` was re-checked before shared writes and commits; no peer
edits were included.

The scoped `rg` over `tools/` found the two scripts only in their own source
and dependency references, with no caller; `.github/` is absent. The hook has
one Python invocation, `doccheck.py --emit-counts`. The entry-history command
in the brief reproduced **26** distinct commits since 09-01. Isolated selftests
ran in **0.167/0.167 s**; those are not the wired timings below.
The old STATE block said `119 F + 12 D + 92 C`; the baseline instrument emitted
`119 F + 13 D + 93 C`.

## A — required falsifiers

`required_selftest()` runs each script using the current Python interpreter.
Doccheck's normal path, including the existing pre-commit hook, now runs both
`ck170_selftest.py` and `repair_pass_selftest.py`. Each emits its name, verdict
and subprocess duration. Nonzero exit, missing script and execution exception
are RED; failing process output is included. Neither needs a game source tree.

All destructive legs ran in a temporary **disk snapshot**, never this checkout:

| broken copy | observed through full doccheck | restored result |
|---|---|---|
| remove LF normalization from doccheck | `ck170_selftest: RED`, exit 1; doccheck RED | full run GREEN |
| replace exact-build matching with substring matching | `repair_pass_selftest: RED`, exit 1; doccheck RED | full run GREEN |
| replace either selftest with a raising script | named falsifier RED; doccheck RED | originals restored |
| delete either selftest | named falsifier RED, exit 2; doccheck RED | originals restored |

Each failed full run withheld the emitted BUILD STATE block. A simulated
`TimeoutExpired` separately made the runner return false and emit RED.
`ck170_selftest` imports the repair-pass module, so breaking/deleting the latter
also fails ck170; the independent exact-build mutant failed only repair-pass.

After restoring the whole suite, the snapshot was GREEN and these SHA256s
matched the saved originals:

```
doccheck.py                bcf6c59059bdebe363fbc1e9460868a2fe32526b3936e2be7060e1d9e74caec1
ck170_selftest.py          4b807e10f2939156d16c6e71df98b5c2b61eb1b07f665e738c9868f3bf899ecc
repair_pass_selftest.py    d95b8659e9fd46d25a7717665bf55a0662bab8f85e3ddca45f5354d94e69e322
```

The live doccheck hash was also unchanged by the experiment. This proves that
the wired falsifiers reject those regressions; it does not re-adjudicate their
underlying owner rulings.

## B — generated region, regeneration and freshness

`--regen` computes the same `counts_block(recount(...))` used by `--emit-counts`
and replaces only the fenced region's contents. It validates STATE before any
generated-file write. An already fresh STATE is not opened for writing.
The freshness check uses that same renderer and the existing `--regen` cure.
`--regen-waiting` remains the contained checklist-only route.

The stable first line must occur exactly once, immediately after an opening
bare triple-backtick fence. Its closing fence must also be bare. Missing or
duplicate first lines, unbalanced fences, and a region without its own matching
fence pair are refused. Other balanced code blocks are accepted. Both fences,
all surrounding raw bytes and the local LF/CRLF ending are preserved. There
are no added markers. The existing LF-normalized hard/per-line caps are checked
on the rendered candidate; warning thresholds remain unchanged.

**Measured boundedness:** STATE stayed **11,098 raw bytes**. Comparing it with
the saved/pre-repair bytes proves that the only changed bytes are the defect
count line; there is no outside reflow or content edit.

```
pre-repair STATE SHA256    e43ff45d4114360d0bd94f9a47a849fd40ab92bc3812d0ee0379476f7cfe04b3
refreshed STATE SHA256     0c27b62f5fbc389e89eaf6c41b1adeaba7a90c406d9d310410e2e6c50e09939c
```

**Measured idempotence:** `sha256sum` before and after another full `--regen`
returned the refreshed hash above, with raw-byte equality and GREEN doccheck.
A temporary full STATE copy using CRLF also stayed byte-identical after regen
(raw SHA256 `da6f1427d90d11b17a7d21c3cc5a3fbc2a6eb9f6e53ed7502336d24b758fb172`).

**Measured failure:** making the temp STATE count line stale produced
`STATE BUILD STATE: RED`, the regen cure, doccheck RED and withheld counts.
The check did not write the file. Running `--regen` restored GREEN and the saved
STATE hash. Disabling either the replacement return or the regen write made
the new `state_counts_selftest` and full doccheck RED, even though the fixture
STATE itself was fresh. Restoring doccheck restored the full suite to GREEN.

Full snapshot `--regen` runs also refused missing/duplicate markers, a
missing/duplicate fence, total overflow and a 201-byte line. Saved bytes of
STATE, both indices, WAITING, AGENTS and the mirrored skills remained untouched
on each refusal. The final restored full snapshot was GREEN, with hashes:

```
doccheck.py                c86a0288d0c3c32d33af5784a7a26ed0d4bf7bb0f66b9a177358b903a3703440
STATE.md                   0c27b62f5fbc389e89eaf6c41b1adeaba7a90c406d9d310410e2e6c50e09939c
```

The live files matched their saved bytes throughout those experiments.
`state_counts_selftest.py` is itself wired into doccheck: future commits repeat
region, delimiter, cap, idempotence, regen and instrument-mutant checks on
small disk fixtures. It also checks the emitter's existing absent-TestKit text;
probe counts remain derived from the TestKit available on the checking rig.

## Commands and measured cost

Durable regression route: `python tools/doccheck.py --emit-counts`. The three
individual falsifiers can also be run as `python tools/<name>.py`. Idempotence:
run `sha256sum docs/agent/STATE.md`, `python tools/doccheck.py --regen`, then
the same `sha256sum` again; check status for foreign entries before regen.

Local integration drivers are retained at
`C:/Users/stkot/AppData/Local/Temp/gate_wiring_a_verify.py`,
`gate_wiring_b_live_verify.py`, and `gate_wiring_b_verify.py` in that same temp
directory. They recreate snapshots and assert full-process RED/GREEN plus
restore hashes. These drivers are ephemeral evidence, not committed tooling.
The live driver initially hit cp1252 while printing captured output after regen;
explicit UTF-8 fixed it, and the complete proof then ran successfully.

First wired A run: full doccheck **1.174 s**, emitted falsifiers **0.154/0.181 s**.
Final repair-tree measurement at **`a5f7719`**, using a PowerShell Stopwatch around
`python tools/doccheck.py --emit-counts`: **1.320 s**, GREEN, emitted
`ck170_selftest: PASS (0.145 s)`, `repair_pass_selftest: PASS (0.226 s)`,
`state_counts_selftest: PASS (0.144 s)`. These are observed wall times, not a
guarantee for another machine or a cold filesystem cache.

## Push set — attributed per file

Emitted by `python tools/doccheck.py --emit-counts` at **`a5f7719`**; baseline at
`5db516f` had the same per-file sizes. Only STATE's count bytes changed in this
set, with no byte-size delta. No external-memory delta is attributed to a commit.

| emitted member | LF-normalized bytes | attribution for this pass |
|---|---:|---|
| CLAUDE.md | 2506 | unchanged |
| docs/agent/STATE.md | 11098 | B count refresh; size unchanged |
| prompts/perma/GENERAL_USE_PROMPT.md | 7947 | unchanged |
| prompts/perma/DISPATCH.md | 10500 | unchanged |
| MEMORY.md (Claude, outside the repo) | 11176 | outside Git; measured on this rig only |

Verbatim emitted warning:

```
PUSH SET: 43227 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
```

The existing over-budget warning is report-only and was present at the anchor.
There was no new out-of-scope repair or owner decision.

## Close-out and R-G

The consumed one-off brief is removed with its `prompts/README.md` row in the
commit carrying this report; the repair commits remain independently revertible.
⛔ **Corrected — see § Adjudication: B calls A's helper, so they revert as a pair.**
The original brief is recoverable with
`git show 3196f5f:docs/agent/prompts/GATE_WIRING.md`.

Executed model: **`gpt-5.6-sol`, effort `high`**, read from the last
`turn_context` record in this session's local transcript:
`C:/Users/stkot/.codex/sessions/2026/09/13/rollout-2026-09-13T17-05-37-01a09c97-0423-7d02-8768-ae26ba4c2118.jsonl`.
The command selected only `payload.model` and `payload.effort`, not an assumed
role description. Element 7 does not apply: no game boot, save or module test.

## Adjudication — separate seat, 2026-09-13: **PASS**, one claim corrected

Judged against the brief's §8 by a seat that did not do the work. Every gate below
was re-falsified here rather than read off this report.

**§8, item by item.** doccheck **GREEN** · both named falsifiers wired and emitting
(`ck170_selftest: PASS`, `repair_pass_selftest: PASS`) · `--regen` **byte-identical**
on an already-correct tree (`sha256 0c27b62f…` before and after) · STATE's block
agrees with `--emit-counts` · push set re-emitted per file at **43,227 B**,
unchanged, with no external-memory delta attributed to a commit · brief and its
`prompts/README.md` row both gone · R-G recorded (`gpt-5.6-sol`, effort high) ·
handover present.

**Gates re-falsified independently, six ways, each restored by hash.** A failing
falsifier REDs doccheck (`exit 1`) and a *missing* one does too (`exit 2`, with the
interpreter's message carried through). B's region gate REDs on a wrong count, on a
**missing** region (`found 0`) and on a **duplicated** one (`found 2`), and `--regen`
repairs a corrupted region back to the exact baseline sha. `tools/doccheck.py` and
`tools/ck170_selftest.py` were each restored and hash-verified after use.

**Coverage probed beyond the pass's own mutants.** `state_counts_selftest` mutates
two guards; this seat removed a third it does not mutate — the `len(markers) != 1`
check — and the selftest **failed**, so the guard is genuinely covered rather than
covered by assertion.

**Exceeded the brief in four places worth keeping.** STATE is validated *before any
file write*, so a bad region cannot leave a half-regenerated tree — the brief only
asked for idempotence. The regenerated result is checked against **both** the hard
byte cap and the per-line cap. Other balanced fences in STATE are tolerated, so the
region cannot be confused with a neighbouring block. And the pass **wired its own
new falsifier** (`state_counts_selftest.py`) instead of leaving it orphaned, which is
precisely the defect this pass existed to repair; the easy failure here was to
reintroduce it, and that did not happen.

### Correction — the two commits are **not** independently revertible

This report says so twice (its opening line and § close-out). Measured: `def
required_selftest` is defined **once**, introduced by `f2b1898` (A). Of its three
call sites, lines 1933–1934 came from A and **line 1935 came from `a5f7719` (B)**.
So reverting A alone deletes the definition and leaves B's call standing — doccheck
raises `NameError` in `main()` and every peer's commit is blocked by the hook.
⛔ **They revert as a pair, B before A.** The dependency itself is the right
engineering call — B authored a falsifier and wiring it through A's runner beats
duplicating the runner or orphaning the test — so the defect is the claim, not the
code. Re-check: `git log -S'def required_selftest' -- tools/doccheck.py` against
`grep -n 'ok = required_selftest' tools/doccheck.py`.

The brief's "independently landable" clause was aimed at a different risk — that a
stop on one item would halt the other, as happened to `REPAIR_PASS` group C. That
risk did not materialise: both items landed. The clause should not have been
restated as a property of the commits.

### Nit

The three new gates emit lowercase labels (`ck170_selftest: PASS`) while every
neighbouring gate emits uppercase (`FLPK SELFTEST:`, `BODYCHECK SELFTEST:`). Not
cosmetic-only: it cost this adjudication a false "not emitted" reading, because the
obvious `grep -E 'SELFTEST'` over doccheck's output misses them. doccheck's runtime
went **0.835 s → 1.318 s**, which the pre-commit hook pays on every commit.
