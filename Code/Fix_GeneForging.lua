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
-- Patch approach: FIX_POLICY §1.4b chained POST-wrapper on the global — the two
-- techs are meant to ADD, so the shipped body keeps owning the GeneSelection term
-- and we add ours to whatever it returns. TechDef entries are read inside the
-- function, not at apply time, because presets do not exist while mod code loads.
-- Layer: §3a layer 2 — a pure arithmetic post-step on a synchronous predicate.
--
-- CONVERTED 2026-08-02 from a §1.5 full replacement (SAVE_SAFETY_REDESIGN §5.4
-- group A). Before/after: the copied six-line body is gone; the GeneSelection
-- term is vanilla's again and only the additive GeneForging term is ours.
-- Behaviour is unchanged in all four states, which is the whole table:
--   neither tech  → orig returns nil, no bonus, we return nil (NOT 0 — the old
--                   copy returned nil here too, and callers do `100 + (x or 0)`
--                   so either would work, but nil keeps the diff empty);
--   GeneSelection → orig returns its param1, no bonus, passed through unchanged;
--   GeneForging   → orig returns nil, (nil or 0) + 50 = 50, as the copy did;
--   both          → orig's 100 + 50 = 150, as the copy did (PT-29 read exactly
--                   this ladder: nil -> 50 -> 150).
-- One deliberate, documented delta: the copy added a `city.colony` nil-guard
-- that vanilla does not have, and delegating gives vanilla's unguarded index
-- back. Nothing rested on it — it was defensive hardening with no defect claim,
-- Src has no producer for a live city without a colony, and vanilla raises in
-- that state anyway.

SMRFixPack.Register("GeneForging", {
	title = "The Gene Forging tech actually increases the rare-trait chance",
	apply = function()
		local err = SMRFixPack.Require("GeneForging", {
			{ global = "GetRareTraitChance" },
		})
		if err then return err end
		local orig = GetRareTraitChance

		return SMRFixPack.SetGlobal("GetRareTraitChance", function(unit)
			local base = orig(unit)
			-- FIX (F41): Gene Forging was researched and then ignored. The two
			-- techs stack, so this is additive on top of whatever the shipped
			-- body decided about GeneSelection.
			local city = unit and unit.city or MainCity
			local colony = city and city.colony
			if colony and colony:IsTechResearched("GeneForging") then
				local def = TechDef.GeneForging
				return (base or 0) + (def and def.param1 or 0)
			end
			return base
		end, "could not install the GetRareTraitChance wrapper")
	end,
})
