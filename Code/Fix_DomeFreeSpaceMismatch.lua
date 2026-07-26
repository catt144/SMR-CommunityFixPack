-- F60: a dome's "free living space" total and the code that actually assigns
-- homes disagree about which residences count.
--
-- Defect: GatherFreeLivingSpaces (Lua\_GameUtils.lua:475-495) picks the member it
-- tests from its second argument:
--     local working_member = player_enabled and "ui_working" or "working"
-- `working` is the building's real operating state (power, air, workers,
-- malfunction); `ui_working` is the player's on/off switch. Dome:
-- RefreshFreeLivingSpaces (Lua\Buildings\Dome.lua:2832-2834) calls it with no
-- second argument, so the dome totals count only residences that are running
-- right now.
--
-- Everything that hands out a home uses `ui_working` instead: ChooseResidence
-- (Residence.lua:404-412) scores `home.ui_working and home:GetFreeSpace()`, and
-- Colonist:UpdateResidence (Colonist.lua:2309-2316) rejects a reserved home for
-- `not home.ui_working`. The two immediately preceding functions in _GameUtils
-- itself — GetFreeWorkplacesAround (:443-455) and GetFreeWorkplaces (:457-473) —
-- both count on `b.ui_working` as well, which is the same author writing the same
-- kind of tally correctly (FIX_POLICY §4).
--
-- Consequence: while a residence is unpowered, out of air or short of workers,
-- the dome reports less free living space than it really has. That total is what
-- the birth and immigration gates read (Community:GetFreeLivingSpace /
-- HasFreeLivingSpace, Community.lua:322-345; Dome.lua:2240, :3295, :3325-3328,
-- :3684), so a power dip makes a dome look full — while ChooseResidence carries
-- on assigning colonists into those very residences.
--
-- Patch approach: full replacement of Dome:RefreshFreeLivingSpaces — a copy of
-- Lua\Buildings\Dome.lua:2832-2834 (shipped Src, game 1.0.7.396349) passing the argument
-- the shipped function already provides for, marked -- FIX. There is nothing to
-- wrap: the method is two lines and the fix IS the argument.
--
-- Deliberately not touched: MicroGHabitatBase:RefreshFreeLivingSpaces
-- (MicroGHabitat.lua:42-44) has the identical omission, but an asteroid
-- habitat's `working` state is its life support, which is F73's subject matter
-- and not this tracked defect.

SMRFixPack.Register("DomeFreeSpaceMismatch", {
	title = "A dome's free-housing total counts the same residences the game assigns colonists to",
	apply = function()
		local D = rawget(_G, "Dome")
		if type(D) ~= "table" or type(D.RefreshFreeLivingSpaces) ~= "function" then
			return "Dome.RefreshFreeLivingSpaces not found (game update changed it?)"
		end
		if type(rawget(_G, "GatherFreeLivingSpaces")) ~= "function" then
			return "GatherFreeLivingSpaces not found (game update changed it?)"
		end

		function D:RefreshFreeLivingSpaces()
			-- FIX (F60): second argument added. Without it the tally is taken on
			-- `working` while every assignment path reads `ui_working`.
			self.free_spaces = GatherFreeLivingSpaces(self.labels.Residence, "player_enabled")
		end
	end,
})
