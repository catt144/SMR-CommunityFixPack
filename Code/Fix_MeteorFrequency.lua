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
-- PT-01 REGRESSION (2026-07-25, reworked 2026-07-26): on a Very High map the fixed
-- thread struck 5 times on the designed cadence (+60/+39/+39/+57h, log
-- Mars.exe-20260725-19.04.10) and then went PERMANENTLY silent for 24+ sols in one
-- uninterrupted session (no load, no cheat, logger armed throughout). The hunt
-- falsified every static explanation:
--   * wait math is bounded even with 3 Sensor Towers: warning = Min(6h+12h*3, 75h)
--     = 42h and the two sleeps total Max(spawn-warning,1s) + Min(spawn,warning)
--     <= spawn+1s <= 60h — it cannot oversleep (this file, and MapSettings.lua:94-98,
--     _GameConst.lua:125-126);
--   * no [LUA ERROR] anywhere near the stall — thread errors always log, so the
--     loop did not die of an error;
--   * nothing in Src or either mod deletes/restarts the thread mid-game
--     (RestartGlobalGameTimeThread callers: _fixup.lua PostNewGame + our LoadGame);
--   * the descriptor-nil day-loop (Meteors.lua:297-301) needs Atmosphere > the 80%
--     MeteorStormStop threshold (TerraformingDisasters.lua:69, TerraformingParam.lua:81)
--     — impossible at sol 12;
--   * the first MeteorStorm was due in the same window (birth_hour = 250h,
--     Meteors.lua:316) and never visibly fired either — whatever stopped the loop is
--     outside both bodies (scheduler/persist side), and only a live capture can pin it.
-- Response: the body now writes a heartbeat (phase + timestamp) at every landmark,
-- the silent top-of-body exit is made loud, a daily watchdog restarts a provably
-- overdue thread and logs the pre-death state (thread alive-but-stuck vs dead), and
-- the LoadGame restart logs a necropsy of the persisted thread it replaces. All
-- report-and-continue; no new GameVars (heartbeat is session-local in SMRFixPack).
--
-- Body below is a copy of Lua\Meteors.lua:266-304 (shipped Src, game 1.0.7.396349); the only
-- changes are marked with `-- FIX:`.

local log = SMRFixPack.Log

-- The thread body below must keep ZERO upvalues (like the shipped body it copies):
-- the running thread is persisted into saves, and a closure that only does global
-- lookups is the persistence shape the engine has already proven it handles. The
-- body therefore reaches these helpers through the real global SMRFixPack.
SMRFixPack.MeteorsNote = log
function SMRFixPack.MeteorsBeatSet(phase)
	SMRFixPack.MeteorsBeat = { t = GameTime(), phase = phase }
end

SMRFixPack.Register("MeteorFrequency", {
	title = "Meteors strike on their designed 35-115h schedule instead of ~every 6 hours",
	apply = function()
		local funcs = rawget(_G, "GlobalGameTimeThreadFuncs")
		if type(funcs) ~= "table" or type(funcs.Meteors) ~= "function" then
			return "Meteors thread function not found (game update changed it?)"
		end

		funcs.Meteors = function()
			SMRFixPack.MeteorsBeatSet("thread-start") -- FIX: heartbeat for the PT-01 watchdog (see header)
			if IsGameRuleActive("NoDisasters") then
				SMRFixPack.MeteorsBeatSet("no-disasters-exit") -- FIX: the silent exits become visible states
				return
			end
			if GeneratingMap then
				WaitMsg("MapGenerated")
			end
			local meteors = GetMeteorsDescr()
			g_MeteorsGameDescr = meteors
			if not meteors or meteors.forbidden then
				-- FIX: this return is the only way the body can end silently — log it
				SMRFixPack.MeteorsBeatSet("descriptor-exit")
				SMRFixPack.MeteorsNote("MeteorFrequency: Meteors thread exiting at start — descriptor %s",
					meteors and "forbidden" or "missing")
				return
			end

			while true do
				local spawn_time = SessionRandom:Random(meteors.spawntime, meteors.spawntime + meteors.spawntime_random)
				local warning_time = GetDisasterWarningTime(meteors)
				SMRFixPack.MeteorsBeatSet("rolled") -- FIX: heartbeat
				Sleep(Max(spawn_time - warning_time, 1000)) -- FIX: was a dead `if` that never slept (compare DustDevils.lua:168)
				SMRFixPack.MeteorsBeatSet("long-sleep-done") -- FIX: heartbeat
				local chance = SessionRandom:Random(100)
				local meteors_type
				if chance < meteors.multispawn_chance then
					meteors_type = "multispawn"
				else
					meteors_type = "single"
				end
				local hit_time = Min(spawn_time, warning_time)
				Sleep(hit_time)
				SMRFixPack.MeteorsBeatSet("striking") -- FIX: heartbeat — set BEFORE the call so a stall inside MeteorsDisaster is identifiable
				MeteorsDisaster(meteors, meteors_type)
				SMRFixPack.MeteorsBeatSet("struck") -- FIX: heartbeat

				local new_meteors = GetMeteorsDescr()
				g_MeteorsGameDescr = new_meteors
				while not new_meteors do
					-- FIX: heartbeat + one loud line; a persistently nil descriptor
					-- FIX: (e.g. Atmosphere past the 80% threshold) is designed silence
					if SMRFixPack.MeteorsBeat and SMRFixPack.MeteorsBeat.phase ~= "descriptor-wait" then
						SMRFixPack.MeteorsNote("MeteorFrequency: meteor descriptor unavailable — rechecking daily (designed when terraforming passes MeteorStormStop)")
					end
					SMRFixPack.MeteorsBeatSet("descriptor-wait")
					Sleep(const.DayDuration)
					new_meteors = GetMeteorsDescr()
					g_MeteorsGameDescr = new_meteors
				end
				meteors = new_meteors
				SMRFixPack.MeteorsBeatSet("descriptor-reread") -- FIX: heartbeat
			end
		end
	end,
})

