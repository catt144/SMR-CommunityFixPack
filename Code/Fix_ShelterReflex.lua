-- F73: Asteroid colonists idle outdoors in vacuum and bleed health; nothing
-- ever tells them to take shelter.
--
-- SRC: Lua/Units/Colonist.lua Colonist:Idle sha256=184e7e2d23cc0bdeaa254cc312781e1181126e9e1892a332b4f28dc11d6114b9
-- DEFECT: self:SetCommand\("Roam"\)
--
-- ⚠️ NAMED-ABSENCE LIMIT, per FIX_POLICY §2b. Half (b)'s defect is a MISSING
-- branch — the shipped Idle has no seek-shelter case at all — and a regex
-- matches what is present. The DEFECT: above therefore states the tail this
-- pre-wrapper runs in FRONT of, so that vanilla restructuring Idle reads as
-- BODY-CHANGED and vanilla ADDING a shelter branch does NOT read as
-- DEFECT-GONE. This module is watched for class (b), and for nothing else.
--
-- Two linked defects. ⛔ HALF (a) WAS DELETED ON 1.1.0 — see the 1.1.0 section
-- at the bottom of this header. Only half (b) is patched here now.
--
-- (a) A momentary life-support gap costs a habitat all its residents.
--     MicroGHabitatAutoResolve:IsSuitable (Lua\Buildings\MicroGHabitat.lua:154-156)
--     is `self:GetScoreFor(colonist.traits) > 0`, and Community:GetScoreFor
--     (Community.lua:367-393) contributes its entire 100-point base ONLY when
--     HasLifeSupport() is true (:396-398 — water plus breathable air or
--     power+air). With a default trait filter the rest of the score is 0, so one
--     tick without power or air makes the habitat "unsuitable", the colonist's
--     residence is dropped, and it is never re-assigned while the blip lasts.
--
-- (b) Nothing shelters a colonist that ends up with no residence.
--     Colonist:Roam (Colonist.lua:1186-1205) only walks them INSIDE when
--     dome == residence; otherwise they mill around outdoors. Colonist:Idle
--     (:1769-1936) has branches for hunger, medical care, panic and darkness but
--     none for the oxygen timer — suffocation merely applies damage
--     (StatusEffects.lua:140-160, Colonist.lua:3728-3733). Workers are safe inside
--     the mine during their shift and die during the idle stretches next to it.
--
-- Patch approach:
-- (a) ⛔ DELETED ON 1.1.0 — see below. It replaced the small mixin method so the
--     score was judged as if life support were up.
-- (b) PRE-wrapper on Colonist:Idle (a post-wrapper is impossible: Idle ends in
--     SetCommand, which kills the calling thread). Once a colonist has been
--     outside in a non-breathable atmosphere for half the oxygen budget and has a
--     working residence to go to, send them to Rest — which enters the residence.
--     Colonists with nowhere to go are left alone, and a one-hour throttle keeps
--     a failed entry from re-triggering every second.
--
-- ======================================================================
-- 1.1.0 (2026-09-08, hotfix2 link 03; re-verification F-3, VANILLA_FIX_QA §0)
-- ======================================================================
--
-- ⛔ HALF (a) IS GONE, AND IT WAS A THROW, NOT MERELY A NO-OP. The signature
-- changed under our replacement: MicroGHabitatAutoResolve:IsSuitable(colonist)
-- now calls self:GetScoreFor(COLONIST) (Lua/Buildings/MicroGHabitat.lua:173-175),
-- and Community:GetScoreFor reads colonist.traits ITSELF
-- (Lua/Buildings/Community.lua:442-445). Our body still handed it
-- `colonist.traits`, so inside GetScoreFor `traits.traits` is nil and
-- FilterObjectAttributes indexes obj_attributes[attrib] for every filter key
-- (Lua/Filter.lua:113-121) ⇒ a THROW on any asteroid habitat with a trait
-- filter. The default filter is `{}` (Community.lua:43), so it was silent until
-- a player set one.
--
-- ⚖️ WHY DELETION AND NOT REPAIR — a corrected call would still be wrong.
-- 1.1.0 turned "no life support" into a deliberate TIER, not a missing bonus:
-- CommunityEvalLifeSupport = 100 against CommunityEvalNoLifeSupport = -400
-- (Community.lua:436-437, read at :443), and the shipped help text states the
-- intent outright — the tier "must lose to any live community … yet stay small
-- enough for a must-have dome filter match (1000000) to override it, so the
-- player can still force colonists into an unpowered dome". Our +100 could not
-- lift -400 in any case, and FIX_POLICY §4 bars fighting a stated design.
--
-- ⚠️ THE COST OF DROPPING (a), NAMED: F73(a)'s blip-eviction comes BACK for
-- 1.1.0 players. An unpowered habitat still scores negative, ChooseResidence
-- still returns false (MicroGHabitat.lua:162-171) and the heavy update still
-- calls UpdateResidence (Colonist.lua:2339-2344), so a power/air blip still
-- costs the residents their home; they are re-homed on the next heavy update
-- once life support is back. That is now vanilla behaviour by design and we
-- leave it alone. It is a patch-note line, not a silent drop.
--
-- ✅ HALF (b) IS KEPT AND IS UNCHANGED. Every field it reads still exists on
-- 1.1.0 and was re-read this session: outside_start (Colonist.lua:94, :3015-3020),
-- g_Consts.OxygenMaxOutsideTime (__const.lua:1756), Colonist:Idle (:2212),
-- Colonist:Rest (:2572), IsDying (:2666).
-- ⛔ ck118 — WHY THIS MODULE NEEDS NO PROBE, said explicitly rather than left
-- implicit. Half (b) gains NO 1.1.0 body shape: it is a pre-wrapper that copies
-- nothing and reads only fields present on BOTH branches, so it is correct on
-- 1.0.7 and on 1.1.0 alike and there is nothing for a branch guard to decline.
-- The rule is that a module carrying a 1.1.0 body must decline on 1.0.7; this
-- one carries none. Half (b) was never the half that broke.

