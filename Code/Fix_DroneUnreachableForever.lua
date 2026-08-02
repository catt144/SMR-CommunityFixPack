-- F55 (drone half): once a drone fails to approach a building, it writes that
-- building off forever.
-- F86 Tier-2 REWRITE (2026-08-01, spec `docs/reports/SAVE_SAFETY_REDESIGN.md`
-- §6.2 Tier 2): layer 3 — patch the CONSUMER, keep vanilla's blocking body.
--
-- Defect: Drone:ApproachWrapper (Lua\Units\Drone.lua:819-849) records a failed
-- approach as
--     unreachable_buildings[building] = GameTime() + max_int
-- with the comment "mark it so it is basically unreachable forever". But the game
-- also ships an expiry mechanism for exactly this table: Drone:CleanUnreachables
-- (:879-896) drops entries once `GameTime() - ts >= const.UnreachablesCleanupDeltaT`
-- (5 sols, :868). A timestamp max_int in the future makes that difference hugely
-- negative, so the entry never expires. The only escape is a passability change
-- bumping g_DroneUnreachablesVersion — and after any such change the drone simply
-- re-fails and re-marks it forever. A dome that was briefly unreachable (opened
-- roof, a blocked entrance, a construction site in the way) is dropped by that
-- drone permanently, which is the "late-game drones stop maintaining buildings
-- and cluster outside" report.
--
-- Fix shape (layer 3, FIX_POLICY §3a — replaces the ApproachWrapper body copy
-- shipped until 2026-08-01). The defect is only the VALUE of the timestamp, and
-- the reader of that value is `Drone:CleanUnreachables`, which is
-- **VERIFIED SYNCHRONOUS** — its whole body is a `pairs` walk over a plain table
-- plus `GameTime()` (Drone.lua:879-896), and `tools/blocking_analysis.py` reports
-- it `clear` (no direct yield, no unambiguous blocking callee). So a PRE-wrapper
-- there normalises the poisoned stamps and hands over to vanilla:
--     ts > GameTime()  ->  ts - max_int      (the actual failure time)
-- `max_int` is the exact constant vanilla added (CommonLua\Core\lib.lua:69), so
-- the subtraction RECOVERS the original GameTime() rather than approximating it,
-- and vanilla's own 5-sol expiry then does what it was written to do. The
-- normalisation is one-way: a stamp already in the past is never touched, so
-- entries written by the pre-2026-08-01 shipped fix (a plain GameTime()) and
-- entries already normalised are both left exactly as they are.
--
-- Nothing else changes. The table, its `version` key, the 64-entry cap, the
-- eviction of the oldest entry and the version-based reset are vanilla's and are
-- untouched — including ApproachWrapper itself, which keeps writing vanilla's
-- value. (One consequence worth naming: between a failed approach and the next
-- CleanUnreachables call the table can hold a mix of raw and normalised stamps,
-- and the cap's "kick oldest" would evict a normalised entry first. That window
-- is one Idle cycle (Drone.lua:640, ~2s), the ordering it produces is still
-- oldest-failure-first, and the shipped fix had the same property with every
-- stamp normalised.)
--
-- Scope note: BUGS.md F55 also describes open-air domes losing their Dome_Entrance
-- attaches (and with them the only drone routes inside). That half is NOT patched
-- here — Dome_Entrance is an auto-attach of the dome entity, recreated by
-- AutoAttachObjects in Building:RebuildAttaches (Building.lua:2409-2429), not one
-- of the configurable attaches that Dome:CalcOpenAirSkin empties
-- (OpenAirBuilding.lua:216-237). Whether the *_Open entity carries the entrance
-- spot is engine data that Lua cannot inspect, so there is nothing to repair from
-- here. See the F55 entry for the finding.
--
-- §3a COMPLIANCE, stated: the module owns no thread and no longer replaces any
-- blocking body. Its only code is a wrapper on the verified-synchronous
-- `Drone:CleanUnreachables`; that frame can never be on the stack while a thread
-- is blocked, so it cannot be serialised by route (a). It is held only by the
-- `Drone` class table (safe by construction) and stores no function value
-- anywhere, so routes (b) and (c) are closed too.
-- SAVE FOOTPRINT (FIX_POLICY §3): none. No GameVar, no new object field.

SMRFixPack.Register("DroneUnreachableForever", {
	title = "Drones re-try buildings they once failed to reach instead of writing them off forever",
	apply = function()
		local err = SMRFixPack.Require("DroneUnreachableForever", {
			{ class = "Drone", method = "CleanUnreachables",
			  reason = "the unreachables expiry mechanism is gone (game update changed it?)" },
			{ path = { "const", "UnreachablesCleanupDeltaT" },
			  reason = "the unreachables expiry mechanism is gone (game update changed it?)" },
			-- the writer we deliberately leave alone: if it is gone, the poisoned
			-- value it produces is gone too and this wrapper has nothing to repair
			{ class = "Drone", method = "ApproachWrapper" },
			{ global = "max_int", kind = "number",
			  reason = "max_int not found (game update changed it?)" },
		})
		if err then return err end
		local D = Drone
		local orig_clean = D.CleanUnreachables

		function D:CleanUnreachables(...)
			-- FIX (F55): vanilla stamps a failed approach GameTime() + max_int, which
			-- puts the entry permanently beyond its own 5-sol expiry test below.
			-- Subtracting the same constant restores the real failure time.
			local t = self.unreachable_buildings
			if t then
				local now = GameTime()
				for id, ts in pairs(t) do
					if id ~= "version" and type(ts) == "number" and ts > now then
						t[id] = ts - max_int
					end
				end
			end
			return orig_clean(self, ...)
		end
	end,
})
