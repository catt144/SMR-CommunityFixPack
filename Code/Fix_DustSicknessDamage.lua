-- F17: Dust Sickness always deals its maximum damage instead of a random amount.
--
-- Defect: the trait's daily update (Data\TraitPreset.lua:85-91) computes the
-- randomised damage and then throws it away:
--     local change = 5 + colonist:Random(trait.param)
--     colonist:ChangeHealth(-trait.param*const.Scale.Stat, trait.id)
-- `change` is never read. Every sick colonist loses a flat `param` (10) Health per
-- sol during a dust storm; the intended spread is 5 to param+4 (5-14).
--
-- Patch approach: data patch — replace the preset's daily_update_func. This is the
-- most compatible option available (FIX_POLICY §1.1): the function is looked up
-- live on every daily tick (Colonist.lua:528-536 reads
-- TraitPresets[trait_id].daily_update_func), and any other mod reading the preset
-- sees the corrected version too.
--
-- Timing: presets do not exist when mod code loads (Data\ is read later, during
-- LoadData -> Msg("DataLoaded"), CommonLua\Dlc.lua:640-662), so the patch is
-- applied from a DataLoaded/DataChanged handler and, if data happens to be loaded
-- already, immediately.
--
-- Note we cannot tell an already-hotfixed daily_update_func from the broken one
-- (no introspection in the mod sandbox), so the fix deactivates only when the
-- preset or its param is missing. Re-applying the correct behaviour over an
-- already-correct version costs nothing.

local FIX_ID = "DustSicknessDamage"

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	if rawget(_G, "ModLog") then ModLog(msg) else print(msg) end
end

-- The shipped body with the one line corrected, marked -- FIX.
local function dust_sickness_daily_update(colonist, trait)
	if g_DustStormStart then
		local change = 5 + colonist:Random(trait.param)
		colonist:ChangeHealth(-change * const.Scale.Stat, trait.id) -- FIX (F17): was -trait.param, ignoring `change`
	end
end

local patched = false

local function patch()
	if patched then return end
	-- FIX (audit 2026-07-29, A1): honor the per-fix veto here too — these OnMsg
	-- handlers are installed unconditionally, and Register's veto only skips
	-- apply(), so without this check a disabled fix still mutated the preset.
	local disabled = rawget(_G, "SMRFixPack_Disabled")
	if type(disabled) == "table" and disabled[FIX_ID] then return end
	local presets = rawget(_G, "TraitPresets")
	local trait = presets and presets.DustSickness
	if type(trait) ~= "table" then return end
	if type(trait.param) ~= "number" or type(trait.daily_update_func) ~= "function" then
		local entry = SMRFixPack.fixes[FIX_ID]
		if entry then
			entry.status = "inactive"
			entry.detail = "TraitPresets.DustSickness has no param/daily_update_func"
		end
		log("%s: inactive (TraitPresets.DustSickness has no param/daily_update_func)", FIX_ID)
		patched = true
		return
	end
	trait.daily_update_func = dust_sickness_daily_update
	patched = true
end

SMRFixPack.Register(FIX_ID, {
	title = "Dust Sickness deals its intended random damage instead of the maximum every sol",
	apply = function()
		if type(rawget(_G, "const")) ~= "table" or type(const.Scale) ~= "table"
			or type(const.Scale.Stat) ~= "number" then
			return "const.Scale.Stat not found (game update changed it?)"
		end
		patch()   -- no-op unless the presets are already loaded
	end,
})

function OnMsg.DataLoaded()
	patch()
end

-- Covers a later data reload (the Mod Editor reloads presets in place).
function OnMsg.DataChanged(classes)
	if classes and not classes.TraitPreset then return end
	patched = false
	patch()
end
