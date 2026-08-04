-- F11: A train parks at a platform and never leaves again, blocking the line.
--
-- Defect: Colonist:ExitVehicle (Lua\Units\ColonistTransport.lua:540-571) has a
-- guard for a passenger that is no longer aboard (the dev comment blames a
-- CargoTransporter abducting them). The guard tries to drop the passenger from the
-- train's list with
--     table.remove(vehicle.units, self)
-- but table.remove takes an integer POSITION, not a value — the intended API is
-- table.remove_entry, which the engine uses for this very list in
-- Holder:OnExitHolder (Holder.lua:37). The call raises, which aborts ExitVehicle
-- before DiscardTransportTicket runs, so the colonist is still listed as a
-- passenger. Train:UnloadTrain (Units\Train.lua:443-453) then spins waiting for a
-- passenger who can never disembark and the train occupies the platform for good.
--
-- Patch approach: PRE-wrapper (FIX_POLICY §1.4; converted 2026-08-03 from a §1.5
-- full copy by the f11-f99-review chain). Re-state the shipped guard condition;
-- when it fires, run the repaired branch (byte-identical to shipped :542-546
-- except the FIX line) and return; otherwise tail-call the captured original,
-- which re-evaluates the same condition — three pure reads with no yield between
-- the two evaluations — and takes the untouched shipped path. This un-freezes
-- the ~23 copied lines the old form pinned to 1.0.7.396349, including two live
-- tuning expressions (the LuxuriousTrains comfort penalty and the GreenView
-- sanity bonus) and a recreated file-local (stat_scale) that no Require check
-- could see.
--
-- ⚠️ MUST stay a PRE-wrapper (agent/facts/EF-012): ExitVehicle is a command
-- method — its only shipped call site is colonist:SetCommand("ExitVehicle", self)
-- (Train.lua:447) and its normal path ends in a destructor-tail SetCommand,
-- which never returns. A post-wrapper here would be silently dead.
--
-- Apply-once: safe by construction — the entry is not `optional`, so 00_Core's
-- Mod Options reconciliation never re-runs apply; Register applies once per Lua
-- load, and a Lua reload rebuilds the shipped method before mod code recaptures.
--
-- ⛔ Verification owed (2026-08-03): behaviour-preserving BY CONSTRUCTION only —
-- this shape earns `tested` from a probe-suite run or a keyboard leg, and
-- neither has run on it. Change marked -- FIX.

SMRFixPack.Register("TrainPlatformWedge", {
	title = "A stale passenger no longer wedges a train at the platform forever",
	apply = function()
		local err = SMRFixPack.Require("TrainPlatformWedge", {
			{ class = "Colonist", method = "ExitVehicle" },
			{ path = { "table", "remove_entry" }, kind = "function" },
			{ global = "IsSameMap" },
		})
		if err then return err end
		local orig = Colonist.ExitVehicle

		function Colonist:ExitVehicle(vehicle)
			if not self.holder or self.holder ~= vehicle or not IsSameMap(self, vehicle) then
				--abducted by CargoTransporter?
				TrainsLogging.warn(self, "not in train", self.command)
				table.remove_entry(vehicle.units, self) -- FIX (F11): was table.remove(list, value), which raises
				self:DiscardTransportTicket()
				return
			end
			return orig(self, vehicle)
		end
	end,
})
