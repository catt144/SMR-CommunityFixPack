-- F92: the Saint trait's dome blessing has never applied to anyone.
--
-- SRC: none  DataPatch on shipped preset data — no game function body is replaced
-- DEFECT@Data/TraitPreset.lua: modify_trait\s*=\s*"Religious"
-- SRC: Lua/TraitPreset.lua TraitPreset:AddDomeColonistsModifier sha256=2b19b712d86dcde5b53e6f54f4b8ef2f0dea623187cf8de53688d0917d222186
--
-- ⚠️ The second SRC carries NO `DEFECT:` line ON PURPOSE (FIX_POLICY §2b's
-- named-exception shape). On 1.1.0 that body is CORRECT — it IS the vanilla
-- repair. It is pinned for class (b) only: the behaviour probe and the 1.1.0
-- save re-base below BOTH call it, so if the label resolution moves a third
-- time we get a `BODY-CHANGED` row instead of silence.
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
--
-- ======================================================================
-- 1.1.0 (2026-09-08, hotfix2 link 03; re-verification F-1, VANILLA_FIX_QA §0.3)
-- ======================================================================
--
-- ⛔ THE DEVELOPERS FIXED F92, AND UNTIL THIS EDIT OUR PATCH BROKE THEIR FIX.
-- TraitPreset:AddDomeColonistsModifier now does the lookup itself:
--     local label = (trait == "") and "Colonist" or GetTraitLabel(trait)
--     if not label then return end
-- (Lua/TraitPreset.lua:86-87, and the same pair in RemoveDomeColonistsModifier
-- at :100-101). Our pass had ALREADY rewritten Saint.modify_trait from
-- "Religious" to "TraitReligious", so vanilla computed
-- GetTraitLabel("TraitReligious"), TraitPresets["TraitReligious"] is nil,
-- GetTraitLabel returns false (Lua/Traits.lua:1325-1328), and the function
-- returned having registered NOTHING. With the pack on, no Saint blessed
-- anyone; with it off, 1.1.0 works. The shipped data still says
-- modify_trait = "Religious" (Data/TraitPreset.lua:405), so the DEFECT@ line
-- above is still true of the DATA — what changed is that the CODE now
-- compensates for it.
--
-- Two halves, and the second is the one that is easy to miss.
--
-- HALF ONE — the branch is decided by BEHAVIOUR, never by a version label
-- (FIX_POLICY §2a; there is no field to read — our lua_revision and 1.1.0's two
-- minimums are all 350453, EF-077). The pass calls the SHIPPED function on stubs
-- and reads back the label it filed under:
--   * captures the RAW value ("Religious")           ⇒ 1.0.7 body ⇒ APPLY;
--   * captures the RESOLVED label ("TraitReligious") ⇒ 1.1.0 body ⇒ DECLINE the
--     data rewrite and arm the save re-base below;
--   * captures nothing / throws / anything else      ⇒ UNKNOWN ⇒ DO NOTHING AT
--     ALL, and latch. ⛔ This third case is not pedantry: AddDomeColonistsModifier
--     returns silently when the stub's GetPropertyMetadata(modify_property) is
--     nil (:80-84), so "captured nothing" carries NO information — and reading
--     that silence as "the old shape" is exactly the bug being repaired here.
--     UNKNOWN is not permission. Both branches go through SMRFixPack.Require's
--     `probe` form, which admits ONLY the literal boolean true.
--
-- HALF TWO — the SAVE RE-BASE, for saves that were loaded while the pack was
-- broken. 1.1.0 ships one-shot SavegameFixups that strip every dome-colonists
-- trait modifier and rebuild it through the same function:
-- MigrateDomeTraitLabelModifiers (Lua/_fixup.lua:2097-2136 — the 1.0.7→1.1.0
-- migration, which also rehomes dome labels from trait.id to GetTraitLabel) and
-- OrphanedDomeColonistsTraitModifiers (:2138-2170). On any save loaded under the
-- broken pack BOTH already ran, with our wrong value, and registered nothing.
-- Fixups do not re-run; label_modifiers is persisted; nothing re-applies until
-- the Saint changes dome. ⚠️ The 1.0.7 heal below cannot cover it — it is keyed
-- on rebased_from, which is EMPTY when the pass declines. Hence a second,
-- separate re-base, armed ONLY by the "resolved" verdict.
--   * It is purely ADDITIVE: the broken value made the function return BEFORE
--     SetLabelModifier, so there is no stale registration anywhere to clean up
--     (unlike the 1.0.7 heal, which does have one). Nothing is subtracted.
--   * It re-applies through vanilla's own AddDomeColonistsModifier, so the id,
--     scale and container are identical to what a new game produces, and the
--     remove side stays symmetric: we do NOT touch the data on this branch, so
--     RemoveDomeColonistsModifier resolves the same label on the way out.
--   * Order against the fixups does not matter. If a fixup runs after us it
--     strips and rebuilds through the same function, which on unpatched 1.1.0
--     data succeeds — the end state is the same either way.
--   * One-shot in effect: a colonist that already carries the modifier under the
--     resolved label is skipped, so a second load of a healed save is silent.
--
-- ⚠️ WHAT THIS MODULE IS ON 1.1.0, said plainly: a save healer for damage a
-- previous version of THIS PACK did, and nothing else. It stays `active` because
-- that job is real, not because it patches anything. Once the installed base has
-- loaded once with this build it becomes a REMOVE candidate — recorded in the
-- bug entry, not decided here.

