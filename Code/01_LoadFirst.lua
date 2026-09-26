-- LoadFirst — the pack puts itself first in the saved mod load order.
--
-- WHY. Every fix here repairs vanilla code at file scope (FIX_POLICY §1). Loaded
-- FIRST, the pack patches the vanilla it was verified against and every later
-- mod wraps or replaces the repaired code; loaded LATER it wraps code another mod
-- already changed, or declines where a mod swaps a class global while it loads
-- (Passage Network 1.38 replaces the global `Dome` with a function during its
-- load, so F125's and C114's guards read the wrong value and switch off). Owner
-- ruling 2026-09-24/25: vanilla repairs run first; content mods alter the game
-- after us. Design record: docs/agent/reports/LOAD_ORDER_CROSSCHECK_2026-09-24.md
-- (lever "Pack promotes its saved seed through public helpers") and the build
-- report docs/agent/reports/LOAD_ORDER_FIRST_BUILD_2026-09-25.md.
--
-- WHAT THE ORDER IS. Inter-mod load order is the account's saved enable list,
-- `AccountStorage.LoadMods`, copied in order into the loading queue (EF-054;
-- game 1.1.1.405907 CommonLua/Modding/Mod.lua:1995-2000 GetModsEnabledByUser,
-- :1873-1993 GetLoadingQueue). Enabling a mod APPENDS to that list
-- (CommonLua/UI/ModManager.lua:35-37), so a player who enabled this pack after
-- other mods has it loading after them, and the Mod Manager's visible list is a
-- cosmetic sort that cannot show it (EF-054).
--
-- WHAT THIS MODULE DOES, once per launch, while the pack's code loads:
--   1. reads the saved list through the public copy, GetModsEnabledByUser();
--   2. if this pack is not at index 1, rebuilds the list through the helpers the
--      Mod Manager itself uses: TurnModOff(id) for every entry, TurnModOn(this
--      pack), then TurnModOn(each other id) in their old order
--      (ModManager.lua:35-41). Every other mod keeps its relative order; a
--      duplicate id collapses to its first position (insert_unique); the id of
--      an uninstalled mod is kept where it was;
--   3. requests the account save through the only public route a mod has:
--      WriteModPersistentData, whose CHANGED write calls SaveAccountStorage(1000)
--      (Mod.lua:1487-1503). AccountStorage and SaveAccountStorage themselves are
--      blacklisted for mods (EF-096);
--   4. tells the player once, at the pregame menu, that a restart applies it,
--      with the game's own restart routine offered on PC (ModsRestartApp,
--      ModManager.lua:96-121, the routine behind the Mod Manager's own Restart).
--   Already first: nothing is written, no save is requested, nothing is shown.
--
-- WHAT IT CANNOT DO. The running session's order was chosen before any mod code
-- ran (ModsLoaded, Mod.lua:2135-2146); the change applies at the next cold start,
-- and an order-only change never triggers the hot reload (:2104-2112 compares
-- sorted id sets). With `LoadAllMods` set (a developer switch: config.LoadAllMods,
-- or an account flag nothing in the shipped Lua sets) the list is every installed
-- mod in alphabetical order and the saved list is ignored (:1997-1998); this
-- module declines on the config flag by reading it, and on the account flag by a
-- net-zero probe made only when it would otherwise rebuild the list (the stated
-- limit is beside that probe below). A required prerequisite of this pack, should
-- it ever have one, is hoisted ahead of it by the loader whatever the list order
-- (:1966-1983), and a mod that declares this pack as ITS prerequisite is not moved.
-- First file execution is a head start for repairs made at file scope; a repair
-- deferred to a later trigger (DataPatch, OnDataReady) is not thereby promised to
-- precede every content mod's edit of the same data.
--
-- PLAYER CONTROL. Options > Mod Options > "Load this pack first" (default on).
-- Off: this module leaves the saved order alone from then on. On again: it
-- promotes again, at once. Modders and the console keep the veto every fix
-- honours: SMRFixPack_Disabled["LoadFirst"] = true before the pack loads.
--
-- PERSISTENT DATA. This module is the pack's only writer of its per-mod
-- persistent slot (AccountStorage.ModPersistentData[<mod id>], 32 KB cap). Its
-- record is exactly one line, "SMRFixPack.LoadFirst v1 promotions=N …"; every
-- other byte already in the slot is preserved verbatim (other lines, blank lines,
-- the trailing newline), and when the record would not fit nothing is written and
-- nothing foreign is dropped. A later user of the slot must keep this line and
-- put its own on other lines.
--
-- SAVE FOOTPRINT: none. Nothing here touches a map, an object or a game-time
-- thread; the only writes are to account storage (FIX_POLICY §3 does not apply).
--
-- MANIFEST (FIX_POLICY §2b)
-- SRC: none pack infrastructure -- LoadFirst patches no shipped body; it reorders the saved mod list through the game's public helpers

