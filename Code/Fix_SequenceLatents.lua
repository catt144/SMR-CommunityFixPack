-- F29: two latent defects in the sequence/mystery systems. Both are mod-facing:
-- nothing shipped exercises either path, but both are part of the surface a
-- scenario or mystery author builds on.
--
-- (a) `SA_GetLabelToRegister:SAExec` (`Lua\Sequences\SA_Filters.lua:30-40`)
-- computes how many objects the author asked for and then hands back all of
-- them:
--     local count = Min(#objs, MulDivRound(#objs, self.random_percent, 100))
--     if self.random_count ~= 0 then count = Min(self.random_count, count) end
--     table.shuffle(objs, GetInteractionSeed(self.parent_seq_id))
--     ...
--     return objs
-- `count` is never used. The action's own editor text promises otherwise —
-- "Get %s objects of label %s", "Get %s%% of the objects of label %s"
-- (`:20-27`) — so `random_count` and `random_percent` are advertised, honoured
-- by the shuffle, and then thrown away. The shuffle is the giveaway: it exists
-- only to make a truncation fair.
--
-- (b) `AlienDigger:GameInit` (`Lua\Mysteries\Diggers.lua:91-95`) is a broken
-- two-variable swap:
--     if self.pre_hit_ground_t < self.pre_hit_ground_t_2 then
--         local t = self.pre_hit_ground_t
--         self.pre_hit_ground_t = self.pre_hit_ground_t_2
--         self.pre_hit_ground_t_2 = self.pre_hit_ground_t   -- already overwritten
--     end
-- `t` is saved and never read, so both fields end up holding the LARGER value
-- instead of being ordered. Unreachable with the shipped defaults (which are
-- already in order), but any subclass or preset that sets them the other way
-- around loses the smaller timing entirely.
--
-- Patch approach: two independent method replacements (copies from shipped
-- Src, game 1.0.7.396349), each tiny, each self-checked separately so one
-- missing target cannot take the other down.
--
-- *Deliberately NOT fixed — the third item on the tracker entry.*
-- `SA_WaitMarsTime:GenerateSequenceCode` (`Lua\Sequences\SA_Gameplay.lua:2705`)
-- emits `while CurrentWorkshift == target_workshift ...`, the exact inverse of
-- the interpreted path's `StopWait` (`:2617-2631`, which stops when
-- `CurrentWorkshift == self.target_workshift`), so generated code waits while it
-- IS the target shift instead of until it becomes one. It is real, but it is a
-- CODE GENERATOR: it runs when a sequence is compiled in the Mod Editor, not
-- when one plays, and mod code cannot regenerate sequences that were already
-- compiled. Repairing it would mean replacing the whole multi-branch generator
-- for a path with no shipped user and no runtime effect. Recorded on the F29
-- entry instead.

SMRFixPack.Register("SequenceLatents", {
	title = "Sequence label sampling and the Digger timing swap behave as written",
	apply = function()
		local fixed, skipped = {}, {}

		---- (a) SA_GetLabelToRegister honours random_count / random_percent ----
		local A = rawget(_G, "SA_GetLabelToRegister")
		if type(A) == "table" and type(rawget(A, "SAExec")) == "function" then
			function A:SAExec(seq_player, ip, seq, registers)
				local objs = GetObjectsByLabel(self.map.City, self.label) or {}
				if #objs > 0 then
					local count = Min(#objs, MulDivRound(#objs, self.random_percent, 100))
					if self.random_count ~= 0 then
						count = Min(self.random_count, count)
					end
					table.shuffle(objs, GetInteractionSeed(self.parent_seq_id))
					-- FIX (F29a): the shipped body computes `count`, shuffles so the
					-- truncation would be fair, and then returns the whole list.
					for i = #objs, count + 1, -1 do
						objs[i] = nil
					end
				end
				return objs
			end
			fixed[#fixed + 1] = "SA_GetLabelToRegister"
		else
			skipped[#skipped + 1] = "SA_GetLabelToRegister.SAExec"
		end

		---- (b) AlienDigger orders its two pre-hit timings -------------------
		local D = rawget(_G, "AlienDigger")
		if type(D) == "table" and type(rawget(D, "GameInit")) == "function" then
			function D:GameInit()
				MainCity:AddToLabel("AlienDiggers", self)
				self:SetCommand("Idle")

				if self.pre_hit_ground_t < self.pre_hit_ground_t_2 then
					local t = self.pre_hit_ground_t
					self.pre_hit_ground_t = self.pre_hit_ground_t_2
					-- FIX (F29b): shipped assigns self.pre_hit_ground_t here, which
					-- the line above has already overwritten, so both fields end up
					-- holding the larger value. `t` is the saved original.
					self.pre_hit_ground_t_2 = t
				end
			end
			fixed[#fixed + 1] = "AlienDigger"
		else
			skipped[#skipped + 1] = "AlienDigger.GameInit"
		end

		if #fixed == 0 then
			return "neither sequence target was found (game update changed them?)"
		end
		SMRFixPack.SequenceLatents = { fixed = fixed, skipped = skipped }
		if #skipped > 0 then
			return nil   -- partial is still active; the detail is on SMRFixPack.SequenceLatents
		end
	end,
})
