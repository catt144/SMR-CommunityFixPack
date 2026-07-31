-- F26: every missile in a bombardment volley flies in from the same direction,
-- so a barrage that should look like a scatter of incoming fire arrives as a
-- rank of parallel missiles.
--
-- Defect: `WaitBombard` (Lua\Bombardment.lua:55-154) draws one base direction
-- for the volley and then, per missile, computes a deviated one and throws it
-- away:
--     local dir, angle = GenerateDir()            -- :73, once for the volley
--     ...
--     local spawn_dir = GenerateDir(dir, angle)   -- :82, deviated per missile
--     local spawn_pos = dest_pos + SetLen(dir, travel_dist)   -- :83, uses `dir`
-- `spawn_dir` is never read again anywhere in the function. `GenerateDir(dir,
-- angle)` exists precisely to jitter the direction — it re-rolls the elevation
-- by up to ±10° around the volley's angle (`:38-50`) — so the intent of :82 is
-- unambiguous, and :83 simply names the wrong variable. Meteors do the
-- equivalent thing correctly (Meteors.lua:106-107). Visible in Mystery 7's
-- bombardments.
--
-- Patch approach: full replacement of `WaitBombard`, because the defect is one
-- expression in the middle of a 100-line function with no seam anywhere near it.
-- Every hook that could reach the missile runs too late: `missile:SetPos` has
-- already placed it at `spawn_pos` (:85) and the visual axis at :93-96 is derived
-- from the same local, so correcting the object after the fact would leave a
-- missile flying along one line while pointing down another. The body below is a
-- copy of Bombardment.lua:55-154 (shipped Src, game 1.0.7.396349), byte-identical except
-- the single line marked `-- FIX:`.
--
-- `GenerateDir` (Bombardment.lua:38-50) and `travel_dist` (:53) are file-locals
-- in the shipped file and therefore unreachable from here, so both are copied in
-- as well — `GenerateDir` verbatim, so it consumes exactly the same number of
-- `SessionRandom` draws in the same order and volleys stay deterministic.
--
-- One deliberate divergence from the copy: the shipped `assert(false, "Failed to
-- find bombard pos!")` at :59 is dropped. `assert` does not unwind mod code in
-- this engine — it prints and execution continues — so copying it would add a
-- log line and change nothing; the `return false` beside it is what actually
-- handles the case and is kept.

