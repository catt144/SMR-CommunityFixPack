-- F29: two latent defects in the sequence/mystery systems.
--
-- ⚠️ NOT mod-facing, despite what this header said until 2026-07-30. The
-- reachability audit enumerated both: item (a) has FOUR shipped callers, all in
-- Mystery 2 "Dredgers" (`Mystery 2.lua:235, :252, :280, :284`), and item (b)
-- runs for every digger that mystery spawns. Both are tier **R3 —
-- latent-by-DATA**: the game executes this code in ordinary play and only the
-- shipped VALUES keep it benign, so a patch or DLC can expose it with no mod
-- involved (FIX_POLICY §4a case 3). See the F29 entry.
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
-- (`:18-28`) — so `random_count` and `random_percent` are advertised, honoured
-- by the shuffle, and then thrown away. The shuffle is the giveaway: it exists
-- only to make a truncation fair.
--
-- (b) `AlienDigger:GameInit` (`Lua\Mysteries\Diggers.lua:86-95`) is a broken
-- two-variable swap:
--     if self.pre_hit_ground_t < self.pre_hit_ground_t_2 then
--         local t = self.pre_hit_ground_t
--         self.pre_hit_ground_t = self.pre_hit_ground_t_2
--         self.pre_hit_ground_t_2 = self.pre_hit_ground_t   -- already overwritten
--     end
-- `t` is saved and never read, so both fields end up holding the LARGER value
-- instead of being ordered. Unreachable with the shipped defaults (1000/500,
-- `Diggers.lua:52-53`, already in order), but any subclass or preset that sets
-- them the other way around loses the smaller timing entirely.
--
-- Patch approach: two independent FIX_POLICY §1.4 chained wrappers, each
-- self-checked separately so one missing target cannot take the other down.
-- Both are §3a **layer 2** — (a) does its work after a synchronous call and
-- returns, (b) does all of its work BEFORE `return orig(self)`.
--
-- ⭐ CONVERTED 2026-08-02 from two §1.5 method replacements, on an explicit
-- owner decision (BUGS F29, "PACKAGE 0 — DECIDED: CONVERT"). FIX_POLICY §4's
-- 2026-08-01 amendment allows an R3 defect to ship only as a §1.1-§1.4 patch
-- unless the owner decides otherwise; converting satisfies the rule rather than
-- invoking the exception. THE DEFECT CLAIMS ARE UNTOUCHED — this changes the
-- technique, not the fix, and both wrappers are no-ops on today's data exactly
-- as the replacements were.
--
-- (a) before/after — POST-wrapper, and it retires an unrecorded risk. The old
-- copy truncated the list `GetObjectsByLabel` returned while assuming that list
-- was not the live city label; true, but nowhere written down. It is verified
-- here: `GetObjectsByLabel` ends in `return table.icopy(labels[label])`
-- (`SA_Gameplay.lua:147-168`), and its one other branch ("Working-age") builds a
-- fresh table too — so the returned list is always ours to mutate and no city
-- label can be shortened by this fix. The wrapper re-derives `count` from
-- `self.random_percent` / `self.random_count` and `#objs` AFTER `orig` returns;
-- `table.shuffle` permutes in place and does not change the length, so that is
-- the same `count` the shipped body computed and discarded. The shuffle stays
-- vanilla's.
--
-- (b) before/after — PRE-wrapper, ZERO copied lines. Ordering the two fields
-- before delegating makes the shipped `if self.pre_hit_ground_t <
-- self.pre_hit_ground_t_2` false BY CONSTRUCTION, so its broken swap becomes
-- unreachable instead of being replaced. The one ordering difference against the
-- old copy — the fields are now settled before `MainCity:AddToLabel` and
-- `SetCommand("Idle")` rather than after — is not observable: game-time thread
-- creation DEFERS (ENGINE_FACTS, measured twice), so the Idle command thread
-- cannot run before `GameInit` returns and sees the final values either way.
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

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Sequences/SA_Filters.lua SA_GetLabelToRegister:SAExec sha256=d0f254c8b59609a018e81ee79aa7277b7a586ce9cc7fe7a47d200d82ba8573bd
--   (Lua/Sequences/SA_Filters.lua:30-40 at pin time)
-- DEFECT: local count = Min\(#objs, MulDivRound\(#objs, self\.random_percent, 100\)\)
--   (a) `count` is computed, the list is shuffled, and every object is
--   returned
-- SRC: Lua/Mysteries/Diggers.lua AlienDigger:GameInit sha256=b1ecb8ec15cf9053b483912427a0a0d3d773cb6cea2bb084f2530ab4b1fd035a
--   (Lua/Mysteries/Diggers.lua:87-96 at pin time)
-- DEFECT: local t = self\.pre_hit_ground_t\s+self\.pre_hit_ground_t = self\.pre_hit_ground_t_2\s+self\.pre_hit_ground_t_2 = self\.pre_hit_ground_t\s+end
--   (b) the swap reads the field it has already overwritten; `t` is never read

SMRFixPack.Register("SequenceLatents", {
	title = "Sequence label sampling and the Digger timing swap behave as written",
	apply = function()
		local fixed, skipped = {}, {}

		---- (a) SA_GetLabelToRegister honours random_count / random_percent ----
		local A = rawget(_G, "SA_GetLabelToRegister")
		if type(A) == "table" and type(rawget(A, "SAExec")) == "function" then
			local orig_exec = A.SAExec
			function A:SAExec(seq_player, ip, seq, registers)
				local objs = orig_exec(self, seq_player, ip, seq, registers)
				-- FIX (F29a): the shipped body computes `count`, shuffles so the
				-- truncation would be fair, and then returns the whole list. The
				-- list is a copy (GetObjectsByLabel -> table.icopy), so dropping
				-- its tail here reaches no city label.
				if type(objs) == "table" and #objs > 0 then
					local count = Min(#objs, MulDivRound(#objs, self.random_percent, 100))
					if self.random_count ~= 0 then
						count = Min(self.random_count, count)
					end
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
			local orig_init = D.GameInit
			function D:GameInit()
				-- FIX (F29b): order the two timings BEFORE delegating. The shipped
				-- body's `if self.pre_hit_ground_t < self.pre_hit_ground_t_2` is
				-- then false by construction, so its broken swap — which assigns
				-- the field the line above has already overwritten, leaving BOTH
				-- holding the larger value — never executes.
				if self.pre_hit_ground_t < self.pre_hit_ground_t_2 then
					self.pre_hit_ground_t, self.pre_hit_ground_t_2 =
						self.pre_hit_ground_t_2, self.pre_hit_ground_t
				end
				return orig_init(self)
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
