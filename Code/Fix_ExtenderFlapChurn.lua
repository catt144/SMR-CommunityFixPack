-- F77: Every Drone Hub Extender working-transition tears down and rebuilds the
-- ENTIRE uplink hub's requester registration — twice per power blip.
--
-- Defect: DroneHubExtenderBase:OnSetWorking (Lua\Buildings\DroneHubExtender.lua
-- :171-178) calls UpdateUplinkRequesters (:109-112) on EVERY working
-- transition, in BOTH directions, and that helper is not incremental: it runs
-- a full uplink:DisconnectTaskRequesters() + ConnectTaskRequesters()
-- (DroneControl.lua:441-450, :327-360). The teardown walks every connected
-- requester of the WHOLE hub; each removal funnels through
-- DroneControl:OnRemoveBuilding (:720-729), which scans the hub's entire
-- drone list per building and kicks every drone en route to that building to
-- Idle — aborting the trip and releasing its request claim. One extender
-- power flicker (dust storm, battery brownout, malfunction, repair, manual
-- toggle) therefore idles the far fleet mid-task twice and burns
-- O(buildings × drones) bookkeeping per edge. Full trace: F77 in docs/BUGS.md.
--
-- Patch approach: a chained wrapper (FIX_POLICY §1.4) on
-- DroneHubExtenderBase:UpdateUplinkRequesters that DEBOUNCES the rebuild: the
-- reconnect is deferred ~2s of game time and coalesced per ROOT hub, so a
-- flap (off→on within the window, or several extenders reacting to the same
-- grid event) costs ONE rebuild instead of two-per-extender. The extender's
-- working/linked state is read at fire time by ConnectTaskRequesters itself,
-- so the deferred rebuild always lands on the CURRENT topology. Uplink chains
-- (extender → extender → hub) resolve to the root hub, exactly like the
-- shipped delegation (DroneHubExtenderBase:ConnectTaskRequesters recurses to
-- the uplink).
--
-- Accepted trade-off (documented on the F77 entry): during the debounce
-- window the hub's registration is stale by up to ~2s — extender-only
-- buildings stay registered while the extender is down, or connect ~2s late.
-- Benign next to the churn; nothing else in the shipped flow is synchronous
-- about this either (SetWorkRadius already defers its reconnect via
-- DelayedCall(300), DroneControl.lua:776).
--
-- Savegame note: the debounce thread is a mod game-time thread — those are
-- NOT persisted across save/load (F06 precedent: "the thread from before the
-- save is gone"). A save landing inside the window simply keeps the pre-flap
-- registration, which is exactly what that save's state describes; the next
-- extender event after load reconnects normally. No persisted state, no
-- object flags (FIX_POLICY §3).

local DEBOUNCE = 2000 -- game-ms; flaps within this window coalesce into one rebuild

local weak_keys = rawget(_G, "weak_keys_meta") or { __mode = "k" }
local pending = setmetatable({}, weak_keys) -- root hub -> debounce thread

-- extender chains resolve to the hub at the top, like the shipped delegation
local function root_hub(node)
	local guard = 0
	while IsValid(node) and IsKindOf(node, "DroneHubExtenderBase") and guard < 16 do
		node = node.uplink
		guard = guard + 1
	end
	return (IsValid(node) and IsKindOf(node, "DroneHubBase")) and node or nil
end

local install_error
do
	local E = rawget(_G, "DroneHubExtenderBase")
	if type(E) ~= "table" or type(E.UpdateUplinkRequesters) ~= "function" then
		install_error = "DroneHubExtenderBase.UpdateUplinkRequesters not found (game update changed it?)"
	end
end

if not install_error then
	local E = DroneHubExtenderBase
	local orig = E.UpdateUplinkRequesters
	function E:UpdateUplinkRequesters()
		if not SMRFixPack.IsActive("ExtenderFlapChurn") then
			return orig(self)
		end
		-- FIX (F77): defer + coalesce the whole-hub rebuild instead of running
		-- it synchronously on every working edge.
		local hub = root_hub(self.uplink)
		if not hub then return end -- orig no-ops without a valid uplink too
		if IsValidThread(pending[hub]) then return end -- a rebuild is already scheduled
		pending[hub] = CreateGameTimeThread(function(hub)
			Sleep(DEBOUNCE)
			pending[hub] = nil
			if IsValid(hub) and hub.can_control_drones then
				hub:DisconnectTaskRequesters()
				hub:ConnectTaskRequesters()
			end
		end, hub)
	end
end

SMRFixPack.Register("ExtenderFlapChurn", {
	title = "Extender power flickers no longer tear down and rebuild the whole hub (fleet-wide Idle churn)",
	apply = function()
		return install_error
	end,
})
