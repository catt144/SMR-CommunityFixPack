-- F39: A solar panel built near the SECOND Artificial Sun is never lit by it.
--
-- Defect: SolarPanelBase:GameInit (Lua\Buildings\SolarPanel.lua:8-14) looks at
-- exactly one sun:
--     local sun = self.city.labels.ArtificialSun and self.city.labels.ArtificialSun[1] or nil
--     if sun and TestSunPanelRange(sun, self) then self.artificial_sun = sun end
-- If the first Artificial Sun in the label is out of range the panel gives up,
-- even when a second one is standing right next to it.
--
-- The reverse direction is correct — ArtificialSunBase:GameInit
-- (ArtificialSun.lua:34-48) queries every SolarPanelBase around itself and calls
-- SetArtificialSun on each — so the bug only shows when the panel is the thing
-- built last. That is the common case: you build the second sun, then fill the
-- area around it with panels, and none of them get the bonus.
--
-- Patch approach: chained post-wrapper on SolarPanelBase:GameInit. The shipped
-- body runs untouched; if it left the panel unlit we walk the rest of the label
-- and hand the first sun in range to the shipped SetArtificialSun (:66-69), which
-- also refreshes production. GameInit is a combined method
-- (CommonLua\Classes\_object.lua:22, DefineCombinedMethod) built from the
-- classdefs when the classes are assembled — after mod code loads — so writing
-- onto SolarPanelBase is picked up for every panel class and for RCSolar.
--
-- Plus a LoadGame sweep: `artificial_sun` is a persisted member and nothing ever
-- re-evaluates it, so panels already built next to sun #2 in an existing save stay
-- unlit forever without one.

local function find_sun_in_range(panel)
	local city = panel.city
	local suns = city and city.labels and city.labels.ArtificialSun
	if not suns then return end
	for _, sun in ipairs(suns) do
		if IsValid(sun) and TestSunPanelRange(sun, panel) then
			return sun
		end
	end
end

SMRFixPack.Register("SecondArtificialSun", {
	title = "Solar panels are lit by any Artificial Sun in range, not only the first one built",
	apply = function()
		local SP = rawget(_G, "SolarPanelBase")
		if type(SP) ~= "table" or type(SP.GameInit) ~= "function"
			or type(SP.SetArtificialSun) ~= "function" then
			return "SolarPanelBase.GameInit/SetArtificialSun not found (game update changed it?)"
		end
		if type(rawget(_G, "TestSunPanelRange")) ~= "function" then
			return "TestSunPanelRange not found (game update changed it?)"
		end

		local orig = SP.GameInit
		function SP:GameInit(...)
			local r = orig(self, ...)
			-- FIX (F39): the shipped body only ever tested labels.ArtificialSun[1].
			if not self.artificial_sun then
				local sun = find_sun_in_range(self)
				if sun then self:SetArtificialSun(sun) end
			end
			return r
		end
	end,
})

-- Panels built next to a second sun before this fix existed are still dark in the
-- save; nothing re-runs the range test for them.
function OnMsg.LoadGame()
	local fix = SMRFixPack.fixes.SecondArtificialSun
	if not (fix and fix.status == "active") then return end
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end

	local lit = 0
	AllMapsForEach("map", "SolarPanelBase", function(panel)
		if not panel.artificial_sun then
			local sun = find_sun_in_range(panel)
			if sun then
				panel:SetArtificialSun(sun)
				lit = lit + 1
			end
		end
	end)

	if lit > 0 then
		local msg = string.format("[CommunityFixPack] SecondArtificialSun: reconnected %d solar panel(s) to an Artificial Sun in range", lit)
		if rawget(_G, "ModLog") then ModLog(msg) else print(msg) end
	end
end
