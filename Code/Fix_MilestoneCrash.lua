-- F05: Completing the last milestone crashes in No-Terraforming / No-Politics games.
--
-- Defect: the local eval_complete_all_milestones (Lua\Milestones.lua:87-106) lets
-- hidden-but-uncompleted milestones fall through to
--     score_sum = score_sum + milestone:GetScore()
-- and GetScore() returns nil for uncompleted milestones -> arithmetic-on-nil error
-- inside CompleteMilestone. Hidden milestones are guaranteed with the
-- NoTerraforming rule (9 terraforming milestones) or NoPolitics (Independence), so
-- completing the final visible milestone errors and the "AllMilestonesCompleted"
-- popup is lost.
--
-- Patch approach: the eval function is a file-local, so we replace the global
-- CompleteMilestone with a copy (of Lua\Milestones.lua:108-142, shipped Src,
-- game 1.0.7.396349) whose completion check is inlined and nil-safe. Changes
-- marked -- FIX.

SMRFixPack.Register("MilestoneCrash", {
	title = "Completing all milestones no longer errors in No Terraforming / No Politics games",
	apply = function()
		if type(CompleteMilestone) ~= "function" then
			return "CompleteMilestone not found (game update changed it?)"
		end

		local function eval_complete_all_milestones(milestones)
			local sponsor = GetMissionSponsor()
			local commander = GetCommanderProfile()
			local all_completed = true
			local score_sum = 0
			for _, milestone in ipairs(milestones) do
				local id = milestone.id
				local hidden = milestone.prerequisite and not milestone.prerequisite:eval(milestone)
				if not MilestoneCompleted[id] and not hidden then
					all_completed = false
					break
				end
				score_sum = score_sum + (milestone:GetScore() or 0) -- FIX: GetScore() is nil for hidden uncompleted milestones
			end
			if all_completed then
				CreateRealTimeThread(function()
					WaitPopupNotification("AllMilestonesCompleted", { params = { sponsor = sponsor.display_name, commander = commander.display_name, sol = UIColony.day, score = score_sum } })
				end)
			end
		end

		local function fixed_CompleteMilestone(id, res)
			if g_Tutorial or ChangingMapInEditorMode or not HasGameLogic(CurrentMap) then
				return
			end

			local milestones = PresetArray("Milestone")
			local milestone = table.find_value(milestones, "id", id)
			if not milestone then
				assert(milestone, "Missing milestone preset: " .. id)
				return
			end

			if milestone.prerequisite and not milestone.prerequisite:eval(milestone) then
				return
			end

			if MilestoneCompleted[id] ~= nil then
				-- some milestones could have already been failed
				return
			end
			MilestoneCompleted[id] = res and GameTime() or false
			ObjModified(MilestoneCompleted)
			if not res then
				return
			end

			MilestoneEnactors[id] = MainCity
			Msg("MilestoneCompleted", id)
			milestone:ShowUINotifications()
			if milestone.trigger_fireworks then
				hr.ShowFireworks = GetAccountStorageOptionValue("ShowFireworks") == "On" and 1 or 0
				TriggerFireworks(MainMap)
			end
			eval_complete_all_milestones(milestones)
		end

		-- Phase 4 (C4): this install previously had no read-back verification —
		-- the only global replacement in the pack without one.
		return SMRFixPack.SetGlobal("CompleteMilestone", fixed_CompleteMilestone)
	end,
})
