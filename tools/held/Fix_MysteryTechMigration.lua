-- F120: restore mystery tech discoveries lost during tech-point conversion.
--
-- HELD, NOT SHIPPED (owner ruling 2026-09-16, checklist 187). Registered in
-- neither items.lua nor metadata.lua; tools/ is excluded from the pack. The
-- state it repairs exists only in a colony started on 1.0.7 and loaded past
-- the old-save gate, which Steam and console refuse, so no platform the pack
-- serves can reach it and it cannot be tested on the owner's Steam copy.
-- Reopen on a report of a lost mystery technology on a carried-over 1.0.7
-- colony from a platform that offers Load anyway; re-register, re-run
-- tools/desk_mystery_tech_migration.py, and restore the RELEASE_OUTBOX row.
--
-- Legacy Research:AddTech stored field='Mysteries' for every mystery
-- technology. That field is not discoverable (1.0.7 Data/TechFieldPreset.lua),
-- so a positive legacy `discovered` marker came only from a scenario's
-- SA_RevealTech or a cheat. The converter preserves BuriedWonders/Storybits/
-- Breakthroughs only and drops the whole Mysteries field, so a tech revealed
-- before conversion stays hidden after it while its scenario keeps waiting on
-- research it can no longer offer. 1.0.7 shipped 17 such techs across 11
-- mysteries. In 1.1.0 three of them are chains whose entrance is the `_1`
-- member named by MysteryTechRevealRemapping; the other fourteen are single
-- nodes that are their own entrance. Wildfire alone has a partial vanilla
-- rescue (medical-building grants); the others have none.
-- Reach is platform-conditional: retail Steam blocks pre-402200 saves;
-- non-Steam retail offers Load anyway. This does not explain a fresh Steam
-- colony's missing cure. See F120 for the reporter/evidence distinction.
--
-- Recovery is the fix: on PostLoadGame, for every legacy Mysteries discovery
-- whose current family (the tech plus each `<id>_N` member) is entirely
-- hidden, unlock ONLY the entrance the current scenario would have revealed.
-- No points, research, effects or scenario steps are granted. A second load
-- and any partial/completed/vanilla-restored family are no-ops. There is no
-- colony-mystery gate: DefenseTower carries no `Mystery` property while the
-- other sixteen do, and the legacy marker itself is the evidence that the
-- scenario revealed the tech. PreProcessLockablePresets makes handler order
-- irrelevant: newly introduced presets are initialised once before
-- inspection; their processed markers remain intact, so vanilla does not
-- re-hide the repaired entrance next load.
--
-- Save safety: additive synchronous handler; no new GameVar, object field,
-- stored function, wrapper or thread. Only the game's own lock state changes,
-- through UnlockTech, which reaches every vanilla TechUnlocked listener
-- exactly as a scenario reveal does (Lua/Mysteries/Mystery.lua also discovers
-- and notifies the colony's Mystery_N display node). Vanilla load processing
-- preserves this state with the fix disabled in desk tests; retail save
-- serialization is untested. Enable path: apply inspects code only; the same
-- handler runs on the next colony load after either a cold boot or main-menu
-- mod enable.
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

local FIX_ID = "MysteryTechMigration"
local GROUP = "Mysteries"

-- The current family of a legacy id: the tech itself plus every `<id>_N`
-- member the shipped registry defines, in chain order.
local function family(techs, id)
	local members = { id }
	local n = 1
	while techs[id .. "_" .. n] do
		members[#members + 1] = id .. "_" .. n
		n = n + 1
	end
	return members
end

local function recover()
	local colony, player = rawget(_G, "UIColony"), rawget(_G, "UIPlayer")
	if not colony or type(colony.tech_status) ~= "table" then return end
	if not player or not player.LockablePresetsInitialized then return end
	local techs = rawget(_G, "Techs")
	local remap = rawget(_G, "MysteryTechRevealRemapping")
	if type(techs) ~= "table" or type(remap) ~= "table" then return end

	local pending = {}
	for id, old in pairs(colony.tech_status) do
		if type(id) == "string" and type(old) == "table" and old.field == GROUP
			and type(old.discovered) == "number" and old.discovered > 0 then
			local tech = techs[id]
			if tech and tech.group == GROUP and tech.LockState == "hidden" and tech.CanBeResearched then
				pending[#pending + 1] = id
			end
		end
	end
	if #pending == 0 then return end
	table.sort(pending)

	PreProcessLockablePresets()
	for _, id in ipairs(pending) do
		local entrance = remap[id] or id
		local members = family(techs, id)
		local ok = false
		for _, member in ipairs(members) do
			if member == entrance then ok = true end
		end
		for _, member in ipairs(members) do
			local tech = techs[member]
			if not tech or tech.group ~= GROUP or tech.LockState ~= "hidden"
				or not tech.CanBeResearched or GetTechState(member, player) ~= "hidden" then
				ok = false
				break
			end
		end
		if ok and UnlockTech(entrance, player) then
			SMRFixPack.Log("%s: restored the previously discovered %s entrance %s after load", FIX_ID, id, entrance)
		end
	end
end

OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, recover)

SMRFixPack.Register(FIX_ID, {
	title = "Restore revealed mystery technologies in converted saves",
	apply = function()
		return SMRFixPack.Require(FIX_ID, {
			{ class = "Player", method = "CanResearch" },
			{ global = "GetTechState" },
			{ global = "GetPresetLockStateAndText" },
			{ global = "UnlockTech" },
			{ global = "PreProcessLockablePresets" },
			{ global = "MysteryTechRevealRemapping", kind = "table" },
			{ probe = function()
				-- Stub contract: GetPresetLockStateAndText reads only
				-- owner.PresetLockStates[class][group][id].state and calls the
				-- pass-through GamePresetLockStateAndText; it is synchronous and
				-- writes nothing (CommonLua/Features/LockablePreset.lua:343-357).
				local preset = { class = "Tech", group = GROUP, id = "WildfireCure_1" }
				local owner = { PresetLockStates = { Tech = { [GROUP] = {
					WildfireCure_1 = { state = "hidden" },
				} } } }
				if GetPresetLockStateAndText(preset, owner) ~= "hidden" then return false end
				owner.PresetLockStates.Tech[GROUP].WildfireCure_1 = nil
				return GetPresetLockStateAndText(preset, owner) == "enabled"
			end, reason = "the stored research lock states no longer match the recovery contract" },
		})
	end,
})
