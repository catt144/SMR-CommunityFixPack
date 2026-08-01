-- F81: a stranded disaster-prediction flag silently gates the whole weather system.
--
-- Defect (game 1.0.7.396349; shipped Lua verified byte-identical to Src, QA
-- session 2026-07-29): AddDisasterNotification sets
-- g_DisastersPredicted[base_id] = true for EVERY disaster notification
-- (MapSettings.lua:169) and only RemoveDisasterNotifications clears it (:176).
-- The meteor STORM duration notification (Meteors.lua:179) is the one
-- notification in the game with no removal on its normal completion path: the
-- storm's end (Meteors.lua:242-251) plays FX, sends MeteorStormEnded and clears
-- g_MeteorStorm — and leaves the flag set forever. The notification's own
-- Expiration removes the UI entry through RemoveNotification
-- (CommonLua\Libs\Notifications\Notifications.lua:194-199), which never touches
-- the flag — which is exactly the flag-true-with-nothing-on-screen state found
-- live. Every other disaster removes its notifications on every path
-- (ColdWave.lua:148,:174; DustStorm.lua:163,:180;
-- TerraformingDisasters.lua:261,:300-302) — grep-exhaustive.
--
-- A stuck flag makes IsDisasterPredicted() (MapSettings.lua:189) true forever:
--   * the rains loop deadlocks on its next roll (Fix_RainsDeadlock, same family);
--   * dust storms and cold waves defer forever (DustStorm.lua:439-446,:464-465;
--     ColdWave.lua:208-215,:228-229);
--   * the three POI reward sequences that call WaitCurrentDisaster() block
--     (Data\POI.lua:79,:166,:381 — includes the terraforming import events);
--   * the Inner Light mystery's dream cycle stalls (Mysteries\Dream.lua:26).
-- PROVEN LIVE 2026-07-29: clearing the flag on a 194-sol save that had never
-- once seen weather started rain within seconds.
--
-- Fix, two halves (FIX_POLICY §1 rank 2 + §3 one-shot sweep — no body copy):
--   1. an additive OnMsg.MeteorStormEnded handler removes the storm's
--      notification (and with it the flag) whenever a storm ends — the same
--      thing cold waves and dust storms already do on their own end paths;
--   2. a PostLoadGame reconciliation clears any g_DisastersPredicted entry with
--      NO live notification behind it. That state is stranded by construction:
--      every disaster notification preset is Dismissable = false
--      (Data\NotificationPreset.lua:863-921), so a player cannot legitimately
--      produce flag-without-notification. The sweep touches only the flag
--      table, never a notification — a genuine warning can never lose its
--      on-screen countdown to this pass.
-- PostLoadGame rather than LoadGame: it must run after the shipped
-- SavegameFixups, which can re-open dust/cold notifications on legacy saves
-- (UnpersistGame ordering, CommonLua\Savegame.lua:810-813 — the same reasoning
-- as 90_SaveSanitizer's handler).
--
-- Known degenerate case, accepted: with two CONCURRENT storms (possible via
-- cheats/sequences; vanilla already trades the single notification slot between
-- them via ReplaceNotification) the first storm to end clears the shared slot
-- early. The alternative is the permanent leak.
--
-- MID-SESSION RECONCILE (added 2026-08-01, F86 Tier-1 rider — spec
-- `SAVE_SAFETY_REDESIGN.md` §6.2a-C, pre-cleared option TAKEN): the same sweep
-- also runs on OnMsg.NewDay. The sweep's predicate — flag set with no live
-- notification — is stranded by construction at ANY time, not just at load
-- (every disaster notification preset is Dismissable = false, and flag and
-- notification are set/cleared in the same synchronous bodies, so cooperative
-- scheduling leaves no observable mid-function window; the PostLoadGame-only
-- placement of the shipped sweep was about SavegameFixups ordering, not
-- mid-session safety). Cost: one flag-table scan per sol. Benefit: an
-- F81a-class stranding (e.g. the wedge-heal's force-clean path with this fix
-- disabled, or any future leak) gates weather for at most one sol instead of
-- the rest of the session. §3a-compliant: OnMsg-based, additive, synchronous.

local FIX_ID = "DisasterPredictionLeak"

local log = SMRFixPack.Log

SMRFixPack.Register(FIX_ID, {
	title = "A finished meteor storm no longer disables rains, cold waves and dust storms forever",
	apply = function()
		return SMRFixPack.Require(FIX_ID, {
			{ global = "RemoveDisasterNotifications" },
			{ global = "AddDisasterNotification" },
			{ global = "FindNotification" },
		})
	end,
})

-- Half 1 — stop the leak. Fires on BOTH end paths; the force-stop path already
-- removed the notification (Meteors.lua:227), and a double removal is a no-op
-- (RemoveNotification returns early, RemoveDisasterNotifications just nils the
-- flag again).
OnMsg.MeteorStormEnded = SMRFixPack.WhenActive(FIX_ID, function(map)
	local presets = rawget(_G, "NotificationPresets")
	if not (type(presets) == "table" and presets.DisasterMeteorStorm) then
		log("%s: NotificationPresets.DisasterMeteorStorm missing — leak handler skipped", FIX_ID)
		return
	end
	RemoveDisasterNotifications("DisasterMeteorStorm", map)
	log("%s: meteor storm ended — its notification and prediction flag are cleared", FIX_ID)
end)

-- Half 2 — heal saves already poisoned. Exposed for the console and the TestKit;
-- returns how many flags it cleared. Idempotent: a second run finds nothing.
function SMRFixPack.ReconcileDisasterPredictions()
	local flags = rawget(_G, "g_DisastersPredicted")
	if type(flags) ~= "table" then return 0 end
	local cleared = 0
	for id, v in pairs(flags) do
		if v and not FindNotification(id) then
			flags[id] = nil
			cleared = cleared + 1
			log("%s: cleared stranded prediction flag '%s' (no live notification behind it)",
				FIX_ID, tostring(id))
		end
	end
	return cleared
end

OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(SMRFixPack.ReconcileDisasterPredictions)
	if not ok then log("%s: reconciliation pass failed: %s", FIX_ID, tostring(err)) end
end)

-- The mid-session reconcile (see header): same sweep, same gates, once per sol.
OnMsg.NewDay = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(SMRFixPack.ReconcileDisasterPredictions)
	if not ok then log("%s: mid-session reconciliation failed: %s", FIX_ID, tostring(err)) end
end)
