-- C120: an automated Earth-bound rocket waits for its departing-colonist count
-- to reach zero while its own hourly draft keeps refilling that count, so with
-- a deport law on it can sit on the pad for good; a landed rocket with no
-- destination drafts deportees and holds them. See docs/agent/bugs/C120.md.
-- Line numbers are archived 1.1.1.405907.
--
-- Fix shape K2 + E, chosen by the owner 2026-09-28 (no cap, no timeout):
--
-- K2 (wrap UniversalRocketBase:IsCargoReady). Only when vanilla answers "not
-- ready" and the same body answers "ready" with AreEarthDepartColonistsReady
-- forced true (UniversalRocket.lua:535-559) -- departures are the only thing
-- holding the launch -- the rocket boards every deportee it can safely take
-- now, then launches. Boarding goes through the game's own path for a deportee
-- who cannot reach the rocket (Colonist:LeavingMars, Units/Colonist.lua:1161-
-- 1175): the colonist gets the raw LeavingMars command, as ExitVehicle and
-- StartTransport issue it (Units/ColonistTransport.lua:703, :371), and a
-- one-shot mark makes Colonist:FindExit (:1049-1057, whose only caller is
-- :1161) answer false for that rocket, so `reached_exit` is false, `rocket_left`
-- is false and the shipped branch dehydrates the colonist into rocket.boarded
-- and runs CleanupLeavingColonist. Colonist:SetCommand is bypassed because it
-- reroutes LeavingMars by train or home when the pad is out of walking range
-- (ColonistTransport.lua:419-446). The gate stays shut while a colonist this
-- load cycle sent is still on its way into that branch (old-command destructors
-- run first), then opens even if walkers, train riders or committed shuttle
-- rides are still pending. Takeoff releases those exactly as a manual Launch
-- does (rocket_left, Colonist.lua:1163-1175; StopDepartureThread, UniversalRocket
-- .lua:2385-2402) and they catch the next rocket.
--   Takeable = GenerateDepartures's own pre-draft test (CanChangeCommand, no
--   transport_ticket, IsColonistValidForDeparture; UniversalRocket.lua:2250)
--   plus the expedition draft's thread_running_destructors skip
--   (CargoTransporterNew.lua:250), and further: not already in LeavingMars,
--   not arriving (Colonist.lua:1639), no shuttle already committed to its
--   transport task (vanilla never cancels one: :2288, :2394), same map slot as
--   the rocket (LeavingMars sends a colonist on another map to Abandoned,
--   Colonist.lua:1148-1153), and not already tried in a live load cycle. Each
--   colonist is sent at most once per load cycle, so the boarding pass ends.
--
-- E (wrap UniversalRocketBase:UpdateDepartureThread). A player rocket on our
-- colony with no destination takes the branch the shipped body already takes
-- for a non-Earth destination (UniversalRocket.lua:2362-2366): hand back the
-- boarded, stop the draft thread. HourlyUpdate calls UpdateDepartureThread every
-- hour while landed (:1574), so an idle rocket in an existing save stops within
-- the hour; setting a destination restarts the draft through SetFlightData (:772).
--
-- Veto: K2 and E run through SMRFixPack.WhenActive, which reads the registry
-- status and SMRFixPack_Disabled on every call (00_Core.lua), so setting
-- SMRFixPack_Disabled.DeportRocketLaunch mid-session turns both off until it
-- is cleared; the wrappers then return vanilla's answer untouched.
--
-- Save safety, FIX_POLICY 3a layer 3: both wrappers and FindExit's are
-- synchronous and hold no yield. State is two module-local weak-keyed tables;
-- nothing is written to a saved object except `leaving_elevator = nil`, the
-- value LeavingMars itself sets (Colonist.lua:1142). No thread, GameVar or
-- saved callback. A save taken while a sent colonist is still in its old
-- command's destructors loses the mark, and that colonist walks as a vanilla
-- draftee would.
--
-- Branch: no body is copied. On 1.0.7.396349 the relied-on shapes read the same
-- (LeavingMars :825-908 with FindExit at :861, AreEarthDepartColonistsReady
-- :451-453, UpdateDepartureThread :1913-1936); desk-run on 1.1.1 only.
--
-- Pin: archived 1.1.1.405907 (byte-identical to the live ModTools\Src, 2026-09-28).
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:AreEarthDepartColonistsReady sha256=83227afd071b9590210225b968f5c6222c3b0d0f905a90d9c90bc8d0fc1f7fef
-- DEFECT: GetPendingDepartureCount\(\)\s*==\s*0
--   the gate waits for zero on a count the rocket's own draft refills
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:IsCargoReady sha256=4fd9a73ae5742edc23a26b65a42cda5053da4dd6f6c717b21ad7222af72a6f83
-- DEFECT: if\s+not\s+self:AreEarthDepartColonistsReady\(\)\s+then\s+return\s+false
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:UpdateDepartureThread sha256=7b27f5cacaa06d7bbc77e39feb4e9f1d395f8d45bdefbe47608dc416ffe3887d
-- DEFECT: \(self\.arrival_loc\s+and\s+self:GetArrivalLocType\(\)\s*~=\s*"earth"\)
--   no destination falls through to the draft thread
-- Route dependencies, pinned for drift only:
-- SRC: Lua/Units/Colonist.lua Colonist:LeavingMars sha256=f55ace356f023f9d84ceb2408f80b5bf5d666885f32a6847c93aaa00912708a9
-- SRC: Lua/Units/Colonist.lua Colonist:FindExit sha256=ff60f299d512cf0cffb3849bf967736c4ea9866aca09b062305f9db041b28f39
-- SRC: Lua/Units/Colonist.lua CleanupLeavingColonist sha256=75622dc52f90574d3cc4decc8118f7c75bca9e24c1322b68ee09107c98cf6519
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:GenerateDepartures sha256=add3ca0c57bd74530fa3c0cadd8802a9faf784035a0e891a457baae6562e2a3e
-- SRC: Lua/UniversalRocket.lua UniversalRocketBase:StopDepartureThread sha256=b7cea08e857d29845a8fc8163c8e63a9c546523d0e28296300d0b76226be11b8