local FIX_ID = "SaintBlessing"

local log = SMRFixPack.Log

-- trait id -> the raw label value the preset carried BEFORE we corrected it.
-- Populated by the pass on the 1.0.7 branch ONLY, consumed by the load-time
-- re-base below. Empty means there is nothing to heal (shipped data already
-- correct, nothing patched, or we are on 1.1.0 — where `rebase_resolved` is the
-- live map instead).
local rebased_from = {}

-- trait id -> the raw (UNPATCHED) modify_trait value, on the 1.1.0 branch only.
-- Non-empty means: the shipped body resolves the label itself, we left the data
-- alone, and saves poisoned by an older build of this pack need re-basing.
local rebase_resolved = {}

-- Calls the SHIPPED TraitPreset:AddDomeColonistsModifier on stubs and returns the
-- label it filed under, or nil if it filed nothing.
--
-- ⛔ STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3). Read straight
-- off the shipped body at Lua/TraitPreset.lua:77-95 — the body pinned by the
-- second SRC: line above:
--     unit.dome                        must be truthy, or the body returns at :79
--     unit:GetPropertyMetadata(prop)   must return a table carrying .scale, or
--                                      the body print()s and returns at :80-84
--     dome:SetLabelModifier(label,...) the capture point, :89
-- WHY THE TARGET IS SAFE TO CALL ON ONE — every line of that body either reads
-- `self` (the real preset, read-only: modify_property/amount/percent/id), calls
-- GetPropScale (pure; CommonLua/PropertyObject.lua:1760, and we hand it a NUMBER
-- so it never even reaches const.Scale), calls GetTraitLabel (pure; two table
-- lookups, Lua/Traits.lua:1325-1328), or calls one of OUR two stubs. It touches
-- no real dome, no real unit, no save and no thread, and starts nothing:
-- synchronous and side-effect-free, shown from the shipped body as §2a requires.
local function capture_filed_label(preset, raw)
	local captured
	local dome = {
		SetLabelModifier = function(_, label)
			captured = label
		end,
	}
	local unit = {
		dome = dome,
		GetPropertyMetadata = function()
			return { scale = 1 }
		end,
	}
	preset:AddDomeColonistsModifier(unit, raw)
	return captured
end

-- true iff the shipped body files under exactly `expected`. Routed through
-- Require's `probe` form so the pcall trap, the strict-`true` rule and the
-- decline logging are the shared ones and not re-implemented here.
local function files_under(preset, raw, expected)
	return SMRFixPack.Require(FIX_ID, {
		{ probe = function()
			return capture_filed_label(preset, raw) == expected
		end },
	}) == nil
end

local function count(t)
	local n = 0
	for _ in pairs(t) do n = n + 1 end
	return n
end

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

		-- Collect first, mutate later: the probe must run against UNTOUCHED data,
		-- because it reads the shipped raw value back out of the shipped function.
		local found, candidates, probe_id = 0, {}, nil
		for trait_id, p in pairs(presets) do
			if type(p) == "table" and p.modify_target == "dome colonists" then
				found = found + 1
				local raw = p.modify_trait
				if type(raw) == "string" and raw ~= "" and presets[raw]
						and get_label(raw) ~= raw then
					candidates[trait_id] = raw
					-- deterministic pick, so the boot log reads the same run to
					-- run (pairs order does not)
					if not probe_id or trait_id < probe_id then probe_id = trait_id end
				end
			end
		end
		ctx.patched = true

		if not probe_id then
			if ctx.ever_changed then
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
			return
		end

		-- THE BRANCH GUARD (FIX_POLICY §2a). Behaviour, never a version label.
		local probe_preset, probe_raw = presets[probe_id], candidates[probe_id]
		if files_under(probe_preset, probe_raw, probe_raw) then
			-- 1.0.7 body: the raw value is used as the label. Correct the data.
			local changed = 0
			for trait_id, raw in pairs(candidates) do
				rebased_from[trait_id] = raw
				presets[trait_id].modify_trait = get_label(raw)
				changed = changed + 1
			end
			ctx.ever_changed = true
			-- heals ONLY an "inactive" mislabel, never "disabled" (audit A1)
			ctx.heal()
			log("%s: corrected %d dome-colonists trait modifier label(s) of %d",
				FIX_ID, changed, found)
		elseif files_under(probe_preset, probe_raw, get_label(probe_raw)) then
			-- 1.1.0 body: it resolves the label itself. Touch NOTHING; the only job
			-- left is re-basing saves an older build of this pack poisoned.
			rebase_resolved = candidates
			ctx.heal()
			log("%s: the shipped code resolves the trait label itself — data left untouched; save re-base armed for %d preset(s) of %d",
				FIX_ID, count(candidates), found)
		else
			-- UNKNOWN, and UNKNOWN is not permission. The function filed under
			-- neither the raw value nor the resolved label, or filed nothing, or
			-- threw. Fail closed on BOTH halves — the latch marks us inactive,
			-- which is also what stops the load-time re-base (WhenActive).
			ctx.latch("the shipped AddDomeColonistsModifier files under neither the raw trait id nor its label (game update changed it?)",
				"dome-colonists label behaviour not recognised")
		end
	end,
})

