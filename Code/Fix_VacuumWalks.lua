-- F52/F125: nearby passage-linked domes in vacuum use their passage instead
-- of sending a migrating colonist over the surface.
--
-- Game 1.1.1.405907 keeps F52 in two places. TryToEmigrateToDome chooses the
-- ordinary 400m walk cap as its vacuum passage threshold (Colonist.lua:1911),
-- and the new multi-leg MigrateStep repeats it for an intermediate walk
-- (:2199). The old module copied the 1.1.0 TryToEmigrateToDome body, which
-- erased 1.1.1's task-retarget, BookShuttleRide and migration_dest machinery.
--
-- This rebase composes with both shipped bodies instead:
--   * layer 3: TryToEmigrateToDome gets an input-only wrapper. For a short,
--     positive vacuum walk with a real passage, it raises only the distance
--     argument across the lookup threshold while keeping it below the later
--     passage-detour threshold. The native body then owns path length, elevator,
--     shuttle availability, reservations, tickets, commands and every return.
--     No-passage and unsafe-threshold calls delegate their original input.
--   * layer 3: MigrateStep remains entirely native. GetNextMigrationLeg arms a
--     one-call input marker only for its synchronous, non-final walk result;
--     IsInWalkingDistDome consumes that marker and reports -1 as the distance
--     for a short vacuum leg. MigrateStep uses that value only to decide whether
--     to call GetDomesPassagePath, then discards it (Colonist.lua:2198-2202).
--
-- The marker is weak-keyed by the actual command thread and requires the same
-- colonist, command, command_thread, current dome, leg dome and city. It is
-- removed before the distance body runs. A cancellation, nested call, later
-- method override, malformed leg or any unexpected next distance query can
-- therefore only make this repair decline; it cannot leak into a later query.
--
-- Callers re-read on archived 1.1.1.405907: TryToEmigrateToDome is called by
-- TryToMigrateHome (ColonistTransport.lua:864), TryToEmigrate (:2068, :2074)
-- and MigrateStep (:2181). GetNextMigrationLeg is called at
-- ColonistTransport.lua:679/:853 and Colonist.lua:2166/:3803/:4330; only :2166
-- runs with command MigrateStep. IsInWalkingDistDome has seven Lua callers
-- (Dome.lua:296; ColonistTransport.lua:863; Colonist.lua:1473,2072,2178,2198,
-- 3317); only :2198 can match the armed record.
--
-- Save/removal disposition: all three wrappers are synchronous. The direct
-- wrapper tail-calls its captured body; GetNextMigrationLeg completes before
-- its wrapper arms the one-call marker. No function is
-- stored on a game object and no mod body replaces the blocking MigrateStep
-- command. The weak marker is process-local closure state, is consumed before a
-- possible yield, and is unreachable after the global wrappers are removed.
-- No persisted residue is created.
--
-- MANIFEST (FIX_POLICY 2b), pinned to archived game 1.1.1.405907.
-- SRC: Lua/Units/Colonist.lua Colonist:TryToEmigrateToDome sha256=062bb2e6eee996c8fbc5e7e20db5c4a0b7c3f286ffb098285eb4b895781fd2f1
--   (Lua/Units/Colonist.lua:1894-1982 at pin time)
-- DEFECT: GetAtmosphereBreathable\(self:GetMap\(\)\)\s+and\s+dome_passage_dist\s+or\s+dome_walk_dist
-- SRC: Lua/Units/Colonist.lua Colonist:MigrateStep sha256=ac305027ecb82916ed11b5181607ce46cb4b1cc3996d7939a66d258acbcd2724
--   (Lua/Units/Colonist.lua:2155-2221 at pin time)
-- DEFECT: GetAtmosphereBreathable\(self:GetMap\(\)\)\s+and\s+g_Consts.ColonistMinDistToIgnorePassage\s+or\s+g_Consts.ColonistMaxDomeWalkDist
-- SRC: Lua/Units/Colonist.lua Colonist:GetNextMigrationLeg sha256=deba3d7951de6c358a04a316457c748641255bbd00040eeb0c061cf8d240ecb7
--   (Lua/Units/Colonist.lua:3709-3717 at pin time)
-- SRC: Lua/Buildings/Dome.lua IsInWalkingDistDome sha256=3c297c411ecc954fbcb052610a6ea76e8728d3c3de6961c7a7887510245b54f0
--   (Lua/Buildings/Dome.lua:299-319 at pin time)

