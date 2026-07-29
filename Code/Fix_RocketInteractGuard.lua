-- F74: RC Transports can be ordered onto trade and refugee rockets, because the
-- guard that forbids it still names only the pre-Relaunched rocket classes.
--
-- Defect: RCTransport:CanInteractWithObject (Lua\Units\RCTransport.lua:338-385)
-- opens with
--     if IsKindOfClasses(obj, "TradeRocketBase", "RefugeeRocketBase") then return false end
-- (:341). In Relaunched those two classes are dead ends: trade and refugee
-- rockets are `UniversalTradeRocket` / `UniversalRefugeeRocket`, both generated
-- from BuildingTemplate with `__parents = { "UniversalRocketBase" }`
-- (Lua\BuildingTemplate\UniversalTradeRocket.generated.lua:4-5,
-- UniversalRefugeeRocket.generated.lua:4-5), while the legacy classes descend
-- the other branch of the tree — TradeRocketBase/RefugeeRocketBase ->
-- SupplyRocketBase -> RocketBase (RocketTrade.lua:1-2, RocketRefugee.lua:1-2,
-- SupplyRocket.lua:1-2). `UniversalRocketBase` is NOT a `RocketBase`
-- (UniversalRocket.lua:28-40), so the guard never matches.
--
-- It is dead in every Relaunched game, not just converted saves: new trade and
-- refugee rockets are placed as the Universal classes directly
-- (SA_Gameplay.lua:2788, :2929; ClassDef-Effects.generated.lua:154, :3134), and
-- old saves are converted to them on load (RocketCompatibility.lua:522, :964,
-- :1050).
--
-- This is a conversion slip, not a design change: five other rocket tests in the
-- very same file WERE updated to name both class families —
--   :314  IsKindOfClasses(depot, "SupplyRocketBase", "UniversalRocketBase")
--   :421  IsKindOfClasses(obj,   "SupplyRocketBase", "UniversalRocketBase")
--   :731  IsKindOfClasses(o,     "SupplyRocketBase", "UniversalRocketBase")
--   :916  IsRocketClass(d, "UniversalRocketBase")   (the compat shim,
--         RocketCompatibility.lua:1037-1046, which covers both families)
--   :1137 IsKindOfClasses(storage_depot, "SupplyRocketBase", "UniversalRocketBase")
-- Only :341 (and the two `IsKindOf(depot, "SupplyRocketBase")` reads at :265 and
-- :285 — see the BUGS entry, deliberately left alone) were missed.
--
-- Player-visible effect: the RC Transport's load/unload cursor now accepts a
-- trade or refugee rocket, so its cargo can be pushed into or pulled out of an
-- event rocket that has no player cargo bookkeeping. Matches the Relaunched
-- report "rival colony rockets glitch permanently if refilled from RC Transport"
-- (docs\archive\RESEARCH.md).
--
-- Patch approach: pre-wrapper (FIX_POLICY §1.4) on CanInteractWithObject that
-- restates the shipped rule for the Relaunched class names, then defers to the
-- original. A wrapper rather than a replacement because the guard is the very
-- first thing the function does — nothing shipped runs before it.
--
-- Two entry points are covered:
--   * CanInteractWithObject gates every interaction the player can start.
--     UnitDirectionModeDialog only stores an interaction target when it answers
--     truthy (UnitControl.lua:470-471, :488), and both the direct-order path
--     (:401) and the transport-route path (TransportRouteInteractionHandler.lua
--     :50) act on that stored target, so this alone closes the hole.
--   * InteractWithObject (:387-480) is wrapped too, belt-and-braces, so a mod or
--     a future call site that reaches the action without asking first still
--     cannot act on an event rocket.
-- Wrapping the class field also covers RCHarvester (:127, :139) and
-- RCConstructorBase (:353), which call RCTransport.CanInteractWithObject /
-- .InteractWithObject statically through the class table.

SMRFixPack.Register("RocketInteractGuard", {
	title = "RC Transports stay off trade and refugee rockets again",
	apply = function()
		local RC = rawget(_G, "RCTransport")
		if type(RC) ~= "table" or type(RC.CanInteractWithObject) ~= "function"
			or type(RC.InteractWithObject) ~= "function" then
			return "RCTransport.CanInteractWithObject/InteractWithObject not found (game update changed it?)"
		end
		if type(rawget(_G, "IsKindOfClasses")) ~= "function" then
			return "IsKindOfClasses not found (game update changed it?)"
		end

		-- Mod code loads before the classes are flattened, so IsKindOf* cannot be
		-- asked about a class yet — walk the classdefs' own __parents lists
		-- instead. Returns true when `name` has `ancestor` anywhere above it.
		local function descends_from(name, ancestor, depth)
			if name == ancestor then return true end
			if (depth or 0) > 8 then return false end
			local class = rawget(_G, name)
			local parents = type(class) == "table" and rawget(class, "__parents")
			if type(parents) ~= "table" then return false end
			for _, parent in ipairs(parents) do
				if type(parent) == "string" and descends_from(parent, ancestor, (depth or 0) + 1) then
					return true
				end
			end
			return false
		end

		-- Only the Relaunched classes the shipped guard misses. Kept as a list so
		-- the self-check below and the wrapper cannot drift apart.
		local BLOCKED, SHIPPED = {}, { "TradeRocketBase", "RefugeeRocketBase" }
		for _, pair in ipairs({
			{ "UniversalTradeRocket",   "TradeRocketBase" },
			{ "UniversalRefugeeRocket", "RefugeeRocketBase" },
		}) do
			local new_class, old_class = pair[1], pair[2]
			if type(rawget(_G, new_class)) ~= "table" then
				return new_class .. " does not exist (game update changed the rocket classes?)"
			end
			-- If the game ever re-parents these under the legacy classes, the
			-- shipped guard covers them and this fix has nothing to do.
			if not descends_from(new_class, old_class) then
				BLOCKED[#BLOCKED + 1] = new_class
			end
		end
		if #BLOCKED == 0 then
			return "the shipped guard already matches the Relaunched trade/refugee rockets"
		end

		local function is_event_rocket(obj)
			-- Re-check the shipped names as well: another mod may hand us a
			-- legacy-class rocket, and the shipped guard is behind us either way.
			return not not (obj and (IsKindOfClasses(obj, BLOCKED) or IsKindOfClasses(obj, SHIPPED)))
		end
		SMRFixPack.IsEventRocket = is_event_rocket   -- exposed for the probe

		-- (QA 2026-07-25) both wrappers pass varargs through: the UnitController
		-- call site hands a third argument (UnitControl.lua:649-653) that the
		-- shipped body ignores today — FIX_POLICY §1.4.
		local orig_can = RC.CanInteractWithObject
		function RC:CanInteractWithObject(obj, interaction_mode, ...)
			-- FIX (F74): the shipped guard at RCTransport.lua:341 names only the
			-- pre-Relaunched classes; restate it for the Universal ones.
			if is_event_rocket(obj) then return false end
			return orig_can(self, obj, interaction_mode, ...)
		end

		local orig_interact = RC.InteractWithObject
		function RC:InteractWithObject(obj, interaction_mode, ...)
			-- FIX (F74): same rule on the action itself (belt-and-braces).
			if is_event_rocket(obj) then return false end
			return orig_interact(self, obj, interaction_mode, ...)
		end
	end,
})
