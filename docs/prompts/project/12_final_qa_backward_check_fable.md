# Chain 12 — FINAL QA: the backward check over everything (run LAST)

**One-off; deletes this file AND `README.md` in its final commit — the
folder must end EMPTY. Read `README.md` first; its exclusion list is part of
your evidence.** Gate: this folder contains only this file + README. If any
numbered prompt remains, the chain is not done — stop and say which.

**Staleness check: `git log --oneline -10` + `git pull`.**

## The job — check BACKWARDS, trust nothing forward

You verify that the chain (and the two big efforts it drained — the
2026-08-01 bug-list audit and the F86 adjudication-through-build arc) left
nothing missed, pending, or wrong. You are adversarial: every "done" is a
claim; sample the evidence, not the assertion (this project's recorded facts
have been wrong before — `recorded-facts-are-claims` is a standing lesson).

### ⭐⭐ JOB 0 — DO THIS BEFORE ANYTHING ELSE: re-verify the "OFF is three different things" doctrine, then sweep on the result (OWNER-REQUESTED 2026-08-01, verbatim: *"We cannot be wrong about this"*)

**Why it is job 0 and not job 8:** its answer changes what the rest of your QA is
checking, and it **re-sizes D13**. If the doctrine holds, the cleaner's target
population is not "players who used a module" but **every player who ever had the
pack installed, whatever their toggles** — which is a different amount of launch
work. The owner asked for this specifically because of that.

**THE CLAIM UNDER TEST** (recorded 2026-08-01 in `ENGINE_FACTS.md` "OFF" IS THREE
DIFFERENT THINGS, `FIX_POLICY.md` §5 last bullet, `WORKFLOW.md` per-fix step 4;
commits `b9c4107`, `a5d4b89`, `227366a`):

> A **Mod Options toggle** leaves the module's hooks installed and the mod env
> present, so it keeps seeding frames into saves and a captured frame merely
> no-ops. Only **Mod-Manager-disable / removal** takes the env away and orphans
> what was seeded. Therefore **a toggle-off reload cannot answer an uninstall
> question — it reads clean by construction.**

**Split it before you test it. Do not verify it as one lump.**

| # | sub-claim | status as recorded | what you must do |
|---|---|---|---|
| **A** | `Opt_DroneOverhaul` leaked into saves at **98 errors/session with its own Mod Options toggle OFF** | claimed **MEASURED** — this is the load-bearing fact and *everything* rests on it | **Go to the primary evidence** — the original log and the first Site 2 entry, NOT a restatement. Confirm the toggle really was OFF. ⛔ **If it was actually ON, the whole doctrine collapses** and `b9c4107`/`a5d4b89`/`227366a` must be reverted. `recorded-facts-are-claims` applies with full force here |
| **B** | Mod-Manager-disable ≡ real uninstall | claimed **MEASURED** (98 vs 98, same save; PT-20 procedure note) | confirm from the log, not the note |
| **C** | A captured frame, loaded with the pack present but the module toggled OFF, **resumes and no-ops cleanly** | **INFERRED ONLY** — read off `module_active()`/`SMRFixPack.IsActive` (`00_Core.lua:39-42`), never observed | say so plainly. ⚠️ The natural instance was Site 2 and it is **repaired**, so this control may no longer be constructible from our own code. **If it is not, that IS the finding**: the doctrine rests on a historical measurement nobody can re-take. Do not paper over it |
| **D** | The `SMRFixPack_Disabled[id]` veto prevents capture for apply()-time installers but **NOT** for file-scope installers | **INFERRED** from `Register` returning before `run_apply` (`00_Core.lua:384-388`) | **Deliverable: enumerate every module in `Code/` as FILE-SCOPE or APPLY()-TIME installer.** That table decides what each off-switch actually removes, and D13 needs it |

**THEN THE SWEEP — only if A and B hold.** The owner asked for *all* documentation,
**including playtest results**:

1. **Void every recorded result whose method was a toggle-reload.** Three were
   found and corrected 2026-08-01 (`227366a`) — `PLAYTEST_CHECKLIST.md` Trigger E
   plus two BUGS restatements — and **all three were unrun, which is luck, not a
   defence.** Hunt the rest, `PLAYTEST_ARCHIVE.md` included. A recorded PASS taken
   that way is **void, not merely weak**: re-label it with why, never delete it.
2. **⭐ The launch-sizing question — this is the one the owner is actually
   asking.** Find every disposition, exposure verdict, "compliant — no work",
   "savegame footprint: none" or "not exposed" call **that leans on a module being
   optional / opt-in / off-by-default**. Under this doctrine every one of them is
   unsound, because off-by-default says nothing about what is installed. Check
   `SAVE_SAFETY_REDESIGN.md` §5.3 and §5.4 in particular: **were the `Opt_*`
   modules swept on their own merits, or discounted for being optional?** Report
   the count and name them.
