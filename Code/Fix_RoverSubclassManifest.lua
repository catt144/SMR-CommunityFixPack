-- C96: a rover manifest asks for a class by NAME and matches by exact leaf
-- class, so a rover's own subclass never satisfies a request for its base. The
-- reported case is the RC Seeker (RCSensor, a genuine RCRover subclass) being
-- refused by an anomaly expedition that wants an RC Commander (RCRover); the
-- same refusal hits RCSolar and every other RC subclass relationship.
-- See docs/agent/bugs/C96.md and reports/C96_ROVER_SUBCLASS_BUILD.md.
--
-- Three gates: the source label, the leaf compare, and total cargo availability.
-- Widening the == compare alone changes NOTHING, because
-- BaseRover:AddToCityLabels registers each rover under "Unit", "Rover" and its
-- own LEAF class, and nothing walks __parents (BaseRover.lua:123-127), so
-- city.labels["RCRover"] never held a Seeker to compare against. The SOURCE
-- LIST is the gate that actually excludes it. (C96 cites this as GameInit;
-- GameInit does no label work at all -- the substance is unchanged.)
--
-- ⛔ BOTH RECEIVERS. CargoTransporter is the legacy path; 1.1.0 expeditions run
-- through UniversalRocketBase, which carries CargoTransporterNew and neither
-- legacy class (UniversalRocket.lua:28-42) -- hooking only the legacy one ships
-- an inert module, which is exactly how Fix_HabitatExpeditionDraft failed its
-- sitting (C95). Both implementations carry both gates, identically.
--
-- Layer 3 (FIX_POLICY 3a): filter synchronous inputs, retain the shipped body.
-- The widened listing calls the SHIPPED lister once per descendant class, so
-- vanilla's own availability filter (drones, CanBeControlled, holder, IsIdle)
-- does all the work unchanged and cannot drift from a copy we maintain.
--
-- ⭐ WIDENS ONLY ON SHORTFALL. The gather runs vanilla first and returns its
-- result untouched whenever the request is already satisfiable, so a colony
-- that owns the exact rover keeps vanilla's nearest-first pick and this module
-- is invisible. Widening is attempted only when vanilla came up short, and the
-- result is kept only when it is strictly better. Directional by construction:
-- a subclass satisfies a request for its base, never the reverse, so an anomaly
-- that wants a Seeker still refuses a plain Commander.
--
-- Cargo must record the ACTUAL leaf class. Transfer the fulfilled part of a
-- base request to that leaf, then let AddCargoAmount credit it normally.
-- The old remap credited a Commander amount for a Seeker object; UnloadRovers
-- reads cargo[rover.class] and would then spawn an extra Commander. A native
-- leaf cargo record also unloads correctly without this module installed.
--
-- Layer 3: synchronous wrappers, no new object field, GameVar, thread,
-- migration or saved callback. Standard cargo data records the substituted
-- request and actual loaded rover; it remains native after pack removal.
-- Labels are never changed. The exact-first flag is module-local and cleared
-- before the synchronous gather returns, including its error path.
-- The shipped gather, lister and their callees are synchronous (GetDist2D,
-- table.sortby_field, table.ifilter, label reads).
--
-- Pin: shipped 1.1.0.403908. The defect is the leaf-class compare plus the
-- leaf-label source list; these detect body drift, not a guard added elsewhere.
-- SRC: Lua/Buildings/CargoTransporter.lua CargoTransporter:ListAvailableRovers sha256=86084cb5dd5b104d3347e5e2fd46db3f5fe2c20d709724aeb35cd756d6ee0736
-- DEFECT: unit\.class == class
-- SRC: Lua/Buildings/CargoTransporter.lua CargoTransporter:GatherAvailableRovers sha256=d89cffb926dcd06b8378e6ca94ee360e8c9fb0f39ed18382c485d5520ec6889f
-- DEFECT: ListAvailableRovers\(class, quick_load, no_drones\)
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:ListAvailableRovers sha256=aab440ec23f3011e1adebbb96b8d758461d972e63b390f4994f7604c8d391e41
-- DEFECT: unit\.class == class
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:GatherAvailableRovers sha256=ed24c06a9d1fa615638807bb600344634bf03621e9f2eec85189adb5a0cec9fe
-- DEFECT: ListAvailableRovers\(class, quick_load\)
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:AddCargoAmount sha256=f3e8566f0819e2117a25209ab0408572050c482b9964bb3ffdeebeb47e73fe1d
-- DEFECT: if self\.cargo\[class_id\] then
-- SRC: Lua/Cargo.lua GetTotalCargoAvailable sha256=a7a0e841bacb7323f6098d5fa7699fbc5c8adc67beccaee080b2bd80a71e5226
-- DEFECT: get_city_cargo_available\(city, cargo_type, class\)
-- SRC: Lua/Buildings/CargoTransporter.lua CargoTransporter:GetPayloadWarning sha256=cb0b538947eeb3d3f1fb15617862273b6ee4e88646f35946ecc90af1e6b2ae8d
-- DEFECT: self\.city\.labels\[item\.class\]
-- SRC: Lua/CargoTransporterNew.lua CargoTransporterNew:GetNonResourceCargoWarning sha256=17f6daff4d20871e5d487ceba37608702d0528c44825c2cb147a2e7053f6a030
-- DEFECT: GetCityLabelWithConnected\(self\.city, item_class\)

