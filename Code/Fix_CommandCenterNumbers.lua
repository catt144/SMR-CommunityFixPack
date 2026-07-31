-- F13: The Command Center's resource rows show a label and no number.
--
-- Defect: the resource rows of the Command Center overview render tags of the form
--     "<metals(AvailableMetals)>"   (Data\XDef\CommandCenterCategories.lua:226-328
--                                    and its generated twin)
-- which resolve `AvailableMetals` as a property/getter on the ResourceOverview
-- context — i.e. ResourceOverview:GetAvailableMetals(). Eleven such getters
-- (Metals, Concrete, Food, PreciousMetals, Polymers, MachineParts, Fuel,
-- Electronics, Seeds, PreciousMinerals, WasteRock) simply do not exist: the
-- remaster refactored them into the single parameterised
-- ResourceOverview:GetAvailable(resource_type) (ResourceOverview.lua:143-145) and
-- other call sites were converted, but this preset was missed. Only the two
-- surviving specific getters, GetAvailableRockets and GetAvailablePods (:335, :347),
-- still render. A nil value makes FormatResource produce nothing, so the player
-- sees empty resource rows.
--
-- Patch approach: define the eleven missing getters as one-line shims delegating to
-- GetAvailable. This is a pure addition — no shipped function is replaced, no
-- preset is touched, and any mod that later defines its own version simply
-- overwrites ours. We never overwrite a getter that already exists, so a game
-- hotfix that adds the real ones wins and this fix reports itself inactive.

SMRFixPack.Register("CommandCenterNumbers", {
	title = "Command Center resource rows show their numbers again",
	apply = function()
		local err = SMRFixPack.Require("CommandCenterNumbers", {
			{ class = "ResourceOverview", method = "GetAvailable" },
		})
		if err then return err end
		local RO = ResourceOverview

		-- exactly the tags used by Data\XDef\CommandCenterCategories.lua
		local resources = {
			"Metals", "Concrete", "Food", "PreciousMetals", "Polymers", "MachineParts",
			"Fuel", "Electronics", "Seeds", "PreciousMinerals", "WasteRock",
		}
		local added = 0
		for _, res in ipairs(resources) do
			local name = "GetAvailable" .. res
			if RO[name] == nil then -- FIX (F13): the remaster dropped these getters
				RO[name] = function(self) return self:GetAvailable(res) end
				added = added + 1
			end
		end
		if added == 0 then
			return "all 11 Available* getters already exist (game update fixed it?)"
		end
	end,
})
