# C1 — the three never-opened monoliths, characterised and adjudicated

**2026-09-14.** Three read-only subagents, one per doc, fired by the orchestrator seat under
checklist **181** ("automate the monoliths, then audit them attended"). This file is the
**adjudication**; the three raw reports sit beside it in `monoliths/` and are **subagent output,
not findings** until graded here.

⛔ **Every claim below that is marked CONFIRMED was re-derived by this seat with its own command.**
Claims marked INHERITED were not. The distinction is the point of this file.

## 0 · What the three docs are, after the pass

| doc | size (git-blob) | state |
|---|---|---|
| `docs/agent/FIX_POLICY.md` | 50,756 B | ✅ characterised — `monoliths/C1_FIX_POLICY.md` |
| `docs/agent/WORKFLOW.md` | 59,724 B | ✅ characterised — `monoliths/C1_WORKFLOW.md` |
| `docs/PLAYTEST_HELP.md` | 62,709 B | ✅ characterised — `monoliths/C1_PLAYTEST_HELP.md` |

⚠️ **These are git-blob bytes.** See §4 — `wc -c` gives a different number for two of the three.

## 1 · ⛔ ACTIVELY WRONG — `PLAYTEST_HELP.md`, and the owner reads this one mid-playtest

This is the highest-stakes output of the pass. `PLAYTEST_HELP` tells the owner what to type and
what to expect; a wrong line costs a sitting.

**(a) CONFIRMED — the storm-meteor safety net does not exist.** Line 369 tells the owner that
`CheatMeteors(…, "storm", …)` is recoverable because *"`Fix_MeteorStormWedge` heals it
automatically"*. That module was deleted 2026-09-08 (`2dc1dbe`, 219 lines). Re-derived here:
`Fix_MeteorStormWedge` is in this seat's own deleted-module list for that commit, and
`bugs/F78.md:350` states the removal outright. ⇒ **An owner who triggers a storm on the strength
of that row gets a wedged storm and no auto-recovery.** Only the manual `g_MeteorStormStop` loop
still applies.

**(b) CONFIRMED — the fix-count the owner is told to expect is wrong by ~40%.** Line 431 says
*"the gate reads `74/74` in every configuration"*. `doccheck --emit-counts` reports **46
registered modules**. An owner seeing `46/46` has nothing in this doc telling them that is
expected rather than a broken install. ⚠️ The opt-in half of the same row (`1/8`) is still right.

**(c) CONFIRMED with a correction to the report — twelve console commands are dead.**
`CheatFillAllStorages` · `CheatResearchAll` · `CheatToggleAllShifts` · `CheatUnlockAllTech` ·
`CheatUnlockAllBreakthroughs` · `CheatUnlockBreakthroughs` · `CheatClearForcedWorkplaces` ·
`CheatSpawnPlanetaryAnomalies` · `CheatBatchSpawnPlanetaryAnomalies` · `CheatOpenAllDomes` ·
`CheatCloseAllDomes` · `SetGameSpeedState`.

⭐ **The mechanism, re-derived here and worth carrying:** 1.1.0 moved cheats from standalone
global `CheatXxx()` functions into a **data-driven `Data/CheatDef.lua` registry** whose `run =`
closures inline the logic. ⇒ **The capability usually still exists — via the cheat MENU — but the
console shortcut the doc hands the owner does not.**

⚠️ **A naive grep gets this wrong, and this seat proved it on itself.** Ten of the twelve names
are absent tree-wide. **Two are not**: `CheatResearchAll` and `CheatUnlockAllTech` return hits in
`Data/CheatDef.lua`. Those hits are **`PauseInfiniteLoopDetection("CheatResearchAll")` debug-label
string literals inside an anonymous `run = function(self)`** — *not definitions*. Verified: no
`function CheatResearchAll` anywhere. Their replacement is traced — `CheatDef` presets
`id = "ResearchAll"` / `id = "UnlockAllTech"`, `in_menu = "Cheats.Research"`, display names
*"Research everything"* / *"Unlock all Techs"*. ⇒ **The verdict holds for all twelve; the route to
it is a menu, not a console call.**

**(d) INHERITED, not re-derived — line-citation drift.** The report sampled a dozen surviving
`Cheats.lua` functions and found every cited `file:line` had moved (e.g. `CheatMeteors`
`:62`→`:40`, spot-checked and CONFIRMED by this seat). The functions still work when typed.
The doc's own framing — *"every entry checked in ModTools\Src"* — is no longer true of its
citations.

