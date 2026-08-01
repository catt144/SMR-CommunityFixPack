# Chain 7 — audit candidate DECISION packages (pre-cleared: the package's own §4 pass IS the decision)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first — especially the owner blanket pre-clearance block, which
changes this prompt's nature:** the owner pre-approved building every
package that PASSES its own §4 bar (as amended by prompt 1 — check which §4
is in force FIRST). **Evidence remains the gate; the ask is removed.** The
owner reviews the outcome table; they are not needed per-item.

**Staleness check: `git log --oneline -10` + `git pull`.** Read prompts
6/6b's outboxes below before packaging anything they swept.

## The decision packages (todo list first; one package = one item)

Work each package to the same standard as if the owner were deciding:
defect claim + Src evidence (on the C-entry), the intent tell, the
reachability tier YOU derive this session (§4 enumeration — the audit did
NOT do these), who benefits (§4a), the fix shape and cost. Then:
**PASSES all bars → record the pass on the entry and hand the spec to
prompt 8 (pre-cleared). FAILS any bar → close it honestly on the entry
(`wontfix` with grounds, or stays a candidate) — the clearance never
converts a failed bar into a build.** Borderline → that is what
stop-and-ask is for; the clearance covers clear passes, not judgment calls
you are unsure of.

1. **C33 — the track-shell leak (+ the F44 amendment).** The package the
   owner most needs: whole-track demolition leaks an undeletable invisible
   `TrackBase` shell, **and our own F44 mass-salvage path reproduces it**.
   Recommendation to present: file the F-row; amend `Fix_TrackSalvageWipe`
   to stop producing shells at source; adopt fredware's exact-signature
   shell deletion (temp-tables + `DoneObject`) as the repair shape + a
   sanitizer sweep for saves that already carry shells. Note the shell pins
   `demolishing = true`, the field F47 half-B stands down on.
2. **C22 — Saint blessing label mismatch.** Airtight Src evidence; the fix
   is a targeted label substitution (`GetTraitLabel("Religious")`) — cheap,
   data-shaped. Derive reachability (Saint is a breakthrough trait —
   R2-ish?); present.
3. **C23 — the three dust-devil scheduler defects.** Each sub-item is its
   own §4 subject (bundle lesson): the chance-as-count truncation, the
   `CurrentMap`/`MainMap` descriptor read, the missing `DustStormsDisabled`
   term. Present individually; they may get different answers.
4. **C24 — the asteroid-visit precedence bug.** Verified on the line;
   complements our F72 (we fix the false negative; vanilla's false positive
   passes through). Present with the empty-selection-screen player symptom.
5. **Anything prompt 6 promoted** (C04 F-row? C32 verdict? F35 extension?)
   gets the same package treatment here.

**For every YES: write the fix SPEC (module, technique per FIX_POLICY §1,
probe outline, intent statement, tier) into the BUGS entry and hand the
build to prompt 8's inbox.** For every NO/defer: record the reasoning on the
entry (a declined defect is a `wontfix` with grounds, or stays a candidate —
owner's wording rules).

## Scope fence

**In:** packaging, tier derivation, pass/fail dispositions, specs for
passing items. **Out:** building anything (prompt 8); re-sweeping (prompts
6/6b did it); any candidate 6/6b left at CANNOT-DETERMINE (it stays a
candidate — no package without settled evidence).

## Stop conditions

- A package's reachability derivation surprises you (R4, or intent turns
  ambiguous) → record the narrower true thing; never round up to "fixable".
  A borderline call you cannot make cleanly → stop and ask (the clearance
  covers clear passes only); route the question to the owner, not to a
  guess.

## What may not be claimed

No recommendation may cite the audit's tier column as reachability — the
audit graded witnesses, not call-site enumerations. Every package derives
its own tier this session or says it didn't.

## On completion

Outbox → `8_f86_phase4_conversion_batch_opus.md`: the approved-fix specs
(or "none approved"). Delete this file, commit, push.

## Notes from upstream

**From prompt 1 (2026-08-01) — the §4 amendment is APPLIED, and applying it
activated one decision on ALREADY-SHIPPED code. It is yours; it is not a
candidate package.**

The amended §4 is in force (`FIX_POLICY.md` §4, adopted verbatim from
`REACHABILITY_AUDIT.md` §4 under the owner's blanket pre-clearance) — that is
the "check which §4 is in force FIRST" answer for your header. Its new R3
bullet reads: **"R3 ships only as a §1.1–§1.4 patch; an R3 §1.5 full
replacement needs an explicit user decision (the F24 lesson)."**

**Two shipped items are in that combination and have no such decision on
record: F29 (items 1 and 3) and F57(a).** Both are R3 latent-by-data fixed by
§1.5 method replacements; both entries anticipated this in writing before the
amendment landed ("No action unless the owner wants the stricter line" — the
owner now has it). Add them as a **package 0** ahead of the candidate work:

- The bar is the same one you apply to candidates, run backwards: does the
  latent benefit justify a permanent §1.5 maintenance cost, given the fix is
  already built, probe-covered and A/B-clean?
- Three live answers, none presumed: keep both as replacements · convert to a
  §1.1–§1.4 shape where a wrapper can reach the defect · drop the latent
  halves. **F57(a)'s defect is a mid-function key write, so the conversion
  option may not exist there** — weigh it, do not use it to skip the ask.
- **This one is NOT covered by the blanket pre-clearance.** The clearance
  removed the approval step for adopting the rule; it did not pre-decide what
  the rule then asks about existing code. If the answer is anything other than
  "keep", it changes shipped modules — put it to the owner.
- Nothing here says either fix is wrong. F29's own entry is the project's
  worked example of an entry's self-description being false while the fix was
  right; do not re-litigate the defect claims.

(prompt 6 appends sweep verdicts here)
