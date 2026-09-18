-- C107: Dry Farming halves crop water for the three base-game plant farms only;
-- the four Feeding the Future plant farms are never reduced.
--
-- SRC: none -- a Tech preset patch plus a load-time heal through vanilla's own OnApplyEffect -- no function body of ours replaces a shipped one
-- DEFECT@Data/Tech.lua: id\s*=\s*"DryFarming",(?:(?!\bid\s*=\s*"|"(?:FarmSmall|FarmSmallUnderground|FarmUnderground|AutomatedFarm|AllFarms)")[\s\S])*?"water_consumption"(?:(?!\bid\s*=\s*"|"(?:FarmSmall|FarmSmallUnderground|FarmUnderground|AutomatedFarm|AllFarms)")[\s\S])*?\n\}\)
--
-- The DEFECT line states an ABSENCE (FIX_POLICY §2b): from DryFarming's `id` to the
-- close of its preset, the tech modifies water_consumption and names none of the
-- labels the four DLC plant farms join. It goes DEFECT-GONE if Data/Tech.lua gains
-- one of those labels in that preset. A repair shipped anywhere else (the norman
-- presets, a template label) is invisible to it; the pass below catches both of
-- those routes at runtime instead (adopt, and the already-reached guard).
--
-- Defect (1.1.0.403908): Data/Tech.lua:769-802, tech DryFarming. Its description
-- and short description promise "Water requirements of crops are reduced by
-- <percent(param1)>" with no qualifier (:770, :782). Its effects are three
-- Effect_ModifyLabel, water_consumption -50, on the labels Farm, HydroponicFarm
-- and OpenFarm (:787-801). A building joins its own class label (template id),
-- its object_class label, label1..label5 and its build-menu category
-- (Lua/Buildings/Building.lua:435-460), so the four Feeding the Future (norman)
-- plant farms FarmSmall, FarmSmallUnderground, FarmUnderground and AutomatedFarm
-- never join any label the tech pays. All four inherit FarmBase and set their base
-- water from the crop (Lua/Buildings/Farm.lua:619), read back through the modifier
-- (:825). Full evidence and the scope ruling: docs/agent/bugs/C107.md.
--
-- Intent tell 4 (self-contradiction): the tech's own text promises every crop and
-- its enumeration pays three buildings. The enumeration is curated by a rule the
-- four DLC farms satisfy: base 1.0.7's AllFarms label held exactly Farm,
-- HydroponicFarm, OpenFarm and the two Fungal Farms, and the author took that set
-- minus the fungi, i.e. "plant-growing farms". Scope is settled at exactly the
-- four norman plant farms. The Fungal Farm and the Insect Farm stay out, and
-- AllFarms is NOT used, because it would pay them.
--
-- Reachability R1 for any Feeding the Future owner who researches the
-- breakthrough: all four templates are buildable (build_category "Farms" or
-- "LifeSupport", no hide_from_build_menu).
--
-- Patch approach: FIX_POLICY §1.1, data/preset patch, ADDITIVE. Four
-- Effect_ModifyLabel entries appended to Techs.DryFarming, one per DLC label, each
-- copying Prop and Percent from the shipped Farm entry. In 1.1.0 the effects live
-- on the `Tech` preset (GlobalMap "Techs", CommonLua/Libs/Research/ClassDefs/
-- ClassDef-PresetDefs.generated.lua:3-27; Data/Tech.lua is PlaceObj('Tech', ...)).
-- Presets.TechPreset / TechDef.DryFarming (Data/TechPreset.lua:205-209) carries
-- only param1 and no effects, so it is not the target. Research applies the
-- tech with `preset:EffectsApply(UIColony)` (Lua/TechTree.lua:1228), which walks
-- the preset's array part (CommonLua/Classes/GameEffect.lua:36-40), so a new
-- research picks up the appended entries with no other code involved.
--
-- ⛔ Built with PlaceObj, never Effect_ModifyLabel:new{} (the F87 rule), and only
-- from the DataPatch pass, which runs after the classes are built.
--
-- Guards, all in the pass, all fail closed:
--   * DLC absent: an entry is appended only for a label whose template preset AND
--     building class both exist. Without Feeding the Future neither exists,
--     nothing is appended, nothing reaches a save, and the module stays active and
--     idle. Absence is NEVER final: the pass latches `patched` only once all four
--     were seen, so a template that arrives on a later trigger is still paid.
--   * ⛔ WHERE A TEMPLATE IS READ, corrected 2026-09-18 after the first in-game boot
--     (log Mars.exe-20260918-17.51.56). The build read `BuildingTemplates`, and
--     that map is wrong for this twice over (1.1.0.403908):
--       - it is rebuilt only at ClassesBuilt and on DataChanged by
--         SetupBuildingTemplateTables (Lua/Buildings/Building.lua:2674-2692). On a
--         cold boot ClassesBuilt precedes LoadData, so at DataLoaded the map holds
--         no preset at all; it fills on the DataChanged that Dlc.lua posts from a
--         thread after DataLoaded (CommonLua/Dlc.lua:715-717 -> :686-690 -> :683).
--         The first pass therefore read "DLC absent" and latched it final;
--       - its values are proxies, `setmetatable({ template_name = id },
--         g_Classes[id])` (Building.lua:2680), so `.id` is nil. The DataChanged
--         re-fire then threw "table index is nil" on `labels[template.id]`.
--     Now: existence comes from the preset map BuildingTemplates_Raw, which
--     Preset:Register fills as each preset file loads (CommonLua/Preset.lua:
--     573-580, the BuildingTemplate GlobalMap, Building.lua:2556), so it is
--     complete at DataLoaded; the labels come from g_Classes[label], the class a
--     placed building IS (the proxy's own metatable), keyed by the label looked up.
--   * Shape: the shipped Farm / HydroponicFarm / OpenFarm water_consumption
--     entries must be present and agree on one negative Percent with Amount 0 and
--     no Stackable; otherwise the pass latches instead of guessing the number.
--   * §2a behaviour probe: the shipped Farm entry's OnApplyEffect is called on a
--     stub colony and must file under its own Label, keyed by the effect object,
--     with a value carrying the same prop and percent and amount 0. That is the
--     shape the heal's presence test below relies on.
--   * Adopt, never duplicate: an existing entry with the same Label and Prop (a
--     previous pass in this process, another mod, or a future game patch) is
--     adopted, not doubled.
--   * Already reached: a template that already joins a label the shipped tech
--     pays for water (for example if a patch adds AllFarms to DryFarming, or a
--     template gains the Farm label) gets no entry, because a second -50% would
--     stack to -100%. If every present template is reached this way the pass
--     latches benign (vanilla fixed it: RETIRE candidate).
--
-- §3 / §3a savegame: nothing of ours enters the save as code. The pass mutates a
-- preset array; the heal is synchronous and calls vanilla's own OnApplyEffect. No
-- thread, no GameVar, no wrapper frame. What DOES persist, as in vanilla, is the
-- modifier in UIColony.label_modifiers, keyed by a copy of the Effect_ModifyLabel
-- (a vanilla class holding vanilla fields). After the pack is removed that
-- modifier stays and the DLC farms keep the -50% they are owed on a save where the
-- tech was researched: a non-harmful trace (§3a tier 2), and it is the intended
-- behaviour, not a residue to clean. The save loads without the pack.

local FIX_ID = "DryFarmingFarms"
local TECH_ID = "DryFarming"

local log = SMRFixPack.Log

-- The four Feeding the Future plant farms, in the order the log reports them.
-- Each is a BuildingTemplate id, and a building always joins its own id label
-- (Lua/Buildings/Building.lua:460).
local TARGETS = { "FarmSmall", "FarmSmallUnderground", "FarmUnderground", "AutomatedFarm" }
local IS_TARGET = {}
for _, label in ipairs(TARGETS) do IS_TARGET[label] = true end

-- The shipped entries the new ones copy their numbers from.
local SHIPPED = { "Farm", "HydroponicFarm", "OpenFarm" }
local PROP = "water_consumption"

-- Label -> the Effect_ModifyLabel that now lives in Techs.DryFarming, appended or
-- adopted. The heal applies exactly these.
local owned = {}

-- Set by apply() after its self-check passes (the C90 guard: a declined apply must
-- stop all pass work, and registry status is written only after apply returns).
local self_check_passed = false

-- Every label a building of class `cls` (named `label`) joins in its own city
-- (Building:AddToCityLabels / SetCustomLabels / ApplyCustomLabels /
-- SetBuildMenuCategoryLabels, Lua/Buildings/Building.lua:394-460): its class name,
-- its object_class, its default_label, label1..label5 and its build category, all
-- read off the class as the building reads them off itself. The top-level parent
-- category is not added; no shipped build category is a farm label.
-- Keyed by the label that was looked up, never by a field of the object, and every
-- value is type-checked before it becomes a key, so nothing here can throw.
local function building_labels(label, cls)
	local labels = { [label] = true }
	local function add(v)
		if type(v) == "string" and v ~= "" then labels[v] = true end
	end
	add(cls.object_class)
	add(cls.default_label)
	for _, prop_id in ipairs(BuildingCustomLabelProps) do
		if type(prop_id) == "string" then add(cls[prop_id]) end
	end
	add(cls.build_category)
	return labels
end

-- Logged once per Lua load, however many triggers find the DLC absent.
local said_absent = false

-- §2a PROBE. Calls the SHIPPED Effect_ModifyLabel:OnApplyEffect
-- (Lua/MarsGameEffects.lua:257-287) of the shipped Farm entry on a stub colony.
-- ⛔ STUB CONTRACT: the stub provides only SetLabelModifier(label, id, modifier),
-- the capture point (:277). WHY THE TARGET IS SAFE ON A STUB: the body reads
-- ModifiablePropScale (a table lookup, CommonLua/Classes/Modifiers.lua:620-631),
-- reads g_TechTimesResearched only when Stackable (the shape check refuses
-- Stackable), builds a T only when Reason ~= "" (the shipped entry has none),
-- constructs a Modifier (InitDone with no Init, Lua/Modifiers.lua:228-235), calls
-- the real preset's GetEffectIdentifier (returns a constant,
-- CommonLua/Classes/GameEffect.lua:42-44) and RefreshConstructionResourcesForLabel
-- only for a "_Construction" label ("Farm" is not). Synchronous, side-effect-free.
local function files_as_expected(effect, tech)
	local got_label, got_id, got_mod
	local stub = {
		SetLabelModifier = function(_, label, id, mod)
			got_label, got_id, got_mod = label, id, mod
		end,
	}
	effect:OnApplyEffect(stub, tech)
	return got_label == effect.Label and got_id == effect
		and type(got_mod) == "table" and got_mod.prop == effect.Prop
		and got_mod.percent == effect.Percent and got_mod.amount == 0
