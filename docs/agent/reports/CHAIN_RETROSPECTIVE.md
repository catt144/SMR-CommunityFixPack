# The First Chain — a full retrospective audit (written 2026-08-04, for the owner)

**What this is.** The complete audit of the project's first prompt chain —
18 self-consuming prompts, 2026-08-01 → 2026-08-03 — written by the terminal
QA session that verified all of it, as its last act. Chain performance, agent
performance, regressions, deviations, successes and failures, and the story
whole. A one-off, written for a human reader; the reusable lessons live in
`CHAIN_METHOD.md`, the findings in `CHAIN_QA_REPORT.md`, the drift ledger in
`DOC_STRUCTURE_REVIEW.md`. This document is the product of the work, on
display.

---

## 1 · The starting position — what was on the table on August 1st

Three problems the project had, at various points, treated as somewhere
between intractable and dangerous:

- **F86.** Two days earlier, the project had discovered its own code was
  being serialized into players' savegames and kept running after the mod was
  removed — one site killing a colony's meteors *permanently*, another
  throwing 98 errors per session, and the discovery had voided a prior audit
  clearance. The exposure list was a lower bound. Release was blocked.
- **A bug-list audit's unfinished business** — contested verdicts, candidate
  sweeps, decision packages, and a growing suspicion that the project's own
  records could not be trusted at face value (the "recorded facts are claims"
  lesson had already drawn blood twice).
- **A documentation system drifting from truth faster than protocols could
  patch it** — statuses stale within a day of being written, corrections that
  landed in one place and not the other, counts that needed unwritten
  exceptions to add up.

The chain was created by owner direction on 2026-08-01, co-designed with a
Fable session that made the per-prompt model placement call itself: Fable on
3 of 18 prompts (the spec, the highest-risk build, the terminal QA), Opus on
the other 15.

## 2 · By the numbers

| | |
|---|---|
| Prompts authored / consumed | 18 / 18, zero abandoned |
| Self-splits under context pressure | 5 (4→4b, 5→5b, 6b→6c, 8→8b/8c, 8b→8b2) — all clean, no state lost |
| Dropped or orphaned handoff items | **0** (all 17 close-out commits audited) |
| Wall-clock | ~3 days, most of it inside ~24 hours of active work |
| Fixes built and play-verified in-chain | F90–F97 (8), plus 8 §5.4/package-0 conversions |
| Entries closed by adjudication | F82 (wontfix-intent), F76 (refuted), C18/C19/C27–C30 and more |
| New defects found in our OWN shipped code | 3 (F87 pre-chain era, F88, F98 — one of them a fix that had *never worked*) |
| Playtest legs run (owner at keyboard) | 6 major (Tier-1 ×5-leg set, PT-58, PT-60, PT-61, PT-62 partial, F76 sitting) |
| Predictions written before runs / met | 40+ numbered; the misses were all diagnostic, not defects |
| Drift instances captured as evidence (rule 4b) | ~40, feeding an 8-class taxonomy |
| Release blockers at chain end | F86: **both proven sites repaired and verified**; gate now per-site with all dispositions recorded |

## 3 · The successes — what actually got solved

