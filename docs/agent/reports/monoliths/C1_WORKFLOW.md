> ⛔ **SUBAGENT OUTPUT — THIS IS A CLAIM, NOT A FINDING.** Produced 2026-09-14 by a read-only
> characterisation agent under checklist **181**. Only the items graded **CONFIRMED** in
> [`../C1_MONOLITHS.md`](../C1_MONOLITHS.md) were re-derived by the orchestrator seat; everything
> else here is unverified. ⚠️ At least one claim in this set was materially imprecise — read the
> adjudication first, and never quote a number from this file without re-deriving it.

# C1 — docs/agent/WORKFLOW.md characterisation

Target read in full at HEAD (`f78d7a8`, working tree matches, 60,648 B). Read-only; no writes made.

## 1. ⭐ The size story — the "2026-09-01 shrink" premise is WRONG

**Command:** `git log --format='%h %ci' -- docs/agent/WORKFLOW.md` piped through `git cat-file -s $h:docs/agent/WORKFLOW.md` for every commit that touched the file (full table run, 53 commits, Aug 1 → Sep 14).

**There is no commit touching `WORKFLOW.md` between `7667b65` (2026-08-24, 70,354 B) and `5d6af93` (2026-09-09, 70,766 B).** Size is flat across that gap — nothing shrank on or near 09-01. `git log --format='%h %ci %s' --since=2026-08-29 --until=2026-09-03` shows real activity that week (F110, release/upload work, checklist rulings) but **zero of it touches this file**.

The size trace actually runs:

| commit | date | size (B) |
|---|---|---|
| e85f8d1 | 08-01 | 14,542 |
| 7667b65 | 08-24 | 70,354 |
| 5d6af93 | 09-09 | 70,766 |
| 38875a2 | 09-12 18:xx | **80,412** (peak) |
| **d56293a** | **09-12 19:38** | **56,083** ← the real shrink, −24,329 B |
| 0c6fd1f…7500625 | 09-13 | 57,738 → 58,597 |
| f78d7a8 (HEAD) | 09-14 | 59,724 (working tree: 60,648) |