-- PT-01 watchdog: once per day, if the game is live, meteors are not legitimately
-- silent, and the thread has not written a heartbeat for longer than any legal wait,
-- log the pre-death state and restart the thread. Additive OnMsg handler; respects
-- the fix's own status (veto/inactive => never armed — the F75 lesson).
-- Detection threshold: max roll (spawntime + spawntime_random) + max warning
-- (SensorTowerPredictionMaxTime = 75h) + 1 sol margin. A healthy loop heartbeats at
-- least once per roll, so this cannot false-positive; detection latency ~6-8 sols.
-- Returns a string describing what it did/why it declined (probe-visible).
SMRFixPack.MeteorsWatchdog = SMRFixPack.MeteorsWatchdog or { restarts = 0 }

-- descr_override is a test hook (the TestKit probe drives the mechanism with a
-- synthetic descriptor); live callers pass nothing and get the full guard set.
function SMRFixPack.MeteorsWatchdogCheck(descr_override)
	local fix = SMRFixPack.fixes and SMRFixPack.fixes.MeteorFrequency
	if not fix or fix.status ~= "active" then return "fix not active" end
	local descr = descr_override
	if not descr then
		if not rawget(_G, "MainMap") or not MainMap then return "no map" end
		if IsGameRuleActive("NoDisasters") then return "NoDisasters rule" end
		descr = GetMeteorsDescr()
		if not descr or descr.forbidden then return "descriptor missing/forbidden (silence is designed)" end
	end

	local wd = SMRFixPack.MeteorsWatchdog
	local b = SMRFixPack.MeteorsBeat
	if not b then
		-- first sighting this session (e.g. save loaded before we ever beat):
		-- arm a full grace period instead of restarting blind
		SMRFixPack.MeteorsBeat = { t = GameTime(), phase = "watchdog-armed" }
		return "armed"
	end
	local max_wait = descr.spawntime + descr.spawntime_random
		+ const.SensorTowerPredictionMaxTime + const.DayDuration
	local silent = GameTime() - b.t
	if silent <= max_wait then return "healthy" end
	if wd.gave_up then return "gave up" end

	local thread = rawget(_G, "Meteors")
	local alive = IsValidThread(thread)
	log("MeteorFrequency: WATCHDOG — Meteors thread silent for %d game hours (last phase '%s', thread %s); restarting",
		silent / const.HourDuration, tostring(b.phase), alive and "ALIVE but stuck" or "DEAD")
	wd.restarts = wd.restarts + 1
	if wd.restarts > 3 then
		wd.gave_up = true
		log("MeteorFrequency: WATCHDOG — 3 restarts did not keep the thread alive; giving up for this session (please report this log)")
		return "gave up"
	end
	RestartGlobalGameTimeThread("Meteors")
	SMRFixPack.MeteorsBeat = { t = GameTime(), phase = "watchdog-restarted" }
	return "restarted"
end

function OnMsg.NewDay()
	SMRFixPack.MeteorsWatchdogCheck()
end

-- Loaded saves resume the persisted (buggy or stalled) thread; swap it for the fixed
-- body. The necropsy line tells us the state the save captured — for the PT-01 save
-- it answers dead-vs-stuck for the wedged thread directly.
function OnMsg.LoadGame()
	local fix = SMRFixPack.fixes.MeteorFrequency
	if fix and fix.status == "active" then
		local old = rawget(_G, "Meteors")
		log("MeteorFrequency: persisted Meteors thread on load was %s — restarting with the fixed body",
			IsValidThread(old) and "alive" or (old == false and "not created" or "DEAD"))
		RestartGlobalGameTimeThread("Meteors")
		SMRFixPack.MeteorsBeat = { t = GameTime(), phase = "restarted-on-load" }
		SMRFixPack.MeteorsWatchdog = { restarts = 0 }
	end
end
