-- F38: Destroyed tunnels rejoin the pathfinding graph after a save/load.
--
-- Defect: the destruction path is correct — TunnelBase:OnDestroyed
-- (Lua\Buildings\Tunnel.lua:153-158) calls RemovePFTunnel, and TunnelBase:Destroy
-- (:33-38) takes the linked half down with it, so both directions go away.
--
-- Loading a save undoes all of it:
--     function OnMsg.LoadGame()
--         AllMapsForEach("map", "TunnelBase", Tunnel.AddPFTunnel)
--     end                                            -- Tunnel.lua:264-266
-- Every TunnelBase gets its pathfinding tunnel back with no `destroyed` test, and
-- TunnelBase:AddPFTunnel (:197-209) only checks IsValid(self.linked_obj) — a
-- destroyed building is a valid object (it is a ruin, Building.lua:1473), so the
-- ruin registers a working shortcut. TunnelBase:TraverseTunnel (:215-262) tests
-- IsValid too and likewise waves it through, so rovers and colonists route through
-- a tunnel that visibly no longer exists until it is repaired or bulldozed.
--
-- Patch approach: chained pre-wrapper on TunnelBase:AddPFTunnel — one hook covers
-- the LoadGame sweep and any other caller, present or future. Wrapping the
-- declaring class is what makes it reach `Tunnel.AddPFTunnel`: mod code runs
-- before the classes are flattened, so a method written onto TunnelBase is the
-- one every subclass inherits (and the shipped handler looks the function up on
-- Tunnel at the moment it runs, not when it was registered).
--
-- Repairing a destroyed tunnel is unaffected: Building:Rebuild (Building.lua:1655)
-- places a construction site and the finished tunnel is a NEW object whose
-- GameInit re-registers normally (Tunnel.lua:77-90).
--
-- The LoadGame sweep below is belt-and-braces for saves where something else has
-- already registered a ruin's tunnel.

SMRFixPack.Register("DestroyedTunnels", {
	title = "Destroyed tunnels stay closed after loading a save instead of rejoining pathfinding",
	apply = function()
		local err = SMRFixPack.Require("DestroyedTunnels", {
			{ class = "TunnelBase", method = "AddPFTunnel",
			  reason = "TunnelBase.AddPFTunnel/RemovePFTunnel not found (game update changed it?)" },
			{ class = "TunnelBase", method = "RemovePFTunnel",
			  reason = "TunnelBase.AddPFTunnel/RemovePFTunnel not found (game update changed it?)" },
		})
		if err then return err end
		local TB = TunnelBase

		local orig = TB.AddPFTunnel
		function TB:AddPFTunnel(...)
			-- FIX (F38): a ruin is still a valid object, so nothing else stops the
			-- LoadGame sweep from giving a destroyed tunnel its shortcut back.
			if self.destroyed or (self.linked_obj and self.linked_obj.destroyed) then
				return
			end
			return orig(self, ...)
		end
	end,
})

-- Runs after the shipped Tunnel.lua handler (OnMsg is additive and ours registers
-- later), so anything it re-added for a ruin is taken back out here.
OnMsg.LoadGame = SMRFixPack.WhenActive("DestroyedTunnels", function()
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end

	local closed = 0
	AllMapsForEach("map", "TunnelBase", function(tunnel)
		if tunnel.destroyed or (tunnel.linked_obj and tunnel.linked_obj.destroyed) then
			tunnel:RemovePFTunnel()
			closed = closed + 1
		end
	end)

	if closed > 0 then
		SMRFixPack.Log("DestroyedTunnels: closed %d destroyed tunnel(s) left open in pathfinding", closed)
	end
end)
