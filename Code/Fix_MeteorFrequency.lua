-- F02: Meteors strike roughly every 6 game-hours instead of every 35-115+ hours.
--
-- Defect: in the "Meteors" global game-time thread (Lua\Meteors.lua:266-304) the
-- long wait between strikes was mangled into a dead `if`:
--     local start_time = GameTime()
--     if GameTime() - start_time > spawn_time - warning_time then Sleep(5000) end
-- The condition compares GameTime() against itself (always 0 > x is false), so the
-- only real wait is Sleep(Min(spawn_time, warning_time)) — and warning_time defaults
-- to 6 game hours. Designed intervals are 35-90h + 0-25h random. Perversely, Sensor
-- Towers (which ADD warning time) lengthen the interval, inverting their purpose.
-- The correct two-phase wait survives in DustDevils.lua:168-173 and in the
-- MeteorStorm thread right below (Meteors.lua:322-342), which proves the intent.
--
-- Patch approach: global thread bodies live in GlobalGameTimeThreadFuncs (registered
-- via GlobalGameTimeThread, Lua\Config\_fixup.lua:9-16) and are (re)started from that
-- table on PostNewGame. We install a repaired copy of the body there, and restart the
-- thread on savegame load (running saves resume the old persisted thread otherwise).
-- Restarting is safe: the loop carries no cross-iteration state; worst case a pending
-- strike/warning is rescheduled once on load.
--
-- Body below is a copy of Lua\Meteors.lua:266-304 (shipped Src, 2026-07); the only
-- changes are marked with `-- FIX:`.

SMRFixPack.Register("MeteorFrequency", {
	title = "Meteors strike on their designed 35-115h schedule instead of ~every 6 hours",
	apply = function()
		local funcs = rawget(_G, "GlobalGameTimeThreadFuncs")
		if type(funcs) ~= "table" or type(funcs.Meteors) ~= "function" then
			return "Meteors thread function not found (game update changed it?)"
		end

		funcs.Meteors = function()
			if IsGameRuleActive("NoDisasters") then return end
			if GeneratingMap then
				WaitMsg("MapGenerated")
			end
			local meteors = GetMeteorsDescr()
			g_MeteorsGameDescr = meteors
			if not meteors or meteors.forbidden then
				return
			end

			while true do
				local spawn_time = SessionRandom:Random(meteors.spawntime, meteors.spawntime + meteors.spawntime_random)
				local warning_time = GetDisasterWarningTime(meteors)
				Sleep(Max(spawn_time - warning_time, 1000)) -- FIX: was a dead `if` that never slept (compare DustDevils.lua:168)
				local chance = SessionRandom:Random(100)
				local meteors_type
				if chance < meteors.multispawn_chance then
					meteors_type = "multispawn"
				else
					meteors_type = "single"
				end
				local hit_time = Min(spawn_time, warning_time)
				Sleep(hit_time)
				MeteorsDisaster(meteors, meteors_type)

				local new_meteors = GetMeteorsDescr()
				g_MeteorsGameDescr = new_meteors
				while not new_meteors do
					Sleep(const.DayDuration)
					new_meteors = GetMeteorsDescr()
					g_MeteorsGameDescr = new_meteors
				end
				meteors = new_meteors
			end
		end
	end,
})

-- Loaded saves resume the persisted (buggy) thread; swap it for the fixed body.
function OnMsg.LoadGame()
	local fix = SMRFixPack.fixes.MeteorFrequency
	if fix and fix.status == "active" then
		RestartGlobalGameTimeThread("Meteors")
	end
end
