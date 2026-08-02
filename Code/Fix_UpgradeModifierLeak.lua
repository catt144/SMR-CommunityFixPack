-- F03: Upgrade buffs leak permanently when a building is salvaged/demolished,
-- and stack on rebuild.
--
-- Defect: Building:StopUpgradeModifiers (Lua\Buildings\Building.lua:1268-1274)
-- iterates `self.upgrade_modifiers` with ipairs, but that table is keyed by
-- upgrade id string (see ApplyUpgrade, Building.lua:1168-1171) — ipairs over a
-- string-keyed table iterates nothing, so TurnOff() never runs. Its twin
-- ApplyUpgradeModifiers (Building.lua:1254-1266) iterates correctly with pairs
-- over upgrade_id_to_modifiers; only the Stop function kept the old flat-array
-- assumption. Call sites: Building:Done (:510) and Building:SetDome (:675).
--
-- Player impact: self-targeted modifiers die with the building object, but
-- LabelModifiers attached to OTHER containers leak forever — e.g. Medical Center /
-- Hospital "Holographic Scanner" (+30 birth comfort on the parent dome) survives
-- salvage and stacks to +60 on rebuild+re-upgrade; Ancient Artifact Interface
-- "Full System Integration" (+1 colony-wide drone carry capacity) likewise.
--
-- Patch approach: FIX_POLICY §1.4 chained POST-wrapper, and this is the shape
-- §1.4b names explicitly — THE BROKEN ORIGINAL IS A VERIFIED NO-OP, so nothing
-- has to be prevented and a post-step doing the correct work is sufficient. The
-- proof is mechanical: `self.upgrade_modifiers` is created empty in Building:Init
-- (:322) and only ever written at `self.upgrade_modifiers[id]` with a string
-- upgrade id (ApplyUpgrade, :1168-1171), so it holds no integer keys and
-- `ipairs` over it visits nothing, always.
-- We still call `orig` rather than skipping it, so that another mod's wrapper on
-- the same method stays in the chain.
-- Layer: §3a layer 2 — synchronous work on modifier objects, nothing blocking.
--
-- CONVERTED 2026-08-02 from a §1.5 full replacement (SAVE_SAFETY_REDESIGN §5.4
-- group A). Before/after: the seven-line copied body is gone; the corrective
-- `pairs` loop survives unchanged as the post-step. Behaviour is unchanged
-- because the delegated call contributes nothing (above), so the set of
-- modifiers turned off is exactly the set the old copy turned off, under the
-- same `only_for_object` filter.
-- One documented consequence of delegating: vanilla's `ipairs(self.upgrade_
-- modifiers)` would raise if that field were still the class default `false`
-- (:255). It cannot be at either call site — Building:Init creates the table and
-- both callers run on constructed buildings — and it is vanilla's own exposure,
-- carried by every unmodded game.
--
-- (A savegame cleanup for already-leaked modifiers ships separately in
-- 90_SaveSanitizer; this fix stops new leaks.)

SMRFixPack.Register("UpgradeModifierLeak", {
	title = "Salvaging an upgraded building now removes its dome/colony-wide upgrade bonuses",
	apply = function()
		local err = SMRFixPack.Require("UpgradeModifierLeak", {
			{ class = "Building", method = "StopUpgradeModifiers",
			  reason = "Building upgrade-modifier methods not found (game update changed them?)" },
			{ class = "Building", method = "ApplyUpgradeModifiers",
			  reason = "Building upgrade-modifier methods not found (game update changed them?)" },
		})
		if err then return err end
		local orig = Building.StopUpgradeModifiers

		function Building:StopUpgradeModifiers(only_for_object)
			orig(self, only_for_object)
			-- FIX (F03): the delegated body iterates the id-keyed table with
			-- ipairs and so turns nothing off. Do the sweep ApplyUpgradeModifiers
			-- does, honouring the same only_for_object filter.
			for _, modifiers in pairs(self.upgrade_id_to_modifiers or empty_table) do
				for i = 1, #modifiers do
					local modifier = modifiers[i]
					if not only_for_object or (IsKindOf(modifier, "LabelModifier") and only_for_object == modifier.container) then
						modifier:TurnOff()
					end
				end
			end
		end
	end,
})
