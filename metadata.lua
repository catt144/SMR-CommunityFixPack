return PlaceObj('ModDef', {
	'title', "Community Fix Pack",
	'description', "Fixes bugs in Surviving Mars: Relaunched gameplay code. Every fix targets a verified defect in the game's Lua source, patches at runtime in a mod-compatible way (no game files are modified), and can be individually disabled. See the mod page for the full list of fixes.",
	'id', "SMR_CommunityFixPack",
	'author', "TBD_SET_BEFORE_RELEASE",
	'version', 1,
	'lua_revision', 350453,
	'code', {
		"Code/00_Core.lua",
		"Code/Fix_CaveInsNoDisasters.lua",
		"Code/Fix_MeteorFrequency.lua",
		"Code/Fix_UpgradeModifierLeak.lua",
		"Code/Fix_NightShiftWork.lua",
		"Code/Fix_MilestoneCrash.lua",
	},
	'TagGameplay', true,
})
