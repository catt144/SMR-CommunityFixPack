-- F83: the First Asteroid popup's three Micro-G Auto Extractor prefabs are lost
-- permanently if its corner notification is left unanswered across a save/load.
--
-- Defect (proven in play, PT-58 2026-07-30 — 1/1/1 without a reload vs 0/0/0
-- after one, same fixture, one variable):
--
--     function OnMsg.SpawnedAsteroid(asteroid)            -- Lua\Asteroids.lua:411-422
--         if UIColony.asteroid_count == 1 then
--             CreateRealTimeThread(function()
--                 WaitPopupNotification("FirstAsteroid", nil, nil, nil, function()
--                     ColonyAddPrefabs("MicroGAutoExtractorExoticMinerals", 1, nil, MainCity)
--                     ColonyAddPrefabs("MicroGAutoExtractorMetals",         1, nil, MainCity)
--                     ColonyAddPrefabs("MicroGAutoExtractorRareMetals",     1, nil, MainCity)
--                 end)
--             end)
--         end
--     end
--
-- The FirstAsteroid preset does not set `start_minimized`, and
-- `ShowPopupNotification` opens immediately only on an explicit `== false`
-- (`Lua\UI\PopupNotification.lua:261`), so the popup ALWAYS arrives as a corner
-- notification. The waiter is a REAL-TIME thread, and real-time threads are not
-- persisted (ENGINE_FACTS: game-time threads persist by default WITH their
-- blocked stacks, real-time threads do not); the popup context is async, so
-- `OnMsg.PersistSave` (:347-355) drops it from `g_PopupQueue` too. The
-- NOTIFICATION does persist — `GameVar("Notifications", {})`, closures included
-- — so after a reload it is still on screen, still clickable, and answering it
-- runs `PopupNotificationEnd` -> `Msg(context.async_signal, i)` with nobody
-- listening. The popup's own `<effect>` line promises the prefabs
-- (`Data\PopupNotifications\PopupNotificationPreset-Asteroid.lua:36`); the
-- preset is `show_once` (:35) and the handler only fires at
-- `asteroid_count == 1`, a counter that never resets — so there is no second
-- chance for the rest of that game, and nothing reports the loss.
--
-- Scope: this is the whole F83 family that costs a player anything, per the
-- popup/deferred-consequence audit (`docs\POPUP_CONSEQUENCE_AUDIT.md` §3.1).
-- The six cosmetic View-button sites lose nothing; storybits, mysteries,
-- sequences and challenges wait in GAME-TIME threads and are save-safe by the
-- engine's own design; `ReconCenterDiscoveryAsteroid` (the second consequential
-- site) is graded separately and is NOT touched here.
--
-- ---------------------------------------------------------------------------
-- Patch approach — SHAPE (i), the load-time heal. FIX_POLICY §1.2 (additive
-- OnMsg handler) + §3 (a separate, clearly marked, conservative one-shot
-- LoadGame sweep).
--
-- On LoadGame, if the FirstAsteroid popup notification is still sitting in the
-- persisted `Notifications` table, its real-time waiter is necessarily dead —
-- that is the stranded state, and nothing else produces it. We then, in order:
--   1. REMOVE the stranded notification. Its `PressFunc` closure is the only
--      thing that can ever re-queue the dead context, so removing it makes a
--      second grant structurally impossible — see "why remove" below.
--   2. grant the same three prefabs the shipped callback would have granted,
--      through the same `ColonyAddPrefabs(..., 1, nil, MainCity)` calls in the
--      same order;
--   3. latch the persistent flag so a repeated save/load cannot grant twice;
--   4. re-show the popup as pure DISPLAY (`ShowPopupNotification`, no wait —
--      its `callback` parameter is dead code, the body never stores or calls
--      it), so the player still gets the story text they were owed. The
--      re-shown notification is built by the shipped function from the shipped
--      preset, so it puts no mod-authored closure into the save.
--
-- The healthy path is untouched: no reload means no LoadGame, so a player who
-- answers the popup normally goes through vanilla and reads 1/1/1.
--
-- WHY REMOVE THE NOTIFICATION rather than just granting alongside it: it is
-- what makes the double-grant impossible in every world. Today vanilla's
-- callback is unreachable anyway (dead thread), but if a future patch moves
-- that waiter to a game-time thread it would persist and still be listening —
-- and then a bare additive grant would pay 2/2/2. With the notification gone,
-- the popup can never be re-queued, so exactly one grant path exists: ours.
--
-- WHY NOT SHAPE (ii), the `show_once` pre-mark (the rejected alternative): an
-- additive `OnMsg.SpawnedAsteroid` that shows the popup itself and then sets
-- `g_ShownPopupNotifications.FirstAsteroid = true` in the same dispatch, so the
-- shipped thread's `ShowPopupNotification` early-returns (:249-251) and its
-- `WaitPopupNotification` reaches `procall(callback, res)` (:302-304)
-- immediately — vanilla grants at spawn. It works on paper and it is why a
-- NAIVE additive grant is wrong (that same always-run procall is the
-- double-grant trap), but it was rejected on three counts: its correctness
-- depends on OnMsg handler order AND on `CreateRealTimeThread` not running the
-- body during the Msg dispatch — a C export whose scheduling is not
-- verifiable from Src, and if it loses that race the player sees two corner
-- notifications; it moves the grant off the healthy path (prefabs arrive at
-- spawn instead of on answer) for every player, fixed or not; and it cannot
-- heal a save that is ALREADY sitting in the stranded state, which shape (i)
-- does.
--
-- KNOWN LIMIT (deliberate, FIX_POLICY §3 "conservative by default"): a player
-- who already answered the dead notification after a reload is past the point
-- where the loss is detectable — the notification is gone and "granted then
-- spent" is indistinguishable from "never granted". Those saves are not
-- healed. Nothing is guessed.
--
-- SAVE FOOTPRINT (FIX_POLICY §3): one new GameVar,
-- `SMRFixPack_FirstAsteroidPrefabs`, boolean. `GameVar` registers it in the
-- real _G and in `PersistableGlobals` (`CommonLua\Core\lib.lua:1040-1055`); a
-- save made with the mod and loaded WITHOUT it is unaffected, because
-- `OnMsg.PersistLoad` only restores names still listed in `PersistableGlobals`
-- (`CommonLua\Core\persist.lua:135-142`) and the stray value is simply ignored.
-- Its absence is tolerated everywhere it is read.

