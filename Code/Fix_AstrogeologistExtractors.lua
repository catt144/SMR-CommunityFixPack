-- F95: the Astrogeologist profile promises "Extractor production increased by
-- 10%" and pays 10 of the 12 buildable extractors.
--
-- Defect: Data\CommanderProfilePreset.lua:329-390. The profile's `effect` text is
-- UNQUALIFIED — "<bullet> Extractor production increased by 10%" (:333) — and it
-- then enumerates exactly TEN Effect_ModifyLabel entries (:336-385), omitting
-- AutomaticMetalsExtractor (production_per_day1) and MicroGAutoWaterExtractor
-- (water_production). Both are ordinary buildable extractors: neither carries
-- hide_from_build_menu, AutomaticMetalsExtractor sits in build_category
-- "MetalExtractors" with production_per_day1 = 12000
-- (AutomaticMetalsExtractor.generated.lua:9, :11, :56) and MicroGAutoWaterExtractor
-- carries water_production through object_class = "WaterExtractorBase" (:9).
--
-- ⭐ Oversight vs deliberate exclusion is settled by the shared label the
-- designers did NOT use. Sixteen templates carry label = "Extractors"; using it
-- would have added three non-extractors (ConcretePlant, MoholeMine, TheExcavator)
-- and two hidden legacy templates (MicroGExtractor, MicroGAutoExtractor,
-- hide_from_build_menu = true). Every building it would have wrongly added is
-- explained — and every one it would have rightly added is already paid, EXCEPT
-- AutomaticMetalsExtractor. Add MicroGAutoWaterExtractor (a buildable extractor
-- that does not carry the label at all) and the count closes exactly: 12
-- buildable extractors, 10 paid. The list is genuinely curated, and the curation
-- rule is "every buildable extractor, and nothing else". There is no principled
-- line that includes MicroGExtractorExoticMinerals and excludes
-- AutomaticMetalsExtractor.
--
-- Intent tell (self-contradiction): an unqualified promise in the preset's own
-- player-facing text against an enumeration in the same preset that does not
-- deliver it. FIX_POLICY §4's ambiguity rule — prefer the reading proven by
-- sibling code in the same file — reads on the other ten entries, and they say
-- "all buildable extractors".
--
-- ⚠️ The counter-reading is recorded rather than dismissed: a designer COULD have
-- excluded these two as a balance choice, and this is a commander-profile number
-- rather than a broken mechanism. What defeats it is that the exclusion set is
-- otherwise fully explained by two principled rules, and a carve-out for exactly
-- these two — one metals, one water, from different content sets — has no visible
-- logic. This is the package to veto if the owner reads it the other way; nothing
-- else depends on it. Full reasoning on BUGS F95.
--
-- Reachability R1: the profile is a start-of-game commander choice, and any
-- player who picks Astrogeologist and builds either building is short 10%.
--
-- Patch approach: FIX_POLICY §1.1 data/preset patch — the top rung, and ADDITIVE.
-- Two Effect_ModifyLabel entries appended to the profile. The rejected
-- alternative was retargeting the existing WaterExtractor entry at the shared
-- object_class label WaterExtractorBase: neater but WIDER — it would silently
-- enroll any future or mod-added template sharing that object_class, and it edits
-- an entry that works today. Two additive entries change exactly the two
-- buildings named and nothing else.
--
-- ⛔ Built with PlaceObj, never Effect_ModifyLabel:new{} — the F87 rule: apply-time
-- code may not construct a class object, and PlaceObj fails soft where :new
-- throws. Installed through SMRFixPack.DataPatch (latch/heal contract), and the
-- append is idempotent: an entry with the same Label is adopted, never duplicated.
--
-- §3a: nothing that is ours enters the save. A preset-array append plus a
-- synchronous load-time pass that calls vanilla's own effect. No thread, no mod
-- field, no wrapper frame.

local FIX_ID = "AstrogeologistExtractors"
local PROFILE_ID = "astrogeologist"

local log = SMRFixPack.Log

-- The two the shipped enumeration misses. Percent 10 matches all ten siblings.
local MISSING = {
	{ Label = "AutomaticMetalsExtractor", Prop = "production_per_day1", Percent = 10 },
	{ Label = "MicroGAutoWaterExtractor", Prop = "water_production",    Percent = 10 },
}

-- Label -> the Effect_ModifyLabel object that now lives in the profile, whether
-- this load created it or adopted one a previous load left there. The load-time
-- heal needs the object itself, because SetLabelModifier keys the modifier by it.
local owned = {}

