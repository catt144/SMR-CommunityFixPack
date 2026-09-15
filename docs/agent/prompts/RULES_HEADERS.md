# RULES_HEADERS — inventory every rule, restyle the corpus to one format, put the doc-local ones in a header, and land the kernel rule in CLAUDE.md

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

Authored against **HEAD `a6726b5`**; **REVISED 2026-09-15 against `d28c781`** for the owner's
rulings of that date — see §2's governing block, which overrides anything above it where they
differ. ⚠️ Five-plus interactive peers share this checkout under
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

## 2 · The job — five stages

### ⭐⭐ GOVERNING BLOCK — owner rulings 2026-09-15. These OVERRIDE anything earlier in this brief.

Recorded in full at `.claude/DECISIONS.md` rows 4, 8 and 9, which are the register; this is the
operative summary. ⚠️ The brief below was written before these and was amended only in the places
they touch — where an older passage and this block disagree, **this block wins**.

**1 · The corpus is NOT grandfathered.** Every existing rule is restyled to one format and
re-tested against the same criteria a new rule would face. This is the one-time deep pass; the
ongoing `STATE_EVICTION` sweep is a separate, deliberately cheap thing and none of this belongs
in it.

**2 · The kernel is `CLAUDE.md`, and `STATE.md` goes to ZERO rules.** Ruled in checklist 179
(`ck179` B1) and specified in `reports/DOC_RULES_ARCHITECTURE.md` §1/§3/§4. ⛔ This brief was
written against an older design in which `STATE.md` was the kernel, and stages A and D still
carried that routing on 2026-09-15. **Global rules move to `CLAUDE.md`. The meta-rule lands in
`CLAUDE.md`. `STATE.md` ends this job carrying no rules at all** — it is a kernel of status,
pointers, holds, owes and the counts block. ⚠️ Also ruled and NOT yet done by this brief:
`WORKFLOW.md`'s **10 global rules move into `CLAUDE.md`**. `DOC_RULES_ARCHITECTURE.md` §3 calls
that *"the single largest adherence win available here."*

**3 · YOU determine the writing style and format.** Owner: *"I want it to determine the style and
format, what it determines is the best format. I don't want there to be emojis in the rules
though, my only guideline."* ⛔ **No owner sign-off gate on the style** — do not ask for one. The
single constraint is **no emoji inside a rule**. ⚠️ State your format decision and the reasoning
for it in the report *before* applying it: a wrong call must stay diagnosable without
reverse-engineering it from the corpus.

**4 · Latitude — the test is whether an operation PRESERVES WHAT BINDS.** Filing is mechanical;
existence is a ruling.
- ✅ **Free, no ask:** move a rule to its correct home (the tier map, `DOC_RULES_ARCHITECTURE.md`
  §1 — "correct" is mechanical, defined by *when it loads*, not by taste) · delete a duplicate
  from a surface that should not hold it (*"the rule should have one home not dozens"*) ·
  restyle · split a numbered item carrying several clauses into one rule per item · repair a
  stale pointer where the rule is live but its target moved.
- ⛔ **The owner's, always:** a rule that fails the criteria is **FLAGGED, NEVER RETIRED**. So is
  a rule whose entire subject is gone, and an echo carrying **scope the home rule lacks** — a
  different rule wearing the same words.
- ⚠️ **Every deletion must name its survivor** (file and line). Dedupe is only dedupe if a copy
  is provably left standing; without the survivor named, "remove from the wrong surfaces" is
  retirement-by-agent through the side door.

**5 · YOU ARE EXEMPT FROM THE RULE CORPUS.** Owner: *"we are changing the way the rules are
formatted and established. By definition it is exempt from all rules, otherwise it cannot do a lot
of its work. It can organize to spec and alter anything it needs to alter to bring us into the new
spec."* ⇒ No existing doc-editing convention blocks you. ⚠️ Two limits, because they are not
conventions: **existence stays the owner's** (item 4), and **nothing whose breach damages the tree
for people outside this job** — `CLAUDE.md` drifting its generated `AGENTS.md`, a doccheck RED left
standing, `docs/archive/`'s append-only boundary. ⭐ `CLAUDE.md:30-32` is **not** exempt from
restyling; it is restyled with everything else.

**6 · Delivery is a REPORT IN TWO HALVES, and the owner reads one.** The sweep never asks
in-session and neither do you.
- **Done** — the mechanical work, as counts plus a diff, each deletion naming its survivor.
- **Asks** — the flagged ones, ⭐ **batched by QUESTION, not by file.** Forty rules raising eight
  distinct questions is **eight** asks with their members listed, not forty. This is the entire
  point of batching and it only happens if it is required.

