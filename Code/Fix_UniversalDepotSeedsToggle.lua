-- C121: a Universal Depot built before Seeds is unlocked never shows a Seeds
-- toggle, because the unlock refresh runs only for the sibling depot branch.
--
-- SRC: Lua/Buildings/MultiResourceDepot.lua OnMsg.PresetLockStateChanged sha256=2736807aab769047dc9eaf634f4cb9c715f3b5b50e91a1329d6142894c177a58
--   (Lua/Buildings/MultiResourceDepot.lua:470-475 at pin time, 6 lines hashed)
-- DEFECT: AllMapsForEach\(true,\s*"MultiResourceDepotBase"
--   the only depot refresh on a lock change walks one branch of the depot tree.
--   The DEFECT line states an ABSENCE (FIX_POLICY §2b): a refresh added for
--   UniversalStorageDepot anywhere else will not fire DEFECT-GONE, so this pin is
--   watched for a changed body only. If vanilla adds the class here, this module
--   becomes a redundant recompute of the same value, not a conflict.
--
-- SRC: Lua/Resources.lua GroupResourcesForIP sha256=2b468cf3844d25834b89ce787a031a18fbc7feb3be9add05e09bbc300078974f
--   (Lua/Resources.lua:137-163 at pin time, 27 lines hashed)
-- SRC: Lua/Buildings/StorageDepot.lua UniversalStorageDepotBase:GameInit sha256=d697cfe870a2af7b92d7a04c5b82879ddb747916fced3dccac12353c0da01816
--   (Lua/Buildings/StorageDepot.lua:423-462 at pin time, 40 lines hashed)
--   No DEFECT: lines on these two, deliberately. They are the bodies this module
--   CALLS and MIRRORS: the grouping it recomputes, and the one line (:461) whose
--   stale result it replaces. A game patch that moves either flips BODY-CHANGED
--   and forces a read.
--
-- Defect (archived 1.1.1.405907, every line re-read; full trace docs/agent/bugs/C121.md):
--   * UniversalStorageDepotBase:SetStorableResources appends "Seeds" for class
--     UniversalStorageDepot with no lock check (StorageDepot.lua:509-519), and
--     CreateResourceRequests registers a request for it (:521-533).
--   * GameInit caches grouped_resources_for_ip = GroupResourcesForIP(storable_
--     resources) (:461), which drops every resource whose lock state is "hidden"
--     (Resources.lua:137-146). Seeds ships hidden (Data/Resource.lua:309).
--   * Researching a Seeds tech fires PresetLockStateChanged, and vanilla's only
--     depot handler re-groups MultiResourceDepotBase alone (MultiResourceDepot.
--     lua:470-475). UniversalStorageDepot -> UniversalStorageDepotBase ->
--     StorageDepot is the sibling branch (StorageDepot.lua:329-330; EF-102).
--   * The infopanel prefers the cached field (contextResourceAcceptToggles.
--     generated.lua:13), so the Seeds toggle never appears on that depot.
--
-- Intent tells (FIX_POLICY §4): (1) player-reported harm; (3) sibling
-- contradiction — the same file re-groups the sibling depots on this exact
-- message, through the same GroupResourcesForIP call (:462-463).
-- Reachability R1: every Universal Depot built before Seeds is unlocked, in
-- ordinary play without the GeoEngineer profile or the NoTerraforming rule.
--
-- Patch approach: FIX_POLICY §1.2, an ADDITIVE handler beside vanilla's, plus a
-- load-time heal for depots whose cache is already stale. Nothing is wrapped and
-- no shipped body is replaced. Both paths run the same recompute: vanilla's own
-- expression from GameInit :461, GroupResourcesForIP(self.storable_resources),
-- with no player argument, exactly as GameInit and vanilla's handler (:463) call
-- it. The result is written only when it differs from the cache, and the panel is
-- rebuilt through the depot's own method (StorageDepot.lua:398-400), which acts
-- only when the depot is selected (Lua/X/Infopanel.lua:428-429).
--
-- ⛔ SCOPE: class == "UniversalStorageDepot" EXACTLY, the same test the shipped
-- code uses to add Seeds (:511) and to scope GameInit's depot-only work (:446).
-- UniversalStorageDepotBase is NOT the target: rockets (RocketBase.lua:2), the
-- Space Elevator (SpaceElevator.lua:2), MysteryDepot (StorageDepot.lua:790-792)
-- and the seven single-resource depots also inherit it, and rockets change their
-- storable_resources at runtime. Re-grouping those is a behaviour change nobody
-- reported and this module does not claim.
--
-- Save safety (FIX_POLICY §3/§3a), tier 1: no thread, no persisted field of ours,
-- no function value stored anywhere. The only write is vanilla's own declared
-- property (StorageDepot.lua:346) set to the value vanilla itself computes for a
-- depot built today. After removal a healed depot simply keeps a correct list.
--
-- Load timing: the heal runs on PostLoadGame, when the player's lock states are
-- already deserialised (they are Player properties, EF-093). If vanilla's own
-- PostLoadGame re-seed then changes a lock, it fires PresetLockStateChanged and
-- the live handler recomputes, so handler order between the two does not matter.

local FIX_ID = "UniversalDepotSeedsToggle"
local DEPOT_CLASS = "UniversalStorageDepot"

local log = SMRFixPack.Log

-- Every resource id a grouping shows, as one sorted key. GroupResourcesForIP
-- returns top-level entries that are groups with `items` (loose items are folded
-- into "other_resources", Resources.lua:148-160); an entry with no items is
-- keyed by its own id so an unexpected shape still compares, never throws.
local function grouping_key(groups)
	if type(groups) ~= "table" then return nil end
	local ids = {}
	for _, entry in ipairs(groups) do
		if type(entry) == "table" then
			if type(entry.items) == "table" then
				for _, id in ipairs(entry.items) do ids[#ids + 1] = tostring(id) end
			elseif entry.id ~= nil then
				ids[#ids + 1] = tostring(entry.id)
			end
		end
	end
	table.sort(ids)
	return table.concat(ids, ",")
end

-- Returns true when this depot's cached list was stale and has been replaced.
local function refresh(depot)
	if not (IsValid(depot) and depot.class == DEPOT_CLASS) then return false end
	if type(depot.storable_resources) ~= "table" then return false end
	local fresh = GroupResourcesForIP(depot.storable_resources)
	if type(fresh) ~= "table" then return false end
	if grouping_key(fresh) == grouping_key(depot.grouped_resources_for_ip) then return false end
	depot.grouped_resources_for_ip = fresh
	depot:RebuildInfopanel()
	return true
end

local function refresh_all()
	local count = 0
	AllMapsForEach(true, DEPOT_CLASS, function(depot)
		local ok, changed = pcall(refresh, depot)
		if not ok then
			log("%s: refresh raised on %s#%s: %s — that depot is left as it was",
				FIX_ID, DEPOT_CLASS, tostring(rawget(depot, "handle")), tostring(changed))
		elseif changed then
			count = count + 1
		end
	end)
	return count
end

-- The live half: same message, same filter, as vanilla's handler for the sibling
-- branch (MultiResourceDepot.lua:470-472).
OnMsg.PresetLockStateChanged = SMRFixPack.WhenActive(FIX_ID, function(preset)
	if not IsKindOf(preset, "Resource") then return end
	local n = refresh_all()
	if n > 0 then
		log("%s: %s changed lock state; updated the resource toggles on %d Universal Depot(s)",
			FIX_ID, tostring(preset.id), n)
	end
end)

-- The heal: depots a save already carries with a stale list. Idempotent, so no
-- one-shot flag (§3a tier 1); on a clean save it compares and writes nothing.
OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local n = refresh_all()
	-- Printed at zero too: a sitting has to tell "clean" from "never ran".
	log("%s: load pass updated the resource toggles on %d Universal Depot(s)", FIX_ID, n)
end)

SMRFixPack.Register(FIX_ID, {
	title = "Universal Depots built before Seeds research get their Seeds toggle when Seeds is unlocked",
	apply = function()
		-- Checked on the classes that DECLARE the methods (the F64 lesson):
		-- RebuildInfopanel is declared on UniversalStorageDepotBase (:398).
		return SMRFixPack.Require(FIX_ID, {
			{ global = "GroupResourcesForIP" },
			{ global = "AllMapsForEach" },
			{ global = "IsKindOf" },
			{ global = "IsValid" },
			{ class = "UniversalStorageDepotBase", method = "RebuildInfopanel" },
		})
	end,
})
