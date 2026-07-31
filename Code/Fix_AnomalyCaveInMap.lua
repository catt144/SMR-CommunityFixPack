-- F31: the anomaly cave-in sequences hardcode the global `UndergroundMap`
-- instead of using the map the sequence is running on, and `TriggerCaveIn` then
-- indexes it without checking.
--
-- Defect: `TriggerCaveIn(map, pos)` (Lua\Buildings\CaveInRubble.lua:94-117)
-- guards its `pos` argument and nothing else:
--     if not pos then
--         assert(pos)
--         return nil
--     end
--     pos = SnapWorldToHex(pos)
--     local strut = map:MapFindNearest(pos, "map", "SupportStruts")
-- The second line is an unguarded method call on `map`. `UndergroundMap` is a
-- **GameVar defaulting to `false`** (RandomMapGenerator_Picard.lua:263) and stays
-- false whenever the underground map was never generated —
-- `GenerateAdditionalMaps` returns immediately under the "No Underground and
-- Asteroids" game rule (:266). Handed `false`, `map:MapFindNearest` raises
-- (indexing a boolean is one of the things this engine does NOT tolerate, cf.
-- F33) and takes the running anomaly sequence down with it.
--
-- Wider than the tracker recorded: **eight** call sites pass the global rather
-- than the sequence-local `map`, across four scenario files —
-- `UndergroundAnomalies.generated.lua:240`,
-- `BuriedWonder_Jumbo_Cave.generated.lua:340,539,769`,
-- `BuriedWonder_Jumbo_Cave_106.generated.lua:339,538,768` and
-- `BuriedWonder_Cave_Of_Wonders.generated.lua:430` (which passes it twice, also
-- to `FindCaveInLocation`). The engine's own callers do it properly:
-- `Marsquake.lua:266` passes the local `map` and `:287` passes `CurrentMap`.
--
-- Patch approach: a chained wrapper on the global `TriggerCaveIn` that declines
-- when it is handed something it cannot use, exactly as the shipped body already
-- declines a missing `pos`. This is the F66 pattern — the function states the
-- invariant for one argument and simply does not check the other — and it is the
-- whole of the repair: when `map` is a real map nothing changes, and when it is
-- not, a hard raise mid-sequence becomes a no-op that lets the anomaly finish.
--
-- *Implemented differently, on better evidence:* the tracked sketch was "wrap
-- `TriggerCaveIn(map, pos)`: reject `map.mapdata.Environment ~= "Underground"`".
-- (CORRECTED by the QA audit 2026-07-25: an earlier version of this paragraph
-- claimed the sketch would cancel marsquake cave-ins — false; every engine
-- caller is already Underground-gated, Marsquake.lua:285/:294/:323-325, so the
-- environment test would have been a no-op for them.) The real problem with the
-- sketch is that `map.mapdata` on the very value this bug is about — `false` —
-- raises inside the wrapper itself, merely relocating the crash into mod code.
-- The defect is an unchecked argument, not a wrong environment, so only the
-- argument is checked. The scenario data itself cannot be corrected from Lua: those calls are
-- baked into generated sequence code (`Data\Scenario\*.lua` `'expression'`
-- strings, e.g. UndergroundAnomalies.lua:195), which is compiled when the
-- scenario preset loads and holds no hook for the map argument. Redirecting the
-- call to the sequence's own map from inside `TriggerCaveIn` is not possible
-- either — the function receives only a position, and positions carry no map.
--
-- Deliberately unchanged: the wrapper never invents a map to fall back to (e.g.
-- `CurrentMap`). Dropping rubble on a different map than the sequence meant would
-- be a worse failure than dropping none, and FIX_POLICY §4 does not license
-- guessing.

SMRFixPack.Register("AnomalyCaveInMap", {
	title = "A cave-in on a map that does not exist is declined instead of crashing the sequence",
	apply = function()
		local err = SMRFixPack.Require("AnomalyCaveInMap", {
			{ global = "TriggerCaveIn" },
			{ class = "CaveInRubble",
			  reason = "CaveInRubble class not found (game update changed it?)" },
		})
		if err then return err end
		local orig = TriggerCaveIn

		-- Can this value stand in for a map in TriggerCaveIn's body? The only
		-- thing it does with it before anything else is call MapFindNearest on it
		-- (CaveInRubble.lua:101), so that is what gets asked. Wrapped in pcall
		-- because indexing `false` — the exact value this fix is about — raises.
		local function is_usable_map(map)
			if not map then return false end
			local ok, member = pcall(function() return map.MapFindNearest end)
			return ok and type(member) == "function"
		end

		SMRFixPack.AnomalyCaveInMap = { IsUsableMap = is_usable_map, declined = 0 }

		local wrapped = function(map, pos, ...)
			if not is_usable_map(map) then
				local state = SMRFixPack.AnomalyCaveInMap
				state.declined = state.declined + 1
				state.last = tostring(map)
				return nil
			end
			return orig(map, pos, ...)
		end
		local err = SMRFixPack.SetGlobal("TriggerCaveIn", wrapped,
			"could not install the TriggerCaveIn wrapper")
		if err then return err end

		-- FIX (QA 2026-07-25): the Cave_Of_Wonders site calls
		-- `TriggerCaveIn(UndergroundMap, FindCaveInLocation(UndergroundMap, ...))`
		-- — the INNER call evaluates first and indexes `map.object_hex_grid`
		-- unguarded (CaveInRubble.lua:27), so it raised before the wrapper above
		-- was ever entered. Same decline treatment for it: returning nil hands
		-- TriggerCaveIn a nil pos, which its own shipped guard already handles.
		local orig_find = rawget(_G, "FindCaveInLocation")
		if type(orig_find) == "function" then
			local wrapped_find = function(map, pos, radius, ...)
				if not is_usable_map(map) then
					local state = SMRFixPack.AnomalyCaveInMap
					state.declined = state.declined + 1
					state.last = tostring(map)
					return nil
				end
				return orig_find(map, pos, radius, ...)
			end
			local err_find = SMRFixPack.SetGlobal("FindCaveInLocation", wrapped_find,
				"could not install the FindCaveInLocation wrapper")
			if err_find then return err_find end
		end
	end,
})
