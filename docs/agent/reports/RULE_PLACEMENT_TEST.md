# The rule-placement test — owner design session, 2026-09-14

Derived with the owner while tearing down `PLAYTEST_HELP.md`'s "Ground rules". Serves **A2**
(minimal always-loaded rules) and **A3** (rules live with their task), checklist **179**/**181**.

## ⭐⭐ The question to ask of every rule

> **What actually stops this, if not the reader's memory?**

⛔ Not *"is this important?"* — importance is why the doc grew. The answer to this question
places the rule, and usually deletes it.

| answer | disposition |
|---|---|
| **Structure** — the reader cannot perform the action at all | **delete the rule** |
| **A guard** — a machine already catches it | **one-line pointer** to the gate |
| **Nothing, and it has been violated in practice** | ⛔ **it was never a rule.** It is a wish. |
| **Nothing, and it binds exactly one job** | **that job's skill or brief** |
| **Already a recorded fact with a canonical home** | delete the prose, keep the fact |
| **Nothing, binds every session, no guard is possible** | the minimal always-loaded set — ⚠️ this list should be very short |

## The worked example that produced it — "Ground rules", 3,900 B

| # | rule | what actually stops it | disposition |
|---|---|---|---|
| 1 | NO third-party mods | ⛔ **nothing, and it has been violated** | **DEAD** |
| 2 | Both mods enabled except PT-20 | nothing — it is a rig fact, not a rule | with the leg that needs it |
| 3 | TestKit must NEVER be uploaded | **structure** | **delete** |
| 4 | Achievements stay ON / cheat taint | already a fact ×5 | keep the facts, cut the prose |
| 5 | No live UI-internals prototyping | nothing, but it is rare and is a lesson | pull-only |
| 6 | "If setup fails, write that down" | nothing, and it needs no saying | **cut** |
| 5a | Warmed-up-save default | nothing — binds **rider authors only** | one line to the prompt-authoring skill |

⇒ **3,900 B reduces to a single line in a skill.** Nothing in "Ground rules" was a rule that
needed a reader to remember it.

### ⛔ Rule 1 is the one that should worry us — MEASURED

*"NO third-party mods. Not ChoGGi's library, not anything else."*

- **It was broken**, on the record: [`bugs/F104.md:64`](../bugs/F104.md) —
  *"Log `Mars.exe-20260823-22.05.52-6a22b86d`, **all six mods + TestKit loaded**"*.
- **The breaking was correct.** Reproducing a reporter's bug requires the reporter's mods. The
  owner adds them, the leg runs, the owner removes them.
- ⭐ **`F104` is the project's cleanest field closure** — cause derived, reply posted, reporter
  confirmed, issue closed.
- ⛔ **No agent ever flagged it.** A search of `F104`/`F105` for any violation framing returns
  **zero**.

⇒ **A rule sat in a doc for six weeks, was broken in the most important field leg the project has
run, and nothing noticed — because nothing was ever going to check.**

⭐⭐ **This project gates module counts, marker integrity, prompt-map freshness and byte budgets,
and has NO gate that asks "is this rule actually being followed?"** That is the real finding.
**An unenforced rule is indistinguishable from a deleted one, except that it still costs every
agent that reads it.** The owner had never read the doc containing it.

### Rule 3 is the instructive one — the protection was never compliance

*"The Test Kit must NEVER be uploaded anywhere — not Workshop, not Paradox Mods, not the public
repo release."* Three surfaces, MEASURED 2026-09-14:

- **The portals** need the in-game mod editor and the owner's hands. ⛔ No agent can.
  (⚠️ `H-03` separately covers console-touching-a-portal-API; that hazard is real and unrelated.)
- **The pack** cannot reach it — TestKit is a **sibling directory**, not inside the pack tree.
- **The public repo release** — the ONLY agent-actionable surface — and
  **`git remote -v` in the TestKit repo is EMPTY.** One local branch, `master`. There is nowhere
  to push it.

Nothing in `metadata.lua` or `tools/upload_preflight.py` mentions TestKit, **because nothing needs
to**. ⇒ **The rule was written as if compliance were the protection, when structure was.** That is
precisely why it reads as necessary and is not.

## ⭐ Audit criterion, owner 2026-09-14 — rules that should not be rules at all

> *"Look for rules that look like they shouldn't even be rules. Either because it's beyond what an
> agent could even do, or something an agent would never do via its programming."*

Three distinct shapes, and **they do not get the same disposition**:

| shape | meaning | disposition |
|---|---|---|
| **(a) CANNOT** | the action is structurally impossible for the reader | **delete the rule** — e.g. Ground rule 3, TestKit upload: no remote exists |
| **(b) WOULD NOT** | possible, but contrary to how the agent operates | ⛔ **incident check REQUIRED before cutting** — see below |
| **(c) WRONG READER** | the actor is not the doc's audience | **move it**, do not delete — e.g. Ground rule 1: only the owner installs mods |

### ⛔ (b) is the branch that can delete an EARNED rule — it needs a falsifier

**The discriminator is not "would a well-behaved agent do this?" It is "has this actually
happened?"** A rule can look exactly like something no careful agent would ever do and exist
precisely because one did.

**The worked counter-case, from this project:** *"⛔ Never `git checkout --` as a restore."* That
reads as gratuitous — no careful agent would restore from HEAD in a falsification harness. **An
agent here did, and it silently destroyed an uncommitted rewrite** (`HANDOFF_PROMPT.md` §6, four
instrument failures in one session). Cutting that rule as a (b) would delete a receipt.

⇒ **Falsifier, run it on every (b) candidate:**

- **A recorded incident exists** → **KEEP.** The incident is the justification, and it should stay
  attached.
- **No incident and no guard** → **cut.**

⭐⭐ **This makes the doc's rule-plus-incident habit FUNCTIONAL, not decorative.** The
`FIX_POLICY` characterisation argued the pairing is plausibly *why* the rules stick; under this
criterion it is stronger than that — **the receipt is the proof the rule was earned.** ⇒ The audit
gets a mechanical first pass: **every rule carrying neither an incident nor a guard is a
candidate.**

### ⚠️ Calibration, and an instrument warning

Sampled 2026-09-14 across `CLAUDE.md`, `WORKFLOW.md`, `FIX_POLICY.md` and `perma/`: two keyword
passes for the *"never fabricate / never lie / be honest / never skip"* genre returned **one** hit
(`perma/SMRTK_SLOTS.md:56`, *"ids, handles, session nonces and game time are variables, never
invented literals"* — and that one is **earned**: an agent holding a nonce from a previous session
will hardcode it).

⇒ The (b) yield here looks **small**, and the criterion may be worth more **preventively** — as a
filter on rules as they are written — than as a harvest from what exists.

⛔ **But two greps do not bound a class defined by MEANING.** A (b)-shaped rule need not contain
any of those words. **The audit must READ for this, not grep for it**, and must not report a small
yield as a measured one.

## ⭐ Three more audit requirements, owner 2026-09-14

### (d) A rule that is actually just INFORMATION — a fourth shape

> *"If a rule is actually just information that's useful to know but shouldn't be a rule and
> belongs somewhere else."*

| shape | test | disposition |
|---|---|---|
| **(d) NOT A RULE** | it requires no action of the reader — it is a fact or a lesson written in the imperative | **engine fact → `facts/EF-*`** · **lesson → pull-only reference.** Never the always-loaded set. |

Worked cases from the Ground-rules teardown: rule 2 (*"both mods stay enabled"* — a rig fact),
rule 4 (*"achievements stay ON"* — already five `EF-*` files), and the bulk of 5a, which the owner
called *"informational info not rule info."*

### ⛔ Duplicates must be found by MEANING, not by string

> *"Don't have it look for just duplicate rules, because we could have duplicate rules with
> different names that are in fact saying the same thing."*

The existing inventory found **14 redundancy pairs**, and the ones verified in the `WORKFLOW`
characterisation were **near-verbatim** (`R2` doccheck-before-commit, `R3` owner-decision
mirroring, both against `CLAUDE.md`). ⇒ **Semantic duplication was never sought.**

⛔ **Cluster by WHAT THE RULE REQUIRES OF THE READER, not by its wording or its name.** Two rules
naming different artifacts, in different docs, under different headings, can impose the same duty.
A hash/grep pass cannot see that; it is a read job. ⚠️ The inventory's own `count_unit` says it
**splits** rather than merges: *"Duplicate and dead clauses separated when adjacent live duties
differ."*

### ⛔ "Every rule in the repo, and a number" — the existing 852 does NOT answer this

MEASURED 2026-09-14 against `reports/RULES_HEADERS_INVENTORY.json`:

| | |
|---|---|
| entries | **852** |
| files covered | **22** — `CLAUDE.md`, `README`, `STATE`, the 4 monoliths, `UPLOAD_WORKFLOW`, the 14 `perma/` prompts |
| classes | global 16 · task-local **780** · redundant 20 · doc-local 30 · dead 6 |
| its own `count_unit` | *"Verbatim imperative occurrence or inseparable same-scope rule group… **Counts are not unique policies or atomic predicates.**"* |

**Three reasons it cannot be quoted as the answer:**

1. ⛔ **Wrong unit — by its own declaration.** 852 is occurrences/spans. The `WORKFLOW`
   characterisation measured the gap directly: **10 JSON entries = 7 distinct rule-texts**
   (R-A's paragraph counted as 4 sub-spans). *A total is not a set.*
2. ⛔ **Wrong scope — 22 of ~618 rule-bearing files.** Never opened: `bugs/` 195 · `reports/` 197 ·
   `facts/` 103 · `tools/*.py` 56 · non-`perma/` prompts 39 · **skills 4** ·
   `metadata.lua`+`items.lua` 2. ⚠️ Not all carry duties — most bug entries carry evidence — but
   some do. **Proof:** `items.lua:204`, *"a module absent from this file SHIPS ABSENT"* — a rule
   with a player-visible consequence, living in a Lua comment. ⭐ And **the skills are the only
   rule-carrier in this project with a cross-vendor gate**, yet they were not inventoried.
3. ⛔ **Not deduplicated by meaning** — see above.

⇒ **Report TWO numbers and say which is which: occurrences, and distinct rules after semantic
merge.** Quoting one without the other is the defect this project already named.

### ⭐⭐ Why the existing inventory could not have answered any of this

**It asks "where should this rule live." It never asks "is this a rule."** Its five classes are
all placement — global, task-local, doc-local, redundant, dead. There is no class for *cannot*,
*would not*, *wrong reader*, or *not a rule at all*, which is why **780 of 852 landed in
"task-local" and the pass moved on.**

⇒ ⛔ **The audit must NOT inherit the 852's classifications.** Placement is the second question.
The first is existence.

## ⚠️ The inverse case — a habit wearing a rule's clothes

The same session found the opposite failure. The owner assumed that an agent setting up a playtest
**scans the existing saves to find a suitable one**, rather than asking for a new fixture.

- The **facts** exist: 7 `EF-*` files cover savegame metadata, cheat taint, branch-lock, `CheatsUsed`.
- Agents **have** done it — sitting 08's fixture was chosen 2026-09-14 by reading `CheatsUsed` off
  disk against a tainted positive control.
- ⛔ **No standing prompt requires it.** `perma/COMBINED_SITTING.md`'s fixture material says of
  itself: *"written for these fixtures and are now history, not a template."*

⇒ **It happens because individual agents did it, not because anything requires it.** A session that
does not think of it will ask the owner to build a save they already have.

⭐ **Rule 1 and this are the same defect from opposite ends:** the project cannot tell a rule from a
habit, in either direction. ⇒ **A rule needs the "what stops this" answer BEFORE it is written**,
and the answer "the reader will remember" is the one that never holds.

## Scope note

⛔ This is a placement test, not a licence to delete. Every disposition above moves a rule to a
cheaper home or shows it was already enforced elsewhere; **none of them removes an actual
protection.** The `F104` case removes a rule that was never protecting anything.
