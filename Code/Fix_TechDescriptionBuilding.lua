-- F25: the "Underground Medium Dome" technology's description names a
-- completely different building.
--
-- Defect: `Data\TechPreset.lua:1484-1493`. The preset's own display_name is
-- "Underground Medium Dome" (:1487) and its single unlock effect is
-- `Effect_TechUnlockBuilding{ Building = "UndergroundDomeMedium" }` (:1491-1493)
-- — a building whose own display_name is likewise "Underground Medium Dome"
-- (Data\BuildingTemplate\UndergroundDomeMedium.lua:22). The description
-- nevertheless opens:
--     "Building: <em>Jumbo Cave Reinforcements</em> (<buildinginfo('UndergroundDomeMedium')>) - A medium-sized Dome for the <em>Underground</em>."
-- The `<buildinginfo(...)>` tag beside it is correct; only the bolded name is
-- wrong, and it names an unrelated thing. Everything else in the sentence — "A
-- medium-sized Dome" — agrees with the building that is actually unlocked, so
-- there is no ambiguity about which half is the mistake.
--
-- Legacy only: the preset carries `condition = function (self) return not
-- UndergroundRework106 end` (:1485), so it exists only for saves made before the
-- 1.0.6 underground rework.
--
-- Patch approach: a preset data patch (FIX_POLICY §1.1 — the most compatible
-- technique) from `OnMsg.DataLoaded`, plus `OnMsg.DataChanged` for Mod Editor
-- reloads. Presets do not exist when mod code loads, so neither can be done at
-- apply time.
--
-- **Localisation, deliberately:** the replacement is built with `T(<the same
-- translation id>, "<corrected English>")`. Reusing id 841885693955 means a
-- localised build still resolves the id in its own translation table and is
-- completely unaffected, while an English build — which falls back to the
-- literal — gets the corrected text. Minting a fresh T instead would have
-- replaced every translated description with an English paragraph, trading a
-- wrong word for a worse regression in every other language. The English string
-- below is byte-identical to the shipped one except for the building name.

SMRFixPack.Register("TechDescriptionBuilding", {
	title = "The Underground Medium Dome tech description names the building it actually unlocks",
	apply = function()
		local TECH = "UndergroundLargeDome"
		local WRONG = "Jumbo Cave Reinforcements"
		local RIGHT = "Underground Medium Dome"
		local TRANSLATION_ID = 841885693955
		local CORRECTED =
			"Building: <em>" .. RIGHT .. "</em> (<buildinginfo('UndergroundDomeMedium')>) - A medium-sized Dome for the <em>Underground</em>.\n\n" ..
			"<grey>With space being the limiting factor below the Martian surface, we have to make the most of every inch we can find.</grey>"

		if type(rawget(_G, "T")) ~= "function" then
			return "T() not found (game update changed it?)"
		end

		-- Returns "patched", or nil plus a reason. Never raises: it runs from a
		-- message handler and reads live preset data.
		local function patch()
			local defs = rawget(_G, "TechDef")
			local tech = type(defs) == "table" and defs[TECH]
			if type(tech) ~= "table" then
				return nil, "tech not present (post-1.0.6 save)"
			end
			local desc = tech.description
			-- A T is a table in this engine and the literal English fallback lives
			-- inside it — at [2] for T(id, text), at [1] for a bare T{text}. Only
			-- patch when the wrong name is really in there; if the layout is not
			-- what we expect, decline rather than guess.
			local found = false
			if type(desc) == "table" then
				for i = 1, 2 do
					if type(desc[i]) == "string" and desc[i]:find(WRONG, 1, true) then
						found = true
						break
					end
				end
			end
			if not found then
				return nil, "description does not carry the literal naming " .. WRONG .. " (already fixed, translated build, or layout changed)"
			end
			tech.description = T(TRANSLATION_ID, CORRECTED)
			return "patched"
		end

		SMRFixPack.TechDescriptionBuilding = { Patch = patch }

		OnMsg.DataLoaded = function()
			local ok, res, why = pcall(patch)
			SMRFixPack.TechDescriptionBuilding.result = ok and (res or why) or tostring(res)
		end
		OnMsg.DataChanged = function()
			pcall(patch)
		end
	end,
})
