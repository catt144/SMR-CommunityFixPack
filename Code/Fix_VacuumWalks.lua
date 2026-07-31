-- F52: Colonists cross open vacuum on foot between two domes that are joined by
-- a passage, and suffocate on the way.
--
-- Defect: Colonist:TryToEmigrateToDome (Lua\Units\Colonist.lua:1545-1590) only
-- looks for a passage route when the walk is long enough:
--     local min_dist = GetAtmosphereBreathable(self:GetMap()) and dome_passage_dist or dome_walk_dist
--     if transport_mode_dist > min_dist then passage_path = GetDomesPassagePath(...) end
-- In a non-breathable atmosphere min_dist is const.ColonistMaxDomeWalkDist
-- (400m, _GameConst.lua:133) — but that is the very cap that makes "walk" mode
-- possible in the first place (IsInWalkingDistDome / CheckWalkableDistance,
-- Dome.lua:186-198). For two domes closer than 400m the test can therefore never
-- pass, no passage path is ever computed, and TransportByFoot sends the colonist
-- across the surface. 400m is roughly a 100-second walk against
-- g_Consts.OxygenMaxOutsideTime of 120 seconds (__const.lua:1604) — leaving the
-- dome, queueing at the entrance and any detour spend the rest. This is the
-- original long-walk suffocation bug, still present.
--
-- Patch approach: full replacement of the method — a copy of
-- Lua\Units\Colonist.lua:1545-1590 (shipped Src, game 1.0.7.396349) with one change: in a
-- non-breathable atmosphere look for a passage route for ANY distance. The walk
-- branch below already forwards `passage_path` to TransportByFoot, so the
-- colonist simply uses the passages that exist. Breathable maps keep the shipped
-- threshold exactly (walking outside is safe there, so passages are not worth the
-- detour).
--
-- Deliberately NOT changed: when no passage route exists the colonist still walks
-- across the surface. Refusing that walk (holding out for a shuttle) would strand
-- colonists on maps with no shuttle coverage — that is a behaviour change, not a
-- defect repair, and is tracked as the remaining half of F52 in BUGS.md.

SMRFixPack.Register("VacuumWalks", {
	title = "Colonists use the passages instead of crossing vacuum on foot between nearby domes",
	apply = function()
		local err = SMRFixPack.Require("VacuumWalks", {
			{ class = "Colonist", method = "TryToEmigrateToDome" },
			{ global = "GetAtmosphereBreathable" },
			{ global = "GetDomesPassagePath" },
			{ global = "IsLRTransportAvailable" },
			{ global = "IsTransportAvailableBetween" },
			{ global = "CreateColonistTransportTask" },
			{ path = { "const", "ColonistMaxDomeWalkDist" },
			  reason = "walk-distance constants not found (game update changed them?)" },
			{ path = { "const", "ColonistMinDistToIgnorePassage" },
			  reason = "walk-distance constants not found (game update changed them?)" },
		})
		if err then return err end
		local C = Colonist

		function C:TryToEmigrateToDome(current_dome, dest_dome, transport_mode, transport_mode_dist)
			local transport_task = self.transport_task
			if not dest_dome then
				if transport_task then
					self:ClearTransportRequest()
				end
				return
			end

			if transport_mode == "walk" then
				local passage_path
				local passage_path_domes = 0
				local dome_walk_dist = const.ColonistMaxDomeWalkDist
				local dome_passage_dist = const.ColonistMinDistToIgnorePassage
				-- FIX (F52): shipped value here was dome_walk_dist, the same 400m cap
				-- that makes walk mode possible — so in vacuum this test never passed
				-- and no passage route was ever looked up.
				local min_dist = GetAtmosphereBreathable(self:GetMap()) and dome_passage_dist or 0
				if transport_mode_dist > min_dist then
					-- try to lead the colonist through the dome passages if the domes are in the same network
					passage_path = GetDomesPassagePath(current_dome, dest_dome)
					passage_path_domes = passage_path and (#passage_path - 2) or 0
				end

				if not passage_path or (transport_mode_dist < dome_passage_dist and passage_path_domes < const.ColonistMaxPassagePassthroughDomes)
						or self.emigration_elevator -- no shuttles to elevators
						or not IsLRTransportAvailable(self.city) then
					self:ClearTransportRequest()
					dest_dome:ReserveResidence(self)
					self:SetCommand("TransportByFoot", dest_dome, passage_path)
					return
				end
			end

			if transport_task then
				if dest_dome ~= transport_task.dest_dome then
					dest_dome:ReserveResidence(self)
					transport_task.dest_dome = dest_dome
				end
				return
			end

			local src_dome = current_dome or self.dome or FindNearestObject(self.city.labels.Community, self)
			--check shuttle availability,
			--if shuttles are available register for transport, shuttle will Setcommand when it picks up the task
			if IsTransportAvailableBetween(src_dome, dest_dome) and CreateColonistTransportTask(self, src_dome, dest_dome) then
				dest_dome:ReserveResidence(self)
				self.transport_task.state = "almost_ready_for_pickup" --so a shuttle can immidiately pick this task up
			end
		end
	end,
})
