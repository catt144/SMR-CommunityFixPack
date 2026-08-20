-- The pack's Mod Editor item list.
--
-- ⛔ THIS PACK HAS NO MOD OPTIONS (2026-08-12, the opt-in split). Every
-- ModItemOptionToggle and ModItemOptionChoice, and the eight Opt_ modules they
-- steered, moved to the standalone Community Opt-In Pack
-- (C:\Dev\SMR-OptInPack). metadata.lua consequently has no `default_options`
-- field, so the pack no longer lists in Options → Mod Options at all — that is
-- the intended post-split shape, and the TestKit's OptionsMenuFixPack probe
-- asserts it. The rules that governed those entries (toggle name == Register
-- id == default_options key; the D09 dial exception) moved with them, into the
-- new mod's items.lua and its FIX_POLICY §5.
--
-- Individual fixes remain vetoable on PC without any of that:
-- `SMRFixPack_Disabled["<FixId>"] = true` before the pack loads.
--
-- ModItemCode entries (audit 2026-07-29, A3): the Mod Editor's SaveDef
-- regenerates metadata.lua's `code` list SOLELY from these items
-- (Mod.lua:960-974 via UpdateCode :816-840) — without them an editor
-- round-trip (and the editor upload flow, which saves-if-dirty) would write
-- `code = false` and publish a mod that loads NO code at all. ORDER IS
-- LOAD-BEARING: the entries below must stay in exactly metadata.lua's
-- current `code` order (00_Core first, then the Fix_ files, then
-- 90_SaveSanitizer last), or a round-trip reorders the load sequence.
return {
	PlaceObj('ModItemCode', {
		'name', "00_Core",
		'CodeFileName', "Code/00_Core.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_CaveInsNoDisasters",
		'CodeFileName', "Code/Fix_CaveInsNoDisasters.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_MeteorFrequency",
		'CodeFileName', "Code/Fix_MeteorFrequency.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_UpgradeModifierLeak",
		'CodeFileName', "Code/Fix_UpgradeModifierLeak.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_NightShiftWork",
		'CodeFileName', "Code/Fix_NightShiftWork.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_MilestoneCrash",
		'CodeFileName', "Code/Fix_MilestoneCrash.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_WispRewards",
		'CodeFileName', "Code/Fix_WispRewards.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TouristApplicants",
		'CodeFileName', "Code/Fix_TouristApplicants.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrainsToVoid",
		'CodeFileName', "Code/Fix_TrainsToVoid.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LanderEmptyLaunch",
		'CodeFileName', "Code/Fix_LanderEmptyLaunch.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LanderCargoRatchet",
		'CodeFileName', "Code/Fix_LanderCargoRatchet.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LanderReturnFuel",
		'CodeFileName', "Code/Fix_LanderReturnFuel.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ShelterReflex",
		'CodeFileName', "Code/Fix_ShelterReflex.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_BrokenTrackSalvage",
		'CodeFileName', "Code/Fix_BrokenTrackSalvage.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrackSalvageWipe",
		'CodeFileName', "Code/Fix_TrackSalvageWipe.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LakeEntombment",
		'CodeFileName', "Code/Fix_LakeEntombment.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_GhostFarmOxygen",
		'CodeFileName', "Code/Fix_GhostFarmOxygen.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_RocketDroneChurn",
		'CodeFileName', "Code/Fix_RocketDroneChurn.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ShuttleTransportCache",
		'CodeFileName', "Code/Fix_ShuttleTransportCache.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_VacuumWalks",
		'CodeFileName', "Code/Fix_VacuumWalks.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ArrivalDeaths",
		'CodeFileName', "Code/Fix_ArrivalDeaths.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DroneUnreachableForever",
		'CodeFileName', "Code/Fix_DroneUnreachableForever.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_StaleReservations",
		'CodeFileName', "Code/Fix_StaleReservations.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_CrystalMysteryHang",
		'CodeFileName', "Code/Fix_CrystalMysteryHang.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TouristSatisfaction",
		'CodeFileName', "Code/Fix_TouristSatisfaction.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrainPlatformWedge",
		'CodeFileName', "Code/Fix_TrainPlatformWedge.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LowStorageWarning",
		'CodeFileName', "Code/Fix_LowStorageWarning.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_CommandCenterNumbers",
		'CodeFileName', "Code/Fix_CommandCenterNumbers.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DomeOverviewHighlight",
		'CodeFileName', "Code/Fix_DomeOverviewHighlight.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrainCargoDumping",
		'CodeFileName', "Code/Fix_TrainCargoDumping.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_UniversityOvertraining",
		'CodeFileName', "Code/Fix_UniversityOvertraining.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DestroyedTunnels",
		'CodeFileName', "Code/Fix_DestroyedTunnels.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustSicknessBiorobots",
		'CodeFileName', "Code/Fix_DustSicknessBiorobots.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustSicknessDamage",
		'CodeFileName', "Code/Fix_DustSicknessDamage.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_GeneForging",
		'CodeFileName', "Code/Fix_GeneForging.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_MirrorSphereSite",
		'CodeFileName', "Code/Fix_MirrorSphereSite.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_PayloadTemplateRefill",
		'CodeFileName', "Code/Fix_PayloadTemplateRefill.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_AsteroidLanderAvailable",
		'CodeFileName', "Code/Fix_AsteroidLanderAvailable.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ShuttleHubOffAvailable",
		'CodeFileName', "Code/Fix_ShuttleHubOffAvailable.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_FreedHousingNotice",
		'CodeFileName', "Code/Fix_FreedHousingNotice.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DomeFreeSpaceMismatch",
		'CodeFileName', "Code/Fix_DomeFreeSpaceMismatch.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SmallLandscapeSites",
		'CodeFileName', "Code/Fix_SmallLandscapeSites.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LandscapeUnitFilter",
		'CodeFileName', "Code/Fix_LandscapeUnitFilter.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_RocketInteractGuard",
		'CodeFileName', "Code/Fix_RocketInteractGuard.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrackConnectorPingPong",
		'CodeFileName', "Code/Fix_TrackConnectorPingPong.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrackTunnelPowerBridge",
		'CodeFileName', "Code/Fix_TrackTunnelPowerBridge.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_GridGlobalStorage",
		'CodeFileName', "Code/Fix_GridGlobalStorage.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LastTransmissionStorage",
		'CodeFileName', "Code/Fix_LastTransmissionStorage.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_GraphConsumedCaption",
		'CodeFileName', "Code/Fix_GraphConsumedCaption.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_MoraleComfortTooltip",
		'CodeFileName', "Code/Fix_MoraleComfortTooltip.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrainWaitTime",
		'CodeFileName', "Code/Fix_TrainWaitTime.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_FounderTraitNotification",
		'CodeFileName', "Code/Fix_FounderTraitNotification.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_StorageRateModifiers",
		'CodeFileName', "Code/Fix_StorageRateModifiers.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SequenceLatents",
		'CodeFileName', "Code/Fix_SequenceLatents.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_IndependenceTerraforming",
		'CodeFileName', "Code/Fix_IndependenceTerraforming.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrackSalvageRefund",
		'CodeFileName', "Code/Fix_TrackSalvageRefund.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_LayoutTechLock",
		'CodeFileName', "Code/Fix_LayoutTechLock.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TrainMinors",
		'CodeFileName', "Code/Fix_TrainMinors.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DroneTransportMinors",
		'CodeFileName', "Code/Fix_DroneTransportMinors.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_AnomalyCaveInMap",
		'CodeFileName', "Code/Fix_AnomalyCaveInMap.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_TechDescriptionBuilding",
		'CodeFileName', "Code/Fix_TechDescriptionBuilding.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_BombardmentSpread",
		'CodeFileName', "Code/Fix_BombardmentSpread.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ExtenderFlapChurn",
		'CodeFileName', "Code/Fix_ExtenderFlapChurn.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DisasterPredictionLeak",
		'CodeFileName', "Code/Fix_DisasterPredictionLeak.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_MeteorStormWedge",
		'CodeFileName', "Code/Fix_MeteorStormWedge.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_RainsDeadlock",
		'CodeFileName', "Code/Fix_RainsDeadlock.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_FirstAsteroidPrefabs",
		'CodeFileName', "Code/Fix_FirstAsteroidPrefabs.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SaintBlessing",
		'CodeFileName', "Code/Fix_SaintBlessing.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustDevilsDescrMap",
		'CodeFileName', "Code/Fix_DustDevilsDescrMap.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_AstrogeologistExtractors",
		'CodeFileName', "Code/Fix_AstrogeologistExtractors.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SinkholeIndestructible",
		'CodeFileName', "Code/Fix_SinkholeIndestructible.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustStormUndergroundBreaks",
		'CodeFileName', "Code/Fix_DustStormUndergroundBreaks.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustDevilSpawnGate",
		'CodeFileName', "Code/Fix_DustDevilSpawnGate.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ExoticDepositSign",
		'CodeFileName', "Code/Fix_ExoticDepositSign.lua",
	}),
	-- ⛔ ADDED 2026-08-19 (pre-launch sweep, link 6 — LAUNCH-BLOCKING). The
	-- module shipped in `metadata.lua`'s `code` list on 2026-08-15 and its
	-- ModItemCode was never written, so this file held 75 entries against 76
	-- code lines. That is the exact failure the header above describes:
	-- `SaveDef` rebuilds `code` SOLELY from these items (`ModDef:UpdateCode`,
	-- Mod.lua:816-840 — `local code = false`, then one entry per item, no disk
	-- scan; `SaveDef` calls it at :973), and BOTH portals force a
	-- `SaveWholeMod` on a first upload — Steam's runs in step 1 of `UploadMod`,
	-- BEFORE `CreatePackageForUpload` (`Steam_PrepareForUpload`,
	-- SteamWorkshop.lua:17-22; GedModEditor.lua:786-793). Steam would therefore
	-- have shipped a `code` list with this file missing, and the automation-law
	-- compensation fix would never have loaded for a single player.
	PlaceObj('ModItemCode', {
		'name', "Fix_AutomationLawCompensation",
		'CodeFileName', "Code/Fix_AutomationLawCompensation.lua",
	}),
	-- Added 2026-08-20 (close-out chain, link 1 — C51). Written by hand, in the
	-- same position it takes in `metadata.lua`'s `code` list, per the header
	-- above and H-10: a module absent from this file SHIPS ABSENT.
	PlaceObj('ModItemCode', {
		'name', "Fix_LocalizedUIText",
		'CodeFileName', "Code/Fix_LocalizedUIText.lua",
	}),
	-- Added 2026-08-20 (close-out chain, link 2 — C50), same rule as above.
	PlaceObj('ModItemCode', {
		'name', "Fix_SpaceYDroneCapBullet",
		'CodeFileName', "Code/Fix_SpaceYDroneCapBullet.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "90_SaveSanitizer",
		'CodeFileName', "Code/90_SaveSanitizer.lua",
	}),
}