1. **F86, end to end.** The problem that blocked release went from "our code
   outlives uninstallation and we don't know the full exposure" to: exposure
   enumerated by five shapes (13 + one inert site), Tier 1 built and verified
   across five legs (the `Meteors` thread now survives uninstall *alive on
   vanilla's body*), Tier 2 moving every remaining blocking-body hook onto
   verified-synchronous seams, and the uninstall leg measuring **zero orphan
   errors where the founding measurement read 98**. The pack ended the chain
   holding zero §1.5 full replacements of the riskiest class.
2. **The route falsifications — the chain's signature move, in both
   directions.** A conversion recorded *"verified feasible"* turned out to
   have no route at all (F46 — correctly declined under a stop condition);
   a fix priced as *"the only route is owning a scheduler thread"* — a cost
   the owner had already accepted — turned out to have a layer-3 seam that
   made it nearly free (F97). Same week, same corpus, opposite signs. Nothing
   found those except the discipline of re-deriving routes instead of
   checking citations.
3. **The blind audit.** A sealed, fresh-context session graded all 66 fix
   premises with the project's records off-limits — and the pack's hit rate
   held (50/66 source-verified "yes"). Its three contested verdicts produced
   the F55 intent-tell finding the informed record had genuinely missed, and
   its closing question ("would a designer have written this on purpose?")
   independently reinvented the §4 policy bar — convergent validation nobody
   planned.
4. **PT-61.** The dust-devil A/B is the chain's evidentiary high-water mark:
   ten predictions written before the run, 29 scored waves, a within-session
   A/B lever, an uninstall half that self-healed on camera — and the vanilla
   arm catching the defect *on the save's own shipped preset with no mod
   installed*. The terminal QA later re-derived every scored claim from the
   raw log files.
5. **D12 under live redesign.** A module whose rule changed five times in one
   sitting under owner review — normally a red flag — came out the other side
   with every change recorded with reasoning, the hardest calls routed to
   independent adjudication, and the adjudication *upholding all five* with
   the key claim (veto ⊥ D07) verified from code.
6. **The honest negative.** F76 — a P1, the owner's own bug report — was
   measured, refuted, and closed as no-defect-established, with its
   unrefuted residue preserved (C41) instead of buried. A project that can
   close its owner's own report on evidence has a working epistemics.
7. **After the chain: the OG answer.** The terminal QA extracted the original
   game's bytecode and settled the one question the record said would decide
   F97's rate judgment — the multiply is original-game code, broken since day
   one. The instrument for "unsolvable" questions turned out to be
   willingness plus forty lines of Python.

## 4 · The failures and regressions — the honest ledger

1. **Two of the three load-time heals actually tested were defective**
   (`Fix_SaintBlessing` re-logging forever; `Fix_AstrogeologistExtractors`
   compounding +10% per load, unbounded). Invisible to source review, code
   review, and their own probes — caught only by the owner reloading a save.
   Worse: the untested heal backlog is larger than the tested set. This is
   the chain's most important *unresolved* risk class (the round-trip sweep
   is queue item 2).
2. **A shipped fix had never worked** (F98: `Fix_TechDescriptionBuilding`
   was a retail no-op from the day it shipped) — and every project surface
   said "fixed" truthfully, because `fixed` measured that code ran, not that
   it did anything. Found only because an entry's three-day-old "someone
   should re-check this" note finally got read.
3. **The record drifted ~40 times in three days** — stale banners above
   their own resolutions, specs authoritative about design and wrong about
   detail (7 of the prompt-7 spec packages had a defective supporting
   detail), a hedge that four documents quoted without the hedge, a scored
   table that silently dropped its tenth observation. The taxonomy exists
   *because* the volume was undeniable.
4. **The terminal QA committed the flagship failure itself** — updated D12's
   heading tag during adjudication and never re-synced the index row, after
   its own 110-row agreement pass had already run. The doccheck baseline
   caught its own architect on its first execution. No better argument for
   mechanical enforcement was ever going to be written.
5. **Primary evidence was lost to log rotation.** The founding 98-error logs
   and the Tier-1 leg logs aged off disk (~20-file cap) before the QA could
   re-read them. The doctrine holds on same-day transcriptions and bracketing
   reads — solid, but weaker than the files, forever.
6. **Probe/fix collisions, three in one day** — artifacts each correct in
   isolation sharing a flag or a seam (the `forbidden` scaffolding vs the 8c
   guard; D12's wrapper vs D07's probe stand-ins). None findable by reading;
   all needed the suite. One was a genuine hardening failure in shipped code,
   fixed and regression-locked.
7. **Routing had no notion of preconditions** — two items each hopped three
   prompts looking for a *situation* (a suite run; an enacted law) while
   every forward looked like diligence.

## 5 · Deviations from plan — and how each was handled

| deviation | handling | verdict in hindsight |
|---|---|---|
| 5 unplanned self-splits | rule 3 existed for exactly this; all clean | the rule is why context pressure never cost anything |
| C23 item 1's approved cost dissolved at build time | owner confirmed the route change before code | the best deviation of the chain |
| F46 conversion declined against its spec | stop condition honored; moved to group C with full reasoning | correct call, though the QA later found its §3a *grounds* inconsistent with F90's precedent (cost-benefit was the honest ground) |
| D12's rule rewritten 5× under live review | every change recorded; adjudication routed, not self-approved | the process working — but only because the recording discipline held |
| D10 parked mid-prompt by owner re-scope | nothing built; the re-derivation kept (3 spec claims falsified, F98+C39 found en route) | a "failed" build prompt that produced more value than the build would have |
| Prompt 11 couldn't self-consume as designed (needed the owner) | routed onward honestly | exposed a real hole: the unit of work is sometimes the keyboard, not the prompt |
| The seal was breached once, deliberately and scoped (F29 guard into prompt 7) | disclosed, recorded, carried as a caveat in the blind-audit annex | defensible, and the disclosure discipline is what made it defensible |

