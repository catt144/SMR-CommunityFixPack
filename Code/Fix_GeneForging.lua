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
--
-- ===== 2026-09-09 · AUGMENT A-1 (1.1.0 re-verification §1c) ==================
-- The module WORKED (K-4) and still does; this changes where it reads two
-- values from, and nothing else. Both reads now go through the shipped body's
-- OWN route on whichever branch is running.
--
-- 1 · THE VALUE. We read `TechDef.GeneForging.param1` — the LEGACY stub map.
--     1.1.0 moved the tech data: `Data/Tech.lua` places `Tech` objects whose
--     value lives in a `Parameters` list, read as
--     `Techs.<id>:ResolveValue("param1")`, and that is exactly what the
--     shipped body does for GeneSelection one line above our term
--     (`Colonist.lua:4399-4400`). `Data/TechPreset.lua` survives as the
--     `TechDef` map and still carries `GeneForging param1 = 50`, so nothing is
--     broken TODAY — but MEASURED 2026-09-09: `TechDef` has exactly ONE
--     mention left in the whole shipped tree, the `GlobalMap = "TechDef"`
--     declaration itself (`ClassDef-PresetDefs.generated.lua:1730`). Zero
--     readers. This module is the last consumer of a map the game abandoned,
--     and a patch that empties the stubs (R-32 shows one already is) would
--     silently zero our bonus with every self-check still green.
--     ⇒ prefer `Techs`, fall back to `TechDef`.
--
-- 2 · THE TECH TEST. We resolved a city and asked `city.colony`. Both branches
--     ship a GLOBAL `IsTechResearched(tech_id)` and each defines it in terms
--     of ITS OWN idea of the researching party — 1.0.7
--     `UIColony:IsTechResearched` (`Tech.lua:466`), 1.1.0
--     `GetTechState(tech_id, UIPlayer) == "researched"` (`Tech.lua:468`) —
--     and 1.1.0's shipped body uses it for the GeneSelection term. Asking the
--     branch's own question is strictly better than hand-rolling one that can
--     drift from vanilla's half of the same sum.
--
-- ⛔ THIS MODULE MUST NOT DECLINE ON 1.0.7, so it gets no branch guard, and
-- that is the ck118 rule applied rather than skipped: the guard is owed by a
-- module that CARRIES a 1.1.0 body. This one carries none — it delegates to
-- `orig` and its value read is dual-branch BY CONSTRUCTION. Verified against
-- the archived 1.0.7 tree (`EF-075`), which is why the fallback is not
-- decoration:
--     1.1.0  `Techs.GeneForging:ResolveValue("param1")` -> 50 (Parameters
--            list; class `Tech` declares no `param1` property, so
--            `Preset:ResolveValue` falls through `GetProperty` to
--            `GetParameterValue` — the same path vanilla's own GeneSelection
--            read takes, on an identically-shaped preset)
--     1.0.7  NOTHING places class `Tech` anywhere in that tree, so `Techs` is
--            EMPTY and the first read is nil ⇒ `TechDef.GeneForging.param1`
--            -> 50 (`Data/TechPreset.lua:1556-1564`). Same answer, other map.
--
-- ⚠️ THE WRAPPER KEEPS ITS VARARG, deliberately, against the note that
-- suggested dropping the `unit` plumbing as "harmless, 1.1.0 ignores it".
-- 1.1.0 does ignore it — `GetRareTraitChance()` is parameterless there and all
-- three call sites pass nothing. But 1.0.7's is `GetRareTraitChance(unit)` and
-- TWO of its call sites DO pass a colonist (`TraitPreset.lua:748`,
-- `Colonist.lua:3559`), which `orig` uses to pick the city. A wrapper declared
-- `function()` would swallow that argument before `orig` ever saw it. `...`
-- forwards whatever the branch passes and invents nothing.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Units/Colonist.lua GetRareTraitChance sha256=ad46cc5455e72581125e01fce4a3ae3969113cb0c04561e9b9ce1d57ae7511a1
--   (Lua/Units/Colonist.lua:4398-4402 at pin time)
-- DEFECT: IsTechResearched\("GeneSelection"\)
--   GeneSelection is the ONLY tech consulted. ⚠️ The defect is an ABSENCE
--   (GeneForging is unknown here), so this expression states the half that IS
--   present: DEFECT-GONE will not fire if vanilla adds GeneForging alongside
--   it -- the body hash is what watches for that (FIX_POLICY §2b)

-- The tech's bonus, read from whichever map the running branch populates. Read
-- at CALL time, never at apply time: presets do not exist while mod code loads.
-- Returns nil when neither map knows the tech, and the caller treats nil as
-- "no bonus" — never as zero-by-accident, which is the failure mode A-1 is
-- about in the first place.
local function gene_forging_bonus()
	local techs = rawget(_G, "Techs")
	local preset = type(techs) == "table" and techs.GeneForging
	if type(preset) == "table" and type(preset.ResolveValue) == "function" then
		local ok, v = pcall(preset.ResolveValue, preset, "param1")
		-- a 0 here is indistinguishable from "this branch does not store it
		-- that way", and both mean the same thing to us: try the other map.
		if ok and type(v) == "number" and v ~= 0 then return v end
	end
	local defs = rawget(_G, "TechDef")
	local def = type(defs) == "table" and defs.GeneForging
	local v = type(def) == "table" and def.param1
	if type(v) == "number" and v ~= 0 then return v end
end

SMRFixPack.Register("GeneForging", {
	title = "The Gene Forging tech actually increases the rare-trait chance",
	apply = function()
		local err = SMRFixPack.Require("GeneForging", {
			{ global = "GetRareTraitChance" },
			-- both branches ship it, each defined in terms of its own
			-- researching party; see the header's item 2
			{ global = "IsTechResearched" },
		})
		if err then return err end
		local orig = GetRareTraitChance

		return SMRFixPack.SetGlobal("GetRareTraitChance", function(...)
			local base = orig(...)
			-- FIX (F41): Gene Forging was researched and then ignored. The two
			-- techs stack, so this is additive on top of whatever the shipped
			-- body decided about GeneSelection.
			if IsTechResearched("GeneForging") then
				return (base or 0) + (gene_forging_bonus() or 0)
			end
			return base
		end, "could not install the GetRareTraitChance wrapper")
	end,
})
