# The Prompt-Chain Method — a playbook from the run that proved it (2026-08-03)

**Written by the chain-12 QA session at the owner's request, at peak knowledge:
this session verified the full 18-prompt chain end to end (inbox audit, flip
sampling against primary logs, consistency pass, adversarial adjudications),
so the claims below about *why* it worked are evidenced, not theorized.**
The chain ran 2026-08-01 → 2026-08-03 and closed problems the project had
classed as intractable — F86 save-safety (discovery to verified repair of both
proven leak sites), the 66-premise blind audit, six approved fixes built and
play-verified, three owner-routed adjudications — with **zero dropped items
across 18 self-consuming prompts** and every sampled claim verifying against
primary evidence.

This document is the reusable method. The authoring mechanics it builds on are
`agent/WORKFLOW.md` "Authoring a prompt" (elements 1–7) — read those first;
this adds the chain-level structure and the lessons.

---

## 1 · What the method is, in one paragraph

Decompose a large effort into **many focused prompts sized to finish
comfortably in one session's context**, numbered in a folder that acts as a
**self-consuming queue**: each prompt ends by appending its handoff notes to
the NEXT prompt's inbox (or to whichever later prompt owns a discovered item),
committing, and **deleting its own file in the same commit**. The folder's
emptiness is the objective done-condition. The final prompt is always an
**adversarial backward QA** with fresh context that trusts nothing forward.

## 2 · Why it worked — mechanisms, each with its evidence from this run

1. **Self-consumption forces completion semantics.** A prompt cannot linger
   half-done: it finishes, or it self-splits at a clean commit boundary
   (rule 3) into a continuation that is a first-class chain member. Five
   splits happened (4→4b, 5→5b, 6b, 8→8b/8c, 8b→8b2); all were clean; the
   QA found no split that lost state. *Contrast: every long-lived "standing"
   document in this project drifted; no consumed prompt did.*
2. **Written inbox/outbox makes handoffs verifiable — and they verified.**
   Nothing owed ever lived in a session's memory. The QA audited all 17
   close-out commits: every outbox landed in the successor + the terminal QA
   prompt + the manifest, in one commit. Zero orphaned notes in 18 prompts.
3. **Mandatory re-derivation beat inheritance, repeatedly, in both
   directions.** The chain's biggest wins came from prompts ordered to
   re-derive premises rather than trust specs: a route recorded *impossible*
   existed (C23 → F97 shipped at a fraction of its approved cost); a route
   recorded *"verified feasible"* did not exist (F46, correctly declined);
   three approved-spec claims fell on re-derivation (D10) and two builds
   shipped because their premises held byte-verbatim (D12). **Rule to carry:
   the builder re-verifies the ROUTE even when told not to re-derive the
   design — every route failure this week sat above individually-correct
   citations.**
4. **Predictions written before runs.** PT-58/60/61/62 all recorded numbered
   predictions before any leg ran, which made results falsifiable, made
   misses diagnosable (PT-60's 79/79 vs predicted 73/79 exposed an
   account-state fact, not a defect), and made the QA's log-verification
   possible at all.
5. **Owner decisions routed, never absorbed — with provisional approval as
   the unlock.** "Build it, but it's not locked — the QA reviews it" (F97)
   and "let the QA look before we make hard decisions" (D12) let building
   proceed at full speed *without* laundering judgment calls into faits
   accomplis. All three routed adjudications were decidable downstream
   because the routing preserved the evidence and the open question.
6. **The adversarial terminal QA is where the method pays compound
   interest.** Fresh context + a different model + "every 'done' is a claim"
   found what forward motion structurally cannot: stale banners above their
   own resolutions, a silently excluded observation in a scored table, a
   heading tag contradicting its own entry, and a permanent evidence loss
   (log rotation) — while *confirming* the work itself everywhere it sampled.
7. **Blind controls are worth their cost.** The sealed BLIND_AUDIT (a fresh
   session grading all 66 fix premises with docs off-limits, examined only by
   the terminal QA) independently validated the pack's evidence base AND
   surfaced findings the informed record had missed (the F55 intent tell).
   The seal held because it was written into every prompt as a named rule
   with a required handoff attestation.
8. **Mistake capture as corpus, not shame (chain rule 4b).** Every drift
   instance — even ten-second fixes — was appended to the QA's evidence list.
   Result: a 40-instance corpus that produced a structural diagnosis
   (`DOC_STRUCTURE_REVIEW.md`) instead of another round of patching. *A
   silently-corrected instance is destroyed evidence* proved to be one of the
   most valuable rules in the chain.
