-- F90: surface dust storms break UNDERGROUND cables and pipes.
--
-- Defect, the whole chain: City:HourlyUpdate (Lua\City.lua:148-149) runs
--     if HasDustStorm(self:GetMap()) and hour % const.BreakIntervalHours == 0
--         then self:RandomBreakSupplyGrid() end
-- -> City:RandomBreakSupplyGrid (:178-181) -> SupplyGrid:RandomBreakElements
-- (SupplyGrid.lua:1017-1021) -> SupplyGridFragment:RandomBreakConnection
-- (:669-683), which on a hit does
--     local element = table.rand(self.connectors, self:Random())   -- :677
--     ... bld:Break()                                              -- :680
-- with NO map filter, no city filter, nothing.
--
-- Underground connectors are in that array on purpose, not by accident — the
-- class is named for it. SupplyGridFragment inherits MultiMapSupplyGrid
-- (SupplyGrid.lua:337-338), which exists precisely to let one fragment span
-- several maps. The join is the elevator: MapPassageLinked:MergePassageGrids
-- (Elevator.lua:402-408) -> MergeGrids (SupplyGrid.lua:1635-1650) ->
-- SupplyGridFragment:AddElement, which pushes every cable/pipe straight into the
-- merged fragment's connector array (:547-548). And AddCityElement (:463-477)
-- registers that one fragment into BOTH cities' lists, so the surface city's
-- hourly break pass is handed a fragment holding both maps' connectors.
--
-- Result: with an elevator built, a dust storm on the surface can break a cable
-- or pipe underground, where no dust storm exists or can exist.
--
-- Intent tells, two:
--   (a) HasDustStorm is hard-gated to MainMap — `return (MainMap == map) and
--       g_DustStorm` (DustStorm.lua:39-42). The disaster is DESIGNED surface-only
--       and the break pass is its damage arm; the damage escaping the map the
--       gate just enforced is not a design choice.
--   (b) Sixteen lines above the break pass, the same file's production pass
--       handles the multi-map case correctly AND SAYS SO: ProductionThreadProc
--       guards with `if self.city == grid_fragment.cities[1] then` under the
--       comment "this grid only updates fragments that were first added to this
--       city / this prevents multiple production calls when multiple cities share
--       the same grid fragment" (:992-1006). RandomBreakElements (:1017-1021)
--       carries no such guard. The code knows fragments span cities; the break
--       path was written as if they did not.
--
-- External corroboration, reached independently: GromGor's "No Underground supply
-- grid breaks" (workshop 3730839706) replaces this same function's whole body to
-- filter the victim list on MainMap. Same function, same line, same diagnosis.
--
-- Reachability R1: ordinary mid-game — underground unlocked, one elevator built
-- (which merges the grids automatically), a surface dust storm, >10 connectors on
-- the merged fragment (IsBreakable, :693-697), and the roll.
--
-- ⭐ A consequence of the call-chain enumeration that removes the hardest part of
-- the design problem: RandomBreakConnection is DUST-STORM-ONLY BY CONSTRUCTION.
-- Every link back to City:HourlyUpdate is single-caller and the whole chain sits
-- behind HasDustStorm, so a fix placed here needs NO key, no CurrentThread() test
-- and no state to know it is the storm pass — the very thing FIX_POLICY §3a warns
-- is usually the hard part of a layer-3 wrapper.
--
-- ⛔ THE CHEAPER-LOOKING ALTERNATIVE IS UNSOUND, and was checked rather than
-- assumed. Vetoing an off-MainMap BreakableSupplyGridElement:Break during a dust
-- storm would suppress LEGITIMATE underground damage: :Break() has eight shipped
-- call sites, including CaveInRubble.lua:158. Cave-ins are an underground
-- phenomenon and they break underground elements on purpose. Dust storms are
-- frequent, so "off-MainMap break while a dust storm is running" occurs
-- legitimately, and the veto would silently eat marsquake/cave-in damage.
--
-- Patch approach: FIX_POLICY §1.4 chained wrapper, §3a LAYER 3 — narrow the
-- INPUT, keep vanilla's body. We hand the shipped function a surface-only
-- connector list and restore the real one. The roll, the seed, the probability
-- and the Break call all stay vanilla's; no mod body sits in the save.
--
-- ⚠️ self.connectors is a PERSISTED field on a saved grid fragment, so an error
-- escaping orig must never strand our filtered array there. Hence pcall + restore
-- + re-raise, with the restore on BOTH paths.
--
-- ===== The four properties that make this safe, each verified in Src ==========
--
-- 1. NO YIELD INSIDE THE CALL, so no §3a route-(a) exposure — and this was traced
--    end to end this session rather than inherited. BreakableSupplyGridElement:Break
--    (SupplyGridBreakable.lua:70-106) is straight-line: no Sleep, no WaitMsg. Its
--    grid calls are RemoveElement (SupplyGrid.lua:494-524) and AddElement
--    (:526-554), both invoked with `update` nil, so RemoveElement's UpdateGrid
--    takes the `update ~= "immediate"` branch and merely Wakeup()s the update
--    thread (:558-562), and AddElement's DelayedGridUpdate only registers a
--    deferred game-time thread (:389-395). Neither runs a walk while we are
--    swapped, and Lua threads here are cooperative — with no yield in the call our
--    frame cannot be suspended, so no save can be written mid-swap either.
-- 2. THE ONLY MUTATIONS TO connectors DURING THE SWAP ARE SYMMETRIC. Break()
--    removes the picked element from grid.connectors (:518-519) and adds it back
--    (:547-548) — both land on our filtered array and cancel out. Nothing else in
--    the chain touches connectors: OnAddedToGrid/OnRemovedFromGrid are empty_func
--    (:79-81), UpdateGrid walks elements/consumers/storages and never connectors
--    (:556-620), and the air element Break() creates for a water break is a
--    detached SupplyGridElement (NewSupplyGridConsumer, :56-62) that joins the AIR
--    grid, a different fragment object.
--    ⚠️ The one difference, stated because it is real and not zero: in vanilla the
--    broken connector ends up moved to the END of the real connectors array, and
--    with this wrapper the real array's ORDER is unchanged. Nothing reads that
--    order — table.rand picks uniformly and `#` is unaffected — but it is a
--    difference, not an identity.
-- 3. ⭐ GromGor's empty-list crash is STRUCTURALLY IMPOSSIBLE in this shape. His
--    version indexes element.building on a table.rand of a possibly-empty
--    surface_connectors. Ours cannot reach that: the filtered list is also what
--    IsBreakable counts, and `#connectors <= 10` returns false long before the
--    pick (:695). The requirement to "guard rather than inherit his shape" is
--    satisfied by construction rather than by an added check.
-- 4. FRAGMENTS THAT DO NOT SPAN MAPS ARE UNTOUCHED — the `#surface == #all` early
--    return means the overwhelming majority of calls pass straight through to orig
--    with nothing swapped.
--
-- ===== The scope question, answered half-way ON PURPOSE ======================
-- Filtering connectors also makes IsBreakable's `#self.connectors <= 10` test
-- surface-only, which is self-consistent (the "nothing to break" gate should count
-- the pool we break from) and is accepted. The break PROBABILITY at :673 is
-- `^ #self.elements`, a different array, and it stays cross-map.
-- ⚠️ RESIDUAL, STATED PLAINLY: after this fix an elevator player's merged fragment
-- still rolls at the inflated cross-map probability while only surface connectors
-- can be picked, so their surface cables break somewhat more often than a
-- non-elevator player's. That is the narrower true thing. Whether the probability
-- should also be surface-only is an intent question, still undecided, and it is
-- not needed to stop underground pipes bursting in a surface dust storm.
--
-- Map accessor: GromGor used `con.building.city:GetMap() == MainMap`. We use
-- `element.building:GetMap()` instead — one hop shorter, and it avoids `.city`,
-- which this very file treats as possibly nil (AddCityElement falls back to
-- `building:GetMap().City` at :467-470 for exactly that reason). `building:GetMap()`
-- is the accessor SupplyGrid.lua itself uses (:293, :310, :468, :484, :1369).
--
-- Install timing: the wrapper goes on SupplyGridFragment, the class that DECLARES
-- RandomBreakConnection (the only declaration in the tree). apply() runs at
-- mod-code load — before class flattening on BOTH the cold-boot and the
-- mid-session-enable paths — so it propagates to the three live subclasses
-- (ElectricityGrid, WaterGrid, AirGridFragment), none of which override it.

