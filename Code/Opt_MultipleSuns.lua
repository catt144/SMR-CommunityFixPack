-- D04 — OPTIONAL module, OFF BY DEFAULT. Not a bug fix.
--
-- Enable it by setting, before this mod loads (console on the main menu, or a
-- tiny mod that loads first):
--     SMRFixPack_Optional = { MultipleSuns = true }
-- `SMRFixPack.ListFixes()` reports it as inactive with the reason until you do.
--
-- Why it exists: the shipped game hard-limits the Artificial Sun to ONE per
-- colony — it is a `build_once` wonder, enforced colony-wide including
-- construction sites (Building.lua:3691-3692, BuildMenu.lua:711-719 counting
-- UIColony.labels). PT-26 (2026-07-27) proved that makes the pack's original
-- F39 fix unreachable dead code in an unmodded game: two suns can never
-- coexist, so `labels.ArtificialSun[1]` is always the only sun. But players DO
-- run "allow multiple wonders" mods, and any such mod walks straight into the
-- vanilla panel-binding bug this module repairs — so the module ships both
-- halves together: it lifts the limit AND makes the lifted limit actually work.
--
-- WHAT THIS SHIPS:
--
--   1. LIMIT LIFT — `BuildingTemplates.ArtificialSun.build_once = false`,
--      applied on OnMsg.DataLoaded (template presets exist only after
--      DataLoaded — the GlobalMap is EMPTY at mod-load time, the F75 lesson —
--      and the engine re-posts Msg("DataChanged", false) right after every
--      DataLoaded, Dlc.lua:715-717, so the patch re-asserts idempotently). The
--      build menu re-reads CanBuildOnlyOnce() live (verified in-session via a
--      console toggle of this exact flag), so no UI refresh is needed.
--      `wonder` stays true — sight category and placement behavior untouched.
--
--   2. BINDING FIX (absorbed from the deleted Fix_SecondArtificialSun.lua,
--      unchanged) — SolarPanelBase:GameInit (SolarPanel.lua:8-14) only ever
--      tests labels.ArtificialSun[1] with TestSunPanelRange; a panel built in
--      range of sun #2 only never registers (the reverse direction is correct,
--      ArtificialSun.lua:34-48, so the bug shows exactly when the panel is
--      built last — the common case). Chained post-wrapper: the shipped body
--      runs untouched; if it left the panel unlit we walk the rest of the
--      label and hand the first sun in range to the shipped SetArtificialSun
--      (:66-69), which also refreshes production. GameInit is a combined
--      method (DefineCombinedMethod, CommonLua\Classes\_object.lua:22)
--      assembled after mod load, so writing onto SolarPanelBase reaches every
--      panel class and RCSolar. Plus the LoadGame sweep: `artificial_sun` is a
--      persisted member nothing re-evaluates, so panels already dark beside a
--      second sun in a modded save stay dark without one.
--
-- However a save acquired its extra suns (this module, a third-party limit
-- lifter, or a B&B-era import), the resulting state is identical — two suns in
-- city.labels.ArtificialSun — and that state is all the binding fix reads.
-- With the module OFF, vanilla is untouched in both directions: the limit
-- stays, and the binding bug is unreachable without the lift.
--
-- Savegame footprint: none. The lifted limit is a preset patch re-applied per
-- session; suns and panels built under it are ordinary game objects, and a
-- save with two standing suns loads fine without the module (the second sun
-- keeps working — only NEW panels beside it would hit the vanilla binding bug
-- again, and the build menu simply refuses further suns).

SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

local FIX_ID = "MultipleSuns"

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	-- ModLog's output path formats the message a second time (00_Core.lua:18-25).
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

local function module_active()
	local fix = SMRFixPack.fixes[FIX_ID]
	return fix and fix.status == "active"
end

local function find_sun_in_range(panel)
	local city = panel.city
	local suns = city and city.labels and city.labels.ArtificialSun
	if not suns then return end
	for _, sun in ipairs(suns) do
		if IsValid(sun) and TestSunPanelRange(sun, panel) then
			return sun
		end
	end
end

SMRFixPack.Register(FIX_ID, {
	title = "OPTIONAL: build more than one Artificial Sun (and panels bind to any sun in range)",
	apply = function()
		if not SMRFixPack_Optional.MultipleSuns then
			return "opt-in module, off by default — set SMRFixPack_Optional = { MultipleSuns = true } before this mod loads"
		end

		-- the binding-fix half installs now; the limit lift waits for DataLoaded
		local SP = rawget(_G, "SolarPanelBase")
		if type(SP) ~= "table" or type(SP.GameInit) ~= "function"
				or type(SP.SetArtificialSun) ~= "function" then
			return "SolarPanelBase.GameInit/SetArtificialSun not found (game update changed it?)"
		end
		if type(rawget(_G, "TestSunPanelRange")) ~= "function" then
			return "TestSunPanelRange not found (game update changed it?)"
		end

		local orig = SP.GameInit
		function SP:GameInit(...)
			local r = orig(self, ...)
			-- FIX (F39, absorbed): the shipped body only ever tested
			-- labels.ArtificialSun[1].
			if not self.artificial_sun then
				local sun = find_sun_in_range(self)
				if sun then self:SetArtificialSun(sun) end
			end
			return r
		end
	end,
})

-- Limit lift: BuildingTemplates exists EMPTY before DataLoaded, so the patch
-- runs from the messages below. Gating on the registry status covers both the
-- opt-in flag and the SMRFixPack_Disabled veto (a vetoed fix never reaches
-- "active"), which OnMsg handlers must re-check themselves (the F75 lesson).
local lifted_logged = false
local function lift_build_limit()
	if not module_active() then return end
	local templates = rawget(_G, "BuildingTemplates")
	local sun = type(templates) == "table" and templates.ArtificialSun
	if type(sun) ~= "table" then
		local fix = SMRFixPack.fixes[FIX_ID]
		if fix and fix.detail == "" then
			fix.detail = "BuildingTemplates.ArtificialSun not found — build limit NOT lifted (binding fix still active)"
			log("%s: %s", FIX_ID, fix.detail)
		end
		return
	end
	if sun.build_once then
		sun.build_once = false
		if not lifted_logged then
			lifted_logged = true
			log("%s: Artificial Sun build-once limit lifted", FIX_ID)
		end
	end
end

function OnMsg.DataLoaded()
	lift_build_limit()
end

function OnMsg.DataChanged()
	-- fires (with false) right after every DataLoaded and on editor reloads;
	-- re-asserting the one boolean is idempotent
	lift_build_limit()
end

-- Panels built beside a second sun BEFORE this module was enabled (typically
-- under a third-party limit mod) are still dark in the save; nothing re-runs
-- the range test for them.
function OnMsg.LoadGame()
	if not module_active() then return end
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end

	local lit = 0
	AllMapsForEach("map", "SolarPanelBase", function(panel)
		if not panel.artificial_sun then
			local sun = find_sun_in_range(panel)
			if sun then
				panel:SetArtificialSun(sun)
				lit = lit + 1
			end
		end
	end)

	if lit > 0 then
		log("%s: reconnected %d solar panel(s) to an Artificial Sun in range", FIX_ID, lit)
	end
end