9. **Scope fences and stop conditions were honored under pressure.** Prompt 8
   stopped rather than force a conversion whose route had dissolved; prompt
   11 refused to self-close a P1 where the reporter was also the adjudicator.
   Fences work when they are written in the prompt, not assumed.
10. **The model division of labor is not a convention — it is what makes the
    method affordable AND accurate, and the owner rates it load-bearing.**
    (Owner, 2026-08-03, on the record: the chain was co-designed by the owner
    with a top-tier session, and **the per-prompt model assignment was
    specifically the Fable authoring session's own decision** — the owner
    could guess at it but not be sure, and rates the resulting division
    load-bearing: *"that model division of labor is the only way this
    works"*.) The economics, both
    directions: run everything on the volume tier and accuracy drops exactly
    where error compounds; run everything — or even half — on the scarce top
    tier and usage limits stretch a ~24-hour chain across one to two weeks.
    **This chain placed the top tier on 3 of 18 prompts (~17%)**: the spec
    (prompt 3 — where a wrong decision poisons every downstream build), the
    highest-risk build (prompt 4, Tier 1 — save-safety code with the worst
    failure mode), and the terminal QA (prompt 12 — the adversary everything
    else is checked by). The volume tier ran the sweeps, the spec-guided
    builds, the legs, and the records — work where the spec-plus-re-derivation
    discipline bounds the cost of any single error. Routing lives in the
    FILENAME only; prompt bodies stay model-neutral so the owner can re-route
    per task. **The placement rule to reuse: the scarce tier goes where errors
    COMPOUND (design, adjudication, the final audit) and where independence
    matters (fresh-context QA); the volume tier goes where errors are CAUGHT
    downstream by a leg, a probe, or the QA.**

## 3 · Failure modes observed, with the countermeasure each earned

| failure | instance | countermeasure (adopt at authoring time) |
|---|---|---|
| Routing without preconditions | two items hopped 3 prompts each (a suite-run debt; C40's enacted-law need) | every routed item carries **TAKEABLE WHEN <condition>**; situation-gated items go to the checklist as riders, not to prompts |
| The manifest no prompt owns | the README chain table went stale about the chain (row 8b2) | the manifest gets an explicit owner: each prompt's close-out updates its OWN row as part of the deletion commit checklist |
| Briefs staler than entries | prompt 7's brief contradicted the C33 entry it described | briefs cite entries; sessions act on the ENTRY, and the brief says so |
| Specs authoritative on design, unreliable on detail | 7 of the prompt-7-era specs had a defective supporting detail; all 7 shapes survived | "do not re-derive the design" never means "do not verify the route"; tag spec details with provenance (MEASURED / SOURCE / INFERRED) |
| A prompt that needs the keyboard | prompt 11's jobs 2–4 needed the owner; the file could not self-consume as designed | mark attended prompts as such up front; split attended and unattended halves at authoring time |
| Context-edge risk | none bitten — because rule 3 existed | keep the self-split rule verbatim; never push a job to the edge of a window |
| Evidence rotation | the founding logs aged off disk (~20-file cap) before the QA could re-read them | any leg whose numbers a status flip will cite gets its log archived in the same commit |

## 4 · The chain template (assemble from these parts)

0. **Author the chain WITH the owner — and size decides who assigns the
   models (owner rule, 2026-08-03):**
   - **5 prompts or fewer:** the owner decides the model placement themselves
     if comfortable doing so.
   - **6 prompts or more:** any agent scoping the effort should RECOMMEND
     that the chain setup — the decomposition AND the per-prompt model
     placement — be done by a top-tier (Fable) session, unless the owner
     overrides.
   This codifies how the proven chain was actually made (owner + Fable
   collaboration, 2026-08-01; the placement was Fable's call, which the
   owner could sanity-check but not derive). The assignment is a judgment
   about *where errors compound versus where they get caught* — a read on
   the work's internal risk structure that grows superlinearly with chain
   length: at 5 prompts the owner can hold the risk map; at 18 nobody but
   the authoring session can. The division of labor in §2.10 is a design
   input, not an afterthought. Budget
   the scarce tier at roughly 15–20% of prompts, placed at the compounding
   points; if the plan needs more than ~half the chain on the top tier, the
   decomposition is wrong (the specs are not carrying enough of the load).
1. **A folder** (`docs/agent/prompts/<effort>/`), a **README manifest** (table:
   number · file · model · owner-needed? · what it drains; strike rows on
   consumption), and **binding chain rules** in the README: inbox/outbox,
   route-don't-drop (unsure → STOP AND ASK), self-split, defect filing,
   drift-evidence capture, WORKFLOW elements 1–7, commit convention, any
   sealed documents.
2. **Prompt bodies**, each with: staleness check first (`git log` + `git
   pull`); the job; a **scope fence** (in/out); **stop conditions**; **"what
   may not be claimed"** (the honesty rail — the single best guard against
   success-theater); live todo requirement; self-deletion instruction; a
   `## Notes from upstream` section others append into.
3. **Decision points**: anything that is genuinely the owner's is packaged
   with a recommendation and ROUTED (to a decisions surface the owner
   actually reads — see `DOC_STRUCTURE_REVIEW.md` R10), optionally with
   provisional go-ahead ("build, not locked, QA reviews").
4. **Ordering**: strict only where work products interfere (the 8b-before-8c
   rule existed because two fixes shared a subsystem and one unrun leg);
   otherwise declare independence explicitly so prompts can run in any order.
5. **The terminal prompt, always**: an adversarial backward QA, fresh
   context, ideally the strongest model — inbox audit, owed-work sweep,
   consistency pass, verification *sampling against primary evidence*, and
   the folder-empty gate. Budget it generously; this run's QA produced new
   primary evidence (the OG bytecode answer) because it had room to chase.
6. **Optional but proven**: a blind-control document produced by a fresh
   context with the record off-limits, sealed from every prompt except the
   terminal QA. Use when the effort's conclusions would benefit from an
   unanchored second derivation (audits especially).

## 5 · Worked outlines for the three named uses

**A — Large project effort** (the form this chain already is): phase-0
measurements → spec (re-derived, decisions closed) → build (split by unit) →
leg prompts (attended, predictions first) → records close-out → backward QA.

**B — Audit chain**: sweep prompts over the target corpus (sized ~10 items
each, verdicts with evidence grades) → decision-package prompts (one §4-style
package per contested item, owner-routed) → a blind control run in parallel
under seal → build/remediation batch → verification legs → terminal QA that
examines the blind control against the informed record and adjudicates
divergences on evidence.

**C — Prelaunch chain (the project's actual next large effort — sketch, not
authored):**
0. Gate: playtest campaign items that block release are done (PT-62 remainder
   etc.); doc-structure adoptions decided (R-list) so the chain builds on the
   final layout.
1. **D13 derivation** — the cleaner's target list derived from scratch (its
   entry already forbids inheriting any recorded count); the chain-12 QA's
   installer table and marker feed (`CHAIN_QA_REPORT.md` §1.4–1.5) are its
   starting evidence, not its answer.
