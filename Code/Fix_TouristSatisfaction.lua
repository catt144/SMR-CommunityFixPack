-- F09: Tourist Satisfaction drifts downwards no matter how well the tourist is
-- treated, which quietly lowers every holiday payout.
--
-- Defect: Colonist:UpdateSatisfaction (Lua\Units\Colonist.lua:4006-4032) awards
-- satisfaction for crossing the "low", "high" and "perfect" stat thresholds, but
-- the up-crossings are exclusive while the down-crossings are cumulative:
--     if new_value >= low and new_value < high and old_value < low then  +low
--     if new_value >= high and new_value < 100 and old_value < high then +high
-- so a stat that jumps from below `low` straight past `high` collects the +high
-- award but never the +low one, and a jump from mid-range to a perfect 100 collects
-- +perfect but not +high. Falling back down, by contrast, pays every threshold it
-- passes: 100 -> 0 charges -perfect, -high AND -low. Two-tier jumps are routine —
-- a service visit sets Comfort directly, and StressedOut recovery restores +50
-- Sanity in one step (StatusEffects.lua:264) — so satisfaction is path-dependent
-- and ratchets down. In the satisfaction log this reads as two red rows for every
-- green one.
--
-- Patch approach: full replacement of the self-contained method — the awards are
-- restated as a value tier (below low / low..high / high..100 / 100) with the
-- difference between the old and new tier applied. Each threshold still produces
-- its own +/- entry with the same reason string, so the satisfaction log is
-- unchanged in form; single-threshold moves behave exactly as they do today. Only
-- multi-threshold moves change, and only to pay symmetrically. Nothing is awarded
-- when the tier does not change. Source: Lua\Units\Colonist.lua:4006-4032 (shipped Src,
-- game 1.0.7.396349); the file-local stat_scale is recreated (Colonist.lua:1).

SMRFixPack.Register("TouristSatisfaction", {
	title = "Tourist satisfaction stops drifting down (threshold awards are now symmetric)",
	apply = function()
		local err = SMRFixPack.Require("TouristSatisfaction", {
			{ class = "Colonist", method = "UpdateSatisfaction" },
			{ path = { "const", "Scale", "Stat" } },
		})
		if err then return err end
		local C = Colonist
		local stat_scale = const.Scale.Stat

		function C:UpdateSatisfaction(stat, old_value, new_value, high_stat_bonus, perfect_stat_bonus)
			if not self.traits.Tourist or self:IsDead() then return end

			old_value = old_value / stat_scale
			new_value = new_value / stat_scale
			local low = g_Consts.LowStatLevel / stat_scale
			local high = g_Consts.HighStatLevel / stat_scale

			-- FIX (F09): rank the value instead of testing each threshold in
			-- isolation, so an upward jump across two thresholds pays both awards
			-- exactly as a downward jump charges both.
			local function tier(v)
				if v >= 100 then return 3 end
				if v >= high then return 2 end
				if v >= low then return 1 end
				return 0
			end
			local old_tier, new_tier = tier(old_value), tier(new_value)
			if old_tier == new_tier then return end

			-- Low stat
			if (new_tier >= 1) ~= (old_tier >= 1) then
				local up = new_tier >= 1
				self:ChangeSatisfaction((up and 1 or -1) * g_Consts.SatisfactionLowStatPenalty * stat_scale,
					(up and "+low " or "-low ") .. stat)
			end
			-- High stat
			if (new_tier >= 2) ~= (old_tier >= 2) then
				local up = new_tier >= 2
				self:ChangeSatisfaction((up and 1 or -1) * high_stat_bonus * stat_scale,
					(up and "+high " or "-high ") .. stat)
			end
			-- Perfect stat
			if (new_tier >= 3) ~= (old_tier >= 3) then
				local up = new_tier >= 3
				self:ChangeSatisfaction((up and 1 or -1) * perfect_stat_bonus * stat_scale,
					(up and "+perfect " or "-perfect ") .. stat)
			end
		end
	end,
})
