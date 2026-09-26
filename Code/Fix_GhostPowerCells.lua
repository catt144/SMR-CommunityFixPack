-- C119: Remove saved electricity connection cells with no power object on their
-- hex. Run after the shipped load fixups, on every loaded map. This repairs the
-- saved state; it does not prevent a new failed connection later in the session.
--
-- Save safety: synchronous PostLoadGame work only. No mod fields, functions,
-- classes, or threads are stored in the save. The remaining grid state is native.
-- Pinned against shipped game 1.1.1.405907.
-- SRC: Lua/SupplyGrid.lua SupplyGridObject:SupplyGridConnectElement sha256=6de15a9e3c301c5760a99b596c9fb730e7a75a5ef404fca64a9bbb27c93b6854
-- DEFECT: local adjacent_element = adjacent\[supply_resource\]
-- SRC: Lua/SupplyGrid.lua SupplyGridObject:SupplyGridDisconnectElement sha256=235e37ca16ad071b4342837ab4a179952ed278a36af655e6fb8a0cf42aac921a
-- DEFECT: if not grid then\s*return
-- SRC: Lua/GridTunnelConnector.lua L1-1 sha256=ecc0a72d6af892732cd6ea44e8fbb25f4d7b228f6e7412d19ad9b0483b71acde
-- Dependency pin: TunnelMask is file-local and must remain 32768; this line
-- states an expected signature, not a defect in the game.

local FIX_ID = "GhostPowerCells"
local TUNNEL_MASK = 32768
local log = SMRFixPack.Log

local function power_owner(obj)
	return obj.electricity
end

local function live_power_object(obj)
	return IsValid(obj) and not IsBeingDestructed(obj) and obj.electricity
end

-- The Excavator and Open Farm have special power shapes that may reach outside
-- their ordinary object-hex-grid footprint. Protect cells using the shape passed to
-- SupplyGridApplyBuilding, transformed as GridObject does for grid positions.
local function protect_shape(protected, width, height, obj)
	if not live_power_object(obj) then return end
	local shape = obj:GetSupplyGridConnectionShapePoints("electricity")
	local q0, r0 = WorldToHex(obj)
	local direction = HexAngleToDirection(obj)
	for i = 1, #shape do
		local dq, dr = HexRotate(shape[i]:x(), shape[i]:y(), direction)
		local q, r = q0 + dq, r0 + dr
		if q >= 0 and q < width and r >= 0 and r < height then
			protected[r * width + q] = true
		end
	end
end

local function make_protected_set(map, width, height)
	local protected = {}
	if type(rawget(_G, "TheExcavatorBase")) == "table" then
		map:MapForEach("map", "TheExcavatorBase", function(obj)
			protect_shape(protected, width, height, obj)
		end)
	end
	if type(rawget(_G, "OpenFarmBase")) == "table" then
		map:MapForEach("map", "OpenFarmBase", function(obj)
			protect_shape(protected, width, height, obj)
		end)
	end
	return protected
end

local function scan_map(map, counts)
	local object_grid = map.object_hex_grid
	local supply = map.supply_connection_grid
	local conn_grid = supply and supply.electricity
	if not object_grid or not conn_grid then return end

	-- Complete protection before the first write. A malformed live shape leaves
	-- the whole map untouched rather than risking the owner's power cells.
	local width, height = object_grid:size()
	local protected = make_protected_set(map, width, height)
	for r = 0, height - 1 do
		for q = 0, width - 1 do
			local cell = HexGridGet(conn_grid, q, r)
			if cell ~= 0 then
				if band(cell, TUNNEL_MASK) ~= 0 then
					counts.tunnel_skipped = counts.tunnel_skipped + 1
				elseif protected[r * width + q] then
					counts.shape_protected = counts.shape_protected + 1
				elseif not HexGridGetObject(object_grid, q, r, nil, nil, power_owner) then
					HexGridSet(conn_grid, q, r, 0)
					counts.cleared = counts.cleared + 1
				end
			end
		end
	end
	counts.maps = counts.maps + 1
	return true
end

local function built_passage_ready(obj)
	local endpoints = obj.domes_connected
	local constructing = obj.elements_under_construction
	local shapes = obj.shape_points
	local connections = obj.shape_connections
	return type(endpoints) == "table" and IsValid(endpoints[1]) and IsValid(endpoints[2])
		and type(constructing) == "table" and #constructing == 0
		and obj.supply_tunnel_set == true
		and type(shapes) == "table" and type(shapes.electricity) == "table"
		and type(connections) == "table" and type(connections.electricity) == "table"
		and obj.water and obj.water.grid
