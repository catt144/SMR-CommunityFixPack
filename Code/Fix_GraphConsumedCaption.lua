-- F19: the Command Center graph caption says a resource was barely consumed
-- while the bar next to it is tall, because the caption leaves out maintenance.
--
-- Defect: the plotted series and its caption are computed from different things.
--   * the series (`Lua\ResourceTracking.lua:162`):
--         ts_resource.consumed:AddValue(
--             ro:GetConsumedByConsumptionYesterday(resource)
--           + ro:GetConsumedByMaintenanceYesterday(resource))
--   * the caption (`Lua\X\ColonyControlCenter.lua:180-188`):
--         consumed = resource_overview_obj:GetConsumedByConsumptionYesterday(id) / const.ResourceScale
-- For Machine Parts, Electronics, Metals and Polymers, maintenance IS the
-- consumption in a developed colony — consumption-by-consumption is close to
-- zero — so the number reads as almost nothing beside a full-height bar.
--
-- The two are separate accumulators on the overview
-- (`ResourceOverview.lua:156-163`), so this is not a rounding difference: the
-- caption is measuring a different quantity from the graph it labels.
--
-- Patch approach: post-wrapper (FIX_POLICY §1.4) on `City:GetColonyStatsButtons`.
-- The shipped function builds the whole descriptor table and returns it; the
-- wrapper walks that table and swaps in a corrected caption closure for exactly
-- the stockpile-resource "Produced and Consumed" panels. Nothing else in the
-- table is touched and the shipped function is untouched, so another mod that
-- adds or edits panels keeps working.
--
-- The panel is found by structure, not by position: an entry is rewritten only
-- when its second sub-panel plots `self.ts_resources[id].consumed`, which is the
-- exact series the caption is supposed to describe. If the UI is rearranged the
-- match simply fails and the fix reports itself inactive rather than relabelling
-- the wrong graph.
--
-- The replacement keeps the shipped translation (T id 8979) and its layout;
-- only the value changes. It sums the two raw accumulators and scales once,
-- which is what the plotted series does (it hands raw values to the graph with
-- `scale = const.ResourceScale`), instead of scaling one of them alone.

SMRFixPack.Register("GraphConsumedCaption", {
	title = "Command Center graph captions count maintenance, like the bars do",
	apply = function()
		local C = rawget(_G, "City")
		if type(C) ~= "table" or type(C.GetColonyStatsButtons) ~= "function" then
			return "City.GetColonyStatsButtons not found (game update changed it?)"
		end
		local RO = rawget(_G, "ResourceOverview")
		if type(RO) ~= "table" or type(RO.GetConsumedByMaintenanceYesterday) ~= "function"
			or type(RO.GetConsumedByConsumptionYesterday) ~= "function"
			or type(RO.GetProducedYesterday) ~= "function" then
			return "ResourceOverview consumption getters not found (game update changed it?)"
		end
		if type(rawget(_G, "GetCityResourceOverview")) ~= "function" then
			return "GetCityResourceOverview not found (game update changed it?)"
		end

		local matched_once = false

		local function fix_panel(city, entry)
			local id = entry.id
			local series = city.ts_resources and city.ts_resources[id]
			if not series then return end
			local panel = entry[2]
			if type(panel) ~= "table" or type(panel.caption) ~= "function" then return end
			local data = panel.data
			-- the produced/consumed panel is the one plotting this resource's
			-- consumed series; the stockpile panel above it plots .stockpile
			if type(data) ~= "table" or data[2] ~= series.consumed then return end

			matched_once = true
			local overview = GetCityResourceOverview(city)
			panel.caption = function()
				-- FIX (F19): add maintenance, so the caption describes the bar.
				local consumed = overview:GetConsumedByConsumptionYesterday(id)
					+ overview:GetConsumedByMaintenanceYesterday(id)
				return T{8979, "<graph_left>Produced</graph_left> <em>(<produced>)</em> and <graph_right>Consumed</graph_right> <em>(<consumed>)</em> (per Sol)",
					produced = overview:GetProducedYesterday(id) / const.ResourceScale,
					consumed = consumed / const.ResourceScale,
				}
			end
		end

		local orig = C.GetColonyStatsButtons
		function C:GetColonyStatsButtons(...)
			local t = orig(self, ...)
			if type(t) == "table" then
				for _, entry in ipairs(t) do
					if type(entry) == "table" and entry.id then
						fix_panel(self, entry)
					end
				end
			end
			return t
		end

		SMRFixPack.GraphConsumedCaption = { Matched = function() return matched_once end }
	end,
})
