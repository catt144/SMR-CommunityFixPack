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
--   F48  station-connector track elements never re-ordered (paren misplaced)
--   F95  the +10% extractor modifiers OUR OWN deleted module left in saves
--
-- ⛔ 2026-09-09 — WHAT THIS MODULE IS FOR HAS CHANGED, and the note below is now
-- only half the reason it ships. F35 and F48 repair damage only a PRE-1.1.0 save
-- can carry, so their reach is platform-conditional (R-36, below). The F95 pass
-- added today is NOT: it cleans residue this pack itself wrote into 1.1.0 saves,
-- which exist on every platform, Steam included. ⇒ "remove the sanitizer" is no
-- longer a question about 1.0.7 saves. Owner decision, checklist item 126.
--
-- 2026-09-08, game 1.1.0 — WHY THIS MODULE SURVIVED THE REMOVE BLOCK, and why
-- one of its three passes did not (re-verification R-36, owner decision 117).
-- Both remaining passes repair damage that only a PRE-1.1.0 save can carry, and
-- 1.1.0 refuses such a save with `config.OldSavegameBehavior`, which is
-- `Platform.steam and "block" or "warn"` (`Lua/Config/config.lua:175`). On Steam
-- that is a hard block, so these passes are unreachable. OFF Steam it is only a
-- warning and the player may "Load anyway" (`CommonLua/SavegameMetadata.lua:164-175`),
-- which lets a 1.0.7 save and its residue through. The owner has non-Steam
-- players, so the passes stay. ⛔ A colony STARTED on 1.1.0 can never carry this
-- damage: `AppliedSavegameFixups` pre-marks every fixup as applied on a new game
-- (`CommonLua/SavegameFixup.lua:10-16`), so the broken migrations never run for it.
--   * F35 STAYS. 1.1.0 still ships the defect — `WindTurbine.lua:95-105` re-applies
--     `WindTurbine_Diffuser` only, leaving the tech's `WindTurbine` and
--     `WindTurbine_Large` labels unbuffed. The old record claiming vanilla
--     re-applies it was WRONG (corrected by `VANILLA_FIX_QA.md` §0.6).
--   * F48 STAYS. The paren is still misplaced upstream.
--   * F03 REMOVED. Unlike the other two, vanilla now cleans this itself, on
--     exactly the migrated saves that matter: `SavegameFixups.RemoveLeakedUpgradeModifiers`
--     (`Lua/Buildings/Building.lua:1313-1345`) strips leaked `<handle>_upgrade<t>_mod_<i>`
--     entries, keyed on live ownership rather than our handle-resolution test.
--     The leak source is fixed too (`StopUpgradeModifiers` now iterates with
--     `pairs`, `:1303-1311`) — re-verification row R-5, which retired
--     `Fix_UpgradeModifierLeak` in the same pass.
--
-- Both remaining passes are read-only until they find something they can positively
-- identify as wrong, run on every PostLoadGame (after the shipped savegame
-- fixups — see the note on the handler below), and are idempotent — a second
-- run finds nothing. F35 re-derives its answer every load; F48 also
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
--      so it cannot re-run on every load the way F35's comparison does.
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
-- say so, not deactivate the F35 repair alongside it.
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
		log("%s: F48 station-connector pass declined — ProcessTrackElements/ResolveMap not found as globals (a game update moved them); F35 is unaffected", FIX_ID)
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
-- F95 — the +10% extractor bonus OUR OWN deleted module left in players' saves
--
-- ⛔ This pass cleans up after the pack, not after the game. Re-verification row
-- F-5 deleted `Fix_AstrogeologistExtractors` (pack 2dc1dbe) because 1.1.0 rewrote
-- the astrogeologist profile to pay the whole `Extractors` label. But that module
-- had appended two Effect_ModifyLabel entries the shipped profile does not have —
--     AutomaticMetalsExtractor . production_per_day1  +10%
--     MicroGAutoWaterExtractor . water_production     +10%
-- — and applying one calls colony:SetLabelModifier(Label, self, Modifier:new{…})
-- (MarsGameEffects.lua:277-283) into `UIColony.label_modifiers`, which is
-- PERSISTED. Deleting the module does not take them back. `MicroGAutoWaterExtractor`
-- also carries vanilla's `Extractors` label, so an affected save is paying **+30%
-- water where 1.1.0 intends +20%**.
--
-- ⚠️ THE PREMISE IS UNRUN. No save has been loaded on 1.1.0 with this pass in it.
-- What IS established, and how (2026-09-09, link 08):
--   * `label_modifiers` is deserialised, never rebuilt from the presets on load.
--     Vanilla says so in its own words twice — "stored keys are deserialized
--     copies, so match by Label+Prop" (MarsGameEffects.lua:312, :443) — and ships
--     FOUR one-shot SavegameFixups that exist only to strip stale entries
--     (RefreshAstrogeologistExtractorBonus :309, RefreshLoadBalancingAlgorithms-
--     Modifier :396, RefreshExoticMineralMetabolismMalnourishmentModifier :419,
--     RemoveBiomeEngineeringFarmComfortModifier :442). Every one of them would be
--     pointless if a load rebuilt the table.
--   * We measured the same thing at the keyboard on 1.0.7, 2026-08-02 (F95 entry,
--     "THE HEAL WAS NOT IDEMPOTENT"): an identity-keyed presence test read 1 and
--     then 2 after one save+reload. A rebuild would have re-keyed on the LIVE
--     effect object, which that test would have matched, leaving 1. It read 2, so
--     the key present was a deserialised copy.
-- ⇒ the residue is real; what is unobserved is only how many saves carry it.
--
-- ⭐ NARROWER THAN THE RECORD SAYS: both write routes require the colony's
-- commander profile to BE astrogeologist — start-of-game EffectsApply, and the
-- deleted module's own load heal, which returned unless `profile.id` matched. A
-- save on any other profile carries nothing. This pass is inert on those.
--
-- How the entry is identified, and why not by its key alone. Effect_ModifyLabel
-- is not Stackable, so GetLabelModifierId returns `self` — the effect OBJECT
-- (MarsGameEffects.lua:248-255). Our objects were built by a module that no longer
-- exists, so the key cannot be reconstructed. It can still be READ: vanilla's own
-- RefreshAstrogeologistExtractorBonus does exactly that (:325-338), matching the
-- stored key's Label/Prop/Percent/Amount. This pass copies that shape and requires
-- the stored VALUE to match as well:
--   value  m.prop, m.percent == 10, m.amount == 0, and no display_text
--   key    IsKindOf "Effect_ModifyLabel" with the same Label/Prop/Percent/Amount
-- Both must hold. An entry whose value matches but whose key we cannot positively
-- identify is LEFT ALONE and logged — removing something another mod owns is the
-- one failure mode here with no undo.
--
-- ⛔ `display_text` is FALSE, not nil, and testing it against nil would have made
-- this whole pass silently inert. `Modifier` declares `display_text = false` as a
-- class default (Lua/Modifiers.lua:228-235 — the live class; the CommonLua one at
-- CommonLua/Classes/Modifiers.lua:346-348 says "" and is shadowed, the same trap
-- R-31 hit). Our effects set no Reason, so OnApplyEffect never builds one
-- (:270-276) and the field keeps its default. `no_display_text` below accepts all
-- three spellings rather than betting on which class wins.
--
-- Safe to remove: SetLabelModifier(label, id, nil) first un-applies the old
-- modifier from every object currently in the label and THEN deletes the entry —
-- one call does both halves (LabelContainer.lua:59-78). Current membership is the
-- right set, because AddToLabel applies every existing label modifier to a
-- newcomer (:17-28), so every member carries ours. Removal is symmetric with the
-- apply: neither passes `check_if_prop_exists`, so both use the same updater.
--
-- ⚠️ NO ONE-SHOT FLAG, deliberately — this departs from the brief, which specced
-- the F48_FLAG model. Three reasons, in the order that decided it: (1) this is a
-- COMPARISON pass, the same shape as F35 above, which is why F35 carries no flag
-- either — on a clean save it finds nothing and costs two table lookups; (2) the
-- premise is UNRUN, and a flag would permanently lock every already-flagged save
-- out of a corrected pass if the sitting finds this match too narrow; (3) §3a
-- tier 1 — a flag is a new persisted field of ours, and this pass does not need
-- one. A save that somehow re-acquires the residue (a rollback to pack v5 and
-- back) is also repaired, which a flag would prevent.
local F95_RESIDUE = {
	{ label = "AutomaticMetalsExtractor", prop = "production_per_day1", percent = 10 },
	{ label = "MicroGAutoWaterExtractor", prop = "water_production",    percent = 10 },
}

