# Audit the 1.1.1 build

One-off audit brief. A builder on another vendor executed
`GAMEPATCH_1_1_1_BUILD_fanout_level_6.md`: three rebases (the track unit, F125, F121),
sixteen retirements, three manifest hygiene items, and one reconciliation of the shared
files. This brief judges that work. It was authored at `16ff1aa`, **before any of the
build existed**, so that its questions come from the archived source and the settled
evidence rather than from the builder's account of itself.

You are not the builder and you do not finish its work. Where the build is wrong, you
say so with evidence; you do not repair code.

## Fill at firing

Filled 2026-09-23 when the build landed.

- **Commit range to judge:** `16ff1aa..45578d4` — one commit, "Preserve native 1.1.1
  behavior and retire superseded fixes". Build report:
  `docs/agent/reports/GAMEPATCH_1.1.1_BUILD_2026-09-23.md`. It names a TestKit companion
  commit `aa47d3e` in `B:\Dev\SMR\SMR-BugFixPack-TestKit`; that repo is outside this
  audit's scope except to confirm the fix-pack side does not depend on unlanded kit work.
- **The builder's reported departures** (its report §"Challenges and departures", read
  them there in full rather than from this summary):
  1. **F121 gained a saved-provenance condition** beyond the exact reason and event
     interlocks, because the same saved fields can describe a *healthy* 1.1.1 disable
     after the story finishes. The load-only repair accepts only pre-1.1.1 provenance and
     leaves already-resaved ambiguous state untouched. Rests on
     `CommonLua/Savegame.lua:775` rewriting the saved revision. **No save file was
     inspected** — this is the departure with the largest unexamined surface.
  2. **F125 used input wrappers rather than a new migration-body copy**, which the
     builder says revises a dated F52 1.1.0 design note that had rejected a distance
     pre-wrapper. It claims the bounded argument crosses only the passage lookup
     threshold.
  3. **F126's deciding consumer includes an assertion before the unknown-id fallback**;
     the builder's first control bypassed it and was corrected.
  One suggestion not acted on: C55's historical duplicate-geometry premise.
- **Changed dispositions:** none reversed — all three rebases and all sixteen retirements
  landed as authorized. Departures 1 and 2 change *how* a repair was built, not whether.
  Two owner legs were opened as checklist ck209 and ck210.

## Authority and outcome

The owner settled this on 2026-09-23: the build does not certify itself, and the audit
runs on a different vendor than built it. This brief authorizes reading, measuring, one
report, and corrections to records the build wrote where a claim is wrong. It does not
authorize code changes, finishing an unfinished unit, reverting the build, a release, or
launching the game.

End state: every behaviour claim the build makes is confirmed, corrected, or marked
unproven, on evidence; and the owner knows what is safe to ship, what is owed to play,
and what is still wrong.

## Judge on evidence, not conformance

This is the clause that matters most here, because you may be reading a specification
you helped write.

The severity ranking (`reports/FULL_BODY_PRIORITY_2026-09-23.md`) and the adjudication
(`reports/GAMEPATCH_1.1.1_ADJUDICATION_2026-09-23.md`) were produced by this seat on
2026-09-23. **They are claims, not authority, and they are not your position to
defend.** A build that departed from them may be right. If the builder challenged one of
those reports and its evidence is sound, record that the challenge holds and correct the
report — do not rank a departure as a defect because it departs.

Likewise: a unit that matched the brief exactly can still be wrong, and a unit that
ignored it can still be correct. Conformance is not the test. The test is whether the
shipped behaviour is right on archived build 1.1.1.405907.

**Do not trust the build report's summary of itself.** Read the diff and the archived
source. Where the report and the diff disagree, the diff is what shipped.

## What to verify

Depth by consequence. The three rebases carry silent, permanent failure modes; the
retirements are mostly loud or inert.

### The track unit — hardest, and first

The build had to start from the complete 1.1.1 `TrackGridElement:DemolishAndSplitTrack`
body and retain **all four** vendor repair-site semantics — repair-site exclusion,
correct-array removal, repair-site rehome with `repair_cgs` rebuild, repair-aware
`ProcessAllElements` (`TrackElement.lua` :484-488, :519-525, :598-614, :628-632;
re-derive) — while reapplying only F44/F91/F116.

- Diff the installed body against the archived 1.1.1 body span by span. A missing vendor
  semantic here corrupts saves silently: this is the single highest-consequence read in
  the audit.
- `Fix_BrokenTrackSalvage` should be gone with its registrations and probes, F45's
  evidence preserved in its entry, and no stale pin left behind.
