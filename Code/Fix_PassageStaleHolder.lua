-- C42: a dome-side passage traversal clears unit.holder directly after LeadIn,
-- leaving the last passage element's units list with a stale member. When that
-- element is destroyed, Holder:KickUnitsFromHolder otherwise asserts and kicks
-- that unrelated colonist from their current activity and position.
--
-- The raw clear lives inside a destructor closure in the blocking
-- PassageBase:TraverseTunnel. Replacing that body would capture mod code across
-- yields and overlap the C116/C117 traversal repairs. This narrower mitigation
-- prunes invalid or mismatched members synchronously just before vanilla's kick
-- loop. The raw clear still happens, so stale entries may remain until element
-- destruction; this module prevents their harmful teardown effect.
--
-- Save safety (§3a): layer 3. This wrapper is synchronous, stores no function
-- in persisted state and installs no thread or field. No mod frame is below a
-- traversal yield. The declaring Holder method is wrapped, with a first-action
-- class gate; every non-passage holder goes straight to the captured original.
-- Branch shape: TraverseTunnel is blocking and unsafe to probe on a stub. The
-- Require checks below name the passage-element and traversal shape; the SRC
-- pins make the raw-clear and kick-loop expressions update discriminators.
--
-- MANIFEST (FIX_POLICY §2b), archived game build 1.1.1.405907.
-- SRC: Lua/Passage.lua PassageBase:TraverseTunnel sha256=33f432f96c8e5b29944b9b2fbf92766de644873f7ea01cb968b080cbebd114c3
-- DEFECT: unit\.holder\s*=\s*nil
-- SRC: Lua/Buildings/Holder.lua Holder:KickUnitsFromHolder sha256=495e387734aff6d4f5d3a3417a978b505d77584b21981071fbbb2d60f8bb7c73
-- DEFECT: unit:KickFromBuilding\(self\)

SMRFixPack.Register("PassageStaleHolder", {
	title = "Stale passage occupants are not kicked during demolition",
	apply = function()
		local err = SMRFixPack.Require("PassageStaleHolder", {
			{ class = "Holder", method = "KickUnitsFromHolder" },
			{ class = "PassageGridElement", method = "Done" },
			{ class = "PassageBase", method = "TraverseTunnel" },
			{ global = "IsKindOf" },
			{ global = "IsValid" },
		})
		if err then return err end

		local orig = Holder.KickUnitsFromHolder
		function Holder:KickUnitsFromHolder(...)
			if not IsKindOf(self, "PassageGridElement") then
				return orig(self, ...)
			end
			local units = self.units
			if type(units) == "table" then
				for i = #units, 1, -1 do
					local unit = units[i]
					if not IsValid(unit) or unit.holder ~= self then
						table.remove(units, i)
					end
				end
			end
			return orig(self, ...)
		end
	end,
})
