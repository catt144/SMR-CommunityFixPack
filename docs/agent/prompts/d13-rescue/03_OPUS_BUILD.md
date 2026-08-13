# Chain prompt 3 — freeze the spec, build the artifact, correct every count

**Read `README.md` first — binding chain rules apply.** Staleness check (all
three repos), todo list. ⛔ **GATE CHECK BEFORE ANY WORK (README rule 7):**
prompt 2's verdict must be BUILD (its Notes below), and BOTH owner answers
(Q-A player story, Q-B channel/mod-shape confirmation) must be recorded on
`docs/PLAYTEST_CHECKLIST.md`. **Either missing → STOP: report which, commit
nothing but the report note, leave this file in place. The chain resumes here
when the owner answers.** Game closed throughout; nothing here launches.

## Job 1 — freeze the spec

From the QA-corrected `90_DERIVATION.md` + the owner's Q-A answer: write the
artifact spec INTO the derivation doc (one doc carries derivation → lists →
disposition → spec, so prompt 5 audits one chain of custody). The spec states:
detection (the curated list as embedded data — repo, name, kind, KEEP/REMOVE,
why), the clean pass order, the one-shot thread-restart set with per-thread
interval cost, what the player sees (report text), the version-skew statement
(which pack versions' residue it handles — say how a too-old or too-new save
is answered), the self-removal story, and the constitution-6d compliance
argument (why nothing of the artifact can persist).

## Job 2 — scaffold and build

* Scaffold the artifact repo per the QA-reviewed proposal (working name from
  prompt 1; LOCAL git, no remote unasked — README rule; junction installed
  but the mod NOT enabled — enabling is owner-only, and the verify prompt
  works junction-side per EF-055 regardless). Scaffolding depth per the
  proposal: the split's `SMR-OptInPack` scaffold is precedent, but this
  artifact is a single-purpose tool — carry PROVENANCE (what came from
  where), a README that answers the no-retraining questions AT ITS SIZE, and
  doccheck only if the proposal argued for it; do not cargo-cult the full
  pack apparatus where the proposal said it is not needed.
* Build the cleaner to the frozen spec. FIX_POLICY binds where it applies
  (fail-safe, never loud; self-checks return reasons, never error). Every
  Lua file parse-swept before commit.
* TestKit: teach the kit to see the artifact the way it learned the opt-in
  pack (a missing artifact is SKIP, never FAIL — it is legitimately absent
  from every config but the rescue ones), and write its probes: the clean
  pass on synthetic residue (KEEP survives, REMOVE goes, one-shot bound
  holds), the artifact-absent no-op, the version-skew answers. If you
  re-baseline the suite here, take the queued `FactionFundingCheck`
  PASS→SKIP repair (TestKit `62f03da`, comment on the probe) in the same
  measured commit and re-stamp the baseline everywhere it is quoted;
  otherwise leave it queued and say so.

## Job 3 — correct every count-stating doc (the derivation is authoritative)

Re-sweep BOTH repos' current docs for every count/denominator the derivation
supersedes ("≥13", "at least 13", "12 exposed", "five of the twelve", every
per-module denominator in the F86 reports). The D13 entry's location table is
the 2026-08-01 starting point with pre-restructure paths — translate and
re-sweep; your sweep's method line goes in the commit. Archive-tier files
(`docs/archive/`) are history and are NOT edited. Every corrected site cites
`agent/reports/D13_EXPOSED_SET.md` — which you create in this job by
promoting the QA-corrected derivation doc (the in-folder draft stays until
prompt 5 deletes the folder). Update the D13 entry itself: front-matter +
heading tag to `speced`/`built` per the truth at your close (edit order:
front matter first, then tag — doccheck red means you stopped halfway).

## Close

doccheck GREEN in every repo that has it; parse sweep GREEN; PROBE SWEEP line
in every result-bearing commit. Append your outbox to `04_OPUS_VERIFY.md`
`## Notes from upstream`: what shipped where (repos, shas), the spec's
verification-relevant promises (exact KEEP/REMOVE names the matrix must read,
the thread set, the version-skew answers), the fixture requirements you
foresee (which saves carry which residue classes — the split matrix's
FixtureCarry dumps say PT35FIXTURE carries fields + `MeteorLatch`; say what a
PRE-REWRITE-lineage witness needs and whether one exists in the save folder
BY NAME, or must be manufactured by a probe writing synthetic residue), and
every uncertainty. Delete this file in the same commit.