The task brief's four milestone numbers (14,542 / 70,354 / 58,597 / 60,648) are real sizes at real commits (`e85f8d1`, `7667b65`, `7500625`, HEAD) — but stringing them together implies a monotonic dip "around 09-01" that never happened. The actual shrink is **−24 KB on 2026-09-12, not −12 KB on 09-01.** ⚠️ Correcting the brief's premise rather than fitting evidence to it (house rule: don't make the evidence fit the claim).

### The method: a verbatim SPLIT to a new perma-prompt, not a deletion

Commit `d56293a` ("Co-runs moves out to a standing prompt (D5), and the verification rails land"), 2026-09-12 19:38:33.

- **Moved out verbatim**: the "Co-runs" section (416 lines) → new file `docs/agent/prompts/perma/CO_RUNS.md` (419 lines incl. a 2-line new header explaining the move and D5).
- **What did NOT move**: the section's last ~25 lines — the "sign-off tiers" block, owner-adopted 2026-08-04 — deliberately kept behind, promoted to its own `## Sign-off tiers` heading (WORKFLOW.md:578). Rationale stated in the commit body: that block is *standing policy for every leg*, not situational co-run procedure; moving it with the rest would file standing policy where only a co-run session looks — the exact failure the split exists to prevent.
- **What was added, same commit**: `## Verification rails (adopted 2026-09-12, owner)` (R-A…R-G, WORKFLOW.md:867-915) appended at the end — new content, not reclaimed space. Numstat: `63 insertions(+), 416 deletions(-)` in WORKFLOW.md; `419 insertions(+)` in the new CO_RUNS.md; `+1` in `prompts/README.md` (the map row for the new file).
- **Verified myself, not just on the commit's word**: `grep -c "never silently" docs/agent/WORKFLOW.md` → 1; same on `CO_RUNS.md` → 0 — matches the commit message's own verification claim exactly. `diff` of the pre-move span against the new file's body is byte-identical except for the 2-line added header (I re-derived this directly rather than trusting the commit text).

**Where the bytes went:** almost entirely into a new, real file (`docs/agent/prompts/perma/CO_RUNS.md`, ~35 KB), not into the archive and not deleted. This is exactly the trap this project's own rules name: *"a move or rename reads as a deletion."* Nothing was lost — the sign-off tiers carve-out shows unusual care (verified against a citation dependency, `C44.md:108`).

**Is the method worth copying onto other monoliths?** Yes, with two caveats: (1) it required identifying a genuinely *situational* sub-procedure cleanly separable from *standing* policy inside the same section — that boundary-drawing is the hard part, not the mechanical move; (2) it was verified with a grep-count spot-check, not a full byte-diff — cheap, but not proof against silent edits inside the moved span (I did that fuller check myself here and it holds).

## 2. Section inventory (26 headings, sorted by size)

| bytes | line | heading |
|---|---|---|
| 6,297 | 26 | Binding authoring rules (adopted 2026-08-03) — 8 numbered authoring rules (markers, provenance words, TAKEABLE-WHEN, log archiving, decision mirroring, INDEX generation, doccheck, STATE byte-budget) |
| 5,703 | 349 | Testing checklist per fix — the per-fix test procedure |
| 5,662 | 257 | ⛔ Probe hygiene — hard gate before any testing (owner rule) |
| 5,222 | 605 | Release steps — pre-upload checklist, heavily dated/ruling-cited |
| 4,966 | 742 | Authoring a prompt / job brief — required elements (incl. R-C, R-D pointers) |
| 3,836 | 468 | ⛔ Cheats on playtest saves are NORMAL (owner rule 2026-08-12) |
| 3,183 | 527 | ⛔ BOTH MODS LOADED is normal (owner rule 2026-08-12) |
| 2,906 | 682 | Release marking — tags not branches |
| 2,843 | 867 | Verification rails (R-A..G, adopted 2026-09-12) |
| 2,843 | 220 | ⛔ What a GREEN does NOT license — trust table |
| 2,535 | 186 | The order of operations (source-diff instruments) |
| 2,106 | 826 | `[FAQ]` tag convention |
| 2,066 | 431 | ⛔ Log review: never silently discount a line |
| 1,802 | 920 | Writing in a shared tree (traps) |
| 1,706 | 578 | Sign-off tiers (stayed behind from the Co-runs split) |
| 1,494 | 3 | Reading path for a new session |
| 1,077 | 157 | fpk verification — release gate |
| 759 | 244 | Where the artefacts are |
| 713 | 116 | Layout |
| 705 | 144 | Per-fix discipline |
| 695 | 174 | After a game patch — source-diff instruments (binding) |
| 664 | 129 | Install for testing |
| 492 | 909 | What these rails are not |
| 210 | 916 | Trust by source |
| 138 | 576 | Co-runs (tombstone heading pointing at CO_RUNS.md) |
| 26 | 1 | title |

Total 60,648 B reconciles (measured by Python byte-offset walk over heading lines).

## 3. Tombstones — rules citing a referent that is gone

All three below are records of something the doc still talks about as live that isn't. Move/rename traced in each case, per house rule.

**(a) `MOD_DESCRIPTION.md` — cited 6 times as a live per-commit target; it was archived over a month before any of this doc's 09-12→09-14 growth.**
- WORKFLOW.md:152-155 (Per-fix discipline, rule 4): *"One commit per fix or tight group; agent/bugs/ updated in the same commit; MOD_DESCRIPTION.md updated in the same commit as the code change it describes."*
- Also cited as live at lines 640, 664, 848, 860, 862 (Release steps and `[FAQ]` sections).
- **Proof the referent moved**: `git log --follow --name-status -- '*MOD_DESCRIPTION.md'` shows `R099 docs/MOD_DESCRIPTION.md → docs/archive/MOD_DESCRIPTION.md` at commit `fe7ea49` (2026-08-03). The archived copy's own banner (`docs/archive/MOD_DESCRIPTION.md:1-6`): *"⛔ FROZEN during development — NOT authoritative … Moved to `docs/archive/` 2026-08-03 … Its fix lists, counts and F76 explainer are as of that date and are not maintained."* `docs/README.md:34` independently confirms: `MOD_DESCRIPTION.md (frozen)`.
- **Verdict**: rule 4 of "Per-fix discipline" instructs every future fix commit to update a file the project itself has called non-authoritative and frozen since 2026-08-03 — six weeks before this doc's most recent edits. This is the single clearest tombstone in the file.

**(b) `public-docs/02_QA.md` — cited once as an authority for a still-binding table; the file was consumed and deleted by its own chain rule.**
- WORKFLOW.md:623-624 (Release steps, `ignore_files` table): *"⭐ Re-derived per mod 2026-08-13 (`public-docs/02_QA.md`) — the three lists are NOT the same:"* — followed by a table that IS still the live rule.
- **Proof the referent is gone**: `docs/agent/reports/STORE_BUILD_AUDIT.md:207` (Sweep 6, staleness audit): *"`02_QA.md` cited five times — the file was consumed and deleted | confirmed → fixed. Chain rule 2 deletes a prompt when it is consumed, so every such citation is born dead. Re-pointed at `PUBLIC_DOCS_DESIGN.md`, which carries the same corrections inline and survives."* That audit fixed the citation everywhere it swept (`CAPTURE_SITTING.md`, `PUBLIC_DOCS_DESIGN.md`, `PLAYTEST_CHECKLIST.md`) — but its sweep scope was "both drafts" (the public-facing pages), not `WORKFLOW.md`, which still carries the dead citation.
- **Verdict**: the citation is decorative (the table it introduces is fine on its own), so nothing is actually at risk — but it is a proven-dead pointer that a prior audit already fixed everywhere else and missed here.

**(c) The 2026-08-12 suite baseline inside "BOTH MODS LOADED" — self-declared VOID, but the dead numbers are still fully written out (see §5, it's also a superseded-in-place case).**

## 4. Dated session records (narrating a day, candidates for `docs/archive/SESSION_LOG.md`)

| span | lines | bytes | what it narrates |
|---|---|---|---|
| Cheats section owner quote | 471-478 | ~620 | Verbatim owner quote from mid-`corun-pt60` sitting, 2026-08-12 |
| Both-mods owner quote + dead baseline | 530-555 | ~1,750 | Verbatim owner quote from `split-optins` authoring + the VOID 2026-08-12/08-13 suite-count narrative (see §5) |
| `[FAQ]` tag derivation note | 847-849 | ~210 | *"re-derived from `grep -rn "\[FAQ\]" docs/ Code/` on 2026-08-01 — the previous list named a tag in `MOD_DESCRIPTION.md` that did not exist"* — a one-time audit narrative, itself now stale (see §3a) |
| Release steps' `.gitattributes`/`.github` derivation | 623-633 | ~950 | *"Re-derived per mod 2026-08-13"* / *"✅ `.github/` is no longer a question … since the site moved out"* — a specific one-time survey result, not a process statement |
| SMR Tool Kit attribution paragraph | 514-524 | ~830 | *"2026-09-14 (smrtk 07, as built)"* — current, but written as a dated status note rather than a standing rule |

**Boundary on this section**: I did not exhaustively hunt every dated citation (the doc cites owner-ruling dates as provenance throughout, which is this project's normal authoring convention per `WORKFLOW.md` rule 2, "Provenance words" — most of those are load-bearing, not narration). The five rows above are the ones that read as *narrating what happened on a day* rather than *stating a rule with a dated citation*.

## 5. Superseded-in-place (original text still sits there in full)

**One clear case**, and it's load-bearing evidence of the doc's rot pattern: the 2026-08-12 suite baseline inside "BOTH MODS LOADED" (WORKFLOW.md:537-555, **1,320 B** of the dead-numbers text spans lines 537-549, ~900 B of that; the correction itself is lines 550-555, ~420 B).

- **Dead half** (still fully present, lines 537-549): *"⭐ MEASURED BASELINE (cell a2, 2026-08-12, audit-recounted from `archive/spa2_Mars.exe-20260812-18.44.24.log`): `fix pack present: 74/74` · `opt-in pack present: 8/8` · suite ~~`78/0/10/0 of 88`~~ ⭐ RE-MEASURED 2026-08-13 (`archive/rs_r0_*`): `78 PASS / 0 FAIL / 16 SKIP / 0 ERROR` of 94 …"* — three full sentences of specific counts, a log filename, and a module-load order.
- **Correction** (lines 550-555): *"⛔ THAT SUITE BASELINE IS VOID as of 2026-09-09 (`100_DOCSWEEP`). It was measured on the 74-module pack against game 1.0.7; the pack is now 44 modules, the kit is a different 94-probe set rebuilt for 1.1.0 … The new baseline is the next attended `SMRTest.RunAll()` after the hotfix-2 upload, which re-stamps this line — none is written here."*
- **Cross-check**: `docs/agent/STATE.md`'s "OWED" line independently points back at this exact dead span: *"the first `RunAll()` on the probe kit (re-stamps `WORKFLOW.md:537`, VOID since 09-09)"* — corroborates both the line number and the VOID status from a second document.
- **Verdict**: the numbers are explicitly dead (VOID) but nobody has struck them; they're just followed by a bigger warning. ~900 B of pure dead weight, easy first cut for a byte-reduction pass, and unlike the two tombstones above this one is self-admittedly dead rather than silently stale.

## 6. ⭐ The "10 global rules" — found, and genuinely two clusters, not ten independent lines

`grep -n -i "10 global" docs/PLAYTEST_CHECKLIST.md` → the phrase "WORKFLOW.md's 10 global rules" comes from the pending ck179 doc-rules-architecture ruling, sourced from Codex's automated inventory (`docs/agent/reports/RULES_HEADERS_INVENTORY.json`, HEAD `968c58e`, 852 rule occurrences project-wide). That inventory's per-doc table (`RULES_HEADERS.md:38`): `docs/agent/WORKFLOW.md | 0 doc-local | 123 task-local | 10 global | 0 redundant | 0 dead | 133 total`.

**The number is real: exactly 10**, and I pulled the 10 tagged entries directly from the JSON (`rules[]` where `file == "docs/agent/WORKFLOW.md"` and `classification == "global"`). All 10 sit inside just **two headings**:

| # | line(s) | quote | genuinely global, or task-scoped? |
|---|---|---|---|
| 1 | 872-881 | **R-A** · *"Verification is routed three ways… VOLATILE-external… VOLATILE in-repo… DURABLE structural… fingerprint…"* (4 JSON entries, one section) | **Global** — applies to any claim involving a number, anywhere, any task |
| 2 | 883-886 | **R-B** · *"Never read a file to prove a negative. Absence is settled by a grep, never by reading… a negative in a compressed artifact is not a sample at all."* | **Global** — general epistemic rule, not tied to any one task |
| 3 | 891-893 | (sub-bullet of R-C) · *"Every check must be scoped so it CAN fail… Ask 'what would make this vacuous?' before the reader acts on it."* | **Global** — but note: R-C's own opening line (888, "Brief element 9 — the derived-facts block") is classified **task-local**, while this one sub-bullet inside it is tagged global. The classifier split one numbered rule across two tiers. |
| 4 | 898-900 | **R-E** · *"Run, then write… Every count carries the command and the filter that produced it. A total is not a set."* | **Global** |
| 5 | 907 | **R-G** · *"Record the executed model at close-out, read from the transcript, never assumed."* | Borderline — applies once per session close-out, not mid-task; I'd call it global by frequency (every session ends) even though it fires once |
| 6 | 928-929 | *"⛔ All sessions share ONE git identity. `git log --author` cannot attribute work. Identify by sha + diff…"* | **Global** — true for any git command in this shared tree |
| 7 | 930-937 | *"⛔ A pathspec is only HALF a commit fence… stage your own hunks…"* | **Global** — true for any commit touching a shared file |

That's 7 distinct rule-texts covering 10 JSON-counted occurrences (R-A's paragraph counted as 4 sub-spans). **Not classified global, and staying task-local per the inventory**, in the same two sections: R-C's own header line, R-D (which is oddly not even in this section — it lives at line 819, inside "Authoring a prompt / job brief", separated from its siblings R-A/B/C/E/F/G), R-F ("size the verification by owner-observability" — a task-sizing heuristic, correctly task-local).

**Honest read**: the count is right (10), but "10 global rules" oversells the diversity — it's 7 rule-statements, concentrated in exactly 2 of the doc's 26 headings (`Verification rails` and `Writing in a shared tree`), both already near the end of the file. Moving them to `CLAUDE.md` is a contained edit, not a doc-wide rewrite, and R-D's separation from R-A/B/C/E/F/G is itself worth fixing regardless of where the rules end up living.

## 7. Duplication against siblings (FIX_POLICY.md, CLAUDE.md, STATE.md only)

Two confirmed exact-rule duplicates against `CLAUDE.md`, both already flagged by Codex's inventory (`R2`, `R3` in `RULES_HEADERS_INVENTORY.json:redundancy`) and re-verified here by quoting both sides myself:

**R2 — doccheck-before-commit:**
- WORKFLOW.md:103-104: *"Run `python tools/doccheck.py` before committing doc changes — red blocks. One-time setup: `git config core.hooksPath tools/hooks`."*
- CLAUDE.md:18-19: *"Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up once: `git config core.hooksPath tools/hooks`."*
- Same rule, same sentence shape, both files, word-for-word overlap on the operative clause.

**R3 — owner-decision mirroring:**
- WORKFLOW.md:54-56: *"Owner-decision mirroring (R10). Every item needing the owner's call is mirrored into `docs/PLAYTEST_CHECKLIST.md` → 'Decisions waiting on you' (one line + pointer)… An owner decision recorded only in an entry or a report is not considered asked."*
- CLAUDE.md:23-24: *"Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → 'Decisions waiting on you', never only in agent docs."*
- WORKFLOW.md's version is the fuller canonical statement (adds marker-update and regeneration duties); CLAUDE.md's is a shorter restatement of the same mirroring clause. Not fully redundant — WORKFLOW.md carries extra operational detail CLAUDE.md lacks — but the core sentence is duplicated.

No FIX_POLICY.md or STATE.md duplication found by heading-name search (`grep -n -i "probe hygiene\|per-fix discipline\|install for testing" docs/agent/FIX_POLICY.md` → no hits) — **boundary stated**: I did not do a full sentence-level diff against FIX_POLICY.md (784 lines) or STATE.md (127 lines) beyond targeted greps and a read of STATE.md's head; a fuller cross-check would need Codex's whole-inventory pass, which already ran and found 0 additional redundant pairs touching WORKFLOW.md against FIX_POLICY.md or STATE.md specifically (only CLAUDE.md pairs appear in the redundancy list for this file).

## 8. Verdict — if this doc had to lose 40% of its bytes (~24 KB) without losing a binding rule

**Cut list, cheapest/safest first:**
1. The dead VOID baseline (§5, WORKFLOW.md:537-549, ~900 B) — already declared dead by its own text; strike to one line pointing at STATE.md's OWED item.
2. The `[FAQ]` section's derivation narrative (§4, lines 847-849, ~210 B) and the "re-derived per mod 2026-08-13" / `.github` narrative in Release steps (§4, lines 623-633, ~950 B) — replace with the still-live conclusion only, drop the "how we found out" story.
3. Fix, don't cut, the 6 dead `MOD_DESCRIPTION.md` citations (§3a) — each is a landmine (an agent following rule 4 literally would edit a frozen archive file, or worse, recreate a live copy). Repoint to whatever the current pre-launch player-text draft actually is (needs an owner/authoring-side answer — I did not chase what replaced it, out of scope for a read-only pass).
4. The two owner-quote blocks in §4 (cheats, both-mods — together ~2,400 B) are the biggest single dated-narrative mass. The project's own convention treats a direct owner quote as *authority*, so I would not cut the quotes themselves, but the surrounding scene-setting ("Adopted mid-sitting during `corun-pt60`…") could move to `docs/archive/SESSION_LOG.md` with the binding rule restated as a bare numbered list, the way "Binding authoring rules" already does it.
5. Fold R-D (line 819) next to its siblings R-A/B/C/E/F/G (867+) — zero byte savings, but fixes a structural defect the same pass would otherwise leave behind.

**What I'm unsure about:**
- Whether `MOD_DESCRIPTION.md`'s six citations have a correct modern replacement target, or whether the whole "update the player-facing doc in the same commit" rule itself lapsed when the file froze — I did not trace what (if anything) plays that role today; that needs an owner or authoring-seat answer, not a grep.
- Whether R-G ("record executed model at close-out") is truly global-by-frequency or is better read as task-scoped to session-wrap prompts specifically — I flagged it borderline rather than asserting either way.
- I did not fully verify the CO_RUNS.md move byte-for-byte across its entire 419 lines (I diffed a ~420-line slice and it matched except for the 2-line added header); a single-line silent edit inside the bulk of the moved body is possible but unlikely given the commit's own stated verification method and my grep-count cross-check landing exactly where the commit claimed.
