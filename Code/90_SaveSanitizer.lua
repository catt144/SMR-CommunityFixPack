-- Save sanitizer — one-shot repair passes for state a bug already baked into a
-- savegame, kept together in one place (FIX_POLICY §3: cleanups are separate,
-- clearly marked and conservative by default).
--
-- Fixes with a live half carry their own LoadGame pass in their own file (F02,
-- F45, F37, F58, F06, F38, F39, F40). This module is for the remainder — damage
-- with nothing left to prevent, only to undo.
--
-- Contents:
--   F35  Large Wind Turbine buff lost by a broken migration fixup
--   F03  upgrade modifiers leaked onto domes and the colony by salvaged buildings
--   F48  station-connector track elements never re-ordered (paren misplaced)
--
-- All three passes are read-only until they find something they can positively
-- identify as wrong, run on every PostLoadGame (after the shipped savegame
-- fixups — see the note on the handler below), and are idempotent — a second
-- run finds nothing. F35 and F03 re-derive their answer every load; F48 also
-- carries a one-shot flag, because its work is a re-ordering rather than a
-- comparison and there is no reason to redo it on a save it has already fixed.

local FIX_ID = "SaveSanitizer"

local log = SMRFixPack.Log

--------------------------------------------------------------------------------
-- F35 — Large Wind Turbines never got their Frictionless Composites buff back
--
-- Defect: SavegameFixups.WindTurbine_Large_ReapplyModifiers
-- (Lua\Buildings\WindTurbine.lua:78-88) exists to re-apply the tech's label
-- modifiers to saves that researched it before the tech data was corrected. The
-- tech carries THREE Effect_ModifyLabel entries — WindTurbine, WindTurbine_Large
-- and WindTurbine_Diffuser, +100% electricity_production each
-- (Data\TechPreset.lua:796-821) — and the fixup re-applies only
-- WindTurbine_Diffuser. Those are disjoint labels (a building is added to a label
-- named after its own class, Building:AddToCityLabels, Building.lua:427-443), so
-- nothing else covers Large turbines: in an affected save they stay unbuffed for
-- the rest of the game. Matches the "polymer upgrade works now, frictionless
-- doesn't" report.
--
-- Repair: for each of the tech's own effects, if the colony carries no
-- electricity_production modifier on that label at all, add the one the effect
-- describes. Driven by the preset rather than a hard-coded list, so a game update
-- that changes the tech changes this pass with it.
--
-- Conservative: the presence of ANY percent modifier for that property on that
-- label is taken as "already buffed" and the label is left alone. That errs
-- towards doing nothing rather than towards double-buffing.
local function repair_turbine_buff()
	local colony = rawget(_G, "UIColony")
	if not colony or type(colony.IsTechResearched) ~= "function"
			or type(colony.SetLabelModifier) ~= "function" then
		return 0
	end
	if not colony:IsTechResearched("FrictionlessComposites") then return 0 end

	local defs = rawget(_G, "TechDef")
	local tech = defs and defs.FrictionlessComposites
	if type(tech) ~= "table" then return 0 end

	local label_modifiers = colony.label_modifiers
	if type(label_modifiers) ~= "table" then return 0 end

	local restored = 0
	for _, effect in ipairs(tech) do
		local label = type(effect) == "table" and effect.Label
		local prop = label and effect.Prop
		local percent = prop and (effect.Percent or 0)
		if label and prop and percent ~= 0 then
			local present = false
			for _, mod in pairs(label_modifiers[label] or empty_table) do
				if type(mod) == "table" and mod.prop == prop and (mod.percent or 0) ~= 0 then
					present = true
					break
				end
			end
			if not present then
				-- Same shape the shipped fixup uses (WindTurbine.lua:81-86); a
				-- stable SMRFixPack_* id instead of its throwaway table, so this
				-- pass can recognise its own work on the next load.
				-- Amount is scaled the way the live tech apply scales it
				-- (Tech.lua:298-301); dormant today — all three effects ship with
				-- Amount 0 — but this pass is preset-driven by design.
				local scale = rawget(_G, "GetModifiablePropScale")
				colony:SetLabelModifier(label, "SMRFixPack_F35_" .. label, {
					amount = (effect.Amount or 0) * (scale and scale(prop) or 1),
					percent = percent,
					prop = prop,
					id = "GameEffect",
				})
				restored = restored + 1
				log("%s: restored the %s buff on the %s label (+%d%% %s)",
					FIX_ID, "Frictionless Composites", label, percent, prop)
			end
		end
	end
	return restored
