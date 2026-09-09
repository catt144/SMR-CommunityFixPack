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

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/X/ColonyControlCenter.lua Community:UICommandCenterStatUpdate sha256=bc009d01c3fb15d65127ee5bb143be217db4dd12726a2615b32103914e715845
--   (Lua/X/ColonyControlCenter.lua:1290-1301 at pin time)
-- DEFECT: idLabel:SetText\(v\)
--   the red-tagged `tv` is built and then `v` is displayed

SMRFixPack.Register("DomeOverviewHighlight", {
	title = "Domes Overview marks low colonist stats in red again",
	apply = function()
		local err = SMRFixPack.Require("DomeOverviewHighlight", {
			{ class = "Community", method = "UICommandCenterStatUpdate" },
			{ global = "GetAverageStat" },
		})
		if err then return err end
		local C = Community

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
