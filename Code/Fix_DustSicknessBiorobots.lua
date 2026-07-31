-- F40: Dust Sickness infects Biorobots.
--
-- Defect: every place that hands out the Dust Sickness trait filters out children
-- and nobody else:
--     Data\StoryBit\DustSickness.lua:63-77, :103-117            (both outcomes)
--     Data\StoryBit\DustSickness_GeneratSick.lua:5-26           (ActivationEffects)
--     Data\StoryBit\DustSickness_GeneratSickNotWorking.lua:5-26 (ActivationEffects)
-- Each is a ForEachExecuteEffects over the Colonist label whose only filter is
-- `HasTrait{Negate = true, Trait = "Child"}`, followed by AddTrait "DustSickness".
-- Biorobots (the Android trait, TraitPreset.lua:436-452) are ordinary Colonists in
-- the label, so they get infected and then bleed Health every dust storm via the
-- trait's daily_update_func — and, on the "shouldn't work" branch, are also given
-- StatusEffect_UnableToWork until the cure tech is researched.
--
-- Colonist:AddTrait (Colonist.lua:426-453) never consults `incompatible`, so
-- marking the traits incompatible would not stop this — the filter list is the
-- only real gate.
--
-- Patch approach: data patch (FIX_POLICY §1.1) — append
-- `HasTrait{Trait = "Android", Negate = true}` to the filter list of every
-- ForEachExecuteEffects in those three storybits that adds the trait. Other mods
-- reading the presets see the corrected data, and nothing in the code path is
-- replaced. The search is by structure ("this effect adds DustSickness"), not by
-- position, so a reshuffled preset is still handled; if it matches nothing the fix
-- reports itself inactive.
--
-- Timing: presets load after mod code (LoadData -> Msg("DataLoaded"),
-- CommonLua\Dlc.lua:640-662), hence the DataLoaded/DataChanged handlers.
--
-- Savegame repair: biorobots already carrying the trait keep losing Health for the
-- rest of the game, so a LoadGame pass removes it from them. It also clears
-- StatusEffect_UnableToWork from those same colonists, mirroring what the
-- DustSickness_CureFound storybit does when the cure is found — only for androids
-- that carry the Dust Sickness trait at that moment, since that storybit is the
-- only shipped source that pairs the two.

local FIX_ID = "DustSicknessBiorobots"

-- Cited above; each of these is a storybit that hands out the trait.
local STORYBIT_IDS = { "DustSickness", "DustSickness_GeneratSick", "DustSickness_GeneratSickNotWorking" }

local log = SMRFixPack.Log

local function adds_dust_sickness(effects)
	if type(effects) ~= "table" then return false end
	for _, e in ipairs(effects) do
		if type(e) == "table" and e.class == "AddTrait" and e.Trait == "DustSickness" then
			return true
		end
	end
	return false
end

local function has_android_filter(filters)
	for _, f in ipairs(filters) do
		if type(f) == "table" and f.class == "HasTrait" and f.Trait == "Android" and f.Negate then
			return true
		end
	end
	return false
end

-- Storybit presets are small trees of nested PlaceObj nodes (outcomes hold
-- effects hold effects), so walk them rather than hard-coding indices.
local function patch_node(node, seen, depth, stats)
	if type(node) ~= "table" or seen[node] or depth > 8 then return end
	seen[node] = true
	if node.class == "ForEachExecuteEffects" and adds_dust_sickness(node.Effects) then
		stats.found = stats.found + 1
		local filters = node.Filters
		if type(filters) == "table" then
			if not has_android_filter(filters) then
				filters[#filters + 1] = HasTrait:new{ Trait = "Android", Negate = true }
				stats.patched = stats.patched + 1
			end
		end
	end
	for _, v in pairs(node) do
		patch_node(v, seen, depth + 1, stats)
	end
end

local patched = false
local data_loaded = false   -- DataLoaded has fired at least once

local function patch()
	if patched then return end
	-- FIX (audit 2026-07-29, A1): honor the per-fix veto here too — these OnMsg
	-- handlers are installed unconditionally, and Register's veto only skips
	-- apply(), so without this check a disabled fix still mutated the presets.
	local disabled = rawget(_G, "SMRFixPack_Disabled")
	if type(disabled) == "table" and disabled[FIX_ID] then return end
	local storybits = rawget(_G, "StoryBits")
	local present = false
	if type(storybits) == "table" and type(rawget(_G, "HasTrait")) == "table" then
		for _, id in ipairs(STORYBIT_IDS) do
			if storybits[id] then
				present = true
				break
			end
		end
	end
	if not present then
		-- Before DataLoaded this just means "presets not loaded yet". Only after
		-- DataLoaded does an absent storybit mean a future update removed the
		-- target — latch inactive then instead of reporting active forever
		-- (audit 2026-07-29, B3; pattern: Fix_LastTransmissionStorage).
		if data_loaded then
			patched = true
			local entry = SMRFixPack.fixes[FIX_ID]
			if entry then
				entry.status = "inactive"
				entry.detail = "the Dust Sickness storybits are gone (game update changed them?)"
			end
			log("%s: inactive (the Dust Sickness storybits are gone)", FIX_ID)
		end
		return
	end

	local stats = { found = 0, patched = 0 }
	for _, id in ipairs(STORYBIT_IDS) do
		local sb = storybits[id]
		if sb then patch_node(sb, {}, 0, stats) end
	end
	patched = true

	if stats.found == 0 then
		local entry = SMRFixPack.fixes[FIX_ID]
		if entry then
			entry.status = "inactive"
			entry.detail = "no Dust Sickness storybit hands out the trait any more"
		end
		log("%s: inactive (no Dust Sickness storybit hands out the trait any more)", FIX_ID)
	end
end

SMRFixPack.Register(FIX_ID, {
	title = "Dust Sickness no longer infects Biorobots",
	apply = function()
		patch()   -- no-op unless the presets are already loaded
	end,
})

function OnMsg.DataLoaded()
	data_loaded = true
	patch()
end

function OnMsg.DataChanged(classes)
	if classes and not classes.StoryBit then return end
	patched = false
	patch()
end

-- Biorobots already infected in an existing save never recover on their own.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end

	local cured = 0
	AllMapsForEach("map", "Colonist", function(colonist)
		local traits = colonist.traits
		if traits and traits.Android and traits.DustSickness then
			colonist:Affect("StatusEffect_UnableToWork", false)
			colonist:RemoveTrait("DustSickness", "ignore_missing")
			cured = cured + 1
		end
	end)

	if cured > 0 then
		log("%s: cleared Dust Sickness from %d Biorobot(s)", FIX_ID, cured)
	end
end)
