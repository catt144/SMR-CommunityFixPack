# Game 1.1.1 — retire the fifteen replaced modules

One-off removal brief. The 1.1.1 full sweep settled these modules as REMOVE because the
vendor supplied a correct replacement or migration. The outcome is a smaller pack with
no retired module loaded, registered, tested as live, or named as shipped.

This brief was authored from fix-pack base `2812098` and the game-patch artifact commit
that added this file. Start with `git log --oneline -6`, `git pull`, and
`git status --short`; compare the named paths and report from `2812098..HEAD` and
recheck shared paths before every write. Invoke `doc-editing` before record edits and
`smr-bug-library` for status/evidence changes; follow `docs/agent/WORKFLOW.md` and
`docs/agent/FIX_POLICY.md`. If unattended, use different owner-selected models for
execution and audit.

## Authority and removal set

Remove exactly these modules after confirming their named 1.1.1 replacement in the
archived tree. Line numbers are leads and must be re-derived.

| module | native replacement / removal condition |
|---|---|
| `Fix_FounderTraitNotification.lua` | Added 2026-09-23 by the adjudication (F126): 1.1.1 deleted the dead handler and the `FounderGainsTrait` preset itself (`Data/NotificationPreset.lua`, 0 hits); `AddNotification` builds an unknown id from the base class (`CommonLua/Libs/Notifications/Notifications.lua:32-48`). The vendor removed the feature; there is nothing to preserve and no saved state. |
| `Fix_BuildingCodesPrefab.lua` | Both law handlers dropped `from_prefab` and the early return at `LawDef-Efficiency.lua:700-710,902-912`. |
| `Fix_DestroyedTunnels.lua` | `TunnelBase:AddPFTunnel` now rejects either destroyed half at `Tunnel.lua:193-205`. |
| `Fix_DomeOverviewHighlight.lua` | Native body writes the computed label and protects empty domes; F122 records the active regression caused by retaining ours. |
| `Fix_GeneForging.lua` | Native `GetRareTraitChance` adds both technologies; F123 records the active double payment caused by retaining ours. |
| `Fix_GraphConsumedCaption.lua` | Native caption now sums consumption plus maintenance at `ColonyControlCenter.lua:184`. |
| `Fix_MirrorSphereSite.lua` | `IsActionEnabled` rejects `progress >= max_progress` while cancellation remains available. |
| `Fix_NightShiftWork.lua` | `ShouldLeaveForWork` uses the modular day window at `Colonist.lua:2396-2403`. |
| `Fix_OpenPastureStockpiles.lua` | New `RebuildPastureStockpilePool` and `MoveOpenPasturePilesOffOrigin2` migrate old piles. Gate cleared 2026-09-23: the retail on-leg logged this module inactive because the Outside Ranch entity variants no longer have the nine-versus-six mismatch. |
| `Fix_SinkholeIndestructible.lua` | Both Sinkhole class and preset now declare `indestructible = true`; the destruction consumer is unchanged. |
| `Fix_TradeRocketFuelRefresh.lua` | Landed rockets now refresh on fuel changes, and newly added `SavegameFixups.ZZZ_UpdateRefuelRequests` covers already-landed non-player upgrade saves at `RocketCompatibility.lua:1139-1144`. |
| `Fix_TrainCargoDumping.lua` | Rewritten `Train:UnloadAll` checks resource enablement and preserves assignments at `Train.lua:787-831`. |
| `Fix_TrainsToVoid.lua` | Station demolition now calls `train:DestroySilent("station", bld)` directly. |
| `Fix_TrainWaitTime.lua` | Boarding explicitly resets `transport_ticket.start_wait` at `ColonistTransport.lua:624`. |
| `Fix_WispRewards.lua` | Native removed the batch research grant and scales free-mode power by 1000 at `Fireflies.lua:712-738`. |

