-- C116: a passage_hub marker can survive departure from the physical hub.
-- Observe synchronous movement and holder transitions; clear only after both
-- logical and visual positions leave the marked hub, then let native outside
-- computation see the corrected holder and marker.
-- No game-time thread or stored function (§3a layer 3). Existing-save markers
-- heal on the next movement/holder transition; no load-time sweep is installed.
--
-- MANIFEST (FIX_POLICY §2b), archived game build 1.1.1.405907.
-- SRC: Lua/Passage.lua PassageBase:TraverseTunnel sha256=33f432f96c8e5b29944b9b2fbf92766de644873f7ea01cb968b080cbebd114c3
-- DEFECT: unit\.passage_hub\s*=\s*nil

SMRFixPack.Register("HubMarkerDeparture", {
	title = "Clear a hub marker after physical departure",
	apply = function()
		local err = SMRFixPack.Require("HubMarkerDeparture", {
			{ class = "Unit", method = "Step" },
			{ class = "Colonist", method = "StopMoving" },
			{ class = "Colonist", method = "SetHolderOnMap" },
			{ class = "PassageHubBase" },
			{ global = "IsValid" },
			{ global = "IsKindOf" },
			{ global = "ResolveMap" },
			{ global = "WorldToHex" },
			{ global = "HexGridGetObject" },
			{ path = { "SMRFixPack", "OnHubNow" }, kind = "function" },
			{ test = function()
				return Unit.passage_hub == false and PassageHubBase.hub_domes == false
			end, reason = "hub marker or hub layout changed" },
		})
		if err then return err end

		local on_hub = SMRFixPack.OnHubNow
		local function departed(unit)
			local hub = unit.passage_hub
			if not IsValid(hub) or not IsKindOf(hub, "PassageHubBase")
				or not IsValid(unit) or not unit:IsValidPos()
				or ResolveMap(unit) ~= ResolveMap(hub) then
				return false
			end
			-- A traversal may cross a dome hex while still protected by its
			-- passage. An uncertain live traversal also keeps shelter.
			if IsValid(unit.traversing_passage) or on_hub(unit, hub) then return false end
			local map = hub:GetMap()
			if not map or not map.object_hex_grid then return false end
			local logical_q, logical_r = WorldToHex(unit)
			if HexGridGetObject(map.object_hex_grid, logical_q, logical_r, "PassageHub") == hub then
				return false
			end
			-- pf.Step may advance the logical position one step ahead of the
			-- model. Do not strip shelter while the model is still on the hub.
			local x, y = unit:GetVisualPosXYZ()
			if not x or not y then return false end
			local visual_q, visual_r = WorldToHex(x, y)
			return HexGridGetObject(map.object_hex_grid, visual_q, visual_r, "PassageHub") ~= hub
		end

		local function repair(unit)
			if not departed(unit) then return end
			local hub = unit.passage_hub
			unit.passage_hub = false
			-- A stale hub holder suppresses native outside effects and dome
			-- detection even after the marker is cleared (Unit.lua:468-470,
			-- Dome.lua:159-165). Use the native holder bookkeeping.
			if unit.holder == hub then unit:SetHolder(false) end
			unit:UpdateOutside()
		end

		local native_step = Unit.Step
		function Unit:Step(...)
			if not IsKindOf(self, "Colonist") then return native_step(self, ...) end
			if not IsValid(self.passage_hub) then return native_step(self, ...) end
			local result = table.pack(native_step(self, ...))
			repair(self)
			return table.unpack(result, 1, result.n)
		end

		local native_stop = Colonist.StopMoving
		function Colonist:StopMoving(...)
			if not IsKindOf(self, "Colonist") then return native_stop(self, ...) end
			repair(self)
			return native_stop(self, ...)
		end

		local native_holder = Colonist.SetHolderOnMap
		function Colonist:SetHolderOnMap(...)
			if not IsKindOf(self, "Colonist") then return native_holder(self, ...) end
			local result = table.pack(native_holder(self, ...))
			repair(self)
			return table.unpack(result, 1, result.n)
		end
	end,
})
