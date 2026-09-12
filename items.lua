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
		'name', "Fix_NightShiftWork",
		'CodeFileName', "Code/Fix_NightShiftWork.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_WispRewards",
		'CodeFileName', "Code/Fix_WispRewards.lua",
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
		'name', "Fix_TradeRocketFuelRefresh",
		'CodeFileName', "Code/Fix_TradeRocketFuelRefresh.lua",
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
		'name', "Fix_StaleReservations",
		'CodeFileName', "Code/Fix_StaleReservations.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_CrystalMysteryHang",
		'CodeFileName', "Code/Fix_CrystalMysteryHang.lua",
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
		'name', "Fix_DestroyedTunnels",
		'CodeFileName', "Code/Fix_DestroyedTunnels.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_DustSicknessBiorobots",
		'CodeFileName', "Code/Fix_DustSicknessBiorobots.lua",
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
		'name', "Fix_ShuttleHubOffAvailable",
		'CodeFileName', "Code/Fix_ShuttleHubOffAvailable.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_FreedHousingNotice",
		'CodeFileName', "Code/Fix_FreedHousingNotice.lua",
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
		'name', "Fix_GraphConsumedCaption",
		'CodeFileName', "Code/Fix_GraphConsumedCaption.lua",
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
		'name', "Fix_SequenceLatents",
		'CodeFileName', "Code/Fix_SequenceLatents.lua",
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
		'name', "Fix_DroneTransportMinors",
		'CodeFileName', "Code/Fix_DroneTransportMinors.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_AnomalyCaveInMap",
		'CodeFileName', "Code/Fix_AnomalyCaveInMap.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_ScanDowngrade",
		'CodeFileName', "Code/Fix_ScanDowngrade.lua",
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
		'name', "Fix_SaintBlessing",
		'CodeFileName', "Code/Fix_SaintBlessing.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SinkholeIndestructible",
		'CodeFileName', "Code/Fix_SinkholeIndestructible.lua",
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
	-- Added 2026-08-20 (close-out chain, link 1 — C51). Written by hand, in the
	-- same position it takes in `metadata.lua`'s `code` list, per the header
	-- above and H-10: a module absent from this file SHIPS ABSENT.
	-- Added 2026-08-20 (close-out chain, link 2 — C50), same rule as above.
	-- Added 2026-08-24 (F105, post-release maintenance — owner ruling, checklist
	-- 72), same rule as above: hand-written, in metadata.lua's `code` position.
	-- Added 2026-08-28 (F108, post-release maintenance — owner ruling, Steam field
	-- report), same rule as above: hand-written, in metadata.lua's `code` position.
	PlaceObj('ModItemCode', {
		'name', "Fix_JumboCaveReinforcementWedge",
		'CodeFileName', "Code/Fix_JumboCaveReinforcementWedge.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Fix_SilentHitMomentFX",
		'CodeFileName', "Code/Fix_SilentHitMomentFX.lua",
	}),
	-- Added 2026-09-12 (C85, post-release maintenance — owner ruling, checklist
	-- 154: the sweep only), same rule as above: hand-written, in metadata.lua's
	-- `code` position, ahead of 90_SaveSanitizer which loads last by design.
	PlaceObj('ModItemCode', {
		'name', "Fix_CloggedBuildingRelease",
		'CodeFileName', "Code/Fix_CloggedBuildingRelease.lua",
	}),
	-- Added 2026-09-12 (C89, post-release maintenance — owner ruling, checklist
	-- 157 (c); a JUDGMENT CALL, not a defect repair), same rule as above.
	PlaceObj('ModItemCode', {
		'name', "Fix_FactionDomeSizeGate",
		'CodeFileName', "Code/Fix_FactionDomeSizeGate.lua",
	}),
	-- Added 2026-09-12 (C88, post-release maintenance — owner ruling, checklist
	-- 150 (b) option 1; a Paradox developer asked us to carry it until their patch),
	-- same rule as above.
	PlaceObj('ModItemCode', {
		'name', "Fix_BuildingCodesPrefab",
		'CodeFileName', "Code/Fix_BuildingCodesPrefab.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "90_SaveSanitizer",
		'CodeFileName', "Code/90_SaveSanitizer.lua",
	}),
}
