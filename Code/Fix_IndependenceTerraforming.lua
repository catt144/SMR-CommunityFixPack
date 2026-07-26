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

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

local patched = false
local ever_changed = false   -- some pass this session actually changed the preset

local function patch()
	if patched then return end
	local defs = rawget(_G, "TechDef")
	local tech = type(defs) == "table" and defs[TECH_ID]
	if type(tech) ~= "table" then return end   -- presets not loaded yet

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
	patched = true

	local entry = SMRFixPack.fixes[FIX_ID]
	if changed > 0 then
		ever_changed = true
		-- restore the status too, in case an earlier pass mislabeled it
		if entry then
			entry.status = "active"
			entry.detail = nil
		end
		log("%s: %s now discounts special projects by %d%% as its param1 says",
			FIX_ID, TECH_ID, -WANTED)
	elseif ever_changed then
		-- FIX (QA 2026-07-25, same defect as F75): the engine posts
		-- DataChanged(false) right after DataLoaded, rerunning this pass over
		-- the preset it just corrected. Finding nothing left to change then is
		-- SUCCESS — without this branch the fix relabeled itself
		-- "inactive: already matches" on every boot (seen in the first B leg).
		return
	elseif found == 0 then
		if entry then
			entry.status = "inactive"
			entry.detail = TECH_ID .. " no longer modifies " .. PROP
		end
		log("%s: inactive (%s no longer modifies %s)", FIX_ID, TECH_ID, PROP)
	else
		if entry then
			entry.status = "inactive"
			entry.detail = "the shipped tech already matches its own param1"
		end
		log("%s: inactive (the shipped tech already matches its own param1)", FIX_ID)
	end
	SMRFixPack.IndependenceTerraforming = { found = found, changed = changed }
end

SMRFixPack.Register(FIX_ID, {
	title = "Independent Terraforming discounts special projects by the 20% it advertises",
	apply = function()
		patch()   -- no-op unless the presets are already loaded
	end,
})

function OnMsg.DataLoaded()
	patch()
end

function OnMsg.DataChanged(classes)
	if classes and not classes.TechPreset then return end
	patched = false
	patch()
end

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