2. **D13 build + leg** (uninstall procedure + save-rescue artifact; attended
   verification with predictions).
3. **MOD_DESCRIPTION rebuild** from entries (R11's release gate), including
   the owner's relabel-package decisions (QA report §3) — every claim
   verified against BUGS, none inherited from the frozen draft. **The player
   FAQ compiles in this same step**: `grep -rn "\[FAQ\]" docs/ Code/` collects
   the tagged sources (15 tags / 10 files as of 2026-08-03, three inside the
   frozen draft itself — the grep must include `archive/`), per WORKFLOW's
   `[FAQ]` convention; each tag's claim gets the same verify-against-entries
   treatment as the description, and tags whose behaviour has since changed
   are dropped, not inherited.
4. **Release-gate sweep** — per-site §3a disposition table complete, fpk
   extraction diff, probe sweep, version/latch checks, the public README.
5. **Doc overhaul execution** (the R15/R12/R13 scripted migration, if not
   already done) + public-facing generation.
6. **Terminal backward QA** — full backward check with a launch-blocking
   stop condition; nothing ships if the folder is not empty.

## 6 · The two sentences to keep if everything else is lost

**Structure work so that finishing is the only way a prompt can disappear,
and route every discovery to a written owner instead of a memory.** And:
**end every chain with a fresh-context adversary whose job is to disbelieve
the chain — the run that produced this document was that adversary, and the
method survived it.**

*Cross-references: `CHAIN_QA_REPORT.md` (the verification this playbook rests
on), `DOC_STRUCTURE_REVIEW.md` (the drift taxonomy and the doc-side
mechanisms), `agent/WORKFLOW.md` (per-prompt authoring elements).*
