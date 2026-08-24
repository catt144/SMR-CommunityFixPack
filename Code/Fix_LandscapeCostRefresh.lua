-- F105: researching a construction-cost tech throws while a landscaping
-- project is active, and the engine's blame box names this pack for it.
--
-- Defect: ConstructionSite pairs `construction_resources` with
-- `construction_costs_at_start` — the class default for both is `false`
-- (Lua\Buildings\ConstructionSite.lua:13, :32) and the ONLY writer that makes
-- them tables is ConstructionSite:GatherConstructionResources (:639-640),
-- which always creates the two together. The landscape family overrides that
-- gatherer and breaks the pair: LandscapeConstructionSite:
-- GatherConstructionResources (Lua\Landscape\LandscapeConstructionSite.lua:
-- 105-155) and ClearWasteRockConstructionSite:GatherConstructionResources
-- (ClearWasteRockConstructionSite.lua:140-177) set
-- `self.construction_resources = {}` and never touch the cost table, and
-- their state machines then park a live request under
-- `construction_resources.WasteRock` (LandscapeConstructionSite.lua:203/:216/
-- :220; ClearWasteRockConstructionSite.lua:209) which nothing ever clears.
-- ConstructionSite:RefreshConstructionResources guards on
-- `construction_resources[resource]` (:670-671) and then indexes the boolean
-- at :673 — the field-reported crash (F105, reporter log
-- Mars.exe-20260824-00.01.27: LandscapeConstructionSite, WasteRock, cost 0).
--
-- Trigger: Effect_ModifyLabel:OnApplyEffect sweeps EVERY construction site on
-- every map for any label ending `_Construction` (Lua\MarsGameEffects.lua:
-- 173-177). The shipped carriers are exactly three techs — NeoConcrete,
-- DomeStreamlining, MarsNoveau (Data\TechPreset.lua:685, :1004, :2366+).
-- Laws and story bits only LOOK like carriers: LawEffectModifyLabel and the
-- story-bit ModifyLabel call SetLabelModifier without the sweep, so they
-- cannot reach the defect (F105 entry, "trigger set").
--
-- TerrainPaintConstructionSite shares the gatherer gap (its :10-36) but never
-- keys `construction_resources`, so it cannot reach :673 today; it is guarded
-- anyway, for uniformity with its two siblings and any future reader.
--
-- Patch approach: FIX_POLICY §1.4 chained pre-wrapper on the reader. A site
-- with no recorded start costs has nothing to refresh — landscape work is
-- volume-driven (`wr_required`/`wr_produced`), its GetConstructionCost is 0
-- (the field log's locals), so skipping is the correct semantic, not merely a
-- guard. The reader shape also heals sites ALREADY saved in the broken state,
-- which initialising the gatherer could not (it runs once per site, long
-- before an old save's tech completes).
--
-- ⚠️ Installed on each LEAF class, not once on ConstructionSite: Building sets
-- `__hierarchy_cache = true` (Lua\Buildings\Building.lua:157) and
-- ConstructionSite does not, so the class builder COPIES every
-- ConstructionSite-declared method by reference into each descendant's built
-- table (CommonLua\Core\classes.lua:700-705 copy branch; the :986-988 comment
-- states the flatten/chain split). A post-ClassesBuilt wrap on
-- ConstructionSite alone is therefore never dispatched from a landscape-site
-- instance. Capturing `prev` per class keeps any other mod's per-class chain
-- intact. The same reach question for an already-shipped module is filed as
-- its own entry (F106) — not repaired here.
-- Layer: §3a layer 2 by construction — synchronous, no blocking calls, all
-- work before `return prev(self)`, no function values stored in game state.

SMRFixPack.Register("LandscapeCostRefresh", {
	title = "Researching a construction-cost tech no longer errors while a landscaping project is active",
	apply = function()
		local OVERRIDE_GONE = "the landscape GatherConstructionResources override is gone (game update changed it?)"
		local err = SMRFixPack.Require("LandscapeCostRefresh", {
			{ class = "ConstructionSite", method = "RefreshConstructionResources" },
			-- The defect premise: these three override the gatherer that pairs
			-- `construction_resources` with `construction_costs_at_start`, and
			-- none of them initialises the cost table.
			{ class = "LandscapeConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
			{ class = "ClearWasteRockConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
			{ class = "TerrainPaintConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
		})
		if err then return err end

		for _, cls in ipairs({
			"LandscapeConstructionSite",
			"ClearWasteRockConstructionSite",
			"TerrainPaintConstructionSite",
		}) do
			local C = rawget(_G, cls)
			local prev = C.RefreshConstructionResources -- the build-time copy, or another mod's chain on this class
			C.RefreshConstructionResources = function(self)
				-- FIX (F105): no start-cost record means nothing to refresh —
				-- vanilla's body would index the boolean class default at :673.
				if not self.construction_costs_at_start then return end
				return prev(self)
			end
		end
	end,
})
