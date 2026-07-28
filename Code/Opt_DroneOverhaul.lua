-- D06 — OPTIONAL module, OFF BY DEFAULT. Not a bug fix: an assignment-POLICY
-- overhaul (core v1). Enable in-game: Options → Mod Options → Community Fix
-- Pack. Toggles take effect immediately in both directions — every hook below
-- consults SMRFixPack.IsActive per call and passes through while off. Design
-- study with the full option analysis: docs/DRONE_OVERHAUL_OPTIONS.md; the
-- underlying investigation is on the BUGS.md DroneControl bullet.
--
-- THE PROBLEM (traced 2026-07-28, live-observed 2026-07-27): drone task
-- assignment has no cross-hub locality anywhere. Assignment is pull-only —
-- an idle drone polls ONLY its own hub (`Drone:Idle`, Drone.lua:621, the sole
-- FindTask call site); a building in overlapping coverage posts its requests
-- into EVERY covering hub's queues; the claim is first-poller-wins, taken
-- before the approach and held for the whole trip (Drone.lua:898-924); repair
-- work requests are max_units=1 (RequiresMaintenance.lua:82). Net effect: a
-- hub 100 hexes away (via a Drone Hub Extender — a pure registration booster,
-- it holds no tasks) can claim a repair that four idle drones are parked on
-- top of, and nothing ever reassigns it.
--
-- WHAT THIS SHIPS (three parts):
--
--  1. CLOSEST-FLEET-FIRST CLAIM GATE — a chained wrapper on
--     `TaskRequestHub:FindTask` (_TaskRequest.lua:72-83; its ONLY caller is
--     the drone auto-Idle path, so player orders are structurally untouched).
--     When the C-side matcher hands a repair/clean WORK request to a hub that
--     is NOT the closest covering Drone Hub of the target building, and that
--     closest hub is working with idle drones, the result is withheld for
--     that poll — the near fleet (whose queue also holds the request) claims
--     it on its own next poll, seconds later. A per-request strike counter
--     (STRIKES_MAX polls, STRIKE_TTL decay) guarantees the veto can never
--     starve a request: if the near fleet doesn't take it (broken, drained,
--     unreachable-cached), the far fleet is allowed through. "Closest" is
--     extender-aware (FindDroneNodes + GetCommandCenter recursion — the same
--     machinery vanilla registration uses) and excludes hubs beyond
--     const.DroneRestrictRadius of the building (whose drones could not
--     legally travel there — the registered-but-unreachable pathology).
--
--  2. REPAIR MOONLIGHTING — a chained POST-wrapper on `Drone:Idle`. The
--     shipped Idle body falls through and returns EXACTLY when it found no
--     work at all (Drone.lua:564-641 ends in Sleep(2000) + CleanUnreachables;
--     every found-work branch SetCommands, which kills the thread before our
--     code — so vanilla own-hub priority is preserved for free; the F73
--     "pre-wrap only" rule is for command bodies that always SetCommand).
--     A workless drone then scans OTHER working Drone Hubs that are
--     SATURATED (zero idle drones of their own) for unclaimed repair/clean
--     work requests whose target building is near the drone (MOONLIGHT_MAX_
--     HEXES) and inside its own movement restriction, and takes one exactly
--     the way the shipped own-hub maintenance branch does (SetCommand "Work",
--     amount = Min(DroneResourceUnits[res], target) — Drone.lua:602-605).
--     Work requests live only in the per-hub priority_queue (plain Lua
--     arrays), so the scan needs no C matcher and no pairing logic.
--     Work/ApproachWrapper never consult command_center (Drone.lua:819-849,
--     :898-938), so cross-hub execution is mechanically clean; a lost claim
--     race lands in the shipped miss path (Sleep + back to Idle).
--
--  3. TELEMETRY — SMRFixPack.DroneReport(): per-hub load/idle/queue/extender
--     snapshot plus this module's counters, printed to the log like
--     ListFixes. Registered UNCONDITIONALLY (read-only; works with the
--     module toggled off) so playtests can always measure.
--
-- WHAT THIS DOES NOT TOUCH: PickUp/Deliver hauling (supply/demand pairing —
-- deliberately out of v1 scope; see H-v2/B in the options doc), construction
-- work (multi-fleet swarming on a build site is desirable), rover fleets
-- (RCRover inherits the same machinery but is player-zoned — every hook here
-- gates on DroneHubBase), rockets, shuttles, and the registration layer
-- (requests stay in every covering hub's queues — vanilla redundancy intact,
-- so toggling this module off restores vanilla behavior instantly and
-- completely).
--
-- Savegame footprint (FIX_POLICY §3): NONE. All state (strike counters,
-- caches, stats) is transient module-local with weak keys; no flags on
-- objects, no GameVars, no long-lived threads. Saves made with the module
-- enabled load identically without it.
--
-- Install pattern: hooks are installed at FILE SCOPE (classdef time, so they
-- propagate through class flattening) and gate per call on IsActive — the
-- Register apply() only validates targets / reports the opt-in status.

SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

-- Tunables (playtest iteration knobs — see FABLE_NEXT_PROMPT board notes)
local WORK_RES           = { repair = true, clean = true }
local STRIKES_MAX        = 4      -- vetoed polls per request before the far fleet is allowed through
local STRIKE_TTL         = 30000  -- game-ms; strike counters decay after this
local MOONLIGHT_MAX_HEXES = 30    -- drone-to-target cap for moonlight pickups
local HUB_MISS_TTL       = 2000   -- game-ms; one fruitless moonlight scan per hub per this window
local COVER_CACHE_TTL    = 5000   -- game-ms; closest-covering-hub answers cached this long

local weak_keys   = rawget(_G, "weak_keys_meta") or { __mode = "k" }
local strikes     = setmetatable({}, weak_keys)  -- request -> { n, t }
local cover_cache = setmetatable({}, weak_keys)  -- building -> { t, closest }
local hub_miss    = setmetatable({}, weak_keys)  -- hub -> GameTime of last fruitless scan
local stats = { vetoed = 0, veto_expired = 0, moonlighted = 0 }
SMRFixPack.DroneOverhaulStats = stats

local function module_active()
	return SMRFixPack.IsActive("DroneOverhaul")
end

-- Closest covering Drone Hub of a building, the way vanilla registration sees
-- coverage: FindDroneNodes returns every DroneNode (hubs AND extenders) whose
-- work_radius covers the building; GetCommandCenter maps a working extender
-- to its uplink hub (DroneHubExtender.lua:156-160). Hubs beyond the drones'
-- own movement restriction are excluded — their fleet cannot legally serve
-- the spot regardless of what the registration layer says.
local function closest_covering_hub(src)
	local now = GameTime()
	local c = cover_cache[src]
	if c and now - c.t < COVER_CACHE_TTL then
		return c.closest
	end
	local closest, best = false, nil
	if type(src.FindDroneNodes) == "function" then
		local reach = const.DroneRestrictRadius
		for _, node in ipairs(src:FindDroneNodes() or empty_table) do
			local cc = node:GetCommandCenter()
			if cc and IsValid(cc) and IsKindOf(cc, "DroneHubBase") and cc:GetDist2D(src) <= reach then
				local d = HexAxialDistance(cc, src)
				if not best or d < best or (d == best and cc.handle < closest.handle) then
					best, closest = d, cc
				end
			end
		end
	end
	cover_cache[src] = { t = now, closest = closest }
	return closest
end

-- Validate every target before installing anything; apply() reports failures.
local install_error
do
	local TRH = rawget(_G, "TaskRequestHub")
	local D = rawget(_G, "Drone")
	local TR = rawget(_G, "TaskRequester")
	if type(TRH) ~= "table" or type(TRH.FindTask) ~= "function" then
		install_error = "TaskRequestHub.FindTask not found (game update changed it?)"
	elseif type(D) ~= "table" or type(D.Idle) ~= "function" then
		install_error = "Drone.Idle not found (game update changed it?)"
	elseif type(TR) ~= "table" or type(TR.FindDroneNodes) ~= "function" then
		install_error = "TaskRequester.FindDroneNodes not found (game update changed it?)"
	elseif not (const.rfWork and const.DroneRestrictRadius and const.MaxBuildingPriority) then
		install_error = "expected const values missing (game update changed them?)"
	elseif type(rawget(_G, "DroneResourceUnits")) ~= "table" then
		install_error = "DroneResourceUnits not found (game update changed it?)"
	end
end

