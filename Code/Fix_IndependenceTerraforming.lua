-- F18: "Independent Terraforming" makes special projects 10% cheaper where its
-- own parameter says 20%.
--
-- Defect (`Data\TechPreset.lua:4798-4812`):
--     id = "Independence_TerraformingProjects",
--     param1 = 20,
--     param1comment = "decrease percent",
--     PlaceObj('Effect_ModifyLabel', {
--         Amount = -10,
--         Label = "Consts",
--         Prop = "SpecialProjectResourcesModifier",
--     }),
-- `SpecialProjectResourcesModifier` is a 100-based percentage consumed by
-- `Lua\SpecialProjects.lua:105`, so -10 is a 10% discount against a declared 20.
--
-- The evidence is the tech's own family. Every other Independence tech has
-- `param1` equal to the magnitude of the effect it drives:
--     Independence_Adaptivity            param1 = 5      Amount  = -5
--     Independence_MartianbornPerformance param1 = 5     Percent = 5
--     Independence_RocketCapacity        param1 = 30000  Amount  = 30000
--     Independence_Research              param1 = 20     Amount  = 20
-- Only this one disagrees with itself. FIX_POLICY §4's "prefer the reading proven
-- by sibling code" test, four times over inside one tech group.
--
-- Patch approach: preset data patch (FIX_POLICY §1.1) from OnMsg.DataLoaded
-- (+ DataChanged), correcting `Amount` to -20 on the effect that carries this
-- property. The effect is found by what it does (Label "Consts", Prop
-- "SpecialProjectResourcesModifier"), not by index, and an Amount that is
-- already -20 leaves the fix inactive — so a game hotfix simply switches it off.
--
-- *Formerly-open half, CLOSED 2026-07-26 (user-driven design): saves where the
-- tech was researched before the fix carried the old -10 in a STORED modifier.*
-- `Effect_ModifyLabel:OnApplyEffect` (`Lua\MarsGameEffects.lua:161-178`) computes
-- `amount = self.Amount * scale` at research time and stores a Modifier on the
-- colony KEYED BY THE EFFECT OBJECT (`colony:SetLabelModifier(self.Label, self,
-- …)`), so the stale modifier is directly addressable — no searching, no id
-- reconstruction. The earlier fear (the `parent` argument decides the Modifier's
-- `id`) dissolved on reading the shipped applier: `GameEffectsContainer:
-- EffectsApply(player)` calls `effect:OnApplyEffect(player, self)` with the
-- CONTAINER (the tech preset) as parent (`CommonLua\Classes\GameEffect.lua:
-- 36-40`), so re-calling `effect:OnApplyEffect(UIColony, tech)` is
-- argument-identical to research and REPLACES the stored modifier under the same
-- key with the corrected amount. The LoadGame sweep below does exactly that,
-- gated on positive identification: tech researched, preset in its corrected
-- state, stored modifier present and carrying exactly the old wrong amount.
-- Anything unexpected is left alone and logged. Idempotent; the engine's own
-- `SavegameFixups.Move_Effect_ModifyLabel_FromCitiesBackToColony`
-- (`MarsGameEffects.lua:180+`) is precedent for surgery on these exact tables.

local FIX_ID = "IndependenceTerraforming"
local TECH_ID = "Independence_TerraformingProjects"
local PROP = "SpecialProjectResourcesModifier"
local WANTED = -20

local log = SMRFixPack.Log

