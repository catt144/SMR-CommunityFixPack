-- F120: restore a Wildfire cure discovery lost during tech-point conversion.
--
-- Legacy Research:AddTech stores field='Mysteries'. The converter preserves
-- BuriedWonders/Storybits/Breakthroughs only, leaving a previously revealed cure
-- hidden when its scenario has already passed SA_RevealTech. The current
-- scenario remaps that reveal to WildfireCure_1, not the final WildfireCure.
-- Reach is platform-conditional: retail Steam blocks pre-402200 saves;
-- non-Steam retail offers Load anyway. This does not explain a fresh Steam
-- colony's missing cure. See F120 for the reporter/evidence distinction.
--
-- Recovery is the fix: on PostLoadGame, restore ONLY that entrance, ONLY in a
-- Wildfire colony with a positive legacy discovery and an entirely hidden
-- shipped family. No points, research, effects or scenario steps are granted.
-- A second load and any partial/completed/vanilla-restored family are no-ops.
-- PreProcessLockablePresets makes handler order irrelevant: newly introduced
-- presets are initialised once before inspection; their processed markers
-- remain intact, so vanilla does not re-hide the repaired entrance next load.
--
-- Save safety: additive synchronous handler; no new GameVar, object field,
-- stored function, wrapper or thread. Only the game's own discovery lock state
-- changes, through UnlockTech. Vanilla load processing preserves this state
-- with the fix disabled in desk tests; retail save serialization is untested.
-- Enable path: apply inspects code only; the same handler runs on the next
-- colony load after either a cold boot or main-menu mod enable.
--
-- Behaviour guard: sample the shipped lock reader on closed owner/preset
-- tables, requiring hidden and cleared states to differ. No globals are swapped
-- and no live owner is touched. Runtime legacy+hidden-family checks detect the
-- defect itself and stand down when vanilla or a prior recovery opened it.
-- This additive repair carries no copied shipped body. A missing modern Player
-- API declines the legacy game branch without reading version numbers.
--
-- SRC: Lua/TechTree.lua SavegameFixups.TechPoints_MigrateDiscoveredSpecialTechs sha256=6df74c576e1c5a9aba231fbb704ab83e71abb012344f8bca253eb91510417b79
-- DEFECT: status\.discovered\s+and\s+migrateGroups\[status\.field\]
-- Absence-shaped defect: the inclusion list omits Mysteries; a refactor needs
-- semantic review, and adding a different recovery elsewhere may not match it.

local FIX_ID = "WildfireCureMigration"
local BASE = "WildfireCure"
local HEAD = "WildfireCure_1"

local function recover()
	local colony, player = rawget(_G, "UIColony"), rawget(_G, "UIPlayer")
	if not colony or colony.mystery_id ~= "TheMarsBug" then return end
	local statuses = colony.tech_status
	local old = type(statuses) == "table" and statuses[BASE]
	if type(old) ~= "table" or old.field ~= "Mysteries"
		or type(old.discovered) ~= "number" or old.discovered <= 0 then return end
	if not player or not player.LockablePresetsInitialized then return end
	local techs = rawget(_G, "Techs")
	local remap = rawget(_G, "MysteryTechRevealRemapping")
	if type(techs) ~= "table" or type(remap) ~= "table" or remap[BASE] ~= HEAD then return end
	for i = 0, 10 do
		local id = i == 0 and BASE or (BASE .. "_" .. i)
		local tech = techs[id]
		if not tech or tech.group ~= "Mysteries" or tech.LockState ~= "hidden"
			or not tech.CanBeResearched then return end
	end

	PreProcessLockablePresets()
	for i = 0, 10 do
		local id = i == 0 and BASE or (BASE .. "_" .. i)
		if GetTechState(id, player) ~= "hidden" then return end
	end
	if UnlockTech(HEAD, player) then
		SMRFixPack.Log("%s: restored the previously discovered Wildfire cure entrance after load", FIX_ID)
	end
end

OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, recover)

SMRFixPack.Register(FIX_ID, {
	title = "Restore the Wildfire cure discovery in converted saves",
	apply = function()
		return SMRFixPack.Require(FIX_ID, {
			{ class = "Player", method = "CanResearch" },
			{ global = "GetTechState" },
			{ global = "GetPresetLockStateAndText" },
			{ global = "UnlockTech" },
			{ global = "PreProcessLockablePresets" },
			{ probe = function()
				local preset = { class = "Tech", group = "Mysteries", id = HEAD }
				local owner = { PresetLockStates = { Tech = { Mysteries = {
					[HEAD] = { state = "hidden" },
				} } } }
				if GetPresetLockStateAndText(preset, owner) ~= "hidden" then return false end
				owner.PresetLockStates.Tech.Mysteries[HEAD] = nil
				return GetPresetLockStateAndText(preset, owner) == "enabled"
			end, reason = "the stored research lock states no longer match the recovery contract" },
		})
	end,
})
