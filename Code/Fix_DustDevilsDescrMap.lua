-- F93: the dust-devil scheduler reads its descriptor from the map the PLAYER IS
-- LOOKING AT, not the map it spawns on.
--
-- Defect: the scheduler thread pins its map on its second line — `local map =
-- MainMap` (Lua\DustDevils.lua:198) — and uses that local everywhere:
-- HasDustStorm(map) (:209, :220), map:MapForEach (:200),
-- GetRandomPassableAwayFromBuilding(map) (:223), GenerateDustDevilIn(pos, map,
-- descr) (:227). Its descriptor getter is the one thing that ignores it.
-- GetDustDevilsDescr (:58-66) takes no map argument at all and reads the global
-- view variable CurrentMap twice.
--
-- CurrentMap is the map the CAMERA is on — ChangeCurrentMapSlot -> SetCurrentMap
-- (CommonLua\Core\map.lua:389-404, :134-144), which is exactly what switching to
-- the underground view does. And the scheduler RE-READS the descriptor every
-- cycle (:234-238), so whichever map the player happens to be viewing at that
-- moment supplies the surface's disaster settings. Two outcomes, both wrong:
--   * the viewed map's setting is "disabled" -> nil -> the scheduler enters its
--     `while not new_descr do Sleep(const.DayDuration) end` retry and stops
--     producing dust devils a day at a time until the player looks at the
--     surface again;
--   * it is any other value -> the surface silently adopts THE OTHER MAP'S
--     intensity for its next wave.
--
-- Intent tell (sibling contradiction, and it is inside the same function's
-- caller): every other map reference in this thread goes through the `map` local
-- the thread declared for the purpose. This is the F31 shape exactly — a global
-- map used where a correct map is already in scope. The getter's SIGNATURE is
-- the giveaway: it cannot be right for a non-current map because it has no way
-- to be told which map it is for.
--
-- Reachability R1: the re-read is on the normal loop, once per wave, forever.
-- The underground is native content in Relaunched and players spend long
-- uninterrupted stretches viewing it. All three callers of GetDustDevilsDescr
-- are inside this one MainMap thread (:193, :234, :237) — enumerated;
-- Cheats.lua:47-53 does its own CurrentMap read and does NOT call this function.
--
-- Patch approach: FIX_POLICY §1.4b global-function replacement WITH A BODY COPY.
-- The defect is a mid-body read, so it is not hookable, and §1.4b's own "prefer a
-- wrapper unless" test selects the copy here — there is no result to widen and no
-- input to narrow from outside. Seven lines, copied byte-identical from
-- Lua\DustDevils.lua:58-66 (shipped Src, game 1.0.7.396349) with CurrentMap ->
-- MainMap on both reads and nothing else changed.
--
-- Why MainMap and not the caller's map: the only consumer is the thread that
-- already pinned `local map = MainMap`, so this makes the getter agree with its
-- sole caller. If a future caller needs another map it can pass one; this fix
-- deliberately does not invent a parameter it would then have to guess a default
-- for.
--
-- §3a: NOTHING ENTERS THE SAVE. The function is synchronous and is called from
-- the persisted DustDevils game-time thread only BETWEEN its Sleeps, so our frame
-- is never on the stack at a yield (route a); the thread's locals hold the
-- returned descriptor TABLE, not our function (route b); and we store nothing
-- (route c).

local FIX_ID = "DustDevilsDescrMap"

-- The shipped body, with the two CurrentMap reads corrected. Marked -- FIX on the
-- changed lines only.
local function fixed_get_dust_devils_descr()
	if MainMap.mapdata.MapSettings_DustDevils == "disabled" then -- FIX (F93): was CurrentMap
		return
	end

	local data = Presets.MapSettings.DustDevils
	local orig_data = data[MainMap.mapdata.MapSettings_DustDevils] or data["DustDevils_VeryLow"] -- FIX (F93): was CurrentMap
	return OverrideDisasterDescriptor(orig_data)
end

local orig            -- vanilla's body, captured at apply
local installed = false

local function set_installed(want)
	if not orig then return end
	local cur = rawget(_G, "GetDustDevilsDescr")
	if want and cur ~= fixed_get_dust_devils_descr then
		_G.GetDustDevilsDescr = fixed_get_dust_devils_descr
	elseif not want and cur == fixed_get_dust_devils_descr then
		_G.GetDustDevilsDescr = orig
	end
end

-- The spec's self-check is "the global exists AND Presets.MapSettings.DustDevils
-- is populated". The first half belongs at apply; the second CANNOT, and putting
-- it there would be the F75 false-inactive bug — presets do not exist when mod
-- code loads on a cold boot, so absence proves nothing until DataLoaded has
-- fired. It runs here instead, on the shared runner that owns both the F75 gate
-- and the F87 enable-path triggers. On a latch the vanilla body is RESTORED, so
-- an entry reporting `inactive` is never quietly still installed.
-- No `changed_class` filter on purpose: the presets in this group are instances
-- of the SUBCLASS MapSettings_DustDevils (DustDevils.lua:1) while the group lives
-- under the root preset class MapSettings, so a class-name filter could miss its
-- own re-arm. An unfiltered re-check is one cheap table read.
local verify = SMRFixPack.DataPatch(FIX_ID, {
	pass = function(ctx)
		if not installed then return end   -- apply() already declined; nothing to verify
		local presets = rawget(_G, "Presets")
		local settings = type(presets) == "table" and presets.MapSettings
		local group = type(settings) == "table" and settings.DustDevils
		if type(group) ~= "table" or not next(group) then
			-- Before DataLoaded this just means "presets not loaded yet".
			if ctx.data_loaded then
				ctx.patched = true
				set_installed(false)
				ctx.latch("Presets.MapSettings.DustDevils not found (game update changed it?)",
					"Presets.MapSettings.DustDevils not found")
			end
			return
		end
		ctx.patched = true
		set_installed(true)
		ctx.heal()
	end,
})

SMRFixPack.Register(FIX_ID, {
	title = "Dust devils on the surface use the surface's settings, not the map the camera is on",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "GetDustDevilsDescr" },
			-- the copied body calls it; if it is gone, the copy is wrong anyway
			{ global = "OverrideDisasterDescriptor" },
		})
		if err then return err end
		orig = orig or rawget(_G, "GetDustDevilsDescr")

		-- §1.4b: plain assignment reaches the real _G through ModEnvMeta.__newindex,
		-- and the rawget read-back confirms the write landed (the F22 donor).
		local fail = SMRFixPack.SetGlobal("GetDustDevilsDescr", fixed_get_dust_devils_descr)
		if fail then return fail end
		installed = true
		verify()  -- no-op at apply time (F87); the runner fires itself once the
		          -- classes are built AND the presets are loaded
	end,
})