SMRFixPack.Register("VacuumWalks", {
	title = "Colonists use the passages instead of crossing vacuum on foot between nearby domes",
	apply = function()
		local C = rawget(_G, "Colonist")
		local has_multileg = type(C) == "table"
			and type(C.MigrateStep) == "function"
			and type(C.GetNextMigrationLeg) == "function"
			and type(C.StartShuttleLeg) == "function"
		local has_any_multileg = type(C) == "table"
			and (C.MigrateStep ~= nil or C.GetNextMigrationLeg ~= nil or C.StartShuttleLeg ~= nil)
		if has_any_multileg and not has_multileg then
			return "the multi-leg migration methods are incomplete (game update changed them?)"
		end

		local function has_110_helpers()
			local D = rawget(_G, "Dome")
			return type(rawget(_G, "HasShuttleLandingSlots")) == "function"
				and type(D) == "table" and type(D.ReserveWorkplace) == "function"
				and type(C) == "table" and type(C.CancelWorkReservation) == "function"
		end

		local function is_107_shape()
			local c = rawget(_G, "const")
			return type(c) == "table" and type(c.ColonistMaxDomeWalkDist) == "number"
				and rawget(_G, "HasShuttleLandingSlots") == nil
		end

		local function thresholds_have_expected_order()
			local c = rawget(_G, "const")
			local colonist = type(c) == "table" and c.Colonist
			return type(colonist) == "table"
				and type(colonist.ColonistMaxDomeWalkDist) == "number"
				and type(colonist.ColonistMinDistToIgnorePassage) == "number"
				and colonist.ColonistMaxDomeWalkDist + 1 < colonist.ColonistMinDistToIgnorePassage
		end

		-- 1.1.0 branch probe. On its shipped body CanWork is evaluated before a
		-- committed shuttle task returns. The 1.0.7 body returns without asking.
		local function shipped_computes_need_work()
			if type(C) ~= "table" or type(C.TryToEmigrateToDome) ~= "function" then return false end
			local asked = false
			local dest = {}
			local colonist = {
				transport_task = { shuttle = true, dest_dome = dest },
				CanWork = function() asked = true return false end,
			}
			C.TryToEmigrateToDome(colonist, false, dest, "shuttle", 0)
			return asked
		end

		-- 1.1.1 branch probe. StartShuttleLeg:2016-2029 is synchronous here:
		-- the supplied task already goes to landing, so BookShuttleRide is never
		-- called. The only side effect is migration_dest on this local stub.
		local function shipped_carries_multileg_destination()
			if not has_multileg then return false end
			local final, landing = {}, {}
			local task = { dest_dome = landing, migration_dest = true }
			local colonist = { transport_task = task, emigration_dome = final }
			local ok = C.StartShuttleLeg(colonist, false, landing)
			return ok == true and task.migration_dest == final
		end

		local specs = {
			{ class = "Colonist", method = "TryToEmigrateToDome" },
			{ test = has_110_helpers,
			  reason = "the shipped emigration code has no work-slot reservation or shuttle landing slots; this repair stands down on the older body" },
			{ global = "GetAtmosphereBreathable" },
			{ global = "AreDomesConnectedWithPassage" },
			{ path = { "const", "Colonist", "ColonistMaxDomeWalkDist" }, kind = "number",
			  reason = "walk-distance constants not found at const.Colonist.* (game update changed them?)" },
			{ path = { "const", "Colonist", "ColonistMinDistToIgnorePassage" }, kind = "number",
			  reason = "walk-distance constants not found at const.Colonist.* (game update changed them?)" },
			{ test = thresholds_have_expected_order,
			  reason = "there is no safe integer gap between the dome walk and passage-detour thresholds; the selective distance input is unsafe" },
			{ probe = has_multileg and shipped_carries_multileg_destination or shipped_computes_need_work,
			  reason = has_multileg
				and "the shipped multi-leg migration body does not carry migration_dest through StartShuttleLeg; this repair stands down on an unknown shape"
				or "the shipped TryToEmigrateToDome does not compute its work reservation before a committed shuttle return; this repair stands down on an unknown shape" },
		}
		if has_multileg then
			specs[#specs + 1] = { class = "Colonist", method = "MigrateStep" }
			specs[#specs + 1] = { class = "Colonist", method = "GetNextMigrationLeg" }
			specs[#specs + 1] = { class = "Colonist", method = "StartShuttleLeg" }
			specs[#specs + 1] = { global = "IsInWalkingDistDome" }
			specs[#specs + 1] = { global = "IsUnitInDome" }
			specs[#specs + 1] = { global = "CurrentThread" }
			specs[#specs + 1] = { path = { "table", "pack" }, kind = "function" }
			specs[#specs + 1] = { path = { "table", "unpack" }, kind = "function" }
		end

		local err = SMRFixPack.Require("VacuumWalks", specs)
		if err then
			if not is_107_shape() then
				local entry = SMRFixPack.fixes["VacuumWalks"]
				if entry then entry.update_suspect = true end
			end
			return err
		end

		local orig_try = C.TryToEmigrateToDome
		local function wrapped_try(self, current_dome, dest_dome, transport_mode, transport_mode_dist)
			-- Longer and passage-only legs already enter the shipped lookup. All
			-- non-walk, malformed and breathable calls remain byte-for-byte native.
			local g = rawget(_G, "g_Consts")
			if not dest_dome or transport_mode ~= "walk" or type(transport_mode_dist) ~= "number"
					or transport_mode_dist <= 0 or type(g) ~= "table"
					or type(g.ColonistMaxDomeWalkDist) ~= "number"
					or type(g.ColonistMinDistToIgnorePassage) ~= "number"
					or g.ColonistMaxDomeWalkDist + 1 >= g.ColonistMinDistToIgnorePassage
					or transport_mode_dist > g.ColonistMaxDomeWalkDist
					or (self.transport_task and self.transport_task.shuttle and not self.emigration_elevator)
					or GetAtmosphereBreathable(self:GetMap()) then
				return orig_try(self, current_dome, dest_dome, transport_mode, transport_mode_dist)
			end

			-- GetDomesPassagePath:1300-1303 uses this exact read-only predicate
			-- as its own no-path gate. Testing it here avoids computing the same
			-- passage twice while preserving the no-passage surface fallback.
			if not AreDomesConnectedWithPassage(current_dome, dest_dome) then
				return orig_try(self, current_dome, dest_dome, transport_mode, transport_mode_dist)
			end

			-- FIX (F52): cross only the native passage-lookup threshold. The
			-- required gap proves this remains positive, avoids the -1 conversion,
			-- and stays below the later `< dome_passage_dist` choice. The distance
			-- is not used after that choice at :1922-1924.
			return orig_try(self, current_dome, dest_dome, transport_mode,
				g.ColonistMaxDomeWalkDist + 1)
		end

		if not has_multileg then
			C.TryToEmigrateToDome = wrapped_try
			return
		end

		local pending_by_thread = setmetatable({}, { __mode = "k" })
		local orig_next_leg = C.GetNextMigrationLeg
		local orig_walking_dist = IsInWalkingDistDome

		local set_err = SMRFixPack.SetGlobal("IsInWalkingDistDome", function(bld1, bld2, source_city)
			local thread = CurrentThread()
			local pending = thread and pending_by_thread[thread]
			if pending then
				-- Consume before calling the shipped body: recursion, errors and
				-- unexpected calls all fail closed instead of extending the window.
				pending_by_thread[thread] = nil
			end
			local result = table.pack(orig_walking_dist(bld1, bld2, source_city))
			local dist = result[2]
			if not pending
					or pending.colonist.command ~= "MigrateStep"
					or pending.colonist.command_thread ~= thread
					or pending.current_dome ~= bld2
					or pending.leg_dome ~= bld1
					or pending.city ~= source_city then
				return table.unpack(result, 1, result.n)
			end
			local g = rawget(_G, "g_Consts")
			if type(dist) == "number" and dist > 0 and type(g) == "table"
					and type(g.ColonistMaxDomeWalkDist) == "number"
					and type(g.ColonistMinDistToIgnorePassage) == "number"
					and g.ColonistMaxDomeWalkDist + 1 < g.ColonistMinDistToIgnorePassage
					and dist <= g.ColonistMaxDomeWalkDist
					and not GetAtmosphereBreathable(pending.colonist:GetMap()) then
				-- FIX (F52/F125): MigrateStep treats a negative distance as a
				-- passage-only leg and asks for the path; it does not use dist again.
				result[2] = -1
				if result.n < 2 then result.n = 2 end
			end
			return table.unpack(result, 1, result.n)
		end, "could not install the IsInWalkingDistDome wrapper")
		if set_err then return set_err end

		local function wrapped_next_leg(self, ...)
			local leg = orig_next_leg(self, ...)
			local thread = CurrentThread()
			if thread then
				pending_by_thread[thread] = nil
				local current_dome = self.command == "MigrateStep"
					and self.command_thread == thread and IsUnitInDome(self)
				if current_dome and type(leg) == "table" and leg.kind == "walk"
						and not leg.final and leg.dome then
					pending_by_thread[thread] = {
						colonist = self,
						current_dome = current_dome,
						leg_dome = leg.dome,
						city = self.city,
					}
				end
			end
			return leg
		end

		-- SetGlobal is the only checked write. Until it succeeds the marker is
		-- empty and inert; install both class wrappers only after that read-back,
		-- so a failed global write leaves every shipped declaration untouched.
		C.GetNextMigrationLeg = wrapped_next_leg
		C.TryToEmigrateToDome = wrapped_try
	end,
})
