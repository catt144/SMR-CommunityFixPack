-- F72: "No available Asteroid Landers" while a lander is sitting on the pad.
--
-- Defect: the Planetary View's VISIT ASTEROID action asks one function whether
-- to open the rocket picker at all, and a DIFFERENT, stricter function builds
-- the list once it is open. They disagree.
--
-- The gate, PlanetaryAsteroidVisitPossible (Lua\PlanetaryView.lua:433-444),
-- accepts a UniversalRocketBase only when
--     not rocket.arrival_loc
--     and ((command == "CmdWaitOrder" and departure_loc == OurColony)
--          or (command == "CmdOnEarth"  and departure_loc == Earth))
-- — i.e. it additionally demands one specific command.
--
-- The list, LandingSiteObject:GetRocketsForExpedition (Lua\UI\PlanetUI.lua:
-- 1623-1635), keeps every UniversalRocketBase that is not a supply pod, has
-- departure_loc == OurColony, has no arrival_loc, and can reach the selected
-- spot. It never looks at the command.
--
-- So a lander parked at the colony with no destination assigned, but running any
-- command other than CmdWaitOrder, is offered by the list and refused by the
-- gate: the player gets the "No available Asteroid Landers" popup
-- (PromptNoAvailableAsteroidLanders, :455-463) while the lander sits on the pad.
-- The everyday case is CmdUnload (UniversalRocket.lua:478-510), which runs for
-- as long as the drones need to empty the hold — and indefinitely when there are
-- no drones or nowhere to put the cargo. CmdWaitMaintenance (:586-630) is the
-- other one: a rocket waiting for maintenance parts is equally listed and
-- equally refused.
--
-- Patch approach: a chained post-wrapper (FIX_POLICY §1.4) rather than a
-- replacement. The repair is purely permissive — every rocket the shipped
-- predicate accepts is still accepted, we only add the ones the list would show
-- — so calling the original first and doing our own scan only when it says "no"
-- leaves the shipped logic, and any other mod's wrapper, completely intact.
--
-- The added scan mirrors GetRocketsForExpedition's own predicate, including its
-- supply-pod exclusion, so the gate can never newly open an empty picker. The
-- one condition it cannot mirror is `table.find(GetAvailableFlightLocations(),
-- selected_spot)`: the gate takes no arguments and has no selected spot. That
-- gap is pre-existing and is not made worse here.
--
-- Everything is read inside the wrapper: MarsScreenLandingSpots is a GameVar
-- (PlanetaryView.lua:1) and does not exist while mod code loads.

SMRFixPack.Register("AsteroidLanderAvailable", {
	title = "A landed lander with no destination counts as available for an asteroid expedition",
	apply = function()
		local orig = rawget(_G, "PlanetaryAsteroidVisitPossible")
		if type(orig) ~= "function" then
			return "PlanetaryAsteroidVisitPossible not found (game update changed it?)"
		end
		if type(rawget(_G, "IsRocketClass")) ~= "function" then
			return "IsRocketClass not found (game update changed it?)"
		end
		-- The list builder is what we are agreeing with; if it is gone, the
		-- disagreement this fix repairs no longer means anything.
		local LSO = rawget(_G, "LandingSiteObject")
		if type(LSO) ~= "table" or type(LSO.GetRocketsForExpedition) ~= "function" then
			return "LandingSiteObject.GetRocketsForExpedition not found (game update changed it?)"
		end

		local fixed_visit_possible = function(...)
			if orig(...) then return true end

			-- FIX (F72): accept what GetRocketsForExpedition would list.
			local city = rawget(_G, "MainCity")
			local rockets = city and city.labels and city.labels.AllRockets
			local spots = rawget(_G, "MarsScreenLandingSpots")
			local our_colony = spots and spots.OurColony
			if not rockets or not our_colony then return false end

			for _, rocket in ipairs(rockets) do
				if IsKindOf(rocket, "UniversalRocketBase")
					and not IsRocketClass(rocket, "UniversalSupplyPodBase")
					and not rocket.arrival_loc
					and rocket.departure_loc == our_colony then
					return true
				end
			end
			return false
		end

		-- Phase 4 (C4): this install previously had no read-back verification.
		return SMRFixPack.SetGlobal("PlanetaryAsteroidVisitPossible", fixed_visit_possible)
	end,
})
