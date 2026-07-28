-- Mod Options — the in-game enable surface for the optional modules
-- (Options → Mod Options → Community Fix Pack), added 2026-07-27 (D05).
--
-- Why this file exists: the old "set SMRFixPack_Optional from the console
-- before the mod loads" instruction was unusable — module gates run at mod
-- code load, DURING game startup, before any console exists (and the console
-- platforms Paradox Mods targets have no console at all). The engine's native
-- mod options are the supported path: values persist per account
-- (AccountStorage.ModOptions), are loaded BEFORE mod code so the gates can
-- read them (CommonLua/Classes/Mod.lua:2128-2131, exposed as
-- CurrentModOptions), and the page works with a gamepad on PS/Xbox.
--
-- RULES:
--   * Each toggle's `name` MUST equal the module's SMRFixPack.Register id —
--     00_Core.lua's OptionEnabled/reconcile read them by that id.
--   * Every toggle here must also appear (as false) in metadata.lua
--     `default_options` — that field is what makes the Options screen list
--     the pack at all (ModDef:HasOptions, Mod.lua:473-475).
--   * Toggling takes effect immediately (00_Core's OnMsg.ApplyModOptions
--     reconciliation activates/deactivates the module live); the tooltips
--     stay behavior-only.
return {
	PlaceObj('ModItemOptionToggle', {
		'name', "ClassicRockets",
		'DisplayName', "Classic rockets — refuel while parked",
		'Help', "A player-controlled rocket parked at your colony keeps its launch fuel requested even with no destination selected, so drones keep it fueled while it waits — the original game's behavior.",
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "AcknowledgedWarnings",
		'DisplayName', "Acknowledged warnings",
		'Help', 'Dismissing a "Building Not Working" warning acknowledges the buildings it lists: they stay quiet until they recover (a later breakage warns again), while a NEWLY broken building always warns immediately. Without this, dismissal silences the whole category for 4 game hours and then it returns.',
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "ResidencyControl",
		'DisplayName', "Residency control",
		'Help', 'Adds a per-Dome "Closed to new residents" policy row to the Dome infopanel: no new Colonists move in, while current residents keep commuting, working and using services normally. Not a quarantine — that toggle still exists and still seals the Dome.',
		'DefaultValue', false,
	}),
	PlaceObj('ModItemOptionToggle', {
		'name', "MultipleSuns",
		'DisplayName', "Multiple Artificial Suns",
		'Help', "Lets you build more than one Artificial Sun, and fixes the base-game bug where solar panels only ever check the first sun for night-time light. Turning it off restores the one-per-colony limit (existing suns keep working).",
		'DefaultValue', false,
	}),
}
