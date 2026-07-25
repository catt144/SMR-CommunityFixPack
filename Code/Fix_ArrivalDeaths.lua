-- F53: Newly arrived colonists set off for a dome they cannot reach and die on
-- the way — or land inside terrain they cannot walk out of.
--
-- Two defects on the arrival path:
--  (a) Colonist:Arrive (Lua\Units\Colonist.lua:1253-1300) drops the colonist at
--      the rocket's raw "Colonistout" spot — `self:SetPos(pos)` with no
--      passability search. Its sibling CargoTransporterNew:EjectColonists goes
--      through GetRandomPassableAroundOnMap for exactly this reason. On uneven
--      ground, or next to a Universal Depot, arrivals land somewhere they cannot
--      leave.
--  (b) Arrive then does `return self:SetCommand("TransportByFoot", dome)`
--      unconditionally. `dome` comes from ChooseDome (_GameUtils.lua:426-441),
--      which falls back to `safety_dome` — and GetDomesReachableByColonists picks
--      safety_dome by raw distance, WITHOUT the `is_walking` test that every real
--      candidate has to pass (:353-365). So the fallback is routinely a dome the
--      colonist cannot walk to, and the hike burns their oxygen.
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\Units\Colonist.lua:1253-1300 (shipped Src, 2026-07) with two changes,
-- marked -- FIX:
--   1. snap the disembark position to a passable point when the spot itself is not;
--   2. before walking, check the destination really is in walking distance. If not,
--      re-run the normal selection over the walkable candidates only; if that
--      finds nothing, fall into the shipped "no dome" branch — the colonist waits
--      by the rocket under the "Confused Colonists" notification and gets another
--      chance on its next update instead of walking to its death.

SMRFixPack.Register("ArrivalDeaths", {
	title = "Arriving colonists no longer hike to unreachable domes or land in impassable ground",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.Arrive) ~= "function" then
			return "Colonist.Arrive not found (game update changed it?)"
		end
		for _, name in ipairs{ "IsInWalkingDist", "GetDomesReachableByColonists", "ChooseDome",
				"AddObjectToNotification", "IsKindOfClasses" } do
			if type(rawget(_G, name)) ~= "function" then
				return name .. " not found (game update changed it?)"
			end
		end

		function C:Arrive()
			local rocket = self.arriving
			assert(rocket)
			if not rocket then
				return
			end
			local dome = self.emigration_dome or self.dome
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
				-- candidates rather than marching there.
				if dome and not IsInWalkingDist(dome, self:GetPos(), self.city) then
					local domes, _, _, dome_elevators = GetDomesReachableByColonists(self.city, self:GetPos())
					dome = ChooseDome(self.traits, domes, false, dome_elevators) or false
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
