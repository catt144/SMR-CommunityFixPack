-- F34(d): the units-underneath sweep on a landscaping site ignores its own
-- filter, so boarding colonists are yanked out of the vehicle they are entering
-- and the same unit can be handled more than once.
--
-- Defect: LandscapeForEachUnit (Lua\Landscape\Landscaping.lua:455-469 on game
-- 1.0.7.396349; :509-523 on 1.1.0.403908) builds a filter and then hands the raw
-- callback to the engine anyway:
--     local passed = {}
--     local function filter_embark(o, ...)
--         if IsValid(o) and not passed[o] and o.command ~= "Embark" then
--             passed[o] = true
--             callback(o, ...)
--         end
--     end
--     Landscape_ForEachObject(landscape, landscape.grid, foreach_params_unit, callback, ...)
--                                                                            ^^^^^^^^
-- `filter_embark` is never used. The function directly above it,
-- LandscapeForEachStockpile (:436-451 on 1.0.7; :490-503 on 1.1.0), is written
-- identically and DOES pass its filter (`filter_parent`) — the slip is a
-- copy-paste, not a decision.
--
-- Two things are lost:
--   * the Embark exclusion. That the exclusion is intended is settled by the
--     ordinary construction site, which applies exactly the same rule to exactly
--     the same question: ConstructionSite:GetUnitsUnderneath passes
--     `exit_impassable_filter`, i.e. `obj.command ~= "Embark"`
--     (Lua\Buildings\ConstructionSite.lua:1713-1720 on 1.0.7; :1905-1912 on 1.1.0);
--   * the `passed` de-duplication — the engine sweep can visit an object more
--     than once, which is why every sibling here keeps that table.
--
-- The consumer on 1.0.7 was LandscapeConstructionSite:GetUnitsUnderneath
-- (LandscapeConstructionSite.lua:21-27), whose list is scattered by
-- ConstructionSite:ScatterUnitsUnderneath (:1722-1740) with
-- `u:SetCommand("ExitImpassable")`. So placing a landscaping job over a rocket,
-- train or shuttle boarding point interrupts the colonists in the middle of
-- boarding it, and does so repeatedly for any unit the sweep reports twice.
--
-- Patch approach: full replacement of the global LandscapeForEachUnit — a copy of
-- the shipped body with the argument corrected, marked -- FIX. The file-local
-- `foreach_params_unit` is reproduced verbatim, a file-local being unreachable
-- from here. Replacement rather than a wrapper because the wrong argument is the
-- whole defect.
--
-- The other three items filed under F34 are NOT patched — see the BUGS.md entry:
-- (a) and (b) are nil-indexes no shipped caller can reach, and (c) would need a
-- behavior change (skipping hexes another mark already owns), not a guard.
--
-- RE-COPIED 2026-09-09 on game 1.1.0.403908 (hotfix2 link 04b, re-verification
-- row F-8, VANILLA_FIX_QA §0.5 + Reader A; owner ruling ck123 = repair, partly
-- reverting ck109's "gate, not repair"). Three-way diff, the archived 1.0.7 tree
-- (C:\Dev\SMR-SrcArchive\1.0.7.396349\Src) against the live 1.1.0 tree against
-- our previous copy: our copy's non-FIX lines matched 1.0.7 byte for byte, and
-- 1.1.0 changed exactly TWO lines of this body —
--     function LandscapeForEachUnit(map, mark, callback, ...)   -- was (mark, callback, ...)
--         local landscape = map.Landscapes[mark]                 -- was Landscapes[mark]
-- because the landscape store moved from a GameVar (a global, lib.lua:1061-1071
-- rawsets it) to `MapVar("Landscapes", {})` (Landscaping.lua:21, registered in
-- MapVarValues, lib.lua:984-999, never in _G). The F34(d) defect line itself
-- (:522, `callback` passed, `filter_embark` unused) is byte-identical on both
-- branches — 1.1.0 did not repair it. The body below is the 1.1.0 one with the
-- one FIX line re-applied. Deliberately NOT carried: nothing; the bodies differ in
-- nothing else.
-- ⚠️ REACH on 1.1.0 is WIDER than on 1.0.7, not narrower. The override moved UP a
-- class: 1.1.0 declares GetUnitsUnderneath on ClearWasteRockConstructionSite
-- (ClearWasteRockConstructionSite.lua:79-85, the one call site in the tree, :81),
-- and LandscapeConstructionSite is its SUBCLASS on both branches
-- (LandscapeConstructionSite.lua:3-4), so flatten/raise/lower sites inherit it —
-- the F115 stack trace is a flatten site reaching :81. On 1.0.7 only
-- LandscapeConstructionSite called this; clear-waste-rock sites used the hex sweep.
--
-- ⛔ BRANCH GUARD (FIX_POLICY §2a, checklist 118): this body is written for 1.1.0
-- and the module must DECLINE on 1.0.7, where our (map, mark, callback) copy over
-- a (mark, callback) caller would shift every argument — F115 in reverse. There is
-- no version field to read (EF-077). Two checks, both testing the thing:
--   1. THE F115 GATE, KEPT, SENSE INVERTED. The measured discriminator
--      (archive/logs/gated110_*: "the global Landscapes table is gone") was "is
--      `Landscapes` a global GameVar (1.0.7) or a registered MapVar (1.1.0)?". It
--      used to APPLY on the GameVar shape because the body was the 1.0.7 one; the
--      body is now the 1.1.0 one, so the same fact now applies on the MapVar shape
--      and declines on the GameVar one. Same registry read (MapVarValues,
--      lib.lua:993-998 is the engine's own "already registered" test), same
--      belt against a stray `Landscapes` global from another mod.
--   2. A behaviour `probe` of the SHIPPED LandscapeForEachUnit on a stub map,
--      applying only if the shipped body reads `map.Landscapes[<mark>]` — the
--      1.1.0 shape (:509-510). The 1.0.7 body binds our stub to `mark` and
--      indexes the GLOBAL, so it never touches the stub (and, before a game
--      starts, throws on the `false` the GameVar holds) — a decline either way.
--      STUB CONTRACT is beside the probe.
-- The verdict is three-valued and the third value is NOT folded into either
-- branch (link 03's F-1 lesson): 1.1.0 shape ⇒ apply; 1.0.7 shape (global
-- present, no MapVar) ⇒ decline, correct, no update_suspect; anything else ⇒
-- decline AND update_suspect, because a body that lives under the 1.1.0 registry
-- yet does not read map.Landscapes is the game having moved again.
--
-- ⛔ NOT tested. Nothing here has run in a game; no landscaping site has been
-- placed on 1.1.0 with this body installed. A boot log line
-- `LandscapeUnitFilter: applied` proves the module loaded, the registry read the
-- 1.1.0 shape and the probe saw the 1.1.0 body — nothing more. The 1.0.7 decline
-- is argued from the archived tree and a desk harness, not from a 1.0.7 boot.
-- ⚠️ tools/sigcheck.py: the MISMATCH it reported on this site while the body was
-- the deliberately-untouched 1.0.7 one is EXPECTED TO CLEAR with this edit (ours
-- and shipped are both (map, mark, callback, ...) now). If it still reports one,
-- that is a finding, not noise.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-09 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Landscape/Landscaping.lua LandscapeForEachUnit sha256=54d26caa5656ab974d05608fdfd6b7e2016c9971a72b606e2016821bed96dffe
--   (Lua/Landscape/Landscaping.lua:509-523 at pin time)
-- DEFECT: Landscape_ForEachObject\(landscape,\s*landscape\.grid,\s*foreach_params_unit,\s*callback,
--   the raw `callback` handed to the engine sweep where the body has just built
--   `filter_embark` for exactly this call; a vanilla fix that passes the filter
--   (as the sibling LandscapeForEachStockpile does, :503) stops the match
-- SRC: Lua/Landscape/Landscaping.lua L505-507 sha256=da6db1e939224a5eabf43153f23884fa7339e4b76d66b57ae0bf8417f3705384
--   (Lua/Landscape/Landscaping.lua:505-507 at pin time). No defect line on
--   purpose: this is the file-local `foreach_params_unit` table reproduced
--   verbatim below, pinned for class (b) only — there is no fault in it to state

SMRFixPack.Register("LandscapeUnitFilter", {
	title = "Landscaping over a boarding point no longer drags boarding colonists out",
	apply = function()
		-- THE DISCRIMINATOR, and why it is this one (F115, 2026-09-08, CONFIRMED
		-- LIVE on 1.1.0, owner repro). The name still exists on both branches, so
		-- `{ global = "LandscapeForEachUnit" }` cannot see a signature change, and
		-- arity is unreadable (`debug.getinfo` is absent in the mod sandbox). What
		-- IS readable is where the landscape store lives:
		--   * GameVar(name, ...) rawsets the global to `false` when it registers
		--     (lib.lua:1061-1071), so on 1.0.7 `Landscapes` is a real global key;
		--   * MapVar(name, ...) registers into MapVars/MapVarValues and NEVER
		--     touches _G (lib.lua:984-999), so on 1.1.0 the global is nil and
		--     MapVarValues.Landscapes is set.
		-- Both run at the top level of Lua/Landscape/Landscaping.lua:21, and
		-- autorun.lua:432-434 runs `dofolder("Lua")` -> `DlcsLoadCode()` ->
		-- `ModsLoadCode()`, so the whole game tree has registered before any line
		-- of ours loads. The registry is therefore populated when this runs.
		local function landscapes_is_per_map()
			-- MapVarValues is the engine's own "already registered" test (lib.lua:993).
			local mvv = rawget(_G, "MapVarValues")
			return type(mvv) == "table" and mvv["Landscapes"] ~= nil
		end
		local function landscapes_is_global()
			-- On 1.0.7 this is `false` until a game starts and a table after — either
			-- way non-nil, because GameVar rawsets it at registration (lib.lua:1071).
			return rawget(_G, "Landscapes") ~= nil
		end
		local function is_107_shape()
			return landscapes_is_global() and not landscapes_is_per_map()
		end

		-- STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3), read from
		-- the shipped 1.1.0 LandscapeForEachUnit (Landscaping.lua:509-523), the
		-- only code this call reaches:
		--   * map            a table whose `Landscapes` field is a table that
		--                    answers nil for the probe mark; the shipped body reads
		--                    `map.Landscapes[mark]` (:510), finds nothing, and
		--                    returns at :512 — BEFORE `passed`, `filter_embark` or
		--                    the engine call Landscape_ForEachObject (:523) exist;
		--   * mark           a string no real landscape can carry (marks are the
		--                    LandscapeMark counter, a number);
		--   * callback       never reached.
		-- Synchronous: no thread, no Msg. Side-effect-free: the one read lands on
		-- the stub. The verdict is WHICH KEY the shipped body asked the stub's
		-- Landscapes table for: the probe mark = it read map.Landscapes[mark] =
		-- 1.1.0; nothing asked = it indexed something else (the 1.0.7 body indexes
		-- the global with our stub as the key) = decline; a throw (the 1.0.7 body
		-- on the `false` the GameVar holds before a game) = decline. Only the
		-- literal `true` applies (00_Core.lua, Require).
		local PROBE_MARK = "SMRFixPack_probe_mark"
		local function shipped_reads_map_landscapes()
			local fn = rawget(_G, "LandscapeForEachUnit")
			if type(fn) ~= "function" then return false end
			local asked
			local stub_map = {
				Landscapes = setmetatable({}, { __index = function(_, k) asked = k return nil end }),
			}
			fn(stub_map, PROBE_MARK, function() end)
			return asked == PROBE_MARK
		end

		local err = SMRFixPack.Require("LandscapeUnitFilter", {
			{ global = "LandscapeForEachUnit" },
			{ global = "Landscape_ForEachObject" },
			-- THE F115 GATE, KEPT (ck123: re-arm ON TOP of the gate, never remove
			-- it), with its sense inverted because the body below is now the 1.1.0
			-- one: apply on the MapVar shape, decline on the GameVar shape. A
			-- `test`, so a decline here does not mark update_suspect by itself —
			-- on 1.0.7 the decline is the CORRECT outcome, not patch rot; the
			-- third-value case is marked by hand below.
			{ test = function() return landscapes_is_per_map() and not landscapes_is_global() end,
			  reason = "the landscape store is a global GameVar, not a per-map MapVar — this copy of LandscapeForEachUnit is written for game 1.1.0 (map, mark, callback) and stands down on an older body" },
			-- FIX (F-8, 2026-09-09) — the branch guard (FIX_POLICY §2a), as a
			-- behaviour probe of the SHIPPED body on a stub map. Contract above.
			{ probe = shipped_reads_map_landscapes,
			  reason = "the shipped LandscapeForEachUnit does not read map.Landscapes[mark] — this copy is written for game 1.1.0 and stands down on a different body" },
		})
		if err then
			-- Three-valued verdict. The 1.0.7 shape is a correct decline and is
			-- NOT patch rot. Anything else that declined — the registry says 1.1.0
			-- but the body does not read map.Landscapes, or neither shape is
			-- present — is a pinned body over a function that moved again, and
			-- must be named in the update report. `run_apply` clears
			-- `update_suspect` only on the ACTIVE branch (00_Core.lua), so a
			-- write before returning survives.
			if not is_107_shape() then
				local entry = SMRFixPack.fixes["LandscapeUnitFilter"]
				if entry then entry.update_suspect = true end
			end
			return err
		end

		-- Reproduced from the file-local at Landscaping.lua:505-507 (1.1.0).
		local foreach_params_unit = {
			accept = { "Unit", },
		}

		-- copy of Lua/Landscape/Landscaping.lua:509-523 (1.1.0), one line changed
		function LandscapeForEachUnit(map, mark, callback, ...)
			local landscape = map.Landscapes[mark]
			if not landscape then
				return
			end

			local passed = {}
			local function filter_embark(o, ...)
				if IsValid(o) and not passed[o] and o.command ~= "Embark" then
					passed[o] = true
					callback(o, ...)
				end
			end
			-- FIX (F34d): was `callback` — the filter above was built and then
			-- never used, so boarding units were reported and duplicates were not
			-- collapsed.
			Landscape_ForEachObject(landscape, landscape.grid, foreach_params_unit, filter_embark, ...)
		end
	end,
})