local log = SMRFixPack.Log
local ID = "LoadFirst"
local NOTE_PREFIX = "SMRFixPack.LoadFirst"

-- Process-lifetime state, preserved across a Lua reload the way SMRFixPack is
-- (00_Core.lua:19): a reload re-runs this file, and a promotion already made in
-- this process must not be repeated, nor its notice shown twice.
local state = type(SMRFixPack.LoadFirst) == "table" and SMRFixPack.LoadFirst or {}
SMRFixPack.LoadFirst = state
local loading = true

local function join(list)
	local out = {}
	for i, id in ipairs(list) do out[i] = tostring(id) end
	return table.concat(out, ", ")
end

-- LoadAllMods. That branch of GetModsEnabledByUser (Mod.lua:1997-1998) returns
-- every installed mod id, sorted, and ignores the saved list. config.LoadAllMods
-- is readable and is checked first, before anything else is concluded. The
-- account flag is not readable (AccountStorage is blacklisted), and its list can
-- be IDENTICAL to a normal one (every installed mod enabled, in ascending id
-- order: two mods do it half the time), so on the rebuild path it is told apart
-- by what the helpers see: a probe id appended with TurnModOn shows up in the
-- normal branch's copy and cannot show up in the sorted-keys branch; TurnModOff
-- then removes exactly that id. No helper yields in between, the id is unique to
-- this process, and an id already present is never touched (a matching id seen
-- in the copy already proves the normal branch), so the saved list is
-- byte-identical afterwards and no save is requested.
-- ⚠️ STATED LIMIT: the probe runs only when a rebuild is about to happen. When
-- this pack is already at index 1 nothing is written, so with the account flag
-- set and this pack alphabetically first among installed mods the status line
-- describes the list the game loads, which is then not the saved list. The
-- wording of that line is chosen for that case.
local function config_load_all()
	local cfg = rawget(_G, "config")
	return type(cfg) == "table" and cfg.LoadAllMods and true or false
end

local probe_serial = 0
local function saved_list_is_live()
	probe_serial = probe_serial + 1
	local os_time = type(os) == "table" and os.time
	local probe = string.format("SMRFixPack.LoadFirst.probe.%d.%d",
		type(os_time) == "function" and os_time() or 0, probe_serial)
	local before = GetModsEnabledByUser()
	if type(before) == "table" and table.find(before, probe) then
		return true   -- visible in the copy: the normal branch, and nothing to add
	end
	local seen
	local ok, err = pcall(function()
		TurnModOn(probe)
		local list = GetModsEnabledByUser()
		seen = type(list) == "table" and table.find(list, probe) ~= nil
		TurnModOff(probe)
	end)
	if not ok then
		pcall(TurnModOff, probe)
		return nil, "the saved mod list could not be read through the game's helpers (" .. tostring(err) .. ")"
	end
	return seen and true or false
end

