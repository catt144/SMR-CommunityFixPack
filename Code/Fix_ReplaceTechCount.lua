-- F28: `Research:ReplaceTech` mishandles the per-field researched counter when
-- it swaps out a tech that was already researched.
--
-- Defect (`Lua\Research.lua:715`):
--     if not next(g_TechFieldResearchedCount[field_id] == 0) then
--         g_TechFieldResearchedCount[field_id] = nil
--     end
-- `next()` is handed the RESULT OF A COMPARISON — a boolean — because the
-- parentheses swallowed the whole test. The intended shape survives four hundred
-- lines earlier in the same file, in `Research:SetTechUndiscovered`
-- (`:246-249`):
--     g_TechFieldDiscoveredCount[tech.field] = g_TechFieldDiscoveredCount[tech.field] - 1
--     if g_TechFieldDiscoveredCount[tech.field] == 0 then
--         g_TechFieldDiscoveredCount[tech.field] = nil
--     end
-- FIX_POLICY §4's "the same author wrote it correctly elsewhere" test, exactly.
--
-- What the broken line actually does is not asserted here. Either `next(false)`
-- raises — in which case the function dies before `self:SetTechResearched(
-- tech_id_new, "notify")` on the next line and the replacement tech is never
-- marked researched — or this engine tolerates it the way it tolerates
-- `next(nil)`, in which case it returns nil, `not nil` is true, and the field's
-- counter is DROPPED even while techs in that field are still researched.
-- Both are wrong and both are repaired by writing the comparison the sibling
-- code writes; the pack does not claim a crash it has not observed (the F10
-- lesson).
--
-- Latent for players: nothing in the base game calls `ReplaceTech`. It is
-- reached from mods, storybits and the console, which is why this is P3 and
-- mod-facing rather than a gameplay fix.
--
-- Patch approach: full replacement of `Research:ReplaceTech` — a copy of
-- Research.lua:684-720 (shipped Src, 2026-07) with one line corrected, marked
-- -- FIX. Replacement because the defect is a statement in the middle of the
-- function, with the call that matters on the very next line.
--
-- The three shipped `assert` lines are dropped from the copy: asserts do not
-- unwind in this engine, so they are log lines rather than guards, and the
-- `if not status then return end` immediately after the first one is the real
-- check.

SMRFixPack.Register("ReplaceTechCount", {
	title = "Research:ReplaceTech keeps the per-field researched counter honest",
	apply = function()
		local R = rawget(_G, "Research")
		if type(R) ~= "table" or type(R.ReplaceTech) ~= "function" then
			return "Research.ReplaceTech not found (game update changed it?)"
		end
		if type(R.SetTechResearched) ~= "function" or type(R.TechQueueIndex) ~= "function"
			or type(R.DequeueResearch) ~= "function" or type(R.QueueResearch) ~= "function" then
			return "Research helpers not found (game update changed it?)"
		end

		function R:ReplaceTech(tech_id, tech_id_new)
			local status = self.tech_status[tech_id]
			if not status then return end

			local tech_def = TechDef[tech_id_new]

			local is_queued = self:TechQueueIndex(tech_id)
			if is_queued then
				self:DequeueResearch(tech_id)
			end

			self.tech_status[tech_id] = nil
			self.tech_status[tech_id_new] = status

			local field_id = tech_def.group
			local field = self.tech_field[field_id]
			local field_idx = table.find(field, tech_id)
			if field_idx then
				field[field_idx] = tech_id_new
			end

			if is_queued then
				self:QueueResearch(tech_id_new)
			elseif status.researched then
				status.researched = false
				g_TechResearchedCount = g_TechResearchedCount - 1
				g_TechFieldResearchedCount[field_id] = g_TechFieldResearchedCount[field_id] - 1
				-- FIX (F28): shipped reads `not next(<count> == 0)` — next() applied
				-- to a boolean. Same shape as Research:SetTechUndiscovered (:247-249).
				if g_TechFieldResearchedCount[field_id] == 0 then
					g_TechFieldResearchedCount[field_id] = nil
				end
				self:SetTechResearched(tech_id_new, "notify")
			end
		end
	end,
})
