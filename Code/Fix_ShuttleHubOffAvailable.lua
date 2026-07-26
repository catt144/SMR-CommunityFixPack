-- F54: Shuttle Hubs the player switched off still count as available transport.
--
-- Defect: IsLRTransportAvailable (Lua\Buildings\ShuttleHub.lua:350-359) answers
-- "can this colony move colonists by shuttle?" with
--     hub.working or hub:GetWorkNotPermittedReason() and not hub:GetWorkNotPossibleReason()
-- The second clause is meant to tolerate a hub that is only suspended for a
-- permission reason while being physically capable. But the commonest
-- permission reason by far is the player's own on/off switch:
-- BaseBuilding:GetWorkNotPermittedReason returns "TurnedOff" whenever
-- `ui_working` is false (BaseBuilding.lua:355-361). So switching every hub off —
-- routine late-game power saving — leaves the colony still believing shuttles
-- are available.
--
-- Nothing ever dispatches one: SendOutShuttles is reached only from
-- ShuttleHubBase:BuildingUpdate under `if self.working` (:1622-1630) and from
-- CargoShuttle:LaunchDstr under `if hub.working` (:509-513). Meanwhile the
-- verdict is consumed by the emigration and transport-request paths
-- (Colonist.lua:1569, :2650, :2759, :2783, :2832) and by dome walkability
-- (Dome.lua:256-259), so colonists queue on pickup spots outside for shuttles
-- that will never come, and passage routes are discounted for a shuttle service
-- that does not exist.
--
-- The other states the second clause admits are genuinely self-lifting and are
-- deliberately kept: `exceptional_circumstances` (BaseBuilding.lua:359) and
-- `exceptional_circumstances_maintenance` (RequiresMaintenance.lua:129-133) are
-- set and cleared by the game itself, not by the player. ("DomeNotWorking",
-- Building.lua:591-596, is the other player toggle in that family but cannot
-- apply here: a Shuttle Hub is an outside building and has no parent dome.)
--
-- Patch approach: full replacement of the global IsLRTransportAvailable — a copy
-- of Lua\Buildings\ShuttleHub.lua:350-359 (shipped Src, game 1.0.7.396349) with one added
-- term, marked -- FIX. Replacement rather than a wrapper because the repair makes
-- the predicate STRICTER: the shipped function returns a single boolean for the
-- whole colony, so a wrapper that sees `true` cannot tell which hub produced it.

SMRFixPack.Register("ShuttleHubOffAvailable", {
	title = "Shuttle Hubs switched off no longer count as available colonist transport",
	apply = function()
		if type(rawget(_G, "IsLRTransportAvailable")) ~= "function" then
			return "IsLRTransportAvailable not found (game update changed it?)"
		end
		-- NB: mod code loads before the classes are flattened, so look these up on
		-- the class that DECLARES them, not on ShuttleHubBase.
		local B = rawget(_G, "BaseBuilding")
		if type(B) ~= "table" or type(B.GetWorkNotPermittedReason) ~= "function"
				or type(B.GetWorkNotPossibleReason) ~= "function" then
			return "BaseBuilding work-reason methods not found (game update changed them?)"
		end

		function IsLRTransportAvailable(city)
			for _, hub in ipairs((city or MainCity).labels.ShuttleHub or empty_table) do
				if #hub.shuttle_infos > 0
				-- FIX (F54): `hub.ui_working` added. A hub the player switched off
				-- reports a work-not-permitted reason with nothing physically wrong,
				-- so it used to pass this test — while never sending a shuttle out.
				and (hub.working or hub.ui_working and hub:GetWorkNotPermittedReason() and not hub:GetWorkNotPossibleReason())
				and (hub.transport_mode == "all" or hub.transport_mode == "people") then
					return true
				end
			end
			return false
		end
	end,
})
