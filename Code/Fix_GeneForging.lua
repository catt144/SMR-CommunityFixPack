-- F41: The Gene Forging tech does nothing at all.
--
-- Defect: GetRareTraitChance (Lua\Units\Colonist.lua:3541-3550 — a global
-- function, despite the tracker entry naming it as a Colonist method) knows about
-- exactly one tech:
--     if city and city.colony:IsTechResearched("GeneSelection") then
--         local def = TechDef.GeneSelection
--         rare_chance_mod = def.param1
--     end
-- `GeneForging` (Data\TechPreset.lua:1556-1564, param1 = 50, param1comment
-- "bonus chance for rare traits", description "Increases the chance that a
-- Colonist will have or gain a rare trait") appears nowhere else in the gameplay
-- code. Researching it changes nothing.
--
-- The value is a percentage bonus on the rare traits' draw weight —
-- GetRandomTrait does `rare_weight_mod = 100 + (rare_weight_mod or 0)` and passes
-- it to CalcTraitWeight (Traits.lua:1001-1022), which is why GeneSelection's 100
-- reads as "double the chance". The two techs therefore add: Gene Forging alone is
-- +50%, both together +150%. That is deliberately NOT ChoGGi's original approach
-- of bumping GeneSelection.param1 to 150, which only pays out when the OTHER tech
-- has also been researched.
--
-- Patch approach: full replacement of the global — it is six lines with the defect
-- in the middle of them, and there is no table or preset to patch instead (the
-- omission is in the code, not the data). Change marked -- FIX. TechDef entries
-- are read inside the function, not at apply time, because presets do not exist
-- while mod code loads.
--
-- Scope note: this is the "have" half. Rare traits GAINED later (schools, sanity
-- breakdowns) go through GetRandomTrait without any rare_weight_mod at all, so
-- neither tech has ever affected them; that is a separate defect and not touched
-- here.

SMRFixPack.Register("GeneForging", {
	title = "The Gene Forging tech actually increases the rare-trait chance",
	apply = function()
		if type(rawget(_G, "GetRareTraitChance")) ~= "function" then
			return "GetRareTraitChance not found (game update changed it?)"
		end

		function GetRareTraitChance(unit)
			local city = unit and unit.city or MainCity
			local rare_chance_mod

			local colony = city and city.colony
			if colony and colony:IsTechResearched("GeneSelection") then
				local def = TechDef.GeneSelection
				rare_chance_mod = (rare_chance_mod or 0) + (def and def.param1 or 0)
			end
			-- FIX (F41): Gene Forging was researched and then ignored.
			if colony and colony:IsTechResearched("GeneForging") then
				local def = TechDef.GeneForging
				rare_chance_mod = (rare_chance_mod or 0) + (def and def.param1 or 0)
			end
			return rare_chance_mod
		end
	end,
})
