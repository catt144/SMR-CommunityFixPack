-- F75: six of Last Transmission's approval conditions can never fire, and one of
-- them measures the wrong resource.
--
-- Found while implementing F22 (the `GetGridGlobalStorage` aggregation defect),
-- which names these same conditions as its victims. Repairing F22 alone would
-- not have made any of them work.
--
-- Defect (a) — the conditions are inert. `FactionLikeGlobalCondition:Eval`
-- (`Lua\ClassDefs\ClassDef-Factions.generated.lua:843-849`) reads ONE property:
--     if not self.Condition or not self.Condition.eval(UIColony) then return 0 end
--     return self.Value
-- but the six storage entries in `Data\FactionDef\LastTransmission.lua:94-192`
-- put their `ScriptConditionList` on **`Prerequisite`** instead of **`Condition`**:
--     TLEPowerStorage2Sols, TLENoPowerStorage, TLEWaterStorage2Sols,
--     TLENoWaterStorage,    TLEOxygenStorage2Sols, TLENoOxygenStorage
-- `Prerequisite` is a real property (inherited from FactionLikeBase, `:645-646`)
-- but it is only a gate — `FactionLikeBase:EvalPreconditions` (`:672-688`) calls
-- it to decide whether the like is considered at all. With `Condition` unset,
-- `Eval()` then returns 0 every single time, so the like contributes nothing
-- however well the colony is doing.
--
-- The authoring slip is visible inside the same file: the other seven
-- `FactionLikeGlobalCondition`s in LastTransmission.lua set `Condition`
-- (`:208, :224, :240, :256, :281, :298, :313`), and the one at `:266-292` sets
-- BOTH — so the difference between the two properties was understood. A sweep of
-- every shipped FactionDef found this pattern only here.
--
-- It is not a quiet failure either: `FactionDef:EvalApproval` (`:181-187`) shows
-- the `HowTo` text of any positive like that evaluated to 0 as an outstanding
-- goal. So Last Transmission permanently advertises "Have Power for more than 2
-- sols stored", the player does it, and nothing ever happens.
--
-- Defect (b) — `TLEOxygenStorage2Sols` (`:160-175`) measures POWER. Its
-- Explanation, HowTo and Id all say Oxygen, but its nested
-- `ScriptCheckGridGlobalStorage` never sets `GridType`, which defaults to
-- "Power" (`ClassDef-Conditions.generated.lua:2034-2035`), and the generated
-- `eval` faithfully reads `GetGridGlobalStorage("Power")`. Its negative twin
-- `TLENoOxygenStorage` sets `GridType = "Oxygen"` correctly, as do both Water
-- entries — only this one was missed.
--
-- Patch approach: preset data patch (FIX_POLICY §1.1, the most compatible
-- technique) from OnMsg.DataLoaded (+ DataChanged for editor reloads), since
-- presets do not exist when mod code runs:
--   (a) move the `ScriptConditionList` from `Prerequisite` to `Condition`,
--       leaving `Prerequisite` false. Gating is unchanged — the same test, in the
--       place `Eval` actually reads — and the entries end up structurally
--       identical to their working siblings in the same file.
--   (b) set the missing `GridType = "Oxygen"` and rebuild that entry's `eval`
--       from the corrected fields, mirroring the shipped CodeTemplate
--       "GetGridGlobalStorage(self.GridType) $self.Condition $self.Value"
--       (`ClassDef-Conditions.generated.lua:2040`). Every other entry keeps its
--       shipped eval untouched.
--
-- Scope: only the six ids above, only in the LastTransmission FactionDef, and
-- only where the defect is still present — an entry that already carries a
-- `Condition` is left exactly as found.

local FIX_ID = "LastTransmissionStorage"

-- id -> the resource the entry's own Explanation/HowTo/Id says it measures
local STORAGE_LIKES = {
	TLEPowerStorage2Sols  = "Power",
	TLENoPowerStorage     = "Power",
	TLEWaterStorage2Sols  = "Water",
	TLENoWaterStorage     = "Water",
	TLEOxygenStorage2Sols = "Oxygen",
	TLENoOxygenStorage    = "Oxygen",
}

local COMPARE = {
	[">"]  = function(a, b) return a >  b end,
	["<"]  = function(a, b) return a <  b end,
	[">="] = function(a, b) return a >= b end,
	["<="] = function(a, b) return a <= b end,
	["=="] = function(a, b) return a == b end,
	["~="] = function(a, b) return a ~= b end,
}