3. Correct the findings **everywhere they appear** — BUGS entries and index rows,
   STATUS, the checklist, module headers in `Code/`, the reports set. One known
   instance was already struck (D06's *"saves made with it load identically
   without it"*, `a5d4b89`); assume there are more.
4. Feed the result to **D13's entry** as a sizing input, since that is the point.

**What may not be claimed here:** that the doctrine is confirmed, unless sub-claim
**A** was read off primary evidence. That C is measured — it is not, unless you
measure it. That the sweep is complete without saying which documents you searched
and how.

**⭐ THE OWNER HAS PRE-OFFERED THE KEYBOARD SITTING FOR C (2026-08-01, verbatim:
*"If fable needs me to do any work for it to witness regarding our findings I am
more than happy to"*). You do not need to negotiate it — you need to design it
well.** A ready-made proposal, so you are not inventing one under time pressure:

**The difficulty, stated first.** A *discriminating* control for C needs a module
that has a **capturable frame** AND can be made **inactive while the mod env stays
present**. Post-Tier-2 that shape may no longer exist in shipped code — Site 2 was
it, and it is repaired. The layer-2 residuals that remain (`Fix_ShelterReflex`,
`Fix_ArrivalDeaths` (b)) are **non-discriminating by design**: they have nothing
after the call, so they produce silence whether C is true or false. ⛔ **Do not
run a non-discriminating leg and record its silence as a pass** — that is the
exact failure this whole job exists to stamp out.

**Proposed protocol (adapt it, but keep the discriminating property):**
1. A purpose-built **TestKit** probe module that deliberately reproduces the old
   Site 2 shape: a POST-wrapper on a blocking body which, after the call, both
   (a) writes an observable marker and (b) touches a mod-created name. **It MUST
   carry the literal word `TEMPORARY` in its header** (WORKFLOW probe hygiene) and
   be deleted in the same commit that records the answer.
2. Save with it active and frames captured (the drone-Idle population is the known
   lever — PT-58 got 73 by letting the colony settle; hubs-off is the fallback).
3. **Leg 1 — env PRESENT, module INACTIVE.** Load with the fix vetoed via
   `SMRFixPack_Disabled` (pack still installed, env still there). **C predicts:
   the frame resumes, resolves the env, no-ops, ZERO errors — and the marker is
   NOT written.** Silence alone is not the pass; *the marker's absence plus zero
   errors* is.
4. **Leg 2 — env ABSENT (the control that proves the instrument works).** Same
   save, pack disabled in the **Mod Manager**. **Predicts: the frame orphans and
   throws**, naming the probe file. ⛔ **If leg 2 is silent, the probe never got
   captured and leg 1 proved nothing — fix the fixture, do not report a result.**
5. Both legs on one save, one sitting, predictions written before either runs.

**Only leg 2 firing makes leg 1 meaningful.** That pairing is the whole design.

If you conclude C cannot be measured even this way, say so and leave it marked
INFERRED — an honest gap beats a manufactured confirmation.

1. **Inbox audit.** Git history of this folder: every deleted prompt's final
   commit should show its outbox landing in a later prompt or a BUGS/STATUS
   record. Hunt for notes that were written and never consumed, and for
   stop-and-ask items routed here — **resolve or present every one**.
2. **Owed-work sweep.** Grep the living docs (`STATUS`, `BUGS`, checklist,
   `FIX_POLICY`, the two standing prompts) for `owed`, `pending`,
   `blocked`, `gated`, `⚠`, `TODO`, `ask the owner` — classify every hit:
   done (point at evidence) / deliberately standing (name the gate) /
   DROPPED (present to the owner). The deliberate-standing list must match
   README's exclusions plus decisions the owner explicitly deferred.
3. **Consistency pass.** BUGS index rows ↔ heading tags (every one);
   STATUS counts recounted from `Code/` and TestKit, not inherited; the
   checklist references no retired test; probe sweep reads ZERO hits;
   `docs/prompts/` holds exactly the two standing prompts + live one-offs.
4. **Verification sampling.** Pick ≥3 status flips the chain made
   (e.g. Tier-1 entries, an approved audit fix, a D-build) and walk each
   back to its leg numbers in the log/commit — not to the entry's own claim.
5. **The freed state, stated.** Write
   `docs/reports/CHAIN_QA_REPORT.md`: verdict up front (CLEAR or the finding
   list), the standing-item table (owner decisions deferred, D13 + release
   gates as the post-playtest queue, the drone track's own prompt, owner
   web-checks if still open), and **the playtest campaign's current top** —
   what the owner should run first at the keyboard now that they are free.
6. Update `STATUS.md` (chain complete, pointer to the QA report) and
   `FABLE_NEXT_PROMPT.md`'s staleness line.
6b. ⭐ **THE BLIND-AUDIT MERIT EXAMINATION (owner-added 2026-08-02) — run
   AFTER jobs 1-6 and BEFORE job 7, because its findings are job-7
   evidence.**
   ✅ **YOU ARE THE ONLY PROMPT AUTHORISED TO OPEN IT** (owner rule, sealed
   2026-08-02): chain prompts **7-11 are explicitly FORBIDDEN** from reading,
   grepping or acting on `BLIND_AUDIT.md`, each carries a sealed block saying
   so, and it is binding rule 8 in this folder's `README.md`. **Two things that
   places on you:** (a) the independence you are about to test is only real if
   that seal held — so **check each consumed prompt's handoff notes for an
   admission that a broad search surfaced its contents**, and treat any such
   admission as a caveat on the comparison rather than ignoring it; (b) the
   seal is why you must do your own pass FIRST — you are the single point
   where the two readings meet, and there is no second chance at an unanchored
   comparison. `docs/reports/BLIND_AUDIT.md` is an independent two-sweep
   audit of all 66 fix premises, produced by a fresh session that read no
   project docs (sweep 2: ENGINE_FACTS only). Your job: examine its merit
   against the full evidence base it was forbidden to see — the witness
   grades in `BUG_LIST_AUDIT.md` §2/§9/§10, the reachability enumerations,
   the play-proven results — verdict by verdict where it disagrees with or
   qualifies the project record.
   - **Do your own examination FIRST, then open the sealed key below and
     reconcile** (the project's fresh-context-QA pattern: neither reading
     anchors the other). Where you and the key disagree, that disagreement
     is a finding — resolve it on evidence, not deference.
   - Deliverable: an ANNEX appended to `BLIND_AUDIT.md` (do not edit its
     body — it is a record of an independent exam) recording: which verdicts
     the informed record confirms/overturns/qualifies, each with its
     evidence pointer; the entry-record updates that fall out (route or
     make per the scope fence); and its two structural observations
     (§11.3 + closing) handed to job 7 as taxonomy evidence.
   - **The relabel question it raises (F55/F40/F73b/F70: "bug fix" vs
     "behavior change" on the mod page) is an OWNER decision** — package it
     with your recommendation; do not decide it.

   <details>
   <summary>SEALED KEY — the 2026-08-02 informed review's findings (open
   only after your own pass)</summary>

   1. **F29(a): the report's "Mod-Editor sequence action with no shipped
      user" is factually wrong** — the reachability audit enumerated four
      live shipped callers in Mystery 2; this is §4a's own worked example
      of trusting a self-description. Its latency conclusion still matches
      (defaults mask both); only the reasoning is bad.
   2. **The three Contested verdicts were made without witness evidence,
      and two flip with it**: F73(b) — a developer replied in the witness
      thread that they are investigating habitat starvation, undercutting
      "deliberate absence"; F40 — the report graded only the grant filter
      and never enumerated the cure path (the harm is androids-never-cured;
      ChoGGi's years-shipped fix targets it). **F55 is the keeper**: the
      vanilla forever-mark comment is a genuine intent tell our own record
      never weighed — the fix still passes §4 on the player-harm tell
      (GOLD witness), but the entry should carry BOTH tells and the
      judgment explicitly, and the mod-page label is the owner's call.
   3. **F68: the "belt-and-braces for a state the engine may not produce"
      lean conflicts with the GOLD witness set** (TheNightglow's
      steal-cargo report + the dev patch note "Fixed drones endlessly
      moving resources between Landers") — the churn was real. **But** the
      report correctly spotted that the fix file's own 2026-07-28 forensic
      note is in tension with the entry's ratchet-mechanism narrative:
      the fix and its witness stand; the ENTRY's mechanism story needs
      reconciling with its own forensics.
   4. **§11.3 is confirmed** — the ENGINE_FACTS two-headers warning went
      stale within a day of being written and was struck 2026-08-02 (the
      strike cites the blind audit). Its correction-cadence observation is
      direct job-7 evidence.
   5. Endorsed without reservation: the §12 defensible-shortlist; and the
      closing "would a designer have written this on purpose" question,
      which independently reinvents the §4 amendment's intent-first bar —
      convergent validation of the adopted policy.
   </details>

7. ⭐ **THEN, AND ONLY AFTER THE QA ABOVE IS DONE: the documentation
   structure review — owner-requested 2026-08-01, deliverable
   `docs/reports/DOC_STRUCTURE_REVIEW.md`.** Do the QA first, because its
   findings are your primary evidence: **the QA is the sample, this is the
   diagnosis.** See the upstream note below for the drift already catalogued
   and why the owner asked.

   **Assess every document the agents read or must keep updated** — the
   living set (`STATUS.md`, `BUGS.md`, `PLAYTEST_CHECKLIST.md`,
   `MOD_DESCRIPTION.md`, `agent/FIX_POLICY.md`, `agent/ENGINE_FACTS.md`,
   `PLAYTEST_HELP.md`, the standing prompts, the `reports/` set, `CLAUDE.md`
   if present) — and answer, for each: who writes it, who must update it and
   *when*, what facts it duplicates from elsewhere, and how a session is
   supposed to know it went stale.

   **Then give the owner RECOMMENDATIONS, not a restructure.** Wanted:
   - the **failure taxonomy** — group the observed drift by structural cause,
     not by incident;
   - for each cause, what would actually prevent it: single-source-of-truth
     moves, generated-instead-of-hand-maintained sections, a
     protocol/checklist change, a mechanical check (a script or a grep a
     session must run), a doc split or merge, or a doc that should stop
     existing;
   - **which are worth it** — cost against how often that class has actually
     bitten, and say plainly where the honest answer is "live with it";
   - a **recommended order**, cheapest-highest-value first.

   ⚠️ **Recommendations only — do not restructure anything.** The owner picks
   what happens. Flag explicitly any recommendation that would change how
   prompts/sessions are authored, since that touches `WORKFLOW.md` and the
   chain conventions.

8. ⭐⭐ **JOB 8 — THE OWNER ASKED FOR THIS BY NAME (2026-08-02): personally
   review the C23 item 1 decision and give feedback.** Verbatim: *"I am gonna do
   the build it, accept the thread for now, but its not locked. I want the QA run
   to personally review it and provide feedback."*

   ⛔⛔ **READ THIS FIRST — HALF OF THIS JOB WAS DISSOLVED BY THE BUILD
   (chain prompt 8c, 2026-08-02). The paragraphs below were written when the fix
   was expected to cost a game-time thread. IT DOES NOT.** The C23 entry's
   *"the only precise route is owning the scheduler body"* was **falsified when
   `8c` re-verified it against Src**: `GetDustDevilsDescr` has three callers, all
   inside that one thread, and the descriptor read is 1:1 with the count draw, so
   §3a **layer 3** reaches the defect by *substituting* the descriptor rather
   than mutating it. **F97 shipped as a §1.4b post-wrapper on
   `OverrideDisasterDescriptor`** — no 14th site, no sleeping mod thread, no
   §1.5 reconstruction, no version latch, no restart and therefore **neither of
   the two named traps applies at all** (they are moot by construction, not
   "handled"). The owner confirmed the route change before any code was written.

   **So the cost side of this review is gone, and what remains is ONE question:
   is the RATE change right?** Nothing in this chain has ever settled that —
   `DustDevils_Low` accidentally approximates a gate today (50% × 1..2 truncates
   to 0-or-1), so the shipped rates *may* have been tuned around the truncation.
   ⭐ **Reversal is still a legitimate outcome, and it now costs the project
   almost nothing** — deleting one 250-line module with no persisted state and
   no save reachable by it. Weigh the rate on its merits; do not let "the build
   turned out cheap" become a reason to keep a gameplay change.
   ⚠️ **Do not read the paragraphs below as current.** They are kept verbatim
   because the owner's approval was given against them, and a review that
   silently swapped its own premises would be worth less. Full record: BUGS
   **F97**, `SAVE_SAFETY_REDESIGN.md` **§8**, and `PLAYTEST_CHECKLIST.md`
   **PT-61**.

   **What was decided and why it is unusual.** C23 item 1 is the dust-devil
   scheduler using `spawn_chance` as a count multiplier instead of a probability
   gate. The owner approved **building** it, which means **owning the
   `DustDevils` game-time thread body** — knowingly adding a **14th §3a exposed
   site**, on a **P3** item, in the same chain that spent Tiers 1 and 2 removing
   two such sites. **That tension is the point of this job.**

   **The evidence FOR the fix is unusually strong and is all on the C23 entry** —
   read it before forming a view: three independent controls for gate-then-count
   (the marker sibling in the same file, `MapSettings_Meteor`'s identical trio,
   and fredware's independent fix), plus the finding that settles it from data
   alone — **`DustDevils_VeryHigh_3` is authored `count 6..8 @ 50%` and the
   multiply makes that range unreachable**, delivering 3-4 while the declared
   *minimum* is 6. The OG presets were also confirmed identical across all eight,
   from the original game's own debug menu.

   **What to weigh, honestly and in both directions:**
   - Is a P3 frequency repair worth a permanent save-safety site? The owner's
     own §3a ordering says prefer 3 → 2 → 1; this is none of those.
   - Both named traps are ones this project has already suffered — the F88
     timer re-roll and `Fix_MeteorFrequency`'s permanent-silence uninstall. If
     the build did not handle **both**, say so loudly.
   - Conversely: if the build is clean and the A/B is convincing, say that too.
     **This is not a job to find fault; it is a second opinion the owner asked
     for in advance.**
   - **C23 item 3 was DECLINED on the same shape.** If item 1 ships, is that
     consistent? Either answer is defensible — but the record should not hold
     both without noticing.

   **Deliverable:** a short section in the QA report — keep / revert / keep-with-
   changes, with reasoning. **It is explicitly NOT locked**, so recommending
   reversal is a legitimate outcome and costs the project only the build time.

## Scope fence

**In:** verification, the report, presenting unresolved items, **and the job-7
structure review (recommendations only)**. **Out:** fixing anything
substantive you find — a QA session that repairs its own findings
un-verifies itself. Trivial doc corrections (a stale row) are fine WITH the
finding recorded; anything larger is presented, not patched. **Job 7 is
explicitly analysis, not execution — it recommends, the owner decides.**

## Stop conditions

- A sampled verification fails (a flip without its leg) → that is the
  headline finding; finish the sweep, report, do not quietly re-run legs.
- The folder is not empty → stop immediately (gate above).

## What may not be claimed

CLEAR requires: zero unconsumed notes, zero unclassified owed-hits, zero
index/heading mismatches, all samples verified. Anything less is a findings
report, and that is a fully successful outcome too — say the true thing.

## On completion

Commit the QA report **and `DOC_STRUCTURE_REVIEW.md`**; delete this file and
`README.md`; push. The owner is free for playtesting, and has the structure
recommendations to decide on separately.

## Notes from upstream

### Routed here from chain prompt 5b (2026-08-01) — a standing coverage gap, not chain work

**Eight `[install]` probes SKIP on every retail run** ("introspection unavailable
(retail sandbox)") and always have. They can be made to report: the mod sandbox
applies on ALL builds including `MarsDebug.exe` (verified 2026-07-26 — the
"asserts build un-sandboxes mod code" assumption was tested and is wrong), but an
asserts build DOES un-sandbox the **console**, so the working attended procedure
is a MarsDebug session, then `SMRTest.EnableIntrospection(debug)` typed in the
console, then `SMRTest.RunAll()`.

Deliberately not done during PT-58: that leg's headline was a comparison against
a figure measured on retail, and an asserts build makes the `dbg()` calls inside
`CommandThreadProc` itself live (`CommandObject.lua:208`, `:273`) — the exact
loop under measurement. Right call there; still worth having as its own sitting.
**Recommend it as a standing playtest item rather than chain work** — it is
TestKit coverage and belongs to nobody's numbered prompt.


(any prompt may have routed standing items here — resolve them all)

### ✅ RESOLVED SAME DAY — do NOT re-ask. Kept for the QA trail only.

**The owner ran BOTH checks on 2026-08-01, within the hour they were routed
here.** Results are recorded in `BUG_LIST_AUDIT.md` **§10.4** and on BUGS **F01
/ F64 / F74 / C33 / D13**. Headlines: **F01's witness is FOUND** (May 8 2026,
Game Version 1.0.7, with repro steps — the audit's "NOT re-derivable" is
retracted); **F74's rival-rocket report is FOUND twice from the same reporter**
(OG 2022 + Relaunched 1.07 May 2026, two different triggers, both bricking the
rocket permanently); **F64 is partial** — family witnessed live, verbatim phrase
still not located, so it stops being a quotable citation. **Paradox Mods:
GromGor mirrors exactly, fredware does not**, plus a discovery problem worth
re-checking (`bug` / `fix` return zero hits; author search works).

**Two live items this leaves for your backward QA:**
1. ~~**⚠️ `[S22]` may be a bad citation of our own.**~~ **✅ RETRIED AND
   RESOLVED the same day — and it WAS partly bad.** The clean URLs work.
   `1113731` is a **retraction** ("NOT A BUG: I missed a crystal") that this
   audit had counted as F06 corroboration **on its title alone** — struck.
   `1112166` is genuine but low-grade (OG-2018, destroyed-crystal confound, and
   its only second witness is the person who retracted the other), so **F06's
   external support is one confounded OG report, not two**. Recorded in
   §10.4 and on the F06 entry; both defect claims stand on Src regardless.
   **✅ AND `1495056` (F16) WAS READ TOO — it VALIDATES**, which is the useful
   half of the lesson: reading bodies moves citations **both** ways. Genuine,
   author-reproducible, **three corroborators across three different
   mysteries** — but OG-2021, so it corroborates the family, not our build.
   **`[S22]` is fully resolved; nothing owed here.**
   **One lead came out of it and is deliberately UNASSIGNED** (§10.4): several
   mysteries failing to complete or clean up suggests shared upstream state, and
   **C36 proved one instance** (Inner Light gates on `IsDisasterPredicted()`,
   which F81(a) strands). Whether other mysteries gate the same way is a cheap
   grep of `Lua\Mysteries\`/`Lua\Scenario\`. **Not routed by guesswork — it is
   the owner's call whether it becomes work.** If it never does, say so in the
   QA report rather than leaving it looking owed.
2. **The audit's §1/§2 witness grades now lag its own §10.4** for F01 and F74.
   Bookkeeping, not a decision — but it is exactly the drift job 7 exists to
   catch, so catch it here.
3. **⚠️ Error counts are compared across arms, and SESSION UPTIME was never
   recorded next to them** (`BUG_LIST_AUDIT.md` §10.6f(i)). The owner does not
   close a game session unless a leg demands it, so a flushed log typically
   covers **1–6 hours of continuous play** — which makes our zero-error results
   *stronger* than they read, and makes cross-arm **count** comparisons depend
   on comparable exposure. The case to look at is **PT-58's `0` against leg 5's
   `80`**: the concern is small there (the orphan errors fire per drone-idle
   tick over 73 idle drones, so a zero does not need hours to mean something),
   but **the uptimes are not on the record and should be**. Fix the convention
   going forward — log the session uptime beside any error count — and note it
   in the QA report rather than re-opening a passed leg.

**The method lesson is the part worth carrying into the QA report:** §7.1 used
*"the crawler is blocked"* as grading input, and a single logged-in browse found
two of the three reports it had written off. **Inability to reach a source is
not evidence about the source.**

<details>
<summary>Original routing note (superseded — expand only if the QA trail needs it)</summary>

### Routed here from chain prompt 6 (2026-08-01) — the audit's TWO remaining owner web-checks, still open

**These are owner actions, not agent work — neither can be done from a
session** (both sources defeat crawlers), which is exactly why they keep
surviving prompts. `BUG_LIST_AUDIT.md` §7.1 lists them as stop-and-ask items
(a) and (b); its third, the GromGor/fredware subscribe, is DONE and consumed.
Prompt 6 had no signal either had been done, so per its own brief it routes
the reminder here rather than dropping it.

1. **A logged-in browse of the Paradox "Relaunched Bug Reports" subforum
   (1189)** for the three reports the audit could cite only at title/snippet
   grade: **F01**'s NoDisasters/cave-ins report, **F64**'s "trains go to void"
   report, **F74**'s rival-rocket report. They are **unretrieved, not
   disproven** — that distinction is load-bearing on all three entries.
2. **A browser check of Paradox Mods' Relaunched section** (a SPA, unfetchable)
   — specifically whether fredware and GromGor mirror there. **This is the
   console channel and it feeds D13**, which the owner has since made a hard
   launch dependency, so it matters more now than when the audit wrote it.

**What to do with the answers:** outcomes go on the named entries (F01, F64,
F74) and on the D13 record, and §7.1's open list closes. **If the owner has
already done either since 2026-08-01, record the outcome and strike the item —
do not re-ask.** If they have not, this is a reminder, not a blocker: it gates
nothing in the chain, and the QA report should say so plainly rather than
carrying it as an unresolved defect.

</details>

### Also from prompt 6 (2026-08-01) — one QA-relevant correction, so job 0's sweep does not inherit it

**`BUG_LIST_AUDIT.md` now has a §10 that contradicts its own §9 twice** (C32
downgraded and F04's demotion undermined; C04 confirmed and promoted to F90).
§9's affected bullets are annotated in place, but **the audit's §1 headline
counts were left alone on purpose** — F04's tier is chain prompt 7's decision,
not the sweep's. If prompt 7 moved it, §1 and the §2 table row need to agree
with wherever it landed; if prompt 7 left it, the ⚠ contested marker on the §2
F04 row is the truth and should stay. **Either way, §1's "GOLD 17→16, BRONZE
29→30" line is the thing most likely to be stale by the time you read it.**

### From chain prompt 4b (2026-08-01) — documentation drift, and why job 7 exists

**The owner asked for job 7 after a single session turned up four more
instances of documentation drifting from truth. It is not the first time —
that is the point.** This is a recurring class in this project, not a run of
bad luck, and the owner wants the structural cause addressed rather than
another round of patching. Treat the list below as the seed corpus for the
taxonomy; your own QA will add to it.

**Found in one session (2026-08-01, prompt 4b):**
1. **F86's heading tag still read "Still nothing BUILT — that is prompt 4"**
   while Tier 1 was built *and* verified. Aggravating detail: that same tag
   already carried a note saying it had been **REFRESHED earlier the same day
   because it had gone stale against its own index row**. It went stale twice
   in one day, in the same way.
2. **Four dangling cross-file pointers** appeared the moment
   `F86_TIER1_BUILD_PROMPT.md` was consumed — live references in `BUGS.md`
   (×2), `PLAYTEST_CHECKLIST.md` and `STATUS.md` pointing at a file the chain's
   own self-consuming design had just deleted. Nothing detected this; it was
   caught by hand.
3. **A bound recorded as if it were a value.** The F86 exposed set is written
   `"at least 13"` / `"≥13"`, but downstream text cites a flat count — while
   **four per-module tables still carry a stale `12` denominator**. A wrong
   denominator in a per-module table silently drops a site rather than merely
   misreporting a total.
4. **A gate that expired into a wrong instruction.** `MOD_DESCRIPTION.md`'s
   draft note said "do not publish until F86 Tier 1 verifies". Tier 1 verified
   — so the note's stated condition became **true** while the claim it guarded
   was still unbackable. A session reading only that note would have published
   correctly-per-the-note and wrongly-in-fact.

**Already on record from before this session** (do not re-derive; cite them):
F18's stale `fixed*` tag and F86's stale heading, both caught by the
2026-08-01 bug-list audit · STATUS counts going stale **within their own day**
(the 2026-07-31 "98", then 100 → 101) · `FABLE_NEXT_PROMPT.md` going stale
whenever playtest commits land after its last edit · the standing protocol
"a status flip must hit the index row **and** the heading tag" — a rule that
exists only because those two locations drift apart.

**A hypothesis to test, not to accept:** several of these look like one cause
— *the same fact is stored in more than one place and kept in sync by hand.*
Index row + heading tag, counts in STATUS + counts in per-module tables,
pointers to files another prompt owns and deletes. If that holds, the
protocols we keep adding ("update both locations") are compensation for a
structural duplication rather than a fix for it. Confirm or refute it against
your own findings; the owner wants the real diagnosis, not this one repeated.

### Added by chain prompt 7 (2026-08-02, per chain rule 4b) — four instances, and **three of them are a class the hypothesis above does not cover**

The duplication hypothesis explains instance 1 below. It does **not** explain
2-4, which are a different failure: **a claim was recorded as a fact, carried
forward by later sessions, and was wrong or unverifiable at the moment it was
written.** No amount of syncing duplicate locations would have caught any of
them. If that second class is real, the taxonomy needs both axes.

1. **The prompt's own brief was stale against the entry it described** (the
   duplication class). `7_audit_candidate_decisions_opus.md` §5d said the C33
   train-report lead's *"provenance is not established"* and that it *"may never
   have reached Paradox"* — while the C33 entry itself already recorded
   **"✅ PROVENANCE ESTABLISHED"** and then a same-day weakening from a rival
   hotfix-2 explanation. The brief was written before both updates and never
   re-synced. Caught only because the entry was read before the brief was acted
   on. **Prompt briefs are a duplication site nobody has been counting.**
2. **An unverifiable claim recorded as fact, and inherited.** C33 stated that
   *"a naive `DoneObject` on it RAISES"*. `ripairs` is engine-provided with **no
   body anywhere in Src**, and `ENGINE_FACTS.md` separately records that this
   Lua *tolerates* the neighbouring cases (`#nil`, `next(nil)`, `ipairs(false)`).
   The claim could not have been derived from source at all. It survived because
   it sounded mechanical.
3. **A property read as deliberate design that is inert on its sibling.** F82's
   entry cited `GameTime = false` as an *"explicit override against a default of
   `true`"* — evidence the real-time expiry was chosen. But `PowerLeak` carries
   the same flag with **no `Expiration` for it to govern**, and
   `LifeSupportLeak` lacks it. The flag is not always a considered choice in
   that file, so the inference was unsound. **Withdrawn on the entry.**
4. **A routing note's guess hardened into a tier.** The brief suggested Saint is
   *"a breakthrough trait — R2-ish?"*. It has no `hidden_on_start` (its sibling
   Empath does), so it is an ordinary rare applicant trait and the tier is R1.
   A parenthetical guess in a handoff note is indistinguishable, three sessions
   later, from a derived result.

**What is worth testing about 2-4:** every one of them was caught by *going back
to the primary source* rather than by any cross-check between documents. The
project already has a rule for this shape — "recorded facts are claims too" —
and it keeps being learned rather than enforced. **A candidate diagnosis for
job 7: the docs have no way to mark the difference between a fact derived from
Src this session, a fact inherited from an earlier session, and a guess.** All
three are written in the same voice.

### Added by chain prompt 8 (2026-08-02) — one review item, and one job-7 instance of exactly the class above

**⚠️ REVIEW ITEM — a group-A conversion was withdrawn after being checked
against source.** `SAVE_SAFETY_REDESIGN.md` §5.4 group A listed **six** modules
as *"convert to a chained wrapper — no body copy, **verified feasible**"*, with
the preamble *"each was checked against the shipped body, not inferred from our
header"*. Prompt 8 built five of them. The sixth,
**`Fix_TrainCargoDumping`, had no route at all**, and the row that promised one
is wrong in its load-bearing clause:

- §5.4 said the fix could come from wrapping the demand request's
  `GetTargetAmount`. **`GetTargetAmount` is not Lua.** The only Lua declaration
  of that name in Src is `ResourcePile:GetTargetAmount`
  (`Lua\ResourcePile.lua:79`) — a different class. `station.demand[res]` is a
  **TaskRequest**, built by the native `Request_New`
  (`CommonLua\TaskRequest.lua:109-137`); its methods live on the native
  metatable `Request_GetMeta()` returns.
- Patching that metatable would desynchronise the savegame **permanents** table
  (`permanents["TaskRequest.GetTargetAmount"]`, `CommonLua\TaskRequest.lua:38`),
  and `PersistGatherPermanents` is **blacklisted for mods** — we could not
  re-register ours.
- 148 call sites across the request economy, and **no key**: the wrapper cannot
  tell it is inside `Train:UnloadAll`, and the fix's two escape hatches need the
  **train**, which the request never carries.

The second route prompt 8 looked for (pre-wrapper swapping
`station.storable_resources` under `pcall`, F90's shape) is behaviourally exact
but mutates a **persisted property** on a live object inside a command path —
worse on §3a grounds than the copy it would replace, on a module §5.4 itself
certifies is already save-safe. **Skipped under prompt 8's stop condition 1;
moved to group C; group counts corrected to 5 / 4 / 10 / 3.** Full reasoning is
on BUGS **F46**; §5.4's row, its bottom line and group C all carry the
correction. **What is owed here is a second opinion on the skip**, not a rebuild:
if a route was missed, the module should still convert.

**⭐ And the second, smaller correction, recorded because prompt 8 disagreed with
its own instructions rather than with a fact.** §5.4 also claimed
`Fix_ShuttleHubOffAvailable` converts to a wrapper that eliminates the copy. It
converts — byte-equivalently — but the copy is **duplicated, not eliminated**:
the shipped function returns one colony-wide boolean and never says which hub
produced it, so the predicate has to be owned. The conversion is still worth
having (we can never be looser than a patched vanilla), and it shipped, but the
row overstated the benefit and both the entry and §5.4 now say so.

**Job-7 seed line (chain rule 4b).** Instance: **a table column that asserts its
own verification.** §5.4's group A is headed *"verified feasible"* and prefaced
*"each was checked against the shipped body, not inferred from our header"* —
and one of its six rows was inferred, from a method name, without checking where
that name is declared. This is the same failure the prompt-7 block above
diagnoses ("the docs have no way to mark the difference between a fact derived
from Src this session, a fact inherited, and a guess"), with one aggravation
worth its own line: **here the doc did not merely fail to mark the difference —
it explicitly claimed the stronger status for all six.** A blanket
"verified"/"checked" header applied to a *list* launders every row to the
standard of the best one, and nothing in the format can record that row 6 was
weaker. Caught only by going to primary source, again, and only because a
session was made to build the thing rather than cite it.

**Second job-7 seed line from prompt 8 (chain rule 4b) — a summary that outlived
its own correction.** `Code/Fix_DroneTransportMinors.lua` opened with *"the third
is deliberately left alone because fixing it would undo F61"*. That reason was
**withdrawn by the QA audit on 2026-07-25** and replaced, in the same file, in
the `(c)` paragraph — which says so explicitly, in a parenthetical beginning
"RATIONALE CORRECTED". The one-line summary at the top of the file went on
asserting the retracted reason for eight days. Caught only because prompt 8 was
rewriting that header for the F57(a) conversion; fixed in the same commit and
reported here rather than silently corrected.

**What is new about this instance, versus the four already listed:** those are
all *facts* that drifted. This one is a **correction that landed in one place and
not in the other place that says the same thing**, in a single file, with the
corrected paragraph and the stale summary visible on one screen. It suggests the
job-7 diagnosis needs a second axis beyond "the docs cannot mark a fact's
provenance": **the docs also have no convention for where a claim's OTHER copies
live.** The project already knows this shape well enough to have a rule for one
instance of it — BUGS statuses live in TWO places, index row and heading tag,
"never flip one without the other" — and that rule exists precisely because the
pairing is invisible unless someone writes it down. Nothing does that for module
headers, entry summaries, or report bottom lines.

### Added by chain prompt 8b (2026-08-02) — six job-7 instances, and they cluster into ONE new shape

**All six were caught the same way as prompt 8's two: by a session being made to
BUILD the thing rather than cite it.** Every one is corrected on its own entry;
they are listed here because rule 4b says a silently-corrected instance is
destroyed evidence.

⭐ **The shape they share, and it is a third axis for the job-7 diagnosis: five
of the six are defects in an APPROVED SPEC — not in a fact, and not in a stale
copy.** Prompt 7's six §4 packages were written to be built without re-derivation
("this prompt should not need to re-derive any of it"), and each carried a module,
a technique, a code sketch, a self-check and a probe outline. The specs were
right about **what to build** in all six cases and the shapes all survived
contact. What failed was the *supporting detail* — a line number, a method name,
a placement, a claim about equivalence — which is exactly the material a builder
must trust if the "do not re-derive" instruction is to mean anything. **A spec
that is authoritative about design and unreliable about detail is a shape the
project has no convention for, and it is more dangerous than an ordinary stale
fact, because the instruction attached to it actively discourages checking.**

| # | instance | where it was corrected |
|---|---|---|
| 1 | **F91's spec cited `Track.lua:56-60` for all three arrays' initialisation.** `TrackBase:Init` gives two; `assigned_vehicles` comes from the combined `StationsLink:Init` (`StationsLink.lua:13`) one class up. The *claim* survives — a constructed track still has all three as tables, so the three-`false` shell signature still cannot match a live track — but the citation was wrong | BUGS F91, BUILT section |
| 2 | **F95's spec named a method that does not exist.** It said to reuse `Effect_ModifyLabel`'s own `__exec`; the method is `OnApplyEffect` (`MarsGameEffects.lua:161-172`). The instruction's substance was followed exactly | BUGS F95, BUILT section |
| 3 | **F93's spec put half a self-check where it cannot run.** "Self-check at apply: the global exists **and `Presets.MapSettings.DustDevils` is populated**" — presets do not exist when mod code loads on a cold boot, so an apply-time absence test *is* the F75 false-inactive bug, and building it as written would have deactivated the fix on every cold start. Moved to `DataPatch`, which owns the F75 gate | BUGS F93, BUILT section |
| 4 | **F96's spec treated two writes as equivalent.** "Patch both `BuildingTemplates.Sinkhole` and the `Sinkhole` class table" reads as belt-and-braces; in fact only the class write is load-bearing. `BuildingTemplates.Sinkhole` is a thin proxy — `setmetatable({template_name = id}, g_Classes[id])`, `Building.lua:2566` — **rebuilt on every `ClassesBuilt`/`DataChanged`**, so a write there is both transient and redundant. Had a builder patched only the template, the fix would have silently done nothing | BUGS F96, BUILT section |
| 5 | **F90's spec overclaimed its own error handling.** "`pcall` + restore + re-raise; **vanilla's error behaviour is preserved**". `error()` in mod code reports and continues — it does not unwind (ENGINE_FACTS, FIX_POLICY §6) — so the re-raise keeps the failure *visible* but does not reproduce the unwind. Narrowed to "vanilla's error is still reported" | BUGS F90, BUILT section |
| 6 | **A count line that lacked the exclusion its neighbour documented.** STATUS's probe count says in writing that `SMRTest.Register(` also matches the *definition* in `00_TestCore.lua` and must be excluded. The registered-module line, derived by the identical technique against `SMRFixPack.Register(`, said no such thing — and `00_Core.lua` has the identical definition line. A first raw recount this session came back one high because of it. Both lines now carry the exclusion | STATUS build-state block |

**And one instance of prompt 8's shape, at four-copy scale.** F94 removed a
property `Fix_AsteroidLanderAvailable` advertised, and that property was asserted
in **four** places: the module header, F72's BUGS entry body, F72's heading tag,
and F72's index row. All four were corrected in the same commit — but the only
reason all four were found is that the F94 entry explicitly warned the builder to
fix the header. **Nothing in the format would have surfaced the other three**,
which is the "no convention for where a claim's other copies live" point above,
now with a measured fan-out: one behaviour change, four documents.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in prompt
8b.** One staging slip is recorded rather than hidden: a `git add -A` in the F93
commit staged `docs/reports/BLIND_AUDIT.md`. It was amended out before any push
and the file is untracked again, exactly as prompt 8 left it. **Nothing in it was
opened, read, grepped or summarised** — the slip was a staging pattern, not a
read, and it is noted in that commit message too. (Job-7 relevance, if any: the
seal is enforced by prose in two prompts and nothing mechanical — no
`.gitignore` entry, no hook — so the only thing standing between the control and
an accidental commit is that every session remembers to name its paths.)

### ⭐ Added by chain prompt 8b AFTER PT-60 ran (2026-08-02) — a THIRD AXIS this corpus does not have

**Two of this batch's three load-time heals were not idempotent, and neither defect
was visible to source review, to code review, or to its own probe. Only a keyboard
save/load round trip exposed them.**

| module | defect | how caught |
|---|---|---|
| `Fix_SaintBlessing` | re-applied and re-logged the re-base on **every** load — idempotent in effect but not the **one-shot** its spec specified; would have printed its line in every future session log forever | re-reading the module against its own spec while setting up an unrelated fixture, *before* the leg |
| `Fix_AstrogeologistExtractors` | **+10% added on every load, unbounded.** Its presence test compared **object identity**, and `label_modifiers` is persisted, so the save deserialises its own copy of the key and the test can never match across a load | **only** because the owner saved, reloaded, and re-read the number |

**Why this is a new shape.** The existing entries are all about *documentation*
drifting from truth — stale facts, a correction that landed in one copy and not
another, a spec authoritative about design and unreliable about detail. **This is
code that is wrong in a way no artefact the project reads can show:**

- **Source review passes it.** Both heals read as obviously idempotent, and the
  reasoning written into their headers was detailed, confident and wrong.
  `Fix_AstrogeologistExtractors` argued idempotence from `SetLabelModifier`'s
  replace semantics — true, and irrelevant, because the **key** changes across the
  save boundary.
- **The probe passes it.** `AstrogeologistExtractors` PASSed throughout: it asserts
  the *profile* carries an entry per buildable extractor, which stayed true while
  the *applied modifier count* doubled on every load. The probe was testing the
  preset, not the colony.
- **Vanilla cannot warn you.** The engine's own ten `Effect_ModifyLabel` entries use
  the identical identity keying and never hit this, because `EffectsApply` runs once
  at game start and nothing re-applies them on load. **Copying vanilla's shape is
  what produced the bug** — the shape is only safe in vanilla's calling context.

**The diagnostic question for job 7.** The project has a rule that a BUGS status
lives in two places and must be flipped in both. It has **no equivalent rule for a
claim whose truth depends on a state transition no static artefact crosses.** Every
load-time heal, migration and version latch in this pack makes an idempotence
claim, and **the only instrument that can falsify one is a human loading a save
twice.** Worth asking whether that class of claim needs its own marker, its own
probe convention (a probe that runs *across* a load rather than within one), or
simply a standing playtest step.

⚠️ **Scope note:** other heals and migrations in this pack have never been
round-tripped this way — the F86 Tier-1 version latch, the rains migration,
`90_SaveSanitizer`. `Fix_TrackSalvageWipe`'s sweep *was* verified on 2026-08-02
(one heal line across five loads). **Two for two on the ones actually tested is not
a reassuring base rate.**

### From chain prompt 8c (2026-08-02) — the C23 item 1 build, and a job-7 axis the corpus does not have

**Job 8's premises changed before you got here — the correction is inline at job 8
itself.** In one line: F97 shipped, it costs no §3a site and no thread, and the
only live question is the rate.

**⭐ A JOB-7 SEED LINE, and it is a different SHAPE from the ones already in this
list (chain rule 4b).** Every drift instance recorded so far is a *citation* going
stale — a wrong line number, a method that does not exist, a self-check in the
wrong place, a summary outliving its reason, a table column asserting its own
verification. **This one is a ROUTE claim, and it failed in the opposite direction
to prompt 8's.**

* **What drifted.** The C23 build spec stated *"the only precise route is owning
  the scheduler body"* and priced the item accordingly — a 14th §3a exposed site,
  a mod-owned sleeping game-time thread in every save, a §1.5 reconstruction, a
  version latch and an uninstall hand-back. **The owner approved the item WITH
  that cost attached.** It was wrong: a §3a layer-3 route existed the whole time.
* **How it was caught.** Only by re-deriving the route from Src rather than
  re-checking the spec's citations. Every supporting fact the spec gave is
  individually TRUE — `:216` really is inside a thread closure, there really is no
  global function to replace, and the descriptor really is a shared preset that
  cannot be mutated. The conclusion still did not follow, because nobody asked
  whether the descriptor could be **substituted** instead of mutated.
* **⭐ Why this is worth a taxonomy row of its own.** Prompt 8 found a route
  recorded as *"verified feasible"* that **did not exist** (§5.4's `GetTargetAmount`
  wrapper). Prompt 8c found a route recorded as **impossible** that **did**. Same
  week, same corpus, opposite signs. **The project's re-verification discipline
  currently checks citations, and both misses were in the reasoning above the
  citations.** A doc convention that distinguishes *"this line says X"* from
  *"therefore the only route is Y"* would have caught both; today the two are
  written in the same voice, and the second inherits the first's authority.
* **One aggravating factor worth recording:** the spec was written in the same
  sitting as F93, and F93 is what made the layer-3 route *obvious* — it put a
  mod-owned seam on `GetDustDevilsDescr`. The route existed before F93 and did not
  depend on it, but nobody looked again after F93 landed. **A spec's cost estimate
  has a shelf life, and nothing in this project's process re-opens one.**

**Two smaller items, both already fixed, both recorded because chain rule 4b says
a silently-corrected instance is destroyed evidence:**

* The C23 entry cited `TerraformingDisasters.lua:97` for *"`OverrideDisasterDescriptor`
  returns the preset itself"*. Line `:97` returns `settings` — a **different**
  preset from the same group; `original` is returned at `:56`, `:62` and `:89`.
  The conclusion (it is always a shared preset, so it cannot be mutated) is
  **unaffected and correct**; the cited line was the wrong one of two right
  answers. This is the **seventh** prompt-7-era spec whose supporting detail had a
  defect.
* `STATUS.md`'s build-state line has carried *"79 registered modules, 73
  default-active"* — a pair that only reconciles if the divisor is **6**, while
  **7** modules register with `optional = true`. It is not an error (the seventh,
  `Opt_DroneStatDials`, reports active at base, by design), but the line never said
  so, so the next recount had to re-derive why 79 − 7 ≠ 73. Now stated explicitly.
  **A count that needs an unwritten exception to add up is a count that will drift.**

**Nothing else is routed here.** F97 is unrun; PT-61 is written with predictions
**P1-P10** before any run, and its verdict belongs to whoever runs it, not to this
prompt.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 8c.** No broad search touched it; the one repo-wide `grep` run in this
sitting was the stale-probe sweep (`TEMPORARY`), which returned zero hits.

### ⭐ PT-61 RAN (2026-08-02, same day) — job 8 now has evidence, and it points at a table rather than at the leg

**F97 is `tested`.** All ten predictions met over 29 scored waves; the full result
is on the F97 entry and in `PLAYTEST_CHECKLIST.md` PT-61. In one line: vanilla
produced **only 3s and 4s** across nine waves and never once entered the authored
`6..8`; the fixed half produced **0 or 6-8** across twenty and reached 8 twice.
Save-boundary and uninstall both clean, zero `[LUA ERROR]`, and the colony kept
its dust devils with the pack removed.

**⛔ THE ONE THING JOB 8 MUST NOT DO IS DECIDE ON PT-61'S NUMBERS.** The leg
measured `DustDevils_VeryHigh_3`, which the per-preset derivation on the F97 entry
shows is the **least**-affected preset anyone actually plays: **+5% on the mean**.
Its observed averages (vanilla 3.22, fixed 4.45) are **not** the rate change —
that sample's gate passed 65% instead of 50%. Decide on the table.

**Two findings on that table that did not exist when job 8 was written:**

* ⛔⛔ **RETRACTED THE SAME DAY — DO NOT USE.** The first version of this note
  claimed `DustDevils_VeryLow` "produces exactly zero dust devils, always" and
  called it "the strongest form of the intent argument yet". **It is wrong.** That
  preset ships `'forbidden', true` — the only one that does — and the scheduler's
  third statement is `if not descr or descr.forbidden then return end`
  (`DustDevils.lua:194-196`), before the marker threads and before the wave loop.
  The whole system is switched off on such a map, deliberately and with an
  explicit flag. **The zero is a design decision, not the defect**, and the
  fallback point inverts: falling back to a forbidden preset is a fail-safe.
  ⚠️ **The intent argument for job 8 is therefore `VeryHigh_3` alone** — an
  authored `6..8` that is entirely unreachable — **plus the three controls already
  on the C23 entry.** Still strong, but one leg rather than two. Weigh it as one.
  ⚠️ **And take the error itself as job-7 material** (chain rule 4b): the table was
  built from a targeted grep for the count fields, `forbidden` was not in the grep
  so it was not in the analysis, and a striking conclusion was drawn from the
  fields that had been looked for rather than from the preset. It survived into
  BUGS, STATUS and this prompt before the owner asked a one-line question that
  falsified it. **Caught in under an hour, and only because someone asked.**
* **The change is not uniform: 0% to +125% across played presets**, largest where
  counts are small. The honest framing for the owner is *"the fix roughly restores
  the authored means, and on some presets the authored mean is twice what the game
  currently delivers"* — repair or difficulty change, which is the judgement asked
  for.

⭐ **And the reachability standing changed.** The uninstall leg, with **no mod
installed** and the map back on **its own shipped setting**, logged
`DustDevils_Low` (authored `count 1..2`) computing `0..1` and producing nothing
across two consecutive waves. Until then R1 rested on source enumeration alone.
The *observation* needed the TestKit logger; the *state* did not.

**Job 8's cost side is now empty and its evidence side is full.** Reversal remains
legitimate and now costs almost nothing — one module, no persisted state, and the
uninstall path is measured. But it is a rate judgement, and it should be made
against nine presets, not one.

**Two more job-7 seed lines from the run itself (chain rule 4b):**

* **A verification step that could never have executed, shipped inside a handover
  and was inherited verbatim into a checklist.** PT-61's terraforming gate check
  came from prompt 8c's addendum as `rawget(_G, "DustStormsDisabled")` — both
  `rawget` and `_G` are in `ModEnvBlacklist` (`Mod.lua:1267-1428`) and the console
  runs in that sandbox, so the line calls a nil value. ⭐ **The failure would not
  have looked like a broken command; it would have looked like an answer**, and
  the check's entire job was to stop the sitting before it started. Nobody had run
  it. **Consider whether console snippets in docs need a "has this ever been
  executed?" marker** — a snippet that has only ever been *written* is a different
  artefact from one that has been *run*, and today they are indistinguishable.
* **A probe that FAILED on correct code**, because it asserted an input the engine
  cannot supply (`vanilla_count(off, 8)` where the range had been zeroed, so
  `Random(0,0)` could only return 0). Caught immediately, but the direction
  matters: a false positive is cheap to notice and a false negative is not, and
  the wave-file house rules say "assert on the mechanism" without saying "and only
  on inputs the engine can produce."

### Added by chain prompt 9 (2026-08-02) — four job-7 instances, and one is a NEW axis: a fix that reports success while doing nothing

Chain rule 4b: captured even though three of the four took seconds to correct.

**1 · ⭐⭐ NEW AXIS — A SHIPPED FIX THAT HAS NEVER WORKED, AND EVERY SURFACE THE
PROJECT HAS SAID SO.** `Fix_TechDescriptionBuilding` (F25, status `fixed` since
it was written) **is a no-op in retail**: it re-uses the shipped translation id,
and `T(id, text)` in a non-dev build discards the replacement literal and returns
the id alone (`CommonLua\Core\localization.lua:250-252`). Filed as **F98**.
**What makes this a new axis rather than another stale fact:** every existing
job-7 instance is a *document* drifting from a *truth*. Here the document was
faithful — the module header, the BUGS entry and the index row all described what
the author believed, consistently, for days. **The defect is that no surface in
the project can distinguish "this fix ran" from "this fix worked."** The module's
own verdict function returns `"patched"` on having performed the assignment,
which it genuinely does; `ListFixes()` reports `active`; the probe suite has
nothing to say about it. **Ask job 7: what does the project do about a claim
whose only available evidence confirms the wrong proposition?** The existing
answer — `fixed` means code written, `tested` means verified in-game — is the
right *shape* and did not help, because `fixed` was true and read as sufficient
for a text change nobody thought needed a playtest.

**2 · A DOC ASKED FOR EXACTLY THIS CHECK AND NOBODY RAN IT FOR THREE DAYS.**
F84's entry, written 2026-07-30, said: *"Precedent exists (F25 is a description
defect), but **F25 should be re-checked for how it handled loc before this is
treated as settled**."* That sentence was correct, specific, actionable, and sat
unexecuted until the D10 build tried to lean on the precedent. **The project has
no mechanism for a written "someone should check X before relying on this"** —
it is not a todo, not a checklist rider, not a BUGS row, and nothing sweeps for
it. ⚠️ Related and worth grepping during the review: how many other entries carry
a conditional like *"should be re-checked"* / *"if this is true then"* / *"treat
as unverified until"* with no owner and no trigger.

**3 · AN APPROVED SPEC CARRYING THREE FALSE CLAIMS, ALL SURVIVING USER APPROVAL.**
D10's entry — specced 2026-07-30, user-approved the same day, and treated as
*"the spec, do not re-design it"* by prompt 9's own brief — asserted (a) three
vocation Workshops when there are **four**, (b) that the workshops' own `upgrade1`
modifies `max_workers` when **none of them has an `upgrade1_id`**, so it never
applies, and (c) that **every** faction def carries unemployment clauses when
**seven of twenty-nine** do. ⭐ **The pattern worth naming: (b) is a false
citation under a true conclusion.** The conclusion — live `max_workers` change is
a vanilla path — is correct, on completely different evidence
(`Workplace:OnModifiableValueChanged`). **A reviewer checking whether the claim
was right would have said yes.** This is the third instance in one week of a
*route* being wrong while its citations read fine (prompt 8's phantom route,
8c's route claim in the opposite direction, now this) — the corpus is large
enough for job 7 to treat "verify the route, not the citations" as a finding
rather than three anecdotes.

**4 · THE CHAIN'S OWN README WENT STALE ABOUT THE CHAIN.** `README.md` row `8b2`
still lists `8b2_pt60_leg_completion_opus.md` as a pending, un-struck chain
member; the file was consumed on 2026-08-02 (`b23e22e`) and does not exist.
Small, but pointed: **the index the chain uses to decide what runs next is the
one document no prompt owns**, because each prompt's mechanics tell it to update
the *next prompt* and delete *itself*. Corrected this session.

### Added by chain prompt 10 (2026-08-02) — the D12 build: one job-7 instance, and one thing the corpus should NOT be told is drift

**1 · JOB-7 SEED LINE (chain rule 4b) — a citation off by one hop, in an
APPROVED spec, in the sentence that carried the design's cheapest claim.** The
D12 entry's Mechanism section said `Colonist:FindEmigrationDome` is *"called
every heavy update from `Colonist.lua:1894-1898`, so no new scheduling"*. It is
not called there. Its **only** caller in Src is `Colonist.lua:1603`, inside
`Colonist:TryToEmigrate` — which the heavy-update block calls at `:1898`, and
*also* calls off-cycle at `:1900-1902` when `user_forced_dome` is set. Corrected
in place on the entry.

⭐ **Why this one is worth a line rather than a shrug: the substance survived and
the citation did not, which is the mirror image of prompt 9's instance** (a false
citation under a true conclusion). Here the conclusion — "no new scheduling" — is
correct, the seam is correct, and the line number points at the caller's caller.
**Both directions of the same failure now sit in the corpus within a day of each
other**, which strengthens prompt 9's suggestion that job 7 name *"verify the
route, not the citations"* as a finding: this instance shows the reverse check is
also needed, because a citation that verifies cleanly against a nearby correct
fact is exactly the kind that never gets challenged. ⚠️ The off-cycle caller at
`:1900-1902` is a real behavioural difference the original citation hid — a
`user_forced_dome` colonist reaches this seam more often than "every heavy
update" implies.

**2 · ⛔ AND ONE NON-INSTANCE, RECORDED SO IT IS NOT MISCOUNTED.** This session
also *changed* the D12 entry's destination rule (adding a suitability filter the
spec did not name) and *decided* its open question. **Neither is documentation
drift.** The spec explicitly delegated the open question to the build (*"Decide
before coding"*), and the added filter is recorded on the entry as a deliberate
departure with its reasoning. Job 7's corpus is about documents drifting from
truth; a document being deliberately amended by the session authorised to amend
it is the process working. **The corpus will over-count if amendments and drift
are pooled** — worth a sentence in the taxonomy about how to tell them apart, and
the tell here is that the departure was written down in the same commit.

**3 · A note for job 0, not for job 7.** D12 ships opt-in and off by default, and
its PT-62 leg explicitly uses the **Mod-Manager-disable** method for the
uninstall half rather than the module toggle, on the "OFF is three different
things" doctrine. If job 0's re-verification of that doctrine changes the answer,
**PT-62's P12 is one of the predictions that would need restating** — it is
written on the assumption that a toggled-off module still has live hooks.

### Added by chain prompt 10, second sitting (2026-08-02) — a NEW job-7 axis: test scaffolding that later became load-bearing behaviour

**What happened.** The first suite run after the D12 build returned
`76 PASS, 1 FAIL, 10 SKIP` (log `Mars.exe-20260802-20.28.19`). The FAIL was
`DustDevilSpawnGate` — **the very item that had been routed forward three times
looking for a suite run** — with the verdict *"the installed wrapper did not gate
a descriptor on a passing roll"*.

**It was a PROBE defect, not a fix defect, and the mechanism is worth naming.**
The probe's end-to-end section set `forbidden = true` on its test descriptor
purely as **scaffolding**: `OverrideDisasterDescriptor` returns a forbidden
descriptor unchanged (`TerraformingDisasters.lua:55-57`), which was the trick
that let the probe run the REAL captured original instead of a stub. Chain 8c
then added a `forbidden` early-return to `gate_descriptor` itself as **real
behaviour**. From that moment the scaffolding lever and the behaviour under test
were the same flag, and the fix's correct answer (hand it back untouched) was
read as a failure.

⭐ **The axis this adds to the corpus.** Every instance so far is a *document*
drifting from a *truth*, or a *route* being wrong under correct citations. This
one is neither: **two artefacts that were each correct in isolation, written
eight hours apart, whose meanings collided because they used the same field for
different purposes.** Nothing drifted, nothing was stale, and no citation was
wrong. **Ask job 7: what, if anything, the project can do about a test whose
setup depends on a game flag that a later fix may give meaning to.** The tell was
available — 8c's own comment said the guard was *"covered by the probe's
forbidden-passthrough assertion"*, which was true of a *different* assertion in
the same probe, and nobody checked whether any other assertion also used the
flag.

⚠️ **And the cost is the real finding: this cannot be caught without running the
suite.** 8c called the change *"behaviour-neutral by construction but not by
measurement"* and routed the measurement forward. It was routed three times
(prompt 9 built nothing, prompt 10's own leg is unrun) and caught only when a
suite finally ran for an unrelated reason. **A change whose own author flags it
as unmeasured should not be routable more than once** — worth a recommendation.

**2 · A SECOND, PLAINER INSTANCE FROM THE SAME RUN — a two-file registration
that only one file knew about.** `Opt_NoHomeless.lua` was added to `items.lua`
but **not** to `metadata.lua`'s `'code'` list, so the module never loaded and its
probe reported `SKIP — optional module not present` rather than anything
alarming. The pack's Lua manifest lives in **two** places that must agree, one of
them is what the game actually reads, and **nothing checks that they do**.
⚠️ Note the failure *presented as a benign SKIP*, which is the same shape as the
opt-in SKIPs around it — there is no reading of that line that says "a file you
shipped is not loaded". **Ask job 7 for a cheap invariant** (a probe that
compares the `Code/` directory against the loaded registry would have caught it
in the same run that missed it).

**3 · THE SAME AXIS A THIRD TIME IN ONE DAY, WITH THE ROLES REVERSED — and this
one was a REAL defect, not a probe artefact.** The re-run after the two repairs
above returned `77 PASS, 0 FAIL, 9 SKIP, **1 ERROR**`: `Opt_NoHomeless.lua:186:
attempt to call a nil value (method 'IsHomeless')`, reported against the **D07
`CohortHousing`** probe. D12's new wrapper sits on the same
`Colonist:FindEmigrationDome` that D07's probe drives with plain-table stand-ins,
and it called `self:IsHomeless()` before checking whether the colonist's dome
even carried D12's flag.

⭐ **Why this belongs next to instance 1 rather than on its own.** Instance 1 was
a *fix* breaking *its own* probe through a shared field; this is a *new module*
breaking *another module's* probe through a shared seam. Same underlying shape —
two artefacts, each correct in isolation, colliding on something neither author
was looking at — and **the corpus now has it in both directions within a single
day.** Neither was findable by reading; both needed the suite.

⚠️ **But the disposition is different and the difference matters.** Instance 1
was unobservable in play. This one is a genuine hardening failure: a module that
only behaves when handed a perfectly formed object is one an unlucky mod
interaction turns into a log full of `[LUA ERROR]`, which is precisely what
PT-62's own P11 forbids. Fixed by reordering the guards so the flag — a plain
field read — is tested before any method call, which is also the correct hot-path
order (this wrapper runs for every colonist on every heavy update, and for almost
every colonist the answer is "not flagged"). A regression lock is now case 11 of
the D12 probe.

**The question for job 7 is a design one, not a documentation one:** two of the
pack's opt-in modules now wrap the same shipped method, and their probes are no
longer independent when both are enabled. **Nothing in the project says who is
responsible for that**, and the answer that fell out here — every wrapper must be
inert for a foreign object before it touches one — is worth stating as a rule
rather than rediscovering per module.