-- No `changed_class` filter: CommanderProfilePreset entries are not what
-- DataChanged is usually posted for, and an unfiltered re-check is one table read.
local patch = SMRFixPack.DataPatch(FIX_ID, {
	pass = function(ctx)
		local profiles = rawget(_G, "CommanderProfiles")
		local profile = type(profiles) == "table" and profiles[PROFILE_ID]
		if type(profile) ~= "table" then
			-- Before DataLoaded this just means "presets not loaded yet"; after it,
			-- absence means a future update removed the target (F75 / B3).
			if ctx.data_loaded then
				ctx.patched = true
				ctx.latch("CommanderProfiles." .. PROFILE_ID .. " not found (game update changed it?)",
					"CommanderProfiles." .. PROFILE_ID .. " not found")
			end
			return
		end
		local place = rawget(_G, "PlaceObj")
		if type(place) ~= "function" then
			ctx.patched = true
			ctx.latch("PlaceObj not available (game update changed it?)", "PlaceObj not available")
			return
		end

		-- How many Effect_ModifyLabel entries the profile already has, as the
		-- shape check: if a future patch rewrites this profile wholesale, the
		-- count moving tells us the copy is stale.
		local existing = 0
		for _, effect in ipairs(profile) do
			if type(effect) == "table" and effect.class == "Effect_ModifyLabel" then
				existing = existing + 1
			end
		end
		if existing == 0 then
			ctx.patched = true
			ctx.latch("the " .. PROFILE_ID .. " profile no longer modifies any label",
				PROFILE_ID .. " has no Effect_ModifyLabel entries")
			return
		end

		local changed = 0
		for _, want in ipairs(MISSING) do
			local found
			for _, effect in ipairs(profile) do
				if type(effect) == "table" and effect.class == "Effect_ModifyLabel"
						and effect.Label == want.Label then
					found = effect
					break
				end
			end
			if found then
				-- Either the game shipped it (a future patch fixed this itself) or
				-- an earlier pass in this session added it. Adopt, never duplicate.
				owned[want.Label] = found
			else
				local effect = place("Effect_ModifyLabel", {
					Label = want.Label,
					Prop = want.Prop,
					Percent = want.Percent,
				})
				if type(effect) == "table" then
					profile[#profile + 1] = effect
					owned[want.Label] = effect
					changed = changed + 1
				end
			end
		end
		ctx.patched = true

		if changed > 0 then
			ctx.ever_changed = true
			-- heals ONLY an "inactive" mislabel, never "disabled" (audit A1)
			ctx.heal()
			log("%s: added %d missing extractor entr(y/ies) to the %s profile (%d already present)",
				FIX_ID, changed, PROFILE_ID, existing)
		elseif ctx.ever_changed then
			-- nothing left to change on the DataChanged(false) re-fire is SUCCESS
			-- (the B3 lesson — see SMRFixPack.DataPatch)
			return
		else
			ctx.latch("the shipped profile already pays every buildable extractor", nil, "benign")
		end
	end,
})

-- Existing saves need a heal: profile effects are applied ONCE, at game start
-- (Colony.lua:436 -> GameEffectsContainer:EffectsApply, GameEffect.lua:36-40), so
-- a save begun before this fix never got the two modifiers and correcting the
-- preset alone does not reach it.
--
-- It calls Effect_ModifyLabel's OWN OnApplyEffect rather than hand-rolling a
-- LabelModifier, which keeps the modifier id, scale and container identical to
-- what a new game produces — and makes the heal idempotent for free, since
-- SetLabelModifier is keyed by (label, effect) and replaces. The presence test is
-- belt as well as braces.
--
-- (The F95 spec called that method `__exec`; the shipped name is `OnApplyEffect`
-- — MarsGameEffects.lua:161-172. Same method, same reuse, corrected on the entry.)
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	if not next(owned) then return end
	local get_profile = rawget(_G, "GetCommanderProfile")
	if type(get_profile) ~= "function" then return end
	local profile = get_profile()
	if type(profile) ~= "table" or profile.id ~= PROFILE_ID then return end
	local colony = rawget(_G, "UIColony")
	if type(colony) ~= "table" or type(colony.label_modifiers) ~= "table" then return end

	local healed = 0
	for label, effect in pairs(owned) do
		local mods = colony.label_modifiers[label]
		if not (mods and mods[effect]) then
			effect:OnApplyEffect(colony, profile)
			healed = healed + 1
		end
	end
	if healed > 0 then
		log("%s: applied %d Astrogeologist extractor bonus(es) this save started without", FIX_ID, healed)
	end
end)

SMRFixPack.Register(FIX_ID, {
	title = "The Astrogeologist bonus reaches every buildable extractor, as its own text promises",
	apply = function()
		-- Checked on the class that DECLARES it (the F64 lesson).
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "GetCommanderProfile" },
			{ global = "PlaceObj" },
			{ class = "Effect_ModifyLabel", method = "OnApplyEffect" },
		})
		if err then return err end
		patch()   -- no-op at apply time (F87); the runner fires itself once
		          -- the classes are built AND the presets are loaded
	end,
})
