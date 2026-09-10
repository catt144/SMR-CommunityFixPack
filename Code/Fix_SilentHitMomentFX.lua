-- Relaunched Fix Pack - restore the shipped animation-moment FX on seven units.
--
-- SRC: CommonLua/Classes/AnimMoment.lua CObject:GetAnimMoments sha256=0b60ce347fed603de33cc3c49b91747a6380088e27301ce8f340acd602001283
-- DEFECT: GetEntityAnimMoments\(self:GetEntity\(\),\s*anim or self:GetStateText\(\),\s*moment_type\)
-- SRC: Lua/Buildings/BaseBuilding.lua BaseBuilding:TrackMultipleHitMoments sha256=2c40e2c2a3f47f2a47d6eb9136a1d6e237aecd13d198eb013d28968f2cebf9c7
-- DEFECT: local anim\s*=\s*obj:GetAnim\(1\)
-- SRC: Lua/Buildings/WaterExtractor.lua WaterExtractorBase:OnSetWorking sha256=a9e04948b076a59a39dd17ade5e2052c57746356f86a06cb00314c21d7e0c040
-- DEFECT: self.anim_moments_thread\s*=\s*TrackAllMoments\(pump,\s*"working",\s*self\)
-- SRC: Lua/Buildings/Building.lua TrackAllMoments sha256=05935ed430c358e4b78f7d2e3077bcfea642b861a7776ceae431c3fc831edc5d
-- DEFECT: local moment_names\s*=\s*GetAllAnimMoments\(obj\)
-- SRC: none  additive AnimMetadata presets for shipped moment-keyed FX
-- DEFECT@Data/FXPreset/ActionFXSound.lua: Target\s*=\s*"UniversalExtractorHammer"
-- DEFECT@Data/FXPreset/ActionFXParticles.lua: Action\s*=\s*"ExcavatorDigging"
--
-- C74 + C77 (game 1.1.0.403908 and 1.0.7.396349).
--
-- Two independent defects silence these effects:
--   * BaseBuilding:TrackMultipleHitMoments passes GetAnim(1), a numeric state
--     index, to a lookup keyed by state name. The wrapper below converts only
--     the two affected attach classes. It is installed at classdef time, before
--     class flattening (EF-058), and leaves every other object alone.
--   * the seven units have shipped ActionFX rows but no AnimMetadata entries.
--     The presets are added only after base-game AND DLC data have loaded, and
--     only while the exact group/id is absent. Preset:Register overwrites the
--     named slot but also appends to the group array (Preset.lua:562-581), so
--     the absence guard is what prevents duplicate preset objects.
--
-- The Water Extractor has a third defect. OnSetWorking starts TrackAllMoments
-- while its pump is still at animation speed 0; the queued
-- UpdateWorkingStateAnim restores speed later, after TimeToMoment has already
-- returned max_int. The post-wrapper restarts the tracker after that update.
-- It always DELETES the old tracker first, matching vanilla's own
-- StopTrackingMultipleHitMoments pattern, so there is never more than one.
--
-- Old-save repair: OnMsg.LoadGame replaces the cosmetic tracker for each
-- working hammer/MOXIE/Water Extractor/Excavator. A persisted handle can still
-- report valid during LoadGame even when its resumed thread is about to exit;
-- the attended first-load control caught exactly that state. Replacement is
-- therefore the discriminator, not IsValidThread. It never replays
-- OnSetWorking or an animation transition. Shuttles, RC Drillers and RC Dozers
-- restart their tracker on the next flight/job/task.
--
-- Save safety (FIX_POLICY section 3a, layer 3): presets and class methods are
-- permanents and do not enter saves. Every tracker body is vanilla's own
-- track_multiple_hit_thread / anim_moments_thread / dig_fx_thread. Our wrappers
-- and load handler are synchronous and only CALL the vanilla starters; because
-- CreateGameTimeThread defers (EF-029), our frame is gone before a tracker can
-- reach its first yield. No mod closure is stored on a persisted object.
-- Uninstall: a blocked vanilla tracker wakes to an empty preset lookup, removes
-- or abandons its remembered moment, and exits without an error; at worst the
-- multiple-hit tracker emits the one hit it had already reached before it sees
-- that the markers are gone.

