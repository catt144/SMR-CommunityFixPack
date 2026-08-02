-- F97 (C23 item 1): the dust-devil scheduler multiplies its COUNT by a field
-- that is a PROBABILITY, so the authored count range is unreachable.
--
-- Defect: the natural scheduler draws its wave size as
--     local count = SessionRandom:Random(descr.count_min, descr.count_max) * descr.spawn_chance / 100
-- (Lua\DustDevils.lua:216, inside the GlobalGameTimeThread("DustDevils", ...)
-- body at :188-241). Lua's `/` here is the engine's integer divide, so the
-- product truncates toward zero. Two consequences, both contradicting the
-- fields' own help text ("Lo Range / Hi Range - how many Dust Devils to spawn",
-- :9-10):
--   * count_max is UNREACHABLE for every descriptor with spawn_chance < 100;
--   * the result can be 0 while count_min is 1.
-- DustDevils_High is the clean example: spawn_chance 75, count 1..3 -> 0, 1 or
-- 2, never 3. DustDevils_VeryHigh_3 is the extreme: authored 6..8 at 50%
-- (Data\MapSettings-DustDevils.lua:111-127), it can only ever produce 3 or 4 —
-- the authored range cannot occur at all.
--
-- Intent, established by three independent controls (BUGS C23):
--   * the SAME FILE's marker path uses the sibling field as a Bernoulli gate —
--     `SessionRandom:Random(100) < descr.marker_spawn_chance` (:169), the field
--     literally named "Spawn Chance (%)";
--   * MapSettings_Meteor declares the same three-field trio with an identical
--     property idiom (multispawn_chance, default 30, min 1, max 100,
--     Meteors.lua:7 against spawn_chance, DustDevils.lua:8) and uses it
--     gate-then-count: the chance GATES (`if chance < meteors.multispawn_chance`,
--     Meteors.lua:284-290) and the count is drawn INDEPENDENTLY and never
--     multiplied (:137);
--   * an outside developer (fredware, workshop 3775120166) read the same line
--     the same way, logging his repair's reason as "vanilla_scaled_spawn_count".
-- There are ZERO examples of chance-as-multiplier anywhere in Lua\.
--
-- ⚠️ What the controls do NOT settle is the tuned RATE. DustDevils_Low
-- accidentally approximates a gate today (50% x count 1..2 truncates to 0-or-1),
-- so the shipped rates MAY have been tuned around the truncation. That residual
-- is why this repair is a provisional owner decision, reviewed by chain prompt 12.
--
-- ── Patch approach ──────────────────────────────────────────────────────────
-- FIX_POLICY §3a LAYER 3 (patch a synchronous input, keep vanilla's body), via a
-- §1.4b chained POST-wrapper on the global OverrideDisasterDescriptor.
--
-- ⛔ THIS IS NOT THE ROUTE THE C23 ENTRY SPECCED, and the divergence is the
-- finding, not an improvisation. The entry states "the only precise route is
-- owning the scheduler body" through GlobalGameTimeThreadFuncs["DustDevils"] —
-- a §1.5 reconstruction, a mod-owned SLEEPING GAME-TIME THREAD in every save (a
-- 14th §3a exposed site), a version-latched one-shot restart to reach existing
-- saves, and a hand-the-loop-back-to-vanilla uninstall gate. That claim is
-- falsified by Src: the count line reads its three numbers from a descriptor the
-- thread obtains from a SYNCHRONOUS getter, exactly once per wave, so changing
-- what it READS reaches the defect without replacing what it DOES. §3a's layer
-- ordering (3 -> 2 -> 1) is binding, so layer 3 is not merely cheaper, it is
-- required where it exists. Owner confirmed the route 2026-08-02.
--
-- Why the gate can be PRE-ROLLED into the descriptor: the thread reads the
-- descriptor exactly once per wave and the count line consumes exactly that
-- read. GetDustDevilsDescr is called at :193 (before the first wave), then once
-- per wave at :234, with :237 re-polling only while it returns nil (terraformed
-- past the DustStormStop threshold — no roll is consumed there, because we pass
-- nil straight through). So one gate roll per count draw, 1:1, forever.
--
-- We therefore hand the thread a plain-data COPY of the descriptor with
-- spawn_chance forced to 100 — making vanilla's multiply the identity — and
-- count_min/count_max either left alone (gate passed) or set to 0/0 (gate
-- failed). Vanilla's line 216 then computes gate-then-count with its own
-- unmodified code:
--     gate passed -> Random(count_min, count_max) * 100 / 100 = the full range
--     gate failed -> Random(0, 0)              * 100 / 100 = 0
--
-- Why OverrideDisasterDescriptor and not GetDustDevilsDescr: F93
-- (Fix_DustDevilsDescrMap) already replaces GetDustDevilsDescr, and its
-- DataPatch runner RE-INSTALLS its own body whenever it finds the global holding
-- anything else — so a wrapper there would be silently unwrapped on every
-- re-check. OverrideDisasterDescriptor sits one level down, is called by F93's
-- body (Fix_DustDevilsDescrMap.lua:67) and by vanilla's (DustDevils.lua:65)
-- alike, so this module is correct with F93 on OR off and the two never contend
-- for the same global.
--
-- Caller enumeration, as §3a layer 3 requires before choosing a key.
-- OverrideDisasterDescriptor has exactly FOUR callers in Src, one per disaster:
-- ColdWave.lua:48, DustDevils.lua:65, DustStorm.lua:61, Meteors.lua:262. Each
-- passes its own MapSettings subclass, so `original.class` separates them
-- exactly; the other three are returned untouched. (The live definition is
-- TerraformingDisasters.lua:54, which shadows the trivial passthrough at
-- MapSettings.lua:31 — mod code loads after both, so the wrapper captures the
-- terraforming one.)
--
-- ⚠️ Why a COPY and not a mutation: OverrideDisasterDescriptor returns the
-- PRESET OBJECT itself (`return original` :56/:62/:89) or another preset from
-- the same group (`return settings` :97). Both are shared, live objects — the
-- table the map editor and every other reader see — so a per-wave mutation would
-- be a permanent global edit. It also returns NIL once terraforming pushes
-- Atmosphere past the DustStormStop threshold (:69), which is passed through
-- unchanged so the scheduler's own day-long re-poll still works.
--
-- ⚠️ Why the copy must resolve CLASS DEFAULTS: preset data only stores
-- non-default values, so DustDevils_VeryHigh_1 declares count_max 3 and no
-- count_min at all — count_min 2 comes from the class property default
-- (DustDevils.lua:9). A raw pairs() copy would hand the thread count_min = nil
-- and Random(nil, ...) would error. The copy therefore walks the DECLARED
-- PROPERTY LIST and reads each id through normal indexing, which resolves
-- instance value first and class default second.
--
-- ── §3a: NO NEW EXPOSED SITE, and nothing executable enters the save ────────
-- Route (a) — our frame never sits below a yield: the wrapper is synchronous and
--   contains no Sleep/WaitMsg; it returns before the scheduler's next Sleep.
-- Route (b) — the persisted thread's locals hold the returned TABLE, never our
--   function. Our function is reachable only from _G.OverrideDisasterDescriptor,
--   which is a plain global and is NOT in PersistableGlobals (only the thread
--   handle "DustDevils" is, Lua\Config\_fixup.lua:9-16).
-- Route (c) — we store nothing ourselves. The one thing of ours that reaches a
--   save is the descriptor copy, stored by VANILLA in its own thread local, and
--   it is INERT PLAIN DATA: plain_copy refuses to copy any function, userdata or
--   thread value and returns nil instead, in which case we hand back the
--   untouched preset and this fix simply does nothing that wave.
--
-- Uninstall behaviour (the Fix_MeteorFrequency trap, F86 Site 1, does not apply
-- here — we own no body and no thread): after removal the scheduler is vanilla's
-- own code holding one plain table. At the end of its current wave it calls
-- :234 and gets the real preset back, so the copy is discarded within ONE wave
-- and the colony keeps its dust devils. Worst case is a single wave whose size
-- came from a pre-roll made while the pack was installed. Marker threads created
-- by a fresh map-gen keep the copy for the session's lifetime, but read only
-- marker_spawntime / marker_spawntime_random / marker_spawn_chance /
-- warning_time and the spawn geometry — all faithful copies, and NONE of the
-- three fields this fix changes (DustDevils.lua:161-179 enumerated).
--
-- The F88 trap does not apply either: nothing here restarts a thread, so no
-- pending wave timer is ever re-rolled and no version latch is needed. Existing
-- saves are reached by themselves — the running thread picks the fix up at its
-- next descriptor re-read, i.e. within one wave, with no load-time action at all.
--
-- ⚠️ Honest limits.
--   * The repair consumes one extra SessionRandom draw per wave, so a save's
--     deterministic stream diverges from an unmodded run of the same save. That
--     is inherent to any gate (fredware's fix does the same) and reverts on
--     removal.
--   * The self-check CANNOT see line 216 — no Lua read reaches a thread body's
--     source. If a future game patch repairs the multiply itself, this module
--     composes rather than conflicts: their gate would test our spawn_chance of
--     100 and always pass, leaving our own pre-roll as the effective gate. The
--     behaviour stays correct; one draw is wasted. Recorded rather than guarded,
--     because the alternative is a guard that cannot be written.

local FIX_ID = "DustDevilSpawnGate"

-- The preset class the count line belongs to. Every other disaster's descriptor
-- passes through this wrapper untouched.
local DUST_DEVIL_CLASS = "MapSettings_DustDevils"

-- Names the residue in a save (the §3a "inert, but named and disclosed" rung)
-- and makes the wrapper a no-op if it is ever handed its own output.
local MARK = "SMRFixPack_spawn_gate"

local orig            -- vanilla's OverrideDisasterDescriptor, captured at apply
local installed = false
local wrapper         -- forward declaration; defined at apply

-- A plain-data snapshot of a preset: every DECLARED property, read through
-- normal indexing so class defaults resolve. Returns nil rather than an
-- incomplete or unsafe copy — the caller then leaves vanilla's descriptor alone.
local function plain_copy(descr)
	local props = descr.GetProperties and descr:GetProperties() or descr.properties
	if type(props) ~= "table" or #props == 0 then return end

	local copy = {}
	for i = 1, #props do
		local id = props[i].id
		if id then
			local value = descr[id]
			local t = type(value)
			-- §3a route (c): a copy that carried a function value would put mod-
			-- reachable code in the save. Refuse rather than persist one.
			if t == "function" or t == "userdata" or t == "thread" then return end
			copy[id] = value
		end
	end

	-- the three the count line reads must all have survived the walk, or this is
	-- not a safe substitute for the preset
	if type(copy.spawn_chance) ~= "number"
	or type(copy.count_min) ~= "number"
	or type(copy.count_max) ~= "number" then
		return
	end

	-- Self-describing for a save inspector and for the D13 cleaner; neither is
	-- read by the game. `id` is carried EXPLICITLY because the property walk
	-- cannot reach it: `Id` is a declared Preset property (CommonLua\Preset.lua
	-- :42) but it is ACCESSOR-BACKED — the value lives in the lowercase `self.id`
	-- field (:96) behind `Preset:GetId` (:400) — so plain indexing of `Id` reads
	-- nil. Observed 2026-08-02 on PT-61's first WAVE line, which printed
	-- `id=nil` for a copy while vanilla's own descriptor prints its id.
	-- ⚠️ Honest limit of this copier, stated once: it snapshots PLAIN-FIELD
	-- properties. Any property served by a `GetX()` accessor rather than a
	-- stored field is not resolved, and `Id` is the only one this class has that
	-- matters. That is deliberate — the alternative is a native `GetProperty`
	-- call per property per wave, and NO consumer of this descriptor reads an
	-- accessor-backed property (all of them are plain numbers and booleans;
	-- enumerated in the header).
	copy.class = descr.class
	copy.id = descr.id
	copy[MARK] = true
	return copy
end

-- The repair itself, split out so the probe can exercise it with an explicit
-- roll and consume no SessionRandom draws. `roll` is 0..99, vanilla's idiom.
-- Returns the descriptor to hand back (the original when nothing is owed).
local function gate_descriptor(descr, roll)
	if type(descr) ~= "table" or descr[MARK] then return descr end
	if descr.class ~= DUST_DEVIL_CLASS then return descr end

	local chance = descr.spawn_chance
	if type(chance) ~= "number" or chance >= 100 then
		-- vanilla's multiply is already the identity; nothing to repair, and no
		-- copy is put in the save at all (DustDevils_VeryHigh is such a preset)
		return descr
	end

	local copy = plain_copy(descr)
	if not copy then return descr end

	-- FIX (F97): spawn_chance is a probability, not a count multiplier. Roll it
	-- as the gate the sibling path uses (DustDevils.lua:169), then let vanilla's
	-- own line 216 draw the count from the authored range.
	copy.spawn_chance = 100
	if not (type(roll) == "number" and roll < chance) then
		copy.count_min, copy.count_max = 0, 0
	end
	return copy
end

local function set_installed(want)
	if not orig then return end
	local cur = rawget(_G, "OverrideDisasterDescriptor")
	if want and cur ~= wrapper then
		_G.OverrideDisasterDescriptor = wrapper
	elseif not want and cur == wrapper then
		_G.OverrideDisasterDescriptor = orig
	end
end

-- The content half of the self-check: the three fields this fix manipulates must
-- still exist as numbers on the shipped presets. It CANNOT run at apply time —
-- presets do not exist when mod code loads on a cold boot, so absence there
-- proves nothing and testing it would be the F75 false-inactive bug. It runs on
-- the shared DataLoaded/DataChanged runner instead, which also owns the F87
-- enable-path triggers. On a latch the vanilla body is RESTORED, so an entry
-- reporting `inactive` is never quietly still installed.
-- No `changed_class` filter, for F93's reason: the presets are instances of the
-- SUBCLASS MapSettings_DustDevils while the group lives under the root preset
-- class MapSettings, so a class-name filter could miss its own re-arm.
local verify = SMRFixPack.DataPatch(FIX_ID, {
	pass = function(ctx)
		if not installed then return end   -- apply() already declined; nothing to verify
		local presets = rawget(_G, "Presets")
		local settings = type(presets) == "table" and presets.MapSettings
		local group = type(settings) == "table" and settings.DustDevils
		if type(group) ~= "table" or not next(group) then
			-- before DataLoaded this only means "presets not loaded yet"
			if ctx.data_loaded then
				ctx.patched = true
				set_installed(false)
				ctx.latch("Presets.MapSettings.DustDevils not found (game update changed it?)",
					"Presets.MapSettings.DustDevils not found")
			end
			return
		end

		-- at least one shipped preset must still carry the trio, or the fields
		-- this fix rewrites are gone
		local ok = false
		for _, preset in ipairs(group) do
			if type(preset.spawn_chance) == "number"
			and type(preset.count_min) == "number"
			and type(preset.count_max) == "number" then
				ok = true
				break
			end
		end
		if not ok then
			ctx.patched = true
			set_installed(false)
			ctx.latch("dust-devil presets no longer carry spawn_chance/count_min/count_max (game update changed them?)",
				"dust-devil preset fields not found")
			return
		end

		ctx.patched = true
		set_installed(true)
		ctx.heal()
	end,
})

SMRFixPack.Register(FIX_ID, {
	title = "Dust devil waves use their authored count range instead of being scaled down by the spawn chance",
	-- exposed for the probe: the repair with the RNG lifted out, so the probe can
	-- assert the transformation without perturbing the session's random stream
	gate_descriptor = gate_descriptor,
	apply = function()
		-- SessionRandom is a GameVar (Lua\_init.lua) and does not exist at apply
		-- time; the body reads it at call time, so it is not preflighted (the
		-- Fix_BombardmentSpread precedent).
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "OverrideDisasterDescriptor" },
			-- the scheduler that consumes the descriptor; if it is gone, the
			-- reasoning above no longer describes the game
			{ global = "GetDustDevilsDescr" },
		})
		if err then return err end
		orig = orig or rawget(_G, "OverrideDisasterDescriptor")

		wrapper = wrapper or function(original)
			local descr = orig(original)
			if not SMRFixPack.IsActive(FIX_ID) then return descr end
			local disabled = rawget(_G, "SMRFixPack_Disabled")
			if type(disabled) == "table" and disabled[FIX_ID] then return descr end
			if type(descr) ~= "table" or descr.class ~= DUST_DEVIL_CLASS then return descr end

			local rand = rawget(_G, "SessionRandom")
			if not rand then return descr end   -- no game session: nothing to gate
			return gate_descriptor(descr, rand:Random(100))
		end

		-- §1.4b: plain assignment reaches the real _G through ModEnvMeta.__newindex,
		-- and the rawget read-back confirms the write landed (the F22 donor).
		local fail = SMRFixPack.SetGlobal("OverrideDisasterDescriptor", wrapper)
		if fail then return fail end
		installed = true
		verify()  -- no-op at apply time (F87); the runner fires itself once the
		          -- classes are built AND the presets are loaded
	end,
})