end

local function retry_one(obj, element)
	if IsKindOf(obj, "PassageBase") then
		if type(obj.elements_under_construction) == "table"
			and #obj.elements_under_construction > 0 then return "unbuilt" end
		if not built_passage_ready(obj) then return false end
		-- PassageBase's instance method is empty. The vendor route suppresses
		-- dome membership and forces physical connections, then also touches
		-- water and tunnels. Only repeat its electricity call here.
		local parent_dome = obj.parent_dome
		obj.parent_dome = false
		local ok = pcall(SupplyGridObject.SupplyGridConnectElement,
			obj, element, ElectricityGrid, nil, "force")
		obj.parent_dome = parent_dome
		return ok and element.grid and true or false
	end
	local ok = pcall(SupplyGridObject.SupplyGridConnectElement,
		obj, element, ElectricityGrid)
	return ok and element.grid and true or false
end

local function repair()
	local started = RealTime()
	local counts = {
		maps = 0, cleared = 0, tunnel_skipped = 0, shape_protected = 0,
		reconnected = 0, retry_failed = 0, unbuilt_skipped = 0, map_failed = 0,
	}
	local maps = rawget(_G, "LoadedMaps")
	if type(maps) == "table" then
		local ready_maps = {}
		for _, map in ipairs(maps) do
			local ok, scanned = pcall(scan_map, map, counts)
			if ok and scanned then
				ready_maps[#ready_maps + 1] = map
			elseif not ok then
				counts.map_failed = counts.map_failed + 1
			end
		end

		-- Collect first. Connections can create/merge grids during the retry.
		local pending = {}
		for _, map in ipairs(ready_maps) do
			local on_map = {}
			local ok = pcall(function()
				map:MapForEach("map", "SupplyGridObject", function(obj)
					if live_power_object(obj) and obj.electricity.grid == false then
						on_map[#on_map + 1] = {obj, obj.electricity}
					end
				end)
			end)
			if ok then
				for i = 1, #on_map do pending[#pending + 1] = on_map[i] end
			else
				counts.map_failed = counts.map_failed + 1
			end
		end
		for i = 1, #pending do
			local obj, element = pending[i][1], pending[i][2]
			if live_power_object(obj) and obj.electricity == element and element.grid == false then
				local ok, outcome = pcall(retry_one, obj, element)
				if ok and outcome == true then
					counts.reconnected = counts.reconnected + 1
				elseif ok and outcome == "unbuilt" then
					counts.unbuilt_skipped = counts.unbuilt_skipped + 1
				else
					counts.retry_failed = counts.retry_failed + 1
				end
			end
		end
	end
	log("%s: maps=%d cleared=%d tunnel_skipped=%d shape_protected=%d reconnected=%d retry_failed=%d unbuilt_skipped=%d map_failed=%d elapsed_ms=%d",
		FIX_ID, counts.maps, counts.cleared, counts.tunnel_skipped,
		counts.shape_protected, counts.reconnected, counts.retry_failed,
		counts.unbuilt_skipped, counts.map_failed, RealTime() - started)
	return counts
end

SMRFixPack.Register(FIX_ID, {
	title = "Clear stale power connection cells after loading",
	apply = function()
		return SMRFixPack.Require(FIX_ID, {
			{ class = "SupplyGridObject", method = "SupplyGridConnectElement" },
			{ test = function()
				local C = rawget(_G, "TheExcavatorBase")
				return C == nil or type(C.GetSupplyGridConnectionShapePoints) == "function"
			end, reason = "Excavator power connection shape changed" },
			{ test = function()
				local C = rawget(_G, "OpenFarmBase")
				return C == nil or type(C.GetSupplyGridConnectionShapePoints) == "function"
			end, reason = "Open Farm power connection shape changed" },
			{ global = "HexGridGet" },
			{ global = "HexGridSet" },
			{ global = "HexGridGetObject" },
			{ global = "HexRotate" },
			{ global = "HexAngleToDirection" },
			{ global = "WorldToHex" },
			{ global = "RealTime" },
			{ global = "band" },
		})
	end,
})

-- The same guarded entry point is callable by TestKit after a fixture load.
SMRFixPack.RunGhostPowerCells = SMRFixPack.WhenActive(FIX_ID, repair)
OnMsg.PostLoadGame = SMRFixPack.RunGhostPowerCells