local FIX_ID = "DeportRocketLaunch"
local installed = false

-- colonist -> the rocket command thread (one load cycle) that sent it
local sent = setmetatable({}, { __mode = "k" })
-- colonist -> that thread, until FindExit consumes it
local marks = setmetatable({}, { __mode = "k" })
-- the rocket whose AreEarthDepartColonistsReady reads true for one synchronous call
local forcing = false

local function is_candidate(rocket)
	return rocket.RocketType == g_RocketTypes.Player
		and rocket:GetDepartureLocType() == "our_colony"
		and rocket:GetArrivalLocType() == "earth"
		and rocket:IsRocketLanded()
		and type(rocket.departures) == "table"
		and type(rocket.boarded) == "table"
		and rocket.command_thread
end

local function is_takeable(rocket, colonist, slot)
	local sent_by = sent[colonist]
	if sent_by and IsValidThread(sent_by) then return false end
	local task = colonist.transport_task
	return colonist:CanChangeCommand()
		and not colonist.thread_running_destructors
		and colonist.command ~= "LeavingMars"
		and not colonist.transport_ticket
		and not colonist.arriving
		and not (task and task.shuttle)
		and colonist:GetMapSlot() == slot
		and rocket:IsColonistValidForDeparture(colonist)
end

-- true while a colonist sent this load cycle has not reached FindExit yet
local function still_boarding(cycle)
	local waiting = false
	for colonist, by in pairs(sent) do
		if by == cycle then
			if marks[colonist] == cycle and IsValid(colonist) and colonist.command == "LeavingMars" then
				waiting = true
			elseif marks[colonist] == cycle then
				marks[colonist] = nil
			end
		end
	end
	return waiting
end

local function forget(cycle)
	for colonist, by in pairs(sent) do
		if by == cycle then
			sent[colonist] = nil
			if marks[colonist] == cycle then
				marks[colonist] = nil
			end
		end
	end
end

local function send_takeable(rocket, cycle)
	local colonists = rawget(_G, "UIColony") and UIColony.labels and UIColony.labels.Colonist
	if type(colonists) ~= "table" then return 0 end
	local slot = rocket:GetMapSlot()
	local n = 0
	for _, colonist in ipairs(colonists) do
		if IsValid(colonist) and is_takeable(rocket, colonist, slot) then
			sent[colonist] = cycle
			marks[colonist] = cycle
			colonist.leaving_elevator = nil
			CommandObject.SetCommand(colonist, "LeavingMars", rocket)
			n = n + 1
		end
	end
	return n