local FIX_ID = "SilentHitMomentFX"
local log = SMRFixPack.Log

local preset_specs = {
	{ "UniversalExtractorHammer", "working", {
		{ Type = "Hit", Time = 3083 },
		{ Type = "Hit", Time = 9250 },
	} },
	{ "MoxiePump", "working", {
		{ Type = "Hit", Time = 3325 },
		{ Type = "Hit", Time = 9975 },
	} },
	{ "WaterExtractorCP3Pump", "working", {
		{ Type = "Hit", Time = 1667 },
		{ Type = "Hit", Time = 5000 },
	} },
	{ "WaterExtractorPump", "working", {
		{ Type = "Hit", Time = 1658 },
		{ Type = "Hit", Time = 4975 },
	} },
	{ "Shuttle", "landing", { { Type = "Hit", Time = 1033 } } },
	{ "Shuttle", "landing2", { { Type = "Hit", Time = 1033 } } },
	{ "Shuttle", "takeOff", { { Type = "Hit", Time = 2500 } } },
	{ "Shuttle", "takeOff2", { { Type = "Hit", Time = 2500 } } },
	{ "RoverRussiaDriller", "workIdle", {
		{ Type = "Hit", Time = 2708 },
		{ Type = "Hit", Time = 8125 },
	} },
	{ "RoverTerraformer", "workIdle", {
		{ Type = "Hit1", Time = 1083 },
		{ Type = "Hit1", Time = 3250 },
	} },
}

