# RULES_HEADERS — inventory every rule, put the doc-local ones in a header, keep one rule in the kernel

**For Codex.** Authored 2026-09-14 by the adjudicating seat, from the owner's design ruling of
the same date. `git rm` this file **and delete its row in `prompts/README.md`, in the same
commit**, when it has fired — doccheck's PROMPT MAP gate fails a commit that moves only one of
the two (checklist 174).

## 0 · Anchor — run first

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -6
git status --porcelain
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'STATE \+ STUBS|PROMPT MAP'
```

Authored against **HEAD `a6726b5`**. ⚠️ Five-plus interactive peers share this checkout under
one git identity; `git log --author` attributes nothing — identify by sha + diff, and re-check
`git status` **immediately before every write**. ⛔ Never `--no-verify`. ⛔ Never check out a
branch in the main tree — it is the game's loadable mod via a junction.

## 1 · The design being implemented — the owner's, 2026-09-14

**Their reasoning, verbatim:** *"the more rules agents have to read especially redundant rules
the more likely they are to not follow them, not out of maliciousness but out of complexity.
Wouldn't a better method be to have a specific header section on docs that list any rules. And
when an agent opens a doc they don't need to read the whole doc, but they have to read that
header section. and then the mandatory doc that all agents have to read lands the rule that all
agents must read the header of any doc they are about to edit?"*

So: **N scattered rules become N local header blocks plus ONE kernel rule.** A session that never
opens a doc never carries that doc's rules. ⭐ The repo already runs a working instance of this
shape — the line-1 banner on `bugs/INDEX.md`, `facts/INDEX.md` and `WAITING_ON_YOU.md`
(*"GENERATED — never hand-edit; regenerate with: …"*) is obeyed by agents who have read no
policy document at all.

⚠️ **Evidence the redundancy problem is real here, not imported:** the `ARCHIVE_RECHECK` brief
written by this seat on 2026-09-14 told its executor to `git pull` in §0 and forbade every
writing git command in §5. Two rules, contradictory, in a 12 KB document written that afternoon,
and the author did not notice — the executing agent had to detect it, choose the safer reading
and document the departure. ⇒ **Rule count produces contradiction, and contradiction produces
silent divergence.** That is the failure this job exists to cut.

## 2 · The job — four stages, with an OWNER GATE before anything moves

### A · Inventory every rule, and classify it

⛔ **First, the definition, because the wrong one drowns this job.** A **rule** is an imperative
that constrains what a future agent may **do**, and that an action can **violate**. It is not:

- a **fact** (can be true or false, cannot be violated) — *"the pack route is MOD EDITOR → Pack Mod"*;
- a **status** — *"v10 is live on both portals"*;
- a **record of a past ruling** — the decision bodies in `PLAYTEST_CHECKLIST.md`.

⚠️ **Measured 2026-09-14: the checklist carries 319 `⛔` of which exactly 2 are in its preamble.**
The other 317 sit inside decision bodies and are **records, not doc-edit rules**. An inventory
that treats every `⛔` as a rule will return hundreds of false members and be useless. The
ruling that created a rule is a record; the rule's home is wherever it binds.

For each rule found, record: its verbatim text · its current file and line · and **one class**:

| class | test | home it should have |
|---|---|---|
| **doc-local** | *"If I never open doc X, can I ever violate this?"* — **no** | X's rules header |
| **task-local** | binds only an agent doing a named task (a release, a fix, an upload) | the doc that governs that task |
| **global** | binds every session regardless of what it opens | the kernel (`STATE.md`) |
| **redundant** | the same rule is stated in 2+ places | one canonical home; the copies become pointers or go |
| **dead** | it names a file, tool, process or state that no longer exists | proposed for deletion |

⛔ A **pointer** to a rule is not a duplicate — leave pointers alone. A **local specialisation**
("in this doc, rule 5 also means…") is not a duplicate either. Only report genuine restatements,
and quote both sides so a reader can judge the call rather than trust it.

⚠️ Expect `dead` to be non-empty and do not treat a small count as failure. The prompts map was
**55% records of prompts that no longer existed** when it was checked on 2026-09-13, and nothing
cited any of them.

### B · Specify the header, and check which docs need one

Propose the block's exact shape and get it approved at the gate before writing any. The starting
proposal, which you may depart from with a reason:

```
<!-- RULES -->
… the rules that govern editing THIS doc, one per line …
<!-- /RULES -->
```

- placed immediately after the doc's H1, before any prose;
- machine-findable by those two literal markers, so doccheck can check it;
- **byte-capped** — ✅ **RULED 2026-09-14: 1,024 B warn / 2,048 B hard** (superseding the 1,536 proposed here, which was an arbitrary number the author invented; 14 of the 16 measured headers are under 800 B and one missed 1,536 by a single byte). ⚠️ The cap is the load-bearing part:
  without it this becomes the original problem one level down.

⛔ **Only docs that actually constrain editing get a header.** A ceremonial empty block on every
file teaches agents the header is noise, which is worse than no header — that is exactly how the
`ck-` stub pointer failed on 2026-09-14 (present, obeyed-looking, and non-discriminating). The doc list is
SETTLED by the all-clear below — seven docs, named there.

### ✅ OWNER ALL-CLEAR GRANTED 2026-09-14 — with three amendments, checklist 179

⛔ **The gate below is DISCHARGED. Read these amendments before Stage C; they override the
text above where they differ.**

1. ⭐ **SEVEN headers, not sixteen** — and **delete the 9 perma restatements** instead.
   Measured: `prompts/README.md:5` already states *"never `git rm`; update in place"* ONCE for
   all eleven perma prompts, and **seven of the nine restate it internally** (10 live copies).
   Per-doc headers there would make nine permanent copies of one rule — the failure this brief
   exists to end. The seven that survive are the docs carrying a genuinely unique rule:
   `PLAYTEST_CHECKLIST` · `PLAYTEST_HELP` · `UPLOAD_WORKFLOW` · `FIX_POLICY` · `STATE.md` ·
   `perma/HANDOFF_ORCHESTRATOR` · `perma/RELEASE_OUTBOX`.
2. ✅ **Cap 1,024 warn / 2,048 hard** (see §B).
3. ⛔ **Re-deriving the STATE arithmetic before writing is a STOP CONDITION, not a note.** The
   banked figure (12,331 → 12,274 B, "14 B under the permanent warn") went stale **within two
   hours** — STATE was 12,504 B the same evening, which puts the post-change file **+159 B OVER**
   the permanent warn. If it does not land where re-derived, **stop and report**.

⚠️ **Also ruled in checklist 179, and in scope for whoever resumes this:** `CLAUDE.md` gets an
explicit rules list including *"Editing a doc? Invoke the doc-editing skill first."*, and
**`WORKFLOW.md`'s 10 global rules move into it** — this brief does not currently move them, and
they bind every session while sitting in a doc read only per task. **`STATE.md` goes to zero
rules.** ⛔ The 09-13 *"converted into a **gate**"* wording is **DECLINED** — leave it alone.

### ⛔ OWNER GATE — DISCHARGED 2026-09-14 (kept for the record)

**Moving a rule changes where it binds, and a rule that silently stops binding is the worst
outcome this job can produce.** A and B are analysis and land as a report; nothing in the doc
tree changes. Then **stop**, and hand the owner one short message carrying:

- the inventory as counts **per class and per doc**, plus the full list as an attachment;
- the redundancy findings, **both sides quoted**, with a proposed canonical home for each;
- the `dead` list, each with the one command showing what it names is gone;
- the header spec and the **cap number** you are asking them to approve;
- the doc list that would get a header, and the docs that would not, with reasons;
- **the net byte effect on `STATE.md`** — see §3;
- anything you would flag if you were the one reverting it later.

⛔ **Do not move, delete or rewrite a single rule until the owner answers.** Waiting costs
nothing; the analysis is already banked in the report.

### C · Land the headers — only after the all-clear

⛔ **Verbatim moves.** A rule's wording is its meaning; rewording one while relocating it is a
silent change to what binds. Move the text byte-for-byte, and where a rule genuinely must be
re-worded to stand alone in a header, **list it separately at the gate as a re-wording, not a
move**, and quote before and after.

- **One commit per source doc**, so any single doc's migration reverts alone.
- After each commit: `doccheck` GREEN · the moved rules' text still present byte-identical
  somewhere in the tree (`git grep -F` the exact string) · nothing else in the doc changed.
- Where a rule leaves a doc entirely, decide with the owner's approved canonical home whether a
  one-line pointer stays behind. ⛔ Do not leave a struck-through or "moved to…" tombstone; the
  prompts-map ruling (checklist 174) is the precedent — a record of something that no longer
  lives there is how a next session follows spent guidance.

### D · Land the kernel rule, and gate the structure

Last, and only once headers exist — a rule telling agents to read a header that is not there yet
teaches them the rule is noise.

- **One line in `STATE.md`**, in `Rules in force`: read the rules header of any doc you are about
  to edit. ⛔ One line. This rule earns kernel bytes **only** because it replaces many.
- **A doccheck check** — `RULES HEADERS` — asserting, for every doc on the approved list: the
  block exists, both markers are present and correctly ordered, and it is within cap. RED on a
  missing or oversized block on a listed doc; that is a structural check the machine can hold.
- ⚠️ **State plainly in the report what this check cannot do: it cannot verify that an agent read
  the header.** This design reduces rule load; it does not convert the hazard into a gate. Do not
  let the report imply otherwise.

## 3 · Read path — these files, not their folders

`docs/agent/WORKFLOW.md` (densest: **40** `⛔`, **27** numbered rules) · `docs/agent/FIX_POLICY.md`
(**18** / **11**) · `docs/PLAYTEST_HELP.md` (**21** / **16**) · `docs/UPLOAD_WORKFLOW.md` (**5** /
**4**) · `docs/agent/STATE.md` (**29** `⛔`, mostly hazards and facts — classify carefully) ·
`docs/PLAYTEST_CHECKLIST.md` **the preamble only** · `CLAUDE.md` · `docs/README.md` ·
`docs/agent/prompts/perma/` (standing prompts carry binding rules) · `tools/doccheck.py`
(`check_state_and_stubs` is the model for a byte-capped check). Indexes for anything further:
`agent/bugs/INDEX.md`, `agent/facts/INDEX.md`.

⛔ **Out of scope:** `docs/archive/` (append-only, never edited — its only rule is "never edit",
and it already lives in `docs/README.md`) · one-off prompts in `prompts/` root (they self-consume)
· chain folders · `docs/PLAYTEST_CHECKLIST.md` **below the preamble** (records, not rules).

⚠️ `CLAUDE.md` has a byte-identical generated mirror, `AGENTS.md`. **Editing `CLAUDE.md` drifts it
and turns doccheck RED for every peer** until `--regen` runs. Treat any change there as a separate,
announced commit.

## 4 · Derived facts (R-C) — every number is a CLAIM; re-derive before acting

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| checklist: **319** `⛔` total, **2** in the preamble | `grep -o` whole file vs `sed -n '1,70p'` | `a6726b5` | `grep -o '⛔' docs/PLAYTEST_CHECKLIST.md \| wc -l` vs the same over lines 1-70 |
| WORKFLOW **40** `⛔` / **27** numbered rules | `grep -o`, `grep -cE '^\s*[0-9]+[a-z]?\. \*\*'` | `a6726b5` | the two greps, per doc |
| corpus ≈ **1.08 MB** over 10 docs + 13 perma prompts | `wc -c` per file, `du -sb` on perma | `a6726b5` | re-run both |
| `STATE.md` **12,176 B**, warn **12,288** | doccheck STATE + STUBS | `a6726b5` | `python tools/doccheck.py \| grep 'STATE + STUBS'` |
| the line-1 banner precedent exists on 3 files | `head -1` each | `a6726b5` | `head -1 docs/agent/bugs/INDEX.md docs/agent/facts/INDEX.md docs/WAITING_ON_YOU.md` |

⚠️ **`STATE.md` has ~112 bytes of headroom.** Stage D adds a line, so the kernel must *lose* at
least as much as it gains: the meta-rule is only affordable if stage A finds doc-local rules in
STATE to evict. **Report the net effect at the gate.** ⛔ If the audit finds nothing evictable
from STATE, say so — do not compress lines to fit (`WORKFLOW.md` rule 8: evict, don't compress),
and do not trip the warn silently.

## 5 · Scope fence

**In:** the corpus in §3, the inventory, the header spec, the migration the owner approves, the
kernel line, and the doccheck check. **Out:** changing what any rule *means* · deleting a rule
the owner has not approved for deletion · `docs/archive/` · the checklist below its preamble ·
the open marker-gate question in checklist **177**, which is a separate owner decision and must
not be folded into this job. Anything interesting outside §2: **file it, do not fix it.**

## 6 · Stop conditions — permission, not failure

Stop and report if: a rule's meaning would change to fit a header · two rules genuinely conflict
(report both, resolve neither — a conflict is an owner decision) · `STATE.md` cannot afford the
kernel line · the tree is dirty or a peer is mid-flight in a target doc · doccheck is RED before
you start · the inventory exceeds what one pass can classify honestly — **report a partial
inventory with its boundary stated, rather than a complete-looking one.**

## 7 · What may NOT be claimed

- ⛔ Never claim this makes rule-following reliable. The check is structural; **nothing verifies
  a header was read**, and the report must say so in its own words.
- ⛔ Never claim a rule is redundant without quoting both instances.
- ⛔ Never claim a rule is dead without the one command that shows its referent is gone.
- ⛔ Never claim a move preserved a rule because the doc still reads well — prove it with
  `git grep -F` on the exact string.
- ⛔ Never widen into checklist 177's marker gate, and never use this job to settle it.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 8 · Required — a live progress list

Create a todo list before starting, **one item per commit-and-verify unit**: inventory per source
doc (one item each) · classification · redundancy pass · dead pass · header spec · **the owner
gate (blocked, waiting)** · one item per doc migrated · the kernel line · the doccheck check ·
the report · the consume. Mark each complete the moment it completes, keep exactly one in
progress, and expand a stage in place if it turns out to be more units than this brief
anticipated. The owner reads this list to decide when to step in.

## 9 · Not applicable, stated rather than omitted

**Element 7 (stale-probe gate) does not apply** — no game boot, save, module or shipped Lua.

## 10 · Done when

⛔ **Not startable past the OWNER GATE without the owner's all-clear in words.**

The inventory exists as `reports/RULES_HEADERS.md` with counts per class and per doc that
**reconcile against their own members** · every approved doc carries a conformant header within
cap · every moved rule is byte-identical somewhere in the tree · the kernel carries exactly one
new line and `STATE.md` is at or under its warn · doccheck's `RULES HEADERS` check is live and
was **watched to fail** on a broken copy and restored by hash · `doccheck` GREEN at every step ·
one commit per source doc so each reverts alone · executed model recorded (R-G) · this brief and
its `prompts/README.md` row both gone, in the same commit.

The report states, in its own words, what the structural check cannot verify.
