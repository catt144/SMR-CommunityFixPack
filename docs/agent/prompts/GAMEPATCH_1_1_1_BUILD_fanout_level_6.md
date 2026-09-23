# Game 1.1.1 — the whole pack response: three repairs and fifteen retirements

One-off build brief, and the single home for the 1.1.1 code response. It replaces the
separate FIX and REMOVE briefs, which are consumed with it: doing both under one
coordinator reconciles `items.lua`, `metadata.lua`, the module lists, the TestKit probe
inventory and the generated counts **once**, against the final state, instead of twice
against two intermediate ones.

The dispositions are settled and are not reopened here. The source audit is
`docs/agent/reports/GAMEPATCH_1.1.1.405907_2026-09-23.md`; the adjudication that
corrected it is `docs/agent/reports/GAMEPATCH_1.1.1_ADJUDICATION_2026-09-23.md`; the
severity ranking is `docs/agent/reports/FULL_BODY_PRIORITY_2026-09-23.md`. Re-derived
totals: 33 KEEP / 3 FIX / 16 REMOVE.

This brief was authored from `234a121`. Start with `git log --oneline -6`, `git pull`,
and `git status --short`; if HEAD has moved, compare the named paths across
`234a121..HEAD` and re-read only moved evidence. Every line number below is a lead and
must be re-derived with `rg -n` before use. Invoke `doc-editing` before record edits and
`smr-bug-library` for status or evidence changes. Apply `CLAUDE.md`,
`docs/agent/WORKFLOW.md` and `docs/agent/FIX_POLICY.md`.

## Authority and outcome

The owner settled the shape on 2026-09-23: one coordinator builds the whole response,
the track unit goes to a tier-3 subagent, and a Claude seat audits the result
afterwards. This brief authorizes the three repairs, the sixteen retirements and the
three manifest hygiene items below. It does not authorize a release, a store or version
change, edits to shipped game files, or launching the game.

End state: a pack with no retired module loaded, registered, probed or named as
shipped; three rebased modules that preserve their still-needed behaviour without
overwriting the vendor's 1.1.1 work; every generated count reconciled once; and a build
report that separates what was measured from what is still owed to play.

## Delegation

You are the coordinator. You hold the plan, every shared-file edit, all gates and all
commits; the units below hold the reading and the module bodies.

