-- F43: a layout-construction preset places its buildings without checking that
-- the player has researched them.
--
-- Defect: `LayoutConstructionController:Activate`
-- (Lua\Construction\LayoutConstruction.lua:231-252) decides per entry whether to
-- include it:
--     local tech_shown, tech_enabled, tech_rollover = GetBuildingTechsStatus(template_name, template.build_category)
--     available_prefabs = prefab_counters[entry.template] or ColonyGetPrefabs(template_name, self.city)
--     local prefab_item = template.require_prefab and GetResupplyItem(template_name)
--     local require_prefab = not tech_enabled and prefab_item and not prefab_item.locked
--     add = not require_prefab or (not not self.prefab)
-- `tech_enabled` is computed and then only ever consulted through
-- `require_prefab`, which describes one narrow case: "locked, but purchasable as
-- a resupply prefab". A building that is tech-locked and has NO usable resupply
-- item makes `prefab_item` false, so `require_prefab` is false, so
-- `add = not false = true` — the entry is added and its sub-controller placed
-- with no research gate at all. Outside layouts the tech gate is the build menu
-- (`GetBuildingTechsStatus`, X\BuildMenu.lua:321-356); a layout entry never
-- passes through it, so nothing else catches this.
--
-- The surrounding logic shows the intent: the author's rule is "do not hand out
-- a building the player would otherwise have to buy, unless this layout IS the
-- prefab package" (`add = not require_prefab or self.prefab`), and owned prefabs
-- re-enable an entry a moment later (:244-248). A building the player cannot
-- obtain by ANY route simply has no branch — it falls through the `or` into
-- `true`.
--
-- Reachability, stated plainly: **this is latent in the shipped game.** Exactly
-- one layout ships — `SelfSufficientDome` (Data\LayoutConstruction.lua:3-54,
-- referenced by Data\BuildingTemplate\SelfSufficientDome.lua:16) — and none of
-- its entries (DomeBasic, MOXIE, OxygenTank, MoistureVaporator, WaterTank,
-- StorageFood, life_support_grid) carries a tech requirement, so no vanilla
-- layout can reach the hole. It is fixed for the same reason F27 and F29 are:
-- the next layout, from a mod or a future update, would inherit it. On the
-- shipped data this fix is a provable no-op.
--
-- Patch approach: a chained post-wrapper on `Activate` (FIX_POLICY §1.4) rather
-- than a replacement of that 70-line function — the shipped loop already records
-- everything the decision needs, so the wrapper can re-read its own results:
--   * `self.prefab_items[entry]` is set whenever the colony owns a prefab for
--     that entry (:244-246), which is the "you may place it anyway" case, so the
--     stateful `prefab_counters` handout does not have to be re-derived;
--   * `self.prefab` marks the layout itself as a prefab package;
--   * `self.skip_items[entry]` marks what the shipped code already dropped.
-- Anything left that is tech-locked with none of those excuses is torn down the
-- same way `LayoutConstructionController:Deactivate` (:310-317) tears a
-- controller down, and marked in `skip_items` — which is exactly what
-- `PlaceCursors` (:341-342) consults before placing anything.
--
-- Deliberately unchanged: `GetLayoutConstructionBuildingCost` (:469-491) and the
-- description builder (:570-584) both walk the whole preset and already ignore
-- `skip_items` for the shipped prefab skip too. Matching that pre-existing
-- behaviour keeps this fix to the placement rule alone (FIX_POLICY §4).

SMRFixPack.Register("LayoutTechLock", {
	title = "Layout construction respects research locks",
	apply = function()
		local L = rawget(_G, "LayoutConstructionController")
		if type(L) ~= "table" or type(L.Activate) ~= "function" then
			return "LayoutConstructionController.Activate not found (game update changed it?)"
		end
		if type(rawget(_G, "GetBuildingTechsStatus")) ~= "function" then
			return "GetBuildingTechsStatus not found (game update changed it?)"
		end
		if type(rawget(_G, "BuildingTemplates")) ~= "table" then
			return "BuildingTemplates not found (game update changed it?)"
		end

		-- Should this entry never have been added? Mirrors the shipped decision at
		-- LayoutConstruction.lua:236-248, reading the state that loop recorded.
		-- Never raises: it runs over live UI state.
		local function is_locked_out(controller, entry)
			if type(entry) ~= "table" then return false end
			if controller.prefab then return false end            -- the layout IS the prefab package
			if (controller.prefab_items or empty_table)[entry] then return false end -- an owned prefab covers it
			local template = BuildingTemplates[entry.template]
			if type(template) ~= "table" then return false end    -- grid entries have no template
			local _, tech_enabled = GetBuildingTechsStatus(template.class, template.build_category)
			return not tech_enabled
		end

		SMRFixPack.LayoutTechLock = { IsLockedOut = is_locked_out }

		local orig_activate = L.Activate
		function L:Activate(template, params, ...)
			local res = orig_activate(self, template, params, ...)

			local controllers = self.controllers
			if type(controllers) ~= "table" or type(self.skip_items) ~= "table" then
				return res
			end
			for entry, controller in pairs(controllers) do
				local ok, locked = pcall(is_locked_out, self, entry)
				if ok and locked then
					self.skip_items[entry] = true
					controllers[entry] = nil
					-- same teardown as LayoutConstructionController:Deactivate.
					-- FIX (QA 2026-07-25): no IsValid() here — sub-controllers are
					-- pure-Lua InitDone objects and the C-side IsValid rejects
					-- non-CObjects (cf. RealTimeCommandObject's own override,
					-- CommandObject.lua:101-114), so the guard made this teardown
					-- unreachable and leaked the controller + its cursor object.
					-- The shipped teardown (LayoutConstruction.lua:310-317) has no
					-- such guard.
					if controller then
						pcall(controller.Deactivate, controller)
						if controller.is_grid_controller then
							pcall(controller.Deactivate, controller)
						end
						DoneObject(controller)
					end
				end
			end
			return res
		end
	end,
})