## ⛔ What you may not claim

- Not "the artifact works" — nothing launched; every claim here is
  static/probe-design tier and says so.
- Not "residue-zero" — that is prompt 4's measured claim; yours is the
  compliance ARGUMENT (no thread, no GameVar, no field, no closure — cited).
- Not "all docs corrected" without the sweep method stated and the archive
  exclusion honored.
- Not "suite baseline unchanged" if you touched any probe — recount or say
  which change is pending measurement.

## Notes from upstream (prompt 2 appends here)

**From prompt 2 (Fable QA gate, 2026-08-13). Verdict: ⭐ BUILD — with
MUST-FIXes, every one already applied in place in `90_DERIVATION.md`
(strike-and-supersede, tagged `[QA 2026-08-13]`). You build from the corrected
doc; nothing below is left for you to re-derive, but every MUST-FIX carries a
spec obligation you must honor.** Staleness at my run: fix-pack `8908367`,
opt-pack `a90d128`, TestKit `62f03da`, all clean (a parallel session's
uncommitted owner-decision edits — opt-in remote now PUBLIC — landed mid-run
and ride this commit; they do not touch the derivation's substance).

### The membership diff: ZERO differences, by a genuinely different route

Independent sweep, different axes than prompt 1's: `SetGlobal(` call-site
inventory + direct `_G` writes (catches the F87 latch paths) · whole-`Src`
regex classification of all 17 replaced names (252 occurrences, exactly ONE
non-call use = `TerraformingDisasters.lua:313`, E1's route — **§1.4 re-confirmed
independently**, including the `PersistableGlobals` whitelist mechanism read
at `persist.lua:119-143`) · literal persisted-name token sweep · own-thread /
`rawset` / `= function` / notification-closure / label-modifier axes · the
instrument re-run on the preserved 80-row list (verdict pattern reproduced,
same four false positives, Colonist again absent from the Idle summary line).
Chases that settled to no-finding: `Fix_RainsDeadlock:195` (entry value is
vanilla's `RainsDisasterLoop`, never replaced), `Opt_NoHomeless:52`
(comment-only mention), the opt pack's `ProcessToggle` rawsets (UI windows,
§2c's class), `Fix_MilestoneCrash:41`'s popup (vanilla-valued params, vanilla
id). §1.3's reconciliation verified at source 4-for-4 (DestroySilent decider
at `Train.lua:183-184` + `Demolishable.lua:91/104`; MirrorSphere's yield is in
the nested closure at `MirrorSphere.lua:836`; RCTransport dispatch body;
both recovered `Colonist:Idle` yields — second cite corrected to `:1796`).

### MUST-FIXes applied — and what each obliges YOU to do

1. **D2 (and D1) — the GameVar rows were wrongly treated as cleaner-visible.**
   Mod-registered GameVars are DROPPED on any load without the registering mod
   and never re-saved (`persist.lua:136-142`, verified at source). D2's REMOVE
   was unexecutable; its "least-certain placement" dissolves. **Spec: the
   cleaner's list must NOT contain D1 or D2, and the artifact must NEVER
   register a `GameVar` to reach a value (that re-persists the name — 6d).**
2. **§8.3 "no thread surgery whatsoever" — struck.** Doubt 4 is SUSTAINED
   (captured frames unreachable, §2a inert-accepted wholesale), but the
   artifact's population includes PRE-REWRITE-LINEAGE saves the current pack
   never touched (uninstalled before Tier 1/2) — the D13 entry's own expected
   leftover classes. **Spec: keep TWO one-shot bounded heals, vanilla bodies
   only: `Meteors` restart only-if-dead/foreign (cost: one 35-115 h re-roll,
   stated to the player) and the rains stale-ACTIVE/dead-loop heal via
   `FinishRainProcedure` / recreate-onto-vanilla-`RainsDisasterLoop` (the
   pack's proven C34 recipe; cost: one rain re-roll). Never repeated;
   skip-and-report on ambiguity. Your Job 1 already demands the per-thread
   cost lines.** Checklist item 17 got an owner-facing QA update saying
   "smaller, not zero"; the (c) recommendation is unchanged.
3. **Count corrections inside the draft** (the project's own defect class):
   §4.1's summary arithmetic ("Removed: 5", "14−5+1") contradicted its own
   table — now 14−4=10, +E3+E12=12; RT thread count 2→**3**; "14 distinct
   persisted names"→**16** (15 rows, F35 family as one, D15 as two).
4. **Cite corrections:** D9's second cite `:173`→`:201` (write) + `:209`
   (guard); `Colonist:Idle` `:1795`→`:1796`; D11 `:339` and D12 `:105`
   verified CORRECT (variable-keyed writes my literal grep couldn't see).
5. **Report dialog placement (spec requirement added to §8.3):** the
   `WaitMessage` report MUST ride a real-time thread (00_Core:498's pattern);
   the clean pass stays synchronous. A yield on the load-path GT frame would
   be the exact shape the artifact exists to avoid.

### Rulings you can lean on

* **E7 defanged** (still INFERRED, no longer load-bearing): the own-thread
  axis is exhaustive — exactly 6 GT creations in both trees, E7's the only
  yield-free body — so neither answer to the created-never-run question
  changes any list or disposition; the 6f gate covers its worst case. An
  optional prompt-4 probe leg is sketched in §6 doubt 1.
* **Doubt 5 settled** (option tables are not save state — mechanism verified).
* **Doubt 2 extended** (zero `Sleep`/`Wait*` tokens anywhere in
  `UIStatUpdate` :2932-3133); still conditional on indirect helpers, still
  disclosed, not a gate item.
* **§4.3's doc-correction list verified complete** by an independent sweep
  (all 9 files confirmed; no unlisted file; TestKit + opt-pack docs clean).
* **KEEP/REMOVE ran per-name, both directions**: D15's removal path is the
  module's own base-position call (`SetLabelModifier(label, id, nil)`,
  labels "Drone"/"Consts", ids at `:64-65`); D5/D6/D7 absence semantics
  verified at `:81-83`/`:65-70`/`:97`; D10's re-add guard at
  `90_SaveSanitizer:69-76` confirms a pattern sweep would re-break F35.
  6f routings verified by my own reads (gates present only in StormWedge,
  `:145`/`:156`; E5/E6/E7 ungated; the stale `:138-141` comment confirmed —
  EF-023's closing claim is FALSE and rides your Job 3).

### Observation, not a MUST-FIX

E9/E10 (and the "frame" wording generally): both Idle wrappers end in strict
tail calls with yield-free pre-work; under proper-tail-call semantics those
frames are elided before vanilla's Sleep, so E9/E10 are likely over-included.
Kept deliberately — same basis as the historical counts, no disposition
changes either way, and un-measurable without a game. Do not cite them as
capture-proven.

### What I did NOT get to (named residue for prompt 5)

* **No game launch** — E7 unmeasured (optional probe sketched); the
  tail-call elision observation unmeasured.
* **D10 still UNSAMPLED** — ROUTED to prompt 4: the damaged-fixture leg must
  plant/manufacture an F35-affected witness and read the modifier back
  (absent ≠ refuted; the house rule requires the condition SAMPLED).
* **E12's indirect-helper yield audit** — token scan only; the conditional
  tag stands.
* The parallel session's owner-decision edits (checklist item 15, STATE's
  remote line) were in the tree uncommitted at my close; they ride my commit
  unreviewed beyond a read of their diff.

**Addendum (same session, 2026-08-13, post-verdict decision batch):** the
owner answered everything you were gated on and more — all recorded on the
checklist. For you specifically: **Q-A = (c)** (launch dependency REAFFIRMED
after an explicit challenge; build ≠ publish — store publication is a
release-time call) · **Q-B = mod-shaped CONFIRMED** · **item 19 = GO** (the
inserted `02b_OPUS_GATES.md` runs before you; read its outbox above yours) ·
**naming RATIFIED as proposed** (display "Save Rescue", mod id
`SMR_CommunitySaveRescue`, log tag `[CommunitySaveRescue]`) · ⭐ **the owner
pre-created the artifact's PUBLIC remote themselves:
`github.com/catt144/SMR-CommunitySaveRescue` (empty)** — scaffold locally,
set that as `origin`, push; align the local folder name to the remote
(`C:\Dev\SMR-CommunitySaveRescue`) rather than the proposal's shorter
`SMR-SaveRescue`. Also decided the same day, opt-in side (not yours to act
on, but your doc sweeps will see it): display name = "Community Fix Pack:
Opt-In Modules" (swept, opt-pack `e17586b`), default-OFF ratified.