-- F01: Cave-ins ignore the "No Disasters" game rule.
--
-- Defect: the underground marsquake scheduler — MapGameTimeRepeat("UndergroundMarsquake")
-- in Lua\Marsquake.lua (repeat body at lines 306-325) — never checks the NoDisasters
-- rule, while every other disaster does (ColdWave.lua:222, DustStorm.lua:413,
-- DustDevils.lua:189, and the surface marsquake path Marsquake.lua:43).
-- Player impact: cave-ins keep destroying underground colonies in games created
-- with the No Disasters rule. Matches live player reports on the Paradox forum.
--
-- Patch approach (mod-friendly): the repeat's registration entry persists in the
-- global PeriodicRepeatInfo table (CommonLua\Core\lib.lua:1532; slot layout
-- THREAD=1, SLEEP=2, FUNC=3, COND=4, CLASS=5 at lib.lua:1538-1542). We wrap the
-- stored FUNC (slot 3) so that when the rule is active the tick returns the normal
-- reschedule interval without triggering a quake. Wrapping (not replacing) means
-- another mod that also wraps this repeat still runs; the repeat's timing,
-- condition, and thread management are untouched. Story-scripted cave-ins
-- (BuriedWonder scenarios) intentionally still work — they are player-triggered
-- events, not random disasters.

SMRFixPack.Register("CaveInsNoDisasters", {
	title = 'Cave-ins no longer occur when the "No Disasters" game rule is active',
	apply = function()
		local err = SMRFixPack.Require("CaveInsNoDisasters", {
			{ path = { "PeriodicRepeatInfo", "UndergroundMarsquake" },
			  reason = "UndergroundMarsquake repeat not found (game update changed it?)" },
			-- slot layout THREAD=1, SLEEP=2, FUNC=3 (lib.lua:1538-1542)
			{ path = { "PeriodicRepeatInfo", "UndergroundMarsquake", 3 }, kind = "function",
			  reason = "unexpected PeriodicRepeatInfo layout (game update changed it?)" },
		})
		if err then return err end
		local FUNC = 3
		local info = PeriodicRepeatInfo["UndergroundMarsquake"]
		local orig = info[FUNC]

		info[FUNC] = function(sleep, map, ...)
			-- First call (sleep == nil) only asks for the interval; quakes fire on
			-- later calls. Skip those while No Disasters is active, but return the
			-- same interval the original would, to keep the schedule alive.
			if sleep and IsGameRuleActive("NoDisasters") then
				return g_Consts.MarsquakeSpawnTime * const.HourDuration
			end
			return orig(sleep, map, ...)
		end
	end,
})