## 6 · Agent performance

**The volume tier (Opus, 15 of 18 prompts).** Consistently strong at:
executing against specs, forensic log work, honest self-reporting (the rule-4b
corpus exists because Opus sessions kept confessing ten-second fixes), and —
notably — *catching the tier above it*: prompt 8c falsified a Fable-era
route claim; the docs-chain sessions later found a fourth structural line
prompt 1 missed and a blocker the spec never anticipated, and handled both by
stopping and asking rather than improvising. Characteristic weaknesses, all
now countermeasured: detail-level errors inside otherwise-correct specs
(line numbers, method names, placements — 7 instances), occasional silent
tidiness (the wave-10 exclusion), and verification that checks citations
rather than routes unless explicitly ordered.

**The top tier (Fable, 3 of 18).** The spec prompt closed seven decisions and
enumerated an exposure set that held through two builds; the Tier-1 build
shipped the highest-risk code of the chain with all five legs passing; the
terminal QA re-verified the doctrine to primary evidence, adjudicated three
routed disputes, rejected one claim of the informed review on evidence, and
extracted OG bytecode to settle the rate question. It also produced the
chain's most instructive error (§4.4) — the two-place status flip it had
itself catalogued — which is the strongest available evidence that the
failure class is structural, not a competence gap any tier escapes.

**The owner.** Not a bystander in this system and shouldn't be audited as
one: the owner's one-line question retracted the VeryLow claim within the
hour ("caught in under an hour, and only because someone asked"); the owner's
pushback discipline overturned two diagnoses earlier in the project and kept
every session honest about attribution; the keyboard legs supplied the only
instrument (save/load round-trips) that could catch the heal-idempotence
class; and the provisional-approval pattern ("build it, not locked, QA
reviews it") is what let the chain move at full speed without laundering
judgment calls. The division of labor extends to the human.

## 7 · The epilogue — the method reproduced itself

Within a day of the chain closing, the same method ran three more times at
smaller scale: a 4-prompt docs-restructure chain (12,726 lines migrated with
zero bytes lost, verified by two independent parsers), a one-off checklist
redesign (with an owner acceptance checkpoint), and a one-off standing-prompts
redesign (Fable, adjudicating seven open observations). The follow-ons
inherited the disciplines — and improved them: the two-derivations-must-agree
rule was invented by an Opus session mid-migration, caught real corruption
byte-accounting could not see, and is now part of the method. The pre-commit
hook built on day one of the follow-ons caught the terminal QA's own
regression on its first run. The system now enforces its own structure on
every commit, whoever makes it.

## 8 · Final overview

The chain was asked to drain everything between a bug-list audit and an
adjudication, with a release-blocking save-safety defect in the middle of it.
It finished in about three days of work: the blocker repaired and verified at
the keyboard, eight new fixes play-verified, the record audited backward to
primary evidence, three disputes adjudicated, and the project's recurring
drift problem converted from an annoyance into a diagnosed taxonomy with
mechanical enforcement now standing guard.

What made it work was not any single session being brilliant. It was
structure: work that cannot linger (self-consumption), handoffs that cannot
be forgotten (written inbox/outbox), claims that cannot inflate (predictions
first, "what may not be claimed"), mistakes that cannot vanish (rule 4b),
decisions that cannot be laundered (owner routing), and a terminal adversary
whose job was to disbelieve all of it. Every failure the chain produced was
either caught by one of those nets or became a named class with a
countermeasure — and the one failure the nets missed twice (heal idempotence)
is first in the queue the owner takes to the keyboard.

**Verdict: the chain earned the method.** The owner called it the most
successful run at solving problems the project thought unsolvable since it
started — and the audit trail supports the sentiment with evidence. The
proof of the whole system is a small, quiet thing that happened on the last
day: the checker the chain built flagged the session that built it, the
error was repaired in daylight, and the record says so. That is what a
self-correcting engineering culture looks like when it is made out of
prompts.

---

*Written 2026-08-04 by the chain-12 terminal QA session (Fable) as its final
act, at the owner's request — the one report that is allowed to be proud.*