**(e) Open, honestly flagged by the report, NOT resolved:** save fixtures SAVE-A/D/E/F and the
Mirror-Sphere fixture could not be confirmed to exist under those names anywhere. Either they
were built under different real filenames, or the section is an unexecuted recipe list. ⚠️ If any
were built before 2026-09-08 they are branch-locked and unloadable (`EF-079`). ⛔ This seat did
not resolve it either — it needs the owner, not a grep.

## 2 · ⛔ `WORKFLOW.md` instructs agents to edit the append-only archive

**CONFIRMED.** `WORKFLOW.md` cites `MOD_DESCRIPTION.md` **6 times as a live per-commit target** —
rule 4 of "Per-fix discipline" (`:152-155`) says *"MOD_DESCRIPTION.md updated in the same commit
as the code change it describes."* Re-derived here: the only tracked copy is
**`docs/archive/MOD_DESCRIPTION.md`**, renamed there 2026-08-03 (`fe7ea49`), carrying its own
banner *"⛔ FROZEN during development — NOT authoritative."*

⇒ **A binding rule in the process doc tells every fix commit to edit a file that `CLAUDE.md`
declares append-only and never edited.** An agent following it literally either edits the archive
or recreates a live copy. This is the sharpest single defect the pass found in an agent-facing doc.

⚠️ **Unresolved and NOT this pass's to settle:** whether a modern doc plays that role today, or
whether the rule itself lapsed when the file froze. That is an owner/authoring answer.

## 3 · Tombstones, graded

| # | doc | finding | grade |
|---|---|---|---|
| 1 | `WORKFLOW` | `MOD_DESCRIPTION.md` ×6 — §2 above | ✅ **CONFIRMED** |
| 2 | `FIX_POLICY` | `:530` cites *"that guard was stripped from `Fix_TrainMinors`"*; the whole module was deleted in `2dc1dbe` | ✅ **CONFIRMED** — ⚠️ but see the harm note below |
| 3 | `PLAYTEST_HELP` | `Fix_MeteorStormWedge` — §1(a) | ✅ **CONFIRMED** |
| 4 | `PLAYTEST_HELP` | `Fix_TechDescriptionBuilding` — the MarsDebug-vs-retail lesson's worked example cites a deleted module | ⬜ INHERITED; the module's deletion is confirmed, the citation's placement is not re-derived |
| 5 | `WORKFLOW` | `public-docs/02_QA.md` — a prior audit fixed this citation everywhere except here | ⬜ INHERITED |
| 6 | `FIX_POLICY` | §5's `Opt_*` "N/A" notice | ✅ **CONFIRMED CORRECT** — self-declared, reasons still true. ⭐ A model of a tombstone done right; do not "fix" it. |

⚠️ **The harm in #2 is narrower than it reads.** The RULE stands — with the module deleted the
argument is if anything stronger. It is the **citation** that dangles: a reader following it finds
nothing. ⇒ One-line citation repair, not a policy change. ⛔ Do not let a size pass rewrite the
rule on the strength of this.

## 4 · ⛔ Two measurement hazards, both live, both found by this pass

**(a) A delta between two sampled dates is not an event at the midpoint.** The brief this seat
wrote — inherited from the handoff — asserted `WORKFLOW.md` *"shrank 12 KB around 09-01"*.
**FALSE, and the subagent refuted it rather than fitting evidence to it.** Re-derived here across
all 53 commits: **the file has ZERO commits between 2026-08-24 and 2026-09-09.** The real event is
`d56293a`, **2026-09-12, −24,329 B** (80,412 → 56,083). The old claim came from comparing 08-24
with 09-13 and attributing the difference to a date where the file was untouched.
⇒ **Read the whole size history, never two points:** `git log --format=%h -- <file>` then
`git cat-file -s $(git rev-parse <sha>:<file>)`.

**(b) ⚠️ `wc -c` and `git cat-file -s` ARE DIFFERENT UNITS IN THIS TREE.** Line endings are mixed
per file. Measured:

| file | worktree | git blob | Δ |
|---|---:|---:|---:|
| `WORKFLOW.md` | 60,648 | 59,724 | 924 |
| `PLAYTEST_HELP.md` | 63,429 | 62,709 | 720 (= its line count) |
| `STATE.md` | 12,526 | 12,526 | **0** |
| `FIX_POLICY.md` | 50,756 | 50,756 | **0** |