-- PERSISTENT SLOT. Our record is exactly one line matching RECORD_PATTERN; every
-- other byte in the slot belongs to someone else and is kept verbatim: other
-- lines, blank lines, a trailing newline, a line with a longer prefix. The slot is
-- split on "\n" keeping empty pieces, our line (the first match only) is taken
-- out, and the rest is re-joined unchanged behind our new line.
local RECORD_PATTERN = "^SMRFixPack%.LoadFirst v%d+ promotions=%d+"
local function split_slot(data)
	if data == nil then return 0, nil end
	if type(data) ~= "string" then data = tostring(data) end
	local pieces, pos = {}, 1
	while true do
		local nl = data:find("\n", pos, true)
		if not nl then
			pieces[#pieces + 1] = data:sub(pos)
			break
		end
		pieces[#pieces + 1] = data:sub(pos, nl - 1)
		pos = nl + 1
	end
	local promotions, kept, found = 0, {}, false
	for _, piece in ipairs(pieces) do
		if not found and piece:find(RECORD_PATTERN) then
			found = true
			promotions = tonumber(piece:match("promotions=(%d+)")) or 0
		else
			kept[#kept + 1] = piece
		end
	end
	if #kept == 0 then return promotions, nil end
	return promotions, table.concat(kept, "\n")
end

-- Writes a record that differs from the stored one on every promotion, which is
-- what makes the shipped writer request the account save (it returns without a
-- save when the data is unchanged, Mod.lua:1499). The writer refuses an oversized
-- value BEFORE writing (:1494-1496); then nothing is written and nothing foreign
-- is dropped to make room: the rebuilt order stands in memory and the log says the
-- save could not be requested through this route.
local function record_promotion(from, count)
	local _, data = ReadModPersistentData()
	local promotions, rest = split_slot(data)
	local os_time = type(os) == "table" and os.time
	local now = type(os_time) == "function" and os_time() or 0
	local line = string.format("%s v1 promotions=%d last=%d from=%d of=%d",
		NOTE_PREFIX, promotions + 1, now, from, count)
	if rest ~= nil then line = line .. "\n" .. rest end
	return WriteModPersistentData(line)
end

-- THE NOTICE. One real-time thread per pending promotion: it waits for the pregame
-- menu (this title never posts Msg("PreGameMenuOpen"); 00_Core's update report
-- polls the same way), shows the box once and clears the pending flag. A later
-- promotion in the same process, for instance the player turning the option back
-- on after moving the pack, sets the flag again and gets its own thread and box.
-- A Lua reload re-runs this file; the file-scope call below re-arms a thread only
-- when a promotion is still pending and no live thread is waiting for it, so one
-- pending change gets one box, never two.
local NOTICE_TITLE = "Relaunched Fix Pack"
local NOTICE_BODY = "The Relaunched Fix Pack has moved itself to the front of your mod load order, so its repairs are applied before other mods change the same parts of the game. Your other mods keep their order.\n\n"
	.. "This takes effect the next time the game starts.\n\n"
	.. "To keep your own order instead, turn off \"Load this pack first\" under Options > Mod Options > Relaunched Fix Pack."

local function show_notice()
	local title, body = Untranslated(NOTICE_TITLE), Untranslated(NOTICE_BODY)
	local platform = rawget(_G, "Platform")
	local restart = rawget(_G, "ModsRestartApp")
	local wait_question = rawget(_G, "WaitQuestion")
	local wait_message = rawget(_G, "WaitMessage")
	if type(platform) == "table" and platform.pc and type(restart) == "function" and type(wait_question) == "function" then
		local res = wait_question(nil, title, body, "Restart now", "Later")
		if res == "ok" then
			log("%s: player chose Restart now", ID)
			-- the game's own routine (ModManager.lua:96-121): relaunch, then quit();
			-- a pending account save is flushed by quit (AccountStorage.lua:166-187)
			local err = restart(platform.debug)
			if err then
				log("%s: the game could not restart itself: %s", ID, tostring(err))
				if type(wait_message) == "function" then
					wait_message(nil, title, Untranslated("The game could not restart itself ("
						.. tostring(err) .. "). Please close it and start it again yourself."))
				end
			end
		else
			log("%s: player chose Later", ID)
		end
	elseif type(wait_message) == "function" then
		wait_message(nil, title, body)
	end
end

local function notice_thread_alive()
	local is_valid = rawget(_G, "IsValidThread")
	if state.notice_thread ~= nil and type(is_valid) == "function" then
		return is_valid(state.notice_thread) and true or false
	end
	return state.notice_thread_live and true or false
end

local function schedule_notice()
	if not state.pending_notice or notice_thread_alive() then return end
	state.notice_thread_live = true
	state.notice_thread = CreateRealTimeThread(function()
		local deadline = RealTime() + 5 * 60 * 1000
		while RealTime() < deadline and state.pending_notice do
			local get_menu = rawget(_G, "GetPreGameMainMenu")
			if type(get_menu) == "function" and get_menu() then break end
			Sleep(500)
		end
		if state.pending_notice then
			state.pending_notice = false
			Sleep(1000)
			show_notice()
		end
		state.notice_thread_live = false
	end)
end

-- Returns nil when this pack is (now) first in the saved list, else the reason
-- it was left alone. Sets state.detail for ListFixes, and state.pending_notice
-- when a promotion was made by this call.
function state.Promote(trigger)
	local me = rawget(_G, "CurrentModId")
	if type(me) ~= "string" or me == "" then
		return "CurrentModId not found (game update changed the mod environment?)"
	end
	local list = GetModsEnabledByUser()
	if type(list) ~= "table" then
		return "GetModsEnabledByUser returned no list (game update changed it?)"
	end
	local entry = SMRFixPack.fixes[ID]

	local pos = table.find(list, me)
	if not pos then
		state.detail = "cannot apply: this pack is not in the saved mod list"
		log("%s: not applied — %s is not in the saved mod list (%s)", ID, me, join(list))
		return "this pack is not in the saved mod list, so there is nothing to reorder"
	end
	if config_load_all() then
		state.detail = "cannot apply: config.LoadAllMods is set"
		log("%s: not applied — config.LoadAllMods is set; the saved order is untouched (%s)", ID, join(list))
		return "the game is loading every installed mod in alphabetical order (LoadAllMods), so the saved order does not apply"
	end
	if pos == 1 then
		-- nothing is written here, so the account's LoadAllMods flag is not probed;
		-- the line names the list the game loads, which is the saved list unless
		-- that flag is set (see the STATED LIMIT above)
		if not state.promoted then
			state.detail = string.format("first in the list the game loads (%d mods); nothing written", #list)
		end
		if entry then entry.detail = state.detail end
		log("%s: already first of %d (%s); nothing written", ID, #list, join(list))
		return nil
	end
	local live, probe_err = saved_list_is_live()
	if live == nil then
		state.detail = "cannot apply: " .. tostring(probe_err)
		log("%s: not applied — %s; the saved order is untouched (%s)", ID, tostring(probe_err), join(list))
		return tostring(probe_err)
	end
	if not live then
		state.detail = "cannot apply: the account's LoadAllMods flag is set, so the saved list is ignored"
		log("%s: not applied — the account's LoadAllMods flag is set; the saved order is untouched (%s)", ID, join(list))
		return "the game is loading every installed mod in alphabetical order (LoadAllMods), so the saved order does not apply"
	end

	-- Rebuild through the helpers the Mod Manager uses (ModManager.lua:35-41).
	-- Neither helper yields, so no other thread sees the list half-built.
	local before = join(list)
	local wanted = { me }
	for _, id in ipairs(list) do
		if id ~= me then wanted[#wanted + 1] = id end
	end
	local ok, err = pcall(function()
		for _, id in ipairs(list) do TurnModOff(id) end
		for _, id in ipairs(wanted) do TurnModOn(id) end
	end)
	if not ok then
		-- put the player's list back exactly as it was read, then stand down
		pcall(function()
			for _, id in ipairs(list) do TurnModOff(id) end
			for _, id in ipairs(list) do TurnModOn(id) end
		end)
		state.detail = "could not change the saved mod order"
		log("%s: FAILED to rebuild the saved mod list (%s); restored (%s)", ID, tostring(err), before)
		return "could not change the saved mod order (" .. tostring(err) .. ")"
	end
	local after = GetModsEnabledByUser()
	if type(after) ~= "table" or after[1] ~= me then
		state.detail = "could not move this pack to the front of the saved mod order"
		log("%s: FAILED — the list read back as (%s) after the rebuild; it was (%s)", ID, join(after or {}), before)
		return "could not move this pack to the front of the saved mod order (the game rebuilt the list)"
	end

	local save_err = record_promotion(pos, #list)
	if save_err then
		-- the rebuilt order stands in memory; the game's next own account save
		-- carries it, and if none comes this launch the next start promotes again
		-- and says so again. Nothing foreign in the slot was dropped to make room.
		log("%s: moved to the front, but the account save could not be requested through this pack's persistent slot (%s); nothing else was written",
			ID, tostring(save_err))
	end
	state.detail = string.format("moved to the front of the saved mod order (was %d of %d); applies at the next game start", pos, #list)
	state.promoted = { from = pos, count = #list, trigger = trigger }
	if entry then entry.detail = state.detail end
	log("%s: moved to the front of the saved mod order via %s (was %d of %d): %s -> %s; applies at the next game start",
		ID, trigger, pos, #list, before, join(after))
	state.pending_notice = true
	schedule_notice()
	return nil
end

SMRFixPack.Register(ID, {
	title = "Load this pack before other mods (moves it to the front of the saved mod order)",
	optional = true,
	apply = function()
		if not SMRFixPack.OptionEnabled(ID) then
			state.detail = "turned off in Mod Options; the saved order is left alone"
			return "turned off in Mod Options"
		end
		local err = SMRFixPack.Require(ID, {
			{ global = "GetModsEnabledByUser" },
			{ global = "TurnModOn" },
			{ global = "TurnModOff" },
			{ global = "Mods", kind = "table" },
			-- env-side names, rawset per mod by ModDef:SetupEnv (Mod.lua:1628-1645);
			-- Require's global form reads the real _G and cannot see them
			{ test = function() return type(rawget(_G, "CurrentModId")) == "string" end,
			  reason = "CurrentModId not found (game update changed the mod environment?)" },
			{ test = function()
				return type(rawget(_G, "WriteModPersistentData")) == "function"
					and type(rawget(_G, "ReadModPersistentData")) == "function"
			  end,
			  reason = "the per-mod persistent data helpers were not found (game update changed them?)" },
		})
		if err then return err end
		return state.Promote(loading and "startup" or "Mod Options")
	end,
	-- Mod Options toggled back on in a running game: 00_Core's reconciler
	-- re-activates an already-installed entry WITHOUT re-running apply, then calls
	-- this, so the toggle does what it says. Idempotent: already first writes nothing.
	on_activate = function() state.Promote("Mod Options") end,
})

-- run_apply clears entry.detail on success (00_Core.lua); ListFixes should still
-- say what this launch did.
do
	local entry = SMRFixPack.fixes[ID]
	if entry and entry.status == "active" and state.detail then entry.detail = state.detail end
end

-- A Lua reload re-runs this file while a promotion made earlier in the process may
-- still be waiting for the menu: re-arm the notice only if no live thread holds it.
schedule_notice()

loading = false
