-- C85 / F121: load-only migration for legacy buildings left clogged forever.
--
-- SOURCE: archived game 1.1.1.405907. BuildingClogged now has Duration 3600000
-- (Data/StoryBit/BuildingClogged.lua:6-8). Its effect creates an anonymous thread
-- only when fired (Lua/ClassDefs/ClassDef-Effects.generated.lua:2772-2790), so
-- it cannot heal a pre-patch stranded building. The thread has no building-owned
-- handle and OnScreenTimer is false: after the story finishes, its healthy timed
-- disable has the same saved reason/state as an old stranded disable.
--
-- Therefore this synchronous LoadGame repair requires the SAVE's lua_revision
-- to predate the first Duration build (405907), supplied by vanilla's LoadGame
-- message (CommonLua/Savegame.lua:798-812; metadata is written at :775).
-- This is provenance of the uninspectable saved timer, not a runtime version
-- gate: the cure still earns a behaviour probe below. Unknown provenance fails
-- closed. Old stranded state already resaved on 1.1.1 is ambiguous and remains
-- untouched, as does every new-game / daily / live event. No new saved marker.
--
-- Detection retains C85's exact reason and event interlocks: a running clogged
-- story, an armed follow-up, or any queued story-bit popup prevents release.
-- Unreadable story state fails closed. An armed follow-up is the player's
-- accepted wait-for-storm choice and is never overridden.
--
-- The only write calls vanilla Setexceptional_circumstances(false) with ONE
-- argument (Lua/Buildings/BaseBuilding.lua:470-480): this clears the reason only
-- when exceptional_circumstances_maintenance is false, exactly as vanilla does.
-- Other reasons, maintenance and healthy events stay vanilla-owned.
--
-- FIX_POLICY section 3a: synchronous load handler, no yield, thread, GameVar,
-- object field or persisted function. Save footprint: only vanilla's existing
-- fields are healed; no executable removal residue. The helper table is a
-- non-persisted mod global used by TestKit. Branch guard: behaviour-probe the
-- shipped setter, and refuse missing/changed cure dependencies.
--
-- MANIFEST: legacy state migration, not a claim of a current preset defect.
-- SRC: none -- load-only legacy state repair; no shipped body replaced
-- DEFECT@Data/StoryBit/BuildingClogged.lua: 'Reason',\s*T\(789863173059,
-- The historical saved reason is the key; a positive Duration does not retire
-- the migration. The setter pin watches the cure, not the legacy defect.
-- SRC: Lua/Buildings/BaseBuilding.lua BaseBuilding:Setexceptional_circumstances sha256=5615939f6817591d0f8b199fd9c00bfe97b4eb538732ba349403f6a38020df47

local FIX_ID = "CloggedBuildingRelease"

-- T(789863173059, "Clogged after a Dust Storm.") -- Data/StoryBit/BuildingClogged.lua:6
local CLOGGED_REASON_ID = 789863173059
local STORY_BIT_ID = "BuildingClogged"
local FOLLOW_UP_ID = "BuildingClogged_1_FixAfterStorm"

-- The end state the reporters are in: disabled by THIS story bit's reason.
-- TGetID handles the packed-userdata and both table forms a T can take after a
-- save/load round trip (CommonLua/Core/localization.lua:47-64).
local function is_stuck_clogged(building)
	if not building.exceptional_circumstances then return false end
	local reason = building.exceptional_circumstances_reason
	if not reason then return false end
	return TGetID(reason) == CLOGGED_REASON_ID
end

-- Interlock 1. g_StoryBitActive is an ARRAY of running states; a state carries
-- .id and .object (Lua/_StoryBits.lua:274-285). Unreadable => fail closed.
local function clogged_popup_running(building)
	local running = rawget(_G, "g_StoryBitActive")
	if type(running) ~= "table" then return true end
	for _, state in ipairs(running) do
		if state.id == STORY_BIT_ID and state.object == building then
			return true
		end
	end
	return false
end

-- Interlock 2. g_StoryBitStates is keyed by id, so there is at most one armed
-- follow-up. Unreadable, or armed with no object to attribute it to => fail
-- closed for this pass.
local function fix_after_storm_pending(building)
	local waiting = rawget(_G, "g_StoryBitStates")
	if type(waiting) ~= "table" then return true end
	local state = waiting[FOLLOW_UP_ID]
	if type(state) ~= "table" then return false end
	if not state.object then return true end
	return state.object == building
end

-- Interlock 3, whole-pass. A story-bit popup queued or open is the one window
-- neither GameVar covers (see the header). Unreadable => fail closed.
local function a_storybit_popup_is_pending()
	local queue = rawget(_G, "g_PopupQueue")
	if type(queue) ~= "table" then return true end
	for _, context in ipairs(queue) do
		if type(context) == "table" and context.is_storybit then return true end
	end
	return false
end

-- The whole per-building decision, in one place so the kit probe can drive the
-- REAL predicate on stub buildings instead of re-deriving it (exposed below).
local function accepts_save(metadata)
	local revision = type(metadata) == "table" and metadata.lua_revision
	return type(revision) == "number" and revision > 0 and revision < 405907
end

local function should_release(building)
	return is_stuck_clogged(building)
		and not clogged_popup_running(building)
		and not fix_after_storm_pending(building)
		and not a_storybit_popup_is_pending()
end

-- Exposed for the TestKit's behaviour probe. Precedent: SMRFixPack.Sanitizer
-- (90_SaveSanitizer.lua:402). SMRFixPack is a plain mod global, not a GameVar,
-- and nothing persisted reaches it, so this stores no function value anywhere the
-- save can see (FIX_POLICY §3a).
SMRFixPack.CloggedRelease = { ShouldRelease = should_release, AcceptsSave = accepts_save }

local function sweep(trigger)
	-- Optimisation only: should_release checks this per building anyway, so this
	-- line carries no behaviour of its own (proved by a scratch variant that
	-- reverts it alone and changes no desk leg). It keeps the whole-map walk off
	-- the common "a popup is up" case.
	if a_storybit_popup_is_pending() then return end
	local each = rawget(_G, "AllMapsForEach")
	if type(each) ~= "function" then return end
	local released = 0
	each("map", "BaseBuilding", function(building)
		if should_release(building) then
			building:Setexceptional_circumstances(false)
			released = released + 1
		end
	end)
	if released > 0 then
		SMRFixPack.Log("%s: released %d building(s) stuck 'Clogged after a Dust Storm.' (%s)",
			FIX_ID, released, trigger)
	end
end

-- Save provenance is required because a 1.1.1 timer has no inspectable handle.
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function(metadata)
	if not accepts_save(metadata) then return end
	sweep("legacy load")
end)

