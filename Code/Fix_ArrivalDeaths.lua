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
					local domes, _, _, dome_elevators = GetDomesReachableByColonists(self.city, pos)
					-- safety_dome deliberately withheld: the walkable candidates are
					-- the only acceptable answers here
					local new_dome, new_elevator = ChooseDome(self.traits, domes, false, dome_elevators)
					-- TransportByFoot rides self.emigration_elevator (:2725); keep it
					-- paired with the destination we just picked. `false` is the class
					-- default for both (Colonist.lua:92, :264).
					self.emigration_dome = new_dome or false
					self.emigration_elevator = new_elevator or false
				end
			end
			return orig_idle(self, ...)
		end
	end,
})
