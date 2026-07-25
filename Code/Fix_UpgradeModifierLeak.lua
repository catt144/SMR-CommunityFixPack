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
-- Patch approach: full replacement of the one broken method, body modeled on the
-- adjacent correct ApplyUpgradeModifiers. (A savegame cleanup for already-leaked
-- modifiers is planned separately; this fix stops new leaks.)

SMRFixPack.Register("UpgradeModifierLeak", {
	title = "Salvaging an upgraded building now removes its dome/colony-wide upgrade bonuses",
	apply = function()
		if type(Building.StopUpgradeModifiers) ~= "function"
				or type(Building.ApplyUpgradeModifiers) ~= "function" then
			return "Building upgrade-modifier methods not found (game update changed them?)"
		end

		function Building:StopUpgradeModifiers(only_for_object)
			-- FIX: iterate the id-keyed table like ApplyUpgradeModifiers does;
			-- the shipped ipairs(self.upgrade_modifiers) iterated nothing.
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
