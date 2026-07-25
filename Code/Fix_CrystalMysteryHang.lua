-- F06: The Philosopher's Stone mystery (Mystery 10) can hang forever at the
-- finale, one step from completion.
--
-- Defect: a one-shot message races a player-gated popup. The composed crystal's
-- thread (Lua\Mysteries\Crystals.lua:45-83) does
--     Msg("CrystalComplete")
--     WaitMsg("CrystalForceFlyAway", const.DayDuration)   -- nothing anywhere emits this
--     Msg("CrystalFlyAway")
-- so exactly one sol after CrystalComplete the crystal announces its departure and
-- is deleted. The scenario (Lua\Scenario\Mystery 10.generated.lua:232-271) reacts
-- to CrystalComplete by granting the wonder tech, then blocks in SA_WaitMessage on
-- the "Epilogue" popup — which the player can minimise and ignore — and only
-- reaches `WaitMsg("CrystalFlyAway")` afterwards. Leave that popup unanswered for
-- more than a sol and the single broadcast has already happened: the scenario waits
-- on a message that will never come again, Msg("MysteryEnd") never fires, and the
-- mystery stays unfinished for the rest of the game. The escape hatch the authors
-- left themselves, CrystalForceFlyAway, has no emitter anywhere in the source.
--
-- Patch approach: additive OnMsg handler plus a game-time thread that re-broadcasts
-- CrystalFlyAway once an hour, so a listener that arrives late still hears it. The
-- crystal's own code is untouched — it has already finished by then. The repeater
-- stops as soon as the mystery ends, when the mystery changes, or after ten sols,
-- and it is restarted on LoadGame (the hang typically outlives a save/reload). The
-- message has exactly one consumer in the shipped content — that WaitMsg — so
-- repeating it cannot do anything else.

local repeater_running = false
local repeater_gen = 0

local function crystals_mystery_active()
	return rawget(_G, "UIColony") and UIColony.mystery and UIColony.mystery_id == "CrystalsMystery"
end

local function stop_repeater()
	repeater_gen = repeater_gen + 1 -- any live thread sees a stale generation and exits
	repeater_running = false
end

local function start_repeater()
	if repeater_running or not crystals_mystery_active() then return end
	repeater_running = true
	repeater_gen = repeater_gen + 1
	local my_gen = repeater_gen
	CreateGameTimeThread(function()
		local deadline = GameTime() + 10 * const.DayDuration
		while GameTime() < deadline and my_gen == repeater_gen do
			Sleep(const.HourDuration)
			if my_gen ~= repeater_gen or not crystals_mystery_active() then break end
			Msg("CrystalFlyAway") -- re-announce for a listener that was still in the Epilogue popup
		end
		if my_gen == repeater_gen then
			repeater_running = false
		end
	end)
end

SMRFixPack.Register("CrystalMysteryHang", {
	title = "The Philosopher's Stone mystery can no longer hang forever at the finale",
	apply = function()
		local M = rawget(_G, "CrystalsMystery")
		if type(M) ~= "table" then
			return "CrystalsMystery not found (game update changed it?)"
		end
		local C = rawget(_G, "Crystal")
		if type(C) ~= "table" or type(C.ComposeProc) ~= "function" then
			return "Crystal.ComposeProc not found (game update changed it?)"
		end
		-- The handlers below are registered at file scope; nothing else to install.
	end,
})

-- Additive: the shipped code has no CrystalFlyAway handler of its own.
function OnMsg.CrystalFlyAway()
	local fix = SMRFixPack.fixes.CrystalMysteryHang
	if not (fix and fix.status == "active") then return end
	start_repeater() -- re-entrant call from our own Msg is a no-op while running
end

function OnMsg.MysteryEnd()
	stop_repeater()
end

function OnMsg.LoadGame()
	local fix = SMRFixPack.fixes.CrystalMysteryHang
	if not (fix and fix.status == "active") then return end
	stop_repeater() -- the thread from before the save is gone
	if crystals_mystery_active() and not IsValid(UIColony.mystery.crystal) then
		-- the crystal has already left (or has not been composed yet — in which case
		-- nothing is listening and the extra broadcasts are ignored)
		start_repeater()
	end
end
