-- Shared physical occupancy test for C114 and C116 (archived 1.1.1.405907).
-- A live traversal is proved by both passage state and hub connectivity.
-- Otherwise a hub field only corroborates the unit's current hub hex.
-- Synchronous, with no persisted state or blocking frame (FIX_POLICY §3a layer 3).
-- SRC: none shared predicate derives from Passage.lua:1205-1239 and the hub hex grid

function SMRFixPack.OnHubNow(unit, hub)
	if not IsValid(unit) or not IsValid(hub)
		or not IsKindOf(hub, "PassageHubBase") or hub.demolishing
		or not unit:IsValidPos() then
		return false
	end
	local map = ResolveMap(unit)
	if not map or map ~= ResolveMap(hub) then return false end

	local passage = unit.traversing_passage
	if IsValid(passage) then
		local connected = type(hub.connected_passages) == "table" and hub.connected_passages[passage]
		local draining = type(hub.draining_passages) == "table" and hub.draining_passages[passage]
		return (connected or draining)
			and type(passage.traversing_colonists) == "table"
			and table.find(passage.traversing_colonists, unit) ~= nil or false
	end

	if unit.holder ~= hub and unit.passage_hub ~= hub then return false end
	map = hub:GetMap()
	if not map or not map.object_hex_grid then return false end
	local q, r = WorldToHex(unit)
	return HexGridGetObject(map.object_hex_grid, q, r, "PassageHub") == hub
end
