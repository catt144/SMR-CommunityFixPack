-- F53: Newly arrived colonists set off for a dome they cannot reach and die on
-- the way — or land inside terrain they cannot walk out of.
--
-- Two defects on the arrival path:
--  (a) Colonist:Arrive (Lua\Units\Colonist.lua:1254-1300) drops the colonist at
--      the rocket's raw "Colonistout" spot — `self:SetPos(pos)` with no
--      passability search. Its sibling CargoTransporterNew:EjectColonists goes
--      through GetRandomPassableAroundOnMap for exactly this reason. On uneven
--      ground, or next to a Universal Depot, arrivals land somewhere they cannot
--      leave.
--  (b) Arrive then does `return self:SetCommand("TransportByFoot", dome)`
--      unconditionally. `dome` comes from ChooseDome (_GameUtils.lua:426-441),
--      which falls back to `safety_dome` — and GetDomesReachableByColonists picks
--      safety_dome by raw distance, WITHOUT the `is_walking` test that every real
--      candidate has to pass (:346-395). So the fallback is routinely a dome the
--      colonist cannot walk to, and the hike burns their oxygen.
--
-- Elevator routes are NOT part of the bug and must not be caught by the fix.
-- The arrival pipeline assigns emigration_dome and emigration_elevator together
-- (RocketBase.lua:2068-2071, CargoTransporterNew.lua:952-953) and TransportByFoot
-- rides that elevator to the destination map (Colonist.lua:2724-2737, with a train
-- fallback on the far side at :2740-2744). IsInWalkingDistDome returns false
-- outright whenever the two maps differ (Dome.lua:248-251), so a plain walking-
-- distance test rejects EVERY legitimate cross-map arrival. The re-check below
-- therefore accepts a destination that the assigned elevator can reach, using the
-- same conditions the shipped code itself relies on:
--    ValidateBuilding(elevator)                       -- Colonist.lua:2725
--    IsSameMap(colonist, elevator)                    -- Unit:UseElevator, Unit.lua:945
--    elevator.other and elevator.other:GetMapSlot()   -- Colonist.lua:2728 assert,
--        == dome:GetMapSlot()                            Colonist:EnterBuilding,
--                                                        ColonistTransport.lua:580
-- (Whether the elevator itself is worth walking to was already decided when it was
-- picked — GetDomesReachableByColonists:370-374 — so we do not second-guess it.)
-- When the re-choose DOES run it takes both of ChooseDome's returns and writes the
-- new elevator back to self.emigration_elevator (clearing it to `false`, the class
-- default at Colonist.lua:264, when the new route needs none). Arrive only clears
-- emigration_dome (:1261); leaving a stale elevator behind would make
-- TransportByFoot ride it to the wrong map, fail its map-slot check (:2731) and
-- SetCommand("Abandoned") (:2736).
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\Units\Colonist.lua:1254-1300 (shipped Src, game 1.0.7.396349) with two changes,
-- marked -- FIX:
--   1. snap the disembark position to a passable point when the spot itself is not;
--   2. before walking, check the destination really is reachable — on foot, or
--      through the elevator it was assigned. If not, re-run the normal selection
--      over the walkable candidates only, keeping destination and elevator in sync;
--      if that finds nothing, fall into the shipped "no dome" branch — the colonist
--      waits by the rocket under the "Confused Colonists" notification and gets
--      another chance on its next update instead of walking to its death.

SMRFixPack.Register("ArrivalDeaths", {
	title = "Arriving colonists no longer hike to unreachable domes or land in impassable ground",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.Arrive) ~= "function" then
			return "Colonist.Arrive not found (game update changed it?)"
		end
		for _, name in ipairs{ "IsInWalkingDist", "GetDomesReachableByColonists", "ChooseDome",
				"AddObjectToNotification", "IsKindOfClasses", "ValidateBuilding", "IsSameMap" } do
			if type(rawget(_G, name)) ~= "function" then
				return name .. " not found (game update changed it?)"
			end
		end
		-- GetMapSlot is an engine method; CObject's copy is only flattened onto the
		-- classes later, so check the table it is published from instead.
		local cobj_funcs = rawget(_G, "g_CObjectFuncs")
		if type(cobj_funcs) ~= "table" or type(cobj_funcs.GetMapSlot) ~= "function" then
			return "CObject:GetMapSlot not found (game update changed it?)"
		end

		function C:Arrive()
			local rocket = self.arriving
			assert(rocket)
			if not rocket then
				return
			end
			local dome = self.emigration_dome or self.dome
			-- FIX (F53b): remember the route that was assigned together with the dome,
			-- before anything on this path can clear it.
			local emigration_elevator = self.emigration_elevator
			self.emigration_dome = nil
			self:PushDestructor(self.OnArrival)
			if not IsKindOfClasses(rocket, "SupplyRocketBase", "UniversalRocketBase") then
				-- backward compatibility
				if rocket.parent_dome then
					self:SetOutside(false)
				end
				rocket:OnEnterUnit(self)
			else
				if HintsEnabled ~= "off" then
					HintTrigger("HintDecorations")
					HintTrigger("HintComfortStatAndServices")
				end

				--@@@msg ColonistArrived,colonist- fired when a colonist has arrived on Mars with a rocket.
				Msg("ColonistArrived", self)

				self:SetOutside(true)
				-- disembark
				local spot = rocket:GetSpotBeginIndex("Colonistout")
				local pos = rocket:GetSpotLoc(spot)
				-- FIX (F53a): the shipped code sets this position blind; find a passable
				-- one when the spot itself is not walkable.
				local map = self:GetMap()
				if map and not map:IsPassable(pos) then
					pos = map:GetPassablePointNearby(pos, self.pfclass) or pos
				end
				rocket:Attach(self, spot)
				self:SetDisembarkAnim(rocket)
				self:PushDestructor(function(self)
					Sleep(self:TimeToAnimEnd())
					self:Detach()
					self:SetPos(pos)
					self:SetState("idle")
					table.remove_value(rocket.disembarking, self)
				end)
				self:PopAndCallDestructor() -- Disembark uninterruptible

				-- FIX (F53b): ChooseDome's safety_dome fallback is picked by distance
				-- alone and may not be walkable at all. Re-choose among the walkable
				-- candidates rather than marching there — but only when the assigned
				-- elevator does not already provide the route (cross-map arrivals are
				-- never "in walking dist", Dome.lua:248-251).
				if dome then
					local elevator = ValidateBuilding(emigration_elevator)
					local reachable = IsInWalkingDist(dome, self:GetPos(), self.city)
						or (elevator and IsSameMap(self, elevator) and elevator.other
							and elevator.other:GetMapSlot() == dome:GetMapSlot())
					if not reachable then
						local domes, _, _, dome_elevators = GetDomesReachableByColonists(self.city, self:GetPos())
						local new_dome, new_elevator = ChooseDome(self.traits, domes, false, dome_elevators)
						dome = new_dome or false
						-- TransportByFoot rides self.emigration_elevator (:2725); keep it
						-- paired with the destination we just picked.
						self.emigration_elevator = new_elevator or false
					end
				end

				if not dome then
					AddObjectToNotification(self, nil, "ConfusedColonists", self:GetMap())
				else
					return self:SetCommand("TransportByFoot", dome)
				end
			end
			self:PopAndCallDestructor() -- OnArrival
		end
	end,
})
