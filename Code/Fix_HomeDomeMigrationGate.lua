-- F61: Turning OFF "accept colonists" on a dome silently stops its own residents
-- from shopping, working and training in the domes next door.
--
-- Defect: `accept_colonists` is the dome's MIGRATION policy — whether outsiders may
-- move IN. Four cross-dome lookups nevertheless require it of the colonist's HOME
-- dome before they will even look through a passage:
--     Dome:GetService            (Lua\Buildings\Dome.lua:2900, 2927)
--     Dome:ChooseTraining        (:2947)
--     Dome:ChooseWorkplace       (:2959)
--     ShiftsBuilding:CanWorkTrainHereDomeCheck (ShiftsBuilding.lua:242-264)
-- all read `self.allow_service_in_connected/allow_work_in_connected and
-- self.accept_colonists`. The destination side is checked separately and correctly
-- by Dome:CanColonistsFromDifferentDomesWorkServiceTrainHere (Dome.lua:2880-2882),
-- which already includes the target's own accept_colonists.
--
-- Proof that the home-side test is spurious: the sibling question
-- Dome:HasFreeWorkplacesAround (:2966-2972) walks the very same connected
-- workplaces with only `allow_work_in_connected` — so the game tells the player
-- there are jobs next door and then refuses to assign them.
--
-- Player impact: closing migration on a residential dome — a routine thing to do
-- once it is full — quietly cuts its residents off from every shop, workplace and
-- school reachable through the passages. Best match for the "colonists refuse to
-- shop through a passage" reports. The `allow_service_in_connected` /
-- `allow_work_in_connected` toggles, which ARE the player's control over this
-- behaviour, keep working exactly as before.
--
-- Patch approach: replacement of the four methods — copies of the shipped bodies
-- (Dome.lua:2899-2941, 2945-2955, 2957-2965 and ShiftsBuilding.lua:242-264,
-- shipped Src 2026-07) with the home-side `accept_colonists` term removed. The
-- file-local GetMaxComfortAvailableServiceInDome is recreated verbatim.
-- Changes marked -- FIX.

SMRFixPack.Register("HomeDomeMigrationGate", {
	title = 'Turning off "accept colonists" no longer blocks a dome\'s own residents from using nearby domes',
	apply = function()
		local D = rawget(_G, "Dome")
		if type(D) ~= "table" then
			return "Dome class not found (game update changed it?)"
		end
		for _, name in ipairs{ "GetService", "ChooseTraining", "ChooseWorkplace",
				"CanColonistsFromDifferentDomesWorkServiceTrainHere", "GetConnectedDomes", "GetClosestFoodPile" } do
			if type(D[name]) ~= "function" then
				return "Dome." .. name .. " not found (game update changed it?)"
			end
		end
		local SB = rawget(_G, "ShiftsBuilding")
		if type(SB) ~= "table" or type(SB.CanWorkTrainHereDomeCheck) ~= "function" then
			return "ShiftsBuilding.CanWorkTrainHereDomeCheck not found (game update changed it?)"
		end
		if type(rawget(_G, "GetMaxComfortAvailableService")) ~= "function"
				or type(rawget(_G, "ChooseTraining")) ~= "function"
				or type(rawget(_G, "ChooseWorkplace")) ~= "function" then
			return "cross-dome service/work helpers not found (game update changed them?)"
		end

		local function GetMaxComfortAvailableServiceInDome(dome, need, colonist)
			local services = dome.labels[need] or empty_table
			return GetMaxComfortAvailableService(services, colonist)
		end

		function D:GetService(need, colonist, starving)
			local max_comfort_service, fail = GetMaxComfortAvailableServiceInDome(self, need, colonist)

			-- FIX (F61): dropped `and self.accept_colonists` — that is the home dome's
			-- migration policy, not a permission to leave through a passage.
			if not max_comfort_service and self.allow_service_in_connected then
				--try domes connected with passages.
				local dome_service_fail = ServiceFailure.NotTried
				for dome in pairs(self:GetConnectedDomes()) do
					if dome:CanColonistsFromDifferentDomesWorkServiceTrainHere() then --quarantine
						max_comfort_service, dome_service_fail = GetMaxComfortAvailableServiceInDome(dome, need, colonist)
						if max_comfort_service then
							return max_comfort_service, dome_service_fail
						else
							fail = Max(fail, dome_service_fail)
						end
					end
				end
			end

			if max_comfort_service then
				return max_comfort_service, fail
			end

			if need ~= "needFood" or not starving then
				return false, fail
			end

			local minpile = self:GetClosestFoodPile(colonist)
			if not minpile and self.allow_service_in_connected then -- FIX (F61): same term dropped
				for dome in pairs(self:GetConnectedDomes()) do
					if dome:CanColonistsFromDifferentDomesWorkServiceTrainHere() then --foreachconnecteddome?
						minpile = dome:GetClosestFoodPile(colonist)
						if minpile then
							break
						end
					end
				end
			end

			if minpile then
				return minpile, ServiceFailure.None
			end

			return false, fail
		end

		function D:ChooseTraining(colonist)
			local workplace, shift = Workforce.ChooseTraining(self, colonist)
			if not workplace and self.allow_work_in_connected then -- FIX (F61): same term dropped
				for dome in pairs(self:GetConnectedDomes()) do
					if dome:CanColonistsFromDifferentDomesWorkServiceTrainHere() then
						workplace, shift = ChooseTraining(colonist, dome.labels.TrainingBuilding, workplace, shift)
					end
				end
			end
			return workplace, shift
		end

		function D:ChooseWorkplace(colonist)
			local list = self.labels.Workplace
			if self.allow_work_in_connected then -- FIX (F61): same term dropped
				list = self:GetCommutableWorkplaces(colonist, "work")
			end

			local work_bld, work_shift, work_to_kick = ChooseWorkplace(colonist, list, true)
			return work_bld, work_shift, work_to_kick
		end

		function SB:CanWorkTrainHereDomeCheck(colonist)
			local his_dome = colonist.dome
			if not his_dome then return false end
			local my_dome = self.parent_dome
			if not my_dome then
				--checking outside bld would be way 2 hvy, just assume it's fine, generally colo cant see this bld if his dome isn't connected
				my_dome = his_dome
			end
			local can_work = (his_dome == my_dome
						or (his_dome.allow_work_in_connected -- FIX (F61): dropped `and his_dome.accept_colonists`
							and AreDomesConnected(his_dome, my_dome)
							and my_dome:CanColonistsFromDifferentDomesWorkServiceTrainHere()
						))

			if can_work then
				return true
			end
			local his_dome = colonist.dome
			if not his_dome then
				return false
			end
			--check dome, not position
			return GetTransportRoute(his_dome, self)
		end
	end,
})
