# Game 1.1.1 — repair the three modules that must survive

One-off build brief. The 1.1.1 full sweep has settled the disposition: repair
`Fix_CloggedBuildingRelease`, `Fix_TrackSalvageWipe`, and `Fix_VacuumWalks`; do not
reopen whether they remain in the pack. The outcome is three 1.1.1-safe modules that
preserve their still-needed behavior without overwriting the vendor's new work.

This brief was authored from fix-pack base `2812098` and the game-patch artifact commit
that added this file. Start with `git log --oneline -6`, `git pull`, and
`git status --short`; compare the named modules, F121/F124/F125, and the patch report
from `2812098..HEAD`, then re-read only moved evidence. Invoke `doc-editing` before
record edits and `smr-bug-library` for status/evidence changes. Apply
`docs/agent/FIX_POLICY.md`, `docs/agent/WORKFLOW.md`, and the repository instructions.

If this is run unattended, execution and audit use different owner-selected models.
The three work units may be analyzed in parallel; their shared registrations, tests,
and final verification are integrated by one coordinator. The filename's fanout level
is a routing hint, not permission to weaken the evidence gate.

## Authority and evidence

The standing game-patch job authorizes a build prompt, not code changes in its own
session. This fired brief authorizes the three repairs below. All line numbers are
from archived build 1.1.1.405907 and must be re-derived with `rg -n` before use.

| module / filing | settled defect | falsifying read |
|---|---|---|
| `Fix_CloggedBuildingRelease` / F121 | Vanilla's new one-hour Duration prevents new C85 cases, but no decoded 1.1.1 migration clears a building already saved with reason `789863173059`; our `shipped_defect_gone()` exits before its load sweep. | Search the whole decoded 1.1.1 tree for that reason and saved state. A shipped migration that clears it cancels the retained load half. The adjudication ran it 2026-09-23: one hit, `Data/StoryBit/BuildingClogged.lua:8`, no fixup, and the Duration thread is created only at firing (`ClassDef-Effects.generated.lua:2772-2790`). |
| `Fix_TrackSalvageWipe` / F124 | The current full replacement loses the new repair-site exclusion, correct-array removal, repair-site rehome/`repair_cgs` rebuild, and repair-aware `ProcessAllElements` semantics at `TrackElement.lua:484-488,519-525,598-614,628-632`. F44 itself remains. Adjudication 2026-09-23: this unit also retires `Fix_BrokenTrackSalvage` (its REMOVE premise holds only once this rebase runs, and its `:35` pin on the same body would otherwise stay BODY-CHANGED) and re-reads `Fix_TrackSalvageRefund`'s `Demolish` wrapper (`:195-250`) against the rebased body. | Compare the complete installed replacement with the current archived body. If all four semantics already survive, F124 is wrong. |
| `Fix_VacuumWalks` / F125 | The old-body replacement erases 1.1.1's multi-leg task logic in `TryToEmigrateToDome` and does not repair the new duplicate threshold in `MigrateStep`. F52 itself remains. | Trace both passage decisions and every caller. If the second site is unreachable in vacuum, record that and do not patch it speculatively. |

The durable source read is
`docs/agent/reports/GAMEPATCH_1.1.1.405907_2026-09-23.md`; use the bug index to
open only F121, F124, F125 and their named predecessor entries. Patchcheck and
bodycheck are routers, never dispositions.

## Required result

1. **Clogged legacy migration.** Preserve a narrow, synchronous, idempotent load-only
   repair for the exact old saved reason/state even when vanilla's Duration is present.
   Remove the daily/live repair and do not add a timer, field, UI, or new-event path.
   Prove healthy 1.1.1 events remain vanilla-owned and the exact legacy fixture heals.
2. **Track salvage rebase.** Start from the complete 1.1.1
   `DemolishAndSplitTrack` behavior, retain all vendor repair-site semantics, then
   reapply only the marked F44/F91/F116 changes. Prefer a smaller composable shape if
   it actually preserves behavior; do not force a full replacement merely to minimize
   the diff. Exercise curved/short salvage, a live repair site spanning a split,
   `repair_cgs`, survivor arrays, refunds, shells, and `skip_track_process`. In the same
   change, delete `Fix_BrokenTrackSalvage` with its registrations and probes (preserve
   F45's evidence in its entry), and re-verify `Fix_TrackSalvageRefund`'s `Demolish`
   wrapper against the rebased split body.
3. **Vacuum migration rebase.** Preserve the complete 1.1.1 direct and multi-leg
   migration state machine. Repair only proven vacuum passage thresholds. Cover a
   direct final leg and an intermediate leg, breathable controls, reservations,
   shuttle/train continuation, cancellation, and no-passage fallback.

Each module must earn a 1.1.1 behavior decline or another FIX_POLICY-compliant guard;
an updated hash alone is not a decline. Record save footprint and removal residue for
every changed exposed site. Extend existing desk fixtures where possible, require a
positive control, and create scratch guard-reverted variants to show each decisive test
can fail. Do not launch the game: put only owner-required retail legs on the checklist.

## Live work list

Put this list in the todo tool before the first write. Keep one unfinished
commit-and-verify unit in progress; add discoveries rather than hiding them.

- [ ] 1. Orient, refresh evidence, and confirm all three filings still describe HEAD
- [ ] 2. F121 load-only migration implemented and falsifiable desk controls green
- [ ] 3. F124 rebase implemented; vendor repair-site semantics and F44 controls green
- [ ] 4. F125 rebase implemented; direct/multi-leg vacuum and breathable controls green
- [ ] 5. Shared registrations, manifests, TestKit coverage, and module lists reconciled
- [ ] 6. Independent audit of every behavior claim and changed full-body seam
- [ ] 7. Parse/body/patch selftests, focused harnesses, doccheck, and clean boot recipe
- [ ] 8. Entries/report/checklist updated; exact paths committed; this prompt and map row removed

## Scope, stops, and claim limits

In scope: the three modules, their existing desk/TestKit coverage, registrations,
F121/F124/F125, the retirement of `Fix_BrokenTrackSalvage` inside the F124 unit, one
build report, and owner-only checklist legs. Out of scope: the REMOVE brief's modules,
unrelated fixes, release/version/store work, game files, and a game launch.

Report instead of continuing only if: (1) a newer game build lands; (2) a load-bearing
owner ruling conflicts with this authority; or (3) a shared target has unresolved peer
changes that cannot be integrated without overwriting them.

Do not claim source-read as tested, that a body hash proves compatibility, or that the
absence of a decoded caller proves an engine route impossible. Supported replacements
are SOURCE on build 1.1.1.405907, desk-MEASURED when a named harness ran, and pending
owner play until its checklist leg runs.

Completion requires focused controls plus `python tools/bodycheck.py --selftest`,
current bodycheck on the pack, parse/module-list checks, `python tools/doccheck.py
--regen` with generated diffs reviewed, and a final green `python tools/doccheck.py`.
Commit only exact paths. When fired, delete this prompt and its prompt-map row in the
result commit; the report and bug entries are the durable record.
