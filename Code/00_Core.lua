-- Community Fix Pack — core registry.
--
-- Every fix lives in its own Code/Fix_*.lua file and registers here. Design goals:
--   * Mod-compatible: fixes prefer wrapping/chaining originals over replacement,
--     so other mods that hook the same functions keep working.
--   * Individually disableable: another mod (or the console) can set
--     SMRFixPack_Disabled["<FixId>"] = true BEFORE our code loads to veto a fix.
--   * Fail-safe: a fix that finds the game code in an unexpected state (e.g. a
--     game hotfix already repaired it) deactivates itself instead of erroring.

SMRFixPack_Disabled = rawget(_G, "SMRFixPack_Disabled") or {}

SMRFixPack = rawget(_G, "SMRFixPack") or {
	fixes = {},        -- id -> { title, status, detail }
	order = {},        -- registration order, for ListFixes()
}

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	-- ModLog stores the message unformatted, but its ModPrint output path is a
	-- printf-style CreatePrint (Mod.lua:109-132, lib.lua:164-174) that formats the
	-- single argument AGAIN — a literal '%' in an already-formatted message raises
	-- "bad argument #2" there. Escape it for the second pass.
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

-- Register and immediately apply a fix.
--   id:    stable identifier, matches the Fix_<id>.lua filename
--   def:   { title = <string>, apply = <function> }
-- The apply function runs right away (mod code loads after game code, before
-- any map/savegame). It should return nil/true on success, or a string
-- explaining why it deactivated itself (not an error — e.g. "already fixed").
function SMRFixPack.Register(id, def)
	local entry = { title = def.title, status = "pending", detail = "" }
	SMRFixPack.fixes[id] = entry
	SMRFixPack.order[#SMRFixPack.order + 1] = id

	if SMRFixPack_Disabled[id] then
		entry.status = "disabled"
		log("%s: disabled by user/mod setting", id)
		return
	end

	local ok, res = pcall(def.apply)
	if not ok then
		entry.status = "error"
		entry.detail = tostring(res)
		log("%s: FAILED to apply: %s", id, tostring(res))
	elseif type(res) == "string" then
		entry.status = "inactive"
		entry.detail = res
		log("%s: inactive (%s)", id, res)
	else
		entry.status = "active"
		log("%s: applied", id)
	end
end

-- Console helper: print what the pack did this session.
function SMRFixPack.ListFixes()
	for _, id in ipairs(SMRFixPack.order) do
		local f = SMRFixPack.fixes[id]
		log("%s [%s] %s%s", id, f.status, f.title, f.detail ~= "" and (" — " .. f.detail) or "")
	end
end