-- nil (never set), false (the live Modifier class default) and "" (the shadowed
-- CommonLua default) all mean "this modifier shows no reason in the UI". A real
-- Reason produces a T() value, which is none of the three.
local function no_display_text(v)
	return v == nil or v == false or v == ""
end

local function remove_astrogeologist_residue()
	local colony = rawget(_G, "UIColony")
	if type(colony) ~= "table" or type(colony.SetLabelModifier) ~= "function" then
		return 0
	end
	local label_modifiers = colony.label_modifiers
	if type(label_modifiers) ~= "table" then return 0 end

	-- Absence-tolerant (§3): with no IsKindOf there is no key-side confirmation,
	-- every candidate becomes a near miss, and the pass removes nothing and says so.
	local is_kind_of = rawget(_G, "IsKindOf")
	local removed, left = 0, 0
	for _, want in ipairs(F95_RESIDUE) do
		-- Collect first, remove after: SetLabelModifier writes to the very table
		-- being walked. (The deleted module's own heal made this mistake's
		-- opposite its rule; keep the shape.)
		local stale, near = {}, 0
		for key, m in pairs(label_modifiers[want.label] or empty_table) do
			if type(m) == "table" and m.prop == want.prop
					and (m.percent or 0) == want.percent
					and (m.amount or 0) == 0
					and no_display_text(m.display_text) then
				if type(is_kind_of) == "function" and is_kind_of(key, "Effect_ModifyLabel")
						and key.Label == want.label and key.Prop == want.prop
						and (key.Percent or 0) == want.percent
						and (key.Amount or 0) == 0 then
					stale[#stale + 1] = key
				else
					near = near + 1
				end
			end
		end
		-- ⛔ EVERY match, not the first. An identity-keyed ancestor of the deleted
		-- module added a fresh +10% on each load — "growing without bound" in its
		-- own words — so one save can hold several entries per label.
		for _, key in ipairs(stale) do
			colony:SetLabelModifier(want.label, key, nil)
		end
		removed = removed + #stale
		left = left + near
		if #stale > 0 then
			log("%s: F95 removed %d leftover +%d%% %s modifier(s) from the %s label — our deleted AstrogeologistExtractors module wrote them; this save was paying a bonus 1.1.0 does not intend",
				FIX_ID, #stale, want.percent, want.prop, want.label)
		end
		if near > 0 then
			log("%s: F95 LEFT %d modifier(s) on the %s label ALONE — the stored value matches ours (+%d%% %s) but the key is not an Effect_ModifyLabel carrying our shape, so it may belong to another mod; please report this line",
				FIX_ID, near, want.label, want.percent, want.prop)
		end
	end
	-- ⛔ Printed even at zero, the same reason F48's total is: the sitting has to
	-- be able to tell "this save was clean" from "the pass never ran", and the
	-- Test Kit's AstrogeologistExtractors probe runs after PostLoadGame, so its
	-- PASS alone cannot separate the two. The per-label lines above are what
	-- separates "clean" from "cleaned".
	log("%s: F95 astrogeologist-residue pass removed %d modifier(s), left %d unidentified",
		FIX_ID, removed, left)
	return removed
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
	RepairStationConnectors = repair_station_connectors,
	RemoveAstrogeologistResidue = remove_astrogeologist_residue,
}

SMRFixPack.Register(FIX_ID, {
	title = "Savegame repair: lost Wind Turbine tech buff, unordered station connectors, our own leftover extractor bonus",
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

	-- F95 runs every load, with no flag — see the pass's own header for why. It
	-- must run AFTER the shipped fixups like the others: on a migrated save
	-- SavegameFixups.RefreshAstrogeologistExtractorBonus (MarsGameEffects.lua:309)
	-- rewrites this very profile's modifiers, and we want the settled state.
	ok, err = pcall(remove_astrogeologist_residue)
	if not ok then log("%s: astrogeologist-residue pass failed: %s", FIX_ID, tostring(err)) end


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
