-- F37: A salvaged farm keeps supplying its dome with oxygen forever.
--
-- Defect: FarmBase:ApplyOxygenProductionMod (Lua\Buildings\Farm.lua:561-571)
-- registers the crop's oxygen output as a NEGATIVE air_consumption modifier on
-- the PARENT DOME, keyed by the farm's own id (`self.farm_id`, assigned once in
-- FarmBase:Init, :80):
--     self.parent_dome:SetModifier("air_consumption", self.farm_id, -amount, 0, ...)
-- Nothing ever clears it when the farm goes away. FarmBase declares no Done;
-- Building:Done (Building.lua:505-514) and Building:SetDome (:670-690) clean up
-- upgrade modifiers but know nothing about this one; and the demolish path skips
-- UpdateWorking(false) for buildings without a demolished state
-- (Building.lua:1457-1483, Demolishable.lua:139), so the "crop is gone" branch
-- never runs either. The dome keeps the phantom oxygen for the rest of the game,
-- and every rebuild adds another one under a fresh farm id.
--
-- Patch approach: chained pre-wrapper on Building:SetDome — the single funnel for
-- a farm parting company with its dome. Building:Done calls SetDome(false) itself
-- (:513), so demolish, salvage, destruction and plain dome changes are all
-- covered by one hook. Gated to FarmBase so no other building pays for it.
-- Plus a LoadGame sweep that removes farm-keyed air_consumption modifiers whose
-- farm no longer lives in that dome — without it, saves already carrying phantom
-- oxygen keep it. The sweep only removes modifiers whose id matches the farm id
-- pattern and has no live owner, so it cannot touch another mod's modifiers.

SMRFixPack.Register("GhostFarmOxygen", {
	title = "Salvaging a farm removes the oxygen it was giving its dome",
	apply = function()
		local B = rawget(_G, "Building")
		if type(B) ~= "table" or type(B.SetDome) ~= "function" then
			return "Building.SetDome not found (game update changed it?)"
		end
		local F = rawget(_G, "FarmBase")
		if type(F) ~= "table" or type(F.ApplyOxygenProductionMod) ~= "function" then
			return "FarmBase.ApplyOxygenProductionMod not found (game update changed it?)"
		end

		local orig = B.SetDome
		function B:SetDome(dome, ...)
			-- FIX (F37): drop the farm's oxygen modifier from the dome it is leaving.
			local old = self.parent_dome
			if old and old ~= dome and self.farm_id and IsKindOf(self, "FarmBase") then
				if IsValid(old) and not IsBeingDestructed(old) then
					old:SetModifier("air_consumption", self.farm_id, 0, 0)
					old:UpdateWorking()
				end
			end
			return orig(self, dome, ...)
		end
	end,
})

-- Saves made before this fix carry one leftover modifier per farm ever removed.
OnMsg.LoadGame = SMRFixPack.WhenActive("GhostFarmOxygen", function()
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end

	local live = {}
	AllMapsForEach(true, "FarmBase", function(farm)
		local dome = farm.parent_dome
		if farm.farm_id and IsValid(dome) then
			local ids = live[dome]
			if not ids then ids = {} live[dome] = ids end
			ids[farm.farm_id] = true
		end
	end)

	local cleaned = 0
	AllMapsForEach(true, "Dome", function(dome)
		local mods = dome.modifications and dome.modifications.air_consumption
		if not mods then return end
		local own = live[dome] or empty_table
		local removed_here = 0
		for i = #mods, 1, -1 do
			local id = mods[i].id
			if type(id) == "string" and string.match(id, "^Farm%d+$") and not own[id] then
				dome:SetModifier("air_consumption", id, 0, 0)
				removed_here = removed_here + 1
			end
		end
		if removed_here > 0 then
			cleaned = cleaned + removed_here
			if IsValid(dome) then dome:UpdateWorking() end
		end
	end)

	if cleaned > 0 then
		SMRFixPack.Log("GhostFarmOxygen: removed %d phantom farm oxygen modifier(s)", cleaned)
	end
end)
