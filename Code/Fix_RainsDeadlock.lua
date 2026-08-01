-- F81 (rains half, F81b): one collision with any other disaster kills a rain
-- type for the rest of the save.
-- F86 Tier-1 REWRITE (2026-08-01, spec `docs/reports/SAVE_SAFETY_REDESIGN.md`
-- §6.2a-B): layer 2 — the loop replacement is gone; vanilla's loop stays and
-- the deadlock is broken at its source. Carries the C34 stale-state rider.
--
-- Defect (TerraformingDisasters.lua:310-316, game 1.0.7.396349):
--     function RainsDisasterLoop(settings)
--         while true do
--             Sleep(settings.spawntime + AsyncRand(settings.spawntime_random))
--             CreateGameTimeThread(RainsDisasterActivation, settings)
--             WaitMsg("RainDisasterEnd")          -- NO TIMEOUT
--         end
--     end
-- `RainsDisasterActivation` opens with `if IsDisasterActive() or
-- IsDisasterPredicted() then return end` (:277) — it returns WITHOUT starting
-- a rain, `FinishRainProcedure`'s `Msg("RainDisasterEnd")` (:267) never comes,
-- and the untimed WaitMsg blocks forever. The collision window is every other
-- disaster's ACTIVE phase plus every WARNING window — up to 75h each with
-- sensor towers at the cap — so on a long save a collision is a certainty.
-- Nothing rescues it: UpdateRainsThreads REUSES any valid activation thread
-- (:412), and a thread blocked in WaitMsg is perfectly valid.
--
-- Fix shape (layer 2, FIX_POLICY §3a — replaces the bounded-timeout loop copy
-- shipped until 2026-08-01; F86 measured that an uninstalled player kept our
-- loop body FOREVER, so the copy had to go): wrap `RainsDisasterActivation`,
-- mirroring vanilla's own collision test BEFORE the call —
--     IsDisasterActive() or IsDisasterPredicted()  (both synchronous)
--       ->  Msg("RainDisasterEnd", MainMap, settings.type or "normal"); return
--     otherwise  ->  return orig(settings)         (tail call, nothing after)
-- The posted Msg wakes the loop immediately and vanilla re-rolls a fresh spawn
-- — a collided cycle costs one re-roll (fredware's immediate-retry behaviour,
-- delivered through vanilla's own loop instead of a replaced one). Why the Msg
-- cannot outrun the WaitMsg: GT creation DEFERS — the loop is already blocked
-- in WaitMsg when the activation body first runs (measured twice 2026-08-01,
-- incl. the GT-creates-GT form with a live WaitMsg receipt; ENGINE_FACTS).
-- `fixed_loop`, the `RainsDisasterLoop` replacement and the
-- `SMRFixPack.RainsFixedLoop` probe surface are DELETED; the global stays
-- vanilla's.
--
-- The migration pass (OnMsg.PostLoadGame, replaces RefreshRainsLoops):
-- persisted activation threads resume whatever body their save captured — the
-- unbounded vanilla body, or our old bounded copy (which an uninstalled player
-- could otherwise never shed). Each entry with a valid activation_thread not
-- yet stamped by the CURRENT pack version is DeleteThread-ed and recreated on
-- VANILLA's `RainsDisasterLoop`, then stamped `SMRFixPack_loop_version` (the
-- shipped `SMRFixPack_fixed_loop` boolean now just means "old fixed body" —
-- treated as unmigrated, cleared on migration). Settings resolve by `data.id`
-- first, else by a UNIQUE `settings.type == rain_type` match over
-- `Presets.MapSettings.RainsDisaster` (the id-less entries the shipped pass
-- skipped — `test 2i`'s `toxic` entry has `id = nil`), else leave-and-log.
-- `main_thread` is never touched — an in-flight warning or rain continues
-- undisturbed. Marker discipline (FIX_POLICY §3): fields inside vanilla's own
-- GameVar entries survive reuse (:411-415), vanish on recreation, and are
-- ignored by a save loaded without the mod.
--
-- ⭐ C34 rider (audit adoption 2026-08-01 — rides this pass, no module of its
-- own): the sibling stale-state class fredware heals and we did not. BEFORE
-- the loop migration, the same pass repairs:
--   * structure — a missing/non-table `RainsDisasterThreads` is recreated as
--     `{}`; dead `soil_thread`s are set to `false`;
--   * stale-ACTIVE — a `g_RainDisaster` rain type whose entry's `main_thread`
--     is dead/invalid heals through VANILLA's own `FinishRainProcedure`
--     (TerraformingDisasters.lua:247-274 — clears the entry's fields, label
--     modifiers, notifications, sets `g_RainDisaster = false`, posts
--     `Msg("RainDisasterEnd")`, which also frees any still-deadlocked
--     persisted loop);
--   * invalid values — a truthy `g_RainDisaster` matching no known rain type
--     (preset `type`s / registry keys) cannot go through FinishRainProcedure
--     (its notif_prefix lookup would concatenate nil): manual fallback,
--     `g_RainDisaster = false` + `Msg("RainDisasterEnd", MainMap, "normal")`,
--     logged.
-- Order within the pass: structure → stale-ACTIVE heal → loop migration.
-- ⚠ fredware's WaitCurrentDisaster/loop-body replacements are §3a violations —
-- his exposure, not a pattern; nothing here copies them.
--
-- §3a COMPLIANCE, stated: no mod-owned thread body; the wrapper does all its
-- work before the call and tail-returns; the migration/heal pass is a
-- synchronous OnMsg handler using only vanilla primitives (DeleteThread /
-- CreateGameTimeThread / FinishRainProcedure / Msg).
-- SAVE FOOTPRINT (FIX_POLICY §3): `SMRFixPack_loop_version` fields inside
-- existing `RainsDisasterThreads` entries (inert data; the legacy
-- `SMRFixPack_fixed_loop` boolean is cleared as entries migrate).

local FIX_ID = "RainsDeadlock"

local log = SMRFixPack.Log

SMRFixPack.Register(FIX_ID, {
	title = "A rain that collides with another disaster retries instead of never raining again",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "RainsDisasterActivation" },
			{ global = "RainsDisasterLoop" },
			{ global = "IsDisasterActive" },
			{ global = "IsDisasterPredicted" },
			{ global = "FinishRainProcedure" },
		})
		if err then return err end

		local orig = rawget(_G, "RainsDisasterActivation")
		local function activation_wrapper(settings)
			-- vanilla's own collision test (:277), mirrored BEFORE the call: on
			-- the early-return case the loop's untimed WaitMsg would never be
			-- signalled — post the Msg it waits for and let vanilla re-roll
			if IsDisasterActive() or IsDisasterPredicted() then
				log("%s: rain activation collided with an active/predicted disaster — posting RainDisasterEnd so the loop re-rolls",
					FIX_ID)
				Msg("RainDisasterEnd", MainMap, settings and settings.type or "normal")
				return
			end
			return orig(settings)
		end
		return SMRFixPack.SetGlobal("RainsDisasterActivation", activation_wrapper,
			"could not install the RainsDisasterActivation wrapper")
	end,
})

