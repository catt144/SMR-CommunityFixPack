-- C86: an Advanced Orbital Probe without Adapted Probes can knock an already
-- deep-scanned neighbouring sector back to "scanned".
--
-- OrbitalProbe:ScanSector chooses "scanned" without Adapted Probes and sends it
-- to every sector in the Advanced probe's five-sector pattern without filtering
-- their current status (Lua/OrbitalProbe.lua:72-100, :161-176). MapSector:Scan
-- returns only for "unexplored" or an equal status, then assigns the requested
-- status directly (Lua/Exploration.lua:229-232, :273-275). A deep-scanned
-- neighbour therefore loses its status and invites a pointless repeat scan.
--
-- Patch approach: chained pre-wrapper. The shipped status schema is monotonic:
-- unexplored -> scanned -> deep scanned. Requests below the exact shipped
-- MapSector object's current rank return through vanilla's own no-op seam;
-- every equal, upward, unknown or foreign-object call delegates unchanged.
--
-- Caller audit (1.1.0.403908): the saved RevealedMapSector load path admits only
-- unexplored -> saved status or scanned -> deep scanned (Exploration.lua:36-45);
-- the queue uses CanBeScanned, which rejects deep-scanned sectors (:154-172),
-- and requests only scanned/deep (:821-856); InitialExplore and the tutorial
-- calls operate during initial/tutorial setup (:1038-1055; TutorialStep.lua
-- :980-990; TutorialsNew.lua:861-864); asteroid MapSectorsReady scans a new map
-- (:1266-1275); Crystals requests deep scanned (:558-566). CheatMapExplore's
-- "Scan Map" route requests scanned for every sector (Cheats.lua:5-24;
-- CheatDef.lua:529-537); preserving an already deeper sector matches that
-- command's additive label and loses no cheat capability. The Advanced probe is
-- the only player route that requests a lower status.
--
-- FIX_POLICY §3a: layer 2. All pack work happens before `return orig(...)`;
-- nothing of ours can execute after a blocking call. No thread, persisted field,
-- or function value is created. SAVE FOOTPRINT: none.
--
-- BRANCH GUARD (FIX_POLICY §2a): MapSector:Scan is byte-identical in behaviour
-- on the two supported trees, so the wrapper carries no branch-specific body.
-- A behaviour probe cannot safely drive the defective branch: the shipped body
-- removes queue state, reveals deposits and may create a notification thread.
-- The fail-closed shape test instead requires the declaring class's exact
-- "unexplored" default, the root of the shipped three-state schema; bodycheck's
-- pin separately detects any edit to the target body.
--
-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-11 against shipped game 1.1.0.403908.
-- SRC: Lua/Exploration.lua MapSector:Scan sha256=996a9ebae835af19ad50734485f841519c33b6bee351b71e8ba8424d4ce92655
--   (Lua/Exploration.lua:229-286 at pin time)
-- DEFECT: self\.status = status
--   a lower requested status overwrites a higher completed scan status

local FIX_ID = "ScanDowngrade"
local rank = {
	["unexplored"] = 0,
	["scanned"] = 1,
	["deep scanned"] = 2,
}

SMRFixPack.Register(FIX_ID, {
	title = "Orbital probes do not downgrade already deep-scanned sectors",
	apply = function()
		local S = MapSector
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "MapSector", method = "Scan" },
			{ test = function()
				return rawget(MapSector, "status") == "unexplored"
			end,
			reason = "MapSector's scan-status schema changed (expected an unexplored default)" },
		})
		if err then return err end

		local orig = S.Scan
		function S:Scan(status, ...)
			-- Exact shipped class first: leave any foreign sector subclass untouched.
			if self.class ~= "MapSector" then
				return orig(self, status, ...)
			end
			local current, requested = rank[self.status], rank[status]
			if current and requested and requested < current then
				return
			end
			return orig(self, status, ...)
		end
	end,
})
