-- C85: a producer "Clogged after a Dust Storm." can stay disabled for good.
--
-- The BuildingClogged story bit disables the building in its ActivationEffects,
-- BEFORE the player answers (Data/StoryBit/BuildingClogged.lua:4-8), and passes
-- only a Reason -- no Duration. SetBuildingEnabledState's Duration branch is the
-- engine's own safety net: it spawns a game-time thread that re-enables the
-- building by itself (Lua/ClassDefs/ClassDef-Effects.generated.lua:2770-2785),
-- and two other shipped events do pass one (DLC/norman/Presets/Event/
-- BugAppetit.lua:26, KitchenRescue_Reopening.lua:44). This one does not.
--
-- A lost reply is therefore PERMANENT, not delayed. The whole outcome path sits
-- inside `if reply then` (Lua/_StoryBits.lua:653-731); with no reply it falls
-- through to ProcessOutcomeEffects(storybit, ...) and Complete(), and because
-- OneTime defaults true (Lua/ClassDef-StoryBits.lua:28-29) Complete() does not
-- re-register the bit (:733-739). The story bit is finished and gone while the
-- building stays disabled and no follow-up was ever armed. Two Steam reporters
-- on 1.1.0 describe exactly that -- "never recovered", destroy-and-rebuild the
-- only way out.
--
-- Patch approach: a read-only sweep on load and daily. The stuck state is two
-- saved fields on the building (BaseBuilding.lua:30-31), so detection is exact,
-- and the cure is the game's OWN setter -- the same call vanilla's Duration
-- thread and RequiresMaintenance:Repaired (:417) make to re-enable a building.
-- The sweep enumerates with the idiom the developers' own reconcile pass uses,
-- AllMapsForEach("map", "BaseBuilding", ...) (BaseBuilding.lua:413-421).
--
-- Setexceptional_circumstances(false) is called with ONE argument, deliberately:
-- with `reason` nil the shipped body clears the reason only when
-- exceptional_circumstances_maintenance is false (:474), which is what vanilla's
-- own re-enable does. Passing an explicit `false` would clear a live maintenance
-- reason too. Where such a state coexists the infopanel reads it first anyway
-- (Building.lua:2930-2935 precedes the exceptional_circumstances branch at
-- :2942), so no stale text is shown.
--
-- ⛔ KEYED ON ONE REASON ID, NOT ON "story-bit-disabled". The evidence covers
-- this bit. Other routes to exceptional_circumstances carry their own reasons
-- and are untouched: LawEffectTurnOffBuildings uses T(374137718365, ...) and
-- restores its own snapshot on repeal (Lua/Factions/LawDef.lua:657-682), and the
-- ScriptStatements/Effects routes pass their preset's Reason.
--
-- ⛔ FOUR STATES ARE LEFT ALONE -- never unstick a building that is legitimately
-- waiting. The first two are read-only GameVars, the third a read-only global:
--   1. g_StoryBitActive (Lua/_StoryBits.lua:130) -- an array of running states;
--      BuildingClogged is inside Run() for that building right now. That is the
--      window the ActivationEffects have already disabled the building in while
--      the player has not been asked anything yet (:515-522): the 60s Delay, the
--      effects, and the notification wait (:592-606).
--   2. g_StoryBitStates[.] (:129) -- id -> StoryBitState, so at most one; the
--      follow-up BuildingClogged_1_FixAfterStorm is armed and pending for it
--      ("we'll fix it after the storm", working as intended; armed with the
--      inherited object at :758-768). An armed follow-up with NO object cannot
--      be attributed, so the sweep stands down for that pass -- fail closed.
--   3. g_PopupQueue -- ⚠️ NEITHER GameVar COVERS THE OPEN POPUP.
--      OnStopRunning() runs BEFORE OpenPopup() (:515-521), so it has already
--      removed the state from g_StoryBitActive, and the state unregistered from
--      g_StoryBitStates when it activated (the comment at :130 says so). In that
--      window the building is disabled and the player is being asked. The popup
--      dialog does pause the game (PopupNotification declares dont_pause = false,
--      so Init() adds an XPauseLayer -- Lua/UI/PopupNotification.lua:1-13), which
--      keeps OnMsg.NewDay from firing while it is on screen; but a context can
--      sit in g_PopupQueue UNOPENED while ArePopupsEnabled() is false (:383) and
--      then nothing is paused. So the sweep stands down for the whole pass if any
--      queued context carries is_storybit, the flag WaitStoryBitPopup sets
--      (Lua/MarsStoryBits.lua:71-79). The context carries no object reference, so
--      it cannot be attributed to one building -- fail closed, whole pass. An
--      open popup is still in the queue: a context is removed only when its
--      dialog closes (:82-94).
--   4. The drones reply needs no interlock: SetBuildingBreakdownState calls
--      Setexceptional_circumstances(not self.EnableBuilding, ...) with
--      EnableBuilding defaulting TRUE (ClassDef-Effects.generated.lua:4331 /
--      Data/ClassDef-Effects.lua:4307), so the building is left with
--      exceptional_circumstances FALSE and the electronics reason
--      T(149427596640, ...). The first detection test already excludes it, and
--      the emergency maintenance it owes is untouched.
--
-- ⚠️ NOT REPAIRED, ON PURPOSE (entry hypothesis H1, unpinned): a follow-up that
-- is armed but never wins its DustStormEnd_FollowUps pick -- each trigger
-- activates only the first eligible follow-up and breaks (:838-843, :199-216) --
-- and terraforming can stop dust storms entirely
-- (TerraformingDisasters.lua:15-19). Interlock 2 deliberately leaves that
-- building alone: the player accepted "the building will be turned off", and
-- releasing it would overrule their own choice. Recorded in bugs/C85.md.
--
-- FIX_POLICY §3a: layer 1 -- leave no trace. Two synchronous sweeps, no thread,
-- no persisted field, no new GameVar, no function value stored anywhere, and the
-- only write is to two fields the game already saves and already writes with
-- this setter. SAVE FOOTPRINT: none.
--
-- BRANCH GUARD (FIX_POLICY §2a): two halves, no version check anywhere.
--   * apply() carries a BEHAVIOUR PROBE on the cure itself -- it drives the
--     shipped setter on a stub and requires that one call clears BOTH fields.
--     Fails closed if that body changes shape.
--   * the DATA half can only be read once presets are loaded and a game is
--     running (FIX_POLICY §2's F110/F75 rules: a preset absent at the menu
--     proves nothing), so the sweep re-checks the shipped story bit each pass
--     and stands the module down when it no longer matches: the reason id we key
--     on must still be the one the bit disables with, and the effect must still
--     carry NO Duration. The day the developers add a Duration -- the fix we are
--     asking them for -- the building re-enables itself and this module latches
--     inactive as a RETIRE candidate. That is the thing, never a label.
--
-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-12 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target
-- moves, never to silence a BODY-CHANGED.
-- SRC: none -- a StoryBit data defect plus a load/daily sweep -- no body of ours
--   replaces a shipped one, so there is no body to hash for the defect itself.
-- DEFECT@Data/StoryBit/BuildingClogged.lua: 'Reason',\s*T\(789863173059,
--   the ActivationEffects disable passes a Reason and NO Duration, so nothing
--   ever re-enables the building. ⚠️ THE DEFECT IS AN ABSENCE (FIX_POLICY §2b):
--   this regex pins the reason id the sweep keys on, so DEFECT-GONE fires if
--   that id moves -- it will NOT fire when a Duration is ADDED beside it. That
--   case is caught at runtime by the shipped-bit re-check above, which latches
--   the module inactive. Watched for class (b)/(e) via the SRC below.
-- SRC: Lua/Buildings/BaseBuilding.lua BaseBuilding:Setexceptional_circumstances sha256=5615939f6817591d0f8b199fd9c00bfe97b4eb538732ba349403f6a38020df47
--   (Lua/Buildings/BaseBuilding.lua:470-480 at pin time) -- the cure, not the defect.

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

-- The DATA half of the branch guard (§2a). Read only where it can be read: a
-- running game, presets loaded. Returns nil when the shipped bit still has the
-- defect, or a reason string naming what changed.
local function shipped_defect_gone()
	local bits = rawget(_G, "StoryBits")
	local bit = type(bits) == "table" and bits[STORY_BIT_ID] or nil
	if type(bit) ~= "table" then
		return "the BuildingClogged story bit is gone"
	end
	local effects = bit.ActivationEffects
	local effect = type(effects) == "table" and effects[1] or nil
	if type(effect) ~= "table" then
		return "BuildingClogged no longer disables the building on activation"
	end
	if TGetID(effect.Reason) ~= CLOGGED_REASON_ID then
		return "BuildingClogged disables buildings with a different reason now"
	end
	local duration = effect.Duration
	if type(duration) == "number" and duration > 0 then
		return "BuildingClogged now re-enables the building itself after " ..
			tostring(duration) .. "ms"
	end
end

-- The whole per-building decision, in one place so the kit probe can drive the
-- REAL predicate on stub buildings instead of re-deriving it (exposed below).
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
SMRFixPack.CloggedRelease = { ShouldRelease = should_release }

local function sweep(trigger)
	local gone = shipped_defect_gone()
	if gone then
		-- Not patch rot: the shipped data no longer has the defect, which is the
		-- RETIRE signal (FIX_POLICY §2b, and the wording tools/logscan.py reads).
		local entry = SMRFixPack.fixes[FIX_ID]
		if entry and entry.status == "active" then
			entry.status = "inactive"
			entry.detail = gone
		end
		SMRFixPack.Log("%s: inactive (%s — already correct, RETIRE candidate)", FIX_ID, gone)
		return
	end
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

-- Rescues players who are ALREADY stranded -- the reporters' case, and the half
-- a Duration data patch could never reach (it is spawned at trigger time).
OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function() sweep("load") end)

-- And the same loss reached WITHOUT a load, which is why the daily pass is not
-- redundant. WaitPopupNotification returns whatever the dialog's close posts:
-- Msg(context.async_signal, reason) (Lua/UI/PopupNotification.lua:89-94). Only a
-- choice index indexes `replies`, so any other close -- a UI teardown, a mode
-- change, any non-numeric reason -- yields a nil reply on the spot
-- (_StoryBits.lua:645-653) and the game carries on unpaused. A `reason ==
-- "suspend"` close posts nothing and is not this case (:78-80). ⚠️ NOT the
-- notification timeout: an expired notification still opens the popup (:606-607
-- returns true either way), so that route is refuted, not covered.
OnMsg.NewDay = SMRFixPack.WhenActive(FIX_ID, function() sweep("daily") end)

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
