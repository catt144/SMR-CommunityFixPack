-- F16: A finished Mirror Sphere site still accepts actions.
--
-- Defect: MirrorSphereBuildingBase:StartAction (Lua\Mysteries\MirrorSphere.lua:813-870)
-- guards against working an already-finished site with
--     if not self:IsActionEnabled(action) or self.progress == 100 then return end
-- but `progress` is not a percentage. It runs 0..max_progress, a file-local 2^22
-- (MirrorSphere.lua:16), which is why GetProgressPct has to divide
-- (:724-726) and SetProgress clamps to max_progress (:734). The site is finished
-- at 2^22, never at 100, so the guard can only fire on a one-in-four-million
-- coincidence on the way past.
--
-- Consequence: once the excavation is complete — the sphere has launched and the
-- update thread is deleted (:748-762) — the remaining actions are still offered.
-- "Pierce the Shell" in particular hands the site a work request and connects it
-- to the drone commanders, so players spend real drone time on a site that cannot
-- progress any further.
--
-- Patch approach: chained pre-wrapper on StartAction. The shipped body is long and
-- the wrapper only needs to answer the question the guard was asking. Cancelling a
-- running action (`self.action == action`) is deliberately still allowed through,
-- since that branch of the shipped body is a StopAction and has nothing to do with
-- progress.
--
-- The limit is read from MirrorSphere.max_progress (:69) — the flying sphere class
-- publishes the same file-local constant the building compares against, and that
-- is the only handle Lua has on it. If it ever stops being published the fix
-- deactivates rather than guessing.

SMRFixPack.Register("MirrorSphereSite", {
	title = "A completed Mirror Sphere site no longer accepts more drone work",
	apply = function()
		local err = SMRFixPack.Require("MirrorSphereSite", {
			{ class = "MirrorSphereBuildingBase", method = "StartAction" },
			-- content check: the published constant must still be the >100 scale
			-- the shipped guard mis-compared against
			{ test = function()
				local S = rawget(_G, "MirrorSphere")
				local mp = type(S) == "table" and S.max_progress or nil
				return type(mp) == "number" and mp > 100
			  end,
			  reason = "MirrorSphere.max_progress not found (game update changed it?)" },
		})
		if err then return err end
		local B = MirrorSphereBuildingBase
		local max_progress = MirrorSphere.max_progress

		local orig = B.StartAction
		function B:StartAction(action, ...)
			-- FIX (F16): the shipped guard compared progress against 100 on a
			-- 0..max_progress scale, so a finished site never locked out.
			if self.action ~= action and (self.progress or 0) >= max_progress then
				return
			end
			return orig(self, action, ...)
		end
	end,
})
