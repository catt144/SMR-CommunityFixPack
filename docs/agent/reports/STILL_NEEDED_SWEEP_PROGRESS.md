# Still-needed sweep — live progress

Coordinator: `/root` (Codex). Started 2026-09-12 against fix-pack HEAD `2983fac`.
Task: `docs/agent/prompts/STILL_NEEDED_SWEEP.md`, explicitly authorising fan-out.
Game pin: 1.1.0.403908, Steam build 24995074. No release changes in this sweep.

- [x] Capture settled retail boot evidence; stale-probe sweep CLEAN
  (zero `TEMPORARY` hits in pack and TestKit `Code/`, 2026-09-12).
- [ ] **IN PROGRESS:** Review the 46 registered modules, one module per agent task; preserve every report verbatim.
- [ ] Compare all store-card bullets with the complete fix list, including aggregate claims.
- [ ] Trace disagreements against primary game artefacts; name all unchecked cases.
- [ ] Collate recommendations, mirror owner decisions into checklist 156, and route surface work after v9.
- [ ] Validate docs, commit explicit session paths, and push reports.

Shared-tree fence: agents write only their assigned report files under
`docs/agent/reports/still-needed/`. They do not change loadable code, entries,
indexes, registration files, cards, release files, or git state. The coordinator
alone owns synthesis and commits. Owner clarified only this team is in the tree;
the existing handoff edit is nevertheless excluded from this work.

## Module reports

- [x] 90_SaveSanitizer.lua
- [x] Fix_AnomalyCaveInMap.lua
- [x] Fix_ArrivalDeaths.lua
- [x] Fix_BombardmentSpread.lua
- [x] Fix_BrokenTrackSalvage.lua
- [x] Fix_CrystalMysteryHang.lua
- [x] Fix_DestroyedTunnels.lua
- [x] Fix_DomeOverviewHighlight.lua
- [x] Fix_DroneTransportMinors.lua
- [x] Fix_DustSicknessBiorobots.lua
- [x] Fix_ExoticDepositSign.lua
- [x] Fix_ExtenderFlapChurn.lua
- [x] Fix_FounderTraitNotification.lua
- [x] Fix_FreedHousingNotice.lua
- [x] Fix_GeneForging.lua
- [x] Fix_GhostFarmOxygen.lua
- [x] Fix_GraphConsumedCaption.lua
- [x] Fix_JumboCaveReinforcementWedge.lua
- [x] Fix_LakeEntombment.lua
- [x] Fix_LanderEmptyLaunch.lua
- [x] Fix_LandscapeUnitFilter.lua
- [x] Fix_LayoutTechLock.lua
- [x] Fix_MirrorSphereSite.lua
- [x] Fix_NightShiftWork.lua
- [x] Fix_PayloadTemplateRefill.lua
- [x] Fix_RocketDroneChurn.lua
- [x] Fix_RocketInteractGuard.lua
- [x] Fix_SaintBlessing.lua
- [x] Fix_ScanDowngrade.lua
- [x] Fix_SequenceLatents.lua
- [x] Fix_ShelterReflex.lua
- [x] Fix_ShuttleHubOffAvailable.lua
- [x] Fix_ShuttleTransportCache.lua
- [x] Fix_SilentHitMomentFX.lua
- [x] Fix_SinkholeIndestructible.lua
- [x] Fix_StaleReservations.lua
- [x] Fix_TrackConnectorPingPong.lua
- [x] Fix_TrackSalvageRefund.lua
- [x] Fix_TrackSalvageWipe.lua
- [ ] Fix_TrackTunnelPowerBridge.lua
- [x] Fix_TradeRocketFuelRefresh.lua
- [ ] Fix_TrainCargoDumping.lua
- [x] Fix_TrainsToVoid.lua
- [x] Fix_TrainWaitTime.lua
- [x] Fix_VacuumWalks.lua
- [x] Fix_WispRewards.lua
