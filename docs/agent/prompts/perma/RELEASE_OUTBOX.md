# Release outbox — player-facing changes staged for the NEXT upload

## Must_Read_Header
<!-- RULES -->
Rule: Append a filled `### Pending` entry whenever a player-facing fix is added, retired, or materially respecified. [A3: pass]
Rule: Do not append a pending entry for a pack-internal fix that never shipped broken. [A3: pass]
Rule: Append every pending entry to `docs/archive/RELEASE_HISTORY.md` and empty `Pending` only through `release_prompt.md` after upload. [A3: pass]
Rule: Do not delete a pending entry except through a release or with an explicit withdrawal reason. [A3: pass]
<!-- /RULES -->

This ledger tracks every player-facing tree change since the last upload.
`docs/agent/prompts/perma/release_prompt.md` derives `last_changes`, fix-list
rows and the store-card count from it, then appends Pending entries to
`docs/archive/RELEASE_HISTORY.md` after upload. `docs/agent/support/RELEASE_SURFACES.md` defines which changes
have a player surface.

**Live tree version:** `metadata.lua` `version` — read it, never hand-set (editor/version rail (`docs/agent/prompts/perma/release_prompt.md` § Release rails)).
**Live count word:** whatever `metadata.lua`'s `description` currently says
(`grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs' metadata.lua` — one hit; zero is a FAIL). Each pending fix that has a
player surface bumps it by one on release.

## Pending — goes out with the next upload

### Pending — game 1.1.1 response (2026-09-23)

- Track salvage retains the vendor's repair-site ownership and indexing changes
  while preserving curved/short-track salvage, refunds and whole-track cleanup.
- Vacuum migration retains the vendor's direct and multi-leg routing; both
  passage decisions are repaired. Legacy clogged-building recovery becomes
  load-only and accepts only saves written before 1.1.1. Already-resaved ambiguous
  state remains untouched so a healthy native timer is not cut short.
- Retire `BrokenTrackSalvage`, `BuildingCodesPrefab`, `DestroyedTunnels`,
  `DomeOverviewHighlight`, `FounderTraitNotification`, `GeneForging`,
  `GraphConsumedCaption`, `MirrorSphereSite`, `NightShiftWork`,
  `OpenPastureStockpiles`, `SinkholeIndestructible`, `TradeRocketFuelRefresh`,
  `TrainCargoDumping`, `TrainWaitTime`, `TrainsToVoid` and `WispRewards`.
- Evidence and limits: [build report](../../reports/GAMEPATCH_1.1.1_BUILD_2026-09-23.md).
  Desk/source results do not replace the separate owner audit or retail legs.
- Release surfaces are pending the release job: reconcile the site fix list,
  store-card copies, description/count word and change notes from the retired
  names and surviving modules. This build does not change a version or publish.

## Last released

**v14** (2026-09-19). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
