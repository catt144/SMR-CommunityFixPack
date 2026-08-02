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
-- Patch approach: FIX_POLICY §1.4b chained POST-wrapper on the global, as a
-- FILTER. The repair only ever makes the predicate STRICTER, so a `false` from
-- the shipped body is already the right answer and is returned untouched; only
-- a `true` is re-validated against the stricter per-hub test.
-- Layer: §3a layer 2 — a synchronous predicate, nothing left to run after.
--
-- CONVERTED 2026-08-02 from a §1.5 full replacement (SAVE_SAFETY_REDESIGN §5.4
-- group A). Before/after: the module no longer OVERRIDES vanilla's verdict — it
-- can only narrow it. Behaviour is unchanged, because the strict per-hub test is
-- a subset of the shipped one (it is the shipped one AND `hub.working or
-- hub.ui_working`), so "some hub passes strict" implies "some hub passes loose":
-- `orig(city) and <strict scan>` selects exactly what the old copy's `<strict
-- scan>` selected. What the delegation buys is the §1.4b degradation property —
-- if a future patch tightens this predicate further, or a DLC adds a term, we
-- inherit it instead of silently reinstating the 1.0.7 shape.
-- ⚠️ Honest limit: the stricter scan is still a loop over the same label, so the
-- shipped loop is duplicated rather than eliminated. A wrapper cannot filter the
-- `true` on its own — the shipped function returns ONE boolean for the whole
-- colony and never says which hub produced it — so the predicate has to be owned.
-- The rot exposure is therefore reduced (we can never be LOOSER than a patched
-- vanilla), not removed.

SMRFixPack.Register("ShuttleHubOffAvailable", {
	title = "Shuttle Hubs switched off no longer count as available colonist transport",
	apply = function()
		-- NB: the work-reason methods are checked on the class that DECLARES
		-- them (BaseBuilding), not on ShuttleHubBase — mod code loads before the
		-- classes are flattened.
		local err = SMRFixPack.Require("ShuttleHubOffAvailable", {
			{ global = "IsLRTransportAvailable" },
			{ class = "BaseBuilding", method = "GetWorkNotPermittedReason",
			  reason = "BaseBuilding work-reason methods not found (game update changed them?)" },
			{ class = "BaseBuilding", method = "GetWorkNotPossibleReason",
			  reason = "BaseBuilding work-reason methods not found (game update changed them?)" },
		})
		if err then return err end
		local orig = IsLRTransportAvailable

		return SMRFixPack.SetGlobal("IsLRTransportAvailable", function(city)
			-- vanilla is never too strict, only too lax: a `false` needs no review
			if not orig(city) then return false end
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
		end, "could not install the IsLRTransportAvailable wrapper")
	end,
})