local FIX_ID = "DustStormUndergroundBreaks"

SMRFixPack.Register(FIX_ID, {
	title = "A surface dust storm can no longer break cables and pipes underground",
	apply = function()
		-- Checked on the DECLARING class (the F64 lesson): SupplyGridFragment is
		-- where RandomBreakConnection is written, and it is the only declaration.
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "SupplyGridFragment", method = "RandomBreakConnection" },
			{ class = "SupplyGridFragment", method = "IsBreakable" },
			-- the gate that makes this pass dust-storm-only by construction; if it
			-- is gone, the reasoning this fix rests on no longer holds
			{ global = "HasDustStorm" },
		})
		if err then return err end

		local F = SupplyGridFragment
		local orig = F.RandomBreakConnection

		function F:RandomBreakConnection(...)
			local all = self.connectors
			local main = rawget(_G, "MainMap")
			-- Nothing resolvable to filter against: behave exactly like vanilla.
			if type(all) ~= "table" or not main then return orig(self, ...) end

			local surface, n = {}, 0
			for i = 1, #all do
				local element = all[i]
				local bld = element and element.building
				-- Keep a connector only when it is PROVABLY on the main map. One
				-- whose building is gone cannot be meaningfully broken anyway —
				-- vanilla's own IsKindOf test would reject it at :679.
				if bld and IsValid(bld) and bld:GetMap() == main then
					n = n + 1
					surface[n] = element
				end
			end

			-- Not a merged fragment (the overwhelming majority): straight through,
			-- nothing swapped, nothing to restore.
			if n == #all then return orig(self, ...) end

			self.connectors = surface
			local ok, r1, r2 = pcall(orig, self, ...)
			self.connectors = all      -- ALWAYS restored, on both paths: this field
			                           -- is persisted and must never be left ours
			if not ok then
				-- FIX_POLICY §6 / ENGINE_FACTS: error() in mod code REPORTS AND
				-- CONTINUES — it does not unwind. So this re-raise keeps vanilla's
				-- failure VISIBLE (the line is still reported, attributed to the
				-- original body) but it does not reproduce vanilla's stack unwind.
				-- Stated rather than glossed: our caller continues where an
				-- unwrapped raise might not have. The alternative — no pcall — would
				-- strand our filtered array in a saved field, which is worse.
				error(r1, 0)
				return
			end
			return r1, r2
		end
	end,
})
