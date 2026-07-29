-- F08: Tourist star-rating applicant bonus is inverted.
--
-- Defect: HolidayRating:RewardApplicants (Lua\HolidayRating.lua:77) rolls
--     if Random(0,100) > (self.rewards[rating].bonus_chance) then
-- granting the bonus applicant with probability ~(100 - bonus_chance). The rewards
-- table (:2-11) is a monotonic progression (0+40%, 0+80%, 1+25%, 1+50%, 1+75%, 2,
-- 2+50% by star rating); as shipped, a 2-star departure yields FEWER applicants on
-- average than a 1-star. The codebase idiom everywhere else is
-- `Random(100) >= chance then return` (MonumentOfMarsLiberty.lua:21, ToxicPool.lua:182).
-- Runs on every tourist departure (RocketBase.lua:818, UniversalRocket.lua:2014).
--
-- Patch approach: replacement of the one small method (copy of
-- Lua\HolidayRating.lua:73-91, shipped Src, game 1.0.7.396349); change marked -- FIX.

SMRFixPack.Register("TouristApplicants", {
	title = "Higher tourist ratings now correctly give more bonus applicants (roll was inverted)",
	apply = function()
		if type(HolidayRating) ~= "table" or type(HolidayRating.RewardApplicants) ~= "function" then
			return "HolidayRating.RewardApplicants not found (game update changed it?)"
		end

		function HolidayRating:RewardApplicants(rating, tourist)
			local applicants = 0
			applicants = self.rewards[rating].fixed_applicants

			if Random(0, 100) < (self.rewards[rating].bonus_chance) then -- FIX: was `>`, inverting the chance
				applicants = applicants + self.rewards[rating].bonus_applicants
			end

			if tourist.traits.Saint then
				applicants = applicants * g_Consts.HolidaySaintMultiplier
			end
			for i = 1, applicants do
				local applicant = GenerateApplicant(false, tourist.city)
				if applicant then
					MakeTourist(applicant)
				end
			end
			return applicants
		end
	end,
})