if not install_error then

	-- Part 1: closest-fleet-first claim gate ---------------------------------
	local TRH = TaskRequestHub
	local orig_findtask = TRH.FindTask
	function TRH:FindTask(agent, flags, ...)
		local request, pair_request, resource, amount, priority = orig_findtask(self, agent, flags, ...)
		if request and not pair_request and module_active()
				and IsKindOf(self, "DroneHubBase") and WORK_RES[resource] then
			local src = request:GetSource(agent)
			-- own-hub self-repair and mobile requesters are never second-guessed
			if IsValid(src) and src ~= self and not IsKindOf(src, "Unit") then
				local closest = closest_covering_hub(src)
				if closest and closest ~= self and IsValid(closest) and closest.working
						and closest:GetIdleDronesCount() > 0 then
					local now = GameTime()
					local s = strikes[request]
					if not s or now - s.t > STRIKE_TTL then
						s = { n = 0, t = now }
						strikes[request] = s
					end
					if s.n < STRIKES_MAX then
						-- FIX (D06): the closest fleet has idle drones and the same
						-- request in its own queue — yield this poll to it. The
						-- strike cap makes starvation impossible: if the near
						-- fleet doesn't claim within a few of our polls, we serve.
						s.n, s.t = s.n + 1, now
						stats.vetoed = stats.vetoed + 1
						return nil
					end
					stats.veto_expired = stats.veto_expired + 1
				end
			end
		end
		return request, pair_request, resource, amount, priority
	end

	-- Part 2: repair moonlighting --------------------------------------------
	local D = Drone
	local orig_idle = D.Idle
	function D:Idle()
		orig_idle(self)
		-- reached ONLY when the shipped Idle found nothing and fell through
		if not module_active() then return end
		local own = self.command_center
		if not (IsValid(self) and IsValid(own) and IsKindOf(own, "DroneHubBase") and own.working) then return end
		if self.resource or self:IsDisabled() then return end
		if self.battery <= g_Consts.DroneEmergencyPower * 2 then return end
		local now = GameTime()
		local city = self.city
		local hubs = city and city.labels and city.labels.DroneControl or empty_table
		for _, hub in ipairs(hubs) do
			if hub ~= own and IsValid(hub) and IsKindOf(hub, "DroneHubBase") and hub.working
					and hub:GetIdleDronesCount() == 0
					and not (hub_miss[hub] and now - hub_miss[hub] < HUB_MISS_TTL) then
				for p = const.MaxBuildingPriority, -1, -1 do
					local q = hub.priority_queue and hub.priority_queue[p]
					for i = 1, #(q or "") do
						local req = q[i]
						if req:IsAnyFlagSet(const.rfWork) and req:CanAssignUnit() then
							local res = req:GetResource()
							if WORK_RES[res] and req:GetTargetAmount() > 0 then
								local src = req:GetSource(self)
								if IsValid(src) and src:IsValidPos() and not IsKindOf(src, "Unit")
										and not (self.unreachable_buildings and self.unreachable_buildings[src])
										and HexAxialDistance(self, src) <= MOONLIGHT_MAX_HEXES
										and own:GetDist2D(src) <= const.DroneRestrictRadius then
									local closest = closest_covering_hub(src)
									-- leave it alone only if ANOTHER hub is closest
									-- and has idle drones of its own to serve it
									if not (closest and closest ~= own and IsValid(closest)
											and closest.working and closest:GetIdleDronesCount() > 0) then
										-- FIX (D06): take the nearby job the way the
										-- shipped own-hub maintenance branch does
										stats.moonlighted = stats.moonlighted + 1
										self:SetCommand("Work", req, res,
											Min(DroneResourceUnits[res] or const.ResourceScale, req:GetTargetAmount()))
										-- SetCommand does not return (kills this thread)
									end
								end
							end
						end
					end
				end
				hub_miss[hub] = now
			end
		end
	end

end -- install guard

-- Part 3: telemetry (always available, read-only) ----------------------------
local function say(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

function SMRFixPack.DroneReport()
	local low = const.DroneLoadLowThreshold or max_int
	local med = const.DroneLoadMediumThreshold or max_int
	for _, map in ipairs(rawget(_G, "LoadedMaps") or empty_table) do
		local city = map.City
		for _, hub in ipairs(city and city.labels and city.labels.DroneControl or empty_table) do
			if IsValid(hub) and IsKindOf(hub, "DroneHubBase") then
				local lap = hub:CalcLapTime()
				local load = (not low or lap < low) and "low" or (lap < med and "medium") or "HEAVY"
				local qparts, work, unclaimed = {}, 0, 0
				for p = const.MaxBuildingPriority, -1, -1 do
					local q = hub.priority_queue and hub.priority_queue[p]
					local n = #(q or "")
					qparts[#qparts + 1] = "p" .. p .. ":" .. n
					for i = 1, n do
						local req = q[i]
						if req:IsAnyFlagSet(const.rfWork) then
							work = work + 1
							if req:CanAssignUnit() and req:GetTargetAmount() > 0 then
								unclaimed = unclaimed + 1
							end
						end
					end
				end
				local exts = {}
				for _, e in ipairs(hub.linked_extenders or empty_table) do
					exts[#exts + 1] = e.handle .. (e.working and ":on" or ":off")
				end
				say("hub %s:%d w=%s drones=%d idle=%d broken=%d lap=%d(%s) q={%s} work=%d unclaimed=%d ext={%s}",
					hub.class, hub.handle, tostring(hub.working and true or false),
					#hub.drones, hub:GetIdleDronesCount(), hub:GetBrokenDronesCount(),
					lap, load, table.concat(qparts, " "), work, unclaimed, table.concat(exts, ","))
			end
		end
	end
	say("DroneOverhaul %s — vetoed=%d veto_expired=%d moonlighted=%d",
		module_active() and "ACTIVE" or "off", stats.vetoed, stats.veto_expired, stats.moonlighted)
end

SMRFixPack.Register("DroneOverhaul", {
	title = "OPTIONAL: drone dispatch overhaul — closest fleet gets first claim on repairs; idle drones help overloaded neighbor hubs",
	optional = true,
	apply = function()
		if install_error then
			return install_error
		end
		if not SMRFixPack.OptionEnabled("DroneOverhaul") then
			return "opt-in module, off by default — enable it in Options → Mod Options"
		end
	end,
})
