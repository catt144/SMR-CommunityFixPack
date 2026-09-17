-- SRC: Lua/Units/Colonist.lua Colonist:OnDisappear sha256=0efb0f0ced12220f91eb590c0da21974cca12cdbc5395c012f00fca1ed04dc9b
-- SRC: Lua/Buildings/Community.lua Community:HasLifeSupport sha256=8dbb874075708e91e66b2ca14bfe17600cb9ba3b96035616149f7381975d200a
-- SRC: Lua/Buildings/Dome.lua IsInWalkingDist sha256=8a3a2917e78a237adb82ae4488e3da740984b4061ef3e27c84b2ed04b160299d
-- SRC: Lua/Units/ColonistTransport.lua GetTransportRoute sha256=fb3e9f23a793560292e42d51c10f99c86a0287f8dea0f9da49d40be5c29a2306
-- SRC: Lua/Buildings/Residence.lua Residence:IsSuitable sha256=2cc6e521204146d7cd3c041c55415ca1f5482fcc32e35f5e0846f6038ff22a06
-- SRC: Lua/Units/Colonist.lua Colonist:GetExpeditionReturnDome sha256=a62a04b7b2b23029783b61be38e5b30abfc02565ec5129692fc5b7518ac7b481
-- DEFECT: table\.find\(domes,\s*dome\)
-- SRC: Lua/Units/Colonist.lua Colonist:SetDome sha256=e6dcc07718abeb15d385c5dd886ec295933ac90a21e664c8ea019fdfd210d011
-- DEFECT: self:UpdateWorkplace\(\)
-- SRC: Lua/Units/Colonist.lua Colonist:UpdateWorkplace sha256=92900189eb622c380841de4e68b1720a01cacf9ca3d5e329110b649dbe4bb5cf
-- SRC: Lua/Units/Colonist.lua Colonist:UpdateResidence sha256=3b4ecda34cdcd007c4d4e5fd3036a3ce560e8bd8164f45320c20bd4aa61d055a
-- SRC: Lua/Units/Colonist.lua Colonist:SetResidence sha256=4500a90c082362252f30449b5a6d92cccfda04f0a56d8eed8469ff8029159091
-- SRC: Lua/Buildings/MicroGHabitat.lua MicroGHabitatBase:CanVisit sha256=8da2814c32997ab6b978fc754b0d11a500e55b3f86644c14f71baa6698382022
-- SRC: Lua/Buildings/Residence.lua Residence:CanReserveResidence sha256=31822e8edc22576660ee764fbfc703a190de5a7a2f893562e481aef06b79cb6b
-- SRC: Lua/Buildings/Residence.lua Residence:CancelResidenceReservation sha256=88050cc8148158ae6031b863f5cf98b21159960273b550242a1c40c3f3444c56
-- SRC: Lua/Units/ColonistTransport.lua Colonist:ReturnFromExpedition_TransportDestination sha256=2582e2b51fee17f5c6c6da3c0efbdbbdf8a83d930efe4749aa5c6048dd34f94d
-- SRC: Lua/Units/ColonistTransport.lua Colonist:SetCommand sha256=0c7464684c1a6cbde17aa0eee4e8f99cff5e6da7cb6118f4aeee578958ffe441
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:UnloadPassengers sha256=6e2e8553aa69322dae5a2b517669236bb9fe9daed8e9c8ad15b4a030ef55cd51
-- SRC: Lua/Buildings/RocketBase.lua RocketBase:Disembark sha256=47e85e84d3b0cdeddd937fa4210d9f1862ea3d9256ba02f868b43fcab8e71758
-- C95: admit the returning colonist's own held habitat before fallback housing
-- can erase it, then run native housing before native employment on rejoin.
-- Layer 3: all wrapped calls are synchronous; no persisted state, threads,
-- callbacks on objects or copied command bodies. Native travel owns the journey.
-- The same CanReturnHome predicate gates the automatic draft at its rocket.
-- Walking or a verified same-map train route only; departure is not a promise
-- that the landing site or route will still exist when the expedition returns.
-- The v11 exclusion is preserved, append-only, at:
-- docs/archive/code/Fix_HabitatExpeditionDraft.v11-4ec3e32.lua.txt
-- Source dependencies pinned above on game 1.1.0.403908, Steam 24995074.
-- The missing per-colonist admission is watched for body drift, not every
-- possible upstream correction of the absence (FIX_POLICY section 2b).

local installed = false

local function can_return_home(unit, home, origin)
	if not IsKindOf(home, "MicroGHabitatBase") then return false end
	if not IsValid(home) or not IsValid(origin) or not IsSameMap(origin, home)
		or not home.ui_working or not home.accept_colonists or not home:HasLifeSupport()
		or not home:CanVisit(unit) then
		return false
	end
	-- At draft time their bed is occupied, not reserved yet. Boarding releases
	-- that occupancy and vanilla OnDisappear reserves the same bed. Do not ask
	-- a full habitat for a second free slot for its own resident.
	local owns_bed = unit.residence == home and table.find(home.colonists, unit)
	if not (owns_bed and home:IsSuitable(unit) or home:CanReserveResidence(unit)) then
		return false
	end
	if IsInWalkingDist(home, origin:GetPos(), unit.city) then return true end
	local first, last = GetTransportRoute(origin, home, true, false)
	return not not (first and last)
end

SMRFixPack.Register("HabitatExpeditionReturn", {
	title = "Expedition crews return to their reserved habitats",
	apply = function()
		if installed then return end
		local err = SMRFixPack.Require("HabitatExpeditionReturn", {
			{ class = "Colonist", method = "GetExpeditionReturnDome" },
			{ class = "Colonist", method = "UpdateWorkplace" },
			{ class = "Colonist", method = "UpdateResidence" },
			{ class = "Colonist", method = "ReturnFromExpedition_TransportDestination" },
			{ class = "MicroGHabitatBase", method = "CanVisit" },
			{ class = "Residence", method = "CanReserveResidence" },
			{ class = "Residence", method = "IsSuitable" },
			{ class = "Community", method = "HasLifeSupport" },
			{ global = "IsValid" }, { global = "IsKindOf" },
			{ global = "IsSameMap" }, { global = "IsInWalkingDist" },
			{ global = "GetTransportRoute" },
			{ path = { "table", "find" }, kind = "function" },
		})
		if err then return err end
		local original = Colonist.GetExpeditionReturnDome
		function Colonist:GetExpeditionReturnDome(domes, ...)
			local home = self.expedition_residence
			if not IsKindOf(home, "MicroGHabitatBase") then
				return original(self, domes, ...)
			end
			if self.reserved_residence == home and not table.find(domes, home)
				and can_return_home(self, home, self.appear_location or self.holder) then
				local extended = {}
				for i, candidate in ipairs(domes) do extended[i] = candidate end
				extended[#extended + 1] = home
				return original(self, extended, ...)
			end
			return original(self, domes, ...)
		end
		local original_work = Colonist.UpdateWorkplace
		function Colonist:UpdateWorkplace(...)
			local home = self.reserved_residence
			if IsKindOf(home, "MicroGHabitatBase") and IsValid(home)
				and self.dome == home and not IsValid(self.residence) then
				self:UpdateResidence()
			end
			return original_work(self, ...)
		end
		SMRFixPack.HabitatExpeditionReturn = { CanReturnHome = can_return_home }
		installed = true
	end,
})
