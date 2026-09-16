-- C96: a rover manifest asks for a class by NAME and matches by exact leaf
-- class, so a rover's own subclass never satisfies a request for its base. The
-- reported case is the RC Seeker (RCSensor, a genuine RCRover subclass) being
-- refused by an anomaly expedition that wants an RC Commander (RCRover); the
-- same refusal hits RCSolar and every other RC subclass relationship.
-- See docs/agent/bugs/C96.md and reports/C96_ROVER_SUBCLASS_BUILD.md.
--
-- ⛔ TWO GATES, not one. Widening the == compare alone changes NOTHING, because
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
-- ⭐ THE CARGO LINE MUST BE CREDITED TO THE REQUESTED CLASS. CargoTransporterNew
-- :LoadRovers credits AddCargoAmount(rover.class, 1) (:444), and AddCargoAmount
-- is a guarded no-op when no line exists for that exact id (:87). A Seeker
-- loaded against an "RCRover" line would therefore credit nothing, leaving
-- requested - amount short (:1837) and the rocket still asking for a rover it
-- already carries. The remap below can only fire when the exact line is absent
-- AND a base line exists, which vanilla never produces on its own.
--
-- Scope: no object field, GameVar, thread, migration or saved callback is added;
-- the widen flag lives in a weak-keyed module local, so nothing reaches a save.
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

-- transporter -> the class name currently being widened. Weak keys: a rocket
-- that is destroyed mid-gather is collectable, and nothing here is persisted.
local widening = setmetatable({}, { __mode = "k" })

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

local function install(class_name)
	local T = g_Classes[class_name]
	if not T then return end

	local orig_list = T.ListAvailableRovers
	local orig_gather = T.GatherAvailableRovers

	-- Widen the SOURCE LIST, and only while our own gather asked for it. The
	-- shipped lister is called once per descendant so its availability filter
	-- is reused verbatim and the leaf-class compare is satisfied by passing
	-- each subclass its own name.
	T.ListAvailableRovers = function(self, class, ...)
		local list = orig_list(self, class, ...)
		if widening[self] ~= class then return list end
		local out = {}
		append(out, list)
		for _, sub in ipairs(rover_descendants(class)) do
			append(out, orig_list(self, sub, ...))
		end
		return out
	end

	T.GatherAvailableRovers = function(self, class, amount, ...)
		local vanilla = orig_gather(self, class, amount, ...)
		local wanted = amount or 0
		if type(vanilla) == "table" and #vanilla >= wanted then
			return vanilla
		end
		if not is_rover_class(class) or #rover_descendants(class) == 0 then
			return vanilla
		end
		-- Vanilla came up short. Retry the shipped body over a widened list.
		widening[self] = class
		local ok, widened = pcall(orig_gather, self, class, amount, ...)
		widening[self] = nil
		if not ok then return vanilla end
		local v_count = type(vanilla) == "table" and #vanilla or 0
		local w_count = type(widened) == "table" and #widened or 0
		if w_count > v_count then return widened end
		return vanilla
	end
end

SMRFixPack.Register("RoverSubclassManifest", {
	title = "Rover requests accept a rover's own subclass (RC Seeker satisfies an RC Commander requirement)",
	apply = function()
		local err = SMRFixPack.Require("RoverSubclassManifest", {
			{ class = "CargoTransporter", method = "ListAvailableRovers" },
			{ class = "CargoTransporter", method = "GatherAvailableRovers" },
			{ class = "CargoTransporterNew", method = "ListAvailableRovers" },
			{ class = "CargoTransporterNew", method = "GatherAvailableRovers" },
			{ class = "CargoTransporterNew", method = "AddCargoAmount" },
			{ class = "BaseRover" },
			{ global = "IsKindOf" },
			{ global = "ClassDescendantsList" },
			{ global = "g_Classes", kind = "table" },
		})
		if err then return err end

		install("CargoTransporter")
		install("CargoTransporterNew")

		-- Credit the REQUESTED class when a subclass was loaded against it.
		-- Fires only when there is no exact line and exactly one base line the
		-- loaded class satisfies; vanilla never loads a rover whose own line is
		-- missing, so this cannot change shipped behaviour.
		local orig_add = CargoTransporterNew.AddCargoAmount
		CargoTransporterNew.AddCargoAmount = function(self, class_id, amount)
			local cargo = self.cargo
			if cargo and not cargo[class_id] and is_rover_class(class_id) then
				local best, best_depth = nil, -1
				for key in pairs(cargo) do
					if type(key) == "string" and key ~= class_id and satisfies(class_id, key) then
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
				if best then
					return orig_add(self, best, amount)
				end
			end
			return orig_add(self, class_id, amount)
		end
	end,
})
