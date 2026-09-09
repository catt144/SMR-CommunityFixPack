-- F53: Newly arrived colonists set off for a dome they cannot reach and die on
-- the way — or land inside terrain they cannot walk out of.
-- F86 Tier-2 REWRITE (2026-08-01, spec `docs/reports/SAVE_SAFETY_REDESIGN.md`
-- §6.2 Tier 2). The module no longer replaces `Colonist:Arrive`. Half (b) moves
-- ahead of it onto a layer-2 pre-wrapper; half (a) moves behind it onto a
-- verified-synchronous seam — the design pass §6.2 flagged as owed, run and
-- answered below.
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
--      candidate has to pass (:346-423). So the fallback is routinely a dome the
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
--    IsSameMap(rocket, elevator)                      -- Unit:UseElevator, Unit.lua:945
--    elevator.other and elevator.other:GetMapSlot()   -- Colonist.lua:2728 assert,
--        == dome:GetMapSlot()                            Colonist:EnterBuilding,
--                                                        ColonistTransport.lua:580
-- (Whether the elevator itself is worth walking to was already decided when it was
-- picked — GetDomesReachableByColonists:370-374 — so we do not second-guess it.)
--
-- ── HALF (b): the re-choose moves AHEAD of Arrive (layer 2) ─────────────────
-- `Colonist:Arrive` yields directly (`Sleep(self:TimeToAnimEnd())` in the
-- disembark destructor, :1285) and is F86 route (a), REPLACE-class, so the copy
-- we shipped until 2026-08-01 had to go. It cannot be repaired from the inside
-- either: the destination is read into a LOCAL at :1260 (`self.emigration_dome or
-- self.dome`) before anything else in the body runs, so no seam after that line —
-- not the `ColonistArrived` message at :1276, not the disembark — can still change
-- where the colonist is sent.
--
-- What CAN change it is the field, before Arrive reads it. The route into Arrive
-- is single and known: `Colonist:Idle` is the only place in the shipped source
-- that issues it (`if self.arriving then self:SetCommand("Arrive")`, :1791-1793),
-- and `RocketBase:2015` confirms the enumeration by listing exactly the states an
-- arriving colonist can be in. So this module PRE-wraps `Colonist:Idle`, keyed on
-- `self.arriving`, and corrects `emigration_dome`/`emigration_elevator` there.
-- Vanilla's Arrive then reads the corrected pair and its own `if not dome` branch
-- (:1293-1294) does the rest: the colonist waits by the rocket under the "Confused
-- Colonists" notification and gets another chance on its next update, instead of
-- walking to its death.
--
-- Layer 2, per FIX_POLICY §3a: all the work happens BEFORE `orig_idle`, and the
-- wrapper ends in `return orig_idle(...)` with nothing after it — so whether or
-- not the frame is serialised, an uninstalled save has nothing of ours left to
-- execute. This is the same shape `Fix_ShelterReflex` already uses on this exact
-- method, which the §5.3 sweep classified "already compliant". The accepted
-- residual is an inert captured frame.
--
-- Position: the check runs from the ROCKET's position (`self.arriving:GetPos()`),
-- not the colonist's — the colonist is not placed until Arrive's disembark
-- destructor. That is the same reference point the original assignment used
-- (`GetDomesReachableByColonists(city, self:GetPos())` with `self` the rocket,
-- RocketBase.lua:2029, :1981), so the re-check is judged on vanilla's own terms.
-- Every function it calls is VERIFIED SYNCHRONOUS — `IsInWalkingDist`,
-- `GetDomesReachableByColonists`, `ChooseDome`, `ValidateBuilding`, `IsSameMap`
-- all report `clear` under `tools/blocking_analysis.py` — so nothing in the
-- re-choose can itself put us on a blocked stack.
--
-- ⚠️ Why not wrap `ChooseDome` itself, which is where the bad fallback is born:
-- because the blast radius is wrong. `ChooseDome` has EIGHT shipped call sites
-- (DroneFactory.lua:224, RocketBase.lua:1985/:2068/:2105, CargoTransporterNew.lua
-- :907/:951/:975, Colonist.lua:1149) and only the arrival ones are F53's subject.
-- Suppressing an unreachable fallback globally would change android spawning and
-- the "Abandoned" path (Colonist.lua:1149-1160, which has its OWN oldest-failed-
-- dome fallback and its own walking-distance test at :1163) — behaviour with no
-- evidence behind it, which FIX_POLICY §4 does not permit. Keying on
-- `self.arriving` is the narrowest thing that separates the call sites, per §5.3.
--
-- ── HALF (a): the passability snap moves BEHIND Arrive (design pass, answered) ─
-- §6.2's warning was that the raw `SetPos` has no route: it happens inside the
-- disembark destructor (:1284-1290), after a `Sleep`, on a value captured into an
-- upvalue at :1281. Nothing can change `pos` from outside. But the fix never
-- needed to change `pos` — it needs the colonist to END UP somewhere walkable,
-- and there is a shipped seam immediately after the placement that is
-- arrival-specific and does not yield: `Colonist:OnArrival`.
--
-- `OnArrival` is pushed as Arrive's outer destructor at :1262 and runs after the
-- disembark destructor has already done `SetPos(pos)` — on the notification path
-- via :1299, and on the walking path inside `SetCommand`'s destructor pass, which
-- runs BEFORE `TransportByFoot` starts (CommandObject.lua:225-235). It is
-- **VERIFIED SYNCHRONOUS**: its body is an assert, three field writes,
-- `UpdateHomelessLabels`, `UpdateEmploymentLabels`, `ChangeComfort` and
-- `GameTime()` (Colonist.lua:1302-1311), and it plus all three callees report
-- `clear` under `tools/blocking_analysis.py`. So a PRE-wrapper there is a layer-3
-- class seam: our frame exists only during synchronous execution and can never be
-- captured by a save.
--
-- The snap is gated on the harm actually being present — no holder, a valid
-- position, and that position not passable — which is self-limiting in two useful
-- ways. It also repairs `Colonist:ReturnFromExpedition` (:4168-4197), which has
-- the identical raw `SetPos(pos)` disembark and was never covered by the old
-- replacement; and it cannot reach the spawn paths that also call `OnArrival`
-- from `GameInit` (:215-217), because those colonists either have a holder
-- (DroneFactory.lua:230) or have no position yet when it fires (RocketBase.lua
-- :2106-2112 places them only afterwards, and with `GetRandomPassableAroundOnMap`
-- already).
--
-- ── §3a COMPLIANCE, stated ─────────────────────────────────────────────────
-- The module owns no thread and replaces no body. Half (a) is a wrapper on the
-- verified-synchronous `Colonist:OnArrival` — route (a) closed outright. Half (b)
-- is a layer-2 pre-wrapper on `Colonist:Idle` whose accepted residual is an inert
-- captured frame with nothing after the call. Both are held only by the `Colonist`
-- classdef (safe by construction, route (b)) and neither stores a function value
-- (route (c)).
-- SAVE FOOTPRINT (FIX_POLICY §3): none. The two fields written — `emigration_dome`
-- and `emigration_elevator` — are vanilla's own (Colonist.lua:92, :264) and carry
-- vanilla values.
--
-- ── F117: WHICH ARGUMENT DOES `ChooseDome` TAKE? A behaviour probe, not a label ─
-- 1.1.0 changed `ChooseDome`'s first argument from the traits table to the
-- COLONIST (`_GameUtils.lua:486-500`; 1.0.7 `:426-441`), and both callees it
-- reaches now index `.traits` off that argument
-- (`Community:GetScoreFor` 1.1.0 `Buildings/Community.lua:445` vs 1.0.7 `:374`;
-- `Community:HasFreeLivingSpaceFor` 1.1.0 `:402-418` vs 1.0.7 `:335-352`).
-- Passing the wrong one is a defect in BOTH directions, and they are not the
-- same defect:
--   * a traits table on the 1.1.0 body → `colonist.traits` is nil →
--     `FilterObjectAttributes(filter, nil)` indexes nil and THROWS, inside the
--     arriving colonist's `Idle` command thread (F117, the P1);
--   * a colonist on the 1.0.7 body → `traits[attrib]` is nil for every trait →
--     no throw, every dome silently MIS-SCORED. Decision 118 (FIX_POLICY §2a)
--     exists to forbid exactly that, and it is the worse of the two.
-- ⛔ So the argument may not be chosen by a version label. `EF-077`: our
-- `lua_revision` and both of 1.1.0's minimums are all 350453 — there is no field
-- to read, which is also why nothing warns a 1.0.7 player who installs this.
--
-- The shape change is visible only at CALL time — `ChooseDome`'s own body barely
-- moved, its CALLERS are what changed — so the probe drives one of the two
-- callees `ChooseDome` invokes with that argument and asks which table it looks
-- the trait up in. It cannot run at apply time: the 1.1.0 body opens on
-- `g_Consts.CommunityEval*`, a per-game GameVar, so it runs once on first use.
-- Fail-closed: neither shape, or a throw, means the re-choose stands down and
-- vanilla's own destination survives (FIX_POLICY §2a, probe property 2 —
-- UNKNOWN is not permission).
--
-- Why `Community.GetScoreFor` is the right body to read: `ChooseDome` walks the
-- `domes` list from `GetDomesReachableByColonists`, which inserts only `Dome`s
-- (`_GameUtils.lua:449-478` — the `Station` sweep contributes their `.labels.Dome`,
-- never a station), and no `Dome` declares `GetScoreFor` on either tree, so
-- `dome:GetScoreFor` resolves to the `Community` body the probe reads. The
-- sibling callee `HasFreeLivingSpaceFor` moved in the same commit and takes the
-- identical value from the identical call site, so it cannot want a different
-- argument without vanilla being broken — that is the one step of this leg not
-- separately measured, and it is recorded as such in `bugs/F117.md`.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Units/Colonist.lua Colonist:Arrive sha256=0e52eeb274cecb7b51f33cd06bfd4a640241155e9cfcdadadce986490ed644b1
--   (Lua/Units/Colonist.lua:1586-1632 at pin time)
-- DEFECT: self:SetPos\(pos\)
--   the raw spot is used with no passability search

