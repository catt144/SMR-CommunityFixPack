# Doc rules architecture — proposal, 2026-09-14

**Nothing has moved.** This is a design for the owner to rule on, built on the inventory in
[RULES_HEADERS](RULES_HEADERS.md) (852 rule occurrences, Codex, `968c58e`). It does not
re-derive that inventory; it re-cuts the *migration* against a three-tier model the owner
specified on 2026-09-14, and it reverses one part of the standing proposal.

⛔ The open marker-enforcement question (checklist **177**) is untouched here, and the
temporary STATE cap (checklist **178**) is not retired by this.

## 0 · The owner's design, and the goals it serves

> *"One source of perma rules that need to be followed all the time, and our goal is to make
> it as small as possible. And then our per folder rules that are only there for an agent if
> they are in there. And possibly … task related rules to the skill so then the rule is only
> called when the skill is."*

Three goals, ranked by the owner: **(1)** cut redundancy, because redundant rules degrade
adherence; **(2)** make a rule visible only where it is relevant, for the same reason;
**(3)** cut always-loaded context.

⚠️ **Goal 3 is the smallest of the three and must not be used to justify the work.** Measured
2026-09-14: the entire always-loaded surface is ~16,000 tokens (`STATE.md` ~6,200 · memory
index ~5,544 · 19 skill descriptions ~3,000 · `CLAUDE.md` ~1,250). One undirected
`rg "OnMsg"` over the shipped tree costs **~76,000 tokens** — 4.8× the whole surface. The
context prize lives in search direction, not in rule placement. **This proposal is justified
by adherence and rot, which are worth it on their own terms.**

## 1 · The tiers, defined by WHEN THEY LOAD

| tier | home | loads | carries |
|---|---|---|---|
| **1 · permanent** | `CLAUDE.md` (mirrored byte-identical to `AGENTS.md`) | mechanically, every session, both vendors | only rules that bind **every** session regardless of task |
| **2 · local** | one block per **folder**, or per doc where a doc is genuinely unique | when an agent works there | rules governing edits to that material |
| **3 · task** | skills (mirrored to `.agents/skills/`, RED-gated) | on invocation | procedure for a named task |
| — | `doccheck.py` | every commit | the only *loud* failures; see §6 |

**Tier 1's delivery is mechanical** — `CLAUDE.md` is loaded without anyone choosing correctly
first, which is a stronger guarantee than a prompt (a prompt reaches an agent only if the
right prompt was picked). This is why the kernel rule belongs there and not in all 13 perma
prompts, which was considered and rejected on 2026-09-14 as N copies of one line.

## 2 · ⭐ The reversal — per-doc headers would encode the redundancy, not remove it

The standing proposal is **16 per-doc headers**. Eleven of those sixteen are in
`prompts/perma/`. Measured at `f129eff`:

- **`prompts/README.md:5` already states the rule once, for all of them** —
  *"never `git rm`; update in place"*.
- **Seven of the nine restate it inside their own text** (10 restatements): `DISPATCH` 1 ·
  `RELEASE` 2 · `POST_UPLOAD_CLOSE` 1 · `DRONE_PROJECT_PROMPT` 1 · `LINUX_DISPATCH` 2 ·
  `SMRTK_SLOTS` 1 · `STATE_EVICTION` 2. (`GENERAL_USE_PROMPT` and `COMBINED_SITTING`: 0.)

⇒ Hoisting each file's copy into its own header would make **nine permanent copies of one
rule** — the precise failure this effort exists to end. Re-check:
`grep -n 'never .git rm.; update in place' docs/agent/prompts/README.md` and the per-file
grep in the row above.

**Instead:** the perma lifecycle rule stays where it already is (the folder's README, which
*is* the folder-level home), and the **in-file restatements are deleted**. 10 copies → 1.
That is a net *reduction* in rules, which serves goal 1 directly; the header proposal serves
neither goal 1 nor 2 for these nine files.

### Headers that survive — where a doc carries a genuinely unique rule

| doc | its own rule |
|---|---|
| `docs/PLAYTEST_CHECKLIST.md` | work-list-only + the ck177 retirement rule |
| `docs/PLAYTEST_HELP.md` | reference-only content contract |
| `docs/UPLOAD_WORKFLOW.md` | upload-only; backup copies match the card |
| `docs/agent/FIX_POLICY.md` | §5 is protected against deletion |
| `docs/agent/STATE.md` | kernel-only (see §4) |
| `prompts/perma/HANDOFF_ORCHESTRATOR.md` | owner-only retirement |
| `prompts/perma/RELEASE_OUTBOX.md` | append/clear lifecycle, no silent deletion |

