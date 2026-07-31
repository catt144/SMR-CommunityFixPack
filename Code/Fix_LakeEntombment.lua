-- F30: Placing an artificial lake buries the RC Constructor that built it, plus
-- any drones working the site. They read as dead.
--
-- Two-part defect:
--  (a) ConstructionSite:ScatterUnitsUnderneath (Lua\Buildings\ConstructionSite.lua:
--      1722-1737) deliberately exempts the RC Constructor that is building the site,
--      so the one rover guaranteed to be standing there is never moved.
--  (b) The scatter runs at Complete (:1574-1580) — BEFORE LandscapeLake:GameInit
--      digs the basin (LandscapeLake.lua:32-35, 215-292). Unit:ExitImpassable
--      (Units\Unit.lua:641-681) no-ops while the ground is still passable, so even
--      the units that WERE scattered can stroll back in. The terrain then drops and
--      map:RebuildPassability seals whatever is inside. Drones drain their batteries
--      and Freeze (Drone.lua:1478-1524).
-- The developers ship a partial rescue for rovers only, as a savegame fixup
-- (BaseRover.lua:736-745) — same remedy, just never applied at the moment the hole
-- appears.
--
-- Patch approach: chained post-wrapper on LandscapeLake:PlacePrefab, which is the
-- exact point after `map:RebuildPassability(bbox)` where the basin exists and
-- passability is up to date. Anything now standing on impassable ground gets the
-- game's own remedy — SetCommand("ExitImpassable"), which ends in
-- Goto(pt, "sl"), a straight-line move that ignores the terrain it is trapped by.
-- The sweep mirrors the developers' SavegameFixups.FixStuckRoversInDomes idiom
-- but covers every Unit, not just rovers. ExitImpassable self-checks
-- map:IsPassable, so a unit that turns out to be fine is left alone.

SMRFixPack.Register("LakeEntombment", {
	title = "Building an artificial lake no longer entombs the RC Constructor and drones",
	apply = function()
		local err = SMRFixPack.Require("LakeEntombment", {
			{ class = "LandscapeLake", method = "PlacePrefab" },
			{ class = "Unit", method = "ExitImpassable" },
		})
		if err then return err end
		local L = LandscapeLake

		local orig = L.PlacePrefab
		function L:PlacePrefab(...)
			local res = orig(self, ...)
			-- FIX (F30): the basin is dug and passability rebuilt by now; free
			-- anything the hole closed over.
			local map = self:GetMap()
			if map then
				map:MapForEach("map", "Unit", function(unit)
					if IsValid(unit) and not IsBeingDestructed(unit) and not unit.holder
							and unit:IsValidPos() and not map:IsPassable(unit) then
						unit:SetCommand("ExitImpassable")
					end
				end)
			end
			return res
		end
	end,
})