local function log(fmt, ...)
	local msg = string.format("[CommunityFixPack] " .. fmt, ...)
	-- ModLog's output path formats the message a second time (00_Core.lua:18-25).
	if rawget(_G, "ModLog") then ModLog((msg:gsub("%%", "%%%%"))) else print(msg) end
end

-- The ScriptCheckGridGlobalStorage node inside a condition list, if there is one.
local function find_grid_check(list)
	if type(list) ~= "table" then return nil end
	for _, node in ipairs(list) do
		if type(node) == "table" and node.class == "ScriptCheckGridGlobalStorage" then
			return node
		end
	end
	return nil
end

local patched = false        -- a full pass ran since the last (re)load of the presets
local ever_changed = false   -- some pass this session actually moved/retargeted entries

local function patch()
	if patched then return end
	-- FIX (QA 2026-07-25): honor the per-fix veto here too — these OnMsg
	-- handlers are installed unconditionally, and Register's veto only skips
	-- apply(), so without this check a disabled fix still mutated the presets.
	local disabled = rawget(_G, "SMRFixPack_Disabled")
	if type(disabled) == "table" and disabled[FIX_ID] then return end
	local defs = rawget(_G, "FactionDefs")
	if type(defs) ~= "table" then return end   -- presets not loaded yet
	local faction = defs.LastTransmission
	local likes = type(faction) == "table" and faction.likes
	if type(likes) ~= "table" then
		-- Presets ARE loaded but the faction (or its likes list) is gone — a
		-- future update removed the target. Say so instead of staying "active"
		-- forever with zero effect (QA 2026-07-25).
		patched = true
		local entry = SMRFixPack.fixes[FIX_ID]
		if entry then
			entry.status = "inactive"
			entry.detail = "FactionDefs.LastTransmission not found (game update changed it?)"
		end
		log("%s: inactive (FactionDefs.LastTransmission not found)", FIX_ID)
		return
	end

	local stats = { seen = 0, moved = 0, retargeted = 0 }
	for _, like in ipairs(likes) do
		local grid_type = type(like) == "table" and like.Id and STORAGE_LIKES[like.Id]
		if grid_type then
			stats.seen = stats.seen + 1

			-- (a) the test has to live where Eval() looks for it
			if not like.Condition and type(like.Prerequisite) == "table" then
				like.Condition = like.Prerequisite
				like.Prerequisite = false
				stats.moved = stats.moved + 1
			end

			-- (b) and it has to measure the resource the entry claims to measure
			local check = find_grid_check(like.Condition)
			if check and check.GridType ~= grid_type then
				check.GridType = grid_type
				local op = COMPARE[check.Condition]
				local value = check.Value or 1440000
				if op and type(like.Condition) == "table" then
					like.Condition.eval = function()
						return op(GetGridGlobalStorage(grid_type) or 0, value)
					end
					stats.retargeted = stats.retargeted + 1
				end
			end
		end
	end
	patched = true

	local entry = SMRFixPack.fixes[FIX_ID]
	if stats.moved > 0 or stats.retargeted > 0 then
		ever_changed = true
		log("%s: %d storage condition(s) made effective, %d retargeted", FIX_ID, stats.moved, stats.retargeted)
	elseif ever_changed then
		-- FIX (QA 2026-07-25): the engine posts Msg("DataChanged", false) right
		-- after every DataLoaded (Dlc.lua:715-717), which reruns this pass over
		-- the presets it just corrected. Finding nothing left to do then is
		-- SUCCESS, not "shipped data already correct" — without this branch the
		-- fix relabeled itself inactive on every normal boot.
		return
	elseif stats.seen == 0 then
		if entry then
			entry.status = "inactive"
			entry.detail = "Last Transmission has no storage conditions any more"
		end
		log("%s: inactive (Last Transmission has no storage conditions any more)", FIX_ID)
	else
		if entry then
			entry.status = "inactive"
			entry.detail = "the shipped presets are already correct"
		end
		log("%s: inactive (the shipped presets are already correct)", FIX_ID)
	end
	SMRFixPack.LastTransmissionStorage = stats
end

SMRFixPack.Register(FIX_ID, {
	title = "Last Transmission's power/water/oxygen storage opinions actually count",
	apply = function()
		patch()   -- no-op unless the presets are already loaded
	end,
})

function OnMsg.DataLoaded()
	patch()
end

function OnMsg.DataChanged(classes)
	if classes and not classes.FactionDef then return end
	patched = false
	patch()
end
