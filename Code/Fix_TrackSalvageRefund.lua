-- F47: salvaging a track refunds one construction group's worth of Metals no
-- matter how long the track is, and salvaging PART of a track refunds nothing
-- at all.
--
-- How a track is actually paid for (this is not what the tracker assumed, see
-- the "*Implemented differently*" note on the BUGS entry):
--   * Track hexes are built in construction GROUPS of at most
--     `const.ConstructiongGridElementsGroupSize` = 5 elements
--     (Lua\Tracks.lua:359, :426; _GameConst.lua:480). A new group is started
--     whenever the current one is full or the drag is not adjacent to it.
--   * The group's leader is charged for the whole group:
--     `ConstructionGroupLeader:GetConstructionCost` scales the per-element cost
--     by `construction_cost_multiplier` (ConstructionSite.lua:2328-2330), and
--     Tracks.lua:463 leaves it at 100 — one element's cost (200 Metals,
--     Data\BuildingTemplate\Track.lua:7) per group, not per hex.
--   * When the group completes, the leader stamps that spend onto exactly ONE
--     of the finished elements — the last one it completed:
--     `self:MarkSpentResources(last_completed)` with the comment "mark spent
--     resources in 1 building so refunds would be correct"
--     (ConstructionSite.lua:2479-2489). Every other member's own
--     MarkSpentResources is suppressed first (:2469), so no other element in
--     the group carries a stamp.
--
-- So a finished track carries one `construction_cost_at_completion` stamp per
-- construction group, each holding that group's real spend, spread over the
-- elements.
--
-- Defect: `TrackBase:GetRefundResources` (Lua\Buildings\Track.lua:286-307)
-- reads the stamp of a SINGLE element — `self.elements[#self.elements]` — and
-- refunds half of that. For a track of 5 hexes or fewer that is exactly right
-- (one group, and its stamp happens to be on the last element). For anything
-- longer, every group before the last one is simply not counted: a 30-hex track
-- costs six groups' worth and refunds one. The refund does not grow with the
-- track at all.
--
-- Second half: `TrackGridElement:DemolishAndSplitTrack`
-- (Lua\Buildings\TrackElement.lua:503-541) deletes the salvaged elements with a
-- bare `DoneObject(el)` in all three of its partial branches, so a partial
-- salvage refunds nothing whatsoever — contrast `PassageBase:OnDemolish`
-- (Lua\Passage.lua:1217-1222), which calls `e:ReturnResources()` on each
-- element before destroying it. Track elements are not Buildings
-- (TrackGridElement inherits `Demolishable`, TrackElement.lua:124-135) and
-- `Demolishable:GetRefundResources` is an empty stub (Demolishable.lua:160), so
-- nothing along that path can refund by itself.
--
-- Patch approach:
--   * Half A is a full replacement of `TrackBase:GetRefundResources` — the read
--     is mid-function and there is nothing to wrap. The shipped body is copied
--     byte-identical except the lines marked `-- FIX:`: the stamps of ALL
--     elements are summed instead of one element's being read. Because each
--     stamp is a real recorded expenditure, the sum is exactly what the player
--     paid; nothing is estimated and the refund can never exceed the shipped
--     50% of cost. When no element carries a positive stamp (Free Construction,
--     instantly-built tracks) the shipped fallback runs unchanged.
--   * Half B chain-wraps `TrackGridElement:Demolish` — the player-salvage entry
--     point (infopanel button via `ToggleDemolish`, TrackElement.lua:259-261;
--     the mass-salvage tool, Construction.lua:2911) — and refunds the stamps
--     carried by the elements the call actually destroyed. It observes the
--     result instead of predicting it, so it cannot drift from the three
--     branches' bookkeeping. Deliberately NOT wrapped: `DemolishAndSplitTrack`
--     itself, whose other caller (Construction.lua:1574, track erased from under
--     a newly placed station) is not a salvage.
--
-- No double refunds: when the whole track goes, the shipped path runs
-- `TrackBase:OnDemolish` -> `ReturnResources` -> the replaced
-- `GetRefundResources` above — and OnDemolish stamps `demolishing = true` on
-- the track first (Track.lua:250), a Lua-side field that survives the object's
-- destruction. Half B stands down exactly when that stamp is present. A stamp
-- lives on one element and dies with it, so each group's spend can be refunded
-- at most once over the whole life of the track.
--
-- QA F47 composition repairs (2026-07-26, both under-refunds found by the
-- wave-4/5 audit):
--   * The stand-down test used to be `IsValid(track) and elements is a table`,
--     which also stood down when the F44 trim EMPTIED the track — an emptied
--     track dies through CanDelete -> DoneObject (TrackElement.lua:203-205)
--     WITHOUT running OnDemolish, so nothing had refunded the trimmed stamps.
--     The `demolishing` stamp separates the two deaths; the map and drop
--     position are captured before the originals run, since both the element
--     and the track can be dead by the time the refund is placed.
--   * The construction-site early-return was broader than the repair-site
--     delegation it existed for: clicking a PLAIN under-construction element
--     still deletes a zone that can contain stamped COMPLETED elements
--     (DemolishAndSplitTrack sorts both arrays into one line), and the early
--     return threw those stamps away. Only the repair-site delegation
--     (TrackElement.lua:451-453) returns early now — its inner re-entry does
--     the accounting; a plain site falls through and is snapshotted. The
--     site's OWN spend is returned by the construction machinery and never
--     carries a completion stamp, so accounting the zone cannot double-refund.

