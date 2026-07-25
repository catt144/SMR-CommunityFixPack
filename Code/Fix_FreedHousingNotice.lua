-- F59: A home falling vacant never tells the dome's homeless colonists about it.
--
-- Defect: Residence:CheckHomeForHomeless (Lua\Buildings\Residence.lua:124-133)
-- walks the dome's Homeless label and re-runs UpdateResidence on each colonist —
-- it is the mechanism that turns "a slot opened up" into "somebody moves in".
-- The shipped code calls it from Residence:GameInit (:30), Residence:SetUIWorking
-- when switched back on (:137) and Residence:SetDome (:180), plus Hotel.lua:23.
-- Every one of those is housing becoming available because the PLAYER did
-- something.
--
-- Nothing calls it when a slot frees up on its own: Residence:RemoveResident
-- (:83-89) only updates the occupation counter and resets the dome's free-space
-- cache. So after a resident dies, retires into a different home, is kicked out
-- or emigrates, the empty bed is invisible to the homeless standing in the same
-- dome until their own heavy update comes round — and that is throttled to one
-- pass every 12 game hours once the colony passes 3600 colonists
-- (City:GetHeavyUpdateFrequency-style gating, City.lua:118-120).
--
-- Patch approach: a chained post-hook (FIX_POLICY §1.4) on Colonist:SetResidence
-- (Colonist.lua:2291-2307) rather than on Residence:RemoveResident as the tracker
-- sketched. Same event — SetResidence is the only caller of RemoveResident — but
-- hooking one level up means the notification runs when the move is FINISHED.
-- RemoveResident is called in the middle of SetResidence, before
-- `home:AddResident(self)` and before `self.residence` is updated; waking the
-- homeless there lets one of them take the slot the colonist in hand is about to
-- move into, and the very next shipped line is `assert(self:GetFreeSpace() > 0)`
-- followed by an unconditional insert — i.e. an over-capacity residence.
--
-- The hook is deliberately cheap: it does nothing unless a home was actually left
-- and there is now a usable slot in it.
--
-- Not hooked: Residence:CancelResidenceReservation (:353-365), the other site
-- that frees a slot without telling anyone. Residence:AddResident calls it
-- (via the colonist, :74) as its second statement, one line before that same
-- `assert(self:GetFreeSpace() > 0)`, so notifying from there reintroduces exactly
-- the race described above. The reservation case is already bounded instead by
-- F58's daily stale-reservation sweep plus the normal heavy update.

SMRFixPack.Register("FreedHousingNotice", {
	title = "A home falling vacant is offered to the dome's homeless straight away",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.SetResidence) ~= "function" then
			return "Colonist.SetResidence not found (game update changed it?)"
		end
		-- NB: mod code loads before the classes are flattened — these are declared
		-- on Residence itself, which is the class to check.
		local R = rawget(_G, "Residence")
		if type(R) ~= "table" or type(R.CheckHomeForHomeless) ~= "function"
				or type(R.GetFreeSpace) ~= "function" then
			return "Residence.CheckHomeForHomeless/GetFreeSpace not found (game update changed them?)"
		end

		local orig = C.SetResidence
		function C:SetResidence(home, ...)
			local left = self.residence
			local r1, r2 = orig(self, home, ...)
			-- FIX (F59): the home we just moved out of now has a bed free. Offer it
			-- to the dome's homeless now instead of leaving it to their next heavy
			-- update, which is a 12-hour wait in a large colony.
			if left and left ~= self.residence and IsValid(left)
				and left.ui_working and type(left.CheckHomeForHomeless) == "function"
				and left:GetFreeSpace() > 0 then
				left:CheckHomeForHomeless()
			end
			return r1, r2
		end
	end,
})