end

local function pending_count(rocket)
	if rocket.GetPendingDepartureCount then
		return rocket:GetPendingDepartureCount()
	end
	return #rocket.departures
end

SMRFixPack.Register(FIX_ID, {
	title = "An automatic rocket to Earth boards the deportees it can take and launches instead of waiting forever; a rocket with no destination stops drafting",
	apply = function()
		if installed then return end
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "UniversalRocketBase", method = "IsCargoReady" },
			{ class = "UniversalRocketBase", method = "AreEarthDepartColonistsReady" },
			{ class = "UniversalRocketBase", method = "UpdateDepartureThread" },
			{ class = "UniversalRocketBase", method = "ReturnDehydratedColonists" },
			{ class = "UniversalRocketBase", method = "StopDepartureThread" },
			{ class = "UniversalRocketBase", method = "IsColonistValidForDeparture" },
			{ class = "UniversalRocketBase", method = "GetArrivalLocType" },
			{ class = "UniversalRocketBase", method = "GetDepartureLocType" },
			{ class = "UniversalRocketBase", method = "IsRocketLanded" },
			{ class = "Colonist", method = "FindExit" },
			{ class = "Colonist", method = "LeavingMars" },
			{ class = "Colonist", method = "CanChangeCommand" },
			{ class = "CommandObject", method = "SetCommand" },
			{ global = "IsValid" },
			{ global = "IsValidThread" },
			{ path = { "g_RocketTypes", "Player" }, kind = "any" },
		})
		if err then return err end
		local R = UniversalRocketBase

		local orig_ready = R.AreEarthDepartColonistsReady
		function R:AreEarthDepartColonistsReady(...)
			if forcing and forcing == self then return true end
			return orig_ready(self, ...)
		end

		local orig_cargo = R.IsCargoReady
		-- true when K2 opens the gate; nil keeps vanilla's answer. WhenActive
		-- re-reads status and SMRFixPack_Disabled on every call, so the veto
		-- switches K2 off and on mid-session.
		local k2 = SMRFixPack.WhenActive(FIX_ID, function(self, instant, ...)
			if not is_candidate(self) then return end
			-- FIX (C120 K2): would this rocket launch now if departures were done?
			forcing = self
			local ok, would = pcall(orig_cargo, self, instant, ...)
			forcing = false
			if not ok or not would then return end
			local cycle = self.command_thread
			local waiting = still_boarding(cycle)
			local n = send_takeable(self, cycle)
			if n > 0 then
				SMRFixPack.Log("%s: rocket %s boarding %d deportee(s) before launch", FIX_ID, tostring(self.handle), n)
			end
			if waiting or n > 0 then return end
			forget(cycle)
			local left = pending_count(self)
			if left > 0 then
				SMRFixPack.Log("%s: rocket %s launching; %d departure(s) in transit are released", FIX_ID, tostring(self.handle), left)
			end
			return true
		end)
		function R:IsCargoReady(instant, ...)
			local ready = orig_cargo(self, instant, ...)
			if ready or instant then
				return ready
			end
			return k2(self, instant, ...) or ready
		end

		local orig_update = R.UpdateDepartureThread
		local e = SMRFixPack.WhenActive(FIX_ID, function(self)
			-- FIX (C120 E): no destination is treated like a non-Earth one
			if not self.arrival_loc and self.RocketType == g_RocketTypes.Player
					and self:GetDepartureLocType() == "our_colony" then
				self:ReturnDehydratedColonists()
				self:StopDepartureThread()
				return true
			end
		end)
		function R:UpdateDepartureThread(...)
			if e(self) then return end
			return orig_update(self, ...)
		end

		-- Not gated: a mark exists only for a colonist K2 already sent, and
		-- honouring it lets that boarding finish if the veto is set mid-way.
		local C = Colonist
		local orig_exit = C.FindExit
		function C:FindExit(rocket, ...)
			local cycle = marks[self]
			if cycle then
				marks[self] = nil
				if rocket and cycle == rocket.command_thread and rocket.command == "CmdLoad" then
					return false
				end
			end
			return orig_exit(self, rocket, ...)
		end

		installed = true
	end,
})
