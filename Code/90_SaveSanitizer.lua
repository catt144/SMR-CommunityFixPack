-- Save sanitizer — one-shot repair passes for state a bug already baked into a
-- savegame, kept together in one place (FIX_POLICY §3: cleanups are separate,
-- clearly marked and conservative by default).
--
-- Fixes with a live half carry their own LoadGame pass in their own file (F02,
-- F45, F37, F58, F06, F38, F39, F40). This module is for the remainder — damage
-- with nothing left to prevent, only to undo.
--
-- Contents:
--   F35  Large Wind Turbine buff lost by a broken migration fixup
--   F03  upgrade modifiers leaked onto domes and the colony by salvaged buildings
--
-- Both passes are read-only until they find something they can positively
-- identify as wrong, run on every PostLoadGame (after the shipped savegame
-- fixups — see the note on the handler below), and are idempotent — a second
-- run finds nothing.
--
-- NOT included, deliberately: F48 (station-connector fixup). See its BUGS.md
-- entry — the "corrected pass" re-runs OrderTrackElements, which rebuilds
-- `el.connections` and rewrites `node_idx` for every element of every track
-- (Tracks.lua:520-624) and whose only failure handling is an `assert(false, ...)`
-- that does not unwind in this engine. That is not a repair we can ship without
-- an in-game test, and its impact is P3.

local FIX_ID = "SaveSanitizer"

local log = SMRFixPack.Log

--------------------------------------------------------------------------------
-- F35 — Large Wind Turbines never got their Frictionless Composites buff back
--
-- Defect: SavegameFixups.WindTurbine_Large_ReapplyModifiers
-- (Lua\Buildings\WindTurbine.lua:78-88) exists to re-apply the tech's label
-- modifiers to saves that researched it before the tech data was corrected. The
-- tech carries THREE Effect_ModifyLabel entries — WindTurbine, WindTurbine_Large
-- and WindTurbine_Diffuser, +100% electricity_production each
-- (Data\TechPreset.lua:796-821) — and the fixup re-applies only
-- WindTurbine_Diffuser. Those are disjoint labels (a building is added to a label
-- named after its own class, Building:AddToCityLabels, Building.lua:427-443), so
-- nothing else covers Large turbines: in an affected save they stay unbuffed for
-- the rest of the game. Matches the "polymer upgrade works now, frictionless
-- doesn't" report.
--
-- Repair: for each of the tech's own effects, if the colony carries no
-- electricity_production modifier on that label at all, add the one the effect
-- describes. Driven by the preset rather than a hard-coded list, so a game update
-- that changes the tech changes this pass with it.
--
-- Conservative: the presence of ANY percent modifier for that property on that
-- label is taken as "already buffed" and the label is left alone. That errs
-- towards doing nothing rather than towards double-buffing.
local function repair_turbine_buff()
	local colony = rawget(_G, "UIColony")
	if not colony or type(colony.IsTechResearched) ~= "function"
			or type(colony.SetLabelModifier) ~= "function" then
		return 0
	end
	if not colony:IsTechResearched("FrictionlessComposites") then return 0 end

	local defs = rawget(_G, "TechDef")
	local tech = defs and defs.FrictionlessComposites
	if type(tech) ~= "table" then return 0 end

	local label_modifiers = colony.label_modifiers
	if type(label_modifiers) ~= "table" then return 0 end

	local restored = 0
	for _, effect in ipairs(tech) do
		local label = type(effect) == "table" and effect.Label
		local prop = label and effect.Prop
		local percent = prop and (effect.Percent or 0)
		if label and prop and percent ~= 0 then
			local present = false
			for _, mod in pairs(label_modifiers[label] or empty_table) do
				if type(mod) == "table" and mod.prop == prop and (mod.percent or 0) ~= 0 then
					present = true
					break
				end
			end
			if not present then
				-- Same shape the shipped fixup uses (WindTurbine.lua:81-86); a
				-- stable SMRFixPack_* id instead of its throwaway table, so this
				-- pass can recognise its own work on the next load.
				-- Amount is scaled the way the live tech apply scales it
				-- (Tech.lua:298-301); dormant today — all three effects ship with
				-- Amount 0 — but this pass is preset-driven by design.
				local scale = rawget(_G, "GetModifiablePropScale")
				colony:SetLabelModifier(label, "SMRFixPack_F35_" .. label, {
					amount = (effect.Amount or 0) * (scale and scale(prop) or 1),
					percent = percent,
					prop = prop,
					id = "GameEffect",
				})
				restored = restored + 1
				log("%s: restored the %s buff on the %s label (+%d%% %s)",
					FIX_ID, "Frictionless Composites", label, percent, prop)
			end
		end
	end
	return restored
end

