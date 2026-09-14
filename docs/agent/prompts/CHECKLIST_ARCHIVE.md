# CHECKLIST_ARCHIVE — mark the settled backlog, then move it

**For Codex.** Authored 2026-09-13 by the adjudicating seat, from checklist **176**.
Owner approved the sequence in words: mark → falsify → move → recheck. `git rm` this file
**and delete its row in `prompts/README.md`, in the same commit**, when it has fired —
doccheck's PROMPT MAP gate fails a commit that moves only one of the two (checklist 174).

## 0 · Anchor — run first

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -5
python tools/doccheck.py | tail -1
python -X utf8 .claude/tools/archive_settled.py | head -12
```

Authored against **HEAD `6c07e69`**. ⚠️ Five-plus interactive peers share this checkout
under one git identity; `git log --author` attributes nothing, identify by sha + diff, and
**re-check `git status` immediately before every write** — a pathspec is only half a fence.
⛔ Never `--no-verify`. ⛔ Never check out a branch in the main tree.
⚠️ `docs/PLAYTEST_CHECKLIST.md` is the **hottest file in the tree** — a peer filed `ck175`
into it mid-session today. Expect to re-derive and re-run rather than trust any number here.

## 1 · The job — four commits, in this order

### A · Mark the settled-but-unmarked backlog

An item qualifies **only if all of these hold**, evaluated in this order:

1. it sits under `## Decisions waiting on you` and has **no marker**;
2. its `### ` heading matches `✅|RULED|CLOSED|DONE|RAN|LANDED|DISCHARGED`
   **OR** carries a date **before 2026-09-08**;
3. it is **not** excluded by the script's rule (a) title-citation;
4. it is **not** excluded by rule (d) number-citation;
5. it is **not** excluded by rule (c) procedure-bearing.

⛔ **Use the script's own functions for 3/4/5** (`rule_a_matches`, `cited_by_number`,
`is_procedure_bearing`) — do not reimplement them. ⚠️ `is_procedure_bearing` returns a
**`(bool, reason)` tuple**; a bare truth test on it is always true. That exact mistake
produced a false "nothing can move" reading during authoring.

**Status word** is derived, never guessed: heading says `RULED` → `ruled`; heading says
`CLOSED`/`DONE`/`RAN`/`LANDED`/`DISCHARGED` or carries only ✅ → `closed`. `owner:no` in
every case — these are settled and owe the owner nothing. Unnumbered items take `ck:-`.
⛔ **If an item's heading yields no status word and it qualified on date alone, it belongs
to group 2 below — do not invent a word for it.**

**Split the marking into two groups and keep them separately revertible:**

- **Group 1 — heading states completion.** ~11 items. Low risk: the item says what it is.
- **Group 2 — date-only.** ~24 items, selected purely on the owner's ruling that
  *"we ran stable with no changes for months before 1.1.0, so anything from before that is
  likely stale."* That is authority, not an inference — but it is a **heuristic**, and
  these items carry no completion word of their own.

### B · Falsify `--apply`, and give the stub a pointer

⛔ **`--apply` has never been executed.** Before it touches the real file:

- copy the repo tree (or the two files plus `tools/`) to a scratch location and run
  `--apply` **there**;
- prove the **header-count invariant**: `grep -c "^### " docs/PLAYTEST_CHECKLIST.md` reads
  the same before and after;
- prove **every surviving body is byte-identical** — diff the live-after against the
  live-before with the moved bodies excised;
- prove the archive gained exactly the moved bytes and nothing else;
- prove the tool **refuses** on a dirty tree and on a RED doccheck (break each on the copy).

⛔ **Close the load→write race before either move.** `main()` reads the checklist at
line 320 and writes it at line 508; `git_is_clean()` sits at line 489, between them. It
catches a peer's *uncommitted* edit, but a peer **commit** landing in that window leaves
the tree clean again and lets a write computed from stale bytes overwrite it. Measured
window: well under the run's 1.55 s total, since doccheck's ~1.3 s happens *before* the
load — call it 0.2–0.3 s. Small, but `PLAYTEST_CHECKLIST.md` is the hottest file in the
tree and a peer filed `ck175` into it today. **Fix: `sha256` the checklist at load, re-hash
immediately before `atomic_write`, and abort if it changed.** Falsify it — mutate the file
mid-run on a copy and require the abort. Cheap, and it makes the tool safe to run without
owning the tree.

Then add the one thing the stub lacks: the header and marker stay, but **nothing points at
where the body went**. Add a single line to the stub naming `archive/PLAYTEST_ARCHIVE.md`
and the `ck` label to grep for. It is covered by the same falsification. ⛔ If adding it
would change the byte tally the tool balances on, make the tally account for it — do not
disable the balance check.