SMRFixPack.Register("TrackSalvageRefund", {
	title = "Salvaging a track refunds what the whole track cost, not one hex",
	apply = function()
		local REFUND_MATHS = "Building.CalcRefundAmount/AddRefundResource not found (game update changed it?)"
		local STAMPING = "the construction-group stamping machinery is gone (game update changed it?)"
		local err = SMRFixPack.Require("TrackSalvageRefund", {
			{ class = "TrackBase", method = "GetRefundResources" },
			{ class = "TrackGridElement", method = "Demolish" },
			-- The refund maths live on Building; TrackBase only overrides the
			-- getter — check the DECLARING class (pre-flattening).
			{ class = "Building", method = "CalcRefundAmount", reason = REFUND_MATHS },
			{ class = "Building", method = "AddRefundResource", reason = REFUND_MATHS },
			-- The premise: one stamp per construction group, written by the leader.
			{ class = "ConstructionGroupLeader", method = "Complete", reason = STAMPING },
			{ class = "ConstructionSite", method = "MarkSpentResources", reason = STAMPING },
			{ global = "PlaceResourceStockpile_Delayed" },
		})
		if err then return err end
		local TB = TrackBase
		local TE = TrackGridElement
		local B = Building

		---- half A -------------------------------------------------------------
		-- Source: Lua\Buildings\Track.lua:286-307 (ModTools\Src, game 1.0.7.396349).
		function TB:GetRefundResources()
			local refund = {}
			if not self.elements or #self.elements == 0 then
				return refund
			end
			local element = self.elements[#self.elements]
			-- FIX: every construction group stamped one of its own elements, so the
			-- FIX: track's real cost is the sum of the stamps, not the last one.
			local total, stamped = {}, false
			for _, el in ipairs(self.elements) do
				local costs = el and el.construction_cost_at_completion
				if costs then
					for r_n, amount in pairs(costs) do
						if type(amount) == "number" and amount > 0 then
							total[r_n] = (total[r_n] or 0) + amount
							stamped = true
						end
					end
				end
			end
			if stamped then -- FIX: was `if element.construction_cost_at_completion then`
				for r_n, amount in pairs(total) do -- FIX: over the summed stamps
					local refund_amount = self:CalcRefundAmount(amount)
					self:AddRefundResource(refund, r_n, refund_amount)
				end
			else
				for _, resource in ipairs(GroupResourceIds.ConstructionResources) do
					local amount = UIColony.construction_cost:GetConstructionCost(element, resource)
					if 0 < amount then
						local refund_amount = self:CalcRefundAmount(amount)
						self:AddRefundResource(refund, resource, refund_amount)
					end
				end
			end
			return refund
		end

		---- half B -------------------------------------------------------------
		-- What did this call actually destroy, and what were those elements
		-- stamped with? Returns a list shaped like GetRefundResources' —
		-- { { resource = <id>, amount = <already halved> }, ... } — plus the
		-- position to drop it at. Pure bookkeeping, no side effects, so the probe
		-- can drive it directly.
		local function collect_refund(track, snapshot)
			local refund, pos, angle = {}, nil, nil
			if type(track) ~= "table" or type(snapshot) ~= "table" then
				return refund
			end
			local total, any = {}, false
			for _, entry in ipairs(snapshot) do
				if not IsValid(entry.el) then
					for r_n, amount in pairs(entry.costs or empty_table) do
						if type(amount) == "number" and amount > 0 then
							total[r_n] = (total[r_n] or 0) + amount
							any = true
							pos = pos or entry.pos
							angle = angle or entry.angle
						end
					end
				end
			end
			if not any then return refund end
			for r_n, amount in pairs(total) do
				track:AddRefundResource(refund, r_n, track:CalcRefundAmount(amount))
			end
			return refund, pos, angle
		end

		SMRFixPack.TrackSalvageRefund = { CollectRefund = collect_refund }

		local orig_demolish = TE.Demolish
		function TE:Demolish(mass_delete, ...)
			local track = self.track_obj
			-- A repair construction site delegates to its broken real element
			-- (TrackElement.lua:451-453), which re-enters this method; let the
			-- inner call do the accounting so a refund is never counted twice.
			-- A PLAIN construction site falls through (F47 composition repair):
			-- its zone can still delete stamped completed elements, its own
			-- spend is returned by the construction machinery, and it never
			-- carries a completion stamp — so snapshotting cannot double-count.
			if self.is_construction_site and IsValid(self.broken)
				and type(track) == "table" and type(track.elements) == "table"
				and table.find(track.elements, self.broken) then
				return orig_demolish(self, mass_delete, ...)
			end

			local snapshot, map
			if type(track) == "table" and type(track.elements) == "table" then
				-- captured now: both self and the track can be dead afterwards
				map = self:GetMap()
				for _, el in ipairs(track.elements) do
					local costs = el and el.construction_cost_at_completion
					if costs then
						-- copy the amounts out: the element is about to be destroyed
						local copy = {}
						for r_n, amount in pairs(costs) do copy[r_n] = amount end
						snapshot = snapshot or {}
						snapshot[#snapshot + 1] = {
							el = el,
							costs = copy,
							pos = el:GetVisualPos(),
							angle = el:GetAngle(),
						}
					end
				end
			end

			local res = orig_demolish(self, mass_delete, ...)

			if snapshot and not track.demolishing then
				-- TrackBase:OnDemolish stamps `demolishing` (Track.lua:250) before
				-- refunding the whole track through the replacement above — stand
				-- down then. Every OTHER outcome that destroyed stamped elements
				-- has not refunded them: trims, splits, and (F47 composition
				-- repair) a trim that emptied the track, whose death runs through
				-- CanDelete -> DoneObject (TrackElement.lua:203-205) with no
				-- OnDemolish — the old `IsValid(track)` test read that death as
				-- "already handled" and lost the refund.
				local ok, refund, pos, angle = pcall(collect_refund, track, snapshot)
				if ok and pos and map then
					for _, item in ipairs(refund) do
						PlaceResourceStockpile_Delayed(pos, map, item.resource, item.amount, angle or 0, true)
					end
				end
			end
			return res
		end
	end,
})
