-- SRC: Lua/Units/Colonist.lua Colonist:OnDisappear sha256=0efb0f0ced12220f91eb590c0da21974cca12cdbc5395c012f00fca1ed04dc9b
-- SRC: Lua/Buildings/Community.lua Community:HasLifeSupport sha256=8dbb874075708e91e66b2ca14bfe17600cb9ba3b96035616149f7381975d200a
-- SRC: Lua/Buildings/Dome.lua IsInWalkingDist sha256=8a3a2917e78a237adb82ae4488e3da740984b4061ef3e27c84b2ed04b160299d
-- SRC: Lua/Buildings/Residence.lua Residence:IsSuitable sha256=2cc6e521204146d7cd3c041c55415ca1f5482fcc32e35f5e0846f6038ff22a06
-- SRC: Lua/Units/Colonist.lua Colonist:GetExpeditionReturnDome sha256=a62a04b7b2b23029783b61be38e5b30abfc02565ec5129692fc5b7518ac7b481
-- DEFECT: table\.find\(domes,\s*dome\)
-- SRC: Lua/Units/Colonist.lua Colonist:ReturnFromExpedition sha256=0b1d6d559e731343f9251b9b746e4d1f0a12307478584e67b3eb86856cd6dad4
-- DEFECT: self:SetCommand\("TransportByFoot",\s*dome\)
-- SRC: Lua/Units/Colonist.lua Colonist:TransportByFoot sha256=2ce92eff11f4b642aba8c08cf80d9325e9fcab850202ed85cd90efdecc4c4060
-- SRC: Lua/Units/ColonistTransport.lua Colonist:EnterBuilding sha256=58a920dc90e767259db6fd40ff4d38a89c744392ba118087de4580856988e48d
-- SRC: Lua/Units/Unit.lua Unit:EnterBuilding sha256=7e309a98e05166d3f8c54cc6318dbd0346baa5085ccebd2f193f4adddbdf18d7
-- SRC: Lua/Buildings/BuildingWayPoints.lua WaypointsObj:GetEntrancePoints sha256=14ecc0848a2fcc57fd0159518922c9806d84a98987ce8eaee2b3bde16359df99
-- SRC: Lua/Units/Colonist.lua Colonist:SetDome sha256=e6dcc07718abeb15d385c5dd886ec295933ac90a21e664c8ea019fdfd210d011
-- DEFECT: self:UpdateWorkplace\(\)
-- SRC: Lua/Units/Colonist.lua Colonist:UpdateWorkplace sha256=92900189eb622c380841de4e68b1720a01cacf9ca3d5e329110b649dbe4bb5cf
-- SRC: Lua/Units/Colonist.lua Colonist:UpdateResidence sha256=3b4ecda34cdcd007c4d4e5fd3036a3ce560e8bd8164f45320c20bd4aa61d055a
-- SRC: Lua/Units/Colonist.lua Colonist:SetResidence sha256=4500a90c082362252f30449b5a6d92cccfda04f0a56d8eed8469ff8029159091
-- SRC: Lua/Buildings/MicroGHabitat.lua MicroGHabitatBase:CanVisit sha256=8da2814c32997ab6b978fc754b0d11a500e55b3f86644c14f71baa6698382022
-- SRC: Lua/Buildings/Residence.lua Residence:ReserveResidence sha256=88018693261f64a17dbb085803ae0436558443ea2e20f0ea0559db5ce5b8e388
-- SRC: Lua/Buildings/Residence.lua Residence:CanReserveResidence sha256=31822e8edc22576660ee764fbfc703a190de5a7a2f893562e481aef06b79cb6b
-- SRC: Lua/Buildings/Residence.lua Residence:CancelResidenceReservation sha256=88050cc8148158ae6031b863f5cf98b21159960273b550242a1c40c3f3444c56
-- SRC: Lua/Units/ColonistTransport.lua Colonist:SetCommand sha256=0c7464684c1a6cbde17aa0eee4e8f99cff5e6da7cb6118f4aeee578958ffe441
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:UnloadPassengers sha256=6e2e8553aa69322dae5a2b517669236bb9fe9daed8e9c8ad15b4a030ef55cd51
-- SRC: Lua/Buildings/RocketBase.lua RocketBase:Disembark sha256=47e85e84d3b0cdeddd937fa4210d9f1862ea3d9256ba02f868b43fcab8e71758
-- C95: an expedition returnee goes back to their held habitat the way they
-- were taken. Boarding attaches a colonist to the rocket wherever they stand
-- (Unit:EnterTransporter); the return makes them walk, so a home outside
-- walking range was never offered and the colonist lost it.
--
-- 1. Selector: a colonist whose expedition_residence is a MicroGHabitatBase,
--    still reserved and usable, has that habitat added to their private
--    candidate list whether or not a route exists, before the receiver's
--    fallback reservation can clear the hold (Residence.lua:290-307, :385-399).
--    When the chosen home is outside walking range of the landing, that one
--    colonist is marked in a weak, in-memory table.
-- 2. Placement: when a marked colonist is issued TransportByFoot to that home
--    (the tail of the native ReturnFromExpedition body), they are set down at
--    the home's own entrance point first. Native EnterBuilding then takes them
--    in, as Unit:EnterBuilding does for a unit with no position. In range, the
--    proven walk is untouched; a native train booking is untouched and its
--    final walk starts in range. Nothing else is ever marked: Earth arrivals,
--    covert-ops recruits and migrants never carry a habitat expedition hold.
-- 3. Rejoin: native UpdateResidence precedes the captured UpdateWorkplace.
--
-- Layer 3: every wrapped call is synchronous; no persisted state, threads,
-- callbacks on objects or copied bodies. The mark is not saved: a save and
-- reload between landing and the walk order (the disembark animation) loses
-- it, and that colonist walks to the still-held home as vanilla would.
-- Same map only: a cross-map home is not admitted and C102's fallback applies.
-- The v11 exclusion is preserved, append-only, at:
-- docs/archive/code/Fix_HabitatExpeditionDraft.v11-4ec3e32.lua.txt
-- Source dependencies pinned above on game 1.1.0.403908, Steam 24995074.
-- The missing per-colonist admission is watched for body drift, not every
-- possible upstream correction of the absence (FIX_POLICY section 2b).

