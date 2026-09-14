# ARCHIVE_RECHECK — read the 35 archived bodies back, and flag what should not have gone

**Read-only.** Authored 2026-09-14 by the adjudicating seat, as the safety net the
`CHECKLIST_ARCHIVE` brief named and deliberately left out of its own scope. Sized for a
subagent: high volume, low reasoning per item, no writing git command. `git rm` this file
**and delete its row in `prompts/README.md`, in the same commit**, when it has fired —
doccheck's PROMPT MAP gate fails a commit that moves only one of the two (checklist 174).

## 0 · Anchor — run first

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -6
git status --porcelain
python tools/doccheck.py | tail -1
cat .rgignore
```

Authored against **HEAD `e547cb5`**. ⚠️ Five-plus interactive peers share this checkout
under one git identity; `git log --author` attributes nothing — identify by sha + diff.
⛔ Never check out a branch in the main tree.

⚠️⚠️ **`docs/archive/` IS HIDDEN FROM A DEFAULT `rg`** by the root `.rgignore`. A search
that does not name it returns **zero hits from the archive and no error**. This job lives
almost entirely in that folder, so every archive search must be
`rg <term> docs/archive/` or `rg --no-ignore <term>`; `grep -r` and `git grep` always see
everything. **An empty default search here is the boundary working, not evidence.**

## 1 · Why this exists — the gap in what just landed

On 2026-09-14, 35 decision bodies (159,621 B) moved out of `PLAYTEST_CHECKLIST.md` into
`archive/PLAYTEST_ARCHIVE.md`, in two commits: `1090f70` (group 1, 11 items whose headings
state completion) and `cfd97bc` (group 2, 24 items selected on the owner's rule that
anything predating 1.1.0 is likely stale). The execution was clean — every invariant held
and the per-move predictions landed to the byte.

**The exposure is in the selection, not the execution.** The archival design leans on rule
(d), which refuses to move an item whose **number** is cited elsewhere. **34 of the 35 have
no number**, so rule (d) could not run on them at all — it protected exactly one item
(`ck139`). And 24 of the 35 carry no completion word of their own; they qualified on the
date heuristic alone. Nothing has checked, item by item, whether a live document still
depends on something now sitting in the archive.

**That check is this job.** It has **no authority to move anything.** It produces a ranked
list of candidates and the evidence for each; a human decides.

## 2 · The job — three legs, in this order

### A · The stub pointers do not do what they say — confirm and quantify

Each of the 35 items left a stub behind: its original `### ` heading, its marker, and one
added line reading *"Body archived in [archive/PLAYTEST_ARCHIVE.md](...); search `ck-` and
this heading."*

⚠️ **Measured at `e547cb5`: following that instruction returns zero hits.** The archive
does not reproduce the checklist heading verbatim — it re-levels `### ` to `## ` and
rewrites the title as `## ck- -- archived 2026-09-14 (was checklist status:<s>): <title>`,
**dropping the leading date** that the checklist heading carries. So a reader who greps the
stub's heading finds nothing, and `ck-` is shared by 34 of the 35, which makes the other
half of the instruction non-discriminating too.

Confirm it, then quantify the damage rather than asserting it:

- take each stub heading; grep it verbatim in `docs/archive/` (naming the folder) — expect 0;
- strip `### ` and the leading `<date> — ` and grep the remaining title tail — expect 1 each;
- report how many of the 35 are findable by **any** literal the stub actually offers.

⛔ **Do not fix it.** The remedy touches the checklist and the append-only archive, and the
wording is an owner-facing surface. Report the exact replacement line you would propose.

### B · Live-dependency sweep — the check rule (d) could not perform

For each of the 35 archived items, decide: **does anything still live point at it?**

Method, per item: pull 2–4 **distinctive literals** from its heading and body — a file path,
a code identifier, a bug/fact id (`F##`/`C##`/`D##`/`EF-###`), a quoted owner phrase, a
proper noun. Prefer literals that would be *expensive to have duplicated by chance*; a bare
word like "upload" proves nothing. Then grep the **live** tree for each.

Live means: `docs/agent/STATE.md` · `docs/agent/prompts/perma/` · `docs/agent/WORKFLOW.md` ·
`docs/agent/FIX_POLICY.md` · `docs/agent/bugs/` · `docs/agent/facts/` ·
`docs/agent/reports/` · `docs/PLAYTEST_CHECKLIST.md` · `docs/PLAYTEST_HELP.md` ·
`docs/UPLOAD_WORKFLOW.md` · `docs/FIELD_REPORT_REPLIES.md` · `docs/README.md` · `Code/`.
⛔ **Exclude `docs/archive/` from this leg** — an archive-to-archive citation is not a live
dependency, and including it will drown the signal.

Flag as a **candidate to bring back** when a live document's meaning depends on the body
being readable in the checklist — not merely when a word co-occurs. A live doc that cites
the *subject* and explains it itself is fine; a live doc that says "see the checklist" for
something now archived is not.

⚠️ Weight the 24 group-2 items harder than the 11 group-1 ones. Group 1 items announce
their own completion; group 2 items were retired on their **age**, which says nothing about
whether an obligation inside them was ever discharged.

### C · Unfinished-obligation sweep — read the bodies

