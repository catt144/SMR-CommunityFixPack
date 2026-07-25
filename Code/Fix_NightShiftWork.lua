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
-- that sends colonists to work (Colonist:Idle, :1911). The codebase handles
-- wrap-around correctly elsewhere (IsDarkHour uses % 24), proving intent.
--
-- Patch approach: full replacement of the small self-contained method using
-- modular hour distance; behavior for shifts 1/2 is bit-identical to shipped
-- (window start-1 .. start+3, plus the leave_early_for_work window).

SMRFixPack.Register("NightShiftWork", {
	title = "Night-shift colonists go to work after midnight instead of skipping their shift",
	apply = function()
		if type(Colonist.ShouldLeaveForWork) ~= "function" then
			return "Colonist.ShouldLeaveForWork not found (game update changed it?)"
		end

		local HOURS = const.HoursPerDay -- 24

		function Colonist:ShouldLeaveForWork()
			if self.workplace then
				local hour = UIColony.hour
				local workshift_start = const.DefaultWorkshifts[self.workplace_shift][1]
				-- FIX: modular distance instead of a raw range so the window wraps
				-- past midnight. d in {23(=start-1), 0..3} == shipped window.
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