end

local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "Tech",
	pass = function(ctx)
		if not self_check_passed then return end
		-- Presets, DLC presets included, are complete only once DataLoaded has
		-- fired (the F75 lesson). Before that, absence means nothing, and the
		-- DLC-absent verdict below must not be reached.
		if not ctx.data_loaded then return end

		local techs = rawget(_G, "Techs")
		local tech = type(techs) == "table" and techs[TECH_ID]
		if type(tech) ~= "table" then
			ctx.patched = true
			ctx.latch("Techs." .. TECH_ID .. " not found (game update changed it?)",
				"Techs." .. TECH_ID .. " not found")
			return
		end
		-- NOT BuildingTemplates: see "WHERE A TEMPLATE IS READ" in the header.
		local presets = rawget(_G, "BuildingTemplates_Raw")
		local classes = rawget(_G, "g_Classes")
		if type(presets) ~= "table" or type(classes) ~= "table" then
			ctx.patched = true
			ctx.latch("BuildingTemplates_Raw / g_Classes not found (game update changed it?)",
				"BuildingTemplates_Raw / g_Classes not found")
			return
		end

		-- Index the tech's water entries by label. A malformed entry with no
		-- string Label is skipped, never used as a key.
		local water = {}
		for _, effect in ipairs(tech) do
			if IsKindOf(effect, "Effect_ModifyLabel") and effect.Prop == PROP
					and type(effect.Label) == "string" then
				water[effect.Label] = water[effect.Label] or effect
			end
		end

		-- Shape check: the three shipped entries, one shared negative Percent.
		local percent
		for _, label in ipairs(SHIPPED) do
			local e = water[label]
			if not e or e.Stackable or (e.Amount or 0) ~= 0
					or type(e.Percent) ~= "number" or e.Percent >= 0
					or (percent and e.Percent ~= percent) then
				ctx.patched = true
				ctx.latch(TECH_ID .. "'s water entries no longer match the shape this fix was written for (game update changed it?)",
					TECH_ID .. " water entries changed shape")
				return
			end
			percent = e.Percent
		end

		-- THE BRANCH GUARD (FIX_POLICY §2a), behaviour, never a version label.
		local farm_entry = water[SHIPPED[1]]
		if SMRFixPack.Require(FIX_ID, {
			{ probe = function() return files_as_expected(farm_entry, tech) end },
		}) then
			ctx.patched = true
			ctx.latch("the shipped Effect_ModifyLabel no longer files its modifier the way this fix expects (game update changed it?)",
				"Effect_ModifyLabel filing behaviour not recognised")
			return
		end

		-- Labels the SHIPPED tech (not our entries) already pays for water.
		local paid = {}
		for label in pairs(water) do
			if not IS_TARGET[label] then paid[label] = true end
		end

		local present, changed, adopted, reached = 0, 0, 0, {}
		for _, label in ipairs(TARGETS) do
			local cls = classes[label]
			if type(presets[label]) == "table" and type(cls) == "table" then
				present = present + 1
				if water[label] then
					-- an earlier pass in this process, another mod, or the game
					owned[label] = water[label]
					adopted = adopted + 1
				else
					local via
					for l in pairs(building_labels(label, cls)) do
						if paid[l] then via = l break end
					end
					if via then
						reached[#reached + 1] = label .. " via " .. via
					else
						local effect = PlaceObj("Effect_ModifyLabel", {
							Label = label,
							Percent = percent,
							Prop = PROP,
						})
						if type(effect) == "table" then
							tech[#tech + 1] = effect
							owned[label] = effect
							changed = changed + 1
						end
					end
				end
			end
		end
		-- ⛔ Final only once every target was seen. A missing one may still arrive
		-- on a later trigger, and every pass is idempotent (adopt), so re-running
		-- costs a few table reads. This is the fault the first boot hit: an early
		-- "absent" latched final and the templates that arrived later were never paid.
		local complete = present == #TARGETS
		if complete then ctx.patched = true end

		if present == 0 then
			-- Feeding the Future is not loaded (yet). Not a game change and not
			-- "already fixed": nothing to pay. Stay active and idle.
			if not said_absent then
				said_absent = true
				log("%s: none of the four Feeding the Future plant farms is loaded; nothing to add", FIX_ID)
			end
			return
		end
		if #reached > 0 then
			log("%s: left %d farm(s) alone because %s already reaches them (%s)",
				FIX_ID, #reached, TECH_ID, table.concat(reached, ", "))
		end
		if changed > 0 then
			ctx.ever_changed = true
			ctx.heal()
			log("%s: added %d water entr(y/ies) at %s%% to %s (%d adopted, %d of 4 farms loaded)",
				FIX_ID, changed, tostring(percent), TECH_ID, adopted, present)
		elseif ctx.ever_changed then
			-- the DataChanged(false) re-fire or a Lua reload finding our own
			-- entries is SUCCESS (the B3 lesson)
			return
		elseif complete then
			ctx.latch(TECH_ID .. " already reaches every Feeding the Future plant farm", nil, "benign")
		end
		-- else: some templates still missing and nothing to add yet; not final.
	end,
})

-- Applies each owned entry this colony does not already carry. Returns the count.
-- ⛔ Presence is tested by PROPERTY, never by object identity. label_modifiers is
-- persisted and a save deserialises its own copy of the key, so an identity test
-- misses on every load and re-applies (F95, measured 2026-08-02: 1 became 2 after
-- one save and reload). The match is the stored key's class, Label, Prop, Percent
-- and Amount, the form vanilla's own fixups use
-- (Lua/MarsGameEffects.lua:329-330, :407).
local function heal(colony, tech)
	local healed = 0
	for _, label in ipairs(TARGETS) do
		local effect = owned[label]
		if effect then
			local found = false
			local mods = colony.label_modifiers[label]
			if type(mods) == "table" then
				for key in pairs(mods) do
					if IsKindOf(key, "Effect_ModifyLabel") and key.Label == label
							and key.Prop == effect.Prop and key.Percent == effect.Percent
							and (key.Amount or 0) == 0 then
						found = true
						break
					end
				end
			end
			if not found then
				effect:OnApplyEffect(colony, tech)
				healed = healed + 1
			end
		end
	end
	return healed
end

-- Exposed for the Test Kit probe, which drives it on a stub colony.
SMRFixPack.DryFarmingFarms = { Heal = heal, Owned = owned, Targets = TARGETS }

-- Existing saves: tech effects are applied once, at research
-- (Lua/TechTree.lua:1228), so a save that researched Dry Farming before this fix
-- never got the four modifiers. A one-shot-in-effect pass: it applies only what is
-- missing, so a second load of a healed save does nothing and logs nothing.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	if not next(owned) then return end
	local techs = rawget(_G, "Techs")
	local tech = type(techs) == "table" and techs[TECH_ID]
	if type(tech) ~= "table" then return end
	if not IsTechResearched(TECH_ID) then return end
	local colony = rawget(_G, "UIColony")
	if type(colony) ~= "table" or type(colony.label_modifiers) ~= "table" then return end
	local healed = heal(colony, tech)
	if healed > 0 then
		log("%s: applied %d Dry Farming water reduction(s) this save researched without", FIX_ID, healed)
	end
end)

SMRFixPack.Register(FIX_ID, {
	title = "Dry Farming also reduces crop water on the Feeding the Future plant farms, as its own text promises",
	apply = function()
		-- Checked on the classes that DECLARE the methods (the F64 lesson).
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "PlaceObj" },
			{ global = "IsKindOf" },
			{ global = "IsTechResearched" },
			{ global = "BuildingCustomLabelProps", kind = "table" },
			{ class = "Effect_ModifyLabel", method = "OnApplyEffect" },
			{ class = "LabelContainer", method = "SetLabelModifier" },
		})
		if err then return err end
		self_check_passed = true
		patch()   -- no-op at apply time (F87); the runner fires itself once
		          -- the classes are built AND the presets are loaded
	end,
})
