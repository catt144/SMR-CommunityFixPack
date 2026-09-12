-- C88: the Building Codes laws skip prefab-deployed buildings, which their own
-- descriptions do not mention.
--
-- ⚖️ A PARADOX DEVELOPER ASKED US TO CARRY THIS. ivanassen, in the reporter's Steam
-- thread, 2026-09-11: "Excluding prefabs is wrong, and will be fixed in the next
-- patch - until then, please include it in your mod." So the exemption is a
-- confirmed defect by the game's own developers. Entry: bugs/C88.md; owner's shape
-- ruling: checklist 150 (b), option 1 — BOTH laws apply to prefab buildings,
-- exactly as their text says and as the developers will ship it.
--
-- THE DEFECT (SOURCE, game 1.1.0.403908). Both laws apply their maintenance change
-- in a ConstructionComplete MsgReaction that opens by discarding prefabs:
--   Policy_BuildingCodesLax    Data/LawDef/LawDef-Efficiency.lua:696-706,
--                              maintenance_change +50 (:687-690), exit at :700
--   Policy_BuildingCodesStrict Data/LawDef/LawDef-Efficiency.lua:904-914,
--                              maintenance_change -30 (:895-898), exit at :908
-- Each then reads ActiveLaws[self.id], requires IsKindOf(bld, "RequiresMaintenance"),
-- and calls bld:SetModifier("maintenance_resource_amount", self.id, 0,
-- self:GetParameterValue("maintenance_change"), self.display_name). The flag is
-- `local from_prefab = self.prefab` (Lua/Buildings/ConstructionSite.lua:1729),
-- passed as Msg("ConstructionComplete", bld, dome, from_prefab) (:1786) and declared
-- in Data/MsgDef.lua:280. Neither description mentions prefabs (:692, :900).
-- ⇒ Under Strict a prefab building misses the promised 30% LESS maintenance (a loss
-- against the law's text); under Lax it dodges the 50% MORE (a gain against it).
-- Both are corrected, because the owner ruled the laws should mean what they say.
--
-- Patch approach: an ADDITIVE HANDLER (FIX_POLICY §1 technique 2), which is what
-- the registration semantics force. A preset's handlers are registered BY FUNCTION
-- REFERENCE: RegisterMsgReactions walks self.msg_reactions and calls
-- RegisterMsgReaction(self, reaction.Event, reaction.Handler)
-- (CommonLua/Reactions.lua:130-137), which appends the instance and the handler into
-- MsgReactions[event_id] (:469-479). ⇒ editing
-- LawDefs.Policy_BuildingCodesStrict.msg_reactions[1].Handler after registration
-- changes NOTHING — the old reference is already in the dispatch table — and
-- re-registering means ReloadMsgReactions(), which clears and rebuilds the table for
-- every preset in the game. Far too wide for this defect, and the owner was not
-- asked to accept it. Vanilla's handler is meanwhile a VERIFIED NO-OP for exactly
-- the case we care about (it returns at :700/:908 before doing anything when
-- from_prefab is true), which is the precise shape §1's technique-2 note describes.
--
-- ⭐ IT DEGRADES TO NOTHING THE DAY PARADOX SHIPS THEIR FIX, and that is why the
-- modifier carries THE LAW'S OWN ID rather than one of ours (owner ruling, ck150).
-- Modifiable:SetModifier is keyed by (id, prop): it finds an existing modifier by id
-- and, when the amounts are unchanged, takes the `amount_change ~= 0 or
-- percent_change ~= 0` branch and does nothing at all (Lua/Modifiers.lua:181-204).
-- Both handlers write the same id, prop and value, so whichever runs second is a
-- no-op and exactly ONE modifier exists in either order.
-- ⚠️ THE COST of the law's id, stated because it is real: our modifier is then
-- indistinguishable from vanilla's, so the uninstall/save-rescue path (D13) cannot
-- identify it as ours. The owner accepted that in exchange for repeal and the
-- shipped savegame fixup treating it as the game's own — the alternative, our own
-- id, would STACK with vanilla's once their patch lands (two ids, double effect),
-- which is a player-visible harm and the same failure shape as F-2.
--
-- ⛔ BUILDINGS ALREADY STANDING CANNOT BE REPAIRED, and no heuristic is attempted.
-- `from_prefab` occurs in exactly eight places in the whole tree (the two handlers,
-- MsgDef.lua:280, ConstructionSite.lua:1729/:1786, Data/Trigger.lua:11) and NOTHING
-- stores it on the finished building, so a building already up cannot be identified
-- as prefab-deployed. Guessing from shape, template or missing construction cost
-- would silently change maintenance on buildings the law never touched. ⇒ This fix
-- applies to buildings COMPLETED AFTER IT IS INSTALLED. That is a scope statement,
-- and it is stated on every surface.
--
-- ⚠️ VANILLA LEAKS THIS MODIFIER ON REPEAL, and we add no new leak shape. Each law's
-- COST half is a LawEffectModifyLabel, which has an OnStop and is reverted; the
-- MAINTENANCE half is this MsgReaction, and nothing reverts it. Every
-- OnMsg.LawDeactivated handler in the tree is accounted for — Laws.lua:463
-- (RecalcApprovalOnLawChange, approval only), Laws.lua:393 / :884 (debug asserts),
-- Legislature.lua:425 (governing-law and efficient-assembly only) — and none touches
-- maintenance_resource_amount. The only clear-down that exists is the one-shot
-- SavegameFixups.RemoveRepealedBuildingCodesMaintenance (Lua/Factions/Laws.lua:465-473).
-- Filed as bugs/C91; because our modifier carries the LAW'S id, it leaks exactly as
-- vanilla's does and is cleared by exactly the same fixup — one more building in an
-- existing leak, never a new kind of leak.
--
-- FIX_POLICY §3a: layer 1 — leave no trace. One synchronous OnMsg handler. No
-- thread, no persisted field of ours, no new GameVar, no function value stored
-- anywhere. The only write is a modifier under the GAME'S OWN id, which the game
-- already writes for every non-prefab building under that law. SAVE FOOTPRINT: none
-- of ours (see the C91 note above for vanilla's).
--
-- BRANCH GUARD (FIX_POLICY §2a) — a real behaviour probe, and no version check.
-- The probe CALLS the shipped handler with from_prefab = true. That is safe and
-- complete: the shipped body's first statement is `if from_prefab then return end`,
-- so the call is one comparison and a return — no global read, no allocation, no
-- yield. And it DISCRIMINATES, because `ActiveLaws` is a GameVar
-- (Lua/Factions/Legislature.lua:1) and so carries no law table while no game is
-- loaded:
--   * shipped shape -> returns at the first line, never reaching ActiveLaws: clean.
--   * their patch   -> the exit is gone, so it reaches ActiveLaws[self.id], indexes a
--                      non-table and THROWS. A throw is a decline, so the module
--                      stands itself down and logs a RETIRE candidate.
--
-- ⛔ TWO PLACES THIS ALMOST WENT WRONG, both corrected, both covered by desk legs:
--   1. `GameVar(name, value)` rawsets the global to **false**, not nil, and
--      OnMsg.DoneGame sets it back to false (CommonLua/Core/lib.lua:1061-1093). A
--      "no game loaded" test written as `~= nil` is TRUE at the menu, which would have
--      made this module decline on every single boot. The test is `nil or false`.
--   2. The guard does NOT run at apply time. A preset GlobalMap is present but EMPTY
--      before DataLoaded and mod code always loads first on a cold boot (the F75
--      lesson), so capturing these handlers in apply() would have found nothing and
--      declined on every cold boot while working on the enable path. The guard runs
--      from SMRFixPack.OnDataReady, which fires once the classes are built AND the
--      presets are loaded, on all three paths, and is idempotent.
-- apply() therefore requires only what a game update could remove and that is present
-- at the menu; `ActiveLaws` is deliberately NOT a Require entry (the F110 rule).
--
-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-12 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about the
-- shipped tree, not a clearance: re-pin them deliberately when a target moves, never
-- to silence a BODY-CHANGED.
-- ⭐ THE DEFECT PIN IS THIS MODULE'S RETIREMENT SIGNAL: `bodycheck` prints
-- DEFECT-GONE the day Paradox's patch removes the prefab exit, which is the day this
-- module should be deleted rather than merely standing itself down.
-- SRC: none -- an additive OnMsg handler beside a preset's MsgReaction -- no function body of ours replaces a shipped one
-- DEFECT@Data/LawDef/LawDef-Efficiency.lua: if from_prefab then return end
--   both Building Codes handlers discard prefab-deployed buildings before applying
--   the maintenance change their descriptions promise (two occurrences, Lax + Strict)

local FIX_ID = "BuildingCodesPrefab"

-- Both laws share policy = "BuildingCodes", so at most one is ever active; the
-- ActiveLaws test below is what decides, exactly as vanilla's does.
local LAW_IDS = { "Policy_BuildingCodesLax", "Policy_BuildingCodesStrict" }
local PROP = "maintenance_resource_amount"
local PARAM = "maintenance_change"

-- nil = not decided yet, true = the shipped shape is the one we correct,
-- string = declined (the reason). The handler refuses to act until it is true.
local guard = nil

-- ⛔ NO GAME LOADED READS AS `false`, NOT nil. `GameVar(name, value)` rawsets the
-- global to **false** at declaration and OnMsg.DoneGame sets it back to false
-- (CommonLua/Core/lib.lua:1061-1093), so at the menu `ActiveLaws` is `false`. A test
-- for `~= nil` would be true there — that mistake would have made this module
-- decline on every boot, and the desk harness models `false` for exactly that reason.
local function no_game_loaded()
	local laws = rawget(_G, "ActiveLaws")
	return laws == nil or laws == false
end

-- Mirrors vanilla's three conditions per law, in vanilla's order, and reads the
-- percentage from the preset so a balance change or another mod's edit is respected.
-- ⛔ Never hard-code 50 / -30.
local function apply_to_prefab(bld)
	local laws = rawget(_G, "ActiveLaws")
	if type(laws) ~= "table" then return 0 end          -- no game loaded
	local defs = rawget(_G, "LawDefs")
	if type(defs) ~= "table" then return 0 end
	if not IsKindOf(bld, "RequiresMaintenance") then return 0 end
	local applied = 0
	for _, law_id in ipairs(LAW_IDS) do
		if laws[law_id] then
			local law = defs[law_id]
			if type(law) == "table" and type(law.GetParameterValue) == "function" then
				local percent = law:GetParameterValue(PARAM)
				if type(percent) == "number" and percent ~= 0 then
					bld:SetModifier(PROP, law_id, 0, percent, law.display_name)
					applied = applied + 1
				end
			end
		end
	end
	return applied
end

-- The shipped ConstructionComplete handler of each law, or nil.
local function shipped_handlers()
	local defs = rawget(_G, "LawDefs")
	if type(defs) ~= "table" then return nil end
	local found = {}
	for _, law_id in ipairs(LAW_IDS) do
		local law = defs[law_id]
		local reactions = type(law) == "table" and law.msg_reactions
		if type(reactions) ~= "table" then return nil end
		for _, reaction in ipairs(reactions) do
			if type(reaction) == "table" and reaction.Event == "ConstructionComplete"
				and type(reaction.Handler) == "function"
			then
				found[law_id] = reaction.Handler
			end
		end
		if not found[law_id] then return nil end
	end
	return found
end

-- ⛔ THE BRANCH GUARD RUNS WHERE THE PRESETS EXIST, NOT AT APPLY TIME (the F75 lesson,
-- FIX_POLICY §2). A preset GlobalMap is present but EMPTY before DataLoaded, and mod
-- code always loads first on a cold boot — so capturing these handlers in apply()
-- would have found nothing and declined this module on every cold boot, while working
-- on the enable path. SMRFixPack.OnDataReady fires once the classes are built AND the
-- presets are loaded, on the cold-boot, enable and reload paths alike, and it may fire
-- several times, so this is idempotent.
local function check_shape()
	if guard ~= nil then return end            -- decided once
	local handlers = shipped_handlers()
	if not handlers then
		-- OnDataReady means DataLoaded has fired, so absence is meaningful here.
		guard = "the Building Codes laws no longer carry a ConstructionComplete handler"
	elseif not no_game_loaded() then
		-- The probe below discriminates only while no game is loaded (see the header).
		-- Stay undecided and let a later firing settle it rather than bank a verdict
		-- the probe cannot support. In practice the first firing is always at the menu.
		return
	else
		-- BEHAVIOUR PROBE, run by hand here rather than through Require's `probe`
		-- form because this is not apply time. Same contract: error-trapped, and ONLY
		-- a clean run with nothing written counts as the shipped shape.
		-- Stub contract: the shipped body's first statement is
		-- `if from_prefab then return end`, so with from_prefab = true the call reads
		-- nothing, allocates nothing and cannot yield. `self` needs only an id for the
		-- path that must NOT be taken; the stub records any SetModifier call.
		-- The discriminator is `ActiveLaws` being `false` with no game loaded: their
		-- patched handler reaches `ActiveLaws[self.id]`, indexes a boolean and THROWS.
		local wrote = 0
		local stub = {
			id = "SMRFixPackProbeNotALaw",
			display_name = "",
			GetParameterValue = function() return 0 end,
			SetModifier = function() wrote = wrote + 1 end,
		}
		local ok = true
		for _, law_id in ipairs(LAW_IDS) do
			local called = pcall(handlers[law_id], stub, stub, nil, true)
			ok = ok and called
		end
		if ok and wrote == 0 then
			guard = true
		else
			guard = "the Building Codes handlers no longer skip prefab buildings "
				.. "(C88 repaired by the game?)"
		end
	end

	if guard ~= true then
		local entry = SMRFixPack.fixes[FIX_ID]
		-- Never overwrite the user veto or a real error (FIX_POLICY §2, the A1 guard).
		if entry and entry.status == "active" then
			entry.status = "inactive"
			entry.detail = guard
		end
		SMRFixPack.Log("%s: inactive (%s — already correct, RETIRE candidate)", FIX_ID, guard)
	end
end

SMRFixPack.OnDataReady(check_shape)

-- Additive handler. Costs a live game nothing on the ordinary path: one truthiness
-- test and a return for every non-prefab building completed.
OnMsg.ConstructionComplete = SMRFixPack.WhenActive(FIX_ID, function(bld, dome, from_prefab)
	if guard ~= true then return end
	if not from_prefab then return end
	if not IsValid(bld) then return end
	apply_to_prefab(bld)
end)

-- Exposed for the TestKit's behaviour probe and for the owner's attended A/B, so both
-- drive the real thing. Precedent SMRFixPack.Sanitizer (90_SaveSanitizer.lua:402);
-- SMRFixPack is a plain mod global that nothing persisted reaches.
SMRFixPack.BuildingCodesPrefab = {
	LawIds = LAW_IDS,
	Prop = PROP,
	Param = PARAM,
	ApplyToPrefab = apply_to_prefab,
	Guard = function() return guard end,
	CheckShape = check_shape,
	ShippedHandlers = shipped_handlers,
}

SMRFixPack.Register(FIX_ID, {
	title = "Building Codes applies to prefab-deployed buildings, as its description says",
	apply = function()
		-- ⛔ Only what a game UPDATE could remove AND that is present at the MENU
		-- (FIX_POLICY §2's F110 rule). The presets and the defect shape are checked by
		-- check_shape above, once they exist; `ActiveLaws` is a GameVar and is
		-- deliberately absent here, so it is not a Require entry.
		return SMRFixPack.Require(FIX_ID, {
			{ global = "IsKindOf" },
			{ global = "IsValid" },
			{ class = "Modifiable", method = "SetModifier" },
			{ class = "Modifiable", method = "FindModifier" },
		})
	end,
})