**Seven, not sixteen** — and nine deletions alongside. ⛔ Byte counts for the seven are in
`RULES_HEADERS.md`'s table and must be **re-emitted before writing**, not inherited.

## 3 · Tier 1 — the permanent list

`CLAUDE.md` has **no rules list today**; its 8 rule occurrences sit in prose. Proposal: an
explicit, short, numbered list, seeded from the **16 global** occurrences the inventory
found, deduped, **plus one line**:

> Editing a doc? Invoke the doc-editing skill first.

⚠️ **10 of those 16 globals currently live in `WORKFLOW.md`** — read per task, not always. They
bind every session but reach only the sessions that happen to open it. That is the inverse of
redundancy and arguably worse, and **the standing proposal does not move them.** Relocating
them is the single largest adherence win available here.

## 4 · `STATE.md` — rules go to zero

STATE's own line 3 reads *"Kernel only: status + pointer, never derivation."* The inventory
found **30 rule occurrences in it**. By its own charter it should carry **none**. Proposal:
every rule leaves STATE for its tier; status, pointers, holds, owes and the counts block stay.

This is also why STATE keeps pressing its cap — it is carrying 30 rules that are not its job.

## 5 · Tier 3 — two skills that earn their existence

⛔ Owner's bar, 2026-09-14: *"it needs to meet the requirements of the skill does something"* —
no skill created merely to host a rule.

**`doc-editing`** — clears the bar on content alone. Every item below was needed in the
2026-09-14 session, and several were got wrong: which docs are **generated** (`bugs/INDEX.md`,
`facts/INDEX.md`, `AGENTS.md`, `WAITING_ON_YOU.md`) and the `--regen` route · editing
`CLAUDE.md` drifts `AGENTS.md` and REDs the tree for every peer · shared-tree protocol
(re-check `git status` before every write, commit by pathspec, never `--no-verify`, `--regen`
is not yours alone) · doccheck GREEN before committing · the `.rgignore` archive boundary ·
the `docs/` folder contract · checklist markers and register regen · ck177 retirement · byte
caps incl. ck178's temporary raise · the PROMPT MAP file-and-row rule · owner decisions go in
the checklist. **That runbook does not exist as a unit today** — it is scattered across
`WORKFLOW.md`, `CLAUDE.md`, `prompts/README.md` and doccheck docstrings.

**`prompt-authoring`** — already written as `WORKFLOW.md` elements 1–9 plus R-C/R-G; the work
is packaging, not authoring.

⚠️ Each skill costs ~120–160 tokens of always-loaded description, and **both existing skills
are already over doccheck's 3,072 B target** (3,685 / 3,312). A cap discipline must come with
tier 3 or the problem rebuilds inside the skills.

## 6 · ⛔ What none of this is

**There are no gates here.** Owner, 2026-09-14: *"nothing is a real gate except my stop
button"* — in bypass mode `--no-verify` defeats doccheck, a script's guard is a line an agent
can edit, a hook lives in a file an agent can rewrite. The achievable goal is moving failures
from **silent** (an unread rule, an orphaned memory, a row pointing at a deleted file) to
**loud** (a RED doccheck, a sha-guard abort, the `⏳` cap line) — bypassable, but not
accidentally and not invisibly.

⚖️ The owner's 2026-09-13 ruling is worded *"a hazard is a failure not yet converted into a
gate."* Under this clarification it should read **"into a loud failure."** Same substance;
the current wording promises something this system cannot provide. It is quoted in
`STATE_EVICTION.md` and in briefs. **The owner's wording, so flagged rather than changed.**

## 7 · What is being asked

1. Adopt the three tiers.
2. **Seven headers, not sixteen**, plus deletion of the nine perma restatements.
3. Tier 1: an explicit rules list in `CLAUDE.md`, including the doc-editing pointer, and
   move `WORKFLOW.md`'s 10 globals into it.
4. `STATE.md` goes to zero rules.
5. Build `doc-editing`; package `prompt-authoring`; set a skill byte cap.
6. Amend the "gate" wording in the 09-13 ruling — owner's call.

Codex's inventory survives all of this: the 852 classifications, 20 redundant pairs, 6 dead
proofs and the E1–E3 / R12–R14 proposals are reusable as-is. What changes is the shape of the
migration, not the evidence under it.
