-- Mod Options — the in-game enable surface for the optional modules
-- (Options → Mod Options → Community Fix Pack), added 2026-07-27 (D05).
--
-- Why this file exists: the old "set SMRFixPack_Optional from the console
-- before the mod loads" instruction was unusable — module gates run at mod
-- code load, DURING game startup, before any console exists (and the console
-- platforms Paradox Mods targets have no console at all). The engine's native
-- mod options are the supported path: values persist per account
-- (AccountStorage.ModOptions), are loaded BEFORE mod code so the gates can
-- read them (CommonLua/Classes/Mod.lua:2128-2131, exposed as
-- CurrentModOptions), and the page works with a gamepad on PS/Xbox.
--
-- RULES:
--   * Each toggle's `name` MUST equal the module's SMRFixPack.Register id —
--     00_Core.lua's OptionEnabled/reconcile read them by that id.
--   * Every toggle here must also appear (as false) in metadata.lua
--     `default_options` — that field is what makes the Options screen list
--     the pack at all (ModDef:HasOptions, Mod.lua:473-475).
--   * EXCEPTION — the two ModItemOptionChoice dials (DroneSpeedDial /
--     DroneCarryDial) belong to the NON-toggle module DroneStatDials (D09):
--     their names are NOT Register ids, 00_Core's boolean reconciler does
--     not manage them, and the module reads CurrentModOptions directly and
--     reconciles itself (FIX_POLICY §5 dial addendum). Their
--     `default_options` entries are the base STRINGS (must stay
--     byte-identical to the ChoiceList/module maps), not false.
--   * Toggling takes effect immediately (00_Core's OnMsg.ApplyModOptions
--     reconciliation activates/deactivates the module live); the tooltips
--     stay behavior-only.
--
-- ModItemCode entries (audit 2026-07-29, A3): the Mod Editor's SaveDef
-- regenerates metadata.lua's `code` list SOLELY from these items
-- (Mod.lua:960-974 via UpdateCode :816-840) — without them an editor
-- round-trip (and the editor upload flow, which saves-if-dirty) would write
-- `code = false` and publish a mod that loads NO code at all. ORDER IS
-- LOAD-BEARING: the entries below must stay in exactly metadata.lua's
-- current `code` order (00_Core first, 90_SaveSanitizer after the last
-- Fix_, then the six Opt_ in their current order), or a round-trip
-- reorders the load sequence.
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
		'name', "90_SaveSanitizer",
		'CodeFileName', "Code/90_SaveSanitizer.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_ClassicRockets",
		'CodeFileName', "Code/Opt_ClassicRockets.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_AcknowledgedWarnings",
		'CodeFileName', "Code/Opt_AcknowledgedWarnings.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_ResidencyControl",
		'CodeFileName', "Code/Opt_ResidencyControl.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_MultipleSuns",
		'CodeFileName', "Code/Opt_MultipleSuns.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_DroneOverhaul",
		'CodeFileName', "Code/Opt_DroneOverhaul.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_CohortHousing",
		'CodeFileName', "Code/Opt_CohortHousing.lua",
	}),
	PlaceObj('ModItemCode', {
		'name', "Opt_DroneStatDials",
		'CodeFileName', "Code/Opt_DroneStatDials.lua",
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "ClassicRockets",
		'DisplayName', "Classic rockets — refuel while parked",
		'Help', "A player-controlled rocket parked at your colony keeps its launch fuel requested even with no destination selected, so drones keep it fueled while it waits — the original game's behavior.",
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "AcknowledgedWarnings",
		'DisplayName', "Acknowledged warnings",
		'Help', 'Dismissing a "Building Not Working" warning acknowledges the buildings it lists: they stay quiet until they recover (a later breakage warns again), while a NEWLY broken building always warns immediately. Without this, dismissal silences the whole category for 4 game hours and then it returns.',
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "ResidencyControl",
		'DisplayName', "Residency control",
		'Help', 'Adds a per-Dome "Closed to new residents" policy row to the Dome infopanel: no new Colonists move in, while current residents keep commuting, working and using services normally. Not a quarantine — that toggle still exists and still seals the Dome.',
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "MultipleSuns",
		'DisplayName', "Multiple Artificial Suns",
		'Help', "Lets you build more than one Artificial Sun, and fixes the base-game bug where solar panels only ever check the first sun for night-time light. Turning it off restores the one-per-colony limit (existing suns keep working).",
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "DroneOverhaul",
		'DisplayName', "Drone dispatch overhaul (experimental)",
		'Help', "With overlapping Drone Hub coverage, the base game lets a far-away hub's drone claim a repair that idle drones are parked next to. This makes the CLOSEST hub's fleet get first claim on repair and cleaning jobs (a far fleet still serves if the near one doesn't respond within seconds), and lets idle drones help a neighboring OVERLOADED hub with nearby repairs. Player orders, hauling, construction and RC rovers are untouched.",
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "CohortHousing",
		'DisplayName', "Cohort housing — Seniors & Children",
		'Help', "Seniors and Children living in normal housing automatically move into free Retirement Home / Nursery slots — in their own Dome first, in any reachable Dome second — and are left completely alone when no such slot exists. Employed Seniors stay put; your manual residence and Dome assignments always win; quarantine and closed Domes are respected. No dome designation needed: concentrate the cohort buildings where you want the cohort to live.",
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionChoice', {
		'name', "DroneSpeedDial",
		'DisplayName', "Drone speed",
		'Help', "Adds a multiple of base Drone movement speed: 2x adds +100%, 3x adds +200%, 5x adds +400%, stacking on top of any speed techs the save has (Low-G Drive, Advanced Drone Drive). Drones only — rovers and shuttles are untouched. Takes effect immediately; 1x is exactly vanilla.",
		'DefaultValue', "1x (base)",
		'ChoiceList', { "1x (base)", "2x", "3x", "5x" },
	}),
	PlaceObj('ModItemOptionChoice', {
		'name', "DroneCarryDial",
		'DisplayName', "Drone carry capacity",
		'Help', "How many extra units of a resource a Drone carries per trip, on top of the base 1 (the Artificial Muscles breakthrough adds another +1 — they stack). Takes effect immediately; +0 is exactly vanilla.",
		'DefaultValue', "+0 (base)",
		'ChoiceList', { "+0 (base)", "+1", "+2" },
	}),
}