**7 · Push-set budget is a live constraint.** `CLAUDE.md` and `STATE.md` are both in it and it is
already **OVER**. Re-derive it (`python tools/doccheck.py | grep -A6 'PUSH SET'`), report the
**net** effect of your moves, and land no move that pushes it further over. Moving rules out of
`STATE.md` shrinks it; moving globals into `CLAUDE.md` grows it; the sum is what matters.

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
| **global** | binds every session regardless of what it opens | the kernel — ⚠️ **`CLAUDE.md`, NOT `STATE.md`**; see §2's governing block item 2 |
| **redundant** | the same rule is stated in 2+ places | one canonical home; the copies become pointers or go |
| **dead** | it names a file, tool, process or state that no longer exists | proposed for deletion |

⛔ A **pointer** to a rule is not a duplicate — leave pointers alone. A **local specialisation**
("in this doc, rule 5 also means…") is not a duplicate either. Only report genuine restatements,
and quote both sides so a reader can judge the call rather than trust it.

⚠️ Expect `dead` to be non-empty and do not treat a small count as failure. The prompts map was
**55% records of prompts that no longer existed** when it was checked on 2026-09-13, and nothing
cited any of them.

#### ⭐ A2 — this pass is also the CENSUS, and it is the only one there will be

⛔ **We do not have an enumeration of the current rules, only a sample.**
`reports/RULES_HEADERS_INVENTORY.json` covered **22 of ~618** rule-bearing files and never
deduplicated by meaning. ⛔ **Do not inherit its 852** — it counts occurrences by its own
`count_unit`, and 780 of the 852 landed in one class, which is a symptom of the instrument.

⚠️ It is circular by construction: rules cannot be grepped until they are marked, and cannot be
marked until they are found. It resolves one way only — **this stage IS the census.** Everything
downstream, the standing check included, is complete only for what this pass finds. ⇒ State the
boundary of what you swept in the report, in your own words. A census that looks complete and is
not is worse than one that says where it stopped.

⚠️ **Rule-shaped prose carrying no marker** needs a detector, and it will be heuristic. It belongs
here, once — ⛔ **never in the ongoing sweep**, and it must be **WARN, never RED**.

#### ⭐ A3 — re-test every rule against the criteria, and record the verdict

Owner: *"all current rules we have should also have to pass our new rules test for creating a
rule."* ⇒ The definition at the head of this stage is that test. Apply it to **existing** rules,
not only to the idea of new ones.

⛔ **You do not decide rule-ness — you decide whether it is OBVIOUS.** A rule that plainly passes
is recorded as passing. A rule that plainly fails, or that you are unsure about, is **flagged for
the owner** per the governing block item 4. ⚠️ The report's Asks half is exactly this set, batched
by question.

⭐ **Record each verdict with the rule**, because that record is what lets the ongoing sweep stay
cheap: the sweep then checks that a verdict EXISTS — a grep — instead of re-deriving the judgement
behind it. A rule carrying no verdict is the sweep's WARN, and that is what makes the ongoing
batch process enumerable rather than open-ended.

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

#### ⭐ RESOLVED 2026-09-15 — seven is a COUNT, not a CEILING, and the trigger is uniform

⛔ **This brief stopped here once already.** `reports/RULE_PLACEMENT_TEST.md` states the
owner-agreed machinery as *"a rule, **anywhere in the repo**, is written `Rule: <the duty>`"*
under a `Must_Read_Header`; this section says seven docs. **Both stand, and here is how.**

**Owner, 2026-09-15:** *"a future doc could get a rule but when it doesn't have a header already,
an agent authoring a rule that is probably just for that doc sees no header, so it adds the doc
rule to the unified rule list every agent needs to know. I am fine doing the 7 but as a trade the
skill needs to pick up the slack: if a doc gets a rule that doesn't have a header, then the header
needs to be created."*

⇒ ⭐ **The absence of a header is not neutral — it is a gradient that promotes doc-local rules into
the kernel**, because an agent with a rule and no local home files it in the one list it knows
exists. That is kernel inflation arriving through a gap rather than through a decision.

**The rule, and it is uniform by design:** ⛔ **a doc that holds a doc-local rule gets a header —
whoever notices first.** ck179's own wording is *"the docs carrying a genuinely unique rule"*,
which is a **criterion**; seven is what that criterion produced against the sixteen proposed docs,
before any census existed. So:
- **You, at census time:** if stage A2 finds a doc-local rule in a doc outside the seven, that doc
  earns a header. ⚠️ **List every doc you add and why, in the report's Done half.** Seven remains
  the count as of the census, and it is not a ceiling.