local FIX_ID = "FirstAsteroidPrefabs"
local FLAG   = "SMRFixPack_FirstAsteroidPrefabs"

-- The shipped callback's three grants, in its order (Asteroids.lua:416-418).
local PREFABS = {
	"MicroGAutoExtractorExoticMinerals",
	"MicroGAutoExtractorMetals",
	"MicroGAutoExtractorRareMetals",
}

-- Persistent, absent-tolerant once-flag. Declared at file scope so the name is
-- registered before any NewGame / persist pass.
GameVar(FLAG, false)

local log = SMRFixPack.Log

local function get_flag()
	-- safe_rawget falls through to the real _G for a name our env does not hold
	return rawget(_G, FLAG) and true or false
end

local function set_flag(value)
	-- ENGINE_FACTS: rawset from mod code writes only into our own env table, so
	-- clear any shadow first and then assign — plain assignment goes through
	-- ModEnvMeta.__newindex (Mod.lua:1557-1563) into the REAL _G. The write is
	-- permitted because GameVar put the name in PersistableGlobals (:1559).
	rawset(_G, FLAG, nil)
	_G[FLAG] = value
end

-- The localization id of the FirstAsteroid popup body text, read from the LIVE
-- preset rather than hardcoded. Two facts force this indirection:
--   * the preset id is NOT on the notification instance — ShowPopupNotification
--     nils `instance.id` before AddNotification (PopupNotification.lua:286),
--     because AddNotification asserts an id-less instance;
--   * T table identity does not survive a load, and in a retail build T() can
--     return light userdata instead of a table when the id is in the
--     translation table (localization.lua:268). `TGetID` (:48) is the accessor
--     that handles both forms.
local function first_asteroid_loc_id()
	local presets = rawget(_G, "PopupNotificationPresets")
	local preset = type(presets) == "table" and presets.FirstAsteroid or nil
	local TGetID = rawget(_G, "TGetID")
	if type(preset) ~= "table" or type(TGetID) ~= "function" then return nil end
	local id = TGetID(preset.text)
	return type(id) == "number" and id or nil
end

