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

## ⭐⭐ THE MACHINERY — owner-agreed 2026-09-14, all of it

Four parts. ⛔ **The marker is mandatory or the rest is for nothing** (owner's words).

### 1 · Every rule carries a marker, and the header does NOT say "rule"

- A rule, anywhere in the repo, is written **`Rule: <the duty>`**, anchored at **line start**.
- The section that collects rules is headed **`Must_Read_Header`** — ⛔ **deliberately without the
  word "rule" in it**, and pointers to it name only that token.

**Why the header naming is load-bearing, MEASURED 2026-09-14:** headings containing "rule(s)" appear
in **66 files**; `^Rule:` appears in **1**. ⇒ Searching for rules by the word *rule* drowns in
scaffolding. **The marker must be absent from everything that talks ABOUT rules.** Line-start
anchoring also keeps quoted rules in prose (this document included) out of the count.

### 2 · ⛔ The tagging is the AUDIT'S OUTPUT, not a find-and-replace

There is no string to find. Deciding which sentences are duties **is** the audit. ⇒ The audit stops
producing a report and produces **a tagged tree plus a coverage manifest**.

⭐ That is strictly better than a report: a report saying "we found N rules" is stale the moment a
peer adds one. **A tagged tree makes the number re-derivable forever** (`rg -c '^Rule:'`) and the
audit never has to be re-run.

⛔ **Two hazards it creates:**

1. **FALSE CONFIDENCE — the dangerous one.** Today the project *knows* it has not audited. After
   tagging, the grep returns a confident number that silently excludes every rule the pass missed.
   That is this project's own *"GREEN is not correct"* failure: fresh is not right.
   ⇒ **The pass records its own coverage, and doccheck gates THAT** — a rule-bearing file absent
   from the reviewed list is flagged. Without it the marker manufactures confidence.
2. **DECAY.** A rule written next week carries no marker unless something requires it — and a rule
   whose only evidence is that it is mostly followed is a habit. See rule 1 below.

### 3 · The gate — one mechanism, two consumers

⛔ An **untagged** rule cannot be detected mechanically; that is the whole problem. What CAN be:

> **a rule-bearing file changed, and its `^Rule:` count did not move** → WARN: *did this change add
> a duty?*

⭐ **This is the same mechanism as ck177's marker gate**, which is RULED but **not built** (no trace
in `tools/doccheck.py`, checked 2026-09-14). **Build once, point it at two things** — which makes
ck177 cheaper rather than more expensive.

### 4 · A rule-creation skill — the owner's four criteria, plus seven

**Owner's four (authority):** rules-about-rules criteria · **the owner must confirm it is a new rule,
not something that merely sounded like a ruling** · where it goes and who needs to see it · must
articulate the danger it solves and show it is repeatable enough to warrant a rule — **if you
cannot, it is not rule-worthy and is likely informational** (⇒ shape **(d)**).

**Added, each earned by a measured case today:**

| # | requirement | the case that earned it |
|---|---|---|
| 5 | ⭐⭐ **An EXPIRY condition — "what would make this stop being true?"** | **Rule 1.** The four criteria above are all ADMISSION tests; nothing removes a rule. Rule 1 died when the project began reproducing field reports with the reporter's mods, and nobody noticed for six weeks **because nobody had written down what would kill it.** Admission-only is how you get a graveyard. |
| 6 | **Ask "what stops this, if not memory?" BEFORE placement** | ⚠️ **Rule 3 passes all four owner criteria** — real danger, repeatable, clear audience — and was still unnecessary, because **structure** enforced it. The four alone would have admitted it. |
| 7 | **A RECEIPT, not a prediction** | Criterion 4 is prospective. The (b) falsifier is retrospective: *has this actually happened?* ⚠️ **Exception that must stay allowed:** `H-03` is pre-emptive and correct. ⇒ The bar is **an incident OR a stated mechanism with its source citation** (`SteamWorkshop.lua:17-22`). "This seems risky" is neither. |
| 8 | **Name the ENFORCER at birth** | House doctrine already says a hazard is a failure not yet converted into a gate. If the honest answer is *"the reader will remember"*, that is a known-failing enforcement and is recorded as such. Rule 1 had no enforcer, which is why its death was silent. |
| 9 | **Born tagged** | `Rule:` + `Must_Read_Header` at creation, or the grep-derivable number decays from day one. |
| 10 | **Quote the owner VERBATIM** | Criterion 2 guards *"he said something that sounded like a ruling."* The mirror failure is real and has a receipt: a peer corrected this seat for widening a genuine rule into *"any TestKit change REDs the tree."* Quoting makes widening visible. |
| 11 | **Duplicate check before writing, BY DUTY not wording** | Otherwise it regenerates the semantic-merge work the audit exists to do. |

⭐ **The skill and the audit are the same criteria pointed in opposite directions** — the audit
applies them retrospectively across ~618 files, the skill prospectively to each new rule. **Write
the criteria once; both cite them**, and the audit's output becomes the skill's worked examples.

⚠️ **The skill cannot stand alone.** Friction on writing rules pushes an agent to write the duty as
ordinary prose instead — an **untagged** rule, which is worse than an unwritten one, because the
tagged count then looks complete. ⇒ It ships **with** the gate in §3, never before it.

### 5 · `STATE_EVICTION` gains a rule sweep — and may NEVER retire a rule

**Host chosen because it already is this decision.** `perma/STATE_EVICTION.md` is *"fired by the
owner whenever doccheck WARNs on STATE.md's size, or on their own call"* — semi-regular by
construction, and already a push/pull "what stays, what goes" pass with an owner gate.

Two new sweeps per run:

1. **Rules with no marker** — candidates missed by the tagging pass or added since.
2. **Rules whose EXPIRY CONDITION has fired** (criterion 5) — the condition is written down, so this
   is checkable rather than a judgement call.

⛔⛔ **THE EVICTION MAY NOT RETIRE A RULE. It ELEVATES to the owner, who rules.** Owner ruling
2026-09-14. ⭐ Exact house precedent: **ck178** — *"⛔ It ends on the owner's word, not on a
measurement, and no agent retires it on its own judgement."* Same shape; this is consistent, not new.

⚠️ **Bound the elevation, or it will be ignored.** Owner attention is the scarce resource. A sweep
that surfaces forty rules per run is useless. ⇒ **Ranked, small, receipt inline, one-line
disposition each** — the shape of ck178's self-printing line, not a wall.

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

⛔ **SETTLED 2026-09-18, the opposite of what the drift above pointed toward — owner ruling:**
*"agents check saves only when the owner asks — most of the time they are wrong anyway."* The habit
this section found is not promoted into a rule; agent-initiated scanning of the owner's saves is cut
outright, not homed.

## Scope note

⛔ This is a placement test, not a licence to delete. Every disposition above moves a rule to a
cheaper home or shows it was already enforced elsewhere; **none of them removes an actual
protection.** The `F104` case removes a rule that was never protecting anything.
