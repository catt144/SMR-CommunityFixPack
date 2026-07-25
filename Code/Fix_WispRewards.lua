-- F07 + F15: St. Elmo's Fire (Mystery 11) light trap fixes.
--
-- F07: choosing "free the wisps" (Symbiotic coexistence) gives ~1/1000 power.
--   SetLightTrapMode's "free" branch (Lua\Mysteries\Fireflies.lua:692) calls
--   trap.el_prod_modifier:Change(#trap.fireflies) — missing the `* 1000` that both
--   sibling call sites of the same modifier use (Fireflies.lua:346 and :479).
--   3 wisps = 3 internal power units (a Solar Panel is 2000) — effectively zero.
--
-- F15: wisp research rewards are inconsistent in "destroy" mode.
--   Each wisp's Die destructor grants +100 RP (Fireflies.lua:540-542; the grant
--   written after SetCommand("Die") in Firefly:Drain at :466-469 is unreachable —
--   DoSetCommand kills the calling thread). The batch "destroy" branch of
--   SetLightTrapMode ALSO granted reward = wisps*100 → trapped wisps paid 200 RP
--   each while the notification claimed 100.
--
-- Patch approach: both defects live in the same small global function, so this
-- file replaces SetLightTrapMode once (copy of Fireflies.lua:674-701, shipped Src
-- 2026-07). Changes marked -- FIX. The destructor's +100 (the consistent payer for
-- wisps caught later) is kept as the single source of RP; the batch branch keeps
-- its notification so the player still sees the total.

SMRFixPack.Register("WispRewards", {
	title = 'Mystery 11: "free the wisps" produces real power; destroyed-wisp rewards match the notification',
	apply = function()
		if type(SetLightTrapMode) ~= "function" then
			return "SetLightTrapMode not found (game update changed it?)"
		end

		function SetLightTrapMode(mode)
			UIColony.mystery.lighttrap_mode = mode
			if UIColony.mystery.lighttrap_mode == "destroy" then
				local reward = 0
				for _, trap in ipairs(MainCity.labels.LightTrap) do
					reward = reward + #trap.fireflies * 100
					for i = #trap.fireflies, 1, -1 do
						trap.fireflies[i]:SetCommand("Die")
					end
					trap:SetWorkState("work_empty")
				end
				if reward > 0 then
					AddUniqueNotification("Mystery11WispsKilled", {points = reward})
					-- FIX (F15): no direct AddResearchPoints here — each wisp's Die
					-- destructor already grants 100 RP; the shipped double-grant paid
					-- 200/wisp while the notification said 100.
				end
			elseif UIColony.mystery.lighttrap_mode == "free" then
				for _, trap in ipairs(MainCity.labels.LightTrap) do
					trap:UpdateAttachedSigns()
					trap.el_prod_modifier:Change(#trap.fireflies * 1000) -- FIX (F07): missing * 1000 (compare Fireflies.lua:346, :479)
					if #trap.fireflies > 0 then
						PlayFX("MakeElectricity", "start", trap)
					end
					for _, firefly in ipairs(trap.fireflies) do
						PlayFX("MakeElectricity", "start", firefly)
					end
				end
			end
		end
	end,
})