--------------------------------------------------------------------------------
-- F03 — upgrade modifiers left behind by salvaged buildings
--
-- Defect: Building:StopUpgradeModifiers iterated a string-keyed table with
-- ipairs, so it turned nothing off (Building.lua:1268-1274). Fix_UpgradeModifierLeak
-- stops new leaks; this pass clears the ones already in the save.
--
-- A leaked entry is a LabelModifier sitting in some container's
-- `label_modifiers[label]` under the id ApplyUpgrade minted for it,
-- `string.format("%s_upgrade%d_mod_%d", self.handle, tier, i)`
-- (Building.lua:1155). The handle in that id is the OWNING building's. So an
-- entry whose handle no longer resolves to a live object is, by construction,
-- one whose building is gone — the leak — and nothing else in the game writes
-- ids of that shape.
--
-- Conservative: if the handle still resolves to anything valid, the entry is
-- left alone, even though handles can in principle be recycled. A missed leak is
-- cheap; wrongly stripping a live building's upgrade bonus is not.
local UPGRADE_MOD_ID = "^(%d+)_upgrade%d+_mod_%d+$"

local function sweep_leaked_upgrade_modifiers(container)
	local by_label = type(container) == "table" and container.label_modifiers
	if type(by_label) ~= "table" or type(container.SetLabelModifier) ~= "function" then
		return 0
	end
	local handles = rawget(_G, "HandleToObject")
	if type(handles) ~= "table" then return 0 end

	local removed = 0
	for label, modifiers in pairs(by_label) do
		-- collect first: SetLabelModifier writes into this very table
		local stale
		for id in pairs(modifiers) do
			if type(id) == "string" then
				local handle = string.match(id, UPGRADE_MOD_ID)
				local owner = handle and handles[tonumber(handle)]
				if handle and not (owner and IsValid(owner)) then
					stale = stale or {}
					stale[#stale + 1] = id
				end
			end
		end
		for _, id in ipairs(stale or empty_table) do
			container:SetLabelModifier(label, id, nil)
			removed = removed + 1
		end
	end
	return removed
end

local function repair_leaked_upgrade_modifiers()
	local removed = 0

	local colony = rawget(_G, "UIColony")
	if colony then removed = removed + sweep_leaked_upgrade_modifiers(colony) end

	for _, city in ipairs(rawget(_G, "Cities") or empty_table) do
		removed = removed + sweep_leaked_upgrade_modifiers(city)
		local labels = city.labels
		for _, dome in ipairs(labels and labels.Dome or empty_table) do
			removed = removed + sweep_leaked_upgrade_modifiers(dome)
		end
	end

	if removed > 0 then
		log("%s: removed %d leaked upgrade modifier(s) from salvaged buildings", FIX_ID, removed)
	end
	return removed
end

--------------------------------------------------------------------------------

-- Exposed so the passes can be re-run from the console on a suspect save (and so
-- the Test Kit can drive them). Both return how many things they repaired.
SMRFixPack.Sanitizer = {
	RepairTurbineBuff = repair_turbine_buff,
	RepairLeakedUpgradeModifiers = repair_leaked_upgrade_modifiers,
}

SMRFixPack.Register(FIX_ID, {
	title = "Savegame repair: lost Wind Turbine tech buff, leaked upgrade bonuses",
	apply = function()
		-- Everything this module touches is savegame state, so there is nothing
		-- to patch at load time. The self-check is that the APIs the passes call
		-- still exist; the game objects themselves are re-checked on every run.
		local LC = rawget(_G, "LabelContainer")
		if type(LC) ~= "table" or type(LC.SetLabelModifier) ~= "function" then
			return "LabelContainer.SetLabelModifier not found (game update changed it?)"
		end
		if type(rawget(_G, "HandleToObject")) ~= "table" then
			return "HandleToObject not found (game update changed it?)"
		end
	end,
})

-- PostLoadGame, NOT LoadGame: UnpersistGame fires Msg("LoadGame"), then runs
-- FixupSavegame, then fires Msg("PostLoadGame") (CommonLua\Savegame.lua:810-813).
-- The F35 pass compensates for SavegameFixups.WindTurbine_Large_ReapplyModifiers,
-- and on the FIRST load of a save that fixup has not yet been applied to, a
-- LoadGame-time pass would run before it: the pass would see the Diffuser label
-- bare and buff it, then the shipped fixup would unconditionally add its own
-- +100% (WindTurbine.lua:80-87 has no already-buffed check) — +200% baked into
-- the save permanently. After fixups the pass sees the world post-migration and
-- the "any percent modifier present → skip" guard holds. (Found by the wave-3
-- QA audit, 2026-07-25.)
OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(repair_turbine_buff)
	if not ok then log("%s: turbine-buff pass failed: %s", FIX_ID, tostring(err)) end

	ok, err = pcall(repair_leaked_upgrade_modifiers)
	if not ok then log("%s: upgrade-modifier pass failed: %s", FIX_ID, tostring(err)) end
end)
