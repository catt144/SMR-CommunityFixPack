-- F04: Night-shift (third shift) colonists never return to work after midnight.
--
-- Defect: Colonist:ShouldLeaveForWork (Lua\Units\Colonist.lua:1758-1768) checks
--     hour >= workshift_start - 1 and hour <= workshift_start + 3
-- with no wrap-around. Shift 3 starts at hour 22 (const.DefaultWorkshifts =
-- {{6,14},{14,22},{22,6}}), so the window becomes `hour >= 21 and hour <= 25` —
-- but the game clock is 0-23, making the catch-up hours 24/25 (i.e. 0:00-1:59)
-- unreachable. A third-shift colonist who was busy at shift start (meal, rest,
-- medical visit, just arrived) and goes idle after midnight skips the entire
-- remainder of their shift; night-staffed buildings silently run understaffed
-- while the player pays the night-shift sanity penalty. This is the only gate
-- that sends colonists to work (Colonist:Idle, :1770). The codebase handles
-- wrap-around correctly elsewhere (IsDarkHour uses % 24), proving intent.
--
-- Patch approach: FIX_POLICY §1.4 chained POST-wrapper. The repair only ever
-- needs the answer to be `true` in MORE cases, never fewer, so the shipped body
-- decides first and we only add the hours it cannot reach:
--     local r = orig(self) if r then return r end  -- then the wrap-around window
-- Layer: §3a layer 2 — the wrapper does no work that can be interrupted and
-- `orig` is a pure predicate.
--
-- CONVERTED 2026-08-02 from a §1.5 reconstruction (SAVE_SAFETY_REDESIGN §5.4
-- group A). Before/after: the reconstructed body (modular-distance rewrite of
-- the whole method) is gone; the modular test survives only as the ADDITIONAL
-- branch. Behaviour is unchanged, and the shift-1/2 half is now identical BY
-- CONSTRUCTION rather than by the old copy's hand-verified "bit-identical"
-- claim — vanilla answers first on every hour it already answered.
-- Equivalence for shift 3 and for the early-leave window: the shipped condition
-- is a strict SUBSET of the modular one, checked for every (start, hour, early)
-- combination the game can produce —
--   * window 1, hour in [start-1, start+3] clamped to 0..23 → d in {23,0,1,2,3};
--   * window 2, hour in [start-early, start] → start-hour in [0,early], so
--     either d == 0 or 24-d == start-hour <= early;
--   * where start-early goes negative (early > start) vanilla widens to hours
--     0..start, all of which satisfy 24-d <= early as well.
-- So `orig(...) or <modular window>` and `<modular window>` alone select the
-- same hours; the union adds nothing and removes nothing.

SMRFixPack.Register("NightShiftWork", {
	title = "Night-shift colonists go to work after midnight instead of skipping their shift",
	apply = function()
		local err = SMRFixPack.Require("NightShiftWork", {
			{ class = "Colonist", method = "ShouldLeaveForWork" },
		})
		if err then return err end
		local orig = Colonist.ShouldLeaveForWork

		local HOURS = const.HoursPerDay -- 24

		function Colonist:ShouldLeaveForWork()
			local r = orig(self)
			if r then return r end
			-- FIX (F04): the hours the shipped range test cannot express. Its
			-- window is `hour >= start-1 and hour <= start+3` on a 0-23 clock, so
			-- shift 3 (start 22) loses the catch-up hours 24/25 = 0:00-1:59.
			if self.workplace then
				local hour = UIColony.hour
				local workshift_start = const.DefaultWorkshifts[self.workplace_shift][1]
				-- modular distance: d in {23(=start-1), 0..3} == the shipped window
				local d = (hour - workshift_start) % HOURS
				if d <= 3 or d == HOURS - 1 then
					return true
				end
				local early = self.leave_early_for_work
				if early and d > 0 and (HOURS - d) <= early then
					return true
				end
			end
		end
	end,
})