-- The stranded FirstAsteroid corner notification, or nil. Popup notifications
-- are added with a nil id (PopupNotification.lua:288), so they all live in the
-- "" bucket of the Notifications GameVar; `popup_notification` reaches the
-- instance from the context (:40 + the table.append at :285).
local function find_stranded_notification()
	local loc_id = first_asteroid_loc_id()
	if not loc_id then return nil end
	local notifications = rawget(_G, "Notifications")
	local list = type(notifications) == "table" and notifications[""] or nil
	if type(list) ~= "table" then return nil end
	local TGetID = rawget(_G, "TGetID")
	for _, n in ipairs(list) do
		if type(n) == "table" and n.popup_notification and TGetID(n.text) == loc_id then
			return n
		end
	end
	return nil
end

-- The sweep itself. Returns the number of prefab grants performed (0 when
-- there is nothing to heal) plus a reason string — the TestKit probe drives
-- this directly with planted globals.
function SMRFixPack.HealFirstAsteroidPrefabs()
	if get_flag() then
		return 0, "already granted in this game"
	end
	local notification = find_stranded_notification()
	if not notification then
		return 0, "no stranded First Asteroid notification"
	end

	local add = rawget(_G, "ColonyAddPrefabs")
	local city = rawget(_G, "MainCity")
	if type(add) ~= "function" or not city then
		return 0, "grant path unavailable"
	end

	-- 1. kill the only route back to the dead context (see the header)
	local remove = rawget(_G, "RemoveNotification")
	if type(remove) == "function" then
		remove(notification)
	end

	-- 2. the grant the popup's own text promised
	for _, prefab in ipairs(PREFABS) do
		add(prefab, 1, nil, city)
	end

	-- 3. never twice, however often this save is reloaded
	set_flag(true)

	-- 4. give the player back the story popup, as pure display
	local show = rawget(_G, "ShowPopupNotification")
	if type(show) == "function" then
		show("FirstAsteroid")
	end

	log("%s: First Asteroid prefabs recovered after a save/load (%d granted)", FIX_ID, #PREFABS)
	return #PREFABS, "granted"
end

SMRFixPack.Register(FIX_ID, {
	title = "The First Asteroid prefabs still arrive if the popup was left unanswered across a save/load",
	apply = function()
		-- Everything the sweep needs is game code loaded before us. On a cold
		-- boot the presets are NOT loaded yet (the GlobalMap exists but is EMPTY
		-- until DataLoaded), so the FirstAsteroid preset itself is checked from
		-- the OnDataReady block below, never here — the F75 false-inactive
		-- lesson. (On the enable path they ARE loaded here; the check still
		-- belongs there, which is why OnDataReady covers both — F87.)
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "ColonyAddPrefabs" },
			{ global = "TGetID" },
			{ global = "ShowPopupNotification" },
			{ global = "RemoveNotification" },
			{ global = "PopupNotificationPresets", kind = "table" },
		})
		if err then return err end
		-- The LoadGame handler below is registered at file scope; nothing else
		-- to install.
	end,
})

-- F87 sweep: OnMsg.DataLoaded alone never fires on the enable path, so this
-- self-check silently skipped the session in which the player enables the mod —
-- the fix would have reported `active` on a preset it never verified.
SMRFixPack.OnDataReady(function()
	local entry = SMRFixPack.fixes[FIX_ID]
	if not entry or entry.status == "disabled" then return end
	-- After DataLoaded a missing preset really does mean a future update removed
	-- it, and the sweep would have nothing to match on (the B3 lesson: silence
	-- would otherwise report `active` forever on a target that is gone).
	if first_asteroid_loc_id() then
		if entry.status == "inactive" and entry.detail == "the FirstAsteroid popup preset no longer exists" then
			entry.status, entry.detail = "active", ""   -- "" not nil: ListFixes concatenates it
		end
	elseif entry.status == "active" then
		entry.status = "inactive"
		entry.detail = "the FirstAsteroid popup preset no longer exists"
		log("%s: inactive (the FirstAsteroid popup preset no longer exists)", FIX_ID)
	end
end)

-- WhenActive carries both FIX_POLICY §2 checks (registry status + the veto
-- re-read this handler used to do by hand).
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	SMRFixPack.HealFirstAsteroidPrefabs()
end)
