-- C114: a colonist physically on a live hub or its passage can reach a
-- connected dome even when the centre-based outside radius says otherwise.
-- Native true results and hypothetical home-relative queries stay native.
-- Synchronous result widening: no saved function frame or state (§3a layer 3).
--
-- MANIFEST (FIX_POLICY §2b), archived game build 1.1.1.405907.
-- SRC: Lua/Units/ColonistTransport.lua Colonist:HasLocalAccess sha256=3249abc15338e94695a7afe6336c9f065f9d93dd6a9cc84574b16aad0edd3e24
-- DEFECT: return\s+g_Consts\.DefaultOutsideWorkplacesRadius\s*>=\s*HexAxialDistance\(to_check,\s*destination\)

SMRFixPack.Register("HubLocalAccess", {
	title = "Let colonists on hub passages reach connected domes",
	apply = function()
		local err = SMRFixPack.Require("HubLocalAccess", {
			{ class = "Colonist", method = "HasLocalAccess" },
			{ class = "PassageHubBase" },
			{ class = "Dome" },
			{ global = "IsValid" },
			{ global = "IsKindOf" },
			{ global = "ResolveMap" },
			{ global = "IsBeingDestructed" },
			{ path = { "SMRFixPack", "OnHubNow" }, kind = "function" },
			-- The hub and network fields distinguish the branch this wrapper uses.
			{ test = function()
				return PassageHubBase.hub_domes == false and Dome.dome_network == false
			end, reason = "hub or dome network layout changed" },
		})
		if err then return err end

		local on_hub = SMRFixPack.OnHubNow
		local native = Colonist.HasLocalAccess
		local function current_hub(unit)
			local passage = unit.traversing_passage
			if IsValid(passage) then
				local hub = passage.hub_draining
				if on_hub(unit, hub) then return hub end
				local ends = passage.domes_connected
				if type(ends) == "table" then
					if on_hub(unit, ends[1]) then return ends[1] end
					if on_hub(unit, ends[2]) then return ends[2] end
				end
				return false
			end
			local hub = unit.holder
			if on_hub(unit, hub) then return hub end
			hub = unit.passage_hub
			if on_hub(unit, hub) then return hub end
			return false
		end

		function Colonist:HasLocalAccess(destination, dome, ...)
			local result = table.pack(native(self, destination, dome, ...))
			if result[1] then return table.unpack(result, 1, result.n) end
			if not IsKindOf(self, "Colonist") or dome or not IsValid(destination) then
				return table.unpack(result, 1, result.n)
			end
			local target = IsKindOf(destination, "Dome") and destination
				or IsKindOf(destination, "Building") and destination.parent_dome
			if not IsValid(target) or not IsKindOf(target, "Dome")
				or IsBeingDestructed(target) then
				return table.unpack(result, 1, result.n)
			end
			local map = ResolveMap(self)
			if not map or map ~= ResolveMap(destination) or map ~= ResolveMap(target) then
				return table.unpack(result, 1, result.n)
			end
			local hub = current_hub(self)
			if not hub then return table.unpack(result, 1, result.n) end
			local attached = hub.hub_domes
			if type(attached) ~= "table" then return table.unpack(result, 1, result.n) end
		for _, source_dome in ipairs(attached) do
			local links = attached[source_dome]
			if type(links) == "number" and links > 0
					and IsValid(source_dome) and IsKindOf(source_dome, "Dome")
					and not IsBeingDestructed(source_dome)
					and type(source_dome.dome_network) == "table"
					and source_dome.dome_network[target] then
					return true
				end
			end
			return table.unpack(result, 1, result.n)
		end
	end,
})