SMRFixPack.Register("BombardmentSpread", {
	title = "Bombardment missiles come in from spread directions instead of in parallel",
	apply = function()
		-- FIX (QA 2026-07-25): HitsDome/GetTimeToImpact are declared on
		-- BaseMeteor (Meteors.lua:443/:453), not on BombardMissile — at apply
		-- time classes are not flattened, so checking BombardMissile finds nil
		-- and deactivated this fix on every launch (the F64 lesson). Check the
		-- DECLARING class. SessionRandom is a GameVar (Lua\_init.lua:5) and does
		-- not exist at apply time either — the body reads it at call time, which
		-- is fine, so it is not preflighted at all.
		local err = SMRFixPack.Require("BombardmentSpread", {
			{ global = "WaitBombard" },
			{ class = "BombardMissile",
			  reason = "BombardMissile not found (game update changed it?)" },
			{ class = "BaseMeteor", method = "HitsDome",
			  reason = "BaseMeteor.HitsDome/GetTimeToImpact not found (game update changed it?)" },
			{ class = "BaseMeteor", method = "GetTimeToImpact",
			  reason = "BaseMeteor.HitsDome/GetTimeToImpact not found (game update changed it?)" },
			{ global = "SetLen", reason = "SetLen/sincos not found (game update changed it?)" },
			{ global = "sincos", reason = "SetLen/sincos not found (game update changed it?)" },
			{ global = "GetRandomPassableAroundOnMap",
			  reason = "the bombardment helpers are gone (game update changed it?)" },
			{ global = "AddObjectToNotification",
			  reason = "the bombardment helpers are gone (game update changed it?)" },
		})
		if err then return err end

		-- Copy of the file-local Bombardment.lua:38-50.
		local function GenerateDir(dir, angle)
			local min, max = 45 * 60, 90 * 60
			dir = dir or point(SessionRandom:Random(-4096, 4096), SessionRandom:Random(-4096, 4096))
			angle = angle and Clamp(angle + SessionRandom:Random(-10 * 60, 10 * 60), min, max) or SessionRandom:Random(min, max)
			local s, c = sincos(angle)
			if c == 0 then
				dir = point(0, 0, 4096)
			else
				dir = dir:SetZ(MulDivRound(dir:Len2D(), s, c))
			end

			return dir, angle
		end

		-- Copy of the file-local Bombardment.lua:53.
		local travel_dist = 1000 * guim

		SMRFixPack.BombardmentSpread = { GenerateDir = GenerateDir }

		-- Source: Lua\Bombardment.lua:55-154 (ModTools\Src, game 1.0.7.396349).
		-- `StartBombard` (:156-161) resolves this name at call time, so it picks
		-- the replacement up.
		local replacement
		replacement = function(obj, radius, count, delay_min, delay_max)
			local map = MainMap
			local pos = IsValid(obj) and obj:GetPos() or IsPoint(obj) and obj or GetRandomPassable(map)
			if not pos then
				-- shipped line was: assert(false, "Failed to find bombard pos!")
				return false
			end
			PlayFX({
				actionFXClass = "Bombard",
				actionFXMoment = "start",
				map = map,
			})
			radius = radius or 0
			delay_min = delay_min or 0
			delay_max = delay_max or 0
			count = count or 1
			local spawned = {}
			local hits = 0
			local dir, angle = GenerateDir()
			local max_travel_time = 0
			while count > 0 do
				count = count - 1
				local dest_pos = GetRandomPassableAroundOnMap(map, pos, radius) or GetRandomPassable(map)
				if not dest_pos then
					break
				end
				dest_pos = dest_pos:SetZ(map:GetHeight(dest_pos))
				local spawn_dir = GenerateDir(dir, angle)
				-- FIX: shipped line used `dir`, discarding the per-missile spawn_dir
				-- FIX: computed on the line above, so every missile in the volley came
				-- FIX: in along the same line (compare Meteors.lua:106-107).
				local spawn_pos = dest_pos + SetLen(spawn_dir, travel_dist)
				local missile = PlaceObject("BombardMissile", {start = spawn_pos, dest = dest_pos}, map)
				missile:SetPos(spawn_pos)
				local dome, dome_pt, dome_normal = missile:HitsDome()
				if dome_pt then
					dest_pos = dome_pt
					missile.dest = dome_pt
				end
				local travel_time = missile:GetTimeToImpact()
				missile:SetPos(dest_pos, travel_time)
				local dir = dest_pos - spawn_pos
				local norm_dir = point(dir:y(), -dir:x(), 0)
				missile:SetAxis(norm_dir)
				missile:SetAngle(-90*60 + atan(dir:z(), dir:Len2D()))
				spawned[missile] = true
				map.g_IncomingMissiles[missile] = true
				CreateGameTimeThread(function()
					AddObjectToNotification(missile, nil, "Bombardment", map)
					Msg("IncomingMissile", missile)
					PlayFX("Move", "start", missile, nil, nil, dir)
					local interrupted, intercepted = WaitMsg(missile, travel_time)
					PlayFX("Move", "end", missile, nil, nil, dir)
					if intercepted then
						PlayFX("AirExplosion", "start", missile)
					elseif dome_pt then
						PlayFX("DomeExplosion", "start", missile)
						missile:CrackDome(dome, dome_pt, dome_normal)
					elseif not interrupted then
						PlayFX("GroundExplosion", "start", missile)
						missile:Explode()
					end
					map.g_IncomingMissiles[missile] = nil
					RemoveObjectFromNotification(missile, "Bombardment", map)
					Msg("BombardMissileHit")
					if not interrupted and not dome_pt then
						missile:MapDelete(dest_pos, 20*guim, missile.explode_decal_name)
						local explode_decal = PlaceObject(missile.explode_decal_name, nil, missile)
						explode_decal:SetPos(dest_pos)
						explode_decal:SetAngle(AsyncRand(360*60))
						explode_decal:SetScale(50 + AsyncRand(50))
						local fade_time = missile.explode_decal_fade
						for opacity = 100, 0, -5 do
							Sleep(fade_time / 20)
							if not IsValid(explode_decal) then return end
							explode_decal:SetOpacity(opacity)
						end
						DoneObject(explode_decal)
					end
					if IsValid(missile) then
						DoneObject(missile)
					end
				end)
				Sleep(SessionRandom:Random(delay_min, delay_max))
			end
			while true do
				local rockets = 0
				for missile in pairs(spawned) do
					if IsValid(missile) then
						rockets = rockets + 1
					end
				end
				if rockets == 0 then
					break
				end
				WaitMsg("BombardMissileHit", 10000)
			end
			PlayFX({
				actionFXClass = "Bombard",
				actionFXMoment = "end",
				map = map,
			})
		end

		return SMRFixPack.SetGlobal("WaitBombard", replacement,
			"could not install the WaitBombard replacement")
	end,
})
