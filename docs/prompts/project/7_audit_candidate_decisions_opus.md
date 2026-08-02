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

### From prompt 6 (2026-08-01) — your item 5 is now concrete: ONE package, ONE tier decision, and two things you must NOT package

**Read `BUG_LIST_AUDIT.md` §10 before item 5.** It is new, and it contradicts
§9 twice. Full trails are on the BUGS entries.

#### 5a. ⭐ ONE NEW PACKAGE: **F90** (was C04) — dust storms break underground cables/pipes

Filed as an F-row because the sweep closed the chain with no gaps, not because
anyone decided anything. **Nothing built. The defect claim and the intent tells
are done for you; the tier, the §4a answer and the fix shape are yours.**

- The whole chain, and both intent tells, are on the **F90** entry with
  file:line. Short version: `City:HourlyUpdate` gates the break pass on
  `HasDustStorm`, which is hard-wired to `MainMap`, then hands it a fragment
  list containing the elevator-merged cross-map fragment; the victim is picked
  by `table.rand` over every connector in it. The sibling production pass
  sixteen lines above **does** guard the shared-fragment case, with a comment
  saying fragments span cities.
- **The hard part is the SHAPE, and it is a genuine FIX_POLICY §3a problem.**
  The bad line is `SupplyGrid.lua:677`, mid-function, behind the roll — a
  wrapper cannot reach it without re-implementing the roll, and a body copy is
  what F86 constrains. Two layer-2 candidates are named on the entry; the
  cheaper-looking one is vetoing an off-`MainMap` `BreakableSupplyGridElement
  :Break` during a dust storm rather than touching the picker at all. **Weigh
  that before defaulting to a replacement** — GromGor's working fix IS a body
  replacement, and copying his shape would walk straight into §3a.
- **Two scope questions are flagged on the entry, not decided.** The merged
  element count also inflates the *surface* break rate (`IsBreakable` :695 and
  the probability at :673 both count underground elements) — that is an intent
  question, and it may not be a defect at all. And GromGor's version would
  index a nil element on an empty surface list; ours must guard rather than
  inherit the shape.

#### 5b. ⚠️ A TIER DECISION YOU OWN THAT IS NOT A CANDIDATE PACKAGE: **F04**

**The audit's §9 demotion of F04 (GOLD → BRONZE-B2) rested on C32 being the
better mechanism match, and the sweep took that reasoning apart.** C32 has no
route in current Src; the specific inference that carried the reassignment —
"an asteroid leaving range fits label rebuilds on map transitions" — is **false
of Src**, there is no label rebuild on a map transition; and the observable
that made C32 look real (GromGor's fix firing in the wild) fires on
destroyed-but-unrebuilt buildings, which is not a defect. Separately, the
onset condition the reporter named cannot occur unattended on 1.0.7 at all.

**This is yours because it is a decision, and the sweep deliberately did not
make it.** The three live options are written out on the F04 entry: restore
its witness and tier, leave both entries witness-less, or hold for the
corrected live rider. **The limit that constrains all three:** the sweep read
1.0.7 only and the thread's reports are 1.0.6-era, so source alone does not
discriminate the two mechanisms *for that reporter's build*. **F04's own defect
claim is untouched and stands on its sibling tell either way — do not
re-litigate it.**

#### 5c. Two things that must NOT become packages

- **C32 — DOWNGRADED, not closed, and not a package.** No route in current Src;
  no F-row; no fix. It keeps its row as history. Your scope fence already says
  a candidate left without settled evidence stays a candidate — this is that.
  (The live rider that could still settle it was **rewritten**, not deleted:
  its old trigger no longer occurs unattended and its old "any non-zero count
  is the defect" rule would have confirmed C32 on the first meteor strike.
  Corrected row in `PLAYTEST_CHECKLIST.md` §6.)
- **C35 (new) — a real gap, an unproven harm, explicitly NOT for you.** The
  fredware-#11 comparison found zero overlap with F67/F68/F70/F71 and located
  a clean sibling asymmetry (the payload path tears down the command-centre
  connection with no wait where the takeoff path waits). But nobody has shown
  a unit stranding, fredware ships it beta and off by default, and his remedy
  removes a player action — a §4 behaviour change, not a repair. **It needs a
  live repro first**, named on the C35 entry. Packaging it today would be
  packaging a description.

#### Housekeeping that lands on you

- **F35 needs nothing from you.** Its live half was measured by prompt 2 and
  its source half re-checked here; scope confirmed both ways, no F-row, no
  extension. Item 5's "F35 extension?" question is answered: no.
- **STATUS's index count was stale by two rows again** and has been re-derived
  by counting (now **102 rows = 90 F + 12 D**, plus **35 C**). If your packages
  file or close anything, re-derive it the same way rather than incrementing.