end

--------------------------------------------------------------------------------
-- F03 — upgrade modifiers left behind by salvaged buildings
--
-- Defect: Building:StopUpgradeModifiers iterated a string-keyed table with
-- ipairs, so it turned nothing off (Building.lua:1268-1274). Fix_UpgradeModifierLeak
-- stops new leaks; this pass clears the ones already in the save.
--
-- A leaked entry is a LabelModifier sitting in some container's
-- `label_modifiers[label]` under the id ApplyUpgrade minted for it,
-- `string.format("%s_upgrade%d_mod_%d", self.handle, tier, i)`
-- (Building.lua:1155). The handle in that id is the OWNING building's. So an
-- entry whose handle no longer resolves to a live object is, by construction,
-- one whose building is gone — the leak — and nothing else in the game writes
-- ids of that shape.
--
-- Conservative: if the handle still resolves to anything valid, the entry is
-- left alone, even though handles can in principle be recycled. A missed leak is
-- cheap; wrongly stripping a live building's upgrade bonus is not.
local UPGRADE_MOD_ID = "^(%d+)_upgrade%d+_mod_%d+$"

local function sweep_leaked_upgrade_modifiers(container)
	local by_label = type(container) == "table" and container.label_modifiers
	if type(by_label) ~= "table" or type(container.SetLabelModifier) ~= "function" then
		return 0
	end
	local handles = rawget(_G, "HandleToObject")
	if type(handles) ~= "table" then return 0 end

	local removed = 0
	for label, modifiers in pairs(by_label) do
		-- collect first: SetLabelModifier writes into this very table
		local stale
		for id in pairs(modifiers) do
			if type(id) == "string" then
				local handle = string.match(id, UPGRADE_MOD_ID)
				local owner = handle and handles[tonumber(handle)]
				if handle and not (owner and IsValid(owner)) then
					stale = stale or {}
					stale[#stale + 1] = id
				end
			end
		end
		for _, id in ipairs(stale or empty_table) do
			container:SetLabelModifier(label, id, nil)
			removed = removed + 1
		end
	end
	return removed
end

local function repair_leaked_upgrade_modifiers()
	local removed = 0

	local colony = rawget(_G, "UIColony")
	if colony then removed = removed + sweep_leaked_upgrade_modifiers(colony) end

	for _, city in ipairs(rawget(_G, "Cities") or empty_table) do
		removed = removed + sweep_leaked_upgrade_modifiers(city)
		local labels = city.labels
		for _, dome in ipairs(labels and labels.Dome or empty_table) do
			removed = removed + sweep_leaked_upgrade_modifiers(dome)
		end
	end

	if removed > 0 then
		log("%s: removed %d leaked upgrade modifier(s) from salvaged buildings", FIX_ID, removed)
	end
	return removed
end

--------------------------------------------------------------------------------
-- F48 — the station-connector migration fixup re-ordered nothing
--
-- Defect (Src-verified 2026-08-11 against 1.0.7.396349):
-- SavegameFixups.A_StationConnectorElements3 (Lua\Buildings\Station.lua:1339-1355)
-- calls, at :1346,
--     ProcessTrackElements(ResolveMap(track, track.elements))
-- with the closing paren one argument too late. `ResolveMap` is a C global taking
-- ONE argument (CommonLua\LuaExportedDocs\Game\realm.lua:92), so `track.elements`
-- is silently dropped; `ProcessTrackElements(map, elements, start_element,
-- adjust_iter)` (Tracks.lua:807) receives nil for `elements`, and `#elements == 0`
-- is true for nil in this engine (:808), so the function returns before doing
-- anything. The migration has therefore never re-ordered a single track element
-- in any save. The correction is the paren:
--     ProcessTrackElements(ResolveMap(track), track.elements)
--
-- Why this ships, and why it did not until now. The entry was `blocked` from
-- 2026-07-25 on the fear that a track the walk cannot complete gets its
-- connections half-rewritten (OrderTrackElements' only failure handling is
-- `assert(false, ...)`, and assert does not unwind here — agent/facts/EF-008).
-- PT-37 measured both halves on 2026-08-05, owner attended, on a copy of the
-- owner's own save (log docs/archive/cb1sitting_Mars.exe-20260805-14.28.49.log):
--   * CASE A, a healthy 280-element track: start_el, end_el, the 1..280 node_idx
--     sequence and the element count were all unchanged, and the connection total
--     moved 559 -> 558 — exactly the 2 x 279 a linear 280-element chain holds, so
--     the call removed one stale or asymmetric connection. It stayed 558 across
--     save + reload. The corrected call is a repair, not merely a no-op.
--   * CASE B, the risky path: a forced meteor produced 8 broken elements and 8
--     repair sites, and the pre-mutation gate still found all 280 elements on the
--     hex grid — HexGetTrackGridElement hands the walk the hidden ORIGINAL
--     element, not the TrackConstructionSite sitting on the same hex. So
--     OrderTrackElements SUCCEEDS on a meteor-damaged track and the assert path
--     is not reachable that way at all. The harness refused to run case B rather
--     than bank a clean pass on an unsampled decider.
-- Owner decision 2026-08-11: SHIP. ⛔ What that evidence does NOT establish is
-- that the assert is unreachable by every route — only by the one the block was
-- written about. Hence the shape below.
--
-- Conservative, in four specific ways:
--   1. It counts an EFFECT, not an execution. Each track's connection total and
--      duplicate-node_idx count are read before and after; a track is counted
--      repaired only if one of them moved. On a save the pass has already fixed
--      the count is 0, which is what makes PT-35's do-no-harm read meaningful.
--   2. It is one-shot per save (a plain SMRFixPack_* boolean on UIColony, absent
--      on saves we have never touched and harmless if the mod is later removed),
--      so it cannot re-run on every load the way F35's and F03's comparisons do.
--   3. Every call is pcall'd per track, so a track that raises costs that track
--      and not the rest of the network — and the raise is logged by name.
--   4. It does NOT hand-assign track.start_el / track.end_el. The shipped fixup
--      does (Station.lua:1347-1348) and ProcessTrackElements sets both itself on
--      the success path (Tracks.lua:820-822); on the FAILURE path the shipped
--      lines would write endpoints derived from an order the engine has just
--      restored, which is strictly worse than leaving them alone.
--
-- ⚠️ ProcessTrackElements / ResolveMap are NOT in this module's apply() Require
-- list, deliberately: if a game update moves them, this pass should decline and
-- say so, not deactivate the F35 and F03 repairs alongside it.
local F48_FLAG = "SMRFixPack_F48_StationConnectors"

-- The signature PT-37 compared. `connections` is rebuilt wholesale by
-- OrderTrackElements (Tracks.lua:578-580, :606-617) and node_idx is renumbered
-- on the success path (:632-635) while the failure path forces start_el.node_idx
-- = 1 (:579) — so a duplicate node_idx is the residue tell, and both numbers
-- together are what "did this call change anything" means for a track.
local function track_signature(track)
	local conn, dup, seen = 0, 0, {}
	for _, el in ipairs(track.elements or empty_table) do
		local n = el.node_idx
		if n ~= nil then
			if seen[n] then dup = dup + 1 end
			seen[n] = true
		end
		conn = conn + #(el.connections or empty_table)
	end
	return conn, dup
end

local function repair_station_connectors()
	local process = rawget(_G, "ProcessTrackElements")
	local resolve = rawget(_G, "ResolveMap")
	if type(process) ~= "function" or type(resolve) ~= "function" then
		log("%s: F48 station-connector pass declined — ProcessTrackElements/ResolveMap not found as globals (a game update moved them); F35 and F03 are unaffected", FIX_ID)
		return 0
	end

	local repaired, walked, raised = 0, 0, 0
	for _, city in ipairs(rawget(_G, "Cities") or empty_table) do
		local labels = city.labels
		for _, track in ipairs((labels and labels.TrackBase) or empty_table) do
			local elements = track.elements
			-- The shipped fixup's own guard (Station.lua:1345).
			if type(elements) == "table" and #elements > 0 then
				walked = walked + 1
				local before_conn, before_dup = track_signature(track)
				local ok, err = pcall(process, resolve(track), elements)
				if not ok then
					raised = raised + 1
					log("%s: F48 pass raised on TrackBase#%s (%d element(s)): %s — that track is left as the engine restored it",
						FIX_ID, tostring(rawget(track, "handle")), #elements, tostring(err))
				else
					local after_conn, after_dup = track_signature(track)
					if after_conn ~= before_conn or after_dup ~= before_dup then
						repaired = repaired + 1
						log("%s: F48 repaired TrackBase#%s — %d element(s), connections %d -> %d, duplicate node_idx %d -> %d",
							FIX_ID, tostring(rawget(track, "handle")), #elements,
							before_conn, after_conn, before_dup, after_dup)
					end
				end
			end
		end
	end
	-- ⛔ Printed even when it is zero, and that is the point: PT-35's do-no-harm
	-- read and the R7 effect rule both need to see a ZERO on a clean save, and an
	-- absence of lines cannot be told from an absence of the pass.
	log("%s: F48 station-connector pass repaired %d of %d track(s) walked (%d raised)",
		FIX_ID, repaired, walked, raised)
	return repaired
end

--------------------------------------------------------------------------------

-- Exposed so the passes can be re-run from the console on a suspect save (and so
-- the Test Kit can drive them). All three return how many things they repaired.
-- ⚠️ RepairStationConnectors deliberately IGNORES the one-shot flag: the flag
-- belongs to the automatic handler, and a direct call that short-circuited on it
-- would return a zero that samples nothing (the PT-35 lesson about a pass that
-- early-returns before its own body).
SMRFixPack.Sanitizer = {
	RepairTurbineBuff = repair_turbine_buff,
	RepairLeakedUpgradeModifiers = repair_leaked_upgrade_modifiers,
	RepairStationConnectors = repair_station_connectors,
}

SMRFixPack.Register(FIX_ID, {
	title = "Savegame repair: lost Wind Turbine tech buff, leaked upgrade bonuses",
	apply = function()
		-- Everything this module touches is savegame state, so there is nothing
		-- to patch at load time. The self-check is that the APIs the passes call
		-- still exist; the game objects themselves are re-checked on every run.
		return SMRFixPack.Require(FIX_ID, {
			{ class = "LabelContainer", method = "SetLabelModifier" },
			{ global = "HandleToObject", kind = "table" },
		})
	end,
})

-- PostLoadGame, NOT LoadGame: UnpersistGame fires Msg("LoadGame"), then runs
-- FixupSavegame, then fires Msg("PostLoadGame") (CommonLua\Savegame.lua:810-813).
-- The F35 pass compensates for SavegameFixups.WindTurbine_Large_ReapplyModifiers,
-- and on the FIRST load of a save that fixup has not yet been applied to, a
-- LoadGame-time pass would run before it: the pass would see the Diffuser label
-- bare and buff it, then the shipped fixup would unconditionally add its own
-- +100% (WindTurbine.lua:80-87 has no already-buffed check) — +200% baked into
-- the save permanently. After fixups the pass sees the world post-migration and
-- the "any percent modifier present → skip" guard holds. (Found by the wave-3
-- QA audit, 2026-07-25.)
OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(repair_turbine_buff)
	if not ok then log("%s: turbine-buff pass failed: %s", FIX_ID, tostring(err)) end

	ok, err = pcall(repair_leaked_upgrade_modifiers)
	if not ok then log("%s: upgrade-modifier pass failed: %s", FIX_ID, tostring(err)) end

	-- F48 is one-shot per save: the flag lives on UIColony, so it travels with
	-- the savegame and a save this pass has already re-ordered is never
	-- re-ordered again. A save from before the pack (or from before this build)
	-- simply has no flag, which is the "tolerate their absence" contract in
	-- FIX_POLICY §3.
	local colony = rawget(_G, "UIColony")
	if type(colony) == "table" and not colony[F48_FLAG] then
		colony[F48_FLAG] = true
		ok, err = pcall(repair_station_connectors)
		if not ok then log("%s: station-connector pass failed: %s", FIX_ID, tostring(err)) end
	end
end)
