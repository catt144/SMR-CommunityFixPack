# GATE_WIRING — run the falsifiers, and generate the block that drifted

**For Codex. Two independent repairs, one pass.** Authored 2026-09-13 by the
adjudicating seat after `reports/CK170_AND_FINGERPRINTS.md` § Adjudication.
`git rm` this file **and delete its row in `prompts/README.md`, in the same
commit**, when it has fired — doccheck's PROMPT MAP gate fails a commit that
moves only one of the two (checklist 174).

## 0 · Anchor — run first, and check staleness

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -5
python tools/doccheck.py | tail -1
```

Authored against **HEAD `7ca25b9`**. Five-plus interactive peers share this
checkout under one git identity — `git log --author` attributes nothing, so
identify by sha + diff, and **re-check `git status` immediately before every
write**. A pathspec is only half a fence. ⛔ Never `--no-verify`; the hook can be
RED from a peer's in-flight probe. ⛔ Never check out a branch in the main tree.

## 1 · The two items — **independently landable, one commit each**

⭐ **A stop on one does NOT halt the other.** If item A is refused or turns out
to rest on a bad premise, land item B anyway, and vice versa. This clause is
here because `REPAIR_PASS` group C halted on a refuted sub-item and took three
unrelated repairs down with it; its own author called that the brief's fault.

### A · Wire the two orphaned falsifiers

`tools/ck170_selftest.py` and `tools/repair_pass_selftest.py` are run by nothing.
Wire them the way `flpk_selftest` and `bodycheck_selftest` already are, so the
gates they prove are re-proved on every commit rather than once by hand.

Shape is yours. The demand is that a future edit removing a guard is caught by a
machine, and that the emitted line says which falsifier ran and that it passed.

### B · Make `BUILD STATE` generated, not hand-typed

`docs/agent/STATE.md`'s fenced `BUILD STATE (emitted by tools/doccheck.py)` block
is a **generated region living in a hand-edited file**, which is why it drifted.
Add it to what `python tools/doccheck.py --regen` rewrites, and let the existing
freshness-check pattern catch drift — the same mechanism as `bugs/INDEX.md`.

⛔ **Do NOT build this as a standalone RED gate that compares the block to
`--emit-counts` and stops there.** Measured: 26 distinct commits since 2026-09-01
added or removed a `bugs/` entry, ~2/day across the peers; a bare comparison gate
would have blocked all 26 and forced a hand edit to the most contended file in
the tree. Regeneration costs nothing extra, because a stale `bugs/INDEX.md` is
**already** RED and `--regen` is therefore already mandatory after any entry
change.

Constraints, all falsifiable:
- **Idempotent.** `--regen` on a tree whose counts already agree must leave
  `STATE.md` **byte-identical**. Prove with `sha256sum` before and after.
- **Bounded.** `STATE.md` is byte-capped (warn 12288, hard 18432, per-line 200)
  and sits at 11,098 B. Regeneration must not push it over, and must not reflow
  or reorder anything outside the fenced block.
- **Delimited.** The fence plus the stable first line are the region's only
  markers; say in the code what happens if either is missing or duplicated.
- This is the **first generated region inside a hand-authored file** in this
  repo. If that turns out to be the wrong shape, say so and stop — see §4.

## 2 · Read path — these files, not their folders

`docs/agent/STATE.md` (the fenced block only) · `tools/doccheck.py`
(`regen`, `check_index`, `flpk_selftest`, `bodycheck_selftest`, `main`) ·
`tools/ck170_selftest.py` · `tools/repair_pass_selftest.py` · `tools/hooks/pre-commit` ·
`docs/agent/reports/CK170_AND_FINGERPRINTS.md` § Adjudication (the finding) ·
`docs/agent/WORKFLOW.md` § "Writing in a shared tree". More via
`agent/bugs/INDEX.md` / `agent/facts/INDEX.md`. ⛔ Do not open the checklist bodies.

## 3 · Derived facts (R-C) — each with the command that re-checks it

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| Neither selftest is run by anything | `grep -rln` over `*.py *.ps1 *.yml *.md`; only their own reports and each other | `7ca25b9` | `grep -rn 'ck170_selftest\|repair_pass_selftest' tools/ .github/ 2>/dev/null` |
| The hook runs doccheck alone | read `tools/hooks/pre-commit` | `7ca25b9` | `grep -c python tools/hooks/pre-commit` |
| Both are cheap | `time python tools/<name>.py` | `7ca25b9` | `time python tools/ck170_selftest.py` — 0.163 s / 0.225 s vs doccheck's 0.835 s |
| STATE's block is stale | block says `119 F + 12 D + 92 C` | `7ca25b9` | `diff <(grep 'BUGS index' docs/agent/STATE.md) <(python tools/doccheck.py --emit-counts \| grep 'BUGS index')` |
| A bare gate would tax ~2 commits/day | `git log --since=2026-09-01 --diff-filter=AD --format=%h -- docs/agent/bugs/ \| sort -u \| wc -l` → 26 | `7ca25b9` | same command |
| `--regen` already rewrites 5 things, and a stale INDEX is RED | read `regen()` and `check_index()` | `7ca25b9` | `sed -n '/^def regen(/,/^def /p' tools/doccheck.py` |

⛔ Every one of these is a **claim** until you re-run it. Re-derive the route,
not just the citation. If a number here is wrong, that is a finding — report it
rather than working around it.

## 4 · Stop conditions — permission, not failure

Stop and report if: a file you are about to write is dirty or owned by a running
peer · doccheck is RED outside your lane before you start · the generated-region
shape in B proves unsafe for a byte-capped file · either repair would need a
STATE **content** change rather than a count refresh · anything reads like an
owner decision (a status, a rule's phrasing, where a rule is filed). Something
interesting found outside §1: **file it, do not fix it.**

## 5 · What may NOT be claimed

- ⛔ **Never claim a gate works because it passes.** A gate nobody has watched
  fail is not known to be a gate. For each item: break a copy, watch it go **RED**,
  restore, and `sha256sum` the restore. Use **disk copies in a temp root** the way
  `ck170_selftest.py` already does — never `git checkout --` as a restore, because
  it restores to HEAD and silently discards uncommitted work.
- ⛔ **Never claim the wiring is cheap without re-timing it** after wiring, in the
  emitted doccheck run, not in isolation.
- ⛔ For B, "regeneration is safe" requires the **byte-identical idempotence proof**,
  not an assertion.
- ⛔ Do not claim item A re-proves the ck170 or repair-pass rulings. It re-proves
  only that those falsifiers still pass — the rulings were adjudicated separately.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 6 · Required — a live progress list

Create a todo list covering the whole job **before starting**, at **one item per
commit-and-verify unit** (A's wiring, A's falsification, B's regen, B's
idempotence proof, B's falsification, the consume commit are separate items — do
not bundle). Mark each complete the moment it completes, keep exactly one in
progress, and expand a stage in place the moment it turns out to be more units
than this brief anticipated. The owner reads this list to decide when to step in.

## 7 · Not applicable, stated rather than omitted

**Element 7 (stale-probe gate) does not apply** — this brief runs no game test
and records no test result. No boot, no save, no module change, no shipped Lua.

## 8 · Done when

Two commits landed, each independently revertible; `doccheck GREEN`; both
falsifiers wired and emitting; each new or changed gate shown RED on a broken
copy and restored by hash; `--regen` idempotent on `STATE.md` by sha; STATE's
block agreeing with `--emit-counts`; the push set re-emitted (it includes
`MEMORY.md`, which is outside the repo and controlled by no commit — attribute
per file, never by total); this brief and its `prompts/README.md` row both gone;
and the executed model recorded at close-out (R-G). Handover:
`reports/GATE_WIRING.md`.
