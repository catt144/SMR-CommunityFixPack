# DOC_EDITING_SKILLS — audit the runbook against the gates FIRST, then build only what is left

Authored 2026-09-15 by the adjudicating seat, from the owner's rulings of the same date. `git rm`
this file **and delete its row in `prompts/README.md`, in the same commit**, when it has fired —
doccheck's PROMPT MAP gate fails a commit that moves only one of the two (checklist 174).

## 0 · Anchor — run first

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -6
git status --porcelain
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'SKILLS' -A4
```

Authored against **HEAD `84f0c86`**. ⚠️ Several interactive peers share this checkout under one git
identity; `git log --author` attributes nothing — identify by sha + diff, and re-check `git status`
**immediately before every write**. ⛔ Never `--no-verify`. ⛔ Never check out a branch in the main
tree — it is the game's loadable mod via a junction.

## ⛔ 1 · READ THIS FIRST, BEFORE ANYTHING ELSE

**`.claude/PENDING_MOVES.md`.** It is gitignored, nothing in the tree points at it, and it says so
itself:

> *"A pending move is INVISIBLE. Nothing in the tree shows that this content is scheduled to leave.
> That is deliberate… This file is the only record."*
> *"WHOEVER BUILDS THE FIX-AUTHORING / PLAYTEST / PROMPT-AUTHORING SKILL MUST READ THIS FILE FIRST.
> If they do not, every row below is silently lost and the source text stays in a doc it was ruled
> out of."*

You are that builder. ⛔ **If you skip it, this job silently fails** and no gate will tell you.

## 2 · Why this brief exists, and what makes it different

The standing plan was "build `doc-editing` from the list in `reports/DOC_RULES_ARCHITECTURE.md`
§5." ⭐ **That list was written before several of its items became doccheck gates, and nobody has
checked which.** Restating a gated duty as skill prose is redundancy in a new container — the exact
thing the 2026-09-15 rules migration spent a day removing from the kernel.

⇒ **The first deliverable is an audit, not a skill.** `DOC_RULES_ARCHITECTURE.md` §6 states the
achievable goal: move failures from **silent** to **loud**. For much of §5's list, doccheck already
did. What the skill must carry is the remainder.

⚠️ **A second reason the shape changed, and it closes off a tempting test.** `smr-session-close` was
A/B-tested cleanly (`.claude/evidence/skill_ab_2026-09-14/`) because every session closes out, so
there was a natural control population. **That method does not transfer here.** For a while yet,
`doc-editing`'s only real consumers are overhaul seats already told what to do by a brief, so
"did an agent invoke it unprompted" cannot be separated from "the brief said to." ⛔ Do not propose
or run that A/B. Its replacement is in §7.

## 3 · The job — five stages

### A · The gate audit — the first deliverable, and the cheap one

Take **every item in `reports/DOC_RULES_ARCHITECTURE.md` §5's `doc-editing` list.** For each,
answer one question: **is this already gated?** Name the check that gates it, and ⛔ **verify by
reading `tools/doccheck.py` and by watching the check's output — not by assuming from its name.**

This seat's own pass, offered as a **starting claim to be falsified, not inherited**:

| §5 item | claimed gate |
|---|---|
| generated INDEX files and the `--regen` route | `INDEX: fresh`, `FACTS INDEX: fresh` |
| `CLAUDE.md` drifts `AGENTS.md` | `ENTRY MIRROR` |
| doccheck GREEN before committing | the pre-commit hook itself |
| the `docs/` folder contract | `ROOT` |
| PROMPT MAP file-and-row | `PROMPT MAP` — ⚠️ **existence only, NOT content** |
| byte caps including temporary raises | `STATE + STUBS`, `RULES HEADERS` |
| checklist markers and register regen | `MARKER INTEGRITY`, `WAITING` |
| the `.rgignore` archive boundary | **none found** |
| shared-tree protocol — status before write, pathspec | **none found** |
| owner decisions go in the checklist | **none found** |
| ck177 retirement | **not checked by this seat** |

⚠️ **Expect to overturn rows.** A claimed gate may check something narrower than the duty — the
`PROMPT MAP` row is exactly that case and it has a receipt: `PROMPT MAP` asserts a row and a file
both exist and never that the row still *describes* the file. On 2026-09-15 this seat revised
`RULES_HEADERS.md` at `9229434` and left its map row describing the design it had replaced; the
gate stayed green and the error was found by accident two commits later (`3ec1e1a`).

**Then classify each ungated item into exactly one of three:**
- ⭐ **GATE** — cheaper as a doccheck check than as prose nobody is forced to read. The stale
  map-row case above is the strongest candidate: comparing a row against its file is mechanical.
- **SKILL** — genuinely needs a reader's judgement, so it goes in the body.
- **DROP** — restates something already loud, or names a duty nothing has ever violated.

⛔ **Do not build anything until this table exists.** It is small, it is the whole point, and it
determines the size of everything downstream.

### B · Build `doc-editing` from the remainder only

Only the SKILL rows from stage A. ⛔ Nothing that stage A found gated. If the remainder is small,
**the skill is small — that is success, not a shortfall.** If the remainder is empty, say so and
stop; a container built to host nothing fails the owner's bar (ck179: *"it needs to meet the
requirements of the skill does something"*).

⚠️ Building this skill discharges an obligation: `CLAUDE.md` currently carries
`Rule: Invoke the doc-editing skill before editing a document.` — **a rule no agent can comply
with, because the skill does not exist.** Once it does, the rule becomes live. Say so in the report.

### C · Build `prompt-authoring`

§5: *"already written as `WORKFLOW.md` elements 1–9 plus R-C/R-G; the work is packaging, not
authoring."* Treat it as packaging. ⚠️ Run it through stage A's same question first — a duty
already gated does not become un-gated by moving to a different skill.

### D · Drain `PENDING_MOVES.md`

Every row whose destination now exists. ⛔ **`PENDING_MOVES` is explicit that a partial move is the
worst outcome:** *"Status is PENDING until the content is in its destination AND removed from its
source. Half a move is worse than none — it duplicates the duty into two places."*

⇒ For each row: content lands in the destination **and** leaves its source, in the same commit, and
the row is marked done in `PENDING_MOVES.md`. A row you cannot complete stays PENDING with a stated
reason — never half-moved.

### E · Measure the skill set and report it

`python tools/doccheck.py | grep -E 'SKILLS' -A4`. At `84f0c86` the three existing skills are
**3,622 / 3,248 / 4,490 B**, all above the 3,072 B design target, and ⏳ **the caps are DOWN by owner
ruling 2026-09-14**, so size is reported and not gated.

⚠️ §5 warns that tier 3 without cap discipline rebuilds the monolith one level down. ⇒ **Report the
five sizes and propose numbers with a reason.** ⛔ **Do not set them** — the owner's ruling says the
new numbers are theirs to pick.

## ⛔ 4 · NOT IN SCOPE — the `PLAYTEST_HELP` dissolution

ck182 proposes dissolving `docs/PLAYTEST_HELP.md` (62,965 B) across four destinations, two of which
are the skills this brief builds. ⛔ **It is `status:open owner:yes` and MUST NOT be started here.**
Building the destinations is this job; moving the monolith into them is a separate job that cannot
begin without the owner's dissolve ruling in words.

⚠️ If stage A or C surfaces content that clearly belongs to that split, **record it and leave it
where it is.** Do not pre-empt an open owner decision by relocating its subject.

## 5 · Read path — these files, not their folders

`.claude/PENDING_MOVES.md` (first, §1) · `reports/DOC_RULES_ARCHITECTURE.md` §5 and §6 ·
`tools/doccheck.py` (the checks themselves, to verify stage A) · `docs/agent/WORKFLOW.md` elements
1–9 plus R-C/R-G (stage C's source) · the three existing skills in `.claude/skills/`, as worked
examples of house voice and size. ⛔ **Out:** `docs/archive/` · the checklist below its preamble ·
`docs/PLAYTEST_HELP.md` (§4) · checklist 177's marker gate, a separate owner decision.

## 6 · Scope fence and stop conditions

**In:** the stage A audit, the two skills, the `PENDING_MOVES` drain, the size report, and any gate
stage A rules cheaper than prose. **Out:** changing what any rule *means* · retiring a rule on your
own judgement — flag it · the ck182 dissolution · setting skill caps.

**Stop and report if:** stage A's remainder is empty or near-empty (that is a finding, not a
failure) · a `PENDING_MOVES` row cannot be completed without a ruling · a duty appears to need a
gate that would be expensive or unreliable · the tree is dirty or a peer is mid-flight in a target
file · doccheck is RED before you start · anything that looks like an owner decision, including
where a rule is filed.

## 7 · Required — the revisit trigger, because provisional becomes permanent

The owner authorised these skills as a **first cut to be revisited in the later skills/rules audit**
(`.claude/SEAT_WORKLIST.md` V6). ⛔ **A provisional artefact with no recorded expiry becomes
permanent by default** — this tree currently carries three live `TEMPORARY` markers, all of which
were going to be temporary.

⇒ **Record, in the report, what would make each skill wrong**, since the A/B method is unavailable
(§2). Use failure modes that leave traces in git and need no control arm:
- a commit that edits `CLAUDE.md` without `AGENTS.md`;
- a prompt file added or removed without its `prompts/README.md` row, **or a row whose content no
  longer describes its file**;
- an INDEX hand-edited rather than regenerated;
- content that leaked back into a doc it was drawn from.

Each is `git log`-detectable after the fact. That is the honest replacement for the A/B, and it is
what the later audit will judge against.

## 8 · What may NOT be claimed

- ⛔ Never claim a duty is gated without naming the check **and** showing its output.
- ⛔ Never claim a gate covers a duty when it covers something narrower — the `PROMPT MAP` case is
  the worked example of exactly that error.
- ⛔ Never claim a skill will be read. Nothing verifies invocation; §6 is explicit that the goal is
  loud failure, not prevention. Say so in the report in your own words.
- ⛔ Never claim a `PENDING_MOVES` row is done until its content is in the destination **and** gone
  from the source.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 9 · Required — a live progress list

One item per commit-and-verify unit: the stage A audit table · each ungated item's
GATE/SKILL/DROP call · `doc-editing` · `prompt-authoring` · one item per `PENDING_MOVES` row · any
gate built · the size report · the revisit trigger · the report · the consume. Keep exactly one in
progress; expand a stage in place if it is more units than this brief anticipated. The owner reads
this list to decide when to step in.

## 10 · Done when

The stage A table exists and every row names a verified check or a GATE/SKILL/DROP call · both
skills exist, mirrored to `.agents/skills/`, carrying **only** ungated content · every
`PENDING_MOVES` row is either drained in both directions or still PENDING with a reason · the five
skill sizes are reported with proposed caps and a rationale, and **no cap is set** · the revisit
trigger is recorded · `doccheck` GREEN at every step · one commit per unit so each reverts alone ·
executed model recorded (R-G) · this brief and its `prompts/README.md` row both gone, in the same
commit.
