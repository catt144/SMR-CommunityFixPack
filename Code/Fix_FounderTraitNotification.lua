-- F23: the "a Founder gained a trait" notification can never fire.
--
-- Defect (`Lua\ColonyViability.lua:282-295`): the category whitelist is written
-- as an ARRAY and then indexed with a group NAME:
--     local FounderGainsTraitCategories = { "Positive", "Negative", "Specialization" }
--     ...
--     TraitPresets[trait_id] and FounderGainsTraitCategories[TraitPresets[trait_id].group]
-- `FounderGainsTraitCategories["Positive"]` is nil — the strings are the VALUES,
-- at integer keys 1..3 — so the condition is false for every trait and the
-- notification is never added.
--
-- Patch approach: additive handler (FIX_POLICY §1.2). `OnMsg` is additive, and
-- the shipped handler is dead rather than wrong, so it can stay exactly where it
-- is: this file adds a second `OnMsg.ColonistAddTrait` with the same conditions
-- and a real set. Nothing shipped is replaced, which is the most compatible
-- outcome — a game hotfix that repairs the array simply makes the shipped
-- handler fire first, and its own `not FindNotification("FounderGainsTrait")`
-- guard is then what stops ours from adding a second one (handlers run in
-- registration order and the shipped one is registered first).
--
-- The conditions are copied verbatim from the shipped handler, including the
-- `init` check (traits granted while the colonist is being created must not
-- notify) and the single-notification guard.

SMRFixPack.Register("FounderTraitNotification", {
	title = "The notification for a Founder gaining a trait fires again",
	apply = function()
		local err = SMRFixPack.Require("FounderTraitNotification", {
			{ global = "FindNotification" },
			{ global = "AddNotification" },
		})
		if err then return err end
		SMRFixPack.FounderTraitNotification = { fired = 0 }
	end,
})

-- The same three groups the shipped array lists, as a set this time.
local FOUNDER_TRAIT_GROUPS = { Positive = true, Negative = true, Specialization = true }

OnMsg.ColonistAddTrait = SMRFixPack.WhenActive("FounderTraitNotification", function(colonist, trait_id, init)
	if init then return end
	if type(colonist) ~= "table" or not colonist.traits or not colonist.traits.Founder then return end
	local presets = rawget(_G, "TraitPresets")
	local preset = presets and presets[trait_id]
	if not preset or not FOUNDER_TRAIT_GROUPS[preset.group] then return end
	if FindNotification("FounderGainsTrait") then return end
	AddNotification("FounderGainsTrait", { obj = colonist, founder = colonist, trait = trait_id })
	local stats = SMRFixPack.FounderTraitNotification
	if stats then stats.fired = stats.fired + 1 end
end)
