-- F52: Colonists cross open vacuum on foot between two domes that are joined by
-- a passage, and suffocate on the way.
--
-- Defect: Colonist:TryToEmigrateToDome (Lua\Units\Colonist.lua:1545-1590 on game
-- 1.0.7.396349; :1886-1983 on 1.1.0.403908) only looks for a passage route when
-- the walk is long enough:
--     local min_dist = GetAtmosphereBreathable(self:GetMap()) and dome_passage_dist or dome_walk_dist
--     if transport_mode_dist > min_dist then passage_path = GetDomesPassagePath(...) end
-- In a non-breathable atmosphere min_dist is ColonistMaxDomeWalkDist (400m;
-- const.ColonistMaxDomeWalkDist, _GameConst.lua:133 on 1.0.7; a DefineConstInt
-- read as g_Consts.ColonistMaxDomeWalkDist, :149 on 1.1.0) — but that is the very
-- cap that makes "walk" mode possible in the first place (IsInWalkingDistDome /
-- CheckWalkableDistance, Dome.lua:186-198 on 1.0.7; :209-231, :299-318 on 1.1.0).
-- For two domes closer than 400m the test can therefore never pass, no passage
-- path is ever computed, and TransportByFoot sends the colonist across the
-- surface. 400m is roughly a 100-second walk against g_Consts.OxygenMaxOutsideTime
-- of 120 seconds (__const.lua:1604 on 1.0.7) — leaving the dome, queueing at the
-- entrance and any detour spend the rest. This is the original long-walk
-- suffocation bug, still present.
--
-- Patch approach: full replacement of the method — a copy of the shipped body
-- with one change: in a non-breathable atmosphere look for a passage route for
-- ANY distance. The walk branch below already forwards `passage_path` to
-- TransportByFoot, so the colonist simply uses the passages that exist.
-- Breathable maps keep the shipped threshold exactly (walking outside is safe
-- there, so passages are not worth the detour).
--
-- Deliberately NOT changed: when no passage route exists the colonist still walks
-- across the surface. Refusing that walk (holding out for a shuttle) would strand
-- colonists on maps with no shuttle coverage — that is a behaviour change, not a
-- defect repair, and is tracked as the remaining half of F52 in BUGS.md.
--
-- RE-COPIED 2026-09-09 on game 1.1.0.403908 (hotfix2 link 04b, re-verification
-- row F-9, VANILLA_FIX_QA §0.5 + Reader A; owner ruling ck123 = repair). Three-way
-- diff, the archived 1.0.7 tree (C:\Dev\SMR-SrcArchive\1.0.7.396349\Src) against
-- the live 1.1.0 tree against our previous copy: our copy's non-FIX lines matched
-- 1.0.7 byte for byte. The defect line (:1903) is byte-identical on both branches
-- — 1.1.0 did not repair it — but 1.1.0 REWROTE the rest of the function (47 lines
-- became 98), and every one of those changes is carried:
--   1. `need_work` (:1894-1896): only a colonist who actually needs a job holds a
--      work slot, reserved on every branch that commits a destination
--      (`dest_dome:ReserveWorkplace(self)`, or `self:CancelWorkReservation()` when
--      the destination cannot reserve one; :1920-1926, :1943-1949, :1972-1978);
--   2. the walk branch is skipped when a shuttle already owns the colonist's
--      transport task, unless they are bound for an elevator (:1898);
--   3. the walk constants moved from `const.` to `g_Consts.` (:1901-1902) — read
--      at CALL time, as the shipped body does (g_Consts is a per-game GameVar,
--      Modifiers.lua:427, and does not exist at apply time);
--   4. a `-1` distance means "walkable only through passages, no outside foot
--      route" and is treated as infinitely far (`max_int`, :1904-1907);
--   5. the walk branch discards a train ticket (`self:DiscardTransportTicket()`,
--      :1918) before reserving and setting TransportByFoot;
--   6. the existing-task branch (:1932-1957) is a five-way ladder: a shuttle-owned
--      task returns; a different map clears the request; the same destination
--      returns; a destination with no landing slots returns; otherwise the task is
--      retargeted, and a colonist already walking to the pickup (`command ==
--      "Transport"`) has `emigration_dome` retargeted too;
--   7. the shuttle request requires landing slots at the destination
--      (`HasShuttleLandingSlots`, ShuttleHub.lua:110) and searches for a source
--      dome that has them — the current dome, else the nearest Community with
--      slots in the same city (`FindNearestObject` from `self.holder or self`),
--      else the colonist's own dome (:1959-1968).
-- Our previous 1.0.7 copy had NONE of these; re-arming it as it stood would have
-- reverted all seven, which is why it was left inactive (by accident — see the
-- gate note) until this re-copy. The body below is the 1.1.0 one (:1886-1983)
-- with the ONE FIX line re-applied at :1903. Deliberately NOT carried: nothing
-- from 1.1.0 is dropped.
-- ⛔ NEVER a distance pre-wrapper: `transport_mode_dist` also drives the `-1`
-- conversion (:1904-1907) and the walk-vs-shuttle choice at :1914; inflating it
-- would flip both. The QA pinned this shape (VANILLA_FIX_QA §0.5 item 5).
-- ⚠️ What the fix reaches on 1.1.0, narrower than on 1.0.7: a `-1` pair (no
-- outside route) already forces the passage lookup through the max_int
-- conversion, so the residual F52 case is "an outside route exists, shorter than
-- 400m, in vacuum" — the colonist would walk it on their oxygen timer. That is
-- the case this line repairs.
--
-- ⛔ THE GATE WAS ACCIDENTAL AND IS NOW DELIBERATE. From 2026-09-08 this module was
-- inactive on 1.1.0 only because its `{ path = { "const", "ColonistMaxDomeWalkDist" } }`
-- spec failed after the rename to g_Consts (gated110_* log: "walk-distance
-- constants not found") — an accident that would have re-armed a stale 1.0.7 body
-- into the rewritten function on the next rename (the F114 mechanism). Replaced by:
-- ⛔ BRANCH GUARD (FIX_POLICY §2a, checklist 118): this body is written for 1.1.0
-- and the module must DECLINE on 1.0.7, where it would call four things that do
-- not exist (HasShuttleLandingSlots, Dome:ReserveWorkplace,
-- Colonist:CancelWorkReservation — 0 hits each in the archived 1.0.7 tree — and
-- g_Consts.ColonistMaxDomeWalkDist) and throw inside a colonist command. There is
-- no version field to read (EF-077). Three checks, all testing the thing:
--   1. a branch `test` on the 1.1.0 declarations the rewritten body calls
--      (HasShuttleLandingSlots, Dome.ReserveWorkplace, Colonist.CancelWorkReservation)
--      — a `test`, so the 1.0.7 decline does not mark update_suspect;
--   2. shape specs for everything else the body reads, including the walk
--      constants at their 1.1.0 location: DefineConstInt("Colonist", id, ...)
--      registers the preset under const.Colonist[id] (ConstDef.lua:349-378,
--      GetConstGroup) — the same table TFormat.game_const falls back to outside a
--      game (Modifiers.lua:432). These DO mark update_suspect when they fail,
--      which is correct once check 1 has said "this is not 1.0.7";
--   3. a behaviour `probe` of the SHIPPED TryToEmigrateToDome on a stub colonist
--      whose transport task is shuttle-owned: the 1.1.0 body computes `need_work`
--      FIRST (:1896) and so calls self:CanWork() before anything else; the 1.0.7
--      body never calls CanWork. STUB CONTRACT is beside the probe.
-- Three-valued (link 03's F-1 lesson): 1.1.0 shape ⇒ apply; 1.0.7 shape (the
-- constants at `const.<id>`, HasShuttleLandingSlots absent) ⇒ decline, correct,
-- no update_suspect; anything else ⇒ decline AND update_suspect.
--
-- ⛔ NOT tested. Nothing here has run in a game; no colonist has emigrated on
-- 1.1.0 with this body installed, and vacuum walking has never been exercised on
-- 1.1.0 at all (the 09-08 boot was menu-only). A boot log line `VacuumWalks:
-- applied` proves the module loaded and the probe saw the 1.1.0 body — nothing
-- more. The 1.0.7 decline is argued from the archived tree and a desk harness.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-09 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Units/Colonist.lua Colonist:TryToEmigrateToDome sha256=b00f60fbcb953176973da9d2a09ba7acfea0084ec283721500635360c88c51cd
--   (Lua/Units/Colonist.lua:1886-1983 at pin time)
-- DEFECT: GetAtmosphereBreathable\(self:GetMap\(\)\)\s+and\s+dome_passage_dist\s+or\s+dome_walk_dist
--   in vacuum the passage lookup is gated on the SAME 400m cap that makes walk
--   mode possible, so it can never pass; a vanilla fix that lowers the vacuum
--   threshold (as ours does, to 0) or restructures the condition stops the match

SMRFixPack.Register("VacuumWalks", {
	title = "Colonists use the passages instead of crossing vacuum on foot between nearby domes",
	apply = function()
		local function has_110_helpers()
			local D, C = rawget(_G, "Dome"), rawget(_G, "Colonist")
			return type(rawget(_G, "HasShuttleLandingSlots")) == "function"
				and type(D) == "table" and type(D.ReserveWorkplace) == "function"
				and type(C) == "table" and type(C.CancelWorkReservation) == "function"
		end
		local function is_107_shape()
			-- 1.0.7: the walk constants live directly on `const` (this file's 1.0.7
			-- record, _GameConst.lua:133-134) and HasShuttleLandingSlots does not
			-- exist. Both halves required, so a tree with neither shape is named.
			local c = rawget(_G, "const")
			return type(c) == "table" and type(c.ColonistMaxDomeWalkDist) == "number"
				and rawget(_G, "HasShuttleLandingSlots") == nil
		end

		-- STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3), read from
		-- the shipped 1.1.0 TryToEmigrateToDome (Colonist.lua:1886-1983), the only
		-- code this call reaches on that body:
		--   * dest_dome          a non-nil stub, so the early return (:1887-1892)
		--                        is skipped;
		--   * self:CanWork()     the stub's; records the call and returns false,
		--                        so `need_work` short-circuits (:1896) before
		--                        IsValid(self.workplace) is evaluated;
		--   * transport_mode     "shuttle", so the walk branch (:1898) is skipped
		--                        and g_Consts — a per-game GameVar that is `false`
		--                        at apply time — is never read;
		--   * self.transport_task { shuttle = true, dest_dome = dest_dome }, so the
		--                        task branch returns at its FIRST rung (:1933),
		--                        before IsSameMap, HasShuttleLandingSlots or any
		--                        reservation. The 1.0.7 body reaches its own task
		--                        branch, finds dest_dome == transport_task.dest_dome
		--                        and returns too (1.0.7 :1578-1584) — without ever
		--                        calling CanWork.
		-- Synchronous: no thread, no Msg. Side-effect-free: nothing is written on
		-- either body. The verdict is whether the shipped body asked the stub
		-- CanWork(): yes = it computes need_work up front = 1.1.0; no = 1.0.7 or
		-- another body = decline; a throw = decline. Only the literal `true`
		-- applies (00_Core.lua, Require).
		local function shipped_computes_need_work()
			local C = rawget(_G, "Colonist")
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

		local CONSTS = "walk-distance constants not found at their 1.1.0 location (const.Colonist.*) — this copy of TryToEmigrateToDome is written for game 1.1.0 (game update changed them?)"
		local err = SMRFixPack.Require("VacuumWalks", {
			{ class = "Colonist", method = "TryToEmigrateToDome" },
			-- FIX (F-9, 2026-09-09) — the branch guard (FIX_POLICY §2a), check 1:
			-- the 1.1.0 declarations the rewritten body calls. A `test`, so a
			-- 1.0.7 decline does not mark update_suspect by itself.
			{ test = has_110_helpers,
			  reason = "the shipped emigration code has no work-slot reservation or shuttle landing slots (HasShuttleLandingSlots / Dome:ReserveWorkplace / Colonist:CancelWorkReservation) — this copy of TryToEmigrateToDome is written for game 1.1.0 and stands down on an older body" },
			{ global = "GetAtmosphereBreathable" },
			{ global = "GetDomesPassagePath" },
			{ global = "IsLRTransportAvailable" },
			{ global = "IsTransportAvailableBetween" },
			{ global = "CreateColonistTransportTask" },
			{ global = "FindNearestObject" },
			{ global = "IsSameMap" },
			{ global = "max_int", kind = "number" },
			{ class = "Colonist", method = "DiscardTransportTicket" },
			{ class = "Colonist", method = "ClearTransportRequest" },
			-- check 2: the walk constants at their 1.1.0 location (see header).
			{ path = { "const", "Colonist", "ColonistMaxDomeWalkDist" }, kind = "number", reason = CONSTS },
			{ path = { "const", "Colonist", "ColonistMinDistToIgnorePassage" }, kind = "number", reason = CONSTS },
			{ path = { "const", "ColonistMaxPassagePassthroughDomes" }, kind = "number", reason = CONSTS },
			-- check 3: the behaviour probe. Contract above.
			{ probe = shipped_computes_need_work,
			  reason = "the shipped TryToEmigrateToDome does not compute a work-slot reservation up front — this copy is written for game 1.1.0 and stands down on a different body" },
		})
		if err then
			-- Three-valued verdict. The 1.0.7 shape is a correct decline and is
			-- NOT patch rot. Anything else that declined is a pinned body over a
			-- function that moved again and must be named in the update report.
			-- (Check 2's shape specs already mark natively; this covers the
			-- `test` and `probe` routes.) `run_apply` clears `update_suspect`
			-- only on the ACTIVE branch (00_Core.lua), so a write here survives.
			if not is_107_shape() then
				local entry = SMRFixPack.fixes["VacuumWalks"]
				if entry then entry.update_suspect = true end
			end
			return err
		end
		local C = Colonist

		-- copy of Lua/Units/Colonist.lua:1886-1983 (1.1.0), one line changed
		function C:TryToEmigrateToDome(current_dome, dest_dome, transport_mode, transport_mode_dist)
			if not dest_dome then
				if self.transport_task then
					self:ClearTransportRequest()
				end
				return
			end

			-- only colonists that actually need a job hold a slot, so several emigrants don't all
			-- head for the same single opening and arrive to find it already filled
			local need_work = self:CanWork() and not IsValid(self.workplace) and not self.user_forced_workplace

			if transport_mode == "walk" and (not (self.transport_task and self.transport_task.shuttle) or self.emigration_elevator) then
				local passage_path
				local passage_path_domes = 0
				local dome_walk_dist = g_Consts.ColonistMaxDomeWalkDist
				local dome_passage_dist = g_Consts.ColonistMinDistToIgnorePassage
				-- FIX (F52): shipped value here was dome_walk_dist, the same 400m cap
				-- that makes walk mode possible — so in vacuum this test never passed
				-- and no passage route was ever looked up.
				local min_dist = GetAtmosphereBreathable(self:GetMap()) and dome_passage_dist or 0
				if transport_mode_dist < 0 then
					-- -1 means walkable only through passages (no outside foot route); treat as infinitely far outside
					transport_mode_dist = max_int
				end
				if transport_mode_dist > min_dist then
					-- try to lead the colonist through the dome passages if the domes are in the same network
					passage_path = GetDomesPassagePath(current_dome, dest_dome)
					passage_path_domes = passage_path and (#passage_path - 2) or 0
				end

				if not passage_path or (transport_mode_dist < dome_passage_dist and passage_path_domes < const.ColonistMaxPassagePassthroughDomes)
						or self.emigration_elevator -- no shuttles to elevators
						or not IsLRTransportAvailable(self.city) then
					self:ClearTransportRequest()
					self:DiscardTransportTicket()
					dest_dome:ReserveResidence(self)
					if need_work then
						if dest_dome.ReserveWorkplace then
							dest_dome:ReserveWorkplace(self)
						else
							self:CancelWorkReservation()
						end
					end
					self:SetCommand("TransportByFoot", dest_dome, passage_path)
					return
				end
			end

			if self.transport_task then
				if self.transport_task.shuttle then
					return
				elseif not IsSameMap(self, dest_dome) then
					self:ClearTransportRequest()
				elseif dest_dome == self.transport_task.dest_dome then
					return
				elseif not HasShuttleLandingSlots(dest_dome) then
					return
				else
					dest_dome:ReserveResidence(self)
					if need_work then
						if dest_dome.ReserveWorkplace then
							dest_dome:ReserveWorkplace(self)
						else
							self:CancelWorkReservation()
						end
					end
					self.transport_task.dest_dome = dest_dome
					if self.command == "Transport" then
						-- we are already walking to the pickup, and emigration_dome is what the end of the ride registers us into
						self.emigration_dome = dest_dome
					end
					return
				end
			end

			if HasShuttleLandingSlots(dest_dome) then
				local src_dome = current_dome and HasShuttleLandingSlots(current_dome) and current_dome
				if not src_dome and self.city == dest_dome.city and IsLRTransportAvailable(self.city) then
					src_dome = FindNearestObject(self.city.labels.Community, self.holder or self, function(obj)
						return IsValid(obj) and obj ~= dest_dome and HasShuttleLandingSlots(obj)
					end)
				end
				if not src_dome and self.dome and HasShuttleLandingSlots(self.dome) then
					src_dome = self.dome
				end
				if IsTransportAvailableBetween(src_dome, dest_dome) then
					if CreateColonistTransportTask(self, src_dome, dest_dome) then
						dest_dome:ReserveResidence(self)
						if need_work then
							if dest_dome.ReserveWorkplace then
								dest_dome:ReserveWorkplace(self)
							else
								self:CancelWorkReservation()
							end
						end
						self.transport_task.state = "almost_ready_for_pickup" --so a shuttle can immidiately pick this task up
					end
				end
			end
		end
	end,
})
