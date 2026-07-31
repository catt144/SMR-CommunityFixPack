-- F45: A meteor-damaged track can't be salvaged at all — clicking Salvage does
-- nothing, forever.
--
-- Defect: when a meteor breaks a track piece, TrackBase:BreakTrackElement
-- (Lua\Buildings\Track.lua:618-659) copies the element's parameters onto the
-- repair construction site — direction, q, r, station, pillared, connections,
-- track_obj — but NOT node_idx, which therefore keeps its class default of
-- `false` (TrackElement.lua:164). Every salvage path then runs
--     table.sort(all_elements, function(a, b) return a.node_idx < b.node_idx end)
-- (TrackElement.lua:458-464) over a list that now contains the repair site, and
-- comparing `false < number` raises before a single element is deleted. The click
-- silently does nothing. This affects the salvage click, Ctrl+click mass salvage,
-- the infopanel Salvage button and clicking the repair site itself — matching the
-- "undeletable track" reports, including after a station is destroyed.
--
-- Patch approach: two parts, both minimal.
--  * chained post-wrapper on BreakTrackElement that stamps the repair site's
--    node_idx from the element it stands in for. New damage is born correct and
--    the vanilla sort works untouched, so other mods' salvage hooks keep working.
--  * a LoadGame sweep that stamps repair sites already sitting in the savegame —
--    without it, tracks broken before this mod was installed stay unsalvageable.
--    It only ever fills in a missing number, so it is safe to re-run and safe to
--    leave behind if the mod is removed.

SMRFixPack.Register("BrokenTrackSalvage", {
	title = "Meteor-damaged tracks can be salvaged again",
	apply = function()
		local err = SMRFixPack.Require("BrokenTrackSalvage", {
			{ class = "TrackBase", method = "BreakTrackElement" },
			-- content check: the fix only makes sense while the class default is
			-- still the broken `false`
			{ test = function()
				local E = rawget(_G, "TrackGridElement")
				return type(E) == "table" and E.node_idx == false
			  end,
			  reason = "TrackGridElement.node_idx no longer defaults to false (already fixed?)" },
		})
		if err then return err end
		local T = TrackBase

		local orig = T.BreakTrackElement
		function T:BreakTrackElement(element, ...)
			local cg = orig(self, element, ...)
			-- FIX (F45): the shipped params copy omits node_idx, leaving it false and
			-- breaking every salvage sort that touches this track.
			local site = element and element.broken
			if IsValid(site) and type(site.node_idx) ~= "number" and type(element.node_idx) == "number" then
				site.node_idx = element.node_idx
			end
			return cg
		end
	end,
})

-- Repair sites created before this fix was installed still carry node_idx = false.
OnMsg.LoadGame = SMRFixPack.WhenActive("BrokenTrackSalvage", function()
	if type(rawget(_G, "AllMapsForEach")) ~= "function" then return end
	local stamped = 0
	AllMapsForEach(true, "TrackGridElement", function(site)
		if site.is_construction_site and IsValid(site.broken)
				and type(site.node_idx) ~= "number" and type(site.broken.node_idx) == "number" then
			site.node_idx = site.broken.node_idx
			stamped = stamped + 1
		end
	end)
	if stamped > 0 then
		SMRFixPack.Log("BrokenTrackSalvage: repaired %d unsalvageable track repair site(s)", stamped)
	end
end)
