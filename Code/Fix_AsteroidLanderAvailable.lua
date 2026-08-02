-- F72 + F94: the Planetary View's VISIT ASTEROID gate, both of its errors.
--
-- One function, two defects pointing opposite ways. PlanetaryAsteroidVisitPossible
-- (Lua\PlanetaryView.lua:433-444) decides whether to open the rocket picker at
-- all; LandingSiteObject:GetRocketsForExpedition (Lua\UI\PlanetUI.lua:1623-1635)
-- builds the list once it is open. They disagree in BOTH directions.
--
-- ===== F72 — the false NEGATIVE ============================================
-- The gate accepts a UniversalRocketBase only when
--     not rocket.arrival_loc
--     and ((command == "CmdWaitOrder" and departure_loc == OurColony)
--          or (command == "CmdOnEarth"  and departure_loc == Earth))
-- — i.e. it additionally demands one specific command. The list keeps every
-- UniversalRocketBase that is not a supply pod, has departure_loc == OurColony,
-- has no arrival_loc, and can reach the selected spot. It never looks at the
-- command.
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
-- ===== F94 — the false POSITIVE, on the line below =========================
-- `and` binds tighter than `or`, so line :439
--     elseif IsKindOf(rocket, "LanderRocketBase") and rocket.command == "Refuel"
--         or rocket.command == "WaitLaunchOrder"
--         or (rocket.command == "LoadAndLaunch" and not rocket.target_spot) then
-- parses as
--     (IsKindOf(…) and cmd == "Refuel") or (cmd == "WaitLaunchOrder") or (…)
-- — the class test governs only the FIRST of the three clauses. Two thirds of the
-- predicate apply to whatever rocket reached the elseif.
--
-- That is not a corner; it is the default state of a supply rocket.
-- SupplyRocketBase.__parents = { "RocketBase" } (SupplyRocket.lua:1-3) — not
-- UniversalRocketBase, so the first branch does not catch it, and not
-- LanderRocketBase, so the class test is false. RocketBase parks in
-- "WaitLaunchOrder" (RocketBase.lua:643, :699), which the detached clause
-- accepts. One supply rocket sitting on its pad therefore makes the gate return
-- true with no lander anywhere in the colony — and the picker it opens keeps only
-- non-pod UniversalRocketBase rockets, so the rocket that opened the screen
-- cannot appear on it. The player gets an EMPTY picker instead of the clear "no
-- asteroid landers" prompt the code was reaching for. Trade, refugee, foreign-aid
-- and expedition rockets all descend from SupplyRocketBase and do the same.
--
-- Intent tells for F94: a guard that cannot do its job for two of the three
-- commands it was written to qualify, and — inside the same function — the branch
-- three lines ABOVE parenthesises its or-group correctly, as does the sibling
-- EarthVisitPossible immediately below (:446-453). Same author, same file, same
-- idiom, right twice and one pair of brackets dropped once.
--
-- ===== Patch approach, and the property it costs ===========================
-- FIX_POLICY §1.4b global replacement with a body copy: 12 lines from
-- Lua\PlanetaryView.lua:433-444 (shipped Src, game 1.0.7.396349), byte-identical
-- except the added parentheses, with F72's permissive scan appended in place of
-- the final `return false` — so it runs on top of the corrected body, in the same
-- order it ran when it was a post-wrapper.
--
-- ⚠️ CONVERTED FROM A CHAINED POST-WRAPPER 2026-08-02 (F94), AND THE CHAIN IS
-- LOST. This module used to be `if orig(...) then return true end` plus the scan,
-- and its header explained that delegation as a design choice: purely permissive,
-- so any other mod's wrapper survived underneath. That shape CANNOT repair a
-- false positive. A wrapper sees only the boolean `true` and never learns which
-- rocket produced it, so there is nothing to filter on — repairing C24/F94 means
-- OWNING the predicate. §1.4b's "prefer a wrapper over a body copy" is a
-- preference, not an absolute, and this is the case it cannot cover.
-- What that costs, stated rather than glossed: if a future game patch changes
-- this predicate, we now reinstate the 1.0.7 shape instead of inheriting theirs,
-- and another mod that wrapped it is overwritten rather than chained onto. The
-- apply-time self-check catches a renamed or removed target, NOT an edited
-- same-named body — the after-every-patch extraction diff is what covers that
-- (WORKFLOW.md).
--
-- One gap is pre-existing and NOT made worse here: the added scan mirrors
-- GetRocketsForExpedition's own predicate including its supply-pod exclusion, but
-- cannot mirror `table.find(GetAvailableFlightLocations(), selected_spot)` —
-- the gate takes no arguments and has no selected spot.
--
-- §3a: nothing enters the save. The function is synchronous and is called only
-- from an XAction handler — UI, real-time, and UI windows are explicitly safe.
--
-- Everything is read inside the replacement: MarsScreenLandingSpots is a GameVar
-- (PlanetaryView.lua:1) and does not exist while mod code loads.

SMRFixPack.Register("AsteroidLanderAvailable", {
	title = "The asteroid-expedition gate counts landed landers, and stops counting supply rockets",
	apply = function()
		local err = SMRFixPack.Require("AsteroidLanderAvailable", {
			{ global = "PlanetaryAsteroidVisitPossible" },
			{ global = "IsRocketClass" },
			-- The list builder is what we are agreeing with; if it is gone, the
			-- disagreement this fix repairs no longer means anything.
			{ class = "LandingSiteObject", method = "GetRocketsForExpedition" },
		})
		if err then return err end

		local fixed_visit_possible = function()
			for _, rocket in ipairs(MainCity.labels.AllRockets) do
				if IsKindOf(rocket, "UniversalRocketBase") then
					if not rocket.arrival_loc and ((rocket.command == "CmdWaitOrder" and rocket.departure_loc == MarsScreenLandingSpots.OurColony) or (rocket.command == "CmdOnEarth" and rocket.departure_loc == MarsScreenLandingSpots.Earth)) then
						return true
					end
				-- FIX (F94): the whole or-group is now inside the class test, the way
				-- the branch above and EarthVisitPossible below both write it. No
				-- rocket that legitimately qualifies today stops qualifying.
				elseif IsKindOf(rocket, "LanderRocketBase") and (rocket.command == "Refuel" or rocket.command == "WaitLaunchOrder" or (rocket.command == "LoadAndLaunch" and not rocket.target_spot)) then
					return true
				end
			end

			-- FIX (F72): accept what GetRocketsForExpedition would list. This ran as
			-- a post-wrapper until F94; it now sits where vanilla's `return false`
			-- was, which is the same position in the same order.
			-- Its defensive reads are kept as they were tested: the copied body above
			-- already dereferences MainCity and MarsScreenLandingSpots directly, so
			-- they are redundant rather than load-bearing — noted, not removed,
			-- because this is `tested` code and the redundancy costs nothing.
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
