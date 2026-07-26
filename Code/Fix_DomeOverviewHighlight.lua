-- F14: The Domes Overview never highlights a dome whose colonists are in trouble.
--
-- Defect: Community:UICommandCenterStatUpdate (Lua\X\ColonyControlCenter.lua:
-- 1308-1320) builds the red-tagged text and then throws it away:
--     local tv
--     if v < low then tv = Untranslated(string.format("<red>%d</red>", v))
--     else tv = Untranslated(v) end
--     win.idLabel:SetText(v)          -- v, not tv
-- so the low-stat column is drawn in the ordinary colour whatever the value, and
-- the Domes Overview gives the player no way to spot the dome with the failing
-- Health, Sanity, Comfort or Morale.
--
-- Patch approach: replacement of the small method — a copy of
-- Lua\X\ColonyControlCenter.lua:1308-1320 (shipped Src, game 1.0.7.396349) with the display
-- value actually used. Change marked -- FIX.

SMRFixPack.Register("DomeOverviewHighlight", {
	title = "Domes Overview marks low colonist stats in red again",
	apply = function()
		local C = rawget(_G, "Community")
		if type(C) ~= "table" or type(C.UICommandCenterStatUpdate) ~= "function" then
			return "Community.UICommandCenterStatUpdate not found (game update changed it?)"
		end
		if type(rawget(_G, "GetAverageStat")) ~= "function" then
			return "GetAverageStat not found (game update changed it?)"
		end

		function C:UICommandCenterStatUpdate(win, stat)
			local stat_scale = const.Scale.Stat
			local v = GetAverageStat(self.labels.Colonist, stat) / stat_scale
			local tv
			local low = g_Consts.LowStatLevel / stat_scale
			if v < low then
				tv = Untranslated(string.format("<red>%d</red>", v))
			else
				tv = Untranslated(v)
			end
			win.idLabel:SetText(tv) -- FIX (F14): shipped code passed v, discarding the red tag
		end
	end,
})
