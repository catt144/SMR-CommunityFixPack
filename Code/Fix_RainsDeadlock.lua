-- F81 (rains half): one collision with any other disaster kills a rain type for
-- the rest of the save.
--
-- Defect (TerraformingDisasters.lua:310-316, game 1.0.7.396349; shipped Lua
-- verified byte-identical to Src):
--     function RainsDisasterLoop(settings)
--         while true do
--             Sleep(settings.spawntime + AsyncRand(settings.spawntime_random))
--             CreateGameTimeThread(RainsDisasterActivation, settings)
--             WaitMsg("RainDisasterEnd")          -- NO TIMEOUT
--         end
--     end
-- RainsDisasterActivation opens with `if IsDisasterActive() or
-- IsDisasterPredicted() then return end` (:277) — it returns WITHOUT starting a
-- rain, FinishRainProcedure's Msg("RainDisasterEnd") (:268) never comes, and the
-- untimed WaitMsg blocks forever. The collision window is every other disaster's
-- ACTIVE phase plus every WARNING window — up to 75h each with sensor towers at
-- the cap (MapSettings.lua:94-98) — so on a long save a collision is a
-- certainty. Nothing rescues it: UpdateRainsThreads REUSES any valid activation
-- thread (:412), and a thread blocked in WaitMsg is perfectly valid, which is
-- why the user's greenhouse-gas imports produced no rain.
--
-- Fix (FIX_POLICY §1 rank 5, deliberately: a 7-line leaf global with one
-- changed line — the F22/F12 replacement precedent at its smallest):
--   * the WaitMsg gets a timeout LONGER than any legitimate warning + rain
--     (settings.max_duration + SensorTowerPredictionMaxTime + one sol ≈ 7 sols
--     for the default presets), so a healthy cycle is never cut short — a
--     premature wake merely re-rolls the next spawn — while a collided cycle
--     costs ~7 sols instead of the save. The timeout must exceed
--     warning+duration: a NORMAL rain's activation carries no notification and
--     no prediction flag during its warning sleep (:304-306), so a shorter
--     timeout could double-start that rain type.
--   * threads persisted in existing saves resume the OLD unbounded body, so a
--     PostLoadGame pass swaps each persisted loop thread for a fresh one running
--     the fixed body — surgical DeleteThread + recreate with the same settings,
--     the exact pattern of vanilla's own RestartGlobalGameTimeThread
--     (Config\_fixup.lua:18-22). The pass never touches main_thread (an
--     in-flight warning or rain continues undisturbed) and marks each entry it
--     has refreshed (SMRFixPack_fixed_loop) so reloads do not re-roll rain
--     cycles every time. FIX_POLICY §3 note on that marker: it is one boolean
--     inside an entry of the existing RainsDisasterThreads GameVar; vanilla
--     iterates those entries by known field names only and copies entries
--     wholesale on reuse (:411-415), so the marker survives reuse, disappears
--     with recreation, and a save loaded WITHOUT the mod ignores it entirely.

local FIX_ID = "RainsDeadlock"

local log = SMRFixPack.Log

-- Body below is a copy of TerraformingDisasters.lua:310-316 (shipped Src, game
-- 1.0.7.396349); the only change is marked with `-- FIX:`. No upvalues: threads
-- suspended inside it persist by the global name this function is written to.
local function fixed_loop(settings)
	while true do
		Sleep(settings.spawntime + AsyncRand(settings.spawntime_random))
		CreateGameTimeThread(RainsDisasterActivation, settings)
		-- FIX: bounded wait — longer than any legal warning + rain, so a healthy
		-- FIX: cycle is untouched and a collided one resumes instead of dying
		WaitMsg("RainDisasterEnd", (settings.max_duration or 3 * const.DayDuration)
			+ const.SensorTowerPredictionMaxTime + const.DayDuration)
	end
end
SMRFixPack.RainsFixedLoop = fixed_loop -- probe surface: the global must BE this

SMRFixPack.Register(FIX_ID, {
	title = "A rain that collides with another disaster retries instead of never raining again",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "RainsDisasterLoop" },
			{ global = "RainsDisasterActivation" },
		})
		if err then return err end
		return SMRFixPack.SetGlobal("RainsDisasterLoop", fixed_loop,
			"replacing RainsDisasterLoop did not land (mod env change?)")
	end,
})

-- Swap persisted (old-body) loop threads for fresh fixed-body ones. Exposed for
-- the console and the TestKit; returns how many loops it refreshed.
function SMRFixPack.RefreshRainsLoops()
	local threads = rawget(_G, "RainsDisasterThreads")
	if type(threads) ~= "table" then return 0 end
	local presets = rawget(_G, "Presets")
	presets = type(presets) == "table" and presets.MapSettings
	presets = type(presets) == "table" and presets.RainsDisaster
	local refreshed = 0
	for rain_type, data in pairs(threads) do
		if type(data) == "table" and IsValidThread(data.activation_thread)
				and not data.SMRFixPack_fixed_loop then
			local settings = presets and data.id and presets[data.id]
			if settings then
				DeleteThread(data.activation_thread)
				data.activation_thread = CreateGameTimeThread(RainsDisasterLoop, settings)
				data.SMRFixPack_fixed_loop = true
				refreshed = refreshed + 1
				log("%s: '%s' rain loop moved onto the bounded body (settings '%s')",
					FIX_ID, tostring(rain_type), tostring(data.id))
			else
				log("%s: '%s' rain loop kept as-is — settings '%s' not found in presets",
					FIX_ID, tostring(rain_type), tostring(data.id))
			end
		end
	end
	return refreshed
end

OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(SMRFixPack.RefreshRainsLoops)
	if not ok then log("%s: rains-loop refresh failed: %s", FIX_ID, tostring(err)) end
end)
