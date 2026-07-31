-- F78: a meteor storm wedges forever in its drain loop; that colony never gets
-- another storm — and, until Fix_DisasterPredictionLeak's sweep runs, no weather.
--
-- Defect (Meteors.lua:238-241, game 1.0.7.396349; reproduced live 2026-07-29):
--     while not g_MeteorStormStop and #spawned > 0 do
--         WaitMsg("MeteorDone", delta)
--         table.validate(spawned)
--     end
-- The loop is unbounded. In the live repro 73 spawned descriptors drained to 2
-- and those two never became invalid (cause unknown — fall thread death, MDS
-- interception and off-map impacts are the candidates), so the loop spun on its
-- 3s tick forever. The storm's scheduler (the "MeteorStorm" named global thread,
-- Meteors.lua:307-359) called MeteorsDisaster inline at :346 and never got
-- control back — no future storm can ever be scheduled. Two storms were observed
-- wedged SIMULTANEOUSLY, and g_MeteorStormStop is a shared GameVar that the
-- first waking thread consumes (:242), so any release must be pulsed, not set
-- once. Both g_MeteorStorm and g_MeteorStormStop are GameVars (Meteors.lua:38-39)
-- and the scheduler thread is a persisted named global (PersistableGlobals via
-- GlobalGameTimeThread, Config\_fixup.lua:9-16) — a wedged storm follows the
-- save around forever.
--
-- Fix (FIX_POLICY §1 rank 3 — registry/thread surgery via vanilla primitives; no
-- body copy): an hourly WATCHDOG (F02 precedent) detects the wedge signature —
--     g_MeteorStorm set  AND  no DisasterMeteorStorm notification  AND
--     no meteor still falling  —  sustained for a full game hour.
-- A healthy storm never matches: its duration notification is up from before the
-- first spawn (Meteors.lua:179) to its expiration at the storm's designed end,
-- and the drain after the last strike completes in seconds (meteor flight is
-- travel_dist/speed ≈ 6-7s). The falling-meteor liveness test is vanilla's own
-- (SavegameFixups.MeteorCleanFXLeftovers, Meteors.lua:1182-1193).
--
-- The heal, in order:
--   1. RestartGlobalGameTimeThread("MeteorStorm") — kills the wedged scheduler
--      thread (the owner of every natural storm) and recreates it on the current
--      body, so future storms resume. This is the mechanism vanilla itself uses
--      to move named threads onto new code (Config\_fixup.lua:18-22, and the
--      pack's own F02 LoadGame restart).
--   2. a guarded g_MeteorStormStop pulse for storms that are NOT the scheduler
--      (console- or sequence-spawned) — re-checking each pulse so a new healthy
--      storm (whose notification is up immediately) is never interrupted. The
--      pulse was the proven live recovery on 2026-07-29.
--   3. if nothing released, force the state clean: reset the two GameVars, clear
--      the stranded prediction flag, and DoneObject stray non-falling meteors
--      (mirroring the vanilla leftover fixup). A released thread instead runs
--      the vanilla tail itself — DoneObject sweep + Msg("MeteorStormEnded"),
--      which Fix_DisasterPredictionLeak's handler turns into the flag clear.
--
-- Residual risk, accepted and bounded: a save made during the ~40s pulse window
-- can persist g_MeteorStormStop = true; the next storm in that save aborts once,
-- cleanly (the stop branch removes its notification, Meteors.lua:227). Three
-- heals per session, then the watchdog gives up loudly (F02 pattern).

local FIX_ID = "MeteorStormWedge"

local log = SMRFixPack.Log

-- The heal thread body reaches the logger through the real global SMRFixPack
-- (zero-upvalue discipline, F02 precedent).
SMRFixPack.StormWedgeNote = log
SMRFixPack.StormWedge = SMRFixPack.StormWedge or { restarts = 0 }

SMRFixPack.Register(FIX_ID, {
	title = "A wedged meteor storm is detected and released instead of blocking storms forever",
	apply = function()
		return SMRFixPack.Require(FIX_ID, {
			{ path = { "GlobalGameTimeThreadFuncs", "MeteorStorm" }, kind = "function",
			  reason = "MeteorStorm thread function not found (game update changed it?)" },
			{ global = "RestartGlobalGameTimeThread" },
			{ global = "FindNotification" },
			{ global = "MeteorsDisaster" },
		})
	end,
})

-- The watchdog predicate. Returns a probe-visible string describing what it saw.
-- opts.dry = true evaluates the full predicate but does not start the heal
-- (the TestKit drives the mechanism this way).
function SMRFixPack.StormWedgeCheck(opts)
	local fix = SMRFixPack.fixes[FIX_ID]
	if not (fix and fix.status == "active") then return "fix not active" end
	if not rawget(_G, "MainMap") or not MainMap then return "no map" end
	local wd = SMRFixPack.StormWedge
	if wd.healing then return "heal in progress" end
	if not rawget(_G, "g_MeteorStorm") then
		wd.first_seen = nil
		return "no storm flagged"
	end
	if FindNotification("DisasterMeteorStorm") then
		wd.first_seen = nil
		return "storm notification live (healthy)"
	end
	local falling = MainMap:MapCount(true, "BaseMeteor", function(m)
		return m.fall_thread and IsValidThread(m.fall_thread)
	end)
	if falling > 0 then
		wd.first_seen = nil
		return "meteors still falling (draining normally)"
	end
	-- wedge signature present; require it to persist a full hour before acting
	local now = GameTime()
	wd.first_seen = wd.first_seen or now
	if now - wd.first_seen < const.HourDuration then
		return "signature armed - confirming"
	end
	if wd.gave_up then return "gave up" end
	if opts and opts.dry then return "would heal (dry)" end

	wd.restarts = wd.restarts + 1
	if wd.restarts > 3 then
		wd.gave_up = true
		log("%s: WATCHDOG - 3 heals did not keep storms healthy; giving up for this session (please report this log)", FIX_ID)
		return "gave up"
	end
	local sched = rawget(_G, "MeteorStorm")
	log("%s: WEDGE confirmed - g_MeteorStorm set for 1h+ with no notification and nothing falling (scheduler thread %s); healing",
		FIX_ID, IsValidThread(sched) and "alive but stuck" or tostring(sched))
	wd.first_seen = nil
	wd.healing = true
	CreateGameTimeThread(SMRFixPack.StormWedgeHeal)
	return "healing"
end

-- The heal itself. A global function (persist-safe by name) with only global
-- lookups plus locals; the thread it runs on is a mod game-time thread and is
-- not persisted (F06/F77 precedent) — an interrupted heal simply re-arms after
-- the next load (state reset below).
function SMRFixPack.StormWedgeHeal()
	RestartGlobalGameTimeThread("MeteorStorm")
	SMRFixPack.StormWedgeNote("MeteorStormWedge: scheduler thread restarted - future storms will schedule again")

	-- release non-scheduler storms; each pulse re-checks so a NEW healthy storm
	-- is never interrupted
	for i = 1, 10 do
		if not g_MeteorStorm then break end
		if FindNotification("DisasterMeteorStorm") then break end
		g_MeteorStormStop = true
		Sleep(4000)
	end

	if g_MeteorStorm and not FindNotification("DisasterMeteorStorm") then
		-- nothing released (the wedged thread was already dead): force clean
		g_MeteorStorm = false
		local flags = rawget(_G, "g_DisastersPredicted")
		if type(flags) == "table" then flags.DisasterMeteorStorm = nil end
		local removed = 0
		MainMap:MapForEach(true, "BaseMeteor", function(m)
			if not (m.fall_thread and IsValidThread(m.fall_thread)) then
				DoneObject(m)
				removed = removed + 1
			end
		end)
		SMRFixPack.StormWedgeNote("MeteorStormWedge: forced storm state clean (%d stray meteor object(s) removed)", removed)
	else
		SMRFixPack.StormWedgeNote("MeteorStormWedge: wedged storm released through the vanilla end path")
		-- FIX (audit 2026-07-29, B2): the vanilla end path clears the prediction
		-- flag only via Fix_DisasterPredictionLeak's MeteorStormEnded handler —
		-- with that fix individually disabled, a released storm stranded
		-- g_DisastersPredicted.DisasterMeteorStorm (the exact leak it exists to
		-- fix). Clear the flag here too if it is still set and no live storm
		-- notification is behind it; idempotent beside F81 (both nil the same
		-- entry, and a new storm's AddDisasterNotification re-sets it).
		local flags = rawget(_G, "g_DisastersPredicted")
		if type(flags) == "table" and flags.DisasterMeteorStorm
				and not FindNotification("DisasterMeteorStorm") then
			flags.DisasterMeteorStorm = nil
			SMRFixPack.StormWedgeNote("MeteorStormWedge: cleared the stranded meteor prediction flag itself (DisasterPredictionLeak handler not active)")
		end
	end
	g_MeteorStormStop = false -- never leave a stray stop signal for the next storm
	SMRFixPack.StormWedge.healing = false
end

function OnMsg.NewHour()
	SMRFixPack.StormWedgeCheck()
end

-- Loads kill mod threads (an in-flight heal dies) and GameTime differs between
-- saves (a stale first_seen would trigger instantly), so the watchdog state is
-- per-save — the F02 LoadGame reset pattern, on PostLoadGame for consistency
-- with this family's other passes.
function OnMsg.PostLoadGame()
	SMRFixPack.StormWedge = { restarts = 0 }
end
