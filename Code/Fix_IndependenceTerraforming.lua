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
-- *Open half — saves where the tech is ALREADY researched keep the old 10%.*
-- `Effect_ModifyLabel:OnApplyEffect` (`Lua\MarsGameEffects.lua:161-178`) computes
-- `amount = self.Amount * scale` at research time and stores a Modifier on the
-- colony keyed by the effect object; that stored Modifier is what persists in the
-- savegame, and correcting the preset afterwards does not touch it. A repair is
-- possible — the key is the same preset object, so re-applying would replace
-- rather than stack — but `OnApplyEffect`'s second parameter also decides the
-- Modifier's `id`, and getting that wrong would leave an unidentifiable modifier
-- in every affected save. Not worth the risk for a 10-point discount; recorded on
-- the F18 entry as the open half for a later sanitizer pass instead.

local FIX_ID = "IndependenceTerraforming"
local TECH_ID = "Independence_TerraformingProjects"
local PROP = "SpecialProjectResourcesModifier"
local WANTED = -20

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

local patched = false

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
	if found == 0 then
		if entry then
			entry.status = "inactive"
			entry.detail = TECH_ID .. " no longer modifies " .. PROP
		end
		log("%s: inactive (%s no longer modifies %s)", FIX_ID, TECH_ID, PROP)
	elseif changed == 0 then
		if entry then
			entry.status = "inactive"
			entry.detail = "the shipped tech already matches its own param1"
		end
		log("%s: inactive (the shipped tech already matches its own param1)", FIX_ID)
	else
		log("%s: %s now discounts special projects by %d%% as its param1 says",
			FIX_ID, TECH_ID, -WANTED)
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