SMRFixPack.Register("ArrivalDeaths", {
	title = "Arriving colonists no longer hike to unreachable domes or land in impassable ground",
	apply = function()
		local err = SMRFixPack.Require("ArrivalDeaths", {
			{ class = "Colonist", method = "Idle" },
			{ class = "Colonist", method = "OnArrival" },
			-- the body we now deliberately leave alone; the repair depends on its
			-- shape (it reads emigration_dome at :1260 and owns the "no dome"
			-- branch at :1293), so a game update that removes it must deactivate us
			{ class = "Colonist", method = "Arrive" },
			{ global = "IsInWalkingDist" },
			{ global = "GetDomesReachableByColonists" },
			{ global = "ChooseDome" },
			-- F117: the body the argument-shape probe drives, and the one
			-- constant its two branches share. Existence only — WHICH argument
			-- it wants is a behaviour question and is asked at first use.
			{ class = "Community", method = "GetScoreFor" },
			{ path = { "const", "Scale", "Stat" }, kind = "number" },
			{ global = "ValidateBuilding" },
			{ global = "IsSameMap" },
			-- GetMapSlot is an engine method; CObject's copy is only flattened
			-- onto the classes later, so check the table it is published from.
			{ path = { "g_CObjectFuncs", "GetMapSlot" }, kind = "function",
			  reason = "CObject:GetMapSlot not found (game update changed it?)" },
		})
		if err then return err end
		local C = Colonist

		-- (a) never leave an arrival standing in ground it cannot walk out of
		local orig_onarrival = C.OnArrival
		function C:OnArrival(...)
			-- FIX (F53a): the shipped disembark sets the position blind, from the
			-- rocket's raw "Colonistout" spot. This runs after that placement and
			-- before the colonist is asked to walk anywhere.
			if not self.holder and self:IsValidPos() then
				local map = self:GetMap()
				local pos = self:GetPos()
				if map and pos and not map:IsPassable(pos) then
					local pt = map:GetPassablePointNearby(pos, self.pfclass)
					if pt then
						self:SetPos(pt)
					end
				end
			end
			return orig_onarrival(self, ...)
		end

		-- ── F117-PROBE-BEGIN (extracted verbatim by the desk falsifier) ──────
		-- A key no trait preset can carry. `FilterObjectAttributes` walks
		-- `pairs(filter)` (`Lua/Filter.lua:113-121`, byte-identical on both
		-- trees), so the stub filter's single key is the ONLY attribute either
		-- body looks up, and it is ours: no real trait, preset or save value is
		-- involved in the answer.
		local PROBE_TRAIT = "SMRFixPack_F117_Probe"

		-- nil until probed; then "colonist" (the 1.1.0 contract), "traits" (the
		-- 1.0.7 contract) or false (UNKNOWN — stand down).
		local arg_shape

		-- ⛔ STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3). Every
		-- field below is read straight off the two shipped bodies; nothing is
		-- here to make the call "work":
		--     self:HasLifeSupport()    1.1.0 `Community.lua:443` · 1.0.7 `:363`
		--     self.traits_filter       1.1.0 `:445`              · 1.0.7 `:374`
		--     self.labels.Residence    1.1.0 `:448`              · 1.0.7 `:386`
		--     self.free_spaces.traits  1.0.7 `:377` only — that body does
		--                              `pairs(self.free_spaces and ...traits)`,
		--                              which throws on nil, so the stub must
		--                              carry an empty one to reach 1.0.7's verdict
		-- WHY THE TARGET IS SAFE TO CALL ON ONE. Each body is: a read of those
		-- fields; `TraitFilterColonist` → `FilterObjectAttributes`, which is a
		-- `pairs` walk and integer adds and nothing else; a `Max`; and one
		-- division by `const.Scale.Stat`. Both accumulate into a LOCAL and assign
		-- NOTHING — not to `self`, not to the argument, not to a global (unlike
		-- the sibling `HasFreeLivingSpaceFor`, which may call
		-- `RefreshFreeLivingSpaces`; that is why the probe drives this body and
		-- not that one). With an EMPTY residence list neither body enters its
		-- residence loop, so `IsSuitable`, `GetResidenceComfort` and
		-- `GetFreeSpace` are never reached and no real object is touched at all.
		-- Nothing sleeps, waits, posts a message or starts a thread: synchronous
		-- and side-effect-free, shown from the shipped bodies as §2a requires.
		--
		-- The two calls differ ONLY in where the probe trait is hung, so the
		-- life-support term — the one value that genuinely differs between the
		-- branches (`g_Consts.CommunityEvalNoLifeSupport` vs a literal 0) —
		-- cancels in the DIFFERENCE, and the surviving 1 names which table the
		-- shipped body indexed. No branch of this reads a constant's value.
		local function discriminate()
			local stub = {
				HasLifeSupport = function() return false end,
				traits_filter = { [PROBE_TRAIT] = 1 },
				labels = { Residence = {} },
				free_spaces = { traits = {} },
			}
			-- trait hung on the ARGUMENT: +1 on the 1.0.7 body, +0 on 1.1.0
			local as_traits = Community.GetScoreFor(stub, { [PROBE_TRAIT] = true, traits = {} })
			-- trait hung on the argument's `.traits`: +1 on 1.1.0, +0 on 1.0.7
			local as_colonist = Community.GetScoreFor(stub, { traits = { [PROBE_TRAIT] = true } })
			if type(as_traits) ~= "number" or type(as_colonist) ~= "number" then
				return false
			end
			if as_colonist - as_traits == 1 then
				arg_shape = "colonist"
			elseif as_traits - as_colonist == 1 then
				arg_shape = "traits"
			else
				-- neither table was looked up, or both were: not a shape we
				-- know, and a guess here is the F114 failure mode.
				return false
			end
			return true
		end

		-- One shot. `false` is a decided verdict (UNKNOWN), not "not yet asked",
		-- so the decline is logged exactly once and never re-tried. Routed
		-- through `Require`'s `probe` form so the pcall trap, the strict-`true`
		-- rule and the decline logging are the shared ones, not re-implemented.
		local probed = false
		local function choose_dome_arg(colonist)
			if not probed then
				probed = true
				local err = SMRFixPack.Require("ArrivalDeaths", {
					{ probe = discriminate,
					  reason = "ChooseDome's argument contract could not be read from Community:GetScoreFor" },
				})
				if err then
					arg_shape = false
					SMRFixPack.Log("ArrivalDeaths: %s -- the F53(b) arrival re-choose stands down for this session (F117)", err)
				end
			end
			if arg_shape == "colonist" then return colonist end
			if arg_shape == "traits" then return colonist.traits end
			return nil
		end
		-- ── F117-PROBE-END ───────────────────────────────────────────────────

		-- (b) do not send an arrival to a dome it cannot reach
		local orig_idle = C.Idle
		function C:Idle(...)
			-- FIX (F53b): Idle is the only issuer of "Arrive" (:1791-1793), and
			-- Arrive reads emigration_dome into a local before anything else runs —
			-- so this is the last moment the destination can still be corrected.
			-- ChooseDome's safety_dome fallback is picked by distance alone and may
			-- not be walkable at all; re-choose among the walkable candidates
			-- rather than marching there, but only when the assigned elevator does
			-- not already provide the route (cross-map arrivals are never "in
			-- walking dist", Dome.lua:248-251).
			local rocket = self.arriving
			local dome = rocket and self.emigration_dome
			if dome and IsValid(rocket) and rocket:IsValidPos() and self.city then
				local pos = rocket:GetPos()
				local elevator = ValidateBuilding(self.emigration_elevator)
				local reachable = IsInWalkingDist(dome, pos, self.city)
					or (elevator and IsSameMap(rocket, elevator) and elevator.other
						and elevator.other:GetMapSlot() == dome:GetMapSlot())
				if not reachable then
					-- F117: what ChooseDome wants is asked of the shipped body,
					-- once, and only on the branch that is about to call it.
					-- `nil` is UNKNOWN and means STAND DOWN — vanilla's own
					-- destination survives untouched, which is exactly what a
					-- player got before this module existed.
					local dome_arg = choose_dome_arg(self)
					if dome_arg ~= nil then
						local domes, _, _, dome_elevators = GetDomesReachableByColonists(self.city, pos)
						-- safety_dome deliberately withheld: the walkable candidates
						-- are the only acceptable answers here
						local new_dome, new_elevator = ChooseDome(dome_arg, domes, false, dome_elevators)
						-- TransportByFoot rides self.emigration_elevator (:2725); keep
						-- it paired with the destination we just picked. `false` is the
						-- class default for both (Colonist.lua:92, :264).
						self.emigration_dome = new_dome or false
						self.emigration_elevator = new_elevator or false
					end
				end
			end
			return orig_idle(self, ...)
		end
	end,
})
