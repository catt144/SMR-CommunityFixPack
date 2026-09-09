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

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Buildings/Track.lua TrackBase:BreakTrackElement sha256=22aa2dbf058fb8f0b340d46dcddb73bf57fa46cd3c5518f59271215d23e4cac7
--   (Lua/Buildings/Track.lua:623-658 at pin time)
--   ⚠️ NO DEFECT LINE FOR THIS TARGET, deliberately: the defect is the ABSENCE
--   of node_idx among the parameters copied onto the repair site, and a regex
--   matches what is present (FIX_POLICY §2b). The body hash is the watch here;
--   the consequence is stated against the sort below
-- SRC: Lua/Buildings/TrackElement.lua TrackGridElement:DemolishAndSplitTrack sha256=7466b9403e6a3b27d12702a8825a61bfcdd2674c9bb6b0289c255cbc0b987c0e
--   (Lua/Buildings/TrackElement.lua:467-618 at pin time)
-- DEFECT: a\.node_idx < b\.node_idx
--   `false < number` raises once the un-stamped repair site is in the list

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