- `Fix_TrackSalvageRefund`'s `Demolish` wrapper (`:195-250`) was an open question owed to
  this unit: whether its snapshot survives the 1.1.1 array rules. Check that it was
  answered with evidence, not asserted.

### F125 `Fix_VacuumWalks`

The complete 1.1.1 direct **and** multi-leg migration state machine must survive in
`Colonist:TryToEmigrateToDome`; only proven vacuum passage thresholds may be repaired.
`Colonist:MigrateStep` is new in 1.1.1 and absent from 1.1.0. If the build patched the
second site, check that its reachability in vacuum was traced rather than assumed; if it
declined to patch it, check that the refusal was recorded with the trace.

### F121 `Fix_CloggedBuildingRelease`

A narrow, synchronous, idempotent **load-only** repair for the exact old saved reason and
state, working with vanilla's Duration present. No timer, field, UI or new-event path.
Verify healthy 1.1.1 events stay vanilla-owned and the legacy fixture actually heals.

### The sixteen retirements

For each: was the replacement body **and its consumer** traced on the archived tree
before deletion, or was a disappearance treated as proof? Then, by name across
`items.lua`, `metadata.lua`, the module lists, desk harnesses, the TestKit probe
inventory, documentation and release surfaces — is every reference gone, and is any
non-retired module's reference gone by accident? Bug history and archived evidence must
be updated, not erased.

F122, F123 and F126 were active defects and each needed a two-sided pack-on/pack-off
control proving deletion restores native behaviour. F123's pack-off leg was still owed
at build time — the earlier retail attempt short-circuited at "fix pack not loaded"
rather than calling the vanilla function. Check it was actually run, not inherited.

### The reconciliation and the gates

The reconciliation was the reason the two briefs were merged, so check it landed as one
pass against the final state: counts from their commands, reconciled **by name** rather
than by total. Re-run the gates yourself — `python tools/bodycheck.py --selftest`,
current bodycheck on the pack, patchcheck selftest, `python tools/doccheck.py` — and
diagnose any red yourself rather than accepting the build's account of it.

Every decisive control must be shown able to fail. Take at least two of the build's
controls, revert the guard in a scratch copy, and confirm the control goes red. A
control that passes on a reverted guard proves nothing, and a vacuous control looks
exactly like success.

### The builder's challenges

The build brief granted the builder and its subagents permission to question the record,
and required challenges to be reported even when overruled. Adjudicate each one on its
evidence: sound, unsound, or unproven. A sound challenge the builder overruled is a
finding. Silence where you expected a challenge — on the 33 KEEP rows, the ranking, or
the bounded retail A/B — is worth a line too.

## Live work list

Put this list in the todo tool before the first write; keep one unfinished unit in
progress and add discoveries rather than hiding them.

- [ ] 1. Derive the range; read the diff before any report prose
- [ ] 2. Track unit verified span by span against the archived 1.1.1 body
- [ ] 3. F125 and F121 verified, including the refusals and their traces
- [ ] 4. Sixteen retirements: replacement + consumer traced, references gone by name
- [ ] 5. F122/F123/F126 two-sided controls verified as run
- [ ] 6. Reconciliation checked by name; gates re-run; two controls shown able to fail
- [ ] 7. Builder's challenges adjudicated; record corrections applied
- [ ] 8. Report committed; this prompt and its map row deleted

## Scope and stops

In scope: the build's commit range, the pack's module bodies, the archived 1.1.0.403908
and 1.1.1.405907 trees, one audit report, and corrections to records the build wrote.

Out of scope: code changes, completing an unfinished unit, reverting the build,
release/version/store work, shipped game files, and launching the game. A wrong unit is
reported and, if the owner wants it repaired, that is a separate brief.

Report instead of continuing only if: (1) a newer game build lands; (2) the build is
incomplete enough that auditing it would mean finishing it; or (3) a shared path carries
peer changes that cannot be integrated without overwriting them.

## Claim limits

A source read is not `tested`: SOURCE on build 1.1.1.405907, desk-MEASURED when a named
harness ran, pending owner play until its checklist leg runs. A matching body hash is not
compatibility. A passing gate is not a correct build. Retail claims inherit the completed
A/B's stated limits — it was not single-variable, and neither leg met its zero-error
acceptance condition — so nothing resting on that run may be reported as clean-boot
verified. Say what a verdict depends on when you give it.

## Lifecycle

One-off. Delete this prompt and its row in `docs/agent/prompts/README.md` in the result
commit. The audit report and the corrected records are the durable record.
