-- F24: when a life-support building is absorbed into a dome, the pipe
-- connections it is giving up are torn down against the DOME instead of against
-- the building.
--
-- Defect (`Lua\LifeSupportGrid.lua:282-316`): `LifeSupportGridObject:MoveInside`
-- removes the building from the outside grid and then destroys each connection
-- it had:
--     WaterGrid.DestroyConnection(pt, other_pt, dome, adjacents[i])
-- The signature is `DestroyConnection(pt1, pt2, building1, building2, test)`
-- (`:157-161`), and `building1` is the owner of `pt1` — the building that is
-- moving. Its electricity twin gets this right:
--     ElectricityGrid.DestroyConnection(pt, other_pt, self, others[i])
-- (`Lua\ElectricityGrid.lua:285-293`), in an otherwise line-for-line identical
-- loop. So the moving building is never told its own connection at `pt` is
-- gone, and the dome is told about a hex it does not own. Stale plugs and
-- connection visuals are left behind, and the sweep that runs from
-- `Dome:OnLoad` (`Dome.lua:896-899`) re-runs the same path on every load.
--
-- Sibling-code evidence is the whole case here (FIX_POLICY §4): the same author
-- wrote the same loop correctly one file over, and `dome` is simply the nearest
-- variable in scope to `self`.
--
-- Patch approach: full replacement of `LifeSupportGridObject:MoveInside` — a
-- copy of LifeSupportGrid.lua:282-316 (shipped Src, 2026-07) with one argument
-- corrected, marked -- FIX. Replacement because the call is inside a loop in the
-- middle of the function: there is no wrapper position that can reach it, and
-- `WaterGrid.DestroyConnection` cannot be patched instead because a wrapper
-- there has no way to know which caller handed it the wrong owner.
--
-- The shipped `assert(IsKindOf(dome, "Dome"))` is dropped from the copy: asserts
-- do not unwind in this engine, so it is a log line rather than a guard, and the
-- statements after it already require a real dome.

SMRFixPack.Register("DomePipeMoveInside", {
	title = "Pipe connections are cleaned up correctly when a dome absorbs a building",
	apply = function()
		local L = rawget(_G, "LifeSupportGridObject")
		if type(L) ~= "table" or type(L.MoveInside) ~= "function" then
			return "LifeSupportGridObject.MoveInside not found (game update changed it?)"
		end
		local W = rawget(_G, "WaterGrid")
		if type(W) ~= "table" or type(W.DestroyConnection) ~= "function" then
			return "WaterGrid.DestroyConnection not found (game update changed it?)"
		end
		for _, name in ipairs({ "ApplyIDToOverlayGrid", "SupplyGridRemoveBuilding",
			"GetObjectHexGrid", "GetGrid", "Building" }) do
			if rawget(_G, name) == nil then
				return name .. " not found (game update changed it?)"
			end
		end

		function L:MoveInside(dome)
			Building.MoveInside(self, dome)

			local grid = self.water.grid
			grid:RemoveElement(self.water)

			local map = self:GetMap()
			local supply_connection_grid = map.supply_connection_grid
			local supply_overlay_grid = map.supply_overlay_grid

			local ls_connection_grid = supply_connection_grid["water"]
			local shape = self:GetSupplyGridConnectionShapePoints("water")
			ApplyIDToOverlayGrid(supply_overlay_grid, self, shape, 15, "band")
			local connections = SupplyGridRemoveBuilding(ls_connection_grid, self, shape)
			local object_hex_grid = GetObjectHexGrid(self)
			-- destroy connections
			for i = 1, #connections, 2 do
				local pt, other_pt = connections[i], connections[i + 1]
				local adjacents = object_hex_grid:GetObjectsAtPos(other_pt, nil, nil, function(o)
					return GetGrid(o, "water") == grid
				end)
				for i = 1, #adjacents do
					-- FIX (F24): `pt` belongs to this building, not to the dome —
					-- the electricity twin passes `self` here (ElectricityGrid.lua:291).
					WaterGrid.DestroyConnection(pt, other_pt, self, adjacents[i])
				end
			end

			if #grid.elements <= 0 then
				grid:delete()
			end
			self.water.parent_dome = dome
			dome:AddToLabel("SupplyGridBuildings", self)
			local my_ls_grid = dome.water.grid
			my_ls_grid:AddElement(self.water)
		end
	end,
})