-- One-shot re-base for saves written before this fix reached them. TWO disjoint
-- branches, at most one of which is ever armed:
--
-- (A) the 1.0.7 branch (rebased_from). A Saint who joined a dome under the broken
--     value left a modifier filed on the raw label; the corrected preset alone
--     does not move it, because nothing re-runs Apply on a load.
--     Idempotent, and ALSO one-shot in effect — the two are different properties
--     and the spec asked for both:
--       * the stale removal runs unconditionally. It walks self.labels["Religious"],
--         an array that is empty by definition of this defect, so it cannot subtract
--         morale from anyone, and doing it every time costs nothing;
--       * the RE-APPLY is skipped when this colonist already carries the modifier
--         under the corrected label. Without that check the pass re-applies to every
--         dome Saint on every load forever — harmless (SetLabelModifier is keyed by
--         (label, unit) and REPLACES, so a re-run nets zero, LabelContainer.lua:59-78)
--         but it is NOT one-shot, and it would print its line in every future
--         session's log. ⚠️ That is exactly what this pass did when first built
--         2026-08-02; caught before the batch leg ran, and the check is the same shape
--         Fix_AstrogeologistExtractors used for its own heal. ⚠️ That module was
--         DELETED in hotfix 2 (re-verification row F-5, 1.1.0 rewrote the profile),
--         so the citation is history now, not a live cross-reference — recorded
--         rather than dropped, because it is where this check's shape came from.
--
-- (B) the 1.1.0 branch (rebase_resolved). No stale registration exists to remove —
--     the broken value made the shipped function return before it filed anything —
--     so this half only ADDS what the vanilla fixups failed to add. The label is
--     computed the way the shipped body computes it (Lua/TraitPreset.lua:86) and
--     not from our own data, because on this branch we deliberately left the data
--     alone.
--
-- The log line therefore MEANS something in both cases: it appears only on a save
-- that actually needed healing, and a second load of a healed save is silent.
-- Both reuse vanilla's own application path rather than hand-rolling a modifier,
-- so the id, scale and container stay identical to what a new game produces.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end
	local presets = rawget(_G, "TraitPresets")
	if type(presets) ~= "table" then return end

	if next(rebased_from) then
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
		return
	end

	if next(rebase_resolved) then
		local get_label = rawget(_G, "GetTraitLabel")
		if type(get_label) ~= "function" then return end
		local restored = 0
		AllMapsForEach(true, "Colonist", function(colonist)
			if not IsValid(colonist) or not colonist.dome then return end
			local traits = colonist.traits
			if type(traits) ~= "table" then return end
			local dome = colonist.dome
			-- ipairs, matching the shipped filing site (Colonist.lua:441) and both
			-- fixups (_fixup.lua:2131, :2165): `traits` is a hybrid set+array
			-- (Colonist.lua:493-495) and the array half is the one vanilla walks.
			for _, trait_id in ipairs(traits) do
				if rebase_resolved[trait_id] then
					local p = presets[trait_id]
					if type(p) == "table" and p.modify_target == "dome colonists" then
						local raw = p.modify_trait
						-- the shipped body's own label rule, Lua/TraitPreset.lua:86
						local label = (raw == "") and "Colonist" or get_label(raw)
						local mods = label and type(dome.label_modifiers) == "table"
							and dome.label_modifiers[label]
						if label and not (mods and mods[colonist]) then
							p:AddDomeColonistsModifier(colonist, raw)
							restored = restored + 1
						end
					end
				end
			end
		end)
		if restored > 0 then
			log("%s: restored %d dome blessing(s) an earlier build of this pack stopped the game from registering", FIX_ID, restored)
		end
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