- **The rule-creation skill, thereafter:** a new rule in a headerless doc means the header is
  created then. ⚠️ **That skill does not exist yet** — build the repo-wide WARN in stage D so the
  gap is covered until it does.
- ⭐ Creating a header is **filing, not an existence ruling**, so it sits in the free tier of the
  governing block's item 4. No new authority is needed for it.

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

### ⭐ B2 · Determine the writing style, state it, then restyle the corpus to it

**NEW 2026-09-15 — this stage did not exist when the brief was written.** It is yours to decide;
see the governing block item 3. There is no owner gate on it.

**Decide and state, before applying:** the canonical shape of a rule line · how the `Rule:` marker
sits in it (the machinery requires `Rule: <duty>` at line start under a `Must_Read_Header` whose
own wording omits the word "rule") · what grammatical form a duty takes · what a rule may not
contain. ⛔ **No emoji inside a rule** — the owner's one guideline, and the only fixed constraint.

⭐ **Choose a form that a machine can check**, because stage D has to check it. The more of the
style that is expressible as a pattern, the more of this survives contact with future sessions.
⭐ **And choose a form that makes two statements of one duty CONVERGE on the same text** — that is
what the style is *for*. Free-prose rules drift, so two statements of one duty never match and
every dedupe becomes a judgement call; canonical rules match exactly, and dedupe becomes a grep.

**Then restyle every rule the census found**, under the exemption in governing block item 5.
⚠️ Restyling is meaning-preserving or it is not restyling: if a rule's duty would change to fit the
format, that is a **re-wording** — list it separately in the report with before and after quoted,
exactly as stage C requires for moves.

⚠️ **`CLAUDE.md:30-32`** (trust-by-source clause 3) is restyled like everything else. Its *duty* is
an open owner decision (`DECISIONS.md` row 8) — its *phrasing* is not, and a meaning-preserving
restyle does not touch the open question. Do not treat the open row as a reason to skip it.

### C · Land the headers and the moves — with the latitude in the governing block

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

- **One line in `CLAUDE.md`** — ⚠️ **NOT `STATE.md`; see the governing block item 2.** Read the
  rules header of any doc you are about to edit. ⛔ One line. This rule earns kernel bytes **only**
  because it replaces many. ⛔ `CLAUDE.md` has a byte-identical generated mirror: edit it and run
  `python tools/doccheck.py --regen` **in the same commit**, or doccheck goes RED for every peer.
- ⭐ **And `STATE.md` finishes this job carrying ZERO rules.** Its own line 3 reads *"Kernel only:
  status + pointer, never derivation"*, and the inventory found ~30 rule occurrences in it —
  which is also why it keeps pressing its cap. Every one leaves for its tier. Status, pointers,
  holds, owes and the counts block stay.
- **A doccheck check in TWO PARTS, with different scopes — owner ruling 2026-09-15.** ⛔ Conflating
  them is what stopped this brief mid-flight; keep the scopes distinct when you build it.
  1. **The header-block check**, scoped to **the approved list**, **RED**: the block exists, both
     markers are present and correctly ordered, and it is within cap. A structural check the
     machine can hold.
  2. ⭐ **The rule-placement check**, scoped **REPO-WIDE**, **WARN, never RED**: a `Rule:` line
     must sit under a `Must_Read_Header`. ⚠️ **This is the load-bearing half and it exists for one
     failure mode:** a doc that holds no header gives an agent with a doc-local rule nowhere local
     to put it, so the rule goes into the kernel list every session reads. **Absence of a header
     silently promotes doc-local rules to global.** This WARN is what catches that the moment it
     happens.
