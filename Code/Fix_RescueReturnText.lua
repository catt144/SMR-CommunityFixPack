-- C111: a shuttle rescue back to a colonist's own dome is labelled as a move
-- to a new dome. Keep the native destination link and all real relocations.
--
-- Archived 1.1.1.405907: ColonistTransport.lua:446-471 creates or reuses a
-- transport task to home and selects Transport. Colonist.lua:4629-4649 gives
-- Transport, TransportByFoot and MigrateStep the same "new Dome" command text;
-- :4672-4716 returns it. The link's getter and selector are :4437-4439 and
-- :4462-4465. LRTransport.lua:96 and Colonist.lua:3966 identify the rescue
-- task by absent source_dome and migration_dest. We change only the synchronous
-- command-text result. The task,
-- destination, command and hyperlink methods remain native.
-- Colonist.lua:106,329 uses false for an unset emigration_dome; a missing
-- instance value inherits that class default. Treat false and nil alike.
--
-- Save/removal: layer 3, a synchronous UI getter wrapper with no persisted
-- field, function or game-time thread. A reload reads the current task and dome
-- again; removal restores vanilla wording without saved residue.
--
-- MANIFEST (FIX_POLICY 2b), archived game 1.1.1.405907.
-- SRC: Lua/Units/Colonist.lua Colonist:Getui_command sha256=1f9e7adc17b84b9f16c7eea5cb83dcc9771e745c15a45941aefcedb0cd7eaa18
-- DEFECT: return\s+tcommand\s+or\s+ColonistCommands\["Unknown"\]
--   Without emigration_dome, Transport falls through to the same new-Dome text.
-- SRC: Lua/Units/Colonist.lua L4647-4649 sha256=7bb47b9b2dd5a3f4e19ed5efcb0543d5ec7ea3ccdd3742b465cb331fd905039c
-- DEFECT: Transport\s*=\s*T\(4333,\s*"Moving to a new Dome:

SMRFixPack.Register("RescueReturnText", {
	title = "Own-home shuttle rescues say returning to the dome",
	apply = function()
		local C = rawget(_G, "Colonist")
		local err = SMRFixPack.Require("RescueReturnText", {
			{ class = "Colonist", method = "Getui_command" },
			{ class = "Colonist", method = "GetEmigrationDomeDisplayName" },
			{ class = "Colonist", method = "SelectEmigrationDome" },
			{ global = "TGetID" },
			{ global = "Untranslated" },
			{ global = "IsKindOf" },
			-- Stub contract: Getui_command reads command, dreaming, transport_task,
			-- dome and emigration_dome, and calls IsInWorkCommand; it writes nothing
			-- and never yields (Colonist.lua:4672-4716), so a table stub is safe.
			{ probe = function()
				local home = {}
				local sample = {
					command = "Transport", dome = home,
					transport_task = { dest_dome = home },
					IsInWorkCommand = function() return false end,
				}
				return TGetID(C.Getui_command(sample)) == 4333
			end,
			  reason = "Transport no longer returns the shipped new-Dome command text" },
		})
		if err then return err end

		local orig = C.Getui_command
		local returning = Untranslated("Returning to Dome: <h SelectEmigrationDome InfopanelSelect><em><EmigrationDomeDisplayName></em></h>")
		C.Getui_command = function(self, ...)
			if not IsKindOf(self, "Colonist") then return orig(self, ...) end
			local result = orig(self, ...)
			local task = self.transport_task
			if self.command == "Transport" and not self.dreaming
				and task and not task.source_dome and not task.migration_dest
				and task.dest_dome ~= nil
				and task.dest_dome == self.dome
				and (not self.emigration_dome or self.emigration_dome == task.dest_dome)
				and TGetID(result) == 4333 then
				return returning
			end
			return result
		end
	end,
})
