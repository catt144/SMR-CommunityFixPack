-- F92: the Saint trait's dome blessing has never applied to anyone.
--
-- Defect: two adjacent lines in the same loop name the same concept two
-- different ways (Lua\Units\Colonist.lua:372-377, a colonist joining a dome):
--     dome:AddToLabel(GetTraitLabel(trait_id), self)          -- files under "TraitReligious"
--     ...
--     trait:AddDomeColonistsModifier(self, trait.modify_trait) -- passes "Religious"
-- TraitPreset:AddDomeColonistsModifier uses that string RAW as the label —
--     local label = (trait ~= "") and trait or "Colonist"
--     dome:SetLabelModifier(label, unit, { … })
-- (Lua\ClassDefs\ClassDef-PresetDefs.generated.lua:1774-1791) — while
-- GetTraitLabel returns `fixed_labels[trait_id] or ("Trait" .. trait_id)`
-- (Lua\Traits.lua:1300-1302) and "Religious" is NOT in fixed_labels (:1268-1298).
--
-- So Saint's +10 base_morale is registered on the label "Religious", which no
-- colonist is ever filed under: the only filing site is Colonist.lua:373, via
-- GetTraitLabel. SetLabelModifier applies to everyone currently in
-- self.labels[label] and AddToLabel applies existing modifiers to newcomers
-- (Lua\LabelContainer.lua:59-78, :17-28) — both operate on an array that stays
-- empty forever. The preset's own promise — "Raises the Morale of all Religious
-- people in the Dome" — has never reached a single colonist.
--
-- Intent tells, two, and the second is an internal control:
--   1. self-contradiction — the preset's description and its
--      infopanel_effect_text ("Blessed by a Saint +<amount>") promise a visible
--      per-colonist effect the code cannot deliver to anybody;
--   2. ⭐ THE SAME FUNCTION WORKS FOR THE SIBLING TRAIT. Exactly two presets in
--      Data\TraitPreset.lua use modify_target = "dome colonists": Empath (:259-272)
--      and Saint (:383-397). Empath sets no modify_trait, so the (trait ~= "")
--      branch hands it the literal "Colonist" — a real dome label — and Empath's
--      blessing works. The only difference between the working case and the broken
--      one is whether the value needs GetTraitLabel and doesn't get it.
--
-- Patch approach: FIX_POLICY §1.1 — a data/preset patch, the most-preferred rung,
-- and it needs no method touched at all. modify_trait has exactly five readers in
-- the tree (ClassDef-PresetDefs.generated.lua:1814/:1825, Colonist.lua:362/:376,
-- _fixup.lua:1918) and NO UI or display consumer, so correcting the stored value
-- fixes every path at once, add and remove symmetrically.
--
-- The rule is stated generally and its two guards each earn their place:
--   * TraitPresets[value] ~= nil keeps us off any MOD-ADDED preset whose author
--     deliberately stored a raw label that is not a trait id — rewriting that
--     would be fixing (or breaking) another mod's data, barred by FIX_POLICY §4a;
--   * GetTraitLabel(value) ~= value makes the patch a no-op for traits that ARE
--     in fixed_labels (Genius, Dreamer, …).
-- On shipped 1.0.7.396349 data the set it changes is exactly {Saint}.
--
-- Existing saves also need a one-shot re-base, because the stale registration was
-- written into the dome when the Saint joined it. See the LoadGame pass below.
--
-- §3a: NOTHING ENTERS THE SAVE. A preset field write plus one synchronous
-- load-time pass — no mod thread, no persisted field, no wrapper frame. This is
-- the layer-3 shape by construction (patch an input, keep vanilla's body).
--
-- ⚠️ STATED PLAINLY, BECAUSE IT IS A REAL EFFECT IN PLAY: after this fix Saints
-- actually raise Religious colonists' morale by +10 in their dome, and the
-- "Blessed by a Saint" line appears on those colonists. That is the documented
-- behaviour being restored, not a balance change — but anyone reading a morale
-- A/B afterwards needs to know it landed.

local FIX_ID = "SaintBlessing"

local log = SMRFixPack.Log

-- trait id -> the raw label value the preset carried BEFORE we corrected it.
-- Populated by the pass, consumed by the load-time re-base below. Empty means
-- there is nothing to heal (shipped data already correct, or nothing patched).
local rebased_from = {}

-- The scaffold (one pass per load, veto re-read, F75 data_loaded latch gate,
-- B3 ever_changed re-fire branch, DataChanged re-arm) lives in
-- SMRFixPack.DataPatch since Phase 4 (audit C2).
local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "TraitPreset",
	pass = function(ctx)
		local presets = rawget(_G, "TraitPresets")
		if type(presets) ~= "table" then
			-- Before DataLoaded this just means "presets not loaded yet"; after
			-- it, absence means a future update removed the target (the F75/B3 pair).
			if ctx.data_loaded then
				ctx.patched = true
				ctx.latch("TraitPresets not found (game update changed it?)",
					"TraitPresets not found")
			end
			return
		end
		local get_label = rawget(_G, "GetTraitLabel")
		if type(get_label) ~= "function" then
			ctx.patched = true
			ctx.latch("GetTraitLabel not found (game update changed it?)",
				"GetTraitLabel not found")
			return
		end

		local found, changed = 0, 0
		for trait_id, p in pairs(presets) do
			if type(p) == "table" and p.modify_target == "dome colonists" then
				found = found + 1
				local raw = p.modify_trait
				if type(raw) == "string" and raw ~= "" and presets[raw]
						and get_label(raw) ~= raw then
					rebased_from[trait_id] = raw
					p.modify_trait = get_label(raw)
					changed = changed + 1
				end
			end
		end
		ctx.patched = true

		if changed > 0 then
			ctx.ever_changed = true
			-- heals ONLY an "inactive" mislabel, never "disabled" (audit A1)
			ctx.heal()
			log("%s: corrected %d dome-colonists trait modifier label(s) of %d",
				FIX_ID, changed, found)
		elseif ctx.ever_changed then
			-- finding nothing left to change on the DataChanged(false) re-fire is
			-- SUCCESS (the B3 lesson — see SMRFixPack.DataPatch)
			return
		elseif found == 0 then
			ctx.latch("no TraitPreset uses modify_target \"dome colonists\" any more",
				"no dome-colonists trait presets")
		else
			ctx.latch("every dome-colonists trait preset already names a real label",
				nil, "benign")
		end
	end,
})

