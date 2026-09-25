-- C115: a passage interrupt can book an own-home pickup before traversal ends.
-- At Transport start the colonist may already stand inside that home dome.
-- Only then discard an uncommitted rescue; every other ride enters native Transport.
--
-- Archived 1.1.1.405907: ColonistTransport.lua:461-474 books the rescue;
-- LRTransport.lua:106-123 records the pickup and registers the task;
-- Colonist.lua:3963-4013 walks to that pickup without rechecking home;
-- LRTransport.lua:63-84 removes a task from its manager and colonist.
-- Dome.lua:159-165 uses the position when unit.holder is absent.
--
-- Save/removal (§3a): layer 2. The bypass is synchronous and stores no state.
-- All other calls tail-delegate before any yield. A save during native Transport
-- may retain an inert wrapper frame; after removal native Transport finishes.
-- Cancellation during native Transport keeps its WaitTransport destructor.
--
-- MANIFEST (FIX_POLICY §2b), archived game build 1.1.1.405907.
-- SRC: Lua/Units/Colonist.lua Colonist:Transport sha256=c3e31e09337e6f82a6b792b678e70eee89d43bc4450c4d8a73035153547d3d6e
-- DEFECT: local\s+pickup_pos\s*=\s*self:GetMap\(\):GetPassablePointNearby\(self\.transport_task\.source_landing_site\[1\],\s*self\.pfclass\)

SMRFixPack.Register("ObsoleteHomeRescue", {
	title = "Stop an obsolete own-home shuttle pickup",
	apply = function()
		local err = SMRFixPack.Require("ObsoleteHomeRescue", {
			{ class = "Colonist", method = "Transport" },
			{ class = "ColonistTransportTask", method = "Cleanup" },
			{ global = "IsKindOf" },
			{ global = "IsValid" },
			{ global = "IsUnitInDome" },
			{ test = function()
				local task = rawget(_G, "ColonistTransportTask")
				return task and task.source_dome == false and task.migration_dest == false
					and task.shuttle == false and task.departure_rocket == false
			end, reason = "colonist transport task defaults changed" },
		})
		if err then return err end

		local orig = Colonist.Transport
		function Colonist:Transport(dest_dome, ...)
			if not IsKindOf(self, "Colonist") then return orig(self, dest_dome, ...) end
			local task = self.transport_task
			if task and IsValid(dest_dome) and task.colonist == self
				and task.dest_dome == dest_dome
				and dest_dome == self.dome and not task.source_dome
				and not task.migration_dest and not task.departure_rocket
				and not task.shuttle and not self.emigration_dome
				and (task.state == "new" or task.state == "almost_ready_for_pickup"
					or task.state == "ready_for_pickup")
				and not self.holder and IsUnitInDome(self) == dest_dome then
				task:Cleanup()
				-- Native Transport returns at once with no task (Colonist.lua:3964);
				-- delegating keeps any earlier wrapper in the chain (FIX_POLICY 1.4).
				return orig(self, dest_dome, ...)
			end
			return orig(self, dest_dome, ...)
		end
	end,
})
