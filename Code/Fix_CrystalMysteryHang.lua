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
--
-- Save footprint / §3a orphan gate (2026-08-13; D13 exposed-set derivation site
-- E5). This module persists nothing of its own — no GameVar, no object field,
-- no mod-created name in the save — but it DOES own a game-time thread body,
-- the repeater closure at :71-85, and a save captures every BLOCKED game-time
-- thread by value, that one included (`agent/facts/EF-023`; the by-name model
-- — "a body written to a global name is not persisted" — is disproven, and the
-- LoadGame comment below used to state it). The body touches only vanilla
-- globals and its own upvalues, which under EF-023 is precisely the shape that
-- KEEPS EXECUTING in an uninstalled player's save instead of dying: an orphan
-- would go on broadcasting CrystalFlyAway hourly for up to its frozen 10-sol
-- deadline. Bounded and silent, but ours and undisclosed — so the body now
-- opens each wake with the FIX_POLICY §3a orphan gate (form copied from
-- `Fix_MeteorStormWedge:154/:165`, the pack's proven precedent). It sets no
-- vanilla state, so a bare `return` satisfies §3a's reset clause vacuously.
-- With the pack installed `SMRFixPack` is always present, the gate is always
-- true, and this module behaves exactly as before.
--
-- ⚠️ Disclosed, NOT repaired here (2026-08-13 — this pass was gate-insertion
-- only; SOURCE-derived, unmeasured, routed to the D13 chain): because persist
-- restores a thread's upvalues BY VALUE, a repeater restored with a save holds
-- its own copies of `repeater_gen`/`my_gen`, while `stop_repeater` below acts
-- on the freshly loaded chunk's locals. So with the pack installed, loading a
-- save taken during an active Crystals mystery leaves the restored repeater
-- running BESIDE the one LoadGame starts — duplicate hourly broadcasts, each
-- lineage still self-limited by the mystery check and its own deadline. Inert
-- (one consumer, and that consumer wants the message), but real.

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
			-- ⛔ orphan gate (FIX_POLICY §3a; header above). Re-checked after the
			-- yield, per the precedent at Fix_MeteorStormWedge:154/:165. No vanilla
			-- state is set here, so a bare return complies vacuously.
			if not SMRFixPack then return end
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
		local err = SMRFixPack.Require("CrystalMysteryHang", {
			{ class = "CrystalsMystery" },
			{ class = "Crystal", method = "ComposeProc" },
		})
		if err then return err end
		-- The handlers below are registered at file scope; nothing else to install.
	end,
})

-- Additive: the shipped code has no CrystalFlyAway handler of its own.
OnMsg.CrystalFlyAway = SMRFixPack.WhenActive("CrystalMysteryHang", function()
	start_repeater() -- re-entrant call from our own Msg is a no-op while running
end)

function OnMsg.MysteryEnd()
	stop_repeater()
end

OnMsg.LoadGame = SMRFixPack.WhenActive("CrystalMysteryHang", function()
	-- bump THIS chunk's generation so a repeater started before the load exits.
	-- ⚠️ It does not reach one RESTORED with the save (own upvalue copies) —
	-- header, "Disclosed, NOT repaired here"; that lineage self-limits.
	stop_repeater()
	if crystals_mystery_active() and not IsValid(UIColony.mystery.crystal) then
		-- the crystal has already left (or has not been composed yet — in which case
		-- nothing is listening and the extra broadcasts are ignored)
		start_repeater()
	end
end)
