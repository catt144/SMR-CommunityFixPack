-- F20: a colonist's Morale tooltip credits a "+Comfort" bonus the game stopped
-- granting, so the listed effects do not add up to the Morale shown above them.
--
-- Defect: `Colonist:UpdateMorale` (`Lua\Units\Colonist.lua:3950-3969`) applies a
-- high-stat bonus for Health and Sanity, and a low-stat penalty for all three —
-- but the high-Comfort bonus is commented out, on purpose:
--     -- remove for comfort policy to work
--     --if self.stat_comfort >= high_stat_threshold then
--     --	new_value = new_value + high_stat_morale_effect
--     --end
--     if self.stat_comfort < low_stat_threshold then
--         new_value = new_value - low_stat_morale_effect
--     end
-- The tooltip built in `Colonist:UIStatUpdate` (`:2932`, Morale branch
-- `:2981-3008`) never got the same treatment. It walks `ColonistStatList`
-- (`:141`) and prints a row whenever `value < low or value >= high`, for every
-- stat alike, so a colonist with Comfort at or above the high threshold is told
-- they are getting a bonus that was never added.
--
-- Which side is wrong is not a judgement call: the comment states the removal
-- was deliberate and names the reason (the comfort policy). The tooltip is the
-- side that is out of date, so only the tooltip is changed — no Morale value
-- moves.
--
-- Patch approach: post-wrapper (FIX_POLICY §1.4) on `Colonist:UIStatUpdate`.
-- The shipped call installs `win.GetRolloverText`; the wrapper then wraps THAT
-- closure, so the shipped text builder still does all the work and every other
-- row — including the low-Comfort penalty, which IS applied — is produced by
-- shipped code exactly as before. It re-wraps on every update, so wrappers do
-- not stack.
--
-- Suppressing just the one row without copying ~130 lines of tooltip builder is
-- done by answering the single comparison it hinges on: for the duration of the
-- call the colonist carries an instance-level `GetProperty` that reports Comfort
-- as one below the high threshold when it is at or above it. That is the only
-- place `value >= high` can become true for Comfort, and the value is only ever
-- moved DOWN to just under the threshold, never up, so the `value < low`
-- penalty row is unaffected and no other stat is touched. The override is
-- removed again in the same call, under pcall, and nothing in the builder
-- yields; only Morale tooltips are wrapped at all.

SMRFixPack.Register("MoraleComfortTooltip", {
	title = "Morale tooltip stops listing a Comfort bonus the game does not apply",
	apply = function()
		local C = rawget(_G, "Colonist")
		if type(C) ~= "table" or type(C.UIStatUpdate) ~= "function" then
			return "Colonist.UIStatUpdate not found (game update changed it?)"
		end
		if type(C.GetProperty) ~= "function" and type(rawget(_G, "PropertyObject")) ~= "table" then
			return "GetProperty not reachable (game update changed it?)"
		end

		-- Reports whether the shipped high-Comfort morale bonus is still absent.
		-- Cannot be checked at apply time (g_Consts is a GameVar and UpdateMorale
		-- is compiled), so it is documented rather than asserted; the fix only
		-- ever hides a row, so being wrong costs a missing line, not a wrong number.
		local hidden = 0

		local orig_update = C.UIStatUpdate
		-- (QA 2026-07-25) pass varargs and returns through: the live caller hands
		-- a second argument (ipColonist.lua:134) that the shipped body ignores
		-- today — FIX_POLICY §1.4 says don't truncate what we don't consume.
		function C:UIStatUpdate(win, ...)
			orig_update(self, win, ...)

			if type(win) ~= "table" then return end
			local progress = win.idProgress
			if type(progress) ~= "table" or type(progress.GetBindTo) ~= "function" then return end
			if progress:GetBindTo() ~= "Morale" then return end

			local shipped = win.GetRolloverText
			if type(shipped) ~= "function" then return end

			win.GetRolloverText = function(w)
				local obj = w and w.context
				if type(obj) ~= "table" or type(obj.GetProperty) ~= "function" then
					return shipped(w)
				end
				local scale = const.Scale and const.Scale.Stat
				local consts = rawget(_G, "g_Consts")
				local high = consts and consts.HighStatLevel
				if type(high) ~= "number" or type(scale) ~= "number" or scale == 0 then
					return shipped(w)
				end
				high = high / scale

				local real_get = obj.GetProperty
				local previous = rawget(obj, "GetProperty")
				-- FIX (F20): report Comfort as just below the high threshold, so
				-- the shipped row for a bonus that UpdateMorale no longer grants
				-- is not printed. Never moves the value up, so the low-Comfort
				-- penalty row is unchanged.
				rawset(obj, "GetProperty", function(o, id, ...)
					local v = real_get(o, id, ...)
					if id == "Comfort" and type(v) == "number" and v >= high then
						hidden = hidden + 1
						return high - 1
					end
					return v
				end)
				local ok, res = pcall(shipped, w)
				rawset(obj, "GetProperty", previous)
				if ok then return res end
				return nil
			end
		end

		SMRFixPack.MoraleComfortTooltip = { Hidden = function() return hidden end }
	end,
})
