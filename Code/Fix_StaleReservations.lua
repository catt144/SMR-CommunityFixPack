-- F58: Residences hold housing slots for colonists that are never coming, and
-- nothing ever releases them.
--
-- Defect: Residence:GetFreeSpace (Lua\Buildings\Residence.lua:198-200) subtracts
-- `#self.reserved` from the capacity, so a reserved slot is unavailable to anyone
-- else. Reservations are taken during emigration (Colonist:TryToEmigrateToDome,
-- Colonist.lua:1568/1587 -> Dome:ReserveResidence, Dome.lua:2840-2851) and are
-- released only when the colonist actually arrives, dies, or is re-homed
-- (Residence:CancelResidenceReservation, :353-365). There is NO timeout — the only
-- timed lock in this family is the user-forced one (Colonist:CheckForcedResidence,
-- :2329-2342, bounded by g_Consts.ForcedByUserLockTimeout). A colonist waiting for
-- a shuttle that never comes (see F51/F54) therefore holds a slot in the
-- destination dome forever, while being excluded from the Homeless label
-- (:2284) — and the residence UI never shows reservations at all
-- (GetUICapacity / GetUIResidentsCount, :374-380), so the player sees a half-empty
-- dome that refuses to house anyone. The developers already ship one fixup for
-- this list drifting out of sync (SavegameFixups.RemoveReservedInSameResidence,
-- :591-599), which is evidence it drifts in production.
--
-- Patch approach:
--  * chained post-hook on Residence:ReserveResidence that timestamps the
--    reservation on the colonist (SMRFixPack_reserved_at — a plain number, safe to
--    leave behind if the mod is removed, per FIX_POLICY §3);
--  * an additive OnMsg.NewDay sweep that cancels reservations which are dead
--    (invalid/dying colonist), desynced (the colonist no longer points back at this
--    residence) or older than g_Consts.ForcedByUserLockTimeout — the game's own
--    "this lock has gone stale" duration, reused rather than invented.
--    Reservations already in a savegame carry no timestamp; they are stamped on the
--    first sweep so they get a full grace period instead of being cancelled
--    outright.
--
-- Deliberately NOT done: showing the reservation count in the residence infopanel.
-- That is a UI addition rather than a defect repair (FIX_POLICY §4).

SMRFixPack.Register("StaleReservations", {
	title = "Housing reserved for colonists that never arrive is released again",
	apply = function()
		local R = rawget(_G, "Residence")
		if type(R) ~= "table" or type(R.ReserveResidence) ~= "function"
				or type(R.CancelResidenceReservation) ~= "function" then
			return "Residence reservation methods not found (game update changed them?)"
		end

		local orig = R.ReserveResidence
		function R:ReserveResidence(unit, ...)
			local reserved = orig(self, unit, ...)
			-- FIX (F58): remember when the slot was taken so it can go stale.
			if reserved and unit then
				unit.SMRFixPack_reserved_at = GameTime()
			end
			return reserved
		end
	end,
})

-- Daily sweep. Additive handler: the shipped OnMsg.NewDay in Residence.lua:567
-- keeps running untouched.
function OnMsg.NewDay()
	local fix = SMRFixPack.fixes.StaleReservations
	if not (fix and fix.status == "active") then return end
	if not (rawget(_G, "MainCity") and MainCity.labels) then return end
	local timeout = g_Consts and g_Consts.ForcedByUserLockTimeout
	if not timeout then return end

	local now = GameTime()
	local released = 0
	for _, residence in ipairs(MainCity.labels.Residence or empty_table) do
		local reserved = residence.reserved
		for i = #(reserved or empty_table), 1, -1 do
			local colonist = reserved[i]
			local stale
			if not IsValid(colonist) then
				stale = true
			elseif colonist.reserved_residence ~= residence then
				stale = true -- the two sides disagree; the slot is orphaned
			elseif colonist:IsDying() then
				stale = true
			else
				local since = colonist.SMRFixPack_reserved_at
				if not since then
					-- pre-existing reservation from an older save: start its clock now
					colonist.SMRFixPack_reserved_at = now
				elseif now - since >= timeout then
					stale = true
				end
			end
			if stale then
				residence:CancelResidenceReservation(colonist)
				released = released + 1
			end
		end
	end

	if released > 0 then
		local msg = string.format("[CommunityFixPack] StaleReservations: released %d stale housing reservation(s)", released)
		-- ModLog's output path formats the message a second time (00_Core.lua:24-30).
		if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
	end
end