### C · Move group 1 · D · Move group 2

Two separate `--apply` runs, two commits, so the heuristic half can be reverted alone.

## 2 · Read path — these files, not their folders

`.claude/tools/archive_settled.py` (`build_items`, `is_procedure_bearing`, `cited_by_number`,
`rule_a_matches`, `is_archive_old`, the apply tail) · `docs/PLAYTEST_CHECKLIST.md`
**§ "Decisions waiting on you" only** · `docs/agent/reports/DOC_OVERHAUL_AUDIT.md` §4 ·
checklist item **176** (the finding and the owner's options) · `tools/doccheck.py`
(`checklist_items`, `MARKER_RE`, `marker_integrity`). ⛔ Do not read the checklist whole.

## 3 · Derived facts (R-C) — every number below is a CLAIM; re-derive before acting

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| 35 items / 159,621 B qualify | the five rules above, via the script's functions | `6c07e69` | re-run the rule; ⛔ **stop and report if it does not reproduce** |
| **34 of the 35 are UNNUMBERED** (153,577 B) | `it["num"] is None` | `6c07e69` | ⚠️ see the risk note below |
| 24 of the 35 qualify on **date alone** | no completion word in the heading | `6c07e69` | heading regex over the qualifying set |
| 16 items / 43,223 B already move today | script dry run | `6c07e69` | `python -X utf8 .claude/tools/archive_settled.py \| tail -12` |
| the decisions section is 92.3% of the file | H2 byte split | `6c07e69` | sum bytes between `## ` headers |
| stub keeps header + marker | script line 12 and the `new_checklist` build | `6c07e69` | read `new_checklist_parts` |

⚠️⚠️ **The risk this brief exists to surface.** `cited_by_number` returns **False** for an
item with no number — so **rule (d) cannot protect 34 of the 35 items by construction**.
The protection that the whole archival design leans on is absent for almost the entire
move set, and 24 of those qualify on a date heuristic alone. This is not a reason to stop;
it is the reason group 2 is a separate commit and the reason a recheck pass follows. **Say
so plainly in the handover — do not let it read as a clean sweep.**

## 4 · Stop conditions — permission, not failure

Stop and report if: the qualifying set does not reproduce at 35 / 159,621 B · the tree is
dirty or a peer is mid-flight in the checklist · doccheck is RED before you start · the
byte tally does not balance · `--apply` fails any falsification leg on the copy · an item
would take a status word you had to guess · the stub pointer cannot be added without
disabling a check. Anything interesting outside §1: **file it, do not fix it.**

## 5 · What may NOT be claimed

- ⛔ **Never claim `--apply` is safe because it ran.** It is safe when a copy showed the
  invariants hold and showed the tool **refuse** on a dirty tree and a RED doccheck.
- ⛔ Never claim the moved items are "stale" — claim only that each met the stated rule.
  The date rule is the owner's heuristic, and 24 items rest on it alone.
- ⛔ Never claim rule (d) protected the move set. For 34 of 35 it could not run at all.
- ⛔ Do not widen the rule, do not auto-mark anything failing it, and do not touch
  `ARCHIVE-OLD` — it is report-only by design and changing that is an owner decision.
- ⛔ Never use `git checkout --` as a restore during falsification: it restores to HEAD and
  silently discards uncommitted work. Copy, then restore from the copy, and `sha256sum`.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 6 · Required — a live progress list

Create a todo list before starting, **one item per commit-and-verify unit**: group 1 marks ·
group 2 marks · the copy falsification · the stub pointer · move 1 · move 2 · the consume
commit. Mark each complete the moment it completes, keep exactly one in progress, and
expand a stage in place if it turns out to be more units than this brief anticipated. The
owner reads this list to decide when to step in.

## 7 · Not applicable, stated rather than omitted

**Element 7 (stale-probe gate) does not apply** — no game boot, save, module or shipped Lua.

## 8 · Done when

Four commits landed, group 2 revertible on its own · `doccheck GREEN` at every step ·
`MARKER INTEGRITY` parses every new marker with no gap · the header-count invariant holds
across both moves · surviving bodies byte-identical · the archive gained exactly the moved
bytes · the stub points at the archive · the before/after checklist size emitted **per
move, separately** · this brief and its `prompts/README.md` row both gone · executed model
recorded (R-G). Handover: `reports/CHECKLIST_ARCHIVE.md`, stating the unnumbered/date-only
risk in its own words. A Sonnet recheck pass over the archive addendum follows this brief
and is **not** part of it.
