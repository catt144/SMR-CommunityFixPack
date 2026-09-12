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

- [ ] 90_SaveSanitizer.lua
- [ ] Fix_AnomalyCaveInMap.lua
- [x] Fix_ArrivalDeaths.lua
- [ ] Fix_BombardmentSpread.lua
- [ ] Fix_BrokenTrackSalvage.lua
- [ ] Fix_CrystalMysteryHang.lua
- [ ] Fix_DestroyedTunnels.lua
- [x] Fix_DomeOverviewHighlight.lua
- [ ] Fix_DroneTransportMinors.lua
- [ ] Fix_DustSicknessBiorobots.lua
- [x] Fix_ExoticDepositSign.lua
- [ ] Fix_ExtenderFlapChurn.lua
- [x] Fix_FounderTraitNotification.lua
- [x] Fix_FreedHousingNotice.lua
- [x] Fix_GeneForging.lua
- [ ] Fix_GhostFarmOxygen.lua
- [x] Fix_GraphConsumedCaption.lua
- [ ] Fix_JumboCaveReinforcementWedge.lua
- [ ] Fix_LakeEntombment.lua
- [ ] Fix_LanderEmptyLaunch.lua
- [ ] Fix_LandscapeUnitFilter.lua
- [x] Fix_LayoutTechLock.lua
- [x] Fix_MirrorSphereSite.lua
- [x] Fix_NightShiftWork.lua
- [ ] Fix_PayloadTemplateRefill.lua
- [ ] Fix_RocketDroneChurn.lua
- [x] Fix_RocketInteractGuard.lua
- [x] Fix_SaintBlessing.lua
- [ ] Fix_ScanDowngrade.lua
- [x] Fix_SequenceLatents.lua
- [x] Fix_ShelterReflex.lua
- [x] Fix_ShuttleHubOffAvailable.lua
- [x] Fix_ShuttleTransportCache.lua
- [ ] Fix_SilentHitMomentFX.lua
- [ ] Fix_SinkholeIndestructible.lua
- [x] Fix_StaleReservations.lua
- [ ] Fix_TrackConnectorPingPong.lua
- [ ] Fix_TrackSalvageRefund.lua
- [ ] Fix_TrackSalvageWipe.lua
- [ ] Fix_TrackTunnelPowerBridge.lua
- [ ] Fix_TradeRocketFuelRefresh.lua
- [ ] Fix_TrainCargoDumping.lua
- [ ] Fix_TrainsToVoid.lua
- [ ] Fix_TrainWaitTime.lua
- [x] Fix_VacuumWalks.lua
- [ ] Fix_WispRewards.lua
