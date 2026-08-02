-- F96: the St. Elmo's Fire sinkhole is the only mystery set-piece in the game a
-- meteor can destroy.
--
-- Defect: Sinkhole carries neither `indestructible` nor
-- `disasters_strike_immunity` (Lua\BuildingTemplate\Sinkhole.generated.lua:1-24 —
-- the template sets can_demolish = false, use_demolished_state = false,
-- count_as_building = false, and no destruction immunity at all). A large
-- meteor's query and filter both pass it (Meteors.lua:405-409, :393-399), the
-- building branch excludes only Dome and ConstructionSite (:817-825), and
-- DestroyBuildingImmediate's ONLY guard is the flag it does not have
-- (Building.lua:1371-1374) -> DoneObject (Demolishable.lua:132-141).
--
-- Intent tell (sibling contradiction, and it is the most lopsided one in this
-- tracker): every other mystery set-piece carries indestructible = true —
-- Crystals big and small, BlackCubeMonolith, MirrorSphereBuilding, CaveOfWonders,
-- JumboCave and its ReinforcementStructure, ArkPod, MartianAssembly and its Fake,
-- BottomlessPit, AncientArtifact, DragonRocket, DropPod. And the property's own
-- help text names the case: "Specify if the building can be destroyed at all (by
-- demolishing, by explosions, BY METEORS, etc)" (Building.lua:209). Sinkhole is
-- the omission, not the rule.
--
-- Reachability R2 — conditional: the St. Elmo's Fire mystery running, meteors
-- enabled (the default), and a LARGE meteor landing on the sinkhole's hex. No
-- mod, no console, no exotic state, but a specific coincidence.
--
-- ⚠️ WHAT THIS FIX DOES NOT CLAIM. The soft-lock is LOCATED, NOT PROVEN. The best
-- candidate is Mystery 11.generated.lua:146 — PlaceResourceStockpile_Delayed(
-- _sinkholePos, _sinkhole:GetMap(), "Polymers", …), an unguarded method call on a
-- persisted register inside the reward branch. Whether :GetMap() on a destroyed
-- object raises or merely yields nil is engine behaviour with no body in Src, and
-- this project has seen the nil outcome before (F44's dead-element seed). The
-- honest statement is: the reward branch touches an object that may no longer
-- exist, with no IsValid guard. The defect claim does not depend on it — a
-- set-piece the game uniformly protects is unprotected here, and the player can
-- lose it to a disaster.
--
-- Patch approach: FIX_POLICY §1.1 — a data/preset patch, the flag the rest of the
-- game already uses on set-pieces. Installed through SMRFixPack.DataPatch (the
-- F87 rule; a plain OnMsg.DataLoaded is dead on the enable path).
--
-- ⭐ SIDE EFFECTS WERE ENUMERATED, and the flag has exactly ONE on this template.
-- All consumers of `indestructible` in Lua\ were listed:
--   * Building.lua:1372 — DestroyBuildingImmediate's guard. THIS IS THE ONE WE WANT.
--   * Building.lua:888  — the demolish predicate, `self.can_demolish and … and not
--     self.indestructible`. Sinkhole already has can_demolish = false; NO CHANGE.
--   * Building.lua:1458 — gated on UseDemolishedState(). Sinkhole sets
--     use_demolished_state = false; NO CHANGE.
--   * Crystals.lua:584, Building.lua:1814 — runtime CLEARS of the flag, on other
--     objects; unaffected.
-- So the patch changes precisely one behaviour: a meteor can no longer delete the
-- sinkhole. That is the whole defect and nothing else.
--
-- WHERE THE WRITE GOES, and why it is two places rather than one:
--   * the CLASS table is the load-bearing one. DestroyBuildingImmediate reads
--     `bld.indestructible` on the INSTANCE, and an instance has no own field for
--     it (the template never sets one), so it falls through to the class default.
--     That is what reaches objects already placed in a save with no sweep at all.
--     After flattening the class global IS the flattened class (classes.lua:1085
--     rebinds _G[name] to classes[name]), and our pass runs from ClassesBuilt.
--   * BuildingTemplates.Sinkhole is belt: it is a thin proxy —
--     `setmetatable({ template_name = id }, g_Classes[id])`, Building.lua:2566 —
--     rebuilt on every ClassesBuilt/DataChanged, so it already inherits the
--     corrected class value. Writing it too costs one assignment and keeps any
--     template-side reader honest even if the proxy shape changes.
--
-- Note on the objection that a flag change "alters vanilla data rather than
-- patching a method": under FIX_POLICY §1 that is the PREFERRED direction, not a
-- concern. A preset patch is rung 1 precisely because other mods then see the
-- corrected value, and it puts nothing of ours in the save. The alternative — a
-- wrapper on the meteor path — would be strictly worse on every axis and would
-- have to re-decide, in our code, a question vanilla already answers with a flag.
--
-- §3a: nothing enters the save. One boolean on a class table and one on a preset
-- proxy. No thread, no persisted field, no wrapper frame.

local FIX_ID = "SinkholeIndestructible"
local CLASS_ID = "Sinkhole"

local log = SMRFixPack.Log

local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "BuildingTemplate",
	pass = function(ctx)
		-- After ClassesBuilt the class global is the flattened class itself; before
		-- it, this pass does not run at all (the runner's own gate).
		local classes = rawget(_G, "g_Classes")
		local C = (type(classes) == "table" and classes[CLASS_ID]) or rawget(_G, CLASS_ID)
		if type(C) ~= "table" then
			if ctx.data_loaded then
				ctx.patched = true
				ctx.latch("the " .. CLASS_ID .. " class no longer exists (game update changed it?)",
					CLASS_ID .. " class not found")
			end
			return
		end

		local templates = rawget(_G, "BuildingTemplates")
		local template = type(templates) == "table" and templates[CLASS_ID] or nil

		local changed = false
		if not C.indestructible then
			C.indestructible = true
			changed = true
		end
		-- Belt: the proxy inherits from the class, so this is normally already true.
		if type(template) == "table" and not rawget(template, "indestructible") then
			template.indestructible = true
		end
		ctx.patched = true

		if changed then
			ctx.ever_changed = true
			-- heals ONLY an "inactive" mislabel, never "disabled" (audit A1)
			ctx.heal()
			log("%s: the St. Elmo's Fire sinkhole is now indestructible, like every other mystery set-piece", FIX_ID)
		elseif ctx.ever_changed then
			-- nothing left to change on the DataChanged(false) re-fire is SUCCESS
			-- (the B3 lesson — see SMRFixPack.DataPatch)
			return
		else
			ctx.latch("the shipped Sinkhole is already indestructible", nil, "benign")
		end
	end,
})

SMRFixPack.Register(FIX_ID, {
	title = "A meteor can no longer destroy the St. Elmo's Fire sinkhole",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			-- the classdef exists from game load; the flag itself is checked in the
			-- pass, once the classes are flattened
			{ class = CLASS_ID },
			-- the guard this fix exists to satisfy
			{ global = "DestroyBuildingImmediate" },
		})
		if err then return err end
		patch()   -- no-op at apply time (F87); the runner fires itself once
		          -- the classes are built AND the presets are loaded
	end,
})