✅ **STATE's byte cap is UNAFFECTED (Δ0) — the cap machinery is sound.**
⚠️ **But the pending `RULES_HEADERS` header cap (1,024 / 2,048 B) must state WHICH UNIT it gates**,
or it is off by one byte per line on a CRLF file. That is an amendment owed before the brief
re-fires.

## 5 · ⭐ The method worth copying: `d56293a` is a SPLIT, not a deletion

CONFIRMED by this seat: `d56293a` moved the 416-line situational "Co-runs" protocol **verbatim**
into a new `prompts/perma/CO_RUNS.md` (+419) and added its prompts-map row in the same commit
(+1), so the `PROMPT MAP` gate stayed GREEN. Nothing was lost; the bytes went to a real file.

⭐ **The judgement that made it good:** the section's last ~25 lines were the **sign-off tiers** —
*standing policy*, not situational — and were deliberately **kept behind** and promoted to their
own heading. Folding them in would have filed a standing rule where only co-run sessions look.
⇒ **The split line is situational-vs-standing, not topic-vs-topic.** That is the transferable part.

⚠️ **A split does not stop growth, it resets the level** — the same commit appended the new R-A..G
verification rails, which is why the file grew again immediately.

## 6 · What the size actually is, per doc

- **`FIX_POLICY`** — §3a SAVE SAFETY is 10,781 B (21%); the top three sections are 60% of the doc.
  ~7,829 B (15%) is dated incident narrative wrapping 1–3 sentence rules. **22 commits, net
  additive except one clean in-place rewrite.** Largest single jump +6,317 B (`6db7457`, §2a+§2b,
  both still live — not padding).
- **`WORKFLOW`** — 26 headings. The "10 global rules" figure is real but **oversells the
  diversity: 7 distinct rule-texts across 10 counted occurrences, concentrated in just 2 of 26
  headings.** ⇒ Moving them to `CLAUDE.md` is a contained edit, not a doc-wide rewrite. ⚠️ R-D is
  orphaned from its R-A/B/C/E/F/G siblings and should be rejoined regardless of where they land.
  One self-declared **VOID** suite baseline (~900 B) still written out in full at `:537`.
- **`PLAYTEST_HELP`** — the command table alone is 15,955 B (25%). **No table of contents**, and
  the table starts past the halfway point of 721 lines.

## 7 · ⚠️ The class this pass exposed, bigger than any single tombstone

`2dc1dbe` deleted **36 modules**. Measured here: **all 36 are still cited somewhere in live
`docs/`**, and **22 of the 36 in the human-facing or process docs**. `FIX_POLICY` alone cites 6;
the subagent found 1, consistent with its own stated boundary.

⛔ **That is a count, not a finding.** Most citations are legitimate history — an entry SHOULD
record the module a fix shipped as. **The defect is only where a doc speaks in the PRESENT TENSE
about a module that is gone**, which is precisely what made §1(a) dangerous and §3 #2 harmless.
⇒ Separating those across 36 names is a mechanical pass and exactly what ck181 means by automate.
Module list: `monoliths/DELETED_MODULES_2dc1dbe.txt`.

⚠️ **Gate candidate, but NOT a clean one** — no machine can separate history from stale present
tense, so this can only ever be a WARN-with-list, never a RED. Raise it at the ck181 attended
session; do not build it on an agent's judgement.

## 8 · ⭐ Orchestration lesson — judge the report, not its summary

This seat told the owner the `PLAYTEST_HELP` agent's *evidence* was wrong on two names, on the
strength of its completion summary, which said *"zero hits each"*. **The report BODY was
accurate** — it said "gone **as a function**, logic lives inline in `CheatDef.lua:852`", which is
exactly right. The compression into the summary is what was wrong.

⇒ **A subagent's summary is a lossy rendering of its report, and grading the summary can convict a
correct agent.** Read the report before grading it. ⛔ This cost a wrong statement to the owner.

## 9 · What is owed out of this pass

1. **⛔ `PLAYTEST_HELP`'s three actively-wrong items are owner-safety, not tidiness** — they should
   be corrected before the next attended sitting, ahead of any size work.
2. `WORKFLOW`'s `MOD_DESCRIPTION.md` rule needs an owner answer, not an edit.
3. The `RULES_HEADERS` header cap needs its unit stated (§4b) before Codex re-fires.
4. The 36-module present-tense sweep (§7) is a delegable pass.
5. ⛔ **None of this closes anything.** Under ck181 these three reports are the **INPUT** to the
   attended you+me audit, not a substitute for it.