local function excavator_moments()
	local moments = {}
	for i = 1, 12 do
		local hit_time = MulDivRound(40000, i - 1, 12)
		moments[#moments + 1] = { Type = "Hit" .. i, Time = hit_time }
		moments[#moments + 1] = { Type = "Out" .. i, Time = (hit_time + 20000) % 40000 }
	end
	table.sort(moments, function(a, b)
		if a.Time ~= b.Time then return a.Time < b.Time end
		return a.Type < b.Type
	end)
	return moments
end

local function set_error(detail)
	local entry = SMRFixPack.fixes[FIX_ID]
	if entry then
		entry.status = "error"
		entry.detail = tostring(detail)
		entry.update_suspect = true
	end
	log("%s: FAILED to register animation moments: %s", FIX_ID, tostring(detail))
end

-- OnDataReady fires after every game and DLC preset has registered on a cold
-- boot, and after ClassesBuilt/ModsReloaded on the enable path (F87). The pass
-- is idempotent: an existing group/id always wins, whether it is vanilla's,
-- another mod's, or an entry this module registered on an earlier re-fire.
local function install_presets()
	local ok, err = pcall(function()
		local presets = rawget(_G, "Presets")
		local groups = type(presets) == "table" and presets.AnimMetadata
		if type(groups) ~= "table" then
			error("Presets.AnimMetadata not found (game update changed it?)")
		end

		local added = 0
		for _, spec in ipairs(preset_specs) do
			local group, id, moments = spec[1], spec[2], spec[3]
			if not (groups[group] and groups[group][id]) then
				PlaceObj("AnimMetadata", { group = group, id = id, Moments = moments })
				added = added + 1
			end
		end

		local group, id = "ExcavatorShovel", "working"
		if not (groups[group] and groups[group][id]) then
			PlaceObj("AnimMetadata", { group = group, id = id, Moments = excavator_moments() })
			added = added + 1
		end

		if added > 0 then
			log("%s: registered %d missing animation-moment preset(s)", FIX_ID, added)
		end
	end)
	if not ok then set_error(err) end
end

-- Behaviour probe for the numeric-index defect. At classdef time the cold-boot
-- preset files have not loaded yet, so the probe lends the shipped lookup one
-- temporary, known marker and restores the exact previous table before it
-- returns. CObject:GetAnimMoments is synchronous and reads only self:GetEntity
-- plus Presets.AnimMetadata (AnimMoment.lua:35-37 -> :5-16): no object, save or
-- thread is touched. Result is tri-state: BROKEN, RESOLVED, or unknown.
local function numeric_lookup_shape(shipped_get)
	local presets = rawget(_G, "Presets")
	if type(presets) ~= "table" then return end
	local state_idx = GetStateIdx("working")
	if type(state_idx) ~= "number" or state_idx < 0 or GetStateName(state_idx) ~= "working" then
		return
	end
	local entity = "UniversalExtractorHammer"
	local group = GetAnimEntity(entity, "working")
	if type(group) ~= "string" or group == "" then return end

	local old_groups = presets.AnimMetadata
	local groups = type(old_groups) == "table" and old_groups or {}
	local old_group = groups[group]
	if groups ~= old_groups then presets.AnimMetadata = groups end
	groups[group] = {
		working = { Moments = { { Type = "C74Probe", Time = 1 } } },
	}

	local stub = {
		GetEntity = function() return entity end,
		GetStateText = function() return "working" end,
	}
	local ok, by_name, by_index = pcall(function()
		return shipped_get(stub, "working"), shipped_get(stub, state_idx)
	end)
	groups[group] = old_group
	if groups ~= old_groups then presets.AnimMetadata = old_groups end
	if not ok then error(by_name) end
	if type(by_name) ~= "table" or #by_name ~= 1 or by_name[1].Type ~= "C74Probe"
		then return end
	if type(by_index) ~= "table" then return end
	if #by_index == 0 then return "broken" end
	if #by_index == 1 and by_index[1].Type == "C74Probe" then return "resolved" end
end

local function lookup_is(shipped_get, expected)
	return SMRFixPack.Require(FIX_ID, {
		-- STUB CONTRACT: numeric_lookup_shape supplies only GetEntity and
		-- GetStateText, the two reads in the pinned three-line shipped body.
		-- The temporary preset makes the result observable without constructing
		-- a class/preset object at apply time (the F87 enable-path rule).
		{ probe = function() return numeric_lookup_shape(shipped_get) == expected end },
	}) == nil
end

local function has_moments(obj, anim, moment_type)
	return IsValid(obj) and obj:GetAnimMomentsCount(anim, moment_type) > 0
end

local function restart_water_tracker(self, replace)
	if not self.working then return false end
	local pump = self:GetAttach("WaterExtractorPump")
	if not IsValid(pump) or GetStateName(pump:GetAnim(1)) ~= "working"
			or pump:GetAnimSpeed(1) <= 0 or not has_moments(pump, "working", "Hit") then
		return false
	end
	if IsValidThread(self.anim_moments_thread) then
		if not replace then return false end
		DeleteThread(self.anim_moments_thread)
	end
	self.anim_moments_thread = TrackAllMoments(pump, "working", self)
	return true
end

local function start_multiple_tracker(self)
	if not self.working then return false end
	-- Mirror ChangeWorkingStateAnim's selection: self first, then attaches, or
	-- the forced attach class when one is declared. Unlike that routine, never
	-- SetAnim here -- an old-save heal must not replay or snap an animation.
	local objects = self:GetAttaches() or {}
	table.insert(objects, 1, self)
	local forced = self.play_working_anim_on_this_attach
	local first = forced and table.find(objects, "class", forced) or 1
	local last = forced and first or #objects
	if not first then return false end
	local obj
	for i = first, last do
		local candidate = objects[i]
		if IsValid(candidate) and candidate:HasEntity()
				and candidate:HasAnim(self.work_anim_loop)
				and has_moments(candidate, self.work_anim_loop, "Hit") then
			obj = candidate
			break
		end
	end
	if not obj then return false end
	local override = type(self.track_multiple_hit_moments_in_work_state) == "table"
		and self.track_multiple_hit_moments_in_work_state or nil
	self:TrackMultipleHitMoments(obj, "Working", nil, override, true)
	return true
end

local function start_excavator_tracker(self)
	if not self.working or not IsValidThread(self.dig_anim_thread) or not IsValid(self.arm)
			or GetStateName(self.arm:GetAnim(1)) ~= "working"
			or not has_moments(self.arm, "working") then
		return false
	end
	if IsValidThread(self.dig_fx_thread) then
		DeleteThread(self.dig_fx_thread)
	end
	self.dig_fx_thread = TrackAllMoments(self.arm, "ExcavatorDigging", self.arm)
	return true
end

-- LoadGame runs after PersistPostLoad reconstructed the saved thread handles and
-- before PostLoadGame declares the colony ready (EF-028). New game-time threads
-- defer until this synchronous handler returns (EF-029), so no mod frame sits
-- below a yield. Each eligible tracker is replaced: TrackMultipleHitMoments
-- deletes its own old thread, while the Water/Excavator helpers do so explicitly.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local each = rawget(_G, "AllMapsForEach")
	if type(each) ~= "function" then return end
	local started = 0
	each(true, "PreciousMetalsExtractor", function(obj)
		if start_multiple_tracker(obj) then started = started + 1 end
	end)
	each(true, "MOXIEBase", function(obj)
		if start_multiple_tracker(obj) then started = started + 1 end
	end)
	each(true, "WaterExtractorBase", function(obj)
		if restart_water_tracker(obj, true) then
			started = started + 1
		end
	end)
	each(true, "TheExcavatorBase", function(obj)
		if start_excavator_tracker(obj) then started = started + 1 end
	end)
	if started > 0 then
		log("%s: restored %d missing hit-moment tracker(s) on load", FIX_ID, started)
	end
end)

SMRFixPack.OnDataReady(SMRFixPack.WhenActive(FIX_ID, install_presets))

SMRFixPack.Register(FIX_ID, {
	title = "Seven units play their shipped strike, landing, drilling and digging effects",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "GetStateIdx" },
			{ global = "GetStateName" },
			{ global = "GetAnimEntity" },
			{ global = "IsKindOf" },
			{ global = "MulDivRound" },
			{ global = "PlaceObj" },
			{ global = "TrackAllMoments" },
			{ class = "CObject", method = "GetAnimMoments" },
			{ class = "BaseBuilding", method = "TrackMultipleHitMoments" },
			{ class = "BaseBuilding", method = "UpdateWorkingStateAnim" },
		})
		if err then return err end

		local shipped_get = CObject.GetAnimMoments
		if lookup_is(shipped_get, "broken") then
			function CObject:GetAnimMoments(anim, moment_type)
				-- The class test is the identity decision: a foreign/non-C74 object
				-- delegates before any field read, allocation or logging.
				if type(anim) ~= "number" or not (IsKindOf(self, "UniversalExtractorHammer")
						or IsKindOf(self, "MoxiePump")) then
					return shipped_get(self, anim, moment_type)
				end
				local name = GetStateName(anim)
				return shipped_get(self, name, moment_type)
			end
		elseif lookup_is(shipped_get, "resolved") then
			log("%s: numeric animation indices already resolve; conversion left to the game", FIX_ID)
		else
			return "numeric animation-moment lookup behaviour not recognised"
		end

		local shipped_update = BaseBuilding.UpdateWorkingStateAnim
		function BaseBuilding:UpdateWorkingStateAnim(...)
			-- Shared wrapper: foreign/non-WaterExtractor objects return before any
			-- field read, allocation or logging (FIX_POLICY section 2).
			if not IsKindOf(self, "WaterExtractorBase") then
				return shipped_update(self, ...)
			end
			local result = shipped_update(self, ...)
			restart_water_tracker(self, true)
			return result
		end
	end,
})