-- One-shot re-base for saves written before this fix. A Saint who joined a dome
-- under the broken value left a modifier filed on the raw label; the corrected
-- preset alone does not move it, because nothing re-runs Apply on a load.
--
-- Idempotent, and ALSO one-shot in effect — the two are different properties and
-- the spec asked for both:
--   * the stale removal runs unconditionally. It walks self.labels["Religious"],
--     an array that is empty by definition of this defect, so it cannot subtract
--     morale from anyone, and doing it every time costs nothing;
--   * the RE-APPLY is skipped when this colonist already carries the modifier
--     under the corrected label. Without that check the pass re-applies to every
--     dome Saint on every load forever — harmless (SetLabelModifier is keyed by
--     (label, unit) and REPLACES, so a re-run nets zero, LabelContainer.lua:59-78)
--     but it is NOT one-shot, and it would print its line in every future
--     session's log. ⚠️ That is exactly what this pass did when first built
--     2026-08-02; caught before the batch leg ran, and the check is the same shape
--     Fix_AstrogeologistExtractors already used for its own heal.
-- The log line therefore MEANS something: it appears only on a save that actually
-- needed healing, and a second load of a healed save is silent.
-- It reuses vanilla's own application path rather than hand-rolling a modifier,
-- so the id, scale and container stay identical to what a new game produces.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	if not next(rebased_from) then return end
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end
	local presets = rawget(_G, "TraitPresets")
	if type(presets) ~= "table" then return end

	local rebased = 0
	AllMapsForEach(true, "Colonist", function(colonist)
		if not IsValid(colonist) or not colonist.dome then return end
		local traits = colonist.traits
		if type(traits) ~= "table" then return end
		local dome = colonist.dome
		for trait_id in pairs(traits) do
			local old_label = rebased_from[trait_id]
			local p = old_label and presets[trait_id]
			if p and p.modify_target == "dome colonists" then
				-- always clear the stale registration; it cannot cost anyone morale
				dome:SetLabelModifier(old_label, colonist, nil)
				local mods = type(dome.label_modifiers) == "table"
					and dome.label_modifiers[p.modify_trait]
				if not (mods and mods[colonist]) then
					p:AddDomeColonistsModifier(colonist, p.modify_trait)
					rebased = rebased + 1
				end
			end
		end
	end)
	if rebased > 0 then
		log("%s: re-based %d dome blessing(s) onto the label colonists are actually filed under", FIX_ID, rebased)
	end
end)

SMRFixPack.Register(FIX_ID, {
	title = "A Saint's blessing reaches the Religious colonists in their dome",
	apply = function()
		-- Checked on the class that DECLARES it (TraitPreset), because mod code
		-- loads before the classes are flattened (the F64 lesson).
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "GetTraitLabel" },
			{ class = "TraitPreset", method = "AddDomeColonistsModifier" },
			{ class = "LabelContainer", method = "SetLabelModifier" },
		})
		if err then return err end
		patch()   -- no-op at apply time (F87); the runner fires itself once
		          -- the classes are built AND the presets are loaded
	end,
})