- **The track unit goes to a tier-3 subagent** (owner's instruction). It is the only
  tier-3 spend here, justified because a near-miss fails silently and permanently inside
  the player's save, so a result that has to be redone costs more than the tier.
- **Everything else is yours to tier**, tier 2 or tier 1 per unit, on the rule of the
  lowest tier that can do the task. The sixteen retirements are well-specified tracing
  and deletion; the other two rebases are design-sensitive and should not be treated as
  bulk work.
- **Set model and effort explicitly on every spawn.** An unset subagent inherits this
  session's effort, which can exceed its cap.
- **Parallel subagents get disjoint files, one writer per file.** The retirement units
  delete their own `Code/Fix_*.lua` and **report** every shared-file reference they
  find; you apply those to `items.lua`, `metadata.lua`, the module lists and the TestKit
  inventory yourself, once, in step 6. No subagent writes a shared file.
- **No subagent runs a writing git command, the hooks, or doccheck.** You regenerate,
  gate and commit. Ask each unit for what its commands printed and for what it did not do.
- **Give each unit spans, not whole files.** The working sets differ by two orders of
  magnitude and naive reads are the only real context risk here. The track unit's entire
  set — both `TrackElement.lua` versions, all three modules, the entry — is about 138 KB.
  F125's looks like 430 KB only because `Colonist.lua` is 6,031 lines on 1.1.1 and 5,689
  on 1.1.0; its actual targets are `Colonist:TryToEmigrateToDome` (:1894 on 1.1.1, :1886
  on 1.1.0) and `Colonist:MigrateStep` (:2155, which does not exist on 1.1.0), plus 15
  call sites tree-wide. Re-derive those spans, then hand the span. A unit that reads
  `Colonist.lua` whole has made the job harder, not safer.
- Clear each result with one check aimed at what it rests on, rather than redoing it. A
  subagent's account of machinery outside its own task — why a gate went red, what an
  exit code meant — is the weak part; diagnose that yourself.
- Re-verification of a unit goes to a subagent that did not build it. That is internal
  to this job and does not replace the owner's separate audit seat (below).

## Order of work

Severity order, from the Phase A ranking. The track unit is both the highest-severity
row and the longest pole, so it starts first and runs while the retirements fan out
alongside it.

### 1 · The track unit — tier 3, one agent, one body

Do not split this across agents: the rebase, the retirement and the wrapper re-read all
act on the same declaration, and splitting them is how a plausible wrong answer gets
made.

- **Rebase `Fix_TrackSalvageWipe` (F124).** Start from the complete 1.1.1
  `TrackGridElement:DemolishAndSplitTrack` behaviour, retain **all** vendor repair-site
  semantics — repair-site exclusion, correct-array removal, repair-site rehome and
  `repair_cgs` rebuild, repair-aware `ProcessAllElements` (`TrackElement.lua`
  :484-488, :519-525, :598-614, :628-632) — then reapply only the marked F44/F91/F116
  changes. Prefer a smaller composable shape if it genuinely preserves behaviour; do not
  force a full replacement merely to minimise the diff.
  *Falsifying read:* compare the complete installed replacement with the current
  archived body. If all four semantics already survive, F124 is wrong.
  *Exercise:* curved and short salvage, a live repair site spanning a split,
  `repair_cgs`, survivor arrays, refunds, shells, `skip_track_process`.
- **Retire `Fix_BrokenTrackSalvage` in the same change**, with its registrations and
  probes. Preserve F45's evidence in its entry. Its REMOVE premise holds only once this
  rebase runs — the vanilla split body it names does not execute in a shipping pack
  before then — and its `:35` pin on the same body would otherwise read BODY-CHANGED for
  as long as the file existed (`FULL_BODY_PRIORITY_2026-09-23.md` §3).
- **Re-read `Fix_TrackSalvageRefund`'s `Demolish` wrapper** (`:195-250`) against the
  rebased split body. Phase A leaves one question explicitly open and owed to this unit:
  whether that module's snapshot survives the 1.1.1 array rules. Answer it here.

### 2 · F125 — rebase `Fix_VacuumWalks`

Preserve the complete 1.1.1 direct **and** multi-leg migration state machine in
`Colonist:TryToEmigrateToDome`; the old-body replacement erases it. Repair only proven
vacuum passage thresholds, including the second site at `Colonist:MigrateStep` (:2199),
which is a second copy of F52 that no module currently reaches. F52 itself remains.
*Falsifying read:* trace both passage decisions and every caller. If the second site is
unreachable in vacuum, record that and do not patch it speculatively.
*Cover:* a direct final leg, an intermediate leg, breathable controls, reservations,
shuttle and train continuation, cancellation, no-passage fallback.

### 3 · F121 — `Fix_CloggedBuildingRelease`

Preserve a narrow, synchronous, idempotent **load-only** repair for the exact old saved
reason and state, working even when vanilla's new one-hour Duration is present. Remove
the daily and live repair. Do not add a timer, field, UI or new-event path. Prove
healthy 1.1.1 events remain vanilla-owned and that the exact legacy fixture heals.
The adjudication already ran the whole-tree search for reason `789863173059`
(2026-09-23): one hit, `Data/StoryBit/BuildingClogged.lua:8`, no fixup, and the Duration
thread is created only at firing (`ClassDef-Effects.generated.lua:2772-2790`) — so the
retained load half stands. The retail on-leg shows the module inactive on 1.1.1, which
is the stand-down F121 describes.

### 4 · The sixteen retirements

Delete each module and its exact references. **A disappearance or rename is not proof:**
trace the replacement body *and* its consumer on the archived 1.1.1.405907 tree before
deleting. Preserve bug history, reports and archived evidence — update them rather than
erasing why the module existed.

| module | native replacement / condition |
|---|---|
| `Fix_FounderTraitNotification.lua` (F126) | 1.1.1 deleted the `FounderGainsTrait` preset itself (`Data/NotificationPreset.lua`, 0 hits); `AddNotification` builds an unknown id from the base class (`CommonLua/Libs/Notifications/Notifications.lua:32-48`). Feature removed by the vendor; nothing to preserve, no saved state. |
| `Fix_BuildingCodesPrefab.lua` | Both law handlers dropped `from_prefab` and the early return, `LawDef-Efficiency.lua:700-710,902-912`. |
| `Fix_DestroyedTunnels.lua` | `TunnelBase:AddPFTunnel` now rejects either destroyed half, `Tunnel.lua:193-205`. |
| `Fix_DomeOverviewHighlight.lua` | Native body writes the computed label and protects empty domes; F122 is the active regression from retaining ours. |
| `Fix_GeneForging.lua` | Native `GetRareTraitChance` adds both technologies; F123 is the active double payment from retaining ours. |
| `Fix_GraphConsumedCaption.lua` | Native caption sums consumption plus maintenance, `ColonyControlCenter.lua:184`. |
| `Fix_MirrorSphereSite.lua` | `IsActionEnabled` rejects `progress >= max_progress`; cancellation remains available. |
| `Fix_NightShiftWork.lua` | `ShouldLeaveForWork` uses the modular day window, `Colonist.lua:2396-2403`. |
| `Fix_OpenPastureStockpiles.lua` | New `RebuildPastureStockpilePool` and `MoveOpenPasturePilesOffOrigin2` migrate old piles. Gate cleared 2026-09-23 — the retail on-leg logged the module inactive because the Outside Ranch entity variants no longer carry the nine-versus-six mismatch. |
| `Fix_SinkholeIndestructible.lua` | Sinkhole class and preset both declare `indestructible = true`; the destruction consumer is unchanged. |
| `Fix_TradeRocketFuelRefresh.lua` | Landed rockets refresh on fuel changes, and `SavegameFixups.ZZZ_UpdateRefuelRequests` covers already-landed non-player upgrade saves, `RocketCompatibility.lua:1139-1144`. |
| `Fix_TrainCargoDumping.lua` | Rewritten `Train:UnloadAll` checks resource enablement and preserves assignments, `Train.lua:787-831`. |
| `Fix_TrainsToVoid.lua` | Station demolition calls `train:DestroySilent("station", bld)` directly. |
| `Fix_TrainWaitTime.lua` | Boarding resets `transport_ticket.start_wait`, `ColonistTransport.lua:624`. |
| `Fix_WispRewards.lua` | Native removed the batch research grant and scales free-mode power by 1000, `Fireflies.lua:712-738`. |

Two gates are already settled at the desk; preserve their evidence rather than re-running
them, and return the module as FIX without blocking the rest only if a current-build read
contradicts them:

- **Open Pasture** — cleared on the retail on-leg, log
  `Mars.exe-20260923-10.39.06-6aad2d75.log:135`. The adjudication confirmed the clearance
  survives that run's single-variable limit: it is a shipped-asset probe, and neither the
  Opt-In pack nor the Train Hub dev mod touches pasture entities.
- **Trade-rocket enrolment** — `FixupSavegame` (`CommonLua/SavegameFixup.lua:24-48`,
  called from `CommonLua/Savegame.lua:809`) runs every `SavegameFixups` entry absent from
  the save's `AppliedSavegameFixups`, and that table is pre-filled only for a new game
  (`:10-16`). A fixup new in 1.1.1 therefore runs once on any older save's first load.
  The runtime check is confirmatory, not the deciding read.

**Controls.** F122, F123 and F126 are active defects, so each needs a focused
pack-on/pack-off control proving deletion restores native behaviour. F123's existing
retail evidence is pack-on only — its pack-off leg short-circuited at "fix pack not
loaded" rather than calling the vanilla function, so the two-sided control is still owed.
For the benign stand-down removals, a load and registration census plus the native
behaviour control is sufficient.

### 5 · Three manifest hygiene items

Comment-only, from the adjudication's §11. Cheap, and each closes a defect a future
reader would otherwise have to re-derive to dismiss: restamp `Fix_BombardmentSpread`
after the Phase A read; pin `DroneHubExtenderBase:UpdateUplinkRequesters` in
`Fix_ExtenderFlapChurn`; restate `Fix_DryFarmingFarms`'s DEFECT regex.

### 6 · The single reconciliation

Yours alone, against the final state, once. Reconcile `items.lua`, the metadata
ignore and load lists, source files, registrations, the TestKit probe inventory and any
shipped-feature list **by name**, not by count. Let every generated count come from its
command. This step is the reason the two briefs were merged; do not distribute it.

## Evidence standard

Each surviving module must earn a 1.1.1 behaviour decline or another FIX_POLICY-compliant
guard; an updated hash alone is not a decline. Record save footprint and removal residue
for every changed exposed site. Extend existing desk fixtures where possible, require a
positive control, and build scratch guard-reverted variants to show each decisive test
can fail — a control that cannot fail is worth nothing.

## Live work list

Put this list in the todo tool before the first write. Keep one unfinished
commit-and-verify unit in progress; add discoveries rather than hiding them.

- [ ] 1. Orient; confirm the filings and both settled gates still describe HEAD
- [ ] 2. Track unit: F124 rebase, `Fix_BrokenTrackSalvage` retired, refund wrapper answered
- [ ] 3. F125 rebase; direct and multi-leg vacuum controls green
- [ ] 4. F121 load-only migration; falsifiable desk controls green
- [ ] 5. Sixteen retirements traced and deleted; F122/F123/F126 two-sided controls green
- [ ] 6. Three manifest hygiene items
- [ ] 7. Single reconciliation of shared files and generated counts, by name
- [ ] 8. Internal re-verification of every behaviour claim by units that did not build them
- [ ] 9. Selftests, focused harnesses, doccheck regen and green; entries, report, checklist
- [ ] 10. Exact-path commits; this prompt and its map row deleted in the result commit

## Scope and stops

In scope: the three rebased modules, the sixteen retirements, the three hygiene items,
their registrations, desk and TestKit coverage, F121–F126, one build report, and
owner-only checklist legs.

Out of scope: any module not named here, unrelated cleanup, release, version and store
work, shipped game files, and launching the game. Put owner-required retail legs on the
checklist rather than running them.

Report instead of continuing only if: (1) a newer game build lands; (2) a native
replacement or a settled gate fails its stated control, so a deletion or a rebase would
be unsafe; or (3) a shared path carries peer changes that cannot be integrated without
overwriting them. A single failed unit does not authorize abandoning the others, and
does not erase progress already committed.

## Claim limits

A source read is not `tested`: say SOURCE on build 1.1.1.405907, desk-MEASURED when a
named harness ran, and pending owner play until its checklist leg runs. A matching body
hash is not compatibility. Do not claim the vendor fixed an original defect merely
because the old expression is gone, nor that a module was harmless merely because its
guard should decline. The absence of a decoded caller does not prove an engine route
impossible. Retail claims inherit the completed A/B's stated limits: it was not
single-variable, and neither leg met its zero-error acceptance condition.

## Audit

This job does not certify itself. The owner runs a separate audit seat afterwards, on a
different vendor than builds this. Write the build report so that seat can judge the
**diff and the archived source** rather than your account of them: per unit, what was
changed, what was measured with which command, and what remains owed to play. Name every
departure from this brief with its reason, and every suggestion you did not act on.

## Lifecycle

One-off. Its two predecessors — `GAMEPATCH_1_1_1_FIX_fanout_level_3.md` and
`GAMEPATCH_1_1_1_REMOVE_medium.md` — were deleted with their map rows in the commit that
authored this file, so nothing fireable duplicates it; recover their text with
`git log --diff-filter=D -- docs/agent/prompts/` if a wording question arises. In the
result commit, `git rm` this file and delete its row from
`docs/agent/prompts/README.md`. The build report, the bug entries and the three
adjudication reports are the durable record.
