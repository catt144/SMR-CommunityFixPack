-- C117: a busy hub passage with another exit disconnects before its current
-- traversers arrive. Disconnect clears the endpoint on the passage element,
-- so native TraverseTunnel otherwise leaves a hub-bound colonist outside.
--
-- Keep native OnDemolish's pre-disconnect wait alive for current traversers,
-- and refuse fresh tunnel entries only while a usable sibling remains. A
-- refused entry returns false to Unit:TraverseTunnel, which clears its path.
-- The last usable exit remains open to traffic under the native safety wait.
-- Cancellation clears hub_draining in native OnSetDemolishing. Save/reload
-- carries only native demolition and traversal state; this module adds none.
--
-- Save/removal (FIX_POLICY §3a): layer 3 for the synchronous wait predicate;
-- layer 2 for traversal, whose non-refused calls tail-delegate to native code.
-- Neither wrapper creates a thread or waits. A saved native demolition wait
-- resumes through the installed predicate after reload; removing the mod
-- restores the shipped predicate and its C117 race for later demolition.
--
-- MANIFEST (FIX_POLICY §2b), archived game build 1.1.1.405907.
-- SRC: Lua/Passage.lua PassageBase:WouldStrandHubColonists sha256=89ae540a00480cf20295fcf48615be5166d312f6be29712a16e6d972a9a1b27b
-- DEFECT: if\s+passage\s*~=\s*self\s+and\s+passage:IsPFTunnelActive\(\)\s+then
-- SRC: Lua/Passage.lua PassageBase:TraverseTunnel sha256=33f432f96c8e5b29944b9b2fbf92766de644873f7ea01cb968b080cbebd114c3
-- DEFECT: local\s+exit_building\s*=\s*element\.is_pf_tunnel

SMRFixPack.Register("PassageHubSalvageDrain", {
	title = "Let hub passage traversers arrive before salvage disconnects",
	apply = function()
		local err = SMRFixPack.Require("PassageHubSalvageDrain", {
			{ class = "PassageBase", method = "WouldStrandHubColonists" },
			{ class = "PassageBase", method = "TraverseTunnel" },
			{ class = "PassageBase", method = "IsPFTunnelActive" },
			{ global = "IsKindOf" },
			{ global = "IsValid" },
			{ test = function()
				return PassageBase.hub_draining == false
					and PassageBase.traversing_colonists == false
			end, reason = "passage drain fields changed" },
			-- The shipped predicate is synchronous and reads only the stub's
			-- GetConnectedHub and a sibling's IsPFTunnelActive on this early path.
			{ probe = function()
				local sibling = { IsPFTunnelActive = function() return true end }
				local hub = { connected_passages = { [sibling] = true } }
				local stub = { GetConnectedHub = function() return hub end }
				return PassageBase.WouldStrandHubColonists(stub) == false
			end, reason = "hub sibling shortcut changed" },
		})
		if err then return err end

		local function usable_sibling(self, hub)
			local connections = hub.connected_passages
			if type(connections) ~= "table" then return false end
			for passage in pairs(connections) do
				if passage ~= self and IsValid(passage) and not passage.demolishing
					and not passage.hub_draining and passage:IsPFTunnelActive() then
					return true
				end
			end
			return false
		end

		local native_wait = PassageBase.WouldStrandHubColonists
		function PassageBase:WouldStrandHubColonists(...)
			if not IsKindOf(self, "PassageBase") then return native_wait(self, ...) end
			if IsValid(self.hub_draining) and self.demolishing
				and #self.traversing_colonists > 0 then
				return true
			end
			return native_wait(self, ...)
		end

		local native_traverse = PassageBase.TraverseTunnel
		function PassageBase:TraverseTunnel(unit, end_point, end_point_map, param, element)
			if not IsKindOf(self, "PassageBase") then
				return native_traverse(self, unit, end_point, end_point_map, param, element)
			end
			local hub = self.hub_draining
			if IsValid(hub) and self.demolishing and usable_sibling(self, hub) then
				return false
			end
			return native_traverse(self, unit, end_point, end_point_map, param, element)
		end
	end,
})
