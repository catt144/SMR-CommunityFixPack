-- F110 (was C25): a Jumbo Cave Reinforcement construction site permanently
-- soft-locks when one of the Waste Rocks underneath it is unreachable.
--
-- Defect (Src-verified, then reproduced LIVE from a field save 2026-08-30). The
-- Jumbo Cave mystery spawns JumboCaveReinforcementStructure construction and
-- blocks on it:
--     while not (UndergroundMap.City.labels["JumboCaveReinforcementStructure"]) do
--         Sleep(3000 + …)
--     end
-- (Scenario\BuriedWonder_Jumbo_Cave.generated.lua:103; the post-1.0.6 rework's
-- …_106.generated.lua:104 is byte-identical). The site cannot start until its
-- Waste Rock is cleared. Clearing is drone work: Drone:ApproachWrapper ->
-- WasteRockObstructor:DroneApproach picks a RANDOM point on the ring around the
-- rock (GetDroneApproachPos, InteractionRand, WasteRock.lua:308-327) and paths to
-- it; if the rock is walled by cave geometry, every angle fails, the drone files
-- the rock in unreachable_buildings "forever" (Drone.lua:822-840), and the rock
-- is never worked -> never TransformToStockpile'd -> the site's
-- waste_rocks_underneath never empties -> the reinforcement never builds -> the
-- mystery's Sleep loop spins forever. Player symptom: "construction site is being
-- cleared" that never finishes; the Jumbo Cave mystery soft-locks with no recourse.
--
-- Field confirmation (F110 entry): a stuck site down to its last rock
-- (waste_rocks_underneath = 1), that rock a WasteRockObstructor (Rocks_04) in two
-- drones' unreachable_buildings, JCRS completed = 0. Permanence witnessed: the
-- unreachable flag resets on load, then rebuilds after ~1-2 min of run, and the
-- site stays stuck. VALIDATED end to end on that save: force-running the game's
-- own clear on the stuck rock emptied waste_rocks_underneath, the site built, and
-- the mystery paid out ("Jumbo Cave: Reinforcements Completed").
--
-- Reachability R1: any player whose Jumbo Cave reinforcement lands on strand-prone
-- geometry hits it, with no recourse — a mystery step that never completes.
--
-- Fix shape (owner ruling 2026-08-30: PROACTIVE, plus a reactive self-heal for
-- saves already affected). No wrapper, no owned thread. A single healing pass,
-- driven by two additive OnMsg handlers (FIX_POLICY §1.2):
--   * OnMsg.NewHour  — proactive: catches a wedge as soon as it forms in play.
--   * OnMsg.LoadGame — reactive: unwedges saves that are already stuck.
-- The pass finds JumboCaveReinforcementStructure construction sites, and for each
-- Waste Rock underneath that the colony's drones have PROVEN they cannot reach
-- (the rock is in a drone's unreachable_buildings table — the game's own
-- "can't get there" signal, so healthy rocks a drone is clearing are never
-- touched), it DoneObject's the rock. That fires WasteRockObstructor:OnDeleted ->
-- parent_construction:OnWasteRockObstructorCleared(rock, false) SYNCHRONOUSLY
-- (WasteRock.lua:126-133) with no leftover stockpile, dropping the rock from
-- waste_rocks_underneath; the site's own TestBlockerClearenceProgress (called once
-- after clearing, and also self-fired by the vanilla DelayedBlockerClearenceTest)
-- then transitions it to construction. This is exactly the end state the live A/B
-- reached; the game builds the reinforcement from there.
--
-- Scope (FIX_POLICY §4a who-benefits). Deliberately narrowed to
-- building_class == "JumboCaveReinforcementStructure" — a mystery-scripted step
-- the player cannot manage and that has no other resolution. Ordinary
-- construction is left entirely alone: an unreachable Waste Rock there may be the
-- player's to resolve (move a building, clear an approach), and force-clearing it
-- would be a behaviour change, not a bug fix (the REACHABILITY_AUDIT F49(c)
-- lesson — do not "fix" behaviour that isn't defective).
--
-- Known limitation, stated: detection keys on the drone's unreachable flag, which
-- is only written after a free drone actually attempts the rock. In a colony so
-- drone-starved that the rock is never attempted, the flag never forms and this
-- pass will not fire. That did not occur in the field case (34 drones, the flag
-- present); if a report ever shows it, the fallback is a time-since-placed signal.
--
-- §3a save-safety, stated: the module owns no thread and stores no function in
-- any object; it holds no GameVar and adds no object field. Its only actions are
-- vanilla's own DoneObject and TestBlockerClearenceProgress, called from OnMsg
-- handlers that run and return. SAVE FOOTPRINT: none.

local FIX_ID = "JumboCaveReinforcementWedge"
local REINFORCEMENT_CLASS = "JumboCaveReinforcementStructure"

local log = SMRFixPack.Log

-- One healing pass across every city. Returns the number of rocks cleared.
local function HealStuckReinforcements()
	local cities = rawget(_G, "Cities")
	if type(cities) ~= "table" then return 0 end

	local total = 0
	for _, city in ipairs(cities) do
		local labels = type(city) == "table" and city.labels
		local sites = type(labels) == "table" and labels.ConstructionSite
		if type(sites) == "table" and #sites > 0 then
			-- Built lazily, and only for a city that actually has a reinforcement
			-- site with rock still underneath: the set of objects this city's
			-- drones currently consider unreachable.
			local flagged

			for _, site in ipairs(sites) do
				if type(site) == "table" and IsValid(site)
						and site.building_class == REINFORCEMENT_CLASS then
					local rocks = site.waste_rocks_underneath
					if type(rocks) == "table" and #rocks > 0 then
						if not flagged then
							flagged = {}
							local drones = labels.Drone
							if type(drones) == "table" then
								for _, d in ipairs(drones) do
									local ub = type(d) == "table" and d.unreachable_buildings
									if type(ub) == "table" then
										for b in pairs(ub) do
											flagged[b] = true   -- keys include a plain "version"; harmless
										end
									end
								end
							end
						end

						local cleared_here = false
						for i = #rocks, 1, -1 do
							local rock = rocks[i]
							if IsValid(rock) and IsKindOf(rock, "WasteRockObstructor")
									and flagged[rock] then
								DoneObject(rock)   -- synchronous OnWasteRockObstructorCleared(false)
								total = total + 1
								cleared_here = true
							end
						end

						if cleared_here and site:HasMember("TestBlockerClearenceProgress") then
							site:TestBlockerClearenceProgress()
						end
					end
				end
			end
		end
	end
	return total
end

local function RunHeal()
	local n = HealStuckReinforcements()
	if n > 0 then
		log("%s: force-cleared %d unreachable waste rock(s) blocking a Jumbo Cave reinforcement",
			FIX_ID, n)
	end
end

-- Reactive: unwedge saves already stuck (heals within an in-game hour of load, as
-- the drones re-attempt and re-flag the rock the NewHour pass then clears).
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, RunHeal)
-- Proactive: catch a wedge as soon as it forms during play.
OnMsg.NewHour = SMRFixPack.WhenActive(FIX_ID, RunHeal)

SMRFixPack.Register(FIX_ID, {
	title = "Jumbo Cave reinforcements no longer soft-lock on a Waste Rock the drones cannot reach",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "Cities" },
			{ global = "IsValid" },
			{ global = "IsKindOf" },
			{ global = "DoneObject" },
			{ class = "WasteRockObstructor" },
			{ class = "ConstructionSite", method = "TestBlockerClearenceProgress" },
		})
		if err then return err end
		-- Nothing at apply time: the OnMsg handlers do the work (F87).
	end,
})
