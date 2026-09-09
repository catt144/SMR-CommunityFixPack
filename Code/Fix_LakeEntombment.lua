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

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Buildings/LandscapeLake.lua LandscapeLake:PlacePrefab sha256=e68c80e20d6bd932d543bca8ae97b424ed218f2d062bc6ccd8790007dce17e46
--   (Lua/Buildings/LandscapeLake.lua:270-345 at pin time)
--   our wrap target -- the seam after RebuildPassability. The defect itself is
--   stated against the scatter below
-- SRC: Lua/Buildings/ConstructionSite.lua ConstructionSite:ScatterUnitsUnderneath sha256=24e0275a6b553d4eb858b3cce00fd1fba8da3dc636d5e6395122845cfc7a8313
--   (Lua/Buildings/ConstructionSite.lua:1914-1933 at pin time)
-- DEFECT: if not u:IsKindOf\("RCConstructorBase"\) or u\.command ~= "Construct" or u\.construction_clearing ~= self then
--   the RC Constructor that built the site -- the one rover guaranteed to be
--   standing there -- is exempted from the scatter

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
