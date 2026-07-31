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
-- technique) driven by `SMRFixPack.OnDataReady` — the presets do not exist when
-- mod code loads, so it cannot be done at apply time, and `OnMsg.DataLoaded`
-- alone is not enough: it never fires on the ENABLE path (F87).
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

		local err = SMRFixPack.Require("TechDescriptionBuilding", {
			{ global = "T", reason = "T() not found (game update changed it?)" },
		})
		if err then return err end

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

		-- F87 sweep: this used to hang off OnMsg.DataLoaded alone, which is the
		-- one message that does NOT fire when the player enables the mod at the
		-- main menu — so on every player's first run the description stayed
		-- wrong. OnDataReady adds the enable path's triggers.
		SMRFixPack.OnDataReady(function()
			local ok, res, why = pcall(patch)
			local stats = SMRFixPack.TechDescriptionBuilding
			-- Called more than once per load now. Keep the FIRST verdict, since
			-- a re-run of an already-applied patch legitimately declines with
			-- "description does not carry ..." — but let a real later patch
			-- (Mod Editor reload restoring the shipped text) upgrade it.
			if stats.result == nil or res == "patched" then
				stats.result = ok and (res or why) or tostring(res)
			end
		end)
	end,
})
