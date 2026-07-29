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

-- Pre-load override surface for the optional modules (kept for other mods and
-- power users; regular players use Options → Mod Options — see OptionEnabled).
SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

SMRFixPack = rawget(_G, "SMRFixPack") or {
	fixes = {},        -- id -> { title, status, detail, installed }
	order = {},        -- registration order, for ListFixes()
	defs = {},         -- id -> the Register def (for Mod Options reconciliation)
}
SMRFixPack.defs = SMRFixPack.defs or {}

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	-- ModLog stores the message unformatted, but its ModPrint output path is a
	-- printf-style CreatePrint (Mod.lua:109-132, lib.lua:164-174) that formats the
	-- single argument AGAIN — a literal '%' in an already-formatted message raises
	-- "bad argument #2" there. Escape it for the second pass.
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

-- Is a fix currently active? Optional modules' wrappers consult this at CALL
-- time, so a Mod Options toggle takes effect live in both directions — the
-- installed hooks simply pass through while the module reads inactive.
function SMRFixPack.IsActive(id)
	local f = SMRFixPack.fixes[id]
	return f ~= nil and f.status == "active"
end

-- Is an optional module enabled? Two surfaces, either wins:
--   * SMRFixPack_Optional[id] — the pre-load override table (console, or a
--     tiny mod that loads first);
--   * the player's saved Mod Options toggle. The engine loads those values
--     BEFORE mod code and exposes them env-side as CurrentModOptions
--     (Mod.lua:2128-2131; values rawset directly onto the object, :679-683,
--     so plain indexing is the intended read).
function SMRFixPack.OptionEnabled(id)
	if SMRFixPack_Optional[id] then return true end
	local opts = CurrentModOptions
	return type(opts) == "table" and opts[id] and true or false
end

-- Shared apply runner: Register and the Mod Options reconciliation both route
-- through here so the verdict handling stays identical.
local function run_apply(id, def, entry)
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
		entry.detail = ""
		entry.installed = true
		log("%s: applied", id)
	end
end

-- Register and immediately apply a fix.
--   id:    stable identifier, matches the Fix_<id>.lua / Opt_<id>.lua filename
--   def:   { title = <string>, apply = <function>,
--            -- optional-module extras (D05):
--            optional = <bool>,            -- reconciled with Mod Options
--            on_activate = <function>,     -- after a LIVE activation
--            on_deactivate = <function> }  -- after a LIVE deactivation
-- The apply function runs right away (mod code loads after game code, before
-- any map/savegame). It should return nil/true on success, or a string
-- explaining why it deactivated itself (not an error — e.g. "already fixed").
function SMRFixPack.Register(id, def)
	local entry = { title = def.title, status = "pending", detail = "" }
	SMRFixPack.fixes[id] = entry
	SMRFixPack.defs[id] = def
	SMRFixPack.order[#SMRFixPack.order + 1] = id

	if SMRFixPack_Disabled[id] then
		entry.status = "disabled"
		log("%s: disabled by user/mod setting", id)
		return
	end

	run_apply(id, def, entry)
end

-- Live reconciliation with Options → Mod Options (D05). The engine fires this
-- when it loads our saved options during startup AND every time the player
-- hits Apply on the page (Mod.lua:746, :2170) — CurrentModOptions already
-- holds the new values at that point. Turning a module ON either re-arms its
-- already-installed hooks or runs its apply now; turning it OFF flips the
-- registry status, which every optional module's hooks consult per call
-- (IsActive), so installed wrappers become pass-throughs immediately.
function OnMsg.ApplyModOptions(mod_id)
	if mod_id ~= "SMR_CommunityFixPack" then return end
	for _, id in ipairs(SMRFixPack.order) do
		local def, entry = SMRFixPack.defs[id], SMRFixPack.fixes[id]
		if def and entry and def.optional then
			local want = SMRFixPack.OptionEnabled(id)
			local active = entry.status == "active"
			if entry.status == "disabled" then
				-- FIX (audit 2026-07-29, B1): reconciliation skips vetoed
				-- entries by design, but say so when the player flips the
				-- checkbox, so the dead toggle is diagnosable.
				if want then
					log("%s: Mod Options toggle ignored — vetoed via SMRFixPack_Disabled", id)
				end
			elseif want and not active then
				-- FIX (audit 2026-07-29, B1): "error" entries used to be
				-- excluded here forever, silently — a permanently dead
				-- checkbox until restart. Retry them like an inactive entry
				-- whose hooks never installed, and log a failed attempt.
				if entry.installed and entry.status ~= "error" then
					entry.status, entry.detail = "active", ""
					log("%s: re-activated via Mod Options", id)
				else
					run_apply(id, def, entry)
					if entry.status ~= "active" then
						log("%s: Mod Options toggle could not activate it (status: %s)", id, entry.status)
					end
				end
				if entry.status == "active" and type(def.on_activate) == "function" then
					local ok, err = pcall(def.on_activate)
					if not ok then
						-- FIX (audit 2026-07-29, B1): don't swallow the hook error
						log("%s: on_activate failed: %s", id, tostring(err))
					end
				end
			elseif not want and active then
				entry.status = "inactive"
				entry.detail = "turned off in Mod Options"
				log("%s: deactivated via Mod Options (installed hooks now pass through)", id)
				if type(def.on_deactivate) == "function" then
					local ok, err = pcall(def.on_deactivate)
					if not ok then
						-- FIX (audit 2026-07-29, B1): don't swallow the hook error
						log("%s: on_deactivate failed: %s", id, tostring(err))
					end
				end
			end
		end
	end
end

-- Console helper: print what the pack did this session.
function SMRFixPack.ListFixes()
	for _, id in ipairs(SMRFixPack.order) do
		local f = SMRFixPack.fixes[id]
		-- tolerate nil detail: fixes historically cleared it with nil (PT-51
		-- crash, 2026-07-27), and other mods may write these entries too
		local detail = f.detail or ""
		log("%s [%s] %s%s", id, f.status, f.title, detail ~= "" and (" — " .. detail) or "")
	end
end
