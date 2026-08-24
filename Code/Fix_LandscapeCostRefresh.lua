-- F105: researching a construction-cost tech throws while a landscaping
-- project is active, and the engine's blame box names this pack for it.
--
-- Defect: ConstructionSite pairs `construction_resources` with
-- `construction_costs_at_start` — the class default for both is `false`
-- (Lua\Buildings\ConstructionSite.lua:13, :32) and the only writer that makes
-- them tables TOGETHER is ConstructionSite:GatherConstructionResources
-- (:639-640, gated at :637). The landscape family overrides that gatherer and
-- breaks the pair: LandscapeConstructionSite:GatherConstructionResources
-- (Lua\Landscape\LandscapeConstructionSite.lua:105-155) and
-- ClearWasteRockConstructionSite:GatherConstructionResources
-- (ClearWasteRockConstructionSite.lua:140-177) set
-- `self.construction_resources = {}` and never touch the cost table, and
-- their state machines then park a live request under
-- `construction_resources.WasteRock` (LandscapeConstructionSite.lua:203/:216/
-- :220; ClearWasteRockConstructionSite.lua:209) which nothing ever clears.
-- ConstructionSite:RefreshConstructionResources guards on
-- `construction_resources[resource]` (:670-671) and then indexes the boolean
-- at :673 — the field-reported crash (F105, reporter log
-- Mars.exe-20260824-00.01.27: LandscapeConstructionSite, WasteRock, cost 0).
-- (Precision, F107 audit 2026-08-24: Track.lua:651 also assigns the cost field,
-- on a track construction-group LEADER in the SafeTransport branch. That path
-- cannot reach a landscape class, so it does not widen the defect — but "the
-- ONLY writer" tree-wide was too strong and is corrected here.)
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
-- keys `construction_resources`, so it cannot reach :673 today; the wrap below
-- covers it anyway, as it covers every other descendant.
--
-- Patch approach: FIX_POLICY §1.4 chained pre-wrapper on the reader. A site
-- with no recorded start costs has nothing to refresh — landscape work is
-- volume-driven (`wr_required`/`wr_produced`), its GetConstructionCost is 0
-- (the field log's locals), so skipping is the correct semantic, not merely a
-- guard. The reader shape also heals sites ALREADY saved in the broken state,
-- which initialising the gatherer could not (it runs once per site, long
-- before an old save's tech completes).
--
-- Installed ONCE, on ConstructionSite — the class that DECLARES the method
-- (:665, the tree's single definition; no shipped subclass re-declares it).
-- The pack applies at file-load, during ModsLoadCode() (CommonLua\Core\
-- autorun.lua:423), which completes BEFORE Msg("Autorun") is raised at
-- CommonLua\Core\lib.lua:371 — so we patch the CLASSDEF and the class builder
-- copies OUR wrap down into all 13 descendants. Measured on the F106 leg
-- (`desc=13`). ⛔ An earlier revision installed on the three landscape LEAF
-- classdefs instead, on the belief that a ConstructionSite wrap could not
-- reach them; that belief was F106, measured WRONG and refuted 2026-08-24, and
-- the leaf shape it produced captured a nil `prev` on every boot (F107).
--
-- ⚠️ The widening to ordinary construction sites is a behaviour surface, and
-- the owner ruled it in (checklist 74(a)). It can only ever PREVENT an error,
-- never cause one: Gather creates both fields together (:639-640), so the only
-- state in which the guard fires on an ordinary site is the ungathered one —
-- where vanilla's own body indexes `construction_resources == false` at :670
-- and raises. Wherever vanilla succeeds, `construction_costs_at_start` is a
-- table and the guard falls straight through to `prev`. Verified at Src
-- 2026-08-24 (ConstructionSite.lua:636-684).
--
-- ⚠️ FIX_POLICY §2's "inert for a foreign object" clause: the "is this mine?"
-- test IS the field read here, because this defect is defined by OBJECT STATE,
-- not by class — no class predicate can separate a broken landscape site from
-- a healthy one. Reading one boolean-or-table field before delegating is the
-- narrowest possible test, and the paragraph above bounds what it can change.
-- Layer: §3a layer 2 by construction — synchronous, no blocking calls, all
-- work before `return prev(self)`, no function values stored in game state.

SMRFixPack.Register("LandscapeCostRefresh", {
	title = "Researching a construction-cost tech no longer errors while a landscaping project is active",
	apply = function()
		local OVERRIDE_GONE = "the landscape GatherConstructionResources override is gone (game update changed it?)"
		local err = SMRFixPack.Require("LandscapeCostRefresh", {
			-- The pair we wrap, on the class that declares it (FIX_POLICY §2).
			{ class = "ConstructionSite", method = "RefreshConstructionResources" },
			-- The defect premise: these three override the gatherer that pairs
			-- `construction_resources` with `construction_costs_at_start`, and
			-- none of them initialises the cost table.
			{ class = "LandscapeConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
			{ class = "ClearWasteRockConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
			{ class = "TerrainPaintConstructionSite", method = "GatherConstructionResources", reason = OVERRIDE_GONE },
		})
		if err then return err end

		local C = rawget(_G, "ConstructionSite")
		local prev = C.RefreshConstructionResources -- real: ConstructionSite declares it (:665)
		C.RefreshConstructionResources = function(self)
			-- FIX (F105): no start-cost record means nothing to refresh —
			-- vanilla's body would index the boolean class default at :673
			-- (or at :670, on a site that never gathered at all).
			if not self.construction_costs_at_start then return end
			return prev(self)
		end
	end,
})