-- transporter -> the class name currently restricted to exact matches. A rocket
-- that is destroyed mid-gather is collectable, and nothing here is persisted.
local exact_only = setmetatable({}, { __mode = "k" })

local descendant_cache = {}

-- Rover subclasses of `class`, most-derived order irrelevant (the shipped
-- gather re-sorts by distance). Empty for anything that is not a rover class,
-- which is what keeps drone and resource requests untouched.
local function rover_descendants(class)
	local cached = descendant_cache[class]
	if cached then return cached end
	local list = {}
	local def = type(class) == "string" and g_Classes[class]
	if def and IsKindOf(def, "BaseRover") then
		for _, name in ipairs(ClassDescendantsList(class) or {}) do
			local sub = g_Classes[name]
			if sub and IsKindOf(sub, "BaseRover") then
				list[#list + 1] = name
			end
		end
	end
	descendant_cache[class] = list
	return list
end

local function is_rover_class(class)
	local def = type(class) == "string" and g_Classes[class]
	return def and IsKindOf(def, "BaseRover") and true or false
end

-- Does `class` satisfy a request for `wanted`? Directional: descendants only.
local function satisfies(class, wanted)
	if class == wanted then return true end
	local def = type(class) == "string" and g_Classes[class]
	local ancestors = def and def.__ancestors
	return ancestors and ancestors[wanted] and true or false
end

local function append(dest, src)
	if type(src) ~= "table" then return dest end
	for i = 1, #src do
		dest[#dest + 1] = src[i]
	end
	return dest
end

local function install(T)
	-- Mod code loads before class construction. Named class globals are the
	-- definitions; g_Classes is empty or contains the PREVIOUS Lua load's
	-- built tables, which classes.lua clears. Patch the definitions themselves.
	if not T then return end

	local orig_list = T.ListAvailableRovers
	local orig_gather = T.GatherAvailableRovers

	-- UI callers need the same subclass-aware availability as the gather. The
	-- shipped lister is called once per descendant so its availability filter
	-- is reused verbatim and the leaf-class compare is satisfied by passing
	-- each subclass its own name.
	T.ListAvailableRovers = function(self, class, ...)
		local list = orig_list(self, class, ...)
		if exact_only[self] == class then return list end
		local out = {}
		append(out, list)
		for _, sub in ipairs(rover_descendants(class)) do
			append(out, orig_list(self, sub, ...))
		end
		-- Cargo gathers each manifest line separately before boarding anything.
		-- Reserve what a more-specific line will select, or the same Seeker can
		-- be returned for BOTH RCRover and RCSensor. Recursion is strictly down
		-- the ancestry tree; exact-class first passes never enter this branch.
		local reserved = {}
		local quick_load, no_drones = ...
		for wanted, item in pairs(self.cargo or empty_table) do
			if wanted ~= class and satisfies(wanted, class) and (item.requested or 0) > 0 then
				for _, unit in ipairs(self:GatherAvailableRovers(wanted, item.requested, quick_load, nil, no_drones)) do
					reserved[unit] = true
				end
			end
		end
		if next(reserved) then
			local available = {}
			for _, unit in ipairs(out) do
				if not reserved[unit] then available[#available + 1] = unit end
			end
			return available
		end
		return out
	end

	T.GatherAvailableRovers = function(self, class, amount, ...)
		local previous = exact_only[self]
		exact_only[self] = class
		local ok, vanilla = pcall(orig_gather, self, class, amount, ...)
		exact_only[self] = previous
		-- Restore the call-local filter before exposing a shipped error path.
		if not ok then return orig_gather(self, class, amount, ...) end
		local wanted = amount or 0
		if type(vanilla) == "table" and #vanilla >= wanted then
			return vanilla
		end
		if not is_rover_class(class) or #rover_descendants(class) == 0 then
			return vanilla
		end
		-- Vanilla came up short. Retry the shipped body over a widened list.
		local widened = orig_gather(self, class, amount, ...)
		local v_count = type(vanilla) == "table" and #vanilla or 0
		local w_count = type(widened) == "table" and #widened or 0
		if w_count > v_count then return widened end
		return vanilla
	end
end

-- The shipped warnings' "busy" check reads a leaf label directly. Their
-- status check now sees subclass totals, but with only a busy subclass they
-- can return no warning. Add that missing result after preserving every
-- warning the shipped body already chose. Synchronous; no object writes.
local function wrap_warning(orig)
	return function(self, ...)
		local warning = orig(self, ...)
		if warning then return warning end
		for _, item in pairs(self.cargo or empty_table) do
			local requested = item.requested or 0
			if requested > 0 and #rover_descendants(item.class) > 0
				and GetTotalCargoAvailable(self.city, CargoType.Rover, item.class) >= requested
				and #self:ListAvailableRovers(item.class) < requested then
				return T(14355, "Rovers are busy")
			end
		end
	end
end

SMRFixPack.Register("RoverSubclassManifest", {
	title = "Rover requests accept a rover's own subclass (RC Seeker satisfies an RC Commander requirement)",
	apply = function()
		local err = SMRFixPack.Require("RoverSubclassManifest", {
			{ class = "CargoTransporter", method = "ListAvailableRovers" },
			{ class = "CargoTransporter", method = "GatherAvailableRovers" },
			{ class = "CargoTransporter", method = "GetPayloadWarning" },
			{ class = "CargoTransporterNew", method = "ListAvailableRovers" },
			{ class = "CargoTransporterNew", method = "GatherAvailableRovers" },
			{ class = "CargoTransporterNew", method = "AddCargoAmount" },
			{ class = "CargoTransporterNew", method = "GetNonResourceCargoWarning" },
			{ class = "BaseRover" },
			{ global = "IsKindOf" },
			{ global = "ClassDescendantsList" },
			{ global = "GetTotalCargoAvailable" },
			{ global = "CargoType", kind = "table" },
			{ global = "g_Classes", kind = "table" },
		})
		if err then return err end

		install(CargoTransporter)
		install(CargoTransporterNew)

		-- Gate 3: the file-local counter reads only city.labels[class]. Sum
		-- the shipped exact-class count for each descendant instead of adding
		-- membership to live city/colony labels. The original retains connected
		-- cities and all non-rover cargo rules. No labels or saved state change.
		local orig_available = GetTotalCargoAvailable
		GetTotalCargoAvailable = function(city, cargo_type, class)
			local total = orig_available(city, cargo_type, class)
			if cargo_type == CargoType.Rover then
				for _, sub in ipairs(rover_descendants(class)) do
					total = total + orig_available(city, cargo_type, sub)
				end
			end
			return total
		end

		CargoTransporter.GetPayloadWarning = wrap_warning(CargoTransporter.GetPayloadWarning)
		CargoTransporterNew.GetNonResourceCargoWarning = wrap_warning(CargoTransporterNew.GetNonResourceCargoWarning)

		-- Record the ACTUAL rover, as the native unload path requires. Transfer
		-- the fulfilled part of an ancestor request to that leaf's cargo line.
		-- Crediting an RCRover amount for a physical RCSensor makes vanilla
		-- unloading fail its leaf lookup and spawn an extra Commander. All data
		-- below is native cargo schema, so saves unload without our code too.
		local orig_add = CargoTransporterNew.AddCargoAmount
		CargoTransporterNew.AddCargoAmount = function(self, class_id, amount)
			local cargo = self.cargo
			local exact = cargo and cargo[class_id]
			local unassigned = amount and amount > 0 and amount or 0
			if exact then
				unassigned = unassigned - math.max(0, (exact.requested or 0) - (exact.amount or 0))
			end
			while cargo and unassigned > 0 and is_rover_class(class_id) do
				local best, best_depth = nil, -1
				for key, item in pairs(cargo) do
					if type(key) == "string" and key ~= class_id and satisfies(class_id, key)
						and (item.requested or 0) > (item.amount or 0) then
						-- most-derived match wins; alphabetical settles a tie so
						-- the choice is stable across runs
						local def = g_Classes[key]
						local ancestors = def and def.__ancestors
						local depth = 0
						if ancestors then
							for _ in pairs(ancestors) do depth = depth + 1 end
						end
						if depth > best_depth or (depth == best_depth and best and key < best) then
							best, best_depth = key, depth
						end
					end
				end
				if not best then break end
				local parent = cargo[best]
				local moved = math.min(unassigned, parent.requested - (parent.amount or 0))
				if not exact then
					exact = { class = class_id, amount = 0, requested = 0 }
					cargo[class_id] = exact
				end
				parent.requested = parent.requested - moved
				exact.requested = (exact.requested or 0) + moved
				unassigned = unassigned - moved
			end
			return orig_add(self, class_id, amount)
		end
	end,
})
