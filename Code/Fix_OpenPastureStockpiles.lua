-- C93: opening domes changes Outside Ranches to OpenPasture_Open, whose entity
-- lacks Resourcepile7..9 even though OpenPastureBase now declares nine shared
-- stockpile spots. The three children lose their anchors and become unreachable
-- Origin piles while retaining their resources and supply requests.
--
-- Keep this one building on the closed OpenPasture entity. Open-air life-support
-- changes are global and independent of the skin; only the ranch's open visual is
-- suppressed. Existing affected saves are repaired by changing the entity back
-- and reattaching only piles that remain invalid. No resource amount, request,
-- controller list, producer cap, or persisted field is rewritten.
--
-- CalcOpenAirEntity callers, shipped 1.1.0.403908: OpenAirBuilding GameInit and
-- CalcOpenAirSkin; Dome:CalcOpenAirSkin; the ordinary/open-city construction
-- cursors; build-menu skin selection; and the infopanel. Every foreign receiver
-- passes straight through before inspection. For OpenPastureBase, returning the
-- closed entity in both positions makes all callers agree and also covers ranches
-- constructed after the law is active.
--
-- SAVE FOOTPRINT (FIX_POLICY section 3a): layer 1. The wrapper and synchronous
-- load/reload sweep add no fields, GameVars, classes, threads, or saved callbacks.
-- A repaired save retains only vanilla objects on vanilla entity spots. Removing
-- the pack can therefore leave at most the closed ranch visual until vanilla next
-- changes its open-air state; no mod function or data is persisted.
--
-- Branch guard: inspect the entities themselves, not a version label. Apply only
-- when the closed entity has Resourcepile7..9 and the open entity does not, while
-- the class still declares the nine-spot list. A future asset correction declines.
--
-- SRC: Lua/Buildings/OpenAirBuilding.lua OpenAirBuilding:CalcOpenAirEntity sha256=981d464d9d5622b2910b88803877f9bb679e68faafe620f910a087a4d8d25a07
-- DEFECT: return entity \.\. "_Open",\s*entity
-- SRC: Lua/Units/Animals.lua L1108-1114 sha256=cf406af6af85dd23b0928651d82335394965eee19df93098cc23a928e5f659a5
-- DEFECT: "Resourcepile9"

local FIX_ID = "OpenPastureStockpiles"
local CLOSED_ENTITY = "OpenPasture"
local OPEN_ENTITY = "OpenPasture_Open"

local function unique_stockpiles(pasture)
	local piles, seen = {}, {}
	for _, producer in ipairs(pasture.producers or empty_table) do
		for _, pile in ipairs(producer.stockpiles or empty_table) do
			if IsValid(pile) and not seen[pile] then
				seen[pile] = true
				piles[#piles + 1] = pile
			end
		end
	end
	return piles
end

local function repair_pasture(pasture)
	if pasture:GetEntity() ~= OPEN_ENTITY then return 0 end

	local piles = unique_stockpiles(pasture)
	local invalid = {}
	for _, pile in ipairs(piles) do
		if pile:GetParent() == pasture and pile:GetAttachSpot() < 0 then
			invalid[#invalid + 1] = pile
		end
	end

	local _, palette = pasture:GetCurrentSkin()
	pasture:ChangeSkin(CLOSED_ENTITY, palette)

	-- ChangeEntity may preserve the old numeric anchors. Reattach only children
	-- that are still invalid after the closed entity and its spots are restored.
	local occupied = {}
	for _, pile in ipairs(piles) do
		if pile:GetParent() == pasture then
			local spot = pile:GetAttachSpot()
			if spot >= 0 then occupied[spot] = true end
		end
	end

	local targets = {}
	for i = 7, 9 do
		local first, last = pasture:GetSpotRange("idle", "Resourcepile" .. i)
		if first >= 0 and last >= first then
			for spot = first, last do
				if not occupied[spot] then targets[#targets + 1] = spot end
			end
		end
	end

	local repaired = 0
	local next_target = 1
	for _, pile in ipairs(invalid) do
		if IsValid(pile) and pile:GetParent() == pasture and pile:GetAttachSpot() < 0 then
			local spot = targets[next_target]
			if not spot then break end
			next_target = next_target + 1
			pile:Detach()
			pasture:Attach(pile, spot)
			pile:SetAttachOffset(0, 0, 0)
			if pile:GetAttachSpot() == spot then
				repaired = repaired + 1
			end
		end
	end
	return repaired
end

local function sweep(trigger)
	local each = rawget(_G, "AllMapsForEach")
	if type(each) ~= "function" then return end
	local ranches, piles = 0, 0
	each("map", "OpenPastureBase", function(pasture)
		if pasture:GetEntity() == OPEN_ENTITY then
			ranches = ranches + 1
			piles = piles + repair_pasture(pasture)
		end
	end)
	if ranches > 0 then
		SMRFixPack.Log("%s: restored %d open ranch(es), explicitly reattached %d pile(s) (%s)",
			FIX_ID, ranches, piles, trigger)
	end
end

OnMsg.LoadGame = SMRFixPack.WhenActive(FIX_ID, function() sweep("load") end)
OnMsg.ModsReloaded = SMRFixPack.WhenActive(FIX_ID, function() sweep("reload") end)

SMRFixPack.Register(FIX_ID, {
	title = "Outside Ranch stockpiles remain reachable after Open Domes",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "OpenAirBuilding", method = "CalcOpenAirEntity" },
			{ class = "OpenPastureBase" },
			{ global = "IsKindOf" },
			{ global = "IsValid" },
			{ global = "GetSpotRange" },
			{ global = "AllMapsForEach" },
			{ probe = function()
				local spots = OpenPastureBase.stockpile_spots1
				if type(spots) ~= "table" or spots[7] ~= "Resourcepile7"
					or spots[8] ~= "Resourcepile8" or spots[9] ~= "Resourcepile9"
				then
					return false
				end
				for i = 7, 9 do
					local name = "Resourcepile" .. i
					local closed_first, closed_last = GetSpotRange(CLOSED_ENTITY, "idle", name)
					local open_first = GetSpotRange(OPEN_ENTITY, "idle", name)
					if closed_first < 0 or closed_last < closed_first or open_first >= 0 then
						return false
					end
				end
				return true
			end,
			reason = "the Outside Ranch entity variants no longer have the nine-versus-six stockpile mismatch" },
		})
		if err then return err end

		local orig = OpenAirBuilding.CalcOpenAirEntity
		function OpenAirBuilding:CalcOpenAirEntity(entity)
			if not IsKindOf(self, "OpenPastureBase") then
				return orig(self, entity)
			end
			local open_entity, closed_entity = orig(self, entity)
			if open_entity == OPEN_ENTITY and closed_entity == CLOSED_ENTITY then
				return CLOSED_ENTITY, CLOSED_ENTITY
			end
			return open_entity, closed_entity
		end
	end,
})
