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
	fixes = {},        -- id -> { title, status, detail, installed, update_suspect }
	order = {},        -- registration order, for ListFixes()
	defs = {},         -- id -> the Register def (for Mod Options reconciliation)
}
SMRFixPack.defs = SMRFixPack.defs or {}

-- The one true logger — Phase 4 (audit C2) hoisted the copy previously cloned
-- in 11 fix files; migrated call sites alias it (`local log = SMRFixPack.Log`).
function SMRFixPack.Log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	-- ModLog stores the message unformatted, but its ModPrint output path is a
	-- printf-style CreatePrint (Mod.lua:109-132, lib.lua:164-174) that formats the
	-- single argument AGAIN — a literal '%' in an already-formatted message raises
	-- "bad argument #2" there. Escape it for the second pass.
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end
local log = SMRFixPack.Log

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

-- ===== shared self-check helpers (Phase 4, audit C2/C4) ======================

-- Walks a classdef's __parents chain looking for the class that DECLARES
-- `method`. Diagnostic only: mod code runs before class flattening, so a class
-- global is a plain classdef exposing only self-declared members
-- (ENGINE_FACTS) — a check against the wrong class reads nil and would
-- otherwise masquerade as "game update changed it" (how F64 shipped broken).
-- classdefs carry __parents (classes.lua:61); post-flattening the walk is
-- harmless and simply finds the baked copy on the class itself first.
local function find_declaring_ancestor(class_name, method, seen)
	seen = seen or {}
	if seen[class_name] then return nil end
	seen[class_name] = true
	local C = rawget(_G, class_name)
	if type(C) ~= "table" then return nil end
	if rawget(C, method) ~= nil then return class_name end
	local parents = rawget(C, "__parents")
	if type(parents) == "table" then
		for _, p in ipairs(parents) do
			local found = find_declaring_ancestor(p, method, seen)
			if found then return found end
		end
	end
	return nil
end

-- Declarative preflight checker. `spec` is a LIST of checks evaluated in
-- order; the FIRST failure returns its reason string (pass `reason` wherever a
-- site's historical string differs from the generated convention — reason
-- strings are an interface and are preserved byte-for-byte). Returns nil when
-- every check passes. A failure also marks the fix entry `update_suspect` for
-- the C1 deactivation report.
--
-- Check forms (each takes an optional `reason`):
--   { global = "Name" }                    -- rawget(_G, Name) is a function
--   { global = "Name", kind = "table" }    -- ... is a table
--   { global = "Name", kind = "any" }      -- ... is not nil
--   { class = "Building" }                 -- the class table exists
--   { class = "Building", method = "X" }   -- the DECLARING class check: plain
--        -- index, which pre-flattening sees only self-declared members. If it
--        -- fails but an ancestor declares X, a LOUD authoring-error line is
--        -- logged so a wrong-class check can never masquerade as patch rot.
--   { path = {"const","Scale","Stat"}, kind = "number"|"function"|"table"|"any" }
--   { test = function() return truthy end, reason = "..." }  -- content checks
function SMRFixPack.Require(id, spec)
	for _, c in ipairs(spec) do
		local ok, name
		if c.test then
			ok = c.test()
			name = "(custom check)"
		elseif c.global then
			local v = rawget(_G, c.global)
			local kind = c.kind or "function"
			ok = (kind == "any") and v ~= nil or type(v) == kind
			name = c.global
		elseif c.class and c.method then
			local C = rawget(_G, c.class)
			ok = type(C) == "table" and type(C[c.method]) == "function"
			name = c.class .. "." .. c.method
			if not ok and type(C) == "table" then
				local declaring = find_declaring_ancestor(c.class, c.method)
				if declaring and declaring ~= c.class then
					log("%s: self-check targets %s but %s declares %s — authoring error, not a game update (FIX_POLICY §2)",
						tostring(id), c.class, declaring, c.method)
				end
			end
		elseif c.class then
			ok = type(rawget(_G, c.class)) == "table"
			name = c.class
		elseif c.path then
			local v
			for i, k in ipairs(c.path) do
				if i == 1 then
					v = rawget(_G, k)
				elseif type(v) == "table" then
					v = v[k]
				else
					v = nil
				end
			end
			local kind = c.kind or "any"
			ok = (kind == "any") and v ~= nil or type(v) == kind
			name = table.concat(c.path, ".")
		end
		if not ok then
			local entry = id and SMRFixPack.fixes[id]
			if entry then entry.update_suspect = true end
			return c.reason or (name .. " not found (game update changed it?)")
		end
	end
end

-- Global replacement with the read-back verification FIX_POLICY §1.4b
-- requires (the F22 donor): plain assignment reaches the real _G through
-- ModEnvMeta.__newindex; rawget confirms the write landed. Returns nil on
-- success, the failure reason otherwise.
function SMRFixPack.SetGlobal(name, value, reason)
	_G[name] = value
	if rawget(_G, name) ~= value then
		return reason or ("could not install the " .. name .. " replacement")
	end
end

-- Wraps a handler so it runs only while the fix is active AND not vetoed —
-- FIX_POLICY §2 requires BOTH checks in every OnMsg handler (the A1 lesson).
-- Register latches status "disabled" for a pre-load veto, so the status read
-- already honours it; the separate table read also covers a mid-session veto.
function SMRFixPack.WhenActive(id, fn)
	return function(...)
		local f = SMRFixPack.fixes[id]
		if not (f and f.status == "active") then return end
		local disabled = rawget(_G, "SMRFixPack_Disabled")
		if type(disabled) == "table" and disabled[id] then return end
		return fn(...)
	end
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