-- The migration + C34 heal pass (see header). Exposed for the console and the
-- TestKit; returns the counts table. Idempotent per version: a second run in
-- the same save finds every entry stamped and nothing stale.
function SMRFixPack.MigrateRainsState()
	local counts = { structure = 0, healed = 0, migrated = 0 }

	-- C34: structure first — later steps index this table
	local threads = rawget(_G, "RainsDisasterThreads")
	if type(threads) ~= "table" then
		log("%s: RainsDisasterThreads was %s — recreated as an empty table (C34 structure repair)",
			FIX_ID, tostring(threads))
		RainsDisasterThreads = {}
		threads = rawget(_G, "RainsDisasterThreads")
		if type(threads) ~= "table" then return counts end -- registry not writable; nothing safe to do
		counts.structure = counts.structure + 1
	end
	for rain_type, data in pairs(threads) do
		if type(data) == "table" and data.soil_thread and not IsValidThread(data.soil_thread) then
			data.soil_thread = false
			counts.structure = counts.structure + 1
			log("%s: '%s' had a dead soil_thread — set to false (C34 structure repair)",
				FIX_ID, tostring(rain_type))
		end
	end

	local presets = rawget(_G, "Presets")
	presets = type(presets) == "table" and presets.MapSettings or nil
	presets = type(presets) == "table" and presets.RainsDisaster or nil

	-- C34: stale-ACTIVE — the save says a rain is running but no thread runs it
	local active = rawget(_G, "g_RainDisaster")
	if active then
		local entry = type(threads[active]) == "table" and threads[active] or nil
		if not (entry and IsValidThread(entry.main_thread)) then
			local known = entry ~= nil
			if not known and presets then
				for _, s in ipairs(presets) do
					if s.type == active then known = true break end
				end
			end
			if known then
				log("%s: stale-ACTIVE rain '%s' (main_thread dead) — healing through vanilla FinishRainProcedure (C34)",
					FIX_ID, tostring(active))
				FinishRainProcedure(active)
			else
				log("%s: invalid g_RainDisaster value '%s' (no such rain type) — cleared manually (C34)",
					FIX_ID, tostring(active))
				g_RainDisaster = false
				Msg("RainDisasterEnd", MainMap, "normal")
			end
			counts.healed = counts.healed + 1
		end
	end

	-- loop migration — every not-yet-stamped persisted loop moves onto
	-- VANILLA's body (main_thread never touched)
	local version = SMRFixPack.PackVersion()
	if not version then
		log("%s: pack version unreadable — persisted rain loops left unmigrated this load", FIX_ID)
		return counts
	end
	for rain_type, data in pairs(threads) do
		if type(data) == "table" and IsValidThread(data.activation_thread)
				and data.SMRFixPack_loop_version ~= version then
			local settings = presets and data.id and presets[data.id] or nil
			if not settings and presets then
				-- the id-less case: a UNIQUE type match resolves it, anything
				-- ambiguous is left alone and reported
				local match, hits = nil, 0
				for _, s in ipairs(presets) do
					if s.type == rain_type then match, hits = s, hits + 1 end
				end
				if hits == 1 then settings = match end
			end
			if settings then
				DeleteThread(data.activation_thread)
				data.activation_thread = CreateGameTimeThread(RainsDisasterLoop, settings)
				data.SMRFixPack_loop_version = version
				data.SMRFixPack_fixed_loop = nil
				counts.migrated = counts.migrated + 1
				log("%s: '%s' rain loop migrated onto vanilla's body (settings '%s', version %s)",
					FIX_ID, tostring(rain_type), tostring(settings.id), version)
			else
				log("%s: '%s' rain loop left as-is — settings unresolved (id '%s') — please report this log",
					FIX_ID, tostring(rain_type), tostring(data.id))
			end
		end
	end
	return counts
end

OnMsg.PostLoadGame = SMRFixPack.WhenActive(FIX_ID, function()
	local ok, err = pcall(SMRFixPack.MigrateRainsState)
	if not ok then log("%s: rains migration/heal pass failed: %s", FIX_ID, tostring(err)) end
end)