SMRFixPack.Register(FIX_ID, {
	title = "Buildings left \"Clogged after a Dust Storm.\" are switched back on",
	apply = function()
		local setter = BaseBuilding and BaseBuilding.Setexceptional_circumstances
		return SMRFixPack.Require(FIX_ID, {
			{ class = "BaseBuilding", method = "Setexceptional_circumstances" },
			{ global = "TGetID" },
			{ global = "AllMapsForEach" },
			-- BEHAVIOUR PROBE on the cure. Stub contract: the shipped body reads
			-- and writes three of its own fields and then calls exactly three
			-- methods on self -- UpdateWorking, UpdateConsumption, AttachSign
			-- (BaseBuilding.lua:470-480). It touches no global, allocates
			-- nothing, starts no thread and cannot yield, so a closed stub with
			-- those three as no-ops drives it safely and completely. The probe
			-- requires the cure to still BE a cure: one argument clears both
			-- saved fields.
			{ probe = function()
				local stub = {
					exceptional_circumstances = true,
					exceptional_circumstances_reason =
						{ CLOGGED_REASON_ID, "Clogged after a Dust Storm." },
					exceptional_circumstances_maintenance = false,
					UpdateWorking = function() end,
					UpdateConsumption = function() end,
					AttachSign = function() end,
				}
				setter(stub, false)
				return stub.exceptional_circumstances == false
					and stub.exceptional_circumstances_reason == false
			end,
			reason = "Setexceptional_circumstances(false) no longer clears the disable and its reason" },
		})
	end,
})
