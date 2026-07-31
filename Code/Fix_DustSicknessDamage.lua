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

local log = SMRFixPack.Log

-- The shipped body with the one line corrected, marked -- FIX.
local function dust_sickness_daily_update(colonist, trait)
	if g_DustStormStart then
		local change = 5 + colonist:Random(trait.param)
		colonist:ChangeHealth(-change * const.Scale.Stat, trait.id) -- FIX (F17): was -trait.param, ignoring `change`
	end
end

-- The scaffold (one pass per load, veto re-read, F75 data_loaded latch gate,
-- DataChanged re-arm) lives in SMRFixPack.DataPatch since Phase 4 (audit C2).
local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "TraitPreset",
	pass = function(ctx)
		local presets = rawget(_G, "TraitPresets")
		local trait = presets and presets.DustSickness
		if type(trait) ~= "table" then
			-- Before DataLoaded this just means "presets not loaded yet"; after
			-- it, a missing preset means a future update removed the target.
			if ctx.data_loaded then
				ctx.patched = true
				ctx.latch("TraitPresets.DustSickness not found (game update changed it?)",
					"TraitPresets.DustSickness not found")
			end
			return
		end
		if type(trait.param) ~= "number" or type(trait.daily_update_func) ~= "function" then
			ctx.latch("TraitPresets.DustSickness has no param/daily_update_func")
			ctx.patched = true
			return
		end
		trait.daily_update_func = dust_sickness_daily_update
		ctx.patched = true
	end,
})

SMRFixPack.Register(FIX_ID, {
	title = "Dust Sickness deals its intended random damage instead of the maximum every sol",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ path = { "const", "Scale", "Stat" }, kind = "number" },
		})
		if err then return err end
		patch()   -- no-op unless the presets are already loaded
	end,
})