local installed = false
local placing = setmetatable({}, { __mode = "k" })
local error_logged = false

local function home_usable(unit, home, origin)
	return IsValid(home) and IsValid(origin) and IsSameMap(origin, home)
		and home.ui_working and home.accept_colonists and home:HasLifeSupport()
		and home:CanVisit(unit) and home:IsSuitable(unit)
end

local function place_at_door(unit, home)
	if not (IsValid(unit) and unit.reserved_residence == home and not IsValid(unit.holder)
		and unit:IsValidPos() and home_usable(unit, home, unit)
		and not IsInWalkingDist(home, unit:GetPos(), unit.city)) then
		return
	end
	local points = home:GetEntrancePoints(unit.entrance_type or "entrance")
	local pos = type(points) == "table" and points[unit:Random(1, #points)] or points
	if pos then
		unit:SetPos(pos)
		return true
	end
end

local function pack(...)
	return { n = select("#", ...), ... }
end

SMRFixPack.Register("HabitatExpeditionReturn", {
	title = "Expedition crews return to their reserved habitats",
	apply = function()
		if installed then return end
		local err = SMRFixPack.Require("HabitatExpeditionReturn", {
			{ class = "Colonist", method = "GetExpeditionReturnDome" },
			{ class = "Colonist", method = "SetCommand" },
			{ class = "Colonist", method = "UpdateWorkplace" },
			{ class = "Colonist", method = "UpdateResidence" },
			{ class = "MicroGHabitatBase", method = "CanVisit" },
			{ class = "Residence", method = "IsSuitable" },
			{ class = "Community", method = "HasLifeSupport" },
			{ class = "WaypointsObj", method = "GetEntrancePoints" },
			{ global = "IsValid" }, { global = "IsKindOf" },
			{ global = "IsSameMap" }, { global = "IsInWalkingDist" },
			{ path = { "table", "find" }, kind = "function" },
			{ path = { "table", "unpack" }, kind = "function" },
		})
		if err then return err end
		local original = Colonist.GetExpeditionReturnDome
		function Colonist:GetExpeditionReturnDome(domes, ...)
			local home = self.expedition_residence
			if not IsKindOf(home, "MicroGHabitatBase") then
				return original(self, domes, ...)
			end
			placing[self] = nil
			local origin = self.appear_location or self.holder
			if self.reserved_residence ~= home or table.find(domes, home)
				or not home_usable(self, home, origin) then
				return original(self, domes, ...)
			end
			local extended = {}
			for i, candidate in ipairs(domes) do extended[i] = candidate end
			extended[#extended + 1] = home
			local result = pack(original(self, extended, ...))
			if result[1] == home and not IsInWalkingDist(home, origin:GetPos(), self.city) then
				placing[self] = home
			end
			return table.unpack(result, 1, result.n)
		end
		local original_command = Colonist.SetCommand
		function Colonist:SetCommand(command, dest, ...)
			local home = placing[self]
			if home and command == "TransportByFoot" then
				placing[self] = nil
				if dest == home and not pcall(place_at_door, self, home) and not error_logged then
					error_logged = true
					SMRFixPack.Log("HabitatExpeditionReturn: placement failed; the returnee walks")
				end
			end
			return original_command(self, command, dest, ...)
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
		installed = true
	end,
})
