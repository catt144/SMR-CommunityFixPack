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

**If a keyboard control is needed for C, STOP AND ASK the owner** — do not
improvise a game leg inside the final QA.

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
