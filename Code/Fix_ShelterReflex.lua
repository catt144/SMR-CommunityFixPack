-- F73: Asteroid colonists idle outdoors in vacuum and bleed health; nothing
-- ever tells them to take shelter.
--
-- Two linked defects, both patched here.
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
-- (a) replace the small mixin method so the score is judged as if life support
--     were up — i.e. exactly the verdict the shipped code reaches when the
--     habitat is powered. It never accepts a colonist the trait filter rejects.
-- (b) PRE-wrapper on Colonist:Idle (a post-wrapper is impossible: Idle ends in
--     SetCommand, which kills the calling thread). Once a colonist has been
--     outside in a non-breathable atmosphere for half the oxygen budget and has a
--     working residence to go to, send them to Rest — which enters the residence.
--     Colonists with nowhere to go are left alone, and a one-hour throttle keeps
--     a failed entry from re-triggering every second.

SMRFixPack.Register("ShelterReflex", {
	title = "Asteroid colonists take shelter before suffocating, and keep their habitat through power blips",
	apply = function()
		local applied = {}

		-- (a) habitat suitability must not hinge on a momentary life-support gap
		local AR = rawget(_G, "MicroGHabitatAutoResolve")
		if type(AR) == "table" and type(AR.IsSuitable) == "function"
				and type(rawget(_G, "Community")) == "table" and type(Community.HasLifeSupport) == "function" then
			function AR:IsSuitable(colonist)
				-- FIX (F73a): GetScoreFor adds 100 only while HasLifeSupport(); add it
				-- back when it is down so a power/air blip cannot evict the residents.
				return self:GetScoreFor(colonist.traits) + (self:HasLifeSupport() and 0 or 100) > 0
			end
			applied[#applied + 1] = "habitat suitability"
		end

		-- (b) seek shelter before the oxygen timer runs out
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
			applied[#applied + 1] = "shelter reflex"
		end

		if #applied == 0 then
			return "neither MicroGHabitatAutoResolve.IsSuitable nor Colonist.Idle found (game update changed them?)"
		end
	end,
})