SMRFixPack.Register("ShelterReflex", {
	title = "Asteroid colonists take shelter before suffocating",
	apply = function()
		-- seek shelter before the oxygen timer runs out
		local C = rawget(_G, "Colonist")
		-- NB: g_Consts is a GameVar (Modifiers.lua:427) and does not exist yet while
		-- mod code loads, so the oxygen budget is read inside the wrapper, not here.
		if type(C) == "table" and type(C.Idle) == "function"
				and type(rawget(_G, "GetAtmosphereBreathable")) == "function" then
			local orig_idle = C.Idle
			function C:Idle(...)
				-- FIX (F73b): the shipped Idle has no seek-shelter branch at all.
				local outside_start = self.outside_start
				local max_outside = g_Consts and g_Consts.OxygenMaxOutsideTime
				if max_outside and outside_start and IsValid(self.residence) and self.residence.working
						and not self.transport_task and not self:IsDying() then
					local now = GameTime()
					local last_try = self.SMRFixPack_shelter_try
					if now - outside_start >= max_outside / 2
							and (not last_try or now - last_try >= const.HourDuration)
							and not GetAtmosphereBreathable(self:GetMap()) then
						self.SMRFixPack_shelter_try = now
						self:SetCommand("Rest") -- kills this thread; never returns
					end
				end
				return orig_idle(self, ...)
			end
		else
			-- ⚠️ Reworded 2026-09-08 with half (a): the old string named
			-- MicroGHabitatAutoResolve.IsSuitable, which this module no longer
			-- touches. Reason strings are otherwise preserved byte-for-byte
			-- (00_Core.lua) — this one was changed because it became FALSE, not
			-- to read better.
			return "Colonist.Idle or GetAtmosphereBreathable not found (game update changed them?)"
		end
	end,
})