Adjudicated 2026-09-23: `Fix_BrokenTrackSalvage` left this set. It is retired inside the
FIX brief's F124 unit, because the vanilla split body its premise named does not run in a
shipping pack until `Fix_TrackSalvageWipe` is rebased, and its `:35` pin would otherwise
read BODY-CHANGED for as long as the file existed
(`docs/agent/reports/FULL_BODY_PRIORITY_2026-09-23.md` §3). The set is still fifteen.

Durable evidence and limits are in
`docs/agent/reports/GAMEPATCH_1.1.1.405907_2026-09-23.md`. Patchcheck/bodycheck rows
are routing only. A disappearance or rename is not proof: trace the replacement body
and consumer before deleting.

## Required result

- Delete each cleared `Code/Fix_*.lua` file and its exact `items.lua`, `metadata.lua`,
  module-list, desk-harness, TestKit, documentation, and release-surface references.
  Preserve bug history, reports, and archived evidence; update them rather than erasing
  why the module existed.
- Let generated counts come from their commands. Reconcile `items.lua`, metadata
  ignore/load lists, source files, registrations, TestKit probe inventory, and any
  shipped-feature list by name.
- Preserve the completed Open Pasture gate evidence when removing it: retail log
  `Mars.exe-20260923-10.39.06-6aad2d75.log:135` records the module declining because
  the entity mismatch is gone. Recheck the archived native migration before deletion;
  a contrary current-build reading returns this module as FIX without blocking the rest.
- Verify the new rocket save fixup is newly enrolled for an upgrading 1.1.0 save, not
  merely present as a never-run function. If that cannot be established, retain only a
  narrow load migration and return this module as FIX; do not keep the duplicate
  modifier wrapper. Adjudicated 2026-09-23 at the desk: `FixupSavegame`
  (`CommonLua/SavegameFixup.lua:24-48`, called from `CommonLua/Savegame.lua:809`) runs
  every `SavegameFixups` entry absent from the save's `AppliedSavegameFixups`, and that
  table is pre-filled only for a new game (`:10-16`), so a fixup new in 1.1.1 runs once on
  any older save's first load. The runtime check is confirmatory, not the deciding read.
- For F122 and F123, add focused pack-on/pack-off controls that prove deletion restores
  native behavior. For benign stand-down removals, a load/registration census plus the
  native behavior control is sufficient.

## Live work list

Put this list in the todo tool before the first write and keep one unfinished
commit-and-verify unit in progress.

- [ ] 1. Orient; revalidate all fifteen native replacements and two migration gates
- [ ] 2. Remove active conflicts F122/F123; run their focused controls
- [ ] 3. Remove native-body replacements and reconcile all registrations/lists
- [ ] 4. Preserve the cleared Open Pasture evidence; resolve the trade-rocket migration gate
- [ ] 5. Remove or retire corresponding desk/TestKit probes without losing controls
- [ ] 6. Update entries/report/checklist and measure all affected generated counts
- [ ] 7. Independent audit, parse/body/patch checks, doccheck, and owner boot recipe
- [ ] 8. Commit exact paths; delete this prompt and its prompt-map row in the result

## Scope, stops, and claim limits

In scope: the fifteen named modules and their exact registrations, tests, pack surfaces,
bug/report updates, and owner-only validation recipe. Out of scope: the three FIX
modules, unrelated cleanup, release/version/store work, shipped game files, and a game
launch.

Report instead of continuing only if: (1) a newer game build lands; (2) a native
replacement fails its stated control and would make deletion unsafe; or (3) shared-path
peer work cannot be integrated without overwrite. A per-module failed gate does not
authorize deleting that module and does not erase progress on the others.

Do not claim the vendor fixed an original defect merely because the old expression is
gone, or that a module was harmless merely because its guard should decline. Supported
claims name the replacement and consumer on archived 1.1.1.405907, then distinguish
desk measurement from the bounded results of the owner's completed retail run.

Completion requires focused controls, parse and module-list agreement,
`python tools/bodycheck.py --selftest`, current bodycheck, patchcheck selftest,
`python tools/doccheck.py --regen` with generated diffs reviewed, and final green
doccheck. Commit only exact paths. When fired, delete this prompt and its map row; the
report and bug entries remain.
