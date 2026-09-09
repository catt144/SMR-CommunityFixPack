-- F58: Residences hold housing slots for colonists that are never coming, and
-- nothing ever releases them.
--
-- SRC: Lua/Buildings/Residence.lua Residence:GetFreeSpace sha256=d7b7f54cb357379f029f5004b7b77e6141c5da184c43401c5c09db92e28ea67f
-- DEFECT: #self\.reserved
-- SRC: Lua/Buildings/Residence.lua Residence:ReserveResidence sha256=88018693261f64a17dbb085803ae0436558443ea2e20f0ea0559db5ce5b8e388
--
-- ⚠️ NAMED-ABSENCE LIMIT, per FIX_POLICY §2b. This module's defect is a MISSING
-- timeout, and a regex matches what is present, not what is absent. The DEFECT:
-- above therefore states the expression that is wrong BECAUSE the timeout is
-- missing — a reservation costs a real housing slot — and the wrap target below
-- it carries no DEFECT: at all. ⇒ if the developers ever add an expiry
-- elsewhere, `DEFECT-GONE` will NOT fire and this module will not be flagged.
-- It is watched for class (b), a changed body, and for nothing else.
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
--
-- ======================================================================
-- 1.1.0 (2026-09-08, hotfix2 link 03; re-verification F-2, VANILLA_FIX_QA §0.4)
-- Owner ruling: KEEP AND FIX (checklist 124, 2026-09-08 — "fix is the ruling").
-- ======================================================================
--
-- ⛔ WHAT THIS MODULE WAS DOING WRONG. 1.1.0 added a LEGITIMATE long-lived
-- reservation that our sweep could not tell from a stale one. A colonist
-- boarding an expedition rocket saves their home
-- (Colonist:EnterTransporter -> self.expedition_residence = self.residence,
-- Lua/Units/Colonist.lua:5027-5031) and Colonist:OnDisappear re-takes it through
-- Residence:ReserveResidence (:5003-5005) — which is OUR wrap target, so the
-- post-hook below stamps it like any other reservation. The colonist stays a
-- VALID object while away (Unit.OnDisappear detaches, it does not delete), and
-- ReturnFromExpedition keeps the slot only if it is still reserved (:5081-5087).
-- The lock our sweep reuses is g_Consts.ForcedByUserLockTimeout = 3,600,000 ms
-- (Lua/__const.lua:171-176) while one-way expedition time is 1,440,000–3,000,000
-- (Data/POI.lua) plus pad wait plus the return leg ⇒ the age branch routinely
-- fired on a real hold. Worse, 1.1.0's CancelResidenceReservation now ALSO wipes
-- expedition_residence (Lua/Buildings/Residence.lua:385-399, the comment there
-- says so), so cancelling did not merely release the slot — it destroyed the
-- record that the colonist was owed one. ⇒ crew back from a long expedition were
-- re-homed at random or left homeless. THE FIX IS ONE CLAUSE, in the sweep.
--
-- ⚠️ THE PREMISE THIS MODULE RESTS ON HAS NARROWED, AND THE HEADER ABOVE NOW
-- OVERSTATES IT. On 1.1.0 the ORDINARY shuttle-wait case F58 was written for is
-- bounded by the game itself: const.ColonistTransportTaskExpirationTime =
-- DayDuration (Lua/_GameConst.lua:144), ColonistTransportTask:IsObsolete fires on
-- it (Lua/LRTransport.lua:43-49), LRManager:ExpireColonistTransportTasks runs on a
-- repeat and calls ClearTransportRequest, whose first act releases the
-- reservation (Lua/LRManager.lua:50-62), and there is a one-sol pickup-wait cap
-- besides (const.ColonistMaxWaitShuttlePickupTimeMs, _GameConst.lua:143).
-- ⇒ WHAT THIS SWEEP STILL BUYS IS NARROWER THAN "F58 IS STILL SHIPPED":
--   * committed-shuttle limbo — IsObsolete returns false the moment a shuttle
--     commits (LRTransport.lua:44-46), and ExpireColonistTransportTasks also
--     skips a colonist whose command is "Transport" (LRManager.lua:55), so a ride
--     that never completes is expired by nothing;
--   * the walk path — TransportByFootDtor (Colonist.lua:3529-3539) clears
--     emigration_dome and the outside flags and does NOT cancel the reservation.
-- Said plainly so nobody re-derives a wider claim from this file: on 1.1.0 the
-- module is a belt for two residual paths, not the whole defect.
--
-- ⚠️ RESIDUAL WE ACCEPT, named rather than hidden. A colonist lost permanently on
-- an expedition while still a valid object would now hold their home forever,
-- because we no longer age out that hold. That is vanilla's own hold and vanilla
-- owns its lifetime; cancelling it is the harm this edit repairs. If it ever
-- shows up in play it is a NEW entry, not a reason to put the age branch back.

SMRFixPack.Register("StaleReservations", {
	title = "Housing reserved for colonists that never arrive is released again",
	apply = function()
		local err = SMRFixPack.Require("StaleReservations", {
			{ class = "Residence", method = "ReserveResidence",
			  reason = "Residence reservation methods not found (game update changed them?)" },
			{ class = "Residence", method = "CancelResidenceReservation",
			  reason = "Residence reservation methods not found (game update changed them?)" },
		})
		if err then return err end
		local R = Residence

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
OnMsg.NewDay = SMRFixPack.WhenActive("StaleReservations", function()
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
			elseif colonist.expedition_residence then
				-- FIX (1.1.0, F-2): a colonist away on an expedition holds their
				-- home DELIBERATELY (Colonist.lua:5003-5005 re-takes it through the
				-- very method we wrap), the residence panel promises they will
				-- return to it, and a round trip routinely outlasts the lock this
				-- sweep reuses. Never let the age branch below cancel that — and
				-- cancelling would not just free the slot, it would wipe
				-- expedition_residence itself (Residence.lua:394-396). The three
				-- branches ABOVE are deliberately left to fire: an invalid,
				-- desynced or dying colonist is not coming back, and releasing the
				-- slot is right for them whether they were on an expedition or not.
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
		SMRFixPack.Log("StaleReservations: released %d stale housing reservation(s)", released)
	end
end)