-- The scaffold (one pass per load, veto re-read, F75 data_loaded latch gate,
-- B3 ever_changed re-fire branch, DataChanged re-arm) lives in
-- SMRFixPack.DataPatch since Phase 4 (audit C2).
local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "TechPreset",
	pass = function(ctx)
		local defs = rawget(_G, "TechDef")
		local tech = type(defs) == "table" and defs[TECH_ID]
		if type(tech) ~= "table" then
			-- Phase 4 (C4): this pass previously had NO missing-target latch at
			-- all — a future update that removed the tech would have reported
			-- `active` forever (the exact B3 gap). Closed via the runner's
			-- data_loaded gate; before DataLoaded, absence still proves nothing.
			if ctx.data_loaded then
				ctx.patched = true
				ctx.latch("TechDef." .. TECH_ID .. " not found (game update changed it?)",
					"TechDef." .. TECH_ID .. " not found")
			end
			return
		end

		local found, changed = 0, 0
		for _, effect in ipairs(tech) do
			if type(effect) == "table" and effect.class == "Effect_ModifyLabel"
				and effect.Label == "Consts" and effect.Prop == PROP then
				found = found + 1
				if effect.Amount ~= WANTED then
					effect.Amount = WANTED
					changed = changed + 1
				end
			end
		end
		ctx.patched = true

		if changed > 0 then
			ctx.ever_changed = true
			-- restore the status too, in case an earlier pass mislabeled it —
			-- ctx.heal() heals ONLY an "inactive" mislabel, never "disabled"
			-- (audit A1)
			ctx.heal()
			log("%s: %s now discounts special projects by %d%% as its param1 says",
				FIX_ID, TECH_ID, -WANTED)
		elseif ctx.ever_changed then
			-- finding nothing left to change on the DataChanged(false) re-fire
			-- is SUCCESS (the B3 lesson — see SMRFixPack.DataPatch)
			return
		elseif found == 0 then
			ctx.latch(TECH_ID .. " no longer modifies " .. PROP,
				TECH_ID .. " no longer modifies " .. PROP)
		else
			ctx.latch("the shipped tech already matches its own param1", nil, "benign")
		end
		SMRFixPack.IndependenceTerraforming = { found = found, changed = changed }
	end,
})

SMRFixPack.Register(FIX_ID, {
	title = "Independent Terraforming discounts special projects by the 20% it advertises",
	apply = function()
		patch()   -- no-op at apply time (F87); the runner fires itself once
		          -- the classes are built AND the presets are loaded
	end,
})

local OLD_WRONG = -10   -- the shipped defect's Amount, the only value the sweep corrects

-- One-shot-by-state repair for saves that researched the tech before the preset
-- fix existed (see the header). colony_override is a test hook for the TestKit
-- probe; live callers pass nothing.
function SMRFixPack.IndependenceTerraformingSweep(colony_override)
	local entry = SMRFixPack.fixes[FIX_ID]
	if not (entry and entry.status == "active") then return "fix not active" end
	local defs = rawget(_G, "TechDef")
	local tech = type(defs) == "table" and defs[TECH_ID]
	if type(tech) ~= "table" then return "tech missing" end
	local colony = colony_override or rawget(_G, "UIColony")
	if not colony or type(colony.IsTechResearched) ~= "function"
		or not colony:IsTechResearched(TECH_ID) then
		return "tech not researched"
	end
	local scale_fn = rawget(_G, "GetModifiablePropScale")
	local scale = type(scale_fn) == "function" and scale_fn(PROP) or 1
	local corrected = 0
	for _, effect in ipairs(tech) do
		if type(effect) == "table" and effect.class == "Effect_ModifyLabel"
			and effect.Label == "Consts" and effect.Prop == PROP then
			if effect.Amount ~= WANTED then return "preset not in corrected state" end
			local mods = colony.label_modifiers
			local stored = type(mods) == "table" and type(mods.Consts) == "table"
				and mods.Consts[effect]
			if not stored then
				return "no stored modifier"   -- nothing to repair; leave alone
			elseif stored.amount == WANTED * scale then
				return "already correct"
			elseif stored.amount ~= OLD_WRONG * scale then
				log("%s: stored modifier carries unexpected amount %s (old bug would be %d) — leaving it alone",
					FIX_ID, tostring(stored.amount), OLD_WRONG * scale)
				return "unexpected amount"
			else
				-- argument-identical to the shipped applier (GameEffect.lua:36-40):
				-- replaces the stored modifier under the same key with Amount -20
				effect:OnApplyEffect(colony, tech)
				corrected = corrected + 1
			end
		end
	end
	if corrected > 0 then
		log("%s: corrected the already-researched tech's stored discount from %d%% to %d%% (savegame sweep)",
			FIX_ID, -OLD_WRONG, -WANTED)
		return "corrected"
	end
	return "no matching effect"
end

function OnMsg.LoadGame()
	SMRFixPack.IndependenceTerraformingSweep()
end