- ⭐ **The style checks, cheap because they run on every commit:** **no emoji on a `Rule:` line**
  (the owner's guideline, and a one-line regex) · the rule conforms to your stage-B2 format so far
  as that format is machine-expressible · its surface is permitted by the tier map ·
  ⭐ **no two surfaces carry the same canonical rule text** — this is dedupe becoming a machine
  check, and it is the payoff the style was ruled in for.
- ⚠️ **The check asserts ADJUDICATION, not rule-ness.** No gate can decide whether something *is*
  a rule. It can assert that stage A3's verdict exists, and WARN where it does not. Build it that
  way; do not build a gate that pretends to judge.
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
| ⛔ ~~`STATE.md` **12,176 B**, warn **12,288**~~ — **STALE, superseded**: 12,930 B, warn 15,360 TEMPORARY | doccheck STATE + STUBS | re-measured `d28c781` | `python tools/doccheck.py \| grep 'STATE + STUBS'` |
| push set **42,602 B** against a **40,960** budget — already OVER | doccheck PUSH SET | `d28c781` | `python tools/doccheck.py \| grep -A6 'PUSH SET'` |
| the line-1 banner precedent exists on 3 files | `head -1` each | `a6726b5` | `head -1 docs/agent/bugs/INDEX.md docs/agent/facts/INDEX.md docs/WAITING_ON_YOU.md` |

⛔ **The "~112 bytes of headroom" this brief was built on is GONE as a premise — re-derive before
reasoning.** Measured 2026-09-15 at `d28c781`: `STATE.md` **12,930 B**, warn **15,360**, hard
**18,432**. The warn was raised +25% by owner ruling (checklist 178) **and is marked TEMPORARY**,
so the headroom is real today and is not a thing to spend. ⚠️ The affordability argument this
paragraph used to make no longer applies in the same shape: stage D no longer adds a line to
`STATE.md` at all (governing block item 2 — the meta-rule lands in `CLAUDE.md`), and `STATE.md`
is emptied of rules rather than trimmed.

⇒ **What to report instead:** `STATE.md`'s byte change from evicting its ~30 rule occurrences,
`CLAUDE.md`'s byte change from receiving the globals and the meta-rule, and **the net push-set
effect of the two together** (governing block item 7). ⛔ Do not compress lines to fit
(`WORKFLOW.md` rule 8: evict, don't compress), and do not trip a warn silently.

⚠️ **`STATE.md` holds still for the duration of this job** — the documentation seat owns it, so
that this before/after is attributable to this job and not to concurrent growth from another tree.
Take its byte count and sha at the moment you start.

## 5 · Scope fence

**In:** the corpus in §3, the inventory **and census**, the **style you determine and the restyle
of every rule to it**, the header spec, the migration **under the latitude in the governing
block**, the kernel line **in `CLAUDE.md`**, emptying `STATE.md` of rules, moving `WORKFLOW.md`'s
10 globals, and the doccheck check. **Out:** changing what any rule *means* · **retiring** a rule
on your own judgement — flag it instead · deleting a duplicate **without naming its survivor** ·
`docs/archive/` · the checklist below its preamble ·
the open marker-gate question in checklist **177**, which is a separate owner decision and must
not be folded into this job. Anything interesting outside §2: **file it, do not fix it.**

## 6 · Stop conditions — permission, not failure

Stop and report if: a rule's meaning would change to fit a header **or to fit the style** · two
rules genuinely conflict (report both, resolve neither — a conflict is an owner decision) · the
push set would end further over budget than it started (governing block item 7) · `STATE.md`
changes under you from another tree while you are measuring it · the tree is dirty or a peer is
mid-flight in a target doc · doccheck is RED before
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
doc (one item each) · classification · **the census boundary** · **the A3 rule-test verdicts** ·
redundancy pass · dead pass · header spec · **the style decision, stated** · **the restyle, one
item per doc** · one item per doc migrated · **`STATE.md` to zero rules** · **`WORKFLOW.md`'s 10
globals into `CLAUDE.md`** · the kernel line · the doccheck check · **the report's two halves** ·
the consume. ⛔ There is no owner gate in this list any more — the old one is discharged and the
style carries none; the owner reads the **report**, not a blocking checkpoint. Mark each complete the moment it completes, keep exactly one in
progress, and expand a stage in place if it turns out to be more units than this brief
anticipated. The owner reads this list to decide when to step in.

## 9 · Not applicable, stated rather than omitted

**Element 7 (stale-probe gate) does not apply** — no game boot, save, module or shipped Lua.

## 10 · Done when

⛔ The old OWNER GATE is **discharged** and the style carries none — see the governing block.
What the owner receives is the **report**, not a blocking checkpoint.

The inventory exists as `reports/RULES_HEADERS.md` with counts per class and per doc that
**reconcile against their own members**, and with **the census boundary stated** · the style
decision and its reasoning are stated **before** the restyle appears in the diff · every rule
carries an A3 verdict, and every rule without one is in the Asks half · the Asks half is batched
**by question, not by file** · every deletion names its survivor · every approved doc carries a
conformant header within cap · every moved rule is byte-identical somewhere in the tree ·
**`CLAUDE.md` carries the one new kernel line, `WORKFLOW.md`'s 10 globals, and its `--regen`'d
`AGENTS.md` mirror in the same commit** · **`STATE.md` carries ZERO rules** · the **net push-set
effect is reported and is not further over budget** · doccheck's `RULES HEADERS` check is live and
was **watched to fail** on a broken copy and restored by hash · `doccheck` GREEN at every step ·
one commit per source doc so each reverts alone · executed model recorded (R-G) · this brief and
its `prompts/README.md` row both gone, in the same commit.

The report states, in its own words, what the structural check cannot verify.
