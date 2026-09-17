-- C95: draft habitat residents only when their home is returnable from this
-- rocket. The registered return repair supplies the same admission predicate.
-- v11 archive: docs/archive/code/Fix_HabitatExpeditionDraft.v11-4ec3e32.lua.txt
-- Naturalist and Micro-G habitats both inherit MicroGHabitatBase; residence,
-- not dome or player-toggleable community policies, identifies their residents.
-- See docs/agent/bugs/C95.md and reports/C95_RETURN_HOME_BUILD.md.
--
-- Layer 3 (FIX_POLICY 3a): filter synchronous inputs, retain the shipped picker.
-- No object fields, GameVars, threads, migration or saved callbacks are added.
-- Both shipped gathers and their callees do not yield. On the New path this
-- includes is_colonist_reachable, GetConnectedCities, GetCityLabelWithConnected,
-- IsDead and CanChangeCommand/IsTransported. This is a dependency: a yielding
-- third-party wrapper on either gather/filter would invalidate the swap.
-- RocketExpeditionBase explicitly reads CargoTransporter.GatherAvailableColonists;
-- UniversalRocketBase uses CargoTransporterNew while its RocketType is Expedition.
-- Lander/elevator gathers stay outside the repair. Guard foreign receivers first.
-- Filter BEFORE each bucket's trait selection so later buckets can fill the crew.
-- Filtering the returned crew instead can strand an otherwise fillable expedition.
--
-- Missing residence is a normal non-match, not a predicate error. If evaluation
-- actually throws, preserve that bucket unchanged. If the picker throws, restore
-- first and retry its read-only body with the original filter: retail error()
-- does not unwind, so it cannot rethrow. A vanilla error remains vanilla's error.
--
-- Pin: shipped 1.1.0.403908, build 24995074. The defect is an absent residence
-- exclusion; this expression detects body drift, not a guard added elsewhere.
-- SRC: Lua/Buildings/CargoTransporter.lua CargoTransporter:GatherAvailableColonists sha256=31b4ac46cc788ca1bc29f8539c281d7471f7bc8862430fe887e2421ec796e3d2
-- DEFECT: FilterColonistsByTrait\(pool,\s*label,\s*amount\s*-\s*#list\)
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:GatherAvailableColonists sha256=3b6ce91eaba5a7dddf26ee798cb66d584b7bdcf8e7dad50446babe82fd0e834a
-- DEFECT: FilterColonistsByTrait\(pool,\s*label,\s*amount\s*-\s*#list\)

local installed = false

local function IsAutoPickerExempt(unit, rocket)
	if not IsKindOf(unit.residence, "MicroGHabitatBase") then return false end
	local repair = SMRFixPack.HabitatExpeditionReturn
	return not (SMRFixPack.IsActive("HabitatExpeditionReturn") and repair
		and repair.CanReturnHome(unit, unit.residence, rocket))
end

local function eligible_pool(pool, rocket)
	local eligible = {}
	for _, unit in ipairs(pool) do
		if not IsAutoPickerExempt(unit, rocket) then
			eligible[#eligible + 1] = unit
		end
	end
	return eligible
end

local function pack(...)
	return { n = select("#", ...), ... }
end

local function wrap_gather(orig, is_automatic_expedition)
	return function(self, ...)
		if not is_automatic_expedition(self) then
			return orig(self, ...)
		end
		local filter = FilterColonistsByTrait
		if type(filter) ~= "function" then return orig(self, ...) end
		-- Plain assignment reaches the real global through ModEnvMeta.__newindex.
		-- rawset(_G, ...) would only shadow it in this mod's sandbox.
		FilterColonistsByTrait = function(pool, ...)
			local ok, eligible = pcall(eligible_pool, pool, self)
			return filter(ok and eligible or pool, ...)
		end
		local result = pack(pcall(orig, self, ...))
		FilterColonistsByTrait = filter
		if not result[1] then return orig(self, ...) end
		return table.unpack(result, 2, result.n)
	end
end

SMRFixPack.Register("HabitatExpeditionDraft", {
	title = "Expeditions draft habitat residents when they have a return route home",
	apply = function()
		if installed then return end
		local err = SMRFixPack.Require("HabitatExpeditionDraft", {
			{ class = "MicroGHabitatBase" },
			{ global = "IsKindOf" },
			{ global = "FilterColonistsByTrait" },
			{ path = { "table", "unpack" }, kind = "function" },
		})
		if err then return err end

		local patched, legacy_err, new_err
		if type(CargoTransporter) == "table" then
			legacy_err = SMRFixPack.Require("HabitatExpeditionDraft", {
				{ class = "CargoTransporter", method = "GatherAvailableColonists" },
				{ class = "RocketExpeditionBase" },
			})
			if not legacy_err then
				local orig = CargoTransporter.GatherAvailableColonists
				CargoTransporter.GatherAvailableColonists = wrap_gather(orig, function(self)
					return IsKindOf(self, "RocketExpeditionBase")
				end)
				patched = true
			end
		end

		if type(CargoTransporterNew) == "table" then
			new_err = SMRFixPack.Require("HabitatExpeditionDraft", {
				{ class = "CargoTransporterNew", method = "GatherAvailableColonists" },
				{ class = "UniversalRocketBase" },
				{ path = { "g_RocketTypes", "Expedition" }, kind = "any" },
			})
			if not new_err then
				local orig = CargoTransporterNew.GatherAvailableColonists
				CargoTransporterNew.GatherAvailableColonists = wrap_gather(orig, function(self)
					return IsKindOf(self, "UniversalRocketBase")
						and self.RocketType == g_RocketTypes.Expedition
				end)
				patched = true
			end
		end

		if not patched then
			return legacy_err or new_err or "no supported expedition gather receiver found"
		end
		installed = true
	end,
})