Read each of the 35 archived bodies and flag any that contains an obligation that was never
discharged: an action owed **by the owner**, an owed test or boot, an open question put to
the owner and never answered, a "NOT RUN" / "untested" / "⏳" / "OWED" / "waiting on you"
construction, a hold or a ruling that something ships only under a condition.

⛔ **A completion word in the heading does not settle the body.** Several of these items
announce one thing as done and add a second, unfinished ask in the same body — that shape is
exactly why the marking pass was auditable but not sufficient. Read to the end of each body.

⛔ Report what the body *says*, quoting the line. Do not adjudicate whether the obligation
was later met somewhere else — that is the human's call, and guessing it is how a real owed
item gets closed silently.

## 3 · Read path — these files, not their folders

`.claude/checklist_archive_group1.json` + `group2.json` (the 35 exact headings — the
selection of record) · `docs/archive/PLAYTEST_ARCHIVE.md` **the addendum only**, the region
after byte 365,038 · `docs/agent/reports/CHECKLIST_ARCHIVE.md` (what was done and what its
author already flagged) · `docs/PLAYTEST_CHECKLIST.md` **the 35 stub lines only** ·
checklist item **176** (the decision and its 2026-09-14 correction). ⛔ Do not read the
checklist whole. Indexes for anything further: `agent/bugs/INDEX.md`, `agent/facts/INDEX.md`.

## 4 · Derived facts (R-C) — every number is a CLAIM; re-derive before acting

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| archive 365,038 → 530,884 B; addendum **165,846 B** | `wc -c` both sides | `e547cb5` | `git show 4624ec2:docs/archive/PLAYTEST_ARCHIVE.md \| wc -c` vs `wc -c docs/archive/PLAYTEST_ARCHIVE.md` |
| **35 items** = 11 group 1 + 24 group 2 | the two JSON selections | `e547cb5` | `python -c "import json;print([len(json.load(open('.claude/checklist_archive_%s.json'%g,encoding='utf-8'))) for g in ('group1','group2')])"` |
| all 35 bodies present, exactly once | title-tail match after the date prefix | `e547cb5` | leg A's second bullet |
| **34 of 35 unnumbered** (only `ck139`) | the stub pointers | `e547cb5` | `grep -c 'search .ck-. and this heading' docs/PLAYTEST_CHECKLIST.md` → 34 |
| the stub's verbatim heading search returns **0** | archive re-levels and drops the date | `e547cb5` | leg A's first bullet |
| 165,846 − 159,621 = **6,225 B of wrappers** | archive delta vs bodies moved | `e547cb5` | the two numbers above |

⚠️ **The trap in this job is the negative.** "I searched and found nothing" is the verdict
this pass will produce most often, and it is the one that is worthless when the instrument
is wrong — a default `rg` silently skips the archive, and the stub headings do not match
verbatim. **Before trusting any zero, prove the same search finds a control you know is
there.** The first probe run during authoring reported all 35 bodies missing; the bodies
were fine and the probe was wrong.

## 5 · Scope fence

**In:** reading, grepping, and one report. **Out:** every write except that report.
⛔ No moves, no un-archiving, no edits to `docs/archive/` (append-only, never edited), no
edits to `PLAYTEST_CHECKLIST.md`, no marker changes, no `--regen`, **no writing git command
at all** — the dispatching seat commits. Anything interesting outside §2: **file it in the
report, do not fix it.**

## 6 · Stop conditions — permission, not failure

Stop and report if: the tree is dirty or a peer is mid-flight in the checklist or the
archive · doccheck is RED before you start · the 35 headings do not resolve to 35 bodies ·
a control search fails, so a negative cannot be trusted · an item's body contains an owner
obligation that looks **live and time-sensitive** (say so immediately, do not finish the
sweep first).

## 7 · What may NOT be claimed

- ⛔ Never claim an item is safe to leave archived because a search found nothing, unless
  the same search found a control. Name the control.
- ⛔ Never claim an obligation was discharged. Quote what the body says and stop.
- ⛔ Never claim the archival was wrong, or right, as a whole. This pass returns a list of
  individual candidates with individual evidence; a rate is not a verdict.
- ⛔ Never widen the sweep into the pre-existing archive (the 365,038 B before the addendum).
  It was not moved by this work and is not in scope.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 8 · Required — a live progress list

Create a todo list before starting, **one item per unit**: leg A stub-pointer confirmation ·
leg B split into batches of ~9 items (group 2 first) · leg C split the same way · the report ·
the consume. Mark each complete the moment it completes, keep exactly one in progress, and
expand a stage in place if it turns out to be more units than this brief anticipated. The
owner reads this list to decide when to step in.

## 9 · Not applicable, stated rather than omitted

**Element 7 (stale-probe gate) does not apply** — no game boot, save, module or shipped Lua.

## 10 · Done when

`reports/ARCHIVE_RECHECK.md` exists and carries: the leg A finding with its proposed
replacement stub line · a **ranked** candidate list, worst first, each row naming the item,
which group it came from, the evidence literal, where the live hit landed, and why it
matters · the items that came back clean, as a count **and** as a list, so the total
reconciles against its own members · every control search named · the executed model
recorded (R-G) · **and, if the list is empty, that stated plainly rather than padded.**

⛔ The report states in its own words that 34 of 35 items were unprotected by rule (d) and
24 rest on a date heuristic — a reader must not mistake a short candidate list for proof
that the selection was sound.

This brief and its `prompts/README.md` row both gone, in the same commit. No other file
changed.
