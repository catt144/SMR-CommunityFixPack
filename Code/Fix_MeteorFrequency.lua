-- F02: Meteors strike roughly every 6 game-hours instead of every 35-115+ hours.
-- F86 Tier-1 REWRITE (2026-08-01, spec `docs/reports/SAVE_SAFETY_REDESIGN.md`
-- §6.2a-A): layer 3 — no mod-owned thread body. Also fixes F88 (the per-load
-- timer re-roll) via a one-shot version-latched heal.
--
-- Defect (Meteors.lua:277-283, game 1.0.7.396349): in the "Meteors" global
-- game-time thread the long wait between strikes was mangled into a dead `if`:
--     local start_time = GameTime()
--     if GameTime() - start_time > spawn_time - warning_time then Sleep(5000) end
-- The condition compares GameTime() against itself (0 > x is false in the normal
-- warning < spawn case), so the only real wait is Sleep(Min(spawn_time,
-- warning_time)) — and warning_time defaults to 6 game hours. Designed intervals
-- are 35-90h + 0-25h random. Perversely, Sensor Towers (which ADD warning time)
-- lengthen the interval, inverting their purpose.
--
-- Fix shape (layer 3, FIX_POLICY §3a — replaces the body copy shipped until
-- 2026-08-01; F86 is why body copies are banned where a route out exists): wrap
-- the SYNCHRONOUS input `GetDisasterWarningTime` (MapSettings.lua:94-98), keyed
-- to the Meteors thread itself —
--     CurrentThread() == rawget(_G, "Meteors")  and a descriptor present
--       ->  return Max(orig(descr), descr.spawntime + descr.spawntime_random)
-- With warning_time >= every possible spawn roll, vanilla's own
-- `Min(spawn_time, warning_time)` (Meteors.lua:291-292) equals spawn_time and
-- VANILLA'S OWN BODY produces the designed 35-115h schedule. The MeteorStorm
-- thread passes the SAME descriptor (Meteors.lua:327), so the CurrentThread()
-- key is what keeps storm warning timing untouched — a descriptor key would be
-- a barred balance change. The defer-when-falsy branch (global `Meteors` falsy
-- -> orig path) is defence in depth, NOT load-bearing: GT creation DEFERS, and
-- `RestartGlobalGameTimeThread` assigns `_G.Meteors` before the persisted
-- body's first call (measured 2026-08-01, ENGINE_FACTS; _fixup.lua:21).
--
-- Disclosed residuals (accepted, spec §6.2a-A):
--   * with warning_time > spawn_time the dead `if`'s condition (0 > negative)
--     goes TRUE, so each cycle gains Sleep(5000) ≈ 10 game minutes —
--     negligible against 35-115h intervals;
--   * the SMRFixPack_MeteorLatch GameVar stays in the save after uninstall as
--     inert data (prior art: GromGor's `MeteorsFixed` GameVar, C31).
--
-- F88 (filed 2026-07-31): the pre-rewrite OnMsg.LoadGame restarted the thread
-- on EVERY load, re-rolling the 35-115h timer — a player who never played out a
-- full interval between loads never saw a meteor, indefinitely and silently.
-- Now a ONE-SHOT LATCHED HEAL (owner decision, F86_EXECUTION_PLAN §7 #2):
-- `SMRFixPack_MeteorLatch` holds the last-healed pack version; on PostLoadGame
-- with the fix active and latch ~= current version, restart the thread ONCE
-- (onto vanilla's body) and stamp the latch. Never restart on an ordinary load
-- — vanilla's PersistPostLoad resumes the persisted thread with its remaining
-- sleep intact (_fixup.lua:50-56), which IS the fix for F88. The one restart
-- per save lineage per version clears persisted old bodies out of existing
-- saves (vanilla-broken, our shipped 2026-07-25 copy, or PT-01-wedged dead
-- threads) at the cost of one timer re-roll, and a pack-version bump re-heals
-- once (the SAVE_SAFETY_REDESIGN §2.5 upgrade path).
--
-- PT-01 (2026-07-25/26 — permanent silence after 5 good strikes): root cause
-- pinned 2026-07-29 to F78 (wedged storm held the scheduler) + F81 (stranded
-- prediction flag gated all weather); those fixes own it. The daily watchdog
-- stays as cheap insurance, with its liveness input moved off the deleted
-- heartbeat surface: an additive OnMsg.MeteorDone timestamp (Meteors.lua:388 —
-- every resolved meteor posts it; a storm meteor stamping it merely delays
-- detection by one threshold window). Threshold unchanged (max roll + max
-- warning + 1 sol — a healthy loop cannot go that long without a strike, so no
-- false positives), 3-restart give-up ladder, designed-silence guards
-- (NoDisasters, missing/forbidden descriptor), and the restart recreates
-- VANILLA's body. First sighting after a load arms a full grace period instead
-- of restarting blind.
--
-- §3a COMPLIANCE, stated: no mod-owned thread body exists in this module; the
-- wrapper is synchronous and never enters a save; watchdog and heal are
-- additive OnMsg handlers that do not yield.
-- SAVE FOOTPRINT (FIX_POLICY §3): one new GameVar, `SMRFixPack_MeteorLatch`
-- (false | version string) — inert data to a save loaded without the mod.

local FIX_ID = "MeteorFrequency"

local log = SMRFixPack.Log

GameVar("SMRFixPack_MeteorLatch", false)

SMRFixPack.Register(FIX_ID, {
	title = "Meteors strike on their designed 35-115h schedule instead of ~every 6 hours",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "GetDisasterWarningTime" },
			{ path = { "GlobalGameTimeThreadFuncs", "Meteors" }, kind = "function",
			  reason = "Meteors thread function not found (game update changed it?)" },
			{ global = "RestartGlobalGameTimeThread" },
		})
		if err then return err end

		local orig = rawget(_G, "GetDisasterWarningTime")
		local function warning_wrapper(disaster, ...)
			-- keyed path: only the Meteors thread's own roll is stretched; a
			-- descriptor without spawn fields (not vanilla's) takes the orig path
			if disaster and disaster.spawntime and disaster.spawntime_random then
				local meteors_thread = rawget(_G, "Meteors")
				if meteors_thread and CurrentThread() == meteors_thread then
					return Max(orig(disaster), disaster.spawntime + disaster.spawntime_random)
				end
			end
			return orig(disaster, ...)
		end
		return SMRFixPack.SetGlobal("GetDisasterWarningTime", warning_wrapper,
			"could not install the GetDisasterWarningTime wrapper")
	end,
})

-- PT-01 watchdog (see header). State is session-local (never persisted) and
-- reset per save below — GameTime differs between saves, so a stale timestamp
-- would either mask a wedge or trigger a false restart.
SMRFixPack.MeteorsWatchdog = SMRFixPack.MeteorsWatchdog or { restarts = 0 }

OnMsg.MeteorDone = SMRFixPack.WhenActive(FIX_ID, function()
	SMRFixPack.MeteorsWatchdog.last_seen = GameTime()
end)

-- descr_override is a test hook (the TestKit probe drives the mechanism with a
-- synthetic descriptor); live callers pass nothing and get the full guard set.
-- Returns a string describing what it did/why it declined (probe-visible).
function SMRFixPack.MeteorsWatchdogCheck(descr_override)
	local fix = SMRFixPack.fixes and SMRFixPack.fixes[FIX_ID]
	if not fix or fix.status ~= "active" then return "fix not active" end
	local descr = descr_override
	if not descr then
		if not rawget(_G, "MainMap") or not MainMap then return "no map" end
		if IsGameRuleActive("NoDisasters") then return "NoDisasters rule" end
		descr = GetMeteorsDescr()
		if not descr or descr.forbidden then return "descriptor missing/forbidden (silence is designed)" end
	end

	local wd = SMRFixPack.MeteorsWatchdog
	if not wd.last_seen then
		-- first sighting this session/save (e.g. save loaded before any strike):
		-- arm a full grace period instead of restarting blind
		wd.last_seen = GameTime()
		return "armed"
	end
	local max_wait = descr.spawntime + descr.spawntime_random
		+ const.SensorTowerPredictionMaxTime + const.DayDuration
	local silent = GameTime() - wd.last_seen
	if silent <= max_wait then return "healthy" end
	if wd.gave_up then return "gave up" end

	local thread = rawget(_G, "Meteors")
	local alive = IsValidThread(thread)
	log("%s: WATCHDOG — no meteor resolved for %d game hours (thread %s); restarting onto vanilla's body",
		FIX_ID, silent / const.HourDuration, alive and "ALIVE but stuck" or "DEAD")
	wd.restarts = wd.restarts + 1
	if wd.restarts > 3 then
		wd.gave_up = true
		log("%s: WATCHDOG — 3 restarts did not keep the thread alive; giving up for this session (please report this log)", FIX_ID)
		return "gave up"
	end
	RestartGlobalGameTimeThread("Meteors")
	wd.last_seen = GameTime()
	return "restarted"
end

function OnMsg.NewDay()
	SMRFixPack.MeteorsWatchdogCheck()
end

-- The one-shot latched heal (F88's fix; see header). The unconditional
-- watchdog reset rides the same handler, BEFORE the active gate — stale
-- session state must never survive into a different save's timeline.
function OnMsg.PostLoadGame()
	SMRFixPack.MeteorsWatchdog = { restarts = 0 }
	local fix = SMRFixPack.fixes[FIX_ID]
	if not (fix and fix.status == "active") then return end
	local disabled = rawget(_G, "SMRFixPack_Disabled")
	if type(disabled) == "table" and disabled[FIX_ID] then return end
	local ok, err = pcall(function()
		local version = SMRFixPack.PackVersion()
		if not version then
			log("%s: pack version unreadable — skipping the one-shot heal (an unkeyed restart is F88's defect)", FIX_ID)
			return
		end
		if rawget(_G, "SMRFixPack_MeteorLatch") == version then
			return -- already healed under this version: NEVER restart again (F88)
		end
		local old = rawget(_G, "Meteors")
		log("%s: one-shot heal — persisted Meteors thread was %s; restarting onto vanilla's body (latch %s -> %s)",
			FIX_ID, IsValidThread(old) and "alive" or (old == false and "not created" or "DEAD"),
			tostring(rawget(_G, "SMRFixPack_MeteorLatch")), version)
		RestartGlobalGameTimeThread("Meteors")
		SMRFixPack_MeteorLatch = version
	end)
	if not ok then log("%s: latched heal failed: %s", FIX_ID, tostring(err)) end
end
