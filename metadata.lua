return PlaceObj('ModDef', {
	'title', "Community Fix Pack",
	-- ⚠️ REWRITTEN 2026-08-13 (owner instruction, public-docs chain prompt 3).
	-- The previous `description` carried TWO defects that would have shipped:
	-- it told players individual fixes can be disabled "via the console", which
	-- is FALSE (Register reads the veto table at mod load, 00_Core.lua:384-388 —
	-- the fixes are applied long before anyone can type), and it named the
	-- sibling mod by its dead working title "Community Opt-In Pack". Both are
	-- corrected below. Full pages + the claim traces: docs/agent/reports/
	-- STORE_FIXPACK.md and STORE_METADATA_STRINGS.md.
	'description', "Bug fixes for Surviving Mars: Relaunched. Almost every fix targets a defect verified in the game's own code — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs rather than rebalancing the game: preferences and features live in a separate mod, Community Fix Pack: Opt-In Modules, and neither mod needs the other. Nothing is patched on disk; the mod wraps the game's own code at runtime and no game files are modified. Safe to add to a save you have already played — the pack writes almost nothing into your savegame, and removing it simply lets the original bugs come back. Every fix checks the game's code before it patches anything and stands down if an official patch changes what it was written for. Five of the fixes are judgment calls rather than plain repairs, and the mod page says which and why.",
	'short_description', "Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the game's own code rather than rebalancing the game, and it is safe to add to a save you have already played.",
	-- ⚠️ `last_changes` no longer quotes a fix COUNT, on purpose: every previous
	-- wording carried one and it drifted every time a fix was retired or added
	-- (68 -> 66 after F24/F28 went `wontfix`, 67 after F83). If launch prep puts
	-- a number back, recount it from `python tools/doccheck.py --emit-counts`
	-- in the same commit — never from this comment.
	-- ⛔ CORRECTED 2026-08-14 (release-3 prompt 1): this field STILL carried the
	-- dead working title "Community Opt-In Pack" that the comment ten lines above
	-- says was corrected — the 08-13 pass fixed `description` and missed this
	-- string. A player told to look for that name would find nothing on any
	-- store. Licence: the owner's standing 22b word ("change any wordings to
	-- their accurate versions"); text-only, no behaviour, no version bump.
	'last_changes', "Initial release: the bug fixes. The optional modules moved to their own mod, Community Fix Pack: Opt-In Modules.",
	'id', "SMR_CommunityFixPack",
	'author', "catt144",
	'version', 1,
	'version_major', 1,
	'version_minor', 0,
	'lua_revision', 350453,
	-- saves made with the pack load fine without it (FIX_POLICY §3), so don't
	-- nag players who removed it with the missing-mods prompt
	'optional_mod', true,
	-- the packer includes EVERYTHING recursively minus this list (Mod.lua:250-256,
	-- GedModEditor.lua:716-732) — without the extra patterns docs/, README.md,
	-- .gitignore and .claude/ all ship inside the .hpk. LICENSE ships on purpose.
	-- ⭐ THREE PATTERNS ADDED 2026-08-14 AT LAUNCH PREP (release-3 prompt 1) —
	-- checklist item 23, the owner's ruling "YES, add the missing patterns, at
	-- launch prep", all three mods. MEASURED before and after over the real
	-- tree: without them this package shipped `CLAUDE.md`, `.gitattributes` and
	-- all TEN files of `tools/` into a player's download — 90 files where 78
	-- belong. Nothing there ever RUNS (only `code` executes), but CLAUDE.md is
	-- agent instructions and `tools/` is our build machinery.
	-- ⚠️ `LICENSE` is NOT excluded, deliberately: item 23 listed it, but the
	-- rescue mod built afterwards states "LICENSE ships on purpose" and a licence
	-- inside the package is right. All three mods now agree on that.
	-- ℹ️ Item 23's one unverifiable sub-case — whether `.github/` slips past the
	-- `.git` pattern — is MOOT here: no mod repo has a `.github/` directory
	-- (checked in all three, 2026-08-14). Only the site repo does, and it is not
	-- a mod.
	'ignore_files', {
		"*.git/*",
		"*.svn/*",
		"*/Source/*",
		"*/SourceData/*",
		"*/docs/*",
		"*/.claude/*",
		"*/tools/*",
		"*README.md",
		"*CLAUDE.md",
		"*.gitignore",
		"*.gitattributes",
	},
	-- ⛔ NO `default_options` FIELD, AND THAT IS THE POINT (2026-08-12, the
	-- opt-in split). This field is what makes Options → Mod Options list a mod
	-- at all (ModDef:HasOptions reads it, Mod.lua:473-475). The pack's eight
	-- optional modules — and every toggle and dial they owned — moved to the
	-- standalone Community Opt-In Pack (SMR_CommunityOptInPack), so this pack
	-- has nothing for a player to set and correctly stops appearing on that
	-- page. 00_Core.lua keeps its `optional`/OptionEnabled/ApplyModOptions
	-- machinery: dormant, not wrong, and not worth an unforced edit to the one
	-- file every fix depends on.
	'code', {
		"Code/00_Core.lua",
		"Code/Fix_CaveInsNoDisasters.lua",
		"Code/Fix_MeteorFrequency.lua",
		"Code/Fix_UpgradeModifierLeak.lua",
		"Code/Fix_NightShiftWork.lua",
		"Code/Fix_MilestoneCrash.lua",
		"Code/Fix_WispRewards.lua",
		"Code/Fix_TouristApplicants.lua",
		"Code/Fix_TrainsToVoid.lua",
		"Code/Fix_LanderEmptyLaunch.lua",
		"Code/Fix_LanderCargoRatchet.lua",
		"Code/Fix_LanderReturnFuel.lua",
		"Code/Fix_ShelterReflex.lua",
		"Code/Fix_BrokenTrackSalvage.lua",
		"Code/Fix_TrackSalvageWipe.lua",
		"Code/Fix_LakeEntombment.lua",
		"Code/Fix_GhostFarmOxygen.lua",
		"Code/Fix_RocketDroneChurn.lua",
		"Code/Fix_ShuttleTransportCache.lua",
		"Code/Fix_VacuumWalks.lua",
		"Code/Fix_ArrivalDeaths.lua",
		"Code/Fix_DroneUnreachableForever.lua",
		"Code/Fix_StaleReservations.lua",
		"Code/Fix_CrystalMysteryHang.lua",
		"Code/Fix_TouristSatisfaction.lua",
		"Code/Fix_TrainPlatformWedge.lua",
		"Code/Fix_LowStorageWarning.lua",
		"Code/Fix_CommandCenterNumbers.lua",
		"Code/Fix_DomeOverviewHighlight.lua",
		"Code/Fix_TrainCargoDumping.lua",
		"Code/Fix_UniversityOvertraining.lua",
		"Code/Fix_DestroyedTunnels.lua",
		"Code/Fix_DustSicknessBiorobots.lua",
		"Code/Fix_DustSicknessDamage.lua",
		"Code/Fix_GeneForging.lua",
		"Code/Fix_MirrorSphereSite.lua",
		"Code/Fix_PayloadTemplateRefill.lua",
		"Code/Fix_AsteroidLanderAvailable.lua",
		"Code/Fix_ShuttleHubOffAvailable.lua",
		"Code/Fix_FreedHousingNotice.lua",
		"Code/Fix_DomeFreeSpaceMismatch.lua",
		"Code/Fix_SmallLandscapeSites.lua",
		"Code/Fix_LandscapeUnitFilter.lua",
		"Code/Fix_RocketInteractGuard.lua",
		"Code/Fix_TrackConnectorPingPong.lua",
		"Code/Fix_TrackTunnelPowerBridge.lua",
		"Code/Fix_GridGlobalStorage.lua",
		"Code/Fix_LastTransmissionStorage.lua",
		"Code/Fix_GraphConsumedCaption.lua",
		"Code/Fix_MoraleComfortTooltip.lua",
		"Code/Fix_TrainWaitTime.lua",
		"Code/Fix_FounderTraitNotification.lua",
		"Code/Fix_StorageRateModifiers.lua",
		"Code/Fix_SequenceLatents.lua",
		"Code/Fix_IndependenceTerraforming.lua",
		"Code/Fix_TrackSalvageRefund.lua",
		"Code/Fix_LayoutTechLock.lua",
		"Code/Fix_TrainMinors.lua",
		"Code/Fix_DroneTransportMinors.lua",
		"Code/Fix_AnomalyCaveInMap.lua",
		"Code/Fix_TechDescriptionBuilding.lua",
		"Code/Fix_BombardmentSpread.lua",
		"Code/Fix_ExtenderFlapChurn.lua",
		"Code/Fix_DisasterPredictionLeak.lua",
		"Code/Fix_MeteorStormWedge.lua",
		"Code/Fix_RainsDeadlock.lua",
		"Code/Fix_FirstAsteroidPrefabs.lua",
		"Code/Fix_SaintBlessing.lua",
		"Code/Fix_DustDevilsDescrMap.lua",
		"Code/Fix_AstrogeologistExtractors.lua",
		"Code/Fix_SinkholeIndestructible.lua",
		"Code/Fix_DustStormUndergroundBreaks.lua",
		"Code/Fix_DustDevilSpawnGate.lua",
		"Code/Fix_ExoticDepositSign.lua",
		"Code/90_SaveSanitizer.lua",
	},
	'TagGameplay', true,
})
